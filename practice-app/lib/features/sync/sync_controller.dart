import 'dart:async';

import 'package:flutter/foundation.dart';

import '../../core/clock.dart';
import '../auth/auth_service.dart';
import '../practice/data/practice_repository.dart';
import 'sync_engine.dart';

enum SyncStatus {
  /// クラウド同期が使えない（Firebase の設定がない端末・オフラインで接続できなかった）
  unavailable,

  /// クラウドに接続している途中（そのあいだも端末内の保存は使える）
  connecting,

  /// ログインしていない（端末内だけで保存）
  signedOut,
  idle,
  syncing,
  error,
}

/// いつ同期するかを決める：ログインしたとき・端末で記録が変わったとき・「今すぐ同期」
///
/// クラウド（ログインと同期の仕組み）は [attach] であとからつなぐ。
/// つながるまで・つながらない端末では、端末内の保存だけで動く。
class SyncController extends ChangeNotifier {
  SyncController({
    required this._repository,
    AuthService? auth,
    SyncEngine? engine,
    this.clock = systemClock,
    this.debounce = const Duration(seconds: 2),
  }) {
    if (auth != null && engine != null) attach(auth, engine);
  }

  final PracticeRepository _repository;
  AuthService? _auth;
  SyncEngine? _engine;
  final Clock clock;
  final Duration debounce;
  final _subs = <StreamSubscription<Object?>>[];

  AppUser? _user;
  SyncStatus _status = SyncStatus.unavailable;
  DateTime? _lastSyncedAt;
  String? _lastError;
  Timer? _timer;
  Future<void>? _running;
  bool _again = false;

  AppUser? get user => _user;
  SyncStatus get status => _status;
  DateTime? get lastSyncedAt => _lastSyncedAt;
  String? get lastError => _lastError;
  bool get isAvailable => _auth != null && _engine != null;

  /// ログイン（クラウドにつながっていなければ null）
  AuthService? get auth => _auth;

  /// クラウドにつなぐ。2回目以降は何もしない
  void attach(AuthService auth, SyncEngine engine) {
    if (isAvailable) return;
    _auth = auth;
    _engine = engine;
    _user = auth.currentUser;
    _status = _user == null ? SyncStatus.signedOut : SyncStatus.idle;
    _subs.add(auth.userChanges.listen(_onUser));
    _subs.add(_repository.localChanges.listen((_) => _schedule()));
    notifyListeners();
    if (_user != null) unawaited(syncNow());
  }

  void beginConnecting() {
    if (isAvailable) return;
    _status = SyncStatus.connecting;
    notifyListeners();
  }

  void markUnavailable() {
    if (isAvailable) return;
    _status = SyncStatus.unavailable;
    notifyListeners();
  }

  void _onUser(AppUser? u) {
    final changed = u?.uid != _user?.uid;
    _user = u;
    if (u == null) {
      _timer?.cancel();
      _status = SyncStatus.signedOut;
      _lastSyncedAt = null;
      _lastError = null;
      notifyListeners();
    } else if (changed) {
      _status = SyncStatus.idle;
      notifyListeners();
      unawaited(syncNow());
    }
  }

  void _schedule() {
    if (_user == null) return;
    _timer?.cancel();
    _timer = Timer(debounce, () => unawaited(syncNow()));
  }

  /// 同期する。実行中に呼ばれたら、終わったあとにもう1回
  Future<void> syncNow() {
    if (_running != null) {
      _again = true;
      return _running!;
    }
    return _running = _run().whenComplete(() => _running = null);
  }

  Future<void> _run() async {
    do {
      _again = false;
      final u = _user;
      final engine = _engine;
      if (u == null || engine == null) return;
      _status = SyncStatus.syncing;
      notifyListeners();
      try {
        await engine.syncOnce(u.uid);
        if (_user?.uid != u.uid) continue;
        _status = SyncStatus.idle;
        _lastSyncedAt = clock();
        _lastError = null;
      } catch (e) {
        if (_user?.uid != u.uid) continue;
        _status = SyncStatus.error;
        _lastError = '同期できませんでした。インターネットにつながったら、もう一度お試しください';
        debugPrint('sync failed: $e');
      }
      notifyListeners();
    } while (_again);
  }

  @override
  void dispose() {
    _timer?.cancel();
    for (final s in _subs) {
      s.cancel();
    }
    super.dispose();
  }
}
