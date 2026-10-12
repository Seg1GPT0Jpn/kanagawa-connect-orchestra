import 'dart:math' as math;
import 'dart:typed_data';

import 'package:flutter_test/flutter_test.dart';
import 'package:kco_practice/core/meta_store.dart';
import 'package:kco_practice/features/audio_tools/data/mic_input.dart';
import 'package:kco_practice/features/audio_tools/data/reference_tone_controller.dart';
import 'package:kco_practice/features/audio_tools/data/tuner_controller.dart';
import 'package:kco_practice/features/audio_tools/domain/pitch.dart';

import '../../helpers.dart';

/// 44.1kHz の正弦波（[seconds] 秒）
Float64List sine(double hz, double seconds, {double amp = 0.4}) =>
    Float64List.fromList([
      for (var i = 0; i < (44100 * seconds).round(); i++)
        amp * math.sin(2 * math.pi * hz * i / 44100),
    ]);

void main() {
  late FakeMicInput mic;
  late ReferenceToneController pitch;
  late TunerController tuner;

  setUp(() async {
    mic = FakeMicInput();
    pitch = await ReferenceToneController.load(
      FakeAudioEngine(),
      MetaStore(await openMemoryDb()),
    );
    tuner = TunerController(mic, pitch);
  });

  test('pcm16ToFloat：16bit リトルエンディアン → -1〜1', () {
    final bytes = Uint8List.fromList([
      0x00,
      0x00,
      0xff,
      0x7f,
      0x00,
      0x80,
      0x00,
      0x40,
    ]);
    expect(pcm16ToFloat(bytes), [0, 32767 / 32768, -1, 0.5]);
  });

  test('マイクが許可されていなければエラーで、測らない', () async {
    mic.allowed = false;
    await tuner.start();
    expect(tuner.isListening, isFalse);
    expect(tuner.error, contains('許可'));
    expect(mic.running, isFalse);
  });

  test('A4＝442Hz・B♭管：実音 A4 を吹くと「記譜 B4・0セント」', () async {
    await tuner.start();
    expect(tuner.isListening, isTrue);
    expect(mic.sampleRate, 44100);
    tuner.addSamples(sine(442, 0.5));
    final r = tuner.reading!;
    expect(noteLabel(r.midi), 'A4');
    expect(noteLabel(pitch.pitch.transposition.concertToWritten(r.midi)), 'B4');
    expect(r.cents.abs(), lessThan(1));
    expect(tuner.level, greaterThan(0));
  });

  test('少し高い音（+20セント）・基準ピッチを変えたときのずれ', () async {
    await tuner.start();
    final f = 442 * math.pow(2, 20 / 1200).toDouble();
    tuner.addSamples(sine(f, 0.5));
    expect(tuner.reading!.cents, closeTo(20, 1.5));

    await pitch.updatePitch(pitch.pitch.copyWith(a4: 440));
    tuner.addSamples(sine(440, 0.5));
    expect(tuner.reading!.cents.abs(), lessThan(1.5));
  });

  test('音が止まって少したつと表示が消える。止めると初期状態に戻る', () async {
    await tuner.start();
    tuner.addSamples(sine(466.16, 0.3));
    expect(tuner.reading, isNotNull);
    tuner.addSamples(Float64List(44100 ~/ 2)); // 0.5秒の無音
    expect(tuner.reading, isNull);

    tuner.addSamples(sine(442, 0.3));
    await tuner.stop();
    expect(tuner.isListening, isFalse);
    expect(tuner.reading, isNull);
    expect(mic.running, isFalse);
  });
}
