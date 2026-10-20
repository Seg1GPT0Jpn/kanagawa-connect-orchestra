/// 練習音型を作る（音階・分散和音・倍音列のリップスラーなど。決定論的）
///
/// 音は記譜の MIDI 番号で作る（楽器の調で実音に直して鳴らす）。
library;

enum ExerciseKind {
  majorScale('長音階'),
  minorScale('短音階（和声的）'),
  chromatic('半音階'),
  majorArpeggio('分散和音（長）'),
  minorArpeggio('分散和音（短）'),
  fifths('5度の往復'),
  lipSlur('リップスラー（倍音列）');

  const ExerciseKind(this.label);
  final String label;
}

/// トランペットのピストンの組み合わせ（下げる半音の数）
enum ValveCombo {
  open('開放', 0),
  v2('2', 1),
  v1('1', 2),
  v12('1・2', 3),
  v23('2・3', 4),
  v13('1・3', 5),
  v123('1・2・3', 6);

  const ValveCombo(this.label, this.semitones);
  final String label;
  final int semitones;
}

/// 倍音（記譜。開放の B♭ トランペットで 2倍音＝記譜 C4）の、記譜 C4 からの半音
/// 2:C4 3:G4 4:C5 5:E5 6:G5 7:B♭5（実際は低め） 8:C6
const harmonicSteps = {2: 0, 3: 7, 4: 12, 5: 16, 6: 19, 7: 22, 8: 24};

/// [kind] の音型。[root] は記譜の主音（リップスラーでは使わず [valves] と倍音の範囲で決める）。
/// [upDown] なら上がって下りる
List<int> buildExercise(
  ExerciseKind kind, {
  required int root,
  bool upDown = true,
  ValveCombo valves = ValveCombo.open,
  int lowPartial = 2,
  int highPartial = 6,
}) {
  final up = switch (kind) {
    ExerciseKind.majorScale => [0, 2, 4, 5, 7, 9, 11, 12],
    ExerciseKind.minorScale => [0, 2, 3, 5, 7, 8, 11, 12],
    ExerciseKind.chromatic => [for (var i = 0; i <= 12; i++) i],
    ExerciseKind.majorArpeggio => [0, 4, 7, 12],
    ExerciseKind.minorArpeggio => [0, 3, 7, 12],
    ExerciseKind.fifths => [0, 7, 0, 7, 0],
    ExerciseKind.lipSlur => [
      for (var p = lowPartial; p <= highPartial; p++) ?harmonicSteps[p],
    ],
  };
  final base = kind == ExerciseKind.lipSlur ? 60 - valves.semitones : root;
  final notes = [for (final s in up) base + s];
  if (!upDown || kind == ExerciseKind.fifths || notes.length < 2) return notes;
  return [...notes, ...notes.reversed.skip(1)];
}
