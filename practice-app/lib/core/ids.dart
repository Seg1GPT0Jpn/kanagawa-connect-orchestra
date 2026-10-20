import 'dart:math';

final _random = Random.secure();
const _chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';

/// 端末内でも衝突しにくいランダムな ID（Firestore の自動 ID と同じ20文字）
String generateId() => String.fromCharCodes(
  Iterable.generate(
    20,
    (_) => _chars.codeUnitAt(_random.nextInt(_chars.length)),
  ),
);
