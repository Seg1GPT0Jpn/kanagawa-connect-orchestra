// Firestore Security Rules のテスト（Firestore エミュレーター上で実行）
// 実行方法：_tools/firebase で `npm test`
import { describe, it, before, after, beforeEach } from "node:test";
import { assertFails, assertSucceeds } from "@firebase/rules-unit-testing";
import {
  doc, getDoc, getDocs, setDoc, updateDoc, deleteDoc, addDoc, collection, query, where,
  serverTimestamp, writeBatch,
} from "firebase/firestore";
import {
  setupEnv, as, newId, baseRecord, recordBatch, baseReport, reportBatch,
  ADMIN, REVIEWER, STRANGER,
} from "./helpers.js";
import { publicEntryFromRecord } from "../src/sponsor-logic.js";

let env;

before(async () => {
  env = await setupEnv("demo-kco");
});
after(async () => {
  await env?.cleanup();
});
beforeEach(async () => {
  await env.clearFirestore();
});

const paid = (o = {}) => baseRecord({
  status: "payment_confirmed", paidAmount: 3000, paymentConfirmedOn: "2026-10-05", ...o,
});
const listed = (o = {}) => paid({
  status: "listed", consentListing: true, consentRecordedOn: "2026-10-02", listingStart: "2026-10-10", ...o,
});

// 入金確認済み・掲載中の記録をテスト用に用意する（ルールを通して作成）
async function seedRecord(id, rec, pub) {
  const db = as(env, ADMIN);
  await recordBatch(db, ADMIN, id, baseRecord({ ...rec, status: "received", paidAmount: 0, paymentConfirmedOn: "" }), { create: true });
  if (rec.status !== "received") await recordBatch(db, ADMIN, id, rec, { public: pub });
}

async function openApplications() {
  await env.withSecurityRulesDisabled(async (ctx) => {
    await setDoc(doc(ctx.firestore(), "settings", "sponsorship"), {
      acceptingApplications: true, benefitsConfirmed: true,
      benefits: { standard: "a", preferred: "b", special: "c" }, updatedAt: new Date(),
    });
  });
}

function application(o = {}) {
  return {
    createdAt: serverTimestamp(), kind: "individual", contactName: "申込 花子", orgName: "",
    email: "hanako@example.com", units: 2, listing: "named", displayName: "申込花子",
    websiteUrl: "", message: "", consentListing: true, consentPrivacy: true, ageConfirmed: true, ...o,
  };
}

// ================================================================ 1〜3：権限のない利用者
describe("権限のない利用者（テスト要件1・2・3）", () => {
  it("未ログイン・一般ユーザーは協賛記録・申込み・履歴を読めない", async () => {
    await seedRecord("r1", paid());
    for (const who of [null, STRANGER]) {
      const db = as(env, who);
      await assertFails(getDoc(doc(db, "sponsorRecords", "r1")));
      await assertFails(getDocs(collection(db, "sponsorRecords")));
      await assertFails(getDocs(collection(db, "sponsorRecords", "r1", "history")));
      await assertFails(getDocs(collection(db, "sponsorApplications")));
    }
  });

  it("未ログイン・一般ユーザーは協賛記録・公開一覧・設定・会計報告を書き換えられない", async () => {
    await seedRecord("r1", listed(), publicEntryFromRecord(listed()));
    for (const who of [null, STRANGER]) {
      const db = as(env, who);
      await assertFails(recordBatch(db, who || "", "r2", baseRecord(), { create: true }));
      await assertFails(updateDoc(doc(db, "sponsorRecords", "r1"), { paidAmount: 0 }));
      await assertFails(setDoc(doc(db, "publicSponsors", "x"), publicEntryFromRecord(listed())));
      await assertFails(deleteDoc(doc(db, "publicSponsors", "r1")));
      await assertFails(setDoc(doc(db, "settings", "sponsorship"), {
        acceptingApplications: true, benefitsConfirmed: true,
        benefits: { standard: "", preferred: "", special: "" }, updatedAt: serverTimestamp(),
      }));
      await assertFails(reportBatch(db, who || "", "rep", baseReport(), { create: true }));
    }
  });

  it("メールアドレス未確認のログインは管理者として扱わない", async () => {
    await seedRecord("r1", paid());
    const db = as(env, ADMIN, { verified: false });
    await assertFails(getDoc(doc(db, "sponsorRecords", "r1")));
  });

  it("一般ユーザーは下書きの会計報告を読めない", async () => {
    await reportBatch(as(env, ADMIN), ADMIN, "rep", baseReport(), { create: true });
    await assertFails(getDoc(doc(as(env, null), "financeReports", "rep")));
    await assertFails(getDocs(collection(as(env, STRANGER), "financeReports")));
  });

  it("存在しないコレクションへの読み書きは拒否される", async () => {
    await assertFails(setDoc(doc(as(env, ADMIN), "ledger", "x"), { a: 1 }));
    await assertFails(getDoc(doc(as(env, null), "ledger", "x")));
  });
});

