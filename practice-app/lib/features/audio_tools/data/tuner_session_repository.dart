import 'package:sembast/sembast.dart';

import '../domain/pitch_stats.dart';

/// チューナーの練習記録（音程の統計）を端末内に保存する（クラウドには送らない）
class TunerSessionRepository {
  TunerSessionRepository(this._db);

  final Database _db;
  static final _store = stringMapStoreFactory.store('tuner_sessions');

  /// 古いものから消して、この数まで残す
  static const keep = 200;

  Future<void> save(TunerSession s) async {
    await _store.record(s.id).put(_db, s.toMap());
    final all = await _store.find(
      _db,
      finder: Finder(sortOrders: [SortOrder('startedAt', false)]),
    );
    for (final old in all.skip(keep)) {
      await _store.record(old.key).delete(_db);
    }
  }

  Future<void> delete(String id) => _store.record(id).delete(_db);

  /// バックアップから取り込む（同じ記録はそのまま）。追加した数を返す
  Future<int> importSessions(List<TunerSession> sessions) async {
    var added = 0;
    await _db.transaction((txn) async {
      for (final s in sessions) {
        if (await _store.record(s.id).exists(txn)) continue;
        await _store.record(s.id).put(txn, s.toMap());
        added++;
      }
    });
    return added;
  }

  /// 新しい順
  Stream<List<TunerSession>> watchAll() => _store
      .query(finder: Finder(sortOrders: [SortOrder('startedAt', false)]))
      .onSnapshots(_db)
      .map((snaps) => [for (final s in snaps) TunerSession.fromMap(s.value)]);

  Future<List<TunerSession>> all() async => [
    for (final s in await _store.find(
      _db,
      finder: Finder(sortOrders: [SortOrder('startedAt', false)]),
    ))
      TunerSession.fromMap(s.value),
  ];
}
