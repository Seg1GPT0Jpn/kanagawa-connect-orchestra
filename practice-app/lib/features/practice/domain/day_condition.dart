/// 今日の予定と調子から、練習の量をすすめる（決定論的なルール。AI は使わない）
///
/// 調査（docs/practice-research.md）の考え方：
///  ・合奏・本番も唇の負荷になる（Chris Martin）。本番前は必要な準備だけにして、練習で疲れ切らない
///  ・忙しい時期は練習量を減らした方が安定する（Steve Hendrickson）
///  ・高音・大音量の翌日は柔らかい音で（Brian Shaw）
///  ・疲労や痛みが出たら、時間を埋めるために吹き続けない
library;

enum Fatigue { fresh, normal, tired }

class DayCondition {
  const DayCondition({
    this.rehearsal = false,
    this.performance = false,
    this.fatigue = Fatigue.normal,
    this.lipPain = false,
    this.heavyYesterday = false,
  });

  /// 今日、合奏・レッスンがある
  final bool rehearsal;

  /// 今日、本番がある
  final bool performance;
  final Fatigue fatigue;

  /// 唇が痛い・腫れている
  final bool lipPain;

  /// 昨日、高音・大音量を多く吹いた
  final bool heavyYesterday;

  DayCondition copyWith({
    bool? rehearsal,
    bool? performance,
    Fatigue? fatigue,
    bool? lipPain,
    bool? heavyYesterday,
  }) => DayCondition(
    rehearsal: rehearsal ?? this.rehearsal,
    performance: performance ?? this.performance,
    fatigue: fatigue ?? this.fatigue,
    lipPain: lipPain ?? this.lipPain,
    heavyYesterday: heavyYesterday ?? this.heavyYesterday,
  );

  Map<String, Object?> toMap() => {
    'rehearsal': rehearsal,
    'performance': performance,
    'fatigue': fatigue.name,
    'lipPain': lipPain,
    'heavyYesterday': heavyYesterday,
  };

  /// 壊れた値は既定値で読む
  factory DayCondition.fromMap(Map<Object?, Object?> m) => DayCondition(
    rehearsal: m['rehearsal'] == true,
    performance: m['performance'] == true,
    fatigue: Fatigue.values.firstWhere(
      (f) => f.name == m['fatigue'],
      orElse: () => Fatigue.normal,
    ),
    lipPain: m['lipPain'] == true,
    heavyYesterday: m['heavyYesterday'] == true,
  );

  @override
  bool operator ==(Object other) =>
      other is DayCondition &&
      other.rehearsal == rehearsal &&
      other.performance == performance &&
      other.fatigue == fatigue &&
      other.lipPain == lipPain &&
      other.heavyYesterday == heavyYesterday;

  @override
  int get hashCode =>
      Object.hash(rehearsal, performance, fatigue, lipPain, heavyYesterday);
}

class DayAdvice {
  const DayAdvice({
    required this.message,
    this.modeId,
    this.presetId,
    this.rest = false,
  });

  /// 画面に出す説明
  final String message;

  /// すすめる時間モード（menu_rules.dart の id）。null なら今のまま
  final String? modeId;

  /// すすめるおすすめメニュー（通常モードのときだけ。menu_presets.dart の id）
  final String? presetId;

  /// 今日は吹かずに休む方がよい
  final bool rest;
}

/// 上から順に当てはまったものを返す
DayAdvice adviseForDay(DayCondition c) {
  if (c.lipPain) {
    return const DayAdvice(
      rest: true,
      message: '唇が痛いときは、今日は吹かずに休みましょう。痛みや腫れが続くときは、指導者や医療機関に相談してください。',
    );
  }
  if (c.performance) {
    return const DayAdvice(
      modeId: 'trumpet_20min',
      message: '本番の日は、練習は整える程度に（20分）。本番で吹く分の余力を残しましょう。',
    );
  }
  if (c.fatigue == Fatigue.tired) {
    return DayAdvice(
      modeId: c.rehearsal ? 'trumpet_10min' : 'trumpet_20min',
      message: c.rehearsal
          ? '疲れていて合奏もある日は、音を出して確かめるだけ（10分）にしましょう。'
          : '疲れている日は短め（20分）に。無理に時間を埋めなくて大丈夫です。',
    );
  }
  if (c.rehearsal) {
    return const DayAdvice(
      modeId: 'trumpet_basic',
      presetId: 'short',
      message: '合奏・レッスンでも吹くので、個人練習は短め（45分）に。曲は難所だけ確認しましょう。',
    );
  }
  if (c.heavyYesterday) {
    return const DayAdvice(
      modeId: 'trumpet_basic',
      presetId: 'tone_flexibility',
      message: '昨日たくさん高音・大音量を吹いたので、今日は柔らかい音で音色・柔軟性を中心に。',
    );
  }
  return const DayAdvice(message: 'いつもどおりのメニューで練習しましょう。');
}
