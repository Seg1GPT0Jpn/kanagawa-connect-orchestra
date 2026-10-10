"""高校 単元パック（授業プリント＋問題プリント）の作問ライブラリ。

単元パックのモジュール（scripts/hs_packs/*.py）は次を定義する。

  UNIT_ID     curriculum_map.json の高校単元 ID
  LESSON      lesson(...) で作る授業プリントの内容
  GENERATORS  gen(...) で登録した問題ジェネレータのリスト

問題ジェネレータは乱数 r（random.Random）を受け取り、banks._common の mc / num / sa / desc などで
作った問題 1 問を返す関数。パラメータを変えて何度も呼ばれ、同じ問題文は自動的に除かれる。
各問題には次のキーで詳細解説を付ける（generate_batch.expand_item がスキーマの項目に展開する）。

  ap="思考の糸口"  steps=[解法の手順...]  alt=[別解・別の確かめ方...]  pc=[(部分点のポイント, 点), ...]
  pit=[典型的なつまずき...]  ver="検算"  why={誤答の選択肢の文: 誤りの理由 or (理由, 誤概念)}
  err=dict(sol=誤答例, step=誤りの箇所, type=誤りの種類, tempt=なぜ誤りやすいか, fix=正しい解答)
  ps=[観点タグ]  rel=[関連単元 ID]（融合問題）
"""
from __future__ import annotations

import random
import re
from dataclasses import dataclass, field
from typing import Callable

LEVELS = {
    "basic_check": ("A", "基本確認", "定義・公式をその場で使えるかを確かめる。全問を短時間で解けるまでくり返す。"),
    "standard_practice": ("B", "標準演習", "定期考査・共通テストの標準レベル。解法の選択理由を言えるようにする。"),
    "thinking_writing": ("C", "思考力・記述応用", "場合分け・論証・融合問題。途中の考え方を答案として書く。"),
    "error_correction": ("D", "典型誤答訂正", "よくある誤答例のどこが誤りかを指摘し、正しく直す。"),
}
DEFAULT_POINTS = {"basic_check": 2, "standard_practice": 4, "thinking_writing": 8, "error_correction": 6}


@dataclass
class Gen:
    fn: Callable
    level: str
    n: int
    ps: list
    name: str = ""
    rel: list = field(default_factory=list)


def gen(level: str, n: int, ps: list, rel: list | None = None):
    """問題ジェネレータを登録するデコレータ。n は既定の出題数（--count で全体を比例配分）。"""
    assert level in LEVELS, level

    def deco(fn):
        return Gen(fn=fn, level=level, n=n, ps=list(ps), name=fn.__name__, rel=list(rel or []))
    return deco


# ---------------------------------------------------------------------------
# 授業プリントの部品
# ---------------------------------------------------------------------------

def tp(point, ask=None, expect=None, caution=None, timing=None):
    """教師が口頭で解説すべきポイント（発問・予想反応・注意・タイミング）。"""
    d = {"point": point}
    for k, v in (("ask", ask), ("expect", expect), ("caution", caution), ("timing", timing)):
        if v:
            d[k] = v
    return d


def _sec(kind, id, title, **kw):
    s = {"id": id, "kind": kind, "title": title}
    for k, v in kw.items():
        if v not in (None, [], ""):
            s[k] = v
    return s


def intro(id, title, body, bullets=None, points=None, figure=None):
    return _sec("intro", id, title, body=body, bullets=bullets, teacher_points=points, figure=figure)


def definition(id, title, body, formula=None, conditions=None, points=None, figure=None, bullets=None):
    return _sec("definition", id, title, body=body, formula=formula, conditions=conditions, teacher_points=points, figure=figure, bullets=bullets)


def theorem(id, title, formula, conditions, body=None, proof=None, points=None, figure=None):
    return _sec("theorem", id, title, formula=formula, conditions=conditions, body=body, proof_steps=proof, teacher_points=points, figure=figure)


def derivation(id, title, steps, body=None, points=None, figure=None):
    return _sec("derivation", id, title, proof_steps=steps, body=body, teacher_points=points, figure=figure)


def proof(id, title, steps, body=None, points=None):
    return _sec("proof", id, title, proof_steps=steps, body=body, teacher_points=points)


def example(id, title, problem, steps, answer, thinking=None, points=None, figure=None, misconceptions=None):
    ex = {"problem": problem, "steps": list(steps), "answer": answer}
    if thinking:
        ex["thinking"] = thinking
    if figure:
        ex["figure"] = figure
    mis = [{"wrong": a, "correct": b} for a, b in (misconceptions or [])]
    return _sec("example", id, title, example=ex, teacher_points=points, misconceptions=mis)


