import 'dart:math' as math;
import 'dart:typed_data';

import 'package:flutter/material.dart';

import '../data/tuner_controller.dart';
import '../domain/pitch.dart';
import '../domain/spectrum.dart';

/// スペクトラム（マイクの音の周波数ごとの強さ）の画面
class SpectrumView extends StatelessWidget {
  const SpectrumView({super.key, required this.controller});

  final TunerController controller;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return ListenableBuilder(
      listenable: controller,
      builder: (context, _) {
        final s = controller.spectrum;
        final h = controller.harmonics;
        final r = controller.reading;
        final t = controller.pitch.transposition;
        return ListView(
          padding: const EdgeInsets.all(16),
          children: [
            Text(
              r == null
                  ? (controller.isListening
                        ? '音を出してください'
                        : '「はじめる」を押すとマイクで測ります')
                  : '${noteLabel(t.concertToWritten(r.midi))}'
                        '${t == Transposition.concert ? '' : '（実音 ${noteLabel(r.midi)}）'}'
                        '・基音 ${r.frequency.toStringAsFixed(1)} Hz',
              textAlign: TextAlign.center,
              style: theme.textTheme.titleMedium,
            ),
            const SizedBox(height: 8),
            SizedBox(
              height: 220,
              child: SpectrumGraph(
                spectrum: s,
                peakHold: controller.peakHold,
                fundamental: r?.frequency,
              ),
            ),
            Text(
              '横：周波数（Hz・対数目盛り）　縦：強さ（dB）。'
              '点線は倍音の位置（1＝基音）、薄い線はいちばん大きかった値',
              style: theme.textTheme.bodySmall,
            ),
            if (s != null)
              Text(
                '音の重心 ${s.centroid().round()} Hz'
                '${r == null ? '' : '（基音の ${(s.centroid() / r.frequency).toStringAsFixed(1)} 倍）'}',
                style: theme.textTheme.bodySmall,
              ),
            const SizedBox(height: 8),
            Row(
              children: [
                Expanded(
                  child: FilledButton.icon(
                    style: FilledButton.styleFrom(
                      minimumSize: const Size.fromHeight(48),
                    ),
                    onPressed: controller.isListening
                        ? controller.stop
                        : controller.start,
                    icon: Icon(
                      controller.isListening ? Icons.mic_off : Icons.mic,
                    ),
                    label: Text(controller.isListening ? '止める' : 'はじめる'),
                  ),
                ),
                const SizedBox(width: 8),
                IconButton.outlined(
                  tooltip: controller.spectrumFrozen ? '動かす' : '止めて見る',
                  isSelected: controller.spectrumFrozen,
                  onPressed: () =>
                      controller.setSpectrumFrozen(!controller.spectrumFrozen),
                  icon: const Icon(Icons.pause),
                  selectedIcon: const Icon(Icons.play_arrow),
                ),
                IconButton.outlined(
                  tooltip: '最大値を消す',
                  onPressed: controller.resetPeakHold,
                  icon: const Icon(Icons.restart_alt),
                ),
              ],
            ),
            if (controller.error != null) ...[
              const SizedBox(height: 8),
              Text(
                controller.error!,
                style: TextStyle(color: theme.colorScheme.error),
              ),
            ],
            const SizedBox(height: 16),
            Text('倍音のバランス（音色メーター）', style: theme.textTheme.titleMedium),
            const SizedBox(height: 8),
            ToneMeter(profile: h),
            const SizedBox(height: 16),
            Text(
              'スペクトラムは、マイクの位置・部屋の響き・端末のマイクの特性で大きく変わります。'
              '同じ場所・同じ距離で比べると、音色の変化（息の量・アンブシュア・マウスピースの違いなど）が分かります。',
              style: theme.textTheme.bodySmall,
            ),
          ],
        );
      },
    );
  }
}

/// 倍音ごとの強さの棒グラフ（基音を 0 dB として、-60 dB まで）
class ToneMeter extends StatelessWidget {
  const ToneMeter({super.key, required this.profile, this.height = 90});

  final HarmonicProfile? profile;
  final double height;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final p = profile;
    final levels = p?.levelsDb ?? List.filled(8, -60.0);
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        SizedBox(
          height: height,
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.end,
            children: [
              for (var k = 0; k < levels.length; k++)
                Expanded(
                  child: Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 3),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.end,
                      children: [
                        AnimatedContainer(
                          duration: const Duration(milliseconds: 80),
                          height:
                              (height - 18) *
                              ((levels[k] + 60) / 60).clamp(0.02, 1.0),
                          color: p == null
                              ? theme.colorScheme.surfaceContainerHighest
                              : Color.lerp(
                                  theme.colorScheme.primary,
                                  theme.colorScheme.tertiary,
                                  k / levels.length,
                                ),
                        ),
                        SizedBox(
                          height: 18,
                          child: Text(
                            '${k + 1}',
                            style: theme.textTheme.labelSmall,
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
            ],
          ),
        ),
        Text(
          p == null
              ? '音を出すと、基音（1）と倍音（2〜8）の強さを表示します'
              : '明るさ ${p.brightness.toStringAsFixed(1)}：${p.description}',
          style: theme.textTheme.bodySmall,
          textAlign: TextAlign.center,
        ),
      ],
    );
  }
}

/// スペクトラムのグラフ（対数の周波数軸）
class SpectrumGraph extends StatelessWidget {
  const SpectrumGraph({
    super.key,
    required this.spectrum,
    this.peakHold,
    this.fundamental,
    this.minHz = 50,
    this.maxHz = 8000,
  });

