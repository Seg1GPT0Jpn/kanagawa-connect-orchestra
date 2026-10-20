import 'package:flutter/material.dart';

import '../../../app/app_services.dart';
import '../../../core/clock.dart';
import '../data/usage_tracker.dart';
import '../domain/practice_stats.dart';

/// 今日の目標の達成リング（練習・メトロノーム・チューナー・基準音・録音）
class GoalRingsCard extends StatelessWidget {
  const GoalRingsCard({super.key, required this.stats});

  final PracticeStats stats;

  @override
  Widget build(BuildContext context) {
    final services = AppScope.of(context);
    final theme = Theme.of(context);
    return ListenableBuilder(
      listenable: Listenable.merge([services.goals, services.usage]),
      builder: (context, _) {
        final goals = services.goals.goals;
        final today = localDateString(services.clock());
        return FutureBuilder<Map<UsageKind, int>>(
          future: services.usage.secondsOn(today),
          builder: (context, snap) {
            final used = {
              ...?snap.data,
              UsageKind.practice: stats.todaySeconds,
            };
            final kinds = [
              for (final k in UsageKind.values)
                if (goals.of(k) > 0) k,
            ];
            return Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Expanded(
                          child: Text(
                            '今日の時間の目標',
                            style: theme.textTheme.titleMedium,
                          ),
                        ),
                        IconButton(
                          tooltip: '目標を決める',
                          onPressed: () => GoalSettingsSheet.show(context),
                          icon: const Icon(Icons.flag_outlined),
                        ),
                      ],
                    ),
                    if (kinds.isEmpty)
                      Text(
                        '目標はまだありません。旗のボタンから、練習や道具ごとに1日の目標の時間を決められます。',
                        style: theme.textTheme.bodySmall,
                      )
                    else
                      Wrap(
                        spacing: 16,
                        runSpacing: 12,
                        children: [
                          for (final (i, k) in kinds.indexed)
                            _Ring(
                              label: k.label,
                              done: (used[k] ?? 0) / 60,
                              goal: goals.of(k).toDouble(),
                              color: _ringColors[i % _ringColors.length],
                            ),
                        ],
                      ),
                  ],
                ),
              ),
            );
          },
        );
      },
    );
  }
}

const _ringColors = [
  Color(0xFF2E7D32),
  Color(0xFF1565C0),
  Color(0xFFEF6C00),
  Color(0xFF6A1B9A),
  Color(0xFFC62828),
];

class _Ring extends StatelessWidget {
  const _Ring({
    required this.label,
    required this.done,
    required this.goal,
    required this.color,
  });

  final String label;
  final double done;
  final double goal;
  final Color color;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final ratio = goal <= 0 ? 0.0 : done / goal;
    return SizedBox(
      width: 88,
      child: Column(
        children: [
          SizedBox(
            width: 64,
            height: 64,
            child: Stack(
              alignment: Alignment.center,
              children: [
                SizedBox.expand(
                  child: CircularProgressIndicator(
                    value: ratio.clamp(0.0, 1.0),
                    strokeWidth: 7,
                    color: color,
                    backgroundColor: color.withValues(alpha: 0.15),
                  ),
                ),
                ratio >= 1
                    ? Icon(Icons.check, color: color)
                    : Text(
                        '${(ratio * 100).floor()}%',
                        style: theme.textTheme.labelMedium,
                      ),
              ],
            ),
          ),
          const SizedBox(height: 4),
          Text(
            label,
            style: theme.textTheme.labelSmall,
            textAlign: TextAlign.center,
          ),
          Text(
            '${done.floor()} / ${goal.round()}分',
            style: theme.textTheme.labelSmall,
          ),
        ],
      ),
    );
  }
}

/// 目標の時間を決める
class GoalSettingsSheet extends StatelessWidget {
  const GoalSettingsSheet({super.key});

  static Future<void> show(BuildContext context) => showModalBottomSheet<void>(
    context: context,
    isScrollControlled: true,
    showDragHandle: true,
    builder: (_) => const GoalSettingsSheet(),
  );

  @override
  Widget build(BuildContext context) {
    final services = AppScope.of(context);
    final theme = Theme.of(context);
    return ListenableBuilder(
      listenable: services.goals,
      builder: (context, _) {
        final g = services.goals.goals;
        return SafeArea(
          child: ListView(
            shrinkWrap: true,
            padding: const EdgeInsets.fromLTRB(16, 0, 16, 16),
            children: [
              Text('1日の目標（分）', style: theme.textTheme.titleLarge),
              Text(
                '長く吹くことより、毎日少しずつ続けることが大切です。疲れや痛みがある日は、目標に届かなくて大丈夫です。',
                style: theme.textTheme.bodySmall,
              ),
              for (final k in UsageKind.values) ...[
                const SizedBox(height: 8),
                Text(k.label, style: theme.textTheme.titleSmall),
                Wrap(
                  spacing: 4,
                  children: [
                    for (final m in const [0, 5, 10, 15, 20, 30, 45, 60, 90])
                      ChoiceChip(
                        label: Text(m == 0 ? 'なし' : '$m'),
                        selected: g.of(k) == m,
                        onSelected: (_) => services.goals.setGoal(k, m),
                      ),
                  ],
                ),
              ],
            ],
          ),
        );
      },
    );
  }
}
