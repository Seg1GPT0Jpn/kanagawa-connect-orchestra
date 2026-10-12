import 'package:sembast/sembast.dart';

import 'ids.dart';

/// 端末内の小さな設定値（端末 ID・同期の位置・メニュー設定など）
class MetaStore {
  MetaStore(this._db);

  final Database _db;
  static final _store = StoreRef<String, Object?>('meta');

  Future<Object?> get(String key) => _store.record(key).get(_db);
  Future<void> put(String key, Object? value) =>
      _store.record(key).put(_db, value);

  /// この端末の ID（同期の競合で、編集時刻が同じときの決め手に使う）。初回に作って保存する
  Future<String> deviceId() async {
    final existing = await get('deviceId');
    if (existing is String) return existing;
    final id = generateId();
    await put('deviceId', id);
    return id;
  }
}
