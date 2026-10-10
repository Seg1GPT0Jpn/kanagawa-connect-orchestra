# 教材制作パイプライン（問題マスター → 自動検査 → PDF）

中学生5教科・高校主要科目・入試対策の問題データ（JSON マスター）を管理し、自動検査を通したうえで
印刷用・タブレット閲覧用の PDF 教材を生成するための仕組みです。
Web サイト本体とは独立しており、ここで扱うディレクトリは `firebase.json` の `ignore` で公開対象から外しています。

## ディレクトリ構成

```
schemas/
  curriculum_map.json      単元マスター（学習指導要領にもとづく階層的な単元マップ・各種コードの定義）
  question_schema.json     問題セット JSON のスキーマ（JSON Schema 2020-12）
data/                      マスターデータ（1ファイル＝1問題セット）
  pilot/                   パイロット（5教科×20問）と 5教科オリジナル模試、レビュー記録 REVIEW.md
  junior_high/             中学生版 全単元（教科別）、tokushoku/ 特色検査対策
  high_school/             高校 自習プリント（科目別）
  hs_packs/                高校 単元パック（単元ごとに lesson.json＝授業プリント、exercise.json＝問題プリント）
  common_test/             大学入学共通テスト対策
  second_stage/            難関大 個別試験（二次試験）対策
templates/
  question_template.html   問題冊子テンプレート（大問・資料・図・表・選択肢・解答欄・解答用紙）
  answer_template.html     解答・解説冊子テンプレート（配点表・解答一覧・解説・採点基準）
  lesson_print_template.html    授業プリント（教師用：指導の流れ・口頭解説のポイント／生徒用：板書を写す欄・メモ欄）
  exercise_print_template.html  問題プリント（A〜D の4段階・観点タグ／解答解説：思考の糸口・別解・部分点・誤答分析）
  _layout.html / _macros.html / print.css   共通レイアウト・部品・印刷用 CSS
  vendor/katex/            数式組版ライブラリ KaTeX（MIT License）
scripts/
  validate_questions.py    自動検査（スキーマ・必須項目・整合性・重複/類似・検算・LaTeX）
  build_pdf.py             PDF 生成（Chromium + KaTeX、レイアウト検査・PDF 検査つき）
  generate_batch.py        作問バンク → JSON 生成 → 検査 → PDF → カタログ をフェーズ単位で一括実行
  generate_highschool_unit.py   高校 単元パック（授業プリント＋問題プリント 50〜100問以上）を生成
  hs_pack_lib.py           単元パックの作問ライブラリ（授業プリントの部品・問題ジェネレータの登録と配分）
  hs_packs/                単元パックのモジュール（1単元1ファイル）
  banks/                   作問バンク（問題の生成元。フェーズごとのモジュール）
  tests/                   検査スクリプトのテストとダミー JSON
output/                    生成物（PDF・CATALOG.md・reports/phase*_report.json）
```

## 準備

```bash
pip install -r scripts/requirements.txt
# Chromium：Playwright のブラウザ、または環境変数 CHROMIUM_PATH で実行ファイルを指定
# 日本語フォント：IPA明朝・IPAゴシック（TrueType）を推奨（なければ Noto CJK でも可）
#   Debian/Ubuntu: apt-get install fonts-ipafont-mincho fonts-ipafont-gothic
```

IPA フォントを優先するのは、Chromium が OTF（CFF）形式の CJK フォントを Type3 として埋め込み、
PDF の肥大化やテキスト抽出の不具合（文字化け）を起こすためです。`build_pdf.py` は日本語フォントがない環境ではビルドを中止し、
Type3 フォントが埋め込まれた場合は警告します。

## よく使うコマンド

```bash
# 自動検査（data/ 全体。エラーがあれば終了コード 1、--strict で警告も不合格）
python scripts/validate_questions.py
python scripts/validate_questions.py data/pilot --strict

# PDF 生成（検査に通らないセットはビルドしない）
python scripts/build_pdf.py data/pilot/math_unit01.json
python scripts/build_pdf.py --unit JH-MATH-G2-U03            # 単元 ID で指定
python scripts/build_pdf.py data/junior_high --paper tablet   # A4 / B5 / tablet

# フェーズ単位のバッチ生成（JSON 生成 → 検査 → auto_checked 付与 → PDF → カタログ・レポート）
python scripts/generate_batch.py --phase 1 --tablet
python scripts/generate_batch.py --phase 2 3 4 5
python scripts/generate_batch.py --phase 2 --only JH-MATH-G1-U01-S1 --note "レビュー指摘 No.3 対応"

# テスト
python -m unittest discover -s scripts/tests
```

## 自動検査の内容（validate_questions.py）

| 区分 | 内容 |
|---|---|
| json_syntax / encoding | JSON 構文エラー（行・列）、UTF-8 でない、BOM、U+FFFD・制御文字（文字化け） |
| schema | `question_schema.json` への適合（型・必須・列挙値・難易度と点数の対応など） |
| required | ID・正答・解説・難易度・採点基準・単元・技能・検証状態・著作権状態の欠落や空値 |
| consistency / curriculum | ID の重複と命名規則、単元 ID の実在、資料・大問の参照切れ、教科の不一致 |
| answer | 選択式の正答が選択肢にあるか、選択肢の重複、並べ替えの正答の妥当性 |
| scoring | 配点合計と `total_points`、採点基準の合計と配点 |
| calc_check | `calc_check` の式を sympy で安全に評価して期待値と照合。数値・短答問題では正答とも照合（`target: "intermediate"` で除外） |
| latex | `$` の対応、波かっこ・`\left`/`\right`・`\begin`/`\end` の対応、KaTeX で描画できない書き方 |
| duplicate / similar | 正規化テキストの SHA-256 で同一問題（エラー）、文字 3-gram の Jaccard 係数（MinHash-LSH で候補抽出）で類似問題（既定 0.85 以上で警告） |
| revision / verification / copyright | 版番号の昇順・日付、`draft`・`rejected` の残存、権利処理未了 |

