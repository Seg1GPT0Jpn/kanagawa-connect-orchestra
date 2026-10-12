import 'dart:async';
import 'dart:typed_data';

import 'package:flutter/foundation.dart';

import '../../../core/clock.dart';
import '../../../core/ids.dart';
import '../../audio_tools/data/audio_engine.dart';
import '../../audio_tools/data/mic_input.dart';
import '../../audio_tools/data/reference_tone_controller.dart';
import '../../audio_tools/domain/wav.dart';
import '../domain/recording_result.dart';
import '../domain/tone_analysis.dart';
import 'recording_repository.dart';

enum RecordingPhase { idle, recording, done }

/// 録音：録りながら分析し、録り終えたら結果をまとめる。音声はメモリにだけ置き、再生できる
class RecordingController extends ChangeNotifier {
  RecordingController({
    required this._mic,
    required this._audio,
    required this._pitch,
    required this._repository,
    this._clock = systemClock,
  });

  final MicInput _mic;
  final AudioEngine _audio;
  final ReferenceToneController _pitch;
  final RecordingRepository _repository;
  final Clock _clock;

  static const micSampleRate = 44100;
  static const analysisRate = 22050.0;

  /// 録音の上限
  static const maxDuration = Duration(seconds: 30);

  RecordingPhase _phase = RecordingPhase.idle;
  StreamSubscription<Float64List>? _sub;
  ToneFrameAnalyzer? _analyzer;
  final List<int> _pcm = [];
  ToneAnalysis? _result;
  DateTime? _startedAt;
  String? _error;
  bool _playing = false;
  bool _saved = false;
  double _level = 0;

  RecordingPhase get phase => _phase;
  ToneAnalysis? get result => _result;
  String? get error => _error;
  bool get isPlaying => _playing;
  bool get isSaved => _saved;
  double get level => _level;
  RecordingRepository get repository => _repository;

  /// 録った長さ
  Duration get elapsed =>
      Duration(microseconds: (_pcm.length / analysisRate * 1000000).round());

  Future<void> start() async {
    if (_phase == RecordingPhase.recording) return;
    stopPlayback();
    try {
      if (!await _mic.requestPermission()) {
        _error = 'マイクの使用が許可されていません。端末やブラウザの設定で許可してください';
        notifyListeners();
        return;
      }
      _pcm.clear();
      _analyzer = ToneFrameAnalyzer(sampleRate: analysisRate);
      _result = null;
      _saved = false;
      _error = null;
      _startedAt = _clock();
      final stream = await _mic.start(sampleRate: micSampleRate);
      _sub = stream.listen(addSamples, onError: (Object e) => stop());
      _phase = RecordingPhase.recording;
    } catch (e) {
      _error = 'マイクを使えませんでした（$e）';
      _phase = RecordingPhase.idle;
    }
    notifyListeners();
  }

  /// 44.1kHz の波形を受け取り、半分に間引いて保存・分析する（テストからも呼ぶ）
  @visibleForTesting
  void addSamples(Float64List samples) {
    if (_phase != RecordingPhase.recording) return;
    final half = Float64List(samples.length ~/ 2);
    var peak = 0.0;
    for (var i = 0; i < half.length; i++) {
      final v = (samples[2 * i] + samples[2 * i + 1]) / 2;
      half[i] = v;
      _pcm.add((v * 32767).round().clamp(-32768, 32767));
      if (v.abs() > peak) peak = v.abs();
    }
    _analyzer!.add(half);
    _level = peak.clamp(0, 1);
    if (elapsed >= maxDuration) {
      unawaited(stop());
    } else {
      notifyListeners();
    }
  }

  Future<void> stop() async {
    if (_phase != RecordingPhase.recording) return;
    _phase = RecordingPhase.done;
    await _sub?.cancel();
    _sub = null;
    await _mic.stop();
    _result = _analyzer?.summarize(a4: _pitch.pitch.a4);
    if (_result == null) _error = '音がほとんど入っていませんでした。楽器を近づけて、もう一度録ってください';
    _level = 0;
    notifyListeners();
  }

  /// 録った音の WAV（22.05kHz・16bit・モノラル）
  Uint8List get wav =>
      pcm16Wav(Int16List.fromList(_pcm), sampleRate: analysisRate.round());

  Future<void> play() async {
    if (_pcm.isEmpty) return;
    try {
      _playing = true;
      notifyListeners();
      await _audio.playWav(
        wav,
        onDone: () {
          _playing = false;
          notifyListeners();
        },
      );
    } on AudioEngineException catch (e) {
      _playing = false;
      _error = e.message;
      notifyListeners();
    }
  }

  void stopPlayback() {
    if (!_playing) return;
    _audio.stopPlayback();
    _playing = false;
    notifyListeners();
  }

  /// 分析結果を保存する（音声は保存しない）
  Future<void> save({String memo = ''}) async {
    final r = _result;
    if (r == null || _saved) return;
    await _repository.save(
      RecordingResult.fromAnalysis(
        generateId(),
        r,
        recordedAt: _startedAt ?? _clock(),
        a4: _pitch.pitch.a4,
        memo: memo,
      ),
    );
    _saved = true;
    notifyListeners();
  }

  /// 録り直す前の状態に戻す
  void reset() {
    stopPlayback();
    _phase = RecordingPhase.idle;
    _result = null;
    _pcm.clear();
    _error = null;
    _saved = false;
    notifyListeners();
  }

  @override
  void dispose() {
    unawaited(_sub?.cancel());
    if (_phase == RecordingPhase.recording) unawaited(_mic.stop());
    if (_playing) _audio.stopPlayback();
    super.dispose();
  }
}
