"""単元パック：数学Ⅰ データの分析（四分位数・分散と標準偏差・相関係数・仮説検定の考え方）。"""
from fractions import Fraction
from math import comb, isqrt, sqrt

from banks._common import desc, figure, mc, num, plane, sa, table
from hs_pack_lib import (board, check, definition, example, figure_explain, frac, fr_py, gen, guide, intro, lesson, nonzero,
                         summary, theorem, tp)

UNIT_ID = "HS-MATH1-U05"


def fnum(f):
    """Fraction → 小数（有限小数なら）または分数の LaTeX。"""
    f = Fraction(f)
    if f.denominator == 1:
        return str(f.numerator)
    d = f.denominator
    while d % 2 == 0:
        d //= 2
    while d % 5 == 0:
        d //= 5
    if d == 1:
        return f"{float(f):g}"
    return frac(f.numerator, f.denominator)


def fans(f):
    """num の正答文字列（整数・有限小数・分数 a/b）。"""
    f = Fraction(f)
    if f.denominator == 1:
        return str(f.numerator)
    s = fnum(f)
    return s if "dfrac" not in s else f"{f.numerator}/{f.denominator}"


def co(k):
    """係数の表記（1 → 空、-1 → -）。"""
    return "" if k == 1 else ("-" if k == -1 else str(k))


def lst(xs):
    return "，".join(map(str, xs))


def pylist(xs):
    return "[" + ", ".join(map(str, xs)) + "]"


