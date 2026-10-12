import 'package:kco_practice/features/menu/domain/menu_rules.dart';

/// Arban の章の id（ルールの順番）
final arbanIds = trumpetBasicRules
    .itemsInGroup('arban')
    .map((i) => i.id)
    .toList();

/// トランペット基礎メニュー（全項目そろった形）。Arban は渡した章だけ分数を入れ、ほかは 0
Map<String, int> menu({
  int mouthpiece = 20,
  int longTone = 15,
  int lipSlur = 5,
  int tonguing = 5,
  Map<String, int> arban = const {
    'arban_slurs': 10,
    'arban_scales': 10,
    'arban_tonguing': 10,
  },
}) => {
  'mouthpiece': mouthpiece,
  'long_tone': longTone,
  'lip_slur': lipSlur,
  'tonguing': tonguing,
  for (final id in arbanIds) id: arban[id] ?? 0,
};
