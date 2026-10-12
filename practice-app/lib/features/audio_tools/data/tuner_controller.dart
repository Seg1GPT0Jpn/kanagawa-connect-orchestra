import 'dart:async';

import 'package:flutter/foundation.dart';

import '../domain/pitch.dart';
import '../domain/pitch_detector.dart';
import '../domain/spectrum.dart';
import 'mic_input.dart';
import 'reference_tone_controller.dart';

/// チューナー：マイクの音から音の高さを測り、いちばん近い音とずれ（セント）を出す
class TunerController extends ChangeNotifier {
  TunerController(this._mic, this._pitch);

  final MicInput _mic;

  /// 基準ピッチ（A4）と楽器の調は、基準音と共通
  final ReferenceToneController _pitch;

  /// マイクは 44.1kHz で取り、半分に間引いて 22.05kHz で測る（トランペットの音域には十分）
  static const micSampleRate = 44100;
  static const analysisRate = 22050.0;
  static const frameSize = 2048;
  static const hopSize = 1024;

  final _detector = const PitchDetector(sampleRate: analysisRate);
  final _smoother = MedianSmoother(5);
  final _buffer = <double>[];
  StreamSubscription<Float64List>? _sub;
  bool _listening = false;
  String? _error;
  PitchReading? _reading;
  double _level = 0;
  int _silentFrames = 0;
  Spectrum? _spectrum;
  Float64List? _peakHold;
  HarmonicProfile? _harmonics;
  bool _spectrumFrozen = false;

  bool get isListening => _listening;
  String? get error => _error;

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

  /// 音の大きさ（0〜1、表示用）
  double get level => _level;

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

  PitchSettings get pitch => _pitch.pitch;

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
    } catch (e) {
      _fail('マイクを使えませんでした（$e）');
    }
    notifyListeners();
  }

  Future<void> stop() async {
    await _sub?.cancel();
    _sub = null;
    if (_listening) await _mic.stop();
    _listening = false;
    _reading = null;
    _harmonics = null;
    _level = 0;
    _buffer.clear();
    _smoother.clear();
    notifyListeners();
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
      }
      _level = _level * 0.7;
      return;
    }
    _silentFrames = 0;
    _level = (e.rms * 4).clamp(0, 1);
    final hz = _smoother.add(e.frequency);
    _reading = PitchReading.fromFrequency(hz, a4: _pitch.pitch.a4);
    if (spectrum != null) {
      _harmonics = HarmonicProfile.of(spectrum, e.frequency);
    }
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
    // 1区間 ≒ 46ms
    const fall = 20 * hopSize / analysisRate;
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
