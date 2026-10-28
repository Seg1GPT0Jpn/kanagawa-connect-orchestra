"""単元パック：中学3年 円（神奈川県公立高校入試形式）。"""
import math
import re
import unicodedata
from fractions import Fraction as Fr

from banks._common import figure, mc, num
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem, tp)

UNIT_ID = "JH-MATH-G3-U06"

PREREQUISITES = [
    ("JH-MATH-G2-U05", "二等辺三角形の底角が等しいこと。円周角の定理の証明では、半径でできる二等辺三角形を使う。"),
    ("JH-MATH-G2-U04", "三角形の内角・外角の性質、平行線と角。円の中の角を順に求めるときの土台になる。"),
    ("JH-MATH-G3-U05", "三角形の相似条件と相似の証明。円周角を根拠にした相似の証明（円と相似）で使う。"),
    ("JH-MATH-G1-U05", "円の接線は接点を通る半径に垂直であること、おうぎ形の中心角と弧の関係。"),
]
EXTENSIONS = [
    ("JH-MATH-G3-U07", "直径に対する円周角が直角になることと三平方の定理を組み合わせて、弦や接線の長さを求める。"),
    ("HS-MATHA-U02", "円に内接する四角形の性質、接線と弦のつくる角、方べきの定理へ発展する。"),
    ("HS-MATH1-U04", "正弦定理（三角形の外接円の半径と辺・角の関係）の証明に、円周角の定理を使う。"),
]


# ----------------------------------------------------------------------
# 共通ヘルパー
# ----------------------------------------------------------------------

def _norm(s):
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", s))


def MC(stem, right, cands, e, k=3, **kw):
    """正答 right と誤答候補 [(文, 理由, 誤概念)] から、重複を除いて k 個の誤答を選ぶ。"""
    seen, ws = {_norm(right)}, []
    for t, why, mis in cands:
        if _norm(t) in seen:
            continue
        seen.add(_norm(t))
        ws.append((t, why, mis))
        if len(ws) == k:
            break
    assert len(ws) == k, (stem, right, cands)
    return mc(stem, [right] + [w[0] for w in ws], e, why={w[0]: (w[1], w[2]) for w in ws}, **kw)


def MARK(stem, v, e, expr, **kw):
    """あいう方式（0〜9 のマーク）で答える数値問題。v は 0 以上の整数か既約分数。"""
    v = Fr(v)
    assert v >= 0
    if v.denominator == 1:
        n = int(v)
        return num(stem, str(n), e, mark=("int", n), chk=(expr, str(n), None, "answer"), **kw)
    p, q = v.numerator, v.denominator
    return num(stem, f"$\\dfrac{{{p}}}{{{q}}}$", e, mark=("frac", p, q), chk=(expr, f"Rational({p},{q})", None, "answer"), **kw)


def RATIO(stem, a, b, e, expr, **kw):
    """最も簡単な整数の比 a：b をマークで答える問題。expr は a/b の値になる式。"""
    g = math.gcd(a, b)
    a, b = a // g, b // g
    assert a >= 1 and b >= 1 and (a, b) != (1, 1)
    return num(stem, f"${a}:{b}$", e, mark=("ratio", a, b), chk=(expr, f"Rational({a},{b})", None, "intermediate"), **kw)


SEL4 = "次の1〜4の中から1つ選び，その番号を答えなさい。"


def A(s):
    return f"\\angle\\mathrm{{{s}}}"


def ftex(v):
    v = Fr(v)
    if v.denominator == 1:
        return str(v.numerator)
    s = "-" if v < 0 else ""
    return f"{s}\\dfrac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def fpy(v):
    v = Fr(v)
    return str(v.numerator) if v.denominator == 1 else f"Rational({v.numerator},{v.denominator})"


def _robust(g):
    """選択肢が重複して誤答が足りないパラメータのときは、同じ乱数列から別のパラメータを引き直す。"""
    import random as _random
    fn = g.fn

    def wrapped(r):
        for _ in range(50):
            try:
                return fn(r)
            except AssertionError:
                r = _random.Random(r.random())
        return fn(r)
    wrapped.__name__ = fn.__name__
    g.fn = wrapped
    return g


# ----------------------------------------------------------------------
# 図（SVG）
# ----------------------------------------------------------------------

def _f(v):
    return f"{v:.1f}"


def geo(pts, segs=(), dashed=(), texts=(), names=None, off=None, scale=26, pad=20, ticks=(), right=(), dots=(), circles=()):
    """幾何の図。pts={名前: (x, y)}、segs=[("A","B"), ...]、texts=[(x, y, 文字)]、off={名前: (dx, dy)}、
    ticks=[("A","B",本数)] 等しい長さの印、right=[("B","A","C")] 頂点 A の直角の印。"""
    names = list(pts) if names is None else list(names)
    xs = [p[0] for p in pts.values()] + [t[0] for t in texts] + [c[0] - c[2] for c in circles] + [c[0] + c[2] for c in circles]
    ys = [p[1] for p in pts.values()] + [t[1] for t in texts] + [c[1] - c[2] for c in circles] + [c[1] + c[2] for c in circles]
    minx, maxx, miny, maxy = min(xs) - 0.5, max(xs) + 0.5, min(ys) - 0.5, max(ys) + 0.5
    W, H = (maxx - minx) * scale + 2 * pad, (maxy - miny) * scale + 2 * pad
    X = lambda x: pad + (x - minx) * scale  # noqa: E731
    Y = lambda y: pad + (maxy - y) * scale  # noqa: E731
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {_f(W)} {_f(H)}" width="{_f(W)}" height="{_f(H)}" font-family="serif" font-size="12">']
    for cx0, cy0, rr in circles:
        o.append(f'<circle cx="{_f(X(cx0))}" cy="{_f(Y(cy0))}" r="{_f(rr * scale)}" fill="none" stroke="#000" stroke-width="1.1"/>')
    for a, b in segs:
        (ax, ay), (bx, by) = pts[a], pts[b]
        o.append(f'<line x1="{_f(X(ax))}" y1="{_f(Y(ay))}" x2="{_f(X(bx))}" y2="{_f(Y(by))}" stroke="#000" stroke-width="1.1"/>')
    for a, b in dashed:
        (ax, ay), (bx, by) = pts[a], pts[b]
        o.append(f'<line x1="{_f(X(ax))}" y1="{_f(Y(ay))}" x2="{_f(X(bx))}" y2="{_f(Y(by))}" stroke="#000" stroke-width="1" stroke-dasharray="4 3"/>')
    for a, b, n in ticks:
        (ax, ay), (bx, by) = pts[a], pts[b]
        mx, my = (X(ax) + X(bx)) / 2, (Y(ay) + Y(by)) / 2
        dx, dy = X(bx) - X(ax), Y(by) - Y(ay)
        L = math.hypot(dx, dy) or 1
        ux, uy = dx / L, dy / L
        for k in range(n):
            s = (k - (n - 1) / 2) * 4
            cx, cy = mx + ux * s, my + uy * s
            o.append(f'<line x1="{_f(cx - uy * 5)}" y1="{_f(cy + ux * 5)}" x2="{_f(cx + uy * 5)}" y2="{_f(cy - ux * 5)}" stroke="#000" stroke-width="1"/>')
    for b, a, c in right:
        (ax, ay), (bx, by), (cx, cy) = pts[a], pts[b], pts[c]

        def u(px, py):
            dx, dy = X(px) - X(ax), Y(py) - Y(ay)
            L = math.hypot(dx, dy) or 1
            return dx / L * 8, dy / L * 8
        (ux, uy), (vx_, vy_) = u(bx, by), u(cx, cy)
        p0 = (X(ax) + ux, Y(ay) + uy)
        p1 = (X(ax) + ux + vx_, Y(ay) + uy + vy_)
        p2 = (X(ax) + vx_, Y(ay) + vy_)
        o.append(f'<polyline points="{_f(p0[0])},{_f(p0[1])} {_f(p1[0])},{_f(p1[1])} {_f(p2[0])},{_f(p2[1])}" fill="none" stroke="#000" stroke-width="0.8"/>')
    for d in dots:
        x, y = pts[d]
        o.append(f'<circle cx="{_f(X(x))}" cy="{_f(Y(y))}" r="2" fill="#000"/>')
    cx_ = sum(p[0] for p in pts.values()) / len(pts)
    cy_ = sum(p[1] for p in pts.values()) / len(pts)
    for nm in names:
        x, y = pts[nm]
        if off and nm in off:
            lx, ly = X(x + off[nm][0]), Y(y + off[nm][1])
        else:
            dx, dy = x - cx_, y - cy_
            L = math.hypot(dx, dy) or 1
            lx, ly = X(x) + dx / L * 11, Y(y) - dy / L * 11
        o.append(f'<text x="{_f(lx)}" y="{_f(ly + 4)}" text-anchor="middle">{nm[0]}</text>')
    for x, y, t in texts:
        o.append(f'<text x="{_f(X(x))}" y="{_f(Y(y) + 4)}" text-anchor="middle" font-size="11">{t}</text>')
    o.append("</svg>")
    return "".join(o)


def tri_xy(a, b, c, size=4.6):
    """BC=a, CA=b, AB=c の三角形の頂点（B を原点、BC を x 軸）。最長辺がおよそ size になるよう縮める。"""
    x = (c * c - b * b + a * a) / (2 * a)
    y = math.sqrt(max(c * c - x * x, 0.01))
    s = size / max(a, b, c)
    return {"A": (x * s, y * s), "B": (0.0, 0.0), "C": (a * s, 0.0)}


def lerp(P, Q, t):
    return (P[0] + (Q[0] - P[0]) * t, P[1] + (Q[1] - P[1]) * t)


def inter(P1, P2, P3, P4):
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = P1, P2, P3, P4
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
    return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))




R0 = 2.2


def on(deg, R=R0):
    t = math.radians(deg)
    return (R * math.cos(t), R * math.sin(t))


def cfig(ang, segs=(), center=False, alt="円", extra=None, dashed=(), off=None, right=(), names=None):
    """円周上の点 ang={名前: 角度(度)}、center=True で中心 O を表示、extra={名前: (x, y)}。"""
    pts = {n: on(a) for n, a in ang.items()}
    if center:
        pts["O"] = (0.0, 0.0)
    if extra:
        pts |= extra
    o = {"O": (0.22, -0.32)} | (off or {})
    return figure(alt, geo(pts, segs=segs, dashed=dashed, off=o, circles=[(0.0, 0.0, R0)], right=right, names=names, scale=30))


def ang(v):
    return f"${v}^\\circ$"


# ----------------------------------------------------------------------
# 授業プリント
# ----------------------------------------------------------------------

