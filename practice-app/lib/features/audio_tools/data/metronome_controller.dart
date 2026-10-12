import 'dart:async';

import 'package:flutter/foundation.dart';

import '../../../core/meta_store.dart';
import '../domain/metronome.dart';
import 'audio_engine.dart';

/// メトロノームを動かす：少し先までのクリックを、音の時計の正確な時刻に予約し続ける
class MetronomeController extends ChangeNotifier {
  MetronomeController(this._engine, this._meta, MetronomeSettings initial)
    : _settings = initial;

  static Future<MetronomeController> load(
    AudioEngine engine,
    MetaStore meta,
  ) async {
    final raw = await meta.get('metronome.settings');
    return MetronomeController(
      engine,
      meta,
      raw is Map ? MetronomeSettings.fromMap(raw) : const MetronomeSettings(),
    );
  }

  /// 鳴らし始めたとき（ほかのクリックを止めるため）
  VoidCallback? onStarted;

  final AudioEngine _engine;
  final MetaStore _meta;
  MetronomeSettings _settings;

  /// どれだけ先まで予約するか
  static const lookahead = Duration(milliseconds: 200);

  /// 予約を足す間隔
  static const tickInterval = Duration(milliseconds: 25);

  /// 開始ボタンから最初の音までの余裕
  static const startLead = Duration(milliseconds: 100);

  Timer? _timer;

  /// 1拍目を鳴らす音の時計の時刻
  Duration? _anchor;

  /// ここまで（開始からの時刻）予約した
  Duration _scheduledUntil = Duration.zero;
  String? _error;
  final List<Duration> _taps = [];

  MetronomeSettings get settings => _settings;
  bool get isRunning => _timer != null;
  String? get error => _error;

  /// いま何拍目か（小節内、0から）。止まっていれば null
  int? get currentBeat {
    final a = _anchor;
    if (!isRunning || a == null) return null;
    final elapsed = _engine.now - a;
    if (elapsed.isNegative) return null;
    return clickAt(
      _settings,
      _settings.clickIndexAt(elapsed.inMicroseconds),
    ).beatInBar;
  }

  Future<void> start() async {
    if (isRunning) return;
    try {
      await _engine.ensureStarted();
    } on AudioEngineException catch (e) {
      _error = e.message;
      notifyListeners();
      return;
    }
    _error = null;
    onStarted?.call();
    _anchor = _engine.now + startLead;
    _scheduledUntil = Duration.zero;
    _timer = Timer.periodic(tickInterval, (_) => _pump());
    _pump();
    notifyListeners();
  }

  void stop() {
    _timer?.cancel();
    _timer = null;
    _anchor = null;
    _engine.cancelScheduledClicks();
    notifyListeners();
  }

  Future<void> toggle() => isRunning ? Future.sync(stop) : start();

  /// 予約が先読みの範囲に届くまでクリックを足す（画面の更新もここで促す）
  void _pump() {
    final a = _anchor;
    if (a == null) return;
    final horizon = _engine.now - a + lookahead;
    if (horizon > _scheduledUntil) {
      for (final c in clicksBetween(_settings, _scheduledUntil, horizon)) {
        _engine.scheduleClick(c.kind, a + c.offset);
      }
      _scheduledUntil = horizon;
    }
    notifyListeners();
  }

  /// 設定を変える。動いていれば、予約し直して新しいテンポで続ける
  Future<void> update(MetronomeSettings s) async {
    final next = s.normalized();
    if (next == _settings) return;
    _settings = next;
    if (isRunning) {
      _engine.cancelScheduledClicks();
      _anchor = _engine.now + startLead;
      _scheduledUntil = Duration.zero;
      _pump();
    }
    notifyListeners();
    await _meta.put('metronome.settings', next.toMap());
  }

  /// タップでテンポを決める（[at] は単調に増える時刻）
  Future<void> tap(Duration at) async {
    if (_taps.isNotEmpty && at - _taps.last > const Duration(seconds: 2)) {
      _taps.clear();
    }
    _taps.add(at);
    if (_taps.length > 9) _taps.removeAt(0);
    final bpm = tapTempo(_taps);
    if (bpm != null) await update(_settings.copyWith(bpm: bpm));
  }

  @override
  void dispose() {
    stop();
    super.dispose();
  }
}
