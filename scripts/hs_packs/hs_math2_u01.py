"""単元パック：数学Ⅱ 式と証明（二項定理・整式の除法・分数式・恒等式・等式と不等式の証明）。"""
from math import comb, factorial, isqrt

from banks._common import desc, num, sa
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, nonzero, poly, summary,
                         theorem, tp)

UNIT_ID = "HS-MATH2-U01"


# ----------------------------------------------------------------------
# 整式の補助（係数リストは次数の高い順）
# ----------------------------------------------------------------------

def pmul(p, q):
    out = [0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return out


def padd(p, q):
    n = max(len(p), len(q))
    p = [0] * (n - len(p)) + list(p)
    q = [0] * (n - len(q)) + list(q)
    return [a + b for a, b in zip(p, q)]


def trim(p):
    p = list(p)
    while len(p) > 1 and p[0] == 0:
        p.pop(0)
    return p


def pt(p):
    return poly(*trim(p))


def ppy(p):
    p = trim(p)
    d = len(p) - 1
    return "(" + "+".join(f"({c})*x**{d - i}" for i, c in enumerate(p)) + ")"


def mono(c, d):
    """単項式 c x^d の LaTeX（符号つき・先頭用でない）。"""
    return poly(*([c] + [0] * d))


def long_div(P, D):
    """P÷D の商・余りと、筆算の各段階の説明。"""
    rem = list(P)
    dq = len(P) - len(D)
    Q = [0] * (dq + 1)
    steps = []
    for i in range(dq + 1):
        c = rem[i] // D[0]
        deg = dq - i
        Q[i] = c
        sub = [0] * i + [c * x for x in D] + [0] * (len(P) - i - len(D))
        rem = [a - b for a, b in zip(rem, sub)]
        if c != 0:
            steps.append(f"商に ${mono(c, deg)}$ を立て、${mono(c, deg)}\\times({pt(D)})$ を引くと ${pt(rem[i + 1:]) if any(rem[i + 1:]) else '0'}$。")
    R = trim(rem[dq + 1:]) if dq + 1 < len(rem) else [0]
    return Q, R, steps


def frac_tex(c, den):
    """c/den の符号つき項（例 +\\dfrac{3}{x}）。"""
    s = "-" if c < 0 else "+"
    return f"{s}\\dfrac{{{abs(c)}}}{{{den}}}"


def xpow(e):
    return "x" if e == 1 else f"x^{{{e}}}"


def lin(c, var="x"):
    """c*var の先頭用表記。"""
    return var if c == 1 else ("-" + var if c == -1 else f"{c}{var}")


def cterm(c, var):
    """符号つきの c*var（途中の項）。"""
    if c == 1:
        return f"+{var}"
    if c == -1:
        return f"-{var}"
    return f"+{c}{var}" if c > 0 else f"{c}{var}"


def C(n, k):
    return f"{{}}_{{{n}}}\\mathrm{{C}}_{{{k}}}"


def shift(v):
    """x+v の v 部分（x-2, x+3）。"""
    return f"+{v}" if v > 0 else f"{v}"


LESSON = lesson(
    goals=["二項定理を組合せの考えから導き、展開式の特定の項の係数を求められる。",
           "整式の除法を筆算で行い、$A=BQ+R$（$R$ の次数は $B$ の次数より低い）の関係を使える。",
           "恒等式の意味を理解し、係数比較法・数値代入法で係数を決定できる。",
           "等式・不等式を「差をとる」「平方の和で表す」「相加平均と相乗平均の関係を使う」方法で証明し、等号成立条件を述べられる。"],
    duration=100,
    readiness=["乗法公式・因数分解（数学Ⅰ）を正確に使える。", "組合せ ${}_n\\mathrm{C}_r$ の意味と計算（数学A）を理解している。",
               "実数の2乗は $0$ 以上であることを知っている。"],
    flow=[("導入：展開の規則性を見つける", 10, "(a+b)^2, (a+b)^3, (a+b)^4 を展開して係数を並べ、パスカルの三角形に気づかせる"),
          ("二項定理", 20, "「どの因数から b を選ぶか」という組合せの見方で二項定理を導き、例題1を解く"),
          ("整式の除法と分数式", 20, "筆算の手順と A=BQ+R を確認する。分数式の約分・通分を整数の分数と対比させる（例題2）"),
          ("恒等式", 15, "方程式との違いを確認し、係数比較法・数値代入法を比較する"),
          ("等式・不等式の証明", 30, "差をとる方法、平方完成、相加平均と相乗平均の関係を順に扱い、等号成立条件の書き方を指導する（例題3）"),
          ("まとめと確認", 5, "確認問題3問、問題プリントAの課題指示")],
    sections=[
        intro("in1", "展開の係数に潜む規則",
              "$(a+b)^2=a^2+2ab+b^2$、$(a+b)^3=a^3+3a^2b+3ab^2+b^3$ の係数を並べると $1,2,1$ と $1,3,3,1$ になる。$(a+b)^4$ の係数 $1,4,6,4,1$ も含めて三角形に並べると、各数がすぐ上の2数の和になっている（パスカルの三角形）。この規則がなぜ成り立つのかを、組合せの考えで説明するのが二項定理である。",
              bullets=["$(a+b)^n$ を展開するとき、$n$ 個の因数 $(a+b)$ のそれぞれから $a$ か $b$ の一方を選んで掛け合わせる。",
                       "式の変形・証明では「何を示せばよいか」を先にはっきりさせ、目標の形に向かって変形する。"],
              points=[tp("$(a+b)^4$ を実際に展開させ、係数を三角形に並べさせてから規則を問う。", ask="上の段とどんな関係があるか。", expect="となり合う2数の和が下の段の数になっている。", timing="導入の冒頭"),
                      tp("展開を「各因数から1つずつ選ぶ」操作として言い直させると、二項定理の導出に直結する。", caution="「掛け算を繰り返す」だけの理解では組合せと結びつかない。")]),
        theorem("th1", "二項定理",
                "$$(a+b)^n={}_n\\mathrm{C}_0a^n+{}_n\\mathrm{C}_1a^{n-1}b+\\cdots+{}_n\\mathrm{C}_ra^{n-r}b^r+\\cdots+{}_n\\mathrm{C}_nb^n$$",
                ["$n$ は自然数", "一般項（第 $r+1$ 項）は ${}_n\\mathrm{C}_ra^{n-r}b^r$（$r=0,1,\\cdots,n$）", "係数 ${}_n\\mathrm{C}_r$ を二項係数という"],
                body="一般項の形を覚えておけば、展開式全体を書かなくても特定の項の係数が求められる。",
                proof=["$(a+b)^n=(a+b)(a+b)\\cdots(a+b)$（$n$ 個の積）を展開した各項は、$n$ 個の因数のそれぞれから $a$ か $b$ を1つずつ選んで掛けたものである。",
                       "$b$ を $r$ 個、$a$ を $n-r$ 個選ぶと、その積は $a^{n-r}b^r$ になる。",
                       "$n$ 個の因数のうち $b$ を選ぶ $r$ 個の因数の決め方は ${}_n\\mathrm{C}_r$ 通りある。",
                       "したがって $a^{n-r}b^r$ の項は ${}_n\\mathrm{C}_r$ 個現れ、その係数は ${}_n\\mathrm{C}_r$ である。$r=0,1,\\cdots,n$ について加えると定理が得られる。"],
                points=[tp("一般項の $a$ と $b$ の指数の和が常に $n$ になることを確認させる。", ask="$a^{n-r}b^r$ の指数の和はいくつか。", expect="$n$"),
                        tp("$(2x-3)^5$ のように係数や符号がつく場合は、$a=2x$、$b=-3$ と「かっこごと」代入させる。", caution="$-3$ の符号や $2$ の累乗を落とす誤りが非常に多い。")]),
        example("ex1", "例題1　特定の項の係数",
                "$(2x-3)^5$ の展開式における $x^3$ の係数を求めよ。",
                ["一般項は ${}_5\\mathrm{C}_r(2x)^{5-r}(-3)^r={}_5\\mathrm{C}_r\\,2^{5-r}(-3)^rx^{5-r}$。",
                 "$x^3$ の項は $5-r=3$、すなわち $r=2$ のとき。", "係数は ${}_5\\mathrm{C}_2\\cdot2^3\\cdot(-3)^2=10\\cdot8\\cdot9=720$。"],
                "$720$",
                thinking="展開式全体を書かず、一般項の $x$ の指数が $3$ になる $r$ を求める。",
                points=[tp("「$x$ の指数＝3」という方程式を立てて $r$ を決める、という流れを板書で明示する。")],
                misconceptions=[("${}_5\\mathrm{C}_2\\cdot2\\cdot(-3)^2=180$", "$(2x)^3=8x^3$ なので $2$ も3乗する")]),
        theorem("th2", "整式の除法",
                "$$A=BQ+R\\qquad(R\\text{ の次数}<B\\text{ の次数})$$",
                ["$A,\\ B$ は整式で $B\\neq0$", "商 $Q$ と余り $R$ はただ1通りに定まる", "$R=0$ のとき「$A$ は $B$ で割り切れる」という"],
                body="整式の割り算は、整数の筆算と同じく「最高次の項に注目して商を立て、掛けて引く」をくり返す。余りの次数が割る式の次数より低くなったところで終える。",
                proof=["$A$ の最高次の項を $B$ の最高次の項で割り、商の最初の項を立てる。",
                       "その項と $B$ の積を $A$ から引くと、最高次の項が消えて次数が下がる。",
                       "次数が下がった式に同じ操作をくり返す。次数は1回ごとに必ず下がるので、有限回で $B$ の次数より低くなり、操作が終わる。",
                       "立てた項の和が商 $Q$、最後に残った式が余り $R$ で、各段階の式を合わせると $A=BQ+R$ が成り立つ。"],
                points=[tp("$x^3+2x-1$ のように抜けている次数がある式は、筆算で $x^2$ の欄を空けておくよう指導する。", caution="欄を詰めて書くと同類項でない項どうしを引いてしまう。"),
                        tp("答えを出したら $BQ+R$ を展開して $A$ にもどるか確かめる習慣をつけさせる。", timing="例題2の後")]),
        example("ex2", "例題2　整式の除法と分数式",
                "(1) $A=2x^3-3x^2+4x-5$ を $B=x^2-x+1$ で割った商と余りを求めよ。\n(2) $\\dfrac{2}{x-1}-\\dfrac{1}{x+1}$ を計算せよ。",
                ["(1) 商に $2x$ を立て、$2x(x^2-x+1)=2x^3-2x^2+2x$ を引くと $-x^2+2x-5$。",
                 "商に $-1$ を立て、$-(x^2-x+1)$ を引くと $x-4$。次数が $B$ より低いので終了。",
                 "(2) 通分すると $\\dfrac{2(x+1)-(x-1)}{(x-1)(x+1)}=\\dfrac{x+3}{(x-1)(x+1)}$。"],
                "(1) 商 $2x-1$、余り $x-4$　(2) $\\dfrac{x+3}{(x-1)(x+1)}$",
                thinking="(1) 最高次の項どうしの割り算をくり返す。(2) 整数の分数と同じく、分母をそろえてから分子を計算する。",
                points=[tp("(2) で「$-(x-1)$」のかっこを外すときの符号を確認させる。", ask="$2(x+1)-(x-1)$ を整理するといくつか。", expect="$x+3$")],
                misconceptions=[("(2) の分子を $2(x+1)-x-1=x+1$ とする", "引く式全体にかっこをつけ、$-(x-1)=-x+1$ とする")]),
        definition("df1", "恒等式",
                   "含まれている文字にどのような値を代入しても常に成り立つ等式を、その文字についての恒等式という。$ax^2+bx+c=a'x^2+b'x+c'$ が $x$ についての恒等式であるための必要十分条件は、両辺の同じ次数の項の係数がそれぞれ等しいことである。",
                   formula="$$ax^2+bx+c=a'x^2+b'x+c'\\ \\text{が恒等式}\\iff a=a',\\ b=b',\\ c=c'$$",
                   conditions=["係数比較法：両辺を展開・整理して同じ次数の係数を比べる", "数値代入法：適当な値を代入して得た条件は必要条件なので、求めた値で恒等式になることを確かめる（十分性の確認）"],
                   points=[tp("方程式（特定の $x$ でだけ成り立つ）と恒等式（すべての $x$ で成り立つ）の違いを、$x^2=1$ と $(x+1)^2=x^2+2x+1$ で対比させる。", ask="$x=1$ を代入するとどちらも成り立つが、何が違うか。")]),
        theorem("th3", "相加平均と相乗平均の関係",
                "$$a>0,\\ b>0\\ \\text{のとき}\\quad \\dfrac{a+b}{2}\\geqq\\sqrt{ab}$$",
                ["$a>0,\\ b>0$（正の数であることが前提）", "等号は $a=b$ のときに限り成り立つ", "$a+b\\geqq2\\sqrt{ab}$ の形で使うことが多い"],
                proof=["$a>0,\\ b>0$ なので $\\sqrt{a},\\ \\sqrt{b}$ は実数で、$a=(\\sqrt{a})^2,\\ b=(\\sqrt{b})^2$。",
                       "$\\dfrac{a+b}{2}-\\sqrt{ab}=\\dfrac{(\\sqrt{a})^2-2\\sqrt{a}\\sqrt{b}+(\\sqrt{b})^2}{2}=\\dfrac{(\\sqrt{a}-\\sqrt{b})^2}{2}\\geqq0$。",
                       "よって $\\dfrac{a+b}{2}\\geqq\\sqrt{ab}$。",
                       "等号は $\\sqrt{a}-\\sqrt{b}=0$、すなわち $a=b$ のときに限り成り立つ。"],
                points=[tp("「（左辺）$-$（右辺）$\\geqq0$ を示す」という不等式の証明の基本方針を、この証明で確認する。"),
                        tp("最小値を求めるときは、等号を成り立たせる値が実際に存在することまで確かめさせる。", caution="等号が成り立たないのに「最小値」と答える誤りが典型（問題プリントD）。")]),
        derivation("dv1", "不等式の証明の進め方",
                   ["示したい不等式 $A\\geqq B$ に対し、差 $A-B$ をつくる。",
                    "$A-B$ を「（実数）$^2$ の和」や「正の数の積」の形に変形する（平方完成・因数分解）。",
                    "実数の2乗は $0$ 以上であることなどから $A-B\\geqq0$ を結論する。",
                    "$A-B=0$ となる条件を調べ、等号成立条件として書く。"],
                   body="例：$x^2+2y^2-2xy=(x-y)^2+y^2\\geqq0$ より $x^2+2y^2\\geqq2xy$。等号は $x-y=0$ かつ $y=0$、すなわち $x=y=0$ のとき。",
                   points=[tp("示したい式を出発点にして変形し、正しい式に到達しても証明にならない（逆向きの推論）ことを確認させる。", caution="「$A\\geqq B$ と仮定して…」と書き始める答案が多い。")]),
        example("ex3", "例題3　相加平均と相乗平均の関係",
                "$x>0$ のとき、$x+\\dfrac{16}{x}$ の最小値と、そのときの $x$ の値を求めよ。",
                ["$x>0,\\ \\dfrac{16}{x}>0$ なので、相加平均と相乗平均の関係が使える。",
                 "$x+\\dfrac{16}{x}\\geqq2\\sqrt{x\\cdot\\dfrac{16}{x}}=2\\sqrt{16}=8$。",
                 "等号は $x=\\dfrac{16}{x}$、すなわち $x^2=16$、$x>0$ より $x=4$ のとき成り立つ。"],
                "最小値 $8$（$x=4$ のとき）",
                thinking="2つの正の数の和で、積 $x\\cdot\\dfrac{16}{x}=16$ が一定になっていることに着目する。",
                points=[tp("積が一定になる組をつくるのがこの関係を使うコツであることを強調する。", ask="なぜ $x$ と $\\dfrac{16}{x}$ の組を選ぶのか。", expect="積が $x$ によらず一定だから。")]),
        board("bd1", "板書案",
              [("① 二項定理", ["$(a+b)^n=\\sum{}_n\\mathrm{C}_ra^{n-r}b^r$", "一般項 ${}_n\\mathrm{C}_ra^{n-r}b^r$", "$(2x-3)^5$ の $x^3$：$r=2$", "${}_5\\mathrm{C}_2\\cdot2^3\\cdot(-3)^2=720$"]),
               ("② 除法・分数式・恒等式", ["$A=BQ+R$（$R$ の次数 $<$ $B$ の次数）", "抜けた次数の欄は空ける", "通分：$\\dfrac{2}{x-1}-\\dfrac{1}{x+1}=\\dfrac{x+3}{(x-1)(x+1)}$", "恒等式 ⇔ 係数がすべて等しい"]),
               ("③ 証明", ["$A\\geqq B$ ⇐ $A-B\\geqq0$", "平方の和にする：$(x-y)^2+y^2\\geqq0$", "$a,b>0$：$a+b\\geqq2\\sqrt{ab}$", "等号成立条件を必ず書く"])],
              points=[tp("板書は3列に分け、③では「証明の型」と「等号成立条件」を色を変えて書く。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("二項定理の計算では、一般項を文字 $r$ のまま書いてから $r$ を決める手順を徹底させる。", ask="求めたい項は $r$ がいくつのときか。"),
               tp("除法の答えには「商」「余り」を明記させ、検算として $BQ+R$ を展開させる。"),
               tp("数値代入法で係数を決めたときは、十分性の確認（求めた値で恒等式になること）を一言書かせる。", caution="必要条件だけで答えを確定させる答案が多い。"),
               tp("相加平均と相乗平均の関係を使う前に「正の数であること」を答案に明記させる。", timing="例題3の後"),
               tp("不等式の証明は「差をとる → 変形 → 符号判定 → 等号成立条件」の4段で答案を構成させる。")],
              misconceptions=[("$(x-2)^6$ の $x^3$ の係数を ${}_6\\mathrm{C}_3\\cdot2^3=160$ とする", "$b=-2$ なので $(-2)^3=-8$ をかけて $-160$"),
                              ("$A\\geqq B$ を両辺変形して正しい式を導き、証明とする", "$A-B$ を変形して $0$ 以上であることを示す"),
                              ("相加平均と相乗平均の関係を2回使って掛け合わせ、それを最小値とする", "2つの等号が同時に成り立つかを確かめる")]),
        summary("sm1", "まとめ",
                ["二項定理：一般項 ${}_n\\mathrm{C}_ra^{n-r}b^r$。係数・符号は「かっこごと」累乗する。",
                 "整式の除法：$A=BQ+R$、余りの次数は割る式の次数より低い。",
                 "恒等式：係数比較法、または数値代入法＋十分性の確認。",
                 "不等式の証明：差をとって平方の和などにする。相加平均と相乗平均の関係は正の数で使い、等号成立条件を確かめる。"]),
        check("ck1", "確認問題",
              [("$(x+2)^6$ の展開式における $x^4$ の係数を求めよ。", "${}_6\\mathrm{C}_2\\cdot2^2=60$"),
               ("$x^3+1$ を $x+1$ で割った商と余りを求めよ。", "商 $x^2-x+1$、余り $0$"),
               ("$a>0$ のとき $a+\\dfrac{1}{a}\\geqq2$ を示し、等号成立条件を答えよ。", "相加平均と相乗平均の関係より $a+\\dfrac{1}{a}\\geqq2\\sqrt{1}=2$。等号は $a=\\dfrac{1}{a}$、$a>0$ より $a=1$ のとき")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

@gen("basic_check", 6, ["computation"])
def binom_coef(r):
    n = r.randint(4, 7)
    a = r.choice([1, 2, 3, -1, -2])
    b = nonzero(r, -4, 4)
    k = r.randint(1, n - 1)
    val = comb(n, k) * a ** k * b ** (n - k)
    expr = poly(a, b)
    return num(f"$({expr})^{{{n}}}$ を展開したとき、${xpow(k)}$ の項の係数を求めなさい。", str(val),
               f"一般項は ${C(n, 'r')}({lin(a)})^{{{n}-r}}\\cdot({b})^r$。$x$ の指数が ${k}$ になるのは $r={n - k}$ のときで、係数は ${C(n, n - k)}\\cdot({a})^{{{k}}}\\cdot({b})^{{{n - k}}}={val}$。", d=2,
               ap="展開式全体を書く必要はない。二項定理の一般項を書き、$x$ の指数が求めたい次数になる $r$ を決める。",
               steps=[f"一般項 ${C(n, 'r')}({lin(a)})^{{{n}-r}}({b})^r={C(n, 'r')}({a})^{{{n}-r}}({b})^rx^{{{n}-r}}$。",
                      f"${n}-r={k}$ より $r={n - k}$。", f"係数 ${C(n, n - k)}\\cdot({a})^{{{k}}}\\cdot({b})^{{{n - k}}}={comb(n, k)}\\cdot({a ** k})\\cdot({b ** (n - k)})={val}$。"],
               alt=[f"${C(n, n - k)}={C(n, k)}={comb(n, k)}$ はパスカルの三角形の第 ${n}$ 段からも読み取れる。符号は $({b})^{{{n - k}}}$ と $({a})^{{{k}}}$ の符号の積で決まる。"],
               pc=[("一般項を正しく書き、$r$ を決めている", 1), ("係数を符号も含めて正しく計算している", 1)],
               pit=[{1: f"定数項 ${b}$ の累乗の指数を ${k}$ と取り違える。", -1: "$-x$ の符号を累乗に反映させ忘れる。"}.get(a, f"$x$ の係数 ${a}$ を累乗し忘れる。"),
                    "負の数の累乗の符号を誤る。"],
               chk=(f"binomial({n},{k})*({a})**{k}*({b})**{n - k}", str(val)))


@gen("basic_check", 5, ["computation"])
def poly_division(r):
    if r.random() < 0.5:
        D = [1, nonzero(r, -4, 4)]
        Q = [r.choice([1, 2, 3, -1, 2]), r.randint(-4, 4), r.randint(-5, 5)]
        R = [r.randint(-6, 6)]
    else:
        D = [1, r.randint(-3, 3), nonzero(r, -3, 3)]
        Q = [r.choice([1, 2, 3, -2]), r.randint(-4, 4)]
        R = [r.randint(-4, 4), r.randint(-5, 5)]
    P = padd(pmul(D, Q), R)
    Q2, R2, st = long_div(P, D)
    assert trim(Q2) == trim(Q) and trim(R2) == trim(R), (P, D)
    return sa(f"整式 $A={pt(P)}$ を整式 $B={pt(D)}$ で割ったときの商 $Q$ と余り $R$ を求めなさい。",
              f"商 ${pt(Q)}$、余り ${pt(R)}$",
              f"筆算で最高次の項に注目して商を立てていくと、$A=({pt(D)})({pt(Q)})+({pt(R)})$ と表せる。", d=2,
              v=[f"Q={pt(Q)}, R={pt(R)}"],
              ap="最高次の項どうしを割って商の項を立て、掛けて引く操作を、余りの次数が $B$ の次数より低くなるまでくり返す。",
              steps=st + [f"余り ${pt(R)}$ の次数は $B$ の次数より低いので終了。商 ${pt(Q)}$、余り ${pt(R)}$。"],
              alt=[f"検算：$BQ+R=({pt(D)})({pt(Q)})+({pt(R)})$ を展開すると $A$ に一致する。"],
              pc=[("商を正しく求めている", 1), ("余りを正しく求めている", 1)],
              pit=["引き算で符号を誤る（引く式全体にかっこをつけていない）。", "抜けている次数の欄を空けずに筆算する。"],
              ver="$BQ+R$ を展開して $A$ にもどることを確かめる。",
              chk=(f"expand({ppy(D)}*{ppy(Q)}+{ppy(R)})", ppy(P), "expand", "intermediate"))


@gen("basic_check", 4, ["concept", "condition_check"])
def identity_coef(r):
    a = r.choice([1, 2, 3, -1, -2])
    b, c = r.randint(-6, 6), r.randint(-7, 7)
    h = nonzero(r, -3, 3)
    P = padd(pmul([a], pmul([1, -h], [1, -h])), padd(pmul([b], [1, -h]), [c]))
    return sa(f"等式 ${pt(P)}=a(x{shift(-h)})^2+b(x{shift(-h)})+c$ が $x$ についての恒等式となるように、定数 $a,\\ b,\\ c$ の値を求めなさい。",
              f"$a={a},\\ b={b},\\ c={c}$",
              f"右辺を展開して係数を比較する（または $t=x{shift(-h)}$ とおいて $x=t{shift(h)}$ を左辺に代入する）。", d=2,
              v=[f"a={a}, b={b}, c={c}"],
              ap="「すべての $x$ で成り立つ」ので、両辺の同じ次数の係数がそれぞれ等しい。展開して比べるか、都合のよい値を代入する。",
              steps=[f"右辺を展開：$ax^2+({-2 * h}a+b)x+({h * h}a{cterm(-h, 'b')}+c)$。",
                     f"$x^2$ の係数から $a={a}$。", f"$x$ の係数から ${-2 * h}a+b={P[1]}$ より $b={b}$。", f"定数項から $c={c}$。"],
              alt=[f"数値代入法：$x={h}$ を代入すると右辺は $c$ だけになり、$c={c}$ がすぐ求まる。ただし代入で得た値は必要条件なので、最後に係数比較などで恒等式になることを確かめる。"],
              pc=[("係数比較（または代入）の式を正しく立てている", 1), ("$a,\\ b,\\ c$ をすべて正しく求めている", 1)],
              pit=["展開したときの $x$ の係数の符号を誤る。", "数値代入法で求めた値の十分性を確かめない。"],
              chk=(f"expand(({a})*(x-({h}))**2+({b})*(x-({h}))+({c}))", ppy(P), "expand", "intermediate"))


@gen("basic_check", 5, ["computation", "condition_check"])
def amgm_min(r):
    p = r.randint(1, 5)
    x0 = r.randint(1, 5)
    c = r.randint(-5, 5)
    q = p * x0 * x0
    val = 2 * p * x0 + c
    tail = "" if c == 0 else (f"+{c}" if c > 0 else f"{c}")
    expr = f"{lin(p)}+\\dfrac{{{q}}}{{x}}{tail}"
    return num(f"$x>0$ のとき、式 ${expr}$ の最小値と、最小値をとるときの $x$ の値を求めなさい。", str(val),
               f"$x>0,\\ \\dfrac{{{q}}}{{x}}>0$ より、相加平均と相乗平均の関係から ${lin(p)}+\\dfrac{{{q}}}{{x}}\\geqq2\\sqrt{{{p * q}}}={2 * p * x0}$。等号は $x={x0}$ のとき。", d=2,
               disp=f"最小値 ${val}$（$x={x0}$）",
               ap=f"${lin(p)}$ と $\\dfrac{{{q}}}{{x}}$ はどちらも正で、積 ${p * q}$ が一定。積が一定の2つの正の数の和には、相加平均と相乗平均の関係が使える。",
               steps=[f"$x>0$ より ${lin(p)}>0,\\ \\dfrac{{{q}}}{{x}}>0$。",
                      f"${lin(p)}+\\dfrac{{{q}}}{{x}}\\geqq2\\sqrt{{{lin(p)}\\cdot\\dfrac{{{q}}}{{x}}}}=2\\sqrt{{{p * q}}}={2 * p * x0}$。",
                      f"等号は ${lin(p)}=\\dfrac{{{q}}}{{x}}$、すなわち $x^2={x0 * x0}$、$x>0$ より $x={x0}$ のとき。", f"最小値は ${2 * p * x0}{tail}={val}$。"],
               alt=[f"$x={x0}$ の前後（$x={x0 + 1}$ など）を代入すると値が ${val}$ より大きくなることで、結果の妥当性を確かめられる。"],
               pc=[("相加平均と相乗平均の関係を正しく使っている", 1), ("等号成立の $x$ と最小値を正しく答えている", 1)],
               pit=["正の数であることを確認せずに使う。", "等号が成り立つ $x$ を確かめない。"],
               chk=(f"2*sqrt({p}*{q})+({c})", str(val)))


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 5, ["computation", "concept"])
def binom_const_term(r):
    s = r.choice([1, 2])
    n = r.randint(4, 8)
    c = r.choice([1, 2, 3, -1, -2, -3])
    rs = [k for k in range(n + 1) if s * (n - k) - k >= 0]
    k = r.choice(rs)
    e = s * (n - k) - k
    val = comb(n, k) * c ** k
    base = "x" if s == 1 else "x^2"
    expr = f"{base}{frac_tex(c, 'x')}"
    target = "定数項" if e == 0 else f"${xpow(e)}$ の項の係数"
    cfx = f"\\dfrac{{{c}}}{{x}}" if c > 0 else f"-\\dfrac{{{-c}}}{{x}}"
    bpow = f"x^{{{n}-r}}" if s == 1 else f"(x^2)^{{{n}-r}}"
    tname = "定数項" if e == 0 else f"${xpow(e)}$ の項"
    return num(f"$\\left({expr}\\right)^{{{n}}}$ の展開式における{target}を求めなさい。", str(val),
               f"一般項は ${C(n, 'r')}{bpow}\\left({cfx}\\right)^r={C(n, 'r')}({c})^rx^{{{s * n}-{s + 1}r}}$。$r={k}$ のとき{tname}になり、値は ${val}$。", d=3,
               ap="$\\dfrac{1}{x}=x^{-1}$ と考えると、一般項の $x$ の指数は $r$ の一次式になる。その指数が求めたい値になる $r$ を求める。",
               steps=[f"一般項：${C(n, 'r')}{bpow}\\left({cfx}\\right)^r={C(n, 'r')}({c})^r\\cdot x^{{{s}({n}-r)-r}}$。" if s == 2 else f"一般項：${C(n, 'r')}{bpow}\\left({cfx}\\right)^r={C(n, 'r')}({c})^r\\cdot x^{{({n}-r)-r}}$。",
                      f"指数 ${s}({n}-r)-r={e}$ を解いて $r={k}$。" if s == 2 else f"指数 $({n}-r)-r={e}$ を解いて $r={k}$。",
                      f"${C(n, k)}\\cdot({c})^{{{k}}}={comb(n, k)}\\cdot({c ** k})={val}$。"],
               alt=["指数法則 $\\dfrac{x^m}{x^r}=x^{m-r}$ を使わず、分母と分子の $x$ の個数を数えて約分してもよい。"],
               pc=[("一般項の $x$ の指数を $r$ で表している", 2), ("$r$ を決めて係数を正しく計算している", 2)],
               pit=[f"$({base})^{{{n}-r}}$ の指数を ${n}-r$ のままにする（$x^2$ の場合は $2({n}-r)$）。" if s == 2 else "$\\dfrac{1}{x}$ の指数を $+r$ と数える。",
                    "$c^r$ の符号を落とす。"],
               chk=(f"binomial({n},{k})*({c})**{k}", str(val)))


@gen("standard_practice", 5, ["computation"])
def fraction_calc(r):
    a, b = r.sample([v for v in range(-5, 6) if v != 0], 2)
    p, q = nonzero(r, -4, 4), nonzero(r, -4, 4)
    op = r.choice(["+", "-"])
    qq = q if op == "+" else -q
    N = [p + qq, p * b + qq * a]
    den = f"(x{shift(a)})(x{shift(b)})"
    num_t = pt(N)
    left = f"\\dfrac{{{p}}}{{x{shift(a)}}}{op}\\dfrac{{{q}}}{{x{shift(b)}}}".replace("\\dfrac{-", "-\\dfrac{")
    left = left.replace("+-\\dfrac", "-\\dfrac").replace("--\\dfrac", "+\\dfrac")
    ans = f"$\\dfrac{{{num_t}}}{{{den}}}$"
    return sa(f"分数式 ${left}$ を計算し、1つの分数式で表しなさい。", ans,
              f"分母を ${den}$ にそろえて分子を計算すると ${num_t}$。", d=3,
              v=[f"({num_t})/{den}"],
              ap="整数の分数と同じく、分母の最小公倍数 $" + den + "$ で通分してから分子を計算する。",
              steps=[f"通分：$\\dfrac{{{p}(x{shift(b)}){'+' if qq > 0 else '-'}{abs(q)}(x{shift(a)})}}{{{den}}}$。",
                     f"分子を展開・整理：${num_t}$。", "分子と分母に共通な因数がないことを確かめて答えとする。"],
              alt=[f"$x=0$ など分母が $0$ にならない値を代入し、もとの式と答えの値が一致するか確かめる（$x=0$ なら ${frac_v(p, a, q if op == '+' else -q, b)}$）。"],
              pc=[("正しく通分している", 1), ("分子を符号も含めて正しく整理している", 2), ("約分の確認をして答えている", 1)],
              pit=["引き算で、引く分数の分子全体にかっこをつけずに符号を誤る。", "分母どうし・分子どうしを足してしまう。"],
              chk=(f"simplify(({p})/(x+({a})){op}({q})/(x+({b}))-({ppy(N)})/((x+({a}))*(x+({b}))))", "0", None, "intermediate"))


def frac_v(p, a, q, b):
    from fractions import Fraction
    f = Fraction(p, a) + Fraction(q, b)
    return str(f.numerator) if f.denominator == 1 else f"\\dfrac{{{f.numerator}}}{{{f.denominator}}}".replace("\\dfrac{-", "-\\dfrac{")


@gen("standard_practice", 5, ["condition_check", "computation"])
def partial_fraction(r):
    m, n_ = r.sample([v for v in range(-5, 6) if v != 0], 2)
    A, B = nonzero(r, -5, 5), nonzero(r, -5, 5)
    N = [A + B, A * n_ + B * m]
    return sa(f"次の等式が $x$ についての恒等式であるとき、定数 $a,\\ b$ の値を求めなさい。$$\\dfrac{{{pt(N)}}}{{(x{shift(m)})(x{shift(n_)})}}=\\dfrac{{a}}{{x{shift(m)}}}+\\dfrac{{b}}{{x{shift(n_)}}}$$",
              f"$a={A},\\ b={B}$",
              f"両辺に $(x{shift(m)})(x{shift(n_)})$ を掛けた ${pt(N)}=a(x{shift(n_)})+b(x{shift(m)})$ の係数を比較する。", d=3,
              v=[f"a={A}, b={B}"],
              ap="分母を払って整式の恒等式にし、係数比較か数値代入で $a,\\ b$ を決める。",
              steps=[f"両辺に $(x{shift(m)})(x{shift(n_)})$ を掛けて ${pt(N)}=(a+b)x+({n_}a{cterm(m, 'b')})$。",
                     f"係数比較：$a+b={N[0]}$、${n_}a{cterm(m, 'b')}={N[1]}$。", f"連立して $a={A},\\ b={B}$。"],
              alt=[f"数値代入：$x={-m}$ を代入すると $b$ の項が消えて ${N[0] * (-m) + N[1]}={n_ - m}a$ より $a={A}$。同様に $x={-n_}$ で $b={B}$。（分母を払った後の整式の恒等式なので、$x={-m}$ を代入してよい。）"],
              pc=[("分母を払って整式の恒等式にしている", 1), ("係数比較の連立方程式を正しく立てている", 2), ("$a,\\ b$ を正しく求めている", 1)],
              pit=["分母を払うとき、右辺の各項に掛ける因数を取り違える。", "「分母が $0$ になる値は代入できない」と考えて数値代入をためらう（払った後の整式なら代入してよい）。"],
              chk=(f"solve([a+b-({N[0]}), ({n_})*a+({m})*b-({N[1]})], [a, b])", f"{{a: {A}, b: {B}}}", None, "intermediate"))


@gen("standard_practice", 5, ["cross_unit", "computation"], rel=["HS-MATHA-U01"])
def multinomial(r):
    n = r.randint(4, 7)
    beta, gamma = r.choice([1, 2, -1, -2, 3]), r.choice([1, 2, -1, -2, 3])
    p = r.randint(1, n - 2)
    q = r.randint(1, n - p - 1)
    s = n - p - q
    val = factorial(n) // (factorial(p) * factorial(q) * factorial(s)) * beta ** q * gamma ** s
    mult = factorial(n) // (factorial(p) * factorial(q) * factorial(s))

    def pw(v, e):
        return v if e == 1 else f"{v}^{{{e}}}"
    expr = f"x{cterm(beta, 'y')}{cterm(gamma, 'z')}"
    return num(f"$({expr})^{{{n}}}$ の展開式における ${pw('x', p)}{pw('y', q)}{pw('z', s)}$ の項の係数を求めなさい。", str(val),
               f"$x$ を ${p}$ 個、${lin(beta, 'y')}$ を ${q}$ 個、${lin(gamma, 'z')}$ を ${s}$ 個選ぶ選び方は $\\dfrac{{{n}!}}{{{p}!\\,{q}!\\,{s}!}}={mult}$ 通り。係数は ${mult}\\cdot({beta})^{{{q}}}\\cdot({gamma})^{{{s}}}={val}$。", d=3,
               ap="$n$ 個の因数のそれぞれから $x,\\ y,\\ z$ の項を1つずつ選ぶと考える。選び方の数は「同じものを含む順列」（数学A）の数になる。",
               steps=[f"${pw('x', p)}{pw('y', q)}{pw('z', s)}$ の項は、${n}$ 個の因数から $x$ を ${p}$ 個、${lin(beta, 'y')}$ を ${q}$ 個、${lin(gamma, 'z')}$ を ${s}$ 個選んで掛けたもの。",
                      f"選び方は $\\dfrac{{{n}!}}{{{p}!\\,{q}!\\,{s}!}}={mult}$ 通り（同じものを含む順列）。",
                      f"係数は ${mult}\\times({beta})^{{{q}}}\\times({gamma})^{{{s}}}={val}$。"],
               alt=[f"二項定理を2回使う方法：$\\{{x+({lin(beta, 'y')}{cterm(gamma, 'z')})\\}}^{{{n}}}$ の一般項から ${C(n, q + s)}x^{{{p}}}$、さらに $({lin(beta, 'y')}{cterm(gamma, 'z')})^{{{q + s}}}$ の展開から ${C(q + s, s)}$ を得て、${C(n, q + s)}\\cdot{C(q + s, s)}={comb(n, q + s) * comb(q + s, s)}$ 通り。"],
               pc=[("選び方の数を正しく求めている", 2), ("係数の累乗・符号を正しく掛けている", 2)],
               pit=["$y,\\ z$ の係数の累乗を掛け忘れる。", "選び方の数を ${}_n\\mathrm{C}_p$ だけで済ませる。"],
               chk=(f"factorial({n})/(factorial({p})*factorial({q})*factorial({s}))*({beta})**{q}*({gamma})**{s}", str(val)))


# ======================================================================
# C 思考力・記述応用
# ======================================================================

@gen("thinking_writing", 3, ["written_reasoning", "condition_check"])
def prove_ineq(r):
    m = r.randint(1, 5)
    e = r.randint(0, 4)
    q = m * m + e
    var1, var2 = r.choice([("x", "y"), ("a", "b"), ("p", "q")])
    my = f"{var1}-{lin(m, var2)}"
    if e == 0:
        eqc = f"${var1}={lin(m, var2)}$ のとき"
        rest = ""
    else:
        eqc = f"${var1}={var2}=0$ のとき"
        rest = f"+{lin(e, var2 + '^2')}" if e != 1 else f"+{var2}^2"
    qy = f"{var2}^2" if q == 1 else f"{q}{var2}^2"
    rhs = f"{2 * m}{var1}{var2}"
    return desc(f"${var1},\\ {var2}$ が実数のとき、不等式 ${var1}^2+{qy}\\geqq {rhs}$ を証明しなさい。また、等号が成り立つ条件を答えなさい。",
                f"$({var1}^2+{qy})-{rhs}=({my})^2{rest}\\geqq0$。よって ${var1}^2+{qy}\\geqq {rhs}$。等号は{eqc}成り立つ。",
                f"差をとって平方完成すると $({my})^2{rest}$ となり、実数の2乗は $0$ 以上であることから示せる。", rubric=[
                    ("（左辺）$-$（右辺）をつくって証明の方針を示している", 2), ("平方の和の形に正しく変形している", 3),
                    ("実数の2乗が $0$ 以上であることを根拠に結論している", 1), ("等号成立条件を正しく答えている", 2)], d=4, p=8, lines=8, kind="proof",
                ap=f"左辺と右辺の差を ${var1}$ についての二次式とみて平方完成すると、「（実数）$^2$ の和」になる。",
                steps=[f"$({var1}^2+{qy})-{rhs}={var1}^2-{2 * m}{var2}\\cdot {var1}+{qy}$。",
                       f"${var1}$ について平方完成：$({my})^2-{m * m if m > 1 else ''}{var2}^2+{qy}=({my})^2{rest}$。".replace("-1" + var2, "-" + var2),
                       f"$({my})^2\\geqq0$" + (f"、${var2}^2\\geqq0$ なので和は $0$ 以上。" if e else " なので差は $0$ 以上。"),
                       "等号は " + (f"${my}=0$ のとき、すなわち{eqc}。" if e == 0 else f"${my}=0$ かつ ${var2}=0$、すなわち{eqc}。")],
                alt=[f"判別式の利用：左辺 $-$ 右辺を ${var1}$ の二次式とみると、判別式 $D/4={lin(m * m, var2 + '^2')}-{q}{var2}^2={'0' if e == 0 else '-' + lin(e, var2 + '^2')}\\leqq0$ で ${var1}^2$ の係数が正なので、常に $0$ 以上（数学Ⅰ 二次関数）。"],
                pc=[("差をとる方針", 2), ("平方の和への変形", 3), ("結論の根拠", 1), ("等号成立条件", 2)],
                pit=["示したい不等式から出発して変形し、正しい式に到達したことで証明とする（逆向きの推論）。",
                     "等号成立条件で、" + ("$" + var2 + "=0$ の条件を見落とす。" if e else "比の関係 $" + var1 + "=" + lin(m, var2) + "$ を書き忘れる。")],
                chk=(f"expand(({var1}-{m}*{var2})**2+{e}*{var2}**2)", f"{var1}**2+{q}*{var2}**2-{2 * m}*{var1}*{var2}", "expand", "intermediate"))


@gen("thinking_writing", 3, ["written_reasoning", "condition_check"])
def shifted_amgm(r):
    s = r.randint(1, 4)
    m, k = r.choice([(1, 1), (1, 4), (1, 9), (1, 16), (2, 2), (2, 8), (3, 3), (3, 12), (4, 1), (4, 9), (2, 18), (5, 5)])
    root = isqrt(m * k)
    assert root * root == m * k
    # m(x-s)+k/(x-s) >= 2*root, 等号 m(x-s)^2=k
    import sympy as sp
    t = sp.sqrt(sp.Rational(k, m))
    x0 = sp.nsimplify(s + t)
    val = 2 * root + m * s
    return desc(f"$x>{s}$ のとき、$P={lin(m)}+\\dfrac{{{k}}}{{x-{s}}}$ の最小値と、そのときの $x$ の値を求めなさい。考え方も記述すること。",
                f"$P={m if m > 1 else ''}(x-{s})+\\dfrac{{{k}}}{{x-{s}}}+{m * s}\\geqq2\\sqrt{{{m * k}}}+{m * s}={val}$。等号は $x={sp.latex(x0)}$ のとき。最小値 ${val}$（$x={sp.latex(x0)}$）",
                f"$x-{s}>0$ に着目し、$P$ を「$x-{s}$ を含む2つの正の項の和＋定数」に変形してから相加平均と相乗平均の関係を使う。", rubric=[
                    ("$x-" + str(s) + ">0$ を確認し、積が一定になるよう式を変形している", 3), ("相加平均と相乗平均の関係を正しく適用している", 2),
                    ("等号成立の $x$ を求め、それが条件を満たすことを確かめている", 2), ("最小値を正しく答えている", 1)], d=4, p=8, lines=8,
                ap=f"そのままでは ${lin(m)}$ と $\\dfrac{{{k}}}{{x-{s}}}$ の積が一定にならない。$x-{s}$ をひとかたまりと見て、積が一定になる2項をつくる。",
                steps=[f"$t=x-{s}$ とおくと $t>0$ で、$P={lin(m, 't')}+\\dfrac{{{k}}}{{t}}+{m * s}$。",
                       f"$t>0$ より相加平均と相乗平均の関係から ${lin(m, 't')}+\\dfrac{{{k}}}{{t}}\\geqq2\\sqrt{{{m * k}}}={2 * root}$。",
                       f"等号は ${lin(m, 't')}=\\dfrac{{{k}}}{{t}}$、すなわち $t^2={sp.latex(sp.Rational(k, m))}$、$t>0$ より $t={sp.latex(t)}$。このとき $x={sp.latex(x0)}$ で、$x>{s}$ を満たす。",
                       f"最小値 $P={2 * root}+{m * s}={val}$。"],
                alt=[f"微分法（数学Ⅱ 微分）を学んだ後なら、$P$ を $x$ で微分して増減を調べても同じ結果が得られる。"],
                pc=[("式の変形", 3), ("関係式の適用", 2), ("等号成立の確認", 2), ("最小値", 1)],
                pit=[f"${lin(m)}$ と $\\dfrac{{{k}}}{{x-{s}}}$ にそのまま関係式を当てはめ、$x$ を含む式を「最小値」と答える。", "等号成立の $x$ が条件を満たすかを確かめない。"],
                chk=(f"2*sqrt({m}*{k})+{m * s}", str(val), None, "intermediate"))


@gen("thinking_writing", 2, ["cross_unit", "written_reasoning"], rel=["HS-MATHA-U01"])
def binom_sum(r):
    n = r.randint(4, 8)
    rr = r.choice([2, 3, 4, -2, -3])
    alt_sign = rr > 0 and r.random() < 0.4
    if alt_sign:
        val = (1 - rr) ** n
        body = f"{C(n, 0)}-{C(n, 1)}\\cdot{rr if rr > 0 else f'({rr})'}+{C(n, 2)}\\cdot{rr if rr > 0 else f'({rr})'}^2-\\cdots+(-1)^{{{n}}}{C(n, n)}\\cdot{rr if rr > 0 else f'({rr})'}^{{{n}}}"
        ident = f"(1+x)^{{{n}}}"
        sub = f"x={-rr}"
        chk_e = f"summation(binomial({n},k)*(-1)**k*({rr})**k, [k, 0, {n}])"
    else:
        val = (1 + rr) ** n
        body = f"{C(n, 0)}+{C(n, 1)}\\cdot{rr if rr > 0 else f'({rr})'}+{C(n, 2)}\\cdot{rr if rr > 0 else f'({rr})'}^2+\\cdots+{C(n, n)}\\cdot{rr if rr > 0 else f'({rr})'}^{{{n}}}"
        ident = f"(1+x)^{{{n}}}"
        sub = f"x={rr}"
        chk_e = f"summation(binomial({n},k)*({rr})**k, [k, 0, {n}])"
    base = 1 - rr if alt_sign else 1 + rr
    return desc(f"二項定理を利用して、和 $S={body}$ の値を求めなさい。どの等式にどの値を代入したかを明記すること。",
                f"二項定理 ${ident}={C(n, 0)}+{C(n, 1)}x+\\cdots+{C(n, n)}x^{{{n}}}$ に ${sub}$ を代入すると $S=({base})^{{{n}}}={val}$。",
                f"$S$ は $(1+x)^{{{n}}}$ の展開式に ${sub}$ を代入したものになっている。", rubric=[
                    ("二項定理による展開式を正しく書いている", 3), ("代入する値を正しく選び、その理由を述べている", 3), ("$S$ の値を正しく計算している", 2)], d=4, p=8, lines=6,
                ap=f"各項が ${C(n, 'k')}\\cdot(\\text{{ある数}})^k$ の形をしている。これは $(1+x)^{{{n}}}$ の展開式の一般項 ${C(n, 'k')}x^k$ に数を代入した形である。",
                steps=[f"二項定理より ${ident}=\\sum_{{k=0}}^{{{n}}}{C(n, 'k')}x^k$（すべての $x$ で成り立つ恒等式）。",
                       f"$S$ の第 $k+1$ 項は ${C(n, 'k')}\\cdot({-rr if alt_sign else rr})^k$ なので、${sub}$ を代入すればよい。",
                       f"$S=(1{'+' if (-rr if alt_sign else rr) > 0 else ''}{-rr if alt_sign else rr})^{{{n}}}=({base})^{{{n}}}={val}$。"],
                alt=[f"組合せの意味からの確認（数学A）：${C(n, 'k')}\\cdot{rr}^k$ は「${n}$ 個のものから $k$ 個を選び、選んだものそれぞれに ${rr}$ 種類の印のどれかをつける」方法の数である。各ものは「選ばない」を含めて ${1 + rr}$ 通りの状態をとるので、総数は ${1 + rr}^{{{n}}}$ となり一致する。" if not alt_sign and rr > 0
                     else f"小さい場合で確かめる：$n=2$ なら ${C(2, 0)}+{C(2, 1)}x+{C(2, 2)}x^2=1+2x+x^2=(1+x)^2$ であり、${sub}$ を代入した値と和を直接計算した値が一致する。"],
                pc=[("展開式", 3), ("代入値の選択と理由", 3), ("計算", 2)],
                pit=["符号が交互に変わる和で、$x$ に代入する値の符号を誤る。", f"$S$ の最後の項 ${C(n, n)}$ の係数を数え落とす。"],
                chk=(chk_e, str(val), None, "intermediate"))


@gen("thinking_writing", 2, ["condition_check", "multiple_solutions"])
def divisible_cond(r):
    p, q = nonzero(r, -3, 3), nonzero(r, -4, 4)
    c2 = r.randint(-4, 4)
    t = c2 - p
    A = q + p * t
    B = q * t
    D = [1, p, q]
    return sa(f"整式 $P(x)=x^3{cterm(c2, 'x^2') if c2 else ''}+ax+b$ が $x^2{cterm(p, 'x')}{'+' if q > 0 else ''}{q}$ で割り切れるように、定数 $a,\\ b$ の値を定めなさい。",
              f"$a={A},\\ b={B}$",
              f"$P(x)$ を $x^2{cterm(p, 'x')}{'+' if q > 0 else ''}{q}$ で割ると商は $x{shift(t) if t else ''}$、余りは $(a-({A}))x+(b-({B}))$。余りが $0$ になる条件から求める。", d=4, p=8,
              v=[f"a={A}, b={B}"],
              ap="「割り切れる」は「余りが $0$」と同じ。実際に割り算をして余りを $a,\\ b$ で表し、余りが恒等的に $0$ になる条件（$x$ の係数も定数項も $0$）を立てる。",
              steps=[f"$P(x)$ を $x^2{cterm(p, 'x')}{'+' if q > 0 else ''}{q}$ で割ると、商 $x{shift(t) if t else ''}$。",
                     f"余りは $(a-({A}))x+(b-({B}))$。",
                     f"余りが恒等的に $0$ である条件：$a-({A})=0$ かつ $b-({B})=0$。", f"$a={A},\\ b={B}$。"],
              alt=[f"恒等式の利用：$P(x)$ は3次式で $x^3$ の係数が $1$ なので、$P(x)=(x^2{cterm(p, 'x')}{'+' if q > 0 else ''}{q})(x+k)$ とおける。$x^2$ の係数を比べて $k={t}$、展開して $x$ の係数・定数項を比べると $a={A},\\ b={B}$。"],
              pc=[("余りを $a,\\ b$ で正しく表している（または恒等式を正しく立てている）", 4), ("余りの各係数を $0$ とおく条件を立てている", 2), ("$a,\\ b$ を正しく求めている", 2)],
              pit=["余りが $0$ になる条件で、$x$ の係数か定数項の一方だけを $0$ とおく。", "割り算の途中で $a,\\ b$ を含む項の符号を誤る。"],
              chk=(f"solve([a-({A}), b-({B}), expand({ppy(pmul(D, [1, t]))}-(x**3+({c2})*x**2+({A})*x+({B})))], [a, b])", f"{{a: {A}, b: {B}}}", None, "intermediate"))


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(stem, wrong, step, etype, tempt, fix, ans, expl, steps, ap, alt, pit, chk=None, d=3):
    return desc(f"{stem}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい答えを求めなさい。", ans, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい解答を途中式とともに示している", 3), ("最終的な答えが正しい", 1)], d=d, p=6, lines=6,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい途中式", 3), ("正しい答え", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix), chk=chk)


@gen("error_correction", 3, ["common_error", "computation"])
def err_binom(r):
    kind = r.choice(["sign", "coef"])
    n = r.randint(4, 7)
    if kind == "sign":
        a = 1
        b = -r.randint(1, 4)
        k = r.choice([k for k in range(1, n) if (n - k) % 2 == 1])
    else:
        a = r.choice([2, 3])
        b = r.choice([1, 2, -1, 3])
        k = r.randint(2, n - 1)
    val = comb(n, k) * a ** k * b ** (n - k)
    expr = poly(a, b)
    if kind == "sign":
        wv = comb(n, k) * abs(b) ** (n - k)
        wrong = f"一般項は ${C(n, 'r')}x^{{{n}-r}}\\cdot{abs(b)}^r$。$x^{{{k}}}$ の項は $r={n - k}$ のときなので、係数は ${C(n, n - k)}\\cdot{abs(b)}^{{{n - k}}}={wv}$"
        step = "一般項で $b$ を $" + str(abs(b)) + "$ としている部分"
        tempt = f"$({expr})^{{{n}}}$ の「$-$」を引き算の記号と見て、二項定理の $b$ を正の数 ${abs(b)}$ としてしまった。"
        etype = "sign"
    else:
        wv = comb(n, k) * a * b ** (n - k)
        wrong = f"一般項は ${C(n, 'r')}\\cdot{a}x^{{{n}-r}}\\cdot({b})^r$。$x^{{{k}}}$ の項は $r={n - k}$ のときなので、係数は ${C(n, n - k)}\\cdot{a}\\cdot({b})^{{{n - k}}}={wv}$"
        step = f"一般項で $({a}x)^{{{n}-r}}$ を ${a}x^{{{n}-r}}$ としている部分"
        tempt = f"$({a}x)^{{{n}-r}}$ の指数が $x$ だけにかかると思い、係数 ${a}$ を累乗し忘れた。"
        etype = "calculation"
    fix = f"一般項は ${C(n, 'r')}({lin(a)})^{{{n}-r}}({b})^r$。$r={n - k}$ として係数は ${C(n, n - k)}\\cdot{a}^{{{k}}}\\cdot({b})^{{{n - k}}}={val}$"
    return err_item(f"$({expr})^{{{n}}}$ の展開式における $x^{{{k}}}$ の係数を求めなさい。", wrong, step, etype, tempt, fix, f"${val}$",
                    f"二項定理の $a,\\ b$ には「項全体」を、符号や係数も含めて代入する。$a={lin(a)}$、$b={b}$。",
                    [f"$a={lin(a)}$、$b={b}$ として一般項 ${C(n, 'r')}({lin(a)})^{{{n}-r}}({b})^r$。", f"$x^{{{k}}}$ の項は $r={n - k}$。",
                     f"係数 ${comb(n, k)}\\cdot{a ** k}\\cdot({b ** (n - k)})={val}$。"],
                    "二項定理の $a,\\ b$ にかっこごと代入し、係数・符号もまとめて累乗する。",
                    [f"$n$ が小さいうちは $({expr})^2$ などで一般項の式と実際の展開を比べると、代入の仕方の誤りに気づける。"],
                    ["負の数・係数つきの項はかっこをつけて累乗する。"],
                    chk=(f"binomial({n},{k})*({a})**{k}*({b})**{n - k}", str(val), None, "intermediate"), d=2)


@gen("error_correction", 3, ["common_error", "condition_check"])
def err_amgm_double(r):
    p, q = r.choice([(1, 4), (4, 1), (1, 9), (9, 1), (2, 8), (8, 2), (1, 16), (4, 9), (9, 4), (3, 12), (12, 3), (1, 25), (2, 18)])
    root = isqrt(p * q)
    wv = 4 * root
    val = p + q + 2 * root
    stem = f"$x>0,\\ y>0$ のとき、$\\left(x+\\dfrac{{{p}}}{{y}}\\right)\\left(y+\\dfrac{{{q}}}{{x}}\\right)$ の最小値を求めなさい。"
    wrong = (f"相加平均と相乗平均の関係より $x+\\dfrac{{{p}}}{{y}}\\geqq2\\sqrt{{\\dfrac{{{p}x}}{{y}}}}$、$y+\\dfrac{{{q}}}{{x}}\\geqq2\\sqrt{{\\dfrac{{{q}y}}{{x}}}}$。"
             f"辺々掛けて $\\left(x+\\dfrac{{{p}}}{{y}}\\right)\\left(y+\\dfrac{{{q}}}{{x}}\\right)\\geqq4\\sqrt{{{p * q}}}={wv}$。よって最小値は ${wv}$")
    fix = f"展開して $xy+\\dfrac{{{p * q}}}{{xy}}+{p + q}\\geqq2\\sqrt{{{p * q}}}+{p + q}={val}$。等号は $xy={root}$ のとき成り立つので最小値 ${val}$"
    return err_item(stem, wrong, "「よって最小値は」と結論した部分（等号成立条件の確認もれ）", "condition",
                    "不等式 $\\geqq " + str(wv) + "$ 自体は正しいので、右辺がそのまま最小値になると思い込みやすい。2つの等号が同時に成り立つかを確かめていない。",
                    fix, f"最小値 ${val}$",
                    f"1つ目の等号は $xy={p}$、2つ目の等号は $xy={q}$ のときで、同時には成り立たない。したがって ${wv}$ には到達しない。",
                    [f"展開：$xy+{q}+{p}+\\dfrac{{{p * q}}}{{xy}}$。", f"$xy>0$ より $xy+\\dfrac{{{p * q}}}{{xy}}\\geqq2\\sqrt{{{p * q}}}={2 * root}$。",
                     f"等号は $xy={root}$ のとき（例えば $x=1,\\ y={root}$）で、実際に成り立つ。", f"最小値 ${2 * root}+{p + q}={val}$。"],
                    "相加平均と相乗平均の関係で得た下限を最小値と言うには、等号を成り立たせる値が実際に存在することを確かめる必要がある。",
                    [f"$x=1,\\ y={root}$ を代入すると $\\left(1+\\dfrac{{{p}}}{{{root}}}\\right)({root}+{q})={val}$ となり、値 ${val}$ が実際にとられることを確かめられる。"],
                    ["不等式を2回使って掛け合わせたときは、等号成立条件が両立するかを確認する。"],
                    chk=(f"{p}+{q}+2*sqrt({p}*{q})", str(val), None, "intermediate"), d=4)


@gen("error_correction", 2, ["common_error", "computation"])
def err_div_missing(r):
    t = nonzero(r, -3, 3)
    b = nonzero(r, -6, 6)
    c = r.randint(-8, 8)
    Pq = [1, 0, b, c]
    Q, R, _ = long_div(Pq, [1, -t])
    wq = [1, b + t]
    wr = c + t * (b + t)
    wrong = f"係数を並べて組立除法を行う：$1,\\ {b},\\ {c}$ を $x{shift(-t)}$ で割って、商 ${pt(wq)}$、余り ${wr}$"
    fix = f"$x^2$ の係数 $0$ を入れて $1,\\ 0,\\ {b},\\ {c}$ と並べ、商 ${pt(Q)}$、余り ${R[0]}$"
    return err_item(f"整式 $x^3{cterm(b, 'x')}{'+' if c > 0 else ''}{c if c else ''}$ を $x{shift(-t)}$ で割ったときの商と余りを求めなさい。".replace("+0", ""), wrong,
                    "係数を並べる段階（$x^2$ の係数 $0$ の書き落とし）", "notation",
                    "式に $x^2$ の項が見えないため、係数の列に書くべき $0$ を省いてしまった。係数だけを扱う方法では各位置が次数を表すことを意識していない。",
                    fix, f"商 ${pt(Q)}$、余り ${R[0]}$",
                    f"係数の並びは $x^3,\\ x^2,\\ x$、定数の順の位置で次数を表すので、$x^2$ の係数 $0$ を省くと3次式が2次式として計算されてしまう。",
                    [f"$x^3+0x^2{cterm(b, 'x')}{'+' if c >= 0 else ''}{c}$ と考え、係数 $1,\\ 0,\\ {b},\\ {c}$ を並べる。",
                     f"$x{shift(-t)}$ で割ると商 ${pt(Q)}$。", f"余り ${R[0]}$（$x={t}$ を代入した値に一致）。"],
                    "抜けている次数がある整式は、係数 $0$ を補ってから割り算する。",
                    [f"検算：$({pt([1, -t])})({pt(Q)})+({R[0]})$ を展開すると $x^3{cterm(b, 'x')}{'+' if c >= 0 else ''}{c}$ にもどる。生徒の答えでは3次の項が出てこない。"],
                    ["抜けた次数の欄を空けずに筆算・組立除法をする。"],
                    chk=(f"expand(({ppy([1, -t])})*{ppy(Q)}+({R[0]}))", ppy(Pq), "expand", "intermediate"))


@gen("error_correction", 2, ["common_error", "computation"])
def err_fraction_minus(r):
    while True:
        a, b = r.sample([v for v in range(-4, 5) if v != 0], 2)
        u, v = r.randint(-5, 5), r.randint(-5, 5)
        N = [u + b - v - a, u * b - v * a]
        if N[0] == 0 or u == a or v == b:
            continue
        # 約分できないか（分子が x+a または x+b を因数にもたない）
        if N[0] * (-a) + N[1] == 0 or N[0] * (-b) + N[1] == 0:
            continue
        break
    W = [u + b + v + a, u * b + v * a]
    den = f"(x{shift(a)})(x{shift(b)})"
    f1 = f"\\dfrac{{x{shift(u) if u else ''}}}{{x{shift(a)}}}"
    f2 = f"\\dfrac{{x{shift(v) if v else ''}}}{{x{shift(b)}}}"
    wrong = (f"$\\dfrac{{(x{shift(u) if u else ''})(x{shift(b)})-(x{shift(v) if v else ''})(x{shift(a)})}}{{{den}}}"
             f"=\\dfrac{{x^2{cterm(u + b, 'x') if u + b else ''}{'+' if u * b >= 0 else ''}{u * b}-x^2{cterm(v + a, 'x') if v + a else ''}{'+' if v * a >= 0 else ''}{v * a}}}{{{den}}}=\\dfrac{{{pt(W)}}}{{{den}}}$")
    fix = f"分子 $=(x{shift(u) if u else ''})(x{shift(b)})-\\{{x^2{cterm(v + a, 'x') if v + a else ''}{'+' if v * a >= 0 else ''}{v * a}\\}}={pt(N)}$ より $\\dfrac{{{pt(N)}}}{{{den}}}$"
    return err_item(f"分数式 ${f1}-{f2}$ を計算しなさい。", wrong, "分子の展開で、引く式の第2項以降の符号を変えていない部分", "sign",
                    "$-(x" + (shift(v) if v else "") + ")(x" + shift(a) + ")$ を展開するとき、$-$ を先頭の $x^2$ にしか付けず、残りの項の符号を変え忘れた。",
                    fix, f"$\\dfrac{{{pt(N)}}}{{{den}}}$",
                    "引く式は展開した結果全体にかっこをつけてから符号を変える。",
                    [f"通分：分子は $(x{shift(u) if u else ''})(x{shift(b)})-(x{shift(v) if v else ''})(x{shift(a)})$。",
                     f"$(x{shift(v) if v else ''})(x{shift(a)})=x^2{cterm(v + a, 'x') if v + a else ''}{'+' if v * a >= 0 else ''}{v * a}$ をかっこごと引く。",
                     f"分子 $={pt(N)}$。分母と共通因数はないので答えは $\\dfrac{{{pt(N)}}}{{{den}}}$。"],
                    "引き算では、引く式を展開した結果全体にかっこをつける。",
                    [f"$x=0$ を代入すると、もとの式は ${frac_v(u, a, -v, b)}$、正しい答えは ${frac_v(N[1], a * b, 0, 1)}$ で一致する。生徒の答えでは一致しない。"],
                    ["引く式のかっこを外すときに、一部の項の符号しか変えない。"],
                    chk=(f"simplify((x+({u}))/(x+({a}))-(x+({v}))/(x+({b}))-({ppy(N)})/((x+({a}))*(x+({b}))))", "0", None, "intermediate"))


GENERATORS = [binom_coef, poly_division, identity_coef, amgm_min,
              binom_const_term, fraction_calc, partial_fraction, multinomial,
              prove_ineq, shifted_amgm, binom_sum, divisible_cond,
              err_binom, err_amgm_double, err_div_missing, err_fraction_minus]
