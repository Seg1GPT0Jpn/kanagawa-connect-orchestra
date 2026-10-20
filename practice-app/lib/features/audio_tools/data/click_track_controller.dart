import 'dart:async';

import 'package:flutter/foundation.dart';

import '../../../core/meta_store.dart';
import '../domain/click_track.dart';
import 'audio_engine.dart';

/// クリックトラックの保存・編集・再生（メトロノームと同じく、少し先までを音の時計に予約し続ける）
class ClickTrackController extends ChangeNotifier {
  ClickTrackController(this._engine, this._meta, List<ClickTrack> tracks)
    : _tracks = tracks.isEmpty ? [const ClickTrack()] : tracks;

  static Future<ClickTrackController> load(
    AudioEngine engine,
    MetaStore meta,
  ) async {
    final raw = await meta.get('clicktracks');
    final tracks = [
      if (raw is List)
        for (final t in raw)
          if (t is Map) ClickTrack.fromMap(t),
    ];
    return ClickTrackController(engine, meta, tracks);
  }

  /// 鳴らし始めたとき（ほかのクリックを止めるため）
  VoidCallback? onStarted;

  final AudioEngine _engine;
  final MetaStore _meta;
  List<ClickTrack> _tracks;
  int _selected = 0;

  static const lookahead = Duration(milliseconds: 200);
  static const tickInterval = Duration(milliseconds: 25);
  static const startLead = Duration(milliseconds: 150);

  Timer? _timer;
  Duration? _anchor;
  List<TrackClick> _clicks = const [];
  int _total = 0;
  int _next = 0;
  String? _error;

  List<ClickTrack> get tracks => List.unmodifiable(_tracks);
  int get selectedIndex => _selected;
  ClickTrack get track => _tracks[_selected];
  bool get isPlaying => _timer != null;
  String? get error => _error;

  /// 再生中の位置（小節・拍・区間）。止まっていれば null
  TrackClick? get position {
    final a = _anchor;
    if (!isPlaying || a == null || _clicks.isEmpty) return null;
    final t = (_engine.now - a).inMicroseconds;
    if (t < 0) return null;
    TrackClick? last;
    for (final c in _clicks) {
      if (c.offsetMicros > t) break;
      last = c;
    }
    return last;
  }

  Future<void> _persist() =>
      _meta.put('clicktracks', [for (final t in _tracks) t.toMap()]);

  Future<void> select(int index) async {
    if (index < 0 || index >= _tracks.length) return;
    stop();
    _selected = index;
    notifyListeners();
  }

  Future<void> updateTrack(ClickTrack t) async {
    if (isPlaying) stop();
    _tracks = [..._tracks]..[_selected] = t;
    notifyListeners();
    await _persist();
  }

  Future<void> addTrack() async {
    stop();
    _tracks = [..._tracks, ClickTrack(name: 'クリックトラック ${_tracks.length + 1}')];
    _selected = _tracks.length - 1;
    notifyListeners();
    await _persist();
  }

  /// 出来上がったトラックを足して選ぶ（プリセットの連続再生など）
  Future<void> addPrepared(ClickTrack t) async {
    stop();
    _tracks = [..._tracks, t];
    _selected = _tracks.length - 1;
    notifyListeners();
    await _persist();
  }

  Future<void> deleteTrack() async {
    stop();
    final next = [..._tracks]..removeAt(_selected);
    _tracks = next.isEmpty ? [const ClickTrack()] : next;
    _selected = _selected.clamp(0, _tracks.length - 1);
    notifyListeners();
    await _persist();
  }

  Future<void> play() async {
    if (isPlaying) return;
    try {
      await _engine.ensureStarted();
    } on AudioEngineException catch (e) {
      _error = e.message;
      notifyListeners();
      return;
    }
    _error = null;
    onStarted?.call();
    final built = buildClickTrack(track);
    _clicks = built.clicks;
    _total = built.totalMicros;
    _next = 0;
    _anchor = _engine.now + startLead;
    _timer = Timer.periodic(tickInterval, (_) => _pump());
    _pump();
    notifyListeners();
  }

  void stop() {
    if (_timer == null) return;
    _timer?.cancel();
    _timer = null;
    _anchor = null;
    _engine.cancelScheduledClicks();
    notifyListeners();
  }

  void _pump() {
    final a = _anchor;
    if (a == null) return;
    final elapsed = (_engine.now - a).inMicroseconds;
    // 最後のクリックのあと、曲の長さまで来たら止める
    if (elapsed >= _total) {
      stop();
      return;
    }
    final horizon = elapsed + lookahead.inMicroseconds;
    while (_next < _clicks.length && _clicks[_next].offsetMicros < horizon) {
      final c = _clicks[_next++];
      _engine.scheduleClick(c.kind, a + Duration(microseconds: c.offsetMicros));
    }
    notifyListeners();
  }

  @override
  void dispose() {
    stop();
    super.dispose();
  }
}
