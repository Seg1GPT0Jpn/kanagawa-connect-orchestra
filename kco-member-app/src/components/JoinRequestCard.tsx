import { useState, type FormEvent } from 'react';
import { deleteDoc, doc, serverTimestamp, setDoc } from 'firebase/firestore';
import { useAuth } from '../auth/AuthProvider';
import { getServices } from '../firebase';
import { useAppConfig, useMyJoinRequest } from '../lib/data';

const CONCERT_CHOICES = ['ぜひ参加したい', '検討中', '参加しない'];

/**
 * 参加希望者のホーム：アプリから正式加入を申し込む。
 * 運営（管理者）が承認すると、スプレッドシートの同期で団員に切り替わる。
 */
export function JoinRequestCard() {
  const { access, canWrite } = useAuth();
  const memberId = access?.memberId ?? null;
  const request = useMyJoinRequest(memberId);
  const config = useAppConfig();
  const [open, setOpen] = useState(false);
  const [concert, setConcert] = useState('');
  const [message, setMessage] = useState('');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const ref = () => doc(getServices().db, 'joinRequests', memberId!);

  async function submit(e: FormEvent) {
    e.preventDefault();
    if (!memberId) return;
    setBusy(true);
    setError(null);
    try {
      // 見送りになった申請があれば消してから申し込み直す
      if (request.data?.status === 'declined') await deleteDoc(ref());
      await setDoc(ref(), { status: 'pending', message: message.slice(0, 500), concert, createdAt: serverTimestamp() });
      setOpen(false);
    } catch {
      setError('申し込めませんでした。時間をおいて再度お試しください。');
    } finally {
      setBusy(false);
    }
  }

  async function cancel() {
    if (!window.confirm('正式加入の申し込みを取り消しますか？')) return;
    setBusy(true);
    setError(null);
    try {
      await deleteDoc(ref());
    } catch {
      setError('取り消せませんでした。');
    } finally {
      setBusy(false);
    }
  }

  const r = request.data;

  return (
    <section className="card card--important" aria-labelledby="applicant-title">
      <h2 className="card__title" id="applicant-title">参加希望者として登録されています</h2>
      <p className="small">
        練習予定・演奏会・お知らせを見たり、練習の出欠（見学・体験）を登録したりできます。
        正式に加入すると、団員一覧・楽譜・アンケートなども使えるようになります。
      </p>

      {request.loading ? null : r?.status === 'pending' ? (
        <div className="join-request join-request--pending" role="status">
          <p><strong>正式加入を申し込みました。</strong>運営の承認をお待ちください。</p>
          <p className="small muted">承認されると、自動で団員用の画面に切り替わります。</p>
          <button type="button" className="btn btn--sm btn--outline" onClick={cancel} disabled={busy || !canWrite}>申し込みを取り消す</button>
        </div>
      ) : r?.status === 'approved' ? (
        <div className="join-request join-request--approved" role="status">
          <p><strong>🎉 正式加入が承認されました！</strong></p>
          <p className="small">まもなく団員用の画面に切り替わります（最長15分ほどかかります）。</p>
        </div>
      ) : open ? (
        <form className="stack join-request" onSubmit={submit}>
          <fieldset className="field">
            <legend>第1回演奏会への参加について</legend>
            <div className="choice-list">
              {CONCERT_CHOICES.map(c => (
                <label key={c} className="checkbox"><input type="radio" name="concert" checked={concert === c} onChange={() => setConcert(c)} />{c}</label>
              ))}
            </div>
          </fieldset>
          <div className="field">
            <label htmlFor="join-message">運営へのひとこと（任意・500文字まで）</label>
            <textarea id="join-message" maxLength={500} value={message} onChange={e => setMessage(e.target.value)} />
          </div>
          <div className="row">
            <button className="btn btn--gold" type="submit" disabled={busy}>正式加入を申し込む</button>
            <button className="btn btn--sm btn--outline" type="button" onClick={() => setOpen(false)}>やめる</button>
          </div>
        </form>
      ) : (
        <div className="join-request">
          {r?.status === 'declined' && (
            <p className="small">前回の申し込みは今回は見送りとなりました。ご不明な点は運営までお問い合わせください。</p>
          )}
          <button type="button" className="btn btn--gold" onClick={() => setOpen(true)} disabled={!canWrite || !memberId}>
            {r?.status === 'declined' ? 'もう一度申し込む' : '正式加入を申し込む'}
          </button>
          {config.data?.joinFormUrl && (
            <p className="small muted" style={{ marginTop: '0.5rem' }}>
              メールでご案内した <a href={config.data.joinFormUrl} target="_blank" rel="noopener noreferrer">正式加入確認フォーム</a> から回答することもできます。
            </p>
          )}
        </div>
      )}
      {error && <p className="alert alert--error small" role="alert">{error}</p>}
    </section>
  );
}