// ================================================================ 協賛記録
describe("協賛記録（テスト要件6・8・9）", () => {
  it("運営管理者は申込受付の記録を作成でき、読み取れる", async () => {
    const db = as(env, ADMIN);
    await assertSucceeds(recordBatch(db, ADMIN, "r1", baseRecord(), { create: true }));
    await assertSucceeds(getDoc(doc(db, "sponsorRecords", "r1")));
  });

  it("入金済みの状態でいきなり記録を作ることはできない", async () => {
    await assertFails(recordBatch(as(env, ADMIN), ADMIN, "r1", paid(), { create: true }));
  });

  it("入金前の状態で入金額を入れることはできない", async () => {
    await assertFails(recordBatch(as(env, ADMIN), ADMIN, "r1",
      baseRecord({ paidAmount: 3000 }), { create: true }));
  });

  it("入金確認済みには入金額と入金確認日が必要", async () => {
    const db = as(env, ADMIN);
    await recordBatch(db, ADMIN, "r1", baseRecord(), { create: true });
    await assertFails(recordBatch(db, ADMIN, "r1", paid({ paymentConfirmedOn: "" })));
    await assertFails(recordBatch(db, ADMIN, "r1", paid({ paidAmount: 0 })));
    await assertSucceeds(recordBatch(db, ADMIN, "r1", paid()));
  });

  it("口数から掲載ランクと金額が正しく判定されないと保存できない", async () => {
    const db = as(env, ADMIN);
    const cases = [
      [{ units: 4, amount: 4000, rank: "standard" }, true],
      [{ units: 5, amount: 5000, rank: "preferred" }, true],
      [{ units: 9, amount: 9000, rank: "preferred" }, true],
      [{ units: 10, amount: 10000, rank: "special" }, true],
      [{ units: 5, amount: 5000, rank: "standard" }, false],
      [{ units: 10, amount: 10000, rank: "preferred" }, false],
      [{ units: 3, amount: 2000, rank: "standard" }, false],
      [{ kind: "organization", units: 2, amount: 20000, rank: "standard" }, true],
      [{ kind: "organization", units: 2, amount: 2000, rank: "standard" }, false],
      [{ units: 0, amount: 0, rank: "standard" }, false],
      [{ units: 1.5, amount: 1500, rank: "standard" }, false],
    ];
    for (const [o, ok] of cases) {
      const p = recordBatch(db, ADMIN, newId("r"), baseRecord(o), { create: true });
      await (ok ? assertSucceeds(p) : assertFails(p));
    }
  });

  it("履歴を同時に追加しない書き込みは拒否される", async () => {
    const db = as(env, ADMIN);
    await assertFails(recordBatch(db, ADMIN, "r1", baseRecord(), { create: true, history: { skip: true } }));
    await recordBatch(db, ADMIN, "r1", baseRecord(), { create: true, history: { id: "h1" } });
    // 過去の履歴IDを使い回す
    await assertFails(recordBatch(db, ADMIN, "r1", baseRecord({ notes: "x" }), { history: { id: "h1" } }));
    // 履歴の内容が記録と食い違う
    await assertFails(recordBatch(db, ADMIN, "r1", baseRecord({ notes: "x" }), { history: { data: { amount: 1 } } }));
    // 他人の名前で履歴を残す
    await assertFails(recordBatch(db, ADMIN, "r1", baseRecord({ notes: "x" }), { history: { data: { by: REVIEWER } } }));
  });

  it("記録と履歴は削除・改変できない", async () => {
    const db = as(env, ADMIN);
    await recordBatch(db, ADMIN, "r1", baseRecord(), { create: true, history: { id: "h1" } });
    await assertFails(deleteDoc(doc(db, "sponsorRecords", "r1")));
    await assertFails(deleteDoc(doc(db, "sponsorRecords", "r1", "history", "h1")));
    await assertFails(updateDoc(doc(db, "sponsorRecords", "r1", "history", "h1"), { note: "改ざん" }));
    await assertFails(deleteDoc(doc(as(env, REVIEWER), "sponsorRecords", "r1")));
  });

  it("運営管理者は返金を記録できず、入金済みの記録を取り消せない（成人の確認者のみ）", async () => {
    await seedRecord("r1", paid());
    const admin = as(env, ADMIN);
    await assertFails(recordBatch(admin, ADMIN, "r1", paid({ refundAmount: 3000, refundApprovedOn: "2026-11-01" })));
    await assertFails(recordBatch(admin, ADMIN, "r1", paid({ status: "cancelled" })));
    const rev = as(env, REVIEWER);
    await assertSucceeds(recordBatch(rev, REVIEWER, "r1",
      paid({ status: "cancelled", refundAmount: 3000, refundApprovedOn: "2026-11-01" })));
  });

  it("返金額は入金額を超えられない", async () => {
    await seedRecord("r1", paid());
    await assertFails(recordBatch(as(env, REVIEWER), REVIEWER, "r1",
      paid({ status: "cancelled", refundAmount: 3001, refundApprovedOn: "2026-11-01" })));
  });

  it("入金前の申込みは運営管理者が取り消せる", async () => {
    const db = as(env, ADMIN);
    await recordBatch(db, ADMIN, "r1", baseRecord(), { create: true });
    await assertSucceeds(recordBatch(db, ADMIN, "r1", baseRecord({ status: "cancelled" })));
  });

  it("危険なURL・ロゴのファイル名は保存できない", async () => {
    const db = as(env, ADMIN);
    const bad = [
      { websiteUrl: "javascript:alert(1)" },
      { websiteUrl: "http://example.com" },
      { websiteUrl: "https://example.com/\"><script>" },
      { websiteUrl: "https://user:pass@example.com" },
      { logoFile: "../index.html" },
      { logoFile: "logo.svg" },
      { logoFile: "https://evil.example/logo.png" },
    ];
    for (const o of bad) {
      await assertFails(recordBatch(db, ADMIN, newId("r"), baseRecord({ kind: "organization", amount: 30000, ...o }), { create: true }));
    }
    await assertSucceeds(recordBatch(db, ADMIN, newId("r"), baseRecord({
      kind: "organization", amount: 30000, websiteUrl: "https://example.co.jp/about", logoFile: "example-co.png",
    }), { create: true }));
  });
});

