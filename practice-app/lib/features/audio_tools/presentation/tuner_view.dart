import 'dart:math' as math;

import 'package:flutter/material.dart';

import '../data/reference_tone_controller.dart';
import '../data/tuner_controller.dart';
import '../domain/note_tracker.dart';
import '../domain/pitch.dart';
import '../domain/temperament.dart';
import '../domain/tuner_settings.dart';
import 'pitch_stats_page.dart';
import 'reference_tone_view.dart';
import 'spectrum_view.dart';

/// チューナーの画面
class TunerView extends StatelessWidget {
  const TunerView({super.key, required this.controller, required this.pitch});

  final TunerController controller;
  final ReferenceToneController pitch;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return ListenableBuilder(
      listenable: controller,
      builder: (context, _) {
        final s = controller.settings;
        final r = controller.reading;
        final cents = controller.targetCents;
        final tuning = controller.pitch;
        final t = tuning.transposition;
        final color = _colorFor(theme, cents, s.tolerance);
        return ListView(
          padding: const EdgeInsets.all(16),
          children: [
            Row(
              children: [
                Expanded(
                  child: Text(
                    t == Transposition.concert ? '実音で表示' : '${t.label}の記譜で表示',
                    style: theme.textTheme.bodySmall,
                  ),
                ),
                IconButton(
                  tooltip: 'チューナーの設定',
                  onPressed: () => TunerSettingsSheet.show(context, controller),
                  icon: const Icon(Icons.tune),
                ),
              ],
            ),
            Text(
              r == null ? '—' : noteLabel(t.concertToWritten(r.midi)),
              textAlign: TextAlign.center,
              style: theme.textTheme.displayLarge?.copyWith(color: color),
            ),
            Text(
              r == null
                  ? (controller.isListening
                        ? '音を出してください'
                        : '「はじめる」を押すとマイクで測ります')
                  : '実音 ${noteLabel(r.midi)}・${r.frequency.toStringAsFixed(s.decimal ? 2 : 1)} Hz',
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 12),
            switch (s.display) {
              TunerDisplay.target => Center(
                child: TargetMeter(
                  cents: cents,
                  tolerance: s.tolerance,
                  streak: controller.inTuneStreak,
                  color: color,
                ),
              ),
              TunerDisplay.bar => CentsMeter(
                cents: cents,
                color: color,
                tolerance: s.tolerance,
              ),
              TunerDisplay.none => const SizedBox.shrink(),
            },
            const SizedBox(height: 4),
            Text(
              cents == null
                  ? ''
                  : '${formatCents(cents, decimal: s.decimal)} セント（${controller.inTune
                        ? 'ぴったり'
                        : cents > 0
                        ? '高い'
                        : '低い'}）',
              textAlign: TextAlign.center,
              style: theme.textTheme.titleMedium?.copyWith(color: color),
            ),
            _Basis(controller: controller),
            if (s.showLevel) ...[
              const SizedBox(height: 8),
              LinearProgressIndicator(value: controller.level, minHeight: 4),
            ],
            if (s.showPrevious || s.showAttack)
              _NoteInfo(controller: controller),
            if (s.showToneMeter) ...[
              const SizedBox(height: 12),
              ToneMeter(profile: controller.harmonics, height: 64),
            ],
            const SizedBox(height: 16),
            FilledButton.icon(
              style: FilledButton.styleFrom(
                minimumSize: const Size.fromHeight(56),
              ),
              onPressed: controller.isListening
                  ? controller.stop
                  : controller.start,
              icon: Icon(controller.isListening ? Icons.mic_off : Icons.mic),
              label: Text(controller.isListening ? '止める' : 'はじめる'),
            ),
            if (controller.error != null) ...[
              const SizedBox(height: 8),
              Text(
                controller.error!,
                style: TextStyle(color: theme.colorScheme.error),
              ),
            ],
            if (s.showTracker) _Tracker(controller: controller),
            const Divider(height: 32),
            PitchSettingsPanel(controller: pitch),
            const SizedBox(height: 8),
            Text(
              'マイクの音は端末の中だけで処理し、保存も送信もしません（保存するのは音程の統計だけです）。',
              style: theme.textTheme.bodySmall,
            ),
          ],
        );
      },
    );
  }
}

