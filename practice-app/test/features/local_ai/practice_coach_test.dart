import 'package:flutter_test/flutter_test.dart';
import 'package:kco_practice/features/local_ai/local_ai_service.dart';
import 'package:kco_practice/features/local_ai/practice_coach.dart';
import 'package:kco_practice/features/menu/domain/menu_audit.dart';
import 'package:kco_practice/features/menu/domain/menu_rules.dart';
import 'package:kco_practice/features/practice/domain/day_condition.dart';
import 'package:kco_practice/features/practice/domain/practice_stats.dart';

import '../../helpers.dart';

void main() {
  final rules = trumpetBasicRules;
  final ctx = CoachContext(
    rules: rules,
    currentMenu: rules.defaultMenu,
    condition: const DayCondition(rehearsal: true, fatigue: Fatigue.tired),
    stats: computeStats([
      record(
        'a',
        day: '2026-10-11',
        actual: {'long_tone': 900, 'arban_scales': 600},
      ),
    ], '2026-10-12'),
  );

  group('指示文', () {
    test('メニュー案：すべての項目の id と範囲、合計、JSON だけで答える指示', () {
      final p = buildMenuPrompt(ctx);
      for (final item in rules.items) {
        expect(p, contains(item.id), reason: item.id);
      }
      expect(p, contains('mouthpiece（ウォームアップ（呼吸・バズィング））：3〜10分'));
      expect(p, contains('Arban の章（合計 20〜40分'));
      expect(p, contains('全体の合計：45〜115分'));
      expect(p, contains('JSON だけ'));
      expect(p, contains('今日は合奏・レッスンがある'));
      expect(p, contains('疲れている'));
      expect(p, contains('ロングトーン 15分'));
      expect(p, contains('Arban：音階 10分'));
    });

    test('20分モードでは、そのモードの範囲を伝える', () {
      final p = buildMenuPrompt(
        CoachContext(
          rules: trumpet20Rules,
          currentMenu: trumpet20Rules.defaultMenu,
          condition: const DayCondition(),
          stats: ctx.stats,
        ),
      );
      expect(p, contains('全体の合計：15〜25分'));
      expect(p, contains('mouthpiece（ウォームアップ（呼吸・バズィング））：2〜5分'));
    });

    test('アドバイス：今日のメニューを含め、長さを指定する', () {
      final p = buildAdvicePrompt(ctx);
      expect(p, contains('100文字以内'));
      expect(p, contains('曲・エチュード 20分'));
    });

    test('アドバイスの整形：空白を詰め、長すぎれば切る', () {
      expect(cleanAdvice('  まずは\n\nロングトーン   から。 '), 'まずは ロングトーン から。');
      expect(cleanAdvice('あ' * 200), hasLength(141));
    });
  });

  group('PracticeCoach', () {
    late FakeLocalAiService ai;
    setUp(() async {
      ai = FakeLocalAiService();
      await ai.initializeModel();
    });

    test('ルールどおりの案（0分の章は省略）はそのまま使える', () async {
      ai.replies.add('''```json
{"mouthpiece": 5, "long_tone": 15, "lip_slur": 10, "tonguing": 5, "arban_slurs": 10, "arban_phrasing": 15, "repertoire": 20}
```''');
      final r = await PracticeCoach(ai).suggestMenu(ctx);
      expect(r.isAcceptable, isTrue);
      expect(r.minutes!['arban_duets'], 0); // 書かれていない章は0分
      expect(ai.systemInstructions.single, coachSystemInstruction);
    });

    test('ルール違反の案は使わず、アプリの修正案を添える', () async {
      ai.replies.add(
        '{"mouthpiece": 25, "long_tone": 15, "arban_scales": 50, "repertoire": 20}',
      );
      final r = await PracticeCoach(ai).suggestMenu(ctx);
      expect(r.isAcceptable, isFalse);
      expect(
        r.audit!.violations.map((v) => v.kind),
        containsAll([
          MenuViolationKind.aboveMaximum,
          MenuViolationKind.groupAboveMaximum,
        ]),
      );
      expect(auditMenu(r.correction!, rules).isValid, isTrue);
    });

    test('読み取れない答えは parseError', () async {
      ai.replies.add('今日はロングトーンを中心にしましょう！');
      final r = await PracticeCoach(ai).suggestMenu(ctx);
      expect(r.parseError, isNotNull);
      expect(r.isAcceptable, isFalse);
    });

    test('アドバイス：整えて返す。空の答えはエラー', () async {
      ai.replies.addAll(['  合奏の前なので、\n軽めに整えましょう。 ', '   ']);
      expect(await PracticeCoach(ai).advice(ctx), '合奏の前なので、 軽めに整えましょう。');
      await expectLater(
        PracticeCoach(ai).advice(ctx),
        throwsA(isA<LocalAiException>()),
      );
    });
  });

  test('UnavailableLocalAiService：使えない', () async {
    const ai = UnavailableLocalAiService();
    expect(await ai.probe(), LocalAiState.unavailable);
    expect(ai.isSupported, isFalse);
    await expectLater(ai.initializeModel(), throwsA(isA<LocalAiException>()));
  });
}
