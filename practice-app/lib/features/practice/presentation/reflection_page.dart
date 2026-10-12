import 'package:flutter/material.dart';

import '../../../app/app_services.dart';
import '../../../core/clock.dart';
import '../../audio_tools/domain/pitch.dart';
import '../../recording/domain/recording_result.dart';
import '../domain/practice_record.dart';

/// 練習の振り返り：目標の達成度・振り返り（メモ）・次回の課題。今日の録音分析も添えられる
class ReflectionPage extends StatefulWidget {
  const ReflectionPage({super.key, required this.record});

  final PracticeRecord record;

  @override
  State<ReflectionPage> createState() => _ReflectionPageState();
}

class _ReflectionPageState extends State<ReflectionPage> {
  late final AppServices _services = AppScope.of(context);
  late final _goal = TextEditingController(text: widget.record.goal);
  late final _note = TextEditingController(text: widget.record.note);
  late final _next = TextEditingController(text: widget.record.nextFocus);
  late int _achievement = widget.record.achievement;
  List<RecordingResult> _todayRecordings = const [];
  final Set<String> _attached = {};
  bool _saving = false;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) => _loadRecordings());
  }

  Future<void> _loadRecordings() async {
    final all = await _services.recording.repository.all();
    if (!mounted) return;
    setState(() {
      _todayRecordings = [
        for (final r in all)
          if (localDateString(
                DateTime.fromMillisecondsSinceEpoch(r.recordedAtMillis),
              ) ==
              widget.record.practicedOn)
            r,
      ];
    });
  }

  @override
  void dispose() {
    _goal.dispose();
    _note.dispose();
    _next.dispose();
    super.dispose();
  }

  String _summary(RecordingResult r) {
    final t = _services.referenceTone.pitch.transposition;
    return '録音 ${noteLabel(t.concertToWritten(r.midi))}：音程のゆれ ±${r.pitchSpreadCents.toStringAsFixed(1)}セント・'
        '変化 ${r.driftCents >= 0 ? '+' : ''}${r.driftCents.toStringAsFixed(0)}セント・'
        '音量のゆれ ${r.volumeSpreadDb.toStringAsFixed(1)}dB'
        '${r.reliability == null ? '' : '（信頼度 ${r.reliability!.label}）'}';
  }

  Future<void> _save() async {
    setState(() => _saving = true);
    final lines = [
      for (final r in _todayRecordings)
        if (_attached.contains(r.id)) _summary(r),
    ];
    var note = _note.text.trim();
    if (lines.isNotEmpty) {
      note = [if (note.isNotEmpty) note, ...lines].join('\n');
    }
    if (note.length > 500) note = note.substring(0, 500);
    await _services.practice.updateReflection(
      widget.record.id,
      goal: _goal.text.trim(),
      achievement: _achievement,
      note: note,
      nextFocus: _next.text.trim(),
    );
    if (mounted) Navigator.pop(context);
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      appBar: AppBar(
        title: const Text('練習の振り返り'),
        actions: [
          TextButton(
            onPressed: _saving ? null : () => Navigator.pop(context),
            child: const Text('あとで'),
          ),
        ],
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Text(
            '${widget.record.practicedOn}・${formatPracticeTime(widget.record.totalActualSeconds)}',
            style: theme.textTheme.bodySmall,
          ),
          const SizedBox(height: 8),
          TextField(
            controller: _goal,
            maxLength: 200,
            decoration: const InputDecoration(
              labelText: '今日の目標',
              hintText: '例：ロングトーンの音程を安定させる',
              border: OutlineInputBorder(),
            ),
          ),
          const SizedBox(height: 8),
          Text('目標はどのくらいできましたか', style: theme.textTheme.titleSmall),
          const SizedBox(height: 4),
          AchievementSelector(
            value: _achievement,
            onChanged: (v) => setState(() => _achievement = v),
          ),
          const SizedBox(height: 16),
          TextField(
            controller: _note,
            maxLines: 3,
            maxLength: 500,
            decoration: const InputDecoration(
              labelText: '振り返り（できたこと・気づいたこと）',
              border: OutlineInputBorder(),
            ),
          ),
          if (_todayRecordings.isNotEmpty) ...[
            Text('今日の録音分析を添える', style: theme.textTheme.titleSmall),
            for (final r in _todayRecordings)
              CheckboxListTile(
                contentPadding: EdgeInsets.zero,
                dense: true,
                value: _attached.contains(r.id),
                onChanged: (v) => setState(
                  () =>
                      v == true ? _attached.add(r.id) : _attached.remove(r.id),
                ),
                title: Text(_summary(r)),
              ),
            const SizedBox(height: 8),
          ],
          TextField(
            controller: _next,
            maxLength: 200,
            decoration: const InputDecoration(
              labelText: '次回の課題（次の練習の目標に引き継げます）',
              hintText: '例：高音の B♭ を楽に出す',
              border: OutlineInputBorder(),
            ),
          ),
          const SizedBox(height: 8),
          FilledButton(
            style: FilledButton.styleFrom(
              minimumSize: const Size.fromHeight(48),
            ),
            onPressed: _saving ? null : _save,
            child: const Text('振り返りを保存'),
          ),
        ],
      ),
    );
  }
}

/// 達成度（1〜5）を選ぶ。もう一度押すと未記入に戻す
class AchievementSelector extends StatelessWidget {
  const AchievementSelector({
    super.key,
    required this.value,
    required this.onChanged,
  });

  final int value;
  final ValueChanged<int> onChanged;

  @override
  Widget build(BuildContext context) => Wrap(
    spacing: 6,
    runSpacing: 4,
    children: [
      for (var i = 1; i <= 5; i++)
        ChoiceChip(
          label: Text(PracticeRecord.achievementLabels[i]),
          selected: value == i,
          onSelected: (sel) => onChanged(sel ? i : 0),
        ),
    ],
  );
}
