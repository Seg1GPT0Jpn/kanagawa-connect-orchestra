import 'package:flutter/foundation.dart';

import '../domain/metronome.dart';
import '../domain/sound.dart';
import 'audio_engine_factory_native.dart'
    if (dart.library.js_interop) 'audio_engine_factory_web.dart'
    as platform;

/// 音を鳴らす窓口（テストでは偽物に差し替える）
abstract interface class AudioEngine {
  /// 端末に合った鳴らし方（Web は Web Audio、スマホなどは SoLoud）
  factory AudioEngine.platform() => platform.createAudioEngine();

  /// 音を出せる状態にする。
  ///
  /// Web（特に iPhone の Safari）では、ボタンを押した処理の中で
  /// **最初の await より前に** 呼ぶ必要がある（ブラウザが音を許可する条件）。
  Future<void> ensureStarted();

  bool get isStarted;

  /// 音の時計（予約に使う）。始まっていなければ 0
  Duration get now;

  /// [kind] のクリック音を、音の時計の [at] に鳴らすよう予約する
  void scheduleClick(
    ClickKind kind,
    Duration at, {
    ClickSound sound = ClickSound.beep,
    double volume = 1,
  });

  /// まだ鳴っていない予約をすべて取り消す
  void cancelScheduledClicks();

  /// [hz] の音を [voice] 番で鳴らし続ける（鳴っていれば高さ・音色・音量だけ変える）。
  /// 番号を変えると、和音のように複数の音を同時に鳴らせる
  Future<void> startTone(
    double hz, {
    double volume = 0.5,
    Timbre timbre = Timbre.sine,
    int voice = 0,
  });

  /// [voice] 番の音を止める。null ならすべて
  void stopTone({int? voice});

  /// WAV（録音の再生など）を鳴らす。[speed] は再生の速さ（音の高さも変わる）。
  /// [onDone] は最後まで鳴ったとき
  Future<void> playWav(
    Uint8List wav, {
    double speed = 1,
    void Function()? onDone,
  });
  void stopPlayback();

  /// 系統ごとの音量（0〜1）
  double volumeOf(AudioChannel channel);
  void setVolume(AudioChannel channel, double volume);
}

class AudioEngineException implements Exception {
  const AudioEngineException(this.message);

  final String message;

  @override
  String toString() => message;
}

/// 音が出せなかったときの案内
const audioTroubleMessage =
    '音を出せませんでした。画面をもう一度タップするか、端末の音量・マナーモード'
    '（iPhone の消音スイッチ）・接続中のイヤホンを確かめてください';

/// 系統ごとの音量を覚えておく（エンジンの共通部分）
mixin ChannelVolumes {
  final Map<AudioChannel, double> _volumes = {
    for (final c in AudioChannel.values) c: 1.0,
  };

  double volumeOf(AudioChannel channel) => _volumes[channel]!;

  void storeVolume(AudioChannel channel, double volume) =>
      _volumes[channel] = volume.clamp(0.0, 1.0);
}

/// 16bit モノラル WAV の標本化周波数とサンプル（-1〜1）
({int sampleRate, Float32List samples}) decodePcm16Wav(Uint8List wav) {
  final b = ByteData.sublistView(wav);
  final sampleRate = b.getUint32(24, Endian.little);
  final n = (wav.length - 44) ~/ 2;
  final out = Float32List(n);
  for (var i = 0; i < n; i++) {
    out[i] = b.getInt16(44 + i * 2, Endian.little) / 32768;
  }
  return (sampleRate: sampleRate, samples: out);
}
