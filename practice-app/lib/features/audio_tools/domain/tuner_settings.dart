/// チューナーの表示と判定の設定
library;

enum TunerDisplay {
  target('ターゲット'),
  bar('横棒'),
  none('表示なし');

  const TunerDisplay(this.label);
  final String label;
}

/// 応答速度（音程を何フレーム分の中央値でならすか）
enum TunerDamping {
  fast('速い', 3),
  normal('ふつう', 5),
  slow('ゆっくり', 9);

  const TunerDamping(this.label, this.frames);
  final String label;
  final int frames;
}

/// 判定範囲の選択肢（±セント）と、その目安
const toleranceChoices = <(double, String)>[
  (2, '±2（とても厳しい）'),
  (3, '±3（厳しい）'),
  (5, '±5（管楽器のふつう）'),
  (10, '±10（ゆるめ・声楽など）'),
];

class TunerSettings {
  const TunerSettings({
    this.display = TunerDisplay.target,
    this.tolerance = 5,
    this.decimal = false,
    this.damping = TunerDamping.normal,
    this.showToneMeter = true,
    this.showLevel = true,
    this.showPrevious = true,
    this.showAttack = true,
    this.showTracker = true,
  });

  final TunerDisplay display;

  /// 「合っている」とみなす範囲（±セント）
  final double tolerance;

  /// セントを 0.1 単位で出す
  final bool decimal;
  final TunerDamping damping;
  final bool showToneMeter;
  final bool showLevel;

  /// 直前の音と、音程の差
  final bool showPrevious;

  /// 音の出だしの音程
  final bool showAttack;

  /// 合っていた割合
  final bool showTracker;

  TunerSettings copyWith({
    TunerDisplay? display,
    double? tolerance,
    bool? decimal,
    TunerDamping? damping,
    bool? showToneMeter,
    bool? showLevel,
    bool? showPrevious,
    bool? showAttack,
    bool? showTracker,
  }) => TunerSettings(
    display: display ?? this.display,
    tolerance: tolerance ?? this.tolerance,
    decimal: decimal ?? this.decimal,
    damping: damping ?? this.damping,
    showToneMeter: showToneMeter ?? this.showToneMeter,
    showLevel: showLevel ?? this.showLevel,
    showPrevious: showPrevious ?? this.showPrevious,
    showAttack: showAttack ?? this.showAttack,
    showTracker: showTracker ?? this.showTracker,
  );

  Map<String, Object?> toMap() => {
    'display': display.name,
    'tolerance': tolerance,
    'decimal': decimal,
    'damping': damping.name,
    'toneMeter': showToneMeter,
    'level': showLevel,
    'previous': showPrevious,
    'attack': showAttack,
    'tracker': showTracker,
  };

  /// 壊れた値は既定値で読む
  factory TunerSettings.fromMap(Map<Object?, Object?> m) {
    const d = TunerSettings();
    final tol = m['tolerance'];
    return TunerSettings(
      display: TunerDisplay.values.firstWhere(
        (v) => v.name == m['display'],
        orElse: () => d.display,
      ),
      tolerance: tol is num && tol >= 1 && tol <= 20 ? tol.toDouble() : 5,
      decimal: m['decimal'] == true,
      damping: TunerDamping.values.firstWhere(
        (v) => v.name == m['damping'],
        orElse: () => d.damping,
      ),
      showToneMeter: m['toneMeter'] != false,
      showLevel: m['level'] != false,
      showPrevious: m['previous'] != false,
      showAttack: m['attack'] != false,
      showTracker: m['tracker'] != false,
    );
  }

  @override
  bool operator ==(Object other) =>
      other is TunerSettings && _mapEq(other.toMap(), toMap());

  @override
  int get hashCode => Object.hashAll(toMap().values);
}

bool _mapEq(Map<String, Object?> a, Map<String, Object?> b) =>
    a.length == b.length && a.keys.every((k) => a[k] == b[k]);

/// セントの表示（[decimal] なら 0.1 単位。0 は ±0）
String formatCents(double cents, {bool decimal = false}) {
  final digits = decimal ? 1 : 0;
  final rounded = double.parse(cents.toStringAsFixed(digits));
  final abs = rounded.abs().toStringAsFixed(digits);
  if (rounded == 0) return '±$abs';
  return '${rounded > 0 ? '+' : '-'}$abs';
}
