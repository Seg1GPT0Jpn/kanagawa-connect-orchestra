import 'package:flutter/material.dart';

import 'app_services.dart';
import 'home_shell.dart';

class KcoPracticeApp extends StatelessWidget {
  const KcoPracticeApp({super.key, required this.services});

  final AppServices services;

  static const _seed = Color(0xFF1F4E79);

  @override
  Widget build(BuildContext context) {
    return AppScope(
      services: services,
      child: MaterialApp(
        title: '練習お助け',
        theme: ThemeData(colorScheme: ColorScheme.fromSeed(seedColor: _seed)),
        darkTheme: ThemeData(
          colorScheme: ColorScheme.fromSeed(
            seedColor: _seed,
            brightness: Brightness.dark,
          ),
        ),
        home: const HomeShell(),
      ),
    );
  }
}
