import 'package:flutter_test/flutter_test.dart';
import 'package:kco_practice/features/menu/domain/menu_audit.dart';
import 'package:kco_practice/features/menu/domain/menu_proposal.dart';
import 'package:kco_practice/features/menu/domain/menu_rules.dart';
import 'package:kco_practice/features/menu/domain/rule_based_plan.dart';

import '../../menu_fixtures.dart';

void main() {
  final rules = trumpetBasicRules;

  test('記録が少ないうちは、今のメニューのまま', () {
    final p = planMenuByRules(
      rules: rules,
      currentMenu: menu(),
      secondsLast7: const {'long_tone': 300},
    );
    expect(p.minutes, menu());
    expect(p.reasons.single, contains('記録がまだ少ない'));
  });

  test('少なかった項目を増やし、多すぎた項目を減らす。Arban は吹いていない章と入れ替える。ルールは必ず守る', () {
    // ロングトーンばかり吹き、曲・エチュードはほとんど吹いていない
    final p = planMenuByRules(
      rules: rules,
      currentMenu: menu(),
      secondsLast7: const {
        'mouthpiece': 1500,
        'long_tone': 9000,
        'lip_slur': 1500,
        'tonguing': 1500,
        'repertoire': 300,
        'arban_slurs': 4000,
        'arban_scales': 1000,
        'arban_tonguing': 1000,
      },
    );
    expect(auditMenu(p.minutes, rules).isValid, isTrue);
    expect(p.minutes['repertoire'], 25);
    expect(p.minutes['long_tone'], 10);
    // いちばん吹いたスラーの章を、まだ吹いていない章（ルール順で最初）に
    expect(p.minutes['arban_slurs'], 0);
    final moved = arbanIds.firstWhere(
      (id) => !{'arban_slurs', 'arban_scales', 'arban_tonguing'}.contains(id),
    );
    expect(p.minutes[moved], 10);
    expect(p.reasons.join(), allOf(contains('曲・エチュード'), contains('スラー')));
    // 合計は変わらない
    expect(
      p.minutes.values.fold(0, (a, b) => a + b),
      menu().values.fold(0, (a, b) => a + b),
    );
  });

  test('バランスがよければ変えない', () {
    final m = menu();
    final p = planMenuByRules(
      rules: rules,
      currentMenu: m,
      secondsLast7: {
        for (final e in m.entries)
          if (e.value > 0) e.key: e.value * 60 * 5,
      },
    );
    expect(p.minutes, m);
    expect(p.reasons.single, contains('バランスはよい'));
  });

  test('AI の案：{"menu": …, "reason": …} の形を読み、理由を取り出す。前の形も読める', () {
    final m = menu();
    final body = m.entries.map((e) => '"${e.key}": ${e.value}').join(', ');
    final r = reviewMenuProposal(
      '{"menu": {$body}, "reason": "  ロングトーンを\\n中心に  "}',
      rules,
    );
    expect(r.isAcceptable, isTrue);
    expect(r.minutes, m);
    expect(r.reason, 'ロングトーンを 中心に');

    final flat = reviewMenuProposal('{$body, "reason": "理由"}', rules);
    expect(flat.isAcceptable, isTrue);
    expect(flat.reason, '理由');
    expect(reviewMenuProposal('{$body}', rules).reason, isNull);
  });
}
