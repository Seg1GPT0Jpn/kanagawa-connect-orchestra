import 'dart:async';

import 'package:flutter/material.dart';

import '../../../app/app_services.dart';
import '../../../core/clock.dart';
import '../domain/practice_record.dart';
import '../domain/practice_session.dart';

/// メニューの項目を順番に計るタイマー。終わったら記録して、保存した記録を返す
class TimerPage extends StatefulWidget {
  const TimerPage({super.key, required this.menu, this.goal = ''});

  final Map<String, int> menu;

  /// 今日の目標（記録にも残す）
  final String goal;

  @override
  State<TimerPage> createState() => _TimerPageState();
}

class _TimerPageState extends State<TimerPage> {
  late final AppServices _services = AppScope.of(context);
  late final PracticeSession _session = PracticeSession.fromMenu(
    widget.menu,
    _services.menu.rules,
    _services.clock(),
  );
  Timer? _ticker;
  bool _saving = false;

  @override
  void initState() {
    super.initState();
    // 表示の更新だけ。時間は時刻の差で計算するので、更新が遅れてもずれない
    _ticker = Timer.periodic(
      const Duration(milliseconds: 250),
      (_) => setState(() {}),
    );
  }

  @override
  void dispose() {
    _ticker?.cancel();
    super.dispose();
  }

  DateTime get _now => _services.clock();

  Future<void> _finish() async {
    if (_saving) return;
    setState(() => _saving = true);
    final actual = _session.finish(_now);
    final navigator = Navigator.of(context);
    PracticeRecord? saved;
    if (actual.values.any((s) => s > 0)) {
      saved = await _services.practice.create(
        ownerUid: _services.sync.user?.uid,
        startedAt: _session.startedAt,
        ruleSetId: _services.menu.rules.id,
        plannedMinutes: widget.menu,
        actualSeconds: actual,
        goal: widget.goal,
      );
    }
    navigator.pop(saved);
  }

  Future<void> _confirmFinish() async {
    final ok = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('練習を終えますか？'),
        content: const Text('ここまでの時間を記録します。疲れや痛みがあるときは、途中で終えて大丈夫です。'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('続ける'),
          ),
          FilledButton(
            onPressed: () => Navigator.pop(context, true),
            child: const Text('終えて記録'),
          ),
        ],
      ),
    );
    if (ok == true) await _finish();
  }

  void _next() {
    if (_session.isLast) {
      _finish();
    } else {
      setState(() => _session.next(_now));
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final now = _now;
    final seg = _session.current;
    final remaining = _session.remainingSeconds(now);
    final progress = seg.plannedSeconds == 0
        ? 1.0
        : (_session.elapsedSeconds(now) / seg.plannedSeconds).clamp(0.0, 1.0);

    return PopScope(
      canPop: false,
      onPopInvokedWithResult: (didPop, _) {
        if (!didPop) _confirmFinish();
      },
      child: Scaffold(
        appBar: AppBar(
          title: Text('${_session.index + 1} / ${_session.segments.length}'),
        ),
        body: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              if (widget.goal.isNotEmpty) ...[
                Text(
                  '今日の目標：${widget.goal}',
                  textAlign: TextAlign.center,
                  style: theme.textTheme.bodyMedium?.copyWith(
                    color: theme.colorScheme.primary,
                  ),
                ),
                const SizedBox(height: 12),
              ],
              Text(
                seg.label,
                style: theme.textTheme.headlineMedium,
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 24),
              Text(
                formatSeconds(remaining),
                style: theme.textTheme.displayLarge?.copyWith(
                  fontFeatures: const [FontFeature.tabularFigures()],
                  color: remaining < 0 ? theme.colorScheme.error : null,
                ),
                textAlign: TextAlign.center,
              ),
              if (remaining < 0)
                Text(
                  '予定の時間を過ぎています',
                  style: TextStyle(color: theme.colorScheme.error),
                  textAlign: TextAlign.center,
                ),
              const SizedBox(height: 16),
              LinearProgressIndicator(value: progress, minHeight: 8),
              const SizedBox(height: 24),
              Expanded(
                child: ListView(
                  children: [
                    for (final (i, s) in _session.segments.indexed)
                      ListTile(
                        dense: true,
                        leading: Icon(
                          i < _session.index
                              ? Icons.check_circle
                              : i == _session.index
                              ? Icons.play_circle_outline
                              : Icons.circle_outlined,
                        ),
                        title: Text(s.label),
                        trailing: Text('${s.plannedSeconds ~/ 60}分'),
                      ),
                  ],
                ),
              ),
              Row(
                children: [
                  Expanded(
                    child: OutlinedButton.icon(
                      style: OutlinedButton.styleFrom(
                        minimumSize: const Size.fromHeight(56),
                      ),
                      onPressed: _saving
                          ? null
                          : () => setState(
                              () => _session.isRunning
                                  ? _session.pause(now)
                                  : _session.resume(now),
                            ),
                      icon: Icon(
                        _session.isRunning ? Icons.pause : Icons.play_arrow,
                      ),
                      label: Text(_session.isRunning ? '一時停止' : '再開'),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: FilledButton.icon(
                      style: FilledButton.styleFrom(
                        minimumSize: const Size.fromHeight(56),
                      ),
                      onPressed: _saving ? null : _next,
                      icon: Icon(
                        _session.isLast ? Icons.flag : Icons.skip_next,
                      ),
                      label: Text(_session.isLast ? '終えて記録' : '次へ'),
                    ),
                  ),
                ],
              ),
              TextButton(
                onPressed: _saving ? null : _confirmFinish,
                child: const Text('途中で終える'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
