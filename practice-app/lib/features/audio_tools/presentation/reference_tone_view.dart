import 'dart:math' as math;

import 'package:flutter/material.dart';

import '../../../app/app_services.dart';
import '../data/reference_tone_controller.dart';
import '../domain/pitch.dart';
import '../domain/sound.dart';
import '../domain/temperament.dart';
import 'exercise_view.dart';
import 'interval_trainer_page.dart';
import 'temperament_editor_page.dart';

/// 基準音の画面：ホイール・鍵盤で音を選ぶ。1つの音・和音・ドローン。音色と音量
class ReferenceToneView extends StatefulWidget {
  const ReferenceToneView({super.key, required this.controller});

  final ReferenceToneController controller;

  @override
  State<ReferenceToneView> createState() => _ReferenceToneViewState();
}

class _ReferenceToneViewState extends State<ReferenceToneView> {
  /// 和音として重ねる（オフなら1つの音）
  bool _chordMode = false;

  /// 選んでいる音域（記譜のオクターブ番号）。音を選んでも変わらない＝音域の固定
  late int _octave =
      widget.controller.pitch.transposition.concertToWritten(
            widget.controller.concertMidi,
          ) ~/
          12 -
      1;

  ReferenceToneController get c => widget.controller;

  int _writtenOf(int pc) => (_octave + 1) * 12 + pc;

  Future<void> _tapWritten(int written) {
    final concert = c.pitch.transposition.writtenToConcert(written);
    if (_chordMode) return c.toggleHeld(concert);
    // 1つの音：選んだ音を鳴らす（鳴っていれば高さだけ変わる）
    return c.playConcert(concert);
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return ListenableBuilder(
      listenable: c,
      builder: (context, _) {
        final p = c.pitch;
        final t = p.transposition;
        final written = c.writtenMidi;
        final heldWritten = {for (final m in c.held) t.concertToWritten(m)};
        final selected = _chordMode ? heldWritten : {written};
        return ListView(
          padding: const EdgeInsets.all(16),
          children: [
            Column(
              children: [
                if (t != Transposition.concert)
                  Text('${t.label}の記譜', style: theme.textTheme.bodySmall),
                Text(
                  _chordMode
                      ? (c.held.isEmpty
                            ? '和音：音を押して重ねる'
                            : ([
                                ...heldWritten,
                              ]..sort()).map(noteLabel).join('・'))
                      : noteLabel(written),
                  style: _chordMode
                      ? theme.textTheme.headlineSmall
                      : theme.textTheme.displayMedium,
                  textAlign: TextAlign.center,
                ),
                if (!_chordMode)
                  Text(
                    '実音 ${noteLabel(c.concertMidi)}・${c.frequency.toStringAsFixed(1)} Hz',
                  ),
              ],
            ),
            const SizedBox(height: 8),
            SegmentedButton<bool>(
              segments: const [
                ButtonSegment(value: false, label: Text('1つの音')),
                ButtonSegment(value: true, label: Text('和音（重ねる）')),
              ],
              selected: {_chordMode},
              showSelectedIcon: false,
              onSelectionChanged: (v) {
                c.stop();
                setState(() => _chordMode = v.single);
              },
            ),
            const SizedBox(height: 8),
            Center(
              child: NoteWheel(
                selectedPitchClasses: {
                  for (final w in selected)
                    if (w ~/ 12 - 1 == _octave || _chordMode) w % 12,
                },
                onTap: (pc) => _tapWritten(_writtenOf(pc)),
              ),
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                IconButton(
                  tooltip: '1オクターブ下',
                  onPressed: _octave > 1
                      ? () => setState(() => _octave--)
                      : null,
                  icon: const Icon(Icons.chevron_left),
                ),
                Text('音域：オクターブ $_octave', style: theme.textTheme.titleMedium),
                IconButton(
                  tooltip: '1オクターブ上',
                  onPressed: _octave < 7
                      ? () => setState(() => _octave++)
                      : null,
                  icon: const Icon(Icons.chevron_right),
                ),
              ],
            ),
            PianoKeyboard(
              firstWritten: (_octave + 1) * 12,
              octaves: 2,
              selected: selected,
              onTap: _tapWritten,
            ),
            const SizedBox(height: 12),
            if (!_chordMode)
              FilledButton.icon(
                style: FilledButton.styleFrom(
                  minimumSize: const Size.fromHeight(56),
                ),
                onPressed: c.toggle,
                icon: Icon(c.isSinglePlaying ? Icons.stop : Icons.volume_up),
                label: Text(c.isSinglePlaying ? '止める' : '鳴らす'),
              )
            else ...[
              Text('和音（いま選んでいる音を根音に）', style: theme.textTheme.titleSmall),
              Wrap(
                spacing: 6,
                children: [
                  for (final type in ChordType.values)
                    ActionChip(
                      label: Text(type.label),
                      onPressed: () => c.playChord(c.concertMidi, type),
                    ),
                ],
              ),
              Row(
                children: [
                  Expanded(
                    child: OutlinedButton.icon(
                      onPressed: c.playDrone,
                      icon: const Icon(Icons.graphic_eq),
                      label: Text(
                        'ドローン（主音 ${pitchClassName(t.concertToWritten(p.tonicPitchClass + 60) % 12)}＋5度）',
                      ),
                    ),
                  ),
                  const SizedBox(width: 8),
                  FilledButton.icon(
                    onPressed: c.held.isEmpty ? null : c.stopHeld,
                    icon: const Icon(Icons.stop),
                    label: const Text('止める'),
                  ),
                ],
              ),
              Text(
                p.temperament == Temperament.equal
                    ? '音律を純正律にすると、和音がうなりのない高さで鳴ります'
                    : '${p.temperamentLabel}の高さで鳴らしています',
                style: theme.textTheme.bodySmall,
              ),
            ],
            if (c.error != null) ...[
              const SizedBox(height: 8),
              Text(c.error!, style: TextStyle(color: theme.colorScheme.error)),
            ],
            const SizedBox(height: 12),
            Row(
              children: [
                const Text('音色'),
                const SizedBox(width: 12),
                Expanded(
                  child: DropdownButton<Timbre>(
                    isExpanded: true,
                    value: c.timbre,
                    items: [
                      for (final tb in Timbre.values)
                        DropdownMenuItem(value: tb, child: Text(tb.label)),
                    ],
                    onChanged: (v) => v == null ? null : c.setTimbre(v),
                  ),
                ),
              ],
            ),
            Row(
              children: [
                const Text('音量'),
                Expanded(
                  child: Slider(
                    value: c.volume,
                    min: 0.05,
                    max: 1,
                    onChanged: c.setVolume,
                  ),
                ),
              ],
            ),
            Text(
              '音量に気をつけてください。イヤホンのときは小さめから。',
              style: theme.textTheme.bodySmall,
            ),
            const Divider(height: 32),
            ExerciseView(tone: c),
            const SizedBox(height: 8),
            OutlinedButton.icon(
              onPressed: () => Navigator.push(
                context,
                MaterialPageRoute<void>(
                  builder: (_) => IntervalTrainerPage(tone: c),
                ),
              ),
              icon: const Icon(Icons.hearing_outlined),
              label: const Text('音程当て（聴き分けの練習）'),
            ),
            const Divider(height: 32),
            PitchSettingsPanel(controller: c),
          ],
        );
      },
    );
  }
}

