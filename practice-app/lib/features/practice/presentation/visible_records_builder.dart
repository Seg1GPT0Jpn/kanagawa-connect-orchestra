import 'package:flutter/material.dart';

import '../../../app/app_services.dart';
import '../domain/practice_record.dart';

/// 今のアカウントで見える練習記録を渡して画面を作る（ログイン・ログアウトで切り替わる）
class VisibleRecordsBuilder extends StatefulWidget {
  const VisibleRecordsBuilder({super.key, required this.builder});

  final Widget Function(BuildContext context, List<PracticeRecord> records)
  builder;

  @override
  State<VisibleRecordsBuilder> createState() => _VisibleRecordsBuilderState();
}

class _VisibleRecordsBuilderState extends State<VisibleRecordsBuilder> {
  Stream<List<PracticeRecord>>? _stream;
  String? _uid;
  bool _first = true;

  @override
  Widget build(BuildContext context) {
    final services = AppScope.of(context);
    return ListenableBuilder(
      listenable: services.sync,
      builder: (context, _) {
        final uid = services.sync.user?.uid;
        if (_first || uid != _uid) {
          _first = false;
          _uid = uid;
          _stream = services.practice.watchVisible(uid);
        }
        return StreamBuilder<List<PracticeRecord>>(
          stream: _stream,
          builder: (context, snap) =>
              widget.builder(context, snap.data ?? const []),
        );
      },
    );
  }
}
