import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:kco_practice/app/app.dart';
import 'package:kco_practice/app/app_services.dart';

import 'package:kco_practice/features/local_ai/local_ai_service.dart';

import 'helpers.dart';

void main() {
  late FakeClock clock;
  late FakeRemote cloud;
  late FakeAuth auth;
  late FakeLocalAiService ai;

  Future<AppServices> services(
    WidgetTester tester, {
    bool cloudSync = true,
  }) async {
    tester.view.physicalSize = const Size(430, 2600);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.reset);
    clock = FakeClock(DateTime(2026, 10, 12, 18));
    cloud = FakeRemote();
    auth = FakeAuth();
    ai = FakeLocalAiService(state: LocalAiState.unavailable);
    return (await tester.runAsync(
      () async => AppServices.fromParts(
        db: await openMemoryDb(),
        authOverride: cloudSync ? auth : null,
        remoteOverride: cloudSync ? cloud : null,
        audioOverride: FakeAudioEngine(),
        micOverride: FakeMicInput(),
        localAiOverride: ai,
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

    await tester.ensureVisible(find.text('練習をはじめる'));
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
    // 記録のあとは振り返りの画面（あとで書ける）
    expect(find.text('練習の振り返り'), findsOneWidget);
    await tester.tap(find.text('あとで'));
    await tester.pumpAndSettle();
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

  testWidgets('AI コーチ：使えない端末では案内だけ、使える端末ではメニューを相談して今日のメニューにできる', (
    tester,
  ) async {
    final s = await services(tester);
    await tester.pumpWidget(KcoPracticeApp(services: s));
    await tester.pumpAndSettle();
    expect(find.textContaining('内蔵の AI を使えません'), findsOneWidget);
    expect(find.text('メニューを相談'), findsNothing);
  });

  testWidgets('AI コーチ：準備してメニューを相談すると、アプリが確かめた案を今日だけ使える', (tester) async {
    final s = await services(tester);
    ai.state = LocalAiState.needsPreparation;
    ai.replies.add(
      '{"mouthpiece": 5, "long_tone": 20, "lip_slur": 15, "arban_slurs": 20, "repertoire": 10}',
    );
    await tester.pumpWidget(KcoPracticeApp(services: s));
    await tester.pumpAndSettle();

    await tester.tap(find.text('AI を準備する'));
    await tester.runAsync(
      () => Future<void>.delayed(const Duration(milliseconds: 20)),
    );
    await tester.pumpAndSettle();
    await tester.tap(find.text('メニューを相談'));
    await tester.runAsync(
      () => Future<void>.delayed(const Duration(milliseconds: 20)),
    );
    await tester.pumpAndSettle();

    expect(find.text('AI の案（合計70分）'), findsOneWidget);
    expect(ai.prompts.single, contains('JSON だけ'));
    await tester.tap(find.text('今日はこの案にする'));
    await tester.pumpAndSettle();
    expect(s.menu.isTemporary, isTrue);
    expect(s.menu.value['lip_slur'], 15);
    expect(s.menu.savedMenu['lip_slur'], 5); // 保存したメニューは変わらない
    expect(find.text('70分'), findsOneWidget); // 練習タブの合計
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
