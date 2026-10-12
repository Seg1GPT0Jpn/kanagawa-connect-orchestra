/// 録音の簡易音響分析（決定論的。AI は使わない）
///
/// ロングトーンを想定し、短い区間（フレーム）ごとに音の高さと大きさを測って、
/// 音程のゆれ・上ずり／下がり・音量のゆれ・立ち上がりをまとめる。
library;

import 'dart:math' as math;
import 'dart:typed_data';

import '../../audio_tools/domain/pitch.dart';
import '../../audio_tools/domain/pitch_detector.dart';
import '../../audio_tools/domain/spectrum.dart';

class ToneFrame {
  const ToneFrame({
    required this.time,
    required this.rms,
    this.frequency,
    this.peak = 0,
    this.clarity = 0,
  });

  /// 録音の始めからの時刻（秒）
  final double time;
  final double rms;

  /// 波形のいちばん大きな値（音割れの確認用）
  final double peak;

  /// 高さの測りやすさ（0〜1。周期がはっきりしているほど 1 に近い）
  final double clarity;

  /// 音の高さが測れなかった（無音・雑音）ときは null
  final double? frequency;
}

/// 評価の段階（表示用）
enum Grade { good, fair, needsWork }

/// 分析結果の信頼度の目安
enum Reliability {
  high('高い'),
  medium('ふつう'),
  low('低い');

  const Reliability(this.label);
  final String label;

  static Reliability? byName(Object? name) {
    for (final r in values) {
      if (r.name == name) return r;
    }
    return null;
  }
}

/// 高さを測れなかった区間（秒）
typedef Gap = ({double start, double end});

class ToneAnalysis {
  const ToneAnalysis({
    required this.frames,
    required this.duration,
    required this.voicedSeconds,
    required this.medianFrequency,
    required this.midi,
    required this.centsOffset,
    required this.pitchSpreadCents,
    required this.driftCents,
    required this.volumeSpreadDb,
    required this.attackSeconds,
    this.reliability = Reliability.high,
    this.reliabilityNotes = const [],
    this.gaps = const [],
    this.levelDb = 0,
    this.spectrum,
    this.harmonics,
  });

  /// 鳴っていた区間の平均のスペクトラム
  final Spectrum? spectrum;

  /// 平均の倍音のバランス
  final HarmonicProfile? harmonics;

  final List<ToneFrame> frames;

  /// 信頼度の目安と、その理由（録り方の注意）
  final Reliability reliability;
  final List<String> reliabilityNotes;

  /// 鳴っている途中で、高さを測れなかった区間
  final List<Gap> gaps;

  /// 鳴っていた区間の音の大きさ（dBFS。0 が最大）
  final double levelDb;

  /// 録音の長さ（秒）
  final double duration;

  /// 音が鳴っていた（高さが測れた）時間（秒）
  final double voicedSeconds;

  /// 音の高さの中央値（Hz）
  final double medianFrequency;

  /// いちばん近い音（実音）と、そこからのずれ（セント）
  final int midi;
  final double centsOffset;

  /// 音程のゆれ：中央値からのずれの標準偏差（セント）
  final double pitchSpreadCents;

  /// 音程の変化：終わりの1/3の中央値 − 始めの1/3の中央値（セント。正なら上ずった）
  final double driftCents;

  /// 音量のゆれ：鳴っていた区間の音量（dB）の標準偏差
  final double volumeSpreadDb;

  /// 立ち上がり：鳴り始めから、音量が安定した大きさ（中央値の90%）に届くまで（秒）
  final double attackSeconds;

  Grade get pitchGrade => pitchSpreadCents <= 5
      ? Grade.good
      : pitchSpreadCents <= 12
      ? Grade.fair
      : Grade.needsWork;
  Grade get driftGrade => driftCents.abs() <= 5
      ? Grade.good
      : driftCents.abs() <= 15
      ? Grade.fair
      : Grade.needsWork;
  Grade get volumeGrade => volumeSpreadDb <= 1.5
      ? Grade.good
      : volumeSpreadDb <= 3
      ? Grade.fair
      : Grade.needsWork;
  Grade get attackGrade => attackSeconds <= 0.15
      ? Grade.good
      : attackSeconds <= 0.4
      ? Grade.fair
      : Grade.needsWork;
}

