import '../practice/domain/practice_record.dart';

/// 同じ記録の2つの版のうち、どちらを残すかを決める（どの端末で計算しても同じ結果になる）
///
/// 1. 後から編集した方（updatedAt が大きい方）
/// 2. 同じ時刻なら、編集した端末 ID が大きい方
/// 3. それも同じなら、削除済みの方（削除を優先して、消したはずの記録が復活しないように）
/// 4. まったく同じなら [remote]
///
/// ※ 端末の時計がずれていると、古い編集が勝つことがある（練習記録では許容する）
PracticeRecord resolveConflict(PracticeRecord local, PracticeRecord remote) {
  if (local.updatedAtMillis != remote.updatedAtMillis) {
    return local.updatedAtMillis > remote.updatedAtMillis ? local : remote;
  }
  final byDevice = local.updatedBy.compareTo(remote.updatedBy);
  if (byDevice != 0) return byDevice > 0 ? local : remote;
  if (local.deleted != remote.deleted) return local.deleted ? local : remote;
  return remote;
}
