"""単元パック：数学C ベクトル。"""
from fractions import Fraction
from math import gcd

import sympy as sp

from banks._common import desc, figure, mc, num, plane, sa, shape
from hs_pack_lib import (board, check, definition, derivation, example, figure_explain, fr_py, frac, gen, guide, intro,
                         lesson, nonzero, summary, theorem, tp)

UNIT_ID = "HS-MATHC-U01"


def V(*c):
    """成分表示 (x,\\,y) の LaTeX。"""
    return "(" + ",\\,".join(str(x) for x in c) + ")"


def coef(m, sym, first=False):
    """係数 m と文字 sym（LaTeX）をつないだ項。"""
    if m == 0:
        return ""
    mag = abs(m)
    body = ("" if mag == 1 else str(mag)) + sym
    if m < 0:
        return "-" + body
    return body if first else "+" + body


def lin2(m, n, a="\\vec{a}", b="\\vec{b}"):
    s = coef(m, a, True) + coef(n, b)
    return s or "\\vec{0}"


def fcoef(f, sym, first=False):
    """分数係数 f（Fraction）の項。"""
    if f == 0:
        return ""
    t = "" if abs(f) == 1 else frac(abs(f).numerator, abs(f).denominator)
    s = t + sym
    if f < 0:
        return "-" + s
    return s if first else "+" + s


def c1(k):
    """係数 1 を省いた表記。"""
    return "" if k == 1 else str(k)


def mul(k, v):
    return str(v) if k == 1 else f"{k}\\cdot{v}"


def tex(v):
    return sp.latex(sp.nsimplify(v))


def sqrt_tex(n):
    return sp.latex(sp.sqrt(n))


COS_TEX = {30: "\\dfrac{\\sqrt{3}}{2}", 45: "\\dfrac{\\sqrt{2}}{2}", 60: "\\dfrac{1}{2}", 90: "0",
           120: "-\\dfrac{1}{2}", 135: "-\\dfrac{\\sqrt{2}}{2}", 150: "-\\dfrac{\\sqrt{3}}{2}"}
VA, VB = "\\vec{a}", "\\vec{b}"
OA, OB, OX = "\\overrightarrow{\\mathrm{OA}}", "\\overrightarrow{\\mathrm{OB}}", "\\overrightarrow{\\mathrm{OX}}"


