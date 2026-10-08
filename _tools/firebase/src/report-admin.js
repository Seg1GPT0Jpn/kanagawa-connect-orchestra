// 会計報告の作成（report-admin.html・管理者専用）
// ・運営管理者：下書きの作成・編集、確認の依頼、公開の取り下げ（緊急時）
// ・成人の確認者：確認済みにする、公開、差し戻し、公開後の訂正
// 合計・残高の整合性と、状態の移り変わりは Firestore Security Rules でも検証しています。
import {
  collection, doc, getDocs, deleteDoc, query, orderBy, writeBatch, serverTimestamp,
} from "firebase/firestore/lite";
import { getDb } from "./firebase-init.js";
import { h, field, textInput, fmtDateTime, errorMessage, startStaffPage } from "./admin-common.js";
import {
  INCOME_FIELDS, EXPENSE_FIELDS, REPORT_STATUSES, computeTotals, reportErrors, confirmedSponsorshipTotal,
  yen, todayJST,
} from "./sponsor-logic.js";

const NUM_FIELDS = ["openingBalance", ...INCOME_FIELDS.map(([k]) => k), ...EXPENSE_FIELDS.map(([k]) => k), "carryover", "reserve"];

const state = { reports: [], records: [], editing: null, history: [] };
let page;

async function load() {
  const db = await getDb();
  const repSnap = await getDocs(query(collection(db, "financeReports"), orderBy("periodStart", "desc")));
  state.reports = repSnap.docs.map((d) => ({ id: d.id, ...d.data() }));
  const recSnap = await getDocs(collection(db, "sponsorRecords"));
  state.records = recSnap.docs.map((d) => d.data());
  state.editing = null;
  render();
}

function render() {
  page.body.replaceChildren(listSection(), state.editing ? editorSection() : "");
}

function blankReport() {
  const r = {
    title: "", periodStart: "", periodEnd: "", achievements: "", status: "draft", publishedOn: "",
    corrections: [], confirmedAt: null,
  };
  NUM_FIELDS.forEach((k) => { r[k] = 0; });
  return { ...r, ...computeTotals(r) };
}

function listSection() {
  const rows = state.reports.map((r) => h("tr", {},
    h("td", { class: "admin-table__title", text: r.title }),
    h("td", { class: "nowrap", text: `${r.periodStart} 〜 ${r.periodEnd}` }),
    h("td", {}, h("span", { class: `status-tag status-tag--report-${r.status}`, text: REPORT_STATUSES[r.status] })),
    h("td", { class: "nowrap", text: r.publishedOn || "—" }),
    h("td", { class: "nowrap", text: fmtDateTime(r.updatedAt) }),
    h("td", {}, h("button", { class: "btn btn--outline btn--sm", type: "button", text: "開く", onclick: () => openEditor(r) }))));
  return h("section", { class: "admin-section", "aria-labelledby": "adm-reports" },
    h("h2", { id: "adm-reports", class: "admin-section__title", text: "会計報告" }),
    h("p", { class: "small muted", text: "金額は、通帳・領収書などの実際の会計記録にもとづいて入力してください。未確認の数値や見込みの金額は入力しないでください。公開資料には、個人名・口座番号・メールアドレス・取引IDを書かないでください。" }),
    h("div", { class: "btn-group" },
      h("button", { class: "btn btn--primary btn--sm", type: "button", text: "新しい会計報告を作成", onclick: () => openEditor(null) })),
    state.reports.length
      ? h("div", { class: "table-wrap", role: "region", "aria-label": "会計報告の一覧（横にスクロールできます）", tabindex: 0 },
        h("table", { class: "admin-table" },
          h("thead", {}, h("tr", {}, ...["会計年度", "対象期間", "状態", "公開日", "最終更新", "操作"].map((t) => h("th", { scope: "col", text: t })))),
          h("tbody", {}, rows)))
      : h("p", { class: "muted", text: "会計報告はまだありません。" }));
}

async function openEditor(r) {
  state.editing = r ? { id: r.id, original: r, data: { ...r } } : { id: null, original: null, data: blankReport() };
  state.history = [];
  render();
  if (r) {
    try {
      const db = await getDb();
      const snap = await getDocs(query(collection(db, "financeReports", r.id, "history"), orderBy("at", "desc")));
      state.history = snap.docs.map((d) => d.data());
      page.body.querySelector("[data-history]")?.replaceChildren(historyList());
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
    h("span", { text: `${x.action}（${REPORT_STATUSES[x.status] || x.status}）` }),
    x.note ? h("span", { class: "history-list__note", text: `メモ：${x.note}` }) : null,
    h("span", { class: "admin-table__meta", text: `操作：${x.by}` }))));
}

