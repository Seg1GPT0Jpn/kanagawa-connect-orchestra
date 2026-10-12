/// 吹いている音の区切り（音が変わった・途切れた）を見つけ、直前の音・音程差・出だしの音程を出す
library;

/// 1つの音（同じ音名が続いた区間）
class NoteEvent {
  NoteEvent(this.midi);

  final int midi;
  int frames = 0;
  double _sum = 0;
  final List<double> _attack = [];
  double _settledSum = 0;
  int _settledFrames = 0;

  /// 出だしとみなすフレーム数（約0.1秒）
  static const attackFrames = 2;

  /// 出だしのあと、安定したとみなすまでのフレーム数
  static const settleAfter = 4;

  void add(double cents) {
    frames++;
    _sum += cents;
    if (_attack.length < attackFrames) _attack.add(cents);
    if (frames > settleAfter) {
      _settledSum += cents;
      _settledFrames++;
    }
  }

  double get meanCents => frames == 0 ? 0 : _sum / frames;

  /// 出だしの音程が、落ち着いたあとの音程からどれだけずれていたか（セント）。
  /// まだ落ち着いていなければ null
  double? get attackOffset {
    if (_settledFrames < 3 || _attack.isEmpty) return null;
    final attack = _attack.reduce((a, b) => a + b) / _attack.length;
    return attack - _settledSum / _settledFrames;
  }

  /// 落ち着いたあとの音程（セント）
  double? get settledCents =>
      _settledFrames == 0 ? null : _settledSum / _settledFrames;
}

class NoteTracker {
  /// 音とみなす最短のフレーム数（これより短い音は記録しない）
  static const minFrames = 4;

  NoteEvent? _current;
  NoteEvent? _previous;

  NoteEvent? get current => _current;

  /// 直前に吹いた音（いまの音の前）
  NoteEvent? get previous => _previous;

  /// いまの音と直前の音の差（半音の数。上なら正）
  int? get intervalSemitones {
    final c = _current, p = _previous;
    if (c == null || p == null) return null;
    return c.midi - p.midi;
  }

  void addFrame(int midi, double cents) {
    final c = _current;
    if (c != null && c.midi != midi) _finish();
    (_current ??= NoteEvent(midi)).add(cents);
  }

  /// 音が途切れた
  void silence() => _finish();

  void _finish() {
    final c = _current;
    _current = null;
    if (c != null && c.frames >= minFrames) _previous = c;
  }

  void reset() {
    _current = null;
    _previous = null;
  }
}

const _intervalNames = [
  '同じ音',
  '短2度',
  '長2度',
  '短3度',
  '長3度',
  '完全4度',
  '増4度',
  '完全5度',
  '短6度',
  '長6度',
  '短7度',
  '長7度',
];

/// 音程の名前（例：長3度上・1オクターブと完全5度下）
String intervalName(int semitones) {
  if (semitones == 0) return '同じ音';
  final up = semitones > 0;
  final n = semitones.abs();
  final octaves = n ~/ 12;
  final rest = n % 12;
  final parts = [
    if (octaves > 0) '$octavesオクターブ',
    if (rest > 0) _intervalNames[rest],
  ];
  return '${parts.join('と')}${up ? '上' : '下'}';
}
