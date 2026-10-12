# 公開の手順（練習お助け）

Web 版は GitHub Actions で自動公開できます。Android・iOS のストア公開は、運営のアカウントで行う作業があります。
ここでは、運営が行う作業を順番にまとめます。

## 0. 公開前のチェックリスト

- [ ] Firestore のルールを公開した（`practice-app/firestore.rules`。README「自動公開の設定」）
- [ ] 自動公開の鍵（GitHub Secrets の `FIREBASE_SERVICE_ACCOUNT_PRACTICE`）を登録した → Web 版が `https://kco-practice.web.app` に出る
- [ ] プライバシーポリシーが `https://kco-practice.web.app/privacy.html` で見られる
- [ ] Android・iOS のアプリを Firebase に登録した（スマホでもログイン・同期を使う場合。下の「3」）
- [ ] 実機で、メトロノーム・基準音・チューナー・録音を試した（音量・マイク・Bluetooth イヤホン）
- [ ] （任意）Web 版で AI コーチを使う場合、Chrome のオリジントライアルのトークンを入れた（README「端末内 AI」）

## 1. Web 版

main に入ると、GitHub Actions が Web 版と Firestore ルールを公開します（鍵の登録が必要。README「自動公開の設定」）。
公開先：`https://kco-practice.web.app`（スマホのブラウザで「ホーム画面に追加」すると、アプリのように使えます）

## 2. Android（Google Play）

### 2-1. 開発者登録（初回のみ・有料）
[Google Play Console](https://play.google.com/console) で開発者アカウントを作ります（登録料が必要。団体の場合は組織として登録）。

### 2-2. 署名の鍵を作る（初回のみ・パソコンで）
```powershell
# Windows（PowerShell）。Android Studio に付いてくる keytool を使う
keytool -genkey -v -keystore $HOME\kco-practice-upload.jks -keyalg RSA -keysize 2048 -validity 10000 -alias upload
```
`practice-app/android/key.properties` を作り、次のように書きます（**このファイルと .jks は絶対にコミットしない**。`.gitignore` 済み）。
```properties
storePassword=作ったパスワード
keyPassword=作ったパスワード
keyAlias=upload
storeFile=C:\\Users\\あなたの名前\\kco-practice-upload.jks
```
鍵とパスワードをなくすと、アプリを更新できなくなります。安全な場所に控えを保管してください。

`key.properties` がない・項目が足りない・鍵のファイルが見つからないときは、リリース版（`--release`）のビルドは**わざと失敗します**（デバッグ用の鍵で署名されたアプリを、誤って公開候補にしないため）。手元でリリース版の動きだけ確かめたいときは、次のようにするとデバッグ用の鍵で作れます（このアプリは公開に使えません）。
```powershell
$env:KCO_ALLOW_DEBUG_SIGNED_RELEASE = "1"; flutter run --release
```

### 2-3. ビルドして登録
```powershell
cd practice-app
flutter build appbundle --release
```
できた `build\app\outputs\bundle\release\app-release.aab` を Play Console にアップロードし、まず「内部テスト」で団員に配って確かめてから公開します。

### 2-4. ストアの掲載情報（下書き）
- アプリ名：練習お助け（かながわコネクトオーケストラ）
- 短い説明：トランペットの練習メニュー・タイマー・チューナー・メトロノーム・録音分析
- 説明：
  > かながわコネクトオーケストラの楽器練習お助けアプリです。
  > ・練習メニューを時間のルールに沿って組み立て（Arban の章ごとに選べます）、タイマーで計って記録
  > ・今日の予定と調子から、練習の量をすすめます（合奏・本番・疲れ）
  > ・チューナー（純正律にも対応）、メトロノーム、クリックトラック、基準音
  > ・ロングトーンを録音して、音程と音量の安定を分析
  > ・端末に内蔵の AI が、メニューの相談にのります（対応機種のみ。AI は端末の中だけで動きます）
  > ・ログインすると、ほかの端末と記録を同期できます（ログインしなくても使えます）
- カテゴリ：音楽＆オーディオ（または 教育）
- プライバシーポリシー：`https://kco-practice.web.app/privacy.html`

### 2-5. データセーフティ（Play Console の申告）
| 項目 | 回答 |
|---|---|
| 収集するデータ | 個人情報：メールアドレス・名前（ログインした場合のみ）／アプリのアクティビティ：アプリ内のその他の操作（練習記録。ログインした場合のみ） |
| 目的 | アプリの機能（アカウント管理・同期） |
| 共有 | なし |
| 暗号化 | 転送時に暗号化（HTTPS） |
| 削除の依頼 | できる（お問い合わせページから） |
| マイク | 使う。音声は端末内だけで処理し、収集しない |

## 3. スマホでのログイン・同期（Firebase への登録）

パソコンで次を実行します（Firebase CLI と FlutterFire CLI が必要）。
```powershell
npm install -g firebase-tools
dart pub global activate flutterfire_cli
firebase login
cd practice-app
flutterfire configure --project=kco-practice --platforms=android,ios,web
```
`lib/firebase_options.dart` が作り直されるので、コミットしてプルリクエストにします（中身は公開されても問題ない識別子です）。
Android の Google ログインには、Firebase コンソールで Android アプリに **SHA-1 フィンガープリント**（2-2 の鍵と、Play Console の「アプリの署名鍵」の両方）を登録します。

## 4. iOS（App Store）

- Mac と Xcode、[Apple Developer Program](https://developer.apple.com/programs/)（年会費が必要）が必要です。
- Mac で `cd practice-app && flutter build ipa` を実行し、Xcode の Organizer（または Transporter）から App Store Connect にアップロードします。
- まず TestFlight で団員に配って確かめてから公開します。
- 「App のプライバシー」は 2-5 と同じ内容で申告します（マイクは「収集しない」）。

## 5. 版を上げるとき

`practice-app/pubspec.yaml` の `version: 1.0.0+1` を上げ（`+` の後ろの数字はストアに出すたびに必ず増やす）、
`lib/app/app_info.dart` の `appVersion` も同じにします（テストで一致を確かめています）。
