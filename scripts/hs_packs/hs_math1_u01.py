"""単元パック：数学Ⅰ 数と式（展開と因数分解・実数・一次不等式・絶対値）。"""
from fractions import Fraction
from math import gcd, isqrt

from banks._common import desc, mc, num, sa
from hs_pack_lib import (board, check, definition, derivation, example, frac, fr_py, gen, guide, intro, lesson, nonzero,
                         poly, summary, theorem, tp)

UNIT_ID = "HS-MATH1-U01"

NONSQ = [2, 3, 5, 6, 7, 10, 11, 13, 14, 15]


def terms(pairs):
    """[(係数, 単項式の LaTeX), ...] → '3x^2-2xy+y^2-5'（係数 0・±1 を整形）。"""
    out = []
    for c, m in pairs:
        if c == 0:
            continue
        mag = abs(c)
        coef = "" if (mag == 1 and m) else str(mag)
        sign = "-" if c < 0 else ("+" if out else "")
        out.append(sign + coef + m)
    return "".join(out) or "0"


_PY = {"x^3": "x**3", "x^2": "x**2", "xy": "x*y", "y^2": "y**2", "y^3": "y**3", "x^2y": "x**2*y", "xy^2": "x*y**2",
       "x": "x", "y": "y", "": "1", "x^4": "x**4"}


def pyterms(pairs):
    return "+".join(f"({c})*{_PY[m]}" for c, m in pairs) or "0"


def root(n):
    return "1" if n == 1 else f"\\sqrt{{{n}}}"


def cst(k):
    return "" if k == 0 else (f"+{k}" if k > 0 else f"{k}")


FLIP = {"<": ">", ">": "<", "\\leqq ": "\\geqq ", "\\geqq ": "\\leqq "}
RELPY = {"<": "<", ">": ">", "\\leqq ": "<=", "\\geqq ": ">="}


