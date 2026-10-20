/// 鳴らす音の種類（クリック音の音色・基準音の音色・音量の系統）。決定論的に作る
library;

import 'dart:math' as math;
import 'dart:typed_data';

import 'metronome.dart';
import 'wav.dart';

/// 音量を分けて調整する系統（ミキサー）
enum AudioChannel {
  click('メトロノーム・クリック'),
  tone('基準音'),
  playback('録音の再生');

  const AudioChannel(this.label);
  final String label;
}

/// メトロノームのクリック音の音色
enum ClickSound {
  beep('電子音'),
  wood('ウッドブロック'),
  click('クリック'),
  cowbell('カウベル'),
  hihat('ハイハット');

  const ClickSound(this.label);
  final String label;

  static ClickSound byName(Object? name) =>
      values.firstWhere((s) => s.name == name, orElse: () => ClickSound.beep);
}

/// 基準音の音色（倍音の強さの組み合わせ。1番目が基音）
enum Timbre {
  sine('正弦波（純音）', [1]),
  flute('フルート風', [1, 0.35, 0.12, 0.05]),
  clarinet('クラリネット風', [1, 0.02, 0.6, 0.02, 0.35, 0.02, 0.15, 0, 0.08]),
  brass('金管風', [1, 0.85, 0.7, 0.55, 0.42, 0.3, 0.2, 0.13, 0.08, 0.05]),
  strings('弦楽器風', [1, 0.5, 0.33, 0.25, 0.2, 0.16, 0.14, 0.12, 0.1, 0.08]),
  organ('オルガン風', [1, 0.7, 0.25, 0.45, 0, 0.2, 0, 0.25]);

  const Timbre(this.label, this.harmonics);
  final String label;

  /// 倍音の強さ（[0] が基音）
  final List<double> harmonics;

  /// 合わせた波の山が 1 を超えない倍率
  double get gain => 1 / harmonics.fold<double>(0, (a, b) => a + b);

  static Timbre byName(Object? name) =>
      values.firstWhere((t) => t.name == name, orElse: () => Timbre.sine);
}

/// [sound] の音色で、[kind]（強拍・拍・細分）のクリック音を作る
Uint8List clickSoundWav(ClickSound sound, ClickKind kind) {
  final accent = kind == ClickKind.accent;
  final sub = kind == ClickKind.subdivision;
  // 強拍は高く大きく、細分は低く小さく
  final pitch = accent ? 1.33 : (sub ? 0.75 : 1.0);
  final volume = accent ? 0.95 : (sub ? 0.45 : 0.75);
  return switch (sound) {
    ClickSound.beep => clickWav(
      frequency: 1320 * pitch,
      volume: volume,
      duration: Duration(milliseconds: sub ? 25 : 40),
    ),
    ClickSound.wood => _synth(
      const Duration(milliseconds: 60),
      volume,
      (t) =>
          math.exp(-t / 0.012) *
          (math.sin(2 * math.pi * 900 * pitch * t) +
              0.35 * math.sin(2 * math.pi * 2430 * pitch * t)) /
          1.35,
    ),
    ClickSound.click => _noise(
      Duration(milliseconds: accent ? 12 : 8),
      volume,
      decay: 0.002,
      highPass: true,
    ),
    ClickSound.cowbell => _synth(
      const Duration(milliseconds: 160),
      volume * 0.9,
      (t) =>
          math.exp(-t / 0.05) *
          (_square(562 * pitch * t) + _square(845 * pitch * t)) /
          2,
    ),
    ClickSound.hihat => _noise(
      Duration(milliseconds: accent ? 90 : 50),
      volume * 0.8,
      decay: accent ? 0.03 : 0.015,
      highPass: true,
    ),
  };
}

/// 角の丸い矩形波（奇数倍音を3つ）。[phase] は周期の数
double _square(double phase) {
  final x = 2 * math.pi * phase;
  return (math.sin(x) + math.sin(3 * x) / 3 + math.sin(5 * x) / 5) * 0.9;
}

const _sampleRate = 44100;

Uint8List _synth(Duration d, double volume, double Function(double t) wave) {
  final n = (_sampleRate * d.inMicroseconds / 1000000).round();
  final s = Int16List(n);
  final attack = _sampleRate ~/ 2000; // 0.5ms で立ち上げる
  for (var i = 0; i < n; i++) {
    final env = i < attack ? i / attack : 1.0;
    // 最後の 5ms で 0 に戻す（プツッという音を防ぐ）
    final tail = math.min(1.0, (n - i) / (_sampleRate * 0.005));
    s[i] = (wave(i / _sampleRate) * env * tail * volume * 32767).round().clamp(
      -32768,
      32767,
    );
  }
  return pcm16Wav(s, sampleRate: _sampleRate);
}

/// 減衰する雑音（毎回同じ音になるよう、乱数の種は固定）
Uint8List _noise(
  Duration d,
  double volume, {
  required double decay,
  bool highPass = false,
}) {
  final rnd = math.Random(7);
  var prev = 0.0;
  return _synth(d, volume, (t) {
    final x = rnd.nextDouble() * 2 - 1;
    final y = highPass ? (x - prev) / 2 : x;
    prev = x;
    return y * math.exp(-t / decay);
  });
}
