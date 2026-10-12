import 'package:flutter/material.dart';

import '../data/reference_tone_controller.dart';
import '../data/tuner_controller.dart';
import '../domain/pitch.dart';
import 'reference_tone_view.dart';

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
        final r = controller.reading;
        final t = controller.pitch.transposition;
        final inTune = r != null && r.cents.abs() <= 5;
        final color = r == null
            ? theme.disabledColor
            : inTune
            ? Colors.green.shade600
            : r.cents.abs() <= 15
            ? Colors.orange.shade700
            : theme.colorScheme.error;
        return ListView(
          padding: const EdgeInsets.all(16),
          children: [
            const SizedBox(height: 8),
            if (t != Transposition.concert)
              Text(
                '${t.label}の記譜',
                textAlign: TextAlign.center,
                style: theme.textTheme.bodySmall,
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
                  : '実音 ${noteLabel(r.midi)}・${r.frequency.toStringAsFixed(1)} Hz',
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 16),
            CentsMeter(cents: r?.cents, color: color),
            const SizedBox(height: 4),
            Text(
              r == null
                  ? ''
                  : '${r.cents >= 0 ? '+' : ''}${r.cents.toStringAsFixed(0)} セント（${inTune
                        ? 'ぴったり'
                        : r.cents > 0
                        ? '高い'
                        : '低い'}）',
              textAlign: TextAlign.center,
              style: theme.textTheme.titleMedium?.copyWith(color: color),
            ),
            const SizedBox(height: 8),
            LinearProgressIndicator(value: controller.level, minHeight: 4),
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
            const Divider(height: 32),
            PitchSettingsPanel(controller: pitch),
            const SizedBox(height: 8),
            Text(
              'マイクの音は端末の中だけで処理し、保存も送信もしません。',
              style: theme.textTheme.bodySmall,
            ),
          ],
        );
      },
    );
  }
}

/// -50〜+50 セントの針
class CentsMeter extends StatelessWidget {
  const CentsMeter({super.key, required this.cents, required this.color});

  final double? cents;
  final Color color;

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
              // 目盛り（-50・-25・0・+25・+50）と、±5セントの「ぴったり」の帯
              Positioned(
                left: x(-5),
                width: x(5) - x(-5),
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