Color _colorFor(ThemeData theme, double? cents, double tolerance) {
  if (cents == null) return theme.disabledColor;
  if (cents.abs() <= tolerance) return Colors.green.shade600;
  if (cents.abs() <= tolerance * 3) return Colors.orange.shade700;
  return theme.colorScheme.error;
}

/// 何を基準に判定しているか（常に見えるように）
class _Basis extends StatelessWidget {
  const _Basis({required this.controller});

  final TunerController controller;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final p = controller.pitch;
    final r = controller.reading;
    final offset = controller.targetOffset;
    final lines = [
      '判定：A4＝${p.a4.toStringAsFixed(p.a4 % 1 == 0 ? 0 : 1)}Hz・${p.temperamentLabel}・'
          '合格 ±${controller.settings.tolerance.toStringAsFixed(0)} セント',
      if (p.temperament != Temperament.equal && r != null && offset != null)
        '${intervalNames[(r.midi - p.tonicPitchClass) % 12]}の目標は平均律より '
            '${formatCents(offset)} セント',
    ];
    return Padding(
      padding: const EdgeInsets.only(top: 4),
      child: Column(
        children: [
          for (final l in lines)
            Text(
              l,
              textAlign: TextAlign.center,
              style: theme.textTheme.bodySmall,
            ),
        ],
      ),
    );
  }
}

/// 直前の音・音程差・出だしの音程
class _NoteInfo extends StatelessWidget {
  const _NoteInfo({required this.controller});

  final TunerController controller;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final s = controller.settings;
    final t = controller.pitch.transposition;
    final prev = controller.previousNote;
    final cur = controller.currentNote;
    final interval = controller.intervalSemitones;
    final attack = cur?.attackOffset ?? prev?.attackOffset;
    final items = <String>[
      if (s.showPrevious && prev != null)
        '直前：${noteLabel(t.concertToWritten(prev.midi))} ${formatCents(prev.settledCents ?? prev.meanCents, decimal: s.decimal)}',
      if (s.showPrevious && interval != null) '音程：${intervalName(interval)}',
      if (s.showAttack && attack != null)
        '出だし：${formatCents(attack, decimal: s.decimal)}'
            '${attack.abs() <= s.tolerance
                ? '（安定して入った）'
                : attack > 0
                ? '（高めに入った）'
                : '（低めに入った）'}',
    ];
    if (items.isEmpty) return const SizedBox(height: 8);
    return Padding(
      padding: const EdgeInsets.only(top: 8),
      child: Wrap(
        alignment: WrapAlignment.center,
        spacing: 12,
        children: [
          for (final i in items) Text(i, style: theme.textTheme.bodyMedium),
        ],
      ),
    );
  }
}

/// 合っていた割合（この練習の間）と、記録を見る入口
class _Tracker extends StatelessWidget {
  const _Tracker({required this.controller});

  final TunerController controller;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final st = controller.stats;
    final saved = controller.lastSaved;
    return Padding(
      padding: const EdgeInsets.only(top: 12),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Row(
            children: [
              Expanded(
                child: Text(
                  st.frames == 0
                      ? '合っていた割合：音を出すと数えます'
                      : '合っていた割合 ${(st.inTuneRatio * 100).round()}%'
                            '（${st.seconds.toStringAsFixed(1)} 秒中）',
                  style: theme.textTheme.titleSmall,
                ),
              ),
              if (st.frames > 0 && controller.isListening)
                TextButton(
                  onPressed: controller.resetTracker,
                  child: const Text('数え直す'),
                ),
            ],
          ),
          if (st.frames > 0) BalanceBar(stats: st),
          if (saved != null && !controller.isListening)
            Text(
              '音程の記録を保存しました（${saved.stats.seconds.toStringAsFixed(0)} 秒）',
              style: theme.textTheme.bodySmall,
            ),
          Align(
            alignment: Alignment.centerLeft,
            child: TextButton.icon(
              onPressed: () => Navigator.push(
                context,
                MaterialPageRoute<void>(builder: (_) => const PitchStatsPage()),
              ),
              icon: const Icon(Icons.insights_outlined),
              label: const Text('音程の記録（音名別・苦手な音）'),
            ),
          ),
        ],
      ),
    );
  }
}

