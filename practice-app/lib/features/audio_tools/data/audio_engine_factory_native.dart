import 'dart:async';

import 'package:audio_session/audio_session.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter_soloud/flutter_soloud.dart';

import '../domain/metronome.dart';
import '../domain/sound.dart';
import 'audio_engine.dart';

AudioEngine createAudioEngine() => SoLoudAudioEngine();

/// SoLoud（flutter_soloud）で鳴らす（Android・iOS・パソコン）
class SoLoudAudioEngine with ChannelVolumes implements AudioEngine {
  final _soloud = SoLoud.instance;
  final Map<(ClickSound, ClickKind), AudioSource> _clicks = {};
  final List<SoundHandle> _scheduled = [];
  final Map<int, _Voice> _voices = {};
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
    throw const AudioEngineException(audioTroubleMessage);
  });

  Future<void> _start() async {
    await _configureSession();
    if (!_soloud.isInitialized) await _soloud.init(bufferSize: 1024);
    for (final sound in ClickSound.values) {
      for (final kind in ClickKind.values) {
        _clicks[(sound, kind)] = await _soloud.loadMem(
          '${sound.name}_${kind.name}.wav',
          clickSoundWav(sound, kind),
        );
      }
    }
  }

  /// iPhone は、アプリが音声の使い方を決めて有効にしないと音が出ない
  /// （SoLoud は設定を任せる作り）。消音スイッチでも鳴るよう再生用にし、
  /// チューナー・録音と同時に使えるよう録音も許す。スピーカーから鳴らす
  Future<void> _configureSession() async {
    if (kIsWeb || defaultTargetPlatform != TargetPlatform.iOS) return;
    try {
      final session = await AudioSession.instance;
      await session.configure(
        AudioSessionConfiguration(
          avAudioSessionCategory: AVAudioSessionCategory.playAndRecord,
          avAudioSessionCategoryOptions:
              AVAudioSessionCategoryOptions.defaultToSpeaker |
              AVAudioSessionCategoryOptions.allowBluetoothA2dp |
              AVAudioSessionCategoryOptions.mixWithOthers,
          avAudioSessionMode: AVAudioSessionMode.measurement,
        ),
      );
      await session.setActive(true);
    } catch (e) {
      // 設定できなくても、鳴らすこと自体は試す
      debugPrint('audio session: $e');
    }
  }

  @override
  void scheduleClick(
    ClickKind kind,
    Duration at, {
    ClickSound sound = ClickSound.beep,
    double volume = 1,
  }) {
    final source = _clicks[(sound, kind)];
    if (source == null) return;
    _scheduled.add(
      _soloud.playScheduled(
        source,
        at,
        volume: volume * volumeOf(AudioChannel.click),
      ),
    );
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
  Future<void> startTone(
    double hz, {
    double volume = 0.5,
    Timbre timbre = Timbre.sine,
    int voice = 0,
  }) async {
    await ensureStarted();
    final current = _voices[voice];
    if (current != null && current.timbre != timbre) {
      current.stop(_soloud);
      _voices.remove(voice);
    }
    final v = _voices[voice] ??= await _Voice.create(_soloud, timbre);
    v.update(_soloud, hz, volume, volumeOf(AudioChannel.tone));
  }

  @override
  void stopTone({int? voice}) {
    final targets = voice == null ? _voices.keys.toList() : [voice];
    for (final k in targets) {
      _voices.remove(k)?.stop(_soloud);
    }
  }

  AudioSource? _clip;
  SoundHandle? _clipHandle;
  Timer? _clipTimer;

  @override
  Future<void> playWav(
    Uint8List wav, {
    double speed = 1,
    void Function()? onDone,
  }) async {
    await ensureStarted();
    stopPlayback();
    final clip = _clip = await _soloud.loadMem('recording.wav', wav);
    final h = _clipHandle = _soloud.play(
      clip,
      volume: volumeOf(AudioChannel.playback),
    );
    if (speed != 1) _soloud.setRelativePlaySpeed(h, speed);
    // 16bit モノラルの WAV なので、長さはデータの大きさから分かる
    final sampleRate = ByteData.sublistView(wav).getUint32(24, Endian.little);
    final micros = ((wav.length - 44) / 2 / sampleRate * 1000000 / speed)
        .round();
    _clipTimer = Timer(Duration(microseconds: micros), () {
      _releaseClip();
      onDone?.call();
    });
  }

  @override
  void stopPlayback() {
    final h = _clipHandle;
    if (h != null && _soloud.isInitialized) {
      unawaited(_soloud.stop(h).catchError((Object _) {}));
    }
    _releaseClip();
  }

  void _releaseClip() {
    _clipTimer?.cancel();
    _clipTimer = null;
    _clipHandle = null;
    final c = _clip;
    _clip = null;
    if (c != null && _soloud.isInitialized) {
      unawaited(_soloud.disposeSource(c).catchError((Object _) {}));
    }
  }

  @override
  void setVolume(AudioChannel channel, double volume) {
    storeVolume(channel, volume);
    if (!_soloud.isInitialized) return;
    switch (channel) {
      case AudioChannel.tone:
        for (final v in _voices.values) {
          v.applyVolume(_soloud, volumeOf(channel));
        }
      case AudioChannel.playback:
        final h = _clipHandle;
        if (h != null) _soloud.setVolume(h, volumeOf(channel));
      case AudioChannel.click:
        break; // 次に予約する音から変わる
    }
  }
}

/// 1つの音（倍音ごとに正弦波を重ねて音色を作る）
class _Voice {
  _Voice(this.timbre, this.sources);

  static Future<_Voice> create(SoLoud soloud, Timbre timbre) async {
    final sources = <AudioSource>[];
    for (var i = 0; i < timbre.harmonics.length; i++) {
      if (timbre.harmonics[i] == 0) continue;
      sources.add(await soloud.loadWaveform(WaveForm.sin, false, 1, 0));
    }
    return _Voice(timbre, sources);
  }

  final Timbre timbre;
  final List<AudioSource> sources;
  final List<SoundHandle> handles = [];

  /// 頼まれた音量（系統の音量を掛ける前）
  double base = 0;

  Iterable<(int, double)> get _partials sync* {
    for (var i = 0; i < timbre.harmonics.length; i++) {
      if (timbre.harmonics[i] != 0) yield (i + 1, timbre.harmonics[i]);
    }
  }

  void update(SoLoud soloud, double hz, double volume, double channel) {
    base = volume;
    final partials = _partials.toList();
    final first = handles.isEmpty;
    for (var i = 0; i < partials.length; i++) {
      final (n, amp) = partials[i];
      soloud.setWaveformFreq(sources[i], hz * n);
      final v = volume * channel * amp * timbre.gain;
      if (first) {
        handles.add(soloud.play(sources[i], volume: v, looping: true));
      } else {
        soloud.setVolume(handles[i], v);
      }
    }
  }

  /// 系統の音量が変わったとき
  void applyVolume(SoLoud soloud, double channel) {
    final partials = _partials.toList();
    for (var i = 0; i < handles.length; i++) {
      soloud.setVolume(
        handles[i],
        base * channel * partials[i].$2 * timbre.gain,
      );
    }
  }

  void stop(SoLoud soloud) {
    for (final h in handles) {
      unawaited(soloud.stop(h).catchError((Object _) {}));
    }
    for (final s in sources) {
      unawaited(soloud.disposeSource(s).catchError((Object _) {}));
    }
    handles.clear();
  }
}
