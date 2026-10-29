"""単元パック：数学Ⅲ 極限（数列の極限・無限等比級数・関数の極限・連続性）。"""
import math
from fractions import Fraction as F

import sympy as sp

from banks._common import desc, figure, mc, plane, sa, shape
from hs_pack_lib import board, check, definition, derivation, example, gen, guide, intro, lesson, nonzero, poly, summary, theorem, tp

UNIT_ID = "HS-MATH3-U01"


# ----------------------------------------------------------------------
# 補助
# ----------------------------------------------------------------------

def ft(v):
    """有理数の LaTeX（分数は \\dfrac）。"""
    v = F(v)
    if v.denominator == 1:
        return str(v.numerator)
    return f"{'-' if v < 0 else ''}\\dfrac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def fp(v):
    v = F(v)
    return str(v.numerator) if v.denominator == 1 else f"Rational({v.numerator},{v.denominator})"


def pyc(coefs, var="x"):
    """係数列（高次から）→ sympy 式の文字列。"""
    deg = len(coefs) - 1
    return "+".join(f"({fp(c)})*{var}**{deg - i}" for i, c in enumerate(coefs))


def evp(coefs, x):
    x = F(x)
    deg = len(coefs) - 1
    return sum(F(c) * x ** (deg - i) for i, c in enumerate(coefs))


def LIM(var="n", to="\\infty"):
    return f"\\displaystyle\\lim_{{{var}\\to {to}}}"


def xp(p, var="x"):
    """var+p の LaTeX。"""
    return var if p == 0 else f"{var}{'+' if p > 0 else '-'}{abs(p)}"


def npow(k, var="n"):
    return "1" if k == 0 else (var if k == 1 else f"{var}^{k}")


def divided(coefs, dd, var="n"):
    """多項式の各項を var^dd で割った式の LaTeX。"""
    deg = len(coefs) - 1
    out = []
    for i, c in enumerate(coefs):
        k = deg - i
        e = k - dd
        if c == 0:
            continue
        mag = abs(c)
        if e > 0:
            term = ("" if mag == 1 else str(mag)) + npow(e, var)
        elif e == 0:
            term = str(mag)
        else:
            term = f"\\dfrac{{{mag}}}{{{npow(-e, var)}}}"
        out.append(("-" if c < 0 else ("+" if out else "")) + term)
    return "".join(out) or "0"


def co(c, var):
    """係数 c をつけた項（c=±1 の省略）。"""
    if c == 1:
        return var
    if c == -1:
        return "-" + var
    return f"{c}{var}"


def tf_(c, first=False):
    """符号つき定数項。"""
    if c == 0:
        return ""
    return (str(c) if first else (f"+{c}" if c > 0 else f"{c}"))


def cf(c):
    """係数の表記（1 は省略、-1 は -）。"""
    return "" if c == 1 else ("-" if c == -1 else str(c))


def trig_arg(a, var="x"):
    return var if a == 1 else f"{a}{var}"


