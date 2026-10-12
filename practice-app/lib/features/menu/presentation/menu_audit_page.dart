import 'package:flutter/material.dart';

import '../domain/menu_audit.dart';
import '../domain/menu_presets.dart';
import '../domain/menu_rules.dart';

/// メニューの時間を決めて、その場でルールを検査する画面
class MenuAuditPage extends StatefulWidget {
  const MenuAuditPage({
    super.key,
    required this.rules,
    this.initialMinutes,
    this.onSave,
    this.presets = const [],
  });

  final MenuRuleSet rules;

  /// 最初に表示するメニュー（null ならルールの初期値）
  final Map<String, int>? initialMinutes;

  /// ルールを満たすメニューを保存する（null なら保存ボタンを出さない）
  final Future<void> Function(Map<String, int> minutes)? onSave;

  /// 「今日の重点」のおすすめ（空なら出さない）
  final List<MenuPreset> presets;

  @override
  State<MenuAuditPage> createState() => _MenuAuditPageState();
}

class _MenuAuditPageState extends State<MenuAuditPage> {
  /// 単独の項目のスライダーの上限（ルールの上限を超えて動かせるようにして、警告を確かめられるようにする）
  static const _sliderMax = 60;

  late Map<String, int> _minutes = {
    ...(widget.initialMinutes ?? widget.rules.defaultMenu),
  };
  bool _saving = false;

  bool get _changed {
    final initial = widget.initialMinutes ?? widget.rules.defaultMenu;
    return widget.rules.items.any((i) => initial[i.id] != _minutes[i.id]);
  }

  Future<void> _save() async {
    setState(() => _saving = true);
    final messenger = ScaffoldMessenger.of(context);
    try {
      await widget.onSave!(_minutes);
      messenger
        ..removeCurrentSnackBar()
        ..showSnackBar(const SnackBar(content: Text('メニューを保存しました')));
    } catch (e) {
      messenger
        ..removeCurrentSnackBar()
        ..showSnackBar(SnackBar(content: Text('保存できませんでした：$e')));
    } finally {
      if (mounted) setState(() => _saving = false);
    }
  }

  void _set(String id, int v) =>
      setState(() => _minutes = {..._minutes, id: v});

  @override
  Widget build(BuildContext context) {
    final rules = widget.rules;
    final audit = auditMenu(_minutes, rules);
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(title: Text(rules.label)),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          if (widget.presets.isNotEmpty) ...[
            Text('今日の重点（おすすめ）', style: theme.textTheme.titleMedium),
            const SizedBox(height: 8),
            Wrap(
              spacing: 8,
              runSpacing: 4,
              children: [
                for (final p in widget.presets)
                  ActionChip(
                    label: Text(p.label),
                    tooltip: p.description,
                    onPressed: () {
                      setState(
                        () =>
                            _minutes = p.menuFor(rules.items.map((i) => i.id)),
                      );
                      ScaffoldMessenger.of(context)
                        ..removeCurrentSnackBar()
                        ..showSnackBar(
                          SnackBar(
                            content: Text('${p.label}：${p.description}'),
                          ),
                        );
                    },
                  ),
              ],
            ),
            const Divider(height: 32),
          ],
          for (final item in rules.items.where((i) => i.group == null))
            _MenuItemTile(
              label: item.label,
              item: item,
              minutes: _minutes[item.id] ?? 0,
              sliderMax: _sliderMax,
              onChanged: (v) => _set(item.id, v),
            ),
          for (final g in rules.groups) ...[
            const Divider(height: 32),
            _GroupHeader(
              group: g,
              sum: rules
                  .itemsInGroup(g.id)
                  .fold(0, (s, i) => s + (_minutes[i.id] ?? 0)),
            ),
            for (final item in rules.itemsInGroup(g.id))
              _MenuItemTile(
                label: item.label,
                item: item,
                minutes: _minutes[item.id] ?? 0,
                sliderMax: g.maxMinutes,
                compact: true,
                onChanged: (v) => _set(item.id, v),
              ),
          ],
          const Divider(height: 32),
          Text(
            '合計 ${audit.totalMinutes}分'
            '（${rules.totalMinMinutes}〜${rules.totalMaxMinutes}分）',
            style: theme.textTheme.titleLarge,
          ),
          const SizedBox(height: 12),
          if (audit.isValid) ...[
            Card(
              color: theme.colorScheme.primaryContainer,
              child: const ListTile(
                leading: Icon(Icons.check_circle_outline),
                title: Text('ルールを満たしています'),
              ),
            ),
            if (widget.onSave != null && _changed) ...[
              const SizedBox(height: 12),
              FilledButton.icon(
                onPressed: _saving ? null : _save,
                icon: const Icon(Icons.save_outlined),
                label: const Text('このメニューを保存'),
              ),
            ],
          ] else ...[
            Card(
              color: theme.colorScheme.errorContainer,
              child: Column(
                children: [
                  for (final v in audit.violations)
                    ListTile(
                      leading: const Icon(Icons.warning_amber_outlined),
                      title: Text(v.message),
                    ),
                ],
              ),
            ),
            const SizedBox(height: 12),
            FilledButton.icon(
              onPressed: () =>
                  setState(() => _minutes = suggestCorrection(_minutes, rules)),
              icon: const Icon(Icons.auto_fix_high),
              label: const Text('ルールに合わせて直す'),
            ),
          ],
          const SizedBox(height: 16),
          Text(
            '疲れや痛みが出たら、時間を埋めるために吹き続けなくて大丈夫です。'
            '高音・大音量など負荷の高い練習は、指導者と相談しながら調整してください。',
            style: theme.textTheme.bodySmall,
          ),
        ],
      ),
    );
  }
}

