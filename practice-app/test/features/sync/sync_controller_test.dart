import 'package:flutter_test/flutter_test.dart';
import 'package:kco_practice/features/auth/auth_service.dart';
import 'package:kco_practice/features/practice/data/practice_repository.dart';
import 'package:kco_practice/features/sync/sync_controller.dart';
import 'package:kco_practice/features/sync/sync_engine.dart';

import '../../helpers.dart';

void main() {
  late FakeRemote cloud;
  late PracticeRepository repo;
  late FakeAuth auth;

  setUp(() async {
    cloud = FakeRemote();
    repo = PracticeRepository(await openMemoryDb(), deviceId: 'devA');
    auth = FakeAuth();
  });

  SyncController controller() => SyncController(
    auth: auth,
    repository: repo,
    engine: SyncEngine(repo, cloud),
    debounce: const Duration(milliseconds: 10),
  );

  Future<void> settle() =>
      Future<void>.delayed(const Duration(milliseconds: 60));

  Future<void> practice() => repo.create(
    ownerUid: auth.currentUser?.uid,
    startedAt: DateTime(2026, 10, 12),
    ruleSetId: 'trumpet_basic',
    plannedMinutes: const {'mouthpiece': 20},
    actualSeconds: const {'mouthpiece': 1200},
  );

  test('クラウドにつながる前は unavailable。接続中・失敗・あとからつながる', () async {
    final c = SyncController(repository: repo);
    expect(c.status, SyncStatus.unavailable);
    expect(c.isAvailable, isFalse);
    expect(c.auth, isNull);

    c.beginConnecting();
    expect(c.status, SyncStatus.connecting);
    c.markUnavailable();
    expect(c.status, SyncStatus.unavailable);

    // ログイン済みのアカウントでつながったら、すぐ同期する
    auth.emit(const AppUser(uid: 'u1'));
    await practice();
    c.attach(auth, SyncEngine(repo, cloud));
    expect(c.isAvailable, isTrue);
    await settle();
    expect(c.status, SyncStatus.idle);
    expect(cloud.data['u1'], hasLength(1));

    // つながったあとは接続中・失敗の印に戻らない
    c.beginConnecting();
    c.markUnavailable();
    expect(c.status, SyncStatus.idle);
  });

  test('ログインしていなければ同期しない。ログインしたらすぐ同期する', () async {
    final c = controller();
    expect(c.status, SyncStatus.signedOut);
    await practice();
    await settle();
    expect(cloud.fetchCount, 0);

    auth.emit(const AppUser(uid: 'u1'));
    await settle();
    expect(c.status, SyncStatus.idle);
    expect(c.lastSyncedAt, isNotNull);
    expect(cloud.data['u1'], hasLength(1)); // ログイン前の記録も送った
  });

  test('ログイン中は、記録が変わると少し待ってから同期する', () async {
    auth.emit(const AppUser(uid: 'u1'));
    final c = controller();
    await settle();
    final before = cloud.fetchCount;
    await practice();
    await practice();
    await settle();
    expect(cloud.fetchCount, before + 1); // 2回の変更をまとめて1回
    expect(cloud.data['u1'], hasLength(2));
    c.dispose();
  });

  test('失敗したら error になり、次に成功すれば戻る', () async {
    auth.emit(const AppUser(uid: 'u1'));
    cloud.offline = true;
    final c = controller();
    await settle();
    expect(c.status, SyncStatus.error);
    expect(c.lastError, isNotNull);

    cloud.offline = false;
    await c.syncNow();
    expect(c.status, SyncStatus.idle);
    expect(c.lastError, isNull);
  });

  test('ログアウトすると signedOut に戻る', () async {
    auth.emit(const AppUser(uid: 'u1'));
    final c = controller();
    await settle();
    auth.emit(null);
    await settle();
    expect(c.status, SyncStatus.signedOut);
    expect(c.user, isNull);
  });

  test('同期中に呼ばれたら、終わったあとにもう1回', () async {
    auth.emit(const AppUser(uid: 'u1'));
    final c = controller();
    await settle();
    final before = cloud.fetchCount;
    final first = c.syncNow();
    final second = c.syncNow();
    await Future.wait([first, second]);
    expect(cloud.fetchCount, before + 2);
  });
}