/// 12の音を円に並べたホイール（記譜の音名）。押すとその音を選ぶ
class NoteWheel extends StatelessWidget {
  const NoteWheel({
    super.key,
    required this.selectedPitchClasses,
    required this.onTap,
    this.size = 220,
  });

  final Set<int> selectedPitchClasses;
  final ValueChanged<int> onTap;
  final double size;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final r = size / 2;
    const button = 46.0;
    return SizedBox(
      width: size,
      height: size,
      child: Stack(
        children: [
          for (var pc = 0; pc < 12; pc++)
            Builder(
              builder: (context) {
                // C を上に、時計回り
                final a = -math.pi / 2 + pc * math.pi / 6;
                final x = r + (r - button / 2 - 2) * math.cos(a) - button / 2;
                final y = r + (r - button / 2 - 2) * math.sin(a) - button / 2;
                final sel = selectedPitchClasses.contains(pc);
                return Positioned(
                  left: x,
                  top: y,
                  width: button,
                  height: button,
                  child: Semantics(
                    button: true,
                    label: pitchClassName(pc),
                    child: Material(
                      shape: const CircleBorder(),
                      color: sel
                          ? theme.colorScheme.primary
                          : theme.colorScheme.surfaceContainerHighest,
                      child: InkWell(
                        customBorder: const CircleBorder(),
                        onTap: () => onTap(pc),
                        child: Center(
                          child: Text(
                            pitchClassName(pc),
                            style: TextStyle(
                              fontSize: pitchClassName(pc).length > 2 ? 11 : 15,
                              color: sel ? theme.colorScheme.onPrimary : null,
                            ),
                          ),
                        ),
                      ),
                    ),
                  ),
                );
              },
            ),
        ],
      ),
    );
  }
}

