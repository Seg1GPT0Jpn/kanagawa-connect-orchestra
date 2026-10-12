import 'package:flutter_test/flutter_test.dart';
import 'package:kco_practice/core/meta_store.dart';
import 'package:kco_practice/features/audio_tools/data/metronome_controller.dart';
import 'package:kco_practice/features/audio_tools/data/metronome_presets.dart';
import 'package:kco_practice/features/audio_tools/domain/metronome.dart';
import 'package:kco_practice/features/audio_tools/domain/metronome_plan.dart';
import 'package:kco_practice/features/audio_tools/domain/sound.dart';

import '../../helpers.dart';

List<PlannedClick> bars(MetronomeSequencer s, int n) => [
  for (var i = 0; i < n; i++) ...s.nextBar(),
];

void main() {
  const s120 = MetronomeSettings(bpm: 120, beatsPerBar: 4);

  group('クリックの作り方', () {
    test('ふつう：今までと同じ時刻（0.5秒ごと・1拍目が強拍）', () {
      final c = bars(MetronomeSequencer(s120, const MetronomeOptions()), 2);
      expect(c.map((e) => e.offsetMicros), [
        for (var i = 0; i < 8; i++) i * 500000,
      ]);
      expect(c.first.kind, ClickKind.accent);
      expect(c[1].kind, ClickKind.beat);
      expect(c.every((e) => !e.muted), isTrue);
      // 3連でも誤差がたまらない（閉じた式と同じ）
      const triplet = MetronomeSettings(
        bpm: 70,
        beatsPerBar: 3,
        subdivision: 3,
      );
      final t = bars(MetronomeSequencer(triplet, const MetronomeOptions()), 20);
      for (final (i, e) in t.indexed) {
        expect(e.offsetMicros, triplet.clickOffsetMicros(i));
      }
    });

    test('拍ごとのパターン：休みの拍は鳴らさない（拍の表示は進む）', () {
      final o = const MetronomeOptions(
        pattern: [
          BeatAccent.accent,
          BeatAccent.mute,
          BeatAccent.accent,
          BeatAccent.normal,
        ],
      );
      final c = MetronomeSequencer(s120, o).nextBar();
      expect(c.map((e) => e.kind), [
        ClickKind.accent,
        ClickKind.beat,
        ClickKind.accent,
        ClickKind.beat,
      ]);
      expect(c.map((e) => e.muted), [false, true, false, false]);
      // 拍の数と合わないパターンは使わない
      expect(o.patternFor(3, accentFirst: true), [
        BeatAccent.accent,
        BeatAccent.normal,
        BeatAccent.normal,
      ]);
    });

    test('小節ごとに 2 鳴らして 1 休む', () {
      final c = bars(
        MetronomeSequencer(
          s120,
          const MetronomeOptions(playBars: 2, muteBars: 1),
        ),
        6,
      );
      final mutedBars = {
        for (final e in c)
          if (e.muted) e.bar,
      };
      expect(mutedBars, {2, 5});
    });

    test('ランダムに休む：だいたいその割合で、同じ種なら同じ休み方', () {
      const o = MetronomeOptions(randomMutePercent: 30);
      final a = bars(MetronomeSequencer(s120, o, seed: 1), 100);
      final b = bars(MetronomeSequencer(s120, o, seed: 1), 100);
      final ratio = a.where((e) => e.muted).length / a.length;
      expect(ratio, closeTo(0.3, 0.08));
      expect(a.map((e) => e.muted), b.map((e) => e.muted));
    });

    test('テンポの段階変化：2小節ごとに +10、130 に着いたら2小節で終わる', () {
      const o = MetronomeOptions(
        rampEnabled: true,
        rampTargetBpm: 130,
        rampStepBpm: 10,
        rampEveryBars: 2,
      );
      final seq = MetronomeSequencer(
        const MetronomeSettings(bpm: 100, beatsPerBar: 2),
        o,
      );
      final c = bars(seq, 20);
      final bpmByBar = {for (final e in c) e.bar: e.bpm};
      expect(bpmByBar, {
        0: 100, 1: 100, 2: 110, 3: 110, 4: 120, 5: 120, 6: 130, 7: 130, //
      });
      expect(seq.finished, isTrue);
      // 小節の境目でテンポが変わっても、時刻はつながる
      final bar2 = c.firstWhere((e) => e.bar == 2);
      expect(bar2.offsetMicros, 2 * 2 * 600000); // 100 BPM の2小節分
    });

    test('カウントイン：始める前の小節は数え（負の小節）。パターン・休みは効かない', () {
      final c = bars(
        MetronomeSequencer(
          const MetronomeSettings(bpm: 120, beatsPerBar: 4, subdivision: 2),
          const MetronomeOptions(countInBars: 1, randomMutePercent: 80),
        ),
        2,
      );
      final countIn = c.where((e) => e.countIn).toList();
      expect(countIn, hasLength(4)); // 細分なし
      expect(countIn.every((e) => e.bar == -1 && !e.muted), isTrue);
      expect(c.firstWhere((e) => !e.countIn).offsetMicros, 2000000);
    });

    test('ポリリズム：4拍子に 3 を重ねる', () {
      final c = MetronomeSequencer(
        s120,
        const MetronomeOptions(polyrhythm: 3),
      ).nextBar();
      final poly = c.where((e) => e.poly).map((e) => e.offsetMicros).toList();
      expect(poly, [0, 666667, 1333333]);
      expect(c.where((e) => !e.poly), hasLength(4));
    });

    test('設定の保存の形と、壊れた値', () {
      const o = MetronomeOptions(
        sound: ClickSound.wood,
        pattern: [BeatAccent.mute],
        rampEnabled: true,
        polyrhythm: 3,
        visual: MetronomeVisual.flash,
        timerMinutes: 10,
      );
      expect(MetronomeOptions.fromMap(o.toMap()), o);
      final broken = MetronomeOptions.fromMap({'poly': 99, 'randomMute': -5});
      expect(broken.polyrhythm, 9);
      expect(broken.randomMutePercent, 0);
    });
  });

  group('メトロノームの動き', () {
    testWidgets('音色・音量で予約し、休みの拍は予約しない', (tester) async {
      final engine = FakeAudioEngine()..time = const Duration(seconds: 1);
      final meta = MetaStore((await tester.runAsync(openMemoryDb))!);
      final c = MetronomeController(
        engine,
        meta,
        s120,
        options: const MetronomeOptions(
          sound: ClickSound.cowbell,
          volume: 0.6,
          pattern: [
            BeatAccent.accent,
            BeatAccent.mute,
            BeatAccent.normal,
            BeatAccent.normal,
          ],
        ),
      );
      await c.start();
      for (var i = 0; i < 80; i++) {
        engine.time += const Duration(milliseconds: 25);
        await tester.pump(MetronomeController.tickInterval);
      }
      // 2秒で 1小節：1・3・4拍目だけ（2拍目は休み）＋次の小節の1拍目
      expect(engine.scheduled.length, 4);
      expect(engine.clickSounds.toSet(), {ClickSound.cowbell});
      expect(engine.clickVolumes.toSet(), {0.6});
      c.stop();
    });

    testWidgets('練習タイマー：時間が来たら止まり、理由を出す', (tester) async {
      final engine = FakeAudioEngine();
      final meta = MetaStore((await tester.runAsync(openMemoryDb))!);
      final c = MetronomeController(
        engine,
        meta,
        s120,
        options: const MetronomeOptions(timerMinutes: 5),
      );
      await c.start();
      // 最初の拍（少し先）から数える
      expect(
        c.timeLeft,
        const Duration(minutes: 5) + MetronomeController.startLead,
      );
      engine.time += const Duration(minutes: 5, seconds: 1);
      await tester.pump(MetronomeController.tickInterval);
      await tester.pump(MetronomeController.tickInterval);
      expect(c.isRunning, isFalse);
      expect(c.stoppedReason, contains('タイマー'));
    });

    testWidgets('テンポの段階変化：目標に着いて鳴らし終えたら止まる', (tester) async {
      final engine = FakeAudioEngine();
      final meta = MetaStore((await tester.runAsync(openMemoryDb))!);
      final c = MetronomeController(
        engine,
        meta,
        const MetronomeSettings(bpm: 240, beatsPerBar: 1),
        options: const MetronomeOptions(
          rampEnabled: true,
          rampTargetBpm: 300,
          rampStepBpm: 30,
          rampEveryBars: 1,
        ),
      );
      await c.start();
      for (var i = 0; i < 80 && c.isRunning; i++) {
        engine.time += const Duration(milliseconds: 25);
        await tester.pump(MetronomeController.tickInterval);
      }
      expect(c.isRunning, isFalse);
      expect(c.stoppedReason, contains('目標のテンポ'));
      expect(engine.scheduled, hasLength(3)); // 240・270・300
    });
  });

  test('プリセット：保存・グループ・削除、グループを順に鳴らすクリックトラック', () async {
    final meta = MetaStore(await openMemoryDb());
    final lib = await MetronomePresetLibrary.load(meta);
    await lib.save(
      'ゆっくり',
      const MetronomeSettings(bpm: 60),
      const MetronomeOptions(),
      group: '曲A',
    );
    await lib.save(
      '',
      const MetronomeSettings(bpm: 132, beatsPerBar: 3),
      const MetronomeOptions(sound: ClickSound.wood),
      group: '曲A',
    );
    await lib.save('単独', const MetronomeSettings(), const MetronomeOptions());
    final again = await MetronomePresetLibrary.load(meta);
    expect(again.items.map((p) => p.name), ['ゆっくり', '132 BPM', '単独']);
    expect(again.groups, ['曲A']);
    expect(again.items[1].options.sound, ClickSound.wood);
    final track = presetsToClickTrack(
      '曲A',
      again.items.where((p) => p.group == '曲A').toList(),
    );
    expect(track.sections.map((s) => (s.bpm, s.beatsPerBar, s.bars)), [
      (60, 4, 8),
      (132, 3, 8),
    ]);
    await again.delete(again.items.first.id);
    expect(again.items, hasLength(2));
  });
}
