import 'package:flutter_test/flutter_test.dart';
import 'package:kco_practice/core/meta_store.dart';
import 'package:kco_practice/features/menu/data/practice_menu_controller.dart';
import 'package:kco_practice/features/menu/data/menu_settings_repository.dart';
import 'package:kco_practice/features/menu/domain/menu_rules.dart';

import '../../helpers.dart';
import '../../menu_fixtures.dart';

void main() {
  final rules = trumpetBasicRules;
  late MetaStore meta;
  late MenuSettingsRepository repo;

  setUp(() async {
    meta = MetaStore(await openMemoryDb());
    repo = MenuSettingsRepository(meta);
  });

  final valid = menu(
    mouthpiece: 3,
    repertoire: 12,
    longTone: 10,
    lipSlur: 0,
    tonguing: 0,
    arban: {'arban_tonguing': 20},
  );

  test('未保存なら初期値', () async {
    expect(await repo.load(rules), rules.defaultMenu);
  });

  test('ルールを満たすメニューは保存して読み戻せる', () async {
    await repo.save(rules, valid);
    expect(await repo.load(rules), valid);
  });

  test('ルールを満たさないメニューは保存できない', () async {
    await expectLater(
      repo.save(rules, {...valid, 'arban_tonguing': 41}),
      throwsArgumentError,
    );
    expect(await repo.load(rules), rules.defaultMenu);
  });

  test('保存済みの値が壊れている・ルールを満たさなくなったら初期値', () async {
    await meta.put('menu.trumpet_basic', {...valid, 'arban_tonguing': 99});
    expect(await repo.load(rules), rules.defaultMenu);
    await meta.put('menu.trumpet_basic', 'broken');
    expect(await repo.load(rules), rules.defaultMenu);
    await meta.put('menu.trumpet_basic', {...valid, 'arban_tonguing': '20'});
    expect(await repo.load(rules), rules.defaultMenu);
    // 章ごとに分ける前に保存したメニュー（arban 1項目）も初期値に戻す
    await meta.put('menu.trumpet_basic', {
      'mouthpiece': 15,
      'long_tone': 10,
      'lip_slur': 0,
      'tonguing': 0,
      'arban': 20,
    });
    expect(await repo.load(rules), rules.defaultMenu);
  });

  Future<PracticeMenuController> controller() =>
      PracticeMenuController.load(repo, trumpetModes);

  test('PracticeMenuController：初めは通常モードの初期値', () async {
    final c = await controller();
    expect(c.rules.id, 'trumpet_basic');
    expect(c.value, rules.defaultMenu);
    expect(c.isTemporary, isFalse);
  });

  test('PracticeMenuController：保存すると値が変わり、違反なら変わらない', () async {
    final c = await controller();
    await c.save(valid);
    expect(c.value, valid);
    await expectLater(c.save({...valid, 'mouthpiece': 0}), throwsArgumentError);
    expect(c.value, valid);
    // 読み込み直しても残っている
    expect((await controller()).value, valid);
  });

  test('PracticeMenuController：時間モードを切り替えると、そのモードのメニューになり、次回も同じモード', () async {
    final c = await controller();
    var notified = 0;
    c.addListener(() => notified++);
    await c.selectMode('trumpet_20min');
    expect(c.rules.id, 'trumpet_20min');
    expect(c.value, trumpet20Rules.defaultMenu);
    expect(notified, 1);

    final short = {...trumpet20Rules.defaultMenu, 'repertoire': 10};
    await c.save(short);
    final again = await controller();
    expect(again.rules.id, 'trumpet_20min');
    expect(again.value, short);
    // 通常モードのメニューは別に保存されている
    await again.selectMode('trumpet_basic');
    expect(again.value, rules.defaultMenu);
    // ないモードは無視
    await again.selectMode('nope');
    expect(again.rules.id, 'trumpet_basic');
  });

  test('PracticeMenuController：今日だけのメニューは保存せず、戻せる', () async {
    final c = await controller();
    c.useForToday('trumpet_10min');
    expect(c.rules.id, 'trumpet_10min');
    expect(c.value, trumpet10Rules.defaultMenu);
    expect(c.isTemporary, isFalse); // 10分モードの保存済みメニューそのもの

    c.useForToday('trumpet_basic', valid);
    expect(c.isTemporary, isTrue);
    expect(c.savedMenu, rules.defaultMenu);
    c.resetToSaved();
    expect(c.value, rules.defaultMenu);
    expect(c.isTemporary, isFalse);

    // ルールを満たさないメニューは使えない
    expect(
      () => c.useForToday('trumpet_10min', rules.defaultMenu),
      throwsArgumentError,
    );
    // 読み込み直すと、保存した時間モード（通常）に戻る
    expect((await controller()).rules.id, 'trumpet_basic');
  });

  test('端末 ID は一度作ったら変わらない', () async {
    final id = await meta.deviceId();
    expect(id, hasLength(20));
    expect(await meta.deviceId(), id);
  });
}
