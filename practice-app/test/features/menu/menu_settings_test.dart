import 'package:flutter_test/flutter_test.dart';
import 'package:kco_practice/core/meta_store.dart';
import 'package:kco_practice/features/menu/data/practice_menu_controller.dart';
import 'package:kco_practice/features/menu/data/menu_settings_repository.dart';
import 'package:kco_practice/features/menu/domain/menu_rules.dart';

import '../../helpers.dart';

void main() {
  const rules = trumpetBasicRules;
  late MetaStore meta;
  late MenuSettingsRepository repo;

  setUp(() async {
    meta = MetaStore(await openMemoryDb());
    repo = MenuSettingsRepository(meta);
  });

  final valid = {
    'mouthpiece': 15,
    'long_tone': 10,
    'lip_slur': 0,
    'tonguing': 0,
    'arban': 20,
  };

  test('未保存なら初期値', () async {
    expect(await repo.load(rules), rules.defaultMenu);
  });

  test('ルールを満たすメニューは保存して読み戻せる', () async {
    await repo.save(rules, valid);
    expect(await repo.load(rules), valid);
  });

  test('ルールを満たさないメニューは保存できない', () async {
    await expectLater(
      repo.save(rules, {...valid, 'arban': 41}),
      throwsArgumentError,
    );
    expect(await repo.load(rules), rules.defaultMenu);
  });

  test('保存済みの値が壊れている・ルールを満たさなくなったら初期値', () async {
    await meta.put('menu.trumpet_basic', {...valid, 'arban': 99});
    expect(await repo.load(rules), rules.defaultMenu);
    await meta.put('menu.trumpet_basic', 'broken');
    expect(await repo.load(rules), rules.defaultMenu);
    await meta.put('menu.trumpet_basic', {...valid, 'arban': '20'});
    expect(await repo.load(rules), rules.defaultMenu);
  });

  test('PracticeMenuController は保存すると値が変わり、違反なら変わらない', () async {
    final c = PracticeMenuController(rules, repo, rules.defaultMenu);
    await c.save(valid);
    expect(c.value, valid);
    await expectLater(c.save({...valid, 'mouthpiece': 0}), throwsArgumentError);
    expect(c.value, valid);
  });

  test('端末 ID は一度作ったら変わらない', () async {
    final id = await meta.deviceId();
    expect(id, hasLength(20));
    expect(await meta.deviceId(), id);
  });
}
