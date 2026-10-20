/*
 * 運営資料の本文（貼り付けたテキスト）を、見やすい形に組み立てる。
 *
 *  ・「* 」「- 」「・」などで始まる行 → 箇条書き
 *  ・すぐ下に箇条書きが続く短い行 → 見出し（先頭の絵文字はアイコンとして表示）
 *  ・それ以外の行 → 段落
 *
 * HTML としては解釈しない（React がテキストとして表示する）。
 */

export type StaffDocBlock =
  | { kind: 'section'; icon: string; heading: string; items: string[] }
  | { kind: 'list'; items: string[] }
  | { kind: 'para'; text: string };

const BULLET = /^\s*(?:[*\-・•●◦▪]|\d+[.)．）])\s*/;
const LEADING_EMOJI = /^((?:\p{Extended_Pictographic}|\p{Regional_Indicator})(?:️|‍\p{Extended_Pictographic}|\p{Emoji_Modifier})*)\s*/u;
const HEADING_MAX = 40;

function isBullet(line: string): boolean {
  return BULLET.test(line) && line.replace(BULLET, '').trim() !== '';
}

/** 先頭の絵文字と残りの文字に分ける */
export function splitIcon(text: string): { icon: string; text: string } {
  const m = text.match(LEADING_EMOJI);
  if (!m) return { icon: '', text };
  const rest = text.slice(m[0].length).trim();
  return rest ? { icon: m[1], text: rest } : { icon: '', text };
}

export function parseStaffDoc(body: string): StaffDocBlock[] {
  const lines = body.replace(/\r\n?/g, '\n').split('\n').map(l => l.trim());
  const blocks: StaffDocBlock[] = [];
  let current: { kind: 'section'; icon: string; heading: string; items: string[] } | { kind: 'list'; items: string[] } | null = null;

  const nextNonBlank = (i: number) => {
    for (let j = i + 1; j < lines.length; j++) if (lines[j] !== '') return lines[j];
    return '';
  };

  lines.forEach((line, i) => {
    if (line === '') return;
    if (isBullet(line)) {
      const item = line.replace(BULLET, '').trim();
      if (!current) {
        current = { kind: 'list', items: [] };
        blocks.push(current);
      }
      current.items.push(item);
      return;
    }
    if (line.length <= HEADING_MAX && isBullet(nextNonBlank(i))) {
      const { icon, text } = splitIcon(line);
      current = { kind: 'section', icon, heading: text, items: [] };
      blocks.push(current);
      return;
    }
    current = null;
    blocks.push({ kind: 'para', text: line });
  });

  return blocks;
}

/** タイトルが空のとき、本文の1行目をタイトルにする（1行目は本文から外す） */
export function takeTitle(title: string, body: string): { title: string; body: string } {
  const t = title.trim();
  if (t) return { title: t, body };
  const lines = body.replace(/\r\n?/g, '\n').split('\n');
  const idx = lines.findIndex(l => l.trim() !== '');
  if (idx < 0) return { title: '', body };
  const first = lines[idx].trim();
  if (first.length > 120) return { title: '', body };
  return { title: first, body: lines.slice(idx + 1).join('\n').replace(/^\n+/, '') };
}
