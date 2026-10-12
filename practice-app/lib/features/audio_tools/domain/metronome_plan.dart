/// メトロノームの拡張（拍ごとの強弱・消音・テンポの段階変化・カウントイン・ポリリズム）。決定論的
///
/// クリックは小節ごとに順に作る。1つの区間（同じテンポが続く間）の中では、時刻を
/// 「区間の始まり＋番号×間隔」で毎回計算するので、誤差がたまらない。
library;

import 'dart:math' as math;

import 'metronome.dart';
import 'sound.dart';

/// 拍ごとの鳴らし方
enum BeatAccent {
  accent('強'),
  normal('ふつう'),
  mute('休み');

  const BeatAccent(this.label);
  final String label;

  BeatAccent get next => values[(index + 1) % values.length];
}

/// 拍の見せ方
enum MetronomeVisual {
  dots('拍の丸'),
  pendulum('振り子'),
  flash('画面の点滅');

  const MetronomeVisual(this.label);
  final String label;
}

class MetronomeOptions {
  const MetronomeOptions({
    this.sound = ClickSound.beep,
    this.volume = 1,
    this.pattern = const [],
    this.randomMutePercent = 0,
    this.playBars = 2,
    this.muteBars = 0,
    this.rampEnabled = false,
    this.rampTargetBpm = 120,
    this.rampStepBpm = 4,
    this.rampEveryBars = 4,
    this.rampStopAtTarget = true,
    this.countInBars = 0,
    this.polyrhythm = 0,
    this.visual = MetronomeVisual.dots,
    this.timerMinutes = 0,
  });

  final ClickSound sound;

  /// メトロノームの音量（0〜1）
  final double volume;

  /// 拍ごとの鳴らし方（拍の数と合わなければ、ふだんの鳴らし方）
  final List<BeatAccent> pattern;

  /// ランダムに休む拍の割合（0〜80%）。内側で拍を感じる練習
  final int randomMutePercent;

  /// [playBars] 小節鳴らして [muteBars] 小節休む（0 なら休まない）
  final int playBars;
  final int muteBars;

  /// テンポを段階的に変える：[rampEveryBars] 小節ごとに [rampStepBpm] ずつ、[rampTargetBpm] まで
  final bool rampEnabled;
  final int rampTargetBpm;
  final int rampStepBpm;
  final int rampEveryBars;

  /// 目標のテンポで [rampEveryBars] 小節鳴らしたら止める
  final bool rampStopAtTarget;

  /// 始める前の数え（小節）
  final int countInBars;

  /// ポリリズム：1小節を、拍とは別にこの数で等分して別の音で鳴らす（0 なら使わない）
  final int polyrhythm;
  final MetronomeVisual visual;

  /// この分数で自動で止める（0 なら止めない）
  final int timerMinutes;

  MetronomeOptions normalized() => MetronomeOptions(
    sound: sound,
    volume: volume.clamp(0.0, 1.0),
    pattern: pattern.length > 12 ? pattern.sublist(0, 12) : pattern,
    randomMutePercent: randomMutePercent.clamp(0, 80),
    playBars: playBars.clamp(1, 16),
    muteBars: muteBars.clamp(0, 16),
    rampEnabled: rampEnabled,
    rampTargetBpm: rampTargetBpm.clamp(
      MetronomeSettings.minBpm,
      MetronomeSettings.maxBpm,
    ),
    rampStepBpm: rampStepBpm.clamp(1, 40),
    rampEveryBars: rampEveryBars.clamp(1, 32),
    rampStopAtTarget: rampStopAtTarget,
    countInBars: countInBars.clamp(0, 2),
    polyrhythm: polyrhythm == 1 ? 0 : polyrhythm.clamp(0, 9),
    visual: visual,
    timerMinutes: timerMinutes.clamp(0, 180),
  );

