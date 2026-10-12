import 'dart:math' as math;
import 'dart:typed_data';

import 'package:flutter_test/flutter_test.dart';
import 'package:kco_practice/core/meta_store.dart';
import 'package:kco_practice/features/audio_tools/data/reference_tone_controller.dart';
import 'package:kco_practice/features/audio_tools/domain/pitch.dart';
import 'package:kco_practice/features/audio_tools/domain/wav.dart';
import 'package:kco_practice/features/recording/data/recording_controller.dart';
import 'package:kco_practice/features/recording/data/recording_repository.dart';
import 'package:kco_practice/features/recording/domain/audio_file.dart';
import 'package:kco_practice/features/recording/domain/tone_analysis.dart';

import '../../helpers.dart';

/// 任意の形式の WAV を作る（テスト用）
Uint8List makeWav(
  List<double> mono, {
  int rate = 48000,
  int channels = 1,
  int bits = 16,
  bool float = false,
}) {
  final bytesPer = bits ~/ 8;
  final data = ByteData(mono.length * channels * bytesPer);
  var at = 0;
  for (final v in mono) {
    for (var c = 0; c < channels; c++) {
      if (float) {
        data.setFloat32(at, v, Endian.little);
      } else if (bits == 24) {
        final x = (v * 8388607).round();
        data
          ..setUint8(at, x & 0xff)
          ..setUint8(at + 1, (x >> 8) & 0xff)
          ..setInt8(at + 2, x >> 16);
      } else {
        data.setInt16(at, (v * 32767).round(), Endian.little);
      }
      at += bytesPer;
    }
  }
  final b = BytesBuilder();
  void str(String s) => b.add(s.codeUnits);
  void u32(int v) =>
      b.add((ByteData(4)..setUint32(0, v, Endian.little)).buffer.asUint8List());
  void u16(int v) =>
      b.add((ByteData(2)..setUint16(0, v, Endian.little)).buffer.asUint8List());
  str('RIFF');
  u32(36 + data.lengthInBytes + 12);
  str('WAVE');
  // 関係ないチャンクを飛ばせること
  str('LIST');
  u32(4);
  str('INFO');
  str('fmt ');
  u32(16);
  u16(float ? 3 : 1);
  u16(channels);
  u32(rate);
  u32(rate * channels * bytesPer);
  u16(channels * bytesPer);
  u16(bits);
  str('data');
  u32(data.lengthInBytes);
  b.add(data.buffer.asUint8List());
  return b.toBytes();
}

List<double> sine(double hz, double seconds, int rate, {double amp = 0.5}) => [
  for (var i = 0; i < (seconds * rate).round(); i++)
    amp *
        (0.7 * math.sin(2 * math.pi * hz * i / rate) +
            0.3 * math.sin(4 * math.pi * hz * i / rate)),
];

