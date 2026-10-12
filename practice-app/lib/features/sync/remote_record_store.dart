import '../practice/domain/practice_record.dart';

class RemoteChanges {
  const RemoteChanges(this.records, this.latestServerMillis);

  final List<PracticeRecord> records;

  /// 取得した記録のうち、クラウドに書き込まれた時刻がいちばん新しいもの（次回の取得位置）
  final int? latestServerMillis;
}

/// クラウド側の練習記録（Firestore。テストでは端末内の偽物に差し替える）
abstract interface class RemoteRecordStore {
  /// [cursorMillis] 以降にクラウドで書き込まれた記録（null なら全部）
  Future<RemoteChanges> fetchChangedSince(String uid, int? cursorMillis);

  /// [record] がクラウドの版より新しければ書き込む。残った方の版を返す
  Future<PracticeRecord> pushIfNewer(String uid, PracticeRecord record);
}
