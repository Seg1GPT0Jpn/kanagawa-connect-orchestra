/// チューナーで測った音程の記録と統計（決定論的）
///
/// 演奏しながら、測れた区間（フレーム）ごとに「どの音を・目標から何セントずれて」吹いたかを
/// 音名（実音の MIDI 番号）ごとに集める。苦手な音の抽出・セッションの比較に使う。
library;

import 'dart:math' as math;

/// 1つの音の統計
class NoteStat {
  NoteStat(this.midi);

  final int midi;
  int frames = 0;
  int inTuneFrames = 0;

  /// 範囲より低かった・高かったフレーム
  int lowFrames = 0;
  int highFrames = 0;
  double sumCents = 0;
  double sumSquares = 0;

  void add(double cents, {required double tolerance}) {
    frames++;
    if (cents.abs() <= tolerance) {
      inTuneFrames++;
    } else if (cents < 0) {
      lowFrames++;
    } else {
      highFrames++;
    }
    sumCents += cents;
    sumSquares += cents * cents;
  }

  /// 平均のずれ（セント。正なら高め）
  double get meanCents => frames == 0 ? 0 : sumCents / frames;

  /// ばらつき（標準偏差・セント）
  double get spreadCents {
    if (frames < 2) return 0;
    final m = meanCents;
    return math.sqrt(math.max(0, sumSquares / frames - m * m));
  }

  /// 合っていた割合（0〜1）
  double get inTuneRatio => frames == 0 ? 0 : inTuneFrames / frames;

  Map<String, Object?> toMap() => {
    'midi': midi,
    'frames': frames,
    'inTune': inTuneFrames,
    'low': lowFrames,
    'high': highFrames,
    'sum': sumCents,
    'sumSq': sumSquares,
  };

  factory NoteStat.fromMap(Map<Object?, Object?> m) =>
      NoteStat((m['midi']! as num).toInt())
        ..frames = (m['frames']! as num).toInt()
        ..inTuneFrames = (m['inTune']! as num).toInt()
        ..lowFrames = ((m['low'] as num?) ?? 0).toInt()
        ..highFrames = ((m['high'] as num?) ?? 0).toInt()
        ..sumCents = (m['sum']! as num).toDouble()
        ..sumSquares = (m['sumSq']! as num).toDouble();
}

/// 音程の分布の目盛り（-50〜+50 セントを 5 セントずつ。端はそれより外も含む）
const histogramStep = 5;
const histogramBuckets = 21;

int histogramIndex(double cents) =>
    ((cents / histogramStep).round() + histogramBuckets ~/ 2).clamp(
      0,
      histogramBuckets - 1,
    );

/// 1回の練習（チューナーを使った間）の統計
class PitchStats {
  PitchStats({required this.frameSeconds, required this.tolerance});

  /// 1フレームの長さ（秒）
  final double frameSeconds;

  /// 「合っている」とみなす範囲（±セント）
  final double tolerance;
  final Map<int, NoteStat> notes = {};
  final List<int> histogram = List.filled(histogramBuckets, 0);

  void add(int midi, double cents) {
    notes
        .putIfAbsent(midi, () => NoteStat(midi))
        .add(cents, tolerance: tolerance);
    histogram[histogramIndex(cents)]++;
  }

  int get frames => notes.values.fold(0, (a, n) => a + n.frames);
  int get inTuneFrames => notes.values.fold(0, (a, n) => a + n.inTuneFrames);
  double get seconds => frames * frameSeconds;
  double secondsOf(NoteStat n) => n.frames * frameSeconds;
  double get inTuneRatio => frames == 0 ? 0 : inTuneFrames / frames;

  /// 低め・合っている・高めの割合
  ({double low, double inTune, double high}) get balance {
    final total = frames;
    if (total == 0) return (low: 0, inTune: 0, high: 0);
    return (
      low: notes.values.fold(0, (a, n) => a + n.lowFrames) / total,
      inTune: inTuneFrames / total,
      high: notes.values.fold(0, (a, n) => a + n.highFrames) / total,
    );
  }