void main() {
  group('WAV の読み込み', () {
    test('16bit・24bit・浮動小数・ステレオを同じ波形として読む', () {
      final x = sine(440, 0.01, 48000);
      for (final w in [
        makeWav(x),
        makeWav(x, bits: 24),
        makeWav(x, float: true, bits: 32),
        makeWav(x, channels: 2),
      ]) {
        final r = readWav(w);
        expect(r.sampleRate, 48000);
        expect(r.samples.length, x.length);
        for (var i = 0; i < x.length; i += 37) {
          expect(r.samples[i], closeTo(x[i], 1e-3));
        }
      }
    });

    test('WAV でない・対応していない形式はエラー', () {
      expect(
        () => readWav(Uint8List.fromList(List.filled(60, 0))),
        throwsA(isA<WavFormatException>()),
      );
      expect(
        () => readWav(makeWav(sine(440, 0.01, 8000), rate: 2000)),
        throwsA(isA<WavFormatException>()),
      );
    });

    test('周波数の変換：48kHz → 22.05kHz でも音の高さは変わらない', () {
      final x = Float64List.fromList(sine(466.16, 1, 48000));
      final y = resample(x, 48000, 22050);
      expect(y.length, closeTo(22050, 30));
      final a = analyzeTone(y, sampleRate: 22050, a4: 442)!;
      expect(noteLabel(a.midi), 'B♭4');
    });
  });

  test('波形の外形と、音の並び・五線上の位置', () {
    final pcm = Int16List.fromList([0, 32767, -32768, 0, 100, -100]);
    final env = waveformEnvelope(pcm, 3);
    expect(env.first, (0.0, 1.0));
    expect(env[1].$1, -1);
    // 音の並び：C5 0.5秒 → D5 0.5秒
    final frames = [
      for (var i = 0; i < 20; i++)
        ToneFrame(
          time: i * 0.025,
          rms: 0.1,
          frequency: midiToFrequency(72, a4: 442),
        ),
      for (var i = 20; i < 40; i++)
        ToneFrame(
          time: i * 0.025,
          rms: 0.1,
          frequency: midiToFrequency(74, a4: 442),
        ),
    ];
    final notes = segmentNotes(frames, a4: 442);
    expect(notes.map((n) => n.midi), [72, 74]);
    expect(notes.first.meanCents.abs(), lessThan(0.01));
    // 五線：E4 が下の線（0）、F5 が上の線（8）、C4 は下の加線（-2）
    expect(staffPosition(64).step, 0);
    expect(staffPosition(77).step, 8);
    expect(staffPosition(60).step, -2);
    expect(staffPosition(70), (step: 4, accidental: '♭')); // B♭4
    expect(staffPosition(66), (step: 1, accidental: '♯')); // F♯4
  });

  group('録音の読み込み・範囲・書き出し', () {
    late RecordingController c;
    late FakeFileGateway files;
    late FakeAudioEngine audio;

    setUp(() async {
      final db = await openMemoryDb();
      audio = FakeAudioEngine();
      files = FakeFileGateway();
      c = RecordingController(
        mic: FakeMicInput(),
        audio: audio,
        pitch: await ReferenceToneController.load(audio, MetaStore(db)),
        repository: RecordingRepository(db),
        files: files,
        clock: FakeClock(DateTime(2026, 10, 12, 19, 5)).call,
      );
    });

    test('WAV を読み込んで分析し、範囲を選び直せて、その範囲だけ書き出せる', () async {
      // 前半 B♭4・後半 F5
      final x = [
        ...sine(midiToFrequency(70, a4: 442), 2, 44100),
        ...sine(midiToFrequency(77, a4: 442), 2, 44100),
      ];
      files.toPick = makeWav(x, rate: 44100);
      expect(await c.importFile(), isTrue);
      expect(c.phase, RecordingPhase.done);
      expect(c.source, isNotNull);
      expect(c.seconds, closeTo(4, 0.01));
      expect(c.result, isNotNull);

      await c.analyzeRange((2.2, 3.8));
      expect(noteLabel(c.result!.midi), 'F5');
      expect(c.range, (2.2, 3.8));
      final wavLen = c.wav.length - 44;
      expect(wavLen / 2 / 22050, closeTo(1.6, 0.01));

      expect(await c.exportWav(), isTrue);
      final (bytes, mime) = files.saved['recording-2026-10-12-1905.wav']!;
      expect(mime, 'audio/wav');
      expect(readWav(bytes).sampleRate, 22050);

      await c.analyzeRange(null);
      expect(c.range, isNull);
    });

    test('読めないファイルはエラー。再生の速さはそのまま渡す', () async {
      files.toPick = Uint8List.fromList(List.filled(100, 1));
      expect(await c.importFile(), isFalse);
      expect(c.error, contains('WAV'));

      files.toPick = makeWav(sine(440, 1, 22050), rate: 22050);
      await c.importFile();
      c.setSpeed(0.5);
      await c.play();
      expect(audio.playbackSpeed, 0.5);
      expect(audio.playedWav, isNotNull);
    });

    test('録る長さを選べる（録音中は変えない）', () {
      c.setLimit(const Duration(minutes: 3));
      expect(c.limit, const Duration(minutes: 3));
      expect(pcm16Wav(Int16List(0), sampleRate: 22050).length, 44);
    });
  });
}
