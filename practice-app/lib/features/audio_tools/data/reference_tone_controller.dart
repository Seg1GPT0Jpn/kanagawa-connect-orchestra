import 'dart:math' as math;

import 'package:flutter/foundation.dart';

import '../../../core/meta_store.dart';
import '../domain/pitch.dart';
import '../domain/temperament.dart';
import '../domain/sound.dart';
import 'audio_engine.dart';

/// 基準ピッチ（A4 の周波数）・楽器の調・音律・音名の表記。基準音・チューナーで共通に使う
class PitchSettings {
  const PitchSettings({
    this.a4 = 442,
    this.transposition = Transposition.bFlat,
    this.temperament = Temperament.equal,
    this.tonicPitchClass = 10,
    this.custom,
    this.naming = NoteNaming.english,
    this.instrument = '',
  });

  static const minA4 = 430.0;
  static const maxA4 = 450.0;

  final double a4;
  final Transposition transposition;

  /// 音律（チューナーの目標・基準音の高さ）
  final Temperament temperament;

  /// 主音（実音。0=C〜11=B）。初期値は B♭（吹奏楽・トランペットでよく使う調）
  final int tonicPitchClass;

  /// 自分で作った音律（[temperament] が custom のとき使う）
  final CustomTemperament? custom;

  /// 音名の表記
  final NoteNaming naming;

  /// 選んだ楽器の名前（表示用。空なら楽器の調だけ）
  final String instrument;

  PitchSettings copyWith({
    double? a4,
    Transposition? transposition,
    Temperament? temperament,
    int? tonicPitchClass,
    CustomTemperament? custom,
    NoteNaming? naming,
    String? instrument,
  }) => PitchSettings(
    a4: (a4 ?? this.a4).clamp(minA4, maxA4),
    transposition: transposition ?? this.transposition,
    temperament: temperament ?? this.temperament,
    tonicPitchClass: (tonicPitchClass ?? this.tonicPitchClass) % 12,
    custom: custom ?? this.custom,
    naming: naming ?? this.naming,
    instrument: instrument ?? this.instrument,
  );

  /// 自分で作った音律を使っている
  bool get usesCustom => temperament == Temperament.custom && custom != null;

  /// 音律の名前（平均律以外は主音つき）
  String get temperamentLabel {
    if (temperament == Temperament.equal) return temperament.label;
    final name = usesCustom ? custom!.name : temperament.label;
    return '$name・主音 ${pitchClassName(tonicPitchClass)}';
  }

  /// [midi]（実音）の、選んだ音律での平均律からのずれ（セント）
  double offsetFor(int midi) => usesCustom
      ? custom!.offsets[(midi - tonicPitchClass) % 12]
      : temperament.offsetFor(midi, tonicPitchClass);

  /// [midi]（実音）の、選んだ音律での周波数
  double frequencyOf(int midi) =>
      midiToFrequency(midi, a4: a4) * math.pow(2, offsetFor(midi) / 1200);

  Map<String, Object?> toMap() => {
    'a4': a4,
    'transposition': transposition.name,
    'temperament': temperament.name,
    'tonic': tonicPitchClass,
    if (custom != null) 'custom': custom!.toMap(),
    'naming': naming.name,
    'instrument': instrument,
  };

  factory PitchSettings.fromMap(Map<Object?, Object?> m) {
    final custom = CustomTemperament.fromMap(m['custom']);
    var temperament = Temperament.values.firstWhere(
      (t) => t.name == m['temperament'],
      orElse: () => Temperament.equal,
    );
    if (temperament == Temperament.custom && custom == null) {
      temperament = Temperament.equal;
    }
    final instrument = m['instrument'];
    return PitchSettings(
      a4: m['a4'] is num
          ? (m['a4']! as num).toDouble().clamp(minA4, maxA4)
          : 442,
      transposition: Transposition.values.firstWhere(
        (t) => t.name == m['transposition'],
        orElse: () => Transposition.bFlat,
      ),
      temperament: temperament,
      tonicPitchClass: m['tonic'] is int ? (m['tonic']! as int) % 12 : 10,
      custom: custom,
      naming: NoteNaming.byName(m['naming']),
      instrument: instrument is String ? instrument : '',
    );
  }
}

/// 和音の種類（主音からの半音の数）
enum ChordType {
  major('長三和音', [0, 4, 7]),
  minor('短三和音', [0, 3, 7]),
  fifth('完全5度', [0, 7]),
  octave('オクターブ', [0, 12]),
  dominant7('属七の和音', [0, 4, 7, 10]);

  const ChordType(this.label, this.intervals);
  final String label;
  final List<int> intervals;
}

/// 基準ピッチの設定と、基準音を鳴らす（1つの音・和音・ドローン）
class ReferenceToneController extends ChangeNotifier {
  ReferenceToneController(
    this._engine,
    this._meta,
    PitchSettings initial, {
    this._timbre = Timbre.sine,
    this._volume = 0.5,
  }) : _pitch = initial {
    currentNaming = initial.naming;
  }

  static Future<ReferenceToneController> load(
    AudioEngine engine,
    MetaStore meta,
  ) async {
    final raw = await meta.get('pitch.settings');
    final tone = await meta.get('tone.settings');
    final v = tone is Map ? tone['volume'] : null;
    return ReferenceToneController(
      engine,
      meta,
      raw is Map ? PitchSettings.fromMap(raw) : const PitchSettings(),
      timbre: Timbre.byName(tone is Map ? tone['timbre'] : null),
      volume: v is num ? v.toDouble().clamp(0.05, 1.0) : 0.5,
    );
  }

