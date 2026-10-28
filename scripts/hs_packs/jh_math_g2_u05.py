"""単元パック：中学2年 三角形と四角形（神奈川県公立高校入試形式）。"""
import math
import re
import unicodedata
from fractions import Fraction as Fr

from banks._common import figure, mc, num, plane
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem, tp)

UNIT_ID = "JH-MATH-G2-U05"

PREREQUISITES = [
    ("JH-MATH-G2-U04", "三角形の合同条件と証明の進め方、平行線の同位角・錯角の性質。この単元の証明はすべてこれを土台にする。"),
    ("JH-MATH-G1-U05", "垂直・平行の記号、角の二等分線や垂線の作図。二等辺三角形やひし形の性質と結びつく。"),
    ("JH-MATH-G2-U03", "座標平面上の直線の式と傾き。等積変形を座標平面で考えるときに使う。"),
]
EXTENSIONS = [
    ("JH-MATH-G3-U05", "合同から相似へ発展し、中点連結定理や平行線と線分の比を学ぶ。"),
    ("JH-MATH-G3-U06", "円周角の定理の証明で、二等辺三角形の底角の性質を使う。"),
    ("HS-MATHA-U02", "高校の図形の性質で、三角形の五心や円に内接する四角形の性質を論証する。"),
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


def ftex(v):
    v = Fr(v)
    if v.denominator == 1:
        return str(v.numerator)
    s = "-" if v < 0 else ""
    return f"{s}\\dfrac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def fpy(v):
    v = Fr(v)
    return str(v.numerator) if v.denominator == 1 else f"Rational({v.numerator},{v.denominator})"


def pt(x, y):
    return f"$({ftex(x)},\\,{ftex(y)})$"


def para_pts():
    return {"A": (1.0, 2.4), "B": (0.0, 0.0), "C": (4.6, 0.0), "D": (5.6, 2.4)}


def isos_fig(alt="AB=AC の二等辺三角形 ABC"):
    pts = {"A": (0, 3.4), "B": (-2, 0), "C": (2, 0)}
    return figure(alt, geo(pts, segs=[("A", "B"), ("B", "C"), ("C", "A")], ticks=[("A", "B", 1), ("A", "C", 1)]))


# ----------------------------------------------------------------------
# 授業プリント
# ----------------------------------------------------------------------

LESSON = lesson(
    goals=["二等辺三角形の定義と性質（底角が等しい、頂角の二等分線は底辺を垂直に2等分する）を証明し、角や長さを求めるのに使える。",
           "直角三角形の合同条件を理解し、証明に使える。",
           "平行四辺形の性質と平行四辺形になるための条件、長方形・ひし形・正方形との関係を説明できる。平行線を使った等積変形ができる。"],
    duration=100,
    readiness=["三角形の合同条件を使った証明の書き方（〜において、仮定から、合同条件、結論）を知っている。",
               "平行線の同位角・錯角の性質、三角形の内角の和を使える。",
               "定義と定理、ことがらの逆の意味を区別できる。"],
    flow=[("導入：定義と定理", 10, "二等辺三角形の定義（2辺が等しい）と、そこから証明される性質（定理）を区別する"),
          ("二等辺三角形", 20, "底角の定理の証明、頂角の二等分線の性質、二等辺三角形になるための条件（例題1）"),
          ("直角三角形の合同", 15, "斜辺と1つの鋭角／斜辺と他の1辺。なぜ2つの条件だけでよいか"),
          ("平行四辺形の性質と条件", 25, "3つの性質の証明、平行四辺形になるための5つの条件（例題2）"),
          ("特別な平行四辺形と等積変形", 20, "長方形・ひし形・正方形の対角線、平行線と面積（例題3）"),
          ("まとめと確認", 10, "確認問題と問題プリントの指示")],
    sections=[
        intro("in1", "定義と定理",
              "ことばの意味をはっきり述べたものを定義という。たとえば「2つの辺が等しい三角形を二等辺三角形という」は定義である。これに対し、「二等辺三角形の2つの底角は等しい」のように、定義や前に証明したことがらをもとに証明されたことがらのうち、大切なものを定理という。",
              bullets=["二等辺三角形で、等しい2辺の間の角を頂角、頂角に対する辺を底辺、底辺の両端の角を底角という。", "定理は、証明の根拠として使える。"],
              points=[tp("「底角が等しい」を二等辺三角形の定義と思っている生徒が多い。定義は1つだけ（2辺が等しい）で、それ以外は証明する性質であることを確認する。", ask="二等辺三角形の定義を言えるか。", expect="2つの辺が等しい三角形。", timing="導入")]),
        theorem("th1", "二等辺三角形の性質（定理）",
                "$$\\mathrm{AB}=\\mathrm{AC}\\ \\Longrightarrow\\ \\angle\\mathrm{B}=\\angle\\mathrm{C}$$",
                ["二等辺三角形の底角は等しい。", "二等辺三角形の頂角の二等分線は、底辺を垂直に2等分する。",
                 "逆に、2つの角が等しい三角形は、その2つの角を底角とする二等辺三角形である（二等辺三角形になるための条件）。",
                 "3つの辺が等しい三角形（正三角形）では、3つの角はすべて $60^\\circ$。"],
                proof=["$\\triangle\\mathrm{ABC}$ で AB $=$ AC とし、$\\angle\\mathrm{A}$ の二等分線と辺 BC の交点を D とする。",
                       "$\\triangle\\mathrm{ABD}$ と $\\triangle\\mathrm{ACD}$ において、仮定から AB $=$ AC、$\\angle\\mathrm{BAD}=\\angle\\mathrm{CAD}$。",
                       "AD は共通。",
                       "2組の辺とその間の角がそれぞれ等しいので、$\\triangle\\mathrm{ABD}\\equiv\\triangle\\mathrm{ACD}$。",
                       "合同な図形の対応する角は等しいので、$\\angle\\mathrm{B}=\\angle\\mathrm{C}$。さらに BD $=$ CD、$\\angle\\mathrm{ADB}=\\angle\\mathrm{ADC}=90^\\circ$ もいえる。"],
                points=[tp("補助線（頂角の二等分線）をひく理由を考えさせる。", ask="合同な三角形をつくるには、どんな線をひけばよいか。", expect="二等辺三角形を左右に分ける線。頂角の二等分線。"),
                        tp("同じ合同から「底辺を垂直に2等分する」ことも導けることを示し、1つの証明から複数の性質が得られることに気づかせる。")]),
        theorem("th2", "直角三角形の合同条件",
                "$$\\text{① 斜辺と1つの鋭角がそれぞれ等しい}\\qquad\\text{② 斜辺と他の1辺がそれぞれ等しい}$$",
                ["2つの直角三角形は、①または②が成り立つとき合同である。", "斜辺は直角に対する辺で、直角三角形の中でいちばん長い辺。",
                 "①は、残りの鋭角も等しくなる（$90^\\circ$ から引く）ので「1組の辺とその両端の角」に帰着する。",
                 "②は、2つの三角形を等しい辺で合わせると二等辺三角形ができることから証明できる。"],
                points=[tp("②の証明は、2つの直角三角形を等しい辺どうしで裏返してくっつけ、二等辺三角形をつくる図で説明する。", caution="「斜辺」でない辺と鋭角が等しくても、その鋭角の位置によっては合同条件にあたらないことに注意させる。")]),
        definition("df1", "平行四辺形の定義・性質・条件",
                   "2組の対辺がそれぞれ平行な四角形を平行四辺形という（定義）。",
                   conditions=["性質：① 2組の対辺はそれぞれ等しい。② 2組の対角はそれぞれ等しい。③ 対角線はそれぞれの中点で交わる。",
                               "平行四辺形になるための条件：(1) 2組の対辺がそれぞれ平行（定義）　(2) 2組の対辺がそれぞれ等しい　(3) 2組の対角がそれぞれ等しい　(4) 対角線がそれぞれの中点で交わる　(5) 1組の対辺が平行でその長さが等しい。",
                               "「1組の対辺が平行で、もう1組の対辺が等しい」四角形は、平行四辺形とは限らない（等脚台形がある）。"],
                   points=[tp("性質①〜③と条件(2)〜(4)が「逆」の関係にあることを、矢印で板書して確認する。", ask="性質①の逆は何か。それは正しいか。", expect="2組の対辺がそれぞれ等しい四角形は平行四辺形である。正しい（条件(2)）。")]),
        derivation("dv1", "平行四辺形の対辺・対角が等しいことを導く",
                   ["平行四辺形 ABCD に対角線 AC をひき、$\\triangle\\mathrm{ABC}$ と $\\triangle\\mathrm{CDA}$ を考える。",
                    "AB$\\parallel$DC より錯角が等しいので $\\angle\\mathrm{BAC}=\\angle\\mathrm{DCA}$。",
                    "AD$\\parallel$BC より錯角が等しいので $\\angle\\mathrm{BCA}=\\angle\\mathrm{DAC}$。",
                    "AC は共通なので、1組の辺とその両端の角がそれぞれ等しく、$\\triangle\\mathrm{ABC}\\equiv\\triangle\\mathrm{CDA}$。",
                    "対応する辺・角は等しいので、AB $=$ CD、BC $=$ DA、$\\angle\\mathrm{B}=\\angle\\mathrm{D}$。同様に $\\angle\\mathrm{A}=\\angle\\mathrm{C}$。"],
                   points=[tp("対角線で2つの三角形に分けると合同な三角形ができる、という発想を、他の性質の証明（対角線の中点）にも使わせる。")]),
        definition("df2", "特別な平行四辺形と等積変形",
                   "4つの角がすべて等しい四角形を長方形、4つの辺がすべて等しい四角形をひし形、4つの角がすべて等しく4つの辺もすべて等しい四角形を正方形という。これらはどれも平行四辺形の特別な場合である。",
                   conditions=["長方形の対角線は長さが等しい。ひし形の対角線は垂直に交わる。正方形の対角線は長さが等しく、垂直に交わる。",
                               "平行四辺形に「1つの角が直角」または「対角線の長さが等しい」を加えると長方形、「となり合う辺が等しい」または「対角線が垂直」を加えるとひし形になる。",
                               "等積変形：直線 ℓ 上の2点 A、B と、ℓ に平行な直線上の点 P、Q について、$\\triangle\\mathrm{PAB}=\\triangle\\mathrm{QAB}$（底辺が共通で高さが等しい）。"],
                   points=[tp("「正方形は長方形でもあり、ひし形でもある」ことをベン図で示す。", caution="「長方形はひし形ではない」と「長方形は平行四辺形である」の区別があいまいな生徒が多い。")]),
        example("ex1", "例題1　二等辺三角形の角",
                "AB $=$ AC の二等辺三角形 ABC で、$\\angle\\mathrm{A}=40^\\circ$ である。辺 AC 上に BD $=$ BC となる点 D をとるとき、$\\angle\\mathrm{ABD}$ の大きさを求めなさい。",
                ["底角は $\\angle\\mathrm{ABC}=\\angle\\mathrm{C}=(180^\\circ-40^\\circ)\\div2=70^\\circ$。",
                 "$\\triangle\\mathrm{BCD}$ も BD $=$ BC の二等辺三角形なので $\\angle\\mathrm{BDC}=\\angle\\mathrm{C}=70^\\circ$。",
                 "$\\angle\\mathrm{DBC}=180^\\circ-70^\\circ\\times2=40^\\circ$。",
                 "$\\angle\\mathrm{ABD}=70^\\circ-40^\\circ=30^\\circ$。"],
                "$30^\\circ$",
                thinking="二等辺三角形が2つある。それぞれ「どの2辺が等しいか」から底角を見つける。",
                points=[tp("等しい辺に同じ印をつけさせ、底角の位置を図で確認させる。")],
                misconceptions=[("$\\triangle\\mathrm{BCD}$ で $\\angle\\mathrm{DBC}=\\angle\\mathrm{C}$ とする", "BD $=$ BC なので、等しいのは $\\angle\\mathrm{BDC}$ と $\\angle\\mathrm{C}$")]),
        example("ex2", "例題2　平行四辺形になることの証明",
                "平行四辺形 ABCD の対角線 BD 上に、BE $=$ DF となる点 E、F をとる。四角形 AECF が平行四辺形であることを証明しなさい。",
                ["対角線 AC をひき、AC と BD の交点を O とする。", "平行四辺形の対角線はそれぞれの中点で交わるから、AO $=$ CO ……①、BO $=$ DO ……②",
                 "仮定から BE $=$ DF ……③　②、③から EO $=$ BO $-$ BE $=$ DO $-$ DF $=$ FO ……④",
                 "①、④より、四角形 AECF の対角線がそれぞれの中点で交わるので、四角形 AECF は平行四辺形である。"],
                "上の証明のとおり",
                thinking="平行四辺形になるための5つの条件のうち、どれが一番示しやすいかを考える。対角線に点があるので「対角線がそれぞれの中点で交わる」が使える。",
                points=[tp("同じことを $\\triangle\\mathrm{ABE}\\equiv\\triangle\\mathrm{CDF}$ から示す方法もあることを紹介し、条件の選び方で証明の長さが変わることに気づかせる。")]),
        example("ex3", "例題3　等積変形",
                "AD$\\parallel$BC の台形 ABCD で、対角線 AC、BD の交点を O とする。$\\triangle\\mathrm{ABO}$ と面積が等しい三角形を答えなさい。",
                ["$\\triangle\\mathrm{ABC}$ と $\\triangle\\mathrm{DBC}$ は、底辺 BC が共通で、AD$\\parallel$BC より高さが等しいので面積が等しい。",
                 "両方から共通部分 $\\triangle\\mathrm{OBC}$ を除くと、$\\triangle\\mathrm{ABO}=\\triangle\\mathrm{DCO}$。"],
                "$\\triangle\\mathrm{DCO}$",
                thinking="平行線にはさまれた三角形で、底辺が共通なものを探す。そこから共通部分を引く。",
                figure=figure("AD//BC の台形と対角線", geo({"A": (1.2, 2.2), "D": (3.4, 2.2), "B": (0, 0), "C": (5, 0), "O": (2.18, 1.0)},
                                                       segs=[("A", "D"), ("D", "C"), ("C", "B"), ("B", "A"), ("A", "C"), ("B", "D")], off={"O": (0, -0.45)})),
                points=[tp("「面積が等しい」と「合同」は違うことを確認する（$\\triangle\\mathrm{ABO}$ と $\\triangle\\mathrm{DCO}$ は合同とは限らない）。")]),
        board("bd1", "板書案",
              [("① 二等辺三角形", ["定義：2辺が等しい", "定理：底角は等しい", "頂角の二等分線 ⊥ 底辺、底辺を2等分", "2角が等しい → 二等辺三角形"]),
               ("② 直角三角形・平行四辺形", ["斜辺と1鋭角／斜辺と他の1辺", "性質：対辺・対角が等しい、対角線は中点で交わる", "条件は5つ（1組の対辺が平行で等しい もOK）", "1組平行＋もう1組等しい はNG（等脚台形）"]),
               ("③ 特別な四角形・等積", ["長方形：対角線の長さが等しい", "ひし形：対角線が垂直", "正方形：その両方", "底辺共通＋平行線 → 面積が等しい"])],
              points=[tp("②の「NG」の例は、等脚台形の図をそえて板書する。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("角を求める問題では、まず等しい辺に印をつけ、「どの角とどの角が等しいか」を言葉で言わせてから計算させる。"),
               tp("平行四辺形になるための条件は、性質の逆として整理させる。", ask="「対角線の長さが等しい四角形は平行四辺形か」。", expect="いいえ。等脚台形など反例がある。長方形の性質であって平行四辺形の条件ではない。"),
               tp("直角三角形の合同条件では「斜辺」がそろっていることを最初に確認させる。", caution="斜辺でない辺が等しい場合は、ふつうの合同条件を使う。"),
               tp("等積変形は、座標平面上の問題（一次関数の単元）でもよく使う。平行な直線の傾きが等しいことと結びつけておく。", timing="等積変形のあと")],
              misconceptions=[("二等辺三角形の定義は「底角が等しい」", "定義は「2辺が等しい」。底角が等しいのは定理"),
                              ("ひし形の対角線は長さが等しい", "ひし形の対角線は垂直に交わる。長さが等しいのは長方形"),
                              ("1組の対辺が平行で、もう1組の対辺が等しければ平行四辺形", "等脚台形があるので平行四辺形とは限らない")]),
        summary("sm1", "まとめ",
                ["二等辺三角形の底角は等しく、頂角の二等分線は底辺を垂直に2等分する。", "直角三角形の合同条件：斜辺と1鋭角、斜辺と他の1辺。",
                 "平行四辺形：対辺・対角が等しく、対角線は中点で交わる。条件は5つ。", "長方形・ひし形・正方形は平行四辺形の特別な場合。対角線の性質で区別する。", "平行線を使うと、面積を変えずに三角形の形を変えられる（等積変形）。"]),
        check("ck1", "確認問題",
              [("AB $=$ AC の二等辺三角形で、$\\angle\\mathrm{B}=65^\\circ$ のとき、$\\angle\\mathrm{A}$ を求めなさい。", "$180^\\circ-65^\\circ\\times2=50^\\circ$"),
               ("平行四辺形 ABCD で AB $=6$ cm、BC $=9$ cm のとき、周の長さを求めなさい。", "$(6+9)\\times2=30$ cm"),
               ("平行四辺形 ABCD に、どんな条件を加えるとひし形になるか。1つ答えなさい。", "AB $=$ BC（となり合う辺が等しい）、または AC $\\perp$ BD")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

@gen("basic_check", 5, ["computation"])
def a_isosceles(r):
    kind = r.choice(["base", "apex", "ext_from_apex", "apex_from_ext"])
    if kind == "base":
        a = r.choice(range(20, 141, 2))
        v = (180 - a) // 2
        stem = f"右の図のように，AB$=$AC の二等辺三角形 ABC がある。${A('BAC')}={a}^\\circ$ のとき，${A('ABC')}$ の大きさは何度か，求めなさい。"
        st = ["二等辺三角形の底角は等しいので ${}={}$。".format(A('ABC'), A('ACB')), f"$(180^\\circ-{a}^\\circ)\\div2={v}^\\circ$。"]
        expr, e = f"(180-{a})/2", f"底角は等しいので $(180^\\circ-{a}^\\circ)\\div2={v}^\\circ$。"
    elif kind == "apex":
        b = r.randint(25, 85)
        v = 180 - 2 * b
        stem = f"右の図のように，AB$=$AC の二等辺三角形 ABC がある。${A('ACB')}={b}^\\circ$ のとき，${A('BAC')}$ の大きさは何度か，求めなさい。"
        st = [f"底角は等しいので ${A('ABC')}={b}^\\circ$。", f"${A('BAC')}=180^\\circ-{b}^\\circ\\times2={v}^\\circ$。"]
        expr, e = f"180-2*{b}", f"底角が2つとも ${b}^\\circ$ なので $180^\\circ-{2 * b}^\\circ={v}^\\circ$。"
    elif kind == "ext_from_apex":
        a = r.choice(range(20, 141, 2))
        v = 180 - (180 - a) // 2
        stem = f"AB$=$AC の二等辺三角形 ABC で，${A('BAC')}={a}^\\circ$ である。辺 BC を C の方に延長した直線上に点 D をとるとき，${A('ACD')}$ の大きさは何度か，求めなさい。"
        st = [f"底角 ${A('ACB')}=(180^\\circ-{a}^\\circ)\\div2={(180 - a) // 2}^\\circ$。", f"${A('ACD')}=180^\\circ-{(180 - a) // 2}^\\circ={v}^\\circ$。"]
        expr, e = f"180-(180-{a})/2", f"${A('ACD')}=180^\\circ-{A('ACB')}={v}^\\circ$。"
    else:
        ext = r.randint(95, 160)
        v = 2 * ext - 180
        stem = f"AB$=$AC の二等辺三角形 ABC で，辺 BC を C の方に延長した直線上に点 D をとると，${A('ACD')}={ext}^\\circ$ であった。${A('BAC')}$ の大きさは何度か，求めなさい。"
        st = [f"${A('ACB')}=180^\\circ-{ext}^\\circ={180 - ext}^\\circ$。", f"底角は等しいので ${A('ABC')}={180 - ext}^\\circ$。", f"${A('BAC')}=180^\\circ-{180 - ext}^\\circ\\times2={v}^\\circ$。"]
        expr, e = f"180-2*(180-{ext})", f"底角は ${180 - ext}^\\circ$ なので ${A('BAC')}={v}^\\circ$。"
    return MARK(stem, v, e, expr, d=1, fig=isos_fig(),
                ap="二等辺三角形の2つの底角は等しい。三角形の内角の和 $180^\\circ$、一直線の角 $180^\\circ$ と組み合わせる。",
                steps=st,
                alt=["外角の性質（外角＝となり合わない2つの内角の和）を使って確かめることもできる。"],
                pc=[("底角が等しいことを使っている", 1), ("正しい大きさを求めている", 1)],
                pit=["頂角と底角を取り違える。", "$\\div2$ を忘れる。"])


@gen("basic_check", 5, ["computation", "concept"])
def a_para_prop(r):
    kind = r.choice(["angle", "angle", "side", "diag", "perim"])
    pts = para_pts()
    pts["O"] = ((pts["A"][0] + pts["C"][0]) / 2, (pts["A"][1] + pts["C"][1]) / 2)
    segs = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")]
    if kind == "angle":
        a = r.choice([x for x in range(50, 131) if x != 90])
        tgt = r.choice(["B", "C", "D"])
        v = a if tgt == "C" else 180 - a
        stem = f"平行四辺形 ABCD で，${A('A')}={a}^\\circ$ のとき，${A(tgt)}$ の大きさは何度か，求めなさい。"
        st = ([f"${A('A')}$ と ${A('C')}$ は対角なので等しい。"] if tgt == "C" else [f"${A('A')}$ と ${A(tgt)}$ はとなり合う角で，AD//BC（または AB//DC）より和は $180^\\circ$。"]) + [f"${A(tgt)}={v}^\\circ$。"]
        expr = f"{v}" if tgt == "C" else f"180-{a}"
        e = st[0] + f"よって ${v}^\\circ$。"
    elif kind in ("side", "perim"):
        p, q = r.sample(range(3, 15), 2)
        if kind == "side":
            tgt = r.choice(["CD", "DA"])
            v = p if tgt == "CD" else q
            stem = f"平行四辺形 ABCD で，AB$={p}$ cm，BC$={q}$ cm のとき，辺 {tgt} の長さは何 cm か，求めなさい。"
            st = ["平行四辺形の2組の対辺はそれぞれ等しい。", f"{tgt} は {'AB' if tgt == 'CD' else 'BC'} の対辺なので ${v}$ cm。"]
            expr = str(v)
        else:
            v = 2 * (p + q)
            stem = f"平行四辺形 ABCD で，AB$={p}$ cm，AD$={q}$ cm のとき，平行四辺形 ABCD の周の長さは何 cm か，求めなさい。"
            st = ["対辺はそれぞれ等しいので CD$=$AB，BC$=$AD。", f"周の長さ $=({p}+{q})\\times2={v}$ cm。"]
            expr = f"2*({p}+{q})"
        e = st[-1]
    else:
        segs += [("A", "C"), ("B", "D")]
        k = r.randint(3, 15)
        tgt = r.choice(["half", "whole"])
        if tgt == "half":
            v = k
            stem = f"平行四辺形 ABCD の対角線の交点を O とする。AC$={2 * k}$ cm のとき，線分 AO の長さは何 cm か，求めなさい。"
            st = ["平行四辺形の対角線はそれぞれの中点で交わる。", f"AO$=\\dfrac{{1}}{{2}}$AC$={k}$ cm。"]
            expr = f"{2 * k}/2"
        else:
            v = 2 * k
            stem = f"平行四辺形 ABCD の対角線の交点を O とする。OB$={k}$ cm のとき，対角線 BD の長さは何 cm か，求めなさい。"
            st = ["平行四辺形の対角線はそれぞれの中点で交わる。", f"BD$=2\\times$OB$={v}$ cm。"]
            expr = f"2*{k}"
        e = st[-1]
    fig = figure("平行四辺形 ABCD", geo(pts, segs=segs, names=["A", "B", "C", "D"] + (["O"] if kind == "diag" else []), off={"O": (0, -0.45)}))
    return MARK(stem, v, e, expr, d=1, fig=fig,
                ap="平行四辺形の性質：2組の対辺はそれぞれ等しい、2組の対角はそれぞれ等しい、対角線はそれぞれの中点で交わる。となり合う角の和は $180^\\circ$。",
                steps=st,
                alt=["図に等しい辺・角の印をかきこんで、どの性質を使うかを確かめる。"],
                pc=[("使う性質を正しく選んでいる", 1), ("正しい値を求めている", 1)],
                pit=["となり合う角も等しいと考える。", "対角線の長さが等しいと考える（長方形と混同）。"])


SPECIAL = [
    ("${A}=90^\\circ$", "長方形"), ("AC$=$BD", "長方形"), ("AB$=$BC", "ひし形"), ("AC$\\perp$BD", "ひし形"),
    ("AC$=$BD，AC$\\perp$BD", "正方形"), ("${A}=90^\\circ$，AB$=$AD", "正方形"),
    ("AB$=$DC", "限らない"), ("${A}={C}$", "限らない"), ("AO$=$CO", "限らない"),
]
QUAD_ANS = {"長方形": "長方形", "ひし形": "ひし形", "正方形": "正方形", "限らない": "長方形・ひし形・正方形のどれになるとも限らない"}
QUAD_WHY = {"長方形": "長方形になるのは，1つの角が直角，または対角線の長さが等しいときである。",
            "ひし形": "ひし形になるのは，となり合う辺が等しい，または対角線が垂直に交わるときである。",
            "正方形": "正方形になるには，長方形の条件とひし形の条件の両方が必要である。",
            "限らない": "この条件はもともとすべての平行四辺形で成り立つので，特別な四角形になるとは限らない。"}


@gen("basic_check", 5, ["condition_check", "concept"])
def a_special_quad(r):
    cond, ans = r.choice(SPECIAL)
    cond = cond.replace("{A}", A("A")).replace("{C}", A("C"))
    rev = r.random() < 0.4 and ans in ("長方形", "ひし形", "正方形")
    if not rev:
        right = QUAD_ANS[ans]
        def wr(k):
            if k == "限らない":
                return "この条件を加えると，特別な平行四辺形になる。"
            if ans == "正方形":
                return f"正方形は{k}の特別な場合でもあるが，この条件では長方形の条件とひし形の条件の両方が成り立つので，最も適するのは正方形である。"
            return QUAD_WHY[k]
        cands = [(QUAD_ANS[k], wr(k), "特別な平行四辺形の条件の取り違え") for k in QUAD_ANS if k != ans]
        return MC(f"平行四辺形 ABCD の対角線の交点を O とする。この平行四辺形に {cond} という条件を加えると，四角形 ABCD はどんな四角形になるか。最も適するものを，" + SEL4,
                  right, cands, f"{cond} を加えると{right}{'になる' if ans != '限らない' else '。'}", d=2,
                  ap="長方形・ひし形・正方形は平行四辺形の特別な場合。角の条件（直角）・辺の条件（となり合う辺が等しい）・対角線の条件（長さが等しい／垂直）で区別する。",
                  steps=["加える条件が、角・辺・対角線のどれについての条件かを確かめる。", QUAD_WHY[ans], f"答えは「{right}」。"],
                  alt=["条件を満たす図をかいて、どんな形になるかを確かめる。"],
                  pc=[("条件の意味を正しくとらえている", 1), ("正しい四角形を選んでいる", 1)],
                  pit=["対角線の長さが等しい → ひし形、と取り違える。", "もともと平行四辺形で成り立つ性質を、特別な条件と考える。"])
    pool = [(c.replace("{A}", A("A")).replace("{C}", A("C")), k) for c, k in SPECIAL]
    rights = [c for c, k in pool if k == ans]
    right = r.choice(rights)
    others = [(c, f"この条件を加えると{QUAD_ANS[k]}{'になる' if k != '限らない' else '（もとの平行四辺形で成り立つ性質）'}。", "特別な平行四辺形の条件の取り違え") for c, k in pool if k != ans and not (k == "正方形" and ans != "正方形")]
    r.shuffle(others)
    return MC(f"平行四辺形 ABCD の対角線の交点を O とする。この平行四辺形が{ans}になるために加える条件として最も適するものを，" + SEL4,
              right, others, f"{right} を加えると{ans}になる。", d=2,
              ap="長方形は「角」または「対角線の長さ」、ひし形は「となり合う辺」または「対角線の垂直」、正方形はその両方の条件で決まる。",
              steps=[QUAD_WHY[ans], f"正答の条件：{right}。"],
              alt=["選択肢の条件を満たす平行四辺形の図をかき、形を確かめる。"],
              pc=[("それぞれの四角形の条件を理解している", 1), ("正しい条件を選んでいる", 1)],
              pit=["長方形とひし形の対角線の性質を取り違える。"])


RT_NAMES = ["直角三角形の斜辺と1つの鋭角がそれぞれ等しい", "直角三角形の斜辺と他の1辺がそれぞれ等しい", "2組の辺とその間の角がそれぞれ等しい", "1組の辺とその両端の角がそれぞれ等しい", "合同であるとはいえない"]


@gen("basic_check", 5, ["condition_check", "concept"])
def a_rt_congruence(r):
    p, q = r.sample(range(3, 13), 2)
    t = r.choice([25, 30, 35, 40, 50, 55, 60, 65])
    cases = [
        (f"AB$=$DE$={max(p, q) + 3}$ cm，${A('A')}={A('D')}={t}^\\circ$", 0, "斜辺 AB と DE，鋭角 A と D が等しい。"),
        (f"AB$=$DE$={max(p, q) + 3}$ cm，BC$=$EF$={min(p, q)}$ cm", 1, "斜辺 AB と DE，もう1つの辺 BC と EF が等しい。"),
        (f"AC$=$DF$={p}$ cm，BC$=$EF$={q}$ cm", 2, "直角をはさむ2辺がそれぞれ等しく，その間の角は直角で等しい。"),
        (f"AC$=$DF$={p}$ cm，${A('A')}={A('D')}={t}^\\circ$", 3, "辺 AC と DF，その両端の角（$\\angle$A と $\\angle$D，直角の $\\angle$C と $\\angle$F）が等しい。"),
        (f"${A('A')}={A('D')}={t}^\\circ$，${A('B')}={A('E')}={90 - t}^\\circ$", 4, "角だけが等しく，辺の長さの条件がない。"),
    ]
    info, k, why_ok = r.choice(cases)
    right = RT_NAMES[k]
    def wr(n):
        if n == "合同であるとはいえない":
            return "合同条件にあてはまるので，合同であるといえる。"
        if k == 4:
            return "等しい辺が1組もなく，この合同条件にはあてはまらない。"
        if "斜辺" in n and k in (0, 1):
            return "斜辺は等しいが，もう1つの等しいものが" + ("鋭角" if k == 0 else "他の1辺") + "なので，この条件ではない。"
        if "斜辺" in n:
            return "等しい辺に斜辺（AB と DE）がふくまれていないので，直角三角形の合同条件は使えない。"
        return "与えられた辺と角の位置関係が，この条件にあてはまらない。"
    cands = [(n, wr(n), "合同条件の取り違え") for n in RT_NAMES if n != right]
    r.shuffle(cands)
    return MC(f"${A('C')}={A('F')}=90^\\circ$ の直角三角形 ABC と DEF で，{info} である。このとき，2つの三角形が合同であるかどうかと，その根拠について述べたものとして最も適するものを，" + SEL4,
              right, cands, f"{why_ok}よって「{right}」。", d=2,
              ap="まず斜辺（直角に対する辺：AB と DE）が等しいかを確かめる。斜辺が等しければ直角三角形の合同条件、そうでなければふつうの合同条件を使う。",
              steps=["斜辺は AB と DE。", why_ok, f"答え：「{right}」。"],
              alt=["条件どおりに直角三角形をかいて、1通りに決まるかどうかを確かめる。"],
              pc=[("斜辺を正しく見分けている", 1), ("正しい合同条件を選んでいる", 1)],
              pit=["斜辺でない辺を斜辺と思いこむ。", "角だけが等しくても合同とする。"])


# ======================================================================
# B 標準演習
# ======================================================================

def _para_conds(r):
    p, q = r.sample(range(3, 12), 2)
    a = r.choice([x for x in range(55, 126, 5) if x != 90])
    k, m = r.sample(range(2, 9), 2)
    T = [
        f"AB$=$DC$={p}$ cm，AD$=$BC$={q}$ cm",
        f"AB//DC，AB$=$DC$={p}$ cm",
        f"${A('A')}={A('C')}={a}^\\circ$，${A('B')}={A('D')}={180 - a}^\\circ$",
        f"対角線の交点を O とすると，AO$=$CO$={k}$ cm，BO$=$DO$={m}$ cm",
        "AB//DC，AD//BC",
    ]
    F = [
        (f"AB//DC，AD$=$BC$={q}$ cm", "AD と BC が平行でない等脚台形になる場合がある。"),
        (f"AB$=$AD$={p}$ cm，CB$=$CD$={q}$ cm", "となり合う辺が等しい「たこ形」になり，平行四辺形ではない。"),
        (f"${A('A')}={A('B')}={a}^\\circ$", f"平行四辺形ではとなり合う角の和が $180^\\circ$ になるので，となり合う角がどちらも ${a}^\\circ$ の四角形は平行四辺形ではない。"),
        (f"対角線の交点を O とすると，AO$=$CO$={k}$ cm", "一方の対角線だけが2等分されても，平行四辺形とは限らない。"),
        (f"AB//DC，${A('A')}={A('B')}$", "等脚台形のように，平行四辺形にならない場合がある。"),
    ]
    return T, F


@gen("standard_practice", 4, ["condition_check", "concept"])
def b_para_cond(r):
    T, F = _para_conds(r)
    if r.random() < 0.5:
        right = r.choice(T)
        cands = [(c, why, "平行四辺形になるための条件の誤解") for c, why in r.sample(F, 4)]
        stem = "四角形 ABCD について，次の条件のうち，四角形 ABCD がいつでも平行四辺形になるものとして最も適するものを，" + SEL4
        e = f"「{right}」は平行四辺形になるための条件にあてはまる。"
    else:
        right, why_r = r.choice(F)
        cands = [(c, "平行四辺形になるための条件にあてはまるので，いつでも平行四辺形になる。", "平行四辺形になるための条件の誤解") for c in r.sample(T, 4)]
        stem = "四角形 ABCD について，次の条件のうち，四角形 ABCD が平行四辺形になるとは限らないものとして最も適するものを，" + SEL4
        e = f"「{right}」では，{why_r}"
    return MC(stem, right, cands, e, d=3, p=4,
              ap="平行四辺形になるための条件（2組の対辺が平行／2組の対辺が等しい／2組の対角が等しい／対角線がそれぞれの中点で交わる／1組の対辺が平行で長さが等しい）と照らし合わせる。あてはまらないものは反例の図を考える。",
              steps=["それぞれの条件を5つの条件と比べる。", "あてはまらないものは、等脚台形・たこ形などの反例がかけるかを考える。", e],
              alt=["条件を満たす四角形を、平行四辺形でない形でかけるかを実際に作図して確かめる。"],
              pc=[("平行四辺形になるための条件を正しく思い出している", 2), ("反例を考えて正しく判断している", 2)],
              pit=["「1組の対辺が平行で、もう1組の対辺が等しい」を平行四辺形の条件と思いこむ。"])


def _isos_pts(a):
    """頂角 a の二等辺三角形（B(-1,0)，C(1,0)）。"""
    h = 1 / math.tan(math.radians(a / 2))
    return {"A": (0.0, h), "B": (-1.0, 0.0), "C": (1.0, 0.0)}


@gen("standard_practice", 4, ["application", "computation"])
def b_isos_combo(r):
    kind = r.choice(["bdbc", "bdbc", "bisect"])
    if kind == "bdbc":
        a = r.choice(range(20, 57, 2))
        beta = (180 - a) // 2
        P = _isos_pts(a)
        Ax, Ay = P["A"]
        # 辺 AC 上の点 D で BD = BC = 2
        best = None
        for i in range(1, 2000):
            t = i / 2000
            x, y = 1 + t * (Ax - 1), t * Ay
            d = abs(math.hypot(x + 1, y) - 2)
            if best is None or d < best[0]:
                best = (d, (x, y))
        P["D"] = best[1]
        sc = min(3.6 / Ay, 2.0)
        P = {k: (x * sc, y * sc) for k, (x, y) in P.items()}
        ask = r.choice(["ABD", "DBC", "ADB"])
        v = {"ABD": beta - a, "DBC": a, "ADB": 180 - beta}[ask]
        stem = f"右の図のように，AB$=$AC の二等辺三角形 ABC の辺 AC 上に，BD$=$BC となる点 D をとる。${A('BAC')}={a}^\\circ$ のとき，${A(ask)}$ の大きさは何度か，求めなさい。"
        st = [f"$\\triangle\\mathrm{{ABC}}$ の底角：${A('ABC')}={A('ACB')}=(180^\\circ-{a}^\\circ)\\div2={beta}^\\circ$。",
              f"$\\triangle\\mathrm{{BCD}}$ は BD$=$BC の二等辺三角形なので ${A('BDC')}={A('BCD')}={beta}^\\circ$。",
              f"${A('DBC')}=180^\\circ-{beta}^\\circ\\times2={a}^\\circ$。",
              {"ABD": f"${A('ABD')}={beta}^\\circ-{a}^\\circ={v}^\\circ$。", "DBC": f"よって ${A('DBC')}={a}^\\circ$。", "ADB": f"${A('ADB')}=180^\\circ-{A('BDC')}={v}^\\circ$。"}[ask]]
        expr = {"ABD": f"(180-{a})/2-{a}", "DBC": f"180-2*((180-{a})/2)", "ADB": f"180-(180-{a})/2"}[ask]
        fig = figure("二等辺三角形 ABC と，BD=BC となる点 D", geo(P, segs=[("A", "B"), ("B", "C"), ("C", "A"), ("B", "D")],
                                                           ticks=[("A", "B", 1), ("A", "C", 1), ("B", "D", 2), ("B", "C", 2)], off={"D": (0.4, 0.1)}))
    else:
        a = r.choice([x for x in range(20, 141, 4)])
        beta = (180 - a) // 2
        P = _isos_pts(a)
        Ax, Ay = P["A"]
        AB = math.hypot(Ax + 1, Ay)
        t = AB / (AB + 2)  # AD:DC = AB:BC
        P["D"] = (Ax + t * (1 - Ax), Ay + t * (0 - Ay))
        sc = min(3.6 / Ay, 2.0)
        P = {k: (x * sc, y * sc) for k, (x, y) in P.items()}
        v = a + beta // 2
        stem = f"右の図のように，AB$=$AC の二等辺三角形 ABC で，${A('ABC')}$ の二等分線と辺 AC の交点を D とする。${A('BAC')}={a}^\\circ$ のとき，${A('BDC')}$ の大きさは何度か，求めなさい。"
        st = [f"底角 ${A('ABC')}=(180^\\circ-{a}^\\circ)\\div2={beta}^\\circ$。", f"${A('ABD')}={beta}^\\circ\\div2={beta // 2}^\\circ$。",
              f"${A('BDC')}$ は $\\triangle\\mathrm{{ABD}}$ の外角なので ${A('BAD')}+{A('ABD')}={a}^\\circ+{beta // 2}^\\circ={v}^\\circ$。"]
        expr = f"{a}+(180-{a})/4"
        fig = figure("二等辺三角形 ABC と，角 B の二等分線", geo(P, segs=[("A", "B"), ("B", "C"), ("C", "A"), ("B", "D")],
                                                      ticks=[("A", "B", 1), ("A", "C", 1)], off={"D": (0.4, 0.1)}))
    return MARK(stem, v, st[-1], expr, d=3, p=4, fig=fig,
                ap="二等辺三角形がどこにあるか（どの2辺が等しいか）を見つけ、底角が等しいことを順に使う。外角の性質も役に立つ。",
                steps=st,
                alt=["わかった角を図にすべて書きこみ、三角形ごとに内角の和が $180^\\circ$ になっているかで確かめる。"],
                pc=[("二等辺三角形の底角を正しく求めている", 2), ("求める角を正しく求めている", 2)],
                pit=["BD$=$BC の三角形で、等しい角の組を取り違える。"])


@gen("standard_practice", 4, ["application", "multiple_solutions"])
def b_para_bisector(r):
    P = para_pts()
    import math as _m
    ab = _m.hypot(P["A"][0] - P["B"][0], P["A"][1] - P["B"][1])
    ad = P["D"][0] - P["A"][0]
    P["E"] = (P["A"][0] + ab, P["A"][1])
    fig = figure("平行四辺形 ABCD と，角 B の二等分線", geo(P, segs=[("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("B", "E")], off={"E": (0, 0.42)}))
    kind = r.choice(["len", "ang", "ang2"])
    if kind == "len":
        p = r.randint(3, 10)
        q = p + r.randint(2, 8)
        v = q - p
        stem = f"右の図のように，平行四辺形 ABCD で，${A('ABC')}$ の二等分線と辺 AD の交点を E とする。AB$={p}$ cm，AD$={q}$ cm のとき，線分 ED の長さは何 cm か，求めなさい。"
        st = [f"AD//BC より錯角は等しいので ${A('AEB')}={A('EBC')}$。", f"BE は二等分線なので ${A('ABE')}={A('EBC')}$。よって ${A('ABE')}={A('AEB')}$。",
              f"$\\triangle\\mathrm{{ABE}}$ は AB$=$AE の二等辺三角形で AE$={p}$ cm。", f"ED$={q}-{p}={v}$ cm。"]
        expr = f"{q}-{p}"
    else:
        a = r.choice([x for x in range(40, 141, 2) if x != 90])
        b = 180 - a
        if kind == "ang":
            v = b // 2
            stem = f"右の図のように，平行四辺形 ABCD で，${A('ABC')}$ の二等分線と辺 AD の交点を E とする。${A('BAD')}={a}^\\circ$ のとき，${A('AEB')}$ の大きさは何度か，求めなさい。"
            st = [f"${A('ABC')}=180^\\circ-{a}^\\circ={b}^\\circ$（となり合う角の和は $180^\\circ$）。", f"${A('EBC')}={b}^\\circ\\div2={v}^\\circ$。", f"AD//BC より錯角は等しいので ${A('AEB')}={A('EBC')}={v}^\\circ$。"]
            expr = f"(180-{a})/2"
        else:
            v = 180 - b // 2
            stem = f"右の図のように，平行四辺形 ABCD で，${A('ABC')}$ の二等分線と辺 AD の交点を E とする。${A('BAD')}={a}^\\circ$ のとき，${A('BED')}$ の大きさは何度か，求めなさい。"
            st = [f"${A('ABC')}=180^\\circ-{a}^\\circ={b}^\\circ$。", f"${A('EBC')}={b // 2}^\\circ$，錯角で ${A('AEB')}={b // 2}^\\circ$。", f"${A('BED')}=180^\\circ-{b // 2}^\\circ={v}^\\circ$。"]
            expr = f"180-(180-{a})/2"
    return MARK(stem, v, st[-1], expr, d=3, p=4, fig=fig,
                ap="平行線の錯角と角の二等分線を組み合わせると、二等辺三角形 ABE が見つかる。",
                steps=st,
                alt=["$\\triangle\\mathrm{ABE}$ の内角の和や、AD//BC の同側内角（和が $180^\\circ$）を使って確かめる。"],
                pc=[("錯角と二等分線から等しい角を見つけている", 2), ("正しい答えを求めている", 2)],
                pit=["AE を AD と同じ長さと思いこむ。", "となり合う角を等しいと考える。"])


TRAP = {"A": (1.2, 2.2), "D": (3.4, 2.2), "B": (0, 0), "C": (5, 0)}


def _inter(P1, P2, P3, P4):
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = P1, P2, P3, P4
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
    return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))


@gen("standard_practice", 4, ["concept", "condition_check"])
def b_equal_area(r):
    kind = r.choice(["trap", "trap", "para"])
    if kind == "trap":
        P = dict(TRAP)
        P["O"] = _inter(P["A"], P["C"], P["B"], P["D"])
        fig = figure("AD//BC の台形 ABCD と対角線", geo(P, segs=[("A", "D"), ("D", "C"), ("C", "B"), ("B", "A"), ("A", "C"), ("B", "D")], off={"O": (0, -0.45)}))
        tgt, right, wrong = r.choice([
            ("ABC", "DBC", ["ABD", "ACD", "AOD", "OBC", "ABO"]),
            ("ABD", "ACD", ["ABC", "DBC", "AOD", "OBC", "DCO"]),
            ("ABO", "DCO", ["AOD", "OBC", "ABD", "ABC", "DBC"]),
            ("DBC", "ABC", ["ABD", "ACD", "OBC", "AOD", "DCO"]),
        ])
        stem = f"右の図のように，AD//BC の台形 ABCD で，対角線 AC と BD の交点を O とする。$\\triangle\\mathrm{{{tgt}}}$ と面積が等しい三角形として最も適するものを，" + SEL4
        why = {"ABC": "△ABC と △DBC は底辺 BC が共通で，AD//BC より高さが等しい。", "DBC": "△ABC と △DBC は底辺 BC が共通で，AD//BC より高さが等しい。",
               "ABD": "△ABD と △ACD は底辺 AD が共通で，AD//BC より高さが等しい。", "ACD": "△ABD と △ACD は底辺 AD が共通で，AD//BC より高さが等しい。",
               "ABO": "△ABC＝△DBC から共通部分 △OBC を除くと △ABO＝△DCO。", "DCO": "△ABC＝△DBC から共通部分 △OBC を除くと △ABO＝△DCO。"}
        e = why[tgt]
        cands = [(f"$\\triangle\\mathrm{{{w}}}$", "底辺と高さがそれぞれ等しい関係になっていない。AD と BC の長さが異なるので面積は等しくない。", "等積変形の条件の誤解") for w in r.sample(wrong, len(wrong))]
    else:
        P = para_pts()
        P["P"] = (P["A"][0] + r.choice([1.2, 2.0, 3.0]), P["A"][1])
        fig = figure("平行四辺形 ABCD と，辺 AD 上の点 P", geo(P, segs=[("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("P", "B"), ("P", "C")], off={"P": (0, 0.42)}))
        tgt = "PBC"
        right = r.choice(["ABC", "DBC", "ABD", "ACD"])
        stem = "右の図のように，平行四辺形 ABCD の辺 AD 上に点 P をとる。$\\triangle\\mathrm{PBC}$ と面積が等しい三角形として最も適するものを，" + SEL4
        e = f"△PBC と △{right} は，どちらも平行四辺形の面積の半分（底辺と高さが平行四辺形と共通）である。"
        cands = [(f"$\\triangle\\mathrm{{{w}}}$", "点 P の位置によって面積が変わり，いつでも等しいとはいえない。", "等積変形の条件の誤解") for w in r.sample(["PAB", "PCD", "PBD", "PAC"], 4)]
    return MC(stem, f"$\\triangle\\mathrm{{{right}}}$", cands, e, d=3, p=4, fig=fig,
              ap="底辺が共通な2つの三角形は、頂点が底辺に平行な直線上にあれば高さが等しく、面積も等しい（等積変形）。共通部分を引く考えも使う。",
              steps=["平行な2直線と、それにはさまれた三角形を探す。", "底辺が共通で高さが等しい三角形の組を見つける。", e],
              alt=["座標や具体的な長さを決めて、実際に面積を計算して確かめる。"],
              pc=[("平行線と底辺の関係に気づいている", 2), ("正しい三角形を選んでいる", 2)],
              pit=["面積が等しいことと合同を混同する。", "平行でない線上の頂点でも高さが等しいと考える。"])


PROOFS = [
    dict(fig=({"A": (0, 3.4), "B": (-2, 0), "C": (2, 0), "D": (0, 0)}, [("A", "B"), ("B", "C"), ("C", "A"), ("A", "D")], [("A", "B", 1), ("A", "C", 1)], {"D": (0, -0.4)}),
         setup="右の図のように，AB$=$AC の二等辺三角形 ABC で，$\\angle\\mathrm{A}$ の二等分線と辺 BC の交点を D とする。このとき，$\\triangle\\mathrm{ABD}\\equiv\\triangle\\mathrm{ACD}$ であることを次のように証明した。",
         body=["$\\triangle\\mathrm{ABD}$ と $\\triangle\\mathrm{ACD}$ において，", "仮定から　AB$=$AC　……①，　$\\angle\\mathrm{BAD}=\\angle\\mathrm{CAD}$　……②", "AD は（a）だから　AD$=$AD　……③", "①，②，③から，（b）ので，$\\triangle\\mathrm{ABD}\\equiv\\triangle\\mathrm{ACD}$"],
         a="共通な辺", b="2組の辺とその間の角がそれぞれ等しい"),
    dict(fig=({"A": (0, 3.6), "B": (-2, 0), "C": (2, 0), "D": (1.057, 1.698), "E": (-1.057, 1.698)}, [("A", "B"), ("B", "C"), ("C", "A"), ("B", "D"), ("C", "E")], [("A", "B", 1), ("A", "C", 1)], None),
         setup="右の図のように，AB$=$AC の二等辺三角形 ABC で，頂点 B，C から辺 AC，AB にそれぞれ垂線 BD，CE をひく。このとき，$\\triangle\\mathrm{DBC}\\equiv\\triangle\\mathrm{ECB}$ であることを次のように証明した。",
         body=["$\\triangle\\mathrm{DBC}$ と $\\triangle\\mathrm{ECB}$ において，", "仮定から　$\\angle\\mathrm{BDC}=\\angle\\mathrm{CEB}=90^\\circ$　……①", "BC は共通　……②", "（a）は等しいから　$\\angle\\mathrm{DCB}=\\angle\\mathrm{EBC}$　……③", "①，②，③から，（b）ので，$\\triangle\\mathrm{DBC}\\equiv\\triangle\\mathrm{ECB}$"],
         a="二等辺三角形の底角", b="直角三角形の斜辺と1つの鋭角がそれぞれ等しい"),
    dict(fig=({"O": (0, 0), "X": (5, 0), "Y": (3.677, 3.085), "P": (3.383, 1.231), "A": (3.383, 0), "B": (2.591, 2.174)}, [("O", "X"), ("O", "Y"), ("O", "P"), ("P", "A"), ("P", "B")], [], {"X": (0.3, 0), "Y": (0.2, 0.3)}),
         setup="右の図のように，$\\angle\\mathrm{XOY}$ の二等分線上の点 P から，2辺 OX，OY にそれぞれ垂線 PA，PB をひく。このとき，$\\triangle\\mathrm{POA}\\equiv\\triangle\\mathrm{POB}$ であることを次のように証明した。",
         body=["$\\triangle\\mathrm{POA}$ と $\\triangle\\mathrm{POB}$ において，", "仮定から　$\\angle\\mathrm{PAO}=\\angle\\mathrm{PBO}=90^\\circ$　……①，　$\\angle\\mathrm{POA}=\\angle\\mathrm{POB}$　……②", "OP は（a）だから　OP$=$OP　……③", "①，②，③から，（b）ので，$\\triangle\\mathrm{POA}\\equiv\\triangle\\mathrm{POB}$"],
         a="共通な辺", b="直角三角形の斜辺と1つの鋭角がそれぞれ等しい"),
    dict(fig=({"A": (1.0, 2.4), "B": (0, 0), "C": (4.6, 0), "D": (5.6, 2.4), "O": (2.8, 1.2), "P": (0.5, 1.2), "Q": (5.1, 1.2)}, [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("A", "C"), ("P", "Q")], [], {"O": (0, -0.42), "P": (-0.35, 0), "Q": (0.35, 0)}),
         setup="右の図のように，平行四辺形 ABCD の対角線 AC の中点 O を通る直線が，辺 AB，CD と交わる点をそれぞれ P，Q とする。このとき，$\\triangle\\mathrm{OAP}\\equiv\\triangle\\mathrm{OCQ}$ であることを次のように証明した。",
         body=["$\\triangle\\mathrm{OAP}$ と $\\triangle\\mathrm{OCQ}$ において，", "仮定から　OA$=$OC　……①", "AB//DC より，（a）は等しいから　$\\angle\\mathrm{OAP}=\\angle\\mathrm{OCQ}$　……②", "対頂角は等しいから　$\\angle\\mathrm{AOP}=\\angle\\mathrm{COQ}$　……③", "①，②，③から，（b）ので，$\\triangle\\mathrm{OAP}\\equiv\\triangle\\mathrm{OCQ}$"],
         a="錯角", b="1組の辺とその両端の角がそれぞれ等しい"),
    dict(fig=({"A": (1.0, 2.4), "B": (0, 0), "C": (4.6, 0), "D": (5.6, 2.4), "E": (1.4, 0.6), "F": (4.2, 1.8)}, [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("B", "D"), ("A", "E"), ("C", "F")], [], {"E": (0.1, -0.4), "F": (-0.1, 0.4)}),
         setup="右の図のように，平行四辺形 ABCD の対角線 BD 上に，BE$=$DF となる点 E，F をとる。このとき，$\\triangle\\mathrm{ABE}\\equiv\\triangle\\mathrm{CDF}$ であることを次のように証明した。",
         body=["$\\triangle\\mathrm{ABE}$ と $\\triangle\\mathrm{CDF}$ において，", "仮定から　BE$=$DF　……①", "（a）は等しいから　AB$=$CD　……②", "AB//DC より，錯角は等しいから　$\\angle\\mathrm{ABE}=\\angle\\mathrm{CDF}$　……③", "①，②，③から，（b）ので，$\\triangle\\mathrm{ABE}\\equiv\\triangle\\mathrm{CDF}$"],
         a="平行四辺形の対辺", b="2組の辺とその間の角がそれぞれ等しい"),
]
REASONS = ["共通な辺", "二等辺三角形の底角", "錯角", "対頂角", "平行四辺形の対辺", "同位角"]
CONDS = ["2組の辺とその間の角がそれぞれ等しい", "1組の辺とその両端の角がそれぞれ等しい", "3組の辺がそれぞれ等しい",
         "直角三角形の斜辺と1つの鋭角がそれぞれ等しい", "直角三角形の斜辺と他の1辺がそれぞれ等しい"]


@gen("standard_practice", 4, ["written_reasoning", "concept"])
def b_proof_fill(r):
    P = r.choice(PROOFS)
    pts, segs, ticks, off = P["fig"]
    fig = figure("証明の図", geo(pts, segs=segs, ticks=ticks, off=off))
    wa = [x for x in REASONS if x != P["a"]]
    wb = [x for x in CONDS if x != P["b"]]

    def C(a, b):
        return f"（a）{a}　（b）{b}"
    cands = [(C(r.choice(wa), P["b"]), f"（a）は{P['a']}である。図で，等しいことを示す辺や角の関係を確かめる。", "根拠の取り違え"),
             (C(P["a"], r.choice(wb)), f"①〜③でそろった条件は「{P['b']}」である。", "合同条件の取り違え"),
             (C(r.choice(wa), r.choice(wb)), f"（a）は{P['a']}，（b）は「{P['b']}」である。", "根拠と合同条件の取り違え"),
             (C(P["a"], r.choice(wb)), f"①〜③でそろった条件は「{P['b']}」である。", "合同条件の取り違え")]
    body = "\n".join(P["body"])
    return MC(P["setup"] + f"\n〔証明〕\n{body}\n上の証明の（a），（b）にあてはまるものの組み合わせとして最も適するものを，" + SEL4,
              C(P["a"], P["b"]), cands, f"（a）は{P['a']}，（b）は「{P['b']}」。", d=3, p=4, fig=fig,
              ap="（a）は、その行で等しいと言っている辺や角が、図や仮定からなぜ等しいといえるかを考える。（b）は、①〜③の辺・角の組み合わせと、直角三角形かどうかで判断する。",
              steps=[f"（a）：{P['a']}。", f"①〜③は「{P['b']}」の形になっている。", f"よって（a）{P['a']}，（b）{P['b']}。"],
              alt=["①〜③で等しいとわかった辺・角を図に印でかきこみ、合同条件と照らし合わせる。"],
              pc=[("（a）の根拠を正しく選んでいる", 2), ("（b）の合同条件を正しく選んでいる", 2)],
              pit=["直角三角形なのに、斜辺かどうかを確かめずに条件を選ぶ。", "錯角と同位角を取り違える。"])


# ======================================================================
# C 思考力・記述応用
# ======================================================================

def _quad_pool(r):
    a = r.choice([40, 50, 70, 80, 100, 110])
    return [
        ("ひし形の対角線は，垂直に交わる。", True, "ひし形の対角線は垂直に交わり，それぞれの中点で交わる。"),
        ("長方形の対角線は，垂直に交わる。", False, "長方形の対角線は長さが等しいが，垂直に交わるとは限らない。"),
        ("正方形は，長方形でもあり，ひし形でもある。", True, "正方形は4つの角が等しく（長方形），4つの辺も等しい（ひし形）。"),
        ("平行四辺形の対角線の長さは等しい。", False, "対角線の長さが等しいのは長方形のときである。"),
        ("長方形は平行四辺形の特別な場合である。", True, "長方形は2組の対辺が平行なので平行四辺形である。"),
        ("2組の対角がそれぞれ等しい四角形は，平行四辺形である。", True, "平行四辺形になるための条件の1つである。"),
        ("1組の対辺が平行で，もう1組の対辺が等しい四角形は，平行四辺形である。", False, "等脚台形のように平行四辺形でない場合がある。"),
        ("二等辺三角形の頂角の二等分線は，底辺を垂直に2等分する。", True, "頂角の二等分線でできる2つの三角形の合同から導かれる。"),
        (f"頂角が ${a}^\\circ$ の二等辺三角形の底角は ${(180 - a) // 2}^\\circ$ である。", True, f"$(180^\\circ-{a}^\\circ)\\div2={(180 - a) // 2}^\\circ$。"),
        (f"頂角が ${a}^\\circ$ の二等辺三角形の底角は ${180 - a}^\\circ$ である。", False, f"底角は2つあるので $(180^\\circ-{a}^\\circ)\\div2={(180 - a) // 2}^\\circ$。"),
        ("斜辺と1つの鋭角がそれぞれ等しい2つの直角三角形は合同である。", True, "直角三角形の合同条件の1つである。"),
        ("1つの鋭角がそれぞれ等しい2つの直角三角形は合同である。", False, "辺の長さの条件がないので，大きさの異なる直角三角形がある。"),
        ("ひし形の4つの角はすべて等しい。", False, "4つの角がすべて等しいのは長方形（正方形）である。ひし形は4つの辺が等しい。"),
    ]


@gen("thinking_writing", 4, ["written_reasoning", "condition_check"])
def c_xy_quads(r):
    S = _quad_pool(r)
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
        why[c] = (" ".join(rs), "三角形・四角形の性質の思いこみ")
    return mc("三角形や四角形の性質について述べた次の X，Y の文の正誤の組み合わせとして最も適するものを，" + SEL4 + f"\nX　{x[0]}\nY　{y[0]}",
              [ans] + [c for c in XY if c != ans], f"X：{x[2]}　Y：{y[2]}", d=4, p=8, why=why,
              ap="定義・定理・条件のどれにあたるかを考え、正しくないと思うものは反例（成り立たない図）を探す。",
              steps=[f"X：{x[2]}", f"Y：{y[2]}", f"よって {ans}。"],
              alt=["長方形・ひし形・正方形・等脚台形などの図をかいて確かめる。"],
              pc=[("X の正誤を根拠をもって判断している", 4), ("Y の正誤を根拠をもって判断している", 4)],
              pit=["長方形とひし形の対角線の性質を取り違える。", "性質の逆も正しいと思いこむ。"])


@gen("thinking_writing", 3, ["cross_unit", "application"], rel=["JH-MATH-G2-U03"])
def c_equal_area_coord(r):
    while True:
        p, q = r.choice([(1, 1), (2, 1), (1, 2), (-1, 1), (-2, 1), (-1, 2), (3, 2), (2, 3), (-3, 2)])
        m = Fr(p, q)
        xa, ya = r.randint(0, 3), r.randint(1, 6)
        s = r.choice([1, 2]) if max(abs(p), q) <= 2 else 1
        xb, yb = xa + q * s, ya + p * s
        cx, cy = r.randint(0, 7), r.randint(1, 7)
        on_ab = (cy - ya) * q == p * (cx - xa)
        if on_ab or yb < 0 or (cx, cy) in ((xa, ya), (xb, yb)) or max(xb, cx) > 8 or max(yb, cy) > 8:
            continue
        axis = r.choice(["x", "y"])
        if axis == "x":
            v = cx - cy / m
            if v <= 0 or v > 12 or v == cx:
                continue
        else:
            v = cy - m * cx
            if v <= 0 or v > 12 or v == cy:
                continue
        break
    v = Fr(v)
    xr = (-1, max(9, xb + 1, cx + 1, (int(v) + 1 if axis == "x" else 0)))
    yr = (-1, max(9, yb + 1, cy + 1, (int(v) + 1 if axis == "y" else 0)))
    sv = plane(xr=xr, yr=yr, unit=max(12, int(220 / max(xr[1] - xr[0], yr[1] - yr[0]))), ticks=False,
               points=[(xa, ya, "A"), (xb, yb, "B"), (cx, cy, "C")],
               segments=[((xa, ya), (xb, yb)), ((xb, yb), (cx, cy)), ((cx, cy), (xa, ya))])
    fig = figure("座標平面上の三角形 ABC", sv)
    k = ya - m * xa
    ax_name, coord = ("$x$ 軸", "$x$ 座標") if axis == "x" else ("$y$ 軸", "$y$ 座標")
    stem = (f"右の図のように，座標平面上に3点 A{pt(xa, ya)}，B{pt(xb, yb)}，C{pt(cx, cy)} がある。{ax_name}上に点 P を，"
            f"直線 AB について点 C と同じ側にとり，$\\triangle\\mathrm{{PAB}}$ の面積が $\\triangle\\mathrm{{CAB}}$ の面積と等しくなるようにする。点 P の{coord}を求めなさい。")
    c_b = cy - m * cx
    line_c = f"y={'' if m == 1 else '-' if m == -1 else ftex(m)}x{'+' if c_b > 0 else ''}{ftex(c_b) if c_b else ''}"
    expr = f"{cx}-({cy})/({fpy(m)})" if axis == "x" else f"{cy}-({fpy(m)})*{cx}"
    return MARK(stem, v, f"C を通り AB に平行な直線 ${line_c}$ と{ax_name}との交点が P。{coord}は ${ftex(v)}$。", expr, d=4, p=8, fig=fig,
                ap="底辺 AB が共通なので、高さが等しければ面積は等しい。点 C を通り AB に平行な直線上に P があればよい（等積変形）。平行な直線は傾きが等しい（一次関数の単元とのつながり）。",
                steps=[f"直線 AB の傾き：$\\dfrac{{{yb}-{ya}}}{{{xb}-{xa}}}={ftex(m)}$。", f"C を通り傾き ${ftex(m)}$ の直線：${line_c}$。",
                       f"この直線と{ax_name}との交点を求めて，P の{coord}は ${ftex(v)}$。"],
                alt=[f"△CAB の面積を計算し（直線 AB の式 $y={ftex(m)}x{'+' if k > 0 else ''}{ftex(k) if k else ''}$ を使う），△PAB の面積が同じになるように P の座標を文字でおいて方程式を解いてもよい。"],
                pc=[("C を通り AB に平行な直線を考えている", 3), ("その直線の式を正しく求めている", 3), ("正しい座標", 2)],
                pit=["AB に平行な直線ではなく、C を通る別の直線を使う。", "傾きの符号を誤る。"])


@gen("thinking_writing", 3, ["application", "multiple_solutions", "computation"])
def c_para_area(r):
    kind = r.choice(["ratio_AD", "mid_mid", "ratio_BC"])
    P = para_pts()
    if kind == "ratio_AD":
        p, q = r.sample(range(1, 6), 2)
        S = r.choice([24, 30, 36, 40, 48, 60, 72, 84, 90, 96])
        v = Fr(S * p, 2 * (p + q))
        P["P"] = (P["A"][0] + 4.6 * p / (p + q), 2.4)
        segs = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("B", "P")]
        stem = f"右の図のように，面積が ${S}$ cm² の平行四辺形 ABCD の辺 AD 上に，AP：PD$={p}:{q}$ となる点 P をとる。$\\triangle\\mathrm{{ABP}}$ の面積は何 cm² か，求めなさい。"
        st = [f"$\\triangle\\mathrm{{ABD}}$ は平行四辺形の半分で ${ftex(Fr(S, 2))}$ cm²。", f"$\\triangle\\mathrm{{ABP}}$ と $\\triangle\\mathrm{{ABD}}$ は高さが共通で，底辺の比は AP：AD$={p}:{p + q}$。", f"${ftex(Fr(S, 2))}\\times\\dfrac{{{p}}}{{{p + q}}}={ftex(v)}$ cm²。"]
        expr = f"Rational({S},2)*Rational({p},{p + q})"
        alt = [f"平行四辺形の面積 $=$ AD $\\times$ 高さ なので，$\\triangle\\mathrm{{ABP}}=\\dfrac{{1}}{{2}}\\times$ AP $\\times$ 高さ $=\\dfrac{{1}}{{2}}\\times\\dfrac{{{p}}}{{{p + q}}}\\times{S}$ と考えてもよい。"]
    elif kind == "mid_mid":
        S = r.choice([16, 24, 32, 40, 48, 56, 64, 72, 80, 20, 28, 36])
        v = Fr(3 * S, 8)
        P["M"] = ((P["B"][0] + P["C"][0]) / 2, 0)
        P["N"] = ((P["C"][0] + P["D"][0]) / 2, 1.2)
        segs = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("A", "M"), ("M", "N"), ("N", "A")]
        stem = f"右の図のように，面積が ${S}$ cm² の平行四辺形 ABCD で，辺 BC，CD の中点をそれぞれ M，N とする。$\\triangle\\mathrm{{AMN}}$ の面積は何 cm² か，求めなさい。"
        st = [f"$\\triangle\\mathrm{{ABM}}=\\dfrac{{1}}{{4}}\\times{S}={ftex(Fr(S, 4))}$（$\\triangle\\mathrm{{ABC}}$ の半分）。", f"$\\triangle\\mathrm{{ADN}}=\\dfrac{{1}}{{4}}\\times{S}={ftex(Fr(S, 4))}$。",
              f"$\\triangle\\mathrm{{MCN}}=\\dfrac{{1}}{{8}}\\times{S}={ftex(Fr(S, 8))}$（$\\triangle\\mathrm{{BCD}}$ の $\\dfrac{{1}}{{4}}$）。", f"$\\triangle\\mathrm{{AMN}}={S}-{ftex(Fr(S, 4))}-{ftex(Fr(S, 4))}-{ftex(Fr(S, 8))}={ftex(v)}$ cm²。"]
        expr = f"{S}-Rational({S},4)*2-Rational({S},8)"
        alt = [f"平行四辺形全体を $1$ とすると，$1-\\dfrac{{1}}{{4}}-\\dfrac{{1}}{{4}}-\\dfrac{{1}}{{8}}=\\dfrac{{3}}{{8}}$。${S}\\times\\dfrac{{3}}{{8}}={ftex(v)}$。"]
    else:
        p, q = r.sample(range(1, 6), 2)
        S = r.choice([24, 30, 36, 40, 48, 60, 70, 72, 84, 90])
        v = Fr(S * q, 2 * (p + q))
        P["E"] = (4.6 * p / (p + q), 0)
        segs = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("A", "E"), ("A", "C")]
        stem = f"右の図のように，面積が ${S}$ cm² の平行四辺形 ABCD の辺 BC 上に，BE：EC$={p}:{q}$ となる点 E をとる。$\\triangle\\mathrm{{AEC}}$ の面積は何 cm² か，求めなさい。"
        st = [f"$\\triangle\\mathrm{{ABC}}$ は平行四辺形の半分で ${ftex(Fr(S, 2))}$ cm²。", f"$\\triangle\\mathrm{{AEC}}$ と $\\triangle\\mathrm{{ABC}}$ は高さが共通で，底辺の比は EC：BC$={q}:{p + q}$。", f"${ftex(Fr(S, 2))}\\times\\dfrac{{{q}}}{{{p + q}}}={ftex(v)}$ cm²。"]
        expr = f"Rational({S},2)*Rational({q},{p + q})"
        alt = [f"$\\triangle\\mathrm{{ABE}}={ftex(Fr(S, 2))}\\times\\dfrac{{{p}}}{{{p + q}}}={ftex(Fr(S * p, 2 * (p + q)))}$ を求め，$\\triangle\\mathrm{{ABC}}$ から引いても求められる。"]
    fig = figure("平行四辺形 ABCD と内部の三角形", geo(P, segs=segs, off={k: (0, 0.42) for k in ("P", "N")} | {k: (0, -0.42) for k in ("M", "E")}))
    return MARK(stem, v, st[-1], expr, d=4, p=8, fig=fig,
                ap="平行四辺形を対角線で分けた三角形はどれも面積が半分。高さが共通な三角形の面積の比は、底辺の比に等しい。",
                steps=st, alt=alt,
                pc=[("基準になる三角形の面積を求めている", 3), ("底辺の比（または引き算）を正しく使っている", 3), ("正しい答え", 2)],
                pit=["平行四辺形の面積の半分にするのを忘れる。", "比を AP：PD のまま使い、AP：AD にしない。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def _err_mc(stem, sol, right, cands, e, err, **kw):
    return MC(f"{stem}\n〔Kさんの解答〕\n{sol}\nKさんの解答の誤りを説明したものとして最も適するものを，" + SEL4, right, cands, e, err=err, **kw)


@gen("error_correction", 4, ["common_error", "condition_check"])
def d_para_cond_err(r):
    p, q = r.sample(range(3, 11), 2)
    k = r.randint(2, 9)
    case = r.choice(["trap", "kite", "half", "diag_eq"])
    if case == "trap":
        given = f"AB//DC，AD$=$BC$={q}$ cm"
        sol = "1組の対辺が平行で，もう1組の対辺の長さが等しいので，四角形 ABCD は平行四辺形である。"
        right = "平行四辺形になるのは「1組の対辺が平行でその長さが等しい」ときで，平行な辺と長さが等しい辺が別の組では，等脚台形になる場合がある。"
        tempt = "「1組の対辺が平行でその長さが等しい」という条件と言葉が似ているため。"
        etype = "condition"
    elif case == "kite":
        given = f"AB$=$AD$={p}$ cm，CB$=$CD$={q}$ cm"
        sol = "2組の辺がそれぞれ等しいので，四角形 ABCD は平行四辺形である。"
        right = "等しいのはとなり合う辺どうしで，対辺ではない。たこ形のように平行四辺形でない四角形がある。"
        tempt = "「2組の対辺がそれぞれ等しい」の「対辺」を読み落としやすい。"
        etype = "condition"
    elif case == "half":
        given = f"対角線の交点を O とすると，AO$=$CO$={k}$ cm"
        sol = "対角線が中点で交わるので，四角形 ABCD は平行四辺形である。"
        right = "平行四辺形になるには，2本の対角線が「それぞれの」中点で交わる必要がある。BO$=$DO がわかっていない。"
        tempt = "「対角線がそれぞれの中点で交わる」の「それぞれの」を見落としやすい。"
        etype = "condition"
    else:
        given = f"対角線 AC，BD の長さが等しく，AC$=$BD$={2 * k}$ cm"
        sol = "対角線の長さが等しいので，四角形 ABCD は平行四辺形（長方形）である。"
        right = "対角線の長さが等しいのは長方形の性質であって，平行四辺形になるための条件ではない。等脚台形のように平行四辺形でない場合がある。"
        tempt = "長方形の性質を逆に使ってしまう。"
        etype = "logic"
    cands = [("平行四辺形であることを示すには，2組の対辺がそれぞれ平行であることを必ず示さなければならない。", "対辺が等しい・対角線が中点で交わるなど，他の条件を使ってもよい。", "条件の誤解"),
             ("四角形の内角の和が $360^\\circ$ であることを使っていないので誤りである。", "内角の和は平行四辺形の判定とは直接関係がない。", "根拠の誤解"),
             ("Kさんの解答に誤りはない。", "条件を満たしても平行四辺形にならない四角形（反例）がかける。", "反例の見落とし"),
             ("対角線が垂直に交わることを示していないので誤りである。", "対角線が垂直であることは平行四辺形の条件ではない（ひし形の性質）。", "特別な四角形との混同")]
    r.shuffle(cands)
    fix = "平行四辺形であるとはいえない（反例がある）"
    return _err_mc(f"〔問題〕四角形 ABCD で，{given} である。四角形 ABCD は平行四辺形であるといえるか。", sol, right, cands,
                   f"正しくは「{fix}」。", dict(sol=sol, step="平行四辺形になるための条件のあてはめ", type=etype, tempt=tempt, fix=fix), d=3, p=6,
                   ap="与えられた条件が、平行四辺形になるための5つの条件のどれかとぴったり一致するかを確かめる。一致しなければ、条件を満たすのに平行四辺形でない図（反例）をかいてみる。",
                   steps=["5つの条件を書き出す。", "与えられた条件と比べる（「対辺」「それぞれの」「その長さ」などのことばに注意）。", "一致しないので，平行四辺形とはいえない。"],
                   alt=["等脚台形・たこ形など、よく知られた反例の図をかいて確かめる。"],
                   pc=[("誤りの理由を正しく指摘している", 3), ("反例や正しい条件を理解している", 3)],
                   pit=["条件のことばの一部を読み落とす。", "特別な四角形の性質を平行四辺形の条件と混同する。"])


@gen("error_correction", 3, ["common_error", "computation"])
def d_isos_steps(r):
    a = r.choice(range(20, 141, 2))
    beta = (180 - a) // 2
    v = 180 - beta
    where = r.randint(0, 2)
    l1 = f"AB$=$AC より，${A('ABC')}={A('ACB')}$"
    l2 = f"${A('ACB')}=(180^\\circ-{a}^\\circ)\\div2={beta}^\\circ$"
    b_used = beta
    if where == 0:
        l1 = f"AB$=$AC より，${A('BAC')}={A('ACB')}$"
        b_used = a
        l2 = f"${A('ACB')}={a}^\\circ$"
    elif where == 1:
        b_used = 180 - a
        l2 = f"${A('ACB')}=180^\\circ-{a}^\\circ={b_used}^\\circ$"
    l3 = f"${A('ACD')}=180^\\circ-{A('ACB')}=180^\\circ-{b_used}^\\circ={180 - b_used}^\\circ$"
    if where == 2:
        l3 = f"${A('ACD')}$ は ${A('ACB')}$ の対頂角なので ${A('ACD')}={b_used}^\\circ$"
        ans = b_used
    else:
        ans = 180 - b_used
    if ans == v:
        raise AssertionError("誤答が正答と一致")
    l4 = f"答え　${ans}^\\circ$"
    sol = "\n".join(f"{i + 1}行目　{t}" for i, t in enumerate([l1, l2, l3, l4]))
    LINES4 = ["1行目", "2行目", "3行目", "4行目"]
    ok = {0: "1行目は正しい。等しい辺 AB，AC に対する角（底角）が等しい。", 1: "2行目は，1行目の関係から正しく計算している。",
          2: "3行目は，一直線の角 $180^\\circ$ から正しく求めている。", 3: "4行目は，3行目の結果をそのまま答えている。"}
    why = {LINES4[i]: (ok[i], "誤りの箇所の見落とし") for i in range(4) if i != where}
    info = {0: ("1行目（等しい角の組の取り違え）", "concept", "「AB$=$AC」から、頂角と底角が等しいと思いこむ。"),
            1: ("2行目（$\\div2$ のし忘れ）", "calculation", "底角が2つあることを忘れて、$180^\\circ$ から頂角を引いただけで終えてしまう。"),
            2: ("3行目（対頂角の誤用）", "concept", "辺の延長でできる角を、対頂角と取り違えている。")}[where]
    fix = f"${A('ACB')}={beta}^\\circ$，${A('ACD')}=180^\\circ-{beta}^\\circ={v}^\\circ$"
    return mc(f"〔問題〕AB$=$AC の二等辺三角形 ABC で，${A('BAC')}={a}^\\circ$ である。辺 BC を C の方に延長した直線上に点 D をとるとき，${A('ACD')}$ の大きさを求めなさい。\n〔Kさんの解答〕\n{sol}\nKさんの解答で，誤りが最初に生じた行として最も適するものを，" + SEL4,
              LINES4, f"誤りが最初に生じたのは{LINES4[where]}。正しくは {fix}。", d=3, p=6, keep=True, ai=where, why=why,
              err=dict(sol=sol, step=info[0], type=info[1], tempt=info[2], fix=fix),
              ap="図をかいて等しい辺に印をつけ、どの角とどの角が等しいかを確かめながら、1行ずつ自分で計算して比べる。",
              steps=[f"底角 ${A('ABC')}={A('ACB')}$。", f"${A('ACB')}=(180^\\circ-{a}^\\circ)\\div2={beta}^\\circ$。", f"${A('ACD')}=180^\\circ-{beta}^\\circ={v}^\\circ$。"],
              alt=[f"外角の性質から ${A('ACD')}={A('BAC')}+{A('ABC')}={a}^\\circ+{beta}^\\circ={v}^\\circ$ と求めて確かめる。"],
              pc=[("誤りの行を正しく指摘している", 3), ("正しい角の大きさを求めている", 3)],
              pit=["頂角と底角を取り違える。", "$\\div2$ を忘れる。"],
              chk=(f"180-(180-{a})/2", str(v), None, "intermediate"))


@gen("error_correction", 3, ["common_error", "concept"])
def d_para_err(r):
    kind = r.choice(["adj", "diag"])
    if kind == "adj":
        a = r.choice([x for x in range(50, 131) if x != 90])
        sol = f"平行四辺形の対角は等しいので，${A('B')}={A('A')}={a}^\\circ$　答え ${a}^\\circ$"
        right = f"${A('A')}$ と ${A('B')}$ は対角ではなく，となり合う角である。AD//BC より和が $180^\\circ$ になる。"
        stem = f"〔問題〕平行四辺形 ABCD で，${A('A')}={a}^\\circ$ のとき，${A('B')}$ の大きさを求めなさい。"
        fix = f"${A('B')}=180^\\circ-{a}^\\circ={180 - a}^\\circ$"
        tempt = "「対角は等しい」を、となり合う角にも使ってしまう。"
        etype = "concept"
        cands = [("平行四辺形の4つの角はすべて等しいので，Kさんの答えは正しいが理由が誤りである。", "4つの角がすべて等しいのは長方形である。", "長方形との混同"),
                 (f"${A('B')}$ は ${A('A')}$ の $2$ 倍になる。", "となり合う角の和が $180^\\circ$ になる関係であり，2倍の関係はない。", "根拠のない推測"),
                 ("Kさんの解答に誤りはない。", f"${A('A')}+{A('B')}$ は $180^\\circ$ になるはずなので，${a}^\\circ$ にはならない。", "検算不足")]
        chk = (f"180-{a}", str(180 - a))
    else:
        k, m = r.sample(range(3, 12), 2)
        sol = f"平行四辺形の対角線の長さは等しいので，BD$=$AC$={2 * k}$ cm，BO$=\\dfrac{{1}}{{2}}$BD$={k}$ cm　答え ${k}$ cm"
        right = "平行四辺形の対角線の長さは等しいとは限らない（等しいのは長方形）。BO は BD の半分なので，BD の長さから求めるべきである。"
        stem = f"〔問題〕平行四辺形 ABCD の対角線の交点を O とする。AC$={2 * k}$ cm，BD$={2 * m}$ cm のとき，BO の長さを求めなさい。"
        fix = f"BO$=\\dfrac{{1}}{{2}}$BD$={m}$ cm"
        tempt = "長方形の性質（対角線の長さが等しい）を、すべての平行四辺形に使ってしまう。"
        etype = "concept"
        cands = [("対角線はそれぞれの中点で交わらないので，BO は求められない。", "平行四辺形の対角線はそれぞれの中点で交わる。", "平行四辺形の性質の誤解"),
                 ("BO は AC の長さの $\\dfrac{1}{4}$ である。", "BO は BD の半分であり，AC とは関係がない。", "根拠のない推測"),
                 ("Kさんの解答に誤りはない。", f"問題文では BD$={2 * m}$ cm と与えられており，AC と等しくない。", "条件の読み落とし")]
        chk = (f"{2 * m}/2", str(m))
    return _err_mc(stem, sol, right, cands, f"正しくは {fix}。", dict(sol=sol, step="平行四辺形の性質を使った部分", type=etype, tempt=tempt, fix=fix), d=3, p=6,
                   ap="平行四辺形の性質（対辺・対角が等しい、対角線はそれぞれの中点で交わる）と、長方形・ひし形だけの性質を区別して、Kさんが使った性質が正しいかを確かめる。",
                   steps=["Kさんが使った性質を確認する。", "それが平行四辺形の性質として正しいかを判断する。", f"正しくは {fix}。"],
                   alt=["平行四辺形の図をかき、問題の条件を書きこんで確かめる。"],
                   pc=[("誤りの原因を正しく指摘している", 3), ("正しい答えを求めている", 3)],
                   pit=["長方形の性質を平行四辺形に使う。", "対角ととなり合う角を取り違える。"],
                   chk=chk + (None, "intermediate"))


GENERATORS = [a_isosceles, a_para_prop, a_special_quad, a_rt_congruence,
              b_para_cond, b_isos_combo, b_para_bisector, b_equal_area, b_proof_fill,
              c_xy_quads, c_equal_area_coord, c_para_area,
              d_para_cond_err, d_isos_steps, d_para_err]


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
