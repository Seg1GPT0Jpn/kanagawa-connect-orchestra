import 'dart:async';

import 'package:flutter/material.dart';

import '../data/reference_tone_controller.dart';
import '../domain/interval_quiz.dart';

/// 音程当て：2つの音を聴いて、音程を答える（聴き分けの練習）
class IntervalTrainerPage extends StatefulWidget {
  const IntervalTrainerPage({super.key, required this.tone});

  final ReferenceToneController tone;

  @override
  State<IntervalTrainerPage> createState() => _IntervalTrainerPageState();
}

class _IntervalTrainerPageState extends State<IntervalTrainerPage> {
  Set<int> _intervals = {...easyIntervals};
  QuizMode _mode = QuizMode.up;
  late IntervalQuiz _quiz = _newQuiz();
  IntervalQuestion? _q;
  int? _answered;
  final List<Timer> _timers = [];

  IntervalQuiz _newQuiz() => IntervalQuiz(intervals: _intervals, mode: _mode);

  @override
  void dispose() {
    _cancel();
    widget.tone.stop();
    super.dispose();
  }

  void _cancel() {
    for (final t in _timers) {
      t.cancel();
    }
    _timers.clear();
  }

  /// 問題の音を鳴らす（ボタンの処理から直接呼ぶ）
  Future<void> _play(IntervalQuestion q) {
    _cancel();
    final tone = widget.tone..stop();
    void later(int ms, void Function() f) =>
        _timers.add(Timer(Duration(milliseconds: ms), f));
    if (q.mode == QuizMode.together) {
      final first = tone.toggleHeld(q.root);
      unawaited(tone.toggleHeld(q.second));
      later(1600, tone.stop);
      return first;
    }
    final first = tone.playConcert(q.root);
    later(800, () => unawaited(tone.playConcert(q.second)));
    later(1700, tone.stop);
    return first;
  }

  void _next() {
    final q = _quiz.next();
    setState(() {
      _q = q;
      _answered = null;
    });
    unawaited(_play(q));
  }

  void _answer(int semitones) {
    final q = _q;
    if (q == null || _answered != null) return;
    _quiz.answer(q, semitones);
    setState(() => _answered = semitones);
  }

  void _reset() {
    _cancel();
    widget.tone.stop();
    setState(() {
      _quiz = _newQuiz();
      _q = null;
      _answered = null;
    });
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final q = _q;
    final answered = _answered;
    return Scaffold(
      appBar: AppBar(title: const Text('音程当て')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Text(
            '2つの音を聴いて、音程を答えます。管楽器では、合奏で音程を合わせる耳を育てる練習になります。',
            style: theme.textTheme.bodySmall,
          ),
          const SizedBox(height: 8),
          SegmentedButton<QuizMode>(
            segments: [
              for (final m in QuizMode.values)
                ButtonSegment(value: m, label: Text(m.label)),
            ],
            selected: {_mode},
            showSelectedIcon: false,
            onSelectionChanged: (v) {
              _mode = v.single;
              _reset();
            },
          ),
          const SizedBox(height: 8),
          Text('出す音程', style: theme.textTheme.titleSmall),
          Wrap(
            spacing: 4,
            runSpacing: 4,
            children: [
              for (final (s, name) in quizIntervals)
                FilterChip(
                  label: Text(name),
                  selected: _intervals.contains(s),
                  onSelected: (v) {
                    final next = {..._intervals};
                    v ? next.add(s) : next.remove(s);
                    if (next.isEmpty) return;
                    _intervals = next;
                    _reset();
                  },
                ),
            ],
          ),
          const Divider(height: 24),
          Text(
            _quiz.asked == 0
                ? 'まだ答えていません'
                : '正解 ${_quiz.correct} / ${_quiz.asked}（${(_quiz.rate * 100).round()}%）',
            style: theme.textTheme.titleMedium,
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 8),
          Row(
            children: [
              Expanded(
                child: FilledButton.icon(
                  onPressed: q == null || answered != null ? _next : null,
                  icon: const Icon(Icons.play_arrow),
                  label: Text(q == null ? 'はじめる' : '次の問題'),
                ),
              ),
              const SizedBox(width: 8),
              OutlinedButton.icon(
                onPressed: q == null ? null : () => _play(q),
                icon: const Icon(Icons.replay),
                label: const Text('もう一度'),
              ),
            ],
          ),
          const SizedBox(height: 12),
          if (q != null)
            Wrap(
              spacing: 6,
              runSpacing: 6,
              children: [
                for (final s in _intervals.toList()..sort())
                  ChoiceChip(
                    label: Text(intervalLabel(s)),
                    selected: answered == s,
                    selectedColor: answered == null
                        ? null
                        : s == q.semitones
                        ? Colors.green.shade200
                        : theme.colorScheme.errorContainer,
                    backgroundColor: answered != null && s == q.semitones
                        ? Colors.green.shade100
                        : null,
                    onSelected: (_) => _answer(s),
                  ),
              ],
            ),
          if (q != null && answered != null) ...[
            const SizedBox(height: 8),
            Text(
              answered == q.semitones
                  ? '正解！ ${intervalLabel(q.semitones)}'
                  : '答えは ${intervalLabel(q.semitones)} でした',
              style: theme.textTheme.titleMedium,
              textAlign: TextAlign.center,
            ),
          ],
          if (_quiz.byInterval.isNotEmpty) ...[
            const Divider(height: 24),
            Text('音程ごとの正解率', style: theme.textTheme.titleSmall),
            for (final MapEntry(key: s, value: (a, c))
                in (_quiz.byInterval.entries.toList()
                  ..sort((x, y) => x.key.compareTo(y.key))))
              Text('${intervalLabel(s)}：$c / $a'),
          ],
        ],
      ),
    );
  }
}
