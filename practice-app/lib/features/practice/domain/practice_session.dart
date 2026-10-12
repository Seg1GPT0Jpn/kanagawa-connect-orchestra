/// 練習タイマー（メニューの項目を順番に計る）
///
/// 経過時間は「いつ始めたか」と時刻の差で計算する（1秒ごとの数え上げはしない）。
/// そのため画面が止まったりアプリが裏に回ったりしても時間がずれない。
/// 時刻はすべて引数で受け取るので、テストで結果が決まる。
library;

import '../../menu/domain/menu_rules.dart';

class TimerSegment {
  const TimerSegment({
    required this.itemId,
    required this.label,
    required this.plannedSeconds,
  });

  final String itemId;
  final String label;
  final int plannedSeconds;
}

class PracticeSession {
  PracticeSession({required this.segments, required this.startedAt})
    : assert(segments.isNotEmpty),
      _runningSince = startedAt;

  /// メニュー（項目 id → 分）から、0分の項目を除いてタイマーを作る
  factory PracticeSession.fromMenu(
    Map<String, int> minutes,
    MenuRuleSet rules,
    DateTime now,
  ) {
    final segments = [
      for (final item in rules.items)
        if ((minutes[item.id] ?? 0) > 0)
          TimerSegment(
            itemId: item.id,
            label: rules.labelOf(item.id),
            plannedSeconds: minutes[item.id]! * 60,
          ),
    ];
    return PracticeSession(segments: segments, startedAt: now);
  }

  final List<TimerSegment> segments;
  final DateTime startedAt;

  int _index = 0;

  /// 今の項目で、一時停止より前に計った時間
  Duration _banked = Duration.zero;

  /// 動いているときは今の区間を始めた時刻、一時停止中は null
  DateTime? _runningSince;
  final Map<String, int> _actualSeconds = {};
  bool _finished = false;

  int get index => _index;
  TimerSegment get current => segments[_index];
  bool get isRunning => _runningSince != null && !_finished;
  bool get isFinished => _finished;
  bool get isLast => _index == segments.length - 1;

  /// 今の項目の経過秒
  int elapsedSeconds(DateTime now) {
    final running = _runningSince == null
        ? Duration.zero
        : _nonNegative(now.difference(_runningSince!));
    return (_banked + running).inSeconds;
  }

  /// 今の項目の残り秒（負の値は予定超過）
  int remainingSeconds(DateTime now) =>
      current.plannedSeconds - elapsedSeconds(now);

  void pause(DateTime now) {
    if (!isRunning) return;
    _banked += _nonNegative(now.difference(_runningSince!));
    _runningSince = null;
  }

  void resume(DateTime now) {
    if (_finished || _runningSince != null) return;
    _runningSince = now;
  }

  /// 今の項目を終えて次へ。最後の項目なら終了する
  void next(DateTime now) {
    if (_finished) return;
    final wasRunning = isRunning;
    _actualSeconds[current.itemId] =
        (_actualSeconds[current.itemId] ?? 0) + elapsedSeconds(now);
    _banked = Duration.zero;
    if (isLast) {
      _finished = true;
      _runningSince = null;
    } else {
      _index++;
      _runningSince = wasRunning ? now : null;
    }
  }

  /// 途中でも終了し、項目ごとの実績（秒）を返す。まだの項目は 0 秒
  Map<String, int> finish(DateTime now) {
    if (!_finished) {
      _actualSeconds[current.itemId] =
          (_actualSeconds[current.itemId] ?? 0) + elapsedSeconds(now);
      _finished = true;
      _runningSince = null;
      _banked = Duration.zero;
    }
    return {for (final s in segments) s.itemId: _actualSeconds[s.itemId] ?? 0};
  }

  /// 時計が戻った（端末の時刻変更など）ときに経過時間が負にならないように
  static Duration _nonNegative(Duration d) => d.isNegative ? Duration.zero : d;
}
