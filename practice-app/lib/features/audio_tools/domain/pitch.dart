/// 音の高さの計算（決定論的。チューナー・基準音・音律で共通に使う）
library;

import 'dart:math' as math;

/// 音名の表記
enum NoteNaming {
  english('英語式（C D E）', [
    'C', 'C♯', 'D', 'E♭', 'E', 'F', 'F♯', 'G', 'A♭', 'A', 'B♭', 'B', //
  ]),
  solfege('ドレミ（固定ド）', [
    'ド', 'ド♯', 'レ', 'ミ♭', 'ミ', 'ファ', 'ファ♯', 'ソ', 'ラ♭', 'ラ', 'シ♭', 'シ', //
  ]),
  german('ドイツ式（C D E … H）', [
    'C', 'Cis', 'D', 'Es', 'E', 'F', 'Fis', 'G', 'As', 'A', 'B', 'H', //
  ]),
  japanese('日本式（ハニホ）', [
    'ハ', '嬰ハ', 'ニ', '変ホ', 'ホ', 'ヘ', '嬰ヘ', 'ト', '変イ', 'イ', '変ロ', 'ロ', //
  ]);

  const NoteNaming(this.label, this.names);
  final String label;
  final List<String> names;

  static NoteNaming byName(Object? name) => values.firstWhere(
    (n) => n.name == name,
    orElse: () => NoteNaming.english,
  );
}

/// いま使っている音名の表記（設定で変える。画面のどこでも同じ表記にするため、アプリ全体で1つ）
NoteNaming currentNaming = NoteNaming.english;

/// 音名（オクターブなし）。表記は [currentNaming]
String pitchClassName(int pitchClass) => currentNaming.names[pitchClass % 12];

/// 音名（英語式。保存・計算の説明用）
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

  /// E♭管（E♭クラリネット・E♭コルネット）：短3度高く鳴る
  eFlat('E♭管', 'E♭', 3),

  /// F管（ホルン・イングリッシュホルン）：完全5度低く鳴る
  f('F管', 'F', -7),

  /// A管（A クラリネット）：短3度低く鳴る
  a('A管', 'A', -3),

  /// D管（D トランペット）：長2度高く鳴る
  d('D管', 'D', 2),

  /// E♭管（アルトサックス）：長6度低く鳴る
  eFlatAlto('E♭管（6度下）', 'E♭↓', -9),

  /// B♭管（テナーサックス・バスクラリネット・ユーフォニアムのト音記号）：長9度低く鳴る
  bFlatTenor('B♭管（9度下）', 'B♭↓', -14),

  /// E♭管（バリトンサックス）：1オクターブと長6度低く鳴る
  eFlatBari('E♭管（13度下）', 'E♭↓↓', -21),

  /// ピッコロ：1オクターブ高く鳴る
  piccolo('C管（1オクターブ上）', 'C↑', 12);

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
String noteLabel(int midi) => '${pitchClassName(midi)}${midi ~/ 12 - 1}';

/// 楽器を選ぶと、楽器の調が決まる
const instrumentPresets = <(String, Transposition)>[
  ('トランペット（B♭）', Transposition.bFlat),
  ('コルネット・フリューゲルホルン', Transposition.bFlat),
  ('C トランペット', Transposition.concert),
  ('D トランペット', Transposition.d),
  ('E♭ コルネット', Transposition.eFlat),
  ('ホルン（F）', Transposition.f),
  ('トロンボーン・チューバ（ヘ音記号）', Transposition.concert),
  ('ユーフォニアム（ト音記号）', Transposition.bFlatTenor),
  ('フルート・オーボエ・ファゴット', Transposition.concert),
  ('ピッコロ', Transposition.piccolo),
  ('クラリネット（B♭）', Transposition.bFlat),
  ('クラリネット（A）', Transposition.a),
  ('E♭ クラリネット', Transposition.eFlat),
  ('バスクラリネット', Transposition.bFlatTenor),
  ('ソプラノサックス', Transposition.bFlat),
  ('アルトサックス', Transposition.eFlatAlto),
  ('テナーサックス', Transposition.bFlatTenor),
  ('バリトンサックス', Transposition.eFlatBari),
  ('イングリッシュホルン', Transposition.f),
  ('弦楽器・鍵盤・声', Transposition.concert),
];

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
