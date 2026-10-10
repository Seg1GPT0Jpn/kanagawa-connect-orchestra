import { useState } from 'react';
import { doc, serverTimestamp, updateDoc } from 'firebase/firestore';
import { useAuth } from '../auth/AuthProvider';
import { Empty, ErrorNote, Loading } from '../components/Layout';
import { getServices } from '../firebase';
import { useApplicants, useJoinRequests } from '../lib/data';
import type { JoinRequest, Member } from '../lib/types';

function formatDate(ts: { toDate(): Date } | null): string {
  if (!ts) return '';
  return new Intl.DateTimeFormat('ja-JP', { timeZone: 'Asia/Tokyo', month: 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit' }).format(ts.toDate());
}

/**
 * 正式加入の申請（管理者のみ）。
 * 承認すると、次の同期でスプレッドシートの対応状況が「正式参加」になり、本人のアプリが団員用に切り替わる。
 */
export function AdminJoinRequests() {
  const { isAdmin } = useAuth();
  const requests = useJoinRequests(isAdmin);
  const applicants = useApplicants(isAdmin);

  if (!isAdmin) return <p className="alert alert--error">正式加入の承認は管理者だけが行えます。</p>;
  if (requests.loading || applicants.loading) return <Loading />;

  const byId = new Map(applicants.data.map(a => [a.id, a]));
  const pending = requests.data.filter(r => r.status === 'pending');
  const decided = requests.data.filter(r => r.status !== 'pending').slice(0, 30);

  return (
    <div className="stack">
      <h2 style={{ margin: 0 }}>正式加入の申請</h2>
      <p className="small muted">
        参加希望者がアプリから申し込んだ正式加入です。「承認」すると、次の同期（自動同期なら15分以内）で
        スプレッドシートの対応状況が「正式参加」に変わり、本人のアプリが団員用に切り替わります。
      </p>
      <ErrorNote message={requests.error || applicants.error} />

      <section>
        <h3>承認待ち（{pending.length}件）</h3>
        {pending.length === 0 ? <Empty>承認待ちの申請はありません。</Empty> : (
          <ul className="stack" style={{ listStyle: 'none', padding: 0, margin: 0 }}>
            {pending.map(r => <li key={r.id}><RequestCard request={r} person={byId.get(r.id)} /></li>)}
          </ul>
        )}
      </section>

      {decided.length > 0 && (
        <section>
          <h3>これまでの申請</h3>
          <ul className="list">
            {decided.map(r => {
              const p = byId.get(r.id);
              return (
                <li key={r.id} className="list__item">
                  <div className="list__body">
                    <span className="row" style={{ gap: '0.35rem' }}>
                      {r.status === 'approved' ? <span className="badge badge--ok">承認</span> : <span className="badge badge--draft">見送り</span>}
                      {r.status === 'approved' && (r.applyError
                        ? <span className="badge badge--important">反映できませんでした</span>
                        : r.appliedAt ? <span className="badge">スプレッドシートに反映済み</span> : <span className="badge badge--gold">次の同期で反映</span>)}
                    </span>
                    <p className="list__title">{p?.displayName ?? '（団員に切り替わり済み・または停止中）'}</p>
                    {r.applyError && <p className="small">{r.applyError}</p>}
                    <p className="small muted">{formatDate(r.decidedAt)}</p>
                  </div>
                </li>
              );
            })}
          </ul>
        </section>
      )}
    </div>
  );
}

function RequestCard({ request: r, person }: { request: JoinRequest; person: Member | undefined }) {
  const { user } = useAuth();
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const name = person?.displayName ?? '（参加希望者）';

  async function decide(status: 'approved' | 'declined') {
    const text = status === 'approved'
      ? `${name} さんの正式加入を承認しますか？\n承認すると、団員一覧・楽譜なども見られるようになります。`
      : `${name} さんの申請を見送りにしますか？（本人は申し込み直せます）`;
    if (!window.confirm(text)) return;
    setBusy(true);
    setError(null);
    try {
      await updateDoc(doc(getServices().db, 'joinRequests', r.id), { status, decidedAt: serverTimestamp(), decidedBy: user?.uid });
    } catch {
      setError('更新できませんでした。');
    } finally {
      setBusy(false);
    }
  }

  return (
    <article className="card">
      <p className="list__title">{name}</p>
      <dl className="info">
        <div className="info__row"><dt>楽器</dt><dd>{person?.instrumentLabel || '未設定'}</dd></div>
        <div className="info__row"><dt>第1回演奏会</dt><dd>{r.concert || '（未回答）'}</dd></div>
        <div className="info__row"><dt>申し込み</dt><dd>{formatDate(r.createdAt)}</dd></div>
      </dl>
      {r.message && <p className="small pre" style={{ marginTop: '0.5rem' }}>{r.message}</p>}
      <div className="row" style={{ marginTop: '0.75rem' }}>
        <button type="button" className="btn btn--sm" onClick={() => decide('approved')} disabled={busy}>承認する</button>
        <button type="button" className="btn btn--sm btn--outline" onClick={() => decide('declined')} disabled={busy}>見送る</button>
      </div>
      {error && <p className="alert alert--error small" role="alert">{error}</p>}
    </article>
  );
}
