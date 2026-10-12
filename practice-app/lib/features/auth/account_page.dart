import 'package:flutter/material.dart';

import '../../app/about_page.dart';
import '../../app/app_services.dart';
import '../sync/sync_controller.dart';
import 'auth_service.dart';

/// ログインとクラウド同期の状態
class AccountPage extends StatelessWidget {
  const AccountPage({super.key});

  @override
  Widget build(BuildContext context) {
    final services = AppScope.of(context);
    return Scaffold(
      appBar: AppBar(
        title: const Text('アカウント'),
        actions: [
          IconButton(
            tooltip: 'このアプリについて',
            icon: const Icon(Icons.info_outline),
            onPressed: () => Navigator.of(
              context,
            ).push(MaterialPageRoute<void>(builder: (_) => const AboutPage())),
          ),
        ],
      ),
      body: ListenableBuilder(
        listenable: services.sync,
        builder: (context, _) {
          final sync = services.sync;
          if (sync.status == SyncStatus.connecting) {
            return const _Message(
              icon: Icons.cloud_sync_outlined,
              text: 'クラウドに接続しています…\nそのあいだも練習記録はこの端末に保存されます。',
            );
          }
          if (!sync.isAvailable) {
            return const _Message(
              icon: Icons.cloud_off,
              text:
                  'いまはクラウド同期を使えません（オフライン、またはこの端末は未対応）。\n'
                  '練習記録はこの端末の中に保存されています。\n'
                  'インターネットにつながったら、アプリを開き直すと同期できます。',
            );
          }
          final user = sync.user;
          if (user == null) return _SignInForm(auth: sync.auth!);
          return _SignedIn(user: user, sync: sync, auth: sync.auth!);
        },
      ),
    );
  }
}

class _Message extends StatelessWidget {
  const _Message({required this.icon, required this.text});

  final IconData icon;
  final String text;

  @override
  Widget build(BuildContext context) => Center(
    child: Padding(
      padding: const EdgeInsets.all(24),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 48),
          const SizedBox(height: 16),
          Text(text, textAlign: TextAlign.center),
        ],
      ),
    ),
  );
}

class _SignedIn extends StatelessWidget {
  const _SignedIn({required this.user, required this.sync, required this.auth});

  final AppUser user;
  final SyncController sync;
  final AuthService auth;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final (icon, text) = switch (sync.status) {
      SyncStatus.syncing => (Icons.sync, '同期しています…'),
      SyncStatus.error => (Icons.sync_problem, sync.lastError ?? '同期できませんでした'),
      _ when sync.lastSyncedAt != null => (
        Icons.cloud_done_outlined,
        '同期しました（${_time(sync.lastSyncedAt!)}）',
      ),
      _ => (Icons.cloud_outlined, 'まだ同期していません'),
    };
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        ListTile(
          leading: const Icon(Icons.account_circle, size: 40),
          title: Text(user.displayName ?? user.email ?? 'ログイン中'),
          subtitle: user.displayName != null && user.email != null
              ? Text(user.email!)
              : null,
        ),
        Card(
          color: sync.status == SyncStatus.error
              ? theme.colorScheme.errorContainer
              : null,
          child: ListTile(leading: Icon(icon), title: Text(text)),
        ),
        const SizedBox(height: 8),
        Text(
          '練習記録はこの端末に保存され、インターネットにつながっているときにクラウドと同期します。'
          '別の端末で同じアカウントにログインすると、記録を引き継げます。',
          style: theme.textTheme.bodySmall,
        ),
        const SizedBox(height: 16),
        FilledButton.icon(
          onPressed: sync.status == SyncStatus.syncing ? null : sync.syncNow,
          icon: const Icon(Icons.sync),
          label: const Text('今すぐ同期'),
        ),
        const SizedBox(height: 8),
        OutlinedButton.icon(
          onPressed: () async {
            final ok = await showDialog<bool>(
              context: context,
              builder: (context) => AlertDialog(
                title: const Text('ログアウトしますか？'),
                content: const Text(
                  'ログアウトすると、このアカウントの記録はこの端末に表示されなくなります（もう一度ログインすれば表示されます）。',
                ),
                actions: [
                  TextButton(
                    onPressed: () => Navigator.pop(context, false),
                    child: const Text('やめる'),
                  ),
                  FilledButton(
                    onPressed: () => Navigator.pop(context, true),
                    child: const Text('ログアウト'),
                  ),
                ],
              ),
            );
            if (ok == true) await auth.signOut();
          },
          icon: const Icon(Icons.logout),
          label: const Text('ログアウト'),
        ),
      ],
    );
  }

  static String _time(DateTime t) {
    final l = t.toLocal();
    return '${l.month}/${l.day} ${l.hour}:${l.minute.toString().padLeft(2, '0')}';
  }
}