// ================================================================ 公開一覧
describe("協賛者一覧の公開（テスト要件4・5）", () => {
  it("掲載同意がない記録は掲載中にできない", async () => {
    await seedRecord("r1", paid());
    const rec = listed({ consentListing: false });
    await assertFails(recordBatch(as(env, ADMIN), ADMIN, "r1", rec, { public: publicEntryFromRecord(rec) }));
    const rec2 = listed({ consentRecordedOn: "" });
    await assertFails(recordBatch(as(env, ADMIN), ADMIN, "r1", rec2, { public: publicEntryFromRecord(rec2) }));
  });

  it("「掲載しない」を選んだ協賛者は掲載中にできない", async () => {
    await seedRecord("r1", paid({ listing: "none" }));
    const rec = listed({ listing: "none" });
    await assertFails(recordBatch(as(env, ADMIN), ADMIN, "r1", rec, { public: publicEntryFromRecord(rec) }));
  });

  it("入金額が協賛金額と一致しないと掲載中にできない", async () => {
    await seedRecord("r1", paid({ paidAmount: 2000 }));
    const rec = listed({ paidAmount: 2000 });
    await assertFails(recordBatch(as(env, ADMIN), ADMIN, "r1", rec, { public: publicEntryFromRecord(rec) }));
  });

  it("未入金の記録は掲載中にできない", async () => {
    await seedRecord("r1", baseRecord({ consentListing: true, consentRecordedOn: "2026-10-02" }));
    const rec = baseRecord({ status: "listed", consentListing: true, consentRecordedOn: "2026-10-02", listingStart: "2026-10-10" });
    await assertFails(recordBatch(as(env, ADMIN), ADMIN, "r1", rec, { public: publicEntryFromRecord(rec) }));
  });

  it("条件を満たせば掲載中にでき、誰でも公開一覧を読める", async () => {
    await seedRecord("r1", paid());
    const rec = listed();
    await assertSucceeds(recordBatch(as(env, ADMIN), ADMIN, "r1", rec, { public: publicEntryFromRecord(rec) }));
    const snap = await assertSucceeds(getDocs(collection(as(env, null), "publicSponsors")));
    const data = snap.docs[0].data();
    // 公開文書に個人情報や入金情報が含まれていない
    for (const k of ["email", "contactName", "paidAmount", "amount", "units", "paymentConfirmedOn", "notes", "internalId"]) {
      if (k in data) throw new Error(`公開文書に ${k} が含まれています`);
    }
  });

  it("掲載中にするとき、公開用の文書がないと拒否される", async () => {
    await seedRecord("r1", paid());
    await assertFails(recordBatch(as(env, ADMIN), ADMIN, "r1", listed()));
  });

  it("公開用の文書だけを単独で作ることはできない", async () => {
    await seedRecord("r1", paid());
    await assertFails(setDoc(doc(as(env, ADMIN), "publicSponsors", "r1"), publicEntryFromRecord(listed())));
  });

  it("匿名を選んだ協賛者の名前は公開文書に入れられない", async () => {
    await seedRecord("r1", paid({ listing: "anonymous" }));
    const rec = listed({ listing: "anonymous" });
    await assertFails(recordBatch(as(env, ADMIN), ADMIN, "r1", rec, {
      public: { ...publicEntryFromRecord(rec), displayName: rec.displayName },
    }));
    const ok = publicEntryFromRecord(rec);
    if (ok.displayName !== "" || ok.anonymous !== true) throw new Error("匿名の公開内容が正しくありません");
    await assertSucceeds(recordBatch(as(env, ADMIN), ADMIN, "r1", rec, { public: ok }));
  });

  it("掲載ランクに含まれない特典（URL・ロゴ・紹介文）は公開できない", async () => {
    const base = { kind: "organization", units: 3, amount: 30000, paidAmount: 30000, websiteUrl: "https://example.com", logoFile: "a.png", intro: "紹介" };
    await seedRecord("r1", paid(base));
    const rec = listed(base);
    await assertFails(recordBatch(as(env, ADMIN), ADMIN, "r1", rec, {
      public: { ...publicEntryFromRecord(rec), websiteUrl: "https://example.com" },
    }));
    await assertSucceeds(recordBatch(as(env, ADMIN), ADMIN, "r1", rec, { public: publicEntryFromRecord(rec) }));
  });

  it("掲載中でなくなるときは、公開用の文書も同時に削除しなければならない", async () => {
    await seedRecord("r1", listed(), publicEntryFromRecord(listed()));
    const ended = listed({ status: "listing_ended", listingEnd: "2027-03-31" });
    await assertFails(recordBatch(as(env, ADMIN), ADMIN, "r1", ended));
    await assertSucceeds(recordBatch(as(env, ADMIN), ADMIN, "r1", ended, { public: null }));
    const snap = await getDocs(collection(as(env, null), "publicSponsors"));
    if (!snap.empty) throw new Error("掲載終了後も公開文書が残っています");
  });

  it("掲載中の記録の表示名を変えるときは、公開用の文書も一致させる必要がある", async () => {
    await seedRecord("r1", listed(), publicEntryFromRecord(listed()));
    const renamed = listed({ displayName: "新しい名前" });
    await assertFails(recordBatch(as(env, ADMIN), ADMIN, "r1", renamed));
    await assertSucceeds(recordBatch(as(env, ADMIN), ADMIN, "r1", renamed, { public: publicEntryFromRecord(renamed) }));
  });
});

