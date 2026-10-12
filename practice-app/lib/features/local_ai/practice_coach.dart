/// AI コーチ：今日の調子と練習記録から、メニュー案とひとことアドバイスを AI に頼む
///
/// AI への指示文は決まった形で組み立て（テストできる）、AI の返事は
///  ・メニュー案：JSON として読み、プログラムの監査（menu_audit.dart）を通す。違反なら修正案を添える
///  ・アドバイス：長さを制限し、医療的な判断はしないよう指示する
/// AI の判断で時間のルールを決めることはない。
library;

import '../menu/domain/menu_proposal.dart';
import '../menu/domain/menu_rules.dart';
import '../practice/domain/day_condition.dart';
import '../practice/domain/practice_stats.dart';
import 'local_ai_service.dart';

const coachSystemInstruction =
    'あなたはトランペットの練習を手伝うコーチです。中高生にも分かるやさしい日本語で、短く答えます。'
    '体の痛みについて診断や医療的な判断はせず、痛みが続くときは指導者や医療機関に相談するよう伝えます。';

/// 今日の状態（AI に渡す材料）
class CoachContext {
  const CoachContext({
    required this.rules,
    required this.currentMenu,
    required this.condition,
    required this.stats,
  });

  final MenuRuleSet rules;
  final Map<String, int> currentMenu;
  final DayCondition condition;
  final PracticeStats stats;
}

String _conditionText(DayCondition c) {
  final parts = [
    if (c.rehearsal) '今日は合奏・レッスンがある',
    if (c.performance) '今日は本番がある',
    if (c.heavyYesterday) '昨日は高音・大音量をたくさん吹いた',
    if (c.lipPain) '唇が痛い',
    switch (c.fatigue) {
      Fatigue.fresh => '体調は元気',
      Fatigue.normal => '体調はふつう',
      Fatigue.tired => '疲れている',
    },
  ];
  return parts.join('、');
}

String _statsText(CoachContext ctx) {
  final s = ctx.stats;
  final byItem = [
    for (final MapEntry(:key, :value) in s.secondsByItemLast7.entries)
      if (value > 0) '${ctx.rules.labelOf(key)} ${value ~/ 60}分',
  ];
  return '直近7日の練習：合計${s.last7DaysSeconds ~/ 60}分、${s.daysPracticedLast7}日練習、${s.streakDays}日連続。'
      '項目別：${byItem.isEmpty ? 'まだ記録なし' : byItem.join('、')}';
}

/// メニュー案を頼む指示文（ルールの範囲をすべて書き、JSON だけで答えさせる）
String buildMenuPrompt(CoachContext ctx) {
  final r = ctx.rules;
  final lines = [
    for (final section in r.sections)
      if (section.item case final item?)
        '- ${item.id}（${item.label}）：${item.minMinutes}〜${item.maxMinutes}分'
      else ...[
        '- ${section.group!.label} の章（合計 ${section.group!.minMinutes}〜${section.group!.maxMinutes}分。その日に鍛えたい章を選び、ほかは 0）：',
        for (final m in section.members)
          '  - ${m.id}（${m.label}）：0〜${m.maxMinutes}分',
      ],
  ];
  return [
    '今日のトランペットの練習メニューを提案してください。',
    '今日の状態：${_conditionText(ctx.condition)}。',
    _statsText(ctx),
    '時間のルール（分。必ず守る）：',
    ...lines,
    '全体の合計：${r.totalMinMinutes}〜${r.totalMaxMinutes}分。',
    '直近7日で少なかった項目を少し増やし、多すぎた項目は休ませてください。',
    '答えは JSON だけにしてください。"menu" には、キーが上の英字の id、値が整数の分のオブジェクトを、'
        '"reason" には、なぜこのメニューにしたかを60文字以内の日本語で書きます。JSON の外に文章は書かないでください。',
    '例：{"menu": {"${r.items.first.id}": ${r.items.first.defaultMinutes}, ...}, "reason": "…"}',
  ].join('\n');
}

/// ひとことアドバイスを頼む指示文
String buildAdvicePrompt(CoachContext ctx) => [
  '今日の練習に向けて、ひとことアドバイスをください（100文字以内、2文まで）。',
  '今日の状態：${_conditionText(ctx.condition)}。',
  _statsText(ctx),
  '今日のメニュー：${[for (final e in ctx.currentMenu.entries)
    if (e.value > 0) '${ctx.rules.labelOf(e.key)} ${e.value}分'].join('、')}。',
].join('\n');

/// AI のアドバイスを表示用に整える（空白を詰め、長すぎれば切る）
String cleanAdvice(String raw, {int maxLength = 140}) {
  final text = raw.replaceAll(RegExp(r'\s+'), ' ').trim();
  return text.length <= maxLength ? text : '${text.substring(0, maxLength)}…';
}

class PracticeCoach {
  const PracticeCoach(this._ai);

  final LocalAiService _ai;

  /// AI にメニュー案を頼み、プログラムで検査した結果を返す
  Future<MenuProposalReview> suggestMenu(CoachContext ctx) async {
    final out = await _ai.generatePrompt(
      buildMenuPrompt(ctx),
      systemInstruction: coachSystemInstruction,
    );
    return reviewMenuProposal(out, ctx.rules, missingAsZero: true);
  }

  Future<String> advice(CoachContext ctx) async {
    final out = await _ai.generatePrompt(
      buildAdvicePrompt(ctx),
      systemInstruction: coachSystemInstruction,
    );
    final text = cleanAdvice(out);
    if (text.isEmpty) throw const LocalAiException('AI から返事がありませんでした');
    return text;
  }
}
