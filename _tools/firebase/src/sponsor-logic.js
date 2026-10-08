// 協賛制度・会計報告の判定ロジック（画面とテストで共通）
//
// ※ 同じ条件を firestore.rules でもサーバー側で検証しています。
//    ここを変更したときは、firestore.rules と test/ も合わせて更新してください。

export const UNIT_PRICE = { individual: 1000, organization: 10000 };

export const KINDS = { individual: "個人", organization: "企業・団体" };

export const RANKS = {
  standard: "通常掲載",
  preferred: "優遇掲載",
  special: "特別優遇掲載",
};

export const RANK_ORDER = ["special", "preferred", "standard"];

export const STATUSES = {
  received: "申込受付",
  awaiting_payment: "入金確認待ち",
  payment_confirmed: "入金確認済み",
  awaiting_listing: "掲載確認待ち",
  listed: "掲載中",
  listing_ended: "掲載終了",
  cancelled: "取消・返金対応",
};

// 入金確認が済んでいることを前提とする状態
export const PAID_STATUSES = ["payment_confirmed", "awaiting_listing", "listed", "listing_ended"];
// 入金前の状態
export const UNPAID_STATUSES = ["received", "awaiting_payment"];

export const LISTING = {
  named: "名前を掲載する",
  anonymous: "匿名で掲載する",
  none: "掲載しない",
};

export const CONTACT_STATUSES = {
  not_contacted: "未連絡",
  contacted: "連絡済み",
  awaiting_reply: "返信待ち",
  completed: "完了",
};

export const REPORT_STATUSES = {
  draft: "下書き",
  review_requested: "確認依頼中",
  confirmed: "確認済み（未公開）",
  published: "公開中",
};

export const INCOME_FIELDS = [
  ["incomeSponsorship", "協賛金収入"],
  ["incomeOther", "その他の収入"],
];

export const EXPENSE_FIELDS = [
  ["expPractice", "練習会場費"],
  ["expConcert", "演奏会場費"],
  ["expMusic", "楽譜・音楽関連費"],
  ["expPublicity", "広報・ウェブサイト費"],
  ["expMemberSupport", "団員の負担軽減"],
  ["expOther", "その他の支出"],
  ["expFees", "決済・振込手数料"],
];

export const MAX_UNITS = 1000;

// ---------------------------------------------------------------- 協賛

export function rankFor(units) {
  if (!Number.isInteger(units) || units < 1) return null;
  if (units >= 10) return "special";
  if (units >= 5) return "preferred";
  return "standard";
}

export function amountFor(kind, units) {
  const price = UNIT_PRICE[kind];
  if (!price || !Number.isInteger(units) || units < 1) return null;
  return price * units;
}

