import { describe, expect, it } from 'vitest';
import { parseStaffDoc, splitIcon, takeTitle } from './staffDoc';

const SAMPLE = `私たちが目指しているのは、みんなでつくっていくオーケストラです。
📣 広報・渉外

* SNSやウェブサイトでの情報発信
* 団員募集や外部団体との連絡

💰 会計・協賛管理

* 予算や収支の記録

少しでも興味がある方は、運営までお気軽にご連絡ください！`;

describe('運営資料の本文', () => {
  it('見出し（絵文字つき）・箇条書き・段落に分ける', () => {
    expect(parseStaffDoc(SAMPLE)).toEqual([
      { kind: 'para', text: '私たちが目指しているのは、みんなでつくっていくオーケストラです。' },
      { kind: 'section', icon: '📣', heading: '広報・渉外', items: ['SNSやウェブサイトでの情報発信', '団員募集や外部団体との連絡'] },
      { kind: 'section', icon: '💰', heading: '会計・協賛管理', items: ['予算や収支の記録'] },
      { kind: 'para', text: '少しでも興味がある方は、運営までお気軽にご連絡ください！' }
    ]);
  });

  it('見出しのない箇条書き・いろいろな記号', () => {
    expect(parseStaffDoc('- あ\n・い\n1. う\n*\n本文')).toEqual([
      { kind: 'list', items: ['あ', 'い', 'う'] },
      { kind: 'para', text: '*' },
      { kind: 'para', text: '本文' }
    ]);
  });

  it('異体字セレクタつきの絵文字もアイコンにする', () => {
    expect(splitIcon('🏛️ 会場・演奏会運営')).toEqual({ icon: '🏛️', text: '会場・演奏会運営' });
    expect(splitIcon('総務')).toEqual({ icon: '', text: '総務' });
    expect(splitIcon('🎻')).toEqual({ icon: '', text: '🎻' });
  });

  it('タイトルが空なら1行目をタイトルにする', () => {
    expect(takeTitle('', '\n🎻 運営メンバー募集\n本文\n')).toEqual({ title: '🎻 運営メンバー募集', body: '本文\n' });
    expect(takeTitle(' 決まった題 ', '本文')).toEqual({ title: '決まった題', body: '本文' });
    expect(takeTitle('', '')).toEqual({ title: '', body: '' });
  });
});
