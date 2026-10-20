import 'dart:async';

import 'package:flutter/foundation.dart';

import '../../../core/clock.dart';
import '../../../core/meta_store.dart';

/// 道具ごとの使った時間（目標・カレンダー用。端末内だけ）
enum UsageKind {
  practice('練習（タイマー）'),
  metronome('メトロノーム'),
  tuner('チューナー'),
  tone('基準音'),
  recording('録音');

  const UsageKind(this.label);
  final String label;
}

/// 道具が動いている時間を、日ごとに数えて保存する
class UsageTracker extends ChangeNotifier {
  UsageTracker(this._meta, {this._clock = systemClock});

  final MetaStore _meta;
  final Clock _clock;
  final Map<UsageKind, DateTime> _running = {};

  /// 読み込み済みの日ごとの秒数
  final Map<String, Map<UsageKind, int>> _days = {};

  /// [isActive] が true の間を [kind] の時間として数える
  void watch(UsageKind kind, Listenable source, bool Function() isActive) {
    source.addListener(() => _update(kind, isActive()));
  }

  void _update(UsageKind kind, bool active) {
    final started = _running[kind];
    if (active && started == null) {
      _running[kind] = _clock();
    } else if (!active && started != null) {
      _running.remove(kind);
      unawaited(add(kind, _clock().difference(started)));
    }
  }

  /// [kind] に [d] を足す（始めた日の分として）
  Future<void> add(UsageKind kind, Duration d, {DateTime? at}) async {
    if (d.inSeconds <= 0) return;
    final day = localDateString(at ?? _clock());
    final m = await _load(day);
    m[kind] = (m[kind] ?? 0) + d.inSeconds;
    notifyListeners();
    await _meta.put('usage.$day', {
      for (final e in m.entries) e.key.name: e.value,
    });
  }

  Future<Map<UsageKind, int>> _load(String day) async {
    final cached = _days[day];
    if (cached != null) return cached;
    final raw = await _meta.get('usage.$day');
    final m = <UsageKind, int>{};
    if (raw is Map) {
      for (final k in UsageKind.values) {
        final v = raw[k.name];
        if (v is int && v > 0) m[k] = v;
      }
    }
    return _days[day] = m;
  }

  /// [day]（yyyy-MM-dd）の、道具ごとの秒数（いま動いている分も含む）
  Future<Map<UsageKind, int>> secondsOn(String day) async {
    final m = {...await _load(day)};
    if (day == localDateString(_clock())) {
      for (final MapEntry(:key, :value) in _running.entries) {
        m[key] = (m[key] ?? 0) + _clock().difference(value).inSeconds;
      }
    }
    return m;
  }
}

/// 1日の目標（分。0 なら目標なし）
class DailyGoals {
  const DailyGoals([this.minutes = const {UsageKind.practice: 30}]);

  final Map<UsageKind, int> minutes;

  int of(UsageKind k) => minutes[k] ?? 0;

  DailyGoals withGoal(UsageKind k, int m) =>
      DailyGoals({...minutes, k: m.clamp(0, 600)});

  bool get isEmpty => minutes.values.every((v) => v <= 0);

  Map<String, Object?> toMap() => {
    for (final e in minutes.entries) e.key.name: e.value,
  };

  factory DailyGoals.fromMap(Map<Object?, Object?> m) => DailyGoals({
    for (final k in UsageKind.values)
      if (m[k.name] case final int v when v > 0) k: v.clamp(0, 600),
  });

  static Future<DailyGoals> load(MetaStore meta) async {
    final raw = await meta.get('goals.daily');
    return raw is Map ? DailyGoals.fromMap(raw) : const DailyGoals();
  }

  Future<void> save(MetaStore meta) => meta.put('goals.daily', toMap());
}

/// 1日の目標の設定（保存する）
class GoalsController extends ChangeNotifier {
  GoalsController(this._meta, this._goals);

  static Future<GoalsController> load(MetaStore meta) async =>
      GoalsController(meta, await DailyGoals.load(meta));

  final MetaStore _meta;
  DailyGoals _goals;

  DailyGoals get goals => _goals;

  Future<void> setGoal(UsageKind kind, int minutes) async {
    _goals = _goals.withGoal(kind, minutes);
    notifyListeners();
    await _goals.save(_meta);
  }
}