/// 鍵盤（記譜）。押すとその音を選ぶ・重ねる
class PianoKeyboard extends StatelessWidget {
  const PianoKeyboard({
    super.key,
    required this.firstWritten,
    required this.octaves,
    required this.selected,
    required this.onTap,
    this.height = 110,
  });

  /// いちばん左の C（記譜の MIDI 番号）
  final int firstWritten;
  final int octaves;
  final Set<int> selected;
  final ValueChanged<int> onTap;
  final double height;

  static const _whiteSteps = [0, 2, 4, 5, 7, 9, 11];
  static const _blackSteps = {1: 0, 3: 1, 6: 3, 8: 4, 10: 5};

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return SizedBox(
      height: height,
      child: LayoutBuilder(
        builder: (context, box) {
          final whites = octaves * 7 + 1;
          final w = box.maxWidth / whites;
          final keys = <Widget>[];
          for (var i = 0; i < whites; i++) {
            final midi = firstWritten + (i ~/ 7) * 12 + _whiteSteps[i % 7];
            final sel = selected.contains(midi);
            keys.add(
              Positioned(
                left: i * w,
                width: w,
                top: 0,
                bottom: 0,
                child: _Key(
                  label: midi % 12 == 0 ? noteLabel(midi) : '',
                  color: sel
                      ? theme.colorScheme.primaryContainer
                      : Colors.white,
                  border: theme.colorScheme.outline,
                  onTap: () => onTap(midi),
                  semantics: noteLabel(midi),
                ),
              ),
            );
          }
          for (var o = 0; o < octaves; o++) {
            for (final MapEntry(key: step, value: afterWhite)
                in _blackSteps.entries) {
              final midi = firstWritten + o * 12 + step;
              final sel = selected.contains(midi);
              keys.add(
                Positioned(
                  left: (o * 7 + afterWhite + 1) * w - w * 0.3,
                  width: w * 0.6,
                  top: 0,
                  height: height * 0.6,
                  child: _Key(
                    label: '',
                    color: sel ? theme.colorScheme.primary : Colors.black87,
                    border: Colors.black,
                    onTap: () => onTap(midi),
                    semantics: noteLabel(midi),
                  ),
                ),
              );
            }
          }
          return Stack(children: keys);
        },
      ),
    );
  }
}

class _Key extends StatelessWidget {
  const _Key({
    required this.label,
    required this.color,
    required this.border,
    required this.onTap,
    required this.semantics,
  });

  final String label;
  final Color color;
  final Color border;
  final VoidCallback onTap;
  final String semantics;

  @override
  Widget build(BuildContext context) => Semantics(
    button: true,
    label: semantics,
    child: GestureDetector(
      onTap: onTap,
      child: Container(
        decoration: BoxDecoration(
          color: color,
          border: Border.all(color: border, width: 0.5),
          borderRadius: const BorderRadius.vertical(bottom: Radius.circular(4)),
        ),
        alignment: Alignment.bottomCenter,
        padding: const EdgeInsets.only(bottom: 4),
        child: Text(
          label,
          style: const TextStyle(fontSize: 10, color: Colors.black54),
        ),
      ),
    ),
  );
}

/// 基準ピッチ（A4）・楽器・音名の表記・音律の設定。チューナーでも使う
class PitchSettingsPanel extends StatelessWidget {
  const PitchSettingsPanel({super.key, required this.controller});

