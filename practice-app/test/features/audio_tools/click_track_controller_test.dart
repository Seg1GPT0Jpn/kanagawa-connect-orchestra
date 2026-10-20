import 'package:flutter_test/flutter_test.dart';
import 'package:kco_practice/core/meta_store.dart';
import 'package:kco_practice/features/audio_tools/data/click_track_controller.dart';
import 'package:kco_practice/features/audio_tools/data/metronome_controller.dart';
import 'package:kco_practice/features/audio_tools/domain/click_track.dart';
import 'package:kco_practice/features/audio_tools/domain/metronome.dart';

import '../../helpers.dart';

void main() {
  late FakeAudioEngine engine;
  late MetaStore meta;

  Future<ClickTrackController> load(WidgetTester tester) async {
    engine = FakeAudioEngine()..time = const Duration(seconds: 5);
    meta = MetaStore((await tester.runAsync(openMemoryDb))!);
    return (await tester.runAsync(
      () => ClickTrackController.load(engine, meta),
    ))!;
  }

  /// 音の時計を [ms] ミリ秒進めながらタイマーを動かす
  Future<void> advance(WidgetTester tester, int ms) async {
    for (var t = 0; t < ms; t += 25) {
      engine.time += const Duration(milliseconds: 25);
      await tester.pump(ClickTrackController.tickInterval);
    }
  }

  testWidgets('初めは1つのトラック（予備拍1小節・4小節・♩=120）', (tester) async {
    final c = await load(tester);
    expect(c.tracks, hasLength(1));
    expect(c.track.countInBars, 1);
    expect(c.track.sections.single, const ClickSection());
  });

  testWidgets('鳴らすと時刻表どおりに予約し、最後まで行くと自動で止まる', (tester) async {
    final c = await load(tester);
    await tester.runAsync(
      () => c.updateTrack(
        const ClickTrack(
          countInBars: 0,
          sections: [
            ClickSection(bars: 1, bpm: 120, beatsPerBar: 2),
            ClickSection(bars: 1, bpm: 60, beatsPerBar: 2),
          ],
        ),
      ),
    );
    await c.play();
    expect(c.isPlaying, isTrue);
    final anchor = const Duration(seconds: 5) + ClickTrackController.startLead;
    await advance(tester, 1200);
    expect(c.position!.section, 1); // 1秒で区間2へ
    expect(c.position!.bar, 2);
    await advance(tester, 2000);
    // 全体 1 + 2 = 3秒で止まる
    expect(c.isPlaying, isFalse);
    expect(engine.scheduled.map((e) => (e.$2 - anchor).inMilliseconds), [
      0,
      500,
      1000,
      2000,
    ]);
    expect(engine.scheduled.map((e) => e.$1), [
      ClickKind.accent,
      ClickKind.beat,
      ClickKind.accent,
      ClickKind.beat,
    ]);
  });

  testWidgets('トラックの追加・名前の変更・削除は保存され、読み直しても残る', (tester) async {
    final c = await load(tester);
    await tester.runAsync(c.addTrack);
    expect(c.tracks, hasLength(2));
    expect(c.selectedIndex, 1);
    await tester.runAsync(
      () => c.updateTrack(c.track.copyWith(name: '序曲', countInBars: 2)),
    );
    final again = (await tester.runAsync(
      () => ClickTrackController.load(engine, meta),
    ))!;
    expect(again.tracks.map((t) => t.name), ['新しいクリックトラック', '序曲']);
    expect(again.tracks[1].countInBars, 2);
    await tester.runAsync(again.deleteTrack);
    await tester.runAsync(again.deleteTrack);
    expect(again.tracks, hasLength(1)); // 0個にはならない
  });

  testWidgets('メトロノームとは、あとから鳴らした方だけが鳴る', (tester) async {
    final c = await load(tester);
    final m = MetronomeController(engine, meta, const MetronomeSettings());
    m.onStarted = c.stop;
    c.onStarted = m.stop;
    await m.start();
    expect(m.isRunning, isTrue);
    await c.play();
    expect(c.isPlaying, isTrue);
    expect(m.isRunning, isFalse);
    await m.start();
    expect(c.isPlaying, isFalse);
    m.stop();
  });
}
