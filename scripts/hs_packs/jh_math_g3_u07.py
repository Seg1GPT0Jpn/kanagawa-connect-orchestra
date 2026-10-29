"""単元パック：中学3年 三平方の定理（神奈川県公立高校入試形式）。"""
import math
import re
import unicodedata
from fractions import Fraction as Fr

from banks._common import figure, mc, num
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem, tp)

UNIT_ID = "JH-MATH-G3-U07"

PREREQUISITES = [
    ("JH-MATH-G3-U02", "平方根の意味と、根号をふくむ数の簡単にし方。三平方の定理の答えの多くは根号で表される。"),
    ("JH-MATH-G3-U05", "相似な直角三角形の辺の比。三平方の定理の相似による証明で使う。"),
    ("JH-MATH-G3-U06", "円の接線と半径の関係、直径に対する円周角。弦や接線の長さを求めるときに使う。"),
    ("JH-MATH-G1-U06", "直方体・角錐・円錐の見取図と展開図。空間図形の中に直角三角形を見つける土台になる。"),
]
EXTENSIONS = [
    ("HS-MATH1-U04", "三角比・余弦定理へ発展する。余弦定理は三平方の定理を一般の三角形に広げたもの。"),
    ("HS-MATH2-U03", "座標平面上の2点間の距離の公式や円の方程式は、三平方の定理がもとになっている。"),
    ("HS-MATHA-U02", "方べきの定理や円と接線の性質を、三平方の定理と組み合わせて活用する。"),
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




def surd(n):
    """√n = c√r（r は平方因数をもたない）となる (c, r)。"""
    c, r_ = 1, n
    k = 2
    while k * k <= r_:
        while r_ % (k * k) == 0:
            r_ //= k * k
            c *= k
        k += 1
    return c, r_


def rform(sq):
    """値の2乗 sq（有理数）から、値 = a√r / q の (a, r, q) を返す。"""
    sq = Fr(sq)
    p, q = sq.numerator, sq.denominator
    c, rad = surd(p * q)
    g = math.gcd(c, q)
    return c // g, rad, q // g


def rtex(sq):
    a, rad, q = rform(sq)
    if rad == 1:
        return ftex(Fr(a, q))
    core = ("" if a == 1 else str(a)) + f"\\sqrt{{{rad}}}"
    return core if q == 1 else f"\\dfrac{{{core}}}{{{q}}}"


def rpy(sq):
    a, rad, q = rform(sq)
    return f"{a}*sqrt({rad})/{q}" if rad != 1 else fpy(Fr(a, q))


def MARKR(stem, sq, e, expr, **kw):
    """答えの2乗 sq を与えて、根号をふくむ数（または整数・分数）をあいう方式で答えさせる。"""
    a, rad, q = rform(sq)
    if rad == 1:
        return MARK(stem, Fr(a, q), e, expr, **kw)
    if q == 1:
        mark = ("root", rad) if a == 1 else ("coef_root", a, rad)
    else:
        mark = ("frac_root", a, rad, q)
    return num(stem, f"${rtex(sq)}$", e, mark=mark, chk=(expr, f"sqrt({fpy(Fr(sq))})", None, "answer"), **kw)


def rtri_fig(a=4.0, b=3.0, labels=("A", "B", "C"), alt="直角三角形", texts=()):
    """直角を B にもつ直角三角形（AB が縦、BC が横）。"""
    s = 3.6 / max(a, b)
    P = {labels[0]: (0.0, a * s), labels[1]: (0.0, 0.0), labels[2]: (b * s, 0.0)}
    return figure(alt, geo(P, segs=[(labels[0], labels[1]), (labels[1], labels[2]), (labels[2], labels[0])], right=[(labels[0], labels[1], labels[2])], texts=texts))


def box_fig(a, b, c, extra_segs=(), extra_dashed=(), extra_pts=None, alt="直方体 ABCD-EFGH"):
    """直方体 ABCD-EFGH（上の面 ABCD、下の面 EFGH、AE が高さ）。a=AB（横）、b=BC（奥行き）、c=AE（高さ）。"""
    m = max(a, b, c)
    a, b, c = 3.6 * a / m, 3.6 * b / m, 3.6 * c / m
    k = 0.5

    def pr(x, y, z):
        return (x + k * y * 0.87, z + k * y * 0.5)
    P = {"E": pr(0, 0, 0), "F": pr(a, 0, 0), "G": pr(a, b, 0), "H": pr(0, b, 0),
         "A": pr(0, 0, c), "B": pr(a, 0, c), "C": pr(a, b, c), "D": pr(0, b, c)}
    if extra_pts:
        P |= {n: pr(*xyz) for n, xyz in extra_pts.items()}
    segs = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("E", "F"), ("F", "G"), ("A", "E"), ("B", "F"), ("C", "G")] + list(extra_segs)
    dashed = [("H", "E"), ("H", "G"), ("H", "D")] + list(extra_dashed)
    off = {"A": (-0.3, 0.0), "B": (0.2, -0.32), "C": (0.3, 0.15), "D": (-0.25, 0.25), "E": (-0.3, -0.15), "F": (0.15, -0.35), "G": (0.32, -0.1), "H": (-0.32, 0.12)}
    return figure(alt, geo(P, segs=segs, dashed=dashed, scale=30, off=off))


def pyr_fig(kind="square", alt="正四角錐"):
    if kind == "square":
        P = {"B": (0.0, 0.0), "C": (3.2, 0.0), "D": (4.4, 1.2), "E": (1.2, 1.2), "A": (2.2, 3.8)}
        P["H"] = (2.2, 0.6)
        return figure(alt, geo(P, segs=[("A", "B"), ("A", "C"), ("A", "D"), ("B", "C"), ("C", "D")], dashed=[("A", "E"), ("E", "B"), ("E", "D"), ("A", "H")],
                               off={"H": (0.3, -0.25)}))
    W, H = 200, 190
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="serif" font-size="12">',
         '<line x1="100" y1="20" x2="30" y2="160" stroke="#000" stroke-width="1.1"/>',
         '<line x1="100" y1="20" x2="170" y2="160" stroke="#000" stroke-width="1.1"/>',
         '<path d="M30,160 A70,16 0 0 0 170,160" fill="none" stroke="#000" stroke-width="1.1"/>',
         '<path d="M30,160 A70,16 0 0 1 170,160" fill="none" stroke="#000" stroke-width="1" stroke-dasharray="4 3"/>',
         '<line x1="100" y1="20" x2="100" y2="160" stroke="#000" stroke-width="0.8" stroke-dasharray="3 3"/>',
         '<line x1="100" y1="160" x2="170" y2="160" stroke="#000" stroke-width="0.8" stroke-dasharray="3 3"/>',
         '<text x="100" y="14" text-anchor="middle">A</text>', '<text x="100" y="176" text-anchor="middle">O</text>', '<text x="180" y="164" text-anchor="middle">B</text>',
         "</svg>"]
    return figure(alt, "".join(o))


# ----------------------------------------------------------------------
# 授業プリント
# ----------------------------------------------------------------------

