import 'dart:async';
import 'dart:typed_data';

import 'package:record/record.dart';

/// マイクの入力（テストでは偽物に差し替える）
abstract interface class MicInput {
  /// 許可を求める（すでに許可されていれば true）
  Future<bool> requestPermission();

  /// -1〜1 の波形（モノラル、[sampleRate]）を流す
  Future<Stream<Float64List>> start({required int sampleRate});
  Future<void> stop();
}

class RecordMicInput implements MicInput {
  AudioRecorder? _recorder;

  @override
  Future<bool> requestPermission() =>
      (_recorder ??= AudioRecorder()).hasPermission();

  @override
  Future<Stream<Float64List>> start({required int sampleRate}) async {
    final r = _recorder ??= AudioRecorder();
    final stream = await r.startStream(
      RecordConfig(
        encoder: AudioEncoder.pcm16bits,
        sampleRate: sampleRate,
        numChannels: 1,
        // 音程を測るので、声の通話向けの加工はすべて切る
        autoGain: false,
        echoCancel: false,
        noiseSuppress: false,
      ),
    );
    return stream.map(pcm16ToFloat);
  }

  @override
  Future<void> stop() async {
    final r = _recorder;
    _recorder = null;
    if (r == null) return;
    await r.stop();
    await r.dispose();
  }
}

/// 16bit リトルエンディアンの PCM → -1〜1
Float64List pcm16ToFloat(Uint8List bytes) {
  final data = ByteData.sublistView(bytes);
  final out = Float64List(bytes.length ~/ 2);
  for (var i = 0; i < out.length; i++) {
    out[i] = data.getInt16(i * 2, Endian.little) / 32768;
  }
  return out;
}
