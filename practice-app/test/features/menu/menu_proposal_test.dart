import 'package:flutter_test/flutter_test.dart';
import 'package:kco_practice/features/menu/domain/menu_audit.dart';
import 'package:kco_practice/features/menu/domain/menu_proposal.dart';
import 'package:kco_practice/features/menu/domain/menu_rules.dart';

void main() {
  const rules = trumpetBasicRules;

  test('前後に文章があっても JSON を読み取り、ルールを満たせば採用できる', () {
    final r = reviewMenuProposal(
      '今日のおすすめです。\n{"mouthpiece": 20, "long_tone": 15, "lip_slur": 10, '
      '"tonguing": 5, "arban": 30.0}\n無理せずに！',
      rules,
    );
    expect(r.parseError, isNull);
    expect(r.minutes!['arban'], 30);
    expect(r.isAcceptable, isTrue);
    expect(r.correction, isNull);
  });

  test('ルール違反の案は採用せず、修正案を添える', () {
    final r = reviewMenuProposal(
      '{"mouthpiece": 45, "long_tone": 15, "lip_slur": 5, "tonguing": 5, "arban": 30}',
      rules,
    );
    expect(r.isAcceptable, isFalse);
    expect(r.audit!.violations.single.kind, MenuViolationKind.aboveMaximum);
    expect(r.correction!['mouthpiece'], 30);
    expect(auditMenu(r.correction!, rules).isValid, isTrue);
  });

  test('読み取れない出力は採用しない', () {
    for (final out in [
      'マウスピース20分、ロングトーン15分がおすすめです',
      '{"mouthpiece": 20,',
      '[20, 15, 5, 5, 30]',
      '{"mouthpiece": "20分"}',
      '{"mouthpiece": 12.5}',
    ]) {
      final r = reviewMenuProposal(out, rules);
      expect(r.parseError, isNotNull, reason: out);
      expect(r.isAcceptable, isFalse, reason: out);
    }
  });
}
