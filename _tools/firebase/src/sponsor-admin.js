// 協賛の管理（sponsor-admin.html・管理者専用）
// ・受け入れ状況と掲載特典の設定
// ・申込みの確認と、協賛記録への登録
// ・協賛記録（入金確認・掲載・返金）の管理と、変更履歴の表示
//
// 書き込みはすべて「記録＋履歴（＋公開用の文書）」を1つの処理で行います。
// 入金確認・掲載・返金の条件は Firestore Security Rules でもサーバー側で検証しています。
import {
  collection, doc, getDoc, getDocs, setDoc, deleteDoc, query, orderBy, writeBatch, runTransaction,
  serverTimestamp,
} from "firebase/firestore/lite";
import { getDb } from "./firebase-init.js";
import {
  h, field, textInput, select, checkbox, fmtDateTime, errorMessage, startStaffPage,
} from "./admin-common.js";
import {
  KINDS, RANKS, STATUSES, PAID_STATUSES, UNPAID_STATUSES, LISTING, CONTACT_STATUSES, MAX_UNITS,
  rankFor, amountFor, recordWarnings, listingBlockers, findDuplicates, publicEntryFromRecord, yen, todayJST,
} from "./sponsor-logic.js";

const EMPTY_BENEFITS = { standard: "", preferred: "", special: "" };

const state = {
  settings: null,
  applications: [],
  records: [],
  filter: "all",
  editing: null, // { id, isNew, data, original, fromApplication }
  history: [],
};

let page;

async function load() {
  const db = await getDb();
  const [settingsSnap, recSnap] = await Promise.all([
    getDoc(doc(db, "settings", "sponsorship")),
    getDocs(query(collection(db, "sponsorRecords"), orderBy("appliedOn", "desc"))),
  ]);
  state.settings = settingsSnap.exists() ? settingsSnap.data() : null;
  state.records = recSnap.docs.map((d) => ({ id: d.id, ...d.data() }));
  const appSnap = await getDocs(query(collection(db, "sponsorApplications"), orderBy("createdAt", "desc")));
  state.applications = appSnap.docs.map((d) => ({ id: d.id, ...d.data() }));
  state.editing = null;
  render();
}

function render() {
  page.body.replaceChildren(
    settingsSection(),
    applicationsSection(),
    recordsSection(),
    state.editing ? editorSection() : "",
  );
}

// ---------------------------------------------------------------- 設定

function settingsSection() {
  const s = state.settings || { acceptingApplications: false, benefitsConfirmed: false, benefits: EMPTY_BENEFITS };
  const benefits = { ...EMPTY_BENEFITS, ...(s.benefits || {}) };
  const inputs = {};
  const rows = Object.entries(RANKS).map(([k, label]) => {
    inputs[k] = h("textarea", { rows: 2, maxlength: 300, value: benefits[k] });
    return field(`${label}の掲載特典`, inputs[k]);
  });
  const confirmed = checkbox("掲載特典の内容を確認済みにする（成人の確認者のみ）", s.benefitsConfirmed);
  const accepting = checkbox("協賛の申込み受付を開始する（成人の確認者のみ・特典の確認が必要）", s.acceptingApplications);
  const msg = h("p", { class: "form-status", role: "status" });

  const save = async () => {
    const next = Object.fromEntries(Object.keys(EMPTY_BENEFITS).map((k) => [k, inputs[k].value.trim()]));
    const changed = JSON.stringify(next) !== JSON.stringify(benefits);
    let benefitsConfirmed = confirmed.input.checked;
    let acceptingApplications = accepting.input.checked;
    if (changed && s.benefitsConfirmed && benefitsConfirmed) {
      // 文言を変えたら、もう一度確認が必要
      benefitsConfirmed = false;
      acceptingApplications = false;
    }
    if (acceptingApplications && !s.acceptingApplications
        && !window.confirm("協賛の申込み受付を開始します。口座・契約・記録方法の確認と、協賛制度規定の確定が済んでいることを確認しましたか？")) {
      return;
    }
    try {
      const db = await getDb();
      await setDoc(doc(db, "settings", "sponsorship"), {
        acceptingApplications, benefitsConfirmed, benefits: next, updatedAt: serverTimestamp(),
      });
      await load();
      page.setStatus(changed && s.benefitsConfirmed ? "保存しました。特典の文言を変更したため、確認済み・受付開始は解除されました。" : "保存しました。");
    } catch (err) {
      msg.textContent = errorMessage(err);
      msg.classList.add("is-error");
    }
  };

  return h("section", { class: "admin-section", "aria-labelledby": "adm-settings" },
    h("h2", { id: "adm-settings", class: "admin-section__title", text: "受け入れ状況と掲載特典" }),
    h("ul", { class: "admin-chips" },
      h("li", { class: s.acceptingApplications ? "is-on" : "", text: `申込み受付：${s.acceptingApplications ? "受付中" : "停止中（準備中と表示）"}` }),
      h("li", { class: s.benefitsConfirmed ? "is-on" : "", text: `掲載特典：${s.benefitsConfirmed ? "確認済み" : "未確認（掲載例を表示）"}` }),
      h("li", { text: "支払い・振込先の表示：無効（第1段階では実装していません）" })),
    h("div", { class: "card admin-form" }, ...rows, confirmed.el, accepting.el,
      h("div", { class: "btn-group" }, h("button", { class: "btn btn--primary btn--sm", type: "button", text: "設定を保存", onclick: save })),
      msg));
}

