import 'package:flutter_test/flutter_test.dart';
import 'package:kco_practice/features/menu/domain/menu_audit.dart';
import 'package:kco_practice/features/menu/domain/menu_rules.dart';

const rules = trumpetBasicRules;

Map<String, int> menu({
  int mouthpiece = 20,
  int longTone = 15,
  int lipSlur = 5,
  int tonguing = 5,
  int arban = 30,
}) => {
  'mouthpiece': mouthpiece,
  'long_tone': longTone,
  'lip_slur': lipSlur,
  'tonguing': tonguing,
  'arban': arban,
};

List<MenuViolationKind> kinds(MenuAuditResult r) =>
    r.violations.map((v) => v.kind).toList();

void main() {
  group('トランペット基礎メニューのルール', () {
    test('仕様どおりの範囲', () {
      final ranges = {
        for (final i in rules.items) i.id: [i.minMinutes, i.maxMinutes],
      };
      expect(ranges, {
        'mouthpiece': [15, 30],
        'long_tone': [10, 20],
        'lip_slur': [0, 15],
        'tonguing': [0, 10],
        'arban': [20, 40],
      });
      expect([rules.totalMinMinutes, rules.totalMaxMinutes], [45, 115]);
      expect(rules.isSatisfiable, isTrue);
    });

    test('初期値はルールを満たす', () {
      final r = auditMenu(rules.defaultMenu, rules);
      expect(r.isValid, isTrue);
      expect(r.totalMinutes, 75);
    });
  });

  group('auditMenu', () {
    test('すべて下限（合計45分）は有効', () {
      final r = auditMenu(
        menu(mouthpiece: 15, longTone: 10, lipSlur: 0, tonguing: 0, arban: 20),
        rules,
      );
      expect(r.isValid, isTrue);
      expect(r.totalMinutes, 45);
    });

    test('すべて上限（合計115分）は有効', () {
      final r = auditMenu(
        menu(
          mouthpiece: 30,
          longTone: 20,
          lipSlur: 15,
          tonguing: 10,
          arban: 40,
        ),
        rules,
      );
      expect(r.isValid, isTrue);
      expect(r.totalMinutes, 115);
    });

    test('リップスラー・タンギングは0分を許可', () {
      expect(auditMenu(menu(lipSlur: 0, tonguing: 0), rules).isValid, isTrue);
    });

    test('下限を1分下回ると違反', () {
      final r = auditMenu(menu(mouthpiece: 14), rules);
      expect(kinds(r), [MenuViolationKind.belowMinimum]);
      final v = r.violations.single;
      expect(
        [v.itemId, v.actualMinutes, v.minMinutes, v.maxMinutes],
        ['mouthpiece', 14, 15, 30],
      );
      expect(v.message, 'マウスピース：14分は短すぎます（15〜30分）');
    });

    test('上限を1分上回ると違反', () {
      final r = auditMenu(menu(arban: 41), rules);
      expect(kinds(r), [MenuViolationKind.aboveMaximum]);
      expect(r.violations.single.itemId, 'arban');
    });

    test('負の値は下限違反', () {
      expect(kinds(auditMenu(menu(tonguing: -1), rules)), [
        MenuViolationKind.belowMinimum,
      ]);
    });

    test('項目が足りない・ルールにない項目がある', () {
      final m = menu()..remove('arban');
      m['scale'] = 10;
      final r = auditMenu(m, rules);
      expect(kinds(r), [
        MenuViolationKind.missingItem,
        MenuViolationKind.unknownItem,
      ]);
      // ルールにない項目は合計に入れない（45分＝下限ちょうど）
      expect(r.totalMinutes, 45);
    });

    test('合計の下限・上限（項目の範囲が狭いルール）', () {
      const custom = MenuRuleSet(
        id: 'custom',
        label: 'テスト',
        items: [
          MenuItemRule(
            id: 'a',
            label: 'A',
            minMinutes: 0,
            maxMinutes: 60,
            defaultMinutes: 30,
          ),
          MenuItemRule(
            id: 'b',
            label: 'B',
            minMinutes: 0,
            maxMinutes: 60,
            defaultMinutes: 30,
          ),
        ],
        totalMinMinutes: 30,
        totalMaxMinutes: 90,
      );
      expect(kinds(auditMenu({'a': 10, 'b': 10}, custom)), [
        MenuViolationKind.totalBelowMinimum,
      ]);
      expect(kinds(auditMenu({'a': 60, 'b': 60}, custom)), [
        MenuViolationKind.totalAboveMaximum,
      ]);
      expect(auditMenu({'a': 45, 'b': 45}, custom).isValid, isTrue);
    });
  });

  group('suggestCorrection', () {
    test('違反がなければそのまま', () {
      expect(suggestCorrection(menu(), rules), menu());
    });

    test('範囲外の項目を範囲内に収め、ほかは変えない', () {
      expect(
        suggestCorrection(menu(mouthpiece: 5, arban: 60), rules),
        menu(mouthpiece: 15, arban: 40),
      );
    });

    test('ない項目は下限で補い、ルールにない項目は捨てる', () {
      final m = menu()..remove('long_tone');
      m['scale'] = 10;
      expect(suggestCorrection(m, rules), menu(longTone: 10));
    });

    const custom = MenuRuleSet(
      id: 'custom',
      label: 'テスト',
      items: [
        MenuItemRule(
          id: 'a',
          label: 'A',
          minMinutes: 0,
          maxMinutes: 40,
          defaultMinutes: 20,
        ),
        MenuItemRule(
          id: 'b',
          label: 'B',
          minMinutes: 0,
          maxMinutes: 40,
          defaultMinutes: 20,
        ),
      ],
      totalMinMinutes: 50,
      totalMaxMinutes: 60,
    );

    test('合計が足りなければ上の項目から増やす', () {
      expect(suggestCorrection({'a': 30, 'b': 0}, custom), {'a': 40, 'b': 10});
    });

    test('合計が多すぎれば下の項目から減らす', () {
      expect(suggestCorrection({'a': 40, 'b': 40}, custom), {'a': 40, 'b': 20});
    });

    test('どんな入力でも修正案はルールを満たす', () {
      for (final v in [-10, 0, 7, 25, 100]) {
        final m = menu(
          mouthpiece: v,
          longTone: v,
          lipSlur: v,
          tonguing: v,
          arban: v,
        );
        expect(auditMenu(suggestCorrection(m, rules), rules).isValid, isTrue);
        expect(auditMenu(suggestCorrection(m, custom), custom).isValid, isTrue);
      }
    });

    test('満たせないルールは StateError', () {
      const impossible = MenuRuleSet(
        id: 'x',
        label: 'X',
        items: [
          MenuItemRule(
            id: 'a',
            label: 'A',
            minMinutes: 0,
            maxMinutes: 10,
            defaultMinutes: 0,
          ),
        ],
        totalMinMinutes: 20,
        totalMaxMinutes: 30,
      );
      expect(impossible.isSatisfiable, isFalse);
      expect(() => suggestCorrection({'a': 5}, impossible), throwsStateError);
    });
  });
}
