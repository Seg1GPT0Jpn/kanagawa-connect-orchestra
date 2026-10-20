import 'package:flutter/material.dart';

import '../../../app/app_services.dart';
import '../domain/pitch.dart';
import '../domain/pitch_stats.dart';
import '../domain/tuner_settings.dart';

/// 音程の記録：期間ごとの傾向・苦手な音・練習ごとの記録
class PitchStatsPage extends StatefulWidget {
  const PitchStatsPage({super.key});

  @override
  State<PitchStatsPage> createState() => _PitchStatsPageState();
}

class _PitchStatsPageState extends State<PitchStatsPage> {
  int _days = 7;

  @override
  Widget build(BuildContext context) {
    final services = AppScope.of(context);
    final theme = Theme.of(context);
    final now = services.clock();
    return Scaffold(
      appBar: AppBar(title: const Text('音程の記録')),
      body: StreamBuilder<List<TunerSession>>(
        stream: services.tunerSessions.watchAll(),
        builder: (context, snap) {
          final sessions = snap.data ?? const [];
          if (sessions.isEmpty) {
            return const Padding(
              padding: EdgeInsets.all(24),
              child: Text('まだ記録がありません。チューナーで5秒以上吹いて「止める」と、音名ごとの音程が記録されます。'),
            );
          }
          final from = _days == 0
              ? null
              : now.subtract(Duration(days: _days)).millisecondsSinceEpoch;
          final inRange = [
            for (final s in sessions)
              if (from == null || s.startedAtMillis >= from) s,
          ];
          final merged = mergeStats(
            inRange.map((s) => s.stats),
            tolerance: services.tuner.settings.tolerance,
          );
          return ListView(
            padding: const EdgeInsets.all(16),
            children: [
              SegmentedButton<int>(
                segments: const [
                  ButtonSegment(value: 7, label: Text('7日')),
                  ButtonSegment(value: 30, label: Text('30日')),
                  ButtonSegment(value: 0, label: Text('すべて')),
                ],
                selected: {_days},
                showSelectedIcon: false,
                onSelectionChanged: (v) => setState(() => _days = v.single),
              ),
              const SizedBox(height: 12),
              if (merged.frames == 0)
                const Text('この期間の記録はありません')
              else
                StatsSummary(
                  stats: merged,
                  title:
                      '${inRange.length}回・${merged.seconds.toStringAsFixed(0)}秒の合計',
                ),
              const Divider(height: 32),
              Text('練習ごとの記録', style: theme.textTheme.titleMedium),
              for (final (i, s) in sessions.indexed)
                ListTile(
                  contentPadding: EdgeInsets.zero,
                  title: Text(
                    '${_date(s.startedAtMillis)}　合っていた割合 ${(s.stats.inTuneRatio * 100).round()}%',
                  ),
                  subtitle: Text(
                    '${s.stats.seconds.toStringAsFixed(0)}秒・${s.stats.notes.length}音・${s.temperamentLabel}・A4＝${s.a4.toStringAsFixed(0)}Hz',
                  ),
                  trailing: const Icon(Icons.chevron_right),
                  onTap: () => Navigator.push(
                    context,
                    MaterialPageRoute<void>(
                      builder: (_) => SessionDetailPage(
                        session: s,
                        previous: i + 1 < sessions.length
                            ? sessions[i + 1]
                            : null,
                      ),
                    ),
                  ),
                ),
            ],
          );
        },
      ),
    );
  }
}

String _date(int millis) {
  final d = DateTime.fromMillisecondsSinceEpoch(millis);
  return '${d.month}/${d.day} ${d.hour}:${d.minute.toString().padLeft(2, '0')}';
}

/// 1回の練習の詳しい記録（音名別の表・前回との比較）
class SessionDetailPage extends StatelessWidget {
  const SessionDetailPage({super.key, required this.session, this.previous});

  final TunerSession session;
  final TunerSession? previous;