/// 録音しながら少しずつフレームを測る（録り終えてからまとめて計算すると、長い録音で画面が固まるため）
class ToneFrameAnalyzer {
  ToneFrameAnalyzer({
    required this.sampleRate,
    this.frameSize = 1024,
    this.hopSize = 256,
  }) : _detector = PitchDetector(sampleRate: sampleRate);

  final double sampleRate;

  /// 約46ミリ秒の区間を約12ミリ秒ずつずらす（ビブラート程度の速いゆれも追える長さ）
  final int frameSize;
  final int hopSize;
  final PitchDetector _detector;
  final List<ToneFrame> frames = [];
  final SpectrumAverager _spectrum = SpectrumAverager();
  final List<double> _pending = [];
  int _consumed = 0;

  /// 受け取ったサンプルの数
  int samplesSeen = 0;

  void add(Float64List samples) {
    samplesSeen += samples.length;
    _pending.addAll(samples);
    while (_pending.length >= frameSize) {
      final frame = Float64List.fromList(_pending.sublist(0, frameSize));
      var sumSq = 0.0;
      var peak = 0.0;
      for (final s in frame) {
        sumSq += s * s;
        if (s.abs() > peak) peak = s.abs();
      }
      final e = _detector.detect(frame);
      if (e != null) _spectrum.add(Spectrum.of(frame, sampleRate: sampleRate));
      frames.add(
        ToneFrame(
          time: (_consumed + frameSize / 2) / sampleRate,
          rms: math.sqrt(sumSq / frameSize),
          frequency: e?.frequency,
          peak: peak,
          clarity: e?.clarity ?? 0,
        ),
      );
      _pending.removeRange(0, hopSize);
      _consumed += hopSize;
    }
  }

  ToneAnalysis? summarize({double a4 = 440}) => summarizeFrames(
    frames,
    hopSeconds: hopSize / sampleRate,
    duration: samplesSeen / sampleRate,
    a4: a4,
    spectrum: _spectrum.average,
  );
}

/// [samples]（-1〜1、[sampleRate] Hz）をまとめて分析する。音の高さが測れた区間が短すぎれば null
ToneAnalysis? analyzeTone(
  Float64List samples, {
  required double sampleRate,
  double a4 = 440,
}) =>
    (ToneFrameAnalyzer(sampleRate: sampleRate)..add(samples)).summarize(a4: a4);

