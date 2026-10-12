import 'package:sembast/sembast.dart';

import '../domain/recording_result.dart';

/// 録音の分析結果を端末内に保存する（音声は保存しない。クラウドにも送らない）
class RecordingRepository {
  RecordingRepository(this._db);

  final Database _db;
  static final _store = stringMapStoreFactory.store('recording_results');

  Future<void> save(RecordingResult r) =>
      _store.record(r.id).put(_db, r.toMap());

  Future<void> delete(String id) => _store.record(id).delete(_db);

  /// バックアップから取り込む（同じ ID があれば上書きしない）。追加した数を返す
  Future<int> importResults(List<RecordingResult> results) async {
    var added = 0;
    await _db.transaction((txn) async {
      for (final r in results) {
        if (await _store.record(r.id).exists(txn)) continue;
        await _store.record(r.id).put(txn, r.toMap());
        added++;
      }
    });
    return added;
  }

  /// 新しい順
  Stream<List<RecordingResult>> watchAll() => _store
      .query(finder: Finder(sortOrders: [SortOrder('recordedAt', false)]))
      .onSnapshots(_db)
      .map(
        (snaps) => [for (final s in snaps) RecordingResult.fromMap(s.value)],
      );

  Future<List<RecordingResult>> all() async => [
    for (final s in await _store.find(
      _db,
      finder: Finder(sortOrders: [SortOrder('recordedAt', false)]),
    ))
      RecordingResult.fromMap(s.value),
  ];
}
