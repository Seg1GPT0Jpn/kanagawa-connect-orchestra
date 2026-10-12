import 'dart:async';
import 'dart:js_interop';
import 'dart:js_interop_unsafe';

import 'package:flutter/foundation.dart';
import 'package:web/web.dart' as web;

import '../domain/metronome.dart';
import '../domain/sound.dart';
import 'audio_engine.dart';

AudioEngine createAudioEngine() => WebAudioEngine();

/// ブラウザの Web Audio で直接鳴らす（Web 版）
///
/// ブラウザは、ユーザーがタップした処理の中で音を始めないと無音のままにする
/// （特に iPhone の Safari）。そのため [ensureStarted] は最初の await より前に
/// 音の準備（AudioContext の作成と再開）を同期的に済ませる。さらに念のため、
/// 画面のどこかをタップするたびに、止まっている音を再開する。
class WebAudioEngine with ChannelVolumes implements AudioEngine {
  WebAudioEngine() {
    // 画面のタップ・キー操作で、止められていた音を再開する
    for (final type in const ['pointerup', 'touchend', 'click', 'keydown']) {
      web.document.addEventListener(type, _onGesture.toJS);
    }
  }

  web.AudioContext? _ctx;
  final Map<AudioChannel, web.GainNode> _channels = {};
  final Map<(ClickSound, ClickKind), web.AudioBuffer> _clicks = {};
  final List<web.AudioBufferSourceNode> _scheduled = [];
  final Map<int, _WebVoice> _voices = {};

  void _onGesture(web.Event _) {
    final ctx = _ctx;
    if (ctx != null && ctx.state != 'running' && ctx.state != 'closed') {
      _resume(ctx);
    }
  }

  @override
  bool get isStarted => _ctx?.state == 'running';

  @override
  Duration get now {
    final ctx = _ctx;
    if (ctx == null) return Duration.zero;
    return Duration(microseconds: (ctx.currentTime * 1000000).round());
  }

  @override
  Future<void> ensureStarted() async {
    // ここから最初の await までは、タップの処理の中で同期的に動く
    final ctx = _ctx ??= _create();
    if (ctx.state != 'running') _resume(ctx);
    if (ctx.state == 'running') return;
    // 再開を少し待つ（Safari は実際に鳴り始めるまで時間がかかる）
    for (var i = 0; i < 20 && ctx.state != 'running'; i++) {
      await Future<void>.delayed(const Duration(milliseconds: 50));
    }
    if (ctx.state != 'running') {
      throw const AudioEngineException(audioTroubleMessage);
    }
  }

  web.AudioContext _create() {
    _allowInSilentMode();
    final ctx = web.AudioContext();
    for (final c in AudioChannel.values) {
      final g = ctx.createGain()..gain.value = volumeOf(c);
      g.connect(ctx.destination);
      _channels[c] = g;
    }
    return ctx;
  }

  /// iPhone の消音スイッチが入っていても鳴らす（Safari 17 以降）
  static void _allowInSilentMode() {
    try {
      final session = web.window.navigator.getProperty<JSObject?>(
        'audioSession'.toJS,
      );
      session?.setProperty('type'.toJS, 'playback'.toJS);
    } catch (_) {}
  }

  void _resume(web.AudioContext ctx) {
    try {
      ctx.resume().toDart.catchError((Object _) => null);
      // 無音を一瞬鳴らす（古い Safari は、タップ中に何か鳴らすと許可される）
      final silent = ctx.createBufferSource()
        ..buffer = ctx.createBuffer(1, 1, 22050);
      silent.connect(ctx.destination);
      silent.start();
    } catch (e) {
      debugPrint('audio resume: $e');
    }
  }

  web.AudioBuffer _bufferOf(web.AudioContext ctx, Uint8List wav) {
    final pcm = decodePcm16Wav(wav);
    final buffer = ctx.createBuffer(
      1,
      pcm.samples.isEmpty ? 1 : pcm.samples.length,
      pcm.sampleRate,
    );
    if (pcm.samples.isNotEmpty) buffer.copyToChannel(pcm.samples.toJS, 0);
    return buffer;
  }

