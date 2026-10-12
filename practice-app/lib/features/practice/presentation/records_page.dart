import 'package:flutter/material.dart';

import '../../../app/app_services.dart';
import '../../../core/clock.dart';
import '../domain/practice_record.dart';
import '../domain/practice_stats.dart';
import '../../data_io/data_menu_button.dart';
import 'reflection_page.dart';
import 'visible_records_builder.dart';

/// 練習記録の一覧と集計
class RecordsPage extends StatelessWidget {
  const RecordsPage({super.key});

  @override
  Widget build(BuildContext context) {
    final services = AppScope.of(context);
    final theme = Theme.of(context);
    return Scaffold(
      appBar: AppBar(
        title: const Text('記録'),
        actions: const [DataMenuButton()],
      ),
      body: VisibleRecordsBuilder(
        builder: (context, records) {
          if (records.isEmpty) {
            return const Center(
              child: Text(
                'まだ記録がありません。\n「練習」タブから練習をはじめましょう。',
                textAlign: TextAlign.center,
              ),
            );
          }
          final stats = computeStats(
            records,
            localDateString(services.clock()),
          );
          final rules = services.menu.rules;
          return ListView(
            padding: const EdgeInsets.symmetric(vertical: 8),
            children: [
              Card(
                margin: const EdgeInsets.all(16),
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('直近7日間', style: theme.textTheme.titleMedium),
                      const SizedBox(height: 4),
                      Text(
                        '${formatPracticeTime(stats.last7DaysSeconds)}・${stats.daysPracticedLast7}日練習・${stats.streakDays}日連続',
                        style: theme.textTheme.bodyLarge,
                      ),
                      const SizedBox(height: 8),
                      for (final MapEntry(:key, :value)
                          in stats.secondsByItemLast7.entries)
                        if (value > 0)
                          Text(
                            '${rules.labelOf(key)}：${formatPracticeTime(value)}',
                            style: theme.textTheme.bodySmall,
                          ),
                    ],
                  ),
                ),
              ),
              for (final r in records)
                ListTile(
                  title: Text(
                    '${r.practicedOn}　${formatPracticeTime(r.totalActualSeconds)}',
                  ),
                  subtitle: Text(
                    [
                      for (final MapEntry(:key, :value)
                          in r.actualSeconds.entries)
                        if (value > 0)
                          '${rules.labelOf(key)} ${formatPracticeTime(value)}',
                      if (r.goal.isNotEmpty)
                        '🎯 ${r.goal}${r.achievement == 0 ? '' : '（${PracticeRecord.achievementLabels[r.achievement]}）'}',
                      if (r.note.isNotEmpty) '📝 ${r.note}',
                      if (r.nextFocus.isNotEmpty) '➡ 次回：${r.nextFocus}',
                    ].join('・'),
                  ),
                  onTap: () => _showDetail(context, r),
                ),
            ],
          );
        },
      ),
    );
  }

  Future<void> _showDetail(BuildContext context, PracticeRecord r) {
    final services = AppScope.of(context);
    final rules = services.menu.rules;
    final note = TextEditingController(text: r.note);
    return showModalBottomSheet<void>(
      context: context,
      isScrollControlled: true,
      builder: (context) => Padding(
        padding: EdgeInsets.fromLTRB(
          16,
          16,
          16,
          16 + MediaQuery.viewInsetsOf(context).bottom,
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text(r.practicedOn, style: Theme.of(context).textTheme.titleLarge),
            const SizedBox(height: 8),
            for (final MapEntry(:key, :value) in r.actualSeconds.entries)
              Text(
                '${rules.labelOf(key)}：${formatSeconds(value)}（予定 ${r.plannedMinutes[key] ?? 0}分）',
              ),
            if (r.goal.isNotEmpty || r.nextFocus.isNotEmpty) ...[
              const SizedBox(height: 8),
              if (r.goal.isNotEmpty)
                Text(
                  '目標：${r.goal}（${PracticeRecord.achievementLabels[r.achievement]}）',
                ),
              if (r.nextFocus.isNotEmpty) Text('次回の課題：${r.nextFocus}'),
            ],
            Align(
              alignment: Alignment.centerLeft,
              child: TextButton.icon(
                onPressed: () {
                  Navigator.pop(context);
                  Navigator.push(
                    context,
                    MaterialPageRoute<void>(
                      fullscreenDialog: true,
                      builder: (_) => ReflectionPage(record: r),
                    ),
                  );
                },
                icon: const Icon(Icons.flag_outlined),
                label: const Text('目標・振り返りを編集'),
              ),
            ),
            const SizedBox(height: 4),
            TextField(
              controller: note,
              maxLines: 3,
              maxLength: 500,
              decoration: const InputDecoration(
                labelText: 'メモ',
                border: OutlineInputBorder(),
              ),
            ),
            Row(
              children: [
                TextButton.icon(
                  onPressed: () async {
                    final messenger = ScaffoldMessenger.of(context);
                    final ok = await showDialog<bool>(
                      context: context,
                      builder: (context) => AlertDialog(
                        title: const Text('この記録を削除しますか？'),
                        actions: [
                          TextButton(
                            onPressed: () => Navigator.pop(context, false),
                            child: const Text('やめる'),
                          ),
                          FilledButton(
                            onPressed: () => Navigator.pop(context, true),
                            child: const Text('削除'),
                          ),
                        ],
                      ),
                    );
                    if (ok == true) {
                      await services.practice.delete(r.id);
                      if (context.mounted) Navigator.pop(context);
                      messenger
                        ..removeCurrentSnackBar()
                        ..showSnackBar(
                          SnackBar(
                            content: Text('${r.practicedOn} の記録を削除しました'),
                            action: SnackBarAction(
                              label: '元に戻す',
                              onPressed: () => services.practice.restore(r.id),
                            ),
                          ),
                        );
                    }
                  },
                  icon: const Icon(Icons.delete_outline),
                  label: const Text('削除'),
                ),
                const Spacer(),
                FilledButton(
                  onPressed: () async {
                    if (note.text != r.note) {
                      await services.practice.updateNote(r.id, note.text);
                    }
                    if (context.mounted) Navigator.pop(context);
                  },
                  child: const Text('保存'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
