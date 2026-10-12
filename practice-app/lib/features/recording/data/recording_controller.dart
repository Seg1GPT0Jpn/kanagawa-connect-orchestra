import 'dart:async';
import 'dart:typed_data';

import 'package:flutter/foundation.dart';

import '../../../core/clock.dart';
import '../../../core/ids.dart';
import '../../audio_tools/data/audio_engine.dart';
import '../../audio_tools/data/mic_input.dart';
import '../../audio_tools/data/reference_tone_controller.dart';
import '../../audio_tools/domain/wav.dart';
import '../../data_io/data_io_service.dart';
import '../domain/audio_file.dart';
import '../domain/recording_result.dart';
import '../domain/tone_analysis.dart';
import 'recording_repository.dart';

enum RecordingPhase { idle, recording, analyzing, done }

/// 録音の長さの選択肢
const recordingLimits = [
  Duration(seconds: 30),
  Duration(minutes: 1),
  Duration(minutes: 3),
  Duration(minutes: 5),
];

/// 録音：録りながら分析し、録り終えたら結果をまとめる。音声はメモリにだけ置き、再生・書き出しできる
class RecordingController extends ChangeNotifier {
  RecordingController({
    required this._mic,
    required this._audio,
    required this._pitch,
    required this._repository,
    this._files,
    this._clock = systemClock,
  });

  final MicInput _mic;
  final AudioEngine _audio;
  final ReferenceToneController _pitch;
  final RecordingRepository _repository;
  final FileGateway? _files;
  final Clock _clock;

  static const micSampleRate = 44100;
  static const analysisRate = 22050.0;

  /// 録音の上限（既定）
  static const maxDuration = Duration(seconds: 30);

  /// 一度に分析する長さ（この間に画面を更新させる）
  static const _chunk = 22050;

  RecordingPhase _phase = RecordingPhase.idle;
  StreamSubscription<Float64List>? _sub;
  ToneFrameAnalyzer? _analyzer;
  final List<Int16List> _chunks = [];
  int _length = 0;
  Int16List? _joined;
  ToneAnalysis? _result;
  DateTime? _startedAt;
  String? _error;
  bool _playing = false;
  bool _saved = false;
  double _level = 0;
  Duration _limit = maxDuration;
  double _speed = 1;
  double _progress = 0;

  /// 分析する範囲（秒）。null なら全体
  (double, double)? _range;

  /// 読み込んだファイルの名前（録音なら null）
  String? _source;

  RecordingPhase get phase => _phase;
  ToneAnalysis? get result => _result;
  String? get error => _error;
  bool get isPlaying => _playing;
  bool get isSaved => _saved;
  double get level => _level;
  RecordingRepository get repository => _repository;

  /// 録音の上限
  Duration get limit => _limit;
  void setLimit(Duration d) {
    if (_phase == RecordingPhase.recording) return;
    _limit = d;
    notifyListeners();
  }

  /// 再生の速さ（音の高さも変わる）
  double get speed => _speed;
  void setSpeed(double s) {
    _speed = s;
    notifyListeners();
  }

  /// 分析し直している進み具合（0〜1）
  double get progress => _progress;

  /// 分析した範囲（秒）。null なら全体
  (double, double)? get range => _range;

  /// 読み込んだファイル（録音なら null）
  String? get source => _source;

  /// 録った長さ
  Duration get elapsed =>
      Duration(microseconds: (_length / analysisRate * 1000000).round());

  double get seconds => _length / analysisRate;

  /// 録った音（22.05kHz・16bit）
  Int16List get pcm {
    final j = _joined;
    if (j != null && j.length == _length) return j;
    final out = Int16List(_length);
    var at = 0;
    for (final c in _chunks) {
      out.setAll(at, c);
      at += c.length;
    }
    _chunks
      ..clear()
      ..add(out);
    return _joined = out;
  }

