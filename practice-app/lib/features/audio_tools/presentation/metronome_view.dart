import 'dart:math' as math;

import 'package:flutter/material.dart';

import '../../../app/app_services.dart';
import '../data/metronome_controller.dart';
import '../data/metronome_presets.dart';
import '../domain/metronome.dart';
import '../domain/metronome_plan.dart';
import '../domain/sound.dart';

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
        final o = controller.options;
        void setO(MetronomeOptions n) => controller.updateOptions(n);
        return ListView(
          padding: const EdgeInsets.all(16),
          children: [
            BeatVisual(controller: controller),
            const SizedBox(height: 8),
            if (controller.isRunning &&
                (o.rampEnabled || o.timerMinutes > 0 || o.countInBars > 0))
              Text(
                [
                  if ((controller.currentBar ?? 0) < 0) 'カウントイン',
                  if (o.rampEnabled) 'いまのテンポ ${controller.currentBpm}',
                  if (controller.currentBar case final b? when b >= 0)
                    '${b + 1}小節目',
                  if (controller.timeLeft case final t?)
                    '残り ${t.inMinutes}:${(t.inSeconds % 60).toString().padLeft(2, '0')}',
                ].join('・'),
                textAlign: TextAlign.center,
                style: theme.textTheme.titleSmall,
              ),
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
              o.rampEnabled
                  ? 'BPM（開始のテンポ。${o.rampTargetBpm} まで変えていく）'
                  : 'BPM（1分間の拍数）',
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
            if (controller.stoppedReason != null) ...[
              const SizedBox(height: 8),
              Text(controller.stoppedReason!, textAlign: TextAlign.center),
            ],
            const SizedBox(height: 12),
            Text('拍子（1小節の拍数）', style: theme.textTheme.titleSmall),
            const SizedBox(height: 4),
            Wrap(
              spacing: 6,
              children: [
                for (final n in [1, 2, 3, 4, 5, 6, 7, 9, 12])
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
            const SizedBox(height: 12),
            Text('拍ごとの鳴らし方（押すと 強→ふつう→休み）', style: theme.textTheme.titleSmall),
            const SizedBox(height: 4),
            Wrap(
              spacing: 4,
              runSpacing: 4,
              children: [
                for (final (i, a)
                    in o
                        .patternFor(
                          s.beatsPerBar,
                          accentFirst: s.accentFirstBeat,
                        )
                        .indexed)
                  ActionChip(
                    avatar: Text('${i + 1}'),
                    label: Text(a.label),
                    backgroundColor: switch (a) {
                      BeatAccent.accent => theme.colorScheme.primaryContainer,
                      BeatAccent.normal => null,
                      BeatAccent.mute =>
                        theme.colorScheme.surfaceContainerHighest,
                    },
                    onPressed: () {
                      final p = [
                        ...o.patternFor(
                          s.beatsPerBar,
                          accentFirst: s.accentFirstBeat,
                        ),
                      ];
                      p[i] = p[i].next;
                      setO(o.copyWith(pattern: p));
                    },
                  ),
                if (o.pattern.isNotEmpty)
                  TextButton(
                    onPressed: () => setO(o.copyWith(pattern: const [])),
                    child: const Text('元に戻す'),
                  ),
              ],
            ),
            const SizedBox(height: 8),
            Row(
              children: [
                const Text('音色'),
                const SizedBox(width: 12),
                Expanded(
                  child: DropdownButton<ClickSound>(
                    isExpanded: true,
                    value: o.sound,
                    items: [
                      for (final c in ClickSound.values)
                        DropdownMenuItem(value: c, child: Text(c.label)),
                    ],
                    onChanged: (v) => setO(o.copyWith(sound: v)),
                  ),
                ),
              ],
            ),
            Row(
              children: [
                const Text('音量'),
                Expanded(
                  child: Slider(
                    value: o.volume,
                    onChanged: (v) => setO(o.copyWith(volume: v)),
                  ),
                ),
              ],
            ),
            Row(
              children: [
                const Text('拍の見せ方'),
                const SizedBox(width: 12),
                Expanded(
                  child: SegmentedButton<MetronomeVisual>(
                    segments: [
                      for (final v in MetronomeVisual.values)
                        ButtonSegment(value: v, label: Text(v.label)),
                    ],
                    selected: {o.visual},
                    showSelectedIcon: false,
                    onSelectionChanged: (v) =>
                        setO(o.copyWith(visual: v.single)),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 8),
            _PracticeOptions(controller: controller),
            const Divider(height: 24),
            _Presets(controller: controller),
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

/// 拍の表示（拍の丸・振り子・画面の点滅）
class BeatVisual extends StatelessWidget {
  const BeatVisual({super.key, required this.controller});

  final MetronomeController controller;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final s = controller.settings;
    final beat = controller.currentBeat;
    final muted = controller.currentBeatMuted;
    final countIn = (controller.currentBar ?? 0) < 0;
    final active = muted
        ? theme.colorScheme.outline
        : countIn
        ? theme.colorScheme.tertiary
        : theme.colorScheme.primary;
    final dots = Row(
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
                    ? active
                    : theme.colorScheme.surfaceContainerHighest,
              ),
            ),
          ),
      ],
    );
    switch (controller.options.visual) {
      case MetronomeVisual.dots:
        return dots;
      case MetronomeVisual.pendulum:
        // 拍ごとに左右へ振れる（拍の瞬間に端に来る）
        final p = controller.beatProgress;
        final dir = controller.beatCount.isEven ? 1.0 : -1.0;
        final angle = controller.isRunning
            ? dir * math.cos(p * math.pi) * 0.5
            : 0.0;
        return Column(
          children: [
            SizedBox(
              height: 110,
              child: Transform.rotate(
                angle: angle,
                alignment: Alignment.bottomCenter,
                child: Align(
                  alignment: Alignment.bottomCenter,
                  child: Container(
                    width: 6,
                    height: 100,
                    decoration: BoxDecoration(
                      color: active,
                      borderRadius: BorderRadius.circular(3),
                    ),
                  ),
                ),
              ),
            ),
            dots,
          ],
        );
      case MetronomeVisual.flash:
        // 拍の頭で光り、すぐ消える（強拍はより強く）
        final p = controller.beatProgress;
        final on = controller.isRunning && beat != null && p < 0.25 && !muted;
        return AnimatedContainer(
          duration: const Duration(milliseconds: 40),
          height: 110,
          decoration: BoxDecoration(
            color: on
                ? active.withValues(
                    alpha: controller.currentBeatAccent ? 0.9 : 0.5,
                  )
                : theme.colorScheme.surfaceContainerHighest,
            borderRadius: BorderRadius.circular(12),
          ),
          alignment: Alignment.center,
          child: Text(
            beat == null ? '' : '${beat + 1}',
            style: theme.textTheme.displaySmall,
          ),
        );
    }
  }
}

/// 練習の工夫（消音・テンポの段階変化・カウントイン・ポリリズム・タイマー）
class _PracticeOptions extends StatelessWidget {
  const _PracticeOptions({required this.controller});

  final MetronomeController controller;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final o = controller.options;
    void setO(MetronomeOptions n) => controller.updateOptions(n);
    Widget counter(
      String label,
      int value,
      int min,
      int max,
      void Function(int) on,
    ) => Row(
      children: [
        Expanded(child: Text(label)),
        IconButton(
          onPressed: value > min ? () => on(value - 1) : null,
          icon: const Icon(Icons.remove),
        ),
        SizedBox(width: 32, child: Text('$value', textAlign: TextAlign.center)),
        IconButton(
          onPressed: value < max ? () => on(value + 1) : null,
          icon: const Icon(Icons.add),
        ),
      ],
    );
    return ExpansionTile(
      tilePadding: EdgeInsets.zero,
      title: const Text('練習の工夫（消音・テンポ変化・カウントイン・ポリリズム・タイマー）'),
      childrenPadding: const EdgeInsets.only(bottom: 8),
      expandedCrossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'ランダムに休む拍：${o.randomMutePercent}%',
          style: theme.textTheme.titleSmall,
        ),
        Slider(
          value: o.randomMutePercent.toDouble(),
          max: 80,
          divisions: 16,
          label: '${o.randomMutePercent}%',
          onChanged: (v) => setO(o.copyWith(randomMutePercent: v.round())),
        ),
        Text('休んだ拍も、内側で拍を感じて吹き続ける練習です', style: theme.textTheme.bodySmall),
        const SizedBox(height: 8),
        SwitchListTile(
          contentPadding: EdgeInsets.zero,
          title: const Text('小節ごとに鳴らす・休む'),
          value: o.muteBars > 0,
          onChanged: (v) => setO(o.copyWith(muteBars: v ? 2 : 0)),
        ),
        if (o.muteBars > 0) ...[
          counter(
            '鳴らす小節',
            o.playBars,
            1,
            16,
            (v) => setO(o.copyWith(playBars: v)),
          ),
          counter(
            '休む小節',
            o.muteBars,
            1,
            16,
            (v) => setO(o.copyWith(muteBars: v)),
          ),
        ],
        SwitchListTile(
          contentPadding: EdgeInsets.zero,
          title: const Text('テンポを段階的に変える'),
          subtitle: const Text('いまの BPM から、目標のテンポまで少しずつ'),
          value: o.rampEnabled,
          onChanged: (v) => setO(o.copyWith(rampEnabled: v)),
        ),
        if (o.rampEnabled) ...[
          counter(
            '目標のテンポ',
            o.rampTargetBpm,
            MetronomeSettings.minBpm,
            MetronomeSettings.maxBpm,
            (v) => setO(o.copyWith(rampTargetBpm: v)),
          ),
          counter(
            '1回に変える量（BPM）',
            o.rampStepBpm,
            1,
            40,
            (v) => setO(o.copyWith(rampStepBpm: v)),
          ),
          counter(
            '何小節ごとに',
            o.rampEveryBars,
            1,
            32,
            (v) => setO(o.copyWith(rampEveryBars: v)),
          ),
          SwitchListTile(
            contentPadding: EdgeInsets.zero,
            title: const Text('目標に着いたら止める'),
            value: o.rampStopAtTarget,
            onChanged: (v) => setO(o.copyWith(rampStopAtTarget: v)),
          ),
        ],
        Text('カウントイン（始める前の数え）', style: theme.textTheme.titleSmall),
        Wrap(
          spacing: 6,
          children: [
            for (final n in [0, 1, 2])
              ChoiceChip(
                label: Text(n == 0 ? 'なし' : '$n小節'),
                selected: o.countInBars == n,
                onSelected: (_) => setO(o.copyWith(countInBars: n)),
              ),
          ],
        ),
        const SizedBox(height: 8),
        Text('ポリリズム（1小節をこの数で等分して、別の音で鳴らす）', style: theme.textTheme.titleSmall),
        Wrap(
          spacing: 6,
          children: [
            for (final n in [0, 2, 3, 4, 5, 6, 7])
              ChoiceChip(
                label: Text(n == 0 ? 'なし' : '$n'),
                selected: o.polyrhythm == n,
                onSelected: (_) => setO(o.copyWith(polyrhythm: n)),
              ),
          ],
        ),
        Text('例：4拍子で「3」なら 3対4。拍子と同じ数は鳴らしません', style: theme.textTheme.bodySmall),
        const SizedBox(height: 8),
        Text('練習タイマー（時間が来たら止める）', style: theme.textTheme.titleSmall),
        Wrap(
          spacing: 6,
          children: [
            for (final n in [0, 5, 10, 15, 20, 30])
              ChoiceChip(
                label: Text(n == 0 ? 'なし' : '$n分'),
                selected: o.timerMinutes == n,
                onSelected: (_) => setO(o.copyWith(timerMinutes: n)),
              ),
          ],
        ),
      ],
    );
  }
}

