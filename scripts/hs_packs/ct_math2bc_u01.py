"""単元パック：共通テスト対策 数学Ⅱ・B・C（微積分・指数対数・三角関数）。"""
import math
from decimal import Decimal
from fractions import Fraction as F

import sympy as sp

from banks._common import desc, figure, mc, num, plane, sa, table
from hs_pack_lib import board, check, definition, derivation, example, gen, guide, intro, lesson, poly, summary, theorem, tp

UNIT_ID = "CT-MATH2BC-U01"

PREREQUISITES = [
    ("HS-MATH2-U06", "導関数・増減表・定積分の計算と、放物線と直線で囲まれた面積の求め方"),
    ("HS-MATH2-U05", "対数の性質と常用対数（$\\log_{10}2,\\ \\log_{10}3$ を用いた近似計算）"),
    ("HS-MATH2-U04", "弧度法・三角関数のグラフ・加法定理と合成"),
    ("HS-MATH1-U03", "二次関数の最大・最小（置き換えた後の変数の範囲を考える処理）"),
]
EXTENSIONS = [
    ("SS-MATH-U02", "共通テストの誘導で身につけた微積分の処理を、誘導のない記述式答案として書き切る"),
    ("HS-MATH3-U02", "三角・指数・対数関数の導関数を使った増減・極値の調べ方へ発展する"),
    ("HS-MATH3-U03", "面積の考え方を置換積分・部分積分による面積・体積の計算へ広げる"),
]


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
    """有理数の sympy 表記。"""
    v = F(v)
    return str(v.numerator) if v.denominator == 1 else f"Rational({v.numerator},{v.denominator})"


def fs(v):
    """有理数の短い表記（9/2 など）。"""
    v = F(v)
    return str(v.numerator) if v.denominator == 1 else f"{v.numerator}/{v.denominator}"


def py(*coefs, var="x"):
    deg = len(coefs) - 1
    return "+".join(f"({fp(c)})*{var}**{deg - i}" for i, c in enumerate(coefs))


def ev(coefs, x):
    x = F(x)
    deg = len(coefs) - 1
    return sum(F(c) * x ** (deg - i) for i, c in enumerate(coefs))


def at(expr, v):
    return expr.replace("x", f"({v})")


def lin(c, var="x"):
    """x-c の LaTeX（c=0 なら x）。"""
    c = F(c)
    return var if c == 0 else f"{var}{'-' if c > 0 else '+'}{ft(abs(c))}"


def fac(c, var="x"):
    """因数 (x-c)。c=0 なら x。"""
    return var if F(c) == 0 else f"({lin(c, var)})"


def smx(s, first=False):
    """s·m の項（符号つき）。"""
    if s == 0:
        return ""
    mag = "" if abs(s) == 1 else str(abs(s))
    return ("-" if s < 0 else ("" if first else "+")) + mag + "m"


def dfmt(x):
    return format(x.normalize(), "f")


def dec(v):
    """有限小数で表せる有理数を小数表記にする。"""
    v = F(v)
    d = Decimal(v.numerator) / Decimal(v.denominator)
    s = format(d.normalize(), "f")
    return s


def lt(v):
    """sympy の値の LaTeX。"""
    return sp.latex(sp.nsimplify(v))


def coef_tex(v, first=False):
    """sympy の係数を、文字の前に置く形で表す（1 → 省略、-1 → -）。"""
    v = sp.nsimplify(v)
    if v == 1:
        s = ""
    elif v == -1:
        s = "-"
    else:
        s = sp.latex(v)
    if not first and not s.startswith("-"):
        s = "+" + s
    return s


LOG2, LOG3 = Decimal("0.3010"), Decimal("0.4771")


# ----------------------------------------------------------------------
# 授業プリント
# ----------------------------------------------------------------------