// 公式サイトURL：https のみ。ユーザー名・パスワード付きや空白・引用符などを含むものは不可
const URL_RE = /^https:\/\/[A-Za-z0-9.-]+(:[0-9]{1,5})?(\/[^\s"'<>\\]*)?$/;

export function isSafeHttpsUrl(value) {
  if (typeof value !== "string" || value.length > 300 || !URL_RE.test(value)) return false;
  try {
    const u = new URL(value);
    return u.protocol === "https:" && !u.username && !u.password && u.hostname.includes(".");
  } catch {
    return false;
  }
}

// ロゴ：images/sponsors/ に運営が確認して置いた画像のファイル名だけを指定できる
const LOGO_RE = /^[a-z0-9][a-z0-9_-]{0,60}\.(png|jpg|jpeg|webp)$/;

export function isSafeLogoFile(value) {
  return typeof value === "string" && LOGO_RE.test(value);
}

export const EMAIL_RE = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;

const DATE_RE = /^\d{4}-\d{2}-\d{2}$/;

export function isDate(value) {
  if (typeof value !== "string" || !DATE_RE.test(value)) return false;
  const d = new Date(`${value}T00:00:00Z`);
  return !Number.isNaN(d.getTime()) && d.toISOString().slice(0, 10) === value;
}

// 公開してよい項目だけを、掲載ランク・区分・匿名の選択に応じて取り出す
export function publicEntryFromRecord(rec) {
  const named = rec.listing === "named";
  const org = rec.kind === "organization";
  return {
    kind: rec.kind,
    anonymous: rec.listing === "anonymous",
    displayName: named ? rec.displayName : "",
    rank: rec.rank,
    websiteUrl: named && org && (rec.rank === "preferred" || rec.rank === "special") ? rec.websiteUrl : "",
    logoFile: named && org && rec.rank === "special" ? rec.logoFile : "",
    intro: named && rec.rank === "special" ? rec.intro : "",
    listingStart: rec.listingStart,
    listingEnd: rec.listingEnd,
  };
}

// 掲載中にしてよいか（だめな理由の一覧を返す）
export function listingBlockers(rec) {
  const reasons = [];
  if (!PAID_STATUSES.includes(rec.status)) reasons.push("入金確認が済んでいません");
  if (!(rec.paidAmount > 0) || !isDate(rec.paymentConfirmedOn)) reasons.push("入金確認日・入金額が記録されていません");
  if (rec.paidAmount !== rec.amount) reasons.push("入金額が協賛金額と一致していません");
  if (rec.listing === "none") reasons.push("掲載しない希望です");
  if (rec.consentListing !== true || !isDate(rec.consentRecordedOn)) reasons.push("掲載への同意が記録されていません");
  if (rec.listing === "named" && !rec.displayName) reasons.push("表示名がありません");
  if (!isDate(rec.listingStart)) reasons.push("掲載開始日がありません");
  if (rec.listingEnd && (!isDate(rec.listingEnd) || rec.listingEnd < rec.listingStart)) {
    reasons.push("掲載終了日が正しくありません");
  }
  return reasons;
}

// 記録の確認事項（管理画面に警告として表示）
export function recordWarnings(rec) {
  const w = [];
  if (rankFor(rec.units) !== rec.rank) w.push("口数と掲載ランクが一致していません");
  if (amountFor(rec.kind, rec.units) !== rec.amount) w.push("口数と協賛金額が一致していません");
  if (PAID_STATUSES.includes(rec.status) && rec.paidAmount !== rec.amount) {
    w.push(`入金額（${yen(rec.paidAmount)}）と協賛金額（${yen(rec.amount)}）が一致していません`);
  }
  if (UNPAID_STATUSES.includes(rec.status) && rec.paidAmount > 0) w.push("入金前の状態なのに入金額が入っています");
  if (rec.listing !== "none" && rec.consentListing !== true) w.push("掲載を希望していますが、掲載同意が記録されていません");
  if (rec.status === "listed") listingBlockers(rec).forEach((r) => w.push(`掲載中ですが、${r}`));
  if (rec.websiteUrl && !isSafeHttpsUrl(rec.websiteUrl)) w.push("公式サイトURLの形式が正しくありません");
  if (rec.logoFile && !isSafeLogoFile(rec.logoFile)) w.push("ロゴのファイル名が正しくありません");
  if (rec.status === "cancelled" && rec.paidAmount > 0 && !rec.refundApprovedOn) {
    w.push("入金済みの取消ですが、成人の確認者による返金承認が記録されていません");
  }
  return w;
}

const norm = (s) => String(s || "").normalize("NFKC").replace(/\s+/g, "").toLowerCase();

// 重複の疑いがある記録の組み合わせを返す（取消済みの記録は除く）
export function findDuplicates(records) {
  const groups = new Map();
  const add = (key, label, rec) => {
    if (!key) return;
    const k = `${label}:${key}`;
    if (!groups.has(k)) groups.set(k, { label, ids: [] });
    groups.get(k).ids.push(rec.id);
  };
  records.filter((r) => r.status !== "cancelled").forEach((r) => {
    add(norm(r.internalId), "管理ID", r);
    add(r.kind + ":" + norm(r.displayName || r.contactName), "名前", r);
    add(norm(r.email), "メールアドレス", r);
    add(r.sourceApplicationId, "申込み", r);
  });
  return [...groups.values()].filter((g) => g.ids.length > 1);
}

// 一般公開ページで表示する協賛者（掲載期間内のもの）
export function visibleSponsors(entries, today) {
  return entries
    .filter((e) => isDate(e.listingStart) && e.listingStart <= today && (!e.listingEnd || today <= e.listingEnd))
    .sort((a, b) => RANK_ORDER.indexOf(a.rank) - RANK_ORDER.indexOf(b.rank)
      || (a.anonymous - b.anonymous)
      || a.listingStart.localeCompare(b.listingStart)
      || a.displayName.localeCompare(b.displayName, "ja"));
}

// 期間内に入金確認した協賛金の合計（会計報告の照合用・返金額を差し引く）
export function confirmedSponsorshipTotal(records, start, end) {
  return records
    .filter((r) => isDate(r.paymentConfirmedOn) && r.paymentConfirmedOn >= start && r.paymentConfirmedOn <= end)
    .reduce((sum, r) => sum + (r.paidAmount || 0) - (r.refundAmount || 0), 0);
}

// ---------------------------------------------------------------- 会計報告

const sum = (r, fields) => fields.reduce((s, [k]) => s + (r[k] || 0), 0);

export function computeTotals(r) {
  const totalIncome = sum(r, INCOME_FIELDS);
  const totalExpense = sum(r, EXPENSE_FIELDS);
  return { totalIncome, totalExpense, closingBalance: (r.openingBalance || 0) + totalIncome - totalExpense };
}

// 公開資料に含めてはいけない情報（メールアドレス・口座番号などの長い数字）の検出
export function containsSensitive(text) {
  return typeof text === "string" && (/@/.test(text) || /[0-9０-９]{7,}/.test(text));
}

export function reportErrors(r) {
  const e = [];
  const ints = ["openingBalance", ...INCOME_FIELDS.map(([k]) => k), ...EXPENSE_FIELDS.map(([k]) => k), "carryover", "reserve"];
  ints.forEach((k) => {
    if (!Number.isInteger(r[k]) || r[k] < 0) e.push(`${k}：0以上の整数（円）を入力してください`);
  });
  if (!r.title || r.title.length > 40) e.push("会計年度の名称を入力してください（40文字以内）");
  if (!isDate(r.periodStart) || !isDate(r.periodEnd) || r.periodStart > r.periodEnd) e.push("対象期間が正しくありません");
  const t = computeTotals(r);
  if (r.totalIncome !== t.totalIncome) e.push("収入合計が内訳の合計と一致していません");
  if (r.totalExpense !== t.totalExpense) e.push("支出合計が内訳の合計と一致していません");
  if (r.closingBalance !== t.closingBalance) e.push("年度末残高が「期首残高＋収入合計−支出合計」と一致していません");
  if (r.carryover > r.closingBalance) e.push("翌年度繰越額が年度末残高を超えています");
  if (r.reserve > r.carryover) e.push("予備費が翌年度繰越額を超えています");
  if (containsSensitive(r.title) || containsSensitive(r.achievements)) {
    e.push("公開資料にメールアドレスや口座番号のような数字（7桁以上）を含めないでください");
  }
  if (typeof r.achievements !== "string" || r.achievements.length > 3000) e.push("活動実績は3000文字以内にしてください");
  return e;
}

export function yen(n) {
  return Number.isInteger(n) ? `${n.toLocaleString("ja-JP")}円` : "—";
}

// 日本時間の今日（YYYY-MM-DD）
export function todayJST(now = new Date()) {
  return now.toLocaleDateString("sv-SE", { timeZone: "Asia/Tokyo" });
}