  Future<void> start() async {
    if (_phase == RecordingPhase.recording) return;
    stopPlayback();
    try {
      if (!await _mic.requestPermission()) {
        _error = 'マイクの使用が許可されていません。端末やブラウザの設定で許可してください';
        notifyListeners();
        return;
      }
      _clear();
      _analyzer = ToneFrameAnalyzer(sampleRate: analysisRate);
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

  void _clear() {
    _chunks.clear();
    _joined = null;
    _length = 0;
    _result = null;
    _saved = false;
    _error = null;
    _range = null;
    _source = null;
  }

  /// 44.1kHz の波形を受け取り、半分に間引いて保存・分析する（テストからも呼ぶ）
  @visibleForTesting
  void addSamples(Float64List samples) {
    if (_phase != RecordingPhase.recording) return;
    final half = Float64List(samples.length ~/ 2);
    final chunk = Int16List(half.length);
    var peak = 0.0;
    for (var i = 0; i < half.length; i++) {
      final v = (samples[2 * i] + samples[2 * i + 1]) / 2;
      half[i] = v;
      chunk[i] = (v * 32767).round().clamp(-32768, 32767);
      if (v.abs() > peak) peak = v.abs();
    }
    _chunks.add(chunk);
    _length += chunk.length;
    _analyzer!.add(half);
    _level = peak.clamp(0, 1);
    if (elapsed >= _limit) {
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

  /// [range]（秒）だけを分析し直す（トリミング）。null なら全体
  Future<void> analyzeRange((double, double)? range) async {
    if (_length == 0 || _phase == RecordingPhase.recording) return;
    final all = pcm;
    final from = range == null
        ? 0
        : (range.$1 * analysisRate).round().clamp(0, _length);
    final to = range == null
        ? _length
        : (range.$2 * analysisRate).round().clamp(from, _length);
    _range = range;
    _phase = RecordingPhase.analyzing;
    _progress = 0;
    notifyListeners();
    final analyzer = ToneFrameAnalyzer(sampleRate: analysisRate);
    for (var i = from; i < to; i += _chunk) {
      final end = (i + _chunk).clamp(i, to);
      analyzer.add(
        Float64List.fromList([for (var k = i; k < end; k++) all[k] / 32768]),
      );
      _progress = (end - from) / (to - from);
      notifyListeners();
      // 画面が固まらないよう、少しずつ
      await Future<void>.delayed(Duration.zero);
    }
    _result = analyzer.summarize(a4: _pitch.pitch.a4);
    _error = _result == null ? 'この範囲には、高さを測れる音がほとんどありません' : null;
    _saved = false;
    _phase = RecordingPhase.done;
    notifyListeners();
  }

  /// WAV ファイルを選んで読み込み、分析する。やめたら false
  Future<bool> importFile() async {
    final files = _files;
    if (files == null || _phase == RecordingPhase.recording) return false;
    final bytes = await files.pickAudio();
    if (bytes == null) return false;
    return importWav(bytes, name: 'ファイル');
  }

  /// WAV の中身を読み込んで分析する（テストからも呼ぶ）
  Future<bool> importWav(Uint8List bytes, {String name = 'ファイル'}) async {
    stopPlayback();
    final ({Float64List samples, int sampleRate}) wav;
    try {
      wav = readWav(bytes);
    } on WavFormatException catch (e) {
      _error = e.message;
      notifyListeners();
      return false;
    }
    final mono = resample(wav.samples, wav.sampleRate, analysisRate.round());
    final maxSamples = (recordingLimits.last.inSeconds * 2 * analysisRate)
        .round();
    final n = mono.length.clamp(0, maxSamples);
    _clear();
    _source = name;
    _startedAt = _clock();
    final data = Int16List(n);
    for (var i = 0; i < n; i++) {
      data[i] = (mono[i] * 32767).round().clamp(-32768, 32767);
    }
    _chunks.add(data);
    _length = n;
    await analyzeRange(null);
    if (mono.length > maxSamples) {
      _error = '長いファイルなので、最初の${recordingLimits.last.inMinutes * 2}分だけ読み込みました';
      notifyListeners();
    }
    return true;
  }

  /// 選んだ範囲（なければ全体）の WAV（22.05kHz・16bit・モノラル）
  Uint8List get wav {
    final all = pcm;
    final r = _range;
    final from = r == null
        ? 0
        : (r.$1 * analysisRate).round().clamp(0, _length);
    final to = r == null
        ? _length
        : (r.$2 * analysisRate).round().clamp(from, _length);
    return pcm16Wav(
      Int16List.sublistView(all, from, to),
      sampleRate: analysisRate.round(),
    );
  }

  /// WAV ファイルとして書き出す（端末・パソコンに保存）。やめたら false
  Future<bool> exportWav() async {
    final files = _files;
    if (files == null || _length == 0) return false;
    final t = _startedAt ?? _clock();
    String two(int v) => v.toString().padLeft(2, '0');
    final name =
        'recording-${t.year}-${two(t.month)}-${two(t.day)}-${two(t.hour)}${two(t.minute)}.wav';
    return files.save(name, wav, mimeType: 'audio/wav');
  }

  Future<void> play() async {
    if (_length == 0) return;
    try {
      _playing = true;
      notifyListeners();
      await _audio.playWav(
        wav,
        speed: _speed,
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
    _clear();
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