// ================================================================ 申込みフォーム
describe("協賛の申込み（テスト要件9）", () => {
  it("受付開始前は、申込みを送信できない", async () => {
    await assertFails(addDoc(collection(as(env, null), "sponsorApplications"), application()));
    await env.withSecurityRulesDisabled(async (ctx) => {
      await setDoc(doc(ctx.firestore(), "settings", "sponsorship"), {
        acceptingApplications: false, benefitsConfirmed: true,
        benefits: { standard: "", preferred: "", special: "" }, updatedAt: new Date(),
      });
    });
    await assertFails(addDoc(collection(as(env, null), "sponsorApplications"), application()));
  });

  it("受付開始後は送信できるが、一般ユーザーは読めない", async () => {
    await openApplications();
    const db = as(env, null);
    const ref = await assertSucceeds(addDoc(collection(db, "sponsorApplications"), application()));
    await assertFails(getDoc(ref));
    await assertFails(updateDoc(ref, { units: 100 }));
    await assertFails(deleteDoc(ref));
    await assertSucceeds(getDoc(doc(as(env, ADMIN), "sponsorApplications", ref.id)));
    await assertSucceeds(deleteDoc(doc(as(env, ADMIN), "sponsorApplications", ref.id)));
  });

  it("申込みに入金済みなどの項目を追加することはできない", async () => {
    await openApplications();
    const db = as(env, null);
    await assertFails(addDoc(collection(db, "sponsorApplications"), application({ status: "payment_confirmed" })));
    await assertFails(addDoc(collection(db, "sponsorApplications"), application({ paidAmount: 2000 })));
  });

  it("不正な申込み内容は拒否される", async () => {
    await openApplications();
    const db = as(env, null);
    const bad = [
      { consentPrivacy: false },
      { listing: "named", consentListing: false },
      { listing: "anonymous", displayName: "名前" },
      { websiteUrl: "https://example.com" }, // 個人はURL不可
      { kind: "organization", orgName: "株式会社テスト", websiteUrl: "javascript:alert(1)" },
      { kind: "organization", orgName: "" },
      { ageConfirmed: false },
      { units: 0 },
      { email: "not-an-email" },
    ];
    for (const o of bad) await assertFails(addDoc(collection(db, "sponsorApplications"), application(o)));
    await assertSucceeds(addDoc(collection(db, "sponsorApplications"), application({
      listing: "anonymous", displayName: "", consentListing: true,
    })));
    await assertSucceeds(addDoc(collection(db, "sponsorApplications"), application({
      listing: "none", displayName: "", consentListing: false,
    })));
    await assertSucceeds(addDoc(collection(db, "sponsorApplications"), application({
      kind: "organization", orgName: "株式会社テスト", displayName: "株式会社テスト",
      websiteUrl: "https://example.co.jp", ageConfirmed: false,
    })));
  });
});