  final ReferenceToneController controller;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final library = AppScope.of(context).temperaments;
    return ListenableBuilder(
      listenable: Listenable.merge([controller, library]),
      builder: (context, _) {
        final p = controller.pitch;
        void set(PitchSettings n) => controller.updatePitch(n);
        // 音律の選択肢：決まった音律と、自分で作った音律
        final temperamentValue = p.usesCustom
            ? 'custom:${p.custom!.id}'
            : p.temperament.name;
        return Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('基準ピッチ（A4）', style: theme.textTheme.titleSmall),
            Row(
              children: [
                IconButton(
                  onPressed: () => set(p.copyWith(a4: p.a4 - 1)),
                  icon: const Icon(Icons.remove),
                ),
                Text(
                  '${p.a4.toStringAsFixed(0)} Hz',
                  style: theme.textTheme.titleLarge,
                ),
                IconButton(
                  onPressed: () => set(p.copyWith(a4: p.a4 + 1)),
                  icon: const Icon(Icons.add),
                ),
                const Spacer(),
                for (final hz in const [440.0, 442.0])
                  Padding(
                    padding: const EdgeInsets.only(left: 6),
                    child: ChoiceChip(
                      label: Text(hz.toStringAsFixed(0)),
                      selected: p.a4 == hz,
                      onSelected: (_) => set(p.copyWith(a4: hz)),
                    ),
                  ),
              ],
            ),
            const SizedBox(height: 8),
            Text('楽器（音名の表示の調）', style: theme.textTheme.titleSmall),
            DropdownButton<String>(
              isExpanded: true,
              value: instrumentPresets.any((i) => i.$1 == p.instrument)
                  ? p.instrument
                  : '',
              items: [
                DropdownMenuItem(
                  value: '',
                  child: Text('楽器を選ぶ（いま：${p.transposition.label}）'),
                ),
                for (final (name, tr) in instrumentPresets)
                  DropdownMenuItem(
                    value: name,
                    child: Text('$name：${tr.label}'),
                  ),
              ],
              onChanged: (name) {
                if (name == null || name.isEmpty) return;
                final tr = instrumentPresets.firstWhere((i) => i.$1 == name).$2;
                set(p.copyWith(instrument: name, transposition: tr));
              },
            ),
            Wrap(
              spacing: 4,
              runSpacing: 4,
              children: [
                for (final tr in Transposition.values)
                  ChoiceChip(
                    label: Text(tr.label),
                    selected: p.transposition == tr,
                    onSelected: (_) =>
                        set(p.copyWith(transposition: tr, instrument: '')),
                  ),
              ],
            ),
            const SizedBox(height: 12),
            Text('音名の表記', style: theme.textTheme.titleSmall),
            DropdownButton<NoteNaming>(
              isExpanded: true,
              value: p.naming,
              items: [
                for (final n in NoteNaming.values)
                  DropdownMenuItem(value: n, child: Text(n.label)),
              ],
              onChanged: (n) => n == null ? null : set(p.copyWith(naming: n)),
            ),
            const SizedBox(height: 12),
            Row(
              children: [
                Expanded(child: Text('音律', style: theme.textTheme.titleSmall)),
                TextButton.icon(
                  onPressed: () => Navigator.push(
                    context,
                    MaterialPageRoute<void>(
                      builder: (_) => const TemperamentListPage(),
                    ),
                  ),
                  icon: const Icon(Icons.edit_outlined, size: 18),
                  label: const Text('自分の音律を作る'),
                ),
              ],
            ),
            DropdownButton<String>(
              isExpanded: true,
              value: temperamentValue,
              items: [
                for (final t in Temperament.values)
                  if (t != Temperament.custom)
                    DropdownMenuItem(value: t.name, child: Text(t.label)),
                for (final c in library.items)
                  DropdownMenuItem(
                    value: 'custom:${c.id}',
                    child: Text('★ ${c.name}'),
                  ),
                if (p.usesCustom && library.byId(p.custom!.id) == null)
                  DropdownMenuItem(
                    value: temperamentValue,
                    child: Text('★ ${p.custom!.name}'),
                  ),
              ],
              onChanged: (v) {
                if (v == null) return;
                if (v.startsWith('custom:')) {
                  final c = library.byId(v.substring(7));
                  if (c == null) return;
                  set(p.copyWith(temperament: Temperament.custom, custom: c));
                } else {
                  set(
                    p.copyWith(
                      temperament: Temperament.values.firstWhere(
                        (t) => t.name == v,
                      ),
                    ),
                  );
                }
              },
            ),
            Text(
              p.usesCustom
                  ? Temperament.custom.description
                  : p.temperament.description,
              style: theme.textTheme.bodySmall,
            ),
            if (p.temperament != Temperament.equal) ...[
              const SizedBox(height: 8),
              Text('主音（調）', style: theme.textTheme.titleSmall),
              const SizedBox(height: 4),
              Wrap(
                spacing: 4,
                runSpacing: 4,
                children: [
                  for (var pc = 0; pc < 12; pc++)
                    ChoiceChip(
                      label: Text(
                        p.transposition == Transposition.concert
                            ? pitchClassName(pc)
                            : '${pitchClassName(pc)}（記譜${pitchClassName(p.transposition.concertToWritten(pc + 60))}）',
                      ),
                      selected: p.tonicPitchClass == pc,
                      onSelected: (_) => set(p.copyWith(tonicPitchClass: pc)),
                    ),
                ],
              ),
            ],
          ],
        );
      },
    );
  }
}
