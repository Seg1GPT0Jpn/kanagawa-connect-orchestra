import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import '../../../app/app_services.dart';
import '../../../core/clock.dart';
import '../data/usage_tracker.dart';
import '../domain/practice_record.dart';
import '../domain/practice_stats.dart';
import 'visible_records_builder.dart';

/// 練習のカレンダー（月ごと）。日を押すと、その日の練習と道具の時間
class CalendarPage extends StatefulWidget {
  const CalendarPage({super.key});

  @override
  State<CalendarPage> createState() => _CalendarPageState();
}

class _CalendarPageState extends State<CalendarPage> {
  late DateTime _month;
  String? _selected;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    final now = AppScope.of(context).clock();
    _month = DateTime(now.year, now.month);
  }

  @override
  Widget build(BuildContext context) {
    final services = AppScope.of(context);
    final theme = Theme.of(context);
    return Scaffold(
      appBar: AppBar(title: const Text('練習のカレンダー')),
      body: VisibleRecordsBuilder(
        builder: (context, records) {
          final byDay = minutesByDay(records);
          final today = localDateString(services.clock());
          final stats = computeStats(records, today);
          final goal = services.goals.goals.of(UsageKind.practice);
          final first = _month;
          final daysInMonth = DateTime(first.year, first.month + 1, 0).day;
          // 月曜はじまり
          final lead = (first.weekday + 6) % 7;
          final monthDays = [
            for (var d = 1; d <= daysInMonth; d++)
              localDateString(DateTime(first.year, first.month, d)),
          ];
          final monthMinutes = monthDays.fold(0, (a, d) => a + (byDay[d] ?? 0));
          final practiced = monthDays.where((d) => (byDay[d] ?? 0) > 0).length;
          final maxMin = byDay.values.fold(1, (a, b) => a > b ? a : b);
          return ListView(
            padding: const EdgeInsets.all(16),
            children: [
              Row(
                children: [
                  IconButton(
                    onPressed: () => setState(
                      () => _month = DateTime(_month.year, _month.month - 1),
                    ),
                    icon: const Icon(Icons.chevron_left),
                  ),
                  Expanded(
                    child: Text(
                      '${_month.year}年${_month.month}月',
                      textAlign: TextAlign.center,
                      style: theme.textTheme.titleLarge,
                    ),
                  ),
                  IconButton(
                    onPressed: () => setState(
                      () => _month = DateTime(_month.year, _month.month + 1),
                    ),
                    icon: const Icon(Icons.chevron_right),
                  ),
                ],
              ),
              Text(
                '$practiced日・${formatPracticeTime(monthMinutes * 60)}'
                '${goal > 0 ? '（目標 $goal分の日：${monthDays.where((d) => (byDay[d] ?? 0) >= goal).length}日）' : ''}',
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 8),
              Row(
                children: [
                  for (final w in const ['月', '火', '水', '木', '金', '土', '日'])
                    Expanded(
                      child: Text(
                        w,
                        textAlign: TextAlign.center,
                        style: theme.textTheme.labelSmall,
                      ),
                    ),
                ],
              ),
              GridView.count(
                crossAxisCount: 7,
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                children: [
                  for (var i = 0; i < lead; i++) const SizedBox.shrink(),
                  for (final (i, day) in monthDays.indexed)
                    _DayCell(
                      day: i + 1,
                      minutes: byDay[day] ?? 0,
                      intensity: (byDay[day] ?? 0) / maxMin,
                      goalMet: goal > 0 && (byDay[day] ?? 0) >= goal,
                      isToday: day == today,
                      selected: day == _selected,
                      onTap: () => setState(() => _selected = day),
                    ),
                ],
              ),
              const SizedBox(height: 8),
              OutlinedButton.icon(
                onPressed: () async {
                  final messenger = ScaffoldMessenger.of(context);
                  await Clipboard.setData(
                    ClipboardData(
                      text:
                          '練習お助け：${stats.streakDays}日連続で練習中！'
                          '（${_month.month}月は$practiced日・${formatPracticeTime(monthMinutes * 60)}）',
                    ),
                  );
                  messenger.showSnackBar(
                    const SnackBar(
                      content: Text('連続日数の文をコピーしました。メッセージなどに貼り付けて共有できます'),
                    ),
                  );
                },
                icon: const Icon(Icons.share_outlined),
                label: Text('${stats.streakDays}日連続を共有（文をコピー）'),
              ),
              if (_selected case final day?) ...[
                const Divider(height: 24),
                _DayDetail(
                  day: day,
                  records: [
                    for (final r in records)
                      if (r.practicedOn == day && !r.deleted) r,
                  ],
                ),
              ],
            ],
          );
        },
      ),
    );
  }
}

