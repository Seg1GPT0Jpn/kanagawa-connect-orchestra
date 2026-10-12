/// 「今日の重点」のおすすめメニュー
///
/// プロ奏者・指導者の練習法の調査（practice-app/docs/practice-research.md）をもとにした配分。
/// 特定の奏者のメニューをそのまま写したものではない。どの案もルール（menu_rules.dart）を満たすことを
/// テストで確かめている。選んだあとで自由に変えられる。
library;

class MenuPreset {
  const MenuPreset({
    required this.id,
    required this.label,
    required this.description,
    required this.minutes,
  });

  final String id;
  final String label;

  /// どんな日に使うか・なぜこの配分か
  final String description;

  /// 項目 id → 分（ここにない項目は 0 分）
  final Map<String, int> minutes;

  Map<String, int> menuFor(Iterable<String> itemIds) => {
    for (final id in itemIds) id: minutes[id] ?? 0,
  };
}

const trumpetBasicPresets = [
  MenuPreset(
    id: 'balanced',
    label: 'バランス',
    description: '音色・柔軟性・指・発音をひととおり。迷ったらこれ',
    minutes: {
      'mouthpiece': 20,
      'long_tone': 15,
      'lip_slur': 5,
      'tonguing': 5,
      'arban_slurs': 10,
      'arban_scales': 10,
      'arban_tonguing': 10,
    },
  ),
  MenuPreset(
    id: 'short',
    label: '短め（45分）',
    description: '時間がない日・合奏や本番がある日。全部を詰め込まず、整えるだけ',
    minutes: {
      'mouthpiece': 15,
      'long_tone': 10,
      'arban_slurs': 10,
      'arban_scales': 10,
    },
  ),
  MenuPreset(
    id: 'tone_flexibility',
    label: '音色・柔軟性',
    description: '音の芯・響き・音の切り替え。高音や大音量を多く吹いた翌日にも',
    minutes: {
      'mouthpiece': 20,
      'long_tone': 20,
      'lip_slur': 15,
      'arban_slurs': 15,
      'arban_phrasing': 10,
    },
  ),
  MenuPreset(
    id: 'fingers_scales',
    label: '指・音階',
    description: '全調の音階・半音階・跳躍。指と息の連携、均一な音の流れ',
    minutes: {
      'mouthpiece': 15,
      'long_tone': 10,
      'lip_slur': 5,
      'tonguing': 5,
      'arban_scales': 15,
      'arban_chromatic': 10,
      'arban_intervals': 10,
    },
  ),
  MenuPreset(
    id: 'articulation',
    label: 'タンギング',
    description: 'シングル・ダブル・トリプル。粒がそろうテンポで、速さは後から',
    minutes: {
      'mouthpiece': 15,
      'long_tone': 10,
      'lip_slur': 5,
      'tonguing': 10,
      'arban_first_studies': 5,
      'arban_syncopation': 5,
      'arban_tonguing': 20,
    },
  ),
  MenuPreset(
    id: 'expression',
    label: '表現・曲',
    description: '旋律の歌い方・フレーズ。学んだ技術を曲の中で使う',
    minutes: {
      'mouthpiece': 15,
      'long_tone': 15,
      'lip_slur': 5,
      'arban_ornaments': 5,
      'arban_phrasing': 15,
      'arban_characteristic': 15,
    },
  ),
  MenuPreset(
    id: 'long',
    label: '長め（95分）',
    description: '時間がある日。基礎を維持しつつ、Arban を広めに',
    minutes: {
      'mouthpiece': 20,
      'long_tone': 15,
      'lip_slur': 10,
      'tonguing': 10,
      'arban_slurs': 10,
      'arban_scales': 10,
      'arban_tonguing': 10,
      'arban_phrasing': 10,
    },
  ),
];
