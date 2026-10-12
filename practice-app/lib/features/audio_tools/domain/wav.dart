/// 短い音（クリック音など）を WAV（16bit・モノラル）として作る（決定論的）
library;

import 'dart:math' as math;
import 'dart:typed_data';

/// [frequency] Hz の正弦波を [duration] 鳴らし、指数的に減衰させたクリック音
Uint8List clickWav({
  required double frequency,
  Duration duration = const Duration(milliseconds: 40),
  double volume = 0.9,
  int sampleRate = 44100,
}) {
  final n = (sampleRate * duration.inMicroseconds / 1000000).round();
  final samples = Int16List(n);
  // 最初の1msで立ち上げ、残りで減衰（プツッという雑音を防ぐ）
  final attack = (sampleRate / 1000).round();
  for (var i = 0; i < n; i++) {
    final t = i / sampleRate;
    final env = i < attack
        ? i / attack
        : math.exp(-6.0 * (i - attack) / (n - attack));
    samples[i] = (math.sin(2 * math.pi * frequency * t) * env * volume * 32767)
        .round()
        .clamp(-32768, 32767);
  }
  return pcm16Wav(samples, sampleRate: sampleRate);
}

/// 16bit モノラルの PCM を WAV ファイルの形にする
Uint8List pcm16Wav(Int16List samples, {required int sampleRate}) {
  final dataBytes = samples.length * 2;
  final b = ByteData(44 + dataBytes);
  void ascii(int offset, String s) {
    for (var i = 0; i < s.length; i++) {
      b.setUint8(offset + i, s.codeUnitAt(i));
    }
  }

  ascii(0, 'RIFF');
  b.setUint32(4, 36 + dataBytes, Endian.little);
  ascii(8, 'WAVE');
  ascii(12, 'fmt ');
  b.setUint32(16, 16, Endian.little); // fmt チャンクの大きさ
  b.setUint16(20, 1, Endian.little); // PCM
  b.setUint16(22, 1, Endian.little); // モノラル
  b.setUint32(24, sampleRate, Endian.little);
  b.setUint32(28, sampleRate * 2, Endian.little); // 1秒あたりのバイト数
  b.setUint16(32, 2, Endian.little); // 1サンプルのバイト数
  b.setUint16(34, 16, Endian.little); // ビット数
  ascii(36, 'data');
  b.setUint32(40, dataBytes, Endian.little);
  for (var i = 0; i < samples.length; i++) {
    b.setInt16(44 + i * 2, samples[i], Endian.little);
  }
  return b.buffer.asUint8List();
}
