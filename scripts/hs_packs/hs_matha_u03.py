"""単元パック：数学A 数学と人間の活動（整数）。"""
from fractions import Fraction
from math import gcd

from banks._common import desc, num, sa
from hs_pack_lib import (board, check, definition, example, gen, guide, intro, lesson, summary, theorem, tp)

UNIT_ID = "HS-MATHA-U03"


# ---------------------------------------------------------------------------
# 補助
# ---------------------------------------------------------------------------

def lcm(a, b):
    return a * b // gcd(a, b)


def factorize(n):
    out, p = {}, 2
    while p * p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
        p += 1
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def fac_tex(f):
    return "\\cdot ".join(f"{p}^{{{e}}}" if e > 1 else f"{p}" for p, e in sorted(f.items()))


def ndiv(f):
    k = 1
    for e in f.values():
        k *= e + 1
    return k


def sdiv(f):
    k = 1
    for p, e in f.items():
        k *= (p ** (e + 1) - 1) // (p - 1)
    return k


def to_base(n, b):
    ds = []
    while n:
        ds.append(n % b)
        n //= b
    return "".join(str(d) for d in reversed(ds)) or "0"


def base_tex(digits, b):
    return f"{digits}_{{({b})}}"


def base_poly(digits, b):
    """'1011',2 → '1*2**3+0*2**2+1*2**1+1*2**0'"""
    k = len(digits)
    return "+".join(f"{d}*{b}**{k - 1 - i}" for i, d in enumerate(digits))


def base_poly_tex(digits, b):
    k = len(digits)
    return "+".join(f"{d}\\cdot {b}^{{{k - 1 - i}}}" if k - 1 - i > 0 else f"{d}" for i, d in enumerate(digits))


def euclid_steps(a, b):
    lines = []
    while b:
        q, r = divmod(a, b)
        lines.append(f"${a}={b}\\times{q}+{r}$")
        a, b = b, r
    return lines, a


def dioph(a, b, c, minus=False):
    """a x + b y = c（minus=True なら a x - b y = c）の、0≦x0<b となる特殊解 (x0, y0)。"""
    inv = pow(a, -1, b)
    x0 = (c * inv) % b
    y0 = (c - a * x0) // b if not minus else (a * x0 - c) // b
    return x0, y0


def sgn_term(v, var):
    if v == 0:
        return var
    return f"{var}{'+' if v > 0 else '-'}{abs(v)}"


