import 'package:flutter/material.dart';

import '../../../app/app_services.dart';
import '../../../core/clock.dart';
import '../domain/practice_record.dart';

/// 削除した記録（ごみ箱）。元に戻せる
class DeletedRecordsPage extends StatelessWidget {
  const DeletedRecordsPage({super.key});

  @override
  Widget build(BuildContext context) {
    final services = AppScope.of(context);
    final theme = Theme.of(context);
    return Scaffold(
      appBar: AppBar(title: const Text('削除した記録')),
      body: ListenableBuilder(
        listenable: services.sync,
        builder: (context, _) => StreamBuilder<List<PracticeRecord>>(
          stream: services.practice.watchDeleted(services.sync.user?.uid),
          builder: (context, snap) {
            final list = snap.data ?? const [];
            return ListView(
              padding: const EdgeInsets.all(16),
              children: [
                Text(
                  '削除した記録は、ここから元に戻せます。ログイン中なら、戻した記録はほかの端末にも戻ります。',
                  style: theme.textTheme.bodySmall,
                ),
                const SizedBox(height: 8),
                if (list.isEmpty)
                  const Padding(
                    padding: EdgeInsets.symmetric(vertical: 24),
                    child: Text('削除した記録はありません', textAlign: TextAlign.center),
                  ),
                for (final r in list)
                  ListTile(
                    contentPadding: EdgeInsets.zero,
                    title: Text(
                      '${r.practicedOn}　${formatSeconds(r.totalActualSeconds)}',
                    ),
                    subtitle: r.note.isEmpty ? null : Text(r.note, maxLines: 1),
                    trailing: TextButton.icon(
                      onPressed: () => services.practice.restore(r.id),
                      icon: const Icon(Icons.restore),
                      label: const Text('元に戻す'),
                    ),
                  ),
              ],
            );
          },
        ),
      ),
    );
  }
}
