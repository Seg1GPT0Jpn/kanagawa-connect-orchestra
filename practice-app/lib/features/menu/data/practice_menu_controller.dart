import 'package:flutter/foundation.dart';

import '../domain/menu_audit.dart';
import '../domain/menu_rules.dart';
import 'menu_settings_repository.dart';

/// いま使っている時間モードとメニュー（保存すると練習画面にも反映される）
///
/// 「今日だけ」のメニュー（今日の調子からのおすすめなど）は [useForToday] で、保存はしない。
class PracticeMenuController extends ChangeNotifier {
  PracticeMenuController({
    required this.modes,
    required this._repository,
    required String modeId,
    required Map<String, Map<String, int>> savedMenus,
  }) : assert(modes.isNotEmpty),
       _saved = {
         for (final m in modes) m.id: savedMenus[m.id] ?? m.defaultMenu,
       } {
    _rules = _modeById(modeId) ?? modes.first;
    _value = _saved[_rules.id]!;
  }

  /// 端末に保存した時間モード・メニューを読み込む
  static Future<PracticeMenuController> load(
    MenuSettingsRepository repository,
    List<MenuRuleSet> modes,
  ) async => PracticeMenuController(
    modes: modes,
    repository: repository,
    modeId: await repository.loadModeId() ?? modes.first.id,
    savedMenus: {for (final m in modes) m.id: await repository.load(m)},
  );

  final List<MenuRuleSet> modes;
  final MenuSettingsRepository _repository;
  final Map<String, Map<String, int>> _saved;
  late MenuRuleSet _rules;
  late Map<String, int> _value;

  MenuRuleSet get rules => _rules;

  /// 今日のメニュー（項目 id → 分）
  Map<String, int> get value => _value;

  /// 今のモードの保存済みメニュー
  Map<String, int> get savedMenu => _saved[_rules.id]!;

  /// [modeId] のモードの保存済みメニュー
  Map<String, int> savedMenuFor(String modeId) => _saved[modeId] ?? savedMenu;

  /// 今日だけのメニューを使っている（保存したメニューと違う）
  bool get isTemporary => !mapEquals(_value, savedMenu);

  MenuRuleSet? _modeById(String id) {
    for (final m in modes) {
      if (m.id == id) return m;
    }
    return null;
  }

  /// 時間モードを切り替える（選んだモードは次回も使う）
  Future<void> selectMode(String modeId) async {
    final mode = _modeById(modeId);
    if (mode == null || mode.id == _rules.id) return;
    _rules = mode;
    _value = _saved[mode.id]!;
    notifyListeners();
    await _repository.saveModeId(mode.id);
  }

  /// 今のモードのメニューを保存する。ルールを満たさないメニューは [ArgumentError]
  Future<void> save(Map<String, int> minutes) async {
    await _repository.save(_rules, minutes);
    _saved[_rules.id] = Map.unmodifiable(minutes);
    _value = _saved[_rules.id]!;
    notifyListeners();
  }

  /// 今日だけ、[modeId] のモードで [minutes]（null なら保存済み）を使う。保存はしない
  void useForToday(String modeId, [Map<String, int>? minutes]) {
    final mode = _modeById(modeId);
    if (mode == null) return;
    final menu = minutes ?? _saved[mode.id]!;
    if (!auditMenu(menu, mode).isValid) {
      throw ArgumentError('ルールを満たさないメニューは使えません');
    }
    _rules = mode;
    _value = Map.unmodifiable(menu);
    notifyListeners();
  }

  /// 今日だけのメニューをやめて、保存したメニューに戻す
  void resetToSaved() {
    _value = savedMenu;
    notifyListeners();
  }
}
