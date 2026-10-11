import { parseStaffDoc, splitIcon } from '../lib/staffDoc';

/** 本文を見出し・箇条書き・段落に分けて表示する（HTML としては解釈しない） */
export function StaffDocView({ title, body }: { title: string; body: string }) {
  const { icon, text } = splitIcon(title);
  const blocks = parseStaffDoc(body);
  return (
    <article className="staffdoc">
      <header className="staffdoc__header">
        {icon && <span className="staffdoc__icon" aria-hidden="true">{icon}</span>}
        <h2 className="staffdoc__title">{text || '（タイトルなし）'}</h2>
      </header>
      <div className="staffdoc__body">
        {blocks.map((b, i) => {
          if (b.kind === 'para') return <p key={i} className="staffdoc__para">{b.text}</p>;
          if (b.kind === 'list') {
            return <ul key={i} className="staffdoc__list">{b.items.map((t, j) => <li key={j}>{t}</li>)}</ul>;
          }
          return (
            <section key={i} className="staffdoc__section">
              <h3 className="staffdoc__heading">
                {b.icon && <span className="staffdoc__heading-icon" aria-hidden="true">{b.icon}</span>}
                {b.heading}
              </h3>
              {b.items.length > 0 && <ul className="staffdoc__list">{b.items.map((t, j) => <li key={j}>{t}</li>)}</ul>}
            </section>
          );
        })}
      </div>
    </article>
  );
}
