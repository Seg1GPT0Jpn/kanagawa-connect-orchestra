/// 音程当て（聴き分けの練習）の問題づくりと採点（決定論的。乱数は外から渡す）
library;

import 'dart:math' as math;

/// 出題する音程（半音の数と名前）
const quizIntervals = <(int, String)>[
  (1, '短2度'),
  (2, '長2度'),
  (3, '短3度'),
  (4, '長3度'),
  (5, '完全4度'),
  (6, '増4度'),
  (7, '完全5度'),
  (8, '短6度'),
  (9, '長6度'),
  (10, '短7度'),
  (11, '長7度'),
  (12, 'オクターブ'),
];

/// やさしい組み合わせ（最初はこれから）
const easyIntervals = {3, 4, 5, 7, 12};

enum QuizMode {
  up('上へ（旋律）'),
  down('下へ（旋律）'),
  together('同時に（和音）');

  const QuizMode(this.label);
  final String label;
}

class IntervalQuestion {
  const IntervalQuestion({
    required this.root,
    required this.semitones,
    required this.mode,
  });

  /// 先に鳴らす音（実音）
  final int root;
  final int semitones;
  final QuizMode mode;

  /// 2つ目の音（実音）
  int get second => mode == QuizMode.down ? root - semitones : root + semitones;
}

class IntervalQuiz {
  IntervalQuiz({
    required this.intervals,
    required this.mode,
    math.Random? random,
    this.lowest = 55,
    this.highest = 79,
  }) : assert(intervals.isNotEmpty),
       _random = random ?? math.Random();

  /// 出題する音程（半音の数）
  final Set<int> intervals;
  final QuizMode mode;

  /// 鳴らす範囲（実音）。初期値は G3〜G5
  final int lowest;
  final int highest;
  final math.Random _random;
  int asked = 0;
  int correct = 0;

  /// 音程ごとの、出題数と正解数（苦手な音程を見つける）
  final Map<int, (int, int)> byInterval = {};

  IntervalQuestion next() {
    final list = intervals.toList()..sort();
    final s = list[_random.nextInt(list.length)];
    final lo = mode == QuizMode.down ? lowest + s : lowest;
    final hi = mode == QuizMode.down ? highest : highest - s;
    final root = lo >= hi ? lo : lo + _random.nextInt(hi - lo + 1);
    return IntervalQuestion(root: root, semitones: s, mode: mode);
  }

  /// 答える。正しければ true
  bool answer(IntervalQuestion q, int semitones) {
    final ok = q.semitones == semitones;
    asked++;
    if (ok) correct++;
    final (a, c) = byInterval[q.semitones] ?? (0, 0);
    byInterval[q.semitones] = (a + 1, c + (ok ? 1 : 0));
    return ok;
  }

  double get rate => asked == 0 ? 0 : correct / asked;
}

String intervalLabel(int semitones) =>
    quizIntervals.firstWhere((i) => i.$1 == semitones).$2;
