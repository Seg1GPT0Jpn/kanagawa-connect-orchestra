"""単元パック：数学Ⅲ 微分法とその応用（積・商・合成関数・逆関数の微分、三角・指数・対数関数の導関数、接線・法線、グラフの概形、速度・加速度）。"""
import math
from fractions import Fraction as F

import sympy as sp

from banks._common import desc, figure, mc, plane, sa
from hs_pack_lib import board, check, definition, derivation, example, gen, guide, intro, lesson, nonzero, summary, theorem, tp

UNIT_ID = "HS-MATH3-U02"

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


def TX(e):
    """sympy 式の LaTeX（\\frac → \\dfrac）。"""
    s = sp.latex(sp.nsimplify(e) if not isinstance(e, sp.Basic) else e).replace("\\frac", "\\dfrac")
    return "\\dfrac{1}{e}" if s == "e^{-1}" else ("-\\dfrac{1}{e}" if s == "- e^{-1}" else s)


def rlin(a, b, var="x"):
    """ax+b の LaTeX。a<0<b のときは b-|a|x の順に書く。"""
    if a < 0 < b:
        return f"{b}-{cf(-a)}{var}"
    return lin(a, b, var)


def cf(c):
    return "" if c == 1 else ("-" if c == -1 else str(c))


def tf_(c):
    return "" if c == 0 else (f"+{c}" if c > 0 else f"{c}")


def lin(a, b, var="x"):
    """ax+b の LaTeX。"""
    return f"{cf(a)}{var}{tf_(b)}"


def LIM(var="x", to="\\infty"):
    return f"\\displaystyle\\lim_{{{var}\\to {to}}}"


def line_tex(m, n):
    """y=mx+n の右辺（m, n は sympy）。"""
    m, n = sp.nsimplify(m), sp.nsimplify(n)
    if m == 0:
        head = ""
    elif m == 1:
        head = "x"
    elif m == -1:
        head = "-x"
    elif isinstance(m, sp.Add):
        head = f"\\left({TX(m)}\\right)x"
    else:
        head = f"{TX(m)}x"
    if n == 0:
        return head or "0"
    s = TX(n)
    if not head:
        return s
    if s.startswith("-"):
        return head + s
    return head + "+" + s


def pyx(s):
    """テンプレート中の X を x に。"""
    return s.replace("X", "x")


def at(s, v):
    """テンプレート中の X を値 v に置きかえた sympy 式の文字列。"""
    return s.replace("X", f"({v})")


PI_ANG = {2: sp.pi / 2, 3: sp.pi / 3, 4: sp.pi / 4, 6: sp.pi / 6}


