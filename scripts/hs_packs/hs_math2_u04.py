"""単元パック：数学Ⅱ 三角関数（一般角と弧度法・グラフ・加法定理・合成）。"""
import math
from fractions import Fraction as F

import sympy as sp

from banks._common import desc, figure, mc, plane, sa
from hs_pack_lib import board, check, definition, derivation, example, gen, guide, intro, lesson, poly, summary, theorem, tp

UNIT_ID = "HS-MATH2-U04"

FN = {"sin": sp.sin, "cos": sp.cos, "tan": sp.tan}
MFN = {"sin": math.sin, "cos": math.cos, "tan": math.tan}


# ----------------------------------------------------------------------
# 補助
# ----------------------------------------------------------------------

def tex(v):
    return sp.latex(sp.nsimplify(v)).replace("\\frac", "\\dfrac")


def py(v):
    return str(sp.nsimplify(v))


def rad(q):
    """π の有理数倍 q（Fraction）を LaTeX で表す。"""
    q = F(q)
    if q == 0:
        return "0"
    s = "-" if q < 0 else ""
    n, d = abs(q.numerator), q.denominator
    if d == 1:
        return f"{s}\\pi" if n == 1 else f"{s}{n}\\pi"
    if n == 1:
        return f"{s}\\dfrac{{\\pi}}{{{d}}}"
    return f"{s}\\dfrac{{{n}}}{{{d}}}\\pi"


def rpy(q):
    q = F(q)
    return f"Rational({q.numerator},{q.denominator})*pi"


def arg(q):
    """関数の引数として使う角（負なら括弧でくくる）。"""
    return f"\\left({rad(q)}\\right)" if F(q) < 0 else rad(q)


def val(fn, q):
    q = F(q)
    return sp.nsimplify(FN[fn](sp.pi * sp.Rational(q.numerator, q.denominator)))


def thetas(qs):
    return ",\\ ".join(rad(q) for q in qs)


def coef(c, first=False):
    """係数（sympy）の表記。1 → ''、-1 → '-'、正の非先頭には + をつける。"""
    c = sp.nsimplify(c)
    if c == 1:
        return "" if first else "+"
    if c == -1:
        return "-"
    t = tex(c)
    return t if (first or t.startswith("-")) else "+" + t


def lin(a, b):
    """a sinθ + b cosθ の LaTeX。"""
    return f"{coef(a, True)}\\sin\\theta{coef(b)}\\cos\\theta"


def angle_of(a, b):
    """cosα=a/r, sinα=b/r を満たす α（-π<α≦π）を π の有理数倍で返す。"""
    return F(str(sp.nsimplify(sp.atan2(b, a) / sp.pi)))


def rsin(r, al):
    rt = "" if r == 1 else tex(r)
    if al == 0:
        return f"{rt}\\sin\\theta"
    return f"{rt}\\sin\\left(\\theta{'+' if al > 0 else '-'}{rad(abs(al))}\\right)"


def grid_solutions(fn, v, m=1, lo=F(0), hi=F(2), lo_closed=True, hi_closed=False):
    """fn(mθ)=v の解のうち lo≦θ<hi（端の開閉は指定）にあるものを π/72 刻みで探す。"""
    out = []
    fv = float(v)
    for k in range(int(lo * 72), int(hi * 72) + 1):
        q = F(k, 72)
        if (q == lo and not lo_closed) or (q == hi and not hi_closed) or q < lo or q > hi:
            continue
        x = m * math.pi * float(q)
        if fn == "tan" and abs(math.cos(x)) < 1e-9:
            continue
        if abs(MFN[fn](x) - fv) < 1e-9:
            out.append(q)
    return out


def dom(lo, hi, lo_closed=True, hi_closed=False):
    return f"{rad(lo)}{'\\leqq' if lo_closed else '<'}\\theta{'\\leqq' if hi_closed else '<'}{rad(hi)}"


TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (12, 35, 37)]
QUAD = {1: ("0<\\theta<\\dfrac{\\pi}{2}", 1, 1), 2: ("\\dfrac{\\pi}{2}<\\theta<\\pi", 1, -1),
        3: ("\\pi<\\theta<\\dfrac{3}{2}\\pi", -1, -1), 4: ("\\dfrac{3}{2}\\pi<\\theta<2\\pi", -1, 1)}


def sin_curve(x):
    return math.sin(x)


