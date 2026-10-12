/// 録音の簡易音響分析（決定論的。AI は使わない）
///
/// ロングトーンを想定し、短い区間（フレーム）ごとに音の高さと大きさを測って、
/// 音程のゆれ・上ずり／下がり・音量のゆれ・立ち上がりをまとめる。
library;

import 'dart:math' as math;
import 'dart:typed_data';

import '../../audio_tools/domain/pitch.dart';
import '../../audio_tools/domain/pitch_detector.dart';

class ToneFrame {
  const ToneFrame({required this.time, required this.rms, this.frequency});

  /// 録音の始めからの時刻（秒）
  final double time;
  final double rms;

  /// 音の高さが測れなかった（無音・雑音）ときは null
  final double? frequency;
}

/// 評価の段階（表示用）
enum Grade { good, fair, needsWork }

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
  });

  final List<ToneFrame> frames;

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
      for (final s in frame) {
        sumSq += s * s;
      }
      final e = _detector.detect(frame);
      frames.add(
        ToneFrame(
          time: (_consumed + frameSize / 2) / sampleRate,
          rms: math.sqrt(sumSq / frameSize),
          frequency: e?.frequency,
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
  return ToneAnalysis(
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
