import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

import '../data/mixer_controller.dart';
import '../domain/sound.dart';

/// 音の設定（系統ごとの音量）と、音が出ないときの確認
class SoundSettingsSheet extends StatelessWidget {
  const SoundSettingsSheet({super.key, required this.controller});

  final MixerController controller;

  static Future<void> show(BuildContext context, MixerController controller) =>
      showModalBottomSheet<void>(
        context: context,
        isScrollControlled: true,
        showDragHandle: true,
        builder: (_) => SoundSettingsSheet(controller: controller),
      );

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return ListenableBuilder(
      listenable: controller,
      builder: (context, _) => SafeArea(
        child: ListView(
          shrinkWrap: true,
          padding: const EdgeInsets.fromLTRB(16, 0, 16, 16),
          children: [
            Text('音の設定・テスト', style: theme.textTheme.titleLarge),
            const SizedBox(height: 12),
            FilledButton.icon(
              onPressed: controller.isTesting ? null : controller.playTest,
              icon: const Icon(Icons.volume_up),
              label: const Text('テスト音を鳴らす'),
            ),
            if (controller.testResult != null)
              Padding(
                padding: const EdgeInsets.only(top: 8),
                child: Text(controller.testResult!),
              ),
            const SizedBox(height: 16),
            Text('音量（ミキサー）', style: theme.textTheme.titleMedium),
            for (final ch in AudioChannel.values)
              Row(
                children: [
                  SizedBox(width: 150, child: Text(ch.label)),
                  Expanded(
                    child: Slider(
                      value: controller.volumeOf(ch),
                      divisions: 20,
                      label: '${(controller.volumeOf(ch) * 100).round()}%',
                      onChanged: (v) => controller.setVolume(ch, v),
                    ),
                  ),
                ],
              ),
            const SizedBox(height: 8),
            Text('音が出ないときは', style: theme.textTheme.titleMedium),
            const SizedBox(height: 4),
            for (final tip in _tips)
              Padding(
                padding: const EdgeInsets.only(bottom: 4),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text('・'),
                    Expanded(child: Text(tip)),
                  ],
                ),
              ),
          ],
        ),
      ),
    );
  }

  static List<String> get _tips => [
    '端末の音量（メディアの音量）が上がっているか',
    'iPhone の消音スイッチ（マナーモード）が入っていないか',
    'Bluetooth のイヤホン・スピーカーにつながったままになっていないか',
    'ほかのアプリが音やマイクを使っていないか',
    if (kIsWeb) ...[
      'ブラウザのタブがミュートになっていないか',
      '画面を一度タップしてから、もう一度鳴らす（ブラウザは、タップしないと音を出さない決まりがあります）',
    ],
  ];
}
