// 練習お助けアプリの Firestore セキュリティルールのテスト（Firestore エミュレーター上で実行）
// 実行方法：practice-app/rules-test で `npm ci` → `npm test`
import { describe, it, before, after, beforeEach } from "node:test";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { initializeTestEnvironment, assertFails, assertSucceeds } from "@firebase/rules-unit-testing";
import {
  doc, getDoc, getDocs, setDoc, updateDoc, deleteDoc, collection, query, where, orderBy,
  serverTimestamp, Timestamp,
} from "firebase/firestore";

const RULES = readFileSync(fileURLToPath(new URL("../../firestore.rules", import.meta.url)), "utf8");

let env;
before(async () => {
  const [host, port] = (process.env.FIRESTORE_EMULATOR_HOST || "127.0.0.1:8086").split(":");
  env = await initializeTestEnvironment({
    projectId: "demo-kco-practice",
    firestore: { rules: RULES, host, port: Number(port) },
  });
});
after(async () => env?.cleanup());
beforeEach(async () => env.clearFirestore());

const as = (uid) => (uid ? env.authenticatedContext(uid) : env.unauthenticatedContext()).firestore();
const recRef = (db, uid, id) => doc(db, "users", uid, "practiceRecords", id);

// アプリ（PracticeRecord.toMap）と同じ形
function rec(id, uid, o = {}) {
  return {
    id,
    ownerUid: uid,
    practicedOn: "2026-10-12",
    startedAt: 1760000000000,
    ruleSetId: "trumpet_basic",
    plannedMinutes: { mouthpiece: 20, long_tone: 15 },
    actualSeconds: { mouthpiece: 1180, long_tone: 900 },
    note: "",
    updatedAt: 1760000000000,
    updatedBy: "devA",
    deleted: false,
    serverUpdatedAt: serverTimestamp(),
    ...o,
  };
}

async function seed(uid, id, o = {}) {
  await assertSucceeds(setDoc(recRef(as(uid), uid, id), rec(id, uid, o)));
}

