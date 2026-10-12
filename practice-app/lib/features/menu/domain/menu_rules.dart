/// 練習メニューの時間ルール（決定論的に検査する。AI の判断には依存しない）
library;

/// メニュー1項目の時間ルール（分）
class MenuItemRule {
  const MenuItemRule({
    required this.id,
    required this.label,
    required this.minMinutes,
    required this.maxMinutes,
    required this.defaultMinutes,
    this.group,
    this.description = '',
  }) : assert(0 <= minMinutes && minMinutes <= maxMinutes),
       assert(minMinutes <= defaultMinutes && defaultMinutes <= maxMinutes);

  /// 保存・AI とのやりとりに使うキー（英小文字）
  final String id;

  /// 画面に出す名前（グループに入る項目は、グループ名を除いた短い名前）
  final String label;
  final int minMinutes;
  final int maxMinutes;
  final int defaultMinutes;

  /// 所属するグループの id（例：arban）。null なら単独の項目
  final String? group;

  /// 何を鍛える練習か（画面に出す）
  final String description;
}

/// 複数の項目をまとめたグループの、合計時間のルール（例：Arban の各章の合計）
class MenuGroupRule {
  const MenuGroupRule({
    required this.id,
    required this.label,
    required this.minMinutes,
    required this.maxMinutes,
    this.description = '',
  }) : assert(0 <= minMinutes && minMinutes <= maxMinutes);

  final String id;
  final String label;
  final int minMinutes;
  final int maxMinutes;
  final String description;
}

/// メニュー全体のルール（項目ごとの範囲＋グループの合計＋全体の合計）
class MenuRuleSet {
  const MenuRuleSet({
    required this.id,
    required this.label,
    required this.items,
    required this.totalMinMinutes,
    required this.totalMaxMinutes,
    this.groups = const [],
    this.legacyLabels = const {},
  });

  final String id;
  final String label;

  /// 練習する順番に並べる
  final List<MenuItemRule> items;
  final List<MenuGroupRule> groups;
  final int totalMinMinutes;
  final int totalMaxMinutes;

  /// 以前のルールにあった項目の名前（古い練習記録の表示用）
  final Map<String, String> legacyLabels;

  MenuItemRule? itemById(String id) {
    for (final item in items) {
      if (item.id == id) return item;
    }
    return null;
  }

  MenuGroupRule? groupById(String id) {
    for (final g in groups) {
      if (g.id == id) return g;
    }
    return null;
  }

  List<MenuItemRule> itemsInGroup(String groupId) => [
    for (final i in items)
      if (i.group == groupId) i,
  ];

  /// 画面・記録に出す名前（グループの項目は「Arban：スラー」のように）
  String labelOf(String itemId) {
    final item = itemById(itemId);
    if (item == null) return legacyLabels[itemId] ?? itemId;
    final group = item.group == null ? null : groupById(item.group!);
    return group == null ? item.label : '${group.label}：${item.label}';
  }

  /// グループで実際に取れる合計の範囲（項目の範囲とグループの範囲の両方を満たす）
  (int, int) effectiveGroupRange(MenuGroupRule g) {
    final members = itemsInGroup(g.id);
    final sumMin = members.fold(0, (s, i) => s + i.minMinutes);
    final sumMax = members.fold(0, (s, i) => s + i.maxMinutes);
    return (
      sumMin > g.minMinutes ? sumMin : g.minMinutes,
      sumMax < g.maxMinutes ? sumMax : g.maxMinutes,
    );
  }

  /// 項目・グループの範囲を守ったまま、全体の合計の範囲にも収められるか
  bool get isSatisfiable {
    if (totalMinMinutes > totalMaxMinutes) return false;
    var lo = 0, hi = 0;
    for (final item in items.where(
      (i) => i.group == null || groupById(i.group!) == null,
    )) {
      lo += item.minMinutes;
      hi += item.maxMinutes;
    }
    for (final g in groups) {
      final (gLo, gHi) = effectiveGroupRange(g);
      if (gLo > gHi) return false;
      lo += gLo;
      hi += gHi;
    }
    return lo <= totalMaxMinutes && hi >= totalMinMinutes;
  }

  /// 初期値のメニュー（項目 id → 分）
  Map<String, int> get defaultMenu => {
    for (final item in items) item.id: item.defaultMinutes,
  };
}

