import 'package:flutter_test/flutter_test.dart';
import 'package:kco_practice/core/meta_store.dart';
import 'package:kco_practice/features/audio_tools/data/exercise_player.dart';
import 'package:kco_practice/features/audio_tools/data/reference_tone_controller.dart';
import 'package:kco_practice/features/audio_tools/data/temperament_library.dart';
import 'package:kco_practice/features/audio_tools/domain/exercise.dart';
import 'package:kco_practice/features/audio_tools/domain/pitch.dart';
import 'package:kco_practice/features/audio_tools/domain/sound.dart';
import 'package:kco_practice/features/audio_tools/domain/temperament.dart';

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

  tearDown(() => currentNaming = NoteNaming.english);

  group('基準音', () {
    test('和音：純正律（主音 B♭）の長三和音は、3度が約14セント低い高さで鳴る', () async {
      await c.updatePitch(
        c.pitch.copyWith(
          temperament: Temperament.justMajor,
          tonicPitchClass: 10,
        ),
      );
      await c.playChord(58, ChordType.major); // B♭3・D4・F4
      expect(c.held, {58, 62, 65});
      expect(engine.voices, hasLength(3));
      final third = engine.voices.values
          .map((v) => v.hz)
          .firstWhere((hz) => (hz - midiToFrequency(62, a4: 442)).abs() < 5);
      expect(
        centsBetween(third, midiToFrequency(62, a4: 442)),
        closeTo(-13.7, 0.1),
      );

      // 1音外す・止める
      await c.toggleHeld(62);
      expect(c.held, {58, 65});
      expect(engine.voices, hasLength(2));
      c.stopHeld();
      expect(engine.voices, isEmpty);
      expect(c.isPlaying, isFalse);
    });

    test('ドローンは主音と5度を低めの音域で。1つの音と同時に鳴らせ、すべて止められる', () async {
      await c.playDrone();
      expect(c.held, {46, 53}); // B♭2・F3
      await c.toggle();
      expect(c.isSinglePlaying, isTrue);
      expect(engine.voices, hasLength(3));
      c.stop();
      expect(engine.voices, isEmpty);
    });

    test('音色と音量は鳴っている音にも効き、保存される', () async {
      await c.toggle();
      await c.setTimbre(Timbre.brass);
      await c.setVolume(0.8);
      expect(engine.voices[0]!.timbre, Timbre.brass);
      expect(engine.voices[0]!.volume, 0.8);
      final again = await ReferenceToneController.load(FakeAudioEngine(), meta);
      expect(again.timbre, Timbre.brass);
      expect(again.volume, 0.8);
    });
  });

  group('音名の表記と楽器', () {
    test('表記を変えると、どの画面の音名も同じ表記になる（保存もする）', () async {
      expect(noteLabel(70), 'B♭4');
      await c.updatePitch(c.pitch.copyWith(naming: NoteNaming.german));
      expect(noteLabel(70), 'B4');
      expect(noteLabel(71), 'H4');
      await c.updatePitch(c.pitch.copyWith(naming: NoteNaming.solfege));
      expect(noteLabel(60), 'ド4');
      await ReferenceToneController.load(FakeAudioEngine(), meta);
      expect(currentNaming, NoteNaming.solfege);
    });

    test('楽器の調：アルトサックスは記譜 C が実音 E♭（6度下）、テナーは9度下', () {
      expect(Transposition.eFlatAlto.writtenToConcert(60), 51);
      expect(Transposition.bFlatTenor.writtenToConcert(62), 48);
      expect(Transposition.piccolo.writtenToConcert(60), 72);
      final alto = instrumentPresets.firstWhere((i) => i.$1 == 'アルトサックス');
      expect(alto.$2, Transposition.eFlatAlto);
    });
  });

  group('自分の音律', () {
    test('作った音律で目標と基準音の高さが決まり、設定として保存される', () async {
      final lib = await TemperamentLibrary.load(meta);
      final offsets = List<double>.filled(12, 0)
        ..[4] = -14
        ..[7] = 2;
      final t = await lib.create('自分の純正', offsets);
      await c.updatePitch(
        c.pitch.copyWith(
          temperament: Temperament.custom,
          custom: t,
          tonicPitchClass: 10,
        ),
      );
      expect(c.pitch.offsetFor(62), -14); // D は B♭ の長3度
      expect(c.pitch.offsetFor(65), 2); // F は完全5度
      expect(c.pitch.temperamentLabel, '自分の純正・主音 B♭');
      final back = PitchSettings.fromMap(c.pitch.toMap());
      expect(back.usesCustom, isTrue);
      expect(back.offsetFor(62), -14);
      // 音律が壊れていたら平均律で読む
      expect(
        PitchSettings.fromMap({'temperament': 'custom'}).temperament,
        Temperament.equal,
      );
    });

    test('複製・編集・削除・共有の文字で取り込み。壊れた文字は読まない', () async {
      final lib = await TemperamentLibrary.load(meta);
      final t = await lib.create('A', List.filled(12, 0));
      final copy = await lib.duplicate(t);
      expect(copy.name, 'Aのコピー');
      await lib.update(copy.copyWith(offsets: List.filled(12, 99)));
      expect(lib.byId(copy.id)!.offsets.first, CustomTemperament.maxOffset);
      final text = lib.exportText(lib.byId(copy.id)!);
      final imported = await lib.importText(text);
      expect(imported!.name, 'Aのコピー');
      expect(await lib.importText('{"format":"other"}'), isNull);
      expect(await lib.importText('壊れた'), isNull);
      await lib.delete(t.id);
      final again = await TemperamentLibrary.load(meta);
      expect(again.items.map((e) => e.name), ['Aのコピー', 'Aのコピー']);
    });

    test('ひな形：ミーントーン・ヴェルクマイスターを含む12音分', () {
      expect(temperamentTemplates.length, greaterThanOrEqualTo(6));
      for (final (_, o) in temperamentTemplates) {
        expect(o, hasLength(12));
      }
    });
  });

  group('練習音型', () {
    test('長音階を上がって下りる・リップスラーはピストンで下がる', () {
      expect(buildExercise(ExerciseKind.majorScale, root: 60), [
        60, 62, 64, 65, 67, 69, 71, 72, 71, 69, 67, 65, 64, 62, 60, //
      ]);
      expect(
        buildExercise(
          ExerciseKind.lipSlur,
          root: 0,
          valves: ValveCombo.v2,
          upDown: false,
        ),
        [59, 66, 71, 75, 78],
      );
      expect(buildExercise(ExerciseKind.fifths, root: 60), [
        60,
        67,
        60,
        67,
        60,
      ]);
    });

    testWidgets('テンポに合わせて順に鳴らし、終わると止まる', (tester) async {
      final player = ExercisePlayer(c);
      // 1音 0.5秒
      player.play([60, 62, 64], bpm: 120);
      await tester.pump();
      expect(player.index, 0);
      expect(c.writtenMidi, 60);
      await tester.pump(const Duration(milliseconds: 510));
      expect(player.index, 1);
      expect(c.writtenMidi, 62);
      await tester.pump(const Duration(milliseconds: 500));
      await tester.pump(const Duration(milliseconds: 500));
      expect(player.isPlaying, isFalse);
      expect(c.isPlaying, isFalse);
    });
  });
}