LESSON = lesson(
    goals=["3次の乗法公式・因数分解の公式を導き、たすき掛けや「1つの文字について整理する」方法で因数分解できる。",
           "実数の分類と絶対値の意味を理解し、$\\sqrt{a^2}=|a|$ や分母の有理化を根拠とともに使える。",
           "不等式の性質（負の数をかけると向きが変わる）を説明し、一次不等式・連立不等式・絶対値を含む方程式や不等式を解ける。"],
    duration=100,
    readiness=["中学で学んだ乗法公式 $(a+b)^2,\\ (a+b)(a-b)$ と因数分解を使える。", "平方根の計算（$\\sqrt{12}=2\\sqrt{3}$ など）と、分母の有理化 $\\dfrac{1}{\\sqrt{2}}=\\dfrac{\\sqrt{2}}{2}$ ができる。",
               "一次方程式を移項して解ける。"],
    flow=[("導入：式を「かたまり」で見る", 10, "$(x+y+1)^2$ を置きかえで展開し、式の構造を見る視点を共有する"),
          ("展開と因数分解", 25, "3次の公式を展開で確かめ、たすき掛け（例題1）と2文字の式の因数分解を扱う"),
          ("実数と根号", 20, "数の分類、$\\sqrt{a^2}=|a|$、分母の有理化（例題2）"),
          ("一次不等式", 20, "不等式の性質を確認し、一次不等式・連立不等式を数直線で解く"),
          ("絶対値を含む方程式・不等式", 20, "絶対値＝距離の見方と、場合分けによる解法（例題3）"),
          ("まとめと確認", 5, "確認問題3問、問題プリントA の課題指示")],
    sections=[
        intro("in1", "式を「かたまり」で見る",
              "$(x+y+1)^2$ を分配法則だけで展開すると項が9つ現れ、計算ミスが起こりやすい。$x+y=A$ とおけば $(A+1)^2=A^2+2A+1$ となり、中学で学んだ公式がそのまま使える。数と式の単元では、式の形を観察して「どの公式が使える形か」を見抜く力を育てる。",
              bullets=["展開と因数分解は互いに逆の操作であり、因数分解の答えは展開すれば必ず確かめられる。", "根号を含む数や絶対値も「式の値」として同じように扱う。そのとき、数の正負が重要な役割を果たす。"],
              points=[tp("最初に $(x+y+1)^2$ を各自で展開させ、置きかえを使った生徒と使わなかった生徒の計算量を比べる。", ask="この式のどこに注目すれば、中学の公式が使えるか。", expect="$x+y$ をひとまとまりと見る。", timing="導入の冒頭"),
                      tp("答えの確かめとして「展開して戻す」「具体的な数を代入する」の2つを、この単元を通して習慣にさせる。")]),
        theorem("th1", "3次の乗法公式と因数分解の公式",
                "$$a^3+b^3=(a+b)(a^2-ab+b^2),\\qquad a^3-b^3=(a-b)(a^2+ab+b^2)$$",
                ["2つ目の因数 $a^2\\mp ab+b^2$ の中央の符号は、1つ目の因数の符号と逆になる", "2つ目の因数は実数の範囲ではこれ以上因数分解できない"],
                body="展開の公式 $(a+b)^3=a^3+3a^2b+3ab^2+b^3$ とともに、右辺を展開して確かめておく。",
                proof=["$(a+b)(a^2-ab+b^2)$ を分配法則で展開する：$a^3-a^2b+ab^2+a^2b-ab^2+b^3$。", "$-a^2b$ と $+a^2b$、$+ab^2$ と $-ab^2$ が打ち消し合い、$a^3+b^3$ が残る。",
                       "$b$ を $-b$ におきかえると、$a^3+(-b)^3=(a-b)(a^2+ab+b^2)$、すなわち $a^3-b^3=(a-b)(a^2+ab+b^2)$ が得られる。"],
                points=[tp("公式を丸暗記させるのではなく、展開して中央の項が打ち消し合う様子を板書で見せる。", ask="なぜ $a^2b$ の項が消えるのか。", expect="$-a^2b$ と $+a^2b$ が両方現れるから。"),
                        tp("符号の覚え方として「1つ目の因数と同じ符号、2つ目の因数の中央は逆、最後は必ず $+$」と言語化させる。", caution="$a^3-b^3=(a-b)(a^2-ab+b^2)$ とする誤りが非常に多い。")]),
        definition("df1", "実数と絶対値",
                   "整数 $m$ と $0$ でない整数 $n$ を用いて分数 $\\dfrac{m}{n}$ の形に表せる数を有理数、有理数でない実数を無理数という。数直線上で、実数 $a$ を表す点と原点との距離を $a$ の絶対値といい、$|a|$ で表す。",
                   formula="$$|a|=\\begin{cases}a & (a\\geqq0)\\\\ -a & (a<0)\\end{cases}$$",
                   conditions=["$|a|\\geqq0$ であり、$|a|=0\\iff a=0$", "$|a-b|$ は数直線上の2点 $a,\\ b$ の間の距離を表す"],
                   points=[tp("$a<0$ のとき $|a|=-a$ となり「マイナスがついているのに正の数」であることを、$a=-3$ を代入して確認させる。", ask="$a=-3$ のとき $-a$ はいくつか。", expect="$3$")]),
        theorem("th2", "$\\sqrt{a^2}=|a|$",
                "$$\\sqrt{a^2}=|a|=\\begin{cases}a & (a\\geqq0)\\\\ -a & (a<0)\\end{cases}$$",
                ["$\\sqrt{\\ }$ は「2乗すると中身になる数のうち、$0$ 以上のもの」を表す", "$a$ が負のとき $\\sqrt{a^2}=a$ としてはいけない"],
                proof=["$\\sqrt{a^2}$ は、2乗して $a^2$ になる数のうち $0$ 以上のものである。", "2乗して $a^2$ になる数は $a$ と $-a$ の2つである。", "$a\\geqq0$ ならそのうち $0$ 以上のものは $a$、$a<0$ なら $-a$ である。",
                       "これはちょうど $|a|$ の定義と一致する。よって $\\sqrt{a^2}=|a|$。"],
                points=[tp("$\\sqrt{(-5)^2}$ を計算させ、$-5$ と答える生徒がいれば、$\\sqrt{25}=5$ と順に計算させて矛盾に気づかせる。", timing="定理の直後")]),
        derivation("dv1", "分母の有理化の仕組み",
                   ["$(\\sqrt{a}+\\sqrt{b})(\\sqrt{a}-\\sqrt{b})=(\\sqrt{a})^2-(\\sqrt{b})^2=a-b$ となり、根号が消える。",
                    "分数の分母と分子に同じ数（$0$ でない）をかけても、分数の値は変わらない。",
                    "したがって $\\dfrac{1}{\\sqrt{a}-\\sqrt{b}}$ の分母・分子に $\\sqrt{a}+\\sqrt{b}$ をかけると、$\\dfrac{\\sqrt{a}+\\sqrt{b}}{a-b}$ となり分母に根号を含まない形になる。",
                    "分母が $\\sqrt{a}+\\sqrt{b}$ のときは、$\\sqrt{a}-\\sqrt{b}$ をかければよい（和と差の積の公式）。"],
                   body="有理化は「分母の根号をなくして値の大きさを見やすくする」ための変形であり、値そのものは変わらない。",
                   points=[tp("$\\dfrac{1}{\\sqrt{2}-1}$ を有理化した $\\sqrt{2}+1\\fallingdotseq2.414$ を示し、有理化すると値の見積もりがしやすくなることを実感させる。")]),
        theorem("th3", "不等式の性質",
                "$$a<b\\ \\Longrightarrow\\ a+c<b+c,\\quad \\begin{cases}c>0\\ \\text{のとき}\\ ac<bc\\\\ c<0\\ \\text{のとき}\\ ac>bc\\end{cases}$$",
                ["負の数をかけたり、負の数で割ったりすると、不等号の向きが変わる", "移項（両辺に同じ数を足す・引く）では向きは変わらない"],
                proof=["$a<b$ は $b-a>0$ と同じ意味である。", "$c>0$ なら、正の数どうしの積は正なので $(b-a)c>0$、すなわち $bc-ac>0$ より $ac<bc$。",
                       "$c<0$ なら、正の数と負の数の積は負なので $(b-a)c<0$、すなわち $ac>bc$。向きが変わる。"],
                points=[tp("$2<3$ の両辺に $-1$ をかけて $-2$ と $-3$ を数直線上で比べ、向きが変わることを目で確認させる。", ask="$-2$ と $-3$ はどちらが大きいか。", expect="$-2$ の方が大きい。")]),
        example("ex1", "例題1　たすき掛け",
                "$6x^2+x-2$ を因数分解せよ。",
                ["$6x^2+x-2=(ax+b)(cx+d)$ とおくと、$ac=6,\\ bd=-2,\\ ad+bc=1$。", "$a=2,\\ c=3$ とし、$b,\\ d$ の組を試す。$b=-1,\\ d=2$ のとき $ad+bc=4-3=1$ で条件を満たす。",
                 "よって $(2x-1)(3x+2)$。展開して $6x^2+4x-3x-2=6x^2+x-2$ を確かめる。"],
                "$(2x-1)(3x+2)$",
                thinking="$x^2$ の係数が $1$ でないので、$x^2$ の係数と定数項の分け方を組み合わせて、$x$ の係数 $1$ になるものを探す。",
                points=[tp("たすき掛けの図を板書し、斜めにかけて足すと $x$ の係数になることを示す。", caution="候補の組合せを書き出さずに暗算で探すと見落としが多い。")],
                misconceptions=[("$(2x+1)(3x-2)$ とする（$x$ の係数が $-1$ になる）", "展開して $x$ の係数を必ず確かめ、符号を入れかえる")]),
        example("ex2", "例題2　分母の有理化と式の値",
                "$x=\\dfrac{2}{\\sqrt{5}-\\sqrt{3}}$ のとき、$x$ の分母を有理化し、$x^2$ の値を求めよ。",
                ["分母・分子に $\\sqrt{5}+\\sqrt{3}$ をかける：$x=\\dfrac{2(\\sqrt{5}+\\sqrt{3})}{5-3}=\\sqrt{5}+\\sqrt{3}$。",
                 "$x^2=(\\sqrt{5}+\\sqrt{3})^2=5+2\\sqrt{15}+3=8+2\\sqrt{15}$。"],
                "$x=\\sqrt{5}+\\sqrt{3}$、$x^2=8+2\\sqrt{15}$",
                thinking="分母の $\\sqrt{5}-\\sqrt{3}$ と組み合わせて根号が消える数（和と差の積）を考える。",
                points=[tp("分母が $5-3=2$ となり、分子の $2$ と約分できることを確認させる。")]),
        example("ex3", "例題3　絶対値を含む方程式",
                "方程式 $|x-1|=2x+1$ を解け。",
                ["(i) $x\\geqq1$ のとき：$x-1=2x+1$ より $x=-2$。これは $x\\geqq1$ を満たさないので不適。",
                 "(ii) $x<1$ のとき：$-(x-1)=2x+1$ より $-x+1=2x+1$、$x=0$。これは $x<1$ を満たす。", "(i)(ii) より $x=0$。"],
                "$x=0$",
                thinking="絶対値の中身 $x-1$ の符号で場合分けし、求めた解がその場合の条件を満たすかを必ず確かめる。",
                points=[tp("(i) で出た $x=-2$ を元の式に代入させ、$3=-3$ となって成り立たないことを確認させる。", ask="$x=-2$ は元の方程式を満たすか。", expect="左辺 $3$、右辺 $-3$ で満たさない。")],
                misconceptions=[("$x=-2,\\ 0$ と両方を答える", "場合分けの条件に合わない解は捨てる")]),
        board("bd1", "板書案",
              [("① 展開・因数分解", ["$a^3-b^3=(a-b)(a^2+ab+b^2)$", "たすき掛け：$6x^2+x-2$", "$=(2x-1)(3x+2)$", "確かめ：展開して元に戻る"]),
               ("② 実数と根号", ["$|a|$：原点からの距離", "$\\sqrt{a^2}=|a|$", "有理化：$(\\sqrt{a}+\\sqrt{b})(\\sqrt{a}-\\sqrt{b})=a-b$", "$\\dfrac{2}{\\sqrt{5}-\\sqrt{3}}=\\sqrt{5}+\\sqrt{3}$"]),
               ("③ 不等式と絶対値", ["負の数をかける → 向きが変わる", "$|x-a|<r\\iff a-r<x<a+r$", "$|x-1|=2x+1$", "場合分け → 条件を確認 → $x=0$"])],
              points=[tp("板書は左から ①→②→③ の順に書き、③ では必ず数直線をかいて範囲を示す。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("因数分解の答えは「これ以上分解できない」まで進めることを強調する（例：$x^4-16$ は3つの因数になる）。", caution="途中でやめた答案は誤りと扱う。"),
               tp("不等式で $x$ の係数が負になったときは、割る直前に「負の数で割るので向きが変わる」と声に出させる。", timing="一次不等式の演習中"),
               tp("絶対値の場合分けでは、各場合の条件と得られた解を並べて書き、条件に合うかを丸で囲んで確認させる。"),
               tp("$|x-a|$ を「$x$ と $a$ の距離」と読む見方を示すと、$|x-2|<3$ などは数直線から直ちに解けることを紹介する。", ask="$|x-2|<3$ を満たす $x$ は、数直線上でどんな点か。", expect="$2$ からの距離が $3$ より小さい点。"),
               tp("連立不等式では、それぞれの解を同じ数直線に重ねてかき、共通部分を読む。端点の白丸・黒丸を区別させる。")],
              misconceptions=[("$\\sqrt{(1-\\sqrt{3})^2}=1-\\sqrt{3}$", "$1-\\sqrt{3}<0$ なので $\\sqrt{(1-\\sqrt{3})^2}=\\sqrt{3}-1$"),
                              ("$-2x<6$ を $x<-3$ とする", "負の数 $-2$ で割るので向きが変わり $x>-3$"),
                              ("$x^3-27=(x-3)(x^2-3x+9)$", "2つ目の因数の中央は逆符号で $(x-3)(x^2+3x+9)$")]),
        summary("sm1", "まとめ",
                ["$a^3\\pm b^3=(a\\pm b)(a^2\\mp ab+b^2)$。因数分解は展開して確かめる。", "$\\sqrt{a^2}=|a|$。中身の符号を必ず調べる。有理化は和と差の積で根号を消す。",
                 "負の数をかける・割ると不等号の向きが変わる。絶対値は中身の符号で場合分けし、条件を確認する。"]),
        check("ck1", "確認問題",
              [("$8x^3+1$ を因数分解せよ。", "$(2x+1)(4x^2-2x+1)$"),
               ("$\\dfrac{3}{\\sqrt{7}+2}$ の分母を有理化せよ。", "$\\dfrac{3(\\sqrt{7}-2)}{7-4}=\\sqrt{7}-2$"),
               ("不等式 $|x+1|\\leqq4$ を解け。", "$-4\\leqq x+1\\leqq4$ より $-5\\leqq x\\leqq3$")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

@gen("basic_check", 5, ["computation"])
def expand_prod(r):
    mode = r.choice(["lin", "sq", "diff", "cube"])
    if mode == "lin":
        a, c = r.choice([1, 2, 3]), r.choice([1, 2, 3, 4])
        b, d = nonzero(r, -6, 6), nonzero(r, -6, 6)
        given = f"({poly(a, b)})({poly(c, d)})"
        pairs = [(a * c, "x^2"), (a * d + b * c, "x"), (b * d, "")]
        prod_py = f"({a}*x+({b}))*({c}*x+({d}))"
        hint = "分配法則で4つの積を作り、同類項 $x$ の項をまとめる。"
        ax, cx = terms([(a, "x")]), terms([(c, "x")])
        st = [f"$x^2$ の項：${ax}\\times {cx}={terms([(a * c, 'x^2')])}$。", f"$x$ の項：${ax}\\times ({d})+({b})\\times {cx}={terms([(a * d + b * c, 'x')])}$。", f"定数項：$({b})\\times ({d})={b * d}$。"]
    elif mode == "sq":
        a, b = r.choice([1, 2, 3]), nonzero(r, -4, 4)
        given = f"({terms([(a, 'x'), (b, 'y')])})^2"
        pairs = [(a * a, "x^2"), (2 * a * b, "xy"), (b * b, "y^2")]
        prod_py = f"({a}*x+({b})*y)**2"
        hint = "公式 $(p+q)^2=p^2+2pq+q^2$ で、$p=" + terms([(a, "x")]) + "$、$q=" + terms([(b, "y")]) + "$ とみる。"
        st = [f"$p^2={terms([(a * a, 'x^2')])}$。", f"$2pq=2\\times {terms([(a, 'x')])}\\times ({terms([(b, 'y')])})={terms([(2 * a * b, 'xy')])}$。", f"$q^2={terms([(b * b, 'y^2')])}$。"]
    elif mode == "diff":
        a, b = r.choice([1, 2, 3, 4]), r.choice([1, 2, 3, 5])
        given = f"({terms([(a, 'x'), (b, 'y')])})({terms([(a, 'x'), (-b, 'y')])})"
        pairs = [(a * a, "x^2"), (-b * b, "y^2")]
        prod_py = f"({a}*x+{b}*y)*({a}*x-{b}*y)"
        hint = "和と差の積 $(p+q)(p-q)=p^2-q^2$ が使える形である。"
        st = ["$(p+q)(p-q)=p^2-q^2$ を使う。", f"$p^2=({terms([(a, 'x')])})^2={a * a}x^2$、$q^2=({terms([(b, 'y')])})^2={b * b}y^2$。"]
    else:
        a, b = r.choice([1, 2]), nonzero(r, -3, 3)
        given = f"({poly(a, b)})^3"
        pairs = [(a ** 3, "x^3"), (3 * a * a * b, "x^2"), (3 * a * b * b, "x"), (b ** 3, "")]
        prod_py = f"({a}*x+({b}))**3"
        hint = "3次の展開公式 $(p+q)^3=p^3+3p^2q+3pq^2+q^3$ を使う。"
        st = [f"$p={terms([(a, 'x')])},\\ q={b}$ とする。", f"$p^3={terms([(a ** 3, 'x^3')])}$、$3p^2q={3 * a * a * b}x^2$、$3pq^2={3 * a * b * b}x$、$q^3={b ** 3}$。"]
    ans = terms(pairs)
    return sa(f"次の式を展開しなさい。　${given}$", f"${ans}$", f"${given}={ans}$。", d=1 if mode != "cube" else 2,
              ap=hint,
              steps=st + [f"まとめて ${ans}$。"],
              alt=["$x=1$（2文字なら $x=1,\\ y=1$）を元の式と答えの両方に代入し、値が一致するかで確かめられる。"],
              pc=[("公式の選択・各項の計算が正しい", 1), ("同類項を正しくまとめている", 1)],
              pit=["$2pq$ の項（中央の項）を落とす。", "負の数の2乗・3乗の符号を誤る。"],
              chk=(f"expand({prod_py})", pyterms(pairs), "expand"))


@gen("basic_check", 5, ["computation"])
def factor_quad(r):
    mode = r.choice(["monic", "ac", "ac", "common"])
    k = 1
    if mode == "monic":
        p, q = sorted([nonzero(r, -9, 9), nonzero(r, -9, 9)])
        a, b, c, d = 1, p, 1, q
    elif mode == "ac":
        while True:
            a, c = r.choice([2, 3, 4, 5, 6]), r.choice([1, 2, 3])
            b, d = nonzero(r, -5, 5), nonzero(r, -5, 5)
            if gcd(a, abs(b)) == 1 and gcd(c, abs(d)) == 1 and (a, b) != (c, d):
                break
    else:
        k = r.choice([2, 3, -2, 5])
        p, q = sorted([nonzero(r, -6, 6), nonzero(r, -6, 6)])
        a, b, c, d = 1, p, 1, q
    A, B, C = k * a * c, k * (a * d + b * c), k * b * d
    f1, f2 = f"({poly(a, b)})", f"({poly(c, d)})"
    kk = "" if k == 1 else ("-" if k == -1 else str(k))
    core = f"{f1}^2" if f1 == f2 else f"{f1}{f2}"
    ans = f"${kk}{core}$"
    v = [] if f1 == f2 else [f"{kk}{f2}{f1}"]
    st = {"monic": [f"積が ${b * d}$、和が ${b + d}$ となる2数を探すと ${b},\\ {d}$。", f"よって {ans}。"],
          "ac": [f"$x^2$ の係数 ${a * c}$ を ${a}\\times {c}$、定数項 ${b * d}$ を $({b})\\times ({d})$ と分ける。", f"たすき掛け：${a}\\times ({d})+({b})\\times {c}={a * d + b * c}$ が $x$ の係数に一致する。", f"よって {ans}。"],
          "common": [f"まず共通因数 ${k}$ をくくり出す：${k}({poly(1, b + d, b * d)})$。", f"かっこの中は、積が ${b * d}$、和が ${b + d}$ の2数 ${b},\\ {d}$ で因数分解できる。", f"よって {ans}。"]}[mode]
    return sa(f"次の式を因数分解しなさい。　${poly(A, B, C)}$", ans, f"${poly(A, B, C)}={ans[1:-1]}$。", d=2 if mode != "ac" else 3, v=v,
              ap={"monic": "$x^2$ の係数が $1$ なので、積が定数項・和が $x$ の係数になる2数を探す。",
                  "ac": "$x^2$ の係数が $1$ でないので、たすき掛けで係数の組合せを探す。",
                  "common": "すべての項に共通な因数があるので、最初にくくり出してから因数分解する。"}[mode],
              steps=st,
              alt=[f"答えを展開して ${poly(A, B, C)}$ に戻ることを確かめる。"],
              pc=[("因数の組合せを正しく見つけている", 1), ("最後まで因数分解して正しく答えている", 1)],
              pit=["定数項の符号の組合せ（$+$ と $-$）を誤る。", "共通因数をくくり出し忘れる。"],
              chk=(f"expand({k}*({a}*x+({b}))*({c}*x+({d})))", f"({A})*x**2+({B})*x+({C})", "expand"))


def rat_tex(k, a, b, minus):
    """k/(√a ∓ √b) を有理化した結果の LaTeX と sympy 式。minus=True は分母が √a-√b。"""
    d = a - b
    f = Fraction(k, d)
    op = "+" if minus else "-"
    inner = f"\\sqrt{{{a}}}{op}{root(b)}"
    if f.denominator == 1:
        p = f.numerator
        if p == 1:
            tex = inner
        elif b == 1:
            tex = f"{p}\\sqrt{{{a}}}{op}{p}"
        else:
            tex = f"{p}\\sqrt{{{a}}}{op}{p}\\sqrt{{{b}}}"
    else:
        num_ = "" if f.numerator == 1 else str(f.numerator)
        tex = f"\\dfrac{{{num_}({inner})}}{{{f.denominator}}}" if num_ else f"\\dfrac{{{inner}}}{{{f.denominator}}}"
    return tex, f"Rational({k},{d})*(sqrt({a}){op}sqrt({b}))"


@gen("basic_check", 4, ["computation"])
def rationalize(r):
    if r.random() < 0.3:
        a = r.choice(NONSQ[:7])
        k = r.randint(1, 12)
        f = Fraction(k, a)
        top = ("" if f.numerator == 1 else str(f.numerator)) + f"\\sqrt{{{a}}}"
        ans = top if f.denominator == 1 else f"\\dfrac{{{top}}}{{{f.denominator}}}"
        stem_e = f"\\dfrac{{{k}}}{{\\sqrt{{{a}}}}}"
        st = [f"分母・分子に $\\sqrt{{{a}}}$ をかける：$\\dfrac{{{k}\\sqrt{{{a}}}}}{{{a}}}$。", f"約分して ${ans}$。" if f.denominator != a else f"これ以上約分できないので ${ans}$。"]
        chk = (f"{k}/sqrt({a})", f"Rational({k},{a})*sqrt({a})")
        ap = "分母の $\\sqrt{" + str(a) + "}$ は、それ自身をかけると根号が消える。"
    else:
        a = r.choice(NONSQ[:7])
        b = r.choice([x for x in [1, 2, 3, 5, 6, 7] if x < a])
        d = a - b
        k = r.choice([1, d, 2 * d, 3 * d, 2])
        minus = r.random() < 0.6
        sop = "-" if minus else "+"
        conj = f"\\sqrt{{{a}}}{'+' if minus else '-'}{root(b)}"
        ans, ans_py = rat_tex(k, a, b, minus)
        stem_e = f"\\dfrac{{{k}}}{{\\sqrt{{{a}}}{sop}{root(b)}}}"
        numer = f"{k}({conj})" if k != 1 else conj
        st = [f"分母・分子に ${conj}$ をかける。", f"分母は $(\\sqrt{{{a}}})^2-({root(b)})^2={a}-{b}={d}$。", f"$\\dfrac{{{numer}}}{{{d}}}={ans}$。" if d != 1 else f"分母が $1$ になるので ${ans}$。"]
        chk = (f"{k}/(sqrt({a}){sop}sqrt({b}))", ans_py)
        ap = f"分母が ${root(b)}$ を含む和・差の形なので、和と差の積 $(p+q)(p-q)=p^2-q^2$ で根号を消す。"
    return sa(f"次の数の分母を有理化して、できるだけ簡単な形で答えなさい。　${stem_e}$", f"${ans}$", f"${stem_e}={ans}$。", d=2,
              ap=ap, steps=st,
              alt=["電卓的な概算（$\\sqrt{2}\\fallingdotseq1.414,\\ \\sqrt{3}\\fallingdotseq1.732$ など）で、有理化の前後の値がほぼ等しいことを確かめられる。"],
              pc=[("適切な数を分母・分子にかけている", 1), ("約分まで正しく行っている", 1)],
              pit=["分子にかけ忘れる（分母だけにかける）。", "分母の計算で $(\\sqrt{a})^2=a$ とせず $2a$ などとする。"],
              chk=chk)


@gen("basic_check", 3, ["concept", "condition_check"])
def abs_remove(r):
    mode = r.choice(["rad", "rad", "var", "two"])
    if mode == "rad":
        n = r.choice([2, 3, 5, 6, 7, 10, 11, 13, 14, 15, 17, 19, 21, 22])
        f = isqrt(n)
        k = r.choice([f, f + 1] + ([f - 1] if f > 1 else []))
        expr = f"|{k}-\\sqrt{{{n}}}|"
        pos = k > f
        right = f"${k}-\\sqrt{{{n}}}$" if pos else f"$\\sqrt{{{n}}}-{k}$"
        w1 = f"$\\sqrt{{{n}}}-{k}$" if pos else f"${k}-\\sqrt{{{n}}}$"
        w2, w3 = f"${k}+\\sqrt{{{n}}}$", f"$-{k}-\\sqrt{{{n}}}$"
        reason = f"${f}^2={f * f}<{n}<{(f + 1) ** 2}={f + 1}^2$ より ${f}<\\sqrt{{{n}}}<{f + 1}$。中身 ${k}-\\sqrt{{{n}}}$ は{'正' if pos else '負'}。"
        why = {w1: ("中身の符号を逆に判断している。$\\sqrt{" + str(n) + "}$ の大きさを整数ではさんで確かめる必要がある。", "中身の符号の判定もれ"),
               w2: ("絶対値をはずすときに、項ごとに符号を正にしてはいけない。中身全体の符号で判断する。", "各項を正にすれば絶対値がはずれるという誤解"),
               w3: ("中身全体に $-1$ をかけると $\\sqrt{" + str(n) + "}-" + str(k) + "$ であり、$-" + str(k) + "-\\sqrt{" + str(n) + "}$ にはならない。", "符号の分配の誤り")}
        chk = (f"Abs({k}-sqrt({n}))", f"{k}-sqrt({n})" if pos else f"sqrt({n})-{k}")
        cond = ""
    elif mode == "var":
        a = nonzero(r, -6, 6)
        cond = f"$x<{a}$ のとき、"
        expr = f"|{poly(1, -a)}|"
        right, w1, w2, w3 = f"${poly(-1, a)}$", f"${poly(1, -a)}$", f"${poly(1, a)}$", f"${poly(-1, -a)}$"
        reason = f"$x<{a}$ なので中身 ${poly(1, -a)}$ は負。符号を変えて $-({poly(1, -a)})={poly(-1, a)}$。"
        why = {w1: ("中身が負のときは、そのままでは絶対値をはずせない。", "中身の符号の確認もれ"),
               w2: ("$x$ の項ではなく定数項の符号だけを変えている。中身全体に $-1$ をかける。", "符号の分配の誤り"),
               w3: ("$-1$ を $x$ にだけでなく定数項にもかけると定数項は " + ("正" if a > 0 else "負") + "になる。", "符号の分配の誤り")}
        chk = (f"-(x-({a}))", f"{-1}*x+({a})", "expand")
    else:
        a, b = r.randint(1, 6), r.randint(1, 6)
        cond = f"$-{b}<x<{a}$ のとき、"
        expr = f"|x-{a}|+|x+{b}|"
        right, w1, w2, w3 = f"${a + b}$", f"$2x{cst(b - a)}$", f"${poly(-2, a - b)}$", f"${-a - b}$"
        if len({right, w1, w2, w3}) < 4:
            w1 = f"$2x+{a + b}$"
        reason = f"$x-{a}<0$、$x+{b}>0$ なので、$-(x-{a})+(x+{b})={a + b}$。"
        why = {w1: (f"$|x-{a}|$ の中身が負であることを見落とし、そのまま $x-{a}$ としている。", "中身の符号の確認もれ"),
               w2: (f"$|x+{b}|$ の中身は正なので符号を変えてはいけない。", "中身の符号の判断の誤り"),
               w3: ("両方の中身の符号を逆に判断している。絶対値の値は負にならない。", "絶対値は 0 以上という性質の無視")}
        chk = (f"Abs(Rational({a - b},2)-{a})+Abs(Rational({a - b},2)+{b})", str(a + b), None, "intermediate")
    return mc(f"{cond}${expr}$ を絶対値記号を使わずに表したものとして正しいものを選びなさい。", [right, w1, w2, w3], reason, d=2,
              ap="絶対値をはずすには、まず中身が正か負かを調べる。正ならそのまま、負なら全体に $-1$ をかける。",
              steps=["中身の符号を調べる。", reason, f"答えは {right}。"],
              alt=["条件に合う具体的な値を1つ代入し、元の式と選択肢の値が等しいかを確かめられる。"],
              pc=[("中身の符号を正しく判断している", 1), ("正しく絶対値をはずしている", 1)],
              why=why, chk=chk)


@gen("basic_check", 3, ["computation", "condition_check"])
def linear_ineq(r):
    rel = r.choice(["<", ">", "\\leqq ", "\\geqq "])
    if r.random() < 0.5:
        Lc, Rc = r.randint(-5, 6), r.randint(-5, 6)
        while Lc == Rc:
            Rc = r.randint(-5, 6)
        Lk, Rk = r.randint(-9, 9), r.randint(-9, 9)
        lhs = poly(Lc, Lk)
        rhs = poly(Rc, Rk)
        pre = []
    else:
        p, q = r.choice([2, 3, 4, -2, -3]), nonzero(r, -5, 5)
        Lc, Lk = p, -p * q
        Rc, Rk = r.randint(-5, 6), r.randint(-8, 8)
        while Lc == Rc:
            Rc = r.randint(-5, 6)
        lhs = f"{p}({poly(1, -q)})"
        rhs = poly(Rc, Rk)
        pre = [f"かっこをはずす：${poly(Lc, Lk)}{rel}{rhs}$。"]
    k, m = Lc - Rc, Rk - Lk
    rel2 = rel if k > 0 else FLIP[rel]
    bnd = frac(m, k)
    ans = f"$x{rel2}{bnd}$"
    kx = terms([(k, "x")])
    st = pre + [f"$x$ の項を左辺、定数項を右辺に移項する：${kx}{rel}{m}$。",
                ("よって" if k == 1 else f"両辺を ${k}$ で割る" + ("。" if k > 0 else "。負の数で割るので不等号の向きが変わる。")) + f"{ans}。"]
    return sa(f"$x$ についての一次不等式 ${lhs}{rel}{rhs}$ を解きなさい。", ans, f"${kx}{rel}{m}$ より {ans}。", d=2 if k > 0 else 3,
              ap="移項して $ax\\ (\\text{不等号})\\ b$ の形にし、$x$ の係数 $a$ の正負に注意して両辺を割る。",
              steps=st,
              alt=[f"境目 $x={bnd}$ を求めたあと、境目以外の値を1つ元の不等式に代入して成り立つかを調べ、解の向きを確かめることもできる。"],
              pc=[("移項して正しく整理している", 1), ("不等号の向き（負の数で割るとき）を正しく扱っている", 1)],
              pit=["負の数で割るときに不等号の向きを変え忘れる。", "移項するときに符号を変え忘れる。"],
              chk=(f"solve(({k})*x-({m}), x)", f"[{fr_py(m, k)}]", None, "intermediate"))


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 4, ["computation", "concept"])
def factor_cubic(r):
    m, k = r.choice([1, 2, 3]), r.randint(1, 5)
    while gcd(m, k) != 1:
        k = r.randint(1, 5)
    s = r.choice([1, -1])
    yv = r.random() < 0.4
    if not yv and m == 1 and k == 2 and s == -1:
        k = 4
    t = "y" if yv else ""
    given = terms([(m ** 3, "x^3"), (s * k ** 3, "y^3" if yv else "")])
    f1 = terms([(m, "x"), (s * k, t)])
    f2 = terms([(m * m, "x^2"), (-s * m * k, "xy" if yv else "x"), (k * k, "y^2" if yv else "")])
    ans = f"$({f1})({f2})$"
    p_tex, q_tex = terms([(m, "x")]), terms([(k, t)])
    form = "a^3+b^3=(a+b)(a^2-ab+b^2)" if s > 0 else "a^3-b^3=(a-b)(a^2+ab+b^2)"
    T = "y" if yv else "1"
    return sa(f"公式を利用して、次の式を因数分解しなさい。　${given}$", ans, f"$a={p_tex},\\ b={q_tex}$ として ${form}$ を使う。", d=3, v=[f"({f1})({f2})"],
              ap="各項が「何かの3乗」になっているかを見る。$" + str(m ** 3) + "x^3=(" + p_tex + ")^3$、$" + str(k ** 3) + ("y^3" if yv else "") + "=(" + q_tex + ")^3$ と書けるので3乗の公式が使える。",
              steps=[f"${given}=({p_tex})^3{'+' if s > 0 else '-'}({q_tex})^3$ と見る。", f"公式 ${form}$ に $a={p_tex},\\ b={q_tex}$ を代入する。", f"$a^2={terms([(m * m, 'x^2')])}$ などを計算して {ans}。"],
              alt=[f"答えを展開すると、中央の項が打ち消し合って ${given}$ に戻ることを確かめる。"],
              pc=[("3乗の形に正しく書き直している", 1), ("公式の符号を正しく使っている", 2), ("2つ目の因数を正しく計算している", 1)],
              pit=["2つ目の因数の中央の符号を1つ目と同じにしてしまう。", f"${q_tex}$ の2乗を計算し忘れる。"],
              chk=(f"expand(({m}*x+({s * k})*{T})*({m * m}*x**2+({-s * m * k})*x*{T}+{k * k}*{T}**2))",
                   pyterms([(m ** 3, "x^3"), (s * k ** 3, "y^3" if yv else "")]), "expand"))


@gen("standard_practice", 4, ["computation", "application"])
def factor_two_var(r):
    while True:
        a, c = nonzero(r, -3, 3), nonzero(r, -3, 3)
        b, d = nonzero(r, -4, 4), nonzero(r, -4, 4)
        if (a, b) != (c, d) and a + c != 0:
            break
    pairs = [(1, "x^2"), (a + c, "xy"), (a * c, "y^2"), (b + d, "x"), (a * d + b * c, "y"), (b * d, "")]
    given = terms(pairs)
    f1, f2 = terms([(1, "x"), (a, "y"), (b, "")]), terms([(1, "x"), (c, "y"), (d, "")])
    yq = f"({terms([(a * c, 'y^2'), (a * d + b * c, 'y'), (b * d, '')])})"
    ycoef = terms([(a + c, "y"), (b + d, "")])
    return sa(f"次の式を、$x$ について整理してから因数分解しなさい。　${given}$", f"$({f1})({f2})$",
              f"$x$ について整理すると $x^2+({ycoef})x+{yq}$。定数項は $({terms([(a, 'y'), (b, '')])})({terms([(c, 'y'), (d, '')])})$ と因数分解できる。", d=3,
              v=[f"({f2})({f1})"],
              ap="2文字を含む2次式は、次数の低い文字に限らず、1つの文字（ここでは $x$）について整理し、残りを係数とみなして因数分解する。",
              steps=[f"$x$ について整理：$x^2+({ycoef})x+{yq}$。", f"定数項（$y$ の式）を因数分解：${yq}=({terms([(a, 'y'), (b, '')])})({terms([(c, 'y'), (d, '')])})$。",
                     f"和が $x$ の係数 ${ycoef}$ になることを確かめ、$({f1})({f2})$。"],
              alt=["$y$ について整理しても同じ結果になる。また、答えを展開して元の式に戻ることを確かめる。"],
              pc=[("$x$ について正しく整理している", 1), ("$y$ の式の部分を正しく因数分解している", 1), ("全体の因数分解が正しい", 2)],
              pit=["整理するときに $xy$ の項を $x$ の係数に入れ忘れる。", "定数項の部分の因数分解の符号を誤る。"],
              chk=(f"expand((x+({a})*y+({b}))*(x+({c})*y+({d})))", pyterms(pairs), "expand"))


SYM_PAIRS = [(3, 1), (5, 1), (2, 1), (3, 2), (5, 3), (7, 5), (7, 3), (6, 2), (6, 5), (7, 6), (11, 7), (10, 6), (13, 11)]


@gen("standard_practice", 4, ["computation", "application"])
def symmetric(r):
    a, b = r.choice(SYM_PAIRS)
    s = 2 * (a + b) // (a - b)
    what = r.choice(["x^2+y^2", "x^3+y^3", "x^2-xy+y^2", "\\dfrac{y}{x}+\\dfrac{x}{y}"])
    val = {"x^2+y^2": s * s - 2, "x^3+y^3": s ** 3 - 3 * s, "x^2-xy+y^2": s * s - 3, "\\dfrac{y}{x}+\\dfrac{x}{y}": s * s - 2}[what]
    X = f"\\dfrac{{\\sqrt{{{a}}}+{root(b)}}}{{\\sqrt{{{a}}}-{root(b)}}}"
    Y = f"\\dfrac{{\\sqrt{{{a}}}-{root(b)}}}{{\\sqrt{{{a}}}+{root(b)}}}"
    xp, yp = f"((sqrt({a})+sqrt({b}))/(sqrt({a})-sqrt({b})))", f"((sqrt({a})-sqrt({b}))/(sqrt({a})+sqrt({b})))"
    wpy = {"x^2+y^2": f"{xp}**2+{yp}**2", "x^3+y^3": f"{xp}**3+{yp}**3", "x^2-xy+y^2": f"{xp}**2-{xp}*{yp}+{yp}**2",
           "\\dfrac{y}{x}+\\dfrac{x}{y}": f"{yp}/{xp}+{xp}/{yp}"}[what]
    how = {"x^2+y^2": f"$x^2+y^2=(x+y)^2-2xy={s * s}-2={val}$。", "x^3+y^3": f"$x^3+y^3=(x+y)^3-3xy(x+y)={s ** 3}-{3 * s}={val}$。",
           "x^2-xy+y^2": f"$x^2-xy+y^2=(x+y)^2-3xy={s * s}-3={val}$。",
           "\\dfrac{y}{x}+\\dfrac{x}{y}": f"$\\dfrac{{y}}{{x}}+\\dfrac{{x}}{{y}}=\\dfrac{{x^2+y^2}}{{xy}}=\\dfrac{{(x+y)^2-2xy}}{{xy}}={val}$。"}[what]
    return num(f"$x={X},\\ y={Y}$ のとき、${what}$ の値を求めなさい。", str(val),
               f"$x+y={s},\\ xy=1$。{how}", d=3,
               ap="$x,\\ y$ を直接代入すると計算が重い。$x,\\ y$ を入れかえても変わらない式（対称式）は、基本対称式 $x+y,\\ xy$ で表せるので、先にこの2つを求める。",
               steps=[f"$x$ と $y$ は互いに逆数なので $xy=1$。", f"$x+y=\\dfrac{{(\\sqrt{{{a}}}+{root(b)})^2+(\\sqrt{{{a}}}-{root(b)})^2}}{{{a}-{b}}}=\\dfrac{{{2 * (a + b)}}}{{{a - b}}}={s}$。", how],
               alt=[f"$x$ を有理化して $x=\\dfrac{{(\\sqrt{{{a}}}+{root(b)})^2}}{{{a - b}}}$ と表し、直接計算しても同じ値になる（計算量は多い）。"],
               pc=[("$x+y$ と $xy$ を正しく求めている", 2), ("対称式を基本対称式で表して値を求めている", 2)],
               pit=["$x+y$ を求めるときに通分で分母を $(\\sqrt{a}-\\sqrt{b})(\\sqrt{a}+\\sqrt{b})=a-b$ とせず誤る。", "$x^3+y^3=(x+y)^3-3xy(x+y)$ の $-3xy(x+y)$ を忘れる。"],
               chk=(wpy, str(val)))


@gen("standard_practice", 4, ["computation", "condition_check"])
def abs_eq_ineq(r):
    c = r.choice([1, 1, 2, 3])
    a, b = r.randint(-6, 6), r.randint(1, 7)
    rel = r.choice(["=", "<", "\\leqq ", ">", "\\geqq "])
    lo, hi = frac(a - b, c), frac(a + b, c)
    inner = poly(c, -a)
    if rel == "=":
        ans = f"$x={lo},\\ {hi}$"
        st = f"${inner}=\\pm{b}$"
    elif rel in ("<", "\\leqq "):
        ans = f"${lo}{rel}x{rel}{hi}$"
        st = f"$-{b}{rel}{inner}{rel}{b}$"
    else:
        r2 = "<" if rel == ">" else "\\leqq "
        ans = f"$x{r2}{lo},\\ {hi}{r2}x$"
        st = f"${inner}{r2}-{b}$ または ${b}{r2}{inner}$"
    return sa(f"$x$ についての次の方程式または不等式を解きなさい。　$|{inner}|{rel}{b}$", ans, f"{st} より {ans}。", d=3,
              ap="$|X|=r\\iff X=\\pm r$、$|X|<r\\iff -r<X<r$、$|X|>r\\iff X<-r$ または $r<X$（$r>0$）を使う。$|x-p|$ は数直線上の距離と読むこともできる。",
              steps=[f"$X={inner}$ とおくと $|X|{rel}{b}$。", f"{st}。", f"各辺を整理して {ans}。"],
              alt=[f"$X={inner}$ とおき、数直線上で原点からの距離が ${b}$ と比べてどうなる点かを考えて $X$ の範囲を求め、最後に $x$ の範囲に直してもよい。"],
              pc=[("絶対値をはずした式（場合分けまたは公式）が正しい", 2), ("範囲・解を正しく求めている", 2)],
              pit=["$|X|>r$ を $-r>X>r$ のようにつなげて書く（そのような $X$ は存在しない）。", "$x$ の係数で割ることを忘れる。"],
              chk=(f"solve(({c}*x-({a}))**2-{b}**2, x)", f"[{fr_py(a - b, c)}, {fr_py(a + b, c)}]", "set", "intermediate"))


@gen("standard_practice", 4, ["computation", "condition_check"])
def ineq_system(r):
    while True:
        k1, k2 = r.randint(1, 4), r.randint(1, 4)
        Ln, Un = r.randint(-12, 6), r.randint(-6, 16)
        L, U = Fraction(Ln, k1), Fraction(Un, k2)
        if U - L >= 1.5 and U - L <= 8:
            break
    C1, B1 = r.randint(-3, 3), r.randint(-6, 6)
    A1, D1 = C1 + k1, B1 + Ln
    C2, B2 = r.randint(-2, 4), r.randint(-6, 6)
    A2, D2 = C2 - k2, B2 - Un
    from math import floor
    cnt = floor(U) - floor(L)
    if cnt <= 0:
        cnt = 0
    ask = r.choice(["count", "max", "min"])
    e1, e2 = f"{poly(A1, B1)}>{poly(C1, D1)}", f"{poly(A2, B2)}\\geqq {poly(C2, D2)}"
    rng = f"${frac(L.numerator, L.denominator)}<x\\leqq {frac(U.numerator, U.denominator)}$"
    if ask == "count":
        q, val, cpy = "整数 $x$ の個数", cnt, f"floor({fr_py(Un, k2)})-floor({fr_py(Ln, k1)})"
    elif ask == "max":
        q, val, cpy = "最大の整数 $x$", floor(U), f"floor({fr_py(Un, k2)})"
    else:
        q, val, cpy = "最小の整数 $x$", floor(L) + 1, f"floor({fr_py(Ln, k1)})+1"
    return num(f"連立不等式 $\\begin{{cases}}{e1}\\\\ {e2}\\end{{cases}}$ を満たす{q}を求めなさい。", str(val),
               f"第1式から $x>{frac(Ln, k1)}$、第2式から $x\\leqq {frac(Un, k2)}$。共通部分は {rng}。", d=3,
               ap="それぞれの不等式を解き、数直線上で共通部分を求める。そのあと、範囲に含まれる整数を端点に注意して数える。",
               steps=[f"第1式：${terms([(k1, 'x')])}>{Ln}$ より $x>{frac(Ln, k1)}$。", f"第2式：${terms([(-k2, 'x')])}\\geqq {-Un}$ より、負の数で割って $x\\leqq {frac(Un, k2)}$。",
                      f"共通部分 {rng}。", f"この範囲の整数を調べて、{q}は ${val}$。"],
               alt=["範囲の端に近い整数を実際に2つの不等式に代入して、満たすかどうかを確かめる。"],
               pc=[("2つの不等式を正しく解いている", 2), ("共通部分を正しく求めている", 1), ("端点に注意して整数を正しく判断している", 1)],
               pit=["第2式で $x$ の係数が負のとき、不等号の向きを変え忘れる。", "端点が整数のとき、等号の有無（含むか含まないか）を誤る。"],
               chk=(cpy, str(val)))


# ======================================================================
# C 思考力・記述応用
# ======================================================================

@gen("thinking_writing", 3, ["written_reasoning", "condition_check"])
def int_frac_part(r):
    while True:
        n = r.choice([2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 17, 18, 19, 21, 22, 23])
        f = isqrt(n)
        m = r.randint(1, f) if f >= 1 else 1
        d = n - m * m
        if d > 0 and m * m < n:
            break
    a = f + m
    val = n - f * f
    return desc(f"$\\dfrac{{{d}}}{{\\sqrt{{{n}}}-{m}}}$ の整数部分を $a$、小数部分を $b$ とする。\n(1) $a,\\ b$ の値を求めなさい。\n(2) $b^2+{2 * f}b$ の値を求めなさい。",
                f"(1) $a={a},\\ b=\\sqrt{{{n}}}-{f}$　(2) ${val}$",
                f"有理化すると $\\sqrt{{{n}}}+{m}$。${f}<\\sqrt{{{n}}}<{f + 1}$ より $a={a}$、$b=\\sqrt{{{n}}}-{f}$。$b^2+{2 * f}b=(b+{f})^2-{f * f}={n}-{f * f}={val}$。",
                rubric=[("分母を正しく有理化している", 2), ("$\\sqrt{" + str(n) + "}$ を整数ではさむ根拠を示している", 2), ("$a,\\ b$ を正しく求めている", 2), ("(2) を工夫して（または正しく展開して）求めている", 2)],
                d=4, p=8, lines=8,
                ap="整数部分を求めるには、まず分母を有理化して値の大きさを見やすくし、$\\sqrt{" + str(n) + "}$ を連続する2整数ではさむ。小数部分は「元の数 $-$ 整数部分」である。",
                steps=[f"分母・分子に $\\sqrt{{{n}}}+{m}$ をかける：$\\dfrac{{{d}(\\sqrt{{{n}}}+{m})}}{{{n}-{m * m}}}=\\sqrt{{{n}}}+{m}$。",
                       f"${f * f}<{n}<{(f + 1) ** 2}$ より ${f}<\\sqrt{{{n}}}<{f + 1}$。よって ${a}<\\sqrt{{{n}}}+{m}<{a + 1}$。",
                       f"$a={a}$、$b=(\\sqrt{{{n}}}+{m})-{a}=\\sqrt{{{n}}}-{f}$。",
                       f"$b+{f}=\\sqrt{{{n}}}$ なので、$b^2+{2 * f}b=(b+{f})^2-{f * f}={n}-{f * f}={val}$。"],
                alt=[f"$b=\\sqrt{{{n}}}-{f}$ をそのまま代入して展開しても、$({n}-{2 * f}\\sqrt{{{n}}}+{f * f})+({2 * f}\\sqrt{{{n}}}-{2 * f * f})={val}$ となる。"],
                pc=[("有理化", 2), ("$\\sqrt{" + str(n) + "}$ の評価", 2), ("$a,\\ b$", 2), ("(2) の値", 2)],
                pit=["小数部分を $0.\\cdots$ のような近似値で答える（$b$ は正確な値 $\\sqrt{" + str(n) + "}-" + str(f) + "$ で表す）。", "整数部分に有理化で出た定数 $" + str(m) + "$ を加え忘れる。"],
                chk=(f"(sqrt({n})-{f})**2+{2 * f}*(sqrt({n})-{f})", str(val), None, "intermediate"))


@gen("thinking_writing", 3, ["written_reasoning", "condition_check"])
def param_ineq(r):
    p, m = r.randint(1, 4), nonzero(r, -6, 6)
    c = r.randint(-5, 5)
    rhs = poly(p, c + m)
    mt = f"\\dfrac{{{m}}}{{a-{p}}}" if m > 0 else f"-\\dfrac{{{-m}}}{{a-{p}}}"
    zero = "解はない" if m > 0 else "すべての実数"
    zero_r = f"$0\\cdot x>{m}$ は{'成り立たない' if m > 0 else 'つねに成り立つ'}"
    return desc(f"$a$ を定数とする。$x$ についての不等式 $ax{cst(c)}>{rhs}$ を解きなさい。",
                f"$a>{p}$ のとき $x>{mt}$、$a={p}$ のとき{zero}、$a<{p}$ のとき $x<{mt}$",
                f"移項して $(a-{p})x>{m}$。$x$ の係数 $a-{p}$ の符号で場合分けする。",
                rubric=[("$(a-" + str(p) + ")x>" + str(m) + "$ と正しく整理している", 2), ("係数の正・0・負の3通りに場合分けしている", 2),
                        ("$a\\neq" + str(p) + "$ の2つの場合を不等号の向きに注意して解いている", 2), ("$a=" + str(p) + "$ の場合を正しく判断している", 2)],
                d=4, p=8, lines=10,
                ap="$x$ の係数に文字が含まれるので、そのまま割ってはいけない。係数が正・0・負のどれかで、割り方（不等号の向き）や割れるかどうかが変わる。",
                steps=[f"移項して $(a-{p})x>{m}$。", f"(i) $a-{p}>0$、すなわち $a>{p}$ のとき：両辺を正の数 $a-{p}$ で割り $x>{mt}$。",
                       f"(ii) $a={p}$ のとき：{zero_r}ので、{zero}。", f"(iii) $a<{p}$ のとき：負の数 $a-{p}$ で割るので向きが変わり $x<{mt}$。"],
                alt=[f"具体的な値（たとえば $a={p + 1}$ と $a={p - 1}$）を代入して、それぞれの不等式を解いた結果が答えと一致するか確かめる。"],
                pc=[("移項・整理", 2), ("場合分けの基準", 2), ("$a\\neq" + str(p) + "$ の解", 2), ("$a=" + str(p) + "$ の判断", 2)],
                pit=[f"$a-{p}$ の符号を確かめずに割ってしまう。", f"$a={p}$ のとき「$x$ がない」と書いて終わり、解がすべての実数か解なしかを判断しない。"],
                chk=(f"solve((a-{p})*x-({m}), x)", f"[{m}/(a-{p})]", None, "intermediate"))


@gen("thinking_writing", 2, ["written_reasoning", "computation"])
def abs_two(r):
    while True:
        a, b = sorted(r.sample(range(-5, 7), 2))
        c = r.randint(b - a + 1, b - a + 8)
        if (a + b + c) % 2 == 0:
            break
    x1, x2 = (a + b - c) // 2, (a + b + c) // 2
    eq = r.random() < 0.6
    rel = "=" if eq else "<"
    stem_e = f"|{poly(1, -a)}|+|{poly(1, -b)}|{rel}{c}"
    ans = f"$x={x1},\\ {x2}$" if eq else f"${x1}<x<{x2}$"
    return desc(f"$x$ についての{'方程式' if eq else '不等式'} ${stem_e}$ を解きなさい。", ans,
                f"$x<{a}$、${a}\\leqq x<{b}$、${b}\\leqq x$ の3つの場合に分けて絶対値をはずす。",
                rubric=[("絶対値の中身の符号が変わる点 $x=" + str(a) + ",\\ " + str(b) + "$ で3つに場合分けしている", 2),
                        ("各場合で絶対値を正しくはずしている", 2), ("各場合の解が、その場合の条件を満たすか確認している", 2), ("結論を正しくまとめている", 2)],
                d=4, p=8, lines=10,
                ap="絶対値が2つあるので、それぞれの中身が $0$ になる $x=" + str(a) + ",\\ " + str(b) + "$ を境に、数直線を3つの区間に分けて考える。",
                steps=[f"(i) $x<{a}$：$-({poly(1, -a)})-({poly(1, -b)}){rel}{c}$ より $-2x{rel}{c - a - b}$、" + (f"$x={x1}$（$x<{a}$ を満たす）。" if eq else f"$x>{x1}$。条件と合わせて ${x1}<x<{a}$。"),
                       f"(ii) ${a}\\leqq x<{b}$：$({poly(1, -a)})-({poly(1, -b)})={b - a}$ なので ${b - a}{rel}{c}$ は" + ("成り立たない（解なし）。" if eq else "つねに成り立つ。この区間全体が解。"),
                       f"(iii) ${b}\\leqq x$：$2x{rel}{c + a + b}$ より " + (f"$x={x2}$（$x\\geqq {b}$ を満たす）。" if eq else f"$x<{x2}$。条件と合わせて ${b}\\leqq x<{x2}$。"),
                       f"以上をまとめて {ans}。"],
                alt=[f"$|{poly(1, -a)}|+|{poly(1, -b)}|$ は「数直線上の点 $x$ から2点 ${a},\\ {b}$ までの距離の和」である。2点の間ではつねに ${b - a}$、外側では両端から離れるほど大きくなるので、和が ${c}$ になる点は両外側に1つずつある。"],
                pc=[("場合分け", 2), ("絶対値のはずし方", 2), ("条件の確認", 2), ("結論", 2)],
                pit=["場合分けの境界の点を、どの場合にも含めない（または重複して含める）。", "求めた解が場合の条件を満たすかを確認しない。"],
                chk=(f"[Abs({x1}-({a}))+Abs({x1}-({b})), Abs({x2}-({a}))+Abs({x2}-({b}))]", f"[{c}, {c}]", None, "intermediate"))


@gen("thinking_writing", 2, ["cross_unit", "application"], rel=["HS-MATH1-U02"])
def cross_sets(r):
    a, b = r.randint(-3, 4), r.randint(2, 5)
    L = a - b + r.randint(1, 2 * b - 1)
    k, c1 = r.randint(1, 4), r.randint(-6, 6)
    comp = r.random() < 0.4
    Bdef = f"{poly(k + 1, c1)}\\geqq {poly(1, k * L + c1)}"
    target = "A\\cap\\overline{B}" if comp else "A\\cap B"
    ans = f"${a - b}<x<{L}$" if comp else f"${L}\\leqq x<{a + b}$"
    return sa(f"実数全体を全体集合とし、$A=\\{{x\\mid |{poly(1, -a)}|<{b}\\}}$、$B=\\{{x\\mid {Bdef}\\}}$ とする。集合 ${target}$ を、$x$ の範囲を表す不等式で答えなさい。",
              ans, f"$A$ は ${a - b}<x<{a + b}$、$B$ は $x\\geqq {L}$。" + ("$\\overline{B}$ は $x<" + str(L) + "$。" if comp else ""), d=4, p=8,
              ap="集合を条件で定めたときは、まず各条件を不等式として解き、数直線上で範囲を重ねて共通部分（補集合なら範囲の外側）を読み取る。",
              steps=[f"$|{poly(1, -a)}|<{b}$ より $-{b}<{poly(1, -a)}<{b}$、$A$：${a - b}<x<{a + b}$。", f"$B$ の不等式を整理：${terms([(k, 'x')])}\\geqq {k * L}$ より $x\\geqq {L}$。"]
              + (["$\\overline{B}$ は $B$ に含まれない実数全体なので $x<" + str(L) + "$（端点 $" + str(L) + "$ は $B$ に含まれるので $\\overline{B}$ には含まれない）。"] if comp else [])
              + [f"数直線上で共通部分をとり、{ans}。"],
              alt=["端点の値（$x=" + str(L) + "$ など）を元の条件に代入して、集合に含まれるかどうかを確かめる。"],
              pc=[("$A$ の範囲を正しく求めている", 2), ("$B$ の範囲を正しく求めている", 2), ("共通部分（・補集合）を端点まで正しく答えている", 4)],
              pit=["$\\overline{B}$ の端点の扱い（$\\geqq$ の補集合は $<$）を誤る。", "絶対値の不等式を $x-" + str(a) + "<" + str(b) + "$ だけにしてしまう。"],
              chk=(f"[{a}-{b}, {a}+{b}, solve({k}*x-({k * L}), x)[0]]", f"[{a - b}, {a + b}, {L}]", None, "intermediate"))


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(stem, wrong, step, etype, tempt, fix, ans, expl, steps, ap, alt, pit, chk=None, d=3):
    return desc(f"{stem}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい答えを求めなさい。", ans, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい解答を途中式とともに示している", 3), ("最終的な答えが正しい", 1)], d=d, p=6, lines=6,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい途中式", 3), ("正しい答え", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix), chk=chk)


@gen("error_correction", 3, ["common_error", "computation"])
def err_ineq_flip(r):
    while True:
        A, C = r.randint(-4, 3), r.randint(-2, 6)
        if A - C < 0:
            break
    B, D = r.randint(-9, 9), r.randint(-9, 9)
    rel = r.choice(["<", ">", "\\leqq ", "\\geqq "])
    k, m = A - C, D - B
    bnd = frac(m, k)
    kx = terms([(k, "x")])
    wrong = f"${poly(A, B)}{rel}{poly(C, D)}$ より ${kx}{rel}{m}$。両辺を ${k}$ で割って $x{rel}{bnd}$"
    ans = f"$x{FLIP[rel]}{bnd}$"
    return err_item(f"不等式 ${poly(A, B)}{rel}{poly(C, D)}$ を解きなさい。", wrong, f"両辺を ${k}$ で割った部分", "sign",
                    "方程式を解くときと同じ感覚で両辺を割っている。$x$ の係数が負になったことに注意が向いていない。",
                    f"${kx}{rel}{m}$ の両辺を負の数 ${k}$ で割ると不等号の向きが変わり、{ans}", ans,
                    f"負の数で割ると不等号の向きが変わるので {ans}。",
                    [f"移項して ${kx}{rel}{m}$。", f"${k}<0$ なので、両辺を ${k}$ で割ると向きが変わる。", f"{ans}。"],
                    "$x$ の係数が負のまま割るときは、不等号の向きが変わる。移項の向きを工夫して係数を正にしてもよい。",
                    [f"$x$ の項を右辺に集めると ${terms([(-k, 'x')])}{FLIP[rel]}{-m}$ となり、正の数で割るだけで {ans} が得られる。", "境目以外の値を1つ代入して、元の不等式が成り立つ側を確かめる。"],
                    ["負の数で割る・かけるときに向きを変え忘れる。"],
                    chk=(f"solve(({k})*x-({m}), x)", f"[{fr_py(m, k)}]", None, "intermediate"), d=2)


@gen("error_correction", 3, ["common_error", "condition_check"])
def err_abs_extraneous(r):
    while True:
        a, c = r.randint(-4, 5), r.randint(-9, 9)
        if c != -2 * a and (a - c) % 3 == 0:
            break
    x1, x2 = -a - c, (a - c) // 3
    good = x1 if c <= -2 * a else x2
    bad = x2 if good == x1 else x1
    inner = poly(1, -a)
    rhs = poly(2, c)
    wrong = f"${inner}={rhs}$ より $x={x1}$、$-({inner})={rhs}$ より $x={x2}$。よって $x={x1},\\ {x2}$"
    case_bad = f"x\\geqq {a}" if bad == x1 else f"x<{a}"
    return err_item(f"方程式 $|{inner}|={rhs}$ を解きなさい。", wrong, "得られた2つの値をどちらも解とした部分", "condition",
                    "絶対値をはずすときに「$\\pm$ をつければよい」と覚えていて、それぞれの式が成り立つための条件（中身の符号）を考えていない。",
                    f"$x\\geqq {a}$ のとき $x={x1}$、$x<{a}$ のとき $x={x2}$ で、条件を満たすのは $x={good}$ のみ", f"$x={good}$",
                    f"$x={bad}$ は ${case_bad}$ を満たさず、代入すると左辺 ${abs(bad - a)}$、右辺 ${2 * bad + c}$ で成り立たない。",
                    [f"(i) $x\\geqq {a}$ のとき：${inner}={rhs}$ より $x={x1}$。" + ("条件を満たす。" if good == x1 else "条件を満たさないので不適。"),
                     f"(ii) $x<{a}$ のとき：$-({inner})={rhs}$ より $x={x2}$。" + ("条件を満たす。" if good == x2 else "条件を満たさないので不適。"), f"よって $x={good}$。"],
                    "右辺に $x$ を含む絶対値の方程式では、中身の符号で場合分けし、各場合の条件を満たす解だけを残す。",
                    [f"左辺は $0$ 以上なので、右辺も ${rhs}\\geqq0$ でなければならない。$x={bad}$ のとき右辺は ${2 * bad + c}$ で負になるので、この条件からも除かれる。",
                     "得られた値を元の方程式に代入して確かめる。"],
                    ["場合分けの条件を書かずに式だけ解く。", "代入による確かめを省く。"],
                    chk=(f"[Abs({good}-({a}))-(2*{good}+({c})), Abs({bad}-({a}))-(2*{bad}+({c}))]", f"[0, {abs(bad - a) - (2 * bad + c)}]", None, "intermediate"))


@gen("error_correction", 2, ["common_error", "concept"])
def err_sqrt_sq(r):
    if r.random() < 0.6:
        n = r.choice([3, 5, 6, 7, 10, 11, 13, 14, 15, 17, 19, 21])
        f = isqrt(n)
        k = r.randint(max(1, f - 2), f)
        j = r.randint(f + 1, f + 3)
        stem = f"$\\sqrt{{({k}-\\sqrt{{{n}}})^2}}+\\sqrt{{({j}-\\sqrt{{{n}}})^2}}$ を簡単にしなさい。"
        wrong = f"$({k}-\\sqrt{{{n}}})+({j}-\\sqrt{{{n}}})={k + j}-2\\sqrt{{{n}}}$"
        ans = f"${j - k}$"
        fix = f"${k}-\\sqrt{{{n}}}<0$ なので $\\sqrt{{({k}-\\sqrt{{{n}}})^2}}=\\sqrt{{{n}}}-{k}$。${j}-\\sqrt{{{n}}}>0$ なので $\\sqrt{{({j}-\\sqrt{{{n}}})^2}}={j}-\\sqrt{{{n}}}$。和は ${j - k}$"
        st = [f"${f}<\\sqrt{{{n}}}<{f + 1}$ より、${k}-\\sqrt{{{n}}}<0$、${j}-\\sqrt{{{n}}}>0$。", f"$\\sqrt{{({k}-\\sqrt{{{n}}})^2}}=|{k}-\\sqrt{{{n}}}|=\\sqrt{{{n}}}-{k}$。",
              f"$\\sqrt{{({j}-\\sqrt{{{n}}})^2}}={j}-\\sqrt{{{n}}}$。", f"和は $(\\sqrt{{{n}}}-{k})+({j}-\\sqrt{{{n}}})={j - k}$。"]
        chk = (f"sqrt(({k}-sqrt({n}))**2)+sqrt(({j}-sqrt({n}))**2)", str(j - k))
        alt = [f"$\\sqrt{{{n}}}\\fallingdotseq{round(n ** 0.5, 2)}$ を使って元の式を概算すると約 ${j - k}$ になり、生徒の答え ${k + j}-2\\sqrt{{{n}}}\\fallingdotseq{round(k + j - 2 * n ** 0.5, 2)}$ とは一致しない。"]
    else:
        a, b = r.randint(1, 5), r.randint(1, 5)
        stem = f"$-{a}<x<{b}$ のとき、$\\sqrt{{(x+{a})^2}}+\\sqrt{{(x-{b})^2}}$ を簡単にしなさい。"
        wrong = f"$(x+{a})+(x-{b})={poly(2, a - b)}$"
        ans = f"${a + b}$"
        fix = f"$x-{b}<0$ なので $\\sqrt{{(x-{b})^2}}=-(x-{b})$。$(x+{a})-(x-{b})={a + b}$"
        st = [f"$-{a}<x<{b}$ より $x+{a}>0$、$x-{b}<0$。", f"$\\sqrt{{(x+{a})^2}}=|x+{a}|=x+{a}$。", f"$\\sqrt{{(x-{b})^2}}=|x-{b}|=-(x-{b})$。", f"和は $(x+{a})-(x-{b})={a + b}$。"]
        x0 = f"Rational({b - a},2)"
        chk = (f"sqrt(({x0}+{a})**2)+sqrt(({x0}-{b})**2)", str(a + b), None, "intermediate")
        alt = [f"範囲内の値 $x=0$ を代入すると元の式は ${a}+{b}={a + b}$、生徒の答えは ${a - b}$ となり、一致しないことから誤りに気づける。"]
    return err_item(stem, wrong, "根号をはずした部分（中身の符号の確認もれ）", "concept",
                    "$\\sqrt{a^2}=a$ と覚えていて、$a$ が負のときに成り立たないことを意識していない。",
                    fix, ans, "$\\sqrt{A^2}=|A|$ であり、$A<0$ のときは $-A$ になる。", st,
                    "$\\sqrt{A^2}$ は $A$ ではなく $|A|$。中身の正負を調べてから根号をはずす。", alt,
                    ["$\\sqrt{A^2}=A$ と機械的にはずす。"], chk=chk)


@gen("error_correction", 2, ["common_error", "computation"])
def err_factor(r):
    if r.random() < 0.55:
        m, k = r.choice([1, 2, 3]), r.randint(1, 5)
        while gcd(m, k) != 1:
            k = r.randint(1, 5)
        s = r.choice([1, -1])
        given = terms([(m ** 3, "x^3"), (s * k ** 3, "")])
        f1 = poly(m, s * k)
        wrong_f2 = poly(m * m, s * m * k, k * k)
        right_f2 = poly(m * m, -s * m * k, k * k)
        wrong = f"${given}=({f1})({wrong_f2})$"
        ans = f"$({f1})({right_f2})$"
        return err_item(f"${given}$ を因数分解しなさい。", wrong, "2つ目の因数の $x$ の項の符号", "formula",
                        "1つ目の因数と同じ符号を2つ目の因数にも使ってしまう。公式の符号の並びを、展開で確かめずに覚えている。",
                        f"${given}=({f1})({right_f2})$", ans,
                        f"$a^3{'+' if s > 0 else '-'}b^3=(a{'+' if s > 0 else '-'}b)(a^2{'-' if s > 0 else '+'}ab+b^2)$ で、2つ目の因数の中央の符号は1つ目と逆。",
                        [f"${given}=({terms([(m, 'x')])})^3{'+' if s > 0 else '-'}{k}^3$。", "公式の2つ目の因数は $a^2\\mp ab+b^2$（中央は1つ目と逆符号）。", f"{ans}。"],
                        "3乗の和・差の公式は、展開して中央の項が打ち消し合うかで符号を確かめられる。",
                        [f"生徒の答えを展開すると $x^2$ の項 ${2 * s * m * m * k}x^2$ が残り、元の式に戻らない。"],
                        ["2つ目の因数の中央の符号を誤る。"],
                        chk=(f"expand(({m}*x+({s * k}))*({m * m}*x**2+({-s * m * k})*x+{k * k}))", f"{m ** 3}*x**3+({s * k ** 3})", "expand"))
    m = r.choice([1, 1, 2])
    k = r.choice([1, 3] if m == 2 else [1, 2, 3, 4])
    given = terms([(m ** 4, "x^4"), (-k ** 4, "")])
    p = terms([(m, "x")])
    wrong = f"${given}=({poly(m * m, 0, -k * k, var='x')})({poly(m * m, 0, k * k, var='x')})$"
    ans = f"$({poly(m, -k)})({poly(m, k)})({poly(m * m, 0, k * k)})$"
    return err_item(f"${given}$ を因数分解しなさい。", wrong, "1つ目の因数 $" + poly(m * m, 0, -k * k) + "$ をそのままにした部分", "concept",
                    "1回公式を使えたことで満足し、得られた因数がさらに分解できるかを確かめていない。",
                    f"${poly(m * m, 0, -k * k)}=({poly(m, -k)})({poly(m, k)})$ とさらに分解して {ans}", ans,
                    f"$({p})^2-{k * k}$ は和と差の積でさらに因数分解できる。$({p})^2+{k * k}$ は実数の範囲でこれ以上分解できない。",
                    [f"$({terms([(m * m, 'x^2')])})^2-{k * k}^2=({poly(m * m, 0, -k * k)})({poly(m * m, 0, k * k)})$。",
                     f"${poly(m * m, 0, -k * k)}=({poly(m, -k)})({poly(m, k)})$。", f"よって {ans}。"],
                    "因数分解の答えは、各因数がこれ以上分解できないところまで進める。",
                    [f"$x={frac(k, m)}$ を代入すると元の式は $0$ になるので、$({poly(m, -k)})$ を因数にもつはずだと気づける（因数定理の考え方）。"],
                    ["途中で因数分解をやめる。"],
                    chk=(f"expand(({m}*x-{k})*({m}*x+{k})*({m * m}*x**2+{k * k}))", f"{m ** 4}*x**4-{k ** 4}", "expand"))


GENERATORS = [expand_prod, factor_quad, rationalize, abs_remove, linear_ineq,
              factor_cubic, factor_two_var, symmetric, abs_eq_ineq, ineq_system,
              int_frac_part, param_ineq, abs_two, cross_sets,
              err_ineq_flip, err_abs_extraneous, err_sqrt_sq, err_factor]
