// テスト用の共通処理
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { initializeTestEnvironment } from "@firebase/rules-unit-testing";
import { doc, writeBatch, serverTimestamp } from "firebase/firestore";

const RULES_PATH = fileURLToPath(new URL("../../../firestore.rules", import.meta.url));

export const ADMIN = "kanagawaorchestra2026renraku@gmail.com";
export const REVIEWER = "reviewer@example.com";
export const STRANGER = "someone@example.com";

// withReviewer: true なら、テスト用の成人の確認者を登録したルールで起動する
// false なら、リポジトリのルールをそのまま使う（確認者が未登録の本番と同じ状態）
export async function setupEnv(projectId, { withReviewer = true } = {}) {
  let rules = readFileSync(RULES_PATH, "utf8");
  if (withReviewer) rules = rules.replace("/*REVIEWERS*/", `'${REVIEWER}'`);
  const [host, port] = (process.env.FIRESTORE_EMULATOR_HOST || "127.0.0.1:8085").split(":");
  return initializeTestEnvironment({ projectId, firestore: { rules, host, port: Number(port) } });
}

export function as(env, who, { verified = true } = {}) {
  if (!who) return env.unauthenticatedContext().firestore();
  return env.authenticatedContext(who.replace(/\W/g, "_"), { email: who, email_verified: verified }).firestore();
}

let seq = 0;
export const newId = (prefix) => `${prefix}${Date.now().toString(36)}${(seq++).toString(36)}`;

export function baseRecord(overrides = {}) {
  return {
    kind: "individual",
    internalId: "KCO-2026-001",
    appliedOn: "2026-10-01",
    contactName: "テスト 太郎",
    email: "taro@example.com",
    units: 3,
    amount: 3000,
    rank: "standard",
    status: "received",
    paidAmount: 0,
    paymentConfirmedOn: "",
    listing: "named",
    consentListing: false,
    consentRecordedOn: "",
    displayName: "テスト太郎",
    websiteUrl: "",
    logoFile: "",
    intro: "",
    listingStart: "",
    listingEnd: "",
    contactStatus: "not_contacted",
    notes: "",
    refundAmount: 0,
    refundApprovedOn: "",
    sourceApplicationId: "",
    ...overrides,
  };
}

export function snapshotOf(rec) {
  const { status, units, amount, paidAmount, refundAmount, listing, consentListing } = rec;
  return { status, units, amount, paidAmount, refundAmount, listing, consentListing };
}

// 記録・履歴・（必要なら）公開用文書を、管理画面と同じく1つの処理で書き込む
// opts.public: 公開用文書の内容 / null なら削除 / undefined なら触らない
export function recordBatch(db, who, id, rec, { create = false, public: pub, history = {} } = {}) {
  const batch = writeBatch(db);
  const hid = history.id || newId("h");
  const data = { ...rec, lastHistoryId: hid, updatedAt: serverTimestamp() };
  if (create) data.createdAt = serverTimestamp();
  batch.set(doc(db, "sponsorRecords", id), data, create ? undefined : { merge: true });
  const hist = {
    at: serverTimestamp(), by: who, action: "test", note: "",
    ...snapshotOf(rec), ...(history.data || {}),
  };
  if (history.skip !== true) batch.set(doc(db, "sponsorRecords", id, "history", hid), hist);
  if (pub === null) batch.delete(doc(db, "publicSponsors", id));
  else if (pub) batch.set(doc(db, "publicSponsors", id), pub);
  return batch.commit();
}

export function baseReport(overrides = {}) {
  const r = {
    title: "2026年度",
    periodStart: "2026-04-01",
    periodEnd: "2027-03-31",
    openingBalance: 10000,
    incomeSponsorship: 50000,
    incomeOther: 5000,
    expPractice: 20000,
    expConcert: 15000,
    expMusic: 3000,
    expPublicity: 2000,
    expMemberSupport: 4000,
    expOther: 1000,
    expFees: 500,
    carryover: 19500,
    reserve: 5000,
    achievements: "第1回演奏会に向けた合奏練習を行いました。",
    status: "draft",
    publishedOn: "",
    corrections: [],
    confirmedAt: null,
    ...overrides,
  };
  if (!("totalIncome" in overrides)) r.totalIncome = r.incomeSponsorship + r.incomeOther;
  if (!("totalExpense" in overrides)) {
    r.totalExpense = r.expPractice + r.expConcert + r.expMusic + r.expPublicity + r.expMemberSupport + r.expOther + r.expFees;
  }
  if (!("closingBalance" in overrides)) r.closingBalance = r.openingBalance + r.totalIncome - r.totalExpense;
  return r;
}

export function reportBatch(db, who, id, rep, { create = false, history = {} } = {}) {
  const batch = writeBatch(db);
  const hid = history.id || newId("h");
  const data = { ...rep, lastHistoryId: hid, updatedAt: serverTimestamp() };
  if (create) data.createdAt = serverTimestamp();
  batch.set(doc(db, "financeReports", id), data, create ? undefined : { merge: true });
  if (history.skip !== true) {
    batch.set(doc(db, "financeReports", id, "history", hid), {
      at: serverTimestamp(), by: who, action: "test", note: "", status: rep.status, ...(history.data || {}),
    });
  }
  return batch.commit();
}
