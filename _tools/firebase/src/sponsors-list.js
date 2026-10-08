// 協賛者一覧（sponsors.html）
// 公開用のコレクション（publicSponsors）だけを読みます。個人情報・入金情報は含まれていません。
// 表示する文字は textContent で設定し、HTMLとして解釈しません。
import { collection, getDocs } from "firebase/firestore/lite";
import { getDb } from "./firebase-init.js";
import { RANKS, RANK_ORDER, KINDS, visibleSponsors, isSafeHttpsUrl, isSafeLogoFile, todayJST } from "./sponsor-logic.js";

const root = document.querySelector("[data-supporters]");

function make(tag, className, text) {
  const n = document.createElement(tag);
  if (className) n.className = className;
  if (text) n.textContent = text;
  return n;
}

function card(e) {
  const li = make("li", `supporter supporter--${e.rank}`);
  if (e.logoFile && isSafeLogoFile(e.logoFile)) {
    const img = make("img", "supporter__logo");
    img.src = `images/sponsors/${e.logoFile}`;
    img.alt = "";
    img.loading = "lazy";
    img.decoding = "async";
    li.append(img);
  }
  const name = e.anonymous ? "匿名の方" : e.displayName;
  if (e.websiteUrl && isSafeHttpsUrl(e.websiteUrl)) {
    const a = make("a", "supporter__name", name);
    a.href = e.websiteUrl;
    a.target = "_blank";
    a.rel = "noopener noreferrer nofollow sponsored";
    a.append(make("span", "visually-hidden", "（公式サイト・新しいタブで開きます）"));
    li.append(a);
  } else {
    li.append(make("p", "supporter__name", name));
  }
  li.append(make("p", "supporter__kind", KINDS[e.kind] || ""));
  if (e.intro) li.append(make("p", "supporter__intro", e.intro));
  return li;
}

async function main() {
  const loading = root.querySelector("[data-supporters-loading]");
  try {
    const db = await getDb();
    const snap = await getDocs(collection(db, "publicSponsors"));
    const list = visibleSponsors(snap.docs.map((d) => d.data()), todayJST());
    loading.remove();
    if (!list.length) {
      document.querySelector("[data-supporters-empty]").hidden = false;
      return;
    }
    RANK_ORDER.forEach((rank) => {
      const items = list.filter((e) => e.rank === rank);
      if (!items.length) return;
      const sec = make("section", `supporters__group supporters__group--${rank}`);
      sec.append(make("h3", "supporters__heading", RANKS[rank]));
      const ul = make("ul", "supporters__list");
      ul.append(...items.map(card));
      sec.append(ul);
      root.append(sec);
    });
  } catch (err) {
    loading.remove();
    document.querySelector("[data-supporters-error]").hidden = false;
  }
}

if (root) main();
