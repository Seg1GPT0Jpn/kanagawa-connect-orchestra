import { useState, type FormEvent } from 'react';
import { addDoc, collection, deleteDoc, doc, serverTimestamp, setDoc } from 'firebase/firestore';
import { useAuth } from '../auth/AuthProvider';
import { Empty, ErrorNote, Loading } from '../components/Layout';
import { getServices } from '../firebase';
import { useStaffDocs } from '../lib/data';
import { StaffDocView } from '../components/StaffDocView';
import { splitIcon, takeTitle } from '../lib/staffDoc';
import type { StaffDoc } from '../lib/types';

/*
 * 運営資料：運営メンバー（管理者・運営補助）だけが読める文書。
 * 読み書きの可否は Firestore ルール（staffDocs）が判定する。団員・参加希望者は読めない。
 */
export function AdminStaffDocs() {
  const { isStaff, isAdmin } = useAuth();
  const docs = useStaffDocs(isStaff);
  const [openId, setOpenId] = useState<string | null>(null);
  const [editing, setEditing] = useState<StaffDoc | 'new' | null>(null);

  if (docs.loading) return <Loading />;

  const sorted = [...docs.data].sort((a, b) => Number(b.pinned) - Number(a.pinned));
  const open = sorted.find(d => d.id === openId) ?? null;

  if (editing) {
    return (
      <StaffDocForm
        key={editing === 'new' ? 'new' : editing.id}
        original={editing === 'new' ? null : editing}
        canDelete={isAdmin}
        onDone={id => { setEditing(null); setOpenId(id); }}
      />
    );
  }

  if (open) {
    return (
      <div className="stack">
        <div className="row">
          <button className="btn btn--sm btn--outline" type="button" onClick={() => setOpenId(null)}>← 一覧へ</button>
          <span className="spacer" />
          <button className="btn btn--sm" type="button" onClick={() => setEditing(open)}>編集</button>
        </div>
        <StaffDocView title={open.title} body={open.body} />
      </div>
    );
  }

  return (
    <div className="stack">
      <div className="row">
        <h2 style={{ margin: 0 }}>運営資料</h2>
        <span className="spacer" />
        <button className="btn btn--sm" type="button" onClick={() => setEditing('new')}>＋ 資料を追加</button>
      </div>
      <p className="small muted">🔒 運営メンバー（管理者・運営補助）だけが見られます。団員・参加希望者には表示されません。</p>
      <ErrorNote message={docs.error} />

      {sorted.length === 0 ? (
        <Empty>資料はまだありません。「＋ 資料を追加」から文章を貼り付けてください。</Empty>
      ) : (
        <ul className="list">
          {sorted.map(d => {
            const { icon, text } = splitIcon(d.title);
            return (
              <li key={d.id}>
                <button type="button" className="list__item staffdoc-item" onClick={() => setOpenId(d.id)}>
                  <span className="staffdoc-item__icon" aria-hidden="true">{icon || '📄'}</span>
                  <span className="list__body">
                    <span className="list__title">{text}</span>
                    <span className="row small muted">
                      {d.pinned && <span className="badge badge--gold">固定</span>}
                      {d.updatedAt && <span>更新：{d.updatedAt.toDate().toLocaleDateString('ja-JP')}</span>}
                    </span>
                  </span>
                </button>
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}

function StaffDocForm({ original, canDelete, onDone }: { original: StaffDoc | null; canDelete: boolean; onDone: (openId: string | null) => void }) {
  const { user } = useAuth();
  const [title, setTitle] = useState(original?.title ?? '');
  const [body, setBody] = useState(original?.body ?? '');
  const [pinned, setPinned] = useState(original?.pinned ?? false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const preview = takeTitle(title, body);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    if (!user) return;
    const t = takeTitle(title, body);
    if (!t.title) {
      setError('タイトルを入力してください（空欄の場合は本文の1行目がタイトルになります）。');
      return;
    }
    setSaving(true);
    setError(null);
    const { db } = getServices();
    const data = {
      title: t.title.slice(0, 120),
      body: t.body.slice(0, 10000),
      pinned,
      updatedAt: serverTimestamp(),
      updatedBy: user.uid
    };
    try {
      let id = original?.id ?? null;
      if (original) await setDoc(doc(db, 'staffDocs', original.id), data, { merge: true });
      else id = (await addDoc(collection(db, 'staffDocs'), { ...data, createdAt: serverTimestamp() })).id;
      onDone(id);
    } catch {
      setError('保存できませんでした。入力内容を確認してください。');
    } finally {
      setSaving(false);
    }
  }

  async function onDelete() {
    if (!original || !window.confirm('この資料を削除しますか？（元に戻せません）')) return;
    try {
      await deleteDoc(doc(getServices().db, 'staffDocs', original.id));
      onDone(null);
    } catch {
      setError('削除できませんでした。');
    }
  }

  return (
    <div className="stack">
      <form className="card" onSubmit={onSubmit}>
        <h3 className="card__title">{original ? '資料を編集' : '資料を追加'}</h3>
        <div className="field">
          <label htmlFor="sd-title">タイトル</label>
          <input id="sd-title" type="text" maxLength={120} value={title} onChange={e => setTitle(e.target.value)} />
          <p className="field__hint">空欄のままにすると、本文の1行目がタイトルになります。</p>
        </div>
        <div className="field">
          <label htmlFor="sd-body">本文</label>
          <textarea id="sd-body" rows={14} maxLength={10000} value={body} onChange={e => setBody(e.target.value)} />
          <p className="field__hint">
            文章をそのまま貼り付けてください。「* 」「・」で始まる行は箇条書きに、箇条書きのすぐ上の短い行は見出しになります（先頭の絵文字はアイコンとして表示）。
          </p>
        </div>
        <label className="checkbox">
          <input type="checkbox" checked={pinned} onChange={e => setPinned(e.target.checked)} />
          一覧の一番上に固定する
        </label>
        <ErrorNote message={error} />
        <div className="row" style={{ marginTop: '0.75rem' }}>
          <button className="btn" type="submit" disabled={saving}>{saving ? '保存中…' : '保存'}</button>
          <button className="btn btn--outline" type="button" onClick={() => onDone(original?.id ?? null)}>キャンセル</button>
          <span className="spacer" />
          {original && canDelete && <button className="btn btn--sm btn--danger" type="button" onClick={onDelete}>削除</button>}
        </div>
      </form>

      {(preview.title || preview.body.trim()) && (
        <div>
          <p className="small muted">プレビュー（保存すると、このように表示されます）</p>
          <StaffDocView title={preview.title} body={preview.body} />
        </div>
      )}
    </div>
  );
}
