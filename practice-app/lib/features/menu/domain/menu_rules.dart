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
  }) : assert(0 <= minMinutes && minMinutes <= maxMinutes),
       assert(minMinutes <= defaultMinutes && defaultMinutes <= maxMinutes);

  /// 保存・AI とのやりとりに使うキー（英小文字）
  final String id;

  /// 画面に出す名前
  final String label;
  final int minMinutes;
  final int maxMinutes;
  final int defaultMinutes;
}

/// メニュー全体のルール（項目ごとの範囲＋合計時間の範囲）
class MenuRuleSet {
  const MenuRuleSet({
    required this.id,
    required this.label,
    required this.items,
    required this.totalMinMinutes,
    required this.totalMaxMinutes,
  });

  final String id;
  final String label;
  final List<MenuItemRule> items;
  final int totalMinMinutes;
  final int totalMaxMinutes;

  MenuItemRule? itemById(String id) {
    for (final item in items) {
      if (item.id == id) return item;
    }
    return null;
  }

  /// 項目ごとの範囲を守ったまま、合計の範囲にも収められるか
  bool get isSatisfiable {
    final sumMin = items.fold(0, (s, i) => s + i.minMinutes);
    final sumMax = items.fold(0, (s, i) => s + i.maxMinutes);
    return totalMinMinutes <= totalMaxMinutes &&
        sumMin <= totalMaxMinutes &&
        sumMax >= totalMinMinutes;
  }

  /// 初期値のメニュー（項目 id → 分）
  Map<String, int> get defaultMenu => {
    for (final item in items) item.id: item.defaultMinutes,
  };
}

/// トランペット基礎メニュー
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
    ),
    MenuItemRule(
      id: 'long_tone',
      label: 'ロングトーン',
      minMinutes: 10,
      maxMinutes: 20,
      defaultMinutes: 15,
    ),
    MenuItemRule(
      id: 'lip_slur',
      label: 'リップスラー',
      minMinutes: 0,
      maxMinutes: 15,
      defaultMinutes: 5,
    ),
    MenuItemRule(
      id: 'tonguing',
      label: 'タンギング',
      minMinutes: 0,
      maxMinutes: 10,
      defaultMinutes: 5,
    ),
    MenuItemRule(
      id: 'arban',
      label: 'Arban（アーバン）',
      minMinutes: 20,
      maxMinutes: 40,
      defaultMinutes: 30,
    ),
  ],
  totalMinMinutes: 45,
  totalMaxMinutes: 115,
);
