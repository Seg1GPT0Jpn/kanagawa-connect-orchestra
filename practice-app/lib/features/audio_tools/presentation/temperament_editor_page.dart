import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import '../../../app/app_services.dart';
import '../domain/temperament.dart';

/// 自分で作る音律の一覧（作る・複製・編集・削除・共有・取り込み）
class TemperamentListPage extends StatelessWidget {
  const TemperamentListPage({super.key});

  @override
  Widget build(BuildContext context) {
    final services = AppScope.of(context);
    final lib = services.temperaments;
    final theme = Theme.of(context);
    return Scaffold(
      appBar: AppBar(
        title: const Text('自分の音律'),
        actions: [
          IconButton(
            tooltip: '共有された音律を取り込む',
            onPressed: () => _import(context),
            icon: const Icon(Icons.download_outlined),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () => _create(context),
        icon: const Icon(Icons.add),
        label: const Text('新しく作る'),
      ),
      body: ListenableBuilder(
        listenable: lib,
        builder: (context, _) => ListView(
          padding: const EdgeInsets.fromLTRB(16, 16, 16, 96),
          children: [
            Text(
              '主音（調の音）から半音ごとに、平均律より何セント高く・低くするかを決めます。'
              'チューナーの目標と基準音の高さに使われます。',
              style: theme.textTheme.bodySmall,
            ),
            const SizedBox(height: 8),
            if (lib.items.isEmpty)
              const Padding(
                padding: EdgeInsets.symmetric(vertical: 24),
                child: Text('まだありません。「新しく作る」から、ひな形を選んで作れます。'),
              ),
            for (final t in lib.items)
              ListTile(
                contentPadding: EdgeInsets.zero,
                title: Text(t.name),
                subtitle: Text(
                  [
                    for (var i = 1; i < 12; i++)
                      if (t.offsets[i].abs() >= 0.05)
                        '${intervalNames[i]} ${t.offsets[i] >= 0 ? '+' : ''}${t.offsets[i].toStringAsFixed(1)}',
                  ].take(4).join('・'),
                ),
                onTap: () => Navigator.push(
                  context,
                  MaterialPageRoute<void>(
                    builder: (_) => TemperamentEditorPage(temperament: t),
                  ),
                ),
                trailing: PopupMenuButton<String>(
                  onSelected: (v) async {
                    final messenger = ScaffoldMessenger.of(context);
                    switch (v) {
                      case 'use':
                        final ref = services.referenceTone;
                        await ref.updatePitch(
                          ref.pitch.copyWith(
                            temperament: Temperament.custom,
                            custom: t,
                          ),
                        );
                        messenger.showSnackBar(
                          SnackBar(content: Text('「${t.name}」を使います')),
                        );
                      case 'copy':
                        await lib.duplicate(t);
                      case 'share':
                        await Clipboard.setData(
                          ClipboardData(text: lib.exportText(t)),
                        );
                        messenger.showSnackBar(
                          const SnackBar(
                            content: Text('共有用の文字をコピーしました。メッセージなどに貼り付けて送れます'),
                          ),
                        );
                      case 'delete':
                        await lib.delete(t.id);
                    }
                  },
                  itemBuilder: (_) => const [
                    PopupMenuItem(value: 'use', child: Text('この音律を使う')),
                    PopupMenuItem(value: 'copy', child: Text('複製')),
                    PopupMenuItem(value: 'share', child: Text('共有用にコピー')),
                    PopupMenuItem(value: 'delete', child: Text('削除')),
                  ],
                ),
              ),
          ],
        ),
      ),
    );
  }

  Future<void> _create(BuildContext context) async {
    final lib = AppScope.of(context).temperaments;
    final navigator = Navigator.of(context);
    final template = await showDialog<(String, List<double>)>(
      context: context,
      builder: (context) => SimpleDialog(
        title: const Text('ひな形を選ぶ'),
        children: [
          for (final t in temperamentTemplates)
            SimpleDialogOption(
              onPressed: () => Navigator.pop(context, t),
              child: Text(t.$1),
            ),
        ],
      ),
    );
    if (template == null) return;
    final created = await lib.create('${template.$1}（自分用）', template.$2);
    await navigator.push(
      MaterialPageRoute<void>(
        builder: (_) => TemperamentEditorPage(temperament: created),
      ),
    );
  }

  Future<void> _import(BuildContext context) async {
    final lib = AppScope.of(context).temperaments;
    final messenger = ScaffoldMessenger.of(context);
    final text = TextEditingController();
    final ok = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('共有された音律を取り込む'),
        content: TextField(
          controller: text,
          maxLines: 4,
          decoration: const InputDecoration(
            hintText: '共有された文字を貼り付けてください',
            border: OutlineInputBorder(),
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('やめる'),
          ),
          FilledButton(
            onPressed: () => Navigator.pop(context, true),
            child: const Text('取り込む'),
          ),
        ],
      ),
    );
    if (ok != true) return;
    final t = await lib.importText(text.text);
    messenger.showSnackBar(
      SnackBar(
        content: Text(
          t == null
              ? '読み取れませんでした。共有された文字をそのまま貼り付けてください'
              : '「${t.name}」を取り込みました',
        ),
      ),
    );
  }
}

