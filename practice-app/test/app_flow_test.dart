import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:kco_practice/app/app.dart';
import 'package:kco_practice/app/app_services.dart';

import 'helpers.dart';

void main() {
  late FakeClock clock;
  late FakeRemote cloud;
  late FakeAuth auth;

  Future<AppServices> services(
    WidgetTester tester, {
    bool cloudSync = true,
  }) async {
    tester.view.physicalSize = const Size(430, 1400);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.reset);
    clock = FakeClock(DateTime(2026, 10, 12, 18));
    cloud = FakeRemote();
    auth = FakeAuth();
    return (await tester.runAsync(
      () async => AppServices.fromParts(
        db: await openMemoryDb(),
        authOverride: cloudSync ? auth : null,
        remoteOverride: cloudSync ? cloud : null,
        clock: clock.call,
      ),
    ))!;
  }

  testWidgets('メニューどおりに練習して記録すると、記録タブと集計に出る', (tester) async {
    final s = await services(tester);
    await tester.pumpWidget(KcoPracticeApp(services: s));
    await tester.pumpAndSettle();

    expect(find.text('75分'), findsOneWidget); // 合計
    await tester.tap(find.text('練習をはじめる'));
    await tester.pumpAndSettle();
    expect(find.text('1 / 5'), findsOneWidget);
    expect(find.text('20:00'), findsOneWidget);

    // 1項目めを18分で次へ、2項目めを途中（5分）で終える
    clock.advance(const Duration(minutes: 18));
    await tester.pump(const Duration(milliseconds: 300));
    expect(find.text('2:00'), findsOneWidget);
    await tester.tap(find.text('次へ'));
    await tester.pump();
    clock.advance(const Duration(minutes: 5));
    await tester.tap(find.text('途中で終える'));
    await tester.pumpAndSettle();
    await tester.tap(find.text('終えて記録').last);
    await tester.runAsync(
      () => Future<void>.delayed(const Duration(milliseconds: 50)),
    );
    await tester.pumpAndSettle();

    expect(find.text('練習を記録しました（23分）'), findsOneWidget);
    final records = (await tester.runAsync(() => s.practice.visible(null)))!;
    expect(records.single.actualSeconds, {
      'mouthpiece': 1080,
      'long_tone': 300,
      'lip_slur': 0,
      'tonguing': 0,
      'arban': 0,
    });
    expect(records.single.ownerUid, isNull); // ログインしていない

    await tester.tap(find.text('記録'));
    await tester.pumpAndSettle();
    expect(find.textContaining('2026-10-12　23分'), findsOneWidget);
    expect(find.textContaining('23分・1日練習・1日連続'), findsOneWidget);

    await tester.tap(find.text('練習').last);
    await tester.pumpAndSettle();
    expect(find.text('23分'), findsWidgets); // 今日・直近7日
  });

  testWidgets('Firebase がない端末では、アカウントタブに端末内保存の案内が出る', (tester) async {
    final s = await services(tester, cloudSync: false);
    await tester.pumpWidget(KcoPracticeApp(services: s));
    await tester.pumpAndSettle();
    await tester.tap(find.text('アカウント'));
    await tester.pumpAndSettle();
    expect(find.textContaining('クラウド同期を使えません'), findsOneWidget);
  });

  testWidgets('ログインすると同期状態が出て、ログアウトできる', (tester) async {
    final s = await services(tester);
    await tester.pumpWidget(KcoPracticeApp(services: s));
    await tester.pumpAndSettle();
    await tester.tap(find.text('アカウント'));
    await tester.pumpAndSettle();

    // メールアドレスでログイン（パスワード違い → エラー表示）
    await tester.enterText(
      find.widgetWithText(TextField, 'メールアドレス'),
      'a@example.com',
    );
    await tester.enterText(
      find.widgetWithText(TextField, 'パスワード（6文字以上）'),
      'wrong',
    );
    await tester.pump();
    await tester.tap(find.text('ログイン'));
    await tester.pump();
    expect(find.text('メールアドレスかパスワードが違います'), findsOneWidget);

    await tester.tap(find.text('Google でログイン'));
    await tester.runAsync(
      () => Future<void>.delayed(const Duration(milliseconds: 50)),
    );
    await tester.pumpAndSettle();
    expect(find.text('u1@example.com'), findsOneWidget);
    expect(find.textContaining('同期しました'), findsOneWidget);

    await tester.tap(find.text('ログアウト'));
    await tester.pumpAndSettle();
    await tester.tap(find.widgetWithText(FilledButton, 'ログアウト'));
    await tester.pumpAndSettle();
    expect(find.text('Google でログイン'), findsOneWidget);
  });
}
