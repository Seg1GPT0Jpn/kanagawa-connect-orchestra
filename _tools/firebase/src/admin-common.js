// 協賛・会計の管理画面で共通の処理（ログイン・表示切り替え・DOM作成）
// 画面の切り替えは使い勝手のためのもので、実際の権限は Firestore Security Rules で判定しています。
import {
  getAuth, connectAuthEmulator, GoogleAuthProvider,
  signInWithPopup, signInWithRedirect, signOut, onAuthStateChanged,
} from "firebase/auth";
import { getApp, isLocal, EMULATOR_PORTS } from "./firebase-init.js";

// DOM を作る。文字列は必ず textContent として設定し、HTMLとして解釈しない
export function h(tag, attrs = {}, ...children) {
  const el = document.createElement(tag);
  Object.entries(attrs || {}).forEach(([k, v]) => {
    if (v === undefined || v === null || v === false) return;
    if (k === "class") el.className = v;
    else if (k === "text") el.textContent = v;
    else if (k === "value") el.value = String(v);
    else if (k.startsWith("on") && typeof v === "function") el.addEventListener(k.slice(2), v);
    else if (k in el && typeof v !== "string") el[k] = v;
    else el.setAttribute(k, v === true ? "" : String(v));
  });
  children.flat().forEach((c) => {
    if (c === null || c === undefined || c === false) return;
    el.append(c instanceof Node ? c : document.createTextNode(String(c)));
  });
  return el;
}

export function fmtDateTime(ts) {
  return ts && typeof ts.toDate === "function"
    ? ts.toDate().toLocaleString("ja-JP", { dateStyle: "medium", timeStyle: "short" })
    : "";
}

export function errorMessage(err) {
  if (err && err.code === "permission-denied") {
    return "保存できませんでした。権限がないか、入力内容がルールの条件を満たしていません（成人の確認者のみの操作、入金・同意の記録漏れ、合計の不一致など）。";
  }
  if (err && err.message === "duplicate") return "この申込みからは、すでに記録が作成されています。";
  return "処理できませんでした。通信環境を確認して、もう一度お試しください。";
}

// 管理画面の入口。ログインできたら onSignedIn(user) を呼ぶ。
// onSignedIn が permission-denied で失敗した場合は「閲覧権限がありません」を表示する。
export function startStaffPage({ onSignedIn }) {
  const root = document.querySelector("[data-staff]");
  if (!root) return null;
  const $ = (sel) => root.querySelector(sel);
  const views = {
    loading: $("[data-admin-loading]"),
    signedOut: $("[data-admin-signed-out]"),
    denied: $("[data-admin-denied]"),
    panel: $("[data-admin-panel]"),
  };
  const statusEl = $("[data-admin-status]");
  const body = $("[data-panel-body]");

  const page = {
    root,
    body,
    user: null,
    show(name) {
      Object.entries(views).forEach(([key, el]) => { el.hidden = key !== name; });
    },
    setStatus(msg, isError = false) {
      statusEl.textContent = msg;
      statusEl.classList.toggle("is-error", isError);
    },
    async reload() {
      page.setStatus("読み込み中…");
      try {
        await onSignedIn(page);
        page.show("panel");
        page.setStatus(`最終更新：${new Date().toLocaleTimeString("ja-JP")}`);
      } catch (err) {
        body.replaceChildren();
        if (err && err.code === "permission-denied") {
          page.show("denied");
          page.setStatus("");
        } else {
          console.error(err && err.code ? err.code : "load-failed");
          page.setStatus("読み込めませんでした。時間をおいて再度お試しください。", true);
        }
      }
    },
  };

  (async () => {
    let auth;
    try {
      const app = await getApp();
      auth = getAuth(app);
      if (isLocal) {
        connectAuthEmulator(auth, `http://127.0.0.1:${EMULATOR_PORTS.auth}`, { disableWarnings: true });
      }
    } catch (err) {
      page.show("signedOut");
      page.setStatus("この環境では管理画面を利用できません。公開中のサイト（Firebase Hosting）で開いてください。", true);
      return;
    }
    const provider = new GoogleAuthProvider();
    provider.setCustomParameters({ prompt: "select_account" });

    root.querySelectorAll("[data-signin]").forEach((btn) => btn.addEventListener("click", async () => {
      page.setStatus("");
      try {
        await signInWithPopup(auth, provider);
      } catch (err) {
        if (err && (err.code === "auth/popup-blocked" || err.code === "auth/operation-not-supported-in-this-environment")) {
          await signInWithRedirect(auth, provider);
        } else if (err && err.code !== "auth/popup-closed-by-user" && err.code !== "auth/cancelled-popup-request") {
          page.setStatus("ログインできませんでした。もう一度お試しください。", true);
        }
      }
    }));
    root.querySelectorAll("[data-signout]").forEach((btn) => btn.addEventListener("click", () => signOut(auth)));
    root.querySelector("[data-reload]").addEventListener("click", () => page.reload());

    onAuthStateChanged(auth, (user) => {
      page.user = user;
      body.replaceChildren();
      root.querySelectorAll("[data-admin-email]").forEach((el) => { el.textContent = user ? user.email : ""; });
      if (user) {
        page.reload();
      } else {
        page.show("signedOut");
        page.setStatus("");
      }
    });
  })();

  return page;
}

// フォームの部品
export function field(label, input, { hint, id } = {}) {
  const fid = id || input.id || `f-${Math.random().toString(36).slice(2, 9)}`;
  input.id = fid;
  return h("div", { class: "field" },
    h("label", { for: fid, text: label }),
    hint ? h("p", { class: "field__hint", text: hint }) : null,
    input);
}

export function textInput(value = "", attrs = {}) {
  return h("input", { type: "text", value: value ?? "", ...attrs });
}

export function select(options, value) {
  const s = h("select", { class: "select" });
  Object.entries(options).forEach(([k, label]) => {
    s.append(h("option", { value: k, text: label, selected: k === value }));
  });
  return s;
}

export function checkbox(label, checked) {
  const input = h("input", { type: "checkbox", checked: !!checked });
  return { input, el: h("label", { class: "choice" }, input, h("span", { text: label })) };
}
