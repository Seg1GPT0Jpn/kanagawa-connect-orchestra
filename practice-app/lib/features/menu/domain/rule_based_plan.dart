/// AI を使わない、ルールによるメニューの提案（決定論的）
///
/// 直近7日の練習の偏りを見て、今のメニューを少しだけ調整する：
///  ・メニューの割合に比べて少なかった項目を 5 分増やし、多すぎた項目を 5 分減らす（それぞれ2つまで）
///  ・Arban は、ほかより目立って多く吹いた章を、7日間吹いていない章と入れ替える
/// 調整した結果は必ず [auditMenu] に通し、合わなければ [suggestCorrection] で直す。
library;

import 'menu_audit.dart';
import 'menu_rules.dart';

class RuleBasedPlan {
  const RuleBasedPlan({required this.minutes, required this.reasons});

  final Map<String, int> minutes;

  /// なぜこう変えたか（画面に出す）
  final List<String> reasons;
}

RuleBasedPlan planMenuByRules({
  required MenuRuleSet rules,
  required Map<String, int> currentMenu,
  required Map<String, int> secondsLast7,
  int step = 5,
}) {
  final menu = {
    for (final item in rules.items) item.id: currentMenu[item.id] ?? 0,
  };
  final reasons = <String>[];
  final practicedTotal = secondsLast7.values.fold(0, (a, b) => a + b);
  if (practicedTotal < 15 * 60) {
    return RuleBasedPlan(
      minutes: _valid(menu, rules),
      reasons: const ['直近7日の記録がまだ少ないので、今のメニューのままがおすすめです'],
    );
  }

  // 単独の項目：メニューでの割合と、実際に吹いた割合を比べる
  final singles = [
    for (final item in rules.items)
      if (item.group == null && (menu[item.id] ?? 0) > 0) item,
  ];
  final plannedTotal = singles.fold(0, (a, i) => a + menu[i.id]!);
  final ratio = <String, double>{
    for (final i in singles)
      i.id:
          ((secondsLast7[i.id] ?? 0) / practicedTotal) /
          (menu[i.id]! / plannedTotal),
  };
  final under = [
    for (final i in singles)
      if (ratio[i.id]! < 0.5 && menu[i.id]! + step <= i.maxMinutes) i,
  ]..sort((a, b) => ratio[a.id]!.compareTo(ratio[b.id]!));
  final over = [
    for (final i in singles)
      if (ratio[i.id]! > 1.5 && menu[i.id]! - step >= i.minMinutes) i,
  ]..sort((a, b) => ratio[b.id]!.compareTo(ratio[a.id]!));
  final n = [under.length, over.length, 2].reduce((a, b) => a < b ? a : b);
  for (var k = 0; k < n; k++) {
    final up = under[k], down = over[k];
    menu[up.id] = menu[up.id]! + step;
    menu[down.id] = menu[down.id]! - step;
    reasons.add(
      '${up.label}が直近7日で少なめだったので +$step分、'
      '${down.label}は多めだったので -$step分',
    );
  }

  // グループ（Arban）：吹いていない章と、いちばん多く吹いた章を入れ替える
  for (final g in rules.groups) {
    final members = rules.itemsInGroup(g.id);
    final inMenu = [
      for (final m in members)
        if ((menu[m.id] ?? 0) > 0) m,
    ];
    final unused = [
      for (final m in members)
        if ((menu[m.id] ?? 0) == 0 && (secondsLast7[m.id] ?? 0) == 0) m,
    ];
    if (inMenu.isEmpty || unused.isEmpty) continue;
    inMenu.sort(
      (a, b) => (secondsLast7[b.id] ?? 0).compareTo(secondsLast7[a.id] ?? 0),
    );
    final most = inMenu.first;
    // ほかの章より目立って多く吹いているときだけ入れ替える
    final average =
        inMenu.fold(0, (a, m) => a + (secondsLast7[m.id] ?? 0)) / inMenu.length;
    final mostSeconds = secondsLast7[most.id] ?? 0;
    if (mostSeconds == 0 || mostSeconds < average * 1.3) continue;
    final next = unused.first;
    final mins = menu[most.id]!.clamp(0, next.maxMinutes);
    menu[next.id] = mins;
    menu[most.id] = menu[most.id]! - mins;
    reasons.add(
      '${g.label}：「${most.label}」は直近7日でよく吹いたので、今日は吹いていない「${next.label}」に',
    );
  }

  if (reasons.isEmpty) {
    reasons.add('直近7日のバランスはよいので、今のメニューのままで大丈夫です');
  }
  return RuleBasedPlan(minutes: _valid(menu, rules), reasons: reasons);
}

Map<String, int> _valid(Map<String, int> menu, MenuRuleSet rules) =>
    auditMenu(menu, rules).isValid ? menu : suggestCorrection(menu, rules);
