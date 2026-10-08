// 会計報告（report.html）
// 成人の確認者が確認・公開した報告（status == "published"）だけを読みます。
import { collection, getDocs, query, where } from "firebase/firestore/lite";
import { getDb } from "./firebase-init.js";
import { INCOME_FIELDS, EXPENSE_FIELDS, computeTotals, yen } from "./sponsor-logic.js";

const root = document.querySelector("[data-reports]");

function make(tag, className, text) {
  const n = document.createElement(tag);
  if (className) n.className = className;
  if (text !== undefined) n.textContent = text;
  return n;
}

function tableRow(label, value, cls) {
  const tr = make("tr", cls);
  tr.append(make("th", "", label));
  const td = make("td", "num", yen(value));
  tr.append(td);
  return tr;
}

function table(caption, rows) {
  const t = make("table", "data-table report-table");
  t.append(make("caption", "", caption));
  const tb = make("tbody");
  tb.append(...rows);
  t.append(tb);
  const wrap = make("div", "table-wrap");
  wrap.append(t);
  return wrap;
}

function render(r) {
  const art = make("article", "card report");
  art.append(make("h3", "report__title", `${r.title} 会計報告`));
  art.append(make("p", "report__meta", `対象期間：${r.periodStart} 〜 ${r.periodEnd}　／　公開日：${r.publishedOn}`));
  const badge = make("p", "report__badge", "成人の確認者による確認済み");
  art.append(badge);

  // 公開データの整合性を表示側でも確認する
  const t = computeTotals(r);
  const consistent = t.totalIncome === r.totalIncome && t.totalExpense === r.totalExpense
    && t.closingBalance === r.closingBalance;

  art.append(table("収入", [
    ...INCOME_FIELDS.map(([k, label]) => tableRow(label, r[k])),
    tableRow("収入合計", r.totalIncome, "is-total"),
  ]));
  art.append(table("支出", [
    ...EXPENSE_FIELDS.map(([k, label]) => tableRow(label, r[k])),
    tableRow("支出合計", r.totalExpense, "is-total"),
  ]));
  art.append(table("残高", [
    tableRow("期首残高", r.openingBalance),
    tableRow("年度末残高", r.closingBalance, "is-total"),
    tableRow("翌年度繰越額", r.carryover),
    tableRow("うち予備費", r.reserve),
  ]));
  if (!consistent) {
    art.append(make("p", "admin-status is-error", "この報告の合計値に不整合があります。運営に確認中です。"));
  }
  if (r.achievements) {
    art.append(make("h4", "report__subtitle", "活動実績・主な成果"));
    art.append(make("p", "report__text", r.achievements));
  }
  if (Array.isArray(r.corrections) && r.corrections.length) {
    art.append(make("h4", "report__subtitle", "訂正履歴"));
    const ul = make("ul", "dash-list");
    r.corrections.forEach((c) => ul.append(make("li", "", `${c.date}：${c.text}`)));
    art.append(ul);
  }
  return art;
}

async function main() {
  const loading = root.querySelector("[data-reports-loading]");
  try {
    const db = await getDb();
    const snap = await getDocs(query(collection(db, "financeReports"), where("status", "==", "published")));
    const list = snap.docs.map((d) => d.data()).sort((a, b) => b.periodStart.localeCompare(a.periodStart));
    loading.remove();
    if (!list.length) {
      document.querySelector("[data-reports-empty]").hidden = false;
      return;
    }
    root.append(...list.map(render));
  } catch (err) {
    loading.remove();
    document.querySelector("[data-reports-error]").hidden = false;
  }
}

if (root) main();
