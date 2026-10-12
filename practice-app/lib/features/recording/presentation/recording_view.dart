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
            const SizedBox(height: 4),
            const _HowToRecord(),
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
                          '音量のゆれ ${r.volumeSpreadDb.toStringAsFixed(1)}dB'
                          '${r.reliability == null ? '' : '・信頼度 ${r.reliability!.label}'}',
                        ),
                        trailing: IconButton(
                          tooltip: '削除',
                          icon: const Icon(Icons.delete_outline),
                          onPressed: () async {
                            final messenger = ScaffoldMessenger.of(context);
                            await c.repository.delete(r.id);
                            messenger
                              ..removeCurrentSnackBar()
                              ..showSnackBar(
                                SnackBar(
                                  content: const Text('分析結果を削除しました'),
                                  action: SnackBarAction(
                                    label: '元に戻す',
                                    onPressed: () => c.repository.save(r),
                                  ),
                                ),
                              );
                          },
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
            const SizedBox(height: 8),
            _ReliabilityBox(analysis: a),
            const SizedBox(height: 12),
            SizedBox(height: 120, child: PitchGraph(analysis: a)),
            Text(
              '音程の変化（中央の線が平均。緑の帯は ±5 セント。'
              '${a.gaps.isEmpty ? '' : '灰色は高さを測れなかった区間。'}）',
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
            const SizedBox(height: 8),
            Text(
              'この評価は、マイクで拾った音から計算した目安です。マイクの位置・部屋の響き・'
              '周りの音・端末のマイクの特性で結果は変わります。指導者や奏者の耳による評価の'
              '代わりにはなりません。同じ条件で録って、自分の変化を見るのに使ってください。',
              style: theme.textTheme.bodySmall,
            ),
          ],
        ),
      ),
    );
  }
}

/// 録り方の案内（たたんでおき、開くと読める）
class _HowToRecord extends StatelessWidget {
  const _HowToRecord();

  @override
  Widget build(BuildContext context) => const ExpansionTile(
    tilePadding: EdgeInsets.zero,
    title: Text('正しく測るための録り方'),
    childrenPadding: EdgeInsets.only(bottom: 8),
    expandedCrossAxisAlignment: CrossAxisAlignment.start,
    children: [
      Text('・マイク（端末の下側など）から 30〜50cm 離し、ベルを少し外して吹く'),
      Text('・静かで、響きすぎない部屋で（エアコン・換気扇・ほかの楽器の音を避ける）'),
      Text('・メゾフォルテくらいの楽な音量で、3秒以上まっすぐ伸ばす'),
      Text('・Bluetooth イヤホンのマイクは使わない（音が加工・圧縮されるため）'),
      Text('・比べるときは、毎回同じ場所・同じ距離・同じ端末で録る'),
    ],
  );
}

/// 信頼度の目安と理由
class _ReliabilityBox extends StatelessWidget {
  const _ReliabilityBox({required this.analysis});

  final ToneAnalysis analysis;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final a = analysis;
    final (icon, color) = switch (a.reliability) {
      Reliability.high => (Icons.verified_outlined, Colors.green.shade700),
      Reliability.medium => (Icons.info_outline, Colors.orange.shade800),
      Reliability.low => (Icons.warning_amber, theme.colorScheme.error),
    };
    return Container(
      padding: const EdgeInsets.all(8),
      decoration: BoxDecoration(
        border: Border.all(color: color.withValues(alpha: 0.5)),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(icon, color: color, size: 18),
              const SizedBox(width: 6),
              Text(
                '分析の信頼度：${a.reliability.label}',
                style: TextStyle(color: color, fontWeight: FontWeight.bold),
              ),
              const Spacer(),
              Text(
                '入力 ${a.levelDb.toStringAsFixed(0)} dB',
                style: theme.textTheme.bodySmall,
              ),
            ],
          ),
          if (a.reliabilityNotes.isEmpty)
            const Text('録音の条件に大きな問題は見つかりませんでした。')
          else
            for (final n in a.reliabilityNotes) Text('・$n'),
          if (a.reliability == Reliability.low)
            const Text('この結果はあてにしにくいため、録り直しをおすすめします。'),
        ],
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
        gap: theme.colorScheme.outline.withValues(alpha: 0.25),
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
    required this.gap,
  });

  final ToneAnalysis a;
  final Color line;
  final Color grid;
  final Color band;
  final Color gap;

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
    for (final g in a.gaps) {
      canvas.drawRect(
        Rect.fromLTRB(x(g.start), 0, x(g.end), size.height),
        Paint()..color = gap,
      );
    }
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
