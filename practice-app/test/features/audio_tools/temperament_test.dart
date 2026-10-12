import 'package:flutter_test/flutter_test.dart';
import 'package:kco_practice/features/audio_tools/domain/temperament.dart';

void main() {
  test('平均律はずれなし', () {
    for (var i = 0; i < 12; i++) {
      expect(Temperament.equal.offsetCents(i), 0);
    }
  });

  test('純正律（長調）：よく知られたずれ', () {
    const t = Temperament.justMajor;
    expect(t.offsetCents(0), 0);
    expect(t.offsetCents(4), closeTo(-13.69, 0.01)); // 長3度
    expect(t.offsetCents(7), closeTo(1.96, 0.01)); // 完全5度
    expect(t.offsetCents(9), closeTo(-15.64, 0.01)); // 長6度
    expect(t.offsetCents(11), closeTo(-11.73, 0.01)); // 長7度
    expect(t.offsetCents(5), closeTo(-1.96, 0.01)); // 完全4度
  });

  test('純正律（短調）：短3度は高く、短7度は 9/5', () {
    expect(Temperament.justMinor.offsetCents(3), closeTo(15.64, 0.01));
    expect(Temperament.justMinor.offsetCents(10), closeTo(17.60, 0.01));
  });

  test('ピタゴラス音律：長3度は約8セント高い', () {
    expect(Temperament.pythagorean.offsetCents(4), closeTo(7.82, 0.01));
    expect(Temperament.pythagorean.offsetCents(7), closeTo(1.96, 0.01));
  });

  test('offsetFor：主音からの音程で決まる（オクターブ違いも同じ）', () {
    // 主音 B♭（10）での D（実音 D5＝74）は長3度
    expect(Temperament.justMajor.offsetFor(74, 10), closeTo(-13.69, 0.01));
    expect(Temperament.justMajor.offsetFor(62, 10), closeTo(-13.69, 0.01));
    // F（5度）
    expect(Temperament.justMajor.offsetFor(77, 10), closeTo(1.96, 0.01));
    expect(intervalNames[(74 - 10) % 12], '長3度');
  });
}