/// プリセット（保存・呼び出し・グループを順に鳴らす）
class _Presets extends StatelessWidget {
  const _Presets({required this.controller});

  final MetronomeController controller;

  @override
  Widget build(BuildContext context) {
    final services = AppScope.of(context);
    final lib = services.metronomePresets;
    final theme = Theme.of(context);
    return ListenableBuilder(
      listenable: lib,
      builder: (context, _) {
        final groups = ['', ...lib.groups];
        return Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Row(
              children: [
                Expanded(
                  child: Text('プリセット', style: theme.textTheme.titleMedium),
                ),
                TextButton.icon(
                  onPressed: () => _save(context, lib),
                  icon: const Icon(Icons.bookmark_add_outlined),
                  label: const Text('いまの設定を保存'),
                ),
              ],
            ),
            if (lib.items.isEmpty)
              Text(
                'テンポ・拍子・音色などをまとめて保存し、すぐに呼び出せます',
                style: theme.textTheme.bodySmall,
              ),
            for (final g in groups)
              if (lib.items.any((p) => p.group == g)) ...[
                if (g.isNotEmpty)
                  Row(
                    children: [
                      Expanded(
                        child: Text(
                          'グループ：$g',
                          style: theme.textTheme.titleSmall,
                        ),
                      ),
                      TextButton(
                        onPressed: () => _playGroup(context, g),
                        child: const Text('順に鳴らす'),
                      ),
                    ],
                  ),
                for (final p in lib.items.where((p) => p.group == g))
                  ListTile(
                    dense: true,
                    contentPadding: EdgeInsets.zero,
                    title: Text(p.name),
                    subtitle: Text(
                      '${p.settings.bpm} BPM・${p.settings.beatsPerBar}拍子・${p.options.sound.label}',
                    ),
                    onTap: () async {
                      await controller.update(p.settings);
                      await controller.updateOptions(p.options);
                    },
                    trailing: IconButton(
                      tooltip: '削除',
                      icon: const Icon(Icons.delete_outline),
                      onPressed: () => lib.delete(p.id),
                    ),
                  ),
              ],
          ],
        );
      },
    );
  }

  Future<void> _save(BuildContext context, MetronomePresetLibrary lib) async {
    final name = TextEditingController(text: '${controller.settings.bpm} BPM');
    final group = TextEditingController();
    final ok = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('プリセットを保存'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(
              controller: name,
              decoration: const InputDecoration(labelText: '名前'),
            ),
            TextField(
              controller: group,
              decoration: const InputDecoration(labelText: 'グループ（曲名など。なくてもよい）'),
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('やめる'),
          ),
          FilledButton(
            onPressed: () => Navigator.pop(context, true),
            child: const Text('保存'),
          ),
        ],
      ),
    );
    if (ok != true) return;
    await lib.save(
      name.text,
      controller.settings,
      controller.options,
      group: group.text,
    );
  }

  Future<void> _playGroup(BuildContext context, String group) async {
    final services = AppScope.of(context);
    final messenger = ScaffoldMessenger.of(context);
    final presets = [
      for (final p in services.metronomePresets.items)
        if (p.group == group) p,
    ];
    await services.clickTrack.addPrepared(
      presetsToClickTrack('$group（プリセット）', presets),
    );
    messenger.showSnackBar(
      SnackBar(
        content: Text(
          '「$group」のプリセットを順に鳴らすクリックトラックを作りました（各8小節）。クリックトラックのタブで鳴らせます',
        ),
      ),
    );
  }
}
