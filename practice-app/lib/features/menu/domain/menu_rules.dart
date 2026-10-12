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

/// 画面に並べる単位：単独の項目か、グループ（その中の項目）
class MenuSection {
  const MenuSection.item(MenuItemRule this.item)
    : group = null,
      members = const [];
  const MenuSection.group(MenuGroupRule this.group, this.members) : item = null;

  final MenuItemRule? item;
  final MenuGroupRule? group;
  final List<MenuItemRule> members;
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
    this.modeLabel = '',
    this.modeDescription = '',
  });

  final String id;
  final String label;

  /// 時間モードとしての短い名前（例：20分）と説明
  final String modeLabel;
  final String modeDescription;

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

  /// 練習する順番に、単独の項目とグループを並べる（グループは最初の項目の位置に出す）
  List<MenuSection> get sections {
    final result = <MenuSection>[];
    final seen = <String>{};
    for (final item in items) {
      final g = item.group == null ? null : groupById(item.group!);
      if (g == null) {
        result.add(MenuSection.item(item));
      } else if (seen.add(g.id)) {
        result.add(MenuSection.group(g, itemsInGroup(g.id)));
      }
    }
    return result;
  }

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

/// メニューの項目（時間モードごとに範囲だけが変わる）
class _ItemDef {
  const _ItemDef(this.id, this.label, this.description, {this.group});

  final String id;
  final String label;
  final String description;
  final String? group;
}

/// 練習する順番。id は記録にも残るので変えない（mouthpiece は「ウォームアップ」の項目）
const _defs = [
  _ItemDef('mouthpiece', 'ウォームアップ（呼吸・バズィング）', '呼吸・唇やマウスピースのバズィングで、楽に振動を始める'),
  _ItemDef('long_tone', 'ロングトーン', '音の立ち上がり・響き・終わり方、強弱と音程'),
  _ItemDef('lip_slur', 'リップスラー', '低〜中音域から。音が変わっても音色・音量を崩さない'),
  _ItemDef('tonguing', 'タンギング', '発音の明瞭さ。音の粒・音量・リズムをそろえる'),
  // Arban の章（1893年 E. F. Goldman 編集版の分類。版によって番号・収録数は異なる）
  _ItemDef(
    'arban_first_studies',
    '初歩練習',
    'First Studies：音の長さ・音程・運指、リズムと発音の連携',
    group: 'arban',
  ),
  _ItemDef(
    'arban_syncopation',
    'シンコペーション',
    '拍の強弱、裏拍・拍をまたぐリズムを正確に',
    group: 'arban',
  ),
  _ItemDef(
    'arban_slurs',
    'スラー',
    'Slurring / Legato：息と唇の協調、滑らかな音のつながり',
    group: 'arban',
  ),
  _ItemDef('arban_scales', '音階', '長音階・短音階：全調への対応、指の均一さ', group: 'arban'),
  _ItemDef('arban_chromatic', '半音階', '半音の動きを均一なリズム・音色で', group: 'arban'),
  _ItemDef(
    'arban_ornaments',
    '装飾音',
    'ターン・前打音・トリル・モルデントを旋律に自然に組み込む',
    group: 'arban',
  ),
  _ItemDef(
    'arban_intervals',
    '音程・跳躍',
    'Intervals・分散和音：広い音程を正確に、和声の理解',
    group: 'arban',
  ),
  _ItemDef(
    'arban_tonguing',
    'タンギング',
    'シングル・ダブル・トリプル：速さより粒・アクセント・均一さ',
    group: 'arban',
  ),
  _ItemDef(
    'arban_phrasing',
    'フレージング（旋律）',
    'The Art of Phrasing：フレーズの山・呼吸位置・音の行き先',
    group: 'arban',
  ),
  _ItemDef(
    'arban_duets',
    '二重奏',
    '68 Duets：拍の共有、相手を聴く、音程・音色を合わせる',
    group: 'arban',
  ),
  _ItemDef(
    'arban_characteristic',
    '性格的練習曲',
    'Characteristic Studies：学んだ技術を1曲の中でまとめて使う',
    group: 'arban',
  ),
  _ItemDef(
    'arban_fantaisies',
    '幻想曲・変奏曲',
    'Fantaisies and Airs Variés：ソロ作品としての表現と技巧',
    group: 'arban',
  ),
  _ItemDef('repertoire', '曲・エチュード', '合奏の楽譜・ソロ・エチュード。苦手な箇所を区切り、遅いテンポから'),
];