  @override
  void scheduleClick(
    ClickKind kind,
    Duration at, {
    ClickSound sound = ClickSound.beep,
    double volume = 1,
  }) {
    final ctx = _ctx;
    if (ctx == null) return;
    final buffer = _clicks[(sound, kind)] ??= _bufferOf(
      ctx,
      clickSoundWav(sound, kind),
    );
    final gain = ctx.createGain()..gain.value = volume;
    gain.connect(_channels[AudioChannel.click]!);
    final src = ctx.createBufferSource()..buffer = buffer;
    src.connect(gain);
    src.start(at.inMicroseconds / 1000000);
    _scheduled.add(src);
    if (_scheduled.length > 64) {
      _scheduled.removeRange(0, _scheduled.length - 64);
    }
  }

  @override
  void cancelScheduledClicks() {
    for (final s in _scheduled) {
      try {
        s.stop();
      } catch (_) {}
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
    final ctx = _ctx!;
    final current = _voices[voice];
    if (current != null && current.timbre != timbre) {
      current.stop(ctx);
      _voices.remove(voice);
    }
    final v = _voices[voice] ??= _WebVoice(
      ctx,
      timbre,
      _channels[AudioChannel.tone]!,
    );
    v.update(ctx, hz, volume);
  }

  @override
  void stopTone({int? voice}) {
    final ctx = _ctx;
    if (ctx == null) return;
    final targets = voice == null ? _voices.keys.toList() : [voice];
    for (final k in targets) {
      _voices.remove(k)?.stop(ctx);
    }
  }

  web.AudioBufferSourceNode? _clip;

  @override
  Future<void> playWav(
    Uint8List wav, {
    double speed = 1,
    void Function()? onDone,
  }) async {
    await ensureStarted();
    stopPlayback();
    final ctx = _ctx!;
    final src = _clip = ctx.createBufferSource()..buffer = _bufferOf(ctx, wav);
    src.playbackRate.value = speed;
    src.connect(_channels[AudioChannel.playback]!);
    src.onended = ((web.Event _) {
      if (identical(_clip, src)) {
        _clip = null;
        onDone?.call();
      }
    }).toJS;
    src.start();
  }

  @override
  void stopPlayback() {
    final src = _clip;
    _clip = null;
    if (src == null) return;
    try {
      src.stop();
    } catch (_) {}
  }

  @override
  void setVolume(AudioChannel channel, double volume) {
    storeVolume(channel, volume);
    _channels[channel]?.gain.value = volumeOf(channel);
  }
}

/// 1つの音（倍音の組み合わせを PeriodicWave にして、発振器1つで鳴らす）
class _WebVoice {
  _WebVoice(web.AudioContext ctx, this.timbre, web.AudioNode out)
    : osc = ctx.createOscillator(),
      gain = ctx.createGain() {
    final n = timbre.harmonics.length + 1;
    final real = List<double>.filled(n, 0);
    final imag = List<double>.filled(n, 0);
    for (var i = 0; i < timbre.harmonics.length; i++) {
      imag[i + 1] = timbre.harmonics[i] * timbre.gain;
    }
    JSArray<JSNumber> js(List<double> v) => [for (final x in v) x.toJS].toJS;
    osc.setPeriodicWave(
      ctx.createPeriodicWave(
        js(real),
        js(imag),
        web.PeriodicWaveConstraints(disableNormalization: true),
      ),
    );
    gain.gain.value = 0;
    osc.connect(gain);
    gain.connect(out);
    osc.start();
  }

  final Timbre timbre;
  final web.OscillatorNode osc;
  final web.GainNode gain;

  void update(web.AudioContext ctx, double hz, double volume) {
    final t = ctx.currentTime;
    osc.frequency.setValueAtTime(hz, t);
    // 10ms かけて音量を変える（プツッという音を防ぐ）
    gain.gain.setTargetAtTime(volume, t, 0.01);
  }

  void stop(web.AudioContext ctx) {
    final t = ctx.currentTime;
    gain.gain.setTargetAtTime(0, t, 0.01);
    try {
      osc.stop(t + 0.08);
    } catch (_) {}
  }
}
