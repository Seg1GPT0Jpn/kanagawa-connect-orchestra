"""単元パック：中学3年 相似な図形（神奈川県公立高校入試形式）。"""
import math
import re
import unicodedata
from fractions import Fraction as Fr

from banks._common import figure, mc, num
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem, tp)

UNIT_ID = "JH-MATH-G3-U05"

PREREQUISITES = [
    ("JH-MATH-G2-U04", "平行線の同位角・錯角、三角形の合同条件と証明の書き方。相似の証明は合同の証明と同じ組み立てで進める。"),
    ("JH-MATH-G2-U05", "二等辺三角形・平行四辺形の性質。中点連結定理や平行四辺形の中の相似で使う。"),
    ("JH-MATH-G1-U03", "比例式 $a:b=c:d$ ならば $ad=bc$。対応する辺の比から長さを求めるときに必ず使う。"),
    ("JH-MATH-G1-U06", "錐体・柱体の体積の公式。相似な立体の体積比を考える土台になる。"),
]
EXTENSIONS = [
    ("JH-MATH-G3-U06", "円周角の定理と組み合わせて、円の中にできる相似な三角形を証明する。"),
    ("JH-MATH-G3-U07", "三平方の定理の証明（直角三角形を垂線で分けた相似）や、相似と組み合わせた長さの計算に使う。"),
    ("HS-MATH1-U04", "高校の三角比は、相似な直角三角形では辺の比が一定であることを土台にしている。"),
    ("HS-MATHA-U02", "メネラウスの定理・チェバの定理、角の二等分線と比など、線分の比の考え方がさらに広がる。"),
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


def geo(pts, segs=(), dashed=(), texts=(), names=None, off=None, scale=26, pad=20, ticks=(), right=(), dots=()):
    """幾何の図。pts={名前: (x, y)}、segs=[("A","B"), ...]、texts=[(x, y, 文字)]、off={名前: (dx, dy)}、
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


STD = tri_xy(6, 5, 4)  # 図用の標準的な三角形


def fig_de_bc(t=0.4, alt="DE//BC の三角形 ABC"):
    P = dict(STD)
    P["D"] = lerp(P["A"], P["B"], t)
    P["E"] = lerp(P["A"], P["C"], t)
    return figure(alt, geo(P, segs=[("A", "B"), ("B", "C"), ("C", "A"), ("D", "E")], off={"D": (-0.35, 0.05), "E": (0.35, 0.05)}))


def fig_sim_pair(k, base=(6, 5, 4), alt="相似な2つの三角形 ABC と DEF"):
    P = tri_xy(*base, size=3.6)
    k = min(max(k, 0.6), 1.5)
    Q = {"D": P["A"], "E": P["B"], "F": P["C"]}
    shift = max(p[0] for p in P.values()) + 1.2
    Q = {n: (x * k + shift, y * k) for n, (x, y) in Q.items()}
    pts = P | Q
    return figure(alt, geo(pts, segs=[("A", "B"), ("B", "C"), ("C", "A"), ("D", "E"), ("E", "F"), ("F", "D")],
                           off={"A": (0, 0.35), "B": (-0.3, -0.2), "C": (0.3, -0.2), "D": (0, 0.35), "E": (-0.3, -0.2), "F": (0.3, -0.2)}))


def fig_trap(a, b, extra=False):
    s = 5.0 / b
    h = 2.4
    off_x = (b - a) * s / 2 - 0.4
    P = {"A": (off_x, h), "D": (off_x + a * s, h), "B": (0.0, 0.0), "C": (b * s, 0.0)}
    P["O"] = inter(P["A"], P["C"], P["B"], P["D"])
    segs = [("A", "D"), ("D", "C"), ("C", "B"), ("B", "A"), ("A", "C"), ("B", "D")]
    off = {"O": (0, -0.45)}
    if extra:
        y = P["O"][1]
        P["E"] = inter(P["A"], P["B"], (0, y), (1, y))
        P["F"] = inter(P["D"], P["C"], (0, y), (1, y))
        segs.append(("E", "F"))
        off |= {"E": (-0.35, 0), "F": (0.35, 0), "O": (0.25, -0.4)}
    return figure("AD//BC の台形 ABCD と対角線", geo(P, segs=segs, off=off))


# ----------------------------------------------------------------------
# 授業プリント
# ----------------------------------------------------------------------

LESSON = lesson(
    goals=["相似の意味と相似比を理解し、三角形の相似条件を使って2つの三角形が相似であることを証明できる。",
           "平行線と線分の比、中点連結定理を、相似をもとに説明し、線分の長さを求めるのに使える。",
           "相似比が $m:n$ の図形の面積比は $m^2:n^2$、立体の体積比は $m^3:n^3$ になることを説明し、活用できる。"],
    duration=100,
    readiness=["比例式 $a:b=c:d$ の性質（$ad=bc$）を使って値を求められる。",
               "平行線の同位角・錯角、対頂角の性質を使える。",
               "三角形の合同条件を使った証明の書き方を知っている。",
               "三角形・円・錐体・柱体の面積や体積の公式を使える。"],
    flow=[("導入：拡大図と縮図", 10, "コピー機の拡大・縮小から、形が同じで大きさが違う図形（相似）を考える"),
          ("相似の意味と相似条件", 20, "対応する辺の比・角、相似比。三角形の相似条件3つと合同条件との対応"),
          ("相似の証明", 15, "例題1：共通な角と平行線を使う証明"),
          ("平行線と線分の比", 20, "三角形と比の定理の導出、例題2、3本の平行線と比"),
          ("中点連結定理", 10, "平行線と線分の比の特別な場合として導く"),
          ("面積比・体積比", 15, "相似比から面積比・体積比を導く、例題3"),
          ("まとめと確認", 10, "確認問題と問題プリントの指示")],
    sections=[
        intro("in1", "形が同じで大きさが違う図形",
              "コピー機で写真を 200％ に拡大すると、形はそのままで、どの長さも2倍になる。このように、1つの図形を形を変えずに一定の割合で拡大または縮小した図形は、もとの図形と相似であるという。地図・設計図・縮図は、すべて相似の考えを利用している。",
              bullets=["相似な図形では、対応する線分の長さの比はすべて等しく、対応する角の大きさはそれぞれ等しい。",
                       "記号 ∽ を使って △ABC∽△DEF のように書く。このとき、対応する頂点を同じ順に書く。"],
              points=[tp("拡大コピーの例で「長さは2倍、角度は変わらない」ことを確かめさせ、相似の2つの性質（辺の比・角）を引き出す。",
                         ask="200％ に拡大すると、角の大きさはどうなるか。", expect="変わらない。2倍にはならない。", timing="導入")]),
        definition("df1", "相似比",
                   "相似な2つの図形で、対応する線分の長さの比を相似比という。△ABC∽△DEF で AB$=6$ cm、DE$=9$ cm ならば、相似比は $6:9=2:3$ である。",
                   conditions=["相似比は最も簡単な整数の比で表すことが多い。", "合同な図形は、相似比が $1:1$ の相似な図形と考えられる。",
                               "対応する辺は、∽ の記号の両側で同じ位置にある頂点どうしで決まる（AB と DE、BC と EF、CA と FD）。"],
                   points=[tp("対応する頂点の順に書くことの大切さを強調する。", caution="△ABC∽△EDF のような書き方では、AB に対応するのは ED になる。図の見た目でなく、記号の順で対応を読ませる。")]),
        theorem("th1", "三角形の相似条件",
                "$$\\text{① 3組の辺の比がすべて等しい}\\quad\\text{② 2組の辺の比とその間の角がそれぞれ等しい}\\quad\\text{③ 2組の角がそれぞれ等しい}$$",
                ["2つの三角形は、①〜③のどれか1つが成り立てば相似である。",
                 "合同条件（3組の辺／2組の辺とその間の角／1組の辺とその両端の角）と見比べると覚えやすい。",
                 "③は、2組の角が等しければ残りの角も等しい（内角の和が $180^\\circ$）ことから、辺の長さに関係なく形が決まる。証明では③を使うことが最も多い。"],
                points=[tp("合同条件と相似条件を左右に並べて板書し、「等しい」が「比が等しい」に変わったこと、③では辺の条件がいらなくなったことに気づかせる。",
                           ask="合同条件の「1組の辺とその両端の角」は、相似条件ではどうなるか。", expect="辺の長さはどうでもよくなり、「2組の角」だけが残る。")]),
        theorem("th2", "三角形と比の定理（平行線と線分の比）",
                "$$\\mathrm{DE}\\parallel\\mathrm{BC}\\ \\Longrightarrow\\ \\mathrm{AD}:\\mathrm{AB}=\\mathrm{AE}:\\mathrm{AC}=\\mathrm{DE}:\\mathrm{BC},\\quad \\mathrm{AD}:\\mathrm{DB}=\\mathrm{AE}:\\mathrm{EC}$$",
                ["△ABC の辺 AB、AC 上（またはその延長上）に点 D、E をとるとき、DE//BC ならば上の比が成り立つ。",
                 "逆に、AD：DB$=$AE：EC ならば DE//BC である。",
                 "注意：DE：BC は AD：AB と等しい。AD：DB と等しいのではない。",
                 "3本以上の平行線に2本の直線が交わるとき、平行線で切りとられる線分の比は等しい。"],
                proof=["DE//BC より、同位角は等しいので ∠ADE$=$∠ABC、∠AED$=$∠ACB。",
                       "2組の角がそれぞれ等しいので、△ADE∽△ABC。",
                       "対応する辺の比は等しいので、AD：AB$=$AE：AC$=$DE：BC。",
                       "AD：DB$=$AE：EC は、E を通り AB に平行な直線をひき、BC との交点を F とすると、△ADE∽△EFC と四角形 DBFE が平行四辺形（DB$=$EF）であることから導ける。"],
                points=[tp("「上：全体」と「上：下」の2種類の比があることを、図に色分けして示す。どちらの比で DE：BC が決まるかを確認させる。",
                           ask="AD：DB$=2:3$ のとき、DE：BC はいくつか。", expect="$2:5$。$2:3$ ではない。", caution="もっとも多い誤答。必ず全体（AB）との比に直させる。")]),
        derivation("dv1", "中点連結定理を導く",
                   ["△ABC で、辺 AB、AC の中点をそれぞれ M、N とする。",
                    "AM：AB$=1:2$、AN：AC$=1:2$、∠A は共通なので、2組の辺の比とその間の角がそれぞれ等しく、△AMN∽△ABC（相似比 $1:2$）。",
                    "対応する角は等しいので ∠AMN$=$∠ABC。同位角が等しいから MN//BC。",
                    "対応する辺の比から MN：BC$=1:2$、すなわち MN$=\\dfrac{1}{2}$BC。",
                    "まとめ（中点連結定理）：三角形の2辺の中点を結ぶ線分は、残りの辺に平行で、長さはその半分である。"],
                   points=[tp("四角形の4辺の中点を結ぶと平行四辺形ができることを、対角線をひいて中点連結定理を2回使うことで確かめさせる。", timing="中点連結定理のあと")]),
        derivation("dv2", "面積比・体積比を導く",
                   ["相似比が $m:n$ の2つの三角形で、底辺を $ma$、$na$、高さを $mh$、$nh$ とする。",
                    "面積は $\\dfrac{1}{2}\\times ma\\times mh=m^2\\times\\dfrac{1}{2}ah$、$\\dfrac{1}{2}\\times na\\times nh=n^2\\times\\dfrac{1}{2}ah$。",
                    "よって面積比は $m^2:n^2$。どんな多角形も三角形に分けられるので、相似な平面図形の面積比は相似比の2乗になる。",
                    "相似比が $m:n$ の立体では、縦・横・高さがすべて $m:n$ になるので、体積比は $m^3:n^3$。表面積の比は $m^2:n^2$。"],
                   points=[tp("1辺 1 cm と 2 cm の立方体を実際に考えさせ、表面積は4倍、体積は8倍になることを確かめる。",
                              ask="1辺が2倍の立方体の体積は何倍か。", expect="8倍。", caution="「2倍」と答える生徒が多い。")]),
        example("ex1", "例題1　相似の証明",
                "∠C$=90^\\circ$ の直角三角形 ABC で、頂点 C から辺 AB に垂線 CD をひく。△ABC∽△ACD であることを証明しなさい。",
                ["△ABC と △ACD において、", "仮定から ∠ACB$=$∠ADC$=90^\\circ$ ……①", "∠A は共通 ……②",
                 "①、②から、2組の角がそれぞれ等しいので、△ABC∽△ACD"],
                "上の証明のとおり",
                thinking="2つの三角形に共通な部分（共通な角）を探す。直角が2つあることにも目をつける。",
                figure=figure("直角三角形 ABC と垂線 CD", geo({"A": (0, 0), "B": (5, 0), "C": (1.8, 2.4), "D": (1.8, 0)}, segs=[("A", "B"), ("B", "C"), ("C", "A"), ("C", "D")],
                                                           right=[("A", "D", "C"), ("A", "C", "B")], off={"D": (0, -0.4)})),
                points=[tp("対応する頂点を正しい順に書かせる。∠A↔∠A、∠ACB↔∠ADC なので、B↔C、C↔D の対応になる。")],
                misconceptions=[("△ABC∽△ADC と書く", "直角どうし（C と D）を対応させるので △ABC∽△ACD")]),
        example("ex2", "例題2　平行線と線分の比",
                "△ABC の辺 AB、AC 上にそれぞれ点 D、E があり、DE//BC である。AD$=4$ cm、DB$=6$ cm、BC$=15$ cm のとき、DE の長さを求めなさい。",
                ["DE//BC より △ADE∽△ABC。", "相似比は AD：AB$=4:(4+6)=2:5$。", "DE：BC$=2:5$ より DE$=15\\times\\dfrac{2}{5}=6$ cm。"],
                "$6$ cm",
                thinking="DE と BC の比は、AD と AB（全体）の比に等しい。",
                figure=fig_de_bc(0.4),
                points=[tp("AD：DB$=4:6$ をそのまま使って $15\\times\\dfrac{4}{6}=10$ とする誤答を板書して、どこが違うかを話し合わせる。")],
                misconceptions=[("DE：BC$=$AD：DB$=4:6$", "DE：BC$=$AD：AB$=4:10$")]),
        example("ex3", "例題3　面積比・体積比",
                "相似な2つの円錐 P、Q があり、相似比は $2:3$ である。P の体積が $48\\pi$ cm³ のとき、Q の体積を求めなさい。",
                ["体積比は $2^3:3^3=8:27$。", "Q の体積を $V$ とすると $48\\pi:V=8:27$。", "$V=48\\pi\\times\\dfrac{27}{8}=162\\pi$ cm³。"],
                "$162\\pi$ cm³",
                thinking="相似な立体の体積比は相似比の3乗。",
                points=[tp("円錐を底面に平行な平面で切った「上の小さい円錐」と「もとの円錐」も相似であることにふれ、問題プリントの容器の水の問題につなげる。")]),
        board("bd1", "板書案",
              [("① 相似と相似条件", ["相似：形が同じ、大きさが違う", "対応する辺の比が等しい・角が等しい", "相似比＝対応する辺の比", "条件：3辺の比／2辺の比と間の角／2角"]),
               ("② 平行線と線分の比", ["DE//BC → △ADE∽△ABC", "AD：AB＝AE：AC＝DE：BC", "AD：DB＝AE：EC", "中点連結：MN//BC，MN＝½BC"]),
               ("③ 面積比・体積比", ["相似比 m：n", "周の長さ m：n", "面積・表面積 m²：n²", "体積 m³：n³"])],
              points=[tp("②の「DE：BC は全体との比」を赤で囲み、例題2の誤答例と並べて板書する。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("相似の証明では、まず対応する頂点を図に印で書きこませ、「どの角とどの角が等しいか」を言葉で確認してから書かせる。"),
               tp("平行線と線分の比では、比の式を立てる前に「どの三角形とどの三角形が相似か」を必ず言わせる。", ask="DE//BC のとき、相似な三角形はどれとどれか。", expect="△ADE と △ABC。"),
               tp("面積比・体積比を求めたら、具体的な数（1辺 1 と 2 の正方形・立方体）で確かめる習慣をつけさせる。", timing="例題3のあと"),
               tp("入試では、相似の証明の空欄補充（根拠と相似条件を選ぶ）が頻出である。根拠（共通な角・同位角・錯角・対頂角・円周角）を整理しておく。", timing="まとめ")],
              misconceptions=[("DE//BC のとき DE：BC$=$AD：DB", "DE：BC$=$AD：AB（全体との比）"),
                              ("相似比が $2:3$ なら面積比も $2:3$", "面積比は $4:9$、体積比は $8:27$"),
                              ("1組の角が等しければ相似", "相似条件は2組の角。1組だけでは形が決まらない")]),
        summary("sm1", "まとめ",
                ["相似な図形では、対応する線分の比はすべて等しく、対応する角はそれぞれ等しい。",
                 "三角形の相似条件：3組の辺の比、2組の辺の比とその間の角、2組の角。",
                 "DE//BC ならば AD：AB$=$AE：AC$=$DE：BC、AD：DB$=$AE：EC。",
                 "中点連結定理：2辺の中点を結ぶ線分は、残りの辺に平行で長さはその半分。",
                 "相似比 $m:n$ → 面積比 $m^2:n^2$、体積比 $m^3:n^3$。"]),
        check("ck1", "確認問題",
              [("△ABC∽△DEF で、AB$=8$ cm、DE$=12$ cm のとき、相似比を求めなさい。", "$8:12=2:3$"),
               ("△ABC の辺 AB、AC の中点を M、N とする。BC$=11$ cm のとき、MN の長さを求めなさい。", "$\\dfrac{11}{2}$ cm"),
               ("相似比が $3:4$ の2つの三角形の面積比を求めなさい。", "$9:16$")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

BASES = [(a, b, c) for a in range(2, 8) for b in range(2, 8) for c in range(2, 8)
         if a < b + c and b < a + c and c < a + b and len({a, b, c}) == 3]
RATIOS = [(2, 3), (3, 2), (3, 4), (4, 3), (2, 5), (5, 2), (3, 5), (5, 3), (1, 2), (2, 1), (4, 5), (5, 4), (1, 3), (3, 1)]


@gen("basic_check", 4, ["computation"])
def a_sim_side(r):
    a0, b0, c0 = r.choice(BASES)
    p, q = r.choice(RATIOS)
    abc = {"BC": a0 * p, "CA": b0 * p, "AB": c0 * p}
    de = {"EF": a0 * q, "FD": b0 * q, "DE": c0 * q}
    corr = {"AB": "DE", "BC": "EF", "CA": "FD"}
    kind = r.choice(["def", "def", "abc", "ratio"])
    fig = fig_sim_pair(q / p, base=(a0, b0, c0))
    gs = f"AB$={abc['AB']}$ cm，BC$={abc['BC']}$ cm，CA$={abc['CA']}$ cm"
    ap = "△ABC∽△DEF では，AB と DE，BC と EF，CA と FD が対応する。対応する辺の比はすべて等しい（相似比）。"
    if kind == "def":
        known = r.choice(list(corr))
        ask = r.choice([s for s in corr if s != known])
        v = de[corr[ask]]
        stem = f"右の図で，△ABC∽△DEF である。{gs}，{corr[known]}$={de[corr[known]]}$ cm のとき，辺 {corr[ask]} の長さは何 cm か，求めなさい。"
        st = [f"{known} と {corr[known]} が対応するので，相似比は ${abc[known]}:{de[corr[known]]}={p}:{q}$。",
              f"{ask} と {corr[ask]} が対応するので，${abc[ask]}:$ {corr[ask]} $={p}:{q}$。",
              f"{corr[ask]}$={abc[ask]}\\times\\dfrac{{{q}}}{{{p}}}={v}$ cm。"]
        expr = f"{abc[ask]}*{q}/{p}"
        return MARK(stem, v, st[-1], expr, d=1, fig=fig, ap=ap, steps=st,
                    alt=[f"相似比 ${p}:{q}$ から，△DEF の辺は △ABC の辺の $\\dfrac{{{q}}}{{{p}}}$ 倍と考えて求めてもよい。"],
                    pc=[("対応する辺を正しく見つけている", 1), ("正しい長さを求めている", 1)],
                    pit=["図の見た目で対応する辺を決めてしまう。", "比を逆にして掛ける。"])
    if kind == "abc":
        known = r.choice(list(corr))
        ask = r.choice([s for s in corr if s != known])
        v = abc[ask]
        gs2 = f"DE$={de['DE']}$ cm，EF$={de['EF']}$ cm，FD$={de['FD']}$ cm"
        stem = f"右の図で，△ABC∽△DEF である。{gs2}，{known}$={abc[known]}$ cm のとき，辺 {ask} の長さは何 cm か，求めなさい。"
        st = [f"{known} と {corr[known]} が対応するので，相似比は ${abc[known]}:{de[corr[known]]}={p}:{q}$。",
              f"{ask}：{corr[ask]}$={p}:{q}$ より，{ask}$={de[corr[ask]]}\\times\\dfrac{{{p}}}{{{q}}}={v}$ cm。"]
        expr = f"{de[corr[ask]]}*{p}/{q}"
        return MARK(stem, v, st[-1], expr, d=1, fig=fig, ap=ap, steps=st,
                    alt=["比例式 $a:b=c:d$ ならば $ad=bc$ を使って方程式として解いてもよい。"],
                    pc=[("相似比を正しく求めている", 1), ("正しい長さを求めている", 1)],
                    pit=["対応しない辺どうしで比をつくる。"])
    known = r.choice(list(corr))
    stem = f"右の図で，△ABC∽△DEF である。{gs}，{corr[known]}$={de[corr[known]]}$ cm のとき，△ABC と △DEF の相似比を最も簡単な整数の比で表しなさい。"
    st = [f"{known} と {corr[known]} が対応する。", f"${abc[known]}:{de[corr[known]]}={p}:{q}$。"]
    return RATIO(stem, p, q, st[-1], f"Rational({abc[known]},{de[corr[known]]})", d=1, fig=fig, ap=ap, steps=st,
                 alt=["ほかの辺も同じ比になることを確かめると、対応のまちがいに気づける。"],
                 pc=[("対応する辺を選んでいる", 1), ("最も簡単な整数の比にしている", 1)],
                 pit=["約分（比を簡単にすること）を忘れる。", "対応しない辺の比を答える。"])


CONDS = ["3組の辺の比がすべて等しい", "2組の辺の比とその間の角がそれぞれ等しい", "2組の角がそれぞれ等しい", "相似であるとはいえない"]


@gen("basic_check", 4, ["condition_check", "concept"])
def a_sim_cond(r):
    a0, b0, c0 = r.choice(BASES)
    p, q = r.choice([x for x in RATIOS if 1 not in x or x[0] == 1])
    t1 = r.choice(range(30, 81, 5))
    t2 = r.choice([x for x in range(35, 96, 5) if x + t1 < 160 and x != t1])
    kind = r.choice(["sss", "sas", "aa", "aa2", "none_a", "none_s"])
    if kind == "sss":
        info = f"AB$={c0 * p}$ cm，BC$={a0 * p}$ cm，CA$={b0 * p}$ cm，DE$={c0 * q}$ cm，EF$={a0 * q}$ cm，FD$={b0 * q}$ cm"
        k, why_ok = 0, f"AB：DE$=$BC：EF$=$CA：FD$={p}:{q}$ で，3組の辺の比がすべて等しい。"
    elif kind == "sas":
        info = f"AB$={c0 * p}$ cm，AC$={b0 * p}$ cm，${A('A')}={t1}^\\circ$，DE$={c0 * q}$ cm，DF$={b0 * q}$ cm，${A('D')}={t1}^\\circ$"
        k, why_ok = 1, f"AB：DE$=$AC：DF$={p}:{q}$ で，その間の角 ${A('A')}={A('D')}$。"
    elif kind == "aa":
        info = f"${A('A')}={t1}^\\circ$，${A('B')}={t2}^\\circ$，${A('D')}={t1}^\\circ$，${A('E')}={t2}^\\circ$"
        k, why_ok = 2, f"${A('A')}={A('D')}$，${A('B')}={A('E')}$ で，2組の角がそれぞれ等しい。"
    elif kind == "aa2":
        info = f"${A('A')}={t1}^\\circ$，${A('B')}={t2}^\\circ$，${A('D')}={t1}^\\circ$，${A('F')}={180 - t1 - t2}^\\circ$"
        k, why_ok = 2, f"${A('C')}=180^\\circ-{t1}^\\circ-{t2}^\\circ={180 - t1 - t2}^\\circ={A('F')}$ なので，${A('A')}={A('D')}$，${A('C')}={A('F')}$ の2組の角がそれぞれ等しい。"
    elif kind == "none_a":
        info = f"AB$={c0 * p}$ cm，BC$={a0 * p}$ cm，${A('A')}={t1}^\\circ$，DE$={c0 * q}$ cm，EF$={a0 * q}$ cm，${A('D')}={t1}^\\circ$"
        k, why_ok = 3, f"AB：DE$=$BC：EF$={p}:{q}$ だが，等しい角 ${A('A')}$，${A('D')}$ は2辺の間の角ではない。この条件だけでは相似とはいえない。"
    else:
        bad = b0 * q + 1
        info = f"AB$={c0 * p}$ cm，BC$={a0 * p}$ cm，CA$={b0 * p}$ cm，DE$={c0 * q}$ cm，EF$={a0 * q}$ cm，FD$={bad}$ cm"
        k, why_ok = 3, f"AB：DE$=$BC：EF$={p}:{q}$ だが，CA：FD$={b0 * p}:{bad}$ は ${p}:{q}$ と等しくない。"
    right = CONDS[k]
    why = {
        0: "3組の辺の比がすべてわかっているわけではない。",
        1: "2組の辺の比と，その間の角がそろっていない。",
        2: "わかっている角は2組そろっていない。",
        3: "相似条件の1つにあてはまるので，相似であるといえる。",
    }
    if kind == "none_s":
        why[0] = "CA：FD の比が，AB：DE，BC：EF の比と等しくない。"
    if kind == "none_a":
        why[1] = f"等しい角 {'$'}{A('A')}{'$'}，{'$'}{A('D')}{'$'} は，比が等しい2辺の間の角ではない。"
    cands = [(CONDS[i], why[i], "相似条件の取り違え") for i in range(4) if i != k]
    return MC(f"△ABC と △DEF で，{info} である。このとき，2つの三角形が相似であるかどうかと，その根拠について述べたものとして最も適するものを，" + SEL4,
              right, cands, f"{why_ok}よって「{right}」。", d=2,
              ap="与えられた辺の比・角が，相似条件（3組の辺の比／2組の辺の比とその間の角／2組の角）のどれかにぴったりあてはまるかを確かめる。",
              steps=["辺の比を計算し，等しい角がどの位置にあるかを確かめる。", why_ok, f"答え：「{right}」。"],
              alt=["与えられた条件で三角形をかき，形が1通りに決まるかどうかを考えて確かめる。"],
              pc=[("辺の比・角の位置を正しく調べている", 1), ("正しい相似条件を選んでいる", 1)],
              pit=["等しい角が2辺の「間の角」かどうかを確かめない。", "2組の辺の比だけで相似と判断する。"])


@gen("basic_check", 4, ["computation"])
def a_parallel(r):
    p, q = r.sample(range(2, 10), 2)
    kind = r.choice(["de", "ec", "bc", "ad"])
    t = p / (p + q)
    fig = fig_de_bc(min(max(t, 0.25), 0.75), "辺 AB 上の点 D，辺 AC 上の点 E で DE//BC")
    head = "右の図のように，△ABC の辺 AB，AC 上にそれぞれ点 D，E があり，DE//BC である。"
    if kind == "de":
        x = r.randint(4, 20)
        v = Fr(x * p, p + q)
        stem = head + f"AD$={p}$ cm，DB$={q}$ cm，BC$={x}$ cm のとき，線分 DE の長さは何 cm か，求めなさい。"
        st = ["DE//BC より △ADE∽△ABC。", f"相似比は AD：AB$={p}:{p + q}$。", f"DE$={x}\\times\\dfrac{{{p}}}{{{p + q}}}={ftex(v)}$ cm。"]
        expr = f"Rational({x}*{p},{p + q})"
    elif kind == "ec":
        y = r.randint(2, 15)
        v = Fr(y * q, p)
        stem = head + f"AD$={p}$ cm，DB$={q}$ cm，AE$={y}$ cm のとき，線分 EC の長さは何 cm か，求めなさい。"
        st = ["DE//BC より AD：DB$=$AE：EC。", f"${p}:{q}={y}:$ EC。", f"EC$={y}\\times\\dfrac{{{q}}}{{{p}}}={ftex(v)}$ cm。"]
        expr = f"Rational({y}*{q},{p})"
    elif kind == "bc":
        z = r.randint(2, 15)
        v = Fr(z * (p + q), p)
        stem = head + f"AD$={p}$ cm，DB$={q}$ cm，DE$={z}$ cm のとき，辺 BC の長さは何 cm か，求めなさい。"
        st = ["DE//BC より △ADE∽△ABC。", f"DE：BC$=$AD：AB$={p}:{p + q}$。", f"BC$={z}\\times\\dfrac{{{p + q}}}{{{p}}}={ftex(v)}$ cm。"]
        expr = f"Rational({z}*{p + q},{p})"
    else:
        s = r.randint(5, 18)
        v = Fr(s * p, p + q)
        stem = head + f"AB$={s}$ cm，AE$={p}$ cm，EC$={q}$ cm のとき，線分 AD の長さは何 cm か，求めなさい。"
        st = ["DE//BC より AD：AB$=$AE：AC。", f"AE：AC$={p}:{p + q}$。", f"AD$={s}\\times\\dfrac{{{p}}}{{{p + q}}}={ftex(v)}$ cm。"]
        expr = f"Rational({s}*{p},{p + q})"
    return MARK(stem, v, st[-1], expr, d=2, fig=fig,
                ap="DE//BC なら △ADE∽△ABC。DE：BC は「上の部分：全体」の比（AD：AB）に等しい。AD：DB$=$AE：EC も成り立つ。",
                steps=st,
                alt=["求めた長さを使って，他の辺の比も同じになっているかを確かめる。"],
                pc=[("正しい比を選んでいる", 1), ("正しい長さを求めている", 1)],
                pit=["DE：BC を AD：DB と等しいとしてしまう。"])


@gen("basic_check", 4, ["computation", "concept"])
def a_midpoint(r):
    kind = r.choice(["mn", "bc", "tri", "quad", "trap"])
    P = dict(STD)
    if kind in ("mn", "bc"):
        P["M"] = lerp(P["A"], P["B"], 0.5)
        P["N"] = lerp(P["A"], P["C"], 0.5)
        fig = figure("辺 AB，AC の中点 M，N", geo(P, segs=[("A", "B"), ("B", "C"), ("C", "A"), ("M", "N")], ticks=[("A", "M", 1), ("M", "B", 1), ("A", "N", 2), ("N", "C", 2)], off={"M": (-0.35, 0.05), "N": (0.35, 0.05)}))
        if kind == "mn":
            x = r.randint(5, 29)
            v = Fr(x, 2)
            stem = f"右の図のように，△ABC の辺 AB，AC の中点をそれぞれ M，N とする。BC$={x}$ cm のとき，線分 MN の長さは何 cm か，求めなさい。"
            st = ["中点連結定理より MN$=\\dfrac{1}{2}$BC。", f"MN$=\\dfrac{{1}}{{2}}\\times{x}={ftex(v)}$ cm。"]
            expr = f"Rational({x},2)"
        else:
            x = r.randint(3, 19)
            v = 2 * x
            stem = f"右の図のように，△ABC の辺 AB，AC の中点をそれぞれ M，N とすると，MN$={x}$ cm であった。辺 BC の長さは何 cm か，求めなさい。"
            st = ["中点連結定理より MN$=\\dfrac{1}{2}$BC。", f"BC$=2\\times{x}={v}$ cm。"]
            expr = f"2*{x}"
    elif kind == "tri":
        a, b, c = sorted(r.sample(range(4, 16), 3))
        if a + b <= c:
            raise AssertionError
        a, b, c = r.sample([a, b, c], 3)
        v = Fr(a + b + c, 2)
        P["D"], P["E"], P["F"] = lerp(P["B"], P["C"], 0.5), lerp(P["C"], P["A"], 0.5), lerp(P["A"], P["B"], 0.5)
        fig = figure("3辺の中点 D，E，F", geo(P, segs=[("A", "B"), ("B", "C"), ("C", "A"), ("D", "E"), ("E", "F"), ("F", "D")], off={"D": (0, -0.4), "E": (0.35, 0.1), "F": (-0.35, 0.1)}))
        stem = f"右の図のように，BC$={a}$ cm，CA$={b}$ cm，AB$={c}$ cm の △ABC の辺 BC，CA，AB の中点をそれぞれ D，E，F とする。△DEF の周の長さは何 cm か，求めなさい。"
        st = ["中点連結定理より EF$=\\dfrac{1}{2}$BC，FD$=\\dfrac{1}{2}$CA，DE$=\\dfrac{1}{2}$AB。", f"周の長さ$=\\dfrac{{1}}{{2}}({a}+{b}+{c})={ftex(v)}$ cm。"]
        expr = f"Rational({a}+{b}+{c},2)"
    elif kind == "quad":
        x, y = r.sample(range(4, 20), 2)
        v = x + y
        Q = {"A": (0.6, 2.6), "B": (0.0, 0.0), "C": (4.6, 0.3), "D": (3.8, 3.0)}
        Q["P"], Q["Q"], Q["R"], Q["S"] = lerp(Q["A"], Q["B"], 0.5), lerp(Q["B"], Q["C"], 0.5), lerp(Q["C"], Q["D"], 0.5), lerp(Q["D"], Q["A"], 0.5)
        fig = figure("四角形 ABCD の各辺の中点 P，Q，R，S", geo(Q, segs=[("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("P", "Q"), ("Q", "R"), ("R", "S"), ("S", "P")], dashed=[("A", "C"), ("B", "D")]))
        stem = f"右の図のように，四角形 ABCD の辺 AB，BC，CD，DA の中点をそれぞれ P，Q，R，S とする。対角線 AC$={x}$ cm，BD$={y}$ cm のとき，四角形 PQRS の周の長さは何 cm か，求めなさい。"
        st = ["△ABC で中点連結定理より PQ$=\\dfrac{1}{2}$AC。同様に SR$=\\dfrac{1}{2}$AC。", "△ABD，△CBD で PS$=$QR$=\\dfrac{1}{2}$BD。", f"周の長さ$=$AC$+$BD$={x}+{y}={v}$ cm。"]
        expr = f"{x}+{y}"
    else:
        a = r.randint(2, 12)
        b = a + r.randint(2, 12)
        v = Fr(a + b, 2)
        T = {"A": (1.0, 2.4), "D": (3.4, 2.4), "B": (0.0, 0.0), "C": (5.0, 0.0)}
        T["M"], T["N"] = lerp(T["A"], T["B"], 0.5), lerp(T["D"], T["C"], 0.5)
        fig = figure("AD//BC の台形 ABCD と，AB，DC の中点 M，N", geo(T, segs=[("A", "D"), ("D", "C"), ("C", "B"), ("B", "A"), ("M", "N")], dashed=[("A", "C")], off={"M": (-0.35, 0), "N": (0.35, 0)}))
        stem = f"右の図のように，AD//BC の台形 ABCD で，辺 AB，DC の中点をそれぞれ M，N とする。AD$={a}$ cm，BC$={b}$ cm のとき，線分 MN の長さは何 cm か，求めなさい。"
        st = ["対角線 AC をひき，MN との交点を P とする。", f"△ABC で MP$=\\dfrac{{1}}{{2}}$BC$={ftex(Fr(b, 2))}$，△CDA で PN$=\\dfrac{{1}}{{2}}$AD$={ftex(Fr(a, 2))}$。",
              f"MN$=\\dfrac{{{a}+{b}}}{{2}}={ftex(v)}$ cm。"]
        expr = f"Rational({a}+{b},2)"
    return MARK(stem, v, st[-1], expr, d=2, fig=fig,
                ap="中点が2つあれば中点連結定理（2辺の中点を結ぶ線分は，残りの辺に平行で長さは半分）が使えないかを考える。必要なら対角線をひいて三角形をつくる。",
                steps=st,
                alt=["相似比 $1:2$ の相似な三角形（△AMN∽△ABC など）を見つけて求めることもできる。"],
                pc=[("中点連結定理を正しく使っている", 1), ("正しい長さを求めている", 1)],
                pit=["半分ではなく2倍にしてしまう。", "どの辺に対応する線分かを取り違える。"])


@gen("basic_check", 4, ["computation", "concept"])
def a_area_vol(r):
    p, q = r.choice([x for x in RATIOS if max(x) <= 5 and x[0] < x[1]] + [(2, 7), (3, 7), (4, 7), (5, 6), (5, 7), (6, 7)])
    kind = r.choice(["area_ratio", "area_val", "vol_ratio", "vol_val", "back"])
    ap = "相似比が $m:n$ のとき，面積比（表面積の比）は $m^2:n^2$，体積比は $m^3:n^3$。"
    if kind == "area_ratio":
        stem = f"相似比が ${p}:{q}$ の2つの三角形 P，Q がある。P と Q の面積の比を最も簡単な整数の比で表しなさい。"
        st = ["面積比は相似比の2乗。", f"${p}^2:{q}^2={p * p}:{q * q}$。"]
        return RATIO(stem, p * p, q * q, st[-1], f"Rational({p}**2,{q}**2)", d=1, ap=ap, steps=st,
                     alt=["1辺の長さが $p$，$q$ の正方形で考えると，面積は $p^2$，$q^2$ になることから確かめられる。"],
                     pc=[("面積比は相似比の2乗であることを使っている", 1), ("正しい比", 1)],
                     pit=["面積比を相似比と同じ比にしてしまう。"])
    if kind == "vol_ratio":
        stem = f"相似な2つの三角柱 P，Q があり，その相似比は ${p}:{q}$ である。P と Q の体積の比を最も簡単な整数の比で表しなさい。"
        st = ["体積比は相似比の3乗。", f"${p}^3:{q}^3={p ** 3}:{q ** 3}$。"]
        return RATIO(stem, p ** 3, q ** 3, st[-1], f"Rational({p}**3,{q}**3)", d=1, ap=ap, steps=st,
                     alt=["縦・横・高さがすべて相似比の割合になるので，体積は相似比を3回かけた割合になる。"],
                     pc=[("体積比は相似比の3乗であることを使っている", 1), ("正しい比", 1)],
                     pit=["体積比を相似比の2乗にしてしまう。"])
    if kind == "back":
        stem = f"相似な2つの四角形 P，Q があり，P と Q の面積の比は ${p * p}:{q * q}$ である。P と Q の相似比を最も簡単な整数の比で表しなさい。"
        st = ["面積比は相似比の2乗なので，相似比は面積比のそれぞれの数の平方根の比。", f"${p * p}:{q * q}=({p})^2:({q})^2$ より ${p}:{q}$。"]
        return RATIO(stem, p, q, st[-1], f"sqrt({p * p})/sqrt({q * q})", d=2, ap=ap, steps=st,
                     alt=[f"相似比を ${p}:{q}$ として，2乗すると ${p * p}:{q * q}$ になるか確かめる。"],
                     pc=[("面積比から相似比を逆に考えている", 1), ("正しい比", 1)],
                     pit=["面積比をそのまま相似比と考える。", "面積比を2でわってしまう。"])
    if kind == "area_val":
        S = p * p * r.randint(2, 12)
        v = Fr(S * q * q, p * p)
        stem = f"相似比が ${p}:{q}$ の2つの図形 P，Q がある。P の面積が ${S}$ cm² のとき，Q の面積は何 cm² か，求めなさい。"
        st = [f"面積比は ${p * p}:{q * q}$。", f"Q の面積$={S}\\times\\dfrac{{{q * q}}}{{{p * p}}}={ftex(v)}$ cm²。"]
        expr = f"Rational({S}*{q * q},{p * p})"
    else:
        V = p ** 3 * r.randint(1, 6)
        v = Fr(V * q ** 3, p ** 3)
        stem = f"相似な2つの直方体 P，Q があり，その相似比は ${p}:{q}$ である。P の体積が ${V}$ cm³ のとき，Q の体積は何 cm³ か，求めなさい。"
        st = [f"体積比は ${p ** 3}:{q ** 3}$。", f"Q の体積$={V}\\times\\dfrac{{{q ** 3}}}{{{p ** 3}}}={ftex(v)}$ cm³。"]
        expr = f"Rational({V}*{q ** 3},{p ** 3})"
    return MARK(stem, v, st[-1], expr, d=2, ap=ap, steps=st,
                alt=["比例式（面積や体積の比＝相似比の2乗・3乗）を立てて解いてもよい。"],
                pc=[("面積比・体積比を正しく求めている", 1), ("正しい値を求めている", 1)],
                pit=["面積や体積にも相似比をそのまま使う。"])


# ======================================================================
# B 標準演習
# ======================================================================

SHADOW_RATIOS = [(3, 4), (4, 5), (2, 3), (5, 4), (6, 5), (3, 2), (5, 6), (4, 3), (5, 8), (7, 5)]


@gen("standard_practice", 4, ["application", "computation"])
def b_shadow(r):
    kind = r.choice(["shadow", "shadow", "scale"])
    if kind == "shadow":
        p, q = r.choice(SHADOW_RATIOS)
        t = r.choice([x for x in (10, 20, 25, 30) if p * x <= 200 and q * x <= 200])
        a, b = p * t, q * t
        u = r.randint(2, 9)
        c, v = q * u, p * u
        obj = r.choice(["木", "旗ざお", "電柱", "校舎"])
        stem = (f"Kさんは，{obj}の高さを調べるため，地面に垂直に長さ ${a}$ cm の棒を立てた。このとき棒の影の長さは ${b}$ cm であった。"
                f"同じ時刻に，{obj}の影の長さは ${c}$ m であった。{obj}の高さは何 m か，求めなさい。ただし，地面は平らであるものとする。")
        st = ["太陽の光は平行と考えると，棒と影がつくる直角三角形と，" + obj + "と影がつくる直角三角形は相似（2組の角が等しい）。",
              f"高さ：影の長さ$={a}:{b}={p}:{q}$。", f"{obj}の高さ$={c}\\times\\dfrac{{{p}}}{{{q}}}={v}$ m。"]
        expr = f"{c}*Rational({a},{b})"
        alt = ["単位を cm にそろえて比例式を立て，最後に m にもどしても同じ結果になる。"]
    else:
        n = r.choice([200, 250, 400, 500, 1000])
        x = r.choice([k for k in range(2, 20) if (k * n) % 100 == 0 and k * n <= 3000])
        v = x * n // 100
        stem = (f"Kさんは，地面の上の地点 P から木の先端を見上げたようすを，${n}$ 分の1の縮図に表した。縮図上で木の高さにあたる線分の長さは ${x}$ cm であった。"
                "実際の木の高さは何 m か，求めなさい。ただし，地点 P の高さは考えないものとする。")
        st = [f"縮図は実際の図形と相似で，相似比は $1:{n}$。", f"実際の高さ$={x}\\times{n}={x * n}$ cm $={v}$ m。"]
        expr = f"{x}*{n}/100"
        alt = ["縮図上の 1 cm が実際の何 m にあたるかを先に求めてからかけてもよい。"]
    return MARK(stem, v, st[-1], expr, d=3, p=4,
                ap="実際の図形と，影や縮図でできる図形が相似になることを使う。対応する長さの比が等しい。",
                steps=st, alt=alt,
                pc=[("相似な図形を見つけて比を立てている", 2), ("単位をそろえて正しい値を求めている", 2)],
                pit=["cm と m の単位をそろえずに計算する。", "比を逆にする。"])


@gen("standard_practice", 4, ["computation", "application"])
def b_trapezoid(r):
    a, b = r.sample(range(2, 13), 2)
    if a > b:
        a, b = b, a
    if b - a < 1 or math.gcd(a, b) == b:
        pass
    kind = r.choice(["ratio", "ao", "ef", "area"])
    head = f"右の図のように，AD//BC，AD$={a}$ cm，BC$={b}$ cm の台形 ABCD で，対角線 AC と BD の交点を O とする。"
    st0 = ["AD//BC より錯角が等しいので，△OAD∽△OCB（2組の角）。", f"相似比は AD：CB$={a}:{b}$。"]
    if kind == "ratio":
        stem = head + "AO：OC を最も簡単な整数の比で表しなさい。"
        st = st0 + [f"AO：OC$={a}:{b}$" + ("。" if math.gcd(a, b) == 1 else f"$={a // math.gcd(a, b)}:{b // math.gcd(a, b)}$。")]
        return RATIO(stem, a, b, st[-1], f"Rational({a},{b})", d=3, p=4, fig=fig_trap(a, b),
                     ap="平行線があるときは錯角が等しい。対角線の交点のまわりに相似な三角形ができる。",
                     steps=st, alt=["△OAD と △OCB の相似比が AD：BC で決まることを，同じ形の「ちょうちょ型」の図として覚えておく。"],
                     pc=[("相似な三角形を見つけている", 2), ("正しい比", 2)],
                     pit=["AO：OC を AD：AB などと取り違える。"])
    if kind == "ao":
        L = (a + b) * r.randint(1, 3) + r.choice([0, 1, 2])
        v = Fr(L * a, a + b)
        stem = head + f"AC$={L}$ cm のとき，線分 AO の長さは何 cm か，求めなさい。"
        st = st0 + [f"AO：AC$={a}:{a + b}$。", f"AO$={L}\\times\\dfrac{{{a}}}{{{a + b}}}={ftex(v)}$ cm。"]
        expr = f"Rational({L}*{a},{a + b})"
        fig = fig_trap(a, b)
    elif kind == "ef":
        v = Fr(2 * a * b, a + b)
        stem = head + "点 O を通り辺 BC に平行な直線が，辺 AB，DC と交わる点をそれぞれ E，F とする。線分 EF の長さは何 cm か，求めなさい。"
        st = st0 + [f"BO：BD$={b}:{a + b}$。△BAD で EO//AD より EO$={a}\\times\\dfrac{{{b}}}{{{a + b}}}={ftex(Fr(a * b, a + b))}$。",
                    f"同様に △CDA で OF$={ftex(Fr(a * b, a + b))}$。", f"EF$=2\\times{ftex(Fr(a * b, a + b))}={ftex(v)}$ cm。"]
        expr = f"Rational(2*{a}*{b},{a + b})"
        fig = fig_trap(a, b, extra=True)
    else:
        S = a * a * r.randint(1, 4)
        v = Fr(S * b * b, a * a)
        stem = head + f"△OAD の面積が ${S}$ cm² のとき，△OBC の面積は何 cm² か，求めなさい。"
        st = st0 + [f"面積比は ${a * a}:{b * b}$。", f"△OBC$={S}\\times\\dfrac{{{b * b}}}{{{a * a}}}={ftex(v)}$ cm²。"]
        expr = f"Rational({S}*{b * b},{a * a})"
        fig = fig_trap(a, b)
    return MARK(stem, v, st[-1], expr, d=3, p=4, fig=fig,
                ap="AD//BC の台形では，対角線の交点 O のまわりに △OAD∽△OCB ができる（錯角が等しい）。相似比は AD：BC。",
                steps=st,
                alt=["高さが共通な三角形の面積比は底辺の比になることを使って確かめることもできる。"],
                pc=[("相似な三角形と相似比を見つけている", 2), ("正しい値を求めている", 2)],
                pit=["AO：AC を AD：BC としてしまう（全体との比にしない）。", "面積比に相似比をそのまま使う。"])


@gen("standard_practice", 4, ["computation", "condition_check"])
def b_three_parallel(r):
    kind = r.choice(["lines", "lines", "lines2", "trap"])
    if kind in ("lines", "lines2"):
        P = {"A": (0.4, 3.0), "B": (1.2, 1.6), "C": (2.2, 0.0), "D": (3.4, 3.0), "E": (3.2, 1.6), "F": (2.9, 0.0),
             "l0": (-0.6, 3.0), "l1": (4.6, 3.0), "m0": (-0.6, 1.6), "m1": (4.6, 1.6), "n0": (-0.6, 0.0), "n1": (4.6, 0.0)}
        P["A"] = (0.4, 3.0)
        fig = figure("3本の平行な直線 ℓ，m，n と2本の直線", geo(P, segs=[("l0", "l1"), ("m0", "m1"), ("n0", "n1"), ("A", "C"), ("D", "F")],
                                                      names=["A", "B", "C", "D", "E", "F"], off={"A": (-0.3, 0.3), "B": (-0.35, 0.25), "C": (-0.3, -0.35), "D": (0.3, 0.3), "E": (0.35, 0.25), "F": (0.3, -0.35)},
                                                      texts=[(4.9, 3.0, "ℓ"), (4.9, 1.6, "m"), (4.9, 0.0, "n")]))
        a, b = r.sample(range(2, 13), 2)
        if kind == "lines":
            c = r.randint(2, 14)
            v = Fr(b * c, a)
            stem = f"右の図で，3本の直線 ℓ，m，n は平行である。AB$={a}$ cm，BC$={b}$ cm，DE$={c}$ cm のとき，線分 EF の長さは何 cm か，求めなさい。"
            st = ["平行線で切りとられる線分の比は等しいので AB：BC$=$DE：EF。", f"${a}:{b}={c}:$ EF。", f"EF$={ftex(v)}$ cm。"]
            expr = f"Rational({b}*{c},{a})"
        else:
            c = r.randint(2, 12)
            t = c + r.randint(2, 12)
            v = Fr(a * (t - c), c)
            stem = f"右の図で，3本の直線 ℓ，m，n は平行である。AB$={a}$ cm，DE$={c}$ cm，DF$={t}$ cm のとき，線分 BC の長さは何 cm か，求めなさい。"
            st = [f"EF$=$DF$-$DE$={t}-{c}={t - c}$ cm。", "AB：BC$=$DE：EF より " + f"${a}:$ BC $={c}:{t - c}$。", f"BC$={ftex(v)}$ cm。"]
            expr = f"Rational({a}*({t}-{c}),{c})"
    else:
        p, q = r.sample(range(1, 7), 2)
        a = r.randint(2, 10)
        b = a + r.randint(2, 10)
        v = Fr(q * a + p * b, p + q)
        T = {"A": (1.0, 2.6), "D": (3.4, 2.6), "B": (0.0, 0.0), "C": (5.0, 0.0)}
        tt = p / (p + q)
        T["E"], T["F"] = lerp(T["A"], T["B"], tt), lerp(T["D"], T["C"], tt)
        fig = figure("AD//EF//BC の台形", geo(T, segs=[("A", "D"), ("D", "C"), ("C", "B"), ("B", "A"), ("E", "F")], dashed=[("A", "C")], off={"E": (-0.35, 0), "F": (0.35, 0)}))
        stem = (f"右の図のように，AD//BC の台形 ABCD で，辺 AB 上に AE：EB$={p}:{q}$ となる点 E をとり，E を通り BC に平行な直線と辺 DC との交点を F とする。"
                f"AD$={a}$ cm，BC$={b}$ cm のとき，線分 EF の長さは何 cm か，求めなさい。")
        st = ["対角線 AC をひき，EF との交点を G とする。", f"△ABC で EG//BC より EG$={b}\\times\\dfrac{{{p}}}{{{p + q}}}={ftex(Fr(b * p, p + q))}$。",
              f"△CDA で GF//AD，CG：CA$=$BE：BA$={q}:{p + q}$ より GF$={a}\\times\\dfrac{{{q}}}{{{p + q}}}={ftex(Fr(a * q, p + q))}$。",
              f"EF$=$EG$+$GF$={ftex(v)}$ cm。"]
        expr = f"Rational({b}*{p}+{a}*{q},{p + q})"
    return MARK(stem, v, st[-1], expr, d=3, p=4, fig=fig,
                ap="平行線と線分の比を使う。台形では対角線をひいて2つの三角形に分け，それぞれで「三角形と比の定理」を使う。",
                steps=st,
                alt=["台形では，A を通り DC に平行な直線をひいて平行四辺形と三角形に分ける方法でも求められる。"],
                pc=[("平行線と線分の比の関係を正しく立てている", 2), ("正しい長さを求めている", 2)],
                pit=["対応しない線分どうしで比をつくる。", "台形で EF を AD と BC の平均と決めつける（中点のときだけ成り立つ）。"])


PROOFS = [
    dict(pts={"A": (0, 0), "B": (5, 0), "C": (1.8, 2.4), "D": (1.8, 0)}, segs=[("A", "B"), ("B", "C"), ("C", "A"), ("C", "D")], off={"D": (0, -0.4)},
         setup="右の図のように，${C}=90^\\circ$ の直角三角形 ABC で，頂点 C から辺 AB に垂線 CD をひく。このとき，△ABC∽△ACD であることを次のように証明した。",
         body=["△ABC と △ACD において，", "仮定から　${ACB}={ADC}=90^\\circ$　……①", "（a）だから　${BAC}={CAD}$　……②", "①，②から，（b）ので，△ABC∽△ACD"],
         a="∠A は共通", b="2組の角がそれぞれ等しい"),
    dict(pts=None, segs=None, off=None,
         setup="右の図のように，△ABC の辺 AB，AC 上にそれぞれ点 D，E があり，DE//BC である。このとき，△ADE∽△ABC であることを次のように証明した。",
         body=["△ADE と △ABC において，", "DE//BC より，（a）は等しいから　${ADE}={ABC}$　……①", "∠A は共通　……②", "①，②から，（b）ので，△ADE∽△ABC"],
         a="同位角", b="2組の角がそれぞれ等しい"),
    dict(pts={"A": (0, 2.4), "C": (1.8, 2.4), "O": inter((0, 2.4), (3.0, -1.0), (1.8, 2.4), (0.0, -1.0)), "B": (3.0, -1.0), "D": (0.0, -1.0)}, segs=[("A", "B"), ("C", "D"), ("A", "C"), ("D", "B")], off={"O": (0.4, 0)},
         setup="右の図のように，2つの線分 AB，CD が点 O で交わり，AC//DB である。このとき，△OAC∽△OBD であることを次のように証明した。",
         body=["△OAC と △OBD において，", "AC//DB より，（a）は等しいから　${OAC}={OBD}$　……①", "対頂角は等しいから　${AOC}={BOD}$　……②", "①，②から，（b）ので，△OAC∽△OBD"],
         a="錯角", b="2組の角がそれぞれ等しい"),
    dict(pts={"O": (2.0, 1.4), "A": (0.0, 2.0), "B": (1.4, 2.6), "C": (5.0, 0.5), "D": (2.9, -0.4)}, segs=[("A", "C"), ("B", "D"), ("A", "B"), ("D", "C")], off={"O": (0, 0.42)},
         setup="右の図のように，2つの線分 AC，BD が点 O で交わり，OA$={oa}$ cm，OB$={ob}$ cm，OC$={oc}$ cm，OD$={od}$ cm である。このとき，△OAB∽△OCD であることを次のように証明した。",
         body=["△OAB と △OCD において，", "OA：OC$={r1}$，OB：OD$={r2}$　……①", "（a）は等しいから　${AOB}={COD}$　……②", "①，②から，（b）ので，△OAB∽△OCD"],
         a="対頂角", b="2組の辺の比とその間の角がそれぞれ等しい"),
    dict(pts={"A": (1.4, 3.0), "B": (0, 0), "C": (5.0, 0), "D": (1.8, 0)}, segs=[("A", "B"), ("B", "C"), ("C", "A"), ("A", "D")], off={"D": (0, -0.4)},
         setup="右の図のように，△ABC の辺 BC 上に，${BAD}={BCA}$ となる点 D をとる。このとき，△ABD∽△CBA であることを次のように証明した。",
         body=["△ABD と △CBA において，", "仮定から　${BAD}={BCA}$　……①", "（a）だから　${ABD}={CBA}$　……②", "①，②から，（b）ので，△ABD∽△CBA"],
         a="∠B は共通", b="2組の角がそれぞれ等しい"),
]
REASONS = ["∠A は共通", "∠B は共通", "同位角", "錯角", "対頂角"]
SCONDS = ["3組の辺の比がすべて等しい", "2組の辺の比とその間の角がそれぞれ等しい", "2組の角がそれぞれ等しい"]



@gen("standard_practice", 4, ["written_reasoning", "concept"])
def b_proof_fill(r):
    P = dict(r.choice(PROOFS))
    p, q = r.choice([(2, 3), (3, 4), (3, 5), (2, 5), (4, 5), (1, 2), (1, 3), (2, 7), (3, 7), (4, 7)])
    m1, m2 = r.randint(1, 3), r.randint(1, 3)
    vals = dict(oa=p * m1, oc=q * m1, ob=p * m2 + 0, od=q * m2, p=p, q=q)
    if vals["oa"] == vals["ob"]:
        vals["ob"], vals["od"] = p * (m2 + 1), q * (m2 + 1)

    def fmt(s):
        s = s.replace("{oa}", str(vals["oa"])).replace("{ob}", str(vals["ob"])).replace("{oc}", str(vals["oc"])).replace("{od}", str(vals["od"]))
        r1 = f"{vals['oa']}:{vals['oc']}" + ("" if vals["oa"] == p else f"={p}:{q}")
        r2 = f"{vals['ob']}:{vals['od']}" + ("" if vals["ob"] == p else f"={p}:{q}")
        s = s.replace("{r1}", r1).replace("{r2}", r2)
        return re.sub(r"\{([A-Z]{1,3})\}", lambda m: A(m.group(1)), s)
    if P["pts"] is None:
        fig = fig_de_bc(r.choice([0.35, 0.45, 0.55]))
    else:
        fig = figure("証明の図", geo(P["pts"], segs=P["segs"], off=P["off"]))
    wa = [x for x in REASONS if x != P["a"]]
    wb = [x for x in SCONDS if x != P["b"]]

    def C(a, b):
        return f"（a）{a}　（b）{b}"
    cands = [(C(r.choice(wa), P["b"]), f"（a）は{P['a']}である。図で，その角がなぜ等しいかを確かめる。", "根拠の取り違え"),
             (C(P["a"], r.choice(wb)), f"①，②でそろったのは「{P['b']}」という条件である。", "相似条件の取り違え"),
             (C(r.choice(wa), r.choice(wb)), f"（a）は{P['a']}，（b）は「{P['b']}」である。", "根拠と相似条件の取り違え"),
             (C(P["a"], r.choice(wb)), f"①，②でそろったのは「{P['b']}」である。", "相似条件の取り違え"),
             (C(r.choice(wa), P["b"]), f"（a）は{P['a']}である。", "根拠の取り違え")]
    body = "\n".join(fmt(x) for x in P["body"])
    setup = fmt(P["setup"])
    return MC(setup + f"\n〔証明〕\n{body}\n上の証明の（a），（b）にあてはまるものの組み合わせとして最も適するものを，" + SEL4,
              C(P["a"], P["b"]), cands, f"（a）は{P['a']}，（b）は「{P['b']}」。", d=3, p=4, fig=fig,
              ap="（a）は，その行で等しいといっている角が，なぜ等しいのか（共通・同位角・錯角・対頂角）を図で確かめる。（b）は①，②でそろったものが辺の比か角かで決める。",
              steps=[f"（a）：{P['a']}。", f"①，②は「{P['b']}」の形になっている。", f"よって（a）{P['a']}，（b）{P['b']}。"],
              alt=["等しいとわかった角に同じ印，比が等しい辺に印をつけ，相似条件と照らし合わせる。"],
              pc=[("（a）の根拠を正しく選んでいる", 2), ("（b）の相似条件を正しく選んでいる", 2)],
              pit=["錯角と同位角を取り違える。", "辺の比が出てこないのに「辺の比」の条件を選ぶ。"])


@gen("standard_practice", 4, ["computation", "application"])
def b_area_tri(r):
    p, q = r.sample(range(1, 7), 2)
    kind = r.choice(["trap_from_small", "small_from_big", "ratio"])
    n = p + q
    fig = fig_de_bc(min(max(p / n, 0.25), 0.75))
    head = f"右の図のように，△ABC の辺 AB，AC 上にそれぞれ点 D，E があり，DE//BC，AD：DB$={p}:{q}$ である。"
    st0 = ["DE//BC より △ADE∽△ABC で，相似比は AD：AB$=" + f"{p}:{n}$。", f"面積比は △ADE：△ABC$={p * p}:{n * n}$。"]
    if kind == "trap_from_small":
        S = p * p * r.randint(1, 5)
        v = Fr(S * (n * n - p * p), p * p)
        stem = head + f"△ADE の面積が ${S}$ cm² のとき，四角形 DBCE の面積は何 cm² か，求めなさい。"
        st = st0 + [f"四角形 DBCE の面積は △ABC の ${n * n}-{p * p}={n * n - p * p}$ にあたる。", f"${S}\\times\\dfrac{{{n * n - p * p}}}{{{p * p}}}={ftex(v)}$ cm²。"]
        expr = f"Rational({S}*({n}**2-{p}**2),{p}**2)"
    elif kind == "small_from_big":
        T = n * n * r.randint(1, 3) + r.choice([0, 0, 1, 2])
        v = Fr(T * p * p, n * n)
        stem = head + f"△ABC の面積が ${T}$ cm² のとき，△ADE の面積は何 cm² か，求めなさい。"
        st = st0 + [f"△ADE$={T}\\times\\dfrac{{{p * p}}}{{{n * n}}}={ftex(v)}$ cm²。"]
        expr = f"Rational({T}*{p * p},{n * n})"
    else:
        stem = head + "△ADE と四角形 DBCE の面積の比を最も簡単な整数の比で表しなさい。"
        st = st0 + [f"△ADE：四角形 DBCE$={p * p}:({n * n}-{p * p})={p * p}:{n * n - p * p}$。"]
        return RATIO(stem, p * p, n * n - p * p, st[-1], f"Rational({p * p},{n * n - p * p})", d=3, p=4, fig=fig,
                     ap="DE//BC なら △ADE∽△ABC。相似比は AD：AB（全体との比）。面積比は相似比の2乗。四角形は △ABC から △ADE を引いた部分。",
                     steps=st, alt=["△ABC の面積を具体的な数（たとえば相似比の2乗の和）とおいて計算して確かめる。"],
                     pc=[("相似比を AD：AB で求めている", 2), ("面積比から四角形の部分を正しく求めている", 2)],
                     pit=["相似比を AD：DB にする。", "四角形の面積を △ABC の面積と取り違える。"])
    return MARK(stem, v, st[-1], expr, d=3, p=4, fig=fig,
                ap="DE//BC なら △ADE∽△ABC。相似比は AD：AB（全体との比）。面積比は相似比の2乗。四角形は △ABC から △ADE を引いた部分。",
                steps=st,
                alt=["△ABC の面積を $1$ とおいて，それぞれの部分が何倍にあたるかを考えてもよい。"],
                pc=[("相似比と面積比を正しく求めている", 2), ("正しい面積を求めている", 2)],
                pit=["相似比を AD：DB にする。", "面積比を相似比のまま使う。"])


# ======================================================================
# C 思考力・記述応用
# ======================================================================

def _xy_pool(r):
    m, n = r.choice([(2, 3), (3, 4), (2, 5), (3, 5), (4, 5), (1, 3), (5, 7)])
    return [
        ("相似な図形では，対応する角の大きさはそれぞれ等しい。", True, "相似な図形は形が同じなので，対応する角はそれぞれ等しい。"),
        (f"相似比が ${m}:{n}$ の2つの三角形の周の長さの比は ${m}:{n}$ である。", True, "周の長さは長さの和なので，相似比と同じ比になる。"),
        (f"相似比が ${m}:{n}$ の2つの三角形の面積の比は ${m}:{n}$ である。", False, f"面積の比は相似比の2乗で ${m * m}:{n * n}$ である。"),
        (f"相似比が ${m}:{n}$ の2つの立体の体積の比は ${m * m}:{n * n}$ である。", False, f"体積の比は相似比の3乗で ${m ** 3}:{n ** 3}$ である。"),
        (f"相似比が ${m}:{n}$ の2つの立体の表面積の比は ${m * m}:{n * n}$ である。", True, "表面積は面積なので，相似比の2乗の比になる。"),
        ("2つの正三角形は，いつでも相似である。", True, "どの正三角形も3つの角がすべて $60^\\circ$ なので，2組の角が等しい。"),
        ("2つの二等辺三角形は，いつでも相似である。", False, "頂角の大きさが違えば形が違うので，相似とは限らない。"),
        ("頂角が等しい2つの二等辺三角形は，いつでも相似である。", True, "頂角が等しければ底角も等しくなり，2組の角がそれぞれ等しい。"),
        ("2つの直角三角形は，いつでも相似である。", False, "直角以外の角が違えば形が違うので，相似とは限らない。"),
        ("2つの円は，いつでも相似である。", True, "円は半径の比で拡大・縮小すると重ねられるので，いつでも相似である。"),
        ("2つのひし形は，いつでも相似である。", False, "ひし形は角の大きさが違うと形が違うので，相似とは限らない。"),
        ("2つの長方形は，いつでも相似である。", False, "縦と横の比が違えば形が違うので，相似とは限らない。"),
        ("2つの正方形は，いつでも相似である。", True, "どの正方形も4つの角が直角で，となり合う辺の比が $1:1$ なので相似である。"),
        ("1組の角がそれぞれ等しい2つの三角形は，いつでも相似である。", False, "相似条件は「2組の角」。1組だけでは形が決まらない。"),
        ("三角形の2辺の中点を結ぶ線分の長さは，残りの辺の長さの半分である。", True, "中点連結定理である。"),
        ("三角形の2辺の中点を結ぶ線分の長さは，残りの辺の長さの2倍である。", False, "中点連結定理より，残りの辺の長さの半分である。"),
        ("合同な2つの図形は，相似比が $1:1$ の相似な図形と考えることができる。", True, "形も大きさも同じなので，相似比 $1:1$ の相似である。"),
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
        why[c] = (" ".join(rs), "相似の性質の思いこみ")
    return mc("相似な図形について述べた次の X，Y の文の正誤の組み合わせとして最も適するものを，" + SEL4 + f"\nX　{x[0]}\nY　{y[0]}",
              [ans] + [c for c in XY if c != ans], f"X：{x[2]}　Y：{y[2]}", d=4, p=8, why=why,
              ap="定義・相似条件・面積比や体積比の性質と照らし合わせる。「いつでも」と書かれた文は，成り立たない例（反例）がないかを探す。",
              steps=[f"X：{x[2]}", f"Y：{y[2]}", f"よって {ans}。"],
              alt=["具体的な図形（直角三角形・ひし形・長方形など）を2つかいて確かめる。"],
              pc=[("X の正誤を根拠をもって判断している", 4), ("Y の正誤を根拠をもって判断している", 4)],
              pit=["面積比・体積比を相似比と同じと考える。", "「いつでも」の反例を探さずに正しいと判断する。"])


def fig_cone(t, flip=False):
    """円錐を底面に平行な平面で切った図。t は頂点から切り口までの高さの割合。flip=True で頂点を下にする（容器）。"""
    W, H = 200, 190
    ax, ay = 100, 20
    bx, by, rx, ry = 100, 160, 70, 16
    cy = ay + (by - ay) * t
    crx, cry = rx * t, ry * t
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="serif" font-size="12">',
         f'<line x1="{ax}" y1="{ay}" x2="{bx - rx}" y2="{by}" stroke="#000" stroke-width="1.1"/>',
         f'<line x1="{ax}" y1="{ay}" x2="{bx + rx}" y2="{by}" stroke="#000" stroke-width="1.1"/>',
         f'<path d="M{bx - rx},{by} A{rx},{ry} 0 0 0 {bx + rx},{by}" fill="none" stroke="#000" stroke-width="1.1"/>',
         f'<path d="M{bx - rx},{by} A{rx},{ry} 0 0 1 {bx + rx},{by}" fill="none" stroke="#000" stroke-width="1" stroke-dasharray="4 3"/>',
         f'<ellipse cx="{bx}" cy="{_f(cy)}" rx="{_f(crx)}" ry="{_f(cry)}" fill="none" stroke="#000" stroke-width="1"/>',
         f'<line x1="{ax}" y1="{ay}" x2="{bx}" y2="{by}" stroke="#000" stroke-width="0.8" stroke-dasharray="3 3"/>',
         f'<text x="{ax}" y="{ay - 6}" text-anchor="middle">O</text>',
         "</svg>"]
    if flip:
        o[-2] = ""
        o.insert(1, f'<g transform="translate(0,{H}) scale(1,-1)">')
        o.insert(-1, "</g>")
    return "".join(o)


@gen("thinking_writing", 3, ["cross_unit", "application"], rel=["JH-MATH-G1-U06"])
def c_cone(r):
    kind = r.choice(["ratio", "frustum", "water"])
    if kind == "ratio":
        p, q = r.choice([(1, 1), (1, 2), (2, 1), (1, 3), (2, 3), (3, 2), (3, 1), (2, 5), (3, 4), (4, 3)])
        n = p + q
        fig = figure("円錐を底面に平行な平面で切った図", fig_cone(p / n))
        stem = (f"右の図のように，頂点を O とする円錐を，底面に平行な平面で，高さを頂点 O の側から ${p}:{q}$ に分けるように切り，"
                "2つの立体に分けた。頂点 O をふくむ小さい円錐を P，残りの立体を Q とするとき，P と Q の体積の比を最も簡単な整数の比で表しなさい。")
        st = [f"小さい円錐 P ともとの円錐は相似で，相似比は ${p}:{n}$。", f"体積比は P：もとの円錐$={p ** 3}:{n ** 3}$。",
              f"Q はもとの円錐から P を除いた部分なので，P：Q$={p ** 3}:({n ** 3}-{p ** 3})={p ** 3}:{n ** 3 - p ** 3}$。"]
        g = math.gcd(p ** 3, n ** 3 - p ** 3)
        if g > 1:
            st[-1] += f" よって ${p ** 3 // g}:{(n ** 3 - p ** 3) // g}$。"
        return RATIO(stem, p ** 3, n ** 3 - p ** 3, st[-1], f"Rational({p ** 3},{n ** 3 - p ** 3})", d=4, p=8, fig=fig,
                     ap="切り取った上の円錐と，もとの円錐は相似（空間図形の円錐の性質と相似の融合）。体積比は相似比の3乗。残りの立体は引き算で考える。",
                     steps=st,
                     alt=["もとの円錐の底面の半径と高さを文字でおき，円錐の体積の公式 $\\dfrac{1}{3}\\pi r^2h$ で2つの円錐の体積を直接計算して比べてもよい。"],
                     pc=[("2つの円錐が相似であることに気づいている", 3), ("体積比を相似比の3乗で求めている", 3), ("残りの立体の比を正しく求めている", 2)],
                     pit=["P：Q を相似比の3乗 $p^3:q^3$ としてしまう（Q は円錐ではない）。", "相似比を $p:q$ としてしまう。"])
    if kind == "frustum":
        p, q = r.choice([(1, 1), (1, 2), (2, 1), (1, 3), (2, 3), (3, 2), (3, 1), (3, 4)])
        n = p + q
        V = p ** 3 * r.randint(1, 6)
        v = Fr(V * (n ** 3 - p ** 3), p ** 3)
        fig = figure("円錐を底面に平行な平面で切った図", fig_cone(p / n))
        stem = (f"右の図のように，頂点を O とする円錐を，底面に平行な平面で，高さを頂点 O の側から ${p}:{q}$ に分けるように切った。"
                f"頂点 O をふくむ小さい円錐の体積が ${V}\\pi$ cm³ のとき，残りの立体の体積は何 $\\pi$ cm³ か，求めなさい。")
        st = [f"小さい円錐ともとの円錐は相似で，相似比は ${p}:{n}$，体積比は ${p ** 3}:{n ** 3}$。",
              f"もとの円錐の体積は ${V}\\pi\\times\\dfrac{{{n ** 3}}}{{{p ** 3}}}={ftex(Fr(V * n ** 3, p ** 3))}\\pi$ cm³。",
              f"残りの立体は ${ftex(Fr(V * n ** 3, p ** 3))}\\pi-{V}\\pi={ftex(v)}\\pi$ cm³。"]
        expr = f"Rational({V}*({n}**3-{p}**3),{p}**3)"
    else:
        H = r.choice([6, 8, 9, 10, 12, 15])
        h = r.choice([x for x in range(2, H) if H // math.gcd(x, H) <= 5])
        g = math.gcd(h, H)
        hp, Hp = h // g, H // g
        V = Hp ** 3 * r.randint(1, 3)
        v = Fr(V * hp ** 3, Hp ** 3)
        fig = figure("頂点を下にした円錐の容器と水", fig_cone(h / H, flip=True))
        stem = (f"深さ ${H}$ cm の円錐の形をした容器を，頂点を下にして底面が水平になるように置く。この容器の容積は ${V}$ cm³ である。"
                f"この容器に，水面が底面と平行になるように，深さ ${h}$ cm まで水を入れた。入れた水の体積は何 cm³ か，求めなさい。")
        st = [f"水の部分は，容器と相似な円錐で，相似比は ${h}:{H}={hp}:{Hp}$。", f"体積比は ${hp ** 3}:{Hp ** 3}$。",
              f"水の体積$={V}\\times\\dfrac{{{hp ** 3}}}{{{Hp ** 3}}}={ftex(v)}$ cm³。"]
        expr = f"Rational({V}*{hp}**3,{Hp}**3)"
    return MARK(stem, v, st[-1], expr, d=4, p=8, fig=fig,
                ap="円錐を底面に平行な平面で切ると，切り取った部分はもとの円錐と相似（空間図形と相似の融合）。体積比は相似比の3乗。",
                steps=st,
                alt=["底面の半径と高さを文字でおき，円錐の体積の公式 $\\dfrac{1}{3}\\pi r^2h$ を使って直接計算して確かめる。"],
                pc=[("相似な円錐を見つけ，相似比を正しく求めている", 3), ("体積比を相似比の3乗で求めている", 3), ("正しい値", 2)],
                pit=["体積比を相似比の2乗や相似比のまま使う。", "深さの比を「水の部分：空の部分」でつくってしまう。"])


@gen("thinking_writing", 3, ["cross_unit", "multiple_solutions", "application"], rel=["JH-MATH-G2-U05"])
def c_para_cross(r):
    p, q = r.sample(range(1, 6), 2)
    n = p + q
    P = {"A": (1.0, 2.6), "B": (0.0, 0.0), "C": (4.8, 0.0), "D": (5.8, 2.6)}
    P["E"] = lerp(P["A"], P["D"], p / n)
    P["F"] = inter(P["B"], P["E"], P["A"], P["C"])
    fig = figure("平行四辺形 ABCD と，辺 AD 上の点 E", geo(P, segs=[("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("B", "E"), ("A", "C")], off={"E": (0, 0.42), "F": (0.15, -0.45)}))
    head = f"右の図のように，平行四辺形 ABCD の辺 AD 上に AE：ED$={p}:{q}$ となる点 E をとり，線分 BE と対角線 AC の交点を F とする。"
    kind = r.choice(["af", "bf", "area"])
    st0 = ["AD//BC より錯角が等しいので，△FAE∽△FCB（2組の角）。", f"相似比は AE：CB$=$AE：AD$={p}:{n}$（平行四辺形の対辺は等しい）。"]
    if kind == "af":
        stem = head + "AF：FC を最も簡単な整数の比で表しなさい。"
        st = st0 + [f"AF：FC$={p}:{n}$。"]
        return RATIO(stem, p, n, st[-1], f"Rational({p},{n})", d=4, p=8, fig=fig,
                     ap="平行四辺形の対辺は平行で長さが等しい（2年の平行四辺形の性質）。平行線の間に「ちょうちょ型」の相似な三角形ができる。",
                     steps=st, alt=["BC を AD と同じ長さ $p+q$ とおき，三角形と比の定理を使っても求められる。"],
                     pc=[("相似な三角形を見つけている", 3), ("BC$=$AD を使って相似比を求めている", 3), ("正しい比", 2)],
                     pit=["相似比を AE：ED としてしまう。", "BC の長さを ED と取り違える。"])
    if kind == "bf":
        stem = head + "BF：FE を最も簡単な整数の比で表しなさい。"
        st = st0 + [f"BF：FE$=$CB：AE$={n}:{p}$。"]
        return RATIO(stem, n, p, st[-1], f"Rational({n},{p})", d=4, p=8, fig=fig,
                     ap="平行四辺形の対辺は平行で長さが等しい（2年の平行四辺形の性質）。平行線の間に「ちょうちょ型」の相似な三角形ができる。",
                     steps=st, alt=["AF：FC を先に求め，対応する辺 BF と EF の比も同じ比になることを使う。"],
                     pc=[("相似な三角形を見つけている", 3), ("対応する辺を正しく選んでいる", 3), ("正しい比", 2)],
                     pit=["対応を逆にして $p:n$ と答える。"])
    S = r.choice([24, 30, 36, 40, 48, 60, 72, 84, 90, 96, 120])
    v = Fr(S * p * p, 2 * n * (2 * p + q))
    stem = head + f"平行四辺形 ABCD の面積が ${S}$ cm² のとき，△AEF の面積は何 cm² か，求めなさい。"
    st = st0 + [f"△ABE の面積は，平行四辺形の $\\dfrac{{1}}{{2}}\\times\\dfrac{{{p}}}{{{n}}}$ で ${ftex(Fr(S * p, 2 * n))}$ cm²。",
                f"EF：EB$={p}:({p}+{n})={p}:{2 * p + q}$。",
                f"△AEF$={ftex(Fr(S * p, 2 * n))}\\times\\dfrac{{{p}}}{{{2 * p + q}}}={ftex(v)}$ cm²。"]
    return MARK(stem, v, st[-1], f"Rational({S}*{p}**2,2*{n}*(2*{p}+{q}))", d=4, p=8, fig=fig,
                ap="平行四辺形の性質（対辺が平行で等しい）から相似な三角形を見つけ，線分の比を求める。高さが共通な三角形の面積比は底辺の比。",
                steps=st,
                alt=[f"△ACD は平行四辺形の半分で，△ACE はその $\\dfrac{{{p}}}{{{n}}}$。AF：AC$={p}:{2 * p + q}$ を使って △AEF$=$△ACE$\\times\\dfrac{{{p}}}{{{2 * p + q}}}$ と求めてもよい。"],
                pc=[("相似な三角形と線分の比を求めている", 3), ("基準になる三角形の面積を求めている", 3), ("正しい面積", 2)],
                pit=["EF：EB を EF：FB と取り違える。", "平行四辺形の半分にするのを忘れる。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def _err_mc(stem, sol, right, cands, e, err, **kw):
    return MC(f"{stem}\n〔Kさんの解答〕\n{sol}\nKさんの解答の誤りを説明したものとして最も適するものを，" + SEL4, right, cands, e, err=err, **kw)


@gen("error_correction", 4, ["common_error", "computation"])
def d_area_err(r):
    p, q = r.choice([(2, 3), (3, 4), (3, 5), (2, 5), (4, 5), (1, 2), (1, 3), (3, 2), (5, 4), (4, 3)])
    kind = r.choice(["area", "area", "vol"])
    if kind == "area":
        S = p * p * r.randint(2, 9)
        good = Fr(S * q * q, p * p)
        bad = Fr(S * q, p)
        stem = f"〔問題〕相似な2つの五角形 P，Q があり，相似比は ${p}:{q}$ である。P の面積が ${S}$ cm² のとき，Q の面積を求めなさい。"
        sol = f"相似比が ${p}:{q}$ なので，面積の比も ${p}:{q}$。Q の面積は ${S}\\times\\dfrac{{{q}}}{{{p}}}={ftex(bad)}$ cm²"
        right = f"面積の比は相似比の2乗の ${p * p}:{q * q}$ になるので，相似比をそのまま使ったところが誤りである。"
        fix = f"${S}\\times\\dfrac{{{q * q}}}{{{p * p}}}={ftex(good)}$ cm²"
        chk = (f"Rational({S}*{q * q},{p * p})", fpy(good))
        cands = [(f"面積の比は相似比の3乗の ${p ** 3}:{q ** 3}$ になるので，相似比をそのまま使ったところが誤りである。", "3乗になるのは体積の比である。", "面積比と体積比の混同"),
                 (f"かける分数が逆で，${S}\\times\\dfrac{{{p}}}{{{q}}}$ とするべきである。", "Q の面積を求めるので，Q 側の数を分子にする向きは正しい。誤りは比そのもの。", "比の向きの誤解"),
                 ("Kさんの解答に誤りはない。", f"1辺が ${p}$ と ${q}$ の正方形で考えると，面積は ${p * p}$ と ${q * q}$ になり，比は相似比と等しくない。", "検算不足"),
                 (f"五角形は三角形ではないので，相似比は使えず，面積は求められない。", "どんな多角形も三角形に分けられるので，面積比は相似比の2乗になる。", "相似の性質の適用範囲の誤解")]
    else:
        V = p ** 3 * r.randint(1, 5)
        good = Fr(V * q ** 3, p ** 3)
        bad = Fr(V * q * q, p * p)
        stem = f"〔問題〕相似な2つの円柱 P，Q があり，相似比は ${p}:{q}$ である。P の体積が ${V}$ cm³ のとき，Q の体積を求めなさい。"
        sol = f"相似比が ${p}:{q}$ なので，体積の比は ${p * p}:{q * q}$。Q の体積は ${V}\\times\\dfrac{{{q * q}}}{{{p * p}}}={ftex(bad)}$ cm³"
        right = f"体積の比は相似比の3乗の ${p ** 3}:{q ** 3}$ になるので，2乗にしたところが誤りである。"
        fix = f"${V}\\times\\dfrac{{{q ** 3}}}{{{p ** 3}}}={ftex(good)}$ cm³"
        chk = (f"Rational({V}*{q ** 3},{p ** 3})", fpy(good))
        cands = [(f"体積の比は相似比と同じ ${p}:{q}$ になるので，2乗にしたところが誤りである。", "体積は縦・横・高さの3つの長さの積なので3乗の比になる。", "体積比の誤解"),
                 ("円柱の体積は「底面積×高さ」なので，相似比は使えない。", "相似な立体なら，体積比は相似比の3乗として求められる。", "相似の性質の適用範囲の誤解"),
                 ("Kさんの解答に誤りはない。", f"1辺 ${p}$ と ${q}$ の立方体で考えると，体積は ${p ** 3}$ と ${q ** 3}$ で，比は相似比の2乗ではない。", "検算不足"),
                 (f"かける分数が逆で，${V}\\times\\dfrac{{{p * p}}}{{{q * q}}}$ とするべきである。", "Q の体積を求めるので Q 側を分子にする向きは正しい。誤りは2乗にしたこと。", "比の向きの誤解")]
    r.shuffle(cands)
    return _err_mc(stem, sol, right, cands, f"正しくは {fix}。",
                   dict(sol=sol, step="面積比・体積比を求める部分", type="formula", tempt="相似比・面積比・体積比の違いをあいまいに覚えているため。", fix=fix), d=3, p=6,
                   ap="相似比 $m:n$ → 面積比 $m^2:n^2$，体積比 $m^3:n^3$。Kさんが使った比がどれにあたるかを確かめる。",
                   steps=["面積（体積）の比は相似比の何乗かを確かめる。", "Kさんの比と比べる。", f"正しくは {fix}。"],
                   alt=["1辺の長さが相似比の数になる正方形・立方体で，実際に面積・体積を計算して比べる。"],
                   pc=[("誤りの原因を正しく指摘している", 3), ("正しい値を求めている", 3)],
                   pit=["面積にも体積にも相似比をそのまま使う。", "面積比と体積比を取り違える。"],
                   chk=chk + (None, "intermediate"))


@gen("error_correction", 3, ["common_error", "computation"])
def d_parallel_lines(r):
    p, q = r.sample(range(2, 9), 2)
    n = p + q
    x = r.randint(5, 20)
    good = Fr(x * p, n)
    where = r.choice([1, 2])
    l1 = "DE//BC より，△ADE∽△ABC"
    if where == 1:
        l2 = f"相似比は AD：DB$={p}:{q}$"
        l3 = f"DE：BC$={p}:{q}$ より，DE$={x}\\times\\dfrac{{{p}}}{{{q}}}$"
        ans = Fr(x * p, q)
    else:
        l2 = f"相似比は AD：AB$={p}:{n}$"
        l3 = f"DE：BC$={p}:{n}$ より，DE$={x}\\times\\dfrac{{{n}}}{{{p}}}$"
        ans = Fr(x * n, p)
    if ans == good:
        raise AssertionError
    l4 = f"答え　${ftex(ans)}$ cm"
    sol = "\n".join(f"{i + 1}行目　{t}" for i, t in enumerate([l1, l2, l3, l4]))
    LINES4 = ["1行目", "2行目", "3行目", "4行目"]
    ok = {0: "1行目は正しい。同位角が等しいので2組の角が等しく，△ADE∽△ABC。",
          1: "2行目は正しい。相似比は AD：AB で求めている。",
          2: "3行目は2行目の比を正しく使っている。",
          3: "4行目は3行目の式を正しく計算している。"}
    why = {LINES4[i]: (ok[i], "誤りの箇所の見落とし") for i in range(4) if i != where}
    info = {1: ("2行目（相似比を AD：DB にした）", "concept", "「上：下」の比と「上：全体」の比を区別していないため。"),
            2: ("3行目（比の式で分数を逆にした）", "calculation", "DE：BC$=p:(p+q)$ から DE を求めるときに，かける分数の向きを確かめなかったため。")}[where]
    fix = f"DE$={x}\\times\\dfrac{{{p}}}{{{n}}}={ftex(good)}$ cm"
    fig = fig_de_bc(min(max(p / n, 0.25), 0.75))
    return mc(f"〔問題〕右の図のように，△ABC の辺 AB，AC 上にそれぞれ点 D，E があり，DE//BC である。AD$={p}$ cm，DB$={q}$ cm，BC$={x}$ cm のとき，DE の長さを求めなさい。\n〔Kさんの解答〕\n{sol}\nKさんの解答で，誤りが最初に生じた行として最も適するものを，" + SEL4,
              LINES4, f"誤りが最初に生じたのは{LINES4[where]}。正しくは {fix}。", d=3, p=6, keep=True, ai=where, why=why, fig=fig,
              err=dict(sol=sol, step=info[0], type=info[1], tempt=info[2], fix=fix),
              ap="1行ずつ，図と照らし合わせて自分で確かめる。DE：BC は「上の部分：全体」の比 AD：AB に等しい。",
              steps=["△ADE∽△ABC は正しい。", f"相似比は AD：AB$={p}:{n}$。", f"DE$={x}\\times\\dfrac{{{p}}}{{{n}}}={ftex(good)}$ cm。"],
              alt=["答えが BC より短くなっているか（DE は BC より短いはず）で，誤りに気づくことができる。"],
              pc=[("誤りの行を正しく指摘している", 3), ("正しい長さを求めている", 3)],
              pit=["AD：DB を相似比と考える。", "比の式で分数の向きを逆にする。"],
              chk=(f"Rational({x}*{p},{n})", fpy(good), None, "intermediate"))


@gen("error_correction", 3, ["common_error", "condition_check"])
def d_cond_err(r):
    a0, b0, c0 = r.choice(BASES)
    p, q = r.choice([(1, 2), (2, 3), (3, 4), (2, 5), (3, 5), (1, 3)])
    t = r.choice(range(35, 86, 5))
    kind = r.choice(["notbetween", "oneangle", "twosides"])
    if kind == "notbetween":
        given = f"AB$={c0 * p}$ cm，BC$={a0 * p}$ cm，${A('A')}={t}^\\circ$，DE$={c0 * q}$ cm，EF$={a0 * q}$ cm，${A('D')}={t}^\\circ$"
        sol = f"AB：DE$=$BC：EF$={p}:{q}$，${A('A')}={A('D')}$ なので，2組の辺の比とその間の角がそれぞれ等しく，△ABC∽△DEF である。"
        right = f"${A('A')}$ は辺 AB と BC の間の角ではない。2組の辺の比と「その間の角」がそろっていないので，相似であるとはいえない。"
        etype, tempt = "condition", "「2組の辺の比と1つの角」で相似条件が成り立つと思いこみやすい。"
    elif kind == "oneangle":
        given = f"${A('A')}={A('D')}={t}^\\circ$，AB$={c0 * p}$ cm，DE$={c0 * q}$ cm"
        sol = f"${A('A')}={A('D')}$ で，AB：DE$={p}:{q}$ と比も決まっているので，△ABC∽△DEF である。"
        right = "1組の角と1組の辺の比だけでは三角形の形は決まらない。相似条件のどれにもあてはまらないので，相似であるとはいえない。"
        etype, tempt = "condition", "相似比が求められたことで，相似であると思いこみやすい。"
    else:
        bad = b0 * q + 1
        given = f"AB$={c0 * p}$ cm，BC$={a0 * p}$ cm，CA$={b0 * p}$ cm，DE$={c0 * q}$ cm，EF$={a0 * q}$ cm，FD$={bad}$ cm"
        sol = f"AB：DE$={p}:{q}$，BC：EF$={p}:{q}$ で，2組の辺の比が等しいので，△ABC∽△DEF である。"
        right = f"3辺の長さがわかっているので，3組の辺の比がすべて等しいかを調べる必要がある。CA：FD$={b0 * p}:{bad}$ は ${p}:{q}$ と等しくないので，相似ではない。"
        etype, tempt = "condition", "2組の辺の比が等しいだけで相似条件がそろったと考えやすい。"
    cands = [("相似比を最も簡単な整数の比にしていないので誤りである。", "比を簡単にするかどうかは，相似かどうかの判断には関係しない。", "論点の取り違え"),
             ("Kさんの解答に誤りはない。", "Kさんが使った条件は，相似条件にあてはまっていない。", "相似条件の誤解"),
             ("三角形の相似を示すには，3組の角がすべて等しいことを示さなければならない。", "2組の角が等しければ十分である。", "相似条件の誤解"),
             ("相似を示すには，対応する辺の長さがそれぞれ等しいことを示さなければならない。", "辺の長さが等しいのは合同の条件で，相似では辺の比が等しければよい。", "合同条件との混同")]
    r.shuffle(cands)
    fix = "△ABC と △DEF は相似であるとはいえない"
    return _err_mc(f"〔問題〕△ABC と △DEF で，{given} である。△ABC と △DEF は相似であるといえるか。", sol, right, cands, f"正しくは「{fix}」。",
                   dict(sol=sol, step="相似条件のあてはめ", type=etype, tempt=tempt, fix=fix), d=3, p=6,
                   ap="相似条件（3組の辺の比／2組の辺の比とその間の角／2組の角）のどれに，与えられた条件がぴったりあてはまるかを1つずつ確かめる。",
                   steps=["与えられた辺の比と角の位置を図にかきこむ。", "相似条件と照らし合わせる。", right],
                   alt=["条件を満たすが形の違う三角形が2つかけないかを考える（反例）。"],
                   pc=[("誤りの理由を正しく指摘している", 3), ("正しい結論を理解している", 3)],
                   pit=["等しい角が2辺の間の角かどうかを確かめない。", "一部の辺の比だけで相似と判断する。"])


GENERATORS = [a_sim_side, a_sim_cond, a_parallel, a_midpoint, a_area_vol,
              b_shadow, b_trapezoid, b_three_parallel, b_proof_fill, b_area_tri,
              c_xy, c_cone, c_para_cross,
              d_area_err, d_parallel_lines, d_cond_err]

GENERATORS = [_robust(g) for g in GENERATORS]