// ---------------------------------------------------------------- 申込み

function applicationsSection() {
  const used = new Set(state.records.map((r) => r.sourceApplicationId).filter(Boolean));
  const rows = state.applications.map((a) => h("tr", {},
    h("td", { class: "nowrap", text: fmtDateTime(a.createdAt) }),
    h("td", { text: KINDS[a.kind] || a.kind }),
    h("td", {}, h("span", { class: "admin-table__name", text: a.kind === "organization" ? `${a.orgName}（${a.contactName}）` : a.contactName }),
      h("span", { class: "admin-table__meta", text: a.email })),
    h("td", { class: "nowrap", text: `${a.units}口／${yen(amountFor(a.kind, a.units))}` }),
    h("td", {}, LISTING[a.listing] || a.listing, a.displayName ? h("span", { class: "admin-table__meta", text: `表示名：${a.displayName}` }) : null,
      a.websiteUrl ? h("span", { class: "admin-table__meta", text: a.websiteUrl }) : null),
    h("td", { class: "admin-table__reason", text: a.message || "—" }),
    h("td", {},
      used.has(a.id)
        ? h("span", { class: "admin-table__meta", text: "記録作成済み" })
        : h("button", { class: "btn btn--outline btn--sm", type: "button", text: "記録を作成", onclick: () => openFromApplication(a) }),
      h("button", { class: "admin-table__delete", type: "button", text: "削除", onclick: () => removeApplication(a) }))));

  return h("section", { class: "admin-section", "aria-labelledby": "adm-apps" },
    h("h2", { id: "adm-apps", class: "admin-section__title", text: `申込み（${state.applications.length}件）` }),
    h("p", { class: "small muted", text: "申込みはフォームから送信された内容です。入金の確認は、協賛記録を作成してから行ってください。保存期間を過ぎた申込みや、本人から削除の依頼があった申込みは削除できます（協賛記録は残ります）。" }),
    state.applications.length
      ? h("div", { class: "table-wrap", role: "region", "aria-label": "申込みの一覧（横にスクロールできます）", tabindex: 0 },
        h("table", { class: "admin-table" },
          h("thead", {}, h("tr", {}, ...["受付日時", "区分", "申込者", "口数・金額", "掲載希望", "連絡事項", "操作"].map((t) => h("th", { scope: "col", text: t })))),
          h("tbody", {}, rows)))
      : h("p", { class: "muted", text: "申込みはありません。" }));
}

async function removeApplication(a) {
  if (!window.confirm(`${a.contactName}さんの申込みを削除します。元に戻せません。よろしいですか？`)) return;
  try {
    const db = await getDb();
    await deleteDoc(doc(db, "sponsorApplications", a.id));
    await load();
    page.setStatus("申込みを1件削除しました。");
  } catch (err) {
    page.setStatus(errorMessage(err), true);
  }
}

// ---------------------------------------------------------------- 記録一覧

function nextInternalId() {
  const year = todayJST().slice(0, 4);
  const nums = state.records.map((r) => (r.internalId || "").match(new RegExp(`^KCO-${year}-(\\d+)$`))).filter(Boolean).map((m) => Number(m[1]));
  return `KCO-${year}-${String((nums.length ? Math.max(...nums) : 0) + 1).padStart(3, "0")}`;
}

