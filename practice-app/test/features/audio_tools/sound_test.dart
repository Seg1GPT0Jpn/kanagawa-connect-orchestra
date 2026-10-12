import 'package:flutter_test/flutter_test.dart';
import 'package:kco_practice/core/meta_store.dart';
import 'package:kco_practice/features/audio_tools/data/audio_engine.dart';
import 'package:kco_practice/features/audio_tools/data/mixer_controller.dart';
import 'package:kco_practice/features/audio_tools/domain/metronome.dart';
import 'package:kco_practice/features/audio_tools/domain/sound.dart';

import '../../helpers.dart';

void main() {
  group('クリック音の音色', () {
    for (final sound in ClickSound.values) {
      test('${sound.label}：強拍・拍・細分とも音が入っていて、割れない（同じ入力なら同じ音）', () {
        double peak(ClickKind k) {
          final pcm = decodePcm16Wav(clickSoundWav(sound, k));
          expect(pcm.sampleRate, 44100);
          expect(pcm.samples.length, greaterThan(100));
          return pcm.samples.fold<double>(
            0,
            (m, v) => v.abs() > m ? v.abs() : m,
          );
        }

        final accent = peak(ClickKind.accent);
        final beat = peak(ClickKind.beat);
        final sub = peak(ClickKind.subdivision);
        for (final p in [accent, beat, sub]) {
          expect(p, greaterThan(0.05));
          expect(p, lessThanOrEqualTo(1));
        }
        // 細分は拍より小さい
        expect(sub, lessThan(beat));
        expect(
          clickSoundWav(sound, ClickKind.beat),
          clickSoundWav(sound, ClickKind.beat),
        );
      });
    }
  });

  test('音色：倍音の合計で割ると山が 1 を超えない', () {
    for (final t in Timbre.values) {
      expect(t.harmonics.first, 1);
      expect(
        t.gain * t.harmonics.fold<double>(0, (a, b) => a + b),
        closeTo(1, 1e-9),
      );
    }
    expect(Timbre.byName('brass'), Timbre.brass);
    expect(Timbre.byName('なし'), Timbre.sine);
    expect(ClickSound.byName('wood'), ClickSound.wood);
    expect(ClickSound.byName(null), ClickSound.beep);
  });

  group('ミキサーと音のテスト', () {
    test('音量を変えると覚えておき、次に開いたときも同じ', () async {
      final engine = FakeAudioEngine();
      final meta = MetaStore(await openMemoryDb());
      final m = await MixerController.load(engine, meta);
      expect(m.volumeOf(AudioChannel.tone), 1);
      await m.setVolume(AudioChannel.tone, 0.3);
      expect(engine.volumeOf(AudioChannel.tone), 0.3);

      final engine2 = FakeAudioEngine();
      final m2 = await MixerController.load(engine2, meta);
      expect(m2.volumeOf(AudioChannel.tone), 0.3);
      expect(m2.volumeOf(AudioChannel.click), 1);
    });

    test('テスト音はクリックを3回予約する。音を出せなければ案内を出す', () async {
      final meta = MetaStore(await openMemoryDb());
      final engine = FakeAudioEngine();
      final m = await MixerController.load(engine, meta);
      await m.playTest();
      expect(engine.scheduled, hasLength(3));
      expect(engine.scheduled.first.$1, ClickKind.accent);
      expect(m.testResult, contains('3回'));

      await m.setVolume(AudioChannel.click, 0);
      await m.playTest();
      expect(m.testResult, contains('音量が 0'));

      final broken = await MixerController.load(
        FakeAudioEngine(failToStart: true),
        meta,
      );
      await broken.playTest();
      expect(broken.testResult, isNotNull);
      expect(broken.isTesting, isFalse);
    });
  });
}
