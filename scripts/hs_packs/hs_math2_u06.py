"""単元パック：数学Ⅱ 微分法・積分法（微分係数と導関数・接線・増減と極値・不定積分と定積分・面積）。"""
from fractions import Fraction as F

import sympy as sp

from banks._common import desc, figure, mc, plane, sa
from hs_pack_lib import board, check, definition, derivation, example, gen, guide, intro, lesson, nonzero, poly, summary, theorem, tp

UNIT_ID = "HS-MATH2-U06"


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


def py(*coefs, var="x"):
    """係数列（高次から）→ sympy 式の文字列。"""
    deg = len(coefs) - 1
    return "+".join(f"({fp(c)})*{var}**{deg - i}" for i, c in enumerate(coefs))


def ev(coefs, x):
    x = F(x)
    deg = len(coefs) - 1
    return sum(F(c) * x ** (deg - i) for i, c in enumerate(coefs))


def dcoef(coefs):
    deg = len(coefs) - 1
    return [c * (deg - i) for i, c in enumerate(coefs[:-1])]


def line_tex(m, n):
    """y=mx+n の右辺。"""
    m, n = F(m), F(n)
    if m == 0:
        return ft(n)
    head = "x" if m == 1 else ("-x" if m == -1 else f"{ft(m)}x")
    if n == 0:
        return head
    return head + ("+" if n > 0 else "-") + ft(abs(n))


def lin(c):
    """x-c の LaTeX。"""
    return "x" if c == 0 else f"x{'-' if c > 0 else '+'}{abs(c)}"


def fac(c):
    """因数 (x-c) の LaTeX（c=0 なら x）。"""
    return "x" if c == 0 else f"({lin(c)})"


def polyf(*coefs, var="x"):
    """有理数係数の多項式の LaTeX。"""
    deg = len(coefs) - 1
    out = []
    for i, c in enumerate(coefs):
        c = F(c)
        k = deg - i
        if c == 0:
            continue
        mag = abs(c)
        co = "" if (mag == 1 and k > 0) else ft(mag)
        term = co + (var if k >= 1 else "") + (f"^{k}" if k >= 2 else "")
        out.append(("-" if c < 0 else ("+" if out else "")) + term)
    return "".join(out) or "0"


def cubic_from_roots(r, a_choices=(1, -1, 2, -2)):
    """f'(x)=3a(x-α)(x-β)（α<β、整数）となる整数係数の三次関数の係数 [a, b, c, d] と α, β。"""
    while True:
        a = r.choice(a_choices)
        al, be = sorted(r.sample(range(-3, 4), 2))
        if (a * (al + be)) % 2 == 0:
            break
    d = r.randint(-5, 5)
    return [a, F(-3 * a * (al + be), 2), 3 * a * al * be, d], al, be


