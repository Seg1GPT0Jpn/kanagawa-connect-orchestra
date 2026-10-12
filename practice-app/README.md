# 練習お助けアプリ（practice-app）

かながわコネクトオーケストラの楽器練習お助けアプリです。Flutter で Android・iOS・PC ブラウザ（Web）に対応します。

- **AI は端末内（ローカル）だけで動かします。** 外部のクラウド AI は使いません（プライバシー保護・オフライン利用・費用ゼロのため）。
- **時間計算・ルール検査・集計はプログラム（Dart）が決定論的に行います。** AI は提案や文章づくりの補助だけで、AI の出力は必ずプログラムの検査を通してから使います。
- **AI が使えない端末でも、** 練習記録・タイマー・テンプレート・メニュー監査はすべて動きます。

## いまできていること（Stage 1）

| 機能 | 場所 |
|---|---|
| 練習タイマー（メニューの項目を順に計る・一時停止・途中で終える） | `lib/features/practice/domain/practice_session.dart`・`presentation/timer_page.dart` |
| 練習記録（端末内に保存・メモ・削除）と集計（今日・直近7日・連続日数・項目別） | `lib/features/practice/` |
| トランペット基礎メニューのルール（Arban は章ごと）と決定論的監査・修正案・おすすめ・自分のメニューの保存 | `lib/features/menu/` |
| AI のメニュー案の読み取り・検査（JSON 以外・ルール違反は採用しない） | `lib/features/menu/domain/menu_proposal.dart` |
| ログイン（Google・メールアドレス）※ログインしなくても使える | `lib/features/auth/` |
| クラウド同期（オフライン対応・競合の解決） | `lib/features/sync/` |
| Firestore のセキュリティルールとテスト | `firestore.rules`・`rules-test/` |
| ローカル AI の抽象化（`LocalAiService`）と「AI なし」の実装 | `lib/features/local_ai/` |

### 端末内の保存とクラウド同期のしくみ

- 記録はまず**端末内**に保存します（Web はブラウザの IndexedDB、Android・iOS はアプリ内のファイル。[sembast](https://pub.dev/packages/sembast) を使用）。
  ログインしていなくても、オフラインでも、練習・記録・集計はすべて使えます。
- アプリはクラウド（Firebase）を**待たずに起動**します。Firebase には裏でつなぎ、15秒以内につながらなければ端末内だけで動きます
  （オフラインだと Firebase の読み込みが終わらず、待っていると画面が出なくなるため）。
- ログインすると、次のときに同期します：ログインしたとき・記録を作る／直す／消したとき（2秒待ってまとめて）・「今すぐ同期」
  1. ログイン前に作った記録を、ログインしたアカウントに引き継ぐ
  2. 前回以降にクラウドで変わった記録を取り込む
  3. 端末でまだ送っていない記録を送る
- **競合の解決**（同じ記録を2台で直したとき）：後から直した方を残します。同じ時刻なら端末 ID で決めます（どの端末で計算しても同じ結果）。
  削除は「削除済み」の印を付けて同期するので、消した記録が別の端末から復活しません。
  ※ 端末の時計が大きくずれていると、古い編集が残ることがあります。
- クラウドでの保存場所：`users/{uid}/practiceRecords/{記録 ID}`。本人しか読み書きできません（`firestore.rules`）。
- ログアウトすると、そのアカウントの記録はこの端末に表示されなくなります（もう一度ログインすれば表示されます）。

### トランペット基礎メニューのルール

| 項目 | 範囲 | 初期値 |
|---|---|---|
| マウスピース | 15〜30分 | 20分 |
| ロングトーン | 10〜20分 | 15分 |
| リップスラー | 0〜15分（0分可） | 5分 |
| タンギング | 0〜10分（0分可） | 5分 |
| **Arban（12の章の合計）** | **20〜40分** | 30分（スラー・音階・タンギング各10分） |
| **合計** | **45〜115分** | 75分 |

Arban は 1893年版の分類で12の章（初歩練習・シンコペーション・スラー・音階・半音階・装飾音・音程跳躍・タンギング・
フレージング・二重奏・性格的練習曲・幻想曲／変奏曲）に分け、各章 0〜40分（0分＝お休み）で、その日に鍛えたい章を選びます。
メニュー画面の「今日の重点」から、調査をもとにしたおすすめ（バランス・短め・音色／柔軟性・指／音階・タンギング・表現／曲・長め）を選べます。
調査の分析と、ルールの見直しの提案は [docs/practice-research.md](docs/practice-research.md) を参照してください。

ルールを変えるときは `lib/features/menu/domain/menu_rules.dart` を直し、`test/features/menu/menu_audit_test.dart` の「仕様どおりの範囲」も合わせて直してください。
おすすめは `lib/features/menu/domain/menu_presets.dart` で、ルールを満たさない案はテストで失敗します。

## フォルダ構成

```
lib/
├── app/                  画面全体の設定（テーマ・最初の画面）
├── core/                 共通の部品（端末内データベース・時計・ID）
├── features/
│   ├── auth/             ログイン
│   ├── practice/         練習記録・タイマー・集計
│   ├── sync/             クラウド同期・競合の解決
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

Firestore のセキュリティルールのテスト（Java が必要）：

```bash
cd practice-app/rules-test
npm ci
npm test
```

プルリクエストでは GitHub Actions（`.github/workflows/practice-app.yml`）が書式・静的解析・テスト・Web ビルド・ルールのテストを確認します。
main に入ると、Web アプリと Firestore ルールを Firebase（kco-practice）に公開します（下の「自動公開の設定」が必要）。

## 設定と今後の予定

### 自動公開の設定（初回のみ）

Firebase プロジェクト `kco-practice` は作成済みです（Authentication：Google・メールアドレス、Firestore：作成済み）。
Web アプリ（`https://kco-practice.web.app`）と Firestore ルールを GitHub Actions から公開するには、鍵を1つ登録します。

1. [Google Cloud コンソールのサービスアカウント](https://console.cloud.google.com/iam-admin/serviceaccounts?project=kco-practice)で「サービスアカウントを作成」
   - 名前：`github-deploy` など
   - ロール：「Firebase 管理者」（Firebase Admin）と「Service Usage ユーザー」（Service Usage Consumer）
2. 作ったサービスアカウント →「鍵」→「鍵を追加」→「新しい鍵を作成」→ JSON をダウンロード
3. GitHub のリポジトリ →「Settings」→「Secrets and variables」→「Actions」→「New repository secret」
   - Name：`FIREBASE_SERVICE_ACCOUNT_PRACTICE`
   - Secret：ダウンロードした JSON の中身をすべて貼り付け
4. ダウンロードした JSON ファイルはパソコンから削除する（鍵は GitHub の Secrets にだけ置く）

鍵を登録するまでは、main に入っても公開だけを飛ばします（警告が出ます）。
**ルールを公開するまでは、クラウド同期は「同期できませんでした」になります**（Firestore が初期状態ではすべて拒否するため）。
急ぐときは、Firebase コンソールの「Firestore Database」→「ルール」に `firestore.rules` の中身を貼り付けて「公開」しても構いません。

### Android・iOS のクラウド同期

Android・iOS はまだ Firebase にアプリを登録していないので、端末内だけで動きます。
実機で確認するときに `flutterfire configure` でアプリを登録し、`lib/firebase_options.dart` を作り直します。

### Web 版の日本語フォント

Flutter の Web 版は、日本語のフォントをインターネットから読み込みます。完全にオフラインだと文字が正しく出ない場合があるので、
フォントをアプリに同梱するかどうかを今後検討します。

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
