import 'package:flutter/material.dart';

import '../features/audio_tools/presentation/tools_page.dart';
import '../features/auth/account_page.dart';
import '../features/menu/domain/menu_presets.dart';
import '../features/menu/domain/menu_rules.dart';
import '../features/menu/presentation/mode_selector.dart';
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
  late final AppLifecycleListener _lifecycle;

  @override
  void initState() {
    super.initState();
    // 裏に回ったら音とマイクを止める（戻ったら、ボタンでもう一度始める）
    _lifecycle = AppLifecycleListener(
      onHide: () => AppScope.of(context).pauseAll(),
    );
  }

  @override
  void dispose() {
    _lifecycle.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final services = AppScope.of(context);
    return Scaffold(
      body: IndexedStack(
        index: _tab,
        children: [
          const PracticeHomePage(),
          const RecordsPage(),
          ListenableBuilder(
            listenable: services.menu,
            builder: (context, _) {
              final menu = services.menu;
              return MenuAuditPage(
                // モード・保存したメニューが変わったら画面の初期値も入れ替える
                key: ObjectKey((menu.rules, menu.savedMenu)),
                rules: menu.rules,
                initialMinutes: menu.savedMenu,
                onSave: menu.save,
                presets: menu.rules.id == trumpetBasicRules.id
                    ? trumpetBasicPresets
                    : const [],
                header: ModeSelector(controller: menu),
              );
            },
          ),
          const ToolsPage(),
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
            icon: Icon(Icons.music_note_outlined),
            selectedIcon: Icon(Icons.music_note),
            label: '道具',
          ),
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
