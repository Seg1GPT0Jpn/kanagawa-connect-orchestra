/// 音声ファイル（WAV）の読み込み・間引き・波形の外形・音の並び（決定論的）
library;

import 'dart:math' as math;
import 'dart:typed_data';

import '../../audio_tools/domain/pitch.dart';
import 'tone_analysis.dart';

class WavFormatException implements Exception {
  const WavFormatException(this.message);

  final String message;

  @override
  String toString() => message;
}

/// WAV を読み、モノラルの波形（-1〜1）と標本化周波数を返す。
/// PCM（8・16・24・32bit）と 32bit の浮動小数に対応。ステレオは左右を平均する
({Float64List samples, int sampleRate}) readWav(Uint8List bytes) {
  if (bytes.length < 44) throw const WavFormatException('WAV ファイルではありません');
  final b = ByteData.sublistView(bytes);
  String tag(int at) => String.fromCharCodes(bytes.sublist(at, at + 4));
  if (tag(0) != 'RIFF' || tag(8) != 'WAVE') {
    throw const WavFormatException('WAV ファイルではありません');
  }
  int? format, channels, rate, bits;
  int? dataAt, dataLength;
  var p = 12;
  while (p + 8 <= bytes.length) {
    final id = tag(p);
    final size = b.getUint32(p + 4, Endian.little);
    final body = p + 8;
    if (id == 'fmt ' && body + 16 <= bytes.length) {
      format = b.getUint16(body, Endian.little);
      channels = b.getUint16(body + 2, Endian.little);
      rate = b.getUint32(body + 4, Endian.little);
      bits = b.getUint16(body + 14, Endian.little);
      // WAVE_FORMAT_EXTENSIBLE は、中の形式で判断する
      if (format == 0xFFFE && size >= 26 && body + 26 <= bytes.length) {
        format = b.getUint16(body + 24, Endian.little);
      }
    } else if (id == 'data') {
      dataAt = body;
      dataLength = math.min(size, bytes.length - body);
      break;
    }
    p = body + size + (size.isOdd ? 1 : 0);
  }
  if (format == null || dataAt == null) {
    throw const WavFormatException('WAV ファイルの中身が読めません');
  }
  final isFloat = format == 3;
  if (!(format == 1 || isFloat) ||
      channels == null ||
      channels < 1 ||
      rate == null ||
      rate < 4000 ||
      bits == null ||
      !(isFloat ? bits == 32 : const [8, 16, 24, 32].contains(bits))) {
    throw const WavFormatException('この形式の WAV には対応していません（PCM か 32bit 浮動小数）');
  }
  final bytesPer = bits ~/ 8;
  final frameBytes = bytesPer * channels;
  final n = dataLength! ~/ frameBytes;
  final out = Float64List(n);
  for (var i = 0; i < n; i++) {
    var sum = 0.0;
    for (var c = 0; c < channels; c++) {
      final at = dataAt + i * frameBytes + c * bytesPer;
      sum += switch ((isFloat, bits)) {
        (true, _) => b.getFloat32(at, Endian.little),
        (false, 8) => (b.getUint8(at) - 128) / 128,
        (false, 16) => b.getInt16(at, Endian.little) / 32768,
        (false, 24) =>
          ((b.getUint8(at) |
                  b.getUint8(at + 1) << 8 |
                  b.getInt8(at + 2) << 16)) /
              8388608,
        _ => b.getInt32(at, Endian.little) / 2147483648,
      };
    }
    out[i] = sum / channels;
  }
  return (samples: out, sampleRate: rate);
}

/// [from] Hz の波形を [to] Hz に直す（直線でつなぐ。下げるときは先に平均してならす）
Float64List resample(Float64List x, int from, int to) {
  if (from == to || x.isEmpty) return x;
  var src = x;
  // 下げるときは、ざっくり平均してから（折り返しの雑音を減らす）
  final factor = from ~/ to;
  if (factor >= 2) {
    final m = Float64List(x.length ~/ factor);
    for (var i = 0; i < m.length; i++) {
      var s = 0.0;
      for (var k = 0; k < factor; k++) {
        s += x[i * factor + k];
      }
      m[i] = s / factor;
    }
    src = m;
    from = from ~/ factor;
  }
  final n = (src.length * to / from).floor();
  final out = Float64List(n);
  for (var i = 0; i < n; i++) {
    final t = i * from / to;
    final j = t.floor();
    final f = t - j;
    final a = src[math.min(j, src.length - 1)];
    final c = src[math.min(j + 1, src.length - 1)];
    out[i] = a + (c - a) * f;
  }
  return out;
}

/// 波形の外形：[buckets] 個に分けた区間ごとの最小・最大（-1〜1）
List<(double, double)> waveformEnvelope(Int16List pcm, int buckets) {
  if (pcm.isEmpty || buckets <= 0) return const [];
  final out = <(double, double)>[];
  for (var k = 0; k < buckets; k++) {
    final from = pcm.length * k ~/ buckets;
    final to = math.max(from + 1, pcm.length * (k + 1) ~/ buckets);
    var lo = 0, hi = 0;
    for (var i = from; i < to && i < pcm.length; i++) {
      final v = pcm[i];
      if (v < lo) lo = v;
      if (v > hi) hi = v;
    }
    out.add((lo / 32768, hi / 32767));
  }
  return out;
}

/// 録音の中の1つの音
class NoteSegment {
  const NoteSegment({
    required this.midi,
    required this.start,
    required this.end,
    required this.meanCents,
  });

  /// 実音
  final int midi;
  final double start;
  final double end;

  /// 平均律からの平均のずれ（セント）
  final double meanCents;

  double get duration => end - start;
}

/// 分析のフレームを、同じ音が続いた区間（音符）に分ける。[minSeconds] より短い音は除く
List<NoteSegment> segmentNotes(
  List<ToneFrame> frames, {
  required double a4,
  double minSeconds = 0.08,
}) {
  final out = <NoteSegment>[];
  int? midi;
  double start = 0, last = 0, sum = 0;
  var count = 0;
  void close() {
    if (midi != null && last - start >= minSeconds) {
      out.add(
        NoteSegment(
          midi: midi!,
          start: start,
          end: last,
          meanCents: sum / count,
        ),
      );
    }
    midi = null;
  }

  for (final f in frames) {
    final hz = f.frequency;
    if (hz == null) {
      close();
      continue;
    }
    final r = PitchReading.fromFrequency(hz, a4: a4);
    if (r.midi != midi) {
      close();
      midi = r.midi;
      start = f.time;
      sum = 0;
      count = 0;
    }
    last = f.time;
    sum += r.cents;
    count++;
  }
  close();
  return out;
}

/// 五線（ト音記号）の上の位置：下の線（E4）を 0 とした、線と間の段の数。
/// 臨時記号は ♯・♭（英語式の音名に合わせる）
({int step, String accidental}) staffPosition(int writtenMidi) {
  const letterOf = [0, 0, 1, 2, 2, 3, 3, 4, 5, 5, 6, 6]; // C D E F G A B
  const accidentals = ['', '♯', '', '♭', '', '', '♯', '', '♭', '', '♭', ''];
  // ♭の音は上の文字の段（E♭ は E）、♯の音は下の文字の段（C♯ は C）
  final pc = writtenMidi % 12;
  final octave = writtenMidi ~/ 12 - 1;
  final letter = letterOf[pc];
  // E4 = 文字 2・オクターブ 4
  final step = (octave - 4) * 7 + letter - 2;
  return (step: step, accidental: accidentals[pc]);
}