/// ターゲット表示：中心からのずれで点が動き、合っていると緑の輪になる。
/// 合ったまま続けると輪が大きくなり、顔の表情も変わる
class TargetMeter extends StatelessWidget {
  const TargetMeter({
    super.key,
    required this.cents,
    required this.tolerance,
    required this.streak,
    required this.color,
    this.size = 180,
  });

  final double? cents;
  final double tolerance;

  /// 合ったまま続いているフレーム数
  final int streak;
  final Color color;
  final double size;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final c = cents;
    final ok = c != null && c.abs() <= tolerance;
    // 約1秒（20フレーム）合わせ続けると最大
    final grow = ok ? (streak / 20).clamp(0.0, 1.0) : 0.0;
    final face = c == null
        ? Icons.sentiment_neutral
        : ok
        ? Icons.sentiment_very_satisfied
        : c.abs() <= tolerance * 3
        ? Icons.sentiment_satisfied
        : Icons.sentiment_dissatisfied;
    return SizedBox(
      width: size,
      height: size,
      child: Stack(
        alignment: Alignment.center,
        children: [
          CustomPaint(
            size: Size.square(size),
            painter: _TargetPainter(
              cents: c,
              tolerance: tolerance,
              grow: grow,
              color: color,
              ring: theme.colorScheme.outlineVariant,
              band: Colors.green.withValues(alpha: 0.18),
            ),
          ),
          AnimatedScale(
            duration: const Duration(milliseconds: 150),
            scale: 1 + grow * 0.6,
            child: Icon(face, color: color, size: 40),
          ),
        ],
      ),
    );
  }
}

class _TargetPainter extends CustomPainter {
  _TargetPainter({
    required this.cents,
    required this.tolerance,
    required this.grow,
    required this.color,
    required this.ring,
    required this.band,
  });

  final double? cents;
  final double tolerance, grow;
  final Color color, ring, band;

  @override
  void paint(Canvas canvas, Size size) {
    final center = size.center(Offset.zero);
    final r = size.width / 2 - 4;
    // 半径：中心＝0 セント、外周＝50 セント
    double radiusOf(double c) => (c.abs().clamp(0, 50) / 50) * r;
    canvas.drawCircle(center, radiusOf(tolerance), Paint()..color = band);
    final ringPaint = Paint()
      ..color = ring
      ..style = PaintingStyle.stroke;
    for (final c in const [10.0, 25.0, 50.0]) {
      canvas.drawCircle(center, radiusOf(c), ringPaint);
    }
    // 上が「高い」、下が「低い」
    canvas.drawLine(center.translate(0, -r), center.translate(0, r), ringPaint);
    final c = cents;
    if (c == null) return;
    if (c.abs() <= tolerance) {
      canvas.drawCircle(
        center,
        radiusOf(tolerance) + 6 + grow * 24,
        Paint()
          ..color = color
          ..style = PaintingStyle.stroke
          ..strokeWidth = 4 + grow * 4,
      );
    } else {
      final y = -math.min(radiusOf(c), r) * c.sign;
      canvas.drawCircle(center.translate(0, y), 9, Paint()..color = color);
    }
  }

  @override
  bool shouldRepaint(_TargetPainter old) =>
      old.cents != cents || old.grow != grow || old.color != color;
}

/// -50〜+50 セントの針（横棒）
class CentsMeter extends StatelessWidget {
  const CentsMeter({
    super.key,
    required this.cents,
    required this.color,
    this.tolerance = 5,
  });

