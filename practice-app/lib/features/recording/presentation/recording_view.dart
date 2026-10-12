import 'package:flutter/material.dart';

import '../../audio_tools/data/reference_tone_controller.dart';
import '../../audio_tools/domain/pitch.dart';
import '../data/recording_controller.dart';
import '../domain/recording_result.dart';
import '../domain/tone_analysis.dart';

/// 録音と簡易音響分析の画面
class RecordingView extends StatelessWidget {
  const RecordingView({
    super.key,
    required this.controller,
    required this.pitch,
  });

  final RecordingController controller;
  final ReferenceToneController pitch;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return ListenableBuilder(
      listenable: controller,
      builder: (context, _) {
        final c = controller;
        final recording = c.phase == RecordingPhase.recording;
        final secs = c.elapsed.inMilliseconds / 1000;
        return ListView(
          padding: const EdgeInsets.all(16),
          children: [
            Text(
              'ロングトーンを録って、音程と音量の安定を確かめます（最大${RecordingController.maxDuration.inSeconds}秒）。',
              style: theme.textTheme.bodyMedium,
            ),
            const SizedBox(height: 12),
            if (recording) ...[
              Text(
                '${secs.toStringAsFixed(1)} 秒',
                textAlign: TextAlign.center,
                style: theme.textTheme.displaySmall,
              ),
              LinearProgressIndicator(value: c.level, minHeight: 6),
              const SizedBox(height: 4),
              LinearProgressIndicator(
                value: secs / RecordingController.maxDuration.inSeconds,
                minHeight: 2,
                color: theme.colorScheme.outline,
              ),
              const SizedBox(height: 12),
            ],
            FilledButton.icon(
              style: FilledButton.styleFrom(
                minimumSize: const Size.fromHeight(56),
                backgroundColor: recording ? theme.colorScheme.error : null,
              ),
              onPressed: recording ? c.stop : c.start,
              icon: Icon(recording ? Icons.stop : Icons.fiber_manual_record),
              label: Text(
                recording
                    ? '止めて分析する'
                    : (c.phase == RecordingPhase.done ? '録り直す' : '録音する'),
              ),
            ),
            if (c.error != null) ...[
              const SizedBox(height: 8),
              Text(c.error!, style: TextStyle(color: theme.colorScheme.error)),
            ],
            if (c.phase == RecordingPhase.done && c.result != null) ...[
              const SizedBox(height: 16),
              _ResultCard(
                analysis: c.result!,
                transposition: pitch.pitch.transposition,
              ),
              const SizedBox(height: 8),
              Row(
                children: [
                  Expanded(
                    child: OutlinedButton.icon(
                      onPressed: c.isPlaying ? c.stopPlayback : c.play,
                      icon: Icon(c.isPlaying ? Icons.stop : Icons.play_arrow),
                      label: Text(c.isPlaying ? '止める' : '聴き直す'),
                    ),
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: FilledButton.tonalIcon(
                      onPressed: c.isSaved ? null : () => c.save(),
                      icon: Icon(c.isSaved ? Icons.check : Icons.save_outlined),
                      label: Text(c.isSaved ? '保存しました' : '結果を保存'),
                    ),
                  ),
                ],
              ),
            ],
            const SizedBox(height: 8),
            Text(
              '録った音はこの画面を閉じるまでの間だけ端末の中に置き、保存も送信もしません（保存するのは分析結果だけです）。',
              style: theme.textTheme.bodySmall,
            ),
            const Divider(height: 32),
            Text('保存した結果', style: theme.textTheme.titleMedium),
            StreamBuilder<List<RecordingResult>>(
              stream: c.repository.watchAll(),
              builder: (context, snap) {
                final list = snap.data ?? const [];
                if (list.isEmpty) {
                  return Padding(
                    padding: const EdgeInsets.symmetric(vertical: 8),
                    child: Text('まだありません', style: theme.textTheme.bodySmall),
                  );
                }
                final t = pitch.pitch.transposition;
                return Column(
                  children: [
                    for (final r in list.take(30))
                      ListTile(
                        contentPadding: EdgeInsets.zero,
                        dense: true,
                        title: Text(
                          '${_date(r.recordedAtMillis)}　${noteLabel(t.concertToWritten(r.midi))}'
                          '（実音 ${noteLabel(r.midi)}）${r.voicedSeconds.toStringAsFixed(1)}秒',
                        ),
                        subtitle: Text(
                          '音程のゆれ ±${r.pitchSpreadCents.toStringAsFixed(1)}・変化 ${_signed(r.driftCents)}セント・'
                          '音量のゆれ ${r.volumeSpreadDb.toStringAsFixed(1)}dB',
                        ),
                        trailing: IconButton(
                          tooltip: '削除',
                          icon: const Icon(Icons.delete_outline),
                          onPressed: () => c.repository.delete(r.id),
                        ),
                      ),
                  ],
                );
              },
            ),
          ],
        );
      },
    );
  }

  static String _date(int millis) {
    final d = DateTime.fromMillisecondsSinceEpoch(millis);
    return '${d.month}/${d.day} ${d.hour}:${d.minute.toString().padLeft(2, '0')}';
  }
}

String _signed(double v) => '${v >= 0 ? '+' : ''}${v.toStringAsFixed(0)}';

