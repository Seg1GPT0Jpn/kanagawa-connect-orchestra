import 'package:flutter_test/flutter_test.dart';
import 'package:kco_practice/features/audio_tools/domain/pitch.dart';

void main() {
  test('MIDI と周波数：A4 は基準ピッチ、オクターブで2倍', () {
    expect(midiToFrequency(69), 440);
    expect(midiToFrequency(69, a4: 442), 442);
    expect(midiToFrequency(81), closeTo(880, 1e-9));
    expect(midiToFrequency(60), closeTo(261.6256, 1e-3)); // 中央ド
    expect(frequencyToMidi(440), closeTo(69, 1e-12));
    expect(frequencyToMidi(466.1638), closeTo(70, 1e-4)); // B♭4
  });

  test('セント：半音は100セント、同じ高さは0', () {
    expect(centsBetween(440, 440), 0);
    expect(centsBetween(midiToFrequency(70), 440), closeTo(100, 1e-9));
    expect(centsBetween(220, 440), closeTo(-1200, 1e-9));
  });

  test('PitchReading：いちばん近い音とずれ', () {
    final r = PitchReading.fromFrequency(445, a4: 440);
    expect(r.midi, 69);
    expect(r.cents, closeTo(19.56, 0.01));
    final low = PitchReading.fromFrequency(
      midiToFrequency(70, a4: 442) * 0.99,
      a4: 442,
    );
    expect(low.midi, 70);
    expect(low.cents, closeTo(-17.4, 0.1));
  });

  test('音名：C4 は中央ド、B♭は♭で表す', () {
    expect(noteLabel(60), 'C4');
    expect(noteLabel(69), 'A4');
    expect(noteLabel(70), 'B♭4');
    expect(noteLabel(58), 'B♭3');
  });

  test('B♭管：記譜の C4 は実音の B♭3、実音 A4 は記譜 B4', () {
    const t = Transposition.bFlat;
    expect(t.writtenToConcert(60), 58);
    expect(t.concertToWritten(69), 71);
    expect(Transposition.concert.concertToWritten(69), 69);
    expect(Transposition.f.writtenToConcert(60), 53); // F管：記譜 C は実音 F（完全5度下）
    expect(Transposition.eFlat.writtenToConcert(60), 63); // E♭管：短3度上
  });
}
