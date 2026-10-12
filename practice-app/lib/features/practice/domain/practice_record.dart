/// 練習記録（端末内とクラウドで同じ形で保存する）
library;

class PracticeRecord {
  const PracticeRecord({
    required this.id,
    required this.ownerUid,
    required this.practicedOn,
    required this.startedAtMillis,
    required this.ruleSetId,
    required this.plannedMinutes,
    required this.actualSeconds,
    required this.note,
    required this.updatedAtMillis,
    required this.updatedBy,
    required this.deleted,
  });

  final String id;

  /// 持ち主のアカウント（ログイン前に作った記録は null。最初にログインしたアカウントに引き継ぐ）
  final String? ownerUid;

  /// 練習した日（端末のローカル日付 yyyy-MM-dd）
  final String practicedOn;
  final int startedAtMillis;

  /// 使ったメニューのルール（例：trumpet_basic）
  final String ruleSetId;

  /// 予定（項目 id → 分）
  final Map<String, int> plannedMinutes;

  /// 実際に練習した時間（項目 id → 秒）
  final Map<String, int> actualSeconds;
  final String note;

  /// 最後に編集した時刻（端末の時計）。同期の競合はこれで決める
  final int updatedAtMillis;

  /// 最後に編集した端末の ID（時刻が同じときの決め手）
  final String updatedBy;

  /// 削除済み（同期のため、消さずに印を付けておく）
  final bool deleted;

  int get totalActualSeconds => actualSeconds.values.fold(0, (s, v) => s + v);

  PracticeRecord copyWith({
    String? ownerUid,
    Map<String, int>? actualSeconds,
    String? note,
    int? updatedAtMillis,
    String? updatedBy,
    bool? deleted,
  }) => PracticeRecord(
    id: id,
    ownerUid: ownerUid ?? this.ownerUid,
    practicedOn: practicedOn,
    startedAtMillis: startedAtMillis,
    ruleSetId: ruleSetId,
    plannedMinutes: plannedMinutes,
    actualSeconds: actualSeconds ?? this.actualSeconds,
    note: note ?? this.note,
    updatedAtMillis: updatedAtMillis ?? this.updatedAtMillis,
    updatedBy: updatedBy ?? this.updatedBy,
    deleted: deleted ?? this.deleted,
  );

  Map<String, Object?> toMap() => {
    'id': id,
    'ownerUid': ownerUid,
    'practicedOn': practicedOn,
    'startedAt': startedAtMillis,
    'ruleSetId': ruleSetId,
    'plannedMinutes': plannedMinutes,
    'actualSeconds': actualSeconds,
    'note': note,
    'updatedAt': updatedAtMillis,
    'updatedBy': updatedBy,
    'deleted': deleted,
  };

  factory PracticeRecord.fromMap(Map<String, Object?> m) => PracticeRecord(
    id: m['id']! as String,
    ownerUid: m['ownerUid'] as String?,
    practicedOn: m['practicedOn']! as String,
    startedAtMillis: (m['startedAt']! as num).toInt(),
    ruleSetId: m['ruleSetId']! as String,
    plannedMinutes: _intMap(m['plannedMinutes']),
    actualSeconds: _intMap(m['actualSeconds']),
    note: (m['note'] as String?) ?? '',
    updatedAtMillis: (m['updatedAt']! as num).toInt(),
    updatedBy: m['updatedBy']! as String,
    deleted: (m['deleted'] as bool?) ?? false,
  );

  static Map<String, int> _intMap(Object? v) => {
    for (final MapEntry(:key, :value) in ((v ?? const {}) as Map).entries)
      key as String: (value as num).toInt(),
  };

  @override
  bool operator ==(Object other) =>
      other is PracticeRecord && _mapEquals(other.toMap(), toMap());

  @override
  int get hashCode => Object.hash(id, updatedAtMillis, updatedBy);

  @override
  String toString() =>
      'PracticeRecord($id, $practicedOn, updated $updatedAtMillis by $updatedBy${deleted ? ', deleted' : ''})';
}

bool _mapEquals(Map a, Map b) {
  if (a.length != b.length) return false;
  for (final k in a.keys) {
    final x = a[k], y = b[k];
    if (x is Map && y is Map) {
      if (!_mapEquals(x, y)) return false;
    } else if (x != y) {
      return false;
    }
  }
  return true;
}
