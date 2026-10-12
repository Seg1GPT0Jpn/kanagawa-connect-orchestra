import 'dart:math' as math;
import 'dart:typed_data';

import 'package:flutter_test/flutter_test.dart';
import 'package:kco_practice/core/meta_store.dart';
import 'package:kco_practice/features/audio_tools/data/reference_tone_controller.dart';
import 'package:kco_practice/features/audio_tools/data/tuner_controller.dart';
import 'package:kco_practice/features/audio_tools/data/tuner_session_repository.dart';
import 'package:kco_practice/features/audio_tools/domain/note_tracker.dart';
import 'package:kco_practice/features/audio_tools/domain/pitch.dart';
import 'package:kco_practice/features/audio_tools/domain/pitch_stats.dart';
import 'package:kco_practice/features/audio_tools/domain/tuner_settings.dart';

import '../../helpers.dart';

Float64List sine(double hz, double seconds, {double amp = 0.4}) =>
    Float64List.fromList([
      for (var i = 0; i < (44100 * seconds).round(); i++)
        amp * math.sin(2 * math.pi * hz * i / 44100),
    ]);

void main() {
  group('音程の統計', () {
    test('音ごとの平均・ばらつき・合っていた割合・低め／高め、分布', () {
      final s = PitchStats(frameSeconds: 0.05, tolerance: 5);
      for (final c in [0.0, 2.0, -3.0, 10.0]) {
        s.add(70, c);
      }
      for (final c in [-20.0, -18.0]) {
        s.add(72, c);
      }
      final n = s.notes[70]!;
      expect(n.frames, 4);
      expect(n.meanCents, closeTo(2.25, 1e-9));
      expect(n.inTuneRatio, 0.75);
      expect(n.spreadCents, greaterThan(4));
      expect(s.frames, 6);
      expect(s.seconds, closeTo(0.3, 1e-9));
      expect(s.inTuneRatio, closeTo(0.5, 1e-9));
      final b = s.balance;
      expect(b.low, closeTo(2 / 6, 1e-9));
      expect(b.high, closeTo(1 / 6, 1e-9));
      expect(b.inTune + b.low + b.high, closeTo(1, 1e-9));
      expect(s.histogram[histogramIndex(0)], 2); // 0 と +2
      expect(histogramIndex(-80), 0);
      expect(histogramIndex(80), histogramBuckets - 1);
    });

    test('苦手な音：2秒以上吹いて、合っていた割合が低い順', () {
      final s = PitchStats(frameSeconds: 0.1, tolerance: 5);
      for (var i = 0; i < 30; i++) {
        s.add(70, i.isEven ? 0 : 12); // 50%
        s.add(72, 20); // 0%
        s.add(74, 1); // 100%
      }
      for (var i = 0; i < 5; i++) {
        s.add(76, 30); // 0.5秒しか吹いていない
      }
      expect(s.weakNotes().map((n) => n.midi), [72, 70]);
    });

    test('保存の形に変えて戻せる。期間でまとめる・前回と比べる', () {
      final a = PitchStats(frameSeconds: 0.05, tolerance: 5)
        ..add(70, 1)
        ..add(70, 9)
        ..add(72, -2);
      final back = PitchStats.fromMap(a.toMap());
      expect(back.notes[70]!.meanCents, a.notes[70]!.meanCents);
      expect(back.notes[70]!.highFrames, 1);
      expect(back.histogram, a.histogram);

      final b = PitchStats(frameSeconds: 0.05, tolerance: 5)
        ..add(70, 0)
        ..add(70, 0);
      final m = mergeStats([a, b], tolerance: 5);
      expect(m.notes[70]!.frames, 4);
      expect(m.seconds, closeTo(0.25, 1e-9));
      final cmp = compareSessions(a, b);
      expect(cmp.single.midi, 70);
      expect(cmp.single.inTuneChange, closeTo(0.5, 1e-9));
    });
  });

  group('音の区切り', () {
    test('直前の音・音程・出だしの音程。短すぎる音は直前の音にしない', () {
      final t = NoteTracker();
      for (final c in [12.0, 10.0, 3, 1, 0, 0, 0, 0, 0]) {
        t.addFrame(70, c.toDouble());
      }
      expect(t.current!.attackOffset, closeTo(11, 1e-9));
      for (var i = 0; i < 6; i++) {
        t.addFrame(74, -4);
      }
      expect(t.previous!.midi, 70);
      expect(t.intervalSemitones, 4);
      expect(intervalName(4), '長3度上');
      t.silence();
      t.addFrame(60, 0); // 1フレームだけ
      t.silence();
      expect(t.previous!.midi, 74);
      expect(intervalName(-19), '1オクターブと完全5度下');
      expect(intervalName(0), '同じ音');
    });
  });

  test('設定：保存の形・壊れた値・セントの表示', () {
    const s = TunerSettings(
      display: TunerDisplay.bar,
      tolerance: 3,
      decimal: true,
      damping: TunerDamping.slow,
      showAttack: false,
    );
    expect(TunerSettings.fromMap(s.toMap()), s);
    final broken = TunerSettings.fromMap({'display': 'x', 'tolerance': 99});
    expect(broken, const TunerSettings());
    expect(formatCents(3.46), '+3');
    expect(formatCents(3.46, decimal: true), '+3.5');
    expect(formatCents(-0.04, decimal: true), '±0.0');
    expect(formatCents(-12.6), '-13');
  });

  group('チューナーの記録', () {
    late FakeMicInput mic;
    late ReferenceToneController pitch;
    late TunerSessionRepository repo;
    late FakeClock clock;
    late MetaStore meta;
    late TunerController tuner;

    setUp(() async {
      final db = await openMemoryDb();
      meta = MetaStore(db);
      mic = FakeMicInput();
      clock = FakeClock(DateTime(2026, 10, 12, 19));
      pitch = await ReferenceToneController.load(FakeAudioEngine(), meta);
      repo = TunerSessionRepository(db);
      tuner = await TunerController.load(
        mic,
        pitch,
        meta: meta,
        sessions: repo,
        clock: clock.call,
      );
    });

    test('5秒以上吹いて止めると、音名ごとの統計を保存する', () async {
      await tuner.start();
      final up10 = 442 * math.pow(2, 10 / 1200).toDouble();
      tuner.addSamples(sine(442, 3)); // A4 ぴったり
      tuner.addSamples(sine(up10, 3)); // A4 の +10セント
      expect(tuner.stats.inTuneRatio, closeTo(0.5, 0.1));
      expect(tuner.inTune, isFalse);
      clock.advance(const Duration(seconds: 7));
      await tuner.stop();
      final saved = await repo.all();
      expect(saved, hasLength(1));
      final n = saved.single.stats.notes[69]!;
      expect(saved.single.stats.seconds, greaterThan(5));
      expect(n.meanCents, closeTo(5, 1.5));
      expect(saved.single.durationSeconds, 7);
      expect(saved.single.temperamentLabel, '平均律');
      expect(tuner.lastSaved, isNotNull);
    });

    test('短い練習は保存しない。合格の範囲を変えると数え直し、設定は保存する', () async {
      await tuner.start();
      tuner.addSamples(sine(442, 2));
      expect(tuner.stats.frames, greaterThan(0));
      expect(tuner.inTuneStreak, greaterThan(10));
      await tuner.updateSettings(tuner.settings.copyWith(tolerance: 2));
      expect(tuner.stats.frames, 0);
      await tuner.stop();
      expect(await repo.all(), isEmpty);

      final again = await TunerController.load(mic, pitch, meta: meta);
      expect(again.settings.tolerance, 2);
    });

    test('音を続けて変えると、直前の音と音程の差が出る', () async {
      await tuner.start();
      tuner.addSamples(sine(midiToFrequency(70, a4: 442), 0.6));
      tuner.addSamples(sine(midiToFrequency(77, a4: 442), 0.6));
      expect(tuner.previousNote!.midi, 70);
      expect(tuner.currentNote!.midi, 77);
      expect(tuner.intervalSemitones, 7);
    });
  });
}