  final Spectrum? spectrum;
  final Float64List? peakHold;
  final double? fundamental;
  final double minHz;
  final double maxHz;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return CustomPaint(
      size: Size.infinite,
      painter: _SpectrumPainter(
        spectrum: spectrum,
        peakHold: peakHold,
        fundamental: fundamental,
        minHz: minHz,
        maxHz: maxHz,
        fill: theme.colorScheme.primary.withValues(alpha: 0.35),
        line: theme.colorScheme.primary,
        hold: theme.colorScheme.tertiary.withValues(alpha: 0.7),
        grid: theme.colorScheme.outlineVariant,
        text: theme.textTheme.labelSmall!.copyWith(
          color: theme.colorScheme.onSurfaceVariant,
        ),
        harmonic: theme.colorScheme.secondary,
      ),
    );
  }
}

class _SpectrumPainter extends CustomPainter {
  _SpectrumPainter({
    required this.spectrum,
    required this.peakHold,
    required this.fundamental,
    required this.minHz,
    required this.maxHz,
    required this.fill,
    required this.line,
    required this.hold,
    required this.grid,
    required this.text,
    required this.harmonic,
  });

  final Spectrum? spectrum;
  final Float64List? peakHold;
  final double? fundamental;
  final double minHz, maxHz;
  final Color fill, line, hold, grid, harmonic;
  final TextStyle text;

  static const minDb = -100.0, maxDb = 0.0;

  @override
  void paint(Canvas canvas, Size size) {
    const bottomPad = 14.0, leftPad = 26.0;
    final w = size.width - leftPad;
    final h = size.height - bottomPad;
    final logMin = math.log(minHz), logMax = math.log(maxHz);
    double x(double hz) =>
        leftPad + (math.log(hz) - logMin) / (logMax - logMin) * w;
    double y(double db) =>
        (1 - ((db - minDb) / (maxDb - minDb)).clamp(0.0, 1.0)) * h;

    final gridPaint = Paint()
      ..color = grid
      ..strokeWidth = 1;
    void label(String s, Offset at) {
      final tp = TextPainter(
        text: TextSpan(text: s, style: text),
        textDirection: TextDirection.ltr,
      )..layout();
      tp.paint(canvas, at - Offset(tp.width / 2, 0));
    }

    for (final hz in const [100.0, 200.0, 500.0, 1000.0, 2000.0, 5000.0]) {
      canvas.drawLine(Offset(x(hz), 0), Offset(x(hz), h), gridPaint);
      label(hz >= 1000 ? '${hz ~/ 1000}k' : '${hz.toInt()}', Offset(x(hz), h));
    }
    for (final db in const [0.0, -20.0, -40.0, -60.0, -80.0, -100.0]) {
      canvas.drawLine(
        Offset(leftPad, y(db)),
        Offset(size.width, y(db)),
        gridPaint,
      );
      label('${db.toInt()}', Offset(leftPad / 2, y(db) - 6));
    }

    final f0 = fundamental;
    if (f0 != null) {
      final hp = Paint()
        ..color = harmonic.withValues(alpha: 0.6)
        ..strokeWidth = 1;
      for (var k = 1; k * f0 <= maxHz && k <= 12; k++) {
        final xx = x(k * f0);
        for (var yy = 0.0; yy < h; yy += 6) {
          canvas.drawLine(Offset(xx, yy), Offset(xx, yy + 3), hp);
        }
        if (k <= 8) label('$k', Offset(xx, 0));
      }
    }

    final s = spectrum;
    if (s == null) return;
    final lo = (minHz / s.binHz).floor().clamp(1, s.amplitude.length - 1);
    final hi = (maxHz / s.binHz).ceil().clamp(lo, s.amplitude.length - 1);

    Path curve(double Function(int i) dbOf) {
      final p = Path();
      // 1画素に複数の点が重なる高い周波数では、その画素の最大値を使う
      double? lastX;
      var maxInPixel = minDb;
      for (var i = lo; i <= hi; i++) {
        final xx = x(math.max(s.frequencyOf(i), minHz))
            .clamp(leftPad, size.width);
        final db = dbOf(i);
        if (lastX != null && xx - lastX < 1) {
          maxInPixel = math.max(maxInPixel, db);
          continue;
        }
        final v = math.max(maxInPixel, db);
        if (lastX == null) {
          p.moveTo(xx, y(v));
        } else {
          p.lineTo(xx, y(v));
        }
        lastX = xx;
        maxInPixel = minDb;
      }
      return p;
    }

    final hold = peakHold;
    if (hold != null && hold.length == s.amplitude.length) {
      canvas.drawPath(
        curve((i) => hold[i]),
        Paint()
          ..color = this.hold
          ..style = PaintingStyle.stroke
          ..strokeWidth = 1,
      );
    }
    final c = curve(s.dbAt);
    final area = Path.from(c)
      ..lineTo(x(maxHz), h)
      ..lineTo(x(math.max(s.frequencyOf(lo), minHz)), h)
      ..close();
    canvas.drawPath(area, Paint()..color = fill);
    canvas.drawPath(
      c,
      Paint()
        ..color = line
        ..style = PaintingStyle.stroke
        ..strokeWidth = 1.5,
    );
  }

  @override
  bool shouldRepaint(_SpectrumPainter old) => true;
}
