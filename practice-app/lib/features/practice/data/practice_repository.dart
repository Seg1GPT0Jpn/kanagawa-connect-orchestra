/// 練習記録を端末内に保存する（ログインしていなくても使える）
///
/// 同期のため、各記録に「まだクラウドに送っていない（dirty）」の印を持たせる。
library;

import 'dart:async';

import 'package:sembast/sembast.dart';

import '../../../core/clock.dart';
import '../../../core/ids.dart';
import '../../../core/meta_store.dart';
import '../../sync/conflict.dart';
import '../domain/practice_record.dart';

class PracticeRepository {
  PracticeRepository(
    this._db, {
    required this.deviceId,
    this.clock = systemClock,
  }) : _meta = MetaStore(_db);

  final Database _db;
  final MetaStore _meta;
  final Clock clock;
  final String deviceId;

  static final _store = stringMapStoreFactory.store('practice_records');
  static const _dirty = '_dirty';

  final _changes = StreamController<void>.broadcast();

  /// 端末内の記録が（ユーザーの操作で）変わったとき。同期のきっかけに使う
  Stream<void> get localChanges => _changes.stream;

  /// [uid] のアカウントで見える記録（自分の記録＋ログイン前に作った記録）。新しい順、削除済みは除く
  Stream<List<PracticeRecord>> watchVisible(String? uid) => _store
      .query(finder: Finder(sortOrders: [SortOrder('startedAt', false)]))
      .onSnapshots(_db)
      .map(
        (snaps) => [
          for (final s in snaps)
            if (_visible(s.value, uid)) PracticeRecord.fromMap(s.value),
        ],
      );

  Future<List<PracticeRecord>> visible(String? uid) async => [
    for (final s in await _store.find(
      _db,
      finder: Finder(sortOrders: [SortOrder('startedAt', false)]),
    ))
      if (_visible(s.value, uid)) PracticeRecord.fromMap(s.value),
  ];

  static bool _visible(Map<String, Object?> m, String? uid) =>
      m['deleted'] != true && (m['ownerUid'] == null || m['ownerUid'] == uid);

  Future<PracticeRecord?> get(String id) async {
    final m = await _store.record(id).get(_db);
    return m == null ? null : PracticeRecord.fromMap(m);
  }

  Future<bool> isDirty(String id) async =>
      (await _store.record(id).get(_db))?[_dirty] == true;

  /// 練習の結果を新しい記録として保存する
  Future<PracticeRecord> create({
    required String? ownerUid,
    required DateTime startedAt,
    required String ruleSetId,
    required Map<String, int> plannedMinutes,
    required Map<String, int> actualSeconds,
    String note = '',
  }) async {
    final record = PracticeRecord(
      id: generateId(),
      ownerUid: ownerUid,
      practicedOn: localDateString(startedAt),
      startedAtMillis: startedAt.millisecondsSinceEpoch,
      ruleSetId: ruleSetId,
      plannedMinutes: plannedMinutes,
      actualSeconds: actualSeconds,
      note: note,
      updatedAtMillis: clock().millisecondsSinceEpoch,
      updatedBy: deviceId,
      deleted: false,
    );
    await _putDirty(_db, record);
    _changes.add(null);
    return record;
  }

  Future<void> updateNote(String id, String note) =>
      _edit(id, (r) => r.copyWith(note: note));

  /// 削除（同期のため、記録は残して削除済みの印を付ける）
  Future<void> delete(String id) => _edit(id, (r) => r.copyWith(deleted: true));

  Future<void> _edit(
    String id,
    PracticeRecord Function(PracticeRecord) change,
  ) async {
    await _db.transaction((txn) async {
      final m = await _store.record(id).get(txn);
      if (m == null) return;
      final edited = change(PracticeRecord.fromMap(m)).copyWith(
        updatedAtMillis: clock().millisecondsSinceEpoch,
        updatedBy: deviceId,
      );
      await _putDirty(txn, edited);
    });
    _changes.add(null);
  }

