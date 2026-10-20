import 'package:flutter/material.dart';

import '../data/practice_menu_controller.dart';

/// 時間モード（通常・20分・10分）の切り替え
class ModeSelector extends StatelessWidget {
  const ModeSelector({super.key, required this.controller});

  final PracticeMenuController controller;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final rules = controller.rules;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('時間モード', style: theme.textTheme.titleMedium),
        const SizedBox(height: 8),
        SizedBox(
          width: double.infinity,
          child: SegmentedButton<String>(
            segments: [
              for (final m in controller.modes)
                ButtonSegment(value: m.id, label: Text(m.modeLabel)),
            ],
            selected: {rules.id},
            showSelectedIcon: false,
            onSelectionChanged: (s) => controller.selectMode(s.single),
          ),
        ),
        const SizedBox(height: 4),
        Text(rules.modeDescription, style: theme.textTheme.bodySmall),
      ],
    );
  }
}
