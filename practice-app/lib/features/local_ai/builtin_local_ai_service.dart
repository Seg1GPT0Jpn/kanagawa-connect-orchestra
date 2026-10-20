import 'dart:async';

import 'package:flutter/foundation.dart';
import 'package:flutter_local_ai/flutter_local_ai.dart';

import 'local_ai_service.dart';

/// 端末・ブラウザに内蔵の AI（無料。モデルのファイルを配らない）
///
///  ・Android：Gemini Nano（ML Kit GenAI / AICore。Pixel 9 以降・Galaxy S25 以降など）
///  ・iPhone：Apple Foundation Models（iPhone 15 Pro 以降・iOS 26 以降、Apple Intelligence をオン）
///  ・Web：Chrome / Edge の Prompt API（パソコン版。オリジントライアルのトークンが必要）
class BuiltInLocalAiService implements LocalAiService {
  LocalAiModel? _model;
  Future<void>? _initializing;

  /// 1回の生成を待つ上限
  static const generationTimeout = Duration(seconds: 90);

  @override
  bool get isSupported => _model != null;

  @override
  Future<LocalAiState> probe() async {
    try {
      final a = await LocalAi.availability();
      return switch (a) {
        LocalAiAvailability.available => LocalAiState.ready,
        LocalAiAvailability.downloadable => LocalAiState.needsPreparation,
        LocalAiAvailability.downloading => LocalAiState.preparing,
        _ => LocalAiState.unavailable,
      };
    } catch (e) {
      debugPrint('local AI probe failed: $e');
      return LocalAiState.unavailable;
    }
  }

  @override
  Future<void> initializeModel({void Function(int percent)? onProgress}) =>
      _initializing ??= _initialize(onProgress).catchError((Object e) {
        _initializing = null;
        throw LocalAiException(_message(e));
      });

  Future<void> _initialize(void Function(int percent)? onProgress) async {
    await LocalAi.ensureReady(onProgress: onProgress);
    _model = await LocalAiModel.create(maxTokens: 4096);
  }

  @override
  Future<String> generatePrompt(
    String promptText, {
    String? systemInstruction,
  }) async {
    final model = _model;
    if (model == null) throw const LocalAiException('AI の準備ができていません');
    // 1回ごとに新しい会話にする（前の相談の内容を引きずらないように）
    final session = await model.openSession(
      temperature: 0.3,
      topK: 3,
      systemInstruction: systemInstruction,
    );
    try {
      await session.addQueryChunk(promptText);
      return await session.getResponse().timeout(generationTimeout);
    } on TimeoutException {
      throw const LocalAiException('AI の返事が時間内に届きませんでした');
    } catch (e) {
      throw LocalAiException(_message(e));
    } finally {
      unawaited(session.close().catchError((Object _) {}));
    }
  }

  static String _message(Object e) => switch (e) {
    LocalAiException() => e.message,
    LocalAiUserActivationRequiredException() =>
      'ボタンを押してから、もう一度お試しください（ブラウザの決まりで、操作の中でしか準備を始められません）',
    LocalAiUnavailableException() => 'この端末・ブラウザでは内蔵の AI を使えません',
    TimeoutException() => 'AI の準備が時間内に終わりませんでした',
    _ => 'AI を使えませんでした（$e）',
  };
}
