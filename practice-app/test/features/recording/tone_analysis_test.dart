import 'dart:math' as math;
import 'dart:typed_data';

import 'package:flutter_test/flutter_test.dart';
import 'package:kco_practice/features/audio_tools/domain/pitch.dart';
import 'package:kco_practice/features/recording/domain/tone_analysis.dart';

const sr = 22050.0;

/// 合成した音：[freq] は時刻→周波数、[amp] は時刻→振幅
Float64List synth(
  double seconds,
  double Function(double t) freq, {
  double Function(double t)? amp,
}) {
  final n = (seconds * sr).round();
  final out = Float64List(n);
  var phase = 0.0;
  for (var i = 0; i < n; i++) {
    final t = i / sr;
    phase += 2 * math.pi * freq(t) / sr;
    final a = amp?.call(t) ?? 0.4;
    // 倍音を少し足す（トランペットらしく）
    out[i] =
        a *
        (0.6 * math.sin(phase) +
            0.3 * math.sin(2 * phase) +
            0.1 * math.sin(3 * phase));
  }
  return out;
}

void main() {
  final a4 = 442.0;
  final bflat = midiToFrequency(70, a4: a4);

  test('安定したロングトーン：音名・ずれ・ゆれ・変化がほぼ0', () {
    final a = analyzeTone(synth(3, (_) => bflat), sampleRate: sr, a4: a4)!;
    expect(noteLabel(a.midi), 'B♭4');
    expect(a.centsOffset.abs(), lessThan(1));
    expect(a.pitchSpreadCents, lessThan(1));
    expect(a.driftCents.abs(), lessThan(1));
    expect(a.volumeSpreadDb, lessThan(0.5));
    expect(a.voicedSeconds, closeTo(3, 0.15));
    expect(a.pitchGrade, Grade.good);
    expect(a.volumeGrade, Grade.good);
  });

  test('ビブラート（±20セント・5Hz）：ゆれは約14セント（正弦波の標準偏差）', () {
    final a = analyzeTone(
      synth(
        3,
        (t) => bflat * math.pow(2, 20 * math.sin(2 * math.pi * 5 * t) / 1200),
      ),
      sampleRate: sr,
      a4: a4,
    )!;
    expect(a.pitchSpreadCents, closeTo(14.1, 3));
    expect(a.pitchGrade, Grade.needsWork);
    expect(a.driftCents.abs(), lessThan(5));
  });

  test('だんだん上ずる音（+30セント）：変化はプラス', () {
    final a = analyzeTone(
      synth(3, (t) => bflat * math.pow(2, (30 * t / 3) / 1200)),
      sampleRate: sr,
      a4: a4,
    )!;
    expect(a.driftCents, closeTo(20, 4)); // 始めの1/3と終わりの1/3の中央値の差
    expect(a.driftGrade, Grade.needsWork);
    expect(describeAnalysis(a)[1], contains('上ずっています'));
  });

  test('クレッシェンド（音量が10倍＝20dB）：音量のゆれが大きい', () {
    final a = analyzeTone(
      synth(3, (_) => bflat, amp: (t) => 0.04 + 0.36 * t / 3),
      sampleRate: sr,
      a4: a4,
    )!;
    expect(a.volumeSpreadDb, greaterThan(3));
    expect(a.volumeGrade, Grade.needsWork);
    expect(a.pitchSpreadCents, lessThan(1)); // 音程は安定
  });

  test('ゆっくりした立ち上がり（0.5秒かけて大きくなる）', () {
    final a = analyzeTone(
      synth(2.5, (_) => bflat, amp: (t) => 0.4 * math.min(1, t / 0.5) + 0.01),
      sampleRate: sr,
      a4: a4,
    )!;
    expect(a.attackSeconds, greaterThan(0.3));
    expect(a.attackGrade, isNot(Grade.good));
  });

  test('前後に無音があっても、鳴っている部分だけを分析する', () {
    final tone = synth(2, (_) => bflat);
    final padded = Float64List(tone.length + (sr * 2).round())
      ..setRange((sr).round(), (sr).round() + tone.length, tone);
    final a = analyzeTone(padded, sampleRate: sr, a4: a4)!;
    expect(a.duration, closeTo(4, 0.01));
    expect(a.voicedSeconds, closeTo(2, 0.15));
    expect(a.pitchSpreadCents, lessThan(1));
  });

  test('無音・短すぎる音は分析しない', () {
    expect(analyzeTone(Float64List((sr * 2).round()), sampleRate: sr), isNull);
    expect(analyzeTone(synth(0.2, (_) => bflat), sampleRate: sr), isNull);
  });

  test('describeAnalysis：4つの観点をことばで返す', () {
    final a = analyzeTone(synth(3, (_) => bflat), sampleRate: sr, a4: a4)!;
    final lines = describeAnalysis(a);
    expect(lines, hasLength(4));
    expect(lines[0], contains('よく安定'));
  });

  group('信頼度の目安', () {
    // 前後に静かな区間（周りの音だけ）を付けた録音
    Float64List withSilence(Float64List tone, {double noise = 0.0005}) {
      final rnd = math.Random(1);
      final pad = (0.5 * sr).round();
      final out = Float64List(tone.length + pad * 2);
      for (var i = 0; i < out.length; i++) {
        final t = i - pad;
        out[i] =
            (t >= 0 && t < tone.length ? tone[t] : 0) +
            noise * (rnd.nextDouble() * 2 - 1);
      }
      return out;
    }

    test('静かな場所でのきれいなロングトーンは「高い」', () {
      final a = analyzeTone(
        withSilence(synth(3, (_) => bflat)),
        sampleRate: sr,
        a4: a4,
      )!;
      expect(a.reliability, Reliability.high);
      expect(a.reliabilityNotes, isEmpty);
      expect(a.gaps, isEmpty);
      expect(a.levelDb, closeTo(-12, 3));
    });

    test('音が小さすぎる・割れている・短いと、理由つきで下がる', () {
      final quiet = analyzeTone(
        synth(3, (_) => bflat, amp: (_) => 0.05),
        sampleRate: sr,
        a4: a4,
      )!;
      expect(quiet.reliability, isNot(Reliability.high));
      expect(quiet.reliabilityNotes.join(), contains('小さ'));

      final loud = synth(3, (_) => bflat, amp: (_) => 2);
      for (var i = 0; i < loud.length; i++) {
        loud[i] = loud[i].clamp(-1.0, 1.0);
      }
      final clipped = analyzeTone(loud, sampleRate: sr, a4: a4)!;
      expect(clipped.reliability, Reliability.low);
      expect(clipped.reliabilityNotes.join(), contains('割れ'));

      final short = analyzeTone(
        synth(1, (_) => bflat),
        sampleRate: sr,
        a4: a4,
      )!;
      expect(short.reliabilityNotes.join(), contains('短め'));
    });

    test('途中で途切れた区間は「測れなかった区間」になり、多ければ信頼度が下がる', () {
      final tone = synth(4, (_) => bflat);
      // 1.0〜2.2秒を無音にする
      for (var i = (1.0 * sr).round(); i < (2.2 * sr).round(); i++) {
        tone[i] = 0;
      }
      final a = analyzeTone(tone, sampleRate: sr, a4: a4)!;
      expect(a.gaps, hasLength(1));
      expect(a.gaps.single.start, closeTo(1.0, 0.1));
      expect(a.gaps.single.end, closeTo(2.2, 0.1));
      expect(a.reliability, isNot(Reliability.high));
      expect(a.reliabilityNotes.join(), contains('測れません'));
    });

    test('周りの音が大きいと下がる', () {
      final a = analyzeTone(
        withSilence(synth(3, (_) => bflat, amp: (_) => 0.05), noise: 0.03),
        sampleRate: sr,
        a4: a4,
      );
      expect(a, isNotNull);
      expect(a!.reliability, isNot(Reliability.high));
      expect(a.reliabilityNotes.join(), contains('周りの音'));
    });
  });
}