// ================================================================ 設定
describe("協賛制度の設定", () => {
  const settings = (o = {}) => ({
    acceptingApplications: false, benefitsConfirmed: false,
    benefits: { standard: "氏名を掲載", preferred: "目立つ位置", special: "ロゴ" },
    updatedAt: serverTimestamp(), ...o,
  });

  it("運営管理者は特典の文言を保存できるが、確認済み・受付開始にはできない", async () => {
    const db = as(env, ADMIN);
    await assertSucceeds(setDoc(doc(db, "settings", "sponsorship"), settings()));
    await assertFails(setDoc(doc(db, "settings", "sponsorship"), settings({ benefitsConfirmed: true })));
    await assertFails(setDoc(doc(db, "settings", "sponsorship"), settings({ benefitsConfirmed: true, acceptingApplications: true })));
  });

  it("成人の確認者は特典を確認済みにし、受付を開始できる", async () => {
    await setDoc(doc(as(env, ADMIN), "settings", "sponsorship"), settings());
    const rev = as(env, REVIEWER);
    await assertFails(setDoc(doc(rev, "settings", "sponsorship"), settings({ acceptingApplications: true })));
    await assertSucceeds(setDoc(doc(rev, "settings", "sponsorship"), settings({ benefitsConfirmed: true, acceptingApplications: true })));
  });

  it("運営管理者は受付を停止できる。特典の文言を変えると確認済みが外れる", async () => {
    await setDoc(doc(as(env, ADMIN), "settings", "sponsorship"), settings());
    await setDoc(doc(as(env, REVIEWER), "settings", "sponsorship"), settings({ benefitsConfirmed: true, acceptingApplications: true }));
    const db = as(env, ADMIN);
    const changed = { standard: "変更", preferred: "目立つ位置", special: "ロゴ" };
    await assertFails(setDoc(doc(db, "settings", "sponsorship"), settings({ benefitsConfirmed: true, acceptingApplications: true, benefits: changed })));
    await assertSucceeds(setDoc(doc(db, "settings", "sponsorship"), settings({ benefitsConfirmed: true, acceptingApplications: false })));
    await assertSucceeds(setDoc(doc(db, "settings", "sponsorship"), settings({ benefits: changed })));
  });

  it("設定は誰でも読めるが、一般ユーザーは変更できない", async () => {
    await setDoc(doc(as(env, ADMIN), "settings", "sponsorship"), settings());
    await assertSucceeds(getDoc(doc(as(env, null), "settings", "sponsorship")));
    await assertFails(setDoc(doc(as(env, STRANGER), "settings", "sponsorship"), settings()));
  });
});

