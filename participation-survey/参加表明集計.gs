/*******************************************************
 * かながわコネクトオーケストラ 参加表明フォーム 集計
 *
 * 「参加表明」スプレッドシートに追加して使います。
 * メニュー「参加表明」→「集計を更新」で、次のシートを自動で作り直します。
 *
 *   参加表明ダッシュボード / 参加表明一覧 / 未回答者リスト /
 *   運営お手伝い / 伝えておきたいこと / データチェック
 *
 * 運営が書き込むシート（自動では作り直しません。無ければ空の状態で作ります）
 *   集計設定     … 団員応募スプレッドシートの場所・締切日など
 *   手入力回答   … Instagram の DM など、フォーム以外でもらった回答
 *   除外リスト   … 未回答者リストから外したい人のメールアドレス
 *
 * 安全のための約束
 *   ・フォームの回答シートと、団員応募スプレッドシートには一切書き込みません（読むだけ）
 *   ・書き込むのは上の「自動生成シート」だけです（名前で確認してから書きます）
 *   ・外部への送信（メール・Web への送信など）は一切しません
 *******************************************************/

const PS_ = {
  // 自動生成シート（毎回まるごと作り直す）
  dashboard: '参加表明ダッシュボード',
  list: '参加表明一覧',
  unanswered: '未回答者リスト',
  helpers: '運営お手伝い',
  messages: '伝えておきたいこと',
  check: 'データチェック',

  // 運営が書き込むシート（作り直さない）
  settings: '集計設定',
  manual: '手入力回答',
  exclude: '除外リスト',

  // 団員応募スプレッドシートのシート名（読むだけ）
  applicantSheet: '応募者一覧',
  instrumentSheet: '楽器別集計',

  timeZone: 'Asia/Tokyo',
  title: 'かながわコネクトオーケストラ 参加表明ダッシュボード'
};

const PS_GENERATED_ = [PS_.dashboard, PS_.list, PS_.unanswered, PS_.helpers, PS_.messages, PS_.check];

// 集計設定シートの項目（初期値）
const PS_SETTINGS_ = [
  { key: 'applicantId', label: '団員応募スプレッドシート（URL または ID）', def: '', desc: '団員応募スプレッドシートの URL をそのまま貼り付けてください（読み取りだけに使います）' },
  { key: 'responseSheet', label: '回答シート名', def: 'フォームの回答 1', desc: 'Googleフォームの回答が入っているシートの名前' },
  { key: 'deadline', label: '締切日', def: '2026/12/06', desc: '残り日数の計算に使います' },
  { key: 'excludeStatuses', label: '未回答者リストから除く対応状況', def: '辞退', desc: 'カンマ区切りで複数書けます（例：辞退, 募集停止）' }
];

// 色
const PS_COLOR_ = {
  header: '#d9d9d9',
  section: '#c9daf8',
  plain: '#ffffff',
  good: '#d9ead3',
  warn: '#fff2cc',
  bad: '#f4cccc',
  skip: '#efefef',
  skipText: '#999999',
  best: '#b6d7a8'
};

// 回答シートの列（ヘッダー名の部分一致で探す。上から順に判定）
const PS_FIELDS_ = [
  { key: 'timestamp', label: 'タイムスタンプ', match: ['タイムスタンプ', 'timestamp'] },
  { key: 'email', label: 'メールアドレス', match: ['メールアドレス', 'emailaddress', 'メール'] },
  { key: 'realName', label: '本名', match: ['本名'] },
  { key: 'name', label: 'お名前', match: ['お名前', '呼ばれたい名前', '名前'] },
  { key: 'part', label: '担当パート', match: ['担当パート', 'パート', '楽器'] },
  { key: 'attend', label: '第1回演奏会への参加', match: ['演奏会への参加', '演奏会'] },
  { key: 'freq', label: '練習に参加できそうな頻度', match: ['頻度'] },
  { key: 'times', label: '参加しやすい曜日・時間帯', match: ['曜日', '時間帯'] },
  { key: 'areas', label: '通いやすい練習場所のエリア', match: ['エリア', '練習場所'] },
  { key: 'fee', label: '参加費', match: ['参加費'] },
  { key: 'help', label: '運営のお手伝い', match: ['お手伝い', '手伝い'] },
  { key: 'message', label: '伝えておきたいこと', match: ['伝えておきたい'] },
  { key: 'minor', label: '18歳未満ですか', match: ['18歳未満'] },
  { key: 'consent', label: '保護者の了承', match: ['保護者'] }
];

// これが無いと集計できない列
const PS_ESSENTIAL_ = ['email', 'name', 'part', 'attend'];

// 選択肢の並び順（ここに無い回答も、後ろに追加して数えます）
const PS_OPTIONS_ = {
  attend: ['参加したい', '日程次第で決める', '今回は見送る'],
  freq: ['ほぼ毎回', '月2回程度', '月1回程度', '日程による'],
  times: ['土曜午前', '土曜午後', '日曜午前', '日曜午後', '祝日', '平日夜'],
  areas: ['横浜駅周辺', '横浜市北部', '横浜市南部', '川崎市', '相模原・県央', '湘南・藤沢', 'その他'],
  help: ['広報・SNS', '会場探し', '楽譜の準備', '会計', '当日運営'],
  fee: [500, 1000, 2000, 5000]
};

const PS_HELP_NONE_ = ['今は厳しい'];

// 「伝えておきたいこと」で、何も書いていないのと同じ扱いにする回答
const PS_EMPTY_MESSAGES_ = ['なし', '特になし', 'とくになし', '特にありません', 'ありません', 'ないです', '無し', '-', 'ー', '－', '・', 'n/a', 'na', 'none'];

/*
 * 楽器の対応表（団員応募の応募者管理と同じ略号）
 * [略号, パート, 表記ゆれ]
 */
const PS_INSTRUMENTS_ = [
  ['Fl', 'Fl', ['フルート', 'Flute', 'Fl', 'フルート／ピッコロ', 'フルート・ピッコロ', 'Fl/Picc', 'Fl/Pic']],
  ['Picc', 'Fl', ['ピッコロ', 'Piccolo', 'Picc', 'Pic']],
  ['Ob', 'Ob', ['オーボエ', 'Oboe', 'Ob']],
  ['E.H.', 'Ob', ['イングリッシュホルン', 'コールアングレ', 'English Horn', 'Cor Anglais', 'E.H.']],
  ['Cl', 'Cl', ['クラリネット', 'Clarinet', 'Cl']],
  ['B.Cl', 'Cl', ['バスクラリネット', 'バスクラ', 'Bass Clarinet', 'B.Cl']],
  ['Fg', 'Fg', ['ファゴット', 'バスーン', 'Fagott', 'Fagotto', 'Bassoon', 'Fg', 'Bsn']],
  ['C.Fg', 'Fg', ['コントラファゴット', 'コントラバスーン', 'Contrabassoon', 'C.Fg']],
  ['Hr', 'Hr', ['ホルン', 'フレンチホルン', 'Horn', 'French Horn', 'Hr', 'Hn']],
  ['Tp', 'Tp', ['トランペット', 'Trumpet', 'Tp', 'Trp']],
  ['Tb', 'Tb', ['トロンボーン', 'Trombone', 'Tb', 'Trb', 'Tbn']],
  ['B.Tb', 'Tb', ['バストロンボーン', 'Bass Trombone', 'B.Tb']],
  ['Tuba', 'Tuba', ['テューバ', 'チューバ', 'Tuba', 'Tu']],
  ['Perc', 'Perc', ['打楽器', 'パーカッション', 'Percussion', 'Perc']],
  ['Timp', 'Perc', ['ティンパニ', 'ティンパニー', 'Timpani', 'Timp', 'Pk']],
  ['1st Vn', 'Vn', ['第1ヴァイオリン', '第一ヴァイオリン', '1stヴァイオリン', 'ファーストヴァイオリン', 'ヴァイオリン1st', '1st Violin', 'First Violin', 'Violin 1', '1st Vn', 'Vn1']],
  ['2nd Vn', 'Vn', ['第2ヴァイオリン', '第二ヴァイオリン', '2ndヴァイオリン', 'セカンドヴァイオリン', 'ヴァイオリン2nd', '2nd Violin', 'Second Violin', 'Violin 2', '2nd Vn', 'Vn2']],
  ['Vn', 'Vn', ['ヴァイオリン', 'バイオリン', 'Violin', 'Vn', 'Vl', 'Vln']],
  ['Va', 'Va', ['ヴィオラ', 'Viola', 'Va', 'Vla']],
  ['Vc', 'Vc', ['チェロ', 'Cello', 'Violoncello', 'Vc', 'Vlc']],
  ['Cb', 'Cb', ['コントラバス', '弦バス', 'ストリングベース', 'ダブルベース', 'Contrabass', 'Double Bass', 'String Bass', 'Cb']],
  ['Hp', 'Hp', ['ハープ', 'Harp', 'Hp']],
  ['Pf', 'Pf', ['ピアノ', '鍵盤', 'キーボード', 'チェレスタ', 'Piano', 'Keyboard', 'Celesta', 'Pf']]
];