/// フレームの結果をまとめる
ToneAnalysis? summarizeFrames(
  List<ToneFrame> frames, {
  required double hopSeconds,
  required double duration,
  double a4 = 440,
  Spectrum? spectrum,
}) {
  final voiced = [
    for (final f in frames)
      if (f.frequency != null) f,
  ];
  if (voiced.length * hopSeconds < 0.3) return null; // 0.3秒未満は分析しない

  final median = _median([for (final f in voiced) f.frequency!]);
  final cents = [for (final f in voiced) centsBetween(f.frequency!, median)];
  // 音の出だし・終わりの不安定な部分と、オクターブを外したような大きな外れ値は除く
  final core = [
    for (final c in cents)
      if (c.abs() <= 100) c,
  ];
  final spread = _std(core);

  final third = voiced.length ~/ 3;
  final drift = third == 0
      ? 0.0
      : centsBetween(
          _median([
            for (final f in voiced.sublist(voiced.length - third)) f.frequency!,
          ]),
          _median([for (final f in voiced.sublist(0, third)) f.frequency!]),
        );

  final dbs = [for (final f in voiced) 20 * math.log(f.rms) / math.ln10];
  // 立ち上がりと消え際を除いた真ん中の 80% で音量のゆれを見る
  final cut = (dbs.length * 0.1).floor();
  final middle = dbs.sublist(cut, dbs.length - cut);
  final volumeSpread = _std(middle.isEmpty ? dbs : middle);

  final steadyRms = _median([for (final f in voiced) f.rms]);
  final onset = voiced.first.time;
  final reached = voiced
      .firstWhere((f) => f.rms >= steadyRms * 0.9, orElse: () => voiced.first)
      .time;

  final reading = PitchReading.fromFrequency(median, a4: a4);
  final gaps = findGaps(frames);
  final check = assessReliability(
    frames,
    voiced: voiced,
    gaps: gaps,
    voicedSeconds: voiced.length * hopSeconds,
    outlierRatio: 1 - core.length / cents.length,
  );
  return ToneAnalysis(
    reliability: check.level,
    reliabilityNotes: check.notes,
    gaps: gaps,
    levelDb: check.levelDb,
    spectrum: spectrum,
    harmonics: spectrum == null ? null : HarmonicProfile.of(spectrum, median),
    frames: frames,
    duration: duration,
    voicedSeconds: voiced.length * hopSeconds,
    medianFrequency: median,
    midi: reading.midi,
    centsOffset: reading.cents,
    pitchSpreadCents: spread,
    driftCents: drift,
    volumeSpreadDb: volumeSpread,
    attackSeconds: math.max(0, reached - onset),
  );
}

/// 鳴り始めから鳴り終わりまでの間で、0.1秒以上続けて高さを測れなかった区間
List<Gap> findGaps(List<ToneFrame> frames, {double minSeconds = 0.1}) {
  final first = frames.indexWhere((f) => f.frequency != null);
  final last = frames.lastIndexWhere((f) => f.frequency != null);
  if (first < 0) return const [];
  final gaps = <Gap>[];
  int? start;
  for (var i = first; i <= last; i++) {
    final missing = frames[i].frequency == null;
    if (missing) {
      start ??= i;
    } else if (start != null) {
      final g = (start: frames[start].time, end: frames[i].time);
      if (g.end - g.start >= minSeconds) gaps.add(g);
      start = null;
    }
  }
  return gaps;
}

double _db(double rms) => 20 * math.log(math.max(rms, 1e-9)) / math.ln10;

/// 分析の信頼度の目安（決定論的）。録った条件の問題を、理由として返す
({Reliability level, List<String> notes, double levelDb}) assessReliability(
  List<ToneFrame> frames, {
  required List<ToneFrame> voiced,
  required List<Gap> gaps,
  required double voicedSeconds,
  required double outlierRatio,
}) {
  var level = Reliability.high;
  final notes = <String>[];
  void lower(Reliability to, String note) {
    if (to.index > level.index) level = to;
    notes.add(note);
  }

  final levelDb = _db(_median([for (final f in voiced) f.rms]));
  // 高さを測る下限は -40 dB。それに近いと、途切れたり雑音に負けたりしやすい
  if (levelDb < -36) {
    lower(Reliability.low, '音がとても小さく入っています。マイクに少し近づいてください');
  } else if (levelDb < -30) {
    lower(Reliability.medium, '音が小さめに入っています。マイクから 30〜50cm くらいで吹いてください');
  }

  final clipped = voiced.where((f) => f.peak >= 0.99).length / voiced.length;
  if (clipped > 0.1) {
    lower(Reliability.low, '音が割れています。マイクから離れるか、少し小さめに吹いてください');
  } else if (clipped > 0.02) {
    lower(Reliability.medium, 'ところどころ音が割れています。マイクから少し離れてください');
  }

  // 鳴っていない区間の大きさ＝周りの音
  final quiet = [
    for (final f in frames)
      if (f.frequency == null) f.rms,
  ];
  if (quiet.length >= 5) {
    final snr = levelDb - _db(_median(quiet));
    if (snr < 8) {
      lower(Reliability.low, '周りの音（雑音・反響）が大きく、楽器の音と区別しにくい状態です');
    } else if (snr < 15) {
      lower(Reliability.medium, '周りの音が少し入っています。静かな場所で録ると確かになります');
    }
  }

  if (voiced.length >= 2) {
    final span = voiced.last.time - voiced.first.time;
    final missing = gaps.fold<double>(0, (a, g) => a + g.end - g.start);
    final ratio = span <= 0 ? 0 : missing / span;
    if (ratio > 0.35) {
      lower(
        Reliability.low,
        '途中の ${(ratio * 100).round()}% で高さを測れませんでした（音のかすれ・雑音・大きなビブラートなど）',
      );
    } else if (ratio > 0.15) {
      lower(
        Reliability.medium,
        '途中の ${(ratio * 100).round()}% で高さを測れませんでした（グラフの灰色の部分）',
      );
    }
  }

  final clarity =
      voiced.fold<double>(0, (a, f) => a + f.clarity) / voiced.length;
  if (clarity > 0 && clarity < 0.8) {
    lower(Reliability.medium, '音の周期がはっきりしません（息の音・雑音が多い、音がかすれているなど）');
  }

  if (outlierRatio > 0.05) {
    lower(Reliability.medium, '高さを大きく取り違えた区間があります（オクターブ違いなど）');
  }

  if (voicedSeconds < 2) {
    lower(Reliability.medium, '鳴っていた時間が短めです。3秒以上伸ばすと確かになります');
  }
  return (level: level, notes: notes, levelDb: levelDb);
}

