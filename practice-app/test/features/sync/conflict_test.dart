import 'package:flutter_test/flutter_test.dart';
import 'package:kco_practice/features/sync/conflict.dart';

import '../../helpers.dart';

void main() {
  test('後から編集した方が残る（どちらから見ても同じ）', () {
    final older = record('r', updatedAt: 1000, by: 'devZ');
    final newer = record('r', updatedAt: 2000, by: 'devA');
    expect(resolveConflict(older, newer), same(newer));
    expect(resolveConflict(newer, older), same(newer));
  });

  test('同じ時刻なら端末 ID が大きい方', () {
    final a = record('r', by: 'devA', note: 'A');
    final b = record('r', by: 'devB', note: 'B');
    expect(resolveConflict(a, b), same(b));
    expect(resolveConflict(b, a), same(b));
  });

  test('時刻も端末も同じなら削除済みの方', () {
    final alive = record('r');
    final gone = record('r', deleted: true);
    expect(resolveConflict(alive, gone), same(gone));
    expect(resolveConflict(gone, alive), same(gone));
  });

  test('まったく同じならクラウドの方', () {
    final local = record('r');
    final remote = record('r');
    expect(resolveConflict(local, remote), same(remote));
  });
}