LESSON = lesson(
    goals=["数列の収束・発散を定義に基づいて判定し、$\\infty-\\infty$ や $\\dfrac{\\infty}{\\infty}$ の形の極限を式変形によって求められる。",
           "数列 $\\{r^n\\}$ の極限を $r$ の値で分類し、無限等比級数が収束する条件とその和を求められる。",
           "関数の極限（片側極限・$x\\to\\pm\\infty$）と $\\displaystyle\\lim_{x\\to0}\\dfrac{\\sin x}{x}=1$ を用いて極限を計算し、関数の連続性と中間値の定理を説明できる。"],
    duration=200,
    readiness=["分数式の約分、分母の有理化（数学Ⅰ・数学Ⅱ）ができる。", "等比数列の和の公式 $S_n=\\dfrac{a(1-r^n)}{1-r}$ と漸化式 $a_{n+1}=pa_n+q$ の解き方（数学B）を使える。",
               "弧度法と三角関数の値・グラフ（数学Ⅱ）を使える。"],
    flow=[("導入：限りなく近づくとは", 10, "$0.999\\cdots$ は $1$ に等しいか、を問いかけ、極限の考え方を導入する"),
          ("数列の極限", 40, "収束・発散の定義、極限の性質、不定形の処理（例題1）"),
          ("$\\{r^n\\}$ と無限等比級数", 40, "$\\{r^n\\}$ の極限の分類とその証明、無限等比級数の和、収束条件（例題2）"),
          ("関数の極限", 45, "$x\\to a$・片側極限・$x\\to\\pm\\infty$、はさみうちの原理、$\\dfrac{\\sin x}{x}$ の極限の証明と例題3"),
          ("連続性", 35, "連続の定義、中間値の定理と方程式の実数解の存在（例題4）"),
          ("演習とまとめ", 30, "確認問題、典型的な誤りの検討、問題プリントの課題指示")],
    sections=[
        intro("in1", "「限りなく近づく」を数学のことばにする",
              "$0.9,\\ 0.99,\\ 0.999,\\ \\cdots$ と $9$ を1つずつ増やしていくと、値は $1$ との差が $\\dfrac{1}{10^n}$ となり、いくらでも $1$ に近づく。このとき、数列は $1$ に収束するといい、循環小数 $0.\\dot{9}$ はこの極限値 $1$ を表すと約束する。極限は、微分（接線の傾き）や積分（面積）の土台となる考え方であり、数学Ⅲではこれを数列と関数の両方について学ぶ。",
              bullets=["数列の極限：$n$ を限りなく大きくしたときの $a_n$ のふるまい。", "関数の極限：$x$ を $a$ に限りなく近づけたときの $f(x)$ のふるまい。",
                       "極限は「代入」ではなく「近づける」操作であり、$\\infty$ は数ではない。"],
              points=[tp("$0.\\dot{9}=1$ に納得できるかを挙手で確認し、「差がいくらでも小さくできる」ことを説明の軸にする。",
                         ask="$1$ と $0.999\\cdots$ の差はいくつか。", expect="どんな正の数よりも小さいので $0$ としか言えない。", timing="導入の冒頭")]),
        definition("df1", "数列の極限",
                   "数列 $\\{a_n\\}$ において、$n$ を限りなく大きくするとき、$a_n$ がある値 $\\alpha$ に限りなく近づくならば、$\\{a_n\\}$ は $\\alpha$ に収束するといい、$\\displaystyle\\lim_{n\\to\\infty}a_n=\\alpha$ と書く。収束しない数列は発散するという。発散には、正の無限大に発散（$\\infty$）、負の無限大に発散（$-\\infty$）、どちらでもない振動の3通りがある。",
                   formula="$$\\lim_{n\\to\\infty}a_n=\\alpha,\\ \\lim_{n\\to\\infty}b_n=\\beta\\ \\Longrightarrow\\ \\lim_{n\\to\\infty}(ka_n+lb_n)=k\\alpha+l\\beta,\\quad \\lim_{n\\to\\infty}a_nb_n=\\alpha\\beta,\\quad \\lim_{n\\to\\infty}\\dfrac{a_n}{b_n}=\\dfrac{\\alpha}{\\beta}\\ (\\beta\\neq0)$$",
                   conditions=["これらの性質は $\\{a_n\\},\\ \\{b_n\\}$ がともに収束するときに使える。$\\infty-\\infty$、$\\dfrac{\\infty}{\\infty}$、$0\\times\\infty$ の形（不定形）は、式を変形してから極限を考える。",
                               "はさみうちの原理：$a_n\\leqq c_n\\leqq b_n$ で $\\displaystyle\\lim_{n\\to\\infty}a_n=\\lim_{n\\to\\infty}b_n=\\alpha$ ならば $\\displaystyle\\lim_{n\\to\\infty}c_n=\\alpha$。",
                               "$a_n\\leqq b_n$ で $\\displaystyle\\lim_{n\\to\\infty}a_n=\\infty$ ならば $\\displaystyle\\lim_{n\\to\\infty}b_n=\\infty$。"],
                   points=[tp("$\\infty-\\infty$ を $0$、$\\dfrac{\\infty}{\\infty}$ を $1$ とする誤りの反例（$n^2-n$、$\\dfrac{2n}{n}$）を示し、不定形は式変形が必要であることを納得させる。",
                              ask="$\\displaystyle\\lim_{n\\to\\infty}(n^2-n)$ は $\\infty-\\infty=0$ と言えるか。", expect="$n(n-1)\\to\\infty$ なので言えない。", caution="$\\infty$ を数のように計算する誤りが多い。")]),
        example("ex1", "例題1　不定形の極限",
                "(1) $\\displaystyle\\lim_{n\\to\\infty}\\dfrac{3n^2-n+2}{2n^2+5}$　(2) $\\displaystyle\\lim_{n\\to\\infty}(\\sqrt{n^2+4n}-n)$ を求めよ。",
                ["(1) 分母の最高次 $n^2$ で分子・分母を割ると $\\dfrac{3-\\dfrac{1}{n}+\\dfrac{2}{n^2}}{2+\\dfrac{5}{n^2}}\\to\\dfrac{3}{2}$。",
                 "(2) $\\sqrt{n^2+4n}-n=\\dfrac{(\\sqrt{n^2+4n}-n)(\\sqrt{n^2+4n}+n)}{\\sqrt{n^2+4n}+n}=\\dfrac{4n}{\\sqrt{n^2+4n}+n}$。",
                 "分子・分母を $n$ で割ると $\\dfrac{4}{\\sqrt{1+\\dfrac{4}{n}}+1}\\to\\dfrac{4}{2}=2$。"],
                "(1) $\\dfrac{3}{2}$　(2) $2$",
                thinking="(1) は $\\dfrac{\\infty}{\\infty}$、(2) は $\\infty-\\infty$ の不定形。(1) は最高次で割り、(2) は分子の有理化で $\\dfrac{\\infty}{\\infty}$ の形に直す。",
                points=[tp("(2) で「$\\sqrt{n^2+4n}$ はほぼ $n$ だから $0$」と答える生徒に、$n=100$ のときの値 $\\sqrt{10400}-100\\fallingdotseq1.98$ を電卓で確かめさせる。")],
                misconceptions=[("(2) を $\\infty-\\infty=0$ とする", "有理化して $\\dfrac{4n}{\\sqrt{n^2+4n}+n}$ とすると $2$ に収束する")]),
        theorem("th1", "数列 $\\{r^n\\}$ の極限",
                "$$r>1\\ \\text{のとき}\\ \\lim_{n\\to\\infty}r^n=\\infty,\\quad r=1\\ \\text{のとき}\\ 1,\\quad |r|<1\\ \\text{のとき}\\ 0,\\quad r\\leqq-1\\ \\text{のとき振動}$$",
                ["$\\{r^n\\}$ が収束するための必要十分条件は $-1<r\\leqq1$。", "$r=1$ では収束（極限値 $1$）、$r=-1$ では $-1,\\ 1,\\ -1,\\ \\cdots$ と振動する。",
                 "底の異なる指数を含む式は、最も大きい底の累乗で分子・分母を割ると $\\left(\\dfrac{b}{a}\\right)^n\\to0$ が使える形になる。"],
                proof=["$r>1$ のとき、$r=1+h\\ (h>0)$ とおくと、二項定理より $r^n=(1+h)^n\\geqq1+nh$。$n\\to\\infty$ のとき $1+nh\\to\\infty$ なので $r^n\\to\\infty$。",
                       "$0<|r|<1$ のとき、$\\dfrac{1}{|r|}>1$ だから前段より $\\dfrac{1}{|r|^n}\\to\\infty$、よって $|r^n|=|r|^n\\to0$ であり $r^n\\to0$。$r=0$ のときは明らか。",
                       "$r<-1$ のとき、$|r|^n\\to\\infty$ で符号が交互に変わるので振動する。$r=-1$ のときも $\\pm1$ を交互にとり振動する。"],
                points=[tp("$r=1$ と $r=-1$ の場合を板書の表で区別させ、収束条件が $-1<r\\leqq1$（右端だけ等号）になる理由を言わせる。",
                           ask="$r=-1$ と $r=1$ で $\\{r^n\\}$ のふるまいはどう違うか。", expect="$r=1$ は常に $1$ で収束、$r=-1$ は $\\pm1$ を往復して振動。", timing="定理の直後")]),
        derivation("dv1", "無限等比級数の和の導出",
                   ["初項 $a\\ (\\neq0)$、公比 $r$ の等比数列の初項から第 $n$ 項までの和は、$r\\neq1$ のとき $S_n=\\dfrac{a(1-r^n)}{1-r}$。",
                    "$|r|<1$ のとき $r^n\\to0$ だから $\\displaystyle\\lim_{n\\to\\infty}S_n=\\dfrac{a}{1-r}$。これが無限等比級数 $\\displaystyle\\sum_{n=1}^{\\infty}ar^{n-1}$ の和である。",
                    "$r>1$ または $r\\leqq-1$ のときは $\\{r^n\\}$ が発散するので $\\{S_n\\}$ も発散する。$r=1$ のときは $S_n=na$ で発散する。",
                    "$a=0$ のときは、すべての項が $0$ なので $r$ によらず和は $0$ に収束する。"],
                   body="無限級数の和とは、部分和 $S_n$ の極限のことである。「無限個を足す」操作を、部分和という有限の和の極限として定める点が大切である。",
                   points=[tp("収束条件は「$a=0$ または $-1<r<1$」であることを強調する。$\\{r^n\\}$ の収束条件（$-1<r\\leqq1$）と $r=1$ の扱いが違う理由を部分和 $S_n=na$ で確認させる。",
                              caution="初項に変数を含む級数で $a=0$ の場合を落とす誤りが非常に多い。")]),
        example("ex2", "例題2　無限等比級数の収束条件",
                "無限等比級数 $x+x(1-x)+x(1-x)^2+\\cdots$ が収束するような $x$ の値の範囲を求め、そのときの和を求めよ。",
                ["初項 $x$、公比 $1-x$ の無限等比級数である。", "$x=0$ のとき、すべての項が $0$ で収束し、和は $0$。",
                 "$x\\neq0$ のとき、収束条件は $-1<1-x<1$、すなわち $0<x<2$。和は $\\dfrac{x}{1-(1-x)}=1$。",
                 "以上をまとめて、収束する範囲は $0\\leqq x<2$。"],
                "$0\\leqq x<2$。和は $x=0$ のとき $0$、$0<x<2$ のとき $1$",
                thinking="初項が $x$ を含むので、初項が $0$ になる場合を別に考える。",
                points=[tp("答えの範囲 $0\\leqq x<2$ のうち $x=0$ がどこから来たかを、生徒に説明させる。")]),
        definition("df2", "関数の極限と片側極限",
                   "$x$ が $a$ と異なる値をとりながら $a$ に限りなく近づくとき、$f(x)$ が値 $\\alpha$ に限りなく近づくならば $\\displaystyle\\lim_{x\\to a}f(x)=\\alpha$ と書く。$x$ が $a$ より大きい値をとりながら近づくときの極限を右側極限 $\\displaystyle\\lim_{x\\to a+0}f(x)$、小さい値をとりながら近づくときを左側極限 $\\displaystyle\\lim_{x\\to a-0}f(x)$ という。",
                   formula="$$\\lim_{x\\to a}f(x)=\\alpha\\iff\\lim_{x\\to a+0}f(x)=\\lim_{x\\to a-0}f(x)=\\alpha$$",
                   conditions=["数列と同様に、和・差・積・商の極限の性質と、はさみうちの原理が成り立つ。",
                               "$x\\to-\\infty$ の極限では、$x<0$ なので $\\sqrt{x^2}=|x|=-x$ となることに注意する（$x=-t$ と置きかえると $t\\to\\infty$ の問題になる）。",
                               "$\\displaystyle\\lim_{x\\to a}\\dfrac{f(x)}{g(x)}$ が有限の値で $\\displaystyle\\lim_{x\\to a}g(x)=0$ ならば、$\\displaystyle\\lim_{x\\to a}f(x)=0$ でなければならない。"],
                   figure=figure("y=1/x のグラフ（x→+0 で ∞、x→-0 で -∞）", plane((-4, 4), (-4, 4), unit=18, curves=[(lambda x: 1 / x if abs(x) > 0.2 else float("nan"), "")])),
                   points=[tp("$y=\\dfrac{1}{x}$ のグラフで、$x\\to+0$ と $x\\to-0$ で行き先が違うことを確認し、「左右の極限が一致しないときは極限はない」とまとめる。",
                              ask="$\\displaystyle\\lim_{x\\to0}\\dfrac{1}{x}$ は $\\infty$ と答えてよいか。", expect="右から $\\infty$、左から $-\\infty$ なので極限はない。")]),
        theorem("th2", "$\\dfrac{\\sin x}{x}$ の極限",
                "$$\\lim_{x\\to0}\\dfrac{\\sin x}{x}=1$$",
                ["$x$ の単位は弧度法（ラジアン）。度数法ではこの式は成り立たない。",
                 "これから $\\displaystyle\\lim_{x\\to0}\\dfrac{\\tan x}{x}=1$、$\\displaystyle\\lim_{x\\to0}\\dfrac{1-\\cos x}{x^2}=\\dfrac{1}{2}$ が導かれる。",
                 "$\\displaystyle\\lim_{x\\to0}\\dfrac{\\sin ax}{bx}=\\dfrac{a}{b}$ のように、$\\sin$ の中身と分母をそろえてから使う。"],
                proof=["$0<x<\\dfrac{\\pi}{2}$ とする。半径 $1$、中心角 $x$ の扇形 OAB と、A における接線と直線 OB の交点を T とする。",
                       "面積を比べると $\\triangle\\mathrm{OAB}<\\text{扇形 OAB}<\\triangle\\mathrm{OAT}$ より $\\dfrac{1}{2}\\sin x<\\dfrac{1}{2}x<\\dfrac{1}{2}\\tan x$。",
                       "各辺を $\\dfrac{1}{2}\\sin x\\ (>0)$ で割って逆数をとると $\\cos x<\\dfrac{\\sin x}{x}<1$。",
                       "$x\\to+0$ のとき $\\cos x\\to1$ なので、はさみうちの原理より $\\dfrac{\\sin x}{x}\\to1$。",
                       "$\\dfrac{\\sin x}{x}$ は偶関数（$x$ を $-x$ にしても値が変わらない）なので、$x\\to-0$ のときも $1$ に近づく。"],
                figure=figure("単位円の扇形 OAB と接線上の点 T（面積の大小関係）",
                              shape({"O": (0, 0), "A": (4, 0), "B": (4 * math.cos(0.7), 4 * math.sin(0.7)), "T": (4, 4 * math.tan(0.7))},
                                    segments=[("O", "A"), ("O", "T"), ("A", "T"), ("A", "B")], circle=((0, 0), 4), scale=26)),
                points=[tp("証明の図で、3つの図形の面積の大小を生徒に言わせてから式にする。弧度法でないと扇形の面積が $\\dfrac{1}{2}x$ にならないことに触れる。",
                           ask="扇形 OAB の面積が $\\dfrac{1}{2}x$ になるのはなぜか。", expect="半径 $r$、中心角 $\\theta$（ラジアン）の扇形の面積は $\\dfrac{1}{2}r^2\\theta$ だから。", timing="証明の第2段")]),
        example("ex3", "例題3　三角関数を含む極限",
                "(1) $\\displaystyle\\lim_{x\\to0}\\dfrac{\\sin 3x}{2x}$　(2) $\\displaystyle\\lim_{x\\to0}\\dfrac{1-\\cos x}{x^2}$ を求めよ。",
                ["(1) $\\dfrac{\\sin 3x}{2x}=\\dfrac{3}{2}\\cdot\\dfrac{\\sin 3x}{3x}$。$x\\to0$ のとき $3x\\to0$ なので $\\dfrac{3}{2}\\cdot1=\\dfrac{3}{2}$。",
                 "(2) 分子・分母に $1+\\cos x$ をかけると $\\dfrac{1-\\cos^2x}{x^2(1+\\cos x)}=\\left(\\dfrac{\\sin x}{x}\\right)^2\\cdot\\dfrac{1}{1+\\cos x}$。",
                 "$x\\to0$ のとき $1^2\\cdot\\dfrac{1}{2}=\\dfrac{1}{2}$。"],
                "(1) $\\dfrac{3}{2}$　(2) $\\dfrac{1}{2}$",
                thinking="$\\dfrac{\\sin\\bigcirc}{\\bigcirc}$ の形（中身と分母が同じ）をつくる。$1-\\cos x$ は $1+\\cos x$ をかけて $\\sin^2x$ にする。",
                points=[tp("(1) で「$\\dfrac{\\sin 3x}{2x}=\\dfrac{3}{2}$ は $\\sin$ を消して $3x$ と $2x$ を約分した」と誤解する生徒がいるので、$\\dfrac{\\sin 3x}{3x}$ をつくる理由を確認する。")]),
        definition("df3", "関数の連続性と中間値の定理",
                   "関数 $f(x)$ が $x=a$ で定義されていて $\\displaystyle\\lim_{x\\to a}f(x)=f(a)$ が成り立つとき、$f(x)$ は $x=a$ で連続であるという。区間のすべての点で連続な関数を、その区間で連続な関数という。多項式関数、分数関数（分母が $0$ でない範囲）、三角関数・指数関数・対数関数は定義域で連続である。",
                   formula="$$\\text{中間値の定理：}f(x)\\ \\text{が}\\ a\\leqq x\\leqq b\\ \\text{で連続で}\\ f(a)f(b)<0\\ \\Longrightarrow\\ f(c)=0\\ \\text{となる}\\ c\\ (a<c<b)\\ \\text{が少なくとも1つある}$$",
                   conditions=["連続であるためには、(i) $f(a)$ が定義されている、(ii) $\\displaystyle\\lim_{x\\to a}f(x)$ が存在する、(iii) 両者が等しい、の3つがすべて必要。",
                               "中間値の定理は「閉区間で連続」が前提。途中で不連続な関数（例：$y=\\dfrac{1}{x}$ を $-1\\leqq x\\leqq1$ で考える）では成り立たない。",
                               "中間値の定理が保証するのは解の存在だけで、解の個数や値は分からない。"],
                   points=[tp("$y=\\dfrac{1}{x}$ で $f(-1)=-1<0<1=f(1)$ なのに $f(x)=0$ の解がないことを示し、「連続」という前提の必要性を考えさせる。",
                              ask="$f(-1)f(1)<0$ なのに解がないのはなぜか。", expect="$x=0$ で定義されておらず、区間で連続でないから。", timing="中間値の定理の直後")]),
        example("ex4", "例題4　方程式の実数解の存在",
                "方程式 $x^3+x-1=0$ は $0<x<1$ の範囲に少なくとも1つの実数解をもつことを示せ。",
                ["$f(x)=x^3+x-1$ とおくと、$f(x)$ は多項式関数なので $0\\leqq x\\leqq1$ で連続である。",
                 "$f(0)=-1<0$、$f(1)=1>0$。",
                 "中間値の定理より、$f(c)=0$ となる $c$ が $0<c<1$ の範囲に少なくとも1つ存在する。"],
                "（証明終）$0<x<1$ に少なくとも1つの実数解をもつ",
                thinking="「連続であること」と「両端の値の符号が異なること」の2つを示せば、中間値の定理が使える。",
                points=[tp("答案で「連続である」と書くことを忘れると減点されることを伝え、定理の前提を書く習慣をつけさせる。")]),
        board("bd1", "板書案",
              [("① 数列の極限", ["収束・発散（$\\infty$、$-\\infty$、振動）", "不定形は式変形：最高次で割る・有理化", "例1 $\\dfrac{3}{2}$、$2$", "はさみうちの原理"]),
               ("② $r^n$ と無限等比級数", ["$\\{r^n\\}$ 収束 $\\iff -1<r\\leqq1$", "$\\displaystyle\\sum_{n=1}^{\\infty}ar^{n-1}=\\dfrac{a}{1-r}\\ (|r|<1)$", "収束 $\\iff a=0$ または $|r|<1$", "例2 $0\\leqq x<2$"]),
               ("③ 関数の極限・連続", ["片側極限 $x\\to a\\pm0$", "$\\displaystyle\\lim_{x\\to0}\\dfrac{\\sin x}{x}=1$（弧度法）", "連続 $\\iff\\displaystyle\\lim_{x\\to a}f(x)=f(a)$", "中間値の定理（連続＋符号の変化）"])],
              points=[tp("②の収束条件は、$\\{r^n\\}$（$-1<r\\leqq1$）と級数（$|r|<1$ または $a=0$）を上下に並べて書き、違いを色チョークで示す。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("極限を求める前に「どの不定形か」を言わせる習慣をつけると、変形の方針（最高次で割る・有理化・因数分解）が自然に決まる。", ask="この極限は何の形か。", expect="$\\dfrac{\\infty}{\\infty}$ の形なので最高次で割る、など。"),
               tp("$x\\to-\\infty$ のときに $\\sqrt{x^2}=x$ としてしまう誤りが多い。$x=-t$ の置きかえを標準の手順として指導する。", caution="符号の誤りに気づかないまま $\\dfrac{a}{2}$ と答える答案が典型。"),
               tp("無限等比級数の収束条件では、初項が $0$ になる場合を必ず検討させる。答えの範囲の端（等号の有無）を、実際に値を代入して確かめさせる。", timing="例題2の後"),
               tp("はさみうちの原理を使う答案では、不等式を立てる根拠（$-1\\leqq\\sin\\theta\\leqq1$ など）と、両側の極限が一致することの両方を書かせる。"),
               tp("中間値の定理では「連続」「符号が異なる」の2つの条件を答案に明記させる。")],
              misconceptions=[("$\\infty-\\infty=0$、$\\dfrac{\\infty}{\\infty}=1$ と計算する", "不定形なので式変形してから極限を考える"),
                              ("$\\{r^n\\}$ が収束する条件を $-1<r<1$ とする", "$r=1$ でも収束するので $-1<r\\leqq1$"),
                              ("$\\displaystyle\\lim_{x\\to\\infty}\\dfrac{\\sin x}{x}=1$", "$\\dfrac{\\sin x}{x}\\to1$ は $x\\to0$ のとき。$x\\to\\infty$ でははさみうちにより $0$")]),
        summary("sm1", "まとめ",
                ["不定形（$\\infty-\\infty$、$\\dfrac{\\infty}{\\infty}$、$\\dfrac{0}{0}$ など）は、最高次で割る・有理化・因数分解で形を変えてから極限を求める。",
                 "$\\{r^n\\}$ は $-1<r\\leqq1$ で収束。無限等比級数は $a=0$ または $|r|<1$ で収束し、和は $\\dfrac{a}{1-r}$。",
                 "$\\displaystyle\\lim_{x\\to0}\\dfrac{\\sin x}{x}=1$（弧度法）。連続 $\\iff\\displaystyle\\lim_{x\\to a}f(x)=f(a)$。中間値の定理で解の存在が示せる。"]),
        check("ck1", "確認問題",
              [("$\\displaystyle\\lim_{n\\to\\infty}\\dfrac{2^n+3^{n+1}}{3^n}$ を求めよ。", "$\\left(\\dfrac{2}{3}\\right)^n+3\\to3$"),
               ("無限等比級数 $1-\\dfrac{1}{2}+\\dfrac{1}{4}-\\cdots$ の和は？", "公比 $-\\dfrac{1}{2}$ より $\\dfrac{1}{1-\\left(-\\frac{1}{2}\\right)}=\\dfrac{2}{3}$"),
               ("$\\displaystyle\\lim_{x\\to0}\\dfrac{\\tan 2x}{x}$ を求めよ。", "$2\\cdot\\dfrac{\\sin 2x}{2x}\\cdot\\dfrac{1}{\\cos 2x}\\to2$")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

@gen("basic_check", 5, ["computation"])
def seq_rational(r):
    while True:
        dn, dd = r.choice([(2, 2), (2, 2), (1, 1), (3, 3), (1, 2), (2, 3), (2, 1), (3, 2)])
        prod = dn == 2 and r.random() < 0.4
        if prod:
            p_, s_ = r.choice([1, 2, 3, -1]), r.choice([1, 2, 3])
            q_, t_ = nonzero(r, -4, 4), nonzero(r, -4, 4)
            num = [p_ * s_, p_ * t_ + q_ * s_, q_ * t_]
            ntex = f"({poly(p_, q_, var='n')})({poly(s_, t_, var='n')})"
        else:
            num = [nonzero(r, -4, 4)] + [r.randint(-5, 5) for _ in range(dn)]
            ntex = poly(*num, var="n")
        den = [r.choice([1, 2, 3, 4, -1, -2])] + [r.randint(-5, 5) for _ in range(dd)]
        if all(evp(den, k) != 0 for k in range(1, 12)):
            break
    dtex = poly(*den, var="n")
    expr = f"({pyc(num, 'n')})/({pyc(den, 'n')})"
    pre = [f"分子を展開すると ${poly(*num, var='n')}$。"] if prod else []
    steps = pre + [f"分母の最高次の項 ${npow(dd)}$ で分子・分母を割ると $\\dfrac{{{divided(num, dd)}}}{{{divided(den, dd)}}}$。"]
    if dn == dd:
        L = F(num[0], den[0])
        steps.append(f"$\\dfrac{{1}}{{n}}\\to0$ などを用いると、極限は $\\dfrac{{{num[0]}}}{{{den[0]}}}={ft(L)}$。")
        ans = f"${ft(L)}$"
        chk = (f"limit({expr}, n, oo)", fp(L))
        e = f"分子・分母の最高次（ともに ${npow(dd)}$）の係数の比 ${ft(L)}$ に収束する。"
    elif dn < dd:
        steps.append(f"分子の各項は $0$ に、分母は ${den[0]}$ に近づくので、極限は $0$。")
        ans = "$0$"
        chk = (f"limit({expr}, n, oo)", "0")
        e = "分子の次数が分母の次数より低いので $0$ に収束する。"
    else:
        s = 1 if num[0] * den[0] > 0 else -1
        steps.append(f"分子は ${co(num[0], npow(dn - dd))}$ の項により{'正' if num[0] > 0 else '負'}の無限大に発散し、分母は ${den[0]}$ に近づく。")
        steps.append(f"よって {'正' if s > 0 else '負'}の無限大に発散する。")
        ans = "$\\infty$（正の無限大に発散する）" if s > 0 else "$-\\infty$（負の無限大に発散する）"
        chk = (f"atan(limit({expr}, n, oo))", "pi/2" if s > 0 else "-pi/2", None, "intermediate")
        e = "分子の次数が分母の次数より高いので発散する。符号は最高次の係数の比で決まる。"
    return sa(f"極限 ${LIM()}\\dfrac{{{ntex}}}{{{dtex}}}$ を求めなさい。", ans, e, d=2,
              ap="$\\dfrac{\\infty}{\\infty}$ の不定形。分母の最高次の項で分子・分母を割り、$\\dfrac{1}{n^k}\\to0$ が使える形にする。",
              steps=steps,
              alt=[f"分子・分母の最高次の項だけを比べる（${co(num[0], npow(dn))}$ と ${co(den[0], npow(dd))}$）と、極限の見当がつく。答えの検算に使える。"],
              pc=[("分母の最高次で割る変形をしている", 1), ("極限を正しく求めている", 1)],
              pit=["$\\dfrac{\\infty}{\\infty}=1$ と考えてしまう。", "分子の最高次で割ってしまい、分母に $\\dfrac{1}{n}$ が残って $\\dfrac{\\cdots}{0}$ の形で迷う。"],
              chk=chk)


def pw(c, base, e, first=False):
    """c·base^{n+e} の LaTeX。"""
    expo = "n" if e == 0 else f"n+{e}"
    mag = abs(c)
    coef = "" if mag == 1 else f"{mag}\\cdot "
    s = "-" if c < 0 else ("" if first else "+")
    return f"{s}{coef}{base}^{{{expo}}}"


@gen("basic_check", 4, ["computation"])
def geom_power(r):
    if r.random() < 0.3:
        q = r.randint(2, 5)
        p = r.randint(-4, 4)
        rt = f"\\dfrac{{{xp(p)}}}{{{q}}}"
        right = f"${-q - p}<x\\leqq {q - p}$"
        ch = [right, f"${-q - p}<x<{q - p}$", f"${-q - p}\\leqq x\\leqq {q - p}$", f"$x\\leqq {q - p}$"]
        why = {ch[1]: ("公比が $1$ のとき（$x=" + str(q - p) + "$）は、すべての項が $1$ で $1$ に収束する。この場合を落としている。", "$r=1$ の場合の見落とし"),
               ch[2]: ("公比が $-1$ のとき（$x=" + str(-q - p) + "$）は、$-1,\\ 1,\\ -1,\\ \\cdots$ と振動して収束しない。", "$r=-1$ の場合の誤解"),
               ch[3]: ("公比が $-1$ 以下のときは振動する。下側の条件を落としている。", "収束条件の片側の見落とし")}
        return mc(f"数列 $\\left\\{{\\left({rt}\\right)^n\\right\\}}$ が収束するような $x$ の値の範囲として正しいものを選びなさい。", ch,
                  f"$\\{{r^n\\}}$ が収束する条件は $-1<r\\leqq1$。$-1<{rt}\\leqq1$ より ${-q - p}<x\\leqq {q - p}$。", d=2,
                  ap="$\\{r^n\\}$ が収束するための必要十分条件 $-1<r\\leqq1$ に、公比 $r$ を当てはめる。右端だけ等号がつくことに注意。",
                  steps=[f"$r={rt}$ とおく。", "$\\{r^n\\}$ が収束する $\\iff -1<r\\leqq1$。", f"$-{q}<{xp(p)}\\leqq {q}$ より ${-q - p}<x\\leqq {q - p}$。"],
                  alt=[f"端の値を代入して確かめる：$x={q - p}$ なら $r=1$ で収束、$x={-q - p}$ なら $r=-1$ で振動。"],
                  pc=[("収束条件 $-1<r\\leqq1$ を使っている", 1), ("$x$ の範囲が正しい", 1)],
                  pit=["無限等比級数の収束条件 $|r|<1$ と混同する。"], why=why, ps=["condition_check"],
                  chk=(f"[solve(Eq(({xp(p)})/{q}, 1), x), solve(Eq(({xp(p)})/{q}, -1), x)]", f"[[{q - p}], [{-q - p}]]", None, "intermediate"))
    while True:
        a = r.randint(3, 7)
        b = r.randint(2, a - 1)
        if math.gcd(a, b) == 1:
            break
    if r.random() < 0.78:
        k1, k2, k3, k4 = nonzero(r, -3, 3), nonzero(r, -3, 3), r.choice([1, 2, 3, -1]), nonzero(r, -3, 3)
        e1, e2, e3 = r.choice([0, 1, 1, 2]), r.choice([0, 1]), r.choice([0, 0, 1])
        num_terms = [(k1, a, e1), (k2, b, e2)]
        if r.random() < 0.4:
            num_terms.reverse()
        L = F(k1 * a ** e1, k3 * a ** e3)
        zero = False
    else:
        k2, k3, k4 = nonzero(r, -3, 3), r.choice([1, 2, -1]), nonzero(r, -3, 3)
        e2, e3 = r.choice([0, 1, 2]), r.choice([0, 1])
        c0 = nonzero(r, -4, 4)
        num_terms = [(k2, b, e2)]
        L = F(0)
        zero = True
    den_terms = [(k3, a, e3), (k4, b, 0)]
    for nn in range(1, 12):
        if k3 * a ** (nn + e3) + k4 * b ** nn == 0:
            k4 = -k4 if k4 * k3 < 0 else k4
    ntex = "".join(pw(c, bs, e, i == 0) for i, (c, bs, e) in enumerate(num_terms)) + (tf_(c0) if zero else "")
    dtex = pw(k3, a, e3, True) + pw(k4, b, 0)
    npy = "+".join(f"({c})*{bs}**(n+{e})" for c, bs, e in num_terms) + (f"+({c0})" if zero else "")
    dpy = f"({k3})*{a}**(n+{e3})+({k4})*{b}**n"
    rr = f"\\left(\\dfrac{{{b}}}{{{a}}}\\right)^n"
    if zero:
        div_num = f"{ft(F(k2 * b ** e2))}{rr}{'+' if c0 > 0 else '-'}{abs(c0)}\\left(\\dfrac{{1}}{{{a}}}\\right)^n"
    else:
        div_num = f"{k1 * a ** e1}{'+' if k2 > 0 else '-'}{cf(abs(k2) * b ** e2)}{rr}"
    div_den = f"{k3 * a ** e3}{'+' if k4 > 0 else '-'}{'' if abs(k4) == 1 else abs(k4)}{rr}"
    return sa(f"極限 ${LIM()}\\dfrac{{{ntex}}}{{{dtex}}}$ を求めなさい。", f"${ft(L)}$",
              f"分子・分母を ${a}^n$ で割ると、$0<\\dfrac{{{b}}}{{{a}}}<1$ より ${rr}\\to0$ となり、極限は ${ft(L)}$。", d=2,
              ap="底が最も大きい累乗（ここでは $" + str(a) + "^n$）で分子・分母を割り、$|r|<1$ のとき $r^n\\to0$ を使う。",
              steps=[f"分子・分母を ${a}^n$ で割る。", f"$\\dfrac{{{div_num}}}{{{div_den}}}$。", f"$0<\\dfrac{{{b}}}{{{a}}}<1$ より ${rr}\\to0$。", f"極限は ${ft(L)}$。"],
              alt=[f"$n$ が大きいとき、${a}^n$ の項が他の項に比べて圧倒的に大きいことから、${a}^n$ の項だけを比べて見当をつける。"],
              pc=[("最大の底の累乗で割っている", 1), ("極限が正しい", 1)],
              pit=["$" + str(a) + "^{n+1}=" + str(a) + "^n\\cdot" + str(a) + "$ の変形を忘れて係数を誤る。", "小さい方の底で割ってしまい、$\\left(\\dfrac{" + str(a) + "}{" + str(b) + "}\\right)^n\\to\\infty$ の扱いに困る。"],
              chk=(f"limit(({npy})/({dpy}), n, oo)", fp(L)))


GEO_R = [F(1, 2), F(-1, 2), F(1, 3), F(-1, 3), F(2, 3), F(-2, 3), F(1, 4), F(-1, 4), F(3, 4), F(2, 5), F(-3, 5), F(1, 5)]


@gen("basic_check", 4, ["computation", "concept"])
def inf_geo_sum(r):
    kind = r.choice(["sigma", "terms", "terms", "decimal"])
    if kind == "decimal":
        d1, d2 = r.randint(0, 9), r.randint(1, 9)
        while d1 == d2:
            d2 = r.randint(1, 9)
        v = 10 * d1 + d2
        S = F(v, 99)
        return sa(f"循環小数 $0.\\dot{{{d1}}}\\dot{{{d2}}}$ を、無限等比級数の和として考えて分数で表しなさい。", f"${ft(S)}$",
                  f"$0.\\dot{{{d1}}}\\dot{{{d2}}}=\\dfrac{{{v}}}{{100}}+\\dfrac{{{v}}}{{100^2}}+\\cdots$ は初項 $\\dfrac{{{v}}}{{100}}$、公比 $\\dfrac{{1}}{{100}}$ の無限等比級数。", d=2,
                  ap="循環する2桁 $" + f"{d1}{d2}" + "$ を1つのかたまりと見ると、$\\dfrac{1}{100}$ ずつ小さくなる項の和になる。",
                  steps=[f"$0.\\dot{{{d1}}}\\dot{{{d2}}}=0.{d1}{d2}+0.00{d1}{d2}+\\cdots$。", f"初項 $\\dfrac{{{v}}}{{100}}$、公比 $\\dfrac{{1}}{{100}}$（$|r|<1$ なので収束）。",
                         f"和は $\\dfrac{{\\frac{{{v}}}{{100}}}}{{1-\\frac{{1}}{{100}}}}=\\dfrac{{{v}}}{{99}}={ft(S)}$。"],
                  alt=[f"$x=0.\\dot{{{d1}}}\\dot{{{d2}}}$ とおき、$100x-x={v}$ から $x=\\dfrac{{{v}}}{{99}}$ としてもよい。"],
                  pc=[("初項と公比を正しく捉えている", 1), ("分数が正しい（約分済み）", 1)],
                  pit=["公比を $\\dfrac{1}{10}$ としてしまう（2桁で循環する）。", "約分を忘れる。"],
                  chk=(f"summation(Rational({v},100)*Rational(1,100)**(n-1), [n, 1, oo])", fp(S)))
    rt = r.choice(GEO_R)
    a = nonzero(r, -6, 9)
    S = F(a) / (1 - rt)
    if kind == "sigma":
        head = "" if a == 1 else ("-" if a == -1 else str(a))
        stem = f"無限等比級数 $\\displaystyle\\sum_{{n=1}}^{{\\infty}}{head}\\left({ft(rt)}\\right)^{{n-1}}$ の和を求めなさい。"
    else:
        terms = [F(a) * rt ** k for k in range(3)]
        tex = ft(terms[0]) + "".join(("+" if t > 0 else "-") + ft(abs(t)) for t in terms[1:])
        stem = f"無限等比級数 ${tex}+\\cdots$ の和を求めなさい。"
    return sa(stem, f"${ft(S)}$", f"初項 ${a}$、公比 ${ft(rt)}$ で $|{ft(rt)}|<1$ なので収束し、和は $\\dfrac{{{a}}}{{1-({ft(rt)})}}={ft(S)}$。", d=2,
              ap="初項 $a$ と公比 $r$ を読み取り、$|r|<1$ を確かめてから $\\dfrac{a}{1-r}$ を使う。",
              steps=[f"初項 ${a}$、公比 ${ft(rt)}$。", f"$|{ft(rt)}|<1$ なので収束する。", f"和は $\\dfrac{{{a}}}{{1-({ft(rt)})}}={ft(S)}$。"],
              alt=[f"部分和 $S_n=\\dfrac{{{a}\\{{1-({ft(rt)})^n\\}}}}{{1-({ft(rt)})}}$ で $n\\to\\infty$ とすると $({ft(rt)})^n\\to0$ から同じ値になる。"],
              pc=[("収束の確認（$|r|<1$）をしている", 1), ("和が正しい", 1)],
              pit=["公比が負のとき $1-r$ を $1+|r|$ ではなく $1-|r|$ と計算してしまう。", "収束条件を確かめずに公式を使う。"],
              chk=(f"summation(({a})*({fp(rt)})**(n-1), [n, 1, oo])", fp(S)))


@gen("basic_check", 4, ["computation"])
def func_limit_factor(r):
    kind = r.choice(["quad", "quad", "cube", "sqrt"])
    if kind == "quad":
        while True:
            al, be, ga = r.randint(-4, 4), r.randint(-5, 5), r.randint(-5, 5)
            m = r.choice([1, 1, 2, 3, -1])
            if ga != al and be != ga and be != al:
                break
        num = [m, -m * (al + be), m * al * be]
        den = [1, -(al + ga), al * ga]
        L = F(m * (al - be), al - ga)
        stem = f"極限 ${LIM('x', al)}\\dfrac{{{poly(*num)}}}{{{poly(*den)}}}$ を求めなさい。"
        steps = [f"$x={al}$ を代入すると分子・分母ともに $0$ になる（$\\dfrac{{0}}{{0}}$ の不定形）。",
                 f"因数分解すると $\\dfrac{{{'' if m == 1 else ('-' if m == -1 else m)}{'x' if al == 0 else '(' + xp(-al) + ')'}({xp(-be)})}}{{{'x' if al == 0 else '(' + xp(-al) + ')'}({xp(-ga)})}}$。",
                 f"共通因数を約分して $\\dfrac{{{co(m, '(' + xp(-be) + ')') if m != 1 else xp(-be)}}}{{{xp(-ga)}}}$、$x={al}$ を代入して ${ft(L)}$。"]
        expr = f"({pyc(num)})/({pyc(den)})"
        to = al
    elif kind == "cube":
        al = nonzero(r, -3, 3)
        if r.random() < 0.5:
            stem = f"極限 ${LIM('x', al)}\\dfrac{{x^3{'-' if al ** 3 > 0 else '+'}{abs(al ** 3)}}}{{{xp(-al)}}}$ を求めなさい。"
            L = F(3 * al * al)
            expr = f"(x**3-({al ** 3}))/(x-({al}))"
            steps = ["$\\dfrac{0}{0}$ の不定形。", f"$x^3-({al})^3=({xp(-al)})(x^2{'+' if al > 0 else '-'}{'' if abs(al) == 1 else abs(al)}x+{al * al})$ と因数分解する。",
                     f"約分して $x^2{'+' if al > 0 else '-'}{'' if abs(al) == 1 else abs(al)}x+{al * al}$、$x={al}$ を代入して ${ft(L)}$。"]
        else:
            stem = f"極限 ${LIM('x', al)}\\dfrac{{x^3{'-' if al ** 3 > 0 else '+'}{abs(al ** 3)}}}{{x^2-{al * al}}}$ を求めなさい。"
            L = F(3 * al, 2)
            expr = f"(x**3-({al ** 3}))/(x**2-{al * al})"
            steps = ["$\\dfrac{0}{0}$ の不定形。", f"分子は $({xp(-al)})(x^2{'+' if al > 0 else '-'}{'' if abs(al) == 1 else abs(al)}x+{al * al})$、分母は $({xp(-al)})({xp(al)})$。",
                     f"約分して $\\dfrac{{x^2{'+' if al > 0 else '-'}{'' if abs(al) == 1 else abs(al)}x+{al * al}}}{{{xp(al)}}}$、$x={al}$ を代入して $\\dfrac{{{3 * al * al}}}{{{2 * al}}}={ft(L)}$。"]
        to = al
    else:
        s = r.randint(1, 4)
        k = r.randint(-3, 8)
        c = s * s - k
        L = F(1, 2 * s)
        stem = f"極限 ${LIM('x', c)}\\dfrac{{\\sqrt{{{xp(k)}}}-{s}}}{{{xp(-c)}}}$ を求めなさい。"
        steps = ["$\\dfrac{0}{0}$ の不定形。分子を有理化する。",
                 f"分子・分母に $\\sqrt{{{xp(k)}}}+{s}$ をかけると、分子は $({xp(k)})-{s * s}={xp(-c)}$。",
                 f"約分して $\\dfrac{{1}}{{\\sqrt{{{xp(k)}}}+{s}}}$、$x={c}$ を代入して $\\dfrac{{1}}{{{s}+{s}}}={ft(L)}$。"]
        expr = f"(sqrt(x+({k}))-{s})/(x-({c}))"
        to = c
    return sa(stem, f"${ft(L)}$", f"$\\dfrac{{0}}{{0}}$ の不定形なので、約分（または有理化）してから代入する。極限は ${ft(L)}$。", d=2,
              ap="代入して $\\dfrac{0}{0}$ になったら、分子・分母に共通因数 $(x-a)$ が隠れている。因数分解か有理化で取り出して約分する。",
              steps=steps,
              alt=[f"$x$ に ${to}$ に近い値（例：${to}\\pm0.01$）を代入して電卓で計算し、${ft(L)}$ に近いことを確かめる。"],
              pc=[("約分・有理化の変形をしている", 1), ("極限が正しい", 1)],
              pit=["$\\dfrac{0}{0}$ を $0$ や $1$ と答えてしまう。", "約分する前に代入してしまう。"],
              chk=(f"limit({expr}, x, {to})", fp(L)))


@gen("basic_check", 3, ["computation", "concept"])
def trig_limit(r):
    a, b = r.sample([1, 2, 3, 4, 5, 6], 2)
    kind = r.choice(["sin", "tan", "sinsin", "cos", "poly"])
    A, B = trig_arg(a), trig_arg(b)
    if kind == "sin":
        tex, expr, L = f"\\dfrac{{\\sin {A}}}{{{B}}}", f"sin({a}*x)/({b}*x)", F(a, b)
        steps = [f"$\\dfrac{{\\sin {A}}}{{{B}}}=\\dfrac{{{a}}}{{{b}}}\\cdot\\dfrac{{\\sin {A}}}{{{A}}}$ と変形する。", f"$x\\to0$ のとき ${A}\\to0$ なので $\\dfrac{{\\sin {A}}}{{{A}}}\\to1$。", f"極限は ${ft(L)}$。"]
    elif kind == "tan":
        tex, expr, L = f"\\dfrac{{\\tan {A}}}{{{B}}}", f"tan({a}*x)/({b}*x)", F(a, b)
        steps = [f"$\\dfrac{{\\tan {A}}}{{{B}}}=\\dfrac{{{a}}}{{{b}}}\\cdot\\dfrac{{\\sin {A}}}{{{A}}}\\cdot\\dfrac{{1}}{{\\cos {A}}}$ と変形する。", f"$\\dfrac{{\\sin {A}}}{{{A}}}\\to1$、$\\cos {A}\\to1$。", f"極限は ${ft(L)}$。"]
    elif kind == "sinsin":
        tex, expr, L = f"\\dfrac{{\\sin {A}}}{{\\sin {B}}}", f"sin({a}*x)/sin({b}*x)", F(a, b)
        steps = [f"$\\dfrac{{\\sin {A}}}{{\\sin {B}}}=\\dfrac{{\\sin {A}}}{{{A}}}\\cdot\\dfrac{{{B}}}{{\\sin {B}}}\\cdot\\dfrac{{{A}}}{{{B}}}$ と変形する。", "前の2つの因数はともに $1$ に近づく。", f"極限は $\\dfrac{{{a}}}{{{b}}}={ft(L)}$。"]
    elif kind == "cos":
        tex, expr, L = f"\\dfrac{{1-\\cos {A}}}{{x^2}}", f"(1-cos({a}*x))/x**2", F(a * a, 2)
        steps = [f"分子・分母に $1+\\cos {A}$ をかけると $\\dfrac{{\\sin^2 {A}}}{{x^2(1+\\cos {A})}}$。", f"$=\\left(\\dfrac{{\\sin {A}}}{{{A}}}\\right)^2\\cdot\\dfrac{{{a * a}}}{{1+\\cos {A}}}$。", f"$x\\to0$ のとき $1\\cdot\\dfrac{{{a * a}}}{{2}}={ft(L)}$。"]
    else:
        tex, expr, L = f"\\dfrac{{\\sin {A}}}{{x^2+{B}}}", f"sin({a}*x)/(x**2+{b}*x)", F(a, b)
        steps = [f"分母を $x(x+{b})$ と因数分解し、$\\dfrac{{\\sin {A}}}{{x}}\\cdot\\dfrac{{1}}{{x+{b}}}$ と変形する。", f"$\\dfrac{{\\sin {A}}}{{x}}={a}\\cdot\\dfrac{{\\sin {A}}}{{{A}}}\\to {a}$、$\\dfrac{{1}}{{x+{b}}}\\to\\dfrac{{1}}{{{b}}}$。", f"極限は ${ft(L)}$。"]
    return sa(f"極限 ${LIM('x', 0)}{tex}$ を求めなさい。", f"${ft(L)}$", f"$\\displaystyle\\lim_{{\\theta\\to0}}\\dfrac{{\\sin\\theta}}{{\\theta}}=1$ が使える形に変形する。極限は ${ft(L)}$。", d=2,
              ap="$\\dfrac{\\sin\\bigcirc}{\\bigcirc}$（$\\sin$ の中身と分母が同じ式）の形をつくり、$\\displaystyle\\lim_{\\theta\\to0}\\dfrac{\\sin\\theta}{\\theta}=1$ を使う。",
              steps=steps,
              alt=["$x=0.01$ などを代入して電卓で値を求め、答えに近いことを確かめる（弧度法で計算する）。"],
              pc=[("公式が使える形に変形している", 1), ("極限が正しい", 1)],
              pit=["$\\sin$ の中身と分母をそろえずに $1$ と答える。", "$\\sin {A}$ を「${A}$ と約分できる」と考えてしまう。".replace("{A}", A)],
              chk=(f"limit({expr}, x, 0)", fp(L)))


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 4, ["computation", "common_error"])
def sqrt_diff(r):
    kind = r.choice(["basic", "two", "times_n", "recip", "k", "sqrt_n"])
    a = nonzero(r, -8, 8)
    if kind == "basic":
        b = r.randint(-5, 5)
        while any(k * k + a * k + b <= 0 for k in range(1, 12)):
            b += 1
        tex = f"(\\sqrt{{n^2{co(a, 'n') if a < 0 else '+' + co(a, 'n')}{tf_(b)}}}-n)"
        expr, L = f"sqrt(n**2+({a})*n+({b}))-n", F(a, 2)
        num = f"{co(a, 'n')}{tf_(b)}"
        steps = [f"分子・分母に $\\sqrt{{n^2{'+' if a > 0 else ''}{co(a, 'n')}{tf_(b)}}}+n$ をかけると、分子は ${num}$。",
                 f"分子・分母を $n$ で割ると $\\dfrac{{{a}{'' if b == 0 else ('+' if b > 0 else '-') + '\\dfrac{' + str(abs(b)) + '}{n}'}}}{{\\sqrt{{1{'+' if a > 0 else '-'}\\dfrac{{{abs(a)}}}{{n}}{'' if b == 0 else ('+' if b > 0 else '-') + '\\dfrac{' + str(abs(b)) + '}{n^2}'}}}+1}}$。",
                 f"$n\\to\\infty$ として $\\dfrac{{{a}}}{{2}}={ft(L)}$。"]
    elif kind == "two":
        a, c = r.sample(range(1, 10), 2)
        tex = f"(\\sqrt{{n^2+{co(a, 'n')}}}-\\sqrt{{n^2+{co(c, 'n')}}})"
        expr, L = f"sqrt(n**2+{a}*n)-sqrt(n**2+{c}*n)", F(a - c, 2)
        steps = [f"分子・分母に $\\sqrt{{n^2+{co(a, 'n')}}}+\\sqrt{{n^2+{co(c, 'n')}}}$ をかけると、分子は $({a}-{c})n={co(a - c, 'n')}$。",
                 f"分子・分母を $n$ で割ると $\\dfrac{{{a - c}}}{{\\sqrt{{1+\\dfrac{{{a}}}{{n}}}}+\\sqrt{{1+\\dfrac{{{c}}}{{n}}}}}}$。", f"$n\\to\\infty$ として $\\dfrac{{{a - c}}}{{2}}={ft(L)}$。"]
    elif kind == "times_n":
        a = abs(a)
        tex = f"n(\\sqrt{{n^2+{a}}}-n)"
        expr, L = f"n*(sqrt(n**2+{a})-n)", F(a, 2)
        steps = [f"$\\sqrt{{n^2+{a}}}-n=\\dfrac{{{a}}}{{\\sqrt{{n^2+{a}}}+n}}$ と有理化する。", f"$n(\\sqrt{{n^2+{a}}}-n)=\\dfrac{{{a}n}}{{\\sqrt{{n^2+{a}}}+n}}=\\dfrac{{{a}}}{{\\sqrt{{1+\\dfrac{{{a}}}{{n^2}}}}+1}}$。", f"$n\\to\\infty$ として ${ft(L)}$。"]
    elif kind == "recip":
        a = abs(a)
        tex = f"\\dfrac{{1}}{{\\sqrt{{n^2+{co(a, 'n')}}}-n}}"
        expr, L = f"1/(sqrt(n**2+{a}*n)-n)", F(2, a)
        steps = [f"分母を有理化：分子・分母に $\\sqrt{{n^2+{co(a, 'n')}}}+n$ をかけると $\\dfrac{{\\sqrt{{n^2+{co(a, 'n')}}}+n}}{{{a}n}}$。",
                 f"分子・分母を $n$ で割ると $\\dfrac{{\\sqrt{{1+\\dfrac{{{a}}}{{n}}}}+1}}{{{a}}}$。", f"$n\\to\\infty$ として $\\dfrac{{2}}{{{a}}}={ft(L)}$。"]
    elif kind == "k":
        k = r.randint(2, 4)
        a = abs(a)
        tex = f"(\\sqrt{{{k * k}n^2+{co(a, 'n')}}}-{k}n)"
        expr, L = f"sqrt({k * k}*n**2+{a}*n)-{k}*n", F(a, 2 * k)
        steps = [f"分子・分母に $\\sqrt{{{k * k}n^2+{co(a, 'n')}}}+{k}n$ をかけると、分子は ${co(a, 'n')}$。",
                 f"分子・分母を $n$ で割ると $\\dfrac{{{a}}}{{\\sqrt{{{k * k}+\\dfrac{{{a}}}{{n}}}}+{k}}}$。", f"$n\\to\\infty$ として $\\dfrac{{{a}}}{{{2 * k}}}={ft(L)}$。"]
    else:
        a = abs(a)
        tex = f"\\sqrt{{n}}(\\sqrt{{n+{a}}}-\\sqrt{{n}})"
        expr, L = f"sqrt(n)*(sqrt(n+{a})-sqrt(n))", F(a, 2)
        steps = [f"$\\sqrt{{n+{a}}}-\\sqrt{{n}}=\\dfrac{{{a}}}{{\\sqrt{{n+{a}}}+\\sqrt{{n}}}}$ と有理化する。",
                 f"$\\sqrt{{n}}$ をかけ、分子・分母を $\\sqrt{{n}}$ で割ると $\\dfrac{{{a}}}{{\\sqrt{{1+\\dfrac{{{a}}}{{n}}}}+1}}$。", f"$n\\to\\infty$ として ${ft(L)}$。"]
    return sa(f"極限 ${LIM()}{tex}$ を求めなさい。", f"${ft(L)}$", f"有理化して不定形を解消すると、極限は ${ft(L)}$。", d=3,
              ap="根号を含む $\\infty-\\infty$ の不定形は、$(\\sqrt{A}-\\sqrt{B})(\\sqrt{A}+\\sqrt{B})=A-B$ を使って有理化し、$\\dfrac{\\infty}{\\infty}$ の形に直してから $n$ で割る。",
              steps=steps,
              alt=[f"$n=10^4$ などを代入して電卓で計算し、${ft(L)}$ に近い値になることを確かめる。"],
              pc=[("有理化して不定形を解消している", 2), ("$n$ で割る変形をしている", 1), ("極限が正しい", 1)],
              pit=["$\\infty-\\infty=0$ や $\\infty\\times0=0$ としてしまう。", "有理化の後、$\\sqrt{n^2+\\cdots}$ を $n$ で割るときに $\\sqrt{\\ }$ の中を $n^2$ で割ることを忘れる。"],
              chk=(f"limit({expr}, n, oo)", fp(L)))


@gen("standard_practice", 4, ["condition_check", "computation"])
def geo_series_x(r):
    if r.random() < 0.5:
        c = nonzero(r, -3, 5)
        p, q = r.randint(-4, 4), r.randint(2, 5)
        rt = f"\\dfrac{{{xp(p)}}}{{{q}}}"
        ctex = "" if c == 1 else ("-" if c == -1 else str(c))
        ser = f"{c}{'+' if c > 0 else '-'}{'' if abs(c) == 1 else str(abs(c)) + '\\cdot '}{rt}{'+' if c > 0 else '-'}{'' if abs(c) == 1 else abs(c)}\\left({rt}\\right)^2+\\cdots"
        lo, hi = -q - p, q - p
        Stex = (f"{'-' if c < 0 else ''}\\dfrac{{{abs(c * q)}}}{{{q - p}-x}}" if q - p != 0 else f"{'' if c < 0 else '-'}\\dfrac{{{abs(c * q)}}}{{x}}")
        ans = f"${lo}<x<{hi}$、和は ${Stex}$"
        return sa(f"無限等比級数 ${ser}$ が収束するような $x$ の値の範囲を求めなさい。また、そのときの和を求めなさい。", ans,
                  f"初項 ${c}\\neq0$、公比 ${rt}$。収束条件は $-1<{rt}<1$。和は $\\dfrac{{{c}}}{{1-{rt}}}={Stex}$。", d=3,
                  ap="無限等比級数は「初項 $=0$ または $|\\text{公比}|<1$」のとき収束する。初項が $0$ でないので、公比の条件だけを調べる。",
                  steps=[f"初項 ${c}$、公比 ${rt}$。初項は $0$ でない。", f"収束条件は $-1<{rt}<1$、すなわち $-{q}<{xp(p)}<{q}$ より ${lo}<x<{hi}$。",
                         f"和は $\\dfrac{{{c}}}{{1-{rt}}}=\\dfrac{{{c * q}}}{{{q}-({xp(p)})}}={Stex}$。"],
                  alt=[f"範囲の端 $x={hi}$ を代入すると公比 $1$ で部分和が ${c}n$ となり発散することから、等号がつかないことを確かめられる。"],
                  pc=[("収束条件 $|r|<1$ を立てている", 1), ("$x$ の範囲が正しい", 2), ("和が正しい", 1)],
                  pit=["数列 $\\{r^n\\}$ の収束条件 $-1<r\\leqq1$ と混同して等号をつける。", "和の分母 $1-r$ の計算で、$x$ の符号を誤る。"],
                  chk=(f"[solve(Eq(({xp(p)})/{q}, 1), x), solve(Eq(({xp(p)})/{q}, -1), x), simplify(({c})/(1-({xp(p)})/{q}))]",
                       f"[[{hi}], [{lo}], ({c * q})/({q - p}-x)]", None, "intermediate"))
    a = r.randint(1, 5)
    m = r.randint(1, 4)
    ax = "x" if a == 1 else f"{a}x"
    rt = "(1-x)" if m == 1 else f"\\dfrac{{{m}-x}}{{{m}}}"
    rt2 = "(1-x)^2" if m == 1 else f"\\left(\\dfrac{{{m}-x}}{{{m}}}\\right)^2"
    ser = f"{ax}+{ax}{rt}+{ax}{rt2}+\\cdots" if m == 1 else f"{ax}+{ax}\\cdot {rt}+{ax}{rt2}+\\cdots"
    return sa(f"無限等比級数 ${ser}$ が収束するような $x$ の値の範囲を求めなさい。また、そのときの和を求めなさい。",
              f"$0\\leqq x<{2 * m}$。和は $x=0$ のとき $0$、$0<x<{2 * m}$ のとき ${a * m}$",
              f"初項 ${ax}$ が $0$ になる $x=0$ の場合を別に考える。$x\\neq0$ のときは $-1<{rt}<1$ より $0<x<{2 * m}$、和は ${a * m}$。", d=3,
              ap="初項に $x$ を含むので、初項 $=0$ の場合と、初項 $\\neq0$ で $|\\text{公比}|<1$ の場合に分ける。",
              steps=[f"初項 ${ax}$、公比 ${rt if m == 1 else rt}$。", "$x=0$ のとき、すべての項が $0$ なので収束し、和は $0$。",
                     f"$x\\neq0$ のとき、収束条件は $-1<{rt}<1$、すなわち $0<x<{2 * m}$。", f"このとき和は $\\dfrac{{{ax}}}{{1-{rt}}}=\\dfrac{{{ax}}}{{\\frac{{x}}{{{m}}}}}={a * m}$。" if m != 1 else f"このとき和は $\\dfrac{{{ax}}}{{1-(1-x)}}={a}$。",
                     f"まとめて $0\\leqq x<{2 * m}$。"],
              alt=["$x=0$ を代入した級数が $0+0+0+\\cdots$ となることを実際に書いて確かめる。"],
              pc=[("初項が $0$ の場合を検討している", 1), ("公比の条件から範囲を求めている", 1), ("範囲と和が正しい", 2)],
              pit=["$x=0$ の場合を落として $0<x<" + str(2 * m) + "$ と答える。", "和を $x$ の式のまま答え、約分を忘れる。"],
              chk=(f"[solve(Eq(({m}-x)/{m}, -1), x), simplify(({a}*x)/(1-({m}-x)/{m}))]", f"[[{2 * m}], {a * m}]", None, "intermediate"))


REC_P = [F(1, 2), F(-1, 2), F(1, 3), F(2, 3), F(-1, 3), F(1, 4), F(3, 4), F(-2, 3), F(2, 5)]


@gen("standard_practice", 4, ["computation", "cross_unit"], rel=["HS-MATHB-U01"])
def recurrence_limit(r):
    p = r.choice(REC_P)
    al = nonzero(r, -3, 3) * p.denominator
    q = F(al) * (1 - p)
    a1 = r.randint(-5, 8)
    while a1 == al:
        a1 = r.randint(-5, 8)
    d = a1 - al
    ptex = ft(p)
    rec = f"a_{{n+1}}={'-' if p < 0 else ''}{ft(abs(p))}a_n{'+' if q > 0 else '-'}{ft(abs(q))}"
    gen_tex = f"a_n={al}{'+' if d > 0 else '-'}{'' if abs(d) == 1 else abs(d)}\\left({ptex}\\right)^{{n-1}}"
    G = f"({al})+({d})*({fp(p)})**(n-1)"
    G1 = f"({al})+({d})*({fp(p)})**n"
    return sa(f"$a_1={a1}$、${rec}\\ (n=1,\\,2,\\,3,\\,\\cdots)$ で定められる数列 $\\{{a_n\\}}$ の一般項を求め、極限 $\\displaystyle\\lim_{{n\\to\\infty}}a_n$ を求めなさい。",
              f"${gen_tex}$、$\\displaystyle\\lim_{{n\\to\\infty}}a_n={al}$",
              f"特性方程式 $\\alpha={ptex}\\alpha{'+' if q > 0 else '-'}{ft(abs(q))}$ の解 $\\alpha={al}$ を用いて $a_{{n+1}}-({al})={ptex}(a_n-({al}))$。$\\left|{ptex}\\right|<1$ より $\\left({ptex}\\right)^{{n-1}}\\to0$。", d=3,
              ap="数学Bの漸化式 $a_{n+1}=pa_n+q$ の解き方（$\\alpha=p\\alpha+q$ の解 $\\alpha$ を引く）で一般項を求め、$|p|<1$ なら $p^{n-1}\\to0$ を使う。",
              steps=[f"$\\alpha={ptex}\\alpha{'+' if q > 0 else '-'}{ft(abs(q))}$ を解くと $\\alpha={al}$。", f"$a_{{n+1}}-({al})={ptex}\\{{a_n-({al})\\}}$ より、数列 $\\{{a_n-({al})\\}}$ は初項 ${d}$、公比 ${ptex}$ の等比数列。",
                     f"${gen_tex}$。", f"$\\left|{ptex}\\right|<1$ より $\\left({ptex}\\right)^{{n-1}}\\to0$ なので、$\\displaystyle\\lim_{{n\\to\\infty}}a_n={al}$。"],
              alt=[f"極限 $\\alpha$ が存在すると仮定すれば、漸化式の両辺で $n\\to\\infty$ として $\\alpha={ptex}\\alpha{'+' if q > 0 else '-'}{ft(abs(q))}$ から $\\alpha={al}$ と見当がつく（ただし収束することは一般項から示す必要がある）。"],
              pc=[("特性方程式を用いて変形している", 1), ("一般項が正しい", 2), ("極限が正しい", 1)],
              pit=["等比数列の初項を $a_1$ のままにして、$a_1-\\alpha$ としない。", "$\\left(" + ptex + "\\right)^{n-1}$ の指数を $n$ にしてしまう。"],
              chk=(f"[simplify(({G1})-({fp(p)})*({G})-({fp(q)})), ({al})+({d})*({fp(p)})**0, ({al})+limit(({d})*Abs({fp(p)})**(n-1), n, oo)]", f"[0, {a1}, {al}]", None, "intermediate"))


@gen("standard_practice", 4, ["condition_check", "written_reasoning"])
def limit_param(r):
    if r.random() < 0.55:
        al = r.randint(-4, 4)
        L = nonzero(r, -6, 6)
        be = al - L
        a, b = -(al + be), al * be
        den = xp(-al)
        return sa(f"等式 ${LIM('x', al)}\\dfrac{{x^2+ax+b}}{{{den}}}={L}$ が成り立つように、定数 $a,\\ b$ の値を定めなさい。", f"$a={a},\\ b={b}$",
                  f"分母 $\\to0$ で極限が有限なので、分子 $\\to0$ が必要。$b={-al * al}{'-' if al > 0 else '+'}{'' if abs(al) == 1 else abs(al)}a$ を代入して約分し、極限を ${L}$ に等しくおく。" if al != 0 else
                  f"分母 $\\to0$ で極限が有限なので、分子 $\\to0$ が必要で $b=0$。このとき $\\dfrac{{x^2+ax}}{{x}}=x+a\\to a$ より $a={L}$。", d=3,
                  ap="$x\\to" + str(al) + "$ で分母 $\\to0$ なのに極限が有限の値になるには、分子も $0$ に近づかなければならない（必要条件）。そこから $a,\\ b$ の関係を出し、実際に極限を計算して決める。",
                  steps=[f"$\\displaystyle\\lim_{{x\\to {al}}}({den})=0$ で極限が有限なので、$\\displaystyle\\lim_{{x\\to {al}}}(x^2+ax+b)=0$ が必要。よって " + ("$b=0$。" if al == 0 else f"${al * al}{'+' if al > 0 else '-'}{'' if abs(al) == 1 else abs(al)}a+b=0$。"),
                         f"$b={-al * al}{'-' if al > 0 else '+'}{'' if abs(al) == 1 else abs(al)}a$ を代入すると、分子は $({xp(-al)})(x+a{'+' if al > 0 else '-'}{abs(al)})$ と因数分解できる。" if al != 0 else "$b=0$ のとき分子は $x(x+a)$。",
                         f"約分して $x+a{tf_(al)}\\to " + (f"{2 * al}+a" if al != 0 else "a") + f"$。これが ${L}$ に等しいので $a={a}$、$b={b}$。",
                         f"（逆に $a={a},\\ b={b}$ のとき $\\dfrac{{({xp(-al)})({xp(-be)})}}{{{den}}}={xp(-be)}\\to {L}$ となり、条件を満たす。）"],
                  alt=[f"極限値が ${L}$ なので、分子は $({xp(-al)})({xp(-be)})$ の形でなければならない、と因数から直接考えてもよい。"],
                  pc=[("分子 $\\to0$ が必要であることを述べている", 1), ("約分して極限を計算している", 1), ("$a,\\ b$ が正しく、十分性を確認している", 2)],
                  pit=["「分子 $\\to0$」という必要条件に気づかず、手が止まる。", "求めた $a,\\ b$ で本当に極限が成り立つか（十分性）を確かめない。"],
                  chk=(f"[({al})**2+({a})*({al})+({b}), limit((x**2+({a})*x+({b}))/(x-({al})), x, {al})]", f"[0, {L}]", None, "intermediate"))
    s = r.randint(1, 4)
    k = r.randint(-3, 6)
    c = s * s - k
    a = nonzero(r, -6, 6)
    L = F(a, 2 * s)
    b = a * s
    return sa(f"等式 ${LIM('x', c)}\\dfrac{{a\\sqrt{{{xp(k)}}}-b}}{{{xp(-c)}}}={ft(L)}$ が成り立つように、定数 $a,\\ b$ の値を定めなさい。", f"$a={a},\\ b={b}$",
              f"分子 $\\to0$ が必要なので $b={s}a$。有理化して極限を計算すると $\\dfrac{{a}}{{{2 * s}}}$ となり、これが ${ft(L)}$ に等しい。", d=3,
              ap="分母 $\\to0$ で極限が有限なので、分子 $\\to0$ が必要。$b$ を $a$ で表してから有理化する。",
              steps=[f"$\\displaystyle\\lim_{{x\\to {c}}}({xp(-c)})=0$ なので、$\\displaystyle\\lim_{{x\\to {c}}}(a\\sqrt{{{xp(k)}}}-b)=0$ が必要。$\\sqrt{{{c}{tf_(k)}}}={s}$ より $b={s}a$。",
                     f"このとき $\\dfrac{{a(\\sqrt{{{xp(k)}}}-{s})}}{{{xp(-c)}}}=\\dfrac{{a}}{{\\sqrt{{{xp(k)}}}+{s}}}$（分子を有理化して約分）。",
                     f"$x\\to {c}$ として $\\dfrac{{a}}{{{2 * s}}}={ft(L)}$ より $a={a}$、$b={b}$。"],
              alt=[f"$a={a},\\ b={b}$ を代入し、$x={c}$ に近い値で電卓計算して ${ft(L)}$ に近いことを確かめる。"],
              pc=[("分子 $\\to0$ から $b$ を $a$ で表している", 1), ("有理化して極限を計算している", 1), ("$a,\\ b$ が正しい", 2)],
              pit=["有理化の際に係数 $a$ を落とす。", "必要条件だけで $a,\\ b$ を決めようとして、もう1つの式が立たない。"],
              chk=(f"[({a})*sqrt({c}+({k}))-({b}), limit((({a})*sqrt(x+({k}))-({b}))/(x-({c})), x, {c})]", f"[0, {fp(L)}]", None, "intermediate"))


@gen("standard_practice", 4, ["computation", "condition_check"])
def one_sided(r):
    kind = r.choice(["neg_sqrt", "neg_ratio", "side", "abs"])
    if kind == "neg_sqrt":
        a = nonzero(r, -8, 8)
        b = r.randint(-4, 4)
        L = F(-a, 2)
        tex = f"(\\sqrt{{x^2{'+' if a > 0 else ''}{co(a, 'x')}{tf_(b)}}}+x)"
        return sa(f"極限 ${LIM('x', '-\\infty')}{tex}$ を求めなさい。", f"${ft(L)}$",
                  f"$x=-t$ とおくと $t\\to\\infty$ で $\\sqrt{{t^2{'-' if a > 0 else '+'}{co(abs(a), 't')}{tf_(b)}}}-t\\to {ft(L)}$。", d=3,
                  ap="$x\\to-\\infty$ では $x<0$ なので $\\sqrt{x^2}=-x$。$x=-t$ と置きかえて $t\\to\\infty$ の極限に直すと安全である。",
                  steps=[f"$x=-t$ とおくと、$x\\to-\\infty$ のとき $t\\to\\infty$。", f"式は $\\sqrt{{t^2{'-' if a > 0 else '+'}{co(abs(a), 't')}{tf_(b)}}}-t$。",
                         f"有理化して $\\dfrac{{{co(-a, 't')}{tf_(b)}}}{{\\sqrt{{t^2{'-' if a > 0 else '+'}{co(abs(a), 't')}{tf_(b)}}}+t}}$、分子・分母を $t$ で割って $t\\to\\infty$ とすると $\\dfrac{{{-a}}}{{2}}={ft(L)}$。"],
                  alt=["$x<0$ のとき $\\sqrt{x^2+\\cdots}=|x|\\sqrt{1+\\cdots}=-x\\sqrt{1+\\cdots}$ として、置きかえずに計算してもよい。"],
                  pc=[("$x=-t$ の置きかえ（または $\\sqrt{x^2}=-x$）を正しく扱っている", 2), ("有理化して計算している", 1), ("極限が正しい", 1)],
                  pit=[f"$x>0$ のときと同じように計算して $\\dfrac{{{a}}}{{2}}$ と答える（符号の誤り）。", "$\\sqrt{x^2}=x$ としてしまう。"],
                  chk=(f"limit(sqrt(x**2+({a})*x+({b}))+x, x, -oo)", fp(L)))
    if kind == "neg_ratio":
        a = nonzero(r, -5, 5)
        b = r.randint(-5, 5)
        c = r.randint(1, 9)
        L = F(-a)
        return sa(f"極限 ${LIM('x', '-\\infty')}\\dfrac{{{co(a, 'x')}{tf_(b)}}}{{\\sqrt{{x^2+{c}}}}}$ を求めなさい。", f"${ft(L)}$",
                  f"$x<0$ のとき $\\sqrt{{x^2+{c}}}=-x\\sqrt{{1+\\dfrac{{{c}}}{{x^2}}}}$。分子・分母を $-x$ で割ると極限は ${ft(L)}$。", d=3,
                  ap="$x\\to-\\infty$ のときは $x<0$ なので、$\\sqrt{x^2}=|x|=-x$。分子・分母を $-x\\ (>0)$ で割る。",
                  steps=[f"$x<0$ より $\\sqrt{{x^2+{c}}}=\\sqrt{{x^2}}\\sqrt{{1+\\dfrac{{{c}}}{{x^2}}}}=-x\\sqrt{{1+\\dfrac{{{c}}}{{x^2}}}}$。",
                         f"分子・分母を $-x$ で割ると $\\dfrac{{{-a}{'' if b == 0 else ('-' if b > 0 else '+') + '\\dfrac{' + str(abs(b)) + '}{x}'}}}{{\\sqrt{{1+\\dfrac{{{c}}}{{x^2}}}}}}$。",
                         f"$x\\to-\\infty$ として ${ft(L)}$。"],
                  alt=["$x=-t$ と置きかえると $\\dfrac{" + co(-a, 't') + tf_(b) + "}{\\sqrt{t^2+" + str(c) + "}}\\ (t\\to\\infty)$ となり、同じ結果が得られる。"],
                  pc=[("$\\sqrt{x^2}=-x$ を正しく扱っている", 2), ("極限が正しい", 2)],
                  pit=[f"$x$ で割って $\\sqrt{{x^2+{c}}}$ を $\\sqrt{{1+\\dfrac{{{c}}}{{x^2}}}}$ としてしまい、${a}$ と答える。"],
                  chk=(f"limit((({a})*x+({b}))/sqrt(x**2+{c}), x, -oo)", fp(L)))
    if kind == "side":
        al = r.randint(-4, 4)
        be = r.randint(-5, 5)
        while al + be == 0:
            be = r.randint(-5, 5)
        s = 1 if al + be > 0 else -1
        f = f"\\dfrac{{{xp(be)}}}{{{xp(-al)}}}"
        right_ = "\\infty" if s > 0 else "-\\infty"
        left_ = "-\\infty" if s > 0 else "\\infty"
        return sa(f"関数 $f(x)={f}$ について、右側極限 $\\displaystyle\\lim_{{x\\to {al}+0}}f(x)$ と左側極限 $\\displaystyle\\lim_{{x\\to {al}-0}}f(x)$ を求めなさい。また、$\\displaystyle\\lim_{{x\\to {al}}}f(x)$ は存在するか答えなさい。",
                  f"右側極限 ${right_}$、左側極限 ${left_}$。左右が一致しないので $\\displaystyle\\lim_{{x\\to {al}}}f(x)$ は存在しない",
                  f"$x\\to {al}$ のとき分子 $\\to {al + be}$、分母 $\\to0$。分母の符号は $x>{al}$ で正、$x<{al}$ で負。", d=3,
                  ap="分母 $\\to0$、分子 $\\to$（$0$ でない定数）のときは発散する。符号は分子の極限の符号と、分母が正負どちらから $0$ に近づくかで決まる。",
                  steps=[f"$x\\to {al}$ のとき、分子 ${xp(be)}\\to {al + be}$（{'正' if s > 0 else '負'}）。",
                         f"$x\\to {al}+0$ では分母 ${xp(-al)}>0$ で $0$ に近づくので、$f(x)\\to {right_}$。", f"$x\\to {al}-0$ では分母 $<0$ で $0$ に近づくので、$f(x)\\to {left_}$。",
                         "左右の極限が一致しないので、極限は存在しない。"],
                  alt=[f"$f(x)=1+\\dfrac{{{al + be}}}{{{xp(-al)}}}$ と変形すると、$y=\\dfrac{{{al + be}}}{{x}}$ のグラフを平行移動した直角双曲線と分かり、漸近線 $x={al}$ の左右で行き先が逆になる。"],
                  pc=[("右側極限が正しい", 1), ("左側極限が正しい", 1), ("極限が存在しないと正しく結論している", 2)],
                  pit=["左右を区別せず「$\\infty$」とだけ答える。", "分子の符号を考えずに右側極限を $\\infty$ と決めつける。"],
                  chk=(f"[atan(limit(({xp(be)})/(x-({al})), x, {al}, \"+\")), atan(limit(({xp(be)})/(x-({al})), x, {al}, \"-\"))]",
                       f"[{s}*pi/2, {-s}*pi/2]", None, "intermediate"))
    a = nonzero(r, -6, 6)
    k = r.choice([1, 2, 3])
    num = f"x^2{'+' if a > 0 else '-'}{'' if abs(a) == 1 else abs(a)}x" if k == 1 else f"{k}x^2{'+' if a > 0 else '-'}{'' if abs(a) == 1 else abs(a)}x"
    return sa(f"関数 $f(x)=\\dfrac{{{num}}}{{|x|}}$ について、$\\displaystyle\\lim_{{x\\to+0}}f(x)$ と $\\displaystyle\\lim_{{x\\to-0}}f(x)$ を求めなさい。また、$\\displaystyle\\lim_{{x\\to0}}f(x)$ は存在するか答えなさい。",
              f"$\\displaystyle\\lim_{{x\\to+0}}f(x)={a}$、$\\displaystyle\\lim_{{x\\to-0}}f(x)={-a}$。一致しないので $\\displaystyle\\lim_{{x\\to0}}f(x)$ は存在しない",
              f"$x>0$ では $|x|=x$ で $f(x)={co(k, 'x')}{tf_(a)}$、$x<0$ では $|x|=-x$ で $f(x)={co(-k, 'x')}{tf_(-a)}$。", d=3,
              ap="絶対値は中身の符号で場合分けする。$x\\to+0$ では $x>0$、$x\\to-0$ では $x<0$ として $|x|$ を外す。",
              steps=[f"$x>0$ のとき $f(x)=\\dfrac{{x({co(k, 'x')}{tf_(a)})}}{{x}}={co(k, 'x')}{tf_(a)}\\to {a}$。", f"$x<0$ のとき $f(x)=\\dfrac{{x({co(k, 'x')}{tf_(a)})}}{{-x}}={co(-k, 'x')}{tf_(-a)}\\to {-a}$。",
                     f"${a}\\neq {-a}$ なので、$x\\to0$ の極限は存在しない。"],
              alt=["$y=f(x)$ のグラフをかくと、$x=0$ の左右で2本の直線に分かれ、$y$ 軸上での高さが異なることが分かる。"],
              pc=[("$x\\to+0$ の極限が正しい", 1), ("$x\\to-0$ の極限が正しい", 1), ("極限が存在しないと結論している", 2)],
              pit=["$|x|$ をそのまま $x$ として約分してしまう。"],
              chk=(f"[limit(({k}*x**2+({a})*x)/Abs(x), x, 0, \"+\"), limit(({k}*x**2+({a})*x)/Abs(x), x, 0, \"-\")]", f"[{a}, {-a}]", None, "intermediate"))


# ======================================================================
# C 思考力・記述応用
# ======================================================================

@gen("thinking_writing", 3, ["written_reasoning", "concept"])
def squeeze(r):
    kind = r.choice(["sin_n", "floor", "root", "root3", "xsin"])
    rub = [("適切な不等式を根拠とともに立てている", 3), ("両側の極限を正しく求めている", 3), ("はさみうちの原理により結論を述べている", 2)]
    pc = [("不等式", 3), ("両側の極限", 3), ("結論", 2)]
    if kind == "sin_n":
        a, b, c, d = nonzero(r, -5, 5), nonzero(r, -4, 4), r.randint(1, 4), r.randint(0, 5)
        fn = r.choice(["sin", "cos"])
        L = F(a, c)
        B = abs(b)
        stem = f"極限 ${LIM()}\\dfrac{{{co(a, 'n')}{'+' if b > 0 else '-'}{'' if B == 1 else B}\\{fn} n}}{{{co(c, 'n')}{tf_(d)}}}$ を求めなさい。求め方も示すこと。"
        steps = [f"$-1\\leqq\\{fn} n\\leqq1$ より、${co(a, 'n')}-{B}\\leqq {co(a, 'n')}{'+' if b > 0 else '-'}{'' if B == 1 else B}\\{fn} n\\leqq {co(a, 'n')}+{B}$。",
                 f"各辺を ${co(c, 'n')}{tf_(d)}\\ (>0)$ で割ると $\\dfrac{{{co(a, 'n')}-{B}}}{{{co(c, 'n')}{tf_(d)}}}\\leqq(\\text{{与式}})\\leqq\\dfrac{{{co(a, 'n')}+{B}}}{{{co(c, 'n')}{tf_(d)}}}$。",
                 f"両端はともに $n\\to\\infty$ で $\\dfrac{{{a}}}{{{c}}}={ft(L)}$ に収束する。", f"はさみうちの原理より、極限は ${ft(L)}$。"]
        chk = (f"[limit(({a}*n-{B})/({c}*n+{d}), n, oo), limit(({a}*n+{B})/({c}*n+{d}), n, oo)]", f"[{fp(L)}, {fp(L)}]", None, "intermediate")
        ap = f"$\\{fn} n$ は振動して極限をもたないが、$-1\\leqq\\{fn} n\\leqq1$ で上下から押さえられる。不等式を作ってはさみうちの原理を使う。"
        alt = [f"分子・分母を $n$ で割ると $\\dfrac{{{a}{'+' if b > 0 else '-'}{B}\\cdot\\dfrac{{\\{fn} n}}{{n}}}}{{{c}{'' if d == 0 else '+' + '\\dfrac{' + str(d) + '}{n}'}}}$。$\\left|\\dfrac{{\\{fn} n}}{{n}}\\right|\\leqq\\dfrac{{1}}{{n}}\\to0$ を示してもよい。"]
        ans = f"${ft(L)}$"
    elif kind == "floor":
        a, b = r.randint(2, 9), r.randint(1, 5)
        while a == b:
            b = r.randint(1, 5)
        L = F(a, b)
        stem = f"実数 $x$ に対して、$x$ を超えない最大の整数を $[x]$ で表す。極限 ${LIM('x', '\\infty')}\\dfrac{{[{a}x]}}{{{co(b, 'x')}}}$ を求めなさい。求め方も示すこと。"
        steps = [f"$[x]$ の定義より ${a}x-1<[{a}x]\\leqq {a}x$。", f"$x>0$ のとき各辺を ${co(b, 'x')}$ で割ると $\\dfrac{{{a}x-1}}{{{co(b, 'x')}}}<\\dfrac{{[{a}x]}}{{{co(b, 'x')}}}\\leqq\\dfrac{{{a}}}{{{b}}}$。",
                 f"$x\\to\\infty$ のとき左端は $\\dfrac{{{a}}}{{{b}}}-\\dfrac{{1}}{{{co(b, 'x')}}}\\to {ft(L)}$。", f"はさみうちの原理より、極限は ${ft(L)}$。"]
        chk = (f"[limit(({a}*x-1)/({b}*x), x, oo), Rational({a},{b})]", f"[{fp(L)}, {fp(L)}]", None, "intermediate")
        ap = "ガウス記号は $t-1<[t]\\leqq t$ という不等式で扱う。これで上下からはさむ。"
        alt = [f"$[{a}x]={a}x-\\theta\\ (0\\leqq\\theta<1)$ とおくと $\\dfrac{{[{a}x]}}{{{co(b, 'x')}}}=\\dfrac{{{a}}}{{{b}}}-\\dfrac{{\\theta}}{{{co(b, 'x')}}}$ で、第2項 $\\to0$ と示してもよい。"]
        ans = f"${ft(L)}$"
    elif kind in ("root", "root3"):
        if kind == "root":
            a, b = sorted(r.sample(range(2, 10), 2))
            bases = [a, b]
        else:
            bases = sorted(r.sample(range(2, 10), 3))
        b = bases[-1]
        m = len(bases)
        inner = "+".join(f"{x}^n" for x in bases)
        stem = f"極限 ${LIM()}({inner})^{{\\frac{{1}}{{n}}}}$ を求めなさい。求め方も示すこと。"
        steps = [f"${',\\ '.join(str(x) for x in bases[:-1])}$ はいずれも $0$ より大きく ${b}$ より小さいので、${b}^n<{inner}<{m}\\cdot {b}^n$。",
                 f"各辺を $\\dfrac{{1}}{{n}}$ 乗すると ${b}<({inner})^{{\\frac{{1}}{{n}}}}<{m}^{{\\frac{{1}}{{n}}}}\\cdot {b}$。",
                 f"$n\\to\\infty$ のとき ${m}^{{\\frac{{1}}{{n}}}}\\to1$ なので、右端は ${b}$ に収束する。", f"はさみうちの原理より、極限は ${b}$。"]
        chk = (f"[{b}, limit({m}**(1/n)*{b}, n, oo), limit(({'+'.join(f'{x}**n' for x in bases)})**(1/n), n, oo)]", f"[{b}, {b}, {b}]", None, "intermediate")
        ap = "最も大きい底 $" + str(b) + "^n$ が全体を支配する。和を $" + str(b) + "^n$ と $" + str(m) + "\\cdot" + str(b) + "^n$ ではさみ、$\\dfrac{1}{n}$ 乗する。"
        alt = [f"$({inner})^{{\\frac{{1}}{{n}}}}={b}\\left(" + "+".join(f"\\left(\\dfrac{{{x}}}{{{b}}}\\right)^n" for x in bases[:-1]) + "+1\\right)^{\\frac{1}{n}}$ と変形し、かっこの中が $1$ と $" + str(m) + "$ の間にあることを使ってもよい。"]
        ans = f"${b}$"
    else:
        mexp = r.randint(1, 3)
        kk = r.randint(1, 5)
        cc = r.randint(1, 4)
        fn = r.choice(["sin", "cos"])
        xm = "x" if mexp == 1 else f"x^{mexp}"
        km = "" if kk == 1 else str(kk)
        stem = f"極限 ${LIM('x', 0)}{km}{xm}\\{fn}\\dfrac{{{cc}}}{{x}}$ を求めなさい。求め方も示すこと。"
        absx = f"|x|^{mexp}" if mexp != 2 else "x^2"
        steps = [f"$x\\neq0$ のとき $\\left|\\{fn}\\dfrac{{{cc}}}{{x}}\\right|\\leqq1$ なので、$0\\leqq\\left|{km}{xm}\\{fn}\\dfrac{{{cc}}}{{x}}\\right|\\leqq {km}{absx}$。",
                 f"$x\\to0$ のとき ${km}{absx}\\to0$。", "はさみうちの原理より $\\left|(\\text{与式})\\right|\\to0$、よって極限は $0$。"]
        chk = (f"[limit({kk}*Abs(x)**{mexp}, x, 0), limit(-{kk}*Abs(x)**{mexp}, x, 0)]", "[0, 0]", None, "intermediate")
        ap = f"$\\{fn}\\dfrac{{{cc}}}{{x}}$ は $x\\to0$ で振動して極限をもたないが、絶対値は $1$ 以下。絶対値をとってはさむ。"
        alt = ["$-" + km + absx + "\\leqq" + km + xm + "\\" + fn + "\\dfrac{" + str(cc) + "}{x}\\leqq" + km + absx + "$ と、絶対値を使わずに上下からはさんでもよい。"]
        ans = "$0$"
    return desc(stem, ans, "はさみうちの原理を用いる。", rub, d=4, p=8, lines=8, ap=ap, steps=steps, alt=alt, pc=pc,
                pit=["振動する部分（$\\sin$、ガウス記号など）の極限を勝手に決めてしまう。", "不等式で割る数の符号を確かめず、不等号の向きを誤る。"], chk=chk)


@gen("thinking_writing", 3, ["cross_unit", "application", "written_reasoning"])
def series_figure(r):
    kind = r.choice(["tri", "tri", "sq", "sq", "ball", "ball"])
    rub = [("図形（運動）の規則から公比を正しく求めている", 3), ("無限等比級数として式を立て、収束を確認している", 3), ("和が正しい", 2)]
    pc = [("公比", 3), ("立式と収束の確認", 3), ("答え", 2)]
    if kind == "tri":
        a = r.randint(2, 12)
        what = r.choice(["area", "peri"])
        if what == "area":
            S = sp.sqrt(3) * a * a / 3
            stem = f"1辺の長さが ${a}$ の正三角形 $T_1$ がある。$T_1$ の3辺の中点を結んでできる正三角形を $T_2$、$T_2$ の3辺の中点を結んでできる正三角形を $T_3$ とし、以下同様に $T_4,\\ T_5,\\ \\cdots$ をつくる。$T_1,\\ T_2,\\ T_3,\\ \\cdots$ の面積の総和を求めなさい。"
            steps = [f"$T_1$ の面積は $\\dfrac{{1}}{{2}}\\cdot {a}^2\\sin 60^\\circ=\\dfrac{{\\sqrt{{3}}}}{{4}}\\cdot {a * a}$。", "中点を結ぶと辺の長さは $\\dfrac{1}{2}$ 倍（中点連結定理）になるので、面積は $\\dfrac{1}{4}$ 倍になる。",
                     f"面積は初項 $\\dfrac{{{a * a}\\sqrt{{3}}}}{{4}}$、公比 $\\dfrac{{1}}{{4}}$ の無限等比級数で、$\\left|\\dfrac{{1}}{{4}}\\right|<1$ より収束する。",
                     f"総和は $\\dfrac{{\\frac{{{a * a}\\sqrt{{3}}}}{{4}}}}{{1-\\frac{{1}}{{4}}}}={sp.latex(S).replace(chr(92) + 'frac', chr(92) + 'dfrac')}$。"]
            chk = (f"summation(sqrt(3)/4*{a * a}*Rational(1,4)**(n-1), [n, 1, oo])", sp.sstr(S))
        else:
            S = sp.Integer(6 * a)
            stem = f"1辺の長さが ${a}$ の正三角形 $T_1$ がある。$T_1$ の3辺の中点を結んでできる正三角形を $T_2$ とし、以下同様に $T_3,\\ T_4,\\ \\cdots$ をつくる。$T_1,\\ T_2,\\ T_3,\\ \\cdots$ の周の長さの総和を求めなさい。"
            steps = ["中点連結定理より、$T_{n+1}$ の1辺の長さは $T_n$ の $\\dfrac{1}{2}$ 倍。", f"周の長さは初項 ${3 * a}$、公比 $\\dfrac{{1}}{{2}}$ の無限等比級数で、収束する。",
                     f"総和は $\\dfrac{{{3 * a}}}{{1-\\frac{{1}}{{2}}}}={6 * a}$。"]
            chk = (f"summation({3 * a}*Rational(1,2)**(n-1), [n, 1, oo])", str(6 * a))
        rel = ["HS-MATH1-U04"]
        ap = "中点を結ぶと相似比 $\\dfrac{1}{2}$ の相似な三角形ができる。長さは $\\dfrac{1}{2}$ 倍、面積は $\\left(\\dfrac{1}{2}\\right)^2$ 倍で、無限等比級数になる。"
        alt = ["$T_1$ は $T_2$ と合同な4つの三角形に分かれることから、面積比 $\\dfrac{1}{4}$ を図で確かめられる。"]
    elif kind == "sq":
        a = r.randint(2, 10)
        what = r.choice(["area", "peri"])
        if what == "area":
            S = sp.Integer(2 * a * a)
            stem = f"1辺の長さが ${a}$ の正方形 $Q_1$ がある。$Q_1$ の4辺の中点を順に結んでできる正方形を $Q_2$ とし、以下同様に $Q_3,\\ Q_4,\\ \\cdots$ をつくる。$Q_1,\\ Q_2,\\ Q_3,\\ \\cdots$ の面積の総和を求めなさい。"
            steps = [f"$Q_n$ の1辺を $l$ とすると、$Q_{{n+1}}$ の1辺は直角をはさむ2辺が $\\dfrac{{l}}{{2}}$ の直角二等辺三角形の斜辺で $\\dfrac{{l}}{{\\sqrt{{2}}}}$。",
                     "よって面積は $\\dfrac{1}{2}$ 倍になる。", f"面積は初項 ${a * a}$、公比 $\\dfrac{{1}}{{2}}$ の無限等比級数で、収束する。", f"総和は $\\dfrac{{{a * a}}}{{1-\\frac{{1}}{{2}}}}={2 * a * a}$。"]
            chk = (f"summation({a * a}*Rational(1,2)**(n-1), [n, 1, oo])", str(2 * a * a))
        else:
            S = 4 * a * (2 + sp.sqrt(2))
            stem = f"1辺の長さが ${a}$ の正方形 $Q_1$ がある。$Q_1$ の4辺の中点を順に結んでできる正方形を $Q_2$ とし、以下同様に $Q_3,\\ Q_4,\\ \\cdots$ をつくる。$Q_1,\\ Q_2,\\ Q_3,\\ \\cdots$ の周の長さの総和を求めなさい。"
            steps = ["三平方の定理より、$Q_{n+1}$ の1辺は $Q_n$ の1辺の $\\dfrac{1}{\\sqrt{2}}$ 倍。", f"周の長さは初項 ${4 * a}$、公比 $\\dfrac{{1}}{{\\sqrt{{2}}}}$ の無限等比級数で、$\\dfrac{{1}}{{\\sqrt{{2}}}}<1$ より収束する。",
                     f"総和は $\\dfrac{{{4 * a}}}{{1-\\frac{{1}}{{\\sqrt{{2}}}}}}=\\dfrac{{{4 * a}\\sqrt{{2}}}}{{\\sqrt{{2}}-1}}={4 * a}\\sqrt{{2}}(\\sqrt{{2}}+1)={8 * a}+{4 * a}\\sqrt{{2}}$。"]
            chk = (f"summation({4 * a}*(1/sqrt(2))**(n-1), [n, 1, oo])", sp.sstr(S))
        rel = ["HS-MATH1-U04"]
        ap = "新しい正方形の1辺は、もとの正方形の角にできる直角二等辺三角形の斜辺。長さの比（公比）を三平方の定理で求める。"
        alt = ["$Q_2$ の面積は、$Q_1$ から四すみの直角二等辺三角形4つを除いたもので、$Q_1$ の半分になることを図で確かめられる。"]
    else:
        h = r.choice([1, 2, 3, 4, 5, 6, 8, 10])
        rt = r.choice([F(1, 2), F(1, 3), F(2, 3), F(3, 4), F(3, 5), F(4, 5), F(2, 5)])
        S = F(h) * (1 + rt) / (1 - rt)
        stem = f"高さ ${h}$ m の位置から静かに落としたボールが、床で跳ね返るたびに、直前に落下した高さの ${ft(rt)}$ 倍の高さまで上がるものとする。ボールが静止するまでに上下に動く距離の総和を求めなさい。ただし、ボールの大きさと空気抵抗は考えないものとする。"
        steps = [f"最初の落下は ${h}$ m。", f"1回目に跳ね返って上がる高さは ${h}\\times {ft(rt)}$ m で、同じ距離を落ちるので往復 $2\\times {h}\\times {ft(rt)}$ m。",
                 f"以後の往復の距離は初項 ${ft(2 * h * rt)}$、公比 ${ft(rt)}$ の無限等比級数で、$0<{ft(rt)}<1$ より収束する。",
                 f"総和は ${h}+\\dfrac{{{ft(2 * h * rt)}}}{{1-{ft(rt)}}}={ft(S)}$（m）。"]
        chk = (f"{h}+summation({fp(2 * h * rt)}*({fp(rt)})**(n-1), [n, 1, oo])", fp(S))
        rel = ["HS-PHYB-U01"]
        ap = "最初の落下だけは片道。2回目以降は「上がって落ちる」往復で、その距離が一定の比で小さくなる無限等比級数になる。"
        alt = [f"全体を $\\dfrac{{1+r}}{{1-r}}h$（$r$ は跳ね返りの比）とまとめた式に $r={ft(rt)},\\ h={h}$ を代入しても同じ値になる。"]
        S = sp.Rational(S.numerator, S.denominator)
    if kind == "sq" and not S.is_Integer:
        ans = f"${8 * a}+{4 * a}\\sqrt{{2}}$"
    else:
        ans = f"${sp.latex(S).replace(chr(92) + 'frac', chr(92) + 'dfrac')}$" + ("（m）" if kind == "ball" else "")
    return desc(stem, ans, "相似な図形（または一定の比での運動）の繰り返しを無限等比級数として表す。", rub, d=4, p=8, lines=8,
                ap=ap, steps=steps, alt=alt, pc=pc, rel=rel,
                pit=["最初の項（$T_1$ や最初の落下）を入れ忘れる。", "長さの比と面積の比を取り違える。" if kind != "ball" else "2回目以降の往復を片道分しか数えない。"], chk=chk)


@gen("thinking_writing", 2, ["condition_check", "written_reasoning"])
def continuity_param(r):
    while True:
        k, d, e = nonzero(r, -3, 3), r.randint(-3, 3), r.randint(-4, 4)
        if d - e != 0:
            break
    a_, b_ = d - e, k
    num = f"{co(k, 'x^{2n+1}')}{'' if d == 0 else ('+' if d > 0 else '-') + ('' if abs(d) == 1 else str(abs(d))) + 'x^{2n}'}+ax^2+bx{tf_(e)}"
    g_tex = f"{co(k, 'x')}{tf_(d)}"
    h_tex = f"ax^2+bx{tf_(e)}"
    return desc(f"関数 $f(x)={LIM()}\\dfrac{{{num}}}{{x^{{2n}}+1}}$ がすべての実数 $x$ で連続となるように、定数 $a,\\ b$ の値を定めなさい。",
                f"$a={a_},\\ b={b_}$",
                f"$|x|>1$ では $f(x)={g_tex}$、$|x|<1$ では $f(x)={h_tex}$、$x=\\pm1$ では2つの式の平均。$x=\\pm1$ で連続となる条件を立てる。",
                [("$|x|<1,\\ |x|>1,\\ x=\\pm1$ に分けて $f(x)$ を求めている", 3), ("$x=1,\\ -1$ での連続の条件を立てている", 3), ("$a,\\ b$ の値が正しい", 2)],
                d=5, p=8, lines=10,
                ap="$x^{2n}$ の極限は $|x|<1$ で $0$、$|x|=1$ で $1$、$|x|>1$ で $\\infty$。場合分けして $f(x)$ を求め、境目 $x=\\pm1$ での連続性を調べる。",
                steps=[f"$|x|<1$ のとき $x^{{2n}}\\to0$ なので $f(x)={h_tex}$。",
                       f"$|x|>1$ のとき分子・分母を $x^{{2n}}$ で割ると $\\dfrac{{\\left({g_tex}\\right)+\\dfrac{{{h_tex}}}{{x^{{2n}}}}}}{{1+\\dfrac{{1}}{{x^{{2n}}}}}}\\to {g_tex}$。",
                       f"$x=1$ のとき $f(1)=\\dfrac{{{k + d}+a+b{tf_(e)}}}{{2}}$、$x=-1$ のとき $f(-1)=\\dfrac{{{-k + d}+a-b{tf_(e)}}}{{2}}$。",
                       f"$x=1$ で連続 $\\iff$ 左右の極限 $a+b{tf_(e)}$ と ${k + d}$ が等しい（このとき $f(1)$ も同じ値）。$x=-1$ でも同様に $a-b{tf_(e)}={-k + d}$。",
                       f"連立して $a={a_},\\ b={b_}$。（$|x|\\neq1$ では多項式なので連続。）"],
                alt=[f"$a={a_},\\ b={b_}$ を代入し、$x=1$ の左右の極限と $f(1)$ がすべて ${k + d}$ になることを確かめる。"],
                pc=[("場合分け", 3), ("連続の条件", 3), ("答え", 2)],
                pit=["$x=\\pm1$ のときの値を求めずに、$|x|<1$ と $|x|>1$ の式をつなげるだけで終える。", "$|x|>1$ で $x^{2n}$ で割ることに気づかず、$\\infty$ のまま扱う。"],
                chk=(f"solve([a+b+({e})-({k + d}), a-b+({e})-({d - k})], [a, b])", f"{{a: {a_}, b: {b_}}}", None, "intermediate"))


@gen("thinking_writing", 2, ["written_reasoning", "condition_check"])
def ivt(r):
    kind = r.choice(["cubic", "cubic", "exp", "cos"])
    rub = [("関数が区間で連続であることを述べている", 2), ("区間の両端の値の符号を調べている", 3), ("中間値の定理により結論を述べている", 3)]
    pc = [("連続性", 2), ("符号の確認", 3), ("結論", 3)]
    if kind == "cubic":
        while True:
            p, q = r.randint(-6, 6), r.randint(-9, 9)
            m = r.randint(-3, 2)
            f0, f1 = m ** 3 + p * m + q, (m + 1) ** 3 + p * (m + 1) + q
            if f0 * f1 < 0:
                break
        ftex = f"x^3{'' if p == 0 else ('+' if p > 0 else '-') + ('' if abs(p) == 1 else str(abs(p))) + 'x'}{tf_(q)}"
        stem = f"方程式 ${ftex}=0$ は ${m}<x<{m + 1}$ の範囲に少なくとも1つの実数解をもつことを示しなさい。"
        steps = [f"$f(x)={ftex}$ とおく。$f(x)$ は多項式関数なので、${m}\\leqq x\\leqq {m + 1}$ で連続である。",
                 f"$f({m})={f0}$、$f({m + 1})={f1}$ で、$f({m})f({m + 1})<0$。", f"中間値の定理より、$f(c)=0$ となる $c$ が ${m}<c<{m + 1}$ に少なくとも1つ存在する。"]
        chk = (f"[({m})**3+({p})*({m})+({q}), ({m + 1})**3+({p})*({m + 1})+({q})]", f"[{f0}, {f1}]", None, "intermediate")
    elif kind == "exp":
        while True:
            base = r.choice([2, 3])
            k = r.randint(3, 20)
            m = r.randint(0, 3)
            f0, f1 = base ** m + m - k, base ** (m + 1) + m + 1 - k
            if f0 < 0 < f1:
                break
        stem = f"方程式 ${base}^x+x={k}$ は ${m}<x<{m + 1}$ の範囲に少なくとも1つの実数解をもつことを示しなさい。"
        steps = [f"$f(x)={base}^x+x-{k}$ とおく。指数関数と多項式関数の和なので、$f(x)$ は ${m}\\leqq x\\leqq {m + 1}$ で連続である。",
                 f"$f({m})={base}^{{{m}}}+{m}-{k}={f0}<0$、$f({m + 1})={base}^{{{m + 1}}}+{m + 1}-{k}={f1}>0$。",
                 f"中間値の定理より、$f(c)=0$ となる $c$ が ${m}<c<{m + 1}$ に少なくとも1つ存在する。"]
        chk = (f"[{base}**{m}+{m}-{k}, {base}**{m + 1}+{m + 1}-{k}]", f"[{f0}, {f1}]", None, "intermediate")
    else:
        c = r.randint(1, 3)
        cx = "x" if c == 1 else f"{c}x"
        stem = f"方程式 $\\cos x={cx}$ は $0<x<\\dfrac{{\\pi}}{{2}}$ の範囲に少なくとも1つの実数解をもつことを示しなさい。"
        steps = [f"$f(x)=\\cos x-{cx}$ とおくと、$f(x)$ は $0\\leqq x\\leqq\\dfrac{{\\pi}}{{2}}$ で連続である。",
                 f"$f(0)=1>0$、$f\\left(\\dfrac{{\\pi}}{{2}}\\right)=-{'' if c == 1 else c}\\dfrac{{\\pi}}{{2}}<0$。",
                 "中間値の定理より、$f(c)=0$ となる $c$ が $0<c<\\dfrac{\\pi}{2}$ に少なくとも1つ存在する。"]
        chk = (f"[cos(0)-0, cos(pi/2)-{c}*pi/2]", f"[1, -{c}*pi/2]", None, "intermediate")
    return desc(stem, "（証明）" + "".join(s for s in steps) + "（証明終）", "中間値の定理を用いる。", rub, d=4, p=8, lines=8,
                ap="中間値の定理の2つの前提「区間で連続」「両端の値が異符号」を確認すれば、解の存在が言える。",
                steps=steps, alt=["$y=f(x)$ のグラフが区間の両端で $x$ 軸の上下に分かれ、途切れずにつながっているので $x$ 軸と交わる、と図で説明してもよい（答案では定理の名前と前提を書く）。"],
                pc=pc, pit=["「連続である」ことを書き落とす。", "$f(a)f(b)<0$ だけ示して、何の定理を使ったかを書かない。"], chk=chk, kind="proof")


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(stem, wrong, step, etype, tempt, fix, ans, expl, steps, ap, alt, pit, chk=None, d=3):
    return desc(f"{stem}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい答えを求めなさい。", ans, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい解答を途中式とともに示している", 3), ("最終的な答えが正しい", 1)], d=d, p=6, lines=6,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい途中式", 3), ("正しい答え", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix), chk=chk)


@gen("error_correction", 3, ["common_error", "computation"])
def err_indeterminate(r):
    kind = r.choice(["inf_minus", "neg", "zero_inf"])
    if kind == "inf_minus":
        a = nonzero(r, -8, 8)
        L = F(a, 2)
        inner = f"n^2{'+' if a > 0 else ''}{co(a, 'n')}"
        while any(k * k + a * k <= 0 for k in range(1, 12)):
            a = abs(a)
            inner = f"n^2+{co(a, 'n')}"
            L = F(a, 2)
        wrong = f"$n\\to\\infty$ のとき $\\sqrt{{{inner}}}\\to\\infty$、$n\\to\\infty$ なので、$\\infty-\\infty=0$。よって極限は $0$"
        return err_item(f"極限 ${LIM()}(\\sqrt{{{inner}}}-n)$ を求めなさい。", wrong, "$\\infty-\\infty=0$ とした部分", "concept",
                        "どちらも $\\infty$ に発散するので、打ち消し合って $0$ になると考えてしまう。$\\infty$ は数ではない。",
                        f"有理化して $\\dfrac{{{co(a, 'n')}}}{{\\sqrt{{{inner}}}+n}}=\\dfrac{{{a}}}{{\\sqrt{{1{'+' if a > 0 else '-'}\\frac{{{abs(a)}}}{{n}}}}+1}}\\to {ft(L)}$", f"${ft(L)}$",
                        "$\\infty-\\infty$ は不定形。有理化して $\\dfrac{\\infty}{\\infty}$ の形に直してから極限を求める。",
                        [f"分子・分母に $\\sqrt{{{inner}}}+n$ をかけると $\\dfrac{{{co(a, 'n')}}}{{\\sqrt{{{inner}}}+n}}$。", "分子・分母を $n$ で割る。", f"$n\\to\\infty$ として ${ft(L)}$。"],
                        "不定形 $\\infty-\\infty$ は、根号を含むなら有理化する。",
                        [f"$n=10000$ を代入すると約 ${float(L):.2f}$ となり、$0$ ではないことが確かめられる。"],
                        ["$\\infty$ を数のように計算する。"], chk=(f"limit(sqrt(n**2+({a})*n)-n, n, oo)", fp(L)))
    if kind == "neg":
        a = nonzero(r, -8, 8)
        L = F(-a, 2)
        inner = f"x^2{'+' if a > 0 else ''}{co(a, 'x')}"
        wrong = (f"$\\sqrt{{{inner}}}+x=\\dfrac{{{co(a, 'x')}}}{{\\sqrt{{{inner}}}-x}}$。分子・分母を $x$ で割ると "
                 f"$\\dfrac{{{a}}}{{\\sqrt{{1{'+' if a > 0 else '-'}\\frac{{{abs(a)}}}{{x}}}}-1}}$。よって分母 $\\to0$ となり、極限は存在しない")
        return err_item(f"極限 ${LIM('x', '-\\infty')}(\\sqrt{{{inner}}}+x)$ を求めなさい。", wrong,
                        "分子・分母を $x$ で割るとき、$\\dfrac{\\sqrt{x^2+\\cdots}}{x}=\\sqrt{1+\\cdots}$ とした部分", "sign",
                        "$x>0$ のときの変形 $\\dfrac{\\sqrt{x^2}}{x}=1$ を、$x<0$ の場合にもそのまま使ってしまう。$x<0$ では $\\sqrt{x^2}=-x$。",
                        f"$x<0$ では $\\dfrac{{\\sqrt{{{inner}}}}}{{x}}=-\\sqrt{{1{'+' if a > 0 else '-'}\\frac{{{abs(a)}}}{{x}}}}$ なので、$\\dfrac{{{a}}}{{-\\sqrt{{1{'+' if a > 0 else '-'}\\frac{{{abs(a)}}}{{x}}}}-1}}\\to {ft(L)}$",
                        f"${ft(L)}$", "$x\\to-\\infty$ では $x<0$ なので $\\sqrt{x^2}=-x$。$x=-t$ と置きかえるとよい。",
                        [f"$x=-t$ とおくと $t\\to\\infty$ で、式は $\\sqrt{{t^2{'-' if a > 0 else '+'}{co(abs(a), 't')}}}-t$。",
                         f"有理化して $\\dfrac{{{co(-a, 't')}}}{{\\sqrt{{t^2{'-' if a > 0 else '+'}{co(abs(a), 't')}}}+t}}$。", f"$t$ で割って $t\\to\\infty$ とすると ${ft(L)}$。"],
                        "$x\\to-\\infty$ の極限は $x=-t$ と置きかえて $t\\to\\infty$ の問題にする。",
                        [f"$x=-10000$ を代入して電卓で計算すると約 ${float(L):.2f}$ になる。"],
                        ["$\\sqrt{x^2}=x$ としてしまう。"], chk=(f"limit(sqrt(x**2+({a})*x)+x, x, -oo)", fp(L)))
    a = r.randint(1, 9)
    k = r.choice([1, 2, 3])
    L = F(a, 2 * k)
    inner = f"{'' if k == 1 else k * k}n^2+{a}"
    kn = "n" if k == 1 else f"{k}n"
    wrong = f"$\\sqrt{{{inner}}}-{kn}\\to0$ であり、$n\\to\\infty$ だから、$\\infty\\times0=0$。よって極限は $0$"
    return err_item(f"極限 ${LIM()}n(\\sqrt{{{inner}}}-{kn})$ を求めなさい。", wrong, "$\\infty\\times0=0$ とした部分", "concept",
                    "「$0$ に何をかけても $0$」という感覚を、$0$ に近づく量と $\\infty$ に発散する量の積にも当てはめてしまう。",
                    f"有理化して $\\dfrac{{{a}n}}{{\\sqrt{{{inner}}}+{kn}}}=\\dfrac{{{a}}}{{\\sqrt{{{k * k}+\\frac{{{a}}}{{n^2}}}}+{k}}}\\to {ft(L)}$", f"${ft(L)}$",
                    "$\\infty\\times0$ は不定形。$0$ に近づく部分を有理化して、積の形を分数の形に直す。",
                    [f"$\\sqrt{{{inner}}}-{kn}=\\dfrac{{{a}}}{{\\sqrt{{{inner}}}+{kn}}}$。", f"$n$ をかけて $\\dfrac{{{a}n}}{{\\sqrt{{{inner}}}+{kn}}}$、分子・分母を $n$ で割る。", f"$n\\to\\infty$ として $\\dfrac{{{a}}}{{{2 * k}}}={ft(L)}$。"],
                    "$0\\times\\infty$ の形は、どちらが「速く」変化するかで結果が変わる。式変形で確かめる。",
                    [f"$n=1000$ を代入すると約 ${float(L):.3f}$ になる。"], ["$0\\times\\infty$ を $0$ と決めつける。"],
                    chk=(f"limit(n*(sqrt({k * k}*n**2+{a})-{k}*n), n, oo)", fp(L)))


@gen("error_correction", 3, ["common_error", "condition_check"])
def err_series(r):
    if r.random() < 0.5:
        rt = r.choice([F(3, 2), F(2), F(4, 3), F(5, 2), F(3), F(5, 3), F(5, 4)])
        a = nonzero(r, -5, 6)
        terms = [F(a) * rt ** k for k in range(3)]
        tex = ft(terms[0]) + "".join(("+" if t > 0 else "-") + ft(abs(t)) for t in terms[1:])
        wv = F(a) / (1 - rt)
        wrong = f"初項 ${a}$、公比 ${ft(rt)}$ なので、和は $\\dfrac{{{a}}}{{1-{ft(rt)}}}={ft(wv)}$"
        s = 1 if a > 0 else -1
        return err_item(f"無限等比級数 ${tex}+\\cdots$ の収束・発散を調べ、収束するときはその和を求めなさい。", wrong,
                        "収束条件 $|r|<1$ を確かめずに和の公式を使った部分", "condition",
                        "公式 $\\dfrac{a}{1-r}$ を「無限等比級数の和の公式」と丸暗記し、$|r|<1$ という前提を忘れている。",
                        f"公比 ${ft(rt)}>1$ なので部分和 $S_n=\\dfrac{{{a}\\{{({ft(rt)})^n-1\\}}}}{{{ft(rt)}-1}}$ は{'正' if s > 0 else '負'}の無限大に発散する。級数は発散する",
                        "発散する（和はない）", f"公比 ${ft(rt)}$ は $|r|<1$ を満たさないので発散する。",
                        [f"初項 ${a}$、公比 ${ft(rt)}$。", f"$|{ft(rt)}|\\geqq1$ なので、収束条件を満たさない。", f"部分和は{'正' if s > 0 else '負'}の無限大に発散し、級数は発散する。"],
                        "和の公式を使う前に、必ず $|r|<1$（または初項 $=0$）を確かめる。",
                        [f"項がどんどん大きくなる（絶対値が増える）ので、和が有限の値 ${ft(wv)}$ になるはずがない、と考えても誤りに気づける。"],
                        ["収束条件の確認を省く。"],
                        chk=(f"atan(limit(({a})*(({fp(rt)})**n-1)/(({fp(rt)})-1), n, oo))", "pi/2" if s > 0 else "-pi/2", None, "intermediate"))
    a = r.randint(1, 4)
    m = r.randint(1, 4)
    ax = "x" if a == 1 else f"{a}x"
    rt = "(1-x)" if m == 1 else f"\\left(1-\\dfrac{{x}}{{{m}}}\\right)"
    rt2 = "(1-x)^2" if m == 1 else f"\\left(1-\\dfrac{{x}}{{{m}}}\\right)^2"
    rin = "1-x" if m == 1 else f"1-\\dfrac{{x}}{{{m}}}"
    wrong = f"公比 ${rin}$ について $-1<{rin}<1$ より $0<x<{2 * m}$。和は $\\dfrac{{{ax}}}{{1-{rt}}}={a * m}$。答え：$0<x<{2 * m}$ のとき和 ${a * m}$"
    return err_item(f"無限等比級数 ${ax}+{ax}{rt}+{ax}{rt2}+\\cdots$ が収束するような $x$ の値の範囲と、そのときの和を求めなさい。", wrong,
                    "初項が $0$ になる場合（$x=0$）を検討していない部分", "condition",
                    "収束条件を「$|r|<1$」だけと覚えていて、初項 $=0$ ならば公比によらず収束することを見落としている。",
                    f"$x=0$ のときはすべての項が $0$ で収束し和は $0$。よって範囲は $0\\leqq x<{2 * m}$、和は $x=0$ のとき $0$、$0<x<{2 * m}$ のとき ${a * m}$",
                    f"$0\\leqq x<{2 * m}$。和は $x=0$ のとき $0$、$0<x<{2 * m}$ のとき ${a * m}$",
                    "無限等比級数は「初項 $=0$」または「$|r|<1$」で収束する。",
                    ["初項 $" + ax + "=0$、すなわち $x=0$ のとき、和は $0$。", f"$x\\neq0$ のとき、$-1<{rin}<1$ より $0<x<{2 * m}$、和は ${a * m}$。", f"合わせて $0\\leqq x<{2 * m}$。"],
                    "初項に文字を含むときは、まず「初項 $=0$」の場合を分けて考える。",
                    ["$x=0$ を問題の級数に代入すると $0+0+0+\\cdots=0$ となり、収束することが直接確かめられる。"],
                    ["初項 $=0$ の場合を落とす。"],
                    chk=(f"[solve(Eq(1-x/{m}, -1), x), simplify(({a}*x)/(1-(1-x/{m})))]", f"[[{2 * m}], {a * m}]", None, "intermediate"))


@gen("error_correction", 2, ["common_error", "concept"])
def err_power_ratio(r):
    while True:
        a, b = sorted(r.sample(range(2, 8), 2))
        if math.gcd(a, b) != 1:
            continue
        c1, c2, c3, c4 = nonzero(r, -3, 3), nonzero(r, -3, 3), r.choice([1, 2, 3]), r.choice([1, 2, 3, -1])
        e1, e2 = r.choice([0, 1]), r.choice([0, 1, 2])
        correct = F(c2 * b ** e2, c4)
        wrongv = F(c1 * a ** e1, c3)
        if correct != wrongv:
            break
    ntex = pw(c1, a, e1, True) + pw(c2, b, e2)
    dtex = pw(c3, a, 0, True) + pw(c4, b, 0)
    rr = f"\\left(\\dfrac{{{b}}}{{{a}}}\\right)^n"
    wrong = f"分子・分母を ${a}^n$ で割ると $\\dfrac{{{c1 * a ** e1}{'+' if c2 > 0 else '-'}{cf(abs(c2) * b ** e2)}{rr}}}{{{c3}{'+' if c4 > 0 else '-'}{cf(abs(c4))}{rr}}}$。${rr}\\to0$ なので、極限は ${ft(wrongv)}$"
    rr2 = f"\\left(\\dfrac{{{a}}}{{{b}}}\\right)^n"
    return err_item(f"極限 ${LIM()}\\dfrac{{{ntex}}}{{{dtex}}}$ を求めなさい。", wrong, f"${rr}\\to0$ とした部分", "concept",
                    "「$r^n\\to0$」という形を見るとすぐ $0$ にしてしまい、$r=\\dfrac{" + str(b) + "}{" + str(a) + "}>1$ であることを確かめていない。",
                    f"${b}>{a}$ なので ${b}^n$ で割る。$\\dfrac{{{cf(c1 * a ** e1)}{rr2}{'+' if c2 > 0 else '-'}{abs(c2) * b ** e2}}}{{{cf(c3)}{rr2}{'+' if c4 > 0 else '-'}{abs(c4)}}}\\to {ft(correct)}$",
                    f"${ft(correct)}$", f"底の大きい ${b}^n$ で割ると、${rr2}\\to0$（$0<\\dfrac{{{a}}}{{{b}}}<1$）が使える。",
                    [f"${b}>{a}$ なので、分子・分母を ${b}^n$ で割る。", f"$\\dfrac{{{cf(c1 * a ** e1)}{rr2}{'+' if c2 > 0 else '-'}{abs(c2) * b ** e2}}}{{{cf(c3)}{rr2}{'+' if c4 > 0 else '-'}{abs(c4)}}}$。", f"$0<\\dfrac{{{a}}}{{{b}}}<1$ より ${rr2}\\to0$、極限は ${ft(correct)}$。"],
                    "累乗の比の極限では、底が最も大きい項で割る。",
                    [f"$n=20$ くらいで ${b}^n$ が ${a}^n$ よりはるかに大きいことを電卓で確かめると、${b}^n$ の項が支配的だと分かる。"],
                    ["公比が $1$ より大きいか小さいかを確かめない。"],
                    chk=(f"limit((({c1})*{a}**(n+{e1})+({c2})*{b}**(n+{e2}))/(({c3})*{a}**n+({c4})*{b}**n), n, oo)", fp(correct)))


@gen("error_correction", 2, ["common_error", "concept"])
def err_trig(r):
    kind = r.choice(["inf", "deg", "xsin", "cos"])
    if kind == "inf":
        k = r.randint(1, 6)
        kx = "x" if k == 1 else f"{k}x"
        wrong = f"$\\displaystyle\\lim_{{\\theta\\to0}}\\dfrac{{\\sin\\theta}}{{\\theta}}=1$ を用いて、$\\dfrac{{\\sin {kx}}}{{{kx}}}\\to1$。よって極限は $1$"
        return err_item(f"極限 ${LIM('x', '\\infty')}\\dfrac{{\\sin {kx}}}{{{kx}}}$ を求めなさい。", wrong,
                        "$x\\to\\infty$ なのに $\\theta\\to0$ の公式を使った部分", "condition",
                        "「$\\dfrac{\\sin\\bigcirc}{\\bigcirc}=1$」という形だけを覚えていて、$\\bigcirc\\to0$ という条件を確かめていない。",
                        f"$\\left|\\dfrac{{\\sin {kx}}}{{{kx}}}\\right|\\leqq\\dfrac{{1}}{{{kx}}}\\to0$ なので、はさみうちの原理より極限は $0$", "$0$",
                        "$x\\to\\infty$ では $\\sin {kx}$ は $-1$ と $1$ の間を振動し、分母は $\\infty$ に発散する。",
                        [f"$x>0$ のとき $-\\dfrac{{1}}{{{kx}}}\\leqq\\dfrac{{\\sin {kx}}}{{{kx}}}\\leqq\\dfrac{{1}}{{{kx}}}$。", f"両端は $x\\to\\infty$ で $0$ に収束する。", "はさみうちの原理より極限は $0$。"],
                        "公式を使う前に、変数がどこに近づくかを確かめる。",
                        ["$x=1000$ などを代入すると値はほぼ $0$ になる。"], ["公式の前提（$\\theta\\to0$）を確かめない。"],
                        chk=(f"[limit(1/({k}*x), x, oo), limit(-1/({k}*x), x, oo)]", "[0, 0]", None, "intermediate"))
    if kind == "deg":
        k = r.choice([1, 2, 3, 5])
        kx = "x" if k == 1 else f"{k}x"
        L = sp.pi * k / 180
        wrong = f"$\\displaystyle\\lim_{{x\\to0}}\\dfrac{{\\sin {kx}^\\circ}}{{x}}={k}\\cdot\\dfrac{{\\sin {kx}^\\circ}}{{{kx}}}\\to {k}$。よって極限は ${k}$"
        return err_item(f"$x^\\circ$ は度数法で表した角とする。極限 ${LIM('x', 0)}\\dfrac{{\\sin {kx}^\\circ}}{{x}}$ を求めなさい。", wrong,
                        "度数法の角に $\\displaystyle\\lim_{\\theta\\to0}\\dfrac{\\sin\\theta}{\\theta}=1$ を使った部分", "concept",
                        "公式 $\\dfrac{\\sin\\theta}{\\theta}\\to1$ が弧度法を前提としていることを意識していない。",
                        f"${kx}^\\circ=\\dfrac{{{k}\\pi}}{{180}}x$（ラジアン）なので、$\\dfrac{{\\sin\\frac{{{k}\\pi}}{{180}}x}}{{x}}\\to {sp.latex(L)}$", f"${sp.latex(L)}$",
                        "公式は弧度法でのみ成り立つ。度数法の角はラジアンに直してから使う。",
                        [f"${kx}^\\circ=\\dfrac{{{k}\\pi x}}{{180}}$（ラジアン）。", f"$\\dfrac{{\\sin\\frac{{{k}\\pi x}}{{180}}}}{{x}}=\\dfrac{{{k}\\pi}}{{180}}\\cdot\\dfrac{{\\sin\\frac{{{k}\\pi x}}{{180}}}}{{\\frac{{{k}\\pi x}}{{180}}}}$。", f"極限は ${sp.latex(L)}$。"],
                        "$\\dfrac{\\sin\\theta}{\\theta}\\to1$ は、扇形の面積 $\\dfrac{1}{2}r^2\\theta$（弧度法）から導かれたことを思い出す。",
                        [f"$x=1$ のとき $\\dfrac{{\\sin {k}^\\circ}}{{1}}\\fallingdotseq{math.sin(math.radians(k)):.4f}$ であり、${k}$ よりはるかに小さい。生徒の答えが不自然であることに数値で気づける。"],
                        ["角の単位を確かめない。"], chk=(f"limit(sin(pi*{k}*x/180)/x, x, 0)", sp.sstr(L)))
    if kind == "xsin":
        a = r.randint(2, 9)
        wrong = f"$x\\to\\infty$ のとき $\\dfrac{{{a}}}{{x}}\\to0$ なので $\\sin\\dfrac{{{a}}}{{x}}\\to0$。よって $x\\sin\\dfrac{{{a}}}{{x}}\\to\\infty\\times0=0$"
        return err_item(f"極限 ${LIM('x', '\\infty')}x\\sin\\dfrac{{{a}}}{{x}}$ を求めなさい。", wrong, "$\\infty\\times0=0$ とした部分", "concept",
                        "$0$ に近づく量と $\\infty$ に発散する量の積を、$0$ と決めつけている。",
                        f"$t=\\dfrac{{{a}}}{{x}}$ とおくと $x\\to\\infty$ で $t\\to+0$、$x\\sin\\dfrac{{{a}}}{{x}}={a}\\cdot\\dfrac{{\\sin t}}{{t}}\\to {a}$", f"${a}$",
                        "$\\infty\\times0$ は不定形。$\\dfrac{\\sin t}{t}$ の形をつくる。",
                        [f"$t=\\dfrac{{{a}}}{{x}}$ とおくと $x=\\dfrac{{{a}}}{{t}}$、$x\\to\\infty$ のとき $t\\to+0$。", f"$x\\sin\\dfrac{{{a}}}{{x}}={a}\\cdot\\dfrac{{\\sin t}}{{t}}$。", f"$t\\to+0$ として ${a}$。"],
                        "置きかえで $\\dfrac{\\sin t}{t}\\ (t\\to0)$ の形に持ち込む。",
                        [f"$x=1000$ を代入すると $1000\\sin {float(a) / 1000:.3f}\\fallingdotseq{1000 * math.sin(a / 1000):.3f}$ で ${a}$ に近い。"],
                        ["置きかえで変数の行き先を確かめない。"], chk=(f"limit(x*sin({a}/x), x, oo)", str(a)))
    a = r.randint(2, 6)
    L = F(a * a, 2)
    wrong = f"$\\dfrac{{1-\\cos {a}x}}{{x^2}}=\\dfrac{{\\sin^2 {a}x}}{{x^2(1+\\cos {a}x)}}=\\left(\\dfrac{{\\sin {a}x}}{{x}}\\right)^2\\cdot\\dfrac{{1}}{{1+\\cos {a}x}}\\to1\\cdot\\dfrac{{1}}{{2}}=\\dfrac{{1}}{{2}}$"
    return err_item(f"極限 ${LIM('x', 0)}\\dfrac{{1-\\cos {a}x}}{{x^2}}$ を求めなさい。", wrong,
                    f"$\\dfrac{{\\sin {a}x}}{{x}}\\to1$ とした部分", "formula",
                    "$\\sin$ の中身と分母がそろっていないのに、$\\dfrac{\\sin\\bigcirc}{\\bigcirc}\\to1$ を当てはめている。",
                    f"$\\dfrac{{\\sin {a}x}}{{x}}={a}\\cdot\\dfrac{{\\sin {a}x}}{{{a}x}}\\to {a}$ なので、極限は ${a}^2\\cdot\\dfrac{{1}}{{2}}={ft(L)}$", f"${ft(L)}$",
                    f"$\\dfrac{{\\sin {a}x}}{{{a}x}}$ の形にそろえると、係数 ${a}$ が外に出る。",
                    [f"分子・分母に $1+\\cos {a}x$ をかけて $\\dfrac{{\\sin^2 {a}x}}{{x^2(1+\\cos {a}x)}}$。", f"$=\\left(\\dfrac{{\\sin {a}x}}{{{a}x}}\\right)^2\\cdot\\dfrac{{{a * a}}}{{1+\\cos {a}x}}$。", f"$x\\to0$ として ${a * a}\\cdot\\dfrac{{1}}{{2}}={ft(L)}$。"],
                    "$\\sin$ の中身と分母を必ずそろえる。",
                    [f"$1-\\cos\\theta=2\\sin^2\\dfrac{{\\theta}}{{2}}$ を使って $\\dfrac{{2\\sin^2\\frac{{{a}x}}{{2}}}}{{x^2}}$ と変形しても ${ft(L)}$ が得られる。"],
                    ["中身と分母をそろえない。"], chk=(f"limit((1-cos({a}*x))/x**2, x, 0)", fp(L)))


GENERATORS = [seq_rational, geom_power, inf_geo_sum, func_limit_factor, trig_limit,
              sqrt_diff, geo_series_x, recurrence_limit, limit_param, one_sided,
              squeeze, series_figure, continuity_param, ivt,
              err_indeterminate, err_series, err_power_ratio, err_trig]
