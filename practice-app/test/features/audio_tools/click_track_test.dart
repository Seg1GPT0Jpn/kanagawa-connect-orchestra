import 'package:flutter_test/flutter_test.dart';
import 'package:kco_practice/features/audio_tools/domain/click_track.dart';
import 'package:kco_practice/features/audio_tools/domain/metronome.dart';

void main() {
  const track = ClickTrack(
    countInBars: 1,
    sections: [
      ClickSection(bars: 2, bpm: 120, beatsPerBar: 4),
      ClickSection(bars: 1, bpm: 60, beatsPerBar: 3, subdivision: 2),
    ],
  );

  test('予備拍1小節＋テンポ・拍子の変わる2区間', () {
    final (:clicks, :totalMicros) = buildClickTrack(track);
    // 予備拍 4 ＋ 区間1（2小節×4拍）8 ＋ 区間2（3拍×2分割）6
    expect(clicks, hasLength(18));
    // 予備拍は小節 0、区間 -1
    expect(clicks.first.bar, 0);
    expect(clicks.first.section, -1);
    expect(clicks.first.kind, ClickKind.accent);
    // 本編の1小節目は予備拍の2秒後（♩=120 で4拍）
    final firstBar = clicks.firstWhere((c) => c.bar == 1);
    expect(firstBar.offsetMicros, 2000000);
    expect(firstBar.kind, ClickKind.accent);
    // 区間2は 2 + 4 = 6秒後から、♩=60 の8分（0.5秒ごと）
    final sec2 = clicks.where((c) => c.section == 1).toList();
    expect(sec2.first.offsetMicros, 6000000);
    expect(sec2.first.bar, 3);
    expect(sec2.map((c) => c.offsetMicros - 6000000), [
      0,
      500000,
      1000000,
      1500000,
      2000000,
      2500000,
    ]);
    expect(sec2.map((c) => c.kind), [
      ClickKind.accent,
      ClickKind.subdivision,
      ClickKind.beat,
      ClickKind.subdivision,
      ClickKind.beat,
      ClickKind.subdivision,
    ]);
    expect(totalMicros, 9000000);
    expect(track.totalBars, 3);
  });

  test('予備拍なし・2小節', () {
    final (:clicks, :totalMicros) = buildClickTrack(
      const ClickTrack(
        countInBars: 0,
        sections: [ClickSection(bars: 2, bpm: 90, beatsPerBar: 2)],
      ),
    );
    expect(clicks.first.bar, 1);
    expect(clicks, hasLength(4));
    expect(totalMicros, (4 * 60000000 / 90).round());
  });

  test('予備拍は最初の区間のテンポ・拍子で、細分しない', () {
    final (:clicks, totalMicros: _) = buildClickTrack(
      const ClickTrack(
        countInBars: 2,
        sections: [
          ClickSection(bars: 1, bpm: 60, beatsPerBar: 3, subdivision: 4),
        ],
      ),
    );
    final countIn = clicks.where((c) => c.section == -1).toList();
    expect(countIn.map((c) => c.bar), [-1, -1, -1, 0, 0, 0]);
    expect(countIn.every((c) => c.kind != ClickKind.subdivision), isTrue);
  });

  test('保存して読み戻せる・壊れた値は直す', () {
    expect(ClickTrack.fromMap(track.toMap()).toMap(), track.toMap());
    final broken = ClickTrack.fromMap({
      'name': 3,
      'countIn': 9,
      'sections': 'x',
    });
    expect(broken.countInBars, 2);
    expect(broken.sections, [const ClickSection()]);
    expect(
      const ClickSection(bars: 0, bpm: 999).normalized(),
      const ClickSection(bars: 1, bpm: 300),
    );
  });
}
