import 'dart:math' as math;
import 'dart:typed_data';

import 'package:flutter_test/flutter_test.dart';
import 'package:kco_practice/core/meta_store.dart';
import 'package:kco_practice/features/audio_tools/data/reference_tone_controller.dart';
import 'package:kco_practice/features/audio_tools/data/tuner_controller.dart';
import 'package:kco_practice/features/audio_tools/domain/spectrum.dart';

import '../../helpers.dart';

const sr = 22050.0;

/// 倍音を [amps] の強さで重ねた音（[n] サンプル）
Float64List tone(
  double f0,
  List<double> amps, {
  int n = 2048,
  double rate = sr,
}) => Float64List.fromList([
  for (var i = 0; i < n; i++)
    [
      for (var k = 0; k < amps.length; k++)
        amps[k] * math.sin(2 * math.pi * f0 * (k + 1) * i / rate),
    ].fold<double>(0, (a, b) => a + b),
]);

void main() {
  test('FFT：インパルスは平ら、定数は 0 Hz だけ', () {
    final re = Float64List(8)..[0] = 1;
    final im = Float64List(8);
    fft(re, im);
    for (var i = 0; i < 8; i++) {
      expect(re[i], closeTo(1, 1e-12));
      expect(im[i], closeTo(0, 1e-12));
    }
    final re2 = Float64List.fromList(List.filled(8, 1));
    final im2 = Float64List(8);
    fft(re2, im2);
    expect(re2[0], closeTo(8, 1e-12));
    for (var i = 1; i < 8; i++) {
      expect(re2[i].abs() + im2[i].abs(), closeTo(0, 1e-12));
    }
  });

  test('正弦波の振幅と周波数がそのまま読める（山は ±1.5 dB 以内）', () {
    for (final hz in [233.08, 440.0, 1046.5]) {
      final s = Spectrum.of(tone(hz, [0.5]), sampleRate: sr);
      expect(s.size, 2048);
      expect(s.binHz, closeTo(10.77, 0.01));
      expect(Spectrum.toDb(s.peakNear(hz)), closeTo(Spectrum.toDb(0.5), 1.5));
      // 離れた周波数はずっと小さい
      expect(Spectrum.toDb(s.peakNear(hz * 2.5)), lessThan(-50));
    }
  });

  test('長さが2のべき乗でなければ、後ろの2のべき乗の長さで分析する', () {
    final s = Spectrum.of(tone(440, [0.5], n: 3000), sampleRate: sr);
    expect(s.size, 2048);
  });

  test('倍音のバランス：基音 0 dB に対する各倍音の強さと、明るさ', () {
    final s = Spectrum.of(tone(466.16, [0.6, 0.3, 0.1]), sampleRate: sr);
    final h = HarmonicProfile.of(s, 466.16);
    expect(h.levelsDb, hasLength(8));
    expect(h.levelsDb[0], 0);
    expect(h.levelsDb[1], closeTo(-6.0, 1.5));
    expect(h.levelsDb[2], closeTo(-15.6, 1.5));
    expect(h.levelsDb[5], lessThan(-40));
    // エネルギーの重み：(1·0.36 + 2·0.09 + 3·0.01) / 0.46 ≒ 1.24
    expect(h.brightness, closeTo(1.24, 0.1));
    expect(h.description, contains('柔らか'));

    final bright = HarmonicProfile.of(
      Spectrum.of(
        tone(233.08, [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]),
        sampleRate: sr,
      ),
      233.08,
    );
    expect(bright.brightness, closeTo(4, 0.3));
    expect(bright.description, contains('明る'));
  });

  test('音の重心は、高い倍音が多いほど高い', () {
    final soft = Spectrum.of(tone(440, [0.6, 0.1]), sampleRate: sr);
    final bright = Spectrum.of(tone(440, [0.3, 0.3, 0.3, 0.3]), sampleRate: sr);
    expect(bright.centroid(), greaterThan(soft.centroid()));
  });

  test('平均：同じスペクトラムの平均はそれ自身', () {
    final s = Spectrum.of(tone(440, [0.5]), sampleRate: sr);
    final avg = SpectrumAverager()
      ..add(s)
      ..add(s);
    expect(avg.count, 2);
    expect(avg.average!.peakNear(440), closeTo(s.peakNear(440), 1e-9));
    expect(SpectrumAverager().average, isNull);
  });

  test('チューナー：音を入れるとスペクトラム・倍音のバランス・最大値が出る。止めて見られる', () async {
    final tuner = TunerController(
      FakeMicInput(),
      await ReferenceToneController.load(
        FakeAudioEngine(),
        MetaStore(await openMemoryDb()),
      ),
    );
    expect(tuner.spectrum, isNull);
    tuner.addSamples(tone(466.16, [0.4, 0.2], n: 44100 ~/ 2, rate: 44100));
    expect(tuner.spectrum, isNotNull);
    expect(tuner.harmonics!.levelsDb[1], closeTo(-6, 2));
    expect(tuner.peakHold, isNotNull);

    tuner.setSpectrumFrozen(true);
    final frozen = tuner.spectrum;
    tuner.addSamples(tone(300, [0.4], n: 44100 ~/ 2, rate: 44100));
    expect(identical(tuner.spectrum, frozen), isTrue);
    tuner.resetPeakHold();
    expect(tuner.peakHold, isNull);
  });
}