function blankRecord() {
  return {
    kind: "individual", internalId: nextInternalId(), appliedOn: todayJST(), contactName: "", email: "",
    units: 1, amount: 1000, rank: "standard", status: "received", paidAmount: 0, paymentConfirmedOn: "",
    listing: "named", consentListing: false, consentRecordedOn: "", displayName: "", websiteUrl: "",
    logoFile: "", intro: "", listingStart: "", listingEnd: "", contactStatus: "not_contacted", notes: "",
    refundAmount: 0, refundApprovedOn: "", sourceApplicationId: "",
  };
}

function openFromApplication(a) {
  const created = fmtDateTime(a.createdAt) ? a.createdAt.toDate().toLocaleDateString("sv-SE", { timeZone: "Asia/Tokyo" }) : todayJST();
  const data = {
    ...blankRecord(),
    kind: a.kind,
    appliedOn: created,
    contactName: a.kind === "organization" ? `${a.orgName}（${a.contactName}）`.slice(0, 100) : a.contactName,
    email: a.email,
    units: a.units,
    listing: a.listing,
    consentListing: a.consentListing,
    consentRecordedOn: a.consentListing ? created : "",
    displayName: a.displayName,
    websiteUrl: a.websiteUrl,
    sourceApplicationId: a.id,
  };
  openEditor({ id: `app-${a.id}`, isNew: true, data, fromApplication: true });
}

function recordsSection() {
  const dups = findDuplicates(state.records);
  const byId = Object.fromEntries(state.records.map((r) => [r.id, r]));
  const list = state.filter === "all" ? state.records : state.records.filter((r) => r.status === state.filter);
  const filters = [["all", "すべて"], ...Object.entries(STATUSES)].map(([k, label]) => {
    const count = k === "all" ? state.records.length : state.records.filter((r) => r.status === k).length;
    return h("button", {
      class: "filter-btn", type: "button", "aria-pressed": String(state.filter === k),
      onclick: () => { state.filter = k; render(); },
    }, label, h("span", { class: "filter-btn__count", text: String(count) }));
  });

  const rows = list.map((r) => {
    const warnings = recordWarnings(r);
    return h("tr", {},
      h("td", { class: "nowrap", text: r.internalId }),
      h("td", { class: "nowrap", text: r.appliedOn }),
      h("td", { text: KINDS[r.kind] }),
      h("td", {}, h("span", { class: "admin-table__name", text: r.displayName || "（表示名なし）" }),
        h("span", { class: "admin-table__meta", text: r.contactName })),
      h("td", { class: "nowrap", text: `${r.units}口／${yen(r.amount)}` }),
      h("td", { class: "nowrap" }, r.paidAmount ? yen(r.paidAmount) : "未入金",
        r.paymentConfirmedOn ? h("span", { class: "admin-table__meta", text: `確認日 ${r.paymentConfirmedOn}` }) : null),
      h("td", {}, h("span", { class: `status-tag status-tag--${r.status}`, text: STATUSES[r.status] })),
      h("td", {}, LISTING[r.listing], h("span", { class: "admin-table__meta", text: `${RANKS[r.rank]}・同意${r.consentListing ? "あり" : "なし"}` })),
      h("td", { text: CONTACT_STATUSES[r.contactStatus] }),
      h("td", {}, warnings.length
        ? h("ul", { class: "warn-list" }, warnings.map((w) => h("li", { text: w })))
        : h("span", { class: "ok-mark", text: "問題なし" })),
      h("td", {}, h("button", { class: "btn btn--outline btn--sm", type: "button", text: "編集", onclick: () => openEditor({ id: r.id, isNew: false, data: r }) })));
  });

  return h("section", { class: "admin-section", "aria-labelledby": "adm-records" },
    h("h2", { id: "adm-records", class: "admin-section__title", text: "協賛記録" }),
    h("div", { class: "btn-group" },
      h("button", { class: "btn btn--primary btn--sm", type: "button", text: "新しい記録を追加", onclick: () => openEditor({ id: null, isNew: true, data: blankRecord() }) })),
    dups.length
      ? h("div", { class: "notice-box notice-box--warn", role: "alert" },
        h("p", { class: "notice-box__title", text: "重複登録の疑いがあります" }),
        h("ul", { class: "dash-list" }, dups.map((g) => h("li", { text: `${g.label}が同じ記録：${g.ids.map((id) => byId[id]?.internalId || id).join("、")}` }))))
      : null,
    h("div", { class: "filter-group", role: "group", "aria-label": "状態で絞り込む" }, filters),
    list.length
      ? h("div", { class: "table-wrap", role: "region", "aria-label": "協賛記録の一覧（横にスクロールできます）", tabindex: 0 },
        h("table", { class: "admin-table admin-table--wide" },
          h("thead", {}, h("tr", {}, ...["管理ID", "申込日", "区分", "表示名・担当者", "口数・金額", "入金", "状態", "掲載", "連絡", "確認事項", "操作"].map((t) => h("th", { scope: "col", text: t })))),
          h("tbody", {}, rows)))
      : h("p", { class: "muted", text: "該当する記録はありません。" }));
}

