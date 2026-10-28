"""単元パック：数学Ⅱ 指数関数・対数関数（指数の拡張・指数関数・対数の性質・常用対数）。"""
import math
from fractions import Fraction as F
from itertools import combinations

from banks._common import desc, figure, mc, plane, sa
from hs_pack_lib import board, check, definition, derivation, example, gen, guide, intro, lesson, poly, summary, theorem, tp

UNIT_ID = "HS-MATH2-U05"


# ----------------------------------------------------------------------
# 補助
# ----------------------------------------------------------------------

def ft(v):
    """有理数の LaTeX（分数は \\dfrac）。"""
    v = F(v)
    if v.denominator == 1:
        return str(v.numerator)
    return f"{'-' if v < 0 else ''}\\dfrac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def fs(v):
    """指数・添字の中で使う小さい分数（\\frac）。"""
    v = F(v)
    if v.denominator == 1:
        return str(v.numerator)
    return f"{'-' if v < 0 else ''}\\frac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def fp(v):
    v = F(v)
    return str(v.numerator) if v.denominator == 1 else f"Rational({v.numerator},{v.denominator})"


def base_t(b):
    """累乗の底の表記（分数なら括弧つき）。"""
    b = F(b)
    return str(b.numerator) if b.denominator == 1 else f"\\left({ft(b)}\\right)"


def logt(a, x):
    """log_a x の LaTeX（x は文字列）。"""
    return f"\\log_{{{fs(a)}}}{x}"


def root_t(b, k, p=1):
    """k 乗根 b^p の LaTeX。"""
    inner = str(b) if p == 1 else f"{b}^{{{p}}}"
    return f"\\sqrt{{{inner}}}" if k == 2 else f"\\sqrt[{k}]{{{inner}}}"


def ilog(n, a):
    """n=a^k となる整数 k（なければ None）。"""
    n, a = F(n), F(a)
    for k in range(-12, 13):
        if a ** k == n:
            return k
    return None


def arg_t(v):
    v = F(v)
    return str(v.numerator) if v.denominator == 1 else ft(v)