エラーは `ファイル:行: ERROR [区分] JSONパス: 理由` の形式で表示します。

## 問題データの作り方

問題は `scripts/banks/*.py` に短い関数呼び出しで書き、`generate_batch.py` がスキーマ準拠の JSON に展開します
（書き方は `scripts/banks/_common.py` の冒頭を参照）。

- 選択肢は正答を先頭に書く。出力時にセット ID と問題番号から決まる順序でシャッフルするので、解説で記号（ア・イ…）を使わない。
- 計算を含む問題には `chk=("式", "期待値")` を付ける（検算）。丸めた値を答えさせる場合は式の中で丸める（例: `floor(x*10+Rational(1,2))/10`）。
- 並べ替え問題は文頭の語も小文字で示す。単位記号は `20\,{}^\circ\mathrm{C}` のように書く。
- 読解の本文はオリジナルで書く。古典はパブリックドメインの作品を使い、`cp="public_domain"` と出典を記録する。
- 統計資料は出典を確認できる実データか、「架空の資料」と明記したデータを使う。

`data/` の JSON を直接編集してもかまいません。ただしバンクから再生成すると上書きされるため、恒久的な修正はバンク側に入れてください。

## 高校 単元パック（generate_highschool_unit.py）

高校の1単元を「授業プリント」と「問題プリント」の2つの独立したセットとして作ります。どちらも `pack_id` と
`pair_set_id` で対になり、`unit_context` に前提条件（Prerequisites）と発展・応用への接続（`curriculum_map.json` の高校全単元に定義）を持ちます。

```bash
python scripts/generate_highschool_unit.py --list
python scripts/generate_highschool_unit.py --unit HS-MATH1-U03              # 既定 60 問
python scripts/generate_highschool_unit.py --unit HS-MATH1-U04 --count 100
python scripts/generate_highschool_unit.py --all --no-pdf --note "レビュー指摘対応"
```

| 出力（output/hs_packs/<単元>/） | 内容 |
|---|---|
| `lesson_teacher.pdf` | 授業プリント 教師用：指導の流れ、概念導入、定義・定理、証明・導出、図解つき例題と解答、板書案、口頭で解説すべきポイント（発問・予想反応・注意）、典型的な誤概念 |
| `lesson_student.pdf` | 授業プリント 生徒用：例題の解答欄・メモ欄・確認問題の解答欄（教師用の指導メモは載せない） |
| `exercise_questions.pdf` | 問題プリント：A 基本確認／B 標準演習／C 思考力・記述応用／D 典型誤答訂正、各問に観点タグ |
| `exercise_answers.pdf` | 解答解説：正答一覧、思考の糸口、解法、別解、部分点の基準、選択肢ごとの誤りの理由、誤答例の分析、よくあるミス |

観点タグ（`perspectives`）は 計算力反復 `computation`／定義・公式の条件確認 `condition_check`／複数単元融合 `cross_unit`／
記述・論証・途中式 `written_reasoning`／典型ミス `common_error` を必須とし、`concept`・`application`・`multiple_solutions` も使えます。

新しい単元は `scripts/hs_packs/<単元>.py` に `UNIT_ID`・`LESSON`・`GENERATORS` を定義して追加します（書き方は `hs_pack_lib.py` の冒頭と既存モジュールを参照）。
ジェネレータはパラメータを変えて問題を作り、同じ問題文は自動で除かれます。`--count` に対して変種が足りない場合はエラーで知らせます。

パック固有の自動検査（`print_type` が lesson / exercise のセット）：授業プリントに導入・定義/定理・証明/導出・例題・板書案・指導ガイドがそろっているか、
口頭解説ポイントが5つ以上あるか。問題プリントが50問以上か、4段階と必須の観点がすべてあるか、各問に段階・観点・詳細解説（糸口・手順・別解・部分点）があるか、
選択式で誤答の選択肢すべてに誤りの理由があるか、典型誤答訂正の問題に誤答分析があるか、部分点の合計が配点を超えないか。

作成済みの単元パック：`HS-MATH1-U03`（二次関数）、`HS-MATH1-U04`（図形と計量）。いずれも 100 問まで検査に合格することを確認済みです。

## 版管理と検証状態

- `revision_history`：`generate_batch.py` が内容のハッシュを比較し、内容が変わったときだけ版を上げて変更概要（追加・削除・修正した問題番号、`--note` の理由）を記録します。
- `verification.status`：生成直後は `draft`。自動検査に合格すると `auto_checked` になります。
  教科担当者がレビューしたら `expert_reviewed`（さらに公開承認で `approved`）に更新してください。
  内容が変わらない限り再生成してもレビュー状態は引き継がれ、内容を修正した問題は `draft` に戻ります。
- `validation`：最後の自動検査の結果（日時・バージョン・合否・内容ハッシュ）。

**現在のすべての問題は `auto_checked`（AI が作成し自動検査に合格）であり、教科担当者による内容レビューは未実施です。**
授業や配布に使う前に、必ず専門家の確認を受けてください。

## ID の規則

- 単元 ID：`{段階}-{教科/科目}-[G{学年}-]U{2桁}`（例 `JH-MATH-G2-U03`、`HS-MATH1-U04`、`CT-ENG-U01`、`SS-JPN-U02`、`EX-KNG-MOCK-SCI`）
- セット ID：単元プリントは `{単元ID}-S1`。パイロットは `PILOT-{教科}-U01`、模試は `KNG-MOCK-R8-01`
- 問題 ID：`{セットID}-Q{3桁}`
