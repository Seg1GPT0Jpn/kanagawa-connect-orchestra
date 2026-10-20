import 'dart:async';

import 'package:flutter/foundation.dart';

import '../../../core/meta_store.dart';
import '../domain/metronome.dart';
import '../domain/metronome_plan.dart';
import '../domain/sound.dart';
import 'audio_engine.dart';

/// メトロノームを動かす：少し先までのクリックを、音の時計の正確な時刻に予約し続ける
class MetronomeController extends ChangeNotifier {
  MetronomeController(
    this._engine,
    this._meta,
    MetronomeSettings initial, {
    this._options = const MetronomeOptions(),
  }) : _settings = initial;

  static Future<MetronomeController> load(
    AudioEngine engine,
    MetaStore meta,
  ) async {
    final raw = await meta.get('metronome.settings');
    final opts = await meta.get('metronome.options');
    return MetronomeController(
      engine,
      meta,
      raw is Map ? MetronomeSettings.fromMap(raw) : const MetronomeSettings(),
      options: opts is Map
          ? MetronomeOptions.fromMap(opts)
          : const MetronomeOptions(),
    );
  }

  /// 鳴らし始めたとき（ほかのクリックを止めるため）
  VoidCallback? onStarted;

  final AudioEngine _engine;
  final MetaStore _meta;
  MetronomeSettings _settings;
  MetronomeOptions _options;

  /// どれだけ先まで予約するか
  static const lookahead = Duration(milliseconds: 200);

  /// 予約を足す間隔
  static const tickInterval = Duration(milliseconds: 25);

  /// 開始ボタンから最初の音までの余裕
  static const startLead = Duration(milliseconds: 100);

  Timer? _timer;

  /// 開始（または設定を変えて続けた）時刻。クリックの時刻はここからの経過
  Duration? _anchor;
  Duration? _stopAt;
  MetronomeSequencer? _sequencer;
  final List<PlannedClick> _pending = [];

  /// 予約したクリック（画面の拍の表示に使う。新しいものが後ろ）
  final List<(Duration, PlannedClick)> _recent = [];
  String? _error;
  String? _stoppedReason;
  int _runs = 0;
  final List<Duration> _taps = [];

  MetronomeSettings get settings => _settings;
  MetronomeOptions get options => _options;
  bool get isRunning => _timer != null;
  String? get error => _error;

  /// 自動で止まった理由（タイマー・テンポの目標）。手で止めたら null
  String? get stoppedReason => _stoppedReason;

  /// いま鳴っている（直前に鳴った）拍
  PlannedClick? get _currentClick {
    if (!isRunning) return null;
    final now = _engine.now;
    for (var i = _recent.length - 1; i >= 0; i--) {
      final (at, c) = _recent[i];
      if (!c.poly && at <= now) return c;
    }
    return null;
  }

  /// いま何拍目か（小節内、0から）。止まっていれば null
  int? get currentBeat => _currentClick?.beatInBar;

  /// いまのテンポ（段階変化のときは変わっていく）
  int get currentBpm => _currentClick?.bpm ?? _settings.bpm;

  /// いま何小節目か（0から。カウントイン中は負）
  int? get currentBar => _currentClick?.bar;

  /// いまの拍が休み（鳴らさない拍）か
  bool get currentBeatMuted => _currentClick?.muted ?? false;

  /// いまの拍が強拍か
  bool get currentBeatAccent => _currentClick?.kind == ClickKind.accent;

  /// 拍の中の位置（0〜1。振り子の表示に使う）
  double get beatProgress {
    final c = _currentClick;
    if (c == null) return 0;
    Duration? start;
    for (final (at, p) in _recent.reversed) {
      if (identical(p, c)) {
        start = at;
        break;
      }
    }
    if (start == null) return 0;
    final beat = 60000000 / c.bpm;
    return ((_engine.now - start).inMicroseconds / beat).clamp(0.0, 1.0);
  }

  /// 何拍目から数えて何回目の拍か（振り子の左右を決める）
  int get beatCount =>
      _recent.where((r) => !r.$2.poly && r.$1 <= _engine.now).length;