LESSON = lesson(
    goals=["平均変化率の極限として微分係数を定義し、導関数の公式 $(x^n)'=nx^{n-1}$ を導いて多項式関数を微分できる。",
           "導関数を用いて接線の方程式を求め、増減表をかいて極値・最大値・最小値を求められる。",
           "微分の逆演算として不定積分を、差 $F(b)-F(a)$ として定積分を計算し、曲線で囲まれた部分の面積を求められる。"],
    duration=200,
    readiness=["二次関数の平方完成と最大・最小（数学Ⅰ）ができる。", "直線の方程式 $y-y_1=m(x-x_1)$（図形と方程式）を使える。",
               "$(a+h)^3=a^3+3a^2h+3ah^2+h^3$ などの展開と、因数分解ができる。"],
    flow=[("導入：瞬間の速さ", 10, "ボールの落下距離 y=5x^2 の平均の速さから、時間幅を 0 に近づけたときの値を考える"),
          ("微分係数と導関数", 35, "極限の意味、微分係数の定義、(x^n)'=nx^{n-1} の導出と微分の計算"),
          ("接線", 25, "微分係数＝接線の傾き。接線の方程式（例題2）と、曲線外の点から引く接線"),
          ("増減と極値", 40, "f'(x) の符号と増減、増減表、極値（例題1）、区間での最大・最小、最大値の応用"),
          ("不定積分と定積分", 35, "微分の逆としての不定積分、定積分の定義と性質、計算練習"),
          ("面積", 40, "面積と定積分の関係の導出、2曲線の間の面積（例題3）、1/6 公式"),
          ("まとめ", 15, "微分と積分の対応を整理し、確認問題と課題を指示")],
    sections=[
        intro("in1", "変化の「瞬間の割合」を求める",
              "ボールを静かに落とすと、$x$ 秒間に落ちる距離はおよそ $y=5x^2$（m）で表される。1秒後から $1+h$ 秒後までの平均の速さは $\\dfrac{5(1+h)^2-5}{h}=10+5h$（m/s）であり、$h$ を $0$ に限りなく近づけると $10$ に近づく。この値を「1秒後の瞬間の速さ」と考えるのが微分の出発点である。積分はその逆に、変化の割合から全体の量（面積など）を求める方法である。",
              bullets=["関数の変化の割合を調べると、グラフの増減・接線・最大値・最小値が分かる。", "微分と積分は互いに逆の計算であり、面積は定積分で求められる。"],
              points=[tp("$h=0.1,\\ 0.01,\\ 0.001$ と小さくしたときの平均の速さを計算させ、値が $10$ に近づくようすを表にまとめさせる。",
                         ask="$h=0$ を代入してはいけないのはなぜか。", expect="分母が $0$ になって式が意味をもたないから。", timing="導入の冒頭")]),
        definition("df1", "微分係数と導関数",
                   "関数 $f(x)$ の $x=a$ から $x=a+h$ までの平均変化率 $\\dfrac{f(a+h)-f(a)}{h}$ が、$h\\to0$ のときに一定の値に近づくとき、その値を $x=a$ における微分係数といい $f'(a)$ で表す。$a$ に $f'(a)$ を対応させる関数 $f'(x)$ を導関数という。",
                   formula="$$f'(a)=\\lim_{h\\to0}\\dfrac{f(a+h)-f(a)}{h},\\qquad f'(x)=\\lim_{h\\to0}\\dfrac{f(x+h)-f(x)}{h}$$",
                   conditions=["$h$ は $0$ でない値をとりながら $0$ に近づく（$h=0$ は代入しない）。", "$\\{kf(x)+lg(x)\\}'=kf'(x)+lg'(x)$（$k,\\ l$ は定数）、定数の導関数は $0$。",
                               "微分係数 $f'(a)$ は、曲線 $y=f(x)$ 上の点 $(a,\\,f(a))$ における接線の傾きを表す。"],
                   points=[tp("「平均変化率＝2点を結ぶ直線の傾き」、その極限が「接線の傾き」であることを、割線が接線に近づく図で示す。",
                              ask="点 $(a+h,\\,f(a+h))$ が点 $(a,\\,f(a))$ に近づくと、2点を通る直線はどうなるか。", expect="接線に近づく。")]),
        derivation("dv1", "導関数の公式 $(x^n)'=nx^{n-1}$ の導出",
                   ["$f(x)=x^2$ のとき $\\dfrac{(x+h)^2-x^2}{h}=\\dfrac{2xh+h^2}{h}=2x+h$。$h\\to0$ として $f'(x)=2x$。",
                    "$f(x)=x^3$ のとき $(x+h)^3-x^3=3x^2h+3xh^2+h^3$ なので、$\\dfrac{(x+h)^3-x^3}{h}=3x^2+3xh+h^2\\to3x^2$。",
                    "一般に、二項定理より $(x+h)^n-x^n=nx^{n-1}h+(h^2\\text{ を因数にもつ項})$ なので、$h$ で割って $h\\to0$ とすると $nx^{n-1}$ が残る。",
                    "よって $(x^n)'=nx^{n-1}$（$n$ は正の整数）。また $(c)'=0$（$c$ は定数）。"],
                   body="分子を展開して $h$ で約分してから $h\\to0$ とするのが、定義に従って微分するときの手順である。",
                   points=[tp("$h$ で約分する前に $h\\to0$ とすると $\\dfrac{0}{0}$ になってしまうことを確認させ、「約分してから極限」の順序を強調する。",
                              caution="$h$ を残したまま答える、または約分前に $h=0$ を代入する誤りが多い。")]),
        theorem("th1", "接線・増減・極値",
                "$$y-f(a)=f'(a)(x-a)\\qquad\\qquad f'(x)>0\\Rightarrow\\text{増加},\\quad f'(x)<0\\Rightarrow\\text{減少}$$",
                ["接線は点 $(a,\\,f(a))$ を通り傾き $f'(a)$ の直線。", "$f'(x)$ の符号が $x=a$ の前後で正から負に変わるとき $f(a)$ は極大値、負から正に変わるとき極小値。",
                 "$f'(a)=0$ であっても、前後で $f'(x)$ の符号が変わらなければ極値ではない（例：$f(x)=x^3$ の $x=0$）。",
                 "閉区間での最大値・最小値は、極値と区間の両端の値を比べて決める。"],
                proof=["ある区間で $f'(x)>0$ ならば、その区間の各点で接線の傾きが正であり、グラフは右上がりになる（平均値の定理による厳密な証明は数学Ⅲで学ぶ）。",
                       "$x=a$ の前後で $f'(x)$ が正から負に変わると、$f(x)$ は $x=a$ の直前まで増加し直後から減少するので、$x=a$ の近くでは $f(a)$ が最大になる。これが極大の意味である。",
                       "極小についても、増減が逆になるだけで同様である。"],
                figure=figure("y=x^3-3x+1 のグラフ（x=-1 で極大値 3、x=1 で極小値 -1）",
                              plane((-3, 3), (-3, 5), unit=20, curves=[(lambda x: x ** 3 - 3 * x + 1, "")], points=[(-1, 3, "(-1,3)"), (1, -1, "(1,-1)")])),
                points=[tp("増減表は「$x$、$f'(x)$ の符号、$f(x)$ の矢印と値」の3段でかかせ、矢印の向きと $f'(x)$ の符号が対応していることを確かめさせる。"),
                        tp("$f'(a)=0$ は極値をとるための必要条件にすぎないことを、$y=x^3$ のグラフで示す。", ask="$y=x^3$ は $x=0$ で極値をとるか。", expect="とらない。常に増加している。", timing="極値の定義の直後")]),
        example("ex1", "例題1　増減と極値",
                "関数 $f(x)=x^3-3x+1$ の増減を調べ、極値を求めよ。",
                ["$f'(x)=3x^2-3=3(x+1)(x-1)$。$f'(x)=0$ とすると $x=-1,\\ 1$。",
                 "増減表：$x<-1$ で $f'(x)>0$（増加）、$-1<x<1$ で $f'(x)<0$（減少）、$x>1$ で $f'(x)>0$（増加）。",
                 "$f(-1)=-1+3+1=3$、$f(1)=1-3+1=-1$。"],
                "$x=-1$ で極大値 $3$、$x=1$ で極小値 $-1$",
                thinking="$f'(x)$ を因数分解して符号の変わり目を求め、増減表にまとめる。",
                points=[tp("極値は「値」と「そのときの $x$」をセットで答えさせる。")]),
        example("ex2", "例題2　接線の方程式",
                "曲線 $y=x^3-2x$ 上の点 $(2,\\,4)$ における接線の方程式を求めよ。",
                ["$f(x)=x^3-2x$ とすると $f'(x)=3x^2-2$。", "接線の傾きは $f'(2)=12-2=10$。", "$y-4=10(x-2)$ より $y=10x-16$。"],
                "$y=10x-16$",
                thinking="接線の傾きは導関数に接点の $x$ 座標を代入した値。点と傾きから直線の式をつくる。",
                misconceptions=[("傾きを $f'(x)=3x^2-2$ のまま使い、$y-4=(3x^2-2)(x-2)$ とする", "傾きは数値 $f'(2)=10$。$x$ を含んだままでは直線にならない")]),
        definition("df2", "不定積分と定積分",
                   "微分すると $f(x)$ になる関数を $f(x)$ の原始関数という。$F(x)$ を原始関数の1つとするとき、原始関数全体を $\\displaystyle\\int f(x)\\,dx=F(x)+C$（$C$ は積分定数）と表し、不定積分という。また、$F(b)-F(a)$ を $a$ から $b$ までの定積分という。",
                   formula="$$\\int x^n\\,dx=\\dfrac{1}{n+1}x^{n+1}+C,\\qquad \\int_a^bf(x)\\,dx=\\Bigl[F(x)\\Bigr]_a^b=F(b)-F(a)$$",
                   conditions=["$n$ は $0$ 以上の整数。$\\displaystyle\\int\\{kf(x)+lg(x)\\}\\,dx=k\\int f(x)\\,dx+l\\int g(x)\\,dx$。",
                               "定積分の値は原始関数の選び方（積分定数 $C$）によらない。",
                               "$\\displaystyle\\int_a^cf(x)\\,dx+\\int_c^bf(x)\\,dx=\\int_a^bf(x)\\,dx$、$\\displaystyle\\int_b^af(x)\\,dx=-\\int_a^bf(x)\\,dx$。"],
                   points=[tp("不定積分の答えは、微分してもとの関数に戻るかで必ず検算できることを習慣づける。", ask="$\\dfrac{1}{3}x^3+C$ を微分すると？", expect="$x^2$")]),
        theorem("th2", "定積分と面積",
                "$$S=\\int_a^b\\{f(x)-g(x)\\}\\,dx\\qquad(a\\leqq x\\leqq b\\ \\text{で}\\ f(x)\\geqq g(x))$$",
                ["区間で $f(x)\\geqq0$ のとき、$y=f(x)$ と $x$ 軸、$x=a,\\ x=b$ で囲まれた部分の面積は $\\displaystyle\\int_a^bf(x)\\,dx$。",
                 "$f(x)\\leqq0$ の部分では面積は $\\displaystyle-\\int f(x)\\,dx$ になる（上の関数から下の関数を引く）。"],
                proof=["$f(x)\\geqq0$ とし、$x=a$ から $x$ までの部分の面積を $S(x)$ とする。",
                       "$h>0$ のとき、$S(x+h)-S(x)$ は幅 $h$ の細長い部分の面積で、区間 $[x,\\,x+h]$ での $f$ の最小値を $m$、最大値を $M$ とすると $mh\\leqq S(x+h)-S(x)\\leqq Mh$。",
                       "$h$ で割って $h\\to0$ とすると $m,\\ M$ はともに $f(x)$ に近づくので $S'(x)=f(x)$（$h<0$ のときも同様）。",
                       "$S(x)$ は $f(x)$ の原始関数で $S(a)=0$ だから、$S(b)=S(b)-S(a)=\\displaystyle\\int_a^bf(x)\\,dx$。"],
                points=[tp("「面積を微分するともとの関数の高さになる」という関係が、微分と積分を結びつける要であることを強調する。", timing="面積の導入時")]),
        derivation("dv2", "$\\dfrac16$ 公式の導出",
                   ["$\\displaystyle\\int_\\alpha^\\beta(x-\\alpha)(x-\\beta)\\,dx$ で、$(x-\\alpha)(x-\\beta)=(x-\\alpha)\\{(x-\\alpha)-(\\beta-\\alpha)\\}=(x-\\alpha)^2-(\\beta-\\alpha)(x-\\alpha)$ と変形する。",
                    "$\\displaystyle\\int_\\alpha^\\beta(x-\\alpha)^2\\,dx=\\Bigl[\\dfrac{(x-\\alpha)^3}{3}\\Bigr]_\\alpha^\\beta=\\dfrac{(\\beta-\\alpha)^3}{3}$、$\\displaystyle\\int_\\alpha^\\beta(x-\\alpha)\\,dx=\\dfrac{(\\beta-\\alpha)^2}{2}$。",
                    "よって $\\dfrac{(\\beta-\\alpha)^3}{3}-(\\beta-\\alpha)\\cdot\\dfrac{(\\beta-\\alpha)^2}{2}=-\\dfrac{(\\beta-\\alpha)^3}{6}$。",
                    "放物線と直線（または2つの放物線）で囲まれた部分の面積は、差が $a(x-\\alpha)(x-\\beta)$ のとき $\\dfrac{|a|}{6}(\\beta-\\alpha)^3$。"],
                   body="交点の $x$ 座標 $\\alpha,\\ \\beta$ さえ分かれば、面積はすぐに求まる。ただし記述式の答案では、定積分の式を立ててから公式を使ったことを示す。",
                   points=[tp("$\\dfrac16$ 公式は「差の二次式の $x^2$ の係数」を使うことを確認させる。", caution="放物線 $y=2x^2$ と直線の場合に係数 $2$ を落とす誤りが多い。")]),
        example("ex3", "例題3　放物線と直線で囲まれた部分の面積",
                "放物線 $y=x^2-2x$ と直線 $y=x$ で囲まれた部分の面積 $S$ を求めよ。",
                ["交点：$x^2-2x=x$ より $x^2-3x=0$、$x=0,\\ 3$。", "$0\\leqq x\\leqq3$ では直線が上にある（例えば $x=1$ で $1>-1$）。",
                 "$S=\\displaystyle\\int_0^3\\{x-(x^2-2x)\\}\\,dx=\\int_0^3(-x^2+3x)\\,dx=\\Bigl[-\\dfrac{x^3}{3}+\\dfrac{3}{2}x^2\\Bigr]_0^3=-9+\\dfrac{27}{2}=\\dfrac92$。"],
                "$S=\\dfrac{9}{2}$",
                thinking="交点を求めて積分区間を決め、どちらが上にあるかを確かめてから「上－下」を積分する。",
                figure=figure("y=x^2-2x と y=x で囲まれた部分", plane((-1, 4), (-2, 4), unit=24, curves=[(lambda x: x * x - 2 * x, ""), (lambda x: x, "")],
                                                                    points=[(0, 0, "O"), (3, 3, "(3,3)")])),
                points=[tp("$\\dfrac16$ 公式で $\\dfrac{1}{6}(3-0)^3=\\dfrac92$ となり一致することを確かめさせる。")]),
        board("bd1", "板書案",
              [("① 微分", ["$f'(a)=\\displaystyle\\lim_{h\\to0}\\dfrac{f(a+h)-f(a)}{h}$", "$(x^n)'=nx^{n-1}$、$(c)'=0$", "接線 $y-f(a)=f'(a)(x-a)$", "例 $y=x^3-2x$、$(2,4)$ → $y=10x-16$"]),
               ("② 増減と極値", ["$f'(x)>0$ → 増加、$f'(x)<0$ → 減少", "増減表（$x$・$f'$・$f$）", "符号が変わる点で極値", "例 $x^3-3x+1$：極大 $3$、極小 $-1$"]),
               ("③ 積分と面積", ["$\\displaystyle\\int x^n\\,dx=\\dfrac{x^{n+1}}{n+1}+C$", "$\\displaystyle\\int_a^bf\\,dx=F(b)-F(a)$", "面積＝$\\displaystyle\\int_a^b(\\text{上}-\\text{下})\\,dx$", "$\\dfrac{|a|}{6}(\\beta-\\alpha)^3$"])],
              points=[tp("左から「微分 → 増減 → 積分」と並べ、③の下に「微分と積分は逆の計算」と矢印で結んで書く。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("接線の問題では、傾きは「導関数に接点の $x$ 座標を代入した数」であることを毎回言葉で確認させる。", ask="接線の傾きを求めるには何が必要か。", expect="接点の $x$ 座標と導関数。"),
               tp("極値の判定では、$f'(x)=0$ の解を求めただけで終わらせず、必ず増減表で前後の符号を確認させる。", caution="$f'(x)=3(x-1)^2$ のように符号が変わらない場合に極値があると答える誤りが多い。"),
               tp("区間での最大・最小は、極値だけでなく区間の両端の値も計算して比べることを徹底する。", timing="最大・最小の演習時"),
               tp("面積を求めるときは、交点・上下関係・積分区間を図で確認してから式を立てさせる。$x$ 軸より下の部分は定積分が負になることに注意させる。"),
               tp("不定積分では積分定数 $C$ を必ず書かせ、微分して戻るかで検算させる。")],
              misconceptions=[("$f'(a)=0$ ならば $x=a$ で必ず極値をとる", "前後で $f'(x)$ の符号が変わるときに限り極値"),
                              ("$\\displaystyle\\int x^2\\,dx=\\dfrac{x^3}{2}+C$", "$\\dfrac{x^{n+1}}{n+1}$ なので $\\dfrac{x^3}{3}+C$"),
                              ("$x$ 軸より下にある部分の面積も $\\displaystyle\\int_a^bf(x)\\,dx$ で求める", "$f(x)\\leqq0$ の区間では $-\\displaystyle\\int_a^bf(x)\\,dx$")]),
        summary("sm1", "まとめ",
                ["微分係数は平均変化率の極限で、接線の傾きを表す。$(x^n)'=nx^{n-1}$。",
                 "接線は $y-f(a)=f'(a)(x-a)$。$f'(x)$ の符号で増減が分かり、符号が変わる点で極値をとる。",
                 "不定積分は微分の逆。定積分は $F(b)-F(a)$ で、面積は「上の関数－下の関数」の定積分。"]),
        check("ck1", "確認問題",
              [("$f(x)=2x^3-x$ の導関数は？", "$f'(x)=6x^2-1$"), ("$\\displaystyle\\int_0^1(3x^2+2x)\\,dx$ の値は？", "$\\Bigl[x^3+x^2\\Bigr]_0^1=2$"),
               ("放物線 $y=x^2$ 上の点 $(1,\\,1)$ における接線の方程式は？", "$y'=2x$ より傾き $2$、$y=2x-1$")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

@gen("basic_check", 5, ["computation"])
def deriv_value(r):
    p = r.randint(-3, 3)
    if r.random() < 0.65:
        c = [nonzero(r, -3, 3), r.randint(-6, 6), r.randint(-6, 6), r.randint(-6, 6)]
        ftex = poly(*c)
        pre = []
    else:
        a, b, k = r.choice([1, 2, 3, -1]), nonzero(r, -4, 4), nonzero(r, -5, 5)
        c = [a, b, a * k, b * k]
        ftex = f"({poly(a, b)})(x^2{'+' if k > 0 else '-'}{abs(k)})"
        pre = [f"展開して $f(x)={poly(*c)}$。"]
    d = dcoef(c)
    v = ev(d, p)
    return sa(f"関数 $f(x)={ftex}$ の導関数 $f'(x)$ を求めなさい。また、微分係数 $f'({p})$ の値を求めなさい。",
              f"$f'(x)={poly(*d)}$、$f'({p})={ft(v)}$",
              f"$(x^n)'=nx^{{n-1}}$ を各項に用いて $f'(x)={poly(*d)}$。$x={p}$ を代入して ${ft(v)}$。", d=1, v=[f"f'(x)={poly(*d)}, f'({p})={v}"],
              ap="多項式は項ごとに $(x^n)'=nx^{n-1}$ を使って微分できる。積の形はまず展開する。微分係数は導関数に値を代入する。",
              steps=pre + [f"$f'(x)={poly(*d)}$。", f"$f'({p})={ft(v)}$。"],
              alt=[f"定義 $f'({p})=\\displaystyle\\lim_{{h\\to0}}\\dfrac{{f({p}+h)-f({p})}}{{h}}$ に従って計算しても同じ値になる（ただし計算量が多い）。"],
              pc=[("導関数を正しく求めている", 1), ("微分係数の値が正しい", 1)],
              pit=["定数項を微分して残してしまう（定数の導関数は $0$）。", "積の形のまま、各因数を微分して掛けてしまう。"],
              chk=(f"[expand(diff({py(*c)}, x)), {py(*d).replace('x', f'({p})')}]", f"[{py(*d)}, {fp(v)}]", "expand", "intermediate"))


@gen("basic_check", 4, ["concept", "computation"])
def by_definition(r):
    a, b, c = nonzero(r, -3, 3), r.randint(-5, 5), r.randint(-5, 5)
    p = r.randint(-3, 3)
    Fs = f"({a})*X**2+({b})*X+({c})"
    if r.random() < 0.5:
        v = 2 * a * p + b
        stem = f"関数 $f(x)={poly(a, b, c)}$ について、微分係数 $f'({p})$ を定義に従って求めなさい。"
        steps = [f"$f({p}+h)-f({p})={ft(2 * a * p + b)}h{'+' if a > 0 else '-'}{'' if abs(a) == 1 else abs(a)}h^2$。",
                 f"$\\dfrac{{f({p}+h)-f({p})}}{{h}}={ft(2 * a * p + b)}{'+' if a > 0 else '-'}{'' if abs(a) == 1 else abs(a)}h$（$h\\neq0$ で約分）。",
                 f"$h\\to0$ として $f'({p})={v}$。"]
        expl = f"$\\displaystyle f'({p})=\\lim_{{h\\to0}}\\dfrac{{f({p}+h)-f({p})}}{{h}}=\\lim_{{h\\to0}}({ft(2 * a * p + b)}{'+' if a > 0 else '-'}{'' if abs(a) == 1 else abs(a)}h)={v}$。"
        chk = (f"limit(({Fs.replace('X', f'({p}+h)')}-({Fs.replace('X', f'({p})')}))/h, h, 0)", str(v), None, "intermediate")
        ap = "定義 $f'(a)=\\displaystyle\\lim_{h\\to0}\\dfrac{f(a+h)-f(a)}{h}$ に当てはめ、分子を展開して $h$ で約分してから $h\\to0$ とする。"
        alt = [f"導関数 $f'(x)={poly(2 * a, b)}$ に $x={p}$ を代入して ${v}$ となることで確かめられる。"]
        pc = [("分子を展開して $h$ で約分している", 1), ("極限値が正しい", 1)]
    else:
        q = p + r.randint(1, 4)
        v = a * (p + q) + b
        stem = f"関数 $f(x)={poly(a, b, c)}$ において、$x$ の値が ${p}$ から ${q}$ まで変化するときの平均変化率を求めなさい。"
        steps = [f"$f({q})={ft(ev([a, b, c], q))}$、$f({p})={ft(ev([a, b, c], p))}$。",
                 f"平均変化率は $\\dfrac{{f({q})-f({p})}}{{{q}-({p})}}=\\dfrac{{{ft(ev([a, b, c], q) - ev([a, b, c], p))}}}{{{q - p}}}={v}$。"]
        expl = f"平均変化率 $\\dfrac{{f({q})-f({p})}}{{{q}-({p})}}={v}$。2点を結ぶ直線の傾きにあたる。"
        chk = (f"(({Fs.replace('X', f'({q})')})-({Fs.replace('X', f'({p})')}))/({q}-({p}))", str(v), None, "intermediate")
        ap = "平均変化率は $\\dfrac{f(b)-f(a)}{b-a}$。グラフ上の2点を結ぶ直線の傾きである。"
        alt = [f"二次関数 $ax^2+bx+c$ の平均変化率は $a(p+q)+b$ と表せる。${a}\\times({p}+{q})+({b})={v}$ で確かめられる。"]
        pc = [("関数の値を正しく計算している", 1), ("平均変化率が正しい", 1)]
    return sa(stem, f"${v}$", expl, d=2, ap=ap, steps=steps, alt=alt, pc=pc,
              pit=["分母の $x$ の増加量を逆にしたり、符号を誤ったりする。", "$h$ で約分する前に $h=0$ を代入してしまう。"], chk=chk)


@gen("basic_check", 5, ["computation"])
def indefinite(r):
    A, B, C = nonzero(r, -3, 3), r.randint(-4, 4), r.randint(-6, 6)
    f = [3 * A, 2 * B, C]
    if r.random() < 0.35 and A != 0:
        # (px+q)(sx+t) の形で与える
        cands = [(pp, qq, ss, tt) for pp in (1, 3, -1, -3) for qq in range(-4, 5) for ss in (1, -1, 3) for tt in range(-4, 5)
                 if pp * ss == 3 * A and pp * tt + qq * ss == 2 * B and qq * tt == C]
        if cands:
            pp, qq, ss, tt = r.choice(cands)
            itex = f"({poly(pp, qq)})({poly(ss, tt)})"
            pre = [f"展開して ${poly(*f)}$ とする。"]
        else:
            itex, pre = poly(*f), []
    else:
        itex, pre = poly(*f), []
    Ftex = poly(A, B, C, 0)
    return sa(f"不定積分 $\\displaystyle\\int({itex})\\,dx$ を求めなさい。", f"${Ftex}+C$（$C$ は積分定数）",
              f"$\\displaystyle\\int x^n\\,dx=\\dfrac{{x^{{n+1}}}}{{n+1}}+C$ を項ごとに用いる。", d=2, v=[f"{Ftex}+C"],
              ap="不定積分は「微分すると被積分関数になる関数」。項ごとに $x^n\\to\\dfrac{x^{n+1}}{n+1}$ とする。積の形はまず展開する。",
              steps=pre + [f"${poly(*f)}$ の各項を積分する。", f"${Ftex}+C$。"],
              alt=[f"答えを微分すると ${poly(*f)}$ に戻ることを確かめる。"],
              pc=[("各項を正しく積分している", 1), ("積分定数 $C$ を書いている", 1)],
              pit=["積分定数 $C$ を書き忘れる。", "$x^2$ を $\\dfrac{x^3}{2}$ とするなど、割る数を誤る。"],
              chk=(f"expand(diff({py(A, B, C, 0)}, x))", py(*f), "expand", "intermediate"))


@gen("basic_check", 4, ["computation"])
def definite(r):
    A, B, C = nonzero(r, -2, 2), r.randint(-4, 4), r.randint(-6, 6)
    f = [3 * A, 2 * B, C]
    Fc = [A, B, C, 0]
    lo = r.randint(-3, 1)
    hi = lo + r.randint(1, 4)
    v = ev(Fc, hi) - ev(Fc, lo)
    if r.random() < 0.3:
        m = r.randint(lo + 1, hi) if hi > lo + 1 else hi
        stem = f"次の定積分を計算しなさい。$$\\int_{{{lo}}}^{{{m}}}({poly(*f)})\\,dx+\\int_{{{m}}}^{{{hi}}}({poly(*f)})\\,dx$$"
        pre = [f"被積分関数が同じなので、区間をつないで $\\displaystyle\\int_{{{lo}}}^{{{hi}}}({poly(*f)})\\,dx$ とまとめる。"]
    else:
        stem = f"定積分 $\\displaystyle\\int_{{{lo}}}^{{{hi}}}({poly(*f)})\\,dx$ の値を求めなさい。"
        pre = []
    return sa(stem, f"${ft(v)}$",
              f"原始関数 $F(x)={poly(*Fc)}$ を用いて $F({hi})-F({lo})={ft(ev(Fc, hi))}-({ft(ev(Fc, lo))})={ft(v)}$。", d=2,
              ap="原始関数 $F(x)$ を1つ求め、$F(\\text{上端})-F(\\text{下端})$ を計算する。積分定数は打ち消し合うので不要。",
              steps=pre + [f"$\\Bigl[{poly(*Fc)}\\Bigr]_{{{lo}}}^{{{hi}}}$。", f"$=({ft(ev(Fc, hi))})-({ft(ev(Fc, lo))})={ft(v)}$。"],
              alt=["項ごとに $\\displaystyle\\int_a^bx^n\\,dx=\\dfrac{b^{n+1}-a^{n+1}}{n+1}$ を計算して足し合わせてもよい。"],
              pc=[("原始関数を正しく求めている", 1), ("値が正しい", 1)],
              pit=["$F(\\text{下端})-F(\\text{上端})$ と逆に引く。", "負の数を代入するときに符号を誤る。"],
              chk=(f"integrate({py(*f)}, [x, {lo}, {hi}])", fp(v)))


@gen("basic_check", 2, ["concept", "condition_check"])
def extremum_judge(r):
    kind = r.choice(["max", "min", "flat", "nonzero"])
    if kind == "flat":
        p = r.randint(-3, 3)
        d = r.randint(-4, 4)
        c = [1, -3 * p, 3 * p * p, d]
        q = p
        fd = f"3{fac(p)}^2"
    else:
        al, be = sorted(r.sample(range(-3, 4), 2))
        a = 1 if (al + be) % 2 == 0 else 2
        c = [a, F(-3 * a * (al + be), 2), 3 * a * al * be, r.randint(-4, 4)]
        fd = f"{3 * a}{fac(al)}{fac(be)}"
        if kind == "max":
            q = al
        elif kind == "min":
            q = be
        else:
            q = r.choice([x for x in range(-4, 5) if x not in (al, be)])
    c1, c2 = f"$x={q}$ で極大値をとる", f"$x={q}$ で極小値をとる"
    c3, c4 = f"$f'({q})=0$ であるが、$x={q}$ で極値をとらない", f"$f'({q})\\neq0$ であり、$x={q}$ で極値をとらない"
    right = {"max": c1, "min": c2, "flat": c3, "nonzero": c4}[kind]
    dv = ev(dcoef(c), q)
    why_all = {c1: ("$f'(x)$ の符号が $x=" + str(q) + "$ の前後で正から負に変わるときに限り極大。この関数ではそうなっていない。", "極大の判定条件の誤解"),
               c2: ("$f'(x)$ の符号が $x=" + str(q) + "$ の前後で負から正に変わるときに限り極小。この関数ではそうなっていない。", "極小の判定条件の誤解"),
               c3: (f"実際には $f'({q})={ft(dv)}$ である。" if dv != 0 else "前後で符号が変わるので極値をとる。", "$f'(a)=0$ と極値の関係の混同"),
               c4: (f"$f'({q})=0$ なので「$f'({q})\\neq0$」は誤り。", "微分係数の計算の誤り")}
    ch = [right] + [w for w in (c1, c2, c3, c4) if w != right]
    expl = {"max": f"$f'(x)={fd}$ は $x={q}$ の前後で正から負に変わるので極大。",
            "min": f"$f'(x)={fd}$ は $x={q}$ の前後で負から正に変わるので極小。",
            "flat": f"$f'(x)={fd}\\geqq0$ で、$x={q}$ の前後で符号が変わらない（常に増加）ので極値ではない。",
            "nonzero": f"$f'({q})={ft(dv)}\\neq0$ なので、$x={q}$ の近くで単調に{'増加' if dv > 0 else '減少'}しており極値ではない。"}[kind]
    return mc(f"関数 $f(x)={poly(*[int(x) for x in c])}$ の $x={q}$ における様子として正しいものを選びなさい。", ch, expl, d=2,
              ap="$f'(x)$ を求めて因数分解し、$x=" + str(q) + "$ での値と、その前後での符号の変化を調べる。",
              steps=[f"$f'(x)={poly(*[int(x) for x in dcoef(c)])}={fd}$。", f"$f'({q})={ft(dv)}$。", expl],
              alt=["増減表をかいて、$x=" + str(q) + "$ の前後の矢印の向きを確かめる。"],
              pc=[("$f'(x)$ を正しく求めている", 1), ("符号の変化から正しく判断している", 1)],
              why={w: why_all[w] for w in ch if w != right},
              chk=(f"{py(*dcoef(c)).replace('x', f'({q})')}", fp(dv), None, "intermediate"))


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 5, ["computation", "concept"])
def tangent(r):
    if r.random() < 0.6:
        c = [nonzero(r, -2, 2), r.randint(-3, 3), r.randint(-4, 4), r.randint(-4, 4)]
        t = r.randint(-2, 2)
        y0 = ev(c, t)
        m = ev(dcoef(c), t)
        n = y0 - m * t
        stem = f"曲線 $y={poly(*c)}$ 上の点 $({t},\\,{ft(y0)})$ における接線の方程式を求めなさい。"
        steps = [f"$y'={poly(*dcoef(c))}$。", f"接線の傾きは $x={t}$ を代入して ${ft(m)}$。", f"$y-({ft(y0)})={ft(m)}(x-({t}))$ より $y={line_tex(m, n)}$。"]
        ap = "接線の傾きは導関数に接点の $x$ 座標を代入した値。点と傾きから直線の式をつくる。"
        chk = (f"[{py(*dcoef(c)).replace('x', f'({t})')}, {py(*c).replace('x', f'({t})')}-({fp(m)})*({t})]", f"[{fp(m)}, {fp(n)}]", None, "intermediate")
        alt = [f"接線の式と曲線の式を連立すると、$x={t}$ を重解（2重以上の解）にもつことで確かめられる。"]
    else:
        a, b, cc = nonzero(r, -2, 2), r.randint(-4, 4), r.randint(-4, 4)
        t = r.randint(-3, 3)
        m = 2 * a * t + b
        y0 = ev([a, b, cc], t)
        n = y0 - m * t
        stem = f"放物線 $y={poly(a, b, cc)}$ の接線のうち、傾きが ${m}$ であるものの方程式と接点の座標を求めなさい。"
        steps = [f"$y'={poly(2 * a, b)}$。接点の $x$ 座標を $t$ とすると ${poly(2 * a, b, var='t')}={m}$ より $t={t}$。", f"接点は $({t},\\,{ft(y0)})$。",
                 f"$y-({ft(y0)})={m}(x-({t}))$ より $y={line_tex(m, n)}$。"]
        ap = "傾きが分かっているので、「導関数の値＝傾き」となる接点の $x$ 座標を先に求める。"
        chk = (f"[solve({2 * a}*t+({b})-({m}), t)[0], ({a})*({t})**2+({b})*({t})+({cc})-({m})*({t})]", f"[{t}, {fp(n)}]", None, "intermediate")
        alt = [f"直線 $y={m}x+k$ と放物線を連立した二次方程式が重解をもつ条件（判別式 $D=0$）から $k$ を求めてもよい。"]
    ans = f"$y={line_tex(m, n)}$"
    if "傾きが" in stem:
        ans += f"（接点 $({t},\\,{ft(y0)})$）"
    return sa(stem, ans, f"接線の傾き ${ft(m)}$、接点 $({t},\\,{ft(y0)})$。$y-f(t)=f'(t)(x-t)$ を用いる。", d=3, v=[f"y={line_tex(m, n)}"],
              ap=ap, steps=steps, alt=alt,
              pc=[("導関数を正しく求めている", 1), ("接線の傾き・接点を正しく求めている", 1), ("接線の方程式が正しい", 2)],
              pit=["傾きに $x$ を含む導関数をそのまま使ってしまう。", "$y-y_1=m(x-x_1)$ の符号を誤る。"], chk=chk)


@gen("standard_practice", 5, ["computation", "written_reasoning"])
def extrema(r):
    c, al, be = cubic_from_roots(r)
    while c == [1, 0, -3, 1]:  # 例題1と同じ関数は避ける
        c, al, be = cubic_from_roots(r)
    a = c[0]
    fa, fb = ev(c, al), ev(c, be)
    if a > 0:
        xM, M, xm, m = al, fa, be, fb
    else:
        xM, M, xm, m = be, fb, al, fa
    ci = [int(x) for x in c]
    d = dcoef(ci)
    return sa(f"関数 $f(x)={poly(*ci)}$ の増減を調べ、極値を求めなさい。",
              f"$x={xM}$ で極大値 ${ft(M)}$、$x={xm}$ で極小値 ${ft(m)}$",
              f"$f'(x)={poly(*d)}={3 * a}{fac(al)}{fac(be)}$。$x={al},\\ {be}$ の前後で符号が変わる。", d=3,
              ap="$f'(x)$ を因数分解して $f'(x)=0$ となる $x$ を求め、その前後の符号を増減表で調べる。",
              steps=[f"$f'(x)={poly(*d)}={3 * a}{fac(al)}{fac(be)}$。", f"$f'(x)=0$ とすると $x={al},\\ {be}$。",
                     f"$x^3$ の係数が{'正' if a > 0 else '負'}なので、$f'(x)$ は $x<{al}$ で{'正' if a > 0 else '負'}、${al}<x<{be}$ で{'負' if a > 0 else '正'}、$x>{be}$ で{'正' if a > 0 else '負'}。",
                     f"$f({al})={ft(fa)}$、$f({be})={ft(fb)}$。", f"$x={xM}$ で極大値 ${ft(M)}$、$x={xm}$ で極小値 ${ft(m)}$。"],
              alt=["グラフの概形（$x^3$ の係数の符号で両端の向きが決まる）をかいて、極大・極小の位置を確かめる。",
                   f"極大値と極小値の差は $\\displaystyle\\int_{{{al}}}^{{{be}}}f'(x)\\,dx$ の絶対値に等しいことからも検算できる（差 ${ft(abs(fb - fa))}$）。"],
              pc=[("$f'(x)$ を求め因数分解している", 1), ("増減表で符号の変化を調べている", 1), ("極大値・極小値とそのときの $x$ が正しい", 2)],
              pit=["$x^3$ の係数が負のときに、極大と極小を逆にする。", "極値の $x$ の値だけを答えて、極値（関数の値）を答えない。"],
              chk=(f"[{py(*ci).replace('x', f'({xM})')}, {py(*ci).replace('x', f'({xm})')}]", f"[{fp(M)}, {fp(m)}]", None, "intermediate"))


@gen("standard_practice", 4, ["computation", "condition_check"])
def interval_maxmin(r):
    while True:
        c, al, be = cubic_from_roots(r, (1, -1))
        lo = r.randint(-4, 1)
        hi = lo + r.randint(2, 5)
        if lo < al < hi or lo < be < hi:
            break
    ci = [int(x) for x in c]
    cand = sorted({lo, hi} | {x for x in (al, be) if lo < x < hi})
    vals = {x: ev(ci, x) for x in cand}
    M, m = max(vals.values()), min(vals.values())
    xM = [x for x in cand if vals[x] == M]
    xm = [x for x in cand if vals[x] == m]
    fx = lambda xs: ",\\ ".join(f"x={x}" for x in xs)  # noqa: E731
    return sa(f"関数 $f(x)={poly(*ci)}\\ ({lo}\\leqq x\\leqq{hi})$ の最大値と最小値を求めなさい。また、そのときの $x$ の値も答えなさい。",
              f"最大値 ${ft(M)}$（${fx(xM)}$）、最小値 ${ft(m)}$（${fx(xm)}$）",
              "区間内の極値と、区間の両端の値を比べる。", d=3,
              ap="閉区間での最大・最小は「区間内の極値」と「両端の値」の中にある。増減表を区間に限ってかき、候補の値を比べる。",
              steps=[f"$f'(x)={poly(*dcoef(ci))}={3 * c[0]}{fac(al)}{fac(be)}$、$f'(x)=0$ とすると $x={al},\\ {be}$。",
                     f"区間 ${lo}\\leqq x\\leqq{hi}$ で増減表をかく。", "候補の値：" + "、".join(f"$f({x})={ft(v)}$" for x, v in vals.items()) + "。",
                     f"最大値 ${ft(M)}$、最小値 ${ft(m)}$。"],
              alt=["候補の点の値をすべて計算して比べれば、増減表の細部に頼らずに確実に求められる。"],
              pc=[("導関数から極値の候補を求めている", 1), ("区間の両端の値も調べている", 1), ("最大値・最小値と $x$ の値が正しい", 2)],
              pit=["区間の外にある極値を候補に入れてしまう。", "両端の値を調べず、極大値を最大値と答える。"],
              chk=(f"[Max({', '.join(py(*ci).replace('x', f'({x})') for x in cand)}), Min({', '.join(py(*ci).replace('x', f'({x})') for x in cand)})]", f"[{fp(M)}, {fp(m)}]", None, "intermediate"))


@gen("standard_practice", 3, ["computation", "multiple_solutions"])
def area_two(r):
    al, be = sorted(r.sample(range(-3, 5), 2))
    kind = r.choice(["line", "line", "parab"])
    if kind == "line":
        a = r.choice([1, -1, 2, -2, 3])
        b, cc = r.randint(-3, 3), r.randint(-3, 3)
        m, n = b + a * (al + be), cc - a * al * be
        f1, f2 = f"y={poly(a, b, cc)}", f"y={line_tex(m, n)}"
        name = f"放物線 ${f1}$ と直線 ${f2}$"
        k = a
        g1, g2 = [a, b, cc], [0, m, n]
    else:
        a1 = r.choice([1, 2])
        k = r.choice([2, 3]) if a1 == 1 else 3
        a2 = a1 - k
        b2, c2 = r.randint(-3, 3), r.randint(-3, 3)
        b1, c1 = b2 - k * (al + be), c2 + k * al * be
        f1, f2 = f"y={poly(a1, b1, c1)}", f"y={poly(a2, b2, c2)}"
        name = f"2つの放物線 ${f1}$、${f2}$"
        g1, g2 = [a1, b1, c1], [a2, b2, c2]
    S = F(abs(k) * (be - al) ** 3, 6)
    diff = [g1[i] - g2[i] for i in range(3)]
    upper = "第2式" if k > 0 else "第1式"
    return sa(f"{name} で囲まれた部分の面積を求めなさい。", f"${ft(S)}$",
              f"交点の $x$ 座標は ${al},\\ {be}$。差は ${poly(*diff)}={k}{fac(al)}{fac(be)}$ で、面積は $\\dfrac{{{abs(k)}}}{{6}}({be}-({al}))^3={ft(S)}$。", d=3,
              ap="交点の $x$ 座標を求め、その間で「上の関数－下の関数」を積分する。差が $a(x-\\alpha)(x-\\beta)$ の形なら $\\dfrac{|a|}{6}(\\beta-\\alpha)^3$ が使える。",
              steps=[f"2式の差：$({poly(*g1)})-({poly(*g2)})={poly(*diff)}={k}{fac(al)}{fac(be)}$。", f"交点の $x$ 座標は $x={al},\\ {be}$。",
                     f"${al}<x<{be}$ では{upper}のグラフが上にある。",
                     f"$S=\\displaystyle\\int_{{{al}}}^{{{be}}}\\{{-({poly(*diff)})\\}}\\,dx$" if k > 0 else f"$S=\\displaystyle\\int_{{{al}}}^{{{be}}}({poly(*diff)})\\,dx$",
                     f"$=\\dfrac{{{abs(k)}}}{{6}}({be}-({al}))^3={ft(S)}$。"],
              alt=["$\\dfrac16$ 公式を使わずに、原始関数を求めて上端・下端を代入しても同じ値になる（検算に使える）。"],
              pc=[("交点の $x$ 座標を正しく求めている", 1), ("上下関係を確認して定積分の式を立てている", 2), ("面積が正しい", 1)],
              pit=["差の $x^2$ の係数を考えずに $\\dfrac16(\\beta-\\alpha)^3$ とする。", "上下を逆にして負の値を答える。"],
              chk=(f"Abs(integrate({py(*diff)}, [x, {al}, {be}]))", fp(S)))


@gen("standard_practice", 3, ["computation", "condition_check"])
def area_axis(r):
    al, be = sorted(r.sample(range(-3, 4), 2))
    k = r.choice([1, -1])
    c = [k, -k * (al + be), k * al * be]
    if r.random() < 0.5:
        lo, hi = al - r.randint(1, 2), be
        parts = [(lo, al), (al, be)]
    else:
        lo, hi = al, be + r.randint(1, 2)
        parts = [(al, be), (be, hi)]
    Fc = [F(k, 3), F(-k * (al + be), 2), k * al * be, 0]

    def I(a, b):
        return ev(Fc, b) - ev(Fc, a)
    S = sum(abs(I(a, b)) for a, b in parts)
    net = I(lo, hi)
    return sa(f"曲線 $y={poly(*c)}$ と $x$ 軸、および2直線 $x={lo}$、$x={hi}$ で囲まれた2つの部分の面積の和 $S$ を求めなさい。", f"${ft(S)}$",
              f"$y={'-' if k == -1 else ''}{fac(al)}{fac(be)}$ は区間の途中で符号が変わるので、区間を分けて面積を足す。", d=3,
              ap="グラフが $x$ 軸より下にある部分では、定積分の値が負になる。$x$ 軸との交点で区間を分け、下にある部分は符号を変えてから足す。",
              steps=[f"$y=0$ となるのは $x={al},\\ {be}$。区間 ${lo}\\leqq x\\leqq{hi}$ を " + "、".join(f"$[{a},\\,{b}]$" for a, b in parts) + " に分ける。"]
              + [f"$\\displaystyle\\int_{{{a}}}^{{{b}}}({poly(*c)})\\,dx={ft(I(a, b))}$（{'上' if I(a, b) > 0 else '下'}にある部分）。" for a, b in parts]
              + [f"$S=" + "+".join(ft(abs(I(a, b))) for a, b in parts) + f"={ft(S)}$。"],
              alt=[f"そのまま $\\displaystyle\\int_{{{lo}}}^{{{hi}}}$ を計算すると ${ft(net)}$ となり、上下の部分が打ち消し合ってしまう。面積とは一致しないことを確かめる。"],
              pc=[("$x$ 軸との交点で区間を分けている", 1), ("各部分の定積分を正しく計算している", 2), ("符号を調整して面積の和を正しく求めている", 1)],
              pit=["区間を分けずに定積分を1回で計算してしまう。", "$x$ 軸より下の部分の定積分（負の値）をそのまま足す。"],
              chk=(" + ".join(f"Abs(integrate({py(*c)}, [x, {a}, {b}]))" for a, b in parts), fp(S)))


# ======================================================================
# C 思考力・記述応用
# ======================================================================

def lin_a(s, t):
    """s*a+t の LaTeX。"""
    if s == 0:
        return str(t)
    head = "a" if s == 1 else ("-a" if s == -1 else f"{s}a")
    return head + ("" if t == 0 else (f"+{t}" if t > 0 else f"{t}"))


@gen("thinking_writing", 3, ["cross_unit", "condition_check", "written_reasoning"], rel=["HS-MATH1-U03"])
def param_extreme(r):
    r1, r2 = sorted(r.sample([-9, -6, -3, 0, 3, 6, 9], 2))
    s, t = (r1 + r2) // 3, -(r1 * r2) // 3
    if s == 0:
        mid = "" if t == 0 else (f"{'+' if t > 0 else '-'}{'' if abs(t) == 1 else abs(t)}x")
        dmid = "" if t == 0 else (f"+{t}" if t > 0 else f"{t}")
    elif t == 0:
        mid = ("+" if s > 0 else "") + lin_a(s, t) + "x"
        dmid = ("+" if s > 0 else "") + lin_a(s, t)
    else:
        mid = f"+({lin_a(s, t)})x"
        dmid = f"+({lin_a(s, t)})"
    d0 = r.randint(-3, 3)
    tail = "" if d0 == 0 else (f"+{d0}" if d0 > 0 else f"{d0}")
    ftex = f"x^3+ax^2{mid}{tail}"
    fd = f"3x^2+2ax{dmid}"
    D4 = poly(1, -(r1 + r2), r1 * r2, var="a")
    has = r.random() < 0.6
    ans = f"$a<{r1},\\ {r2}<a$" if has else f"${r1}\\leqq a\\leqq{r2}$"
    word = "極値をもつ" if has else "極値をもたない"
    return desc(f"$a$ を定数とする。関数 $f(x)={ftex}$ が{word}ような $a$ の値の範囲を求めなさい。理由も示すこと。", ans,
                f"$f'(x)={fd}$。極値をもつ $\\iff$ $f'(x)=0$ が異なる2つの実数解をもつ $\\iff$ $\\dfrac{{D}}{{4}}>0$。",
                [("極値をもつ条件を「$f'(x)=0$ が異なる2つの実数解をもつ」と言いかえている", 3), ("判別式を正しく計算している", 2), ("二次不等式を正しく解いている", 3)],
                d=4, p=8, lines=8,
                ap="三次関数が極値をもつのは、$f'(x)$ の符号が変わる点があるとき、すなわち二次方程式 $f'(x)=0$ が異なる2つの実数解をもつとき。数学Ⅰの判別式と二次不等式に帰着する。",
                steps=[f"$f'(x)={fd}$。",
                       "$f'(x)=0$ が異なる2つの実数解をもてば、その前後で $f'(x)$ の符号が変わり極値をもつ。重解または実数解なしなら $f'(x)\\geqq0$ で常に増加し、極値をもたない。",
                       f"$\\dfrac{{D}}{{4}}=a^2-3\\cdot({lin_a(s, t)})={D4}={fac(r1).replace('x', 'a')}{fac(r2).replace('x', 'a')}$。",
                       (f"極値をもつ条件 $\\dfrac{{D}}{{4}}>0$ より $a<{r1},\\ {r2}<a$。" if has else f"極値をもたない条件 $\\dfrac{{D}}{{4}}\\leqq0$ より ${r1}\\leqq a\\leqq{r2}$。")],
                alt=[f"境界の $a={r1}$ を代入すると $f'(x)$ が $3(x+\\cdots)^2$ の形の完全平方式になり（重解）、極値をもたないことが確かめられる。"],
                pc=[("条件の言いかえ", 3), ("判別式の計算", 2), ("不等式の解", 3)],
                pit=["$D\\geqq0$ としてしまい、重解（$D=0$）の場合を含めてしまう（重解では $f'(x)$ の符号が変わらない）。" if has
                     else "$D<0$ としてしまい、重解（$D=0$）の場合を落とす（重解でも極値をもたない）。", "$f'(x)$ の定数項の計算で $a$ を含む部分を誤る。"],
                chk=(f"solve(a**2-3*(({s})*a+({t})), a)", f"[{r1}, {r2}]", "set", "intermediate"))


@gen("thinking_writing", 3, ["cross_unit", "written_reasoning", "multiple_solutions"], rel=["HS-MATH2-U03"])
def tangent_from_point(r):
    while True:
        a = r.choice([1, 1, -1, 2])
        b, c = r.randint(-3, 3), r.randint(-3, 3)
        t1, t2 = sorted(r.sample(range(-4, 5), 2))
        if (t1 + t2) % 2 == 0:
            break
    p = (t1 + t2) // 2
    q = a * t1 * t2 + b * p + c
    lines = [(t, 2 * a * t + b, -a * t * t + c) for t in (t1, t2)]
    ans = "、".join(f"$y={line_tex(m, n)}$（接点 $({t},\\,{ft(ev([a, b, c], t))})$）" for t, m, n in lines)
    tl = f"y=({poly(2 * a, b, var='t')})x{polyf(-a, 0, c, var='t') if polyf(-a, 0, c, var='t').startswith('-') else '+' + polyf(-a, 0, c, var='t')}"
    return desc(f"点 $({p},\\,{q})$ から放物線 $y={poly(a, b, c)}$ に引いた接線の方程式と、その接点の座標をすべて求めなさい。", ans,
                f"接点を $(t,\\,{poly(a, b, c, var='t')})$ とおき、接線が点 $({p},\\,{q})$ を通る条件から $t$ を求める。",
                [("接点の $x$ 座標を $t$ とおいて接線の方程式を表している", 3), ("点を通る条件から $t$ の方程式を立てて解いている", 3), ("接線と接点をすべて正しく答えている", 2)],
                d=4, p=8, lines=10,
                ap=f"点 $({p},\\,{q})$ は放物線上にない。接点が分からないので、接点の $x$ 座標を $t$ とおいて接線を表し、その接線が与えられた点を通る条件を使う。",
                steps=[f"$y'={poly(2 * a, b)}$。接点を $(t,\\,{poly(a, b, c, var='t')})$ とすると、接線は ${tl}$。",
                       f"これが点 $({p},\\,{q})$ を通るので、代入して整理すると ${poly(a, -2 * a * p, a * t1 * t2, var='t')}=0$。",
                       f"これを解いて $t={t1},\\ {t2}$。", f"よって {ans}。"],
                alt=[f"点 $({p},\\,{q})$ を通る直線 $y=m(x-({p}))+({q})$ と放物線を連立した二次方程式が重解をもつ条件（判別式 $=0$）から $m$ を求めてもよい。"],
                pc=[("接線の式の設定", 3), ("通る条件と $t$ の決定", 3), ("答え", 2)],
                pit=["与えられた点を接点と誤解し、その点での微分係数を傾きにしてしまう。", "接線が2本あることに気づかず1本だけ答える。"],
                chk=(f"solve(({a})*t**2-2*({a})*({p})*t+({q})-({b})*({p})-({c}), t)", f"[{t1}, {t2}]", "set", "intermediate"))


BOXES = [("sq", 6), ("sq", 9), ("sq", 12), ("sq", 18), ("sq", 24), ("sq", 30), ("sq", 15), ("sq", 36),
         ("rect", (3, 8)), ("rect", (5, 8)), ("rect", (8, 15)), ("rect", (7, 15)), ("rect", (16, 21)), ("rect", (10, 16)), ("rect", (6, 16)), ("rect", (15, 24))]


@gen("thinking_writing", 2, ["application", "written_reasoning"])
def box_volume(r):
    kind, val = r.choice(BOXES)
    if kind == "sq":
        A = B = val
        sheet = f"1辺の長さが ${val}$ cm の正方形の厚紙"
    else:
        A, B = val
        sheet = f"縦 ${A}$ cm、横 ${B}$ cm の長方形の厚紙"
    x = sp.Symbol("x")
    V = sp.expand(x * (A - 2 * x) * (B - 2 * x))
    crit = [s for s in sp.solve(sp.diff(V, x), x) if 0 < s < sp.Rational(min(A, B), 2)]
    x0 = crit[0]
    Vmax = V.subs(x, x0)
    dV = sp.factor(sp.diff(V, x))
    return desc(f"{sheet}の四すみから、1辺の長さが $x$ cm の正方形を切り取り、残りを折り曲げてふたのない箱をつくる。箱の容積 $V$ の最大値と、そのときの $x$ の値を求めなさい。",
                f"$x={sp.latex(x0)}$ のとき最大値 ${sp.latex(Vmax)}$（cm$^3$）",
                f"$V=x({A}-2x)({B}-2x)\\ \\left(0<x<{sp.latex(sp.Rational(min(A, B), 2))}\\right)$ を微分して増減を調べる。",
                [("$V$ を $x$ の式で表し、$x$ の変域を示している", 2), ("導関数を求め増減を調べている", 3), ("最大値とそのときの $x$ が正しい", 3)], d=4, p=8, lines=10,
                ap="容積を1つの変数 $x$ の三次関数で表し、変域（辺の長さが正）の中で増減表をかく。",
                steps=[f"底面は縦 ${A}-2x$、横 ${B}-2x$、高さ $x$ なので $V=x({A}-2x)({B}-2x)={sp.latex(V)}$。",
                       f"辺の長さは正なので $0<x<{sp.latex(sp.Rational(min(A, B), 2))}$。",
                       f"$V'={sp.latex(sp.expand(sp.diff(V, x)))}={sp.latex(dV)}$。変域内で $V'=0$ となるのは $x={sp.latex(x0)}$。",
                       f"$x={sp.latex(x0)}$ の前後で $V'$ は正から負に変わるので、ここで極大かつ最大。", f"最大値 $V={sp.latex(Vmax)}$。"],
                alt=["変域の端（$x\\to0$ や辺の長さが $0$ になるとき）では $V\\to0$ なので、変域内のただ1つの極大値が最大値になる、と説明してもよい。"],
                pc=[("式と変域", 2), ("増減の調べ方", 3), ("最大値と $x$", 3)],
                pit=["変域を考えず、変域外の $V'=0$ の解も候補にしてしまう。", "底面の辺の長さを ${0}-x$ のように、切り取る分を片側だけ引いてしまう。".format(A)],
                chk=(f"({sp.sstr(x0)})*({A}-2*({sp.sstr(x0)}))*({B}-2*({sp.sstr(x0)}))", sp.sstr(Vmax), None, "intermediate"))


@gen("thinking_writing", 2, ["computation", "written_reasoning"])
def area_tangent(r):
    a = r.choice([1, 1, 2, -1, 3])
    p, q = r.randint(-2, 2), r.randint(-3, 3)
    c = [a, -2 * a * p, a * p * p + q]
    if r.random() < 0.5:
        t = p + nonzero(r, -3, 3)
        m, n = 2 * a * t - 2 * a * p, ev(c, t) - (2 * a * t - 2 * a * p) * t
        S = F(abs(a) * abs(t - p) ** 3, 3)
        lo, hi = sorted((p, t))
        stem = f"放物線 $y={poly(*c)}$ と、その上の点 $({t},\\,{ft(ev(c, t))})$ における接線、および直線 $x={p}$ で囲まれた部分の面積を求めなさい。"
        steps = [f"$y'={poly(2 * a, -2 * a * p)}$ より接線は $y={line_tex(m, n)}$。",
                 f"放物線と接線の差は ${poly(*c)}-({line_tex(m, n)})={'' if a == 1 else ('-' if a == -1 else a)}{fac(t)}^2$。",
                 f"$S=\\displaystyle\\int_{{{lo}}}^{{{hi}}}{abs(a) if abs(a) != 1 else ''}{fac(t)}^2\\,dx=\\Bigl[\\dfrac{{{abs(a) if abs(a) != 1 else ''}{fac(t)}^3}}{{3}}\\Bigr]_{{{lo}}}^{{{hi}}}={ft(S)}$。"]
        chk = (f"Abs(integrate(({py(*c)})-(({fp(m)})*x+({fp(n)})), [x, {lo}, {hi}]))", fp(S))
        ap = "放物線と接線の差は、接点の $x$ 座標を $t$ として $a(x-t)^2$ の形になる。これを積分区間で積分する。"
        alt = ["$\\displaystyle\\int(x-t)^2\\,dx=\\dfrac{(x-t)^3}{3}+C$ を使うと展開せずに計算できる。展開して積分しても同じ値になる。"]
    else:
        t1, t2 = sorted(r.sample(range(-3, 4), 2))
        S = F(abs(a) * (t2 - t1) ** 3, 12)
        L1 = (2 * a * t1 - 2 * a * p, ev(c, t1) - (2 * a * t1 - 2 * a * p) * t1)
        L2 = (2 * a * t2 - 2 * a * p, ev(c, t2) - (2 * a * t2 - 2 * a * p) * t2)
        mid = F(t1 + t2, 2)
        stem = f"放物線 $y={poly(*c)}$ 上の2点 $({t1},\\,{ft(ev(c, t1))})$、$({t2},\\,{ft(ev(c, t2))})$ における接線をそれぞれ引く。放物線と2本の接線で囲まれた部分の面積を求めなさい。"
        steps = [f"接線は $y={line_tex(*L1)}$ と $y={line_tex(*L2)}$。", f"2本の接線の交点の $x$ 座標は $x={ft(mid)}$（接点の $x$ 座標の中点）。",
                 f"放物線と各接線の差は ${abs(a) if abs(a) != 1 else ''}{fac(t1)}^2$、${abs(a) if abs(a) != 1 else ''}{fac(t2)}^2$（符号は上下関係による）。",
                 f"$S=\\displaystyle\\int_{{{t1}}}^{{{ft(mid)}}}{abs(a) if abs(a) != 1 else ''}{fac(t1)}^2\\,dx+\\int_{{{ft(mid)}}}^{{{t2}}}{abs(a) if abs(a) != 1 else ''}{fac(t2)}^2\\,dx={ft(S)}$。"]
        chk = (f"Abs(integrate(({py(*c)})-(({fp(L1[0])})*x+({fp(L1[1])})), [x, {t1}, {fp(mid)}]))+Abs(integrate(({py(*c)})-(({fp(L2[0])})*x+({fp(L2[1])})), [x, {fp(mid)}, {t2}]))", fp(S))
        ap = "2本の接線の交点で積分区間を分ける。放物線と接線の差は $a(x-t)^2$ の形になるので、$\\dfrac{(x-t)^3}{3}$ を使って計算する。"
        alt = [f"結果は $\\dfrac{{|a|}}{{12}}(t_2-t_1)^3$ と表せる。$\\dfrac{{{abs(a)}}}{{12}}\\times({t2}-({t1}))^3={ft(S)}$ と一致することで検算できる。"]
    return desc(stem, f"${ft(S)}$", "放物線と接線の差は $a(x-t)^2$ の形になることを使う。", [("接線の方程式を正しく求めている", 2), ("積分区間と被積分関数を正しく設定している", 3), ("面積を正しく計算している", 3)],
                d=4, p=8, lines=10, ap=ap, steps=steps, alt=alt, pc=[("接線", 2), ("立式", 3), ("計算", 3)],
                pit=["接線と放物線の上下関係を逆にして負の値を出す。", "2本の接線の交点で区間を分けずに積分する。"], chk=chk)


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(stem, wrong, step, etype, tempt, fix, ans, expl, steps, ap, alt, pit, chk=None, d=3):
    return desc(f"{stem}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい答えを求めなさい。", ans, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい解答を途中式とともに示している", 3), ("最終的な答えが正しい", 1)], d=d, p=6, lines=6,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい途中式", 3), ("正しい答え", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix), chk=chk)


@gen("error_correction", 3, ["common_error", "computation"])
def err_tangent(r):
    while True:
        c = [r.choice([1, -1, 2]), r.randint(-3, 3), r.randint(-4, 4), r.randint(-4, 4)]
        t = nonzero(r, -2, 2)
        y0, m = ev(c, t), ev(dcoef(c), t)
        if y0 != m and m != 0:
            break
    n = y0 - m * t
    stem = f"曲線 $y={poly(*c)}$ 上の点 $({t},\\,{ft(y0)})$ における接線の方程式を求めなさい。"
    if r.random() < 0.5:
        wrong = f"$y'={poly(*dcoef(c))}$、$x={t}$ のとき $y'={ft(m)}$。よって接線は $y={line_tex(m, y0)}$"
        step, et = "直線の式 $y=mx+f(t)$ とした部分（$x$ 方向の平行移動を考えていない）", "formula"
        tempt = "「傾き $m$、点の $y$ 座標を切片」と思い込み、接点が $y$ 軸上にない場合にも $y=mx+f(t)$ としてしまう。"
    else:
        wrong = f"$x={t}$ のとき $y={ft(y0)}$ なので傾きは ${ft(y0)}$。よって $y-({ft(y0)})={ft(y0)}(x-({t}))$、$y={line_tex(y0, y0 - y0 * t)}$"
        step, et = "接線の傾きに関数の値 $f(t)$ を使った部分", "concept"
        tempt = "接線の傾きは「微分係数」であるのに、接点の $y$ 座標（関数の値）と混同している。"
    return err_item(stem, wrong, step, et, tempt, f"傾き $f'({t})={ft(m)}$、$y-({ft(y0)})={ft(m)}(x-({t}))$ より $y={line_tex(m, n)}$", f"$y={line_tex(m, n)}$",
                    "接線は点 $(t,\\,f(t))$ を通り傾き $f'(t)$ の直線：$y-f(t)=f'(t)(x-t)$。",
                    [f"$y'={poly(*dcoef(c))}$、$f'({t})={ft(m)}$。", f"$y-({ft(y0)})={ft(m)}(x-({t}))$。", f"$y={line_tex(m, n)}$。"],
                    "接線の公式 $y-f(t)=f'(t)(x-t)$ に、傾き（微分係数）と接点を正しく当てはめる。",
                    [f"答えの直線に $x={t}$ を代入すると $y={ft(y0)}$ となり、接点を通ることを確かめられる（生徒の直線は通らない、または傾きが違う）。"],
                    ["接点を通るかどうかの検算をしない。"],
                    chk=(f"[{py(*dcoef(c)).replace('x', f'({t})')}, {py(*c).replace('x', f'({t})')}-({fp(m)})*({t})]", f"[{fp(m)}, {fp(n)}]", None, "intermediate"))


@gen("error_correction", 3, ["common_error", "condition_check"])
def err_extreme(r):
    if r.random() < 0.5:
        p, d = r.randint(-3, 3), r.randint(-4, 4)
        k = r.choice([1, -1])
        c = [k, -3 * k * p, 3 * k * p * p, d]
        fp_ = ev(c, p)
        fd = f"{3 * k}{fac(p)}^2"
        fd_eq = poly(*dcoef(c)) if fd == poly(*dcoef(c)) else f"{poly(*dcoef(c))}={fd}"
        wrong = f"$f'(x)={fd_eq}$。$f'(x)=0$ より $x={p}$。よって $x={p}$ で極値 ${ft(fp_)}$ をとる"
        trend = "増加" if k > 0 else "減少"
        return err_item(f"関数 $f(x)={poly(*c)}$ の極値を調べなさい。", wrong, "$f'(x)=0$ となる点を、そのまま極値をとる点とした部分", "condition",
                        "「極値では $f'(x)=0$」を逆向きに使い、$f'(x)=0$ ならば極値と思い込んでいる。",
                        f"$f'(x)={3 * k}{fac(p)}^2$ は $x={p}$ の前後で符号が変わらない（常に $f'(x){'\\geqq' if k > 0 else '\\leqq'}0$）。$f(x)$ は常に{trend}し、極値をもたない",
                        "極値をもたない", f"$f'(x)$ の符号が $x={p}$ の前後で変わらないので、$x={p}$ は極値をとる点ではない。",
                        [f"$f'(x)={3 * k}{fac(p)}^2$。", f"$x<{p}$ でも $x>{p}$ でも $f'(x){'>' if k > 0 else '<'}0$。", f"$f(x)$ は常に{trend}し、極値はない。"],
                        "極値の判定は、$f'(x)=0$ の点の「前後の符号の変化」まで確かめる。",
                        [f"$f(x)={fac(p)}^3{'' if fp_ == 0 else ('+' if fp_ > 0 else '-') + ft(abs(fp_))}$ と変形でき、$y=x^3$ を平行移動したグラフと分かる。" if k > 0 else
                         f"$f(x)=-{fac(p)}^3{'' if fp_ == 0 else ('+' if fp_ > 0 else '-') + ft(abs(fp_))}$ と変形でき、$y=-x^3$ を平行移動したグラフと分かる。"],
                        ["増減表をかかずに $f'(x)=0$ の解だけで判断する。"],
                        chk=(f"expand(diff({py(*c)}, x))", f"{3 * k}*(x-({p}))**2", "expand", "intermediate"))
    while True:
        al, be = sorted(r.sample(range(-3, 4), 2))
        if (al + be) % 2 == 0:
            break
    c = [-1, F(3 * (al + be), 2), -3 * al * be, r.randint(-4, 4)]
    ci = [int(x) for x in c]
    fa, fb = ev(ci, al), ev(ci, be)
    wrong = f"$f'(x)=-3{fac(al)}{fac(be)}$ より、$x={al}$ で極大値 ${ft(fa)}$、$x={be}$ で極小値 ${ft(fb)}$"
    return err_item(f"関数 $f(x)={poly(*ci)}$ の極値を求めなさい。", wrong, "極大・極小の判定（$f'(x)$ の符号の調べ方）", "sign",
                    "$x^3$ の係数が正のときの「左が極大、右が極小」というパターンを、係数が負の場合にもそのまま当てはめている。",
                    f"$x<{al}$ で $f'(x)<0$、${al}<x<{be}$ で $f'(x)>0$、$x>{be}$ で $f'(x)<0$。よって $x={al}$ で極小値 ${ft(fa)}$、$x={be}$ で極大値 ${ft(fb)}$",
                    f"$x={be}$ で極大値 ${ft(fb)}$、$x={al}$ で極小値 ${ft(fa)}$", f"$f'(x)=-3{fac(al)}{fac(be)}$ は、${al}<x<{be}$ で正になる。",
                    [f"$f'(x)=-3{fac(al)}{fac(be)}$。", f"${al}<x<{be}$ で $f'(x)>0$、その外側で $f'(x)<0$。", f"$x={al}$ で極小値 ${ft(fa)}$、$x={be}$ で極大値 ${ft(fb)}$。"],
                    "増減表で $f'(x)$ の符号を実際に調べてから、極大・極小を判定する。",
                    [f"極大値は極小値より大きいはず：${ft(fb)}>{ft(fa)}$ であることからも、$x={be}$ が極大と確かめられる。"],
                    ["$x^3$ の係数の符号を確認しない。"],
                    chk=(f"[{py(*ci).replace('x', f'({be})')}, {py(*ci).replace('x', f'({al})')}]", f"[{fp(fb)}, {fp(fa)}]", None, "intermediate"))


@gen("error_correction", 2, ["common_error", "concept"])
def err_area_sign(r):
    al, be = sorted(r.sample(range(-3, 4), 2))
    c = [1, -(al + be), al * be]
    S = F((be - al) ** 3, 6)
    if r.random() < 0.5:
        wrong = f"$\\displaystyle\\int_{{{al}}}^{{{be}}}({poly(*c)})\\,dx=-\\dfrac{{1}}{{6}}({be}-({al}))^3={ft(-S)}$。よって面積は ${ft(-S)}$"
        return err_item(f"放物線 $y={poly(*c)}$ と $x$ 軸で囲まれた部分の面積を求めなさい。", wrong, "定積分の値をそのまま面積とした部分", "concept",
                        "「面積＝定積分」と覚えていて、グラフが $x$ 軸より下にあると定積分が負になることを考えていない。",
                        f"${al}\\leqq x\\leqq{be}$ で $y\\leqq0$ なので、面積は $-\\displaystyle\\int_{{{al}}}^{{{be}}}({poly(*c)})\\,dx={ft(S)}$", f"${ft(S)}$",
                        "面積は「上の関数－下の関数」の積分。$x$ 軸 $(y=0)$ が上にあるので $\\displaystyle\\int(0-f(x))\\,dx$。",
                        [f"交点は $x={al},\\ {be}$、その間で $y\\leqq0$。", f"$S=\\displaystyle\\int_{{{al}}}^{{{be}}}\\{{0-({poly(*c)})\\}}\\,dx$。", f"$=\\dfrac{{1}}{{6}}({be}-({al}))^3={ft(S)}$。"],
                        "面積は必ず正。定積分の値が負になったら、上下関係を見直す。", ["面積が負の値になることはないので、答えの符号で誤りに気づける。"],
                        ["上下関係を確かめずに積分する。"], chk=(f"-integrate({py(*c)}, [x, {al}, {be}])", fp(S)))
    lo, hi = al - r.randint(1, 2), be
    Fc = [F(1, 3), F(-(al + be), 2), al * be, 0]
    I1, I2 = ev(Fc, al) - ev(Fc, lo), ev(Fc, be) - ev(Fc, al)
    tot = abs(I1) + abs(I2)
    wrong = f"$\\displaystyle\\int_{{{lo}}}^{{{hi}}}({poly(*c)})\\,dx={ft(I1 + I2)}$。よって面積は ${ft(abs(I1 + I2))}$"
    return err_item(f"曲線 $y={poly(*c)}$ と $x$ 軸、および直線 $x={lo}$ で囲まれた部分と、曲線と $x$ 軸で囲まれた部分の面積の和を求めなさい。", wrong,
                    "区間を分けずに定積分を1回で計算した部分", "concept",
                    "$x$ 軸の上側と下側にまたがる区間で積分すると、正の部分と負の部分が打ち消し合うことに気づいていない。",
                    f"$x={al}$ で区間を分ける。$\\displaystyle\\int_{{{lo}}}^{{{al}}}={ft(I1)}$、$\\displaystyle\\int_{{{al}}}^{{{be}}}={ft(I2)}$ より、面積の和は ${ft(abs(I1))}+{ft(abs(I2))}={ft(tot)}$",
                    f"${ft(tot)}$", "グラフが $x$ 軸と交わる点で区間を分け、下にある部分は符号を変えて足す。",
                    [f"$x$ 軸との交点 $x={al},\\ {be}$ で区間を分ける。", f"$\\displaystyle\\int_{{{lo}}}^{{{al}}}({poly(*c)})\\,dx={ft(I1)}$（上）、$\\displaystyle\\int_{{{al}}}^{{{be}}}({poly(*c)})\\,dx={ft(I2)}$（下）。",
                     f"$S={ft(abs(I1))}+{ft(abs(I2))}={ft(tot)}$。"],
                    "定積分は「符号つきの面積」。面積を求めるときは、まずグラフをかいて $x$ 軸との上下を確認する。",
                    ["グラフの略図をかくと、$x$ 軸の下にある部分があることがすぐに分かる。"], ["交点で区間を分けない。"],
                    chk=(f"Abs(integrate({py(*c)}, [x, {lo}, {al}]))+Abs(integrate({py(*c)}, [x, {al}, {be}]))", fp(tot)))


@gen("error_correction", 2, ["common_error", "computation"])
def err_integral(r):
    while True:
        A, B, C = nonzero(r, -2, 2), nonzero(r, -3, 3), r.randint(-4, 4)
        lo = r.randint(-2, 1)
        hi = lo + r.randint(1, 3)
        Fc = [A, B, C, 0]
        v = ev(Fc, hi) - ev(Fc, lo)
        Wc = [F(3 * A, 2), F(2 * B, 1), C, 0]
        if v != 0 and ev(Wc, hi) - ev(Wc, lo) != v:
            break
    f = [3 * A, 2 * B, C]
    stem = f"定積分 $\\displaystyle\\int_{{{lo}}}^{{{hi}}}({poly(*f)})\\,dx$ を計算しなさい。"
    if r.random() < 0.5:
        wv = ev(Wc, hi) - ev(Wc, lo)
        wrong = f"$\\Bigl[{polyf(*Wc)}\\Bigr]_{{{lo}}}^{{{hi}}}={ft(wv)}$"
        step, et = "原始関数を求める部分（$x^n$ を $n$ で割っている）", "formula"
        tempt = "微分の公式 $(x^n)'=nx^{n-1}$ の「$n$」と混同し、$x^{n+1}$ を $n+1$ ではなく $n$ で割ってしまった。"
    else:
        wv = -v
        wrong = f"$\\Bigl[{poly(*Fc)}\\Bigr]_{{{lo}}}^{{{hi}}}=({ft(ev(Fc, lo))})-({ft(ev(Fc, hi))})={ft(wv)}$"
        step, et = "上端と下端の値を引く順序", "sign"
        tempt = "記号 $\\Bigl[F(x)\\Bigr]_a^b$ の下端 $a$ を先に書くので、$F(a)-F(b)$ と逆に引いてしまう。"
    return err_item(stem, wrong, step, et, tempt,
                    f"$\\Bigl[{poly(*Fc)}\\Bigr]_{{{lo}}}^{{{hi}}}=({ft(ev(Fc, hi))})-({ft(ev(Fc, lo))})={ft(v)}$", f"${ft(v)}$",
                    "$\\displaystyle\\int x^n\\,dx=\\dfrac{x^{n+1}}{n+1}+C$、$\\displaystyle\\int_a^bf(x)\\,dx=F(b)-F(a)$。",
                    [f"原始関数は $F(x)={poly(*Fc)}$。", f"$F({hi})={ft(ev(Fc, hi))}$、$F({lo})={ft(ev(Fc, lo))}$。", f"$F({hi})-F({lo})={ft(v)}$。"],
                    "原始関数は微分して確かめ、定積分は「上端の値－下端の値」の順で計算する。",
                    [f"原始関数 $F(x)={poly(*Fc)}$ を微分すると ${poly(*f)}$ に戻ることを確かめる。"], ["原始関数を微分して検算しない。"],
                    chk=(f"integrate({py(*f)}, [x, {lo}, {hi}])", fp(v)))


GENERATORS = [deriv_value, by_definition, indefinite, definite, extremum_judge,
              tangent, extrema, interval_maxmin, area_two, area_axis,
              param_extreme, tangent_from_point, box_volume, area_tangent,
              err_tangent, err_extreme, err_area_sign, err_integral]
