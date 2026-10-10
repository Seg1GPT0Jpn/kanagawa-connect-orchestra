"""単元パック：数学Ⅱ 図形と方程式（点と直線・円の方程式・軌跡と領域）。"""
from fractions import Fraction
from math import gcd, isqrt

import sympy as sp

from banks._common import desc, figure, mc, plane, sa
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, nonzero, summary, theorem,
                         tp)

UNIT_ID = "HS-MATH2-U03"


# ----------------------------------------------------------------------
# 補助
# ----------------------------------------------------------------------

def tx(v):
    """整数・分数の LaTeX。"""
    f = Fraction(v)
    if f.denominator == 1:
        return str(f.numerator)
    s = "-" if f < 0 else ""
    return f"{s}\\dfrac{{{abs(f.numerator)}}}{{{f.denominator}}}"


def fpy(v):
    f = Fraction(v)
    return str(f.numerator) if f.denominator == 1 else f"Rational({f.numerator},{f.denominator})"


def pt(x, y):
    if Fraction(x).denominator > 1 or Fraction(y).denominator > 1:
        return f"\\left({tx(x)},\\,{tx(y)}\\right)"
    return f"({tx(x)},\\,{tx(y)})"


def stex(e):
    return sp.latex(sp.nsimplify(e)).replace("\\frac", "\\dfrac")


def lin3(a, b, c):
    """ax+by+c の表記。"""
    out = []
    for coef, var in ((a, "x"), (b, "y"), (c, "")):
        if coef == 0:
            continue
        mag = abs(coef)
        body = ("" if (mag == 1 and var) else str(mag)) + var
        sign = "-" if coef < 0 else ("+" if out else "")
        out.append(sign + body)
    return "".join(out) or "0"


def norm_line(a, b, c):
    g = gcd(gcd(abs(a), abs(b)), abs(c)) or 1
    a, b, c = a // g, b // g, c // g
    if a < 0 or (a == 0 and b < 0):
        a, b, c = -a, -b, -c
    return a, b, c


def yform(m, k):
    """y=mx+k の表記（m, k は Fraction 可）。"""
    m, k = Fraction(m), Fraction(k)
    if m == 0:
        return f"y={tx(k)}"
    if m == 1:
        mt = "x"
    elif m == -1:
        mt = "-x"
    else:
        mt = f"{tx(m)}x"
    kt = "" if k == 0 else (f"+{tx(k)}" if k > 0 else tx(k))
    return f"y={mt}{kt}"


def sq(v, var):
    """(x-a)^2 の表記。"""
    if v == 0:
        return f"{var}^2"
    return f"({var}{'-' if v > 0 else '+'}{tx(abs(Fraction(v)))})^2"


def circ(a, b, R):
    return f"{sq(a, 'x')}+{sq(b, 'y')}={tx(R)}"


def circle_curves(a, b, r):
    import math

    def up(x):
        d = r * r - (x - a) ** 2
        return b + math.sqrt(d) if d >= 0 else float("nan")

    def dn(x):
        d = r * r - (x - a) ** 2
        return b - math.sqrt(d) if d >= 0 else float("nan")
    return [(up, ""), (dn, "")]


PYTH = [(3, 4), (4, 3), (5, 12), (12, 5), (3, -4), (4, -3), (6, 8), (8, -6)]


def lattice_on(R):
    out = []
    m = isqrt(R)
    for dx in range(-m, m + 1):
        dy2 = R - dx * dx
        dy = isqrt(dy2)
        if dy * dy == dy2:
            out.append((dx, dy))
            if dy:
                out.append((dx, -dy))
    return out