LESSON = lesson(
    goals=["角を一般角・弧度法に拡張し、単位円を用いて三角関数を定義して、値・符号・周期を説明できる。",
           "$y=a\\sin b(\\theta-p)+q$ などのグラフを、基本のグラフの拡大・縮小と平行移動としてかける。",
           "加法定理を単位円と2点間の距離から証明し、2倍角・半角の公式と三角関数の合成を導いて、方程式・不等式・最大最小に活用できる。"],
    duration=250,
    readiness=["$0^\\circ\\leqq\\theta\\leqq180^\\circ$ の三角比を単位円で求められ、$\\sin^2\\theta+\\cos^2\\theta=1$ を使える。",
               "2点間の距離の公式と余弦定理を使える。", "二次関数の最大・最小を平方完成で求められる。"],
    flow=[("導入：回転を表す角", 15, "観覧車のゴンドラの高さを例に、360°を超える回転・逆向きの回転を表す必要性を示す"),
          ("一般角と弧度法", 35, "動径と一般角、1ラジアンの定義、扇形の弧の長さと面積"),
          ("三角関数の定義と性質", 40, "単位円上の点の座標として定義、符号・相互関係・θ+2nπ、−θ、θ+π などの公式"),
          ("三角関数のグラフ", 45, "y=sinθ, cosθ, tanθ のグラフと周期、拡大・縮小と平行移動"),
          ("方程式・不等式", 25, "単位円で解を読み取る。解の範囲に注意"),
          ("加法定理", 45, "cos(α−β) を2点間の距離で証明し、sin・tan の加法定理を導く"),
          ("2倍角・半角の公式と合成", 35, "加法定理から導出、合成で最大・最小を求める"),
          ("まとめと確認", 10, "公式の系統図を板書し、確認問題と問題プリントの課題を指示")],
    sections=[
        intro("in1", "回転を表す角と三角関数",
              "観覧車のゴンドラは、1周して元の位置に戻った後も回り続ける。このような回転の量を表すには、$360^\\circ$ を超える角や、逆向きの回転を表す負の角が必要になる。角をこのように拡張し、単位円上の点の座標として三角比を定義し直したものが三角関数である。三角関数は、くり返し現れる現象（波・振動・季節の変化など）を表す基本の関数である。",
              bullets=["角の大きさを「弧の長さ」で測る弧度法を使うと、扇形の公式や数学Ⅲの微分の公式が簡潔になる。",
                       "数学Ⅰの三角比（$0^\\circ\\leqq\\theta\\leqq180^\\circ$）は、三角関数の特別な場合として含まれる。"],
              points=[tp("観覧車の高さが時間とともに上下をくり返すグラフを示し、「同じ形がくり返す関数」が必要であることを実感させる。",
                         ask="ゴンドラが2周したとき、回転した角は何度か。", expect="$720^\\circ$", timing="導入の冒頭")]),
        definition("df1", "一般角と弧度法",
                   "平面上で、点 O を中心に半直線 OP（動径）を、始線 OX の位置から回転させる。時計の針と逆向きを正の向き、同じ向きを負の向きとし、回転の量を表す角を一般角という。また、半径 $r$ の円で長さ $r$ の弧に対する中心角を $1$ ラジアン（弧度）とする角の測り方を弧度法という。",
                   formula="$$180^\\circ=\\pi\\ (\\text{ラジアン}),\\qquad \\ell=r\\theta,\\qquad S=\\dfrac{1}{2}r^2\\theta=\\dfrac{1}{2}r\\ell$$",
                   conditions=["扇形の公式の $\\theta$ は弧度法で表した中心角（度数のまま代入しない）", "動径の位置が同じ角は $\\theta+2n\\pi$（$n$ は整数）と表せる",
                               "弧度法では単位「ラジアン」を省略して書くことが多い"],
                   points=[tp("1ラジアンは「半径と同じ長さの弧に対する中心角」であり、約 $57.3^\\circ$ であることを、ひもと円盤などで実際に確かめさせる。",
                              ask="半円の弧の長さは半径の何倍か。", expect="$\\pi$ 倍。だから $180^\\circ=\\pi$ ラジアン。"),
                           tp("扇形の面積 $S=\\dfrac12r^2\\theta$ は、円の面積 $\\pi r^2$ に $\\dfrac{\\theta}{2\\pi}$ をかけたものとして導けることを示す。",
                              caution="度数法の $\\theta$ をそのまま代入する誤りが多い。")]),
        definition("df2", "三角関数の定義",
                   "原点 O を中心とする半径 $r$ の円周上の点 P$(x,\\,y)$ について、動径 OP の表す一般角を $\\theta$ とするとき、次のように定める。",
                   formula="$$\\sin\\theta=\\dfrac{y}{r},\\qquad \\cos\\theta=\\dfrac{x}{r},\\qquad \\tan\\theta=\\dfrac{y}{x}\\ (x\\neq0)$$",
                   conditions=["単位円（$r=1$）では P$(\\cos\\theta,\\,\\sin\\theta)$、$\\tan\\theta$ は直線 OP の傾き",
                               "$\\theta=\\dfrac{\\pi}{2}+n\\pi$（$n$ は整数）では $\\tan\\theta$ は定義されない",
                               "$-1\\leqq\\sin\\theta\\leqq1,\\ -1\\leqq\\cos\\theta\\leqq1$ で、$\\tan\\theta$ はすべての実数値をとる"],
                   bullets=["$\\sin(\\theta+2n\\pi)=\\sin\\theta,\\ \\cos(\\theta+2n\\pi)=\\cos\\theta,\\ \\tan(\\theta+n\\pi)=\\tan\\theta$",
                            "$\\sin(-\\theta)=-\\sin\\theta,\\ \\cos(-\\theta)=\\cos\\theta,\\ \\tan(-\\theta)=-\\tan\\theta$",
                            "$\\sin\\left(\\theta+\\dfrac{\\pi}{2}\\right)=\\cos\\theta,\\ \\cos\\left(\\theta+\\dfrac{\\pi}{2}\\right)=-\\sin\\theta$"],
                   figure=figure("単位円と点P(cosθ, sinθ)", plane((-1.4, 1.4), (-1.4, 1.4), unit=60, grid=False, ticks=False,
                                                                curves=[(lambda x: (1 - x * x) ** 0.5 if abs(x) <= 1 else float("nan"), ""),
                                                                        (lambda x: -((1 - x * x) ** 0.5) if abs(x) <= 1 else float("nan"), "")],
                                                                points=[(-0.866, -0.5, "P(cosθ, sinθ)")], segments=[((0, 0), (-0.866, -0.5)), ((-0.866, 0), (-0.866, -0.5))])),
                   points=[tp("各象限での $\\sin,\\ \\cos,\\ \\tan$ の符号を、点 P の座標の符号と傾きから判断させ、表にまとめさせる。",
                              ask="第3象限の角では、$\\tan\\theta$ の符号はどうなるか。", expect="$x<0,\\ y<0$ なので傾きは正。$\\tan\\theta>0$。")]),
        theorem("th1", "加法定理",
                "$$\\begin{aligned}\\sin(\\alpha\\pm\\beta)&=\\sin\\alpha\\cos\\beta\\pm\\cos\\alpha\\sin\\beta\\\\ \\cos(\\alpha\\pm\\beta)&=\\cos\\alpha\\cos\\beta\\mp\\sin\\alpha\\sin\\beta\\\\ \\tan(\\alpha\\pm\\beta)&=\\dfrac{\\tan\\alpha\\pm\\tan\\beta}{1\\mp\\tan\\alpha\\tan\\beta}\\end{aligned}$$",
                ["複号同順", "$\\tan$ の式は、$\\tan\\alpha,\\ \\tan\\beta,\\ \\tan(\\alpha\\pm\\beta)$ が定義される場合に成り立つ",
                 "$\\cos$ の式だけ、左辺の符号と右辺の符号が逆になる"],
                proof=["単位円上に P$(\\cos\\alpha,\\,\\sin\\alpha)$、Q$(\\cos\\beta,\\,\\sin\\beta)$ をとる。",
                       "2点間の距離の公式より $\\mathrm{PQ}^2=(\\cos\\alpha-\\cos\\beta)^2+(\\sin\\alpha-\\sin\\beta)^2=2-2(\\cos\\alpha\\cos\\beta+\\sin\\alpha\\sin\\beta)$。",
                       "一方、$\\triangle\\mathrm{OPQ}$ で $\\angle\\mathrm{POQ}$ に対応する回転角は $\\alpha-\\beta$ なので、余弦定理（または O を中心に $-\\beta$ だけ回転して Q を $(1,\\,0)$ に移す考え）により $\\mathrm{PQ}^2=2-2\\cos(\\alpha-\\beta)$。",
                       "2式を比べて $\\cos(\\alpha-\\beta)=\\cos\\alpha\\cos\\beta+\\sin\\alpha\\sin\\beta$。",
                       "$\\beta$ を $-\\beta$ に置きかえると $\\cos(\\alpha+\\beta)=\\cos\\alpha\\cos\\beta-\\sin\\alpha\\sin\\beta$。",
                       "$\\sin(\\alpha+\\beta)=\\cos\\left(\\dfrac{\\pi}{2}-(\\alpha+\\beta)\\right)=\\cos\\left(\\left(\\dfrac{\\pi}{2}-\\alpha\\right)-\\beta\\right)=\\sin\\alpha\\cos\\beta+\\cos\\alpha\\sin\\beta$。",
                       "$\\tan(\\alpha+\\beta)=\\dfrac{\\sin(\\alpha+\\beta)}{\\cos(\\alpha+\\beta)}$ の分母・分子を $\\cos\\alpha\\cos\\beta$ で割ると $\\tan$ の式が得られる。"],
                points=[tp("証明の出発点は $\\cos(\\alpha-\\beta)$ ただ1つで、残りはすべて置きかえで導けることを系統図で示す。",
                           ask="$\\cos(\\alpha+\\beta)$ の式は、$\\cos(\\alpha-\\beta)$ の式から何をすれば得られるか。", expect="$\\beta$ を $-\\beta$ に置きかえる。", timing="加法定理の証明の直後"),
                        tp("$\\sin(\\alpha+\\beta)=\\sin\\alpha+\\sin\\beta$ が成り立たないことを、$\\alpha=\\beta=\\dfrac{\\pi}{2}$ などの反例で確認させる。",
                           caution="「かっこを分配する」感覚で誤る生徒が多い。")]),
        derivation("dv1", "2倍角・半角の公式",
                   ["加法定理で $\\beta=\\alpha$ とすると $\\sin2\\alpha=2\\sin\\alpha\\cos\\alpha$、$\\cos2\\alpha=\\cos^2\\alpha-\\sin^2\\alpha$。",
                    "$\\sin^2\\alpha+\\cos^2\\alpha=1$ を使うと $\\cos2\\alpha=2\\cos^2\\alpha-1=1-2\\sin^2\\alpha$。",
                    "$\\tan2\\alpha=\\dfrac{2\\tan\\alpha}{1-\\tan^2\\alpha}$。",
                    "$\\cos2\\alpha=1-2\\sin^2\\alpha$ で $\\alpha$ を $\\dfrac{\\alpha}{2}$ に置きかえて整理すると $\\sin^2\\dfrac{\\alpha}{2}=\\dfrac{1-\\cos\\alpha}{2}$。同様に $\\cos^2\\dfrac{\\alpha}{2}=\\dfrac{1+\\cos\\alpha}{2}$。"],
                   body="2倍角・半角の公式は、どれも加法定理と $\\sin^2\\alpha+\\cos^2\\alpha=1$ から数行で導ける。暗記に頼らず、導き方とセットで身につける。",
                   points=[tp("$\\cos2\\alpha$ の3つの形を、「$\\sin$ だけで表したい」「$\\cos$ だけで表したい」という目的に応じて使い分けることを例で示す。")]),
        theorem("th2", "三角関数の合成",
                "$$a\\sin\\theta+b\\cos\\theta=\\sqrt{a^2+b^2}\\,\\sin(\\theta+\\alpha)\\qquad\\left(\\cos\\alpha=\\dfrac{a}{\\sqrt{a^2+b^2}},\\ \\sin\\alpha=\\dfrac{b}{\\sqrt{a^2+b^2}}\\right)$$",
                ["$(a,\\,b)\\neq(0,\\,0)$", "$\\alpha$ は点 $(a,\\,b)$ を表す動径の角（$\\sin\\theta$ の係数が $x$ 座標、$\\cos\\theta$ の係数が $y$ 座標）"],
                proof=["$r=\\sqrt{a^2+b^2}$ とし、座標平面上に点 $(a,\\,b)$ をとると、$a=r\\cos\\alpha,\\ b=r\\sin\\alpha$ となる角 $\\alpha$ がある。",
                       "$a\\sin\\theta+b\\cos\\theta=r(\\sin\\theta\\cos\\alpha+\\cos\\theta\\sin\\alpha)$。",
                       "加法定理より $=r\\sin(\\theta+\\alpha)$。"],
                figure=figure("点(a, b)と合成の角α（例: a=1, b=√3）", plane((-0.5, 2), (-0.5, 2), unit=60, grid=False, ticks=False,
                                                                       points=[(1, 1.732, "(1, √3)")], segments=[((0, 0), (1, 1.732)), ((1, 0), (1, 1.732))],
                                                                       labels=[(0.25, 0.15, "α")])),
                points=[tp("点 $(a,\\,b)$ を図にかかせ、$r$ と $\\alpha$ を図から読み取る手順を定着させる。",
                           caution="$\\cos\\alpha=\\dfrac{b}{r}$ と取り違える誤りが多い。$\\sin\\theta$ の係数が $x$ 座標（$\\cos\\alpha$ 側）。")]),
        example("ex1", "例題1　加法定理で値を求める",
                "$\\cos\\dfrac{\\pi}{12}$ の値を求めよ。",
                ["$\\dfrac{\\pi}{12}=\\dfrac{\\pi}{3}-\\dfrac{\\pi}{4}$ と分ける。",
                 "$\\cos\\left(\\dfrac{\\pi}{3}-\\dfrac{\\pi}{4}\\right)=\\cos\\dfrac{\\pi}{3}\\cos\\dfrac{\\pi}{4}+\\sin\\dfrac{\\pi}{3}\\sin\\dfrac{\\pi}{4}=\\dfrac12\\cdot\\dfrac{\\sqrt2}{2}+\\dfrac{\\sqrt3}{2}\\cdot\\dfrac{\\sqrt2}{2}$。",
                 "$=\\dfrac{\\sqrt6+\\sqrt2}{4}$。"],
                "$\\dfrac{\\sqrt{6}+\\sqrt{2}}{4}$", thinking="値を知っている角（$\\dfrac{\\pi}{6},\\ \\dfrac{\\pi}{4},\\ \\dfrac{\\pi}{3}$ など）の和・差で表す。",
                misconceptions=[("$\\cos(\\alpha-\\beta)=\\cos\\alpha\\cos\\beta-\\sin\\alpha\\sin\\beta$", "$\\cos$ の加法定理は符号が逆になる。差なら $+\\sin\\alpha\\sin\\beta$")],
                points=[tp("答えが約 $0.966$ で、$\\cos0=1$ に近いことを確かめさせ、概算による検算を習慣づける。")]),
        example("ex2", "例題2　合成と最大・最小",
                "$0\\leqq\\theta\\leqq\\pi$ のとき、$y=\\sqrt{3}\\sin\\theta+\\cos\\theta$ の最大値と最小値、およびそのときの $\\theta$ を求めよ。",
                ["点 $(\\sqrt3,\\,1)$ を考えると $r=2$、$\\alpha=\\dfrac{\\pi}{6}$。よって $y=2\\sin\\left(\\theta+\\dfrac{\\pi}{6}\\right)$。",
                 "$\\dfrac{\\pi}{6}\\leqq\\theta+\\dfrac{\\pi}{6}\\leqq\\dfrac{7}{6}\\pi$ なので、$-\\dfrac12\\leqq\\sin\\left(\\theta+\\dfrac{\\pi}{6}\\right)\\leqq1$。",
                 "最大値 $2$（$\\theta+\\dfrac{\\pi}{6}=\\dfrac{\\pi}{2}$ より $\\theta=\\dfrac{\\pi}{3}$）、最小値 $-1$（$\\theta+\\dfrac{\\pi}{6}=\\dfrac{7}{6}\\pi$ より $\\theta=\\pi$）。"],
                "最大値 $2$（$\\theta=\\dfrac{\\pi}{3}$）、最小値 $-1$（$\\theta=\\pi$）",
                thinking="$\\sin$ と $\\cos$ が混ざっていると最大・最小が分からない → 合成して $\\sin$ 1つにまとめ、角の範囲を単位円で読む。",
                figure=figure("y=2sin(θ+π/6) のグラフ（0≦θ≦π）", plane((-0.5, 3.5), (-2.5, 2.5), unit=36, xl="θ",
                                                                    curves=[(lambda x: 2 * math.sin(x + math.pi / 6) if 0 <= x <= math.pi else float("nan"), "")],
                                                                    points=[(math.pi / 3, 2, "最大"), (math.pi, -1, "最小")])),
                misconceptions=[("$\\theta+\\dfrac{\\pi}{6}$ の範囲を考えず、最小値を $-2$ とする", "範囲 $\\dfrac{\\pi}{6}\\leqq\\theta+\\dfrac{\\pi}{6}\\leqq\\dfrac{7}{6}\\pi$ では $\\sin$ は $-\\dfrac12$ までしか下がらない")],
                points=[tp("置きかえた角 $\\theta+\\dfrac{\\pi}{6}$ の範囲を必ず書かせ、単位円上の弧として図示させる。", timing="例題2の板書中")]),
        example("ex3", "例題3　2倍角の公式を使う方程式",
                "$0\\leqq\\theta<2\\pi$ のとき、方程式 $\\cos2\\theta+\\sin\\theta=0$ を解け。",
                ["$\\cos2\\theta=1-2\\sin^2\\theta$ を代入すると $2\\sin^2\\theta-\\sin\\theta-1=0$。",
                 "$(2\\sin\\theta+1)(\\sin\\theta-1)=0$ より $\\sin\\theta=-\\dfrac12,\\ 1$。",
                 "$\\sin\\theta=1$ のとき $\\theta=\\dfrac{\\pi}{2}$、$\\sin\\theta=-\\dfrac12$ のとき $\\theta=\\dfrac{7}{6}\\pi,\\ \\dfrac{11}{6}\\pi$。"],
                "$\\theta=\\dfrac{\\pi}{2},\\ \\dfrac{7}{6}\\pi,\\ \\dfrac{11}{6}\\pi$",
                thinking="$\\sin\\theta$ と $\\cos2\\theta$ が混在 → $\\cos2\\theta$ を $\\sin\\theta$ だけで表す形（$1-2\\sin^2\\theta$）を選ぶ。"),
        board("bd1", "板書案",
              [("① 一般角・弧度法・定義", ["$180^\\circ=\\pi$", "$\\ell=r\\theta,\\ S=\\dfrac12r^2\\theta$", "単位円 P$(\\cos\\theta,\\sin\\theta)$", "$\\tan\\theta$＝OP の傾き",
                                          "周期：$\\sin,\\cos$ は $2\\pi$、$\\tan$ は $\\pi$"]),
               ("② 加法定理と系統図", ["$\\cos(\\alpha-\\beta)$（距離で証明）", "↓ $\\beta\\to-\\beta$：$\\cos(\\alpha+\\beta)$", "↓ 余角：$\\sin(\\alpha\\pm\\beta)$",
                                     "↓ $\\beta=\\alpha$：2倍角", "↓ $\\alpha\\to\\dfrac{\\alpha}{2}$：半角"]),
               ("③ 合成と活用", ["$a\\sin\\theta+b\\cos\\theta=r\\sin(\\theta+\\alpha)$", "点 $(a,b)$ で $r,\\ \\alpha$ を読む", "例 $\\sqrt3\\sin\\theta+\\cos\\theta=2\\sin(\\theta+\\frac{\\pi}{6})$",
                               "角の範囲を必ず書く", "最大・最小、方程式へ"])]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("方程式・不等式では、まず $\\theta$ の範囲を確認し、単位円上の点や弧として解を読み取らせる。", ask="$0\\leqq\\theta<2\\pi$ で $\\sin\\theta=\\dfrac12$ の解はいくつあるか。", expect="2つ"),
               tp("$\\sin2\\theta=k$ のように角が $2\\theta$ のときは、$2\\theta$ の範囲（$0\\leqq2\\theta<4\\pi$）で考えることを強調する。", caution="解の個数が半分になる誤りが非常に多い。",
                  timing="方程式の演習の後"),
               tp("グラフの平行移動は $y=\\sin2\\left(\\theta-\\dfrac{\\pi}{6}\\right)$ のように $\\theta$ の係数でくくってから読む。", caution="$y=\\sin\\left(2\\theta-\\dfrac{\\pi}{3}\\right)$ を $\\dfrac{\\pi}{3}$ 移動と読む誤り。"),
               tp("合成の結果は、$\\theta=0$ などを代入して元の式と値が一致するかで検算させる。")],
              misconceptions=[("扇形の面積を $S=\\dfrac12r^2\\theta$ に度数の $\\theta$ を代入して求める", "$\\theta$ は弧度法で代入する"),
                              ("$\\sin(\\alpha+\\beta)=\\sin\\alpha+\\sin\\beta$", "加法定理 $\\sin\\alpha\\cos\\beta+\\cos\\alpha\\sin\\beta$ を使う"),
                              ("$y=\\sin3\\theta$ の周期を $6\\pi$ とする", "周期は $\\dfrac{2\\pi}{3}$（$\\theta$ の係数で割る）")]),
        summary("sm1", "まとめ", ["弧度法では $180^\\circ=\\pi$。扇形は $\\ell=r\\theta,\\ S=\\dfrac12r^2\\theta$。",
                                   "三角関数は単位円上の点の座標で定義する。$\\sin,\\ \\cos$ の周期は $2\\pi$、$\\tan$ の周期は $\\pi$。",
                                   "加法定理は $\\cos(\\alpha-\\beta)$ を距離で証明し、置きかえで他の公式を導く。2倍角・半角・合成はすべて加法定理から得られる。",
                                   "方程式・最大最小では、置きかえた角の範囲を必ず確認する。"]),
        check("ck1", "確認問題", [("$\\dfrac{5}{4}\\pi$ を度数法で表すと？", "$225^\\circ$"), ("$\\sin\\dfrac{4}{3}\\pi$ の値は？", "$-\\dfrac{\\sqrt3}{2}$"),
                                  ("$\\sin\\dfrac{5}{12}\\pi$ の値は？", "$\\dfrac{\\sqrt6+\\sqrt2}{4}$"),
                                  ("$\\sin\\theta-\\cos\\theta$ を $r\\sin(\\theta+\\alpha)$ の形に表すと？", "$\\sqrt2\\sin\\left(\\theta-\\dfrac{\\pi}{4}\\right)$")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

DEGS = [15, 30, 45, 60, 75, 105, 120, 135, 150, 210, 225, 240, 270, 300, 315, 330, 360, 390, 405, 420, 450, 480, 540, 600, 720,
        -30, -45, -60, -90, -120, -135, -150, -210, -270, -300]


@gen("basic_check", 4, ["computation", "concept"])
def rad_convert(r):
    d = r.choice(DEGS)
    q = F(d, 180)
    if r.random() < 0.5:
        return sa(f"度数法で表された角 ${d}^\\circ$ を、弧度法に直しなさい。", f"${rad(q)}$",
                  f"$1^\\circ=\\dfrac{{\\pi}}{{180}}$ ラジアンなので、${d}^\\circ={d}\\times\\dfrac{{\\pi}}{{180}}={rad(q)}$。", d=1,
                  ap="$180^\\circ=\\pi$ ラジアンという対応をもとに、比例で換算する。",
                  steps=[f"${d}^\\circ={d}\\times\\dfrac{{\\pi}}{{180}}$。", f"約分して ${rad(q)}$。"],
                  alt=[f"${d}^\\circ$ を $30^\\circ$ や $45^\\circ$ の何倍かで考え、$\\dfrac{{\\pi}}{{6}}$ や $\\dfrac{{\\pi}}{{4}}$ の何倍かとして求めてもよい。"],
                  pc=[("$\\dfrac{\\pi}{180}$ をかける換算を正しく行っている", 1), ("約分して正しく答えている", 1)],
                  pit=["$\\dfrac{180}{\\pi}$ をかけてしまう（換算の向きの取り違え）。"], chk=(f"{d}*pi/180", rpy(q), None, "intermediate"))
    return sa(f"弧度法で表された角 ${rad(q)}$ を、度数法に直しなさい。", f"${d}^\\circ$",
              f"$\\pi$ ラジアン $=180^\\circ$ なので、$\\pi$ を $180^\\circ$ に置きかえる。", d=1,
              ap="$\\pi=180^\\circ$ を代入する。",
              steps=[f"${rad(q)}$ の $\\pi$ を $180^\\circ$ に置きかえる。", f"${q.numerator}\\times180^\\circ\\div{q.denominator}={d}^\\circ$。"],
              alt=[f"$1$ ラジアン $=\\dfrac{{180^\\circ}}{{\\pi}}$ をかけて ${rad(q)}\\times\\dfrac{{180^\\circ}}{{\\pi}}={d}^\\circ$ としてもよい。"],
              pc=[("$\\pi=180^\\circ$ の置きかえができている", 1), ("値が正しい", 1)],
              pit=["$\\pi\\fallingdotseq3.14$ を代入して小数で答えてしまう。"], chk=(f"{rpy(q)}*180/pi", str(d), None, "intermediate"))


VAL_ANGLES = [F(n, d) for d in (6, 4, 3, 2) for n in range(-2 * d, 4 * d + 1) if F(n, d).denominator == d]


@gen("basic_check", 5, ["computation", "condition_check"])
def trig_value(r):
    while True:
        q = r.choice(VAL_ANGLES)
        fn = r.choice(["sin", "cos", "tan"])
        if not (fn == "tan" and q.denominator == 2):
            break
    v = val(fn, q)
    q0 = q - 2 * math.floor(q / 2)
    quad_note = "" if q0 == q else f"${rad(q)}={rad(q0)}{'+' if q > q0 else '-'}{rad(abs(q - q0))}$ より、動径は ${rad(q0)}$ と同じ位置にある。"
    return sa(f"単位円を利用して、$\\{fn}{arg(q)}$ の値を求めなさい。", f"${tex(v)}$",
              f"{quad_note}単位円上の点 $({tex(val('cos', q0))},\\,{tex(val('sin', q0))})$ から $\\{fn}{arg(q)}={tex(v)}$。", d=2,
              ap="動径の位置を $0\\leqq\\theta<2\\pi$ の角に直し、単位円上の点の座標（$\\cos$ が $x$、$\\sin$ が $y$、$\\tan$ は傾き）を読む。",
              steps=[quad_note or f"動径の表す角は ${rad(q0)}$。", f"単位円上の点は $({tex(val('cos', q0))},\\,{tex(val('sin', q0))})$。", f"$\\{fn}{arg(q)}={tex(v)}$。"],
              alt=["$\\sin(-\\theta)=-\\sin\\theta$、$\\cos(\\theta+\\pi)=-\\cos\\theta$ などの公式で、鋭角の三角関数に直してもよい。"],
              pc=[("動径の位置（同じ位置の角）を正しくとらえている", 1), ("符号を含めて値が正しい", 1)],
              pit=["象限による符号の判断を誤る。", "負の角を正の向きに回してしまう。"], chk=(f"{fn}({rpy(q)})", py(v), None, "intermediate"))


SECT_ANG = [F(1, 6), F(1, 4), F(1, 3), F(1, 2), F(2, 3), F(3, 4), F(5, 6), F(5, 4), F(4, 3), F(3, 2), F(5, 3), F(7, 6)]


@gen("basic_check", 3, ["computation"])
def sector(r):
    R = r.randint(2, 12)
    th = r.choice(SECT_ANG)
    ell, S = R * th, F(R * R, 2) * th
    return sa(f"半径 ${R}$、中心角 ${rad(th)}$ の扇形の弧の長さ $\\ell$ と面積 $S$ を求めなさい。", f"$\\ell={rad(ell)},\\ S={rad(S)}$",
              f"$\\ell=r\\theta={R}\\times{rad(th)}={rad(ell)}$、$S=\\dfrac12r^2\\theta={rad(S)}$。", d=1,
              ap="中心角が弧度法で与えられているので、公式 $\\ell=r\\theta,\\ S=\\dfrac12r^2\\theta$ にそのまま代入できる。",
              steps=[f"$\\ell={R}\\cdot{rad(th)}={rad(ell)}$。", f"$S=\\dfrac12\\cdot{R}^2\\cdot{rad(th)}={rad(S)}$。"],
              alt=[f"$S=\\dfrac12r\\ell=\\dfrac12\\cdot{R}\\cdot{rad(ell)}={rad(S)}$ でも求められ、検算になる。"],
              pc=[("弧の長さが正しい", 1), ("面積が正しい", 1)], pit=["$\\dfrac12$ を忘れる、または $r$ を2乗し忘れる。"],
              chk=(f"[{R}*{rpy(th)}, Rational(1,2)*{R}**2*{rpy(th)}]", f"[{rpy(ell)}, {rpy(S)}]", None, "intermediate"))


B_LIST = [F(2), F(3), F(4), F(1, 2), F(1, 3), F(3, 2)]


def barg(b):
    if b.denominator == 1:
        return f"{b.numerator}\\theta"
    if b.numerator == 1:
        return f"\\dfrac{{\\theta}}{{{b.denominator}}}"
    return f"\\dfrac{{{b.numerator}}}{{{b.denominator}}}\\theta"


@gen("basic_check", 4, ["concept", "condition_check"])
def period_mc(r):
    fn = r.choice(["sin", "cos", "tan"])
    b = r.choice(B_LIST)
    a = r.choice([1, 2, 3, -2, -1])
    base = F(1) if fn == "tan" else F(2)
    right = f"${rad(base / b)}$"
    cands = {}
    cands[f"${rad(base * b)}$"] = ("$\\theta$ の係数で割るべきところを、かけてしまっている。", "周期と係数の関係の逆転")
    other = F(2) if fn == "tan" else F(1)
    cands[f"${rad(other / b)}$"] = ((f"$\\tan$ の周期は $\\pi$ である。" if fn == "tan" else "$\\sin,\\ \\cos$ の周期は $2\\pi$ で、$\\pi$ ではない。") + "基本の周期を取り違えている。",
                                   "基本の周期の混同")
    cands[f"${rad(base)}$"] = ("$\\theta$ の係数による周期の変化を考えていない。", "グラフの横方向の拡大・縮小の見落とし")
    if abs(a) != 1:
        cands[f"${rad(base * abs(a) / b)}$"] = ("係数 " + f"${a}$" + " はグラフの縦方向の拡大（振幅）に関係し、周期には影響しない。", "振幅と周期の混同")
    cands.pop(right, None)
    wrongs = list(dict.fromkeys(cands))[:3]
    ac = "" if a == 1 else ("-" if a == -1 else str(a))
    f = f"y={ac}\\{fn}{barg(b)}"
    return mc(f"関数 ${f}$ の周期（正の周期のうち最小のもの）として正しいものを選びなさい。", [right] + wrongs,
              f"$y=\\{fn} k\\theta$ の周期は ${'\\pi' if fn == 'tan' else '2\\pi'}$ を $k$ で割ったもの。${rad(base)}\\div{tex(sp.Rational(b.numerator, b.denominator))}={rad(base / b)}$。", d=2,
              ap=f"$y=\\{fn}\\theta$ の周期は ${rad(base)}$。$\\theta$ の係数が $k$ なら、グラフは横に $\\dfrac{{1}}{{k}}$ 倍に縮むので周期も $\\dfrac{{1}}{{k}}$ 倍になる。",
              steps=[f"$y=\\{fn}\\theta$ の周期は ${rad(base)}$。", f"$\\theta$ の係数は ${tex(sp.Rational(b.numerator, b.denominator))}$ なので、周期は ${rad(base)}\\div{tex(sp.Rational(b.numerator, b.denominator))}={rad(base / b)}$。",
                     "係数 $" + str(a) + "$ は周期に影響しない。"],
              alt=[f"$\\theta$ を $\\theta+{rad(base / b)}$ に置きかえると、角が ${rad(base)}$ だけ増えて同じ値に戻ることを確かめる。"],
              pc=[("基本の周期を正しく用いている", 1), ("係数で割って周期を求めている", 1)],
              why={w: cands[w] for w in wrongs}, chk=(f"{rpy(base)}/Rational({b.numerator},{b.denominator})", rpy(base / b), None, "intermediate"))


ADD_DEC = {15: (45, 30, -1), 75: (45, 30, 1), 105: (60, 45, 1), 165: (120, 45, 1), 195: (150, 45, 1), 255: (210, 45, 1), 285: (240, 45, 1), 345: (300, 45, 1)}


def dv(fn, d):
    return sp.nsimplify(FN[fn](sp.pi * d / 180))


@gen("basic_check", 4, ["computation"])
def addition_value(r):
    t = r.choice(list(ADD_DEC))
    fn = r.choice(["sin", "cos", "tan"])
    a, b, s = ADD_DEC[t]
    v = sp.nsimplify(sp.radsimp(dv(fn, t)))
    pm = "+" if s > 0 else "-"
    mp = "-" if s > 0 else "+"
    if fn == "sin":
        form = f"\\sin{a}^\\circ\\cos{b}^\\circ{pm}\\cos{a}^\\circ\\sin{b}^\\circ"
        sub = f"{tex(dv('sin', a))}\\cdot{tex(dv('cos', b))}{pm}\\left({tex(dv('cos', a))}\\right)\\cdot{tex(dv('sin', b))}"
    elif fn == "cos":
        form = f"\\cos{a}^\\circ\\cos{b}^\\circ{mp}\\sin{a}^\\circ\\sin{b}^\\circ"
        sub = f"\\left({tex(dv('cos', a))}\\right)\\cdot{tex(dv('cos', b))}{mp}\\left({tex(dv('sin', a))}\\right)\\cdot{tex(dv('sin', b))}"
    else:
        form = f"\\dfrac{{\\tan{a}^\\circ{pm}\\tan{b}^\\circ}}{{1{mp}\\tan{a}^\\circ\\tan{b}^\\circ}}"
        sub = f"\\dfrac{{{tex(dv('tan', a))}{pm}\\left({tex(dv('tan', b))}\\right)}}{{1{mp}\\left({tex(dv('tan', a))}\\right)\\cdot{tex(dv('tan', b))}}}"
    return sa(f"加法定理を用いて、$\\{fn}{t}^\\circ$ の値を求めなさい。", f"${tex(v)}$",
              f"${t}^\\circ={a}^\\circ{pm}{b}^\\circ$ と分けて加法定理を使う。", d=2,
              ap="値を知っている角（$30^\\circ,\\ 45^\\circ,\\ 60^\\circ$ やその仲間）の和・差に分ける。",
              steps=[f"${t}^\\circ={a}^\\circ{pm}{b}^\\circ$。", f"$\\{fn}{t}^\\circ={form}$。", f"$={sub}$。", f"$={tex(v)}$。"],
              alt=[f"電卓（関数電卓）で $\\{fn}{t}^\\circ\\fallingdotseq{float(v):.4f}$ を確かめ、答えの概数と比べる。"],
              pc=[("角を適切な和・差に分けて加法定理を立てている", 1), ("値が正しい", 1)],
              pit=["$\\cos$ の加法定理の符号を逆にする。", "$\\sin(\\alpha+\\beta)=\\sin\\alpha+\\sin\\beta$ としてしまう。"],
              chk=(f"{fn}(deg({t}))", py(v), None, "intermediate"))


# ======================================================================
# B 標準演習
# ======================================================================

def _pick_triple(r):
    a, b, c = r.choice(TRIPLES)
    if r.random() < 0.5:
        a, b = b, a
    return a, b, c


@gen("standard_practice", 5, ["computation", "condition_check"])
def addition_given(r):
    a1, b1, c1 = _pick_triple(r)
    a2, b2, c2 = _pick_triple(r)
    obt = r.random() < 0.5
    sA = sp.Rational(a1, c1)
    cA = sp.Rational(-b1 if obt else b1, c1)
    rngA = "\\dfrac{\\pi}{2}<\\alpha<\\pi" if obt else "0<\\alpha<\\dfrac{\\pi}{2}"
    qb = r.choice([1, 2, 3, 4])
    rngB, ss, cs = QUAD[qb]
    rngB = rngB.replace("\\theta", "\\beta")
    cB = sp.Rational(cs * a2, c2)
    sB = sp.Rational(ss * b2, c2)
    kind = r.choice(["sin+", "sin-", "cos+", "cos-"])
    if kind == "sin+":
        lab, ans, form = "\\sin(\\alpha+\\beta)", sA * cB + cA * sB, "\\sin\\alpha\\cos\\beta+\\cos\\alpha\\sin\\beta"
        ex = f"({sA})*({cB})+({cA})*({sB})"
    elif kind == "sin-":
        lab, ans, form = "\\sin(\\alpha-\\beta)", sA * cB - cA * sB, "\\sin\\alpha\\cos\\beta-\\cos\\alpha\\sin\\beta"
        ex = f"({sA})*({cB})-({cA})*({sB})"
    elif kind == "cos+":
        lab, ans, form = "\\cos(\\alpha+\\beta)", cA * cB - sA * sB, "\\cos\\alpha\\cos\\beta-\\sin\\alpha\\sin\\beta"
        ex = f"({cA})*({cB})-({sA})*({sB})"
    else:
        lab, ans, form = "\\cos(\\alpha-\\beta)", cA * cB + sA * sB, "\\cos\\alpha\\cos\\beta+\\sin\\alpha\\sin\\beta"
        ex = f"({cA})*({cB})+({sA})*({sB})"
    return sa(f"${rngA},\\ {rngB}$ で、$\\sin\\alpha={tex(sA)},\\ \\cos\\beta={tex(cB)}$ のとき、${lab}$ の値を求めなさい。", f"${tex(ans)}$",
              f"$\\cos\\alpha={tex(cA)},\\ \\sin\\beta={tex(sB)}$ を求めてから加法定理に代入する。", d=3,
              ap="加法定理には $\\sin\\alpha,\\ \\cos\\alpha,\\ \\sin\\beta,\\ \\cos\\beta$ の4つが必要。足りない2つを相互関係で求め、符号は角の範囲で決める。",
              steps=[f"$\\cos^2\\alpha=1-\\sin^2\\alpha$、${rngA}$ より $\\cos\\alpha={tex(cA)}$。",
                     f"$\\sin^2\\beta=1-\\cos^2\\beta$、${rngB}$ より $\\sin\\beta={tex(sB)}$。",
                     f"${lab}={form}={tex(ans)}$。"],
              alt=["$\\alpha,\\ \\beta$ の動径を単位円上にかき、各点の座標の符号を図で確かめてから計算すると、符号の誤りを防げる。"],
              pc=[("$\\cos\\alpha$ を符号も含めて正しく求めている", 1), ("$\\sin\\beta$ を符号も含めて正しく求めている", 1), ("加法定理に代入して正しい値を得ている", 2)],
              pit=["平方根をとるときに、角の範囲による符号の判断を忘れる。", "$\\cos$ の加法定理の符号を取り違える。"],
              chk=(ex, py(ans), None, "intermediate"))


@gen("standard_practice", 4, ["computation", "condition_check"])
def double_angle(r):
    a, b, c = _pick_triple(r)
    qd = r.choice([1, 2, 3, 4])
    rng, ss, cs = QUAD[qd]
    s, co = sp.Rational(ss * a, c), sp.Rational(cs * b, c)
    given_sin = r.random() < 0.5
    gl = f"\\sin\\theta={tex(s)}" if given_sin else f"\\cos\\theta={tex(co)}"
    other = f"\\cos\\theta={tex(co)}" if given_sin else f"\\sin\\theta={tex(s)}"
    s2, c2 = 2 * s * co, co ** 2 - s ** 2
    return sa(f"${rng}$ で ${gl}$ のとき、$\\sin2\\theta$ と $\\cos2\\theta$ の値を求めなさい。", f"$\\sin2\\theta={tex(s2)},\\ \\cos2\\theta={tex(c2)}$",
              f"${other}$ を求め、2倍角の公式に代入する。", d=3,
              ap="$\\sin2\\theta=2\\sin\\theta\\cos\\theta$ には $\\sin\\theta,\\ \\cos\\theta$ の両方が必要。$\\cos2\\theta$ は与えられた方だけで表す形を選ぶと速い。",
              steps=[f"相互関係と $\\theta$ の範囲から ${other}$。", f"$\\sin2\\theta=2\\sin\\theta\\cos\\theta=2\\cdot\\left({tex(s)}\\right)\\cdot\\left({tex(co)}\\right)={tex(s2)}$。",
                     (f"$\\cos2\\theta=1-2\\sin^2\\theta={tex(c2)}$。" if given_sin else f"$\\cos2\\theta=2\\cos^2\\theta-1={tex(c2)}$。")],
              alt=["$\\cos2\\theta$ は $\\cos^2\\theta-\\sin^2\\theta$ でも計算でき、3つの形のどれで計算しても一致することが検算になる。",
                   "$\\sin^22\\theta+\\cos^22\\theta=1$ になっているかを確かめる。"],
              pc=[("もう一方の三角関数の値を符号も含めて求めている", 1), ("$\\sin2\\theta$ が正しい", 2), ("$\\cos2\\theta$ が正しい", 1)],
              pit=["$\\theta$ の範囲から符号を決めずに正の値をとる。", "$\\sin2\\theta=2\\sin\\theta$ としてしまう。"],
              chk=(f"[2*({s})*({co}), 1-2*({s})**2]", f"[{py(s2)}, {py(c2)}]", None, "intermediate"))


S3 = sp.sqrt(3)
BASES = [(1, S3), (S3, 1), (1, 1), (1, -1), (-1, 1), (-1, -1), (S3, -1), (-S3, 1), (1, -S3), (-1, S3), (-1, -S3), (-S3, -1), (0, 1), (1, 0)]
BASES = [x for x in BASES if 0 not in x]


@gen("standard_practice", 4, ["computation", "concept"])
def synthesis(r):
    a0, b0 = r.choice(BASES)
    k = r.choice([1, 2, 3])
    a, b = sp.nsimplify(k * a0), sp.nsimplify(k * b0)
    R = sp.sqrt(a * a + b * b)
    al = angle_of(a, b)
    return sa(f"次の式を $r\\sin(\\theta+\\alpha)$ の形に変形しなさい。ただし $r>0,\\ -\\pi<\\alpha\\leqq\\pi$ とする。\n$${lin(a, b)}$$", f"${rsin(R, al)}$",
              f"点 $({tex(a)},\\,{tex(b)})$ をとると、原点からの距離は ${tex(R)}$、動径の角は ${rad(al)}$。", d=3,
              ap="$\\sin\\theta$ の係数を $x$ 座標、$\\cos\\theta$ の係数を $y$ 座標とする点をとり、その点までの距離 $r$ と動径の角 $\\alpha$ を読む。",
              steps=[f"$r=\\sqrt{{({tex(a)})^2+({tex(b)})^2}}={tex(R)}$。", f"$\\cos\\alpha={tex(a / R)},\\ \\sin\\alpha={tex(b / R)}$ より $\\alpha={rad(al)}$。",
                     f"よって ${lin(a, b)}={rsin(R, al)}$。"],
              alt=[f"結果を加法定理で展開し、元の式 ${lin(a, b)}$ に戻ることを確かめる。", "$\\theta=0$ を代入すると左辺は $" + tex(b) + "$、右辺は $r\\sin\\alpha$ で一致する。"],
              pc=[("$r$ を正しく求めている", 1), ("$\\cos\\alpha,\\ \\sin\\alpha$ を正しく対応させている", 2), ("$\\alpha$ を範囲内で正しく答えている", 1)],
              pit=["$\\cos\\alpha$ と $\\sin\\alpha$ の対応を逆にする。", "$\\alpha$ を第1象限の角だけで考え、符号を無視する。"],
              chk=(f"simplify({py(R)}*sin(theta+{rpy(al)})-({py(a)})*sin(theta)-({py(b)})*cos(theta))", "0", None, "intermediate"))


EQS = [("sin", "2\\sin\\theta-1=0", sp.Rational(1, 2)), ("sin", "2\\sin\\theta+1=0", -sp.Rational(1, 2)), ("sin", "2\\sin\\theta-\\sqrt{3}=0", S3 / 2),
       ("sin", "2\\sin\\theta+\\sqrt{3}=0", -S3 / 2), ("sin", "\\sqrt{2}\\sin\\theta-1=0", sp.sqrt(2) / 2), ("sin", "\\sqrt{2}\\sin\\theta+1=0", -sp.sqrt(2) / 2),
       ("cos", "2\\cos\\theta-1=0", sp.Rational(1, 2)), ("cos", "2\\cos\\theta+1=0", -sp.Rational(1, 2)), ("cos", "2\\cos\\theta-\\sqrt{3}=0", S3 / 2),
       ("cos", "2\\cos\\theta+\\sqrt{3}=0", -S3 / 2), ("cos", "\\sqrt{2}\\cos\\theta+1=0", -sp.sqrt(2) / 2), ("cos", "\\sqrt{2}\\cos\\theta-1=0", sp.sqrt(2) / 2),
       ("tan", "\\tan\\theta+1=0", -1), ("tan", "\\sqrt{3}\\tan\\theta-1=0", S3 / 3), ("tan", "\\tan\\theta+\\sqrt{3}=0", -S3), ("tan", "\\sqrt{3}\\tan\\theta+1=0", -S3 / 3),
       ("tan", "\\tan\\theta-\\sqrt{3}=0", S3), ("tan", "\\tan\\theta-1=0", 1)]
DOMS = [(F(0), F(2), True, False), (F(-1), F(1), False, True)]


@gen("standard_practice", 4, ["computation", "condition_check"])
def trig_equation(r):
    fn, eq, v = r.choice(EQS)
    lo, hi, lc, hc = r.choice(DOMS)
    sols = grid_solutions(fn, v, 1, lo, hi, lc, hc)
    where = {"sin": f"直線 $y={tex(v)}$ と単位円の交点", "cos": f"直線 $x={tex(v)}$ と単位円の交点", "tan": f"原点を通る傾き ${tex(v)}$ の直線と単位円の交点"}[fn]
    return sa(f"${dom(lo, hi, lc, hc)}$ のとき、方程式 ${eq}$ を解きなさい。", f"$\\theta={thetas(sols)}$",
              f"$\\{fn}\\theta={tex(v)}$。{where}を考える。", d=3,
              ap=f"まず $\\{fn}\\theta$ について解き、単位円上で条件を満たす点を探す。範囲 ${dom(lo, hi, lc, hc)}$ に入る角だけを答える。",
              steps=[f"$\\{fn}\\theta={tex(v)}$。", f"{where}は{len(sols) if fn != 'tan' else 2}個。", f"範囲内の角は $\\theta={thetas(sols)}$。"],
              alt=[f"$y=\\{fn}\\theta$ のグラフと直線 $y={tex(v)}$ の交点の $\\theta$ 座標として読み取ってもよい。"],
              pc=[(f"$\\{fn}\\theta$ の値を正しく求めている", 1), ("単位円などで解の候補を正しくとらえている", 1), ("範囲内の解をすべて答えている", 2)],
              pit=["解を1つしか答えない。", "範囲が $-\\pi<\\theta\\leqq\\pi$ のときに、$0\\leqq\\theta<2\\pi$ の解をそのまま答える。"],
              chk=(f"[{', '.join(f'{fn}({rpy(s)})' for s in sols)}]", f"[{', '.join([py(v)] * len(sols))}]", None, "intermediate"))


SHIFT = [F(1, 6), F(1, 4), F(1, 3), F(1, 2), F(2, 3)]


@gen("standard_practice", 3, ["concept", "computation"])
def graph_props(r):
    fn = r.choice(["sin", "cos"])
    a = r.choice([1, 2, 3, -1, -2])
    b = r.choice([1, 2, 3])
    c = r.choice(SHIFT)
    d = r.choice([-1, 0, 1, 2])
    ac = "" if a == 1 else ("-" if a == -1 else str(a))
    inner = f"{b if b != 1 else ''}\\theta-{rad(c)}"
    dt = "" if d == 0 else (f"+{d}" if d > 0 else f"{d}")
    f = f"y={ac}\\{fn}\\left({inner}\\right){dt}"
    base = f"y={ac}\\{fn}{b if b != 1 else ''}\\theta"
    per, sh = F(2, b), c / b
    M, m = abs(a) + d, -abs(a) + d
    mv = f"$\\theta$ 軸方向に ${rad(sh)}$" + ("" if d == 0 else f"、$y$ 軸方向に ${d}$")
    fact = f"y={ac}\\{fn}{b if b != 1 else ''}\\left(\\theta-{rad(sh)}\\right){dt}" if b != 1 else f
    return sa(f"関数 ${f}$ の周期、最大値、最小値を求めなさい。また、このグラフは ${base}$ のグラフをどのように平行移動したものか答えなさい。",
              f"周期 ${rad(per)}$、最大値 ${M}$、最小値 ${m}$。${base}$ のグラフを{mv}だけ平行移動したもの",
              f"${fact}$ と変形すると、移動量が読み取れる。", d=3,
              ap="$\\theta$ の係数でくくって $y=a\\" + fn + " b(\\theta-p)+q$ の形にする。周期は $\\dfrac{2\\pi}{b}$、最大・最小は $\\pm|a|+q$。",
              steps=[f"${f}$ を ${fact}$ と変形する。", f"周期は $\\dfrac{{2\\pi}}{{{b}}}={rad(per)}$。", f"$-1\\leqq\\{fn}(\\cdots)\\leqq1$ より最大値 ${M}$、最小値 ${m}$。",
                     f"${base}$ のグラフを{mv}だけ平行移動したもの。"],
              alt=[f"$\\theta={rad(sh)}$ を代入すると、かっこの中が $0$ になる。基本のグラフで $\\theta=0$ の点がここに移ったと考えて移動量を確かめる。"],
              pc=[("周期が正しい", 1), ("最大値・最小値が正しい", 1), ("平行移動の量（$\\theta$ の係数でくくった値）が正しい", 2)],
              pit=[f"$\\theta$ 軸方向の移動量を ${rad(c)}$ と答える（係数 ${b}$ でくくっていない）。" if b != 1 else "最大値を $|a|$ ではなく $a$ で計算し、負の係数で誤る。",
                   "$a<0$ のとき最大値と最小値を取り違える。"],
              chk=(f"[2*pi/{b}, Abs({a})+({d}), -Abs({a})+({d}), {rpy(c)}/{b}]", f"[{rpy(per)}, {M}, {m}, {rpy(sh)}]", None, "intermediate"))


# ======================================================================
# C 思考力・記述応用
# ======================================================================

MM_DOMS = [(F(0), F(1)), (F(0), F(1, 2)), (F(-1, 2), F(1, 2)), (F(1, 2), F(3, 2))]


def _extreme(L, U, target):
    """[L,U]（π 単位）で sin が target（1 か -1）をとる u を探す。"""
    base = F(1, 2) if target == 1 else F(3, 2)
    out = []
    for k in range(-3, 4):
        u = base + 2 * k
        if L <= u <= U:
            out.append(u)
    return out


@gen("thinking_writing", 3, ["written_reasoning", "multiple_solutions", "condition_check"])
def synth_maxmin(r):
    a0, b0 = r.choice(BASES)
    k = r.choice([1, 2])
    a, b = sp.nsimplify(k * a0), sp.nsimplify(k * b0)
    R = sp.sqrt(a * a + b * b)
    al = angle_of(a, b)
    lo, hi = r.choice(MM_DOMS)
    L, U = lo + al, hi + al
    res = {}
    for tgt, name in ((1, "max"), (-1, "min")):
        us = _extreme(L, U, tgt)
        if us:
            res[name] = (R * tgt, [u - al for u in us])
        else:
            vL, vU = val("sin", L), val("sin", U)
            better = (vL > vU) if tgt == 1 else (vL < vU)
            if vL == vU:
                res[name] = (sp.nsimplify(R * vL), [lo, hi])
            else:
                res[name] = (sp.nsimplify(R * (vL if better else vU)), [lo if better else hi])
    (Mv, Mt), (mv, mt) = res["max"], res["min"]
    ans = f"最大値 ${tex(Mv)}$（$\\theta={thetas(Mt)}$）、最小値 ${tex(mv)}$（$\\theta={thetas(mt)}$）"
    rng = f"{rad(lo)}\\leqq\\theta\\leqq{rad(hi)}"
    rng2 = f"{rad(L)}\\leqq\\theta{'+' if al > 0 else '-'}{rad(abs(al))}\\leqq{rad(U)}"
    return desc(f"関数 $y={lin(a, b)}\\ \\left({rng}\\right)$ について、最大値と最小値、およびそれらをとるときの $\\theta$ の値を求めなさい。",
                ans, f"$y={rsin(R, al)}$ と合成し、${rng2}$ の範囲で $\\sin$ の値の範囲を単位円で読み取る。",
                [("三角関数の合成を正しく行っている", 3), ("合成後の角の範囲を正しく求めている", 2), ("最大値・最小値と $\\theta$ を正しく求めている", 3)], d=4, p=8, lines=10,
                ap="$\\sin\\theta$ と $\\cos\\theta$ が混在したままでは値の範囲が分からない。合成して1つの $\\sin$ にまとめ、かっこの中の角の範囲を考える。",
                steps=[f"$y={rsin(R, al)}$。", f"${rng}$ より ${rng2}$。",
                       f"この範囲で $\\sin$ の最大は ${tex(Mv / R)}$、最小は ${tex(mv / R)}$（単位円で確認）。", f"よって{ans}。"],
                alt=[f"$y$ を $\\theta$ の関数としてグラフ（$y={rsin(R, al)}$ のグラフ）をかき、区間 ${rng}$ の部分の最高点・最低点を読む。",
                     "端点 $\\theta=" + rad(lo) + ",\\ " + rad(hi) + "$ での $y$ の値を元の式に代入して求め、答えと照合する。"],
                pc=[("合成", 3), ("角の範囲", 2), ("最大・最小と $\\theta$", 3)],
                pit=["角の範囲を考えずに最大値 $r$・最小値 $-r$ と答える。", "最大・最小をとる $\\theta$ を、かっこの中の角のまま答える。"],
                chk=(f"[{py(R)}*sin({rpy(Mt[0])}+{rpy(al)}), {py(R)}*sin({rpy(mt[0])}+{rpy(al)})]", f"[{py(Mv)}, {py(mv)}]", None, "intermediate"))


T_TH = {"sin": {F(1): [F(1, 2)], F(1, 2): [F(1, 6), F(5, 6)], F(-1, 2): [F(7, 6), F(11, 6)], F(-1): [F(3, 2)]},
        "cos": {F(1): [F(0)], F(1, 2): [F(1, 3), F(5, 3)], F(-1, 2): [F(2, 3), F(4, 3)], F(-1): [F(1)]}}


@gen("thinking_writing", 3, ["cross_unit", "written_reasoning"], rel=["HS-MATH1-U03"])
def quad_trig(r):
    t = r.choice(["sin", "cos"])
    o = "cos" if t == "sin" else "sin"
    p = r.choice([-4, -3, -2, -1, 1, 2, 3, 4])
    q = r.choice([-2, -1, 0, 1, 2])
    pt = "" if p == 1 else ("-" if p == -1 else str(p))
    ptxt = (f"+{pt}" if p > 0 else pt) + f"\\{t}\\theta"
    qt = "" if q == 0 else (f"+{q}" if q > 0 else f"{q}")
    f = f"y=\\{o}^2\\theta{ptxt}{qt}"

    def fval(x):
        return -x * x + p * x + 1 + q
    tv = F(p, 2) if abs(F(p, 2)) <= 1 else F(1 if p > 0 else -1)
    tm = F(-1 if p > 0 else 1)
    M, m = fval(tv), fval(tm)
    Mt, mt = T_TH[t][tv], T_TH[t][tm]
    ans = f"最大値 ${frac_t(M)}$（$\\theta={thetas(Mt)}$）、最小値 ${frac_t(m)}$（$\\theta={thetas(mt)}$）"
    g = poly(-1, p, 1 + q)
    vx = F(p, 2)
    return desc(f"$0\\leqq\\theta<2\\pi$ のとき、関数 ${f}$ の最大値と最小値、およびそれらをとるときの $\\theta$ の値を求めなさい。", ans,
                f"$\\{o}^2\\theta=1-\\{t}^2\\theta$ として $x=\\{t}\\theta\\ (-1\\leqq x\\leqq1)$ とおくと、$x$ の二次関数 $y={g}$ の最大・最小の問題になる。",
                [("$\\" + o + "^2\\theta=1-\\" + t + "^2\\theta$ で1種類の三角関数に直している", 2), ("置きかえた文字の範囲 $-1\\leqq x\\leqq1$ を示している", 2),
                 ("平方完成して最大・最小を正しく求めている", 2), ("対応する $\\theta$ をすべて求めている", 2)], d=4, p=8, lines=10,
                ap=f"$\\{o}^2\\theta$ を $\\{t}\\theta$ で表すと、$\\{t}\\theta$ だけの式（二次関数）になる。置きかえた文字には範囲がつくことに注意する（数学Ⅰの定義域つき最大・最小）。",
                steps=[f"$y=1-\\{t}^2\\theta{ptxt}{qt}$。$x=\\{t}\\theta$ とおくと $-1\\leqq x\\leqq1$。",
                       f"$y={g}=-\\left(x{'-' if vx > 0 else '+'}{frac_t(abs(vx))}\\right)^2+{frac_t(vx * vx + 1 + q)}$。",
                       f"軸 $x={frac_t(vx)}$ と範囲 $-1\\leqq x\\leqq1$ の位置関係から、最大は $x={frac_t(tv)}$ で ${frac_t(M)}$、最小は $x={frac_t(tm)}$ で ${frac_t(m)}$。",
                       f"$\\{t}\\theta={frac_t(tv)}$ より $\\theta={thetas(Mt)}$、$\\{t}\\theta={frac_t(tm)}$ より $\\theta={thetas(mt)}$。"],
                alt=["$x=-1,\\ 1$ と軸の位置での $y$ の値をすべて計算して比べても、最大・最小を確かめられる。"],
                pc=[("1種類への変形", 2), ("$x$ の範囲", 2), ("最大・最小", 2), ("$\\theta$", 2)],
                pit=["$x=\\" + t + "\\theta$ の範囲を考えず、頂点の値をそのまま最大値とする。", "$\\theta$ を1つしか答えない。"],
                chk=(f"[-({fpy(tv)})**2+({p})*({fpy(tv)})+{1 + q}, -({fpy(tm)})**2+({p})*({fpy(tm)})+{1 + q}]", f"[{fpy(M)}, {fpy(m)}]", None, "intermediate"))


def frac_t(v):
    v = F(v)
    if v.denominator == 1:
        return str(v.numerator)
    return f"{'-' if v < 0 else ''}\\dfrac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def fpy(v):
    v = F(v)
    return str(v.numerator) if v.denominator == 1 else f"Rational({v.numerator},{v.denominator})"


PROOFS = [
    ("$\\cos(\\alpha+\\beta)=\\cos\\alpha\\cos\\beta-\\sin\\alpha\\sin\\beta$ を既知として、$\\sin(\\alpha+\\beta)=\\sin\\alpha\\cos\\beta+\\cos\\alpha\\sin\\beta$ を証明しなさい。",
     "$\\sin(\\alpha+\\beta)=\\cos\\left(\\dfrac{\\pi}{2}-\\alpha-\\beta\\right)=\\cos\\left(\\left(\\dfrac{\\pi}{2}-\\alpha\\right)+(-\\beta)\\right)=\\cos\\left(\\dfrac{\\pi}{2}-\\alpha\\right)\\cos(-\\beta)-\\sin\\left(\\dfrac{\\pi}{2}-\\alpha\\right)\\sin(-\\beta)=\\sin\\alpha\\cos\\beta+\\cos\\alpha\\sin\\beta$。",
     "余角の公式 $\\sin x=\\cos\\left(\\dfrac{\\pi}{2}-x\\right)$ で $\\sin$ を $\\cos$ に直し、$\\cos$ の加法定理を使う。",
     ["$\\sin(\\alpha+\\beta)=\\cos\\left(\\dfrac{\\pi}{2}-(\\alpha+\\beta)\\right)$。", "$\\dfrac{\\pi}{2}-\\alpha$ と $-\\beta$ の和と見て $\\cos$ の加法定理を使う。",
      "$\\cos\\left(\\dfrac{\\pi}{2}-\\alpha\\right)=\\sin\\alpha,\\ \\sin\\left(\\dfrac{\\pi}{2}-\\alpha\\right)=\\cos\\alpha,\\ \\cos(-\\beta)=\\cos\\beta,\\ \\sin(-\\beta)=-\\sin\\beta$ で整理する。"],
     ["単位円上の点を $\\dfrac{\\pi}{2}$ 回転させる考え（$\\sin(\\theta+\\frac{\\pi}{2})=\\cos\\theta$）を使っても示せる。"],
     "simplify(sin(a+b)-(sin(a)*cos(b)+cos(a)*sin(b)))"),
    ("加法定理を用いて、$\\cos2\\alpha=2\\cos^2\\alpha-1=1-2\\sin^2\\alpha$ を証明しなさい。",
     "加法定理で $\\beta=\\alpha$ とすると $\\cos2\\alpha=\\cos^2\\alpha-\\sin^2\\alpha$。$\\sin^2\\alpha=1-\\cos^2\\alpha$ を代入すると $2\\cos^2\\alpha-1$、$\\cos^2\\alpha=1-\\sin^2\\alpha$ を代入すると $1-2\\sin^2\\alpha$。",
     "$\\cos(\\alpha+\\beta)$ の式で $\\beta=\\alpha$ とし、相互関係で一方の関数だけの式にする。",
     ["$\\cos2\\alpha=\\cos(\\alpha+\\alpha)=\\cos^2\\alpha-\\sin^2\\alpha$。", "$\\sin^2\\alpha=1-\\cos^2\\alpha$ を代入 → $2\\cos^2\\alpha-1$。", "$\\cos^2\\alpha=1-\\sin^2\\alpha$ を代入 → $1-2\\sin^2\\alpha$。"],
     ["$\\alpha=\\dfrac{\\pi}{3}$ などを代入して3つの式の値が一致することを確かめる（証明ではなく検算）。"],
     "simplify(cos(2*a)-(2*cos(a)**2-1))"),
    ("$\\cos2\\alpha=1-2\\sin^2\\alpha$ を用いて、半角の公式 $\\sin^2\\dfrac{\\alpha}{2}=\\dfrac{1-\\cos\\alpha}{2}$ を証明しなさい。",
     "$\\cos2x=1-2\\sin^2x$ に $x=\\dfrac{\\alpha}{2}$ を代入すると $\\cos\\alpha=1-2\\sin^2\\dfrac{\\alpha}{2}$。これを $\\sin^2\\dfrac{\\alpha}{2}$ について解くと $\\sin^2\\dfrac{\\alpha}{2}=\\dfrac{1-\\cos\\alpha}{2}$。",
     "2倍角の公式で、角を半分にして読みかえる。",
     ["$\\cos2x=1-2\\sin^2x$ で $x=\\dfrac{\\alpha}{2}$ とおく。", "$\\cos\\alpha=1-2\\sin^2\\dfrac{\\alpha}{2}$。", "$\\sin^2\\dfrac{\\alpha}{2}$ について解く。"],
     ["$\\alpha=\\dfrac{\\pi}{3}$ とすると左辺 $\\sin^2\\dfrac{\\pi}{6}=\\dfrac14$、右辺 $\\dfrac{1-\\frac12}{2}=\\dfrac14$ で一致する（検算）。"],
     "simplify(sin(a/2)**2-(1-cos(a))/2)"),
    ("$\\sin,\\ \\cos$ の加法定理を用いて、$\\tan(\\alpha+\\beta)=\\dfrac{\\tan\\alpha+\\tan\\beta}{1-\\tan\\alpha\\tan\\beta}$ を証明しなさい。ただし、各辺の $\\tan$ は定義されるものとする。",
     "$\\tan(\\alpha+\\beta)=\\dfrac{\\sin\\alpha\\cos\\beta+\\cos\\alpha\\sin\\beta}{\\cos\\alpha\\cos\\beta-\\sin\\alpha\\sin\\beta}$。$\\cos\\alpha\\cos\\beta\\neq0$ なので分母・分子をこれで割ると $\\dfrac{\\tan\\alpha+\\tan\\beta}{1-\\tan\\alpha\\tan\\beta}$。",
     "$\\tan=\\dfrac{\\sin}{\\cos}$ と加法定理を使い、分母・分子を $\\cos\\alpha\\cos\\beta$ で割る。",
     ["$\\tan(\\alpha+\\beta)=\\dfrac{\\sin(\\alpha+\\beta)}{\\cos(\\alpha+\\beta)}$。", "加法定理で展開する。", "$\\tan\\alpha,\\ \\tan\\beta$ が定義されるので $\\cos\\alpha\\cos\\beta\\neq0$。分母・分子をこれで割る。"],
     ["$\\alpha=\\beta=\\dfrac{\\pi}{8}$ などで両辺の値を電卓で比べ、式の形を確かめる（検算）。"],
     "simplify(tan(a+b)-(tan(a)+tan(b))/(1-tan(a)*tan(b)))"),
    ("$a,\\ b$ は $(a,\\,b)\\neq(0,\\,0)$ を満たす実数とする。$a\\sin\\theta+b\\cos\\theta=\\sqrt{a^2+b^2}\\sin(\\theta+\\alpha)$ を満たす $\\alpha$ が存在することを、加法定理を用いて証明しなさい。",
     "$r=\\sqrt{a^2+b^2}>0$ とする。点 $(a,\\,b)$ は原点を中心とする半径 $r$ の円周上にあるので、$a=r\\cos\\alpha,\\ b=r\\sin\\alpha$ となる角 $\\alpha$ がある。このとき $a\\sin\\theta+b\\cos\\theta=r(\\sin\\theta\\cos\\alpha+\\cos\\theta\\sin\\alpha)=r\\sin(\\theta+\\alpha)$。",
     "点 $(a,\\,b)$ を動径で表し、三角関数の定義から $a=r\\cos\\alpha,\\ b=r\\sin\\alpha$ とおく。",
     ["$r=\\sqrt{a^2+b^2}$ とおく。", "三角関数の定義より $a=r\\cos\\alpha,\\ b=r\\sin\\alpha$ となる $\\alpha$ が存在する。", "代入して加法定理を逆向きに使う。"],
     ["$\\sin\\theta+\\sqrt3\\cos\\theta=2\\sin\\left(\\theta+\\dfrac{\\pi}{3}\\right)$ のような具体例で、右辺を展開して確かめる。"],
     "simplify(2*sin(theta+pi/3)-(sin(theta)+sqrt(3)*cos(theta)))"),
    ("加法定理を用いて、$\\sin3\\alpha=3\\sin\\alpha-4\\sin^3\\alpha$ を証明しなさい。",
     "$\\sin3\\alpha=\\sin(2\\alpha+\\alpha)=\\sin2\\alpha\\cos\\alpha+\\cos2\\alpha\\sin\\alpha=2\\sin\\alpha\\cos^2\\alpha+(1-2\\sin^2\\alpha)\\sin\\alpha=2\\sin\\alpha(1-\\sin^2\\alpha)+\\sin\\alpha-2\\sin^3\\alpha=3\\sin\\alpha-4\\sin^3\\alpha$。",
     "$3\\alpha=2\\alpha+\\alpha$ と分けて加法定理・2倍角の公式を使い、$\\cos^2\\alpha=1-\\sin^2\\alpha$ で $\\sin$ だけの式にする。",
     ["$\\sin3\\alpha=\\sin(2\\alpha+\\alpha)$ と加法定理。", "2倍角の公式で $\\sin2\\alpha,\\ \\cos2\\alpha$ を展開（$\\cos2\\alpha=1-2\\sin^2\\alpha$ を選ぶ）。", "$\\cos^2\\alpha=1-\\sin^2\\alpha$ を代入して整理。"],
     ["$\\alpha=\\dfrac{\\pi}{6}$ を代入すると左辺 $\\sin\\dfrac{\\pi}{2}=1$、右辺 $\\dfrac32-\\dfrac12=1$ で一致する（検算）。"],
     "simplify(sin(3*a)-(3*sin(a)-4*sin(a)**3))"),
]


@gen("thinking_writing", 2, ["written_reasoning", "concept"])
def proof_item(r):
    stem, ans, ex, steps, alt, ck = r.choice(PROOFS)
    return desc(stem, ans, ex, [("方針（使う公式・置きかえ）が正しい", 3), ("式変形が正確で論理的につながっている", 3), ("結論を明記している", 2)],
                d=4, p=8, kind="proof", lines=8, ap=ex, steps=steps, alt=alt, pc=[("方針", 3), ("式変形", 3), ("結論", 2)],
                pit=["示すべき式を前提として使ってしまう（循環論法）。", "符号を含む公式（$\\cos(-\\beta)=\\cos\\beta,\\ \\sin(-\\beta)=-\\sin\\beta$ など）を確認せずに使う。"],
                chk=(ck, "0", None, "intermediate"))


INEQ = [("\\sin\\theta>\\dfrac{1}{2}", "\\dfrac{\\pi}{6}<\\theta<\\dfrac{5}{6}\\pi", "sin", "Rational(1,2)", [F(1, 6), F(5, 6)]),
        ("\\sin\\theta\\leqq\\dfrac{1}{2}", "0\\leqq\\theta\\leqq\\dfrac{\\pi}{6},\\ \\dfrac{5}{6}\\pi\\leqq\\theta<2\\pi", "sin", "Rational(1,2)", [F(1, 6), F(5, 6)]),
        ("2\\sin\\theta+\\sqrt{3}<0", "\\dfrac{4}{3}\\pi<\\theta<\\dfrac{5}{3}\\pi", "sin", "-sqrt(3)/2", [F(4, 3), F(5, 3)]),
        ("2\\sin\\theta+1\\geqq0", "0\\leqq\\theta\\leqq\\dfrac{7}{6}\\pi,\\ \\dfrac{11}{6}\\pi\\leqq\\theta<2\\pi", "sin", "-Rational(1,2)", [F(7, 6), F(11, 6)]),
        ("\\sqrt{2}\\sin\\theta+1>0", "0\\leqq\\theta<\\dfrac{5}{4}\\pi,\\ \\dfrac{7}{4}\\pi<\\theta<2\\pi", "sin", "-sqrt(2)/2", [F(5, 4), F(7, 4)]),
        ("\\sin\\theta\\geqq\\dfrac{\\sqrt{3}}{2}", "\\dfrac{\\pi}{3}\\leqq\\theta\\leqq\\dfrac{2}{3}\\pi", "sin", "sqrt(3)/2", [F(1, 3), F(2, 3)]),
        ("\\cos\\theta<\\dfrac{1}{2}", "\\dfrac{\\pi}{3}<\\theta<\\dfrac{5}{3}\\pi", "cos", "Rational(1,2)", [F(1, 3), F(5, 3)]),
        ("\\sqrt{2}\\cos\\theta-1\\geqq0", "0\\leqq\\theta\\leqq\\dfrac{\\pi}{4},\\ \\dfrac{7}{4}\\pi\\leqq\\theta<2\\pi", "cos", "sqrt(2)/2", [F(1, 4), F(7, 4)]),
        ("2\\cos\\theta+\\sqrt{3}>0", "0\\leqq\\theta<\\dfrac{5}{6}\\pi,\\ \\dfrac{7}{6}\\pi<\\theta<2\\pi", "cos", "-sqrt(3)/2", [F(5, 6), F(7, 6)]),
        ("2\\cos\\theta+1\\leqq0", "\\dfrac{2}{3}\\pi\\leqq\\theta\\leqq\\dfrac{4}{3}\\pi", "cos", "-Rational(1,2)", [F(2, 3), F(4, 3)]),
        ("\\cos\\theta>0", "0\\leqq\\theta<\\dfrac{\\pi}{2},\\ \\dfrac{3}{2}\\pi<\\theta<2\\pi", "cos", "0", [F(1, 2), F(3, 2)]),
        ("\\tan\\theta>1", "\\dfrac{\\pi}{4}<\\theta<\\dfrac{\\pi}{2},\\ \\dfrac{5}{4}\\pi<\\theta<\\dfrac{3}{2}\\pi", "tan", "1", [F(1, 4), F(5, 4)]),
        ("\\tan\\theta\\leqq\\sqrt{3}", "0\\leqq\\theta\\leqq\\dfrac{\\pi}{3},\\ \\dfrac{\\pi}{2}<\\theta\\leqq\\dfrac{4}{3}\\pi,\\ \\dfrac{3}{2}\\pi<\\theta<2\\pi", "tan", "sqrt(3)", [F(1, 3), F(4, 3)]),
        ("\\sqrt{3}\\tan\\theta+1<0", "\\dfrac{\\pi}{2}<\\theta<\\dfrac{5}{6}\\pi,\\ \\dfrac{3}{2}\\pi<\\theta<\\dfrac{11}{6}\\pi", "tan", "-sqrt(3)/3", [F(5, 6), F(11, 6)])]


@gen("thinking_writing", 2, ["condition_check", "written_reasoning"])
def trig_ineq(r):
    ineq, ans, fn, vpy, bds = r.choice(INEQ)
    tan_note = "$\\tan\\theta$ は $\\theta=\\dfrac{\\pi}{2},\\ \\dfrac{3}{2}\\pi$ で定義されないので、これらの角は除く。" if fn == "tan" else ""
    return desc(f"$0\\leqq\\theta<2\\pi$ のとき、不等式 ${ineq}$ を解きなさい。考え方も示すこと。", f"${ans}$",
                f"等号が成り立つ角 $\\theta={thetas(bds)}$ を求め、単位円（またはグラフ）で不等式を満たす部分を読み取る。" + tan_note,
                [("境界となる角を正しく求めている", 3), ("単位円・グラフを用いて満たす範囲を判断している", 3), ("範囲の端（等号・定義域）を正しく処理して答えている", 2)], d=4, p=8, lines=8,
                ap="まず等号の場合（方程式）を解いて境界の角を求め、単位円上で不等式を満たす弧を探す。$0\\leqq\\theta<2\\pi$ で弧が $0$ をまたぐときは2つの区間に分かれる。",
                steps=[f"境界：$\\{fn}\\theta$ の値が等号の値になる角は $\\theta={thetas(bds)}$。", "単位円（$\\tan$ は直線 $x=1$ 上の点）で、不等式を満たす点の集まりを図示する。" + tan_note,
                       f"答え：${ans}$。"],
                alt=[f"$y=\\{fn}\\theta$ のグラフをかき、直線との上下関係から $\\theta$ の範囲を読み取る。", "区間内の代表値（例えば $\\theta=\\pi$）を代入し、不等式を満たすかどうかで答えを確かめる。"],
                pc=[("境界", 3), ("範囲の判断", 3), ("端の処理", 2)],
                pit=["区間が $0$ をまたぐとき、$\\dfrac{11}{6}\\pi<\\theta<\\dfrac{\\pi}{6}$ のような誤った書き方をする。", "等号を含むかどうか（$<$ と $\\leqq$）を取り違える。"],
                chk=(f"[{fn}({rpy(bds[0])}), {fn}({rpy(bds[1])})]", f"[{vpy}, {vpy}]", None, "intermediate"))


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(stem, wrong, step, etype, tempt, fix, ans, expl, steps, ap, alt, pit, chk=None, d=3):
    return desc(f"{stem}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい答えを求めなさい。", ans, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい解答を途中式とともに示している", 3), ("最終的な答えが正しい", 1)], d=d, p=6, lines=6,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい途中式", 3), ("正しい答え", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix), chk=chk)


@gen("error_correction", 2, ["common_error", "condition_check"])
def err_sector(r):
    R = r.randint(2, 12)
    d = r.choice([30, 45, 60, 90, 120, 135, 150, 210, 240, 270])
    q = F(d, 180)
    if r.random() < 0.5:
        ell = R * q
        return err_item(f"半径 ${R}$、中心角 ${d}^\\circ$ の扇形の弧の長さを求めなさい。", f"$\\ell=r\\theta={R}\\times{d}={R * d}$",
                        "中心角 $\\theta$ に度数 $" + str(d) + "$ を代入した部分", "unit",
                        "公式 $\\ell=r\\theta$ の $\\theta$ が弧度法であることを意識せず、問題文の数値をそのまま代入している。",
                        f"${d}^\\circ={rad(q)}$ なので $\\ell={R}\\times{rad(q)}={rad(ell)}$", f"$\\ell={rad(ell)}$",
                        "$\\ell=r\\theta$ は弧度法で表した角について成り立つ公式である。",
                        [f"${d}^\\circ={rad(q)}$。", f"$\\ell={R}\\cdot{rad(q)}={rad(ell)}$。"],
                        "公式に代入する前に、角の単位が弧度法かどうかを確認する。",
                        [f"度数法のまま使うなら $\\ell=2\\pi r\\times\\dfrac{{{d}}}{{360}}$（円周の何分のいくつか）で計算でき、同じ結果になる。"],
                        ["弧の長さが円周 $" + rad(2 * R) + "$ より長くなっていないか確かめる。"],
                        chk=(f"{R}*{d}*pi/180", rpy(ell), None, "intermediate"), d=2)
    S = F(R * R, 2) * q
    return err_item(f"半径 ${R}$、中心角 ${d}^\\circ$ の扇形の面積を求めなさい。", f"$S=\\dfrac12r^2\\theta=\\dfrac12\\times{R}^2\\times{d}={F(R * R * d, 2)}$",
                    "中心角 $\\theta$ に度数 $" + str(d) + "$ を代入した部分", "unit",
                    "公式 $S=\\dfrac12r^2\\theta$ の $\\theta$ が弧度法であることを意識せず、度数をそのまま代入している。",
                    f"${d}^\\circ={rad(q)}$ なので $S=\\dfrac12\\times{R}^2\\times{rad(q)}={rad(S)}$", f"$S={rad(S)}$",
                    "扇形の面積の公式は、弧度法で表した中心角について成り立つ。",
                    [f"${d}^\\circ={rad(q)}$。", f"$S=\\dfrac12\\cdot{R * R}\\cdot{rad(q)}={rad(S)}$。"],
                    "公式に代入する前に、角の単位が弧度法かどうかを確認する。",
                    [f"度数法のまま使うなら $S=\\pi r^2\\times\\dfrac{{{d}}}{{360}}$ で計算でき、同じ結果になる。"],
                    ["円全体の面積 $" + rad(R * R) + "$ より大きくなっていないか確かめる。"],
                    chk=(f"Rational(1,2)*{R}**2*{d}*pi/180", rpy(S), None, "intermediate"), d=2)


@gen("error_correction", 3, ["common_error", "computation"])
def err_addition(r):
    t = r.choice([15, 75, 105, 165, 195, 255, 285, 345])
    a, b, s = ADD_DEC[t]
    pm = "+" if s > 0 else "-"
    fn = r.choice(["sin", "cos"])
    kind = r.choice(["split", "sign"])
    right = sp.nsimplify(sp.radsimp(dv(fn, t)))
    if kind == "split":
        wrong_v = sp.nsimplify(dv(fn, a) + s * dv(fn, b))
        wrong = f"$\\{fn}{t}^\\circ=\\{fn}({a}^\\circ{pm}{b}^\\circ)=\\{fn}{a}^\\circ{pm}\\{fn}{b}^\\circ={tex(wrong_v)}$"
        step, et = f"$\\{fn}({a}^\\circ{pm}{b}^\\circ)=\\{fn}{a}^\\circ{pm}\\{fn}{b}^\\circ$ と分けた部分", "formula"
        tempt = "$a(x+y)=ax+ay$ のような分配法則の感覚で、関数の記号もかっこの中に分配できると考えている。"
    else:
        if fn == "sin":
            wrong_v = sp.nsimplify(dv("sin", a) * dv("cos", b) - s * dv("cos", a) * dv("sin", b))
            mid = f"\\sin{a}^\\circ\\cos{b}^\\circ{'-' if s > 0 else '+'}\\cos{a}^\\circ\\sin{b}^\\circ"
        else:
            wrong_v = sp.nsimplify(dv("cos", a) * dv("cos", b) + s * dv("sin", a) * dv("sin", b))
            mid = f"\\cos{a}^\\circ\\cos{b}^\\circ{pm}\\sin{a}^\\circ\\sin{b}^\\circ"
        wrong = f"$\\{fn}{t}^\\circ=\\{fn}({a}^\\circ{pm}{b}^\\circ)={mid}={tex(sp.radsimp(wrong_v))}$"
        step, et = "加法定理の右辺の符号", "sign"
        tempt = ("$\\cos$ の加法定理は左辺と右辺で符号が逆になる（$\\cos(\\alpha+\\beta)$ は $-\\sin\\alpha\\sin\\beta$）が、$\\sin$ と同じ符号だと思い込んでいる。" if fn == "cos"
                 else "$\\cos$ の加法定理の「符号が逆になる」性質を $\\sin$ にも当てはめてしまっている。")
    form = (f"\\sin{a}^\\circ\\cos{b}^\\circ{pm}\\cos{a}^\\circ\\sin{b}^\\circ" if fn == "sin" else f"\\cos{a}^\\circ\\cos{b}^\\circ{'-' if s > 0 else '+'}\\sin{a}^\\circ\\sin{b}^\\circ")
    return err_item(f"$\\{fn}{t}^\\circ$ の値を求めなさい。", wrong, step, et, tempt,
                    f"$\\{fn}({a}^\\circ{pm}{b}^\\circ)={form}={tex(right)}$", f"${tex(right)}$",
                    f"加法定理 $\\{fn}(\\alpha{pm}\\beta)$ を正しく使う。",
                    [f"${t}^\\circ={a}^\\circ{pm}{b}^\\circ$。", f"$\\{fn}{t}^\\circ={form}$。", f"$={tex(right)}$。"],
                    "加法定理は「$\\sin$ は sin・cos・cos・sin で符号そのまま、$\\cos$ は cos・cos・sin・sin で符号が逆」と、形と符号をセットで確認する。",
                    [f"電卓で $\\{fn}{t}^\\circ\\fallingdotseq{float(right):.4f}$、生徒の答えは $\\fallingdotseq{float(wrong_v):.4f}$ となり、一致しないことで誤りに気づける。"],
                    ["$|\\sin|,\\ |\\cos|\\leqq1$ を超える答えになっていないか確かめる。"],
                    chk=(f"{fn}(deg({t}))", py(right), None, "intermediate"))


ER_V = [sp.Rational(1, 2), -sp.Rational(1, 2), S3 / 2, -S3 / 2, sp.sqrt(2) / 2, -sp.sqrt(2) / 2]


@gen("error_correction", 3, ["common_error", "condition_check"])
def err_range(r):
    fn = r.choice(["sin", "cos"])
    v = r.choice(ER_V)
    m = r.choice([2, 2, 3])
    base = grid_solutions(fn, v, 1)
    wrong_s = [x / m for x in base]
    right_s = grid_solutions(fn, v, m)
    return err_item(f"$0\\leqq\\theta<2\\pi$ のとき、方程式 $\\{fn}{m}\\theta={tex(v)}$ を解きなさい。",
                    f"${m}\\theta={thetas(base)}$ より $\\theta={thetas(wrong_s)}$",
                    f"${m}\\theta$ の範囲を $0\\leqq {m}\\theta<2\\pi$ のまま考えた部分", "condition",
                    f"$\\{fn} x={tex(v)}$ の解を $0\\leqq x<2\\pi$ で求める手順に慣れていて、$x={m}\\theta$ の範囲が ${m}$ 倍に広がることを見落としている。",
                    f"$0\\leqq{m}\\theta<{m * 2}\\pi$ で考えると $\\theta={thetas(right_s)}$", f"$\\theta={thetas(right_s)}$",
                    f"$\\theta$ の範囲が $0\\leqq\\theta<2\\pi$ なら、${m}\\theta$ の範囲は $0\\leqq{m}\\theta<{2 * m}\\pi$ で、単位円を{m}周する。",
                    [f"$x={m}\\theta$ とおくと $0\\leqq x<{2 * m}\\pi$。", f"$\\{fn} x={tex(v)}$ の解は1周につき2つずつ、計 ${2 * m}$ 個：$x={thetas([s * m for s in right_s])}$。",
                     f"${m}$ で割って $\\theta={thetas(right_s)}$。"],
                    "角を置きかえたら、置きかえた文字の範囲を最初に書く。",
                    [f"$y=\\{fn}{m}\\theta$ の周期は ${rad(F(2, m))}$ なので、$0\\leqq\\theta<2\\pi$ にはグラフが{m}周期分入り、解は ${2 * m}$ 個あると予想できる。"],
                    ["解の個数を周期から見積もってから解く。"],
                    chk=(f"[{', '.join(f'{fn}({m}*{rpy(s)})' for s in right_s)}]", f"[{', '.join([py(v)] * len(right_s))}]", None, "intermediate"))


@gen("error_correction", 2, ["common_error", "concept"])
def err_synth(r):
    while True:
        a0, b0 = r.choice(BASES)
        k = r.choice([1, 2, 3])
        a, b = sp.nsimplify(k * a0), sp.nsimplify(k * b0)
        al, wal = angle_of(a, b), angle_of(b, a)
        if al != wal:
            break
    R = sp.sqrt(a * a + b * b)
    return err_item(f"${lin(a, b)}$ を $r\\sin(\\theta+\\alpha)\\ (r>0,\\ -\\pi<\\alpha\\leqq\\pi)$ の形に表しなさい。",
                    f"$r={tex(R)}$。$\\cos\\alpha={tex(b / R)},\\ \\sin\\alpha={tex(a / R)}$ より $\\alpha={rad(wal)}$。よって ${rsin(R, wal)}$",
                    "$\\cos\\alpha,\\ \\sin\\alpha$ の対応を決めた部分", "formula",
                    "「$\\cos$ の係数は $\\cos\\alpha$ に対応する」と字面で結びつけてしまい、加法定理の展開と照合していない。",
                    f"$\\cos\\alpha=\\dfrac{{a}}{{r}}={tex(a / R)},\\ \\sin\\alpha=\\dfrac{{b}}{{r}}={tex(b / R)}$ より $\\alpha={rad(al)}$。${rsin(R, al)}$",
                    f"${rsin(R, al)}$",
                    "$r\\sin(\\theta+\\alpha)=r\\cos\\alpha\\sin\\theta+r\\sin\\alpha\\cos\\theta$ なので、$\\sin\\theta$ の係数が $r\\cos\\alpha$、$\\cos\\theta$ の係数が $r\\sin\\alpha$。",
                    [f"$r=\\sqrt{{({tex(a)})^2+({tex(b)})^2}}={tex(R)}$。", f"$\\cos\\alpha={tex(a / R)},\\ \\sin\\alpha={tex(b / R)}$。", f"$\\alpha={rad(al)}$ より ${rsin(R, al)}$。"],
                    "結果を加法定理で展開して元の式に戻るかを確かめる。",
                    [f"$\\theta=0$ を代入すると元の式は ${tex(b)}$。生徒の式では ${tex(sp.nsimplify(R * val('sin', wal)))}$、正しい式では ${tex(sp.nsimplify(R * val('sin', al)))}$ となり、誤りが確かめられる。"],
                    ["合成の結果は $\\theta=0$ を代入して検算する。"],
                    chk=(f"simplify({py(R)}*sin(theta+{rpy(al)})-({py(a)})*sin(theta)-({py(b)})*cos(theta))", "0", None, "intermediate"))


GENERATORS = [rad_convert, trig_value, sector, period_mc, addition_value,
              addition_given, double_angle, synthesis, trig_equation, graph_props,
              synth_maxmin, quad_trig, proof_item, trig_ineq,
              err_sector, err_addition, err_range, err_synth]
