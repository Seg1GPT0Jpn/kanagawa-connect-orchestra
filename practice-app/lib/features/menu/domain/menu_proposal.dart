/// ローカル AI が出したメニュー案の読み取りと検査
///
/// AI の出力はそのまま信用しない。JSON として読めるか・値が整数の分か を確かめ、
/// さらに [auditMenu] でルールを検査する。違反があれば [suggestCorrection] の修正案を添える。
library;

import 'dart:convert';

import 'menu_audit.dart';
import 'menu_rules.dart';

class MenuProposalReview {
  const MenuProposalReview._({
    this.minutes,
    this.parseError,
    this.audit,
    this.correction,
  });

  /// AI が提案したメニュー（読み取れなかったときは null）
  final Map<String, int>? minutes;

  /// 読み取れなかった理由（日本語）
  final String? parseError;
  final MenuAuditResult? audit;

  /// 違反があったときのプログラム側の修正案
  final Map<String, int>? correction;

  /// そのまま採用してよいか
  bool get isAcceptable => audit?.isValid ?? false;
}

/// AI の出力テキストから最初の JSON オブジェクト（`{"mouthpiece": 20, ...}`）を取り出して検査する
///
/// [missingAsZero] が true なら、書かれていない項目は 0 分とみなす（AI は 0 分の章を省きがちなため）。
MenuProposalReview reviewMenuProposal(
  String aiOutput,
  MenuRuleSet rules, {
  bool missingAsZero = false,
}) {
  final start = aiOutput.indexOf('{');
  final end = aiOutput.lastIndexOf('}');
  if (start < 0 || end < start) {
    return const MenuProposalReview._(parseError: 'メニュー案（JSON）が見つかりません');
  }

  final Object? decoded;
  try {
    decoded = jsonDecode(aiOutput.substring(start, end + 1));
  } on FormatException {
    return const MenuProposalReview._(parseError: 'メニュー案（JSON）の形式が正しくありません');
  }
  if (decoded is! Map<String, dynamic>) {
    return const MenuProposalReview._(parseError: 'メニュー案は「項目: 分」の形で出してください');
  }

  final minutes = <String, int>{};
  for (final MapEntry(:key, :value) in decoded.entries) {
    if (value is int) {
      minutes[key] = value;
    } else if (value is double && value == value.truncateToDouble()) {
      minutes[key] = value.toInt();
    } else {
      return MenuProposalReview._(parseError: '「$key」の時間が整数の分ではありません');
    }
  }

  if (missingAsZero) {
    for (final item in rules.items) {
      minutes.putIfAbsent(item.id, () => 0);
    }
  }

  final audit = auditMenu(minutes, rules);
  return MenuProposalReview._(
    minutes: minutes,
    audit: audit,
    correction: audit.isValid ? null : suggestCorrection(minutes, rules),
  );
}
