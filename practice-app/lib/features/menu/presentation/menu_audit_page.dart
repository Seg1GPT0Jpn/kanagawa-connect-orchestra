import 'package:flutter/material.dart';

import '../domain/menu_audit.dart';
import '../domain/menu_rules.dart';

/// メニューの時間を決めて、その場でルールを検査する画面
class MenuAuditPage extends StatefulWidget {
  const MenuAuditPage({
    super.key,
    required this.rules,
    this.initialMinutes,
    this.onSave,
  });

  final MenuRuleSet rules;

  /// 最初に表示するメニュー（null ならルールの初期値）
  final Map<String, int>? initialMinutes;

  /// ルールを満たすメニューを保存する（null なら保存ボタンを出さない）
  final Future<void> Function(Map<String, int> minutes)? onSave;

  @override
  State<MenuAuditPage> createState() => _MenuAuditPageState();
}

class _MenuAuditPageState extends State<MenuAuditPage> {
  /// スライダーの上限（ルールの上限を超えて動かせるようにして、警告を確かめられるようにする）
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
      messenger.showSnackBar(const SnackBar(content: Text('メニューを保存しました')));
    } catch (e) {
      messenger.showSnackBar(SnackBar(content: Text('保存できませんでした：$e')));
    } finally {
      if (mounted) setState(() => _saving = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final audit = auditMenu(_minutes, widget.rules);
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(title: Text(widget.rules.label)),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          for (final item in widget.rules.items)
            _MenuItemTile(
              item: item,
              minutes: _minutes[item.id]!,
              sliderMax: _sliderMax,
              onChanged: (v) =>
                  setState(() => _minutes = {..._minutes, item.id: v}),
            ),
          const Divider(height: 32),
          Text(
            '合計 ${audit.totalMinutes}分'
            '（${widget.rules.totalMinMinutes}〜${widget.rules.totalMaxMinutes}分）',
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
              onPressed: () => setState(
                () => _minutes = suggestCorrection(_minutes, widget.rules),
              ),
              icon: const Icon(Icons.auto_fix_high),
              label: const Text('ルールに合わせて直す'),
            ),
          ],
        ],
      ),
    );
  }
}

class _MenuItemTile extends StatelessWidget {
  const _MenuItemTile({
    required this.item,
    required this.minutes,
    required this.sliderMax,
    required this.onChanged,
  });

  final MenuItemRule item;
  final int minutes;
  final int sliderMax;
  final ValueChanged<int> onChanged;

  @override
  Widget build(BuildContext context) {
    final outOfRange = minutes < item.minMinutes || minutes > item.maxMinutes;
    final theme = Theme.of(context);
    return Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Expanded(
                child: Text(item.label, style: theme.textTheme.titleMedium),
              ),
              Text(
                '$minutes分',
                style: theme.textTheme.titleMedium?.copyWith(
                  color: outOfRange ? theme.colorScheme.error : null,
                ),
              ),
            ],
          ),
          Text(
            '${item.minMinutes}〜${item.maxMinutes}分',
            style: theme.textTheme.bodySmall,
          ),
          Slider(
            value: minutes.clamp(0, sliderMax).toDouble(),
            max: sliderMax.toDouble(),
            divisions: sliderMax,
            label: '$minutes分',
            semanticFormatterCallback: (v) => '${item.label} ${v.round()}分',
            onChanged: (v) => onChanged(v.round()),
          ),
        ],
      ),
    );
  }
}
