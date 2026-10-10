"""単元パック：数学Ⅱ 複素数と方程式（複素数・解と係数の関係・剰余の定理と因数定理・高次方程式）。"""
from fractions import Fraction
from math import isqrt

from banks._common import desc, mc, num, sa
from hs_pack_lib import (board, check, definition, example, fr_py, frac, gen, guide, intro, lesson, nonzero, poly, summary,
                         theorem, tp)

UNIT_ID = "HS-MATH2-U02"


# ----------------------------------------------------------------------
# 補助
# ----------------------------------------------------------------------

def pmul(p, q):
    out = [0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return out


def ppy(p):
    d = len(p) - 1
    return "(" + "+".join(f"({c})*x**{d - i}" for i, c in enumerate(p)) + ")"


def peval(p, t):
    v = 0
    for c in p:
        v = v * t + c
    return v


def fprod(p, q):
    """(x-p)(x-q) の表記（p=0 なら x(x-q)）。"""
    if p == 0:
        return f"x({xm(q)})"
    if q == 0:
        return f"x({xm(p)})"
    return f"({xm(p)})({xm(q)})"


def la(p):
    """p*a+b の表記。"""
    return "b" if p == 0 else ("a+b" if p == 1 else ("-a+b" if p == -1 else f"{p}a+b"))


def at(expr, v):
    return expr.replace("x", f"({v})")


def cx(p, q):
    """複素数 p+qi の LaTeX（整数）。"""
    if q == 0:
        return str(p)
    im = "i" if q == 1 else ("-i" if q == -1 else f"{q}i")
    if p == 0:
        return im
    return f"{p}{im}" if q < 0 else f"{p}+{im}"


def cxp(p, q):
    return f"({p})+({q})*I"


def shift(v):
    return f"+{v}" if v > 0 else f"{v}"


def xm(t):
    """x-t の表記。"""
    return "x" if t == 0 else f"x{shift(-t)}"


def ftex(f):
    f = Fraction(f)
    return frac(f.numerator, f.denominator)


def fstr(f):
    f = Fraction(f)
    return str(f.numerator) if f.denominator == 1 else f"{f.numerator}/{f.denominator}"


def sqrt_tex(k):
    """√k（k>0 整数）を簡約した LaTeX。"""
    out, inner = 1, k
    for d in range(2, isqrt(k) + 1):
        while inner % (d * d) == 0:
            inner //= d * d
            out *= d
    if inner == 1:
        return str(out)
    return ("" if out == 1 else str(out)) + f"\\sqrt{{{inner}}}"


def pm_root(t):
    """x^2=t の解 ±… の LaTeX。"""
    if t > 0:
        return f"\\pm {sqrt_tex(t)}"
    s = sqrt_tex(-t)
    return "\\pm i" if s == "1" else f"\\pm {s}i"


def quad_roots(h, k):
    """(x-h)^2 = -k の解、すなわち x^2-2hx+(h^2+k)=0 の解の LaTeX と sympy 表記。"""
    if k == 0:
        return f"{h}", [f"{h}"]
    if k < 0:
        s = sqrt_tex(-k)
        tex = (f"{h}" if h else "") + f"\\pm {s}"
        return tex, [f"{h}+sqrt({-k})", f"{h}-sqrt({-k})"]
    s = sqrt_tex(k)
    im = "i" if s == "1" else f"{s}i"
    tex = (f"{h}" if h else "") + f"\\pm {im}"
    return tex, [f"{h}+sqrt({k})*I", f"{h}-sqrt({k})*I"]


LESSON = lesson(
    goals=["虚数単位 $i$ を用いて複素数の四則計算を行い、負の数の平方根を正しく扱える。",
           "二次方程式の解を複素数の範囲で求め、判別式で解の種類を判別できる。",
           "解と係数の関係を導き、対称式の値の計算や2数を解とする方程式の作成に使える。",
           "剰余の定理・因数定理を除法の関係式から導き、高次方程式を因数分解して解ける。"],
    duration=100,
    readiness=["二次方程式の解の公式と判別式（数学Ⅰ）を使える。", "整式の除法 $A=BQ+R$（式と証明）を理解している。", "平方根の計算と分母の有理化ができる。"],
    flow=[("導入：数の範囲を広げる", 10, "x^2=-1 が実数解をもたないことを確認し、2乗して -1 になる数 i を導入する"),
          ("複素数の計算", 20, "相等・四則計算・共役複素数を扱い、例題1で除法（分母の実数化）を行う"),
          ("二次方程式と判別式", 15, "解の公式を複素数の範囲に広げ、D の符号で解の種類を判別する"),
          ("解と係数の関係", 20, "解の公式から関係を導き、例題2で対称式の値を求める"),
          ("剰余の定理・因数定理と高次方程式", 30, "A=BQ+R から剰余の定理を導き、例題3で3次方程式を解く"),
          ("まとめと確認", 5, "確認問題3問、問題プリントAの課題指示")],
    sections=[
        intro("in1", "2乗して $-1$ になる数",
              "実数は2乗すると必ず $0$ 以上になるので、方程式 $x^2=-1$ は実数の範囲には解をもたない。そこで、2乗すると $-1$ になる新しい数を1つ考え、それを $i$ で表す。$i$ を実数と同じように文字式の計算規則にしたがって扱うと、すべての二次方程式が解をもつようになる。",
              bullets=["$i^2=-1$ を満たす数 $i$ を虚数単位という。", "$a+bi$（$a,\\ b$ は実数）の形の数を複素数といい、実数（$b=0$）も複素数に含まれる。"],
              points=[tp("数の範囲を自然数→整数→有理数→実数と広げてきた歴史と、方程式が解をもつようにするための拡張という見方を結びつける。", ask="$x+3=1$ や $2x=1$ が解をもつために、数の範囲をどう広げてきたか。", expect="負の数、分数を導入した。", timing="導入の冒頭"),
                      tp("$i$ は「実数ではない数」であり、大小関係（$i>0$ など）は考えないことを最初に確認する。", caution="$i>0$ と思い込む生徒がいる。")]),
        definition("df1", "複素数とその相等・共役",
                   "$a,\\ b$ を実数として $a+bi$ と表される数を複素数といい、$a$ を実部、$b$ を虚部という。$b\\neq0$ のものを虚数、$a=0,\\ b\\neq0$ のものを純虚数という。$a+bi$ に対し $a-bi$ を共役な複素数といい、$\\overline{a+bi}$ で表す。",
                   formula="$$a+bi=c+di\\iff a=c\\ \\text{かつ}\\ b=d\\qquad(a,\\ b,\\ c,\\ d\\ \\text{は実数})$$",
                   conditions=["相等の条件は $a,\\ b,\\ c,\\ d$ が実数のときに限って使える", "$a>0$ のとき $\\sqrt{-a}=\\sqrt{a}\\,i$ と定める", "$(a+bi)(a-bi)=a^2+b^2$ は実数（分母の実数化に使う）"],
                   points=[tp("$\\sqrt{-2}\\sqrt{-3}$ は $\\sqrt{2}i\\cdot\\sqrt{3}i=-\\sqrt{6}$ であり、$\\sqrt{(-2)(-3)}=\\sqrt{6}$ ではないことを必ず扱う。", caution="$\\sqrt{a}\\sqrt{b}=\\sqrt{ab}$ は $a,\\ b\\geqq0$ のときの性質。"),
                           tp("相等の条件を使う前に「$x,\\ y$ は実数」という前提を確認させる。", ask="$x,\\ y$ が実数でないと、なぜ実部と虚部を比べられないのか。")]),
        example("ex1", "例題1　複素数の除法",
                "$\\dfrac{3+i}{1-2i}$ を $a+bi$ の形で表せ。",
                ["分母の共役複素数 $1+2i$ を分母・分子に掛ける。", "分子：$(3+i)(1+2i)=3+6i+i+2i^2=1+7i$。", "分母：$(1-2i)(1+2i)=1-4i^2=5$。", "$\\dfrac{1+7i}{5}=\\dfrac{1}{5}+\\dfrac{7}{5}i$。"],
                "$\\dfrac{1}{5}+\\dfrac{7}{5}i$",
                thinking="分母を実数にするために、分母と共役な複素数を分母・分子に掛ける（分母の有理化と同じ発想）。",
                points=[tp("$i^2=-1$ におきかえるタイミングを毎回声に出させる。", ask="$2i^2$ はいくつか。", expect="$-2$")],
                misconceptions=[("分母の $(1-2i)(1+2i)$ を $1-4=-3$ とする", "$-(2i)^2=-4i^2=+4$ なので $1+4=5$")]),
        theorem("th1", "二次方程式の解と判別式",
                "$$ax^2+bx+c=0\\ \\Longrightarrow\\ x=\\dfrac{-b\\pm\\sqrt{b^2-4ac}}{2a}$$",
                ["$a,\\ b,\\ c$ は実数、$a\\neq0$", "$D=b^2-4ac>0$：異なる2つの実数解、$D=0$：重解、$D<0$：異なる2つの虚数解", "虚数解は互いに共役な複素数になる"],
                body="複素数の範囲で考えると、$D<0$ のときも $\\sqrt{D}=\\sqrt{-D}\\,i$ として解の公式がそのまま使える。",
                points=[tp("数学Ⅰでは「$D<0$ なら解なし」と学んだが、ここでは「実数解はないが虚数解が2つある」と言い直させる。")]),
        theorem("th2", "解と係数の関係",
                "$$ax^2+bx+c=0\\ \\text{の2つの解を}\\ \\alpha,\\ \\beta\\ \\text{とすると}\\quad \\alpha+\\beta=-\\dfrac{b}{a},\\quad \\alpha\\beta=\\dfrac{c}{a}$$",
                ["$a\\neq0$（係数は複素数でも成り立つが、ここでは実数で扱う）", "重解のときは $\\alpha=\\beta$ として成り立つ", "$\\alpha,\\ \\beta$ を解とする二次方程式の1つは $x^2-(\\alpha+\\beta)x+\\alpha\\beta=0$"],
                proof=["解の公式より $\\alpha=\\dfrac{-b+\\sqrt{D}}{2a},\\ \\beta=\\dfrac{-b-\\sqrt{D}}{2a}$（$D=b^2-4ac$）とおける。",
                       "和：$\\alpha+\\beta=\\dfrac{-2b}{2a}=-\\dfrac{b}{a}$。",
                       "積：$\\alpha\\beta=\\dfrac{(-b)^2-(\\sqrt{D})^2}{4a^2}=\\dfrac{b^2-(b^2-4ac)}{4a^2}=\\dfrac{c}{a}$。",
                       "$D<0$ のときも $(\\sqrt{D})^2=D$ が成り立つので、同じ計算で関係が得られる。"],
                points=[tp("和の符号にマイナスがつくことを、$a(x-\\alpha)(x-\\beta)$ を展開して $x$ の係数を比べる方法でも確認させる。", ask="$a(x-\\alpha)(x-\\beta)$ を展開すると $x$ の係数は何か。", expect="$-a(\\alpha+\\beta)$"),
                        tp("$\\alpha^2+\\beta^2=(\\alpha+\\beta)^2-2\\alpha\\beta$ など、対称式は基本対称式 $\\alpha+\\beta,\\ \\alpha\\beta$ で表せることを示す。")]),
        example("ex2", "例題2　対称式の値",
                "$2x^2-4x+3=0$ の2つの解を $\\alpha,\\ \\beta$ とするとき、$\\alpha^3+\\beta^3$ の値を求めよ。",
                ["解と係数の関係より $\\alpha+\\beta=2,\\ \\alpha\\beta=\\dfrac{3}{2}$。",
                 "$\\alpha^3+\\beta^3=(\\alpha+\\beta)^3-3\\alpha\\beta(\\alpha+\\beta)$。", "$=8-3\\cdot\\dfrac{3}{2}\\cdot2=8-9=-1$。"],
                "$-1$",
                thinking="解を具体的に求める（虚数になる）よりも、和と積だけで表す方が速く確実。",
                points=[tp("解が虚数でも、和と積は実数になることに注目させる。")]),
        theorem("th3", "剰余の定理・因数定理",
                "$$P(x)\\ \\text{を}\\ x-\\alpha\\ \\text{で割った余りは}\\ P(\\alpha)\\qquad P(\\alpha)=0\\iff P(x)\\ \\text{は}\\ x-\\alpha\\ \\text{で割り切れる}$$",
                ["$ax-b$ で割った余りは $P\\left(\\dfrac{b}{a}\\right)$", "因数定理：$P(\\alpha)=0$ ならば $P(x)$ は $x-\\alpha$ を因数にもつ", "整数係数で最高次の係数が1のとき、整数の解の候補は定数項の約数"],
                proof=["$P(x)$ を1次式 $x-\\alpha$ で割った商を $Q(x)$、余りを $R$ とすると、余りの次数は $0$ 以下なので $R$ は定数で、$P(x)=(x-\\alpha)Q(x)+R$。",
                       "この等式は $x$ についての恒等式なので、$x=\\alpha$ を代入できて $P(\\alpha)=0\\cdot Q(\\alpha)+R=R$。",
                       "したがって余りは $P(\\alpha)$（剰余の定理）。",
                       "特に $P(\\alpha)=0$ と $R=0$（割り切れる）は同値である（因数定理）。"],
                points=[tp("「$x+2$ で割る」ときは $x=-2$ を代入する。$x-\\alpha$ の形に直して $\\alpha$ を読む習慣をつけさせる。", caution="$x=2$ を代入する誤りが典型（問題プリントD）。")]),
        example("ex3", "例題3　3次方程式",
                "方程式 $x^3-3x^2+4x-2=0$ を解け。",
                ["$P(x)=x^3-3x^2+4x-2$ とおくと $P(1)=1-3+4-2=0$。", "因数定理より $P(x)$ は $x-1$ で割り切れ、$P(x)=(x-1)(x^2-2x+2)$。",
                 "$x^2-2x+2=0$ を解くと $x=1\\pm\\sqrt{1-2}=1\\pm i$。"],
                "$x=1,\\ 1\\pm i$",
                thinking="定数項 $-2$ の約数 $\\pm1,\\ \\pm2$ を代入して $P(\\alpha)=0$ となる $\\alpha$ を探す。",
                points=[tp("2次の因数が実数の範囲で因数分解できなくても、複素数の範囲では解をもつ。答えに虚数解を書き落とさないよう指導する。")],
                misconceptions=[("$x^2-2x+2=0$ は判別式が負なので「解なし」とし、答えを $x=1$ のみとする", "複素数の範囲で解くので $x=1\\pm i$ も解")]),
        board("bd1", "板書案",
              [("① 複素数", ["$i^2=-1$、$a+bi$（$a,b$ 実数）", "相等：実部どうし・虚部どうし", "$\\dfrac{3+i}{1-2i}=\\dfrac{(3+i)(1+2i)}{5}$", "$\\sqrt{-2}\\sqrt{-3}=-\\sqrt{6}$ に注意"]),
               ("② 解と係数の関係", ["$D<0$：異なる2つの虚数解", "$\\alpha+\\beta=-\\dfrac{b}{a}$、$\\alpha\\beta=\\dfrac{c}{a}$", "$\\alpha^3+\\beta^3=(\\alpha+\\beta)^3-3\\alpha\\beta(\\alpha+\\beta)$"]),
               ("③ 剰余・因数定理", ["$P(x)=(x-\\alpha)Q(x)+R$", "余り $R=P(\\alpha)$", "$P(1)=0$ → $(x-1)(x^2-2x+2)$", "$x=1,\\ 1\\pm i$"])],
              points=[tp("板書の③は「代入 → 割り算 → 2次方程式」の流れが一目で分かるよう矢印でつなぐ。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("複素数の計算は「$i$ を文字として計算し、$i^2$ が出たら $-1$」と1つの規則にまとめて指導する。"),
               tp("負の数の平方根は、計算の最初に $\\sqrt{-a}=\\sqrt{a}\\,i$ と書き直させる。", caution="先に根号どうしを掛けると符号を誤る。"),
               tp("解と係数の関係の符号（和は $-\\dfrac{b}{a}$）を、毎回 $a(x-\\alpha)(x-\\beta)$ と比較して確認させる。", timing="例題2の後"),
               tp("高次方程式の答えは、因数分解した各因数から出る解をすべて並べ、個数（重解を含めて次数と同じ）を確認させる。"),
               tp("「実数を係数とする方程式が虚数解 $p+qi$ をもてば共役な $p-qi$ も解」という性質は、係数が実数であることが前提だと強調する。")],
              misconceptions=[("$\\sqrt{-4}\\times\\sqrt{-9}=\\sqrt{36}=6$", "$2i\\times3i=6i^2=-6$"),
                              ("$x^2+3x+5=0$ の解の和を $3$ とする", "和は $-\\dfrac{b}{a}=-3$"),
                              ("$P(x)$ を $x+2$ で割った余りを $P(2)$ とする", "$x+2=x-(-2)$ なので $P(-2)$")]),
        summary("sm1", "まとめ",
                ["$i^2=-1$。複素数の相等は実部・虚部（実数）どうしで比べる。除法は分母の共役複素数を掛ける。",
                 "$D<0$ の二次方程式は異なる2つの虚数解（互いに共役）をもつ。",
                 "解と係数の関係：$\\alpha+\\beta=-\\dfrac{b}{a},\\ \\alpha\\beta=\\dfrac{c}{a}$。対称式は和と積で表す。",
                 "剰余の定理：余りは $P(\\alpha)$。因数定理で1次の因数を見つけて高次方程式を解く。"]),
        check("ck1", "確認問題",
              [("$(1+2i)^2$ を計算せよ。", "$1+4i+4i^2=-3+4i$"),
               ("$x^2+2x+4=0$ の2つの解を $\\alpha,\\ \\beta$ とするとき、$\\alpha^2+\\beta^2$ の値を求めよ。", "$(\\alpha+\\beta)^2-2\\alpha\\beta=4-8=-4$"),
               ("$P(x)=x^3+2x-5$ を $x+1$ で割った余りを求めよ。", "$P(-1)=-1-2-5=-8$")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

@gen("basic_check", 6, ["computation"])
def complex_arith(r):
    kind = r.choice(["mul", "mul", "div", "sq"])
    if kind == "mul":
        a, b, c, d = r.randint(-4, 5), nonzero(r, -4, 4), r.randint(-4, 5), nonzero(r, -4, 4)
        P, Q = a * c - b * d, a * d + b * c
        expr = f"({cx(a, b)})({cx(c, d)})"
        steps = [f"展開すると $({a * c})+({a * d})i+({b * c})i+({b * d})i^2$。",
                 f"$i^2=-1$ を代入して整理すると ${cx(P, Q)}$。"]
        chk = f"expand(({cxp(a, b)})*({cxp(c, d)}))"
        why = "分配法則で展開し、$i^2=-1$ におきかえる。"
    elif kind == "sq":
        a, b = nonzero(r, -4, 4), nonzero(r, -4, 4)
        P, Q = a * a - b * b, 2 * a * b
        expr = f"({cx(a, b)})^2"
        steps = [f"$(a+bi)^2=a^2+2abi+b^2i^2$ に $a={a},\\ b={b}$ を当てはめると ${a * a}{'+' if Q > 0 else ''}{Q}i+{b * b}i^2$。",
                 f"整理して ${cx(P, Q)}$。"]
        chk = f"expand(({cxp(a, b)})**2)"
        why = "乗法公式 $(a+b)^2$ と同様に展開し、$i^2=-1$ とする。"
    else:
        e, f = r.randint(-4, 4), nonzero(r, -4, 4)
        c, d = nonzero(r, -3, 3), nonzero(r, -3, 3)
        a, b = e * c - f * d, e * d + f * c
        P, Q = e, f
        N = c * c + d * d
        expr = f"\\dfrac{{{cx(a, b)}}}{{{cx(c, d)}}}"
        steps = [f"分母・分子に分母の共役複素数 ${cx(c, -d)}$ を掛ける。",
                 f"分母：$({cx(c, d)})({cx(c, -d)})={c * c}+{d * d}={N}$。",
                 f"分子：$({cx(a, b)})({cx(c, -d)})={cx(a * c + b * d, b * c - a * d)}$。", f"${N}$ で割って ${cx(P, Q)}$。"]
        chk = f"simplify(({cxp(a, b)})/({cxp(c, d)}))"
        why = "分母の共役複素数を分母・分子に掛けて、分母を実数にする。"
    return sa(f"次の計算をして、結果を $a+bi$（$a,\\ b$ は実数）の形で答えなさい。$${expr}$$", f"${cx(P, Q)}$", why, d=2,
              v=[cx(P, Q)],
              ap="$i$ を文字と同じように扱って計算し、$i^2$ が現れたら $-1$ におきかえる。" + ("除法は分母の共役複素数を掛けて分母を実数にする。" if kind == "div" else ""),
              steps=steps,
              alt=[f"検算：答え ${cx(P, Q)}$ に分母 ${cx(c, d)}$ を掛けると分子 ${cx(a, b)}$ にもどる。" if kind == "div" else "実部と虚部を別々に計算する公式 $(a+bi)(c+di)=(ac-bd)+(ad+bc)i$ に当てはめても同じ結果になる。"],
              pc=[("展開（または分母の実数化）を正しく行っている", 1), ("$i^2=-1$ を用いて正しく整理している", 1)],
              pit=["$i^2$ を $1$ として計算する。", "分母の実数化で、分子にだけ共役複素数を掛ける。" if kind == "div" else "虚部の符号を誤る。"],
              chk=(chk, cxp(P, Q)))


@gen("basic_check", 4, ["concept", "condition_check"])
def complex_equality(r):
    x, y = r.randint(-4, 4), r.randint(-4, 4)
    p, q = r.choice([(1, 1), (2, 1), (1, 2), (3, 1), (1, 3), (2, 3)])
    s, t = r.choice([(1, -1), (1, 2), (2, -1), (1, -2), (3, -1)])
    if p * t - q * s == 0:
        s, t = 1, -1
    R1, R2 = p * x + q * y, s * x + t * y

    def lf(a, b):
        out = ("x" if a == 1 else f"{a}x")
        out += ("+y" if b == 1 else "-y" if b == -1 else f"{'+' if b > 0 else ''}{b}y")
        return out
    return sa(f"$x,\\ y$ を実数とする。等式 $({lf(p, q)})+({lf(s, t)})i={cx(R1, R2)}$ が成り立つとき、$x,\\ y$ の値を求めなさい。",
              f"$x={x},\\ y={y}$",
              f"$x,\\ y$ は実数なので ${lf(p, q)},\\ {lf(s, t)}$ も実数。実部・虚部を比べて ${lf(p, q)}={R1}$、${lf(s, t)}={R2}$。", d=2,
              v=[f"x={x}, y={y}"],
              ap="複素数の相等「実部どうし・虚部どうしが等しい」を使う。そのためには、かっこ内が実数であること（$x,\\ y$ が実数）が前提になる。",
              steps=[f"$x,\\ y$ が実数なので、${lf(p, q)}$ と ${lf(s, t)}$ はともに実数。", f"実部：${lf(p, q)}={R1}$、虚部：${lf(s, t)}={R2}$。", f"連立して $x={x},\\ y={y}$。"],
              alt=[f"求めた値を代入して $({p * x + q * y})+({s * x + t * y})i={cx(R1, R2)}$ となることを確かめる。"],
              pc=[("実部・虚部を比べた連立方程式を立てている", 1), ("$x,\\ y$ を正しく求めている", 1)],
              pit=["$x,\\ y$ が実数であることを確認せずに実部・虚部を比べる。", "右辺の虚部の符号を読み違える。"],
              chk=(f"solve([{p}*x+({q})*y-({R1}), {s}*x+({t})*y-({R2})], [x, y])", f"{{x: {x}, y: {y}}}", None, "intermediate"))


@gen("basic_check", 5, ["concept", "computation"])
def root_kind(r):
    kind = r.choice(["real2", "double", "imag"])
    a = r.choice([1, 1, 2, 3, -1])
    if kind == "real2":
        r1, r2 = r.sample(range(-5, 6), 2)
        b, c = -a * (r1 + r2), a * r1 * r2
        if r.random() < 0.5:
            c -= a  # 整数解にならない実数解
            if b * b - 4 * a * c <= 0:
                c += a
    elif kind == "double":
        h = r.randint(-4, 4)
        b, c = -2 * a * h, a * h * h
    else:
        h, k = r.randint(-3, 3), r.randint(1, 5)
        b, c = -2 * a * h, a * (h * h + k)
    D = b * b - 4 * a * c
    lab = {"real2": "異なる2つの実数解", "double": "重解（実数解）", "imag": "異なる2つの虚数解"}
    ans = lab[kind]
    wrong = [v for k_, v in lab.items() if k_ != kind] + ["実数解も虚数解ももたない"]
    why = {lab["real2"]: ("異なる2つの実数解をもつのは $D>0$ のとき。この方程式では $D\\leqq0$。", "判別式の符号と解の種類の対応の誤り"),
           lab["double"]: ("重解をもつのは $D=0$ のとき。この方程式では $D\\neq0$。", "判別式の符号と解の種類の対応の誤り"),
           lab["imag"]: ("虚数解をもつのは $D<0$ のとき。この方程式では $D\\geqq0$。", "判別式の符号と解の種類の対応の誤り"),
           "実数解も虚数解ももたない": ("複素数の範囲では、二次方程式は必ず解（重解を含めて2つ）をもつ。", "「$D<0$ なら解なし」という数学Ⅰの言い方のまま考えている")}
    return mc(f"二次方程式 ${poly(a, b, c)}=0$ の解を複素数の範囲で考える。解の種類として正しいものを選びなさい。", [ans] + wrong,
              f"判別式 $D=({b})^2-4\\cdot({a})\\cdot({c})={D}$。" + {"real2": "$D>0$ なので異なる2つの実数解。", "double": "$D=0$ なので重解。", "imag": "$D<0$ なので異なる2つの虚数解。"}[kind], d=2,
              ap="解の公式の根号の中 $D=b^2-4ac$ の符号で、解が実数か虚数か、異なるか重なるかが決まる。",
              steps=[f"$D=b^2-4ac={b * b}-({4 * a * c})={D}$。", {"real2": "$D>0$ → 異なる2つの実数解。", "double": "$D=0$ → 重解。", "imag": "$D<0$ → $\\sqrt{D}$ が虚数になり、異なる2つの虚数解。"}[kind]],
              alt=["実際に解の公式で解を求めて確かめてもよい。" + ("$b$ が偶数なので $D/4=(b/2)^2-ac$ を使うと計算が楽になる。" if b % 2 == 0 else "")],
              pc=[("判別式を正しく計算している", 1), ("符号から解の種類を正しく判断している", 1)],
              why={w: why[w] for w in wrong}, chk=(f"({b})**2-4*({a})*({c})", str(D), None, "intermediate"))


SYM = [
    ("a2b2", "\\alpha^2+\\beta^2", lambda s, p: s * s - 2 * p, "(S)**2-2*(P)", "(\\alpha+\\beta)^2-2\\alpha\\beta"),
    ("inv", "\\dfrac{1}{\\alpha}+\\dfrac{1}{\\beta}", lambda s, p: s / p, "(S)/(P)", "\\dfrac{\\alpha+\\beta}{\\alpha\\beta}"),
    ("diff2", "(\\alpha-\\beta)^2", lambda s, p: s * s - 4 * p, "(S)**2-4*(P)", "(\\alpha+\\beta)^2-4\\alpha\\beta"),
    ("cube", "\\alpha^3+\\beta^3", lambda s, p: s ** 3 - 3 * p * s, "(S)**3-3*(P)*(S)", "(\\alpha+\\beta)^3-3\\alpha\\beta(\\alpha+\\beta)"),
    ("mix", "\\alpha^2\\beta+\\alpha\\beta^2", lambda s, p: p * s, "(P)*(S)", "\\alpha\\beta(\\alpha+\\beta)"),
    ("ratio", "\\dfrac{\\beta}{\\alpha}+\\dfrac{\\alpha}{\\beta}", lambda s, p: (s * s - 2 * p) / p, "((S)**2-2*(P))/(P)", "\\dfrac{(\\alpha+\\beta)^2-2\\alpha\\beta}{\\alpha\\beta}"),
]


@gen("basic_check", 5, ["computation"])
def symmetric_value(r):
    a = r.choice([1, 1, 2, 3])
    b, c = nonzero(r, -6, 6), nonzero(r, -6, 6)
    key, tex, f, py, form = r.choice(SYM)
    s, p = Fraction(-b, a), Fraction(c, a)
    val = f(s, p)
    return num(f"二次方程式 ${poly(a, b, c)}=0$ の2つの解を $\\alpha,\\ \\beta$ とする。${tex}$ の値を求めなさい。", fstr(val),
               f"解と係数の関係より $\\alpha+\\beta={ftex(s)},\\ \\alpha\\beta={ftex(p)}$。${tex}={form}={ftex(val)}$。", d=2, disp=f"${ftex(val)}$",
               ap="解そのものを求めず、解と係数の関係で和 $\\alpha+\\beta$ と積 $\\alpha\\beta$ を求め、式をこの2つで表す。",
               steps=[f"$\\alpha+\\beta=-\\dfrac{{b}}{{a}}={ftex(s)}$、$\\alpha\\beta=\\dfrac{{c}}{{a}}={ftex(p)}$。",
                      f"${tex}={form}$ と変形する。", f"代入して ${ftex(val)}$。"],
               alt=["解の公式で $\\alpha,\\ \\beta$ を具体的に求めて代入しても同じ値になる（虚数解の場合は計算が重く、誤りやすい）。"],
               pc=[("和と積を正しく求めている", 1), ("式を和と積で表して正しく計算している", 1)],
               pit=["$\\alpha+\\beta$ を $\\dfrac{b}{a}$ と符号を誤る。", "$\\alpha^2+\\beta^2=(\\alpha+\\beta)^2$ のように $-2\\alpha\\beta$ を落とす。"],
               chk=(py.replace("S", fr_py(s.numerator, s.denominator)).replace("P", fr_py(p.numerator, p.denominator)), fr_py(val.numerator, val.denominator)))


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 5, ["computation", "condition_check"])
def remainder_thm(r):
    deg = r.choice([3, 3, 4])
    P = [r.choice([1, 2, -1, 3])] + [r.randint(-5, 5) for _ in range(deg)]
    if r.random() < 0.65:
        t = Fraction(nonzero(r, -3, 3))
        dv = xm(int(t))
    else:
        a = r.choice([2, 3])
        b = r.choice([v for v in range(-5, 6) if v % a != 0])
        t = Fraction(b, a)
        dv = f"{a}x{shift(-b)}"
    val = peval(P, t)
    return num(f"整式 $P(x)={poly(*P)}$ を ${dv}$ で割ったときの余りを求めなさい。", fstr(val),
               f"剰余の定理より、余りは $P\\left({ftex(t)}\\right)={ftex(val)}$。", d=3, disp=f"${ftex(val)}$",
               ap=f"1次式で割った余りは定数。${dv}=0$ となる $x={ftex(t)}$ を $P(x)$ に代入すれば、実際に割り算をしなくても余りが求まる（剰余の定理）。",
               steps=[f"${dv}=0$ となる $x$ は $x={ftex(t)}$。", f"$P(x)=({dv})Q(x)+R$ に $x={ftex(t)}$ を代入すると $R=P\\left({ftex(t)}\\right)$。",
                      f"$P\\left({ftex(t)}\\right)={ftex(val)}$。"],
               alt=[f"実際に ${dv}$ で割り算（筆算）をして余りを求め、一致することを確かめる。"],
               pc=[("代入する値を正しく決めている", 2), ("代入の計算を正しく行っている", 2)],
               pit=["$x+a$ で割るときに $x=a$ を代入する（符号の誤り）。", "$ax-b$ で割るときに $x=b$ を代入する。"],
               chk=(at(ppy(P), fr_py(t.numerator, t.denominator)), fr_py(val.numerator, val.denominator)))


@gen("standard_practice", 5, ["computation"])
def cubic_solve(r):
    while True:
        rt = nonzero(r, -3, 3)
        h = r.randint(-2, 2)
        k = r.choice([1, 4, 9, 2, 3, -1, -4, 1, 4])
        roots_tex, roots_py = quad_roots(h, k)
        if k < 0 and rt in (h + isqrt(-k), h - isqrt(-k)):
            continue
        break
    Qd = [1, -2 * h, h * h + k]
    P = pmul([1, -rt], Qd)
    lead = r.choice([1, 1, 2])
    P = [lead * c for c in P]
    cands = sorted({d for d in range(1, abs(P[-1]) + 1) if P[-1] % d == 0})
    return sa(f"3次方程式 ${poly(*P)}=0$ を、複素数の範囲で解きなさい。", f"$x={rt},\\ {roots_tex}$",
              f"$x={rt}$ を代入すると左辺が $0$ になるので、因数定理より ${xm(rt)}$ を因数にもつ。",
              d=3, v=[f"x={rt}, {roots_tex}"],
              ap="3次式を因数分解するために、因数定理を使って1次の因数を見つける。整数解の候補は定数項の約数" + ("（最高次の係数が1でないときは、定数項の約数を最高次の係数の約数で割った数）" if lead != 1 else "") + "。",
              steps=[f"$P(x)={poly(*P)}$ とおく。定数項 ${P[-1]}$ の約数 $\\pm" + ",\\ \\pm".join(map(str, cands[:4])) + f"$ などを代入し、$P({rt})=0$ を見つける。",
                     f"$P(x)$ を ${xm(rt)}$ で割って $P(x)={'' if lead == 1 else lead}({xm(rt)})({poly(*Qd)})$。",
                     f"${poly(*Qd)}=0$ を解の公式で解くと $x={roots_tex}$。", f"解は $x={rt},\\ {roots_tex}$。"],
              alt=[f"組立除法で ${xm(rt)}$ による割り算を行うと、商 ${'' if lead == 1 else str(lead) + '('}{poly(*Qd)}{'' if lead == 1 else ')'}$ が速く求まる。"],
              pc=[("因数定理で1次の因数を見つけている", 1), ("正しく因数分解している", 1), ("2次方程式を複素数の範囲で正しく解いている", 2)],
              pit=["2次の因数の判別式が負のとき「解なし」として虚数解を書き落とす。" if k > 0 else "2次の因数をさらに因数分解できるのに見落とす。", "割り算の計算で符号を誤る。"],
              chk=(f"solve({ppy(P)}, x)", "[" + ", ".join([str(rt)] + roots_py) + "]", "set", "intermediate"))


@gen("standard_practice", 5, ["condition_check", "computation"])
def remainder_two(r):
    A, B = nonzero(r, -4, 4), r.randint(-5, 5)
    p, q = r.sample([v for v in range(-3, 4)], 2)
    R1, R2 = A * p + B, A * q + B
    expanded = r.random() < 0.5
    dv = f"{poly(1, -(p + q), p * q)}" if expanded else f"{fprod(p, q)}"
    return sa(f"整式 $P(x)$ を ${xm(p)}$ で割ると余りが ${R1}$、${xm(q)}$ で割ると余りが ${R2}$ である。$P(x)$ を ${dv}$ で割ったときの余りを求めなさい。",
              f"${poly(A, B)}$",
              f"2次式で割った余りは1次以下なので $ax+b$ とおける。$P({p})={R1}$、$P({q})={R2}$ から $a,\\ b$ を決める。", d=3,
              v=[poly(A, B)],
              ap="割る式が2次式なので、余りは1次以下の式 $ax+b$ とおける。除法の関係式に、割る式が $0$ になる $x$ の値を代入する。",
              steps=[f"商を $Q(x)$、余りを $ax+b$ として $P(x)={fprod(p, q)}Q(x)+ax+b$。" + (f"（割る式は ${fprod(p, q)}$ と因数分解できる）" if expanded else ""),
                     f"剰余の定理より $P({p})={R1}$、$P({q})={R2}$。", f"$x={p}$：${la(p)}={R1}$、$x={q}$：${la(q)}={R2}$。",
                     f"連立して $a={A},\\ b={B}$。余り ${poly(A, B)}$。"],
              alt=[f"求めた余り ${poly(A, B)}$ に $x={p},\\ {q}$ を代入して、それぞれ ${R1},\\ {R2}$ になることを確かめる。"],
              pc=[("余りを $ax+b$ とおく理由（次数）を理解している", 1), ("剰余の定理から連立方程式を立てている", 2), ("余りを正しく求めている", 1)],
              pit=["余りを定数 $R$ とおいてしまう（2次式で割った余りは1次以下）。", "因数分解されていない割る式から $x$ の値を読み取れない。" if expanded else "代入する値の符号を誤る。"],
              chk=(f"solve([{p}*a+b-({R1}), {q}*a+b-({R2})], [a, b])", f"{{a: {A}, b: {B}}}", None, "intermediate"))


@gen("standard_practice", 5, ["computation", "concept"])
def biquadratic(r):
    t1, t2 = r.sample([1, 4, 9, 2, 3, -1, -4, -9, -2, -3, 16], 2)
    p, q = -(t1 + t2), t1 * t2
    ans = f"$x={pm_root(t1)},\\ {pm_root(t2)}$"
    teq = poly(1, p, q, var="t")
    return sa(f"4次方程式 ${poly(1, 0, p, 0, q)}=0$ を、複素数の範囲で解きなさい。",
              ans, f"$x^2=t$ とおくと ${teq}=0$、$(t{shift(-t1)})(t{shift(-t2)})=0$。", d=3,
              v=[ans.strip("$")],
              ap="$x^4$ と $x^2$ の項しかない（複2次式）ので、$x^2=t$ とおくと $t$ の2次方程式になる。",
              steps=[f"$x^2=t$ とおくと ${teq}=0$。",
                     f"$(t{shift(-t1)})(t{shift(-t2)})=0$ より $t={t1},\\ {t2}$。",
                     f"$x^2={t1}$ より $x={pm_root(t1)}$、$x^2={t2}$ より $x={pm_root(t2)}$。"],
              alt=[f"左辺を $(x^2{shift(-t1)})(x^2{shift(-t2)})$ と因数分解し、各因数を $0$ とおいて解いてもよい（虚数解は $x^2+a=(x+\\sqrt{{a}}i)(x-\\sqrt{{a}}i)$ と考える）。"],
              pc=[("$x^2=t$ とおいて $t$ の方程式を解いている", 2), ("$x$ の値（虚数解を含む4つ）をすべて正しく求めている", 2)],
              pit=["$x^2=" + str(min(t1, t2)) + "$ を「解なし」として虚数解を書き落とす。" if min(t1, t2) < 0 else "$x^2=t$ の解で $\\pm$ の一方を書き落とす。",
                   "$t$ の値をそのまま $x$ の解としてしまう。"],
              chk=(f"solve(x**4+({p})*x**2+({q}), x)", f"[sqrt({t1}), -sqrt({t1}), sqrt({t2}), -sqrt({t2})]", "set", "intermediate"))


# ======================================================================
# C 思考力・記述応用
# ======================================================================

@gen("thinking_writing", 3, ["written_reasoning", "condition_check"])
def complex_root_coef(r):
    p, q = r.randint(-2, 3), r.randint(1, 3)
    rt = nonzero(r, -4, 4)
    N = p * p + q * q
    A, B, Cc = -(2 * p + rt), N + 2 * p * rt, -rt * N
    return desc(f"$a,\\ b$ を実数の定数とする。3次方程式 $x^3+ax^2+bx{shift(Cc)}=0$ が $x={cx(p, q)}$ を解にもつとき、$a,\\ b$ の値と他の解を求めなさい。",
                f"$a={A},\\ b={B}$、他の解は $x={cx(p, -q)},\\ {rt}$",
                f"係数が実数なので、共役な ${cx(p, -q)}$ も解。この2つを解とする2次式 $x^2{shift(-2 * p) if p else ''}{'x' if p else ''}+{N}$ で左辺が割り切れることを使う。".replace("+1x", "+x").replace("-1x", "-x"),
                rubric=[("係数が実数であることから共役複素数も解であると述べている（または代入して実部・虚部を比較している）", 3),
                        ("$a,\\ b$ を正しく求めている", 3), ("他の解をすべて正しく求めている", 2)], d=4, p=8, lines=10,
                ap="実数係数の方程式が虚数解をもてば、その共役複素数も解になる。2つの虚数解を解とする2次式を作ると、左辺はそれで割り切れる。",
                steps=[f"係数が実数なので ${cx(p, -q)}$ も解。2解の和 ${2 * p}$、積 ${N}$ より、${poly(1, -2 * p, N)}$ は左辺の因数。",
                       f"定数項を比べて、左辺 $=({poly(1, -2 * p, N)})({xm(rt)})$（${N}\\times({-rt})={Cc}$）。",
                       f"展開して $x^3{shift(A) if A else ''}{'x^2' if A else ''}{shift(B) if B else ''}{'x' if B else ''}{shift(Cc)}$ より $a={A},\\ b={B}$。".replace("+1x", "+x").replace("-1x", "-x"),
                       f"他の解は $x={cx(p, -q)},\\ {rt}$。"],
                alt=[f"$x={cx(p, q)}$ を直接代入し、$({cx(p, q)})^2={cx(p * p - q * q, 2 * p * q)}$、$({cx(p, q)})^3={cx(p ** 3 - 3 * p * q * q, 3 * p * p * q - q ** 3)}$ を用いて実部・虚部がともに $0$ という連立方程式から $a,\\ b$ を求める方法もある（$a,\\ b$ が実数なので実部・虚部を比べられる）。"],
                pc=[("共役解の利用（または実部・虚部の比較）", 3), ("$a,\\ b$ の値", 3), ("他の解", 2)],
                pit=["係数が実数であることを確認せずに共役複素数を解とする。", "3つ目の実数解を求め忘れる。"],
                chk=(f"expand({ppy([1, -2 * p, N])}*(x-({rt})))",
                     f"x**3+({A})*x**2+({B})*x+({Cc})", "expand", "intermediate"))


TRANS = [
    ("shift", "\\alpha{k},\\ \\beta{k}", lambda s, p, k: (s + 2 * k, p + k * s + k * k)),
    ("scale", "{k}\\alpha,\\ {k}\\beta", lambda s, p, k: (k * s, k * k * p)),
    ("square", "\\alpha^2,\\ \\beta^2", lambda s, p, k: (s * s - 2 * p, p * p)),
    ("inv", "\\dfrac{{1}}{{\\alpha}},\\ \\dfrac{{1}}{{\\beta}}", lambda s, p, k: (s / p, 1 / p)),
    ("sumprod", "\\alpha+\\beta,\\ \\alpha\\beta", lambda s, p, k: (s + p, s * p)),
]


@gen("thinking_writing", 3, ["written_reasoning", "computation"])
def new_equation(r):
    b, c = r.randint(-5, 5), nonzero(r, -5, 5)
    key, tmpl, f = r.choice(TRANS)
    k = nonzero(r, -3, 3) if key == "shift" else r.choice([2, 3, -2, -1]) if key == "scale" else 0
    s, p = Fraction(-b), Fraction(c)
    S, P = f(s, p, k)
    from math import lcm
    L = lcm(S.denominator, P.denominator)
    coefs = [L, -S * L, P * L]
    coefs = [int(x) for x in coefs]
    if key == "shift":
        roots_tex = f"\\alpha{shift(k)},\\ \\beta{shift(k)}"
        rexpr = [f"solve(x**2+({b})*x+({c}),x)[{i}]+({k})" for i in (0, 1)]
    elif key == "scale":
        roots_tex = f"{'-' if k == -1 else k}\\alpha,\\ {'-' if k == -1 else k}\\beta"
        rexpr = [f"({k})*solve(x**2+({b})*x+({c}),x)[{i}]" for i in (0, 1)]
    elif key == "square":
        roots_tex = "\\alpha^2,\\ \\beta^2"
        rexpr = [f"solve(x**2+({b})*x+({c}),x)[{i}]**2" for i in (0, 1)]
    elif key == "inv":
        roots_tex = "\\dfrac{1}{\\alpha},\\ \\dfrac{1}{\\beta}"
        rexpr = [f"1/solve(x**2+({b})*x+({c}),x)[{i}]" for i in (0, 1)]
    else:
        roots_tex = "\\alpha+\\beta,\\ \\alpha\\beta"
        rexpr = [str(-b), str(c)]
    eq = f"{poly(*coefs)}=0"
    return desc(f"二次方程式 ${poly(1, b, c)}=0$ の2つの解を $\\alpha,\\ \\beta$ とするとき、${roots_tex}$ を2つの解とする二次方程式を1つ作りなさい（係数は整数とする）。",
                f"${eq}$",
                f"新しい2解の和は ${ftex(S)}$、積は ${ftex(P)}$。$x^2-(\\text{{和}})x+(\\text{{積}})=0$ を整数係数に直す。", rubric=[
                    ("解と係数の関係で $\\alpha+\\beta,\\ \\alpha\\beta$ を求めている", 2), ("新しい2解の和と積を $\\alpha+\\beta,\\ \\alpha\\beta$ で表して計算している", 4),
                    ("方程式を正しく作っている", 2)], d=4, p=8, lines=8,
                ap="2数 $u,\\ v$ を解とする二次方程式は $x^2-(u+v)x+uv=0$。新しい2解の和と積を、もとの方程式の $\\alpha+\\beta,\\ \\alpha\\beta$ で表す。",
                steps=[f"解と係数の関係より $\\alpha+\\beta={-b},\\ \\alpha\\beta={c}$。",
                       f"新しい2解の和：${ftex(S)}$、積：${ftex(P)}$。",
                       f"$x^2-({ftex(S)})x+({ftex(P)})=0$" + (f"。両辺を ${L}$ 倍して ${eq}$。" if L > 1 else f"、すなわち ${eq}$。")],
                alt=["もとの方程式の解を解の公式で具体的に求め、新しい2解を直接計算して $(x-u)(x-v)$ を展開しても確かめられる（虚数解でも同じ結果になる）。"],
                pc=[("和と積", 2), ("新しい2解の和と積", 4), ("方程式", 2)],
                pit=["$x^2+(\\text{和})x+(\\text{積})=0$ と和の符号を誤る。", "$\\alpha^2+\\beta^2$ を $(\\alpha+\\beta)^2$ とする。" if key == "square" else "新しい2解の積の計算で展開を誤る。"],
                chk=(f"expand(({L})*(x-({rexpr[0]}))*(x-({rexpr[1]})))", "+".join(f"({c_})*x**{2 - i}" for i, c_ in enumerate(coefs)), None, "intermediate"))


@gen("thinking_writing", 2, ["cross_unit", "condition_check", "written_reasoning"], rel=["HS-MATH1-U03"])
def sign_of_roots(r):
    s = r.randint(1, 4)
    c = s * (s + 1)
    kind = r.choice(["pos", "neg", "opp"])
    label = {"pos": "異なる2つの正の解", "neg": "異なる2つの負の解", "opp": "正の解と負の解を1つずつ"}[kind]
    ans = {"pos": f"$m>{s + 1}$", "neg": f"$-{c}<m<-{s}$", "opp": f"$m<-{c}$"}[kind]
    steps_k = {
        "pos": [f"$D/4=m^2-(m+{c})=(m-{s + 1})(m+{s})>0$ より $m<-{s},\\ {s + 1}<m$。", "$\\alpha+\\beta=2m>0$ より $m>0$。", f"$\\alpha\\beta=m+{c}>0$ より $m>-{c}$。", f"共通範囲は $m>{s + 1}$。"],
        "neg": [f"$D/4=(m-{s + 1})(m+{s})>0$ より $m<-{s},\\ {s + 1}<m$。", "$\\alpha+\\beta=2m<0$ より $m<0$。", f"$\\alpha\\beta=m+{c}>0$ より $m>-{c}$。", f"共通範囲は $-{c}<m<-{s}$。"],
        "opp": [f"異符号の2解をもつ条件は $\\alpha\\beta<0$ だけでよい（このとき $D/4=m^2-\\alpha\\beta>0$ は自動的に成り立つ）。", f"$\\alpha\\beta=m+{c}<0$ より $m<-{c}$。"],
    }[kind]
    return desc(f"$m$ を実数の定数とする。二次方程式 $x^2-2mx+m+{c}=0$ が{label}をもつような $m$ の値の範囲を求めなさい。",
                ans, f"2つの解を $\\alpha,\\ \\beta$ とし、判別式と解と係数の関係（和 $2m$、積 $m+{c}$）から条件を立てる。", rubric=[
                    ("必要な条件（判別式・和・積の符号）を過不足なく立てている", 4), ("各不等式を正しく解いている", 2), ("共通範囲を正しく求めている", 2)], d=4, p=8, lines=10,
                ap="解の符号の条件は、判別式（実数解をもつか）と、解と係数の関係による和・積の符号の組み合わせで表せる。二次関数のグラフ（数学Ⅰ）と $x$ 軸の交点の位置で考えることもできる。",
                steps=steps_k,
                alt=[f"二次関数 $f(x)=x^2-2mx+m+{c}$ のグラフ（数学Ⅰ）で考える：" + {"pos": f"軸 $x=m>0$、頂点の $y$ 座標 $<0$、$f(0)>0$ の3条件。", "neg": f"軸 $x=m<0$、頂点の $y$ 座標 $<0$、$f(0)>0$ の3条件。", "opp": "$f(0)<0$ の1条件。"}[kind] + "同じ範囲が得られる。"],
                pc=[("条件の設定", 4), ("各不等式の解", 2), ("共通範囲", 2)],
                pit=["判別式の条件だけで答える（解の符号の条件を忘れる）。" if kind != "opp" else "異符号の場合にも判別式・和の条件を加えて範囲を狭めてしまう。", "$D\\geqq0$ として重解の場合を含めてしまう。"],
                chk=(f"solve(m**2-m-{c}, m)", f"[{s + 1}, {-s}]", "set", "intermediate"))


@gen("thinking_writing", 2, ["written_reasoning", "condition_check"])
def xn_remainder(r):
    p, q = r.sample([-1, 0, 1, 2, 3, -2], 2)
    n = r.randint(5, 10) if max(abs(p), abs(q)) <= 2 else r.randint(4, 7)
    A = (p ** n - q ** n) // (p - q)
    B = (p * q ** n - q * p ** n) // (p - q)
    dv = poly(1, -(p + q), p * q)
    return desc(f"$x^{{{n}}}$ を ${dv}$ で割ったときの余りを求めなさい。",
                f"${poly(A, B)}$",
                f"${dv}={fprod(p, q)}$。余りを $ax+b$ とおき、$x={p},\\ {q}$ を代入して $a,\\ b$ を決める。", rubric=[
                    ("割る式を因数分解し、余りを $ax+b$ とおいている", 2), ("除法の関係式に適切な値を代入して連立方程式を立てている", 4), ("余りを正しく求めている", 2)], d=4, p=8, lines=8,
                ap=f"${n}$ 次式を実際に割るのは大変。商を $Q(x)$ とおいた除法の関係式に、割る式が $0$ になる $x$ を代入すると、$Q(x)$ を知らなくても余りが決まる。",
                steps=[f"$x^{{{n}}}={fprod(p, q)}Q(x)+ax+b$ とおく（余りは1次以下）。",
                       f"$x={p}$ を代入：${la(p)}={p ** n}$。", f"$x={q}$ を代入：${la(q)}={q ** n}$。",
                       f"連立して $a={A},\\ b={B}$。余りは ${poly(A, B)}$。"],
                alt=[f"検算：求めた余り ${poly(A, B)}$ に $x={p},\\ {q}$ を代入すると $({p})^{{{n}}}={p ** n}$、$({q})^{{{n}}}={q ** n}$ と一致する。"],
                pc=[("余りの形", 2), ("連立方程式", 4), ("答え", 2)],
                pit=["余りを定数とおいてしまう。", "負の数の累乗 $(" + str(min(p, q)) + ")^{" + str(n) + "}$ の符号を誤る。" if min(p, q) < 0 else "連立方程式の計算を誤る。"],
                chk=(f"solve([({p})*a+b-({p ** n}), ({q})*a+b-({q ** n})], [a, b])", f"{{a: {A}, b: {B}}}", None, "intermediate"))


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(stem, wrong, step, etype, tempt, fix, ans, expl, steps, ap, alt, pit, chk=None, d=3):
    return desc(f"{stem}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい答えを求めなさい。", ans, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい解答を途中式とともに示している", 3), ("最終的な答えが正しい", 1)], d=d, p=6, lines=6,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい途中式", 3), ("正しい答え", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix), chk=chk)


@gen("error_correction", 3, ["common_error", "concept"])
def err_complex(r):
    if r.random() < 0.5:
        s = r.choice([1, 2, 3, 5])
        u, v = r.sample([1, 2, 3, 4], 2)
        P, Q = s * u * u, s * v * v
        val = -s * u * v
        su, sv = sqrt_tex(P), sqrt_tex(Q)
        wrong = f"$\\sqrt{{-{P}}}\\times\\sqrt{{-{Q}}}=\\sqrt{{(-{P})\\times(-{Q})}}=\\sqrt{{{P * Q}}}={s * u * v}$"
        fix = f"$\\sqrt{{-{P}}}\\times\\sqrt{{-{Q}}}={su}i\\times{sv}i={val}$" if s == 1 else f"$\\sqrt{{-{P}}}\\times\\sqrt{{-{Q}}}={su}i\\times{sv}i={u * v}\\cdot{s}\\,i^2={val}$"
        return err_item(f"$\\sqrt{{-{P}}}\\times\\sqrt{{-{Q}}}$ を計算しなさい。", wrong, "1つ目の等号（根号どうしをまとめた部分）", "concept",
                        "$\\sqrt{a}\\sqrt{b}=\\sqrt{ab}$ を、$a,\\ b$ が負の場合にもそのまま使ってしまった。この性質は $a\\geqq0,\\ b\\geqq0$ のときにしか成り立たない。",
                        fix, f"${val}$",
                        f"負の数の平方根は、まず $\\sqrt{{-a}}=\\sqrt{{a}}\\,i$ と $i$ を用いて表してから計算する。",
                        [f"$\\sqrt{{-{P}}}={su}i$、$\\sqrt{{-{Q}}}={sv}i$。", f"積は ${su}\\cdot{sv}\\cdot i^2$。", f"$i^2=-1$ より ${val}$。"],
                        "$\\sqrt{}$ の中が負のときは、最初に $i$ を使った形に書き直す。",
                        [f"$\\sqrt{{-{P}}}$ と $\\sqrt{{-{Q}}}$ はどちらも純虚数なので、積は「純虚数×純虚数＝負の実数」になるはず。正の答え ${s * u * v}$ は符号の点で不自然と気づける。"],
                        ["$\\sqrt{a}\\sqrt{b}=\\sqrt{ab}$ を負の数に使う。"],
                        chk=(f"sqrt(-{P})*sqrt(-{Q})", str(val), None, "intermediate"), d=2)
    a, b = nonzero(r, -4, 4), nonzero(r, -4, 4)
    wrongv = cx(a * a + b * b, 2 * a * b)
    val = cx(a * a - b * b, 2 * a * b)
    wrong = f"$({cx(a, b)})^2={a * a}{'+' if 2 * a * b > 0 else ''}{2 * a * b}i+{b * b}i^2={a * a}{'+' if 2 * a * b > 0 else ''}{2 * a * b}i+{b * b}={wrongv}$"
    fix = f"$({cx(a, b)})^2={a * a}{'+' if 2 * a * b > 0 else ''}{2 * a * b}i+{b * b}i^2={a * a}{'+' if 2 * a * b > 0 else ''}{2 * a * b}i-{b * b}={val}$"
    return err_item(f"$({cx(a, b)})^2$ を計算しなさい。", wrong, f"2つ目の等号（${b * b}i^2$ を ${b * b}$ とした部分）", "calculation",
                    "$i^2$ の $2$ 乗を見て「2乗すれば正になる」という実数の感覚で処理してしまった。",
                    fix, f"${val}$", "$i^2=-1$ なので、$" + str(b * b) + "i^2=-" + str(b * b) + "$。",
                    [f"$({cx(a, b)})^2={a * a}+2\\cdot({a})\\cdot({b})i+({b})^2i^2$。", f"$i^2=-1$ より ${b * b}i^2=-{b * b}$。", f"整理して ${val}$。"],
                    "$i^2$ が現れたら、すぐに $-1$ におきかえる。",
                    [f"$(a+bi)^2=(a^2-b^2)+2abi$ の形を覚えておき、実部が $a^2-b^2={a * a - b * b}$ になることで確かめる。"],
                    ["$i^2=1$ と扱う。"],
                    chk=(f"expand(({cxp(a, b)})**2)", cxp(a * a - b * b, 2 * a * b), None, "intermediate"), d=2)


@gen("error_correction", 3, ["common_error", "computation"])
def err_vieta_sign(r):
    a = r.choice([1, 2, 3])
    b, c = nonzero(r, -6, 6), nonzero(r, -6, 6)
    key, tex, f, py, form = r.choice([SYM[1], SYM[3], SYM[4], ("pp1", "(\\alpha+1)(\\beta+1)", lambda s, p: p + s + 1, "(P)+(S)+1", "\\alpha\\beta+(\\alpha+\\beta)+1")])
    s, p = Fraction(-b, a), Fraction(c, a)
    val = f(s, p)
    wv = f(-s, p)
    if wv == val:
        b = b + 1 if b != -1 else 2
        s = Fraction(-b, a)
        val, wv = f(s, p), f(-s, p)
    wrong = f"解と係数の関係より $\\alpha+\\beta={ftex(-s)}$、$\\alpha\\beta={ftex(p)}$。${tex}={form}={ftex(wv)}$"
    fix = f"$\\alpha+\\beta=-\\dfrac{{b}}{{a}}={ftex(s)}$ として ${tex}={ftex(val)}$"
    return err_item(f"二次方程式 ${poly(a, b, c)}=0$ の2つの解を $\\alpha,\\ \\beta$ とするとき、${tex}$ の値を求めなさい。", wrong,
                    "$\\alpha+\\beta$ の値（符号）", "formula",
                    "$\\alpha\\beta=\\dfrac{c}{a}$ と同じ感覚で、和も $\\dfrac{b}{a}$ と符号をつけずに覚えてしまっている。",
                    fix, f"${ftex(val)}$",
                    f"$a(x-\\alpha)(x-\\beta)=ax^2-a(\\alpha+\\beta)x+a\\alpha\\beta$ と比べると、$\\alpha+\\beta=-\\dfrac{{b}}{{a}}$ である。",
                    [f"$\\alpha+\\beta=-\\dfrac{{b}}{{a}}={ftex(s)}$、$\\alpha\\beta=\\dfrac{{c}}{{a}}={ftex(p)}$。", f"${tex}={form}$。", f"代入して ${ftex(val)}$。"],
                    "解と係数の関係の和は $-\\dfrac{b}{a}$。展開した式と係数比較すれば符号を確かめられる。",
                    [f"$a(x-\\alpha)(x-\\beta)$ を展開して $x$ の係数を ${b}$ と比べると、$\\alpha+\\beta$ の符号を確かめられる。"],
                    ["和の符号を誤る。"],
                    chk=(py.replace("S", fr_py(s.numerator, s.denominator)).replace("P", fr_py(p.numerator, p.denominator)), fr_py(val.numerator, val.denominator), None, "intermediate"))


@gen("error_correction", 2, ["common_error", "computation"])
def err_remainder_sign(r):
    while True:
        P = [r.choice([1, 2, -1])] + [r.randint(-5, 5) for _ in range(3)]
        t = r.randint(1, 4)
        if peval(P, t) != peval(P, -t):
            break
    val, wv = peval(P, -t), peval(P, t)
    wrong = f"剰余の定理より、余りは $P({t})={wv}$"
    fix = f"$x+{t}=x-(-{t})$ なので、余りは $P(-{t})={val}$"
    return err_item(f"整式 $P(x)={poly(*P)}$ を $x+{t}$ で割ったときの余りを求めなさい。", wrong, f"代入する値（$x={t}$ とした部分）", "sign",
                    f"割る式 $x+{t}$ に見える数 ${t}$ をそのまま代入してしまった。剰余の定理の「$x-\\alpha$ で割った余りは $P(\\alpha)$」の符号を意識していない。",
                    fix, f"${val}$", f"$x+{t}=0$ となる $x=-{t}$ を代入する。",
                    [f"$x+{t}=x-(-{t})$ なので $\\alpha=-{t}$。", f"$P(-{t})={val}$。"],
                    "割る式を $x-\\alpha$ の形に直すか、「割る式 $=0$」を解いて代入する値を決める。",
                    [f"実際に $x+{t}$ で割り算をして余りが ${val}$ になることを確かめる。"],
                    ["$x+a$ で割るときに $x=a$ を代入する。"],
                    chk=(at(ppy(P), -t), str(val), None, "intermediate"), d=2)


@gen("error_correction", 2, ["common_error", "concept"])
def err_missing_imag(r):
    rt = nonzero(r, -3, 3)
    h = r.randint(-2, 2)
    k = r.choice([1, 2, 3, 4, 9])
    roots_tex, roots_py = quad_roots(h, k)
    Qd = [1, -2 * h, h * h + k]
    P = pmul([1, -rt], Qd)
    wrong = f"$P({rt})=0$ より $({xm(rt)})({poly(*Qd)})=0$。${poly(*Qd)}=0$ は判別式が負なので解をもたない。よって解は $x={rt}$ のみ"
    fix = f"${poly(*Qd)}=0$ を複素数の範囲で解くと $x={roots_tex}$。解は $x={rt},\\ {roots_tex}$"
    return err_item(f"方程式 ${poly(*P)}=0$ を、複素数の範囲で解きなさい。", wrong, "「判別式が負なので解をもたない」とした部分", "concept",
                    "数学Ⅰで「$D<0$ なら（実数の）解なし」と学んだことを、複素数の範囲で解く場面でもそのまま使ってしまった。",
                    fix, f"$x={rt},\\ {roots_tex}$",
                    "複素数の範囲では、判別式が負の二次方程式は異なる2つの虚数解をもつ。3次方程式は重解を含めて3つの解をもつ。",
                    [f"因数分解 $({xm(rt)})({poly(*Qd)})=0$ までは正しい。", f"${poly(*Qd)}=0$ を解の公式で解くと $x={roots_tex}$。", f"解は $x={rt},\\ {roots_tex}$。"],
                    "「複素数の範囲で解く」と指示されたら、虚数解まで求める。",
                    ["3次方程式の解は重解を含めて3つあるはず、という個数の確認で書き落としに気づける。"],
                    ["虚数解を書き落とす。"],
                    chk=(f"solve({ppy(P)}, x)", "[" + ", ".join([str(rt)] + roots_py) + "]", "set", "intermediate"))


GENERATORS = [complex_arith, complex_equality, root_kind, symmetric_value,
              remainder_thm, cubic_solve, remainder_two, biquadratic,
              complex_root_coef, new_equation, sign_of_roots, xn_remainder,
              err_complex, err_vieta_sign, err_remainder_sign, err_missing_imag]
