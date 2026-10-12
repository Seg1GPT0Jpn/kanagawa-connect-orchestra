import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:kco_practice/app/about_page.dart';
import 'package:kco_practice/app/app_info.dart';

void main() {
  test('appVersion は pubspec.yaml の version と同じ', () {
    final pubspec = File('pubspec.yaml').readAsStringSync();
    final m = RegExp(
      r'^version:\s*([0-9.]+)\+\d+',
      multiLine: true,
    ).firstMatch(pubspec)!;
    expect(appVersion, m.group(1));
  });

  test('プライバシーポリシーのページが Web 版に含まれる', () {
    final html = File('web/privacy.html').readAsStringSync();
    expect(html, contains('プライバシーポリシー'));
    expect(html, contains(contactUrl));
    expect(privacyPolicyUrl, endsWith('/privacy.html'));
  });

  testWidgets('このアプリについて：版・データの扱い・ライセンス', (tester) async {
    await tester.pumpWidget(const MaterialApp(home: AboutPage()));
    expect(find.textContaining('バージョン $appVersion'), findsOneWidget);
    expect(find.textContaining('端末の中だけで行い'), findsOneWidget);
    await tester.tap(find.text('使っている部品のライセンス'));
    await tester.pumpAndSettle();
    expect(find.byType(LicensePage), findsOneWidget);
  });
}
