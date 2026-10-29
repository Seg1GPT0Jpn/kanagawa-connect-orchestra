"""単元パック：数学Ⅲ 積分法とその応用（置換積分法・部分積分法、定積分と面積、区分求積法、体積、曲線の長さ）。"""
import math
from fractions import Fraction as F

import sympy as sp

from banks._common import desc, figure, plane, sa
from hs_pack_lib import board, check, definition, derivation, example, gen, guide, intro, lesson, nonzero, summary, theorem, tp

UNIT_ID = "HS-MATH3-U03"

X = sp.Symbol("x")


# ----------------------------------------------------------------------
# 補助
# ----------------------------------------------------------------------

def ft(v):
    v = F(v)
    if v.denominator == 1:
        return str(v.numerator)
    return f"{'-' if v < 0 else ''}\\dfrac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def fp(v):
    v = F(v)
    return str(v.numerator) if v.denominator == 1 else f"Rational({v.numerator},{v.denominator})"


def _tx1(e):
    s = sp.latex(e).replace("\\frac", "\\dfrac")
    return "\\dfrac{1}{e}" if s == "e^{-1}" else s


def TX(e):
    """sympy 式の LaTeX。和は「数でない項（e, π を含む項）を先、定数項を後」の順に並べる。"""
    e = sp.nsimplify(e) if not isinstance(e, sp.Basic) else e
    if isinstance(e, sp.Add):
        terms = sorted(e.as_ordered_terms(), key=lambda t: (t.could_extract_minus_sign(), bool(t.is_Rational)))
        out = ""
        for t in terms:
            neg = t.could_extract_minus_sign()
            body = _tx1(-t if neg else t)
            out += ("-" if neg else ("+" if out else "")) + body
        return out
    return _tx1(e)


def cf(c):
    return "" if c == 1 else ("-" if c == -1 else str(c))


def tf_(c):
    return "" if c == 0 else (f"+{c}" if c > 0 else f"{c}")


def lin(a, b, var="x"):
    return f"{cf(a)}{var}{tf_(b)}"


def kfrac(k, body):
    """係数 k（有理数）× body の LaTeX。"""
    k = F(k)
    if k == 1:
        return body
    if k == -1:
        return "-" + body
    return f"{ft(k)}{body}"


def INT(a=None, b=None):
    if a is None:
        return "\\displaystyle\\int "
    a, b = str(a).replace("dfrac", "frac"), str(b).replace("dfrac", "frac")
    return f"\\displaystyle\\int_{{{a}}}^{{{b}}}"


