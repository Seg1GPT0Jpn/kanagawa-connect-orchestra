import 'dart:math' as math;

import 'package:flutter_test/flutter_test.dart';
import 'package:kco_practice/features/audio_tools/domain/interval_quiz.dart';

void main() {
  test('出す音程・方向・範囲を守り、採点して音程ごとに数える', () {
    final quiz = IntervalQuiz(
      intervals: {3, 7},
      mode: QuizMode.down,
      random: math.Random(1),
    );
    for (var i = 0; i < 200; i++) {
      final q = quiz.next();
      expect({3, 7}, contains(q.semitones));
      expect(q.second, q.root - q.semitones);
      expect(q.second, greaterThanOrEqualTo(quiz.lowest));
      expect(q.root, lessThanOrEqualTo(quiz.highest));
    }
    const q = IntervalQuestion(root: 60, semitones: 7, mode: QuizMode.up);
    expect(q.second, 67);
    expect(quiz.answer(q, 7), isTrue);
    expect(quiz.answer(q, 3), isFalse);
    expect(quiz.rate, 0.5);
    expect(quiz.byInterval[7], (2, 1));
    expect(intervalLabel(12), 'オクターブ');
  });
}