LESSON = lesson(
    goals=["積・商・合成関数・逆関数の微分法を導き、三角関数・指数関数・対数関数を含むさまざまな関数を微分できる。",
           "接線・法線の方程式を求め、第1次・第2次導関数を用いて増減・極値・凹凸・漸近線を調べ、グラフの概形をかける。",
           "微分法を方程式・不等式、最大・最小の問題、直線上や平面上の点の速度・加速度に応用できる。"],
    duration=200,
    readiness=["関数の極限、特に $\\displaystyle\\lim_{x\\to0}\\dfrac{\\sin x}{x}=1$ と、片側極限・$x\\to\\pm\\infty$ の極限（数学Ⅲ 極限）を使える。",
               "多項式関数の微分、接線の方程式、増減表（数学Ⅱ）をかける。", "指数・対数の性質（数学Ⅱ）と三角関数の加法定理（数学Ⅱ）を使える。"],
    flow=[("導入：微分できる関数を広げる", 10, "数学Ⅱの微分の公式が使えない関数（$\\sqrt{x}$、$\\sin x$、$e^x$）を示し、本単元の目標を確認する"),
          ("積・商・合成関数・逆関数の微分", 40, "積の微分法の証明、商と合成関数の微分法、逆関数の微分法と $x^r$ の導関数（例題1）"),
          ("三角・指数・対数関数の導関数", 35, "$(\\sin x)'=\\cos x$ の導出、$e$ の定義と $(\\log x)'=\\dfrac{1}{x}$、$(e^x)'=e^x$"),
          ("接線・法線と平均値の定理", 25, "接線・法線の方程式（例題2）、平均値の定理の意味"),
          ("グラフの概形", 45, "第2次導関数と凹凸・変曲点、漸近線、$y=xe^{-x}$ のグラフ（例題3）"),
          ("速度・加速度と応用", 30, "直線上・平面上の運動（例題4）、方程式・不等式への応用"),
          ("まとめ", 15, "公式の整理、確認問題、問題プリントの課題指示")],
    sections=[
        intro("in1", "どんな関数でも微分できるようにする",
              "数学Ⅱでは多項式関数を微分した。しかし、振り子の運動は三角関数で、放射性物質の量の変化は指数関数で表される。こうした関数の変化の割合を調べるには、$\\sin x$、$e^x$、$\\log x$ などの導関数と、関数を組み合わせたもの（積・商・合成）を微分する方法が必要になる。この単元では、導関数の定義 $f'(x)=\\displaystyle\\lim_{h\\to0}\\dfrac{f(x+h)-f(x)}{h}$ に立ち返って公式を導き、グラフの概形や運動の解析に応用する。",
              bullets=["積・商・合成関数・逆関数の微分法を身につければ、初等関数はすべて微分できる。", "第2次導関数はグラフの曲がり方（凹凸）を表し、物理では加速度を表す。"],
              points=[tp("$y=\\sqrt{x}$ の導関数を定義から求めさせ（分子の有理化）、毎回定義に戻るのは大変なので公式が必要だと実感させる。",
                         ask="$(\\sqrt{x})'$ は数学Ⅱの公式 $(x^n)'=nx^{n-1}$ で求めてよいか。", expect="$n$ が正の整数でないので、まだ使えるとは言えない。", timing="導入の冒頭")]),
        theorem("th1", "積・商・合成関数・逆関数の微分法",
                "$$\\{f(x)g(x)\\}'=f'(x)g(x)+f(x)g'(x),\\qquad \\left\\{\\dfrac{f(x)}{g(x)}\\right\\}'=\\dfrac{f'(x)g(x)-f(x)g'(x)}{\\{g(x)\\}^2},\\qquad \\dfrac{dy}{dx}=\\dfrac{dy}{du}\\cdot\\dfrac{du}{dx}$$",
                ["合成関数 $y=f(g(x))$ は $u=g(x)$ とおくと $y'=f'(g(x))\\,g'(x)$。中身の導関数 $g'(x)$ をかけ忘れないこと。",
                 "逆関数の微分法：$\\dfrac{dy}{dx}=\\dfrac{1}{\\dfrac{dx}{dy}}$（$\\dfrac{dx}{dy}\\neq0$）。",
                 "$r$ が有理数のとき $(x^r)'=rx^{r-1}$（$x>0$）。たとえば $(\\sqrt{x})'=\\dfrac{1}{2\\sqrt{x}}$。",
                 "媒介変数表示 $x=f(t),\\ y=g(t)$ のとき $\\dfrac{dy}{dx}=\\dfrac{g'(t)}{f'(t)}$（$f'(t)\\neq0$）。"],
                proof=["積：$f(x+h)g(x+h)-f(x)g(x)=\\{f(x+h)-f(x)\\}g(x+h)+f(x)\\{g(x+h)-g(x)\\}$ と変形する。",
                       "両辺を $h$ で割って $h\\to0$ とする。$g(x)$ は微分可能なので連続であり $g(x+h)\\to g(x)$。よって $\\{f(x)g(x)\\}'=f'(x)g(x)+f(x)g'(x)$。",
                       "商：まず $\\left\\{\\dfrac{1}{g(x)}\\right\\}'=\\displaystyle\\lim_{h\\to0}\\dfrac{1}{h}\\cdot\\dfrac{g(x)-g(x+h)}{g(x+h)g(x)}=-\\dfrac{g'(x)}{\\{g(x)\\}^2}$ を示し、$\\dfrac{f}{g}=f\\cdot\\dfrac{1}{g}$ に積の微分法を用いる。",
                       "合成関数：$\\Delta u=g(x+h)-g(x)$ とすると、$\\Delta u\\neq0$ のとき $\\dfrac{\\Delta y}{h}=\\dfrac{\\Delta y}{\\Delta u}\\cdot\\dfrac{\\Delta u}{h}$。$h\\to0$ のとき $\\Delta u\\to0$ なので $\\dfrac{dy}{dx}=\\dfrac{dy}{du}\\cdot\\dfrac{du}{dx}$。"],
                points=[tp("積の微分法の証明で「$f(x)g(x+h)$ を引いて加える」工夫がどこから来るかを、長方形の面積の増加分の図で説明する。",
                           ask="縦 $f$、横 $g$ の長方形で、両方が少し増えたとき面積の増加分はどんな部分からなるか。", expect="縦の増加分×横、縦×横の増加分、（小さい）増加分どうしの積。"),
                        tp("合成関数の微分では「外側を微分 × 中身を微分」と唱えさせ、$(\\sin 3x)'=3\\cos 3x$ のように中身の微分を必ず書かせる。", caution="中身の微分をかけ忘れる誤りが最も多い。", timing="合成関数の導入時")]),
        derivation("dv1", "三角関数・指数関数・対数関数の導関数",
                   ["$\\sin(x+h)-\\sin x=2\\cos\\left(x+\\dfrac{h}{2}\\right)\\sin\\dfrac{h}{2}$（和積の公式、または加法定理から導く）。",
                    "$\\dfrac{\\sin(x+h)-\\sin x}{h}=\\cos\\left(x+\\dfrac{h}{2}\\right)\\cdot\\dfrac{\\sin\\frac{h}{2}}{\\frac{h}{2}}\\to\\cos x\\cdot1$。よって $(\\sin x)'=\\cos x$。同様に $(\\cos x)'=-\\sin x$、商の微分法から $(\\tan x)'=\\dfrac{1}{\\cos^2x}$。",
                    "$\\displaystyle e=\\lim_{h\\to0}(1+h)^{\\frac{1}{h}}=2.71828\\cdots$ と定める。$e$ を底とする対数を自然対数といい、$\\log x$ と書く。",
                    "$\\dfrac{\\log(x+h)-\\log x}{h}=\\dfrac{1}{x}\\log\\left(1+\\dfrac{h}{x}\\right)^{\\frac{x}{h}}$。$k=\\dfrac{h}{x}$ とおくと $h\\to0$ で $k\\to0$、$(1+k)^{\\frac{1}{k}}\\to e$ なので $(\\log x)'=\\dfrac{1}{x}\\log e=\\dfrac{1}{x}$。",
                    "$y=e^x$ は $x=\\log y$ の逆関数なので $\\dfrac{dy}{dx}=\\dfrac{1}{\\frac{1}{y}}=y=e^x$。また $(a^x)'=a^x\\log a$、$(\\log|x|)'=\\dfrac{1}{x}$、$(\\log_ax)'=\\dfrac{1}{x\\log a}$。"],
                   body="$e$ は「$x=0$ における接線の傾きが $1$ になる指数関数 $y=a^x$ の底」と言いかえることもできる。数学Ⅲでは、断りがなければ $\\log$ は自然対数を表す。",
                   points=[tp("$(\\sin x)'=\\cos x$ の導出で $\\displaystyle\\lim_{\\theta\\to0}\\dfrac{\\sin\\theta}{\\theta}=1$ が使われていることを確認し、弧度法でなければ公式が変わることに触れる。"),
                           tp("$(a^x)'=a^x\\log a$ を $(a^x)'=xa^{x-1}$ と混同する生徒が多いので、「指数に変数がある関数」と「底に変数がある関数」を対比させる。",
                              caution="$(2^x)'=x\\cdot2^{x-1}$ は誤り。", ask="$y=2^x$ と $y=x^2$ の違いは？", expect="変数が指数にあるか底にあるか。")]),
        example("ex1", "例題1　いろいろな関数の微分",
                "次の関数を微分せよ。(1) $y=\\sin^3 2x$　(2) $y=\\log(x^2+1)$　(3) $y=xe^{-x}$",
                ["(1) $u=\\sin 2x$ とおくと $y=u^3$。$y'=3u^2\\cdot u'=3\\sin^2 2x\\cdot2\\cos 2x=6\\sin^2 2x\\cos 2x$。",
                 "(2) $y'=\\dfrac{(x^2+1)'}{x^2+1}=\\dfrac{2x}{x^2+1}$。",
                 "(3) 積の微分法と $(e^{-x})'=-e^{-x}$ より $y'=e^{-x}+x\\cdot(-e^{-x})=(1-x)e^{-x}$。"],
                "(1) $y'=6\\sin^2 2x\\cos 2x$　(2) $y'=\\dfrac{2x}{x^2+1}$　(3) $y'=(1-x)e^{-x}$",
                thinking="関数の「つくり」を見抜く。(1) は3重の合成（3乗・$\\sin$・$2x$）、(2) は $\\log$ と2次式の合成、(3) は積。",
                points=[tp("(1) で「外側から順に」微分する様子を、矢印で $3u^2\\to\\cos 2x\\to2$ と板書して見せる。")],
                misconceptions=[("(1) を $3\\sin^2 2x\\cos 2x$ とする", "中身 $2x$ の微分 $2$ もかける"), ("(2) を $\\dfrac{1}{x^2+1}$ とする", "$\\{\\log g(x)\\}'=\\dfrac{g'(x)}{g(x)}$")]),
        theorem("th2", "接線・法線と平均値の定理",
                "$$\\text{接線}\\ y-f(a)=f'(a)(x-a),\\qquad \\text{法線}\\ y-f(a)=-\\dfrac{1}{f'(a)}(x-a)\\ \\ (f'(a)\\neq0)$$",
                ["法線は接点を通り接線に垂直な直線。$f'(a)=0$ のときの法線は $x=a$。",
                 "平均値の定理：$f(x)$ が $a\\leqq x\\leqq b$ で連続、$a<x<b$ で微分可能ならば、$\\dfrac{f(b)-f(a)}{b-a}=f'(c)$、$a<c<b$ を満たす $c$ が存在する。",
                 "平均値の定理から、ある区間でつねに $f'(x)>0$ ならば $f(x)$ はその区間で増加することが示される。"],
                proof=["2直線が垂直 $\\iff$ 傾きの積が $-1$。接線の傾きが $f'(a)$ なので、法線の傾きは $-\\dfrac{1}{f'(a)}$。",
                       "平均値の定理の意味：2点 $(a,\\,f(a)),\\ (b,\\,f(b))$ を結ぶ直線と平行な接線が、その間のどこかで引ける。",
                       "増加の証明：$x_1<x_2$ とすると平均値の定理より $f(x_2)-f(x_1)=(x_2-x_1)f'(c)>0$。"],
                points=[tp("法線の傾きを $-f'(a)$ とする誤りが多いので、「垂直 $\\iff$ 傾きの積 $-1$」を毎回確認させる。", caution="傾きの符号だけ変えて逆数にし忘れる。")]),
        example("ex2", "例題2　接線と法線",
                "曲線 $y=\\log x$ 上の点 $(e,\\,1)$ における接線と法線の方程式を求めよ。",
                ["$y'=\\dfrac{1}{x}$ より、接線の傾きは $\\dfrac{1}{e}$。", "接線：$y-1=\\dfrac{1}{e}(x-e)$ より $y=\\dfrac{1}{e}x$。",
                 "法線の傾きは $-e$。法線：$y-1=-e(x-e)$ より $y=-ex+e^2+1$。"],
                "接線 $y=\\dfrac{1}{e}x$、法線 $y=-ex+e^2+1$",
                thinking="導関数から接線の傾きを求め、法線は傾きの積が $-1$ になる直線として求める。",
                points=[tp("接線が原点を通ることに気づかせ、「原点から $y=\\log x$ に引いた接線」の問題と結びつける。")]),
        definition("df1", "第2次導関数とグラフの凹凸",
                   "導関数 $f'(x)$ の導関数を第2次導関数といい $f''(x)$ で表す。ある区間で $f''(x)>0$ ならば曲線 $y=f(x)$ はその区間で下に凸、$f''(x)<0$ ならば上に凸である。凹凸が入れかわる境目の点を変曲点という。",
                   formula="$$f''(x)>0\\Rightarrow\\text{下に凸},\\qquad f''(x)<0\\Rightarrow\\text{上に凸},\\qquad f''(a)=0\\ \\text{かつ前後で符号が変わる}\\Rightarrow(a,\\,f(a))\\ \\text{は変曲点}$$",
                   conditions=["$f''(a)=0$ でも前後で $f''(x)$ の符号が変わらなければ変曲点ではない（例：$y=x^4$ の原点）。",
                               "$f'(a)=0,\\ f''(a)<0$ ならば $f(a)$ は極大値、$f'(a)=0,\\ f''(a)>0$ ならば極小値（第2次導関数による判定）。",
                               "漸近線：$\\displaystyle\\lim_{x\\to a\\pm0}f(x)=\\pm\\infty$ なら直線 $x=a$、$\\displaystyle\\lim_{x\\to\\pm\\infty}\\{f(x)-(mx+n)\\}=0$ なら直線 $y=mx+n$ が漸近線。"],
                   points=[tp("$f''(x)$ は「接線の傾きの増減」を表すことを、下に凸のグラフ上で接線を左から右へ動かして見せる。", ask="下に凸のグラフで、接線の傾きは右へ行くほどどうなるか。", expect="大きくなる（増加する）。")]),
        example("ex3", "例題3　グラフの概形",
                "関数 $y=xe^{-x}$ の増減、極値、グラフの凹凸、変曲点を調べ、グラフの概形をかけ。ただし $\\displaystyle\\lim_{x\\to\\infty}xe^{-x}=0$ を用いてよい。",
                ["$y'=(1-x)e^{-x}$、$y''=(x-2)e^{-x}$。", "$y'=0$ より $x=1$。$x<1$ で増加、$x>1$ で減少し、$x=1$ で極大値 $\\dfrac{1}{e}$。",
                 "$y''=0$ より $x=2$。$x<2$ で上に凸、$x>2$ で下に凸。変曲点は $\\left(2,\\,\\dfrac{2}{e^2}\\right)$。",
                 "$x\\to\\infty$ で $y\\to0$（$x$ 軸が漸近線）、$x\\to-\\infty$ で $y\\to-\\infty$。"],
                "$x=1$ で極大値 $\\dfrac{1}{e}$、変曲点 $\\left(2,\\,\\dfrac{2}{e^2}\\right)$、漸近線 $y=0$（図）",
                thinking="$y'$ と $y''$ の符号を1つの表（増減表）にまとめ、極限で両端のようすを調べる。",
                figure=figure("y=xe^{-x} のグラフ（x=1 で極大、x=2 に変曲点）", plane((-1, 6), (-2, 1), unit=30, curves=[(lambda x: x * math.exp(-x), "")],
                                                                          points=[(1, math.exp(-1), "極大"), (2, 2 * math.exp(-2), "変曲点")])),
                points=[tp("増減表に $y''$ の行を加え、矢印を「曲がった矢印」（4種類）でかく方法を示す。", timing="例題3の増減表をかく場面")]),
        definition("df2", "速度・加速度",
                   "数直線上を動く点 P の時刻 $t$ における座標が $x=f(t)$ のとき、速度 $v=\\dfrac{dx}{dt}$、加速度 $\\alpha=\\dfrac{dv}{dt}=\\dfrac{d^2x}{dt^2}$ である。平面上を動く点 $(x,\\,y)$ では、速度は $\\vec{v}=\\left(\\dfrac{dx}{dt},\\,\\dfrac{dy}{dt}\\right)$、速さは $|\\vec{v}|=\\sqrt{\\left(\\dfrac{dx}{dt}\\right)^2+\\left(\\dfrac{dy}{dt}\\right)^2}$、加速度は $\\vec{\\alpha}=\\left(\\dfrac{d^2x}{dt^2},\\,\\dfrac{d^2y}{dt^2}\\right)$ である。",
                   formula="$$v=\\dfrac{dx}{dt},\\qquad \\alpha=\\dfrac{d^2x}{dt^2},\\qquad |\\vec{v}|=\\sqrt{\\left(\\dfrac{dx}{dt}\\right)^2+\\left(\\dfrac{dy}{dt}\\right)^2}$$",
                   conditions=["速度は向きを含む量（数直線上では符号つき）、速さはその大きさ $|v|$。", "$x=A\\sin\\omega t$ のとき $\\dfrac{d^2x}{dt^2}=-\\omega^2x$ となり、物理の単振動の式と一致する。"],
                   points=[tp("物理で学ぶ等加速度直線運動 $x=v_0t+\\dfrac{1}{2}at^2$ を微分して $v=v_0+at$ になることを確かめ、教科の間のつながりを示す。")]),
        example("ex4", "例題4　平面上の運動",
                "座標平面上を動く点 P の時刻 $t$ における座標が $x=3\\cos 2t,\\ y=3\\sin 2t$ のとき、P の速さと加速度の大きさを求めよ。",
                ["$\\dfrac{dx}{dt}=-6\\sin 2t,\\ \\dfrac{dy}{dt}=6\\cos 2t$。", "速さは $\\sqrt{36\\sin^2 2t+36\\cos^2 2t}=6$。",
                 "$\\dfrac{d^2x}{dt^2}=-12\\cos 2t,\\ \\dfrac{d^2y}{dt^2}=-12\\sin 2t$ より、加速度の大きさは $12$。"],
                "速さ $6$、加速度の大きさ $12$",
                thinking="成分ごとに微分してから大きさを求める。$\\sin^2+\\cos^2=1$ で $t$ が消える。",
                points=[tp("加速度ベクトルが $-4\\overrightarrow{\\mathrm{OP}}$ となり、つねに中心を向くこと（向心加速度）を確認し、物理の等速円運動と結びつける。")]),
        board("bd1", "板書案",
              [("① 微分法の公式", ["$(fg)'=f'g+fg'$", "$\\left(\\dfrac{f}{g}\\right)'=\\dfrac{f'g-fg'}{g^2}$", "$\\{f(g(x))\\}'=f'(g(x))g'(x)$", "$(\\sin x)'=\\cos x,\\ (e^x)'=e^x,\\ (\\log x)'=\\dfrac{1}{x}$"]),
               ("② 接線・グラフ", ["接線 $y-f(a)=f'(a)(x-a)$", "法線の傾き $-\\dfrac{1}{f'(a)}$", "$f''>0$ 下に凸／$f''<0$ 上に凸", "例3 $y=xe^{-x}$：極大 $\\dfrac{1}{e}$、変曲点 $x=2$"]),
               ("③ 応用", ["$v=\\dfrac{dx}{dt},\\ \\alpha=\\dfrac{d^2x}{dt^2}$", "速さ $\\sqrt{\\dot{x}^2+\\dot{y}^2}$", "例4 速さ $6$、加速度 $12$", "不等式 → 差の関数の増減"])],
              points=[tp("①の4行目は、導出（$\\sin$ は極限、$\\log$ は $e$ の定義、$e^x$ は逆関数）の矢印を添えて書き、公式の出どころを残す。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("微分する前に関数の「つくり」（和・積・商・合成）を言わせてから計算に入ると、公式の選び間違いが減る。", ask="$y=e^{-x^2}$ はどんなつくりの関数か。", expect="$e^u$ と $u=-x^2$ の合成。"),
               tp("グラフの概形では、増減表の $y'$・$y''$ の符号、極限（両端・漸近線）、座標軸との交点の3点を必ずそろえさせる。", timing="例題3の後"),
               tp("不等式の証明は「差をとった関数の最小値が $0$ 以上」と方針を立てさせ、$f(0)=0$ と単調性を組み合わせる型も示す。"),
               tp("速度と速さの違い（符号・向きの有無）を物理の用語と対応させて説明する。", caution="平面上の速さを $\\dfrac{dx}{dt}+\\dfrac{dy}{dt}$ とする誤りがある。"),
               tp("$\\log$ の真数条件と、$\\log|x|$ の微分を対で扱い、定義域を意識させる。")],
              misconceptions=[("$(\\sin 3x)'=\\cos 3x$", "中身の微分をかけて $3\\cos 3x$"), ("$(2^x)'=x\\cdot2^{x-1}$", "$(a^x)'=a^x\\log a$ なので $2^x\\log 2$"),
                              ("$f''(a)=0$ ならば $(a,\\,f(a))$ は変曲点", "前後で $f''(x)$ の符号が変わるときに限る")]),
        summary("sm1", "まとめ",
                ["積・商・合成関数・逆関数の微分法で、三角・指数・対数関数を含む関数はすべて微分できる。",
                 "$(\\sin x)'=\\cos x$、$(\\cos x)'=-\\sin x$、$(\\tan x)'=\\dfrac{1}{\\cos^2x}$、$(e^x)'=e^x$、$(\\log|x|)'=\\dfrac{1}{x}$、$(a^x)'=a^x\\log a$。",
                 "接線は傾き $f'(a)$、法線は傾き $-\\dfrac{1}{f'(a)}$。$f'$ で増減、$f''$ で凹凸を調べてグラフをかく。速度は $\\dfrac{dx}{dt}$、加速度は $\\dfrac{d^2x}{dt^2}$。"]),
        check("ck1", "確認問題",
              [("$y=e^{3x}\\sin x$ を微分せよ。", "$y'=e^{3x}(3\\sin x+\\cos x)$"), ("$y=\\tan^2x$ を微分せよ。", "$y'=2\\tan x\\cdot\\dfrac{1}{\\cos^2x}=\\dfrac{2\\sin x}{\\cos^3x}$"),
               ("曲線 $y=e^x$ 上の点 $(0,\\,1)$ における法線の方程式は？", "接線の傾き $1$ より法線の傾き $-1$、$y=-x+1$")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

def power_family(k):
    """(f の LaTeX, f' の LaTeX, f の式, f' の式)。"""
    return [
        (f"{cf(k)}\\sqrt{{x}}", f"\\dfrac{{{k}}}{{2\\sqrt{{x}}}}", f"{k}*sqrt(x)", f"{k}/(2*sqrt(x))"),
        (f"{cf(k)}x\\sqrt{{x}}", f"{ft(F(3 * k, 2))}\\sqrt{{x}}", f"{k}*x*sqrt(x)", f"Rational({3 * k},2)*sqrt(x)"),
        (f"\\dfrac{{{k}}}{{x}}", f"-\\dfrac{{{k}}}{{x^2}}", f"{k}/x", f"-{k}/x**2"),
        (f"\\dfrac{{{k}}}{{x^2}}", f"-\\dfrac{{{2 * k}}}{{x^3}}", f"{k}/x**2", f"-{2 * k}/x**3"),
        (f"{cf(k)}\\sqrt[3]{{x}}", f"\\dfrac{{{k}}}{{3\\sqrt[3]{{x^2}}}}", f"{k}*x**Rational(1,3)", f"{k}/(3*x**Rational(2,3))"),
        (f"{cf(k)}\\sqrt[3]{{x^2}}", f"\\dfrac{{{2 * k}}}{{3\\sqrt[3]{{x}}}}", f"{k}*x**Rational(2,3)", f"{2 * k}/(3*x**Rational(1,3))"),
        (f"\\dfrac{{{k}}}{{\\sqrt{{x}}}}", f"-\\dfrac{{{k}}}{{2x\\sqrt{{x}}}}", f"{k}/sqrt(x)", f"-{k}/(2*x*sqrt(x))"),
    ]


@gen("basic_check", 5, ["computation"])
def deriv_basic(r):
    kind = r.choice(["power", "power", "trig", "exp", "log"])
    if kind == "power":
        k = r.randint(1, 6)
        ftex, dtex, fpy, dpy = r.choice(power_family(k))
        why = "$x^r$ の形に直して $(x^r)'=rx^{r-1}$ を使う（$r$ は有理数）。"
        steps = ["根号・分数を $x^r$ の形（$\\sqrt{x}=x^{\\frac{1}{2}},\\ \\dfrac{1}{x^2}=x^{-2}$ など）に直す。", "$(x^r)'=rx^{r-1}$ を用いる。", f"もとの形に戻して $y'={dtex}$。"]
        pit = ["$\\sqrt{x}$ を $x^{\\frac{1}{2}}$ に直さず、公式が使えないと思い込む。", "負の指数の計算で $r-1$ を誤る（$x^{-2}$ の微分を $-2x^{-1}$ とするなど）。"]
    elif kind == "trig":
        a, b = r.randint(1, 5), r.randint(-3, 3)
        arg = lin(a, b)
        g = r.choice(["sin", "cos", "tan"])
        A = f"({arg})" if b != 0 else arg
        if g == "sin":
            ftex, dtex, fpy, dpy = f"\\sin {A}", f"{cf(a)}\\cos {A}", f"sin({a}*x+({b}))", f"{a}*cos({a}*x+({b}))"
        elif g == "cos":
            ftex, dtex, fpy, dpy = f"\\cos {A}", f"-{cf(a)}\\sin {A}", f"cos({a}*x+({b}))", f"-{a}*sin({a}*x+({b}))"
        else:
            ftex, dtex, fpy, dpy = f"\\tan {A}", f"\\dfrac{{{a}}}{{\\cos^2 {A}}}", f"tan({a}*x+({b}))", f"{a}/cos({a}*x+({b}))**2"
        why = f"三角関数の導関数と合成関数の微分法（中身 ${arg}$ の微分 ${a}$ をかける）。"
        steps = [f"$u={arg}$ とおくと $u'={a}$。", f"$(\\{g} u)'$ の公式に当てはめ、$u'$ をかける。", f"$y'={dtex}$。"]
        pit = ["中身の微分 $" + str(a) + "$ をかけ忘れる。", "$(\\cos x)'=\\sin x$ と符号を誤る。"]
    elif kind == "exp":
        if r.random() < 0.5:
            a, b = nonzero(r, -4, 4), r.randint(-3, 3)
            arg = lin(a, b)
            ftex, dtex, fpy, dpy = f"e^{{{arg}}}", f"{cf(a)}e^{{{arg}}}", f"exp({a}*x+({b}))", f"{a}*exp({a}*x+({b}))"
            why = "$(e^x)'=e^x$ と合成関数の微分法。"
            steps = [f"$u={arg}$ とおくと $(e^u)'=e^u\\cdot u'$。", f"$u'={a}$。", f"$y'={dtex}$。"]
        else:
            c, k = r.choice([2, 3, 5, 10]), r.randint(1, 5)
            ftex, dtex, fpy, dpy = f"{cf(k)}\\cdot {c}^x" if k != 1 else f"{c}^x", (f"{c}^x\\log {c}" if k == 1 else f"{k}\\cdot {c}^x\\log {c}"), f"{k}*{c}**x", f"{k}*{c}**x*log({c})"
            ftex = ftex.replace("\\cdot ", "") if k == 1 else ftex
            why = "$(a^x)'=a^x\\log a$。"
            steps = [f"$(a^x)'=a^x\\log a$ に $a={c}$ を当てはめる。", f"$y'={dtex}$。"]
        pit = ["$(a^x)'=xa^{x-1}$ と、$x^n$ の公式と混同する。", "指数の中身の微分をかけ忘れる。"]
    else:
        if r.random() < 0.6:
            a, b = r.randint(1, 5), r.randint(-4, 6)
            arg = lin(a, b)
            ftex, dtex, fpy, dpy = f"\\log({arg})", f"\\dfrac{{{a}}}{{{arg}}}", f"log({a}*x+({b}))", f"{a}/({a}*x+({b}))"
            why = "$\\{\\log g(x)\\}'=\\dfrac{g'(x)}{g(x)}$。"
            steps = [f"$u={arg}$ とおくと $(\\log u)'=\\dfrac{{u'}}{{u}}$。", f"$u'={a}$ より $y'={dtex}$。"]
        else:
            c = r.choice([2, 3, 5, 10])
            k = r.randint(1, 4)
            ftex, dtex, fpy, dpy = f"{cf(k)}\\log_{{{c}}}x", f"\\dfrac{{{k}}}{{x\\log {c}}}", f"{k}*log(x)/log({c})", f"{k}/(x*log({c}))"
            why = "底の変換 $\\log_ax=\\dfrac{\\log x}{\\log a}$ より $(\\log_ax)'=\\dfrac{1}{x\\log a}$。"
            steps = [f"底の変換で $\\log_{{{c}}}x=\\dfrac{{\\log x}}{{\\log {c}}}$。", "$\\log {c}$ は定数なので、$(\\log x)'=\\dfrac{1}{x}$ を用いる。".replace("{c}", str(c)), f"$y'={dtex}$。"]
        pit = ["$\\{\\log(ax+b)\\}'$ を $\\dfrac{1}{ax+b}$ として、中身の微分を落とす。", "底が $e$ でない対数で $\\log a$ を落とす。"]
    return sa(f"関数 $y={ftex}$ を微分しなさい。", f"$y'={dtex}$", why, d=2,
              ap="基本の導関数（$x^r$、三角関数、指数関数、対数関数）のどれにあたるかを見分け、中身があれば合成関数の微分法を使う。",
              steps=steps, alt=["定義 $\\displaystyle\\lim_{h\\to0}\\dfrac{f(x+h)-f(x)}{h}$ に戻って確かめることもできる。また、$x=1$ など具体的な値で、$\\dfrac{f(1.001)-f(1)}{0.001}$ を電卓で求めて近い値になるかを調べられる。"],
              pc=[("用いる公式が正しい", 1), ("導関数が正しい", 1)], pit=pit,
              chk=(f"simplify(diff({fpy}, x)-({dpy}))", "0"))


@gen("basic_check", 4, ["computation"])
def chain_rule(r):
    kind = r.choice(["lin_pow", "quad_pow", "sqrt_quad", "sqrt_lin", "exp_quad", "log_quad", "sin_pow", "recip"])
    if kind == "lin_pow":
        a, b, n = nonzero(r, -4, 4), nonzero(r, -5, 5), r.randint(3, 7)
        ftex, dtex = f"({lin(a, b)})^{n}", f"{n * a}({lin(a, b)})^{{{n - 1}}}"
        fpy, dpy = f"({a}*x+({b}))**{n}", f"{n * a}*({a}*x+({b}))**{n - 1}"
        st = [f"$u={lin(a, b)}$ とおくと $y=u^{n}$。", f"$y'={n}u^{{{n - 1}}}\\cdot u'={n}({lin(a, b)})^{{{n - 1}}}\\cdot({a})$。"]
    elif kind == "quad_pow":
        c, n = nonzero(r, -5, 6), r.randint(2, 6)
        ftex, dtex = f"(x^2{tf_(c)})^{n}", f"{2 * n}x(x^2{tf_(c)})^{{{n - 1}}}" if n > 2 else f"{2 * n}x(x^2{tf_(c)})"
        fpy, dpy = f"(x**2+({c}))**{n}", f"{2 * n}*x*(x**2+({c}))**{n - 1}"
        st = [f"$u=x^2{tf_(c)}$ とおくと $y=u^{n}$、$u'=2x$。", f"$y'={n}u^{{{n - 1}}}\\cdot2x$。"]
    elif kind == "sqrt_quad":
        c = r.randint(1, 9)
        ftex, dtex = f"\\sqrt{{x^2+{c}}}", f"\\dfrac{{x}}{{\\sqrt{{x^2+{c}}}}}"
        fpy, dpy = f"sqrt(x**2+{c})", f"x/sqrt(x**2+{c})"
        st = [f"$u=x^2+{c}$ とおくと $y=u^{{\\frac{{1}}{{2}}}}$。", f"$y'=\\dfrac{{1}}{{2}}u^{{-\\frac{{1}}{{2}}}}\\cdot2x=\\dfrac{{x}}{{\\sqrt{{x^2+{c}}}}}$。"]
    elif kind == "sqrt_lin":
        a, b = r.randint(2, 6), r.randint(-4, 5)
        ftex, dtex = f"\\sqrt{{{lin(a, b)}}}", f"\\dfrac{{{a}}}{{2\\sqrt{{{lin(a, b)}}}}}" if a % 2 else f"\\dfrac{{{a // 2}}}{{\\sqrt{{{lin(a, b)}}}}}"
        fpy, dpy = f"sqrt({a}*x+({b}))", f"{a}/(2*sqrt({a}*x+({b})))"
        st = [f"$u={lin(a, b)}$ とおくと $y=\\sqrt{{u}}$、$u'={a}$。", f"$y'=\\dfrac{{1}}{{2\\sqrt{{u}}}}\\cdot {a}$。"]
    elif kind == "exp_quad":
        a = r.choice([1, 2, 3, -1, -2, F(1, 2)])
        at_ = ft(a) if a != 1 else ""
        at_ = "-" if a == -1 else at_
        ftex = f"e^{{{at_}x^2}}"
        dtex = f"{cf(2 * a) if F(2 * a).denominator == 1 else ft(2 * a)}xe^{{{at_}x^2}}"
        fpy, dpy = f"exp({fp(a)}*x**2)", f"{fp(2 * a)}*x*exp({fp(a)}*x**2)"
        st = [f"$u={at_}x^2$ とおくと $y=e^u$、$u'={cf(2 * a) if F(2 * a).denominator == 1 else ft(2 * a)}x$。".replace("=x", "=x"), f"$y'=e^u\\cdot u'={dtex}$。"]
    elif kind == "log_quad":
        c = r.randint(1, 9)
        ftex, dtex = f"\\log(x^2+{c})", f"\\dfrac{{2x}}{{x^2+{c}}}"
        fpy, dpy = f"log(x**2+{c})", f"2*x/(x**2+{c})"
        st = [f"$u=x^2+{c}$ とおくと $y=\\log u$。", f"$y'=\\dfrac{{u'}}{{u}}=\\dfrac{{2x}}{{x^2+{c}}}$。"]
    elif kind == "sin_pow":
        n = r.randint(2, 5)
        g = r.choice(["sin", "cos"])
        ftex = f"\\{g}^{n} x"
        dtex = f"{n}\\sin^{{{n - 1}}}x\\cos x" if g == "sin" else f"-{n}\\cos^{{{n - 1}}}x\\sin x"
        dtex = dtex.replace("^{1}", "")
        fpy = f"{g}(x)**{n}"
        dpy = f"{n}*sin(x)**{n - 1}*cos(x)" if g == "sin" else f"-{n}*cos(x)**{n - 1}*sin(x)"
        st = [f"$u=\\{g} x$ とおくと $y=u^{n}$。", f"$y'={n}u^{{{n - 1}}}\\cdot(\\{g} x)'$。"]
    else:
        a, b, n = r.randint(1, 4), nonzero(r, -5, 5), r.randint(1, 4)
        den = f"({lin(a, b)})^{n}" if n > 1 else f"{lin(a, b)}"
        ftex, dtex = f"\\dfrac{{1}}{{{den}}}", f"-\\dfrac{{{n * a}}}{{({lin(a, b)})^{{{n + 1}}}}}"
        fpy, dpy = f"1/({a}*x+({b}))**{n}", f"-{n * a}/({a}*x+({b}))**{n + 1}"
        st = [f"$y=({lin(a, b)})^{{-{n}}}$ と表す。", f"$y'=-{n}({lin(a, b)})^{{-{n + 1}}}\\cdot {a}$。"]
    return sa(f"合成関数の微分法を用いて、関数 $y={ftex}$ を微分しなさい。", f"$y'={dtex}$",
              "外側の関数を微分し、中身の導関数をかける：$\\{f(g(x))\\}'=f'(g(x))\\,g'(x)$。", d=2,
              ap="「外側」と「中身」に分けて $u=(\\text{中身})$ とおき、$\\dfrac{dy}{dx}=\\dfrac{dy}{du}\\cdot\\dfrac{du}{dx}$ を使う。",
              steps=st + [f"よって $y'={dtex}$。"],
              alt=["展開できる場合（低い累乗など）は展開してから微分し、結果が一致するか確かめる。"],
              pc=[("中身の導関数をかけている", 1), ("導関数が正しい", 1)],
              pit=["中身の導関数をかけ忘れる。", "累乗の指数を下ろした後、指数を1減らし忘れる。"],
              chk=(f"simplify(diff({fpy}, x)-({dpy}))", "0"))


@gen("basic_check", 4, ["computation"])
def product_quotient(r):
    kind = r.choice(["xn_exp", "xn_log", "exp_sin", "x_trig", "lin_frac", "log_frac", "x_quad"])
    if kind == "xn_exp":
        n, a = r.randint(1, 3), nonzero(r, -3, 3)
        xn = "x" if n == 1 else f"x^{n}"
        ftex = f"{xn}e^{{{cf(a)}x}}"
        inner = rlin(a, n)
        dtex = (f"({inner})e^{{{cf(a)}x}}" if n == 1 else f"{'x' if n == 2 else 'x^' + str(n - 1)}({inner})e^{{{cf(a)}x}}")
        fpy, dpy = f"x**{n}*exp({a}*x)", f"x**{n - 1}*({a}*x+{n})*exp({a}*x)"
        st = [f"積の微分法：$({xn})'e^{{{cf(a)}x}}+{xn}(e^{{{cf(a)}x}})'$。", f"$(e^{{{cf(a)}x}})'={cf(a)}e^{{{cf(a)}x}}$ を用いて整理する。"]
        rule = "積"
    elif kind == "xn_log":
        n = r.randint(1, 4)
        xn = "x" if n == 1 else f"x^{n}"
        ftex = f"{xn}\\log x"
        dtex = f"\\log x+1" if n == 1 else f"{'x' if n == 2 else 'x^' + str(n - 1)}({n}\\log x+1)"
        fpy, dpy = f"x**{n}*log(x)", f"x**{n - 1}*({n}*log(x)+1)"
        st = [f"積の微分法：$({xn})'\\log x+{xn}\\cdot\\dfrac{{1}}{{x}}$。", "共通因数でくくって整理する。"]
        rule = "積"
    elif kind == "exp_sin":
        a, b = nonzero(r, -3, 3), r.randint(1, 4)
        g = r.choice(["sin", "cos"])
        B = "x" if b == 1 else f"{b}x"
        ftex = f"e^{{{cf(a)}x}}\\{g} {B}"
        if g == "sin":
            dtex = f"e^{{{cf(a)}x}}({cf(a)}\\sin {B}+{cf(b)}\\cos {B})"
            dpy = f"exp({a}*x)*({a}*sin({b}*x)+{b}*cos({b}*x))"
        else:
            dtex = f"e^{{{cf(a)}x}}({cf(a)}\\cos {B}-{cf(b)}\\sin {B})"
            dpy = f"exp({a}*x)*({a}*cos({b}*x)-{b}*sin({b}*x))"
        fpy = f"exp({a}*x)*{g}({b}*x)"
        st = [f"積の微分法：$(e^{{{cf(a)}x}})'\\{g} {B}+e^{{{cf(a)}x}}(\\{g} {B})'$。", f"$e^{{{cf(a)}x}}$ でくくる。"]
        rule = "積"
    elif kind == "x_trig":
        n = r.randint(1, 3)
        g = r.choice(["sin", "cos"])
        xn = "x" if n == 1 else f"x^{n}"
        dxn = "" if n == 1 else (f"{n}x" if n == 2 else f"{n}x^{n - 1}")
        ftex = f"{xn}\\{g} x"
        if g == "sin":
            dtex = f"{dxn or ''}\\sin x+{xn}\\cos x"
            dpy = f"{n}*x**{n - 1}*sin(x)+x**{n}*cos(x)"
        else:
            dtex = f"{dxn or ''}\\cos x-{xn}\\sin x"
            dpy = f"{n}*x**{n - 1}*cos(x)-x**{n}*sin(x)"
        fpy = f"x**{n}*{g}(x)"
        st = [f"積の微分法：$({xn})'\\{g} x+{xn}(\\{g} x)'$。"]
        rule = "積"
    elif kind == "lin_frac":
        while True:
            a, b, c, d = nonzero(r, -4, 4), r.randint(-5, 5), r.randint(1, 3), nonzero(r, -5, 5)
            if a * d - b * c != 0:
                break
        ftex = f"\\dfrac{{{lin(a, b)}}}{{{lin(c, d)}}}"
        D = a * d - b * c
        dtex = f"{'-' if D < 0 else ''}\\dfrac{{{abs(D)}}}{{({lin(c, d)})^2}}"
        fpy, dpy = f"({a}*x+({b}))/({c}*x+({d}))", f"({D})/({c}*x+({d}))**2"
        st = [f"商の微分法：$\\dfrac{{({a})({lin(c, d)})-({lin(a, b)})\\cdot {c}}}{{({lin(c, d)})^2}}$。", f"分子を整理すると ${D}$。"]
        rule = "商"
    elif kind == "log_frac":
        n = r.randint(1, 3)
        xn = "x" if n == 1 else f"x^{n}"
        ftex = f"\\dfrac{{\\log x}}{{{xn}}}"
        dtex = f"\\dfrac{{1-{cf(n)}\\log x}}{{x^{n + 1}}}"
        fpy, dpy = f"log(x)/x**{n}", f"(1-{n}*log(x))/x**{n + 1}"
        st = [f"商の微分法：$\\dfrac{{\\frac{{1}}{{x}}\\cdot {xn}-\\log x\\cdot({xn})'}}{{x^{{{2 * n}}}}}$。", "分子・分母を整理する。"]
        rule = "商"
    else:
        a = r.randint(1, 9)
        ftex = f"\\dfrac{{x}}{{x^2+{a}}}"
        dtex = f"\\dfrac{{{a}-x^2}}{{(x^2+{a})^2}}"
        fpy, dpy = f"x/(x**2+{a})", f"({a}-x**2)/(x**2+{a})**2"
        st = [f"商の微分法：$\\dfrac{{1\\cdot(x^2+{a})-x\\cdot2x}}{{(x^2+{a})^2}}$。"]
        rule = "商"
    return sa(f"関数 $y={ftex}$ を微分しなさい。", f"$y'={dtex}$", f"{rule}の微分法を用いる。", d=2,
              ap=f"関数が2つの関数の{rule}になっている。{'$(fg)' + chr(39) + '=f' + chr(39) + 'g+fg' + chr(39) + '$' if rule == '積' else '$\\left(\\dfrac{f}{g}\\right)' + chr(39) + '=\\dfrac{f' + chr(39) + 'g-fg' + chr(39) + '}{g^2}$'} を使う。",
              steps=st + [f"$y'={dtex}$。"],
              alt=["商は $f\\cdot g^{-1}$ と積に直して微分しても同じ結果になる。" if rule == "商" else "対数微分法（両辺の自然対数をとって微分）でも確かめられる（$y>0$ の範囲）。"],
              pc=[(f"{rule}の微分法を正しく適用している", 1), ("整理した導関数が正しい", 1)],
              pit=["商の微分法の分子を $f'g+fg'$ と、積の公式と混同する。" if rule == "商" else "$(fg)'=f'g'$ としてしまう。", "整理の途中で符号を誤る。"],
              chk=(f"simplify(diff({fpy}, x)-({dpy}))", "0"))


TANG = [  # (f の LaTeX, f の式（X）, 接点の x（sympy）)
    ("e^{X}", "exp(X)", [0, 1, -1]), ("e^{2X}", "exp(2*X)", [0]), ("e^{-X}", "exp(-X)", [0, 1]),
    ("\\log X", "log(X)", [1, sp.E, sp.E ** 2]), ("2\\log X", "2*log(X)", [1]), ("\\sqrt{X}", "sqrt(X)", [1, 4, 9]),
    ("\\sin X", "sin(X)", [0, sp.pi / 3, sp.pi / 6]), ("\\cos X", "cos(X)", [sp.pi / 2, sp.pi / 3]), ("\\tan X", "tan(X)", [0, sp.pi / 4]),
    ("Xe^{X}", "X*exp(X)", [0, 1]), ("\\dfrac{4}{X}", "4/X", [1, 2]), ("\\dfrac{1}{X}", "1/X", [2, 3]), ("\\sqrt{X+3}", "sqrt(X+3)", [1, 6]),
]


@gen("basic_check", 4, ["computation", "concept"])
def tangent_line(r):
    while True:
        ftex, fpy, ts = r.choice(TANG)
        t = sp.nsimplify(r.choice(ts))
        f = sp.sympify(fpy, locals={"X": X})
        m = sp.simplify(sp.diff(f, X).subs(X, t))
        y0 = sp.simplify(f.subs(X, t))
        normal = r.random() < 0.35
        if not normal or m != 0:
            break
    ftex_ = ftex.replace("X", "x")
    pt = f"\\left({TX(t)},\\,{TX(y0)}\\right)"
    if normal:
        mm = sp.simplify(-1 / m)
        what = "法線"
    else:
        mm = m
        what = "接線"
    n = sp.simplify(y0 - mm * t)
    ans = f"$y={line_tex(mm, n)}$"
    return sa(f"曲線 $y={ftex_}$ 上の点 ${pt}$ における{what}の方程式を求めなさい。", ans,
              f"$y'$ に $x={TX(t)}$ を代入して接線の傾き ${TX(m)}$ を求める。" + ("法線の傾きは $-\\dfrac{1}{f'(a)}$。" if normal else ""), d=2,
              ap="接線の傾きは導関数に接点の $x$ 座標を代入した値。法線は接線に垂直なので、傾きは $-\\dfrac{1}{f'(a)}$。",
              steps=[f"$y'$ を求め、$x={TX(t)}$ を代入すると接線の傾きは ${TX(m)}$。"]
              + ([f"法線の傾きは $-\\dfrac{{1}}{{{TX(m)}}}={TX(mm)}$。"] if normal else [])
              + [f"$y-{TX(y0) if not str(TX(y0)).startswith('-') else '(' + TX(y0) + ')'}={TX(mm) if not isinstance(mm, sp.Add) else '(' + TX(mm) + ')'}\\left(x-{TX(t) if not str(TX(t)).startswith('-') else '(' + TX(t) + ')'}\\right)$ より ${ans[1:-1]}$。"],
              alt=[f"求めた直線に $x={TX(t)}$ を代入して $y={TX(y0)}$ となり、接点を通ることを確かめる。"],
              pc=[("接線の傾きを正しく求めている", 1), (f"{what}の方程式が正しい", 1)],
              pit=["法線の傾きを $-f'(a)$ とする（逆数にし忘れる）。" if normal else "傾きに導関数の式をそのまま使ってしまう。", "接点の $y$ 座標の計算を誤る。"],
              chk=(f"[limit(diff({pyx(fpy)}, x), x, {sp.sstr(t)}), {sp.sstr(mm)}*({sp.sstr(t)})+({sp.sstr(n)})-({sp.sstr(y0)})]", f"[{sp.sstr(m)}, 0]", None, "intermediate"))


@gen("basic_check", 3, ["computation"])
def second_deriv(r):
    kind = r.choice(["xexp", "trig", "log", "xlog", "sq"])
    if kind == "xexp":
        a = nonzero(r, -3, 3)
        ftex, fpy = f"xe^{{{cf(a)}x}}", f"x*exp({a}*x)"
        d1, d2 = f"({lin(a, 1)})e^{{{cf(a)}x}}", f"{cf(a)}({lin(a, 2)})e^{{{cf(a)}x}}"
        d2py = f"{a}*({a}*x+2)*exp({a}*x)"
    elif kind == "trig":
        a, b = r.sample([1, 2, 3, 4], 2)
        A, B = ("x" if a == 1 else f"{a}x"), ("x" if b == 1 else f"{b}x")
        ftex, fpy = f"\\sin {A}+\\cos {B}", f"sin({a}*x)+cos({b}*x)"
        d1 = f"{cf(a)}\\cos {A}-{cf(b)}\\sin {B}"
        d2 = f"-{cf(a * a)}\\sin {A}-{cf(b * b)}\\cos {B}"
        d2py = f"-{a * a}*sin({a}*x)-{b * b}*cos({b}*x)"
    elif kind == "log":
        a, b = r.randint(1, 4), r.randint(-3, 5)
        ftex, fpy = f"\\log({lin(a, b)})", f"log({a}*x+({b}))"
        d1, d2 = f"\\dfrac{{{a}}}{{{lin(a, b)}}}", f"-\\dfrac{{{a * a}}}{{({lin(a, b)})^2}}"
        d2py = f"-{a * a}/({a}*x+({b}))**2"
    elif kind == "xlog":
        k = r.randint(2, 4)
        ftex, fpy = f"x^{k}\\log x", f"x**{k}*log(x)"
        d1 = f"{'x' if k == 2 else 'x^' + str(k - 1)}({k}\\log x+1)"
        c2, c1 = k * (k - 1), 2 * k - 1
        d2 = f"{c2}\\log x+{c1}" if k == 2 else f"{'x' if k == 3 else 'x^' + str(k - 2)}({c2}\\log x+{c1})"
        d2py = f"x**{k - 2}*({c2}*log(x)+{c1})"
    else:
        a = r.randint(1, 4)
        A = "x" if a == 1 else f"{a}x"
        ftex, fpy = f"\\sin^2 {A}", f"sin({a}*x)**2"
        d1 = f"{cf(a)}\\sin {2 * a}x" if a > 0 else ""
        d2 = f"{2 * a * a}\\cos {2 * a}x"
        d2py = f"{2 * a * a}*cos({2 * a}*x)"
    return sa(f"関数 $y={ftex}$ の第2次導関数 $y''$ を求めなさい。", f"$y''={d2}$", f"$y'={d1}$ をもう一度微分する。", d=2,
              ap="まず $y'$ を求めて整理し、それをもう一度微分する。整理してから微分すると計算が楽になる。",
              steps=[f"$y'={d1}$。", f"もう一度微分して $y''={d2}$。"],
              alt=["$y''$ の符号から、グラフの凹凸（$y''>0$ なら下に凸）を読み取ると、答えの妥当性を確かめられる。"],
              pc=[("$y'$ が正しい", 1), ("$y''$ が正しい", 1)],
              pit=["$y'$ を整理せずに微分して計算を誤る。", "積の微分法の項を落とす。"],
              chk=(f"simplify(diff({fpy}, x, 2)-({d2py}))", "0"))


# ======================================================================
# B 標準演習
# ======================================================================

TRIG_T = [sp.pi / 6, sp.pi / 4, sp.pi / 3, 2 * sp.pi / 3, 3 * sp.pi / 4, 5 * sp.pi / 6]


@gen("standard_practice", 4, ["computation", "cross_unit"], rel=["HS-MATHC-U02"])
def param_implicit(r):
    kind = r.choice(["ellipse_t", "poly_t", "implicit", "inverse"])
    if kind == "ellipse_t":
        a, b = r.sample([1, 2, 3, 4, 5], 2)
        t0 = r.choice(TRIG_T)
        val = sp.simplify(-b * sp.cos(t0) / (a * sp.sin(t0)))
        xt, yt = f"{cf(a)}\\cos t", f"{cf(b)}\\sin t"
        stem = f"媒介変数 $t$ を用いて $x={xt},\\ y={yt}$ と表された曲線について、$\\dfrac{{dy}}{{dx}}$ を $t$ の式で表し、$t={TX(t0)}$ における値を求めなさい。"
        ans = f"$\\dfrac{{dy}}{{dx}}=-\\dfrac{{{b}\\cos t}}{{{a}\\sin t}}$、$t={TX(t0)}$ のとき ${TX(val)}$"
        steps = [f"$\\dfrac{{dx}}{{dt}}=-{cf(a)}\\sin t$、$\\dfrac{{dy}}{{dt}}={cf(b)}\\cos t$。", f"$\\dfrac{{dy}}{{dx}}=\\dfrac{{dy/dt}}{{dx/dt}}=-\\dfrac{{{b}\\cos t}}{{{a}\\sin t}}$。",
                 f"$t={TX(t0)}$ を代入して ${TX(val)}$。"]
        chk = (f"limit(diff({b}*sin(t), t)/diff({a}*cos(t), t), t, {sp.sstr(t0)})", sp.sstr(val))
        ap = "媒介変数表示の曲線では $\\dfrac{dy}{dx}=\\dfrac{dy/dt}{dx/dt}$。これは楕円（数学C）の接線の傾きを表す。"
        alt = [f"媒介変数を消去すると楕円 $\\dfrac{{x^2}}{{{a * a}}}+\\dfrac{{y^2}}{{{b * b}}}=1$。陰関数の微分で $\\dfrac{{dy}}{{dx}}=-\\dfrac{{{b * b}x}}{{{a * a}y}}$ を求め、点の座標を代入しても一致する。"]
    elif kind == "poly_t":
        while True:
            p, q, t0 = r.randint(-3, 3), r.randint(-4, 4), r.randint(-2, 3)
            if 2 * t0 + p != 0:
                break
        val = F(3 * t0 * t0 + q, 2 * t0 + p)
        stem = f"媒介変数 $t$ を用いて $x=t^2{'' if p == 0 else ('+' if p > 0 else '-') + cf(abs(p)) + 't'},\\ y=t^3{'' if q == 0 else ('+' if q > 0 else '-') + cf(abs(q)) + 't'}$ と表された曲線上で、$t={t0}$ に対応する点における $\\dfrac{{dy}}{{dx}}$ の値を求めなさい。"
        ans = f"${ft(val)}$"
        steps = [f"$\\dfrac{{dx}}{{dt}}=2t{tf_(p)}$、$\\dfrac{{dy}}{{dt}}=3t^2{tf_(q)}$。", f"$\\dfrac{{dy}}{{dx}}=\\dfrac{{3t^2{tf_(q)}}}{{2t{tf_(p)}}}$。", f"$t={t0}$ を代入して $\\dfrac{{{3 * t0 * t0 + q}}}{{{2 * t0 + p}}}={ft(val)}$。"]
        chk = (f"limit(diff(t**3+({q})*t, t)/diff(t**2+({p})*t, t), t, {t0})", fp(val))
        ap = "$x,\\ y$ をそれぞれ $t$ で微分し、$\\dfrac{dy}{dx}=\\dfrac{dy/dt}{dx/dt}$ を使う。"
        alt = ["$t$ を消去して $y$ を $x$ の式で表すのは難しい。媒介変数のまま微分するのが効率的である。"]
    elif kind == "implicit":
        while True:
            A, B = r.randint(1, 4), r.choice([1, 2, 3, -1, -2])
            x0, y0 = nonzero(r, -3, 3), nonzero(r, -3, 3)
            C = A * x0 * x0 + B * y0 * y0
            if C > 0:
                break
        val = F(-A * x0, B * y0)
        eq = f"{cf(A)}x^2{'+' if B > 0 else '-'}{cf(abs(B))}y^2={C}"
        stem = f"曲線 ${eq}$ 上の点 $({x0},\\,{y0})$ における接線の傾き $\\dfrac{{dy}}{{dx}}$ を、両辺を $x$ で微分することによって求めなさい。"
        ans = f"${ft(val)}$"
        steps = [f"両辺を $x$ で微分する。$y$ は $x$ の関数なので $(y^2)'=2y\\cdot\\dfrac{{dy}}{{dx}}$。", f"${2 * A}x{'+' if B > 0 else '-'}{2 * abs(B)}y\\dfrac{{dy}}{{dx}}=0$ より $\\dfrac{{dy}}{{dx}}={'-' if A * B > 0 else ''}\\dfrac{{{A}x}}{{{abs(B)}y}}$（$y\\neq0$）。",
                 f"$x={x0},\\ y={y0}$ を代入して ${ft(val)}$。"]
        chk = (f"limit(limit(-diff({A}*x**2+({B})*y**2, x)/diff({A}*x**2+({B})*y**2, y), x, {x0}), y, {y0})", fp(val))
        ap = "$y$ を $x$ の関数とみて、合成関数の微分法 $\\dfrac{d}{dx}y^2=2y\\dfrac{dy}{dx}$ を使い、両辺を $x$ で微分する。"
        alt = [f"{'楕円' if B > 0 else '双曲線'}（数学C）の接線の公式 ${cf(A)}x_0x{'+' if B > 0 else '-'}{cf(abs(B))}y_0y={C}$ に点を代入した直線の傾きと一致する。"]
    else:
        p, q = r.randint(1, 5), r.randint(-4, 4)
        k = r.randint(-2, 2)
        c = k ** 3 + p * k + q
        val = F(1, 3 * k * k + p)
        stem = f"関数 $f(x)=x^3+{cf(p)}x{tf_(q)}$ の逆関数を $g(x)$ とするとき、$g'({c})$ の値を求めなさい。"
        ans = f"${ft(val)}$"
        steps = [f"$f'(x)=3x^2+{p}>0$ なので $f(x)$ は増加関数で、逆関数 $g(x)$ が存在する。", f"$f({k})={c}$ より $g({c})={k}$。",
                 f"逆関数の微分法より $g'({c})=\\dfrac{{1}}{{f'({k})}}=\\dfrac{{1}}{{{3 * k * k + p}}}$。"]
        chk = (f"[({k})**3+{p}*({k})+({q}), 1/limit(diff(x**3+{p}*x+({q}), x), x, {k})]", f"[{c}, {fp(val)}]", None, "intermediate")
        ap = "$y=g(x)\\iff x=f(y)$。$\\dfrac{dy}{dx}=\\dfrac{1}{dx/dy}$ より、$g'(c)=\\dfrac{1}{f'(g(c))}$。まず $f(k)=" + str(c) + "$ となる $k$ を見つける。"
        alt = ["$y=f(x)$ と $y=g(x)$ のグラフは直線 $y=x$ に関して対称なので、対応する点での接線の傾きは互いに逆数になる。"]
    return sa(stem, ans, "媒介変数表示・陰関数・逆関数の微分法を用いる。", d=3, ap=ap, steps=steps, alt=alt,
              pc=[("微分の方法（式の立て方）が正しい", 2), ("導関数の式が正しい", 1), ("値が正しい", 1)],
              pit=["$\\dfrac{dy}{dx}$ を $\\dfrac{dx/dt}{dy/dt}$ と逆にする。", "$y^2$ を $x$ で微分して $2y$ とし、$\\dfrac{dy}{dx}$ をかけ忘れる。"], chk=chk,
              rel=(["HS-MATHC-U02"] if kind != "inverse" else ["HS-MATH2-U03"]))


@gen("standard_practice", 4, ["computation", "written_reasoning"])
def extrema_trans(r):
    kind = r.choice(["xexp", "x2exp", "logx", "trig_s", "trig_c", "cosh"])
    if kind == "xexp":
        a = r.choice([1, 2, 3, -1, -2])
        ftex, fpy = f"xe^{{{cf(-a)}x}}", f"x*exp({-a}*x)"
        x0 = F(1, a)
        v = sp.Rational(1, a) * sp.exp(-1)
        kind_word = "極大" if a > 0 else "極小"
        ans = f"$x={ft(x0)}$ で{kind_word}値 ${TX(v)}$（他に極値はない）"
        steps = [f"$y'=e^{{{cf(-a)}x}}+x\\cdot({-a})e^{{{cf(-a)}x}}=({rlin(-a, 1)})e^{{{cf(-a)}x}}$。", f"$e^{{{cf(-a)}x}}>0$ なので、$y'$ の符号は ${lin(-a, 1)}$ の符号と一致する。$y'=0$ より $x={ft(x0)}$。",
                 f"$x={ft(x0)}$ の前後で $y'$ は{'正から負' if a > 0 else '負から正'}に変わるので{kind_word}。", f"{kind_word}値は ${ft(x0)}e^{{-1}}={TX(v)}$。"]
        chk = (f"[solve(diff({fpy}, x), x), limit({fpy}, x, {fp(x0)})]", f"[[{fp(x0)}], {sp.sstr(v)}]", None, "intermediate")
    elif kind == "x2exp":
        a = r.choice([1, 2, 3])
        ftex, fpy = f"x^2e^{{{cf(-a)}x}}", f"x**2*exp({-a}*x)"
        x1 = F(2, a)
        v = sp.Rational(4, a * a) * sp.exp(-2)
        ans = f"$x=0$ で極小値 $0$、$x={ft(x1)}$ で極大値 ${TX(v)}$"
        steps = [f"$y'=2xe^{{{cf(-a)}x}}-{cf(a)}x^2e^{{{cf(-a)}x}}=x({rlin(-a, 2)})e^{{{cf(-a)}x}}$。", f"$y'=0$ より $x=0,\\ {ft(x1)}$。",
                 f"$x<0$ で $y'<0$、$0<x<{ft(x1)}$ で $y'>0$、$x>{ft(x1)}$ で $y'<0$。", f"$x=0$ で極小値 $0$、$x={ft(x1)}$ で極大値 ${TX(v)}$。"]
        chk = (f"[solve(diff({fpy}, x), x), limit({fpy}, x, {fp(x1)})]", f"[[0, {fp(x1)}], {sp.sstr(v)}]", "set", "intermediate")
    elif kind == "logx":
        k = r.randint(1, 3)
        xk = "x" if k == 1 else f"x^{k}"
        ftex, fpy = f"\\dfrac{{\\log x}}{{{xk}}}", f"log(x)/x**{k}"
        x0tex = "e" if k == 1 else f"\\sqrt{{e}}" if k == 2 else "\\sqrt[3]{e}"
        v = sp.Rational(1, k) / sp.E
        ans = f"$x={x0tex}$ で極大値 ${TX(v)}$（他に極値はない）"
        steps = [f"定義域は $x>0$。$y'=\\dfrac{{1-{cf(k)}\\log x}}{{x^{k + 1}}}$。", f"$y'=0$ より $\\log x={ft(F(1, k))}$、$x={x0tex}$。",
                 f"$0<x<{x0tex}$ で $y'>0$、$x>{x0tex}$ で $y'<0$。", f"極大値は $\\dfrac{{{ft(F(1, k))}}}{{({x0tex})^{k}}}={TX(v)}$。" if k > 1 else f"極大値は $\\dfrac{{1}}{{e}}$。"]
        chk = (f"[solve(diff({fpy}, x), x), limit({fpy}, x, exp(Rational(1,{k})))]", f"[[exp(Rational(1,{k}))], {sp.sstr(v)}]", None, "intermediate")
    elif kind in ("trig_s", "trig_c"):
        c, x0 = r.choice([(1, None), (sp.sqrt(2), None), (sp.sqrt(3), None)])
        ctex = "" if c == 1 else TX(c)
        if kind == "trig_s":
            x0 = {1: sp.pi / 3, sp.sqrt(2): sp.pi / 4, sp.sqrt(3): sp.pi / 6}[c]
            x1 = 2 * sp.pi - x0
            ftex, fpy = f"{ctex}x-2\\sin x", f"{sp.sstr(c)}*x-2*sin(x)"
            s0 = sp.sin(x0)
            vmin = f"{TX(c * x0)}-{TX(2 * s0)}"
            vmax = f"{TX(c * x1)}+{TX(2 * s0)}"
            ans = f"$x={TX(x0)}$ で極小値 ${vmin}$、$x={TX(x1)}$ で極大値 ${vmax}$"
            steps = [f"$y'={ctex or '1'}-2\\cos x$。$y'=0$ より $\\cos x={TX(c / 2)}$、$0<x<2\\pi$ で $x={TX(x0)},\\ {TX(x1)}$。",
                     f"$0<x<{TX(x0)}$ で $y'<0$、${TX(x0)}<x<{TX(x1)}$ で $y'>0$、${TX(x1)}<x<2\\pi$ で $y'<0$。",
                     f"$x={TX(x0)}$ で極小値 ${vmin}$、$x={TX(x1)}$ で極大値 ${vmax}$。"]
            chk = (f"[limit({fpy}, x, {sp.sstr(x0)}), limit({fpy}, x, {sp.sstr(x1)})]", f"[{sp.sstr(c * x0 - 2 * s0)}, {sp.sstr(c * x1 + 2 * s0)}]", None, "intermediate")
        else:
            x0 = {1: sp.pi / 6, sp.sqrt(2): sp.pi / 4, sp.sqrt(3): sp.pi / 3}[c]
            x1 = sp.pi - x0
            ftex, fpy = f"{ctex}x+2\\cos x", f"{sp.sstr(c)}*x+2*cos(x)"
            c0 = sp.cos(x0)
            vmax = f"{TX(c * x0)}+{TX(2 * c0)}"
            vmin = f"{TX(c * x1)}-{TX(2 * c0)}"
            ans = f"$x={TX(x0)}$ で極大値 ${vmax}$、$x={TX(x1)}$ で極小値 ${vmin}$"
            steps = [f"$y'={ctex or '1'}-2\\sin x$。$y'=0$ より $\\sin x={TX(c / 2)}$、$0<x<2\\pi$ で $x={TX(x0)},\\ {TX(x1)}$。",
                     f"$0<x<{TX(x0)}$ で $y'>0$、${TX(x0)}<x<{TX(x1)}$ で $y'<0$、${TX(x1)}<x<2\\pi$ で $y'>0$。",
                     f"$x={TX(x0)}$ で極大値 ${vmax}$、$x={TX(x1)}$ で極小値 ${vmin}$。"]
            chk = (f"[limit({fpy}, x, {sp.sstr(x0)}), limit({fpy}, x, {sp.sstr(x1)})]", f"[{sp.sstr(c * x0 + 2 * c0)}, {sp.sstr(c * x1 - 2 * c0)}]", None, "intermediate")
        ftex = ftex + "\\ (0<x<2\\pi)"
    else:
        a = r.choice([4, 9, 16, 2, 3])
        ftex, fpy = f"e^x+{a}e^{{-x}}", f"exp(x)+{a}*exp(-x)"
        sq = {4: "2", 9: "3", 16: "4", 2: "\\sqrt{2}", 3: "\\sqrt{3}"}[a]
        x0tex = f"\\log {sq}"
        v = 2 * sp.sqrt(a)
        ans = f"$x={x0tex}$ で極小値 ${TX(v)}$（他に極値はない）"
        steps = [f"$y'=e^x-{a}e^{{-x}}=\\dfrac{{e^{{2x}}-{a}}}{{e^x}}$。", f"$y'=0$ より $e^{{2x}}={a}$、$e^x={sq}$、$x={x0tex}$。",
                 f"$x<{x0tex}$ で $y'<0$、$x>{x0tex}$ で $y'>0$。", f"極小値は ${sq}+\\dfrac{{{a}}}{{{sq}}}={TX(v)}$。"]
        chk = (f"[limit(diff({fpy}, x), x, log({sp.sstr(sp.sqrt(a))})), limit({fpy}, x, log({sp.sstr(sp.sqrt(a))}))]", f"[0, {sp.sstr(v)}]", None, "intermediate")
    return sa(f"関数 $y={ftex}$ の極値を求めなさい。", ans, "導関数の符号の変化を増減表で調べる。", d=3,
              ap="$y'$ を因数分解（または1つの分数にまとめ）し、正の因数（$e^x$ など）を除いて符号を決める部分を見つける。増減表で極大・極小を判定する。",
              steps=steps, alt=["第2次導関数 $y''$ の符号（$y''<0$ なら極大、$y''>0$ なら極小）で判定してもよい。"],
              pc=[("導関数を正しく求めている", 1), ("増減表で符号の変化を調べている", 1), ("極値とそのときの $x$ が正しい", 2)],
              pit=["$e^{-x}$ などの正の因数の符号を気にして増減表が混乱する。", "極値をとる $x$ だけ答えて、極値（関数の値）を答えない。"], chk=chk)


@gen("standard_practice", 4, ["computation", "condition_check"])
def inflection(r):
    kind = r.choice(["quartic", "gauss", "xexp", "logq"])
    if kind == "quartic":
        while True:
            al, be = sorted(r.sample(range(-3, 4), 2))
            if (al + be) % 1 == 0:
                break
        # y''=12(x-α)(x-β) → y = x^4 - 2(α+β)x^3 + 6αβ x^2 + ...
        b3, b2 = -2 * (al + be), 6 * al * be
        c1, c0 = r.randint(-3, 3), r.randint(-3, 3)
        coefs = [1, b3, b2, c1, c0]
        terms = []
        for i, cc in enumerate(coefs):
            k = 4 - i
            if cc == 0:
                continue
            mag = abs(cc)
            co = "" if (mag == 1 and k > 0) else str(mag)
            terms.append(("-" if cc < 0 else ("+" if terms else "")) + co + ("x" if k >= 1 else "") + (f"^{k}" if k >= 2 else ""))
        ftex = "".join(terms)
        fpy = f"x**4+({b3})*x**3+({b2})*x**2+({c1})*x+({c0})"
        ya, yb = [al ** 4 + b3 * al ** 3 + b2 * al ** 2 + c1 * al + c0, be ** 4 + b3 * be ** 3 + b2 * be ** 2 + c1 * be + c0]
        ans = f"$({al},\\,{ya})$、$({be},\\,{yb})$"
        steps = [f"$y''=12x^2{tf_(6 * b3)}x{tf_(2 * b2)}=12(x{tf_(-al)})(x{tf_(-be)})$。".replace("x+0", "x").replace("(x)", "x"), f"$y''=0$ より $x={al},\\ {be}$。",
                 f"$x<{al}$ で $y''>0$、${al}<x<{be}$ で $y''<0$、$x>{be}$ で $y''>0$ なので、どちらの前後でも凹凸が変わる。", f"変曲点は {ans}。"]
        chk = (f"[solve(diff({fpy}, x, 2), x), limit({fpy}, x, {al}), limit({fpy}, x, {be})]", f"[[{al}, {be}], {ya}, {yb}]", None, "intermediate")
    elif kind == "gauss":
        m = r.randint(1, 4)
        den = 2 * m * m
        ftex, fpy = f"e^{{-\\frac{{x^2}}{{{den}}}}}", f"exp(-x**2/{den})"
        ans = f"$\\left({m},\\,\\dfrac{{1}}{{\\sqrt{{e}}}}\\right)$、$\\left(-{m},\\,\\dfrac{{1}}{{\\sqrt{{e}}}}\\right)$"
        steps = [f"$y'=-\\dfrac{{x}}{{{m * m}}}e^{{-\\frac{{x^2}}{{{den}}}}}$。", f"$y''=\\dfrac{{x^2-{m * m}}}{{{m ** 4}}}e^{{-\\frac{{x^2}}{{{den}}}}}$。",
                 f"$y''=0$ より $x=\\pm {m}$。前後で $y''$ の符号が変わる。", f"$y=e^{{-\\frac{{1}}{{2}}}}=\\dfrac{{1}}{{\\sqrt{{e}}}}$。変曲点は {ans}。"]
        chk = (f"[solve(diff({fpy}, x, 2), x), limit({fpy}, x, {m})]", f"[[{-m}, {m}], exp(Rational(-1,2))]", None, "intermediate")
    elif kind == "xexp":
        a = r.choice([1, 2, 3])
        ftex, fpy = f"xe^{{{cf(-a)}x}}", f"x*exp({-a}*x)"
        x0 = F(2, a)
        v = sp.Rational(2, a) * sp.exp(-2)
        ans = f"$\\left({ft(x0)},\\,{TX(v)}\\right)$"
        steps = [f"$y'=({rlin(-a, 1)})e^{{{cf(-a)}x}}$。", f"$y''={cf(a)}({lin(a, -2)})e^{{{cf(-a)}x}}$。".replace("1(", "("),
                 f"$y''=0$ より $x={ft(x0)}$。前後で $y''$ の符号が負から正に変わる。", f"変曲点は {ans}。"]
        chk = (f"[solve(diff({fpy}, x, 2), x), limit({fpy}, x, {fp(x0)})]", f"[[{fp(x0)}], {sp.sstr(v)}]", None, "intermediate")
    else:
        a = r.randint(1, 4)
        ftex, fpy = f"\\log(x^2+{a * a})", f"log(x**2+{a * a})"
        ans = f"$({a},\\,\\log {2 * a * a})$、$(-{a},\\,\\log {2 * a * a})$"
        steps = [f"$y'=\\dfrac{{2x}}{{x^2+{a * a}}}$。", f"$y''=\\dfrac{{2(x^2+{a * a})-2x\\cdot2x}}{{(x^2+{a * a})^2}}=\\dfrac{{2({a * a}-x^2)}}{{(x^2+{a * a})^2}}$。",
                 f"$y''=0$ より $x=\\pm {a}$。前後で符号が変わる。", f"$y=\\log {2 * a * a}$。変曲点は {ans}。"]
        chk = (f"[solve(diff({fpy}, x, 2), x), limit({fpy}, x, {a})]", f"[[{-a}, {a}], log({2 * a * a})]", None, "intermediate")
    return sa(f"曲線 $y={ftex}$ の変曲点の座標をすべて求めなさい。", ans, "$y''=0$ となる点のうち、前後で $y''$ の符号が変わる点が変曲点。", d=3,
              ap="第2次導関数 $y''$ を求め、$y''=0$ の解の前後で符号が変わるかを確かめる（符号が変わらなければ変曲点ではない）。",
              steps=steps, alt=["グラフの対称性（偶関数ならば $y$ 軸対称）を使うと、片側の変曲点から他方が分かる。"],
              pc=[("$y''$ を正しく求めている", 1), ("符号の変化を確認している", 1), ("変曲点の座標が正しい", 2)],
              pit=["$y''=0$ を解いただけで、符号の変化を確かめない。", "変曲点の $y$ 座標を求め忘れる。"], chk=chk)


@gen("standard_practice", 4, ["application", "cross_unit"])
def velocity(r):
    kind = r.choice(["line", "line", "shm", "circle", "cycloid"])
    if kind == "line":
        b, c = r.randint(-6, 3), r.randint(-9, 9)
        t1 = r.randint(1, 4)
        xt = f"t^3{'' if b == 0 else ('+' if b > 0 else '-') + cf(abs(b)) + 't^2'}{'' if c == 0 else ('+' if c > 0 else '-') + cf(abs(c)) + 't'}"
        v, a = 3 * t1 * t1 + 2 * b * t1 + c, 6 * t1 + 2 * b
        stem = f"数直線上を動く点 P の時刻 $t$ における座標が $x={xt}$ であるとき、$t={t1}$ における P の速度、速さ、加速度を求めなさい。"
        ans = f"速度 ${v}$、速さ ${abs(v)}$、加速度 ${a}$"
        steps = [f"$v=\\dfrac{{dx}}{{dt}}=3t^2{tf_(2 * b)}t{tf_(c)}$".replace("+0t", "").replace("-0t", "") + "。", f"$\\alpha=\\dfrac{{dv}}{{dt}}=6t{tf_(2 * b)}$。",
                 f"$t={t1}$ を代入して $v={v}$、速さ $|v|={abs(v)}$、$\\alpha={a}$。"]
        chk = (f"[limit(diff(t**3+({b})*t**2+({c})*t, t), t, {t1}), limit(diff(t**3+({b})*t**2+({c})*t, t, 2), t, {t1})]", f"[{v}, {a}]", None, "intermediate")
        rel = ["HS-PHYB-U01"]
        ap = "速度は位置の時間微分、加速度は速度の時間微分。速さは速度の絶対値。"
        alt = ["物理の等加速度運動 $x=v_0t+\\dfrac{1}{2}at^2$ のように、位置を2回微分すると加速度になることと対応させて確かめる。"]
    elif kind == "shm":
        A, w = r.randint(1, 5), r.randint(1, 4)
        g = r.choice(["sin", "cos"])
        W = "t" if w == 1 else f"{w}t"
        stem = f"数直線上を動く点 P の時刻 $t$ における座標が $x={cf(A)}\\{g} {W}$ であるとき、P の加速度 $\\alpha$ を $x$ を用いて表し、P の速さの最大値を求めなさい。"
        ans = f"$\\alpha=-{cf(w * w)}x$、速さの最大値 ${A * w}$"
        vt = f"{A * w}\\cos {W}" if g == "sin" else f"-{A * w}\\sin {W}"
        steps = [f"$v=\\dfrac{{dx}}{{dt}}={vt}$。", f"$\\alpha=\\dfrac{{dv}}{{dt}}=-{A * w * w}\\{g} {W}=-{w * w}\\cdot {cf(A)}\\{g} {W}=-{cf(w * w)}x$。",
                 f"$|v|\\leqq {A * w}$ で、等号は $\\{'cos' if g == 'sin' else 'sin'} {W}=\\pm1$ のとき成り立つので、速さの最大値は ${A * w}$。"]
        chk = (f"[simplify(diff({A}*{g}({w}*t), t, 2)+{w * w}*{A}*{g}({w}*t)), {A}*{w}]", f"[0, {A * w}]", None, "intermediate")
        rel = ["HS-PHY-U01"]
        ap = "2回微分すると、もとの関数の $-\\omega^2$ 倍に戻る。これが物理の単振動の運動方程式 $a=-\\omega^2x$ の数学的な背景である。"
        alt = ["力学的エネルギー保存の考え方（物理）からも、速さが最大になるのは振動の中心 $x=0$ を通るときと分かる。"]
    elif kind == "circle":
        R, w = r.randint(1, 6), r.randint(1, 4)
        W = "t" if w == 1 else f"{w}t"
        stem = f"座標平面上を動く点 P の時刻 $t$ における座標が $x={cf(R)}\\cos {W},\\ y={cf(R)}\\sin {W}$ であるとき、P の速さと加速度の大きさを求めなさい。"
        ans = f"速さ ${R * w}$、加速度の大きさ ${R * w * w}$"
        steps = [f"$\\dfrac{{dx}}{{dt}}=-{R * w}\\sin {W},\\ \\dfrac{{dy}}{{dt}}={R * w}\\cos {W}$。", f"速さは $\\sqrt{{{(R * w) ** 2}(\\sin^2 {W}+\\cos^2 {W})}}={R * w}$。",
                 f"$\\dfrac{{d^2x}}{{dt^2}}=-{R * w * w}\\cos {W},\\ \\dfrac{{d^2y}}{{dt^2}}=-{R * w * w}\\sin {W}$ より、加速度の大きさは ${R * w * w}$。"]
        chk = (f"[simplify(sqrt(diff({R}*cos({w}*t), t)**2+diff({R}*sin({w}*t), t)**2)), simplify(sqrt(diff({R}*cos({w}*t), t, 2)**2+diff({R}*sin({w}*t), t, 2)**2))]", f"[{R * w}, {R * w * w}]", None, "intermediate")
        rel = ["HS-PHY-U01"]
        ap = "成分ごとに微分してベクトルの大きさを求める。$\\sin^2+\\cos^2=1$ で $t$ が消える。"
        alt = [f"物理の等速円運動の公式 $v=r\\omega,\\ a=r\\omega^2$（$r={R},\\ \\omega={w}$）と一致することを確かめる。"]
    else:
        a = r.randint(1, 4)
        t0 = r.choice([sp.pi / 3, sp.pi / 2, 2 * sp.pi / 3, sp.pi])
        sp_ = sp.simplify(2 * a * sp.sin(t0 / 2))
        stem = f"座標平面上を動く点 P の時刻 $t$ における座標が $x={cf(a)}(t-\\sin t),\\ y={cf(a)}(1-\\cos t)$ であるとき、$t={TX(t0)}$ における P の速さを求めなさい。"
        ans = f"${TX(sp_)}$"
        steps = [f"$\\dfrac{{dx}}{{dt}}={cf(a)}(1-\\cos t),\\ \\dfrac{{dy}}{{dt}}={cf(a)}\\sin t$。", f"速さは ${cf(a)}\\sqrt{{(1-\\cos t)^2+\\sin^2t}}={cf(a)}\\sqrt{{2-2\\cos t}}={2 * a}\\left|\\sin\\dfrac{{t}}{{2}}\\right|$。",
                 f"$t={TX(t0)}$ を代入して ${TX(sp_)}$。"]
        chk = (f"limit(sqrt(diff({a}*(t-sin(t)), t)**2+diff({a}*(1-cos(t)), t)**2), t, {sp.sstr(t0)})", sp.sstr(sp_))
        rel = ["HS-MATHC-U02"]
        ap = "サイクロイド（数学C の媒介変数表示）上を動く点。成分ごとに微分し、半角の公式 $1-\\cos t=2\\sin^2\\dfrac{t}{2}$ で整理する。"
        alt = ["半角の公式を使わず、$t$ の値を直接代入して $\\sqrt{\\left(\\frac{dx}{dt}\\right)^2+\\left(\\frac{dy}{dt}\\right)^2}$ を計算しても同じ値になる。"]
    return sa(stem, ans, "位置を時刻で微分すると速度、さらに微分すると加速度。平面では成分ごとに微分する。", d=3, ap=ap, steps=steps, alt=alt,
              pc=[("速度（成分）を正しく求めている", 1), ("加速度または速さの式が正しい", 1), ("値が正しい", 2)],
              pit=["速さを $\\dfrac{dx}{dt}+\\dfrac{dy}{dt}$ と成分の和で求める。", "速度（符号つき）と速さ（大きさ）を区別しない。"], chk=chk, rel=rel)


@gen("standard_practice", 4, ["condition_check", "concept"])
def mean_value(r):
    kind = r.choice(["quad", "cube", "sqrt", "recip", "log", "exp"])
    if kind == "quad":
        p, q = r.randint(-4, 4), r.randint(-4, 4)
        a = r.randint(-3, 2)
        b = a + r.randint(1, 4)
        ftex = f"x^2{'' if p == 0 else ('+' if p > 0 else '-') + cf(abs(p)) + 'x'}{tf_(q)}"
        fpy = f"x**2+({p})*x+({q})"
        c = sp.Rational(a + b, 2)
        steps = [f"$\\dfrac{{f({b})-f({a})}}{{{b}-({a})}}={a + b}{tf_(p)}$。", f"$f'(c)=2c{tf_(p)}$ とおいて $c={TX(c)}$。", f"${a}<{TX(c)}<{b}$ を満たす。"]
    elif kind == "cube":
        b = r.randint(1, 4)
        a = 0
        ftex, fpy = "x^3", "x**3"
        c = b / sp.sqrt(3)
        steps = [f"$\\dfrac{{f({b})-f(0)}}{{{b}-0}}={b * b}$。", f"$f'(c)=3c^2={b * b}$ より $c=\\pm {TX(c)}$。", f"$0<c<{b}$ より $c={TX(c)}$。"]
    elif kind == "sqrt":
        s, t = sorted(r.sample(range(1, 6), 2))
        a, b = s * s, t * t
        ftex, fpy = "\\sqrt{x}", "sqrt(x)"
        c = sp.Rational(s + t, 2) ** 2
        steps = [f"$\\dfrac{{\\sqrt{{{b}}}-\\sqrt{{{a}}}}}{{{b}-{a}}}=\\dfrac{{{t - s}}}{{{b - a}}}={TX(sp.Rational(1, s + t))}$。", f"$f'(c)=\\dfrac{{1}}{{2\\sqrt{{c}}}}={TX(sp.Rational(1, s + t))}$ より $\\sqrt{{c}}={TX(sp.Rational(s + t, 2))}$、$c={TX(c)}$。", f"${a}<{TX(c)}<{b}$ を満たす。"]
    elif kind == "recip":
        a = r.randint(1, 4)
        b = a * r.choice([4, 9]) if r.random() < 0.6 else a + r.randint(1, 5)
        ftex, fpy = "\\dfrac{1}{x}", "1/x"
        c = sp.sqrt(a * b)
        steps = [f"$\\dfrac{{\\frac{{1}}{{{b}}}-\\frac{{1}}{{{a}}}}}{{{b}-{a}}}=-\\dfrac{{1}}{{{a * b}}}$。", f"$f'(c)=-\\dfrac{{1}}{{c^2}}=-\\dfrac{{1}}{{{a * b}}}$ より $c^2={a * b}$。", f"${a}<c<{b}$ より $c={TX(c)}$。"]
    elif kind == "log":
        k = r.randint(1, 3)
        a, b = 1, sp.E ** k
        ftex, fpy = "\\log x", "log(x)"
        c = (sp.E ** k - 1) / k
        btex = "e" if k == 1 else f"e^{k}"
        steps = [f"$\\dfrac{{\\log {btex}-\\log 1}}{{{btex}-1}}=\\dfrac{{{k}}}{{{btex}-1}}$。", f"$f'(c)=\\dfrac{{1}}{{c}}$ とおいて $c={TX(c)}$。", f"$1<{TX(c)}<{btex}$ を満たす（$e\\fallingdotseq2.718$）。"]
    else:
        k = r.randint(1, 3)
        a, b = 0, k
        ftex, fpy = "e^x", "exp(x)"
        c = sp.log((sp.E ** k - 1) / k)
        inner = f"e-1" if k == 1 else f"\\dfrac{{e^{k}-1}}{{{k}}}"
        steps = [f"$\\dfrac{{e^{{{k}}}-e^0}}{{{k}-0}}={'e-1' if k == 1 else inner}$。", f"$f'(c)=e^c$ とおいて $c=\\log{'(e-1)' if k == 1 else '\\left(' + inner + '\\right)'}$。", f"$0<c<{k}$ を満たす。"]
    ctex = TX(c) if kind != "exp" else ("\\log(e-1)" if k == 1 else f"\\log\\left(\\dfrac{{e^{k}-1}}{{{k}}}\\right)")
    atex, btex2 = TX(a), TX(b)
    fx = sp.sympify(fpy, locals={"x": X})
    fa_, fb_ = sp.sstr(sp.simplify(fx.subs(X, a))), sp.sstr(sp.simplify(fx.subs(X, b)))
    return sa(f"関数 $f(x)={ftex}$ と区間 ${atex}\\leqq x\\leqq {btex2}$ について、平均値の定理 $\\dfrac{{f({btex2})-f({atex})}}{{{btex2}-{atex if not atex.startswith('-') else '(' + atex + ')'}}}=f'(c),\\ {atex}<c<{btex2}$ を満たす $c$ の値を求めなさい。",
              f"$c={ctex}$", "平均変化率を計算し、$f'(c)$ と等しいとおいて $c$ を求める。区間内にあるものを選ぶ。", d=3,
              ap="平均値の定理は「2点を結ぶ直線と平行な接線が区間内にある」ことを主張する。平均変化率を求め、$f'(c)$ と等しくなる $c$ を区間の中から選ぶ。",
              steps=steps, alt=["グラフ上で2端点を結ぶ直線をかき、これと平行な接線の接点の $x$ 座標が $c$ であることを図で確かめる。"],
              pc=[("平均変化率を正しく求めている", 1), ("$f'(c)$ との方程式を立てて解いている", 2), ("区間内の解を選んでいる", 1)],
              pit=["$c$ が区間 $a<c<b$ に入っているかを確かめない。", "平均変化率の分母・分子を逆にする。"],
              chk=(f"simplify(limit(diff({fpy}, x), x, {sp.sstr(c)})-(({fb_})-({fa_}))/(({sp.sstr(b)})-({sp.sstr(a)})))", "0"))


# ======================================================================
# C 思考力・記述応用
# ======================================================================

@gen("thinking_writing", 3, ["written_reasoning"])
def ineq_proof(r):
    kind = r.choice(["bern", "logtan", "exptan", "log1p"])
    rub = [("差の関数を設定し、導関数を正しく求めている", 3), ("増減（最小値）を正しく調べている", 3), ("結論を不等式として述べている", 2)]
    pc = [("差の関数と導関数", 3), ("増減・最小値", 3), ("結論", 2)]
    if kind == "bern":
        n = r.randint(2, 8)
        stem = f"$x\\geqq 0$ のとき、不等式 $(1+x)^{{{n}}}\\geqq 1+{n}x$ が成り立つことを証明しなさい。"
        g, gp, x0 = f"(1+x)**{n}-1-{n}*x", f"{n}*((1+x)**{n - 1}-1)", "0"
        steps = [f"$f(x)=(1+x)^{{{n}}}-(1+{n}x)$ とおく。", f"$f'(x)={n}(1+x)^{{{n - 1}}}-{n}={n}\\{{(1+x)^{{{n - 1}}}-1\\}}$。$x\\geqq 0$ のとき $(1+x)^{{{n - 1}}}\\geqq 1$ なので $f'(x)\\geqq 0$。",
                 "よって $f(x)$ は $x\\geqq 0$ で増加し、$f(x)\\geqq f(0)=0$。", f"したがって $(1+x)^{{{n}}}\\geqq 1+{n}x$（等号は $x=0$ のとき）。"]
        alt = [f"二項定理で $(1+x)^{{{n}}}=1+{n}x+(\\text{{0以上の項}})$ と展開しても示せる（$x\\geqq 0$）。"]
    elif kind == "logtan":
        a = r.randint(1, 6)
        rhs = "x-1" if a == 1 else f"\\dfrac{{x}}{{{a}}}+\\log {a}-1"
        stem = f"$x>0$ のとき、不等式 $\\log x\\leqq {rhs}$ が成り立つことを証明しなさい。"
        g = f"x/{a}+log({a})-1-log(x)"
        gp, x0 = f"1/{a}-1/x", str(a)
        steps = [f"$f(x)={rhs}-\\log x$ とおく（$x>0$）。", f"$f'(x)=\\dfrac{{1}}{{{a}}}-\\dfrac{{1}}{{x}}=\\dfrac{{x-{a}}}{{{a}x}}$。" if a != 1 else "$f'(x)=1-\\dfrac{1}{x}=\\dfrac{x-1}{x}$。",
                 f"$0<x<{a}$ で $f'(x)<0$、$x>{a}$ で $f'(x)>0$ なので、$f(x)$ は $x={a}$ で最小となる。",
                 f"最小値は $f({a})={'0' if a == 1 else '1+\\log ' + str(a) + '-1-\\log ' + str(a) + '=0'}$。よって $f(x)\\geqq 0$ であり、不等式が成り立つ（等号は $x={a}$ のとき）。"]
        alt = [f"右辺は曲線 $y=\\log x$ の $x={a}$ における接線である。$y=\\log x$ のグラフは上に凸（$y''<0$）なので、接線より下にあることからも分かる。"]
    elif kind == "exptan":
        a = r.randint(-2, 2)
        rhs = "x+1" if a == 0 else f"e^{{{a}}}(x{tf_(1 - a)})"
        stem = f"すべての実数 $x$ について、不等式 $e^x\\geqq {rhs}$ が成り立つことを証明しなさい。"
        g, gp, x0 = f"exp(x)-exp({a})*(x+1-({a}))", f"exp(x)-exp({a})", str(a)
        steps = [f"$f(x)=e^x-{rhs if a == 0 else rhs}$ とおく。".replace("-x+1", "-(x+1)"), f"$f'(x)=e^x-{'1' if a == 0 else 'e^{' + str(a) + '}'}$。$x<{a}$ で $f'(x)<0$、$x>{a}$ で $f'(x)>0$。",
                 f"$f(x)$ は $x={a}$ で最小で、最小値は $f({a})=e^{{{a}}}-e^{{{a}}}\\cdot1=0$。", f"よって $f(x)\\geqq 0$ であり、$e^x\\geqq {rhs}$（等号は $x={a}$ のとき）。"]
        alt = [f"右辺は曲線 $y=e^x$ の $x={a}$ における接線。$y=e^x$ は下に凸（$y''=e^x>0$）なので、グラフは接線より上にある。"]
    else:
        stem = "$x>0$ のとき、不等式 $x-\\dfrac{x^2}{2}<\\log(1+x)<x$ が成り立つことを証明しなさい。"
        g, gp, x0 = "x-log(1+x)", "x/(1+x)", "0"
        steps = ["$f(x)=x-\\log(1+x)$ とおくと $f'(x)=1-\\dfrac{1}{1+x}=\\dfrac{x}{1+x}>0\\ (x>0)$。$f(0)=0$ なので $x>0$ で $f(x)>0$、すなわち $\\log(1+x)<x$。",
                 "$g(x)=\\log(1+x)-x+\\dfrac{x^2}{2}$ とおくと $g'(x)=\\dfrac{1}{1+x}-1+x=\\dfrac{x^2}{1+x}>0\\ (x>0)$。",
                 "$g(0)=0$ なので $x>0$ で $g(x)>0$、すなわち $x-\\dfrac{x^2}{2}<\\log(1+x)$。", "以上より、$x>0$ のとき $x-\\dfrac{x^2}{2}<\\log(1+x)<x$。"]
        alt = ["$\\log(1+x)=\\displaystyle\\int_0^x\\dfrac{dt}{1+t}$ と表し、$1-t<\\dfrac{1}{1+t}<1\\ (t>0)$ を積分しても示せる（積分法の単元）。"]
        rub = [("右側の不等式を差の関数で示している", 3), ("左側の不等式を差の関数で示している", 3), ("$f(0)=0$ と単調性から結論を述べている", 2)]
        pc = [("右側", 3), ("左側", 3), ("結論", 2)]
    return desc(stem, "（証明）" + "".join(steps) + "（証明終）", "差をとった関数の増減を調べる。", rub, d=4, p=8, lines=10, kind="proof",
                ap="不等式 $A\\geqq B$ は、$f(x)=A-B$ の最小値が $0$ 以上であることを示せばよい。$f'(x)$ の符号から増減を調べる。",
                steps=steps, alt=alt, pc=pc,
                pit=["$f'(x)\\geqq 0$ を示しただけで、出発点 $f(0)$ や最小値の値を確かめない。", "定義域（$x>0$ など）を考えずに符号を判断する。"],
                chk=(f"[simplify(diff({g}, x)-({gp})), limit({g}, x, {x0})]", "[0, 0]", None, "intermediate"))


@gen("thinking_writing", 3, ["written_reasoning", "cross_unit"], rel=["HS-MATH3-U01"])
def count_roots(r):
    kind = r.choice(["xnexp", "xnexp", "logxm", "expx"])
    if kind == "xnexp":
        n, a = r.randint(1, 4), r.choice([1, 2])
        xn = "x" if n == 1 else f"x^{n}"
        ftex = f"{xn}e^{{{cf(-a)}x}}"
        x0 = sp.Rational(n, a)
        M = x0 ** n * sp.exp(-n)
        Mt = TX(M)
        if n % 2 == 1:
            ans = f"$k\\leqq 0$ のとき1個、$0<k<{Mt}$ のとき2個、$k={Mt}$ のとき1個、$k>{Mt}$ のとき0個"
            shape = f"$x<{TX(x0)}$ で増加、$x>{TX(x0)}$ で減少し、$x={TX(x0)}$ で極大値（最大値）${Mt}$ をとる。$x\\to-\\infty$ で $f(x)\\to-\\infty$、$x\\to\\infty$ で $f(x)\\to+0$。"
            crit = f"[{fp(F(n, a))}]" if n == 1 else f"[0, {fp(F(n, a))}]"
        else:
            ans = f"$k<0$ のとき0個、$k=0$ のとき1個、$0<k<{Mt}$ のとき3個、$k={Mt}$ のとき2個、$k>{Mt}$ のとき1個"
            shape = f"$x=0$ で極小値 $0$、$x={TX(x0)}$ で極大値 ${Mt}$ をとる。$x\\to-\\infty$ で $f(x)\\to\\infty$、$x\\to\\infty$ で $f(x)\\to+0$。"
            crit = f"[0, {fp(F(n, a))}]"
        stem = f"$k$ を実数の定数とする。方程式 ${ftex}=k$ の異なる実数解の個数を、$k$ の値によって分類しなさい。ただし、$\\displaystyle\\lim_{{x\\to\\infty}}x^ne^{{-x}}=0$（$n$ は自然数）を用いてよい。"
        fpy = f"x**{n}*exp({-a}*x)"
        fd = f"$f'(x)={'' if n == 1 else ('x' if n == 2 else 'x^' + str(n - 1))}({rlin(-a, n)})e^{{{cf(-a)}x}}$"
        chk = (f"[solve(diff({fpy}, x), x), limit({fpy}, x, {fp(F(n, a))})]", f"[{crit}, {sp.sstr(M)}]", "set" if n > 1 else None, "intermediate")
        if n > 1:
            chk = (f"[limit({fpy}, x, {fp(F(n, a))}), limit({fpy}, x, oo)]", f"[{sp.sstr(M)}, 0]", None, "intermediate")
    elif kind == "logxm":
        m = r.randint(1, 3)
        xm = "x" if m == 1 else f"x^{m}"
        ftex = f"\\dfrac{{\\log x}}{{{xm}}}"
        M = sp.Rational(1, m) / sp.E
        Mt = TX(M)
        x0t = "e" if m == 1 else ("\\sqrt{e}" if m == 2 else "\\sqrt[3]{e}")
        ans = f"$k\\leqq 0$ のとき1個、$0<k<{Mt}$ のとき2個、$k={Mt}$ のとき1個、$k>{Mt}$ のとき0個"
        shape = f"$0<x<{x0t}$ で増加、$x>{x0t}$ で減少し、最大値 $f({x0t})={Mt}$。$x\\to+0$ で $f(x)\\to-\\infty$、$x\\to\\infty$ で $f(x)\\to+0$。"
        stem = f"$k$ を実数の定数とする。方程式 $\\log x=k{xm}$ の異なる実数解の個数を、$k$ の値によって分類しなさい。ただし、$\\displaystyle\\lim_{{x\\to\\infty}}\\dfrac{{\\log x}}{{x}}=0$ を用いてよい。"
        fpy = f"log(x)/x**{m}"
        fd = f"$f(x)={ftex}$ とおくと（$x>0$）、$f'(x)=\\dfrac{{1-{cf(m)}\\log x}}{{x^{m + 1}}}$"
        chk = (f"[solve(diff({fpy}, x), x), limit({fpy}, x, exp(Rational(1,{m})))]", f"[[exp(Rational(1,{m}))], {sp.sstr(M)}]", None, "intermediate")
    else:
        a = r.randint(1, 3)
        ftex = f"\\dfrac{{e^{{{cf(a)}x}}}}{{x}}"
        M = a * sp.E
        Mt = TX(M)
        ans = f"$k<0$ のとき1個、$0\\leqq k<{Mt}$ のとき0個、$k={Mt}$ のとき1個、$k>{Mt}$ のとき2個"
        shape = (f"$x<0$ では減少し、$x\\to-\\infty$ で $f(x)\\to-0$、$x\\to-0$ で $f(x)\\to-\\infty$。$x>0$ では $x={ft(F(1, a))}$ で極小値 ${Mt}$ をとり、"
                 f"$x\\to+0$、$x\\to\\infty$ でともに $f(x)\\to\\infty$。")
        stem = f"$k$ を実数の定数とする。方程式 $e^{{{cf(a)}x}}=kx$ の異なる実数解の個数を、$k$ の値によって分類しなさい。ただし、$\\displaystyle\\lim_{{x\\to\\infty}}\\dfrac{{e^x}}{{x}}=\\infty$ を用いてよい。"
        fpy = f"exp({a}*x)/x"
        fd = f"$x=0$ は解でないので、両辺を $x$ で割って $k=\\dfrac{{e^{{{cf(a)}x}}}}{{x}}$。$f(x)={ftex}$ とおくと $f'(x)=\\dfrac{{({lin(a, -1)})e^{{{cf(a)}x}}}}{{x^2}}$"
        chk = (f"[solve(diff({fpy}, x), x), limit({fpy}, x, {fp(F(1, a))})]", f"[[{fp(F(1, a))}], {sp.sstr(M)}]", None, "intermediate")
    steps = ([f"$f(x)={ftex}$ とおくと、方程式の実数解の個数は、曲線 $y=f(x)$ と直線 $y=k$ の共有点の個数に等しい。"] if kind == "xnexp" else
             ["方程式を $k=f(x)$ の形に変形し、曲線 $y=f(x)$ と直線 $y=k$ の共有点の個数を調べる（定数分離）。"]) + [fd + "。", shape, f"直線 $y=k$ を上下に動かして共有点を数えると、{ans}。"]
    return desc(stem, ans, "定数 $k$ を分離し、$y=f(x)$ のグラフと直線 $y=k$ の共有点を数える。",
                [("$k$ を分離して $y=f(x)$ と $y=k$ の共有点の問題に言いかえている", 2), ("増減と極値・端の極限を正しく調べている", 4), ("$k$ による分類が正しい", 2)],
                d=5, p=8, lines=12,
                ap="文字定数 $k$ を片側に集めて $k=f(x)$ とし、$y=f(x)$ のグラフ（増減・極値・極限）をかいて、水平な直線 $y=k$ との共有点を数える。端のふるまいは極限（数学Ⅲ 極限）で調べる。",
                steps=steps, alt=["グラフをかかずに、増減表と中間値の定理を区間ごとに使って解の個数を数えることもできる。"],
                pc=[("定数分離", 2), ("増減と極限", 4), ("分類", 2)],
                pit=["端の極限（$x\\to\\pm\\infty$ や $x\\to+0$）を調べず、グラフの形を誤る。", "境界の $k$（極値と等しいとき）の個数を落とす。"], chk=chk)


@gen("thinking_writing", 2, ["written_reasoning", "computation"])
def asymptote_graph(r):
    q = r.randint(-3, 3)
    s = r.randint(1, 4)
    p = s * s - q * q
    num = f"x^2{tf_(p)}"
    den = "x" if q == 0 else f"x{tf_(-q)}"
    xmin, xmax = q + s, q - s
    vmin, vmax = 2 * q + 2 * s, 2 * q - 2 * s
    stem = f"関数 $y=\\dfrac{{{num}}}{{{den}}}$ の極値と、グラフの漸近線の方程式をすべて求めなさい。"
    ans = f"$x={xmax}$ で極大値 ${vmax}$、$x={xmin}$ で極小値 ${vmin}$。漸近線は $x={q}$ と $y={'x' if q == 0 else 'x' + tf_(q)}$"
    return desc(stem, ans, f"$y=x{tf_(q)}+\\dfrac{{{s * s}}}{{{den}}}$ と変形する。",
                [("帯分数式に変形している（割り算）", 2), ("導関数から極値を正しく求めている", 3), ("2本の漸近線を極限を用いて正しく求めている", 3)], d=4, p=8, lines=10,
                ap="分子の次数が分母以上なので、割り算して $y=(\\text{1次式})+\\dfrac{\\text{定数}}{x-q}$ の形にする。斜めの漸近線はこの1次式、縦の漸近線は分母 $=0$ の直線。",
                steps=[f"$x^2{tf_(p)}=({den})({'x' if q == 0 else 'x' + tf_(q)})+{s * s}$ より $y=x{tf_(q)}+\\dfrac{{{s * s}}}{{{den}}}$。",
                       f"$y'=1-\\dfrac{{{s * s}}}{{({den})^2}}=\\dfrac{{({den})^2-{s * s}}}{{({den})^2}}$。$y'=0$ より ${den}=\\pm {s}$、$x={xmin},\\ {xmax}$。",
                       f"$x<{xmax}$ で $y'>0$、${xmax}<x<{q}$ で $y'<0$、${q}<x<{xmin}$ で $y'<0$、$x>{xmin}$ で $y'>0$。",
                       f"$x={xmax}$ で極大値 ${vmax}$、$x={xmin}$ で極小値 ${vmin}$。",
                       f"$\\displaystyle\\lim_{{x\\to {q}+0}}y=\\infty,\\ \\lim_{{x\\to {q}-0}}y=-\\infty$ より直線 $x={q}$ は漸近線。",
                       f"$\\displaystyle\\lim_{{x\\to\\pm\\infty}}\\left\\{{y-\\left(x{tf_(q)}\\right)\\right\\}}=\\lim_{{x\\to\\pm\\infty}}\\dfrac{{{s * s}}}{{{den}}}=0$ より直線 $y={'x' if q == 0 else 'x' + tf_(q)}$ も漸近線。"],
                alt=[f"グラフは点 $({q},\\,{2 * q})$（2本の漸近線の交点）に関して対称であり、極大値と極小値の平均が ${2 * q}$ になることで検算できる。"],
                pc=[("変形", 2), ("極値", 3), ("漸近線", 3)],
                pit=["極大値が極小値より小さくなることに戸惑い、計算ミスと思い込む（不連続点をはさむので起こりうる）。", "斜めの漸近線を見落とし、$x=" + str(q) + "$ だけを答える。"],
                chk=(f"[limit(({num.replace('^', '**').replace('x**2', 'x**2')})/({den})-(x+({q})), x, oo), limit((x**2+({p}))/(x-({q})), x, {xmin}), limit((x**2+({p}))/(x-({q})), x, {xmax})]",
                     f"[0, {vmin}, {vmax}]", None, "intermediate"))


@gen("thinking_writing", 2, ["application", "written_reasoning"])
def optimization(r):
    kind = r.choice(["cyl", "cone", "rect", "dist"])
    if kind == "cyl":
        R = r.randint(1, 6)
        V = sp.Rational(4, 9) * sp.sqrt(3) * sp.pi * R ** 3
        h = 2 * sp.sqrt(3) * R / 3
        stem = f"半径 ${R}$ の球に内接する直円柱の体積の最大値と、そのときの円柱の高さを求めなさい。"
        ans = f"高さ ${TX(h)}$ のとき最大値 ${TX(V)}$"
        steps = [f"円柱の高さを $2x\\ (0<x<{R})$ とすると、底面の半径 $r$ は $r^2={R * R}-x^2$。", f"体積 $V=\\pi({R * R}-x^2)\\cdot2x=2\\pi({R * R}x-x^3)$。",
                 f"$V'=2\\pi({R * R}-3x^2)$、$V'=0$ より $x={TX(R / sp.sqrt(3))}$。この前後で $V'$ は正から負に変わり、極大かつ最大。",
                 f"最大値 $V={TX(V)}$、高さ $2x={TX(h)}$。"]
        x = sp.Symbol("x")
        chk = (f"limit(2*pi*({R * R}*x-x**3), x, {sp.sstr(R / sp.sqrt(3))})", sp.sstr(V))
        ap = "変数を1つ（高さの半分 $x$）に決め、三平方の定理で底面の半径を $x$ で表す。体積を $x$ の3次関数にして増減を調べる。"
    elif kind == "cone":
        R = r.randint(1, 6)
        V = sp.Rational(32, 81) * sp.pi * R ** 3
        h = sp.Rational(4, 3) * R
        stem = f"半径 ${R}$ の球に内接する直円錐の体積の最大値と、そのときの円錐の高さを求めなさい。"
        ans = f"高さ ${TX(h)}$ のとき最大値 ${TX(V)}$"
        steps = [f"円錐の高さを $h\\ (0<h<{2 * R})$ とすると、球の中心から底面までの距離は $|h-{R}|$ で、底面の半径 $r$ は $r^2={R * R}-(h-{R})^2={2 * R}h-h^2$。",
                 f"体積 $V=\\dfrac{{1}}{{3}}\\pi({2 * R}h-h^2)h=\\dfrac{{\\pi}}{{3}}({2 * R}h^2-h^3)$。", f"$V'=\\dfrac{{\\pi}}{{3}}h({4 * R}-3h)$、$V'=0$ より $h={TX(h)}$。前後で $V'$ は正から負に変わる。",
                 f"最大値 $V={TX(V)}$。"]
        chk = (f"limit(pi/3*({2 * R}*x**2-x**3), x, {sp.sstr(h)})", sp.sstr(V))
        ap = "高さ $h$ を変数にとり、球の中心・底面の中心・底面の円周上の点がつくる直角三角形で底面の半径を表す。"
    elif kind == "rect":
        a, b = r.randint(1, 6), r.randint(1, 4)
        S = sp.Rational(a, b) / sp.E
        stem = f"曲線 $y={cf(a)}e^{{{cf(-b)}x}}\\ (x>0)$ 上の点 P$(t,\\,{cf(a)}e^{{{cf(-b)}t}})$ から $x$ 軸、$y$ 軸に垂線 PQ、PR を下ろす。長方形 OQPR の面積の最大値と、そのときの $t$ の値を求めなさい。"
        ans = f"$t={ft(F(1, b))}$ のとき最大値 ${TX(S)}$"
        steps = [f"面積 $S(t)={cf(a)}te^{{{cf(-b)}t}}\\ (t>0)$。", f"$S'(t)={cf(a)}(1-{cf(b)}t)e^{{{cf(-b)}t}}$。$S'(t)=0$ より $t={ft(F(1, b))}$。",
                 f"$0<t<{ft(F(1, b))}$ で $S'>0$、$t>{ft(F(1, b))}$ で $S'<0$ なので、$t={ft(F(1, b))}$ で最大。", f"最大値は ${TX(S)}$。"]
        chk = (f"limit({a}*x*exp(-{b}*x), x, {fp(F(1, b))})", sp.sstr(S))
        ap = "面積を $t$ の関数で表し、$t>0$ の範囲で増減を調べる。"
    else:
        p = r.randint(1, 6)
        d = sp.sqrt(4 * p - 1) / 2
        stem = f"曲線 $y=\\sqrt{{x}}$ 上の点 P と点 A$({p},\\,0)$ の距離の最小値と、そのときの P の座標を求めなさい。"
        xm = sp.Rational(2 * p - 1, 2)
        ans = f"P$\\left({TX(xm)},\\,{TX(sp.sqrt(xm))}\\right)$ のとき最小値 ${TX(d)}$"
        steps = [f"P$(x,\\,\\sqrt{{x}})\\ (x\\geqq 0)$ とすると $\\mathrm{{AP}}^2=(x-{p})^2+x=x^2-{2 * p - 1}x+{p * p}$。",
                 f"$f(x)=x^2-{2 * p - 1}x+{p * p}$ とおくと $f'(x)=2x-{2 * p - 1}$、$x={TX(xm)}$ で最小（$0\\leqq x$ の範囲内）。",
                 f"最小値は $f\\left({TX(xm)}\\right)={TX(d ** 2)}$。よって AP の最小値は ${TX(d)}$。"]
        chk = (f"sqrt(limit((x-{p})**2+x, x, {sp.sstr(xm)}))", sp.sstr(d))
        ap = "距離そのものより、距離の2乗を考えると根号が消えて扱いやすい。変域 $x\\geqq0$ に注意する。"
    return desc(stem, ans, "求める量を1変数の関数で表し、変域内で増減を調べる。",
                [("求める量を1つの変数で表し、変域を示している", 3), ("導関数を求め増減を調べている", 3), ("最大値（最小値）とそのときの値が正しい", 2)], d=4, p=8, lines=10,
                ap=ap, steps=steps, alt=["変域の端での値（$0$ に近づく、など）と比べて、極値が最大（最小）であることを確認する説明もできる。"],
                pc=[("立式と変域", 3), ("増減", 3), ("答え", 2)],
                pit=["変域を考えず、変域外の解を候補にする。", "極値を求めただけで、それが最大（最小）であることを示さない。"], chk=chk)


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(stem, wrong, step, etype, tempt, fix, ans, expl, steps, ap, alt, pit, chk=None, d=3):
    return desc(f"{stem}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい答えを求めなさい。", ans, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい解答を途中式とともに示している", 3), ("最終的な答えが正しい", 1)], d=d, p=6, lines=6,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい途中式", 3), ("正しい答え", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix), chk=chk)


@gen("error_correction", 3, ["common_error", "computation"])
def err_chain(r):
    kind = r.choice(["trig", "exp", "log", "pow"])
    if kind == "trig":
        a, b = r.randint(2, 6), r.randint(-3, 3)
        g = r.choice(["sin", "cos"])
        arg = lin(a, b)
        A = f"({arg})" if b else arg
        wrongd = f"\\cos {A}" if g == "sin" else f"-\\sin {A}"
        right = f"{a}\\cos {A}" if g == "sin" else f"-{a}\\sin {A}"
        ftex, fpy, dpy = f"\\{g} {A}", f"{g}({a}*x+({b}))", (f"{a}*cos({a}*x+({b}))" if g == "sin" else f"-{a}*sin({a}*x+({b}))")
    elif kind == "exp":
        c = r.choice([1, 2, 3, -1, -2])
        ctex = cf(c)
        ftex, fpy = f"e^{{{ctex}x^2}}", f"exp({c}*x**2)"
        wrongd = f"e^{{{ctex}x^2}}"
        right = f"{cf(2 * c)}xe^{{{ctex}x^2}}"
        dpy = f"{2 * c}*x*exp({c}*x**2)"
        arg = f"{ctex}x^2"
    elif kind == "log":
        a, b = r.randint(2, 6), r.randint(1, 7)
        arg = lin(a, b)
        ftex, fpy = f"\\log({arg})", f"log({a}*x+({b}))"
        wrongd = f"\\dfrac{{1}}{{{arg}}}"
        right = f"\\dfrac{{{a}}}{{{arg}}}"
        dpy = f"{a}/({a}*x+({b}))"
    else:
        c, n = nonzero(r, -5, 5), r.randint(3, 7)
        arg = f"x^2{tf_(c)}"
        ftex, fpy = f"({arg})^{n}", f"(x**2+({c}))**{n}"
        wrongd = f"{n}({arg})^{{{n - 1}}}"
        right = f"{2 * n}x({arg})^{{{n - 1}}}"
        dpy = f"{2 * n}*x*(x**2+({c}))**{n - 1}"
    return err_item(f"関数 $y={ftex}$ を微分しなさい。", f"$y'={wrongd}$", "中身の関数の導関数をかけていない部分", "formula",
                    "外側の関数の公式（$(\\sin u)'=\\cos u$ など）だけを当てはめ、合成関数であることを意識していない。",
                    f"$u={arg}$ とおくと $y'=\\dfrac{{dy}}{{du}}\\cdot\\dfrac{{du}}{{dx}}$ なので $y'={right}$", f"$y'={right}$",
                    "合成関数の微分法：外側を微分したものに、中身の導関数をかける。",
                    [f"$u={arg}$ とおく。", "$\\dfrac{dy}{du}$ と $\\dfrac{du}{dx}$ を求める。", f"積をとって $y'={right}$。"],
                    "微分する前に「中身」があるかを確かめ、$u$ とおいて計算する。",
                    ["$x$ に具体的な値（例：$x=1$）を入れ、$\\dfrac{f(1.001)-f(1)}{0.001}$ を電卓で求めると、生徒の答えとは一致しないことが確かめられる。"],
                    ["中身の導関数をかけ忘れる。"], chk=(f"simplify(diff({fpy}, x)-({dpy}))", "0"))


@gen("error_correction", 3, ["common_error", "concept"])
def err_rules(r):
    kind = r.choice(["ax", "quot", "xx"])
    if kind == "ax":
        a = r.choice([2, 3, 5, 10])
        k = r.randint(1, 4)
        ftex = f"{cf(k)}{a}^x" if k == 1 else f"{k}\\cdot {a}^x"
        wrong = f"$y'={cf(k)}x\\cdot {a}^{{x-1}}$" if k == 1 else f"$y'={k}x\\cdot {a}^{{x-1}}$"
        right = f"{cf(k)}{a}^x\\log {a}"
        return err_item(f"関数 $y={ftex}$ を微分しなさい。", wrong, "$(x^n)'=nx^{n-1}$ の公式を使った部分", "formula",
                        "指数関数 $a^x$（変数が指数にある）と累乗関数 $x^n$（変数が底にある）を混同している。",
                        f"$(a^x)'=a^x\\log a$ より $y'={right}$", f"$y'={right}$", "指数関数の導関数は $(a^x)'=a^x\\log a$。",
                        [f"${a}^x=e^{{x\\log {a}}}$ と表せる。", f"合成関数の微分法より $({a}^x)'=e^{{x\\log {a}}}\\cdot\\log {a}={a}^x\\log {a}$。", f"$y'={right}$。"],
                        "変数が「底」にあるか「指数」にあるかを確認してから公式を選ぶ。",
                        [f"$x=0$ での接線の傾きを数値で求める：$\\dfrac{{{a}^{{0.001}}-1}}{{0.001}}\\fallingdotseq{(a ** 0.001 - 1) / 0.001:.3f}$ で、$\\log {a}\\fallingdotseq{math.log(a):.3f}$ と一致する（生徒の式では $0$ になる）。"],
                        ["指数関数と累乗関数の公式を混同する。"], chk=(f"simplify(diff({k}*{a}**x, x)-({k}*{a}**x*log({a})))", "0"))
    if kind == "quot":
        while True:
            a, b, c, d = nonzero(r, -4, 4), r.randint(-5, 5), r.randint(1, 3), nonzero(r, -5, 5)
            if a * d - b * c != 0:
                break
        D = a * d - b * c
        W = a * d + b * c if False else -(a * d - b * c)
        ftex = f"\\dfrac{{{lin(a, b)}}}{{{lin(c, d)}}}"
        wrong = f"$y'=\\dfrac{{({lin(a, b)})\\cdot {c}-({a})({lin(c, d)})}}{{({lin(c, d)})^2}}=\\dfrac{{{W}}}{{({lin(c, d)})^2}}$"
        right = f"{'-' if D < 0 else ''}\\dfrac{{{abs(D)}}}{{({lin(c, d)})^2}}"
        return err_item(f"関数 $y={ftex}$ を微分しなさい。", wrong, "商の微分法の分子で、引く順序を逆にした部分", "sign",
                        "商の微分法の分子 $f'g-fg'$ の順序をあいまいに覚えていて、$fg'-f'g$ としてしまった。",
                        f"$\\left(\\dfrac{{f}}{{g}}\\right)'=\\dfrac{{f'g-fg'}}{{g^2}}$ より $y'=\\dfrac{{({a})({lin(c, d)})-({lin(a, b)})\\cdot {c}}}{{({lin(c, d)})^2}}={right}$",
                        f"$y'={right}$", "分子は「分子の微分 × 分母 － 分子 × 分母の微分」。",
                        [f"$f={lin(a, b)},\\ g={lin(c, d)}$、$f'={a},\\ g'={c}$。", f"分子：$f'g-fg'={D}$。", f"$y'={right}$。"],
                        "$\\left(\\dfrac{1}{g}\\right)'=-\\dfrac{g'}{g^2}$ と積の微分法から公式を導き直せるようにしておく。",
                        [f"$y={ft(F(a, c))}+\\dfrac{{{ft(F(b * c - a * d, c))}}}{{{lin(c, d)}}}$ と変形してから微分しても ${right}$ が得られる。"],
                        ["分子の順序を逆にする。"], chk=(f"simplify(diff(({a}*x+({b}))/({c}*x+({d})), x)-({D})/({c}*x+({d}))**2)", "0"))
    n = r.randint(1, 3)
    xn = "x" if n == 1 else f"{n}x"
    ftex = f"x^{{{xn}}}\\ (x>0)"
    wrong = f"$y'={xn}\\cdot x^{{{xn}-1}}$"
    right = f"x^{{{xn}}}({cf(n)}\\log x+{n})" if n > 1 else "x^x(\\log x+1)"
    rpy = f"x**({n}*x)*({n}*log(x)+{n})"
    return err_item(f"関数 $y={ftex}$ を微分しなさい。", wrong, "累乗の公式 $(x^n)'=nx^{n-1}$ を、指数が変数の場合に使った部分", "concept",
                    "$x^{" + xn + "}$ を見て累乗関数と思い込み、指数にも変数 $x$ があることを見落としている。",
                    f"両辺の自然対数をとると $\\log y={xn}\\log x$。両辺を $x$ で微分して $\\dfrac{{y'}}{{y}}={cf(n)}\\log x+{n}$、よって $y'={right}$",
                    f"$y'={right}$", "底と指数の両方に変数があるときは、対数微分法を使う。",
                    [f"$y>0$ なので両辺の自然対数をとって $\\log y={xn}\\log x$。", f"両辺を $x$ で微分：$\\dfrac{{y'}}{{y}}={cf(n)}\\log x+{xn}\\cdot\\dfrac{{1}}{{x}}$。", f"$y'={right}$。"],
                    "$(x^n)'=nx^{n-1}$ は指数 $n$ が定数のときだけ使える。",
                    [f"$x^{{{xn}}}=e^{{{xn}\\log x}}$ と表して合成関数の微分法を使っても同じ結果になる。"],
                    ["指数に変数があることを見落とす。"], chk=(f"simplify(diff(x**({n}*x), x)-({rpy}))", "0"))


@gen("error_correction", 2, ["common_error", "condition_check"])
def err_extremum(r):
    kind = r.choice(["xsin", "xcos", "quartic"])
    if kind == "xsin":
        b = r.randint(-4, 4)
        k = r.randint(1, 3)
        ftex = f"{cf(k)}x-{cf(k)}\\sin x{tf_(b)}"
        wrong = f"$f'(x)={k}-{k}\\cos x$。$f'(x)=0$ より $\\cos x=1$、$x=0$ などで極値 $f(0)={b}$ をとる".replace("1-1", "1-")
        wrong = wrong.replace("$f'(x)=1-1\\cos x$", "$f'(x)=1-\\cos x$")
        return err_item(f"関数 $f(x)={ftex}$ は極値をもつか調べなさい。", wrong, "$f'(x)=0$ となる点をそのまま極値をとる点とした部分", "condition",
                        "「極値をとる点では $f'(x)=0$」を逆向きに使い、$f'(x)=0$ ならば極値と思い込んでいる。",
                        f"$f'(x)={cf(k)}(1-\\cos x)\\geqq 0$ で、$f'(x)=0$ となる点の前後でも符号は変わらない。$f(x)$ は常に増加し、極値をもたない", "極値をもたない",
                        "極値の判定には、$f'(x)=0$ の点の前後で $f'(x)$ の符号が変わるかを調べる。",
                        [f"$f'(x)={cf(k)}(1-\\cos x)$。", "$1-\\cos x\\geqq 0$ で、等号は $x=2n\\pi$（$n$ は整数）のときだけ。", "前後で符号が変わらないので、$f(x)$ は単調に増加し、極値をもたない。"],
                        "$f'(a)=0$ は極値の必要条件にすぎない。",
                        ["グラフ $y=x-\\sin x$ は、原点のまわりで $y=x^3$ のように平らになりながら増加し続ける。"],
                        ["前後の符号を確かめない。"], chk=(f"simplify(diff({k}*x-{k}*sin(x)+({b}), x)-{k}*(1-cos(x)))", "0"))
    if kind == "xcos":
        b = r.randint(-4, 4)
        ftex = f"x+\\cos x{tf_(b)}\\ (0<x<2\\pi)"
        wrong = f"$f'(x)=1-\\sin x$。$f'(x)=0$ より $x=\\dfrac{{\\pi}}{{2}}$。よって $x=\\dfrac{{\\pi}}{{2}}$ で極大値 $\\dfrac{{\\pi}}{{2}}{tf_(b)}$ をとる"
        return err_item(f"関数 $f(x)={ftex}$ の極値を調べなさい。", wrong, "$f'(x)=0$ の点の前後の符号を調べずに極大とした部分", "condition",
                        "$f'(x)=0$ の解が1つ見つかると、それを極値と決めつけてしまう。",
                        "$f'(x)=1-\\sin x\\geqq 0$ で、$x=\\dfrac{\\pi}{2}$ の前後でも $f'(x)>0$。$f(x)$ は増加し、極値をもたない", "極値をもたない",
                        "$\\sin x\\leqq 1$ より $f'(x)\\geqq 0$ がつねに成り立つ。",
                        ["$f'(x)=1-\\sin x$。", "$x\\neq\\dfrac{\\pi}{2}$ のとき $\\sin x<1$ なので $f'(x)>0$。", "$f(x)$ は $0<x<2\\pi$ で増加し、極値をもたない。"],
                        "増減表を必ずかき、前後の矢印の向きを確かめる。",
                        [f"$f\\left(\\dfrac{{\\pi}}{{3}}\\right)<f\\left(\\dfrac{{\\pi}}{{2}}\\right)<f\\left(\\dfrac{{2\\pi}}{{3}}\\right)$ を数値で確かめると、$x=\\dfrac{{\\pi}}{{2}}$ が極大でないことが分かる。"],
                        ["増減表をかかない。"], chk=("limit(diff(x+cos(x), x), x, pi/2)", "0", None, "intermediate"))
    a, b = r.randint(-5, 5), r.randint(-4, 4)
    ftex = f"x^4{'' if a == 0 else ('+' if a > 0 else '-') + cf(abs(a)) + 'x'}{tf_(b)}"
    wrong = f"$y'=4x^3{tf_(a)}$、$y''=12x^2$。$y''=0$ より $x=0$。よって変曲点は $(0,\\,{b})$"
    return err_item(f"曲線 $y={ftex}$ の変曲点を求めなさい。", wrong, "$y''=0$ となる点をそのまま変曲点とした部分", "condition",
                    "「変曲点では $y''=0$」を逆向きに使い、符号の変化を確かめていない。",
                    "$y''=12x^2\\geqq 0$ で、$x=0$ の前後で符号が変わらない。曲線はつねに下に凸で、変曲点はない", "変曲点はない",
                    "変曲点は、$y''$ の符号が変わる（凹凸が入れかわる）点。",
                    ["$y''=12x^2$。", "$x<0$ でも $x>0$ でも $y''>0$。", "凹凸が入れかわらないので、変曲点はない。"],
                    "$y''=0$ は変曲点の必要条件にすぎない。前後の符号を確かめる。",
                    ["$y=x^4$ のグラフは原点で平らだが、両側とも下に凸のままである。"], ["符号の変化を確かめない。"],
                    chk=(f"diff(x**4+({a})*x+({b}), x, 2)", "12*x**2", "expand", "intermediate"))


@gen("error_correction", 2, ["common_error", "computation"])
def err_normal_speed(r):
    if r.random() < 0.5:
        ftex, fpy, t = r.choice([("e^{2x}", "exp(2*X)", 0), ("\\log x", "log(X)", sp.E), ("\\sqrt{x}", "sqrt(X)", 4), ("x^3", "X**3", 1), ("\\dfrac{2}{x}", "2/X", 1)])
        f = sp.sympify(fpy, locals={"X": X})
        m = sp.diff(f, X).subs(X, t)
        y0 = f.subs(X, t)
        wn = y0 - (-m) * t
        rm = -1 / m
        rn = y0 - rm * t
        wrong = f"$y'$ に $x={TX(t)}$ を代入して接線の傾きは ${TX(m)}$。法線の傾きは ${TX(-m)}$ なので、法線は $y={line_tex(-m, wn)}$"
        return err_item(f"曲線 $y={ftex}$ 上の点 $({TX(t)},\\,{TX(y0)})$ における法線の方程式を求めなさい。", wrong, "法線の傾きを $-f'(a)$ とした部分", "formula",
                        "「垂直」を「傾きの符号を変える」と覚えてしまい、逆数にすることを忘れている。",
                        f"法線の傾きは $-\\dfrac{{1}}{{{TX(m)}}}={TX(rm)}$ なので、法線は $y={line_tex(rm, rn)}$", f"$y={line_tex(rm, rn)}$",
                        "2直線が垂直 $\\iff$ 傾きの積が $-1$。法線の傾きは $-\\dfrac{1}{f'(a)}$。",
                        [f"接線の傾き $f'({TX(t)})={TX(m)}$。", f"法線の傾き $-\\dfrac{{1}}{{{TX(m)}}}={TX(rm)}$。", f"$y-{TX(y0)}={TX(rm)}(x-{TX(t)})$ より $y={line_tex(rm, rn)}$。"],
                        "傾きの積が $-1$ になっているかで検算する習慣をつける。",
                        [f"接線の傾き ${TX(m)}$ と法線の傾き ${TX(rm)}$ の積が $-1$ になることを確かめる（生徒の答えでは積が ${TX(-m * m)}$）。"],
                        ["逆数にし忘れる。"], chk=(f"[limit(diff({pyx(fpy)}, x), x, {sp.sstr(t)})*({sp.sstr(rm)}), ({sp.sstr(rm)})*({sp.sstr(t)})+({sp.sstr(rn)})-({sp.sstr(y0)})]", "[-1, 0]", None, "intermediate"))
    R, w = r.randint(2, 6), r.randint(2, 4)
    W = f"{w}t"
    t0 = r.choice([sp.pi / (4 * w), sp.pi / (6 * w), sp.pi / (3 * w)])
    vx, vy = -R * w * sp.sin(w * t0), R * w * sp.cos(w * t0)
    wrongv = sp.simplify(vx + vy)
    wrong = f"$\\dfrac{{dx}}{{dt}}=-{R * w}\\sin {W},\\ \\dfrac{{dy}}{{dt}}={R * w}\\cos {W}$。$t={TX(t0)}$ のとき、速さは $\\dfrac{{dx}}{{dt}}+\\dfrac{{dy}}{{dt}}={TX(wrongv)}$"
    return err_item(f"座標平面上を動く点 P の時刻 $t$ における座標が $x={R}\\cos {W},\\ y={R}\\sin {W}$ のとき、$t={TX(t0)}$ における P の速さを求めなさい。", wrong,
                    "速さを速度の成分の和とした部分", "concept",
                    "速さを「$x$ 方向と $y$ 方向の速度を足したもの」と考え、ベクトルの大きさとして求めていない。",
                    f"速さは速度ベクトルの大きさ $\\sqrt{{\\left(\\dfrac{{dx}}{{dt}}\\right)^2+\\left(\\dfrac{{dy}}{{dt}}\\right)^2}}={R * w}$", f"${R * w}$",
                    "平面上の速さは $|\\vec{v}|=\\sqrt{\\left(\\frac{dx}{dt}\\right)^2+\\left(\\frac{dy}{dt}\\right)^2}$。",
                    [f"$\\vec{{v}}=(-{R * w}\\sin {W},\\ {R * w}\\cos {W})$。", f"$|\\vec{{v}}|=\\sqrt{{{(R * w) ** 2}(\\sin^2 {W}+\\cos^2 {W})}}={R * w}$。", f"$t={TX(t0)}$ でも速さは ${R * w}$。"],
                    "速さはベクトルの大きさ。成分は三平方の定理で合成する。",
                    [f"等速円運動（半径 ${R}$、角速度 ${w}$）の速さ $r\\omega={R * w}$ と一致する（生徒の答えは時刻によって変わってしまう）。"],
                    ["速度の成分を足してしまう。"],
                    chk=(f"limit(sqrt(diff({R}*cos({w}*t), t)**2+diff({R}*sin({w}*t), t)**2), t, {sp.sstr(t0)})", str(R * w)))


GENERATORS = [deriv_basic, chain_rule, product_quotient, tangent_line, second_deriv,
              param_implicit, extrema_trans, inflection, velocity, mean_value,
              ineq_proof, count_roots, asymptote_graph, optimization,
              err_chain, err_rules, err_extremum, err_normal_speed]
