"""作問バンク共通ヘルパー。

問題は短い関数呼び出しで記述し、generate_batch.py がスキーマ準拠の JSON に展開する。

  mc(stem, [正答, 誤答1, 誤答2, ...], 解説)       選択式（正答を先頭に書く。出力時に決定的にシャッフル）
  ms(stem, [正答...], [誤答...], 解説)            複数選択
  tf(stem, True/False, 解説)                      正誤
  num(stem, 答, 解説, chk=("式", "期待値"))       数値・式の答え（chk は検算）
  sa(stem, 答, 解説, v=[別解...])                 短答記述
  fill(stem, 答, 解説)                            空所補充
  order(stem, [正しい順の語句...], 解説)          並べ替え
  desc(stem, 模範解答, 解説, rubric=[(観点, 点)]) 記述・説明（proof / essay は kind= で指定）

共通キーワード
  d=難易度スコア(1-5)  k=[技能]  p=配点  st=資料ID  sec=大問ID  no=表示番号  tp=トピック
  fig=figure(...)  tbl=table(...)  lines=解答行数  grid=字数マス  h=解答欄高さmm
  asp="k"|"t"（評価観点）  keep=True（選択肢の順序を固定）  u=単元ID（セットと異なる場合）
"""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

COPYRIGHT_HOLDER = "かながわコネクト教材プロジェクト"
LICENSE = "教育目的での複製可・再配布不可（著作権者の許諾が必要）"


def _curriculum():
    m = json.loads((ROOT / "schemas" / "curriculum_map.json").read_text(encoding="utf-8"))
    units = {}
    for st in m["stages"]:
        for s in st["subjects"]:
            for u in s["units"]:
                units[u["unit_id"]] = dict(u, stage=st["id"])
    for t in m["exam_tracks"]:
        for u in t["units"]:
            units[u["unit_id"]] = dict(u, stage="high_school" if u["unit_id"][:2] in ("CT", "SS") else "junior_high")
    return units


UNITS = _curriculum()


def _q(t, stem, **kw):
    kw["t"] = t
    kw["s"] = stem
    return kw


def mc(stem, choices, e, d=2, **kw):
    return _q("mc", stem, c=list(choices), e=e, d=d, **kw)


def ms(stem, correct, wrong, e, d=3, **kw):
    return _q("ms", stem, c=list(correct) + list(wrong), n_correct=len(correct), e=e, d=d, **kw)


def tf(stem, is_true, e, d=1, **kw):
    return _q("tf", stem, truth=bool(is_true), e=e, d=d, **kw)


def num(stem, a, e, d=2, **kw):
    return _q("num", stem, a=a, e=e, d=d, **kw)


def sa(stem, a, e, d=2, **kw):
    return _q("sa", stem, a=a, e=e, d=d, **kw)


def fill(stem, a, e, d=2, **kw):
    return _q("fill", stem, a=a, e=e, d=d, **kw)


def order(stem, parts, e, d=3, **kw):
    return _q("ord", stem, c=list(parts), e=e, d=d, **kw)


def desc(stem, a, e, rubric, d=4, kind="desc", **kw):
    return _q(kind, stem, a=a, e=e, r=list(rubric), d=d, **kw)


def table(rows, header=None, caption=None):
    t = {"rows": [list(r) for r in rows]}
    if header:
        t["header"] = list(header)
    if caption:
        t["caption"] = caption
    return t


def figure(alt, svg=None, caption=None, height_mm=None):
    f = {"alt": alt}
    if svg:
        f["svg"] = svg
    if caption:
        f["caption"] = caption
    if height_mm:
        f["height_mm"] = height_mm
    return f


def stim(id, content, type="passage", title=None, source=None, glossary=None, cp=None, tbl=None, fig=None):
    s = {"id": id, "type": type, "content": content}
    if title:
        s["title"] = title
    if source:
        s["source"] = source
    if glossary:
        s["glossary"] = [{"term": a, "meaning": b} for a, b in glossary]
    if cp:
        s["copyright_status"] = cp
    if tbl:
        s["table"] = tbl
    if fig:
        s["figure"] = fig
    return s


