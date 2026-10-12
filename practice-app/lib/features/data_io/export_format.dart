/// 記録の書き出し・読み込みの形（決定論的）
///
///  ・バックアップ（JSON）：このアプリで読み込める形。練習記録と録音の分析結果
///  ・表（CSV）：Excel などで開ける形。練習記録を1行1回で
library;

import 'dart:convert';

import '../../core/clock.dart';
import '../menu/domain/menu_rules.dart';
import '../practice/domain/practice_record.dart';
import '../recording/domain/recording_result.dart';

const exportFormatName = 'kco-practice';
const exportFormatVersion = 1;

/// 読み込める記録の数の上限（壊れた・大きすぎるファイルで固まらないように）
const maxImportRecords = 20000;

class ExportData {
  const ExportData({required this.records, required this.recordingResults});

  final List<PracticeRecord> records;
  final List<RecordingResult> recordingResults;
}

/// バックアップ（JSON）。削除済みの記録は含めない
String buildBackupJson(ExportData data, {required DateTime exportedAt}) =>
    const JsonEncoder.withIndent('  ').convert({
      'format': exportFormatName,
      'version': exportFormatVersion,
      'exportedAt': exportedAt.toUtc().toIso8601String(),
      'records': [
        for (final r in data.records)
          if (!r.deleted) r.toMap(),
      ],
      'recordingResults': [for (final r in data.recordingResults) r.toMap()],
    });

class ImportFormatException implements Exception {
  const ImportFormatException(this.message);

  final String message;

  @override
  String toString() => message;
}

/// バックアップ（JSON）を読む。形が違えば [ImportFormatException]
ExportData parseBackupJson(String text) {
  final Object? decoded;
  try {
    decoded = jsonDecode(text);
  } on FormatException {
    throw const ImportFormatException('JSON として読めないファイルです');
  }
  if (decoded is! Map || decoded['format'] != exportFormatName) {
    throw const ImportFormatException('このアプリのバックアップではありません');
  }
  final version = decoded['version'];
  if (version is! int || version > exportFormatVersion) {
    throw const ImportFormatException(
      '新しい版のアプリで作ったバックアップです。アプリを更新してから読み込んでください',
    );
  }
  final rawRecords = decoded['records'];
  final rawResults = decoded['recordingResults'] ?? const [];
  if (rawRecords is! List || rawResults is! List) {
    throw const ImportFormatException('バックアップの中身が壊れています');
  }
  if (rawRecords.length + rawResults.length > maxImportRecords) {
    throw const ImportFormatException('記録が多すぎて読み込めません');
  }
  try {
    return ExportData(
      records: [for (final m in rawRecords) _record(m)],
      recordingResults: [
        for (final m in rawResults)
          RecordingResult.fromMap(Map<String, Object?>.from(m as Map)),
      ],
    );
  } on ImportFormatException {
    rethrow;
  } catch (_) {
    throw const ImportFormatException('バックアップの中の記録が壊れています');
  }
}

PracticeRecord _record(Object? m) {
  final r = PracticeRecord.fromMap(Map<String, Object?>.from(m! as Map));
  if (!RegExp(r'^[A-Za-z0-9]{1,40}$').hasMatch(r.id) ||
      !RegExp(r'^\d{4}-\d{2}-\d{2}$').hasMatch(r.practicedOn)) {
    throw const ImportFormatException('バックアップの中の記録が壊れています');
  }
  if (r.note.length > 500) throw const ImportFormatException('メモが長すぎる記録があります');
  if (r.goal.length > 200 || r.nextFocus.length > 200) {
    throw const ImportFormatException('目標・次回の課題が長すぎる記録があります');
  }
  return r;
}

/// 表（CSV）。Excel で文字化けしないよう、先頭に BOM を付ける
String buildRecordsCsv(List<PracticeRecord> records, MenuRuleSet rules) {
  // 列：ルールにある項目＋記録にだけある項目（以前の arban など）
  final ids = [
    for (final i in rules.items) i.id,
    for (final id in {for (final r in records) ...r.actualSeconds.keys})
      if (rules.itemById(id) == null) id,
  ];
  final header = [
    '練習した日',
    '開始時刻',
    '合計（分）',
    for (final id in ids) '${rules.labelOf(id)}（分）',
    '目標',
    '達成度',
    'メモ',
    '次回の課題',
  ];
  final rows = [
    for (final r in records.where((r) => !r.deleted))
      [
        r.practicedOn,
        _time(r.startedAtMillis),
        _minutes(r.totalActualSeconds),
        for (final id in ids) _minutes(r.actualSeconds[id] ?? 0),
        r.goal,
        r.achievement == 0
            ? ''
            : PracticeRecord.achievementLabels[r.achievement],
        r.note,
        r.nextFocus,
      ],
  ];
  return '﻿${[header, ...rows].map((row) => row.map(_csvField).join(',')).join('\r\n')}\r\n';
}

String _time(int millis) {
  final t = DateTime.fromMillisecondsSinceEpoch(millis);
  return '${t.hour.toString().padLeft(2, '0')}:${t.minute.toString().padLeft(2, '0')}';
}

String _minutes(int seconds) => (seconds / 60).toStringAsFixed(1);

String _csvField(String v) {
  // 数式として解釈されないように（CSV インジェクション対策）
  final safe =
      v.startsWith(RegExp(r'[=+\-@\t\r]')) && double.tryParse(v) == null
      ? "'$v"
      : v;
  return safe.contains(RegExp(r'[",\r\n]'))
      ? '"${safe.replaceAll('"', '""')}"'
      : safe;
}

/// 書き出すファイルの名前（例：practice-2026-10-12.csv）
String exportFileName(DateTime now, String extension) =>
    'practice-${localDateString(now)}.$extension';
