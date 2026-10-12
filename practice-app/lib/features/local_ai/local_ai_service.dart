/// ローカル AI（端末内 LLM）の抽象化
///
/// モデルやエンジン（LiteRT-LM・MediaPipe など）を差し替えられるように、
/// アプリの他の部分はこのインターフェースだけを使う。
/// AI が使えない端末では [UnavailableLocalAiService] を使い、AI なしで動かす。
library;

abstract interface class LocalAiService {
  /// 今の端末・環境でローカル AI が使えるか
  bool get isSupported;

  /// モデルの読み込み・初期化。失敗したら [LocalAiException]
  Future<void> initializeModel();

  /// [promptText] に対するローカル推論の結果。出力は必ずプログラム側で検査してから使う
  Future<String> generatePrompt(String promptText);
}

class LocalAiException implements Exception {
  const LocalAiException(this.message);

  final String message;

  @override
  String toString() => 'LocalAiException: $message';
}

/// ローカル AI が使えないときの実装（初期化に失敗した端末・非対応ブラウザなど）
class UnavailableLocalAiService implements LocalAiService {
  const UnavailableLocalAiService({this.reason = 'この端末ではローカル AI を使えません'});

  final String reason;

  @override
  bool get isSupported => false;

  @override
  Future<void> initializeModel() async => throw LocalAiException(reason);

  @override
  Future<String> generatePrompt(String promptText) async =>
      throw LocalAiException(reason);
}