LESSON = lesson(
    goals=["素因数分解を用いて、約数の個数・総和、最大公約数・最小公倍数を求め、その理由を説明できる。",
           "ユークリッドの互除法の原理を理解し、最大公約数の計算と一次不定方程式の整数解の決定に活用できる。",
           "余りによる整数の分類を用いて整数の性質を証明でき、$n$ 進法と10進法の変換ができる。"],
    duration=100,
    readiness=["素因数分解（中学1年）ができる。", "整数の割り算を「割られる数＝割る数×商＋余り」の形で書ける。", "文字式による整数の表し方（偶数 $2k$、奇数 $2k+1$）を使える。"],
    flow=[("導入：大きな数の最大公約数", 8, "素因数分解しにくい 2 数の最大公約数を求める方法を問い、互除法の必要性を感じさせる"),
          ("約数と倍数", 17, "約数の個数・総和の公式を、展開による数え上げとして導く。例題1"),
          ("ユークリッドの互除法", 20, "原理の証明（公約数の集合が一致する）と計算の手順"),
          ("一次不定方程式", 25, "互除法の逆算で特殊解を見つけ、一般解を互いに素の性質から導く。例題2"),
          ("余りによる分類と n 進法", 20, "余りで分けて証明する方法、n 進法と10進法の変換。例題3"),
          ("まとめと確認", 10, "確認問題3問、問題プリントAの課題指示")],
    sections=[
        intro("in1", "割り算の「余り」が主役になる",
              "整数の世界では、割り切れるかどうか、割ったときの余りがいくつかが大切な情報になる。たとえば 391 と 299 の最大公約数は、素因数分解をしなくても、割り算をくり返すだけで求められる。また、ある整数を 3 で割った余りは 0, 1, 2 のどれかなので、すべての整数を3つのグループに分けて調べれば、無限にある整数についての性質を有限回の確認で証明できる。",
              bullets=["割り算の基本式：$a=bq+r\\quad(0\\leqq r<b)$", "余りに注目すると、「無限の整数」を「有限個の場合」に分けて扱える。"],
              points=[tp("最初に 391 と 299 を素因数分解させて、時間がかかることを体験させてから互除法を紹介する。", ask="391 と 299 の最大公約数を求めるには、どうすればよいか。", expect="素因数分解する（が、どちらも割り切る素数を見つけにくい）。", timing="導入の冒頭")]),
        definition("df1", "約数・倍数と素因数分解",
                   "整数 $a$、$b$ について、$a=bk$ を満たす整数 $k$ があるとき、$b$ を $a$ の約数、$a$ を $b$ の倍数という。2つ以上の整数に共通な約数のうち最大のものを最大公約数、共通な正の倍数のうち最小のものを最小公倍数という。",
                   formula="$$a=ga',\\ b=gb'\\ (a',b'\\ \\text{は互いに素})\\ \\Longrightarrow\\ \\text{最小公倍数}\\ l=ga'b',\\qquad ab=gl$$",
                   conditions=["$g$ は $a$、$b$ の最大公約数。", "2つの整数の最大公約数が $1$ のとき、2つの整数は互いに素であるという。",
                               "最大公約数は共通な素因数を「少ない方の指数」で、最小公倍数はすべての素因数を「多い方の指数」でかけ合わせて求められる。"],
                   points=[tp("$ab=gl$ は、$a'$ と $b'$ が互いに素であることから成り立つ。互いに素の条件を落とすと成り立たないことを例で示す。", caution="$a=4,\\ b=6$ を $2\\cdot2,\\ 2\\cdot3$ と分けて $a'=2,\\ b'=3$ としても $g$ は $2$ のまま。")]),
        theorem("th1", "約数の個数と総和",
                "$$N=p^aq^br^c\\ \\Longrightarrow\\ \\text{正の約数の個数}=(a+1)(b+1)(c+1),\\quad \\text{総和}=(1+p+\\cdots+p^a)(1+q+\\cdots+q^b)(1+r+\\cdots+r^c)$$",
                ["$p,\\ q,\\ r$ は異なる素数（素因数分解した形で使う）。", "素因数が2個や4個以上の場合も同様。"],
                proof=["$N$ の正の約数は $p^xq^yr^z$（$0\\leqq x\\leqq a,\\ 0\\leqq y\\leqq b,\\ 0\\leqq z\\leqq c$）の形にちょうど1通りに表される（素因数分解の一意性）。",
                       "指数 $x$ の選び方は $a+1$ 通り、$y$ は $b+1$ 通り、$z$ は $c+1$ 通り。積の法則より約数の個数は $(a+1)(b+1)(c+1)$。",
                       "$(1+p+\\cdots+p^a)(1+q+\\cdots+q^b)(1+r+\\cdots+r^c)$ を展開すると、各項は $p^xq^yr^z$ の形で、すべての約数がちょうど1回ずつ現れる。よってこの積が総和になる。"],
                points=[tp("指数 $0$ も選べる（その素数を含まない約数）ことが「$+1$」の理由であることを強調する。", ask="$p^0$ は何を表すか。", expect="$1$。その素因数を使わないこと。")]),
        theorem("th2", "ユークリッドの互除法",
                "$$a=bq+r\\ \\Longrightarrow\\ \\gcd(a,\\,b)=\\gcd(b,\\,r)$$",
                ["$a,\\ b$ は正の整数、$q$ は商、$r$ は余り（$0\\leqq r<b$）。", "割り算をくり返して余りが $0$ になったときの割る数が、最大公約数である。"],
                proof=["$a$ と $b$ の公約数を $d$ とすると、$r=a-bq$ も $d$ で割り切れるので、$d$ は $b$ と $r$ の公約数である。",
                       "逆に $b$ と $r$ の公約数を $d'$ とすると、$a=bq+r$ も $d'$ で割り切れるので、$d'$ は $a$ と $b$ の公約数である。",
                       "したがって「$a$ と $b$ の公約数全体」と「$b$ と $r$ の公約数全体」は一致し、その最大のものも等しい。",
                       "余りは割るたびに小さくなる非負の整数なので、有限回で $0$ になり、計算は必ず終わる。"],
                points=[tp("証明の中心は「公約数の集合が一致する」こと。等式 $r=a-bq$ の役割を言葉で説明させる。", ask="$a$ と $b$ を割り切る数は、なぜ $r$ も割り切るのか。")]),
        example("ex1", "例題1　互除法",
                "互除法を用いて、$437$ と $323$ の最大公約数を求めよ。",
                ["$437=323\\times1+114$", "$323=114\\times2+95$", "$114=95\\times1+19$", "$95=19\\times5+0$"],
                "最大公約数は $19$",
                thinking="大きい方を小さい方で割り、「割る数」と「余り」で次の割り算をする。余りが $0$ になったときの割る数が答え。",
                points=[tp("各段で「割る数→次の割られる数」「余り→次の割る数」と左下へずれていく形を板書で見せる。")]),
        theorem("th3", "一次不定方程式の整数解",
                "$$ax+by=c\\ \\text{の1つの解を}\\ (x_0,\\,y_0)\\ \\text{とすると、すべての整数解は}\\ x=x_0+bk,\\ y=y_0-ak\\ (k\\ \\text{は整数})$$",
                ["$a,\\ b$ は互いに素な整数（$ab\\neq0$）。", "$a$ と $b$ の最大公約数が $c$ を割り切らなければ、整数解はない。"],
                proof=["$ax+by=c$ と $ax_0+by_0=c$ の差をとると $a(x-x_0)=-b(y-y_0)$。",
                       "左辺は $a$ の倍数なので $b(y-y_0)$ も $a$ の倍数。$a$ と $b$ は互いに素なので、$y-y_0$ が $a$ の倍数となり、$y-y_0=-ak$（$k$ は整数）とおける。",
                       "これを代入すると $a(x-x_0)=abk$、$a\\neq0$ より $x-x_0=bk$。",
                       "逆に $x=x_0+bk,\\ y=y_0-ak$ は方程式を満たすので、これがすべての整数解である。"],
                points=[tp("「$a$ と $b$ が互いに素だから $y-y_0$ が $a$ の倍数」という一文が証明の核心。互いに素でない例（$4\\times3=6\\times2$）で、この推論が成り立たないことを示す。", caution="互いに素の確認を省いて一般解を書く答案が多い。")]),
        example("ex2", "例題2　互除法の逆算で解を見つける",
                "方程式 $17x+12y=1$ の整数解をすべて求めよ。",
                ["互除法：$17=12\\times1+5$、$12=5\\times2+2$、$5=2\\times2+1$。",
                 "逆にたどる：$1=5-2\\times2=5-(12-5\\times2)\\times2=5\\times5-12\\times2=(17-12)\\times5-12\\times2=17\\times5+12\\times(-7)$。",
                 "特殊解 $(x,\\,y)=(5,\\,-7)$。$17(x-5)=-12(y+7)$、17 と 12 は互いに素なので $x-5=12k$。",
                 "$x=12k+5,\\ y=-17k-7$（$k$ は整数）。"],
                "$x=12k+5,\\ y=-17k-7$（$k$ は整数）",
                thinking="係数が大きく特殊解が見つけにくいので、互除法の式を下から逆にたどって $17\\times\\square+12\\times\\triangle=1$ の形をつくる。",
                points=[tp("得られた一般解に $k=0,\\ 1$ を代入し、もとの方程式を満たすことを確かめさせる。")],
                misconceptions=[("$x=5+17k,\\ y=-7-12k$ とする", "$x$ には相手の係数 $12$ がつく：$17\\cdot12k-12\\cdot17k=0$ となるように組み合わせる")]),
        definition("df2", "n 進法",
                   "$n$ を2以上の整数とするとき、数を $n$ 個ずつまとめて位を上げて表す方法を $n$ 進法といい、$n$ 進法で表された数を $\\square_{(n)}$ と書く。各位の数字は $0$ から $n-1$ まで。",
                   formula="$$a_ka_{k-1}\\cdots a_1a_0{}_{(n)}=a_k\\cdot n^k+a_{k-1}\\cdot n^{k-1}+\\cdots+a_1\\cdot n+a_0$$",
                   conditions=["10進法から $n$ 進法へは、$n$ で割った余りを下の位から順に求め、最後に下から読む。", "小数部分 $0.b_1b_2\\cdots{}_{(n)}=\\dfrac{b_1}{n}+\\dfrac{b_2}{n^2}+\\cdots$"],
                   points=[tp("$n$ で割ったときの余りが一の位になる理由（$a_0$ 以外はすべて $n$ の倍数）を、展開式から説明させる。", ask="$n$ 進法の数を $n$ で割った余りは、どの位の数字か。", expect="一の位 $a_0$。")]),
        example("ex3", "例題3　余りによる分類",
                "整数 $n$ について、$n^2$ を $3$ で割った余りは $0$ または $1$ であることを証明せよ。",
                ["すべての整数は、$k$ を整数として $3k,\\ 3k+1,\\ 3k+2$ のいずれかで表される。",
                 "$n=3k$ のとき $n^2=3\\cdot3k^2$ で余り $0$。",
                 "$n=3k+1$ のとき $n^2=3(3k^2+2k)+1$ で余り $1$。",
                 "$n=3k+2$ のとき $n^2=9k^2+12k+4=3(3k^2+4k+1)+1$ で余り $1$。"],
                "いずれの場合も余りは $0$ または $1$ である。（証明終）",
                thinking="「3 で割った余り」が問題なので、$n$ を 3 で割った余りで3つの場合に分ける。",
                points=[tp("場合分けが「すべての整数をもれなく、重複なく」覆っていることを最初に書かせる。", caution="$n=3k+2$ を $3k-1$ と書いてもよいことにも触れる。")]),
        board("bd1", "板書案",
              [("① 約数と倍数", ["$N=p^aq^b$", "個数 $(a+1)(b+1)$", "総和 $(1+\\cdots+p^a)(1+\\cdots+q^b)$", "$ab=gl$（$a'$, $b'$ 互いに素）"]),
               ("② 互除法と不定方程式", ["$a=bq+r\\Rightarrow\\gcd(a,b)=\\gcd(b,r)$", "$437,\\ 323\\to 19$", "$17x+12y=1$：逆算で $(5,-7)$", "$x=12k+5,\\ y=-17k-7$"]),
               ("③ 余りと n 進法", ["$n=3k,\\ 3k+1,\\ 3k+2$ で場合分け", "$n^2$ を $3$ で割った余りは $0,\\ 1$", "$1011_{(2)}=8+2+1=11$", "$n$ で割った余りを下から読む"])],
              points=[tp("②では互除法の式を左に縦に並べ、右側に逆算の式を書いて、同じ数がどこから来たかを矢印で結ぶ。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("約数の個数では、まず素因数分解の結果を指数まで確認させてから公式に入る。", caution="指数の積 $a\\times b$ を答える誤りが多い。"),
               tp("不定方程式の一般解は、求めた後に必ず代入して検算させる。", timing="例題2の後"),
               tp("互除法の逆算では、余りを「割られる数 − 割る数×商」の形で書き直すことを1段ずつ確認させる。", ask="$2$ はどの式から、何と何で表せるか。"),
               tp("$n$ 進法への変換では、余りを読む順序（下から上）を、変換後の数を10進法にもどして確かめさせる。"),
               tp("最大公約数・最小公倍数から2数を求める問題では、$a'$ と $b'$ が互いに素であるという条件を必ず使わせる。", caution="互いに素でない組を答えに含める誤りが典型的。")],
              misconceptions=[("$72=2^3\\cdot3^2$ の約数の個数を $3\\times2=6$ とする", "指数 $0$ も選べるので $(3+1)(2+1)=12$"),
                              ("$11$ を2進法で表すとき、余りを上から順に読んで $1101_{(2)}$ とする", "余りは一の位から順に出てくるので下から読み、$1011_{(2)}$"),
                              ("$ax+by=c$ の一般解を $x=x_0+ak$ とする", "$x$ には $b$ の倍数を加え、$y$ からは $a$ の倍数を引く")]),
        summary("sm1", "まとめ",
                ["約数の個数・総和は素因数分解の指数から求める。$ab=gl$。",
                 "互除法：$\\gcd(a,b)=\\gcd(b,r)$。不定方程式は特殊解＋互いに素の性質で一般解。",
                 "余りで場合分けすれば整数の性質を証明できる。$n$ 進法は $n$ の累乗の位取り。"]),
        check("ck1", "確認問題",
              [("$200$ の正の約数の個数を求めよ。", "$200=2^3\\cdot5^2$ より $4\\times3=12$ 個"),
               ("互除法で $221$ と $91$ の最大公約数を求めよ。", "$221=91\\times2+39$、$91=39\\times2+13$、$39=13\\times3$ より $13$"),
               ("$212_{(3)}$ を10進法で表せ。", "$2\\cdot9+1\\cdot3+2=23$")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

def rand_n(r, primes=(2, 3, 5, 7, 11), kmin=2, kmax=3, emax=4, lo=24, hi=3000):
    while True:
        ps = r.sample(primes, r.randint(kmin, kmax))
        f = {p: r.randint(1, emax) for p in ps}
        n = 1
        for p, e in f.items():
            n *= p ** e
        if lo <= n <= hi:
            return n, f


@gen("basic_check", 4, ["computation"])
def divisor_count(r):
    n, f = rand_n(r)
    k = ndiv(f)
    return num(f"自然数 ${n}$ の正の約数は全部で何個あるか。", str(k),
               f"${n}={fac_tex(f)}$ より、約数の個数は " + "$" + "\\times".join(f"({e}+1)" for e in f.values()) + f"={k}$ 個。", d=2,
               ap="素因数分解して、各素因数の指数を $0$ から何通り選べるかを数える（積の法則）。",
               steps=[f"${n}={fac_tex(f)}$。", "約数は $" + "\\cdot ".join(f"{p}^{{x_{i}}}" for i, p in enumerate(sorted(f), 1)) + "$ の形（各指数は $0$ 以上）。",
                      "各指数の選び方を掛けて " + "$" + "\\times".join(f"{e + 1}" for _, e in sorted(f.items())) + f"={k}$。"],
               alt=["素因数が少ない場合は、表（縦に一方の素数の累乗、横に他方の素数の累乗）をかいて約数を書き出して数えてもよい。"],
               pc=[("正しく素因数分解している", 1), ("約数の個数を正しく求めている", 1)],
               pit=["指数をそのまま掛けて $\\prod e$ とする（指数 $0$ の場合を数え忘れる）。"],
               chk=(f"len(divisors({n}))", str(k)))


@gen("basic_check", 4, ["computation", "concept"])
def gcd_lcm(r):
    while True:
        g = r.choice([2, 3, 4, 5, 6, 7, 8, 9, 12, 14, 15, 18])
        a1, b1 = r.sample(range(2, 16), 2)
        if gcd(a1, b1) == 1:
            break
    a, b = g * a1, g * b1
    ask = r.choice(["gcd", "lcm"])
    fa, fb = factorize(a), factorize(b)
    val = gcd(a, b) if ask == "gcd" else lcm(a, b)
    nm = "最大公約数" if ask == "gcd" else "最小公倍数"
    return num(f"${a}$ と ${b}$ の{nm}を求めなさい。", str(val),
               f"${a}={fac_tex(fa)}$、${b}={fac_tex(fb)}$。" + ("共通な素因数を少ない方の指数でかけて" if ask == "gcd" else "すべての素因数を多い方の指数でかけて") + f" ${val}$。", d=1,
               ap="素因数分解して指数を比べる。最大公約数は共通な素因数の「少ない方の指数」、最小公倍数は「多い方の指数」。",
               steps=[f"${a}={fac_tex(fa)}$、${b}={fac_tex(fb)}$。", f"{nm}は ${val}$。"],
               alt=[f"最大公約数 $g={gcd(a, b)}$ を求めれば、最小公倍数は $\\dfrac{{ab}}{{g}}=\\dfrac{{{a}\\times{b}}}{{{gcd(a, b)}}}={lcm(a, b)}$ でも求められる。"],
               pc=[("素因数分解が正しい", 1), (f"{nm}を正しく求めている", 1)],
               pit=["最大公約数と最小公倍数の指数の選び方（少ない方・多い方）を逆にする。"],
               chk=(f"{ask}({a},{b})", str(val)))


@gen("basic_check", 4, ["computation"])
def base_to_dec(r):
    b = r.choice([2, 2, 3, 4, 5, 6, 7])
    k = r.randint(3, 6 if b == 2 else 4)
    digits = str(r.randint(1, b - 1)) + "".join(str(r.randint(0, b - 1)) for _ in range(k - 1))
    val = int(digits, b)
    return num(f"${base_tex(digits, b)}$ を10進法で表すといくつになるか。", str(val),
               f"${base_tex(digits, b)}={base_poly_tex(digits, b)}={val}$。", d=1,
               ap=f"{b}進法では、右から順に $1,\\ {b},\\ {b}^2,\\ \\cdots$ の位になる。各位の数字と位の大きさの積を足す。",
               steps=[f"位の大きさは右から $1,\\ {b},\\ {b * b}" + (f",\\ {b ** 3}" if k > 3 else "") + ",\\ \\cdots$。", f"${base_poly_tex(digits, b)}={val}$。"],
               alt=[f"上の位から順に「{b} 倍して次の数字を足す」をくり返しても求められる（ホーナー法）。"],
               pc=[("位の大きさを正しく使っている", 1), ("正しく計算している", 1)],
               pit=["一番右の位を ${b}^1$ の位と考えてしまう。".replace("{b}", str(b))],
               chk=(base_poly(digits, b), str(val)))


@gen("basic_check", 4, ["computation"])
def dec_to_base(r):
    b = r.choice([2, 3, 4, 5, 6, 7, 8, 9])
    n = r.randint(b * b + 1, 400 if b > 2 else 120)
    digits = to_base(n, b)
    if n == 45 and b == 2:
        n, digits = 46, to_base(46, 2)
    steps, m = [], n
    while m:
        steps.append(f"${m}\\div{b}={m // b}$ 余り ${m % b}$")
        m //= b
    return sa(f"10進数の ${n}$ を {b} 進法で表しなさい。", f"${base_tex(digits, b)}$",
              f"{b} で割った余りを下の位から順に並べると ${base_tex(digits, b)}$。", d=2, v=[digits],
              ap=f"{b} で割った余りが一の位、その商をまた {b} で割った余りが次の位、…と下の位から決まる。",
              steps=steps + ["余りを下（最後）から上へ読む。"],
              alt=[f"検算：${base_poly_tex(digits, b)}={n}$ になることを確かめる。"],
              pc=[("割り算をくり返して余りを正しく求めている", 1), ("正しい順序で読んで答えている", 1)],
              pit=["余りを上から順に読み、数字の並びが逆になる。"],
              chk=(base_poly(digits, b), str(n), None, "intermediate"))


@gen("basic_check", 4, ["computation", "concept"])
def remainder(r):
    m = r.choice([5, 6, 7, 8, 9, 11, 12, 13])
    r1, r2 = r.randint(1, m - 1), r.randint(1, m - 1)
    form = r.choice(["sum", "prod", "sq", "cube"])
    if form == "sum":
        expr, val, how = "a+b", (r1 + r2) % m, f"${r1}+{r2}={r1 + r2}$"
        py = f"Mod({r1}+{r2},{m})"
    elif form == "prod":
        expr, val, how = "ab", (r1 * r2) % m, f"${r1}\\times{r2}={r1 * r2}$"
        py = f"Mod({r1}*{r2},{m})"
    elif form == "sq":
        expr, val, how = "a^2", (r1 * r1) % m, f"${r1}^2={r1 * r1}$"
        py = f"Mod({r1}**2,{m})"
    else:
        expr, val, how = "a^3", (r1 ** 3) % m, f"${r1}^3={r1 ** 3}$"
        py = f"Mod({r1}**3,{m})"
    return num(f"整数 $a$ を ${m}$ で割ると ${r1}$ 余り、整数 $b$ を ${m}$ で割ると ${r2}$ 余る。${expr}$ を ${m}$ で割った余りを求めなさい。", str(val),
               f"余りだけで計算してよい：{how}、これを ${m}$ で割った余りは ${val}$。", d=2,
               ap=f"$a={m}k+{r1}$、$b={m}l+{r2}$ とおいて計算すると、${m}$ の倍数の部分は余りに影響しない。余りどうしで計算すればよい。",
               steps=[f"$a={m}k+{r1}$、$b={m}l+{r2}$（$k,\\ l$ は整数）とおく。", f"${expr}$ を展開すると、${m}$ の倍数＋（余りどうしの計算）の形になる。", f"{how}、${m}$ で割った余りは ${val}$。"],
               alt=[f"具体的な数で確かめる：$a={r1}$、$b={r2}$（または $a={m + r1}$ など）として ${expr}$ を計算し、${m}$ で割る。"],
               pc=[("余りどうしで計算してよい理由を理解している", 1), ("余りを正しく求めている", 1)],
               pit=[f"余りどうしの計算結果が ${m}$ 以上になっても、もう一度 ${m}$ で割るのを忘れる。"],
               chk=(py, str(val)))


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 5, ["computation"])
def euclid(r):
    while True:
        g = r.choice([7, 11, 13, 17, 19, 23, 29, 31, 37])
        m, n = r.randint(8, 40), r.randint(5, 35)
        if gcd(m, n) == 1 and m > n and 100 <= g * n and g * m < 1500:
            break
    a, b = g * m, g * n
    lines, gg = euclid_steps(a, b)
    if (a, b) in ((391, 299), (437, 323)):
        a, b = a + 2 * g, b
        lines, gg = euclid_steps(a, b)
    return num(f"互除法を用いて、${a}$ と ${b}$ の最大公約数を求めなさい。途中の割り算の式も書きなさい。", str(gg),
               "互除法：" + "、".join(lines) + f"。余りが $0$ になったときの割る数 ${gg}$ が最大公約数。", d=3,
               ap="2数がともに大きく素因数分解しにくいときは、互除法 $\\gcd(a,b)=\\gcd(b,r)$ をくり返す。",
               steps=lines + [f"最大公約数は ${gg}$。"],
               alt=[f"求めた ${gg}$ で両方を割ると ${a // gg}$、${b // gg}$ となり、これらが互いに素であることを確かめる。"],
               pc=[("互除法の割り算を正しく続けている", 2), ("最大公約数を正しく答えている", 2)],
               pit=["最後の余り $0$ の1つ前の「余り」ではなく、割られる数を答えてしまう。", "商と余りを取り違えて次の割り算に進む。"],
               chk=(f"gcd({a},{b})", str(gg)))


@gen("standard_practice", 5, ["computation", "condition_check"])
def diophantine(r):
    while True:
        a, b = r.randint(3, 19), r.randint(2, 15)
        if gcd(a, b) == 1 and a != b and a > 2 and b > 2:
            break
    minus = r.random() < 0.35
    c = r.randint(1, 9) if r.random() < 0.6 else 1
    if (a, b, c, minus) == (3, 5, 1, False):
        c = 2
    x0, y0 = dioph(a, b, c, minus)
    op = "-" if minus else "+"
    ya = f"{a}k" if minus else f"-{a}k"
    yexpr = sgn_term(y0, ya)
    ans = f"$x={sgn_term(x0, f'{b}k')},\\ y={yexpr}$（$k$ は整数）"
    return sa(f"方程式 ${a}x{op}{b}y={c}$ を満たす整数 $x$、$y$ の組をすべて求めなさい。", ans,
              f"1組の解 $(x,\\,y)=({x0},\\,{y0})$ を見つけ、差をとって ${a}(x-{x0})={'' if minus else '-'}{b}(y{'-' if y0 >= 0 else '+'}{abs(y0)})$。${a}$ と ${b}$ は互いに素。", d=3,
              v=[f"x={sgn_term(x0, f'{b}k')}, y={yexpr}"],
              ap="まず1組の整数解（特殊解）を見つけ、もとの式との差をとる。係数が互いに素であることを使って一般解を決める。",
              steps=[f"$x={x0}$ のとき $y={y0}$ となり、$(x,\\,y)=({x0},\\,{y0})$ は1つの解。",
                     f"${a}x{op}{b}y={c}$ と ${a}\\cdot{x0}{op}{b}\\cdot({y0})={c}$ の差をとる：${a}(x-{x0}){op}{b}(y-({y0}))=0$。",
                     f"${a}$ と ${b}$ は互いに素なので、$x-{x0}$ は ${b}$ の倍数：$x-{x0}={b}k$。",
                     f"代入して $y={yexpr}$。"],
              alt=["互除法を逆にたどって特殊解を求める方法もある。特殊解の選び方によって答えの見た目は変わるが、$k$ をずらせば同じ解の集合になる。"],
              pc=[("特殊解を正しく見つけている", 1), ("互いに素であることを使って一般解を導いている", 2), ("一般解を正しく答えている", 1)],
              pit=["$x$ に $a$ の倍数、$y$ に $b$ の倍数をつけてしまう（係数の入れかえ）。", "「$k$ は整数」を書き忘れる。"],
              chk=(f"expand({a}*({b}*k+({x0})){op}{b}*({ya.replace('k', '*k')}+({y0})))", str(c), "expand", "intermediate"))


@gen("standard_practice", 3, ["computation"])
def divisor_sum(r):
    n, f = rand_n(r, primes=(2, 3, 5, 7), kmin=2, kmax=2, emax=3, lo=12, hi=800)
    s = sdiv(f)
    factors = "".join("(" + "+".join(["1"] + [f"{p}" if e == 1 else f"{p}^{{{e}}}" for e in range(1, f[p] + 1)]) + ")" for p in sorted(f))
    return num(f"${n}$ の正の約数の総和を求めなさい。", str(s),
               f"${n}={fac_tex(f)}$ より、総和は ${factors}={s}$。", d=3,
               ap="約数の総和は、各素因数について $1+p+\\cdots+p^a$ をつくって掛け合わせる。展開するとすべての約数が1回ずつ現れる。",
               steps=[f"${n}={fac_tex(f)}$。", f"総和 $={factors}$。", "各かっこを計算して " + "$" + "\\times".join(f"{(p ** (e + 1) - 1) // (p - 1)}" for p, e in sorted(f.items())) + f"={s}$。"],
               alt=[f"約数を書き出して足しても確かめられる（全部で ${ndiv(f)}$ 個）。"],
               pc=[("素因数分解が正しい", 1), ("総和の式を正しく立てている", 2), ("正しく計算している", 1)],
               pit=["かっこの中の $1$（$p^0$）を書き忘れる。", "各かっこを掛けずに足してしまう。"],
               chk=(f"sum(divisors({n}))", str(s)))


@gen("standard_practice", 3, ["computation", "concept"])
def base_fraction(r):
    b = r.choice([2, 3, 4, 5])
    k = r.randint(2, 3)
    ds = "".join(str(r.randint(0, b - 1)) for _ in range(k - 1)) + str(r.randint(1, b - 1))
    v = sum(Fraction(int(d), b ** (i + 1)) for i, d in enumerate(ds))
    terms = "+".join(f"\\dfrac{{{d}}}{{{b ** (i + 1)}}}" for i, d in enumerate(ds))
    tex = f"\\dfrac{{{v.numerator}}}{{{v.denominator}}}"
    return num(f"${b}$ 進法で表された小数 $0.{ds}_{{({b})}}$ を10進法の分数で表しなさい。", f"{v.numerator}/{v.denominator}",
               f"$0.{ds}_{{({b})}}={terms}={tex}$。", d=3, disp=f"${tex}$",
               ap=f"小数点以下の位は、左から $\\dfrac{{1}}{{{b}}},\\ \\dfrac{{1}}{{{b}^2}},\\ \\cdots$ の位になる。",
               steps=[f"小数第1位は $\\dfrac{{1}}{{{b}}}$ の位、第2位は $\\dfrac{{1}}{{{b * b}}}$ の位" + (f"、第3位は $\\dfrac{{1}}{{{b ** 3}}}$ の位。" if k == 3 else "。"),
                      f"$0.{ds}_{{({b})}}={terms}$。", f"通分して ${tex}$。"],
              alt=[f"$0.{ds}_{{({b})}}$ を ${b}^{k}={b ** k}$ 倍すると整数 ${ds}_{{({b})}}={int(ds, b)}$ になるので、$\\dfrac{{{int(ds, b)}}}{{{b ** k}}}$ を約分してもよい。"],
               pc=[("小数の位の大きさを正しく使っている", 2), ("既約分数で答えている", 2)],
               pit=["小数第1位を $\\dfrac{1}{10}$ の位と考えてしまう。"],
               chk=(f"Rational({int(ds, b)},{b ** k})", f"{v.numerator}/{v.denominator}"))


@gen("standard_practice", 4, ["application", "computation"])
def tile_problem(r):
    form = r.choice(["lcm_side", "lcm_count", "gcd_side", "gcd_count"])
    if form.startswith("lcm"):
        while True:
            a, b = r.sample(range(4, 31), 2)
            if gcd(a, b) > 1 and lcm(a, b) <= 240 and a % b and b % a:
                break
        L = lcm(a, b)
        cnt = (L // a) * (L // b)
        if form == "lcm_side":
            stem, val = f"縦 ${a}$ cm、横 ${b}$ cm の長方形のタイルを、すべて同じ向きにすき間なく並べて正方形をつくる。できる正方形のうち最も小さいものの1辺の長さを求めなさい。", L
        else:
            stem, val = f"縦 ${a}$ cm、横 ${b}$ cm の長方形の板を同じ向きにすき間なく並べて、できるだけ小さい正方形をつくる。必要な板の枚数を求めなさい。", cnt
        e = f"正方形の1辺は ${a}$ と ${b}$ の公倍数で、最小のものは最小公倍数 ${L}$。枚数は $\\dfrac{{{L}}}{{{a}}}\\times\\dfrac{{{L}}}{{{b}}}={cnt}$。"
        steps = [f"1辺の長さは ${a}$ の倍数かつ ${b}$ の倍数。", f"最小公倍数は ${L}$ cm。"] + ([f"縦に ${L // a}$ 枚、横に ${L // b}$ 枚で ${cnt}$ 枚。"] if form == "lcm_count" else [])
        ap = "正方形の1辺は、縦の長さの倍数でも横の長さの倍数でもある。最も小さい正方形は最小公倍数。"
        py = f"lcm({a},{b})" if form == "lcm_side" else f"(lcm({a},{b})/{a})*(lcm({a},{b})/{b})"
    else:
        while True:
            W, H = r.sample(range(24, 241, 6), 2)
            if W % H and H % W and (W // gcd(W, H)) * (H // gcd(W, H)) <= 200:
                break
        g = gcd(W, H)
        cnt = (W // g) * (H // g)
        if form == "gcd_side":
            stem, val = f"縦 ${W}$ cm、横 ${H}$ cm の長方形の床に、同じ大きさの正方形のタイルをすき間なく敷きつめる。使えるタイルのうち最も大きいものの1辺の長さを求めなさい。", g
        else:
            stem, val = f"縦 ${W}$ cm、横 ${H}$ cm の長方形の紙を、余りが出ないようにできるだけ大きな同じ大きさの正方形に切り分ける。正方形は何枚できるか。", cnt
        e = f"正方形の1辺は ${W}$ と ${H}$ の公約数で、最大のものは最大公約数 ${g}$。枚数は $\\dfrac{{{W}}}{{{g}}}\\times\\dfrac{{{H}}}{{{g}}}={cnt}$。"
        steps = [f"1辺の長さは ${W}$ の約数かつ ${H}$ の約数。", f"最大公約数は ${g}$ cm。"] + ([f"縦に ${W // g}$ 枚、横に ${H // g}$ 枚で ${cnt}$ 枚。"] if form == "gcd_count" else [])
        ap = "正方形の1辺は、縦の長さも横の長さも割り切る。最も大きい正方形は最大公約数。"
        py = f"gcd({W},{H})" if form == "gcd_side" else f"({W}/gcd({W},{H}))*({H}/gcd({W},{H}))"
    return num(stem, str(val), e, d=3, ap=ap, steps=steps,
               alt=["求めた長さが条件を満たすか（縦・横ともに割り切れる／割り切る）を割り算で確かめ、それより小さい（大きい）候補がないことも確認する。"],
               pc=[("公倍数・公約数のどちらを使うかを正しく判断している", 2), ("正しい値を求めている", 2)],
               pit=["最大公約数と最小公倍数を取り違える。", "枚数を求めるとき、面積の比ではなく1方向の枚数だけを答える。"],
               chk=(py, str(val)))


# ======================================================================
# C 思考力・記述応用
# ======================================================================

PROOFS = [
    ("整数 $n$ について、$n^2$ を $4$ で割った余りは $0$ または $1$ であることを証明しなさい。", "$n$ を偶数 $2k$ と奇数 $2k+1$ に分ける。",
     ["$n=2k$ のとき $n^2=4k^2$ で余り $0$。", "$n=2k+1$ のとき $n^2=4(k^2+k)+1$ で余り $1$。", "よって余りは $0$ または $1$。"],
     "[Mod(0**2,4), Mod(1**2,4), Mod(2**2,4), Mod(3**2,4)]", "[0, 1, 0, 1]"),
    ("奇数の2乗を $8$ で割った余りは $1$ であることを証明しなさい。", "奇数を $2k+1$ とおき、$k(k+1)$ が連続2整数の積で偶数であることを使う。",
     ["奇数を $2k+1$（$k$ は整数）とおくと $(2k+1)^2=4k(k+1)+1$。", "$k(k+1)$ は連続する2つの整数の積なので偶数で、$k(k+1)=2m$ とおける。", "$(2k+1)^2=8m+1$ より、余りは $1$。"],
     "[Mod(1**2,8), Mod(3**2,8), Mod(5**2,8), Mod(7**2,8)]", "[1, 1, 1, 1]"),
    ("連続する3つの整数の積 $n(n+1)(n+2)$ は $6$ の倍数であることを証明しなさい。", "2 の倍数かつ 3 の倍数であることを示す。",
     ["連続する2つの整数のうち1つは偶数なので、積は $2$ の倍数。", "$n$ を $3$ で割った余りで分けると、$n,\\ n+1,\\ n+2$ のいずれかが $3$ の倍数になるので、積は $3$ の倍数。",
      "$2$ と $3$ は互いに素なので、積は $6$ の倍数。"],
     "[Mod(0*1*2,6), Mod(1*2*3,6), Mod(2*3*4,6), Mod(3*4*5,6), Mod(4*5*6,6), Mod(5*6*7,6)]", "[0, 0, 0, 0, 0, 0]"),
    ("整数 $n$ について、$n^2+1$ は $3$ の倍数でないことを証明しなさい。", "$n$ を $3$ で割った余りで3つの場合に分ける。",
     ["$n=3k$ のとき $n^2+1=3\\cdot3k^2+1$ で余り $1$。", "$n=3k\\pm1$ のとき $n^2+1=3(3k^2\\pm2k)+2$ で余り $2$。", "いずれの場合も余りは $0$ でないので、$3$ の倍数でない。"],
     "[Mod(0**2+1,3), Mod(1**2+1,3), Mod(2**2+1,3)]", "[1, 2, 2]"),
    ("整数 $n$ について、$n^5-n$ は $5$ の倍数であることを証明しなさい。", "$n^5-n=n(n-1)(n+1)(n^2+1)$ と因数分解し、$n$ を $5$ で割った余りで分ける。",
     ["$n^5-n=n(n-1)(n+1)(n^2+1)$。", "$n=5k,\\ 5k+1,\\ 5k-1$ のとき、それぞれ $n,\\ n-1,\\ n+1$ が $5$ の倍数。",
      "$n=5k\\pm2$ のとき $n^2+1=25k^2\\pm20k+5=5(5k^2\\pm4k+1)$ で $5$ の倍数。", "いずれの場合も $5$ の倍数である。"],
     "[Mod(0**5-0,5), Mod(1**5-1,5), Mod(2**5-2,5), Mod(3**5-3,5), Mod(4**5-4,5)]", "[0, 0, 0, 0, 0]"),
    ("整数 $n$ について、$n(n+1)(2n+1)$ は $6$ の倍数であることを証明しなさい。", "$2$ の倍数であることと、$n$ を $3$ で割った余りで分けて $3$ の倍数であることを示す。",
     ["$n(n+1)$ は連続2整数の積なので偶数。", "$n=3k$ なら $n$、$n=3k+2$ なら $n+1$、$n=3k+1$ なら $2n+1=6k+3$ が $3$ の倍数。", "$2$ と $3$ は互いに素なので $6$ の倍数。"],
     "[Mod(0*1*1,6), Mod(1*2*3,6), Mod(2*3*5,6), Mod(3*4*7,6), Mod(4*5*9,6), Mod(5*6*11,6)]", "[0, 0, 0, 0, 0, 0]"),
    ("整数 $a$、$b$ について、$a^2+b^2$ が $3$ の倍数ならば、$a$、$b$ はともに $3$ の倍数であることを証明しなさい。", "対偶「$a$、$b$ の少なくとも一方が $3$ の倍数でなければ、$a^2+b^2$ は $3$ の倍数でない」を示す。",
     ["平方数を $3$ で割った余りは $0$（もとの数が $3$ の倍数）か $1$（そうでない）。", "$a$、$b$ の少なくとも一方が $3$ の倍数でないとき、$a^2+b^2$ を $3$ で割った余りは $0+1=1$ または $1+1=2$。",
      "よって $3$ の倍数でない。対偶が真なので、もとの命題も真。"],
     "[Mod(0**2,3), Mod(1**2,3), Mod(2**2,3)]", "[0, 1, 1]"),
]


@gen("thinking_writing", 3, ["written_reasoning", "condition_check"])
def proof_mod(r):
    stem, ap, steps, expr, exp = r.choice(PROOFS)
    return desc(stem, "（証明）" + "".join(steps) + "（証明終）", ap + "場合分けが、すべての整数をもれなく覆っていることを明記する。",
                [("適切な場合分け（または文字のおき方）をしている", 2), ("各場合の計算が正しい", 4), ("結論を正しく述べている", 2)], d=4, p=8, lines=10, kind="proof",
                ap=ap, steps=steps,
                alt=["余りだけに注目した計算（合同式の考え方）で各場合を確認すると、文字式の展開を短くできる。", "小さい $n$ で具体的に計算して、主張が正しそうか確かめてから証明を書く。"],
                pc=[("場合分け・文字のおき方", 2), ("各場合の計算", 4), ("結論", 2)],
                pit=["いくつかの具体例で成り立つことを確かめただけで「証明」としてしまう。", "場合分けにもれがある（例：$3$ で割った余りが $2$ の場合を忘れる）。"],
                chk=(expr, exp, None, "intermediate"))


@gen("thinking_writing", 3, ["application", "written_reasoning", "condition_check"])
def dioph_app(r):
    while True:
        unit = r.choice([10, 20, 30, 50])
        a, b = r.sample(range(3, 13), 2)
        if gcd(a, b) != 1:
            continue
        x, y = r.randint(1, 8), r.randint(1, 8)
        c = a * x + b * y
        sols = [(i, (c - a * i) // b) for i in range(1, c // a + 1) if (c - a * i) % b == 0 and (c - a * i) // b >= 1]
        if 2 <= len(sols) <= 5:
            break
    A, B, C = a * unit, b * unit, c * unit
    ans = "、".join(f"({i},\\,{j})" for i, j in sols)
    return desc(f"1個 ${A}$ 円の品物 P と1個 ${B}$ 円の品物 Q を、どちらも少なくとも1個は買い、代金の合計をちょうど ${C}$ 円にしたい。P と Q の個数の組 $(x,\\,y)$ をすべて求めなさい。考え方も書きなさい。",
                f"$(x,\\,y)={ans}$",
                f"${A}x+{B}y={C}$ の両辺を ${unit}$ で割って ${a}x+{b}y={c}$。一般解を求め、$x\\geqq1$、$y\\geqq1$ を満たす $k$ を調べる。",
                [("方程式を立てて簡単にしている", 2), ("一般解（または候補の絞り込み）を正しく求めている", 3), ("正の整数の条件から $k$ の範囲を決めている", 2), ("すべての組を答えている", 1)],
                d=4, p=8, lines=10,
                ap="個数は正の整数なので、一次不定方程式の一般解を求めたあと、$x\\geqq1$、$y\\geqq1$ から整数 $k$ の範囲をしぼる。",
                steps=[f"${A}x+{B}y={C}$ より ${a}x+{b}y={c}$。", f"1組の解 $(x,\\,y)=({sols[0][0]},\\,{sols[0][1]})$。${a}$ と ${b}$ は互いに素なので、一般解は $x={b}k+{sols[0][0]},\\ y=-{a}k+{sols[0][1]}$。",
                       f"$x\\geqq1,\\ y\\geqq1$ より $0\\leqq k\\leqq{len(sols) - 1}$。", f"$(x,\\,y)={ans}$。"],
                alt=[f"$y=\\dfrac{{{c}-{a}x}}{{{b}}}$ が正の整数になる $x$ を、$x=1,\\ 2,\\ \\cdots$ と順に調べてもよい（${b}$ ごとに解が現れる）。"],
                pc=[("方程式", 2), ("一般解", 3), ("$k$ の範囲", 2), ("答え", 1)],
                pit=["「少なくとも1個」の条件を忘れて $x=0$ や $y=0$ の組を含める。", "両辺を割らずに大きな係数のまま計算して誤る。"],
                chk=("[" + ", ".join(f"{a}*{i}+{b}*{j}" for i, j in sols) + "]", "[" + ", ".join(str(c) for _ in sols) + "]", None, "intermediate"))


@gen("thinking_writing", 2, ["cross_unit", "computation", "written_reasoning"], rel=["HS-MATHA-U01"])
def divisor_multiple(r):
    while True:
        f = {2: r.randint(1, 4), 3: r.randint(1, 3), 5: r.randint(0, 2)}
        f = {p: e for p, e in f.items() if e}
        N = 1
        for p, e in f.items():
            N *= p ** e
        k = r.choice([2, 3, 4, 6, 9, 10, 12, 15])
        if N % k == 0 and N != k and 60 <= N <= 2000:
            break
    M = N // k
    fM = factorize(M) if M > 1 else {}
    cnt = ndiv(fM) if fM else 1
    tot = k * (sdiv(fM) if fM else 1)
    return sa(f"${N}$ の正の約数のうち、${k}$ の倍数であるものの個数と、それらの総和を求めなさい。考え方も書きなさい。",
              f"個数 ${cnt}$ 個、総和 ${tot}$",
              f"${k}$ の倍数である約数は ${k}m$（$m$ は ${N}\\div{k}={M}$ の正の約数）の形。", d=4, p=8, v=[f"{cnt}, {tot}"],
              ap="「$N$ の約数で $k$ の倍数」は、$km$（$m$ は $N/k$ の約数）と1対1に対応する。約数の個数・総和の公式（積の法則による数え上げ）を $N/k$ に使う。",
              steps=[f"${N}={fac_tex(factorize(N))}$。${k}$ の倍数である約数を $d={k}m$ とおくと、$m$ は ${M}$ の正の約数。",
                     (f"${M}={fac_tex(fM)}$ の正の約数は ${cnt}$ 個。" if fM else "$m=1$ のみで1個。"),
                     f"総和は ${k}\\times({M}\\ \\text{{の約数の総和}})={k}\\times{tot // k}={tot}$。"],
              alt=["素因数の指数の選び方で直接数える：" + "、".join(f"${p}$ の指数は ${factorize(k).get(p, 0)}$ 以上 ${e}$ 以下" for p, e in sorted(factorize(N).items())) + " で、積の法則を使う。"],
              pc=[(f"${k}m$ の形に対応させる（または指数の範囲を正しく設定する）", 3), ("個数を正しく求めている", 2), ("総和を正しく求めている", 3)],
              pit=["$k$ の倍数の条件を指数の範囲に反映させず、すべての約数を数える。", "総和で $k$ 倍し忘れる。"],
              chk=(f"[len(divisors({M})), {k}*sum(divisors({M}))]", f"[{cnt}, {tot}]", None, "intermediate"))


@gen("thinking_writing", 2, ["written_reasoning", "condition_check"])
def gcd_lcm_pairs(r):
    while True:
        G = r.choice([2, 3, 4, 5, 6, 7, 8, 9, 12, 15])
        Q = r.choice([6, 10, 14, 15, 21, 30, 12, 18, 20, 28, 36, 60, 42, 24, 40])
        pairs = [(i, Q // i) for i in range(1, Q + 1) if Q % i == 0 and i < Q // i and gcd(i, Q // i) == 1]
        if len(pairs) >= 2:
            break
    L = G * Q
    ans = "、".join(f"({G * i},\\,{G * j})" for i, j in pairs)
    return desc(f"最大公約数が ${G}$、最小公倍数が ${L}$ である2つの自然数 $a$、$b$（$a<b$）の組をすべて求めなさい。考え方も書きなさい。",
                f"$(a,\\,b)={ans}$",
                f"$a={G}a'$、$b={G}b'$（$a'$ と $b'$ は互いに素、$a'<b'$）とおくと、最小公倍数は ${G}a'b'={L}$ より $a'b'={Q}$。",
                [("$a=ga'$、$b=gb'$（互いに素）とおいている", 2), ("$a'b'$ の値を正しく求めている", 2), ("互いに素の条件で組を正しくしぼっている", 3), ("答えが正しい", 1)],
                d=4, p=8, lines=8,
                ap="最大公約数 $g$ でくくると、残りの $a'$、$b'$ は互いに素。最小公倍数は $ga'b'$ になるので、$a'b'$ の値が決まる。互いに素という条件を忘れない。",
                steps=[f"$a={G}a'$、$b={G}b'$（$a'<b'$、互いに素）とおく。", f"最小公倍数 ${G}a'b'={L}$ より $a'b'={Q}$。",
                       f"積が ${Q}$ になる互いに素な組は $(a',\\,b')=" + "、".join(f"({i},\\,{j})" for i, j in pairs) + "$。", f"$(a,\\,b)={ans}$。"],
                alt=[f"求めた各組について、実際に最大公約数と最小公倍数を計算して ${G}$、${L}$ になることを確かめる。"],
                pc=[("おき方", 2), ("$a'b'$ の値", 2), ("互いに素での絞り込み", 3), ("答え", 1)],
                pit=[f"積が ${Q}$ になる組をすべて答え、互いに素でない組（最大公約数が ${G}$ より大きくなる組）を含めてしまう。"],
                chk=("[" + ", ".join(f"gcd({G * i},{G * j}), lcm({G * i},{G * j})" for i, j in pairs) + "]", "[" + ", ".join(f"{G}, {L}" for _ in pairs) + "]", None, "intermediate"))


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(stem, wrong, step, etype, tempt, fix, ans, expl, steps, ap, alt, pit, chk=None, d=3):
    return desc(f"{stem}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい答えを求めなさい。", ans, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい解答を途中式とともに示している", 3), ("最終的な答えが正しい", 1)], d=d, p=6, lines=6,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい途中式", 3), ("正しい答え", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix), chk=chk)


@gen("error_correction", 3, ["common_error", "computation"])
def err_divcount(r):
    while True:
        n, f = rand_n(r, kmin=2, kmax=3, emax=4)
        wrong_v = 1
        for e in f.values():
            wrong_v *= e
        if wrong_v != ndiv(f) and max(f.values()) >= 2:
            break
    k = ndiv(f)
    wrong = f"${n}={fac_tex(f)}$ だから、約数の個数は指数を掛けて " + "$" + "\\times".join(f"{e}" for _, e in sorted(f.items())) + f"={wrong_v}$ 個"
    fix = f"指数 $0$ の場合も含めて、" + "$" + "\\times".join(f"({e}+1)" for _, e in sorted(f.items())) + f"={k}$ 個"
    return err_item(f"${n}$ の正の約数の個数を求めなさい。", wrong, "個数の公式（指数をそのまま掛けた部分）", "formula",
                    "素因数分解の指数がそのまま目に入るので、「指数を掛ける」と覚え違えやすい。指数 $0$（その素因数を含まない約数）の存在を意識していない。",
                    fix, f"${k}$ 個", f"約数は各素因数の指数を $0$ から選ぶので、選び方は（指数＋1）通り。",
                    [f"${n}={fac_tex(f)}$。", "各素因数の指数は $0$ から最大の指数まで選べる。", "$" + "\\times".join(f"({e}+1)" for _, e in sorted(f.items())) + f"={k}$。"],
                    "約数 $1$ はどの素因数も含まない（指数がすべて $0$）。$1$ を数えられているかで公式の正しさを確かめられる。",
                    ["小さい数（例：$12=2^2\\cdot3$ の約数 $1,2,3,4,6,12$ の6個）で公式を確かめる。"],
                    ["指数 $0$ を数えない。"],
                    chk=(f"len(divisors({n}))", str(k), None, "intermediate"), d=2)


@gen("error_correction", 3, ["common_error", "condition_check"])
def err_dioph(r):
    while True:
        a, b = r.randint(3, 13), r.randint(3, 13)
        if gcd(a, b) == 1 and a != b:
            break
    c = r.randint(1, 6)
    x0, y0 = dioph(a, b, c)
    wrong = f"$(x,\\,y)=({x0},\\,{y0})$ が1つの解なので、一般解は $x={sgn_term(x0, f'{a}k')},\\ y={sgn_term(y0, f'-{b}k')}$（$k$ は整数）"
    fix = f"$x={sgn_term(x0, f'{b}k')},\\ y={sgn_term(y0, f'-{a}k')}$（$k$ は整数）"
    return err_item(f"方程式 ${a}x+{b}y={c}$ の整数解をすべて求めなさい。", wrong, "一般解の係数（$x$ と $y$ に付ける倍数の入れかえ）", "formula",
                    "「$x$ には $x$ の係数」と思いこみやすい。一般解を導く過程（差をとって互いに素を使う）を省いて形だけ覚えている。",
                    fix, fix, f"${a}(x-{x0})=-{b}(y-({y0}))$ で、${a}$ と ${b}$ は互いに素なので $x-{x0}$ は ${b}$ の倍数。",
                    [f"差をとって ${a}(x-{x0})=-{b}(y-({y0}))$。", f"${a}$ と ${b}$ は互いに素なので $x-{x0}={b}k$。", f"代入して $y={sgn_term(y0, f'-{a}k')}$。"],
                    "一般解は、もとの方程式に代入して $k$ が消えるかどうかで検算できる。",
                    [f"生徒の解を代入すると ${a}({a}k+{x0})+{b}(-{b}k+{y0})={c}+({a * a - b * b})k$ となり、$k\\neq0$ で ${c}$ にならない。"],
                    ["一般解を代入して確かめない。"],
                    chk=(f"expand({a}*({b}*k+({x0}))+{b}*(-{a}*k+({y0})))", str(c), "expand", "intermediate"))


@gen("error_correction", 2, ["common_error", "computation"])
def err_base(r):
    while True:
        b = r.choice([2, 3, 5, 6, 7])
        n = r.randint(b * b + 1, 200)
        digits = to_base(n, b)
        if digits != digits[::-1] and digits[-1] != "0":
            break
    wrong = f"${n}$ を ${b}$ で割っていき、余りを上から順に並べて ${base_tex(digits[::-1], b)}$"
    fix = f"余りは下の位から順に出てくるので、下から読んで ${base_tex(digits, b)}$"
    return err_item(f"10進数の ${n}$ を ${b}$ 進法で表しなさい。", wrong, "余りを読む順序", "concept",
                    "割り算を上から書いていくので、書いた順にそのまま読んでしまう。最初に出る余りが一の位であることを意識していない。",
                    fix, f"${base_tex(digits, b)}$", f"最初の余りは ${n}$ を ${b}$ で割った余りで、一の位の数字である。",
                    [f"{b} で割り続けて余りを求める。", "最初の余りが一の位、最後の余りが最上位。", f"下から読んで ${base_tex(digits, b)}$。"],
                    "得られた数を10進法にもどして、もとの数になるか確かめる。",
                    [f"生徒の答えを10進法にもどすと ${int(digits[::-1], b)}$ となり、${n}$ にならない。"],
                    ["余りを読む順序を逆にする。"],
                    chk=(base_poly(digits, b), str(n), None, "intermediate"), d=2)


@gen("error_correction", 2, ["common_error", "condition_check"])
def err_coprime(r):
    G = r.choice([2, 3, 4, 5, 6, 7, 8])
    Q = r.choice([12, 18, 20, 24, 28, 40, 45, 50, 72])
    allp = [(i, Q // i) for i in range(1, Q + 1) if Q % i == 0 and i < Q // i]
    good = [p for p in allp if gcd(*p) == 1]
    L = G * Q
    wrong = f"$a={G}a'$、$b={G}b'$ とおくと $a'b'={Q}$ なので、$(a,\\,b)=" + "、".join(f"({G * i},\\,{G * j})" for i, j in allp) + "$"
    ans = "$(a,\\,b)=" + "、".join(f"({G * i},\\,{G * j})" for i, j in good) + "$"
    bad = [p for p in allp if gcd(*p) != 1]
    return err_item(f"最大公約数が ${G}$、最小公倍数が ${L}$ である2つの自然数 $a$、$b$（$a<b$）の組をすべて求めなさい。", wrong,
                    "$a'$、$b'$ の組の選び方（互いに素の条件の確認もれ）", "condition",
                    "$a'b'$ の値を求めたところで安心し、$a'$ と $b'$ が互いに素でなければならない理由（最大公約数が $g$ であること）を忘れている。",
                    ans + "（" + "、".join(f"$({G * i},\\,{G * j})$" for i, j in bad) + " は最大公約数が " + "、".join(f"${G * gcd(i, j)}$" for i, j in bad) + " となり不適）", ans,
                    f"$a'$ と $b'$ が互いに素でないと、最大公約数が ${G}$ より大きくなる。",
                    [f"$a={G}a'$、$b={G}b'$（$a'$、$b'$ は互いに素）。", f"$a'b'={Q}$。", "互いに素な組だけを残す。", ans + "。"],
                    "答えの各組について、最大公約数・最小公倍数を実際に計算して確かめる。",
                    [f"例えば $({G * bad[0][0]},\\,{G * bad[0][1]})$ の最大公約数は ${G * gcd(*bad[0])}$ で、条件の ${G}$ と合わない。"],
                    ["「互いに素」の条件を使わない。"],
                    chk=("[" + ", ".join(f"gcd({G * i},{G * j})" for i, j in good) + "]", "[" + ", ".join(str(G) for _ in good) + "]", None, "intermediate"))


GENERATORS = [divisor_count, gcd_lcm, base_to_dec, dec_to_base, remainder,
              euclid, diophantine, divisor_sum, base_fraction, tile_problem,
              proof_mod, dioph_app, divisor_multiple, gcd_lcm_pairs,
              err_divcount, err_dioph, err_base, err_coprime]
