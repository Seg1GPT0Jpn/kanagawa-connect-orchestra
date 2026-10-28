"""単元パック：共通テスト対策 数学Ⅱ・B・C（数列・統計的な推測・ベクトル）。"""
from decimal import ROUND_HALF_UP, Decimal
from fractions import Fraction as F

import sympy as sp

from banks._common import desc, mc, num, sa, table
from hs_pack_lib import board, check, definition, derivation, example, gen, guide, intro, lesson, poly, summary, theorem, tp

UNIT_ID = "CT-MATH2BC-U02"

PREREQUISITES = [
    ("HS-MATHB-U01", "等差・等比数列、階差数列、漸化式 $a_{n+1}=pa_n+q$ の解き方"),
    ("HS-MATHB-U02", "二項分布・正規分布と標準化、標本平均の分布、母平均・母比率の推定と仮説検定"),
    ("HS-MATHC-U01", "ベクトルの内積の定義と計算規則、成分による内積、位置ベクトル"),
    ("HS-MATHA-U01", "確率の計算（確率の漸化式で、次の状態への推移確率を立てるため）"),
]
EXTENSIONS = [
    ("SS-MATH-U02", "誘導つきで解いた確率・ベクトルの計算を、記述式の答案として論理的に書き切る"),
    ("SS-MATH-U01", "漸化式で求めた一般項を数学的帰納法で証明する論述へ発展する"),
    ("HS-MATH3-U01", "漸化式で定まる数列の極限（$n\\to\\infty$ でどの値に近づくか）を調べる"),
]


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


def dstr(v):
    """Decimal / Fraction（有限小数）を小数表記の文字列に。"""
    if isinstance(v, F):
        v = Decimal(v.numerator) / Decimal(v.denominator)
    s = format(v.normalize(), "f")
    return "0" if s in ("-0", "0") else s


def rnd(v, nd):
    if isinstance(v, F):
        v = Decimal(v.numerator) / Decimal(v.denominator)
    return str(Decimal(v).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP))


def pw(base, e="n-1"):
    """base^{e} の LaTeX（負・分数の底はかっこ）。"""
    b = F(base)
    bt = ft(b)
    if b < 0 or b.denominator != 1:
        bt = f"\\left({bt}\\right)"
    return f"{bt}^{{{e}}}"


def term_coef(c, body, first=True):
    """係数 c と本体 body の積（c=±1 は省略）。"""
    c = F(c)
    if c == 0:
        return ""
    mag = "" if abs(c) == 1 else ft(abs(c)) + "\\cdot "
    sign = "-" if c < 0 else ("" if first else "+")
    return f"{sign}{mag}{body}"


def cst(c):
    c = F(c)
    return "" if c == 0 else (f"+{ft(c)}" if c > 0 else f"-{ft(-c)}")


def vexpr(k, name="b"):
    """\\vec{a}+k\\vec{b} の LaTeX。"""
    if k == 1:
        return f"\\vec{{a}}+\\vec{{{name}}}"
    if k == -1:
        return f"\\vec{{a}}-\\vec{{{name}}}"
    return f"\\vec{{a}}{'+' if k > 0 else '-'}{abs(k)}\\vec{{{name}}}"


def sq(v):
    return sp.latex(sp.sqrt(sp.nsimplify(v)))


Z95 = Decimal("1.96")


# ----------------------------------------------------------------------
# 授業プリント
# ----------------------------------------------------------------------

