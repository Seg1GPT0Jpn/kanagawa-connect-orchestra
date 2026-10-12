import 'dart:convert';
import 'dart:typed_data';

import 'package:flutter_test/flutter_test.dart';
import 'package:kco_practice/features/data_io/data_io_service.dart';
import 'package:kco_practice/features/data_io/export_format.dart';
import 'package:kco_practice/features/menu/domain/menu_rules.dart';
import 'package:kco_practice/features/practice/data/practice_repository.dart';
import 'package:kco_practice/features/recording/data/recording_repository.dart';
import 'package:kco_practice/features/recording/domain/recording_result.dart';

import '../../helpers.dart';

RecordingResult result(String id) => RecordingResult(
  id: id,
  recordedAtMillis: 1000,
  durationSeconds: 5,
  voicedSeconds: 4.5,
  midi: 70,
  centsOffset: 1.2,
  pitchSpreadCents: 3.4,
  driftCents: -2,
  volumeSpreadDb: 0.8,
  attackSeconds: 0.1,
  a4: 442,
);

void main() {
  group('形', () {
    test('バックアップ：削除済みを除いて書き出し、読み戻せる', () {
      final json = buildBackupJson(
        ExportData(
          records: [
            record('r1', note: 'メモ'),
            record('r2', deleted: true),
          ],
          recordingResults: [result('x1')],
        ),
        exportedAt: DateTime.utc(2026, 10, 12),
      );
      final m = jsonDecode(json) as Map;
      expect(m['format'], 'kco-practice');
      expect(m['version'], 1);
      expect(m['exportedAt'], '2026-10-12T00:00:00.000Z');
      final back = parseBackupJson(json);
      expect(back.records.single, record('r1', note: 'メモ'));
      expect(back.recordingResults.single.toMap(), result('x1').toMap());
    });

    test('ほかのファイル・壊れたファイル・新しい版は読み込まない', () {
      for (final (text, why) in [
        ('not json', 'JSON として読めない'),
        ('{"format": "other"}', 'このアプリのバックアップではありません'),
        ('{"format": "kco-practice", "version": 99, "records": []}', '新しい版'),
        ('{"format": "kco-practice", "version": 1, "records": "x"}', '壊れています'),
        (
          '{"format": "kco-practice", "version": 1, "records": [{"id": "a"}]}',
          '壊れています',
        ),
        (
          '{"format": "kco-practice", "version": 1, "records": [${jsonEncode(record('bad-id!').toMap())}]}',
          '壊れています',
        ),
      ]) {
        expect(
          () => parseBackupJson(text),
          throwsA(
            isA<ImportFormatException>().having(
              (e) => e.message,
              'message',
              contains(why),
            ),
          ),
          reason: text,
        );
      }
    });

    test('CSV：BOM 付き・見出し・分（小数1桁）・ルールにない項目も列にする・数式にならない', () {
      final csv = buildRecordsCsv([
        record(
          'r1',
          actual: {'long_tone': 900, 'arban_scales': 630},
          note: '=SUM(A1)',
        ),
        record('r2', actual: {'arban': 1200}, note: 'カンマ, と "引用"'),
        record('r3', deleted: true),
      ], trumpetBasicRules);
      expect(csv.startsWith('﻿'), isTrue);
      final lines = csv.substring(1).trimRight().split('\r\n');
      expect(lines, hasLength(3));
      expect(
        lines[0],
        startsWith('練習した日,開始時刻,合計（分）,ウォームアップ（呼吸・バズィング）（分）,ロングトーン（分）'),
      );
      expect(lines[0], contains('Arban：音階（分）'));
      expect(lines[0], endsWith('Arban（アーバン）（分）,目標,達成度,メモ,次回の課題'));
      expect(lines[1], contains(',25.5,')); // 合計 1530秒
      expect(lines[1], contains(',15.0,'));
      expect(lines[1], endsWith(",,,'=SUM(A1),"));
      expect(lines[2], endsWith(',"カンマ, と ""引用""",'));
    });

    test('ファイル名', () {
      expect(
        exportFileName(DateTime(2026, 10, 12, 9), 'csv'),
        'practice-2026-10-12.csv',
      );
    });
  });

  group('取り込み', () {
    late PracticeRepository repo;
    late RecordingRepository recs;
    late FakeFileGateway files;
    late DataIoService io;

    setUp(() async {
      final db = await openMemoryDb();
      repo = PracticeRepository(db, deviceId: 'devA');
      recs = RecordingRepository(db);
      files = FakeFileGateway();
      io = DataIoService(
        practice: repo,
        recordings: recs,
        files: files,
        clock: FakeClock().call,
      );
    });

    test('ない記録は追加、古い版は無視、新しい版は更新。持ち主は今のアカウントにそろえ、未送信にする', () async {
      await repo.applyRemote(
        record('keep', owner: 'u1', updatedAt: 5000, note: '端末'),
      );
      await repo.applyRemote(
        record('upd', owner: 'u1', updatedAt: 1000, note: '古い'),
      );
      final r = await repo.importRecords([
        record('new', owner: 'someone'),
        record('keep', owner: 'u1', updatedAt: 1000, note: '古いバックアップ'),
        record('upd', owner: 'u1', updatedAt: 9000, note: '新しい'),
      ], 'u1');
      expect([r.added, r.updated, r.unchanged], [1, 1, 1]);
      expect((await repo.get('new'))!.ownerUid, 'u1');
      expect(await repo.isDirty('new'), isTrue);
      expect((await repo.get('keep'))!.note, '端末');
      expect((await repo.get('upd'))!.note, '新しい');
    });

    test('書き出したバックアップを別の端末で読み込むと、同じ記録になる', () async {
      await repo.create(
        ownerUid: null,
        startedAt: DateTime(2026, 10, 12, 18),
        ruleSetId: 'trumpet_basic',
        plannedMinutes: const {'long_tone': 15},
        actualSeconds: const {'long_tone': 900},
      );
      await recs.save(result('x1'));
      expect(await io.exportBackup(null), isTrue);
      expect(await io.exportCsv(null, trumpetBasicRules), isTrue);
      expect(
        files.saved.keys,
        containsAll(['practice-2026-10-12.json', 'practice-2026-10-12.csv']),
      );
      expect(files.saved['practice-2026-10-12.csv']!.$2, 'text/csv');

      final db2 = await openMemoryDb();
      final repo2 = PracticeRepository(db2, deviceId: 'devB');
      final recs2 = RecordingRepository(db2);
      final files2 = FakeFileGateway()
        ..toPick = files.saved['practice-2026-10-12.json']!.$1;
      final io2 = DataIoService(
        practice: repo2,
        recordings: recs2,
        files: files2,
      );
      final report = (await io2.importBackup(null))!;
      expect(
        [report.added, report.updated, report.unchanged, report.results],
        [1, 0, 0, 1],
      );
      expect((await repo2.visible(null)).single.actualSeconds, {
        'long_tone': 900,
      });
      expect((await recs2.all()).single.id, 'x1');

      // もう一度読み込んでも増えない
      final again = (await io2.importBackup(null))!;
      expect([again.added, again.unchanged, again.results], [0, 1, 0]);
    });

    test('やめたら何もしない・UTF-8 でなければエラー', () async {
      files.cancel = true;
      expect(await io.importBackup(null), isNull);
      expect(await io.exportCsv(null, trumpetBasicRules), isFalse);
      files
        ..cancel = false
        ..toPick = Uint8List.fromList([0xff, 0xfe, 0x00]);
      await expectLater(
        io.importBackup(null),
        throwsA(isA<ImportFormatException>()),
      );
    });
  });
}
