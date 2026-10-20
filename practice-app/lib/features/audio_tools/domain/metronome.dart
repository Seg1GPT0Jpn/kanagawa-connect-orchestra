/// メトロノームの拍の計算（決定論的。音を鳴らす部分とは分ける）
///
/// 拍の時刻は「開始からの経過時間」で決める。画面の更新やタイマーが遅れても、
/// 次の拍の時刻はずれない（音を鳴らす側が、先の拍を正確な時刻に予約する）。
library;

enum ClickKind {
  /// 小節の1拍目（強拍）
  accent,

  /// ほかの拍
  beat,

  /// 拍の細分（8分・3連・16分）
  subdivision,
}

class MetronomeSettings {
  const MetronomeSettings({
    this.bpm = 80,
    this.beatsPerBar = 4,
    this.subdivision = 1,
    this.accentFirstBeat = true,
  });

  static const minBpm = 20;
  static const maxBpm = 300;

  /// 1分間の拍数
  final int bpm;

  /// 1小節の拍数（1〜12。1なら強拍なし）
  final int beatsPerBar;

  /// 1拍の分割（1＝なし、2＝8分、3＝3連、4＝16分）
  final int subdivision;
  final bool accentFirstBeat;

  /// ずれた値は範囲に収める
  MetronomeSettings normalized() => MetronomeSettings(
    bpm: bpm.clamp(minBpm, maxBpm),
    beatsPerBar: beatsPerBar.clamp(1, 12),
    subdivision: subdivision.clamp(1, 4),
    accentFirstBeat: accentFirstBeat,
  );

  MetronomeSettings copyWith({
    int? bpm,
    int? beatsPerBar,
    int? subdivision,
    bool? accentFirstBeat,
  }) => MetronomeSettings(
    bpm: bpm ?? this.bpm,
    beatsPerBar: beatsPerBar ?? this.beatsPerBar,
    subdivision: subdivision ?? this.subdivision,
    accentFirstBeat: accentFirstBeat ?? this.accentFirstBeat,
  ).normalized();

  /// クリック（細分を含む）の間隔（マイクロ秒、目安。時刻の計算には [clickOffsetMicros] を使う）
  int get clickIntervalMicros => (60000000 / (bpm * subdivision)).round();

  /// [index] 番目のクリックの、開始からの時刻（マイクロ秒）。毎回計算するので誤差がたまらない
  int clickOffsetMicros(int index) =>
      (index * 60000000 / (bpm * subdivision)).round();

  /// 開始から [micros] までに鳴り終えたクリックの番号（0から。まだなら -1）
  int clickIndexAt(int micros) =>
      micros < 0 ? -1 : (micros * bpm * subdivision / 60000000).floor();

  Map<String, Object?> toMap() => {
    'bpm': bpm,
    'beatsPerBar': beatsPerBar,
    'subdivision': subdivision,
    'accentFirstBeat': accentFirstBeat,
  };

  factory MetronomeSettings.fromMap(Map<Object?, Object?> m) =>
      MetronomeSettings(
        bpm: m['bpm'] is int ? m['bpm']! as int : 80,
        beatsPerBar: m['beatsPerBar'] is int ? m['beatsPerBar']! as int : 4,
        subdivision: m['subdivision'] is int ? m['subdivision']! as int : 1,
        accentFirstBeat: m['accentFirstBeat'] is bool
            ? m['accentFirstBeat']! as bool
            : true,
      ).normalized();

  @override
  bool operator ==(Object other) =>
      other is MetronomeSettings &&
      other.bpm == bpm &&
      other.beatsPerBar == beatsPerBar &&
      other.subdivision == subdivision &&
      other.accentFirstBeat == accentFirstBeat;

  @override
  int get hashCode =>
      Object.hash(bpm, beatsPerBar, subdivision, accentFirstBeat);
}

class Click {
  const Click({
    required this.index,
    required this.offset,
    required this.kind,
    required this.beatInBar,
  });

  /// 開始から数えたクリックの番号（0から）
  final int index;

  /// 開始からの時刻
  final Duration offset;
  final ClickKind kind;

  /// 小節の何拍目か（0から）
  final int beatInBar;
}

/// [index] 番目のクリック
Click clickAt(MetronomeSettings s, int index) {
  final isBeat = index % s.subdivision == 0;
  final beatIndex = index ~/ s.subdivision;
  final beatInBar = beatIndex % s.beatsPerBar;
  final kind = !isBeat
      ? ClickKind.subdivision
      : (beatInBar == 0 && s.accentFirstBeat && s.beatsPerBar > 1)
      ? ClickKind.accent
      : ClickKind.beat;
  return Click(
    index: index,
    offset: Duration(microseconds: s.clickOffsetMicros(index)),
    kind: kind,
    beatInBar: beatInBar,
  );
}

/// 開始から [from] 以上 [to] 未満の時刻に鳴るクリック（先読みして予約するのに使う）
List<Click> clicksBetween(MetronomeSettings s, Duration from, Duration to) {
  final result = <Click>[];
  // 丸めの境目で取りこぼさないよう、1つ手前から調べる
  for (var i = s.clickIndexAt(from.inMicroseconds) - 1; ; i++) {
    if (i < 0) continue;
    final t = s.clickOffsetMicros(i);
    if (t >= to.inMicroseconds) break;
    if (t >= from.inMicroseconds) result.add(clickAt(s, i));
  }
  return result;
}

/// タップした時刻（新しいものが後ろ）からテンポを求める。2回未満なら null
///
/// 直近の最大8回の間隔の中央値を使う（1回だけのずれに引っぱられないように）。
/// 2秒以上あいたら、そこから前のタップは数えない。
int? tapTempo(List<Duration> taps) {
  if (taps.length < 2) return null;
  final intervals = <int>[];
  for (var i = taps.length - 1; i > 0 && intervals.length < 8; i--) {
    final d = taps[i].inMicroseconds - taps[i - 1].inMicroseconds;
    if (d <= 0 || d > 2000000) break;
    intervals.add(d);
  }
  if (intervals.isEmpty) return null;
  intervals.sort();
  final mid = intervals.length ~/ 2;
  final median = intervals.length.isOdd
      ? intervals[mid].toDouble()
      : (intervals[mid - 1] + intervals[mid]) / 2;
  return (60000000 / median).round().clamp(
    MetronomeSettings.minBpm,
    MetronomeSettings.maxBpm,
  );
}
