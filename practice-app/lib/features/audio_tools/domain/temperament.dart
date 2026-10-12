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
  pythagorean('ピタゴラス音律', '純正な5度を積み重ねた高さ。旋律で音程を広めにとるときの目安'),
  custom('自分で作った音律', '音ごとのずれを自分で決めた音律');

  const Temperament(this.label, this.description);

  final String label;
  final String description;

  /// 主音からの半音数（0〜11）ごとの周波数比
  List<(int, int)> get _ratios => switch (this) {
    Temperament.equal || Temperament.custom => const [],
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
    if (this == Temperament.equal || this == Temperament.custom) return 0;
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

/// 自分で作る音律：主音からの半音ごとに、平均律からのずれ（セント）を決める
class CustomTemperament {
  const CustomTemperament({
    required this.id,
    required this.name,
    required this.offsets,
  }) : assert(offsets.length == 12);

  final String id;
  final String name;

  /// [0] が主音、[1] が短2度 …（平均律からのずれ・セント）
  final List<double> offsets;

  /// ずれの範囲（大きすぎる値は打ち間違いとして直す）
  static const maxOffset = 50.0;

  CustomTemperament copyWith({String? name, List<double>? offsets}) =>
      CustomTemperament(
        id: id,
        name: name ?? this.name,
        offsets: offsets ?? this.offsets,
      );

  Map<String, Object?> toMap() => {'id': id, 'name': name, 'offsets': offsets};

  /// 壊れた値は読まない（null）
  static CustomTemperament? fromMap(Object? raw) {
    if (raw is! Map) return null;
    final id = raw['id'], name = raw['name'], o = raw['offsets'];
    if (id is! String || name is! String || o is! List || o.length != 12) {
      return null;
    }
    if (o.any((v) => v is! num)) return null;
    return CustomTemperament(
      id: id,
      name: name.length > 40 ? name.substring(0, 40) : name,
      offsets: [
        for (final v in o)
          (v as num).toDouble().clamp(-maxOffset, maxOffset).toDouble(),
      ],
    );
  }
}

/// 作るときのひな形（主音を C にすると本来の形になる、歴史的な音律も含む）
final temperamentTemplates = <(String, List<double>)>[
  ('平均律', List.filled(12, 0)),
  for (final t in [
    Temperament.justMajor,
    Temperament.justMinor,
    Temperament.pythagorean,
  ])
    (t.label, [for (var i = 0; i < 12; i++) t.offsetCents(i)]),
  // 1/4 シントニックコンマ・ミーントーン（C を主音に。A を 0 にそろえた値）
  (
    'ミーントーン（1/4コンマ）',
    [10.3, -13.7, 3.4, 20.5, -3.4, 13.7, -10.3, 6.8, -17.1, 0, 17.1, -6.8],
  ),
  // ヴェルクマイスター第3（C を主音に）
  (
    'ヴェルクマイスター第3',
    [0, -9.8, -7.8, -5.9, -9.8, -2.0, -11.7, -3.9, -7.8, -11.7, -3.9, -7.8],
  ),
];