class _ResultCard extends StatelessWidget {
  const _ResultCard({required this.analysis, required this.transposition});

  final ToneAnalysis analysis;
  final Transposition transposition;

  @override
  Widget build(BuildContext context) {
    final a = analysis;
    final theme = Theme.of(context);
    final lines = describeAnalysis(a);
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              '${noteLabel(transposition.concertToWritten(a.midi))}'
              '${transposition == Transposition.concert ? '' : '（実音 ${noteLabel(a.midi)}）'}'
              '　${_signed(a.centsOffset)} セント',
              style: theme.textTheme.titleLarge,
            ),
            Text(
              '鳴っていた時間 ${a.voicedSeconds.toStringAsFixed(1)} 秒・${a.medianFrequency.toStringAsFixed(1)} Hz',
              style: theme.textTheme.bodySmall,
            ),
            const SizedBox(height: 12),
            SizedBox(height: 120, child: PitchGraph(analysis: a)),
            Text(
              '音程の変化（中央の線が平均。緑の帯は ±5 セント）',
              style: theme.textTheme.bodySmall,
            ),
            const SizedBox(height: 12),
            _GradeRow(
              label: '音程のゆれ',
              value: '±${a.pitchSpreadCents.toStringAsFixed(1)} セント',
              grade: a.pitchGrade,
            ),
            _GradeRow(
              label: '上ずり・下がり',
              value: '${_signed(a.driftCents)} セント',
              grade: a.driftGrade,
            ),
            _GradeRow(
              label: '音量のゆれ',
              value: '${a.volumeSpreadDb.toStringAsFixed(1)} dB',
              grade: a.volumeGrade,
            ),
            _GradeRow(
              label: '立ち上がり',
              value: '${a.attackSeconds.toStringAsFixed(2)} 秒',
              grade: a.attackGrade,
            ),
            const SizedBox(height: 8),
            for (final l in lines) Text('・$l'),
          ],
        ),
      ),
    );
  }
}

class _GradeRow extends StatelessWidget {
  const _GradeRow({
    required this.label,
    required this.value,
    required this.grade,
  });

  final String label;
  final String value;
  final Grade grade;

  @override
  Widget build(BuildContext context) {
    final (icon, color, text) = switch (grade) {
      Grade.good => (Icons.check_circle, Colors.green.shade600, 'よい'),
      Grade.fair => (Icons.adjust, Colors.orange.shade700, 'もう少し'),
      Grade.needsWork => (
        Icons.error_outline,
        Theme.of(context).colorScheme.error,
        '課題',
      ),
    };
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 2),
      child: Row(
        children: [
          Icon(icon, color: color, size: 18),
          const SizedBox(width: 6),
          Expanded(child: Text(label)),
          Text(value),
          const SizedBox(width: 8),
          SizedBox(
            width: 56,
            child: Text(
              text,
              style: TextStyle(color: color),
              textAlign: TextAlign.end,
            ),
          ),
        ],
      ),
    );
  }
}

/// 音程の変化のグラフ（平均からのずれ、±50 セント）
class PitchGraph extends StatelessWidget {
  const PitchGraph({super.key, required this.analysis});

  final ToneAnalysis analysis;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return CustomPaint(
      painter: _PitchGraphPainter(
        analysis,
        line: theme.colorScheme.primary,
        grid: theme.colorScheme.outlineVariant,
        band: Colors.green.withValues(alpha: 0.18),
      ),
      size: Size.infinite,
    );
  }
}

class _PitchGraphPainter extends CustomPainter {
  _PitchGraphPainter(
    this.a, {
    required this.line,
    required this.grid,
    required this.band,
  });

  final ToneAnalysis a;
  final Color line;
  final Color grid;
  final Color band;

  @override
  void paint(Canvas canvas, Size size) {
    const range = 50.0;
    double y(double cents) =>
        size.height / 2 -
        (cents.clamp(-range, range) / range) * (size.height / 2);
    final dur = a.duration <= 0 ? 1 : a.duration;
    double x(double t) => t / dur * size.width;

    canvas.drawRect(
      Rect.fromLTRB(0, y(5), size.width, y(-5)),
      Paint()..color = band,
    );
    final gridPaint = Paint()
      ..color = grid
      ..strokeWidth = 1;
    for (final c in const [-50.0, -25.0, 0.0, 25.0, 50.0]) {
      canvas.drawLine(Offset(0, y(c)), Offset(size.width, y(c)), gridPaint);
    }
    final p = Paint()
      ..color = line
      ..strokeWidth = 2
      ..style = PaintingStyle.stroke;
    Path? path;
    for (final f in a.frames) {
      final hz = f.frequency;
      if (hz == null) {
        if (path != null) canvas.drawPath(path, p);
        path = null;
        continue;
      }
      final pt = Offset(x(f.time), y(centsBetween(hz, a.medianFrequency)));
      if (path == null) {
        path = Path()..moveTo(pt.dx, pt.dy);
      } else {
        path.lineTo(pt.dx, pt.dy);
      }
    }
    if (path != null) canvas.drawPath(path, p);
  }

  @override
  bool shouldRepaint(_PitchGraphPainter old) => old.a != a || old.line != line;
}