  final double? cents;
  final Color color;
  final double tolerance;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return SizedBox(
      height: 48,
      child: LayoutBuilder(
        builder: (context, box) {
          final w = box.maxWidth;
          double x(double c) => w / 2 + (c.clamp(-50, 50) / 50) * (w / 2 - 8);
          return Stack(
            children: [
              // 目盛り（-50・-25・0・+25・+50）と、合格の範囲の帯
              Positioned(
                left: x(-tolerance),
                width: x(tolerance) - x(-tolerance),
                top: 8,
                bottom: 8,
                child: ColoredBox(color: Colors.green.withValues(alpha: 0.2)),
              ),
              for (final c in const [-50.0, -25.0, 0.0, 25.0, 50.0])
                Positioned(
                  left: x(c) - 1,
                  width: 2,
                  top: c == 0 ? 4 : 14,
                  bottom: c == 0 ? 4 : 14,
                  child: ColoredBox(color: theme.colorScheme.outline),
                ),
              if (cents != null)
                AnimatedPositioned(
                  duration: const Duration(milliseconds: 80),
                  left: x(cents!) - 3,
                  width: 6,
                  top: 0,
                  bottom: 0,
                  child: DecoratedBox(
                    decoration: BoxDecoration(
                      color: color,
                      borderRadius: BorderRadius.circular(3),
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

/// チューナーの設定（表示方式・判定範囲・応答速度・表示する項目）
class TunerSettingsSheet extends StatelessWidget {
  const TunerSettingsSheet({super.key, required this.controller});

  final TunerController controller;

  static Future<void> show(BuildContext context, TunerController c) =>
      showModalBottomSheet<void>(
        context: context,
        isScrollControlled: true,
        showDragHandle: true,
        builder: (_) => TunerSettingsSheet(controller: c),
      );

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return ListenableBuilder(
      listenable: controller,
      builder: (context, _) {
        final s = controller.settings;
        void set(TunerSettings n) => controller.updateSettings(n);
        return SafeArea(
          child: ListView(
            shrinkWrap: true,
            padding: const EdgeInsets.fromLTRB(16, 0, 16, 16),
            children: [
              Text('チューナーの設定', style: theme.textTheme.titleLarge),
              const SizedBox(height: 12),
              Text('表示の方式', style: theme.textTheme.titleSmall),
              const SizedBox(height: 4),
              SegmentedButton<TunerDisplay>(
                segments: [
                  for (final d in TunerDisplay.values)
                    ButtonSegment(value: d, label: Text(d.label)),
                ],
                selected: {s.display},
                showSelectedIcon: false,
                onSelectionChanged: (v) => set(s.copyWith(display: v.single)),
              ),
              const SizedBox(height: 12),
              Text('合格の範囲（判定）', style: theme.textTheme.titleSmall),
              Wrap(
                spacing: 6,
                children: [
                  for (final (v, label) in toleranceChoices)
                    ChoiceChip(
                      label: Text(label),
                      selected: s.tolerance == v,
                      onSelected: (_) => set(s.copyWith(tolerance: v)),
                    ),
                ],
              ),
              const SizedBox(height: 12),
              Text('応答の速さ（音程をならす時間）', style: theme.textTheme.titleSmall),
              const SizedBox(height: 4),
              SegmentedButton<TunerDamping>(
                segments: [
                  for (final d in TunerDamping.values)
                    ButtonSegment(value: d, label: Text(d.label)),
                ],
                selected: {s.damping},
                showSelectedIcon: false,
                onSelectionChanged: (v) => set(s.copyWith(damping: v.single)),
              ),
              Text(
                '速い：音の動きにすぐ反応（ゆれも見える）／ゆっくり：落ち着いた表示',
                style: theme.textTheme.bodySmall,
              ),
              const SizedBox(height: 8),
              SwitchListTile(
                contentPadding: EdgeInsets.zero,
                title: const Text('セントを 0.1 単位で表示'),
                value: s.decimal,
                onChanged: (v) => set(s.copyWith(decimal: v)),
              ),
              SwitchListTile(
                contentPadding: EdgeInsets.zero,
                title: const Text('直前の音と音程の差'),
                value: s.showPrevious,
                onChanged: (v) => set(s.copyWith(showPrevious: v)),
              ),
              SwitchListTile(
                contentPadding: EdgeInsets.zero,
                title: const Text('音の出だしの音程'),
                value: s.showAttack,
                onChanged: (v) => set(s.copyWith(showAttack: v)),
              ),
              SwitchListTile(
                contentPadding: EdgeInsets.zero,
                title: const Text('合っていた割合'),
                value: s.showTracker,
                onChanged: (v) => set(s.copyWith(showTracker: v)),
              ),
              SwitchListTile(
                contentPadding: EdgeInsets.zero,
                title: const Text('音色メーター（倍音のバランス）'),
                value: s.showToneMeter,
                onChanged: (v) => set(s.copyWith(showToneMeter: v)),
              ),
              SwitchListTile(
                contentPadding: EdgeInsets.zero,
                title: const Text('音量のバー'),
                value: s.showLevel,
                onChanged: (v) => set(s.copyWith(showLevel: v)),
              ),
            ],
          ),
        );
      },
    );
  }
}