/// トランペット基礎メニュー
///
/// 項目の範囲と合計（45〜115分）は指示書の仕様。Arban は 1893年 Goldman 編集版の分類で章ごとに分け、
/// その日に鍛えたい章を選んで吹く（0分＝お休み）。Arban の合計は 20〜40分。
const trumpetBasicRules = MenuRuleSet(
  id: 'trumpet_basic',
  label: 'トランペット基礎メニュー',
  items: [
    MenuItemRule(
      id: 'mouthpiece',
      label: 'マウスピース',
      minMinutes: 15,
      maxMinutes: 30,
      defaultMinutes: 20,
      description: '呼吸・バズィングで、楽に振動を始める',
    ),
    MenuItemRule(
      id: 'long_tone',
      label: 'ロングトーン',
      minMinutes: 10,
      maxMinutes: 20,
      defaultMinutes: 15,
      description: '音の立ち上がり・響き・終わり方、強弱と音程',
    ),
    MenuItemRule(
      id: 'lip_slur',
      label: 'リップスラー',
      minMinutes: 0,
      maxMinutes: 15,
      defaultMinutes: 5,
      description: '低〜中音域から。音が変わっても音色・音量を崩さない',
    ),
    MenuItemRule(
      id: 'tonguing',
      label: 'タンギング',
      minMinutes: 0,
      maxMinutes: 10,
      defaultMinutes: 5,
      description: '発音の明瞭さ。音の粒・音量・リズムをそろえる',
    ),
    ..._arbanItems,
  ],
  groups: [
    MenuGroupRule(
      id: 'arban',
      label: 'Arban',
      minMinutes: 20,
      maxMinutes: 40,
      description: '毎日全部ではなく、その日に鍛えたい章を選ぶ',
    ),
  ],
  totalMinMinutes: 45,
  totalMaxMinutes: 115,
  // 章ごとに分ける前は「arban」1項目だった
  legacyLabels: {'arban': 'Arban（アーバン）'},
);

/// Arban の章（1893年 E. F. Goldman 編集版の分類。版によって番号・収録数は異なる）
const _arbanItems = [
  MenuItemRule(
    id: 'arban_first_studies',
    label: '初歩練習',
    group: 'arban',
    minMinutes: 0,
    maxMinutes: 40,
    defaultMinutes: 0,
    description: 'First Studies：音の長さ・音程・運指、リズムと発音の連携',
  ),
  MenuItemRule(
    id: 'arban_syncopation',
    label: 'シンコペーション',
    group: 'arban',
    minMinutes: 0,
    maxMinutes: 40,
    defaultMinutes: 0,
    description: '拍の強弱、裏拍・拍をまたぐリズムを正確に',
  ),
  MenuItemRule(
    id: 'arban_slurs',
    label: 'スラー',
    group: 'arban',
    minMinutes: 0,
    maxMinutes: 40,
    defaultMinutes: 10,
    description: 'Slurring / Legato：息と唇の協調、滑らかな音のつながり',
  ),
  MenuItemRule(
    id: 'arban_scales',
    label: '音階',
    group: 'arban',
    minMinutes: 0,
    maxMinutes: 40,
    defaultMinutes: 10,
    description: '長音階・短音階：全調への対応、指の均一さ',
  ),
  MenuItemRule(
    id: 'arban_chromatic',
    label: '半音階',
    group: 'arban',
    minMinutes: 0,
    maxMinutes: 40,
    defaultMinutes: 0,
    description: '半音の動きを均一なリズム・音色で',
  ),
  MenuItemRule(
    id: 'arban_ornaments',
    label: '装飾音',
    group: 'arban',
    minMinutes: 0,
    maxMinutes: 40,
    defaultMinutes: 0,
    description: 'ターン・前打音・トリル・モルデントを旋律に自然に組み込む',
  ),
  MenuItemRule(
    id: 'arban_intervals',
    label: '音程・跳躍',
    group: 'arban',
    minMinutes: 0,
    maxMinutes: 40,
    defaultMinutes: 0,
    description: 'Intervals・分散和音：広い音程を正確に、和声の理解',
  ),
  MenuItemRule(
    id: 'arban_tonguing',
    label: 'タンギング',
    group: 'arban',
    minMinutes: 0,
    maxMinutes: 40,
    defaultMinutes: 10,
    description: 'シングル・ダブル・トリプル：速さより粒・アクセント・均一さ',
  ),
  MenuItemRule(
    id: 'arban_phrasing',
    label: 'フレージング（旋律）',
    group: 'arban',
    minMinutes: 0,
    maxMinutes: 40,
    defaultMinutes: 0,
    description: 'The Art of Phrasing：フレーズの山・呼吸位置・音の行き先',
  ),
  MenuItemRule(
    id: 'arban_duets',
    label: '二重奏',
    group: 'arban',
    minMinutes: 0,
    maxMinutes: 40,
    defaultMinutes: 0,
    description: '68 Duets：拍の共有、相手を聴く、音程・音色を合わせる',
  ),
  MenuItemRule(
    id: 'arban_characteristic',
    label: '性格的練習曲',
    group: 'arban',
    minMinutes: 0,
    maxMinutes: 40,
    defaultMinutes: 0,
    description: 'Characteristic Studies：学んだ技術を1曲の中でまとめて使う',
  ),
  MenuItemRule(
    id: 'arban_fantaisies',
    label: '幻想曲・変奏曲',
    group: 'arban',
    minMinutes: 0,
    maxMinutes: 40,
    defaultMinutes: 0,
    description: 'Fantaisies and Airs Variés：ソロ作品としての表現と技巧',
  ),
];
