// 判定ロジックのテスト（エミュレーター不要）
import { describe, it } from "node:test";
import assert from "node:assert/strict";
import {
  rankFor, amountFor, isSafeHttpsUrl, isSafeLogoFile, isDate, publicEntryFromRecord, listingBlockers,
  recordWarnings, findDuplicates, visibleSponsors, confirmedSponsorshipTotal, computeTotals, reportErrors,
  containsSensitive,
} from "../src/sponsor-logic.js";
import { baseRecord, baseReport } from "./helpers.js";

describe("口数と掲載ランク（テスト要件6）", () => {
  it("1〜4口は通常、5〜9口は優遇、10口以上は特別優遇", () => {
    assert.equal(rankFor(1), "standard");
    assert.equal(rankFor(4), "standard");
    assert.equal(rankFor(5), "preferred");
    assert.equal(rankFor(9), "preferred");
    assert.equal(rankFor(10), "special");
    assert.equal(rankFor(250), "special");
    assert.equal(rankFor(0), null);
    assert.equal(rankFor(2.5), null);
    assert.equal(rankFor("5"), null);
  });

  it("個人は1口1,000円、企業・団体は1口10,000円", () => {
    assert.equal(amountFor("individual", 3), 3000);
    assert.equal(amountFor("organization", 3), 30000);
    assert.equal(amountFor("other", 3), null);
    assert.equal(amountFor("individual", 0), null);
  });
});

describe("入力値の検証（XSS・不正なリンク対策）", () => {
  it("https の正しいURLだけを受け付ける", () => {
    assert.ok(isSafeHttpsUrl("https://example.com"));
    assert.ok(isSafeHttpsUrl("https://www.example.co.jp/path?a=1"));
    for (const bad of ["http://example.com", "javascript:alert(1)", "https://example.com/\"><script>",
      "https://user:pw@example.com", "https://localhost", "data:text/html,x", "https://exa mple.com", ""]) {
      assert.equal(isSafeHttpsUrl(bad), false, bad);
    }
  });

  it("ロゴは images/sponsors/ 内の画像ファイル名だけ", () => {
    assert.ok(isSafeLogoFile("example-co.png"));
    for (const bad of ["../x.png", "a/b.png", "x.svg", "X.PNG", "https://a.example/x.png", ".png"]) {
      assert.equal(isSafeLogoFile(bad), false, bad);
    }
  });

  it("日付の形式と実在を確認する", () => {
    assert.ok(isDate("2026-02-28"));
    assert.equal(isDate("2026-02-30"), false);
    assert.equal(isDate("2026/02/01"), false);
  });

  it("公開資料に含めてはいけない情報を検出する", () => {
    assert.ok(containsSensitive("連絡は a@example.com まで"));
    assert.ok(containsSensitive("口座番号 1234567"));
    assert.ok(containsSensitive("口座番号 １２３４５６７"));
    assert.equal(containsSensitive("2026年12月に合奏を開始"), false);
  });
});

describe("公開する内容（テスト要件4・5）", () => {
  const rec = (o) => baseRecord({
    kind: "organization", units: 10, amount: 100000, rank: "special", listing: "named", displayName: "株式会社テスト",
    websiteUrl: "https://example.com", logoFile: "test.png", intro: "紹介文", listingStart: "2026-10-01", ...o,
  });

  it("特別優遇の企業・団体は、名前・URL・ロゴ・紹介文を公開する", () => {
    const p = publicEntryFromRecord(rec());
    assert.deepEqual(
      [p.displayName, p.websiteUrl, p.logoFile, p.intro],
      ["株式会社テスト", "https://example.com", "test.png", "紹介文"],
    );
  });

  it("ランクに含まれない特典は公開しない", () => {
    const p = publicEntryFromRecord(rec({ units: 5, amount: 50000, rank: "preferred" }));
    assert.equal(p.websiteUrl, "https://example.com");
    assert.equal(p.logoFile, "");
    assert.equal(p.intro, "");
    const s = publicEntryFromRecord(rec({ units: 1, amount: 10000, rank: "standard" }));
    assert.equal(s.websiteUrl, "");
  });

  it("個人の公式サイトURL・ロゴは公開しない", () => {
    const p = publicEntryFromRecord(rec({ kind: "individual", amount: 10000 }));
    assert.equal(p.websiteUrl, "");
    assert.equal(p.logoFile, "");
  });

  it("匿名を選んだ場合は名前も特典も公開しない", () => {
    const p = publicEntryFromRecord(rec({ listing: "anonymous" }));
    assert.equal(p.anonymous, true);
    assert.deepEqual([p.displayName, p.websiteUrl, p.logoFile, p.intro], ["", "", "", ""]);
  });

  it("公開内容に個人情報・入金情報が含まれない", () => {
    const p = publicEntryFromRecord(rec());
    for (const k of ["email", "contactName", "paidAmount", "amount", "units", "internalId", "notes"]) {
      assert.equal(k in p, false, k);
    }
  });

  it("同意・入金がない記録は掲載できない理由を返す", () => {
    const r = baseRecord({ status: "payment_confirmed", paidAmount: 3000, paymentConfirmedOn: "2026-10-05", listingStart: "2026-10-10" });
    assert.ok(listingBlockers(r).some((m) => m.includes("同意")));
    assert.ok(listingBlockers({ ...r, listing: "none" }).some((m) => m.includes("掲載しない")));
    assert.ok(listingBlockers(baseRecord({ consentListing: true, consentRecordedOn: "2026-10-01" })).some((m) => m.includes("入金")));
    assert.deepEqual(listingBlockers({ ...r, consentListing: true, consentRecordedOn: "2026-10-02" }), []);
  });

  it("掲載期間内のものだけを、ランク順に表示する", () => {
    const e = (o) => ({ anonymous: false, displayName: "x", rank: "standard", listingStart: "2026-01-01", listingEnd: "", ...o });
    const list = visibleSponsors([
      e({ displayName: "通常" }),
      e({ displayName: "特別", rank: "special" }),
      e({ displayName: "終了", listingEnd: "2026-05-31" }),
      e({ displayName: "未開始", listingStart: "2026-12-01" }),
      e({ displayName: "", anonymous: true }),
    ], "2026-10-08");
    assert.deepEqual(list.map((x) => x.displayName), ["特別", "通常", ""]);
  });
});

