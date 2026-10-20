import '../../../core/meta_store.dart';
import '../domain/day_condition.dart';

/// 日ごとの予定と調子を端末内に保存する（クラウドには送らない）
class DayConditionRepository {
  DayConditionRepository(this._meta);

  final MetaStore _meta;

  /// [day] は yyyy-MM-dd。未入力なら既定値
  Future<DayCondition> load(String day) async {
    final raw = await _meta.get('condition.$day');
    return raw is Map ? DayCondition.fromMap(raw) : const DayCondition();
  }

  Future<void> save(String day, DayCondition c) =>
      _meta.put('condition.$day', c.toMap());

  final Map<String, String> _goals = {};

  /// その日の目標（練習を始める前に書いておく）
  Future<String> loadGoal(String day) async =>
      _goals[day] ??= (await _meta.get('goal.$day') as String?) ?? '';

  /// 読み込み済み・書いた目標（待たずに使う）
  String cachedGoal(String day) => _goals[day] ?? '';

  Future<void> saveGoal(String day, String goal) {
    _goals[day] = goal;
    return _meta.put('goal.$day', goal);
  }
}
