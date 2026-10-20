import 'package:flutter/material.dart';

import '../data/exercise_player.dart';
import '../data/reference_tone_controller.dart';
import '../domain/exercise.dart';
import '../domain/pitch.dart';

/// 練習音型（音階・分散和音・リップスラー）を基準音で鳴らす
class ExerciseView extends StatefulWidget {
  const ExerciseView({super.key, required this.tone});

  final ReferenceToneController tone;

  @override
  State<ExerciseView> createState() => _ExerciseViewState();
}

class _ExerciseViewState extends State<ExerciseView> {
  late final ExercisePlayer _player = ExercisePlayer(widget.tone);
  ExerciseKind _kind = ExerciseKind.majorScale;
  ValveCombo _valves = ValveCombo.open;
  int _bpm = 72;
  bool _loop = false;

  @override
  void dispose() {
    _player
      ..stop()
      ..dispose();
    super.dispose();
  }

  List<int> get _notes =>
      buildExercise(_kind, root: widget.tone.writtenMidi, valves: _valves);

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return ListenableBuilder(
      listenable: _player,
      builder: (context, _) {
        final notes = _player.isPlaying ? _player.notes : _notes;
        return Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text('練習音型', style: theme.textTheme.titleMedium),
            Text(
              _kind == ExerciseKind.lipSlur
                  ? '倍音列（記譜 C4〜G5 をピストンの組み合わせで下げる）を順に鳴らします'
                  : '上で選んでいる音（${noteLabel(widget.tone.writtenMidi)}）から始めます',
              style: theme.textTheme.bodySmall,
            ),
            const SizedBox(height: 4),
            DropdownButton<ExerciseKind>(
              isExpanded: true,
              value: _kind,
              items: [
                for (final k in ExerciseKind.values)
                  DropdownMenuItem(value: k, child: Text(k.label)),
              ],
              onChanged: (k) => setState(() => _kind = k!),
            ),
            if (_kind == ExerciseKind.lipSlur)
              Wrap(
                spacing: 4,
                children: [
                  for (final v in ValveCombo.values)
                    ChoiceChip(
                      label: Text(v.label),
                      selected: _valves == v,
                      onSelected: (_) => setState(() => _valves = v),
                    ),
                ],
              ),
            Row(
              children: [
                Text('テンポ $_bpm'),
                Expanded(
                  child: Slider(
                    value: _bpm.toDouble(),
                    min: 40,
                    max: 160,
                    divisions: 24,
                    onChanged: (v) => setState(() => _bpm = v.round()),
                  ),
                ),
                const Text('くり返す'),
                Switch(
                  value: _loop,
                  onChanged: (v) => setState(() => _loop = v),
                ),
              ],
            ),
            Wrap(
              spacing: 4,
              runSpacing: 4,
              children: [
                for (final (i, n) in notes.indexed)
                  Chip(
                    visualDensity: VisualDensity.compact,
                    label: Text(noteLabel(n)),
                    backgroundColor: i == _player.index
                        ? theme.colorScheme.primaryContainer
                        : null,
                  ),
              ],
            ),
            const SizedBox(height: 8),
            FilledButton.tonalIcon(
              onPressed: _player.isPlaying
                  ? _player.stop
                  : () => _player.play(_notes, bpm: _bpm, loop: _loop),
              icon: Icon(_player.isPlaying ? Icons.stop : Icons.play_arrow),
              label: Text(_player.isPlaying ? '止める' : '音型を鳴らす'),
            ),
          ],
        );
      },
    );
  }
}