// パートの並び順（木管 → 金管 → 打楽器 → 弦 → その他）
const PS_PART_ORDER_ = ['Fl', 'Ob', 'Cl', 'Fg', 'Hr', 'Tp', 'Tb', 'Tuba', 'Perc', 'Vn', 'Va', 'Vc', 'Cb', 'Hp', 'Pf'];

const PS_PART_LABELS_ = {
  Fl: 'フルート', Ob: 'オーボエ', Cl: 'クラリネット', Fg: 'ファゴット',
  Hr: 'ホルン', Tp: 'トランペット', Tb: 'トロンボーン', Tuba: 'テューバ',
  Perc: '打楽器', Vn: 'ヴァイオリン', Va: 'ヴィオラ', Vc: 'チェロ', Cb: 'コントラバス',
  Hp: 'ハープ', Pf: 'ピアノ・鍵盤'
};

const PS_UNKNOWN_PART_ = '（判定できない）';


/*******************************************************
 * メニュー
 *******************************************************/

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('参加表明')
    .addItem('集計を更新', 'updateParticipationSummary')
    .addSeparator()
    .addItem('フォーム送信時の自動更新を設定', 'setupParticipationTrigger')
    .addItem('フォーム送信時の自動更新を止める', 'removeParticipationTrigger')
    .addToUi();
}


/*******************************************************
 * 集計を更新（メニューから実行）
 *******************************************************/

function updateParticipationSummary() {
  const result = runParticipationUpdate_();
  const ui = getUiOrNull_();
  if (!ui) return result;

  const lines = [];
  if (result.ok) {
    lines.push('集計を更新しました。');
    lines.push('');
    lines.push('回答：' + result.total + '人（フォーム ' + result.formCount + '件・手入力 ' + result.manualCount + '件、重複を除く）');
    lines.push('参加したい ' + result.yes + '人／日程次第 ' + result.maybe + '人／見送る ' + result.no + '人');
    if (result.applicantStatus) lines.push('');
    if (result.applicantStatus) lines.push(result.applicantStatus);
    if (result.warnings.length) {
      lines.push('');
      lines.push('⚠ 確認してほしいこと（「データチェック」シートに詳しく出ています）');
      result.warnings.forEach(w => lines.push('・' + w));
    }
  } else {
    lines.push('集計できませんでした。');
    lines.push('');
    lines.push(result.error);
  }
  ui.alert('参加表明の集計', lines.join('\n'), ui.ButtonSet.OK);
  return result;
}


/*******************************************************
 * フォームが送信されたとき（インストール型トリガーから呼ばれる）
 *******************************************************/

function onParticipationFormSubmit(e) {
  runParticipationUpdate_();
}


/*******************************************************
 * トリガーの設定・解除（メニューから実行）
 *******************************************************/

function setupParticipationTrigger() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  removeTriggers_('onParticipationFormSubmit');
  ScriptApp.newTrigger('onParticipationFormSubmit')
    .forSpreadsheet(ss)
    .onFormSubmit()
    .create();
  const ui = getUiOrNull_();
  if (ui) {
    ui.alert('参加表明の集計',
      'フォームが送信されたときに、自動で集計を更新するように設定しました。\n\n' +
      '※ 設定した人のアカウントで動きます。止めたいときは「参加表明」→「フォーム送信時の自動更新を止める」を選んでください。',
      ui.ButtonSet.OK);
  }
}

function removeParticipationTrigger() {
  const count = removeTriggers_('onParticipationFormSubmit');
  const ui = getUiOrNull_();
  if (ui) {
    ui.alert('参加表明の集計',
      count ? '自動更新を止めました（' + count + '件のトリガーを削除）。' : '自動更新は設定されていませんでした。',
      ui.ButtonSet.OK);
  }
}

function removeTriggers_(handler) {
  let count = 0;
  ScriptApp.getProjectTriggers().forEach(t => {
    if (t.getHandlerFunction() === handler) {
      ScriptApp.deleteTrigger(t);
      count++;
    }
  });
  return count;
}


/*******************************************************
 * 集計の本体
 *******************************************************/

function runParticipationUpdate_() {
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(30 * 1000)) {
    return { ok: false, error: 'ほかの更新が実行中です。少し待ってからもう一度お試しください。', warnings: [] };
  }
  try {
    return updateAll_();
  } finally {
    lock.releaseLock();
  }
}