LESSON = lesson(
    goals=["共通テスト数学Ⅱ・B・C の微積分・指数対数・三角関数の大問で、誘導の意図（何を求めさせようとしているか）を読み取り、方針を短時間で立てられる。",
           "増減表による極値の判定、$\\dfrac{1}{6}$ 公式による面積、常用対数による桁数・年数の評価を、導出の筋道とともに使いこなせる。",
           "置き換えた変数の範囲・対数の底の条件・積分区間内の符号など、得点を落としやすい条件を答案の中で自分で確認できる。"],
    duration=100,
    readiness=["三次関数を微分して増減表をかける（数学Ⅱ 微分法）。", "定積分 $\\displaystyle\\int_\\alpha^\\beta f(x)\\,dx$ を計算できる。",
               "$\\log_{10}2=0.3010,\\ \\log_{10}3=0.4771$ から $\\log_{10}6$ などを計算できる。", "$a\\sin\\theta+b\\cos\\theta$ を合成できる。"],
    flow=[("導入：誘導文の読み方", 10, "大問の前半が後半の道具になっている構造を、過去の出題形式に似せた短い問題で確認する"),
          ("微分と極値・実数解の個数", 25, "増減表の作り方と、方程式 f(x)=k の実数解をグラフの共有点として数える方法（例題1）"),
          ("面積と 1/6 公式", 20, "公式の導出と、交点の差 β−α に注目した計算（例題2）"),
          ("対数の活用", 20, "桁数・何年後かの評価。不等号の向きと近似値の扱い（例題3）"),
          ("三角関数の置き換え", 15, "合成と、sinθ=t とおいたときの t の範囲"),
          ("まとめと時間配分", 10, "典型的な失点と見直しの観点を確認し、問題プリントの課題を指示")],
    sections=[
        intro("in1", "共通テストの数学Ⅱ・B・C は「誘導に乗る」試験",
              "共通テストの数学Ⅱ・B・C は試験時間 70 分で、数学Ⅱの必答問題と、数学B・数学C の内容から選んで解く問題で構成される。各大問は、前半の小問で求めた式や値が後半の考察の道具になるように作られていることが多い。問題文が長く、会話文や資料が添えられることもあるが、裏にある数学は教科書の基本事項である。大切なのは、(1) 前半の結果を後半でどう使うのかを予測しながら読むこと、(2) 計算の途中で条件（変数の範囲・底の条件など）を確認すること、の2点である。",
              bullets=["前半の小問の答えは、後半で「何に使われるか」を考えながら書きとめる。", "会話文に出てくる「〜とおくと」「〜に注目すると」は、方針そのものを示すヒントである。",
                       "1大問あたりの時間の目安を決め、手が止まったら次の小問・次の大問へ進む判断をする。"],
              points=[tp("大問全体を最初に30秒ほど眺め、小問どうしのつながり（どの結果がどこで使われるか）を矢印で書きこませる。", ask="(1) で求めた $f'(x)$ は、後の小問のどこで使われそうか。", expect="増減表・極値・実数解の個数で使う。", timing="導入の冒頭"),
                      tp("会話文は読み飛ばさず、数式に関係する一文に下線を引かせる。", caution="会話文を飛ばすと、誘導の置き換え（例：$t=\\sin\\theta$）に気づかず遠回りの計算をしてしまう。")]),
        definition("df1", "極値の判定（増減表）",
                   "関数 $f(x)$ が $x=a$ で極値をとるかどうかは、$f'(x)$ の符号が $x=a$ の前後で変わるかどうかで判定する。$f'(a)=0$ は極値をとるための必要条件にすぎない。",
                   formula="$$f'(x)\\ \\text{の符号が}\\ x=a\\ \\text{の前後で}\\ +\\to-\\ \\Longrightarrow\\ \\text{極大},\\qquad -\\to+\\ \\Longrightarrow\\ \\text{極小}$$",
                   conditions=["$f'(a)=0$ でも符号が変わらなければ極値ではない（例：$f(x)=x^3$ の $x=0$）。",
                               "三次関数 $f(x)=ax^3+\\cdots$ が極値をもつ $\\iff$ $f'(x)=0$ が異なる2つの実数解をもつ（判別式 $D>0$）。"],
                   points=[tp("増減表は「$f'(x)$ の符号の行」を先に埋め、その後で $f(x)$ の矢印を書く順序を守らせる。", caution="$f'(x)=0$ の解を求めただけで極値と決めつける答案が多い。")]),
        theorem("th1", "放物線と直線で囲まれた部分の面積（$\\dfrac{1}{6}$ 公式）",
                "$$\\int_\\alpha^\\beta (x-\\alpha)(x-\\beta)\\,dx=-\\dfrac{(\\beta-\\alpha)^3}{6}$$",
                ["放物線 $y=ax^2+bx+c$ と直線が $x=\\alpha,\\ \\beta\\ (\\alpha<\\beta)$ で交わるとき、囲まれた部分の面積は $S=\\dfrac{|a|}{6}(\\beta-\\alpha)^3$。",
                 "2つの放物線で囲まれる場合も、差の $x^2$ の係数の絶対値を $|a|$ として同じ形で使える。"],
                body="交点の $x$ 座標の差 $\\beta-\\alpha$ だけで面積が決まるので、交点の座標そのものが汚い数でも、解と係数の関係から $(\\beta-\\alpha)^2=(\\alpha+\\beta)^2-4\\alpha\\beta$ を求めれば計算できる。",
                proof=["$x-\\beta=(x-\\alpha)-(\\beta-\\alpha)$ と書きかえると、$(x-\\alpha)(x-\\beta)=(x-\\alpha)^2-(\\beta-\\alpha)(x-\\alpha)$。",
                       "$\\displaystyle\\int_\\alpha^\\beta (x-\\alpha)^2dx=\\left[\\dfrac{(x-\\alpha)^3}{3}\\right]_\\alpha^\\beta=\\dfrac{(\\beta-\\alpha)^3}{3}$。",
                       "$\\displaystyle\\int_\\alpha^\\beta (\\beta-\\alpha)(x-\\alpha)dx=(\\beta-\\alpha)\\left[\\dfrac{(x-\\alpha)^2}{2}\\right]_\\alpha^\\beta=\\dfrac{(\\beta-\\alpha)^3}{2}$。",
                       "差をとって $\\dfrac{(\\beta-\\alpha)^3}{3}-\\dfrac{(\\beta-\\alpha)^3}{2}=-\\dfrac{(\\beta-\\alpha)^3}{6}$。",
                       "放物線と直線の差は $a(x-\\alpha)(x-\\beta)$ と因数分解できるので、面積は $|a|\\cdot\\dfrac{(\\beta-\\alpha)^3}{6}$ となる。"],
                points=[tp("$(x-\\alpha)$ のかたまりのまま積分する発想を強調する。展開してから積分すると計算量が増え、時間を失う。", ask="なぜ $x-\\beta$ を $(x-\\alpha)-(\\beta-\\alpha)$ と書きかえるのか。", expect="すべてを $x-\\alpha$ の式にすると、原始関数が $(x-\\alpha)^n$ の形になり、下端 $\\alpha$ を代入すると 0 になるから。")]),
        derivation("dv1", "常用対数で「大きさ」を読む",
                   ["正の数 $N$ が $n$ 桁の整数であることは、$10^{n-1}\\leqq N<10^n$ と同じである。",
                    "各辺の常用対数をとると（底 $10>1$ なので不等号の向きは変わらない）$n-1\\leqq\\log_{10}N<n$。",
                    "したがって、$\\log_{10}N$ の整数部分に 1 を加えたものが桁数である。",
                    "同様に、$0<N<1$ で小数第 $m$ 位に初めて 0 でない数字が現れることは $10^{-m}\\leqq N<10^{-m+1}$、すなわち $-m\\leqq\\log_{10}N<-m+1$ と同じである。",
                    "「$a$ 倍を $n$ 回くり返して $T$ 倍を超える」条件 $a^n>T$ は、$a>1$ なら $n\\log_{10}a>\\log_{10}T$、$0<a<1$ なら $\\log_{10}a<0$ で割るので不等号の向きが変わる。"],
                   body="共通テストでは「何年後に初めて〜を超えるか」「何桁か」という形で、常用対数の近似値 $\\log_{10}2=0.3010,\\ \\log_{10}3=0.4771$ が与えられることが多い。",
                   points=[tp("負の数で割る場面（$\\log_{10}0.8<0$ など）を必ず板書で取り上げ、不等号の向きを確認させる。", caution="減少の問題で不等号の向きを変え忘れ、答えが「0年後」などの不自然な値になる。")]),
        theorem("th2", "三角関数の合成",
                "$$a\\sin\\theta+b\\cos\\theta=\\sqrt{a^2+b^2}\\,\\sin(\\theta+\\alpha)\\quad\\left(\\cos\\alpha=\\dfrac{a}{\\sqrt{a^2+b^2}},\\ \\sin\\alpha=\\dfrac{b}{\\sqrt{a^2+b^2}}\\right)$$",
                ["$(a,\\,b)\\neq(0,\\,0)$", "最大・最小は、$\\theta+\\alpha$ の動く範囲を単位円上で確認してから読み取る。"],
                proof=["座標平面上の点 $(a,\\,b)$ をとり、原点からの距離を $r=\\sqrt{a^2+b^2}$、$x$ 軸の正の向きとのなす角を $\\alpha$ とすると $a=r\\cos\\alpha,\\ b=r\\sin\\alpha$。",
                       "$a\\sin\\theta+b\\cos\\theta=r(\\sin\\theta\\cos\\alpha+\\cos\\theta\\sin\\alpha)$。",
                       "加法定理より、これは $r\\sin(\\theta+\\alpha)$ に等しい。"],
                points=[tp("$\\theta$ の範囲が制限されている問題では、$\\theta+\\alpha$ の範囲を単位円上に太線で示させ、端点の値も必ず計算させる。")]),
        example("ex1", "例題1　三次方程式の実数解の個数",
                "$k$ を定数とする。$x$ の方程式 $x^3-3x^2-9x=k$ が異なる3つの実数解をもつような $k$ の値の範囲を求めよ。",
                ["$f(x)=x^3-3x^2-9x$ とおくと、実数解の個数は曲線 $y=f(x)$ と直線 $y=k$ の共有点の個数に等しい。",
                 "$f'(x)=3x^2-6x-9=3(x+1)(x-3)$。$x=-1$ で極大値 $f(-1)=5$、$x=3$ で極小値 $f(3)=-27$。",
                 "直線 $y=k$ が曲線と3点で交わるのは、$k$ が極小値と極大値の間にあるとき。"],
                "$-27<k<5$",
                thinking="文字定数 $k$ を右辺に分離すると、$k$ を含まない関数のグラフと水平な直線の共有点の問題になる（定数分離）。",
                figure=figure("y=x^3-3x^2-9x のグラフと直線 y=k", plane((-3, 5), (-30, 8), unit=12, grid=False, ticks=False,
                                                                      curves=[(lambda x: x ** 3 - 3 * x ** 2 - 9 * x, "")], points=[(-1, 5, "(-1,5)"), (3, -27, "(3,-27)")])),
                points=[tp("$k=5,\\ -27$ のとき（直線が極値の点を通るとき）は共有点が2個になることを、図で確認させる。", ask="$k=5$ のとき、異なる実数解はいくつか。", expect="2個（$x=-1$ は重解）。")],
                misconceptions=[("$f'(x)=0$ の解 $x=-1,\\ 3$ の間に $k$ があればよいとして $-1<k<3$", "比べるのは $x$ 座標ではなく極値（$y$ 座標）。$-27<k<5$")]),
        example("ex2", "例題2　放物線と直線で囲まれた部分の面積",
                "放物線 $y=x^2$ と直線 $y=2x+3$ で囲まれた部分の面積 $S$ を求めよ。",
                ["交点の $x$ 座標は $x^2=2x+3$、すなわち $(x+1)(x-3)=0$ より $x=-1,\\ 3$。", "$-1\\leqq x\\leqq3$ では直線が上にある。",
                 "$S=\\displaystyle\\int_{-1}^{3}\\{(2x+3)-x^2\\}dx=-\\int_{-1}^{3}(x+1)(x-3)\\,dx=\\dfrac{(3-(-1))^3}{6}$。"],
                "$S=\\dfrac{32}{3}$",
                thinking="(上の式)−(下の式) が $-(x-\\alpha)(x-\\beta)$ の形になるので、$\\dfrac{1}{6}$ 公式がそのまま使える。",
                figure=figure("放物線 y=x^2 と直線 y=2x+3 で囲まれた部分", plane((-2, 4), (-1, 10), unit=14, grid=False, ticks=False,
                                                                        curves=[(lambda x: x * x, "")], lines=[(2, 3, "")], points=[(-1, 1, "(-1,1)"), (3, 9, "(3,9)")])),
                points=[tp("公式の結果 $\\dfrac{4^3}{6}$ を約分し忘れる、$|a|$ をかけ忘れる、の2点を答え合わせで確認する。")]),
        example("ex3", "例題3　常用対数による「何か月後」の評価",
                "ある動画チャンネル（架空）の登録者数は毎月 1.2 倍に増えている。登録者数が現在の 10 倍を初めて超えるのは何か月後か。$\\log_{10}2=0.3010,\\ \\log_{10}3=0.4771$ とする。",
                ["$n$ か月後に $1.2^n>10$ となる最小の自然数 $n$ を求める。", "$\\log_{10}1.2=\\log_{10}\\dfrac{2^2\\cdot3}{10}=2\\times0.3010+0.4771-1=0.0791$。",
                 "$n\\times0.0791>1$ より $n>12.6\\cdots$。", "最小の自然数は $n=13$。"],
                "13か月後",
                thinking="「初めて超える」は「不等式を満たす最小の自然数」と読みかえる。1.2 を 2 と 3 と 10 の積・商で表す。",
                points=[tp("答えを出した後、$n=12$ では超えないことを $12\\times0.0791=0.9492<1$ で確認させる（境目の確認）。")]),
        board("bd1", "板書案",
              [("① 極値と実数解", ["$f'(a)=0$ は必要条件", "符号変化 $+\\to-$：極大", "$f(x)=k$ → $y=f(x)$ と $y=k$", "3解 $\\iff$ 極小値 $<k<$ 極大値"]),
               ("② 面積", ["$\\displaystyle\\int_\\alpha^\\beta(x-\\alpha)(x-\\beta)dx=-\\dfrac{(\\beta-\\alpha)^3}{6}$", "$S=\\dfrac{|a|}{6}(\\beta-\\alpha)^3$", "例：$y=x^2,\\ y=2x+3$ → $\\dfrac{32}{3}$"]),
               ("③ 対数・三角の置き換え", ["$n$ 桁 $\\iff n-1\\leqq\\log_{10}N<n$", "$\\log_{10}a<0$ で割ると向きが逆", "$t=\\sin\\theta$ → $-1\\leqq t\\leqq1$", "合成：$\\theta+\\alpha$ の範囲を図示"])],
              points=[tp("3列はそのまま「見直しのチェックリスト」として使えるように、各列の最後に確認すべき条件を赤で書く。")]),
        guide("gd1", "指導ガイド（口頭で補う要点と時間配分）",
              [tp("70 分で6つの大問を解く試験では、1大問あたりの時間の目安を最初に決めさせる。手が止まった小問は印をつけて後回しにする習慣を演習で身につけさせる。", timing="導入の後"),
               tp("誘導で「$t=\\sin\\theta$ とおく」とあれば、直後に「$t$ の範囲」を書く。範囲を書かずに二次関数・三次関数の最大・最小を求めると失点する。", ask="$0\\leqq\\theta<2\\pi$ のとき、$t=\\sin\\theta$ の範囲は何か。", expect="$-1\\leqq t\\leqq1$"),
               tp("面積の問題では、積分区間内でどちらのグラフが上にあるかを、区間内の1点（例：中点）を代入して確認させる。", caution="$x$ 軸の下にある部分を含めたまま積分すると、面積が打ち消し合う。"),
               tp("対数の近似値を使う問題では、答えの直前の自然数でも条件を満たさないことを確認させる。", timing="例題3の後"),
               tp("誤答訂正（問題プリントD）は、ペアで「どの行が誤りか」を先に言わせてから直させると、誤りの型が定着しやすい。")],
              misconceptions=[("$f'(a)=0$ なら $x=a$ で必ず極値をとる", "$f'(x)$ の符号が $x=a$ の前後で変わるときに限り極値"),
                              ("$\\log_{\\frac{1}{2}}(x-1)>2$ から $x-1>\\dfrac{1}{4}$", "底が1より小さいので不等号の向きが変わり、真数条件と合わせて $0<x-1<\\dfrac{1}{4}$"),
                              ("$y=2\\sin(\\theta+\\alpha)$ なら $\\theta$ の範囲によらず最大値 $2$", "$\\theta+\\alpha$ の動く範囲に $\\dfrac{\\pi}{2}$ が含まれるときに限り最大値 2")]),
        summary("sm1", "まとめ",
                ["誘導は「前半の結果が後半の道具」。小問どうしのつながりを意識して読む。",
                 "極値は $f'(x)$ の符号変化で判定。方程式の実数解の個数は、定数を分離してグラフの共有点で数える。",
                 "放物線と直線の面積は $\\dfrac{|a|}{6}(\\beta-\\alpha)^3$。上下関係と $x$ 軸の上下を確認する。",
                 "常用対数で桁数・年数を評価するときは、負の数で割る場面の不等号の向きと境目の自然数を確認する。",
                 "三角関数は置き換えた変数・合成した角の範囲を必ず書いてから最大・最小を求める。"]),
        check("ck1", "確認問題",
              [("$f(x)=x^3-3x$ の極大値と極小値を求めよ。", "$f'(x)=3(x+1)(x-1)$ より、$x=-1$ で極大値 $2$、$x=1$ で極小値 $-2$"),
               ("放物線 $y=x^2-4x$ と $x$ 軸で囲まれた部分の面積を求めよ。", "交点 $x=0,\\ 4$ より $S=\\dfrac{4^3}{6}=\\dfrac{32}{3}$"),
               ("$\\log_{10}2=0.3010$ として、$2^{30}$ は何桁の整数か。", "$30\\times0.3010=9.03$ より $10^9<2^{30}<10^{10}$、10桁"),
               ("$0\\leqq\\theta\\leqq\\pi$ のとき、$\\sin\\theta+\\sqrt{3}\\cos\\theta$ の最小値を求めよ。", "$2\\sin\\left(\\theta+\\dfrac{\\pi}{3}\\right)$、$\\theta+\\dfrac{\\pi}{3}=\\dfrac{4}{3}\\pi$ で最小値 $-\\sqrt{3}$")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

@gen("basic_check", 4, ["computation"])
def a_extreme(r):
    a = r.choice([1, -1, 2, -2])
    while True:
        p, q = sorted(r.sample(range(-3, 6), 2))
        if (p + q) % 2 == 0:
            break
    d = r.randint(-6, 6)
    cs = [a, -3 * a * (p + q) // 2, 3 * a * p * q, d]
    Fs = py(*cs)
    xM, xm = (p, q) if a > 0 else (q, p)
    M, m = ev(cs, xM), ev(cs, xm)
    dps = poly(3 * a, -3 * a * (p + q), 3 * a * p * q)
    sign_seq = "$+\\to-\\to+$" if a > 0 else "$-\\to+\\to-$"
    return sa(f"大問の前半で、関数 $f(x)={poly(*cs)}$ の極値を求める。$f(x)$ が極大となる $x$ の値と極大値、極小となる $x$ の値と極小値をそれぞれ答えなさい。",
              f"$x={xM}$ で極大値 ${M}$、$x={xm}$ で極小値 ${m}$",
              f"$f'(x)={dps}={3 * a}{fac(p)}{fac(q)}$。$f'(x)$ の符号は {sign_seq} と変わる。",
              d=2, v=[f"極大値{M}(x={xM}), 極小値{m}(x={xm})"],
              ap="極値は増減表で判定する。$f'(x)$ を因数分解して、符号が変わる $x$ を求める。",
              steps=[f"$f'(x)={dps}$ を因数分解し、$f'(x)=0$ の解 $x={p},\\ {q}$ を求める。",
                     f"$x^3$ の係数が{'正' if a > 0 else '負'}なので、$f'(x)$ の符号は $x<{p}$ で{'正' if a > 0 else '負'}、${p}<x<{q}$ で{'負' if a > 0 else '正'}、$x>{q}$ で{'正' if a > 0 else '負'}。",
                     f"極大：$x={xM}$、$f({xM})={M}$。極小：$x={xm}$、$f({xm})={m}$。"],
              alt=["三次関数のグラフの概形（$x^3$ の係数の符号でN字型か逆N字型か）から、左右どちらの解が極大かを判断して確かめる。"],
              pc=[("$f'(x)$ を正しく求めて因数分解している", 1), ("極大・極小を正しく判定し、値を求めている", 1)],
              pit=["$x^3$ の係数が負のとき、極大と極小を逆にする。", "$f(x)$ に代入すべきところを $f'(x)$ に代入する。"],
              chk=(f"[{at(Fs, xM)}, {at(Fs, xm)}]", f"[{fp(M)}, {fp(m)}]", None, "intermediate"))


@gen("basic_check", 3, ["computation"])
def a_tangent(r):
    a = r.choice([1, -1, 2])
    b, c, d = r.randint(-3, 3), r.randint(-4, 4), r.randint(-3, 3)
    t = r.choice([-2, -1, 1, 2, 3])
    cs = [a, b, c, d]
    Fs = py(*cs)
    ft_ = ev(cs, t)
    m = 3 * a * t * t + 2 * b * t + c
    n = ft_ - m * t
    ans = poly(m, n) if m != 0 else str(n)
    return sa(f"曲線 $C:\\ y={poly(*cs)}$ 上の、$x$ 座標が ${t}$ である点を $\\mathrm{{P}}$ とする。点 $\\mathrm{{P}}$ における $C$ の接線 $\\ell$ の方程式を求めなさい。",
              f"$y={ans}$", f"$y'={poly(3 * a, 2 * b, c)}$ より接線の傾きは ${m}$。点 $\\mathrm{{P}}({t},\\,{ft_})$ を通るので $y-({ft_})={m}{fac(t)}$。", d=2,
              v=[f"y={ans}"],
              ap="接線の方程式は「接点の座標」と「傾き＝その点での微分係数」の2つで決まる。",
              steps=[f"接点の $y$ 座標：$({t})$ を代入して ${ft_}$。", f"$y'={poly(3 * a, 2 * b, c)}$、$x={t}$ で傾き ${m}$。",
                     f"$y-({ft_})={m}{fac(t)}$ を整理して $y={ans}$。"],
              alt=[f"求めた直線の式と曲線の式を連立すると、$x={t}$ を重解にもつ三次方程式になることで確かめられる。"],
              pc=[("接点の座標と傾きを正しく求めている", 1), ("接線の方程式を正しく整理している", 1)],
              pit=["傾きを求めるときに $y'$ ではなく $y$ に代入してしまう。", "$y-y_1=m(x-x_1)$ の $x_1$ の符号を誤る。"],
              chk=(f"expand(limit(diff({Fs}, x), x, {t})*(x-({t}))+limit({Fs}, x, {t}))", f"({m})*x+({fp(n)})", "expand"))


@gen("basic_check", 4, ["computation", "concept"])
def a_log_value(r):
    while True:
        i, j, k = r.randint(-3, 5), r.randint(0, 3), r.randint(-3, 2)
        if i == 0 and j == 0:
            continue
        if (i, j, k) in ((1, 0, 0), (0, 1, 0)):
            continue
        N = F(2) ** i * F(3) ** j * F(10) ** k
        if not (F(1, 1000) <= N <= 5000):
            continue
        s = dec(N)
        if len(s.replace(".", "").replace("-", "").lstrip("0")) > 4:
            continue
        break
    L = i * LOG2 + j * LOG3 + k
    Ls = f"{L:.4f}"

    def pw(b, e):
        return "" if e == 0 else (f"{b}" if e == 1 else f"{b}^{{{e}}}")
    fac = "\\cdot".join(x for x in (pw(2, i), pw(3, j), pw(10, k)) if x)
    return num(f"常用対数表のかわりに $\\log_{{10}}2=0.3010$、$\\log_{{10}}3=0.4771$ の2つの値だけが与えられている。${s}$ を $2,\\ 3,\\ 10$ の累乗の積で表すことにより、$\\log_{{10}}{s}$ の近似値を小数第4位まで求めなさい。",
               Ls, f"${s}={fac}$ より、$\\log_{{10}}{s}={i}\\log_{{10}}2+{j}\\log_{{10}}3+({k})={Ls}$。", d=2,
               ap="与えられた対数の値は 2 と 3 だけなので、$N$ を $2^a3^b10^c$ の形に分解し、対数の性質で和に直す。",
               steps=[f"${s}={fac}$ と分解する。", f"$\\log_{{10}}{s}={i}\\times0.3010+{j}\\times0.4771+({k})$。", f"計算して ${Ls}$。"],
               alt=["5 が含まれるときは $5=\\dfrac{10}{2}$、小数は $10^{-1}$ などで表すと、どんな数も 2・3・10 で分解できることを確かめる。",
                    f"大きさの見当：$10^{{{math.floor(L)}}}\\leqq {s}<10^{{{math.floor(L) + 1}}}$ なので、求めた値が ${math.floor(L)}$ 以上 ${math.floor(L) + 1}$ 未満であることを確かめる。"],
               pc=[("2・3・10 の累乗の積に正しく分解している", 1), ("対数の性質を使って正しく計算している", 1)],
               pit=["$\\log_{10}5$ を $\\log_{10}2+\\log_{10}3$ のように誤って分解する。", "小数の数で $10^{-1}$ の分の $-1$ を加え忘れる。"],
               chk=(f"({i})*0.3010+({j})*0.4771+({k})", Ls))


DIGIT_BASES = [(2, 1, 0), (3, 0, 1), (6, 1, 1), (12, 2, 1), (18, 1, 2), (24, 3, 1)]


@gen("basic_check", 3, ["computation", "application"])
def a_digits(r):
    while True:
        b, i, j = r.choice(DIGIT_BASES)
        n = r.randint(15, 80)
        kind = r.choice(["int", "int", "dec"])
        L = i * LOG2 + j * LOG3
        x = n * L
        fl = int(x)
        if x - fl < Decimal("0.02") or x - fl > Decimal("0.98"):
            continue
        if kind == "int":
            truth = len(str(b ** n))
        else:
            p = 0
            while 10 ** p < b ** n:
                p += 1
            truth = p
        if truth != fl + 1:
            continue
        break
    Ls = f"{L:.4f}"
    if kind == "int":
        stem = f"${b}^{{{n}}}$ が何桁の整数であるかを、常用対数を用いて調べたい。$\\log_{{10}}2=0.3010$、$\\log_{{10}}3=0.4771$ として、桁数を求めなさい。"
        res = f"${fl}\\leqq\\log_{{10}}{b}^{{{n}}}<{fl + 1}$ より ${fl + 1}$ 桁"
        concl = f"$10^{{{fl}}}\\leqq {b}^{{{n}}}<10^{{{fl + 1}}}$ なので ${fl + 1}$ 桁。"
    else:
        stem = f"$\\left(\\dfrac{{1}}{{{b}}}\\right)^{{{n}}}$ を小数で表すと、小数第何位に初めて 0 でない数字が現れるか。$\\log_{{10}}2=0.3010$、$\\log_{{10}}3=0.4771$ として求めなさい。"
        res = f"$\\log_{{10}}\\left(\\dfrac{{1}}{{{b}}}\\right)^{{{n}}}=-{dfmt(x)}$ より小数第 ${fl + 1}$ 位"
        concl = f"$-{fl + 1}\\leqq -{dfmt(x)}<-{fl}$ なので $10^{{-{fl + 1}}}\\leqq\\left(\\dfrac{{1}}{{{b}}}\\right)^{{{n}}}<10^{{-{fl}}}$、小数第 ${fl + 1}$ 位。"
    return num(stem, str(fl + 1), res, d=2,
               ap="桁数や小数の位は「$10$ の何乗と何乗の間にあるか」で決まるので、常用対数をとって整数部分を調べる。",
               steps=[f"$\\log_{{10}}{b}={Ls}$（$2$ と $3$ の値から計算）。", f"$\\log_{{10}}{b}^{{{n}}}={n}\\times{Ls}={dfmt(x)}$。", concl],
               alt=[f"$n$ 桁 $\\iff 10^{{n-1}}\\leqq N<10^n$ を思い出し、${b}^{{{n}}}$ を $10^{{{dfmt(x)}}}$ と見て、$10^{{{fl}}}$ と $10^{{{fl + 1}}}$ の間にあることを確かめる。" if kind == "int" else
                    f"$\\left(\\dfrac{{1}}{{{b}}}\\right)^{{{n}}}=10^{{-{dfmt(x)}}}=10^{{-{fl + 1}}}\\times10^{{{dfmt(fl + 1 - x)}}}$ と書くと、$1\\leqq10^{{{dfmt(fl + 1 - x)}}}<10$ なので小数第 ${fl + 1}$ 位に初めて 0 でない数字が現れると確かめられる。"],
               pc=[("常用対数の値を正しく計算している", 1), ("整数部分から桁数（位）を正しく判断している", 1)],
               pit=(["桁数を $\\log_{10}N$ の整数部分そのもの（1 を加え忘れ）と答える。", "近似値の積を途中で四捨五入し、整数部分が変わってしまう。"] if kind == "int" else
                    ["$-" + f"{dfmt(x)}" + "$ の整数部分を $-" + f"{fl}" + "$ と考え、位を1つ小さく答える。", "$\\log_{10}\\dfrac{1}{" + f"{b}" + "}$ の符号（負）を落とす。"]),
               chk=(f"floor({n}*({i}*0.3010+{j}*0.4771))+1", str(fl + 1)))


@gen("basic_check", 3, ["concept"])
def a_trig_graph(r):
    A = r.choice([1, 2, 3, 4])
    B = r.choice([F(2), F(3), F(4), F(1, 2)])
    D = r.choice([-3, -2, -1, 1, 2, 3])
    fn = r.choice(["sin", "cos"])
    arg = "\\dfrac{\\theta}{2}" if B == F(1, 2) else f"{B}\\theta"
    head = "" if A == 1 else str(A)
    expr = f"{head}\\{fn} {arg}{'+' if D > 0 else ''}{D}"
    per = sp.latex(2 * sp.pi / sp.Rational(B.numerator, B.denominator))
    per_w1 = sp.latex(2 * sp.pi * sp.Rational(B.numerator, B.denominator))
    per_w2 = sp.latex(sp.pi / sp.Rational(B.numerator, B.denominator))
    right = f"最大値 ${A + D}$、最小値 ${-A + D}$、周期 ${per}$"
    w1 = f"最大値 ${A}$、最小値 ${-A}$、周期 ${per}$"
    w2 = f"最大値 ${A + D}$、最小値 ${-A + D}$、周期 ${per_w1}$"
    w3 = f"最大値 ${A + D}$、最小値 ${-A + D}$、周期 ${per_w2}$"
    return mc(f"会話文の中で、関数 $y={expr}$ のグラフの特徴が話題になっている。この関数の最大値・最小値・周期（正の周期のうち最小のもの）の組として正しいものを選びなさい。",
              [right, w1, w2, w3], f"$-1\\leqq\\{fn} {arg}\\leqq1$ より最大値 ${A + D}$、最小値 ${-A + D}$。周期は $\\dfrac{{2\\pi}}{{{ft(B)}}}={per}$。", d=1,
              ap="$y=A\\sin B\\theta+D$ では、$A$ が振幅、$D$ が上下の平行移動、$B$ が周期を決める。3つを別々に読む。",
              steps=[f"$\\{fn}$ の値の範囲 $[-1,\\,1]$ を ${A}$ 倍して ${D}$ を加え、最大値 ${A + D}$、最小値 ${-A + D}$。",
                     f"$\\theta$ の係数が ${ft(B)}$ なので、周期は $2\\pi\\div{ft(B)}={per}$。"],
              alt=[f"$\\theta=0$ から $\\theta={per}$ まで動かすと、${arg}$ がちょうど $0$ から $2\\pi$ まで動くことで周期を確かめられる。"],
              pc=[("最大値・最小値を正しく読み取っている", 1), ("周期を正しく求めている", 1)],
              why={w1: (f"定数項 ${D}$ による上下の平行移動を無視している。最大値・最小値はともに ${D}$ だけずれる。", "定数項の見落とし"),
                   w2: (f"周期を $2\\pi\\times{ft(B)}$ と計算している。$\\theta$ の係数が大きいほどグラフは横に縮み、周期は短くなる。", "周期の公式の逆用"),
                   w3: ("周期を $\\dfrac{\\pi}{B}$ としている。$\\sin,\\ \\cos$ の周期は $2\\pi$ がもとになる（$\\pi$ は $\\tan$ の周期）。", "正接の周期との混同")})


@gen("basic_check", 3, ["computation", "concept"])
def a_integral(r):
    al, be = sorted(r.sample(range(-3, 6), 2))
    a = r.choice([1, -1, 2, 3, -3])
    cs = [a, -a * (al + be), a * al * be]
    val = F(-a * (be - al) ** 3, 6)
    return num(f"定積分 $\\displaystyle\\int_{{{al}}}^{{{be}}}({poly(*cs)})\\,dx$ の値を求めなさい。ただし、被積分関数を因数分解し、$\\dfrac{{1}}{{6}}$ 公式を利用して計算すること。",
               fs(val), f"${poly(*cs)}={'' if a == 1 else ('-' if a == -1 else a)}(x-\\alpha)(x-\\beta)$（$\\alpha={al},\\ \\beta={be}$）より、値は $-\\dfrac{{{a}\\cdot({be}-({al}))^3}}{{6}}={ft(val)}$。", d=2, disp=f"${ft(val)}$",
               ap="被積分関数が積分区間の両端を解にもつことに気づけば、$\\displaystyle\\int_\\alpha^\\beta (x-\\alpha)(x-\\beta)dx=-\\dfrac{(\\beta-\\alpha)^3}{6}$ が使える。",
               steps=[f"${poly(*cs)}={'' if a == 1 else ('-' if a == -1 else a)}{fac(al)}{fac(be)}$ と因数分解する。", f"$\\beta-\\alpha={be - al}$。", f"値は ${'(' + str(a) + ')' if a < 0 else a}\\times\\left(-\\dfrac{{{be - al}^3}}{{6}}\\right)={ft(val)}$。"],
               alt=["展開したまま原始関数を求め、上端・下端を代入して計算しても同じ値になる（検算として有効）。"],
               pc=[("因数分解して公式の形を見抜いている", 1), ("正しい値を求めている", 1)],
               pit=["公式の負号を落とす。", "$x^2$ の係数 " + f"${a}$" + " をかけ忘れる。"],
               chk=(f"integrate({py(*cs)}, [x, {al}, {be}])", fp(val)))


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 4, ["computation", "condition_check"])
def b_area(r):
    a = r.choice([1, 1, 2, -1, -2])
    al, be = sorted(r.sample(range(-3, 5), 2))
    m, n = r.randint(-3, 3), r.randint(-4, 6)
    cs = [a, m - a * (al + be), n + a * al * be]
    S = F(abs(a) * (be - al) ** 3, 6)
    upper = "直線" if a > 0 else "放物線"
    line = poly(m, n) if m else str(n)
    diff_tex = f"-{abs(a) if abs(a) != 1 else ''}{fac(al)}{fac(be)}"
    return num(f"放物線 $y={poly(*cs)}$ と直線 $y={line}$ で囲まれた部分の面積 $S$ を求めなさい。（共通テストでは、交点の $x$ 座標を求める小問の直後に問われる形が多い。）",
               fs(S), f"交点は $x={al},\\ {be}$。区間内では{upper}が上にあり、$S=\\dfrac{{{abs(a)}}}{{6}}({be}-({al}))^3={ft(S)}$。", d=3, disp=f"$S={ft(S)}$",
               ap="2つのグラフの交点の $x$ 座標を求め、区間内でどちらが上かを確かめてから、(上)−(下) を積分する。差が $x^2$ の係数つきの $(x-\\alpha)(x-\\beta)$ になるので $\\dfrac{1}{6}$ 公式が使える。",
               steps=[f"連立して $({poly(*cs)})-({line})={poly(a, -a * (al + be), a * al * be)}={'' if a == 1 else ('-' if a == -1 else a)}{fac(al)}{fac(be)}$。", f"交点の $x$ 座標は $x={al},\\ {be}$。",
                      f"区間内の点 $x={ft(F(al + be, 2))}$ などで比べると{upper}が上。", f"(上)−(下)$={diff_tex}$ より $S=\\dfrac{{{abs(a)}}}{{6}}\\cdot{be - al}^3={ft(S)}$。"],
               alt=[f"$\\displaystyle S=\\left|\\int_{{{al}}}^{{{be}}}\\{{({poly(*cs)})-({line})\\}}dx\\right|$ を展開して直接計算しても同じ値になる。"],
               pc=[("交点の $x$ 座標を正しく求めている", 1), ("上下関係を確認して積分の式を立てている", 1), ("面積を正しく求めている", 2)],
               pit=["$x^2$ の係数 " + f"${abs(a)}$" + " をかけ忘れる。", "(下)−(上) で積分して負の値を答える。"],
               chk=(f"Abs(integrate(({py(*cs)})-(({m})*x+({n})), [x, {al}, {be}]))", fp(S)))


@gen("standard_practice", 3, ["computation", "condition_check"])
def b_cubic_interval(r):
    while True:
        p, q = sorted(r.sample(range(-3, 4), 2))
        if (p + q) % 2 == 0:
            break
    a = r.choice([1, -1])
    d = r.randint(-5, 5)
    cs = [2 * a, -3 * a * (p + q), 6 * a * p * q, d]
    lo = r.randint(p - 2, p)
    hi = r.randint(max(lo + 2, p + 1), q + 2)
    cands = sorted({lo, hi} | {x for x in (p, q) if lo <= x <= hi})
    vals = {x: ev(cs, x) for x in cands}
    M, m = max(vals.values()), min(vals.values())
    xM = [x for x in cands if vals[x] == M]
    xm = [x for x in cands if vals[x] == m]
    Fs = py(*cs)
    fx = lambda xs: "，".join(f"x={x}" for x in xs)  # noqa: E731
    inside = [x for x in (p, q) if lo <= x <= hi]
    return sa(f"関数 $f(x)={poly(*cs)}$ の定義域を ${lo}\\leqq x\\leqq {hi}$ に制限する。このとき $f(x)$ の最大値と最小値、およびそれらをとる $x$ の値を求めなさい。",
              f"最大値 ${M}$（${fx(xM)}$）、最小値 ${m}$（${fx(xm)}$）",
              f"$f'(x)={6 * a}{fac(p)}{fac(q)}$。区間内の極値をとる点と区間の両端の値を比べる。", d=3,
              ap="閉区間での最大・最小は「区間内の極値」と「区間の両端の値」の比較で決まる。極値だけで判断しない。",
              steps=[f"$f'(x)={poly(6 * a, -6 * a * (p + q), 6 * a * p * q)}={6 * a}{fac(p)}{fac(q)}$。",
                     ("区間内にある $f'(x)=0$ の解：" + "、".join(f"$x={x}$" for x in inside)) if inside else "区間内に $f'(x)=0$ の解はない。",
                     "候補の値：" + "、".join(f"$f({x})={v}$" for x, v in vals.items()), f"最大値 ${M}$、最小値 ${m}$。"],
              alt=["増減表を区間の範囲だけでかき、矢印の向きから最大・最小の候補を絞ってから値を計算する方法でもよい。"],
              pc=[("$f'(x)$ を求め、区間内の極値をとる点を調べている", 1), ("候補の点の値を正しく計算している", 1), ("最大・最小とそのときの $x$ を正しく答えている", 2)],
              pit=["極大値をそのまま最大値と答え、端点の値との比較を忘れる。", "区間外にある極値の点を候補に入れてしまう。"],
              chk=(f"[Max({', '.join(at(Fs, x) for x in cands)}), Min({', '.join(at(Fs, x) for x in cands)})]", f"[{fp(M)}, {fp(m)}]", None, "intermediate"))


# (表示, 2 の指数, 3 の指数, 10 の指数)
RATIOS = [("1.2", 2, 1, -1), ("1.5", -1, 1, 0), ("1.08", 2, 3, -2), ("1.44", 4, 2, -2), ("1.6", 4, 0, -1), ("1.8", 1, 2, -1),
          ("0.8", 3, 0, -1), ("0.9", 0, 2, -1), ("0.6", 1, 1, -1), ("0.75", -2, 1, 0), ("0.96", 5, 1, -2), ("0.72", 3, 2, -2)]
TARGETS_UP = [("2", 1, 0, 0), ("3", 0, 1, 0), ("10", 0, 0, 1), ("100", 0, 0, 2), ("6", 1, 1, 0), ("5", -1, 0, 1)]
TARGETS_DOWN = [("\\dfrac{1}{2}", -1, 0, 0), ("\\dfrac{1}{10}", 0, 0, -1), ("\\dfrac{1}{100}", 0, 0, -2), ("\\dfrac{1}{3}", 0, -1, 0), ("\\dfrac{1}{5}", 1, 0, -1)]
CTX_UP = [("ある地域で栽培している植物（架空）の株数は、1年ごとに {r} 倍に増える", "年"),
          ("ある会員制サービス（架空）の会員数は、1か月ごとに {r} 倍に増える", "か月"),
          ("ある細胞の培養実験（架空）では、細胞の数が1日ごとに {r} 倍になる", "日")]
CTX_DOWN = [("ある薬品（架空）の体内濃度は、1時間ごとに {r} 倍に減少する", "時間"),
            ("ある放射性物質（架空）の量は、1日ごとに {r} 倍に減少する", "日"),
            ("ある機械（架空）の価値は、1年ごとに {r} 倍に下がる", "年")]


@gen("standard_practice", 4, ["application", "computation", "condition_check"])
def b_log_growth(r):
    while True:
        rs, i, j, k = r.choice(RATIOS)
        up = F(2) ** i * F(3) ** j * F(10) ** k > 1
        ts, ti, tj, tk = r.choice(TARGETS_UP if up else TARGETS_DOWN)
        Lr = i * LOG2 + j * LOG3 + k
        Lt = ti * LOG2 + tj * LOG3 + tk
        q = Lt / Lr
        if q <= 1:
            continue
        n = int(q) + 1
        if q == int(q) or q - int(q) < Decimal("0.03") or n > 60:
            continue
        ratio = F(2) ** i * F(3) ** j * F(10) ** k
        T = F(2) ** ti * F(3) ** tj * F(10) ** tk
        ok = (ratio ** n > T and ratio ** (n - 1) <= T) if up else (ratio ** n < T and ratio ** (n - 1) >= T)
        if ok:
            break
    ctx, unit = r.choice(CTX_UP if up else CTX_DOWN)
    ctx = ctx.format(r=rs)
    goal = f"初めて最初の ${ts}$ 倍を超える" if up else f"初めて最初の ${ts}$ 倍より小さくなる"
    rel = ">" if up else "<"
    Lrs, Lts = f"{Lr:.4f}", f"{Lt:.4f}"
    return num(f"{ctx}とする。最初の状態から数えて、{goal}のは何{unit}後か。$\\log_{{10}}2=0.3010,\\ \\log_{{10}}3=0.4771$ を用いて求めなさい。",
               str(n), f"$n$ {unit}後に $({rs})^n{rel}{ts}$。両辺の常用対数をとって $n\\times({Lrs}){rel}{Lts}$。" + ("" if up else "$\\log_{10}" + rs + "<0$ で割るので不等号の向きが変わる。"), d=3,
               disp=f"{n}{unit}後",
               ap="「初めて〜を超える（下回る）」は、指数不等式を満たす最小の自然数 $n$ を求める問題。常用対数をとって一次不等式にする。",
               steps=[f"条件は $({rs})^n{rel}{ts}$。", f"$\\log_{{10}}{rs}={Lrs}$、$\\log_{{10}}{ts}={Lts}$（2・3・10 に分解して計算）。",
                      f"$n\\times({Lrs}){rel}{Lts}$ より $n>{Lts}\\div({Lrs})={(Lt / Lr):.3f}\\cdots$" + ("（負の数で割ったので向きが変わる）" if not up else "") + "。",
                      f"最小の自然数は $n={n}$。"],
               alt=[f"$n={n - 1}$ のとき ${n - 1}\\times({Lrs})$ は ${Lts}$ を{'超えない' if up else '下回らない'}ことを確認し、$n={n}$ が境目であることを確かめる。"],
               pc=[("条件を指数不等式で表している", 1), ("対数の値を正しく計算している", 1), ("不等号の向きに注意して最小の自然数を求めている", 2)],
               pit=["$\\log_{10}" + rs + "$ を計算するとき、小数点の位置の分（$10$ の累乗で割った分）を引き忘れる。",
                    "負の数で割ったときに不等号の向きを変え忘れる。" if not up else "割り算の結果の小数を四捨五入して、境目の自然数を1つ小さく答える。"],
               chk=(f"floor(({Lts})/({Lrs}))+1", str(n)))


SYN = [  # (alpha, R)
    (sp.pi / 6, 2), (sp.pi / 3, 2), (2 * sp.pi / 3, 2), (5 * sp.pi / 6, 2), (-sp.pi / 6, 2), (-sp.pi / 3, 2),
    (sp.pi / 4, sp.sqrt(2)), (3 * sp.pi / 4, sp.sqrt(2)), (-sp.pi / 4, sp.sqrt(2)), (sp.pi / 6, 4), (sp.pi / 3, 4), (-sp.pi / 4, 2 * sp.sqrt(2))]
INTERVALS = [(0, sp.pi, "0\\leqq\\theta\\leqq\\pi"), (0, sp.pi / 2, "0\\leqq\\theta\\leqq\\dfrac{\\pi}{2}"), (sp.pi / 2, sp.pi, "\\dfrac{\\pi}{2}\\leqq\\theta\\leqq\\pi"),
             (-sp.pi / 2, sp.pi / 2, "-\\dfrac{\\pi}{2}\\leqq\\theta\\leqq\\dfrac{\\pi}{2}")]


def synth_data(alpha, R, lo, hi):
    a = sp.nsimplify(R * sp.cos(alpha))
    b = sp.nsimplify(R * sp.sin(alpha))
    cands = {lo, hi}
    for kk in range(-3, 4):
        for base in (sp.pi / 2, 3 * sp.pi / 2):
            t = base - alpha + 2 * kk * sp.pi
            if lo <= t <= hi:
                cands.add(sp.nsimplify(t))
    vals = {t: sp.nsimplify(R * sp.sin(t + alpha)) for t in cands}
    M = max(vals.values(), key=lambda v: float(v))
    m = min(vals.values(), key=lambda v: float(v))
    tM = sorted([t for t in cands if sp.simplify(vals[t] - M) == 0], key=float)
    tm = sorted([t for t in cands if sp.simplify(vals[t] - m) == 0], key=float)
    expr = f"{coef_tex(a, True)}\\sin\\theta{coef_tex(b)}\\cos\\theta"
    return a, b, sorted(cands, key=float), vals, M, m, tM, tm, expr


def theta_tex(ts):
    return "，".join(f"\\theta={sp.latex(t)}" for t in ts)


@gen("standard_practice", 3, ["computation", "condition_check"])
def b_trig_synth(r):
    alpha, R = r.choice(SYN)
    lo, hi, rng = r.choice(INTERVALS)
    a, b, cands, vals, M, m, tM, tm, expr = synth_data(alpha, R, lo, hi)
    vs = ", ".join(f"({a})*sin({t})+({b})*cos({t})" for t in cands)
    return sa(f"関数 $y={expr}\\ \\left({rng}\\right)$ について、最大値と最小値、およびそれらをとる $\\theta$ の値を求めなさい。",
              f"最大値 ${lt(M)}$（${theta_tex(tM)}$）、最小値 ${lt(m)}$（${theta_tex(tm)}$）",
              f"$y={lt(R)}\\sin\\left(\\theta{'+' if float(alpha) > 0 else '-'}{sp.latex(abs(alpha))}\\right)$ と合成し、$\\theta{'+' if float(alpha) > 0 else '-'}{sp.latex(abs(alpha))}$ の範囲で考える。", d=3,
              ap="$\\sin$ と $\\cos$ が混ざった1次式は合成して1つの $\\sin$ にまとめる。その後、角の動く範囲を単位円で確認する。",
              steps=[f"$y={lt(R)}\\sin\\left(\\theta{'+' if float(alpha) > 0 else '-'}{sp.latex(abs(alpha))}\\right)$。",
                     f"${rng}$ より $\\theta{'+' if float(alpha) > 0 else '-'}{sp.latex(abs(alpha))}$ は ${sp.latex(lo + alpha)}$ から ${sp.latex(hi + alpha)}$ まで動く。",
                     "候補の値：" + "、".join(f"$\\theta={sp.latex(t)}$ で ${lt(vals[t])}$" for t in cands), f"最大値 ${lt(M)}$、最小値 ${lt(m)}$。"],
              alt=["$y'=" + f"{coef_tex(a, True)}\\cos\\theta{coef_tex(-b)}\\sin\\theta" + "$ の符号を調べて増減から最大・最小を求めることもできる（数学Ⅲの方法）。端点と、合成で求めた角での値を比べるだけでも確認できる。"],
              pc=[("正しく合成している", 1), ("角の範囲を正しく求めている", 1), ("最大値・最小値とそのときの $\\theta$ を正しく答えている", 2)],
              pit=["角の範囲を確認せず、最大値 " + f"${lt(R)}$" + "・最小値 " + f"${lt(-R)}$" + " と答える。", "合成の角 $\\alpha$ の符号を誤る。"],
              chk=(f"[Max({vs}), Min({vs})]", f"[{M}, {m}]", None, "intermediate"))


@gen("standard_practice", 3, ["computation", "condition_check"])
def b_trig_quad(r):
    form = r.choice(["sin", "cos"])
    k = r.choice([-3, -2, -1, 1, 2, 3])
    c = r.randint(-2, 2)
    if form == "sin":
        A, B, C = F(-2), F(2 * k), F(1 + c)
    else:
        A, B, C = F(2), F(2 * k), F(-1 + c)
    s0 = -B / (2 * A)
    cands = sorted({F(-1), F(1)} | ({s0} if -1 <= s0 <= 1 else set()))
    g = lambda s: A * s * s + B * s + C  # noqa: E731
    vals = {s: g(s) for s in cands}
    M, m = max(vals.values()), min(vals.values())
    cst = "" if c == 0 else (f"+{c}" if c > 0 else f"{c}")
    expr = f"\\cos2\\theta{'+' if 2 * k > 0 else ''}{2 * k}\\{form}\\theta{cst}"
    gtex = f"{poly(int(A), int(B), int(C), var='t')}"
    where = "頂点が範囲内にある" if -1 <= s0 <= 1 else "頂点が範囲外にある"
    return sa(f"$0\\leqq\\theta<2\\pi$ のとき、関数 $y={expr}$ の最大値と最小値を求めなさい。（誘導：$t=\\{form}\\theta$ とおき、$y$ を $t$ の式で表す。）",
              f"最大値 ${ft(M)}$、最小値 ${ft(m)}$",
              f"$\\cos2\\theta={'1-2\\sin^2\\theta' if form == 'sin' else '2\\cos^2\\theta-1'}$ より $y={gtex}$、$-1\\leqq t\\leqq1$。{where}。", d=3,
              ap="2倍角の公式で $\\cos2\\theta$ を $\\" + form + "\\theta$ で表すと、$t$ の二次関数になる。置き換えたら $t$ の範囲を必ず書く。",
              steps=[f"$\\cos2\\theta={'1-2t^2' if form == 'sin' else '2t^2-1'}$（$t=\\{form}\\theta$）。", f"$y={gtex}$、$-1\\leqq t\\leqq1$。",
                     f"軸 $t={ft(s0)}$（{where}）。", "候補：" + "、".join(f"$t={ft(s)}$ で ${ft(v)}$" for s, v in vals.items()), f"最大値 ${ft(M)}$、最小値 ${ft(m)}$。"],
              alt=["$t$ の二次関数のグラフを $-1\\leqq t\\leqq1$ の部分だけかき、最も高い点と低い点を読み取って確かめる。"],
              pc=[("2倍角の公式で $t$ の二次関数に直している", 1), ("$t$ の範囲を書いている", 1), ("最大値・最小値を正しく求めている", 2)],
              pit=["$t$ の範囲を考えずに頂点の値を答える。", "$\\cos2\\theta=1-2\\sin^2\\theta$ と $2\\cos^2\\theta-1$ を取り違える。"],
              chk=(f"[Max({', '.join(f'({fp(A)})*({fp(s)})**2+({fp(B)})*({fp(s)})+({fp(C)})' for s in cands)}), Min({', '.join(f'({fp(A)})*({fp(s)})**2+({fp(B)})*({fp(s)})+({fp(C)})' for s in cands)})]",
                   f"[{fp(M)}, {fp(m)}]", None, "intermediate"))


LOG_EQ = [(2, 3, [(8, 1), (4, 2)]), (5, 2, [(25, 1)]), (2, 1, [(2, 1)]), (3, 1, [(3, 1)]), (2, 4, [(16, 1), (8, 2)]), (2, 5, [(32, 1), (16, 2), (8, 4)]), (3, 2, [(9, 1)]), (3, 3, [(27, 1), (9, 3)]), (3, 4, [(81, 1), (27, 3)]),
          (2, 2, [(4, 1)]), (2, 6, [(64, 1), (32, 2), (16, 4)])]


@gen("standard_practice", 3, ["condition_check", "computation"])
def b_log_eq(r):
    base, k, pairs = r.choice([e for e in LOG_EQ if any(u_ - v_ <= 15 for u_, v_ in e[2])])
    u, v = r.choice([uv for uv in pairs if uv[0] - uv[1] <= 15])
    p = r.randint(-3, 5)
    q = p + (u - v)
    x1, x2 = p + u, p - v
    t1 = "x" if p == 0 else f"x{'-' if p > 0 else '+'}{abs(p)}"
    t2 = "x" if q == 0 else f"x{'-' if q > 0 else '+'}{abs(q)}"
    return sa(f"方程式 $\\log_{{{base}}}({t1})+\\log_{{{base}}}({t2})={k}$ を解きなさい。（真数条件の確認を答案に書くこと。）",
              f"$x={x1}$", f"真数条件 $x>{q}$。$({t1})({t2})={base}^{k}={base ** k}$ の解 $x={x1},\\ {x2}$ のうち、条件を満たすのは $x={x1}$。", d=3, v=[f"x={x1}"],
              ap="対数の方程式は、最初に真数条件（真数 $>0$）で $x$ の範囲を確定させてから、対数をはずして解く。",
              steps=[f"真数条件：${t1}>0$ かつ ${t2}>0$ より $x>{q}$。", f"左辺 $=\\log_{{{base}}}({t1})({t2})$ なので $({t1})({t2})={base ** k}$。",
                     f"展開・整理して因数分解すると ${fac(x1)}{fac(x2)}=0$、$x={x1},\\ {x2}$。", f"$x>{q}$ を満たすのは $x={x1}$。"],
              alt=[f"$x={x2}$ を元の式に代入すると、真数 ${x2 - p}$ が負になり $\\log$ が定義されないことを確かめる。"],
              pc=[("真数条件を正しく書いている", 1), ("対数をはずして二次方程式をつくっている", 1), ("条件に合う解だけを答えている", 2)],
              pit=[f"二次方程式の解 $x={x2}$ も答えに含める。", "$\\log_a M+\\log_a N=\\log_a(M+N)$ と誤って変形する。"],
              chk=(f"solve(({t1.replace('x', 'x')})*({t2})-{base ** k}, x)", f"[{x1}, {x2}]", "set", "intermediate"))


# ======================================================================
# C 思考力・記述応用
# ======================================================================

@gen("thinking_writing", 3, ["cross_unit", "written_reasoning"], rel=["HS-MATH2-U02", "HS-MATH2-U06"])
def c_three_roots(r):
    p, q = sorted(r.sample(range(-3, 4), 2))
    d = r.randint(-4, 4)
    cs = [2, -3 * (p + q), 6 * p * q, d]
    Mx, mn = ev(cs, p), ev(cs, q)
    Fs = py(*cs)
    return desc(f"$k$ を定数とする。$x$ の方程式 ${poly(*cs)}=k$ について、次の問いに答えなさい。\n(1) 異なる3つの実数解をもつような $k$ の値の範囲を求めなさい。\n(2) 異なる実数解がちょうど2個となる $k$ の値をすべて求めなさい。\n考え方がわかるように記述すること。",
                f"(1) ${mn}<k<{Mx}$　(2) $k={Mx},\\ {mn}$",
                f"$f(x)={poly(*cs)}$ とおくと、実数解の個数は $y=f(x)$ と $y=k$ の共有点の個数。$f'(x)=6{fac(p)}{fac(q)}$ より極大値 $f({p})={Mx}$、極小値 $f({q})={mn}$。",
                [("定数を分離し、グラフの共有点の個数に言いかえている", 2), ("$f'(x)$ を求めて増減を調べ、極大値・極小値を正しく求めている", 3),
                 ("(1) の範囲を正しく答えている", 2), ("(2) の値を正しく答えている", 1)], d=4, p=8, lines=10,
                ap="文字 $k$ を右辺に分離すると、$k$ を含まない曲線 $y=f(x)$ と、$x$ 軸に平行な直線 $y=k$ の共有点の問題になる（高次方程式の実数解の個数をグラフで数える）。",
                steps=[f"$f(x)={poly(*cs)}$ とおく。", f"$f'(x)={poly(6, -6 * (p + q), 6 * p * q)}=6{fac(p)}{fac(q)}$。",
                       f"増減表より、$x={p}$ で極大値 ${Mx}$、$x={q}$ で極小値 ${mn}$。",
                       f"(1) 直線 $y=k$ と3点で交わるのは ${mn}<k<{Mx}$。", f"(2) 直線が極大・極小の点を通るとき接するので共有点は2個：$k={Mx},\\ {mn}$。"],
                alt=["$g(x)=f(x)-k$ として、「極大値 $>0$ かつ 極小値 $<0$」という条件（極値の積が負）から (1) を導くこともできる。"],
                pc=[("定数分離による言いかえ", 2), ("増減と極値", 3), ("(1) の範囲", 2), ("(2) の値", 1)],
                pit=["$f'(x)=0$ の解（$x$ 座標）を $k$ の範囲の端と取り違える。", "(1) で等号を含めてしまう（接する場合は解が2個）。"],
                chk=(f"[{at(Fs, p)}, {at(Fs, q)}]", f"[{fp(Mx)}, {fp(mn)}]", None, "intermediate"))


@gen("thinking_writing", 2, ["written_reasoning", "application"])
def c_area_min(r):
    s = r.randint(-3, 3)
    h = r.choice([1, 4, 9, 16])
    c0 = r.randint(-2, 2)
    py0 = s * s + c0 + h
    S = F(4, 3) * F(int(h ** 0.5) ** 3)
    curve = f"x^2{'+' if c0 > 0 else ''}{c0 if c0 else ''}"
    msq = "m^2" if s == 0 else f"({lin(2 * s, 'm')})^2"
    return desc(f"放物線 $C:\\ y={curve}$ と、点 $\\mathrm{{A}}({s},\\,{py0})$ を通る傾き $m$ の直線 $\\ell$ を考える。\n太郎：「点 A は放物線の上側（内側）にあるから、$m$ がどんな値でも $\\ell$ は $C$ と2点で交わりそうだね。」\n花子：「囲まれた部分の面積 $S$ を $m$ で表して、最小値を調べてみよう。」\n$\\ell$ と $C$ が常に2点で交わることを示し、$S$ の最小値とそのときの $m$ の値を求めなさい。",
                f"$m={2 * s}$ のとき最小値 $S={ft(S)}$",
                f"交点の $x$ 座標 $\\alpha<\\beta$ について $(\\beta-\\alpha)^2={msq}+{4 * h}$。$S=\\dfrac{{(\\beta-\\alpha)^3}}{{6}}$ は $m={2 * s}$ で最小。",
                [("判別式を計算し、常に2点で交わることを示している", 2), ("$S=\\dfrac{(\\beta-\\alpha)^3}{6}$ を用い、$(\\beta-\\alpha)^2$ を $m$ で表している", 3),
                 ("最小となる $m$ と最小値を正しく求めている", 3)], d=4, p=8, lines=12,
                ap="面積は交点の $x$ 座標の差 $\\beta-\\alpha$ だけで決まる（$\\dfrac{1}{6}$ 公式）。$(\\beta-\\alpha)^2$ を解と係数の関係で $m$ の式にすれば、二次関数の最小値の問題になる。",
                steps=[f"$\\ell:\\ y=m{fac(s)}+{py0}$。$C$ の式と連立して整理すると $x^2-mx{smx(s)}-{s * s + h}=0$。",
                       f"判別式 $D=m^2-4({smx(s, True)}-{s * s + h})={msq}+{4 * h}>0$ なので、常に異なる2点で交わる。",
                       f"解と係数の関係より $(\\beta-\\alpha)^2=D={msq}+{4 * h}$。",
                       f"$S=\\dfrac{{(\\beta-\\alpha)^3}}{{6}}=\\dfrac{{D^{{3/2}}}}{{6}}$ は $D$ が最小のとき最小。$m={2 * s}$ で $D={4 * h}$。",
                       f"最小値 $S=\\dfrac{{({4 * h})^{{3/2}}}}{{6}}={ft(S)}$。"],
                alt=[f"$m={2 * s}$ は、点 A の真下にある $C$ 上の点 $({s},\\,{s * s + c0})$ における接線の傾き $2\\times({s})$ と等しい。つまり、最小になるのは $\\ell$ がその接線と平行になるときだと図形的に解釈できる。"],
                pc=[("常に2点で交わることの証明", 2), ("$(\\beta-\\alpha)^2$ の式", 3), ("最小値と $m$", 3)],
                pit=["$S$ を $m$ で表す前に $\\alpha,\\ \\beta$ を解の公式で求めて計算が複雑になり、時間を失う。", "$D^{3/2}$ の計算で $(4h)^{3/2}$ を $4h^{3/2}$ とする。"],
                chk=(f"Rational(1,6)*({4 * h})**Rational(3,2)", fp(S), None, "intermediate"))


@gen("thinking_writing", 2, ["cross_unit", "condition_check", "written_reasoning"], rel=["HS-MATH2-U04", "HS-MATH2-U06"])
def c_trig_cubic(r):
    fn = r.choice(["sin", "cos"])
    k = r.choice([F(1), F(-1), F(1, 2), F(-1, 2)])
    A = r.choice([2, -2]) if k.denominator == 2 else r.choice([1, 2, -1, -2])
    c = r.randint(-3, 3)
    a3, a2 = 2 * A, -3 * A * k
    cands = sorted({F(-1), F(0), k, F(1)})
    g = lambda t: a3 * t ** 3 + a2 * t * t + c  # noqa: E731
    vals = {t: g(t) for t in cands}
    M, m = max(vals.values()), min(vals.values())

    def term(co, pw, first=False):
        co = F(co)
        if co == 0:
            return ""
        mag = "" if abs(co) == 1 else ft(abs(co))
        sign = "-" if co < 0 else ("" if first else "+")
        return f"{sign}{mag}\\{fn}^{pw}\\theta"
    cst = "" if c == 0 else (f"+{c}" if c > 0 else f"{c}")
    expr = term(a3, 3, True) + term(a2, 2) + cst
    gtex = poly(int(a3), int(a2), 0, c, var="t")
    Ft = f"({fp(a3)})*t**3+({fp(a2)})*t**2+({c})"
    return desc(f"$0\\leqq\\theta<2\\pi$ のとき、関数 $y={expr}$ の最大値と最小値を求めなさい。$t=\\{fn}\\theta$ とおいて考え、$t$ の範囲に注意して記述すること。",
                f"最大値 ${ft(M)}$、最小値 ${ft(m)}$",
                f"$y={gtex}\\ (-1\\leqq t\\leqq1)$。$\\dfrac{{dy}}{{dt}}={ft(6 * A)}t(t{'-' if k > 0 else '+'}{ft(abs(k))})$ より、候補 $t={', '.join(ft(t) for t in cands)}$ の値を比べる。",
                [("$t=\\" + fn + "\\theta$ とおき、$-1\\leqq t\\leqq1$ を明記している", 2), ("$t$ で微分して増減を調べている", 3), ("端点を含めて比較し、最大値・最小値を正しく求めている", 3)], d=4, p=8, lines=10,
                ap="三角関数の3次式は、$t=\\" + fn + "\\theta$ とおくと $t$ の三次関数になる（三角関数と微分法の融合）。定義域は $t$ の範囲 $-1\\leqq t\\leqq1$。",
                steps=[f"$t=\\{fn}\\theta$ とおくと $-1\\leqq t\\leqq1$、$y={gtex}$。", f"$\\dfrac{{dy}}{{dt}}={ft(6 * A)}t^2{'-' if 6 * A * k > 0 else '+'}{ft(abs(6 * A * k))}t={ft(6 * A)}t(t{'-' if k > 0 else '+'}{ft(abs(k))})$、$t=0,\\ {ft(k)}$ で極値。",
                       "候補の値：" + "、".join(f"$t={ft(t)}$ で ${ft(v)}$" for t, v in vals.items()), f"最大値 ${ft(M)}$、最小値 ${ft(m)}$。"],
                alt=["$-1\\leqq t\\leqq1$ における増減表をかき、矢印の向きから候補を絞ってから値を比べる。"],
                pc=[("置き換えと $t$ の範囲", 2), ("増減の調べ方", 3), ("最大値・最小値", 3)],
                pit=["$t$ の範囲を書かず、$t$ の三次関数の極値をそのまま最大・最小とする。", "端点 $t=\\pm1$ の値を比較に入れ忘れる。"],
                chk=(f"[Max({', '.join(Ft.replace('t', f'({fp(t)})') for t in cands)}), Min({', '.join(Ft.replace('t', f'({fp(t)})') for t in cands)})]",
                     f"[{fp(M)}, {fp(m)}]", None, "intermediate"))


@gen("thinking_writing", 3, ["cross_unit", "application", "written_reasoning"], rel=["HS-MATH2-U05", "HS-MATH1-U05"])
def c_loglog(r):
    b = r.choice([F(1, 2), F(3, 2), F(2), F(3), F(-1), F(-2), F(1, 3)])
    C = r.choice([2, 3, 4, 5, 6, 8])
    if b.denominator == 2:
        ms = [0, 2, 4]
    elif b.denominator == 3:
        ms = [0, 3, 6]
    else:
        ms = sorted(r.sample([0, 1, 2, 3], 3))
    xs = [F(10) ** mm for mm in ms]
    ys = [C * F(10) ** int(b * mm) for mm in ms]
    rows = [[f"${dec(x)}$", f"${dec(y)}$"] for x, y in zip(xs, ys)]
    btex = ft(b)
    bexp = str(b.numerator) if b.denominator == 1 else f"\\frac{{{b.numerator}}}{{{b.denominator}}}"
    pts = "、".join(f"$({dec(x)},\\ {dec(y)})$" for x, y in zip(xs, ys))
    ans = f"$y={C}x^{{{bexp}}}$"
    m1, m2 = ms[0], ms[-1]
    return desc(f"ある実験（架空の資料）で2つの量 $x,\\ y$ を測定したところ、下の表の結果（$(x,\\ y)=$ {pts}）を得た。横軸に $X=\\log_{{10}}x$、縦軸に $Y=\\log_{{10}}y$ をとって点をかくと、3点は一直線上に並んだ。\n(1) $Y$ を $X$ の一次式で表しなさい。\n(2) $y$ を $x$ の式で表しなさい。また、両対数をとると直線になる理由を説明しなさい。",
                f"(1) $Y={btex}X+\\log_{{10}}{C}$　(2) {ans}。$y=Cx^b$ の両辺の常用対数をとると $\\log_{{10}}y=b\\log_{{10}}x+\\log_{{10}}C$ となり、$X,\\ Y$ の一次式だから。",
                f"傾き $b=\\dfrac{{\\log_{{10}}{dec(ys[-1])}-\\log_{{10}}{dec(ys[0])}}}{{{m2}-{m1}}}={btex}$、$X=0$ のとき $Y=\\log_{{10}}{C}$。",
                [("2点から直線の傾きを対数の性質で正しく求めている", 3), ("$Y$ 切片が $\\log_{10}" + f"{C}" + "$ であることを求め、(1) を答えている", 2),
                 ("$y$ を $x$ の式で表し、直線になる理由を対数の性質で説明している", 3)], d=4, p=8, lines=10,
                tbl=table(rows, header=["$x$", "$y$"], caption="測定結果（架空の資料）"),
                ap="べき関数 $y=Cx^b$ は、両辺の対数をとると $\\log y=b\\log x+\\log C$ と一次式になる（データの分析で学ぶ「変数変換して直線にのせる」考え方と対数の融合）。",
                steps=[f"$X={m1}$ のとき $Y=\\log_{{10}}{dec(ys[0])}$、$X={m2}$ のとき $Y=\\log_{{10}}{dec(ys[-1])}$。",
                       f"傾き $=\\dfrac{{\\log_{{10}}{dec(ys[-1])}-\\log_{{10}}{dec(ys[0])}}}{{{m2 - m1}}}=\\dfrac{{\\log_{{10}}10^{{{int(b * (m2 - m1))}}}}}{{{m2 - m1}}}={btex}$。",
                       f"$Y={btex}X+\\beta$ に $X={m1},\\ Y=\\log_{{10}}{dec(ys[0])}$ を代入して $\\beta=\\log_{{10}}{C}$。",
                       f"$\\log_{{10}}y={btex}\\log_{{10}}x+\\log_{{10}}{C}=\\log_{{10}}{C}x^{{{bexp}}}$ より {ans}。"],
                alt=[f"表の残りの点 $x={dec(xs[1])}$ を {ans} に代入すると $y={dec(ys[1])}$ となり、3点すべてが式を満たすことで確かめられる。"],
                pc=[("傾き", 3), ("切片と (1)", 2), ("(2) の式と理由", 3)],
                pit=["傾きを $\\dfrac{y_2-y_1}{x_2-x_1}$（対数をとる前の値）で計算する。", "$\\log_{10}" + f"{C}" + "$ を切片として求めたのに、$y=x^b+" + f"{C}" + "$ のように足し算で表す。"],
                chk=(f"(log({fp(ys[-1])}, 10)-log({fp(ys[0])}, 10))/({m2 - m1})", fp(b), None, "intermediate"))


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(stem, wrong, step, etype, tempt, fix, ans, expl, steps, ap, alt, pit, chk=None, d=3):
    return desc(f"{stem}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい答えを求めなさい。", ans, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい解答を途中式とともに示している", 3), ("最終的な答えが正しい", 1)], d=d, p=6, lines=6,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい途中式", 3), ("正しい答え", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix), chk=chk)


@gen("error_correction", 3, ["common_error", "condition_check"])
def d_no_extreme(r):
    a = r.choice([1, 2, -1, -2])
    p = r.choice([-3, -2, -1, 1, 2, 3])
    c = r.randint(-5, 5)
    cs = [a, -3 * a * p, 3 * a * p * p, -a * p ** 3 + c]
    dps = poly(3 * a, -6 * a * p, 3 * a * p * p)
    sq = f"{3 * a}{fac(p)}^2"
    mono = "増加" if a > 0 else "減少"
    wrong = f"$f'(x)={dps}={sq}$。$f'(x)=0$ より $x={p}$。よって $f(x)$ は $x={p}$ で極値 ${c}$ をとる。"
    fix = f"$f'(x)={sq}$ は $x={p}$ の前後で符号が変わらない（常に $f'(x){'\\geqq' if a > 0 else '\\leqq'}0$）。$f(x)$ は常に{mono}し、極値をもたない。"
    return err_item(f"大問の(1)で「関数 $f(x)={poly(*cs)}$ の極値を調べよ」と問われた。", wrong, f"「$f'(x)=0$ より $x={p}$ で極値」と結論した部分", "concept",
                    "$f'(a)=0$ を極値の条件として覚えてしまい、符号の変化を確かめる手順（増減表）を省いている。2乗の形が出たのに符号を考えていない。",
                    fix, "極値をもたない", f"$f'(x)={sq}$ は $x\\neq{p}$ で常に{'正' if a > 0 else '負'}。",
                    [f"$f'(x)={sq}$。", f"$x<{p}$ でも $x>{p}$ でも $f'(x)$ は{'正' if a > 0 else '負'}。", f"符号が変わらないので $x={p}$ は極値をとる点ではない。$f(x)$ は単調に{mono}し、極値なし。"],
                    "極値は「$f'(x)=0$」ではなく「$f'(x)$ の符号の変化」で判定する。",
                    [f"$f(x)={'' if a == 1 else ('-' if a == -1 else a)}{fac(p)}^3{'+' if c >= 0 else ''}{c}$ と変形でき、$y={'' if a == 1 else ('-' if a == -1 else a)}x^3$ のグラフを平行移動したものなので極値をもたないと確かめられる。"],
                    ["$f'(x)=0$ の解を求めた後、必ず増減表で符号を確認する。"],
                    chk=(f"expand(diff({py(*cs)}, x))", f"{3 * a}*(x-({p}))**2", "expand", "intermediate"), d=3)


@gen("error_correction", 3, ["common_error", "computation"])
def d_area_sign(r):
    a = r.randint(1, 4)
    b = a + r.randint(1, 3)
    s = r.choice([1, -1])
    cs = [s, -s * a, 0]
    student = abs(F(s) * (F(b) ** 3 / 3 - F(a) * b * b / 2))
    S1 = F(a) ** 3 / 6
    S2 = abs(F(b) ** 3 / 3 - F(a) * b * b / 2 - (F(a) ** 3 / 3 - F(a) ** 3 / 2))
    S = S1 + S2
    if student == S:
        b += 1
        student = abs(F(s) * (F(b) ** 3 / 3 - F(a) * b * b / 2))
        S2 = abs(F(b) ** 3 / 3 - F(a) * b * b / 2 - (F(a) ** 3 / 3 - F(a) ** 3 / 2))
        S = S1 + S2
    Fs = py(*cs)
    wrong = f"$S=\\left|\\displaystyle\\int_0^{{{b}}}({poly(*cs)})\\,dx\\right|=\\left|{'' if s > 0 else '-'}\\left(\\dfrac{{{b}^3}}{{3}}-\\dfrac{{{a}\\cdot{b}^2}}{{2}}\\right)\\right|={ft(student)}$"
    fix = f"$0\\leqq x\\leqq{a}$ と ${a}\\leqq x\\leqq{b}$ で曲線と $x$ 軸の上下が入れかわるので分けて積分し、$S={ft(S1)}+{ft(S2)}={ft(S)}$"
    return err_item(f"曲線 $y={poly(*cs)}$ と $x$ 軸、および直線 $x={b}$ で囲まれた2つの部分の面積の和 $S$ を求めなさい。", wrong, "区間 $0\\leqq x\\leqq" + f"{b}" + "$ をまとめて積分した部分", "sign",
                    f"定積分を「面積を求める計算」と思いこみ、$x$ 軸の下にある部分では定積分が負になることを忘れている。絶対値をつければ面積になると考えてしまう。",
                    fix, f"$S={ft(S)}$", f"曲線は $x={a}$ で $x$ 軸と交わり、上下が入れかわる。上下が入れかわる区間ごとに積分して和をとる。",
                    [f"$y={poly(*cs)}={'' if s > 0 else '-'}x(x-{a})$ は $x=0,\\ {a}$ で $x$ 軸と交わる。",
                     f"$0\\leqq x\\leqq{a}$ では $y{'\\leqq' if s > 0 else '\\geqq'}0$：面積 ${ft(S1)}$（$\\dfrac{{1}}{{6}}$ 公式）。",
                     f"${a}\\leqq x\\leqq{b}$ では $y{'\\geqq' if s > 0 else '\\leqq'}0$：面積 ${ft(S2)}$。", f"$S={ft(S)}$。"],
                    "面積は「上下関係が変わらない区間ごと」に定積分する。まず $x$ 軸との交点を求めて区間を分ける。",
                    ["グラフの略図をかき、$x$ 軸の上と下にある部分を色分けすると、まとめて積分すると打ち消し合うことが一目でわかる。"],
                    ["区間内で $x$ 軸と交わるかどうかを確認せずに積分する。"],
                    chk=(f"Abs(integrate({Fs}, [x, 0, {a}]))+Abs(integrate({Fs}, [x, {a}, {b}]))", fp(S)), d=3)


@gen("error_correction", 2, ["common_error", "condition_check"])
def d_log_base(r):
    a = r.choice([2, 3])
    m = r.choice([-3, -2, -1, 1, 2])
    p = r.randint(-3, 4)
    rel = r.choice([">", "<"])
    B = F(1, a) ** m
    t = "x" if p == 0 else f"x{'-' if p > 0 else '+'}{abs(p)}"
    tl = "x" if p == 0 else f"({t})"
    bnd = ft(B + p)
    if rel == ">":
        wrong = f"$\\log_{{\\frac{{1}}{{{a}}}}}{tl}>{m}=\\log_{{\\frac{{1}}{{{a}}}}}{ft(B)}$ より ${t}>{ft(B)}$。よって $x>{bnd}$。"
        ans = f"${p}<x<{bnd}$"
        fix = f"底 $\\dfrac{{1}}{{{a}}}<1$ なので不等号の向きが変わり ${t}<{ft(B)}$。真数条件 ${t}>0$ と合わせて {ans}。"
        ck = ("真数条件 $" + t + ">0$ も同時に必要。")
    else:
        wrong = f"$\\log_{{\\frac{{1}}{{{a}}}}}{tl}<{m}=\\log_{{\\frac{{1}}{{{a}}}}}{ft(B)}$ より ${t}<{ft(B)}$。真数条件と合わせて ${p}<x<{bnd}$。"
        ans = f"$x>{bnd}$"
        fix = f"底 $\\dfrac{{1}}{{{a}}}<1$ なので不等号の向きが変わり ${t}>{ft(B)}$。これは真数条件も満たすので {ans}。"
        ck = "このとき真数条件は自動的に満たされる。"
    return err_item(f"不等式 $\\log_{{\\frac{{1}}{{{a}}}}}{tl}{rel}{m}$ を解きなさい。", wrong, "対数をはずして真数の大小に直した部分", "condition",
                    "底が1より大きい場合と同じ感覚で、対数をはずすときに不等号の向きをそのままにしている。底 $\\dfrac{1}{" + f"{a}" + "}$ の関数 $y=\\log_{\\frac{1}{" + f"{a}" + "}}x$ は減少関数である。",
                    fix, ans, f"$y=\\log_{{\\frac{{1}}{{{a}}}}}x$ は減少関数なので、真数の大小は対数の大小と逆になる。{ck}",
                    [f"真数条件：${t}>0$。", f"${m}=\\log_{{\\frac{{1}}{{{a}}}}}{ft(B)}$ と右辺を同じ底の対数で表す。",
                     f"底 $\\dfrac{{1}}{{{a}}}<1$ より、${t}{'<' if rel == '>' else '>'}{ft(B)}$。", f"真数条件と合わせて {ans}。"],
                    "対数をはずす前に「底と1の大小」と「真数条件」の2つを確認する。",
                    [f"底の変換で $\\log_{{\\frac{{1}}{{{a}}}}}X=-\\log_{a}X$ と直し、$\\log_{a}{tl}{'<' if rel == '>' else '>'}{-m}$ として底が1より大きい形で解いても同じ結果になる。"],
                    ["底が1より小さいときに不等号の向きを変え忘れる。", "真数条件を最後の範囲に反映させ忘れる。"],
                    chk=(f"Rational(1,{a})**({m})+({p})", fp(B + p), None, "intermediate"), d=3)


@gen("error_correction", 2, ["common_error", "condition_check"])
def d_trig_range(r):
    while True:
        alpha, R = r.choice(SYN)
        lo, hi, rng = r.choice(INTERVALS)
        a, b, cands, vals, M, m, tM, tm, expr = synth_data(alpha, R, lo, hi)
        if sp.simplify(M - R) != 0 or sp.simplify(m + R) != 0:
            break
    sgn_ = "+" if float(alpha) > 0 else "-"
    al = sp.latex(abs(alpha))
    wrong = f"$y={lt(R)}\\sin\\left(\\theta{sgn_}{al}\\right)$ で、$-1\\leqq\\sin\\left(\\theta{sgn_}{al}\\right)\\leqq1$ だから、最大値 ${lt(R)}$、最小値 ${lt(-R)}$。"
    vs = ", ".join(f"({a})*sin({t})+({b})*cos({t})" for t in cands)
    return err_item(f"関数 $y={expr}\\ \\left({rng}\\right)$ の最大値と最小値を求めなさい。", wrong, "$\\sin$ の値の範囲を $-1$ から $1$ とした部分", "condition",
                    "合成までは正しくできたので安心し、$\\theta$ に範囲の制限があることを見落としている。$\\sin$ がどんな角でも $-1$ から $1$ のすべての値をとれると思いこんでいる。",
                    f"$\\theta{sgn_}{al}$ は ${sp.latex(lo + alpha)}$ から ${sp.latex(hi + alpha)}$ まで動く。この範囲で最大値 ${lt(M)}$、最小値 ${lt(m)}$。",
                    f"最大値 ${lt(M)}$（${theta_tex(tM)}$）、最小値 ${lt(m)}$（${theta_tex(tm)}$）",
                    "合成した角 $\\theta+\\alpha$ の範囲を単位円上で確認すると、$\\sin$ の値は一部の範囲しかとらない。",
                    [f"合成：$y={lt(R)}\\sin\\left(\\theta{sgn_}{al}\\right)$。", f"角の範囲：${sp.latex(lo + alpha)}\\leqq\\theta{sgn_}{al}\\leqq{sp.latex(hi + alpha)}$。",
                     "候補：" + "、".join(f"$\\theta={sp.latex(t)}$ で ${lt(vals[t])}$" for t in cands), f"最大値 ${lt(M)}$、最小値 ${lt(m)}$。"],
                    "角に範囲の制限があるときは、合成した角の範囲を単位円上に図示してから最大・最小を読む。",
                    ["区間の両端と、区間内で $\\sin$ が $\\pm1$ になる角での値をすべて計算して比べると確実に求められる。"],
                    ["$\\theta$ の範囲を $\\theta+\\alpha$ の範囲に直し忘れる。"],
                    chk=(f"[Max({vs}), Min({vs})]", f"[{M}, {m}]", None, "intermediate"), d=3)


GENERATORS = [a_extreme, a_tangent, a_log_value, a_digits, a_trig_graph, a_integral,
              b_area, b_cubic_interval, b_log_growth, b_trig_synth, b_trig_quad, b_log_eq,
              c_three_roots, c_area_min, c_trig_cubic, c_loglog,
              d_no_extreme, d_area_sign, d_log_base, d_trig_range]
