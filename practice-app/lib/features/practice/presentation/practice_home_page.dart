import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

import '../../../app/app_services.dart';
import '../../../core/clock.dart';
import '../../menu/domain/menu_audit.dart';
import '../../menu/domain/menu_presets.dart';
import '../domain/day_condition.dart';
import '../domain/practice_record.dart';
import '../domain/practice_stats.dart';
import '../../local_ai/ai_coach_card.dart';
import 'timer_page.dart';
import 'visible_records_builder.dart';

/// 今日の予定と調子・今日のメニューと、練習の開始
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
          return ListenableBuilder(
            listenable: services.menu,
            builder: (context, _) {
              final menu = services.menu;
              final rules = menu.rules;
              final minutes = menu.value;
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
                  const SizedBox(height: 8),
                  const TodayConditionCard(),
                  const SizedBox(height: 8),
                  AiCoachCard(stats: stats),
                  const SizedBox(height: 16),
                  Row(
                    children: [
                      Expanded(
                        child: Text(
                          rules.label,
                          style: theme.textTheme.titleLarge,
                        ),
                      ),
                      if (menu.isTemporary)
                        TextButton(
                          onPressed: menu.resetToSaved,
                          child: const Text('いつものメニューに戻す'),
                        ),
                    ],
                  ),
                  if (menu.isTemporary)
                    Text(
                      '今日だけのメニューです（保存はしていません）',
                      style: theme.textTheme.bodySmall,
                    ),
                  const SizedBox(height: 8),
                  for (final section in rules.sections)
                    if (section.item case final item?)
                      ListTile(
                        dense: true,
                        title: Text(item.label),
                        trailing: Text(
                          (minutes[item.id] ?? 0) == 0
                              ? 'お休み'
                              : '${minutes[item.id]}分',
                          style: theme.textTheme.titleMedium,
                        ),
                      )
                    else ...[
                      // グループ（Arban）は合計と、今日吹く章だけ
                      ListTile(
                        dense: true,
                        title: Text(section.group!.label),
                        trailing: Text(
                          '${section.members.fold(0, (s, i) => s + (minutes[i.id] ?? 0))}分',
                          style: theme.textTheme.titleMedium,
                        ),
                      ),
                      for (final item in section.members)
                        if ((minutes[item.id] ?? 0) > 0)
                          ListTile(
                            dense: true,
                            contentPadding: const EdgeInsets.only(
                              left: 32,
                              right: 16,
                            ),
                            title: Text(item.label),
                            trailing: Text('${minutes[item.id]}分'),
                          ),
                    ],
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
                    '時間モードとメニューは「メニュー」タブで変えられます',
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

/// 今日の予定と調子を入れると、練習の量をすすめる
class TodayConditionCard extends StatefulWidget {
  const TodayConditionCard({super.key});

  @override
  State<TodayConditionCard> createState() => _TodayConditionCardState();
}

class _TodayConditionCardState extends State<TodayConditionCard> {
  late final AppServices _services = AppScope.of(context);
  DayCondition? _condition;
  String? _day;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    final day = localDateString(_services.clock());
    if (day != _day) {
      _day = day;
      _services.dayConditions.load(day).then((c) {
        if (mounted && _day == day) setState(() => _condition = c);
      });
    }
  }

  void _update(DayCondition c) {
    setState(() => _condition = c);
    _services.dayConditions.save(_day!, c);
  }

  /// おすすめどおりのメニュー（プリセットがなければ、そのモードの保存済みメニュー）
  Map<String, int> _adviceMenu(DayAdvice advice) {
    final menu = _services.menu;
    final modeId = advice.modeId!;
    if (advice.presetId == null) return menu.savedMenuFor(modeId);
    final rules = menu.modes.firstWhere((m) => m.id == modeId);
    return trumpetBasicPresets
        .firstWhere((p) => p.id == advice.presetId)
        .menuFor(rules.items.map((i) => i.id));
  }

  @override
  Widget build(BuildContext context) => ListenableBuilder(
    listenable: _services.menu,
    builder: (context, _) => _build(context),
  );

  Widget _build(BuildContext context) {
    final c = _condition;
    final theme = Theme.of(context);
    if (c == null) return const SizedBox.shrink();
    final advice = adviseForDay(c);
    final menu = _services.menu;
    final applied =
        advice.modeId == null ||
        (menu.rules.id == advice.modeId &&
            mapEquals(menu.value, _adviceMenu(advice)));
    return Card(
      color: advice.rest ? theme.colorScheme.errorContainer : null,
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('今日の予定と調子', style: theme.textTheme.titleMedium),
            const SizedBox(height: 8),
            Wrap(
              spacing: 8,
              runSpacing: 4,
              children: [
                FilterChip(
                  label: const Text('合奏・レッスン'),
                  selected: c.rehearsal,
                  onSelected: (v) => _update(c.copyWith(rehearsal: v)),
                ),
                FilterChip(
                  label: const Text('本番'),
                  selected: c.performance,
                  onSelected: (v) => _update(c.copyWith(performance: v)),
                ),
                FilterChip(
                  label: const Text('昨日たくさん吹いた'),
                  selected: c.heavyYesterday,
                  onSelected: (v) => _update(c.copyWith(heavyYesterday: v)),
                ),
                FilterChip(
                  label: const Text('唇が痛い'),
                  selected: c.lipPain,
                  onSelected: (v) => _update(c.copyWith(lipPain: v)),
                ),
              ],
            ),
            const SizedBox(height: 8),
            SizedBox(
              width: double.infinity,
              child: SegmentedButton<Fatigue>(
                segments: const [
                  ButtonSegment(value: Fatigue.fresh, label: Text('元気')),
                  ButtonSegment(value: Fatigue.normal, label: Text('ふつう')),
                  ButtonSegment(value: Fatigue.tired, label: Text('疲れている')),
                ],
                selected: {c.fatigue},
                showSelectedIcon: false,
                onSelectionChanged: (s) =>
                    _update(c.copyWith(fatigue: s.single)),
              ),
            ),
            const SizedBox(height: 12),
            Text(advice.message),
            if (advice.modeId != null && !applied) ...[
              const SizedBox(height: 8),
              FilledButton.tonal(
                onPressed: () =>
                    menu.useForToday(advice.modeId!, _adviceMenu(advice)),
                child: const Text('今日はこのおすすめにする'),
              ),
            ],
          ],
        ),
      ),
    );
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
