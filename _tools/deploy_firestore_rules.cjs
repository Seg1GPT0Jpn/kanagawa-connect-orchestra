/*
 * Firestore ルールを Firebase Rules API で直接公開する（GitHub Actions の公開で使用）
 *   node _tools/deploy_firestore_rules.cjs <project-id>
 *
 * `firebase deploy --only firestore:rules` は公開の前に「Firestore API が有効か」を
 * Service Usage API で確認するため、Firebase コンソールで作った鍵（firebase-adminsdk-…）では
 * 403 で止まることがある。ルールの公開そのもの（ルールセットの作成とリリースの更新）は
 * その鍵の権限でできるので、確認を飛ばして同じ API を直接呼ぶ。
 * 認証には GOOGLE_APPLICATION_CREDENTIALS（google-github-actions/auth が設定）を使う。
 */
const fs = require('fs');
const path = require('path');
const { GoogleAuth } = require(path.join(__dirname, 'firebase/node_modules/google-auth-library'));

const project = process.argv[2];
if (!project) {
  console.error('使い方: node _tools/deploy_firestore_rules.cjs <project-id>');
  process.exit(2);
}

const API = 'https://firebaserules.googleapis.com/v1';
const content = fs.readFileSync(path.join(__dirname, '..', 'firestore.rules'), 'utf8');

(async () => {
  const auth = new GoogleAuth({ scopes: ['https://www.googleapis.com/auth/cloud-platform'] });
  const client = await auth.getClient();

  // 1. ルールセットを作る（ここで文法チェックもされる）
  const created = await client.request({
    url: `${API}/projects/${project}/rulesets`,
    method: 'POST',
    data: { source: { files: [{ name: 'firestore.rules', content }] } },
  });
  const rulesetName = created.data.name;
  console.log('ルールセットを作成しました：' + rulesetName);

  // 2. Firestore（既定のデータベース）のリリースを、新しいルールセットに切り替える
  const releaseName = `projects/${project}/releases/cloud.firestore`;
  try {
    await client.request({
      url: `${API}/${releaseName}`,
      method: 'PATCH',
      data: { release: { name: releaseName, rulesetName } },
    });
  } catch (err) {
    if (!(err.response && err.response.status === 404)) throw err;
    await client.request({
      url: `${API}/projects/${project}/releases`,
      method: 'POST',
      data: { name: releaseName, rulesetName },
    });
  }
  console.log('Firestore ルールを公開しました');
})().catch((err) => {
  const detail = err.response ? JSON.stringify(err.response.data) : String(err);
  console.error('::error::Firestore ルールを公開できませんでした：' + detail);
  process.exit(1);
});
