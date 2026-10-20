import 'dart:async';

import 'package:flutter/foundation.dart';

import '../../../core/clock.dart';
import '../../../core/ids.dart';
import '../../../core/meta_store.dart';
import '../domain/note_tracker.dart';
import '../domain/pitch.dart';
import '../domain/pitch_detector.dart';
import '../domain/pitch_stats.dart';
import '../domain/spectrum.dart';
import '../domain/tuner_settings.dart';
import 'mic_input.dart';
import 'reference_tone_controller.dart';
import 'tuner_session_repository.dart';

/// チューナー：マイクの音から音の高さを測り、いちばん近い音とずれ（セント）を出す。
/// 吹いた音の音程を音名ごとに集め、止めたときに記録として保存する
class TunerController extends ChangeNotifier {
  TunerController(
    this._mic,
    this._pitch, {
    this._meta,
    this._sessions,
    this._clock = systemClock,
    TunerSettings settings = const TunerSettings(),
  }) : _settings = settings,
       _smoother = MedianSmoother(settings.damping.frames) {
    _stats = _newStats();
  }

  static Future<TunerController> load(
    MicInput mic,
    ReferenceToneController pitch, {
    required MetaStore meta,
    TunerSessionRepository? sessions,
    Clock clock = systemClock,
  }) async {
    final raw = await meta.get('tuner.settings');
    return TunerController(
      mic,
      pitch,
      meta: meta,
      sessions: sessions,
      clock: clock,
      settings: raw is Map ? TunerSettings.fromMap(raw) : const TunerSettings(),
    );
  }

  final MicInput _mic;

  /// 基準ピッチ（A4）と楽器の調は、基準音と共通
  final ReferenceToneController _pitch;
  final MetaStore? _meta;
  final TunerSessionRepository? _sessions;
  final Clock _clock;
  TunerSettings _settings;

  /// マイクは 44.1kHz で取り、半分に間引いて 22.05kHz で測る（トランペットの音域には十分）
  static const micSampleRate = 44100;
  static const analysisRate = 22050.0;
  static const frameSize = 2048;
  static const hopSize = 1024;

  /// 1フレームの長さ（秒）
  static const frameSeconds = hopSize / analysisRate;

  /// これより短い練習は記録に残さない（秒）
  static const minSessionSeconds = 5.0;

  final _detector = const PitchDetector(sampleRate: analysisRate);
  MedianSmoother _smoother;
  final _buffer = <double>[];
  final _notes = NoteTracker();
  late PitchStats _stats;
  DateTime? _startedAt;
  StreamSubscription<Float64List>? _sub;
  bool _listening = false;
  String? _error;
  PitchReading? _reading;
  double _level = 0;
  int _silentFrames = 0;
  int _inTuneStreak = 0;
  Spectrum? _spectrum;
  Float64List? _peakHold;
  HarmonicProfile? _harmonics;
  bool _spectrumFrozen = false;
  TunerSession? _lastSaved;

  bool get isListening => _listening;
  String? get error => _error;
  TunerSettings get settings => _settings;

  /// いま測れている音（無音・はっきりしないときは null）。cents は平均律からのずれ
  PitchReading? get reading => _reading;

  /// 選んだ音律での目標からのずれ（セント）。平均律なら reading.cents と同じ
  double? get targetCents {
    final r = _reading;
    return r == null ? null : r.cents - _pitch.pitch.offsetFor(r.midi);
  }

  /// いまの音の、選んだ音律での平均律からのずれ（目標をどれだけずらすか）
  double? get targetOffset {
    final r = _reading;
    return r == null ? null : _pitch.pitch.offsetFor(r.midi);
  }

  /// 判定範囲に入っているか
  bool get inTune {
    final c = targetCents;
    return c != null && c.abs() <= _settings.tolerance;
  }

  /// 範囲に入ったまま続いているフレーム数（ターゲット表示を大きくするのに使う）
  int get inTuneStreak => _inTuneStreak;

  /// 音の大きさ（0〜1、表示用）
  double get level => _level;
  PitchSettings get pitch => _pitch.pitch;

  /// いまの音と、直前の音（音程の差・出だしの音程）
  NoteEvent? get currentNote => _notes.current;
  NoteEvent? get previousNote => _notes.previous;
  int? get intervalSemitones => _notes.intervalSemitones;

  /// この練習（はじめる〜止める）の音程の統計
  PitchStats get stats => _stats;

  /// 止めたときに保存した記録（画面で「記録しました」を出す）
  TunerSession? get lastSaved => _lastSaved;

  /// いまのスペクトラム（周波数ごとの強さ）
  Spectrum? get spectrum => _spectrum;

  /// これまでのいちばん大きな値（ゆっくり下がる。dB）
  Float64List? get peakHold => _peakHold;

  /// いまの音の倍音のバランス（音色メーター）。音が測れないときは null
  HarmonicProfile? get harmonics => _harmonics;

  /// スペクトラムの表示を止めて、じっくり見る
  bool get spectrumFrozen => _spectrumFrozen;
  void setSpectrumFrozen(bool v) {
    _spectrumFrozen = v;
    notifyListeners();
  }

  void resetPeakHold() {
    _peakHold = null;
    notifyListeners();
  }

  PitchStats _newStats() =>
      PitchStats(frameSeconds: frameSeconds, tolerance: _settings.tolerance);

