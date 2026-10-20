/// 練習メニューの決定論的監査と修正案
///
/// ユーザーの入力もローカル AI の提案も、必ずここを通してから採用する。
library;

import 'menu_rules.dart';

enum MenuViolationKind {
  /// ルールにある項目が入っていない
  missingItem,

  /// ルールにない項目が入っている
  unknownItem,
  belowMinimum,
  aboveMaximum,

  /// グループ（例：Arban の各章）の合計が範囲外
  groupBelowMinimum,
  groupAboveMaximum,
  totalBelowMinimum,
  totalAboveMaximum,
}

class MenuViolation {
  const MenuViolation({
    required this.kind,
    required this.message,
    this.itemId,
    this.groupId,
    this.actualMinutes,
    this.minMinutes,
    this.maxMinutes,
  });

  final MenuViolationKind kind;

  /// 合計時間・グループの違反では null
  final String? itemId;

  /// グループの違反のときだけ
  final String? groupId;
  final int? actualMinutes;
  final int? minMinutes;
  final int? maxMinutes;

  /// 画面に出す説明（日本語）
  final String message;

  @override
  String toString() => 'MenuViolation($kind, $itemId: $message)';
}

class MenuAuditResult {
  const MenuAuditResult({required this.totalMinutes, required this.violations});

  /// ルールにある項目だけの合計（分）
  final int totalMinutes;
  final List<MenuViolation> violations;

  bool get isValid => violations.isEmpty;
}

/// [minutes]（項目 id → 分）が [rules] を満たしているかを調べる
MenuAuditResult auditMenu(Map<String, int> minutes, MenuRuleSet rules) {
  final violations = <MenuViolation>[];
  var total = 0;

  for (final item in rules.items) {
    final value = minutes[item.id];
    final range = '${item.minMinutes}〜${item.maxMinutes}分';
    if (value == null) {
      violations.add(
        MenuViolation(
          kind: MenuViolationKind.missingItem,
          itemId: item.id,
          minMinutes: item.minMinutes,
          maxMinutes: item.maxMinutes,
          message: '${rules.labelOf(item.id)}の時間が入っていません（$range）',
        ),
      );
      continue;
    }
    total += value;
    if (value < item.minMinutes) {
      violations.add(
        MenuViolation(
          kind: MenuViolationKind.belowMinimum,
          itemId: item.id,
          actualMinutes: value,
          minMinutes: item.minMinutes,
          maxMinutes: item.maxMinutes,
          message: '${rules.labelOf(item.id)}：$value分は短すぎます（$range）',
        ),
      );
    } else if (value > item.maxMinutes) {
      violations.add(
        MenuViolation(
          kind: MenuViolationKind.aboveMaximum,
          itemId: item.id,
          actualMinutes: value,
          minMinutes: item.minMinutes,
          maxMinutes: item.maxMinutes,
          message: '${rules.labelOf(item.id)}：$value分は長すぎます（$range）',
        ),
      );
    }
  }

  for (final id in minutes.keys) {
    if (rules.itemById(id) == null) {
      violations.add(
        MenuViolation(
          kind: MenuViolationKind.unknownItem,
          itemId: id,
          actualMinutes: minutes[id],
          message: '「$id」は${rules.label}にない項目です',
        ),
      );
    }
  }

  for (final g in rules.groups) {
    final sum = rules
        .itemsInGroup(g.id)
        .fold(0, (s, i) => s + (minutes[i.id] ?? 0));
    final range = '${g.minMinutes}〜${g.maxMinutes}分';
    if (sum < g.minMinutes || sum > g.maxMinutes) {
      final below = sum < g.minMinutes;
      violations.add(
        MenuViolation(
          kind: below
              ? MenuViolationKind.groupBelowMinimum
              : MenuViolationKind.groupAboveMaximum,
          groupId: g.id,
          actualMinutes: sum,
          minMinutes: g.minMinutes,
          maxMinutes: g.maxMinutes,
          message: '${g.label}の合計$sum分は${below ? '短' : '長'}すぎます（$range）',
        ),
      );
    }
  }

  final totalRange = '${rules.totalMinMinutes}〜${rules.totalMaxMinutes}分';
  if (total < rules.totalMinMinutes) {
    violations.add(
      MenuViolation(
        kind: MenuViolationKind.totalBelowMinimum,
        actualMinutes: total,
        minMinutes: rules.totalMinMinutes,
        maxMinutes: rules.totalMaxMinutes,
        message: '合計$total分は短すぎます（$totalRange）',
      ),
    );
  } else if (total > rules.totalMaxMinutes) {
    violations.add(
      MenuViolation(
        kind: MenuViolationKind.totalAboveMaximum,
        actualMinutes: total,
        minMinutes: rules.totalMinMinutes,
        maxMinutes: rules.totalMaxMinutes,
        message: '合計$total分は長すぎます（$totalRange）',
      ),
    );
  }

  return MenuAuditResult(totalMinutes: total, violations: violations);
}

