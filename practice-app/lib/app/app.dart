import 'package:flutter/material.dart';

import '../features/menu/domain/menu_rules.dart';
import '../features/menu/presentation/menu_audit_page.dart';

class KcoPracticeApp extends StatelessWidget {
  const KcoPracticeApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: '練習お助け',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF1F4E79)),
      ),
      darkTheme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF1F4E79),
          brightness: Brightness.dark,
        ),
      ),
      home: const MenuAuditPage(rules: trumpetBasicRules),
    );
  }
}