// ================================================================ 会計報告
describe("会計報告（テスト要件7・8）", () => {
  it("運営管理者は整合性のとれた下書きを作成できる", async () => {
    await assertSucceeds(reportBatch(as(env, ADMIN), ADMIN, "rep", baseReport(), { create: true }));
  });

  it("合計・残高が内訳と一致しない報告は保存できない", async () => {
    const db = as(env, ADMIN);
    await assertFails(reportBatch(db, ADMIN, newId("rep"), baseReport({ totalIncome: 99999 }), { create: true }));
    await assertFails(reportBatch(db, ADMIN, newId("rep"), baseReport({ totalExpense: 1 }), { create: true }));
    await assertFails(reportBatch(db, ADMIN, newId("rep"), baseReport({ closingBalance: 1 }), { create: true }));
    await assertFails(reportBatch(db, ADMIN, newId("rep"), baseReport({ carryover: 999999 }), { create: true }));
    await assertFails(reportBatch(db, ADMIN, newId("rep"), baseReport({ reserve: 20000 }), { create: true }));
    await assertFails(reportBatch(db, ADMIN, newId("rep"), baseReport({ expFees: -1 }), { create: true }));
    await assertFails(reportBatch(db, ADMIN, newId("rep"), baseReport({ expFees: 0.5 }), { create: true }));
  });

  it("公開資料にメールアドレスや口座番号のような数字を含められない", async () => {
    const db = as(env, ADMIN);
    await assertFails(reportBatch(db, ADMIN, newId("rep"), baseReport({ achievements: "連絡先 a@example.com" }), { create: true }));
    await assertFails(reportBatch(db, ADMIN, newId("rep"), baseReport({ achievements: "口座 1234567" }), { create: true }));
    await assertFails(reportBatch(db, ADMIN, newId("rep"), baseReport({ achievements: "口座 １２３４５６７" }), { create: true }));
  });

  it("運営管理者は確認済み・公開にできない（成人の確認者のみ）", async () => {
    const db = as(env, ADMIN);
    await reportBatch(db, ADMIN, "rep", baseReport(), { create: true });
    await assertSucceeds(reportBatch(db, ADMIN, "rep", baseReport({ status: "review_requested" })));
    await assertFails(reportBatch(db, ADMIN, "rep", baseReport({ status: "confirmed", confirmedAt: serverTimestamp() })));
    await assertFails(reportBatch(db, ADMIN, "rep", baseReport({ status: "published", publishedOn: "2027-05-01", confirmedAt: serverTimestamp() })));
  });

  it("確認を経ずに公開することはできない", async () => {
    await reportBatch(as(env, ADMIN), ADMIN, "rep", baseReport(), { create: true });
    await assertFails(reportBatch(as(env, REVIEWER), REVIEWER, "rep",
      baseReport({ status: "published", publishedOn: "2027-05-01", confirmedAt: serverTimestamp() })));
  });

  it("成人の確認者が確認・公開すると、誰でも読めるようになる", async () => {
    await reportBatch(as(env, ADMIN), ADMIN, "rep", baseReport(), { create: true });
    const rev = as(env, REVIEWER);
    await assertSucceeds(reportBatch(rev, REVIEWER, "rep", baseReport({ status: "confirmed", confirmedAt: serverTimestamp() })));
    await assertFails(getDoc(doc(as(env, null), "financeReports", "rep")));
    await assertSucceeds(reportBatch(rev, REVIEWER, "rep", { status: "published", publishedOn: "2027-05-01" }));
    await assertSucceeds(getDoc(doc(as(env, null), "financeReports", "rep")));
    await assertSucceeds(getDocs(query(collection(as(env, null), "financeReports"), where("status", "==", "published"))));
    await assertFails(getDocs(collection(as(env, null), "financeReports", "rep", "history")));
  });

  it("確認済み・公開後の数値は運営管理者が変更できず、削除もできない", async () => {
    await reportBatch(as(env, ADMIN), ADMIN, "rep", baseReport(), { create: true });
    await reportBatch(as(env, REVIEWER), REVIEWER, "rep", baseReport({ status: "confirmed", confirmedAt: serverTimestamp() }));
    const db = as(env, ADMIN);
    await assertFails(reportBatch(db, ADMIN, "rep", { status: "confirmed", expOther: 0, totalExpense: 44500, closingBalance: 20500, carryover: 19500 }));
    await assertFails(deleteDoc(doc(db, "financeReports", "rep")));
    await reportBatch(as(env, REVIEWER), REVIEWER, "rep", { status: "published", publishedOn: "2027-05-01" });
    await assertFails(reportBatch(db, ADMIN, "rep", { status: "published", achievements: "書き換え" }));
    await assertFails(reportBatch(as(env, REVIEWER), REVIEWER, "rep", { status: "published", achievements: "訂正履歴なしの書き換え" }));
    await assertFails(deleteDoc(doc(as(env, REVIEWER), "financeReports", "rep")));
  });

  it("公開後の訂正は、成人の確認者が訂正履歴を残して行う", async () => {
    await reportBatch(as(env, ADMIN), ADMIN, "rep", baseReport(), { create: true });
    const rev = as(env, REVIEWER);
    await reportBatch(rev, REVIEWER, "rep", baseReport({ status: "confirmed", confirmedAt: serverTimestamp() }));
    await reportBatch(rev, REVIEWER, "rep", { status: "published", publishedOn: "2027-05-01" });
    await assertSucceeds(reportBatch(rev, REVIEWER, "rep", {
      status: "published", expOther: 0, totalExpense: 44500, closingBalance: 20500, carryover: 20500,
      corrections: [{ date: "2027-05-10", text: "その他の支出の計上誤りを訂正しました。" }],
      confirmedAt: serverTimestamp(),
    }));
    // 訂正履歴は消せない
    await assertFails(reportBatch(rev, REVIEWER, "rep", { status: "published", corrections: [], confirmedAt: serverTimestamp() }));
    // 2回目の訂正：過去の訂正履歴を書き換えずに1件追加する
    const first = { date: "2027-05-10", text: "その他の支出の計上誤りを訂正しました。" };
    await assertFails(reportBatch(rev, REVIEWER, "rep", {
      status: "published", confirmedAt: serverTimestamp(),
      corrections: [{ date: "2027-05-10", text: "書き換えた訂正" }, { date: "2027-06-01", text: "2回目" }],
    }));
    await assertSucceeds(reportBatch(rev, REVIEWER, "rep", {
      status: "published", confirmedAt: serverTimestamp(),
      corrections: [first, { date: "2027-06-01", text: "2回目の訂正です。" }],
    }));
    // 運営管理者は訂正できない
    await assertFails(reportBatch(as(env, ADMIN), ADMIN, "rep", {
      status: "published", confirmedAt: serverTimestamp(),
      corrections: [first, { date: "2027-06-01", text: "2回目の訂正です。" }, { date: "2027-06-02", text: "3回目" }],
    }));
  });

  it("公開の取り下げは運営管理者もできる（数値は変えられない）", async () => {
    await reportBatch(as(env, ADMIN), ADMIN, "rep", baseReport(), { create: true });
    const rev = as(env, REVIEWER);
    await reportBatch(rev, REVIEWER, "rep", baseReport({ status: "confirmed", confirmedAt: serverTimestamp() }));
    await reportBatch(rev, REVIEWER, "rep", { status: "published", publishedOn: "2027-05-01" });
    await assertSucceeds(reportBatch(as(env, ADMIN), ADMIN, "rep", { status: "confirmed", publishedOn: "" }));
    await assertFails(getDoc(doc(as(env, null), "financeReports", "rep")));
  });

  it("下書きは削除できる", async () => {
    await reportBatch(as(env, ADMIN), ADMIN, "rep", baseReport(), { create: true });
    await assertSucceeds(deleteDoc(doc(as(env, ADMIN), "financeReports", "rep")));
  });
});

