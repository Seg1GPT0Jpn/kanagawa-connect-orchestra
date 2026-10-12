import 'dart:async';

import 'package:flutter/foundation.dart';
import 'package:flutter_soloud/flutter_soloud.dart';

import '../domain/metronome.dart';
import '../domain/wav.dart';

/// 音を鳴らす窓口（テストでは偽物に差し替える）
abstract interface class AudioEngine {
  /// 音を出せる状態にする（Web では、ボタンを押した中で呼ぶ必要がある）
  Future<void> ensureStarted();

  bool get isStarted;

  /// 音の時計（予約に使う）。始まっていなければ 0
  Duration get now;

  /// [kind] のクリック音を、音の時計の [at] に鳴らすよう予約する
  void scheduleClick(ClickKind kind, Duration at);

  /// まだ鳴っていない予約をすべて取り消す
  void cancelScheduledClicks();

  /// [hz] の正弦波を鳴らし続ける（鳴っていれば高さだけ変える）
  Future<void> startTone(double hz, {double volume = 0.5});
  void stopTone();
}

class AudioEngineException implements Exception {
  const AudioEngineException(this.message);

  final String message;

  @override
  String toString() => message;
}

/// SoLoud（flutter_soloud）で鳴らす
class SoLoudAudioEngine implements AudioEngine {
  final _soloud = SoLoud.instance;
  final Map<ClickKind, AudioSource> _clicks = {};
  final List<SoundHandle> _scheduled = [];
  AudioSource? _sine;
  SoundHandle? _toneHandle;
  Future<void>? _starting;

  @override
  bool get isStarted => _soloud.isInitialized && _clicks.isNotEmpty;

  @override
  Duration get now =>
      _soloud.isInitialized ? _soloud.getEngineTime() : Duration.zero;

  @override
  Future<void> ensureStarted() => _starting ??= _start().catchError((Object e) {
    _starting = null;
    debugPrint('audio init failed: $e');
    throw const AudioEngineException('音を出せませんでした。端末の音量や、ほかのアプリの使用状況を確かめてください');
  });

  Future<void> _start() async {
    if (!_soloud.isInitialized) await _soloud.init(bufferSize: 1024);
    // 強拍は高く大きく、細分は低く小さく
    _clicks[ClickKind.accent] = await _soloud.loadMem(
      'accent.wav',
      clickWav(frequency: 1760),
    );
    _clicks[ClickKind.beat] = await _soloud.loadMem(
      'beat.wav',
      clickWav(frequency: 1320, volume: 0.75),
    );
    _clicks[ClickKind.subdivision] = await _soloud.loadMem(
      'sub.wav',
      clickWav(
        frequency: 990,
        volume: 0.45,
        duration: const Duration(milliseconds: 25),
      ),
    );
    _sine = await _soloud.loadWaveform(WaveForm.sin, false, 1, 0);
  }

  @override
  void scheduleClick(ClickKind kind, Duration at) {
    final source = _clicks[kind];
    if (source == null) return;
    _scheduled.add(_soloud.playScheduled(source, at));
    // 終わった予約の記録は古いものから捨てる（取り消しは数秒先までで足りる）
    if (_scheduled.length > 64) {
      _scheduled.removeRange(0, _scheduled.length - 64);
    }
  }

  @override
  void cancelScheduledClicks() {
    for (final h in _scheduled) {
      unawaited(_soloud.stop(h).catchError((Object _) {}));
    }
    _scheduled.clear();
  }

  @override
  Future<void> startTone(double hz, {double volume = 0.5}) async {
    await ensureStarted();
    final sine = _sine!;
    _soloud.setWaveformFreq(sine, hz);
    if (_toneHandle == null || !_soloud.getIsValidVoiceHandle(_toneHandle!)) {
      _toneHandle = _soloud.play(sine, volume: volume, looping: true);
    } else {
      _soloud.setVolume(_toneHandle!, volume);
    }
  }

  @override
  void stopTone() {
    final h = _toneHandle;
    _toneHandle = null;
    if (h != null && _soloud.isInitialized) {
      unawaited(_soloud.stop(h).catchError((Object _) {}));
    }
  }
}