def median(xs):
    xs = sorted(xs)
    n = len(xs)
    return Fraction(xs[n // 2]) if n % 2 else Fraction(xs[n // 2 - 1] + xs[n // 2], 2)


def quartiles(xs):
    xs = sorted(xs)
    n = len(xs)
    return median(xs[: n // 2]), median(xs), median(xs[(n + 1) // 2:])


def var(xs):
    m = Fraction(sum(xs), len(xs))
    return sum((x - m) ** 2 for x in xs) / len(xs)


def r2(v):
    """小数第3位を四捨五入した値（文字列）。"""
    from decimal import ROUND_HALF_UP, Decimal
    return str(Decimal(repr(v)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def r3(v):
    from decimal import ROUND_HALF_UP, Decimal
    return str(Decimal(repr(v)).quantize(Decimal("0.001"), rounding=ROUND_HALF_UP))


def tail_prob(n, k):
    """公正なコインを n 回投げて表が k 回以上出る確率（厳密値）。"""
    return Fraction(sum(comb(n, i) for i in range(k, n + 1)), 2 ** n)


SCATTER = [(1, 2), (2, 4), (3, 5), (4, 4), (5, 5)]

LESSON = lesson(
    goals=["四分位数・箱ひげ図・外れ値の意味を理解し、データの散らばりを読み取れる。",
           "分散・標準偏差を定義に従って、また公式 $s^2=\\overline{x^2}-(\\overline{x})^2$ を用いて計算でき、変量の変換による変化を説明できる。",
           "共分散と相関係数を計算して2つの変量の関係を判断し、仮説検定の考え方を用いて主張の妥当性を説明できる。"],
    duration=100,
    readiness=["平均値・中央値・最頻値（中学1年）を求められる。", "四分位数と箱ひげ図（中学2年）をかける。", "平方根の計算と、確率の基本的な求め方を知っている。"],
    flow=[("導入：平均値が同じでも違うデータ", 10, "平均値が等しく散らばりが異なる2組のデータを比べ、散らばりの指標が必要なことを確認する"),
          ("四分位数・箱ひげ図・外れ値", 15, "四分位範囲と外れ値の基準を確認する"),
          ("分散と標準偏差", 25, "定義・計算公式の導出と例題1、変量の変換"),
          ("散布図と相関係数", 25, "共分散・相関係数の定義と計算（例題2）、相関と因果の区別"),
          ("仮説検定の考え方", 20, "コイン投げの例で、仮説のもとで起こる確率を基準と比べて判断する（例題3）"),
          ("まとめと確認", 5, "確認問題3問、問題プリントA の課題指示")],
    sections=[
        intro("in1", "平均値だけでは分からないこと",
              "2つのクラスの小テストの平均点がどちらも 6 点でも、一方は全員が 5〜7 点、もう一方は 0 点から 10 点まで大きくばらついているかもしれない。データの特徴をとらえるには、代表値に加えて「散らばりの度合い」を数値で表す必要がある。さらに2つの変量の関係や、「偶然とは考えにくいか」を判断する方法も学ぶ。",
              bullets=["散らばりの指標：範囲、四分位範囲、分散、標準偏差。", "2つの変量の関係：散布図、共分散、相関係数。", "判断の方法：仮説検定の考え方（ある仮定のもとで、その結果がどのくらい起こりやすいか）。"],
              points=[tp("平均値が等しい2組のデータをドットプロットで並べて示し、違いを言葉で説明させる。", ask="2つのデータはどこが違うか。", expect="値の散らばり方が違う。", timing="導入の冒頭"),
                      tp("この単元では「計算した値が何を意味するか」を必ず言葉で説明させる方針を伝える。")]),
        definition("df1", "四分位数と外れ値",
                   "データを小さい順に並べ、中央値で前半と後半に分ける（データの個数が奇数のときは中央値を除く）。前半の中央値を第1四分位数 $Q_1$、後半の中央値を第3四分位数 $Q_3$ という。$Q_3-Q_1$ を四分位範囲という。",
                   formula="$$\\text{外れ値の目安：}\\ Q_1-1.5(Q_3-Q_1)\\ \\text{より小さい値、または}\\ Q_3+1.5(Q_3-Q_1)\\ \\text{より大きい値}$$",
                   conditions=["四分位範囲は、極端な値の影響を受けにくい散らばりの指標である", "外れ値の基準は1つの目安であり、問題文の定めに従う"],
                   points=[tp("データの個数が奇数・偶数の場合で、前半・後半の分け方が変わることを具体例で確認させる。", caution="奇数個のとき中央値を前半・後半の両方に入れる誤りが多い。")]),
        definition("df2", "分散と標準偏差",
                   "変量 $x$ のデータを $x_1,\\ x_2,\\ \\cdots,\\ x_n$、平均値を $\\overline{x}$ とする。各値と平均値の差 $x_k-\\overline{x}$ を偏差といい、偏差の2乗の平均値を分散 $s^2$、その正の平方根を標準偏差 $s$ という。",
                   formula="$$s^2=\\dfrac{1}{n}\\left\\{(x_1-\\overline{x})^2+(x_2-\\overline{x})^2+\\cdots+(x_n-\\overline{x})^2\\right\\},\\qquad s=\\sqrt{s^2}$$",
                   conditions=["偏差の和はつねに $0$ になるので、偏差をそのまま平均しても散らばりは測れない（2乗してから平均する）", "標準偏差は元のデータと同じ単位をもつ"],
                   points=[tp("偏差の和が $0$ になることを例で確かめさせ、なぜ2乗するのかを考えさせる。", ask="偏差をそのまま平均するとどうなるか。", expect="いつも $0$ になる。")]),
        theorem("th1", "分散の計算公式と変量の変換",
                "$$s^2=\\overline{x^2}-(\\overline{x})^2,\\qquad y=ax+b\\ \\text{のとき}\\ \\overline{y}=a\\overline{x}+b,\\ \\ s_y^2=a^2s_x^2,\\ \\ s_y=|a|s_x$$",
                ["$\\overline{x^2}$ は $x^2$ の平均値（2乗の平均）であり、$(\\overline{x})^2$（平均の2乗）とは異なる", "変換で $b$（全体を平行移動する量）は散らばりに影響しない"],
                proof=["$(x_k-\\overline{x})^2=x_k^2-2\\overline{x}x_k+(\\overline{x})^2$ を $k=1$ から $n$ まで加えて $n$ で割る。",
                       "$\\dfrac{1}{n}\\sum x_k^2=\\overline{x^2}$、$\\dfrac{1}{n}\\sum x_k=\\overline{x}$ より、$s^2=\\overline{x^2}-2\\overline{x}\\cdot\\overline{x}+(\\overline{x})^2=\\overline{x^2}-(\\overline{x})^2$。",
                       "$y_k=ax_k+b$ の平均は $\\dfrac{1}{n}\\sum(ax_k+b)=a\\overline{x}+b$。",
                       "偏差は $y_k-\\overline{y}=a(x_k-\\overline{x})$ となるので、2乗して平均すると $s_y^2=a^2s_x^2$。正の平方根をとって $s_y=|a|s_x$。"],
                points=[tp("$s_y=as_x$ と書く誤りに対し、$a=-2$ の例で標準偏差が負になる矛盾を示す。", caution="$|a|$ の絶対値を落とす誤りが多い。"),
                        tp("計算公式は、平均値が整数にならないデータや、2乗の平均が与えられている場合に有効であることを示す。")]),
        definition("df3", "共分散と相関係数",
                   "2つの変量 $x,\\ y$ の組のデータについて、偏差の積 $(x_k-\\overline{x})(y_k-\\overline{y})$ の平均値を共分散 $s_{xy}$ という。共分散をそれぞれの標準偏差の積で割った値を相関係数 $r$ という。",
                   formula="$$s_{xy}=\\dfrac{1}{n}\\sum_{k=1}^{n}(x_k-\\overline{x})(y_k-\\overline{y}),\\qquad r=\\dfrac{s_{xy}}{s_xs_y}$$",
                   conditions=["$-1\\leqq r\\leqq 1$ であり、$r$ が $1$ に近いほど強い正の相関、$-1$ に近いほど強い負の相関がある", "$r$ が $0$ に近いときは直線的な相関がほとんどない", "相関があっても、一方が他方の原因であるとは限らない"],
                   points=[tp("散布図を4つの区画に分け、偏差の積の符号が区画ごとに決まることから、共分散の符号の意味を説明する。")]),
        figure_explain("fg1", "散布図と偏差の積",
                       figure("5点の散布図。平均値の点(3,4)を通る縦線と横線で4つの区画に分かれている",
                              plane((0, 6), (0, 6), unit=22, points=[(x, y, "") for x, y in SCATTER], segments=[((3, 0), (3, 6)), ((0, 4), (6, 4))])),
                       "平均値 $(\\overline{x},\\ \\overline{y})=(3,\\ 4)$ を通る直線で区切ると、右上と左下の区画の点は偏差の積が正、左上と右下の区画の点は負になる。右上・左下に点が多いほど共分散は大きな正の値になる。",
                       points=[tp("点ごとに偏差の積の符号を書きこませ、合計の符号が散布図の傾向と一致することを確認させる。")]),
        definition("df4", "仮説検定の考え方",
                   "ある主張が正しいかどうかを判断するために、その主張に反する仮説（たとえば「コインは公正である」）を立てる。その仮説のもとで、実際に得られた結果以上に極端なことが起こる確率を求め、それがあらかじめ決めた基準（たとえば $5\\%$）より小さければ、仮説は正しくなかったと判断する。",
                   conditions=["確率が基準より小さいとき：「めったに起こらないことが起こった」と考え、仮説を誤りと判断する", "確率が基準以上のとき：仮説が誤りとは判断できない（仮説が正しいと証明されたわけではない）"],
                   points=[tp("「判断できない」と「正しいと証明された」の違いを強調する。", caution="基準以上のとき「仮説は正しい」と結論する答案が多い。", timing="例題3の後")]),
        example("ex1", "例題1　分散と標準偏差",
                "データ 5，7，8，9，11 の分散と標準偏差を求めよ。",
                ["平均値は $\\dfrac{5+7+8+9+11}{5}=8$。", "偏差は $-3,\\ -1,\\ 0,\\ 1,\\ 3$。", "偏差の2乗の和は $9+1+0+1+9=20$ なので、分散は $\\dfrac{20}{5}=4$。", "標準偏差は $\\sqrt{4}=2$。"],
                "分散 $4$、標準偏差 $2$",
                thinking="定義どおり、平均値 → 偏差 → 偏差の2乗の平均 の順に求める。",
                points=[tp("偏差の和が $0$ になることを途中で確かめる習慣をつけさせる（計算ミスの発見に役立つ）。")],
                misconceptions=[("分散を $\\dfrac{20}{4}=5$ とする（$n-1$ で割る）", "数学Ⅰでは個数 $n=5$ で割る")]),
        example("ex2", "例題2　相関係数",
                "5人の2つのテストの得点 $(x,\\ y)$ が $(1,\\ 2),\\ (2,\\ 4),\\ (3,\\ 5),\\ (4,\\ 4),\\ (5,\\ 5)$ である（架空のデータ）。相関係数を小数第3位を四捨五入して求めよ。",
                ["$\\overline{x}=3,\\ \\overline{y}=4$。$x$ の偏差：$-2,\\ -1,\\ 0,\\ 1,\\ 2$、$y$ の偏差：$-2,\\ 0,\\ 1,\\ 0,\\ 1$。",
                 "偏差の積の和は $4+0+0+0+2=6$、$x$ の偏差の2乗の和は $10$、$y$ の偏差の2乗の和は $6$。",
                 "$r=\\dfrac{6}{\\sqrt{10}\\sqrt{6}}=\\dfrac{6}{\\sqrt{60}}\\fallingdotseq0.7746$。"],
                "$r\\fallingdotseq0.77$",
                thinking="$r=\\dfrac{s_{xy}}{s_xs_y}$ で、分子・分母の $\\dfrac{1}{n}$ は約分できるので、和のまま計算してよい。",
                points=[tp("共通の $\\dfrac{1}{n}$ が約分できることを示し、計算量を減らす工夫として紹介する。")]),
        example("ex3", "例題3　仮説検定の考え方",
                "あるコインを10回投げたところ、表が9回出た。「このコインは表が出やすい」と判断してよいか。基準となる確率を $5\\%$ として考えよ。",
                ["「コインは公正である（表と裏が出る確率はともに $\\dfrac{1}{2}$）」という仮説を立てる。",
                 "仮説のもとで、表が9回以上出る確率は $\\dfrac{{}_{10}\\mathrm{C}_9+{}_{10}\\mathrm{C}_{10}}{2^{10}}=\\dfrac{11}{1024}\\fallingdotseq0.011$。",
                 "これは $0.05$ より小さいので、仮説のもとではめったに起こらないことが起こったと考え、仮説は誤りと判断する。"],
                "表が出やすいと判断してよい",
                thinking="主張と反対の「公正である」を仮定し、実際の結果以上に偏る確率を求めて基準と比べる。",
                points=[tp("「9回ちょうど」ではなく「9回以上」の確率を求める理由（それ以上に極端な場合も含めて評価する）を説明する。")]),
        board("bd1", "板書案",
              [("① 散らばり", ["四分位範囲 $Q_3-Q_1$", "外れ値：$Q_1-1.5\\times$IQR より小", "分散 $s^2$＝偏差の2乗の平均", "$s^2=\\overline{x^2}-(\\overline{x})^2$", "$y=ax+b$：$s_y=|a|s_x$"]),
               ("② 相関", ["$s_{xy}$＝偏差の積の平均", "$r=\\dfrac{s_{xy}}{s_xs_y}$、$-1\\leqq r\\leqq1$", "例題2：$r\\fallingdotseq0.77$", "相関 ≠ 因果"]),
               ("③ 仮説検定", ["仮説：コインは公正", "9回以上の確率 $\\dfrac{11}{1024}\\fallingdotseq0.011$", "$0.011<0.05$ → 仮説は誤り", "基準以上 → 判断できない"])],
              points=[tp("③では「仮説 → 確率 → 基準と比較 → 結論」の4段階を板書の型として示す。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("分散の計算では、平均値が整数なら定義、そうでなければ計算公式、と使い分けを判断させる。"),
               tp("標準偏差を答えるときは単位（点、cm など）をつけさせ、分散との単位の違いに気づかせる。", ask="身長（cm）のデータの分散の単位は何か。", expect="$\\mathrm{cm}^2$"),
               tp("相関係数の値だけでなく、散布図をかいて外れ値や曲線的な関係がないか確かめさせる。"),
               tp("相関があっても因果関係があるとは限らない例（気温とアイスの売上と水難事故の件数など、共通の要因がある場合）を口頭で紹介する。", timing="相関係数の後"),
               tp("仮説検定では、基準の確率（有意水準）を先に決めておくこと、結論は「判断できる／できない」の形で書くことを徹底させる。")],
              misconceptions=[("$\\overline{x^2}$ と $(\\overline{x})^2$ を同じものとして扱う", "2乗の平均と平均の2乗は一般に異なる（その差が分散）"),
                              ("$y=-2x+3$ のとき $s_y=-2s_x$", "$s_y=|-2|s_x=2s_x$"),
                              ("確率が $5\\%$ 以上なので仮説は正しいと証明された", "仮説が誤りとは判断できない、というだけである")]),
        summary("sm1", "まとめ",
                ["分散＝偏差の2乗の平均＝$\\overline{x^2}-(\\overline{x})^2$、標準偏差＝$\\sqrt{\\text{分散}}$。$y=ax+b$ で $s_y=|a|s_x$。",
                 "相関係数 $r=\\dfrac{s_{xy}}{s_xs_y}$（$-1\\leqq r\\leqq1$）。相関は因果を意味しない。",
                 "仮説検定：仮説のもとでの確率を基準と比べ、小さければ仮説は誤りと判断する。"]),
        check("ck1", "確認問題",
              [("データ 2，3，5，6，9 の分散を求めよ。", "平均 $5$、偏差の2乗の和 $9+4+0+1+16=30$ より $6$"),
               ("$x$ の標準偏差が $4$ のとき、$y=-3x+1$ の標準偏差を求めよ。", "$|-3|\\times4=12$"),
               ("$s_{xy}=6,\\ s_x=2,\\ s_y=5$ のとき、相関係数を求めよ。", "$\\dfrac{6}{2\\times5}=0.6$")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

def nice_data(r, n, spread=6):
    """平均値が整数のデータ。"""
    while True:
        m = r.randint(5, 30)
        devs = [r.randint(-spread, spread) for _ in range(n - 1)]
        last = -sum(devs)
        if abs(last) <= spread + 2:
            xs = [m + d for d in devs + [last]]
            if min(xs) >= 0 and len(set(xs)) >= n - 1:
                r.shuffle(xs)
                return xs, m


@gen("basic_check", 5, ["computation"])
def mean_var(r):
    n = r.choice([5, 5, 6, 4])
    for _ in range(200):
        xs, m = nice_data(r, n)
        v = var(xs)
        if v.denominator == 1 or v.denominator in (2, 4, 5):
            break
    ask_sd = isqrt(v.numerator) ** 2 == v.numerator and v.denominator == 1 and r.random() < 0.5
    sv = int(sqrt(v)) if ask_sd else None
    devs = [x - m for x in xs]
    sq = [d * d for d in devs]
    q = "標準偏差" if ask_sd else "分散"
    val = str(sv) if ask_sd else fans(v)
    return num(f"次のデータの{q}を求めなさい。　{lst(xs)}", val,
               f"平均値 ${m}$、偏差の2乗の和 ${sum(sq)}$ より、分散 ${fnum(v)}$" + (f"、標準偏差 ${sv}$。" if ask_sd else "。"), d=2,
               disp=f"${fnum(v) if not ask_sd else sv}$",
               ap="定義どおり、平均値 → 偏差 → 偏差の2乗の平均（分散）→ その正の平方根（標準偏差）の順に求める。",
               steps=[f"平均値：$\\dfrac{{{sum(xs)}}}{{{n}}}={m}$。", f"偏差：{'，'.join(f'${d}$' for d in devs)}（和は $0$）。",
                      f"偏差の2乗：{'，'.join(f'${s}$' for s in sq)}、和は ${sum(sq)}$。", f"分散 $=\\dfrac{{{sum(sq)}}}{{{n}}}={fnum(v)}$。" + (f"標準偏差 $=\\sqrt{{{sv * sv}}}={sv}$。" if ask_sd else "")],
               alt=[f"計算公式 $s^2=\\overline{{x^2}}-(\\overline{{x}})^2$ を使うと、$\\overline{{x^2}}={fnum(Fraction(sum(x * x for x in xs), n))}$ より $s^2={fnum(Fraction(sum(x * x for x in xs), n))}-{m * m}={fnum(v)}$。"],
               pc=[("平均値と偏差を正しく求めている", 1), (f"{q}を正しく計算している", 1)],
               pit=["偏差を2乗せずに平均してしまう（必ず $0$ になる）。", "個数 $n$ ではなく $n-1$ で割る。"],
               chk=(f"std({pylist(xs)})" if ask_sd else f"variance({pylist(xs)})", val))


@gen("basic_check", 5, ["computation", "concept"])
def quartile(r):
    n = r.choice([7, 8, 9, 10, 11])
    xs = sorted(r.sample(range(10, 60), n))
    show = xs[:]
    r.shuffle(show)
    q1, q2, q3 = quartiles(xs)
    ask = r.choice(["Q1", "Q3", "IQR", "IQR"])
    val = {"Q1": q1, "Q3": q3, "IQR": q3 - q1}[ask]
    word = {"Q1": "第1四分位数", "Q3": "第3四分位数", "IQR": "四分位範囲"}[ask]
    lo, hi = xs[: n // 2], xs[(n + 1) // 2:]
    split = "中央値を除いて" if n % 2 else ""
    idx = {"Q1": 0, "Q3": 2, "IQR": None}[ask]
    chk = (f"quartiles({pylist(show)})[{idx}]", fans(val)) if idx is not None else (f"quartiles({pylist(show)})[2]-quartiles({pylist(show)})[0]", fans(val))
    return num(f"次の {n} 個のデータの{word}を求めなさい。　{lst(show)}", fans(val),
               f"小さい順に並べると {lst(xs)}。$Q_1={fnum(q1)}$、$Q_2={fnum(q2)}$、$Q_3={fnum(q3)}$。", d=2, disp=f"${fnum(val)}$",
               ap="まずデータを小さい順に並べ、中央値で前半・後半に分ける（個数が奇数なら中央値はどちらにも入れない）。",
               steps=[f"小さい順に並べる：{lst(xs)}。", f"中央値 $Q_2={fnum(q2)}$。{split}前半 {lst(lo)}、後半 {lst(hi)}。",
                      f"前半の中央値 $Q_1={fnum(q1)}$、後半の中央値 $Q_3={fnum(q3)}$。"] + ([f"四分位範囲 $=Q_3-Q_1={fnum(q3)}-{fnum(q1)}={fnum(q3 - q1)}$。"] if ask == "IQR" else []),
               alt=["箱ひげ図をかいて、箱の左端・右端の値として読み取り、計算結果と一致するか確かめる。"],
               pc=[("データを並べて前半・後半に正しく分けている", 1), (f"{word}を正しく求めている", 1)],
               pit=["データを並べ替えずに中央値をとる。", "個数が奇数のとき、中央値を前半・後半に含めてしまう。"],
               chk=chk)


@gen("basic_check", 4, ["computation", "condition_check"])
def transform(r):
    m, s = r.randint(3, 60), r.randint(2, 9)
    a, b = nonzero(r, -4, 5, exclude=(0, 1)), r.randint(-20, 30)
    ask = r.choice(["mean", "var", "sd", "sd"])
    if ask == "mean":
        val, q, how = a * m + b, "平均値", f"$\\overline{{y}}={a}\\times{m}{'+' if b >= 0 else ''}{b}={a * m + b}$"
    elif ask == "var":
        val, q, how = a * a * s * s, "分散", f"$s_y^2=({a})^2\\times{s}^2={a * a * s * s}$"
    else:
        val, q, how = abs(a) * s, "標準偏差", f"$s_y=|{a}|\\times{s}={abs(a) * s}$"
    bt = "" if b == 0 else (f"+{b}" if b > 0 else f"{b}")
    return num(f"変量 $x$ のデータの平均値が ${m}$、標準偏差が ${s}$ である。変量 $y$ を $y={co(a)}x{bt}$ で定めるとき、$y$ のデータの{q}を求めなさい。", str(val),
               f"{how}。", d=2,
               ap="$y=ax+b$ のとき、平均値は $a\\overline{x}+b$、分散は $a^2$ 倍、標準偏差は $|a|$ 倍になる。$b$ は散らばりに影響しない。",
               steps=[f"$a={a},\\ b={b}$。", how + "。"],
               alt=[f"具体的なデータ（たとえば ${m - s},\\ {m + s}$ の2つの値）で $y$ を計算し、{q}を直接求めて確かめる。"],
               pc=[("変換の公式を正しく選んでいる", 1), ("正しく計算している", 1)],
               pit=["標準偏差に $b$ を加えてしまう。", f"標準偏差を ${a}$ 倍として負の値にする（$|a|$ 倍が正しい）。" if a < 0 else "分散を $a$ 倍としてしまう（$a^2$ 倍が正しい）。"],
               chk=({"mean": f"{a}*{m}+({b})", "var": f"({a})**2*{s}**2", "sd": f"Abs({a})*{s}"}[ask], str(val)))


@gen("basic_check", 3, ["concept"])
def corr_meaning(r):
    rv = r.choice(["0.93", "0.87", "0.95", "-0.91", "-0.86", "-0.94", "0.04", "-0.03", "0.02"])
    f = float(rv)
    ctx = r.choice([("ある地域の各日の最高気温", "その日の飲料の販売数"), ("生徒の1日の勉強時間", "小テストの得点"), ("中古車の走行距離", "販売価格"),
                    ("ある果樹の木の高さ", "その年の収穫量")])
    A = "強い正の相関がある"
    B = "強い負の相関がある"
    C = "直線的な相関はほとんどない"
    D = f"{ctx[0]}が{ctx[1]}を変化させる原因であると結論できる"
    right = A if f >= 0.8 else (B if f <= -0.8 else C)
    others = [x for x in (A, B, C, D) if x != right]
    why = {A: ("正の強い相関は $r$ が $1$ に近いとき。" + ("この値は負である。" if f < 0 else "この値は $0$ に近い。"), "相関係数の符号・大きさの読み誤り"),
           B: ("負の強い相関は $r$ が $-1$ に近いとき。" + ("この値は正である。" if f > 0 else "この値は $0$ に近い。"), "相関係数の符号・大きさの読み誤り"),
           C: (f"$|r|={abs(f)}$ は $1$ に近く、強い相関がある。", "相関係数の大きさの読み誤り"),
           D: ("相関係数は2つの変量の直線的な関係の強さを表すだけで、因果関係は示さない。", "相関と因果の混同")}
    return mc(f"{ctx[0]} $x$ と{ctx[1]} $y$ について調べたところ、相関係数は ${rv}$ であった（架空のデータ）。この結果の解釈として最も適切なものを選びなさい。",
              [right] + others, f"$r={rv}$ なので{right}。", d=1,
              ap="相関係数の符号で正・負の相関を、絶対値の大きさ（$1$ に近いか $0$ に近いか）で相関の強さを判断する。因果関係は相関係数からは分からない。",
              steps=[f"符号は{'正' if f > 0 else '負'}。", f"絶対値は ${abs(f)}$ で、{'$1$ に近い' if abs(f) >= 0.8 else '$0$ に近い'}。", f"よって{right}。"],
              alt=["散布図を想像すると、$r$ が $1$ に近いときは右上がり、$-1$ に近いときは右下がりの直線の近くに点が集まる。"],
              pc=[("符号と大きさを正しく読み取っている", 1), ("相関と因果を区別している", 1)],
              why={o: why[o] for o in others})


RS = [Fraction(1, 4), Fraction(1, 2), Fraction(3, 5), Fraction(3, 4), Fraction(4, 5), Fraction(9, 10), Fraction(-2, 5), Fraction(-3, 5), Fraction(-4, 5), Fraction(-1, 2), Fraction(-7, 10)]


@gen("basic_check", 3, ["computation"])
def corr_from_cov(r):
    while True:
        sx, sy, rv = r.randint(2, 8), r.randint(2, 9), r.choice(RS)
        sxy = rv * sx * sy
        if (sx, sy, sxy) != (4, 5, 12) and fnum(sxy).find("dfrac") < 0:
            break
    return num(f"2つの変量 $x,\\ y$ について、$x$ の標準偏差が ${sx}$、$y$ の標準偏差が ${sy}$、$x$ と $y$ の共分散が ${fnum(sxy)}$ である。$x$ と $y$ の相関係数を求めなさい。",
               fans(rv), f"$r=\\dfrac{{{fnum(sxy)}}}{{{sx}\\times{sy}}}={fnum(rv)}$。", d=1, disp=f"${fnum(rv)}$",
               ap="相関係数は共分散を2つの標準偏差の積で割った値 $r=\\dfrac{s_{xy}}{s_xs_y}$。",
               steps=[f"$s_xs_y={sx}\\times{sy}={sx * sy}$。", f"$r=\\dfrac{{{fnum(sxy)}}}{{{sx * sy}}}={fnum(rv)}$。"],
               alt=["求めた値が $-1\\leqq r\\leqq 1$ の範囲にあることを確かめる（範囲外なら計算ミス）。"],
               pc=[("公式を正しく用いている", 1), ("正しく計算している", 1)],
               pit=["分散の積で割ってしまう。", "共分散の符号を落とす。"],
               chk=(f"{fr_py(sxy.numerator, sxy.denominator)}/({sx}*{sy})", fans(rv)))


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 4, ["computation", "concept"])
def var_formula(r):
    n = r.choice([8, 10, 12, 20, 25, 50])
    m = r.randint(3, 40)
    sd = r.randint(1, 12)
    ask_sd = r.random() < 0.5
    if not ask_sd and r.random() < 0.5:
        v = sd * sd + r.choice([1, 2, 3, 5, 6])
    else:
        v = sd * sd
    q2 = m * m + v
    q = "標準偏差" if ask_sd else "分散"
    val = isqrt(v) if ask_sd and isqrt(v) ** 2 == v else (None if ask_sd else v)
    if val is None:
        ask_sd, q, val = False, "分散", v
    return num(f"{n} 個の値からなる変量 $x$ のデータについて、$x$ の平均値は ${m}$、$x^2$ の平均値は ${q2}$ であった。$x$ のデータの{q}を求めなさい。", str(val),
               f"$s^2=\\overline{{x^2}}-(\\overline{{x}})^2={q2}-{m * m}={v}$" + (f"、$s={val}$。" if ask_sd else "。"), d=3,
               ap="個々の値が分からなくても、$\\overline{x}$ と $\\overline{x^2}$ が分かれば計算公式 $s^2=\\overline{x^2}-(\\overline{x})^2$ で分散が求まる。",
               steps=[f"$(\\overline{{x}})^2={m}^2={m * m}$。", f"$s^2={q2}-{m * m}={v}$。"] + ([f"$s=\\sqrt{{{v}}}={val}$。"] if ask_sd else []),
               alt=["公式の導出（偏差の2乗を展開して平均する）を思い出せば、引く量が「平均の2乗」であることを確かめられる。"],
               pc=[("計算公式を正しく選んでいる", 2), (f"{q}を正しく求めている", 2)],
               pit=["$\\overline{x^2}-\\overline{x}$ と、平均を2乗し忘れる。", "標準偏差を求めるときに平方根をとり忘れる。"],
               chk=(f"sqrt({q2}-{m}**2)" if ask_sd else f"{q2}-{m}**2", str(val)))


@gen("standard_practice", 4, ["computation"])
def corr_calc(r):
    while True:
        dx = [-2, -1, 0, 1, 2]
        r.shuffle(dx)
        dy = [r.randint(-4, 4) for _ in range(4)]
        dy.append(-sum(dy))
        sxy = sum(a * b for a, b in zip(dx, dy))
        syy = sum(b * b for b in dy)
        if abs(dy[-1]) <= 5 and sxy != 0 and syy > 0 and 0.15 < abs(sxy / sqrt(10 * syy)) < 0.99:
            break
    mx, my = r.randint(3, 8), r.randint(4, 9)
    xs, ys = [mx + d for d in dx], [my + d for d in dy]
    rv = sxy / sqrt(10 * syy)
    ans = r2(rv)
    rows = [["$x$"] + [str(v) for v in xs], ["$y$"] + [str(v) for v in ys]]
    pairs = "，".join(f"$({x},\\ {y})$" for x, y in zip(xs, ys))
    return num(f"5人の生徒の2つの小テストの得点 $(x,\\ y)$ は {pairs} であった（架空のデータ。下の表にもまとめてある）。$x$ と $y$ の相関係数を、小数第3位を四捨五入して小数第2位まで求めなさい。",
               ans, f"$\\overline{{x}}={mx},\\ \\overline{{y}}={my}$。偏差の積の和 ${sxy}$、偏差の2乗の和はそれぞれ $10,\\ {syy}$。$r=\\dfrac{{{sxy}}}{{\\sqrt{{10}}\\sqrt{{{syy}}}}}\\fallingdotseq{ans}$。", d=3,
               tbl=table(rows, header=["生徒", "1", "2", "3", "4", "5"]),
               ap="平均値 → 偏差 → 偏差の積の和と偏差の2乗の和 の順に表をつくる。$r=\\dfrac{s_{xy}}{s_xs_y}$ の $\\dfrac{1}{n}$ は分子・分母で約分できるので、和のまま計算してよい。",
               steps=[f"$\\overline{{x}}={mx}$、$\\overline{{y}}={my}$。", f"$x$ の偏差：{'，'.join(map(str, dx))}、$y$ の偏差：{'，'.join(map(str, dy))}。",
                      f"偏差の積の和 ${sxy}$、$x$ の偏差の2乗の和 $10$、$y$ の偏差の2乗の和 ${syy}$。", f"$r=\\dfrac{{{sxy}}}{{\\sqrt{{{10 * syy}}}}}\\fallingdotseq{r3(rv)}$ より ${ans}$。"],
               alt=[f"共分散 $s_{{xy}}={fnum(Fraction(sxy, 5))}$、標準偏差 $s_x=\\sqrt{{2}}$、$s_y=\\sqrt{{{fnum(Fraction(syy, 5))}}}$ を求めてから $r=\\dfrac{{s_{{xy}}}}{{s_xs_y}}$ に代入しても同じ値になる。"],
               pc=[("平均値と偏差を正しく求めている", 1), ("偏差の積の和・2乗の和を正しく求めている", 2), ("相関係数を正しく四捨五入している", 1)],
               pit=["偏差の積の符号を誤る。", "分母を $\\sqrt{10\\times" + str(syy) + "}$ ではなく $10\\times" + str(syy) + "$ としてしまう。"],
               chk=(f"floor(({sxy})/sqrt(10*{syy})*100+Rational(1,2))/100", ans))


@gen("standard_practice", 4, ["computation", "condition_check"])
def outlier(r):
    for _ in range(500):
        n = r.choice([9, 10, 11, 12])
        base = sorted(r.sample(range(30, 61), n - 1))
        extra = r.choice([r.randint(85, 120), r.randint(85, 120), r.randint(0, 8), r.randint(32, 58)])
        xs = sorted(base + [extra])
        if len(set(xs)) < n:
            continue
        q1, _, q3 = quartiles(xs)
        iqr = q3 - q1
        L, U = q1 - Fraction(3, 2) * iqr, q3 + Fraction(3, 2) * iqr
        if any(x == L or x == U for x in xs):
            continue
        outs = [x for x in xs if x < L or x > U]
        if len(outs) <= 2:
            break
    show = xs[:]
    r.shuffle(show)
    ans = "，".join(map(str, outs)) if outs else "なし"
    return sa(f"次の {n} 個のデータについて、「第1四分位数から四分位範囲の1.5倍を引いた値より小さい値、または第3四分位数に四分位範囲の1.5倍を加えた値より大きい値」を外れ値とする。外れ値をすべて答えなさい（ない場合は「なし」と答えなさい）。　{lst(show)}",
              ans, f"$Q_1={fnum(q1)},\\ Q_3={fnum(q3)}$、四分位範囲 ${fnum(iqr)}$。基準は ${fnum(L)}$ より小さい値と ${fnum(U)}$ より大きい値。", d=3,
              ap="外れ値の基準は四分位数から決まるので、まず小さい順に並べて $Q_1,\\ Q_3$ と四分位範囲を求め、下側・上側の基準値を計算する。",
              steps=[f"小さい順：{lst(xs)}。", f"$Q_1={fnum(q1)}$、$Q_3={fnum(q3)}$、四分位範囲 ${fnum(iqr)}$。",
                     f"下側の基準 ${fnum(q1)}-1.5\\times{fnum(iqr)}={fnum(L)}$、上側の基準 ${fnum(q3)}+1.5\\times{fnum(iqr)}={fnum(U)}$。", f"基準の外にある値：{ans}。"],
              alt=["箱ひげ図をかき、箱の長さの1.5倍を箱の両端から伸ばした範囲の外にある点を確かめる。"],
              pc=[("四分位数と四分位範囲を正しく求めている", 2), ("基準値を正しく計算している", 1), ("外れ値を正しく判定している", 1)],
              pit=["四分位範囲の1.5倍を、四分位数ではなく中央値から引いてしまう。", "データを並べ替えずに四分位数を求める。"],
              chk=(f"quartiles({pylist(show)})", f"[{fr_py(q1.numerator, q1.denominator)}, {fr_py(median(xs).numerator, median(xs).denominator)}, {fr_py(q3.numerator, q3.denominator)}]", None, "intermediate"))


TEST_CTX = [
    ("あるコインを {n} 回投げたところ、表が {k} 回出た", "このコインは公正である（表が出る確率は $\\dfrac{{1}}{{2}}$）", "このコインは表が出やすい", "このコインは裏が出やすい", "表が {k} 回以上出る"),
    ("2つの選択肢から1つを選ぶ問題 {n} 問に、ある生徒が答えたところ {k} 問正解した", "この生徒はでたらめに答えている（各問の正解の確率は $\\dfrac{{1}}{{2}}$）", "この生徒には実力がある", "この生徒は正解しにくい答え方をしている", "{k} 問以上正解する"),
    ("新しい飲料 A と従来の飲料 B を {n} 人に飲み比べてもらったところ、{k} 人が A の方がおいしいと答えた", "A と B の好みに差はない（A を選ぶ確率は $\\dfrac{{1}}{{2}}$）", "A の方が好まれる", "B の方が好まれる", "{k} 人以上が A を選ぶ"),
]


def test_case(r):
    while True:
        n = r.randint(10, 30)
        k = r.randint(n // 2 + 2, n - 1)
        P = tail_prob(n, k)
        if 0.004 < P < 0.2 and not (0.045 < P < 0.056):
            return n, k, P


@gen("standard_practice", 4, ["concept", "application"])
def hypothesis(r):
    n, k, P = test_case(r)
    tmpl = r.choice(TEST_CTX)
    sit, H, claim, opp, ev = tmpl[0].format(n=n, k=k), tmpl[1].format(), tmpl[2], tmpl[3], tmpl[4].format(k=k)
    cmp_ = "<" if P < Fraction(1, 20) else "\\geqq "
    Ps = r3(float(P))
    sig = P < Fraction(1, 20)
    R1 = f"仮説「{H}」のもとでは起こりにくいことが起こったので、「{claim}」と判断してよい"
    R2 = f"仮説「{H}」のもとでも起こりうることなので、「{claim}」とは判断できない"
    R3 = f"仮説「{H}」が正しいことが証明された"
    R4 = f"「{opp}」と判断してよい"
    right = R1 if sig else R2
    wrongs = [x for x in (R1, R2, R3, R4) if x != right]
    why = {R1: (f"確率約 ${Ps}$ は基準 $0.05$ 以上なので、めったに起こらないこととはいえない。", "基準との比較の誤り"),
           R2: (f"確率約 ${Ps}$ は基準 $0.05$ より小さいので、仮説のもとでは起こりにくいことが起こったと考える。", "基準との比較の誤り"),
           R3: ("仮説検定で仮説が正しいと証明されることはない。確率が基準以上のときは「誤りとは判断できない」だけである。", "判断できないことを証明と取り違える誤り"),
           R4: ("観察された結果は主張と同じ向きに偏っており、反対の向きの判断の根拠にはならない。", "検定の向きの取り違え")}
    return mc(f"{sit}（架空の設定）。「{claim}」と判断してよいかを、基準となる確率を $5\\%$ として考える。仮説「{H}」のもとで、{ev}確率は約 ${Ps}$ である。正しい判断を選びなさい。",
              [right] + wrongs, f"約 ${Ps}$ は $0.05$ {'より小さい' if sig else '以上'}。", d=3,
              ap="仮説のもとで実際の結果以上に偏る確率を、基準 $0.05$ と比べる。小さければ仮説は誤りと判断し、そうでなければ「判断できない」と結論する。",
              steps=[f"仮説：{H}。", f"仮説のもとで実際の結果以上に偏る確率：約 ${Ps}$。", f"${Ps}{cmp_}0.05$。", f"よって、{right}。"],
              alt=[f"確率の値は ${{}}_{{{n}}}\\mathrm{{C}}_{{{k}}}+\\cdots+{{}}_{{{n}}}\\mathrm{{C}}_{{{n}}}$ を $2^{{{n}}}$ で割って求められる（反復試行の確率）。"],
              pc=[("確率と基準を正しく比較している", 2), ("結論を正しい形（判断できる／できない）で選んでいる", 2)],
              why={w: why[w] for w in wrongs},
              chk=(f"floor(summation(binomial({n},t),(t,{k},{n}))/2**{n}*1000+Rational(1,2))/1000", Ps, None, "intermediate"))


@gen("standard_practice", 4, ["computation", "application"])
def combined(r):
    for _ in range(500):
        n1, n2 = r.randint(2, 10), r.randint(2, 10)
        m1, m2 = r.randint(40, 80), r.randint(40, 80)
        v1, v2 = r.randint(4, 40), r.randint(4, 40)
        N = n1 + n2
        if (n1 * m1 + n2 * m2) % N:
            continue
        M = (n1 * m1 + n2 * m2) // N
        sq = Fraction(n1 * (v1 + m1 * m1) + n2 * (v2 + m2 * m2), N)
        V = sq - M * M
        if V.denominator == 1:
            break
    ask = r.choice(["mean", "var", "var"])
    val = M if ask == "mean" else V
    return num(f"A 組 {n1} 人と B 組 {n2} 人の小テストの得点について、A 組の平均値は ${m1}$ 点、分散は ${v1}$、B 組の平均値は ${m2}$ 点、分散は ${v2}$ である（架空のデータ）。2つの組を合わせた {N} 人の得点の{'平均値' if ask == 'mean' else '分散'}を求めなさい。",
               fans(val), f"全体の平均値は ${M}$、全体の2乗の平均値は ${fnum(sq)}$ なので、分散は ${fnum(sq)}-{M}^2={fnum(V)}$。", d=4,
               ap="合計を使って全体の平均値を求める。分散は平均同士を合わせられないので、各組の「2乗の平均値」$\\overline{x^2}=s^2+(\\overline{x})^2$ を求めて全体の2乗の平均値をつくる。",
               steps=[f"得点の合計：${n1}\\times{m1}+{n2}\\times{m2}={n1 * m1 + n2 * m2}$、全体の平均値 ${M}$。",
                      f"各組の2乗の平均値：A 組 ${v1}+{m1}^2={v1 + m1 * m1}$、B 組 ${v2}+{m2}^2={v2 + m2 * m2}$。",
                      f"全体の2乗の平均値：$\\dfrac{{{n1}\\times{v1 + m1 * m1}+{n2}\\times{v2 + m2 * m2}}}{{{N}}}={fnum(sq)}$。", f"全体の分散：${fnum(sq)}-{M}^2={fnum(V)}$。"][: 1 if ask == "mean" else 4],
               alt=["全体の分散は「各組の分散の加重平均」と「各組の平均値の全体の平均値からのずれ」の和としても求められる：$\\dfrac{" + f"{n1}\\times{v1}+{n2}\\times{v2}" + "}{" + str(N) + "}+\\dfrac{" + f"{n1}({m1}-{M})^2+{n2}({m2}-{M})^2" + "}{" + str(N) + "}$。"],
               pc=[("全体の平均値を正しく求めている", 2), ("2乗の平均値を用いて正しく計算している", 2)],
               pit=["2つの組の平均値（分散）をそのまま平均してしまう（人数の違いを無視）。", "分散を合わせるときに平均値のずれを考えない。"],
               chk=(f"({n1}*{m1}+{n2}*{m2})/{N}" if ask == "mean" else f"({n1}*({v1}+{m1}**2)+{n2}*({v2}+{m2}**2))/{N}-(({n1}*{m1}+{n2}*{m2})/{N})**2", fans(val)))


# ======================================================================
# C 思考力・記述応用
# ======================================================================

@gen("thinking_writing", 3, ["written_reasoning", "concept"])
def var_proof(r):
    t = r.choice(["formula", "lin", "lin", "dev"])
    a, b = nonzero(r, -5, 6, exclude=(0, 1, -1)), r.randint(-9, 12)
    bt = "" if b == 0 else (f"+{b}" if b > 0 else f"{b}")
    if t == "formula":
        stem = "変量 $x$ のデータ $x_1,\\ x_2,\\ \\cdots,\\ x_n$ の平均値を $\\overline{x}$、分散を $s^2$ とする。$s^2=\\overline{x^2}-(\\overline{x})^2$ が成り立つことを証明しなさい。ただし、$\\overline{x^2}$ は $x_1^2,\\ x_2^2,\\ \\cdots,\\ x_n^2$ の平均値である。"
        steps = ["$s^2=\\dfrac{1}{n}\\sum_{k=1}^{n}(x_k-\\overline{x})^2$ の各項を展開する：$(x_k-\\overline{x})^2=x_k^2-2\\overline{x}x_k+(\\overline{x})^2$。",
                 "和をとって $n$ で割ると $s^2=\\dfrac{1}{n}\\sum x_k^2-2\\overline{x}\\cdot\\dfrac{1}{n}\\sum x_k+(\\overline{x})^2$。",
                 "$\\dfrac{1}{n}\\sum x_k^2=\\overline{x^2}$、$\\dfrac{1}{n}\\sum x_k=\\overline{x}$ を代入して $s^2=\\overline{x^2}-2(\\overline{x})^2+(\\overline{x})^2=\\overline{x^2}-(\\overline{x})^2$。"]
        chk = ("expand(variance([p, q, r]) - (mean([p**2, q**2, r**2]) - mean([p, q, r])**2))", "0", "expand", "intermediate")
        ans = "$s^2=\\overline{x^2}-(\\overline{x})^2$（証明は手順を参照）"
    elif t == "lin":
        stem = f"変量 $x$ のデータ $x_1,\\ x_2,\\ \\cdots,\\ x_n$ の平均値を $\\overline{{x}}$、標準偏差を $s_x$ とする。$y_k={a}x_k{bt}$（$k=1,\\ 2,\\ \\cdots,\\ n$）で定まる変量 $y$ の標準偏差 $s_y$ が $s_y={abs(a)}s_x$ となることを証明しなさい。"
        steps = [f"$\\overline{{y}}=\\dfrac{{1}}{{n}}\\sum({a}x_k{bt})={a}\\overline{{x}}{bt}$。", f"偏差は $y_k-\\overline{{y}}={a}(x_k-\\overline{{x}})$（定数 ${b}$ は打ち消し合う）。",
                 f"$s_y^2=\\dfrac{{1}}{{n}}\\sum\\{{{a}(x_k-\\overline{{x}})\\}}^2={a * a}\\cdot\\dfrac{{1}}{{n}}\\sum(x_k-\\overline{{x}})^2={a * a}s_x^2$。",
                 f"$s_y\\geqq0,\\ s_x\\geqq0$ なので、正の平方根をとって $s_y=\\sqrt{{{a * a}}}\\,s_x={abs(a)}s_x$。"]
        chk = (f"variance([{a}*1+({b}), {a}*4+({b}), {a}*7+({b})])-({a})**2*variance([1, 4, 7])", "0", None, "intermediate")
        ans = f"$s_y={abs(a)}s_x$（証明は手順を参照）"
    else:
        stem = f"変量 $x$ のデータ $x_1,\\ x_2,\\ \\cdots,\\ x_n$ の平均値を $\\overline{{x}}$ とする。偏差の和 $\\sum_{{k=1}}^{{n}}(x_k-\\overline{{x}})$ がつねに $0$ になることを証明し、このことから、散らばりの大きさを測るのに偏差をそのまま平均してはいけない理由を説明しなさい。"
        steps = ["$\\sum(x_k-\\overline{x})=\\sum x_k-n\\overline{x}$。", "$\\overline{x}=\\dfrac{1}{n}\\sum x_k$ より $n\\overline{x}=\\sum x_k$。よって和は $0$。",
                 "偏差の平均はどんなデータでも $0$ になり、散らばりの大小を区別できない。", "そこで偏差を2乗して正の量にしてから平均する（分散）。"]
        chk = ("expand((p-mean([p, q, r]))+(q-mean([p, q, r]))+(r-mean([p, q, r])))", "0", "expand", "intermediate")
        ans = "偏差の和は $0$（証明は手順を参照）。偏差の平均はつねに $0$ で散らばりを区別できないため。"
    return desc(stem, ans, "定義の式を展開し、平均値の定義 $\\overline{x}=\\dfrac{1}{n}\\sum x_k$ を使って整理する。",
                rubric=[("定義の式を正しく書き出している", 2), ("展開・整理の過程が正しい", 3), ("平均値の定義を用いて結論を導いている", 2), ("結論（または理由）を明確に述べている", 1)],
                d=4, p=8, lines=10, kind="proof",
                ap="分散・平均値の定義を $\\sum$ を用いた式で書き、和の性質（定数は和の外に出せる、定数の $n$ 個の和は $n$ 倍）を使って変形する。",
                steps=steps,
                alt=["$n=3$ などの具体的なデータで両辺を計算し、等しくなることを確かめてから一般の証明に進むとよい。"],
                pc=[("定義の式", 2), ("展開と整理", 3), ("平均値の定義の利用", 2), ("結論", 1)],
                pit=["$\\sum(\\overline{x})^2$ を $(\\overline{x})^2$ としてしまう（$n$ 個の和なので $n(\\overline{x})^2$）。", "標準偏差で絶対値（または正の平方根）の扱いを落とす。"],
                chk=chk)


TEST_CTX2 = [
    ("ある店で、新しいパン A と従来のパン B を {n} 人に食べ比べてもらったところ、{k} 人が A を選んだ", "A と B の好みに差はない", "A の方が好まれる"),
    ("ある生徒が、形が少しゆがんだコインを {n} 回投げたところ、表が {k} 回出た", "このコインは公正である", "このコインは表が出やすい"),
    ("ある植物の種を2つの方法 A, B で育てて {n} 組で比べたところ、{k} 組で A の方がよく育った", "育ち方に方法による差はない（どちらがよく育つ確率も $\\dfrac{1}{2}$）", "方法 A の方がよく育つ"),
]


@gen("thinking_writing", 3, ["written_reasoning", "application"])
def hyp_writing(r):
    n, k, P = test_case(r)
    sit, H, claim = r.choice(TEST_CTX2)
    sit = sit.format(n=n, k=k)
    Ps = r3(float(P))
    sig = P < Fraction(1, 20)
    cmp_ = "<" if sig else "\\geqq "
    concl = f"「{claim}」と判断してよい" if sig else f"「{claim}」とは判断できない"
    return desc(f"{sit}（架空の設定）。「{claim}」と判断してよいか、基準となる確率を $5\\%$ として、仮説検定の考え方を用いて説明しなさい。ただし、各回（各人・各組）の結果は互いに無関係とし、確率 $\\dfrac{{1}}{{2}}$ で起こることが {n} 回中 {k} 回以上起こる確率は約 ${Ps}$ であることを用いてよい。",
                f"仮説「{H}」を立てる。仮説のもとで {k} 回以上起こる確率は約 ${Ps}$ で、$0.05$ {'より小さい' if sig else '以上である'}。よって{concl}。",
                f"仮説のもとでの確率 ${Ps}$ を基準 $0.05$ と比べる。",
                rubric=[("主張に反する仮説を正しく立てている", 2), ("仮説のもとでの確率を示している", 2), ("確率と基準を正しく比較している", 2), ("結論を「判断してよい／できない」の形で正しく述べている", 2)],
                d=4, p=8, lines=8,
                ap="主張と反対の「差がない（確率 $\\dfrac{1}{2}$）」という仮説を立て、その仮説のもとで実際の結果以上に偏る確率を基準と比べる。",
                steps=[f"仮説：{H}。", f"仮説のもとで {k} 回以上となる確率は約 ${Ps}$。", f"${Ps}{cmp_}0.05$。",
                       ("仮説のもとではめったに起こらないことが起こったと考え、仮説は誤りと判断する。" if sig else "仮説のもとでも起こりうることなので、仮説が誤りとは判断できない。") + f"よって{concl}。"],
                alt=["シミュレーション（コインを" + str(n) + "回投げる実験を多数回くり返す）で、" + str(k) + "回以上となる相対度数を調べても、同じ判断ができる。"],
                pc=[("仮説の設定", 2), ("確率の提示", 2), ("基準との比較", 2), ("結論", 2)],
                pit=["確率が基準以上のときに「仮説は正しい」「差がないことが証明された」と書く。", f"「ちょうど {k} 回」の確率で判断してしまう。"],
                chk=(f"floor(summation(binomial({n},t),(t,{k},{n}))/2**{n}*1000+Rational(1,2))/1000", Ps, None, "intermediate"))


@gen("thinking_writing", 2, ["cross_unit", "application"], rel=["HS-MATH1-U03", "HS-MATHA-U01"])
def cross_unit(r):
    if r.random() < 0.55:
        n = r.choice([4, 5, 6])
        xs, m = nice_data(r, n, spread=5)
        v = var(xs)
        S = v * n
        return sa(f"データ {lst(xs)} に対して、$t$ の関数 $f(t)=" + "+".join(f"(t-{x})^2" for x in xs) + "$ を考える。$f(t)$ を最小にする $t$ の値と、そのときの最小値を求めなさい。また、その $t$ の値がデータの何であるかを答えなさい。",
                  f"$t={m}$ のとき最小値 ${fnum(S)}$。$t$ はデータの平均値", f"$f(t)={n}t^2-{2 * sum(xs)}t+{sum(x * x for x in xs)}$ を平方完成すると $f(t)={n}(t-{m})^2+{fnum(S)}$。", d=4, p=8,
                  ap="$f(t)$ は $t$ の二次関数（二次関数の単元）なので、展開して平方完成すれば最小値が分かる。結果をデータの分析の言葉（平均値・分散）で解釈する。",
                  steps=[f"展開：$f(t)={n}t^2-{2 * sum(xs)}t+{sum(x * x for x in xs)}$。", f"平方完成：$f(t)={n}(t-{m})^2+{fnum(S)}$。",
                         f"$t={m}$ のとき最小値 ${fnum(S)}$。", f"$t={m}$ はデータの平均値であり、最小値 ${fnum(S)}$ はデータの個数 ${n}$ と分散 ${fnum(v)}$ の積に等しい。"],
                  alt=[f"一般に $f(t)=\\sum(x_k-t)^2=n(t-\\overline{{x}})^2+ns^2$ と変形できるので、$t=\\overline{{x}}$ で最小値 $ns^2$ をとる。"],
                  pc=[("$f(t)$ を正しく展開している", 2), ("平方完成して最小値を求めている", 4), ("平均値であることを指摘している", 2)],
                  pit=["展開で $x^2$ の係数（データの個数）を 1 としてしまう。", "最小値を分散そのものと答える（個数倍になっている）。"],
                  chk=(f"[mean({pylist(xs)}), {len(xs)}*variance({pylist(xs)})]", f"[{m}, {fr_py(S.numerator, S.denominator)}]", None, "intermediate"))
    n = r.choice([5, 6, 7, 8])
    k = r.choice([n, n - 1])
    P = tail_prob(n, k)
    sig = P < Fraction(1, 20)
    terms_ = "+".join(f"{{}}_{{{n}}}\\mathrm{{C}}_{{{i}}}" for i in range(k, n + 1))
    return sa(f"あるコインを {n} 回投げたところ、表が {k} 回出た（架空の設定）。コインが公正である（表の出る確率が $\\dfrac{{1}}{{2}}$）と仮定したとき、表が {k} 回以上出る確率を、反復試行の確率を用いて分数で求めなさい。また、基準となる確率を $5\\%$ として、「このコインは表が出やすい」と判断してよいか答えなさい。",
              f"${frac(P.numerator, P.denominator)}$、" + ("判断してよい" if sig else "判断できない"),
              f"$\\dfrac{{{terms_}}}{{2^{{{n}}}}}={frac(P.numerator, P.denominator)}\\fallingdotseq{r3(float(P))}$。", d=4, p=8,
              ap="仮説のもとでの確率は、反復試行の確率 ${}_n\\mathrm{C}_r\\left(\\dfrac{1}{2}\\right)^n$（場合の数と確率の単元）で計算できる。それを基準 $0.05$ と比べる。",
              steps=[f"表が $r$ 回出る確率は ${{}}_{{{n}}}\\mathrm{{C}}_r\\left(\\dfrac{{1}}{{2}}\\right)^{{{n}}}$。", f"{k} 回以上：$\\dfrac{{{terms_}}}{{2^{{{n}}}}}=\\dfrac{{{sum(comb(n, i) for i in range(k, n + 1))}}}{{{2 ** n}}}" + ("" if P.denominator == 2 ** n else f"={frac(P.numerator, P.denominator)}") + "$。",
                     f"$\\fallingdotseq{r3(float(P))}$ は $0.05$ {'より小さい' if sig else '以上'}。", "よって" + ("表が出やすいと判断してよい。" if sig else "表が出やすいとは判断できない。")],
              alt=["表と裏の出方を樹形図で書き出し、全 $2^{" + str(n) + "}$ 通りのうち条件に合う場合を数えても同じ確率が得られる。"],
              pc=[("反復試行の確率の式を正しく立てている", 3), ("確率を正しく計算している", 3), ("基準と比べて正しく判断している", 2)],
              pit=["「ちょうど " + str(k) + " 回」の確率だけで判断する。", "確率が基準以上のとき「公正であると証明された」と書く。"],
              chk=(f"summation(binomial({n},t),(t,{k},{n}))/2**{n}", fr_py(P.numerator, P.denominator), None, "intermediate"))


@gen("thinking_writing", 2, ["written_reasoning", "condition_check"])
def corr_transform(r):
    rv = r.choice(RS)
    a, c = nonzero(r, -4, 5), nonzero(r, -4, 5)
    b, d = r.randint(-20, 20), r.randint(-20, 20)
    sgn = 1 if a * c > 0 else -1
    new = rv * sgn
    bt = "" if b == 0 else (f"+{b}" if b > 0 else f"{b}")
    dt = "" if d == 0 else (f"+{d}" if d > 0 else f"{d}")
    return desc(f"2つの変量 $x,\\ y$ の相関係数は ${fnum(rv)}$ である。変量 $u,\\ v$ を $u={co(a)}x{bt}$、$v={co(c)}y{dt}$ で定めるとき、$u$ と $v$ の相関係数を求め、その理由を説明しなさい。",
                f"${fnum(new)}$。共分散は ${a * c}$ 倍、標準偏差の積は ${abs(a * c)}$ 倍になるので、相関係数は ${'' if sgn > 0 else '-'}1$ 倍になる。",
                f"$s_{{uv}}={a * c}s_{{xy}}$、$s_us_v={abs(a * c)}s_xs_y$ より $r_{{uv}}={'' if sgn > 0 else '-'}r_{{xy}}$。",
                rubric=[("$u,\\ v$ の偏差を $x,\\ y$ の偏差で表している", 2), ("共分散が $" + str(a * c) + "$ 倍になることを示している", 2), ("標準偏差がそれぞれ $|a|,\\ |c|$ 倍になることを用いている", 2), ("相関係数を正しく求めている", 2)],
                d=4, p=8, lines=8,
                ap="偏差は $u_k-\\overline{u}=a(x_k-\\overline{x})$ のように、定数項が消えて係数倍になる。共分散と標準偏差がそれぞれ何倍になるかを調べる。",
                steps=[f"$u_k-\\overline{{u}}={co(a)}(x_k-\\overline{{x}})$、$v_k-\\overline{{v}}={co(c)}(y_k-\\overline{{y}})$。", f"共分散：$s_{{uv}}=({a})\\times({c})\\,s_{{xy}}={co(a * c)}s_{{xy}}$。",
                       f"標準偏差：$s_u={co(abs(a))}s_x$、$s_v={co(abs(c))}s_y$。", f"$r_{{uv}}=\\dfrac{{{co(a * c)}s_{{xy}}}}{{{co(abs(a * c))}s_xs_y}}={'' if sgn > 0 else '-'}r_{{xy}}={fnum(new)}$。"],
                alt=["散布図で考えると、正の数をかける・数を足す変換は点の並び方の傾向を変えず、負の数をかけると左右（または上下）が反転して傾向の向きが逆になる。"],
                pc=[("偏差の表現", 2), ("共分散", 2), ("標準偏差", 2), ("相関係数", 2)],
                pit=["相関係数も $" + str(a * c) + "$ 倍になると考える（標準偏差の積で割るので打ち消される）。", "負の係数のときに符号が変わることを見落とす。"],
                chk=(f"{fr_py(rv.numerator, rv.denominator)}*({a}*{c})/Abs({a}*{c})", fr_py(new.numerator, new.denominator), None, "intermediate"))


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(stem, wrong, step, etype, tempt, fix, ans, expl, steps, ap, alt, pit, chk=None, d=3):
    return desc(f"{stem}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい答えを求めなさい。", ans, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい解答を途中式とともに示している", 3), ("最終的な答えが正しい", 1)], d=d, p=6, lines=6,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい途中式", 3), ("正しい答え", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix), chk=chk)


@gen("error_correction", 3, ["common_error", "computation"])
def err_variance(r):
    for _ in range(300):
        xs, m = nice_data(r, 5, spread=5)
        v = var(xs)
        q2 = Fraction(sum(x * x for x in xs), 5)
        if v.denominator == 1 and v > 0:
            break
    if r.random() < 0.5:
        wrongv = q2 - m
        wrong = f"$x^2$ の平均値は ${fnum(q2)}$、平均値は ${m}$ なので、分散は ${fnum(q2)}-{m}={fnum(wrongv)}$"
        step, etype = "分散の計算公式の適用（平均値を2乗していない）", "formula"
        tempt = "公式 $s^2=\\overline{x^2}-(\\overline{x})^2$ の「平均値の2乗」を「平均値」と読み違えた。"
        fix = f"$s^2=\\overline{{x^2}}-(\\overline{{x}})^2={fnum(q2)}-{m}^2={fnum(v)}$"
    else:
        devs = [x - m for x in xs]
        wrong = f"平均値は ${m}$。偏差は {'，'.join(f'${d}$' for d in devs)} で、その平均値は $0$ なので、分散は $0$"
        step, etype = "偏差を2乗せずに平均した部分", "concept"
        tempt = "「偏差の平均」と「偏差の2乗の平均」を混同した。偏差の和がつねに $0$ になることに気づいていない。"
        fix = f"偏差の2乗の和は ${sum(d * d for d in devs)}$ なので、分散は $\\dfrac{{{sum(d * d for d in devs)}}}{{5}}={fnum(v)}$"
    return err_item(f"データ {lst(xs)} の分散を求めなさい。", wrong, step, etype, tempt, fix, f"${fnum(v)}$",
                    "分散は偏差の2乗の平均値であり、計算公式では $\\overline{x^2}$ から平均値の2乗を引く。",
                    [f"平均値 $\\overline{{x}}={m}$。", f"$\\overline{{x^2}}={fnum(q2)}$。", f"$s^2={fnum(q2)}-{m * m}={fnum(v)}$。"],
                    "定義（偏差の2乗の平均）と計算公式（2乗の平均 − 平均の2乗）を正確に区別する。",
                    ["定義と計算公式の両方で計算し、結果が一致するかで確かめる。", "分散が $0$ になるのは、すべての値が等しいときだけである。"],
                    ["$(\\overline{x})^2$ を $\\overline{x}$ とする。", "偏差を2乗し忘れる。"],
                    chk=(f"variance({pylist(xs)})", fans(v), None, "intermediate"), d=2)


@gen("error_correction", 3, ["common_error", "condition_check"])
def err_transform(r):
    m, s = r.randint(10, 60), r.randint(2, 9)
    a, b = nonzero(r, -5, 5, exclude=(0, 1, -1)), nonzero(r, -20, 20)
    bt = f"+{b}" if b > 0 else f"{b}"
    if r.random() < 0.5 or a > 0:
        wrong = f"$s_y={a}s_x{bt}={a * s + b}$"
        step = "標準偏差に $b$ を加え、係数をそのままかけた部分"
        tempt = "平均値の変換 $\\overline{y}=a\\overline{x}+b$ と同じ形で標準偏差も変換されると考えた。"
    else:
        wrong = f"$s_y={a}s_x={a * s}$"
        step = "係数 $a$ の絶対値をとっていない部分"
        tempt = "分散が $a^2$ 倍であることから、平方根をとるときに $\\sqrt{a^2}=a$ としてしまった。"
    val = abs(a) * s
    return err_item(f"変量 $x$ の平均値が ${m}$、標準偏差が $s_x={s}$ である。$y={a}x{bt}$ で定まる変量 $y$ の標準偏差 $s_y$ を求めなさい。", wrong, step, "formula", tempt,
                    f"$s_y=|{a}|s_x={abs(a)}\\times{s}={val}$", f"${val}$",
                    f"$y$ の偏差は ${a}(x_k-\\overline{{x}})$ となり $b$ は消える。分散は ${a * a}$ 倍、標準偏差は $|{a}|={abs(a)}$ 倍。",
                    [f"偏差：$y_k-\\overline{{y}}={a}(x_k-\\overline{{x}})$。", f"分散：$s_y^2=({a})^2s_x^2={a * a * s * s}$。", f"標準偏差：$s_y=\\sqrt{{{a * a * s * s}}}={val}$。"],
                    "平行移動（$+b$）は散らばりを変えない。標準偏差は $|a|$ 倍で、負になることはない。",
                    [f"$x$ が ${m - s},\\ {m + s}$ の2つの値だけのデータ（標準偏差 ${s}$）で $y$ を計算すると、$y$ の値の差の半分が ${val}$ になることで確かめられる。"],
                    ["標準偏差に $b$ を加える。", "標準偏差を負の値にする。"],
                    chk=(f"sqrt(({a})**2*{s}**2)", str(val), None, "intermediate"))


@gen("error_correction", 2, ["common_error", "computation"])
def err_median(r):
    n = r.choice([7, 8, 9])
    xs = r.sample(range(10, 60), n)
    def wrong_parts(v):
        wm = Fraction(v[n // 2]) if n % 2 else Fraction(v[n // 2 - 1] + v[n // 2], 2)
        return wm, median(v[: n // 2]), median(v[(n + 1) // 2:])
    while xs == sorted(xs) or wrong_parts(xs) == quartiles(xs)[1:2] + quartiles(xs)[0:1] + quartiles(xs)[2:3]:
        r.shuffle(xs)
    srt = sorted(xs)
    q1, q2, q3 = quartiles(xs)
    wrong_med = Fraction(xs[n // 2]) if n % 2 else Fraction(xs[n // 2 - 1] + xs[n // 2], 2)
    wq1 = median(xs[: n // 2])
    wq3 = median(xs[(n + 1) // 2:])
    wrong = f"中央値は真ん中の値なので ${fnum(wrong_med)}$。前半 {lst(xs[: n // 2])} の中央値 $Q_1={fnum(wq1)}$、後半 {lst(xs[(n + 1) // 2:])} の中央値 $Q_3={fnum(wq3)}$"
    return err_item(f"データ {lst(xs)} の中央値 $Q_2$ と、第1四分位数 $Q_1$、第3四分位数 $Q_3$ を求めなさい。", wrong, "データを小さい順に並べていない部分", "calculation",
                    "与えられた順番のまま「真ん中」をとった。中央値・四分位数は、大きさの順に並べたときの位置で決まることを忘れている。",
                    f"小さい順に並べて {lst(srt)}。$Q_2={fnum(q2)}$、$Q_1={fnum(q1)}$、$Q_3={fnum(q3)}$", f"$Q_1={fnum(q1)},\\ Q_2={fnum(q2)},\\ Q_3={fnum(q3)}$",
                    "中央値・四分位数は、データを大きさの順に並べてから求める。",
                    [f"小さい順に並べる：{lst(srt)}。", f"中央値 $Q_2={fnum(q2)}$。", f"前半 {lst(srt[: n // 2])}、後半 {lst(srt[(n + 1) // 2:])}。", f"$Q_1={fnum(q1)}$、$Q_3={fnum(q3)}$。"],
                    "代表値・四分位数を求める前に、必ずデータを大きさの順に並べる。",
                    ["求めた中央値より小さい値と大きい値の個数が等しいかを数えて確かめる。"],
                    ["並べ替えずに中央値をとる。"],
                    chk=(f"quartiles({pylist(xs)})", f"[{fr_py(q1.numerator, q1.denominator)}, {fr_py(q2.numerator, q2.denominator)}, {fr_py(q3.numerator, q3.denominator)}]", None, "intermediate"))


@gen("error_correction", 2, ["common_error", "concept"])
def err_interpret(r):
    t = r.choice(["cause", "weak", "proof"])
    if t == "cause":
        rv = r.choice(["0.82", "0.88", "0.91", "0.85"])
        ctx = r.choice([("ある市の各月のアイスクリームの売上", "その月の水難事故の件数", "気温（季節）"), ("各都市の消防署の数", "その都市の1年間の火災の件数", "都市の人口や面積"),
                        ("ある学校の生徒の靴のサイズ", "漢字テストの得点", "学年（年齢）")])
        stem = f"{ctx[0]} $x$ と{ctx[1]} $y$ の相関係数は ${rv}$ であった（架空のデータ）。このデータからいえることを答えなさい。"
        wrong = f"相関係数が ${rv}$ と $1$ に近いので、$x$ を減らせば $y$ も減らせる（$x$ が $y$ の原因である）"
        right = f"$x$ と $y$ には強い正の相関がある。ただし、因果関係があるとはいえない（{ctx[2]}のような共通の要因が両方に影響している可能性がある）"
        step, etype, tempt = "相関から因果関係を結論した部分", "interpretation", "相関係数が大きいと、一方が他方を引き起こしていると考えがちである。"
    elif t == "weak":
        rv = r.choice(["-0.83", "-0.9", "-0.87", "-0.94"])
        stem = f"ある地域で、標高 $x$（m）とその地点の気温 $y$（℃）を調べたところ、相関係数は ${rv}$ であった（架空のデータ）。$x$ と $y$ の相関について答えなさい。"
        wrong = f"相関係数が ${rv}$ で $0$ より小さいので、相関は弱い"
        right = "相関係数が $-1$ に近いので、強い負の相関がある（標高が高い地点ほど気温が低い傾向が強い）"
        step, etype, tempt = "相関係数の符号を強さと結びつけた部分", "interpretation", "負の値を「小さい＝弱い」と感じてしまい、強さは絶対値で判断することを忘れた。"
    else:
        rv = r.choice(["0.02", "-0.04", "0.05", "-0.01"])
        stem = f"ある2つの変量 $x,\\ y$ の相関係数は ${rv}$ であった（架空のデータ）。$x$ と $y$ の関係について答えなさい。"
        wrong = "相関係数がほぼ $0$ なので、$x$ と $y$ の間には何の関係もない"
        right = "直線的な相関はほとんどない。ただし、曲線的な関係など、直線的でない関係がある可能性は否定できない（散布図で確かめる必要がある）"
        step, etype, tempt = "「相関がない」を「関係がない」と言いかえた部分", "interpretation", "相関係数が直線的な関係の強さだけを表すことを意識していない。"
    return err_item(stem, wrong, step, etype, tempt, right, right,
                    "相関係数は直線的な関係の強さと向きを表す指標で、符号が向き、絶対値の大きさが強さを表す。因果関係や曲線的な関係は判断できない。",
                    ["相関係数の符号から相関の向きを読む。", "絶対値の大きさから相関の強さを読む。", "相関係数から言えないこと（因果関係・直線以外の関係）を区別する。"],
                    "相関係数から言えることと言えないことを区別する。強さは絶対値で判断する。",
                    ["散布図をかいて、点の並び方（直線的か、曲線的か、外れ値があるか）を確かめる。"],
                    ["相関と因果を混同する。", "負の相関を弱い相関と考える。"])


GENERATORS = [mean_var, quartile, transform, corr_meaning, corr_from_cov,
              var_formula, corr_calc, outlier, hypothesis, combined,
              var_proof, hyp_writing, cross_unit, corr_transform,
              err_variance, err_transform, err_median, err_interpret]
