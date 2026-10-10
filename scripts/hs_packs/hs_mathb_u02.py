"""単元パック：数学B 統計的な推測。"""
import math
from decimal import ROUND_HALF_UP, Decimal
from fractions import Fraction
from math import comb

from banks._common import desc, mc, num, sa, table
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem, tp)

UNIT_ID = "HS-MATHB-U02"


# ---------------------------------------------------------------------------
# 補助
# ---------------------------------------------------------------------------

def u(z):
    """正規分布表の値 p(z)=P(0≦Z≦z)（小数第4位まで）。"""
    return Decimal(str(round(0.5 * math.erf(z / math.sqrt(2)), 4))).quantize(Decimal("0.0001"))


ZS = [0.5, 0.8, 1, 1.2, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 3]


def zt(z):
    """z の表記（1 → 1、1.5 → 1.5）。"""
    return f"{z:g}"


def fx(v):
    """Fraction → LaTeX。"""
    v = Fraction(v)
    if v.denominator == 1:
        return str(v.numerator)
    s = "-" if v < 0 else ""
    return f"{s}\\dfrac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def fpy(v):
    v = Fraction(v)
    return str(v.numerator) if v.denominator == 1 else f"{v.numerator}/{v.denominator}"


def rnd(x, nd):
    """Fraction / Decimal を小数第 nd 位に四捨五入した文字列。"""
    if isinstance(x, Fraction):
        x = Decimal(x.numerator) / Decimal(x.denominator)
    return str(Decimal(x).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP))


def table_note(zs):
    return "ただし、" + "、".join(f"$p({zt(z)})={u(z)}$" for z in zs) + " とする（$p(z)=P(0\\leqq Z\\leqq z)$、$Z$ は標準正規分布に従う確率変数）。"


# 二項分布で標準偏差が整数になる (n, p, 文脈)
COIN = ("1枚の硬貨を投げる試行", "表が出る")
SUCC5 = ("成功する確率が $\\dfrac{1}{5}$ である試行", "成功する")
# (試行, 事象) の組。問題文は「{試行}を n 回くり返すとき、{事象}回数を X とする」の形で使う。
BINOMS = [(100, Fraction(1, 2), COIN), (400, Fraction(1, 2), COIN), (900, Fraction(1, 2), COIN), (1600, Fraction(1, 2), COIN),
          (180, Fraction(1, 6), ("1個のさいころを投げる試行", "1の目が出る")), (720, Fraction(1, 6), ("1個のさいころを投げる試行", "6の目が出る")),
          (450, Fraction(1, 3), ("1個のさいころを投げる試行", "3の倍数の目が出る")), (288, Fraction(1, 3), ("1個のさいころを投げる試行", "5以上の目が出る")),
          (625, Fraction(1, 5), SUCC5), (400, Fraction(1, 5), SUCC5), (3600, Fraction(1, 2), COIN), (2500, Fraction(1, 2), COIN)]


def bin_ms(n, p):
    m = n * p
    v = n * p * (1 - p)
    s = math.isqrt(int(v)) if v.denominator == 1 and math.isqrt(int(v)) ** 2 == v else None
    return m, v, s