LESSON = lesson(
    goals=["共通テストの選択問題（数列・統計的な推測・ベクトル）で、誘導の式変形の意図を読み取り、漸化式・推定・内積の典型処理を短時間で実行できる。",
           "漸化式 $a_{n+1}=pa_n+q$ の変形、信頼区間の式、$|\\vec{a}+t\\vec{b}|$ の最小値などの重要な結果を、導出の筋道とともに説明できる。",
           "指数のずれ・$\\sqrt{n}$ の位置・係数の2乗など、得点を落としやすい箇所を自分で点検できる。"],
    duration=100,
    readiness=["等比数列の一般項 $a_n=ar^{n-1}$ と、階差数列による一般項の求め方を使える。",
               "標準正規分布で $P(|Z|\\leqq1.96)=0.95$ であることを知っている。",
               "ベクトルの内積 $\\vec{a}\\cdot\\vec{b}=|\\vec{a}||\\vec{b}|\\cos\\theta$ と成分による計算ができる。"],
    flow=[("導入：選択問題の選び方と読み方", 10, "選択問題の構成と、誘導の「次に何を求めさせたいか」を予測する読み方を確認する"),
          ("漸化式", 25, "a_{n+1}=pa_n+q の変形の導出、確率の漸化式への応用（例題1）"),
          ("統計的な推測", 30, "標本平均の分布から信頼区間を導出し、母比率の推定を行う（例題2）。幅と標本の大きさの関係"),
          ("ベクトルの内積", 25, "|a+tb| の最小値と正射影。内積を求める3つの方法の使い分け（例題3）"),
          ("まとめと見直しの観点", 10, "典型的な失点と見直しの観点を確認し、問題プリントの課題を指示")],
    sections=[
        intro("in1", "選択問題は「型」と「誘導の意図」で解く",
              "共通テストの数学Ⅱ・B・C では、数学Ⅱの必答問題に加えて、数学B（数列、統計的な推測）と数学C（ベクトル、平面上の曲線と複素数平面）の内容から問題を選んで解答する。数列では漸化式の変形、統計的な推測では正規分布表を用いた推定・検定、ベクトルでは内積を使った長さ・角・垂直の処理が中心になる。どの分野も、誘導の式変形には「この形にすれば既に知っている型になる」という意図がある。",
              bullets=["誘導で「$b_n=a_n-\\alpha$ とおく」とあれば、$\\{b_n\\}$ は等比数列になる、と先に予測する。",
                       "統計の問題では、問題冊子に与えられる正規分布表と、$1.96$ などの値の使い方を確認しておく。",
                       "ベクトルでは、長さの条件は「2乗して内積で展開する」が基本方針である。"],
              points=[tp("どの選択問題を解くかは事前の演習で決めておき、本番で迷う時間をなくすよう指導する。", ask="自分が選ぶ分野と、その分野で最初に確認すべき条件は何か。", expect="例：統計なら正規分布表と信頼度、ベクトルなら与えられた長さと内積。", timing="導入の冒頭"),
                      tp("誘導文中の「〜とおく」「〜と変形できる」に下線を引かせ、変形後に何の型になるかを言わせる。", caution="誘導を無視して自己流で解くと、後の小問の誘導とつながらず時間を失う。")]),
        theorem("th1", "漸化式 $a_{n+1}=pa_n+q$ の解法",
                "$$a_{n+1}=pa_n+q\\ (p\\neq1)\\quad\\Longrightarrow\\quad a_n=(a_1-\\alpha)p^{n-1}+\\alpha\\qquad\\left(\\alpha=\\dfrac{q}{1-p}\\right)$$",
                ["$\\alpha$ は $\\alpha=p\\alpha+q$（特性方程式）の解。", "$p=1$ のときは等差数列。"],
                body="漸化式の両辺から同じ数 $\\alpha$ を引いて「等比数列の型」に直すことが本質である。$a_{n+1}=pa_n+r^n$ の型も、$c\\,r^n$ の形の数を引いて同じ型に直せる。",
                proof=["$\\alpha=p\\alpha+q$ を満たす $\\alpha$ をとり、漸化式から辺々引くと $a_{n+1}-\\alpha=p(a_n-\\alpha)$。",
                       "$b_n=a_n-\\alpha$ とおくと $b_{n+1}=pb_n$ なので、$\\{b_n\\}$ は初項 $b_1=a_1-\\alpha$、公比 $p$ の等比数列。",
                       "$b_n=(a_1-\\alpha)p^{n-1}$ より $a_n=(a_1-\\alpha)p^{n-1}+\\alpha$。"],
                points=[tp("答えを出したら $n=1,\\ 2$ を代入して漸化式と一致するか必ず確かめさせる。", ask="一般項に $n=1$ を代入すると何になるべきか。", expect="$a_1$ の値。", caution="指数を $p^n$ としてしまう誤りは $n=1$ の代入で発見できる。")]),
        derivation("dv1", "信頼度 95% の信頼区間の導出",
                   ["母平均 $m$、母標準偏差 $\\sigma$ の母集団から大きさ $n$ の無作為標本をとると、$n$ が大きいとき標本平均 $\\overline{X}$ は近似的に $N\\left(m,\\ \\dfrac{\\sigma^2}{n}\\right)$ に従う。",
                    "標準化 $Z=\\dfrac{\\overline{X}-m}{\\sigma/\\sqrt{n}}$ は近似的に $N(0,\\,1)$ に従い、$P(|Z|\\leqq1.96)=0.95$。",
                    "$|Z|\\leqq1.96$ を $m$ について解くと $\\overline{X}-1.96\\cdot\\dfrac{\\sigma}{\\sqrt{n}}\\leqq m\\leqq\\overline{X}+1.96\\cdot\\dfrac{\\sigma}{\\sqrt{n}}$。",
                    "母比率 $p$ の推定では、標本比率 $R$ を用いて、標準偏差を $\\sqrt{\\dfrac{R(1-R)}{n}}$ で近似する：$R-1.96\\sqrt{\\dfrac{R(1-R)}{n}}\\leqq p\\leqq R+1.96\\sqrt{\\dfrac{R(1-R)}{n}}$。",
                    "区間の幅は $\\dfrac{1}{\\sqrt{n}}$ に比例するので、幅を $\\dfrac{1}{k}$ にするには標本の大きさを $k^2$ 倍にする必要がある。"],
                   body="「信頼度 95%」とは、同じ方法で標本をとって区間を作ることを何度もくり返すと、そのうちのおよそ 95% の区間が母平均を含む、という意味である。",
                   points=[tp("$\\sigma$ と $\\dfrac{\\sigma}{\\sqrt{n}}$ の違い（個々のデータの散らばりと、標本平均の散らばり）を図で区別させる。", caution="$1.96\\sigma$ や $1.96\\cdot\\dfrac{\\sigma}{n}$ とする誤りが多い。")]),
        definition("df1", "ベクトルの内積と長さ",
                   "$\\vec{0}$ でない2つのベクトル $\\vec{a},\\ \\vec{b}$ のなす角を $\\theta\\ (0^\\circ\\leqq\\theta\\leqq180^\\circ)$ とするとき、内積を次で定める。成分が分かるときは成分で計算できる。",
                   formula="$$\\vec{a}\\cdot\\vec{b}=|\\vec{a}||\\vec{b}|\\cos\\theta=a_1b_1+a_2b_2,\\qquad |\\vec{a}+t\\vec{b}|^2=|\\vec{a}|^2+2t\\,\\vec{a}\\cdot\\vec{b}+t^2|\\vec{b}|^2$$",
                   conditions=["$\\vec{a}\\perp\\vec{b}\\iff\\vec{a}\\cdot\\vec{b}=0$（$\\vec{a},\\ \\vec{b}\\neq\\vec{0}$）。", "長さの条件は2乗して内積で展開する。係数も2乗されることに注意する。"],
                   points=[tp("内積を求める3つの方法（定義・成分・長さの条件から逆算）を表にし、与えられた情報で使い分けさせる。")]),
        theorem("th2", "$|\\vec{a}+t\\vec{b}|$ の最小値と正射影",
                "$$|\\vec{a}+t\\vec{b}|\\ \\text{は}\\ t=-\\dfrac{\\vec{a}\\cdot\\vec{b}}{|\\vec{b}|^2}\\ \\text{で最小},\\qquad \\text{最小値}=\\sqrt{|\\vec{a}|^2-\\dfrac{(\\vec{a}\\cdot\\vec{b})^2}{|\\vec{b}|^2}}$$",
                ["$\\vec{b}\\neq\\vec{0}$、$t$ は実数全体を動く。", "最小となるとき $(\\vec{a}+t\\vec{b})\\perp\\vec{b}$（垂線の足を考えることと同じ）。"],
                proof=["$f(t)=|\\vec{a}+t\\vec{b}|^2=|\\vec{b}|^2t^2+2(\\vec{a}\\cdot\\vec{b})t+|\\vec{a}|^2$ は $t$ の二次関数で、$|\\vec{b}|^2>0$ より下に凸。",
                       "平方完成すると $f(t)=|\\vec{b}|^2\\left(t+\\dfrac{\\vec{a}\\cdot\\vec{b}}{|\\vec{b}|^2}\\right)^2+|\\vec{a}|^2-\\dfrac{(\\vec{a}\\cdot\\vec{b})^2}{|\\vec{b}|^2}$。",
                       "$|\\vec{a}+t\\vec{b}|\\geqq0$ なので、$f(t)$ が最小のとき $|\\vec{a}+t\\vec{b}|$ も最小。",
                       "そのとき $(\\vec{a}+t\\vec{b})\\cdot\\vec{b}=\\vec{a}\\cdot\\vec{b}+t|\\vec{b}|^2=0$ となり、垂直であることがわかる。"],
                points=[tp("二次関数の最小値（数学Ⅰ）と図形の垂線の足が同じことを表している点を、図を使って説明する。", ask="最小になるとき、ベクトル $\\vec{a}+t\\vec{b}$ と $\\vec{b}$ はどんな位置関係か。", expect="垂直。")]),
        example("ex1", "例題1　漸化式の一般項",
                "$a_1=1,\\ a_{n+1}=3a_n+2$ で定められる数列 $\\{a_n\\}$ の一般項を求めよ。",
                ["$\\alpha=3\\alpha+2$ より $\\alpha=-1$。", "$a_{n+1}+1=3(a_n+1)$ と変形できる。", "$\\{a_n+1\\}$ は初項 $a_1+1=2$、公比 $3$ の等比数列なので $a_n+1=2\\cdot3^{n-1}$。"],
                "$a_n=2\\cdot3^{n-1}-1$",
                thinking="両辺から同じ数を引いて等比数列の型にする。引く数は特性方程式で求める。",
                points=[tp("$n=2$ を代入して $a_2=5$（漸化式から $3\\cdot1+2=5$）と一致することを確認させる。")],
                misconceptions=[("$a_n+1=2\\cdot3^{n}$ として $a_n=2\\cdot3^n-1$", "初項が第1項なので指数は $n-1$。$n=1$ を代入すると $a_1=5$ となり矛盾する")]),
        example("ex2", "例題2　母比率の推定",
                "ある市（架空）で無作為に選んだ 400 人のうち、80 人がある政策に賛成した。賛成者の母比率 $p$ に対する信頼度 95% の信頼区間を求めよ。",
                ["標本比率 $R=\\dfrac{80}{400}=0.2$。", "$\\sqrt{\\dfrac{R(1-R)}{n}}=\\sqrt{\\dfrac{0.2\\times0.8}{400}}=\\sqrt{0.0004}=0.02$。",
                 "$1.96\\times0.02=0.0392$ より $0.2-0.0392\\leqq p\\leqq0.2+0.0392$。"],
                "$0.1608\\leqq p\\leqq0.2392$",
                thinking="標本比率と標本の大きさから標準偏差を近似し、$\\pm1.96$ 倍の幅をとる。",
                points=[tp("標本の大きさを 4 倍の 1600 人にすると幅が半分になることを、その場で計算して確かめさせる。", ask="1600 人で同じ比率なら、区間の幅はどうなるか。", expect="$\\sqrt{4}=2$ で割られて半分になる。")]),
        example("ex3", "例題3　内積と長さの最小値",
                "$|\\vec{a}|=2,\\ |\\vec{b}|=3,\\ |\\vec{a}+\\vec{b}|=\\sqrt{19}$ のとき、$\\vec{a}\\cdot\\vec{b}$ となす角 $\\theta$ を求めよ。また、実数 $t$ に対して $|\\vec{a}+t\\vec{b}|$ の最小値を求めよ。",
                ["$|\\vec{a}+\\vec{b}|^2=|\\vec{a}|^2+2\\vec{a}\\cdot\\vec{b}+|\\vec{b}|^2$ より $19=4+2\\vec{a}\\cdot\\vec{b}+9$、$\\vec{a}\\cdot\\vec{b}=3$。",
                 "$\\cos\\theta=\\dfrac{3}{2\\cdot3}=\\dfrac{1}{2}$ より $\\theta=60^\\circ$。",
                 "$|\\vec{a}+t\\vec{b}|^2=9t^2+6t+4=9\\left(t+\\dfrac{1}{3}\\right)^2+3$。", "$t=-\\dfrac{1}{3}$ のとき最小値 $\\sqrt{3}$。"],
                "$\\vec{a}\\cdot\\vec{b}=3,\\ \\theta=60^\\circ$、最小値 $\\sqrt{3}$（$t=-\\dfrac{1}{3}$）",
                thinking="長さの条件は2乗して内積で展開する。$|\\vec{a}+t\\vec{b}|^2$ は $t$ の二次関数。",
                points=[tp("最後に2乗をはずして（平方根をとって）答えることを確認する。", caution="$|\\vec{a}+t\\vec{b}|^2$ の最小値 3 をそのまま答える誤り。")]),
        board("bd1", "板書案",
              [("① 漸化式", ["$a_{n+1}=pa_n+q$", "$\\alpha=p\\alpha+q$", "$a_{n+1}-\\alpha=p(a_n-\\alpha)$", "$a_n=(a_1-\\alpha)p^{n-1}+\\alpha$", "検算：$n=1,\\ 2$ を代入"]),
               ("② 推定", ["$\\overline{X}\\sim N\\left(m,\\ \\dfrac{\\sigma^2}{n}\\right)$（近似）", "$\\overline{X}\\pm1.96\\dfrac{\\sigma}{\\sqrt{n}}$", "$R\\pm1.96\\sqrt{\\dfrac{R(1-R)}{n}}$", "幅 $\\propto\\dfrac{1}{\\sqrt{n}}$"]),
               ("③ 内積", ["$\\vec{a}\\cdot\\vec{b}=|\\vec{a}||\\vec{b}|\\cos\\theta$", "長さは2乗して展開", "$|\\vec{a}+t\\vec{b}|^2$ は $t$ の二次関数", "最小 $\\iff(\\vec{a}+t\\vec{b})\\perp\\vec{b}$"])],
              points=[tp("各列の最後に「検算・確認の方法」を書き、問題演習で毎回参照させる。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("確率の漸化式では、「$n$ 回目の状態から $n+1$ 回目の状態への移り方」を樹形図や表に整理してから式を立てさせる。", timing="例題1の後"),
               tp("推定の答えは、区間の両端を計算した後、「標本の値が区間の中央にあるか」で検算させる。"),
               tp("仮説検定の結論は「棄却される → 〜でないといえる」「棄却されない → 〜でないとはいえない（判断できない）」と、言い回しまで正確に書かせる。", caution="棄却されないことを「仮説が正しいと証明された」と書く誤りが多い。"),
               tp("ベクトルの長さの問題では、係数つきの展開 $|\\vec{a}+k\\vec{b}|^2=|\\vec{a}|^2+2k\\vec{a}\\cdot\\vec{b}+k^2|\\vec{b}|^2$ を毎回書かせ、$k^2$ の付け忘れを防ぐ。"),
               tp("誤答訂正（問題プリントD）は、まず「どの行から誤っているか」だけを答えさせ、次に直させる2段階で扱う。")],
              misconceptions=[("$\\overline{X}$ の標準偏差は母標準偏差 $\\sigma$ と同じ", "標本平均の標準偏差は $\\dfrac{\\sigma}{\\sqrt{n}}$。$n$ が大きいほど小さい"),
                              ("信頼度 95% の信頼区間には、データの 95% が含まれる", "信頼区間は母平均（母比率）を推定する区間であり、個々のデータの分布の範囲ではない"),
                              ("$|\\vec{a}-2\\vec{b}|^2=|\\vec{a}|^2-4\\vec{a}\\cdot\\vec{b}+2|\\vec{b}|^2$", "係数も2乗され、$+4|\\vec{b}|^2$")]),
        summary("sm1", "まとめ",
                ["漸化式は「同じ数を引いて等比数列の型」にする。一般項は $n=1,\\ 2$ の代入で検算する。",
                 "信頼区間は $\\overline{X}\\pm1.96\\dfrac{\\sigma}{\\sqrt{n}}$、$R\\pm1.96\\sqrt{\\dfrac{R(1-R)}{n}}$。幅は $\\dfrac{1}{\\sqrt{n}}$ に比例する。",
                 "仮説検定の結論は「棄却される／されない」と、その意味を正確な言葉で述べる。",
                 "ベクトルの長さは2乗して内積で展開。$|\\vec{a}+t\\vec{b}|$ の最小は $t$ の二次関数の最小、図形的には垂線の足。"]),
        check("ck1", "確認問題",
              [("$a_1=4,\\ a_{n+1}=2a_n-3$ の一般項を求めよ。", "$a_{n+1}-3=2(a_n-3)$ より $a_n=2^{n-1}+3$"),
               ("母標準偏差 12 の母集団から大きさ 144 の標本をとり、標本平均が 50 であった。母平均の信頼度 95% の信頼区間を求めよ。", "$\\dfrac{12}{\\sqrt{144}}=1$ より $48.04\\leqq m\\leqq51.96$"),
               ("$|\\vec{a}|=1,\\ |\\vec{b}|=2,\\ \\vec{a}\\cdot\\vec{b}=-1$ のとき $|\\vec{a}+\\vec{b}|$ を求めよ。", "$1-2+4=3$ より $\\sqrt{3}$")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

def lin_seq(a1, p, q, n):
    a = F(a1)
    out = [a]
    for _ in range(n - 1):
        a = p * a + q
        out.append(a)
    return out


def an_tex(K, p, alpha, e="n-1"):
    return term_coef(K, pw(p, e)) + cst(alpha)


@gen("basic_check", 4, ["computation"])
def a_recur_linear(r):
    p = r.choice([2, 3, 4, -2, -3])
    alpha = r.randint(-4, 4)
    q = alpha * (1 - p)
    a1 = r.choice([x for x in range(-5, 7) if x != alpha])
    K = a1 - alpha
    vals = lin_seq(a1, p, q, 4)
    fexpr = lambda k: f"({K})*({p})**({k}-1)+({alpha})"  # noqa: E731
    ans = an_tex(K, p, alpha)
    sh = "a_n" if alpha == 0 else f"a_n{cst(-alpha)}"
    return sa(f"数列 $\\{{a_n\\}}$ は $a_1={a1},\\ a_{{n+1}}={p}a_n{cst(q)}$ を満たす。誘導に従い、この漸化式を $a_{{n+1}}-\\alpha={p}(a_n-\\alpha)$ と変形する。定数 $\\alpha$ の値と、一般項 $a_n$ を求めなさい。",
              f"$\\alpha={alpha}$、$a_n={ans}$",
              f"$\\alpha={p}\\alpha{cst(q)}$ より $\\alpha={alpha}$。$\\{{{sh}\\}}$ は初項 ${K}$、公比 ${p}$ の等比数列。", d=2,
              v=[f"a_n={ans}"],
              ap="定数 $\\alpha$ を引くと等比数列の型になる。$\\alpha$ は漸化式の $a_{n+1},\\ a_n$ を $\\alpha$ でおきかえた方程式（特性方程式）の解。",
              steps=[f"$\\alpha={p}\\alpha{cst(q)}$ を解いて $\\alpha={alpha}$。", f"$b_n=a_n-({alpha})$ とおくと $b_{{n+1}}={p}b_n$、$b_1={a1}-({alpha})={K}$。",
                     f"$b_n={term_coef(K, pw(p))}$ より $a_n={ans}$。"],
              alt=[f"検算：$n=1$ で ${ans.replace('n-1', '0')}$ を計算すると ${a1}$、$n=2$ では漸化式から ${vals[1]}$ になることを確かめる。"],
              pc=[("$\\alpha$ を正しく求めている", 1), ("一般項を正しく求めている", 1)],
              pit=["指数を $n$ として、$n=1$ で $a_1$ にならない式を答える。", "初項を $a_1$ のまま（$a_1-\\alpha$ にせず）等比数列の初項にする。"],
              chk=(f"[{', '.join(fexpr(k) for k in range(1, 5))}]", f"[{', '.join(fp(v) for v in vals)}]", None, "intermediate"))


@gen("basic_check", 3, ["computation", "condition_check"])
def a_diff_recur(r):
    b = r.choice([2, 4, -2, 6])
    c = r.randint(-3, 4)
    d = r.randint(-3, 5)
    A, B, C = b // 2, c - b // 2, d - c
    ans = poly(A, B, C, var="n")
    return sa(f"数列 $\\{{a_n\\}}$ は $a_1={d}$、$a_{{n+1}}-a_n={poly(b, c, var='n')}$ を満たす。一般項 $a_n$ を求めなさい。（$n\\geqq2$ で求めた式が $n=1$ でも成り立つかを確認すること。）",
              f"$a_n={ans}$",
              f"$n\\geqq2$ のとき $a_n={d}+\\displaystyle\\sum_{{k=1}}^{{n-1}}({poly(b, c, var='k')})={ans}$。$n=1$ のとき ${d}$ となり成り立つ。", d=2, v=[f"a_n={ans}"],
              ap="$a_{n+1}-a_n=b_n$ の形は階差数列の型。$a_n=a_1+\\displaystyle\\sum_{k=1}^{n-1}b_k$ は $n\\geqq2$ でしか使えないので、最後に $n=1$ を確認する。",
              steps=[f"$n\\geqq2$ のとき $a_n={d}+\\displaystyle\\sum_{{k=1}}^{{n-1}}({poly(b, c, var='k')})$。",
                     f"$\\displaystyle\\sum_{{k=1}}^{{n-1}}k=\\dfrac{{(n-1)n}}{{2}}$ を用いて計算すると $a_n={ans}$。",
                     f"$n=1$ を代入すると ${A + B + C}={d}$ となり、$n=1$ でも成り立つ。"],
              alt=[f"$a_2={d + b + c}$ を漸化式から直接求め、求めた式に $n=2$ を代入した値と一致することを確かめる。"],
              pc=[("$\\Sigma$ の上端を $n-1$ として正しく計算している", 1), ("$n=1$ の確認をして一般項を答えている", 1)],
              pit=["$\\Sigma$ の上端を $n$ にしてしまう。", "$n\\geqq2$ の条件を書かず、$n=1$ の確認も忘れる。"],
              chk=(f"expand({d}+summation({b}*k+({c}), [k, 1, n-1]))", f"({A})*n**2+({B})*n+({C})", "expand"))


POPS = [("ある地域（架空）の高校生の1日の学習時間（分）", "分"), ("ある工場（架空）で作られる製品の重さ（g）", "g"),
        ("ある果樹園（架空）でとれる果実の糖度（度）", "度"), ("ある市（架空）の世帯の1か月の水道使用量（$\\mathrm{m}^3$）", "")]


@gen("basic_check", 3, ["concept", "computation"])
def a_sample_dist(r):
    ctx, _ = r.choice(POPS)
    m = r.choice([20, 45, 60, 80, 120, 150, 200])
    rn = r.choice([5, 6, 8, 10, 12, 15, 20])
    n = rn * rn
    sig = r.choice([s for s in (6, 8, 10, 12, 15, 20, 24, 30) if s != rn])
    var = F(sig * sig, n)
    right = f"$N\\left({m},\\ {ft(var)}\\right)$"
    w1 = f"$N\\left({m},\\ {sig * sig}\\right)$"
    w2 = f"$N\\left({m},\\ {ft(F(sig, rn))}\\right)$"
    w3 = f"$N\\left({m * n},\\ {sig * sig * n}\\right)$"
    if len({right, w1, w2, w3}) < 4:
        w2 = f"$N\\left({m},\\ {ft(F(sig * sig, rn))}\\right)$"
    return mc(f"{ctx}の分布は、母平均 ${m}$、母標準偏差 ${sig}$ である。この母集団から大きさ ${n}$ の無作為標本を抽出するとき、標本平均 $\\overline{{X}}$ が近似的に従う分布として正しいものを選びなさい。",
              [right, w1, w2, w3], f"$E(\\overline{{X}})={m}$、$V(\\overline{{X}})=\\dfrac{{{sig}^2}}{{{n}}}={ft(var)}$。$n$ が大きいので近似的に正規分布 $N\\left({m},\\ {ft(var)}\\right)$ に従う。", d=2,
              ap="標本平均の期待値は母平均と同じ、分散は母分散の $\\dfrac{1}{n}$。$N(m,\\,\\sigma^2)$ の2番目は「分散」であることに注意する。",
              steps=[f"$E(\\overline{{X}})=m={m}$。", f"$V(\\overline{{X}})=\\dfrac{{\\sigma^2}}{{n}}=\\dfrac{{{sig * sig}}}{{{n}}}={ft(var)}$。", f"よって $N\\left({m},\\ {ft(var)}\\right)$。"],
              alt=[f"標準偏差 $\\sigma(\\overline{{X}})=\\dfrac{{{sig}}}{{\\sqrt{{{n}}}}}={ft(F(sig, rn))}$ を求め、それを2乗して分散 ${ft(var)}$ になることを確かめる。"],
              pc=[("期待値を正しく判断している", 1), ("分散 $\\dfrac{\\sigma^2}{n}$ を正しく計算している", 1)],
              why={w1: ("母集団の分布をそのまま答えている。標本平均は個々のデータより散らばりが小さく、分散は $\\dfrac{1}{n}$ になる。", "母分散と標本平均の分散の混同"),
                   w2: (f"標準偏差 $\\dfrac{{\\sigma}}{{\\sqrt{{n}}}}={ft(F(sig, rn))}$ を分散の位置に書いている。$N(m,\\,\\sigma^2)$ の2番目は分散である。", "標準偏差と分散の混同"),
                   w3: ("標本の合計 $X_1+\\cdots+X_n$ の分布（期待値 $nm$、分散 $n\\sigma^2$）である。平均はさらに $n$ で割る。", "標本の和と標本平均の混同")})


@gen("basic_check", 3, ["computation"])
def a_ci_mean(r):
    ctx, unit = r.choice(POPS)
    rn = r.choice([8, 10, 12, 15, 16, 20, 25, 30])
    while True:
        sig = r.randint(4, 40)
        sd = F(sig, rn)
        if (sd * 100).denominator == 1:
            break
    n = rn * rn
    xbar = Decimal(r.randint(200, 1500)) / 10
    h = Z95 * Decimal(sd.numerator) / Decimal(sd.denominator)
    lo, hi = xbar - h, xbar + h
    return sa(f"{ctx}について母平均 $m$ を推定するため、大きさ ${n}$ の無作為標本を抽出したところ、標本平均は ${dstr(xbar)}$ であった。母標準偏差を ${sig}$ として、$m$ に対する信頼度 95% の信頼区間を求めなさい。",
              f"${dstr(lo)}\\leqq m\\leqq{dstr(hi)}$",
              f"$1.96\\times\\dfrac{{{sig}}}{{\\sqrt{{{n}}}}}=1.96\\times{dstr(sd)}={dstr(h)}$ より、${dstr(xbar)}\\pm{dstr(h)}$。", d=2,
              ap="信頼区間は $\\overline{X}-1.96\\dfrac{\\sigma}{\\sqrt{n}}\\leqq m\\leqq\\overline{X}+1.96\\dfrac{\\sigma}{\\sqrt{n}}$。まず $\\dfrac{\\sigma}{\\sqrt{n}}$ を計算する。",
              steps=[f"$\\dfrac{{\\sigma}}{{\\sqrt{{n}}}}=\\dfrac{{{sig}}}{{{rn}}}={dstr(sd)}$。", f"$1.96\\times{dstr(sd)}={dstr(h)}$。", f"${dstr(xbar)}-{dstr(h)}\\leqq m\\leqq{dstr(xbar)}+{dstr(h)}$。"],
              alt=["求めた区間の中央（両端の平均）が標本平均に一致し、幅が $2\\times1.96\\dfrac{\\sigma}{\\sqrt{n}}$ になっていることを確かめる。"],
              pc=[("$\\dfrac{\\sigma}{\\sqrt{n}}$ を正しく計算している", 1), ("信頼区間を正しく答えている", 1)],
              pit=["$\\sqrt{n}$ で割らずに $1.96\\sigma$ を使う。", "$n$ で割ってしまう。"],
              chk=(f"[{dstr(xbar)}-1.96*{sig}/sqrt({n}), {dstr(xbar)}+1.96*{sig}/sqrt({n})]", f"[{dstr(lo)}, {dstr(hi)}]", None, "intermediate"))


@gen("basic_check", 4, ["computation", "concept"])
def a_dot_from_norm(r):
    A, B = r.randint(1, 5), r.randint(1, 5)
    th = r.choice([60, 90, 120])
    k = r.choice([1, -1, 2, -2, 3])
    cosv = {60: F(1, 2), 90: F(0), 120: F(-1, 2)}[th]
    D = A * B * cosv
    L2 = A * A + 2 * k * D + k * k * B * B
    if L2 <= 0:
        k = 1
        L2 = A * A + 2 * D + B * B
    return sa(f"2つのベクトル $\\vec{{a}},\\ \\vec{{b}}$ が $|\\vec{{a}}|={A},\\ |\\vec{{b}}|={B},\\ |{vexpr(k)}|={sq(L2)}$ を満たしている。内積 $\\vec{{a}}\\cdot\\vec{{b}}$ と、$\\vec{{a}},\\ \\vec{{b}}$ のなす角 $\\theta\\ (0^\\circ\\leqq\\theta\\leqq180^\\circ)$ を求めなさい。",
              f"$\\vec{{a}}\\cdot\\vec{{b}}={ft(D)}$、$\\theta={th}^\\circ$",
              f"$|{vexpr(k)}|^2=|\\vec{{a}}|^2{'+' if k > 0 else '-'}{2 * abs(k)}\\vec{{a}}\\cdot\\vec{{b}}+{k * k if k * k != 1 else ''}|\\vec{{b}}|^2$ に代入して $\\vec{{a}}\\cdot\\vec{{b}}={ft(D)}$。$\\cos\\theta={ft(cosv)}$。", d=2,
              ap="長さの条件は2乗して内積で展開すると、内積についての一次方程式になる。",
              steps=[f"$|{vexpr(k)}|^2={A * A}{'+' if k > 0 else '-'}{2 * abs(k)}\\vec{{a}}\\cdot\\vec{{b}}+{k * k * B * B}={L2}$。",
                     f"$\\vec{{a}}\\cdot\\vec{{b}}={ft(D)}$。", f"$\\cos\\theta=\\dfrac{{{ft(D)}}}{{{A}\\cdot{B}}}={ft(cosv)}$ より $\\theta={th}^\\circ$。"],
              alt=[f"$\\theta={th}^\\circ$ から逆に $|{vexpr(k)}|^2$ を計算し、${L2}$ になることを確かめる。"],
              pc=[("2乗して内積で展開し、内積を求めている", 1), ("なす角を正しく求めている", 1)],
              pit=[f"展開で $|\\vec{{b}}|^2$ の係数 ${k * k}$（係数の2乗）を付け忘れる。", "$|" + vexpr(k) + "|$ を2乗せずに $|\\vec{a}|" + ("+" if k > 0 else "-") + "|\\vec{b}|$ のように計算する。"],
              chk=(f"(({L2})-({A})**2-({k})**2*({B})**2)/(2*({k}))", fp(D), None, "intermediate"))


@gen("basic_check", 3, ["concept"])
def a_ci_width(r):
    k = r.choice([2, 3, 4, 5, 10])
    kind = r.choice(["mean", "prop"])
    what = "母平均" if kind == "mean" else "母比率"
    form = r.choice(["need", "effect"])
    if form == "need":
        stem = f"{what}を信頼度 95% で推定する。標本の大きさを $n$ としたときの信頼区間の幅を、ほかの条件を変えずに $\\dfrac{{1}}{{{k}}}$ にしたい。標本の大きさを何倍にすればよいか。"
        right, w1, w2, w3 = f"${k * k}$ 倍", f"${k}$ 倍", f"$\\sqrt{{{k}}}$ 倍", f"$\\dfrac{{1}}{{{k * k}}}$ 倍"
        why = {w1: ("幅は $\\dfrac{1}{\\sqrt{n}}$ に比例し、$\\dfrac{1}{n}$ には比例しない。$n$ を " + f"${k}$" + " 倍にしても幅は $\\dfrac{1}{\\sqrt{" + f"{k}" + "}}$ にしかならない。", "幅が $n$ に反比例するという誤解"),
               w2: ("$\\sqrt{n}$ を " + f"${k}$" + " 倍にするには、$n$ を " + f"${k}^2$" + " 倍にする必要がある。$n$ と $\\sqrt{n}$ を取り違えている。", "根号の処理の誤り"),
               w3: ("標本を小さくすると幅は広がる。増減の向きが逆である。", "標本の大きさと精度の関係の逆転")}
        expl = f"幅は $\\dfrac{{1}}{{\\sqrt{{n}}}}$ に比例する。$\\dfrac{{1}}{{\\sqrt{{cn}}}}=\\dfrac{{1}}{{{k}}}\\cdot\\dfrac{{1}}{{\\sqrt{{n}}}}$ より $\\sqrt{{c}}={k}$、$c={k * k}$。"
        chk = (f"({k})**2", str(k * k), None, "intermediate")
    else:
        c = k * k
        stem = f"{what}を信頼度 95% で推定する。ほかの条件を変えずに標本の大きさを ${c}$ 倍にすると、信頼区間の幅はおよそ何倍になるか。"
        right, w1, w2, w3 = f"$\\dfrac{{1}}{{{k}}}$ 倍", f"$\\dfrac{{1}}{{{c}}}$ 倍", f"${k}$ 倍", f"${c}$ 倍"
        why = {w1: ("幅は $\\dfrac{1}{\\sqrt{n}}$ に比例するので、$\\dfrac{1}{" + f"{c}" + "}$ ではなく $\\dfrac{1}{\\sqrt{" + f"{c}" + "}}$ 倍になる。", "幅が $n$ に反比例するという誤解"),
               w2: ("標本を大きくすると推定の精度が上がり、幅は狭くなる。広くなるとするのは向きが逆である。", "標本の大きさと精度の関係の逆転"),
               w3: ("標本の大きさに比例して幅が広がると考えている。幅は狭くなり、しかも $\\sqrt{n}$ に反比例する。", "標本の大きさと精度の関係の逆転")}
        expl = f"幅は $\\dfrac{{1}}{{\\sqrt{{n}}}}$ に比例するので、$\\dfrac{{1}}{{\\sqrt{{{c}}}}}=\\dfrac{{1}}{{{k}}}$ 倍。"
        chk = (f"1/sqrt({c})", f"Rational(1,{k})", None, "intermediate")
    return mc(stem, [right, w1, w2, w3], expl, d=2,
              ap="信頼区間の幅は $2\\times1.96\\times\\dfrac{\\sigma}{\\sqrt{n}}$（母比率なら $\\sigma$ の代わりに $\\sqrt{R(1-R)}$）なので、$\\dfrac{1}{\\sqrt{n}}$ に比例する。",
              steps=["幅 $=2\\times1.96\\times\\dfrac{(\\text{母標準偏差など})}{\\sqrt{n}}$ と書き、$n$ 以外は変わらないことを確認する。", expl],
              alt=["具体的な数（例：$n=100$ と $n=400$）で幅を計算し、比を確かめる。"],
              pc=[("幅が $\\dfrac{1}{\\sqrt{n}}$ に比例することを用いている", 1), ("正しい倍率を選んでいる", 1)],
              why=why, chk=chk)


# ======================================================================
# B 標準演習
# ======================================================================

EXP_PAIRS = [(2, 3), (3, 2), (3, 4), (4, 3), (4, 5), (5, 4)]


@gen("standard_practice", 3, ["computation"])
def b_recur_exp(r):
    p, q = r.choice(EXP_PAIRS)
    c = F(1, q - p)
    a1 = r.choice([x for x in range(-4, 7) if x != c * q])
    K = a1 - c * q
    vals = [F(a1)]
    for nn in range(1, 4):
        vals.append(p * vals[-1] + F(q) ** nn)
    ans = term_coef(K, pw(p)) + ("+" if c > 0 else "-") + f"{q}^n"
    fexpr = lambda k: f"({fp(K)})*({p})**({k}-1)+({fp(c)})*({q})**({k})"  # noqa: E731
    return sa(f"数列 $\\{{a_n\\}}$ は $a_1={a1},\\ a_{{n+1}}={p}a_n+{q}^n$ を満たす。定数 $c$ を用いて、この漸化式は $a_{{n+1}}-c\\cdot{q}^{{n+1}}={p}\\left(a_n-c\\cdot{q}^n\\right)$ と変形できる。$c$ の値と一般項 $a_n$ を求めなさい。",
              f"$c={ft(c)}$、$a_n={ans}$",
              f"$c\\cdot{q}^{{n+1}}-{p}c\\cdot{q}^n={q}^n$ より $c({q}-{p})=1$、$c={ft(c)}$。$\\{{a_n-({ft(c)})\\cdot{q}^n\\}}$ は初項 ${ft(K)}$、公比 ${p}$ の等比数列。", d=3,
              ap="誘導の変形式を展開して元の漸化式と係数を比べれば $c$ が決まる。その後は $b_n=a_n-c\\cdot" + f"{q}" + "^n$ が等比数列になる。",
              steps=[f"変形式を展開すると $a_{{n+1}}={p}a_n+c({q}-{p})\\cdot{q}^n$。元の式と比べて $c({q}-{p})=1$、$c={ft(c)}$。",
                     f"$b_n=a_n-({ft(c)})\\cdot{q}^n$ とおくと $b_{{n+1}}={p}b_n$、$b_1={a1}-({ft(c * q)})={ft(K)}$。",
                     f"$b_n={term_coef(K, pw(p))}$ より $a_n={ans}$。"],
              alt=[f"両辺を ${q}^{{n+1}}$ で割り、$d_n=\\dfrac{{a_n}}{{{q}^n}}$ とおくと $d_{{n+1}}=\\dfrac{{{p}}}{{{q}}}d_n+\\dfrac{{1}}{{{q}}}$ となり、$pa_n+q$ 型に帰着して同じ結果が得られる。"],
              pc=[("$c$ を正しく求めている", 1), ("等比数列の初項・公比を正しく求めている", 1), ("一般項を正しく答えている", 2)],
              pit=["$b_1$ を求めるとき $c\\cdot" + f"{q}" + "^1$ を引き忘れる。", "指数を $n$ と $n-1$ で取り違える（$n=1$ で検算する）。"],
              chk=(f"[{', '.join(fexpr(k) for k in range(1, 5))}]", f"[{', '.join(fp(v) for v in vals)}]", None, "intermediate"))


MODEL_C = {F(1, 2): [20, 40, 60, 100, 120], F(1, 3): [20, 40, 60, 100, 120], F(1, 4): [30, 60, 90, 120]}


@gen("standard_practice", 3, ["application", "computation"])
def b_recur_model(r):
    p = r.choice(list(MODEL_C))
    c = r.choice(MODEL_C[p])
    T = r.choice([10, 20, 50, 100])
    L = F(c) / (1 - p)
    thr = L * (1 - F(1, T))
    nmin = 1
    while p ** nmin >= F(1, T):
        nmin += 1
    vals = lin_seq(c, p, c, 4)
    ans = f"{ft(L)}-{ft(L)}\\cdot{pw(p, 'n')}"
    return sa(f"ある薬（架空）を毎朝 ${c}$ mg ずつ服用する。体内に残る薬の量は、1日たつと服用直後の ${ft(p)}$ 倍になるものとする。$n$ 回目に服用した直後の体内の量を $a_n$ mg とする（$a_1={c}$）。\n(1) $a_{{n+1}}$ を $a_n$ で表し、一般項 $a_n$ を求めなさい。\n(2) $a_n>{dstr(thr)}$ となる最小の自然数 $n$ を求めなさい。",
              f"(1) $a_{{n+1}}={ft(p)}a_n+{c}$、$a_n={ans}$　(2) $n={nmin}$",
              f"$\\alpha={ft(p)}\\alpha+{c}$ より $\\alpha={ft(L)}$。$a_n-{ft(L)}=({c}-{ft(L)})\\cdot{pw(p)}$。", d=3,
              ap="「前日の量の一定倍＋毎日の追加量」は $a_{n+1}=pa_n+q$ 型の漸化式になる。$\\alpha$ は量が変化しなくなる値（つり合いの値）である。",
              steps=[f"$a_{{n+1}}={ft(p)}a_n+{c}$。", f"$\\alpha={ft(p)}\\alpha+{c}$ より $\\alpha={ft(L)}$。",
                     f"$a_n-{ft(L)}=({c}-{ft(L)})\\cdot{pw(p)}=-{ft(L)}\\cdot{pw(p, 'n')}$ より $a_n={ans}$。",
                     f"(2) $a_n>{dstr(thr)}\\iff {ft(L)}\\cdot{pw(p, 'n')}<{dstr(L / T)}\\iff {pw(p, 'n')}<\\dfrac{{1}}{{{T}}}$。",
                     f"${pw(p, str(nmin - 1))}={ft(p ** (nmin - 1))}\\geqq\\dfrac{{1}}{{{T}}}$、${pw(p, str(nmin))}={ft(p ** nmin)}<\\dfrac{{1}}{{{T}}}$ より $n={nmin}$。"],
              alt=[f"$a_1,\\ a_2,\\ a_3,\\ \\cdots$ を漸化式から順に計算すると ${', '.join(ft(v) for v in vals)},\\ \\cdots$ となり、一般項の式と一致することを確かめられる。"],
              pc=[("漸化式を正しく立てている", 1), ("一般項を正しく求めている", 2), ("(2) の最小の $n$ を正しく求めている", 1)],
              pit=["$a_1$ が「1回目の服用直後」であることを読み落とし、$a_0$ から始める。", "$\\left(" + ft(p) + "\\right)^n$ と $\\left(" + ft(p) + "\\right)^{n-1}$ を取り違える。"],
              chk=(f"[{', '.join(f'{fp(L)}-{fp(L)}*({fp(p)})**{k}' for k in range(1, 5))}]", f"[{', '.join(fp(v) for v in vals)}]", None, "intermediate"))


def prop_cases():
    out = []
    for R in (F(1, 10), F(1, 5), F(9, 25), F(1, 2), F(16, 25), F(4, 5), F(9, 10)):
        for sd in (F(1, 100), F(1, 50), F(1, 40), F(1, 25), F(1, 20), F(3, 200)):
            n = R * (1 - R) / (sd * sd)
            if n.denominator == 1 and 100 <= n <= 10000 and (R * n).denominator == 1:
                out.append((R, int(n), sd))
    return out


PROP_CASES = prop_cases()
PROP_CTX = ["ある市（架空）で無作為に選んだ {n} 人に調査したところ、{k} 人がある公共施設を利用したことがあると答えた",
            "ある工場（架空）の製品から無作為に {n} 個を取り出して検査したところ、{k} 個が規格の上限に近い値であった",
            "ある高校（架空）の卒業生から無作為に {n} 人を選んだところ、{k} 人が理系の学部に進学していた",
            "ある湖（架空）で無作為に {n} 匹の魚を捕獲したところ、{k} 匹が特定の種類であった"]


@gen("standard_practice", 4, ["computation", "condition_check"])
def b_ci_prop(r):
    R, n, sd = r.choice(PROP_CASES)
    k = int(R * n)
    ctx = r.choice(PROP_CTX).format(n=n, k=k)
    Rd = Decimal(R.numerator) / Decimal(R.denominator)
    sdd = Decimal(sd.numerator) / Decimal(sd.denominator)
    h = Z95 * sdd
    lo, hi = Rd - h, Rd + h
    return sa(f"{ctx}。その性質をもつものの母比率 $p$ に対する信頼度 95% の信頼区間を求めなさい。答えは小数第4位を四捨五入して小数第3位まで求めること。",
              f"${rnd(lo, 3)}\\leqq p\\leqq{rnd(hi, 3)}$",
              f"標本比率 $R={dstr(Rd)}$、$\\sqrt{{\\dfrac{{R(1-R)}}{{n}}}}={dstr(sdd)}$。$1.96\\times{dstr(sdd)}={dstr(h)}$ より ${dstr(lo)}\\leqq p\\leqq{dstr(hi)}$。", d=3,
              ap="母比率の推定では、標本の大きさ $n$ が大きいとき、標本比率 $R$ を使って標準偏差を $\\sqrt{\\dfrac{R(1-R)}{n}}$ と近似し、$R\\pm1.96\\times$（標準偏差）の区間をつくる。",
              steps=[f"$R=\\dfrac{{{k}}}{{{n}}}={dstr(Rd)}$。", f"$\\sqrt{{\\dfrac{{{dstr(Rd)}\\times{dstr(1 - Rd)}}}{{{n}}}}}={dstr(sdd)}$。",
                     f"$1.96\\times{dstr(sdd)}={dstr(h)}$。", f"${dstr(lo)}\\leqq p\\leqq{dstr(hi)}$ を四捨五入して ${rnd(lo, 3)}\\leqq p\\leqq{rnd(hi, 3)}$。"],
              alt=["区間の中央が標本比率 $R$ に一致すること、幅が $2\\times1.96\\sqrt{\\dfrac{R(1-R)}{n}}$ になっていることを確かめる。"],
              pc=[("標本比率と標準偏差を正しく求めている", 1), ("$\\pm1.96$ 倍の区間をつくっている", 1), ("指示どおりに四捨五入して答えている", 2)],
              pit=["$\\sqrt{\\ }$ をとり忘れて $\\dfrac{R(1-R)}{n}$ をそのまま使う。", "四捨五入を途中で行い、端の値がずれる。"],
              chk=(f"[{k}/{n}-1.96*sqrt(({k}/{n})*(1-{k}/{n})/{n}), {k}/{n}+1.96*sqrt(({k}/{n})*(1-{k}/{n})/{n})]", f"[{dstr(lo)}, {dstr(hi)}]", None, "intermediate"))


@gen("standard_practice", 3, ["application", "computation"])
def b_sample_size(r):
    while True:
        R = r.choice([Decimal("0.1"), Decimal("0.2"), Decimal("0.3"), Decimal("0.4"), Decimal("0.5")])
        e = r.choice([Decimal("0.01"), Decimal("0.02"), Decimal("0.025"), Decimal("0.03"), Decimal("0.04"), Decimal("0.05")])
        val = Z95 * Z95 * R * (1 - R) / (e * e)
        if val != val.to_integral_value():
            break
    nmin = int(val) + 1
    W = 2 * e
    return num(f"ある調査（架空）で母比率 $p$ を信頼度 95% で推定したい。過去の調査から標本比率はおよそ ${dstr(R)}$ と見込まれる。信頼区間の幅（上端と下端の差）を ${dstr(W)}$ 以下にするには、標本の大きさ $n$ を少なくともいくつにすればよいか。標本比率は ${dstr(R)}$ になるものとして求めなさい。",
               str(nmin), f"幅 $2\\times1.96\\sqrt{{\\dfrac{{{dstr(R)}\\times{dstr(1 - R)}}}{{n}}}}\\leqq{dstr(W)}$ を解いて $n\\geqq{dstr(val)}$。", d=3,
               ap="信頼区間の幅を $n$ の式で表し、「幅 $\\leqq$ 目標値」という不等式を $n$ について解く。$n$ は自然数なので最後に切り上げる。",
               steps=[f"幅 $=2\\times1.96\\sqrt{{\\dfrac{{{dstr(R * (1 - R))}}}{{n}}}}$。", f"$1.96\\sqrt{{\\dfrac{{{dstr(R * (1 - R))}}}{{n}}}}\\leqq{dstr(e)}$ の両辺を2乗して $n\\geqq\\dfrac{{1.96^2\\times{dstr(R * (1 - R))}}}{{{dstr(e)}^2}}={dstr(val)}$。",
                      f"これを満たす最小の自然数は $n={nmin}$。"],
               alt=[f"$n={nmin - 1}$ と $n={nmin}$ でそれぞれ幅を計算し、${dstr(W)}$ を超えるか超えないかを確かめる。"],
               pc=[("幅を $n$ の式で表している", 1), ("不等式を正しく解いている", 2), ("切り上げて最小の自然数を答えている", 1)],
               pit=["幅（全体）と片側の幅を取り違え、目標値をそのまま $1.96\\sqrt{\\cdots}$ と比べる。", "小数のまま答えたり、切り捨てたりする。"],
               chk=(f"ceiling(1.96**2*{dstr(R)}*(1-{dstr(R)})/{dstr(e)}**2)", str(nmin)))


@gen("standard_practice", 3, ["computation", "concept"])
def b_dot_projection(r):
    while True:
        a1, a2 = r.randint(-4, 5), r.randint(-4, 5)
        b1, b2 = r.randint(-4, 5), r.randint(-4, 5)
        if (a1, a2) == (0, 0):
            continue
        dot = a1 * b1 + a2 * b2
        if dot == 0 or a1 * b2 - a2 * b1 == 0:
            continue
        break
    n2 = a1 * a1 + a2 * a2
    k = F(dot, n2)
    Hx, Hy = k * a1, k * a2
    return sa(f"座標平面上に原点 O と2点 $\\mathrm{{A}}({a1},\\,{a2})$、$\\mathrm{{B}}({b1},\\,{b2})$ がある。点 B から直線 OA に下ろした垂線と直線 OA の交点を H とする。$\\overrightarrow{{\\mathrm{{OH}}}}=k\\overrightarrow{{\\mathrm{{OA}}}}$ とおくとき、$k$ の値と点 H の座標を求めなさい。",
              f"$k={ft(k)}$、$\\mathrm{{H}}\\left({ft(Hx)},\\,{ft(Hy)}\\right)$",
              f"$\\overrightarrow{{\\mathrm{{BH}}}}\\cdot\\overrightarrow{{\\mathrm{{OA}}}}=0$ より $k|\\overrightarrow{{\\mathrm{{OA}}}}|^2=\\overrightarrow{{\\mathrm{{OA}}}}\\cdot\\overrightarrow{{\\mathrm{{OB}}}}$、$k=\\dfrac{{{dot}}}{{{n2}}}$。", d=3,
              ap="垂直の条件は内積 $=0$ で表す。$\\overrightarrow{\\mathrm{BH}}=k\\overrightarrow{\\mathrm{OA}}-\\overrightarrow{\\mathrm{OB}}$ と OA が垂直、という式を立てる。",
              steps=[f"$\\overrightarrow{{\\mathrm{{OA}}}}\\cdot\\overrightarrow{{\\mathrm{{OB}}}}={a1}\\cdot({b1})+{a2}\\cdot({b2})={dot}$、$|\\overrightarrow{{\\mathrm{{OA}}}}|^2={n2}$。",
                     "$(k\\overrightarrow{\\mathrm{OA}}-\\overrightarrow{\\mathrm{OB}})\\cdot\\overrightarrow{\\mathrm{OA}}=0$ より $k|\\overrightarrow{\\mathrm{OA}}|^2-\\overrightarrow{\\mathrm{OA}}\\cdot\\overrightarrow{\\mathrm{OB}}=0$。",
                     f"$k=\\dfrac{{{dot}}}{{{n2}}}={ft(k)}$、$\\mathrm{{H}}\\left({ft(Hx)},\\,{ft(Hy)}\\right)$。"],
              alt=["直線 OA の方程式と、B を通り OA に垂直な直線の方程式を連立して交点を求めても同じ結果になる（図形と方程式）。"],
              pc=[("垂直条件を内積で表している", 1), ("内積と大きさを正しく計算している", 1), ("$k$ と H の座標を正しく答えている", 2)],
              pit=["$k=\\dfrac{\\overrightarrow{\\mathrm{OA}}\\cdot\\overrightarrow{\\mathrm{OB}}}{|\\overrightarrow{\\mathrm{OA}}|}$ と、分母を2乗し忘れる。", "垂直なベクトルの組を取り違える（$\\overrightarrow{\\mathrm{BH}}$ と $\\overrightarrow{\\mathrm{OB}}$ など）。"],
              chk=(f"[{fp(Hx)}, {fp(Hy)}, (({b1})-({fp(Hx)}))*({a1})+(({b2})-({fp(Hy)}))*({a2})]", f"[({dot})*({a1})/({n2}), ({dot})*({a2})/({n2}), 0]", None, "intermediate"))


@gen("standard_practice", 4, ["computation", "condition_check"])
def b_dot_min(r):
    while True:
        A, B = r.randint(1, 5), r.randint(1, 5)
        D = r.randint(-A * B + 1, A * B - 1)
        if D != 0:
            break
    t0 = F(-D, B * B)
    m2 = F(A * A) - F(D * D, B * B)
    mv = sp.sqrt(sp.Rational(m2.numerator, m2.denominator))
    return sa(f"ベクトル $\\vec{{a}},\\ \\vec{{b}}$ が $|\\vec{{a}}|={A},\\ |\\vec{{b}}|={B},\\ \\vec{{a}}\\cdot\\vec{{b}}={D}$ を満たしている。実数 $t$ を変化させるとき、$|\\vec{{a}}+t\\vec{{b}}|$ の最小値と、そのときの $t$ の値を求めなさい。",
              f"$t={ft(t0)}$ のとき最小値 ${sp.latex(mv)}$",
              f"$|\\vec{{a}}+t\\vec{{b}}|^2={B * B}t^2{'+' if D > 0 else '-'}{2 * abs(D)}t+{A * A}$ は $t={ft(t0)}$ で最小値 ${ft(m2)}$。", d=3,
              ap="$|\\vec{a}+t\\vec{b}|$ は根号を含むので、2乗した $|\\vec{a}+t\\vec{b}|^2$ を $t$ の二次関数として最小化する（長さは0以上なので、2乗が最小のとき長さも最小）。",
              steps=[f"$|\\vec{{a}}+t\\vec{{b}}|^2=|\\vec{{b}}|^2t^2+2(\\vec{{a}}\\cdot\\vec{{b}})t+|\\vec{{a}}|^2={B * B}t^2{'+' if D > 0 else '-'}{2 * abs(D)}t+{A * A}$。",
                     f"平方完成：${B * B}\\left(t{'+' if D > 0 else '-'}{ft(abs(t0))}\\right)^2+{ft(m2)}$。".replace("\\left(t+0\\right)", "t"),
                     f"$t={ft(t0)}$ のとき $|\\vec{{a}}+t\\vec{{b}}|^2$ の最小値 ${ft(m2)}$、よって最小値 ${sp.latex(mv)}$。"],
              alt=[f"最小となるのは $(\\vec{{a}}+t\\vec{{b}})\\perp\\vec{{b}}$ のときなので、$(\\vec{{a}}+t\\vec{{b}})\\cdot\\vec{{b}}={D}+{B * B}t=0$ から $t={ft(t0)}$ と求めてもよい。"],
              pc=[("2乗して $t$ の二次関数で表している", 1), ("平方完成して最小となる $t$ を求めている", 1), ("平方根をとって最小値を答えている", 2)],
              pit=["2乗の最小値 " + f"${ft(m2)}$" + " をそのまま答える。", "$2\\vec{a}\\cdot\\vec{b}$ の係数 2 を落とす。"],
              chk=(f"[-({D})/({B})**2, sqrt(({A})**2-({D})**2/({B})**2)]", f"[{fp(t0)}, {mv}]", None, "intermediate"))


# ======================================================================
# C 思考力・記述応用
# ======================================================================

@gen("thinking_writing", 3, ["cross_unit", "written_reasoning"], rel=["HS-MATHA-U02", "HS-MATHC-U01"])
def c_orthocenter(r):
    while True:
        A, B = r.randint(2, 6), r.randint(2, 6)
        D = r.randint(1, A * B - 1)
        A2, B2 = A * A, B * B
        AB2 = A2 + B2 - 2 * D
        if AB2 > 0 and D != A2 and D != B2:
            break
    det = D * D - A2 * B2
    s = F(D * (D - B2), det)
    t = F(D * (D - A2), det)
    oh = term_coef(s, "\\vec{a}") + term_coef(t, "\\vec{b}", first=(s == 0))
    return desc(f"$\\triangle\\mathrm{{OAB}}$ において $\\mathrm{{OA}}={A},\\ \\mathrm{{OB}}={B},\\ \\mathrm{{AB}}={sq(AB2)}$ である。$\\overrightarrow{{\\mathrm{{OA}}}}=\\vec{{a}},\\ \\overrightarrow{{\\mathrm{{OB}}}}=\\vec{{b}}$ とし、$\\triangle\\mathrm{{OAB}}$ の垂心を H とする。\n(1) 内積 $\\vec{{a}}\\cdot\\vec{{b}}$ を求めなさい。\n(2) $\\overrightarrow{{\\mathrm{{OH}}}}=s\\vec{{a}}+t\\vec{{b}}$ と表すとき、$s,\\ t$ の値を求めなさい。垂心の性質をどのように式にしたかがわかるように記述すること。",
                f"(1) $\\vec{{a}}\\cdot\\vec{{b}}={D}$　(2) $s={ft(s)},\\ t={ft(t)}$（$\\overrightarrow{{\\mathrm{{OH}}}}={oh}$）",
                f"$\\mathrm{{AB}}^2=|\\vec{{b}}-\\vec{{a}}|^2$ から内積を求める。垂心は $\\mathrm{{AH}}\\perp\\mathrm{{OB}}$、$\\mathrm{{BH}}\\perp\\mathrm{{OA}}$ を満たす。",
                [("$|\\vec{b}-\\vec{a}|^2$ を展開して内積を正しく求めている", 2), ("垂心の条件を2つの内積の式で表している", 3), ("連立方程式を解いて $s,\\ t$ を正しく求めている", 3)], d=4, p=8, lines=12,
                ap="垂心は「各頂点から対辺に下ろした垂線の交点」（数学A 図形の性質）。2本の垂線について「垂直 ⇔ 内積 $=0$」を使えば、$s,\\ t$ の連立方程式になる。",
                steps=[f"(1) $|\\vec{{b}}-\\vec{{a}}|^2=|\\vec{{b}}|^2-2\\vec{{a}}\\cdot\\vec{{b}}+|\\vec{{a}}|^2$ より ${AB2}={B2}-2\\vec{{a}}\\cdot\\vec{{b}}+{A2}$、$\\vec{{a}}\\cdot\\vec{{b}}={D}$。",
                       f"(2) $\\mathrm{{AH}}\\perp\\mathrm{{OB}}$：$(s\\vec{{a}}+t\\vec{{b}}-\\vec{{a}})\\cdot\\vec{{b}}=0$ より ${D}s+{B2}t={D}$。",
                       f"$\\mathrm{{BH}}\\perp\\mathrm{{OA}}$：$(s\\vec{{a}}+t\\vec{{b}}-\\vec{{b}})\\cdot\\vec{{a}}=0$ より ${A2}s+{D}t={D}$。",
                       f"連立して $s={ft(s)},\\ t={ft(t)}$。"],
                alt=[f"求めた $\\overrightarrow{{\\mathrm{{OH}}}}$ について、3本目の垂線の条件 $\\overrightarrow{{\\mathrm{{OH}}}}\\cdot(\\vec{{b}}-\\vec{{a}})=0$ も成り立つことを確かめると検算になる（垂心では3本の垂線が1点で交わる）。"],
                pc=[("内積の計算", 2), ("垂直条件の立式", 3), ("連立方程式の解", 3)],
                pit=["$|\\vec{b}-\\vec{a}|^2$ の展開で $-2\\vec{a}\\cdot\\vec{b}$ の符号を誤る。", "垂直にすべきベクトルの組を取り違える（$\\overrightarrow{\\mathrm{AH}}$ と $\\overrightarrow{\\mathrm{OA}}$ など）。"],
                chk=(f"[({fp(s)})*({D})+({fp(t)})*({B2})-({D}), ({fp(s)})*({A2})+({fp(t)})*({D})-({D})]", "[0, 0]", None, "intermediate"))


PROBS = [F(1, 2), F(1, 3), F(2, 3), F(1, 4), F(3, 4), F(1, 5), F(2, 5), F(3, 5)]


@gen("thinking_writing", 3, ["cross_unit", "written_reasoning"], rel=["HS-MATHA-U01", "HS-MATHB-U01"])
def c_prob_recur(r):
    kind = r.choice(["weather", "walk"])
    if kind == "weather":
        a, b = r.sample(PROBS, 2)
        rr = a - b
        alpha = b / (1 - rr)
        K = 1 - alpha
        p1 = F(1)
        stem = (f"ある地域の天気を、次のような（架空の）モデルで考える。晴れの日の翌日が晴れである確率は ${ft(a)}$、晴れでない日の翌日が晴れである確率は ${ft(b)}$ とする。1日目は晴れであった。$n$ 日目が晴れである確率を $p_n$ とする（$p_1=1$）。\n"
                "(1) $p_{n+1}$ を $p_n$ で表しなさい。\n(2) $p_n$ を $n$ の式で表しなさい。考え方がわかるように記述すること。")
        rec = f"p_{{n+1}}={ft(a)}p_n+{ft(b)}(1-p_n)={ft(rr)}p_n{cst(b)}".replace("=1p_n", "=p_n").replace("=-1p_n", "=-p_n")
        rec_reason = f"$n+1$ 日目が晴れになるのは、「$n$ 日目が晴れ（確率 $p_n$）で翌日も晴れ」か「$n$ 日目が晴れでない（確率 $1-p_n$）で翌日が晴れ」のどちらかで、これらは互いに排反。"
        e = "n-1"
        seq = [p1]
        for _ in range(3):
            seq.append(rr * seq[-1] + b)
        fexpr = lambda k: f"({fp(alpha)})+({fp(K)})*({fp(rr)})**({k}-1)"  # noqa: E731
    else:
        kk = r.choice([3, 4, 5, 6])
        shape_ = {3: "正三角形 ABC の頂点", 4: "正四面体 ABCD の頂点", 5: "正五角形の5つの頂点", 6: "正六角形の6つの頂点"}[kk]
        rr = F(-1, kk - 1)
        alpha = F(1, kk)
        K = 1 - alpha
        a = rr
        b = F(1, kk - 1)
        stem = (f"点 P は{shape_}の上を動く。P は最初頂点 A にあり、1秒ごとに、今いる頂点以外の {kk - 1} つの頂点のいずれかに等しい確率 ${ft(F(1, kk - 1))}$ で移動する。$n$ 秒後に P が頂点 A にある確率を $p_n$ とする（$p_0=1$）。\n"
                "(1) $p_{n+1}$ を $p_n$ で表しなさい。\n(2) $p_n$ を $n$ の式で表しなさい。考え方がわかるように記述すること。")
        rec = f"p_{{n+1}}={ft(F(1, kk - 1))}(1-p_n)={ft(rr)}p_n+{ft(b)}"
        rec_reason = f"$n+1$ 秒後に A にあるのは、$n$ 秒後に A 以外の頂点（確率 $1-p_n$）にいて、そこから A へ移動する（確率 ${ft(F(1, kk - 1))}$）場合に限る。"
        e = "n"
        seq = [F(1)]
        for _ in range(3):
            seq.append(rr * seq[-1] + b)
        fexpr = lambda k: f"({fp(alpha)})+({fp(K)})*({fp(rr)})**({k}-1)"  # noqa: E731
    start = 1
    pn = f"{ft(alpha)}{'+' if K > 0 else '-'}{ft(abs(K))}{pw(rr, e)}"
    if kind == "walk":
        fexpr = lambda k: f"({fp(alpha)})+({fp(K)})*({fp(rr)})**({k})"  # noqa: E731
        start = 0
    return desc(stem, f"(1) ${rec}$　(2) $p_n={pn}$",
                f"{rec_reason}特性方程式 $\\alpha={ft(rr)}\\alpha{cst(b)}$ より $\\alpha={ft(alpha)}$。",
                [("排反な場合に分けて漸化式を正しく立てている", 3), ("$\\alpha$ を引いて等比数列の型に直している", 2), ("初項（$p_" + str(start) + "$）と指数に注意して $p_n$ を正しく求めている", 3)], d=4, p=8, lines=12,
                ap="確率の漸化式は「$n$ 回目の状態で場合分けし、$n+1$ 回目に注目する状態になる確率を足す」（数学A の確率）。得られた式は $p_{n+1}=rp_n+q$ 型（数学B の数列）。",
                steps=[rec_reason, f"よって ${rec}$。", f"$\\alpha={ft(rr)}\\alpha{cst(b)}$ を解いて $\\alpha={ft(alpha)}$。$p_{{n+1}}-{ft(alpha)}={ft(rr)}\\left(p_n-{ft(alpha)}\\right)$。",
                       f"$\\{{p_n-{ft(alpha)}\\}}$ は初項 $p_{start}-{ft(alpha)}={ft(K)}$、公比 ${ft(rr)}$ の等比数列。", f"$p_n={pn}$。"],
                alt=[f"$p_{start + 1},\\ p_{start + 2}$ を問題の状況から直接計算すると ${ft(seq[1])},\\ {ft(seq[2])}$ で、求めた式と一致することを確かめる。"],
                pc=[("漸化式", 3), ("等比数列への変形", 2), ("一般項", 3)],
                pit=["$n$ 回目が注目する状態「でない」場合の確率 $1-p_n$ を考え忘れる。", f"初項が $p_{start}$ であるのに、指数を {'$n$' if start == 1 else '$n-1$'} としてしまう。"],
                chk=(f"[{', '.join(fexpr(k) for k in range(start, start + 4))}]", f"[{', '.join(fp(v) for v in seq)}]", None, "intermediate"))


@gen("thinking_writing", 2, ["written_reasoning", "concept"])
def c_ci_interpret(r):
    cases = [(R, n, sd) for R, n, sd in PROP_CASES if any(R2 == R and n2 == 4 * n for R2, n2, _ in PROP_CASES)]
    R, n, sd = r.choice(cases)
    n2 = 4 * n
    sd2 = sd / 2
    Rd = Decimal(R.numerator) / Decimal(R.denominator)
    h1 = Z95 * Decimal(sd.numerator) / Decimal(sd.denominator)
    h2 = h1 / 2
    who = r.choice(["太郎さんと花子さん", "AさんとBさん", "2つの調査会社（架空）"])
    return desc(f"ある意見に賛成する人の母比率 $p$ を調べるため、{who}がそれぞれ無作為抽出による調査を行った。一方は ${n}$ 人、もう一方は ${n2}$ 人を調べ、どちらも標本比率は ${dstr(Rd)}$ であった。\n(1) それぞれについて、$p$ に対する信頼度 95% の信頼区間を求めなさい。\n(2) 2つの区間の幅の比を求め、そうなる理由を説明しなさい。また、「信頼度 95%」の意味を説明しなさい。",
                f"(1) ${n}$ 人：${dstr(Rd - h1)}\\leqq p\\leqq{dstr(Rd + h1)}$、${n2}$ 人：${dstr(Rd - h2)}\\leqq p\\leqq{dstr(Rd + h2)}$　(2) 幅の比は $2:1$。幅は $\\dfrac{{1}}{{\\sqrt{{n}}}}$ に比例し、$\\sqrt{{4}}=2$ だから。信頼度 95% とは、同じ方法で標本をとり区間をつくることをくり返すと、そのうちおよそ 95% の区間が $p$ を含むという意味。",
                f"標準偏差は ${dstr(Decimal(sd.numerator) / Decimal(sd.denominator))}$ と ${dstr(Decimal(sd2.numerator) / Decimal(sd2.denominator))}$。",
                [("2つの信頼区間を正しく求めている", 3), ("幅の比を求め、$\\dfrac{1}{\\sqrt{n}}$ に比例することから理由を説明している", 3), ("信頼度 95% の意味を正しく説明している", 2)], d=4, p=8, lines=12,
                ap="母比率の信頼区間 $R\\pm1.96\\sqrt{\\dfrac{R(1-R)}{n}}$ の式を見ると、標本比率が同じなら幅を決めるのは $\\sqrt{n}$ だけである。",
                steps=[f"${n}$ 人：$\\sqrt{{\\dfrac{{{dstr(Rd)}\\times{dstr(1 - Rd)}}}{{{n}}}}}={dstr(Decimal(sd.numerator) / Decimal(sd.denominator))}$、$1.96$ 倍して ${dstr(h1)}$。",
                       f"${n2}$ 人：標準偏差は $\\dfrac{{1}}{{\\sqrt{{4}}}}$ 倍の ${dstr(Decimal(sd2.numerator) / Decimal(sd2.denominator))}$、$1.96$ 倍して ${dstr(h2)}$。",
                       "幅の比は $2\\times" + dstr(h1) + ":2\\times" + dstr(h2) + "=2:1$。", "信頼度の意味：区間をつくる方法の信頼性を表す。1つの区間についての確率ではなく、くり返したときの割合として述べる。"],
                alt=["幅の式 $2\\times1.96\\sqrt{\\dfrac{R(1-R)}{n}}$ に $n$ と $4n$ を代入して比をとると、$\\sqrt{\\dfrac{4n}{n}}=2$ が直接得られる。"],
                pc=[("2つの区間", 3), ("幅の比と理由", 3), ("信頼度の意味", 2)],
                pit=["標本の大きさが4倍なので幅も $\\dfrac{1}{4}$ になると考える。", "「データの 95% がこの区間に入る」と説明してしまう。"],
                chk=(f"(2*1.96*sqrt(({fp(R)})*(1-{fp(R)})/{n}))/(2*1.96*sqrt(({fp(R)})*(1-{fp(R)})/{n2}))", "2", None, "intermediate"))


TEST_CASES = [(400, F(1, 5), 8), (625, F(1, 5), 10), (900, F(1, 2), 15), (400, F(1, 2), 10), (1600, F(1, 5), 16), (2500, F(1, 2), 25), (100, F(1, 2), 5), (225, F(1, 5), 6)]
TEST_Z = [Decimal(x) for x in ("1.2", "1.5", "2.2", "2.5", "3", "0.8", "1.8", "2.4", "-1.2", "-1.5", "-2.2", "-2.5", "-3", "-0.8", "-1.8", "-2.4")]


@gen("thinking_writing", 2, ["condition_check", "written_reasoning"])
def c_test(r):
    while True:
        n, p0, sd = r.choice(TEST_CASES)
        z = r.choice(TEST_Z)
        dk = z * sd
        if dk == dk.to_integral_value():
            break
    mu = int(n * p0)
    k = mu + int(dk)
    rej = abs(z) > Z95
    ctx = r.choice([("ある店のくじ（架空）", "当たりが出る", "当たりを引く"), ("ある種子（架空）", "発芽しない", "発芽しない種子がある"), ("ある製品の検査（架空）", "不良品である", "不良品が見つかる")])
    concl = (f"棄却される。{ctx[1]}確率は ${ft(p0)}$ ではないといえる。" if rej else f"棄却されない。{ctx[1]}確率は ${ft(p0)}$ ではないとはいえない（判断を保留する）。")
    return desc(f"{ctx[0]}で、{ctx[1]}確率は ${ft(p0)}$ とされている。無作為に ${n}$ 回（個）調べたところ、{ctx[2]}回数（個数）は ${k}$ であった。{ctx[1]}確率は ${ft(p0)}$ であるといえるか。帰無仮説を「確率は ${ft(p0)}$ である」として、有意水準 5% で両側検定しなさい。ただし、二項分布は正規分布で近似し、標準正規分布に従う $Z$ について $P(|Z|\\leqq1.96)=0.95$ を用いること。",
                f"$Z={dstr(z)}$。$|Z|{'>' if rej else '\\leqq'}1.96$ なので帰無仮説は{concl}",
                f"帰無仮説のもとで回数 $X$ は $B\\left({n},\\ {ft(p0)}\\right)$ に従い、近似的に $N({mu},\\,{sd}^2)$。$Z=\\dfrac{{{k}-{mu}}}{{{sd}}}={dstr(z)}$。",
                [("帰無仮説のもとでの分布（期待値・標準偏差）を正しく求めている", 2), ("$Z$ の値を正しく計算し、棄却域と比較している", 3), ("結論を「棄却される／されない」とその意味を正確な言葉で述べている", 3)], d=4, p=8, lines=10,
                ap="帰無仮説が正しいと仮定したときに、観測された結果が「めったに起こらない（確率 5% 未満の範囲）」かどうかを調べる。棄却域は $|Z|>1.96$。",
                steps=[f"帰無仮説のもとで $E(X)={n}\\times{ft(p0)}={mu}$、$\\sigma(X)=\\sqrt{{{n}\\times{ft(p0)}\\times{ft(1 - p0)}}}={sd}$。",
                       f"$Z=\\dfrac{{X-{mu}}}{{{sd}}}$ は近似的に $N(0,\\,1)$ に従う。$X={k}$ のとき $Z={dstr(z)}$。",
                       f"棄却域は $|Z|>1.96$。$|{dstr(z)}|{'>' if rej else '\\leqq'}1.96$。", f"帰無仮説は{concl}"],
                alt=[f"棄却域を回数で表すと $X<{mu}-1.96\\times{sd}={dstr(mu - Z95 * sd)}$ または $X>{dstr(mu + Z95 * sd)}$。観測値 ${k}$ がこの範囲に{'入る' if rej else '入らない'}ことでも判断できる。"],
                pc=[("帰無仮説のもとでの分布", 2), ("$Z$ の値と棄却域の比較", 3), ("結論の述べ方", 3)],
                pit=["棄却されないことを「確率は " + ft(p0) + " であることが証明された」と述べる。", "標準偏差の $\\sqrt{\\ }$ をとり忘れる。"],
                chk=(f"({k}-{n}*{fp(p0)})/sqrt({n}*{fp(p0)}*(1-{fp(p0)}))", dstr(z), None, "intermediate"))


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(stem, wrong, step, etype, tempt, fix, ans, expl, steps, ap, alt, pit, chk=None, d=3):
    return desc(f"{stem}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい答えを求めなさい。", ans, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい解答を途中式とともに示している", 3), ("最終的な答えが正しい", 1)], d=d, p=6, lines=6,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい途中式", 3), ("正しい答え", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix), chk=chk)


@gen("error_correction", 3, ["common_error", "computation"])
def d_recur_index(r):
    p = r.choice([2, 3, -2, 4])
    alpha = r.choice([x for x in range(-4, 5) if x != 0])
    q = alpha * (1 - p)
    a1 = r.choice([x for x in range(-3, 7) if x != alpha])
    K = a1 - alpha
    wrong_an = an_tex(K, p, alpha, "n")
    right_an = an_tex(K, p, alpha)
    vals = lin_seq(a1, p, q, 4)
    wrong = f"$\\alpha={p}\\alpha{cst(q)}$ より $\\alpha={alpha}$。$a_{{n+1}}{cst(-alpha)}={p}(a_n{cst(-alpha)})$ より、$\\{{a_n{cst(-alpha)}\\}}$ は初項 ${K}$、公比 ${p}$ の等比数列。よって $a_n={wrong_an}$。"
    return err_item(f"$a_1={a1},\\ a_{{n+1}}={p}a_n{cst(q)}$ で定められる数列 $\\{{a_n\\}}$ の一般項を求めなさい。", wrong, "最後の一般項の指数", "formula",
                    "等比数列の一般項 $ar^{n-1}$ の「$n-1$」を、公比を $n$ 回かけると思いこんで $r^n$ と書いてしまう。初項が第1項であることを意識していない。",
                    f"初項が第1項なので $a_n{cst(-alpha)}={term_coef(K, pw(p))}$、$a_n={right_an}$。", f"$a_n={right_an}$",
                    f"生徒の式に $n=1$ を代入すると ${K * p + alpha}$ となり、$a_1={a1}$ と一致しない。",
                    [f"$\\alpha={alpha}$、$\\{{a_n{cst(-alpha)}\\}}$ は初項 ${K}$、公比 ${p}$。", f"一般項は（初項）$\\times$（公比）$^{{n-1}}$ なので $a_n{cst(-alpha)}={term_coef(K, pw(p))}$。", f"$a_n={right_an}$。"],
                    "等比数列の一般項は（初項）$\\times$（公比）$^{n-1}$。求めた式は必ず $n=1$ を代入して検算する。",
                    [f"$a_2={fp(vals[1])}$ を漸化式から求め、正しい式に $n=2$ を代入した値と一致することを確かめる。"],
                    ["指数を $n$ とする。", "$\\alpha$ の符号を誤って $a_n+\\alpha$ の形で考える。"],
                    chk=(f"[{', '.join(f'({K})*({p})**({k}-1)+({alpha})' for k in range(1, 5))}]", f"[{', '.join(fp(v) for v in vals)}]", None, "intermediate"), d=2)


@gen("error_correction", 3, ["common_error", "computation"])
def d_ci_sqrt(r):
    ctx, unit = r.choice(POPS)
    rn = r.choice([5, 6, 8, 10, 12, 15, 16, 20])
    while True:
        sig = r.randint(5, 40)
        sd = F(sig, rn)
        if (sd * 100).denominator == 1:
            break
    n = rn * rn
    xbar = Decimal(r.randint(200, 1200)) / 10
    sdd = Decimal(sd.numerator) / Decimal(sd.denominator)
    h = Z95 * sdd
    wh = Z95 * Decimal(sig) / Decimal(n)
    wrong = f"$1.96\\times\\dfrac{{{sig}}}{{{n}}}={dstr(wh)}$ より、${dstr(xbar - wh)}\\leqq m\\leqq{dstr(xbar + wh)}$"
    return err_item(f"{ctx}の母平均 $m$ を推定するため、大きさ ${n}$ の無作為標本をとったところ、標本平均は ${dstr(xbar)}$ であった。母標準偏差を ${sig}$ として、信頼度 95% の信頼区間を求めなさい。",
                    wrong, "標本平均の標準偏差を $\\dfrac{\\sigma}{n}$ とした部分", "formula",
                    "「標本が多いほど精度が上がる」ことから、母標準偏差を $n$ で割れば良いと思いこんでいる。分散が $\\dfrac{\\sigma^2}{n}$ になることと標準偏差の関係を混同している。",
                    f"$\\sigma(\\overline{{X}})=\\dfrac{{{sig}}}{{\\sqrt{{{n}}}}}={dstr(sdd)}$、$1.96\\times{dstr(sdd)}={dstr(h)}$ より ${dstr(xbar - h)}\\leqq m\\leqq{dstr(xbar + h)}$。",
                    f"${dstr(xbar - h)}\\leqq m\\leqq{dstr(xbar + h)}$",
                    "標本平均の分散は $\\dfrac{\\sigma^2}{n}$ なので、標準偏差はその正の平方根 $\\dfrac{\\sigma}{\\sqrt{n}}$。",
                    ["$V(\\overline{X})=\\dfrac{\\sigma^2}{n}$ より $\\sigma(\\overline{X})=\\dfrac{\\sigma}{\\sqrt{n}}$。", f"$\\dfrac{{{sig}}}{{\\sqrt{{{n}}}}}={dstr(sdd)}$、$1.96$ 倍して ${dstr(h)}$。",
                     f"${dstr(xbar - h)}\\leqq m\\leqq{dstr(xbar + h)}$。"],
                    "信頼区間の半分の幅は $1.96\\times\\dfrac{\\sigma}{\\sqrt{n}}$。$\\sqrt{n}$ で割ることを公式とともに覚える。",
                    ["区間の幅が標本の大きさとともにどう変わるかを考えると、$n$ で割ると幅が狭くなりすぎる（$n$ を4倍にすると幅が $\\dfrac{1}{4}$）ことから誤りに気づける。"],
                    ["$\\sqrt{n}$ でなく $n$ で割る。", "$1.96$ をかけ忘れる。"],
                    chk=(f"[{dstr(xbar)}-1.96*{sig}/sqrt({n}), {dstr(xbar)}+1.96*{sig}/sqrt({n})]", f"[{dstr(xbar - h)}, {dstr(xbar + h)}]", None, "intermediate"), d=3)


@gen("error_correction", 2, ["common_error", "computation"])
def d_dot_coef(r):
    while True:
        A, B = r.randint(1, 5), r.randint(1, 5)
        D = r.randint(-A * B + 1, A * B - 1)
        k = r.choice([2, 3, -2, -3])
        L2 = A * A + 2 * k * D + k * k * B * B
        W2 = A * A + 2 * k * D + k * B * B
        if L2 > 0 and W2 > 0 and L2 != W2:
            break
    ve = vexpr(k)
    wrong = f"$|{ve}|^2=|\\vec{{a}}|^2{'+' if k > 0 else '-'}{2 * abs(k)}\\vec{{a}}\\cdot\\vec{{b}}{'+' if k > 0 else '-'}{abs(k)}|\\vec{{b}}|^2={A * A}{'+' if 2 * k * D >= 0 else ''}{2 * k * D}{'+' if k * B * B >= 0 else ''}{k * B * B}={W2}$ より $|{ve}|={sq(W2)}$"
    return err_item(f"$|\\vec{{a}}|={A},\\ |\\vec{{b}}|={B},\\ \\vec{{a}}\\cdot\\vec{{b}}={D}$ のとき、$|{ve}|$ を求めなさい。", wrong, "$|\\vec{b}|^2$ の係数", "calculation",
                    f"$(x+ky)^2=x^2+2kxy+k^2y^2$ と同じ展開であることを意識せず、$|\\vec{{b}}|^2$ の係数を ${k}$ のままにしている。",
                    f"$|{ve}|^2=|\\vec{{a}}|^2{'+' if k > 0 else '-'}{2 * abs(k)}\\vec{{a}}\\cdot\\vec{{b}}+{k * k}|\\vec{{b}}|^2={L2}$、$|{ve}|={sq(L2)}$",
                    f"$|{ve}|={sq(L2)}$",
                    f"$|\\vec{{a}}+k\\vec{{b}}|^2=(\\vec{{a}}+k\\vec{{b}})\\cdot(\\vec{{a}}+k\\vec{{b}})=|\\vec{{a}}|^2+2k\\vec{{a}}\\cdot\\vec{{b}}+k^2|\\vec{{b}}|^2$。",
                    [f"$|{ve}|^2=(\\vec{{a}}{'+' if k > 0 else '-'}{abs(k)}\\vec{{b}})\\cdot(\\vec{{a}}{'+' if k > 0 else '-'}{abs(k)}\\vec{{b}})$ と内積の形で書く。",
                     f"$=|\\vec{{a}}|^2{'+' if k > 0 else '-'}{2 * abs(k)}\\vec{{a}}\\cdot\\vec{{b}}+{k * k}|\\vec{{b}}|^2={A * A}{'+' if 2 * k * D >= 0 else ''}{2 * k * D}+{k * k * B * B}={L2}$。", f"$|{ve}|={sq(L2)}$。"],
                    "長さの2乗は「自分自身との内積」として分配法則で展開する。係数は2乗される。",
                    ["$\\vec{a}=(" + f"{A}" + ",\\,0)$ などの具体的な成分を条件に合うようにとり、成分で計算して確かめる方法もある。"],
                    ["$|\\vec{b}|^2$ の係数を2乗し忘れる。", "$2k\\vec{a}\\cdot\\vec{b}$ の符号を誤る。"],
                    chk=(f"sqrt(({A})**2+2*({k})*({D})+({k})**2*({B})**2)", str(sp.sqrt(L2)), None, "intermediate"), d=2)


@gen("error_correction", 2, ["common_error", "concept"])
def d_ci_meaning(r):
    ctx, unit = r.choice(POPS)
    rn = r.choice([8, 10, 12, 15, 20, 25])
    while True:
        sig = r.randint(5, 40)
        sd = F(sig, rn)
        if (sd * 100).denominator == 1:
            break
    n = rn * rn
    xbar = Decimal(r.randint(200, 1200)) / 10
    sdd = Decimal(sd.numerator) / Decimal(sd.denominator)
    h = Z95 * sdd
    lo, hi = dstr(xbar - h), dstr(xbar + h)
    wrong = f"$1.96\\times\\dfrac{{{sig}}}{{\\sqrt{{{n}}}}}={dstr(h)}$ より、信頼区間は ${lo}\\leqq m\\leqq{hi}$。したがって、調べた ${n}$ 個のデータのうちおよそ 95% が ${lo}$ 以上 ${hi}$ 以下の範囲にある。"
    return err_item(f"{ctx}について、大きさ ${n}$ の無作為標本の標本平均が ${dstr(xbar)}$ であった。母標準偏差を ${sig}$ として母平均 $m$ の信頼度 95% の信頼区間を求め、その意味を説明しなさい。",
                    wrong, "「データのおよそ 95% がこの範囲にある」と解釈した部分", "interpretation",
                    "「95%」という数字から、データの分布の範囲（平均 $\\pm1.96$ 標準偏差）と混同している。計算に使ったのは標本平均の標準偏差 $\\dfrac{\\sigma}{\\sqrt{n}}$ であり、個々のデータの散らばりではない。",
                    f"信頼区間は ${lo}\\leqq m\\leqq{hi}$（計算は正しい）。これは母平均 $m$ を推定する区間であり、「同じ方法で区間をつくることをくり返すと、そのうちおよそ 95% の区間が $m$ を含む」という意味である。",
                    f"${lo}\\leqq m\\leqq{hi}$。同じ方法で区間をつくることをくり返すと、およそ 95% の区間が母平均を含む、という意味。",
                    "信頼区間は母平均についての推定であり、標本の個々のデータの範囲ではない。",
                    [f"区間の計算 ${lo}\\leqq m\\leqq{hi}$ は正しい。", "誤りは解釈の部分。個々のデータは標準偏差 " + f"${sig}$" + " で散らばっており、区間（幅 " + f"${dstr(2 * h)}$" + "）よりずっと広い範囲に広がる。",
                     "正しい解釈：母平均を推定する区間であり、くり返し区間をつくったとき約 95% が母平均を含む。"],
                    "信頼区間の幅は $\\dfrac{\\sigma}{\\sqrt{n}}$ から作るので、データの散らばり $\\sigma$ よりはるかに狭い。何についての区間かを必ず言葉で確認する。",
                    [f"データの約 95% が入る範囲はおよそ $m\\pm1.96\\times{sig}$ であり、幅は信頼区間の $\\sqrt{{{n}}}={rn}$ 倍になることと比べると、両者が別物であることがわかる。"],
                    ["信頼区間を「データの範囲」と解釈する。", "$\\dfrac{\\sigma}{\\sqrt{n}}$ と $\\sigma$ を区別しない。"],
                    chk=(f"[{dstr(xbar)}-1.96*{sig}/sqrt({n}), {dstr(xbar)}+1.96*{sig}/sqrt({n})]", f"[{lo}, {hi}]", None, "intermediate"), d=3)


GENERATORS = [a_recur_linear, a_diff_recur, a_sample_dist, a_ci_mean, a_dot_from_norm, a_ci_width,
              b_recur_exp, b_recur_model, b_ci_prop, b_sample_size, b_dot_projection, b_dot_min,
              c_orthocenter, c_prob_recur, c_ci_interpret, c_test,
              d_recur_index, d_ci_sqrt, d_dot_coef, d_ci_meaning]