class _SignInForm extends StatefulWidget {
  const _SignInForm({required this.auth});

  final AuthService auth;

  @override
  State<_SignInForm> createState() => _SignInFormState();
}

class _SignInFormState extends State<_SignInForm> {
  final _email = TextEditingController();
  final _password = TextEditingController();
  bool _busy = false;
  String? _error;
  String? _info;

  @override
  void dispose() {
    _email.dispose();
    _password.dispose();
    super.dispose();
  }

  Future<void> _run(Future<void> Function() action, {String? success}) async {
    setState(() {
      _busy = true;
      _error = null;
      _info = null;
    });
    try {
      await action();
      if (mounted && success != null) setState(() => _info = success);
    } on AuthFailure catch (e) {
      if (mounted) setState(() => _error = e.message);
    } finally {
      if (mounted) setState(() => _busy = false);
    }
  }

  bool get _hasEmailAndPassword =>
      _email.text.trim().isNotEmpty && _password.text.isNotEmpty;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        Text(
          'ログインしなくても使えます。ログインすると、練習記録をクラウドに保存して、ほかの端末と同期できます。',
          style: theme.textTheme.bodyMedium,
        ),
        const SizedBox(height: 16),
        FilledButton.icon(
          onPressed: _busy ? null : () => _run(widget.auth.signInWithGoogle),
          icon: const Icon(Icons.login),
          label: const Text('Google でログイン'),
        ),
        const SizedBox(height: 24),
        Text('メールアドレスでログイン', style: theme.textTheme.titleMedium),
        const SizedBox(height: 8),
        TextField(
          controller: _email,
          keyboardType: TextInputType.emailAddress,
          autofillHints: const [AutofillHints.email],
          decoration: const InputDecoration(
            labelText: 'メールアドレス',
            border: OutlineInputBorder(),
          ),
          onChanged: (_) => setState(() {}),
        ),
        const SizedBox(height: 8),
        TextField(
          controller: _password,
          obscureText: true,
          autofillHints: const [AutofillHints.password],
          decoration: const InputDecoration(
            labelText: 'パスワード（6文字以上）',
            border: OutlineInputBorder(),
          ),
          onChanged: (_) => setState(() {}),
        ),
        const SizedBox(height: 8),
        Row(
          children: [
            Expanded(
              child: FilledButton.tonal(
                onPressed: _busy || !_hasEmailAndPassword
                    ? null
                    : () => _run(
                        () => widget.auth.signInWithEmail(
                          _email.text,
                          _password.text,
                        ),
                      ),
                child: const Text('ログイン'),
              ),
            ),
            const SizedBox(width: 8),
            Expanded(
              child: OutlinedButton(
                onPressed: _busy || !_hasEmailAndPassword
                    ? null
                    : () => _run(
                        () => widget.auth.signUpWithEmail(
                          _email.text,
                          _password.text,
                        ),
                      ),
                child: const Text('新規登録'),
              ),
            ),
          ],
        ),
        TextButton(
          onPressed: _busy || _email.text.trim().isEmpty
              ? null
              : () => _run(
                  () => widget.auth.sendPasswordReset(_email.text),
                  success: 'パスワード再設定のメールを送りました',
                ),
          child: const Text('パスワードを忘れた'),
        ),
        if (_error != null)
          Text(_error!, style: TextStyle(color: theme.colorScheme.error)),
        if (_info != null) Text(_info!),
      ],
    );
  }
}