// ---------------------------------------------------------------- 記録の編集

async function openEditor(editing) {
  state.editing = { ...editing, data: { ...editing.data }, original: editing.isNew ? null : { ...editing.data } };
  state.history = [];
  render();
  if (!editing.isNew) {
    try {
      const db = await getDb();
      const snap = await getDocs(query(collection(db, "sponsorRecords", editing.id, "history"), orderBy("at", "desc")));
      state.history = snap.docs.map((d) => d.data());
      const box = page.body.querySelector("[data-history]");
      if (box) box.replaceChildren(historyList());
    } catch (err) {
      page.setStatus("履歴を読み込めませんでした。", true);
    }
  }
  page.body.querySelector("[data-editor]")?.scrollIntoView({ block: "start" });
}

function historyList() {
  if (!state.history.length) return h("p", { class: "muted small", text: "履歴はありません。" });
  return h("ol", { class: "history-list" }, state.history.map((x) => h("li", {},
    h("span", { class: "history-list__when", text: fmtDateTime(x.at) }),
    h("span", { text: `${x.action}（${STATUSES[x.status] || x.status}・${x.units}口・入金${yen(x.paidAmount)}${x.refundAmount ? `・返金${yen(x.refundAmount)}` : ""}）` }),
    x.note ? h("span", { class: "history-list__note", text: `メモ：${x.note}` }) : null,
    h("span", { class: "admin-table__meta", text: `操作：${x.by}` }))));
}

