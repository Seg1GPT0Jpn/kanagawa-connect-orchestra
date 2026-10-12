/// 音の高さの計算（決定論的。チューナー・基準音・音律で共通に使う）
library;

import 'dart:math' as math;

/// 音名（実音・記譜音の表示用。♯で表す）
const noteNames = [
  'C',
  'C♯',
  'D',
  'E♭',
  'E',
  'F',
  'F♯',
  'G',
  'A♭',
  'A',
  'B♭',
  'B',
];

/// 楽器の調（記譜音と実音の差）
enum Transposition {
  /// 実音（in C）
  concert('C管（実音）', '実音', 0),

  /// B♭管トランペット：記譜の C が実音の B♭（長2度＝2半音低く鳴る）
  bFlat('B♭管', 'B♭', -2),

  /// E♭管・F管（参考）
  eFlat('E♭管', 'E♭', 3),
  f('F管', 'F', -7);

  const Transposition(this.label, this.shortLabel, this.semitonesToConcert);

  final String label;

  /// ボタン用の短い名前
  final String shortLabel;

  /// 記譜音 + この値 = 実音（半音）
  final int semitonesToConcert;

  int concertToWritten(int concertMidi) => concertMidi - semitonesToConcert;
  int writtenToConcert(int writtenMidi) => writtenMidi + semitonesToConcert;
}

/// MIDI ノート番号 → 周波数（Hz）。A4（69）= [a4]
double midiToFrequency(num midi, {double a4 = 440}) =>
    a4 * math.pow(2, (midi - 69) / 12).toDouble();

/// 周波数 → MIDI ノート番号（小数。69.0 が A4）
double frequencyToMidi(double hz, {double a4 = 440}) =>
    69 + 12 * _log2(hz / a4);

/// 2つの周波数の差（セント。正なら [hz] の方が高い）
double centsBetween(double hz, double referenceHz) =>
    1200 * _log2(hz / referenceHz);

/// 「A4」「B♭3」のような音名（オクターブ番号は C4 = 中央ド＝60）
String noteLabel(int midi) => '${noteNames[midi % 12]}${midi ~/ 12 - 1}';

/// 周波数を、いちばん近い平均律の音と、そこからのずれ（セント）に分ける
class PitchReading {
  const PitchReading({
    required this.midi,
    required this.cents,
    required this.frequency,
  });

  factory PitchReading.fromFrequency(double hz, {double a4 = 440}) {
    final m = frequencyToMidi(hz, a4: a4);
    final nearest = m.round();
    return PitchReading(
      midi: nearest,
      cents: (m - nearest) * 100,
      frequency: hz,
    );
  }

  /// いちばん近い音（実音の MIDI 番号）
  final int midi;

  /// その音からのずれ（-50〜+50 セント）
  final double cents;
  final double frequency;
}

double _log2(double x) => math.log(x) / math.ln2;
