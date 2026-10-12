import 'package:flutter/foundation.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:kco_practice/core/meta_store.dart';
import 'package:kco_practice/features/practice/data/usage_tracker.dart';
import 'package:kco_practice/features/practice/presentation/calendar_page.dart';

import '../../helpers.dart';

class _Switch extends ChangeNotifier {
  bool on = false;
  void set(bool v) {
    on = v;
    notifyListeners();
  }
}

void main() {
  test('道具が動いていた時間を日ごとに数え、保存する（いま動いている分も見える）', () async {
    final meta = MetaStore(await openMemoryDb());
    final clock = FakeClock(DateTime(2026, 10, 12, 18));
    final usage = UsageTracker(meta, clock: clock.call);
    final metro = _Switch();
    usage.watch(UsageKind.metronome, metro, () => metro.on);

    metro.set(true);
    clock.advance(const Duration(minutes: 3));
    expect((await usage.secondsOn('2026-10-12'))[UsageKind.metronome], 180);
    metro.set(false);
    await Future<void>.delayed(Duration.zero);
    metro.set(true);
    clock.advance(const Duration(minutes: 2));
    metro.set(false);
    await Future<void>.delayed(Duration.zero);

    final again = UsageTracker(meta, clock: clock.call);
    expect((await again.secondsOn('2026-10-12'))[UsageKind.metronome], 300);
    expect(await again.secondsOn('2026-10-13'), isEmpty);
  });

  test('1日の目標：決めて保存、0 は目標なし、壊れた値は読まない', () async {
    final meta = MetaStore(await openMemoryDb());
    final g = await GoalsController.load(meta);
    expect(g.goals.of(UsageKind.practice), 30); // 初期値
    await g.setGoal(UsageKind.tuner, 10);
    await g.setGoal(UsageKind.practice, 0);
    final again = await GoalsController.load(meta);
    expect(again.goals.of(UsageKind.tuner), 10);
    expect(again.goals.of(UsageKind.practice), 0);
    expect(DailyGoals.fromMap({'tuner': 'x', 'tone': -3}).isEmpty, isTrue);
  });

  test('カレンダー：日ごとの練習の分（削除済みは除く）', () {
    final m = minutesByDay([
      record('a', day: '2026-10-01', actual: {'long_tone': 600}),
      record('b', day: '2026-10-01', actual: {'mouthpiece': 300}),
      record('c', day: '2026-10-02', deleted: true),
    ]);
    expect(m, {'2026-10-01': 15});
  });
}
