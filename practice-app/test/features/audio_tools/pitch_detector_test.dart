import 'dart:math' as math;
import 'dart:typed_data';

import 'package:flutter_test/flutter_test.dart';
import 'package:kco_practice/features/audio_tools/domain/pitch.dart';
import 'package:kco_practice/features/audio_tools/domain/pitch_detector.dart';

const sr = 22050.0;
const n = 2048;

/// 基本周波数 [f] に倍音を重ねた音（トランペットのように倍音が強い音も作れる）
Float64List tone(
  double f, {
  List<double> harmonics = const [1],
  double amp = 0.5,
  double noise = 0,
  int seed = 1,
}) {
  final rnd = math.Random(seed);
  final total = harmonics.fold(0.0, (s, h) => s + h);
  return Float64List.fromList([
    for (var i = 0; i < n; i++)
      amp *
              [
                for (var k = 0; k < harmonics.length; k++)
                  harmonics[k] *
                      math.sin(2 * math.pi * f * (k + 1) * i / sr + k),
              ].fold(0.0, (s, v) => s + v) /
              total +
          noise * (rnd.nextDouble() * 2 - 1),
  ]);
}

void main() {
  const detector = PitchDetector(sampleRate: sr);

  test('正弦波：トランペットの音域で ±1 セント以内', () {
    for (var midi = 52; midi <= 84; midi++) {
      // 実音 E3〜C6
      final f = midiToFrequency(midi, a4: 442);
      final e = detector.detect(tone(f))!;
      expect(
        centsBetween(e.frequency, f).abs(),
        lessThan(1),
        reason: noteLabel(midi),
      );
      expect(e.clarity, greaterThan(0.9));
    }
  });

  test('倍音の強い音（基音より第2・第3倍音が大きい）でも、オクターブを間違えない', () {
    const brassy = [0.6, 1.0, 0.9, 0.7, 0.5, 0.35, 0.2];
    for (final midi in [58, 65, 70, 77, 82]) {
      final f = midiToFrequency(midi, a4: 442);
      final e = detector.detect(tone(f, harmonics: brassy))!;
      expect(
        centsBetween(e.frequency, f).abs(),
        lessThan(3),
        reason: noteLabel(midi),
      );
    }
  });

  test('少しの雑音があっても検出し、わずかなずれ（+12セント）も分かる', () {
    final f = midiToFrequency(69, a4: 442) * math.pow(2, 12 / 1200);
    final e = detector.detect(tone(f, noise: 0.05))!;
    final r = PitchReading.fromFrequency(e.frequency, a4: 442);
    expect(r.midi, 69);
    expect(r.cents, closeTo(12, 2));
  });

  test('無音・雑音だけのときは null', () {
    expect(detector.detect(Float64List(n)), isNull);
    expect(detector.detect(tone(440, amp: 0.001)), isNull);
    final noise = Float64List.fromList([
      for (var i = 0; i < n; i++) math.Random(i).nextDouble() * 2 - 1,
    ]);
    expect(detector.detect(noise), isNull);
  });

  test('MedianSmoother：とびはねた値を抑える', () {
    final m = MedianSmoother(3);
    expect(m.add(440), 440);
    expect(m.add(441), 441);
    expect(m.add(880), 441); // 1回だけのオクターブ違いは表示しない
    expect(m.add(442), 442);
  });
}