  /// タイマーの残り（使っていなければ null）
  Duration? get timeLeft {
    final s = _stopAt;
    if (s == null || !isRunning) return null;
    final left = s - _engine.now;
    return left.isNegative ? Duration.zero : left;
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
    _stoppedReason = null;
    onStarted?.call();
    _begin(countIn: true);
    final minutes = _options.timerMinutes;
    _stopAt = minutes > 0 ? _anchor! + Duration(minutes: minutes) : null;
    _timer = Timer.periodic(tickInterval, (_) => _pump());
    _pump();
    notifyListeners();
  }

  /// 今の設定で、少し先から数え始める
  void _begin({required bool countIn}) {
    _anchor = _engine.now + startLead;
    _sequencer = MetronomeSequencer(
      _settings,
      _options,
      seed: _runs++,
      countIn: countIn,
    );
    _pending.clear();
    _recent.clear();
  }

  void stop() => _stop(null);

  void _stop(String? reason) {
    _timer?.cancel();
    _timer = null;
    _anchor = null;
    _stopAt = null;
    _sequencer = null;
    _pending.clear();
    _recent.clear();
    _stoppedReason = reason;
    _engine.cancelScheduledClicks();
    notifyListeners();
  }

  Future<void> toggle() => isRunning ? Future.sync(stop) : start();

  ClickSound get _polySound =>
      _options.sound == ClickSound.wood ? ClickSound.cowbell : ClickSound.wood;

  /// 予約が先読みの範囲に届くまでクリックを足す（画面の更新もここで促す）
  void _pump() {
    final a = _anchor;
    final seq = _sequencer;
    if (a == null || seq == null) return;
    final now = _engine.now;
    final stopAt = _stopAt;
    if (stopAt != null && now >= stopAt) {
      _stop('タイマーの${_options.timerMinutes}分がたったので止めました');
      return;
    }
    final horizon = (now - a + lookahead).inMicroseconds;
    while (true) {
      if (_pending.isEmpty) {
        final bar = seq.nextBar();
        if (bar.isEmpty) break;
        _pending.addAll(bar);
      }
      final c = _pending.first;
      if (c.offsetMicros >= horizon) break;
      _pending.removeAt(0);
      final at = a + Duration(microseconds: c.offsetMicros);
      if (!c.muted) {
        _engine.scheduleClick(
          c.kind,
          at,
          sound: c.poly
              ? _polySound
              : c.countIn
              ? ClickSound.click
              : _options.sound,
          volume: _options.volume * (c.poly ? 0.8 : 1),
        );
      }
      _recent.add((at, c));
      if (_recent.length > 48) _recent.removeAt(0);
    }
    // テンポの段階変化が目標に着き、最後の拍が鳴り終えたら止める
    if (seq.finished && _pending.isEmpty) {
      final last = _recent.isEmpty ? null : _recent.last.$1;
      final beat = Duration(microseconds: (60000000 / currentBpm).round());
      if (last == null || now >= last + beat) {
        _stop('目標のテンポ（${_options.rampTargetBpm}）に着いたので止めました');
        return;
      }
    }
    notifyListeners();
  }

  /// 設定を変える。動いていれば、予約し直して新しいテンポで続ける
  Future<void> update(MetronomeSettings s) async {
    final next = s.normalized();
    if (next == _settings) return;
    _settings = next;
    _restartIfRunning();
    notifyListeners();
    await _meta.put('metronome.settings', next.toMap());
  }

  /// 音色・拍のパターン・消音・テンポの段階変化などを変える
  Future<void> updateOptions(MetronomeOptions o) async {
    final next = o.normalized();
    if (next == _options) return;
    final timerChanged = next.timerMinutes != _options.timerMinutes;
    _options = next;
    _restartIfRunning();
    if (timerChanged && isRunning) {
      _stopAt = next.timerMinutes > 0
          ? _anchor! + Duration(minutes: next.timerMinutes)
          : null;
    }
    notifyListeners();
    await _meta.put('metronome.options', next.toMap());
  }

  void _restartIfRunning() {
    if (!isRunning) return;
    _engine.cancelScheduledClicks();
    _begin(countIn: false);
    _pump();
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
