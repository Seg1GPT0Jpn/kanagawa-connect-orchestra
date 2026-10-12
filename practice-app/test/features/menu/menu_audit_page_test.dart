import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:kco_practice/app/app.dart';

void main() {
  testWidgets('初期値は合計75分でルールを満たし、範囲外にすると警告と修正ボタンが出る', (tester) async {
    // スマホの縦長画面（ListView の下の方まで描画されるように）
    tester.view.physicalSize = const Size(430, 1400);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.reset);
    await tester.pumpWidget(const KcoPracticeApp());

    expect(find.text('合計 75分（45〜115分）'), findsOneWidget);
    expect(find.text('ルールを満たしています'), findsOneWidget);
    expect(find.text('ルールに合わせて直す'), findsNothing);

    // マウスピースのスライダーを左端（0分）へ
    final slider = find.byType(Slider).first;
    await tester.drag(slider, const Offset(-1000, 0));
    await tester.pump();

    expect(find.text('マウスピース：0分は短すぎます（15〜30分）'), findsOneWidget);
    await tester.scrollUntilVisible(find.text('ルールに合わせて直す'), 100);
    await tester.tap(find.text('ルールに合わせて直す'));
    await tester.pump();

    expect(find.text('ルールを満たしています'), findsOneWidget);
    expect(find.text('合計 70分（45〜115分）'), findsOneWidget);
  });
}
