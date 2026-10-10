"""単元パック：数学B 数列。"""
from fractions import Fraction

import sympy as sp

from banks._common import desc, num, sa
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem, tp)

UNIT_ID = "HS-MATHB-U01"

N = sp.Symbol("n")
K = sp.Symbol("k")


# ---------------------------------------------------------------------------
# 補助
# ---------------------------------------------------------------------------

def tex(e):
    return sp.latex(sp.expand(e))


def lin_tex(a, b, var="n"):
    """a*var+b の LaTeX。"""
    return sp.latex(sp.expand(a * sp.Symbol(var) + b))


def geo_tex(c, p, alpha=0):
    """c*p^(n-1)+alpha の LaTeX。"""
    base = f"({p})" if p < 0 else str(p)
    if c == p:
        t = f"{base}^{{n}}"
        if alpha:
            t += f"+{alpha}" if alpha > 0 else f"{alpha}"
        return t
    head = "" if c == 1 else ("-" if c == -1 else f"{c}\\cdot ")
    t = f"{head}{base}^{{n-1}}"
    if alpha:
        t += f"+{alpha}" if alpha > 0 else f"{alpha}"
    return t


def geo_py(c, p, alpha=0):
    return f"({c})*({p})**(n-1)+({alpha})"


def fr_tex(v):
    v = Fraction(v)
    if v.denominator == 1:
        return str(v.numerator)
    s = "-" if v < 0 else ""
    return f"{s}\\dfrac{{{abs(v.numerator)}}}{{{v.denominator}}}"


