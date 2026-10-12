import 'dart:convert';
import 'dart:typed_data';

import 'package:file_picker/file_picker.dart';

import '../../core/clock.dart';
import '../menu/domain/menu_rules.dart';
import '../practice/data/practice_repository.dart';
import '../audio_tools/data/tuner_session_repository.dart';
import '../recording/data/recording_repository.dart';
import 'export_format.dart';

/// ファイルの保存・選択（テストでは偽物に差し替える）
abstract interface class FileGateway {
  /// 保存したら true（やめたら false）
  Future<bool> save(
    String fileName,
    Uint8List bytes, {
    required String mimeType,
  });

  /// 選んだファイルの中身（やめたら null）
  Future<Uint8List?> pickJson();

  /// 選んだ音声ファイル（WAV）の中身（やめたら null）
  Future<Uint8List?> pickAudio();
}

class FilePickerGateway implements FileGateway {
  @override
  Future<bool> save(
    String fileName,
    Uint8List bytes, {
    required String mimeType,
  }) async =>
      await FilePicker.saveFile(
        fileName: fileName,
        bytes: bytes,
        mimeType: mimeType,
      ) !=
      null;

  @override
  Future<Uint8List?> pickJson() => _pick(const ['json']);

  @override
  Future<Uint8List?> pickAudio() => _pick(const ['wav']);

  Future<Uint8List?> _pick(List<String> extensions) async {
    final files = await FilePicker.pickFiles(
      type: FileType.custom,
      allowedExtensions: extensions,
    );
    if (files.isEmpty) return null;
    return files.first.xFile.readAsBytes();
  }
}

class ImportReport {
  const ImportReport({
    required this.added,
    required this.updated,
    required this.unchanged,
    required this.results,
    this.tunerSessions = 0,
  });

  final int added;
  final int updated;
  final int unchanged;

  /// 取り込んだ録音の分析結果の数
  final int results;

  /// 取り込んだ音程の記録の数
  final int tunerSessions;

  String get summary =>
      '練習記録：追加 $added 件・更新 $updated 件・変わらず $unchanged 件／録音の分析結果：追加 $results 件'
      '${tunerSessions == 0 ? '' : '／音程の記録：追加 $tunerSessions 件'}';
}

/// 記録の書き出し（CSV・バックアップ）と、バックアップの読み込み
class DataIoService {
  DataIoService({
    required this.practice,
    required this.recordings,
    required this.files,
    this.tunerSessions,
    this.clock = systemClock,
  });

  final PracticeRepository practice;
  final RecordingRepository recordings;
  final TunerSessionRepository? tunerSessions;
  final FileGateway files;
  final Clock clock;

  Future<bool> exportCsv(String? uid, MenuRuleSet rules) async {
    final csv = buildRecordsCsv(await practice.exportable(uid), rules);
    return files.save(
      exportFileName(clock(), 'csv'),
      Uint8List.fromList(utf8.encode(csv)),
      mimeType: 'text/csv',
    );
  }

  Future<bool> exportBackup(String? uid) async {
    final json = buildBackupJson(
      ExportData(
        records: await practice.exportable(uid),
        recordingResults: await recordings.all(),
        tunerSessions: await tunerSessions?.all() ?? const [],
      ),
      exportedAt: clock(),
    );
    return files.save(
      exportFileName(clock(), 'json'),
      Uint8List.fromList(utf8.encode(json)),
      mimeType: 'application/json',
    );
  }

  /// バックアップを選んで読み込む（やめたら null）。形が違えば [ImportFormatException]
  Future<ImportReport?> importBackup(String? uid) async {
    final bytes = await files.pickJson();
    if (bytes == null) return null;
    final String text;
    try {
      text = utf8.decode(bytes);
    } on FormatException {
      throw const ImportFormatException('文字コードが UTF-8 ではないファイルです');
    }
    final data = parseBackupJson(text);
    final r = await practice.importRecords(data.records, uid);
    final results = await recordings.importResults(data.recordingResults);
    final sessions =
        await tunerSessions?.importSessions(data.tunerSessions) ?? 0;
    return ImportReport(
      added: r.added,
      updated: r.updated,
      unchanged: r.unchanged,
      results: results,
      tunerSessions: sessions,
    );
  }
}