LESSON = lesson(
    goals=["置換積分法・部分積分法を合成関数・積の微分法から導き、三角・指数・対数関数を含む不定積分・定積分を計算できる。",
           "区分求積法によって定積分を和の極限として理解し、面積・体積を定積分で表して求められる。",
           "曲線の長さの公式を導き、媒介変数表示された曲線や $y=f(x)$ の曲線の長さを求められる。"],
    duration=200,
    readiness=["三角・指数・対数関数の導関数、合成関数・積の微分法（数学Ⅲ 微分法）を使える。", "定積分の計算と、2曲線の間の面積の求め方（数学Ⅱ）を使える。",
               "$\\displaystyle\\sum_{k=1}^{n}k^2=\\dfrac{n(n+1)(2n+1)}{6}$ などの和の公式（数学B）と数列の極限（数学Ⅲ 極限）を使える。"],
    flow=[("導入：微分の逆として積分を広げる", 10, "微分法で得た公式を逆に読み、積分できる関数を増やすことを確認する"),
          ("基本公式・置換積分法", 40, "基本公式の表、置換積分法の導出、$f'(x)/f(x)$ の形、定積分の置換（例題1・2）"),
          ("部分積分法", 25, "積の微分法からの導出と、$x e^x$・$\\log x$ の積分（例題1）"),
          ("区分求積法と面積", 40, "和の極限としての定積分、面積の計算（例題3）"),
          ("体積", 40, "断面積の積分 $V=\\displaystyle\\int_a^bS(x)\\,dx$、回転体の体積（例題4）"),
          ("曲線の長さとまとめ", 45, "曲線の長さの公式とサイクロイド（例題5）、確認問題、課題指示")],
    sections=[
        intro("in1", "微分の公式を逆に読む",
              "数学Ⅲの微分法で、$(\\sin x)'=\\cos x$、$(e^x)'=e^x$、$(\\log|x|)'=\\dfrac{1}{x}$ などを学んだ。これらを逆に読めば、$\\cos x$、$e^x$、$\\dfrac{1}{x}$ の原始関数が分かる。さらに、合成関数の微分法を逆にした置換積分法、積の微分法を逆にした部分積分法を使うと、積分できる関数が大きく広がる。積分は面積だけでなく、体積や曲線の長さを求める強力な道具になる。",
              bullets=["微分の公式 → 不定積分の基本公式", "合成関数の微分法 → 置換積分法、積の微分法 → 部分積分法", "定積分 = 細かく分けた量の和の極限（区分求積法）"],
              points=[tp("$\\displaystyle\\int\\dfrac{1}{x}\\,dx$ が数学Ⅱの公式 $\\dfrac{x^{n+1}}{n+1}$ では求められない（$n=-1$ で分母が $0$）ことを確認し、新しい公式の必要性を示す。",
                         ask="$\\displaystyle\\int x^{-1}\\,dx$ に数学Ⅱの公式を当てはめるとどうなるか。", expect="$\\dfrac{x^0}{0}$ となって意味をもたない。", timing="導入の冒頭")]),
        definition("df1", "不定積分の基本公式",
                   "$F'(x)=f(x)$ のとき $\\displaystyle\\int f(x)\\,dx=F(x)+C$（$C$ は積分定数）。微分の公式から次が得られる。",
                   formula="$$\\int x^r\\,dx=\\dfrac{x^{r+1}}{r+1}+C\\ (r\\neq-1),\\quad \\int\\dfrac{dx}{x}=\\log|x|+C,\\quad \\int e^x\\,dx=e^x+C,\\quad \\int a^x\\,dx=\\dfrac{a^x}{\\log a}+C$$",
                   conditions=["$\\displaystyle\\int\\sin x\\,dx=-\\cos x+C$、$\\displaystyle\\int\\cos x\\,dx=\\sin x+C$、$\\displaystyle\\int\\dfrac{dx}{\\cos^2x}=\\tan x+C$。",
                               "$F'(x)=f(x)$ のとき $\\displaystyle\\int f(ax+b)\\,dx=\\dfrac{1}{a}F(ax+b)+C$（$a\\neq0$）。",
                               "$\\displaystyle\\int\\dfrac{g'(x)}{g(x)}\\,dx=\\log|g(x)|+C$。"],
                   points=[tp("答えを微分してもとの関数に戻るかで必ず検算させる。特に $\\displaystyle\\int\\sin x\\,dx$ の符号を間違えやすい。", caution="$\\displaystyle\\int\\sin x\\,dx=\\cos x+C$ とする誤りが多い。")]),
        theorem("th1", "置換積分法と部分積分法",
                "$$\\int f(g(x))g'(x)\\,dx=\\int f(t)\\,dt\\ \\ (t=g(x)),\\qquad \\int f(x)g'(x)\\,dx=f(x)g(x)-\\int f'(x)g(x)\\,dx$$",
                ["定積分で置換するときは、積分区間も新しい変数の区間に取りかえる：$\\displaystyle\\int_a^bf(g(x))g'(x)\\,dx=\\int_{g(a)}^{g(b)}f(t)\\,dt$。",
                 "$\\sqrt{a^2-x^2}$ を含むときは $x=a\\sin\\theta$、$\\dfrac{1}{x^2+a^2}$ を含むときは $x=a\\tan\\theta$ と置換する。",
                 "部分積分法では、微分すると簡単になる方（$x^n$、$\\log x$ など）を $f(x)$ に選ぶ。"],
                proof=["置換積分：$F'(t)=f(t)$ とすると、合成関数の微分法より $\\{F(g(x))\\}'=f(g(x))g'(x)$。",
                       "よって $\\displaystyle\\int f(g(x))g'(x)\\,dx=F(g(x))+C=\\int f(t)\\,dt$（$t=g(x)$）。形式的には $dt=g'(x)\\,dx$ と書ける。",
                       "部分積分：積の微分法 $\\{f(x)g(x)\\}'=f'(x)g(x)+f(x)g'(x)$ の両辺を積分すると $f(x)g(x)=\\displaystyle\\int f'(x)g(x)\\,dx+\\int f(x)g'(x)\\,dx$。",
                       "移項して $\\displaystyle\\int f(x)g'(x)\\,dx=f(x)g(x)-\\int f'(x)g(x)\\,dx$。"],
                points=[tp("置換積分は「合成関数の微分法の逆」、部分積分は「積の微分法の逆」であることを、公式を並べて板書し対応させる。",
                           ask="$\\displaystyle\\int 2x(x^2+1)^3\\,dx$ はどの微分の公式の逆か。", expect="$(x^2+1)^4$ を合成関数の微分法で微分したもの（の $\\dfrac14$ 倍）。"),
                        tp("定積分の置換で積分区間を取りかえ忘れる誤りが非常に多い。$x$ と $t$ の対応表をかかせる。", caution="区間を $x$ のまま使ってしまう。", timing="例題2の前")]),
        example("ex1", "例題1　置換積分法・部分積分法",
                "次の不定積分を求めよ。(1) $\\displaystyle\\int x(x^2+1)^3\\,dx$　(2) $\\displaystyle\\int xe^x\\,dx$　(3) $\\displaystyle\\int\\log x\\,dx$",
                ["(1) $t=x^2+1$ とおくと $dt=2x\\,dx$。$\\displaystyle\\int t^3\\cdot\\dfrac{1}{2}\\,dt=\\dfrac{t^4}{8}+C=\\dfrac{(x^2+1)^4}{8}+C$。",
                 "(2) $f=x,\\ g'=e^x$ として $xe^x-\\displaystyle\\int e^x\\,dx=xe^x-e^x+C=(x-1)e^x+C$。",
                 "(3) $\\log x=(\\log x)\\cdot(x)'$ と見て $x\\log x-\\displaystyle\\int\\dfrac{1}{x}\\cdot x\\,dx=x\\log x-x+C$。"],
                "(1) $\\dfrac{(x^2+1)^4}{8}+C$　(2) $(x-1)e^x+C$　(3) $x\\log x-x+C$",
                thinking="(1) は中身 $x^2+1$ の導関数 $2x$ が外にあるので置換。(2)(3) は積（(3) は $1\\times\\log x$）なので部分積分。",
                points=[tp("(3) で「$1$ を $x'$ と見る」発想を強調し、$\\displaystyle\\int\\log x\\,dx$ は結果を覚えるのではなく導けるようにさせる。")]),
        example("ex2", "例題2　三角関数による置換",
                "定積分 $\\displaystyle\\int_0^1\\sqrt{1-x^2}\\,dx$ を求めよ。",
                ["$x=\\sin\\theta$ とおくと $dx=\\cos\\theta\\,d\\theta$。$x:0\\to1$ のとき $\\theta:0\\to\\dfrac{\\pi}{2}$。",
                 "$0\\leqq\\theta\\leqq\\dfrac{\\pi}{2}$ で $\\cos\\theta\\geqq0$ なので $\\sqrt{1-\\sin^2\\theta}=\\cos\\theta$。",
                 "$\\displaystyle\\int_0^{\\frac{\\pi}{2}}\\cos^2\\theta\\,d\\theta=\\int_0^{\\frac{\\pi}{2}}\\dfrac{1+\\cos2\\theta}{2}\\,d\\theta=\\dfrac{\\pi}{4}$。"],
                "$\\dfrac{\\pi}{4}$",
                thinking="$\\sqrt{1-x^2}$ は $x=\\sin\\theta$ で根号が外れる。区間の取りかえと、$\\cos\\theta$ の符号に注意する。",
                points=[tp("答えが半径 $1$ の四分円の面積 $\\dfrac{\\pi}{4}$ に一致することを図で確かめさせ、置換の結果に納得させる。")]),
        theorem("th2", "区分求積法",
                "$$\\lim_{n\\to\\infty}\\dfrac{1}{n}\\sum_{k=1}^{n}f\\left(\\dfrac{k}{n}\\right)=\\int_0^1f(x)\\,dx$$",
                ["$f(x)$ が $0\\leqq x\\leqq1$ で連続のとき成り立つ。和の範囲を $k=0$ から $n-1$ にしても同じ極限になる。",
                 "一般に $\\displaystyle\\lim_{n\\to\\infty}\\dfrac{b-a}{n}\\sum_{k=1}^{n}f\\left(a+\\dfrac{b-a}{n}k\\right)=\\int_a^bf(x)\\,dx$。",
                 "和の極限を求めるには、$\\dfrac{1}{n}$ をくくり出し、残りを $\\dfrac{k}{n}$ だけの式に直す。"],
                proof=["区間 $[0,\\,1]$ を $n$ 等分し、幅 $\\dfrac{1}{n}$、高さ $f\\left(\\dfrac{k}{n}\\right)$ の長方形を $k=1,\\,2,\\,\\cdots,\\,n$ について並べる。",
                       "長方形の面積の和 $\\dfrac{1}{n}\\displaystyle\\sum_{k=1}^{n}f\\left(\\dfrac{k}{n}\\right)$ は、$n$ を大きくするとグラフの下の部分の面積に近づく。",
                       "$f(x)\\geqq0$ のとき、この面積は $\\displaystyle\\int_0^1f(x)\\,dx$ である（一般の連続関数でも、符号つき面積として同様に成り立つ）。"],
                figure=figure("y=x^2 の下に並べた幅 1/n の長方形（区分求積法）",
                              plane((0, 1.2), (0, 1.2), unit=150, curves=[(lambda x: x * x, "")],
                                    polygons=[[(k / 5 - 0.2, 0), (k / 5, 0), (k / 5, (k / 5) ** 2), (k / 5 - 0.2, (k / 5) ** 2)] for k in range(1, 6)], ticks=False)),
                points=[tp("$\\displaystyle\\lim_{n\\to\\infty}\\dfrac{1}{n^3}\\sum_{k=1}^{n}k^2$ を、和の公式で計算した結果と区分求積法の結果（$\\dfrac{1}{3}$）が一致することを確かめさせる。",
                           ask="$\\dfrac{1}{n^3}\\displaystyle\\sum k^2$ を $\\dfrac{1}{n}\\displaystyle\\sum f\\left(\\dfrac{k}{n}\\right)$ の形に直すと、$f(x)$ は何か。", expect="$f(x)=x^2$")]),
        example("ex3", "例題3　面積",
                "曲線 $y=\\log x$ と $x$ 軸、直線 $x=e$ で囲まれた部分の面積を求めよ。",
                ["$y=\\log x$ は $x=1$ で $x$ 軸と交わり、$1\\leqq x\\leqq e$ で $y\\geqq0$。",
                 "$S=\\displaystyle\\int_1^e\\log x\\,dx=\\Bigl[x\\log x-x\\Bigr]_1^e=(e-e)-(0-1)=1$。"],
                "$1$",
                thinking="まず $x$ 軸との交点と上下関係を確かめ、例題1(3) の原始関数を使う。",
                figure=figure("y=log x と x 軸、x=e で囲まれた部分", plane((0, 3), (-1, 1.5), unit=50, curves=[(lambda x: math.log(x) if x > 0.05 else float("nan"), "")],
                                                                        points=[(1, 0, "1"), (math.e, 1, "(e,1)")])),
                points=[tp("$y$ 軸方向に積分して $\\displaystyle\\int_0^1(e-e^y)\\,dy=1$ としても求められることを紹介し、逆関数の見方を示す。")]),
        derivation("dv1", "体積と曲線の長さの公式",
                   ["立体を $x$ 軸に垂直な平面で切った断面積を $S(x)$ とする。$x$ から $x+\\Delta x$ までの薄い部分の体積はおよそ $S(x)\\Delta x$。",
                    "これを足し合わせて $\\Delta x\\to0$ とすると $V=\\displaystyle\\int_a^bS(x)\\,dx$。$y=f(x)$ を $x$ 軸のまわりに回転した立体では $S(x)=\\pi\\{f(x)\\}^2$ なので $V=\\pi\\displaystyle\\int_a^b\\{f(x)\\}^2\\,dx$。",
                    "曲線 $x=f(t),\\ y=g(t)$ の微小部分の長さは、三平方の定理よりおよそ $\\sqrt{(\\Delta x)^2+(\\Delta y)^2}=\\sqrt{\\left(\\dfrac{\\Delta x}{\\Delta t}\\right)^2+\\left(\\dfrac{\\Delta y}{\\Delta t}\\right)^2}\\,\\Delta t$。",
                    "足し合わせて $\\Delta t\\to0$ とすると $L=\\displaystyle\\int_\\alpha^\\beta\\sqrt{\\left(\\dfrac{dx}{dt}\\right)^2+\\left(\\dfrac{dy}{dt}\\right)^2}\\,dt$。$y=f(x)$ のときは $L=\\displaystyle\\int_a^b\\sqrt{1+\\{f'(x)\\}^2}\\,dx$。"],
                   body="「小さく分けて足し合わせ、極限をとる」という区分求積法の考え方が、面積・体積・長さに共通している。",
                   points=[tp("半径 $r$ の球の体積を、断面積 $\\pi(r^2-x^2)$ の積分として求めさせ、公式 $\\dfrac{4}{3}\\pi r^3$ が導かれることを確認する。",
                              ask="球を中心から距離 $x$ の平面で切った断面の半径は？", expect="$\\sqrt{r^2-x^2}$")]),
        example("ex4", "例題4　回転体の体積",
                "曲線 $y=\\sin x\\ (0\\leqq x\\leqq\\pi)$ と $x$ 軸で囲まれた部分を、$x$ 軸のまわりに1回転してできる立体の体積を求めよ。",
                ["$V=\\pi\\displaystyle\\int_0^{\\pi}\\sin^2x\\,dx$。", "$\\sin^2x=\\dfrac{1-\\cos2x}{2}$ より $\\displaystyle\\int_0^{\\pi}\\sin^2x\\,dx=\\Bigl[\\dfrac{x}{2}-\\dfrac{\\sin2x}{4}\\Bigr]_0^{\\pi}=\\dfrac{\\pi}{2}$。",
                 "$V=\\dfrac{\\pi^2}{2}$。"],
                "$\\dfrac{\\pi^2}{2}$",
                thinking="回転体の断面は半径 $\\sin x$ の円。$\\sin^2x$ は半角の公式で次数を下げて積分する。",
                points=[tp("$\\pi$ をかけ忘れる、$\\sin^2x$ をそのまま積分できずに止まる、の2点を机間指導で確認する。")]),
        example("ex5", "例題5　曲線の長さ",
                "サイクロイド $x=a(t-\\sin t),\\ y=a(1-\\cos t)\\ (0\\leqq t\\leqq2\\pi,\\ a>0)$ の長さを求めよ。",
                ["$\\dfrac{dx}{dt}=a(1-\\cos t),\\ \\dfrac{dy}{dt}=a\\sin t$。", "$\\left(\\dfrac{dx}{dt}\\right)^2+\\left(\\dfrac{dy}{dt}\\right)^2=2a^2(1-\\cos t)=4a^2\\sin^2\\dfrac{t}{2}$。",
                 "$0\\leqq t\\leqq2\\pi$ で $\\sin\\dfrac{t}{2}\\geqq0$ なので $L=\\displaystyle\\int_0^{2\\pi}2a\\sin\\dfrac{t}{2}\\,dt=\\Bigl[-4a\\cos\\dfrac{t}{2}\\Bigr]_0^{2\\pi}=8a$。"],
                "$8a$",
                thinking="根号の中を半角の公式で完全平方にする。$\\sqrt{A^2}=|A|$ なので符号を確かめる。",
                points=[tp("転がる円の半径 $a$ に対し、1回転で進む距離が $2\\pi a$、描く曲線の長さが $8a$ であることを比べさせる。")]),
        board("bd1", "板書案",
              [("① 積分の計算", ["基本公式（微分の逆）", "置換：$\\displaystyle\\int f(g(x))g'(x)\\,dx=\\int f(t)\\,dt$", "部分：$\\displaystyle\\int fg'=fg-\\int f'g$", "定積分の置換は区間も変える"]),
               ("② 区分求積・面積", ["$\\displaystyle\\lim\\dfrac{1}{n}\\sum f\\left(\\dfrac{k}{n}\\right)=\\int_0^1f(x)\\,dx$", "面積 $=\\displaystyle\\int(\\text{上}-\\text{下})\\,dx$", "例3 $\\displaystyle\\int_1^e\\log x\\,dx=1$"]),
               ("③ 体積・長さ", ["$V=\\displaystyle\\int_a^bS(x)\\,dx$", "回転体 $V=\\pi\\displaystyle\\int_a^by^2\\,dx$", "$L=\\displaystyle\\int\\sqrt{\\dot{x}^2+\\dot{y}^2}\\,dt$", "例5 サイクロイド $8a$"])],
              points=[tp("③の各公式の横に「何を細かく分けたか（断面・弧の微小部分）」を小さく図示し、②の区分求積の考え方から矢印で結ぶ。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("置換積分では「中身の導関数が外にあるか」を見る習慣をつけさせる。なければ係数を調整するか、別の方法を考える。", ask="$\\displaystyle\\int xe^{x^2}\\,dx$ で $t=x^2$ とおくと何が残るか。", expect="$\\dfrac{1}{2}e^t\\,dt$"),
               tp("部分積分の $f$ と $g'$ の選び方は「微分して簡単になる方を $f$」。$\\log x$ と多項式の積では $\\log x$ を $f$ にすることを確認する。"),
               tp("面積・体積の問題では、必ず図をかいて交点・上下関係・回転軸を確認してから式を立てさせる。", timing="例題3・4の前"),
               tp("回転体の体積で、2曲線の間の部分は $\\pi\\displaystyle\\int(f^2-g^2)\\,dx$ であり $\\pi\\displaystyle\\int(f-g)^2\\,dx$ ではないことを、ドーナツ型の断面で説明する。", caution="$(f-g)^2$ とする誤りが多い。"),
               tp("曲線の長さでは $\\sqrt{A^2}=|A|$ に注意させ、区間で $A$ の符号が変わるときは区間を分けさせる。")],
              misconceptions=[("定積分で置換したのに積分区間を $x$ のままにする", "$t=g(x)$ に対応する区間 $g(a)$ から $g(b)$ に取りかえる"),
                              ("$\\displaystyle\\int\\log x\\,dx=\\dfrac{1}{x}+C$", "それは微分。部分積分で $x\\log x-x+C$"),
                              ("2曲線の間の回転体を $\\pi\\displaystyle\\int(f-g)^2\\,dx$ とする", "外側の円から内側の円を除くので $\\pi\\displaystyle\\int(f^2-g^2)\\,dx$")]),
        summary("sm1", "まとめ",
                ["置換積分法は合成関数の微分法の逆、部分積分法は積の微分法の逆。定積分の置換では区間も取りかえる。",
                 "区分求積法 $\\displaystyle\\lim_{n\\to\\infty}\\dfrac{1}{n}\\sum_{k=1}^{n}f\\left(\\dfrac{k}{n}\\right)=\\int_0^1f(x)\\,dx$ が、面積・体積・長さの公式の土台になる。",
                 "体積 $V=\\displaystyle\\int_a^bS(x)\\,dx$、回転体 $V=\\pi\\displaystyle\\int_a^by^2\\,dx$、曲線の長さ $L=\\displaystyle\\int\\sqrt{\\left(\\frac{dx}{dt}\\right)^2+\\left(\\frac{dy}{dt}\\right)^2}\\,dt$。"]),
        check("ck1", "確認問題",
              [("$\\displaystyle\\int\\dfrac{2x}{x^2+3}\\,dx$ を求めよ。", "$\\log(x^2+3)+C$"), ("$\\displaystyle\\int_0^{\\pi}x\\sin x\\,dx$ を求めよ。", "$\\Bigl[-x\\cos x+\\sin x\\Bigr]_0^{\\pi}=\\pi$"),
               ("$y=\\sqrt{x}\\ (0\\leqq x\\leqq4)$ を $x$ 軸のまわりに回転した立体の体積は？", "$\\pi\\displaystyle\\int_0^4x\\,dx=8\\pi$")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

@gen("basic_check", 5, ["computation"])
def basic_indef(r):
    kind = r.choice(["pow", "pow", "recip", "exp", "ax", "trig", "trig", "sec2"])
    if kind == "pow":
        k = r.randint(1, 6)
        ftex, fpy, Ftex, Fpy = r.choice([
            (f"{cf(k)}\\sqrt{{x}}", f"{k}*sqrt(x)", f"{kfrac(F(2 * k, 3), 'x' + chr(92) + 'sqrt{x}')}", f"Rational({2 * k},3)*x*sqrt(x)"),
            (f"\\dfrac{{{k}}}{{x^2}}", f"{k}/x**2", f"-\\dfrac{{{k}}}{{x}}", f"-{k}/x"),
            (f"\\dfrac{{{k}}}{{\\sqrt{{x}}}}", f"{k}/sqrt(x)", f"{2 * k}\\sqrt{{x}}", f"{2 * k}*sqrt(x)"),
            (f"{cf(k)}\\sqrt[3]{{x}}", f"{k}*x**Rational(1,3)", f"{kfrac(F(3 * k, 4), 'x' + chr(92) + 'sqrt[3]{x}')}", f"Rational({3 * k},4)*x**Rational(4,3)"),
            (f"\\dfrac{{{k}}}{{x^3}}", f"{k}/x**3", f"-\\dfrac{{{k}}}{{2x^2}}", f"-{k}/(2*x**2)"),
        ])
        ap = "根号や分数を $x^r$ の形に直し、$\\displaystyle\\int x^r\\,dx=\\dfrac{x^{r+1}}{r+1}+C$ を使う。"
    elif kind == "recip":
        a, b = r.randint(1, 5), r.randint(-4, 6)
        ftex, fpy = f"\\dfrac{{1}}{{{lin(a, b)}}}", f"1/({a}*x+({b}))"
        Ftex, Fpy = kfrac(F(1, a), f"\\log|{lin(a, b)}|"), f"log({a}*x+({b}))/{a}"
        ap = "$\\displaystyle\\int\\dfrac{dx}{x}=\\log|x|+C$ と、$\\displaystyle\\int f(ax+b)\\,dx=\\dfrac{1}{a}F(ax+b)+C$ を組み合わせる。"
    elif kind == "exp":
        a, b = nonzero(r, -4, 4), r.randint(-3, 3)
        ftex, fpy = f"e^{{{lin(a, b)}}}", f"exp({a}*x+({b}))"
        Ftex, Fpy = kfrac(F(1, a), f"e^{{{lin(a, b)}}}"), f"exp({a}*x+({b}))/({a})"
        ap = "$\\displaystyle\\int e^x\\,dx=e^x+C$。中身が1次式 $ax+b$ なので $\\dfrac{1}{a}$ 倍する。"
    elif kind == "ax":
        c, k = r.choice([2, 3, 5, 10]), r.randint(1, 4)
        ftex, fpy = (f"{c}^x" if k == 1 else f"{k}\\cdot {c}^x"), f"{k}*{c}**x"
        Ftex, Fpy = f"\\dfrac{{{'' if k == 1 else k}{c}^x}}{{\\log {c}}}" if k == 1 else f"\\dfrac{{{k}\\cdot {c}^x}}{{\\log {c}}}", f"{k}*{c}**x/log({c})"
        ap = "$(a^x)'=a^x\\log a$ を逆に使い、$\\displaystyle\\int a^x\\,dx=\\dfrac{a^x}{\\log a}+C$。"
    elif kind == "trig":
        a, b = r.randint(1, 5), r.randint(-3, 3)
        g = r.choice(["sin", "cos"])
        arg = lin(a, b)
        A = f"({arg})" if b else arg
        ftex, fpy = f"\\{g} {A}", f"{g}({a}*x+({b}))"
        if g == "sin":
            Ftex, Fpy = "-" + kfrac(F(1, a), f"\\cos {A}"), f"-cos({a}*x+({b}))/{a}"
        else:
            Ftex, Fpy = kfrac(F(1, a), f"\\sin {A}"), f"sin({a}*x+({b}))/{a}"
        ap = "$\\displaystyle\\int\\sin x\\,dx=-\\cos x+C$、$\\displaystyle\\int\\cos x\\,dx=\\sin x+C$。中身が1次式なので係数で割る。"
    else:
        a = r.randint(1, 5)
        A = "x" if a == 1 else f"{a}x"
        ftex, fpy = f"\\dfrac{{1}}{{\\cos^2 {A}}}", f"1/cos({a}*x)**2"
        Ftex, Fpy = kfrac(F(1, a), f"\\tan {A}"), f"tan({a}*x)/{a}"
        ap = "$(\\tan x)'=\\dfrac{1}{\\cos^2x}$ を逆に使う。"
    return sa(f"不定積分 ${INT()}{ftex}\\,dx$ を求めなさい。", f"${Ftex}+C$（$C$ は積分定数）", "基本公式（微分の公式の逆）を使う。", d=2,
              ap=ap, steps=["被積分関数を基本公式が使える形に直す。", f"${Ftex}+C$。"],
              alt=[f"答え ${Ftex}$ を微分すると ${ftex}$ に戻ることを確かめる。"],
              pc=[("原始関数が正しい", 1), ("積分定数 $C$ を書いている", 1)],
              pit=["$\\displaystyle\\int\\sin x\\,dx=\\cos x$ と符号を誤る。", "中身の1次式の係数で割るのを忘れる。"],
              chk=(f"simplify(diff({Fpy}, x)-({fpy}))", "0"))


@gen("basic_check", 4, ["computation"])
def substitution(r):
    kind = r.choice(["lin_pow", "xquad", "xexp", "sincos", "fprime", "tan", "logx"])
    if kind == "lin_pow":
        a, b, n = r.randint(2, 5), nonzero(r, -5, 5), r.randint(2, 6)
        ftex, fpy = f"({lin(a, b)})^{n}", f"({a}*x+({b}))**{n}"
        Ftex, Fpy = f"\\dfrac{{({lin(a, b)})^{{{n + 1}}}}}{{{a * (n + 1)}}}", f"({a}*x+({b}))**{n + 1}/{a * (n + 1)}"
        st = [f"$t={lin(a, b)}$ とおくと $dt={a}\\,dx$。", f"${INT()}t^{n}\\cdot\\dfrac{{1}}{{{a}}}\\,dt=\\dfrac{{t^{{{n + 1}}}}}{{{a * (n + 1)}}}+C$。"]
    elif kind == "xquad":
        c, n = nonzero(r, -5, 6), r.randint(2, 5)
        ftex, fpy = f"x(x^2{tf_(c)})^{n}", f"x*(x**2+({c}))**{n}"
        Ftex, Fpy = f"\\dfrac{{(x^2{tf_(c)})^{{{n + 1}}}}}{{{2 * (n + 1)}}}", f"(x**2+({c}))**{n + 1}/{2 * (n + 1)}"
        st = [f"$t=x^2{tf_(c)}$ とおくと $dt=2x\\,dx$、$x\\,dx=\\dfrac{{1}}{{2}}dt$。", f"${INT()}\\dfrac{{1}}{{2}}t^{n}\\,dt=\\dfrac{{t^{{{n + 1}}}}}{{{2 * (n + 1)}}}+C$。"]
    elif kind == "xexp":
        a = r.choice([1, 2, 3, -1, -2])
        A = cf(a)
        ftex, fpy = f"xe^{{{A}x^2}}", f"x*exp({a}*x**2)"
        Ftex, Fpy = kfrac(F(1, 2 * a), f"e^{{{A}x^2}}"), f"exp({a}*x**2)/({2 * a})"
        st = [f"$t={A}x^2$ とおくと $dt={cf(2 * a)}x\\,dx$。".replace("=x", "=x"), f"${INT()}e^t\\cdot {ft(F(1, 2 * a))}\\,dt={kfrac(F(1, 2 * a), 'e^t')}+C$。"]
    elif kind == "sincos":
        n = r.randint(2, 6)
        g = r.choice(["sin", "cos"])
        h = "cos" if g == "sin" else "sin"
        ftex, fpy = f"\\{g}^{n} x\\{h} x", f"{g}(x)**{n}*{h}(x)"
        if g == "sin":
            Ftex, Fpy = f"\\dfrac{{\\sin^{{{n + 1}}}x}}{{{n + 1}}}", f"sin(x)**{n + 1}/{n + 1}"
        else:
            Ftex, Fpy = f"-\\dfrac{{\\cos^{{{n + 1}}}x}}{{{n + 1}}}", f"-cos(x)**{n + 1}/{n + 1}"
        st = [f"$t=\\{g} x$ とおくと $dt={'' if g == 'sin' else '-'}\\{h} x\\,dx$。", f"${INT()}{'' if g == 'sin' else '-'}t^{n}\\,dt={'' if g == 'sin' else '-'}\\dfrac{{t^{{{n + 1}}}}}{{{n + 1}}}+C$。"]
    elif kind == "fprime":
        a, c = r.randint(1, 4), r.randint(1, 9)
        ftex, fpy = f"\\dfrac{{{2 * a}x}}{{{cf(a)}x^2+{c}}}", f"{2 * a}*x/({a}*x**2+{c})"
        Ftex, Fpy = f"\\log({cf(a)}x^2+{c})", f"log({a}*x**2+{c})"
        st = [f"分子 ${2 * a}x$ は分母 ${cf(a)}x^2+{c}$ の導関数。", f"${INT()}\\dfrac{{g'(x)}}{{g(x)}}\\,dx=\\log|g(x)|+C$ で、${cf(a)}x^2+{c}>0$ より絶対値は不要。"]
    elif kind == "tan":
        a = r.randint(1, 4)
        A = "x" if a == 1 else f"{a}x"
        ftex, fpy = f"\\tan {A}", f"tan({a}*x)"
        Ftex, Fpy = "-" + kfrac(F(1, a), f"\\log|\\cos {A}|"), f"-log(cos({a}*x))/{a}"
        st = [f"$\\tan {A}=\\dfrac{{\\sin {A}}}{{\\cos {A}}}$ で、分子は分母の導関数の $-{ft(F(1, a))}$ 倍。".replace("$-1$", "$-1$"),
              f"${INT()}\\dfrac{{g'(x)}}{{g(x)}}\\,dx=\\log|g(x)|+C$ を用いる。"]
    else:
        n = r.randint(1, 4)
        ftex = "\\dfrac{\\log x}{x}" if n == 1 else f"\\dfrac{{(\\log x)^{n}}}{{x}}"
        fpy = f"log(x)**{n}/x"
        Ftex, Fpy = f"\\dfrac{{(\\log x)^{{{n + 1}}}}}{{{n + 1}}}", f"log(x)**{n + 1}/{n + 1}"
        st = ["$t=\\log x$ とおくと $dt=\\dfrac{1}{x}\\,dx$。", f"${INT()}t^{n}\\,dt=\\dfrac{{t^{{{n + 1}}}}}{{{n + 1}}}+C$。"]
    return sa(f"置換積分法を用いて、不定積分 ${INT()}{ftex}\\,dx$ を求めなさい。", f"${Ftex}+C$", "中身を $t$ とおき、$dt$ を $dx$ で表して置きかえる。", d=2,
              ap="被積分関数の中に「ある関数 $g(x)$」と「その導関数 $g'(x)$」が組で現れているかを探し、$t=g(x)$ とおく。",
              steps=st + [f"$x$ に戻して ${Ftex}+C$。"],
              alt=[f"答えを微分して ${ftex}$ に戻ることを確かめる。"],
              pc=[("適切な置換をして $dx$ を $dt$ で表している", 1), ("原始関数が正しい（積分定数を含む）", 1)],
              pit=["$dx$ を $dt$ に置きかえるときの係数を落とす。", "最後に $x$ の式に戻し忘れる。"],
              chk=(f"simplify(diff({Fpy}, x)-({fpy}))", "0"))


@gen("basic_check", 4, ["computation"])
def by_parts(r):
    kind = r.choice(["xexp", "xsin", "xcos", "log", "xnlog", "x2exp"])
    if kind == "xexp":
        a = nonzero(r, -3, 3)
        ftex, fpy = f"xe^{{{cf(a)}x}}", f"x*exp({a}*x)"
        k = F(1, a)
        Ftex = f"\\left({kfrac(k, 'x')}{'-' if k * k > 0 else '+'}{ft(k * k)}\\right)e^{{{cf(a)}x}}"
        Fpy = f"({fp(k)}*x-({fp(k * k)}))*exp({a}*x)"
        st = [f"$f=x,\\ g'=e^{{{cf(a)}x}}$ とすると $g={kfrac(k, 'e^{' + cf(a) + 'x}')}$。", f"${INT()}xe^{{{cf(a)}x}}\\,dx={kfrac(k, 'xe^{' + cf(a) + 'x}')}-{INT()}{kfrac(k, 'e^{' + cf(a) + 'x}')}\\,dx$。".replace("--", "+")]
    elif kind in ("xsin", "xcos"):
        a = r.randint(1, 4)
        A = "x" if a == 1 else f"{a}x"
        k = F(1, a)
        if kind == "xsin":
            ftex, fpy = f"x\\sin {A}", f"x*sin({a}*x)"
            Ftex = f"-{kfrac(k, 'x' + chr(92) + 'cos ' + A)}+{kfrac(k * k, chr(92) + 'sin ' + A)}"
            Fpy = f"-{fp(k)}*x*cos({a}*x)+{fp(k * k)}*sin({a}*x)"
            st = [f"$f=x,\\ g'=\\sin {A}$ とすると $g=-{kfrac(k, chr(92) + 'cos ' + A)}$。", f"$-{kfrac(k, 'x' + chr(92) + 'cos ' + A)}+{INT()}{kfrac(k, chr(92) + 'cos ' + A)}\\,dx$。"]
        else:
            ftex, fpy = f"x\\cos {A}", f"x*cos({a}*x)"
            Ftex = f"{kfrac(k, 'x' + chr(92) + 'sin ' + A)}+{kfrac(k * k, chr(92) + 'cos ' + A)}"
            Fpy = f"{fp(k)}*x*sin({a}*x)+{fp(k * k)}*cos({a}*x)"
            st = [f"$f=x,\\ g'=\\cos {A}$ とすると $g={kfrac(k, chr(92) + 'sin ' + A)}$。", f"${kfrac(k, 'x' + chr(92) + 'sin ' + A)}-{INT()}{kfrac(k, chr(92) + 'sin ' + A)}\\,dx$。"]
    elif kind == "log":
        a = r.randint(1, 4)
        A = "x" if a == 1 else f"{a}x"
        ftex, fpy = f"\\log {A}", f"log({a}*x)"
        Ftex, Fpy = f"x\\log {A}-x", f"x*log({a}*x)-x"
        st = [f"$\\log {A}=(\\log {A})\\cdot(x)'$ と見て、$f=\\log {A},\\ g'=1$ とする。", f"$x\\log {A}-{INT()}x\\cdot\\dfrac{{1}}{{x}}\\,dx$。"]
    elif kind == "xnlog":
        n = r.randint(1, 4)
        xn = "x" if n == 1 else f"x^{n}"
        ftex, fpy = f"{xn}\\log x", f"x**{n}*log(x)"
        Ftex = f"\\dfrac{{x^{{{n + 1}}}}}{{{n + 1}}}\\log x-\\dfrac{{x^{{{n + 1}}}}}{{{(n + 1) ** 2}}}"
        Fpy = f"x**{n + 1}/{n + 1}*log(x)-x**{n + 1}/{(n + 1) ** 2}"
        st = [f"$f=\\log x,\\ g'={xn}$ とすると $g=\\dfrac{{x^{{{n + 1}}}}}{{{n + 1}}}$。", f"$\\dfrac{{x^{{{n + 1}}}}}{{{n + 1}}}\\log x-{INT()}\\dfrac{{x^{{{n}}}}}{{{n + 1}}}\\,dx$。".replace("x^{1}", "x")]
    else:
        ftex, fpy = "x^2e^x", "x**2*exp(x)"
        sgn = r.choice([1, -1])
        if sgn == -1:
            ftex, fpy = "x^2e^{-x}", "x**2*exp(-x)"
            Ftex, Fpy = "-(x^2+2x+2)e^{-x}", "-(x**2+2*x+2)*exp(-x)"
            st = ["$f=x^2,\\ g'=e^{-x}$ として $-x^2e^{-x}+2\\displaystyle\\int xe^{-x}\\,dx$。", "もう一度部分積分して $\\displaystyle\\int xe^{-x}\\,dx=-(x+1)e^{-x}+C$。"]
        else:
            Ftex, Fpy = "(x^2-2x+2)e^x", "(x**2-2*x+2)*exp(x)"
            st = ["$f=x^2,\\ g'=e^x$ として $x^2e^x-2\\displaystyle\\int xe^x\\,dx$。", "もう一度部分積分して $\\displaystyle\\int xe^x\\,dx=(x-1)e^x+C$。"]
    return sa(f"部分積分法を用いて、不定積分 ${INT()}{ftex}\\,dx$ を求めなさい。", f"${Ftex}+C$", "$\\displaystyle\\int fg'\\,dx=fg-\\int f'g\\,dx$。", d=2,
              ap="微分すると簡単になる方（$x^n$ や $\\log x$）を $f$、積分しやすい方を $g'$ にとって部分積分する。",
              steps=st + [f"整理して ${Ftex}+C$。"],
              alt=["答えを微分して被積分関数に戻ることを確かめる（積の微分法を使う）。"],
              pc=[("$f,\\ g'$ を適切に選んで部分積分している", 1), ("原始関数が正しい（積分定数を含む）", 1)],
              pit=["$f$ と $g'$ の選び方を逆にして、かえって複雑になる。", "$-\\displaystyle\\int f'g\\,dx$ の符号を誤る。"],
              chk=(f"simplify(diff({Fpy}, x)-({fpy}))", "0"))


@gen("basic_check", 4, ["computation"])
def definite_basic(r):
    kind = r.choice(["recip", "exp", "sin", "cos", "recip2", "sqrt"])
    if kind == "recip":
        k = r.randint(1, 4)
        up = "e" if k == 1 else f"e^{k}"
        tex, py, val, vtex = f"{INT(1, up)}\\dfrac{{1}}{{x}}\\,dx", f"integrate(1/x, [x, 1, exp({k})])", str(k), f"{k}"
        st = [f"$\\Bigl[\\log x\\Bigr]_1^{{{up}}}=\\log {up}-\\log 1={k}$。"]
    elif kind == "exp":
        a = nonzero(r, -3, 3)
        b = r.randint(1, 2)
        V = (sp.exp(a * b) - 1) / a
        tex, py = f"{INT(0, b)}e^{{{cf(a)}x}}\\,dx", f"integrate(exp({a}*x), [x, 0, {b}])"
        val = sp.sstr(V)
        vtex = (f"\\dfrac{{e^{{{a * b}}}-1}}{{{a}}}" if a > 0 else f"\\dfrac{{1-e^{{{a * b}}}}}{{{-a}}}").replace("{1}}-1}{1}", "")
        if a == 1:
            vtex = f"e^{{{b}}}-1" if b > 1 else "e-1"
        if a == -1:
            vtex = f"1-e^{{{-b}}}" if b > 1 else "1-\\dfrac{1}{e}"
        st = [f"$\\Bigl[{kfrac(F(1, a), 'e^{' + cf(a) + 'x}')}\\Bigr]_0^{{{b}}}$。", f"$={vtex}$。"]
    elif kind == "sin":
        a = r.randint(1, 4)
        A = "x" if a == 1 else f"{a}x"
        up = "\\pi" if a == 1 else f"\\dfrac{{\\pi}}{{{a}}}"
        tex, py, val, vtex = f"{INT(0, up)}\\sin {A}\\,dx", f"integrate(sin({a}*x), [x, 0, pi/{a}])", fp(F(2, a)), ft(F(2, a))
        st = [f"$\\Bigl[-{kfrac(F(1, a), chr(92) + 'cos ' + A)}\\Bigr]_0^{{{up}}}$。", f"$={ft(F(1, a))}-(-{ft(F(1, a))})={ft(F(2, a))}$。".replace("=1-(-1)", "=1-(-1)")]
    elif kind == "cos":
        a = r.randint(1, 4)
        A = "x" if a == 1 else f"{a}x"
        up = "\\dfrac{\\pi}{2}" if a == 1 else f"\\dfrac{{\\pi}}{{{2 * a}}}"
        tex, py, val, vtex = f"{INT(0, up)}\\cos {A}\\,dx", f"integrate(cos({a}*x), [x, 0, pi/{2 * a}])", fp(F(1, a)), ft(F(1, a))
        st = [f"$\\Bigl[{kfrac(F(1, a), chr(92) + 'sin ' + A)}\\Bigr]_0^{{{up}}}={ft(F(1, a))}$。"]
    elif kind == "recip2":
        a, b = sorted(r.sample(range(1, 7), 2))
        V = F(1, a) - F(1, b)
        tex, py, val, vtex = f"{INT(a, b)}\\dfrac{{dx}}{{x^2}}", f"integrate(1/x**2, [x, {a}, {b}])", fp(V), ft(V)
        st = [f"$\\Bigl[-\\dfrac{{1}}{{x}}\\Bigr]_{{{a}}}^{{{b}}}=-\\dfrac{{1}}{{{b}}}+\\dfrac{{1}}{{{a}}}={ft(V)}$。".replace("\\dfrac{1}{1}", "1")]
    else:
        s = r.randint(2, 5)
        V = F(2, 3) * s ** 3
        tex, py, val, vtex = f"{INT(0, s * s)}\\sqrt{{x}}\\,dx", f"integrate(sqrt(x), [x, 0, {s * s}])", fp(V), ft(V)
        st = [f"$\\Bigl[\\dfrac{{2}}{{3}}x\\sqrt{{x}}\\Bigr]_0^{{{s * s}}}=\\dfrac{{2}}{{3}}\\cdot {s * s}\\cdot {s}={ft(V)}$。"]
    return sa(f"定積分 ${tex}$ の値を求めなさい。", f"${vtex}$", "原始関数を求め、上端の値から下端の値を引く。", d=2,
              ap="基本公式で原始関数 $F(x)$ を求め、$F(\\text{上端})-F(\\text{下端})$ を計算する。",
              steps=st, alt=["被積分関数のグラフをかき、面積として値の大きさの見当をつけて検算する。"],
              pc=[("原始関数が正しい", 1), ("値が正しい", 1)],
              pit=["$\\cos$ の原始関数の符号を誤る。", "上端と下端を逆に引く。"], chk=(py, val))


RIEM = [  # (和の LaTeX, f(x) の LaTeX, f の式, 値の LaTeX, 値の式)
    lambda m: (f"\\dfrac{{1}}{{n^{{{m + 1}}}}}\\sum_{{k=1}}^{{n}}k^{m}" if m > 1 else "\\dfrac{1}{n^2}\\sum_{k=1}^{n}k", f"x^{m}" if m > 1 else "x", f"x**{m}", ft(F(1, m + 1)), fp(F(1, m + 1))),
    lambda m: ("\\sum_{k=1}^{n}\\dfrac{1}{n+k}", "\\dfrac{1}{1+x}", "1/(1+x)", "\\log 2", "log(2)"),
    lambda m: ("\\sum_{k=1}^{n}\\dfrac{n}{n^2+k^2}", "\\dfrac{1}{1+x^2}", "1/(1+x**2)", "\\dfrac{\\pi}{4}", "pi/4"),
    lambda m: ("\\dfrac{1}{n}\\sum_{k=1}^{n}e^{\\frac{k}{n}}", "e^x", "exp(x)", "e-1", "E-1"),
    lambda m: ("\\dfrac{1}{n}\\sum_{k=1}^{n}\\sqrt{\\dfrac{k}{n}}", "\\sqrt{x}", "sqrt(x)", "\\dfrac{2}{3}", "Rational(2,3)"),
    lambda m: ("\\dfrac{\\pi}{n}\\sum_{k=1}^{n}\\sin\\dfrac{k\\pi}{n}", "\\pi\\sin\\pi x", "pi*sin(pi*x)", "2", "2"),
    lambda m: ("\\sum_{k=1}^{n}\\dfrac{k}{n^2+k^2}", "\\dfrac{x}{1+x^2}", "x/(1+x**2)", "\\dfrac{1}{2}\\log 2", "log(2)/2"),
]


@gen("basic_check", 3, ["computation", "concept", "cross_unit"], rel=["HS-MATH3-U01", "HS-MATHB-U01"])
def riemann_sum(r):
    m = r.randint(1, 5)
    stex, ftex, fpy, vtex, vpy = r.choice(RIEM)(m)
    return sa(f"区分求積法を用いて、極限 $\\displaystyle\\lim_{{n\\to\\infty}}{stex}$ を求めなさい。", f"${vtex}$",
              f"$\\dfrac{{1}}{{n}}\\displaystyle\\sum_{{k=1}}^{{n}}f\\left(\\dfrac{{k}}{{n}}\\right)$ の形に直すと $f(x)={ftex}$。極限は $\\displaystyle\\int_0^1{ftex}\\,dx={vtex}$。", d=3,
              ap="和を $\\dfrac{1}{n}\\displaystyle\\sum_{k=1}^{n}f\\left(\\dfrac{k}{n}\\right)$ の形（$\\dfrac{1}{n}$ をくくり出し、残りを $\\dfrac{k}{n}$ だけで表す）に直し、$\\displaystyle\\int_0^1f(x)\\,dx$ に置きかえる。",
              steps=["$\\dfrac{1}{n}$ をくくり出し、残りの各項を $\\dfrac{k}{n}$ の式で表す。", f"$f(x)={ftex}$ として $\\displaystyle\\lim_{{n\\to\\infty}}\\dfrac{{1}}{{n}}\\sum_{{k=1}}^{{n}}f\\left(\\dfrac{{k}}{{n}}\\right)=\\int_0^1{ftex}\\,dx$。",
                     f"定積分を計算して ${vtex}$。"],
              alt=["$\\displaystyle\\sum k^m$ の場合は、和の公式（数学B）で和を求めてから $n\\to\\infty$ としても同じ結果になる。" if "k^" in stex or stex.endswith("k") else
                   "$n=100$ などで和を数値計算すると、極限の値に近いことが確かめられる。"],
              pc=[("$\\dfrac{1}{n}\\sum f\\left(\\frac{k}{n}\\right)$ の形に正しく変形している", 1), ("定積分の値が正しい", 1)],
              pit=["$\\dfrac{1}{n}$ をくくり出さずに $f$ を決めてしまう。", "積分区間を $0$ から $n$ のようにしてしまう。"],
              chk=(f"integrate({fpy}, [x, 0, 1])", vpy))


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 4, ["computation", "condition_check"])
def def_subst(r):
    kind = r.choice(["circle", "atan", "xexp2", "sinpow", "sqrtlin"])
    if kind == "circle":
        a = r.randint(1, 5)
        V = sp.pi * a * a / 4
        tex, py = f"{INT(0, a)}\\sqrt{{{a * a}-x^2}}\\,dx", f"integrate(sqrt({a * a}-x**2), [x, 0, {a}])"
        st = [f"$x={a}\\sin\\theta$ とおくと $dx={a}\\cos\\theta\\,d\\theta$、$x:0\\to {a}$ のとき $\\theta:0\\to\\dfrac{{\\pi}}{{2}}$。",
              f"$0\\leqq\\theta\\leqq\\dfrac{{\\pi}}{{2}}$ で $\\cos\\theta\\geqq0$ より $\\sqrt{{{a * a}-{a * a}\\sin^2\\theta}}={a}\\cos\\theta$。",
              f"${a * a}{INT(0, chr(92) + 'frac{' + chr(92) + 'pi}{2}')}\\cos^2\\theta\\,d\\theta={a * a}\\cdot\\dfrac{{\\pi}}{{4}}={TX(V)}$。"]
        ap = f"$\\sqrt{{a^2-x^2}}$ は $x=a\\sin\\theta$ で根号が外れる。半径 ${a}$ の四分円の面積と一致するはず。"
    elif kind == "atan":
        a = r.randint(1, 5)
        up = r.choice([("a", 1), ("sa", 1)])
        if r.random() < 0.6:
            b, ang, btex = a, sp.pi / 4, str(a)
        else:
            b, ang, btex = sp.sqrt(3) * a, sp.pi / 3, (f"{a}\\sqrt{{3}}" if a > 1 else "\\sqrt{3}")
        V = ang / a
        tex, py = f"{INT(0, btex)}\\dfrac{{dx}}{{x^2+{a * a}}}", f"integrate(1/(x**2+{a * a}), [x, 0, {sp.sstr(b)}])"
        st = [f"$x={a}\\tan\\theta$ とおくと $dx=\\dfrac{{{a}}}{{\\cos^2\\theta}}\\,d\\theta$、$x:0\\to {btex}$ のとき $\\theta:0\\to {TX(ang)}$。",
              f"$x^2+{a * a}=\\dfrac{{{a * a}}}{{\\cos^2\\theta}}$ より、被積分関数と $dx$ の積は $\\dfrac{{1}}{{{a}}}\\,d\\theta$。", f"$\\dfrac{{1}}{{{a}}}\\cdot {TX(ang)}={TX(V)}$。".replace("\\dfrac{1}{1}\\cdot", "")]
        ap = "$\\dfrac{1}{x^2+a^2}$ は $x=a\\tan\\theta$ と置換すると、$1+\\tan^2\\theta=\\dfrac{1}{\\cos^2\\theta}$ により簡単になる。"
    elif kind == "xexp2":
        b = r.randint(1, 3)
        V = (sp.exp(b * b) - 1) / 2
        tex, py = f"{INT(0, b)}xe^{{x^2}}\\,dx", f"integrate(x*exp(x**2), [x, 0, {b}])"
        st = [f"$t=x^2$ とおくと $dt=2x\\,dx$、$x:0\\to {b}$ のとき $t:0\\to {b * b}$。", f"$\\dfrac{{1}}{{2}}{INT(0, b * b)}e^t\\,dt=\\dfrac{{1}}{{2}}(e^{{{b * b}}}-1)$。"]
        ap = "$x$ と $x^2$ の導関数 $2x$ の組に注目して $t=x^2$ とおく。区間も $t$ の区間に変える。"
    elif kind == "sinpow":
        n = r.randint(2, 6)
        V = sp.Rational(1, n + 1)
        g = r.choice(["sin", "cos"])
        h = "cos" if g == "sin" else "sin"
        tex, py = f"{INT(0, chr(92) + 'frac{' + chr(92) + 'pi}{2}')}\\{g}^{n} x\\{h} x\\,dx", f"integrate({g}(x)**{n}*{h}(x), [x, 0, pi/2])"
        if g == "sin":
            st = ["$t=\\sin x$ とおくと $dt=\\cos x\\,dx$、$x:0\\to\\dfrac{\\pi}{2}$ のとき $t:0\\to1$。", f"${INT(0, 1)}t^{n}\\,dt=\\dfrac{{1}}{{{n + 1}}}$。"]
        else:
            st = ["$t=\\cos x$ とおくと $dt=-\\sin x\\,dx$、$x:0\\to\\dfrac{\\pi}{2}$ のとき $t:1\\to0$。", f"${INT(1, 0)}t^{n}\\cdot(-1)\\,dt={INT(0, 1)}t^{n}\\,dt=\\dfrac{{1}}{{{n + 1}}}$。"]
        ap = "$\\sin x$（または $\\cos x$）とその導関数の組に注目して置換する。区間の対応に注意する。"
    else:
        a = r.randint(1, 3)
        s = r.randint(2, 4)
        b = (s * s - 1)
        # ∫_0^b x/√(x+1) dx
        V = sp.integrate(X / sp.sqrt(X + 1), (X, 0, b))
        tex, py = f"{INT(0, b)}\\dfrac{{x}}{{\\sqrt{{x+1}}}}\\,dx", f"integrate(x/sqrt(x+1), [x, 0, {b}])"
        st = [f"$t=\\sqrt{{x+1}}$ とおくと $x=t^2-1$、$dx=2t\\,dt$、$x:0\\to {b}$ のとき $t:1\\to {s}$。", f"${INT(1, s)}\\dfrac{{t^2-1}}{{t}}\\cdot2t\\,dt=2{INT(1, s)}(t^2-1)\\,dt=2\\Bigl[\\dfrac{{t^3}}{{3}}-t\\Bigr]_1^{{{s}}}$。",
              f"$={TX(V)}$。"]
        ap = "根号の中が1次式のときは、根号全体を $t$ とおくと有理式になる。"
    return sa(f"定積分 ${tex}$ の値を求めなさい。", f"${TX(V)}$", "置換積分法を用いる。積分区間も新しい変数に対応させる。", d=3, ap=ap, steps=st,
              alt=["置換した後の区間を使わず、いったん不定積分を $x$ の式に戻してから元の区間で計算しても同じ値になる。"],
              pc=[("適切な置換をしている", 1), ("積分区間を正しく取りかえている", 1), ("値が正しい", 2)],
              pit=["積分区間を $x$ の区間のまま使う。", "$\\sqrt{\\cos^2\\theta}=\\cos\\theta$ とするとき、符号を確かめない。"], chk=(py, sp.sstr(V)))


@gen("standard_practice", 4, ["computation", "multiple_solutions"])
def def_parts(r):
    kind = r.choice(["xsin", "xcos", "log", "xnlog", "xexp", "log2"])
    if kind == "xsin":
        tex, py, V = f"{INT(0, chr(92) + 'pi')}x\\sin x\\,dx", "integrate(x*sin(x), [x, 0, pi])", sp.pi
        st = ["$\\Bigl[-x\\cos x\\Bigr]_0^{\\pi}+\\displaystyle\\int_0^{\\pi}\\cos x\\,dx$。", "$=\\pi+\\Bigl[\\sin x\\Bigr]_0^{\\pi}=\\pi$。"]
        k = r.randint(1, 3)
        if k > 1:
            tex, py = f"{INT(0, chr(92) + 'pi')}x\\sin {k}x\\,dx", f"integrate(x*sin({k}*x), [x, 0, pi])"
            V = sp.integrate(X * sp.sin(k * X), (X, 0, sp.pi))
            st = [f"$\\Bigl[-\\dfrac{{x\\cos {k}x}}{{{k}}}\\Bigr]_0^{{\\pi}}+\\dfrac{{1}}{{{k}}}\\displaystyle\\int_0^{{\\pi}}\\cos {k}x\\,dx$。", f"$={TX(V)}+0={TX(V)}$。"]
    elif kind == "xcos":
        tex, py, V = f"{INT(0, chr(92) + 'frac{' + chr(92) + 'pi}{2}')}x\\cos x\\,dx", "integrate(x*cos(x), [x, 0, pi/2])", sp.pi / 2 - 1
        st = ["$\\Bigl[x\\sin x\\Bigr]_0^{\\frac{\\pi}{2}}-\\displaystyle\\int_0^{\\frac{\\pi}{2}}\\sin x\\,dx$。", "$=\\dfrac{\\pi}{2}+\\Bigl[\\cos x\\Bigr]_0^{\\frac{\\pi}{2}}=\\dfrac{\\pi}{2}-1$。"]
    elif kind == "log":
        k = r.randint(1, 3)
        up = "e" if k == 1 else f"e^{k}"
        V = sp.integrate(sp.log(X), (X, 1, sp.E ** k))
        tex, py = f"{INT(1, up)}\\log x\\,dx", f"integrate(log(x), [x, 1, exp({k})])"
        st = [f"$\\Bigl[x\\log x-x\\Bigr]_1^{{{up}}}$。", f"$=({up}\\cdot {k}-{up})-(0-1)={TX(sp.expand(V))}$。"]
        V = sp.expand(V)
    elif kind == "xnlog":
        n = r.randint(1, 3)
        xn = "x" if n == 1 else f"x^{n}"
        V = sp.expand(sp.integrate(X ** n * sp.log(X), (X, 1, sp.E)))
        tex, py = f"{INT(1, 'e')}{xn}\\log x\\,dx", f"integrate(x**{n}*log(x), [x, 1, E])"
        st = [f"$\\Bigl[\\dfrac{{x^{{{n + 1}}}}}{{{n + 1}}}\\log x\\Bigr]_1^e-\\dfrac{{1}}{{{n + 1}}}\\displaystyle\\int_1^ex^{{{n}}}\\,dx$。".replace("x^{1}", "x"),
              f"$=\\dfrac{{e^{{{n + 1}}}}}{{{n + 1}}}-\\dfrac{{e^{{{n + 1}}}-1}}{{{(n + 1) ** 2}}}={TX(V)}$。"]
    elif kind == "xexp":
        a = r.choice([1, 2, -1])
        V = sp.integrate(X * sp.exp(a * X), (X, 0, 1))
        V = sp.simplify(V)
        tex, py = f"{INT(0, 1)}xe^{{{cf(a)}x}}\\,dx", f"integrate(x*exp({a}*x), [x, 0, 1])"
        st = [f"$\\Bigl[{kfrac(F(1, a), 'xe^{' + cf(a) + 'x}')}\\Bigr]_0^1-{ft(F(1, a))}{INT(0, 1)}e^{{{cf(a)}x}}\\,dx$。".replace("--", "+"), f"$={TX(V)}$。"]
    else:
        V = sp.E - 2
        tex, py = f"{INT(1, 'e')}(\\log x)^2\\,dx", "integrate(log(x)**2, [x, 1, E])"
        st = ["$\\Bigl[x(\\log x)^2\\Bigr]_1^e-\\displaystyle\\int_1^e2\\log x\\,dx$。", "$=e-2\\Bigl[x\\log x-x\\Bigr]_1^e=e-2\\cdot1=e-2$。"]
    return sa(f"定積分 ${tex}$ の値を求めなさい。", f"${TX(V)}$", "部分積分法 $\\displaystyle\\int_a^bfg'\\,dx=\\Bigl[fg\\Bigr]_a^b-\\int_a^bf'g\\,dx$ を用いる。", d=3,
              ap="定積分の部分積分では、$\\Bigl[fg\\Bigr]_a^b$ の部分をその場で計算すると式が短くなる。",
              steps=st, alt=["先に不定積分（原始関数）を部分積分で求めてから、上端・下端を代入しても同じ値になる。"],
              pc=[("部分積分の式を正しく立てている", 2), ("各部分の計算が正しい", 1), ("値が正しい", 1)],
              pit=["$\\Bigl[fg\\Bigr]_a^b$ の計算で下端の値を引き忘れる。", "$-\\displaystyle\\int f'g\\,dx$ の符号を誤る。"], chk=(py, sp.sstr(V)))


@gen("standard_practice", 4, ["computation", "cross_unit"], rel=["HS-MATHC-U02"])
def area(r):
    kind = r.choice(["ellipse", "sqrtline", "sincos", "logarea", "recip"])
    rel = ["HS-MATH2-U06"]
    if kind == "ellipse":
        a, b = r.sample([1, 2, 3, 4, 5], 2)
        V = sp.pi * a * b
        stem = f"楕円 ${'x^2' if a == 1 else '\\dfrac{x^2}{' + str(a * a) + '}'}+{'y^2' if b == 1 else '\\dfrac{y^2}{' + str(b * b) + '}'}=1$ で囲まれた部分の面積を、定積分を用いて求めなさい。"
        st = [f"$y\\geqq0$ の部分は $y=\\dfrac{{{b}}}{{{a}}}\\sqrt{{{a * a}-x^2}}$。対称性から面積は第1象限の部分の4倍。", f"$S=4\\cdot\\dfrac{{{b}}}{{{a}}}{INT(0, a)}\\sqrt{{{a * a}-x^2}}\\,dx$。",
              f"定積分は半径 ${a}$ の四分円の面積 $\\dfrac{{{a * a}\\pi}}{{4}}$ なので、$S={TX(V)}$。"]
        py = f"4*Rational({b},{a})*integrate(sqrt({a * a}-x**2), [x, 0, {a}])"
        rel = ["HS-MATHC-U02"]
        ap = "楕円は $x$ 軸・$y$ 軸に関して対称。第1象限の部分を求めて4倍する。根号の積分は円の面積に帰着する（または $x=a\\sin\\theta$ と置換）。"
    elif kind == "sqrtline":
        k = r.randint(1, 4)
        V = sp.Rational(k ** 3, 6)
        line = "x" if k == 1 else f"\\dfrac{{x}}{{{k}}}"
        stem = f"曲線 $y=\\sqrt{{x}}$ と直線 $y={line}$ で囲まれた部分の面積を求めなさい。"
        st = [f"交点：$\\sqrt{{x}}={line}$ より $x=0,\\ {k * k}$。", f"$0<x<{k * k}$ では $\\sqrt{{x}}>{line}$。",
              f"$S={INT(0, k * k)}\\left(\\sqrt{{x}}-{line}\\right)dx=\\Bigl[\\dfrac{{2}}{{3}}x\\sqrt{{x}}-\\dfrac{{x^2}}{{{2 * k}}}\\Bigr]_0^{{{k * k}}}={TX(V)}$。"]
        py = f"integrate(sqrt(x)-x/{k}, [x, 0, {k * k}])"
        ap = "交点を求めて積分区間を決め、「上の関数－下の関数」を積分する。"
    elif kind == "sincos":
        V = 2 * sp.sqrt(2)
        stem = "$\\dfrac{\\pi}{4}\\leqq x\\leqq\\dfrac{5}{4}\\pi$ の範囲で、2曲線 $y=\\sin x$、$y=\\cos x$ で囲まれた部分の面積を求めなさい。"
        if r.random() < 0.5:
            stem = "2曲線 $y=\\sin x,\\ y=\\cos x\\ \\left(\\dfrac{\\pi}{4}\\leqq x\\leqq\\dfrac{5}{4}\\pi\\right)$ で囲まれた部分の面積を求めなさい。"
        st = ["交点は $\\tan x=1$ より $x=\\dfrac{\\pi}{4},\\ \\dfrac{5}{4}\\pi$。その間では $\\sin x\\geqq\\cos x$。",
              "$S=\\displaystyle\\int_{\\frac{\\pi}{4}}^{\\frac{5}{4}\\pi}(\\sin x-\\cos x)\\,dx=\\Bigl[-\\cos x-\\sin x\\Bigr]_{\\frac{\\pi}{4}}^{\\frac{5}{4}\\pi}$。", "$=\\sqrt{2}-(-\\sqrt{2})=2\\sqrt{2}$。"]
        py = "integrate(sin(x)-cos(x), [x, pi/4, 5*pi/4])"
        rel = ["HS-MATH2-U04"]
        ap = "交点を三角方程式で求め、区間内でどちらが上かを確かめてから積分する。"
    elif kind == "logarea":
        k = r.randint(1, 3)
        up = "e" if k == 1 else f"e^{k}"
        V = sp.expand(sp.integrate(sp.log(X), (X, 1, sp.E ** k)))
        stem = f"曲線 $y=\\log x$ と $x$ 軸、および直線 $x={up}$ で囲まれた部分の面積を求めなさい。"
        st = ["$y=\\log x$ は $x=1$ で $x$ 軸と交わり、$1\\leqq x\\leqq " + up + "$ で $y\\geqq0$。", f"$S={INT(1, up)}\\log x\\,dx=\\Bigl[x\\log x-x\\Bigr]_1^{{{up}}}={TX(V)}$。"]
        py = f"integrate(log(x), [x, 1, exp({k})])"
        rel = ["HS-MATH2-U05"]
        ap = "$x$ 軸との交点 $x=1$ を求めて積分区間を決める。$\\log x$ の原始関数は部分積分で求める。"
    else:
        a, m = r.randint(1, 4), r.choice([2, 3, 4])
        b = a * m
        V = sp.log(m)
        stem = f"曲線 $y=\\dfrac{{1}}{{x}}$ と $x$ 軸、および2直線 $x={a}$、$x={b}$ で囲まれた部分の面積を求めなさい。"
        st = [f"${a}\\leqq x\\leqq {b}$ で $\\dfrac{{1}}{{x}}>0$。", f"$S={INT(a, b)}\\dfrac{{dx}}{{x}}=\\log {b}-\\log {a}=\\log {m}$。".replace("-\\log 1", "")]
        py = f"integrate(1/x, [x, {a}, {b}])"
        rel = ["HS-MATH2-U05"]
        ap = "$\\displaystyle\\int\\dfrac{dx}{x}=\\log|x|+C$。対数の性質 $\\log b-\\log a=\\log\\dfrac{b}{a}$ で整理する。"
    vt = TX(V) if kind not in ("recip",) else f"\\log {m}"
    return sa(stem, f"${vt}$", "面積は「上の関数－下の関数」の定積分。", d=3, ap=ap, steps=st,
              alt=["図をかき、長方形や三角形などで大まかに見積もった値と比べて、答えの大きさが妥当か確かめる。"],
              pc=[("交点・上下関係を確かめて積分の式を立てている", 2), ("定積分の計算が正しい", 1), ("面積が正しい", 1)],
              pit=["上下関係を確かめずに積分し、負の値を出す。", "積分区間（交点）を誤る。"], chk=(py, sp.sstr(V)), rel=rel)


@gen("standard_practice", 4, ["computation", "application"])
def volume(r):
    kind = r.choice(["sqrt", "sin", "exp", "sphere", "ellipsoid", "parab", "cone"])
    if kind == "sqrt":
        a = r.randint(1, 6)
        V = sp.pi * a * a / 2
        stem = f"曲線 $y=\\sqrt{{x}}$ と $x$ 軸、直線 $x={a}$ で囲まれた部分を、$x$ 軸のまわりに1回転してできる立体の体積を求めなさい。"
        st = [f"$V=\\pi{INT(0, a)}(\\sqrt{{x}})^2\\,dx=\\pi{INT(0, a)}x\\,dx$。", f"$=\\pi\\cdot\\dfrac{{{a * a}}}{{2}}={TX(V)}$。"]
        py = f"pi*integrate(x, [x, 0, {a}])"
    elif kind == "sin":
        k = r.randint(1, 3)
        V = sp.pi ** 2 * k * k / 2
        stem = f"曲線 $y={cf(k)}\\sin x\\ (0\\leqq x\\leqq\\pi)$ と $x$ 軸で囲まれた部分を、$x$ 軸のまわりに1回転してできる立体の体積を求めなさい。"
        st = [f"$V=\\pi{INT(0, chr(92) + 'pi')}{k * k if k > 1 else ''}\\sin^2x\\,dx$。", "$\\sin^2x=\\dfrac{1-\\cos 2x}{2}$ より $\\displaystyle\\int_0^{\\pi}\\sin^2x\\,dx=\\dfrac{\\pi}{2}$。", f"$V={TX(V)}$。"]
        py = f"pi*integrate(({k}*sin(x))**2, [x, 0, pi])"
    elif kind == "exp":
        a = r.randint(1, 2)
        V = sp.pi * (sp.exp(2 * a) - 1) / 2
        stem = f"曲線 $y=e^x$ と $x$ 軸、$y$ 軸、直線 $x={a}$ で囲まれた部分を、$x$ 軸のまわりに1回転してできる立体の体積を求めなさい。"
        st = [f"$V=\\pi{INT(0, a)}e^{{2x}}\\,dx=\\pi\\Bigl[\\dfrac{{e^{{2x}}}}{{2}}\\Bigr]_0^{{{a}}}$。", f"$=\\dfrac{{\\pi(e^{{{2 * a}}}-1)}}{{2}}$。"]
        py = f"pi*integrate(exp(2*x), [x, 0, {a}])"
    elif kind == "sphere":
        R = r.randint(1, 6)
        V = sp.Rational(4, 3) * sp.pi * R ** 3
        stem = f"円 $x^2+y^2={R * R}$ の $y\\geqq0$ の部分と $x$ 軸で囲まれた部分を、$x$ 軸のまわりに1回転してできる球の体積を、定積分を用いて求めなさい。"
        st = [f"$y^2={R * R}-x^2$ より $V=\\pi{INT(-R, R)}({R * R}-x^2)\\,dx$。", f"偶関数なので $=2\\pi{INT(0, R)}({R * R}-x^2)\\,dx=2\\pi\\left({R ** 3}-\\dfrac{{{R ** 3}}}{{3}}\\right)={TX(V)}$。"]
        py = f"pi*integrate({R * R}-x**2, [x, {-R}, {R}])"
    elif kind == "ellipsoid":
        a, b = r.sample([1, 2, 3, 4], 2)
        V = sp.Rational(4, 3) * sp.pi * a * b * b
        stem = f"楕円 ${'x^2' if a == 1 else '\\dfrac{x^2}{' + str(a * a) + '}'}+{'y^2' if b == 1 else '\\dfrac{y^2}{' + str(b * b) + '}'}=1$ で囲まれた部分を、$x$ 軸のまわりに1回転してできる立体の体積を求めなさい。"
        st = [f"$y^2={b * b}\\left(1-\\dfrac{{x^2}}{{{a * a}}}\\right)$。", f"$V=\\pi{INT(-a, a)}{b * b}\\left(1-\\dfrac{{x^2}}{{{a * a}}}\\right)dx=2\\pi\\cdot {b * b}\\left({a}-\\dfrac{{{a}}}{{3}}\\right)={TX(V)}$。"]
        py = f"pi*integrate({b * b}*(1-x**2/{a * a}), [x, {-a}, {a}])"
    elif kind == "parab":
        a = r.randint(1, 3)
        V = sp.pi * a ** 5 / 5
        stem = f"放物線 $y=x^2$ と $x$ 軸、直線 $x={a}$ で囲まれた部分を、$x$ 軸のまわりに1回転してできる立体の体積を求めなさい。"
        st = [f"$V=\\pi{INT(0, a)}(x^2)^2\\,dx=\\pi{INT(0, a)}x^4\\,dx$。", f"$=\\pi\\cdot\\dfrac{{{a ** 5}}}{{5}}={TX(V)}$。"]
        py = f"pi*integrate(x**4, [x, 0, {a}])"
    else:
        rr, h = r.randint(1, 5), r.randint(1, 6)
        V = sp.pi * rr * rr * h / 3
        stem = f"直線 $y={'' if F(rr, h) == 1 else ft(F(rr, h))}x$ と $x$ 軸、直線 $x={h}$ で囲まれた部分を、$x$ 軸のまわりに1回転してできる円錐の体積を、定積分を用いて求めなさい。"
        st = [f"$V=\\pi{INT(0, h)}\\left({ft(F(rr, h))}x\\right)^2dx=\\pi\\cdot {ft(F(rr * rr, h * h))}\\cdot\\dfrac{{{h ** 3}}}{{3}}$。".replace("\\left(1x\\right)", "x"), f"$={TX(V)}$。"]
        py = f"pi*integrate((Rational({rr},{h})*x)**2, [x, 0, {h}])"
    vt = f"\\dfrac{{\\pi(e^{{{2 * a}}}-1)}}{{2}}" if kind == "exp" else TX(V)
    return sa(stem, f"${vt}$", "回転体の体積 $V=\\pi\\displaystyle\\int_a^b\\{f(x)\\}^2\\,dx$。", d=3,
              ap="$x$ 軸に垂直な平面で切った断面は半径 $|f(x)|$ の円。断面積 $\\pi\\{f(x)\\}^2$ を積分する。",
              steps=st, alt=["球・円錐など体積の公式が分かっている立体は、公式の値と一致するかで検算できる。" if kind in ("sphere", "cone", "ellipsoid") else
                             "円柱や円錐で外側・内側から見積もり、答えの大きさが妥当か確かめる。"],
              pc=[("体積を定積分で正しく表している", 2), ("積分の計算が正しい", 1), ("体積が正しい", 1)],
              pit=["$\\pi$ をかけ忘れる。", "$\\{f(x)\\}^2$ ではなく $f(x)$ を積分してしまう。"], chk=(py, sp.sstr(V)))


@gen("standard_practice", 4, ["computation", "cross_unit"], rel=["HS-MATHC-U02"])
def arc_length(r):
    kind = r.choice(["cycloid", "astroid", "catenary", "semicubic", "spiral"])
    if kind == "cycloid":
        a = r.randint(1, 5)
        V = sp.Integer(8 * a)
        stem = f"サイクロイド $x={cf(a)}(t-\\sin t),\\ y={cf(a)}(1-\\cos t)\\ (0\\leqq t\\leqq 2\\pi)$ の長さを求めなさい。"
        st = [f"$\\left(\\dfrac{{dx}}{{dt}}\\right)^2+\\left(\\dfrac{{dy}}{{dt}}\\right)^2={a * a}\\{{(1-\\cos t)^2+\\sin^2t\\}}={2 * a * a}(1-\\cos t)={4 * a * a}\\sin^2\\dfrac{{t}}{{2}}$。",
              f"$0\\leqq t\\leqq 2\\pi$ で $\\sin\\dfrac{{t}}{{2}}\\geqq0$ より $L={INT(0, '2' + chr(92) + 'pi')}{2 * a}\\sin\\dfrac{{t}}{{2}}\\,dt=\\Bigl[-{4 * a}\\cos\\dfrac{{t}}{{2}}\\Bigr]_0^{{2\\pi}}={8 * a}$。"]
        chk = (f"[simplify(diff({a}*(t-sin(t)), t)**2+diff({a}*(1-cos(t)), t)**2-{4 * a * a}*sin(t/2)**2), integrate({2 * a}*sin(t/2), [t, 0, 2*pi])]", f"[0, {8 * a}]", None, "intermediate")
        rel = ["HS-MATHC-U02"]
    elif kind == "astroid":
        a = r.randint(1, 5)
        V = sp.Integer(6 * a)
        stem = f"アステロイド $x={cf(a)}\\cos^3t,\\ y={cf(a)}\\sin^3t\\ (0\\leqq t\\leqq 2\\pi)$ の全長を求めなさい。"
        st = [f"$\\dfrac{{dx}}{{dt}}=-{3 * a}\\cos^2t\\sin t,\\ \\dfrac{{dy}}{{dt}}={3 * a}\\sin^2t\\cos t$。", f"$\\left(\\dfrac{{dx}}{{dt}}\\right)^2+\\left(\\dfrac{{dy}}{{dt}}\\right)^2={9 * a * a}\\sin^2t\\cos^2t$。",
              f"対称性から第1象限の部分（$0\\leqq t\\leqq\\dfrac{{\\pi}}{{2}}$）の4倍。$L=4{INT(0, chr(92) + 'frac{' + chr(92) + 'pi}{2}')}{3 * a}\\sin t\\cos t\\,dt=4\\cdot\\dfrac{{{3 * a}}}{{2}}={6 * a}$。"]
        chk = (f"[simplify(diff({a}*cos(t)**3, t)**2+diff({a}*sin(t)**3, t)**2-({3 * a}*sin(t)*cos(t))**2), 4*integrate({3 * a}*sin(t)*cos(t), [t, 0, pi/2])]", f"[0, {6 * a}]", None, "intermediate")
        rel = ["HS-MATHC-U02"]
    elif kind == "catenary":
        k = r.randint(2, 5)
        V = sp.Rational(k * k - 1, 2 * k)
        stem = f"曲線 $y=\\dfrac{{e^x+e^{{-x}}}}{{2}}\\ (0\\leqq x\\leqq\\log {k})$ の長さを求めなさい。"
        st = ["$y'=\\dfrac{e^x-e^{-x}}{2}$、$1+(y')^2=\\left(\\dfrac{e^x+e^{-x}}{2}\\right)^2$。", f"$L={INT(0, chr(92) + 'log ' + str(k))}\\dfrac{{e^x+e^{{-x}}}}{{2}}\\,dx=\\Bigl[\\dfrac{{e^x-e^{{-x}}}}{{2}}\\Bigr]_0^{{\\log {k}}}$。",
              f"$=\\dfrac{{1}}{{2}}\\left({k}-\\dfrac{{1}}{{{k}}}\\right)={TX(V)}$。"]
        chk = (f"[simplify(1+diff((exp(x)+exp(-x))/2, x)**2-((exp(x)+exp(-x))/2)**2), integrate((exp(x)+exp(-x))/2, [x, 0, log({k})])]", f"[0, {sp.sstr(V)}]", None, "intermediate")
        rel = ["HS-MATH2-U05"]
    elif kind == "semicubic":
        s = r.randint(2, 4)
        b = s * s - 1
        V = sp.Rational(2 * (s ** 3 - 1), 3)
        stem = f"曲線 $y=\\dfrac{{2}}{{3}}x\\sqrt{{x}}\\ (0\\leqq x\\leqq {b})$ の長さを求めなさい。"
        st = ["$y'=\\sqrt{x}$ より $\\sqrt{1+(y')^2}=\\sqrt{1+x}$。", f"$L={INT(0, b)}\\sqrt{{1+x}}\\,dx=\\Bigl[\\dfrac{{2}}{{3}}(1+x)\\sqrt{{1+x}}\\Bigr]_0^{{{b}}}$。", f"$=\\dfrac{{2}}{{3}}({s ** 3}-1)={TX(V)}$。"]
        chk = (f"integrate(sqrt(1+diff(Rational(2,3)*x**Rational(3,2), x)**2), [x, 0, {b}])", sp.sstr(V))
        rel = ["HS-MATH3-U02"]
    else:
        a = r.randint(1, 3)
        V = sp.sqrt(2) * (sp.exp(a) - 1)
        stem = f"曲線 $x=e^t\\cos t,\\ y=e^t\\sin t\\ (0\\leqq t\\leqq {a})$ の長さを求めなさい。"
        st = ["$\\dfrac{dx}{dt}=e^t(\\cos t-\\sin t),\\ \\dfrac{dy}{dt}=e^t(\\sin t+\\cos t)$。", "2乗の和は $e^{2t}\\{(\\cos t-\\sin t)^2+(\\sin t+\\cos t)^2\\}=2e^{2t}$。",
              f"$L={INT(0, a)}\\sqrt{{2}}e^t\\,dt=\\sqrt{{2}}(e^{{{a}}}-1)$。".replace("e^{1}", "e")]
        chk = (f"[simplify(diff(exp(t)*cos(t), t)**2+diff(exp(t)*sin(t), t)**2-2*exp(2*t)), integrate(sqrt(2)*exp(t), [t, 0, {a}])]", f"[0, {sp.sstr(V)}]", None, "intermediate")
        rel = ["HS-MATHC-U02"]
    vt = TX(V) if kind != "spiral" else (f"\\sqrt{{2}}(e^{{{a}}}-1)" if a > 1 else "\\sqrt{2}(e-1)")
    return sa(stem, f"${vt}$", "曲線の長さ $L=\\displaystyle\\int\\sqrt{\\left(\\frac{dx}{dt}\\right)^2+\\left(\\frac{dy}{dt}\\right)^2}\\,dt$（$y=f(x)$ なら $\\displaystyle\\int\\sqrt{1+(y')^2}\\,dx$）。", d=3,
              ap="根号の中を計算し、三角関数の公式や $(e^x+e^{-x})^2$ の形を使って完全平方にしてから根号を外す。$\\sqrt{A^2}=|A|$ の符号に注意する。",
              steps=st, alt=["曲線の始点と終点を結ぶ線分の長さより長くなっているかを確かめると、答えの妥当性が分かる。"],
              pc=[("長さの公式に正しく当てはめている", 1), ("根号の中を整理して外している", 2), ("長さが正しい", 1)],
              pit=["根号の中の2乗の和を計算せず、各成分を別々に積分して足す。", "$\\sqrt{A^2}=A$ として符号を確かめない。"], chk=chk, rel=rel)


# ======================================================================
# C 思考力・記述応用
# ======================================================================

@gen("thinking_writing", 3, ["written_reasoning", "condition_check"])
def integral_eq(r):
    kind = r.choice(["upper", "upper", "const"])
    if kind == "upper":
        fam = r.choice(["log", "exp", "sin", "cos"])
        if fam == "log":
            c = r.randint(1, 3)
            g, gpy, f, a, atex = f"\\log x-{c}", f"log(x)-{c}", "\\dfrac{1}{x}", sp.E ** c, ("e" if c == 1 else f"e^{c}")
        elif fam == "exp":
            k, c = r.randint(1, 3), r.randint(1, 3)
            g, gpy, f, a, atex = (f"e^{{{cf(k)}x}}-" + ("e" if k * c == 1 else f"e^{{{k * c}}}")), f"exp({k}*x)-exp({k * c})", f"{cf(k)}e^{{{cf(k)}x}}", sp.Integer(c), str(c)
        elif fam == "sin":
            g, gpy, f = "\\sin x-\\dfrac{1}{2}", "sin(x)-Rational(1,2)", "\\cos x"
            a, atex = sp.pi / 6, "\\dfrac{\\pi}{6}"
        else:
            g, gpy, f = "\\cos x-\\dfrac{\\sqrt{3}}{2}", "cos(x)-sqrt(3)/2", "-\\sin x"
            a, atex = sp.pi / 6, "\\dfrac{\\pi}{6}"
        stem = f"等式 ${INT('a', 'x')}f(t)\\,dt={g}$ がすべての $x$（ただし ${'x>0' if fam == 'log' else '実数'}$）について成り立つような関数 $f(x)$ と、定数 $a$ の値を求めなさい。" + ("ただし、$0<a<\\dfrac{\\pi}{2}$ とする。" if fam in ("sin", "cos") else "")
        stem = stem.replace("（ただし $実数$）", " ")
        ans = f"$f(x)={f}$、$a={atex}$"
        steps = [f"両辺を $x$ で微分すると、$\\dfrac{{d}}{{dx}}{INT('a', 'x')}f(t)\\,dt=f(x)$ より $f(x)={f}$。",
                 f"もとの等式に $x=a$ を代入すると、左辺は $\\displaystyle\\int_a^af(t)\\,dt=0$ なので ${g.replace('x', 'a').replace(chr(92) + 'cos a', chr(92) + 'cos a').replace('e^{', 'e^{')}=0$。",
                 f"これを解いて $a={atex}$。"]
        steps[1] = steps[1].replace("\\dfrac{1}{a}", "\\dfrac{1}{x}")
        chk = (f"[simplify(diff({gpy}, x)-({sp.sstr(sp.diff(sp.sympify(gpy, locals={'x': X}), X))})), limit({gpy}, x, {sp.sstr(a)})]", "[0, 0]", None, "intermediate")
        rub = [("両辺を微分して $f(x)$ を求めている", 3), ("$x=a$ を代入して $a$ の方程式を立てている", 3), ("$f(x)$ と $a$ が正しい", 2)]
        ap = "上端が変数の定積分は、微分すると被積分関数になる：$\\dfrac{d}{dx}\\displaystyle\\int_a^xf(t)\\,dt=f(x)$。また $x=a$ を代入すると左辺は $0$。"
        alt = ["求めた $f(x)$ を実際に $a$ から $x$ まで積分し、右辺と一致することを確かめる。"]
    else:
        k = r.choice([F(1, 2), F(1, 3), F(2), F(-1), F(-2), F(3), F(2, 3), F(-1, 2)])
        A = (sp.E - 1) / (1 - sp.Rational(k.numerator, k.denominator))
        kt = ft(k)
        stem = f"等式 $f(x)=e^x{'+' if k > 0 else '-'}{ft(abs(k)) if abs(k) != 1 else ''}{INT(0, 1)}f(t)\\,dt$ を満たす関数 $f(x)$ を求めなさい。"
        c = sp.simplify(sp.Rational(k.numerator, k.denominator) * A)
        ans = f"$f(x)=e^x{'+' if c > 0 else ''}{TX(c)}$"
        steps = [f"$\\displaystyle\\int_0^1f(t)\\,dt$ は定数なので $A$ とおく。$f(x)=e^x+{kt}A$。".replace("+-", "-"),
                 f"これを $A=\\displaystyle\\int_0^1f(t)\\,dt$ に代入すると $A=\\displaystyle\\int_0^1(e^t+{kt}A)\\,dt=e-1+{kt}A$。".replace("+-", "-"),
                 f"$\\left(1-{kt if k > 0 else '(' + kt + ')'}\\right)A=e-1$ より $A={TX(A)}$。", f"よって $f(x)=e^x{'+' if c > 0 else ''}{TX(c)}$。"]
        chk = (f"simplify(integrate(exp(x)+({sp.sstr(c)}), [x, 0, 1])-({sp.sstr(A)}))", "0", None, "intermediate")
        rub = [("定積分を定数 $A$ とおいている", 3), ("$A$ についての方程式を立てて解いている", 3), ("$f(x)$ が正しい", 2)]
        ap = "積分区間が定数の定積分は定数。$A$ とおいて $f(x)$ を表し、その式を定義の積分に代入して $A$ を決める。"
        alt = [f"求めた $f(x)$ を右辺に代入して計算し、左辺に一致することを確かめる。"]
    return desc(stem, ans, "定積分の性質（微分・定数）を使う。", rub, d=4, p=8, lines=8, ap=ap, steps=steps, alt=alt,
                pc=[("方針", 3), ("方程式", 3), ("答え", 2)],
                pit=["$\\displaystyle\\int_a^xf(t)\\,dt$ を微分するとき、$f(t)$ のまま $t$ を残す。", "定数 $A$ とおくべき定積分を、$x$ の関数と思い込む。"], chk=chk)


@gen("thinking_writing", 3, ["written_reasoning", "cross_unit"], rel=["HS-MATHB-U01"])
def ineq_integral(r):
    kind = r.choice(["sq", "cube", "harm", "rsqrt", "sqrt"])
    n0 = r.randint(2, 5)
    if kind == "sq":
        stem = f"$n$ を ${n0}$ 以上の自然数とする。不等式 $1+\\dfrac{{1}}{{2^2}}+\\dfrac{{1}}{{3^2}}+\\cdots+\\dfrac{{1}}{{n^2}}<2-\\dfrac{{1}}{{n}}$ を、定積分を用いて証明しなさい。"
        steps = ["$k\\geqq2$ のとき、$k-1\\leqq x\\leqq k$ で $\\dfrac{1}{x^2}\\geqq\\dfrac{1}{k^2}$（等号は $x=k$ のときのみ）なので $\\dfrac{1}{k^2}<\\displaystyle\\int_{k-1}^{k}\\dfrac{dx}{x^2}$。",
                 "$k=2,\\,3,\\,\\cdots,\\,n$ について辺々を加えると $\\displaystyle\\sum_{k=2}^{n}\\dfrac{1}{k^2}<\\int_1^n\\dfrac{dx}{x^2}=1-\\dfrac{1}{n}$。",
                 "両辺に $1$ を加えて $1+\\dfrac{1}{2^2}+\\cdots+\\dfrac{1}{n^2}<2-\\dfrac{1}{n}$。"]
        chk = ("integrate(1/x**2, [x, 1, n])", "1-1/n", None, "intermediate")
    elif kind == "cube":
        stem = f"$n$ を ${n0}$ 以上の自然数とする。不等式 $1+\\dfrac{{1}}{{2^3}}+\\dfrac{{1}}{{3^3}}+\\cdots+\\dfrac{{1}}{{n^3}}<\\dfrac{{3}}{{2}}-\\dfrac{{1}}{{2n^2}}$ を、定積分を用いて証明しなさい。"
        steps = ["$k\\geqq2$ のとき、$k-1\\leqq x\\leqq k$ で $\\dfrac{1}{x^3}\\geqq\\dfrac{1}{k^3}$（等号は $x=k$ のときのみ）なので $\\dfrac{1}{k^3}<\\displaystyle\\int_{k-1}^{k}\\dfrac{dx}{x^3}$。",
                 "$k=2$ から $n$ まで加えると $\\displaystyle\\sum_{k=2}^{n}\\dfrac{1}{k^3}<\\int_1^n\\dfrac{dx}{x^3}=\\dfrac{1}{2}-\\dfrac{1}{2n^2}$。", "両辺に $1$ を加えて結論を得る。"]
        chk = ("integrate(1/x**3, [x, 1, n])", "Rational(1,2)-1/(2*n**2)", None, "intermediate")
    elif kind == "harm":
        stem = f"$n$ を自然数とする。不等式 $1+\\dfrac{{1}}{{2}}+\\dfrac{{1}}{{3}}+\\cdots+\\dfrac{{1}}{{n}}>\\log(n+1)$ を、定積分を用いて証明しなさい。また、このことを用いて $\\displaystyle\\lim_{{n\\to\\infty}}\\sum_{{k=1}}^{{n}}\\dfrac{{1}}{{k}}$ を調べなさい。"
        steps = ["$k\\leqq x\\leqq k+1$ で $\\dfrac{1}{x}\\leqq\\dfrac{1}{k}$（等号は $x=k$ のときのみ）なので $\\displaystyle\\int_k^{k+1}\\dfrac{dx}{x}<\\dfrac{1}{k}$。",
                 "$k=1$ から $n$ まで加えると $\\displaystyle\\int_1^{n+1}\\dfrac{dx}{x}=\\log(n+1)<\\sum_{k=1}^{n}\\dfrac{1}{k}$。",
                 "$n\\to\\infty$ のとき $\\log(n+1)\\to\\infty$ なので、$\\displaystyle\\sum_{k=1}^{n}\\dfrac{1}{k}\\to\\infty$（正の無限大に発散する）。"]
        chk = ("integrate(1/x, [x, 1, n+1])", "log(n+1)", None, "intermediate")
    elif kind == "rsqrt":
        stem = f"$n$ を ${n0}$ 以上の自然数とする。不等式 $1+\\dfrac{{1}}{{\\sqrt{{2}}}}+\\dfrac{{1}}{{\\sqrt{{3}}}}+\\cdots+\\dfrac{{1}}{{\\sqrt{{n}}}}<2\\sqrt{{n}}-1$ を、定積分を用いて証明しなさい。"
        steps = ["$k\\geqq2$ のとき、$k-1\\leqq x\\leqq k$ で $\\dfrac{1}{\\sqrt{x}}\\geqq\\dfrac{1}{\\sqrt{k}}$（等号は $x=k$ のときのみ）なので $\\dfrac{1}{\\sqrt{k}}<\\displaystyle\\int_{k-1}^{k}\\dfrac{dx}{\\sqrt{x}}$。",
                 "$k=2$ から $n$ まで加えると $\\displaystyle\\sum_{k=2}^{n}\\dfrac{1}{\\sqrt{k}}<\\int_1^n\\dfrac{dx}{\\sqrt{x}}=2\\sqrt{n}-2$。", "両辺に $1$ を加えて $\\displaystyle\\sum_{k=1}^{n}\\dfrac{1}{\\sqrt{k}}<2\\sqrt{n}-1$。"]
        chk = ("integrate(1/sqrt(x), [x, 1, n])", "2*sqrt(n)-2", None, "intermediate")
    else:
        stem = "$n$ を自然数とする。不等式 $\\sqrt{1}+\\sqrt{2}+\\cdots+\\sqrt{n}>\\dfrac{2}{3}n\\sqrt{n}$ を、定積分を用いて証明しなさい。"
        steps = ["$k-1\\leqq x\\leqq k$ で $\\sqrt{x}\\leqq\\sqrt{k}$（等号は $x=k$ のときのみ）なので $\\displaystyle\\int_{k-1}^{k}\\sqrt{x}\\,dx<\\sqrt{k}$。",
                 "$k=1$ から $n$ まで加えると $\\displaystyle\\int_0^n\\sqrt{x}\\,dx=\\dfrac{2}{3}n\\sqrt{n}<\\sum_{k=1}^{n}\\sqrt{k}$。"]
        chk = ("integrate(sqrt(x), [x, 0, n])", "Rational(2,3)*n**Rational(3,2)", None, "intermediate")
    return desc(stem, "（証明）" + "".join(steps) + "（証明終）", "階段状の長方形の面積と、曲線の下の面積を比べる。",
                [("各項を1つの区間での定積分と比べる不等式を、理由とともに立てている", 3), ("和をとって定積分を計算している", 3), ("結論を正しく導いている", 2)], d=5, p=8, lines=10, kind="proof",
                ap="和 $\\displaystyle\\sum f(k)$（数学Bの $\\Sigma$）は、幅 $1$ の長方形の面積の和。単調な関数 $y=f(x)$ のグラフの下の面積（定積分）と比べて不等式を作る。",
                steps=steps, alt=["図をかき、幅 $1$ の長方形がグラフの上にはみ出すか、下に収まるかを確かめてから不等式の向きを決めると間違えにくい。"],
                pc=[("項ごとの不等式", 3), ("和と定積分", 3), ("結論", 2)],
                pit=["長方形をどちら側に置くかを誤り、不等号の向きが逆になる。", "和の始まり（$k=1$ か $k=2$ か）と積分区間がずれる。"], chk=chk)


@gen("thinking_writing", 2, ["application", "written_reasoning"])
def volume_adv(r):
    kind = r.choice(["washer", "yaxis", "tri", "square"])
    if kind == "washer":
        k = r.randint(1, 3)
        V = sp.pi * k ** 4 / 6
        line = "x" if k == 1 else f"\\dfrac{{x}}{{{k}}}"
        stem = f"曲線 $y=\\sqrt{{x}}$ と直線 $y={line}$ で囲まれた部分を、$x$ 軸のまわりに1回転してできる立体の体積を求めなさい。"
        steps = [f"交点の $x$ 座標は $0,\\ {k * k}$。$0\\leqq x\\leqq {k * k}$ で $\\sqrt{{x}}\\geqq {line}\\geqq0$。",
                 f"断面はドーナツ形（外半径 $\\sqrt{{x}}$、内半径 ${line}$）なので、断面積は $\\pi\\left\\{{x-\\dfrac{{x^2}}{{{k * k}}}\\right\\}}$。".replace("\\dfrac{x^2}{1}", "x^2"),
                 f"$V=\\pi{INT(0, k * k)}\\left(x-\\dfrac{{x^2}}{{{k * k}}}\\right)dx=\\pi\\left(\\dfrac{{{k ** 4}}}{{2}}-\\dfrac{{{k ** 4}}}{{3}}\\right)={TX(V)}$。".replace("\\dfrac{x^2}{1}", "x^2")]
        chk = (f"pi*integrate(x-x**2/{k * k}, [x, 0, {k * k}])", sp.sstr(V))
        ap = "2曲線の間の部分を回転すると、断面は穴のあいた円（ドーナツ形）。外側の円の面積から内側の円の面積を引く。"
    elif kind == "yaxis":
        a = r.randint(1, 3)
        V = sp.pi * a ** 4 / 2
        stem = f"放物線 $y=x^2$ と直線 $y={a * a}$ で囲まれた部分を、$y$ 軸のまわりに1回転してできる立体の体積を求めなさい。"
        steps = [f"$y$ 軸に垂直な平面 $y=t\\ (0\\leqq t\\leqq {a * a})$ で切ると、断面は半径 $\\sqrt{{t}}$ の円（$x^2=t$）。", "断面積は $\\pi t$。",
                 f"$V=\\pi{INT(0, a * a)}y\\,dy=\\pi\\cdot\\dfrac{{{a ** 4}}}{{2}}={TX(V)}$。"]
        chk = (f"pi*integrate(y, [y, 0, {a * a}])", sp.sstr(V))
        ap = "$y$ 軸のまわりの回転体は、$y$ 軸に垂直な断面で考え、$x^2$ を $y$ で表して $y$ について積分する。"
    elif kind == "tri":
        R = r.randint(1, 4)
        V = sp.Rational(4, 3) * sp.sqrt(3) * R ** 3
        stem = f"底面が半径 ${R}$ の円 $x^2+y^2\\leqq {R * R}$ である立体がある。この立体を $x$ 軸に垂直な平面で切った断面は、つねに底面の弦を1辺とする正三角形である。この立体の体積を求めなさい。"
        steps = [f"$x$ 軸に垂直な平面 $x=t\\ (-{R}\\leqq t\\leqq {R})$ で切ると、弦の長さは $2\\sqrt{{{R * R}-t^2}}$。",
                 f"1辺 $l$ の正三角形の面積は $\\dfrac{{\\sqrt{{3}}}}{{4}}l^2$ なので、断面積 $S(t)=\\sqrt{{3}}({R * R}-t^2)$。",
                 f"$V={INT(-R, R)}\\sqrt{{3}}({R * R}-t^2)\\,dt=2\\sqrt{{3}}\\left({R ** 3}-\\dfrac{{{R ** 3}}}{{3}}\\right)={TX(V)}$。"]
        chk = (f"integrate(sqrt(3)*({R * R}-t**2), [t, {-R}, {R}])", sp.sstr(V))
        ap = "回転体でなくても、断面積 $S(x)$ が分かれば $V=\\displaystyle\\int S(x)\\,dx$ で体積が求まる。弦の長さを三平方の定理で表す。"
    else:
        R = r.randint(1, 4)
        V = sp.Rational(16, 3) * R ** 3
        stem = f"底面が半径 ${R}$ の円 $x^2+y^2\\leqq {R * R}$ である立体がある。この立体を $x$ 軸に垂直な平面で切った断面は、つねに底面の弦を1辺とする正方形である。この立体の体積を求めなさい。"
        steps = [f"平面 $x=t\\ (-{R}\\leqq t\\leqq {R})$ での弦の長さは $2\\sqrt{{{R * R}-t^2}}$。", f"断面積 $S(t)=4({R * R}-t^2)$。",
                 f"$V={INT(-R, R)}4({R * R}-t^2)\\,dt=8\\left({R ** 3}-\\dfrac{{{R ** 3}}}{{3}}\\right)={TX(V)}$。"]
        chk = (f"integrate(4*({R * R}-t**2), [t, {-R}, {R}])", sp.sstr(V))
        ap = "断面積 $S(t)$ を求めて積分する。断面の正方形の1辺は底面の円の弦。"
    return desc(stem, f"${TX(V)}$", "断面積を求めて積分する。",
                [("断面の形と断面積を正しく求めている", 3), ("体積を定積分で表している（区間を含む）", 3), ("体積が正しい", 2)], d=4, p=8, lines=10,
                ap=ap, steps=steps, alt=["対称性（偶関数）を使って区間の半分で計算し、2倍してもよい。"],
                pc=[("断面積", 3), ("立式", 3), ("答え", 2)],
                pit=["ドーナツ形の断面を $\\pi(f-g)^2$ としてしまう。", "積分変数（$x$ か $y$ か）と区間の対応を誤る。"], chk=chk)


@gen("thinking_writing", 2, ["cross_unit", "written_reasoning"], rel=["HS-MATH3-U01"])
def riemann_adv(r):
    kind = r.choice(["prod", "harm_m", "k_over", "sqrt_sum"])
    if kind == "prod":
        stem = "極限 $\\displaystyle\\lim_{n\\to\\infty}\\dfrac{1}{n}\\sqrt[n]{(n+1)(n+2)\\cdots(2n)}$ を求めなさい。"
        ans = "$\\dfrac{4}{e}$"
        steps = ["与式を $a_n$ とおくと $a_n=\\sqrt[n]{\\left(1+\\dfrac{1}{n}\\right)\\left(1+\\dfrac{2}{n}\\right)\\cdots\\left(1+\\dfrac{n}{n}\\right)}$。",
                 "自然対数をとると $\\log a_n=\\dfrac{1}{n}\\displaystyle\\sum_{k=1}^{n}\\log\\left(1+\\dfrac{k}{n}\\right)$。",
                 "区分求積法より $\\displaystyle\\lim_{n\\to\\infty}\\log a_n=\\int_0^1\\log(1+x)\\,dx=\\Bigl[(1+x)\\log(1+x)-x\\Bigr]_0^1=2\\log2-1$。",
                 "$\\log$ は連続なので $\\displaystyle\\lim_{n\\to\\infty}a_n=e^{2\\log2-1}=\\dfrac{4}{e}$。"]
        chk = ("exp(integrate(log(1+x), [x, 0, 1]))", "4/E", None, "intermediate")
    elif kind == "harm_m":
        m = r.randint(2, 5)
        stem = f"極限 $\\displaystyle\\lim_{{n\\to\\infty}}\\left(\\dfrac{{1}}{{n+1}}+\\dfrac{{1}}{{n+2}}+\\cdots+\\dfrac{{1}}{{{m}n}}\\right)$ を求めなさい。"
        ans = f"$\\log {m}$"
        steps = [f"与式 $=\\displaystyle\\sum_{{k=1}}^{{{m - 1}n}}\\dfrac{{1}}{{n+k}}=\\dfrac{{1}}{{n}}\\sum_{{k=1}}^{{{m - 1}n}}\\dfrac{{1}}{{1+\\frac{{k}}{{n}}}}$。".replace("{1n}", "{n}"),
                 f"$\\dfrac{{k}}{{n}}$ は $\\dfrac{{1}}{{n}}$ から ${m - 1}$ まで動くので、区間 $[0,\\,{m - 1}]$ の区分求積となる。",
                 f"極限は $\\displaystyle\\int_0^{{{m - 1}}}\\dfrac{{dx}}{{1+x}}=\\log {m}$。"]
        chk = (f"integrate(1/(1+x), [x, 0, {m - 1}])", f"log({m})", None, "intermediate")
    elif kind == "k_over":
        a = r.randint(1, 3)
        stem = f"極限 $\\displaystyle\\lim_{{n\\to\\infty}}\\sum_{{k=1}}^{{n}}\\dfrac{{k}}{{n^2+{'' if a == 1 else a * a}k^2}}$ を求めなさい。"
        V = sp.log(1 + a * a) / (2 * a * a)
        ans = f"${TX(V)}$".replace("\\log{\\left(", "\\log(").replace(" \\right)}", ")")
        ans = f"$\\dfrac{{\\log {1 + a * a}}}{{{2 * a * a}}}$"
        steps = [f"与式 $=\\dfrac{{1}}{{n}}\\displaystyle\\sum_{{k=1}}^{{n}}\\dfrac{{\\frac{{k}}{{n}}}}{{1+{'' if a == 1 else a * a}\\left(\\frac{{k}}{{n}}\\right)^2}}$。",
                 f"区分求積法より、極限は $\\displaystyle\\int_0^1\\dfrac{{x}}{{1+{'' if a == 1 else a * a}x^2}}\\,dx$。",
                 f"$\\Bigl[\\dfrac{{1}}{{{2 * a * a}}}\\log(1+{'' if a == 1 else a * a}x^2)\\Bigr]_0^1=\\dfrac{{\\log {1 + a * a}}}{{{2 * a * a}}}$。"]
        chk = (f"integrate(x/(1+{a * a}*x**2), [x, 0, 1])", sp.sstr(V), None, "intermediate")
    else:
        stem = "極限 $\\displaystyle\\lim_{n\\to\\infty}\\dfrac{1}{n\\sqrt{n}}\\left(\\sqrt{1}+\\sqrt{2}+\\cdots+\\sqrt{n}\\right)$ を求めなさい。"
        ans = "$\\dfrac{2}{3}$"
        steps = ["与式 $=\\dfrac{1}{n}\\displaystyle\\sum_{k=1}^{n}\\sqrt{\\dfrac{k}{n}}$。", "区分求積法より $\\displaystyle\\int_0^1\\sqrt{x}\\,dx=\\dfrac{2}{3}$。"]
        chk = ("integrate(sqrt(x), [x, 0, 1])", "Rational(2,3)", None, "intermediate")
    return desc(stem, ans, "和を $\\dfrac{1}{n}\\sum f\\left(\\frac{k}{n}\\right)$ の形に直し、区分求積法を用いる。",
                [("和を $\\dfrac{1}{n}\\sum f\\left(\\frac{k}{n}\\right)$ の形に変形している", 3), ("対応する定積分（区間を含む）を正しく立てている", 3), ("極限値が正しい", 2)], d=5, p=8, lines=10,
                ap="数列の和の極限（数学Ⅲ 極限）で、和の公式が使えないものは区分求積法で定積分に直す。積の形は対数をとって和に直す。",
                steps=steps, alt=["$n=1000$ 程度で和を数値計算すると、求めた値に近いことが確かめられる。"],
                pc=[("変形", 3), ("定積分", 3), ("答え", 2)],
                pit=["和の項数が $n$ でないとき（$" + "2n" + "$ 項など）、積分区間を $[0,\\,1]$ のままにする。", "積の形のまま区分求積法を使おうとする。"], chk=chk)


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(stem, wrong, step, etype, tempt, fix, ans, expl, steps, ap, alt, pit, chk=None, d=3):
    return desc(f"{stem}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい答えを求めなさい。", ans, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい解答を途中式とともに示している", 3), ("最終的な答えが正しい", 1)], d=d, p=6, lines=6,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい途中式", 3), ("正しい答え", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix), chk=chk)


@gen("error_correction", 3, ["common_error", "condition_check"])
def err_subst(r):
    if r.random() < 0.5:
        b = r.randint(2, 3)
        k = r.choice([1, 2])
        if k == 1:
            ftex, fpy = "xe^{x^2}", "x*exp(x**2)"
            V = (sp.exp(b * b) - 1) / 2
            W = (sp.exp(b) - 1) / 2
            wrong = f"$t=x^2$ とおくと $dt=2x\\,dx$。${INT(0, b)}xe^{{x^2}}\\,dx=\\dfrac{{1}}{{2}}{INT(0, b)}e^t\\,dt=\\dfrac{{1}}{{2}}(e^{{{b}}}-1)$"
            right = f"\\dfrac{{1}}{{2}}(e^{{{b * b}}}-1)"
            steps = [f"$t=x^2$ とおくと $dt=2x\\,dx$。$x:0\\to {b}$ のとき $t:0\\to {b * b}$。", f"$\\dfrac{{1}}{{2}}{INT(0, b * b)}e^t\\,dt=\\dfrac{{1}}{{2}}(e^{{{b * b}}}-1)$。"]
        else:
            ftex, fpy = "x(x^2+1)^2", "x*(x**2+1)**2"
            V = sp.Rational((b * b + 1) ** 3 - 1, 6)
            W = sp.Rational((b + 1) ** 3 - 1, 6)
            wrong = f"$t=x^2+1$ とおくと $dt=2x\\,dx$。${INT(0, b)}x(x^2+1)^2\\,dx=\\dfrac{{1}}{{2}}{INT(0, b)}t^2\\,dt=\\dfrac{{{b ** 3}}}{{6}}$"
            W = sp.Rational(b ** 3, 6)
            right = TX(V)
            steps = [f"$t=x^2+1$ とおくと $dt=2x\\,dx$。$x:0\\to {b}$ のとき $t:1\\to {b * b + 1}$。", f"$\\dfrac{{1}}{{2}}{INT(1, b * b + 1)}t^2\\,dt=\\dfrac{{{(b * b + 1) ** 3}-1}}{{6}}={TX(V)}$。"]
        return err_item(f"定積分 ${INT(0, b)}{ftex}\\,dx$ を求めなさい。", wrong, "置換した後も積分区間を $x$ の区間のまま使った部分", "condition",
                        "被積分関数だけを $t$ に置きかえ、積分区間も $t$ の値に対応させる必要があることを忘れている。",
                        f"$t$ の区間に取りかえて計算すると ${right}$", f"${right}$",
                        "定積分の置換では、$x$ の区間を $t=g(x)$ によって $t$ の区間に変える。",
                        steps, "置換したら「$x$ と $t$ の対応表」をかいて区間を取りかえる。",
                        ["いったん不定積分を求めて $x$ の式に戻し、$x$ の区間で計算しても同じ値になる（生徒の値とは異なる）。"],
                        ["区間を取りかえ忘れる。"], chk=(f"integrate({fpy}, [x, 0, {b}])", sp.sstr(V)))
    a, b, n = r.randint(2, 5), nonzero(r, -4, 4), r.randint(3, 6)
    wrong = f"$\\displaystyle\\int({lin(a, b)})^{n}\\,dx=\\dfrac{{({lin(a, b)})^{{{n + 1}}}}}{{{n + 1}}}+C$"
    right = f"\\dfrac{{({lin(a, b)})^{{{n + 1}}}}}{{{a * (n + 1)}}}+C"
    return err_item(f"不定積分 ${INT()}({lin(a, b)})^{n}\\,dx$ を求めなさい。", wrong, f"$dx$ を $dt$ に置きかえるときの係数 $\\dfrac{{1}}{{{a}}}$ を落とした部分", "calculation",
                    "$x^n$ の積分公式をそのまま当てはめ、中身が $" + lin(a, b) + "$ であることによる係数を考えていない。",
                    f"$t={lin(a, b)}$ とおくと $dx=\\dfrac{{1}}{{{a}}}dt$ なので ${right}$", f"${right}$",
                    "$\\displaystyle\\int f(ax+b)\\,dx=\\dfrac{1}{a}F(ax+b)+C$。",
                    [f"$t={lin(a, b)}$ とおくと $dt={a}\\,dx$。", f"${INT()}t^{n}\\cdot\\dfrac{{1}}{{{a}}}\\,dt=\\dfrac{{t^{{{n + 1}}}}}{{{a * (n + 1)}}}+C$。", f"${right}$。"],
                    "答えを微分してもとの関数に戻るか確かめる。",
                    [f"生徒の答えを微分すると ${a}({lin(a, b)})^{n}$ となり、もとの関数の ${a}$ 倍になってしまう。"],
                    ["微分して検算しない。"], chk=(f"simplify(diff(({a}*x+({b}))**{n + 1}/{a * (n + 1)}, x)-({a}*x+({b}))**{n})", "0"))


@gen("error_correction", 3, ["common_error", "computation"])
def err_parts(r):
    kind = r.choice(["xsin", "log", "xcos"])
    if kind == "xsin":
        a = r.randint(1, 3)
        A = "x" if a == 1 else f"{a}x"
        k = F(1, a)
        g = f"-{kfrac(k, chr(92) + 'cos ' + A)}"
        right = f"-{kfrac(k, 'x' + chr(92) + 'cos ' + A)}+{kfrac(k * k, chr(92) + 'sin ' + A)}+C"
        wrong = f"$\\displaystyle\\int x\\sin {A}\\,dx=x\\left({g}\\right)-{INT()}\\left({g}\\right)dx=-{kfrac(k, 'x' + chr(92) + 'cos ' + A)}-{kfrac(k * k, chr(92) + 'sin ' + A)}+C$"
        return err_item(f"不定積分 ${INT()}x\\sin {A}\\,dx$ を求めなさい。", wrong, "$-\\displaystyle\\int\\left(" + g + "\\right)dx$ を計算する部分の符号", "sign",
                        "$-\\displaystyle\\int(-\\cdots)\\,dx$ と負の符号が重なる部分で、符号の処理を誤っている。",
                        f"$-{INT()}\\left({g}\\right)dx=+{kfrac(k, INT() + chr(92) + 'cos ' + A)}\\,dx={kfrac(k * k, chr(92) + 'sin ' + A)}$ なので ${right}$", f"${right}$",
                        "部分積分の第2項 $-\\displaystyle\\int f'g\\,dx$ では、$g$ に負号があると $+$ になる。",
                        [f"$f=x,\\ g'=\\sin {A}$、$g={g}$。", f"$x\\left({g}\\right)+{kfrac(k, INT() + chr(92) + 'cos ' + A)}\\,dx$。", f"${right}$。"],
                        "負号を含む部分は、かっこを付けて書いてから外す。",
                        ["答えを微分すると $x\\sin " + A + "$ に戻ることを確かめる（生徒の答えを微分すると余分な項が残る）。"],
                        ["符号の処理を急ぐ。"], chk=(f"simplify(diff(-{fp(k)}*x*cos({a}*x)+{fp(k * k)}*sin({a}*x), x)-x*sin({a}*x))", "0"))
    if kind == "log":
        up = r.randint(1, 3)
        uptex = "e" if up == 1 else f"e^{up}"
        V = sp.expand(sp.integrate(sp.log(X), (X, 1, sp.E ** up)))
        W = 1 - sp.exp(-up)
        wrong = f"$(\\log x)'=\\dfrac{{1}}{{x}}$ なので ${INT(1, uptex)}\\log x\\,dx=\\Bigl[\\dfrac{{1}}{{x}}\\Bigr]_1^{{{uptex}}}={TX(W - 1 + 1 - 1 + 1 - 1 + (sp.exp(-up) - 1) * 0 + sp.exp(-up) - 1)}$"
        wrong = f"$(\\log x)'=\\dfrac{{1}}{{x}}$ なので ${INT(1, uptex)}\\log x\\,dx=\\Bigl[\\dfrac{{1}}{{x}}\\Bigr]_1^{{{uptex}}}=\\dfrac{{1}}{{{uptex}}}-1$"
        return err_item(f"定積分 ${INT(1, uptex)}\\log x\\,dx$ を求めなさい。", wrong, "$\\log x$ の原始関数を $\\dfrac{1}{x}$ とした部分", "concept",
                        "微分と積分を取り違え、導関数 $\\dfrac{1}{x}$ を原始関数として使っている。",
                        f"部分積分で原始関数は $x\\log x-x$。$\\Bigl[x\\log x-x\\Bigr]_1^{{{uptex}}}={TX(V)}$", f"${TX(V)}$",
                        "$\\displaystyle\\int\\log x\\,dx=x\\log x-x+C$（$1\\cdot\\log x$ と見て部分積分）。",
                        ["$\\log x=(x)'\\log x$ と見て部分積分：$x\\log x-\\displaystyle\\int x\\cdot\\dfrac{1}{x}\\,dx=x\\log x-x$。", f"$\\Bigl[x\\log x-x\\Bigr]_1^{{{uptex}}}={TX(V)}$。"],
                        "原始関数は、微分してもとの関数に戻るもの。$\\left(\\dfrac{1}{x}\\right)'=-\\dfrac{1}{x^2}$ は $\\log x$ にならない。",
                        [f"$1\\leqq x\\leqq {uptex}$ で $\\log x\\geqq0$ なので定積分は正のはず。生徒の答え $\\dfrac{{1}}{{{uptex}}}-1$ は負で、誤りに気づける。"],
                        ["微分と積分を取り違える。"], chk=(f"integrate(log(x), [x, 1, exp({up})])", sp.sstr(V)))
    a = r.randint(1, 3)
    A = "x" if a == 1 else f"{a}x"
    k = F(1, a)
    up = "\\pi" if a == 1 else f"\\dfrac{{\\pi}}{{{a}}}"
    V = sp.integrate(X * sp.cos(a * X), (X, 0, sp.pi / (2 * a)))
    uph = "\\dfrac{\\pi}{2}" if a == 1 else f"\\dfrac{{\\pi}}{{{2 * a}}}"
    wrong = f"$\\Bigl[{kfrac(k, 'x' + chr(92) + 'sin ' + A)}\\Bigr]_0^{{{uph}}}-{INT(0, uph)}{kfrac(k, chr(92) + 'sin ' + A)}\\,dx=\\Bigl[{kfrac(k, 'x' + chr(92) + 'sin ' + A)}+{kfrac(k * k, chr(92) + 'cos ' + A)}\\Bigr]_0^{{{uph}}}$ の上端だけを代入して ${TX(sp.pi / (2 * a * a))}$"
    return err_item(f"定積分 ${INT(0, uph)}x\\cos {A}\\,dx$ を求めなさい。", wrong, "下端 $x=0$ での値を引いていない部分", "calculation",
                    "下端 $0$ を代入すると $0$ になると思い込み、$\\cos 0=1$ の項を見落としている。",
                    f"下端の値 ${kfrac(k * k, chr(92) + 'cos 0')}={ft(k * k)}$ を引いて ${TX(V)}$", f"${TX(V)}$",
                    "$\\Bigl[F(x)\\Bigr]_a^b=F(b)-F(a)$。$\\cos 0=1$ なので下端の値は $0$ にならない。",
                    [f"原始関数 $F(x)={kfrac(k, 'x' + chr(92) + 'sin ' + A)}+{kfrac(k * k, chr(92) + 'cos ' + A)}$。", f"$F\\left({uph}\\right)={TX(sp.pi / (2 * a * a))}$、$F(0)={ft(k * k)}$。", f"$F\\left({uph}\\right)-F(0)={TX(V)}$。"],
                    "下端が $0$ でも、$\\cos 0=1$、$e^0=1$ のように値が $0$ にならない関数に注意する。",
                    ["グラフの面積として見積もると、値は生徒の答えより小さいはずだと分かる。"], ["下端の代入を省略する。"],
                    chk=(f"integrate(x*cos({a}*x), [x, 0, pi/{2 * a}])", sp.sstr(V)))


@gen("error_correction", 2, ["common_error", "concept"])
def err_area(r):
    if r.random() < 0.5:
        k = r.randint(1, 4)
        stem = f"曲線 $y={cf(k)}\\sin x\\ (0\\leqq x\\leqq 2\\pi)$ と $x$ 軸で囲まれた部分の面積を求めなさい。"
        wrong = f"$S={INT(0, '2' + chr(92) + 'pi')}{cf(k)}\\sin x\\,dx=\\Bigl[-{cf(k)}\\cos x\\Bigr]_0^{{2\\pi}}=0$"
        return err_item(stem, wrong, "区間を分けずに定積分をそのまま面積とした部分", "concept",
                        "定積分は「符号つきの面積」であり、$x$ 軸の下にある部分が負として打ち消し合うことを考えていない。",
                        f"$\\pi\\leqq x\\leqq2\\pi$ では $y\\leqq0$ なので区間を分けて $S={INT(0, chr(92) + 'pi')}{cf(k)}\\sin x\\,dx-{INT(chr(92) + 'pi', '2' + chr(92) + 'pi')}{cf(k)}\\sin x\\,dx={4 * k}$", f"${4 * k}$",
                        "面積は $\\displaystyle\\int|f(x)|\\,dx$。$x$ 軸との交点で区間を分ける。",
                        [f"$0\\leqq x\\leqq\\pi$ で $y\\geqq0$、$\\pi\\leqq x\\leqq2\\pi$ で $y\\leqq0$。", f"${INT(0, chr(92) + 'pi')}{cf(k)}\\sin x\\,dx={2 * k}$、${INT(chr(92) + 'pi', '2' + chr(92) + 'pi')}{cf(k)}\\sin x\\,dx=-{2 * k}$。", f"$S={2 * k}+{2 * k}={4 * k}$。"],
                        "面積が $0$ になることはない。図をかいて $x$ 軸の上下を確認する。",
                        ["図形が $x$ 軸に関して対称な2つの山（谷）からなることから、片方の面積の2倍として求めてもよい。"],
                        ["$x$ 軸の下の部分を考えない。"], chk=(f"integrate(Abs({k}*sin(x)), [x, 0, 2*pi])", str(4 * k)))
    k = r.randint(1, 3)
    up = sp.E ** k
    uptex = "e" if k == 1 else f"e^{k}"
    V = sp.expand(-sp.integrate(sp.log(X), (X, sp.exp(-k), 1)) + sp.integrate(sp.log(X), (X, 1, up)))
    lo = "\\dfrac{1}{e}" if k == 1 else f"\\dfrac{{1}}{{e^{k}}}"
    Wv = sp.expand(sp.integrate(sp.log(X), (X, sp.exp(-k), up)))
    stem = f"曲線 $y=\\log x$ と $x$ 軸、および2直線 $x={lo}$、$x={uptex}$ で囲まれた2つの部分の面積の和を求めなさい。"
    wrong = f"$S={INT(lo, uptex)}\\log x\\,dx=\\Bigl[x\\log x-x\\Bigr]_{{{lo}}}^{{{uptex}}}={TX(Wv)}$"
    return err_item(stem, wrong, "$x=1$ で区間を分けずに定積分をそのまま面積とした部分", "concept",
                    "$\\dfrac{1}{e^k}\\leqq x<1$ では $\\log x<0$ であり、定積分の値が負になって打ち消されることを考えていない。",
                    f"$x=1$ で区間を分け、$-{INT(lo, 1)}\\log x\\,dx+{INT(1, uptex)}\\log x\\,dx={TX(V)}$", f"${TX(V)}$",
                    "面積は $\\displaystyle\\int|f(x)|\\,dx$。グラフが $x$ 軸を横切る点で区間を分ける。",
                    [f"$x<1$ で $\\log x<0$、$x>1$ で $\\log x>0$。", f"$-{INT(lo, 1)}\\log x\\,dx={TX(sp.expand(-sp.integrate(sp.log(X), (X, sp.exp(-k), 1))))}$、${INT(1, uptex)}\\log x\\,dx={TX(sp.expand(sp.integrate(sp.log(X), (X, 1, up))))}$。", f"和は ${TX(V)}$。"],
                    "原始関数 $x\\log x-x$ はそのまま使えるが、区間を分けて符号を調整する。",
                    ["グラフをかけば、$x=1$ の左側に $x$ 軸より下の部分があることがすぐ分かる。"], ["区間を分けない。"],
                    chk=(f"-integrate(log(x), [x, exp({-k}), 1])+integrate(log(x), [x, 1, exp({k})])", sp.sstr(V)))


@gen("error_correction", 2, ["common_error", "concept"])
def err_volume(r):
    if r.random() < 0.6:
        k = r.randint(1, 3)
        line = "x" if k == 1 else f"\\dfrac{{x}}{{{k}}}"
        V = sp.pi * k ** 4 / 6
        W = sp.pi * sp.integrate((sp.sqrt(X) - X / k) ** 2, (X, 0, k * k))
        wrong = f"$V=\\pi{INT(0, k * k)}\\left(\\sqrt{{x}}-{line}\\right)^2dx={TX(W)}$"
        return err_item(f"曲線 $y=\\sqrt{{x}}$ と直線 $y={line}$ で囲まれた部分を、$x$ 軸のまわりに1回転してできる立体の体積を求めなさい。", wrong,
                        "体積を $\\pi\\displaystyle\\int(f-g)^2\\,dx$ とした部分", "formula",
                        "面積の「上－下」の考えを回転体にもそのまま当てはめ、半径の差を2乗してしまっている。",
                        f"断面はドーナツ形なので $V=\\pi{INT(0, k * k)}\\left\\{{x-\\left({line}\\right)^2\\right\\}}dx={TX(V)}$", f"${TX(V)}$",
                        "断面積は「外側の円の面積－内側の円の面積」$=\\pi(f^2-g^2)$ であり、$\\pi(f-g)^2$ ではない。",
                        [f"交点の $x$ 座標は $0,\\ {k * k}$。", "断面は外半径 $\\sqrt{x}$、内半径 $" + line + "$ のドーナツ形。", f"$V=\\pi{INT(0, k * k)}\\left(x-\\dfrac{{x^2}}{{{k * k}}}\\right)dx={TX(V)}$。".replace("\\dfrac{x^2}{1}", "x^2")],
                        "回転体では、断面の図（ドーナツ形）を必ずかいてから断面積を式にする。",
                        ["外側の立体（$y=\\sqrt{x}$ の回転体）の体積から内側の円錐の体積を引いても同じ値になる。"], ["$(f-g)^2$ とする。"],
                        chk=(f"pi*integrate(x-x**2/{k * k}, [x, 0, {k * k}])", sp.sstr(V)))
    s = r.randint(2, 4)
    b = s * s - 1
    V = sp.Rational(2 * (s ** 3 - 1), 3)
    W = sp.Rational(2, 3) * b ** sp.Rational(3, 2) + b
    wrong = f"$L={INT(0, b)}(1+y')\\,dx={INT(0, b)}(1+\\sqrt{{x}})\\,dx$ として計算した"
    return err_item(f"曲線 $y=\\dfrac{{2}}{{3}}x\\sqrt{{x}}\\ (0\\leqq x\\leqq {b})$ の長さを求めなさい。", wrong, "曲線の長さの被積分関数を $1+y'$ とした部分", "formula",
                    "公式 $\\sqrt{1+(y')^2}$ の根号と2乗を落とし、形だけを覚えている。",
                    f"$L={INT(0, b)}\\sqrt{{1+(y')^2}}\\,dx={INT(0, b)}\\sqrt{{1+x}}\\,dx={TX(V)}$", f"${TX(V)}$",
                    "微小部分の長さは三平方の定理で $\\sqrt{(\\Delta x)^2+(\\Delta y)^2}$。これが $\\sqrt{1+(y')^2}$ の由来。",
                    ["$y'=\\sqrt{x}$、$(y')^2=x$。", f"$L={INT(0, b)}\\sqrt{{1+x}}\\,dx=\\Bigl[\\dfrac{{2}}{{3}}(1+x)\\sqrt{{1+x}}\\Bigr]_0^{{{b}}}$。", f"$={TX(V)}$。"],
                    "公式は導出（三平方の定理）と結びつけて覚える。",
                    [f"曲線の長さは、両端を結ぶ線分の長さ $\\sqrt{{{b}^2+\\left(\\frac{{2}}{{3}}{b}\\sqrt{{{b}}}\\right)^2}}$ より少しだけ長いはず、という見積もりで検算できる。"],
                    ["根号を落とす。"], chk=(f"integrate(sqrt(1+x), [x, 0, {b}])", sp.sstr(V)))


GENERATORS = [basic_indef, substitution, by_parts, definite_basic, riemann_sum,
              def_subst, def_parts, area, volume, arc_length,
              integral_eq, ineq_integral, volume_adv, riemann_adv,
              err_subst, err_parts, err_area, err_volume]