  MetronomeOptions copyWith({
    ClickSound? sound,
    double? volume,
    List<BeatAccent>? pattern,
    int? randomMutePercent,
    int? playBars,
    int? muteBars,
    bool? rampEnabled,
    int? rampTargetBpm,
    int? rampStepBpm,
    int? rampEveryBars,
    bool? rampStopAtTarget,
    int? countInBars,
    int? polyrhythm,
    MetronomeVisual? visual,
    int? timerMinutes,
  }) => MetronomeOptions(
    sound: sound ?? this.sound,
    volume: volume ?? this.volume,
    pattern: pattern ?? this.pattern,
    randomMutePercent: randomMutePercent ?? this.randomMutePercent,
    playBars: playBars ?? this.playBars,
    muteBars: muteBars ?? this.muteBars,
    rampEnabled: rampEnabled ?? this.rampEnabled,
    rampTargetBpm: rampTargetBpm ?? this.rampTargetBpm,
    rampStepBpm: rampStepBpm ?? this.rampStepBpm,
    rampEveryBars: rampEveryBars ?? this.rampEveryBars,
    rampStopAtTarget: rampStopAtTarget ?? this.rampStopAtTarget,
    countInBars: countInBars ?? this.countInBars,
    polyrhythm: polyrhythm ?? this.polyrhythm,
    visual: visual ?? this.visual,
    timerMinutes: timerMinutes ?? this.timerMinutes,
  ).normalized();

  /// [beatsPerBar] 拍の小節の、拍ごとの鳴らし方
  List<BeatAccent> patternFor(int beatsPerBar, {required bool accentFirst}) =>
      pattern.length == beatsPerBar
      ? pattern
      : [
          for (var i = 0; i < beatsPerBar; i++)
            i == 0 && accentFirst && beatsPerBar > 1
                ? BeatAccent.accent
                : BeatAccent.normal,
        ];

  Map<String, Object?> toMap() => {
    'sound': sound.name,
    'volume': volume,
    'pattern': [for (final p in pattern) p.name],
    'randomMute': randomMutePercent,
    'playBars': playBars,
    'muteBars': muteBars,
    'ramp': rampEnabled,
    'rampTarget': rampTargetBpm,
    'rampStep': rampStepBpm,
    'rampEvery': rampEveryBars,
    'rampStop': rampStopAtTarget,
    'countIn': countInBars,
    'poly': polyrhythm,
    'visual': visual.name,
    'timer': timerMinutes,
  };

  /// 壊れた値は既定値で読む
  factory MetronomeOptions.fromMap(Map<Object?, Object?> m) {
    int i(String k, int d) => m[k] is int ? m[k]! as int : d;
    bool b(String k, bool d) => m[k] is bool ? m[k]! as bool : d;
    final pattern = m['pattern'];
    return MetronomeOptions(
      sound: ClickSound.byName(m['sound']),
      volume: m['volume'] is num ? (m['volume']! as num).toDouble() : 1,
      pattern: [
        if (pattern is List)
          for (final p in pattern)
            BeatAccent.values.firstWhere(
              (a) => a.name == p,
              orElse: () => BeatAccent.normal,
            ),
      ],
      randomMutePercent: i('randomMute', 0),
      playBars: i('playBars', 2),
      muteBars: i('muteBars', 0),
      rampEnabled: b('ramp', false),
      rampTargetBpm: i('rampTarget', 120),
      rampStepBpm: i('rampStep', 4),
      rampEveryBars: i('rampEvery', 4),
      rampStopAtTarget: b('rampStop', true),
      countInBars: i('countIn', 0),
      polyrhythm: i('poly', 0),
      visual: MetronomeVisual.values.firstWhere(
        (v) => v.name == m['visual'],
        orElse: () => MetronomeVisual.dots,
      ),
      timerMinutes: i('timer', 0),
    ).normalized();
  }

  @override
  bool operator ==(Object other) =>
      other is MetronomeOptions &&
      other.toMap().toString() == toMap().toString();

  @override
  int get hashCode => toMap().toString().hashCode;
}

/// 予約するクリック1つ
class PlannedClick {
  const PlannedClick({
    required this.offsetMicros,
    required this.kind,
    required this.bar,
    required this.beatInBar,
    required this.bpm,
    this.muted = false,
    this.countIn = false,
    this.poly = false,
  });

  /// 開始からの時刻（マイクロ秒）
  final int offsetMicros;
  final ClickKind kind;

  /// 何小節目か（0から。カウントインは負）
  final int bar;
  final int beatInBar;

  /// この小節のテンポ
  final int bpm;

  /// 鳴らさない（拍の表示だけ進める）
  final bool muted;
  final bool countIn;

  /// ポリリズムの音
  final bool poly;
}

/// クリックを小節ごとに順に作る
class MetronomeSequencer {
  MetronomeSequencer(
    this.settings,
    this.options, {
    this.seed = 0,
    bool countIn = true,
  }) : _bar = countIn ? -options.countInBars : 0;

