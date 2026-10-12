import 'dart:async';

import 'package:kco_practice/features/auth/auth_service.dart';
import 'package:kco_practice/features/practice/domain/practice_record.dart';
import 'package:kco_practice/features/sync/conflict.dart';
import 'package:kco_practice/features/sync/remote_record_store.dart';
import 'package:sembast/sembast_memory.dart';

/// テストごとに別の、メモリ上のデータベース
Future<Database> openMemoryDb() =>
    newDatabaseFactoryMemory().openDatabase('test.db');

/// 手で進める時計
class FakeClock {
  FakeClock([DateTime? start]) : now = start ?? DateTime(2026, 10, 12, 9);

  DateTime now;
  DateTime call() => now;
  void advance(Duration d) => now = now.add(d);
}

PracticeRecord record(
  String id, {
  String? owner = 'u1',
  int updatedAt = 1000,
  String by = 'devA',
  bool deleted = false,
  String note = '',
  String day = '2026-10-12',
  Map<String, int> actual = const {'mouthpiece': 1200},
}) => PracticeRecord(
  id: id,
  ownerUid: owner,
  practicedOn: day,
  startedAtMillis: 0,
  ruleSetId: 'trumpet_basic',
  plannedMinutes: const {'mouthpiece': 20},
  actualSeconds: actual,
  note: note,
  updatedAtMillis: updatedAt,
  updatedBy: by,
  deleted: deleted,
);

/// Firestore の代わり（FirestoreRemoteRecordStore と同じ決まりで動く）
class FakeRemote implements RemoteRecordStore {
  final Map<String, Map<String, (PracticeRecord, int)>> data = {};
  int serverTime = 100;
  bool offline = false;
  int fetchCount = 0;

  /// 送信の直前に割り込む処理（送っている間に別の端末が書き込んだ、などを再現する）
  Future<void> Function()? beforePush;

  void putServer(String uid, PracticeRecord r) =>
      (data[uid] ??= {})[r.id] = (r, serverTime++);

  PracticeRecord? get(String uid, String id) => data[uid]?[id]?.$1;

  @override
  Future<RemoteChanges> fetchChangedSince(String uid, int? cursorMillis) async {
    if (offline) throw StateError('offline');
    fetchCount++;
    final hits =
        (data[uid] ?? {}).values
            .where((e) => cursorMillis == null || e.$2 >= cursorMillis)
            .toList()
          ..sort((a, b) => a.$2.compareTo(b.$2));
    return RemoteChanges([
      for (final e in hits) e.$1,
    ], hits.isEmpty ? null : hits.last.$2);
  }

  @override
  Future<PracticeRecord> pushIfNewer(String uid, PracticeRecord record) async {
    if (offline) throw StateError('offline');
    await beforePush?.call();
    final existing = get(uid, record.id);
    if (existing != null &&
        identical(resolveConflict(record, existing), existing)) {
      return existing;
    }
    putServer(uid, record);
    return record;
  }
}

class FakeAuth implements AuthService {
  FakeAuth([this._user]);

  AppUser? _user;
  final _controller = StreamController<AppUser?>.broadcast();

  void emit(AppUser? u) {
    _user = u;
    _controller.add(u);
  }

  @override
  AppUser? get currentUser => _user;

  @override
  Stream<AppUser?> get userChanges => _controller.stream;

  @override
  Future<void> signInWithGoogle() async =>
      emit(const AppUser(uid: 'u1', email: 'u1@example.com'));

  @override
  Future<void> signInWithEmail(String email, String password) async {
    if (password != 'secret1') throw const AuthFailure('メールアドレスかパスワードが違います');
    emit(AppUser(uid: 'u-$email', email: email));
  }

  @override
  Future<void> signUpWithEmail(String email, String password) =>
      signInWithEmail(email, password);

  @override
  Future<void> sendPasswordReset(String email) async {}

  @override
  Future<void> signOut() async => emit(null);
}