class _GroupHeader extends StatelessWidget {
  const _GroupHeader({required this.group, required this.sum});

  final MenuGroupRule group;
  final int sum;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final outOfRange = sum < group.minMinutes || sum > group.maxMinutes;
    return Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Expanded(
                child: Text(group.label, style: theme.textTheme.titleLarge),
              ),
              Text(
                '合計 $sum分',
                style: theme.textTheme.titleMedium?.copyWith(
                  color: outOfRange ? theme.colorScheme.error : null,
                ),
              ),
            ],
          ),
          Text(
            '${group.minMinutes}〜${group.maxMinutes}分・${group.description}',
            style: theme.textTheme.bodySmall,
          ),
        ],
      ),
    );
  }
}

class _MenuItemTile extends StatelessWidget {
  const _MenuItemTile({
    required this.label,
    required this.item,
    required this.minutes,
    required this.sliderMax,
    required this.onChanged,
    this.compact = false,
  });

  final String label;
  final MenuItemRule item;
  final int minutes;
  final int sliderMax;
  final ValueChanged<int> onChanged;

  /// グループの中の項目（範囲は書かず、0分は「お休み」）
  final bool compact;

  @override
  Widget build(BuildContext context) {
    final outOfRange = minutes < item.minMinutes || minutes > item.maxMinutes;
    final theme = Theme.of(context);
    final resting = compact && minutes == 0;
    return Padding(
      padding: const EdgeInsets.only(bottom: 4),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Expanded(
                child: Text(
                  label,
                  style:
                      (compact
                              ? theme.textTheme.titleSmall
                              : theme.textTheme.titleMedium)
                          ?.copyWith(
                            color: resting ? theme.disabledColor : null,
                          ),
                ),
              ),
              Text(
                resting ? 'お休み' : '$minutes分',
                style: theme.textTheme.titleMedium?.copyWith(
                  color: outOfRange
                      ? theme.colorScheme.error
                      : resting
                      ? theme.disabledColor
                      : null,
                ),
              ),
            ],
          ),
          Text(
            [
              if (!compact) '${item.minMinutes}〜${item.maxMinutes}分',
              if (item.description.isNotEmpty) item.description,
            ].join('・'),
            style: theme.textTheme.bodySmall,
          ),
          Slider(
            value: minutes.clamp(0, sliderMax).toDouble(),
            max: sliderMax.toDouble(),
            divisions: sliderMax,
            label: '$minutes分',
            semanticFormatterCallback: (v) => '$label ${v.round()}分',
            onChanged: (v) => onChanged(v.round()),
          ),
        ],
      ),
    );
  }
}
