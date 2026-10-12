import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import 'app_info.dart';

/// このアプリについて（版・データの扱い・ライセンス）
class AboutPage extends StatelessWidget {
  const AboutPage({super.key});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    Widget link(String label, String url) => ListTile(
      contentPadding: EdgeInsets.zero,
      title: Text(label),
      subtitle: Text(url),
      trailing: IconButton(
        tooltip: 'URL をコピー',
        icon: const Icon(Icons.copy),
        onPressed: () {
          Clipboard.setData(ClipboardData(text: url));
          ScaffoldMessenger.of(context)
              .showSnackBar(const SnackBar(content: Text('URL をコピーしました')));
        },
      ),
    );
    return Scaffold(
      appBar: AppBar(title: const Text('このアプリについて')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Text('$appName　バージョン $appVersion', style: theme.textTheme.titleLarge),
          const Text('かながわコネクトオーケストラ'),
          const SizedBox(height: 16),
          Text('データの扱い', style: theme.textTheme.titleMedium),
          const SizedBox(height: 4),
          const Text(
            '・ログインしなければ、記録はこの端末の中だけに保存します。\n'
            '・ログインすると、練習記録をクラウド（Google Firebase）に保存して、ほかの端末と同期します。本人しか読めません。\n'
            '・マイクの音・録音・AI の処理は、すべて端末の中だけで行い、保存・送信しません。\n'
            '・広告・行動の追跡・利用状況の分析は使っていません。',
          ),
          const SizedBox(height: 8),
          link('プライバシーポリシー', privacyPolicyUrl),
          link('お問い合わせ', contactUrl),
          const SizedBox(height: 8),
          OutlinedButton(
            onPressed: () => showLicensePage(
              context: context,
              applicationName: appName,
              applicationVersion: appVersion,
            ),
            child: const Text('使っている部品のライセンス'),
          ),
        ],
      ),
    );
  }
}