  @override
  Widget build(BuildContext context) {
    final services = AppScope.of(context);
    final theme = Theme.of(context);
    final prev = previous;
    final comparison = prev == null
        ? const <NoteComparison>[]
        : compareSessions(prev.stats, session.stats);
    final t = services.referenceTone.pitch.transposition;
    return Scaffold(
      appBar: AppBar(
        title: Text(_date(session.startedAtMillis)),
        actions: [
          IconButton(
            tooltip: 'この記録を削除',
            onPressed: () async {
              final navigator = Navigator.of(context);
              await services.tunerSessions.delete(session.id);
              navigator.pop();
            },
            icon: const Icon(Icons.delete_outline),
          ),
        ],
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Text(
            '${session.temperamentLabel}・A4＝${session.a4.toStringAsFixed(0)}Hz・'
            '合格 ±${session.stats.tolerance.toStringAsFixed(0)} セント',
            style: theme.textTheme.bodySmall,
          ),
          const SizedBox(height: 8),
          StatsSummary(
            stats: session.stats,
            title: '${session.stats.seconds.toStringAsFixed(0)}秒の記録',
          ),
          if (comparison.isNotEmpty) ...[
            const Divider(height: 32),
            Text(
              '前回（${_date(prev!.startedAtMillis)}）との比べ',
              style: theme.textTheme.titleMedium,
            ),
            Text(
              '全体：${(prev.stats.inTuneRatio * 100).round()}% → ${(session.stats.inTuneRatio * 100).round()}%',
            ),
            for (final c in comparison)
              Text(
                '${noteLabel(t.concertToWritten(c.midi))}：'
                '${(c.before.inTuneRatio * 100).round()}% → ${(c.after.inTuneRatio * 100).round()}%'
                '（${c.inTuneChange >= 0 ? '+' : ''}${(c.inTuneChange * 100).round()}）',
                style: TextStyle(
                  color: c.inTuneChange >= 0.05
                      ? Colors.green.shade700
                      : c.inTuneChange <= -0.05
                      ? theme.colorScheme.error
                      : null,
                ),
              ),
          ],
        ],
      ),
    );
  }
}

enum _NoteSort {
  pitch('音の高さ'),
  weak('苦手な順'),
  time('長く吹いた順'),
  offset('ずれの大きい順');

  const _NoteSort(this.label);
  final String label;
}

/// 統計のまとめ：合っていた割合・高め／低めの割合・分布・苦手な音・音名別の表
class StatsSummary extends StatefulWidget {
  const StatsSummary({super.key, required this.stats, required this.title});

  final PitchStats stats;
  final String title;

  @override
  State<StatsSummary> createState() => _StatsSummaryState();
}

class _StatsSummaryState extends State<StatsSummary> {
  _NoteSort _sort = _NoteSort.pitch;