describe("練習記録（users/{uid}/practiceRecords）", () => {
  it("本人は作成・読み取りができる", async () => {
    await seed("alice", "r1");
    const db = as("alice");
    const snap = await assertSucceeds(getDoc(recRef(db, "alice", "r1")));
    if (snap.data().actualSeconds.mouthpiece !== 1180) throw new Error("内容が違う");
  });

  it("ログインしていない人・ほかの人は読めない・書けない", async () => {
    await seed("alice", "r1");
    for (const db of [as(null), as("bob")]) {
      await assertFails(getDoc(recRef(db, "alice", "r1")));
      await assertFails(getDocs(collection(db, "users", "alice", "practiceRecords")));
      await assertFails(setDoc(recRef(db, "alice", "r2"), rec("r2", "alice")));
    }
  });

  it("ほかの人のフォルダに、自分の記録として書き込むこともできない", async () => {
    await assertFails(setDoc(recRef(as("bob"), "alice", "r1"), rec("r1", "bob")));
  });

  it("同期で使う「serverUpdatedAt 以降」のクエリが本人なら通る", async () => {
    await seed("alice", "r1");
    const db = as("alice");
    await assertSucceeds(getDocs(query(
      collection(db, "users", "alice", "practiceRecords"),
      where("serverUpdatedAt", ">=", Timestamp.fromMillis(0)),
      orderBy("serverUpdatedAt"),
    )));
  });

  it("持ち主・ID・サーバー時刻がおかしい記録は書けない", async () => {
    const db = as("alice");
    const bad = [
      ["ownerUid がほかの人", rec("r1", "bob")],
      ["ownerUid が null", rec("r1", null)],
      ["中の id とドキュメント ID が違う", { ...rec("r1", "alice"), id: "r999" }],
      ["serverUpdatedAt が端末の時刻", rec("r1", "alice", { serverUpdatedAt: Timestamp.fromMillis(1) })],
    ];
    for (const [why, data] of bad) {
      await assertFails(setDoc(recRef(db, "alice", "r1"), data), why);
    }
  });

  it("形のおかしい記録は書けない", async () => {
    const db = as("alice");
    const { note: _n, ...withoutNote } = rec("r1", "alice");
    const bad = [
      ["項目が足りない", withoutNote],
      ["余計な項目", rec("r1", "alice", { extra: 1 })],
      ["日付の形式", rec("r1", "alice", { practicedOn: "2026/10/12" })],
      ["startedAt が文字列", rec("r1", "alice", { startedAt: "1760000000000" })],
      ["updatedAt が小数", rec("r1", "alice", { updatedAt: 1.5 })],
      ["deleted が文字列", rec("r1", "alice", { deleted: "false" })],
      ["メモが長すぎる", rec("r1", "alice", { note: "あ".repeat(501) })],
      ["実績が map でない", rec("r1", "alice", { actualSeconds: [1180] })],
      ["ruleSetId が空", rec("r1", "alice", { ruleSetId: "" })],
      ["updatedBy が空", rec("r1", "alice", { updatedBy: "" })],
    ];
    for (const [why, data] of bad) {
      await assertFails(setDoc(recRef(db, "alice", "r1"), data), why);
    }
    // 使えない文字のドキュメント ID
    await assertFails(setDoc(recRef(db, "alice", "r-1"), rec("r-1", "alice")));
    // ちょうど500文字のメモは OK
    await assertSucceeds(setDoc(recRef(db, "alice", "r2"), rec("r2", "alice", { note: "あ".repeat(500) })));
  });

  it("目標・達成度・次回の課題は、あってもなくてもよい（形は確かめる）", async () => {
    const db = as("alice");
    await assertSucceeds(setDoc(recRef(db, "alice", "g1"), rec("g1", "alice", {
      goal: "ロングトーンの音程を安定させる", achievement: 4, nextFocus: "高音の B♭ を楽に",
    })));
    await assertSucceeds(setDoc(recRef(db, "alice", "g2"), rec("g2", "alice", { goal: "あ".repeat(200) })));
    const bad = [
      ["目標が長すぎる", rec("g3", "alice", { goal: "あ".repeat(201) })],
      ["達成度が 6", rec("g3", "alice", { achievement: 6 })],
      ["達成度が文字列", rec("g3", "alice", { achievement: "4" })],
      ["次回の課題が数", rec("g3", "alice", { nextFocus: 1 })],
    ];
    for (const [why, data] of bad) {
      await assertFails(setDoc(recRef(db, "alice", "g3"), data), why);
    }
  });

  it("新しい版での上書き・削除の印は OK、古い版での上書きはできない", async () => {
    await seed("alice", "r1", { updatedAt: 2000 });
    const db = as("alice");
    const ref = recRef(db, "alice", "r1");
    await assertFails(setDoc(ref, rec("r1", "alice", { updatedAt: 1999, note: "古い" })));
    // 同じ時刻（端末 ID で勝った版）は OK
    await assertSucceeds(setDoc(ref, rec("r1", "alice", { updatedAt: 2000, updatedBy: "devB" })));
    await assertSucceeds(setDoc(ref, rec("r1", "alice", { updatedAt: 3000, note: "新しい" })));
    await assertSucceeds(setDoc(ref, rec("r1", "alice", { updatedAt: 4000, deleted: true })));
    // 一部だけの更新でも、サーバー時刻は必須
    await assertFails(updateDoc(ref, { note: "x", updatedAt: 5000 }));
    await assertSucceeds(updateDoc(ref, { note: "x", updatedAt: 5000, serverUpdatedAt: serverTimestamp() }));
  });

  it("ドキュメントの削除はできない（削除済みの印を使う）", async () => {
    await seed("alice", "r1");
    await assertFails(deleteDoc(recRef(as("alice"), "alice", "r1")));
  });

  it("ほかの場所には読み書きできない", async () => {
    const db = as("alice");
    await assertFails(setDoc(doc(db, "users", "alice"), { name: "alice" }));
    await assertFails(getDoc(doc(db, "users", "alice")));
    await assertFails(setDoc(doc(db, "anything", "x"), { a: 1 }));
    await assertFails(setDoc(doc(db, "users", "alice", "other", "x"), { a: 1 }));
  });
});
