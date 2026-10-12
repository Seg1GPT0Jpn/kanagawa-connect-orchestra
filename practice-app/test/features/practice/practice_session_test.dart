import 'package:flutter_test/flutter_test.dart';
import 'package:kco_practice/features/menu/domain/menu_rules.dart';
import 'package:kco_practice/features/practice/domain/practice_session.dart';

void main() {
  final t0 = DateTime(2026, 10, 12, 9);
  DateTime at(int seconds) => t0.add(Duration(seconds: seconds));

  PracticeSession session() => PracticeSession.fromMenu(
    {
      'mouthpiece': 20,
      'long_tone': 15,
      'lip_slur': 0,
      'tonguing': 5,
      'arban': 30,
    },
    trumpetBasicRules,
    t0,
  );

  test('0分の項目は飛ばし、メニューの順に並ぶ', () {
    final s = session();
    expect(s.segments.map((x) => x.itemId), [
      'mouthpiece',
      'long_tone',
      'tonguing',
      'arban',
    ]);
    expect(s.segments.first.plannedSeconds, 1200);
    expect(s.isRunning, isTrue);
  });

  test('経過・残りは時刻の差で決まり、予定を過ぎると残りが負になる', () {
    final s = session();
    expect(s.elapsedSeconds(at(0)), 0);
    expect(s.remainingSeconds(at(90)), 1110);
    expect(s.remainingSeconds(at(1230)), -30);
  });

  test('一時停止中の時間は数えない', () {
    final s = session();
    s.pause(at(60));
    expect(s.isRunning, isFalse);
    expect(s.elapsedSeconds(at(600)), 60);
    s.resume(at(600));
    expect(s.elapsedSeconds(at(630)), 90);
    // 二重に呼んでも変わらない
    s.resume(at(640));
    s.pause(at(650));
    s.pause(at(700));
    expect(s.elapsedSeconds(at(9999)), 110);
  });

  test('次へで実績を記録し、最後の項目のあとで終了', () {
    final s = session();
    s.next(at(1200)); // マウスピース 20分
    expect(s.current.itemId, 'long_tone');
    s.next(at(1200 + 600)); // ロングトーン 10分
    s.next(at(1800 + 300)); // タンギング 5分
    expect(s.isLast, isTrue);
    s.next(at(2100 + 1800)); // Arban 30分
    expect(s.isFinished, isTrue);
    expect(s.finish(at(99999)), {
      'mouthpiece': 1200,
      'long_tone': 600,
      'tonguing': 300,
      'arban': 1800,
    });
  });

  test('一時停止中に次へ進むと、次の項目も止まったまま', () {
    final s = session();
    s.pause(at(100));
    s.next(at(500));
    expect(s.isRunning, isFalse);
    expect(s.elapsedSeconds(at(800)), 0);
  });

  test('途中で終えると、まだの項目は0秒', () {
    final s = session();
    s.next(at(1200));
    expect(s.finish(at(1500)), {
      'mouthpiece': 1200,
      'long_tone': 300,
      'tonguing': 0,
      'arban': 0,
    });
    // 終了後は何をしても変わらない
    s.next(at(2000));
    s.resume(at(2000));
    expect(s.finish(at(3000))['long_tone'], 300);
  });

  test('端末の時計が戻っても経過時間は負にならない', () {
    final s = session();
    expect(s.elapsedSeconds(at(-100)), 0);
  });
}
