import 'package:flutter/material.dart';

import '../data/reference_tone_controller.dart';
import '../domain/pitch.dart';
import '../domain/temperament.dart';

/// 基準音の画面（実音と、楽器の記譜音を並べて表示）
class ReferenceToneView extends StatelessWidget {
  const ReferenceToneView({super.key, required this.controller});

  final ReferenceToneController controller;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return ListenableBuilder(
      listenable: controller,
      builder: (context, _) {
        final p = controller.pitch;
        final t = p.transposition;
        return ListView(
          padding: const EdgeInsets.all(16),
          children: [
            PitchSettingsPanel(controller: controller),
            const Divider(height: 32),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                IconButton.outlined(
                  tooltip: '半音下げる',
                  onPressed: () =>
                      controller.selectConcert(controller.concertMidi - 1),
                  icon: const Icon(Icons.arrow_downward),
                ),
                Expanded(
                  child: Column(
                    children: [
                      if (t != Transposition.concert)
                        Text('${t.label}の記譜', style: theme.textTheme.bodySmall),
                      Text(
                        noteLabel(
                          t == Transposition.concert
                              ? controller.concertMidi
                              : controller.writtenMidi,
                        ),
                        style: theme.textTheme.displayMedium,
                      ),
                      Text(
                        '実音 ${noteLabel(controller.concertMidi)}・${controller.frequency.toStringAsFixed(1)} Hz',
                        style: theme.textTheme.bodyMedium,
                      ),
                    ],
                  ),
                ),
                IconButton.outlined(
                  tooltip: '半音上げる',
                  onPressed: () =>
                      controller.selectConcert(controller.concertMidi + 1),
                  icon: const Icon(Icons.arrow_upward),
                ),
              ],
            ),
            const SizedBox(height: 12),
            Text('よく使う音（実音）', style: theme.textTheme.titleSmall),
            const SizedBox(height: 4),
            Wrap(
              spacing: 6,
              children: [
                for (final m in const [58, 65, 69, 70]) // B♭3・F4・A4・B♭4
                  ChoiceChip(
                    label: Text(noteLabel(m)),
                    selected: controller.concertMidi == m,
                    onSelected: (_) => controller.selectConcert(m),
                  ),
              ],
            ),
            const SizedBox(height: 16),
            FilledButton.icon(
              style: FilledButton.styleFrom(
                minimumSize: const Size.fromHeight(56),
              ),
              onPressed: controller.toggle,
              icon: Icon(controller.isPlaying ? Icons.stop : Icons.volume_up),
              label: Text(controller.isPlaying ? '止める' : '鳴らす'),
            ),
            if (controller.error != null) ...[
              const SizedBox(height: 8),
              Text(
                controller.error!,
                style: TextStyle(color: theme.colorScheme.error),
              ),
            ],
            const SizedBox(height: 8),
            Text(
              '音量に気をつけてください。イヤホンのときは小さめから。',
              style: theme.textTheme.bodySmall,
            ),
          ],
        );
      },
    );
  }
}

/// 基準ピッチ（A4）と楽器の調の設定。チューナーでも使う
class PitchSettingsPanel extends StatelessWidget {
  const PitchSettingsPanel({super.key, required this.controller});

  final ReferenceToneController controller;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return ListenableBuilder(
      listenable: controller,
      builder: (context, _) {
        final p = controller.pitch;
        return Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('基準ピッチ（A4）', style: theme.textTheme.titleSmall),
            Row(
              children: [
                IconButton(
                  onPressed: () =>
                      controller.updatePitch(p.copyWith(a4: p.a4 - 1)),
                  icon: const Icon(Icons.remove),
                ),
                Text(
                  '${p.a4.toStringAsFixed(0)} Hz',
                  style: theme.textTheme.titleLarge,
                ),
                IconButton(
                  onPressed: () =>
                      controller.updatePitch(p.copyWith(a4: p.a4 + 1)),
                  icon: const Icon(Icons.add),
                ),
                const Spacer(),
                for (final hz in const [440.0, 442.0])
                  Padding(
                    padding: const EdgeInsets.only(left: 6),
                    child: ChoiceChip(
                      label: Text(hz.toStringAsFixed(0)),
                      selected: p.a4 == hz,
                      onSelected: (_) =>
                          controller.updatePitch(p.copyWith(a4: hz)),
                    ),
                  ),
              ],
            ),
            const SizedBox(height: 8),
            Text('楽器の調（音名の表示）', style: theme.textTheme.titleSmall),
            const SizedBox(height: 4),
            SizedBox(
              width: double.infinity,
              child: SegmentedButton<Transposition>(
                segments: [
                  for (final t in Transposition.values)
                    ButtonSegment(value: t, label: Text(t.shortLabel)),
                ],
                selected: {p.transposition},
                showSelectedIcon: false,
                onSelectionChanged: (v) =>
                    controller.updatePitch(p.copyWith(transposition: v.single)),
              ),
            ),
            const SizedBox(height: 12),
            Text('音律', style: theme.textTheme.titleSmall),
            DropdownButton<Temperament>(
              isExpanded: true,
              value: p.temperament,
              items: [
                for (final t in Temperament.values)
                  DropdownMenuItem(value: t, child: Text(t.label)),
              ],
              onChanged: (t) => t == null
                  ? null
                  : controller.updatePitch(p.copyWith(temperament: t)),
            ),
            Text(p.temperament.description, style: theme.textTheme.bodySmall),
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
                            ? noteNames[pc]
                            : '${noteNames[pc]}（記譜${noteNames[p.transposition.concertToWritten(pc + 60) % 12]}）',
                      ),
                      selected: p.tonicPitchClass == pc,
                      onSelected: (_) => controller.updatePitch(
                        p.copyWith(tonicPitchClass: pc),
                      ),
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
