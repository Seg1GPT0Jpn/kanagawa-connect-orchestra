import 'package:flutter_test/flutter_test.dart';
import 'package:kco_practice/core/meta_store.dart';
import 'package:kco_practice/features/menu/domain/menu_presets.dart';
import 'package:kco_practice/features/menu/domain/menu_rules.dart';
import 'package:kco_practice/features/practice/data/day_condition_repository.dart';
import 'package:kco_practice/features/practice/domain/day_condition.dart';

import '../../helpers.dart';

void main() {
  group('adviseForDay', () {
    test('何もなければ、いつもどおり（モードは変えない）', () {
      final a = adviseForDay(const DayCondition());
      expect([a.rest, a.modeId, a.presetId], [false, null, null]);
      expect(
        adviseForDay(const DayCondition(fatigue: Fatigue.fresh)).modeId,
        isNull,
      );
    });

    test('唇が痛いときは、何があっても休む', () {
      final a = adviseForDay(
        const DayCondition(
          lipPain: true,
          performance: true,
          rehearsal: true,
          fatigue: Fatigue.tired,
        ),
      );
      expect(a.rest, isTrue);
      expect(a.modeId, isNull);
      expect(a.message, contains('休み'));
    });

    test('本番の日は20分', () {
      expect(
        adviseForDay(const DayCondition(performance: true)).modeId,
        'trumpet_20min',
      );
      expect(
        adviseForDay(const DayCondition(performance: true, rehearsal: true))
            .modeId,
        'trumpet_20min',
      );
    });

    test('疲れている日は20分、合奏もあれば10分', () {
      expect(
        adviseForDay(const DayCondition(fatigue: Fatigue.tired)).modeId,
        'trumpet_20min',
      );
      expect(
        adviseForDay(
          const DayCondition(fatigue: Fatigue.tired, rehearsal: true),
        ).modeId,
        'trumpet_10min',
      );
    });

    test('合奏・レッスンがある日は通常モードの「短め（45分）」', () {
      final a = adviseForDay(const DayCondition(rehearsal: true));
      expect([a.modeId, a.presetId], ['trumpet_basic', 'short']);
    });

    test('昨日たくさん吹いた日は「音色・柔軟性」', () {
      final a = adviseForDay(const DayCondition(heavyYesterday: true));
      expect([a.modeId, a.presetId], ['trumpet_basic', 'tone_flexibility']);
    });

    test('すすめるモード・おすすめは、どれも実在する', () {
      final modeIds = trumpetModes.map((m) => m.id).toSet();
      final presetIds = trumpetBasicPresets.map((p) => p.id).toSet();
      for (final rehearsal in [false, true]) {
        for (final performance in [false, true]) {
          for (final fatigue in Fatigue.values) {
            for (final lipPain in [false, true]) {
              for (final heavy in [false, true]) {
                final a = adviseForDay(
                  DayCondition(
                    rehearsal: rehearsal,
                    performance: performance,
                    fatigue: fatigue,
                    lipPain: lipPain,
                    heavyYesterday: heavy,
                  ),
                );
                expect(a.message, isNotEmpty);
                if (a.modeId != null) expect(modeIds, contains(a.modeId));
                if (a.presetId != null) {
                  expect(presetIds, contains(a.presetId));
                  expect(a.modeId, 'trumpet_basic'); // おすすめは通常モードのもの
                }
                if (a.rest) expect(a.modeId, isNull);
              }
            }
          }
        }
      }
    });
  });

  test('DayConditionRepository：日ごとに保存し、壊れた値は既定値で読む', () async {
    final meta = MetaStore(await openMemoryDb());
    final repo = DayConditionRepository(meta);
    expect(await repo.load('2026-10-12'), const DayCondition());

    const c = DayCondition(
      rehearsal: true,
      fatigue: Fatigue.tired,
      heavyYesterday: true,
    );
    await repo.save('2026-10-12', c);
    expect(await repo.load('2026-10-12'), c);
    expect(await repo.load('2026-10-13'), const DayCondition());

    await meta.put('condition.2026-10-14', {
      'fatigue': 'unknown',
      'lipPain': 'yes',
    });
    expect(await repo.load('2026-10-14'), const DayCondition());
  });

  test('おすすめには理由と避けたいことが付く。本番で疲れている日は10分', () {
    final perf = adviseForDay(
      const DayCondition(performance: true, fatigue: Fatigue.tired),
    );
    expect(perf.modeId, 'trumpet_10min');
    expect(perf.reasons.join(), allOf(contains('本番'), contains('疲れ')));
    expect(perf.avoid.join(), contains('新しい曲'));

    final pain = adviseForDay(
      const DayCondition(lipPain: true, performance: true),
    );
    expect(pain.rest, isTrue);
    expect(pain.message, contains('指導者'));
    expect(pain.avoid.single, contains('吹くこと'));

    final usual = adviseForDay(const DayCondition());
    expect(usual.reasons, isEmpty);
    expect(usual.avoid, isEmpty);
    expect(alwaysAdvice, contains('途中で終えて大丈夫'));
  });

  test('今日の目標は日ごとに保存し、読み込み後は待たずに使える', () async {
    final repo = DayConditionRepository(MetaStore(await openMemoryDb()));
    expect(repo.cachedGoal('2026-10-12'), '');
    await repo.saveGoal('2026-10-12', '音程を安定させる');
    expect(repo.cachedGoal('2026-10-12'), '音程を安定させる');
    expect(await repo.loadGoal('2026-10-12'), '音程を安定させる');
    expect(await repo.loadGoal('2026-10-13'), '');
  });
}
