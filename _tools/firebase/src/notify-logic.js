// お知らせの受け取り登録：入力の検証（ブラウザに依存しない部分。test/logic.test.js でテスト）
// 条件は firestore.rules の isValidSignup と同じにしてください。

export const TOPICS = {
  concert: "演奏会の日程・会場が決まったとき",
  session: "説明会・見学会の案内",
  recruit: "団員募集の大切なお知らせ",
};

const EMAIL_RE = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;

/** 入力値を検証し、保存するデータとエラーの一覧を返す（テスト用に分けている） */
export function buildSignup({ email, topics, consent }) {
  const errors = [];
  const mail = String(email || "").trim();
  if (!mail) errors.push({ id: "nt-email", message: "メールアドレスを入力してください。" });
  else if (mail.length > 254 || !EMAIL_RE.test(mail)) {
    errors.push({ id: "nt-email", message: "メールアドレスの形式を確認してください（例：name@example.com）。" });
  }
  const picked = [...new Set(topics || [])].filter((t) => Object.prototype.hasOwnProperty.call(TOPICS, t));
  if (!picked.length) errors.push({ id: "nt-topics", message: "受け取りたいお知らせを1つ以上選んでください。" });
  if (!consent) errors.push({ id: "nt-consent", message: "メールアドレスの取り扱いを確認し、チェックを入れてください。" });
  return { errors, data: { email: mail, topics: picked, consent: true } };
}
