import 'package:cloud_firestore/cloud_firestore.dart';

import '../practice/domain/practice_record.dart';
import 'conflict.dart';
import 'remote_record_store.dart';

/// Firestore の users/{uid}/practiceRecords/{recordId}
class FirestoreRemoteRecordStore implements RemoteRecordStore {
  FirestoreRemoteRecordStore(this._firestore);

  final FirebaseFirestore _firestore;
  static const _pageSize = 200;

  CollectionReference<Map<String, dynamic>> _col(String uid) =>
      _firestore.collection('users').doc(uid).collection('practiceRecords');

  @override
  Future<RemoteChanges> fetchChangedSince(String uid, int? cursorMillis) async {
    // 同じ時刻の書き込みを取りこぼさないよう「以降（>=）」で取る。重なった分は取り込んでも結果が変わらない
    var query = _col(uid).orderBy('serverUpdatedAt');
    if (cursorMillis != null) {
      query = query.where(
        'serverUpdatedAt',
        isGreaterThanOrEqualTo: Timestamp.fromMillisecondsSinceEpoch(
          cursorMillis,
        ),
      );
    }
    final records = <PracticeRecord>[];
    int? latest;
    DocumentSnapshot? last;
    while (true) {
      var page = query.limit(_pageSize);
      if (last != null) page = page.startAfterDocument(last);
      final snap = await page.get(const GetOptions(source: Source.server));
      for (final doc in snap.docs) {
        final data = doc.data();
        final serverMillis = (data.remove(
          'serverUpdatedAt',
        ) as Timestamp).millisecondsSinceEpoch;
        records.add(PracticeRecord.fromMap(data));
        if (latest == null || serverMillis > latest) latest = serverMillis;
      }
      if (snap.docs.length < _pageSize) break;
      last = snap.docs.last;
    }
    return RemoteChanges(records, latest);
  }

  @override
  Future<PracticeRecord> pushIfNewer(String uid, PracticeRecord record) {
    final ref = _col(uid).doc(record.id);
    return _firestore.runTransaction((tx) async {
      final snap = await tx.get(ref);
      final data = snap.data();
      if (data != null) {
        data.remove('serverUpdatedAt');
        final remote = PracticeRecord.fromMap(data);
        if (identical(resolveConflict(record, remote), remote)) return remote;
      }
      tx.set(ref, {
        ...record.toMap(),
        'serverUpdatedAt': FieldValue.serverTimestamp(),
      });
      return record;
    });
  }
}