LESSON = lesson(
    goals=["確率変数の期待値・分散・標準偏差を求め、$aX+b$ の期待値・分散の性質を導いて使える。",
           "二項分布 $B(n,\\,p)$ の期待値・分散を求め、正規分布の標準化と正規分布表を用いて確率を計算できる。",
           "標本平均の分布をもとに母平均・母比率を推定し、仮説検定の考え方で結論を適切な言葉で述べられる。"],
    duration=100,
    readiness=["確率の計算（数学A「場合の数と確率」）、反復試行の確率 ${}_n\\mathrm{C}_rp^r(1-p)^{n-r}$ を使える。",
               "データの平均・分散・標準偏差（数学Ⅰ「データの分析」）の意味を説明できる。", "平方根の計算ができる。"],
    flow=[("導入：一部から全体を知る", 8, "世論調査の例から「標本から母集団を推し測る」ための道具が必要であることを示す"),
          ("確率変数と確率分布", 17, "期待値・分散の定義と、$aX+b$ の性質の導出。例題1"),
          ("二項分布", 15, "$X=X_1+\\cdots+X_n$ と分けて期待値・分散を導く"),
          ("正規分布", 20, "標準化と正規分布表の使い方。二項分布の正規分布による近似。例題2"),
          ("推定", 20, "標本平均の分布から信頼度 95% の信頼区間を導く。例題3"),
          ("仮説検定とまとめ", 20, "帰無仮説・有意水準・棄却域。結論の言い方。確認問題")],
    sections=[
        intro("in1", "一部を調べて全体を推し測る",
              "全国の高校生全員の睡眠時間を調べることは難しいが、無作為に選んだ数百人を調べれば、全体の平均をかなりの精度で推し測ることができる。どのくらいの精度なのかを数で表すために、偶然によって値が決まる量（確率変数）とその分布を学ぶ。",
              bullets=["調べたい集団全体を母集団、そこから取り出した一部を標本という。", "標本の選び方が偶然に左右されるので、標本から計算した値も確率変数になる。",
                       "推定は「母数がどの範囲にありそうか」、検定は「仮説が正しいと考えてよいか」を判断する方法である。"],
              points=[tp("最初に「100人調べた平均と、別の100人を調べた平均は同じになるか」と問い、標本平均がばらつく量であることに気づかせる。", ask="同じ方法で別の標本をとると、平均は同じ値になるか。",
                         expect="毎回少しずつ違う値になる。", timing="導入の冒頭")]),
        definition("df1", "確率変数と期待値・分散",
                   "試行の結果によって値が定まり、その値をとる確率が定まっている変数を確率変数という。確率変数 $X$ のとる値が $x_1,\\ \\cdots,\\ x_n$、それぞれの確率が $p_1,\\ \\cdots,\\ p_n$ のとき、次のように定める。",
                   formula="$$E(X)=m=\\sum_{k=1}^{n}x_kp_k,\\qquad V(X)=\\sum_{k=1}^{n}(x_k-m)^2p_k=E(X^2)-\\{E(X)\\}^2,\\qquad \\sigma(X)=\\sqrt{V(X)}$$",
                   conditions=["確率の和 $p_1+\\cdots+p_n=1$ を必ず確認する。", "分散は「平均からのずれの2乗」の期待値。計算には $E(X^2)-\\{E(X)\\}^2$ が便利。"],
                   points=[tp("データの分析の「平均・分散」との対応（度数の割合が確率に置きかわる）を表で比べさせる。", ask="データの平均の式で、相対度数にあたるものは何か。", expect="確率 $p_k$。")]),
        theorem("th1", "$aX+b$ の期待値・分散",
                "$$E(aX+b)=aE(X)+b,\\qquad V(aX+b)=a^2V(X),\\qquad \\sigma(aX+b)=|a|\\sigma(X)$$",
                ["$a,\\ b$ は定数。", "定数 $b$ を加えても散らばりは変わらないので、分散に $b$ は現れない。"],
                proof=["$E(aX+b)=\\displaystyle\\sum(ax_k+b)p_k=a\\sum x_kp_k+b\\sum p_k=aE(X)+b$（$\\sum p_k=1$）。",
                       "$Y=aX+b$ の期待値は $am+b$ なので、$Y$ の値と期待値の差は $(ax_k+b)-(am+b)=a(x_k-m)$。",
                       "$V(Y)=\\displaystyle\\sum\\{a(x_k-m)\\}^2p_k=a^2\\sum(x_k-m)^2p_k=a^2V(X)$。",
                       "標準偏差は正の平方根なので $\\sigma(Y)=\\sqrt{a^2V(X)}=|a|\\sigma(X)$。"],
                points=[tp("$b$ が分散から消える理由を「全員の点数に5点ずつ加えても散らばりは同じ」という具体例で説明する。", caution="$V(aX+b)=aV(X)+b$ とする誤りが典型的。")]),
        example("ex1", "例題1　期待値と分散",
                "1個のさいころを1回投げ、出た目を $X$ とする。$E(X)$、$V(X)$ を求めよ。また、$Y=2X-3$ の期待値と分散を求めよ。",
                ["$E(X)=\\dfrac{1+2+\\cdots+6}{6}=\\dfrac{7}{2}$。", "$E(X^2)=\\dfrac{1+4+9+16+25+36}{6}=\\dfrac{91}{6}$。",
                 "$V(X)=\\dfrac{91}{6}-\\left(\\dfrac{7}{2}\\right)^2=\\dfrac{35}{12}$。", "$E(Y)=2\\cdot\\dfrac{7}{2}-3=4$、$V(Y)=2^2\\cdot\\dfrac{35}{12}=\\dfrac{35}{3}$。"],
                "$E(X)=\\dfrac{7}{2}$、$V(X)=\\dfrac{35}{12}$、$E(Y)=4$、$V(Y)=\\dfrac{35}{3}$",
                thinking="分散は $E(X^2)-\\{E(X)\\}^2$ で計算すると速い。$Y$ は $aX+b$ の性質を使い、分布を作り直さない。",
                points=[tp("$V(Y)$ を $2\\cdot\\dfrac{35}{12}-3$ とする誤答を板書で取り上げ、性質の証明にもどって正させる。")]),
        theorem("th2", "二項分布の期待値・分散",
                "$$X\\sim B(n,\\,p)\\ \\Longrightarrow\\ E(X)=np,\\qquad V(X)=np(1-p),\\qquad \\sigma(X)=\\sqrt{np(1-p)}$$",
                ["1回の試行で事象 A の起こる確率が $p$ のとき、この試行を $n$ 回くり返す反復試行で A の起こる回数 $X$ は二項分布 $B(n,\\,p)$ に従う。",
                 "$P(X=r)={}_n\\mathrm{C}_rp^r(1-p)^{n-r}\\quad(r=0,\\ 1,\\ \\cdots,\\ n)$"],
                proof=["$k$ 回目に A が起これば $1$、起こらなければ $0$ をとる確率変数を $X_k$ とすると、$X=X_1+X_2+\\cdots+X_n$。",
                       "$E(X_k)=1\\cdot p+0\\cdot(1-p)=p$、$V(X_k)=E(X_k^2)-p^2=p-p^2=p(1-p)$。",
                       "期待値は和の期待値＝期待値の和なので $E(X)=np$。",
                       "各回の試行は独立なので、$X_1,\\ \\cdots,\\ X_n$ は互いに独立で、分散も和になる：$V(X)=np(1-p)$。"],
                points=[tp("分散の和の性質は「独立」のときだけ成り立つことを確認する。", ask="なぜ分散を足し合わせてよいのか。", expect="各回の試行が互いに独立だから。")]),
        definition("df2", "正規分布と標準化",
                   "確率変数 $X$ が平均 $m$、標準偏差 $\\sigma$ の正規分布 $N(m,\\,\\sigma^2)$ に従うとき、$Z=\\dfrac{X-m}{\\sigma}$ は標準正規分布 $N(0,\\,1)$ に従う。$Z$ についての確率は正規分布表（$p(z)=P(0\\leqq Z\\leqq z)$）から求める。",
                   formula="$$Z=\\dfrac{X-m}{\\sigma},\\qquad P(Z\\geqq z)=0.5-p(z),\\qquad P(|Z|\\leqq1.96)=2p(1.96)=0.95$$",
                   conditions=["標準正規分布の曲線は $z=0$ に関して対称で、全体の面積は $1$（片側は $0.5$）。",
                               "$n$ が大きいとき、二項分布 $B(n,\\,p)$ は正規分布 $N(np,\\,np(1-p))$ で近似できる。"],
                   points=[tp("表の値は「0 から $z$ まで」の面積であることを図で確認し、求めたい部分の面積を足し引きで表させる。", caution="$P(Z\\geqq z)$ を $p(z)$ そのものとする誤り。")]),
        example("ex2", "例題2　二項分布の正規分布による近似",
                "1枚の硬貨を 400 回投げるとき、表が 220 回以上出る確率を求めよ。ただし $p(2)=0.4772$ とする。",
                ["表の出る回数 $X$ は $B\\left(400,\\ \\dfrac{1}{2}\\right)$ に従い、$E(X)=200$、$\\sigma(X)=\\sqrt{400\\cdot\\dfrac{1}{2}\\cdot\\dfrac{1}{2}}=10$。",
                 "$n$ が大きいので $X$ は近似的に $N(200,\\,10^2)$ に従う。$Z=\\dfrac{X-200}{10}$ とおく。",
                 "$P(X\\geqq220)=P(Z\\geqq2)=0.5-p(2)=0.0228$。"],
                "$0.0228$",
                thinking="回数が多いので正規分布で近似し、標準化して表を使う。",
                points=[tp("答えが約 2% であることから、「220 回以上」はめったに起こらないことを読み取らせ、仮説検定への伏線にする。")]),
        theorem("th3", "標本平均の分布",
                "$$E(\\overline{X})=m,\\qquad \\sigma(\\overline{X})=\\dfrac{\\sigma}{\\sqrt{n}}$$",
                ["母平均 $m$、母標準偏差 $\\sigma$ の母集団から大きさ $n$ の無作為標本を（復元抽出で）取り出したときの標本平均 $\\overline{X}$ について成り立つ。",
                 "$n$ が大きいとき、$\\overline{X}$ は近似的に正規分布 $N\\left(m,\\ \\dfrac{\\sigma^2}{n}\\right)$ に従う。"],
                proof=["$\\overline{X}=\\dfrac{1}{n}(X_1+\\cdots+X_n)$ で、各 $X_k$ の期待値は $m$、分散は $\\sigma^2$。",
                       "$E(\\overline{X})=\\dfrac{1}{n}\\cdot nm=m$。",
                       "$X_1,\\ \\cdots,\\ X_n$ は互いに独立なので $V(\\overline{X})=\\dfrac{1}{n^2}\\cdot n\\sigma^2=\\dfrac{\\sigma^2}{n}$、$\\sigma(\\overline{X})=\\dfrac{\\sigma}{\\sqrt{n}}$。"],
                points=[tp("標本を4倍にすると標本平均の標準偏差が半分になることを確認し、「精度を2倍にするには4倍の標本が必要」と言いかえさせる。")]),
        derivation("dv1", "母平均の推定（信頼度 95%）",
                   ["$\\overline{X}$ は近似的に $N\\left(m,\\ \\dfrac{\\sigma^2}{n}\\right)$ に従うので、$Z=\\dfrac{\\overline{X}-m}{\\sigma/\\sqrt{n}}$ は近似的に $N(0,\\,1)$ に従う。",
                    "$P(|Z|\\leqq1.96)=0.95$ より、$P\\left(\\overline{X}-1.96\\cdot\\dfrac{\\sigma}{\\sqrt{n}}\\leqq m\\leqq\\overline{X}+1.96\\cdot\\dfrac{\\sigma}{\\sqrt{n}}\\right)=0.95$。",
                    "標本平均の値 $\\overline{x}$ を代入した区間 $\\left[\\overline{x}-1.96\\cdot\\dfrac{\\sigma}{\\sqrt{n}},\\ \\overline{x}+1.96\\cdot\\dfrac{\\sigma}{\\sqrt{n}}\\right]$ を、母平均 $m$ に対する信頼度 95% の信頼区間という。",
                    "母比率 $p$ の推定では、標本比率 $R$ を用いて $\\left[R-1.96\\sqrt{\\dfrac{R(1-R)}{n}},\\ R+1.96\\sqrt{\\dfrac{R(1-R)}{n}}\\right]$ とする。"],
                   body="$n$ が大きいとき、母標準偏差 $\\sigma$ が分からなければ標本の標準偏差で代用してよい。",
                   points=[tp("「信頼度 95%」は「同じ方法で何度も区間をつくると、そのうち約 95% が $m$ を含む」という意味であり、「$m$ がこの区間に入る確率が 95%」とは言わないことを確認する。", caution="母平均は定数であり、確率的に動くのは区間の方である。")]),
        example("ex3", "例題3　母平均の推定",
                "ある農園のりんごから無作為に 144 個を選んで重さを量ったところ、平均は 310 g であった。母標準偏差を 24 g として、りんご全体の平均の重さを信頼度 95% で推定せよ。",
                ["$\\dfrac{\\sigma}{\\sqrt{n}}=\\dfrac{24}{12}=2$。", "$1.96\\times2=3.92$。", "$310-3.92=306.08$、$310+3.92=313.92$。"],
                "$[306.08,\\ 313.92]$（単位 g）",
                thinking="信頼区間の式 $\\overline{x}\\pm1.96\\cdot\\dfrac{\\sigma}{\\sqrt{n}}$ に代入する。$\\sqrt{144}=12$。",
                points=[tp("区間の幅 $2\\times1.96\\cdot\\dfrac{\\sigma}{\\sqrt{n}}$ が $n$ を大きくすると狭くなることを確認する。")]),
        theorem("th4", "仮説検定の手順（有意水準 5%、両側検定）",
                "$$|Z|=\\left|\\dfrac{X-m_0}{\\sigma_0}\\right|>1.96\\ \\Longrightarrow\\ \\text{帰無仮説を棄却する}$$",
                ["① 主張したいことと反対の仮説（帰無仮説）を立てる。", "② 帰無仮説のもとで、観測値以上に極端な値が出る確率が 5% 未満か（$|Z|>1.96$ か）を調べる。",
                 "③ 棄却域に入れば帰無仮説を棄却し、主張は正しいと判断する。入らなければ「帰無仮説は棄却されない（主張が正しいとは判断できない）」と結論する。"],
                proof=["帰無仮説が正しいとき、$Z$ は近似的に $N(0,\\,1)$ に従い、$P(|Z|>1.96)=1-0.95=0.05$。",
                       "$|Z|>1.96$ となる観測値は、帰無仮説のもとでは 5% 未満の確率でしか起こらない「まれな」結果である。",
                       "まれなことが起きたと考えるより、帰無仮説が誤っていると考える方が自然なので、帰無仮説を棄却する。"],
                points=[tp("棄却されなかったときに「帰無仮説が正しいと証明された」と書く誤りを、具体的な答案例で示す。", caution="「棄却できない」は「正しい」とは違う。判断を保留するという意味。")]),
        board("bd1", "板書案",
              [("① 確率変数", ["$E(X)=\\sum x_kp_k$", "$V(X)=E(X^2)-\\{E(X)\\}^2$", "$E(aX+b)=aE(X)+b$", "$V(aX+b)=a^2V(X)$", "例1 さいころ $\\frac{7}{2},\\ \\frac{35}{12}$"]),
               ("② 二項分布・正規分布", ["$B(n,p)$：$np$、$np(1-p)$", "$Z=\\frac{X-m}{\\sigma}$", "$P(Z\\geqq z)=0.5-p(z)$", "例2 $P(Z\\geqq2)=0.0228$"]),
               ("③ 推定と検定", ["$\\overline{x}\\pm1.96\\frac{\\sigma}{\\sqrt{n}}$", "例3 $[306.08,\\ 313.92]$", "帰無仮説 → $|Z|>1.96$ で棄却", "棄却されない ≠ 正しい"])],
              points=[tp("②では標準正規分布の曲線をかき、求める面積に斜線を引いてから式を書く。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("確率分布の表をつくったら、確率の和が $1$ になることを必ず確認させる。", timing="例題1の前"),
               tp("正規分布の確率は、毎回曲線の略図をかき、面積を $0.5$ と $p(z)$ の足し引きで表させる。", ask="求める部分は、$0$ の右側か左側か、両側か。"),
               tp("二項分布の分散は $np$ ではなく $np(1-p)$。標準偏差はその平方根であることを区別させる。", caution="$\\sigma=np(1-p)$ とする誤り。"),
               tp("推定の答えは区間で答え、単位も書かせる。四捨五入の位を問題文で確認させる。"),
               tp("検定の結論は「〜と判断できる」「〜とは判断できない」の形で書かせ、仮説が証明されたような表現を避けさせる。")],
              misconceptions=[("$V(2X+3)=2V(X)+3$", "$V(2X+3)=4V(X)$。定数を加えても散らばりは変わらない"),
                              ("$P(Z\\geqq1.5)=p(1.5)=0.4332$", "$P(Z\\geqq1.5)=0.5-p(1.5)=0.0668$"),
                              ("検定で棄却されなかったので「硬貨は正しくつくられている」と結論する", "「正しくつくられていないとは判断できない」と結論する")]),
        summary("sm1", "まとめ",
                ["$E(aX+b)=aE(X)+b$、$V(aX+b)=a^2V(X)$。二項分布は $np$、$np(1-p)$。",
                 "正規分布は標準化して表を使う。$n$ が大きい二項分布・標本平均は正規分布で近似できる。",
                 "信頼度 95% の信頼区間は $\\overline{x}\\pm1.96\\cdot\\dfrac{\\sigma}{\\sqrt{n}}$。検定は $|Z|>1.96$ で棄却。"]),
        check("ck1", "確認問題",
              [("$E(X)=4$、$V(X)=9$ のとき、$E(-2X+5)$、$\\sigma(-2X+5)$ を求めよ。", "$E=-3$、$\\sigma=|-2|\\times3=6$"),
               ("$X$ が $B\\left(90,\\ \\dfrac{1}{3}\\right)$ に従うとき、$E(X)$ と $V(X)$ を求めよ。", "$E(X)=30$、$V(X)=90\\cdot\\dfrac{1}{3}\\cdot\\dfrac{2}{3}=20$"),
               ("$Z$ が $N(0,\\,1)$ に従うとき、$P(Z\\leqq-1)$ を求めよ。ただし $p(1)=0.3413$。", "$0.5-0.3413=0.1587$")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

def rand_dist(r):
    k = r.choice([3, 3, 4])
    xs = sorted(r.sample(range(-2, 10), k))
    den = r.choice([6, 8, 10, 12])
    while True:
        ws = [r.randint(1, den) for _ in range(k - 1)]
        if sum(ws) < den:
            ws.append(den - sum(ws))
            break
    return xs, [Fraction(w, den) for w in ws], den, ws


@gen("basic_check", 4, ["computation"])
def expect_var(r):
    xs, ps, den, ws = rand_dist(r)
    ask = r.choice(["E", "V", "E"])
    E = sum(x * p for x, p in zip(xs, ps))
    E2 = sum(x * x * p for x, p in zip(xs, ps))
    V = E2 - E * E
    val = E if ask == "E" else V
    tbl = table([["$X$"] + [f"${x}$" for x in xs] + ["計"], ["$P$"] + [f"${fx(p)}$" for p in ps] + ["$1$"]])
    nm = "期待値 $E(X)$" if ask == "E" else "分散 $V(X)$"
    dist = "、".join(f"$P(X={x})={fx(p)}$" for x, p in zip(xs, ps))
    return num(f"確率変数 $X$ の確率分布は {dist} である（下の表）。$X$ の{nm}を求めなさい。", fpy(val),
               f"$E(X)={fx(E)}$" + ("" if ask == "E" else f"、$E(X^2)={fx(E2)}$、$V(X)=E(X^2)-\\{{E(X)\\}}^2={fx(V)}$") + "。", d=2, disp=f"${fx(val)}$", tbl=tbl,
               ap="期待値は「値×確率」の和。分散は $E(X^2)-\\{E(X)\\}^2$ で計算すると速い。",
               steps=[f"$E(X)=" + "+".join(f"{x}\\cdot{fx(p)}" if x >= 0 else f"({x})\\cdot{fx(p)}" for x, p in zip(xs, ps)) + f"={fx(E)}$。"]
               + ([] if ask == "E" else [f"$E(X^2)=" + "+".join(f"{x * x}\\cdot{fx(p)}" for x, p in zip(xs, ps)) + f"={fx(E2)}$。", f"$V(X)={fx(E2)}-\\left({fx(E)}\\right)^2={fx(V)}$。"]),
               alt=["分散は定義どおり $\\sum(x_k-m)^2p_k$ で計算しても同じ値になる。"] if ask == "V" else ["確率をすべて分母 " + f"${den}$" + " にそろえて、分子だけで「値×重み」の和を計算し、最後に分母で割ると計算が楽になる。"],
               pc=[("式を正しく立てている", 1), ("値を正しく求めている", 1)],
               pit=["分散を $E(X^2)$ だけで止める。", "負の値の符号を落とす。"],
               chk=("sum([" + ", ".join(f"({x})*({fpy(p)})" if ask == "E" else f"({x})**2*({fpy(p)})" for x, p in zip(xs, ps)) + "])" + ("" if ask == "E" else f"-({fpy(E)})**2"), fpy(val)))


@gen("basic_check", 4, ["computation", "condition_check"])
def linear_transform(r):
    m, v = r.randint(-5, 12), r.choice([1, 4, 9, 16, 25, 2, 3, 5])
    a, b = r.choice([x for x in range(-5, 6) if x not in (0, 1)]), r.choice([x for x in range(-9, 10) if x])
    ask = r.choice(["E", "V", "S"])
    Y = f"{a}X{'+' if b > 0 else '-'}{abs(b)}"
    if ask == "E":
        val, nm = a * m + b, "期待値 $E(Y)$"
        e = f"$E(Y)={a}E(X){'+' if b > 0 else '-'}{abs(b)}={val}$"
        py = f"{a}*{m}+({b})"
    elif ask == "V":
        val, nm = a * a * v, "分散 $V(Y)$"
        e = f"$V(Y)=({a})^2V(X)={val}$"
        py = f"({a})**2*{v}"
    else:
        if v not in (1, 4, 9, 16, 25):
            v = 9
        val, nm = abs(a) * math.isqrt(v), "標準偏差 $\\sigma(Y)$"
        e = f"$\\sigma(Y)=|{a}|\\sigma(X)=|{a}|\\times{math.isqrt(v)}={val}$"
        py = f"Abs({a})*sqrt({v})"
    return num(f"確率変数 $X$ の期待値が ${m}$、分散が ${v}$ である。$Y={Y}$ の{nm}を求めなさい。", str(val), e + "。", d=2,
               ap="$E(aX+b)=aE(X)+b$、$V(aX+b)=a^2V(X)$、$\\sigma(aX+b)=|a|\\sigma(X)$。定数 $b$ は散らばりに影響しない。",
               steps=[f"$Y={Y}$ で $a={a}$、$b={b}$。", e + "。"],
               alt=["分散は「ずれの2乗」の平均なので、$X$ を $a$ 倍するとずれも $a$ 倍、2乗して $a^2$ 倍になる、と意味から確かめる。"],
               pc=[("正しい性質を選んでいる", 1), ("値を正しく求めている", 1)],
               pit=["$V(aX+b)=aV(X)+b$ とする。", "$\\sigma(aX+b)$ で $a$ が負のとき絶対値をつけ忘れる。"],
               chk=(py, str(val)))


@gen("basic_check", 4, ["computation"])
def binom_ev(r):
    n, p, ctx = r.choice(BINOMS + [(60, Fraction(1, 6), ("1個のさいころを投げる試行", "1の目が出る")), (50, Fraction(2, 5), ("成功する確率が $\\dfrac{2}{5}$ である試行", "成功する")),
                                   (150, Fraction(1, 3), ("1個のさいころを投げる試行", "2以下の目が出る"))])
    if (n, p) == (180, Fraction(1, 6)):
        n = 360
    ask = r.choice(["E", "V", "S"])
    m, v, s = bin_ms(n, p)
    if ask == "S" and s is None:
        ask = "V"
    val = {"E": m, "V": v, "S": s}[ask]
    nm = {"E": "期待値", "V": "分散", "S": "標準偏差"}[ask]
    return num(f"{ctx[0]}を ${n}$ 回くり返すとき、{ctx[1]}回数を $X$ とする。$X$ の{nm}を求めなさい。", fpy(val),
               f"$X$ は二項分布 $B\\left({n},\\ {fx(p)}\\right)$ に従う。" + {"E": f"$E(X)=np={fx(m)}$。", "V": f"$V(X)=np(1-p)={fx(v)}$。", "S": f"$\\sigma(X)=\\sqrt{{np(1-p)}}=\\sqrt{{{fx(v)}}}={s}$。"}[ask],
               d=2, disp=f"${fx(val)}$",
               ap="独立な試行のくり返しで、ある事象の起こる回数は二項分布に従う。$E(X)=np$、$V(X)=np(1-p)$。",
               steps=[f"$X$ は $B\\left({n},\\ {fx(p)}\\right)$ に従う。", {"E": f"$E(X)={n}\\times{fx(p)}={fx(m)}$。", "V": f"$V(X)={n}\\times{fx(p)}\\times{fx(1 - p)}={fx(v)}$。",
                                                                         "S": f"$V(X)={fx(v)}$、$\\sigma(X)=\\sqrt{{{fx(v)}}}={s}$。"}[ask]],
               alt=["$X=X_1+\\cdots+X_n$（各回の成功を $1$、失敗を $0$）と分けて、1回分の期待値 $p$・分散 $p(1-p)$ の $n$ 倍として確かめる。"],
               pc=[("二項分布であることと $n,\\ p$ を正しく捉えている", 1), ("値を正しく求めている", 1)],
               pit=["分散を $np$ とする。", "標準偏差の平方根をとり忘れる。"],
               chk=({"E": f"{n}*{fpy(p)}", "V": f"{n}*{fpy(p)}*(1-{fpy(p)})", "S": f"sqrt({n}*{fpy(p)}*(1-{fpy(p)}))"}[ask], fpy(val)))


@gen("basic_check", 4, ["computation", "concept"])
def standardize(r):
    m = r.choice([50, 60, 65, 70, 160, 170, 300, 500, 20, 40])
    while True:
        s = r.choice([2, 4, 5, 8, 10, 12, 15, 20])
        z = Fraction(str(r.choice([-2.5, -2, -1.5, -1.25, -1, -0.5, 0.5, 1, 1.25, 1.5, 2, 2.5, 3])))
        if (z * s).denominator == 1:
            break
    x = int(m + z * s)
    zv = Fraction(x - m, s)
    return num(f"確率変数 $X$ が正規分布 $N({m},\\,{s}^2)$ に従うとする。$X={x}$ を標準化した値 $Z=\\dfrac{{X-m}}{{\\sigma}}$ を求めなさい。", fpy(zv) if zv.denominator == 1 else str(float(zv)),
               f"$Z=\\dfrac{{{x}-{m}}}{{{s}}}={float(zv):g}$。", d=1,
               ap="標準化は「平均からのずれが標準偏差の何倍か」を表す。$N(m,\\,\\sigma^2)$ の $\\sigma^2$ は分散なので、$\\sigma$ はその平方根。",
               steps=[f"$m={m}$、$\\sigma={s}$。", f"$Z=\\dfrac{{{x}-{m}}}{{{s}}}={float(zv):g}$。"],
               alt=[f"逆に $X=m+Z\\sigma={m}+({float(zv):g})\\times{s}={x}$ となることで確かめる。"],
               pc=[("$m$ と $\\sigma$ を正しく読み取っている", 1), ("$Z$ を正しく求めている", 1)],
               pit=["分散 $\\sigma^2$ で割ってしまう。"],
               chk=(f"({x}-{m})/{s}", fpy(zv) if zv.denominator == 1 else str(float(zv))))


@gen("basic_check", 4, ["computation", "concept"])
def normal_prob(r):
    form = r.choice(["ge", "le_neg", "between0", "sym", "two"])
    a = r.choice(ZS)
    if form == "ge":
        stem, val, how, expr = f"P(Z\\geqq{zt(a)})", Decimal("0.5") - u(a), f"0.5-p({zt(a)})", f"0.5-{u(a)}"
        zs = [a]
    elif form == "le_neg":
        stem, val, how, expr = f"P(Z\\leqq-{zt(a)})", Decimal("0.5") - u(a), f"0.5-p({zt(a)})", f"0.5-{u(a)}"
        zs = [a]
    elif form == "between0":
        stem, val, how, expr = f"P(-{zt(a)}\\leqq Z\\leqq0)", u(a), f"p({zt(a)})", f"{u(a)}"
        zs = [a]
    elif form == "sym":
        stem, val, how, expr = f"P(|Z|\\leqq{zt(a)})", 2 * u(a), f"2p({zt(a)})", f"2*{u(a)}"
        zs = [a]
    else:
        b = r.choice([z for z in ZS if z != a])
        stem, val, how, expr = f"P(-{zt(a)}\\leqq Z\\leqq{zt(b)})", u(a) + u(b), f"p({zt(a)})+p({zt(b)})", f"{u(a)}+{u(b)}"
        zs = sorted({a, b})
    return num(f"確率変数 $Z$ が標準正規分布 $N(0,\\,1)$ に従うとき、${stem}$ を求めなさい。{table_note(zs)}", str(val),
               f"曲線の対称性と、片側の面積が $0.5$ であることを使って ${how}={val}$。", d=2,
               ap="標準正規分布の曲線は $z=0$ に関して対称。表の値 $p(z)$ は $0$ から $z$ までの面積なので、求める部分を $0.5$ と $p(z)$ の足し引きで表す。",
               steps=["曲線をかき、求める部分に斜線を引く。", f"対称性から ${stem}={how}$。", f"$={val}$。"],
               alt=["求めた値が $0$ から $1$ の間にあり、図の面積の見当（$0.5$ より大きいか小さいか）と合うかで確かめる。"],
               pc=[("面積を $p(z)$ で正しく表している", 1), ("値を正しく求めている", 1)],
               pit=["$P(Z\\geqq a)$ を $p(a)$ とする。", "負の側の範囲を、対称性を使わずに表の値をそのまま負にする。"],
               chk=(expr, str(val)))


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 5, ["computation"])
def normal_x_prob(r):
    ctx = r.choice([("ある高校の男子の身長", "cm", 170, [4, 5, 6, 8]), ("ある試験の得点", "点", 60, [8, 10, 12, 15, 20]),
                    ("ある工場で作られる製品の重さ", "g", 200, [2, 4, 5, 10]), ("ある地域の 1 日の最高気温", "℃", 25, [2, 4]),
                    ("ある農園のみかん1個の重さ", "g", 100, [5, 8, 10])])
    name, unit, m0, sds = ctx
    m = m0 + r.choice([-10, -5, 0, 0, 5, 10]) if unit != "℃" else m0 + r.choice([-2, 0, 2])
    s = r.choice(sds)
    form = r.choice(["ge", "le", "between", "between2"])
    za = r.choice([0.5, 1, 1.5, 2, 2.5])
    zb = r.choice([z for z in [0.5, 1, 1.5, 2, 2.5] if z != za])
    xa = m + Fraction(str(za)) * s
    xb = m - Fraction(str(zb)) * s

    def X(v):
        return f"{float(v):g}"
    if form == "ge":
        ev, val, how, zs = f"X\\geqq{X(xa)}", Decimal("0.5") - u(za), f"P(Z\\geqq{zt(za)})=0.5-p({zt(za)})", [za]
        expr, exp = f"[({fpy(xa)}-{m})/{s}, 0.5-{u(za)}]", f"[{za}, {val}]"
    elif form == "le":
        ev, val, how, zs = f"X\\leqq{X(xb)}", Decimal("0.5") - u(zb), f"P(Z\\leqq-{zt(zb)})=0.5-p({zt(zb)})", [zb]
        expr, exp = f"[({fpy(xb)}-{m})/{s}, 0.5-{u(zb)}]", f"[-{zb}, {val}]"
    elif form == "between":
        ev, val, how, zs = f"{X(xb)}\\leqq X\\leqq{X(xa)}", u(zb) + u(za), f"P(-{zt(zb)}\\leqq Z\\leqq{zt(za)})=p({zt(zb)})+p({zt(za)})", sorted({za, zb})
        expr, exp = f"[({fpy(xb)}-{m})/{s}, ({fpy(xa)}-{m})/{s}, {u(zb)}+{u(za)}]", f"[-{zb}, {za}, {val}]"
    else:
        lo, hi = sorted([za, zb])
        x1, x2 = m + Fraction(str(lo)) * s, m + Fraction(str(hi)) * s
        ev, val, how, zs = f"{X(x1)}\\leqq X\\leqq{X(x2)}", u(hi) - u(lo), f"P({zt(lo)}\\leqq Z\\leqq{zt(hi)})=p({zt(hi)})-p({zt(lo)})", [lo, hi]
        expr, exp = f"[({fpy(x1)}-{m})/{s}, ({fpy(x2)}-{m})/{s}, {u(hi)}-{u(lo)}]", f"[{lo}, {hi}, {val}]"
    return num(f"{name} $X$（{unit}）は、平均 ${m}$、標準偏差 ${s}$ の正規分布に従うとする。$P({ev})$ を求めなさい。{table_note(zs)}", str(val),
               f"$Z=\\dfrac{{X-{m}}}{{{s}}}$ と標準化すると ${how}={val}$。", d=3,
               ap="正規分布の確率は、標準化 $Z=\\dfrac{X-m}{\\sigma}$ で標準正規分布に直してから、正規分布表を使う。",
               steps=[f"$Z=\\dfrac{{X-{m}}}{{{s}}}$ とおくと、$Z$ は $N(0,\\,1)$ に従う。", "$X$ の範囲を $Z$ の範囲に直す。", f"${how}={val}$。"],
               alt=["標準化した $Z$ の範囲を図にかき、面積の見当（$0.5$ より大きいか小さいか）と答えが合うか確かめる。"],
               pc=[("正しく標準化している", 2), ("表を使って確率を正しく求めている", 2)],
               pit=["$X$ の範囲を $Z$ に直すとき、平均を引き忘れる。", "片側の確率で $0.5$ から引き忘れる。"],
               chk=(expr, exp, None, "intermediate"))


@gen("standard_practice", 4, ["computation", "application"])
def binom_normal(r):
    n, p, ctx = r.choice(BINOMS)
    m, v, s = bin_ms(n, p)
    z = r.choice([1, 1.5, 2, 2.5, 3])
    if (Fraction(str(z)) * s).denominator != 1:
        z = int(z) or 1
    k = int(m + Fraction(str(z)) * s)
    side = r.choice(["ge", "le"])
    if side == "ge":
        ev, val = f"${k}$ 回以上", Decimal("0.5") - u(z)
    else:
        k = int(m - Fraction(str(z)) * s)
        ev, val = f"${k}$ 回以下", Decimal("0.5") - u(z)
    rel = "\\geqq" if side == "ge" else "\\leqq-"
    return num(f"{ctx[0]}を ${n}$ 回くり返すとき、{ctx[1]}回数が {ev} となる確率を、正規分布で近似して求めなさい。{table_note([z])}", str(val),
               f"回数 $X$ は $B\\left({n},\\ {fx(p)}\\right)$ に従い、$E(X)={fx(m)}$、$\\sigma(X)={s}$。$n$ が大きいので近似的に $N({fx(m)},\\,{s}^2)$ に従う。", d=3,
               ap="回数が多い二項分布は、同じ平均・分散をもつ正規分布で近似できる。期待値と標準偏差を求めて標準化する。",
               steps=[f"$E(X)={n}\\times{fx(p)}={fx(m)}$、$\\sigma(X)=\\sqrt{{{n}\\times{fx(p)}\\times{fx(1 - p)}}}={s}$。",
                      f"$Z=\\dfrac{{X-{fx(m)}}}{{{s}}}$ とおくと、$X={k}$ は $Z={'' if side == 'ge' else '-'}{zt(z)}$ に対応する。",
                      f"$P(Z{rel}{zt(z)})=0.5-p({zt(z)})={val}$。"],
               alt=["求めた確率が小さいことは、観測値が期待値から標準偏差の " + f"${zt(z)}$" + " 倍離れていることからも見当がつく（約68%が ±1σ、約95%が ±2σ の範囲に入る）。"],
               pc=[("期待値と標準偏差を正しく求めている", 2), ("標準化して確率を正しく求めている", 2)],
               pit=["分散と標準偏差を取り違えて標準化する。", "片側の確率を $p(z)$ のままにする。"],
               chk=(f"[{n}*{fpy(p)}, sqrt({n}*{fpy(p)}*(1-{fpy(p)})), 0.5-{u(z)}]", f"[{fpy(m)}, {s}, {val}]", None, "intermediate"))


@gen("standard_practice", 4, ["computation", "concept"])
def sample_mean(r):
    m = r.choice([50, 60, 120, 170, 250, 30])
    s = r.choice([6, 8, 10, 12, 15, 20, 24, 30])
    n = r.choice([4, 9, 16, 25, 36, 64, 100, 144])
    ask = r.choice(["S", "S", "V"])
    sv = Fraction(s, math.isqrt(n))
    val = sv if ask == "S" else sv * sv
    nm = "標準偏差 $\\sigma(\\overline{X})$" if ask == "S" else "分散 $V(\\overline{X})$"
    return num(f"母平均 ${m}$、母標準偏差 ${s}$ の母集団から、大きさ ${n}$ の無作為標本を抽出する。標本平均 $\\overline{{X}}$ の期待値と{nm}を求めなさい。", fpy(val),
               f"$E(\\overline{{X}})={m}$、" + (f"$\\sigma(\\overline{{X}})=\\dfrac{{{s}}}{{\\sqrt{{{n}}}}}={fx(sv)}$。" if ask == "S" else f"$V(\\overline{{X}})=\\dfrac{{{s}^2}}{{{n}}}={fx(val)}$。"),
               d=3, disp=f"$E(\\overline{{X}})={m}$、" + (f"$\\sigma(\\overline{{X}})={fx(val)}$" if ask == "S" else f"$V(\\overline{{X}})={fx(val)}$"),
               ap="標本平均の期待値は母平均と等しく、標準偏差は母標準偏差の $\\dfrac{1}{\\sqrt{n}}$ 倍（分散は $\\dfrac{1}{n}$ 倍）になる。",
               steps=[f"$E(\\overline{{X}})=m={m}$。", f"$\\sigma(\\overline{{X}})=\\dfrac{{{s}}}{{\\sqrt{{{n}}}}}={fx(sv)}$。"] + ([] if ask == "S" else [f"$V(\\overline{{X}})=\\left({fx(sv)}\\right)^2={fx(val)}$。"]),
               alt=["$V(\\overline{X})=\\dfrac{1}{n^2}\\{V(X_1)+\\cdots+V(X_n)\\}=\\dfrac{\\sigma^2}{n}$ と、独立な確率変数の和の分散から導いて確かめる。"],
               pc=[("期待値を正しく答えている", 1), ("標準偏差（分散）を正しく求めている", 3)],
               pit=["$\\sqrt{n}$ ではなく $n$ で割る（標準偏差の場合）。", "分散と標準偏差を取り違える。"],
               chk=(f"{s}/sqrt({n})" if ask == "S" else f"{s}**2/{n}", fpy(val)))


@gen("standard_practice", 4, ["computation", "application"])
def ci_mean(r):
    ctx = r.choice([("ある工場で作られた菓子袋", "内容量", "g", "袋"), ("ある市の中学生", "1日の読書時間", "分", "人"), ("ある養鶏場の卵", "重さ", "g", "個"),
                    ("ある高校の2年生", "通学時間", "分", "人"), ("ある農園のトマト", "糖度", "度", "個")])
    n = r.choice([64, 100, 144, 196, 225, 256, 400, 900])
    s = r.choice([4, 5, 6, 7, 8, 10, 12, 14, 15, 20])
    xbar = Fraction(r.randint(200, 2000), 10) if ctx[2] != "度" else Fraction(r.randint(60, 120), 10)
    if (n, s) == (100, 2):
        n = 144
    half = Fraction(196, 100) * Fraction(s, math.isqrt(n))
    lo, hi = xbar - half, xbar + half
    return sa(f"{ctx[0]}から無作為に ${n}$ {ctx[3]}を選んで{ctx[1]}を調べたところ、標本平均は ${float(xbar):g}$ {ctx[2]}であった。母標準偏差を ${s}$ {ctx[2]}として、母平均を信頼度 95% で推定しなさい。答えは小数第2位を四捨五入して小数第1位まで求めなさい。",
              f"$[{rnd(lo, 1)},\\ {rnd(hi, 1)}]$（単位 {ctx[2]}）",
              f"信頼区間は $\\overline{{x}}\\pm1.96\\cdot\\dfrac{{\\sigma}}{{\\sqrt{{n}}}}={float(xbar):g}\\pm1.96\\times\\dfrac{{{s}}}{{{math.isqrt(n)}}}$。", d=3, v=[f"[{rnd(lo, 1)}, {rnd(hi, 1)}]"],
              ap="標本平均 $\\overline{X}$ は近似的に $N\\left(m,\\ \\dfrac{\\sigma^2}{n}\\right)$ に従う。信頼度 95% の信頼区間は $\\overline{x}\\pm1.96\\cdot\\dfrac{\\sigma}{\\sqrt{n}}$。",
              steps=[f"$\\dfrac{{\\sigma}}{{\\sqrt{{n}}}}=\\dfrac{{{s}}}{{{math.isqrt(n)}}}$。", f"$1.96\\times\\dfrac{{{s}}}{{{math.isqrt(n)}}}={float(half):g}$。",
                     f"${float(xbar):g}-{float(half):g}={float(lo):g}$、${float(xbar):g}+{float(half):g}={float(hi):g}$。", f"四捨五入して $[{rnd(lo, 1)},\\ {rnd(hi, 1)}]$。"],
              alt=["区間の中央が標本平均、半分の幅が $1.96\\times$（標本平均の標準偏差）になっているかを確かめる。"],
              pc=[("信頼区間の式を正しく立てている", 2), ("区間の両端を正しく計算し、指示どおりに四捨五入している", 2)],
              pit=["$\\sqrt{n}$ で割り忘れる。", "区間ではなく1つの値で答える。"],
              chk=(f"[{fpy(xbar)}-196/100*{s}/sqrt({n}), {fpy(xbar)}+196/100*{s}/sqrt({n})]", f"[{fpy(lo)}, {fpy(hi)}]", None, "intermediate"))


PROPS = [(Fraction(1, 5), 400), (Fraction(1, 2), 100), (Fraction(3, 5), 600), (Fraction(4, 5), 400), (Fraction(9, 10), 900), (Fraction(1, 10), 900),
         (Fraction(1, 2), 400), (Fraction(1, 2), 625), (Fraction(1, 5), 1600), (Fraction(2, 5), 600), (Fraction(3, 5), 2400), (Fraction(1, 2), 2500)]


@gen("standard_practice", 3, ["computation", "application"])
def ci_prop(r):
    R, n = r.choice(PROPS)
    ctx = r.choice(["ある市の有権者", "ある町の世帯", "ある高校の生徒", "ある工場の製品", "ある地域の住民"])
    cnt = {"ある市の有権者": "人", "ある町の世帯": "世帯", "ある高校の生徒": "人", "ある工場の製品": "個", "ある地域の住民": "人"}[ctx]
    what = {"ある工場の製品": "規格に適合していた", "ある市の有権者": "ある政策に賛成と答えた", "ある町の世帯": "家庭菜園をしていると答えた",
            "ある高校の生徒": "毎朝朝食をとると答えた", "ある地域の住民": "路線バスを利用していると答えた"}[ctx]
    k = int(R * n)
    var = R * (1 - R) / n
    sd = Fraction(math.isqrt(var.numerator), math.isqrt(var.denominator))
    assert sd * sd == var
    half = Fraction(196, 100) * sd
    lo, hi = R - half, R + half
    return sa(f"{ctx}から無作為に ${n}$ {cnt}を抽出して調べたところ、${k}$ {cnt}が{what}。全体のうち{what}ものの割合（母比率）$p$ を信頼度 95% で推定しなさい。答えは小数第4位を四捨五入して小数第3位まで求めなさい。",
              f"$[{rnd(lo, 3)},\\ {rnd(hi, 3)}]$",
              f"標本比率 $R={float(R):g}$、$\\sqrt{{\\dfrac{{R(1-R)}}{{n}}}}={float(sd):g}$。$R\\pm1.96\\times{float(sd):g}$。", d=3, v=[f"[{rnd(lo, 3)}, {rnd(hi, 3)}]"],
              ap="$n$ が大きいとき、標本比率 $R$ は近似的に $N\\left(p,\\ \\dfrac{p(1-p)}{n}\\right)$ に従う。母比率 $p$ の代わりに $R$ を用いて信頼区間をつくる。",
              steps=[f"$R=\\dfrac{{{k}}}{{{n}}}={float(R):g}$。", f"$\\sqrt{{\\dfrac{{{float(R):g}\\times{float(1 - R):g}}}{{{n}}}}}={float(sd):g}$。",
                     f"$1.96\\times{float(sd):g}={float(half):g}$。", f"$[{float(lo):g},\\ {float(hi):g}]$ を四捨五入して $[{rnd(lo, 3)},\\ {rnd(hi, 3)}]$。"],
              alt=["区間の中央が標本比率 $R$ になっていること、区間の幅が $n$ を大きくすると狭くなることを確かめる。"],
              pc=[("標本比率と標準偏差の式を正しく立てている", 2), ("区間を正しく計算している", 2)],
              pit=["$\\sqrt{\\ }$ をとり忘れる。", "人数 $k$ をそのまま比率として使う。"],
              chk=(f"[{fpy(R)}-196/100*sqrt({fpy(R)}*(1-{fpy(R)})/{n}), {fpy(R)}+196/100*sqrt({fpy(R)}*(1-{fpy(R)})/{n})]", f"[{fpy(lo)}, {fpy(hi)}]", None, "intermediate"))


# ======================================================================
# C 思考力・記述応用
# ======================================================================

@gen("thinking_writing", 3, ["written_reasoning", "condition_check"])
def test_binom(r):
    n, p, ctx = r.choice([b for b in BINOMS if b[0] >= 180])
    m, v, s = bin_ms(n, p)
    reject = r.random() < 0.5
    zr = r.choice([2, 2.5, 3, 2.2, 2.4]) if reject else r.choice([0.6, 1, 1.2, 1.4, 1.6, 1.8])
    d = round(zr * s)
    if reject and d <= 1.96 * s:
        d = math.ceil(1.96 * s) + 1
    if not reject and d >= 1.96 * s:
        d = math.floor(1.96 * s) - 1
    sign = r.choice([1, -1])
    k = int(m + sign * d)
    z = Fraction(k - m) / s
    claim = f"{ctx[1]}確率は ${fx(p)}$ ではない"
    concl = ("帰無仮説は棄却される。よって、" + claim + "と判断できる。") if abs(z) > Fraction(196, 100) else ("帰無仮説は棄却されない。よって、" + claim + "とは判断できない。")
    cmp = ">" if abs(z) > Fraction(196, 100) else "\\leqq"
    return desc(f"{ctx[0]}を ${n}$ 回くり返したところ、{ctx[1]}回数は ${k}$ 回であった。{ctx[1]}確率は ${fx(p)}$ であるといえるか。有意水準 5% で仮説検定しなさい。"
                f"ただし、二項分布は正規分布で近似し、$P(|Z|\\leqq1.96)=0.95$ を用いること。",
                f"$z={float(z):.2f}$。" + concl,
                f"帰無仮説「確率は ${fx(p)}$」のもとで、回数 $X$ は近似的に $N({fx(m)},\\,{s}^2)$ に従う。$z=\\dfrac{{{k}-{fx(m)}}}{{{s}}}$。",
                [("帰無仮説を正しく立てている", 2), ("帰無仮説のもとでの期待値・標準偏差を正しく求め、標準化している", 3), ("棄却域と比べて正しく判断している", 2), ("結論を適切な言葉で述べている", 1)],
                d=4, p=8, lines=10,
                ap="主張したいこと（確率が $" + fx(p) + "$ でない）の反対を帰無仮説にする。帰無仮説のもとで観測値がどのくらい「まれ」かを $|z|$ と $1.96$ の比較で判断する。",
                steps=[f"帰無仮説：確率は ${fx(p)}$ である。", f"帰無仮説のもとで $X$ は $B\\left({n},\\ {fx(p)}\\right)$ に従い、$E(X)={fx(m)}$、$\\sigma(X)={s}$。",
                       f"$z=\\dfrac{{{k}-{fx(m)}}}{{{s}}}={float(z):.2f}$。", f"$|z|{cmp}1.96$ なので、" + concl],
                alt=["棄却域を回数で表してもよい：$|X-" + fx(m) + f"|>1.96\\times{s}={float(Fraction(196, 100) * s):g}$、すなわち $X<{float(m - Fraction(196, 100) * s):g}$ または $X>{float(m + Fraction(196, 100) * s):g}$ なら棄却。"],
                pc=[("帰無仮説", 2), ("標準化", 3), ("判断", 2), ("結論の表現", 1)],
                pit=["棄却されないときに「確率は " + f"${fx(p)}$" + " であることが示された」と書く。", "片側の確率 $0.025$ と両側の $0.05$ を混同する。"],
                chk=(f"({k}-{fpy(m)})/{s}", fpy(z), None, "intermediate"))


@gen("thinking_writing", 2, ["written_reasoning", "application"])
def test_mean(r):
    m0 = r.choice([200, 250, 300, 500, 100])
    s = r.choice([6, 8, 10, 12, 15, 20])
    n = r.choice([36, 64, 100, 144])
    se = Fraction(s, math.isqrt(n))
    reject = r.random() < 0.5
    zr = r.choice([2.2, 2.5, 3]) if reject else r.choice([0.8, 1.2, 1.5, 1.8])
    xbar = Fraction(m0) + r.choice([1, -1]) * Fraction(round(zr * se * 10), 10)
    z = (xbar - m0) / se
    rej = abs(z) > Fraction(196, 100)
    cmp = ">" if rej else "\\leqq"
    concl = ("帰無仮説は棄却される。よって、内容量の平均は表示どおりではないと判断できる。" if rej else "帰無仮説は棄却されない。よって、内容量の平均が表示どおりでないとは判断できない。")
    return desc(f"内容量が ${m0}$ g と表示された製品から無作為に ${n}$ 個を抽出したところ、内容量の標本平均は ${float(xbar):g}$ g であった。母標準偏差を ${s}$ g として、内容量の母平均は表示どおり ${m0}$ g であるといえるか。有意水準 5% で仮説検定しなさい。",
                f"$z={float(z):.2f}$。" + concl,
                f"帰無仮説「母平均は ${m0}$ g」のもとで、$\\overline{{X}}$ は近似的に $N\\left({m0},\\ \\left({fx(se)}\\right)^2\\right)$ に従う。",
                [("帰無仮説を正しく立てている", 2), ("標本平均の標準偏差を求めて標準化している", 3), ("$1.96$ と比べて正しく判断している", 2), ("結論を適切に述べている", 1)],
                d=4, p=8, lines=10,
                ap="標本平均 $\\overline{X}$ の分布は $N\\left(m,\\ \\dfrac{\\sigma^2}{n}\\right)$。帰無仮説の母平均を使って標準化し、$|z|>1.96$ かどうかで判断する。",
                steps=[f"帰無仮説：母平均は ${m0}$ g である。", f"$\\sigma(\\overline{{X}})=\\dfrac{{{s}}}{{\\sqrt{{{n}}}}}={fx(se)}$。",
                       f"$z=\\dfrac{{{float(xbar):g}-{m0}}}{{{fx(se)}}}={float(z):.2f}$。", f"$|z|{cmp}1.96$ なので、" + concl],
                alt=[f"信頼度 95% の信頼区間 $\\overline{{x}}\\pm1.96\\times{fx(se)}$ に ${m0}$ が含まれるかどうかで判断しても、同じ結論になる。"],
                pc=[("帰無仮説", 2), ("標準化", 3), ("判断", 2), ("結論", 1)],
                pit=["母標準偏差 $\\sigma$ のまま標準化し、$\\sqrt{n}$ で割り忘れる。", "棄却されないことを「表示どおりであることが証明された」と書く。"],
                chk=(f"({fpy(xbar)}-{m0})/({s}/sqrt({n}))", fpy(z), None, "intermediate"))


@gen("thinking_writing", 3, ["cross_unit", "computation"], rel=["HS-MATHA-U01"])
def hyper_dist(r):
    red, white = r.randint(2, 6), r.randint(2, 6)
    draw = r.choice([2, 2, 3])
    if draw > red + white - 1:
        draw = 2
    tot = comb(red + white, draw)
    ks = [k for k in range(0, draw + 1) if k <= red and draw - k <= white]
    ps = [Fraction(comb(red, k) * comb(white, draw - k), tot) for k in ks]
    E = sum(k * p for k, p in zip(ks, ps))
    dist = "、".join(f"$P(X={k})={fx(p)}$" for k, p in zip(ks, ps))
    return sa(f"赤玉 ${red}$ 個、白玉 ${white}$ 個が入った袋から、同時に ${draw}$ 個の玉を取り出す。取り出した赤玉の個数を $X$ とするとき、$X$ の確率分布を求め、期待値 $E(X)$ を求めなさい。",
              f"{dist}、$E(X)={fx(E)}$",
              f"組合せで確率を求める：$P(X=k)=\\dfrac{{{{}}_{{{red}}}\\mathrm{{C}}_k\\cdot{{}}_{{{white}}}\\mathrm{{C}}_{{{draw}-k}}}}{{{{}}_{{{red + white}}}\\mathrm{{C}}_{{{draw}}}}}$。", d=4, p=8, v=[fpy(E)],
              ap="確率分布は「場合の数と確率」の組合せ ${}_n\\mathrm{C}_r$ で求める。各値の確率を表にまとめ、確率の和が $1$ になることを確かめてから期待値を計算する。",
              steps=[f"全体の取り出し方は ${{}}_{{{red + white}}}\\mathrm{{C}}_{{{draw}}}={tot}$ 通り。"]
              + [f"$X={k}$：${{}}_{{{red}}}\\mathrm{{C}}_{{{k}}}\\times{{}}_{{{white}}}\\mathrm{{C}}_{{{draw - k}}}={comb(red, k) * comb(white, draw - k)}$ 通りで ${fx(p)}$。" for k, p in zip(ks, ps)]
              + ["確率の和が $1$ になることを確認する。", f"$E(X)=" + "+".join(f"{k}\\cdot{fx(p)}" for k, p in zip(ks, ps)) + f"={fx(E)}$。"],
              alt=[f"1個ずつ取り出すと考え、$i$ 番目が赤なら $1$ をとる確率変数 $Y_i$ を使うと $E(X)={draw}\\times\\dfrac{{{red}}}{{{red + white}}}={fx(Fraction(draw * red, red + white))}$ と求められる（期待値の和の性質）。"],
              pc=[("各値の確率を組合せで正しく求めている", 4), ("確率の和が $1$ であることを確認している", 1), ("期待値を正しく求めている", 3)],
              pit=["取り出す順序を区別する数え方と区別しない数え方を混在させる。", "$X=0$ の場合を落とす。"],
              chk=("[" + ", ".join(f"binomial({red},{k})*binomial({white},{draw - k})/binomial({red + white},{draw})" for k in ks) + "]", "[" + ", ".join(fpy(p) for p in ps) + "]", None, "intermediate"))


@gen("thinking_writing", 2, ["application", "condition_check", "written_reasoning"])
def sample_size(r):
    s = r.choice([5, 8, 10, 12, 15, 20, 25])
    L = r.choice([1, 2, 3, 4, 5])
    need = Fraction(392 * s, 100 * L) ** 2
    nmin = math.ceil(need)
    return num(f"母標準偏差が ${s}$ である母集団の母平均を、信頼度 95% で推定したい。信頼区間の幅（上端と下端の差）を ${L}$ 以下にするには、標本の大きさ $n$ を少なくともいくつにすればよいか。",
               str(nmin), f"幅は $2\\times1.96\\cdot\\dfrac{{{s}}}{{\\sqrt{{n}}}}$。$\\dfrac{{3.92\\times{s}}}{{\\sqrt{{n}}}}\\leqq{L}$ より $n\\geqq{float(need):g}$。", d=4, p=8,
               ap="信頼区間の幅は $2\\times1.96\\cdot\\dfrac{\\sigma}{\\sqrt{n}}$ で、$n$ が大きいほど狭くなる。幅についての不等式を $n$ について解く。",
               steps=[f"幅 $=\\dfrac{{3.92\\times{s}}}{{\\sqrt{{n}}}}\\leqq{L}$。", f"$\\sqrt{{n}}\\geqq\\dfrac{{3.92\\times{s}}}{{{L}}}={float(Fraction(392 * s, 100 * L)):g}$。",
                      f"両辺を2乗して $n\\geqq{float(need):g}$。", f"$n$ は自然数なので、最小の $n$ は ${nmin}$。"],
               alt=[f"$n={nmin}$ と $n={nmin - 1}$ を代入して幅を計算し、${L}$ 以下になるかどうかで境目を確かめる。"],
               pc=[("幅を $2\\times1.96\\cdot\\dfrac{\\sigma}{\\sqrt{n}}$ と正しく表している", 3), ("不等式を正しく解いている", 3), ("自然数の条件から最小値を答えている", 2)],
               pit=["幅を片側（$1.96\\cdot\\dfrac{\\sigma}{\\sqrt{n}}$）だけで考える。", "小数を切り捨てて条件を満たさない $n$ を答える。"],
               chk=(f"ceiling((392*{s}/(100*{L}))**2)", str(nmin)))


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(stem, wrong, step, etype, tempt, fix, ans, expl, steps, ap, alt, pit, chk=None, d=3):
    return desc(f"{stem}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい答えを求めなさい。", ans, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい解答を途中式とともに示している", 3), ("最終的な答えが正しい", 1)], d=d, p=6, lines=6,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい途中式", 3), ("正しい答え", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix), chk=chk)


@gen("error_correction", 3, ["common_error", "computation"])
def err_var_linear(r):
    v = r.choice([2, 3, 4, 5, 6, 9])
    a = r.choice([2, 3, 4, -2, -3])
    b = r.choice([x for x in range(-8, 9) if x])
    m = r.randint(-3, 8)
    Y = f"{a}X{'+' if b > 0 else '-'}{abs(b)}"
    wrong = f"$V(Y)={a}V(X){'+' if b > 0 else '-'}{abs(b)}={a * v + b}$"
    fix = f"$V(Y)=({a})^2V(X)={a * a * v}$"
    return err_item(f"確率変数 $X$ の期待値が ${m}$、分散が ${v}$ のとき、$Y={Y}$ の分散を求めなさい。", wrong, "分散の性質（期待値の性質と同じ形にした部分）", "formula",
                    "期待値の性質 $E(aX+b)=aE(X)+b$ と同じ形で分散も計算できると思いこんでいる。分散が「ずれの2乗」であることを意識していない。",
                    fix, f"$V(Y)={a * a * v}$", "分散は平均からのずれの2乗の期待値。$X$ を $a$ 倍するとずれは $a$ 倍、2乗は $a^2$ 倍。$b$ を加えてもずれは変わらない。",
                    [f"$V(aX+b)=a^2V(X)$。", f"$V(Y)=({a})^2\\times{v}={a * a * v}$。"],
                    "性質の証明（ずれ $a(x_k-m)$ を2乗する）にもどれば、$a^2$ になり $b$ が消える理由が分かる。",
                    ["具体例：$X$ が $0,\\ 2$ を確率 $\\dfrac{1}{2}$ ずつとる（分散 $1$）とき、$" + Y + "$ の値を計算して分散を直接求めると $" + str(a * a) + "$ になる。"],
                    ["分散に定数 $b$ を加える。", "$a$ を2乗しない。"],
                    chk=(f"({a})**2*{v}", str(a * a * v), None, "intermediate"), d=2)


@gen("error_correction", 3, ["common_error", "concept"])
def err_binom_sd(r):
    n, p, ctx = r.choice(BINOMS)
    m, v, s = bin_ms(n, p)
    form = r.choice(["np", "nosqrt"])
    if form == "np":
        wrong = f"$X$ は $B\\left({n},\\ {fx(p)}\\right)$ に従うので、標準偏差は $\\sqrt{{np}}=\\sqrt{{{fx(m)}}}$"
        step, tempt = "分散の公式（$1-p$ を掛け忘れた部分）", "期待値 $np$ の形に引きずられ、分散も $np$ と覚え違えている。"
    else:
        wrong = f"$X$ は $B\\left({n},\\ {fx(p)}\\right)$ に従うので、標準偏差は $np(1-p)={fx(v)}$"
        step, tempt = "分散と標準偏差の区別（平方根をとっていない部分）", "分散の公式 $np(1-p)$ を覚えていて、そのまま標準偏差として答えてしまう。"
    fix = f"$V(X)=np(1-p)={fx(v)}$、$\\sigma(X)=\\sqrt{{{fx(v)}}}={s}$"
    return err_item(f"{ctx[0]}を ${n}$ 回くり返すとき、{ctx[1]}回数 $X$ の標準偏差を求めなさい。", wrong, step, "formula", tempt, fix, f"$\\sigma(X)={s}$",
                    "二項分布では $V(X)=np(1-p)$、$\\sigma(X)=\\sqrt{np(1-p)}$。",
                    [f"$V(X)={n}\\times{fx(p)}\\times{fx(1 - p)}={fx(v)}$。", f"$\\sigma(X)=\\sqrt{{{fx(v)}}}={s}$。"],
                    "1回分の分散 $p(1-p)$ を $n$ 倍したものが分散で、その平方根が標準偏差、と構造で覚える。",
                    ["$p=1$（必ず起こる）のとき回数は常に $n$ でばらつきは $0$ のはず。$np(1-p)$ なら $0$ になるが、$np$ では $0$ にならないことから公式を確かめられる。"],
                    ["分散と標準偏差を取り違える。"],
                    chk=(f"sqrt({n}*{fpy(p)}*(1-{fpy(p)}))", str(s), None, "intermediate"))


@gen("error_correction", 2, ["common_error", "concept"])
def err_normal_tail(r):
    a = r.choice([0.5, 0.8, 1, 1.2, 1.25, 1.5, 1.75, 2, 2.25, 2.5])
    form = r.choice(["ge", "le"])
    ev = f"Z\\geqq{zt(a)}" if form == "ge" else f"Z\\leqq-{zt(a)}"
    wrong = f"$P({ev})=p({zt(a)})={u(a)}$" if r.random() < 0.5 else f"$P({ev})=0.5+p({zt(a)})={Decimal('0.5') + u(a)}$"
    right = Decimal("0.5") - u(a)
    return err_item(f"$Z$ が標準正規分布 $N(0,\\,1)$ に従うとき、$P({ev})$ を求めなさい。{table_note([a])}", wrong, "求める面積の表し方", "concept",
                    "表の値 $p(z)$ が「どの部分の面積か」を図で確かめずに、数値だけを使っている。",
                    f"$P({ev})=0.5-p({zt(a)})={right}$", f"${right}$", f"$p({zt(a)})$ は $0$ から ${zt(a)}$ までの面積。求めるのはその外側なので、片側全体 $0.5$ から引く。",
                    ["曲線をかき、求める部分に斜線を引く。", f"片側の面積 $0.5$ から $p({zt(a)})$ を引く。", f"$0.5-{u(a)}={right}$。"],
                    "答えが $0.5$ より大きいか小さいかを図で見当をつけてから計算する。",
                    [f"$z={zt(a)}$ は平均より右（左）にあるので、その外側の確率は $0.5$ より小さいはず。生徒の答えはこの見当と合わない。"],
                    ["表の値をそのまま答える。"],
                    chk=(f"0.5-{u(a)}", str(right), None, "intermediate"), d=2)


@gen("error_correction", 2, ["common_error", "condition_check"])
def err_test_concl(r):
    n, p, ctx = r.choice([b for b in BINOMS if b[0] >= 180])
    m, v, s = bin_ms(n, p)
    d = math.floor(r.choice([0.5, 1, 1.2, 1.5]) * s)
    k = int(m + r.choice([1, -1]) * max(d, 1))
    z = Fraction(k - m) / s
    wrong = f"$z=\\dfrac{{{k}-{fx(m)}}}{{{s}}}={float(z):.2f}$ で $|z|\\leqq1.96$ だから帰無仮説は正しい。よって、確率は ${fx(p)}$ であることが証明された。"
    fix = f"$|z|={abs(float(z)):.2f}\\leqq1.96$ なので帰無仮説は棄却されない。確率が ${fx(p)}$ でないとは判断できない（確率が ${fx(p)}$ であると証明されたわけではない）。"
    return err_item(f"{ctx[0]}を ${n}$ 回くり返したところ、{ctx[1]}回数は ${k}$ 回であった。{ctx[1]}確率は ${fx(p)}$ でないといえるか。有意水準 5% で仮説検定しなさい（二項分布は正規分布で近似する）。",
                    wrong, "結論の述べ方（棄却されないことを「正しいと証明された」とした部分）", "interpretation",
                    "「棄却されない」を「正しい」と同じ意味に受け取りやすい。検定は帰無仮説を否定できるかどうかを調べる方法であり、肯定する方法ではない。",
                    fix, "帰無仮説は棄却されず、確率が " + f"${fx(p)}$" + " でないとは判断できない",
                    "検定で帰無仮説が棄却されないのは「データが帰無仮説と矛盾するとまではいえない」というだけで、帰無仮説が正しいことの証明にはならない。",
                    [f"帰無仮説：確率は ${fx(p)}$。$E(X)={fx(m)}$、$\\sigma(X)={s}$。", f"$z={float(z):.2f}$、$|z|\\leqq1.96$。", "帰無仮説は棄却されない。", "結論：確率が " + f"${fx(p)}$" + " でないとは判断できない。"],
                    "結論は「〜と判断できる」「〜とは判断できない」のどちらかの形で書く。",
                    ["同じデータでも、確率が少しだけ違う値（例えば $" + fx(p) + "$ に近い別の値）を帰無仮説にしても棄却されないことがある。棄却されないことが「その値で正しい」ことを意味しないのはこのため。"],
                    ["「棄却されない」を「正しいと証明された」と言いかえる。"],
                    chk=(f"({k}-{fpy(m)})/{s}", fpy(z), None, "intermediate"))


GENERATORS = [expect_var, linear_transform, binom_ev, standardize, normal_prob,
              normal_x_prob, binom_normal, sample_mean, ci_mean, ci_prop,
              test_binom, test_mean, hyper_dist, sample_size,
              err_var_linear, err_binom_sd, err_normal_tail, err_test_concl]
