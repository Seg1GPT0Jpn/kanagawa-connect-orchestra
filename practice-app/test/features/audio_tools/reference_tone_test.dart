import 'package:flutter_test/flutter_test.dart';
import 'package:kco_practice/core/meta_store.dart';
import 'package:kco_practice/features/audio_tools/data/reference_tone_controller.dart';
import 'package:kco_practice/features/audio_tools/domain/pitch.dart';

import '../../helpers.dart';

void main() {
  late FakeAudioEngine engine;
  late MetaStore meta;
  late ReferenceToneController c;

  setUp(() async {
    engine = FakeAudioEngine();
    meta = MetaStore(await openMemoryDb());
    c = await ReferenceToneController.load(engine, meta);
  });

  test('初期値：A4＝442Hz・B♭管、A4（記譜 B4）', () {
    expect(c.pitch.a4, 442);
    expect(c.pitch.transposition, Transposition.bFlat);
    expect(c.concertMidi, 69);
    expect(c.writtenMidi, 71);
    expect(c.frequency, 442);
  });

  test('鳴らす・止める。鳴っている間に音や基準ピッチを変えると高さが変わる', () async {
    await c.toggle();
    expect(c.isPlaying, isTrue);
    expect(engine.toneHz, 442);
    await c.selectWritten(60); // 記譜 C4 ＝ 実音 B♭3
    expect(c.concertMidi, 58);
    expect(engine.toneHz, closeTo(midiToFrequency(58, a4: 442), 1e-9));
    await c.updatePitch(c.pitch.copyWith(a4: 440));
    expect(engine.toneHz, closeTo(midiToFrequency(58), 1e-9));
    await c.toggle();
    expect(c.isPlaying, isFalse);
    expect(engine.toneHz, isNull);
  });

  test('基準ピッチは 430〜450Hz に収め、保存して読み戻せる', () async {
    await c.updatePitch(
      c.pitch.copyWith(a4: 500, transposition: Transposition.concert),
    );
    expect(c.pitch.a4, 450);
    final again = await ReferenceToneController.load(engine, meta);
    expect(again.pitch.a4, 450);
    expect(again.pitch.transposition, Transposition.concert);
  });

  test('音を出せないときはエラーを出して鳴らさない', () async {
    final failing = ReferenceToneController(
      FakeAudioEngine(failToStart: true),
      meta,
      const PitchSettings(),
    );
    await failing.toggle();
    expect(failing.isPlaying, isFalse);
    expect(failing.error, isNotNull);
  });
}