def figure_explain(id, title, figure, body, points=None):
    return _sec("figure_explain", id, title, figure=figure, body=body, teacher_points=points)


def board(id, title, columns, points=None):
    return _sec("board_plan", id, title, board={"columns": [{"title": t, "lines": list(ls)} for t, ls in columns]}, teacher_points=points)


def guide(id, title, points, body=None, misconceptions=None):
    mis = [{"wrong": a, "correct": b} for a, b in (misconceptions or [])]
    return _sec("teacher_guide", id, title, teacher_points=points, body=body, misconceptions=mis)


def summary(id, title, bullets, body=None):
    return _sec("summary", id, title, bullets=bullets, body=body)


def check(id, title, items):
    return _sec("check", id, title, check_items=[{"q": q, "a": a} for q, a in items])


def lesson(goals, flow, sections, duration=50, readiness=None):
    return {"goals": list(goals), "duration_minutes": duration,
            "flow": [{"phase": p, "minutes": m, "activity": a} for p, m, a in flow],
            "sections": list(sections), "readiness": list(readiness or [])}


# ---------------------------------------------------------------------------
# 数式の整形
# ---------------------------------------------------------------------------

def sgn(c, first=False):
    """係数の符号つき表記（+3, -3）。first=True のときは先頭の + を省く。"""
    if c < 0:
        return f"-{abs(c)}"
    return f"{c}" if first else f"+{c}"


def poly(*coefs, var="x"):
    """poly(a, b, c) → 'ax^2+bx+c'（係数 0・±1 を整形）。"""
    deg = len(coefs) - 1
    out = []
    for i, c in enumerate(coefs):
        p = deg - i
        if c == 0:
            continue
        mag = abs(c)
        coef = "" if (mag == 1 and p > 0) else str(mag)
        term = coef + (var if p >= 1 else "") + (f"^{p}" if p >= 2 else "")
        sign = "-" if c < 0 else ("+" if out else "")
        out.append(sign + term)
    return "".join(out) or "0"


def frac(p, q):
    """既約分数の LaTeX 表記。"""
    from fractions import Fraction
    f = Fraction(p, q)
    if f.denominator == 1:
        return str(f.numerator)
    s = "-" if f < 0 else ""
    return f"{s}\\dfrac{{{abs(f.numerator)}}}{{{f.denominator}}}"


def fr_py(p, q):
    """sympy 用の分数表記。"""
    from fractions import Fraction
    f = Fraction(p, q)
    return str(f.numerator) if f.denominator == 1 else f"Rational({f.numerator},{f.denominator})"


def nonzero(r, lo, hi, exclude=(0,)):
    while True:
        v = r.randint(lo, hi)
        if v not in exclude:
            return v


def norm_key(item) -> str:
    text = item["s"] + "|" + "|".join(map(str, item.get("c", [])))
    return re.sub(r"\s+", "", text)


def allocate(gens: list[Gen], total: int) -> list[int]:
    """各ジェネレータの既定数 n に比例して、合計がちょうど total になるよう配分する（最大剰余法）。"""
    base = sum(g.n for g in gens)
    raw = [g.n * total / base for g in gens]
    out = [max(1, int(x)) for x in raw]
    order = sorted(range(len(gens)), key=lambda i: raw[i] - int(raw[i]), reverse=True)
    i = 0
    while sum(out) < total:
        out[order[i % len(order)]] += 1
        i += 1
    return out


def run_generators(unit_id: str, gens: list[Gen], total: int, max_tries: int = 200):
    """ジェネレータを実行し、段階順に並んだ問題リストを返す。重複は除き、足りなければ例外。"""
    out = {lv: [] for lv in LEVELS}
    seen: set[str] = set()
    for g, need in zip(gens, allocate(gens, total)):
        got = 0
        tries = 0
        while got < need:
            tries += 1
            if tries > max_tries + need * 20:
                raise RuntimeError(f"{unit_id}:{g.name} の問題パターンが足りません（{got}/{need} 問）。パラメータの範囲を広げてください。")
            r = random.Random(f"{unit_id}|{g.name}|{tries}")
            it = g.fn(r)
            key = norm_key(it)
            if key in seen:
                continue
            seen.add(key)
            it.setdefault("lvl", g.level)
            it["ps"] = list(dict.fromkeys(list(it.get("ps", [])) + g.ps))
            if g.rel and "rel" not in it:
                it["rel"] = list(g.rel)
            it.setdefault("vg", f"{unit_id}-{g.name}")
            it.setdefault("p", DEFAULT_POINTS[g.level])
            out[g.level].append(it)
            got += 1
    return out
