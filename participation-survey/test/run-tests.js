/*
 * 参加表明集計.gs のローカル検証（Node.js）。本番には関係しません。
 * 架空のデータだけを使います。
 *   node test/run-tests.js
 */
'use strict';
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const assert = require('assert');

function makeEnv(opts) {
  const o = opts || {};
  let idSeq = 1;
  class Sheet {
    constructor(name, values, readOnly) {
      this.name = name; this.readOnly = !!readOnly;
      this.data = (values || []).map(r => r.slice());
      this.maxRows = Math.max(this.data.length, 1000); this.maxCols = Math.max(26, ...this.data.map(r => r.length));
      this.filter = null; this.frozen = 0; this.bgs = {}; this.colors = {};
    }
    getName() { return this.name; }
    guard() { if (this.readOnly) throw new Error('読み取り専用のシートに書き込もうとしました: ' + this.name); }
    lastRow() { for (let r = this.data.length - 1; r >= 0; r--) if ((this.data[r] || []).some(v => v !== '' && v !== null && v !== undefined)) return r + 1; return 0; }
    lastCol() { let m = 0; this.data.forEach(r => { for (let c = r.length - 1; c >= 0; c--) if (r[c] !== '' && r[c] !== undefined) { m = Math.max(m, c + 1); break; } }); return m; }
    getLastRow() { return this.lastRow(); }
    getLastColumn() { return this.lastCol(); }
    getMaxRows() { return this.maxRows; }
    getMaxColumns() { return this.maxCols; }
    insertRowsAfter(a, n) { this.guard(); this.maxRows += n; }
    insertColumnsAfter(a, n) { this.guard(); this.maxCols += n; }
    getRange(r, c, nr, nc) { return new Range(this, r, c, nr || 1, nc || 1); }
    getDataRange() { return new Range(this, 1, 1, Math.max(this.lastRow(), 1), Math.max(this.lastCol(), 1)); }
    clear() { this.guard(); this.data = []; this.bgs = {}; this.colors = {}; }
    getFilter() { return this.filter; }
    setColumnWidth() { this.guard(); return this; }
    setFrozenRows(n) { this.guard(); this.frozen = n; return this; }
    setFrozenColumns() { this.guard(); return this; }
    cell(r, c) { return (this.data[r - 1] || [])[c - 1]; }
  }
  class Range {
    constructor(s, r, c, nr, nc) {
      if (r + nr - 1 > s.maxRows || c + nc - 1 > s.maxCols) throw new Error('範囲外: ' + s.name);
      Object.assign(this, { s, r, c, nr, nc });
    }
    getValues() {
      const out = [];
      for (let i = 0; i < this.nr; i++) { const line = []; for (let j = 0; j < this.nc; j++) { const v = this.s.cell(this.r + i, this.c + j); line.push(v === undefined ? '' : v); } out.push(line); }
      return out;
    }
    setValues(v) {
      this.s.guard();
      assert.strictEqual(v.length, this.nr, '行数');
      v.forEach((line, i) => { assert.strictEqual(line.length, this.nc, '列数'); line.forEach((x, j) => { const rr = this.r + i - 1; while (this.s.data.length <= rr) this.s.data.push([]); this.s.data[rr][this.c + j - 1] = x; }); });
      return this;
    }
    setBackgrounds(b) { this.s.guard(); b.forEach((l, i) => l.forEach((x, j) => { this.s.bgs[(this.r + i) + ':' + (this.c + j)] = x; })); return this; }
    setFontColors(b) { this.s.guard(); b.forEach((l, i) => l.forEach((x, j) => { this.s.colors[(this.r + i) + ':' + (this.c + j)] = x; })); return this; }
    createFilter() { this.s.guard(); this.s.filter = { remove: () => { this.s.filter = null; } }; return this.s.filter; }
  }
  ['setVerticalAlignment', 'setFontWeight', 'setWrap', 'setFontSize', 'setNumberFormat', 'setBackground', 'setNote'].forEach(m => {
    Range.prototype[m] = function () { this.s.guard(); return this; };
  });
  class SS {
    constructor(id, sheets) { this.id = id; this.sheets = sheets; }
    getId() { return this.id; }
    getSpreadsheetTimeZone() { return 'Asia/Tokyo'; }
    getSheetByName(n) { return this.sheets.find(s => s.name === n) || null; }
    insertSheet(n) { if (this.readOnlyAll) throw new Error('読み取り専用のスプレッドシートにシートを追加しようとしました'); const s = new Sheet(n, []); this.sheets.push(s); return s; }
    getSheets() { return this.sheets; }
  }
  const active = new SS('active-id-000000000000000000', o.activeSheets || []);
  const external = o.external ? new SS(o.external.id, o.external.sheets) : null;
  if (external) external.readOnlyAll = true;
  const alerts = [];
  const triggers = [];
  const fmt = (d, tz, pattern) => {
    const p = new Intl.DateTimeFormat('en-CA', { timeZone: tz, year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', hour12: false }).formatToParts(d);
    const g = t => p.find(x => x.type === t).value;
    return pattern.replace('yyyy', g('year')).replace('MM', g('month')).replace('dd', g('day')).replace('HH', g('hour').replace('24', '00')).replace('mm', g('minute'));
  };
  const ctx = {
    SpreadsheetApp: {
      getActiveSpreadsheet: () => active,
      openById: id => { if (external && id === external.id) return external; throw new Error('not found'); },
      getUi: () => { if (o.noUi) throw new Error('no ui'); return { alert: (t, m) => alerts.push(m), ButtonSet: { OK: 'OK' }, createMenu: () => ({ addItem() { return this; }, addSeparator() { return this; }, addToUi() {} }) }; }
    },
    Utilities: { formatDate: fmt },
    LockService: { getScriptLock: () => ({ tryLock: () => true, releaseLock: () => {} }) },
    ScriptApp: {
      getProjectTriggers: () => triggers.slice(),
      deleteTrigger: t => triggers.splice(triggers.indexOf(t), 1),
      newTrigger: h => ({ forSpreadsheet() { return this; }, onFormSubmit() { return this; }, create() { const t = { getHandlerFunction: () => h }; triggers.push(t); return t; } })
    },
    console, Date, Math, JSON, Intl
  };
  vm.createContext(ctx);
  vm.runInContext(fs.readFileSync(path.join(__dirname, '..', '参加表明集計.gs'), 'utf8'), ctx);
  return { ctx, active, external, alerts, triggers, Sheet };
}

// ---- 架空の回答データ（ヘッダーには前後の空白・改行を入れる） ----
const HEADER = [' タイムスタンプ', 'メールアドレス ', '\nお名前（呼ばれたい名前）※参加希望フォームと同じ名前', '　担当パート', '第1回演奏会への参加\n', '練習に参加できそうな頻度', '参加しやすい曜日・時間帯', '通いやすい練習場所のエリア', '練習1回あたりの参加費、いくらまでなら無理なく参加できますか', '運営のお手伝い', '伝えておきたいこと', '18歳未満ですか', '（上記の質問ではいの方）保護者の了承を得ていますか'];
const d = s => new Date(s);
const FORM = [HEADER,
  [d('2026-11-01T10:00:00+09:00'), 'a@example.com', 'あおい', 'フルート', '参加したい', 'ほぼ毎回', '土曜午後, 日曜午後', '横浜駅周辺, 川崎市', '1000円以下', '広報・SNS, 会計', 'よろしくお願いします', 'いいえ', ''],
  [d('2026-11-02T10:00:00+09:00'), 'B@Example.com', 'べに', 'ヴァイオリン（1st,2ndどちらも）', '日程次第で決める', '月2回程度', '土曜午後', '横浜駅周辺', '500円以下', '今は厳しい', 'なし', 'はい', 'はい'],
  [d('2026-11-03T10:00:00+09:00'), 'c@example.com', 'しろ', 'パーカッション', '今回は見送る', '日程による', '平日夜', 'その他', '2000円以下', '会場探し', '', 'はい', ''],
  [d('2026-11-04T10:00:00+09:00'), 'd@example.com', 'みどり', 'ﾁｭｰﾊﾞ', '参加したい', '月1回程度', '日曜午後', '川崎市', '5000円以下', '', '=HYPERLINK("http://example.com")', 'いいえ', ''],
  [d('2026-11-05T10:00:00+09:00'), 'b@example.com', 'べに', 'ヴァイオリン', '参加したい', 'ほぼ毎回', '土曜午後, 日曜午前', '横浜駅周辺', '1000円以下', '当日運営', '', 'はい', 'いいえ'],
  [d('2026-11-06T10:00:00+09:00'), 'e@example.com', 'くろ', 'オカリナ', '参加したい', 'ほぼ毎回', '土曜午後', '湘南・藤沢', '1000円以下', '', '', 'いいえ', ''],
  ['', '', '', '', '', '', '', '', '', '', '', '', '']
];

const APPLICANTS = [
  ['No.', '回答日時', '氏名', 'ニックネーム', '年代・学年', '地域', '楽器', '希望パート', '経験年数', 'オーケストラ経験', '現在の所属', '参加理由', '参加可能性', '第1回演奏会', 'やりたいこと', 'メールアドレス', '対応状況', '最終連絡日', '次の対応', '備考', '同期メモ', 'アプリID', 'アプリ用メールアドレス'],
  [1, '', '青井', 'あおい', '', '', 'Fl', '', '', '', '', '', '', '', '', 'a@example.com', '正式参加', '', '', '', '', '', ''],
  [2, '', '紅', 'べに', '', '', 'Vn', '', '', '', '', '', '', '', '', 'b@example.com', '正式参加', '', '', '', '', '', ''],
  [3, '', '黄田', 'きいろ', '', '', 'Ob', '', '', '', '', '', '', '', '', 'f@example.com', '初回連絡済み', '', '', '', '', '', ''],
  [4, '', '灰野', 'はい', '', '', 'Cl', '', '', '', '', '', '', '', '', 'g@example.com', '辞退', '', '', '', '', '', ''],
  [5, '', '茶山', 'ちゃ', '', '', 'Hr', '', '', '', '', '', '', '', '', 'h@example.com', '未対応', '', '', '', '', '', ''],
  [6, '', '桃井', 'しろ', '', '', 'Perc', '', '', '', '', '', '', '', '', 'other@example.com', '未対応', '', '', '', '', '', ''],
  [7, '', '紫', 'むらさき', '', '', 'Va', '', '', '', '', '', '', '', '', '', '未対応', '', '', '', '', '', ''],
  [8, '', '金', 'きん', '', '', 'Tp', '', '', '', '', '', '', '', '', 'x@example.com', '未対応', '', '', '', '', '', '']
];
const TARGETS = [
  ['楽器', '目標人数', '最低人数', '応募者数'],
  ['Fl', 4, 2, 1], ['Ob', 2, 1, 1], ['Cl', 5, 3, 1], ['Hr', 6, 4, 1], ['Tuba', 1, 1, 0], ['Perc', 4, 3, 1],
  ['1st Vn', 10, 7, 1], ['2nd Vn', 10, 7, 0], ['Va', 10, 5, 1], ['合計', 52, 33, 7], [], ['最終更新', 'x']
];

let passed = 0;
function test(name, fn) { fn(); passed++; console.log('✔ ' + name); }

const EXT_ID = '1AbCdEfGhIjKlMnOpQrStUvWxYz0123456789';
function setup(extra) {
  const e = makeEnv(Object.assign({
    external: { id: EXT_ID, sheets: [] }
  }, extra || {}));
  e.active.sheets.push(new e.Sheet('フォームの回答 1', FORM, true));
  e.external.sheets.push(new e.Sheet('応募者一覧', APPLICANTS, true), new e.Sheet('楽器別集計', TARGETS, true), new e.Sheet('募集設定', [['x']], true));
  return e;
}
function configure(e) {
  // 集計設定を作ってから URL を書き込む（運営の操作のかわり）
  e.ctx.updateParticipationSummary();
  const s = e.active.getSheetByName('集計設定');
  const row = s.data.findIndex(r => String(r[0]).indexOf('団員応募') === 0);
  s.data[row][1] = 'https://docs.google.com/spreadsheets/d/' + EXT_ID + '/edit#gid=0';
  const ex = e.active.getSheetByName('除外リスト');
  ex.data.push(['x@example.com', '募集停止でお断り']);
}
const flat = sheet => sheet.data.map(r => r.join('\t')).join('\n');

test('初回：設定シート・手入力・除外リストを作り、団員応募が未設定でも集計できる', () => {
  const e = setup();
  const r = e.ctx.updateParticipationSummary();
  assert.ok(r.ok, r.error);
  assert.strictEqual(r.total, 5); // b@ の重複を除く
  ['参加表明ダッシュボード', '参加表明一覧', '未回答者リスト', '運営お手伝い', '伝えておきたいこと', 'データチェック', '集計設定', '手入力回答', '除外リスト'].forEach(n => assert.ok(e.active.getSheetByName(n), n));
  assert.ok(flat(e.active.getSheetByName('未回答者リスト')).indexOf('未設定') >= 0);
  // 手入力回答のヘッダーはフォームと同じ
  assert.deepStrictEqual(e.active.getSheetByName('手入力回答').data[0], HEADER);
});

test('重複は新しい方を採用・パートを略号にそろえて木管→金管→打楽器→弦の順', () => {
  const e = setup(); configure(e);
  const r = e.ctx.updateParticipationSummary();
  assert.ok(r.ok);
  assert.deepStrictEqual([r.yes, r.maybe, r.no], [4, 0, 1]);
  const list = e.active.getSheetByName('参加表明一覧').data;
  const rows = list.slice(3);
  assert.deepStrictEqual(rows.map(x => x[2]), ['Fl', 'Tuba', 'Perc', 'Vn', '（判定できない）']);
  const beni = rows.find(x => x[3] === 'べに');
  assert.strictEqual(beni[4], '参加したい'); // 新しい方
  // 見送る＝灰色、18歳未満で了承「いいえ」＝赤
  const sheet = e.active.getSheetByName('参加表明一覧');
  const shiroRow = list.findIndex(x => x[3] === 'しろ') + 1;
  const beniRow = list.findIndex(x => x[3] === 'べに') + 1;
  assert.strictEqual(sheet.bgs[shiroRow + ':1'], '#f4cccc'); // しろ：18歳未満で了承空欄 → 赤（見送りより優先）
  assert.strictEqual(sheet.bgs[beniRow + ':1'], '#f4cccc');
});

test('数式に見える回答は文字として書く', () => {
  const e = setup(); configure(e);
  e.ctx.updateParticipationSummary();
  const msgs = flat(e.active.getSheetByName('伝えておきたいこと'));
  assert.ok(msgs.indexOf("'=HYPERLINK") >= 0);
  assert.ok(msgs.indexOf('なし') < 0); // 「なし」は記入なし扱い
  assert.ok(msgs.indexOf('よろしくお願いします') >= 0);
});

test('ダッシュボード：パート別の目標比較・曜日・参加費の累積', () => {
  const e = setup(); configure(e);
  e.ctx.updateParticipationSummary();
  const rows = e.active.getSheetByName('参加表明ダッシュボード').data;
  const find = label => rows.find(x => String(x[0]) === label);
  // Vn：目標 10+10、最低 7+7。参加したい 1人
  assert.deepStrictEqual(find('Vn（ヴァイオリン）').slice(1, 8), [1, 0, 0, 20, 14, 13, 19]);
  assert.deepStrictEqual(find('Fl（フルート）').slice(1, 8), [1, 0, 0, 4, 2, 1, 3]);
  // 曜日：土曜午後 = あおい・べに・くろ（見送るの しろ は除く）
  assert.deepStrictEqual(find('土曜午後').slice(1, 4), [3, 0, 3]);
  assert.deepStrictEqual(find('平日夜').slice(1, 4), [0, 0, 0]);
  // 参加費の累積（見送るを除く）：500円→4人、1000円→4人、5000円→1人
  assert.deepStrictEqual(find('500円').slice(1, 3), [4, 4]);
  assert.deepStrictEqual(find('1,000円').slice(1, 3), [4, 4]);
  assert.deepStrictEqual(find('2,000円').slice(1, 3), [1, 1]);
  assert.deepStrictEqual(find('5,000円').slice(1, 3), [1, 1]);
  assert.ok(find('締切'));
});

test('未回答者リスト：辞退・除外リスト・回答済みを除き、BCC 用の一覧を出す', () => {
  const e = setup(); configure(e);
  e.ctx.updateParticipationSummary();
  const sheet = e.active.getSheetByName('未回答者リスト');
  const text = flat(sheet);
  assert.ok(text.indexOf('黄田') >= 0 && text.indexOf('茶山') >= 0 && text.indexOf('紫') >= 0 && text.indexOf('桃井') >= 0);
  assert.ok(text.indexOf('灰野') < 0, '辞退は除く');
  assert.ok(text.indexOf('x@example.com') < 0, '除外リストは除く');
  assert.ok(text.indexOf('青井') < 0 && text.indexOf('紅') < 0, '回答済み（大文字小文字の違いも）');
  const bcc = sheet.data.find(r => String(r[0]).indexOf('@') > 0 && String(r[0]).indexOf(',') > 0);
  assert.strictEqual(bcc[0], 'f@example.com, h@example.com'); // 桃井は名前「しろ」が一致 → 確認のため宛先に入れない
  assert.ok(text.indexOf('同じ名前の回答があります') >= 0);
  assert.ok(text.indexOf('メールアドレスがありません') >= 0);
});

test('運営お手伝い・データチェック', () => {
  const e = setup(); configure(e);
  e.ctx.updateParticipationSummary();
  const help = e.active.getSheetByName('運営お手伝い').data;
  const header = help[3];
  assert.ok(header[0].indexOf('広報・SNS（1人）') === 0);
  assert.ok(help.some(r => r[1] === 'しろ（Perc）（見送り）'));
  assert.ok(!header.some(h => String(h).indexOf('今は厳しい') >= 0));
  const check = flat(e.active.getSheetByName('データチェック'));
  assert.ok(check.indexOf('b@example.com') >= 0 || check.indexOf('B@Example.com') >= 0);
  assert.ok(check.indexOf('オカリナ') >= 0);
});

test('手入力回答も集計に入り、フォームにない参加費の値も扱える', () => {
  const e = setup(); configure(e);
  const manual = e.active.getSheetByName('手入力回答');
  manual.data.push(['2026/11/10 12:00', '', 'DMさん', 'ホルン', '参加したい', '月2回程度', '日曜午後', '川崎市', '状況次第', '', 'DMで回答', 'いいえ', '']);
  const r = e.ctx.updateParticipationSummary();
  assert.strictEqual(r.total, 6);
  assert.strictEqual(r.manualCount, 1);
  const dash = e.active.getSheetByName('参加表明ダッシュボード').data;
  assert.ok(dash.some(x => x[0] === '状況次第' && x[2] === 1));
  assert.ok(dash.some(x => x[0] === 'Hr（ホルン）' && x[1] === 1));
});

test('回答シート・団員応募スプレッドシートには書き込まない（再実行しても同じ）', () => {
  const e = setup(); configure(e);
  const before = JSON.stringify(e.active.getSheetByName('フォームの回答 1').data);
  e.ctx.updateParticipationSummary();
  e.ctx.updateParticipationSummary();
  assert.strictEqual(JSON.stringify(e.active.getSheetByName('フォームの回答 1').data), before);
  // 読み取り専用にしてあるので、書き込もうとすればここまでに例外で止まる
  assert.throws(() => e.ctx.writeSheet_(e.active, '集計設定', new e.ctx.Table_(1), {}));
  assert.throws(() => e.ctx.writeSheet_(e.active, 'フォームの回答 1', new e.ctx.Table_(1), {}));
});

test('列が増えても（本名の列を追加）壊れない・本名は一覧に出る', () => {
  const e = makeEnv({ external: { id: EXT_ID, sheets: [] } });
  const h = HEADER.slice(0, 3).concat(['本名（運営のみ確認）']).concat(HEADER.slice(3));
  const rows = FORM.slice(1, 3).map(r => r.slice(0, 3).concat(['本名' + r[2]]).concat(r.slice(3)));
  e.active.sheets.push(new e.Sheet('フォームの回答 1', [h].concat(rows), true));
  const r = e.ctx.updateParticipationSummary();
  assert.ok(r.ok, r.error);
  const list = e.active.getSheetByName('参加表明一覧').data;
  assert.strictEqual(list[2][4], '本名');
  assert.ok(list.some(x => x[4] === '本名あおい'));
});

test('回答シートが見つからない・必須列が無いときは分かりやすく止まる', () => {
  const e = makeEnv({});
  const r = e.ctx.updateParticipationSummary();
  assert.ok(!r.ok && r.error.indexOf('フォームの回答 1') >= 0);
  const e2 = makeEnv({});
  e2.active.sheets.push(new e2.Sheet('フォームの回答 1', [['タイムスタンプ', 'メールアドレス']], true));
  const r2 = e2.ctx.updateParticipationSummary();
  assert.ok(!r2.ok && r2.error.indexOf('担当パート') >= 0);
});

test('トリガーの設定は1つだけ（何度押しても増えない）・解除できる・画面なしでも動く', () => {
  const e = setup({ noUi: true });
  e.ctx.setupParticipationTrigger();
  e.ctx.setupParticipationTrigger();
  assert.strictEqual(e.triggers.length, 1);
  e.ctx.onParticipationFormSubmit({});
  assert.ok(e.active.getSheetByName('参加表明ダッシュボード'));
  e.ctx.removeParticipationTrigger();
  assert.strictEqual(e.triggers.length, 0);
});

test('締切までの日数（日本時間の日付で数える）', () => {
  const e = setup();
  const RealDate = Date;
  e.ctx.Date = class extends RealDate { constructor(...a) { if (a.length) super(...a); else super('2026-12-05T23:30:00+09:00'); } };
  assert.strictEqual(e.ctx.daysLeft_('2026/12/06'), 1);
  e.ctx.Date = class extends RealDate { constructor(...a) { if (a.length) super(...a); else super('2026-12-06T00:10:00+09:00'); } };
  assert.strictEqual(e.ctx.daysLeft_('2026/12/06'), 0);
  assert.strictEqual(e.ctx.ymdOf_('２０２６年１２月６日'), '2026/12/06');
  assert.strictEqual(e.ctx.extractSpreadsheetId_('https://docs.google.com/spreadsheets/d/' + EXT_ID + '/edit'), EXT_ID);
});

console.log('\n' + passed + ' 件すべて成功');
