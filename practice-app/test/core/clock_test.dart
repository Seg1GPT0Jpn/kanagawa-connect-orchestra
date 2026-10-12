import 'package:flutter_test/flutter_test.dart';
import 'package:kco_practice/core/clock.dart';
import 'package:kco_practice/core/ids.dart';

void main() {
  test('formatPracticeTime：1分未満は秒、それ以上は分（切り捨て）', () {
    expect(formatPracticeTime(0), '0秒');
    expect(formatPracticeTime(59), '59秒');
    expect(formatPracticeTime(60), '1分');
    expect(formatPracticeTime(1399), '23分');
  });

  test('formatSeconds：m:ss、負の値は予定超過の +m:ss', () {
    expect(formatSeconds(1200), '20:00');
    expect(formatSeconds(65), '1:05');
    expect(formatSeconds(0), '0:00');
    expect(formatSeconds(-30), '+0:30');
  });

  test('localDateString：端末のローカル日付', () {
    expect(localDateString(DateTime(2026, 1, 5, 23, 59)), '2026-01-05');
  });

  test('generateId：20文字の英数字で、毎回違う', () {
    final ids = {for (var i = 0; i < 1000; i++) generateId()};
    expect(ids, hasLength(1000));
    expect(
      ids.every((id) => RegExp(r'^[A-Za-z0-9]{20}$').hasMatch(id)),
      isTrue,
    );
  });
}
