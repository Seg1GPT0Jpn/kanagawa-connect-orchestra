/// 端末内の練習記録とクラウドの同期（1回分）
///
/// 1. ログイン前に作った記録をこのアカウントに引き継ぐ
/// 2. 前回以降にクラウドで変わった記録を取り込む（端末で未送信の編集と競合したら [resolveConflict]）
/// 3. 端末で未送信の記録を送る（クラウドの方が新しければクラウドの版を取り込む）
library;

import '../practice/data/practice_repository.dart';
import 'remote_record_store.dart';

class SyncReport {
  const SyncReport({required this.pulled, required this.pushed});

  /// クラウドから取り込んで端末の内容が変わった件数
  final int pulled;

  /// クラウドに送った件数
  final int pushed;
}

class SyncEngine {
  SyncEngine(this._local, this._remote);

  final PracticeRepository _local;
  final RemoteRecordStore _remote;

  Future<SyncReport> syncOnce(String uid) async {
    await _local.claimGuestRecords(uid);

    var pulled = 0;
    final changes = await _remote.fetchChangedSince(
      uid,
      await _local.syncCursor(uid),
    );
    for (final r in changes.records) {
      if (r.ownerUid != uid) continue; // ルールで防いでいるが念のため
      if (await _local.applyRemote(r)) pulled++;
    }
    if (changes.latestServerMillis != null) {
      await _local.setSyncCursor(uid, changes.latestServerMillis!);
    }

    var pushed = 0;
    for (final r in await _local.dirtyRecordsFor(uid)) {
      final winner = await _remote.pushIfNewer(uid, r);
      if (identical(winner, r)) pushed++;
      final changed = await _local.applyRemote(winner, pushed: r);
      if (changed && !identical(winner, r)) pulled++;
    }
    return SyncReport(pulled: pulled, pushed: pushed);
  }
}
