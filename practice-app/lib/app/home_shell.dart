import 'package:flutter/material.dart';

import '../features/auth/account_page.dart';
import '../features/menu/domain/menu_presets.dart';
import '../features/menu/presentation/menu_audit_page.dart';
import '../features/practice/presentation/practice_home_page.dart';
import '../features/practice/presentation/records_page.dart';
import 'app_services.dart';

/// 下のタブで画面を切り替える
class HomeShell extends StatefulWidget {
  const HomeShell({super.key});

  @override
  State<HomeShell> createState() => _HomeShellState();
}

class _HomeShellState extends State<HomeShell> {
  int _tab = 0;

  @override
  Widget build(BuildContext context) {
    final services = AppScope.of(context);
    return Scaffold(
      body: IndexedStack(
        index: _tab,
        children: [
          const PracticeHomePage(),
          const RecordsPage(),
          ValueListenableBuilder<Map<String, int>>(
            valueListenable: services.menu,
            builder: (context, minutes, _) => MenuAuditPage(
              // 保存し直したら画面の初期値も入れ替える
              key: ValueKey(minutes),
              rules: services.menu.rules,
              initialMinutes: minutes,
              onSave: services.menu.save,
              presets: trumpetBasicPresets,
            ),
          ),
          const AccountPage(),
        ],
      ),
      bottomNavigationBar: NavigationBar(
        selectedIndex: _tab,
        onDestinationSelected: (i) => setState(() => _tab = i),
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.timer_outlined),
            selectedIcon: Icon(Icons.timer),
            label: '練習',
          ),
          NavigationDestination(icon: Icon(Icons.history), label: '記録'),
          NavigationDestination(icon: Icon(Icons.tune), label: 'メニュー'),
          NavigationDestination(
            icon: Icon(Icons.person_outline),
            selectedIcon: Icon(Icons.person),
            label: 'アカウント',
          ),
        ],
      ),
    );
  }
}
