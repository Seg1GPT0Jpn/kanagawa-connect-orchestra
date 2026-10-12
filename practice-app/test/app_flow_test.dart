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
        audioOverride: FakeAudioEngine(),
        clock: clock.call,
      ),
    ))!;
  }

  testWidgets('メニューどおりに練習して記録すると、記録タブと集計に出る', (tester) async {
    final s = await services(tester);
    await tester.pumpWidget(KcoPracticeApp(services: s));
    await tester.pumpAndSettle();

    expect(find.text('80分'), findsOneWidget); // 合計
    expect(find.text('Arban'), findsOneWidget);
    expect(find.text('30分'), findsOneWidget); // Arban の合計（今日吹く章：スラー・音階・タンギング）
    expect(find.text('音階'), findsOneWidget);
    expect(find.text('二重奏'), findsNothing); // 0分の章は出さない
    expect(find.text('曲・エチュード'), findsOneWidget);

    await tester.tap(find.text('練習をはじめる'));
    await tester.pumpAndSettle();
    expect(find.text('1 / 8'), findsOneWidget);
    expect(find.text('5:00'), findsOneWidget);
    expect(find.text('Arban：スラー'), findsOneWidget);

    // ウォームアップを4分で次へ、ロングトーンを途中（10分）で終える
    clock.advance(const Duration(minutes: 4));
    await tester.pump(const Duration(milliseconds: 300));
    expect(find.text('1:00'), findsOneWidget);
    await tester.tap(find.text('次へ'));
    await tester.pump();
    clock.advance(const Duration(minutes: 10));
    await tester.tap(find.text('途中で終える'));
    await tester.pumpAndSettle();
    await tester.tap(find.text('終えて記録').last);
    await tester.runAsync(
      () => Future<void>.delayed(const Duration(milliseconds: 50)),
    );
    await tester.pumpAndSettle();

    expect(find.text('練習を記録しました（14分）'), findsOneWidget);
    final records = (await tester.runAsync(() => s.practice.visible(null)))!;
    expect(records.single.actualSeconds, {
      'mouthpiece': 240,
      'long_tone': 600,
      'lip_slur': 0,
      'tonguing': 0,
      'arban_slurs': 0,
      'arban_scales': 0,
      'arban_tonguing': 0,
      'repertoire': 0,
    });
    expect(records.single.ruleSetId, 'trumpet_basic');
    expect(records.single.ownerUid, isNull); // ログインしていない

    await tester.tap(find.text('記録'));
    await tester.pumpAndSettle();
    expect(find.textContaining('2026-10-12　14分'), findsOneWidget);
    expect(find.textContaining('14分・1日練習・1日連続'), findsOneWidget);

    await tester.tap(find.text('練習').last);
    await tester.pumpAndSettle();
    expect(find.text('14分'), findsWidgets); // 今日・直近7日
  });

  testWidgets('今日の予定と調子からおすすめを選ぶと、今日だけのメニューになり、戻せる', (tester) async {
    final s = await services(tester);
    await tester.pumpWidget(KcoPracticeApp(services: s));
    await tester.pumpAndSettle();
    expect(find.text('いつもどおりのメニューで練習しましょう。'), findsOneWidget);
    expect(find.text('今日はこのおすすめにする'), findsNothing);

    // 合奏がある → 通常モードの「短め（45分）」
    await tester.tap(find.text('合奏・レッスン'));
    await tester.runAsync(
      () => Future<void>.delayed(const Duration(milliseconds: 20)),
    );
    await tester.pumpAndSettle();
    expect(find.textContaining('個人練習は短め（45分）'), findsOneWidget);
    await tester.tap(find.text('今日はこのおすすめにする'));
    await tester.pumpAndSettle();
    expect(find.text('45分'), findsOneWidget); // 合計
    expect(find.text('今日だけのメニューです（保存はしていません）'), findsOneWidget);
    expect(find.text('今日はこのおすすめにする'), findsNothing); // 適用済み
    expect(s.menu.savedMenu['repertoire'], 20); // 保存したメニューは変わらない

    // さらに疲れている → 10分モード
    await tester.tap(find.text('疲れている'));
    await tester.runAsync(
      () => Future<void>.delayed(const Duration(milliseconds: 20)),
    );
    await tester.pumpAndSettle();
    await tester.tap(find.text('今日はこのおすすめにする'));
    await tester.pumpAndSettle();
    expect(s.menu.rules.id, 'trumpet_10min');
    expect(find.text('トランペット基礎メニュー（10分）'), findsOneWidget);
    expect(find.text('10分'), findsOneWidget); // 合計

    // 唇が痛い → 休む（おすすめのボタンは出ない）
    await tester.tap(find.text('唇が痛い'));
    await tester.runAsync(
      () => Future<void>.delayed(const Duration(milliseconds: 20)),
    );
    await tester.pumpAndSettle();
    expect(find.textContaining('今日は吹かずに休みましょう'), findsOneWidget);
    expect(find.text('今日はこのおすすめにする'), findsNothing);

    // 入れた調子は日ごとに残る
    final saved = (await tester.runAsync(
      () => s.dayConditions.load('2026-10-12'),
    ))!;
    expect(
      [saved.rehearsal, saved.lipPain, saved.fatigue.name],
      [true, true, 'tired'],
    );
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
