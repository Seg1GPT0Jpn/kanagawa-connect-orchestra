/// 音の高さの検出（YIN 法。決定論的で、合成した波形でテストできる）
///
/// de Cheveigné & Kawahara (2002) "YIN, a fundamental frequency estimator for speech and music"
/// の差分関数・累積平均正規化・絶対しきい値・放物線補間を使う。
library;

import 'dart:math' as math;
import 'dart:typed_data';

class PitchEstimate {
  const PitchEstimate({
    required this.frequency,
    required this.clarity,
    required this.rms,
  });

  final double frequency;

  /// 周期性のはっきりさ（0〜1。1に近いほど確か）
  final double clarity;

  /// 音の大きさ（-1〜1 の波形の二乗平均平方根）
  final double rms;
}

class PitchDetector {
  const PitchDetector({
    required this.sampleRate,
    this.minFrequency = 80,
    this.maxFrequency = 1500,
    this.threshold = 0.15,
    this.minRms = 0.01,
  });

  final double sampleRate;

  /// トランペットの最低音（実音 E3 ≒ 165Hz）より下まで、最高音（実音 C6 ≒ 1047Hz）より上まで
  final double minFrequency;
  final double maxFrequency;

  /// YIN の絶対しきい値（小さいほど厳しい）
  final double threshold;

  /// これより小さい音は無音として扱う
  final double minRms;

  /// [samples]（-1〜1）の基本周波数。無音・はっきりしない音なら null
  PitchEstimate? detect(Float64List samples) {
    final n = samples.length;
    var sumSq = 0.0;
    for (final s in samples) {
      sumSq += s * s;
    }
    final rms = math.sqrt(sumSq / n);
    if (rms < minRms) return null;

    final minLag = (sampleRate / maxFrequency).floor().clamp(2, n ~/ 2);
    final maxLag = (sampleRate / minFrequency).ceil().clamp(minLag + 1, n ~/ 2);
    final w = n - maxLag; // 比べる長さ
    if (w < 16) return null;

    // 差分関数 d(τ) と累積平均正規化 d'(τ)
    final d = Float64List(maxLag + 1);
    for (var tau = 1; tau <= maxLag; tau++) {
      var sum = 0.0;
      for (var i = 0; i < w; i++) {
        final diff = samples[i] - samples[i + tau];
        sum += diff * diff;
      }
      d[tau] = sum;
    }
    final dn = Float64List(maxLag + 1)..[0] = 1;
    var running = 0.0;
    for (var tau = 1; tau <= maxLag; tau++) {
      running += d[tau];
      dn[tau] = running == 0 ? 1 : d[tau] * tau / running;
    }

    // しきい値を下回った最初の谷（なければ範囲内の最小値）
    var best = -1;
    for (var tau = minLag; tau <= maxLag; tau++) {
      if (dn[tau] < threshold) {
        while (tau + 1 <= maxLag && dn[tau + 1] < dn[tau]) {
          tau++;
        }
        best = tau;
        break;
      }
    }
    if (best < 0) {
      var minVal = double.infinity;
      for (var tau = minLag; tau <= maxLag; tau++) {
        if (dn[tau] < minVal) {
          minVal = dn[tau];
          best = tau;
        }
      }
      // はっきりしない（雑音など）
      if (minVal > 0.35) return null;
    }

    // 放物線補間で谷の位置を細かく求める
    var refined = best.toDouble();
    if (best > 1 && best < maxLag) {
      // 正規化前の差分関数で補間する（正規化した値より谷の形が素直で、ずれが小さい）
      final a = d[best - 1], b = d[best], c = d[best + 1];
      final denom = a - 2 * b + c;
      if (denom.abs() > 1e-12) refined = best + 0.5 * (a - c) / denom;
    }
    final freq = sampleRate / refined;
    if (freq < minFrequency || freq > maxFrequency) return null;
    return PitchEstimate(
      frequency: freq,
      clarity: (1 - dn[best]).clamp(0, 1),
      rms: rms,
    );
  }
}

/// 直近の値の中央値で、表示のふらつきを抑える
class MedianSmoother {
  MedianSmoother([this.size = 5]);

  final int size;
  final _values = <double>[];

  double add(double v) {
    _values.add(v);
    if (_values.length > size) _values.removeAt(0);
    final sorted = [..._values]..sort();
    return sorted[sorted.length ~/ 2];
  }

  void clear() => _values.clear();
}