  /// バックアップから記録を取り込む。持ち主は [uid] にそろえる（ほかの人の記録として入らないように）
  ///
  /// 端末にない記録は追加し、ある記録は同期と同じ決まり（後から編集した方）で残す。
  /// 取り込んで変わった記録は未送信にする（ログイン中なら次の同期で送る）。
  Future<({int added, int updated, int unchanged})> importRecords(
    List<PracticeRecord> records,
    String? uid,
  ) async {
    var added = 0, updated = 0, unchanged = 0;
    await _db.transaction((txn) async {
      for (final incoming in records) {
        final r = incoming.copyWith(ownerUid: uid);
        final m = await _store.record(r.id).get(txn);
        if (m == null) {
          await _putDirty(txn, r);
          added++;
          continue;
        }
        final local = PracticeRecord.fromMap(m);
        // 持ち主を除いて同じ内容なら何もしない
        if (local.copyWith(ownerUid: uid) == r ||
            identical(resolveConflict(local, r), local)) {
          unchanged++;
        } else {
          await _putDirty(txn, r);
          updated++;
        }
      }
    });
    if (added + updated > 0) _changes.add(null);
    return (added: added, updated: updated, unchanged: unchanged);
  }

  /// 書き出し用：[uid] で見える記録（削除済みを除く、古い順）
  Future<List<PracticeRecord>> exportable(String? uid) async =>
      (await visible(uid)).reversed.toList();

  // ---- 同期用 ----

  /// ログイン前に作った記録を [uid] のアカウントに引き継ぐ（次の同期で送る）
  Future<void> claimGuestRecords(String uid) async {
    await _db.transaction((txn) async {
      final guests = await _store.find(
        txn,
        finder: Finder(filter: Filter.isNull('ownerUid')),
      );
      for (final s in guests) {
        await _putDirty(
          txn,
          PracticeRecord.fromMap(s.value).copyWith(ownerUid: uid),
        );
      }
    });
  }

  /// まだクラウドに送っていない [uid] の記録
  Future<List<PracticeRecord>> dirtyRecordsFor(String uid) async => [
    for (final s in await _store.find(
      _db,
      finder: Finder(
        filter: Filter.and([
          Filter.equals(_dirty, true),
          Filter.equals('ownerUid', uid),
        ]),
      ),
    ))
      PracticeRecord.fromMap(s.value),
  ];

  /// クラウドの版 [remote] を取り込む
  ///
  /// [pushed] は、いま送った端末側の版（送った結果を取り込むとき）。
  /// 送っている間に端末で編集されていたら、その編集は消さずに競合を解決する。
  /// 戻り値：端末の内容が変わったか
  Future<bool> applyRemote(PracticeRecord remote, {PracticeRecord? pushed}) {
    return _db.transaction((txn) async {
      final m = await _store.record(remote.id).get(txn);
      if (m == null) {
        await _putClean(txn, remote);
        return true;
      }
      final local = PracticeRecord.fromMap(m);
      if (m[_dirty] != true || (pushed != null && local == pushed)) {
        await _putClean(txn, remote);
        return local != remote;
      }
      final winner = resolveConflict(local, remote);
      if (identical(winner, local)) return false; // 端末の版が新しい → 次に送る
      await _putClean(txn, remote);
      return true;
    });
  }

  Future<int?> syncCursor(String uid) async =>
      (await _meta.get('syncCursor.$uid')) as int?;
  Future<void> setSyncCursor(String uid, int millis) =>
      _meta.put('syncCursor.$uid', millis);

  static Future<void> _putDirty(DatabaseClient c, PracticeRecord r) =>
      _store.record(r.id).put(c, {...r.toMap(), _dirty: true});
  static Future<void> _putClean(DatabaseClient c, PracticeRecord r) =>
      _store.record(r.id).put(c, {...r.toMap(), _dirty: false});

  Future<void> dispose() => _changes.close();
}
