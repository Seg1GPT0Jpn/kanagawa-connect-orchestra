import 'package:flutter/material.dart';

import '../../../app/app_services.dart';
import '../../../core/clock.dart';
import '../../menu/domain/menu_audit.dart';
import '../domain/practice_record.dart';
import '../domain/practice_stats.dart';
import 'timer_page.dart';
import 'visible_records_builder.dart';

/// 今日のメニューと、練習の開始
class PracticeHomePage extends StatelessWidget {
  const PracticeHomePage({super.key});

  @override
  Widget build(BuildContext context) {
    final services = AppScope.of(context);
    final theme = Theme.of(context);
    return Scaffold(
      appBar: AppBar(title: const Text('練習')),
      body: VisibleRecordsBuilder(
        builder: (context, records) {
          final stats = computeStats(
            records,
            localDateString(services.clock()),
          );
          return ValueListenableBuilder<Map<String, int>>(
            valueListenable: services.menu,
            builder: (context, minutes, _) {
              final rules = services.menu.rules;
              final audit = auditMenu(minutes, rules);
              return ListView(
                padding: const EdgeInsets.all(16),
                children: [
                  Card(
                    child: Padding(
                      padding: const EdgeInsets.all(16),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.spaceAround,
                        children: [
                          _Stat(
                            label: '今日',
                            value: formatPracticeTime(stats.todaySeconds),
                          ),
                          _Stat(
                            label: '直近7日',
                            value: formatPracticeTime(stats.last7DaysSeconds),
                          ),
                          _Stat(label: '連続', value: '${stats.streakDays}日'),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(height: 16),
                  Text(rules.label, style: theme.textTheme.titleLarge),
                  const SizedBox(height: 8),
                  for (final item in rules.items)
                    ListTile(
                      dense: true,
                      title: Text(item.label),
                      trailing: Text(
                        minutes[item.id] == 0 ? 'お休み' : '${minutes[item.id]}分',
                        style: theme.textTheme.titleMedium,
                      ),
                    ),
                  const Divider(),
                  ListTile(
                    title: const Text('合計'),
                    trailing: Text(
                      '${audit.totalMinutes}分',
                      style: theme.textTheme.titleLarge,
                    ),
                  ),
                  const SizedBox(height: 16),
                  FilledButton.icon(
                    style: FilledButton.styleFrom(
                      minimumSize: const Size.fromHeight(56),
                    ),
                    onPressed: audit.isValid
                        ? () => _start(context, minutes)
                        : null,
                    icon: const Icon(Icons.play_arrow),
                    label: const Text('練習をはじめる'),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    'メニューは「メニュー」タブで変えられます',
                    style: theme.textTheme.bodySmall,
                    textAlign: TextAlign.center,
                  ),
                ],
              );
            },
          );
        },
      ),
    );
  }

  Future<void> _start(BuildContext context, Map<String, int> minutes) async {
    final messenger = ScaffoldMessenger.of(context);
    final saved = await Navigator.of(context).push<PracticeRecord>(
      MaterialPageRoute(builder: (_) => TimerPage(menu: minutes)),
    );
    if (saved != null) {
      messenger.showSnackBar(
        SnackBar(
          content: Text(
            '練習を記録しました（${formatPracticeTime(saved.totalActualSeconds)}）',
          ),
        ),
      );
    }
  }
}

class _Stat extends StatelessWidget {
  const _Stat({required this.label, required this.value});

  final String label;
  final String value;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Column(
      children: [
        Text(label, style: theme.textTheme.bodySmall),
        Text(value, style: theme.textTheme.headlineSmall),
      ],
    );
  }
}