// ================================================================ 既存機能
describe("既存の曲目候補フォーム（テスト要件11）", () => {
  const suggestion = (o = {}) => ({
    timestamp: serverTimestamp(), name: "提案者", email: "s@example.com", category: "opening",
    title: "新世界より", composer: "ドヴォルザーク", reason: "", participationStatus: "", ...o,
  });

  it("誰でも提案を送信でき、読めるのは運営管理者だけ", async () => {
    const ref = await assertSucceeds(addDoc(collection(as(env, null), "programSuggestions"), suggestion()));
    await assertFails(getDoc(doc(as(env, null), "programSuggestions", ref.id)));
    await assertFails(getDoc(doc(as(env, REVIEWER), "programSuggestions", ref.id)));
    await assertSucceeds(getDoc(doc(as(env, ADMIN), "programSuggestions", ref.id)));
    await assertSucceeds(deleteDoc(doc(as(env, ADMIN), "programSuggestions", ref.id)));
  });

  it("複数カテゴリーの一括送信と、不正な提案の拒否", async () => {
    const db = as(env, null);
    const batch = writeBatch(db);
    batch.set(doc(collection(db, "programSuggestions")), suggestion());
    batch.set(doc(collection(db, "programSuggestions")), suggestion({ category: "encore1" }));
    await assertSucceeds(batch.commit());
    await assertFails(addDoc(collection(db, "programSuggestions"), suggestion({ category: "main" })));
    await assertFails(addDoc(collection(db, "programSuggestions"), suggestion({ extra: 1 })));
  });
});
