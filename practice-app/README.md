# 練習お助けアプリ（practice-app）

かながわコネクトオーケストラの楽器練習お助けアプリです。Flutter で Android・iOS・PC ブラウザ（Web）に対応します。

- **AI は端末内（ローカル）だけで動かします。** 外部のクラウド AI は使いません（プライバシー保護・オフライン利用・費用ゼロのため）。
- **時間計算・ルール検査・集計はプログラム（Dart）が決定論的に行います。** AI は提案や文章づくりの補助だけで、AI の出力は必ずプログラムの検査を通してから使います。
- **AI が使えない端末でも、** 練習記録・タイマー・テンプレート・メニュー監査はすべて動きます。

## できること

| 機能 | 場所 |
|---|---|
| 練習タイマー（メニューの項目を順に計る・一時停止・途中で終える） | `lib/features/practice/` |
| 練習記録（端末内に保存・メモ・削除）と集計（今日・直近7日・連続日数・項目別） | `lib/features/practice/` |
| メニュー：時間のルールの決定論的監査・修正案・時間モード（通常・20分・10分）・今日の重点・Arban の章 | `lib/features/menu/` |
| 今日の予定と調子からのすすめ（合奏・本番・疲れ・唇の痛み） | `lib/features/practice/domain/day_condition.dart` |
| AI コーチ（端末・ブラウザに内蔵の AI。メニューの相談・ひとことアドバイス） | `lib/features/local_ai/` |
| チューナー（YIN 法・B♭管などの移調表示・純正律などの音律） | `lib/features/audio_tools/` |
| メトロノーム・クリックトラック（テンポ・拍子が変わる曲）・基準音 | `lib/features/audio_tools/` |
| 録音と簡易音響分析（ロングトーンの音程・音量の安定、グラフ） | `lib/features/recording/` |
| 記録の書き出し（CSV・バックアップ JSON）と読み込み | `lib/features/data_io/` |
| ログイン（Google・メールアドレス）※ログインしなくても使える | `lib/features/auth/` |
| クラウド同期（オフライン対応・競合の解決） | `lib/features/sync/` |
| Firestore のセキュリティルールとテスト | `firestore.rules`・`rules-test/` |
| このアプリについて・プライバシーポリシー（`web/privacy.html`） | `lib/app/about_page.dart` |

公開の手順（Web・Google Play・App Store、ストアの掲載情報の下書き、データの申告内容）は [docs/release.md](docs/release.md)、
開発の進み具合は [docs/progress.md](docs/progress.md) を参照してください。

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

時間モードを3つから選べます（メニュータブ）。どのモードも項目は同じで、範囲だけが変わります。

| 項目 | 通常 | 20分 | 10分 |
|---|---|---|---|
| ウォームアップ（呼吸・バズィング） | 3〜10分（初期値5） | 2〜5分 | 1〜3分 |
| ロングトーン | 10〜20分（15） | 3〜10分 | 2〜5分 |
| リップスラー | 0〜15分（5） | 0〜5分 | 0〜5分 |
| タンギング | 0〜10分（5） | 0〜5分 | 0〜3分 |
| **Arban（12の章の合計）** | **20〜40分**（30：スラー・音階・タンギング各10） | 0〜15分 | 0〜10分 |
| 曲・エチュード | 0〜40分（20） | 0〜15分 | 0〜10分 |
| **合計** | **45〜115分**（80） | **15〜25分**（20） | **5〜15分**（10） |

- Arban は 1893年版の分類で12の章（初歩練習・シンコペーション・スラー・音階・半音階・装飾音・音程跳躍・タンギング・
  フレージング・二重奏・性格的練習曲・幻想曲／変奏曲）に分け、0分＝お休みで、その日に鍛えたい章を選びます。
- 通常モードでは「今日の重点」から、調査をもとにしたおすすめ（バランス・短め・音色／柔軟性・指／音階・タンギング・表現／曲・長め）を選べます。
- 練習タブの「今日の予定と調子」（合奏・レッスン／本番／昨日たくさん吹いた／唇が痛い／疲れ具合）から、
  時間モード・おすすめ・休息を決まったルールですすめます（`lib/features/practice/domain/day_condition.dart`）。
  すすめを選ぶと「今日だけのメニュー」になり、保存したメニューは変わりません。調子は端末内にだけ保存します。
- 調査の分析と、ルールを決めた経緯は [docs/practice-research.md](docs/practice-research.md) を参照してください。

ルールを変えるときは `lib/features/menu/domain/menu_rules.dart` を直し、`test/features/menu/menu_audit_test.dart` の
「仕様どおりの範囲」「時間モード」も合わせて直してください。おすすめ（`menu_presets.dart`）がルールを満たさないとテストで失敗します。

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
│   ├── local_ai/         端末内 AI（AI コーチ・使えないときの代わり）
│   ├── audio_tools/      チューナー・メトロノーム・クリックトラック・基準音・音律
│   ├── recording/        録音と簡易音響分析
│   └── data_io/          記録の書き出し・読み込み
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

### 端末内 AI（AI コーチ）

費用のかからない、**端末・ブラウザに内蔵の AI** を使います（[flutter_local_ai](https://pub.dev/packages/flutter_local_ai)。モデルのファイルは配りません）。

| 端末 | 使う AI | 条件 |
|---|---|---|
| Android | Gemini Nano（ML Kit GenAI / AICore） | Pixel 9 以降・Galaxy S25 以降など対応機種。初回に端末が AI を準備（ダウンロード） |
| iPhone | Apple Foundation Models | iPhone 15 Pro 以降・iOS 26 以降で、Apple Intelligence をオン |
| Web | Chrome・Edge の Prompt API | パソコン版のみ。**オリジントライアルのトークンが必要**（下記） |

- 練習タブの「AI コーチ」で、今日の調子と直近7日の記録から「メニューの相談」「ひとことアドバイス」ができます。
- AI のメニュー案は JSON で受け取り、アプリが時間のルールを確かめます。違反していればアプリが直した案を出します（`lib/features/local_ai/practice_coach.dart`）。
- 対応していない端末では「使えません」と表示するだけで、ほかの機能はそのまま使えます。
- AI は端末の中だけで動き、記録を外に送りません。

**Web 版でAIを使う準備（公開 URL が決まってから）**：[Chrome のオリジントライアル](https://developer.chrome.com/origintrials/) で「Prompt API」に公開 URL（例：`https://kco-practice.web.app`）を登録し、発行されたトークンを `web/index.html` の `<head>` に
`<meta http-equiv="origin-trial" content="発行されたトークン">` として追加します（無料）。
