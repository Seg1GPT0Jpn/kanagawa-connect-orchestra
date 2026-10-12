import 'tone_analysis.dart';

/// 保存する分析結果（音声そのものは保存しない）
class RecordingResult {
  const RecordingResult({
    required this.id,
    required this.recordedAtMillis,
    required this.durationSeconds,
    required this.voicedSeconds,
    required this.midi,
    required this.centsOffset,
    required this.pitchSpreadCents,
    required this.driftCents,
    required this.volumeSpreadDb,
    required this.attackSeconds,
    required this.a4,
    this.memo = '',
    this.reliability,
  });

  factory RecordingResult.fromAnalysis(
    String id,
    ToneAnalysis a, {
    required DateTime recordedAt,
    required double a4,
    String memo = '',
  }) => RecordingResult(
    id: id,
    recordedAtMillis: recordedAt.millisecondsSinceEpoch,
    durationSeconds: a.duration,
    voicedSeconds: a.voicedSeconds,
    midi: a.midi,
    centsOffset: a.centsOffset,
    pitchSpreadCents: a.pitchSpreadCents,
    driftCents: a.driftCents,
    volumeSpreadDb: a.volumeSpreadDb,
    attackSeconds: a.attackSeconds,
    a4: a4,
    memo: memo,
    reliability: a.reliability,
  );

  final String id;
  final int recordedAtMillis;
  final double durationSeconds;
  final double voicedSeconds;

  /// 実音
  final int midi;
  final double centsOffset;
  final double pitchSpreadCents;
  final double driftCents;
  final double volumeSpreadDb;
  final double attackSeconds;

  /// そのときの基準ピッチ
  final double a4;
  final String memo;

  /// 分析の信頼度の目安（古い記録にはない）
  final Reliability? reliability;

  Map<String, Object?> toMap() => {
    'id': id,
    'recordedAt': recordedAtMillis,
    'duration': durationSeconds,
    'voiced': voicedSeconds,
    'midi': midi,
    'centsOffset': centsOffset,
    'pitchSpread': pitchSpreadCents,
    'drift': driftCents,
    'volumeSpread': volumeSpreadDb,
    'attack': attackSeconds,
    'a4': a4,
    'memo': memo,
    if (reliability != null) 'reliability': reliability!.name,
  };

  factory RecordingResult.fromMap(Map<String, Object?> m) {
    double d(String k) => (m[k]! as num).toDouble();
    return RecordingResult(
      id: m['id']! as String,
      recordedAtMillis: (m['recordedAt']! as num).toInt(),
      durationSeconds: d('duration'),
      voicedSeconds: d('voiced'),
      midi: (m['midi']! as num).toInt(),
      centsOffset: d('centsOffset'),
      pitchSpreadCents: d('pitchSpread'),
      driftCents: d('drift'),
      volumeSpreadDb: d('volumeSpread'),
      attackSeconds: d('attack'),
      a4: d('a4'),
      memo: (m['memo'] as String?) ?? '',
      reliability: Reliability.byName(m['reliability']),
    );
  }
}