/// [minutes] をできるだけ保ったまま [rules] を満たすように直した修正案を返す
///
/// 1. ルールにない項目は捨て、ない項目は下限で補う
/// 2. 各項目を範囲内に収める
/// 3. グループ（Arban など）の合計が足りなければ上の項目から順に増やし、多すぎれば下の項目から減らす
/// 4. 全体の合計も同じように直す（項目・グループの範囲は守る）
///
/// 違反がなければ同じ内容を返す。[rules] が満たせないルールなら [StateError]。
Map<String, int> suggestCorrection(
  Map<String, int> minutes,
  MenuRuleSet rules,
) {
  if (!rules.isSatisfiable) {
    throw StateError('${rules.label}は満たせないルールです');
  }

  final result = <String, int>{
    for (final item in rules.items)
      item.id: (minutes[item.id] ?? item.minMinutes).clamp(
        item.minMinutes,
        item.maxMinutes,
      ),
  };
  int groupSum(String groupId) =>
      rules.itemsInGroup(groupId).fold(0, (s, i) => s + result[i.id]!);

  for (final g in rules.groups) {
    final members = rules.itemsInGroup(g.id);
    var sum = groupSum(g.id);
    if (sum < g.minMinutes) {
      for (final item in members) {
        final add = (g.minMinutes - sum).clamp(
          0,
          item.maxMinutes - result[item.id]!,
        );
        result[item.id] = result[item.id]! + add;
        sum += add;
      }
    } else if (sum > g.maxMinutes) {
      for (final item in members.reversed) {
        final remove = (sum - g.maxMinutes).clamp(
          0,
          result[item.id]! - item.minMinutes,
        );
        result[item.id] = result[item.id]! - remove;
        sum -= remove;
      }
    }
  }

  // グループの中の項目は、グループの範囲も超えない分だけ動かせる
  int headroom(MenuItemRule item) {
    final up = item.maxMinutes - result[item.id]!;
    final g = item.group == null ? null : rules.groupById(item.group!);
    return g == null ? up : up.clamp(0, g.maxMinutes - groupSum(g.id));
  }

  int slack(MenuItemRule item) {
    final down = result[item.id]! - item.minMinutes;
    final g = item.group == null ? null : rules.groupById(item.group!);
    return g == null ? down : down.clamp(0, groupSum(g.id) - g.minMinutes);
  }

  var total = result.values.fold(0, (s, v) => s + v);
  if (total < rules.totalMinMinutes) {
    for (final item in rules.items) {
      final add = (rules.totalMinMinutes - total).clamp(0, headroom(item));
      result[item.id] = result[item.id]! + add;
      total += add;
    }
  } else if (total > rules.totalMaxMinutes) {
    for (final item in rules.items.reversed) {
      final remove = (total - rules.totalMaxMinutes).clamp(0, slack(item));
      result[item.id] = result[item.id]! - remove;
      total -= remove;
    }
  }

  return result;
}
