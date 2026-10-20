import 'package:flutter/foundation.dart';

import '../../../core/ids.dart';
import '../../../core/meta_store.dart';
import '../domain/click_track.dart';
import '../domain/metronome.dart';
import '../domain/metronome_plan.dart';

/// メトロノームのプリセット（テンポ・拍子・細分・音色・パターンなどをまとめて保存）
class MetronomePreset {
  const MetronomePreset({
    required this.id,
    required this.name,
    required this.settings,
    required this.options,
    this.group = '',
  });

  final String id;
  final String name;

  /// まとめて管理するグループ（曲名など。空ならグループなし）
  final String group;
  final MetronomeSettings settings;
  final MetronomeOptions options;

  Map<String, Object?> toMap() => {
    'id': id,
    'name': name,
    'group': group,
    'settings': settings.toMap(),
    'options': options.toMap(),
  };

  static MetronomePreset? fromMap(Object? m) {
    if (m is! Map || m['id'] is! String || m['name'] is! String) return null;
    final s = m['settings'], o = m['options'];
    return MetronomePreset(
      id: m['id']! as String,
      name: m['name']! as String,
      group: m['group'] is String ? m['group']! as String : '',
      settings: s is Map
          ? MetronomeSettings.fromMap(s)
          : const MetronomeSettings(),
      options: o is Map
          ? MetronomeOptions.fromMap(o)
          : const MetronomeOptions(),
    );
  }
}

class MetronomePresetLibrary extends ChangeNotifier {
  MetronomePresetLibrary(this._meta, this._items);

  static Future<MetronomePresetLibrary> load(MetaStore meta) async {
    final raw = await meta.get('metronome.presets');
    return MetronomePresetLibrary(meta, [
      if (raw is List)
        for (final r in raw) ?MetronomePreset.fromMap(r),
    ]);
  }

  final MetaStore _meta;
  final List<MetronomePreset> _items;
  static const maxItems = 100;

  List<MetronomePreset> get items => List.unmodifiable(_items);

  /// グループの名前（空のグループは除く）
  List<String> get groups => {
    for (final p in _items)
      if (p.group.isNotEmpty) p.group,
  }.toList();

  Future<MetronomePreset> save(
    String name,
    MetronomeSettings settings,
    MetronomeOptions options, {
    String group = '',
  }) async {
    final p = MetronomePreset(
      id: generateId(),
      name: name.trim().isEmpty ? '${settings.bpm} BPM' : name.trim(),
      group: group.trim(),
      settings: settings,
      options: options,
    );
    _items.add(p);
    if (_items.length > maxItems) _items.removeAt(0);
    await _persist();
    return p;
  }

  Future<void> delete(String id) async {
    _items.removeWhere((p) => p.id == id);
    await _persist();
  }

  /// 並べ替え（[from] を [to] の位置へ）
  Future<void> move(int from, int to) async {
    final p = _items.removeAt(from);
    _items.insert(to.clamp(0, _items.length), p);
    await _persist();
  }

  Future<void> _persist() async {
    notifyListeners();
    await _meta.put('metronome.presets', [for (final p in _items) p.toMap()]);
  }
}

/// プリセットを順に鳴らすためのクリックトラック（それぞれ [bars] 小節ずつ）
ClickTrack presetsToClickTrack(
  String name,
  List<MetronomePreset> presets, {
  int bars = 8,
}) => ClickTrack(
  name: name,
  sections: [
    for (final p in presets)
      ClickSection(
        bars: bars,
        bpm: p.settings.bpm,
        beatsPerBar: p.settings.beatsPerBar,
        subdivision: p.settings.subdivision,
      ).normalized(),
  ],
);
