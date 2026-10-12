import 'package:flutter/foundation.dart';

import '../../../core/meta_store.dart';
import '../domain/pitch.dart';
import 'audio_engine.dart';

/// 基準ピッチ（A4 の周波数）と楽器の調。基準音・チューナーで共通に使う
class PitchSettings {
  const PitchSettings({
    this.a4 = 442,
    this.transposition = Transposition.bFlat,
  });

  static const minA4 = 430.0;
  static const maxA4 = 450.0;

  final double a4;
  final Transposition transposition;

  PitchSettings copyWith({double? a4, Transposition? transposition}) =>
      PitchSettings(
        a4: (a4 ?? this.a4).clamp(minA4, maxA4),
        transposition: transposition ?? this.transposition,
      );

  Map<String, Object?> toMap() => {
    'a4': a4,
    'transposition': transposition.name,
  };

  factory PitchSettings.fromMap(Map<Object?, Object?> m) => PitchSettings(
    a4: m['a4'] is num ? (m['a4']! as num).toDouble().clamp(minA4, maxA4) : 442,
    transposition: Transposition.values.firstWhere(
      (t) => t.name == m['transposition'],
      orElse: () => Transposition.bFlat,
    ),
  );
}

/// 基準ピッチの設定と、基準音（正弦波）を鳴らす
class ReferenceToneController extends ChangeNotifier {
  ReferenceToneController(this._engine, this._meta, PitchSettings initial)
    : _pitch = initial;

  static Future<ReferenceToneController> load(
    AudioEngine engine,
    MetaStore meta,
  ) async {
    final raw = await meta.get('pitch.settings');
    return ReferenceToneController(
      engine,
      meta,
      raw is Map ? PitchSettings.fromMap(raw) : const PitchSettings(),
    );
  }

  final AudioEngine _engine;
  final MetaStore _meta;
  PitchSettings _pitch;

  /// 鳴らす音（実音の MIDI 番号）。初期値は A4
  int _concertMidi = 69;
  bool _playing = false;
  String? _error;

  PitchSettings get pitch => _pitch;
  int get concertMidi => _concertMidi;

  /// 選んでいる楽器の調での記譜音
  int get writtenMidi => _pitch.transposition.concertToWritten(_concertMidi);
  double get frequency => midiToFrequency(_concertMidi, a4: _pitch.a4);
  bool get isPlaying => _playing;
  String? get error => _error;

  Future<void> updatePitch(PitchSettings p) async {
    _pitch = p;
    if (_playing) await _engine.startTone(frequency);
    notifyListeners();
    await _meta.put('pitch.settings', p.toMap());
  }

  /// 鳴らす音を実音で選ぶ（B♭3〜C6 の範囲に収める）
  Future<void> selectConcert(int midi) async {
    _concertMidi = midi.clamp(46, 84);
    if (_playing) await _engine.startTone(frequency);
    notifyListeners();
  }

  /// 鳴らす音を、選んでいる楽器の記譜音で選ぶ
  Future<void> selectWritten(int writtenMidi) =>
      selectConcert(_pitch.transposition.writtenToConcert(writtenMidi));

  Future<void> toggle() async {
    if (_playing) {
      _engine.stopTone();
      _playing = false;
    } else {
      try {
        await _engine.startTone(frequency);
        _playing = true;
        _error = null;
      } on AudioEngineException catch (e) {
        _error = e.message;
      }
    }
    notifyListeners();
  }

  void stop() {
    if (!_playing) return;
    _engine.stopTone();
    _playing = false;
    notifyListeners();
  }

  @override
  void dispose() {
    if (_playing) _engine.stopTone();
    super.dispose();
  }
}
