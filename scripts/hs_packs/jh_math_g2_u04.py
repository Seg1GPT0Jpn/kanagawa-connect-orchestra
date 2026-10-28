"""単元パック：中学2年 図形の調べ方　平行と合同（神奈川県公立高校入試形式）。"""
import math
import re
import unicodedata
from fractions import Fraction as Fr

from banks._common import figure, mc, num
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, proof, summary, theorem, tp)

UNIT_ID = "JH-MATH-G2-U04"

PREREQUISITES = [
    ("JH-MATH-G1-U05", "直線・角の表し方（∠、//、⊥）と、図形の移動（平行移動・回転移動・対称移動）で重なる図形の見方。"),
    ("JH-MATH-G1-U03", "一次方程式を解けること。角の大きさを文字で表して方程式をつくるときに使う。"),
    ("JH-MATH-G2-U01", "文字式を使った説明のしかた。「仮定から結論を導く」証明の書き方の土台になる。"),
]
EXTENSIONS = [
    ("JH-MATH-G2-U05", "合同条件と証明の進め方を使い、二等辺三角形・平行四辺形の性質を証明する。"),
    ("JH-MATH-G3-U05", "合同条件から相似条件へ発展し、相似な図形の証明を行う。"),
    ("HS-MATHA-U02", "高校の図形の性質で、三角形の五心や円の性質を論証する。"),
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


SEL4 = "次の1〜4の中から1つ選び，その番号を答えなさい。"
_D = "一二三四五六七八九"


def kan(n):
    """漢数字（1〜99）。"""
    t, o = divmod(n, 10)
    s = ("" if t == 0 else ("十" if t == 1 else _D[t - 1] + "十"))
    return s + ("" if o == 0 else _D[o - 1])


def regname(n):
    return "正方形" if n == 4 else f"正{kan(n)}角形"


def ang(v):
    return f"${v}^\\circ$"


def A(s):
    """∠ABC の LaTeX。"""
    return f"\\angle\\mathrm{{{s}}}"


def M(s):
    return f"\\mathrm{{{s}}}"


def T(s):
    return f"\\triangle\\mathrm{{{s}}}"


# ----------------------------------------------------------------------
# 図（SVG）
# ----------------------------------------------------------------------

def _f(v):
    return f"{v:.1f}"


def geo(pts, segs=(), dashed=(), texts=(), arcs=(), dots=(), names=None, off=None, scale=26, pad=20, ticks=(), right=(), thick=()):
    """幾何の図。pts={名前: (x, y)}、segs=[("A","B"), ...]、texts=[(x, y, 文字)]（中央そろえ）、
    arcs=[(頂点名, 始角, 終角)]（度、反時計回り）、names=表示する頂点名（既定はすべて）、off={名前: (dx, dy)} ラベル位置の調整、
    ticks=[("A","B",本数)] 等しい長さの印、right=[("B","A","C")] 頂点 A の直角の印。"""
    names = list(pts) if names is None else list(names)
    xs = [p[0] for p in pts.values()] + [t[0] for t in texts]
    ys = [p[1] for p in pts.values()] + [t[1] for t in texts]
    minx, maxx, miny, maxy = min(xs) - 0.5, max(xs) + 0.5, min(ys) - 0.5, max(ys) + 0.5
    W, H = (maxx - minx) * scale + 2 * pad, (maxy - miny) * scale + 2 * pad
    X = lambda x: pad + (x - minx) * scale  # noqa: E731
    Y = lambda y: pad + (maxy - y) * scale  # noqa: E731
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {_f(W)} {_f(H)}" width="{_f(W)}" height="{_f(H)}" font-family="serif" font-size="12">']
    for a, b in segs:
        (ax, ay), (bx, by) = pts[a], pts[b]
        w = "1.6" if (a, b) in thick else "1.1"
        o.append(f'<line x1="{_f(X(ax))}" y1="{_f(Y(ay))}" x2="{_f(X(bx))}" y2="{_f(Y(by))}" stroke="#000" stroke-width="{w}"/>')
    for a, b in dashed:
        (ax, ay), (bx, by) = pts[a], pts[b]
        o.append(f'<line x1="{_f(X(ax))}" y1="{_f(Y(ay))}" x2="{_f(X(bx))}" y2="{_f(Y(by))}" stroke="#000" stroke-width="1" stroke-dasharray="4 3"/>')
    for v, t0, t1 in arcs:
        vx, vy = pts[v]
        r = 11
        t0r, t1r = math.radians(t0), math.radians(t1)
        x0, y0 = X(vx) + r * math.cos(t0r), Y(vy) - r * math.sin(t0r)
        x1, y1 = X(vx) + r * math.cos(t1r), Y(vy) - r * math.sin(t1r)
        large = 1 if (t1 - t0) % 360 > 180 else 0
        o.append(f'<path d="M{_f(x0)},{_f(y0)} A{r},{r} 0 {large} 0 {_f(x1)},{_f(y1)}" fill="none" stroke="#000" stroke-width="0.8"/>')
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
        o.append(f'<text x="{_f(lx)}" y="{_f(ly + 4)}" text-anchor="middle">{nm}</text>')
    for x, y, t in texts:
        o.append(f'<text x="{_f(X(x))}" y="{_f(Y(y) + 4)}" text-anchor="middle" font-size="11">{t}</text>')
    o.append("</svg>")
    return "".join(o)


POS = {"UR": (0, "θ"), "UL": (1, "180−θ"), "LL": (0, "θ"), "LR": (1, "180−θ")}
POS_JP = {"UR": "右上", "UL": "左上", "LL": "左下", "LR": "右下"}


def _pos_span(pos, th):
    return {"UR": (0, th), "UL": (th, 180), "LL": (180, 180 + th), "LR": (180 + th, 360)}[pos]


def parallel_fig(th, marks, alt="平行な2直線 ℓ，m と，それらに交わる直線"):
    """ℓ（上）と m（下）が平行で、直線が角 th（ℓ の右向きとなす角）で交わる図。marks=[("P"|"Q", 位置, 文字)]。"""
    t = math.radians(th)
    d = (math.cos(t), math.sin(t))
    h = 2.6
    qx = -h * d[0] / d[1]
    lo, hi = min(0, qx) - 2.6, max(0, qx) + 2.6
    pts = {"P": (0, 0), "Q": (qx, -h), "l0": (lo, 0), "l1": (hi, 0), "m0": (lo, -h), "m1": (hi, -h),
           "t0": (1.3 * d[0], 1.3 * d[1]), "t1": (qx - 1.3 * d[0], -h - 1.3 * d[1])}
    texts = [(hi + 0.35, 0.05, "ℓ"), (hi + 0.35, -h + 0.05, "m")]
    arcs = []
    for v, pos, lab in marks:
        a0, a1 = _pos_span(pos, th)
        mid = math.radians((a0 + a1) / 2)
        vx, vy = pts[v]
        rr = (0.95 if (a1 - a0) < 50 else 0.75) + 0.07 * max(0, len(lab) - 3)
        texts.append((vx + rr * math.cos(mid), vy + rr * math.sin(mid), lab))
        arcs.append((v, a0, a1))
    return figure(alt, geo(pts, segs=[("l0", "l1"), ("m0", "m1"), ("t0", "t1")], texts=texts, arcs=arcs, names=["P", "Q"],
                           off={"P": (-0.45 if th < 90 else 0.45, 0.3), "Q": (0.45 if th < 90 else -0.45, -0.3)}, scale=30))


def bent_fig(a, b, la, lb, lx, a_left=False):
    """ℓ//m の間で折れ曲がった線（くの字）。A は ℓ 上、B は m 上、P は折れ曲がりの点。"""
    h = 4.0
    P = (0.0, -2.0)
    Ax = P[0] - 2.0 / math.tan(math.radians(a))
    Bx = P[0] - 2.0 / math.tan(math.radians(b))
    lo, hi = min(Ax, Bx) - 1.8, max(0.0, Ax, Bx) + 1.6
    pts = {"A": (Ax, 0), "B": (Bx, -h), "P": P, "l0": (lo, 0), "l1": (hi, 0), "m0": (lo, -h), "m1": (hi, -h)}
    texts = [(hi + 0.35, 0.05, "ℓ"), (hi + 0.35, -h + 0.05, "m")]
    if a_left:
        arcs = [("A", 180, 360 - a), ("B", 0, b)]
        mid_a = math.radians((180 + 360 - a) / 2)
        texts.append((Ax + 0.95 * math.cos(mid_a), 0.95 * math.sin(mid_a), la))
    else:
        arcs = [("A", 360 - a, 360), ("B", 0, b)]
        texts.append((Ax + 1.15 * math.cos(math.radians(-a / 2)), 1.15 * math.sin(math.radians(-a / 2)), la))
    texts.append((Bx + 1.15 * math.cos(math.radians(b / 2)), -h + 1.15 * math.sin(math.radians(b / 2)), lb))
    ta = math.degrees(math.atan2(0 - P[1], Ax - P[0]))
    tb = math.degrees(math.atan2(-h - P[1], Bx - P[0])) % 360
    arcs.append(("P", ta, tb))
    mid = math.radians((ta + tb) / 2)
    texts.append((P[0] + 0.85 * math.cos(mid), P[1] + 0.85 * math.sin(mid), lx))
    return figure("平行な2直線 ℓ，m の間で折れ曲がった線", geo(pts, segs=[("l0", "l1"), ("m0", "m1"), ("A", "P"), ("P", "B")], texts=texts, arcs=arcs,
                                                     names=["A", "B", "P"], off={"A": (0, 0.4), "B": (0, -0.45), "P": (0.4, 0)}, scale=28))


# ----------------------------------------------------------------------
# 授業プリント
# ----------------------------------------------------------------------

LESSON = lesson(
    goals=["平行線の同位角・錯角の性質と平行線になるための条件を理解し、角の大きさを根拠を示して求められる。",
           "三角形の内角・外角の性質と多角形の内角の和・外角の和を、平行線の性質から導いて使える。",
           "三角形の合同条件を理解し、仮定と結論を区別して、根拠を示しながら証明を書ける。"],
    duration=100,
    readiness=["対頂角が等しいこと、一直線の角が $180^\\circ$ であることを知っている。",
               "三角形の内角の和が $180^\\circ$ であることを小学校で学んでいる（ここでは理由を説明できるようにする）。",
               "合同な図形（ぴったり重なる図形）の意味と、対応する頂点・辺・角を答えられる。"],
    flow=[("導入：なぜ $180^\\circ$ といえるのか", 10, "小学校での「切って集める」確かめ方と、どんな三角形でも成り立つと言える理由の違いを考える"),
          ("平行線と角", 20, "同位角・錯角、平行線の性質と平行線になるための条件（例題1）"),
          ("三角形と多角形の角", 20, "内角の和・外角の性質の証明、多角形の内角の和 $180^\\circ\\times(n-2)$ と外角の和 $360^\\circ$（例題2）"),
          ("合同条件", 20, "3つの合同条件、合同条件にならない例（2辺と間でない角、3つの角）"),
          ("証明の進め方", 20, "仮定と結論、根拠になることがら、証明の書き方（例題3）"),
          ("まとめと確認", 10, "確認問題と問題プリントの指示")],
    sections=[
        intro("in1", "「いつでも成り立つ」と言うために",
              "小学校では、三角形の3つの角を切り取って並べると一直線になることから、内角の和が $180^\\circ$ になることを確かめた。しかし、それはいくつかの三角形で確かめただけである。この単元では、すでに正しいとわかっていることがら（平行線の性質など）を根拠にして、どんな三角形でも成り立つことを説明する方法――証明――を学ぶ。",
              bullets=["根拠となることがら：対頂角は等しい、平行線の同位角・錯角は等しい、など。", "根拠を順につないで、仮定から結論を導くのが証明である。"],
              points=[tp("いろいろな形の三角形の角を切って並べる活動を短く行い、「何個確かめれば全部と言えるか」を問う。", ask="1000個の三角形で確かめたら、すべての三角形で成り立つと言えるか。", expect="言えない。まだ確かめていない三角形があるから。", timing="導入")]),
        definition("df1", "同位角・錯角と平行線",
                   "2直線 ℓ、m に1つの直線が交わってできる角のうち、同じ位置にある角を同位角、ℓ と m の間で交わる直線の反対側にある角を錯角という。",
                   conditions=["平行線の性質：2直線が平行ならば、同位角は等しく、錯角も等しい。",
                               "平行線になるための条件：同位角が等しければ（または錯角が等しければ）、2直線は平行である。",
                               "2直線が平行のとき、ℓ と m の間で交わる直線の同じ側にある2つの角（同側内角）の和は $180^\\circ$。"],
                   points=[tp("同位角・錯角は「位置関係の名前」であり、等しいとは限らないことを強調する。等しいのは2直線が平行なときだけ。", caution="「錯角は等しい」とだけ覚えて、平行でない場合にも使う誤りが多い。")]),
        theorem("th1", "三角形の内角と外角",
                "$$\\angle\\mathrm{A}+\\angle\\mathrm{B}+\\angle\\mathrm{C}=180^\\circ\\qquad \\angle\\mathrm{ACD}=\\angle\\mathrm{A}+\\angle\\mathrm{B}$$",
                ["三角形の3つの内角の和は $180^\\circ$。", "三角形の1つの外角は、それととなり合わない2つの内角の和に等しい（$\\mathrm{D}$ は辺 BC を C の方に延長した直線上の点）。"],
                proof=["$\\triangle\\mathrm{ABC}$ の辺 BC を延長した直線上に点 D をとり、C を通り辺 BA に平行な直線 CE をひく。",
                       "$\\mathrm{BA}\\parallel\\mathrm{CE}$ で、錯角は等しいから $\\angle\\mathrm{BAC}=\\angle\\mathrm{ACE}$。",
                       "同位角は等しいから $\\angle\\mathrm{ABC}=\\angle\\mathrm{ECD}$。",
                       "よって $\\angle\\mathrm{A}+\\angle\\mathrm{B}=\\angle\\mathrm{ACE}+\\angle\\mathrm{ECD}=\\angle\\mathrm{ACD}$（外角の性質）。",
                       "さらに $\\angle\\mathrm{ACB}+\\angle\\mathrm{ACD}=180^\\circ$（一直線）なので、$\\angle\\mathrm{A}+\\angle\\mathrm{B}+\\angle\\mathrm{C}=180^\\circ$。"],
                points=[tp("証明の各行に「なぜそう言えるか（根拠）」を必ず添えさせる。根拠に使ってよいのは、すでに正しいと認められたことがらだけであることを確認する。", ask="この証明で根拠にしたことがらは何か。", expect="平行線の錯角・同位角は等しいこと、一直線の角は $180^\\circ$ であること。")]),
        derivation("dv1", "多角形の内角の和・外角の和を導く",
                   ["$n$ 角形の1つの頂点から対角線をひくと、$n-3$ 本の対角線で $(n-2)$ 個の三角形に分けられる。",
                    "それぞれの三角形の内角の和は $180^\\circ$ なので、$n$ 角形の内角の和は $180^\\circ\\times(n-2)$。",
                    "各頂点で、内角と外角の和は $180^\\circ$（一直線）。頂点は $n$ 個あるので、内角の和と外角の和を合わせると $180^\\circ\\times n$。",
                    "外角の和 $=180^\\circ\\times n-180^\\circ\\times(n-2)=360^\\circ$。$n$ に関係なく $360^\\circ$ である。",
                    "正 $n$ 角形では、1つの外角は $360^\\circ\\div n$、1つの内角は $180^\\circ-360^\\circ\\div n$。"],
                   points=[tp("五角形・六角形で三角形に分ける図をかかせ、三角形の数が「辺の数 − 2」になる理由を説明させる。", caution="内部の1点から各頂点に線をひく方法では三角形が $n$ 個でき、中心のまわりの $360^\\circ$ を引く必要がある。どちらの方法でも同じ式になることを確かめさせるとよい。")]),
        definition("df2", "三角形の合同条件",
                   "2つの三角形は、次のどれかが成り立つとき合同である。",
                   formula="$$\\begin{aligned}&\\text{① 3組の辺がそれぞれ等しい}\\\\&\\text{② 2組の辺とその間の角がそれぞれ等しい}\\\\&\\text{③ 1組の辺とその両端の角がそれぞれ等しい}\\end{aligned}$$",
                   conditions=["合同を記号 $\\equiv$ で表し、対応する頂点を同じ順に書く（$\\triangle\\mathrm{ABC}\\equiv\\triangle\\mathrm{DEF}$）。",
                               "2組の辺と「間でない角」が等しくても、合同とは限らない。",
                               "3つの角がそれぞれ等しくても、大きさの異なる三角形があるので合同とは限らない。"],
                   points=[tp("②で「間の角」でない場合に2通りの三角形がかけることを、コンパスで作図して見せる。", ask="AB $=5$ cm、BC $=4$ cm、$\\angle\\mathrm{A}=40^\\circ$ の三角形は1通りに決まるか。", expect="決まらない。C の位置が2通りある。", timing="合同条件の説明の後")]),
        proof("pf1", "証明の進め方（仮定と結論）",
              ["「○○ならば□□」の○○の部分を仮定、□□の部分を結論という。",
               "証明では、仮定から出発し、根拠となることがら（定義・定理・対頂角・平行線の性質・合同条件など）を使って結論を導く。",
               "合同を使う証明の流れ：①どの三角形とどの三角形の合同を示すか決める → ②等しい辺や角を、根拠とともに3つ示す → ③合同条件を書いて合同を示す → ④合同な図形の対応する辺（角）は等しいことから結論を導く。",
               "「○○ならば□□」の仮定と結論を入れかえたものを、もとのことがらの逆という。あることがらが正しくても、その逆が正しいとは限らない。"],
              points=[tp("例題3の証明で、どの行が「仮定」から、どの行が「すでに知っていること」から言えるかを色分けさせる。")]),
        example("ex1", "例題1　平行線と角",
                "右の図で、ℓ$\\parallel$m のとき、$\\angle x$ の大きさを求めなさい。",
                ["点 P を通り ℓ に平行な直線をひく。", "ℓ との間の錯角から、上側の角は $40^\\circ$。", "m との間の錯角から、下側の角は $35^\\circ$。", "$\\angle x=40^\\circ+35^\\circ=75^\\circ$。"],
                "$75^\\circ$",
                thinking="折れ曲がった点を通る平行線をひくと、錯角が2つ見つかる。",
                figure=bent_fig(40, 35, "40°", "35°", "x"),
                points=[tp("補助線をひく理由（錯角・同位角が使える形をつくる）を言葉で説明させる。")],
                misconceptions=[("$\\angle x=180^\\circ-(40^\\circ+35^\\circ)$ とする", "P を通る平行線で分けた2つの角の和が $\\angle x$")]),
        example("ex2", "例題2　多角形の角",
                "正九角形の1つの内角の大きさを求めなさい。",
                ["外角の和は $360^\\circ$ なので、1つの外角は $360^\\circ\\div9=40^\\circ$。", "1つの内角は $180^\\circ-40^\\circ=140^\\circ$。", "（別解）内角の和 $180^\\circ\\times(9-2)=1260^\\circ$ を $9$ でわって $140^\\circ$。"],
                "$140^\\circ$",
                thinking="正多角形では、外角から求めると計算が簡単になる。"),
        example("ex3", "例題3　合同を使った証明",
                "線分 AB と CD が点 O で交わり、AO $=$ BO、CO $=$ DO である。このとき、AC $=$ BD であることを証明しなさい。",
                ["$\\triangle\\mathrm{AOC}$ と $\\triangle\\mathrm{BOD}$ において、", "仮定から AO $=$ BO ……①、CO $=$ DO ……②",
                 "対頂角は等しいから $\\angle\\mathrm{AOC}=\\angle\\mathrm{BOD}$ ……③",
                 "①、②、③から、2組の辺とその間の角がそれぞれ等しいので $\\triangle\\mathrm{AOC}\\equiv\\triangle\\mathrm{BOD}$",
                 "合同な図形の対応する辺は等しいので AC $=$ BD"],
                "上の証明のとおり",
                thinking="結論 AC $=$ BD をふくむ2つの三角形を探す。仮定の2組の辺の「間の角」が等しいことを言えれば合同条件がそろう。",
                figure=figure("線分 AB と CD が点 O で交わる図", geo({"A": (-3, 1.6), "B": (3, -1.6), "C": (-2.2, -1.8), "D": (2.2, 1.8), "O": (0, 0)},
                                                             segs=[("A", "B"), ("C", "D"), ("A", "C"), ("B", "D")], off={"O": (0.45, -0.1)})),
                points=[tp("証明の1行目「〜と〜において」を必ず書かせ、どの三角形の話かを明確にさせる。", caution="合同条件を書かずに「よって合同」とする答案が多い。")]),
        board("bd1", "板書案",
              [("① 平行線と角", ["同位角・錯角（位置の名前）", "ℓ$\\parallel$m ⇔ 同位角が等しい", "ℓ$\\parallel$m ⇔ 錯角が等しい", "くの字：平行線をひいて錯角"]),
               ("② 多角形の角", ["三角形の内角の和 $180^\\circ$", "外角 ＝ となり合わない2内角の和", "$n$ 角形の内角の和 $180^\\circ(n-2)$", "外角の和はいつも $360^\\circ$"]),
               ("③ 合同と証明", ["3辺／2辺と間の角／1辺と両端の角", "仮定 ⇒（根拠）⇒ 結論", "合同 → 対応する辺・角が等しい", "逆はいつも正しいとは限らない"])],
              points=[tp("③では、証明の型（〜において／仮定から／根拠／合同条件／結論）を枠で示して板書する。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("角を求める問題でも「なぜその角が等しいか（同位角・錯角・対頂角）」を一言添えさせると、証明の練習になる。"),
               tp("多角形の内角の和の公式は、丸暗記ではなく「三角形に分ける図」とセットで思い出させる。", ask="十角形の内角の和を、公式を使わずに説明できるか。", expect="1つの頂点から対角線をひくと三角形が8個できるので $180^\\circ\\times8$。"),
               tp("合同条件の「間の角」「両端の角」を、図に印をつけて確認させる。", caution="辺と角の対応がずれていても合同と書いてしまう誤りが多い。"),
               tp("仮定と結論の区別、逆の意味を、数や身近なことがらの例でも確かめさせる。", timing="証明の進め方の最後")],
              misconceptions=[("$n$ 角形の内角の和は $180^\\circ\\times n$", "三角形は $(n-2)$ 個なので $180^\\circ\\times(n-2)$"),
                              ("錯角はいつでも等しい", "等しいのは2直線が平行なときだけ"),
                              ("2組の辺と1つの角が等しければ合同", "その角が2組の辺の間の角でなければならない")]),
        summary("sm1", "まとめ",
                ["平行線の同位角・錯角は等しい。逆に、同位角や錯角が等しければ2直線は平行。", "三角形の内角の和は $180^\\circ$、外角はとなり合わない2内角の和。",
                 "$n$ 角形の内角の和 $180^\\circ\\times(n-2)$、外角の和 $360^\\circ$。", "三角形の合同条件は3つ。証明は仮定から根拠をつないで結論を導く。"]),
        check("ck1", "確認問題",
              [("十二角形の内角の和を求めなさい。", "$180^\\circ\\times10=1800^\\circ$"),
               ("1つの外角が $24^\\circ$ の正多角形は正何角形か。", "$360\\div24=15$ より正十五角形"),
               ("「$\\triangle\\mathrm{ABC}\\equiv\\triangle\\mathrm{DEF}$ ならば $\\angle\\mathrm{A}=\\angle\\mathrm{D}$」の仮定と結論を答えなさい。", "仮定：$\\triangle\\mathrm{ABC}\\equiv\\triangle\\mathrm{DEF}$、結論：$\\angle\\mathrm{A}=\\angle\\mathrm{D}$")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

REG = [5, 6, 8, 9, 10, 12, 15, 18, 20, 24, 30, 36]


@gen("basic_check", 5, ["computation"])
def a_polygon_sum(r):
    kind = r.choice(["sum", "ext", "int", "from_ext"])
    if kind == "sum":
        n = r.randint(5, 20)
        v = 180 * (n - 2)
        return MARK(f"{kan(n)}角形の内角の和は何度か，求めなさい。", v, f"1つの頂点から対角線をひくと三角形が ${n - 2}$ 個できるので，$180^\\circ\\times{n - 2}={v}^\\circ$。", f"180*({n}-2)", d=1,
                    ap="$n$ 角形は、1つの頂点からひいた対角線で $(n-2)$ 個の三角形に分けられる。",
                    steps=[f"三角形の数：${n}-2={n - 2}$ 個。", f"内角の和：$180^\\circ\\times{n - 2}={v}^\\circ$。"],
                    alt=[f"内部の1点と各頂点を結ぶと三角形が ${n}$ 個でき，$180^\\circ\\times{n}-360^\\circ={v}^\\circ$ としても求められる。"],
                    pc=[("三角形の個数を正しくとらえている", 1), ("内角の和を正しく求めている", 1)],
                    pit=["$180^\\circ\\times n$ としてしまう。"])
    n = r.choice(REG)
    e = 360 // n
    if kind == "ext":
        return MARK(f"正{kan(n)}角形の1つの外角の大きさは何度か，求めなさい。", e, f"外角の和は $360^\\circ$ なので $360^\\circ\\div{n}={e}^\\circ$。", f"360/{n}", d=1,
                    ap="多角形の外角の和は、何角形でも $360^\\circ$。正多角形では外角がすべて等しい。",
                    steps=["外角の和は $360^\\circ$。", f"$360^\\circ\\div{n}={e}^\\circ$。"],
                    alt=[f"1つの内角 $180^\\circ\\times{n - 2}\\div{n}={180 - e}^\\circ$ を求め，$180^\\circ$ から引いても求められる。"],
                    pc=[("外角の和が $360^\\circ$ であることを使っている", 1), ("正しく計算している", 1)],
                    pit=["内角の和を $n$ でわってしまう。"])
    if kind == "int":
        return MARK(f"正{kan(n)}角形の1つの内角の大きさは何度か，求めなさい。", 180 - e, f"1つの外角は $360^\\circ\\div{n}={e}^\\circ$ なので，内角は $180^\\circ-{e}^\\circ={180 - e}^\\circ$。", f"180-360/{n}", d=2,
                    ap="正多角形の1つの内角は、外角から求めると簡単。内角と外角の和は $180^\\circ$。",
                    steps=[f"1つの外角：$360^\\circ\\div{n}={e}^\\circ$。", f"1つの内角：$180^\\circ-{e}^\\circ={180 - e}^\\circ$。"],
                    alt=[f"内角の和 $180^\\circ\\times{n - 2}={180 * (n - 2)}^\\circ$ を ${n}$ でわっても ${180 - e}^\\circ$。"],
                    pc=[("外角（または内角の和）を正しく求めている", 1), ("1つの内角を正しく求めている", 1)],
                    pit=["外角を答えてしまう。"])
    return MARK(f"1つの外角の大きさが ${e}^\\circ$ である正多角形は，正何角形か。その数を答えなさい。", n, f"外角の和 $360^\\circ$ を ${e}^\\circ$ でわって ${n}$。正{kan(n)}角形。", f"360/{e}", d=2,
                ap="正多角形の外角はすべて等しく、その和は $360^\\circ$。外角がいくつあるか（＝頂点の数）を求める。",
                steps=["外角の和は $360^\\circ$。", f"$360\\div{e}={n}$。", f"正{kan(n)}角形。"],
                alt=[f"1つの内角は ${180 - e}^\\circ$。正 $n$ 角形の内角の式 $\\dfrac{{180(n-2)}}{{n}}={180 - e}$ を解いても $n={n}$。"],
                pc=[("外角の和を使っている", 1), ("正しい数を求めている", 1)],
                pit=["$180\\div e$ としてしまう。"])


def _relname(p, q):
    if p == q:
        return "同位角", "ℓ//m より，同位角は等しい"
    if (p, q) in (("LR", "UL"), ("LL", "UR")):
        return "錯角", "ℓ//m より，錯角は等しい"
    if (p, q) in (("LL", "UL"), ("LR", "UR")):
        return "同側内角", "ℓ//m より，ℓ と m の間で同じ側にある2つの角の和は $180^\\circ$"
    return "対頂角と同位角", "対頂角は等しく，ℓ//m より同位角も等しい"


@gen("basic_check", 5, ["concept", "condition_check"])
def a_parallel_angle(r):
    th = r.choice([x for x in range(35, 146, 5) if x != 90])
    p, q = r.choice(list(POS)), r.choice(list(POS))
    a = th if POS[p][0] == 0 else 180 - th
    x = th if POS[q][0] == 0 else 180 - th
    name, reason = _relname(p, q)
    fig = parallel_fig(th, [("P", p, f"{a}°"), ("Q", q, "x")])
    if name == "同側内角":
        st = [f"$\\angle x$ と ${a}^\\circ$ の角は ℓ と m の間で同じ側にある。", "ℓ//m のとき，その2つの角の和は $180^\\circ$。", f"$\\angle x=180^\\circ-{a}^\\circ={x}^\\circ$。"]
    elif name == "対頂角と同位角":
        st = [f"${a}^\\circ$ の角の対頂角，またはとなりの角（和が $180^\\circ$）を考え，$\\angle x$ の同位角の大きさを求める。", "ℓ//m より同位角は等しい。", f"$\\angle x={x}^\\circ$。"]
    else:
        st = [f"$\\angle x$ と ${a}^\\circ$ の角は{name}の位置にある。", f"{reason}。", f"$\\angle x={x}^\\circ$。"]
    return MARK(f"右の図のように，平行な2直線 ℓ，m に1つの直線が交わり，ℓ との交点を P，m との交点を Q とする。点 P の{POS_JP[p]}にできる角の大きさが ${a}^\\circ$ のとき，点 Q の{POS_JP[q]}にできる角 $\\angle x$ の大きさは何度か，求めなさい。", x, f"{reason}ことなどから，$\\angle x={x}^\\circ$。", f"{x}", d=1, fig=fig,
                ap="平行な2直線に1つの直線が交わるとき、同位角・錯角は等しい。一直線の角 $180^\\circ$ や対頂角も組み合わせて考える。",
                steps=st,
                alt=["2つの交点のまわりの8つの角は、大きさが2種類（和が $180^\\circ$）しかないことを使って、どちらの種類かを判断してもよい。"],
                pc=[("等しい角（または和が $180^\\circ$ の角）を正しく見つけている", 1), ("正しい大きさを求めている", 1)],
                pit=["同側内角を「等しい」と考えてしまう。"])


@gen("basic_check", 5, ["computation", "concept"])
def a_triangle_angle(r):
    kind = r.choice(["ext", "inner_from_ext", "third", "right"])
    if kind == "ext":
        a, b = r.randint(25, 85), r.randint(25, 85)
        v = a + b
        stem = f"$\\triangle\\mathrm{{ABC}}$ で，${A('A')}={a}^\\circ$，${A('B')}={b}^\\circ$ である。辺 BC を C の方に延長した直線上に点 D をとるとき，${A('ACD')}$ の大きさは何度か，求めなさい。"
        e = f"外角は，となり合わない2つの内角の和なので ${a}^\\circ+{b}^\\circ={v}^\\circ$。"
        st = [f"${A('ACD')}$ は頂点 C における外角。", "外角＝となり合わない2つの内角の和。", f"${a}^\\circ+{b}^\\circ={v}^\\circ$。"]
        alt = [f"${A('ACB')}=180^\\circ-{a}^\\circ-{b}^\\circ={180 - a - b}^\\circ$ を求め，$180^\\circ$ から引いても ${v}^\\circ$。"]
        expr = f"{a}+{b}"
    elif kind == "inner_from_ext":
        a = r.randint(25, 80)
        v = r.randint(25, 80)
        ext = a + v
        stem = f"$\\triangle\\mathrm{{ABC}}$ の辺 BC を C の方に延長した直線上に点 D をとる。${A('BAC')}={a}^\\circ$，${A('ACD')}={ext}^\\circ$ のとき，${A('ABC')}$ の大きさは何度か，求めなさい。"
        e = f"外角 ${A('ACD')}={A('BAC')}+{A('ABC')}$ なので，${A('ABC')}={ext}^\\circ-{a}^\\circ={v}^\\circ$。"
        st = [f"${A('ACD')}$ は頂点 C の外角で，${A('BAC')}+{A('ABC')}$ に等しい。", f"${ext}={a}+{A('ABC')}$。", f"${A('ABC')}={v}^\\circ$。"]
        alt = [f"${A('ACB')}=180^\\circ-{ext}^\\circ={180 - ext}^\\circ$ を求め，内角の和から ${A('ABC')}=180^\\circ-{a}^\\circ-{180 - ext}^\\circ={v}^\\circ$。"]
        expr = f"{ext}-{a}"
    elif kind == "third":
        a, b = r.randint(20, 100), r.randint(20, 60)
        v = 180 - a - b
        stem = f"$\\triangle\\mathrm{{PQR}}$ で，${A('P')}={a}^\\circ$，${A('Q')}={b}^\\circ$ のとき，${A('R')}$ の大きさは何度か，求めなさい。"
        e = f"内角の和は $180^\\circ$ なので $180^\\circ-{a}^\\circ-{b}^\\circ={v}^\\circ$。"
        st = ["三角形の内角の和は $180^\\circ$。", f"$180^\\circ-({a}^\\circ+{b}^\\circ)={v}^\\circ$。"]
        alt = [f"頂点 R の外角は ${a}^\\circ+{b}^\\circ={a + b}^\\circ$ なので，$180^\\circ-{a + b}^\\circ={v}^\\circ$。"]
        expr = f"180-{a}-{b}"
    else:
        a = r.randint(15, 75)
        v = 90 - a
        stem = f"${A('C')}=90^\\circ$ の直角三角形 ABC で，${A('A')}={a}^\\circ$ のとき，${A('B')}$ の大きさは何度か，求めなさい。"
        e = f"直角三角形の2つの鋭角の和は $90^\\circ$ なので $90^\\circ-{a}^\\circ={v}^\\circ$。"
        st = ["内角の和 $180^\\circ$ から直角 $90^\\circ$ を引くと，残りの2つの角の和は $90^\\circ$。", f"$90^\\circ-{a}^\\circ={v}^\\circ$。"]
        alt = [f"$180^\\circ-90^\\circ-{a}^\\circ={v}^\\circ$ と直接計算してもよい。"]
        expr = f"90-{a}"
    return MARK(stem, v, e, expr, d=1,
                ap="三角形の内角の和は $180^\\circ$。外角は、それととなり合わない2つの内角の和に等しい。",
                steps=st, alt=alt,
                pc=[("内角の和・外角の性質を正しく使っている", 1), ("正しい大きさを求めている", 1)],
                pit=["外角を、となり合う内角との和と取り違える。"])


def _tri_sets(r):
    """△ABC と △DEF（A↔D，B↔E，C↔F）について、合同条件になる組と、ならない組を作る。"""
    V = ["A", "B", "C"]
    W = {"A": "D", "B": "E", "C": "F"}
    i = r.randrange(3)
    X, Y, Z = V[i], V[(i + 1) % 3], V[(i + 2) % 3]

    def side(p, q):
        a, b = "".join(sorted(p + q)), "".join(sorted(W[p] + W[q]))
        return f"$\\mathrm{{{a}}}=\\mathrm{{{b}}}$"

    def angle(p):
        return f"${A(p)}={A(W[p])}$"
    good = {
        "3組の辺がそれぞれ等しい": f"{side(X, Y)}，{side(Y, Z)}，{side(Z, X)}",
        "2組の辺とその間の角がそれぞれ等しい": f"{side(X, Y)}，{side(Y, Z)}，{angle(Y)}",
        "1組の辺とその両端の角がそれぞれ等しい": f"{side(X, Y)}，{angle(X)}，{angle(Y)}",
    }
    bad = [
        (f"{side(X, Y)}，{side(Y, Z)}，{angle(X)}", "等しい角が，等しい2組の辺の間の角ではない。この条件では三角形が1通りに決まらない。", "合同条件の「間の角」の見落とし"),
        (f"{side(X, Y)}，{side(Y, Z)}，{angle(Z)}", "等しい角が，等しい2組の辺の間の角ではない。", "合同条件の「間の角」の見落とし"),
        (f"{angle(X)}，{angle(Y)}，{angle(Z)}", "3つの角が等しくても，大きさの異なる三角形がある。", "形が同じなら合同という誤解"),
        (f"{side(X, Y)}，{side(Y, Z)}", "条件が2つしかなく，三角形が1通りに決まらない。", "条件の不足"),
        (f"{side(X, Y)}，{angle(X)}", "条件が2つしかなく，三角形が1通りに決まらない。", "条件の不足"),
    ]
    return good, bad


COND_NAMES = ["3組の辺がそれぞれ等しい", "2組の辺とその間の角がそれぞれ等しい", "1組の辺とその両端の角がそれぞれ等しい"]


@gen("basic_check", 5, ["condition_check", "concept"])
def a_congruence_cond(r):
    good, bad = _tri_sets(r)
    cname = r.choice(COND_NAMES)
    if r.random() < 0.6:
        r.shuffle(bad)
        return MC("$\\triangle\\mathrm{ABC}$ と $\\triangle\\mathrm{DEF}$ で，次の条件が成り立つとき，いつでも $\\triangle\\mathrm{ABC}\\equiv\\triangle\\mathrm{DEF}$ であるといえるものとして最も適するものを，" + SEL4,
                  good[cname], bad, f"この条件は「{cname}」という合同条件にあてはまる。", d=2,
                  ap="3つの合同条件（3組の辺／2組の辺とその間の角／1組の辺とその両端の角）のどれかにあてはまるかを、辺と角の位置関係に注意して調べる。",
                  steps=["それぞれの条件で、等しい辺と角の位置を図にかきこむ。", "角が「2辺の間」または「1辺の両端」にあるかを確かめる。", f"正答の条件は「{cname}」にあてはまる。"],
                  alt=["条件どおりに三角形を作図して、1通りに決まるかどうかで判断してもよい。"],
                  pc=[("合同条件を正しく思い出している", 1), ("辺と角の位置関係を正しく判断している", 1)],
                  pit=["2組の辺と「間でない角」が等しいだけで合同と判断する。", "3つの角が等しければ合同と考える。"])
    others = [c for c in COND_NAMES if c != cname]
    cands = [(o, f"与えられた条件は「{o}」の形になっていない。", "合同条件の取り違え") for o in others]
    cands.append(("2組の角がそれぞれ等しい", "角だけが等しい条件は合同条件ではない（大きさが決まらない）。", "合同条件の誤解"))
    return MC(f"$\\triangle\\mathrm{{ABC}}$ と $\\triangle\\mathrm{{DEF}}$ で，{good[cname]} が成り立つ。このとき $\\triangle\\mathrm{{ABC}}\\equiv\\triangle\\mathrm{{DEF}}$ であるといえる根拠となる合同条件として最も適するものを，" + SEL4,
              cname, cands, f"「{cname}」が成り立つので合同である。", d=2,
              ap="等しい辺と角を図にかきこみ、角が辺の「間」にあるのか「両端」にあるのかを確かめる。",
              steps=["等しい辺・角を書き出す。", "辺と角の位置関係を図で確認する。", f"「{cname}」にあてはまる。"],
              alt=["条件の中の辺の数と角の数（辺3つ／辺2つと角1つ／辺1つと角2つ）で、まず候補をしぼる。"],
              pc=[("等しい辺と角の位置関係をとらえている", 1), ("正しい合同条件を選んでいる", 1)],
              pit=["「間の角」と「両端の角」を取り違える。"])


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 4, ["application", "multiple_solutions"])
def b_bent(r):
    a, b = r.randint(25, 65), r.randint(25, 65)
    kind = r.choice(["x", "x_supp", "find_b"])
    if kind == "x":
        fig = bent_fig(a, b, f"{a}°", f"{b}°", "x")
        v = a + b
        stem = f"右の図で，ℓ//m である。図の角の大きさが ${a}^\\circ$，${b}^\\circ$ のとき，$\\angle x$ の大きさは何度か，求めなさい。"
        st = ["点 P を通り ℓ に平行な直線 n をひく。", f"ℓ//n より錯角は等しいので，上側の角は ${a}^\\circ$。", f"n//m より錯角は等しいので，下側の角は ${b}^\\circ$。", f"$\\angle x={a}^\\circ+{b}^\\circ={v}^\\circ$。"]
        expr = f"{a}+{b}"
    elif kind == "x_supp":
        fig = bent_fig(a, b, f"{180 - a}°", f"{b}°", "x", a_left=True)
        v = a + b
        stem = f"右の図で，ℓ//m である。図の角の大きさが ${180 - a}^\\circ$，${b}^\\circ$ のとき，$\\angle x$ の大きさは何度か，求めなさい。"
        st = [f"点 A で，ℓ の右側の部分と AP がつくる角は $180^\\circ-{180 - a}^\\circ={a}^\\circ$。", "点 P を通り ℓ に平行な直線をひき，錯角を使う。", f"$\\angle x={a}^\\circ+{b}^\\circ={v}^\\circ$。"]
        expr = f"(180-{180 - a})+{b}"
    else:
        fig = bent_fig(a, b, f"{a}°", "y", f"{a + b}°")
        v = b
        stem = f"右の図で，ℓ//m である。図の角の大きさが ${a}^\\circ$，${a + b}^\\circ$ のとき，$\\angle y$ の大きさは何度か，求めなさい。"
        st = ["点 P を通り ℓ に平行な直線をひく。", f"P の角 ${a + b}^\\circ$ は，${a}^\\circ$ と $\\angle y$ の和になる（錯角）。", f"$\\angle y={a + b}^\\circ-{a}^\\circ={b}^\\circ$。"]
        expr = f"{a + b}-{a}"
    return MARK(stem, v, f"P を通り ℓ に平行な直線をひくと，錯角から求める角は ${v}^\\circ$。", expr, d=3, p=4, fig=fig,
                ap="折れ曲がった点 P を通り ℓ に平行な直線をひくと、錯角が2つできる。",
                steps=st,
                alt=["直線 AP を延長して m との交点をつくり、三角形の外角の性質（外角＝となり合わない2内角の和）と同位角・錯角を使っても求められる。"],
                pc=[("補助線をひいて錯角を見つけている", 2), ("正しい大きさを求めている", 2)],
                pit=["$180^\\circ$ から引いてしまう。", "補助線をひかずに、角の位置関係を思いこみで決める。"])


@gen("standard_practice", 4, ["computation", "condition_check"])
def b_polygon_reverse(r):
    kind = r.choice(["sum_to_n", "ratio", "interior", "diag"])
    if kind == "sum_to_n":
        n = r.randint(5, 20)
        S = 180 * (n - 2)
        return MARK(f"内角の和が ${S}^\\circ$ である多角形は何角形か。その数を答えなさい。", n, f"$180(n-2)={S}$ より $n={n}$。{kan(n)}角形。", f"{S}/180+2", d=2, p=4,
                    ap="$n$ 角形の内角の和は $180^\\circ\\times(n-2)$。方程式をつくって $n$ を求める（一次方程式の利用）。",
                    steps=[f"$180(n-2)={S}$。", f"$n-2={S // 180}$。", f"$n={n}$。"],
                    alt=[f"${S}\\div180={n - 2}$ 個の三角形に分けられるので，頂点は ${n - 2}+2={n}$ 個。"],
                    pc=[("方程式を正しく立てている", 2), ("正しい答え", 2)],
                    pit=["$180n={S}$ としてしまう。"])
    if kind == "ratio":
        k = r.choice([2, 3, 4, 5, 7, 8, 9, 11])
        n = 2 * (k + 1)
        return MARK(f"1つの内角の大きさが，1つの外角の大きさの ${k}$ 倍である正多角形は，正何角形か。その数を答えなさい。", n,
                    f"外角を $x^\\circ$ とすると $x+{k}x=180$，$x={ftex_(Fr(180, k + 1))}$。$360\\div{ftex_(Fr(180, k + 1))}={n}$。", f"360/(Rational(180,{k + 1}))", d=3, p=4,
                    ap="内角と外角の和は $180^\\circ$。外角を文字でおいて方程式をつくり、外角の和 $360^\\circ$ を使う。",
                    steps=[f"外角を $x^\\circ$ とおくと内角は ${k}x^\\circ$。", f"$x+{k}x=180$ より $x={ftex_(Fr(180, k + 1))}$。", f"$360\\div{ftex_(Fr(180, k + 1))}={n}$。"],
                    alt=[f"外角の和 $360^\\circ$ と内角の和 $180^\\circ(n-2)$ の比が $1:{k}$ になることから $180(n-2)={k}\\times360$ を解いてもよい。"],
                    pc=[("内角と外角の関係から方程式を立てている", 2), ("正しい答え", 2)],
                    pit=["内角の大きさを $360$ でわってしまう。"])
    if kind == "interior":
        n = r.choice(REG)
        I = 180 - 360 // n
        return MARK(f"1つの内角の大きさが ${I}^\\circ$ である正多角形は，正何角形か。その数を答えなさい。", n,
                    f"1つの外角は $180^\\circ-{I}^\\circ={360 // n}^\\circ$。$360\\div{360 // n}={n}$。", f"360/(180-{I})", d=2, p=4,
                    ap="内角から外角を求め、外角の和 $360^\\circ$ を使う。",
                    steps=[f"外角：$180^\\circ-{I}^\\circ={360 // n}^\\circ$。", f"$360\\div{360 // n}={n}$。"],
                    alt=[f"$\\dfrac{{180(n-2)}}{{n}}={I}$ を解いても $n={n}$。"],
                    pc=[("外角を求めている", 2), ("正しい答え", 2)],
                    pit=["$360\\div{I}$ と内角でわってしまう。"])
    d = r.randint(2, 15)
    n = d + 3
    S = 180 * (n - 2)
    return MARK(f"1つの頂点から ${d}$ 本の対角線をひくことができる多角形の内角の和は何度か，求めなさい。", S,
                f"頂点の数は ${d}+3={n}$。内角の和は $180^\\circ\\times{n - 2}={S}^\\circ$。", f"180*({d}+3-2)", d=3, p=4,
                ap="$n$ 角形の1つの頂点からひける対角線は、自分自身と両どなりの頂点を除いた $(n-3)$ 本。",
                steps=[f"$n-3={d}$ より $n={n}$。", f"内角の和：$180^\\circ\\times({n}-2)={S}^\\circ$。"],
                alt=[f"対角線 ${d}$ 本で三角形が ${d}+1={d + 1}$ 個できるので，$180^\\circ\\times{d + 1}={S}^\\circ$。"],
                pc=[("頂点の数（または三角形の数）を正しく求めている", 2), ("内角の和を正しく求めている", 2)],
                pit=["対角線の本数をそのまま頂点の数と考える。"])


def ftex_(v):
    v = Fr(v)
    return str(v.numerator) if v.denominator == 1 else f"\\dfrac{{{v.numerator}}}{{{v.denominator}}}"


@gen("standard_practice", 4, ["application", "computation"])
def b_shape_angles(r):
    kind = r.choice(["boomerang", "butterfly", "bisector"])
    if kind == "boomerang":
        a, b, c = r.randint(30, 70), r.randint(15, 35), r.randint(15, 35)
        v = a + b + c
        pts = {"A": (0, 4.2), "B": (-3.2, 0), "C": (3.2, 0), "D": (0.3, 1.7)}
        fig = figure("頂点 D が三角形の内側にへこんだ四角形 ABDC", geo(pts, segs=[("A", "B"), ("B", "D"), ("D", "C"), ("C", "A")],
                     texts=[(0, 3.25, f"{a}°"), (-2.05, 0.85, f"{b}°"), (2.1, 0.88, f"{c}°"), (0.28, 1.05, "x")], off={"D": (0, 0.45)},
                     arcs=[("A", 233, 307), ("B", 26, 53), ("C", 127, 150), ("D", 206, 330)]))
        stem = f"右の図の四角形 ABDC で，${A('BAC')}={a}^\\circ$，${A('ABD')}={b}^\\circ$，${A('ACD')}={c}^\\circ$ のとき，$\\angle x={A('BDC')}$ の大きさは何度か，求めなさい。"
        st = ["線分 AD を延長して辺 BC 側に進む直線をひき，2つの三角形の外角を考える。", f"B 側の三角形の外角：${a}^\\circ$ の一部と ${b}^\\circ$ の和。C 側も同様。", f"合わせて $\\angle x={a}^\\circ+{b}^\\circ+{c}^\\circ={v}^\\circ$。"]
        alt = [f"点 B と C を結ぶと，$\\triangle\\mathrm{{ABC}}$ と $\\triangle\\mathrm{{DBC}}$ の内角の和の差から $\\angle x={a}^\\circ+{b}^\\circ+{c}^\\circ$ がわかる。"]
        expr = f"{a}+{b}+{c}"
        e = f"$\\angle x={a}^\\circ+{b}^\\circ+{c}^\\circ={v}^\\circ$。"
    elif kind == "butterfly":
        while True:
            a, b, v = r.randint(40, 80), r.randint(40, 80), r.randint(30, 100)
            c = a + b - v
            if 30 <= c <= 100:
                break
        pts = {"A": (-2.6, 2.8), "B": (2.6, 2.8), "O": (0, 0.85), "C": (3.0, -1.4), "D": (-3.0, -1.4)}
        fig = figure("線分 AC と BD が点 O で交わる図", geo(pts, segs=[("A", "B"), ("A", "C"), ("B", "D"), ("D", "C")],
                     texts=[(-1.75, 2.45, f"{a}°"), (1.75, 2.45, f"{b}°"), (2.1, -1.05, f"{c}°"), (-2.15, -1.05, "x")], off={"O": (0, 0.45)},
                     arcs=[("A", 323, 360), ("B", 180, 217), ("C", 143, 180), ("D", 0, 37)]))
        stem = f"右の図のように，線分 AC と BD が点 O で交わっている。${A('BAC')}={a}^\\circ$，${A('ABD')}={b}^\\circ$，${A('ACD')}={c}^\\circ$ のとき，$\\angle x={A('BDC')}$ の大きさは何度か，求めなさい。"
        st = [f"$\\triangle\\mathrm{{OAB}}$ で，${A('AOB')}=180^\\circ-{a}^\\circ-{b}^\\circ={180 - a - b}^\\circ$。", f"対頂角は等しいので ${A('COD')}={180 - a - b}^\\circ$。", f"$\\triangle\\mathrm{{OCD}}$ で，$\\angle x=180^\\circ-{c}^\\circ-{180 - a - b}^\\circ={v}^\\circ$。"]
        alt = [f"対頂角をはさむ2つの三角形では「残りの2角の和」が等しいので，${a}+{b}={c}+x$ から $x={v}$。"]
        expr = f"{a}+{b}-{c}"
        e = f"${a}^\\circ+{b}^\\circ=\\angle x+{c}^\\circ$ より $\\angle x={v}^\\circ$。"
    else:
        a = r.choice(range(30, 121, 2))
        v = 90 + a // 2
        pts = {"A": (0.6, 3.6), "B": (-3, 0), "C": (3.4, 0), "I": (0.47, 1.44)}
        fig = figure("三角形 ABC と，角 B，角 C の二等分線の交点 I", geo(pts, segs=[("A", "B"), ("B", "C"), ("C", "A"), ("B", "I"), ("I", "C")],
                     texts=[(0.6, 2.75, f"{a}°"), (0.47, 0.88, "x")], off={"I": (0, 0.45)}, arcs=[("A", 225, 308), ("I", 202, 334)]))
        stem = f"右の図の $\\triangle\\mathrm{{ABC}}$ で，${A('ABC')}$ の二等分線と ${A('ACB')}$ の二等分線の交点を I とする。${A('BAC')}={a}^\\circ$ のとき，$\\angle x={A('BIC')}$ の大きさは何度か，求めなさい。"
        st = [f"${A('ABC')}+{A('ACB')}=180^\\circ-{a}^\\circ={180 - a}^\\circ$。", f"それぞれの半分の和は ${(180 - a) // 2}^\\circ$。", f"$\\triangle\\mathrm{{IBC}}$ で $\\angle x=180^\\circ-{(180 - a) // 2}^\\circ={v}^\\circ$。"]
        alt = [f"一般に $\\angle x=90^\\circ+\\dfrac{{1}}{{2}}{A('A')}$ となることを文字で示し，$90+{a // 2}={v}$ と求めてもよい。"]
        expr = f"180-(180-{a})/2"
        e = f"${A('IBC')}+{A('ICB')}=\\dfrac{{1}}{{2}}(180^\\circ-{a}^\\circ)={(180 - a) // 2}^\\circ$ なので $\\angle x={v}^\\circ$。"
    return MARK(stem, v, e, expr, d=3, p=4, fig=fig,
                ap="三角形の内角の和、外角の性質、対頂角を組み合わせる。求める角をふくむ三角形を見つけ、補助線も考える。",
                steps=st, alt=alt,
                pc=[("使う三角形や性質を正しく選んでいる", 2), ("正しい大きさを求めている", 2)],
                pit=["図の見た目で角の大きさを判断する。", "外角と内角を取り違える。"])


def _stmt(r):
    k = r.choice([4, 6, 8, 9, 10, 12, 15])
    d = r.choice([x for x in (2, 3, 4, 5) if k % x == 0 and x != k])
    a = r.randint(2, 9)
    n = r.choice([5, 6, 8, 10])
    return r.choice([
        (f"$x$ が ${k}$ の倍数", f"$x$ は ${d}$ の倍数", True, False),
        (f"$a={a}$", f"$a^2={a * a}$", True, False),
        ("$\\triangle\\mathrm{ABC}\\equiv\\triangle\\mathrm{DEF}$", "$\\triangle\\mathrm{ABC}$ と $\\triangle\\mathrm{DEF}$ の面積は等しい", True, False),
        ("2直線 ℓ，m が平行", "ℓ，m に1つの直線が交わってできる錯角は等しい", True, True),
        ("$\\triangle\\mathrm{ABC}$ が正三角形", "$\\triangle\\mathrm{ABC}$ の3つの角は等しい", True, True),
        (f"四角形 ABCD が正方形", "四角形 ABCD の4つの辺は等しい", True, False),
        (f"多角形が{kan(n)}角形", f"その多角形の内角の和は ${180 * (n - 2)}^\\circ$", True, True),
        (f"$x>{a}$", f"$x>{a - 1}$", True, False),
    ])


@gen("standard_practice", 4, ["concept", "written_reasoning"])
def b_hyp_concl(r):
    P, Q, t, conv_t = _stmt(r)
    s = f"「{P} ならば，{Q}」"
    kind = r.choice(["hyp", "concl", "conv"])
    if kind == "hyp":
        right = P
        cands = [(Q, "これは結論（「ならば」の後ろの部分）である。", "仮定と結論の取り違え"),
                 (f"{Q} ならば，{P}", "これはもとのことがらの逆である。", "逆との混同"),
                 (f"{P} ならば，{Q}", "ことがら全体であり，仮定ではない。", "仮定の意味の誤解")]
        stem = f"ことがら {s} の仮定として最も適するものを，" + SEL4
        e = f"「ならば」の前の部分「{P}」が仮定である。"
    elif kind == "concl":
        right = Q
        cands = [(P, "これは仮定（「ならば」の前の部分）である。", "仮定と結論の取り違え"),
                 (f"{Q} ならば，{P}", "これはもとのことがらの逆である。", "逆との混同"),
                 (f"{P} ならば，{Q}", "ことがら全体であり，結論ではない。", "結論の意味の誤解")]
        stem = f"ことがら {s} の結論として最も適するものを，" + SEL4
        e = f"「ならば」の後ろの部分「{Q}」が結論である。"
    else:
        right = f"{Q} ならば，{P}　（{'正しい' if conv_t else '正しくない'}）"
        cands = [(f"{Q} ならば，{P}　（{'正しくない' if conv_t else '正しい'}）", "逆の文は正しいが，正誤の判断が誤っている。", "逆の正誤の判断の誤り"),
                 (f"{P} ならば，{Q}　（正しい）", "これはもとのことがらであり，逆ではない。", "逆の意味の誤解"),
                 (f"{P} でないならば，{Q} でない　（正しくない）", "仮定と結論を入れかえておらず，逆ではない。", "逆の意味の誤解")]
        stem = f"ことがら {s} の逆と，その逆が正しいかどうかを述べたものとして最も適するものを，" + SEL4
        e = f"逆は「{Q} ならば，{P}」で，{'正しい' if conv_t else '正しくない（反例がある）'}。"
    return MC(stem, right, cands, e, d=3, p=4,
              ap="「○○ならば□□」の○○が仮定、□□が結論。仮定と結論を入れかえたものが逆。逆が正しいかどうかは、反例があるかで判断する。",
              steps=[f"仮定：{P}。", f"結論：{Q}。", e],
              alt=["逆の正誤は、成り立たない例（反例）を1つでも見つければ「正しくない」と言える。"],
              pc=[("仮定と結論を正しく区別している", 2), ("正しいものを選んでいる", 2)],
              pit=["逆を「否定したもの」と考える。", "もとのことがらが正しければ逆も正しいと思いこむ。"])


PROOFS = [
    dict(key="vert", fig=({"A": (-3, 1.6), "B": (3, -1.6), "C": (-2.2, -1.8), "D": (2.2, 1.8), "O": (0, 0)}, [("A", "B"), ("C", "D"), ("A", "C"), ("B", "D")], {"O": (0.45, -0.1)}),
         setup="右の図のように，線分 AB と CD が点 O で交わり，AO$=$BO，CO$=$DO である。このとき，$\\triangle\\mathrm{AOC}\\equiv\\triangle\\mathrm{BOD}$ であることを次のように証明した。",
         body=["$\\triangle\\mathrm{AOC}$ と $\\triangle\\mathrm{BOD}$ において，", "仮定から　AO$=$BO　……①，　CO$=$DO　……②", "（a）は等しいから　$\\angle\\mathrm{AOC}=\\angle\\mathrm{BOD}$　……③", "①，②，③から，（b）ので，$\\triangle\\mathrm{AOC}\\equiv\\triangle\\mathrm{BOD}$"],
         a="対頂角", b="2組の辺とその間の角がそれぞれ等しい"),
    dict(key="alt", fig=({"A": (-3, 1.8), "B": (-0.6, 1.8), "C": (0.6, -1.8), "D": (3, -1.8), "O": (0, 0)}, [("A", "B"), ("C", "D"), ("A", "D"), ("B", "C")], {"O": (-0.5, 0)}),
         setup="右の図のように，AB//CD で，線分 AD と BC の交点を O とする。O が線分 AD の中点であるとき，$\\triangle\\mathrm{ABO}\\equiv\\triangle\\mathrm{DCO}$ であることを次のように証明した。",
         body=["$\\triangle\\mathrm{ABO}$ と $\\triangle\\mathrm{DCO}$ において，", "仮定から　AO$=$DO　……①", "AB//CD より，（a）は等しいから　$\\angle\\mathrm{BAO}=\\angle\\mathrm{CDO}$　……②", "対頂角は等しいから　$\\angle\\mathrm{AOB}=\\angle\\mathrm{DOC}$　……③", "①，②，③から，（b）ので，$\\triangle\\mathrm{ABO}\\equiv\\triangle\\mathrm{DCO}$"],
         a="錯角", b="1組の辺とその両端の角がそれぞれ等しい"),
    dict(key="sss", fig=({"A": (-1.2, 2.6), "D": (1.2, 2.6), "B": (-2.6, 0), "C": (2.6, 0)}, [("A", "B"), ("D", "C"), ("B", "C"), ("A", "C"), ("D", "B")], None),
         setup="右の図で，AB$=$DC，AC$=$DB である。このとき，$\\triangle\\mathrm{ABC}\\equiv\\triangle\\mathrm{DCB}$ であることを次のように証明した。",
         body=["$\\triangle\\mathrm{ABC}$ と $\\triangle\\mathrm{DCB}$ において，", "仮定から　AB$=$DC　……①，　AC$=$DB　……②", "BC は（a）だから　BC$=$CB　……③", "①，②，③から，（b）ので，$\\triangle\\mathrm{ABC}\\equiv\\triangle\\mathrm{DCB}$"],
         a="共通な辺", b="3組の辺がそれぞれ等しい"),
    dict(key="asa_common", fig=({"A": (-1.2, 2.6), "D": (1.2, 2.6), "B": (-2.6, 0), "C": (2.6, 0)}, [("A", "B"), ("D", "C"), ("B", "C"), ("A", "C"), ("D", "B")], None),
         setup="右の図で，$\\angle\\mathrm{ABC}=\\angle\\mathrm{DCB}$，$\\angle\\mathrm{ACB}=\\angle\\mathrm{DBC}$ である。このとき，$\\triangle\\mathrm{ABC}\\equiv\\triangle\\mathrm{DCB}$ であることを次のように証明した。",
         body=["$\\triangle\\mathrm{ABC}$ と $\\triangle\\mathrm{DCB}$ において，", "仮定から　$\\angle\\mathrm{ABC}=\\angle\\mathrm{DCB}$　……①，　$\\angle\\mathrm{ACB}=\\angle\\mathrm{DBC}$　……②", "BC は（a）だから　BC$=$CB　……③", "①，②，③から，（b）ので，$\\triangle\\mathrm{ABC}\\equiv\\triangle\\mathrm{DCB}$"],
         a="共通な辺", b="1組の辺とその両端の角がそれぞれ等しい"),
    dict(key="sas_common", fig=({"A": (0, 3), "B": (-2.4, 0.2), "C": (0, -0.6), "D": (2.4, 0.2)}, [("A", "B"), ("B", "C"), ("A", "D"), ("D", "C"), ("A", "C")], None),
         setup="右の図で，AB$=$AD，$\\angle\\mathrm{BAC}=\\angle\\mathrm{DAC}$ である。このとき，$\\triangle\\mathrm{ABC}\\equiv\\triangle\\mathrm{ADC}$ であることを次のように証明した。",
         body=["$\\triangle\\mathrm{ABC}$ と $\\triangle\\mathrm{ADC}$ において，", "仮定から　AB$=$AD　……①，　$\\angle\\mathrm{BAC}=\\angle\\mathrm{DAC}$　……②", "AC は（a）だから　AC$=$AC　……③", "①，②，③から，（b）ので，$\\triangle\\mathrm{ABC}\\equiv\\triangle\\mathrm{ADC}$"],
         a="共通な辺", b="2組の辺とその間の角がそれぞれ等しい"),
    dict(key="corr", fig=({"A": (-3, 0), "B": (-0.6, 0), "C": (1.8, 0), "D": (-1.6, 2.4), "E": (0.8, 2.4)}, [("A", "C"), ("A", "D"), ("D", "B"), ("B", "E"), ("E", "C")], None),
         setup="右の図で，3点 A，B，C は一直線上にあり，AB$=$BC，AD//BE，DB//EC である。このとき，$\\triangle\\mathrm{ABD}\\equiv\\triangle\\mathrm{BCE}$ であることを次のように証明した。",
         body=["$\\triangle\\mathrm{ABD}$ と $\\triangle\\mathrm{BCE}$ において，", "仮定から　AB$=$BC　……①", "AD//BE より，（a）は等しいから　$\\angle\\mathrm{DAB}=\\angle\\mathrm{EBC}$　……②", "DB//EC より，同位角は等しいから　$\\angle\\mathrm{DBA}=\\angle\\mathrm{ECB}$　……③", "①，②，③から，（b）ので，$\\triangle\\mathrm{ABD}\\equiv\\triangle\\mathrm{BCE}$"],
         a="同位角", b="1組の辺とその両端の角がそれぞれ等しい"),
]
REASONS = ["対頂角", "錯角", "同位角", "共通な辺"]


@gen("standard_practice", 4, ["written_reasoning", "concept"])
def b_proof_fill(r):
    P = r.choice(PROOFS)
    pts, segs, off = P["fig"]
    fig = figure("証明の図", geo(pts, segs=segs, off=off))
    wa = [x for x in REASONS if x != P["a"]]
    wb = [x for x in COND_NAMES if x != P["b"]]

    def C(a, b):
        return f"（a）{a}　（b）{b}"
    right = C(P["a"], P["b"])
    cands = [(C(r.choice(wa), P["b"]), f"（a）は{P['a']}である。図で，等しいことを示す角（辺）の位置関係を確かめる。", "根拠の取り違え"),
             (C(P["a"], r.choice(wb)), f"①〜③でそろった条件は「{P['b']}」である。", "合同条件の取り違え"),
             (C(r.choice(wa), r.choice(wb)), f"（a）は{P['a']}，（b）は「{P['b']}」である。", "根拠と合同条件の取り違え"),
             (C(P["a"], "2組の角がそれぞれ等しい"), "「2組の角がそれぞれ等しい」は合同条件ではない。", "合同条件の誤解")]
    body = "\n".join(P["body"])
    return MC(P["setup"] + f"\n〔証明〕\n{body}\n上の証明の（a），（b）にあてはまるものの組み合わせとして最も適するものを，" + SEL4, right, cands,
              f"（a）は{P['a']}，（b）は「{P['b']}」。", d=3, p=4, fig=fig,
              ap="（a）は、その行で等しいと言っている2つの角（辺）が図の中でどんな位置関係にあるかを見る。（b）は、①〜③が辺か角か、角が辺の間か両端かで判断する。",
              steps=[f"（a）：図で確かめると{P['a']}。", f"①〜③は「{P['b']}」の形になっている。", f"よって（a）{P['a']}，（b）{P['b']}。"],
              alt=["①〜③で等しいとわかった辺・角を図に印でかきこむと、合同条件が見えやすい。"],
              pc=[("（a）の根拠を正しく選んでいる", 2), ("（b）の合同条件を正しく選んでいる", 2)],
              pit=["錯角と同位角を取り違える。", "「間の角」「両端の角」を確かめずに合同条件を選ぶ。"])


# ======================================================================
# C 思考力・記述応用
# ======================================================================

def _xy_pool(r):
    n = r.randint(5, 12)
    m = r.choice([5, 6, 8, 9, 10, 12])
    return [
        (f"{kan(n)}角形の外角の和は $360^\\circ$ である。", True, "外角の和は，何角形でも $360^\\circ$ である。"),
        (f"{kan(n)}角形の内角の和は $180^\\circ\\times{n}$ で求められる。", False, f"三角形は ${n - 2}$ 個に分けられるので $180^\\circ\\times{n - 2}$ である。"),
        (f"正{kan(m)}角形の1つの内角は ${180 - 360 // m}^\\circ$ である。", True, f"1つの外角が $360^\\circ\\div{m}={360 // m}^\\circ$ なので，内角は ${180 - 360 // m}^\\circ$。"),
        (f"正{kan(m)}角形の1つの内角は ${360 // m}^\\circ$ である。", False, f"${360 // m}^\\circ$ は1つの外角である。内角は ${180 - 360 // m}^\\circ$。"),
        ("2直線に1つの直線が交わるとき，同位角が等しければ，その2直線は平行である。", True, "平行線になるための条件である。"),
        ("2直線に1つの直線が交わるとき，錯角はいつでも等しい。", False, "錯角が等しいのは，2直線が平行なときだけである。"),
        ("3つの角がそれぞれ等しい2つの三角形は，合同であるとは限らない。", True, "形が同じでも大きさが異なる三角形があるので，合同とは限らない。"),
        ("2組の辺と1つの角がそれぞれ等しい2つの三角形は，必ず合同である。", False, "その角が2組の辺の間の角でなければ，合同とは限らない。"),
        ("三角形の1つの外角は，それととなり合わない2つの内角の和に等しい。", True, "平行線の同位角・錯角を使って証明できる三角形の性質である。"),
        ("あることがらが正しいとき，その逆もいつでも正しい。", False, "「$x=2$ ならば $x^2=4$」は正しいが，逆の「$x^2=4$ ならば $x=2$」は $x=-2$ という反例があるので正しくない。"),
        ("合同な2つの図形では，対応する辺の長さや角の大きさはそれぞれ等しい。", True, "合同な図形の性質である。"),
        ("三角形の外角のうち，鈍角になるものは多くても1つである。", False, "鋭角三角形では3つの外角がすべて鈍角になる。"),
    ]


@gen("thinking_writing", 4, ["written_reasoning", "condition_check"])
def c_xy_judge(r):
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
        why[c] = (" ".join(rs), "図形の性質の思いこみ")
    return mc("図形の性質について述べた次の X，Y の文の正誤の組み合わせとして最も適するものを，" + SEL4 + f"\nX　{x[0]}\nY　{y[0]}",
              [ans] + [c for c in XY if c != ans], f"X：{x[2]}　Y：{y[2]}", d=4, p=8, why=why,
              ap="それぞれの文が、定義・定理・合同条件などの「すでに正しいとわかっていることがら」から説明できるか、反例がないかを考える。",
              steps=[f"X：{x[2]}", f"Y：{y[2]}", f"よって {ans}。"],
              alt=["図をかいて具体的な数で確かめたり、反例となる図形を探したりする。"],
              pc=[("X の正誤を根拠をもって判断している", 4), ("Y の正誤を根拠をもって判断している", 4)],
              pit=["正しいことがらの逆も正しいと思いこむ。", "合同条件の「間の角」を見落とす。"])


@gen("thinking_writing", 3, ["application", "multiple_solutions"])
def c_regular_mix(r):
    kind = r.choice(["diag", "gap", "diff"])
    if kind == "diag":
        n = r.choice([5, 6, 9, 10, 12, 15, 18, 20])
        I = 180 - 360 // n
        v = 180 // n
        return MARK(f"正{kan(n)}角形の連続する3つの頂点を A，B，C とする。${A('BAC')}$ の大きさは何度か，求めなさい。", v,
                    f"1つの内角 ${A('ABC')}={I}^\\circ$。BA$=$BC なので $\\triangle\\mathrm{{ABC}}$ は二等辺三角形で，${A('BAC')}=(180^\\circ-{I}^\\circ)\\div2={v}^\\circ$。", f"(180-(180-360/{n}))/2", d=4, p=8,
                    ap="正多角形の辺はすべて等しいので、△ABC は BA$=$BC の二等辺三角形になる（二等辺三角形の底角は等しい）。",
                    steps=[f"1つの内角：$180^\\circ-360^\\circ\\div{n}={I}^\\circ$。", "△ABC は BA$=$BC の二等辺三角形。", f"${A('BAC')}=(180^\\circ-{I}^\\circ)\\div2={v}^\\circ$。"],
                    alt=[f"1つの外角 ${360 // n}^\\circ$ の半分になる（$(180-I)\\div2=E\\div2$）ことに気づけば，${360 // n}\\div2={v}$ とすぐ求められる。"],
                    pc=[("1つの内角を正しく求めている", 3), ("二等辺三角形の底角として計算している", 3), ("正しい答え", 2)],
                    pit=["内角の大きさをそのまま答える。"])
    if kind == "gap":
        while True:
            n, m = r.sample([3, 4, 5, 6, 8, 9, 10, 12], 2)
            In, Im = 180 - 360 // n, 180 - 360 // m
            v = 360 - In - Im
            if 360 % n == 0 and 360 % m == 0 and v > 0:
                break
        return MARK(f"{regname(n)}と{regname(m)}を，1辺を共有して重ならないように並べた。共有した辺の一方の端の点のまわりで，2つの図形のどちらにもふくまれない部分の角の大きさは何度か，求めなさい。", v,
                    f"1点のまわりの角は $360^\\circ$。$360^\\circ-{In}^\\circ-{Im}^\\circ={v}^\\circ$。", f"360-(180-360/{n})-(180-360/{m})", d=4, p=8,
                    ap="1点のまわりの角の和は $360^\\circ$。それぞれの正多角形の1つの内角を求めて引く。",
                    steps=[f"{regname(n)}の内角：${In}^\\circ$。", f"{regname(m)}の内角：${Im}^\\circ$。", f"$360^\\circ-{In}^\\circ-{Im}^\\circ={v}^\\circ$。"],
                    alt=[f"外角を使うと，${360 // n}^\\circ+{360 // m}^\\circ={v}^\\circ$ と求めることもできる（$360-(180-E_1)-(180-E_2)=E_1+E_2$）。"],
                    pc=[("それぞれの内角を正しく求めている", 3), ("1点のまわりの角を使っている", 3), ("正しい答え", 2)],
                    pit=["外角と内角を取り違える。"])
    n = r.choice([5, 6, 8, 9, 10, 12, 15, 18, 20, 24, 30, 36])
    d = 180 - 720 // n
    return MARK(f"ある正多角形の1つの内角の大きさは，1つの外角の大きさより ${d}^\\circ$ 大きい。この正多角形は正何角形か。その数を答えなさい。", n,
                f"外角を $x^\\circ$ とすると $(180-x)-x={d}$，$x={360 // n}$。$360\\div{360 // n}={n}$。", f"360/((180-{d})/2)", d=4, p=8,
                ap="外角を $x^\\circ$ とおくと内角は $(180-x)^\\circ$。差の条件から方程式をつくる。",
                steps=[f"$(180-x)-x={d}$。", f"$2x={180 - d}$，$x={360 // n}$。", f"$360\\div{360 // n}={n}$。"],
                alt=[f"正 $n$ 角形の内角 $180-\\dfrac{{360}}{{n}}$ と外角 $\\dfrac{{360}}{{n}}$ の差 $180-\\dfrac{{720}}{{n}}={d}$ を解いても $n={n}$。"],
                pc=[("内角と外角の関係を式に表している", 3), ("方程式を正しく解いている", 3), ("正しい答え", 2)],
                pit=["内角の大きさを $x$ とおいたまま、外角の和を使い忘れる。"])


@gen("thinking_writing", 3, ["cross_unit", "computation"], rel=["JH-MATH-G1-U03"])
def c_parallel_eq(r):
    th = r.choice([x for x in range(40, 141, 5) if x != 90])
    p, q = r.choice(list(POS)), r.choice(list(POS))
    same = POS[p][0] == POS[q][0]
    x0 = r.randint(8, 35)
    a_val = th if POS[p][0] == 0 else 180 - th
    b_val = a_val if same else 180 - a_val
    k1 = r.randint(1, 4)
    c1 = a_val - k1 * x0
    k2 = r.choice([k for k in range(1, 6) if k != k1]) if same else r.randint(1, 5)
    c2 = b_val - k2 * x0

    def ex(k, c):
        s = ("" if k == 1 else str(k)) + "x"
        return f"({s}{'+' if c > 0 else '−'}{abs(c)})°" if c else f"{s}°"

    def exl(k, c):
        s = ("" if k == 1 else str(k)) + "x"
        return f"({s}{'+' if c > 0 else '-'}{abs(c)})^\\circ" if c else f"{s}^\\circ"
    fig = parallel_fig(th, [("P", p, ex(k1, c1)), ("Q", q, ex(k2, c2))])
    name, reason = _relname(p, q)
    def lx(k, c):
        s = ("" if k == 1 else str(k)) + "x"
        return s + (f"+{c}" if c > 0 else f"-{abs(c)}" if c < 0 else "")
    if same:
        eq = f"{lx(k1, c1)}={lx(k2, c2)}"
        eqtxt = "2つの角は等しい"
    else:
        eq = f"({lx(k1, c1)})+({lx(k2, c2)})=180"
        eqtxt = "2つの角の和は $180^\\circ$"
    return MARK(f"右の図で，ℓ//m である。2つの角の大きさがそれぞれ ${exl(k1, c1)}$，${exl(k2, c2)}$ と表されているとき，$x$ の値を求めなさい。", x0,
                f"{eqtxt}ので ${eq}$。これを解いて $x={x0}$。", f"{x0}", d=4, p=8, fig=fig,
                ap="2つの角の位置関係（同位角・錯角・同側内角など）から「等しい」か「和が $180^\\circ$」かを判断し、一次方程式をつくる（一次方程式の単元とのつながり）。",
                steps=[f"2つの角の関係：{reason}。", f"方程式：${eq}$。", f"$x={x0}$。", f"確かめ：2つの角は ${a_val}^\\circ$ と ${b_val}^\\circ$。"],
                alt=["求めた $x$ を代入して2つの角の大きさを計算し、等しい（または和が $180^\\circ$）かどうかで検算する。"],
                pc=[("2つの角の関係を正しく判断している", 3), ("方程式を正しく立てている", 3), ("正しい答え", 2)],
                pit=["和が $180^\\circ$ になる関係なのに、等しいとして方程式をつくる。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def _err_mc(stem, sol, right, cands, e, err, **kw):
    return MC(f"{stem}\n〔Kさんの解答〕\n{sol}\nKさんの解答の誤りを説明したものとして最も適するものを，" + SEL4, right, cands, e, err=err, **kw)


@gen("error_correction", 4, ["common_error", "computation"])
def d_polygon_err(r):
    kind = r.choice(["sum", "int"])
    if kind == "sum":
        n = r.randint(5, 20)
        v = 180 * (n - 2)
        sol = f"{kan(n)}角形は1つの頂点から対角線をひくと，三角形が ${n}$ 個できる。\n$180^\\circ\\times{n}={180 * n}^\\circ$　答え ${180 * n}^\\circ$"
        right = f"1つの頂点から対角線をひいてできる三角形は ${n}$ 個ではなく ${n - 2}$ 個である。"
        step, etype, tempt = "三角形の個数を数える部分", "concept", "「$n$ 角形だから三角形も $n$ 個」と、図をかかずに考えてしまう。"
        cands = [(f"三角形の内角の和は $360^\\circ$ なので，$360^\\circ$ をかけるべきである。", "三角形の内角の和は $180^\\circ$ で正しい。", "三角形の内角の和の誤解"),
                 ("外角の和 $360^\\circ$ を加えるべきである。", "内角の和に外角の和を加える必要はない。", "内角と外角の混同"),
                 ("Kさんの解答に誤りはない。", f"五角形で確かめると三角形は3個で，$180^\\circ\\times5$ にはならない。", "検算不足")]
        fix = f"$180^\\circ\\times({n}-2)={v}^\\circ$"
        stem = f"〔問題〕{kan(n)}角形の内角の和を求めなさい。"
        chk = (f"180*({n}-2)", str(v))
    else:
        n = r.choice([5, 6, 8, 9, 10, 12, 15, 18, 20])
        e = 360 // n
        v = 180 - e
        sol = f"外角の和は $360^\\circ$ だから，$360^\\circ\\div{n}={e}^\\circ$　答え ${e}^\\circ$"
        right = f"${e}^\\circ$ は1つの外角の大きさである。内角は $180^\\circ$ から外角を引いて求めなければならない。"
        step, etype, tempt = "最後に答えを決める部分", "interpretation", "外角を求める計算をしたところで、問われているのが内角であることを忘れてしまう。"
        cands = [("外角の和は $180^\\circ$ なので，$180^\\circ$ を使うべきである。", "外角の和は $360^\\circ$ で正しい。", "外角の和の誤解"),
                 (f"$360^\\circ$ を ${n}$ ではなく ${n - 2}$ でわるべきである。", f"外角は ${n}$ 個あるので ${n}$ でわるのは正しい。", "公式の混同"),
                 ("Kさんの解答に誤りはない。", f"正{kan(n)}角形の内角は鈍角であり，${e}^\\circ$ にはならない。", "検算不足")]
        fix = f"$180^\\circ-{e}^\\circ={v}^\\circ$"
        stem = f"〔問題〕正{kan(n)}角形の1つの内角の大きさを求めなさい。"
        chk = (f"180-360/{n}", str(v))
    return _err_mc(stem, sol, right, cands, f"正しくは {fix}。", dict(sol=sol, step=step, type=etype, tempt=tempt, fix=fix), d=3, p=6,
                   ap="図をかいて三角形の数を数えたり、内角と外角のどちらを求めているのかを確かめたりして、Kさんの解答と比べる。",
                   steps=["問われているもの（内角の和／1つの内角）を確認する。", "Kさんの解答の各部分を、図や公式と照らし合わせる。", f"正しくは {fix}。"],
                   alt=["五角形など小さい場合で答えを確かめ、Kさんの方法が正しいかを調べる。"],
                   pc=[("誤りの箇所を正しく指摘している", 3), ("正しい答えを求めている", 3)],
                   pit=["三角形の数を $n$ 個とする。", "外角と内角を取り違える。"],
                   chk=chk + (None, "intermediate"))


@gen("error_correction", 3, ["common_error", "condition_check"])
def d_congruence_err(r):
    kind = r.choice(["ssa", "aaa"])
    if kind == "ssa":
        p, q = r.sample(range(4, 10), 2)
        t = r.choice([30, 35, 40, 45, 50])
        given = f"AB$=$DE$={p}$ cm，BC$=$EF$={q}$ cm，${A('A')}={A('D')}={t}^\\circ$"
        sol = "2組の辺と1つの角がそれぞれ等しいので，$\\triangle\\mathrm{ABC}\\equiv\\triangle\\mathrm{DEF}$ である。"
        right = "等しい角 $\\angle\\mathrm{A}$ は，等しい2組の辺 AB，BC の間の角ではないので，合同条件にあてはまらない。"
        step, etype = "合同条件のあてはめ", "condition"
        tempt = "「2組の辺とその間の角」の「間の」を読み落としやすい。"
        fix = "合同であるとはいえない（$\\angle\\mathrm{B}=\\angle\\mathrm{E}$ のように間の角が等しければ合同といえる）"
        cands = [("3組の辺がすべて等しくなければ，合同とはいえない。", "2組の辺とその間の角が等しい場合など，3組の辺がわからなくても合同といえる場合がある。", "合同条件の誤解"),
                 ("角が等しいときは，対頂角でなければ合同とはいえない。", "対頂角かどうかは合同条件と関係がない。", "根拠の混同"),
                 ("Kさんの解答に誤りはない。", "条件を満たす三角形をかくと，C の位置が2通りできる場合があり，合同とは限らない。", "合同条件の誤解")]
    else:
        a, b = r.randint(35, 75), r.randint(35, 75)
        c = 180 - a - b
        given = f"${A('A')}={A('D')}={a}^\\circ$，${A('B')}={A('E')}={b}^\\circ$，${A('C')}={A('F')}={c}^\\circ$"
        sol = "3組の角がそれぞれ等しいので，$\\triangle\\mathrm{ABC}\\equiv\\triangle\\mathrm{DEF}$ である。"
        right = "3つの角がそれぞれ等しくても，大きさの異なる三角形があるので，合同とはいえない。辺が1組も等しいとわかっていない。"
        step, etype = "合同条件のあてはめ", "concept"
        tempt = "形が同じなら合同だと思いこみやすい。"
        fix = "合同であるとはいえない（辺の長さの条件が必要）"
        cands = [("3つの角の和が $180^\\circ$ にならないので，三角形ができない。", f"${a}+{b}+{c}=180$ で，三角形はできる。", "計算の確認不足"),
                 ("「2組の角がそれぞれ等しい」で合同といえるので，3組目を書く必要はない。", "角だけの条件は，何組あっても合同条件にならない。", "合同条件の誤解"),
                 ("Kさんの解答に誤りはない。", "1辺が2倍の拡大図も3つの角が等しいが，合同ではない。", "合同条件の誤解")]
    return _err_mc(f"〔問題〕$\\triangle\\mathrm{{ABC}}$ と $\\triangle\\mathrm{{DEF}}$ で，{given} である。この2つの三角形は合同であるといえるか。", sol, right, cands,
                   f"正しくは「{fix}」。", dict(sol=sol, step=step, type=etype, tempt=tempt, fix=fix), d=3, p=6,
                   ap="与えられた辺と角を図にかきこみ、3つの合同条件のどれかにぴったりあてはまるかを確かめる。あてはまらなければ、反例（合同にならない例）を考える。",
                   steps=["等しい辺と角を図にかきこむ。", "合同条件のどれにあてはまるかを調べる。", "あてはまらないので，合同とはいえない。"],
                   alt=["条件どおりの三角形を2通りかいてみて、形や大きさが違うものができれば合同とはいえない。"],
                   pc=[("誤りの理由を正しく指摘している", 3), ("合同条件を正しく理解している", 3)],
                   pit=["2組の辺と「間でない角」で合同と判断する。", "角だけで合同と判断する。"])


@gen("error_correction", 3, ["common_error", "written_reasoning"])
def d_angle_steps(r):
    a, b = r.randint(25, 65), r.randint(25, 65)
    where = r.randint(1, 3)
    l1 = "点 P を通り ℓ に平行な直線 n をひく"
    up, lo, x = a, b, a + b
    l2 = f"ℓ//n より錯角は等しいので，P の上側の角は ${a}^\\circ$"
    l3 = f"n//m より錯角は等しいので，P の下側の角は ${b}^\\circ$"
    if where == 1:
        up = 180 - a
        l2 = f"ℓ//n より，P の上側の角は $180^\\circ-{a}^\\circ={up}^\\circ$"
    if where == 2:
        lo = 180 - b
        l3 = f"n//m より，P の下側の角は $180^\\circ-{b}^\\circ={lo}^\\circ$"
    l4 = f"$\\angle x={up}^\\circ+{lo}^\\circ={up + lo}^\\circ$"
    if where == 3:
        l4 = f"$\\angle x=180^\\circ-({up}^\\circ+{lo}^\\circ)={180 - up - lo}^\\circ$"
    sol = "\n".join(f"{i + 1}行目　{t}" for i, t in enumerate([l1, l2, l3, l4]))
    LINES4 = ["1行目", "2行目", "3行目", "4行目"]
    ok = {0: "1行目は正しい。平行線をひくのは錯角を使うための有効な補助線である。", 1: f"2行目は正しい。ℓ と n の錯角で上側の角は ${a}^\\circ$。",
          2: f"3行目は正しい。n と m の錯角で下側の角は ${b}^\\circ$。", 3: "4行目は，上側と下側の角を正しく加えている。"}
    why = {LINES4[i]: (ok[i], "誤りの箇所の見落とし") for i in range(4) if i != where}
    info = {1: ("2行目（錯角を $180^\\circ$ から引いた）", "concept", "錯角と同側内角（和が $180^\\circ$）を混同している。"),
            2: ("3行目（錯角を $180^\\circ$ から引いた）", "concept", "錯角と同側内角（和が $180^\\circ$）を混同している。"),
            3: ("4行目（$180^\\circ$ から引いた）", "logic", "三角形の内角の和の計算と混同して、$180^\\circ$ から引いてしまう。")}[where]
    fix = f"$\\angle x={a}^\\circ+{b}^\\circ={x}^\\circ$"
    return mc(f"〔問題〕右の図で，ℓ//m のとき，$\\angle x$ の大きさを求めなさい。\n〔Kさんの解答〕\n{sol}\nKさんの解答で，誤りが最初に生じた行として最も適するものを，" + SEL4,
              LINES4, f"誤りが最初に生じたのは{LINES4[where]}。正しくは {fix}。", d=3, p=6, keep=True, ai=where, why=why,
              fig=bent_fig(a, b, f"{a}°", f"{b}°", "x"),
              err=dict(sol=sol, step=info[0], type=info[1], tempt=info[2], fix=fix),
              ap="補助線 n をかきこみ、各行で使っている角が錯角か同位角か同側内角かを図で確かめる。",
              steps=["点 P を通り ℓ に平行な直線 n をひく。", f"錯角から上側 ${a}^\\circ$，下側 ${b}^\\circ$。", f"$\\angle x={x}^\\circ$。"],
              alt=["直線 AP を延長して m との交点をつくり、三角形の外角の性質で求めて比べる。"],
              pc=[("誤りの行を正しく指摘している", 3), ("正しい角の大きさを求めている", 3)],
              pit=["錯角と同側内角を混同する。"],
              chk=(f"{a}+{b}", str(x), None, "intermediate"))


GENERATORS = [a_polygon_sum, a_parallel_angle, a_triangle_angle, a_congruence_cond,
              b_bent, b_polygon_reverse, b_shape_angles, b_hyp_concl, b_proof_fill,
              c_xy_judge, c_regular_mix, c_parallel_eq,
              d_polygon_err, d_congruence_err, d_angle_steps]


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


GENERATORS = [_robust(g) for g in GENERATORS]