  Future<void> updateSettings(TunerSettings s) async {
    if (s == _settings) return;
    final dampingChanged = s.damping != _settings.damping;
    final toleranceChanged = s.tolerance != _settings.tolerance;
    _settings = s;
    if (dampingChanged) _smoother = MedianSmoother(s.damping.frames);
    // 判定範囲が変わったら、そこから数え直す
    if (toleranceChanged) _resetStats();
    notifyListeners();
    await _meta?.put('tuner.settings', s.toMap());
  }

  /// 合っていた割合を数え直す（それまでの分は記録しない）
  void resetTracker() {
    _resetStats();
    notifyListeners();
  }

  void _resetStats() {
    _stats = _newStats();
    _startedAt = _listening ? _clock() : null;
    _notes.reset();
  }

  Future<void> start() async {
    if (_listening) return;
    try {
      if (!await _mic.requestPermission()) {
        _error = 'マイクの使用が許可されていません。端末やブラウザの設定で許可してください';
        notifyListeners();
        return;
      }
      final stream = await _mic.start(sampleRate: micSampleRate);
      _sub = stream.listen(
        addSamples,
        onError: (Object e) => _fail('マイクの音を受け取れませんでした'),
      );
      _listening = true;
      _error = null;
      _lastSaved = null;
      _stats = _newStats();
      _startedAt = _clock();
      _notes.reset();
    } catch (e) {
      _fail('マイクを使えませんでした（$e）');
    }
    notifyListeners();
  }

  Future<void> stop() async {
    await _sub?.cancel();
    _sub = null;
    final wasListening = _listening;
    if (_listening) await _mic.stop();
    _listening = false;
    _reading = null;
    _harmonics = null;
    _level = 0;
    _inTuneStreak = 0;
    _buffer.clear();
    _smoother.clear();
    _notes.silence();
    if (wasListening) await _saveSession();
    notifyListeners();
  }

  Future<void> _saveSession() async {
    final started = _startedAt;
    final repo = _sessions;
    if (started == null || _stats.seconds < minSessionSeconds) return;
    final p = _pitch.pitch;
    final session = TunerSession(
      id: generateId(),
      startedAtMillis: started.millisecondsSinceEpoch,
      durationSeconds: _clock().difference(started).inMilliseconds / 1000,
      a4: p.a4,
      temperamentLabel: p.temperamentLabel,
      stats: _stats,
    );
    _lastSaved = session;
    await repo?.save(session);
  }

  void _fail(String message) {
    _error = message;
    _listening = false;
    notifyListeners();
  }

  /// 44.1kHz の波形を受け取り、間引いてためて、たまったら測る（テストからも呼ぶ）
  @visibleForTesting
  void addSamples(Float64List samples) {
    for (var i = 0; i + 1 < samples.length; i += 2) {
      _buffer.add((samples[i] + samples[i + 1]) / 2);
    }
    var changed = false;
    while (_buffer.length >= frameSize) {
      _analyze(Float64List.fromList(_buffer.sublist(0, frameSize)));
      _buffer.removeRange(0, hopSize);
      changed = true;
    }
    if (changed) notifyListeners();
  }

  void _analyze(Float64List frame) {
    final spectrum = _spectrumFrozen
        ? null
        : Spectrum.of(frame, sampleRate: analysisRate);
    if (spectrum != null) {
      _spectrum = spectrum;
      _updatePeakHold(spectrum);
    }
    final e = _detector.detect(frame);
    if (e == null) {
      // 短い途切れでは表示を消さない（音の切れ目でちらつかないように）
      if (++_silentFrames > 4) {
        _reading = null;
        _harmonics = null;
        _smoother.clear();
        _notes.silence();
        _inTuneStreak = 0;
      }
      _level = _level * 0.7;
      return;
    }
    _silentFrames = 0;
    _level = (e.rms * 4).clamp(0, 1);
    final hz = _smoother.add(e.frequency);
    final a4 = _pitch.pitch.a4;
    _reading = PitchReading.fromFrequency(hz, a4: a4);
    if (spectrum != null) {
      _harmonics = HarmonicProfile.of(spectrum, e.frequency);
    }

    // 記録と、音の区切り（出だしの音程はならす前の値で見る）
    final raw = PitchReading.fromFrequency(e.frequency, a4: a4);
    final rawTarget = raw.cents - _pitch.pitch.offsetFor(raw.midi);
    _notes.addFrame(raw.midi, rawTarget);
    final target = targetCents!;
    _stats.add(_reading!.midi, target);
    _inTuneStreak = target.abs() <= _settings.tolerance ? _inTuneStreak + 1 : 0;
  }

  /// 山の高さを覚えておき、1秒に約 20 dB ずつ下げる
  void _updatePeakHold(Spectrum s) {
    final hold = _peakHold;
    if (hold == null || hold.length != s.amplitude.length) {
      _peakHold = Float64List.fromList([
        for (var i = 0; i < s.amplitude.length; i++) s.dbAt(i),
      ]);
      return;
    }
    const fall = 20 * frameSeconds;
    for (var i = 0; i < hold.length; i++) {
      final db = s.dbAt(i);
      hold[i] = db > hold[i] - fall ? db : hold[i] - fall;
    }
  }

  @override
  void dispose() {
    unawaited(_sub?.cancel());
    if (_listening) unawaited(_mic.stop());
    super.dispose();
  }
}
