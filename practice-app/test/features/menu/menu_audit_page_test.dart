import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:kco_practice/features/menu/domain/menu_rules.dart';
import 'package:kco_practice/features/menu/presentation/menu_audit_page.dart';

void main() {
  void phoneSize(WidgetTester tester) {
    // スマホの縦長画面（ListView の下の方まで描画されるように）
    tester.view.physicalSize = const Size(430, 1400);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.reset);
  }

  testWidgets('初期値は合計75分でルールを満たし、範囲外にすると警告と修正ボタンが出る', (tester) async {
    phoneSize(tester);
    await tester.pumpWidget(
      const MaterialApp(home: MenuAuditPage(rules: trumpetBasicRules)),
    );

    expect(find.text('合計 75分（45〜115分）'), findsOneWidget);
    expect(find.text('ルールを満たしています'), findsOneWidget);
    expect(find.text('ルールに合わせて直す'), findsNothing);
    expect(find.text('このメニューを保存'), findsNothing); // onSave なし

    // マウスピースのスライダーを左端（0分）へ
    await tester.drag(find.byType(Slider).first, const Offset(-1000, 0));
    await tester.pump();

    expect(find.text('マウスピース：0分は短すぎます（15〜30分）'), findsOneWidget);
    await tester.tap(find.text('ルールに合わせて直す'));
    await tester.pump();

    expect(find.text('ルールを満たしています'), findsOneWidget);
    expect(find.text('合計 70分（45〜115分）'), findsOneWidget);
  });

  testWidgets('変更してルールを満たすときだけ保存でき、違反中は保存ボタンが出ない', (tester) async {
    phoneSize(tester);
    Map<String, int>? saved;
    await tester.pumpWidget(
      MaterialApp(
        home: MenuAuditPage(
          rules: trumpetBasicRules,
          initialMinutes: trumpetBasicRules.defaultMenu,
          onSave: (m) async => saved = m,
        ),
      ),
    );
    expect(find.text('このメニューを保存'), findsNothing); // 変更なし

    await tester.drag(find.byType(Slider).first, const Offset(-1000, 0));
    await tester.pump();
    expect(find.text('このメニューを保存'), findsNothing); // 違反中

    await tester.tap(find.text('ルールに合わせて直す'));
    await tester.pump();
    await tester.tap(find.text('このメニューを保存'));
    await tester.pump();
    expect(saved?['mouthpiece'], 15);
    expect(find.text('メニューを保存しました'), findsOneWidget);
  });
}
