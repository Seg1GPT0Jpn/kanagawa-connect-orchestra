import 'package:flutter_test/flutter_test.dart';
import 'package:kco_practice/features/practice/domain/practice_stats.dart';

import '../../helpers.dart';

void main() {
  test('記録がなければすべて0', () {
    final s = computeStats([], '2026-10-12');
    expect(
      [s.todaySeconds, s.last7DaysSeconds, s.daysPracticedLast7, s.streakDays],
      [0, 0, 0, 0],
    );
  });

  test('今日・直近7日・項目別・連続日数', () {
    final s = computeStats([
      record(
        'a',
        day: '2026-10-12',
        actual: {'mouthpiece': 600, 'arban': 1200},
      ),
      record('b', day: '2026-10-12', actual: {'mouthpiece': 300}),
      record('c', day: '2026-10-11', actual: {'mouthpiece': 600}),
      record('d', day: '2026-10-10', actual: {'arban': 60}),
      record('e', day: '2026-10-06', actual: {'arban': 60}), // 7日目（含む）
      record('f', day: '2026-10-05', actual: {'arban': 6000}), // 8日前（含まない）
      record(
        'g',
        day: '2026-10-09',
        actual: {'arban': 6000},
        deleted: true,
      ), // 削除済み
      record('h', day: '2026-10-09', actual: {'arban': 0}), // 0秒
    ], '2026-10-12');
    expect(s.todaySeconds, 2100);
    expect(s.last7DaysSeconds, 2100 + 600 + 60 + 60);
    expect(s.daysPracticedLast7, 4);
    expect(s.streakDays, 3); // 12・11・10日（9日は削除と0秒だけ）
    expect(s.secondsByItemLast7, {'mouthpiece': 1500, 'arban': 1320});
  });

  test('今日まだ練習していなければ、昨日までの連続日数', () {
    final s = computeStats([
      record('a', day: '2026-10-11'),
      record('b', day: '2026-10-10'),
    ], '2026-10-12');
    expect(s.streakDays, 2);
    expect(s.todaySeconds, 0);
  });

  test('月・年をまたいでも数えられる', () {
    final s = computeStats([
      record('a', day: '2027-01-01'),
      record('b', day: '2026-12-31'),
      record('c', day: '2026-12-30'),
    ], '2027-01-01');
    expect(s.streakDays, 3);
    expect(s.daysPracticedLast7, 3);
  });
}
