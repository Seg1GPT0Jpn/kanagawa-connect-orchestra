import 'dart:typed_data';

import 'package:flutter_test/flutter_test.dart';
import 'package:kco_practice/core/meta_store.dart';
import 'package:kco_practice/features/audio_tools/data/metronome_controller.dart';
import 'package:kco_practice/features/audio_tools/domain/metronome.dart';
import 'package:kco_practice/features/audio_tools/domain/wav.dart';

import '../../helpers.dart';

void main() {
  group('拍の計算', () {
    test('BPM 120 の4拍子：0.5秒ごと、1拍目が強拍', () {
      const s = MetronomeSettings(bpm: 120, beatsPerBar: 4);
      final clicks = clicksBetween(
        s,
        Duration.zero,
        const Duration(seconds: 2),
      );
      expect(clicks.map((c) => c.offset.inMilliseconds), [0, 500, 1000, 1500]);
      expect(clicks.map((c) => c.kind), [
        ClickKind.accent,
        ClickKind.beat,
        ClickKind.beat,
        ClickKind.beat,
      ]);
      expect(clickAt(s, 4).kind, ClickKind.accent); // 次の小節
      expect(clickAt(s, 5).beatInBar, 1);
    });

    test('3連の細分：1拍に3回、拍の頭だけが拍', () {
      const s = MetronomeSettings(bpm: 60, beatsPerBar: 2, subdivision: 3);
      final clicks = clicksBetween(
        s,
        Duration.zero,
        const Duration(seconds: 2),
      );
      expect(clicks, hasLength(6));
      expect(clicks.map((c) => c.kind).toList(), [
        ClickKind.accent,
        ClickKind.subdivision,
        ClickKind.subdivision,
        ClickKind.beat,
        ClickKind.subdivision,
        ClickKind.subdivision,
      ]);
      expect(clicks[1].offset.inMicroseconds, 333333);
    });

    test('「なし」（1拍子）・強拍オフでは強拍を鳴らさない', () {
      expect(
        clickAt(const MetronomeSettings(beatsPerBar: 1), 0).kind,
        ClickKind.beat,
      );
      expect(
        clickAt(const MetronomeSettings(accentFirstBeat: false), 0).kind,
        ClickKind.beat,
      );
    });

    test('clicksBetween は [from, to) で、つなげても重複・抜けがない', () {
      const s = MetronomeSettings(bpm: 97, subdivision: 2);
      final all = clicksBetween(s, Duration.zero, const Duration(seconds: 10));
      final pieces = [
        for (var t = 0; t < 10000; t += 137)
          ...clicksBetween(
            s,
            Duration(milliseconds: t),
            Duration(milliseconds: (t + 137).clamp(0, 10000)),
          ),
      ];
      expect(pieces.map((c) => c.index), all.map((c) => c.index));
    });

    test('範囲外の設定は収める・保存して読み戻せる', () {
      const s = MetronomeSettings(bpm: 999, beatsPerBar: 0, subdivision: 9);
      final n = s.normalized();
      expect([n.bpm, n.beatsPerBar, n.subdivision], [300, 1, 4]);
      const t = MetronomeSettings(
        bpm: 132,
        beatsPerBar: 3,
        subdivision: 2,
        accentFirstBeat: false,
      );
      expect(MetronomeSettings.fromMap(t.toMap()), t);
      expect(
        MetronomeSettings.fromMap({'bpm': 'x'}),
        const MetronomeSettings(),
      );
    });

    test('タップテンポ：間隔の中央値、2秒以上あいたら数えない', () {
      Duration ms(int v) => Duration(milliseconds: v);
      expect(tapTempo([ms(0)]), isNull);
      expect(tapTempo([ms(0), ms(500), ms(1000), ms(1500)]), 120);
      // 1回だけ遅れても中央値なので 120 のまま
      expect(tapTempo([ms(0), ms(500), ms(1000), ms(1700), ms(2200)]), 120);
      // 古いタップのあと3秒あいたら、そこから前は使わない
      expect(tapTempo([ms(0), ms(1000), ms(4000), ms(4600)]), 100);
      expect(tapTempo([ms(0), ms(10)]), 300); // 上限に収める
    });
  });

  test('クリック音の WAV：ヘッダーと長さ', () {
    final wav = clickWav(
      frequency: 1000,
      duration: const Duration(milliseconds: 40),
    );
    final b = ByteData.sublistView(wav);
    expect(String.fromCharCodes(wav.sublist(0, 4)), 'RIFF');
    expect(String.fromCharCodes(wav.sublist(8, 12)), 'WAVE');
    expect(b.getUint32(24, Endian.little), 44100);
    expect(b.getUint32(40, Endian.little), 1764 * 2); // 40ms ＝ 1764サンプル
    expect(wav.length, 44 + 1764 * 2);
    expect(b.getInt16(44, Endian.little), 0); // 無音から立ち上がる
  });

  group('MetronomeController', () {
    late FakeAudioEngine engine;
    late MetaStore meta;

    Future<MetronomeController> controller(WidgetTester tester) async {
      engine = FakeAudioEngine()..time = const Duration(seconds: 10);
      meta = MetaStore((await tester.runAsync(openMemoryDb))!);
      return (await tester.runAsync(
        () => MetronomeController.load(engine, meta),
      ))!;
    }

    testWidgets('鳴らすと、少し先までのクリックを正確な時刻に予約し続ける', (tester) async {
      final c = await controller(tester);
      await c.update(c.settings.copyWith(bpm: 120, beatsPerBar: 4));
      await c.start();
      expect(c.isRunning, isTrue);
      // 開始の余裕（100ms）のあとに1拍目
      final anchor =
          const Duration(seconds: 10) + MetronomeController.startLead;
      expect(engine.scheduled.first, (ClickKind.accent, anchor));

      // 音の時計を1.2秒進めながら、タイマーを動かす
      for (var i = 0; i < 48; i++) {
        engine.time += const Duration(milliseconds: 25);
        await tester.pump(MetronomeController.tickInterval);
      }
      final times = engine.scheduled.map((e) => e.$2 - anchor).toList();
      expect(times.map((d) => d.inMilliseconds), [0, 500, 1000]);
      expect(engine.scheduled.map((e) => e.$1), [
        ClickKind.accent,
        ClickKind.beat,
        ClickKind.beat,
      ]);
      expect(c.currentBeat, 2);

      c.stop();
      expect(c.isRunning, isFalse);
      expect(c.currentBeat, isNull);
      expect(engine.cancelCount, 1);
    });

    testWidgets('動いている間にテンポを変えると、予約を取り消して新しいテンポで続ける', (tester) async {
      final c = await controller(tester);
      await c.start();
      engine.time += const Duration(milliseconds: 300);
      await tester.pump(MetronomeController.tickInterval);
      final before = engine.cancelCount;
      await tester.runAsync(() => c.update(c.settings.copyWith(bpm: 200)));
      expect(engine.cancelCount, before + 1);
      expect(c.settings.bpm, 200);
      // 設定は保存される
      final saved =
          (await tester.runAsync(() => meta.get('metronome.settings')))! as Map;
      expect(saved['bpm'], 200);
      c.stop();
    });

    testWidgets('音を出せないときは止まったままで、エラーを出す', (tester) async {
      final m = MetaStore((await tester.runAsync(openMemoryDb))!);
      final c = MetronomeController(
        FakeAudioEngine(failToStart: true),
        m,
        const MetronomeSettings(),
      );
      await c.start();
      expect(c.isRunning, isFalse);
      expect(c.error, isNotNull);
    });

    testWidgets('タップでテンポが決まる', (tester) async {
      final c = await controller(tester);
      for (final t in [0, 750, 1500, 2250]) {
        await tester.runAsync(() => c.tap(Duration(milliseconds: t)));
      }
      expect(c.settings.bpm, 80);
    });
  });
}
