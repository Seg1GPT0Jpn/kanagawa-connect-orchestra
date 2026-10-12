import 'package:flutter/foundation.dart';

import '../domain/menu_rules.dart';
import 'menu_settings_repository.dart';

/// いま使っているメニュー（保存すると練習画面にも反映される）
class PracticeMenuController extends ValueNotifier<Map<String, int>> {
  PracticeMenuController(this.rules, this._repository, Map<String, int> initial)
    : super(initial);

  final MenuRuleSet rules;
  final MenuSettingsRepository _repository;

  /// ルールを満たさないメニューは [ArgumentError]
  Future<void> save(Map<String, int> minutes) async {
    await _repository.save(rules, minutes);
    value = Map.unmodifiable(minutes);
  }
}
