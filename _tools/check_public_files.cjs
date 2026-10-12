/*
 * 公開されるファイルの確認（GitHub Actions の公開前チェックで実行）
 *   node _tools/check_public_files.cjs
 *
 * firebase deploy が実際に使うのと同じ関数（firebase-tools の listFiles）で公開されるファイルを列挙し、
 * サイト以外のもの（.git・.github などの隠しフォルダ、_tools・団員アプリ・練習アプリ・Apps Script のソース、
 * 設定・ルール・ログ・README）が含まれていたら失敗にする。
 */
const path = require('path');

const root = path.resolve(__dirname, '..');
const { listFiles } = require(path.join(__dirname, 'firebase/node_modules/firebase-tools/lib/listFiles.js'));
const cfg = require(path.join(root, 'firebase.json'));
const files = listFiles(path.join(root, cfg.hosting.public), cfg.hosting.ignore);

const bad = files.filter(f =>
  f.split('/').some(seg => seg.startsWith('.')) ||
  /^(_tools|kco-member-app|practice-app|orchestra-management|node_modules)\//.test(f) ||
  /(^|\/)(firebase\.json|firestore\.rules|README\.md)$|\.(gs|log)$/.test(f));

console.log('公開されるファイル：' + files.length + '件');

if (bad.length) {
  console.error('::error::公開してはいけないファイルが含まれています：' + bad.slice(0, 10).join(', ') + (bad.length > 10 ? ' ほか' : ''));
  process.exit(1);
}

console.log('公開してはいけないファイルは含まれていません');
