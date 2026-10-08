// リポジトリのルールをそのまま使ったテスト
// 成人の確認者が未登録の状態では、確定・公開・受付開始・返金承認が誰にもできないことを確認する
import { describe, it, before, after, beforeEach } from "node:test";
import { assertFails, assertSucceeds } from "@firebase/rules-unit-testing";
import { doc, setDoc, serverTimestamp } from "firebase/firestore";
import { setupEnv, as, baseRecord, recordBatch, baseReport, reportBatch, ADMIN, REVIEWER } from "./helpers.js";

let env;

before(async () => {
  env = await setupEnv("demo-kco", { withReviewer: false });
});
after(async () => {
  await env?.cleanup();
});
beforeEach(async () => {
  await env.clearFirestore();
});

describe("確認者が未登録の状態（公開時の初期状態）", () => {
  it("確認者のつもりのアカウントでも、会計報告を確認済みにできない", async () => {
    await reportBatch(as(env, ADMIN), ADMIN, "rep", baseReport(), { create: true });
    for (const who of [ADMIN, REVIEWER]) {
      await assertFails(reportBatch(as(env, who), who, "rep", baseReport({ status: "confirmed", confirmedAt: serverTimestamp() })));
    }
  });

  it("誰も申込みの受付を開始できない", async () => {
    for (const who of [ADMIN, REVIEWER]) {
      await assertFails(setDoc(doc(as(env, who), "settings", "sponsorship"), {
        acceptingApplications: true, benefitsConfirmed: true,
        benefits: { standard: "", preferred: "", special: "" }, updatedAt: serverTimestamp(),
      }));
    }
  });

  it("誰も返金を承認できない", async () => {
    const db = as(env, ADMIN);
    await recordBatch(db, ADMIN, "r1", baseRecord(), { create: true });
    const paid = baseRecord({ status: "payment_confirmed", paidAmount: 3000, paymentConfirmedOn: "2026-10-05" });
    await assertSucceeds(recordBatch(db, ADMIN, "r1", paid));
    await assertFails(recordBatch(db, ADMIN, "r1", { ...paid, status: "cancelled", refundAmount: 3000, refundApprovedOn: "2026-11-01" }));
  });
});