LESSON = lesson(
    goals=["円周角と中心角の関係（円周角の定理）を、場合に分けて証明し、角の大きさを求めるのに使える。",
           "円周角の定理の逆を理解し、4点が1つの円周上にあるかどうかを判断できる。",
           "円周角の定理を根拠にして、円の中にできる三角形の相似を証明し、線分の長さを求められる。"],
    duration=100,
    readiness=["二等辺三角形の底角が等しいこと、三角形の外角はとなり合わない2つの内角の和に等しいことを使える。",
               "円の接線は接点を通る半径に垂直であることを知っている。",
               "三角形の相似条件（特に2組の角）を使って相似を証明できる。"],
    flow=[("導入：見える角度が同じ席", 10, "劇場のステージを見こむ角が等しくなる席はどこかを考え、円周角への問いをもつ"),
          ("円周角の定理", 25, "用語（円周角・中心角）、3つの場合に分けた証明、半円の弧に対する円周角（例題1）"),
          ("弧と円周角", 10, "等しい弧に対する円周角、弧の長さと円周角の比例"),
          ("円周角の定理の逆", 20, "円の内部・外部の点と角の大小から逆を説明、4点が同じ円周上にある条件（例題2）"),
          ("円と相似", 25, "円周角を根拠にした相似の証明と線分の長さ（例題3）"),
          ("まとめと確認", 10, "確認問題と問題プリントの指示")],
    sections=[
        intro("in1", "同じ角度でステージが見える席",
              "円形の劇場で、ステージの両端 A、B を見こむ角が同じになる席はどこだろうか。実は、A、B を通る円の周上（AB について同じ側）に席があれば、どの席からも同じ角度で見える。この単元では、その理由を「円周角の定理」として学ぶ。",
              bullets=["円 O の周上の点 P について、弧 AB をのぞく部分に P があるとき、∠APB を弧 AB に対する円周角という。",
                       "∠AOB を弧 AB に対する中心角という。"],
              points=[tp("円周上のいろいろな位置に P をとって ∠APB を分度器ではからせ、「いつも同じ」「中心角の半分」に気づかせる。",
                         ask="P を動かすと ∠APB はどうなるか。", expect="どこでも同じ大きさになる。", timing="導入")]),
        theorem("th1", "円周角の定理",
                "$$\\angle\\mathrm{APB}=\\dfrac{1}{2}\\angle\\mathrm{AOB}$$",
                ["1つの弧に対する円周角の大きさは一定であり、その弧に対する中心角の大きさの半分である。",
                 "同じ弧（または長さの等しい弧）に対する円周角の大きさは等しい。",
                 "半円の弧に対する円周角は $90^\\circ$ である（直径 AB に対して ∠APB$=90^\\circ$）。",
                 "1つの円で、円周角の大きさは弧の長さに比例する。"],
                proof=["【中心 O が ∠APB の辺の上にある場合】OP$=$OA（半径）より △OPA は二等辺三角形で、∠OPA$=$∠OAP。",
                       "∠AOB は △OPA の外角なので、∠AOB$=$∠OPA$+$∠OAP$=2$∠APB。よって ∠APB$=\\dfrac{1}{2}$∠AOB。",
                       "【O が ∠APB の内部にある場合】直径 PQ をひくと、∠APB$=$∠APQ$+$∠QPB$=\\dfrac{1}{2}$∠AOQ$+\\dfrac{1}{2}$∠QOB$=\\dfrac{1}{2}$∠AOB。",
                       "【O が ∠APB の外部にある場合】直径 PQ をひき、差を考えると ∠APB$=$∠QPB$-$∠QPA$=\\dfrac{1}{2}$(∠QOB$-$∠QOA)$=\\dfrac{1}{2}$∠AOB。"],
                points=[tp("証明は「O が辺上」を基本形とし、残りの2つの場合はそれを足す・引くことで導けることを強調する。",
                           ask="O が ∠APB の内部にあるとき、どんな補助線をひけば基本形が使えるか。", expect="P を通る直径をひく。"),
                        tp("「半円の弧に対する円周角は直角」は、中心角が $180^\\circ$ の特別な場合であることを確認する。", timing="定理のあと")]),
        theorem("th2", "円周角の定理の逆",
                "$$\\angle\\mathrm{APB}=\\angle\\mathrm{AQB}\\ \\Longrightarrow\\ \\text{4点 A，B，P，Q は1つの円周上にある}$$",
                ["2点 P、Q が直線 AB について同じ側にあって ∠APB$=$∠AQB ならば、4点 A、B、P、Q は1つの円周上にある。",
                 "「同じ側にある」という条件が大切。反対側にある場合は、この形では使えない。",
                 "特に ∠APB$=$∠AQB$=90^\\circ$ ならば、P、Q は AB を直径とする円の周上にある。"],
                proof=["A、B、P を通る円をかき、Q が円の内部・周上・外部のどこにあるかで場合を分ける。",
                       "Q が円の内部にあれば、AQ の延長と円の交点を R として、外角の性質から ∠AQB$>$∠ARB$=$∠APB となる。",
                       "Q が円の外部にあれば、同じようにして ∠AQB$<$∠APB となる。",
                       "∠AQB$=$∠APB なので、Q は円の内部にも外部にもなく、円周上にある。"],
                points=[tp("円の内部・外部の点で角が大きく・小さくなることを、図を動かして確かめさせてから逆の証明に入る。",
                           caution="「同じ側」の条件を落とす誤りが多い。反対側に点をとった反例の図を見せる。")]),
        derivation("dv1", "円と相似：交わる2つの弦",
                   ["円の2つの弦 AB、CD が点 P で交わっているとする。",
                    "△PAC と △PDB において、弧 BC に対する円周角は等しいので ∠PAC$=$∠PDB。",
                    "対頂角は等しいので ∠APC$=$∠DPB。",
                    "2組の角がそれぞれ等しいので △PAC∽△PDB。",
                    "対応する辺の比は等しいので PA：PD$=$PC：PB。よって PA$\\times$PB$=$PC$\\times$PD が成り立つ。"],
                   points=[tp("円周角の定理は「等しい角を見つける道具」であり、相似の証明の根拠になることを意識させる。",
                              ask="弧 BC に対する円周角はどれとどれか。", expect="∠BAC と ∠BDC。")]),
        example("ex1", "例題1　円周角と中心角",
                "円 O の周上に3点 A、B、C があり、∠AOB$=128^\\circ$ である。点 C が弧 AB のうち長い方の上にあるとき、∠ACB の大きさを求めなさい。また、点 C が短い方の弧の上にあるときはどうなるか。",
                ["C が長い方の弧の上にあるとき、∠ACB は弧 AB（短い方）に対する円周角なので ∠ACB$=128^\\circ\\div2=64^\\circ$。",
                 "C が短い方の弧の上にあるとき、∠ACB は長い方の弧 AB に対する円周角で、その中心角は $360^\\circ-128^\\circ=232^\\circ$。",
                 "∠ACB$=232^\\circ\\div2=116^\\circ$。"],
                "$64^\\circ$（長い方の弧の上）、$116^\\circ$（短い方の弧の上）",
                thinking="円周角がどちらの弧に対するものかを、まず図で確かめる。",
                figure=cfig({"A": 210, "B": 334, "C": 90}, segs=[("A", "C"), ("B", "C"), ("O", "A"), ("O", "B")], center=True, alt="円 O と円周角"),
                points=[tp("C を短い方の弧に移した図もかかせ、中心角が $180^\\circ$ をこえる場合を確認させる。")],
                misconceptions=[("C の位置に関係なく ∠ACB$=64^\\circ$", "C が短い方の弧上なら、長い方の弧に対する円周角になり $116^\\circ$")]),
        example("ex2", "例題2　円周角の定理の逆",
                "四角形 ABCD で、対角線 AC と BD の交点を E とする。∠BAC$=38^\\circ$、∠BDC$=38^\\circ$、∠ACB$=55^\\circ$ のとき、∠ADB の大きさを求めなさい。",
                ["2点 A、D は直線 BC について同じ側にあり、∠BAC$=$∠BDC なので、円周角の定理の逆より 4点 A、B、C、D は1つの円周上にある。",
                 "∠ADB と ∠ACB は弧 AB に対する円周角なので等しい。", "∠ADB$=55^\\circ$。"],
                "$55^\\circ$",
                thinking="等しい角の組から「4点が同じ円周上にある」ことを見つければ、円周角の定理が使えるようになる。",
                points=[tp("円がかかれていない図でも、円周角の定理の逆で円を「見つける」と角が求められることを強調する。")]),
        example("ex3", "例題3　円と相似",
                "円の2つの弦 AB、CD が点 P で交わっている。PA$=6$ cm、PB$=4$ cm、PC$=3$ cm のとき、PD の長さを求めなさい。",
                ["△PAC∽△PDB（弧 BC に対する円周角、対頂角）。", "PA：PD$=$PC：PB より $6:$ PD $=3:4$。", "PD$=8$ cm。"],
                "$8$ cm",
                thinking="まず相似な三角形の組を見つけ、対応する辺を正しく並べる。",
                figure=cfig({"A": 160, "B": -20, "C": 80, "D": 230}, segs=[("A", "B"), ("C", "D"), ("A", "C"), ("D", "B")],
                            extra={"P": inter(on(160), on(-20), on(80), on(230))}, off={"P": (0.3, -0.3)}, alt="交わる2つの弦"),
                points=[tp("PA$\\times$PB$=$PC$\\times$PD は高校で「方べきの定理」として学ぶことを紹介し、中学では相似から導くことを確認する。")]),
        board("bd1", "板書案",
              [("① 円周角の定理", ["円周角＝中心角の½", "同じ弧の円周角は等しい", "半円の弧 → 90°", "円周角は弧の長さに比例"]),
               ("② 円周角の定理の逆", ["P，Q が AB の同じ側", "∠APB＝∠AQB", "→ A，B，P，Q は同一円周上", "反対側ではダメ（反例の図）"]),
               ("③ 円と相似", ["等しい円周角 → 2組の角", "△PAC∽△PDB", "PA：PD＝PC：PB", "PA×PB＝PC×PD"])],
              points=[tp("③では、等しい円周角に同じ印をつけた図を必ず板書する。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("角を求める問題では「この角はどの弧に対する円周角か」を言わせてから計算させる。", ask="∠ACB はどの弧に対する円周角か。", expect="弧 AB。"),
               tp("直径があれば直角ができる、というパターンを最初に探す習慣をつけさせる。"),
               tp("入試では、円周角を根拠とする相似の証明の空欄補充と、角度を求める問題がセットで出題されやすい。証明の根拠のことば（「弧 ○○ に対する円周角」）を正確に書けるようにする。", timing="まとめ")],
              misconceptions=[("円周角は中心角の2倍", "円周角は中心角の半分"),
                              ("円周角の定理の逆は、P、Q が直線 AB の反対側にあっても使える", "同じ側にあることが条件"),
                              ("C がどちらの弧の上にあっても、円周角は同じ", "C がある弧と反対側の弧に対する円周角になる")]),
        summary("sm1", "まとめ",
                ["円周角は、同じ弧に対する中心角の半分。同じ弧に対する円周角は等しい。",
                 "半円の弧（直径）に対する円周角は $90^\\circ$。", "円周角の大きさは弧の長さに比例する。",
                 "同じ側にある2点から見こむ角が等しければ、4点は1つの円周上にある（円周角の定理の逆）。",
                 "等しい円周角を使って三角形の相似を証明し、線分の長さを求められる。"]),
        check("ck1", "確認問題",
              [("弧 AB に対する中心角が $140^\\circ$ のとき、弧 AB に対する円周角を求めなさい。", "$70^\\circ$"),
               ("AB を直径とする円の周上に点 C がある。∠CAB$=25^\\circ$ のとき、∠CBA を求めなさい。", "∠ACB$=90^\\circ$ より $65^\\circ$"),
               ("円の2つの弦 AB、CD が点 P で交わり、PA$=4$、PB$=9$、PC$=6$ のとき、PD を求めなさい。", "$4\\times9=6\\times$PD より $6$")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

@gen("basic_check", 4, ["computation"])
def a_central(r):
    kind = r.choice(["c2i", "i2c", "minor", "reflex"])
    if kind == "c2i":
        x = r.choice(range(40, 171, 2))
        v = x // 2
        stem = f"右の図のように，円 O の周上に3点 A，B，C があり，${A('AOB')}={x}^\\circ$ である。点 C が弧 AB のうち長い方の上にあるとき，${A('ACB')}$ の大きさは何度か，求めなさい。"
        st = ["∠ACB は弧 AB に対する円周角，∠AOB は弧 AB に対する中心角。", f"${A('ACB')}=\\dfrac{{1}}{{2}}\\times{x}^\\circ={v}^\\circ$。"]
        expr, cang = f"{x}/2", x
    elif kind == "i2c":
        y = r.randint(20, 85)
        v = 2 * y
        stem = f"右の図のように，円 O の周上に3点 A，B，C があり，${A('ACB')}={y}^\\circ$ である。点 C が弧 AB のうち長い方の上にあるとき，${A('AOB')}$ の大きさは何度か，求めなさい。"
        st = ["中心角は円周角の2倍。", f"${A('AOB')}=2\\times{y}^\\circ={v}^\\circ$。"]
        expr, cang = f"2*{y}", v
    elif kind == "minor":
        x = r.choice(range(60, 171, 2))
        v = 180 - x // 2
        stem = f"円 O の周上に3点 A，B，C があり，${A('AOB')}={x}^\\circ$ である。点 C が弧 AB のうち短い方の上にあるとき，${A('ACB')}$ の大きさは何度か，求めなさい。"
        st = ["C が短い方の弧の上にあるので，∠ACB は長い方の弧 AB に対する円周角。", f"長い方の弧に対する中心角は $360^\\circ-{x}^\\circ={360 - x}^\\circ$。",
              f"${A('ACB')}=\\dfrac{{1}}{{2}}\\times{360 - x}^\\circ={v}^\\circ$。"]
        expr, cang = f"(360-{x})/2", x
    else:
        y = r.randint(95, 165)
        v = 360 - 2 * y
        stem = f"円 O の周上に3点 A，B，C があり，点 C は弧 AB のうち短い方の上にある。${A('ACB')}={y}^\\circ$ のとき，${A('AOB')}$（$180^\\circ$ より小さい方の角）の大きさは何度か，求めなさい。"
        st = [f"∠ACB は長い方の弧 AB に対する円周角なので，その中心角は $2\\times{y}^\\circ={2 * y}^\\circ$。",
              f"${A('AOB')}=360^\\circ-{2 * y}^\\circ={v}^\\circ$。"]
        expr, cang = f"360-2*{y}", v
    h = cang / 2
    cpos = 90 if kind in ("c2i", "i2c") else -90
    fig = cfig({"A": -90 - h, "B": -90 + h, "C": cpos},
               segs=[("A", "C"), ("B", "C"), ("O", "A"), ("O", "B")], center=True, alt="円 O と中心角・円周角")
    return MARK(stem, v, st[-1], expr, d=1, fig=fig,
                ap="円周角は同じ弧に対する中心角の半分。まず，その円周角がどちらの弧に対するものかを確かめる。",
                steps=st,
                alt=["半径でできる二等辺三角形 OAC，OBC の底角を使って，円周角の定理の証明と同じ考え方で確かめる。"],
                pc=[("どの弧に対する円周角・中心角かを正しく判断している", 1), ("正しい大きさを求めている", 1)],
                pit=["円周角と中心角の関係（半分・2倍）を逆にする。", "C が短い方の弧の上にあることを見落とす。"])


@gen("basic_check", 4, ["computation", "concept"])
def a_diameter(r):
    kind = r.choice(["right", "same_arc", "outer"])
    t = r.randint(18, 72)
    if kind == "right":
        given = r.choice(["ABC", "BAC"])
        other = "BAC" if given == "ABC" else "ABC"
        v = 90 - t
        stem = f"右の図のように，線分 AB を直径とする円 O の周上に点 C がある。${A(given)}={t}^\\circ$ のとき，${A(other)}$ の大きさは何度か，求めなさい。"
        st = ["半円の弧に対する円周角なので ∠ACB$=90^\\circ$。", f"${A(other)}=180^\\circ-90^\\circ-{t}^\\circ={v}^\\circ$。"]
        expr = f"90-{t}"
        fig = cfig({"A": 180, "B": 0, "C": 180 - 2 * t if given == "ABC" else 2 * t}, segs=[("A", "B"), ("A", "C"), ("B", "C")], center=True, alt="直径 AB と円周上の点 C")
    elif kind == "same_arc":
        v = 90 - t
        stem = f"右の図のように，線分 AB を直径とする円 O の周上に2点 C，D があり，C と D は直線 AB について反対側にある。${A('ADC')}={t}^\\circ$ のとき，${A('BAC')}$ の大きさは何度か，求めなさい。"
        st = ["∠ABC と ∠ADC は弧 AC に対する円周角なので，∠ABC$=" + f"{t}^\\circ$。", "AB は直径なので ∠ACB$=90^\\circ$。", f"${A('BAC')}=180^\\circ-90^\\circ-{t}^\\circ={v}^\\circ$。"]
        expr = f"90-{t}"
        fig = cfig({"A": 180, "B": 0, "C": 180 - 2 * t, "D": -110}, segs=[("A", "B"), ("A", "C"), ("B", "C"), ("A", "D"), ("D", "C")], center=True, alt="直径 AB と円周上の点 C，D")
    else:
        s = r.randint(20, 70)
        v = 90 - s
        stem = (f"右の図のように，線分 AB を直径とする円 O の周上に点 C があり，中心 O と点 C を結ぶ。${A('ABC')}={s}^\\circ$ のとき，"
                f"${A('OCA')}$ の大きさは何度か，求めなさい。")
        st = ["AB は直径なので ∠ACB$=90^\\circ$。", f"∠BAC$=180^\\circ-90^\\circ-{s}^\\circ={v}^\\circ$。",
              f"OA$=$OC（半径）より △OAC は二等辺三角形なので，∠OCA$=$∠OAC$={v}^\\circ$。"]
        expr = f"180-90-{s}"
        fig = cfig({"A": 180, "B": 0, "C": 180 - 2 * s}, segs=[("A", "B"), ("A", "C"), ("B", "C"), ("O", "C")], center=True, alt="直径 AB と円周上の点 C")
    return MARK(stem, v, st[-1], expr, d=1, fig=fig,
                ap="直径があれば，半円の弧に対する円周角は $90^\\circ$。三角形の内角の和と組み合わせる。",
                steps=st,
                alt=["中心 O と C を結ぶと二等辺三角形 OAC，OBC ができる。底角を使って確かめることもできる。"],
                pc=[("直径に対する円周角が直角であることを使っている", 1), ("正しい大きさを求めている", 1)],
                pit=["直径に対する円周角を $180^\\circ$ と考える。", "同じ弧に対する円周角の組を取り違える。"])


@gen("basic_check", 4, ["computation"])
def a_same_arc(r):
    x = r.randint(20, 70)
    y = r.randint(20, 70)
    if x + y >= 150:
        y = 150 - x - 5
    kind = r.choice(["bdc", "acd", "apb", "bpc"])
    fig = cfig({"A": 150, "B": 215, "C": -30, "D": 70}, segs=[("A", "B"), ("B", "D"), ("D", "C"), ("C", "A"), ("A", "C"), ("B", "D")],
               extra={"P": inter(on(150), on(-30), on(215), on(70))}, off={"P": (0.0, -0.4)}, alt="円周上の4点と対角線")
    head = f"右の図のように，円周上に4点 A，B，C，D があり，線分 AC と BD の交点を P とする。${A('BAC')}={x}^\\circ$，${A('ABD')}={y}^\\circ$ のとき，"
    if kind == "bdc":
        v = x
        stem = head + f"${A('BDC')}$ の大きさは何度か，求めなさい。"
        st = ["∠BAC と ∠BDC は弧 BC に対する円周角。", f"${A('BDC')}={A('BAC')}={x}^\\circ$。"]
        expr = f"{x}"
    elif kind == "acd":
        v = y
        stem = head + f"${A('ACD')}$ の大きさは何度か，求めなさい。"
        st = ["∠ABD と ∠ACD は弧 AD に対する円周角。", f"${A('ACD')}={A('ABD')}={y}^\\circ$。"]
        expr = f"{y}"
    elif kind == "apb":
        v = 180 - x - y
        stem = head + f"${A('APB')}$ の大きさは何度か，求めなさい。"
        st = ["△ABP の内角の和を使う。", f"${A('APB')}=180^\\circ-{x}^\\circ-{y}^\\circ={v}^\\circ$。"]
        expr = f"180-{x}-{y}"
    else:
        v = x + y
        stem = head + f"${A('BPC')}$ の大きさは何度か，求めなさい。"
        st = ["∠BPC は △ABP の外角。", f"${A('BPC')}={A('BAP')}+{A('ABP')}={x}^\\circ+{y}^\\circ={v}^\\circ$。"]
        expr = f"{x}+{y}"
    return MARK(stem, v, st[-1], expr, d=1, fig=fig,
                ap="同じ弧に対する円周角は等しい。どの角がどの弧に対する円周角かを，弧の両端の点から読み取る。",
                steps=st,
                alt=["△DCP の内角や外角を使って同じ答えになるか確かめる（∠BDC，∠ACD も同じ大きさ）。"],
                pc=[("同じ弧に対する円周角を正しく見つけている", 1), ("正しい大きさを求めている", 1)],
                pit=["弧の両端を取り違え，別の弧に対する円周角を等しいとする。"])


@gen("basic_check", 4, ["computation", "concept"])
def a_arc_ratio(r):
    kind = r.choice(["div", "div", "ratio"])
    if kind == "div":
        n = r.choice([5, 6, 8, 9, 10, 12, 15, 18])
        unit = Fr(180, n)
        names = "ABCDEFGHIJKLMNOPQR"[:n]
        i, j = 0, r.randint(1, n // 2)
        k = r.randint(j + 1, n - 1)
        if (unit * j).denominator != 1:
            raise AssertionError
        v = unit * j
        stem = f"円周を ${n}$ 等分する点を，順に {names[0]}，{names[1]}，{names[2]}，…，{names[n - 1]} とする。${A(names[i] + names[k] + names[j])}$ の大きさは何度か，求めなさい。"
        st = [f"弧1つ分に対する中心角は $360^\\circ\\div{n}={ftex(Fr(360, n))}^\\circ$，円周角は ${ftex(unit)}^\\circ$。",
              f"∠{names[i]}{names[k]}{names[j]} は弧 {names[i]}{names[j]}（{names[k]} をふくまない方，弧 ${j}$ つ分）に対する円周角。",
              f"${ftex(unit)}^\\circ\\times{j}={ftex(v)}^\\circ$。"]
        expr = f"Rational(180,{n})*{j}"
        angs = {names[t]: 90 - 360 * t / n for t in sorted({i, j, k})}
        fig = cfig(angs, segs=[(names[k], names[i]), (names[k], names[j])], alt=f"円周を {n} 等分する点")
    else:
        p, q = r.sample(range(1, 7), 2)
        x = r.choice([d for d in range(20, 80) if (d * q) % p == 0 and d * (p + q) // p < 170] or [AssertionError])
        if not isinstance(x, int):
            raise AssertionError
        v = Fr(x * q, p)
        stem = f"円周上に3点 A，B，C があり，弧 AB と弧 BC の長さの比は ${p}:{q}$ である（どちらも点 C，A をふくまない方の弧）。${A('ACB')}={x}^\\circ$ のとき，${A('BAC')}$ の大きさは何度か，求めなさい。"
        st = ["1つの円で，円周角の大きさは弧の長さに比例する。", f"∠ACB（弧 AB）：∠BAC（弧 BC）$={p}:{q}$。", f"${A('BAC')}={x}^\\circ\\times\\dfrac{{{q}}}{{{p}}}={ftex(v)}^\\circ$。"]
        expr = f"Rational({x}*{q},{p})"
        a1 = 2 * x
        fig = cfig({"A": 200, "B": 200 + a1, "C": 200 + a1 + 2 * float(v)}, segs=[("A", "C"), ("B", "C"), ("A", "B")], alt="円周上の3点")
    return MARK(stem, v, st[-1], expr, d=2, fig=fig,
                ap="円周角の大きさは弧の長さに比例する。等分点なら，弧1つ分に対する円周角を先に求める。",
                steps=st,
                alt=["中心角（弧1つ分は $360^\\circ$ の等分）を先に求め，その半分として円周角を求めてもよい。"],
                pc=[("弧と円周角の比例関係を使っている", 1), ("正しい大きさを求めている", 1)],
                pit=["中心角と円周角を取り違える（半分にし忘れる）。", "どの弧に対する円周角かを取り違える。"])


PAIRS_SAME = [("BAC", "BDC"), ("ABD", "ACD"), ("CAD", "CBD"), ("ADB", "ACB")]
PAIRS_DIFF = [("BAC", "ABD"), ("BAC", "ACD"), ("ABD", "BDC"), ("CAD", "ACB"), ("ADB", "BAC"), ("CBD", "ACD")]


@gen("basic_check", 4, ["condition_check", "concept"])
def a_converse(r):
    x = r.randint(25, 70)
    right_pair = r.choice(PAIRS_SAME)
    right = f"${A(right_pair[0])}={x}^\\circ$，${A(right_pair[1])}={x}^\\circ$"
    cands = []
    for p1, p2 in r.sample(PAIRS_DIFF, 3):
        cands.append((f"${A(p1)}={x}^\\circ$，${A(p2)}={x}^\\circ$", f"∠{p1} と ∠{p2} は同じ線分を見こむ角ではないので，等しくても円周角の定理の逆は使えない。", "円周角の定理の逆の条件の誤解"))
    for p1, p2 in r.sample([s for s in PAIRS_SAME if s != right_pair], 2):
        y = x + r.choice([-6, -4, 4, 6])
        cands.append((f"${A(p1)}={x}^\\circ$，${A(p2)}={y}^\\circ$", f"同じ線分を見こむ角だが，大きさが等しくないので，4点は1つの円周上にない。", "角の大きさの読み落とし"))
    r.shuffle(cands)
    fig = figure("四角形 ABCD と対角線", geo({"A": (0.4, 2.6), "B": (-0.4, 0.0), "C": (4.6, 0.0), "D": (3.6, 2.9)},
                                             segs=[("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("A", "C"), ("B", "D")]))
    seg = {"BAC": "BC", "BDC": "BC", "ABD": "AD", "ACD": "AD", "CAD": "CD", "CBD": "CD", "ADB": "AB", "ACB": "AB"}[right_pair[0]]
    return MC("右の図のように，四角形 ABCD に対角線 AC，BD をひいた。4点 A，B，C，D が1つの円周上にあるといえる条件として最も適するものを，" + SEL4,
              right, cands, f"∠{right_pair[0]} と ∠{right_pair[1]} は，線分 {seg} について同じ側にある2点から {seg} を見こむ角で，それが等しいので，円周角の定理の逆より4点は1つの円周上にある。", d=2,
              fig=fig,
              ap="円周角の定理の逆：同じ線分を，その線分について同じ側にある2点から見こむ角が等しければ，4点は1つの円周上にある。",
              steps=["それぞれの2つの角が，どの線分を見こむ角かを調べる。", f"同じ線分（{seg}）を見こみ，大きさも等しいものを選ぶ。"],
              alt=["条件を満たすときに，どの弧に対する円周角になるかを考えて確かめる。"],
              pc=[("見こむ線分を正しく読み取っている", 1), ("正しい条件を選んでいる", 1)],
              pit=["大きさが等しいだけで，同じ線分を見こむ角かどうかを確かめない。"])


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 4, ["computation", "application"])
def b_angle_chase(r):
    kind = r.choice(["oab", "obc", "two_arcs"])
    if kind == "oab":
        t = r.randint(15, 75)
        v = 90 - t
        stem = (f"右の図で，3点 A，B，C は中心が O の円の周上の点で，弦 AB と半径 OA のつくる角 ${A('OAB')}$ は ${t}^\\circ$ である。"
                f"点 C が直線 AB について中心 O と同じ側にあるとき，${A('ACB')}$ の大きさを求めなさい。")
        st = ["OA$=$OB（半径）なので △OAB は二等辺三角形で ∠OBA$=" + f"{t}^\\circ$。", f"∠AOB$=180^\\circ-2\\times{t}^\\circ={180 - 2 * t}^\\circ$。",
              f"${A('ACB')}=\\dfrac{{1}}{{2}}\\times{180 - 2 * t}^\\circ={v}^\\circ$。"]
        expr = f"(180-2*{t})/2"
        h = 90 - t
        fig = cfig({"A": -90 - h, "B": -90 + h, "C": 100}, segs=[("A", "B"), ("A", "C"), ("B", "C"), ("O", "A"), ("O", "B")], center=True, alt="円 O と二等辺三角形 OAB")
    elif kind == "obc":
        a = r.randint(25, 80)
        v = 90 - a
        stem = f"右の図のように，円 O の周上に3点 A，B，C があり，${A('BAC')}={a}^\\circ$ である。中心 O が △ABC の内部にあるとき，${A('OBC')}$ の大きさは何度か，求めなさい。"
        st = [f"∠BOC は弧 BC に対する中心角なので，$2\\times{a}^\\circ={2 * a}^\\circ$。", "OB$=$OC より △OBC は二等辺三角形。",
              f"${A('OBC')}=(180^\\circ-{2 * a}^\\circ)\\div2={v}^\\circ$。"]
        expr = f"(180-2*{a})/2"
        fig = cfig({"A": 90, "B": -90 - a, "C": -90 + a}, segs=[("A", "B"), ("A", "C"), ("B", "C"), ("O", "B"), ("O", "C")], center=True, alt="円 O と △ABC")
    else:
        a, b = r.sample(range(20, 61), 2)
        v = a + b
        stem = (f"右の図のように，円周上に4点 A，B，C，D があり，弦 AC と弦 BD の交点を E とする。${A('ACD')}={a}^\\circ$，${A('BAC')}={b}^\\circ$ のとき，"
                f"${A('BEC')}$ の大きさは何度か，求めなさい。")
        st = [f"∠ABD と ∠ACD は弧 AD に対する円周角なので ∠ABE$={a}^\\circ$。", f"∠BEC は △ABE の外角なので，∠BAE$+$∠ABE$={b}^\\circ+{a}^\\circ={v}^\\circ$。"]
        expr = f"{a}+{b}"
        fig = cfig({"A": 150, "B": 215, "C": -30, "D": 70}, segs=[("A", "B"), ("C", "D"), ("A", "C"), ("B", "D")],
                   extra={"E": inter(on(150), on(-30), on(215), on(70))}, off={"E": (0.0, -0.4)}, alt="円周上の4点と弦")
    return MARK(stem, v, st[-1], expr, d=3, p=4, fig=fig,
                ap="中心 O があれば半径でできる二等辺三角形を，弦が交わっていれば同じ弧に対する円周角を探す。円周角と中心角の関係，三角形の外角を組み合わせる。",
                steps=st,
                alt=["わかった角をすべて図にかきこみ，三角形ごとに内角の和が $180^\\circ$ になっているかで確かめる。"],
                pc=[("円周角・中心角・二等辺三角形の性質を正しく使っている", 2), ("正しい大きさを求めている", 2)],
                pit=["中心角と円周角の関係を逆にする。", "同じ弧に対する円周角の組を取り違える。"])


@gen("standard_practice", 4, ["computation", "cross_unit"], rel=["JH-MATH-G1-U05"])
def b_tangent(r):
    t = r.choice(range(30, 151, 2))
    th = (180 - t) / 2
    d = R0 / math.cos(math.radians(th))
    pts_extra = {"P": (d, 0.0)}
    kind = r.choice(["aob", "acb", "pab", "back"])
    fig = cfig({"A": th, "B": -th, "C": 180}, segs=[("P", "A"), ("P", "B"), ("O", "A"), ("O", "B"), ("A", "C"), ("B", "C")], center=True,
               extra=pts_extra, alt="円外の点 P からひいた2本の接線", right=[("O", "A", "P"), ("O", "B", "P")], off={"P": (0.3, 0)})
    head = "右の図のように，円 O の外部の点 P から円 O に2本の接線をひき，接点をそれぞれ A，B とする。点 C は弧 AB のうち長い方の上の点である。"
    if kind == "aob":
        v = 180 - t
        stem = head + f"${A('APB')}={t}^\\circ$ のとき，${A('AOB')}$ の大きさは何度か，求めなさい。"
        st = ["接線は接点を通る半径に垂直なので，∠OAP$=$∠OBP$=90^\\circ$。", f"四角形 OAPB の内角の和は $360^\\circ$ より，∠AOB$=360^\\circ-90^\\circ\\times2-{t}^\\circ={v}^\\circ$。"]
        expr = f"360-180-{t}"
    elif kind == "acb":
        v = Fr(180 - t, 2)
        stem = head + f"${A('APB')}={t}^\\circ$ のとき，${A('ACB')}$ の大きさは何度か，求めなさい。"
        st = ["∠OAP$=$∠OBP$=90^\\circ$ より，∠AOB$=" + f"{180 - t}^\\circ$。", f"∠ACB は弧 AB に対する円周角なので ${ftex(v)}^\\circ$。"]
        expr = f"Rational(180-{t},2)"
    elif kind == "pab":
        v = Fr(180 - t, 2)
        stem = head + f"${A('APB')}={t}^\\circ$ のとき，${A('PAB')}$ の大きさは何度か，求めなさい。"
        st = ["円外の点からひいた2本の接線の長さは等しいので PA$=$PB。", f"△PAB は二等辺三角形で，∠PAB$=(180^\\circ-{t}^\\circ)\\div2={ftex(v)}^\\circ$。"]
        expr = f"Rational(180-{t},2)"
    else:
        c = Fr(180 - t, 2)
        if c.denominator != 1:
            raise AssertionError
        v = t
        stem = head + f"${A('ACB')}={c}^\\circ$ のとき，${A('APB')}$ の大きさは何度か，求めなさい。"
        st = [f"∠AOB は弧 AB に対する中心角なので，$2\\times{c}^\\circ={2 * c}^\\circ$。", f"四角形 OAPB で ∠APB$=360^\\circ-90^\\circ\\times2-{2 * c}^\\circ={v}^\\circ$。"]
        expr = f"180-2*{c}"
    return MARK(stem, v, st[-1], expr, d=3, p=4, fig=fig,
                ap="接線は接点を通る半径に垂直（1年の平面図形とのつながり）。四角形 OAPB の内角の和 $360^\\circ$ と，円周角の定理を組み合わせる。",
                steps=st,
                alt=["PA$=$PB の二等辺三角形 PAB と，OA$=$OB の二等辺三角形 OAB の角を順に求めても同じ結果になる。"],
                pc=[("接線と半径が垂直であることを使っている", 2), ("正しい大きさを求めている", 2)],
                pit=["接線と半径の角を直角にしない。", "∠AOB と ∠APB を等しいと考える。"])


def _secant_pts(phi1, phi2, d=4.2):
    """円外の点 P(d,0) から角度 phi1, phi2（度）の方向にひいた直線と円の交点（近い方 A,C、遠い方 B,D）。"""
    out = {"P": (d, 0.0)}
    for (n1, n2), ph in ((("A", "B"), phi1), (("C", "D"), phi2)):
        ux, uy = -math.cos(math.radians(ph)), math.sin(math.radians(ph))
        bq = d * ux
        cq = d * d - R0 * R0
        disc = math.sqrt(max(bq * bq - cq, 0.0))
        t1, t2 = -bq - disc, -bq + disc
        out[n1] = (d + ux * t1, uy * t1)
        out[n2] = (d + ux * t2, uy * t2)
    return out


@gen("standard_practice", 4, ["computation", "application"])
def b_chords(r):
    kind = r.choice(["inside", "inside", "outside"])
    if kind == "inside":
        a, b, c = r.randint(2, 12), r.randint(2, 12), r.randint(2, 12)
        if c in (a, b):
            raise AssertionError
        v = Fr(a * b, c)
        ask = r.choice(["PD", "CD"])
        if ask == "CD":
            v = v + c
        stem = f"右の図のように，円の2つの弦 AB，CD が点 P で交わっている。PA$={a}$ cm，PB$={b}$ cm，PC$={c}$ cm のとき，{'線分 PD' if ask == 'PD' else '弦 CD'} の長さは何 cm か，求めなさい。"
        st = ["△PAC と △PDB で，弧 BC に対する円周角より ∠PAC$=$∠PDB，対頂角より ∠APC$=$∠DPB。よって △PAC∽△PDB。",
              f"PA：PD$=$PC：PB より ${a}\\times{b}={c}\\times$PD，PD$={ftex(Fr(a * b, c))}$ cm。"]
        if ask == "CD":
            st.append(f"CD$=$PC$+$PD$={c}+{ftex(Fr(a * b, c))}={ftex(v)}$ cm。")
        expr = f"Rational({a}*{b},{c})" + (f"+{c}" if ask == "CD" else "")
        fig = cfig({"A": 160, "B": -20, "C": 80, "D": 230}, segs=[("A", "B"), ("C", "D"), ("A", "C"), ("D", "B")],
                   extra={"P": inter(on(160), on(-20), on(80), on(230))}, off={"P": (0.3, -0.3)}, alt="交わる2つの弦")
    else:
        a, s, c = r.randint(2, 9), r.randint(2, 12), r.randint(2, 9)
        pd = Fr(a * (a + s), c)
        if pd <= c or c == a:
            raise AssertionError
        v = pd - c
        stem = (f"右の図のように，円の外部の点 P を通る2本の直線が，円とそれぞれ点 A，B および点 C，D で交わっている（P に近い方を A，C とする）。"
                f"PA$={a}$ cm，AB$={s}$ cm，PC$={c}$ cm のとき，線分 CD の長さは何 cm か，求めなさい。")
        st = ["△PAD と △PCB で，∠P は共通，弧 AC に対する円周角より ∠PDA$=$∠PBC。よって △PAD∽△PCB。",
              f"PA：PC$=$PD：PB より PA$\\times$PB$=$PC$\\times$PD，${a}\\times{a + s}={c}\\times$PD，PD$={ftex(pd)}$ cm。",
              f"CD$=$PD$-$PC$={ftex(pd)}-{c}={ftex(v)}$ cm。"]
        expr = f"Rational({a}*({a}+{s}),{c})-{c}"
        Q = _secant_pts(16, -14)
        fig = cfig({}, segs=[("P", "B"), ("P", "D"), ("A", "D"), ("C", "B")], extra=Q, off={"P": (0.3, 0)}, alt="円の外部の点 P を通る2本の直線")
    return MARK(stem, v, st[-1], expr, d=3, p=4, fig=fig,
                ap="円周角の定理を根拠に，相似な三角形の組を見つける（円と相似）。対応する辺の比から長さを求める。",
                steps=st,
                alt=["相似から得られる「PA$\\times$PB$=$PC$\\times$PD」の形にして計算してもよい（高校で学ぶ方べきの定理）。"],
                pc=[("相似な三角形と対応する辺を正しく見つけている", 2), ("正しい長さを求めている", 2)],
                pit=["対応する辺を取り違えて PA：PC$=$PB：PD とする。", "外部の点の場合に PB を AB と取り違える。"])


CPROOFS = [
    dict(kind="chords", setup="右の図のように，円の2つの弦 AB，CD が点 P で交わっている。このとき，△PAC∽△PDB であることを次のように証明した。",
         body=["△PAC と △PDB において，", "（a）は等しいから　${PAC}={PDB}$　……①", "対頂角は等しいから　${APC}={DPB}$　……②", "①，②から，（b）ので，△PAC∽△PDB"],
         a="弧 BC に対する円周角"),
    dict(kind="secant", setup="右の図のように，円の外部の点 P を通る2本の直線が，円とそれぞれ点 A，B および点 C，D で交わっている（P に近い方を A，C とする）。このとき，△PAD∽△PCB であることを次のように証明した。",
         body=["△PAD と △PCB において，", "∠P は共通　……①", "（a）は等しいから　${PDA}={PBC}$　……②", "①，②から，（b）ので，△PAD∽△PCB"],
         a="弧 AC に対する円周角"),
    dict(kind="diam", setup="右の図のように，線分 AB を直径とする円の周上に点 C をとり，C から AB に垂線 CH をひく。このとき，△ABC∽△ACH であることを次のように証明した。",
         body=["△ABC と △ACH において，", "（a）は $90^\\circ$ だから，仮定とあわせて　${ACB}={AHC}=90^\\circ$　……①", "∠A は共通　……②", "①，②から，（b）ので，△ABC∽△ACH"],
         a="半円の弧に対する円周角"),
    dict(kind="bisect", setup="右の図のように，円に内接する △ABC で，∠A の二等分線と辺 BC，円との交点をそれぞれ E，D とする。このとき，△ABE∽△ADC であることを次のように証明した。",
         body=["△ABE と △ADC において，", "仮定から　${BAE}={DAC}$　……①", "（a）は等しいから　${ABE}={ADC}$　……②", "①，②から，（b）ので，△ABE∽△ADC"],
         a="弧 AC に対する円周角"),
    dict(kind="quad", setup="右の図のように，円周上に4点 A，B，C，D があり，弦 AC と弦 BD の交点を E とする。このとき，△ABE∽△DCE であることを次のように証明した。",
         body=["△ABE と △DCE において，", "（a）は等しいから　${BAE}={CDE}$　……①", "対頂角は等しいから　${AEB}={DEC}$　……②", "①，②から，（b）ので，△ABE∽△DCE"],
         a="弧 BC に対する円周角"),
]
CREASONS = ["弧 AB に対する円周角", "弧 AC に対する円周角", "弧 BC に対する円周角", "弧 AD に対する円周角", "弧 BD に対する円周角", "半円の弧に対する円周角", "錯角", "同位角", "対頂角"]
SCONDS = ["3組の辺の比がすべて等しい", "2組の辺の比とその間の角がそれぞれ等しい", "2組の角がそれぞれ等しい"]


def _cproof_fig(kind, L):
    if kind == "chords":
        P = {n: on(a) for n, a in {"A": 160, "B": -20, "C": 80, "D": 230}.items()}
        P["P"] = inter(P["A"], P["B"], P["C"], P["D"])
        segs, off = [("A", "B"), ("C", "D"), ("A", "C"), ("D", "B")], {"P": (0.3, -0.3)}
    elif kind == "secant":
        P = _secant_pts(16, -14)
        segs, off = [("P", "B"), ("P", "D"), ("A", "D"), ("C", "B")], {"P": (0.3, 0)}
    elif kind == "diam":
        P = {"A": on(180), "B": on(0), "C": on(125)}
        P["H"] = (P["C"][0], 0.0)
        segs, off = [("A", "B"), ("A", "C"), ("B", "C"), ("C", "H")], {"H": (0, -0.4)}
    elif kind == "bisect":
        P = {"A": on(115), "B": on(205), "C": on(-25)}
        P["D"] = on((205 + 335) / 2)
        P["E"] = inter(P["A"], P["D"], P["B"], P["C"])
        segs, off = [("A", "B"), ("B", "C"), ("C", "A"), ("A", "D"), ("D", "C")], {"E": (0.32, 0.25)}
    else:
        P = {n: on(a) for n, a in {"A": 150, "B": 215, "C": -30, "D": 70}.items()}
        P["E"] = inter(P["A"], P["C"], P["B"], P["D"])
        segs, off = [("A", "B"), ("C", "D"), ("A", "C"), ("B", "D")], {"E": (0.0, -0.4)}
    pts = {L(k): v for k, v in P.items()}
    return figure("証明の図", geo(pts, segs=[(L(a), L(b)) for a, b in segs], off={L(k): v for k, v in off.items()}, circles=[(0.0, 0.0, R0)], scale=30))


@gen("standard_practice", 4, ["written_reasoning", "concept"])
def b_proof_fill(r):
    P = r.choice(CPROOFS)
    mp = r.choice([{}, {}, {"A": "Q", "B": "R", "C": "S", "D": "T", "E": "U", "H": "K"}])

    def L(t):
        return re.sub(r"(?<![a-z\\])[A-EHP](?![a-z])", lambda m: mp.get(m.group(0), m.group(0)), t) if mp else t

    def fmt(t):
        return L(re.sub(r"\{([A-Z]{1,3})\}", lambda m: A(m.group(1)), t))
    pa, pb = L(P["a"]), "2組の角がそれぞれ等しい"
    wa = [L(x) for x in CREASONS if x != P["a"]]
    wb = [x for x in SCONDS if x != pb]
    r.shuffle(wa)

    def C(a, b):
        return f"（a）{a}　（b）{b}"
    cands = [(C(wa[0], pb), f"（a）は{pa}である。等しいとしている2つの角が，どの弧の両端を見こんでいるかを確かめる。", "根拠の取り違え"),
             (C(pa, wb[0]), f"①，②でそろったのは2組の角であり，「{pb}」が正しい。", "相似条件の取り違え"),
             (C(wa[1], wb[1]), f"（a）は{pa}，（b）は「{pb}」である。", "根拠と相似条件の取り違え"),
             (C(wa[2], pb), f"（a）は{pa}である。", "根拠の取り違え")]
    body = "\n".join(fmt(x) for x in P["body"])
    return MC(fmt(P["setup"]) + f"\n〔証明〕\n{body}\n上の証明の（a），（b）にあてはまるものの組み合わせとして最も適するものを，" + SEL4,
              C(pa, pb), cands, f"（a）は{pa}，（b）は「{pb}」。", d=3, p=4, fig=_cproof_fig(P["kind"], L),
              ap="（a）は，等しいとしている2つの角の頂点を除いた2点（見こんでいる弧の両端）を読み取り，「弧 ○○ に対する円周角」と表す。（b）は①，②でそろったものから決める。",
              steps=[f"（a）：{pa}。", "①，②はどちらも角が等しいことを示している。", f"よって（b）は「{pb}」。"],
              alt=["等しい角に同じ印をつけ，その2つの角が同じ弧の両端を見こんでいるかを図で確かめる。"],
              pc=[("（a）の根拠を正しく選んでいる", 2), ("（b）の相似条件を正しく選んでいる", 2)],
              pit=["円周角が見こむ弧を取り違える。", "対頂角や錯角と円周角を混同する。"])


@gen("standard_practice", 4, ["application", "condition_check"])
def b_converse_angle(r):
    x = r.randint(25, 60)
    w = r.randint(x + 20, min(120, 175 - x))
    z = r.randint(15, w - 10)
    kind = r.choice(["cad", "adb"])
    fig = figure("四角形 ABCD と対角線", geo({"A": (0.4, 2.6), "B": (-0.4, 0.0), "C": (4.6, 0.0), "D": (3.6, 2.9)},
                                             segs=[("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("A", "C"), ("B", "D")]))
    if kind == "cad":
        v = w - z
        stem = (f"右の図の四角形 ABCD で，${A('BAC')}={A('BDC')}={x}^\\circ$，${A('ABC')}={w}^\\circ$，${A('ABD')}={z}^\\circ$ である。"
                f"このとき，${A('CAD')}$ の大きさは何度か，求めなさい。")
        st = ["2点 A，D は直線 BC について同じ側にあり，∠BAC$=$∠BDC なので，円周角の定理の逆より 4点 A，B，C，D は1つの円周上にある。",
              f"∠DBC$=" + f"{w}^\\circ-{z}^\\circ={v}^\\circ$。", f"∠CAD と ∠CBD は弧 CD に対する円周角なので，∠CAD$={v}^\\circ$。"]
        expr = f"{w}-{z}"
    else:
        y = r.randint(30, 150 - x)
        v = y
        stem = (f"右の図の四角形 ABCD で，${A('BAC')}={A('BDC')}={x}^\\circ$，${A('ACB')}={y}^\\circ$ である。"
                f"このとき，${A('ADB')}$ の大きさは何度か，求めなさい。")
        st = ["2点 A，D は直線 BC について同じ側にあり，∠BAC$=$∠BDC なので，4点 A，B，C，D は1つの円周上にある。",
              f"∠ADB と ∠ACB は弧 AB に対する円周角なので，∠ADB$={y}^\\circ$。"]
        expr = f"{y}"
    return MARK(stem, v, st[-1], expr, d=3, p=4, fig=fig,
                ap="円がかかれていなくても，等しい角の組から円周角の定理の逆で「4点が1つの円周上にある」ことを見つければ，円周角の定理が使える。",
                steps=st,
                alt=["4点を通る円を実際にかき入れて，どの角がどの弧に対する円周角かを確かめる。"],
                pc=[("円周角の定理の逆で4点が同じ円周上にあることを示している", 2), ("正しい大きさを求めている", 2)],
                pit=["円がないので円周角の定理が使えないと考える。", "見こむ弧を取り違える。"])


# ======================================================================
# C 思考力・記述応用
# ======================================================================

def _xy_pool(r):
    return [
        ("1つの弧に対する円周角の大きさは，その弧に対する中心角の大きさの半分である。", True, "円周角の定理である。"),
        ("1つの弧に対する円周角の大きさは，その弧に対する中心角の大きさの2倍である。", False, "円周角は中心角の半分である。"),
        ("同じ弧に対する円周角の大きさは，円周上の点の位置によらず等しい。", True, "円周角の定理から，同じ弧に対する円周角は一定である。"),
        ("半円の弧に対する円周角は $90^\\circ$ である。", True, "中心角が $180^\\circ$ なので，円周角はその半分の $90^\\circ$ である。"),
        ("1つの円で，長さの等しい弧に対する円周角は等しい。", True, "長さの等しい弧に対する中心角は等しいので，円周角も等しい。"),
        ("1つの円で，円周角の大きさは弧の長さに反比例する。", False, "円周角の大きさは弧の長さに比例する。"),
        ("2点 P，Q が直線 AB について同じ側にあり，∠APB$=$∠AQB ならば，4点 A，B，P，Q は1つの円周上にある。", True, "円周角の定理の逆である。"),
        ("2点 P，Q が直線 AB について反対側にあり，∠APB$=$∠AQB ならば，4点 A，B，P，Q は必ず1つの円周上にある。", False, "円周角の定理の逆は，2点が同じ側にあるときに成り立つ。反対側では成り立たない例がある。"),
        ("円の接線は，接点を通る半径に垂直である。", True, "1年で学んだ円の接線の性質である。"),
        ("円の外部の1点からその円にひいた2本の接線の長さは等しい。", True, "2つの直角三角形の合同（斜辺と他の1辺）から示せる。"),
        ("円周角が $90^\\circ$ になる弦は，その円の直径である。", True, "円周角が $90^\\circ$ なら中心角は $180^\\circ$ なので，弦は直径である。"),
        ("中心角が $180^\\circ$ より大きい弧に対する円周角は存在しない。", False, "中心角が $180^\\circ$ より大きくても，円周角はその半分として決まる（$90^\\circ$ より大きい角になる）。"),
        ("円周角の大きさは，その円の半径が大きいほど大きくなる。", False, "円周角は弧に対する中心角だけで決まり，半径の大きさとは関係がない。"),
    ]


@gen("thinking_writing", 4, ["written_reasoning", "condition_check"])
def c_xy(r):
    S = _xy_pool(r)
    tx, ty = r.choice([True, False]), r.choice([True, False])
    x = r.choice([s for s in S if s[1] == tx])
    y = r.choice([s for s in S if s[1] == ty and s is not x])
    XY = ["X：正　Y：正", "X：正　Y：誤", "X：誤　Y：正", "X：誤　Y：誤"]
    ans = XY[(0 if tx else 2) + (0 if ty else 1)]
    why = {}
    for c in XY:
        if c == ans:
            continue
        cx, cy = c.startswith("X：正"), c.endswith("Y：正")
        rs = []
        if cx != tx:
            rs.append(f"X は{'正しい' if tx else '誤り'}。{x[2]}")
        if cy != ty:
            rs.append(f"Y は{'正しい' if ty else '誤り'}。{y[2]}")
        why[c] = (" ".join(rs), "円の性質の思いこみ")
    return mc("円の性質について述べた次の X，Y の文の正誤の組み合わせとして最も適するものを，" + SEL4 + f"\nX　{x[0]}\nY　{y[0]}",
              [ans] + [c for c in XY if c != ans], f"X：{x[2]}　Y：{y[2]}", d=4, p=8, why=why,
              ap="円周角の定理・その逆・接線の性質と照らし合わせる。「必ず」「いつでも」と書かれた文は，成り立たない図（反例）がないかを考える。",
              steps=[f"X：{x[2]}", f"Y：{y[2]}", f"よって {ans}。"],
              alt=["実際に円をかき，条件に合う点をとって確かめる。"],
              pc=[("X の正誤を根拠をもって判断している", 4), ("Y の正誤を根拠をもって判断している", 4)],
              pit=["円周角の定理の逆の「同じ側」の条件を見落とす。", "円周角と中心角の関係を逆に覚えている。"])


@gen("thinking_writing", 3, ["cross_unit", "application"], rel=["JH-MATH-G3-U05"])
def c_circle_sim(r):
    kind = r.choice(["ad", "ah", "radius"])
    P = {"A": on(110), "B": on(205), "C": on(-20)}
    P["D"] = on(-70)
    bx, by = P["B"]
    cx, cy = P["C"]
    ax, ay = P["A"]
    ux, uy = cx - bx, cy - by
    t = ((ax - bx) * ux + (ay - by) * uy) / (ux * ux + uy * uy)
    P["H"] = (bx + t * ux, by + t * uy)
    P["D"] = (-ax, -ay)
    P["O"] = (0.0, 0.0)
    fig = figure("円に内接する △ABC，垂線 AH，直径 AD", geo(P, segs=[("A", "B"), ("B", "C"), ("C", "A"), ("A", "H"), ("A", "D"), ("D", "C")],
                                                        off={"H": (0.05, -0.38), "O": (0.25, 0.1)}, circles=[(0.0, 0.0, R0)], scale=30, right=[("A", "H", "C")]))
    head = "右の図のように，円 O に内接する △ABC があり，頂点 A から辺 BC に垂線 AH をひく。また，線分 AD は円 O の直径である。"
    ap = "直径 AD に対する円周角 ∠ACD$=90^\\circ$ と，弧 AC に対する円周角 ∠ABH$=$∠ADC から，△ABH∽△ADC（相似の単元との融合）。対応する辺から AB：AD$=$AH：AC。"
    while True:
        b, c = r.randint(4, 15), r.randint(4, 15)
        h = r.randint(2, min(b, c) - 1)
        if b != c:
            break
    if kind == "ad":
        v = Fr(b * c, h)
        stem = head + f"AB$={b}$ cm，AC$={c}$ cm，AH$={h}$ cm のとき，直径 AD の長さは何 cm か，求めなさい。"
        st = ["△ABH と △ADC で，∠AHB$=$∠ACD$=90^\\circ$（AD は直径），∠ABH$=$∠ADC（弧 AC に対する円周角）。よって △ABH∽△ADC。",
              "AB：AD$=$AH：AC より AD$=\\dfrac{\\mathrm{AB}\\times\\mathrm{AC}}{\\mathrm{AH}}$。", f"AD$=\\dfrac{{{b}\\times{c}}}{{{h}}}={ftex(v)}$ cm。"]
        expr = f"Rational({b}*{c},{h})"
    elif kind == "radius":
        v = Fr(b * c, 2 * h)
        stem = head + f"AB$={b}$ cm，AC$={c}$ cm，AH$={h}$ cm のとき，円 O の半径は何 cm か，求めなさい。"
        st = ["△ABH∽△ADC（∠AHB$=$∠ACD$=90^\\circ$，弧 AC に対する円周角 ∠ABH$=$∠ADC）。",
              f"AD$=\\dfrac{{{b}\\times{c}}}{{{h}}}={ftex(Fr(b * c, h))}$ cm。", f"半径は AD の半分で ${ftex(v)}$ cm。"]
        expr = f"Rational({b}*{c},2*{h})"
    else:
        d = max(b, c) + r.randint(1, 8)
        v = Fr(b * c, d)
        stem = head + f"AB$={b}$ cm，AC$={c}$ cm，AD$={d}$ cm のとき，線分 AH の長さは何 cm か，求めなさい。"
        st = ["△ABH∽△ADC（∠AHB$=$∠ACD$=90^\\circ$，弧 AC に対する円周角 ∠ABH$=$∠ADC）。",
              "AB：AD$=$AH：AC より AH$=\\dfrac{\\mathrm{AB}\\times\\mathrm{AC}}{\\mathrm{AD}}$。", f"AH$=\\dfrac{{{b}\\times{c}}}{{{d}}}={ftex(v)}$ cm。"]
        expr = f"Rational({b}*{c},{d})"
    return MARK(stem, v, st[-1], expr, d=4, p=8, fig=fig, ap=ap, steps=st,
                alt=["∠ABC と ∠ADC が同じ弧 AC に対する円周角であることを，C を通る別の点で確かめると対応がはっきりする。三平方の定理を学んだあとなら，数値の妥当性を確かめることもできる。"],
                pc=[("直径に対する円周角が直角であることを使っている", 3), ("相似な三角形と対応する辺を正しく見つけている", 3), ("正しい長さ", 2)],
                pit=["対応する辺を取り違えて AB：AC$=$AH：AD とする。", "直径と半径を取り違える。"])


@gen("thinking_writing", 3, ["application", "multiple_solutions"])
def c_angle_complex(r):
    x = r.randint(20, 60)
    y = r.randint(15, 70)
    if abs(x - y) < 5:
        raise AssertionError
    v = 90 - x + y
    kind = r.choice(["aec", "aed"])
    if kind == "aed":
        v = 180 - v
    if not (10 < v < 170):
        raise AssertionError
    P = {"A": on(180), "B": on(0), "C": on(2 * x), "D": on(-2 * y)}
    P["E"] = inter(P["A"], P["B"], P["C"], P["D"])
    P["O"] = (0.0, 0.0)
    fig = figure("直径 AB と弦 CD", geo(P, segs=[("A", "B"), ("C", "D"), ("A", "C"), ("B", "C"), ("A", "D")], circles=[(0.0, 0.0, R0)], scale=30,
                                         off={"E": (0.25, 0.3), "O": (0.0, -0.35)}))
    tgt = "AEC" if kind == "aec" else "AED"
    stem = (f"右の図のように，線分 AB を直径とする円 O の周上に，直線 AB について反対側に2点 C，D がある。弦 CD と直径 AB の交点を E とする。"
            f"${A('CAB')}={x}^\\circ$，${A('DAB')}={y}^\\circ$ のとき，${A(tgt)}$ の大きさは何度か，求めなさい。")
    st = ["AB は直径なので ∠ACB$=90^\\circ$，∠ABC$=" + f"90^\\circ-{x}^\\circ={90 - x}^\\circ$。",
          f"∠ADC と ∠ABC は弧 AC に対する円周角なので，∠ADE$={90 - x}^\\circ$。",
          f"△AED で ∠AED$=180^\\circ-{y}^\\circ-{90 - x}^\\circ={90 + x - y}^\\circ$。"]
    if kind == "aec":
        st.append(f"∠AEC$=180^\\circ-{90 + x - y}^\\circ={v}^\\circ$。")
        expr = f"180-(180-{y}-(90-{x}))"
    else:
        expr = f"180-{y}-(90-{x})"
    return MARK(stem, v, st[-1], expr, d=4, p=8, fig=fig,
                ap="直径に対する円周角（$90^\\circ$），同じ弧に対する円周角，三角形の内角・外角を順につなげる。どの三角形に注目するかで解き方がいくつかある。",
                steps=st,
                alt=[f"∠ACD は弧 AD に対する円周角で ∠ABD と等しく，∠ABD$=90^\\circ-{y}^\\circ$。△ACE で ∠AEC$=180^\\circ-{x}^\\circ-(90^\\circ-{y}^\\circ)$ と求めてもよい。"],
                pc=[("直径に対する円周角を使っている", 3), ("同じ弧に対する円周角を正しく使っている", 3), ("正しい大きさ", 2)],
                pit=["∠ADC を弧 AD に対する円周角と取り違える。", "直径に対する円周角を見落とす。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def _err_mc(stem, sol, right, cands, e, err, **kw):
    return MC(f"{stem}\n〔Kさんの解答〕\n{sol}\nKさんの解答の誤りを説明したものとして最も適するものを，" + SEL4, right, cands, e, err=err, **kw)


@gen("error_correction", 4, ["common_error", "computation"])
def d_inscribed_err(r):
    kind = r.choice(["double", "minor", "oab"])
    if kind == "double":
        x = r.choice(range(40, 171, 2))
        good = x // 2
        stem = f"〔問題〕円 O の周上に3点 A，B，C があり，${A('AOB')}={x}^\\circ$ である。点 C が弧 AB のうち長い方の上にあるとき，${A('ACB')}$ の大きさを求めなさい。"
        sol = f"円周角は中心角の2倍なので，${A('ACB')}=2\\times{x}^\\circ={2 * x}^\\circ$"
        right = "円周角は中心角の半分である。2倍と半分の関係を逆にしている。"
        fix = f"${A('ACB')}=\\dfrac{{1}}{{2}}\\times{x}^\\circ={good}^\\circ$"
        etype, tempt = "formula", "中心角と円周角のどちらが大きいかをあいまいに覚えているため。"
        cands = [("C が長い方の弧の上にあるので，$360^\\circ$ から引かなければならない。", "C が長い方の弧の上にあるとき，∠ACB は短い方の弧 AB に対する円周角で，そのまま半分にすればよい。", "場合分けの誤解"),
                 ("Kさんの解答に誤りはない。", f"三角形の内角は $180^\\circ$ より小さいので，${2 * x}^\\circ$ にはならない。", "検算不足"),
                 ("∠ACB は ∠AOB と等しい。", "円周角と中心角は等しくない。円周角は中心角の半分である。", "円周角と中心角の混同"),
                 ("△OAC が正三角形であることを使っていない。", "△OAC は二等辺三角形だが，正三角形とは限らない。", "根拠のない仮定")]
        chk = (f"{x}/2", str(good))
    elif kind == "minor":
        x = r.choice(range(60, 171, 2))
        good = 180 - x // 2
        stem = f"〔問題〕円 O の周上に3点 A，B，C があり，${A('AOB')}={x}^\\circ$ である。点 C が弧 AB のうち短い方の上にあるとき，${A('ACB')}$ の大きさを求めなさい。"
        sol = f"円周角は中心角の半分なので，${A('ACB')}=\\dfrac{{1}}{{2}}\\times{x}^\\circ={x // 2}^\\circ$"
        right = f"C が短い方の弧の上にあるので，∠ACB は長い方の弧 AB に対する円周角である。その中心角は $360^\\circ-{x}^\\circ$ である。"
        fix = f"${A('ACB')}=\\dfrac{{1}}{{2}}\\times(360^\\circ-{x}^\\circ)={good}^\\circ$"
        etype, tempt = "condition", "C の位置を確かめずに，図にかかれた中心角をそのまま使ってしまう。"
        cands = [("円周角は中心角の2倍なので，$2\\times" + f"{x}^\\circ$ とするべきである。", "円周角は中心角の半分であり，2倍ではない。", "円周角と中心角の関係の誤解"),
                 ("Kさんの解答に誤りはない。", "C が短い方の弧の上にあるときは，∠ACB は長い方の弧に対する円周角になる。", "場合分けの見落とし"),
                 ("∠ACB は $90^\\circ$ と決まっている。", "AB が直径のときだけ $90^\\circ$ になる。", "直径の場合との混同"),
                 (f"$180^\\circ-{x}^\\circ$ が答えである。", "長い方の弧に対する中心角の半分を求める必要があり，この式はその値にならない。", "計算方法の誤解")]
        chk = (f"(360-{x})/2", str(good))
    else:
        t = r.randint(15, 75)
        good = 90 - t
        stem = f"〔問題〕円 O の周上に3点 A，B，C があり，${A('OAB')}={t}^\\circ$ である。点 C が弧 AB のうち長い方の上にあるとき，${A('ACB')}$ の大きさを求めなさい。"
        sol = f"∠OAB と ∠ACB は弧 OB に対する円周角なので等しい。${A('ACB')}={t}^\\circ$"
        right = "O は円の中心で，円周上の点ではない。∠OAB は円周角ではないので，円周角の定理は使えない。"
        fix = f"∠AOB$=180^\\circ-2\\times{t}^\\circ={180 - 2 * t}^\\circ$，${A('ACB')}={good}^\\circ$"
        etype, tempt = "concept", "図の中で同じ弦をはさむように見える角を，どれも円周角と思いこむため。"
        cands = [(f"∠ACB は ∠OAB の2倍で ${2 * t}^\\circ$ である。", "∠OAB と ∠ACB に2倍の関係はない。", "根拠のない推測"),
                 ("Kさんの解答に誤りはない。", f"OA$=$OB より ∠AOB$={180 - 2 * t}^\\circ$ で，∠ACB はその半分になり ${t}^\\circ$ にはならない（${t}=45$ のときを除く）。", "検算不足"),
                 ("∠ACB は ∠AOB と等しい。", "円周角は中心角の半分である。", "円周角と中心角の混同"),
                 ("△OAB が正三角形なので，∠ACB$=60^\\circ$ である。", "△OAB は二等辺三角形だが，正三角形とは限らない。", "根拠のない仮定")]
        chk = (f"(180-2*{t})/2", str(good))
        if t == 45:
            raise AssertionError
    r.shuffle(cands)
    return _err_mc(stem, sol, right, cands, f"正しくは {fix}。", dict(sol=sol, step="円周角を求める部分", type=etype, tempt=tempt, fix=fix), d=3, p=6,
                   ap="円周角の定理を使う前に，① その角の頂点が円周上にあるか，② どちらの弧に対する円周角か，③ 中心角との関係（半分）を確かめる。",
                   steps=["Kさんが使った性質を確認する。", "円周角の定理の使い方として正しいかを判断する。", f"正しくは {fix}。"],
                   alt=["求めた角を図にかきこみ，三角形の内角の和などで矛盾がないか確かめる。"],
                   pc=[("誤りの原因を正しく指摘している", 3), ("正しい大きさを求めている", 3)],
                   pit=["中心が頂点の角を円周角とみなす。", "C の位置による場合分けを忘れる。"],
                   chk=chk + (None, "intermediate"))


@gen("error_correction", 3, ["common_error", "computation"])
def d_lines_err(r):
    x = r.randint(20, 70)
    good = 90 - x
    where = r.choice([0, 1, 2])
    l1 = "AB は直径なので，∠ACB$=90^\\circ$"
    l2 = f"△ABC で，∠ABC$=180^\\circ-90^\\circ-{x}^\\circ={90 - x}^\\circ$"
    l3 = "∠ADC と ∠ABC は弧 AC に対する円周角なので，∠ADC$=$∠ABC" + f"$={90 - x}^\\circ$"
    ans = good
    if where == 0:
        l1 = "AB は直径なので，∠ACB$=180^\\circ$"
        l2 = f"△ABC で，∠ABC$=180^\\circ-{x}^\\circ={180 - x}^\\circ$"
        l3 = f"∠ADC と ∠ABC は弧 AC に対する円周角なので，∠ADC$={180 - x}^\\circ$"
        ans = 180 - x
    elif where == 1:
        l2 = f"△ABC で，∠ABC$=90^\\circ+{x}^\\circ={90 + x}^\\circ$"
        l3 = f"∠ADC と ∠ABC は弧 AC に対する円周角なので，∠ADC$={90 + x}^\\circ$"
        ans = 90 + x
    elif where == 2:
        l3 = f"∠ADC は弧 AC に対する円周角，∠ABC は中心角なので，∠ADC$=\\dfrac{{1}}{{2}}$∠ABC$={ftex(Fr(90 - x, 2))}^\\circ$"
        ans = Fr(90 - x, 2)
    l4 = f"答え　${ftex(ans)}^\\circ$"
    sol = "\n".join(f"{i + 1}行目　{t}" for i, t in enumerate([l1, l2, l3, l4]))
    LINES4 = ["1行目", "2行目", "3行目", "4行目"]
    ok = {0: "1行目は正しい。半円の弧に対する円周角は $90^\\circ$。", 1: "2行目は三角形の内角の和から正しく求めている。",
          2: "3行目は正しい。∠ADC と ∠ABC は同じ弧 AC に対する円周角。", 3: "4行目は3行目の結果をそのまま答えている。"}
    why = {LINES4[i]: (ok[i], "誤りの箇所の見落とし") for i in range(4) if i != where}
    info = {0: ("1行目（直径に対する円周角を $180^\\circ$ とした）", "concept", "直径（一直線）を見て $180^\\circ$ と思いこみやすい。"),
            1: ("2行目（内角の和の計算で引くべき角を足した）", "calculation", "式を急いで立てると，符号を取り違えやすい。"),
            2: ("3行目（∠ABC を中心角と取り違えた）", "concept", "円周上の点 B を頂点とする角を，中心角と取り違えた。")}[where]
    fix = f"∠ADC$=$∠ABC$={good}^\\circ$"
    P = {"A": on(180), "B": on(0), "C": on(180 - 2 * (90 - x)), "D": on(-120)}
    P["O"] = (0.0, 0.0)
    fig = figure("直径 AB と円周上の点 C，D", geo(P, segs=[("A", "B"), ("A", "C"), ("B", "C"), ("A", "D"), ("D", "C")], circles=[(0.0, 0.0, R0)], scale=30, off={"O": (0.0, -0.35)}))
    return mc(f"〔問題〕右の図のように，線分 AB を直径とする円 O の周上に2点 C，D がある。${A('BAC')}={x}^\\circ$ のとき，${A('ADC')}$ の大きさを求めなさい。\n〔Kさんの解答〕\n{sol}\nKさんの解答で，誤りが最初に生じた行として最も適するものを，" + SEL4,
              LINES4, f"誤りが最初に生じたのは{LINES4[where]}。正しくは {fix}。", d=3, p=6, keep=True, ai=where, why=why, fig=fig,
              err=dict(sol=sol, step=info[0], type=info[1], tempt=info[2], fix=fix),
              ap="1行ずつ，使っている性質（直径に対する円周角，内角の和，同じ弧に対する円周角）が正しいかを自分で確かめる。",
              steps=["AB は直径なので ∠ACB$=90^\\circ$。", f"∠ABC$={90 - x}^\\circ$。", f"∠ADC$=$∠ABC$={good}^\\circ$。"],
              alt=[f"中心 O と C を結ぶと ∠AOC$=2\\times{90 - x}^\\circ$ で，∠ADC はその半分になることからも確かめられる。"],
              pc=[("誤りの行を正しく指摘している", 3), ("正しい大きさを求めている", 3)],
              pit=["直径に対する円周角を $180^\\circ$ とする。", "円周上の点が頂点の角を中心角と考える。"],
              chk=(f"90-{x}", str(good), None, "intermediate"))


@gen("error_correction", 3, ["common_error", "condition_check"])
def d_converse_err(r):
    x = r.randint(25, 70)
    kind = r.choice(["diffseg", "opposite", "unequal"])
    if kind == "diffseg":
        p1, p2 = r.choice(PAIRS_DIFF)
        given = f"${A(p1)}={A(p2)}={x}^\\circ$"
        sol = f"${A(p1)}={A(p2)}$ なので，円周角の定理の逆より，4点 A，B，C，D は1つの円周上にある。"
        right = f"∠{p1} と ∠{p2} は同じ線分を見こむ角ではない。円周角の定理の逆は，同じ線分を同じ側から見こむ角が等しいときに使える。"
        fix = "この条件だけでは，4点が1つの円周上にあるとはいえない"
        tempt = "等しい角が2つあるだけで，円周角の定理の逆が使えると思いこみやすい。"
        stem = f"〔問題〕四角形 ABCD に対角線 AC，BD をひくと，{given} であった。4点 A，B，C，D は1つの円周上にあるといえるか。"
    elif kind == "opposite":
        given = f"点 C と点 D は直線 AB について反対側にあり，${A('ACB')}={A('ADB')}={x}^\\circ$"
        sol = "∠ACB$=$∠ADB なので，円周角の定理の逆より，4点 A，B，C，D は1つの円周上にある。"
        right = "円周角の定理の逆は，C と D が直線 AB について同じ側にあるときに成り立つ。反対側にあるときは使えない。"
        fix = "この条件だけでは，4点が1つの円周上にあるとはいえない"
        tempt = "「同じ側にある」という条件を読み落としやすい。"
        stem = f"〔問題〕4点 A，B，C，D について，{given} である。4点 A，B，C，D は1つの円周上にあるといえるか。"
    else:
        y = x + r.choice([-5, 5, 10])
        given = f"${A('BAC')}={x}^\\circ$，${A('BDC')}={y}^\\circ$"
        sol = "∠BAC と ∠BDC はどちらも線分 BC を見こむ角なので，円周角の定理の逆より，4点 A，B，C，D は1つの円周上にある。"
        right = "同じ線分 BC を見こむ角だが，大きさが等しくない。円周角の定理の逆は，見こむ角が等しいときにしか使えない。"
        fix = "4点は1つの円周上にない"
        tempt = "見こむ線分が同じであることだけに注目して，角の大きさを確かめなかった。"
        stem = f"〔問題〕四角形 ABCD に対角線 AC，BD をひくと，{given} であった。4点 A，B，C，D は1つの円周上にあるといえるか。"
    cands = [("円周角の定理の逆を使うには，4つの角がすべて等しくなければならない。", "等しい角は2つでよい。必要なのは，同じ線分を同じ側から見こむ2つの角が等しいことである。", "条件の誤解"),
             ("Kさんの解答に誤りはない。", "Kさんが使った条件は，円周角の定理の逆の条件を満たしていない。", "条件の確認不足"),
             ("円周角の定理の逆を使うには，中心 O の位置がわかっていなければならない。", "中心の位置がわからなくても，円周角の定理の逆は使える。", "条件の誤解"),
             ("4点が1つの円周上にあるには，四角形 ABCD が長方形でなければならない。", "長方形でなくても，4点が1つの円周上にある四角形はたくさんある。", "特殊な場合との混同")]
    r.shuffle(cands)
    return _err_mc(stem, sol, right, cands, f"正しくは「{fix}」。", dict(sol=sol, step="円周角の定理の逆のあてはめ", type="condition", tempt=tempt, fix=fix), d=3, p=6,
                   ap="円周角の定理の逆の条件「同じ線分を，その線分について同じ側にある2点から見こむ角が等しい」を1つずつ確かめる。",
                   steps=["等しいとされた2つの角が，どの線分を見こむ角かを調べる。", "2つの頂点が，その線分について同じ側にあるかを調べる。", right],
                   alt=["条件を満たすのに4点が同じ円周上にない図（反例）をかけるかを考える。"],
                   pc=[("誤りの理由を正しく指摘している", 3), ("正しい結論を理解している", 3)],
                   pit=["見こむ線分が同じかどうかを確かめない。", "「同じ側」の条件を落とす。"])


GENERATORS = [a_central, a_diameter, a_same_arc, a_arc_ratio, a_converse,
              b_angle_chase, b_tangent, b_chords, b_proof_fill, b_converse_angle,
              c_xy, c_circle_sim, c_angle_complex,
              d_inscribed_err, d_lines_err, d_converse_err]

GENERATORS = [_robust(g) for g in GENERATORS]
