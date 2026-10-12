import 'package:flutter/material.dart';

import '../data/metronome_controller.dart';
import '../domain/metronome.dart';

/// メトロノームの画面
class MetronomeView extends StatelessWidget {
  const MetronomeView({
    super.key,
    required this.controller,
    required this.clock,
  });

  final MetronomeController controller;

  /// タップテンポ用の時刻（単調に増える）
  final Duration Function() clock;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return ListenableBuilder(
      listenable: controller,
      builder: (context, _) {
        final s = controller.settings;
        final beat = controller.currentBeat;
        return ListView(
          padding: const EdgeInsets.all(16),
          children: [
            // 拍の表示（今の拍が光る。1拍目は大きめ）
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                for (var i = 0; i < s.beatsPerBar; i++)
                  Padding(
                    padding: const EdgeInsets.all(4),
                    child: AnimatedContainer(
                      duration: const Duration(milliseconds: 60),
                      width: i == 0 && s.accentFirstBeat ? 22 : 16,
                      height: i == 0 && s.accentFirstBeat ? 22 : 16,
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        color: beat == i
                            ? theme.colorScheme.primary
                            : theme.colorScheme.surfaceContainerHighest,
                      ),
                    ),
                  ),
              ],
            ),
            const SizedBox(height: 16),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                IconButton.outlined(
                  tooltip: '5 遅く',
                  onPressed: () =>
                      controller.update(s.copyWith(bpm: s.bpm - 5)),
                  icon: const Text('-5'),
                ),
                IconButton(
                  tooltip: '1 遅く',
                  onPressed: () =>
                      controller.update(s.copyWith(bpm: s.bpm - 1)),
                  icon: const Icon(Icons.remove),
                ),
                SizedBox(
                  width: 120,
                  child: Text(
                    '${s.bpm}',
                    textAlign: TextAlign.center,
                    style: theme.textTheme.displayMedium?.copyWith(
                      fontFeatures: const [FontFeature.tabularFigures()],
                    ),
                  ),
                ),
                IconButton(
                  tooltip: '1 速く',
                  onPressed: () =>
                      controller.update(s.copyWith(bpm: s.bpm + 1)),
                  icon: const Icon(Icons.add),
                ),
                IconButton.outlined(
                  tooltip: '5 速く',
                  onPressed: () =>
                      controller.update(s.copyWith(bpm: s.bpm + 5)),
                  icon: const Text('+5'),
                ),
              ],
            ),
            Text(
              'BPM（1分間の拍数）',
              textAlign: TextAlign.center,
              style: theme.textTheme.bodySmall,
            ),
            Slider(
              value: s.bpm.toDouble(),
              min: MetronomeSettings.minBpm.toDouble(),
              max: MetronomeSettings.maxBpm.toDouble(),
              divisions: MetronomeSettings.maxBpm - MetronomeSettings.minBpm,
              label: '${s.bpm}',
              onChanged: (v) => controller.update(s.copyWith(bpm: v.round())),
            ),
            const SizedBox(height: 8),
            Text('拍子（1小節の拍数）', style: theme.textTheme.titleSmall),
            const SizedBox(height: 4),
            Wrap(
              spacing: 6,
              children: [
                for (final n in [1, 2, 3, 4, 5, 6, 7])
                  ChoiceChip(
                    label: Text(n == 1 ? 'なし' : '$n'),
                    selected: s.beatsPerBar == n,
                    onSelected: (_) =>
                        controller.update(s.copyWith(beatsPerBar: n)),
                  ),
              ],
            ),
            const SizedBox(height: 12),
            Text('細分', style: theme.textTheme.titleSmall),
            const SizedBox(height: 4),
            SizedBox(
              width: double.infinity,
              child: SegmentedButton<int>(
                segments: const [
                  ButtonSegment(value: 1, label: Text('なし')),
                  ButtonSegment(value: 2, label: Text('8分')),
                  ButtonSegment(value: 3, label: Text('3連')),
                  ButtonSegment(value: 4, label: Text('16分')),
                ],
                selected: {s.subdivision},
                showSelectedIcon: false,
                onSelectionChanged: (v) =>
                    controller.update(s.copyWith(subdivision: v.single)),
              ),
            ),
            SwitchListTile(
              contentPadding: EdgeInsets.zero,
              title: const Text('1拍目を強く'),
              value: s.accentFirstBeat,
              onChanged: (v) =>
                  controller.update(s.copyWith(accentFirstBeat: v)),
            ),
            const SizedBox(height: 8),
            Row(
              children: [
                Expanded(
                  child: FilledButton.icon(
                    style: FilledButton.styleFrom(
                      minimumSize: const Size.fromHeight(56),
                    ),
                    onPressed: controller.toggle,
                    icon: Icon(
                      controller.isRunning ? Icons.stop : Icons.play_arrow,
                    ),
                    label: Text(controller.isRunning ? '止める' : '鳴らす'),
                  ),
                ),
                const SizedBox(width: 12),
                OutlinedButton(
                  style: OutlinedButton.styleFrom(
                    minimumSize: const Size(96, 56),
                  ),
                  onPressed: () => controller.tap(clock()),
                  child: const Text('タップ'),
                ),
              ],
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
              '「タップ」を拍に合わせて数回押すと、そのテンポになります。',
              style: theme.textTheme.bodySmall,
            ),
          ],
        );
      },
    );
  }
}