function updateAll_() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const stamp = Utilities.formatDate(new Date(), PS_.timeZone, 'yyyy/MM/dd HH:mm');

  // 運営が書き込むシート（無ければ作る。あれば触らない）
  const settings = readSettings_(ensureSettingsSheet_(ss), ss.getSpreadsheetTimeZone());
  const responseSheet = ss.getSheetByName(settings.responseSheet);
  if (!responseSheet) {
    return { ok: false, error: '回答シート「' + settings.responseSheet + '」が見つかりません。\n「集計設定」シートの「回答シート名」を、回答が入っているシートの名前に直してください。', warnings: [] };
  }
  ensureManualSheet_(ss, responseSheet);
  ensureExcludeSheet_(ss);

  const check = { duplicates: [], unknownParts: [], multiParts: [], minors: [], attendOther: [], noDate: [], missingColumns: [], applicant: [] };

  // ---- 回答を読む（フォーム＋手入力） ----
  const form = readResponses_(responseSheet, 'フォーム');
  if (form.missing.length) {
    return { ok: false, error: '回答シートに次の列が見つかりません：' + form.missing.join('、') + '\nフォームの質問名が変わっていないか確認してください。', warnings: [] };
  }
  const manual = readResponses_(ss.getSheetByName(PS_.manual), '手入力');
  if (manual.rows.length && manual.missing.length) {
    check.missingColumns.push('手入力回答：' + manual.missing.join('、') + ' の列が見つかりません');
  }
  ['realName', 'freq', 'times', 'areas', 'fee', 'help', 'message', 'minor', 'consent'].forEach(k => {
    if (form.columns[k] === undefined) check.missingColumns.push('回答シート：「' + fieldLabel_(k) + '」の列が見つかりません（この項目は集計しません）');
  });

  const all = form.rows.concat(manual.rows);
  all.forEach(r => { if (r.source === '手入力' && !r.timestamp) check.noDate.push(r); });

  const people = dedupe_(all, check.duplicates);

  people.forEach(p => {
    if (!p.partCodes.length && p.partRaw) check.unknownParts.push(p);
    if (!p.partRaw) check.unknownParts.push(p);
    if (p.partGroups.length > 1) check.multiParts.push(p);
    if (p.minorIssue) check.minors.push(p);
    if (p.attend === 'other') check.attendOther.push(p);
  });

  sortByPart_(people);

  // ---- 団員応募スプレッドシート（読むだけ） ----
  const applicant = readApplicantSpreadsheet_(settings, ss);
  if (applicant.error) check.applicant.push(applicant.error);

  const excluded = readExcludeList_(ss.getSheetByName(PS_.exclude));
  const unanswered = applicant.applicants ? findUnanswered_(applicant.applicants, people, excluded, settings.excludeStatuses) : null;

  // ---- 書き出し ----
  const ctx = { stamp, settings, people, check, applicant, unanswered, formCount: form.rows.length, manualCount: manual.rows.length, hasRealName: form.columns.realName !== undefined };

  writeDashboard_(ss, ctx);
  writeList_(ss, ctx);
  writeUnanswered_(ss, ctx);
  writeHelpers_(ss, ctx);
  writeMessages_(ss, ctx);
  writeCheck_(ss, ctx);

  const counts = countAttend_(people);
  const warnings = [];
  if (check.duplicates.length) warnings.push('同じメールアドレスの重複回答：' + check.duplicates.length + '件（新しい方を採用）');
  if (check.unknownParts.length) warnings.push('パートを判定できない回答：' + check.unknownParts.length + '件');
  if (check.minors.length) warnings.push('18歳未満で保護者の了承が確認できない人：' + check.minors.length + '人');
  if (check.attendOther.length) warnings.push('「第1回演奏会への参加」が想定外の回答：' + check.attendOther.length + '件');
  if (check.noDate.length) warnings.push('手入力回答で日時が空欄：' + check.noDate.length + '件');
  check.applicant.forEach(m => warnings.push(m));

  return {
    ok: true,
    total: people.length,
    formCount: form.rows.length,
    manualCount: manual.rows.length,
    yes: counts.yes,
    maybe: counts.maybe,
    no: counts.no,
    applicantStatus: unanswered ? '未回答の応募者：' + unanswered.list.length + '人' : '',
    warnings
  };
}


/*******************************************************
 * 集計設定
 *******************************************************/

function ensureSettingsSheet_(ss) {
  let sheet = ss.getSheetByName(PS_.settings);
  if (sheet) return sheet;
  sheet = ss.insertSheet(PS_.settings);
  const rows = [['集計設定（運営が書き込むシートです。自動では書き換えません）', '', ''], ['項目', '値', '説明']];
  PS_SETTINGS_.forEach(s => rows.push([s.label, s.def, s.desc]));
  sheet.getRange(1, 1, rows.length, 3).setValues(rows);
  sheet.getRange(1, 1).setFontWeight('bold').setFontSize(12);
  sheet.getRange(2, 1, 1, 3).setFontWeight('bold').setBackground(PS_COLOR_.header);
  sheet.getRange(3, 2, PS_SETTINGS_.length, 1).setBackground(PS_COLOR_.warn);
  sheet.setColumnWidth(1, 300);
  sheet.setColumnWidth(2, 360);
  sheet.setColumnWidth(3, 480);
  sheet.setFrozenRows(2);
  return sheet;
}

function readSettings_(sheet, tz) {
  const out = {};
  PS_SETTINGS_.forEach(s => { out[s.key] = s.def; });
  const values = sheet.getDataRange().getValues();
  values.forEach(row => {
    const label = normKey_(row[0]);
    if (!label) return;
    PS_SETTINGS_.forEach(s => {
      if (normKey_(s.label) === label) out[s.key] = row[1];
    });
  });
  out.applicantId = extractSpreadsheetId_(out.applicantId);
  out.responseSheet = str_(out.responseSheet) || 'フォームの回答 1';
  out.deadline = ymdOf_(out.deadline, tz) || '2026/12/06';
  out.excludeStatuses = splitList_(out.excludeStatuses);
  return out;
}

function extractSpreadsheetId_(value) {
  const s = str_(value);
  if (!s) return '';
  const m = s.match(/\/d\/([a-zA-Z0-9_-]{20,})/);
  if (m) return m[1];
  return /^[a-zA-Z0-9_-]{20,}$/.test(s) ? s : '';
}


/*******************************************************
 * 手入力回答・除外リスト（無ければ作る。あれば触らない）
 *******************************************************/

function ensureManualSheet_(ss, responseSheet) {
  if (ss.getSheetByName(PS_.manual)) return;
  const sheet = ss.insertSheet(PS_.manual);
  const lastCol = Math.max(responseSheet.getLastColumn(), 1);
  const header = responseSheet.getRange(1, 1, 1, lastCol).getValues()[0];
  sheet.getRange(1, 1, 1, header.length).setValues([header]);
  sheet.getRange(1, 1, 1, header.length).setFontWeight('bold').setBackground(PS_COLOR_.warn).setWrap(true);
  sheet.setFrozenRows(1);
  sheet.getRange(1, 1).setNote('Instagram の DM など、フォーム以外でもらった回答を2行目から書き込んでください。\n' +
    '・列はフォームの回答シートと同じです\n' +
    '・タイムスタンプ（日時）も書いてください（同じ人の回答が複数あるとき、新しい方を採用します）\n' +
    '・書いたあと「参加表明」→「集計を更新」で集計に入ります');
}

function ensureExcludeSheet_(ss) {
  if (ss.getSheetByName(PS_.exclude)) return;
  const sheet = ss.insertSheet(PS_.exclude);
  sheet.getRange(1, 1, 1, 2).setValues([['メールアドレス', 'メモ（任意。例：募集停止でお断り）']]);
  sheet.getRange(1, 1, 1, 2).setFontWeight('bold').setBackground(PS_COLOR_.warn);
  sheet.setColumnWidth(1, 300);
  sheet.setColumnWidth(2, 400);
  sheet.setFrozenRows(1);
}

function readExcludeList_(sheet) {
  const set = {};
  if (!sheet) return set;
  sheet.getDataRange().getValues().forEach(row => {
    row.forEach(cell => {
      const e = normEmail_(cell);
      if (e && e.indexOf('@') > 0) set[e] = true;
    });
  });
  return set;
}


/*******************************************************
 * 回答を読む
 *******************************************************/

function readResponses_(sheet, source) {
  const out = { rows: [], columns: {}, missing: [] };
  if (!sheet) return out;
  const values = sheet.getDataRange().getValues();
  if (!values.length) {
    out.missing = PS_ESSENTIAL_.map(fieldLabel_);
    return out;
  }
  out.columns = findColumns_(values[0]);
  out.missing = PS_ESSENTIAL_.filter(k => out.columns[k] === undefined).map(fieldLabel_);
  const c = out.columns;
  const get = (row, k) => (c[k] === undefined ? '' : row[c[k]]);

  for (let i = 1; i < values.length; i++) {
    const row = values[i];
    if (row.every(v => str_(v) === '')) continue;
    out.rows.push(makePerson_({
      source,
      rowNumber: i + 1,
      timestamp: toDate_(get(row, 'timestamp')),
      email: normEmail_(get(row, 'email')),
      emailRaw: str_(get(row, 'email')),
      realName: str_(get(row, 'realName')),
      name: str_(get(row, 'name')),
      partRaw: str_(get(row, 'part')),
      attendRaw: str_(get(row, 'attend')),
      freq: str_(get(row, 'freq')),
      times: splitList_(get(row, 'times')),
      areas: splitList_(get(row, 'areas')),
      fee: str_(get(row, 'fee')),
      help: splitList_(get(row, 'help')),
      message: str_(get(row, 'message')),
      minorRaw: str_(get(row, 'minor')),
      consentRaw: str_(get(row, 'consent'))
    }));
  }
  return out;
}

