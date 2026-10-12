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
}