describe("記録の確認（テスト要件8・9）", () => {
  it("口数と入金額の不一致、同意のない掲載を警告する", () => {
    const w = recordWarnings(baseRecord({ status: "payment_confirmed", paidAmount: 2000, paymentConfirmedOn: "2026-10-05" }));
    assert.ok(w.some((m) => m.includes("一致していません")));
    assert.ok(w.some((m) => m.includes("掲載同意")));
    assert.ok(recordWarnings(baseRecord({ units: 5, amount: 5000 })).some((m) => m.includes("ランク")));
  });

  it("入金前なのに入金額がある記録を警告する", () => {
    assert.ok(recordWarnings(baseRecord({ paidAmount: 3000 })).some((m) => m.includes("入金前")));
  });

  it("重複登録の疑いを検出する（取消済みは除く）", () => {
    const groups = findDuplicates([
      { id: "a", ...baseRecord({ internalId: "KCO-1", displayName: "山田 花子", email: "h@example.com" }) },
      { id: "b", ...baseRecord({ internalId: "KCO-2", displayName: "山田花子", email: "other@example.com" }) },
      { id: "c", ...baseRecord({ internalId: "kco-1", displayName: "別人", email: "H@example.com" }) },
      { id: "d", ...baseRecord({ internalId: "KCO-9", displayName: "山田花子", status: "cancelled" }) },
    ]);
    const byLabel = Object.fromEntries(groups.map((g) => [g.label, g.ids.sort()]));
    assert.deepEqual(byLabel["名前"], ["a", "b"]);
    assert.deepEqual(byLabel["管理ID"], ["a", "c"]);
    assert.deepEqual(byLabel["メールアドレス"], ["a", "c"]);
  });

  it("同じ申込みから2件の記録を作ると検出する", () => {
    const groups = findDuplicates([
      { id: "a", ...baseRecord({ internalId: "A", displayName: "甲", email: "", sourceApplicationId: "app1" }) },
      { id: "b", ...baseRecord({ internalId: "B", displayName: "乙", email: "", sourceApplicationId: "app1" }) },
    ]);
    assert.deepEqual(groups.map((g) => g.label), ["申込み"]);
  });
});

describe("会計報告の集計（テスト要件7・8）", () => {
  it("収入・支出の合計と期末残高を計算する", () => {
    const t = computeTotals(baseReport());
    assert.deepEqual(t, { totalIncome: 55000, totalExpense: 45500, closingBalance: 19500 });
    assert.deepEqual(reportErrors(baseReport()), []);
  });

  it("合計や残高が一致しない報告を検出する", () => {
    assert.ok(reportErrors(baseReport({ totalIncome: 1 })).length > 0);
    assert.ok(reportErrors(baseReport({ closingBalance: 1 })).length > 0);
    assert.ok(reportErrors(baseReport({ carryover: 30000 })).length > 0);
    assert.ok(reportErrors(baseReport({ reserve: 20000 })).length > 0);
    assert.ok(reportErrors(baseReport({ expFees: -1 })).length > 0);
    assert.ok(reportErrors(baseReport({ periodStart: "2027-04-01" })).length > 0);
    assert.ok(reportErrors(baseReport({ achievements: "a@example.com" })).length > 0);
  });

  it("期間内に入金確認した協賛金を、返金を差し引いて集計する（二重計上の照合用）", () => {
    const recs = [
      baseRecord({ paidAmount: 3000, paymentConfirmedOn: "2026-05-01" }),
      baseRecord({ paidAmount: 10000, paymentConfirmedOn: "2026-06-01", refundAmount: 10000 }),
      baseRecord({ paidAmount: 5000, paymentConfirmedOn: "2027-04-01" }),
      baseRecord({ paidAmount: 0, paymentConfirmedOn: "" }),
    ];
    assert.equal(confirmedSponsorshipTotal(recs, "2026-04-01", "2027-03-31"), 3000);
  });
});
