/// クリックトラック：テンポ・拍子が変わる曲のための、区間を並べたクリック（決定論的）
library;

import 'metronome.dart';

class ClickSection {
  const ClickSection({
    this.bars = 4,
    this.bpm = 120,
    this.beatsPerBar = 4,
    this.subdivision = 1,
  });

  final int bars;
  final int bpm;
  final int beatsPerBar;
  final int subdivision;

  ClickSection normalized() => ClickSection(
    bars: bars.clamp(1, 999),
    bpm: bpm.clamp(MetronomeSettings.minBpm, MetronomeSettings.maxBpm),
    beatsPerBar: beatsPerBar.clamp(1, 12),
    subdivision: subdivision.clamp(1, 4),
  );

  ClickSection copyWith({
    int? bars,
    int? bpm,
    int? beatsPerBar,
    int? subdivision,
  }) => ClickSection(
    bars: bars ?? this.bars,
    bpm: bpm ?? this.bpm,
    beatsPerBar: beatsPerBar ?? this.beatsPerBar,
    subdivision: subdivision ?? this.subdivision,
  ).normalized();

  /// この区間の長さ（マイクロ秒）
  int get durationMicros => (bars * beatsPerBar * 60000000 / bpm).round();

  Map<String, Object?> toMap() => {
    'bars': bars,
    'bpm': bpm,
    'beats': beatsPerBar,
    'sub': subdivision,
  };

  factory ClickSection.fromMap(Map<Object?, Object?> m) => ClickSection(
    bars: m['bars'] is int ? m['bars']! as int : 4,
    bpm: m['bpm'] is int ? m['bpm']! as int : 120,
    beatsPerBar: m['beats'] is int ? m['beats']! as int : 4,
    subdivision: m['sub'] is int ? m['sub']! as int : 1,
  ).normalized();

  @override
  bool operator ==(Object other) =>
      other is ClickSection &&
      other.bars == bars &&
      other.bpm == bpm &&
      other.beatsPerBar == beatsPerBar &&
      other.subdivision == subdivision;

  @override
  int get hashCode => Object.hash(bars, bpm, beatsPerBar, subdivision);
}

class ClickTrack {
  const ClickTrack({
    this.name = '新しいクリックトラック',
    this.countInBars = 1,
    this.sections = const [ClickSection()],
  });

  final String name;

  /// 予備拍（最初の区間のテンポ・拍子で数える小節数、0〜2）
  final int countInBars;
  final List<ClickSection> sections;

  int get totalBars => sections.fold(0, (s, x) => s + x.bars);

  ClickTrack copyWith({
    String? name,
    int? countInBars,
    List<ClickSection>? sections,
  }) => ClickTrack(
    name: name ?? this.name,
    countInBars: (countInBars ?? this.countInBars).clamp(0, 2),
    sections: sections ?? this.sections,
  );

  Map<String, Object?> toMap() => {
    'name': name,
    'countIn': countInBars,
    'sections': [for (final s in sections) s.toMap()],
  };

  factory ClickTrack.fromMap(Map<Object?, Object?> m) {
    final raw = m['sections'];
    final sections = [
      if (raw is List)
        for (final s in raw)
          if (s is Map) ClickSection.fromMap(s),
    ];
    return ClickTrack(
      name: m['name'] is String ? m['name']! as String : '新しいクリックトラック',
      countInBars: m['countIn'] is int ? (m['countIn']! as int).clamp(0, 2) : 1,
      sections: sections.isEmpty ? const [ClickSection()] : sections,
    );
  }
}

class TrackClick {
  const TrackClick({
    required this.offsetMicros,
    required this.kind,
    required this.bar,
    required this.beatInBar,
    required this.section,
  });

  /// 開始からの時刻（マイクロ秒）
  final int offsetMicros;
  final ClickKind kind;

  /// 小節番号（1から。予備拍は 0 以下：-1, 0）
  final int bar;

  /// 小節の何拍目か（0から）
  final int beatInBar;

  /// 区間の番号（0から。予備拍は -1）
  final int section;
}

/// クリックトラック全体のクリックの時刻表と、全体の長さ
({List<TrackClick> clicks, int totalMicros}) buildClickTrack(ClickTrack track) {
  final clicks = <TrackClick>[];
  var start = 0;

  void addSection(ClickSection s, int sectionIndex, int firstBar, int bars) {
    final perBar = s.beatsPerBar * s.subdivision;
    final rate = s.bpm * s.subdivision;
    for (var i = 0; i < bars * perBar; i++) {
      final beatIndex = i ~/ s.subdivision;
      final beatInBar = beatIndex % s.beatsPerBar;
      final isBeat = i % s.subdivision == 0;
      clicks.add(
        TrackClick(
          offsetMicros: start + (i * 60000000 / rate).round(),
          kind: !isBeat
              ? ClickKind.subdivision
              : (beatInBar == 0 && s.beatsPerBar > 1)
              ? ClickKind.accent
              : ClickKind.beat,
          bar: firstBar + i ~/ perBar,
          beatInBar: beatInBar,
          section: sectionIndex,
        ),
      );
    }
    start += (bars * s.beatsPerBar * 60000000 / s.bpm).round();
  }

  final first = track.sections.first.copyWith(subdivision: 1);
  addSection(first, -1, 1 - track.countInBars, track.countInBars);
  var bar = 1;
  for (final (i, s) in track.sections.indexed) {
    addSection(s, i, bar, s.bars);
    bar += s.bars;
  }
  return (clicks: clicks, totalMicros: start);
}