  @override
  Widget build(BuildContext context) {
    final services = AppScope.of(context);
    final theme = Theme.of(context);
    final st = widget.stats;
    final t = services.referenceTone.pitch.transposition;
    final weak = st.weakNotes();
    final notes = st.notes.values.toList();
    switch (_sort) {
      case _NoteSort.pitch:
        notes.sort((a, b) => a.midi.compareTo(b.midi));
      case _NoteSort.weak:
        notes.sort((a, b) => a.inTuneRatio.compareTo(b.inTuneRatio));
      case _NoteSort.time:
        notes.sort((a, b) => b.frames.compareTo(a.frames));
      case _NoteSort.offset:
        notes.sort((a, b) => b.meanCents.abs().compareTo(a.meanCents.abs()));
    }
    String name(int midi) => noteLabel(t.concertToWritten(midi));
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Text(widget.title, style: theme.textTheme.bodySmall),
        Text(
          '合っていた割合 ${(st.inTuneRatio * 100).round()}%',
          style: theme.textTheme.headlineSmall,
        ),
        const SizedBox(height: 4),
        BalanceBar(stats: st),
        const SizedBox(height: 12),
        Text('ずれの分布（セント）', style: theme.textTheme.titleSmall),
        SizedBox(height: 90, child: Histogram(stats: st)),
        const SizedBox(height: 12),
        Text('苦手な音', style: theme.textTheme.titleSmall),
        if (weak.isEmpty)
          const Text('目立って苦手な音はありません（2秒以上吹いた音のうち、合っていた割合が60%未満の音）')
        else
          for (final n in weak)
            Text(
              '・${name(n.midi)}：合っていた割合 ${(n.inTuneRatio * 100).round()}%・'
              '平均 ${formatCents(n.meanCents)} セント'
              '（${n.meanCents > st.tolerance
                  ? '高めになりがち'
                  : n.meanCents < -st.tolerance
                  ? '低めになりがち'
                  : 'ばらつきが大きい'}）',
            ),
        const SizedBox(height: 12),
        Row(
          children: [
            Expanded(child: Text('音名別', style: theme.textTheme.titleSmall)),
            DropdownButton<_NoteSort>(
              value: _sort,
              items: [
                for (final s in _NoteSort.values)
                  DropdownMenuItem(value: s, child: Text(s.label)),
              ],
              onChanged: (v) => setState(() => _sort = v!),
            ),
          ],
        ),
        Text('音名を押すと、その音（実音）を基準音で鳴らします', style: theme.textTheme.bodySmall),
        for (final n in notes)
          ListTile(
            dense: true,
            contentPadding: EdgeInsets.zero,
            leading: IconButton(
              tooltip: '${name(n.midi)} を鳴らす',
              icon: const Icon(Icons.volume_up_outlined),
              onPressed: () => services.referenceTone.playConcert(n.midi),
            ),
            title: Text('${name(n.midi)}　${(n.inTuneRatio * 100).round()}%'),
            subtitle: Text(
              '平均 ${formatCents(n.meanCents)}・ばらつき ±${n.spreadCents.toStringAsFixed(1)} セント・'
              '${st.secondsOf(n).toStringAsFixed(1)}秒',
            ),
          ),
        ListenableBuilder(
          listenable: services.referenceTone,
          builder: (context, _) => services.referenceTone.isPlaying
              ? OutlinedButton.icon(
                  onPressed: services.referenceTone.stop,
                  icon: const Icon(Icons.stop),
                  label: const Text('基準音を止める'),
                )
              : const SizedBox.shrink(),
        ),
      ],
    );
  }
}

/// 低め・合っている・高めの割合の帯
class BalanceBar extends StatelessWidget {
  const BalanceBar({super.key, required this.stats});

  final PitchStats stats;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final b = stats.balance;
    final parts = [
      (b.low, Colors.blue.shade400, '低め'),
      (b.inTune, Colors.green.shade500, '合っている'),
      (b.high, Colors.orange.shade600, '高め'),
    ];
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        ClipRRect(
          borderRadius: BorderRadius.circular(4),
          child: SizedBox(
            height: 12,
            child: Row(
              children: [
                for (final (v, c, _) in parts)
                  if (v > 0)
                    Expanded(
                      flex: (v * 1000).round().clamp(1, 1000),
                      child: ColoredBox(
                        color: c,
                        child: const SizedBox.expand(),
                      ),
                    ),
              ],
            ),
          ),
        ),
        const SizedBox(height: 2),
        Text(
          parts.map((p) => '${p.$3} ${(p.$1 * 100).round()}%').join('・'),
          style: theme.textTheme.bodySmall,
        ),
      ],
    );
  }
}

/// ずれの分布の棒グラフ（-50〜+50 セント）
class Histogram extends StatelessWidget {
  const Histogram({super.key, required this.stats});

  final PitchStats stats;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final h = stats.histogram;
    final max = h.fold(0, (a, b) => a > b ? a : b);
    return Column(
      children: [
        Expanded(
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.end,
            children: [
              for (var i = 0; i < h.length; i++)
                Expanded(
                  child: Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 1),
                    child: FractionallySizedBox(
                      heightFactor: max == 0
                          ? 0
                          : (h[i] / max).clamp(0.02, 1.0),
                      alignment: Alignment.bottomCenter,
                      child: ColoredBox(
                        color:
                            ((i - histogramBuckets ~/ 2) * histogramStep)
                                    .abs() <=
                                stats.tolerance
                            ? Colors.green.shade500
                            : theme.colorScheme.primary.withValues(alpha: 0.6),
                      ),
                    ),
                  ),
                ),
            ],
          ),
        ),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            for (final l in const ['-50', '-25', '0', '+25', '+50'])
              Text(l, style: theme.textTheme.labelSmall),
          ],
        ),
      ],
    );
  }
}
