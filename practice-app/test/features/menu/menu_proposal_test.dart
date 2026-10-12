import 'package:flutter_test/flutter_test.dart';
import 'package:kco_practice/features/menu/domain/menu_audit.dart';
import 'package:kco_practice/features/menu/domain/menu_proposal.dart';
import 'package:kco_practice/features/menu/domain/menu_rules.dart';

import '../../menu_fixtures.dart';

void main() {
  final rules = trumpetBasicRules;

  test('前後に文章があっても JSON を読み取り、ルールを満たせば採用できる', () {
    final json =
        menu(lipSlur: 10, arban: {'arban_scales': 20, 'arban_phrasing': 10})
            .entries
            .map(
              (e) =>
                  '"${e.key}": ${e.key == 'arban_scales' ? '20.0' : e.value}',
            )
            .join(', ');
    final r = reviewMenuProposal('今日のおすすめです。\n{$json}\n無理せずに！', rules);
    expect(r.parseError, isNull);
    expect(r.minutes!['arban_scales'], 20);
    expect(r.isAcceptable, isTrue);
    expect(r.correction, isNull);
  });

  test('ルール違反の案は採用せず、修正案を添える', () {
    final json = menu(mouthpiece: 11).entries
        .map((e) => '"${e.key}": ${e.value}')
        .join(', ');
    final r = reviewMenuProposal('{$json}', rules);
    expect(r.isAcceptable, isFalse);
    expect(r.audit!.violations.single.kind, MenuViolationKind.aboveMaximum);
    expect(r.correction!['mouthpiece'], 10);
    expect(auditMenu(r.correction!, rules).isValid, isTrue);
  });

  test('以前の「arban」1項目の案は、章がないので採用しない', () {
    final r = reviewMenuProposal(
      '{"mouthpiece": 20, "long_tone": 15, "lip_slur": 5, "tonguing": 5, "arban": 30}',
      rules,
    );
    expect(r.isAcceptable, isFalse);
    expect(
      r.audit!.violations.map((v) => v.kind),
      contains(MenuViolationKind.unknownItem),
    );
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
