import 'package:flutter_test/flutter_test.dart';
import 'package:kco_practice/features/practice/data/practice_repository.dart';

import '../../helpers.dart';

void main() {
  late FakeClock clock;
  late PracticeRepository repo;

  setUp(() async {
    clock = FakeClock(DateTime(2026, 10, 12, 21, 30));
    repo = PracticeRepository(
      await openMemoryDb(),
      deviceId: 'devA',
      clock: clock.call,
    );
  });

  Future<String> create({String? owner}) async => (await repo.create(
    ownerUid: owner,
    startedAt: clock.now,
    ruleSetId: 'trumpet_basic',
    plannedMinutes: const {'mouthpiece': 20},
    actualSeconds: const {'mouthpiece': 1180},
  )).id;

  test('作った記録は未送信で、練習した日はローカル日付', () async {
    final id = await create();
    final r = (await repo.get(id))!;
    expect(r.practicedOn, '2026-10-12');
    expect(r.updatedBy, 'devA');
    expect(r.updatedAtMillis, clock.now.millisecondsSinceEpoch);
    expect(await repo.isDirty(id), isTrue);
  });

  test('ログイン前の記録は誰からも見え、アカウントの記録はそのアカウントだけ', () async {
    await create();
    await create(owner: 'u1');
    await create(owner: 'u2');
    expect((await repo.visible(null)).map((r) => r.ownerUid), [null]);
    expect((await repo.visible('u1')).map((r) => r.ownerUid).toSet(), {
      null,
      'u1',
    });
  });

  test('メモの編集・削除は更新時刻を進め、未送信にする。削除済みは一覧に出ない', () async {
    final id = await create(owner: 'u1');
    await repo.applyRemote((await repo.get(id))!); // 送信済みにする
    expect(await repo.isDirty(id), isFalse);

    clock.advance(const Duration(minutes: 5));
    await repo.updateNote(id, '高音が楽になった');
    final edited = (await repo.get(id))!;
    expect(edited.note, '高音が楽になった');
    expect(edited.updatedAtMillis, clock.now.millisecondsSinceEpoch);
    expect(await repo.isDirty(id), isTrue);

    await repo.delete(id);
    expect((await repo.get(id))!.deleted, isTrue);
    expect(await repo.visible('u1'), isEmpty);
  });

  test('ログイン前の記録をアカウントに引き継ぐ', () async {
    final guest = await create();
    await create(owner: 'u2');
    await repo.claimGuestRecords('u1');
    expect((await repo.get(guest))!.ownerUid, 'u1');
    expect((await repo.dirtyRecordsFor('u1')).map((r) => r.id), [guest]);
  });

  test('localChanges は操作のたびに届く', () async {
    var count = 0;
    final sub = repo.localChanges.listen((_) => count++);
    final id = await create();
    await repo.updateNote(id, 'x');
    await repo.delete(id);
    await Future<void>.delayed(Duration.zero);
    expect(count, 3);
    await sub.cancel();
  });

  group('applyRemote', () {
    test('端末にない記録はそのまま取り込む', () async {
      expect(await repo.applyRemote(record('r1')), isTrue);
      expect(await repo.get('r1'), record('r1'));
      expect(await repo.isDirty('r1'), isFalse);
    });

    test('送信済みの記録はクラウドの版で上書き', () async {
      await repo.applyRemote(record('r1', note: 'old'));
      expect(
        await repo.applyRemote(record('r1', note: 'new', updatedAt: 2000)),
        isTrue,
      );
      expect((await repo.get('r1'))!.note, 'new');
      // 同じ版をもう一度取り込んでも「変わった」にはならない
      expect(
        await repo.applyRemote(record('r1', note: 'new', updatedAt: 2000)),
        isFalse,
      );
    });

    test('未送信の編集が新しければ端末の版を残す（次に送る）', () async {
      final id = await create(owner: 'u1');
      final remoteOld = (await repo.get(id))!
          .copyWith(note: 'クラウド', updatedAtMillis: 1, updatedBy: 'devB');
      expect(await repo.applyRemote(remoteOld), isFalse);
      expect((await repo.get(id))!.note, '');
      expect(await repo.isDirty(id), isTrue);
    });

    test('クラウドの版が新しければ端末の未送信の編集より優先', () async {
      final id = await create(owner: 'u1');
      final local = (await repo.get(id))!;
      final remoteNew = local.copyWith(
        note: 'クラウド',
        updatedAtMillis: local.updatedAtMillis + 1,
        updatedBy: 'devB',
      );
      expect(await repo.applyRemote(remoteNew), isTrue);
      expect((await repo.get(id))!.note, 'クラウド');
      expect(await repo.isDirty(id), isFalse);
    });

    test('送った版がそのままなら送信済みにする', () async {
      final id = await create(owner: 'u1');
      final pushed = (await repo.get(id))!;
      await repo.applyRemote(pushed, pushed: pushed);
      expect(await repo.isDirty(id), isFalse);
    });

    test('送っている間に端末で編集されていたら、その編集は消さない', () async {
      final id = await create(owner: 'u1');
      final pushed = (await repo.get(id))!;
      clock.advance(const Duration(seconds: 1));
      await repo.updateNote(id, '送信中に書いたメモ');
      await repo.applyRemote(pushed, pushed: pushed);
      expect((await repo.get(id))!.note, '送信中に書いたメモ');
      expect(await repo.isDirty(id), isTrue);
    });
  });

  test('同期の位置はアカウントごと', () async {
    expect(await repo.syncCursor('u1'), isNull);
    await repo.setSyncCursor('u1', 123);
    expect(await repo.syncCursor('u1'), 123);
    expect(await repo.syncCursor('u2'), isNull);
  });
}
