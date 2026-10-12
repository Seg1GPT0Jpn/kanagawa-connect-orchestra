import 'package:flutter/material.dart';

import '../../app/app_services.dart';
import 'export_format.dart';

/// 記録タブの「︙」：CSV・バックアップの書き出しと、バックアップの読み込み
class DataMenuButton extends StatelessWidget {
  const DataMenuButton({super.key});

  @override
  Widget build(BuildContext context) {
    final services = AppScope.of(context);
    return PopupMenuButton<String>(
      tooltip: '書き出し・読み込み',
      onSelected: (v) => _run(context, services, v),
      itemBuilder: (context) => const [
        PopupMenuItem(value: 'csv', child: Text('表（CSV）で書き出す')),
        PopupMenuItem(value: 'backup', child: Text('バックアップ（JSON）を書き出す')),
        PopupMenuItem(value: 'import', child: Text('バックアップを読み込む')),
      ],
    );
  }

  Future<void> _run(
    BuildContext context,
    AppServices services,
    String action,
  ) async {
    final messenger = ScaffoldMessenger.of(context);
    final uid = services.sync.user?.uid;
    String? message;
    try {
      message = switch (action) {
        'csv' =>
          await services.dataIo.exportCsv(uid, services.menu.rules)
              ? '表（CSV）を書き出しました'
              : null,
        'backup' =>
          await services.dataIo.exportBackup(uid) ? 'バックアップを書き出しました' : null,
        _ => switch (await services.dataIo.importBackup(uid)) {
          final r? => '読み込みました（${r.summary}）',
          null => null,
        },
      };
    } on ImportFormatException catch (e) {
      message = '読み込めませんでした：${e.message}';
    } catch (e) {
      message = 'うまくいきませんでした（$e）';
    }
    if (message != null) {
      messenger.showSnackBar(SnackBar(content: Text(message)));
    }
  }
}
