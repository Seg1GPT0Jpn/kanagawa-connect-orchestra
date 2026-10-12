import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:kco_practice/features/menu/domain/menu_presets.dart';
import 'package:kco_practice/features/menu/domain/menu_rules.dart';
import 'package:kco_practice/features/menu/presentation/menu_audit_page.dart';

void main() {
  void phoneSize(WidgetTester tester) {
    tester.view.physicalSize = const Size(430, 1400);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.reset);
  }

  /// 画面の下の方にあるものは、スクロールしてから探す
  Future<Finder> scrollTo(WidgetTester tester, Finder f) async {
    await tester.scrollUntilVisible(
      f,
      300,
      scrollable: find.byType(Scrollable).first,
    );
    return f;
  }

  testWidgets('初期値は合計75分でルールを満たし、範囲外にすると警告と修正ボタンが出る', (tester) async {
    phoneSize(tester);
    await tester.pumpWidget(
      const MaterialApp(home: MenuAuditPage(rules: trumpetBasicRules)),
    );

    expect(find.text('今日の重点（おすすめ）'), findsNothing); // presets なし
    expect(find.text('Arban'), findsOneWidget);
    expect(find.text('合計 30分'), findsOneWidget); // Arban の合計
    expect(
      await scrollTo(tester, find.text('合計 75分（45〜115分）')),
      findsOneWidget,
    );
    expect(find.text('ルールを満たしています'), findsOneWidget);
    expect(find.text('このメニューを保存'), findsNothing); // onSave なし

    // マウスピースのスライダーを左端（0分）へ
    await tester.scrollUntilVisible(
      find.text('マウスピース'),
      -300,
      scrollable: find.byType(Scrollable).first,
    );
    await tester.drag(find.byType(Slider).first, const Offset(-1000, 0));
    await tester.pump();

    await tester.tap(await scrollTo(tester, find.text('ルールに合わせて直す')));
    await tester.pump();
    expect(find.text('ルールを満たしています'), findsOneWidget);
    expect(find.text('合計 70分（45〜115分）'), findsOneWidget);
  });

  testWidgets('今日の重点を選ぶとメニューが変わり、変更があってルールを満たすときだけ保存できる', (tester) async {
    phoneSize(tester);
    Map<String, int>? saved;
    await tester.pumpWidget(
      MaterialApp(
        home: MenuAuditPage(
          rules: trumpetBasicRules,
          initialMinutes: trumpetBasicRules.defaultMenu,
          onSave: (m) async => saved = m,
          presets: trumpetBasicPresets,
        ),
      ),
    );
    expect(find.text('今日の重点（おすすめ）'), findsOneWidget);
    expect(find.text('このメニューを保存'), findsNothing); // 変更なし

    await tester.tap(find.text('タンギング').first); // おすすめのチップ
    await tester.pump();
    expect(find.text('合計 30分'), findsOneWidget); // Arban の合計（5+5+20）

    await tester.tap(await scrollTo(tester, find.text('このメニューを保存')));
    await tester.pump();
    expect(saved?['arban_tonguing'], 20);
    expect(saved?['tonguing'], 10);
    expect(find.text('メニューを保存しました'), findsOneWidget);
  });

  testWidgets('Arban の合計が足りないと警告が出て、保存ボタンは出ない', (tester) async {
    phoneSize(tester);
    await tester.pumpWidget(
      MaterialApp(
        home: MenuAuditPage(
          rules: trumpetBasicRules,
          initialMinutes: {
            ...trumpetBasicRules.defaultMenu,
            'arban_scales': 0,
            'arban_tonguing': 0,
          },
          onSave: (_) async {},
        ),
      ),
    );
    expect(find.text('合計 10分'), findsOneWidget);
    expect(
      await scrollTo(tester, find.text('Arbanの合計10分は短すぎます（20〜40分）')),
      findsOneWidget,
    );
    expect(find.text('このメニューを保存'), findsNothing);
  });
}