  /// 鳴らせる範囲（実音）：B♭1〜C7（ドローン・低音の楽器も使えるように）
  static const minMidi = 34;
  static const maxMidi = 96;

  final AudioEngine _engine;
  final MetaStore _meta;
  PitchSettings _pitch;
  Timbre _timbre;
  double _volume;

  /// 鳴らす音（実音の MIDI 番号）。初期値は A4
  int _concertMidi = 69;
  bool _playing = false;

  /// 和音・ドローンとして鳴らしている音（実音）
  final Set<int> _held = {};
  String? _error;

  PitchSettings get pitch => _pitch;
  int get concertMidi => _concertMidi;
  Timbre get timbre => _timbre;
  double get volume => _volume;

  /// 選んでいる楽器の調での記譜音
  int get writtenMidi => _pitch.transposition.concertToWritten(_concertMidi);

  /// 選んだ音律での高さ
  double get frequency => _pitch.frequencyOf(_concertMidi);

  /// 1つの音か、和音のどちらかが鳴っている
  bool get isPlaying => _playing || _held.isNotEmpty;

  /// 1つの音（「鳴らす」ボタン）が鳴っている
  bool get isSinglePlaying => _playing;

  /// 和音・ドローンとして鳴らしている音
  Set<int> get held => Set.unmodifiable(_held);
  String? get error => _error;

  static int _voiceOf(int midi) => 1 + midi;

  Future<void> _sound(int voice, int midi) => _engine.startTone(
    _pitch.frequencyOf(midi),
    volume: _volume,
    timbre: _timbre,
    voice: voice,
  );

  /// 鳴っている音を、いまの設定（基準ピッチ・音律・音色・音量）で鳴らし直す
  Future<void> _retune() async {
    if (_playing) await _sound(0, _concertMidi);
    for (final m in _held) {
      await _sound(_voiceOf(m), m);
    }
  }

  Future<void> updatePitch(PitchSettings p) async {
    _pitch = p;
    currentNaming = p.naming;
    await _retune();
    notifyListeners();
    await _meta.put('pitch.settings', p.toMap());
  }

  Future<void> setTimbre(Timbre t) async {
    _timbre = t;
    await _retune();
    notifyListeners();
    await _saveTone();
  }

  Future<void> setVolume(double v) async {
    _volume = v.clamp(0.05, 1.0);
    await _retune();
    notifyListeners();
    await _saveTone();
  }

  Future<void> _saveTone() =>
      _meta.put('tone.settings', {'timbre': _timbre.name, 'volume': _volume});

  /// 鳴らす音を実音で選ぶ
  Future<void> selectConcert(int midi) async {
    _concertMidi = midi.clamp(minMidi, maxMidi);
    if (_playing) await _sound(0, _concertMidi);
    notifyListeners();
  }

  /// 鳴らす音を、選んでいる楽器の記譜音で選ぶ
  Future<void> selectWritten(int writtenMidi) =>
      selectConcert(_pitch.transposition.writtenToConcert(writtenMidi));

  /// [midi]（実音）を選んで鳴らす（鳴っていれば高さだけ変える）。
  /// ボタンの処理から直接呼ぶ（Web では、待たずに音を始める必要があるため）
  Future<void> playConcert(int midi) {
    _concertMidi = midi.clamp(minMidi, maxMidi);
    notifyListeners();
    return _playing ? _sound(0, _concertMidi) : toggle();
  }

  Future<void> toggle() async {
    if (_playing) {
      _engine.stopTone(voice: 0);
      _playing = false;
    } else {
      try {
        await _sound(0, _concertMidi);
        _playing = true;
        _error = null;
      } on AudioEngineException catch (e) {
        _error = e.message;
      }
    }
    notifyListeners();
  }

  /// 和音の音を1つ足す・外す（実音）
  Future<void> toggleHeld(int midi) async {
    final m = midi.clamp(minMidi, maxMidi);
    if (_held.remove(m)) {
      _engine.stopTone(voice: _voiceOf(m));
      notifyListeners();
      return;
    }
    try {
      await _sound(_voiceOf(m), m);
      _held.add(m);
      _error = null;
    } on AudioEngineException catch (e) {
      _error = e.message;
    }
    notifyListeners();
  }

  /// [root]（実音）を根音にした和音を鳴らす（それまでの和音は止める）。
  /// 音律が純正律なら、和音もうなりのない高さになる
  Future<void> playChord(int root, ChordType type) async {
    _stopHeld();
    try {
      for (final i in type.intervals) {
        final m = (root + i).clamp(minMidi, maxMidi);
        await _sound(_voiceOf(m), m);
        _held.add(m);
      }
      _error = null;
    } on AudioEngineException catch (e) {
      _error = e.message;
    }
    notifyListeners();
  }

  /// ドローン：主音（調の音）と5度を低めの音域で鳴らし続ける
  Future<void> playDrone() {
    final pc = _pitch.tonicPitchClass;
    // B♭2〜A3 の中で主音を選ぶ
    final root = 46 + (pc - 46 % 12 + 12) % 12;
    return playChord(root, ChordType.fifth);
  }

  void _stopHeld() {
    for (final m in _held) {
      _engine.stopTone(voice: _voiceOf(m));
    }
    _held.clear();
  }

  /// 和音・ドローンを止める
  void stopHeld() {
    _stopHeld();
    notifyListeners();
  }

  /// すべて止める
  void stop() {
    if (!isPlaying) return;
    _engine.stopTone();
    _playing = false;
    _held.clear();
    notifyListeners();
  }

  @override
  void dispose() {
    if (isPlaying) _engine.stopTone();
    super.dispose();
  }
}
