/// 練習記録の集計（決定論的。AI は使わない）
library;

import 'practice_record.dart';

class PracticeStats {
  const PracticeStats({
    required this.todaySeconds,
    required this.last7DaysSeconds,
    required this.daysPracticedLast7,
    required this.streakDays,
    required this.secondsByItemLast7,
  });

  final int todaySeconds;

  /// 今日を含む直近7日間
  final int last7DaysSeconds;
  final int daysPracticedLast7;

  /// 今日（今日まだなら昨日）から何日続けて練習しているか
  final int streakDays;
  final Map<String, int> secondsByItemLast7;
}

/// [today] は端末のローカル日付（yyyy-MM-dd）。削除済み・0秒の記録は数えない
PracticeStats computeStats(Iterable<PracticeRecord> records, String today) {
  final byDay = <String, int>{};
  final active = records
      .where((r) => !r.deleted && r.totalActualSeconds > 0)
      .toList();
  for (final r in active) {
    byDay[r.practicedOn] = (byDay[r.practicedOn] ?? 0) + r.totalActualSeconds;
  }

  final todayDate = _parse(today);
  final last7 = {
    for (var i = 0; i < 7; i++) _format(todayDate.subtract(Duration(days: i))),
  };

  final byItem = <String, int>{};
  for (final r in active.where((r) => last7.contains(r.practicedOn))) {
    for (final MapEntry(:key, :value) in r.actualSeconds.entries) {
      byItem[key] = (byItem[key] ?? 0) + value;
    }
  }

  var streak = 0;
  var day = byDay.containsKey(today)
      ? todayDate
      : todayDate.subtract(const Duration(days: 1));
  while (byDay.containsKey(_format(day))) {
    streak++;
    day = day.subtract(const Duration(days: 1));
  }

  return PracticeStats(
    todaySeconds: byDay[today] ?? 0,
    last7DaysSeconds: last7.fold(0, (s, d) => s + (byDay[d] ?? 0)),
    daysPracticedLast7: last7.where(byDay.containsKey).length,
    streakDays: streak,
    secondsByItemLast7: byItem,
  );
}

// 日付の計算は UTC で行う（夏時間などで1日が24時間でない地域でもずれないように）
DateTime _parse(String ymd) {
  final [y, m, d] = ymd.split('-').map(int.parse).toList();
  return DateTime.utc(y, m, d);
}

String _format(DateTime t) =>
    '${t.year.toString().padLeft(4, '0')}-${t.month.toString().padLeft(2, '0')}-${t.day.toString().padLeft(2, '0')}';

/// いちばん新しい記録の「次回の課題」（次の練習の目標の候補）。なければ null
String? latestNextFocus(Iterable<PracticeRecord> records) {
  PracticeRecord? latest;
  for (final r in records) {
    if (r.deleted || r.nextFocus.trim().isEmpty) continue;
    if (latest == null || r.startedAtMillis > latest.startedAtMillis) {
      latest = r;
    }
  }
  return latest?.nextFocus.trim();
}