function editorSection() {
  const ed = state.editing;
  const d = ed.data;
  const inp = {
    internalId: textInput(d.internalId, { maxlength: 40, pattern: "[A-Za-z0-9_-]+" }),
    appliedOn: h("input", { type: "date", value: d.appliedOn }),
    kind: select(KINDS, d.kind),
    contactName: textInput(d.contactName, { maxlength: 100 }),
    email: h("input", { type: "email", value: d.email, maxlength: 254 }),
    units: h("input", { type: "number", min: 1, max: MAX_UNITS, step: 1, value: d.units, inputmode: "numeric" }),
    status: select(STATUSES, d.status),
    paidAmount: h("input", { type: "number", min: 0, step: 1, value: d.paidAmount, inputmode: "numeric" }),
    paymentConfirmedOn: h("input", { type: "date", value: d.paymentConfirmedOn }),
    listing: select(LISTING, d.listing),
    consentRecordedOn: h("input", { type: "date", value: d.consentRecordedOn }),
    displayName: textInput(d.displayName, { maxlength: 100 }),
    websiteUrl: h("input", { type: "url", value: d.websiteUrl, maxlength: 300, placeholder: "https://" }),
    logoFile: textInput(d.logoFile, { maxlength: 70, placeholder: "example.png" }),
    intro: h("textarea", { rows: 3, maxlength: 300, value: d.intro }),
    listingStart: h("input", { type: "date", value: d.listingStart }),
    listingEnd: h("input", { type: "date", value: d.listingEnd }),
    contactStatus: select(CONTACT_STATUSES, d.contactStatus),
    notes: h("textarea", { rows: 2, maxlength: 500, value: d.notes }),
    refundAmount: h("input", { type: "number", min: 0, step: 1, value: d.refundAmount, inputmode: "numeric" }),
    refundApprovedOn: h("input", { type: "date", value: d.refundApprovedOn }),
    changeNote: h("textarea", { rows: 2, maxlength: 300 }),
  };
  const consent = checkbox("掲載について本人の明確な同意を得ている", d.consentListing);
  const computed = h("p", { class: "admin-computed", "aria-live": "polite" });
  const checks = h("div", { "aria-live": "polite" });
  const preview = h("div", { class: "admin-preview" });
  const msg = h("p", { class: "form-status", role: "status" });

  const collect = () => {
    const units = Number(inp.units.value);
    const kind = inp.kind.value;
    return {
      ...d,
      internalId: inp.internalId.value.trim(),
      appliedOn: inp.appliedOn.value,
      kind,
      contactName: inp.contactName.value.trim(),
      email: inp.email.value.trim(),
      units,
      amount: amountFor(kind, units) ?? 0,
      rank: rankFor(units) ?? "standard",
      status: inp.status.value,
      paidAmount: Number(inp.paidAmount.value || 0),
      paymentConfirmedOn: inp.paymentConfirmedOn.value,
      listing: inp.listing.value,
      consentListing: consent.input.checked,
      consentRecordedOn: inp.consentRecordedOn.value,
      displayName: inp.displayName.value.trim(),
      websiteUrl: inp.websiteUrl.value.trim(),
      logoFile: inp.logoFile.value.trim(),
      intro: inp.intro.value.trim(),
      listingStart: inp.listingStart.value,
      listingEnd: inp.listingEnd.value,
      contactStatus: inp.contactStatus.value,
      notes: inp.notes.value.trim(),
      refundAmount: Number(inp.refundAmount.value || 0),
      refundApprovedOn: inp.refundApprovedOn.value,
    };
  };

  const update = () => {
    const r = collect();
    computed.textContent = `協賛金額：${yen(r.amount)}　掲載ランク：${RANKS[r.rank] || "—"}（口数から自動で判定）`;
    const w = recordWarnings(r);
    const blockers = r.status === "listed" ? listingBlockers(r) : [];
    checks.replaceChildren(
      w.length || blockers.length
        ? h("ul", { class: "warn-list" }, [...new Set([...w, ...blockers])].map((x) => h("li", { text: x })))
        : h("p", { class: "ok-mark", text: "確認事項はありません。" }));
    if (r.listing === "none") {
      preview.replaceChildren(h("p", { class: "muted small", text: "掲載しない希望のため、協賛者一覧には表示されません。" }));
    } else {
      const p = publicEntryFromRecord(r);
      preview.replaceChildren(
        h("p", { class: "small", text: "協賛者一覧に表示される内容（掲載中のときのみ）：" }),
        h("ul", { class: "dash-list small" },
          h("li", { text: `名前：${p.anonymous ? "匿名の方" : p.displayName || "（未入力）"}` }),
          h("li", { text: `掲載ランク：${RANKS[p.rank]}` }),
          p.websiteUrl ? h("li", { text: `リンク：${p.websiteUrl}` }) : null,
          p.logoFile ? h("li", { text: `ロゴ：images/sponsors/${p.logoFile}` }) : null,
          p.intro ? h("li", { text: `紹介文：${p.intro}` }) : null,
          h("li", { text: `掲載期間：${p.listingStart || "未設定"} 〜 ${p.listingEnd || "（終了日なし）"}` })));
    }
  };

  const save = async () => {
    const r = collect();
    const prev = ed.original;
    const wasPaid = prev && PAID_STATUSES.includes(prev.status);
    if (PAID_STATUSES.includes(r.status) && !wasPaid
        && !window.confirm(`入金確認済みにします。\n\n実際の入金（${yen(r.paidAmount)}・${r.paymentConfirmedOn || "日付未入力"}）を、通帳や入金記録で確認しましたか？\nフォームの送信や本人からの連絡だけでは、入金済みにしないでください。`)) {
      return;
    }
    if (r.status === "listed" && (!prev || prev.status !== "listed")
        && !window.confirm("協賛者一覧に公開します。表示内容と掲載への同意を確認しましたか？")) {
      return;
    }
    const action = !prev ? "記録を作成"
      : prev.status !== r.status ? `状態の変更：${STATUSES[prev.status]}→${STATUSES[r.status]}`
        : "内容の変更";
    try {
      const db = await getDb();
      const recRef = ed.id ? doc(db, "sponsorRecords", ed.id) : doc(collection(db, "sponsorRecords"));
      const histRef = doc(collection(db, "sponsorRecords", recRef.id, "history"));
      const { id: _drop, ...rest } = r;
      const data = {
        ...rest,
        lastHistoryId: histRef.id,
        createdAt: prev ? prev.createdAt : serverTimestamp(),
        updatedAt: serverTimestamp(),
      };
      const hist = {
        at: serverTimestamp(), by: page.user.email, action, note: inp.changeNote.value.trim(),
        status: r.status, units: r.units, amount: r.amount, paidAmount: r.paidAmount,
        refundAmount: r.refundAmount, listing: r.listing, consentListing: r.consentListing,
      };
      const pubRef = doc(db, "publicSponsors", recRef.id);

      if (ed.fromApplication) {
        // 同じ申込みから2件の記録ができないように、存在確認と作成を1つの処理で行う
        await runTransaction(db, async (tx) => {
          const existing = await tx.get(recRef);
          if (existing.exists()) throw new Error("duplicate");
          tx.set(recRef, data);
          tx.set(histRef, hist);
        });
      } else {
        const batch = writeBatch(db);
        batch.set(recRef, data);
        batch.set(histRef, hist);
        if (r.status === "listed") batch.set(pubRef, publicEntryFromRecord(r));
        else if (prev) batch.delete(pubRef);
        await batch.commit();
      }
      await load();
      page.setStatus("保存しました。");
    } catch (err) {
      msg.textContent = errorMessage(err);
      msg.classList.add("is-error");
    }
  };

  const form = h("div", { class: "card admin-form", "data-editor": true },
    h("h3", { class: "card__title", text: ed.isNew ? "協賛記録の追加" : `協賛記録の編集（${d.internalId}）` }),
    h("fieldset", { class: "admin-fieldset" }, h("legend", { text: "申込み" }),
      h("div", { class: "admin-grid" },
        field("管理ID（内部用）", inp.internalId, { hint: "英数字・ハイフンのみ。公開されません。" }),
        field("申込日", inp.appliedOn),
        field("協賛者区分", inp.kind),
        field("口数", inp.units),
        field("担当者名・お名前（非公開）", inp.contactName),
        field("メールアドレス（非公開）", inp.email)),
      computed),
    h("fieldset", { class: "admin-fieldset" }, h("legend", { text: "入金" }),
      h("div", { class: "admin-grid" },
        field("状態", inp.status, { hint: "入金確認済み以降にするには、実際の入金を確認したうえで入金額と入金確認日を入力してください。" }),
        field("入金額（円）", inp.paidAmount),
        field("入金確認日", inp.paymentConfirmedOn),
        field("連絡状況", inp.contactStatus))),
    h("fieldset", { class: "admin-fieldset" }, h("legend", { text: "掲載" }),
      h("div", { class: "admin-grid" },
        field("掲載方法", inp.listing),
        field("同意を記録した日", inp.consentRecordedOn),
        field("表示名", inp.displayName),
        field("公式サイトURL（企業・団体の優遇以上）", inp.websiteUrl, { hint: "https:// から始まるURLのみ。" }),
        field("ロゴのファイル名（企業・団体の特別優遇）", inp.logoFile, { hint: "確認済みの画像を images/sponsors/ に置き、そのファイル名を入力します（png・jpg・webp）。" }),
        field("掲載開始日", inp.listingStart),
        field("掲載終了日", inp.listingEnd, { hint: "空欄の場合は終了日なし。" })),
      field("紹介文（特別優遇）", inp.intro, { hint: "300文字以内。HTMLは使えません（文字としてそのまま表示されます）。" }),
      consent.el,
      preview),
    h("fieldset", { class: "admin-fieldset" }, h("legend", { text: "取消・返金（成人の確認者のみ）" }),
      h("div", { class: "admin-grid" },
        field("返金額（円）", inp.refundAmount),
        field("返金を承認した日", inp.refundApprovedOn))),
    field("備考（必要最小限・非公開）", inp.notes, { hint: "口座番号・住所などは書かないでください。" }),
    field("この変更のメモ（履歴に残ります）", inp.changeNote),
    h("div", { class: "admin-checks" }, h("p", { class: "small", text: "確認事項：" }), checks),
    h("div", { class: "btn-group" },
      h("button", { class: "btn btn--primary btn--sm", type: "button", text: "保存", onclick: save }),
      h("button", { class: "btn btn--outline btn--sm", type: "button", text: "閉じる", onclick: () => { state.editing = null; render(); } })),
    msg,
    ed.isNew ? null : h("div", {}, h("h4", { class: "admin-subtitle", text: "変更履歴（削除・変更できません）" }), h("div", { "data-history": true }, historyList())));

  form.addEventListener("input", update);
  form.addEventListener("change", update);
  update();
  return h("section", { class: "admin-section", "aria-label": "協賛記録の編集" }, form);
}

page = startStaffPage({
  onSignedIn: async (p) => {
    page = p;
    await load();
  },
});
