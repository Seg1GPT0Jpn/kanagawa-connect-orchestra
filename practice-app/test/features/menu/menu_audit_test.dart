import 'package:flutter_test/flutter_test.dart';
import 'package:kco_practice/features/menu/domain/menu_audit.dart';
import 'package:kco_practice/features/menu/domain/menu_presets.dart';
import 'package:kco_practice/features/menu/domain/menu_rules.dart';

import '../../menu_fixtures.dart';

const rules = trumpetBasicRules;

List<MenuViolationKind> kinds(MenuAuditResult r) =>
    r.violations.map((v) => v.kind).toList();

int arbanSum(Map<String, int> m) => arbanIds.fold(0, (s, id) => s + m[id]!);

void main() {
  group('トランペット基礎メニューのルール', () {
    test('仕様どおりの範囲（Arban は章ごと、合計20〜40分）', () {
      final ranges = {
        for (final i in rules.items.where((i) => i.group == null))
          i.id: [i.minMinutes, i.maxMinutes],
      };
      expect(ranges, {
        'mouthpiece': [15, 30],
        'long_tone': [10, 20],
        'lip_slur': [0, 15],
        'tonguing': [0, 10],
      });
      final arban = rules.groupById('arban')!;
      expect([arban.minMinutes, arban.maxMinutes], [20, 40]);
      expect([rules.totalMinMinutes, rules.totalMaxMinutes], [45, 115]);
      expect(rules.isSatisfiable, isTrue);
    });

    test('Arban は 1893年版の12の章', () {
      expect(arbanIds, [
        'arban_first_studies',
        'arban_syncopation',
        'arban_slurs',
        'arban_scales',
        'arban_chromatic',
        'arban_ornaments',
        'arban_intervals',
        'arban_tonguing',
        'arban_phrasing',
        'arban_duets',
        'arban_characteristic',
        'arban_fantaisies',
      ]);
      for (final i in rules.itemsInGroup('arban')) {
        expect([i.minMinutes, i.maxMinutes], [0, 40], reason: i.id);
        expect(i.description, isNotEmpty, reason: i.id);
      }
    });

    test('名前：Arban の章は「Arban：章名」、以前の arban 項目も読める', () {
      expect(rules.labelOf('mouthpiece'), 'マウスピース');
      expect(rules.labelOf('arban_slurs'), 'Arban：スラー');
      expect(rules.labelOf('arban'), 'Arban（アーバン）');
      expect(rules.labelOf('unknown'), 'unknown');
    });

    test('初期値はルールを満たす（合計75分・Arban 30分）', () {
      final r = auditMenu(rules.defaultMenu, rules);
      expect(r.isValid, isTrue);
      expect(r.totalMinutes, 75);
      expect(arbanSum(rules.defaultMenu), 30);
    });
  });

  group('auditMenu', () {
    test('すべて下限（合計45分・Arban 20分）は有効', () {
      final r = auditMenu(
        menu(
          mouthpiece: 15,
          longTone: 10,
          lipSlur: 0,
          tonguing: 0,
          arban: {'arban_scales': 20},
        ),
        rules,
      );
      expect(r.isValid, isTrue);
      expect(r.totalMinutes, 45);
    });

    test('すべて上限（合計115分・Arban 40分）は有効', () {
      final r = auditMenu(
        menu(
          mouthpiece: 30,
          longTone: 20,
          lipSlur: 15,
          tonguing: 10,
          arban: {'arban_slurs': 20, 'arban_tonguing': 20},
        ),
        rules,
      );
      expect(r.isValid, isTrue);
      expect(r.totalMinutes, 115);
    });

    test('リップスラー・タンギング・Arban の各章は0分を許可', () {
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
      final r = auditMenu(menu(longTone: 21), rules);
      expect(kinds(r), [MenuViolationKind.aboveMaximum]);
      expect(r.violations.single.itemId, 'long_tone');
    });

    test('負の値は下限違反', () {
      expect(kinds(auditMenu(menu(tonguing: -1), rules)), [
        MenuViolationKind.belowMinimum,
      ]);
    });

    test('Arban の合計が20分未満・40分超は違反', () {
      final below = auditMenu(
        menu(arban: {'arban_slurs': 10, 'arban_scales': 9}),
        rules,
      );
      expect(kinds(below), [MenuViolationKind.groupBelowMinimum]);
      final v = below.violations.single;
      expect(
        [v.groupId, v.actualMinutes, v.minMinutes, v.maxMinutes],
        ['arban', 19, 20, 40],
      );
      expect(v.message, 'Arbanの合計19分は短すぎます（20〜40分）');

      final above = auditMenu(
        menu(arban: {'arban_slurs': 21, 'arban_scales': 20}),
        rules,
      );
      expect(kinds(above), [MenuViolationKind.groupAboveMaximum]);
      expect(above.violations.single.message, 'Arbanの合計41分は長すぎます（20〜40分）');
    });

    test('Arban の章の範囲外（41分）は章とグループの両方で違反', () {
      final r = auditMenu(menu(arban: {'arban_phrasing': 41}), rules);
      expect(kinds(r), [
        MenuViolationKind.aboveMaximum,
        MenuViolationKind.groupAboveMaximum,
      ]);
      expect(r.violations.first.message, 'Arban：フレージング（旋律）：41分は長すぎます（0〜40分）');
    });

    test('項目が足りない・ルールにない項目（以前の arban）がある', () {
      final m = menu()..remove('long_tone');
      m['arban'] = 30;
      final r = auditMenu(m, rules);
      expect(kinds(r), [
        MenuViolationKind.missingItem,
        MenuViolationKind.unknownItem,
      ]);
      // ルールにない項目は合計に入れない
      expect(r.totalMinutes, 60);
    });

    test('合計の下限・上限（項目の範囲が広いルール）', () {
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
        suggestCorrection(menu(mouthpiece: 5, longTone: 60), rules),
        menu(mouthpiece: 15, longTone: 20),
      );
    });

    test('ない項目は下限で補い、ルールにない項目は捨てる', () {
      final m = menu()..remove('long_tone');
      m['arban'] = 30;
      expect(suggestCorrection(m, rules), menu(longTone: 10));
    });

    test('Arban が足りなければ上の章から増やし、多すぎれば下の章から減らす', () {
      expect(
        suggestCorrection(menu(arban: {'arban_scales': 5}), rules),
        menu(arban: {'arban_first_studies': 15, 'arban_scales': 5}),
      );
      expect(
        suggestCorrection(
          menu(arban: {'arban_slurs': 30, 'arban_phrasing': 30}),
          rules,
        ),
        menu(arban: {'arban_slurs': 30, 'arban_phrasing': 10}),
      );
    });

    const grouped = MenuRuleSet(
      id: 'grouped',
      label: 'テスト',
      items: [
        MenuItemRule(
          id: 'a',
          label: 'A',
          minMinutes: 0,
          maxMinutes: 30,
          defaultMinutes: 0,
        ),
        MenuItemRule(
          id: 'g1',
          label: 'G1',
          group: 'g',
          minMinutes: 0,
          maxMinutes: 30,
          defaultMinutes: 10,
        ),
        MenuItemRule(
          id: 'g2',
          label: 'G2',
          group: 'g',
          minMinutes: 0,
          maxMinutes: 30,
          defaultMinutes: 10,
        ),
      ],
      groups: [
        MenuGroupRule(id: 'g', label: 'G', minMinutes: 10, maxMinutes: 20),
      ],
      totalMinMinutes: 45,
      totalMaxMinutes: 48,
    );

    test('全体の合計を直すときも、グループの範囲は超えない', () {
      // a を上限（30）まで増やし、足りない5分をグループ（上限20）の空きから
      final up = suggestCorrection({'a': 0, 'g1': 5, 'g2': 5}, grouped);
      expect(up, {'a': 30, 'g1': 10, 'g2': 5});
      // 下の項目から減らす（グループの下限10は守る）
      final down = suggestCorrection({'a': 30, 'g1': 10, 'g2': 10}, grouped);
      expect(down, {'a': 30, 'g1': 10, 'g2': 8});
      // グループが上限なら、グループの外の項目だけを増やす
      final full = suggestCorrection({'a': 0, 'g1': 20, 'g2': 0}, grouped);
      expect(full, {'a': 25, 'g1': 20, 'g2': 0});
    });

    test('どんな入力でも修正案はルールを満たす', () {
      for (final v in [-10, 0, 3, 7, 25, 41, 100]) {
        final m = {for (final i in rules.items) i.id: v};
        expect(
          auditMenu(suggestCorrection(m, rules), rules).isValid,
          isTrue,
          reason: '$v',
        );
        final g = {for (final i in grouped.items) i.id: v};
        expect(
          auditMenu(suggestCorrection(g, grouped), grouped).isValid,
          isTrue,
          reason: '$v',
        );
      }
      // 章ごとに違う値
      for (var seed = 0; seed < 50; seed++) {
        final m = {
          for (final (k, i) in rules.items.indexed)
            i.id: (seed * 7 + k * 13) % 45 - 3,
        };
        expect(
          auditMenu(suggestCorrection(m, rules), rules).isValid,
          isTrue,
          reason: '$m',
        );
      }
    });

    test('満たせないルールは StateError（グループの下限が章の上限の合計より大きい場合も）', () {
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

      const badGroup = MenuRuleSet(
        id: 'y',
        label: 'Y',
        items: [
          MenuItemRule(
            id: 'g1',
            label: 'G1',
            group: 'g',
            minMinutes: 0,
            maxMinutes: 5,
            defaultMinutes: 0,
          ),
        ],
        groups: [
          MenuGroupRule(id: 'g', label: 'G', minMinutes: 10, maxMinutes: 20),
        ],
        totalMinMinutes: 0,
        totalMaxMinutes: 100,
      );
      expect(badGroup.isSatisfiable, isFalse);
    });
  });

  group('今日の重点（おすすめ）', () {
    test('どの案もルールを満たし、ルールにない項目を使っていない', () {
      expect(trumpetBasicPresets, isNotEmpty);
      for (final p in trumpetBasicPresets) {
        for (final id in p.minutes.keys) {
          expect(rules.itemById(id), isNotNull, reason: '${p.id}: $id');
        }
        final m = p.menuFor(rules.items.map((i) => i.id));
        final audit = auditMenu(m, rules);
        expect(audit.violations, isEmpty, reason: p.id);
        expect(p.description, isNotEmpty);
      }
    });

    test('id は重複しない・「バランス」は初期値と同じ', () {
      expect(
        trumpetBasicPresets.map((p) => p.id).toSet(),
        hasLength(trumpetBasicPresets.length),
      );
      final balanced = trumpetBasicPresets.firstWhere(
        (p) => p.id == 'balanced',
      );
      expect(balanced.menuFor(rules.items.map((i) => i.id)), rules.defaultMenu);
    });

    test('「短め」は合計45分、「長め」は95分', () {
      int total(String id) => trumpetBasicPresets
          .firstWhere((p) => p.id == id)
          .minutes
          .values
          .fold(0, (s, v) => s + v);
      expect(total('short'), 45);
      expect(total('long'), 95);
    });
  });
}