LESSON = lesson(
    goals=["座標平面上で内分点・外分点・2点間の距離を求め、図形の性質を座標で説明できる。",
           "直線の方程式、2直線の平行・垂直条件、点と直線の距離の公式を導き、使える。",
           "円の方程式を標準形・一般形で扱い、円と直線の位置関係や接線を求められる。",
           "条件を満たす点の軌跡を式で求め、不等式の表す領域を図示して最大・最小に活用できる。"],
    duration=150,
    readiness=["一次関数のグラフと傾き・切片（中学2年）を理解している。", "三平方の定理（中学3年）を使える。", "平方完成（数学Ⅰ 二次関数）ができる。"],
    flow=[("導入：図形を式で表す", 10, "中学の一次関数を振り返り、図形の性質を座標と式で調べるという単元の見通しを示す"),
          ("点の座標", 20, "2点間の距離、内分点・外分点、重心の公式を数直線から拡張して導く"),
          ("直線の方程式", 30, "傾きと通る点から直線を表し、平行・垂直条件、点と直線の距離の公式を導出する（例題1）"),
          ("円の方程式", 35, "標準形と一般形、円と直線の位置関係（d と r の比較）、接線の公式を扱う（例題2）"),
          ("軌跡", 25, "アポロニウスの円を例に、軌跡を求める手順（設定→条件の式→整理→逆の確認）を示す（例題3）"),
          ("領域と最大・最小", 25, "不等式の表す領域を図示し、一次式の最大・最小を直線の平行移動で考える"),
          ("まとめと確認", 5, "確認問題3問、問題プリントAの課題指示")],
    sections=[
        intro("in1", "図形を式で調べる",
              "中学校では一次関数 $y=ax+b$ のグラフが直線になることを学んだ。この単元では逆に、直線や円などの図形を方程式で表し、図形の性質（交わるか、接するか、距離はいくらか）を計算によって調べる。図形の問題を式の問題に置きかえる方法は、デカルトによって体系化された座標幾何の考え方である。",
              bullets=["点は座標 $(x,\\,y)$、直線は1次方程式、円は2次方程式で表される。", "図形の条件（距離・垂直・接する）を、座標や係数の条件に言いかえるのがこの単元の中心である。"],
              points=[tp("中学の一次関数と「直線の方程式」の違い（$x=3$ のような縦の直線も表せる一般形 $ax+by+c=0$）を最初に確認する。", ask="$x=3$ のグラフはどんな図形か。$y=ax+b$ の形で書けるか。", expect="$y$ 軸に平行な直線。$y=ax+b$ の形では書けない。", timing="導入の冒頭"),
                      tp("図をかいてから式を立てる、という習慣を単元全体で徹底する。", caution="式だけで処理すると、解の個数や符号の誤りに気づけない。")]),
        definition("df1", "2点間の距離・内分点・外分点",
                   "2点 $\\mathrm{A}(x_1,\\,y_1)$、$\\mathrm{B}(x_2,\\,y_2)$ について、距離は三平方の定理から求められる。線分 $\\mathrm{AB}$ を $m:n$ に内分する点、外分する点の座標は次の通りである。",
                   formula="$$\\mathrm{AB}=\\sqrt{(x_2-x_1)^2+(y_2-y_1)^2},\\qquad \\text{内分点}\\left(\\dfrac{nx_1+mx_2}{m+n},\\ \\dfrac{ny_1+my_2}{m+n}\\right)$$",
                   conditions=["外分点は内分点の式の $n$ を $-n$ におきかえたもの：$\\left(\\dfrac{-nx_1+mx_2}{m-n},\\ \\dfrac{-ny_1+my_2}{m-n}\\right)$（$m\\neq n$）",
                               "$\\triangle\\mathrm{ABC}$ の重心は $\\left(\\dfrac{x_1+x_2+x_3}{3},\\ \\dfrac{y_1+y_2+y_3}{3}\\right)$"],
                   points=[tp("内分点の式で、$x_1$ に掛かるのは「遠い方の比」$n$ であることを、数直線上の例（$0$ と $10$ を $2:3$ に内分）で確かめさせる。", ask="$0$ と $10$ を $2:3$ に内分する点はどこか。", expect="$4$")]),
        theorem("th1", "2直線の平行・垂直",
                "$$y=m_1x+n_1,\\ y=m_2x+n_2\\ \\text{について}\\quad \\text{平行}\\iff m_1=m_2,\\qquad \\text{垂直}\\iff m_1m_2=-1$$",
                ["傾きをもつ（$y$ 軸に平行でない）直線について", "一般形 $a_1x+b_1y+c_1=0,\\ a_2x+b_2y+c_2=0$ では、平行 $\\iff a_1b_2-a_2b_1=0$、垂直 $\\iff a_1a_2+b_1b_2=0$",
                 "点 $(x_1,\\,y_1)$ を通り傾き $m$ の直線は $y-y_1=m(x-x_1)$"],
                proof=["2直線を平行移動して、どちらも原点を通る $y=m_1x,\\ y=m_2x$ にしても、平行・垂直の関係は変わらない。",
                       "直線 $x=1$ との交点を $\\mathrm{P}(1,\\,m_1)$、$\\mathrm{Q}(1,\\,m_2)$ とする。2直線が垂直 $\\iff\\angle\\mathrm{POQ}=90^\\circ\\iff\\mathrm{OP}^2+\\mathrm{OQ}^2=\\mathrm{PQ}^2$（三平方の定理とその逆）。",
                       "$(1+m_1^2)+(1+m_2^2)=(m_1-m_2)^2$ を整理すると $2=-2m_1m_2$、すなわち $m_1m_2=-1$。"],
                points=[tp("垂直条件の導出で三平方の定理の「逆」を使っていることに触れる。"),
                        tp("「傾き $2$ に垂直な傾き」を $\\dfrac{1}{2}$ と答える誤りを取り上げ、$-\\dfrac{1}{2}$ になることをグラフで確認させる。", caution="符号の付け忘れが最も多い誤り（問題プリントD）。")]),
        derivation("dv1", "点と直線の距離の公式",
                   ["点 $\\mathrm{P}(x_0,\\,y_0)$ と直線 $\\ell:ax+by+c=0$ を、$\\mathrm{P}$ が原点に移るように平行移動する。$\\ell$ は $a(x+x_0)+b(y+y_0)+c=0$、すなわち $ax+by+c'=0$（$c'=ax_0+by_0+c$）に移り、求める距離は変わらない。",
                    "原点から $\\ell'$ に下ろした垂線は、$\\ell'$ に垂直な向き $(a,\\,b)$ の直線上にあるので、垂線の足を $\\mathrm{H}(ta,\\,tb)$ とおける。",
                    "$\\mathrm{H}$ は $\\ell'$ 上にあるので $a\\cdot ta+b\\cdot tb+c'=0$、$t=-\\dfrac{c'}{a^2+b^2}$。",
                    "$\\mathrm{OH}=|t|\\sqrt{a^2+b^2}=\\dfrac{|c'|}{\\sqrt{a^2+b^2}}=\\dfrac{|ax_0+by_0+c|}{\\sqrt{a^2+b^2}}$。"],
                   body="$$d=\\dfrac{|ax_0+by_0+c|}{\\sqrt{a^2+b^2}}$$ 直線は必ず $ax+by+c=0$ の形（右辺を $0$）にしてから使う。",
                   points=[tp("$y=2x+3$ を $2x-y+3=0$ と移項する場面で、$y$ の係数の符号を確認させる。", ask="$y=2x+3$ を $ax+by+c=0$ の形にすると $b$ はいくつか。", expect="$-1$"),
                           tp("分子の絶対値を忘れると距離が負になることがある。距離は必ず正であることを確認させる。")],
                   figure=figure("点 P(3,4) から直線 y=-x+2 に下ろした垂線", plane((-1, 5), (-1, 5), unit=18, lines=[(-1, 2, "ℓ")], points=[(3, 4, "P"), (0.5, 1.5, "H")], segments=[((3, 4), (0.5, 1.5))]))),
        example("ex1", "例題1　垂直な直線と点と直線の距離",
                "点 $\\mathrm{A}(1,\\,3)$ と直線 $\\ell:x+2y-2=0$ がある。(1) $\\mathrm{A}$ を通り $\\ell$ に垂直な直線の方程式を求めよ。(2) $\\mathrm{A}$ と $\\ell$ の距離を求めよ。",
                ["(1) $\\ell$ は $y=-\\dfrac{1}{2}x+1$ で傾き $-\\dfrac{1}{2}$。垂直な直線の傾き $m$ は $-\\dfrac{1}{2}m=-1$ より $m=2$。",
                 "$y-3=2(x-1)$ より $y=2x+1$。",
                 "(2) $d=\\dfrac{|1+2\\cdot3-2|}{\\sqrt{1^2+2^2}}=\\dfrac{5}{\\sqrt{5}}=\\sqrt{5}$。"],
                "(1) $y=2x+1$　(2) $\\sqrt{5}$",
                thinking="(1) 傾きの積が $-1$。(2) 直線を $ax+by+c=0$ の形のまま公式に代入する。",
                points=[tp("(2) の答えを、(1) の直線と $\\ell$ の交点 $\\left(0,\\,1\\right)$ と $\\mathrm{A}$ の距離 $\\sqrt{1+4}=\\sqrt{5}$ でも確かめさせる（別解）。")]),
        definition("df2", "円の方程式",
                   "点 $\\mathrm{C}(a,\\,b)$ からの距離が $r$ である点 $\\mathrm{P}(x,\\,y)$ 全体が、中心 $\\mathrm{C}$、半径 $r$ の円である。$\\mathrm{CP}=r$ の両辺を2乗して標準形が得られる。展開すると一般形になる。",
                   formula="$$(x-a)^2+(y-b)^2=r^2\\qquad x^2+y^2+lx+my+n=0$$",
                   conditions=["$r>0$", "一般形は平方完成して $(x-a)^2+(y-b)^2=k$ とし、$k>0$ のときに限り円を表す（$k=0$ なら1点、$k<0$ なら図形なし）",
                               "円と直線の位置関係は、中心と直線の距離 $d$ と半径 $r$ の大小で判定する：$d<r$ で2点、$d=r$ で接する、$d>r$ で共有点なし"],
                   points=[tp("一般形から中心と半径を読むとき、右辺の符号の扱い（移項）で誤りが多い。平方完成の途中式を必ず書かせる。", caution="$x^2+y^2-4x+6y-3=0$ で右辺を $4+9-3$ とする誤り。")]),
        theorem("th2", "円の接線",
                "$$\\text{円}\\ x^2+y^2=r^2\\ \\text{上の点}\\ (x_1,\\,y_1)\\ \\text{における接線は}\\quad x_1x+y_1y=r^2$$",
                ["点 $(x_1,\\,y_1)$ が円周上にあること", "中心 $(a,\\,b)$ の円 $(x-a)^2+(y-b)^2=r^2$ では $(x_1-a)(x-a)+(y_1-b)(y-b)=r^2$"],
                proof=["接点を $\\mathrm{P}(x_1,\\,y_1)$、接線上の $\\mathrm{P}$ 以外の点を $\\mathrm{Q}(x,\\,y)$ とする。接線は半径 $\\mathrm{OP}$ に垂直なので $\\angle\\mathrm{OPQ}=90^\\circ$。",
                       "三平方の定理より $\\mathrm{OQ}^2=\\mathrm{OP}^2+\\mathrm{PQ}^2$、すなわち $x^2+y^2=r^2+(x-x_1)^2+(y-y_1)^2$。",
                       "展開して整理すると $0=r^2+x_1^2+y_1^2-2x_1x-2y_1y$。$x_1^2+y_1^2=r^2$ を用いて $x_1x+y_1y=r^2$。",
                       "逆にこの式を満たす点は $\\angle\\mathrm{OPQ}=90^\\circ$ を満たす。$\\mathrm{Q}=\\mathrm{P}$ のときも式は成り立つので、これが接線の方程式である。"],
                points=[tp("公式は「円の方程式の $x^2$ を $x_1x$、$y^2$ を $y_1y$ におきかえる」と覚えると、中心がずれた円にも拡張できる。")]),
        example("ex2", "例題2　円と直線の位置関係",
                "円 $x^2+y^2-2x-4y-4=0$ と直線 $3x+4y+k=0$ が接するように、定数 $k$ の値を定めよ。",
                ["平方完成：$(x-1)^2+(y-2)^2=9$。中心 $(1,\\,2)$、半径 $3$。", "中心と直線の距離 $d=\\dfrac{|3+8+k|}{5}=\\dfrac{|k+11|}{5}$。",
                 "接する条件 $d=3$ より $|k+11|=15$。", "$k+11=\\pm15$ より $k=4,\\ -26$。"],
                "$k=4,\\ -26$",
                thinking="円と直線の問題は、連立して判別式を使うよりも「中心と直線の距離 $d$ と半径 $r$ の比較」の方が計算が軽い。",
                figure=figure("円 (x-1)^2+(y-2)^2=9 と接線 3x+4y+4=0", plane((-6, 6), (-4, 7), unit=14, curves=circle_curves(1, 2, 3), lines=[(-0.75, -1, "")], points=[(1, 2, "C(1,2)")])),
                points=[tp("絶対値の方程式から2つの値が出ることを、図で「上側で接する直線」と「下側で接する直線」に対応させる。")],
                misconceptions=[("$|k+11|=15$ から $k=4$ だけを答える", "絶対値の中が $-15$ の場合も考え、$k=-26$ も答える")]),
        definition("df3", "軌跡と領域",
                   "与えられた条件を満たす点全体の集合を、その条件を満たす点の軌跡という。軌跡を求めるには、動く点を $\\mathrm{P}(x,\\,y)$ とおき、条件を $x,\\ y$ の式で表して整理する。最後に、得られた図形上のすべての点が条件を満たすか（逆）を確かめる。また、不等式を満たす点 $(x,\\,y)$ 全体の集合を、その不等式の表す領域という。",
                   formula="$$y>f(x)\\ \\text{はグラフの上側},\\qquad (x-a)^2+(y-b)^2<r^2\\ \\text{は円の内部}$$",
                   conditions=["境界線を含むかどうか（$\\leqq$ か $<$ か）を図に明記する", "軌跡では除外される点がないかを確認する"],
                   points=[tp("「軌跡を求めよ」の答えは図形の名前（中心・半径など）で述べ、方程式だけで終えないよう指導する。")]),
        example("ex3", "例題3　アポロニウスの円",
                "2点 $\\mathrm{A}(-2,\\,0)$、$\\mathrm{B}(4,\\,0)$ からの距離の比が $\\mathrm{AP}:\\mathrm{BP}=2:1$ である点 $\\mathrm{P}$ の軌跡を求めよ。",
                ["$\\mathrm{P}(x,\\,y)$ とおく。条件は $\\mathrm{AP}=2\\mathrm{BP}$、すなわち $\\mathrm{AP}^2=4\\mathrm{BP}^2$。",
                 "$(x+2)^2+y^2=4\\{(x-4)^2+y^2\\}$。", "展開・整理：$3x^2+3y^2-36x+60=0$、$x^2+y^2-12x+20=0$。", "$(x-6)^2+y^2=16$。逆にこの円上の点は条件を満たす。"],
                "中心 $(6,\\,0)$、半径 $4$ の円",
                thinking="距離の条件は根号を避けるために2乗して式にする。",
                points=[tp("線分 $\\mathrm{AB}$ を $2:1$ に内分する点 $(2,\\,0)$ と外分する点 $(10,\\,0)$ が円の直径の両端になっていることを確認させると、結果の検算になる。")]),
        board("bd1", "板書案",
              [("① 点と直線", ["内分点 $\\left(\\dfrac{nx_1+mx_2}{m+n},\\cdots\\right)$", "平行 $m_1=m_2$、垂直 $m_1m_2=-1$", "$d=\\dfrac{|ax_0+by_0+c|}{\\sqrt{a^2+b^2}}$", "例1：$y=2x+1$、$d=\\sqrt{5}$"]),
               ("② 円", ["$(x-a)^2+(y-b)^2=r^2$", "一般形 → 平方完成", "位置関係：$d$ と $r$ を比較", "接線 $x_1x+y_1y=r^2$", "例2：$k=4,\\ -26$"]),
               ("③ 軌跡・領域", ["$\\mathrm{P}(x,y)$ とおく → 条件を式に → 整理 → 逆の確認", "例3：$(x-6)^2+y^2=16$", "$y>f(x)$：上側", "最大・最小：直線 $x+y=k$ を動かす"])],
              points=[tp("各列の最後に例題の結果を書き、公式と具体例が対応するように板書する。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("直線の方程式の答えは $y=mx+n$ でも $ax+by+c=0$ でもよいが、$y$ 軸に平行な直線は一般形でしか書けないことを確認する。"),
               tp("垂直な直線の傾きは「逆数にして符号を変える」と2段階で言わせる。", ask="傾き $3$ の直線に垂直な直線の傾きは。", expect="$-\\dfrac{1}{3}$"),
               tp("円と直線の問題では、まず中心と半径を求めて図をかかせてから、$d$ と $r$ を比べさせる。", timing="例題2の後"),
               tp("軌跡の問題で、条件を2乗したときに同値性が保たれているか（距離は $0$ 以上）を一言述べさせる。"),
               tp("領域の最大・最小では、目的の一次式 $=k$ とおいた直線の傾きと、境界線の傾きを比べてどの頂点を通るかを判断させる。", caution="頂点の値を比べずに、交点を1つ求めただけで答える答案が多い。")],
              misconceptions=[("傾き $2$ の直線に垂直な直線の傾きを $\\dfrac{1}{2}$ とする", "積が $-1$ なので $-\\dfrac{1}{2}$"),
                              ("$x^2+y^2+4x-2y-4=0$ の半径を $\\sqrt{4+1-4}=1$ とする", "$(x+2)^2+(y-1)^2=4+1+4=9$ で半径 $3$"),
                              ("点 $(2,\\,4)$ から円 $x^2+y^2=4$ への接線を、傾き $m$ とおく方法で1本だけ求める", "$y$ 軸に平行な接線 $x=2$ も忘れずに調べる")]),
        summary("sm1", "まとめ",
                ["距離・内分点・外分点・重心は座標の公式で求める。",
                 "平行 $m_1=m_2$、垂直 $m_1m_2=-1$。点と直線の距離 $d=\\dfrac{|ax_0+by_0+c|}{\\sqrt{a^2+b^2}}$。",
                 "円は平方完成で中心と半径を読む。円と直線は $d$ と $r$ の比較。接線 $x_1x+y_1y=r^2$。",
                 "軌跡：$\\mathrm{P}(x,\\,y)$ とおいて条件を式にし、図形を答える。領域：境界線の上下・内外で判断し、最大・最小は直線を平行移動して考える。"]),
        check("ck1", "確認問題",
              [("2点 $\\mathrm{A}(1,\\,-2)$、$\\mathrm{B}(7,\\,4)$ を結ぶ線分を $1:2$ に内分する点の座標を求めよ。", "$\\left(\\dfrac{2\\cdot1+1\\cdot7}{3},\\ \\dfrac{2\\cdot(-2)+1\\cdot4}{3}\\right)=(3,\\,0)$"),
               ("点 $(2,\\,1)$ と直線 $3x-4y+8=0$ の距離を求めよ。", "$\\dfrac{|6-4+8|}{5}=2$"),
               ("円 $x^2+y^2=25$ 上の点 $(3,\\,-4)$ における接線の方程式を求めよ。", "$3x-4y=25$")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

@gen("basic_check", 6, ["computation"])
def points_basic(r):
    kind = r.choice(["dist", "dist", "int", "ext", "cent"])
    x1, y1, x2, y2 = (r.randint(-5, 5) for _ in range(4))
    while (x1, y1) == (x2, y2) or x1 == x2 and y1 == y2:
        x2 += 1
    A, B = pt(x1, y1), pt(x2, y2)
    if kind == "dist":
        D2 = (x2 - x1) ** 2 + (y2 - y1) ** 2
        val = sp.sqrt(D2)
        return sa(f"座標平面上の2点 $\\mathrm{{A}}{A}$、$\\mathrm{{B}}{B}$ について、線分 $\\mathrm{{AB}}$ の長さを求めなさい。", f"${stex(val)}$",
                  f"$\\mathrm{{AB}}=\\sqrt{{({x2}-({x1}))^2+({y2}-({y1}))^2}}=\\sqrt{{{D2}}}={stex(val)}$。", d=1, v=[stex(val).replace(" ", "")],
                  ap="2点の $x$ 座標の差と $y$ 座標の差を2辺とする直角三角形を考え、三平方の定理を使う。",
                  steps=[f"$x$ 座標の差 ${x2 - x1}$、$y$ 座標の差 ${y2 - y1}$。", f"$\\mathrm{{AB}}^2=({x2 - x1})^2+({y2 - y1})^2={D2}$。", f"$\\mathrm{{AB}}={stex(val)}$。"],
                  alt=["方眼に2点をとり、直角三角形をかいて三平方の定理を確認する。"],
                  pc=[("差の2乗の和を正しく計算している", 1), ("根号を正しく簡約している", 1)],
                  pit=["差をとる前に座標の符号を誤る（$5-(-2)$ を $3$ とする）。", "根号の中を簡約し忘れる。"],
                  chk=(f"sqrt(({x2}-({x1}))**2+({y2}-({y1}))**2)", str(val)))
    m, n = r.choice([(1, 2), (2, 1), (1, 3), (3, 1), (2, 3), (3, 2), (1, 1)])
    if kind == "ext" and m == n:
        m, n = 3, 1
    if kind == "int":
        X, Y = Fraction(n * x1 + m * x2, m + n), Fraction(n * y1 + m * y2, m + n)
        what = f"線分 $\\mathrm{{AB}}$ を ${m}:{n}$ に内分する点" if m != n else "線分 $\\mathrm{AB}$ の中点"
        form = f"\\left(\\dfrac{{{n}\\cdot({x1})+{m}\\cdot({x2})}}{{{m + n}}},\\ \\dfrac{{{n}\\cdot({y1})+{m}\\cdot({y2})}}{{{m + n}}}\\right)"
        stem = f"2点 $\\mathrm{{A}}{A}$、$\\mathrm{{B}}{B}$ に対して、{what}の座標を求めなさい。"
        pyx, pyy = f"({n}*({x1})+{m}*({x2}))/{m + n}", f"({n}*({y1})+{m}*({y2}))/{m + n}"
    elif kind == "ext":
        X, Y = Fraction(-n * x1 + m * x2, m - n), Fraction(-n * y1 + m * y2, m - n)
        what = f"線分 $\\mathrm{{AB}}$ を ${m}:{n}$ に外分する点"
        form = f"\\left(\\dfrac{{-{n}\\cdot({x1})+{m}\\cdot({x2})}}{{{m}-{n}}},\\ \\dfrac{{-{n}\\cdot({y1})+{m}\\cdot({y2})}}{{{m}-{n}}}\\right)"
        stem = f"2点 $\\mathrm{{A}}{A}$、$\\mathrm{{B}}{B}$ に対して、{what}の座標を求めなさい。"
        pyx, pyy = f"(-{n}*({x1})+{m}*({x2}))/({m}-{n})", f"(-{n}*({y1})+{m}*({y2}))/({m}-{n})"
    else:
        x3, y3 = r.randint(-5, 5), r.randint(-5, 5)
        X, Y = Fraction(x1 + x2 + x3, 3), Fraction(y1 + y2 + y3, 3)
        what = "$\\triangle\\mathrm{ABC}$ の重心"
        form = f"\\left(\\dfrac{{{x1}+({x2})+({x3})}}{{3}},\\ \\dfrac{{{y1}+({y2})+({y3})}}{{3}}\\right)"
        stem = f"3点 $\\mathrm{{A}}{A}$、$\\mathrm{{B}}{B}$、$\\mathrm{{C}}{pt(x3, y3)}$ を頂点とする{what}の座標を求めなさい。"
        pyx, pyy = f"({x1}+({x2})+({x3}))/3", f"({y1}+({y2})+({y3}))/3"
    return sa(stem, f"${pt(X, Y)}$", f"公式より ${form}={pt(X, Y)}$。", d=2, v=[f"({tx(X)},{tx(Y)})"],
              ap={"int": "内分点の公式では、$x_1$ に「$\\mathrm{B}$ 側の比」$n$、$x_2$ に「$\\mathrm{A}$ 側の比」$m$ を掛ける（たすきがけ）。",
                  "ext": "外分点は、内分点の公式の $n$ を $-n$ におきかえる。",
                  "cent": "重心の座標は3頂点の座標の平均。"}[kind],
              steps=[f"公式に代入：${form}$。", f"計算して ${pt(X, Y)}$。"],
              alt=["$x$ 座標だけを数直線上で考え、比の位置にあるかを確かめる（$y$ 座標も同様）。" if kind != "cent" else "重心は中線を $2:1$ に内分する点なので、辺 $\\mathrm{BC}$ の中点 $\\mathrm{M}$ をとり、$\\mathrm{AM}$ を $2:1$ に内分しても同じ点が得られる。"],
              pc=[("公式に正しく代入している", 1), ("座標を正しく計算している", 1)],
              pit=["$m$ と $n$ を掛ける相手を逆にする。", "外分で $m-n$ の符号を誤る。" if kind == "ext" else "負の座標のかっこを忘れて符号を誤る。"],
              chk=(f"[{pyx}, {pyy}]", f"[{fpy(X)}, {fpy(Y)}]"))


@gen("basic_check", 5, ["computation"])
def line_through(r):
    kind = r.choice(["two", "two", "slope", "vert"])
    x1, y1 = r.randint(-4, 4), r.randint(-4, 4)
    if kind == "vert":
        y2 = y1 + nonzero(r, -4, 4)
        stem = f"2点 ${pt(x1, y1)}$、${pt(x1, y2)}$ を通る直線の方程式を求めなさい。"
        ans = f"x={x1}"
        return sa(stem, f"${ans}$", f"2点の $x$ 座標がともに ${x1}$ なので、$y$ 軸に平行な直線 $x={x1}$。", d=2, v=[ans, f"x-({x1})=0"],
                  ap="2点の $x$ 座標が等しいときは傾きが定義できない（分母が $0$）。$y$ 軸に平行な直線になる。",
                  steps=[f"2点の $x$ 座標はどちらも ${x1}$。", f"傾きの式 $\\dfrac{{y_2-y_1}}{{x_2-x_1}}$ は分母が $0$ で使えない。", f"求める直線は $x={x1}$。"],
                  alt=[f"一般形 $ax+by+c=0$ で $b=0$ の場合にあたる。$1\\cdot x+0\\cdot y-({x1})=0$ と書ける。"],
                  pc=[("傾きが存在しないことに気づいている", 1), ("$x=" + str(x1) + "$ と答えている", 1)],
                  pit=["傾きを $\\dfrac{" + str(y2 - y1) + "}{0}$ として計算を進めてしまう。", "$y=" + str(x1) + "$ と答える。"],
                  chk=(f"{x1}", str(x1), None, "intermediate"))
    m = nonzero(r, -3, 3)
    k = y1 - m * x1
    if kind == "two":
        x2 = x1 + nonzero(r, -3, 3)
        y2 = y1 + m * (x2 - x1)
        stem = f"2点 ${pt(x1, y1)}$、${pt(x2, y2)}$ を通る直線の方程式を求めなさい。"
        st0 = f"傾きは $\\dfrac{{{y2}-({y1})}}{{{x2}-({x1})}}=\\dfrac{{{y2 - y1}}}{{{x2 - x1}}}={m}$。"
        chk = (f"[({y2}-({y1}))/({x2}-({x1})), {y1}-({m})*({x1})]", f"[{m}, {k}]", None, "intermediate")
    else:
        stem = f"点 ${pt(x1, y1)}$ を通り、傾きが ${m}$ の直線の方程式を求めなさい。"
        st0 = f"傾きは ${m}$。"
        chk = (f"{y1}-({m})*({x1})", str(k), None, "intermediate")
    ans = yform(m, k)
    a_, b_, c_ = norm_line(m, -1, k)
    return sa(stem, f"${ans}$", f"$y-({y1})={m}(x-({x1}))$ を整理して ${ans}$。", d=2, v=[ans, f"{lin3(a_, b_, c_)}=0"],
              ap="点 $(x_1,\\,y_1)$ を通り傾き $m$ の直線は $y-y_1=m(x-x_1)$。まず傾きを求める。",
              steps=[st0, f"$y-({y1})={m}(x-({x1}))$。", f"整理して ${ans}$。"],
              alt=[f"$y=mx+n$ に2点（または1点と傾き）を代入して $m,\\ n$ の連立方程式を解いてもよい。"],
              pc=[("傾きを正しく求めている", 1), ("直線の方程式を正しく整理している", 1)],
              pit=["傾きの分子と分母で引く順序をそろえない。", "$y-y_1=m(x-x_1)$ の符号を逆にする。"],
              chk=chk)


@gen("basic_check", 4, ["concept", "condition_check"])
def perp_parallel(r):
    while True:
        a, b = nonzero(r, -3, 3), nonzero(r, -3, 3)
        c = r.randint(-5, 5)
        p, q = r.randint(-3, 3), r.randint(-3, 3)
        ask = r.choice(["perp", "para"])
        perp = norm_line(b, -a, a * q - b * p)
        para = norm_line(a, b, -(a * p + b * q))
        swap = norm_line(b, a, -(b * p + a * q))
        right, other = (perp, para) if ask == "perp" else (para, perp)
        wrongpt = norm_line(right[0], right[1], -right[2]) if right[2] != 0 else norm_line(right[0], right[1], right[2] + 1)
        opts = [right, other, swap, wrongpt]
        texts = [f"${lin3(*o)}=0$" for o in opts]
        if len(set(texts)) == 4 and gcd(abs(a), abs(b)) == 1 and abs(a) != abs(b):
            break
    word = "垂直" if ask == "perp" else "平行"
    oword = "平行" if ask == "perp" else "垂直"
    why = {texts[1]: (f"これは {pt(p, q)} を通り、$\\ell$ に{oword}な直線である。", "平行と垂直の条件の取り違え"),
           texts[2]: (f"$x$ と $y$ の係数を入れかえただけで、符号を変えていない。$a_1a_2+b_1b_2={2 * a * b}\\neq0$、$a_1b_2-a_2b_1={a * a - b * b}\\neq0$ なので、$\\ell$ と垂直にも平行にもならない。", "垂直条件の符号の付け忘れ"),
           texts[3]: (f"向きは正しいが、点 ${pt(p, q)}$ を代入すると成り立たない（通る点を誤っている）。", "定数項の符号・計算の誤り")}
    return mc(f"直線 $\\ell:{lin3(a, b, c)}=0$ に{word}で、点 ${pt(p, q)}$ を通る直線の方程式として正しいものを選びなさい。", texts,
              f"$\\ell$ の係数は $(a,\\,b)=({a},\\,{b})$。" + ("垂直な直線は $" + f"{b}x-({a})y+c'=0" + "$ の形" if ask == "perp" else "平行な直線は $" + f"{a}x+({b})y+c'=0" + "$ の形") + f"で、点 ${pt(p, q)}$ を通るように $c'$ を決めると {texts[0]}。", d=2,
              ap="一般形 $ax+by+c=0$ に平行な直線は $ax+by+c'=0$、垂直な直線は $bx-ay+c'=0$。最後に通る点を代入して定数項を決める。",
              steps=[f"$\\ell$ の傾きは $-\\dfrac{{a}}{{b}}={tx(Fraction(-a, b))}$。",
                     (f"垂直な直線の傾きは ${tx(Fraction(b, a))}$（積が $-1$）。" if ask == "perp" else f"平行な直線の傾きは ${tx(Fraction(-a, b))}$。"),
                     f"点 ${pt(p, q)}$ を通るので {texts[0]}。"],
              alt=["選択肢の直線に点の座標を代入して成り立つか、さらに係数から傾きの関係を確かめる、という2段階の検算で選べる。"],
              pc=[("平行・垂直の条件を正しく使っている", 1), ("通る点の条件を確かめている", 1)],
              why={texts[i]: why[texts[i]] for i in (1, 2, 3)})


@gen("basic_check", 5, ["computation", "condition_check"])
def circle_center(r):
    a, b = r.randint(-5, 5), r.randint(-5, 5)
    R = r.choice([1, 2, 4, 5, 8, 9, 10, 13, 16, 18, 20, 25, 3, 7])
    l, m, n = -2 * a, -2 * b, a * a + b * b - R
    eq = lin3(l, m, n)
    eq = "x^2+y^2" + ("" if eq == "0" else (eq if eq.startswith("-") else "+" + eq))
    rad = sp.sqrt(R)
    return sa(f"方程式 ${eq}=0$ が表す円の中心の座標と半径を答えなさい。", f"中心 ${pt(a, b)}$、半径 ${stex(rad)}$",
              f"平方完成すると ${circ(a, b, R)}$。", d=2, v=[f"({a},{b}), {stex(rad).replace(' ', '')}"],
              ap="$x$ の項、$y$ の項をそれぞれ平方完成して、標準形 $(x-a)^2+(y-b)^2=r^2$ に直す。",
              steps=[f"$x$ について：$x^2{'+' if l > 0 else '-'}{abs(l)}x={sq(a, 'x')}-{a * a}$。" if l else "$x$ の1次の項はないので $x^2$ のまま。",
                     f"$y$ について：$y^2{'+' if m > 0 else '-'}{abs(m)}y={sq(b, 'y')}-{b * b}$。" if m else "$y$ の1次の項はないので $y^2$ のまま。",
                     f"${sq(a, 'x')}+{sq(b, 'y')}={a * a}+{b * b}{'-' if n > 0 else '+'}{abs(n)}={R}$。", f"中心 ${pt(a, b)}$、半径 " + (f"$\\sqrt{{{R}}}={stex(rad)}$。" if stex(rad) != f"\\sqrt{{{R}}}" else f"${stex(rad)}$。")],
              alt=[f"公式：$x^2+y^2+lx+my+n=0$ の中心は $\\left(-\\dfrac{{l}}{{2}},\\ -\\dfrac{{m}}{{2}}\\right)$、半径は $\\sqrt{{\\dfrac{{l^2+m^2}}{{4}}-n}}$。$l={l},\\ m={m},\\ n={n}$ を代入しても同じ結果。"],
              pc=[("平方完成を正しく行っている", 1), ("中心と半径を正しく答えている", 1)],
              pit=["右辺に移項するときの定数項の符号を誤る。", "半径を $r^2$ の値のまま答える。"],
              chk=(f"[-({l})/2, -({m})/2, sqrt(({l})**2/4+({m})**2/4-({n}))]", f"[{a}, {b}, sqrt({R})]", None, "intermediate"))


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 5, ["computation"])
def point_line_dist(r):
    while True:
        a, b = r.choice([(3, 4), (4, 3), (5, 12), (12, 5), (1, 2), (2, 1), (1, 1), (1, 3), (3, -4), (1, -2), (2, -1)])
        c = r.randint(-9, 9)
        x0, y0 = r.randint(-4, 5), r.randint(-4, 5)
        num_ = a * x0 + b * y0 + c
        if num_ != 0:
            break
    val = sp.Abs(num_) / sp.sqrt(a * a + b * b)
    form = r.random() < 0.3 and b != 0
    if form:
        line = yform(Fraction(-a, b), Fraction(-c, b))
        pre = [f"直線を $ax+by+c=0$ の形に直すと ${lin3(a, b, c)}=0$。"]
    else:
        line = f"{lin3(a, b, c)}=0"
        pre = []
    return sa(f"点 $\\mathrm{{A}}{pt(x0, y0)}$ から直線 ${line}$ までの距離を求めなさい。", f"${stex(val)}$",
              f"$d=\\dfrac{{|{a}\\cdot({x0})+({b})\\cdot({y0})+({c})|}}{{\\sqrt{{{a}^2+({b})^2}}}}={stex(val)}$。", d=3, v=[stex(val).replace(" ", "")],
              ap="点と直線の距離の公式 $d=\\dfrac{|ax_0+by_0+c|}{\\sqrt{a^2+b^2}}$ を使う。直線は $ax+by+c=0$ の形にしてから代入する。",
              steps=pre + [f"分子：$|{a}\\cdot({x0})+({b})\\cdot({y0})+({c})|=|{num_}|={abs(num_)}$。", f"分母：$\\sqrt{{{a * a}+{b * b}}}=\\sqrt{{{a * a + b * b}}}$。",
                           f"$d={stex(val)}$" + ("（分母を有理化）。" if sp.sqrt(a * a + b * b).is_Rational is False else "。")],
              alt=["点 $\\mathrm{A}$ を通り直線に垂直な直線との交点 $\\mathrm{H}$ を求め、$\\mathrm{AH}$ を2点間の距離として計算してもよい。"],
              pc=[("直線を $ax+by+c=0$ の形にして公式に代入している", 2), ("分子の絶対値・分母の根号を正しく計算している", 1), ("答えを簡約している", 1)],
              pit=["$y=mx+n$ の形のまま係数を読み取り、$y$ の係数の符号を誤る。", "分子の絶対値をつけ忘れる。"],
              chk=(f"Abs(({a})*({x0})+({b})*({y0})+({c}))/sqrt(({a})**2+({b})**2)", str(val)))


@gen("standard_practice", 5, ["computation", "concept"])
def circle_equation(r):
    kind = r.choice(["diam", "point", "axis", "line"])
    a, b = r.randint(-4, 4), r.randint(-4, 4)
    if kind == "diam":
        dx, dy = r.randint(-4, 4), r.randint(-4, 4)
        if dx == 0 and dy == 0:
            dx = 2
        A, B = (a - dx, b - dy), (a + dx, b + dy)
        R = dx * dx + dy * dy
        stem = f"2点 $\\mathrm{{A}}{pt(*A)}$、$\\mathrm{{B}}{pt(*B)}$ を直径の両端とする円の方程式を求めなさい。"
        steps = [f"中心は $\\mathrm{{AB}}$ の中点 ${pt(a, b)}$。", f"半径は中点と $\\mathrm{{A}}$ の距離で、$r^2=({dx})^2+({dy})^2={R}$。", f"${circ(a, b, R)}$。"]
        ap = "直径の両端が分かっているので、中心は中点、半径は直径の半分（中心から端点までの距離）。"
        chk = (f"(({B[0]})-({A[0]}))**2/4+(({B[1]})-({A[1]}))**2/4", str(R), None, "intermediate")
        alt = f"円周角の定理（直径に対する円周角は直角）から、円周上の点 $\\mathrm{{P}}(x,\\,y)$ について $\\mathrm{{AP}}\\perp\\mathrm{{BP}}$。$(x-({A[0]}))(x-({B[0]}))+(y-({A[1]}))(y-({B[1]}))=0$ を整理しても同じ式になる。"
    elif kind == "point":
        px, py_ = a + r.randint(-4, 4), b + nonzero(r, -4, 4)
        R = (px - a) ** 2 + (py_ - b) ** 2
        stem = f"中心が ${pt(a, b)}$ で、点 ${pt(px, py_)}$ を通る円の方程式を求めなさい。"
        steps = [f"半径の2乗は中心と点の距離の2乗：$({px}-({a}))^2+({py_}-({b}))^2={R}$。", f"${circ(a, b, R)}$。"]
        ap = "半径は中心から通る点までの距離。標準形 $(x-a)^2+(y-b)^2=r^2$ に代入する。"
        chk = (f"({px}-({a}))**2+({py_}-({b}))**2", str(R), None, "intermediate")
        alt = f"$(x-({a}))^2+(y-({b}))^2=r^2$ に点 ${pt(px, py_)}$ を代入して $r^2$ を求めても同じ。"
    elif kind == "axis":
        if b == 0:
            b = 2
        R = b * b
        stem = f"中心が ${pt(a, b)}$ で、$x$ 軸に接する円の方程式を求めなさい。"
        steps = [f"$x$ 軸に接するので、半径は中心の $y$ 座標の絶対値 $|{b}|={abs(b)}$。", f"${circ(a, b, R)}$。"]
        ap = "$x$ 軸に接する円では、中心から $x$ 軸までの距離（$y$ 座標の絶対値）が半径になる。"
        chk = (f"Abs({b})**2", str(R), None, "intermediate")
        alt = f"$x$ 軸 $y=0$ と連立すると $(x-({a}))^2={R}-{R}=0$ となり重解をもつので、接していることが確かめられる。"
    else:
        la, lb = r.choice([(3, 4), (4, 3), (3, -4), (4, -3)])
        rr = r.randint(1, 4)
        sgn = r.choice([1, -1])
        c = sgn * 5 * rr - (la * a + lb * b)
        R = rr * rr
        stem = f"中心が ${pt(a, b)}$ で、直線 ${lin3(la, lb, c)}=0$ に接する円の方程式を求めなさい。"
        steps = [f"半径は中心と直線の距離：$\\dfrac{{|{la}\\cdot({a})+({lb})\\cdot({b})+({c})|}}{{\\sqrt{{{la * la}+{lb * lb}}}}}=\\dfrac{{{abs(la * a + lb * b + c)}}}{{5}}={rr}$。", f"${circ(a, b, R)}$。"]
        ap = "円が直線に接するとき、中心と直線の距離が半径に等しい。点と直線の距離の公式を使う。"
        chk = (f"(Abs(({la})*({a})+({lb})*({b})+({c}))/sqrt({la * la + lb * lb}))**2", str(R), None, "intermediate")
        alt = "円の方程式と直線の方程式を連立して判別式 $D=0$ となることを確かめてもよい（計算は重くなる）。"
    ans = circ(a, b, R)
    return sa(stem, f"${ans}$", f"中心 ${pt(a, b)}$、半径の2乗 ${R}$ より ${ans}$。", d=3, v=[ans],
              ap=ap, steps=steps, alt=[alt],
              pc=[("中心を正しく決めている", 1), ("半径（の2乗）を正しく求めている", 2), ("円の方程式を正しく書いている", 1)],
              pit=["右辺に $r$ を書き、$r^2$ にし忘れる。", "中心の座標の符号を式の中で逆にし忘れる（$(x-a)^2$ の $a$）。"],
              chk=chk)


@gen("standard_practice", 5, ["computation", "concept"])
def tangent_at(r):
    R = r.choice([5, 10, 13, 25, 17, 20, 8, 2, 26, 29])
    dx, dy = r.choice([p for p in lattice_on(R)])
    a, b = (0, 0) if r.random() < 0.5 else (r.randint(-3, 3), r.randint(-3, 3))
    x1, y1 = a + dx, b + dy
    K = R + dx * a + dy * b
    A, B, Cc = norm_line(dx, dy, -K)
    ans = f"{lin3(A, B, 0)}={-Cc}"
    ceq = circ(a, b, R)
    return sa(f"点 $\\mathrm{{P}}{pt(x1, y1)}$ は円 ${ceq}$ 上にある。点 $\\mathrm{{P}}$ における円の接線の方程式を求めなさい。", f"${ans}$",
              f"接線は半径 $\\mathrm{{CP}}$（$\\mathrm{{C}}{pt(a, b)}$）に垂直で $\\mathrm{{P}}$ を通る直線。" + ("公式 $x_1x+y_1y=r^2$ より" if (a, b) == (0, 0) else "公式 $(x_1-a)(x-a)+(y_1-b)(y-b)=r^2$ より") + f" ${ans}$。", d=3,
              v=[ans, f"{lin3(A, B, Cc)}=0"],
              ap="円の接線は接点を通る半径に垂直。中心が原点なら公式 $x_1x+y_1y=r^2$、中心が $(a,\\,b)$ なら $(x_1-a)(x-a)+(y_1-b)(y-b)=r^2$ を使う。",
              steps=([f"公式 $x_1x+y_1y=r^2$ に $x_1={dx},\\ y_1={dy},\\ r^2={R}$ を代入して ${lin3(dx, dy, 0)}={R}$。"]
                     if (a, b) == (0, 0) else
                     [f"中心 $\\mathrm{{C}}{pt(a, b)}$、$\\mathrm{{P}}-\\mathrm{{C}}=({dx},\\,{dy})$。", f"公式より $({dx})(x-({a}))+({dy})(y-({b}))={R}$。"])
                    + [f"整理して ${ans}$。"],
              alt=[f"半径 $\\mathrm{{CP}}$ の傾き" + (f" ${tx(Fraction(dy, dx))}$" if dx else "（$y$ 軸に平行）") + " に垂直な傾きをもち $\\mathrm{P}$ を通る直線として求めても同じ。" if dy else "接点の $y$ 座標が中心と同じなので、接線は $y$ 軸に平行な直線になる。"],
              pc=[("接線の公式（または半径との垂直）を正しく使っている", 2), ("接線の方程式を正しく整理している", 2)],
              pit=["中心が原点でない円に $x_1x+y_1y=r^2$ をそのまま使う。" if (a, b) != (0, 0) else "右辺を $r$ とする（正しくは $r^2$）。", "接点の座標の符号を誤る。"],
              chk=(f"({dx})*({x1}-({a}))+({dy})*({y1}-({b}))", str(R), None, "intermediate"))


@gen("standard_practice", 5, ["concept", "condition_check"])
def circle_line_pos(r):
    a, b = r.randint(-3, 3), r.randint(-3, 3)
    rr = r.randint(2, 5)
    la, lb = r.choice([(3, 4), (4, 3), (3, -4), (4, -3)])
    kind = r.choice(["two", "tan", "none"])
    d = {"two": r.randint(1, rr - 1), "tan": rr, "none": rr + r.randint(1, 3)}[kind]
    c = r.choice([1, -1]) * 5 * d - (la * a + lb * b)
    lab = {"two": "異なる2点で交わる", "tan": "接する", "none": "共有点をもたない"}
    ans = lab[kind]
    wrong = [v for k, v in lab.items() if k != kind] + ["直線が円の中心を通る"]
    why = {lab["two"]: ("2点で交わるのは $d<r$ のとき。この問題では $d\\geqq r$。", "距離と半径の比較の誤り"),
           lab["tan"]: ("接するのは $d=r$ のとき。この問題では $d\\neq r$。", "距離と半径の比較の誤り"),
           lab["none"]: ("共有点をもたないのは $d>r$ のとき。この問題では $d\\leqq r$。", "距離と半径の比較の誤り"),
           "直線が円の中心を通る": (f"中心を通るなら $d=0$。この問題では $d={d}\\neq0$。", "中心の座標を直線の式に代入していない")}
    R = rr * rr
    return mc(f"円 ${circ(a, b, R)}$ と直線 ${lin3(la, lb, c)}=0$ の位置関係として正しいものを選びなさい。", [ans] + wrong,
              f"中心 ${pt(a, b)}$ と直線の距離 $d=\\dfrac{{|{la * a + lb * b + c}|}}{{5}}={d}$、半径 $r={rr}$。" + {"two": "$d<r$ より2点で交わる。", "tan": "$d=r$ より接する。", "none": "$d>r$ より共有点をもたない。"}[kind], d=3,
              ap="円と直線の位置関係は、中心と直線の距離 $d$ と半径 $r$ の大小で決まる。",
              steps=[f"中心 ${pt(a, b)}$、半径 ${rr}$。", f"$d=\\dfrac{{|{la}\\cdot({a})+({lb})\\cdot({b})+({c})|}}{{\\sqrt{{{la * la}+{lb * lb}}}}}={d}$。",
                     {"two": f"${d}<{rr}$ より $d<r$。", "tan": f"$d=r={rr}$。", "none": f"${d}>{rr}$ より $d>r$。"}[kind]],
              alt=["円と直線の方程式を連立して1文字を消去し、2次方程式の判別式の符号で判定してもよい（$D>0$：2点、$D=0$：接する、$D<0$：共有点なし）。"],
              pc=[("中心と半径を読み取り、距離を正しく計算している", 2), ("$d$ と $r$ を比べて正しく判断している", 2)],
              why={w: why[w] for w in wrong},
              chk=(f"Abs(({la})*({a})+({lb})*({b})+({c}))/5", str(d), None, "intermediate"))


# ======================================================================
# C 思考力・記述応用
# ======================================================================

@gen("thinking_writing", 3, ["written_reasoning", "condition_check"])
def apollonius(r):
    m, n = r.choice([(2, 1), (1, 2), (3, 1), (1, 3), (3, 2), (2, 3)])
    k = m * m - n * n
    d = abs(k) * r.choice([1, 2]) if abs(k) <= 5 else abs(k)
    s, t = r.randint(-3, 3), r.randint(-3, 3)
    A, B = (s, t), (s + d, t)
    cx = s + Fraction(m * m * d, k)
    rad = Fraction(m * n * d, abs(k))
    # 条件 n^2 AP^2 = m^2 BP^2
    ans = f"中心 ${pt(cx, t)}$、半径 ${tx(rad)}$ の円"
    eq = circ(cx, t, rad * rad)
    ix = s + Fraction(m * d, m + n)
    ex = s + Fraction(m * d, m - n)
    return desc(f"2点 $\\mathrm{{A}}{pt(*A)}$、$\\mathrm{{B}}{pt(*B)}$ に対して、$\\mathrm{{AP}}:\\mathrm{{BP}}={m}:{n}$ を満たす点 $\\mathrm{{P}}$ の軌跡を求めなさい。",
                ans + f"（方程式 ${eq}$）",
                f"$\\mathrm{{P}}(x,\\,y)$ とおき、${n if n > 1 else ''}\\mathrm{{AP}}={m if m > 1 else ''}\\mathrm{{BP}}$ の両辺を2乗した式を整理すると ${eq}$。", rubric=[
                    ("$\\mathrm{P}(x,\\,y)$ とおき、条件を2乗した式で表している", 3), ("式を正しく整理して円の方程式を得ている", 3), ("軌跡を図形として答えている（逆の確認を含む）", 2)], d=4, p=8, lines=10,
                ap="距離の比の条件は、根号を避けるために $n\\mathrm{AP}=m\\mathrm{BP}$ を2乗して $n^2\\mathrm{AP}^2=m^2\\mathrm{BP}^2$ として式にする。",
                steps=[f"$\\mathrm{{P}}(x,\\,y)$ とおく。条件は ${n if n > 1 else ''}\\mathrm{{AP}}={m if m > 1 else ''}\\mathrm{{BP}}$、両辺は $0$ 以上なので2乗して ${n * n if n > 1 else ''}\\mathrm{{AP}}^2={m * m if m > 1 else ''}\\mathrm{{BP}}^2$ と同値。",
                       f"${n * n if n > 1 else ''}\\{{{sq(s, 'x')}+{sq(t, 'y')}\\}}={m * m if m > 1 else ''}\\{{{sq(s + d, 'x')}+{sq(t, 'y')}\\}}$。",
                       f"展開して整理すると ${eq}$。", f"逆にこの円上の点は条件を満たす。よって軌跡は{ans}。"],
                alt=[f"検算：線分 $\\mathrm{{AB}}$ を ${m}:{n}$ に内分する点 $({tx(ix)},\\,{t})$ と外分する点 $({tx(ex)},\\,{t})$ は条件を満たし、この2点を直径の両端とする円が答えの円に一致する（中心の $x$ 座標 ${tx(cx)}$、半径 ${tx(rad)}$ の円）。"],
                pc=[("条件の式", 3), ("整理", 3), ("図形として答える", 2)],
                pit=["$\\mathrm{AP}:\\mathrm{BP}=m:n$ を $m\\mathrm{AP}=n\\mathrm{BP}$ と逆に立てる。", "方程式だけを書き、中心と半径を答えない。"],
                chk=(f"expand(({n * n})*((x-({s}))**2+(y-({t}))**2)-({m * m})*((x-({s + d}))**2+(y-({t}))**2))",
                     f"expand(({n * n - m * m})*((x-({fpy(cx)}))**2+(y-({t}))**2-({fpy(rad * rad)})))", "expand", "intermediate"))


@gen("thinking_writing", 3, ["cross_unit", "written_reasoning"], rel=["HS-MATH1-U03"])
def locus_midpoint(r):
    while True:
        b, c = r.randint(-4, 4), r.randint(-4, 4)
        a1, a2 = r.randint(-3, 3), r.randint(-4, 4)
        if (a1 * a1 - a1 * b + c + a2) % 2 == 0:
            break
    B = b - 2 * a1
    Cc = (a1 * a1 - a1 * b + c + a2) // 2
    par = f"y={poly_s(1, b, c)}"
    ans = f"y={poly_s(2, B, Cc)}"
    return desc(f"点 $\\mathrm{{Q}}$ が放物線 ${par}$ 上を動くとき、点 $\\mathrm{{A}}{pt(a1, a2)}$ と $\\mathrm{{Q}}$ を結ぶ線分 $\\mathrm{{AQ}}$ の中点 $\\mathrm{{M}}$ の軌跡を求めなさい。",
                f"放物線 ${ans}$",
                f"$\\mathrm{{Q}}(s,\\,t)$、$\\mathrm{{M}}(x,\\,y)$ とおくと $s=2x{'-' if a1 > 0 else '+'}{abs(a1)}$、$t=2y{'-' if a2 > 0 else '+'}{abs(a2)}$。これを $t={poly_s(1, b, c, 's')}$ に代入して整理する。".replace("+0", "").replace("-0", ""), rubric=[
                    ("動く点 $\\mathrm{Q}$ と中点 $\\mathrm{M}$ の座標を文字でおき、中点の関係式を立てている", 3), ("$\\mathrm{Q}$ の座標を $\\mathrm{M}$ の座標で表し、放物線の式に代入している", 3), ("整理して軌跡を答えている", 2)], d=4, p=8, lines=10,
                ap="軌跡を求めたい点 $\\mathrm{M}(x,\\,y)$ と、条件が分かっている点 $\\mathrm{Q}(s,\\,t)$ の関係を式にし、$s,\\ t$ を消去する（つなぎの文字の消去）。",
                steps=[f"$\\mathrm{{Q}}(s,\\,t)$ とおくと $t={poly_s(1, b, c, 's')}$ …①。", f"$\\mathrm{{M}}(x,\\,y)$ は中点なので $x=\\dfrac{{s{shift_s(a1)}}}{{2}}$、$y=\\dfrac{{t{shift_s(a2)}}}{{2}}$。",
                       f"$s=2x{shift_s(-a1)}$、$t=2y{shift_s(-a2)}$ を①に代入：$2y{shift_s(-a2)}=(2x{shift_s(-a1)})^2{cterm_s(b, f'(2x{shift_s(-a1)})')}{shift_s(c)}$。",
                       f"整理して ${ans}$。$s$ はすべての実数をとるので、$x$ もすべての実数をとり、軌跡は放物線全体。"],
                alt=[f"検算：$\\mathrm{{Q}}$ が放物線の頂点など具体的な点のとき、中点 $\\mathrm{{M}}$ が答えの放物線上にあるかを確かめる。例えば $s=0$ のとき $\\mathrm{{Q}}(0,\\,{c})$、中点 $\\left({tx(Fraction(a1, 2))},\\,{tx(Fraction(c + a2, 2))}\\right)$ は ${ans}$ を満たす。二次関数（数学Ⅰ）の平行移動・拡大の見方でも、$x^2$ の係数が $2$ になる理由が説明できる。"],
                pc=[("中点の関係式", 3), ("代入と消去", 3), ("軌跡の答え", 2)],
                pit=["中点の座標を $\\dfrac{s-a}{2}$ のように差で書く。", "代入後の展開で $(2x)^2=4x^2$ の係数を誤る。"],
                chk=(f"expand(((2*x-({a1}))**2+({b})*(2*x-({a1}))+({c})+({a2}))/2)", f"2*x**2+({B})*x+({Cc})", "expand", "intermediate"))


def poly_s(a, b, c, var="x"):
    from hs_pack_lib import poly
    return poly(a, b, c, var=var)


def shift_s(v):
    return "" if v == 0 else (f"+{v}" if v > 0 else f"{v}")


def cterm_s(c, body):
    if c == 0:
        return ""
    if c == 1:
        return f"+{body}"
    if c == -1:
        return f"-{body}"
    return f"+{c}{body}" if c > 0 else f"{c}{body}"


@gen("thinking_writing", 2, ["application", "written_reasoning"])
def lp_region(r):
    while True:
        u, v = r.randint(1, 5), r.randint(1, 5)
        k1, k2 = r.choice([2, 3]), r.choice([2, 3])
        c1, c2 = k1 * u + v, u + k2 * v
        p, q = r.randint(1, 4), r.randint(1, 4)
        X1 = Fraction(c1, k1)
        Y2 = Fraction(c2, k2)
        verts = [((0, 0), 0), ((X1, 0), p * X1), ((u, v), p * u + q * v), ((0, Y2), q * Y2)]
        best = max(verts, key=lambda t: t[1])
        if sum(1 for t in verts if t[1] == best[1]) == 1:
            break
    (bx, by), M = best
    obj = f"{'' if p == 1 else p}x+{'' if q == 1 else q}y"
    poly_pts = [(0, 0), (float(X1), 0), (u, v), (0, float(Y2))]
    fig = figure("連立不等式の表す領域（四角形）", plane((-1, max(int(X1) + 2, 7)), (-1, max(int(Y2) + 2, 7)), unit=16, polygons=[poly_pts],
                                                lines=[(-k1, c1, ""), (-1 / k2, c2 / k2, "")], points=[(u, v, f"({u},{v})")]))
    return desc(f"$x,\\ y$ が4つの不等式 $x\\geqq0$、$y\\geqq0$、${k1}x+y\\leqq{c1}$、$x+{k2}y\\leqq{c2}$ を満たすとき、${obj}$ の最大値と、そのときの $x,\\ y$ の値を求めなさい。",
                f"最大値 ${tx(M)}$（$x={tx(bx)},\\ y={tx(by)}$）",
                f"領域は4点 $(0,\\,0)$、$({tx(X1)},\\,0)$、$({u},\\,{v})$、$(0,\\,{tx(Y2)})$ を頂点とする四角形。${obj}=k$ とおいた直線を平行移動し、$k$ が最大になる点を調べる。", rubric=[
                    ("領域を正しく図示し、頂点の座標を求めている", 3), ("${obj}=k$ とおいた直線の動きで最大となる点を判断している", 3), ("最大値とそのときの $x,\\ y$ を正しく答えている", 2)], d=4, p=8, lines=10, fig=fig,
                ap=f"${obj}=k$ とおくと、これは傾き ${tx(Fraction(-p, q))}$、$y$ 切片 ${tx(Fraction(1, q)) if q > 1 else ''}k$ の直線。領域と共有点をもつ範囲で $y$ 切片が最大になるときを考える。",
                steps=[f"境界線 ${k1}x+y={c1}$ と $x+{k2}y={c2}$ の交点は $({u},\\,{v})$。領域の頂点は $(0,\\,0)$、$({tx(X1)},\\,0)$、$({u},\\,{v})$、$(0,\\,{tx(Y2)})$。",
                       f"${obj}=k$ は傾き ${tx(Fraction(-p, q))}$ の直線。境界線の傾き $-{k1}$、${tx(Fraction(-1, k2))}$ と比べて、直線が最後に領域から離れる点を判断する。",
                       "各頂点での値：" + "、".join(f"$({tx(x)},\\,{tx(y)})$ で ${tx(val)}$" for (x, y), val in verts) + "。",
                       f"最大値 ${tx(M)}$（$x={tx(bx)},\\ y={tx(by)}$）。"],
                alt=["領域が多角形で目的の式が一次式のとき、最大値・最小値は必ず頂点でとる。頂点の値をすべて計算して比べる方法でも確実に求まる。"],
                pc=[("領域と頂点", 3), ("直線の平行移動による判断", 3), ("答え", 2)],
                pit=["交点 $(" + f"{u},{v}" + ")$ だけで最大と決めつけ、他の頂点と比べない。", "不等号の向きを誤り、境界線の反対側を領域とする。"],
                chk=(f"Max(0, {p}*{fpy(X1)}, {p}*{u}+{q}*{v}, {q}*{fpy(Y2)})", fpy(M), None, "intermediate"))


@gen("thinking_writing", 2, ["condition_check", "multiple_solutions"])
def tangent_external(r):
    cands = []
    for R in (5, 10, 13, 25):
        pts = lattice_on(R)
        for i, (x1, y1) in enumerate(pts):
            for (x2, y2) in pts[i + 1:]:
                det = x1 * y2 - x2 * y1
                if det == 0:
                    continue
                X, Y = Fraction(R * (y2 - y1), det), Fraction(R * (x1 - x2), det)
                if X.denominator == 1 and Y.denominator == 1 and abs(X) <= 9 and abs(Y) <= 9:
                    cands.append((R, (x1, y1), (x2, y2), int(X), int(Y)))
    R, T1, T2, X, Y = r.choice(cands)
    n1, n2 = norm_line(T1[0], T1[1], -R), norm_line(T2[0], T2[1], -R)
    l1, l2 = f"{lin3(n1[0], n1[1], 0)}={-n1[2]}", f"{lin3(n2[0], n2[1], 0)}={-n2[2]}"
    return desc(f"点 $\\mathrm{{A}}{pt(X, Y)}$ から円 $x^2+y^2={R}$ に引いた接線の方程式と、接点の座標を求めなさい。",
                f"接線 ${l1}$（接点 ${pt(*T1)}$）、${l2}$（接点 ${pt(*T2)}$）",
                f"接点を $(x_1,\\,y_1)$ とおくと接線は $x_1x+y_1y={R}$。これが $\\mathrm{{A}}$ を通り、接点が円周上にある条件から求める。", rubric=[
                    ("接点を $(x_1,\\,y_1)$ とおいて接線の方程式を立てている（または傾きをおいて距離の条件を立てている）", 3),
                    ("連立方程式を解いて接点を2つとも求めている", 3), ("接線と接点を正しく答えている", 2)], d=5, p=8, lines=12,
                ap="接点を文字でおけば接線の公式が使える。「$\\mathrm{A}$ を通る」「接点は円周上」の2条件で接点が決まる。",
                steps=[f"接点 $(x_1,\\,y_1)$ とおくと、接線は $x_1x+y_1y={R}$、かつ $x_1^2+y_1^2={R}$ …①。",
                       f"接線が $\\mathrm{{A}}{pt(X, Y)}$ を通るので ${lin3(X, Y, 0).replace('x', 'x_1').replace('y', 'y_1')}={R}$ …②。",
                       f"①②を連立して $(x_1,\\,y_1)={pt(*T1)},\\ {pt(*T2)}$。",
                       f"接線は ${l1}$、${l2}$。"],
                alt=[f"傾き $m$ の直線 $y-({Y})=m(x-({X}))$ とおき、原点との距離が $\\sqrt{{{R}}}$ に等しい条件から $m$ を求める方法もある。ただし、この方法では $y$ 軸に平行な接線（傾きをもたない直線）があるときに見落とすので、別に確かめる必要がある。"],
                pc=[("方針と式の設定", 3), ("連立方程式の解", 3), ("答え", 2)],
                pit=["傾き $m$ でおく方法で、$y$ 軸に平行な接線の有無を確かめない。", "接点を1つしか求めない。"],
                chk=(f"[({T1[0]})*({X})+({T1[1]})*({Y}), ({T2[0]})*({X})+({T2[1]})*({Y}), ({T1[0]})**2+({T1[1]})**2, ({T2[0]})**2+({T2[1]})**2]", f"[{R}, {R}, {R}, {R}]", None, "intermediate"))


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(stem, wrong, step, etype, tempt, fix, ans, expl, steps, ap, alt, pit, chk=None, d=3):
    return desc(f"{stem}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい答えを求めなさい。", ans, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい解答を途中式とともに示している", 3), ("最終的な答えが正しい", 1)], d=d, p=6, lines=6,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい途中式", 3), ("正しい答え", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix), chk=chk)


@gen("error_correction", 3, ["common_error", "condition_check"])
def err_perp_slope(r):
    m = r.choice([2, 3, -2, -3, 4, -4])
    k = r.randint(-5, 5)
    p, q = r.randint(-3, 3), r.randint(-3, 3)
    wm, cm = Fraction(1, m), Fraction(-1, m)
    wrong_line = yform(wm, q - wm * p)
    right_line = yform(cm, q - cm * p)
    wrong = f"垂直な直線の傾きは ${m}$ の逆数で ${tx(wm)}$。$y-({q})={tx(wm)}(x-({p}))$ より ${wrong_line}$"
    fix = f"傾きを $m'$ とすると ${m}m'=-1$ より $m'={tx(cm)}$。$y-({q})={tx(cm)}(x-({p}))$ より ${right_line}$"
    return err_item(f"点 ${pt(p, q)}$ を通り、直線 ${yform(m, k)}$ に垂直な直線の方程式を求めなさい。", wrong, "垂直な直線の傾きを決める部分", "formula",
                    "「垂直なら逆数」という覚え方が中途半端で、符号を変えることを忘れている。",
                    fix, f"${right_line}$",
                    f"2直線が垂直 $\\iff$ 傾きの積が $-1$。${m}\\times\\left({tx(wm)}\\right)=1\\neq-1$ なので、生徒の直線は垂直ではない。",
                    [f"与えられた直線の傾きは ${m}$。", f"垂直な直線の傾き $m'$ は ${m}m'=-1$ より $m'={tx(cm)}$。", f"$y-({q})={tx(cm)}(x-({p}))$ を整理して ${right_line}$。"],
                    "垂直条件は「傾きの積が $-1$」。逆数にして符号を変える。",
                    [f"求めた2直線の傾きの積が ${m}\\times\\left({tx(cm)}\\right)=-1$ になることを確かめる。"],
                    ["符号を変え忘れる。"],
                    chk=(f"({m})*({fpy(cm)})", "-1", None, "intermediate"), d=2)


@gen("error_correction", 3, ["common_error", "computation"])
def err_circle_radius(r):
    while True:
        a, b = nonzero(r, -4, 4), r.randint(-4, 4)
        R = r.choice([4, 9, 16, 25, 1, 36])
        n = a * a + b * b - R
        W = a * a + b * b + n
        if n != 0 and W > 0 and W != R:
            break
    eq = "x^2+y^2" + ("" if lin3(-2 * a, -2 * b, n).startswith("-") else "+") + lin3(-2 * a, -2 * b, n)
    wr = sp.sqrt(W)
    wrong = f"${sq(a, 'x')}+{sq(b, 'y')}={a * a}+{b * b}{'+' if n > 0 else '-'}{abs(n)}={W}$ より、中心 ${pt(a, b)}$、半径 ${stex(wr)}$"
    fix = f"${sq(a, 'x')}-{a * a}+{sq(b, 'y')}-{b * b}{'+' if n > 0 else '-'}{abs(n)}=0$ より ${sq(a, 'x')}+{sq(b, 'y')}={a * a}+{b * b}{'-' if n > 0 else '+'}{abs(n)}={R}$。中心 ${pt(a, b)}$、半径 ${isqrt(R)}$"
    return err_item(f"方程式 ${eq}=0$ が表す円の中心と半径を求めなさい。", wrong, "右辺の定数項（移項したときの符号）", "sign",
                    "平方完成で出てきた定数 $" + f"{a * a},\\ {b * b}" + "$ と、もとの定数項 $" + str(n) + "$ を、どちらも同じ符号で右辺に集めてしまった。移項で符号が変わることを意識していない。",
                    fix, f"中心 ${pt(a, b)}$、半径 ${isqrt(R)}$",
                    f"定数項 ${n}$ は左辺にあるので、右辺に移すと ${-n}$ になる。",
                    [f"${sq(a, 'x')}-{a * a}+{sq(b, 'y')}-{b * b}{'+' if n > 0 else '-'}{abs(n)}=0$。", f"定数を右辺に移項：${a * a}+{b * b}{'-' if n > 0 else '+'}{abs(n)}={R}$。", f"中心 ${pt(a, b)}$、半径 ${isqrt(R)}$。"],
                    "平方完成したら、左辺に残る定数をすべて書いてから右辺へ移項する。",
                    [f"答えの円 ${circ(a, b, R)}$ を展開すると、もとの方程式にもどることで確かめられる。生徒の答えを展開すると定数項が ${a * a + b * b - W}$ になり一致しない。"],
                    ["移項の符号を誤る。"],
                    chk=(f"expand((x-({a}))**2+(y-({b}))**2-{R})", f"x**2+y**2+({-2 * a})*x+({-2 * b})*y+({n})", "expand", "intermediate"))


@gen("error_correction", 2, ["common_error", "computation"])
def err_dist_sign(r):
    while True:
        m, k = nonzero(r, -3, 3), r.randint(-5, 5)
        x0, y0 = r.randint(-3, 3), nonzero(r, -4, 4)
        right_n, wrong_n = m * x0 - y0 + k, m * x0 + y0 + k
        if right_n != 0 and abs(right_n) != abs(wrong_n):
            break
    den = m * m + 1
    val = sp.Abs(right_n) / sp.sqrt(den)
    wv = sp.Abs(wrong_n) / sp.sqrt(den)
    wrong = f"直線を ${lin3(m, 1, k)}=0$ として、$d=\\dfrac{{|{m}\\cdot({x0})+({y0})+({k})|}}{{\\sqrt{{({m})^2+1^2}}}}={stex(wv)}$"
    fix = f"直線は ${lin3(m, -1, k)}=0$。$d=\\dfrac{{|{m}\\cdot({x0})-({y0})+({k})|}}{{\\sqrt{{({m})^2+(-1)^2}}}}={stex(val)}$"
    return err_item(f"点 ${pt(x0, y0)}$ と直線 ${yform(m, k)}$ の距離を求めなさい。", wrong, "直線を $ax+by+c=0$ の形に直す部分（$y$ の係数の符号）", "sign",
                    "$y=" + f"{m}x" + "\\cdots$ の $y$ を左辺に残したまま、右辺の項を同じ符号で並べてしまった。移項すると $y$ の係数は $-1$ になる。",
                    fix, f"${stex(val)}$",
                    f"${yform(m, k)}$ を移項すると ${lin3(m, -1, k)}=0$ で、$a={m},\\ b=-1,\\ c={k}$。",
                    [f"${yform(m, k)}$ より ${lin3(m, -1, k)}=0$。", f"分子：$|{m}\\cdot({x0})-({y0})+({k})|={abs(right_n)}$。", f"分母：$\\sqrt{{{den}}}$。$d={stex(val)}$。"],
                    "公式を使う前に、直線を必ず「$ax+by+c=0$」（右辺 $0$）の形に書き直す。",
                    [f"点 ${pt(x0, y0)}$ を通り直線に垂直な直線との交点を求め、2点間の距離として計算しても ${stex(val)}$ になる。"],
                    ["$y$ の係数の符号を誤る。"],
                    chk=(f"Abs(({m})*({x0})-({y0})+({k}))/sqrt({den})", str(val), None, "intermediate"))


@gen("error_correction", 2, ["common_error", "condition_check"])
def err_tangent_vertical(r):
    while True:
        rr = r.randint(1, 4)
        q = r.choice([v for v in range(-6, 7) if abs(v) > rr or (v != 0 and abs(v) == rr)])
        if q * q != rr * rr:
            break
    m = Fraction(q * q - rr * rr, 2 * q * rr)
    rm = "m" if rr == 1 else f"{rr}m"
    A, B, Cc = norm_line(int((q * q - rr * rr)), -2 * q * rr, int(2 * q * q * rr - rr * (q * q - rr * rr)))
    line2 = f"{lin3(A, B, Cc)}=0"
    wrong = (f"接線を $y-({q})=m(x-{rr})$ とおく。原点との距離が ${rr}$ なので $\\dfrac{{|{rm}-({q})|}}{{\\sqrt{{m^2+1}}}}={rr}$。"
             f"2乗して整理すると $m={tx(m)}$。よって接線は1本で ${line2}$")
    fix = f"傾きをもたない直線 $x={rr}$ も点 $({rr},\\,{q})$ を通り、原点との距離が ${rr}$ なので接線。接線は $x={rr}$ と ${line2}$ の2本"
    return err_item(f"点 ${pt(rr, q)}$ から円 $x^2+y^2={rr * rr}$ に引いた接線の方程式をすべて求めなさい。", wrong,
                    "接線を傾き $m$ でおいた最初の段階（$y$ 軸に平行な直線の見落とし）", "condition",
                    "「直線は $y-y_1=m(x-x_1)$ とおける」と思い込み、傾きが存在しない（$y$ 軸に平行な）直線がこの形で表せないことを忘れている。2乗した方程式が1次方程式になったことも、見落としの合図である。",
                    fix, f"$x={rr}$、${line2}$",
                    "円の外の点からは接線が2本引ける。傾き $m$ でおいた方法で1本しか得られないときは、$y$ 軸に平行な直線を別に調べる。",
                    [f"$y$ 軸に平行な直線 $x={rr}$ は点 ${pt(rr, q)}$ を通り、原点との距離は ${rr}$（半径）なので接線。",
                     f"傾き $m$ の場合：$({rm}-({q}))^2={'' if rr == 1 else rr * rr}(m^2+1)$ を整理すると $m$ の1次方程式になり $m={tx(m)}$。", f"接線は $x={rr}$ と ${line2}$。"],
                    "直線を傾きでおくときは、傾きをもたない場合を必ず別に確かめる。",
                    [f"接点を $(x_1,\\,y_1)$ とおいて $x_1x+y_1y={rr * rr}$ が ${pt(rr, q)}$ を通る条件から求めると、接点 $({rr},\\,0)$ が得られ、$x={rr}$ が漏れなく出てくる。"],
                    ["傾きをもたない接線を見落とす。"],
                    chk=(f"solve(({rr}*m-({q}))**2-{rr * rr}*(m**2+1), m)", f"[{fpy(m)}]", "set", "intermediate"))


GENERATORS = [points_basic, line_through, perp_parallel, circle_center,
              point_line_dist, circle_equation, tangent_at, circle_line_pos,
              apollonius, locus_midpoint, lp_region, tangent_external,
              err_perp_slope, err_circle_radius, err_dist_sign, err_tangent_vertical]
