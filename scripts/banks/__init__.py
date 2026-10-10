"""作問バンク（問題マスター JSON の生成元）。

各モジュールは PHASE（1〜5）と SETS（問題セット定義のリスト）を持つ。
generate_batch.py がこれを読み込み、スキーマ準拠の JSON を data/ 以下に書き出す。

フェーズ
  1: パイロット（中学5教科×各1単元・神奈川県公立高校入試型模試）
  2: 中学生版 全単元・特色検査対策
  3: 高校生向け 基礎科目 自習プリント
  4: 大学入学共通テスト 対策
  5: 難関大 個別試験（二次試験）対策
"""
PHASE_MODULES = {
    1: ["pilot_math", "pilot_english", "pilot_science", "pilot_social", "pilot_japanese", "pilot_mock"],
    2: ["jh_math", "jh_english", "jh_japanese", "jh_science", "jh_social", "jh_tokushoku"],
    3: ["hs_math", "hs_english", "hs_japanese", "hs_science", "hs_social"],
    4: ["common_test"],
    5: ["second_stage"],
}