function findColumns_(header) {
  const keys = header.map(normKey_);
  const used = {};
  const columns = {};
  PS_FIELDS_.forEach(f => {
    for (let m = 0; m < f.match.length && columns[f.key] === undefined; m++) {
      const needle = normKey_(f.match[m]);
      for (let i = 0; i < keys.length; i++) {
        if (used[i] || !keys[i]) continue;
        if (keys[i].indexOf(needle) >= 0) {
          columns[f.key] = i;
          used[i] = true;
          break;
        }
      }
    }
  });
  return columns;
}

function fieldLabel_(key) {
  const f = PS_FIELDS_.find(x => x.key === key);
  return f ? f.label : key;
}

function makePerson_(p) {
  // 参加の意思
  const a = normKey_(p.attendRaw);
  if (a.indexOf(normKey_('参加したい')) >= 0) p.attend = 'yes';
  else if (a.indexOf(normKey_('日程次第')) >= 0) p.attend = 'maybe';
  else if (a.indexOf(normKey_('見送')) >= 0) p.attend = 'no';
  else p.attend = 'other';

  // パート
  const parsed = parsePart_(p.partRaw);
  p.partCodes = parsed.codes;
  p.partGroups = parsed.groups;
  p.partCode = parsed.codes.length ? parsed.codes.join(', ') : '';
  p.partGroup = parsed.groups.length ? parsed.groups[0] : PS_UNKNOWN_PART_;

  // 18歳未満・保護者の了承
  const minor = normKey_(p.minorRaw);
  const consent = normKey_(p.consentRaw);
  p.isMinor = minor.indexOf('はい') === 0 || minor === 'yes';
  p.consentOk = consent.indexOf('はい') === 0 || consent.indexOf('得てい') >= 0 || consent === 'yes';
  p.minorIssue = p.isMinor && !p.consentOk;

  p.help = p.help.filter(h => PS_HELP_NONE_.indexOf(h) < 0);
  p.hasMessage = !!p.message && PS_EMPTY_MESSAGES_.indexOf(normKey_(p.message)) < 0;
  p.displayName = p.name || p.realName || '（名前なし）';
  return p;
}


/*******************************************************
 * パートの判定
 *******************************************************/

let PS_ALIAS_MAP_ = null;

function aliasMap_() {
  if (PS_ALIAS_MAP_) return PS_ALIAS_MAP_;
  const map = {};
  PS_INSTRUMENTS_.forEach(item => {
    [item[0]].concat(item[2]).forEach(a => {
      const k = instrumentKey_(a);
      if (k && !map[k]) map[k] = item[0];
    });
  });
  PS_ALIAS_MAP_ = map;
  return map;
}

function codeToPart_(code) {
  const item = PS_INSTRUMENTS_.find(x => x[0] === code);
  return item ? item[1] : null;
}

function resolveInstrument_(text) {
  const map = aliasMap_();
  const k = instrumentKey_(text);
  if (k && map[k]) return map[k];
  // 括弧の中を除いて再判定（例：ヴァイオリン（1st,2ndどちらも）→ ヴァイオリン）
  const k2 = instrumentKey_(nfkc_(text).replace(/[(\[［【「『][^)\]］】」』]*[)\]］】」』]/g, ' '));
  if (k2 && map[k2]) return map[k2];
  return null;
}

function parsePart_(raw) {
  const codes = [];
  const add = c => { if (c && codes.indexOf(c) < 0) codes.push(c); };
  if (raw) {
    const whole = resolveInstrument_(raw);
    if (whole) {
      add(whole);
    } else {
      // 「フルート, ピッコロ」のような複数回答（括弧の中のカンマでは区切らない）
      const outside = nfkc_(raw).replace(/[(\[［【「『][^)\]］】」』]*[)\]］】」』]/g, ' ');
      outside.split(/[,、，;；\n\/／]+/).map(s => s.trim()).filter(Boolean).forEach(t => add(resolveInstrument_(t)));
    }
  }
  const groups = [];
  codes.forEach(c => { const g = codeToPart_(c); if (g && groups.indexOf(g) < 0) groups.push(g); });
  return { codes, groups };
}