LESSON = lesson(
    goals=["累乗根を用いて指数を有理数（さらに実数）まで拡張し、指数法則を使って計算できる。",
           "対数を指数の逆の関係として定義し、対数の性質・底の変換公式を指数法則から証明して計算に使える。",
           "指数関数・対数関数のグラフと増減をもとに、方程式・不等式・大小比較を解き、常用対数で桁数などを求められる。"],
    duration=200,
    readiness=["$a^m\\times a^n=a^{m+n}$ など、自然数の指数についての指数法則を使える。", "平方根の計算と有理化ができる。", "二次関数の最大・最小、二次方程式の解法を使える。"],
    flow=[("導入：倍々に増える量", 10, "細菌の増殖や紙を折る回数を例に、指数で表される量の増え方を確かめる"),
          ("指数の拡張", 35, "0・負の整数の指数、累乗根、有理数の指数を、指数法則が成り立つように定める"),
          ("指数関数", 30, "y=2^x, y=(1/2)^x のグラフ、増減と大小比較、方程式・不等式"),
          ("対数の定義と性質", 40, "a^p=M ⇔ p=log_a M、性質を指数法則から証明"),
          ("底の変換と対数関数", 35, "底の変換公式、y=log_a x のグラフ、真数条件、方程式・不等式"),
          ("常用対数", 35, "桁数・小数首位、日常の事象（増加率）への応用"),
          ("まとめ", 15, "指数と対数の対応表を板書し、確認問題と課題を指示")],
    sections=[
        intro("in1", "倍々に増える量を表す",
              "ある細菌が1時間ごとに2倍に増えるとき、$x$ 時間後の個数はもとの $2^x$ 倍になる。$x$ が自然数でないとき（30分後、1時間前など）にも $2^x$ に意味を与えたい。指数を実数まで拡張し、それを逆に「何乗すればよいか」で表したものが対数である。",
              bullets=["指数関数は、人口・放射性物質の量・預金の複利など、一定の割合で増減する量を表す。", "対数を使うと、非常に大きな数・小さな数の桁数を求めたり、かけ算をたし算に直したりできる。"],
              points=[tp("厚さ $0.1\\,\\mathrm{mm}$ の紙を何回折れば富士山の高さを超えるかを予想させ、倍々の増え方が予想を大きく上回ることを体感させる。",
                         ask="10回折ると厚さは何倍になるか。", expect="$2^{10}=1024$ 倍", timing="導入の冒頭")]),
        definition("df1", "累乗根と有理数の指数",
                   "$n$ を正の整数とするとき、$n$ 乗して $a$ になる数を $a$ の $n$ 乗根という。$a>0$ のとき、$n$ 乗根のうち正のものを $\\sqrt[n]{a}$ と書く。これを使い、$a>0$ のとき指数を次のように定める。",
                   formula="$$a^0=1,\\qquad a^{-n}=\\dfrac{1}{a^n},\\qquad a^{\\frac{m}{n}}=\\sqrt[n]{a^m}=\\left(\\sqrt[n]{a}\\right)^m$$",
                   conditions=["有理数の指数は底 $a>0$ のときに考える（$a<0$ だと $(-8)^{\\frac13}$ と $(-8)^{\\frac26}$ が一致しないなどの不都合が起こる）",
                               "$m,\\ n$ は整数で $n>0$"],
                   points=[tp("定義は「指数法則がそのまま成り立つように」決めたものであることを、$a^3\\div a^3=a^{0}$ から $a^0=1$ を導く流れで説明する。",
                              ask="$a^{\\frac12}$ を2乗すると何になるはずか。", expect="指数法則から $a^{1}=a$。だから $a^{\\frac12}=\\sqrt a$。")]),
        theorem("th1", "指数法則（実数の指数）",
                "$$a^pa^q=a^{p+q},\\qquad (a^p)^q=a^{pq},\\qquad (ab)^p=a^pb^p$$",
                ["$a>0,\\ b>0$、$p,\\ q$ は実数", "$a^p\\div a^q=a^{p-q}$ も成り立つ"],
                proof=["$p=\\dfrac{m}{n}$（$n>0$）のとき、$\\left(a^{\\frac{m}{n}}\\right)^n=\\left(\\sqrt[n]{a^m}\\right)^n=a^m$ である。",
                       "$p=\\dfrac{m}{n},\\ q=\\dfrac{k}{n}$ と通分しておくと、$\\left(a^pa^q\\right)^n=\\left(a^p\\right)^n\\left(a^q\\right)^n=a^ma^k=a^{m+k}$。",
                       "$a^pa^q>0$ なので、$a^pa^q$ は $a^{m+k}$ の正の $n$ 乗根、すなわち $a^{\\frac{m+k}{n}}=a^{p+q}$。",
                       "ほかの法則も同様に、両辺を $n$ 乗して整数の指数の法則に帰着させて示せる。"],
                points=[tp("「正の $n$ 乗根はただ1つ」という事実が証明の鍵であることを確認する。", caution="$\\sqrt[n]{a}$ の定義で $a>0$ を落とすと議論が崩れる。")]),
        definition("df2", "対数の定義",
                   "$a>0,\\ a\\neq1$ のとき、任意の正の数 $M$ に対して $a^p=M$ を満たす実数 $p$ がただ1つ定まる。この $p$ を、$a$ を底とする $M$ の対数といい、$\\log_aM$ と書く。$M$ を真数という。",
                   formula="$$a^p=M\\iff p=\\log_aM$$",
                   conditions=["底の条件：$a>0,\\ a\\neq1$", "真数条件：$M>0$", "$\\log_a1=0,\\ \\log_aa=1,\\ a^{\\log_aM}=M$"],
                   points=[tp("「$\\log_28$ は、2を何乗すれば8になるかという数」と、言葉で読む練習をくり返させる。", ask="$\\log_3\\dfrac19$ は何か。", expect="$3^{-2}=\\dfrac19$ なので $-2$"),
                           tp("真数条件 $M>0$ は、対数の方程式・不等式で最初に確認する条件であることを予告しておく。")]),
        theorem("th2", "対数の性質",
                "$$\\log_aMN=\\log_aM+\\log_aN,\\qquad \\log_a\\dfrac{M}{N}=\\log_aM-\\log_aN,\\qquad \\log_aM^r=r\\log_aM$$",
                ["$a>0,\\ a\\neq1,\\ M>0,\\ N>0$、$r$ は実数", "$\\log_a(M+N)$ を分ける公式はない"],
                proof=["$\\log_aM=p,\\ \\log_aN=q$ とおくと、$M=a^p,\\ N=a^q$。",
                       "$MN=a^pa^q=a^{p+q}$ なので、対数の定義から $\\log_aMN=p+q=\\log_aM+\\log_aN$。",
                       "$\\dfrac{M}{N}=a^{p-q}$ から第2式、$M^r=(a^p)^r=a^{pr}$ から第3式が同様に得られる。"],
                points=[tp("対数の性質は指数法則を「指数の側から見たもの」であることを、表を並べて対応させる。",
                           caution="$\\log_a(M+N)=\\log_aM+\\log_aN$ と誤る生徒が多い。$M=N=2,\\ a=2$ などで反例を示す。")]),
        derivation("dv1", "底の変換公式",
                   ["$\\log_ab=p$ とおくと $a^p=b$。", "両辺の、$c$ を底とする対数をとる（$c>0,\\ c\\neq1$）：$\\log_ca^p=\\log_cb$、すなわち $p\\log_ca=\\log_cb$。",
                    "$a\\neq1$ より $\\log_ca\\neq0$ なので、$p=\\dfrac{\\log_cb}{\\log_ca}$。よって $\\log_ab=\\dfrac{\\log_cb}{\\log_ca}$。"],
                   body="底がそろっていない対数は、底の変換公式で同じ底にそろえてから計算する。特に $\\log_ab\\cdot\\log_ba=1$ が成り立つ。",
                   points=[tp("底の変換公式を使って、関数電卓の $\\log$（常用対数）で $\\log_23$ を計算させ、公式の実用性を確かめさせる。", timing="底の変換公式の導出直後")]),
        theorem("th3", "指数関数・対数関数の増減",
                "$$a>1\\ \\text{のとき}\\quad p<q\\iff a^p<a^q,\\qquad 0<M<N\\iff\\log_aM<\\log_aN$$",
                ["$0<a<1$ のときは不等号の向きが逆になる", "$y=a^x$ の値域は $y>0$、$y=\\log_ax$ の定義域は $x>0$",
                 "$y=a^x$ と $y=\\log_ax$ のグラフは直線 $y=x$ に関して対称"],
                proof=["$a>1,\\ p<q$ のとき $a^q\\div a^p=a^{q-p}$ で、$q-p>0$ なので $a^{q-p}>1$。よって $a^p<a^q$。",
                       "対数については、$\\log_aM=p,\\ \\log_aN=q$ とおくと $M=a^p,\\ N=a^q$ なので、上の結果から $M<N\\iff p<q$。"],
                figure=figure("y=2^x と y=log₂x のグラフ（直線 y=x に関して対称）", plane((-3, 5), (-3, 5), unit=20,
                                                                                curves=[(lambda x: 2 ** x, "y=2^x"), (lambda x: math.log2(x) if x > 0.01 else float("nan"), "y=log₂x"),
                                                                                        (lambda x: x, "")])),
                points=[tp("底が $1$ より大きいか小さいかで増減が変わることを、$y=2^x$ と $y=\\left(\\frac12\\right)^x$ のグラフを並べて確認させる。",
                           ask="$\\left(\\frac12\\right)^x>\\left(\\frac12\\right)^3$ を満たす $x$ の範囲は？", expect="減少関数なので $x<3$")]),
        example("ex1", "例題1　指数の方程式",
                "方程式 $4^x-3\\cdot2^{x+1}+8=0$ を解け。",
                ["$2^x=t$ とおくと $t>0$。$4^x=t^2,\\ 2^{x+1}=2t$ より $t^2-6t+8=0$。",
                 "$(t-2)(t-4)=0$ より $t=2,\\ 4$（どちらも $t>0$ を満たす）。", "$2^x=2$ より $x=1$、$2^x=4$ より $x=2$。"],
                "$x=1,\\ 2$", thinking="$4^x=(2^x)^2$ に注目し、$2^x$ を1つの文字に置きかえると二次方程式になる。置きかえた文字は正であることに注意。",
                points=[tp("$t=2^x>0$ の条件を必ず書かせる。負の解が出たときに捨てる根拠になる。")]),
        example("ex2", "例題2　対数の方程式（真数条件）",
                "方程式 $\\log_2x+\\log_2(x-2)=3$ を解け。",
                ["真数条件より $x>0$ かつ $x-2>0$、すなわち $x>2$。", "左辺 $=\\log_2x(x-2)$、右辺 $=\\log_28$ より $x(x-2)=8$。",
                 "$x^2-2x-8=0$、$(x-4)(x+2)=0$ より $x=4,\\ -2$。", "$x>2$ より $x=4$。"],
                "$x=4$", thinking="対数をまとめて $\\log_2(\\ \\ )=\\log_2(\\ \\ )$ の形にし、真数を比べる。最初に真数条件を書いておく。",
                misconceptions=[("$x=4,\\ -2$ と両方答える", "$x=-2$ は真数 $x$ が負になるので不適")]),
        example("ex3", "例題3　常用対数と桁数",
                "$\\log_{10}2=0.3010,\\ \\log_{10}3=0.4771$ とする。$6^{30}$ は何桁の整数か。",
                ["$\\log_{10}6^{30}=30(\\log_{10}2+\\log_{10}3)=30\\times0.7781=23.343$。", "$23<\\log_{10}6^{30}<24$ より $10^{23}<6^{30}<10^{24}$。", "よって24桁。"],
                "24桁", thinking="$N$ が $n$ 桁 $\\iff 10^{n-1}\\leqq N<10^n\\iff n-1\\leqq\\log_{10}N<n$。",
                points=[tp("「$10^{23}$ は24桁」であることを、$10^1=10$ が2桁であることから確認させる。", caution="23桁と答える誤りが多い。")]),
        board("bd1", "板書案",
              [("① 指数の拡張", ["$a^0=1,\\ a^{-n}=\\dfrac{1}{a^n}$", "$a^{\\frac{m}{n}}=\\sqrt[n]{a^m}$", "指数法則 $a^pa^q=a^{p+q}$", "$a>1$：増加、$0<a<1$：減少"]),
               ("② 対数", ["$a^p=M\\iff p=\\log_aM$", "底 $a>0,\\ a\\neq1$、真数 $M>0$", "$\\log_aMN=\\log_aM+\\log_aN$", "$\\log_aM^r=r\\log_aM$", "$\\log_ab=\\dfrac{\\log_cb}{\\log_ca}$"]),
               ("③ 活用", ["置きかえ $t=2^x>0$", "真数条件を最初に", "底 $<1$ なら不等号逆向き", "$n$ 桁 $\\iff n-1\\leqq\\log_{10}N<n$"])]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("指数・対数の方程式では、置きかえた文字の範囲（$t=a^x>0$）や真数条件を、式変形より先に書く習慣をつけさせる。", ask="$\\log_2x+\\log_2(x-2)=3$ で、最初に書くべき条件は？", expect="$x>2$"),
               tp("不等式では、底と $1$ の大小で不等号の向きが決まることを、グラフの増減と結びつけて説明させる。", caution="底が $\\frac12$ のときに不等号の向きを変え忘れる誤りが最も多い。"),
               tp("常用対数の値（$\\log_{10}2=0.3010$ など）は近似値なので、境目の判断ではその誤差が結論に影響しないかを意識させる。", timing="常用対数の例題の後"),
               tp("$\\log_aM+\\log_aN=\\log_a(M+N)$ のような誤りは、具体的な数値で反例を作らせて自分で気づかせる。")],
              misconceptions=[("$\\log_a(M+N)=\\log_aM+\\log_aN$", "成り立つのは $\\log_aMN=\\log_aM+\\log_aN$"),
                              ("$a^{-n}=-a^n$", "$a^{-n}=\\dfrac{1}{a^n}$（正の数）"),
                              ("$\\log_{\\frac12}x>1$ を $x>\\dfrac12$ とする", "底が1より小さいので $0<x<\\dfrac12$")]),
        summary("sm1", "まとめ", ["指数は、指数法則が成り立つように $0$・負の数・有理数・実数へと拡張した（底は正）。",
                                   "$a^p=M\\iff p=\\log_aM$。対数の性質と底の変換公式は指数法則から導ける。",
                                   "$y=a^x,\\ y=\\log_ax$ は $a>1$ で増加、$0<a<1$ で減少。不等式では底と $1$ の大小を確認する。",
                                   "常用対数で桁数・小数首位が求められる。"]),
        check("ck1", "確認問題", [("$27^{-\\frac23}$ の値は？", "$\\dfrac19$"), ("$\\log_4 8$ の値は？", "$\\dfrac32$"),
                                  ("$\\log_23\\cdot\\log_34$ の値は？", "$2$"), ("不等式 $\\left(\\frac13\\right)^x<9$ を解くと？", "$x>-2$")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

@gen("basic_check", 5, ["computation", "concept"])
def exp_value(r):
    b = r.choice([2, 3, 4, 5, 6, 7, 10])
    n = r.choice([2, 3, 4] if b <= 5 else [2, 3])
    m = r.choice([1, 2, 3, 4, 5])
    while math.gcd(m, n) != 1:
        m = r.choice([1, 2, 3, 4, 5])
    sgn = r.choice([1, -1])
    flip = r.random() < 0.3
    base = F(1, b ** n) if flip else F(b ** n)
    e = F(sgn * m, n)
    v = base ** e.numerator
    # base^(e) = (b^{±n})^(±m/n)
    ans = (F(1, b) if flip else F(b)) ** (sgn * m)
    st = [f"${base_t(base)}={base_t(F(1, b) if flip else F(b))}^{{{n}}}$ と表す。",
          f"${base_t(base)}^{{{fs(e)}}}=\\left({base_t(F(1, b) if flip else F(b))}^{{{n}}}\\right)^{{{fs(e)}}}={base_t(F(1, b) if flip else F(b))}^{{{sgn * m}}}$。",
          f"$={ft(ans)}$。"]
    del v
    return sa(f"指数法則を用いて、${base_t(base)}^{{{fs(e)}}}$ の値を求めなさい。", f"${ft(ans)}$",
              f"底を $n$ 乗の形に直してから指数法則 $(a^p)^q=a^{{pq}}$ を使う。", d=2,
              ap="底を「何かの $" + str(n) + "$ 乗」で表すと、指数の分母と打ち消し合って整数の指数になる。",
              steps=st, alt=[f"$a^{{\\frac{{m}}{{n}}}}=\\left(\\sqrt[n]{{a}}\\right)^m$ を使い、$\\sqrt[{n}]{{{arg_t(base)}}}={ft(F(1, b) if flip else F(b))}$ を先に求めてから累乗してもよい。"],
              pc=[("底を累乗の形に直している", 1), ("値が正しい", 1)], pit=["負の指数で $-$ をつけてしまう（$a^{-n}=-a^n$ と誤る）。", "指数の分数を約分せずに計算して迷う。"],
              chk=(f"({fp(base)})**({fp(e)})", fp(ans), None, "intermediate"))


@gen("basic_check", 4, ["computation"])
def root_law(r):
    b = r.choice([2, 3, 5, 6, 10])
    while True:
        ks = [r.choice([2, 3, 4, 6]) for _ in range(3)]
        ps = [r.randint(1, 5) for _ in range(3)]
        ops = r.choice([(1, 1, -1), (1, -1, 1), (1, 1, 1)])
        tot = sum(o * F(p, k) for o, p, k in zip(ops, ps, ks))
        if tot.denominator == 1 and 1 <= tot <= 4 and all(F(p, k).denominator != 1 for p, k in zip(ps, ks)):
            break
    terms = [root_t(b, k, p) for p, k in zip(ps, ks)]
    expr = terms[0] + "".join(("\\times" if o > 0 else "\\div") + t for o, t in zip(ops[1:], terms[1:]))
    exps = [F(p, k) for p, k in zip(ps, ks)]
    sm = "+".join(fs(x) if o > 0 else "" for o, x in zip(ops, exps))
    sm = fs(exps[0]) + "".join(("+" if o > 0 else "-") + fs(x) for o, x in zip(ops[1:], exps[1:]))
    return sa(f"$a^{{\\frac{{m}}{{n}}}}$ の形に直して計算しなさい。$${expr}$$", f"${b ** tot.numerator}$",
              f"各項を ${b}$ の累乗で表すと、指数は ${sm}={tot}$。", d=2,
              ap=f"累乗根を $\\sqrt[n]{{a^m}}=a^{{\\frac{{m}}{{n}}}}$ と分数の指数に直すと、かけ算・わり算が指数のたし算・ひき算になる。",
              steps=[f"${expr}=" + "".join(f"{('' if i == 0 else ('\\times' if o > 0 else '\\div'))}{b}^{{{fs(x)}}}" for i, (o, x) in enumerate(zip(ops, exps))) + "$。",
                     f"指数を計算して ${sm}={tot}$。", f"${b}^{{{tot}}}={b ** tot.numerator}$。"],
              alt=["指数の分母を通分して1つの累乗根 $\\sqrt[N]{\\ \\ }$ にまとめて計算しても、同じ結果になる。"],
              pc=[("分数の指数に正しく直している", 1), ("値が正しい", 1)], pit=["$\\sqrt[3]{a^2}$ を $a^{\\frac32}$ と、分母と分子を逆にする。"],
              chk=(f"{b}**({'+'.join(f'({o})*Rational({p},{k})' for o, p, k in zip(ops, ps, ks))})", str(b ** tot.numerator), None, "intermediate"))


@gen("basic_check", 4, ["computation", "concept"])
def log_value(r):
    c = r.choice([2, 3, 5])
    i = r.choice([1, 1, 2, 3, -1])
    j = r.choice([-3, -2, -1, 2, 3, 4, F(1, 2), F(3, 2), F(-1, 2)])
    a = F(c) ** i
    if F(j).denominator == 1:
        x = F(c) ** int(j)
        xt = arg_t(x)
    else:
        jj = F(j)
        whole = F(c) ** (jj.numerator // 2) if jj.numerator > 0 else None
        if jj == F(1, 2):
            xt = f"\\sqrt{{{c}}}"
        elif jj == F(3, 2):
            xt = f"{c}\\sqrt{{{c}}}"
        else:
            xt = f"\\dfrac{{1}}{{\\sqrt{{{c}}}}}"
        del whole
    v = F(j) / i
    return sa(f"対数の定義にもとづいて、${logt(a, xt)}$ の値を求めなさい。", f"${ft(v)}$",
              f"${base_t(a)}={c}^{{{i}}}$、${xt}={c}^{{{fs(j)}}}$ なので、$({c}^{{{i}}})^p={c}^{{{fs(j)}}}$ より $p={ft(v)}$。", d=2,
              ap="$" + logt(a, xt) + "=p$ とおき、$" + base_t(a) + "^p=" + xt + "$ を満たす $p$ を探す。底と真数を同じ数の累乗で表すとよい。",
              steps=[f"${logt(a, xt)}=p$ とおくと ${base_t(a)}^p={xt}$。", f"${c}^{{{i}p}}={c}^{{{fs(j)}}}$ より ${i}p={fs(j)}$。", f"$p={ft(v)}$。"],
              alt=[f"底の変換公式で $\\dfrac{{\\log_{{{c}}}{xt}}}{{\\log_{{{c}}}{arg_t(a)}}}=\\dfrac{{{fs(j)}}}{{{i}}}$ と計算してもよい。"],
              pc=[("底と真数を同じ数の累乗で表している", 1), ("値が正しい", 1)], pit=["底と真数の役割を逆にして、逆数を答える。"],
              chk=(f"log({c}**({fp(j)}), {fp(a)})", fp(v), None, "intermediate"))


def _divisors(n):
    return [d for d in range(2, n) if n % d == 0]


@gen("basic_check", 4, ["computation"])
def log_props(r):
    a = r.choice([2, 3, 5, 6, 10])
    kind = r.choice(["sum", "diff", "coef"])
    if kind == "sum":
        a = r.choice([6, 10, 12])
        n = r.choice([2, 3] if a == 6 else [2])
        ds = [d for d in _divisors(a ** n) if ilog(d, a) is None and ilog(F(a ** n, d), a) is None]
        M = r.choice(ds)
        N = a ** n // M
        expr = f"{logt(a, M)}+{logt(a, N)}"
        st = [f"$={logt(a, f'({M}\\times{N})')}={logt(a, a ** n)}$。", f"$={n}$。"]
        ck = f"log({M},{a})+log({N},{a})"
    elif kind == "diff":
        n = r.choice([1, 2, 3] if a <= 5 else [1, 2])
        Q = r.choice([q for q in (2, 3, 5, 6, 7) if q != a and ilog(q, a) is None])
        M = Q * a ** n
        expr = f"{logt(a, M)}-{logt(a, Q)}"
        st = [f"$={logt(a, f'\\dfrac{{{M}}}{{{Q}}}')}={logt(a, a ** n)}$。", f"$={n}$。"]
        ck = f"log({M},{a})-log({Q},{a})"
    else:
        n = r.choice([1, 2])
        cands = [(P, P * P // a ** n) for P in range(2, 31) if (P * P) % (a ** n) == 0 and P * P // a ** n > 1 and ilog(P, a) is None]
        P, Q = r.choice(cands)
        expr = f"2{logt(a, P)}-{logt(a, Q)}"
        st = [f"$2{logt(a, P)}={logt(a, f'{P}^2')}={logt(a, P * P)}$。", f"$={logt(a, f'\\dfrac{{{P * P}}}{{{Q}}}')}={logt(a, a ** n)}={n}$。"]
        ck = f"2*log({P},{a})-log({Q},{a})"
    return sa(f"対数の性質を用いて、次の式を簡単にしなさい。$${expr}$$", f"${n}$",
              "対数の性質で1つの対数にまとめ、真数を底の累乗で表す。", d=2,
              ap="1つ1つの対数は簡単な値にならない。性質 $\\log_aM+\\log_aN=\\log_aMN$ などで1つにまとめると、真数が底の累乗になる。",
              steps=[f"${expr}$"] + st,
              alt=[f"各真数を素因数分解し、$\\log_{{{a}}}$ の和・差に分けてから打ち消し合いを見てもよい。"],
              pc=[("性質を正しく使って1つの対数にまとめている", 1), ("値が正しい", 1)],
              pit=["$\\log_aM+\\log_aN=\\log_a(M+N)$ と誤る。", "係数 $2$ を真数の2乗に直さずに真数に掛ける。"],
              chk=(ck, str(n), None, "intermediate"))


CMP_POOL = [(2, 2), (3, 3), (4, 3), (2, 3), (8, 4), (5, 5), (5, 4), (3, 4), (6, 6), (9, 6), (2, 4), (32, 6)]


def root_val(bk):
    b, k = bk
    return b ** (1 / k)


def root_tex(bk):
    b, k = bk
    return root_t(b, k)


@gen("basic_check", 3, ["condition_check", "concept"])
def exp_compare(r):
    while True:
        trio = r.sample(CMP_POOL, 3)
        vals = [root_val(x) for x in trio]
        L = math.lcm(*[k for _, k in trio])
        if len({round(v, 9) for v in vals}) == 3 and max(b ** (L // k) for b, k in trio) <= 10 ** 6:
            break
    big = r.random() < 0.5
    key = max if big else min
    right = key(trio, key=root_val)
    ords = sorted(trio, key=root_val)
    why = {}
    for w in trio:
        if w == right:
            continue
        why[f"${root_tex(w)}$"] = (f"${L}$ 乗して比べると ${root_tex(w)}$ は ${w[0] ** (L // w[1])}$ で、{'最大ではない' if big else '最小ではない'}。根号の中の数や根号の指数だけで判断している。",
                                   "累乗根の大小を中身や指数だけで判断する誤り")
    word = "最も大きい" if big else "最も小さい"
    return mc(f"次の3つの数のうち、{word}ものを選びなさい。$$" + ",\\quad ".join(root_tex(x) for x in trio) + "$$", [f"${root_tex(right)}$"] + list(why),
              f"すべて正の数なので、${L}$ 乗した値の大小で比べられる：" + "、".join(f"$\\left({root_tex(x)}\\right)^{{{L}}}={x[0] ** (L // x[1])}$" for x in trio) + "。", d=3,
              ap=f"根号の指数がそろっていないので、すべてを ${L}$ 乗（指数の分母の最小公倍数）して整数にしてから比べる。正の数 $A,\\ B$ では $A<B\\iff A^{{n}}<B^{{n}}$。",
              steps=[f"$\\sqrt[k]{{b}}=b^{{\\frac1k}}$ と表し、${L}$ 乗する。"] + [f"$\\left({root_tex(x)}\\right)^{{{L}}}={x[0]}^{{{L // x[1]}}}={x[0] ** (L // x[1])}$。" for x in trio]
              + ["小さい順に $" + "<".join(root_tex(x) for x in ords) + "$。"],
              alt=["底を $2$ にそろえられるもの（$\\sqrt[3]{4}=2^{\\frac23}$ など）は指数の大小で比べてもよい（底 $2>1$ なので指数が大きいほど大きい）。"],
              pc=[("同じ数で累乗して比べる方針を立てている", 1), ("正しく選んでいる", 1)], why=why,
              chk=(f"[{', '.join(f'{b}**{L // k}' for b, k in trio)}]", f"[{', '.join(str(b ** (L // k)) for b, k in trio)}]", None, "intermediate"))


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 4, ["computation"])
def exp_equation(r):
    c = r.choice([2, 3])
    while True:
        i, j = r.sample([1, 2, 3, 4], 2)
        s, t = r.randint(-3, 3), r.randint(-3, 3)
        x0 = F(j * t - i * s, i - j)
        if x0.denominator == 1 and x0 != 0 and (s, t) != (0, 0):
            break
    A, B = c ** i, c ** j

    def ex(k):
        return "x" if k == 0 else f"x{'+' if k > 0 else '-'}{abs(k)}"
    lhs = f"{A}^{{{ex(s)}}}"
    rhs = f"{B}^{{{ex(t)}}}"
    return sa(f"方程式 ${lhs}={rhs}$ を解きなさい。", f"$x={ft(x0)}$",
              f"底を ${c}$ にそろえると ${c}^{{{i}({ex(s)})}}={c}^{{{j}({ex(t)})}}$。指数を比べる。", d=3,
              ap=f"${A}$ と ${B}$ はどちらも ${c}$ の累乗。底をそろえれば、指数関数は1対1なので指数どうしが等しいという式になる。",
              steps=[f"${A}={c}^{{{i}}},\\ {B}={c}^{{{j}}}$ より ${c}^{{{i}({ex(s)})}}={c}^{{{j}({ex(t)})}}$。", f"${i}({ex(s)})={j}({ex(t)})$。", f"$x={ft(x0)}$。"],
              alt=["両辺の $" + str(c) + "$ を底とする対数をとっても、同じ一次方程式が得られる。", f"$x={ft(x0)}$ を代入して両辺が等しくなることを確かめる。"],
              pc=[("底をそろえている", 1), ("指数の方程式を正しく立てている", 2), ("解が正しい", 1)],
              pit=["$(c^i)^{x+s}$ を $c^{i+x+s}$ と、指数を掛けずに足してしまう。"],
              chk=(f"{A}**({fp(x0)}+({s})) - {B}**({fp(x0)}+({t}))", "0", None, "intermediate"))


@gen("standard_practice", 4, ["computation", "condition_check"])
def exp_quad_eq(r):
    c = r.choice([2, 3])
    u = r.choice([-1, 0, 1, 2, 3])
    two = r.random() < 0.6
    if two:
        v = r.choice([w for w in [-1, 0, 1, 2, 3] if w != u])
        t1, t2 = F(c) ** u, F(c) ** v
    else:
        t1, t2 = F(c) ** u, F(-r.choice([1, 2, 3, 4, 5]))
    S, P = t1 + t2, t1 * t2
    if S.denominator != 1 or P.denominator != 1:
        # 分数係数を避けて、両辺に分母を掛ける
        L = math.lcm(S.denominator, P.denominator)
    else:
        L = 1
    a2, a1, a0 = L, -S * L, P * L
    eq = f"{c * c}^x" if a2 == 1 else f"{a2}\\cdot{c * c}^x"
    mid = "" if a1 == 0 else (("+" if a1 > 0 else "-") + (f"{c}^x" if abs(a1) == 1 else f"{abs(a1)}\\cdot{c}^x"))
    tail = "" if a0 == 0 else f"{'+' if a0 > 0 else '-'}{abs(a0)}"
    eq = f"{eq}{mid}{tail}=0"
    sols = [t for t in (t1, t2) if t > 0]
    xs = sorted({ilog(t, c) for t in sols})
    tq = poly(int(a2), int(a1), int(a0), var="t")
    return sa(f"方程式 ${eq}$ を解きなさい。", "$x=" + ",\\ ".join(str(x) for x in xs) + "$",
              f"${c}^x=t\\ (t>0)$ とおくと ${tq}=0$。", d=3,
              ap=f"${c * c}^x=({c}^x)^2$ に注目して ${c}^x=t$ とおくと、$t$ の二次方程式になる。$t$ は正の数しかとらないことに注意する。",
              steps=[f"${c}^x=t$ とおくと $t>0$、方程式は ${tq}=0$。", f"$t={ft(t1)},\\ {ft(t2)}$。" + ("" if two else f" $t>0$ より $t={ft(t1)}$。"),
                     "$" + ",\\ ".join(f"{c}^x={ft(t)}" for t in sols) + "$ より $x=" + ",\\ ".join(str(x) for x in xs) + "$。"],
              alt=["得られた $x$ をもとの方程式に代入して $0$ になることを確かめる。"],
              pc=[("$t$ に置きかえ、$t>0$ を示している", 1), ("$t$ の二次方程式を正しく解いている", 2), ("$x$ を正しく求めている", 1)],
              pit=["$t>0$ を考えずに負の $t$ からも $x$ を求めようとする。", "$" + str(c * c) + "^x=" + str(c) + "^{x^2}$ と誤る。"],
              chk=(f"[{', '.join(f'{a2}*{c * c}**({x})+({a1})*{c}**({x})+({a0})' for x in xs)}]", "[" + ", ".join("0" for _ in xs) + "]", None, "intermediate"))


def _log_eq(r):
    a = r.choice([2, 3])
    n = r.choice([2, 3] if a == 2 else [1, 2])
    if a == 2:
        n = r.choice([2, 3, 4])
    while True:
        i = r.randint(0, n)
        k = a ** i - a ** (n - i)
        if k != 0:
            break
    s = r.choice([-2, -1, 0, 1, 2])
    # (x+s)(x+s-k)=a^n、適する解 x+s=a^i
    good = a ** i - s
    bad = k - a ** i - s  # x+s = k - a^i = -a^{n-i}
    return a, n, k, s, good, bad


def _lin(c):
    return "x" if c == 0 else f"x{'+' if c > 0 else '-'}{abs(c)}"


def _par(e):
    return e if e == "x" else f"({e})"


@gen("standard_practice", 4, ["computation", "condition_check"])
def log_equation(r):
    a, n, k, s, good, bad = _log_eq(r)
    A, B = _lin(s), _lin(s - k)
    cond = f"x>{max(-s, k - s)}"
    return sa(f"方程式 ${logt(a, _par(A))}+{logt(a, _par(B))}={n}$ を解きなさい。", f"$x={good}$",
              f"真数条件 ${cond}$ のもとで ${_par(A)}{_par(B)}={a ** n}$ を解く。", d=3,
              ap="対数の和を1つの対数にまとめ、右辺も同じ底の対数で表して真数を比べる。真数条件を最初に確認しておく。",
              steps=[f"真数条件：${A}>0$ かつ ${B}>0$ より ${cond}$。", f"${_par(A)}{_par(B)}={a}^{{{n}}}={a ** n}$。",
                     f"これを解くと $x={good},\\ {bad}$。", f"${cond}$ より $x={good}$。"],
              alt=[f"$x={good}$ を代入すると左辺は ${logt(a, good + s)}+{logt(a, good + s - k)}={n}$ となり、確かに成り立つ。"],
              pc=[("真数条件を示している", 1), ("真数の方程式を正しく立てて解いている", 2), ("条件に合う解を選んでいる", 1)],
              pit=[f"$x={bad}$ も答えてしまう（真数が負になる）。"],
              chk=(f"solve(({A})*({B})-{a ** n}, x)", f"[{bad}, {good}]", "set", "intermediate"))


IBASES = [F(2), F(3), F(1, 2), F(1, 3)]
OPS = {"<": ("<", "\\leqq", False), ">": (">", "\\geqq", False), "\\leqq": ("<", "\\leqq", True), "\\geqq": (">", "\\geqq", True)}


@gen("standard_practice", 4, ["computation", "condition_check"])
def log_ineq(r):
    b = r.choice(IBASES)
    op = r.choice(list(OPS))
    n = r.choice([1, 2, 3, -1, -2])
    p = r.choice([-2, -1, 0, 1, 2, 3])
    bound = p + b ** n
    if abs(b ** n) > 30:
        n = 1 if n > 0 else -1
        bound = p + b ** n
    less = OPS[op][0] == "<"
    eq = OPS[op][2]
    inc = b > 1
    inner_less = less == inc
    A = _lin(-p)
    if inner_less:
        ans = f"{p}<x{'\\leqq' if eq else '<'}{ft(bound)}"
    else:
        ans = f"x{'\\geqq' if eq else '>'}{ft(bound)}"
    return sa(f"不等式 ${logt(b, _par(A))}{op}{n}$ を満たす $x$ の値の範囲を求めなさい。", f"${ans}$",
              f"右辺を ${logt(b, ft(b ** n))}$ と表す。底 ${ft(b)}$ は $1$ より{'大きい' if inc else '小さい'}ので、真数の大小は{'同じ向き' if inc else '逆向き'}。", d=3,
              ap="真数条件を確認し、右辺を同じ底の対数で表して真数どうしを比べる。底が $1$ より小さいときは不等号の向きが逆になる。",
              steps=[f"真数条件：$x>{p}$。", f"${n}={logt(b, ft(b ** n))}$ より ${logt(b, _par(A))}{op}{logt(b, ft(b ** n))}$。",
                     f"底 ${ft(b)}$ は $1$ より{'大きい' if inc else '小さい'}ので ${A}{(('\\leqq' if eq else '<') if inner_less else ('\\geqq' if eq else '>'))}{ft(b ** n)}$。",
                     f"真数条件と合わせて ${ans}$。"],
              alt=[f"$y={logt(b, 'x')}$ のグラフ（底が $1$ より{'大きいので増加' if inc else '小さいので減少'}）をかき、$y={n}$ との上下関係から読み取る。"],
              pc=[("真数条件を示している", 1), ("底と $1$ の大小から不等号の向きを正しく決めている", 2), ("範囲を正しく答えている", 1)],
              pit=["底が $1$ より小さいのに不等号の向きを変えない。", "真数条件 $x>" + str(p) + "$ を落とす。"],
              chk=(f"[{p}, {p}+({fp(b)})**({n})]", f"[{p}, {fp(bound)}]", None, "intermediate"))


PAIRS = [(2, 3), (3, 2), (2, 5), (5, 2), (3, 5)]


@gen("standard_practice", 4, ["computation", "multiple_solutions"])
def change_base(r):
    p, q = r.choice(PAIRS)
    a1, a2, b1, b2 = (r.choice([1, 2, 3]) for _ in range(4))
    t1 = f"{logt(p, q ** a1)}+{logt(p * p, q ** a2)}"
    t2 = f"{logt(q, p ** b1)}+{logt(q * q, p ** b2)}"
    X, Y = F(a1) + F(a2, 2), F(b1) + F(b2, 2)
    v = X * Y
    return sa(f"次の式の値を求めなさい。$$\\left({t1}\\right)\\left({t2}\\right)$$", f"${ft(v)}$",
              f"底の変換公式で底を ${p}$ にそろえ、$\\log_{{{p}}}{q}=L$ とおくと、第1因数は ${ft(X)}L$、第2因数は $\\dfrac{{{ft(Y)}}}{{L}}$。", d=3,
              ap="底がばらばらなので、底の変換公式で同じ底にそろえる。$\\log_{" + str(p) + "}" + str(q) + "=L$ とおくと見通しがよい。",
              steps=[f"${logt(p, q ** a1)}={a1}L$、${logt(p * p, q ** a2)}=\\dfrac{{\\log_{{{p}}}{q ** a2}}}{{\\log_{{{p}}}{p * p}}}=\\dfrac{{{a2}L}}{{2}}$ より、第1因数 $={ft(X)}L$。",
                     f"${logt(q, p ** b1)}=\\dfrac{{{b1}}}{{L}}$、${logt(q * q, p ** b2)}=\\dfrac{{{b2}}}{{2L}}$ より、第2因数 $=\\dfrac{{{ft(Y)}}}{{L}}$。",
                     f"積は ${ft(X)}\\times{ft(Y)}={ft(v)}$。"],
              alt=[f"底をすべて ${q}$ や $10$ にそろえても同じ値になる（底の選び方によらない）。", f"$\\log_{{{p}}}{q}\\cdot\\log_{{{q}}}{p}=1$ を使って、展開した各項を計算してもよい。"],
              pc=[("底の変換公式で底をそろえている", 1), ("各因数を正しく簡単にしている", 2), ("値が正しい", 1)],
              pit=[f"$\\log_{{{p * p}}}M$ を $2\\log_{{{p}}}M$ としてしまう（正しくは $\\dfrac12\\log_{{{p}}}M$）。"],
              chk=(f"(log({q ** a1},{p})+log({q ** a2},{p * p}))*(log({p ** b1},{q})+log({p ** b2},{q * q}))", fp(v), None, "intermediate"))


# ======================================================================
# C 思考力・記述応用
# ======================================================================

L2, L3 = F(3010, 10000), F(4771, 10000)
DIG = {2: (1, 0, 0), 3: (0, 1, 0), 5: (-1, 0, 1), 6: (1, 1, 0), 12: (2, 1, 0), 15: (-1, 1, 1), 18: (1, 2, 0), 24: (3, 1, 0)}
DEC = {"\\dfrac{1}{2}": (F(1, 2), (-1, 0, 0)), "\\dfrac{1}{3}": (F(1, 3), (0, -1, 0)), "\\dfrac{2}{3}": (F(2, 3), (1, -1, 0)), "\\dfrac{3}{4}": (F(3, 4), (-2, 1, 0)),
       "\\dfrac{4}{5}": (F(4, 5), (3, 0, -1)), "\\dfrac{1}{6}": (F(1, 6), (-1, -1, 0)), "\\dfrac{5}{9}": (F(5, 9), (-1, -2, 1)), "0.6": (F(3, 5), (1, 1, -1))}


def _logexpr(c):
    a, b, g = c
    parts = []
    if a:
        parts.append(f"{a}\\log_{{10}}2" if a not in (1, -1) else ("" if a == 1 else "-") + "\\log_{10}2")
    if b:
        s = f"{b}\\log_{{10}}3" if b not in (1, -1) else ("" if b == 1 else "-") + "\\log_{10}3"
        parts.append(s if (not parts or s.startswith("-")) else "+" + s)
    if g:
        parts.append(("+" if g > 0 and parts else "") + str(g))
    return "".join(parts)


@gen("thinking_writing", 3, ["computation", "written_reasoning", "application"])
def common_log(r):
    while True:
        if r.random() < 0.55:
            b = r.choice(list(DIG))
            n = r.randint(15, 60)
            c = DIG[b]
            lv = n * (c[0] * L2 + c[1] * L3 + c[2])
            exact = len(str(b ** n))
            approx = math.floor(lv) + 1
            fr = lv - math.floor(lv)
            if exact == approx and 0.01 < fr < 0.99:
                kind = "dig"
                break
        else:
            name, (x, c) = r.choice(list(DEC.items()))
            n = r.randint(10, 50)
            lv = n * (c[0] * L2 + c[1] * L3 + c[2])
            X = x ** n
            k = 1
            while X * 10 ** k < 1:
                k += 1
            approx = -math.floor(lv)
            fr = lv - math.floor(lv)
            if k == approx and 0.01 < fr < 0.99:
                kind = "dec"
                b = name
                break
    pre = "$\\log_{10}2=0.3010,\\ \\log_{10}3=0.4771$ とする。"
    lexpr = _logexpr(c)
    lvs = f"{float(lv):.4f}".rstrip("0")
    if kind == "dig":
        fl = math.floor(lv)
        return desc(pre + f"${b}^{{{n}}}$ は何桁の整数か。求め方も示しなさい。", f"{approx}桁",
                    f"$\\log_{{10}}{b}^{{{n}}}={n}({lexpr})={lvs}$ より $10^{{{fl}}}<{b}^{{{n}}}<10^{{{fl + 1}}}$。",
                    [("常用対数をとり、与えられた値で正しく計算している", 3), ("$10^{n-1}\\leqq N<10^n$ の形の不等式で評価している", 3), ("桁数を正しく答えている", 2)], d=4, p=8, lines=7,
                    ap="$N$ が $k$ 桁 $\\iff10^{k-1}\\leqq N<10^k\\iff k-1\\leqq\\log_{10}N<k$。常用対数の値を計算し、整数部分に注目する。",
                    steps=[f"$\\log_{{10}}{b}^{{{n}}}={n}\\log_{{10}}{b}={n}({lexpr})$。" + ("（$\\log_{10}5=\\log_{10}\\dfrac{10}{2}=1-\\log_{10}2$ を用いる）" if c[2] else ""),
                           f"$={lvs}$。", f"${fl}<\\log_{{10}}{b}^{{{n}}}<{fl + 1}$ より $10^{{{fl}}}<{b}^{{{n}}}<10^{{{fl + 1}}}$。", f"よって {approx} 桁。"],
                    alt=[f"$10^{{{fl}}}$ が ${fl + 1}$ 桁の最小の数であることから、$10^{{{fl}}}$ 以上 $10^{{{fl + 1}}}$ 未満の整数は ${fl + 1}$ 桁と確かめる。"],
                    pc=[("常用対数の計算", 3), ("不等式による評価", 3), ("桁数", 2)],
                    pit=[f"整数部分 ${fl}$ をそのまま桁数と答える。", "$\\log_{10}5$ を $\\log_{10}2+\\log_{10}3$ などと誤って表す。" if c[2] else "掛け算の途中で小数点の位置を誤る。"],
                    chk=(f"floor({n}*(({c[0]})*Rational(3010,10000)+({c[1]})*Rational(4771,10000)+({c[2]})))+1", str(approx), None, "intermediate"))
    fl = math.floor(lv)
    return desc(pre + f"$\\left({b}\\right)^{{{n}}}$ を小数で表すと、小数第何位に初めて $0$ でない数字が現れるか。求め方も示しなさい。", f"小数第{approx}位",
                f"$\\log_{{10}}\\left({b}\\right)^{{{n}}}={lvs}$ より $10^{{{fl}}}<\\left({b}\\right)^{{{n}}}<10^{{{fl + 1}}}$。",
                [("常用対数をとり、与えられた値で正しく計算している", 3), ("$10^{-k}\\leqq x<10^{-k+1}$ の形の不等式で評価している", 3), ("位を正しく答えている", 2)], d=4, p=8, lines=7,
                ap="$0<x<1$ のとき、小数第 $k$ 位に初めて $0$ でない数字が現れる $\\iff10^{-k}\\leqq x<10^{-k+1}$。常用対数の値が負になることに注意する。",
                steps=[f"$\\log_{{10}}\\left({b}\\right)^{{{n}}}={n}({lexpr})$。", f"$={lvs}$。",
                       f"${fl}<{lvs}<{fl + 1}$ より $10^{{{fl}}}<\\left({b}\\right)^{{{n}}}<10^{{{fl + 1}}}$。", f"よって小数第 {approx} 位に初めて $0$ でない数字が現れる。"],
                alt=[f"$10^{{{fl}}}$ は小数第 ${-fl}$ 位に初めて $1$ が現れる数で、$10^{{{fl + 1}}}$ 未満の数は小数第 ${-fl - 1}$ 位までがすべて $0$ であることから確かめる。"],
                pc=[("常用対数の計算", 3), ("不等式による評価", 3), ("位", 2)],
                pit=[f"負の数 ${lvs}$ の整数部分を ${fl + 1}$ と考えて、1つずれた位を答える。"],
                chk=(f"-floor({n}*(({c[0]})*Rational(3010,10000)+({c[1]})*Rational(4771,10000)+({c[2]})))", str(approx), None, "intermediate"))


EXP_DOMS = [(-1, 2), (0, 2), (0, 3), (-1, 3), (1, 3), (-2, 1), (-1, 1)]


@gen("thinking_writing", 3, ["cross_unit", "written_reasoning", "condition_check"], rel=["HS-MATH1-U03"])
def exp_log_maxmin(r):
    d = r.randint(-3, 3)
    if r.random() < 0.5:
        c = r.choice([2, 4, 6, 8])
        lo, hi = r.choice(EXP_DOMS)
        tl, th = F(2) ** lo, F(2) ** hi
        t0 = F(c, 2)

        def y(t):
            return t * t - c * t + d

        def xt(t):
            k = ilog(t, 2)
            return str(k) if k is not None else f"\\log_{{2}}{ft(t)}"
        f = f"y=4^x-{c}\\cdot2^x{'+' if d > 0 else '-' if d < 0 else ''}{abs(d) if d else ''}"
        rng = f"{lo}\\leqq x\\leqq{hi}"
        sub = "2^x=t"
        trng = f"{ft(tl)}\\leqq t\\leqq{ft(th)}"
        why = "$2^x$ は増加関数なので"
    else:
        c = r.choice([-2, 2, 4, 6])
        lo, hi = r.choice(EXP_DOMS)
        tl, th = F(lo), F(hi)
        t0 = F(c, 2)

        def y(t):
            return t * t - c * t + d

        def xt(t):
            return ft(F(2) ** int(t)) if F(t).denominator == 1 else f"2^{{{fs(t)}}}"
        ct = "" if c == 0 else (f"-{c}" if c > 0 else f"+{abs(c)}")
        f = f"y=(\\log_{{2}}x)^2{ct}\\log_{{2}}x{'+' if d > 0 else '-' if d < 0 else ''}{abs(d) if d else ''}"
        rng = f"{ft(F(2) ** lo)}\\leqq x\\leqq{ft(F(2) ** hi)}"
        sub = "\\log_{2}x=t"
        trng = f"{lo}\\leqq t\\leqq{hi}"
        why = "$\\log_{2}x$ は増加関数なので"
    cand = [tl, th] + ([t0] if tl <= t0 <= th else [])
    M = max(y(t) for t in cand)
    m = min(y(t) for t in cand)
    tM = sorted({t for t in cand if y(t) == M})
    tm = sorted({t for t in cand if y(t) == m})
    ans = f"最大値 ${ft(M)}$（$x=" + ",\\ ".join(xt(t) for t in tM) + f"$）、最小値 ${ft(m)}$（$x=" + ",\\ ".join(xt(t) for t in tm) + "$）"
    q = poly(1, -c, d, var="t")
    vt = f"t={ft(t0)}"
    return desc(f"関数 ${f}\\ \\left({rng}\\right)$ の最大値と最小値、およびそれらをとるときの $x$ の値を求めなさい。", ans,
                f"${sub}$ とおくと ${trng}$ で $y={q}$。二次関数の定義域つき最大・最小の問題になる。",
                [("適切に置きかえ、$t$ の変域を正しく求めている", 3), ("$t$ の二次関数の最大・最小を正しく求めている", 3), ("対応する $x$ の値を正しく求めている", 2)], d=4, p=8, lines=10,
                ap=f"${sub}$ とおくと $y$ は $t$ の二次関数になる。{why}、$x$ の変域から $t$ の変域が決まる。あとは数学Ⅰの「定義域つきの最大・最小」と同じ。",
                steps=[f"${sub}$ とおく。{why} ${rng}$ のとき ${trng}$。", f"$y={q}=\\left(t{'-' if t0 > 0 else '+'}{ft(abs(t0))}\\right)^2" + ("" if y(t0) == 0 else ("+" if y(t0) > 0 else "-") + ft(abs(y(t0)))) + f"$（軸 ${vt}$）。",
                       f"変域内の端点と軸の位置を比べ、最大値 ${ft(M)}$、最小値 ${ft(m)}$。", f"対応する $x$ を求めて、{ans}。"],
                alt=["$t$ の変域の端点と軸での $y$ の値をすべて計算して比較してもよい。", "グラフ（放物線）をかいて、変域の部分の最高点・最低点を読む。"],
                pc=[("置きかえと変域", 3), ("最大・最小", 3), ("$x$ の値", 2)],
                pit=["$t$ の変域を考えず、頂点の値をそのまま最小値とする。", "最大・最小をとる $t$ の値を、$x$ に戻さずに答える。"],
                chk=(f"[({fp(tM[0])})**2-({c})*({fp(tM[0])})+({d}), ({fp(tm[0])})**2-({c})*({fp(tm[0])})+({d})]", f"[{fp(M)}, {fp(m)}]", None, "intermediate"))


PROOFS = [
    ("$a>0,\\ a\\neq1,\\ M>0,\\ N>0$ のとき、$\\log_aMN=\\log_aM+\\log_aN$ を証明しなさい。",
     "$\\log_aM=p,\\ \\log_aN=q$ とおくと $M=a^p,\\ N=a^q$。$MN=a^pa^q=a^{p+q}$ なので、対数の定義より $\\log_aMN=p+q=\\log_aM+\\log_aN$。",
     "対数を文字でおいて指数の形に直し、指数法則を使ってから対数の定義に戻る。",
     ["$\\log_aM=p,\\ \\log_aN=q$ とおく。", "$M=a^p,\\ N=a^q$ より $MN=a^{p+q}$。", "対数の定義から $\\log_aMN=p+q$。"],
     ["$a=2,\\ M=4,\\ N=8$ で両辺を計算すると、左辺 $\\log_232=5$、右辺 $2+3=5$（検算）。"], "log(32,2)-log(4,2)-log(8,2)"),
    ("$a>0,\\ a\\neq1,\\ M>0$、$r$ を実数とするとき、$\\log_aM^r=r\\log_aM$ を証明しなさい。",
     "$\\log_aM=p$ とおくと $M=a^p$。$M^r=(a^p)^r=a^{pr}$ なので、対数の定義より $\\log_aM^r=pr=r\\log_aM$。",
     "$\\log_aM=p$ とおき、指数法則 $(a^p)^r=a^{pr}$ を使う。",
     ["$\\log_aM=p$ とおくと $M=a^p$。", "$M^r=a^{pr}$。", "対数の定義から $\\log_aM^r=pr$。"],
     ["$a=3,\\ M=9,\\ r=3$ で、左辺 $\\log_3729=6$、右辺 $3\\times2=6$（検算）。"], "log(729,3)-3*log(9,3)"),
    ("$a,\\ b,\\ c$ は正の数で、$a\\neq1,\\ c\\neq1$ とする。底の変換公式 $\\log_ab=\\dfrac{\\log_cb}{\\log_ca}$ を証明しなさい。",
     "$\\log_ab=p$ とおくと $a^p=b$。両辺の $c$ を底とする対数をとると $p\\log_ca=\\log_cb$。$a\\neq1$ より $\\log_ca\\neq0$ なので $p=\\dfrac{\\log_cb}{\\log_ca}$。",
     "$\\log_ab=p$ とおいて指数の形に直し、両辺の $c$ を底とする対数をとる。",
     ["$a^p=b$。", "$\\log_ca^p=\\log_cb$ より $p\\log_ca=\\log_cb$。", "$\\log_ca\\neq0$ を確認して割る。"],
     ["$a=4,\\ b=8,\\ c=2$ で、左辺 $\\log_48=\\dfrac32$、右辺 $\\dfrac{3}{2}$（検算）。"], "log(8,4)-log(8,2)/log(4,2)"),
    ("$\\log_23$ が無理数であることを証明しなさい。",
     "$\\log_23$ が有理数であると仮定する。$\\log_23>0$ なので、正の整数 $m,\\ n$ を用いて $\\log_23=\\dfrac{m}{n}$ と表せる。このとき $2^{\\frac{m}{n}}=3$、両辺を $n$ 乗して $2^m=3^n$。左辺は偶数、右辺は奇数なので矛盾。よって $\\log_23$ は無理数である。",
     "背理法を用いる。有理数 $\\dfrac{m}{n}$ とおいて指数の形に直し、偶奇を比べる。",
     ["有理数と仮定し $\\log_23=\\dfrac{m}{n}$（$m,\\ n$ は正の整数）とおく。", "$2^m=3^n$ を導く。", "偶数＝奇数となり矛盾。"],
     ["$\\log_23\\fallingdotseq1.585$ は $1$ と $2$ の間にあり、整数でないことは $2<3<4$ からすぐ分かる（ただしこれだけでは無理数の証明にならない）。"], "log(3,2)*log(2,3)-1"),
    ("$a>0,\\ a\\neq1,\\ b>0,\\ b\\neq1$ のとき、$\\log_ab\\cdot\\log_ba=1$ を証明しなさい。",
     "底の変換公式で底を $a$ にそろえると、$\\log_ba=\\dfrac{\\log_aa}{\\log_ab}=\\dfrac{1}{\\log_ab}$（$b\\neq1$ より $\\log_ab\\neq0$）。よって $\\log_ab\\cdot\\log_ba=1$。",
     "底の変換公式で底をそろえる。",
     ["$\\log_ba=\\dfrac{\\log_aa}{\\log_ab}$。", "$\\log_aa=1$、$\\log_ab\\neq0$ を確認。", "積が $1$ になる。"],
     ["$\\log_ab=p$ とおくと $a^p=b$。両辺を $\\dfrac1p$ 乗して $a=b^{\\frac1p}$、よって $\\log_ba=\\dfrac1p$ としても示せる。"], "log(5,2)*log(2,5)-1"),
    ("$a>1$ のとき、関数 $y=a^x$ が増加関数であること、すなわち $p<q$ ならば $a^p<a^q$ であることを証明しなさい。ただし、$a>1,\\ r>0$ ならば $a^r>1$ であることは用いてよい。",
     "$p<q$ とすると $q-p>0$ なので $a^{q-p}>1$。$a^p>0$ を両辺に掛けて $a^p\\cdot a^{q-p}>a^p$、すなわち $a^q>a^p$。",
     "差 $q-p>0$ を指数にもつ $a^{q-p}$ に注目し、指数法則 $a^pa^{q-p}=a^q$ を使う。",
     ["$q-p>0$ より $a^{q-p}>1$。", "$a^p>0$ を掛ける。", "$a^q>a^p$。"],
     ["$a^q-a^p=a^p(a^{q-p}-1)$ と因数分解し、$a^p>0,\\ a^{q-p}-1>0$ から正であることを示してもよい。"], "2**3-2**2*2**1"),
]


@gen("thinking_writing", 2, ["written_reasoning", "concept"])
def proof_item(r):
    stem, ans, ex, steps, alt, ck = r.choice(PROOFS)
    return desc(stem, ans, ex, [("方針（文字のおき方・使う法則）が正しい", 3), ("式変形・論理が正確である", 3), ("結論を明記している", 2)],
                d=4, p=8, kind="proof", lines=8, ap=ex, steps=steps, alt=alt, pc=[("方針", 3), ("論理", 3), ("結論", 2)],
                pit=["示すべき性質そのものを途中で使ってしまう（循環論法）。", "底や真数の条件（$a\\neq1$、$\\log_ca\\neq0$ など）にふれずに割り算をする。"],
                chk=(ck, "0", "numeric", "intermediate"))


ROOT_POOL = [(2, 2), (3, 3), (5, 5), (6, 6), (4, 3), (5, 4), (3, 4), (2, 3), (7, 3), (10, 5)]


@gen("thinking_writing", 2, ["written_reasoning", "multiple_solutions"])
def compare_roots(r):
    while True:
        trio = r.sample(ROOT_POOL, 3)
        L = math.lcm(*[k for _, k in trio])
        pw = [b ** (L // k) for b, k in trio]
        if len(set(pw)) == 3 and max(pw) <= 200000:
            break
    order = sorted(range(3), key=lambda i: pw[i])
    ans = "<".join(root_t(trio[i][0], trio[i][1]) for i in order)
    return desc("次の3つの数を小さい順に並べなさい。理由も示すこと。$$" + ",\\quad ".join(root_t(b, k) for b, k in trio) + "$$", f"${ans}$",
                f"3つとも正の数なので、${L}$ 乗した値で比べる：" + "、".join(f"${pw[i]}$" for i in range(3)) + "。",
                [("すべて正であることと、同じ数で累乗して比べる方針を示している", 3), ("累乗した値を正しく計算している", 3), ("正しい順に並べている", 2)], d=4, p=8, lines=7,
                ap=f"根号の指数（$k$ 乗根の $k$）がそろっていない。$a>0,\\ b>0$ のとき $a<b\\iff a^n<b^n$ なので、指数の最小公倍数 ${L}$ 乗して整数にそろえる。",
                steps=[f"各数を ${L}$ 乗する（すべて正なので大小関係は変わらない）。"] + [f"$\\left({root_t(b, k)}\\right)^{{{L}}}={b}^{{{L // k}}}={p}$。" for (b, k), p in zip(trio, pw)]
                + [f"よって ${ans}$。"],
                alt=["常用対数をとって $\\dfrac{1}{k}\\log_{10}b$ の大小を比べてもよい（$\\log_{10}$ は増加関数）。"],
                pc=[("方針", 3), ("累乗の計算", 3), ("順序", 2)],
                pit=["根号の中の数が大きい方が大きいと決めつける。", "$k$ 乗根の $k$ が大きいほど大きいと考える。"],
                chk=(f"[{', '.join(f'{b}**{L // k}' for b, k in trio)}]", f"[{', '.join(map(str, pw))}]", None, "intermediate"))


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(stem, wrong, step, etype, tempt, fix, ans, expl, steps, ap, alt, pit, chk=None, d=3):
    return desc(f"{stem}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい答えを求めなさい。", ans, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい解答を途中式とともに示している", 3), ("最終的な答えが正しい", 1)], d=d, p=6, lines=6,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい途中式", 3), ("正しい答え", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix), chk=chk)


@gen("error_correction", 3, ["common_error", "computation"])
def err_log_rule(r):
    a = r.choice([2, 3, 5, 6, 10])
    if r.random() < 0.5:
        a = r.choice([6, 10, 12])
        n = r.choice([2, 3] if a == 6 else [2])
        ds = [d for d in _divisors(a ** n) if ilog(d, a) is None and ilog(F(a ** n, d), a) is None]
        M = r.choice(ds)
        N = a ** n // M
        return err_item(f"${logt(a, M)}+{logt(a, N)}$ を簡単にしなさい。", f"${logt(a, M)}+{logt(a, N)}={logt(a, f'({M}+{N})')}={logt(a, M + N)}$",
                        "$\\log_aM+\\log_aN=\\log_a(M+N)$ とした部分", "formula",
                        "「たし算はたし算のまま」という見た目の対応で公式を作ってしまっている。対数の和は真数の積に対応する。",
                        f"${logt(a, M)}+{logt(a, N)}={logt(a, M * N)}={n}$", f"${n}$",
                        "対数の性質は $\\log_aM+\\log_aN=\\log_aMN$（真数は積）。",
                        [f"${logt(a, M)}+{logt(a, N)}={logt(a, f'({M}\\times{N})')}$。", f"$={logt(a, a ** n)}={n}$。"],
                        "対数の性質は「$\\log$ の和 ⇔ 真数の積」。指数法則 $a^pa^q=a^{p+q}$ と対応させて確認する。",
                        [f"$\\log_{{{a}}}{M},\\ \\log_{{{a}}}{N}$ の概数を電卓で求めて足すと ${n}$ に近くなり、生徒の答えとは一致しないことで確かめられる。"],
                        ["公式を指数法則と対応させて覚える。"], chk=(f"log({M},{a})+log({N},{a})", str(n), None, "intermediate"))
    n = r.choice([1, 2])
    cands = [(P, P * P // a ** n) for P in range(2, 31) if (P * P) % (a ** n) == 0 and P * P // a ** n > 1 and ilog(P, a) is None and (2 * P) % (P * P // a ** n) != 0]
    if not cands:
        cands = [(P, P * P // a ** n) for P in range(2, 31) if (P * P) % (a ** n) == 0 and P * P // a ** n > 1 and ilog(P, a) is None]
    P, Q = r.choice(cands)
    wv = F(2 * P, Q)
    return err_item(f"$2{logt(a, P)}-{logt(a, Q)}$ を簡単にしなさい。", f"$2{logt(a, P)}-{logt(a, Q)}={logt(a, 2 * P)}-{logt(a, Q)}={logt(a, ft(wv))}$",
                    f"$2{logt(a, P)}={logt(a, 2 * P)}$ とした部分", "formula",
                    "係数の $2$ を真数に「掛ける」と考えてしまっている。$r\\log_aM=\\log_aM^r$ で、係数は真数の指数になる。",
                    f"$2{logt(a, P)}={logt(a, P * P)}$ より、${logt(a, f'\\dfrac{{{P * P}}}{{{Q}}}')}={logt(a, a ** n)}={n}$", f"${n}$",
                    "係数は真数の指数に移る：$r\\log_aM=\\log_aM^r$。",
                    [f"$2{logt(a, P)}={logt(a, f'{P}^2')}={logt(a, P * P)}$。", f"${logt(a, P * P)}-{logt(a, Q)}={logt(a, f'\\dfrac{{{P * P}}}{{{Q}}}')}$。", f"$={logt(a, a ** n)}={n}$。"],
                    "係数つきの対数は、先に $\\log_aM^r$ の形に直してからまとめる。",
                    [f"$2{logt(a, P)}$ を $\\log_{{{a}}}{P}+\\log_{{{a}}}{P}=\\log_{{{a}}}({P}\\times{P})$ と見れば、真数が2乗になることが分かる。"],
                    ["$r\\log_aM=\\log_aM^r$ を指数法則 $(a^p)^r=a^{pr}$ と対応させて確認する。"], chk=(f"2*log({P},{a})-log({Q},{a})", str(n), None, "intermediate"))


@gen("error_correction", 3, ["common_error", "condition_check"])
def err_antilog(r):
    a, n, k, s, good, bad = _log_eq(r)
    A, B = _lin(s), _lin(s - k)
    cond = f"x>{max(-s, k - s)}"
    return err_item(f"方程式 ${logt(a, _par(A))}+{logt(a, _par(B))}={n}$ を解きなさい。",
                    f"${_par(A)}{_par(B)}={a ** n}$ を解いて $x={good},\\ {bad}$",
                    "最後に解の吟味（真数条件の確認）をしていない部分", "condition",
                    "対数をまとめた後は普通の二次方程式になるため、もとの式に対数があったこと（真数は正）を忘れてしまう。",
                    f"真数条件 ${cond}$ より $x={bad}$ は不適。$x={good}$", f"$x={good}$",
                    f"真数条件は ${A}>0$ かつ ${B}>0$、すなわち ${cond}$。",
                    [f"真数条件：${cond}$。", f"${_par(A)}{_par(B)}={a ** n}$ より $x={good},\\ {bad}$。", f"${cond}$ を満たすのは $x={good}$。"],
                    "対数の方程式では、最初に真数条件を書き、最後に解がそれを満たすか確かめる。",
                    [f"$x={bad}$ を代入すると真数 ${bad + s}$ が負になり、$\\log$ が定義されないことから不適と分かる。"],
                    ["真数条件を最初に書く。"], chk=(f"solve(({A})*({B})-{a ** n}, x)", f"[{bad}, {good}]", "set", "intermediate"))


@gen("error_correction", 2, ["common_error", "condition_check"])
def err_base_small(r):
    b = r.choice([F(1, 2), F(1, 3)])
    m = r.choice([2, 3, 4])
    s = r.choice([0, 1, -1, 2])
    gt = r.random() < 0.5
    op = ">" if gt else "<"
    rop = "<" if gt else ">"
    if r.random() < 0.5:
        A = _lin(-s)
        rhs = b ** m
        bound = m + s
        return err_item(f"不等式 $\\left({ft(b)}\\right)^{{{A}}}{op}{ft(rhs)}$ を解きなさい。",
                        f"${ft(rhs)}=\\left({ft(b)}\\right)^{{{m}}}$ より ${A}{op}{m}$、よって $x{op}{bound}$",
                        "指数を比べるときに不等号の向きをそのままにした部分", "sign",
                        "底が $1$ より大きいときの解き方（不等号の向きはそのまま）を、底が $1$ より小さい場合にも当てはめている。",
                        f"底 ${ft(b)}<1$ なので ${A}{rop}{m}$、よって $x{rop}{bound}$", f"$x{rop}{bound}$",
                        f"$y=\\left({ft(b)}\\right)^x$ は減少関数なので、関数の値の大小と指数の大小は逆になる。",
                        [f"${ft(rhs)}=\\left({ft(b)}\\right)^{{{m}}}$。", f"底 ${ft(b)}$ は $0$ と $1$ の間なので、不等号の向きが変わる：${A}{rop}{m}$。", f"$x{rop}{bound}$。"],
                        "底と $1$ の大小を、指数を比べる前に必ず確認する。",
                        [f"両辺の逆数をとると $\\left({ft(1 / b)}\\right)^{{{A}}}{rop}{ft(1 / rhs)}$ となり、底が $1$ より大きい形で解ける。",
                         f"$x={bound + (1 if not gt else -1)}$ などを代入して確かめる。"],
                        ["底が $1$ より小さいときは不等号の向きが逆。"], chk=(f"({fp(b)})**({m})", fp(rhs), None, "intermediate"))
    A = _lin(-s)
    bound = s + b ** m
    return err_item(f"不等式 ${logt(b, _par(A))}{op}{m}$ を解きなさい。",
                    f"${m}={logt(b, ft(b ** m))}$ より ${A}{op}{ft(b ** m)}$、よって $x{op}{ft(bound)}$",
                    "真数を比べるときに不等号の向きをそのままにした部分（と、真数条件の確認もれ）", "condition",
                    "底が $1$ より小さい対数関数は減少関数であることを意識せず、また真数条件 $" + A + ">0$ を考えていない。",
                    (f"底 ${ft(b)}<1$ なので ${A}<{ft(b ** m)}$、真数条件 $x>{s}$ と合わせて ${s}<x<{ft(bound)}$" if gt
                     else f"底 ${ft(b)}<1$ なので ${A}>{ft(b ** m)}$、よって $x>{ft(bound)}$（真数条件も満たす）"),
                    f"${s}<x<{ft(bound)}$" if gt else f"$x>{ft(bound)}$",
                    f"$y={logt(b, 'x')}$ は減少関数。真数の大小は対数の大小と逆になる。",
                    [f"真数条件：$x>{s}$。", f"${m}={logt(b, ft(b ** m))}$、底 ${ft(b)}<1$ より ${A}{rop}{ft(b ** m)}$。",
                     (f"真数条件と合わせて ${s}<x<{ft(bound)}$。" if gt else f"$x>{ft(bound)}$（これは真数条件を満たす）。")],
                    "対数の不等式は「真数条件 → 底と $1$ の大小 → 真数の比較」の順に処理する。",
                    ["$y=" + logt(b, "x") + "$ のグラフ（右下がり）をかいて確かめる。"],
                    ["真数条件と、底による不等号の向きの両方を確認する。"], chk=(f"[{s}, {s}+({fp(b)})**({m})]", f"[{s}, {fp(bound)}]", None, "intermediate"))


@gen("error_correction", 2, ["common_error", "concept"])
def err_exp_law(r):
    b = r.choice([2, 3, 4, 5])
    n = r.choice([2, 3] if b > 3 else [2, 3, 4])
    m = r.choice([1, 2, 3])
    while math.gcd(m, n) != 1:
        m = r.choice([1, 2, 3])
    base = b ** n
    if r.random() < 0.5:
        e = F(-m, n)
        right = F(1, b ** m)
        wrong = f"${base}^{{{fs(e)}}}=-{base}^{{{fs(-e)}}}=-{b ** m}$"
        return err_item(f"${base}^{{{fs(e)}}}$ の値を求めなさい。", wrong, "負の指数を「符号がマイナスになる」と解釈した部分", "concept",
                        "指数の $-$ を、数そのものの符号と混同している。$a^{-p}$ は逆数を表す。",
                        f"${base}^{{{fs(e)}}}=\\dfrac{{1}}{{{base}^{{{fs(-e)}}}}}={ft(right)}$", f"${ft(right)}$",
                        "$a^{-p}=\\dfrac{1}{a^p}$。底が正なら、どんな指数でも値は正。",
                        [f"${base}={b}^{{{n}}}$。", f"${base}^{{{fs(e)}}}={b}^{{{-m}}}$。", f"$=\\dfrac{{1}}{{{b ** m}}}$。"],
                        "負の指数は逆数。底 $a>0$ の累乗は常に正であることで検算する。",
                        ["$a^x>0$（$a>0$）なので、負の答えはありえないと気づける。"], ["負の指数を見たら逆数を考える。"],
                        chk=(f"{base}**({fp(e)})", fp(right), None, "intermediate"), d=2)
    e = F(m, n)
    right = F(b) ** m
    wv = F(base ** m, n)
    return err_item(f"${base}^{{{fs(e)}}}$ の値を求めなさい。", f"${base}^{{{fs(e)}}}=\\dfrac{{{base}^{{{m}}}}}{{{n}}}={ft(wv)}$",
                    f"$a^{{\\frac{{m}}{{n}}}}$ を $\\dfrac{{a^m}}{{n}}$ とした部分", "concept",
                    "分数の指数の「分母」を、累乗根ではなく割り算だと思い込んでいる。",
                    f"${base}^{{{fs(e)}}}=\\left(\\sqrt[{n}]{{{base}}}\\right)^{{{m}}}={b}^{{{m}}}={b ** m}$", f"${b ** m}$",
                    "$a^{\\frac{m}{n}}=\\sqrt[n]{a^m}=\\left(\\sqrt[n]{a}\\right)^m$。分母は累乗根を表す。",
                    [f"$\\sqrt[{n}]{{{base}}}={b}$。", f"${base}^{{{fs(e)}}}={b}^{{{m}}}$。", f"$={b ** m}$。"],
                    "分数の指数は「分母が累乗根、分子が累乗」。",
                    [f"答えを ${n}$ 乗して ${base}^{{{m}}}$ に戻るかを確かめる：$({b ** m})^{{{n}}}={base ** m}$。"], ["$a^{\\frac{m}{n}}$ の定義を確認する。"],
                    chk=(f"{base}**({fp(e)})", str(b ** m), None, "intermediate"), d=2)


GENERATORS = [exp_value, root_law, log_value, log_props, exp_compare,
              exp_equation, exp_quad_eq, log_equation, log_ineq, change_base,
              common_log, exp_log_maxmin, proof_item, compare_roots,
              err_log_rule, err_antilog, err_base_small, err_exp_law]
