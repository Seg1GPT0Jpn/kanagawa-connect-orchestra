/// 現在時刻を返す関数。テストでは固定の時刻を渡す
typedef Clock = DateTime Function();

DateTime systemClock() => DateTime.now();

/// 端末のローカル日付（yyyy-MM-dd）
String localDateString(DateTime t) {
  final l = t.toLocal();
  return '${l.year.toString().padLeft(4, '0')}-'
      '${l.month.toString().padLeft(2, '0')}-'
      '${l.day.toString().padLeft(2, '0')}';
}

/// 練習時間を「23分」「45秒」で表す（1分未満は秒）
String formatPracticeTime(int seconds) =>
    seconds < 60 ? '$seconds秒' : '${seconds ~/ 60}分';

/// 秒を「m:ss」で表す（負の値は「+m:ss」＝予定超過）
String formatSeconds(int seconds) {
  final over = seconds < 0;
  final s = seconds.abs();
  final text = '${s ~/ 60}:${(s % 60).toString().padLeft(2, '0')}';
  return over ? '+$text' : text;
}