function instrumentKey_(value) {
  let s = nfkc_(value).toLowerCase();
  s = s.replace(/ヴァ/g, 'バ').replace(/ヴィ/g, 'ビ').replace(/ヴェ/g, 'ベ').replace(/ヴォ/g, 'ボ').replace(/ヴ/g, 'ブ');
  const small = { 'ァ': 'ア', 'ィ': 'イ', 'ゥ': 'ウ', 'ェ': 'エ', 'ォ': 'オ', 'ッ': 'ツ', 'ャ': 'ヤ', 'ュ': 'ユ', 'ョ': 'ヨ', 'ヮ': 'ワ' };
  s = s.replace(/[ァィゥェォッャュョヮ]/g, c => small[c]);
  return s.replace(/[\s　ー〜~\-‐‑‒–—―−・･.。\/()\[\]{}「」【】『』'"’‘“”]/g, '');
}

function sortByPart_(people) {
  const rank = g => { const i = PS_PART_ORDER_.indexOf(g); return i < 0 ? 999 : i; };
  const codeRank = c => { const i = PS_INSTRUMENTS_.findIndex(x => x[0] === c); return i < 0 ? 999 : i; };
  people.sort((a, b) =>
    rank(a.partGroup) - rank(b.partGroup) ||
    codeRank(a.partCodes[0]) - codeRank(b.partCodes[0]) ||
    (a.timestamp ? a.timestamp.getTime() : 0) - (b.timestamp ? b.timestamp.getTime() : 0));
}


/*******************************************************
 * 重複（同じメールアドレス）→ 新しい方を採用
 *******************************************************/

function dedupe_(rows, duplicates) {
  const byKey = {};
  const order = [];
  rows.forEach(r => {
    const key = r.email ? 'mail:' + r.email : (r.name ? 'name:' + normKey_(r.name) : 'row:' + r.source + r.rowNumber);
    if (!byKey[key]) {
      byKey[key] = [];
      order.push(key);
    }
    byKey[key].push(r);
  });
  const time = r => (r.timestamp ? r.timestamp.getTime() : 0);
  return order.map(key => {
    const list = byKey[key].slice().sort((a, b) => time(b) - time(a));
    if (list.length > 1) duplicates.push({ key, adopted: list[0], dropped: list.slice(1) });
    return list[0];
  });
}

function countAttend_(people) {
  const c = { yes: 0, maybe: 0, no: 0, other: 0 };
  people.forEach(p => { c[p.attend]++; });
  return c;
}


/*******************************************************
 * 団員応募スプレッドシート（読むだけ）
 *******************************************************/

function readApplicantSpreadsheet_(settings, activeSs) {
  const out = { applicants: null, targets: null, error: '' };
  if (!settings.applicantId) {
    out.error = '団員応募スプレッドシートが未設定です（「集計設定」に URL を貼り付けると、未回答者リストと目標人数の比較が表示されます）';
    return out;
  }
  if (settings.applicantId === activeSs.getId()) {
    out.error = '「集計設定」の団員応募スプレッドシートに、この参加表明スプレッドシートが指定されています。団員応募スプレッドシートの URL に直してください';
    return out;
  }
  let ext;
  try {
    ext = SpreadsheetApp.openById(settings.applicantId);
  } catch (e) {
    out.error = '団員応募スプレッドシートを開けませんでした（URL が正しいか、このアカウントに閲覧権限があるか確認してください）';
    return out;
  }

  const appSheet = ext.getSheetByName(PS_.applicantSheet);
  if (appSheet) out.applicants = readApplicants_(appSheet.getDataRange().getValues());
  else out.error = '団員応募スプレッドシートに「' + PS_.applicantSheet + '」シートがありません';

  const instSheet = ext.getSheetByName(PS_.instrumentSheet);
  if (instSheet) out.targets = readTargets_(instSheet.getDataRange().getValues());
  else out.error = (out.error ? out.error + '／' : '') + '団員応募スプレッドシートに「' + PS_.instrumentSheet + '」シートがありません';

  if (out.applicants && out.applicants.error) {
    out.error = out.applicants.error;
    out.applicants = null;
  }
  return out;
}

function findHeaderRow_(values, must) {
  for (let r = 0; r < Math.min(values.length, 10); r++) {
    const keys = values[r].map(normKey_);
    if (must.every(m => keys.indexOf(normKey_(m)) >= 0)) return r;
  }
  return -1;
}

function colIndex_(headerKeys, names) {
  for (let n = 0; n < names.length; n++) {
    const i = headerKeys.indexOf(normKey_(names[n]));
    if (i >= 0) return i;
  }
  return -1;
}

function readApplicants_(values) {
  const h = findHeaderRow_(values, ['メールアドレス']);
  if (h < 0) return { error: '「応募者一覧」に「メールアドレス」の列が見つかりません' };
  const keys = values[h].map(normKey_);
  const col = {
    no: colIndex_(keys, ['No.', 'No']),
    name: colIndex_(keys, ['氏名', 'お名前・呼ばれたい名前', 'お名前', '名前']),
    nickname: colIndex_(keys, ['ニックネーム']),
    instrument: colIndex_(keys, ['楽器']),
    status: colIndex_(keys, ['対応状況', 'ステータス']),
    email: colIndex_(keys, ['メールアドレス']),
    appEmail: colIndex_(keys, ['アプリ用メールアドレス'])
  };
  const get = (row, k) => (col[k] < 0 ? '' : row[col[k]]);
  const list = [];
  for (let r = h + 1; r < values.length; r++) {
    const row = values[r];
    const email = normEmail_(get(row, 'email'));
    const name = str_(get(row, 'name'));
    if (!email && !name) continue;
    list.push({
      no: str_(get(row, 'no')),
      name,
      nickname: str_(get(row, 'nickname')),
      instrument: str_(get(row, 'instrument')),
      status: str_(get(row, 'status')),
      email,
      appEmail: normEmail_(get(row, 'appEmail'))
    });
  }
  return list;
}

function readTargets_(values) {
  const h = findHeaderRow_(values, ['楽器', '目標人数']);
  if (h < 0) return null;
  const keys = values[h].map(normKey_);
  const cCode = colIndex_(keys, ['楽器']);
  const cTarget = colIndex_(keys, ['目標人数']);
  const cMin = colIndex_(keys, ['最低人数']);
  const out = {};
  for (let r = h + 1; r < values.length; r++) {
    const code = str_(values[r][cCode]);
    if (!code || code === '合計') break;
    const part = codeToPart_(code) || codeToPart_(resolveInstrument_(code) || '');
    if (!part) continue;
    if (!out[part]) out[part] = { target: null, min: null };
    const t = toNumber_(values[r][cTarget]);
    const m = cMin < 0 ? null : toNumber_(values[r][cMin]);
    if (t !== null) out[part].target = (out[part].target || 0) + t;
    if (m !== null) out[part].min = (out[part].min || 0) + m;
  }
  return out;
}

function findUnanswered_(applicants, people, excluded, excludeStatuses) {
  const answeredEmails = {};
  const answeredNames = {};
  people.forEach(p => {
    if (p.email) answeredEmails[p.email] = true;
    [p.name, p.realName].forEach(n => { if (n) answeredNames[normKey_(n)] = true; });
  });
  const seen = {};
  const list = [];
  let excludedCount = 0;
  applicants.forEach(a => {
    const dupKey = a.email || 'name:' + normKey_(a.name);
    if (seen[dupKey]) return;
    seen[dupKey] = true;
    if (excludeStatuses.some(s => s && a.status.indexOf(s) >= 0)) { excludedCount++; return; }
    if ((a.email && excluded[a.email]) || (a.appEmail && excluded[a.appEmail])) { excludedCount++; return; }
    if ((a.email && answeredEmails[a.email]) || (a.appEmail && answeredEmails[a.appEmail])) return;
    const nameHit = [a.name, a.nickname].some(n => n && answeredNames[normKey_(n)]);
    let note = '';
    if (nameHit) note = '同じ名前の回答があります（メールアドレスが違う・手入力など）。確認してください';
    else if (!a.email) note = 'メールアドレスがありません';
    list.push({ a, note, remind: !!a.email && !nameHit });
  });
  return { list, excludedCount };
}


/*******************************************************
 * 書き出し：参加表明ダッシュボード
 *******************************************************/

function writeDashboard_(ss, ctx) {
  const W = 8;
  const t = new Table_(W);
  const people = ctx.people;
  const counts = countAttend_(people);
  const active = people.filter(p => p.attend !== 'no');

  t.row([PS_.title], { bold: true, size: 14 });
  t.row(['最終更新', ctx.stamp, '※ 自動生成シートです。直接編集しないでください（「参加表明」→「集計を更新」で作り直されます）']);
  t.blank();

  // ---- 概要 ----
  t.section('【概要】');
  t.header(['項目', '人数・値', 'メモ']);
  t.row(['回答数（重複を除く）', people.length, 'フォーム ' + ctx.formCount + '件・手入力 ' + ctx.manualCount + '件（重複 ' + ctx.check.duplicates.length + '件は新しい方を採用）']);
  t.row(['参加したい', counts.yes, ''], { bg: PS_COLOR_.good });
  t.row(['日程次第で決める', counts.maybe, ''], { bg: PS_COLOR_.warn });
  t.row(['今回は見送る', counts.no, ''], { bg: PS_COLOR_.skip });
  if (counts.other) t.row(['その他の回答', counts.other, '「データチェック」で確認してください'], { bg: PS_COLOR_.bad });
  const days = daysLeft_(ctx.settings.deadline);
  t.row(['締切', ctx.settings.deadline, days < 0 ? '締切を過ぎました' : (days === 0 ? '今日が締切です' : 'あと ' + days + ' 日')],
    { bg: days < 0 ? PS_COLOR_.skip : (days <= 7 ? PS_COLOR_.bad : PS_COLOR_.plain) });
  if (ctx.unanswered) {
    t.row(['未回答の応募者', ctx.unanswered.list.length, '「未回答者リスト」シート（辞退・除外リストの ' + ctx.unanswered.excludedCount + '人は除く）']);
  } else {
    t.row(['未回答の応募者', '—', ctx.applicant.error || ''], { bg: PS_COLOR_.warn });
  }
  if (ctx.check.minors.length) {
    t.row(['18歳未満で保護者の了承が未確認', ctx.check.minors.length, '「参加表明一覧」で赤色の人'], { bg: PS_COLOR_.bad });
  }
  t.blank();

  // ---- パート別 ----
  t.section('【パート別】（目標人数・最低人数は団員応募シートの「楽器別集計」から）');
  t.header(['パート', '参加したい', '日程次第', '見送る', '目標人数', '最低人数', '最低まであと', '目標まであと']);
  const targets = ctx.applicant.targets || {};
  const groups = PS_PART_ORDER_.filter(g => targets[g] || people.some(p => p.partGroup === g));
  if (people.some(p => p.partGroup === PS_UNKNOWN_PART_)) groups.push(PS_UNKNOWN_PART_);
  const sum = { yes: 0, maybe: 0, no: 0, target: 0, min: 0, needMin: 0, needTarget: 0 };
  groups.forEach(g => {
    const inPart = people.filter(p => p.partGroup === g);
    const c = countAttend_(inPart);
    const tg = targets[g] || { target: null, min: null };
    const needMin = tg.min === null ? '' : Math.max(0, tg.min - c.yes);
    const needTarget = tg.target === null ? '' : Math.max(0, tg.target - c.yes);
    let bg = PS_COLOR_.plain;
    if (tg.min !== null || tg.target !== null) {
      if (tg.target !== null && c.yes >= tg.target) bg = PS_COLOR_.good;
      else if (tg.min !== null && c.yes >= tg.min) bg = PS_COLOR_.warn;
      else bg = PS_COLOR_.bad;
    }
    const label = g === PS_UNKNOWN_PART_ ? g : g + '（' + PS_PART_LABELS_[g] + '）';
    t.row([label, c.yes, c.maybe, c.no, blank_(tg.target), blank_(tg.min), needMin, needTarget], { bg });
    sum.yes += c.yes; sum.maybe += c.maybe; sum.no += c.no;
    sum.target += tg.target || 0; sum.min += tg.min || 0;
    sum.needMin += needMin || 0; sum.needTarget += needTarget || 0;
  });
  t.row(['合計', sum.yes, sum.maybe, sum.no, sum.target || '', sum.min || '', sum.needMin, sum.needTarget], { bg: PS_COLOR_.header, bold: true });
  t.note('※ 色：緑＝目標達成／黄＝最低人数は達成／赤＝最低人数に届いていない（「参加したい」の人数で判定）');
  if (!ctx.applicant.targets) t.note('※ 団員応募シートを読めないため、目標人数・最低人数は空欄です');
  t.blank();

  // ---- 曜日・時間帯 ----
  multiChoiceSection_(t, '【参加しやすい曜日・時間帯】（どこに練習を入れると集まるか）', '曜日・時間帯', active, 'times', PS_OPTIONS_.times);
  t.blank();

  // ---- エリア ----
  multiChoiceSection_(t, '【通いやすい練習場所のエリア】', 'エリア', active, 'areas', PS_OPTIONS_.areas);
  t.blank();

  // ---- 参加費 ----
  t.section('【参加費】この金額なら参加できる人数（その金額以上まで払えると答えた人の累積）');
  t.header(['1回の参加費', '参加したい人', '日程次第も含めると', '', 'グラフ（日程次第も含む）']);
  const fees = {};
  PS_OPTIONS_.fee.forEach(x => { fees[x] = true; });
  const otherFees = {};
  active.forEach(p => {
    const n = feeAmount_(p.fee);
    if (n !== null) fees[n] = true;
    else if (p.fee) otherFees[p.fee] = (otherFees[p.fee] || 0) + 1;
  });
  const amounts = Object.keys(fees).map(Number).sort((a, b) => a - b);
  const feeRows = amounts.map(x => {
    const ok = active.filter(p => { const n = feeAmount_(p.fee); return n !== null && n >= x; });
    return { x, yes: ok.filter(p => p.attend === 'yes').length, all: ok.length };
  });
  const maxFee = Math.max(1, ...feeRows.map(r => r.all));
  feeRows.forEach(r => t.row([r.x.toLocaleString('ja-JP') + '円', r.yes, r.all, '', bar_(r.all, maxFee)]));
  Object.keys(otherFees).forEach(k => t.row([k, '', otherFees[k], '', '（金額以外の回答。上の人数には含みません）'], { bg: PS_COLOR_.warn }));
  if (!feeRows.length && !Object.keys(otherFees).length) t.row(['（回答なし）']);
  t.note('※ 例：「1,000円」の行は、1,000円以下・2,000円以下・5,000円以下と答えた人の合計です。「今回は見送る」の人は数えません');
  t.blank();

  // ---- 頻度 ----
  multiChoiceSection_(t, '【練習に参加できそうな頻度】', '頻度', active, 'freq', PS_OPTIONS_.freq);
  t.note('※ 曜日・エリア・頻度は「今回は見送る」の人を除いて数えています');

  writeSheet_(ss, PS_.dashboard, t, { widths: [240, 110, 110, 90, 90, 90, 110, 110], frozen: 2 });
}

function multiChoiceSection_(t, title, label, people, key, order) {
  t.section(title);
  t.header([label, '参加したい', '日程次第', '合計', 'グラフ']);
  const counts = {};
  const options = order.slice();
  people.forEach(p => {
    const values = Array.isArray(p[key]) ? p[key] : (p[key] ? [p[key]] : []);
    values.forEach(v => {
      if (!counts[v]) counts[v] = { yes: 0, maybe: 0, all: 0 };
      if (options.indexOf(v) < 0) options.push(v);
      counts[v].all++;
      if (p.attend === 'yes') counts[v].yes++;
      if (p.attend === 'maybe') counts[v].maybe++;
    });
  });
  const max = Math.max(1, ...options.map(o => (counts[o] ? counts[o].all : 0)));
  const best = Math.max(0, ...options.map(o => (counts[o] ? counts[o].all : 0)));
  options.forEach(o => {
    const c = counts[o] || { yes: 0, maybe: 0, all: 0 };
    t.row([o, c.yes, c.maybe, c.all, bar_(c.all, max)], { bg: best > 0 && c.all === best ? PS_COLOR_.best : PS_COLOR_.plain });
  });
}

function bar_(n, max) {
  if (!n) return '';
  const len = Math.max(1, Math.round((n / max) * 20));
  return '■'.repeat(len) + ' ' + n;
}

function feeAmount_(value) {
  const s = nfkc_(value).replace(/[,，]/g, '');
  const m = s.match(/(\d+)\s*円/);
  if (m) return Number(m[1]);
  return null;
}

// 締切日（yyyy/MM/dd）まであと何日か（日本時間の今日から数える。当日は 0）
function daysLeft_(deadlineYmd) {
  const utc = ymd => { const a = ymd.split('/').map(Number); return Date.UTC(a[0], a[1] - 1, a[2]); };
  const today = Utilities.formatDate(new Date(), PS_.timeZone, 'yyyy/MM/dd');
  return Math.round((utc(deadlineYmd) - utc(today)) / 86400000);
}

// 日付（セルの日付 or 「2026/12/06」などの文字）を yyyy/MM/dd にそろえる
function ymdOf_(v, tz) {
  if (v instanceof Date && !isNaN(v.getTime())) return Utilities.formatDate(v, tz || PS_.timeZone, 'yyyy/MM/dd');
  const m = nfkc_(str_(v)).match(/^(\d{4})[\/\-.年](\d{1,2})[\/\-.月](\d{1,2})日?$/);
  if (!m) return '';
  const pad = n => ('0' + n).slice(-2);
  return m[1] + '/' + pad(m[2]) + '/' + pad(m[3]);
}


/*******************************************************
 * 書き出し：参加表明一覧
 *******************************************************/

function writeList_(ss, ctx) {
  const header = ['No.', 'パート', 'パート（略号）', 'お名前'];
  if (ctx.hasRealName) header.push('本名');
  header.push('第1回演奏会への参加', '練習の頻度', '曜日・時間帯', 'エリア', '参加費', '運営のお手伝い', '18歳未満', '保護者の了承', '伝えておきたいこと', 'メールアドレス', '回答日時', '回答方法', '担当パート（回答そのまま）');
  const W = header.length;
  const t = new Table_(W);
  t.row(['参加表明一覧']);
  t.row(['最終更新', ctx.stamp, '※ 自動生成シートです。直接編集しないでください。灰色＝今回は見送る／赤＝18歳未満で保護者の了承が未確認']);
  t.header(header);
  ctx.people.forEach((p, i) => {
    const line = [i + 1, p.partGroup === PS_UNKNOWN_PART_ ? p.partGroup : PS_PART_LABELS_[p.partGroup] || p.partGroup, p.partCode || PS_UNKNOWN_PART_, p.displayName];
    if (ctx.hasRealName) line.push(p.realName);
    line.push(p.attendRaw, p.freq, p.times.join(', '), p.areas.join(', '), p.fee, p.help.join(', '), p.minorRaw, p.consentRaw, p.hasMessage ? p.message : '', p.emailRaw, p.timestamp || '', p.source, p.partRaw);
    let opt = {};
    if (p.minorIssue) opt = { bg: PS_COLOR_.bad };
    else if (p.attend === 'no') opt = { bg: PS_COLOR_.skip, color: PS_COLOR_.skipText };
    t.row(line, opt);
  });
  if (!ctx.people.length) t.row(['（まだ回答がありません）']);
  const widths = header.map(h => (h === '伝えておきたいこと' ? 280 : (h === 'No.' ? 50 : 130)));
  writeSheet_(ss, PS_.list, t, { widths, frozen: 3, frozenCols: 4, dateCol: header.indexOf('回答日時') + 1, headerRow: 3, filter: ctx.people.length > 0 });
}


/*******************************************************
 * 書き出し：未回答者リスト
 *******************************************************/

function writeUnanswered_(ss, ctx) {
  const W = 7;
  const t = new Table_(W);
  t.row(['未回答者リスト（団員応募の「応募者一覧」にいて、まだ参加表明していない人）'], { bold: true });
  t.row(['最終更新', ctx.stamp, '※ 自動生成シートです。直接編集しないでください。除きたい人は「除外リスト」シートにメールアドレスを書いてください']);
  if (!ctx.unanswered) {
    t.blank();
    t.row([ctx.applicant.error || '団員応募スプレッドシートを読めませんでした'], { bg: PS_COLOR_.warn });
    writeSheet_(ss, PS_.unanswered, t, { widths: [500, 150, 150, 120, 120, 260, 360], frozen: 2 });
    return;
  }
  const list = ctx.unanswered.list;
  const remind = list.filter(x => x.remind).map(x => x.a.email);
  t.row(['未回答の人数', list.length, '（対応状況が「' + ctx.settings.excludeStatuses.join('・') + '」の人と、除外リストの人 ' + ctx.unanswered.excludedCount + '人は除いています）']);
  t.blank();
  t.section('【リマインドメールの宛先】下のセルをコピーして、Gmail の BCC にそのまま貼り付けてください（' + remind.length + '人）');
  t.row([remind.join(', ')], { wrap: true, bg: PS_COLOR_.warn });
  t.note('※ 「同じ名前の回答があります」の人は、すでに回答している可能性があるので宛先に入れていません');
  t.blank();
  t.header(['No.', '氏名', 'ニックネーム', '楽器', '対応状況', 'メールアドレス', '備考']);
  list.forEach(x => {
    t.row([x.a.no, x.a.name, x.a.nickname, x.a.instrument, x.a.status, x.a.email, x.note], { bg: x.note ? PS_COLOR_.warn : PS_COLOR_.plain });
  });
  if (!list.length) t.row(['（未回答の人はいません）']);
  writeSheet_(ss, PS_.unanswered, t, { widths: [500, 150, 150, 120, 120, 260, 360], frozen: 2 });
}


/*******************************************************
 * 書き出し：運営お手伝い
 *******************************************************/

function writeHelpers_(ss, ctx) {
  const roles = PS_OPTIONS_.help.slice();
  ctx.people.forEach(p => p.help.forEach(h => { if (roles.indexOf(h) < 0) roles.push(h); }));
  const W = Math.max(roles.length, 3);
  const t = new Table_(W);
  t.row(['運営お手伝い（手伝えると答えた人）'], { bold: true });
  t.row(['最終更新', ctx.stamp, '※ 自動生成シートです。直接編集しないでください。（見送り）＝第1回演奏会は見送ると答えた人']);
  t.blank();
  const lists = roles.map(r => ctx.people.filter(p => p.help.indexOf(r) >= 0)
    .map(p => p.displayName + '（' + (p.partCode || '?') + '）' + (p.attend === 'no' ? '（見送り）' : '')));
  t.header(roles.map((r, i) => r + '（' + lists[i].length + '人）'));
  const depth = Math.max(0, ...lists.map(l => l.length));
  for (let i = 0; i < depth; i++) t.row(lists.map(l => l[i] || ''));
  if (!depth) t.row(['（まだいません）']);
  writeSheet_(ss, PS_.helpers, t, { widths: new Array(W).fill(200), frozen: 4 });
}


/*******************************************************
 * 書き出し：伝えておきたいこと
 *******************************************************/

function writeMessages_(ss, ctx) {
  const W = 5;
  const t = new Table_(W);
  t.row(['伝えておきたいこと（記入があった人だけ）'], { bold: true });
  t.row(['最終更新', ctx.stamp, '※ 自動生成シートです。直接編集しないでください']);
  t.header(['回答日時', 'お名前', 'パート', '第1回演奏会への参加', '伝えておきたいこと']);
  const list = ctx.people.filter(p => p.hasMessage).sort((a, b) => (b.timestamp ? b.timestamp.getTime() : 0) - (a.timestamp ? a.timestamp.getTime() : 0));
  list.forEach(p => t.row([p.timestamp || '', p.displayName, p.partCode || PS_UNKNOWN_PART_, p.attendRaw, p.message], { wrap: true }));
  if (!list.length) t.row(['（記入はまだありません）']);
  writeSheet_(ss, PS_.messages, t, { widths: [130, 150, 90, 150, 520], frozen: 3, dateCol: 1 });
}


/*******************************************************
 * 書き出し：データチェック
 *******************************************************/

function writeCheck_(ss, ctx) {
  const W = 6;
  const t = new Table_(W);
  const c = ctx.check;
  const fmt = d => (d ? Utilities.formatDate(d, PS_.timeZone, 'yyyy/MM/dd HH:mm') : '（日時なし）');
  t.row(['データチェック'], { bold: true });
  t.row(['最終更新', ctx.stamp, '※ 自動生成シートです。直接編集しないでください。直すときは回答そのもの（手入力回答など）を直して、集計を更新してください']);
  t.blank();

  t.section('【同じメールアドレスの重複回答】新しい方を採用しています（' + c.duplicates.length + '件）');
  t.header(['メールアドレス・名前', '採用した回答', '採用しなかった回答', '回答方法', '', '']);
  c.duplicates.forEach(d => d.dropped.forEach(x =>
    t.row([d.adopted.emailRaw || d.adopted.displayName, fmt(d.adopted.timestamp) + '（' + d.adopted.attendRaw + '）', fmt(x.timestamp) + '（' + x.attendRaw + '）', d.adopted.source + ' ← ' + x.source, '', ''])));
  if (!c.duplicates.length) t.row(['（ありません）']);
  t.blank();

  t.section('【パートを判定できなかった回答】（' + c.unknownParts.length + '件）');
  t.header(['お名前', '担当パート（回答そのまま）', '回答方法', '行', '', '']);
  c.unknownParts.forEach(p => t.row([p.displayName, p.partRaw || '（空欄）', p.source, p.rowNumber, '', ''], { bg: PS_COLOR_.warn }));
  if (!c.unknownParts.length) t.row(['（ありません）']);
  t.blank();

  if (c.multiParts.length) {
    t.section('【複数のパートが書かれている回答】最初のパートで集計しています（' + c.multiParts.length + '件）');
    t.header(['お名前', '担当パート（回答そのまま）', '判定したパート', '', '', '']);
    c.multiParts.forEach(p => t.row([p.displayName, p.partRaw, p.partCode, '', '', '']));
    t.blank();
  }

  t.section('【18歳未満で、保護者の了承が「はい」になっていない人】（' + c.minors.length + '人）');
  t.header(['お名前', 'パート', '18歳未満', '保護者の了承', 'メールアドレス', '']);
  c.minors.forEach(p => t.row([p.displayName, p.partCode || PS_UNKNOWN_PART_, p.minorRaw, p.consentRaw || '（空欄）', p.emailRaw, ''], { bg: PS_COLOR_.bad }));
  if (!c.minors.length) t.row(['（ありません）']);
  t.blank();

  if (c.attendOther.length) {
    t.section('【「第1回演奏会への参加」が想定外の回答】参加・日程次第・見送るのどれにも数えていません（' + c.attendOther.length + '件）');
    t.header(['お名前', '回答', '回答方法', '行', '', '']);
    c.attendOther.forEach(p => t.row([p.displayName, p.attendRaw || '（空欄）', p.source, p.rowNumber, '', ''], { bg: PS_COLOR_.warn }));
    t.blank();
  }

  if (c.noDate.length) {
    t.section('【手入力回答で日時が空欄】重複したときに古い回答として扱われます（' + c.noDate.length + '件）');
    t.header(['お名前', '行', '', '', '', '']);
    c.noDate.forEach(p => t.row([p.displayName, p.rowNumber, '', '', '', '']));
    t.blank();
  }

  if (c.missingColumns.length || c.applicant.length) {
    t.section('【設定・列の確認】');
    c.missingColumns.concat(c.applicant).forEach(m => t.row([m], { bg: PS_COLOR_.warn }));
  }

  writeSheet_(ss, PS_.check, t, { widths: [260, 220, 220, 150, 220, 80], frozen: 2 });
}


/*******************************************************
 * 表を組み立てて書き込む
 *******************************************************/

function Table_(width) {
  this.width = width;
  this.values = [];
  this.bgs = [];
  this.colors = [];
  this.bold = [];
  this.wrap = [];
  this.sizes = [];
}

Table_.prototype.row = function (cells, opt) {
  const o = opt || {};
  const line = cells.slice(0, this.width).map(safeCell_);
  while (line.length < this.width) line.push('');
  this.values.push(line);
  this.bgs.push(new Array(this.width).fill(o.bg || PS_COLOR_.plain));
  this.colors.push(new Array(this.width).fill(o.color || '#000000'));
  this.bold.push(!!o.bold);
  this.wrap.push(!!o.wrap);
  this.sizes.push(o.size || null);
};
Table_.prototype.blank = function () { this.row([]); };
Table_.prototype.section = function (title) { this.row([title], { bg: PS_COLOR_.section, bold: true }); };
Table_.prototype.header = function (cells) { this.row(cells, { bg: PS_COLOR_.header, bold: true }); };
Table_.prototype.note = function (text) { this.row([text], { color: '#666666' }); };

/*
 * 自動生成シートだけに書き込む（回答シート・運営が書くシートには絶対に書かない）
 */
function writeSheet_(ss, name, table, opt) {
  if (PS_GENERATED_.indexOf(name) < 0) throw new Error('自動生成シート以外には書き込みません：' + name);
  let sheet = ss.getSheetByName(name);
  if (!sheet) sheet = ss.insertSheet(name);

  const rows = Math.max(table.values.length, 1);
  const W = table.width;
  if (sheet.getMaxRows() < rows) sheet.insertRowsAfter(sheet.getMaxRows(), rows - sheet.getMaxRows());
  if (sheet.getMaxColumns() < W) sheet.insertColumnsAfter(sheet.getMaxColumns(), W - sheet.getMaxColumns());

  const oldFilter = sheet.getFilter();
  if (oldFilter) oldFilter.remove();
  sheet.clear();
  if (!table.values.length) return;

  const range = sheet.getRange(1, 1, rows, W);
  range.setValues(table.values);
  range.setBackgrounds(table.bgs);
  range.setFontColors(table.colors);
  range.setVerticalAlignment('top');
  table.bold.forEach((b, i) => { if (b) sheet.getRange(i + 1, 1, 1, W).setFontWeight('bold'); });
  table.wrap.forEach((w, i) => { if (w) sheet.getRange(i + 1, 1, 1, W).setWrap(true); });
  table.sizes.forEach((s, i) => { if (s) sheet.getRange(i + 1, 1).setFontSize(s); });

  if (opt.dateCol && opt.dateCol > 0) sheet.getRange(1, opt.dateCol, rows, 1).setNumberFormat('yyyy/mm/dd hh:mm');
  if (opt.widths) opt.widths.forEach((w, i) => { if (i < W) sheet.setColumnWidth(i + 1, w); });
  sheet.setFrozenRows(opt.frozen || 0);
  sheet.setFrozenColumns(opt.frozenCols || 0);
  if (opt.filter && opt.headerRow && rows > opt.headerRow) sheet.getRange(opt.headerRow, 1, rows - opt.headerRow + 1, W).createFilter();
}


/*******************************************************
 * 小さな関数
 *******************************************************/

function getUiOrNull_() {
  try {
    return SpreadsheetApp.getUi();
  } catch (e) {
    return null; // トリガーから動いているときは画面が無い
  }
}

function str_(v) {
  if (v === null || v === undefined) return '';
  return String(v).trim();
}

function nfkc_(v) {
  const s = v === null || v === undefined ? '' : String(v);
  return typeof s.normalize === 'function' ? s.normalize('NFKC') : s;
}

// ヘッダー・選択肢の照合用（全角/半角・空白・改行・記号の違いを無視）
function normKey_(v) {
  return nfkc_(str_(v)).toLowerCase().replace(/[\s　]+/g, '').replace(/[?？*＊:：]+$/, '');
}

function normEmail_(v) {
  return nfkc_(str_(v)).replace(/\s+/g, '').toLowerCase();
}

function splitList_(v) {
  if (Array.isArray(v)) return v.map(str_).filter(Boolean);
  return str_(v).split(/\s*[,、，]\s*/).map(s => s.trim()).filter(Boolean);
}

function toDate_(v) {
  if (v instanceof Date && !isNaN(v.getTime())) return v;
  const s = nfkc_(str_(v));
  if (!s) return null;
  const m = s.match(/^(\d{4})[\/\-.年](\d{1,2})[\/\-.月](\d{1,2})日?(?:\s+(\d{1,2}):(\d{2})(?::(\d{2}))?)?$/);
  if (!m) return null;
  return new Date(Number(m[1]), Number(m[2]) - 1, Number(m[3]), Number(m[4] || 0), Number(m[5] || 0), Number(m[6] || 0));
}

function toNumber_(v) {
  if (typeof v === 'number') return v;
  const s = nfkc_(str_(v));
  if (!s || !/^\d+(\.\d+)?$/.test(s)) return null;
  return Number(s);
}

function blank_(v) {
  return v === null || v === undefined ? '' : v;
}

// 「=」「+」「-」「@」で始まる文字は、数式として動かないように文字として書き込む
function safeCell_(v) {
  if (typeof v === 'string' && /^[=+\-@]/.test(v)) return "'" + v;
  return v;
}