LESSON = lesson(
    goals=["三平方の定理とその逆を、図形の面積や相似を使って証明し、説明できる。",
           "三平方の定理を使って、平面図形（特別な直角三角形、弦、座標平面上の2点間の距離など）の長さを求められる。",
           "空間図形の中に直角三角形を見つけ、対角線・高さ・最短距離などを求められる。"],
    duration=100,
    readiness=["平方根の意味と、根号をふくむ式の簡単にし方（$\\sqrt{12}=2\\sqrt{3}$ など）を使える。",
               "三角形の相似条件と、相似な図形の対応する辺の比を使える。",
               "円の接線と半径の関係、正三角形・正方形の性質を知っている。",
               "直方体・角錐・円錐の見取図や展開図をかける。"],
    flow=[("導入：直角三角形の3辺の関係", 10, "方眼の上の直角三角形で、各辺を1辺とする正方形の面積を調べる"),
          ("三平方の定理と証明", 20, "面積による証明・相似による証明、定理の逆"),
          ("特別な直角三角形", 15, "$45^\\circ$・$30^\\circ$・$60^\\circ$ の直角三角形の辺の比（例題1）"),
          ("平面図形への利用", 20, "二等辺三角形の高さ、弦の長さ、座標平面上の2点間の距離（例題2）"),
          ("空間図形への利用", 25, "直方体の対角線、角錐・円錐の高さ、展開図と最短距離（例題3）"),
          ("まとめと確認", 10, "確認問題と問題プリントの指示")],
    sections=[
        intro("in1", "直角三角形の3辺の関係",
              "方眼紙に、直角をはさむ2辺が 3 目もりと 4 目もりの直角三角形をかき、3つの辺をそれぞれ1辺とする正方形をかく。正方形の面積は 9、16、25 になり、$9+16=25$ が成り立つ。どんな直角三角形でもこの関係が成り立つのだろうか。",
              bullets=["直角三角形で、直角に対する辺を斜辺という。斜辺はいちばん長い辺である。",
                       "この関係は古代から知られ、ピタゴラスの定理ともよばれる。"],
              points=[tp("いくつかの直角三角形で正方形の面積を数えさせ、「直角をはさむ2辺の正方形の和＝斜辺の正方形」を予想させる。",
                         ask="直角三角形でない三角形でも成り立つか。", expect="成り立たない（鈍角三角形では大きく、鋭角三角形では小さくなる）。", timing="導入")]),
        theorem("th1", "三平方の定理",
                "$$a^2+b^2=c^2$$",
                ["直角三角形の直角をはさむ2辺の長さを $a$、$b$、斜辺の長さを $c$ とすると、$a^2+b^2=c^2$ が成り立つ。",
                 "逆に、3辺の長さが $a$、$b$、$c$ の三角形で $a^2+b^2=c^2$ が成り立てば、その三角形は長さ $c$ の辺を斜辺とする直角三角形である（三平方の定理の逆）。",
                 "辺の長さを求めるときは、どの辺が斜辺かを最初に確かめる。"],
                proof=["【面積による証明】1辺が $a+b$ の正方形の中に、直角をはさむ2辺が $a$、$b$、斜辺が $c$ の直角三角形を4つ、斜辺が内側に正方形をつくるように並べる。",
                       "内側の四角形は4つの辺がすべて $c$ で、4つの角はどれも $180^\\circ-90^\\circ=90^\\circ$（直角三角形の2つの鋭角の和は $90^\\circ$）なので、1辺 $c$ の正方形。",
                       "大きい正方形の面積を2通りに表すと $(a+b)^2=4\\times\\dfrac{1}{2}ab+c^2$。",
                       "左辺を展開して $a^2+2ab+b^2=2ab+c^2$。よって $a^2+b^2=c^2$。"],
                points=[tp("証明の図を実際に紙で切って並べさせると、式変形の意味がつかみやすい。", ask="内側の四角形が正方形であることはどう説明できるか。", expect="4辺が $c$ で、角が $90^\\circ$ になるから。")]),
        derivation("dv1", "相似を使った証明と、特別な直角三角形",
                   ["∠C$=90^\\circ$ の直角三角形 ABC で、C から斜辺 AB に垂線 CH をひく（BC$=a$、CA$=b$、AB$=c$）。",
                    "△ABC∽△ACH（∠A が共通、直角）より AC：AH$=$AB：AC、よって $b^2=c\\times$AH。",
                    "同様に △ABC∽△CBH より $a^2=c\\times$BH。",
                    "たして $a^2+b^2=c\\times($AH$+$BH$)=c\\times c=c^2$。",
                    "直角二等辺三角形（$45^\\circ$、$45^\\circ$、$90^\\circ$）：直角をはさむ辺を $1$ とすると斜辺は $\\sqrt{1^2+1^2}=\\sqrt{2}$。辺の比は $1:1:\\sqrt{2}$。",
                    "正三角形を半分にした直角三角形（$30^\\circ$、$60^\\circ$、$90^\\circ$）：斜辺 $2$、短い辺 $1$ とすると残りは $\\sqrt{2^2-1^2}=\\sqrt{3}$。辺の比は $1:2:\\sqrt{3}$。"],
                   points=[tp("$30^\\circ$・$60^\\circ$ の直角三角形の比は、正三角形を半分にした図から毎回導けるようにし、丸暗記にしない。",
                              caution="「$1:\\sqrt{3}:2$」の順番（短い辺：長い辺：斜辺）を取り違える生徒が多い。図に辺の長さを書きこませる。")]),
        example("ex1", "例題1　特別な直角三角形",
                "1辺が $6$ cm の正三角形の高さと面積を求めなさい。",
                ["頂点から底辺に垂線をひくと、底辺は2等分され、$30^\\circ$・$60^\\circ$・$90^\\circ$ の直角三角形ができる。",
                 "高さを $h$ とすると $h^2+3^2=6^2$、$h^2=27$、$h=3\\sqrt{3}$ cm。",
                 "面積は $\\dfrac{1}{2}\\times6\\times3\\sqrt{3}=9\\sqrt{3}$ cm²。"],
                "高さ $3\\sqrt{3}$ cm、面積 $9\\sqrt{3}$ cm²",
                thinking="正三角形の高さは、底辺の中点に垂線をひいてできる直角三角形で考える。",
                figure=figure("正三角形と高さ", geo({"A": (2.0, 3.46), "B": (0.0, 0.0), "C": (4.0, 0.0), "H": (2.0, 0.0)}, segs=[("A", "B"), ("B", "C"), ("C", "A")],
                                                   dashed=[("A", "H")], right=[("A", "H", "C")], off={"H": (0, -0.4)})),
                points=[tp("比 $1:2:\\sqrt{3}$ を使っても求められることを確認し、2つの方法を比べさせる。")],
                misconceptions=[("$h^2=6^2+3^2$", "斜辺は $6$ cm なので $h^2=6^2-3^2$")]),
        example("ex2", "例題2　座標平面上の2点間の距離",
                "2点 A$(-1,\\,2)$、B$(3,\\,5)$ の間の距離を求めなさい。",
                ["AB を斜辺とし、座標軸に平行な2辺をもつ直角三角形を考える。", "横の長さ $3-(-1)=4$、縦の長さ $5-2=3$。", "AB$=\\sqrt{4^2+3^2}=5$。"],
                "$5$",
                thinking="2点を結ぶ線分を斜辺とする直角三角形を、座標軸に平行な線でつくる。",
                points=[tp("座標の差は「大きい方 − 小さい方」でとれば負にならないこと、2乗するので順番は関係ないことを確認する。")]),
        example("ex3", "例題3　直方体の対角線",
                "縦 $3$ cm、横 $4$ cm、高さ $12$ cm の直方体の対角線の長さを求めなさい。",
                ["底面の対角線の長さは $\\sqrt{3^2+4^2}=5$ cm。", "底面の対角線と高さを2辺とする直角三角形を考えると、対角線は $\\sqrt{5^2+12^2}=13$ cm。",
                 "まとめると、対角線は $\\sqrt{3^2+4^2+12^2}$ で求められる。"],
                "$13$ cm",
                thinking="空間の中から、求める線分を斜辺とする直角三角形を取り出す。",
                figure=box_fig(4, 3, 6, extra_dashed=[("A", "G"), ("E", "G")]),
                points=[tp("見取図から直角三角形 AEG を取り出して平面にかき直させる。どの角が直角かを説明させる。")]),
        board("bd1", "板書案",
              [("① 三平方の定理", ["$a^2+b^2=c^2$（$c$ は斜辺）", "証明：正方形の面積を2通りに", "逆：$a^2+b^2=c^2$ → 直角三角形", "まず斜辺を確認！"]),
               ("② 平面図形", ["$1:1:\\sqrt{2}$（$45^\\circ$）", "$1:2:\\sqrt{3}$（$30^\\circ$・$60^\\circ$）", "弦：$\\left(\\dfrac{\\ell}{2}\\right)^2+d^2=r^2$", "2点間の距離：$\\sqrt{(x の差)^2+(y の差)^2}$"]),
               ("③ 空間図形", ["直方体の対角線 $\\sqrt{a^2+b^2+c^2}$", "正四角錐の高さ：底面の対角線の半分", "円錐の高さ：$\\sqrt{母線^2-半径^2}$", "最短距離 → 展開図で直線"])],
              points=[tp("③では、立体ごとに「取り出す直角三角形」の図を必ず横にかく。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("長さを求める前に「斜辺はどれか」を必ず言わせる。斜辺がわかっていれば、2乗の差、わかっていなければ2乗の和になる。", ask="斜辺と他の1辺がわかっているときはどう計算するか。", expect="斜辺の2乗から他の辺の2乗を引く。"),
               tp("根号の答えは、根号の中をできるだけ小さい自然数にする（入試のマーク方式の約束）。$\\sqrt{72}=6\\sqrt{2}$ のように素因数分解して確かめさせる。"),
               tp("空間図形では、見取図のままでは直角が見えにくい。直角三角形を平面に取り出してかく習慣をつけさせる。", timing="空間図形の導入")],
              misconceptions=[("斜辺と他の1辺がわかっているのに2乗の和をとる", "斜辺の2乗から他の1辺の2乗を引く"),
                              ("$30^\\circ$・$60^\\circ$ の直角三角形の斜辺を $\\sqrt{3}$ とする", "辺の比は 短い辺：斜辺：残りの辺 $=1:2:\\sqrt{3}$"),
                              ("直方体の対角線を $\\sqrt{a^2+b^2}$ とする", "高さもふくめて $\\sqrt{a^2+b^2+c^2}$")]),
        summary("sm1", "まとめ",
                ["直角三角形で、直角をはさむ2辺 $a$、$b$、斜辺 $c$ について $a^2+b^2=c^2$。逆も成り立つ。",
                 "特別な直角三角形の辺の比：$1:1:\\sqrt{2}$、$1:2:\\sqrt{3}$。",
                 "弦の長さ、接線の長さ、2点間の距離は、直角三角形をつくって求める。",
                 "空間図形では、求める線分を斜辺とする直角三角形を取り出す。最短距離は展開図で考える。"]),
        check("ck1", "確認問題",
              [("直角をはさむ2辺が $5$ cm、$12$ cm の直角三角形の斜辺を求めなさい。", "$13$ cm"),
               ("1辺が $4$ cm の正方形の対角線の長さを求めなさい。", "$4\\sqrt{2}$ cm"),
               ("3辺が $7$ cm、$24$ cm、$25$ cm の三角形は直角三角形か。", "$7^2+24^2=625=25^2$ なので直角三角形")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

@gen("basic_check", 4, ["computation"])
def a_hyp(r):
    kind = r.choice(["hyp", "hyp", "leg"])
    if kind == "hyp":
        a, b = r.sample(range(1, 13), 2)
        sq = a * a + b * b
        stem = f"右の図の直角三角形 ABC で，${A('ABC')}=90^\\circ$，AB$={a}$ cm，BC$={b}$ cm である。辺 AC の長さは何 cm か，求めなさい。"
        st = ["AC は直角に対する辺（斜辺）。", f"AC$^2={a}^2+{b}^2={sq}$。", f"AC$=\\sqrt{{{sq}}}={rtex(sq)}$ cm。"]
        expr = f"sqrt({a}**2+{b}**2)"
        fig = rtri_fig(a, b)
    else:
        a = r.randint(1, 12)
        c = r.randint(a + 1, 15)
        sq = c * c - a * a
        stem = f"右の図の直角三角形 ABC で，${A('ABC')}=90^\\circ$，AC$={c}$ cm，AB$={a}$ cm である。辺 BC の長さは何 cm か，求めなさい。"
        st = ["斜辺は AC。", f"BC$^2={c}^2-{a}^2={sq}$。", f"BC$=\\sqrt{{{sq}}}={rtex(sq)}$ cm。"]
        expr = f"sqrt({c}**2-{a}**2)"
        fig = rtri_fig(a, math.sqrt(sq))
    return MARKR(stem, sq, st[-1], expr, d=1, fig=fig,
                 ap="三平方の定理 $a^2+b^2=c^2$（$c$ は斜辺）。まず直角の位置から斜辺を確かめる。根号の中はできるだけ小さい自然数にする。",
                 steps=st,
                 alt=["求めた長さを2乗して，三平方の定理が成り立つかを確かめる。"],
                 pc=[("三平方の定理を正しく立てている", 1), ("根号を簡単にして正しく答えている", 1)],
                 pit=["斜辺がわかっているのに2乗の和をとる。", "根号の中を簡単にしない。"])


def _tri_text(t):
    return "，".join(f"${x}$ cm" for x in t)


@gen("basic_check", 4, ["condition_check", "concept"])
def a_converse(r):
    k = r.randint(1, 3)
    base = r.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (6, 8, 10), (9, 12, 15), (20, 21, 29)])
    right_t = tuple(x * k for x in base) if max(base) * k <= 40 else base
    cands = []
    near = [(right_t[0], right_t[1], right_t[2] + 1), (right_t[0] + 1, right_t[1], right_t[2]), (right_t[0], right_t[1] + 1, right_t[2] + 1),
            (right_t[0] + 2, right_t[1] + 2, right_t[2] + 2), (right_t[0], right_t[1], right_t[2] - 1)]
    for t in r.sample(near, 3):
        a, b, c = sorted(t)
        if a * a + b * b == c * c or a + b <= c:
            continue
        cands.append((_tri_text(t), f"${a}^2+{b}^2={a * a + b * b}$，${c}^2={c * c}$ で等しくない。", "三平方の定理の逆の確かめ不足"))
    if r.random() < 0.5:
        cands.append(("$2$ cm，$3$ cm，$\\sqrt{10}$ cm", "$2^2+3^2=13$，$(\\sqrt{10})^2=10$ で等しくない。", "三平方の定理の逆の確かめ不足"))
    cands.append(("$1$ cm，$1$ cm，$\\sqrt{3}$ cm", "$1^2+1^2=2$，$(\\sqrt{3})^2=3$ で等しくない。", "三平方の定理の逆の確かめ不足"))
    r.shuffle(cands)
    use_root = r.random() < 0.3
    if use_root:
        a = r.randint(1, 4)
        b = r.randint(1, 4)
        right = f"${a}$ cm，${b}$ cm，${rtex(a * a + b * b)}$ cm"
        e = f"${a}^2+{b}^2={a * a + b * b}=({rtex(a * a + b * b)})^2$ なので，直角三角形である。"
    else:
        tt = list(right_t)
        r.shuffle(tt)
        right = _tri_text(tt)
        a, b, c = right_t
        e = f"${a}^2+{b}^2={a * a + b * b}={c}^2$ なので，直角三角形である。"
    return MC("3辺の長さが次のようになる三角形のうち，直角三角形であるものとして最も適するものを，" + SEL4,
              right, cands, e, d=2,
              ap="三平方の定理の逆：いちばん長い辺を $c$，他の2辺を $a$，$b$ として $a^2+b^2=c^2$ が成り立てば直角三角形。",
              steps=["それぞれ，いちばん長い辺を見つける。", "残りの2辺の2乗の和と，いちばん長い辺の2乗を比べる。", e],
              alt=["$3:4:5$，$5:12:13$ などのよく知られた比になっているかを見て，見当をつけてから確かめる。"],
              pc=[("いちばん長い辺を正しく選んでいる", 1), ("2乗の和を正しく比べている", 1)],
              pit=["いちばん長い辺以外を斜辺として計算する。", "2乗せずに長さの和で比べる。"])


@gen("basic_check", 4, ["computation", "concept"])
def a_special(r):
    kind = r.choice(["sq_diag", "sq_side", "tri_height", "t30_long", "t30_hyp", "t45_leg"])
    n = r.randint(2, 12)
    if kind == "sq_diag":
        sq = 2 * n * n
        stem = f"1辺の長さが ${n}$ cm の正方形の対角線の長さは何 cm か，求めなさい。"
        st = ["対角線で直角二等辺三角形が2つできる。辺の比は $1:1:\\sqrt{2}$。", f"対角線$={n}\\times\\sqrt{{2}}={rtex(sq)}$ cm。"]
        expr = f"{n}*sqrt(2)"
        fig = figure("正方形と対角線", geo({"A": (0, 3), "B": (0, 0), "C": (3, 0), "D": (3, 3)}, segs=[("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("A", "C")]))
    elif kind == "sq_side":
        sq = Fr(n * n, 2)
        stem = f"対角線の長さが ${n}$ cm の正方形の1辺の長さは何 cm か，求めなさい。"
        st = ["1辺を $x$ cm とすると，$x^2+x^2=" + f"{n}^2$。", f"$x^2={ftex(sq)}$，$x={rtex(sq)}$ cm。"]
        expr = f"{n}/sqrt(2)"
        fig = figure("正方形と対角線", geo({"A": (0, 3), "B": (0, 0), "C": (3, 0), "D": (3, 3)}, segs=[("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("A", "C")]))
    elif kind == "tri_height":
        sq = Fr(3 * n * n, 4)
        stem = f"1辺の長さが ${n}$ cm の正三角形の高さは何 cm か，求めなさい。"
        st = [f"頂点から底辺に垂線をひくと，底辺は2等分され，斜辺 ${n}$，短い辺 ${ftex(Fr(n, 2))}$ の直角三角形ができる。",
              f"高さ$^2={n}^2-\\left({ftex(Fr(n, 2))}\\right)^2={ftex(sq)}$。", f"高さ$={rtex(sq)}$ cm。"]
        expr = f"sqrt({n}**2-Rational({n},2)**2)"
        fig = figure("正三角形と高さ", geo({"A": (2.0, 3.46), "B": (0.0, 0.0), "C": (4.0, 0.0), "H": (2.0, 0.0)}, segs=[("A", "B"), ("B", "C"), ("C", "A")],
                                          dashed=[("A", "H")], right=[("A", "H", "C")], off={"H": (0, -0.4)}))
    elif kind in ("t30_long", "t30_hyp"):
        P = {"A": (0.0, 2.08), "B": (0.0, 0.0), "C": (3.6, 0.0)}
        fig = figure("30°・60°・90° の直角三角形", geo(P, segs=[("A", "B"), ("B", "C"), ("C", "A")], right=[("A", "B", "C")], texts=[(0.35, 1.55, "60°"), (2.75, 0.25, "30°")]))
        if kind == "t30_long":
            sq = 3 * n * n
            stem = f"右の図の直角三角形 ABC で，${A('ABC')}=90^\\circ$，${A('ACB')}=30^\\circ$，AB$={n}$ cm である。辺 BC の長さは何 cm か，求めなさい。"
            st = ["$30^\\circ$・$60^\\circ$・$90^\\circ$ の直角三角形の辺の比は AB：AC：BC$=1:2:\\sqrt{3}$。", f"BC$={n}\\times\\sqrt{{3}}={rtex(sq)}$ cm。"]
            expr = f"{n}*sqrt(3)"
        else:
            sq = Fr(3 * n * n, 4)
            stem = f"右の図の直角三角形 ABC で，${A('ABC')}=90^\\circ$，${A('ACB')}=30^\\circ$，AC$={n}$ cm である。辺 BC の長さは何 cm か，求めなさい。"
            st = ["辺の比は AB：AC：BC$=1:2:\\sqrt{3}$。", f"BC$={n}\\times\\dfrac{{\\sqrt{{3}}}}{{2}}={rtex(sq)}$ cm。"]
            expr = f"{n}*sqrt(3)/2"
    else:
        sq = Fr(n * n, 2)
        P = {"A": (0.0, 3.0), "B": (0.0, 0.0), "C": (3.0, 0.0)}
        fig = figure("直角二等辺三角形", geo(P, segs=[("A", "B"), ("B", "C"), ("C", "A")], right=[("A", "B", "C")], ticks=[("A", "B", 1), ("B", "C", 1)]))
        stem = f"右の図の直角二等辺三角形 ABC で，${A('ABC')}=90^\\circ$，AB$=$BC，AC$={n}$ cm である。辺 AB の長さは何 cm か，求めなさい。"
        st = ["辺の比は AB：BC：AC$=1:1:\\sqrt{2}$。", f"AB$=\\dfrac{{{n}}}{{\\sqrt{{2}}}}={rtex(sq)}$ cm。"]
        expr = f"{n}/sqrt(2)"
    return MARKR(stem, sq, st[-1], expr, d=2, fig=fig,
                 ap="直角二等辺三角形は $1:1:\\sqrt{2}$，$30^\\circ$・$60^\\circ$・$90^\\circ$ の直角三角形は $1:2:\\sqrt{3}$（短い辺：斜辺：残りの辺）。",
                 steps=st,
                 alt=["辺の比を使わずに，三平方の定理で方程式を立てても同じ答えになる。"],
                 pc=[("特別な直角三角形の辺の比を正しく使っている", 1), ("根号を簡単にして正しく答えている", 1)],
                 pit=["$1:2:\\sqrt{3}$ の順番を取り違える。", "分母に根号を残したままにする（有理化を忘れる）。"])


@gen("basic_check", 4, ["computation", "cross_unit"], rel=["JH-MATH-G2-U03"])
def a_distance(r):
    while True:
        x1, y1, x2, y2 = (r.randint(-6, 6) for _ in range(4))
        if x1 != x2 and y1 != y2:
            break
    sq = (x2 - x1) ** 2 + (y2 - y1) ** 2
    stem = f"座標平面上の2点 A$({x1},\\,{y1})$，B$({x2},\\,{y2})$ の間の距離を求めなさい。ただし，座標の1目もりを 1 cm とする。"
    st = [f"横の長さ $|{x2}-({x1})|={abs(x2 - x1)}$，縦の長さ $|{y2}-({y1})|={abs(y2 - y1)}$。",
          f"AB$^2={abs(x2 - x1)}^2+{abs(y2 - y1)}^2={sq}$。", f"AB$={rtex(sq)}$ cm。"]
    from banks._common import plane
    lo = min(x1, x2, y1, y2, 0) - 1
    hi = max(x1, x2, y1, y2, 0) + 1
    fig = figure("座標平面上の2点 A，B", plane(xr=(lo, hi), yr=(lo, hi), unit=max(12, int(200 / (hi - lo))), ticks=False,
                                             points=[(x1, y1, "A"), (x2, y2, "B")], segments=[((x1, y1), (x2, y2))]))
    return MARKR(stem, sq, st[-1], f"sqrt(({x2}-({x1}))**2+({y2}-({y1}))**2)", d=2, fig=fig,
                 ap="AB を斜辺とし，座標軸に平行な2辺をもつ直角三角形をつくる（座標平面・一次関数の単元とのつながり）。横は $x$ 座標の差，縦は $y$ 座標の差。",
                 steps=st,
                 alt=["座標平面に点をとり，方眼で横・縦の長さを数えて確かめる。"],
                 pc=[("横・縦の長さを正しく求めている", 1), ("正しい距離を求めている", 1)],
                 pit=["負の座標の差を計算するときに符号を誤る。", "座標の差を2乗せずにたす。"])


@gen("basic_check", 4, ["computation"])
def a_cuboid(r):
    kind = r.choice(["box", "box", "cube", "face"])
    if kind == "cube":
        a = r.randint(2, 12)
        sq = 3 * a * a
        stem = f"1辺の長さが ${a}$ cm の立方体 ABCD-EFGH の対角線 AG の長さは何 cm か，求めなさい。"
        st = [f"底面の対角線 EG$={a}\\sqrt{{2}}$ cm。", f"△AEG は ∠AEG$=90^\\circ$ の直角三角形なので AG$^2={a}^2+({a}\\sqrt{{2}})^2={sq}$。", f"AG$={rtex(sq)}$ cm。"]
        expr = f"sqrt(3*{a}**2)"
        fig = box_fig(1, 1, 1, extra_dashed=[("A", "G"), ("E", "G")], alt="立方体 ABCD-EFGH")
    elif kind == "face":
        a, b, c = r.sample(range(2, 13), 3)
        sq = b * b + c * c
        stem = f"直方体 ABCD-EFGH で，AB$={a}$ cm，BC$={b}$ cm，AE$={c}$ cm である。線分 BG の長さは何 cm か，求めなさい。"
        st = ["BG は長方形 BFGC の対角線で，△BFG は ∠BFG$=90^\\circ$ の直角三角形。", f"BG$^2=$BF$^2+$FG$^2={c}^2+{b}^2={sq}$。", f"BG$={rtex(sq)}$ cm。"]
        expr = f"sqrt({b}**2+{c}**2)"
        fig = box_fig(a, b, c, extra_segs=[("B", "G")])
    else:
        a, b, c = r.sample(range(1, 13), 3)
        sq = a * a + b * b + c * c
        stem = f"直方体 ABCD-EFGH で，AB$={a}$ cm，BC$={b}$ cm，AE$={c}$ cm である。対角線 AG の長さは何 cm か，求めなさい。"
        st = [f"EG$^2=$EF$^2+$FG$^2={a}^2+{b}^2$。", f"AG$^2=$AE$^2+$EG$^2={c}^2+{a}^2+{b}^2={sq}$。", f"AG$={rtex(sq)}$ cm。"]
        expr = f"sqrt({a}**2+{b}**2+{c}**2)"
        fig = box_fig(a, b, c, extra_dashed=[("A", "G"), ("E", "G")])
    return MARKR(stem, sq, st[-1], expr, d=2, fig=fig,
                 ap="求める線分を斜辺とする直角三角形を見取図から取り出す。直方体の対角線は $\\sqrt{a^2+b^2+c^2}$。",
                 steps=st,
                 alt=["直方体の対角線の公式 $\\sqrt{a^2+b^2+c^2}$ にあてはめて確かめる。"],
                 pc=[("直角三角形を正しく取り出している", 1), ("正しい長さを求めている", 1)],
                 pit=["高さをふくめ忘れて $\\sqrt{a^2+b^2}$ とする。", "見取図の見かけの角度を直角と思いこむ。"])


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 4, ["computation", "application"])
def b_isosceles(r):
    kind = r.choice(["height", "area", "eq_area"])
    if kind == "eq_area":
        a = r.randint(2, 12)
        sq = Fr(3 * a ** 4, 16)
        stem = f"1辺の長さが ${a}$ cm の正三角形の面積は何 cm² か，求めなさい。"
        st = [f"高さは ${a}\\times\\dfrac{{\\sqrt{{3}}}}{{2}}={rtex(Fr(3 * a * a, 4))}$ cm。", f"面積$=\\dfrac{{1}}{{2}}\\times{a}\\times{rtex(Fr(3 * a * a, 4))}={rtex(sq)}$ cm²。"]
        expr = f"Rational(1,2)*{a}*{a}*sqrt(3)/2"
        fig = figure("正三角形", geo({"A": (2.0, 3.46), "B": (0.0, 0.0), "C": (4.0, 0.0), "H": (2.0, 0.0)}, segs=[("A", "B"), ("B", "C"), ("C", "A")], dashed=[("A", "H")], off={"H": (0, -0.4)}))
    else:
        while True:
            s = r.randint(3, 15)
            b = r.randint(2, 2 * s - 1)
            if b != s:
                break
        hsq = Fr(4 * s * s - b * b, 4)
        P = {"A": (2.0, 3.2), "B": (0.0, 0.0), "C": (4.0, 0.0), "H": (2.0, 0.0)}
        fig = figure("二等辺三角形 ABC と高さ AH", geo(P, segs=[("A", "B"), ("B", "C"), ("C", "A")], dashed=[("A", "H")], ticks=[("A", "B", 1), ("A", "C", 1)], right=[("A", "H", "C")], off={"H": (0, -0.4)}))
        st = ["頂点 A から底辺 BC に垂線 AH をひくと，H は BC の中点。", f"AH$^2={s}^2-\\left({ftex(Fr(b, 2))}\\right)^2={ftex(hsq)}$，AH$={rtex(hsq)}$ cm。"]
        if kind == "height":
            sq = hsq
            stem = f"右の図のように，AB$=$AC$={s}$ cm，BC$={b}$ cm の二等辺三角形 ABC がある。頂点 A から辺 BC にひいた垂線 AH の長さは何 cm か，求めなさい。"
            expr = f"sqrt({s}**2-Rational({b},2)**2)"
        else:
            sq = hsq * b * b / 4
            stem = f"右の図のように，AB$=$AC$={s}$ cm，BC$={b}$ cm の二等辺三角形 ABC がある。△ABC の面積は何 cm² か，求めなさい。"
            st.append(f"面積$=\\dfrac{{1}}{{2}}\\times{b}\\times{rtex(hsq)}={rtex(sq)}$ cm²。")
            expr = f"Rational(1,2)*{b}*sqrt({s}**2-Rational({b},2)**2)"
    return MARKR(stem, sq, st[-1], expr, d=3, p=4, fig=fig,
                 ap="二等辺三角形（正三角形）は，頂点から底辺に垂線をひくと底辺が2等分され，直角三角形が2つできる。",
                 steps=st,
                 alt=["正三角形なら辺の比 $1:2:\\sqrt{3}$，二等辺三角形なら三平方の定理で高さを求め，面積の公式にあてはめる。"],
                 pc=[("高さを正しく求めている", 2), ("面積（または長さ）を正しく求めている", 2)],
                 pit=["底辺を2等分し忘れる。", "高さを求めるときに2乗の和をとる。"])


@gen("standard_practice", 4, ["cross_unit", "computation"], rel=["JH-MATH-G3-U06"])
def b_chord(r):
    kind = r.choice(["chord", "dist", "tangent"])
    R = 2.2
    if kind == "chord":
        rr = r.randint(3, 15)
        d = r.randint(1, rr - 1)
        sq = 4 * (rr * rr - d * d)
        stem = f"半径 ${rr}$ cm の円 O で，中心 O からの距離が ${d}$ cm である弦 AB の長さは何 cm か，求めなさい。"
        st = ["O から弦 AB に垂線 OH をひくと，H は AB の中点。", f"AH$^2={rr}^2-{d}^2={rr * rr - d * d}$，AH$={rtex(rr * rr - d * d)}$ cm。", f"AB$=2\\times$AH$={rtex(sq)}$ cm。"]
        expr = f"2*sqrt({rr}**2-{d}**2)"
        hy = -R * d / rr
        hx = math.sqrt(R * R - hy * hy)
        P = {"O": (0.0, 0.0), "A": (-hx, hy), "B": (hx, hy), "H": (0.0, hy)}
        fig = figure("円 O と弦 AB", geo(P, segs=[("A", "B"), ("O", "A")], dashed=[("O", "H")], circles=[(0, 0, R)], right=[("O", "H", "B")], scale=30, off={"O": (0, 0.3), "H": (0.2, -0.35)}))
    elif kind == "dist":
        rr = r.randint(3, 15)
        half = r.randint(1, rr - 1)
        sq = rr * rr - half * half
        stem = f"半径 ${rr}$ cm の円 O に，長さ ${2 * half}$ cm の弦 AB がある。中心 O と弦 AB との距離は何 cm か，求めなさい。"
        st = ["O から弦 AB に垂線 OH をひくと，H は AB の中点で AH$=" + f"{half}$ cm。", f"OH$^2={rr}^2-{half}^2={sq}$。", f"OH$={rtex(sq)}$ cm。"]
        expr = f"sqrt({rr}**2-{half}**2)"
        hx = R * half / rr
        hy = -math.sqrt(R * R - hx * hx)
        P = {"O": (0.0, 0.0), "A": (-hx, hy), "B": (hx, hy), "H": (0.0, hy)}
        fig = figure("円 O と弦 AB", geo(P, segs=[("A", "B"), ("O", "A")], dashed=[("O", "H")], circles=[(0, 0, R)], right=[("O", "H", "B")], scale=30, off={"O": (0, 0.3), "H": (0.2, -0.35)}))
    else:
        rr = r.randint(2, 12)
        d = r.randint(rr + 1, rr + 12)
        sq = d * d - rr * rr
        stem = f"半径 ${rr}$ cm の円 O の外部に，中心 O からの距離が ${d}$ cm の点 P がある。P から円 O に接線をひき，接点を A とするとき，線分 PA の長さは何 cm か，求めなさい。"
        st = ["接線は接点を通る半径に垂直なので ∠OAP$=90^\\circ$。", f"PA$^2=$OP$^2-$OA$^2={d}^2-{rr}^2={sq}$。", f"PA$={rtex(sq)}$ cm。"]
        expr = f"sqrt({d}**2-{rr}**2)"
        th = math.acos(rr / d)
        P = {"O": (0.0, 0.0), "P": (R * d / rr, 0.0), "A": (R * math.cos(th), R * math.sin(th))}
        fig = figure("円 O と接線 PA", geo(P, segs=[("O", "A"), ("A", "P"), ("O", "P")], circles=[(0, 0, R)], right=[("O", "A", "P")], scale=30, off={"O": (-0.3, -0.2)}))
    return MARKR(stem, sq, st[-1], expr, d=3, p=4, fig=fig,
                 ap="円の中心から弦にひいた垂線は弦を2等分する。接線は接点を通る半径に垂直（円の単元とのつながり）。半径を斜辺とする直角三角形をつくる。",
                 steps=st,
                 alt=["図に半径をかき入れて，どの辺が斜辺になるかを確かめてから計算する。"],
                 pc=[("直角三角形を正しくつくっている", 2), ("正しい長さを求めている", 2)],
                 pit=["弦の半分ではなく弦全体の長さで計算する。", "接線の問題で OP を斜辺にしない。"])


@gen("standard_practice", 4, ["computation", "application"])
def b_pyramid(r):
    kind = r.choice(["sq_h", "sq_vol", "cone_h", "cone_slant"])
    if kind in ("sq_h", "sq_vol"):
        a = r.choice(range(2, 13, 2))
        e = r.randint(a // 2 + 2, a + 10)
        hsq = Fr(e * e) - Fr(a * a, 2)
        if hsq <= 0:
            raise AssertionError
        fig = pyr_fig("square", "正四角錐 ABCDE")
        st = [f"底面の対角線 BD$={a}\\sqrt{{2}}$ cm，その半分 BH$={rtex(Fr(a * a, 2))}$ cm（H は底面の対角線の交点）。",
              f"AH$^2=$AB$^2-$BH$^2={e}^2-{ftex(Fr(a * a, 2))}={ftex(hsq)}$，AH$={rtex(hsq)}$ cm。"]
        if kind == "sq_h":
            sq = hsq
            stem = f"右の図の正四角錐 ABCDE は，底面が1辺 ${a}$ cm の正方形 BCDE で，側面の辺 AB，AC，AD，AE の長さがすべて ${e}$ cm である。この正四角錐の高さ AH は何 cm か，求めなさい。"
            expr = f"sqrt({e}**2-Rational({a * a},2))"
        else:
            sq = hsq * Fr(a * a, 3) ** 2
            stem = f"右の図の正四角錐 ABCDE は，底面が1辺 ${a}$ cm の正方形 BCDE で，側面の辺 AB，AC，AD，AE の長さがすべて ${e}$ cm である。この正四角錐の体積は何 cm³ か，求めなさい。"
            st.append(f"体積$=\\dfrac{{1}}{{3}}\\times{a}^2\\times{rtex(hsq)}={rtex(sq)}$ cm³。")
            expr = f"Rational({a * a},3)*sqrt({e}**2-Rational({a * a},2))"
    else:
        fig = pyr_fig("cone", "円錐（頂点 A，底面の中心 O）")
        if kind == "cone_h":
            rr = r.randint(1, 10)
            l_ = r.randint(rr + 1, rr + 10)
            sq = l_ * l_ - rr * rr
            stem = f"右の図の円錐は，頂点が A，底面の円の中心が O で，底面の半径 OB が ${rr}$ cm，母線 AB の長さが ${l_}$ cm である。この円錐の高さ AO は何 cm か，求めなさい。"
            st = ["△AOB は ∠AOB$=90^\\circ$ の直角三角形。", f"AO$^2={l_}^2-{rr}^2={sq}$。", f"AO$={rtex(sq)}$ cm。"]
            expr = f"sqrt({l_}**2-{rr}**2)"
        else:
            rr = r.randint(1, 10)
            h = r.randint(1, 12)
            sq = rr * rr + h * h
            stem = f"右の図の円錐は，頂点が A，底面の円の中心が O で，底面の半径 OB が ${rr}$ cm，高さ AO が ${h}$ cm である。この円錐の母線 AB の長さは何 cm か，求めなさい。"
            st = ["△AOB は ∠AOB$=90^\\circ$ の直角三角形で，AB が斜辺。", f"AB$^2={rr}^2+{h}^2={sq}$。", f"AB$={rtex(sq)}$ cm。"]
            expr = f"sqrt({rr}**2+{h}**2)"
    return MARKR(stem, sq, st[-1], expr, d=3, p=4, fig=fig,
                 ap="角錐・円錐の高さは，頂点から底面に垂線をひいてできる直角三角形で求める。正四角錐では底面の対角線の半分を使う。",
                 steps=st,
                 alt=["正四角錐では，側面の二等辺三角形の高さ（斜高）を先に求め，底面の1辺の半分と組み合わせて高さを求めることもできる。"],
                 pc=[("直角三角形を正しく取り出している", 2), ("正しい値を求めている", 2)],
                 pit=["正四角錐で底面の1辺の半分を使ってしまう（対角線の半分を使う）。", "母線と高さを取り違える。"])


@gen("standard_practice", 4, ["application", "cross_unit"], rel=["JH-MATH-G1-U03"])
def b_equation(r):
    kind = r.choice(["hyp_longer", "leg_sum"])
    if kind == "hyp_longer":
        m = r.randint(1, 6)
        k = r.randint(m + 1, 15)
        v = Fr(k * k - m * m, 2 * m)
        stem = f"∠B$=90^\\circ$ の直角三角形 ABC で，BC$={k}$ cm であり，斜辺 AC は辺 AB より ${m}$ cm 長い。辺 AB の長さは何 cm か，求めなさい。"
        st = [f"AB$=x$ cm とすると AC$=x+{m}$ cm。", f"三平方の定理より $x^2+{k}^2=(x+{m})^2$。",
              f"$x^2+{k * k}=x^2+{2 * m}x+{m * m}$ より ${2 * m}x={k * k - m * m}$。", f"$x={ftex(v)}$。"]
        expr = f"Rational({k}**2-{m}**2,2*{m})"
    else:
        while True:
            a, b = r.sample(range(1, 16), 2)
            c2 = a * a + b * b
            c = math.isqrt(c2)
            if c * c == c2:
                break
        s = a + b
        v = min(a, b)
        stem = f"斜辺の長さが ${c}$ cm の直角三角形で，直角をはさむ2辺の長さの和は ${s}$ cm である。直角をはさむ2辺のうち，短い方の辺の長さは何 cm か，求めなさい。"
        st = [f"短い方の辺を $x$ cm とすると，もう1辺は $({s}-x)$ cm。", f"$x^2+({s}-x)^2={c}^2$ を整理して $x^2-{s}x+{(s * s - c * c) // 2}=0$。",
              f"$(x-{a})(x-{b})=0$ より $x={min(a, b)},\\ {max(a, b)}$。", f"短い方なので ${v}$ cm。"]
        expr = f"{v}"
        if (s * s - c * c) % 2:
            raise AssertionError
    return MARK(stem, v, st[-1], expr, d=3, p=4,
                ap="わからない辺を $x$ とおき，三平方の定理で方程式をつくる（方程式の単元とのつながり）。解が問題に合っているかも確かめる。",
                steps=st,
                alt=["求めた値を三平方の定理にあてはめて，等式が成り立つか確かめる。"],
                pc=[("三平方の定理を使って方程式を正しく立てている", 2), ("方程式を解き，問題に合う解を選んでいる", 2)],
                pit=["$(x+m)^2$ を $x^2+m^2$ と展開してしまう。", "どの辺が斜辺かを取り違える。"])


@gen("standard_practice", 4, ["application", "multiple_solutions"])
def b_shortest(r):
    kind = r.choice(["box", "box", "cyl"])
    if kind == "box":
        a, b, c = r.sample(range(2, 13), 3)
        sq = (a + b) ** 2 + c * c
        stem = (f"右の図の直方体 ABCD-EFGH で，AB$={a}$ cm，BC$={b}$ cm，AE$={c}$ cm である。頂点 A から辺 BF 上の点 P を通って頂点 G まで糸をかける。"
                "糸の長さがもっとも短くなるとき，その長さは何 cm か，求めなさい。")
        st = ["面 ABFE と面 BCGF の展開図をかくと，A と G を結ぶ線分が最短の糸になる。", f"展開図で，横の長さは AB$+$BC$={a}+{b}={a + b}$，縦の長さは CG$={c}$。",
              f"最短の長さ$=\\sqrt{{{a + b}^2+{c}^2}}={rtex(sq)}$ cm。"]
        expr = f"sqrt(({a}+{b})**2+{c}**2)"
        fig = box_fig(a, b, c, extra_segs=[("A", "P"), ("P", "G")], extra_pts={"P": (a * 3.6 / max(a, b, c), 0, c * 3.6 / max(a, b, c) * b / (a + b))})
        alt = [f"展開図で △ の相似を使うと，BP$={ftex(Fr(c * b, a + b))}$ cm のときに最短になることもわかる。"]
    else:
        rr = r.randint(1, 6)
        h = r.randint(2, 20)
        # 円周 2πr は π をふくむので，半周の長さを整数で与える
        half = r.randint(3, 15)
        sq = half * half + h * h
        stem = (f"円柱の側面上で，下の底面の円周上の点 A から，ちょうど反対側にある上の底面の円周上の点 B まで，側面にそって糸をかける。"
                f"円柱の高さは ${h}$ cm で，底面の円周の半分の長さは ${half}$ cm である。糸の長さがもっとも短くなるとき，その長さは何 cm か，求めなさい。")
        st = ["側面の展開図は長方形になる。", f"A と B は展開図で，横に ${half}$ cm（円周の半分），縦に ${h}$ cm はなれている。", f"最短の長さ$=\\sqrt{{{half}^2+{h}^2}}={rtex(sq)}$ cm。"]
        expr = f"sqrt({half}**2+{h}**2)"
        fig = None
        alt = ["円柱の側面を切り開いた長方形の図をかき，A と B の位置を確かめる。"]
        del rr
    kw = {"fig": fig} if fig else {}
    return MARKR(stem, sq, st[-1], expr, d=3, p=4,
                 ap="立体の表面を通る最短の長さは，展開図にかいたときの線分の長さ。展開図で直角三角形をつくって三平方の定理を使う。",
                 steps=st, alt=alt,
                 pc=[("展開図で考えることに気づいている", 2), ("正しい長さを求めている", 2)],
                 pit=["見取図のまま直方体の対角線 AG を答える。", "展開図で横の長さを1辺分しかとらない。"], **kw)


# ======================================================================
# C 思考力・記述応用
# ======================================================================

def _xy_pool(r):
    return [
        ("直角三角形で，斜辺の長さの2乗は，他の2辺の長さの2乗の和に等しい。", True, "三平方の定理である。"),
        ("どんな三角形でも，いちばん長い辺の長さの2乗は，他の2辺の長さの2乗の和に等しい。", False, "直角三角形のときだけ成り立つ。たとえば正三角形では成り立たない。"),
        ("3辺の長さが $a$，$b$，$c$ の三角形で $a^2+b^2=c^2$ ならば，その三角形は直角三角形である。", True, "三平方の定理の逆である。"),
        ("1辺が $a$ の正方形の対角線の長さは $\\sqrt{2}a$ である。", True, "直角二等辺三角形の辺の比 $1:1:\\sqrt{2}$ より。"),
        ("1辺が $a$ の正方形の対角線の長さは $2a$ である。", False, "対角線は $\\sqrt{2}a$ である。"),
        ("1辺が $a$ の正三角形の高さは $\\dfrac{\\sqrt{3}}{2}a$ である。", True, "辺の比 $1:2:\\sqrt{3}$ より。"),
        ("1辺が $a$ の正三角形の高さは $\\dfrac{a}{2}$ である。", False, "$\\dfrac{a}{2}$ は底辺の半分。高さは $\\dfrac{\\sqrt{3}}{2}a$。"),
        ("縦 $a$，横 $b$，高さ $c$ の直方体の対角線の長さは $\\sqrt{a^2+b^2+c^2}$ である。", True, "底面の対角線と高さで直角三角形をつくると求められる。"),
        ("縦 $a$，横 $b$，高さ $c$ の直方体の対角線の長さは $\\sqrt{a^2+b^2}+c$ である。", False, "底面の対角線と高さは直角に交わるので，和ではなく三平方の定理を使う。"),
        ("3辺の長さが $3$ cm，$4$ cm，$6$ cm の三角形は直角三角形である。", False, "$3^2+4^2=25$，$6^2=36$ で等しくない。"),
        ("3辺の長さが $5$ cm，$12$ cm，$13$ cm の三角形は直角三角形である。", True, "$5^2+12^2=169=13^2$。"),
        ("立体の表面を通る2点間の最短の長さは，展開図で2点を結ぶ線分の長さとして求められる。", True, "展開図で2点を結ぶ線分がもっとも短い。"),
    ]


@gen("thinking_writing", 3, ["written_reasoning", "condition_check"])
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
        why[c] = (" ".join(rs), "三平方の定理の使い方の思いこみ")
    return mc("三平方の定理とその利用について述べた次の X，Y の文の正誤の組み合わせとして最も適するものを，" + SEL4 + f"\nX　{x[0]}\nY　{y[0]}",
              [ans] + [c for c in XY if c != ans], f"X：{x[2]}　Y：{y[2]}", d=4, p=8, why=why,
              ap="三平方の定理が成り立つ条件（直角三角形であること），特別な直角三角形の辺の比，空間での直角三角形の取り出し方と照らし合わせる。",
              steps=[f"X：{x[2]}", f"Y：{y[2]}", f"よって {ans}。"],
              alt=["具体的な数（$a=1$ など）を入れて，文が成り立つかを計算で確かめる。"],
              pc=[("X の正誤を根拠をもって判断している", 4), ("Y の正誤を根拠をもって判断している", 4)],
              pit=["直角三角形でない三角形にも三平方の定理を使う。", "特別な直角三角形の辺の比を取り違える。"])


A_LIST = [Fr(1, 2), Fr(1), Fr(1, 4), Fr(2), Fr(1, 3)]


@gen("thinking_writing", 4, ["cross_unit", "application"], rel=["JH-MATH-G3-U04"])
def c_coord(r):
    a = r.choice(A_LIST)
    xs = [x for x in range(-6, 7) if x != 0 and (a * x * x).denominator == 1 and a * x * x <= 18]
    x1, x2 = r.sample(xs, 2)
    if abs(x1) == abs(x2) and r.random() < 0.5:
        raise AssertionError
    y1, y2 = a * x1 * x1, a * x2 * x2
    kind = r.choice(["ab", "oa", "ab"])
    from banks._common import plane
    lo_x, hi_x = min(x1, x2, 0) - 1, max(x1, x2, 0) + 1
    hi_y = int(max(y1, y2)) + 1
    afn = (lambda t, a=a: float(a) * t * t)
    fig = figure("放物線 y=ax² 上の2点", plane(xr=(lo_x, hi_x), yr=(-1, hi_y), unit=max(10, int(220 / max(hi_x - lo_x, hi_y + 1))), ticks=False, grid=False,
                                            curves=[(afn, "")], points=[(x1, float(y1), "A"), (x2, float(y2), "B")],
                                            segments=[((x1, float(y1)), (x2, float(y2)))] if kind == "ab" else [((0, 0), (x1, float(y1)))]))
    eq = f"y={'' if a == 1 else ftex(a)}x^2"
    if kind == "ab":
        sq = (x2 - x1) ** 2 + (y2 - y1) ** 2
        stem = (f"右の図のように，関数 ${eq}$ のグラフ上に2点 A，B があり，点 A の $x$ 座標は ${x1}$，点 B の $x$ 座標は ${x2}$ である。"
                "線分 AB の長さを求めなさい。ただし，座標の1目もりを 1 cm とする。")
        st = [f"A$({x1},\\,{ftex(y1)})$，B$({x2},\\,{ftex(y2)})$。", f"横の長さ $|{x2}-({x1})|={abs(x2 - x1)}$，縦の長さ $|{ftex(y2)}-{ftex(y1)}|={ftex(abs(y2 - y1))}$。",
              f"AB$=\\sqrt{{{abs(x2 - x1)}^2+\\left({ftex(abs(y2 - y1))}\\right)^2}}={rtex(sq)}$ cm。"]
        expr = f"sqrt(({x2}-({x1}))**2+({fpy(y2)}-{fpy(y1)})**2)"
    else:
        sq = x1 * x1 + y1 * y1
        stem = (f"右の図のように，関数 ${eq}$ のグラフ上に点 A があり，点 A の $x$ 座標は ${x1}$ である。原点を O とするとき，線分 OA の長さを求めなさい。"
                f"ただし，座標の1目もりを 1 cm とする。（点 B は $x$ 座標が ${x2}$ のグラフ上の点で，この問いでは使わない。）")
        st = [f"A$({x1},\\,{ftex(y1)})$。", f"OA$^2={x1}^2+\\left({ftex(y1)}\\right)^2={ftex(Fr(sq))}$。", f"OA$={rtex(sq)}$ cm。"]
        expr = f"sqrt(({x1})**2+({fpy(y1)})**2)"
    return MARKR(stem, sq, st[-1], expr, d=4, p=8, fig=fig,
                 ap="グラフ上の点の座標を関数の式から求め（関数 $y=ax^2$ の単元），2点を結ぶ線分を斜辺とする直角三角形をつくって三平方の定理を使う。",
                 steps=st,
                 alt=["座標平面に点をとり，方眼で横・縦の長さを数えて確かめる。"],
                 pc=[("点の座標を正しく求めている", 3), ("横・縦の長さから三平方の定理を正しく使っている", 3), ("根号を簡単にして正しく答えている", 2)],
                 pit=["$y$ 座標を $ax$ と計算してしまう（2乗を忘れる）。", "負の $x$ 座標の差の計算で符号を誤る。"])


@gen("thinking_writing", 3, ["application", "multiple_solutions"])
def c_space(r):
    a = r.randint(2, 16)
    kind = r.choice(["mid", "center", "tri", "mid2"])
    if kind == "mid":
        sq = Fr(9 * a * a, 4)
        stem = f"1辺の長さが ${a}$ cm の立方体 ABCD-EFGH で，辺 FG の中点を M とする。線分 AM の長さは何 cm か，求めなさい。"
        em = Fr(5 * a * a, 4)
        st = [f"△EFM で，EM$^2=$EF$^2+$FM$^2={a}^2+\\left({ftex(Fr(a, 2))}\\right)^2={ftex(em)}$。", f"△AEM は ∠AEM$=90^\\circ$ の直角三角形なので，AM$^2={a}^2+{ftex(em)}={ftex(sq)}$。", f"AM$={rtex(sq)}$ cm。"]
        expr = f"sqrt({a}**2+{a}**2+({a}/2)**2)"
        fig = box_fig(1, 1, 1, extra_pts={"M": (3.6, 1.8, 0)}, extra_dashed=[("A", "M"), ("E", "M")], alt="立方体 ABCD-EFGH と辺 FG の中点 M")
    elif kind == "center":
        sq = Fr(3 * a * a, 2)
        stem = f"1辺の長さが ${a}$ cm の立方体 ABCD-EFGH で，面 EFGH の対角線の交点を P とする。線分 AP の長さは何 cm か，求めなさい。"
        st = [f"EP は EG の半分で，EP$=\\dfrac{{{a}\\sqrt{{2}}}}{{2}}$，EP$^2={ftex(Fr(a * a, 2))}$。", f"△AEP は直角三角形で AP$^2={a}^2+{ftex(Fr(a * a, 2))}={ftex(sq)}$。", f"AP$={rtex(sq)}$ cm。"]
        expr = f"sqrt({a}**2+{a}**2/2)"
        fig = box_fig(1, 1, 1, extra_pts={"P": (1.8, 1.8, 0)}, extra_dashed=[("A", "P"), ("E", "G")], alt="立方体 ABCD-EFGH と面 EFGH の中心 P")
    elif kind == "tri":
        sq = Fr(3 * a ** 4, 4)
        stem = f"1辺の長さが ${a}$ cm の立方体 ABCD-EFGH で，3点 A，C，F を結んでできる △ACF の面積は何 cm² か，求めなさい。"
        st = [f"AC，CF，FA はどれも正方形の対角線なので，長さはすべて ${a}\\sqrt{{2}}$ cm で，△ACF は正三角形。",
              f"高さは ${a}\\sqrt{{2}}\\times\\dfrac{{\\sqrt{{3}}}}{{2}}={rtex(Fr(6 * a * a, 4))}$ cm。",
              f"面積$=\\dfrac{{1}}{{2}}\\times{a}\\sqrt{{2}}\\times{rtex(Fr(6 * a * a, 4))}={rtex(sq)}$ cm²。"]
        expr = f"Rational(1,2)*{a}*sqrt(2)*{a}*sqrt(2)*sqrt(3)/2"
        fig = box_fig(1, 1, 1, extra_segs=[("A", "C"), ("C", "F"), ("F", "A")], alt="立方体 ABCD-EFGH と △ACF")
    else:
        stem = f"1辺の長さが ${a}$ cm の立方体 ABCD-EFGH で，辺 AB の中点を M，辺 GH の中点を N とする。線分 MN の長さは何 cm か，求めなさい。"
        st = ["M から面 EFGH に垂線 MM' をひく（M' は辺 EF の中点）。", f"M'N は面 EFGH の向かい合う辺の中点を結ぶ線分で長さ ${a}$ cm。",
              f"MN$^2=$MM'$^2+$M'N$^2={a}^2+{a}^2={2 * a * a}$。", f"MN$={rtex(2 * a * a)}$ cm。"]
        sq = 2 * a * a
        expr = f"sqrt(2*{a}**2)"
        fig = box_fig(1, 1, 1, extra_pts={"M": (1.8, 0, 3.6), "N": (1.8, 3.6, 0)}, extra_dashed=[("M", "N")], alt="立方体 ABCD-EFGH と辺 AB，GH の中点 M，N")
    return MARKR(stem, sq, st[-1], expr, d=4, p=8, fig=fig,
                 ap="空間の線分は，それを斜辺とする直角三角形を見取図から取り出し，必要なら三平方の定理を2回使う。",
                 steps=st,
                 alt=["座標のように，3つの方向（縦・横・高さ）の差を求めて $\\sqrt{(縦)^2+(横)^2+(高さ)^2}$ で計算しても同じ結果になる。"],
                 pc=[("直角三角形を正しく取り出している", 3), ("必要な長さを順に求めている", 3), ("正しい答え", 2)],
                 pit=["見取図で直角に見えない角を直角でないと思いこむ（またはその逆）。", "中点までの長さを半分にし忘れる。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def _err_mc(stem, sol, right, cands, e, err, **kw):
    return MC(f"{stem}\n〔Kさんの解答〕\n{sol}\nKさんの解答の誤りを説明したものとして最も適するものを，" + SEL4, right, cands, e, err=err, **kw)


@gen("error_correction", 4, ["common_error", "condition_check"])
def d_hyp_err(r):
    a = r.randint(2, 12)
    c = r.randint(a + 1, 16)
    good = c * c - a * a
    bad = c * c + a * a
    kind = r.choice(["leg", "which"])
    if kind == "leg":
        stem = f"〔問題〕${A('ABC')}=90^\\circ$ の直角三角形 ABC で，AC$={c}$ cm，AB$={a}$ cm のとき，辺 BC の長さを求めなさい。"
        sol = f"BC$^2={c}^2+{a}^2={bad}$ なので，BC$={rtex(bad)}$ cm"
        right = f"斜辺は直角に対する辺 AC である。斜辺の2乗から他の辺の2乗を引いて BC$^2={c}^2-{a}^2$ とするべきである。"
    else:
        stem = f"〔問題〕3辺の長さが AB$={a}$ cm，BC$=$ ? cm，CA$={c}$ cm の直角三角形 ABC があり，${A('ABC')}=90^\\circ$ である。辺 BC の長さを求めなさい。"
        sol = f"最後の辺 BC を斜辺と考えて，BC$^2={a}^2+{c}^2={bad}$，BC$={rtex(bad)}$ cm"
        right = f"∠B が直角なので，斜辺は ∠B に対する辺 CA である。BC$^2={c}^2-{a}^2$ とするべきである。"
    fix = f"BC$={rtex(good)}$ cm"
    cands = [("三平方の定理は，直角をはさむ2辺がわかっているときにしか使えない。", "斜辺と他の1辺がわかっていれば，引き算で残りの辺が求められる。", "定理の使い方の誤解"),
             ("根号の中を簡単にしていないことだけが誤りである。", "根号の扱いより前に，式の立て方（どれが斜辺か）が誤っている。", "論点の取り違え"),
             ("Kさんの解答に誤りはない。", f"BC は斜辺 AC（${c}$ cm）より短いはずだが，Kさんの答えは ${c}$ cm より長い。", "検算不足"),
             ("2乗をせずに，BC$=" + f"{c}-{a}" + "$ とするべきである。", "辺の長さの差ではなく，2乗の差をとる。", "三平方の定理の誤解")]
    r.shuffle(cands)
    return _err_mc(stem, sol, right, cands, f"正しくは {fix}。", dict(sol=sol, step="三平方の定理の式を立てる部分", type="formula", tempt="どの辺が斜辺かを確かめずに，いつも2乗の和をとってしまうため。", fix=fix),
                   d=3, p=6, fig=rtri_fig(a, math.sqrt(good)),
                   ap="三平方の定理を使う前に，直角の位置から斜辺を確かめる。斜辺がわかっているなら2乗の差。",
                   steps=["直角は ∠B なので，斜辺は AC。", f"BC$^2={c}^2-{a}^2={good}$。", f"BC$={rtex(good)}$ cm。"],
                   alt=["答えが斜辺より短くなっているか（斜辺がいちばん長い）で確かめる。"],
                   pc=[("誤りの原因を正しく指摘している", 3), ("正しい長さを求めている", 3)],
                   pit=["斜辺を確かめずに2乗の和をとる。"],
                   chk=(f"sqrt({c}**2-{a}**2)", f"sqrt({good})", None, "intermediate"))


@gen("error_correction", 3, ["common_error", "computation"])
def d_lines_err(r):
    while True:
        a, b = r.sample(range(2, 13), 2)
        n = a * a + b * b
        cc, rad = surd(n)
        if cc > 1 and rad > 1:
            break
    where = r.choice([0, 1, 2])
    l1 = f"AC$^2=$AB$^2+$BC$^2$"
    l2 = f"AC$^2={a}^2+{b}^2={n}$"
    l3 = f"AC$=\\sqrt{{{n}}}={cc}\\sqrt{{{rad}}}$"
    ans = (cc, rad)
    if where == 0:
        l1 = "AC$=$AB$+$BC"
        l2 = f"AC$={a}+{b}={a + b}$"
        l3 = f"AC$={a + b}$"
        ans = None
    elif where == 1:
        n2 = 2 * a + 2 * b
        l2 = f"AC$^2={a}^2+{b}^2={n2}$"
        c2, r2 = surd(n2)
        l3 = f"AC$=\\sqrt{{{n2}}}" + ("" if c2 == 1 else f"={c2}\\sqrt{{{r2}}}") + "$"
        if n2 == n:
            raise AssertionError
    else:
        # 根号の外に出す数を誤る：√(k²·r) を k²√r や (k/…) とする
        bad_c = cc * cc
        l3 = f"AC$=\\sqrt{{{n}}}={bad_c}\\sqrt{{{rad}}}$"
    l4 = "答え　" + l3.split("=")[-1].rstrip("$").join(["$", "$"]) + " cm"
    sol = "\n".join(f"{i + 1}行目　{t}" for i, t in enumerate([l1, l2, l3, l4]))
    del ans
    LINES4 = ["1行目", "2行目", "3行目", "4行目"]
    ok = {0: "1行目は正しい。∠B が直角なので AC が斜辺。", 1: "2行目は2乗を正しく計算している。",
          2: "3行目は根号の中を正しく簡単にしている。", 3: "4行目は3行目の結果をそのまま答えている。"}
    why = {LINES4[i]: (ok[i], "誤りの箇所の見落とし") for i in range(4) if i != where}
    info = {0: ("1行目（2乗の和ではなく，長さの和にした）", "formula", "「2辺から斜辺を求める」ことだけを覚えていて，2乗することを忘れた。"),
            1: (f"2行目（${a}^2$ を ${a}\\times2$ のように計算した）", "calculation", "累乗の計算で，2乗と2倍を取り違えた。"),
            2: ("3行目（根号の外に出す数を2乗のまま書いた）", "calculation", f"$\\sqrt{{{cc * cc}\\times{rad}}}$ の ${cc * cc}$ を，$\\sqrt{{{cc * cc}}}={cc}$ にせずに外に出した。")}[where]
    fix = f"AC$={cc}\\sqrt{{{rad}}}$ cm"
    return mc(f"〔問題〕${A('ABC')}=90^\\circ$ の直角三角形 ABC で，AB$={a}$ cm，BC$={b}$ cm のとき，辺 AC の長さを求めなさい。\n〔Kさんの解答〕\n{sol}\nKさんの解答で，誤りが最初に生じた行として最も適するものを，" + SEL4,
              LINES4, f"誤りが最初に生じたのは{LINES4[where]}。正しくは {fix}。", d=3, p=6, keep=True, ai=where, why=why, fig=rtri_fig(a, b),
              err=dict(sol=sol, step=info[0], type=info[1], tempt=info[2], fix=fix),
              ap="1行ずつ，三平方の定理の式・2乗の計算・根号の簡単にし方を自分で確かめる。",
              steps=["AC$^2=$AB$^2+$BC$^2$。", f"AC$^2={a * a}+{b * b}={n}$。", f"AC$=\\sqrt{{{n}}}={cc}\\sqrt{{{rad}}}$ cm。"],
              alt=[f"答えを2乗して ${n}$ にもどるかで確かめる。"],
              pc=[("誤りの行を正しく指摘している", 3), ("正しい長さを求めている", 3)],
              pit=["2乗と2倍を取り違える。", "根号の外に出す数を2乗のまま書く。"],
              chk=(f"sqrt({a}**2+{b}**2)", f"{cc}*sqrt({rad})", None, "intermediate"))


@gen("error_correction", 3, ["common_error", "concept"])
def d_space_err(r):
    kind = r.choice(["box", "ratio", "pyr"])
    if kind == "box":
        a, b, c = r.sample(range(1, 13), 3)
        good = a * a + b * b + c * c
        stem = f"〔問題〕直方体 ABCD-EFGH で，AB$={a}$ cm，BC$={b}$ cm，AE$={c}$ cm のとき，対角線 AG の長さを求めなさい。"
        sol = f"AG$^2=$AB$^2+$BC$^2={a}^2+{b}^2={a * a + b * b}$ なので，AG$={rtex(a * a + b * b)}$ cm"
        right = "求めたのは底面の対角線（AC または EG）の長さである。AG を求めるには高さ AE もふくめて，AG$^2=$AE$^2+$EG$^2$ とするべきである。"
        fix = f"AG$={rtex(good)}$ cm"
        chk = (f"sqrt({a}**2+{b}**2+{c}**2)", f"sqrt({good})")
        cands = [("AG$=$AB$+$BC$+$AE とするべきである。", "辺の長さの和ではなく，三平方の定理を2回使う。", "三平方の定理の誤解"),
                 ("Kさんの解答に誤りはない。", "AG は空間の対角線で，底面の対角線より長いはずである。", "検算不足"),
                 ("直方体の対角線には三平方の定理は使えない。", "直角三角形 AEG を取り出せば使える。", "定理の適用範囲の誤解"),
                 ("AG$^2=$AB$^2+$BC$^2-$AE$^2$ とするべきである。", "高さは引くのではなく，2乗してたす。", "式の立て方の誤解")]
        etype, tempt = "concept", "見取図で直角三角形を取り出すとき，平面（底面）の三角形だけを考えてしまう。"
    elif kind == "ratio":
        n = r.randint(2, 12)
        good = 3 * n * n
        stem = f"〔問題〕${A('ABC')}=90^\\circ$，${A('ACB')}=30^\\circ$ の直角三角形 ABC で，AB$={n}$ cm のとき，辺 BC の長さを求めなさい。"
        sol = f"$30^\\circ$・$60^\\circ$・$90^\\circ$ の直角三角形の辺の比は $1:2:\\sqrt{{3}}$ なので，AB：BC$=1:2$，BC$={2 * n}$ cm"
        right = f"$2$ にあたるのは斜辺 AC である。BC は $30^\\circ$ の角のとなりの辺で，AB：BC$=1:\\sqrt{{3}}$ になる。"
        fix = f"BC$={n}\\sqrt{{3}}$ cm"
        chk = (f"{n}*sqrt(3)", f"sqrt({good})")
        cands = [("辺の比は $1:1:\\sqrt{2}$ を使うべきである。", "$1:1:\\sqrt{2}$ は直角二等辺三角形の辺の比である。", "特別な直角三角形の混同"),
                 ("Kさんの解答に誤りはない。", "斜辺でない BC を，斜辺と同じ比 $2$ にあてはめている。", "検算不足"),
                 ("AB：BC$=\\sqrt{3}:1$ とするべきである。", "AB は $30^\\circ$ の角に向かい合う短い辺なので，比の $1$ にあたる。", "比の対応の誤解"),
                 ("$30^\\circ$ の直角三角形では三平方の定理は使えない。", "どんな直角三角形でも使える。辺の比は三平方の定理から導かれる。", "定理の適用範囲の誤解")]
        etype, tempt = "concept", "比 $1:2:\\sqrt{3}$ の数字の順番だけを覚えていて，どの辺に対応するかを確かめなかった。"
    else:
        a = r.choice(range(2, 13, 2))
        e = r.randint(a // 2 + 2, a + 8)
        good = Fr(e * e) - Fr(a * a, 2)
        bad = Fr(e * e) - Fr(a * a, 4)
        if good <= 0 or good == bad:
            raise AssertionError
        stem = f"〔問題〕底面が1辺 ${a}$ cm の正方形で，側面の辺の長さがすべて ${e}$ cm の正四角錐の高さを求めなさい。"
        sol = f"高さ$^2={e}^2-\\left({ftex(Fr(a, 2))}\\right)^2={ftex(bad)}$ なので，高さ$={rtex(bad)}$ cm"
        right = "頂点から底面にひいた垂線の足は底面の正方形の中心（対角線の交点）であり，側面の辺と組み合わせるのは底面の対角線の半分である。1辺の半分を使ったのが誤り。"
        fix = f"高さ$={rtex(good)}$ cm"
        chk = (f"sqrt({e}**2-Rational({a * a},2))", f"sqrt({fpy(good)})")
        cands = [("高さ$^2=$側面の辺$^2+$底面の1辺$^2$ とするべきである。", "高さは直角三角形の斜辺ではないので，2乗の和にはならない。", "斜辺の取り違え"),
                 ("Kさんの解答に誤りはない。", f"Kさんの式は側面の三角形の高さ（斜高）を求めたもので，立体の高さではない。", "検算不足"),
                 ("正四角錐の高さは側面の辺の長さと等しい。", "側面の辺は高さより長い（斜めに傾いている）。", "見取図の読み違い"),
                 ("底面の1辺の長さ全体を使うべきである。", "使うのは底面の対角線の半分である。", "直角三角形の取り違え")]
        etype, tempt = "concept", "側面の二等辺三角形の高さ（斜高）と，立体の高さを区別していない。"
    r.shuffle(cands)
    return _err_mc(stem, sol, right, cands, f"正しくは {fix}。", dict(sol=sol, step="直角三角形を取り出す（辺の比をあてはめる）部分", type=etype, tempt=tempt, fix=fix), d=3, p=6,
                   ap="求める線分を斜辺または1辺とする直角三角形がどれかを，見取図から正しく取り出す。辺の比を使うときは，比のどの数がどの辺に対応するかを確かめる。",
                   steps=["Kさんが使った直角三角形（辺の比）を確かめる。", "求める線分をふくむ正しい直角三角形を見つける。", f"正しくは {fix}。"],
                   alt=["求めた長さが図の中の他の長さと比べて自然か（斜辺がいちばん長いか）を確かめる。"],
                   pc=[("誤りの原因を正しく指摘している", 3), ("正しい長さを求めている", 3)],
                   pit=["平面の三角形だけで考え，高さをふくめ忘れる。", "辺の比の対応を取り違える。"],
                   chk=chk + (None, "intermediate"))


GENERATORS = [a_hyp, a_converse, a_special, a_distance, a_cuboid,
              b_isosceles, b_chord, b_pyramid, b_equation, b_shortest,
              c_xy, c_coord, c_space,
              d_hyp_err, d_lines_err, d_space_err]

GENERATORS = [_robust(g) for g in GENERATORS]
