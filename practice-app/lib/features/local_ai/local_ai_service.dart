/// ローカル AI（端末内 LLM）の抽象化
///
/// エンジン（端末・ブラウザに内蔵の AI など）を差し替えられるように、
/// アプリの他の部分はこのインターフェースだけを使う。
/// AI が使えない端末では [UnavailableLocalAiService] を使い、AI なしで動かす。
library;

/// AI がこの端末で使えるか
enum LocalAiState {
  /// すぐ使える
  ready,

  /// 使えるが、最初に OS・ブラウザが AI を準備（ダウンロード）する必要がある
  needsPreparation,

  /// 準備中（ダウンロード中など）
  preparing,

  /// この端末・ブラウザでは使えない
  unavailable,
}

abstract interface class LocalAiService {
  /// 今の端末・環境でローカル AI が使えるか（[initializeModel] が成功したあとで true）
  bool get isSupported;

  /// 使えるかどうかを調べる（時間がかかっても固まらない）
  Future<LocalAiState> probe();

  /// モデルの読み込み・初期化（必要なら OS・ブラウザの準備も）。失敗したら [LocalAiException]
  ///
  /// Web では、ボタンを押した中で呼ぶ必要がある（ブラウザがダウンロードを始めるため）。
  Future<void> initializeModel({void Function(int percent)? onProgress});

  /// [promptText] に対するローカル推論の結果。出力は必ずプログラム側で検査してから使う
  Future<String> generatePrompt(String promptText, {String? systemInstruction});
}

class LocalAiException implements Exception {
  const LocalAiException(this.message);

  final String message;

  @override
  String toString() => message;
}

/// ローカル AI が使えないときの実装（対応していない端末・ブラウザなど）
class UnavailableLocalAiService implements LocalAiService {
  const UnavailableLocalAiService({this.reason = 'この端末ではローカル AI を使えません'});

  final String reason;

  @override
  bool get isSupported => false;

  @override
  Future<LocalAiState> probe() async => LocalAiState.unavailable;

  @override
  Future<void> initializeModel({
    void Function(int percent)? onProgress,
  }) async => throw LocalAiException(reason);

  @override
  Future<String> generatePrompt(
    String promptText, {
    String? systemInstruction,
  }) async => throw LocalAiException(reason);
}
