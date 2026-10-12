import 'package:flutter/material.dart';

import '../data/click_track_controller.dart';
import '../domain/click_track.dart';

/// クリックトラック（テンポ・拍子が変わる曲用）の編集と再生
class ClickTrackView extends StatelessWidget {
  const ClickTrackView({super.key, required this.controller});

  final ClickTrackController controller;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return ListenableBuilder(
      listenable: controller,
      builder: (context, _) {
        final c = controller;
        final t = c.track;
        final pos = c.position;
        return ListView(
          padding: const EdgeInsets.all(16),
          children: [
            Row(
              children: [
                Expanded(
                  child: DropdownButton<int>(
                    isExpanded: true,
                    value: c.selectedIndex,
                    items: [
                      for (final (i, x) in c.tracks.indexed)
                        DropdownMenuItem(value: i, child: Text(x.name)),
                    ],
                    onChanged: (i) => i == null ? null : c.select(i),
                  ),
                ),
                IconButton(
                  tooltip: '新しく作る',
                  onPressed: c.addTrack,
                  icon: const Icon(Icons.add),
                ),
                IconButton(
                  tooltip: '名前を変える',
                  onPressed: () => _rename(context, t),
                  icon: const Icon(Icons.edit_outlined),
                ),
                IconButton(
                  tooltip: '削除',
                  onPressed: c.deleteTrack,
                  icon: const Icon(Icons.delete_outline),
                ),
              ],
            ),
            const SizedBox(height: 8),
            Row(
              children: [
                Text('予備拍', style: theme.textTheme.titleSmall),
                const SizedBox(width: 12),
                for (final n in const [0, 1, 2])
                  Padding(
                    padding: const EdgeInsets.only(right: 6),
                    child: ChoiceChip(
                      label: Text(n == 0 ? 'なし' : '$n小節'),
                      selected: t.countInBars == n,
                      onSelected: (_) =>
                          c.updateTrack(t.copyWith(countInBars: n)),
                    ),
                  ),
              ],
            ),
            const SizedBox(height: 8),
            for (final (i, s) in t.sections.indexed)
              _SectionCard(
                index: i,
                section: s,
                active: pos != null && pos.section == i,
                canDelete: t.sections.length > 1,
                onChanged: (v) => c.updateTrack(
                  t.copyWith(sections: [...t.sections]..[i] = v),
                ),
                onDelete: () => c.updateTrack(
                  t.copyWith(sections: [...t.sections]..removeAt(i)),
                ),
              ),
            TextButton.icon(
              onPressed: () => c.updateTrack(
                t.copyWith(sections: [...t.sections, t.sections.last]),
              ),
              icon: const Icon(Icons.add),
              label: const Text('区間を足す'),
            ),
            const Divider(height: 24),
            Text(
              pos == null
                  ? '全 ${t.totalBars} 小節'
                  : pos.bar <= 0
                  ? '予備拍 ${pos.beatInBar + 1}'
                  : '小節 ${pos.bar} / ${t.totalBars}・${pos.beatInBar + 1} 拍目（区間 ${pos.section + 1}）',
              textAlign: TextAlign.center,
              style: theme.textTheme.titleLarge,
            ),
            const SizedBox(height: 12),
            FilledButton.icon(
              style: FilledButton.styleFrom(
                minimumSize: const Size.fromHeight(56),
              ),
              onPressed: c.isPlaying ? c.stop : c.play,
              icon: Icon(c.isPlaying ? Icons.stop : Icons.play_arrow),
              label: Text(c.isPlaying ? '止める' : '最初から鳴らす'),
            ),
            if (c.error != null) ...[
              const SizedBox(height: 8),
              Text(c.error!, style: TextStyle(color: theme.colorScheme.error)),
            ],
          ],
        );
      },
    );
  }

  Future<void> _rename(BuildContext context, ClickTrack t) async {
    final text = TextEditingController(text: t.name);
    final name = await showDialog<String>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('名前'),
        content: TextField(controller: text, autofocus: true, maxLength: 40),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('やめる'),
          ),
          FilledButton(
            onPressed: () => Navigator.pop(context, text.text.trim()),
            child: const Text('決定'),
          ),
        ],
      ),
    );
    if (name != null && name.isNotEmpty) {
      await controller.updateTrack(t.copyWith(name: name));
    }
  }
}

class _SectionCard extends StatelessWidget {
  const _SectionCard({
    required this.index,
    required this.section,
    required this.active,
    required this.canDelete,
    required this.onChanged,
    required this.onDelete,
  });

  final int index;
  final ClickSection section;
  final bool active;
  final bool canDelete;
  final ValueChanged<ClickSection> onChanged;
  final VoidCallback onDelete;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final s = section;
    Widget stepper(
      String label,
      int value,
      int step,
      ClickSection Function(int) apply,
    ) => Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Text(label),
        IconButton(
          visualDensity: VisualDensity.compact,
          onPressed: () => onChanged(apply(value - step)),
          icon: const Icon(Icons.remove),
        ),
        Text('$value', style: theme.textTheme.titleMedium),
        IconButton(
          visualDensity: VisualDensity.compact,
          onPressed: () => onChanged(apply(value + step)),
          icon: const Icon(Icons.add),
        ),
      ],
    );
    return Card(
      color: active ? theme.colorScheme.primaryContainer : null,
      child: Padding(
        padding: const EdgeInsets.fromLTRB(12, 8, 4, 8),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Text('区間 ${index + 1}', style: theme.textTheme.titleSmall),
                const Spacer(),
                if (canDelete)
                  IconButton(
                    tooltip: 'この区間を消す',
                    onPressed: onDelete,
                    icon: const Icon(Icons.close),
                  ),
              ],
            ),
            Wrap(
              spacing: 8,
              children: [
                stepper('小節', s.bars, 1, (v) => s.copyWith(bars: v)),
                stepper('♩=', s.bpm, 1, (v) => s.copyWith(bpm: v)),
                stepper(
                  '拍子',
                  s.beatsPerBar,
                  1,
                  (v) => s.copyWith(beatsPerBar: v),
                ),
              ],
            ),
            Wrap(
              spacing: 6,
              children: [
                for (final (sub, label) in const [
                  (1, '細分なし'),
                  (2, '8分'),
                  (3, '3連'),
                  (4, '16分'),
                ])
                  ChoiceChip(
                    label: Text(label),
                    selected: s.subdivision == sub,
                    onSelected: (_) => onChanged(s.copyWith(subdivision: sub)),
                  ),
              ],
            ),
            Text(
              '${(s.durationMicros / 1000000).toStringAsFixed(1)} 秒',
              style: theme.textTheme.bodySmall,
            ),
          ],
        ),
      ),
    );
  }
}
