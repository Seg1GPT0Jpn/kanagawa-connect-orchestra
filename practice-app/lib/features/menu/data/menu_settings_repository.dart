import '../../../core/meta_store.dart';
import '../domain/menu_audit.dart';
import '../domain/menu_rules.dart';

/// 自分のメニュー（項目 id → 分）を端末内に保存する。保存できるのはルールを満たすメニューだけ
class MenuSettingsRepository {
  MenuSettingsRepository(this._meta);

  final MetaStore _meta;

  String _key(MenuRuleSet rules) => 'menu.${rules.id}';

  /// 最後に選んだ時間モード（未選択なら null）
  Future<String?> loadModeId() async {
    final v = await _meta.get('menu.mode');
    return v is String ? v : null;
  }

  Future<void> saveModeId(String id) => _meta.put('menu.mode', id);

  /// 保存したメニュー。未保存・壊れている・ルールを満たさない（ルール変更後など）ときは初期値
  Future<Map<String, int>> load(MenuRuleSet rules) async {
    final raw = await _meta.get(_key(rules));
    if (raw is! Map) return rules.defaultMenu;
    final minutes = <String, int>{};
    for (final MapEntry(:key, :value) in raw.entries) {
      if (key is! String || value is! int) return rules.defaultMenu;
      minutes[key] = value;
    }
    return auditMenu(minutes, rules).isValid ? minutes : rules.defaultMenu;
  }

  Future<void> save(MenuRuleSet rules, Map<String, int> minutes) async {
    final audit = auditMenu(minutes, rules);
    if (!audit.isValid) {
      throw ArgumentError(
        'ルールを満たさないメニューは保存できません：'
        '${audit.violations.map((v) => v.message).join('、')}',
      );
    }
    await _meta.put(_key(rules), Map.of(minutes));
  }
}