LESSON = lesson(
    goals=["ベクトルの和・差・実数倍を図と成分の両方で表し、大きさを計算できる。",
           "内積の定義と成分表示を余弦定理から導き、なす角・垂直条件・図形の量の計算に使える。",
           "位置ベクトルを使って内分点・外分点・交点を表し、図形の性質を式で示せる。空間ベクトルにも同じ考え方を広げられる。"],
    duration=100,
    readiness=["三平方の定理と余弦定理（数学Ⅰ）を使える。", "$\\cos\\theta$ の値から $0^\\circ\\leqq\\theta\\leqq180^\\circ$ の角を求められる。",
               "座標平面上の2点間の距離・内分点の座標（数学Ⅱ）を求められる。"],
    flow=[("導入：向きと大きさをもつ量", 10, "移動・力の例から有向線分とベクトルを導入し、和を平行四辺形でかく"),
          ("成分と演算", 20, "成分表示・和・実数倍・大きさを確認し、平行条件を式で表す"),
          ("内積", 25, "定義 → 余弦定理による成分表示の導出 → 例題1（なす角）"),
          ("位置ベクトル", 25, "内分点の公式を導き、例題2（2直線の交点）を全体で解く"),
          ("空間ベクトル", 15, "成分に z を加えるだけで同じ公式が使えることを例題3で確認"),
          ("まとめと確認", 5, "確認問題3問、問題プリントA の課題指示")],
    sections=[
        intro("in1", "向きと大きさをもつ量",
              "「東へ3 km、北へ1 km 進む」という移動や、物体を押す力は、大きさだけでなく向きも合わせて初めて決まる。このように向きと大きさをもつ量をベクトルという。ベクトルは矢印（有向線分）で表し、位置を問題にしない。つまり、平行移動して重なる矢印は同じベクトルとみなす。",
              bullets=["2つのベクトルの和 $\\vec{a}+\\vec{b}$ は、$\\vec{a}$ の終点に $\\vec{b}$ の始点をつないだ矢印（平行四辺形の対角線）で表される。",
                       "ベクトルを座標で表す（成分表示）と、図形の問題を計算で処理できるようになる。"],
              points=[tp("同じ向き・同じ長さで位置の違う矢印を3本かき、「すべて同じベクトル」であることを確認させる。", ask="この3本の矢印は同じベクトルか。", expect="向きも長さも同じなので同じベクトル。", timing="導入の冒頭"),
                      tp("和は「続けて移動したときの全体の移動」と説明すると、三角形の作図と平行四辺形の作図が同じであることが理解しやすい。")],
              figure=figure("ベクトルa=(3,1)、b=(1,2) と和 a+b=(4,3) を表す平行四辺形", plane((-1, 5), (-1, 4), unit=26, ticks=True,
                                                                                    segments=[((0, 0), (3, 1)), ((0, 0), (1, 2)), ((3, 1), (4, 3)), ((1, 2), (4, 3)), ((0, 0), (4, 3))],
                                                                                    points=[(3, 1, "a"), (1, 2, "b"), (4, 3, "a+b")]))),
        definition("df1", "ベクトルの成分と演算",
                   "座標平面で、原点 O を始点として $\\vec{a}=\\overrightarrow{\\mathrm{OA}}$ となる点 A の座標が $(a_1,\\,a_2)$ のとき、$\\vec{a}=(a_1,\\,a_2)$ と書き、$a_1,\\ a_2$ を $\\vec{a}$ の成分という。",
                   formula="$$\\vec{a}=(a_1,\\,a_2),\\ \\vec{b}=(b_1,\\,b_2)\\ \\Longrightarrow\\ \\vec{a}\\pm\\vec{b}=(a_1\\pm b_1,\\,a_2\\pm b_2),\\quad k\\vec{a}=(ka_1,\\,ka_2),\\quad |\\vec{a}|=\\sqrt{a_1^2+a_2^2}$$",
                   conditions=["2点 A$(x_1,\\,y_1)$、B$(x_2,\\,y_2)$ について $\\overrightarrow{\\mathrm{AB}}=(x_2-x_1,\\,y_2-y_1)$（終点 − 始点）。",
                               "$\\vec{a}\\neq\\vec{0},\\ \\vec{b}\\neq\\vec{0}$ のとき、$\\vec{a}\\parallel\\vec{b}\\iff\\vec{b}=k\\vec{a}$ となる実数 $k$ がある $\\iff a_1b_2-a_2b_1=0$。",
                               "空間では成分が3つになり、$\\vec{a}=(a_1,\\,a_2,\\,a_3)$、$|\\vec{a}|=\\sqrt{a_1^2+a_2^2+a_3^2}$ となる。演算の規則は平面と同じ。"],
                   points=[tp("$\\overrightarrow{\\mathrm{AB}}$ を「終点 − 始点」で求めることを、始点と終点を逆にした誤答と比べて確認させる。", caution="「始点 − 終点」で計算して向きが逆になる誤りが多い。"),
                           tp("平行条件 $a_1b_2-a_2b_1=0$ は「成分の比が等しい」$a_1:a_2=b_1:b_2$ を、分母が $0$ になる場合も含めて書き直したものだと説明する。")]),
        theorem("th1", "内積の定義と成分表示",
                "$$\\vec{a}\\cdot\\vec{b}=|\\vec{a}||\\vec{b}|\\cos\\theta=a_1b_1+a_2b_2$$",
                ["$\\vec{a}\\neq\\vec{0},\\ \\vec{b}\\neq\\vec{0}$、$\\theta$ は $\\vec{a}$ と $\\vec{b}$ のなす角（$0^\\circ\\leqq\\theta\\leqq180^\\circ$）。どちらかが $\\vec{0}$ のときは $\\vec{a}\\cdot\\vec{b}=0$ と定める。",
                 "$\\vec{a}\\perp\\vec{b}\\iff\\vec{a}\\cdot\\vec{b}=0$（$\\vec{a}\\neq\\vec{0},\\ \\vec{b}\\neq\\vec{0}$）",
                 "$|\\vec{a}|^2=\\vec{a}\\cdot\\vec{a}$。空間では $\\vec{a}\\cdot\\vec{b}=a_1b_1+a_2b_2+a_3b_3$。"],
                body="内積はベクトルではなく実数（スカラー）である。なす角は、2つのベクトルの始点をそろえたときにできる角で測る。",
                proof=["$\\overrightarrow{\\mathrm{OA}}=\\vec{a},\\ \\overrightarrow{\\mathrm{OB}}=\\vec{b}$ とすると、$\\overrightarrow{\\mathrm{AB}}=\\vec{b}-\\vec{a}$。",
                       "$\\triangle\\mathrm{OAB}$ に余弦定理を使うと $\\mathrm{AB}^2=\\mathrm{OA}^2+\\mathrm{OB}^2-2\\,\\mathrm{OA}\\cdot\\mathrm{OB}\\cos\\theta$。",
                       "これは $|\\vec{b}-\\vec{a}|^2=|\\vec{a}|^2+|\\vec{b}|^2-2\\vec{a}\\cdot\\vec{b}$ を意味する。",
                       "成分で書くと $(b_1-a_1)^2+(b_2-a_2)^2=a_1^2+a_2^2+b_1^2+b_2^2-2\\vec{a}\\cdot\\vec{b}$。",
                       "左辺を展開して整理すると $-2a_1b_1-2a_2b_2=-2\\vec{a}\\cdot\\vec{b}$、よって $\\vec{a}\\cdot\\vec{b}=a_1b_1+a_2b_2$。（O, A, B が一直線上にある場合も、同じ式が成り立つことが確かめられる。）"],
                points=[tp("余弦定理の式がそのまま内積の式に置きかわることを、2つの式を上下に並べて板書して見せる。", ask="余弦定理の $2bc\\cos A$ にあたるのは、ベクトルでは何か。", expect="$2\\vec{a}\\cdot\\vec{b}$"),
                        tp("$\\cos\\theta=\\dfrac{\\vec{a}\\cdot\\vec{b}}{|\\vec{a}||\\vec{b}|}$ の符号で、鋭角・直角・鈍角が判定できることを確認する。", caution="内積が負なのに鋭角と答える誤りが多い。")]),
        derivation("dv1", "内分点・外分点の位置ベクトル",
                   ["点 P が線分 AB を $m:n$ に内分するとき、$\\overrightarrow{\\mathrm{AP}}=\\dfrac{m}{m+n}\\overrightarrow{\\mathrm{AB}}$。",
                    "位置ベクトルで書くと $\\vec{p}-\\vec{a}=\\dfrac{m}{m+n}(\\vec{b}-\\vec{a})$。",
                    "$\\vec{a}$ について整理すると $\\vec{p}=\\left(1-\\dfrac{m}{m+n}\\right)\\vec{a}+\\dfrac{m}{m+n}\\vec{b}=\\dfrac{n\\vec{a}+m\\vec{b}}{m+n}$。",
                    "外分（$m\\neq n$）は、内分の式の $n$ を $-n$ におきかえて $\\vec{p}=\\dfrac{-n\\vec{a}+m\\vec{b}}{m-n}$。",
                    "特に中点は $\\dfrac{\\vec{a}+\\vec{b}}{2}$、$\\triangle\\mathrm{ABC}$ の重心は $\\dfrac{\\vec{a}+\\vec{b}+\\vec{c}}{3}$。"],
                   body="基準の点 O を決めると、点 P はベクトル $\\vec{p}=\\overrightarrow{\\mathrm{OP}}$ と1対1に対応する。これを P の位置ベクトルという。",
                   points=[tp("係数の「たすきがけ」（A の係数が $n$、B の係数が $m$）は、P が B に近いほど $\\vec{b}$ の係数が大きくなることで納得させる。", ask="$m:n=3:1$ のとき、P は A と B のどちらに近いか。", expect="B に近い"),
                           tp("係数の和が $1$ になっていることを、検算の習慣として身につけさせる。", timing="導出の直後")]),
        example("ex1", "例題1　成分からなす角を求める",
                "$\\vec{a}=(2,\\,1),\\ \\vec{b}=(1,\\,3)$ のなす角 $\\theta$ を求めよ。",
                ["$\\vec{a}\\cdot\\vec{b}=2\\cdot1+1\\cdot3=5$。", "$|\\vec{a}|=\\sqrt{5},\\ |\\vec{b}|=\\sqrt{10}$。",
                 "$\\cos\\theta=\\dfrac{5}{\\sqrt{5}\\sqrt{10}}=\\dfrac{5}{5\\sqrt{2}}=\\dfrac{1}{\\sqrt{2}}$。", "$0^\\circ\\leqq\\theta\\leqq180^\\circ$ より $\\theta=45^\\circ$。"],
                "$\\theta=45^\\circ$",
                thinking="内積を2通りに表した $|\\vec{a}||\\vec{b}|\\cos\\theta=a_1b_1+a_2b_2$ から $\\cos\\theta$ を求める。",
                points=[tp("答えの前に「$0^\\circ\\leqq\\theta\\leqq180^\\circ$ より」と範囲を書かせる。", caution="範囲を書かないと、$\\cos\\theta$ から角が1つに決まる理由が答案に残らない。")],
                misconceptions=[("$\\cos\\theta=\\dfrac{5}{\\sqrt{5}+\\sqrt{10}}$ とする", "分母は大きさの積 $|\\vec{a}||\\vec{b}|$")]),
        example("ex2", "例題2　2直線の交点の位置ベクトル",
                "$\\triangle\\mathrm{OAB}$ において、辺 OA を $2:1$ に内分する点を P、辺 OB の中点を Q とし、線分 AQ と BP の交点を X とする。$\\overrightarrow{\\mathrm{OA}}=\\vec{a},\\ \\overrightarrow{\\mathrm{OB}}=\\vec{b}$ として、$\\overrightarrow{\\mathrm{OX}}$ を $\\vec{a},\\ \\vec{b}$ で表せ。",
                ["X は AQ 上にあるので、$\\mathrm{AX}:\\mathrm{XQ}=s:(1-s)$ とおくと $\\overrightarrow{\\mathrm{OX}}=(1-s)\\vec{a}+\\dfrac{s}{2}\\vec{b}$。",
                 "X は BP 上にあるので、$\\mathrm{BX}:\\mathrm{XP}=u:(1-u)$ とおくと $\\overrightarrow{\\mathrm{OX}}=\\dfrac{2u}{3}\\vec{a}+(1-u)\\vec{b}$。",
                 "$\\vec{a},\\ \\vec{b}$ は $\\vec{0}$ でなく平行でもないので、係数を比較して $1-s=\\dfrac{2u}{3},\\ \\dfrac{s}{2}=1-u$。",
                 "これを解いて $s=\\dfrac{1}{2},\\ u=\\dfrac{3}{4}$。"],
                "$\\overrightarrow{\\mathrm{OX}}=\\dfrac{1}{2}\\vec{a}+\\dfrac{1}{4}\\vec{b}$",
                thinking="交点 X を「AQ 上の点」「BP 上の点」の2通りに表し、係数を比較する。",
                figure=figure("三角形OABと、OA上の点P、OBの中点Q、AQとBPの交点X",
                              shape({"O": (0, 0), "A": (6, 0), "B": (2, 4), "P": (4, 0), "Q": (1, 2), "X": (3.5, 1)},
                                    segments=[("O", "A"), ("O", "B"), ("A", "B"), ("A", "Q"), ("B", "P")], scale=26)),
                points=[tp("係数比較ができる根拠「$\\vec{a},\\ \\vec{b}$ は $\\vec{0}$ でなく平行でない（1次独立）」を必ず答案に書かせる。", ask="なぜ係数を比べてよいのか。", expect="$\\vec{a}$ と $\\vec{b}$ が平行でないから。"),
                        tp("メネラウスの定理で $\\mathrm{AX}:\\mathrm{XQ}$ を求める方法と比べさせると、図形の性質（数学A）との結びつきが見える。")]),
        example("ex3", "例題3　空間ベクトルと三角形",
                "空間の3点 A$(1,\\,0,\\,2)$、B$(2,\\,1,\\,0)$、C$(0,\\,2,\\,1)$ について、$\\angle\\mathrm{BAC}$ と $\\triangle\\mathrm{ABC}$ の面積を求めよ。",
                ["$\\overrightarrow{\\mathrm{AB}}=(1,\\,1,\\,-2)$、$\\overrightarrow{\\mathrm{AC}}=(-1,\\,2,\\,-1)$。",
                 "$\\overrightarrow{\\mathrm{AB}}\\cdot\\overrightarrow{\\mathrm{AC}}=-1+2+2=3$、$|\\overrightarrow{\\mathrm{AB}}|=|\\overrightarrow{\\mathrm{AC}}|=\\sqrt{6}$。",
                 "$\\cos\\angle\\mathrm{BAC}=\\dfrac{3}{6}=\\dfrac{1}{2}$ より $\\angle\\mathrm{BAC}=60^\\circ$。",
                 "面積 $S=\\dfrac{1}{2}\\sqrt{6}\\cdot\\sqrt{6}\\sin60^\\circ=\\dfrac{3\\sqrt{3}}{2}$。"],
                "$\\angle\\mathrm{BAC}=60^\\circ$、面積 $\\dfrac{3\\sqrt{3}}{2}$",
                thinking="平面と同じく、終点 − 始点で辺のベクトルをつくり、内積からなす角を求める。",
                points=[tp("面積公式 $S=\\dfrac{1}{2}\\sqrt{|\\vec{a}|^2|\\vec{b}|^2-(\\vec{a}\\cdot\\vec{b})^2}$ で $\\sqrt{36-9}$ と計算しても同じ値になることを確かめさせる。")]),
        board("bd1", "板書案",
              [("① 成分と演算", ["$\\overrightarrow{\\mathrm{AB}}=$ 終点 − 始点", "$|\\vec{a}|=\\sqrt{a_1^2+a_2^2}$", "平行：$a_1b_2-a_2b_1=0$"]),
               ("② 内積", ["$\\vec{a}\\cdot\\vec{b}=|\\vec{a}||\\vec{b}|\\cos\\theta=a_1b_1+a_2b_2$", "余弦定理から導く", "垂直 $\\iff\\vec{a}\\cdot\\vec{b}=0$", "例1：$\\cos\\theta=\\dfrac{1}{\\sqrt{2}}$、$\\theta=45^\\circ$"]),
               ("③ 位置ベクトル・空間", ["内分 $\\dfrac{n\\vec{a}+m\\vec{b}}{m+n}$", "外分 $\\dfrac{-n\\vec{a}+m\\vec{b}}{m-n}$", "交点：2通りに表して係数比較", "空間：成分が3つになるだけ"])],
              points=[tp("板書は3列に分け、②の導出では余弦定理と内積の式を上下にそろえて書く。③には例題2の図を添える。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("$|\\vec{a}+\\vec{b}|$ を求めるときは、まず2乗して内積で展開することを徹底させる。", caution="$|\\vec{a}+\\vec{b}|=|\\vec{a}|+|\\vec{b}|$ とする誤りが多い。"),
               tp("なす角は始点をそろえて測ることを、三角形の頂点の角と比べて確認させる。", ask="$\\triangle\\mathrm{ABC}$ で $\\overrightarrow{\\mathrm{AB}}$ と $\\overrightarrow{\\mathrm{BC}}$ のなす角は $\\angle\\mathrm{B}$ か。", expect="$180^\\circ-\\angle\\mathrm{B}$"),
               tp("平行条件と垂直条件を混同しないよう、「平行は成分のたすきがけの差が 0、垂直は内積が 0」と対で板書する。", timing="成分と内積の両方を学んだ後"),
               tp("交点の問題では、係数比較の前に「$\\vec{a},\\ \\vec{b}$ が1次独立」であることを書く習慣をつけさせる。"),
               tp("空間ベクトルでは新しい公式を覚えるのではなく、平面の公式に $z$ 成分を加えるだけだと確認し、負担感を減らす。")],
              misconceptions=[("$\\overrightarrow{\\mathrm{AB}}=\\vec{a}-\\vec{b}$ とする", "終点 − 始点なので $\\vec{b}-\\vec{a}$"),
                              ("内積が負でも $\\cos\\theta$ の絶対値から鋭角を答える", "$\\cos\\theta<0$ なら $\\theta$ は鈍角"),
                              ("外分点を $\\dfrac{n\\vec{a}+m\\vec{b}}{m+n}$ で計算する", "外分は $n$ を $-n$ にして $\\dfrac{-n\\vec{a}+m\\vec{b}}{m-n}$")]),
        summary("sm1", "まとめ",
                ["成分で計算：和・差・実数倍は成分ごと、大きさは $\\sqrt{\\ }$ の中に成分の2乗の和。",
                 "内積 $\\vec{a}\\cdot\\vec{b}=|\\vec{a}||\\vec{b}|\\cos\\theta=a_1b_1+a_2b_2$。垂直 $\\iff$ 内積 $0$。$|\\vec{a}+\\vec{b}|$ は2乗して展開。",
                 "位置ベクトル：内分 $\\dfrac{n\\vec{a}+m\\vec{b}}{m+n}$。交点は2通りに表して係数比較。空間でも同じ考え方が使える。"]),
        check("ck1", "確認問題",
              [("$\\vec{a}=(3,\\,-1),\\ \\vec{b}=(2,\\,6)$ の内積を求め、2つのベクトルの位置関係を答えよ。", "$\\vec{a}\\cdot\\vec{b}=6-6=0$ より垂直"),
               ("$|\\vec{a}|=2,\\ |\\vec{b}|=1,\\ \\vec{a}\\cdot\\vec{b}=1$ のとき $|\\vec{a}-\\vec{b}|$ を求めよ。", "$|\\vec{a}-\\vec{b}|^2=4-2+1=3$ より $\\sqrt{3}$"),
               ("2点 A, B の位置ベクトルを $\\vec{a},\\ \\vec{b}$ とするとき、線分 AB を $1:3$ に内分する点の位置ベクトルを求めよ。", "$\\dfrac{3\\vec{a}+\\vec{b}}{4}$")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

@gen("basic_check", 5, ["computation"])
def comp_linear(r):
    while True:
        a1, a2, b1, b2 = (r.randint(-5, 5) for _ in range(4))
        m, n = r.choice([2, 3, -1, -2, 1, 4]), r.choice([1, -1, 2, -3, 3, -2])
        X, Y = m * a1 + n * b1, m * a2 + n * b2
        if (a1, a2) != (0, 0) and (b1, b2) != (0, 0) and (X, Y) != (0, 0):
            break
    N = X * X + Y * Y
    e = lin2(m, n)
    return sa(f"2つのベクトル $\\vec{{a}}={V(a1, a2)},\\ \\vec{{b}}={V(b1, b2)}$ について、ベクトル ${e}$ の成分と大きさを求めなさい。",
              f"${e}={V(X, Y)}$、大きさ ${sqrt_tex(N)}$",
              f"成分ごとに計算して ${V(X, Y)}$。大きさは $\\sqrt{{({X})^2+({Y})^2}}={sqrt_tex(N)}$。", d=1, v=[f"({X},{Y}), {sqrt_tex(N)}"],
              ap="和・差・実数倍は成分ごとに計算できる。大きさは成分の2乗の和の正の平方根。",
              steps=[f"$x$ 成分：${m}\\cdot({a1})+({n})\\cdot({b1})={X}$。", f"$y$ 成分：${m}\\cdot({a2})+({n})\\cdot({b2})={Y}$。",
                     f"大きさ：$\\sqrt{{({X})^2+({Y})^2}}=\\sqrt{{{N}}}={sqrt_tex(N)}$。"],
              alt=[f"先に ${coef(m, VA, True)}={V(m * a1, m * a2)}$、${coef(n, VB, True)}={V(n * b1, n * b2)}$ を求めてから足しても同じ結果になる。"],
              pc=[("成分を正しく計算している", 1), ("大きさを正しく求めている", 1)],
              pit=["負の成分を2乗するときに符号を誤る（$(-3)^2=-9$ など）。", "大きさを $|X|+|Y|$ と計算してしまう。"],
              chk=(f"[{m}*({a1})+({n})*({b1}), {m}*({a2})+({n})*({b2}), sqrt(({X})**2+({Y})**2)]", f"[{X}, {Y}, sqrt({N})]", None, "intermediate"))


@gen("basic_check", 5, ["concept", "computation"])
def dot_angle(r):
    case = r.choice(["half", "half", "r3", "r2"])
    if case == "half":
        th = r.choice([60, 90, 120])
        while True:
            p, q = r.randint(2, 7), r.randint(2, 7)
            if (p * q) % 2 == 0:
                break
        A_tex, B_tex, A_py, B_py = str(p), str(q), str(p), str(q)
        dot = {60: p * q // 2, 90: 0, 120: -p * q // 2}[th]
    elif case == "r3":
        th = r.choice([30, 150])
        while True:
            p, q = r.randint(1, 6), r.randint(1, 5)
            if (p * q) % 2 == 0:
                break
        A_tex, B_tex, A_py, B_py = str(p), f"{'' if q == 1 else q}\\sqrt{{3}}", str(p), f"{q}*sqrt(3)"
        dot = (3 * p * q // 2) * (1 if th == 30 else -1)
    else:
        th = r.choice([45, 135])
        p, q = r.randint(1, 6), r.randint(1, 5)
        A_tex, B_tex, A_py, B_py = str(p), f"{'' if q == 1 else q}\\sqrt{{2}}", str(p), f"{q}*sqrt(2)"
        dot = p * q * (1 if th == 45 else -1)
    angles = [30, 45, 60, 90, 120, 135, 150]
    wrong = [180 - th] if th != 90 else []
    rest = [x for x in angles if x != th and x not in wrong]
    r.shuffle(rest)
    wrong += rest[: 3 - len(wrong)]
    ch = lambda d: f"$\\theta={d}^\\circ$"  # noqa: E731
    why = {}
    for w in wrong:
        if w == 180 - th:
            why[ch(w)] = ("内積の符号を見落としている。$\\cos\\theta$ の符号が逆になると、鋭角と鈍角が入れかわる。", "内積の符号と鋭角・鈍角の対応の誤り")
        else:
            why[ch(w)] = (f"$\\cos{w}^\\circ={COS_TEX[w]}$ であり、求めた $\\cos\\theta={COS_TEX[th]}$ と一致しない。", "三角比の値と角の対応の取り違え")
    return mc(f"ベクトル $\\vec{{a}},\\ \\vec{{b}}$ が $|\\vec{{a}}|={A_tex},\\ |\\vec{{b}}|={B_tex},\\ \\vec{{a}}\\cdot\\vec{{b}}={dot}$ を満たすとき、2つのベクトルのなす角 $\\theta$ として正しいものを選びなさい。ただし $0^\\circ\\leqq\\theta\\leqq180^\\circ$ とする。",
              [ch(th)] + [ch(w) for w in wrong],
              f"$\\cos\\theta=\\dfrac{{\\vec{{a}}\\cdot\\vec{{b}}}}{{|\\vec{{a}}||\\vec{{b}}|}}={COS_TEX[th]}$ より $\\theta={th}^\\circ$。", d=1,
              ap="内積の定義 $\\vec{a}\\cdot\\vec{b}=|\\vec{a}||\\vec{b}|\\cos\\theta$ を $\\cos\\theta$ について解く。",
              steps=[f"$|\\vec{{a}}||\\vec{{b}}|={tex(sp.sympify(A_py) * sp.sympify(B_py))}$。", f"$\\cos\\theta=\\dfrac{{{dot}}}{{{tex(sp.sympify(A_py) * sp.sympify(B_py))}}}={COS_TEX[th]}$。",
                     f"$0^\\circ\\leqq\\theta\\leqq180^\\circ$ より $\\theta={th}^\\circ$。"],
              alt=["内積の符号だけを先に見ると、正なら鋭角、$0$ なら直角、負なら鈍角と見当がつけられる。"],
              pc=[("$\\cos\\theta$ を正しく求めている", 1), ("角を正しく判断している", 1)],
              why=why, chk=(f"acos(({dot})/(({A_py})*({B_py})))*180/pi", str(th), None, "intermediate"))


@gen("basic_check", 5, ["condition_check", "computation"])
def perp_param(r):
    kind = r.choice(["perp", "para"])
    while True:
        b1, b2 = nonzero(r, -6, 6), nonzero(r, -6, 6)
        k = r.randint(-8, 8)
        known = nonzero(r, -6, 6)
        pos = r.choice([0, 1])
        # a = (known, k) または (k, known)
        A1, A2 = (known, k) if pos == 1 else (k, known)
        ok = (A1 * b1 + A2 * b2 == 0) if kind == "perp" else (A1 * b2 - A2 * b1 == 0)
        if ok and (A1, A2) != (0, 0):
            break
        # 条件を満たすように k を決め直す
        if kind == "perp":
            num_, den = (-known * b1, b2) if pos == 1 else (-known * b2, b1)
        else:
            num_, den = (known * b2, b1) if pos == 1 else (known * b1, b2)
        if num_ % den == 0 and abs(num_ // den) <= 12:
            k = num_ // den
            A1, A2 = (known, k) if pos == 1 else (k, known)
            break
    a_tex = V(known, "k") if pos == 1 else V("k", known)
    Ap1, Ap2 = (str(known), "k") if pos == 1 else ("k", str(known))
    word = "垂直" if kind == "perp" else "平行"
    if kind == "perp":
        expr = f"solve(({Ap1})*({b1})+({Ap2})*({b2}), k)[0]"
        eq = f"{Ap1}\\cdot({b1})+{Ap2}\\cdot({b2})=0"
        cond = "内積が $0$"
    else:
        expr = f"solve(({Ap1})*({b2})-({Ap2})*({b1}), k)[0]"
        eq = f"{Ap1}\\cdot({b2})-{Ap2}\\cdot({b1})=0"
        cond = "$a_1b_2-a_2b_1=0$"
    return num(f"$k$ を定数とする。$\\vec{{a}}={a_tex}$ と $\\vec{{b}}={V(b1, b2)}$ が{word}になるような $k$ の値を求めなさい。", str(k),
               f"{word}条件は{cond}。${eq}$ を解いて $k={k}$。", d=2,
               ap=("2つのベクトルが垂直 $\\iff$ 内積が $0$（どちらも $\\vec{0}$ でないとき）。" if kind == "perp"
                   else "2つのベクトルが平行 $\\iff\\vec{a}=t\\vec{b}$ となる実数 $t$ がある $\\iff a_1b_2-a_2b_1=0$。"),
               steps=[f"{word}条件：{cond}。", f"${eq}$。", f"これを解いて $k={k}$。",
                      f"このとき $\\vec{{a}}={V(A1, A2)}\\neq\\vec{{0}}$ であることを確認する。"],
               alt=([f"$k={k}$ を代入して内積 ${A1}\\cdot({b1})+({A2})\\cdot({b2})=0$ となることを確かめる。"] if kind == "perp"
                    else [f"$\\vec{{a}}=t\\vec{{b}}$ とおき、既知の成分から $t$ を求めてから $k$ を決めてもよい。$k={k}$ のとき $\\vec{{a}}={V(A1, A2)}$ は $\\vec{{b}}$ の実数倍になっている。"]),
               pc=[("条件式を正しく立てている", 1), ("$k$ の値を正しく求めている", 1)],
               pit=["垂直と平行の条件を取り違える（平行なのに内積を $0$ とおく）。", "成分の位置（$x$ 成分・$y$ 成分）を取り違えて式を立てる。"],
               chk=(expr, str(k)))


@gen("basic_check", 5, ["computation", "concept"])
def section_point(r):
    kind = r.choice(["in", "in", "out"])
    while True:
        x1, y1, x2, y2 = (r.randint(-6, 6) for _ in range(4))
        m, n = r.randint(1, 5), r.randint(1, 5)
        if x1 == x2 or y1 == y2 or gcd(m, n) != 1:
            continue
        if kind == "in":
            d = m + n
            X, Y = n * x1 + m * x2, n * y1 + m * y2
        else:
            if abs(m - n) < 2:
                continue
            d = m - n
            X, Y = -n * x1 + m * x2, -n * y1 + m * y2
        if X % d == 0 and Y % d == 0 and not (kind == "in" and m == n == 1 and r.random() < 0.5):
            X, Y = X // d, Y // d
            break
    word = "内分" if kind == "in" else "外分"
    form = "\\dfrac{n\\vec{a}+m\\vec{b}}{m+n}" if kind == "in" else "\\dfrac{-n\\vec{a}+m\\vec{b}}{m-n}"
    nn = n if kind == "in" else -n
    return sa(f"座標平面上の2点 A${V(x1, y1)}$、B${V(x2, y2)}$ に対して、線分 AB を ${m}:{n}$ に{word}する点 P の座標を、位置ベクトルを用いて求めなさい。",
              f"${V(X, Y)}$", f"$\\overrightarrow{{\\mathrm{{OP}}}}={form}$ に $m={m},\\ n={n}$ を代入する。", d=2, v=[f"({X},{Y})"],
              ap=f"{word}点の位置ベクトル ${form}$ を成分で計算する。係数は「遠い方の比」がかかる（たすきがけ）。",
              steps=[f"$\\overrightarrow{{\\mathrm{{OP}}}}=\\dfrac{{{nn}\\overrightarrow{{\\mathrm{{OA}}}}+{m}\\overrightarrow{{\\mathrm{{OB}}}}}}{{{d}}}$。",
                     f"$x$ 座標：$\\dfrac{{{nn}\\cdot({x1})+{m}\\cdot({x2})}}{{{d}}}={X}$。", f"$y$ 座標：$\\dfrac{{{nn}\\cdot({y1})+{m}\\cdot({y2})}}{{{d}}}={Y}$。"],
              alt=[f"$\\overrightarrow{{\\mathrm{{AP}}}}=\\dfrac{{{m}}}{{{d}}}\\overrightarrow{{\\mathrm{{AB}}}}$ として、A に $\\overrightarrow{{\\mathrm{{AP}}}}$ を加えて求めてもよい。"],
              pc=[("公式に正しく代入している", 1), ("座標を正しく求めている", 1)],
              pit=["A の係数に $m$、B の係数に $n$ をかけてしまう（たすきがけの逆）。"] + (["外分で $-n$ の符号を落とす。"] if kind == "out" else []),
              chk=(f"[({nn}*({x1})+{m}*({x2}))/({d}), ({nn}*({y1})+{m}*({y2}))/({d})]", f"[{X}, {Y}]", None, "intermediate"))


# ======================================================================
# B 標準演習
# ======================================================================

def _angle_pair(r):
    """なす角がきれいな値になるベクトルの組 (a, b, 角)。"""
    if r.random() < 0.55:
        while True:
            x, y = r.randint(-3, 3), r.randint(-3, 3)
            if (x, y) != (0, 0):
                break
        th = r.choice([45, 90, 135])
        k = r.choice([1, 1, 2, -1]) if th == 90 else r.choice([1, 2])
        b = {45: (x - y, x + y), 90: (-y, x), 135: (-x - y, x - y)}[th]
        return (x, y), tuple(k * c for c in b), th
    while True:
        u = [0, 0, 0]
        v = [0, 0, 0]
        for vec in (u, v):
            idx = r.sample([0, 1, 2], 2)
            for i in idx:
                vec[i] = r.choice([1, -1])
        dot = sum(a * b for a, b in zip(u, v))
        if dot in (-1, 0, 1):
            break
    th = {1: 60, 0: 90, -1: 120}[dot]
    s, t = r.choice([1, 2, 3]), r.choice([1, 2])
    return tuple(s * c for c in u), tuple(t * c for c in v), th


@gen("standard_practice", 5, ["computation"])
def angle_components(r):
    a, b, th = _angle_pair(r)
    dot = sum(x * y for x, y in zip(a, b))
    na, nb = sum(x * x for x in a), sum(x * x for x in b)
    cos = sp.nsimplify(dot / sp.sqrt(na * nb))
    space = len(a) == 3
    return num(f"{'空間の' if space else ''}2つのベクトル $\\vec{{a}}={V(*a)},\\ \\vec{{b}}={V(*b)}$ のなす角 $\\theta\\ (0^\\circ\\leqq\\theta\\leqq180^\\circ)$ を求めなさい。", str(th),
               f"$\\vec{{a}}\\cdot\\vec{{b}}={dot}$、$|\\vec{{a}}|={sqrt_tex(na)}$、$|\\vec{{b}}|={sqrt_tex(nb)}$ より $\\cos\\theta={sp.latex(cos)}$、$\\theta={th}^\\circ$。", d=3,
               disp=f"$\\theta={th}^\\circ$",
               ap="成分から内積と大きさを計算し、$\\cos\\theta=\\dfrac{\\vec{a}\\cdot\\vec{b}}{|\\vec{a}||\\vec{b}|}$ を求める。",
               steps=[f"$\\vec{{a}}\\cdot\\vec{{b}}={'+'.join(f'({x})({y})' for x, y in zip(a, b))}={dot}$。",
                      f"$|\\vec{{a}}|=\\sqrt{{{na}}}$、$|\\vec{{b}}|=\\sqrt{{{nb}}}$。", f"$\\cos\\theta=\\dfrac{{{dot}}}{{\\sqrt{{{na}}}\\sqrt{{{nb}}}}}={sp.latex(cos)}$。",
                      f"$0^\\circ\\leqq\\theta\\leqq180^\\circ$ より $\\theta={th}^\\circ$。"],
               alt=(["内積が $0$ になった時点で、$\\vec{a}\\perp\\vec{b}$ すなわち $\\theta=90^\\circ$ と分かる。"] if th == 90
                    else ["$\\vec{a},\\ \\vec{b}$ を始点をそろえて図にかくと、角が鋭角か鈍角かの見当がつき、答えの検算になる。" if not space
                          else "成分を $\\dfrac{1}{s}$ 倍などして簡単にしてから計算しても、なす角は変わらない（正の実数倍は向きを変えない）。"]),
               pc=[("内積を正しく計算している", 1), ("大きさを正しく計算している", 1), ("$\\cos\\theta$ から角を正しく求めている", 2)],
               pit=["$\\cos\\theta$ が負なのに鋭角を答える。", "大きさの積を $\\sqrt{" + f"{na}" + "}+\\sqrt{" + f"{nb}" + "}$ と和にしてしまう。"],
               chk=(f"acos(({dot})/sqrt({na}*{nb}))*180/pi", str(th)))


@gen("standard_practice", 4, ["computation", "concept"])
def magnitude_expand(r):
    while True:
        p, q = r.randint(1, 5), r.randint(1, 5)
        d = r.randint(-p * q + 1, p * q - 1)
        m, n = r.choice([1, 2, 3, -1, -2]), r.choice([1, -1, 2, -2, 3, -3])
        val = m * m * p * p + 2 * m * n * d + n * n * q * q
        if val > 0 and not (abs(m) == abs(n) == 1 and r.random() < 0.4):
            break
    e = lin2(m, n)
    return sa(f"$|\\vec{{a}}|={p},\\ |\\vec{{b}}|={q},\\ \\vec{{a}}\\cdot\\vec{{b}}={d}$ のとき、$|{e}|$ の値を求めなさい。", f"${sqrt_tex(val)}$",
              f"$|{e}|^2={c1(m * m)}|\\vec{{a}}|^2{'+' if 2 * m * n >= 0 else '-'}{abs(2 * m * n)}\\vec{{a}}\\cdot\\vec{{b}}+{c1(n * n)}|\\vec{{b}}|^2={val}$。", d=3,
              v=[sqrt_tex(val)],
              ap="大きさの式は直接展開できないので、2乗して内積の計算にもちこむ。$|\\vec{x}|^2=\\vec{x}\\cdot\\vec{x}$ を使う。",
              steps=[f"$|{e}|^2=({e})\\cdot({e})$。", f"$={c1(m * m)}|\\vec{{a}}|^2{'+' if 2 * m * n >= 0 else '-'}{abs(2 * m * n)}\\vec{{a}}\\cdot\\vec{{b}}+{c1(n * n)}|\\vec{{b}}|^2$。",
                     f"$={mul(m * m, p * p)}{'+' if 2 * m * n * d >= 0 else '-'}{abs(2 * m * n * d)}+{mul(n * n, q * q)}={val}$。", f"$|{e}|\\geqq0$ より $|{e}|={sqrt_tex(val)}$。"],
              alt=["$\\vec{a},\\ \\vec{b}$ を始点をそろえてかき、余弦定理で $|" + e + "|$ を辺とする三角形の辺の長さとして求めることもできる（$\\cos\\theta=\\dfrac{" + str(d) + "}{" + str(p * q) + "}$）。"],
              pc=[("2乗して展開する方針を立てている", 1), ("内積を用いて正しく展開・計算している", 2), ("正の平方根をとって答えている", 1)],
              pit=["$|\\vec{a}+\\vec{b}|^2=|\\vec{a}|^2+|\\vec{b}|^2$ として $2\\vec{a}\\cdot\\vec{b}$ の項を落とす。", "最後に平方根をとり忘れて2乗の値を答える。"],
              chk=(f"sqrt(({m})**2*({p})**2+2*({m})*({n})*({d})+({n})**2*({q})**2)", f"sqrt({val})", None, "intermediate"))


@gen("standard_practice", 4, ["computation", "multiple_solutions"])
def triangle_area(r):
    while True:
        P = [(r.randint(-4, 5), r.randint(-4, 5)) for _ in range(3)]
        (x1, y1), (x2, y2), (x3, y3) = P
        u1, u2, v1, v2 = x2 - x1, y2 - y1, x3 - x1, y3 - y1
        det = u1 * v2 - u2 * v1
        if det != 0:
            break
    S = Fraction(abs(det), 2)
    S_ans = str(S.numerator) if S.denominator == 1 else f"{S.numerator}/{S.denominator}"
    uu, vv, uv = u1 * u1 + u2 * u2, v1 * v1 + v2 * v2, u1 * v1 + u2 * v2
    return num(f"3点 A${V(x1, y1)}$、B${V(x2, y2)}$、C${V(x3, y3)}$ を頂点とする $\\triangle\\mathrm{{ABC}}$ の面積を、ベクトルを用いて求めなさい。", S_ans,
               f"$\\overrightarrow{{\\mathrm{{AB}}}}={V(u1, u2)},\\ \\overrightarrow{{\\mathrm{{AC}}}}={V(v1, v2)}$ より $S=\\dfrac{{1}}{{2}}|({u1})({v2})-({u2})({v1})|={frac(S.numerator, S.denominator)}$。", d=3,
               disp=f"${frac(S.numerator, S.denominator)}$",
               ap="1つの頂点から出る2辺をベクトルで表し、面積公式 $S=\\dfrac{1}{2}|a_1b_2-a_2b_1|$ を使う。",
               steps=[f"$\\overrightarrow{{\\mathrm{{AB}}}}={V(u1, u2)}$、$\\overrightarrow{{\\mathrm{{AC}}}}={V(v1, v2)}$。",
                      f"$a_1b_2-a_2b_1=({u1})({v2})-({u2})({v1})={det}$。", f"$S=\\dfrac{{1}}{{2}}\\cdot|{det}|={frac(S.numerator, S.denominator)}$。"],
               alt=[f"$S=\\dfrac{{1}}{{2}}\\sqrt{{|\\overrightarrow{{\\mathrm{{AB}}}}|^2|\\overrightarrow{{\\mathrm{{AC}}}}|^2-(\\overrightarrow{{\\mathrm{{AB}}}}\\cdot\\overrightarrow{{\\mathrm{{AC}}}})^2}}=\\dfrac{{1}}{{2}}\\sqrt{{{uu}\\cdot{vv}-({uv})^2}}$ でも同じ値になる。",
                    "座標平面上なので、三角形を囲む長方形から周りの直角三角形を引いて求めることもできる。"],
               pc=[("2辺のベクトルを正しく求めている", 1), ("面積公式に正しく代入している", 2), ("絶対値をつけて正の値で答えている", 1)],
               pit=["絶対値を忘れて負の面積を答える。", "$\\dfrac{1}{2}$ をかけ忘れる。"],
               chk=(f"Abs(({u1})*({v2})-({u2})*({v1}))/2", fr_py(S.numerator, S.denominator)))


@gen("standard_practice", 4, ["computation", "application"])
def space_min(r):
    while True:
        b = [r.randint(-2, 2) for _ in range(3)]
        c = [r.randint(-3, 3) for _ in range(3)]
        if any(b) and any(c) and sum(x * y for x, y in zip(b, c)) == 0:
            break
    t0 = nonzero(r, -3, 3)
    a = [ci - t0 * bi for ci, bi in zip(c, b)]
    nc = sum(x * x for x in c)
    nb = sum(x * x for x in b)
    ab = sum(x * y for x, y in zip(a, b))
    na = sum(x * x for x in a)
    E = "+".join(f"(({ai})+t*({bi}))**2" for ai, bi in zip(a, b))
    return sa(f"空間のベクトル $\\vec{{a}}={V(*a)},\\ \\vec{{b}}={V(*b)}$ がある。実数 $t$ が変化するとき、$|\\vec{{a}}+t\\vec{{b}}|$ の最小値と、そのときの $t$ の値を求めなさい。",
              f"最小値 ${sqrt_tex(nc)}$（$t={t0}$）",
              f"$|\\vec{{a}}+t\\vec{{b}}|^2={nb}t^2{'+' if 2 * ab >= 0 else '-'}{abs(2 * ab)}t+{na}$ を平方完成すると、$t={t0}$ で最小値 ${nc}$。", d=3,
              ap="大きさは2乗すると $t$ の二次関数になる。平方完成して最小値を求め、最後に平方根をとる。",
              steps=[f"$|\\vec{{a}}+t\\vec{{b}}|^2=|\\vec{{b}}|^2t^2+2(\\vec{{a}}\\cdot\\vec{{b}})t+|\\vec{{a}}|^2$。",
                     f"$|\\vec{{b}}|^2={nb}$、$\\vec{{a}}\\cdot\\vec{{b}}={ab}$、$|\\vec{{a}}|^2={na}$。",
                     f"${nb}t^2{'+' if 2 * ab >= 0 else '-'}{abs(2 * ab)}t+{na}={nb}(t{'+' if t0 < 0 else '-'}{abs(t0)})^2+{nc}$。",
                     f"$t={t0}$ のとき最小値 ${nc}$。よって $|\\vec{{a}}+t\\vec{{b}}|$ の最小値は ${sqrt_tex(nc)}$。"],
              alt=[f"$|\\vec{{a}}+t\\vec{{b}}|$ が最小になるのは $(\\vec{{a}}+t\\vec{{b}})\\perp\\vec{{b}}$ のとき。$(\\vec{{a}}+t\\vec{{b}})\\cdot\\vec{{b}}={ab}+{nb}t=0$ から $t={t0}$ が求まる（図形的な意味）。"],
              pc=[("2乗して $t$ の二次式で表している", 1), ("平方完成して最小となる $t$ を求めている", 2), ("最小値（平方根をとった値）を正しく答えている", 1)],
              pit=["2乗の最小値 " + f"${nc}$" + " をそのまま答え、平方根をとり忘れる。", "内積 $\\vec{a}\\cdot\\vec{b}$ の係数 $2$ を落とす。"],
              chk=(f"[solve(diff({E}, t), t)[0], sqrt(expand({E.replace('t', f'({t0})')}))]", f"[{t0}, sqrt({nc})]", None, "intermediate"))


@gen("standard_practice", 3, ["condition_check", "computation"])
def collinear_space(r):
    while True:
        A = [r.randint(-3, 4) for _ in range(3)]
        D = [r.randint(-3, 3) for _ in range(3)]
        if D[2] != 0 and (D[0] or D[1]):
            break
    s = r.choice([2, 3, -1, -2])
    B = [x + d for x, d in zip(A, D)]
    C = [x + s * d for x, d in zip(A, D)]
    return sa(f"空間の3点 A${V(*A)}$、B${V(*B)}$、C$(p,\\,q,\\,{C[2]})$ が一直線上にあるとき、$p,\\ q$ の値を求めなさい。",
              f"$p={C[0]},\\ q={C[1]}$",
              f"$\\overrightarrow{{\\mathrm{{AC}}}}=k\\overrightarrow{{\\mathrm{{AB}}}}$ とおき、$z$ 成分から $k={s}$。", d=3, v=[f"p={C[0]}, q={C[1]}"],
              ap="3点 A, B, C が一直線上 $\\iff\\overrightarrow{\\mathrm{AC}}=k\\overrightarrow{\\mathrm{AB}}$ となる実数 $k$ がある。成分が分かっている $z$ 成分から $k$ を決める。",
              steps=[f"$\\overrightarrow{{\\mathrm{{AB}}}}={V(*D)}$、$\\overrightarrow{{\\mathrm{{AC}}}}=(p-({A[0]}),\\,q-({A[1]}),\\,{C[2] - A[2]})$。",
                     f"$z$ 成分：${C[2] - A[2]}=k\\cdot({D[2]})$ より $k={s}$。",
                     f"$x$ 成分：$p-({A[0]})={s}\\cdot({D[0]})$ より $p={C[0]}$。", f"$y$ 成分：$q-({A[1]})={s}\\cdot({D[1]})$ より $q={C[1]}$。"],
              alt=[f"直線 AB 上の点を $\\overrightarrow{{\\mathrm{{OP}}}}=\\overrightarrow{{\\mathrm{{OA}}}}+k\\overrightarrow{{\\mathrm{{AB}}}}$ と表し、$z$ 座標が ${C[2]}$ になる $k$ を求めてもよい。"],
              pc=[("一直線上の条件を $\\overrightarrow{\\mathrm{AC}}=k\\overrightarrow{\\mathrm{AB}}$ と表している", 1), ("$k$ を正しく求めている", 1), ("$p,\\ q$ を正しく求めている", 2)],
              pit=["$\\overrightarrow{\\mathrm{AC}}=\\overrightarrow{\\mathrm{AB}}$ として $k=1$ と決めつける。", "成分ごとに別の $k$ を使ってしまう。"],
              chk=(f"solve([p-({A[0]})-k*({D[0]}), q-({A[1]})-k*({D[1]}), {C[2]}-({A[2]})-k*({D[2]})], [p, q, k])",
                   f"{{p: {C[0]}, q: {C[1]}, k: {s}}}", None, "intermediate"))


# ======================================================================
# C 思考力・記述応用
# ======================================================================

@gen("thinking_writing", 4, ["written_reasoning", "cross_unit"], rel=["HS-MATHA-U02"])
def intersection(r):
    while True:
        m1, n1, m2, n2 = (r.randint(1, 4) for _ in range(4))
        if gcd(m1, n1) == 1 and gcd(m2, n2) == 1:
            break
    al, be = Fraction(m1, m1 + n1), Fraction(m2, m2 + n2)
    den = 1 - al * be
    ca, cb = al * (1 - be) / den, be * (1 - al) / den
    s = (1 - al) / den          # AX:AQ の比
    u = 1 - s * be              # BX:BP の比
    VA, VB = "\\vec{a}", "\\vec{b}"
    ans = f"${OX}={fcoef(ca, VA, True)}{fcoef(cb, VB)}$"
    O, A, B = (0, 0), (6, 0), (2, 4)
    P = (6 * al, 0)
    Q = (2 * be, 4 * be)
    X = (6 * ca + 2 * cb, 4 * cb)
    fig = figure(f"三角形OABと、OAを{m1}:{n1}に内分する点P、OBを{m2}:{n2}に内分する点Q、AQとBPの交点X",
                 shape({"O": O, "A": A, "B": B, "P": (float(P[0]), 0), "Q": (float(Q[0]), float(Q[1])), "X": (float(X[0]), float(X[1]))},
                       segments=[("O", "A"), ("O", "B"), ("A", "B"), ("A", "Q"), ("B", "P")], scale=24))
    al_t, be_t = frac(m1, m1 + n1), frac(m2, m2 + n2)
    return desc(f"$\\triangle\\mathrm{{OAB}}$ において、辺 OA を ${m1}:{n1}$ に内分する点を P、辺 OB を ${m2}:{n2}$ に内分する点を Q とし、線分 AQ と線分 BP の交点を X とする。${OA}=\\vec{{a}},\\ {OB}=\\vec{{b}}$ とするとき、${OX}$ を $\\vec{{a}},\\ \\vec{{b}}$ を用いて表しなさい。途中の考え方も書くこと。",
                ans, f"X を AQ 上・BP 上の点として2通りに表し、$\\vec{{a}},\\ \\vec{{b}}$ が1次独立であることから係数を比較する。$\\mathrm{{AX}}:\\mathrm{{XQ}}={frac(s.numerator, s.denominator)}:{frac((1 - s).numerator, (1 - s).denominator)}$ となる。",
                [("X を AQ 上の点として媒介変数で表している", 2), ("X を BP 上の点として媒介変数で表している", 2),
                 ("$\\vec{a},\\ \\vec{b}$ が1次独立であることを述べて係数比較している", 2), ("連立方程式を解いて正しく答えている", 2)], d=4, p=8, lines=10, fig=fig,
                ap="交点は「2つの線分の両方の上にある点」。それぞれの線分上の点として媒介変数を使って表し、同じ点だから係数が一致すると考える。",
                steps=[f"$\\overrightarrow{{\\mathrm{{OP}}}}={al_t}\\vec{{a}}$、$\\overrightarrow{{\\mathrm{{OQ}}}}={be_t}\\vec{{b}}$。",
                       f"X は AQ 上：${OX}=(1-s)\\vec{{a}}+{be_t}s\\vec{{b}}$。", f"X は BP 上：${OX}={al_t}u\\vec{{a}}+(1-u)\\vec{{b}}$。",
                       f"$\\vec{{a}},\\ \\vec{{b}}$ は $\\vec{{0}}$ でなく平行でないので、$1-s={al_t}u,\\ {be_t}s=1-u$。",
                       f"解くと $s={frac(s.numerator, s.denominator)},\\ u={frac(u.numerator, u.denominator)}$。よって {ans}。"],
                alt=[f"メネラウスの定理（数学A）を $\\triangle\\mathrm{{OAQ}}$ と直線 BP に用いると $\\dfrac{{\\mathrm{{OP}}}}{{\\mathrm{{PA}}}}\\cdot\\dfrac{{\\mathrm{{AX}}}}{{\\mathrm{{XQ}}}}\\cdot\\dfrac{{\\mathrm{{QB}}}}{{\\mathrm{{BO}}}}=1$ から $\\mathrm{{AX}}:\\mathrm{{XQ}}$ が求まり、内分点の公式で同じ結果が得られる。",
                     "答えの係数を使って、X が AQ 上にある（$\\vec{a}$ と $\\overrightarrow{\\mathrm{OQ}}$ の係数の和が $1$）ことを確かめられる。"],
                pc=[("AQ 上の点としての表示", 2), ("BP 上の点としての表示", 2), ("1次独立の明記と係数比較", 2), ("正しい結論", 2)],
                pit=["1次独立であることを書かずに係数を比較する（論証の不備）。", "AQ 上の点を $s\\vec{a}+(1-s)\\overrightarrow{\\mathrm{OQ}}$ とおいたとき、$s$ の意味（どちらからの比か）を取り違える。"],
                chk=(f"solve([1-s-({fr_py(al.numerator, al.denominator)})*u, ({fr_py(be.numerator, be.denominator)})*s-(1-u)], [s, u])",
                     f"{{s: {fr_py(s.numerator, s.denominator)}, u: {fr_py(u.numerator, u.denominator)}}}", None, "intermediate"))


@gen("thinking_writing", 3, ["cross_unit", "multiple_solutions", "application"], rel=["HS-MATH1-U04"])
def cosine_cross(r):
    while True:
        p, q, s = r.randint(2, 8), r.randint(2, 8), r.randint(2, 9)
        if abs(p - q) < s < p + q and (p * p + q * q - s * s) % 2 == 0:
            break
    dot = (p * p + q * q - s * s) // 2
    S = sp.sqrt(sp.Integer(p * p * q * q - dot * dot)) / 2
    return sa(f"$\\triangle\\mathrm{{OAB}}$ において $\\mathrm{{OA}}={p},\\ \\mathrm{{OB}}={q},\\ \\mathrm{{AB}}={s}$ である。${OA}=\\vec{{a}},\\ {OB}=\\vec{{b}}$ とするとき、内積 $\\vec{{a}}\\cdot\\vec{{b}}$ と $\\triangle\\mathrm{{OAB}}$ の面積 $S$ を求めなさい。",
              f"$\\vec{{a}}\\cdot\\vec{{b}}={dot}$、$S={sp.latex(S)}$",
              f"$|\\vec{{b}}-\\vec{{a}}|^2={s * s}$ を展開して $\\vec{{a}}\\cdot\\vec{{b}}={dot}$。$S=\\dfrac{{1}}{{2}}\\sqrt{{|\\vec{{a}}|^2|\\vec{{b}}|^2-(\\vec{{a}}\\cdot\\vec{{b}})^2}}={sp.latex(S)}$。", d=4, p=8,
              ap="辺 AB の長さは $|\\vec{b}-\\vec{a}|$ で表せる。2乗して展開すると内積が現れるので、内積が求まる。面積は内積と大きさだけで表せる公式を使う。",
              steps=[f"$\\overrightarrow{{\\mathrm{{AB}}}}=\\vec{{b}}-\\vec{{a}}$ より $|\\vec{{b}}-\\vec{{a}}|^2={s * s}$。",
                     f"$|\\vec{{b}}|^2-2\\vec{{a}}\\cdot\\vec{{b}}+|\\vec{{a}}|^2={s * s}$、すなわち ${q * q}-2\\vec{{a}}\\cdot\\vec{{b}}+{p * p}={s * s}$。",
                     f"$\\vec{{a}}\\cdot\\vec{{b}}={dot}$。",
                     f"$S=\\dfrac{{1}}{{2}}\\sqrt{{{p * p}\\cdot{q * q}-({dot})^2}}=\\dfrac{{1}}{{2}}\\sqrt{{{p * p * q * q - dot * dot}}}={sp.latex(S)}$。"],
              alt=[f"余弦定理（数学Ⅰ）で $\\cos\\angle\\mathrm{{AOB}}=\\dfrac{{{p}^2+{q}^2-{s}^2}}{{2\\cdot{p}\\cdot{q}}}={tex(sp.Rational(dot, p * q))}$ を求め、$\\vec{{a}}\\cdot\\vec{{b}}={p}\\cdot{q}\\cos\\angle\\mathrm{{AOB}}$、$S=\\dfrac{{1}}{{2}}\\cdot{p}\\cdot{q}\\sin\\angle\\mathrm{{AOB}}$ としても同じ結果になる。",
                   "ヘロンの公式で面積を求めて照合することもできる。"],
              pc=[("$|\\vec{b}-\\vec{a}|^2$ を展開して内積を求めている", 3), ("面積公式を正しく使っている", 3), ("値を正しく答えている", 2)],
              pit=["$|\\vec{b}-\\vec{a}|^2=|\\vec{b}|^2-|\\vec{a}|^2$ と展開してしまう。", "面積公式の $\\dfrac{1}{2}$ を落とす。"],
              chk=(f"[(({p})**2+({q})**2-({s})**2)/2, sqrt(({p})**2*({q})**2-(({p})**2+({q})**2-({s})**2)**2/4)/2]", f"[{dot}, {sp.sstr(S)}]", None, "intermediate"))


TRIPLES = [(3, 4, 5), (4, 3, 5), (5, 12, 13), (12, 5, 13), (8, 15, 17), (15, 8, 17), (1, 0, 1), (0, 1, 1)]


@gen("thinking_writing", 3, ["condition_check", "written_reasoning"])
def perp_vector(r):
    x0, y0, L0 = r.choice(TRIPLES)
    g = r.choice([1, 1, 2, 3])
    sx, sy = r.choice([1, -1]), r.choice([1, -1])
    x, y = sx * g * x0, sy * g * y0
    unit = r.random() < 0.3
    j = 1 if unit else r.randint(1, 4)
    rr = j * L0 if not unit else 1
    if unit:
        v1 = (Fraction(-y, g * L0), Fraction(x, g * L0))
    else:
        v1 = (Fraction(-j * sy * y0), Fraction(j * sx * x0))
    v2 = (-v1[0], -v1[1])
    ft = lambda f: frac(f.numerator, f.denominator)  # noqa: E731
    fp = lambda f: fr_py(f.numerator, f.denominator)  # noqa: E731
    vt = lambda v: f"\\left({ft(v[0])},\\,{ft(v[1])}\\right)"  # noqa: E731
    what = "単位ベクトル" if unit else f"大きさが ${rr}$ のベクトル"
    return sa(f"$\\vec{{a}}={V(x, y)}$ に垂直な{what} $\\vec{{e}}$ をすべて求めなさい。答えだけでなく、条件を式で表して求める過程も書くこと。",
              f"$\\vec{{e}}={vt(v1)},\\ {vt(v2)}$",
              f"$\\vec{{e}}=(p,\\,q)$ とおくと、${x}p+({y})q=0$ かつ $p^2+q^2={rr * rr}$。これを解くと2つの解が得られる。", d=4, p=8,
              ap="求めるベクトルを $(p,\\,q)$ とおき、「垂直」と「大きさ」の2つの条件を式にして連立する。向きが逆の2つが答えになることに注意する。",
              steps=[f"$\\vec{{e}}=(p,\\,q)$ とおく。", f"垂直条件：$\\vec{{a}}\\cdot\\vec{{e}}={x}p+({y})q=0$。", f"大きさの条件：$p^2+q^2={rr * rr}$。",
                     ("垂直条件から $p=0$。これを大きさの条件に代入すると $q^2=" + f"{rr * rr}" + "$。" if y == 0 else ("垂直条件から $q=0$。これを大きさの条件に代入すると $p^2=" + f"{rr * rr}" + "$。" if x == 0 else f"垂直条件から $q={tex(sp.Rational(-x, y))}p$。これを大きさの条件に代入して解くと、2組の解が得られる。")),
                     f"$\\vec{{e}}={vt(v1)},\\ {vt(v2)}$。"],
              alt=[f"$\\vec{{a}}=(a_1,\\,a_2)$ に垂直なベクトルの1つは $(-a_2,\\,a_1)$ である（内積が $0$）。$({-y},\\,{x})$ の大きさは ${g * L0}$ なので、これを ${tex(sp.Rational(rr, g * L0))}$ 倍したものと、その逆向きが答えになる。"],
              pc=[("垂直条件を内積で表している", 2), ("大きさの条件を式にしている", 2), ("連立して正しく解いている", 2), ("向きが逆の2つを両方答えている", 2)],
              pit=["一方の向きだけを答え、逆向きのベクトルを落とす。", "大きさの条件を $p^2+q^2=" + f"{rr}" + "$（2乗し忘れ）とする。"],
              chk=(f"solve([({x})*p+({y})*q, p**2+q**2-{rr * rr}], [p, q])", f"[({fp(v1[0])}, {fp(v1[1])}), ({fp(v2[0])}, {fp(v2[1])})]", "set", "intermediate"))


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(stem, wrong, step, etype, tempt, fix, ans, expl, steps, ap, alt, pit, chk=None, d=3):
    return desc(f"{stem}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい答えを求めなさい。", ans, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい解答を途中式とともに示している", 3), ("最終的な答えが正しい", 1)], d=d, p=6, lines=6,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい途中式", 3), ("正しい答え", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix), chk=chk)


@gen("error_correction", 3, ["common_error", "computation"])
def err_magnitude(r):
    while True:
        p, q = r.randint(1, 6), r.randint(1, 6)
        d = nonzero(r, -p * q + 1, p * q - 1) if p * q > 1 else 0
        sgn_ = r.choice([1, -1])
        val = p * p + 2 * sgn_ * d + q * q
        if d != 0 and val > 0:
            break
    op = "+" if sgn_ == 1 else "-"
    e = f"\\vec{{a}}{op}\\vec{{b}}"
    wrong_val = p * p + q * q
    wrong = f"$|{e}|^2=|\\vec{{a}}|^2+|\\vec{{b}}|^2={p * p}+{q * q}={wrong_val}$　よって $|{e}|={sqrt_tex(wrong_val)}$"
    fix = f"$|{e}|^2=|\\vec{{a}}|^2{op}2\\vec{{a}}\\cdot\\vec{{b}}+|\\vec{{b}}|^2={p * p}{'+' if sgn_ * d > 0 else '-'}{abs(2 * d)}+{q * q}={val}$　よって $|{e}|={sqrt_tex(val)}$"
    return err_item(f"$|\\vec{{a}}|={p},\\ |\\vec{{b}}|={q},\\ \\vec{{a}}\\cdot\\vec{{b}}={d}$ のとき、$|{e}|$ を求めなさい。", wrong, "1つ目の等号（2乗の展開）", "formula",
                    "三平方の定理の形 $c^2=a^2+b^2$ に引きずられ、$\\vec{a}\\perp\\vec{b}$ のときにしか成り立たない式を一般に使っている。",
                    fix, f"${sqrt_tex(val)}$",
                    f"$|{e}|^2=({e})\\cdot({e})$ を分配法則で展開すると、$2\\vec{{a}}\\cdot\\vec{{b}}$ の項が残る。この問題では $\\vec{{a}}\\cdot\\vec{{b}}={d}\\neq0$。",
                    [f"$|{e}|^2=({e})\\cdot({e})=|\\vec{{a}}|^2{op}2\\vec{{a}}\\cdot\\vec{{b}}+|\\vec{{b}}|^2$。", f"$={p * p}{'+' if sgn_ * d > 0 else '-'}{abs(2 * d)}+{q * q}={val}$。", f"$|{e}|\\geqq0$ より ${sqrt_tex(val)}$。"],
                    "大きさの2乗は内積で展開する。$(x+y)^2=x^2+2xy+y^2$ と同じ形になる。",
                    ["$\\vec{a}\\cdot\\vec{b}=0$（垂直）のときに限り生徒の式が成り立つ。内積が $0$ でないことを確認すれば、誤りに気づける。"],
                    ["$2\\vec{a}\\cdot\\vec{b}$ の項を落とす。", "差のときの符号 $-2\\vec{a}\\cdot\\vec{b}$ を誤る。"],
                    chk=(f"sqrt(({p})**2+2*({sgn_})*({d})+({q})**2)", f"sqrt({val})", None, "intermediate"), d=2)


@gen("error_correction", 3, ["common_error", "condition_check"])
def err_external(r):
    while True:
        x1, y1, x2, y2 = (r.randint(-5, 5) for _ in range(4))
        m, n = r.randint(1, 5), r.randint(1, 5)
        if abs(m - n) < 2 or gcd(m, n) != 1 or (x1, y1) == (x2, y2):
            continue
        dd = m - n
        X, Y = (-n * x1 + m * x2), (-n * y1 + m * y2)
        WX, WY = (m * x1 - n * x2), (m * y1 - n * y2)
        if X % dd == 0 and Y % dd == 0 and WX % dd == 0 and WY % dd == 0 and (X, Y) != (WX, WY):
            X, Y, WX, WY = X // dd, Y // dd, WX // dd, WY // dd
            break
    wrong = f"$\\dfrac{{m\\vec{{a}}-n\\vec{{b}}}}{{m-n}}$ に $m={m},\\ n={n}$ を代入して、$x=\\dfrac{{{m}\\cdot({x1})-{n}\\cdot({x2})}}{{{dd}}}={WX}$、$y=\\dfrac{{{m}\\cdot({y1})-{n}\\cdot({y2})}}{{{dd}}}={WY}$。よって $({WX},\\,{WY})$"
    fix = f"外分点は $\\dfrac{{-n\\vec{{a}}+m\\vec{{b}}}}{{m-n}}$。$x=\\dfrac{{-{n}\\cdot({x1})+{m}\\cdot({x2})}}{{{dd}}}={X}$、$y=\\dfrac{{-{n}\\cdot({y1})+{m}\\cdot({y2})}}{{{dd}}}={Y}$。よって $({X},\\,{Y})$"
    return err_item(f"2点 A${V(x1, y1)}$、B${V(x2, y2)}$ に対して、線分 AB を ${m}:{n}$ に外分する点 Q の座標を求めなさい。", wrong, "公式の係数（$\\vec{a}$ と $\\vec{b}$ にかける数）", "formula",
                    "「比 $m:n$ の $m$ を A に、$n$ を B に」と、比の順に係数をかけてしまった。内分・外分とも係数はたすきがけになることを忘れている。",
                    fix, f"$({X},\\,{Y})$", "外分点の位置ベクトルは、内分の公式の $n$ を $-n$ におきかえた $\\dfrac{-n\\vec{a}+m\\vec{b}}{m-n}$。A の係数に $n$ がかかる。",
                    ["外分の公式 $\\dfrac{-n\\vec{a}+m\\vec{b}}{m-n}$ を確認する。", f"$x$ 座標：$\\dfrac{{-{n}\\cdot({x1})+{m}\\cdot({x2})}}{{{dd}}}={X}$。", f"$y$ 座標：$\\dfrac{{-{n}\\cdot({y1})+{m}\\cdot({y2})}}{{{dd}}}={Y}$。"],
                    "外分点 Q は直線 AB 上で、比の大きい方の点の外側にある。図で位置を確かめると検算になる。",
                    [f"$\\overrightarrow{{\\mathrm{{AQ}}}}=\\dfrac{{{m}}}{{{dd}}}\\overrightarrow{{\\mathrm{{AB}}}}$ として求めても $({X},\\,{Y})$ になる。また、$\\mathrm{{AQ}}:\\mathrm{{QB}}={m}:{n}$ を距離で確かめられる。"],
                    ["比の順に係数をかけてしまう。", "外分で分母を $m+n$ にしてしまう。"],
                    chk=(f"[(-{n}*({x1})+{m}*({x2}))/({dd}), (-{n}*({y1})+{m}*({y2}))/({dd})]", f"[{X}, {Y}]", None, "intermediate"))


@gen("error_correction", 2, ["common_error", "concept"])
def err_obtuse(r):
    while True:
        a, b, th = _angle_pair(r)
        if th in (120, 135):
            break
    dot = sum(x * y for x, y in zip(a, b))
    na, nb = sum(x * x for x in a), sum(x * x for x in b)
    cos = sp.nsimplify(dot / sp.sqrt(na * nb))
    acute = 180 - th
    wrong = f"$\\vec{{a}}\\cdot\\vec{{b}}={dot}$、$|\\vec{{a}}|=\\sqrt{{{na}}},\\ |\\vec{{b}}|=\\sqrt{{{nb}}}$ より $\\cos\\theta={sp.latex(cos)}$。$\\cos\\theta$ の大きさが $\\cos{acute}^\\circ$ と等しいので $\\theta={acute}^\\circ$"
    fix = f"$\\cos\\theta={sp.latex(cos)}<0$ なので $\\theta$ は鈍角。$0^\\circ\\leqq\\theta\\leqq180^\\circ$ より $\\theta={th}^\\circ$"
    return err_item(f"2つのベクトル $\\vec{{a}}={V(*a)},\\ \\vec{{b}}={V(*b)}$ のなす角 $\\theta\\ (0^\\circ\\leqq\\theta\\leqq180^\\circ)$ を求めなさい。", wrong, "$\\cos\\theta$ から角を決める部分", "sign",
                    "特別な角の $\\cos$ の値を鋭角の表だけで覚えていて、負の値を絶対値で照合してしまった。",
                    fix, f"$\\theta={th}^\\circ$", f"$\\cos\\theta<0$ なら $90^\\circ<\\theta\\leqq180^\\circ$。$\\cos{th}^\\circ={COS_TEX[th]}$。",
                    [f"$\\cos\\theta={sp.latex(cos)}$ の符号を確認する（負）。", "負なので鈍角。", f"$\\cos{th}^\\circ={COS_TEX[th]}$ より $\\theta={th}^\\circ$。"],
                    "内積の符号で、鋭角（正）・直角（$0$）・鈍角（負）がまず判定できる。",
                    ["2つのベクトルを始点をそろえてかくと、鈍角に開いていることが図からも確かめられる。" if len(a) == 2 else "$\\cos(180^\\circ-\\theta)=-\\cos\\theta$ の関係から、鈍角の値は対応する鋭角の値の符号を変えたものになる。"],
                    ["$\\cos\\theta$ の符号を無視して鋭角を答える。"],
                    chk=(f"acos(({dot})/sqrt({na}*{nb}))*180/pi", str(th), None, "intermediate"))


@gen("error_correction", 2, ["common_error", "concept"])
def err_parallel(r):
    while True:
        b1, b2 = nonzero(r, -5, 5), nonzero(r, -5, 5)
        a1 = nonzero(r, -6, 6)
        # 平行：a1*b2 - k*b1 = 0  → k = a1*b2/b1、誤答：a1*b1 + k*b2 = 0 → k = -a1*b1/b2
        if (a1 * b2) % b1 == 0:
            k = a1 * b2 // b1
            wk = Fraction(-a1 * b1, b2)
            if wk != k:
                break
    wtex = frac(wk.numerator, wk.denominator)
    wrong = f"平行なので $\\vec{{a}}\\cdot\\vec{{b}}=0$。${a1}\\cdot({b1})+k\\cdot({b2})=0$ より $k={wtex}$"
    fix = f"平行条件は $a_1b_2-a_2b_1=0$。${a1}\\cdot({b2})-k\\cdot({b1})=0$ より $k={k}$"
    return err_item(f"$\\vec{{a}}=({a1},\\,k)$ と $\\vec{{b}}={V(b1, b2)}$ が平行になるような定数 $k$ の値を求めなさい。", wrong, "最初の条件式（平行の条件）", "concept",
                    "「内積が $0$」という条件が印象に残っていて、垂直条件と平行条件を取り違えた。",
                    fix, f"$k={k}$", f"平行 $\\iff\\vec{{a}}=t\\vec{{b}}$（$t$ は実数）。成分で書くと $a_1b_2-a_2b_1=0$。内積が $0$ になるのは垂直のとき。",
                    ["平行条件：$\\vec{a}=t\\vec{b}$ となる実数 $t$ がある。", f"$x$ 成分から $t={tex(sp.Rational(a1, b1))}$。", f"$y$ 成分：$k=t\\cdot({b2})={k}$。"],
                    "平行は「実数倍」、垂直は「内積 $0$」。条件を言葉で確認してから式にする。",
                    [f"$k={k}$ のとき $\\vec{{a}}=({a1},\\,{k})$ が $\\vec{{b}}$ の ${tex(sp.Rational(a1, b1))}$ 倍になっていることを確かめる。また、生徒の $k={wtex}$ を代入すると内積が $0$（垂直）になり、平行でないことが分かる。"],
                    ["平行と垂直の条件を取り違える。"],
                    chk=(f"solve(({a1})*({b2})-k*({b1}), k)", f"[{k}]", None, "intermediate"))


GENERATORS = [comp_linear, dot_angle, perp_param, section_point,
              angle_components, magnitude_expand, triangle_area, space_min, collinear_space,
              intersection, cosine_cross, perp_vector,
              err_magnitude, err_external, err_obtuse, err_parallel]