/// 日ごとの練習の分（削除済みは除く）
Map<String, int> minutesByDay(Iterable<PracticeRecord> records) {
  final m = <String, int>{};
  for (final r in records) {
    if (r.deleted) continue;
    m[r.practicedOn] = (m[r.practicedOn] ?? 0) + r.totalActualSeconds;
  }
  return {for (final e in m.entries) e.key: (e.value / 60).round()};
}

class _DayCell extends StatelessWidget {
  const _DayCell({
    required this.day,
    required this.minutes,
    required this.intensity,
    required this.goalMet,
    required this.isToday,
    required this.selected,
    required this.onTap,
  });

  final int day;
  final int minutes;
  final double intensity;
  final bool goalMet;
  final bool isToday;
  final bool selected;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Semantics(
      button: true,
      label: '$day日 $minutes分',
      child: InkWell(
        onTap: onTap,
        child: Container(
          margin: const EdgeInsets.all(2),
          decoration: BoxDecoration(
            color: minutes == 0
                ? null
                : Colors.green.withValues(alpha: 0.15 + 0.6 * intensity),
            border: Border.all(
              color: selected
                  ? theme.colorScheme.primary
                  : isToday
                  ? theme.colorScheme.outline
                  : Colors.transparent,
              width: selected ? 2 : 1,
            ),
            borderRadius: BorderRadius.circular(6),
          ),
          child: Stack(
            children: [
              Center(child: Text('$day')),
              if (minutes > 0)
                Positioned(
                  bottom: 2,
                  left: 0,
                  right: 0,
                  child: Text(
                    '$minutes分',
                    textAlign: TextAlign.center,
                    style: const TextStyle(fontSize: 9),
                  ),
                ),
              if (goalMet)
                const Positioned(
                  top: 2,
                  right: 2,
                  child: Icon(Icons.star, size: 10, color: Colors.amber),
                ),
            ],
          ),
        ),
      ),
    );
  }
}

class _DayDetail extends StatelessWidget {
  const _DayDetail({required this.day, required this.records});

  final String day;
  final List<PracticeRecord> records;

  @override
  Widget build(BuildContext context) {
    final services = AppScope.of(context);
    final theme = Theme.of(context);
    return FutureBuilder<Map<UsageKind, int>>(
      future: services.usage.secondsOn(day),
      builder: (context, snap) {
        final usage = snap.data ?? const {};
        return Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(day, style: theme.textTheme.titleMedium),
            if (records.isEmpty) const Text('練習の記録はありません'),
            for (final r in records)
              Text(
                '・${formatPracticeTime(r.totalActualSeconds)}'
                '${r.goal.isEmpty ? '' : '　目標：${r.goal}（${PracticeRecord.achievementLabels[r.achievement]}）'}',
              ),
            if (usage.isNotEmpty) ...[
              const SizedBox(height: 4),
              Text('道具を使った時間', style: theme.textTheme.titleSmall),
              for (final MapEntry(:key, :value) in usage.entries)
                if (key != UsageKind.practice)
                  Text('・${key.label} ${formatPracticeTime(value)}'),
            ],
          ],
        );
      },
    );
  }
}
