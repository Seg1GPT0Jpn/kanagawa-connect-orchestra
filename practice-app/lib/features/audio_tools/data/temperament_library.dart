import 'dart:convert';

import 'package:flutter/foundation.dart';

import '../../../core/ids.dart';
import '../../../core/meta_store.dart';
import '../domain/temperament.dart';

/// 自分で作った音律の一覧（端末内に保存。文字にして共有・取り込みできる）
class TemperamentLibrary extends ChangeNotifier {
  TemperamentLibrary(this._meta, this._items);

  static Future<TemperamentLibrary> load(MetaStore meta) async {
    final raw = await meta.get('temperaments.custom');
    return TemperamentLibrary(meta, [
      if (raw is List)
        for (final r in raw) ?CustomTemperament.fromMap(r),
    ]);
  }

  final MetaStore _meta;
  final List<CustomTemperament> _items;

  /// 共有用の文字の目印
  static const shareFormat = 'kco-temperament';
  static const maxItems = 50;

  List<CustomTemperament> get items => List.unmodifiable(_items);

  CustomTemperament? byId(String id) {
    for (final t in _items) {
      if (t.id == id) return t;
    }
    return null;
  }

  Future<CustomTemperament> create(String name, List<double> offsets) async {
    final t = CustomTemperament.fromMap({
      'id': generateId(),
      'name': name.trim().isEmpty ? '自分の音律' : name.trim(),
      'offsets': offsets,
    })!;
    _items.add(t);
    if (_items.length > maxItems) _items.removeAt(0);
    await _save();
    return t;
  }

  /// 複製（名前に「のコピー」を付ける）
  Future<CustomTemperament> duplicate(CustomTemperament from) =>
      create('${from.name}のコピー', from.offsets);

  Future<void> update(CustomTemperament t) async {
    final i = _items.indexWhere((e) => e.id == t.id);
    if (i < 0) return;
    _items[i] = CustomTemperament.fromMap(t.toMap())!;
    await _save();
  }

  Future<void> delete(String id) async {
    _items.removeWhere((t) => t.id == id);
    await _save();
  }

  /// 共有用の文字（JSON）
  String exportText(CustomTemperament t) => jsonEncode({
    'format': shareFormat,
    'name': t.name,
    'offsets': [for (final o in t.offsets) double.parse(o.toStringAsFixed(2))],
  });

  /// 共有された文字を取り込む。読めなければ null
  Future<CustomTemperament?> importText(String text) async {
    final Object? decoded;
    try {
      decoded = jsonDecode(text.trim());
    } on FormatException {
      return null;
    }
    if (decoded is! Map || decoded['format'] != shareFormat) return null;
    final parsed = CustomTemperament.fromMap({
      'id': 'x',
      'name': decoded['name'] is String ? decoded['name'] : '取り込んだ音律',
      'offsets': decoded['offsets'],
    });
    if (parsed == null) return null;
    return create(parsed.name, parsed.offsets);
  }

  Future<void> _save() async {
    notifyListeners();
    await _meta.put('temperaments.custom', [for (final t in _items) t.toMap()]);
  }
}
