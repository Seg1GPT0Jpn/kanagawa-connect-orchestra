import 'dart:math' as math;
import 'dart:typed_data';

import 'package:flutter_test/flutter_test.dart';
import 'package:kco_practice/core/meta_store.dart';
import 'package:kco_practice/features/audio_tools/data/reference_tone_controller.dart';
import 'package:kco_practice/features/audio_tools/domain/pitch.dart';
import 'package:kco_practice/features/recording/data/recording_controller.dart';
import 'package:kco_practice/features/recording/data/recording_repository.dart';
import 'package:kco_practice/features/recording/domain/recording_result.dart';

import '../../helpers.dart';

/// 44.1kHz の音（倍音入り）
Float64List tone44(double hz, double seconds, {double amp = 0.4}) =>
    Float64List.fromList([
      for (var i = 0; i < (44100 * seconds).round(); i++)
        amp *
            (0.7 * math.sin(2 * math.pi * hz * i / 44100) +
                0.3 * math.sin(4 * math.pi * hz * i / 44100)),
    ]);

void main() {
  late FakeMicInput mic;
  late FakeAudioEngine audio;
  late RecordingRepository repo;
  late RecordingController c;
  final clock = FakeClock(DateTime(2026, 10, 12, 19));

  setUp(() async {
    mic = FakeMicInput();
    audio = FakeAudioEngine();
    final db = await openMemoryDb();
    final pitch = await ReferenceToneController.load(audio, MetaStore(db));
    repo = RecordingRepository(db);
    c = RecordingController(
      mic: mic,
      audio: audio,
      pitch: pitch,
      repository: repo,
      clock: clock.call,
    );
  });

  test('マイクが許可されていなければ録音しない', () async {
    mic.allowed = false;
    await c.start();
    expect(c.phase, RecordingPhase.idle);
    expect(c.error, contains('許可'));
  });

  test('録音して止めると分析される（実音 B♭4・A4=442）', () async {
    await c.start();
    expect(c.phase, RecordingPhase.recording);
    // 連続した2秒の音を、マイクのように0.1秒ずつ流す
    final whole = tone44(midiToFrequency(70, a4: 442), 2);
    for (var i = 0; i < 20; i++) {
      c.addSamples(Float64List.sublistView(whole, i * 4410, (i + 1) * 4410));
    }
    expect(c.elapsed.inMilliseconds, closeTo(2000, 5));
    await c.stop();
    expect(c.phase, RecordingPhase.done);
    expect(mic.running, isFalse);
    final r = c.result!;
    expect(noteLabel(r.midi), 'B♭4');
    expect(r.centsOffset.abs(), lessThan(1.5));
    expect(r.pitchSpreadCents, lessThan(1.5));
  });

  test('音が入っていなければ分析せず案内する', () async {
    await c.start();
    c.addSamples(Float64List(44100));
    await c.stop();
    expect(c.result, isNull);
    expect(c.error, contains('音がほとんど'));
  });

  test('上限（30秒）で自動的に止まる', () async {
    await c.start();
    for (var i = 0; i < 31; i++) {
      c.addSamples(tone44(440, 1));
    }
    await Future<void>.delayed(Duration.zero);
    expect(c.phase, RecordingPhase.done);
    expect(c.elapsed.inSeconds, inInclusiveRange(30, 31));
  });

  test('聴き直す：22.05kHz の WAV を再生し、終われば止まる', () async {
    await c.start();
    c.addSamples(tone44(440, 1));
    await c.stop();
    await c.play();
    expect(c.isPlaying, isTrue);
    final wav = audio.playedWav!;
    expect(ByteData.sublistView(wav).getUint32(24, Endian.little), 22050);
    expect(wav.length, 44 + 22050 * 2);
    audio.onPlaybackDone!();
    expect(c.isPlaying, isFalse);
  });

  test('結果を保存すると履歴に出る（音声は保存しない）。二重には保存しない', () async {
    await c.start();
    c.addSamples(tone44(466.16, 1.5));
    await c.stop();
    await c.save();
    await c.save();
    expect(c.isSaved, isTrue);
    final all = await repo.all();
    expect(all, hasLength(1));
    final r = all.single;
    expect(r.recordedAtMillis, clock.now.millisecondsSinceEpoch);
    expect(r.a4, 442);
    expect(r.toMap().keys, isNot(contains('audio')));
    // 保存した形から読み戻せる
    expect(RecordingResult.fromMap(r.toMap()).toMap(), r.toMap());
    await repo.delete(r.id);
    expect(await repo.all(), isEmpty);
  });

  test('録り直すと前の結果は消える', () async {
    await c.start();
    c.addSamples(tone44(440, 1));
    await c.stop();
    c.reset();
    expect(c.phase, RecordingPhase.idle);
    expect(c.result, isNull);
    expect(c.elapsed, Duration.zero);
  });
}