  /// 苦手な音：[minSeconds] 秒以上吹いた音のうち、合っていた割合が低い順（最大 [limit] 個）
  List<NoteStat> weakNotes({double minSeconds = 2, int limit = 3}) {
    final candidates = [
      for (final n in notes.values)
        if (secondsOf(n) >= minSeconds && n.inTuneRatio < 0.6) n,
    ]..sort((a, b) => a.inTuneRatio.compareTo(b.inTuneRatio));
    return candidates.take(limit).toList();
  }

  Map<String, Object?> toMap() => {
    'frameSeconds': frameSeconds,
    'tolerance': tolerance,
    'notes': [for (final n in notes.values) n.toMap()],
    'histogram': histogram,
  };

  factory PitchStats.fromMap(Map<Object?, Object?> m) {
    final s = PitchStats(
      frameSeconds: (m['frameSeconds']! as num).toDouble(),
      tolerance: (m['tolerance']! as num).toDouble(),
    );
    for (final raw in (m['notes'] as List?) ?? const []) {
      final n = NoteStat.fromMap(raw as Map);
      s.notes[n.midi] = n;
    }
    final h = m['histogram'];
    if (h is List && h.length == histogramBuckets) {
      for (var i = 0; i < histogramBuckets; i++) {
        s.histogram[i] = (h[i] as num).toInt();
      }
    }
    return s;
  }
}

/// 保存する1回分（チューナーを「はじめる」から「止める」まで）
class TunerSession {
  const TunerSession({
    required this.id,
    required this.startedAtMillis,
    required this.durationSeconds,
    required this.a4,
    required this.temperamentLabel,
    required this.stats,
  });

  final String id;
  final int startedAtMillis;

  /// チューナーを使っていた時間（秒）
  final double durationSeconds;
  final double a4;

  /// そのときの音律（主音つき。表示用）
  final String temperamentLabel;
  final PitchStats stats;

  Map<String, Object?> toMap() => {
    'id': id,
    'startedAt': startedAtMillis,
    'duration': durationSeconds,
    'a4': a4,
    'temperament': temperamentLabel,
    'stats': stats.toMap(),
  };

  factory TunerSession.fromMap(Map<Object?, Object?> m) => TunerSession(
    id: m['id']! as String,
    startedAtMillis: (m['startedAt']! as num).toInt(),
    durationSeconds: (m['duration']! as num).toDouble(),
    a4: (m['a4']! as num).toDouble(),
    temperamentLabel: (m['temperament'] as String?) ?? '',
    stats: PitchStats.fromMap(m['stats']! as Map),
  );
}

/// 2回の練習の、音ごとの比べ（両方で吹いた音だけ）
class NoteComparison {
  const NoteComparison(this.midi, this.before, this.after);

  final int midi;
  final NoteStat before;
  final NoteStat after;

  /// 合っていた割合の変化（正ならよくなった）
  double get inTuneChange => after.inTuneRatio - before.inTuneRatio;
}

List<NoteComparison> compareSessions(PitchStats before, PitchStats after) => [
  for (final midi in (after.notes.keys.toList()..sort()))
    if (before.notes[midi] case final b?)
      NoteComparison(midi, b, after.notes[midi]!),
];

/// いくつかの練習の統計をまとめる（期間ごとの傾向を見る）
PitchStats mergeStats(Iterable<PitchStats> all, {required double tolerance}) {
  final out = PitchStats(frameSeconds: 0, tolerance: tolerance);
  var seconds = 0.0;
  var frames = 0;
  for (final s in all) {
    seconds += s.seconds;
    frames += s.frames;
    for (final n in s.notes.values) {
      final m = out.notes.putIfAbsent(n.midi, () => NoteStat(n.midi));
      m.frames += n.frames;
      m.inTuneFrames += n.inTuneFrames;
      m.lowFrames += n.lowFrames;
      m.highFrames += n.highFrames;
      m.sumCents += n.sumCents;
      m.sumSquares += n.sumSquares;
    }
    for (var i = 0; i < histogramBuckets; i++) {
      out.histogram[i] += s.histogram[i];
    }
  }
  // 1フレームの長さは、合計の時間とフレーム数から
  return PitchStats(
      frameSeconds: frames == 0 ? 0 : seconds / frames,
      tolerance: tolerance,
    )
    ..notes.addAll(out.notes)
    ..histogram.setAll(0, out.histogram);
}