def unit_set(unit_id, items, *, track, out, suffix="S1", title=None, subtitle=None, points=None, **extra):
    """単元プリント1枚分のセット定義を作る。"""
    u = UNITS[unit_id]
    spec = {
        "set_id": f"{unit_id}-{suffix}",
        "track": track,
        "title": title or f"{u['title']}",
        "subtitle": subtitle or f"{u['domain']}｜{'・'.join(u['topics'][:4])}",
        "stage": u["stage"],
        "subject": u["subject"],
        "grade": u["grade"],
        "unit_ids": [unit_id],
        "default_skills": u["default_skills"],
        "out": out,
        "items": items,
    }
    if "course" in u:
        spec["course"] = u["course"]
    if points:
        spec["default_points"] = points
    spec.update(extra)
    return spec


# --------------------------------------------------------------------------
# 図（SVG）ヘルパー
# --------------------------------------------------------------------------

def _fmt(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def plane(xr=(-5, 5), yr=(-5, 5), unit=18, lines=(), curves=(), points=(), segments=(), grid=True,
          ticks=True, polygons=(), labels=(), xl="x", yl="y"):
    """座標平面。lines=[(傾き, 切片, ラベル)], curves=[(関数, ラベル)], points=[(x, y, ラベル)],
    segments=[((x1,y1),(x2,y2))], polygons=[[(x,y),...]] (薄く塗る), labels=[(x, y, 文字)]。"""
    x0, x1 = xr
    y0, y1 = yr
    pad = 14
    W = (x1 - x0) * unit + 2 * pad
    H = (y1 - y0) * unit + 2 * pad
    X = lambda x: pad + (x - x0) * unit  # noqa: E731
    Y = lambda y: pad + (y1 - y) * unit  # noqa: E731
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {_fmt(W)} {_fmt(H)}" width="{_fmt(W)}" height="{_fmt(H)}" font-family="serif" font-size="11">']
    if grid:
        for gx in range(math.ceil(x0), math.floor(x1) + 1):
            out.append(f'<line x1="{_fmt(X(gx))}" y1="{_fmt(Y(y0))}" x2="{_fmt(X(gx))}" y2="{_fmt(Y(y1))}" stroke="#ddd" stroke-width="0.6"/>')
        for gy in range(math.ceil(y0), math.floor(y1) + 1):
            out.append(f'<line x1="{_fmt(X(x0))}" y1="{_fmt(Y(gy))}" x2="{_fmt(X(x1))}" y2="{_fmt(Y(gy))}" stroke="#ddd" stroke-width="0.6"/>')
    for poly in polygons:
        pts = " ".join(f"{_fmt(X(x))},{_fmt(Y(y))}" for x, y in poly)
        out.append(f'<polygon points="{pts}" fill="#cfdcec" fill-opacity="0.6" stroke="#333" stroke-width="1"/>')
    # 軸
    if True:  # 軸（原点が範囲外でも描く）
        out.append(f'<line x1="{_fmt(X(x0))}" y1="{_fmt(Y(0))}" x2="{_fmt(X(x1) + 6)}" y2="{_fmt(Y(0))}" stroke="#000" stroke-width="1" marker-end="url(#ar)"/>')
        out.append(f'<line x1="{_fmt(X(0))}" y1="{_fmt(Y(y0))}" x2="{_fmt(X(0))}" y2="{_fmt(Y(y1) - 6)}" stroke="#000" stroke-width="1" marker-end="url(#ar)"/>')
    out.insert(1, '<defs><marker id="ar" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#000"/></marker></defs>')
    out.append(f'<text x="{_fmt(X(x1) + 2)}" y="{_fmt(Y(0) + 13)}" font-style="italic">{xl}</text>')
    out.append(f'<text x="{_fmt(X(0) + 5)}" y="{_fmt(Y(y1) - 2)}" font-style="italic">{yl}</text>')
    out.append(f'<text x="{_fmt(X(0) - 11)}" y="{_fmt(Y(0) + 12)}">O</text>')
    if ticks:
        for gx in range(math.ceil(x0), math.floor(x1) + 1):
            if gx and gx % (1 if x1 - x0 <= 12 else 2) == 0:
                out.append(f'<text x="{_fmt(X(gx) - 3)}" y="{_fmt(Y(0) + 12)}" font-size="8" fill="#555">{gx}</text>')
        for gy in range(math.ceil(y0), math.floor(y1) + 1):
            if gy and gy % (1 if y1 - y0 <= 12 else 2) == 0:
                out.append(f'<text x="{_fmt(X(0) - 13)}" y="{_fmt(Y(gy) + 3)}" font-size="8" fill="#555">{gy}</text>')
    for m, b, lab in lines:
        pts = []
        for x in (x0, x1):
            pts.append((x, m * x + b))
        # クリップ
        (ax, ay), (bx, by) = pts
        out.append(f'<clipPath id="c{len(out)}"><rect x="{_fmt(X(x0))}" y="{_fmt(Y(y1))}" width="{_fmt((x1 - x0) * unit)}" height="{_fmt((y1 - y0) * unit)}"/></clipPath>')
        cid = f"c{len(out) - 1}"
        out.append(f'<line x1="{_fmt(X(ax))}" y1="{_fmt(Y(ay))}" x2="{_fmt(X(bx))}" y2="{_fmt(Y(by))}" stroke="#1f4e79" stroke-width="1.5" clip-path="url(#{cid})"/>')
        if lab:
            lx = x1 - 0.6 if abs(m) <= 1 else (y1 - 0.6 - b) / m if m > 0 else (y0 + 0.6 - b) / m
            lx = max(x0 + 0.3, min(x1 - 0.6, lx))
            ly = m * lx + b
            ly = max(y0 + 0.3, min(y1 - 0.3, ly))
            out.append(f'<text x="{_fmt(X(lx) + 3)}" y="{_fmt(Y(ly) - 4)}" fill="#1f4e79">{lab}</text>')
    for f, lab in curves:
        d = []
        steps = 200
        for i in range(steps + 1):
            x = x0 + (x1 - x0) * i / steps
            try:
                y = f(x)
            except (ZeroDivisionError, ValueError):
                continue
            if y0 - 2 <= y <= y1 + 2:
                d.append(("M" if not d or d[-1][0] == "break" else "L", X(x), Y(y)))
            else:
                d.append(("break", 0, 0))
        # 範囲外で途切れる部分ごとに別の線分にする
        segs, cur = [], []
        for c, px, py in d:
            if c == "break":
                if cur:
                    segs.append(cur)
                cur = []
            else:
                cur.append((px, py))
        if cur:
            segs.append(cur)
        path = " ".join("M" + " L".join(f"{_fmt(px)},{_fmt(py)}" for px, py in sg) for sg in segs if len(sg) > 1)
        out.append(f'<clipPath id="k{len(out)}"><rect x="{_fmt(X(x0))}" y="{_fmt(Y(y1))}" width="{_fmt((x1 - x0) * unit)}" height="{_fmt((y1 - y0) * unit)}"/></clipPath>')
        cid = f"k{len(out) - 1}"
        out.append(f'<path d="{path}" fill="none" stroke="#1f4e79" stroke-width="1.5" clip-path="url(#{cid})"/>')
        if lab and segs:
            px, py = segs[-1][-1]
            out.append(f'<text x="{_fmt(px - 22)}" y="{_fmt(max(py, pad) + 12)}" fill="#1f4e79">{lab}</text>')
    for (ax, ay), (bx, by) in segments:
        out.append(f'<line x1="{_fmt(X(ax))}" y1="{_fmt(Y(ay))}" x2="{_fmt(X(bx))}" y2="{_fmt(Y(by))}" stroke="#333" stroke-width="1"/>')
    for x, y, lab in points:
        out.append(f'<circle cx="{_fmt(X(x))}" cy="{_fmt(Y(y))}" r="2.3" fill="#000"/>')
        if lab:
            out.append(f'<text x="{_fmt(X(x) + 4)}" y="{_fmt(Y(y) - 4)}">{lab}</text>')
    for x, y, lab in labels:
        out.append(f'<text x="{_fmt(X(x))}" y="{_fmt(Y(y))}">{lab}</text>')
    out.append("</svg>")
    return "".join(out)


def shape(points, labels=None, segments=None, scale=22, marks=(), texts=(), dashed=(), circle=None, pad=16):
    """幾何図形。points={名前: (x, y)}、segments=[("A","B"), ...]（省略時は順に閉じた多角形）。
    marks=[(名前, 文字)] は頂点ラベル以外の注記、texts=[(x, y, 文字)]、dashed=[("A","B")]、
    circle=((cx, cy), r)。"""
    xs = [p[0] for p in points.values()]
    ys = [p[1] for p in points.values()]
    if circle:
        (cx, cy), r = circle
        xs += [cx - r, cx + r]
        ys += [cy - r, cy + r]
    for tx, ty, tt in texts:
        xs += [tx, tx + 0.45 * len(tt) * 12 / scale]
        ys += [ty]
    minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
    W = (maxx - minx) * scale + 2 * pad
    H = (maxy - miny) * scale + 2 * pad
    X = lambda x: pad + (x - minx) * scale  # noqa: E731
    Y = lambda y: pad + (maxy - y) * scale  # noqa: E731
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {_fmt(W)} {_fmt(H)}" width="{_fmt(W)}" height="{_fmt(H)}" font-family="serif" font-size="12">']
    if circle:
        (cx, cy), r = circle
        out.append(f'<circle cx="{_fmt(X(cx))}" cy="{_fmt(Y(cy))}" r="{_fmt(r * scale)}" fill="none" stroke="#000" stroke-width="1.2"/>')
    names = list(points)
    segs = segments if segments is not None else [(names[i], names[(i + 1) % len(names)]) for i in range(len(names))]
    for a, b in segs:
        (ax, ay), (bx, by) = points[a], points[b]
        out.append(f'<line x1="{_fmt(X(ax))}" y1="{_fmt(Y(ay))}" x2="{_fmt(X(bx))}" y2="{_fmt(Y(by))}" stroke="#000" stroke-width="1.2"/>')
    for a, b in dashed:
        (ax, ay), (bx, by) = points[a], points[b]
        out.append(f'<line x1="{_fmt(X(ax))}" y1="{_fmt(Y(ay))}" x2="{_fmt(X(bx))}" y2="{_fmt(Y(by))}" stroke="#000" stroke-width="1" stroke-dasharray="4 3"/>')
    cx_ = sum(p[0] for p in points.values()) / len(points)
    cy_ = sum(p[1] for p in points.values()) / len(points)
    for name, (x, y) in points.items():
        if labels is not None and name not in labels:
            continue
        dx, dy = x - cx_, y - cy_
        n = math.hypot(dx, dy) or 1
        lx, ly = X(x) + dx / n * 11 - 4, Y(y) - dy / n * 11 + 4
        out.append(f'<text x="{_fmt(lx)}" y="{_fmt(ly)}">{labels.get(name, name) if isinstance(labels, dict) else name}</text>')
    for x, y, t in texts:
        out.append(f'<text x="{_fmt(X(x))}" y="{_fmt(Y(y))}" font-size="10.5">{t}</text>')
    out.append("</svg>")
    return "".join(out)