/// [ranges]：項目 id → (下限, 上限, 初期値)。Arban の章は [arbanChapter]（下限0）と [arbanDefaults] で決める
List<MenuItemRule> _buildItems({
  required Map<String, (int, int, int)> ranges,
  required int arbanChapterMax,
  required Map<String, int> arbanDefaults,
}) => [
  for (final d in _defs)
    MenuItemRule(
      id: d.id,
      label: d.label,
      description: d.description,
      group: d.group,
      minMinutes: d.group == null ? ranges[d.id]!.$1 : 0,
      maxMinutes: d.group == null ? ranges[d.id]!.$2 : arbanChapterMax,
      defaultMinutes: d.group == null
          ? ranges[d.id]!.$3
          : (arbanDefaults[d.id] ?? 0),
    ),
];

MenuGroupRule _arban(int min, int max) => MenuGroupRule(
  id: 'arban',
  label: 'Arban',
  minMinutes: min,
  maxMinutes: max,
  description: '毎日全部ではなく、その日に鍛えたい章を選ぶ',
);

/// 章ごとに分ける前は「arban」1項目だった（古い記録の表示用）
const _legacy = {'arban': 'Arban（アーバン）'};

/// トランペット基礎メニュー（通常：合計45〜115分）
///
/// 合計45〜115分・ロングトーン・リップスラー・タンギング・Arban（合計20〜40分）は指示書の仕様。
/// ウォームアップ（3〜10分）と曲・エチュード（0〜40分）は、プロ奏者の練習法の調査をもとに運営と決めた
/// （docs/practice-research.md）。
final trumpetBasicRules = MenuRuleSet(
  id: 'trumpet_basic',
  label: 'トランペット基礎メニュー',
  modeLabel: '通常',
  modeDescription: '合計45〜115分。基礎と曲をひととおり',
  items: _buildItems(
    ranges: {
      'mouthpiece': (3, 10, 5),
      'long_tone': (10, 20, 15),
      'lip_slur': (0, 15, 5),
      'tonguing': (0, 10, 5),
      'repertoire': (0, 40, 20),
    },
    arbanChapterMax: 40,
    arbanDefaults: {
      'arban_slurs': 10,
      'arban_scales': 10,
      'arban_tonguing': 10,
    },
  ),
  groups: [_arban(20, 40)],
  totalMinMinutes: 45,
  totalMaxMinutes: 115,
  legacyLabels: _legacy,
);

/// 20分モード（時間がない日・本番や合奏の前に整える）
final trumpet20Rules = MenuRuleSet(
  id: 'trumpet_20min',
  label: 'トランペット基礎メニュー（20分）',
  modeLabel: '20分',
  modeDescription: '合計15〜25分。時間がない日・本番や合奏の前に整える',
  items: _buildItems(
    ranges: {
      'mouthpiece': (2, 5, 3),
      'long_tone': (3, 10, 5),
      'lip_slur': (0, 5, 2),
      'tonguing': (0, 5, 0),
      'repertoire': (0, 15, 5),
    },
    arbanChapterMax: 15,
    arbanDefaults: {'arban_slurs': 5},
  ),
  groups: [_arban(0, 15)],
  totalMinMinutes: 15,
  totalMaxMinutes: 25,
  legacyLabels: _legacy,
);

/// 10分モード（とても短い日・疲れている日に、音を出して確かめるだけ）
final trumpet10Rules = MenuRuleSet(
  id: 'trumpet_10min',
  label: 'トランペット基礎メニュー（10分）',
  modeLabel: '10分',
  modeDescription: '合計5〜15分。とても短い日・疲れている日に、音を出して確かめるだけ',
  items: _buildItems(
    ranges: {
      'mouthpiece': (1, 3, 2),
      'long_tone': (2, 5, 3),
      'lip_slur': (0, 5, 2),
      'tonguing': (0, 3, 0),
      'repertoire': (0, 10, 3),
    },
    arbanChapterMax: 10,
    arbanDefaults: const {},
  ),
  groups: [_arban(0, 10)],
  totalMinMinutes: 5,
  totalMaxMinutes: 15,
  legacyLabels: _legacy,
);

/// 時間モード（選べる順）
final trumpetModes = [trumpetBasicRules, trumpet20Rules, trumpet10Rules];