  final MetronomeSettings settings;
  final MetronomeOptions options;

  /// ランダムに休む拍を決める種（同じ種なら同じ休み方）
  final int seed;

  int _bar;
  bool _finished = false;

  /// 同じテンポが続く区間の始まり（その小節番号と時刻）。区間の中は掛け算で時刻を出す
  int? _segmentBar;
  int _segmentBpm = 0;
  double _segmentStart = 0;
  double _nextBarStart = 0;

  /// テンポの段階変化が目標に着いて終わった
  bool get finished => _finished;

  /// [bar] 小節目のテンポ
  int bpmForBar(int bar) {
    if (!options.rampEnabled || bar < 0) return settings.bpm;
    final steps = bar ~/ options.rampEveryBars;
    final start = settings.bpm, target = options.rampTargetBpm;
    final v = start + (target >= start ? 1 : -1) * steps * options.rampStepBpm;
    return target >= start ? math.min(v, target) : math.max(v, target);
  }

  /// 目標のテンポで決めた小節数を鳴らし終えた小節（それより後は作らない）
  int? get _lastBar {
    if (!options.rampEnabled || !options.rampStopAtTarget) return null;
    final diff = (options.rampTargetBpm - settings.bpm).abs();
    final steps = (diff / options.rampStepBpm).ceil();
    return (steps + 1) * options.rampEveryBars - 1;
  }

  /// 次の1小節分のクリック。終わっていれば空
  List<PlannedClick> nextBar() {
    final last = _lastBar;
    if (_finished || (last != null && _bar > last)) {
      _finished = true;
      return const [];
    }
    final bar = _bar++;
    final countIn = bar < 0;
    final bpm = bpmForBar(bar);
    final beats = settings.beatsPerBar;
    final sub = countIn ? 1 : settings.subdivision;
    final beatMicros = 60000000 / bpm;
    if (_segmentBar == null || bpm != _segmentBpm) {
      _segmentBar = bar;
      _segmentBpm = bpm;
      _segmentStart = _nextBarStart;
    }
    final start = _segmentStart + (bar - _segmentBar!) * beats * beatMicros;
    final pattern = options.patternFor(
      beats,
      accentFirst: settings.accentFirstBeat,
    );
    final barMuted =
        !countIn &&
        options.muteBars > 0 &&
        bar % (options.playBars + options.muteBars) >= options.playBars;
    final out = <PlannedClick>[];
    for (var i = 0; i < beats * sub; i++) {
      final beat = i ~/ sub;
      final isBeat = i % sub == 0;
      final accent = pattern[beat];
      final kind = countIn
          ? (beat == 0 ? ClickKind.accent : ClickKind.beat)
          : !isBeat
          ? ClickKind.subdivision
          : accent == BeatAccent.accent
          ? ClickKind.accent
          : ClickKind.beat;
      final muted =
          !countIn &&
          (barMuted || accent == BeatAccent.mute || _randomMuted(bar, beat));
      out.add(
        PlannedClick(
          offsetMicros: (start + i * beatMicros / sub).round(),
          kind: kind,
          bar: bar,
          beatInBar: beat,
          bpm: bpm,
          muted: muted,
          countIn: countIn,
        ),
      );
    }
    final poly = options.polyrhythm;
    if (!countIn && poly > 1 && poly != beats) {
      final barMicros = beats * beatMicros;
      for (var j = 0; j < poly; j++) {
        out.add(
          PlannedClick(
            offsetMicros: (start + j * barMicros / poly).round(),
            kind: j == 0 ? ClickKind.beat : ClickKind.subdivision,
            bar: bar,
            beatInBar: -1,
            bpm: bpm,
            muted: barMuted,
            poly: true,
          ),
        );
      }
      out.sort((a, b) => a.offsetMicros.compareTo(b.offsetMicros));
    }
    _nextBarStart = start + beats * beatMicros;
    return out;
  }

  /// 拍ごとに決まった疑似乱数で休むかを決める（同じ種・小節・拍なら同じ）
  bool _randomMuted(int bar, int beat) {
    final p = options.randomMutePercent;
    if (p <= 0) return false;
    var h = seed * 73856093 ^ bar * 19349663 ^ beat * 83492791;
    h = (h ^ (h >> 13)) * 1274126177;
    h = h ^ (h >> 16);
    return (h & 0x7fffffff) % 100 < p;
  }
}
