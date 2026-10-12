/// 周波数分析（スペクトラム）と倍音のバランス（決定論的）
library;

import 'dart:math' as math;
import 'dart:typed_data';

/// 高速フーリエ変換（基数2・その場で計算）。[re]・[im] の長さは2のべき乗
void fft(Float64List re, Float64List im) {
  final n = re.length;
  assert(n == im.length && n > 0 && (n & (n - 1)) == 0);
  // ビット反転の並べ替え
  for (var i = 1, j = 0; i < n; i++) {
    var bit = n >> 1;
    for (; j & bit != 0; bit >>= 1) {
      j ^= bit;
    }
    j ^= bit;
    if (i < j) {
      final tr = re[i];
      re[i] = re[j];
      re[j] = tr;
      final ti = im[i];
      im[i] = im[j];
      im[j] = ti;
    }
  }
  for (var len = 2; len <= n; len <<= 1) {
    final ang = -2 * math.pi / len;
    final wr = math.cos(ang), wi = math.sin(ang);
    for (var i = 0; i < n; i += len) {
      var cr = 1.0, ci = 0.0;
      for (var k = 0; k < len ~/ 2; k++) {
        final a = i + k, b = a + len ~/ 2;
        final xr = re[b] * cr - im[b] * ci;
        final xi = re[b] * ci + im[b] * cr;
        re[b] = re[a] - xr;
        im[b] = im[a] - xi;
        re[a] += xr;
        im[a] += xi;
        final nr = cr * wr - ci * wi;
        ci = cr * wi + ci * wr;
        cr = nr;
      }
    }
  }
}

final Map<int, Float64List> _hannCache = {};

Float64List _hann(int n) => _hannCache.putIfAbsent(
  n,
  () => Float64List.fromList([
    for (var i = 0; i < n; i++) 0.5 - 0.5 * math.cos(2 * math.pi * i / (n - 1)),
  ]),
);

/// 1区間のスペクトラム。[amplitude] は周波数ごとの振幅（正弦波の振幅と同じ単位。1 が最大）
class Spectrum {
  Spectrum({
    required this.sampleRate,
    required this.size,
    required this.amplitude,
  });

  /// [samples]（-1〜1）を分析する。長さが2のべき乗でなければ、前を切って合わせる
  factory Spectrum.of(Float64List samples, {required double sampleRate}) {
    var n = 1;
    while (n * 2 <= samples.length) {
      n *= 2;
    }
    final w = _hann(n);
    final re = Float64List(n);
    final im = Float64List(n);
    final start = samples.length - n;
    for (var i = 0; i < n; i++) {
      re[i] = samples[start + i] * w[i];
    }
    fft(re, im);
    // 窓（ハン窓）の分を戻して、正弦波の振幅にそろえる
    final amp = Float64List(n ~/ 2 + 1);
    for (var i = 0; i < amp.length; i++) {
      amp[i] = math.sqrt(re[i] * re[i] + im[i] * im[i]) * 4 / n;
    }
    return Spectrum(sampleRate: sampleRate, size: n, amplitude: amp);
  }

  final double sampleRate;
  final int size;
  final Float64List amplitude;

  double get binHz => sampleRate / size;
  double frequencyOf(int bin) => bin * binHz;

  /// 振幅のデシベル（0 dB が最大。小さすぎる値は -120）
  static double toDb(double amp) =>
      amp <= 1e-6 ? -120 : 20 * math.log(amp) / math.ln10;

  double dbAt(int bin) => toDb(amplitude[bin]);

  /// [hz] 付近（±[toleranceHz]）でいちばん強い山の振幅
  double peakNear(double hz, {double? toleranceHz}) {
    final tol = toleranceHz ?? math.max(binHz * 1.5, hz * 0.03);
    final lo = ((hz - tol) / binHz).floor().clamp(1, amplitude.length - 1);
    final hi = ((hz + tol) / binHz).ceil().clamp(1, amplitude.length - 1);
    var best = 0.0;
    for (var i = lo; i <= hi; i++) {
      if (amplitude[i] > best) best = amplitude[i];
    }
    return best;
  }

  /// 音の重心（Hz）。[minHz]〜[maxHz] で、振幅で重みを付けた周波数の平均（明るさの目安）
  double centroid({double minHz = 60, double maxHz = 8000}) {
    var num = 0.0, den = 0.0;
    final lo = (minHz / binHz).ceil();
    final hi = math.min((maxHz / binHz).floor(), amplitude.length - 1);
    for (var i = lo; i <= hi; i++) {
      num += frequencyOf(i) * amplitude[i];
      den += amplitude[i];
    }
    return den == 0 ? 0 : num / den;
  }
}

/// いくつかのスペクトラムの平均（録音全体のまとめ用。振幅の二乗で平均する）
class SpectrumAverager {
  Float64List? _power;
  double _sampleRate = 0;
  int _size = 0;
  int count = 0;

  void add(Spectrum s) {
    final p = _power ??= Float64List(s.amplitude.length);
    if (p.length != s.amplitude.length) return;
    _sampleRate = s.sampleRate;
    _size = s.size;
    for (var i = 0; i < p.length; i++) {
      p[i] += s.amplitude[i] * s.amplitude[i];
    }
    count++;
  }

  Spectrum? get average {
    final p = _power;
    if (p == null || count == 0) return null;
    return Spectrum(
      sampleRate: _sampleRate,
      size: _size,
      amplitude: Float64List.fromList([
        for (final v in p) math.sqrt(v / count),
      ]),
    );
  }
}

/// 倍音のバランス（音色メーター）
class HarmonicProfile {
  const HarmonicProfile({
    required this.fundamental,
    required this.levelsDb,
    required this.brightness,
  });

  /// [spectrum] から、基音 [f0] の1〜[count]倍音の強さを測る
  factory HarmonicProfile.of(Spectrum spectrum, double f0, {int count = 8}) {
    final nyquist = spectrum.sampleRate / 2;
    final amps = [
      for (var k = 1; k <= count; k++)
        k * f0 < nyquist * 0.95 ? spectrum.peakNear(k * f0) : 0.0,
    ];
    final ref = amps.first <= 0 ? amps.reduce(math.max) : amps.first;
    var num = 0.0, den = 0.0;
    for (var k = 0; k < amps.length; k++) {
      num += (k + 1) * amps[k] * amps[k];
      den += amps[k] * amps[k];
    }
    return HarmonicProfile(
      fundamental: f0,
      levelsDb: [
        for (final a in amps)
          ref <= 0 ? -60.0 : math.max(-60.0, Spectrum.toDb(a / ref)),
      ],
      brightness: den == 0 ? 1 : num / den,
    );
  }

  final double fundamental;

  /// 基音を 0 dB としたときの、各倍音の強さ（[0] が基音。-60 dB で打ち止め）
  final List<double> levelsDb;

  /// 明るさの目安：エネルギーで重みを付けた倍音の番号の平均（1 なら基音だけ）
  final double brightness;

  /// ことばでの説明（よい・悪いではなく、音の傾向）
  String get description => brightness >= 3
      ? '高い倍音が多い、明るく輝かしい音'
      : brightness >= 2
      ? '倍音のバランスがよい、ふつうの響き'
      : '基音が中心の、柔らかく丸い音';
}
