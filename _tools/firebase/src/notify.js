// お知らせの受け取り登録（notify.html）
// 送信内容は Firestore の updateSignups コレクションに保存します（運営の管理者だけが読めます）。
import { collection, addDoc, serverTimestamp } from "firebase/firestore/lite";
import { getDb, SIGNUP_COLLECTION } from "./firebase-init.js";
import { buildSignup } from "./notify-logic.js";

const form = document.querySelector("[data-notify-form]");

if (form) {
  const summary = form.querySelector("[data-error-summary]");
  const summaryList = summary.querySelector("ul");
  const status = form.querySelector("[data-form-status]");
  const submitBtn = form.querySelector("[type=submit]");
  const thanks = document.querySelector("[data-thanks]");

  const clearErrors = () => {
    form.querySelectorAll(".field__error").forEach((el) => {
      el.hidden = true;
      el.textContent = "";
    });
    form.querySelectorAll("[aria-invalid]").forEach((el) => el.removeAttribute("aria-invalid"));
  };

  const showErrors = (errors) => {
    errors.forEach(({ id, message }) => {
      const el = document.getElementById(`${id}-error`);
      if (el) {
        el.textContent = message;
        el.hidden = false;
      }
      document.getElementById(id)?.setAttribute("aria-invalid", "true");
    });
    summaryList.replaceChildren(...errors.map(({ id, message }) => {
      const li = document.createElement("li");
      const a = document.createElement("a");
      a.href = `#${id}`;
      a.textContent = message;
      a.addEventListener("click", (e) => {
        e.preventDefault();
        const target = document.getElementById(id);
        (target.matches("fieldset") ? target.querySelector("input") : target).focus();
      });
      li.append(a);
      return li;
    }));
    summary.hidden = false;
    summary.focus();
  };

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    status.textContent = "";
    status.classList.remove("is-error");
    clearErrors();

    // スパム対策：人には見えない入力欄に値があれば保存しない
    if (form.elements.website.value) {
      showThanks();
      return;
    }

    const { errors, data } = buildSignup({
      email: form.elements.email.value,
      topics: [...form.querySelectorAll('input[name="topic"]:checked')].map((b) => b.value),
      consent: form.elements.consent.checked,
    });
    if (errors.length) {
      showErrors(errors);
      return;
    }
    summary.hidden = true;

    submitBtn.disabled = true;
    submitBtn.setAttribute("aria-busy", "true");
    status.textContent = "登録しています…";
    try {
      const db = await getDb();
      await addDoc(collection(db, SIGNUP_COLLECTION), { ...data, timestamp: serverTimestamp() });
      showThanks();
    } catch (err) {
      console.error(err);
      status.classList.add("is-error");
      status.textContent = err && err.message === "firebase-config-unavailable"
        ? "現在この環境からは登録できません。公開中のサイトから登録するか、時間をおいて再度お試しください。"
        : "登録できませんでした。通信環境を確認して、もう一度お試しください。解決しない場合はお問い合わせページのメールアドレスまでご連絡ください。";
    } finally {
      submitBtn.disabled = false;
      submitBtn.removeAttribute("aria-busy");
    }
  });

  function showThanks() {
    form.hidden = true;
    form.reset();
    thanks.hidden = false;
    thanks.focus();
    thanks.scrollIntoView({ block: "start" });
  }
}
