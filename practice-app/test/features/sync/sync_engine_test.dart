import 'package:flutter_test/flutter_test.dart';
import 'package:kco_practice/features/practice/data/practice_repository.dart';
import 'package:kco_practice/features/practice/domain/practice_record.dart';
import 'package:kco_practice/features/sync/sync_engine.dart';

import '../../helpers.dart';

/// 2台の端末（A・B）と1つのクラウドで、同期の結果を確かめる
void main() {
  late FakeRemote cloud;
  late FakeClock clock;
  late PracticeRepository deviceA, deviceB;
  late SyncEngine syncA, syncB;

  setUp(() async {
    cloud = FakeRemote();
    clock = FakeClock();
    deviceA = PracticeRepository(
      await openMemoryDb(),
      deviceId: 'devA',
      clock: clock.call,
    );
    deviceB = PracticeRepository(
      await openMemoryDb(),
      deviceId: 'devB',
      clock: clock.call,
    );
    syncA = SyncEngine(deviceA, cloud);
    syncB = SyncEngine(deviceB, cloud);
  });

  Future<PracticeRecord> practice(
    PracticeRepository device, {
    String? owner = 'u1',
  }) => device.create(
    ownerUid: owner,
    startedAt: clock.now,
    ruleSetId: 'trumpet_basic',
    plannedMinutes: const {'mouthpiece': 20},
    actualSeconds: const {'mouthpiece': 1200},
  );

  test('端末 A の記録が端末 B に届く', () async {
    final r = await practice(deviceA);
    final reportA = await syncA.syncOnce('u1');
    expect(reportA.pushed, 1);
    expect(cloud.get('u1', r.id), r);
    expect(await deviceA.isDirty(r.id), isFalse);

    final reportB = await syncB.syncOnce('u1');
    expect(reportB.pulled, 1);
    expect(await deviceB.get(r.id), r);
  });

  test('ログイン前の記録は、ログインしたアカウントに引き継いで送る', () async {
    final r = await practice(deviceA, owner: null);
    await syncA.syncOnce('u1');
    expect(cloud.get('u1', r.id)!.ownerUid, 'u1');
    expect((await deviceA.get(r.id))!.ownerUid, 'u1');
  });

  test('オフラインで両方の端末が同じ記録を編集したら、後から編集した方が残る', () async {
    final r = await practice(deviceA);
    await syncA.syncOnce('u1');
    await syncB.syncOnce('u1');

    clock.advance(const Duration(minutes: 1));
    await deviceA.updateNote(r.id, 'A のメモ');
    clock.advance(const Duration(minutes: 1));
    await deviceB.updateNote(r.id, 'B のメモ（後）');

    await syncB.syncOnce('u1');
    await syncA.syncOnce('u1'); // A の編集は古いので負ける
    await syncB.syncOnce('u1');

    for (final device in [deviceA, deviceB]) {
      expect((await device.get(r.id))!.note, 'B のメモ（後）');
      expect(await device.isDirty(r.id), isFalse);
    }
    expect(cloud.get('u1', r.id)!.note, 'B のメモ（後）');
  });

  test('先に送った古い編集は、後から来た新しい編集に上書きされる', () async {
    final r = await practice(deviceA);
    await syncA.syncOnce('u1');
    await syncB.syncOnce('u1');

    clock.advance(const Duration(minutes: 1));
    await deviceA.updateNote(r.id, '古い');
    clock.advance(const Duration(minutes: 1));
    await deviceB.updateNote(r.id, '新しい');

    await syncA.syncOnce('u1'); // 古い方が先に届く
    await syncB.syncOnce('u1'); // 新しい方が勝つ
    await syncA.syncOnce('u1');

    expect((await deviceA.get(r.id))!.note, '新しい');
    expect(cloud.get('u1', r.id)!.note, '新しい');
  });

  test('削除は別の端末にも伝わり、古い編集で復活しない', () async {
    final r = await practice(deviceA);
    await syncA.syncOnce('u1');
    await syncB.syncOnce('u1');

    clock.advance(const Duration(minutes: 1));
    await deviceB.updateNote(r.id, '古い編集');
    clock.advance(const Duration(minutes: 1));
    await deviceA.delete(r.id);

    await syncA.syncOnce('u1');
    await syncB.syncOnce('u1');

    expect(await deviceB.visible('u1'), isEmpty);
    expect(cloud.get('u1', r.id)!.deleted, isTrue);
  });

  test('送信の直前に別の端末が新しい版を書き込んでいたら、その版を取り込む', () async {
    final r = await practice(deviceA);
    await syncA.syncOnce('u1');
    clock.advance(const Duration(minutes: 1));
    await deviceA.updateNote(r.id, 'A');
    cloud.beforePush = () async {
      cloud.beforePush = null;
      cloud.putServer(
        'u1',
        r.copyWith(
          note: 'B（より新しい）',
          updatedAtMillis: clock.now.millisecondsSinceEpoch + 1,
          updatedBy: 'devB',
        ),
      );
    };
    final report = await syncA.syncOnce('u1');
    expect(report.pushed, 0);
    expect((await deviceA.get(r.id))!.note, 'B（より新しい）');
    expect(await deviceA.isDirty(r.id), isFalse);
  });

  test('2回目以降は前回の位置から取得し、何度同期しても結果は同じ', () async {
    await practice(deviceA);
    await practice(deviceA);
    await syncA.syncOnce('u1'); // 送るだけ（クラウドは空だったので取得位置はまだない）
    expect(await deviceA.syncCursor('u1'), isNull);
    final before = await deviceA.visible('u1');

    // 2回目：自分が送った記録が返ってくるが、端末の内容は変わらない
    final again = await syncA.syncOnce('u1');
    expect(again.pushed, 0);
    expect(again.pulled, 0);
    expect(await deviceA.syncCursor('u1'), cloud.serverTime - 1);
    expect(await deviceA.visible('u1'), before);

    final third = await syncA.syncOnce('u1');
    expect([third.pushed, third.pulled], [0, 0]);
    expect(await deviceA.visible('u1'), before);
  });

  test('ほかのアカウントの記録は送らない・取り込まない', () async {
    final mine = await practice(deviceA);
    final others = await practice(deviceA, owner: 'u2');
    cloud.putServer('u1', record('stray', owner: 'u2'));
    await syncA.syncOnce('u1');
    expect(cloud.get('u1', mine.id), isNotNull);
    expect(cloud.get('u1', others.id), isNull);
    expect(await deviceA.get('stray'), isNull);
  });

  test('オフラインなら失敗し、端末の記録は未送信のまま残る', () async {
    final r = await practice(deviceA);
    cloud.offline = true;
    await expectLater(syncA.syncOnce('u1'), throwsStateError);
    expect(await deviceA.isDirty(r.id), isTrue);
    cloud.offline = false;
    await syncA.syncOnce('u1');
    expect(await deviceA.isDirty(r.id), isFalse);
  });
}