LESSON = lesson(
    goals=["等差数列・等比数列の一般項と和を求め、和の公式を導出できる。",
           "$\\Sigma$ 記号の性質と $\\displaystyle\\sum k,\\ \\sum k^2$ などの公式を使って和を計算し、階差数列や和 $S_n$ から一般項を求められる。",
           "漸化式 $a_{n+1}=pa_n+q$ を解き、数学的帰納法で自然数についての命題を証明できる。"],
    duration=100,
    readiness=["文字式の展開・因数分解ができる。", "指数法則 $a^m\\cdot a^n=a^{m+n}$ を使える。", "命題・仮定・結論の意味（数学Ⅰ「集合と命題」）を理解している。"],
    flow=[("導入：並んだ数の規則", 8, "身近な数の並びから「前の項との関係」と「番号との関係」の2つの見方を引き出す"),
          ("等差数列・等比数列", 22, "一般項と和の公式の導出（逆順に並べて足す／$S-rS$）。例題1"),
          ("Σ 記号と和の公式", 20, "$\\Sigma$ の意味と性質、$\\displaystyle\\sum k^2$ の公式の導出（恒等式の和）"),
          ("階差数列と和からの一般項", 15, "階差数列の公式、$a_n=S_n-S_{n-1}\\ (n\\geqq2)$ と $n=1$ の確認"),
          ("漸化式", 20, "$a_{n+1}=pa_n+q$ を $a_{n+1}-\\alpha=p(a_n-\\alpha)$ に変形して解く。例題2"),
          ("数学的帰納法とまとめ", 15, "帰納法の2段階の構造（例題3）、確認問題")],
    sections=[
        intro("in1", "数の並びを2つの見方でとらえる",
              "数列 $3,\\ 7,\\ 11,\\ 15,\\ \\cdots$ は「前の項に $4$ を足すと次の項になる」と見ることも、「第 $n$ 項は $4n-1$」と見ることもできる。前者は漸化式、後者は一般項による表し方である。この単元では、この2つの見方を行き来しながら、和の計算や証明の方法を身につける。",
              bullets=["一般項：番号 $n$ の式で項を直接表す。", "漸化式：前の項（いくつか前の項）から次の項を決める規則。", "和 $S_n=a_1+a_2+\\cdots+a_n$ は $\\displaystyle\\sum_{k=1}^{n}a_k$ と書く。"],
              points=[tp("最初に数の並びを見せ、「次の数は何か」「100番目の数は何か」と2つの問いを続けて投げかける。", ask="100番目の数を、99番目までを計算せずに求めるにはどうすればよいか。",
                         expect="番号との関係（一般項）を見つければよい。", timing="導入の冒頭")]),
        definition("df1", "等差数列・等比数列",
                   "初項 $a$、公差 $d$ の等差数列は、各項に一定の数 $d$ を加えて次の項が得られる数列である。初項 $a$、公比 $r$ の等比数列は、各項に一定の数 $r$ を掛けて次の項が得られる数列である。",
                   formula="$$\\text{等差数列：}a_n=a+(n-1)d,\\qquad \\text{等比数列：}a_n=ar^{n-1}$$",
                   conditions=["第 $n$ 項までに公差を加える回数は $n-1$ 回（公比を掛ける回数も $n-1$ 回）。", "3つの数 $a,\\ b,\\ c$ がこの順に等差数列 $\\iff 2b=a+c$、等比数列 $\\iff b^2=ac$。"],
                   points=[tp("「$n-1$」の理由を、植木算（木と間の数）と結びつけて確認する。", caution="$a_n=a+nd$ と書く誤りが多い。")]),
        theorem("th1", "等差数列・等比数列の和",
                "$$S_n=\\dfrac{n(a+l)}{2}=\\dfrac{n\\{2a+(n-1)d\\}}{2},\\qquad S_n=\\dfrac{a(r^n-1)}{r-1}\\ (r\\neq1)$$",
                ["$l$ は末項（第 $n$ 項）。", "等比数列で $r=1$ のときは $S_n=na$。", "$r<1$ のときは $S_n=\\dfrac{a(1-r^n)}{1-r}$ の形が計算しやすい。"],
                proof=["（等差）$S_n=a_1+a_2+\\cdots+a_n$ と、逆順に並べた $S_n=a_n+a_{n-1}+\\cdots+a_1$ を辺々加える。",
                       "上下に並ぶ2項の和はどれも $a+l$ で、それが $n$ 組あるので $2S_n=n(a+l)$。",
                       "（等比）$S_n=a+ar+\\cdots+ar^{n-1}$、$rS_n=ar+ar^2+\\cdots+ar^n$。",
                       "上の式から下の式を引くと、間の項がすべて消えて $(1-r)S_n=a(1-r^n)$。$r\\neq1$ で割って公式を得る。"],
                points=[tp("等比数列の和の導出「$S-rS$」は、後の $\\displaystyle\\sum kr^{k-1}$ 型の和でも使うので、手順として身につけさせる。", ask="$rS_n$ と $S_n$ を1つずらして並べると、何が見えるか。")]),
        example("ex1", "例題1　等比数列の和",
                "初項 $3$、公比 $2$ の等比数列の初項から第 $6$ 項までの和を求めよ。",
                ["$S_6=\\dfrac{3(2^6-1)}{2-1}$。", "$=3\\times63=189$。"],
                "$189$",
                thinking="初項・公比・項数がそろっているので、和の公式に代入する。項数は $6$。",
                points=[tp("項を書き出して $3+6+12+24+48+96=189$ と確かめさせ、公式への信頼を育てる。")],
                misconceptions=[("$S_6=\\dfrac{3(2^5-1)}{2-1}=93$ とする", "和の公式の指数は項数 $n$ そのもの：$2^6$")]),
        theorem("th2", "Σ 記号と和の公式",
                "$$\\sum_{k=1}^{n}k=\\dfrac{1}{2}n(n+1),\\quad \\sum_{k=1}^{n}k^2=\\dfrac{1}{6}n(n+1)(2n+1),\\quad \\sum_{k=1}^{n}k^3=\\left\\{\\dfrac{1}{2}n(n+1)\\right\\}^2,\\quad \\sum_{k=1}^{n}c=nc$$",
                ["$\\displaystyle\\sum_{k=1}^{n}(pa_k+qb_k)=p\\sum_{k=1}^{n}a_k+q\\sum_{k=1}^{n}b_k$（$p,\\ q$ は $k$ に無関係な定数）。", "$\\displaystyle\\sum_{k=1}^{n}c$ は $c$ を $n$ 個足したものなので $nc$（$c$ ではない）。"],
                proof=["恒等式 $(k+1)^3-k^3=3k^2+3k+1$ で $k=1,\\ 2,\\ \\cdots,\\ n$ とした $n$ 個の式を辺々加える。",
                       "左辺は隣どうしが打ち消し合って $(n+1)^3-1$。右辺は $\\displaystyle 3\\sum_{k=1}^{n}k^2+3\\cdot\\dfrac{1}{2}n(n+1)+n$。",
                       "$\\displaystyle 3\\sum_{k=1}^{n}k^2=(n+1)^3-1-\\dfrac{3}{2}n(n+1)-n=\\dfrac{1}{2}n(n+1)(2n+1)$。",
                       "両辺を $3$ で割って $\\displaystyle\\sum_{k=1}^{n}k^2=\\dfrac{1}{6}n(n+1)(2n+1)$。"],
                points=[tp("「隣どうしが打ち消し合う和」は、部分分数分解による和（$\\dfrac{1}{k(k+1)}$ 型）と同じ発想であることを予告しておく。")]),
        theorem("th3", "階差数列と一般項、和と一般項",
                "$$a_n=a_1+\\sum_{k=1}^{n-1}b_k\\ (n\\geqq2),\\qquad a_n=S_n-S_{n-1}\\ (n\\geqq2),\\quad a_1=S_1$$",
                ["$b_n=a_{n+1}-a_n$ を $\\{a_n\\}$ の階差数列という。", "どちらの式も $n\\geqq2$ でしか使えないので、最後に $n=1$ のときに成り立つかを確かめる。"],
                proof=["$a_2-a_1=b_1,\\ a_3-a_2=b_2,\\ \\cdots,\\ a_n-a_{n-1}=b_{n-1}$ の $n-1$ 個の式を辺々加える。",
                       "左辺は打ち消し合って $a_n-a_1$ となり、$a_n=a_1+\\displaystyle\\sum_{k=1}^{n-1}b_k$。",
                       "$S_n=S_{n-1}+a_n$（$n\\geqq2$）より $a_n=S_n-S_{n-1}$。$n=1$ では $S_0$ が定義されないので $a_1=S_1$ を別に求める。"],
                points=[tp("$\\Sigma$ の上端が $n-1$ になる理由を、式を $n-1$ 個並べた図で示す。", caution="上端を $n$ にする誤りが典型的。")]),
        derivation("dv1", "漸化式 $a_{n+1}=pa_n+q$ の解き方",
                   ["$p\\neq1$ のとき、$\\alpha=p\\alpha+q$ を満たす $\\alpha=\\dfrac{q}{1-p}$ を求める。",
                    "$a_{n+1}=pa_n+q$ から $\\alpha=p\\alpha+q$ を引くと $a_{n+1}-\\alpha=p(a_n-\\alpha)$。",
                    "数列 $\\{a_n-\\alpha\\}$ は初項 $a_1-\\alpha$、公比 $p$ の等比数列なので $a_n-\\alpha=(a_1-\\alpha)p^{n-1}$。",
                    "よって $a_n=(a_1-\\alpha)p^{n-1}+\\alpha$。"],
                   body="定数 $\\alpha$ を引くことで、等比数列に帰着させるのが要点である。",
                   points=[tp("$\\alpha$ は「数列が一定値 $\\alpha$ をとり続けるならその値」という意味をもつことを説明する。", ask="$a_1=\\alpha$ のとき、数列はどうなるか。", expect="ずっと $\\alpha$ のまま。")]),
        example("ex2", "例題2　漸化式",
                "$a_1=2,\\ a_{n+1}=3a_n-4$ で定められる数列 $\\{a_n\\}$ の一般項を求めよ。",
                ["$\\alpha=3\\alpha-4$ より $\\alpha=2$。", "$a_{n+1}-2=3(a_n-2)$。", "$a_1-2=0$ なので、$a_n-2=0\\cdot3^{n-1}=0$。"],
                "$a_n=2$（すべての項が $2$）",
                thinking="$a_{n+1}-\\alpha=3(a_n-\\alpha)$ の形に変形する。初項が $\\alpha$ と等しいときは特別な結果になる。",
                points=[tp("$a_1=\\alpha$ の特別な場合を例に選び、変形の意味（ずれ $a_n-\\alpha$ が公比 $p$ 倍される）を実感させる。続けて $a_1=5$ の場合 $a_n=3^n+2$ も求めさせる。")]),
        theorem("th4", "数学的帰納法",
                "$$\\text{[I] } P(1)\\ \\text{が成り立つ},\\quad \\text{[II] } P(k)\\Longrightarrow P(k+1)\\quad \\Longrightarrow\\quad \\text{すべての自然数 } n\\ \\text{で } P(n)$$",
                ["[II] では「$P(k)$ が成り立つと仮定して $P(k+1)$ を導く」。$P(k)$ そのものを証明するわけではない。", "[I] を省くと、正しくない命題でも [II] だけは示せてしまうことがある。"],
                proof=["[I] より $P(1)$ が成り立つ。", "[II] で $k=1$ とすると $P(2)$ が成り立つ。続けて $k=2$ とすると $P(3)$ が成り立つ。", "これをくり返すと、どの自然数 $n$ についても有限回で $P(n)$ に到達する。"],
                points=[tp("ドミノ倒しのたとえで、[I]（最初のドミノを倒す）と [II]（倒れたら次も倒れる）の両方が必要なことを説明する。", caution="[II] で結論 $P(k+1)$ を仮定に使ってしまう答案に注意。")]),
        example("ex3", "例題3　数学的帰納法",
                "すべての自然数 $n$ について $\\displaystyle\\sum_{k=1}^{n}k\\cdot2^{k-1}=(n-1)2^n+1$ が成り立つことを証明せよ。",
                ["[I] $n=1$ のとき、左辺 $=1$、右辺 $=0\\cdot2+1=1$ で成り立つ。",
                 "[II] $n=k$ のとき成り立つと仮定すると、$\\displaystyle\\sum_{i=1}^{k+1}i\\cdot2^{i-1}=(k-1)2^k+1+(k+1)2^k$。",
                 "$=2k\\cdot2^k+1=k\\cdot2^{k+1}+1=\\{(k+1)-1\\}2^{k+1}+1$ となり、$n=k+1$ のときも成り立つ。",
                 "[I]、[II] より、すべての自然数 $n$ で成り立つ。"],
                "（証明終）",
                thinking="$n=k+1$ の左辺を「$n=k$ の左辺＋第 $k+1$ 項」に分け、仮定を使う。目標の右辺 $(k+1-1)2^{k+1}+1$ を意識して変形する。",
                points=[tp("[II] の変形では、目標の式を先に書いておき、そこへ向かって式を整理するよう指導する。")]),
        board("bd1", "板書案",
              [("① 等差・等比", ["$a_n=a+(n-1)d$", "$a_n=ar^{n-1}$", "$S_n=\\dfrac{n(a+l)}{2}$", "$S_n=\\dfrac{a(r^n-1)}{r-1}$", "例1 $189$"]),
               ("② Σ・階差・和", ["$\\sum k=\\frac{1}{2}n(n+1)$", "$\\sum k^2=\\frac{1}{6}n(n+1)(2n+1)$", "$a_n=a_1+\\sum_{k=1}^{n-1}b_k$", "$a_n=S_n-S_{n-1}\\ (n\\geqq2)$", "$n=1$ を確認"]),
               ("③ 漸化式・帰納法", ["$a_{n+1}-\\alpha=p(a_n-\\alpha)$", "$\\alpha=p\\alpha+q$", "[I] $n=1$", "[II] $P(k)\\Rightarrow P(k+1)$", "例3"])],
              points=[tp("②の「$n\\geqq2$」と「$n=1$ を確認」は赤で囲み、毎回答案に書く習慣をつけさせる。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("一般項を求めたら、$n=1,\\ 2,\\ 3$ を代入して最初の数項と一致するか確かめさせる。", timing="各例題の後"),
               tp("$\\Sigma$ の計算では、定数項の和 $\\displaystyle\\sum_{k=1}^{n}c=nc$ を $c$ としてしまう誤りに注意させる。", ask="$\\displaystyle\\sum_{k=1}^{n}3$ は何か。", expect="$3n$"),
               tp("階差数列・和からの一般項では、$n\\geqq2$ で求めた式が $n=1$ でも成り立つか、必ず確認させる。", caution="$S_n$ に定数項があるときは $n=1$ で一致しない。"),
               tp("漸化式の変形後、$\\{a_n-\\alpha\\}$ が等比数列であることを言葉で書かせる（何が等比数列かを明示）。"),
               tp("帰納法の [II] では「仮定」「示すべき式」を最初に書き出させ、仮定をどこで使ったかを明示させる。")],
              misconceptions=[("等比数列の和で指数を $n-1$ にする", "和の公式では $r^n$（項数が指数）。一般項の $r^{n-1}$ と区別する"),
                              ("階差数列の公式で $\\displaystyle\\sum_{k=1}^{n}b_k$ とする", "差の式は $n-1$ 個なので上端は $n-1$"),
                              ("$S_n=n^2+n+1$ から $a_n=2n$ をすべての $n$ で成り立つとする", "$a_1=S_1=3$ で、$a_n=2n$ は $n\\geqq2$ のみ")]),
        summary("sm1", "まとめ",
                ["等差・等比の一般項と和の公式。和の導出は「逆順に足す」「$S-rS$」。",
                 "$\\Sigma$ の公式と性質。階差・和からの一般項は $n\\geqq2$ で求め、$n=1$ を確認。",
                 "$a_{n+1}=pa_n+q$ は $a_{n+1}-\\alpha=p(a_n-\\alpha)$。帰納法は [I] と [II] の両方が必要。"]),
        check("ck1", "確認問題",
              [("初項 $5$、公差 $-3$ の等差数列の第 $10$ 項を求めよ。", "$5+9\\times(-3)=-22$"),
               ("$\\displaystyle\\sum_{k=1}^{n}(3k-1)$ を求めよ。", "$\\dfrac{3}{2}n(n+1)-n=\\dfrac{1}{2}n(3n+1)$"),
               ("$a_1=1,\\ a_{n+1}=2a_n+3$ の一般項を求めよ。", "$a_{n+1}+3=2(a_n+3)$ より $a_n=4\\cdot2^{n-1}-3=2^{n+1}-3$")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

@gen("basic_check", 4, ["computation"])
def arith_term(r):
    a, d = r.randint(-15, 20), r.choice([x for x in range(-7, 8) if x])
    n = r.randint(8, 40)
    if (a, d, n) == (3, 4, 20):
        n = 21
    v = a + (n - 1) * d
    return num(f"初項が ${a}$、公差が ${d}$ である等差数列 $\\{{a_n\\}}$ について、第 ${n}$ 項 $a_{{{n}}}$ の値を求めなさい。", str(v),
               f"$a_n={a}+(n-1)\\cdot({d})$ より $a_{{{n}}}={a}+{n - 1}\\times({d})={v}$。", d=1,
               ap="等差数列の一般項 $a_n=a+(n-1)d$ に代入する。第 $n$ 項までに公差を加える回数は $n-1$ 回。",
               steps=[f"$a_n={a}+(n-1)\\cdot({d})={lin_tex(d, a - d)}$。", f"$n={n}$ を代入して $a_{{{n}}}={v}$。"],
               alt=[f"一般項 $a_n={lin_tex(d, a - d)}$ を先に求め、$n=1$ で ${a}$ になることを確認してから代入するとよい。"],
               pc=[("一般項の公式を正しく使っている", 1), ("値を正しく求めている", 1)],
               pit=[f"$a+nd$ として $a_{{{n}}}={a + n * d}$ としてしまう（公差を加える回数の誤り）。"],
               chk=(f"{a}+({n}-1)*({d})", str(v)))


@gen("basic_check", 4, ["computation"])
def geo_term(r):
    a = r.choice([1, 2, 3, -1, -2, 5, 4])
    p = r.choice([2, 3, -2, -3, 2, 4])
    n = r.randint(4, 8)
    v = a * p ** (n - 1)
    return num(f"初項 ${a}$、公比 ${p}$ の等比数列 $\\{{a_n\\}}$ の第 ${n}$ 項を求めなさい。", str(v),
               f"$a_n={geo_tex(a, p)}$ より $a_{{{n}}}={a}\\cdot({p})^{{{n - 1}}}={v}$。", d=1,
               ap="等比数列の一般項は $a_n=ar^{n-1}$。第 $n$ 項までに公比を掛ける回数は $n-1$ 回。",
               steps=[f"$a_n={geo_tex(a, p)}$。", f"$a_{{{n}}}={a}\\times({p})^{{{n - 1}}}={v}$。"],
               alt=["項を順に書き出して確かめる：" + "、".join(f"${a * p ** i}$" for i in range(n)) + "。"],
               pc=[("一般項の公式を正しく使っている", 1), ("値を正しく求めている", 1)],
               pit=["指数を $n$ にしてしまう。", "負の公比の累乗の符号を誤る。"],
               chk=(f"{a}*({p})**({n}-1)", str(v)))


@gen("basic_check", 4, ["computation"])
def arith_sum(r):
    a, d = r.randint(-10, 15), r.choice([x for x in range(-5, 7) if x])
    n = r.randint(10, 40)
    l = a + (n - 1) * d
    S = n * (a + l) // 2
    return num(f"初項 ${a}$、公差 ${d}$ の等差数列の、初項から第 ${n}$ 項までの和を求めなさい。", str(S),
               f"末項は $a_{{{n}}}={l}$。$S={n}\\times\\dfrac{{{a}+({l})}}{{2}}={S}$。", d=2,
               ap="等差数列の和は「(初項＋末項)×項数÷2」。末項を先に求めるか、$\\dfrac{n\\{2a+(n-1)d\\}}{2}$ を使う。",
               steps=[f"末項 $a_{{{n}}}={a}+{n - 1}\\times({d})={l}$。", f"$S_{{{n}}}=\\dfrac{{{n}({a}+({l}))}}{{2}}={S}$。"],
               alt=[f"$S_n=\\dfrac{{n\\{{2a+(n-1)d\\}}}}{{2}}=\\dfrac{{{n}\\{{{2 * a}+{n - 1}\\cdot({d})\\}}}}{{2}}={S}$ でも求められる。"],
               pc=[("末項または公式を正しく使っている", 1), ("和を正しく求めている", 1)],
               pit=["末項を $a+nd$ と誤る。", "最後に $2$ で割り忘れる。"],
               chk=(f"summation({a}+(k-1)*({d}), (k, 1, {n}))", str(S)))


@gen("basic_check", 4, ["computation", "concept"])
def sigma_value(r):
    form = r.choice(["lin", "sq", "cube", "sqlin"])
    n = r.randint(5, 20)
    if form == "lin":
        a, b = r.randint(2, 6), r.randint(-5, 5)
        term, py = f"({lin_tex(a, b, 'k')})", f"{a}*k+({b})"
    elif form == "sq":
        term, py = "k^2", "k**2"
    elif form == "cube":
        n = r.randint(4, 12)
        term, py = "k^3", "k**3"
    else:
        b = r.choice([1, 2, 3, -1, -2])
        term, py = f"k(k{'+' if b > 0 else '-'}{abs(b)})", f"k*(k+({b}))"
    v = sum(sp.sympify(py).subs(K, i) for i in range(1, n + 1))
    return num(f"$\\displaystyle\\sum_{{k=1}}^{{{n}}}{term}$ の値を求めなさい。", str(v),
               "$\\Sigma$ の性質で項ごとに分け、$\\displaystyle\\sum k=\\dfrac{1}{2}n(n+1)$、$\\displaystyle\\sum k^2=\\dfrac{1}{6}n(n+1)(2n+1)$、$\\displaystyle\\sum k^3=\\left\\{\\dfrac{1}{2}n(n+1)\\right\\}^2$ を使う。" + f"値は ${v}$。", d=2,
               ap="$\\Sigma$ の中を $k$ の多項式として展開し、項ごとに和の公式を使ってから $n$ に数値を代入する。",
               steps=[f"${term}$ を展開して $k$ の次数ごとに分ける：${tex(sp.sympify(py))}$。", f"公式を使って $n={n}$ を代入する。", f"和は ${v}$。"],
               alt=["$n$ が小さい場合は、数項書き出して足し、結果を確かめる。"],
               pc=[("和の公式を正しく使っている", 1), ("値を正しく求めている", 1)],
               pit=["定数項の和 $\\displaystyle\\sum_{k=1}^{n}c$ を $c$ としてしまう（正しくは $nc$）。"],
               chk=(f"summation({py}, (k, 1, {n}))", str(v)))


@gen("basic_check", 4, ["computation"])
def geo_sum(r):
    a = r.choice([1, 2, 3, 4, 5, -1, -3])
    p = r.choice([2, 3, -2, 4, 5, -3])
    n = r.randint(4, 8)
    if (a, p, n) == (2, 3, 5):
        n = 6
    S = a * (p ** n - 1) // (p - 1)
    return num(f"等比数列 ${a},\\ {a * p},\\ {a * p * p},\\ \\cdots$ の初項から第 ${n}$ 項までの和を求めなさい。", str(S),
               f"初項 ${a}$、公比 ${p}$ なので $S_{{{n}}}=\\dfrac{{{a}\\{{({p})^{{{n}}}-1\\}}}}{{{p}-1}}={S}$。", d=2,
               ap="与えられた項から初項と公比を読み取り、等比数列の和の公式 $S_n=\\dfrac{a(r^n-1)}{r-1}$ に代入する。指数は項数 $n$。",
               steps=[f"初項 ${a}$、公比 $\\dfrac{{{a * p}}}{{{a}}}={p}$。", f"$S_{{{n}}}=\\dfrac{{{a}\\{{({p})^{{{n}}}-1\\}}}}{{{p}-1}}$。", f"$={S}$。"],
               alt=["項を書き出して足しても確かめられる：" + "$" + "+".join(f"({a * p ** i})" for i in range(n)) + f"={S}$。"],
               pc=[("初項・公比を正しく読み取っている", 1), ("和を正しく求めている", 1)],
               pit=["指数を $n-1$ にする。", "公比が負のときの符号を誤る。"],
               chk=(f"summation({a}*({p})**(k-1), (k, 1, {n}))", str(S)))


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 4, ["computation", "concept"])
def arith_two_terms(r):
    a, d = r.randint(-20, 30), r.choice([x for x in range(-6, 8) if x])
    p, q = sorted(r.sample(range(2, 25), 2))
    ap_, aq = a + (p - 1) * d, a + (q - 1) * d
    return sa(f"等差数列 $\\{{a_n\\}}$ において、$a_{{{p}}}={ap_}$、$a_{{{q}}}={aq}$ である。一般項 $a_n$ を求めなさい。",
              f"$a_n={lin_tex(d, a - d)}$",
              f"$a+{p - 1}d={ap_}$、$a+{q - 1}d={aq}$ を解いて $a={a},\\ d={d}$。", d=3, v=[f"a_n={lin_tex(d, a - d)}"],
              ap="初項 $a$ と公差 $d$ を未知数として、2つの項の条件から連立方程式をつくる。",
              steps=[f"$a_{{{p}}}=a+{p - 1}d={ap_}$、$a_{{{q}}}=a+{q - 1}d={aq}$。", f"辺々引いて ${q - p}d={aq - ap_}$、$d={d}$。", f"$a={a}$。",
                     f"$a_n={a}+(n-1)\\cdot({d})={lin_tex(d, a - d)}$。"],
              alt=[f"$a_{{{q}}}-a_{{{p}}}=({q}-{p})d$ を使えば、すぐに $d={d}$ が分かる（項の番号の差が公差の個数）。"],
              pc=[("連立方程式を正しく立てている", 1), ("初項と公差を正しく求めている", 2), ("一般項を整理して答えている", 1)],
              pit=["番号の差 $q-p$ ではなく $q-p+1$ で割る。"],
              chk=(f"solve([a+({p}-1)*d-({ap_}), a+({q}-1)*d-({aq})], [a, d])", f"{{a: {a}, d: {d}}}", None, "intermediate"))


@gen("standard_practice", 5, ["computation"])
def sigma_formula(r):
    while True:
        a, b, c = r.choice([0, 1, 2, 3, 1, 6]), r.randint(-4, 5), r.randint(-4, 4)
        if (a, b, c) not in ((0, 2, 1),) and (a, b) != (0, 0) and not (a == 0 and c == 0 and b == 1):
            break
    term = a * K ** 2 + b * K + c
    S = sp.factor(sp.summation(term, (K, 1, N)))
    return sa(f"$\\displaystyle\\sum_{{k=1}}^{{n}}({sp.latex(term)})$ を計算し、因数分解した形で答えなさい。", f"${sp.latex(S)}$",
              "$\\displaystyle\\sum k^2=\\dfrac{1}{6}n(n+1)(2n+1)$、$\\displaystyle\\sum k=\\dfrac{1}{2}n(n+1)$、$\\displaystyle\\sum c=nc$ を使い、共通因数 $n$ でくくる。", d=3,
              v=[str(S)],
              ap="$\\Sigma$ の線形性で項ごとに分け、公式を使う。最後に共通因数 $n$（や $n+1$）でくくって整理する。",
              steps=[f"$\\displaystyle\\sum_{{k=1}}^{{n}}({sp.latex(term)})={sp.latex(a * sp.Symbol('A') + b * sp.Symbol('B') + c * N).replace('A', chr(92) + 'sum k^2').replace('B', chr(92) + 'sum k')}$（$\\sum$ はすべて $k=1$ から $n$ まで）。",
                     "公式を代入して、分母の最小公倍数で通分し $n$ でくくる。", f"$={sp.latex(S)}$。"],
              alt=["$n=1,\\ 2$ を代入して、もとの和（第1項、第1項＋第2項）と一致するか確かめる。"],
              pc=[("和の公式を正しく使っている", 2), ("正しく整理・因数分解している", 2)],
              pit=["定数 $c$ の和を $c$ とする（正しくは $cn$）。", "通分の計算を誤る。"],
              chk=(f"summation({sp.sstr(term)}, (k, 1, n))", sp.sstr(S), "expand"))


@gen("standard_practice", 4, ["computation", "condition_check"])
def diff_seq(r):
    while True:
        a1, b1, e = r.randint(-5, 8), r.randint(-4, 6), r.choice([1, 2, 3, 4, 2])
        terms = [a1]
        for i in range(5):
            terms.append(terms[-1] + b1 + i * e)
        if terms[:5] != [1, 2, 5, 10, 17]:
            break
    an = sp.expand(a1 + sp.summation(b1 + (K - 1) * e, (K, 1, N - 1)))
    bn = sp.expand(b1 + (N - 1) * e)
    return sa("数列 " + "，".join(f"${t}$" for t in terms) + "，$\\cdots$ の一般項 $a_n$ を求めなさい。", f"$a_n={sp.latex(sp.together(an))}$",
              f"階差数列は ${'，'.join(str(terms[i + 1] - terms[i]) for i in range(5))},\\ \\cdots$ で、一般項 $b_n={sp.latex(bn)}$ の等差数列。", d=3,
              v=[f"a_n={sp.sstr(an)}"],
              ap="隣り合う項の差（階差数列）をとると規則が見える。$n\\geqq2$ で $a_n=a_1+\\displaystyle\\sum_{k=1}^{n-1}b_k$ を使い、$n=1$ も確認する。",
              steps=[f"階差数列 $b_n={sp.latex(bn)}$。", f"$n\\geqq2$ のとき $a_n={a1}+\\displaystyle\\sum_{{k=1}}^{{n-1}}({sp.latex(b1 + (K - 1) * e)})$。",
                     f"計算して $a_n={sp.latex(sp.together(an))}$。", f"$n=1$ を代入すると ${a1}$ となり $a_1$ と一致するので、$n=1$ でも成り立つ。"],
              alt=[f"一般項は $n$ の2次式になるので、$a_n=pn^2+qn+r$ とおいて $n=1,\\ 2,\\ 3$ の値から $p,\\ q,\\ r$ を決めてもよい。"],
              pc=[("階差数列の一般項を求めている", 1), ("$\\Sigma$ の上端を $n-1$ として計算している", 2), ("$n=1$ の確認をしている", 1)],
              pit=["$\\Sigma$ の上端を $n$ にしてしまう。", "$n=1$ のときの確認を書かない。"],
              chk=(f"expand({a1}+summation({b1}+(k-1)*{e}, (k, 1, n-1)))", sp.sstr(an), "expand"))


@gen("standard_practice", 4, ["computation", "concept"])
def recur_linear(r):
    while True:
        p = r.choice([2, 3, -2, 4, 3, 2, 5])
        alpha = r.randint(-5, 5)
        q = alpha * (1 - p)
        a1 = r.randint(-4, 6)
        if a1 != alpha and q != 0 and (a1, p, q) != (1, 2, 1):
            break
    c = a1 - alpha
    vals = [a1]
    for _ in range(3):
        vals.append(p * vals[-1] + q)
    qs = f"+{q}" if q > 0 else f"{q}"
    return sa(f"$a_1={a1},\\ a_{{n+1}}={p}a_n{qs}$ で定められる数列 $\\{{a_n\\}}$ の一般項を求めなさい。", f"$a_n={geo_tex(c, p, alpha)}$",
              f"$\\alpha={p}\\alpha{qs}$ より $\\alpha={alpha}$。$a_{{n+1}}{'-' if alpha >= 0 else '+'}{abs(alpha)}={p}(a_n{'-' if alpha >= 0 else '+'}{abs(alpha)})$。", d=3,
              v=[f"a_n={c}*({p})**(n-1)+({alpha})"],
              ap="$a_{n+1}=pa_n+q$ 型は、$\\alpha=p\\alpha+q$ を満たす $\\alpha$ を使って $a_{n+1}-\\alpha=p(a_n-\\alpha)$ と変形し、等比数列に帰着させる。",
              steps=[f"$\\alpha={p}\\alpha{qs}$ を解いて $\\alpha={alpha}$。",
                     f"$a_{{n+1}}-({alpha})={p}\\{{a_n-({alpha})\\}}$。数列 $\\{{a_n-({alpha})\\}}$ は初項 ${a1}-({alpha})={c}$、公比 ${p}$ の等比数列。",
                     f"$a_n-({alpha})={geo_tex(c, p)}$。", f"$a_n={geo_tex(c, p, alpha)}$。"],
              alt=["求めた一般項に $n=1,\\ 2,\\ 3$ を代入し、漸化式から順に計算した値 " + "，".join(f"${v}$" for v in vals[:3]) + " と一致するか確かめる。"],
              pc=[("$\\alpha$ を求めて変形している", 1), ("等比数列の初項・公比を正しく捉えている", 2), ("一般項を正しく答えている", 1)],
              pit=["等比数列 $\\{a_n-\\alpha\\}$ の初項を $a_1$ としてしまう。", "$\\alpha$ を足すのを忘れて $a_n=(a_1-\\alpha)p^{n-1}$ で止める。"],
              chk=("[" + ", ".join(geo_py(c, p, alpha).replace("n", str(i)) for i in range(1, 5)) + "]", str(vals), None, "intermediate"))


@gen("standard_practice", 3, ["computation", "application"])
def telescoping(r):
    form = r.choice([1, 2, 3])
    n = r.randint(5, 40)
    if form == 1:
        term, py, res = "\\dfrac{1}{k(k+1)}", "1/(k*(k+1))", Fraction(n, n + 1)
        split = "\\dfrac{1}{k}-\\dfrac{1}{k+1}"
    elif form == 2:
        term, py, res = "\\dfrac{1}{(2k-1)(2k+1)}", "1/((2*k-1)*(2*k+1))", Fraction(n, 2 * n + 1)
        split = "\\dfrac{1}{2}\\left(\\dfrac{1}{2k-1}-\\dfrac{1}{2k+1}\\right)"
    else:
        term, py, res = "\\dfrac{1}{(3k-2)(3k+1)}", "1/((3*k-2)*(3*k+1))", Fraction(n, 3 * n + 1)
        split = "\\dfrac{1}{3}\\left(\\dfrac{1}{3k-2}-\\dfrac{1}{3k+1}\\right)"
    return num(f"$\\displaystyle\\sum_{{k=1}}^{{{n}}}{term}$ の値を求めなさい。", f"{res.numerator}/{res.denominator}",
               f"${term}={split}$ と部分分数に分けると、隣り合う項が打ち消し合う。", d=3, disp=f"${fr_tex(res)}$",
               ap="分母が「差が一定の2つの1次式の積」なので、部分分数に分解すると和が打ち消し合い、最初と最後の項だけが残る。",
               steps=[f"${term}={split}$。", "和を書き並べると、途中の項が打ち消し合う。", f"残った項を計算して ${fr_tex(res)}$。"],
               alt=["一般の $n$ で和を求めると " + {1: "$\\dfrac{n}{n+1}$", 2: "$\\dfrac{n}{2n+1}$", 3: "$\\dfrac{n}{3n+1}$"}[form] + f"。これに $n={n}$ を代入しても同じ。"],
               pc=[("部分分数に正しく分解している（係数を含む）", 2), ("値を正しく求めている", 2)],
               pit=["部分分数分解で前に付く係数（$\\dfrac{1}{2}$ など）を忘れる。", "残る項を取り違える。"],
               chk=(f"summation({py}, (k, 1, {n}))", f"{res.numerator}/{res.denominator}"))


# ======================================================================
# C 思考力・記述応用
# ======================================================================

INDUCTIONS = [
    ("すべての自然数 $n$ について、$\\displaystyle\\sum_{k=1}^{n}k^2=\\dfrac{1}{6}n(n+1)(2n+1)$ が成り立つことを、数学的帰納法で証明しなさい。",
     ["[I] $n=1$ のとき、左辺 $=1$、右辺 $=\\dfrac{1}{6}\\cdot1\\cdot2\\cdot3=1$。",
      "[II] $n=k$ で成り立つと仮定すると、$\\displaystyle\\sum_{i=1}^{k+1}i^2=\\dfrac{1}{6}k(k+1)(2k+1)+(k+1)^2=\\dfrac{1}{6}(k+1)\\{k(2k+1)+6(k+1)\\}$。",
      "$=\\dfrac{1}{6}(k+1)(2k^2+7k+6)=\\dfrac{1}{6}(k+1)(k+2)(2k+3)$ で、$n=k+1$ のときも成り立つ。"],
     "expand(summation(k**2, (k, 1, n)) - n*(n+1)*(2*n+1)/6)", "0"),
    ("すべての自然数 $n$ について、$\\displaystyle\\sum_{k=1}^{n}k^3=\\left\\{\\dfrac{1}{2}n(n+1)\\right\\}^2$ が成り立つことを、数学的帰納法で証明しなさい。",
     ["[I] $n=1$ のとき、両辺とも $1$。",
      "[II] $n=k$ で成り立つと仮定すると、$\\displaystyle\\sum_{i=1}^{k+1}i^3=\\dfrac{1}{4}k^2(k+1)^2+(k+1)^3=\\dfrac{1}{4}(k+1)^2(k^2+4k+4)$。",
      "$=\\left\\{\\dfrac{1}{2}(k+1)(k+2)\\right\\}^2$ で、$n=k+1$ のときも成り立つ。"],
     "expand(summation(k**3, (k, 1, n)) - (n*(n+1)/2)**2)", "0"),
    ("すべての自然数 $n$ について、$4^n-1$ は $3$ の倍数であることを、数学的帰納法で証明しなさい。",
     ["[I] $n=1$ のとき、$4-1=3$ で $3$ の倍数。",
      "[II] $n=k$ のとき $4^k-1=3m$（$m$ は整数）と仮定すると、$4^{k+1}-1=4\\cdot4^k-1=4(3m+1)-1=3(4m+1)$。",
      "$4m+1$ は整数なので、$n=k+1$ のときも $3$ の倍数。"],
     "[Mod(4**1-1,3), Mod(4**2-1,3), Mod(4**3-1,3), Mod(4**4-1,3)]", "[0, 0, 0, 0]"),
    ("すべての自然数 $n$ について、$7^n-1$ は $6$ の倍数であることを、数学的帰納法で証明しなさい。",
     ["[I] $n=1$ のとき、$7-1=6$ で $6$ の倍数。",
      "[II] $n=k$ のとき $7^k-1=6m$（$m$ は整数）と仮定すると、$7^{k+1}-1=7(6m+1)-1=6(7m+1)$。",
      "$7m+1$ は整数なので、$n=k+1$ のときも $6$ の倍数。"],
     "[Mod(7**1-1,6), Mod(7**2-1,6), Mod(7**3-1,6), Mod(7**4-1,6)]", "[0, 0, 0, 0]"),
    ("すべての自然数 $n$ について、$\\displaystyle\\sum_{k=1}^{n}\\dfrac{1}{k(k+1)}=\\dfrac{n}{n+1}$ が成り立つことを、数学的帰納法で証明しなさい。",
     ["[I] $n=1$ のとき、左辺 $=\\dfrac{1}{2}$、右辺 $=\\dfrac{1}{2}$。",
      "[II] $n=k$ で成り立つと仮定すると、$\\displaystyle\\sum_{i=1}^{k+1}\\dfrac{1}{i(i+1)}=\\dfrac{k}{k+1}+\\dfrac{1}{(k+1)(k+2)}=\\dfrac{k(k+2)+1}{(k+1)(k+2)}$。",
      "$=\\dfrac{(k+1)^2}{(k+1)(k+2)}=\\dfrac{k+1}{k+2}$ で、$n=k+1$ のときも成り立つ。"],
     "simplify(summation(1/(k*(k+1)), (k, 1, n)) - n/(n+1))", "0"),
    ("$n$ が $3$ 以上の自然数のとき、$2^n>2n$ が成り立つことを、数学的帰納法で証明しなさい。",
     ["[I] $n=3$ のとき、左辺 $=8$、右辺 $=6$ で成り立つ。",
      "[II] $k\\geqq3$ として $n=k$ で $2^k>2k$ が成り立つと仮定すると、$2^{k+1}=2\\cdot2^k>4k$。",
      "$4k-2(k+1)=2k-2>0$（$k\\geqq3$）より $4k>2(k+1)$。よって $2^{k+1}>2(k+1)$ で、$n=k+1$ のときも成り立つ。"],
     "[2**3-2*3, 2**4-2*4, 2**5-2*5]", "[2, 8, 22]"),
    ("すべての自然数 $n$ について、$\\displaystyle\\sum_{k=1}^{n}(2k-1)\\cdot 3^{k-1}=(n-1)3^n+1$ が成り立つことを、数学的帰納法で証明しなさい。",
     ["[I] $n=1$ のとき、左辺 $=1$、右辺 $=0+1=1$。",
      "[II] $n=k$ で成り立つと仮定すると、$\\displaystyle\\sum_{i=1}^{k+1}(2i-1)3^{i-1}=(k-1)3^k+1+(2k+1)3^k=3k\\cdot3^k+1$。",
      "$=k\\cdot3^{k+1}+1=\\{(k+1)-1\\}3^{k+1}+1$ で、$n=k+1$ のときも成り立つ。"],
     "simplify(summation((2*k-1)*3**(k-1), (k, 1, n)) - ((n-1)*3**n+1))", "0"),
]


@gen("thinking_writing", 3, ["written_reasoning"])
def induction(r):
    stem, steps, expr, exp = r.choice(INDUCTIONS)
    concl = "[I]、[II] より、" + ("$n\\geqq3$ のすべての自然数 $n$ で成り立つ。" if "3$ 以上" in stem else "すべての自然数 $n$ で成り立つ。")
    return desc(stem, "（証明）" + "".join(steps) + concl + "（証明終）", "数学的帰納法の2段階 [I]・[II] を示す。[II] では仮定を使って $n=k+1$ の場合を導く。",
                [("[I] 出発点の場合を確かめている", 2), ("[II] 仮定を明示し、それを用いて $n=k+1$ の場合を正しく導いている", 4), ("結論を正しく述べている", 2)],
                d=4, p=8, lines=12, kind="proof",
                ap="[II] では「$n=k$ のときの式（仮定）」と「$n=k+1$ のときに示すべき式（目標）」を先に書き出し、左辺を「仮定の部分＋増えた部分」に分けて目標に向けて変形する。",
                steps=steps + [concl],
                alt=["示すべき式の両辺に $n=1,\\ 2,\\ 3$ を代入して成り立つことを確かめておくと、[II] の変形の見通しが立つ（証明の代わりにはならない）。"],
                pc=[("[I]", 2), ("[II] の仮定と変形", 4), ("結論", 2)],
                pit=["[I] を書き忘れる。", "[II] で示すべき式を仮定として使ってしまう（循環論法）。"],
                chk=(expr, exp, None, "intermediate"))


@gen("thinking_writing", 3, ["condition_check", "written_reasoning"])
def sn_to_an(r):
    p, q = r.choice([1, 2, 3, -1, 2]), r.randint(-5, 6)
    rr = r.choice([0, 0, r.randint(-4, 5)])
    S = p * N ** 2 + q * N + rr
    an = sp.expand(S - S.subs(N, N - 1))
    a1 = p + q + rr
    same = rr == 0
    ans = f"$a_n={sp.latex(an)}$" if same else f"$a_1={a1}$、$n\\geqq2$ のとき $a_n={sp.latex(an)}$"
    return sa(f"数列 $\\{{a_n\\}}$ の初項から第 $n$ 項までの和 $S_n$ が $S_n={sp.latex(S)}$ で表されるとき、一般項 $a_n$ を求めなさい。", ans,
              f"$n\\geqq2$ のとき $a_n=S_n-S_{{n-1}}={sp.latex(an)}$。$a_1=S_1={a1}$。" + ("$n=1$ を代入した値と一致するので、まとめて表せる。" if same else f"$n=1$ を代入した値 ${an.subs(N, 1)}$ と一致しないので、分けて答える。"),
              d=4, p=8,
              ap="$a_n=S_n-S_{n-1}$ は $n\\geqq2$ でしか使えない（$S_0$ は定義されない）。$a_1=S_1$ を別に求めて、まとめられるかを確かめる。",
              steps=[f"$a_1=S_1={a1}$。", f"$n\\geqq2$ のとき $a_n=S_n-S_{{n-1}}=({sp.latex(S)})-({sp.latex(sp.expand(S.subs(N, N - 1)))})={sp.latex(an)}$。",
                     f"$n=1$ を代入すると ${an.subs(N, 1)}$" + ("で $a_1$ と一致する。" if same else f"で $a_1={a1}$ と一致しない。"), ans + "。"],
              alt=[f"$a_1,\\ a_2,\\ a_3$ を $S_1,\\ S_2-S_1,\\ S_3-S_2$ から実際に計算し（${a1},\\ {an.subs(N, 2)},\\ {an.subs(N, 3)}$）、答えと照合する。"],
              pc=[("$n\\geqq2$ の条件を明記して $S_n-S_{n-1}$ を計算している", 3), ("$a_1=S_1$ を求めている", 2), ("$n=1$ の場合の確認と正しい結論", 3)],
              pit=["$n=1$ の確認をせずに $a_n=" + sp.latex(an) + "$ とまとめる" + ("（この問題ではたまたま正しいが、根拠が書かれていないと減点される）。" if same else "（定数項があるため誤り）。")],
              chk=(f"[expand({sp.sstr(S)} - ({sp.sstr(S.subs(N, N - 1))})), {sp.sstr(S.subs(N, 1))}]",
                   f"[{sp.sstr(an)}, {a1}]", "expand", "intermediate"))


@gen("thinking_writing", 2, ["cross_unit", "application", "computation"], rel=["HS-MATH2-U05"])
def log_seq(r):
    import math
    while True:
        base, lg = r.choice([(2, "0.3010"), (3, "0.4771")])
        k = r.randint(3, 15)
        form = r.choice(["n-1", "n"])
        x = k / math.log10(base)
        xa = k / float(lg)
        if math.floor(x) == math.floor(xa) and abs(x - round(x)) > 0.05:
            break
    if form == "n-1":
        n0 = math.floor(x) + 2
        seq, cond = f"a_n={base}^{{n-1}}", f"{base}^{{n-1}}>10^{{{k}}}"
        expr = f"floor({k}*log(10)/log({base}))+2"
        st = [f"${cond}$ の両辺の常用対数をとる：$(n-1)\\log_{{10}}{base}>{k}$。", f"$n-1>\\dfrac{{{k}}}{{{lg}}}={xa:.2f}\\cdots$。", f"$n-1\\geqq{n0 - 1}$ より $n\\geqq{n0}$。"]
    else:
        n0 = math.floor(x) + 1
        seq, cond = f"a_n={base}^n", f"{base}^n>10^{{{k}}}"
        expr = f"floor({k}*log(10)/log({base}))+1"
        st = [f"${cond}$ の両辺の常用対数をとる：$n\\log_{{10}}{base}>{k}$。", f"$n>\\dfrac{{{k}}}{{{lg}}}={xa:.2f}\\cdots$。", f"$n\\geqq{n0}$。"]
    return num(f"一般項が ${seq}$ である等比数列 $\\{{a_n\\}}$ において、初めて $10^{{{k}}}$ を超えるのは第何項か。ただし、$\\log_{{10}}{base}={lg}$ とする。", str(n0),
               f"${cond}$ の常用対数をとり、$n$ についての1次不等式を解く。最小の自然数 $n$ は ${n0}$。", d=4, p=8,
               ap="指数に未知数 $n$ があるので、両辺の常用対数をとって $n$ の1次不等式に直す（指数・対数関数の単元）。底 $10>1$ なので不等号の向きは変わらない。",
               steps=st + [f"よって第 ${n0}$ 項。"],
               alt=[f"$\\log_{{10}}a_n$ が ${k}$ を超える最初の $n$ を求める、と言いかえてもよい。$n={n0 - 1}$ と $n={n0}$ で $\\log_{{10}}a_n$ を計算し、${k}$ をはさむことを確かめる。"],
               pc=[("常用対数をとって不等式を立てている", 3), ("不等式を正しく解いている", 3), ("最小の自然数 $n$ を正しく答えている", 2)],
               pit=["$a_n=r^{n-1}$ の指数 $n-1$ を $n$ として計算する。", "$n>\\cdots$ の小数を切り捨てた値を答えてしまう（超える最初の整数を答える）。"],
               chk=(expr, str(n0)))


def _weighted():
    out = []
    for rr in (2, 3, 4):
        for a in (1, 2, 3):
            for b in (-2, -1, 0, 1, 2):
                if a + b <= 0:
                    continue
                res = sp.expand(sp.summation((a * K + b) * rr ** (K - 1), (K, 1, N)))
                if all(t.as_coeff_Mul()[0].is_integer for t in sp.Add.make_args(res)):
                    out.append((rr, a, b, sp.collect(sp.expand(sp.powsimp(res)), rr ** N)))
    return out


WEIGHTED = _weighted()


@gen("thinking_writing", 2, ["written_reasoning", "computation"])
def weighted_sum(r):
    rr, a, b, res = r.choice(WEIGHTED)
    term = a * K + b
    tt = "k" if (a, b) == (1, 0) else f"({sp.latex(term)})"
    return desc(f"$S_n=\\displaystyle\\sum_{{k=1}}^{{n}}{tt}\\cdot {rr}^{{k-1}}$ を求めなさい。途中の考え方も書きなさい。", f"$S_n={sp.latex(res)}$",
                f"$S_n-{rr}S_n$ を計算すると、等比数列の和が現れる。", [("$S_n$ と ${rr}S_n$ を1つずらして並べ、差をとっている".replace("{rr}", str(rr)), 3),
                                                       ("等比数列の和を正しく計算している", 3), ("$S_n$ を正しく求めている", 2)], d=4, p=8, lines=10,
                ap="（等差数列）×（等比数列）の形の和は、等比数列の和の公式の導出と同じく、$S_n-rS_n$ をつくると等比数列の和に帰着する。",
                steps=[f"$S_n={a + b}\\cdot1+{2 * a + b}\\cdot{rr}+\\cdots+({sp.latex(a * N + b)}){rr}^{{n-1}}$。",
                       f"${rr}S_n={a + b}\\cdot{rr}+\\cdots+({sp.latex(a * N - a + b)}){rr}^{{n-1}}+({sp.latex(a * N + b)}){rr}^{{n}}$。",
                       f"辺々引くと $(1-{rr})S_n={a + b}+{a}({rr}+{rr}^2+\\cdots+{rr}^{{n-1}})-({sp.latex(a * N + b)}){rr}^n$。",
                       f"等比数列の和を計算して整理すると $S_n={sp.latex(res)}$。"],
                alt=["求めた式に $n=1,\\ 2$ を代入し、$S_1=" + f"{a + b}" + "$、$S_2=" + f"{a + b + (2 * a + b) * rr}" + "$ と一致するか確かめる。", "数学的帰納法で、求めた式が正しいことを証明することもできる。"],
                pc=[("ずらして差をとる", 3), ("等比数列の和", 3), ("答え", 2)],
                pit=["差をとるとき、最後の項 $(an+b)r^n$ の符号を誤る。", "等比数列の部分の項数を誤る（$r$ から $r^{n-1}$ までの $n-1$ 項）。"],
                chk=(f"summation(({sp.sstr(term)})*{rr}**(k-1), (k, 1, n))", sp.sstr(res), None, "intermediate"))


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(stem, wrong, step, etype, tempt, fix, ans, expl, steps, ap, alt, pit, chk=None, d=3):
    return desc(f"{stem}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい答えを求めなさい。", ans, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい解答を途中式とともに示している", 3), ("最終的な答えが正しい", 1)], d=d, p=6, lines=6,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい途中式", 3), ("正しい答え", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix), chk=chk)


@gen("error_correction", 3, ["common_error", "computation"])
def err_geo_sum(r):
    a, p, n = r.choice([1, 2, 3, 5]), r.choice([2, 3, 4]), r.randint(4, 8)
    S = a * (p ** n - 1) // (p - 1)
    W = a * (p ** (n - 1) - 1) // (p - 1)
    wrong = f"$S=\\dfrac{{{a}({p}^{{{n - 1}}}-1)}}{{{p}-1}}={W}$"
    fix = f"$S=\\dfrac{{{a}({p}^{{{n}}}-1)}}{{{p}-1}}={S}$"
    return err_item(f"初項 ${a}$、公比 ${p}$ の等比数列の、初項から第 ${n}$ 項までの和 $S$ を求めなさい。", wrong, "和の公式の指数（$r^{n-1}$ とした部分）", "formula",
                    "一般項 $ar^{n-1}$ の指数 $n-1$ と、和の公式の指数 $n$ を混同している。",
                    fix, f"$S={S}$", f"和の公式 $S_n=\\dfrac{{a(r^n-1)}}{{r-1}}$ の指数は項数 $n$。生徒の式は第 ${n - 1}$ 項までの和になっている。",
                    [f"項数は ${n}$。", f"$S=\\dfrac{{{a}({p}^{{{n}}}-1)}}{{{p}-1}}$。", f"$={S}$。"],
                    "公式の導出 $S-rS$ で、最後に残るのは $ar^n$（第 $n+1$ 項にあたる）であることを思い出す。",
                    ["項を書き出して足す：$" + "+".join(str(a * p ** i) for i in range(n)) + f"={S}$。"],
                    ["一般項と和の公式の指数を混同する。"],
                    chk=(f"summation({a}*{p}**(k-1), (k, 1, {n}))", str(S), None, "intermediate"), d=2)


@gen("error_correction", 3, ["common_error", "condition_check"])
def err_sn(r):
    p, q = r.choice([1, 2, 3]), r.randint(-4, 5)
    c = r.choice([x for x in range(-5, 7) if x])
    S = p * N ** 2 + q * N + c
    an = sp.expand(S - S.subs(N, N - 1))
    a1 = p + q + c
    wrong = f"$a_n=S_n-S_{{n-1}}={sp.latex(an)}$（すべての自然数 $n$）"
    fix = f"$a_1=S_1={a1}$、$n\\geqq2$ のとき $a_n={sp.latex(an)}$"
    return err_item(f"初項から第 $n$ 項までの和が $S_n={sp.latex(S)}$ である数列 $\\{{a_n\\}}$ の一般項を求めなさい。", wrong, "$n=1$ の場合の検討（$n\\geqq2$ の条件の無視）", "condition",
                    "$a_n=S_n-S_{n-1}$ がどの $n$ でも使えると思いこんでいる。$S_0$ が定義されないことに気づいていない。",
                    fix, fix, f"$n=1$ を代入すると ${an.subs(N, 1)}$ となり $a_1={a1}$ と一致しない。",
                    [f"$a_1=S_1={a1}$。", f"$n\\geqq2$ のとき $a_n=S_n-S_{{n-1}}={sp.latex(an)}$。", f"$n=1$ を代入すると ${an.subs(N, 1)}\\neq{a1}$ なので、分けて答える。"],
                    "$S_n$ に定数項があると、$n=1$ のときだけ値がずれる。必ず $a_1=S_1$ と照合する。",
                    [f"$S_1={a1}$ を直接計算し、生徒の式に $n=1$ を代入した値 ${an.subs(N, 1)}$ と比べれば誤りが分かる。"],
                    ["$n\\geqq2$ の条件を書かない。"],
                    chk=(f"[{sp.sstr(S.subs(N, 1))}, expand({sp.sstr(S)} - ({sp.sstr(S.subs(N, N - 1))}))]", f"[{a1}, {sp.sstr(an)}]", "expand", "intermediate"))


@gen("error_correction", 2, ["common_error", "computation"])
def err_diff(r):
    a1, b1, e = r.randint(-3, 6), r.randint(1, 5), r.choice([1, 2, 3])
    bn = b1 + (K - 1) * e
    right = sp.expand(a1 + sp.summation(bn, (K, 1, N - 1)))
    wrong_v = sp.expand(a1 + sp.summation(bn, (K, 1, N)))
    terms = [a1]
    for i in range(4):
        terms.append(terms[-1] + b1 + i * e)
    wrong = f"階差数列は $b_n={sp.latex(sp.expand(bn.subs(K, N)))}$。$a_n={a1}+\\displaystyle\\sum_{{k=1}}^{{n}}({sp.latex(bn)})={sp.latex(wrong_v)}$"
    fix = f"$n\\geqq2$ のとき $a_n={a1}+\\displaystyle\\sum_{{k=1}}^{{n-1}}({sp.latex(bn)})={sp.latex(right)}$（$n=1$ でも成り立つ）"
    return err_item("数列 " + "，".join(f"${t}$" for t in terms) + "，$\\cdots$ の一般項を求めなさい。", wrong, "$\\Sigma$ の上端（$n$ とした部分）", "formula",
                    "「$n$ 項目まで」と考えて上端を機械的に $n$ にしている。$a_n$ までに加える差の個数が $n-1$ 個であることを意識していない。",
                    fix, f"$a_n={sp.latex(right)}$", "$a_1$ から $a_n$ までに差を加える回数は $n-1$ 回。",
                    ["$a_n=a_1+b_1+b_2+\\cdots+b_{n-1}$（$n\\geqq2$）。", f"$a_n={a1}+\\displaystyle\\sum_{{k=1}}^{{n-1}}({sp.latex(bn)})={sp.latex(right)}$。", f"$n=1$ で ${a1}$ となり成り立つ。"],
                    "答えに $n=1,\\ 2$ を代入して、もとの数列と比べれば誤りに気づける。",
                    [f"生徒の式に $n=1$ を代入すると ${wrong_v.subs(N, 1)}$ となり、初項 ${a1}$ と一致しない。"],
                    ["上端を $n$ にする。"],
                    chk=(f"expand({a1}+summation({sp.sstr(bn)}, (k, 1, n-1)))", sp.sstr(right), "expand", "intermediate"), d=3)


@gen("error_correction", 2, ["common_error", "computation"])
def err_count(r):
    a, d = r.randint(1, 20), r.choice([2, 3, 4, 5, 6, 7])
    n = r.randint(12, 40)
    l = a + (n - 1) * d
    S = n * (a + l) // 2
    wn = n - 1
    W = wn * (a + l) // 2 if (wn * (a + l)) % 2 == 0 else Fraction(wn * (a + l), 2)
    wrong = f"項数は $\\dfrac{{{l}-{a}}}{{{d}}}={wn}$。和は $\\dfrac{{{wn}({a}+{l})}}{{2}}={fr_tex(W)}$"
    fix = f"項数は $\\dfrac{{{l}-{a}}}{{{d}}}+1={n}$。和は $\\dfrac{{{n}({a}+{l})}}{{2}}={S}$"
    return err_item(f"等差数列 ${a},\\ {a + d},\\ {a + 2 * d},\\ \\cdots,\\ {l}$ の和を求めなさい。", wrong, "項数の計算（$+1$ の忘れ）", "calculation",
                    "（末項－初項）÷公差 は「公差を加えた回数」であり、項数はそれより $1$ 多い。植木算と同じ構造を見落としやすい。",
                    fix, f"${S}$", f"$a_n={a}+(n-1)\\cdot{d}={l}$ を解くと $n={n}$。",
                    [f"$a_n={a}+(n-1)\\cdot{d}$ とおき、$a_n={l}$ を解いて $n={n}$。", f"和 $=\\dfrac{{{n}({a}+{l})}}{{2}}={S}$。"],
                    "項数は一般項 $a_n=l$ を解いて求めると確実。",
                    [f"小さな例（${a},\\ {a + d},\\ {a + 2 * d}$ の3項）で「（末項－初項）÷公差」が $2$ になり、項数より $1$ 少ないことを確かめる。"],
                    ["項数を（末項－初項）÷公差 とする。"],
                    chk=(f"[({l}-{a})/{d}+1, summation({a}+(k-1)*{d}, (k, 1, {n}))]", f"[{n}, {S}]", None, "intermediate"), d=2)


GENERATORS = [arith_term, geo_term, arith_sum, sigma_value, geo_sum,
              arith_two_terms, sigma_formula, diff_seq, recur_linear, telescoping,
              induction, sn_to_an, log_seq, weighted_sum,
              err_geo_sum, err_sn, err_diff, err_count]