double _median(List<double> v) {
  final s = [...v]..sort();
  final m = s.length ~/ 2;
  return s.length.isOdd ? s[m] : (s[m - 1] + s[m]) / 2;
}

double _std(List<double> v) {
  if (v.length < 2) return 0;
  final mean = v.reduce((a, b) => a + b) / v.length;
  var sum = 0.0;
  for (final x in v) {
    sum += (x - mean) * (x - mean);
  }
  return math.sqrt(sum / v.length);
}

/// 結果をことばで（決定論的）
List<String> describeAnalysis(ToneAnalysis a) => [
  switch (a.pitchGrade) {
    Grade.good =>
      '音程がよく安定しています（ゆれ ±${a.pitchSpreadCents.toStringAsFixed(1)} セント）。',
    Grade.fair =>
      '音程が少しゆれています（±${a.pitchSpreadCents.toStringAsFixed(1)} セント）。息の量を一定に保ってみましょう。',
    Grade.needsWork =>
      '音程のゆれが大きめです（±${a.pitchSpreadCents.toStringAsFixed(1)} セント）。チューナーを見ながら、楽な音量で伸ばしてみましょう。',
  },
  switch (a.driftGrade) {
    Grade.good => '始めから終わりまで、音の高さが保てています。',
    _ when a.driftCents > 0 =>
      '終わりにかけて ${a.driftCents.toStringAsFixed(0)} セント上ずっています。',
    _ =>
      '終わりにかけて ${(-a.driftCents).toStringAsFixed(0)} セント下がっています。息の支えを最後まで保ちましょう。',
  },
  switch (a.volumeGrade) {
    Grade.good => '音量が安定しています（ゆれ ${a.volumeSpreadDb.toStringAsFixed(1)} dB）。',
    Grade.fair => '音量が少しゆれています（${a.volumeSpreadDb.toStringAsFixed(1)} dB）。',
    Grade.needsWork =>
      '音量のゆれが大きめです（${a.volumeSpreadDb.toStringAsFixed(1)} dB）。強弱をつける練習なら問題ありません。',
  },
  switch (a.attackGrade) {
    Grade.good => '音の出だしがはっきりしています。',
    Grade.fair => '音の出だしが少しゆっくりです（${a.attackSeconds.toStringAsFixed(2)} 秒）。',
    Grade.needsWork =>
      '音が安定するまでに時間がかかっています（${a.attackSeconds.toStringAsFixed(2)} 秒）。',
  },
];