/// 音律の編集（音ごとのずれ）
class TemperamentEditorPage extends StatefulWidget {
  const TemperamentEditorPage({super.key, required this.temperament});

  final CustomTemperament temperament;

  @override
  State<TemperamentEditorPage> createState() => _TemperamentEditorPageState();
}

class _TemperamentEditorPageState extends State<TemperamentEditorPage> {
  late final _name = TextEditingController(text: widget.temperament.name);
  late final List<double> _offsets = [...widget.temperament.offsets];

  @override
  void dispose() {
    _name.dispose();
    super.dispose();
  }

  Future<void> _save({bool use = false}) async {
    final services = AppScope.of(context);
    final navigator = Navigator.of(context);
    final t = widget.temperament.copyWith(
      name: _name.text.trim().isEmpty
          ? widget.temperament.name
          : _name.text.trim(),
      offsets: [..._offsets],
    );
    await services.temperaments.update(t);
    final ref = services.referenceTone;
    if (use || ref.pitch.custom?.id == t.id) {
      await ref.updatePitch(
        ref.pitch.copyWith(temperament: Temperament.custom, custom: t),
      );
    }
    navigator.pop();
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      appBar: AppBar(
        title: const Text('音律を編集'),
        actions: [TextButton(onPressed: _save, child: const Text('保存'))],
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          TextField(
            controller: _name,
            maxLength: 40,
            decoration: const InputDecoration(
              labelText: '名前',
              border: OutlineInputBorder(),
            ),
          ),
          Text(
            '主音は 0 に固定するのがふつうです。±${CustomTemperament.maxOffset.toStringAsFixed(0)} セントまで。',
            style: theme.textTheme.bodySmall,
          ),
          for (var i = 0; i < 12; i++)
            Row(
              children: [
                SizedBox(width: 72, child: Text(intervalNames[i])),
                Expanded(
                  child: Slider(
                    min: -CustomTemperament.maxOffset,
                    max: CustomTemperament.maxOffset,
                    divisions: 1000,
                    value: _offsets[i],
                    onChanged: (v) => setState(
                      () => _offsets[i] = double.parse(v.toStringAsFixed(1)),
                    ),
                  ),
                ),
                SizedBox(
                  width: 64,
                  child: Text(
                    '${_offsets[i] >= 0 ? '+' : ''}${_offsets[i].toStringAsFixed(1)}',
                    textAlign: TextAlign.end,
                  ),
                ),
              ],
            ),
          const SizedBox(height: 12),
          FilledButton(
            onPressed: () => _save(use: true),
            child: const Text('保存して、この音律を使う'),
          ),
        ],
      ),
    );
  }
}
