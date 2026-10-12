# 練習お助けアプリ（practice-app）

かながわコネクトオーケストラの楽器練習お助けアプリです。Flutter で Android・iOS・PC ブラウザ（Web）に対応します。

- **AI は端末内（ローカル）だけで動かします。** 外部のクラウド AI は使いません（プライバシー保護・オフライン利用・費用ゼロのため）。
- **時間計算・ルール検査・集計はプログラム（Dart）が決定論的に行います。** AI は提案や文章づくりの補助だけで、AI の出力は必ずプログラムの検査を通してから使います。
- **AI が使えない端末でも、** 練習記録・タイマー・テンプレート・メニュー監査はすべて動きます。

## いまできていること（Stage 1 の土台）

| 機能 | 場所 |
|---|---|
| トランペット基礎メニューのルールと決定論的監査・修正案 | `lib/features/menu/domain/` |
| AI のメニュー案の読み取り・検査（JSON 以外・ルール違反は採用しない） | `lib/features/menu/domain/menu_proposal.dart` |
| ローカル AI の抽象化（`LocalAiService`）と「AI なし」の実装 | `lib/features/local_ai/` |
| メニュー監査の画面 | `lib/features/menu/presentation/` |

### トランペット基礎メニューのルール

| 項目 | 範囲 | 初期値 |
|---|---|---|
| マウスピース | 15〜30分 | 20分 |
| ロングトーン | 10〜20分 | 15分 |
| リップスラー | 0〜15分（0分可） | 5分 |
| タンギング | 0〜10分（0分可） | 5分 |
| Arban（アーバン） | 20〜40分 | 30分 |
| **合計** | **45〜115分** | 75分 |

ルールを変えるときは `lib/features/menu/domain/menu_rules.dart` を直し、`test/features/menu/menu_audit_test.dart` の「仕様どおりの範囲」も合わせて直してください。

## フォルダ構成

```
lib/
├── app/                  画面全体の設定（テーマ・最初の画面）
├── core/                 共通の部品（必要になったら作る）
├── features/
│   ├── auth/             認証（Stage 1・Firebase プロジェクト作成後）
│   ├── practice/         練習記録・タイマー（Stage 1）
│   ├── menu/             メニュー作成・決定論的監査
│   ├── local_ai/         ローカル AI（モデル管理・推論・使えないときの代わり）
│   └── audio_tools/      チューナー・メトロノーム・録音（Stage 2〜3）
└── main.dart
```

## 開発環境

- Flutter 3.47.7（stable）／ Dart 3.13.5
- Android の確認：Android Studio（Android SDK）
- iOS の確認：Mac と Xcode
- Web の確認：Chrome（Chromium 系）

```bash
cd practice-app
flutter pub get
flutter run -d chrome     # PC ブラウザで起動
flutter test              # テスト
flutter analyze           # 静的解析
dart format lib test      # 書式をそろえる

# Web 版の本番ビルド（描画エンジン CanvasKit を CDN から読まずに同梱する＝オフラインでも起動できる）
flutter build web --no-web-resources-cdn
```

プルリクエストでは GitHub Actions（`.github/workflows/practice-app.yml`）が書式・静的解析・テスト・Web ビルドを確認します。

## これからの予定

### Firebase プロジェクト（新しく作る）

団員アプリ・公式サイトとは別の Firebase プロジェクトを使います。作成は運営の Google アカウントで行ってください。

1. [Firebase コンソール](https://console.firebase.google.com/) でプロジェクトを作成（例：`kco-practice`）
2. Authentication と Firestore を有効にする
3. 手元で `dart pub global activate flutterfire_cli` → `cd practice-app && flutterfire configure` を実行し、Android・iOS・Web のアプリを登録する
   （生成される `lib/firebase_options.dart` をコミットします。中身は公開されても問題ない識別子です）

### ローカル AI（Stage 2）

- エンジン：[`flutter_edge_ai`](https://pub.dev/packages/flutter_edge_ai)（旧 `flutter_gemma`）
  - Android・iOS：LiteRT-LM（`.litertlm`）
  - Web：MediaPipe（`.task`、WebGPU が必要）
  - 予備：[`llamadart`](https://pub.dev/packages/llamadart)（GGUF）
- モデル：Gemma 2 2B に加えて Gemma 3 1B・Gemma 3n E2B も比べて選ぶ。数百 MB〜数 GB あるので、アプリには入れず初回にダウンロードする
- Google は MediaPipe LLM Inference API を保守のみとし、新機能は LiteRT-LM に集中させる方針です
- 端末ごとの制約
  - Android：LiteRT-LM は minSdk 30（Android 11）以上・arm64-v8a のみ
  - iOS：15.0 以上（MediaPipe を使うなら 16.0）。大きなモデルにはメモリ上限を引き上げる entitlements が必要。シミュレーターは CPU のみ
  - Web：WebGPU が使えないブラウザでは `isSupported = false` として AI なしで動かす