function editorSection() {
  const ed = state.editing;
  const d = ed.data;
  const status = ed.original ? ed.original.status : "draft";
  const editable = status === "draft" || status === "review_requested";
  const correcting = status === "published";
  const numsEditable = editable || correcting;

  const num = (k) => h("input", { type: "number", min: 0, step: 1, value: d[k], inputmode: "numeric", disabled: !numsEditable });
  const inp = {
    title: textInput(d.title, { maxlength: 40, placeholder: "例：2026年度", disabled: !numsEditable }),
    periodStart: h("input", { type: "date", value: d.periodStart, disabled: !numsEditable }),
    periodEnd: h("input", { type: "date", value: d.periodEnd, disabled: !numsEditable }),
    achievements: h("textarea", { rows: 5, maxlength: 3000, value: d.achievements, disabled: !numsEditable }),
    note: h("textarea", { rows: 2, maxlength: 300 }),
    correction: h("textarea", { rows: 2, maxlength: 500 }),
  };
  NUM_FIELDS.forEach((k) => { inp[k] = num(k); });

  const totals = h("dl", { class: "info-list admin-totals", "aria-live": "polite" });
  const checks = h("div", { "aria-live": "polite" });
  const msg = h("p", { class: "form-status", role: "status" });

  const collect = () => {
    const r = { ...d };
    ["title", "periodStart", "periodEnd", "achievements"].forEach((k) => { r[k] = inp[k].value.trim(); });
    NUM_FIELDS.forEach((k) => { r[k] = inp[k].value === "" ? NaN : Number(inp[k].value); });
    return { ...r, ...computeTotals(r) };
  };

  const update = () => {
    const r = collect();
    const row = (dt, dd) => h("div", { class: "info-list__row" }, h("dt", { text: dt }), h("dd", { text: dd }));
    totals.replaceChildren(
      row("収入合計", yen(r.totalIncome)),
      row("支出合計", yen(r.totalExpense)),
      row("年度末残高（期首残高＋収入合計−支出合計）", yen(r.closingBalance)));
    const errors = reportErrors(r);
    const warnings = [];
    if (r.periodStart && r.periodEnd) {
      const ref = confirmedSponsorshipTotal(state.records, r.periodStart, r.periodEnd);
      if (ref !== r.incomeSponsorship) {
        warnings.push(`協賛金収入（${yen(r.incomeSponsorship)}）が、協賛記録で期間内に入金確認した金額の合計（返金を除く：${yen(ref)}）と一致しません。二重計上・記録漏れがないか確認してください。`);
      }
    }
    if (r.carryover !== r.closingBalance) warnings.push("翌年度繰越額が年度末残高と異なります。差額の理由を確認してください。");
    const overlap = state.reports.filter((x) => x.id !== ed.id && r.periodStart && r.periodEnd
      && x.periodStart <= r.periodEnd && r.periodStart <= x.periodEnd);
    if (overlap.length) warnings.push(`対象期間が他の報告（${overlap.map((x) => x.title).join("、")}）と重なっています。二重計上に注意してください。`);
    checks.replaceChildren(...[
      errors.length ? h("ul", { class: "warn-list warn-list--error" }, errors.map((x) => h("li", { text: x }))) : null,
      warnings.length ? h("ul", { class: "warn-list" }, warnings.map((x) => h("li", { text: x }))) : null,
      !errors.length && !warnings.length ? h("p", { class: "ok-mark", text: "整合性の問題はありません。" }) : null,
    ].filter(Boolean));
    return errors;
  };

  const save = async (nextStatus, action, { confirmText, extra = {} } = {}) => {
    const r = collect();
    if (update().length && nextStatus !== "confirmed_unpublish") {
      msg.textContent = "入力内容にエラーがあります。確認事項を直してから保存してください。";
      msg.classList.add("is-error");
      return;
    }
    if (confirmText && !window.confirm(confirmText)) return;
    try {
      const db = await getDb();
      const ref = ed.id ? doc(db, "financeReports", ed.id) : doc(collection(db, "financeReports"));
      const histRef = doc(collection(db, "financeReports", ref.id, "history"));
      const { id: _drop, ...rest } = r;
      const data = {
        ...rest,
        ...extra,
        status: nextStatus === "confirmed_unpublish" ? "confirmed" : nextStatus,
        lastHistoryId: histRef.id,
        createdAt: ed.original ? ed.original.createdAt : serverTimestamp(),
        updatedAt: serverTimestamp(),
      };
      if (ed.original && !numsEditable) {
        // 確認済みの報告は数値を変えない
        NUM_FIELDS.concat(["title", "periodStart", "periodEnd", "achievements", "totalIncome", "totalExpense", "closingBalance"])
          .forEach((k) => { data[k] = ed.original[k]; });
      }
      const batch = writeBatch(db);
      batch.set(ref, data);
      batch.set(histRef, { at: serverTimestamp(), by: page.user.email, action, note: inp.note.value.trim(), status: data.status });
      await batch.commit();
      await load();
      page.setStatus("保存しました。");
    } catch (err) {
      msg.textContent = errorMessage(err);
      msg.classList.add("is-error");
    }
  };

  const buttons = [];
  const b = (text, onclick, variant = "outline") => buttons.push(h("button", { class: `btn btn--${variant} btn--sm`, type: "button", text, onclick }));
  if (editable) {
    b("下書きとして保存", () => save("draft", ed.original ? "下書きを保存" : "下書きを作成"), "primary");
    b("成人の確認者に確認を依頼", () => save("review_requested", "確認を依頼"));
    b("確認済みにする（成人の確認者のみ）", () => save("confirmed", "確認済みにした", {
      extra: { confirmedAt: serverTimestamp() },
      confirmText: "この会計報告を「確認済み」にします。\n\n通帳・領収書・振込記録などの実際の会計記録と照合し、金額が正しいこと、公開資料に個人情報が含まれていないことを確認しましたか？",
    }));
    if (ed.original) {
      b("この下書きを削除", async () => {
        if (!window.confirm("この下書きを削除します。よろしいですか？")) return;
        try {
          const db = await getDb();
          await deleteDoc(doc(db, "financeReports", ed.id));
          await load();
          page.setStatus("下書きを削除しました。");
        } catch (err) {
          msg.textContent = errorMessage(err);
          msg.classList.add("is-error");
        }
      });
    }
  } else if (status === "confirmed") {
    b("ウェブサイトで公開する（成人の確認者のみ）", () => save("published", "公開した", {
      extra: { publishedOn: todayJST() },
      confirmText: "この会計報告を一般公開します。よろしいですか？",
    }), "primary");
    b("差し戻す（成人の確認者のみ）", () => save("draft", "差し戻した", { extra: { confirmedAt: null, publishedOn: "" } }));
  } else if (status === "published") {
    b("訂正を保存する（成人の確認者のみ）", () => {
      const text = inp.correction.value.trim();
      if (!text) {
        msg.textContent = "訂正の内容を入力してください（訂正履歴として公開されます）。";
        msg.classList.add("is-error");
        return;
      }
      save("published", "公開後に訂正した", {
        extra: { corrections: [...(d.corrections || []), { date: todayJST(), text }], confirmedAt: serverTimestamp() },
        confirmText: "訂正を保存して公開します。訂正内容は訂正履歴として公開されます。よろしいですか？",
      });
    }, "primary");
    b("公開を取り下げる", () => save("confirmed_unpublish", "公開を取り下げた", {
      extra: { publishedOn: "" },
      confirmText: "この会計報告の公開を取り下げます（数値は変わりません）。よろしいですか？",
    }));
  }
  b("閉じる", () => { state.editing = null; render(); });

  const group = (legend, fields) => h("fieldset", { class: "admin-fieldset" }, h("legend", { text: legend }),
    h("div", { class: "admin-grid" }, fields.map(([k, label]) => field(`${label}（円）`, inp[k]))));

  const form = h("div", { class: "card admin-form", "data-editor": true },
    h("h3", { class: "card__title", text: ed.original ? `${d.title} 会計報告（${REPORT_STATUSES[status]}）` : "新しい会計報告" }),
    !numsEditable ? h("p", { class: "notice-box", text: "確認済みの報告の数値は変更できません。直す必要がある場合は、成人の確認者が差し戻してください。" }) : null,
    correcting ? h("p", { class: "notice-box", text: "公開中の報告を直す場合は、数値を修正し、訂正の内容を入力して「訂正を保存する」を押してください（成人の確認者のみ）。訂正履歴は公開され、削除できません。" }) : null,
    h("fieldset", { class: "admin-fieldset" }, h("legend", { text: "対象期間" }),
      h("div", { class: "admin-grid" },
        field("会計年度の名称", inp.title),
        field("開始日", inp.periodStart),
        field("終了日", inp.periodEnd),
        field("期首残高（円）", inp.openingBalance))),
    group("収入", INCOME_FIELDS),
    group("支出", EXPENSE_FIELDS),
    h("fieldset", { class: "admin-fieldset" }, h("legend", { text: "残高" }),
      totals,
      h("div", { class: "admin-grid" },
        field("翌年度繰越額（円）", inp.carryover, { hint: "年度末残高のうち、翌年度に繰り越す金額。" }),
        field("うち予備費（円）", inp.reserve, { hint: "翌年度繰越額のうち、予備費とする金額。" }))),
    field("活動実績・主な成果（公開されます）", inp.achievements, { hint: "個人名・メールアドレス・口座番号などは書かないでください。" }),
    correcting ? field("訂正の内容（公開されます）", inp.correction) : null,
    field("この操作のメモ（履歴に残ります・非公開）", inp.note),
    h("div", { class: "admin-checks" }, h("p", { class: "small", text: "確認事項：" }), checks),
    h("div", { class: "btn-group" }, buttons),
    msg,
    ed.original ? h("div", {}, h("h4", { class: "admin-subtitle", text: "操作履歴（削除・変更できません）" }), h("div", { "data-history": true }, historyList())) : null);

  form.addEventListener("input", update);
  update();
  return h("section", { class: "admin-section", "aria-label": "会計報告の編集" }, form);
}

page = startStaffPage({
  onSignedIn: async (p) => {
    page = p;
    await load();
  },
});
