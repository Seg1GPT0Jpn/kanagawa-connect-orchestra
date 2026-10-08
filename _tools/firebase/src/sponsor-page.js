// ご支援・協賛のご案内（sponsor.html）
// ・確定済みの掲載特典を表示する
// ・成人の確認者が受付を開始したときだけ、申込みフォームを表示する
//   （受付開始前の送信は Firestore Security Rules でも拒否されます）
// ※ 振込先・支払いボタン・決済リンクはこのページに表示しません。
import { collection, addDoc, doc, getDoc, serverTimestamp } from "firebase/firestore/lite";
import { getDb } from "./firebase-init.js";
import { amountFor, rankFor, RANKS, isSafeHttpsUrl, EMAIL_RE, yen } from "./sponsor-logic.js";

const formSection = document.querySelector("[data-sponsor-form-section]");

async function loadSettings() {
  try {
    const db = await getDb();
    const snap = await getDoc(doc(db, "settings", "sponsorship"));
    return snap.exists() ? snap.data() : null;
  } catch (err) {
    return null; // 読み込めない場合は「準備中」のまま
  }
}

function applySettings(s) {
  if (!s) return;
  if (s.benefitsConfirmed && s.benefits) {
    Object.entries(s.benefits).forEach(([key, text]) => {
      const cell = document.querySelector(`[data-benefit="${key}"]`);
      if (cell && typeof text === "string" && text) cell.textContent = text;
    });
    const note = document.querySelector("[data-benefits-note]");
    if (note) note.textContent = "※ 掲載特典の内容は、成人の確認者の確認を経て確定したものです。";
  }
  if (s.acceptingApplications && s.benefitsConfirmed && formSection) {
    const banner = document.querySelector("[data-sponsor-status]");
    if (banner) {
      banner.querySelector(".status-banner__label").textContent = "お申込み受付中";
      banner.querySelector("[data-sponsor-status-text]").textContent =
        "協賛のお申込みを受け付けています。お申込み後、担当者からお支払い方法をご連絡します。それまではお振り込みなどをなさらないでください。";
    }
    formSection.hidden = false;
    setupForm();
  }
}

function setupForm() {
  const form = formSection.querySelector("[data-sponsor-form]");
  const summary = form.querySelector("[data-error-summary]");
  const status = form.querySelector("[data-form-status]");
  const submitBtn = form.querySelector("[type=submit]");
  const thanks = formSection.querySelector("[data-thanks]");
  const sumEl = form.querySelector("[data-sponsor-summary]");
  const el = form.elements;

  const kind = () => el.kind.value;
  const listing = () => el.listing.value;

  function sync() {
    const org = kind() === "organization";
    form.querySelectorAll("[data-org-only]").forEach((n) => { n.hidden = !org; });
    form.querySelectorAll("[data-individual-only]").forEach((n) => { n.hidden = org; });
    form.querySelector("[data-label-name]").textContent = org ? "ご担当者のお名前" : "お名前";
    form.querySelector("[data-named-only]").hidden = listing() !== "named";
    form.querySelector("[data-consent-listing]").hidden = listing() === "none";
    const units = Number(el.units.value);
    sumEl.textContent = `協賛金額：${yen(amountFor(kind(), units))}（${RANKS[rankFor(units)]}）`;
  }
  form.addEventListener("change", sync);
  sync();

  function setError(id, msg, errors) {
    const e = document.getElementById(`${id}-error`);
    if (e) { e.textContent = msg; e.hidden = false; }
    const input = document.getElementById(id);
    if (input) input.setAttribute("aria-invalid", "true");
    errors.push({ id, msg });
  }

  function validate() {
    const errors = [];
    form.querySelectorAll(".field__error").forEach((n) => { n.hidden = true; n.textContent = ""; });
    form.querySelectorAll("[aria-invalid]").forEach((n) => n.removeAttribute("aria-invalid"));
    const org = kind() === "organization";
    if (org && !el.orgName.value.trim()) setError("sp-org", "企業・団体名を入力してください。", errors);
    if (!el.contactName.value.trim()) setError("sp-name", "お名前を入力してください。", errors);
    const email = el.email.value.trim();
    if (!EMAIL_RE.test(email)) setError("sp-email", "メールアドレスを正しく入力してください。", errors);
    if (listing() === "named" && !el.displayName.value.trim()) setError("sp-display", "掲載する名前を入力してください。", errors);
    const url = el.websiteUrl.value.trim();
    if (org && url && !isSafeHttpsUrl(url)) setError("sp-url", "https:// から始まる正しいURLを入力してください。", errors);
    const consentMissing = (listing() !== "none" && !el.consentListing.checked)
      || !el.consentPrivacy.checked || (!org && !el.ageConfirmed.checked);
    if (consentMissing) setError("sp-consent", "確認事項をすべて確認し、チェックを入れてください。", errors);
    return errors;
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    status.textContent = "";
    status.classList.remove("is-error");
    if (el.website.value) return; // スパム対策
    const errors = validate();
    if (errors.length) {
      summary.querySelector("ul").replaceChildren(...errors.map(({ id, msg }) => {
        const li = document.createElement("li");
        const a = document.createElement("a");
        a.href = `#${id}`;
        a.textContent = msg;
        li.append(a);
        return li;
      }));
      summary.hidden = false;
      summary.focus();
      return;
    }
    summary.hidden = true;
    const org = kind() === "organization";
    const named = listing() === "named";
    const data = {
      createdAt: serverTimestamp(),
      kind: kind(),
      contactName: el.contactName.value.trim(),
      orgName: org ? el.orgName.value.trim() : "",
      email: el.email.value.trim(),
      units: Number(el.units.value),
      listing: listing(),
      displayName: named ? el.displayName.value.trim() : "",
      websiteUrl: org && named ? el.websiteUrl.value.trim() : "",
      message: el.message.value.trim(),
      consentListing: listing() !== "none",
      consentPrivacy: true,
      ageConfirmed: org ? false : true,
    };
    submitBtn.disabled = true;
    status.textContent = "送信しています…";
    try {
      const db = await getDb();
      await addDoc(collection(db, "sponsorApplications"), data);
      form.hidden = true;
      thanks.hidden = false;
      thanks.focus();
    } catch (err) {
      status.classList.add("is-error");
      status.textContent = err && err.code === "permission-denied"
        ? "現在、お申込みを受け付けていません。お問い合わせのメールアドレスまでご連絡ください。"
        : "送信できませんでした。時間をおいて再度お試しください。";
    } finally {
      submitBtn.disabled = false;
    }
  });
}

loadSettings().then(applySettings);
