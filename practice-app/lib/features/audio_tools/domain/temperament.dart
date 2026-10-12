/// 音律（決定論的）。平均律からのずれ（セント）を、主音からの音程ごとに持つ
///
/// 合奏では和音の中の役割で音程を少し変える（純正な響きにする）。
/// 例：長3度は平均律より約14セント低く、完全5度は約2セント高く。
library;

import 'dart:math' as math;

enum Temperament {
  equal('平均律', '12の半音がすべて同じ幅（チューナーのふつうの基準）'),
  justMajor('純正律（長調）', '主音に対して、和音がうなりなく響く高さ。長3度は約14セント低い'),
  justMinor('純正律（短調）', '短調の和音がうなりなく響く高さ。短3度は約16セント高い'),
  pythagorean('ピタゴラス音律', '純正な5度を積み重ねた高さ。旋律で音程を広めにとるときの目安');

  const Temperament(this.label, this.description);

  final String label;
  final String description;

  /// 主音からの半音数（0〜11）ごとの周波数比
  List<(int, int)> get _ratios => switch (this) {
    Temperament.equal => const [],
    Temperament.justMajor => const [
      (1, 1),
      (16, 15),
      (9, 8),
      (6, 5),
      (5, 4),
      (4, 3),
      (45, 32),
      (3, 2),
      (8, 5),
      (5, 3),
      (16, 9),
      (15, 8),
    ],
    Temperament.justMinor => const [
      (1, 1),
      (16, 15),
      (9, 8),
      (6, 5),
      (5, 4),
      (4, 3),
      (45, 32),
      (3, 2),
      (8, 5),
      (5, 3),
      (9, 5),
      (15, 8),
    ],
    Temperament.pythagorean => const [
      (1, 1),
      (256, 243),
      (9, 8),
      (32, 27),
      (81, 64),
      (4, 3),
      (729, 512),
      (3, 2),
      (128, 81),
      (27, 16),
      (16, 9),
      (243, 128),
    ],
  };

  /// 主音から [semitones] 半音上の音の、平均律からのずれ（セント）
  double offsetCents(int semitones) {
    if (this == Temperament.equal) return 0;
    final i = semitones % 12;
    final (n, d) = _ratios[i];
    return 1200 * math.log(n / d) / math.ln2 - 100 * i;
  }

  /// [midi]（実音）の、主音 [tonicPitchClass]（0=C〜11=B、実音）での平均律からのずれ
  double offsetFor(int midi, int tonicPitchClass) =>
      offsetCents((midi - tonicPitchClass) % 12);
}

/// 主音からの音程の名前（表示用）
const intervalNames = [
  '主音',
  '短2度',
  '長2度',
  '短3度',
  '長3度',
  '完全4度',
  '増4度',
  '完全5度',
  '短6度',
  '長6度',
  '短7度',
  '長7度',
];
