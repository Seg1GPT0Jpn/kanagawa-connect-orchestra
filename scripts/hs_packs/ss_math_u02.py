"""単元パック：二次試験対策 数学　記述式計算問題（微積分・確率・ベクトル）。"""
import math
from fractions import Fraction as F

import sympy as sp

from banks._common import desc, num, sa
from hs_pack_lib import board, check, definition, derivation, example, gen, guide, intro, lesson, poly, summary, theorem, tp

UNIT_ID = "SS-MATH-U02"

PREREQUISITES = [
    ("HS-MATH2-U06", "導関数・接線・増減表・定積分と面積の計算"),
    ("HS-MATHA-U01", "反復試行の確率・条件付き確率・余事象の考え方"),
    ("HS-MATHC-U01", "ベクトルの内積・大きさ・内分点の位置ベクトルと一次独立による係数比較"),
    ("HS-MATHB-U01", "漸化式 $a_{n+1}=pa_n+q$ の一般項の求め方"),
]
EXTENSIONS = [
    ("HS-MATH3-U03", "面積の計算を、回転体の体積や置換積分・部分積分を用いた求積へ広げる"),
    ("HS-MATHB-U02", "確率の計算を、確率変数の期待値・分散や二項分布の考察へつなげる"),
    ("SS-MATH-U01", "計算答案で身につけた論理の示し方を、証明問題の答案作成に生かす"),
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


def fs(v):
    v = F(v)
    return str(v.numerator) if v.denominator == 1 else f"{v.numerator}/{v.denominator}"


def lt(v):
    return sp.latex(sp.nsimplify(v))


def py(*coefs, var="x"):
    deg = len(coefs) - 1
    return "+".join(f"({fp(c)})*{var}**{deg - i}" for i, c in enumerate(coefs))


def ev(coefs, x):
    x = F(x)
    deg = len(coefs) - 1
    return sum(F(c) * x ** (deg - i) for i, c in enumerate(coefs))


def fac(c, var="x"):
    c = F(c)
    if c == 0:
        return var
    return f"({var}{'-' if c > 0 else '+'}{ft(abs(c))})"


def vcomb(al, be, u="\\vec{a}", v="\\vec{b}"):
    """α a + β b の LaTeX（係数は有理数）。"""
    out = ""
    for c, s in ((F(al), u), (F(be), v)):
        if c == 0:
            continue
        mag = "" if abs(c) == 1 else ft(abs(c))
        sign = "-" if c < 0 else ("+" if out else "")
        out += sign + mag + s
    return out or "\\vec{0}"


def coef(c, first=False):
    c = F(c)
    if c == 1:
        s = ""
    elif c == -1:
        s = "-"
    else:
        s = ft(c)
    if not first and not s.startswith("-"):
        s = "+" + s
    return s


VA, VB = "\\vec{a}", "\\vec{b}"


def c1(v):
    """係数 1 を省いた表記。"""
    return "" if v == 1 else str(v)


# ----------------------------------------------------------------------
# 授業プリント
# ----------------------------------------------------------------------

LESSON = lesson(
    goals=["二次試験の記述式計算問題で、答えだけでなく「立式の根拠・条件の確認・結論」を採点者に伝わる形で書ける。",
           "微積分（接線と囲まれた部分の面積・最大最小・積分方程式）、確率（反復試行・条件付き確率・確率漸化式）、ベクトル（交点の位置ベクトル・内積と大きさ）の頻出型を、導出の筋道とともに使いこなせる。",
           "計算の見通しを立てて時間内に処理し、検算で誤りを自分で見つけられる。"],
    duration=100,
    readiness=["三次関数の導関数・接線の方程式・定積分の計算ができる（数学Ⅱ）。",
               "反復試行の確率 ${}_n\\mathrm{C}_r\\,p^r(1-p)^{n-r}$ を計算できる（数学A）。",
               "内分点の位置ベクトルと内積の計算ができる（数学C）。",
               "漸化式 $a_{n+1}=pa_n+q$ を解ける（数学B）。"],
    flow=[("導入：記述式計算答案の採点", 10, "同じ答えでも点数が変わる答案を比べ、書くべき要素を確認する"),
          ("微積分：接線と面積", 25, "$\\dfrac{1}{12}$ 公式の導出と例題1、上下関係・交点の確認"),
          ("確率：反復試行と条件付き確率", 25, "優勝確率（例題2）、条件付き確率の立式、確率漸化式"),
          ("ベクトル：交点の位置ベクトル", 25, "2通りに表して係数比較（例題3）、内積と大きさ"),
          ("まとめと時間配分", 15, "1題 25〜30 分の配分と、検算の方法を確認する")],
    sections=[
        intro("in1", "記述式計算問題は「答案の読みやすさ」も得点の一部",
              "二次試験の数学では、答えの数値だけでなく、その数値に至る過程が採点される。採点者は「何を文字でおいたか」「どの公式・定理を使ったか」「条件（範囲・場合分け）を確かめたか」を順に確認する。計算の途中で誤っても、方針と立式が正しければ部分点がつく。逆に、答えが正しくても根拠のない飛躍があれば減点される。本時は、微積分・確率・ベクトルの3分野について、出題頻度の高い型と答案の書き方を整理する。",
              bullets=["最初に「おいた文字」と「求めるもの」を1行で書く（例：「接点の $x$ 座標を $t$ とおく」）。",
                       "公式を使うときは、使える条件（区間内の上下関係・独立な試行・一次独立など）を確かめたことを書く。",
                       "最後に「よって、求める〇〇は △△」と結論を明示する。"],
              points=[tp("答えが同じ2つの答案（立式を書いたものと、計算だけのもの）を見せ、点差の理由を考えさせる。", ask="どちらの答案が高く評価されるか。理由は何か。", expect="立式の根拠が書かれた答案。途中で誤っても部分点がつくから。", timing="導入の冒頭"),
                      tp("計算が終わったら、別の方法（具体的な値の代入・概算・図）で答えを確かめる習慣をつけさせる。", caution="検算をしないまま次の問題に進み、符号や係数の誤りで完答を逃す答案が多い。")]),
        derivation("dv1", "三次関数と接線で囲まれた部分の面積（$\\dfrac{1}{12}$ 公式）の導出",
                   ["三次関数 $y=f(x)=ax^3+\\cdots$ と、$x=\\alpha$ で接し $x=\\beta$ で交わる直線 $y=g(x)$ を考える。$f(x)-g(x)$ は $x=\\alpha$ を重解、$x=\\beta$ を解にもつので $f(x)-g(x)=a(x-\\alpha)^2(x-\\beta)$。",
                    "$x-\\beta=(x-\\alpha)-(\\beta-\\alpha)$ と書きかえると $(x-\\alpha)^2(x-\\beta)=(x-\\alpha)^3-(\\beta-\\alpha)(x-\\alpha)^2$。",
                    "$\\displaystyle\\int_\\alpha^\\beta(x-\\alpha)^3dx=\\dfrac{(\\beta-\\alpha)^4}{4}$、$\\displaystyle\\int_\\alpha^\\beta(\\beta-\\alpha)(x-\\alpha)^2dx=\\dfrac{(\\beta-\\alpha)^4}{3}$。",
                    "差をとって $\\displaystyle\\int_\\alpha^\\beta(x-\\alpha)^2(x-\\beta)\\,dx=-\\dfrac{(\\beta-\\alpha)^4}{12}$。",
                    "よって、囲まれた部分の面積は $S=\\dfrac{|a|}{12}|\\beta-\\alpha|^4$。また、解と係数の関係から $2\\alpha+\\beta=-\\dfrac{b}{a}$（$f(x)=ax^3+bx^2+\\cdots$）で、交点 $\\beta$ がすぐに求まる。"],
                   body="記述式の答案では、公式の結果だけを書くと根拠不足とされることがある。$\\dfrac{1}{12}$ 公式は検算用に使い、答案には定積分の式と因数分解した形を必ず書く。",
                   points=[tp("$\\dfrac{1}{6}$ 公式の導出と同じ「$(x-\\alpha)$ のかたまりで積分する」発想であることを強調する。", ask="なぜ $x-\\beta$ を $(x-\\alpha)-(\\beta-\\alpha)$ と書きかえるのか。", expect="すべてを $x-\\alpha$ の累乗で表すと、下端 $\\alpha$ を代入した値が 0 になり計算が軽くなるから。")]),
        theorem("th1", "条件付き確率と乗法定理",
                "$$P_A(B)=\\dfrac{P(A\\cap B)}{P(A)},\\qquad P(A\\cap B)=P(A)\\,P_A(B)$$",
                ["$P(A)>0$", "「$A$ が起こったとき $B$ が起こる確率」は $P_A(B)$。分母は条件として与えられた事象 $A$ の確率。"],
                body="「結果から原因をさかのぼる」問題（赤玉が出たとき、それが袋 A から取り出されたものである確率など）では、分母 $P(\\text{結果})$ を、原因ごとに場合分けした和で求める。",
                proof=["全事象 $U$ の根元事象が同様に確からしいとき、$A$ が起こったという条件の下では、$A$ を新たな全事象とみなせる。",
                       "その中で $B$ が起こるのは $A\\cap B$ の場合なので、$P_A(B)=\\dfrac{n(A\\cap B)}{n(A)}$。",
                       "分母・分子を $n(U)$ で割ると $P_A(B)=\\dfrac{P(A\\cap B)}{P(A)}$。両辺に $P(A)$ をかけると乗法定理が得られる。"],
                points=[tp("「$P_A(B)$ と $P_B(A)$ の取り違え」を図（樹形図・面積図）で確認させる。", caution="分母に全体の確率 1 を使い、$P(A\\cap B)$ をそのまま答える誤りが多い。")]),
        definition("df1", "ベクトルの一次独立と係数比較",
                   "平面上の2つのベクトル $\\vec{a},\\ \\vec{b}$ が $\\vec{a}\\neq\\vec{0},\\ \\vec{b}\\neq\\vec{0}$ で平行でないとき、$\\vec{a},\\ \\vec{b}$ は一次独立であるという。このとき、平面上のすべてのベクトルはただ1通りに $s\\vec{a}+t\\vec{b}$ と表せる。",
                   formula="$$s\\vec{a}+t\\vec{b}=s'\\vec{a}+t'\\vec{b}\\iff s=s'\\ \\text{かつ}\\ t=t'\\qquad(\\vec{a},\\ \\vec{b}\\ \\text{は一次独立})$$",
                   conditions=["係数比較の前に「$\\vec{a},\\ \\vec{b}$ は一次独立であるから」と根拠を書く。", "2直線の交点は、それぞれの直線上の点として2通りに表し、係数を比較して求める。"],
                   points=[tp("一次独立でない例（$\\vec{b}=2\\vec{a}$ など）では係数比較ができないことを示し、条件を書く意味を理解させる。", ask="$\\vec{b}=2\\vec{a}$ のとき、$\\vec{a}+\\vec{b}=3\\vec{a}+0\\vec{b}$ はどうなるか。", expect="両辺とも $3\\vec{a}$ で等しいが係数は一致しない。係数比較には一次独立が必要。")]),
        example("ex1", "例題1　三次関数と接線で囲まれた部分の面積",
                "曲線 $C:\\ y=x^3-3x^2+2$ 上の点 $(0,\\ 2)$ における接線を $\\ell$ とする。$C$ と $\\ell$ で囲まれた部分の面積 $S$ を求めよ。",
                ["$y'=3x^2-6x$ より、$x=0$ での傾きは 0。$\\ell:\\ y=2$。",
                 "$C$ と $\\ell$ の共有点：$x^3-3x^2+2-2=x^2(x-3)=0$ より $x=0$（接点）、$3$。",
                 "$0\\leqq x\\leqq3$ で $x^2(x-3)\\leqq0$ なので $\\ell$ が上。",
                 "$S=\\displaystyle\\int_0^3\\{2-(x^3-3x^2+2)\\}dx=\\int_0^3(3x^2-x^3)dx=27-\\dfrac{81}{4}=\\dfrac{27}{4}$。"],
                "$S=\\dfrac{27}{4}$",
                thinking="接線の式を引くと「接点で重解」の因数分解 $x^2(x-3)$ が現れる。検算として $\\dfrac{(3-0)^4}{12}=\\dfrac{27}{4}$ と一致することを確かめる。",
                points=[tp("答案には上下関係の確認（区間内の1点での値の比較）を必ず書かせる。", ask="$x=1$ で $C$ と $\\ell$ の $y$ 座標はそれぞれいくつか。", expect="$C$ は 0、$\\ell$ は 2 で、$\\ell$ が上。")]),
        example("ex2", "例題2　反復試行と優勝の確率",
                "A と B が試合をくり返し、先に3勝した方を優勝とする。1試合で A が勝つ確率は $\\dfrac{2}{3}$ で、引き分けはなく、各試合の結果は独立とする。A が優勝する確率を求めよ。",
                ["A が優勝するのは、最後の試合に A が勝ち、それまでに A が2勝、B が $j$ 勝（$j=0,\\ 1,\\ 2$）している場合。",
                 "$j$ 勝の場合の確率は ${}_{2+j}\\mathrm{C}_{j}\\left(\\dfrac{2}{3}\\right)^2\\left(\\dfrac{1}{3}\\right)^j\\times\\dfrac{2}{3}$。",
                 "和は $\\left(\\dfrac{2}{3}\\right)^3\\left(1+3\\cdot\\dfrac{1}{3}+6\\cdot\\dfrac{1}{9}\\right)=\\dfrac{8}{27}\\cdot\\dfrac{8}{3}$。"],
                "$\\dfrac{64}{81}$",
                thinking="「最後の試合は優勝する側が勝つ」ことに注目して、それより前の試合の勝ち負けの並べ方を数える。",
                points=[tp("最後の試合を含めて ${}_{3+j}\\mathrm{C}_{3}$ と数える誤りを、具体的な並び（A が3連勝した後に試合はない）で確認させる。")],
                misconceptions=[("5試合中 A が3勝する確率 ${}_5\\mathrm{C}_3\\left(\\dfrac{2}{3}\\right)^3\\left(\\dfrac{1}{3}\\right)^2$ が答え", "優勝が決まった後は試合をしない。最後の試合を A の勝ちに固定して場合分けする")]),
        example("ex3", "例題3　2直線の交点の位置ベクトル",
                "$\\triangle\\mathrm{OAB}$ において、$\\overrightarrow{\\mathrm{OA}}=\\vec{a},\\ \\overrightarrow{\\mathrm{OB}}=\\vec{b}$ とする。辺 AB を $1:2$ に内分する点を P、辺 OB の中点を Q とし、線分 OP と線分 AQ の交点を R とする。$\\overrightarrow{\\mathrm{OR}}$ を $\\vec{a},\\ \\vec{b}$ で表せ。",
                ["$\\overrightarrow{\\mathrm{OP}}=\\dfrac{2\\vec{a}+\\vec{b}}{3}$。R は OP 上なので $\\overrightarrow{\\mathrm{OR}}=k\\overrightarrow{\\mathrm{OP}}=\\dfrac{2k}{3}\\vec{a}+\\dfrac{k}{3}\\vec{b}$。",
                 "R は AQ 上なので $\\overrightarrow{\\mathrm{OR}}=(1-s)\\vec{a}+\\dfrac{s}{2}\\vec{b}$。",
                 "$\\vec{a},\\ \\vec{b}$ は一次独立なので $\\dfrac{2k}{3}=1-s,\\ \\dfrac{k}{3}=\\dfrac{s}{2}$。",
                 "解いて $k=\\dfrac{3}{4},\\ s=\\dfrac{1}{2}$。"],
                "$\\overrightarrow{\\mathrm{OR}}=\\dfrac{1}{2}\\vec{a}+\\dfrac{1}{4}\\vec{b}$",
                thinking="交点は「2つの直線のどちらの上にもある点」。それぞれの直線上の点として媒介変数で表し、係数を比べる。",
                points=[tp("求めた $\\overrightarrow{\\mathrm{OR}}$ の係数の和が 1 になっていない（OP 上の点だから）ことと、AQ 上の点としての表し方で係数の和が 1 になることを確認させる。", timing="例題3の後")]),
        board("bd1", "板書案",
              [("① 微積分", ["$f(x)-g(x)=a(x-\\alpha)^2(x-\\beta)$", "$S=\\dfrac{|a|}{12}|\\beta-\\alpha|^4$（検算用）", "上下関係は区間内の1点で確認", "例：$y=x^3-3x^2+2,\\ \\ell:y=2$ → $\\dfrac{27}{4}$"]),
               ("② 確率", ["$P_A(B)=\\dfrac{P(A\\cap B)}{P(A)}$", "原因が複数 → 分母を場合分けの和で", "優勝：最後の試合を固定", "漸化式 $p_{n+1}=(1-2r)p_n+r$"]),
               ("③ ベクトル", ["交点は2通りに表す", "「一次独立より」係数比較", "$|\\vec{a}+t\\vec{b}|^2=|\\vec{a}|^2+2t\\,\\vec{a}\\cdot\\vec{b}+t^2|\\vec{b}|^2$", "例：$\\overrightarrow{\\mathrm{OR}}=\\dfrac{1}{2}\\vec{a}+\\dfrac{1}{4}\\vec{b}$"])],
              points=[tp("各列に「答案に必ず書く一文」（上下関係の確認・分母の意味・一次独立）を赤で添える。")]),
        guide("gd1", "指導ガイド（口頭で補う要点と時間配分）",
              [tp("記述式の大問は1題 25〜30 分が目安。最初の 3 分で「何を文字でおくか」「どの型か」を決め、計算に入る前に方針を1行書かせる。", timing="導入の後"),
               tp("面積の問題では、公式の結果を答案の根拠にせず、定積分の式を書いたうえで公式を検算に使わせる。", ask="$\\dfrac{1}{12}$ 公式だけを書いた答案はどう評価されうるか。", expect="立式の根拠が示されていないとして減点されうる。"),
               tp("確率の問題では、根元事象が同様に確からしいかを意識させる（玉は区別する、さいころは区別する）。", caution="区別しない数え方で確率を計算すると、同様に確からしくない場合を数えることになる。"),
               tp("ベクトルの交点では、係数比較の前に「$\\vec{a},\\ \\vec{b}$ は一次独立」と必ず書かせる。", timing="例題3の後"),
               tp("誤答訂正（問題プリントD）では、誤りの種類（公式・概念・条件）を言葉で分類させてから訂正させる。")],
              misconceptions=[("$|\\vec{a}+t\\vec{b}|^2=|\\vec{a}|^2+t^2|\\vec{b}|^2$", "内積の項 $2t\\,\\vec{a}\\cdot\\vec{b}$ が必要。文字式の展開と同じ形になる"),
                              ("さいころを $n$ 回投げて最大値が $k$ である確率は $\\left(\\dfrac{k}{6}\\right)^n$", "それは「最大値が $k$ 以下」の確率。「$k-1$ 以下」の確率を引く"),
                              ("曲線外の点 $(p,\\ q)$ から引いた接線の傾きは $f'(p)$", "接点を $(t,\\ f(t))$ とおき、接線が $(p,\\ q)$ を通る条件から $t$ を求める")]),
        summary("sm1", "まとめ",
                ["記述式計算の答案は「おいた文字・方針 → 立式と根拠 → 計算 → 結論」の順に書く。",
                 "三次関数と接線：$f(x)-g(x)=a(x-\\alpha)^2(x-\\beta)$、面積は $\\dfrac{|a|}{12}|\\beta-\\alpha|^4$ で検算する。",
                 "確率：条件付き確率は分母が条件の事象。優勝の確率は最後の試合を固定する。確率の推移は漸化式で表す。",
                 "ベクトル：交点は2通りに表して一次独立から係数比較。大きさは2乗して内積で展開する。",
                 "答えが出たら、別の方法や具体的な値で検算する。"]),
        check("ck1", "確認問題",
              [("$\\displaystyle\\int_\\alpha^\\beta(x-\\alpha)^2(x-\\beta)\\,dx$ を $\\alpha,\\ \\beta$ で表せ。", "$-\\dfrac{(\\beta-\\alpha)^4}{12}$"),
               ("袋 A（赤2・白1）と袋 B（赤1・白2）から1つを等確率で選び玉を1個取り出す。赤玉だったとき、袋 A から取り出した確率は。", "$\\dfrac{\\frac{1}{2}\\cdot\\frac{2}{3}}{\\frac{1}{2}\\cdot\\frac{2}{3}+\\frac{1}{2}\\cdot\\frac{1}{3}}=\\dfrac{2}{3}$"),
               ("$|\\vec{a}|=2,\\ |\\vec{b}|=1,\\ \\vec{a}\\cdot\\vec{b}=1$ のとき、$|\\vec{a}-\\vec{b}|$ を求めよ。", "$|\\vec{a}-\\vec{b}|^2=4-2+1=3$ より $\\sqrt{3}$"),
               ("$p_1=\\dfrac{2}{3},\\ p_{n+1}=\\dfrac{1}{3}p_n+\\dfrac{1}{3}$ の一般項を求めよ。", "$p_n-\\dfrac{1}{2}=\\dfrac{1}{6}\\left(\\dfrac{1}{3}\\right)^{n-1}$ より $p_n=\\dfrac{1}{2}+\\dfrac{1}{2}\\left(\\dfrac{1}{3}\\right)^n$")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

@gen("basic_check", 4, ["computation", "condition_check"])
def a_abs_integral(r):
    kind = r.choice(["xc", "sq"])
    if kind == "xc":
        c = r.randint(1, 4)
        b = c + r.randint(1, 3)
        expr_tex = f"x^2-{c}x"
        Fs = f"x**2-{c}*x"
        a0 = 0
        cut = c
    else:
        c = r.randint(1, 3)
        b = c + r.randint(1, 3)
        expr_tex = f"x^2-{c * c}"
        Fs = f"x**2-{c * c}"
        a0 = 0
        cut = c
    x = sp.Symbol("x")
    fe = sp.sympify(Fs)
    S1 = abs(sp.integrate(fe, (x, a0, cut)))
    S2 = abs(sp.integrate(fe, (x, cut, b)))
    S = sp.nsimplify(S1 + S2)
    Sf = F(int(sp.fraction(S)[0]), int(sp.fraction(S)[1]))
    return num(f"定積分 $\\displaystyle\\int_{{0}}^{{{b}}}\\left|{expr_tex}\\right|dx$ を求めなさい。絶対値をはずすための場合分けを答案に示すこと。",
               fs(Sf), f"$x={cut}$ を境に ${expr_tex}$ の符号が変わる。$0\\leqq x\\leqq{cut}$ では $-({expr_tex})$、${cut}\\leqq x\\leqq{b}$ では ${expr_tex}$ を積分して和をとる。", d=2, disp=f"${ft(Sf)}$",
               ap="絶対値を含む定積分は、中身の符号が変わる点で区間を分け、それぞれの区間で絶対値をはずす。",
               steps=[f"${expr_tex}=0$ となる $x$（区間内）は $x={cut}$。",
                      f"$0\\leqq x\\leqq{cut}$ で ${expr_tex}\\leqq0$、${cut}\\leqq x\\leqq{b}$ で ${expr_tex}\\geqq0$。",
                      f"$\\displaystyle\\int_0^{{{cut}}}\\{{-({expr_tex})\\}}dx={lt(S1)}$、$\\displaystyle\\int_{{{cut}}}^{{{b}}}({expr_tex})dx={lt(S2)}$。",
                      f"和は ${ft(Sf)}$。"],
               alt=[f"$y=|{expr_tex}|$ のグラフ（$x$ 軸より下の部分を折り返したもの）と $x$ 軸で囲まれた面積と考え、各部分の面積を求めて加えても同じ値になる。"],
               pc=[("符号が変わる点で区間を分けている", 1), ("値を正しく求めている", 1)],
               pit=["絶対値をはずさずに $\\displaystyle\\int_0^{" + str(b) + "}(" + expr_tex + ")dx$ を計算し、打ち消し合った値を答える。", "区間ごとの符号を逆に判断する。"],
               chk=(f"Abs(integrate({Fs}, [x, 0, {cut}]))+Abs(integrate({Fs}, [x, {cut}, {b}]))", fp(Sf)))


@gen("basic_check", 4, ["computation", "concept"])
def a_dice_extreme(r):
    n = r.choice([2, 3, 4, 5])
    kind = r.choice(["max", "min", "maxle", "minge"])
    if kind == "max":
        k = r.randint(2, 6)
        P = F(k ** n - (k - 1) ** n, 6 ** n)
        what, cond = f"出た目の最大値が ${k}$ である", f"「すべて ${k}$ 以下」から「すべて ${k - 1}$ 以下」を除く"
        expr = f"Rational({k}**{n}-{k - 1}**{n}, 6**{n})"
        stp = [f"すべて ${k}$ 以下：$\\left(\\dfrac{{{k}}}{{6}}\\right)^{{{n}}}$。", f"すべて ${k - 1}$ 以下：$\\left(\\dfrac{{{k - 1}}}{{6}}\\right)^{{{n}}}$。"]
    elif kind == "min":
        k = r.randint(1, 5)
        P = F((7 - k) ** n - (6 - k) ** n, 6 ** n)
        what, cond = f"出た目の最小値が ${k}$ である", f"「すべて ${k}$ 以上」から「すべて ${k + 1}$ 以上」を除く"
        expr = f"Rational({7 - k}**{n}-{6 - k}**{n}, 6**{n})"
        stp = [f"すべて ${k}$ 以上：$\\left(\\dfrac{{{7 - k}}}{{6}}\\right)^{{{n}}}$。", f"すべて ${k + 1}$ 以上：$\\left(\\dfrac{{{6 - k}}}{{6}}\\right)^{{{n}}}$。"]
    elif kind == "maxle":
        k = r.randint(2, 5)
        P = 1 - F(k ** n, 6 ** n)
        what, cond = f"出た目の最大値が ${k + 1}$ 以上である", f"余事象「すべて ${k}$ 以下」の確率を 1 から引く"
        expr = f"1-Rational({k}**{n}, 6**{n})"
        stp = [f"余事象は「すべて ${k}$ 以下」で、確率 $\\left(\\dfrac{{{k}}}{{6}}\\right)^{{{n}}}$。", "1 から引く。"]
    else:
        k = r.randint(2, 5)
        P = 1 - F((6 - k + 1) ** n, 6 ** n)
        what, cond = f"出た目の最小値が ${k - 1}$ 以下である", f"余事象「すべて ${k}$ 以上」の確率を 1 から引く"
        expr = f"1-Rational({7 - k}**{n}, 6**{n})"
        stp = [f"余事象は「すべて ${k}$ 以上」で、確率 $\\left(\\dfrac{{{7 - k}}}{{6}}\\right)^{{{n}}}$。", "1 から引く。"]
    return num(f"1個のさいころを ${n}$ 回続けて投げるとき、{what}確率を求めなさい。",
               fs(P), f"{cond}と考える。答えは ${ft(P)}$。", d=2, disp=f"${ft(P)}$",
               ap="最大値・最小値の確率は「すべての目が〇以下（以上）」という事象の差や余事象で表すと、場合分けせずに求められる。",
               steps=stp + [f"求める確率は ${ft(P)}$。"],
               alt=["$n$ が小さいときは、目の組を数え上げる（例えば最大値の目が何回出るかで場合分けする）方法で確かめられる。"],
               pc=[("事象を「すべて〜以下（以上）」の差や余事象で表している", 1), ("確率を正しく計算している", 1)],
               pit=["「最大値が $k$」の確率を $\\left(\\dfrac{k}{6}\\right)^n$ としてしまう（$k$ 以下との混同）。", "差をとるときに引く事象の境目を1つずらす。"],
               chk=(expr, fp(P)))


@gen("basic_check", 4, ["computation"])
def a_vec_norm(r):
    p, q = r.randint(1, 5), r.randint(1, 5)
    ang = r.choice([60, 90, 120])
    d = {60: F(p * q, 2), 90: F(0), 120: F(-p * q, 2)}[ang]
    while True:
        s, t = r.choice([1, 2, 3, -1, -2]), r.choice([1, 2, 3, -1, -2, -3])
        val2 = s * s * p * p + 2 * s * t * d + t * t * q * q
        if val2 > 0:
            break
    val = sp.sqrt(sp.Rational(val2.numerator, val2.denominator))
    vt = vcomb(s, t)
    ang_tex = {60: "60^\\circ", 90: "90^\\circ", 120: "120^\\circ"}[ang]
    return sa(f"$|\\vec{{a}}|={p},\\ |\\vec{{b}}|={q}$ で、$\\vec{{a}}$ と $\\vec{{b}}$ のなす角が ${ang_tex}$ であるとき、$|{vt}|$ を求めなさい。",
              f"${sp.latex(val)}$",
              f"$\\vec{{a}}\\cdot\\vec{{b}}={p}\\cdot{q}\\cos{ang_tex}={ft(d)}$。$|{vt}|^2={s * s}|\\vec{{a}}|^2{'+' if 2 * s * t >= 0 else '-'}{abs(2 * s * t)}\\vec{{a}}\\cdot\\vec{{b}}+{t * t}|\\vec{{b}}|^2={ft(val2)}$。", d=2,
              v=[str(val)],
              ap="ベクトルの大きさは直接計算できないので、2乗して内積で展開する。内積は $|\\vec{a}||\\vec{b}|\\cos\\theta$ で求める。",
              steps=[f"$\\vec{{a}}\\cdot\\vec{{b}}={p}\\times{q}\\times\\cos{ang_tex}={ft(d)}$。",
                     f"$|{vt}|^2={s * s}\\times{p * p}{'+' if 2 * s * t * d >= 0 else '-'}{ft(abs(2 * s * t * d))}+{t * t}\\times{q * q}={ft(val2)}$。",
                     f"$|{vt}|=\\sqrt{{{ft(val2)}}}" + ("" if sp.latex(val) == f"\\sqrt{{{ft(val2)}}}" else f"={sp.latex(val)}") + "$。"],
              alt=[f"$\\vec{{a}}=({p},\\ 0)$、$\\vec{{b}}=({q}\\cos{ang_tex},\\ {q}\\sin{ang_tex})$ と成分で表して計算しても同じ値になる。"],
              pc=[("内積を求め、2乗して展開している", 1), ("大きさを正しく求めている", 1)],
              pit=["$|s\\vec{a}+t\\vec{b}|^2$ の展開で、内積の項 $2st\\,\\vec{a}\\cdot\\vec{b}$ を落とす。", "最後に平方根をとり忘れ、2乗の値を答える。"],
              chk=(f"sqrt(({s})**2*{p}**2+2*({s})*({t})*({fp(d)})+({t})**2*{q}**2)", str(val), None, "intermediate"))


@gen("basic_check", 4, ["computation", "concept"])
def a_cond_prob(r):
    while True:
        r1, w1, r2, w2 = r.randint(1, 5), r.randint(1, 5), r.randint(1, 5), r.randint(1, 5)
        if F(r1, r1 + w1) != F(r2, r2 + w2):
            break
    sel = r.choice(["coin", "die13", "die12"])
    pa = {"coin": F(1, 2), "die13": F(1, 3), "die12": F(1, 2)}[sel]
    seltxt = {"coin": "硬貨を1枚投げて表なら袋 A、裏なら袋 B を選び",
              "die13": "さいころを1個投げて1か2の目なら袋 A、それ以外なら袋 B を選び",
              "die12": "さいころを1個投げて偶数の目なら袋 A、奇数の目なら袋 B を選び"}[sel]
    target = r.choice(["赤", "白"])
    ga = F(r1 if target == "赤" else w1, r1 + w1)
    gb = F(r2 if target == "赤" else w2, r2 + w2)
    num_ = pa * ga
    den = pa * ga + (1 - pa) * gb
    P = num_ / den
    return num(f"袋 A には赤玉 ${r1}$ 個と白玉 ${w1}$ 個、袋 B には赤玉 ${r2}$ 個と白玉 ${w2}$ 個が入っている。{seltxt}、選んだ袋から玉を1個取り出す。取り出した玉が{target}玉であったとき、それが袋 A から取り出されたものである確率を求めなさい。",
               fs(P), f"$P(\\text{{{target}}})={ft(pa)}\\cdot{ft(ga)}+{ft(1 - pa)}\\cdot{ft(gb)}={ft(den)}$、$P(\\text{{A かつ{target}}})={ft(num_)}$。求める確率は ${ft(P)}$。", d=2, disp=f"${ft(P)}$",
               ap="「結果（取り出した玉の色）がわかったときの原因（袋）の確率」は条件付き確率 $P_{\\text{結果}}(\\text{原因})=\\dfrac{P(\\text{原因かつ結果})}{P(\\text{結果})}$。",
               steps=[f"$P(\\text{{A}}\\cap\\text{{{target}}})={ft(pa)}\\times{ft(ga)}={ft(num_)}$。", f"$P(\\text{{B}}\\cap\\text{{{target}}})={ft(1 - pa)}\\times{ft(gb)}={ft((1 - pa) * gb)}$。",
                      f"$P(\\text{{{target}}})={ft(den)}$。", f"求める確率は $\\dfrac{{{ft(num_)}}}{{{ft(den)}}}$ を計算して ${ft(P)}$。"],
               alt=["全体の試行回数を適当な数（分母の最小公倍数など）と考え、それぞれの場合の回数の比で求めても同じ結果になる（面積図・表による確認）。"],
               pc=[("分母 $P(\\text{" + target + "})$ を場合分けの和で求めている", 1), ("条件付き確率を正しく計算している", 1)],
               pit=["分子の $P(\\text{A}\\cap\\text{" + target + "})$ をそのまま答える。", "「袋 A を選んだときに" + target + "玉が出る確率」$P_{\\text{A}}(\\text{" + target + "})$ と取り違える。"],
               chk=(f"({fp(pa)})*({fp(ga)})/(({fp(pa)})*({fp(ga)})+({fp(1 - pa)})*({fp(gb)}))", fp(P)))


TRIALS = [("1個のさいころを投げて3の倍数の目が出る", F(1, 3)), ("1個のさいころを投げて1の目が出る", F(1, 6)), ("1枚の硬貨を投げて表が出る", F(1, 2)),
          ("1個のさいころを投げて4以下の目が出る", F(2, 3)), ("2枚の硬貨を同時に投げて2枚とも表が出る", F(1, 4)),
          ("1個のさいころを投げて5以上の目が出る", F(1, 3)), ("2枚の硬貨を同時に投げて少なくとも1枚は表が出る", F(3, 4))]


@gen("basic_check", 4, ["computation", "application"])
def a_repeated_trial(r):
    ev_, p = r.choice(TRIALS)
    n = r.randint(3, 6)
    k = r.randint(1, n - 1)
    form = r.choice(["eq", "ge"])
    if form == "eq":
        P = math.comb(n, k) * p ** k * (1 - p) ** (n - k)
        what = f"ちょうど ${k}$ 回"
        expr = f"binomial({n},{k})*({fp(p)})**{k}*({fp(1 - p)})**{n - k}"
        stp = [f"${n}$ 回のうちどの ${k}$ 回で起こるかが ${{}}_{{{n}}}\\mathrm{{C}}_{{{k}}}={math.comb(n, k)}$ 通り。",
               f"確率は ${math.comb(n, k)}\\times\\left({ft(p)}\\right)^{{{k}}}\\left({ft(1 - p)}\\right)^{{{n - k}}}={ft(P)}$。"]
    else:
        P = 1 - (1 - p) ** n
        what = "少なくとも1回"
        expr = f"1-({fp(1 - p)})**{n}"
        stp = ["余事象は「1回も起こらない」。", f"その確率は $\\left({ft(1 - p)}\\right)^{{{n}}}$ なので、求める確率は $1-\\left({ft(1 - p)}\\right)^{{{n}}}={ft(P)}$。"]
    return num(f"「{ev_}」という試行を ${n}$ 回くり返す。この事象が{what}起こる確率を求めなさい。",
               fs(P), f"1回の試行で起こる確率は ${ft(p)}$。" + ("反復試行の確率の公式を用いる。" if form == "eq" else "余事象を用いる。"), d=2, disp=f"${ft(P)}$",
               ap="独立な試行のくり返しでは、「どの回で起こるか」の選び方と、各回の確率の積を組み合わせる（反復試行）。「少なくとも」は余事象。",
               steps=[f"1回で起こる確率 $p={ft(p)}$、起こらない確率 ${ft(1 - p)}$。"] + stp,
               alt=["$n$ 回の結果をすべて書き出す樹形図で、小さい場合（例えば2回）について公式と一致することを確かめる。"],
               pc=[("1回の確率と立式が正しい", 1), ("確率を正しく計算している", 1)],
               pit=["${}_n\\mathrm{C}_k$ をかけ忘れる。" if form == "eq" else "「少なくとも1回」を $n\\times p$ と計算する。", "起こらない確率 $1-p$ の指数を誤る。"],
               chk=(expr, fp(P)))


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 4, ["computation", "condition_check"])
def b_tangent_area(r):
    while True:
        a = r.choice([1, -1])
        b = r.choice([-6, -3, 0, 3, 6, -2, 2])
        c, d = r.randint(-4, 4), r.randint(-3, 3)
        t = r.randint(-2, 2)
        u = F(-b, a) - 2 * t
        if u != t and abs(u - t) <= 6:
            break
    cs = [a, b, c, d]
    Fs = py(*cs)
    ftv = ev(cs, t)
    m = 3 * a * t * t + 2 * b * t + c
    n0 = ftv - m * t
    S = F(abs(u - t)) ** 4 / 12
    lo, hi = min(F(t), u), max(F(t), u)
    line = poly(m, int(n0)) if m != 0 else str(n0)
    return num(f"曲線 $C:\\ y={poly(*cs)}$ 上の点 $\\mathrm{{T}}({t},\\ {ftv})$ における接線を $\\ell$ とする。$\\ell$ と $C$ の T 以外の共有点の $x$ 座標を求め、$C$ と $\\ell$ で囲まれた部分の面積 $S$ を求めなさい。",
               fs(S), f"$\\ell:\\ y={line}$。$({poly(*cs)})-({line})={'' if a == 1 else '-'}{fac(t)}^2{fac(u)}$ より、もう1つの共有点は $x={ft(u)}$。$S={ft(S)}$。", d=3, disp=f"$S={ft(S)}$",
               ap="接線の式を曲線の式から引くと、接点の $x$ 座標を重解にもつ三次式 $a(x-t)^2(x-u)$ になる。$u$ は解と係数の関係 $2t+u=-\\dfrac{b}{a}$ からすぐに求まる。",
               steps=[f"$y'={poly(3 * a, 2 * b, c)}$ より傾き ${m}$、$\\ell:\\ y={line}$。",
                      f"$({poly(*cs)})-({line})={'' if a == 1 else '-'}{fac(t)}^2{fac(u)}$（$2\\cdot({t})+u={ft(F(-b, a))}$ より $u={ft(u)}$）。",
                      f"${ft(lo)}\\leqq x\\leqq{ft(hi)}$ で上下関係を確かめ、$S=\\left|\\displaystyle\\int_{{{ft(lo)}}}^{{{ft(hi)}}}{'' if a == 1 else '-'}{fac(t)}^2{fac(u)}\\,dx\\right|$。",
                      f"$S=\\dfrac{{|{ft(u)}-({t})|^4}}{{12}}={ft(S)}$。"],
               alt=[f"$\\dfrac{{1}}{{12}}$ 公式を使わずに、${'' if a == 1 else '-'}{fac(t)}^2{fac(u)}$ を展開して ${ft(lo)}$ から ${ft(hi)}$ まで積分しても同じ値になる。"],
               pc=[("接線の方程式を正しく求めている", 1), ("もう1つの共有点を因数分解（解と係数の関係）で求めている", 1), ("上下関係を確かめて面積を正しく求めている", 2)],
               pit=["接線の式を引いた三次式を、接点の重解を使わずに解こうとして時間を失う。", "上下関係を確かめずに積分し、負の値を答える。"],
               chk=(f"Abs(integrate(({Fs})-(({m})*x+({fp(n0)})), [x, {fp(lo)}, {fp(hi)}]))", fp(S)))


def solve_intersection(m, n, p, q, side):
    """P は AB を m:n に内分、Q は side（'OA' or 'OB'）を p:q に内分。OP と BQ（または AQ）の交点の係数。"""
    k, s = sp.symbols("k s")
    Pa, Pb = sp.Rational(n, m + n), sp.Rational(m, m + n)
    if side == "OA":   # Q on OA, line BQ: (1-s)b + s*(p/(p+q)) a
        eqs = [k * Pa - s * sp.Rational(p, p + q), k * Pb - (1 - s)]
    else:              # Q on OB, line AQ: (1-s)a + s*(p/(p+q)) b
        eqs = [k * Pa - (1 - s), k * Pb - s * sp.Rational(p, p + q)]
    sol = sp.solve(eqs, [k, s], dict=True)[0]
    return F(str(sol[k] * Pa)), F(str(sol[k] * Pb)), F(str(sol[k])), F(str(sol[s]))


@gen("standard_practice", 4, ["computation", "condition_check"])
def b_vec_intersection(r):
    m, n = r.choice([(1, 1), (1, 2), (2, 1), (1, 3), (3, 1), (2, 3), (3, 2), (3, 4)])
    p, q = r.choice([(1, 1), (1, 2), (2, 1), (2, 3), (3, 2), (1, 3), (3, 1)])
    side = r.choice(["OA", "OB"])
    al, be, k, s = solve_intersection(m, n, p, q, side)
    other = "B" if side == "OA" else "A"
    qv = vcomb(F(p, p + q), 0) if side == "OA" else vcomb(0, F(p, p + q))
    return sa(f"$\\triangle\\mathrm{{OAB}}$ において $\\overrightarrow{{\\mathrm{{OA}}}}=\\vec{{a}},\\ \\overrightarrow{{\\mathrm{{OB}}}}=\\vec{{b}}$ とする。辺 AB を ${m}:{n}$ に内分する点を P、辺 O{side[1]} を ${p}:{q}$ に内分する点を Q とし、線分 OP と線分 {other}Q の交点を R とする。$\\overrightarrow{{\\mathrm{{OR}}}}$ を $\\vec{{a}},\\ \\vec{{b}}$ を用いて表しなさい。",
              f"$\\overrightarrow{{\\mathrm{{OR}}}}={vcomb(al, be)}$",
              f"R を OP 上の点、{other}Q 上の点として2通りに表し、$\\vec{{a}},\\ \\vec{{b}}$ が一次独立であることから係数を比較する。$\\mathrm{{OR}}:\\mathrm{{OP}}={ft(k)}:1$。", d=3,
              v=[f"OR={fs(al)}a+{fs(be)}b"],
              ap="交点は「2つの線分のどちらの上にもある点」。それぞれの線分上の点として媒介変数で表し、一次独立を根拠に係数を比較する。",
              steps=[f"$\\overrightarrow{{\\mathrm{{OP}}}}=\\dfrac{{{c1(n)}\\vec{{a}}+{c1(m)}\\vec{{b}}}}{{{m + n}}}$、$\\overrightarrow{{\\mathrm{{OQ}}}}={qv}$。",
                     f"R は OP 上：$\\overrightarrow{{\\mathrm{{OR}}}}=k\\overrightarrow{{\\mathrm{{OP}}}}=\\dfrac{{{c1(n)}k}}{{{m + n}}}\\vec{{a}}+\\dfrac{{{c1(m)}k}}{{{m + n}}}\\vec{{b}}$。",
                     f"R は {other}Q 上：$\\overrightarrow{{\\mathrm{{OR}}}}=(1-s)\\overrightarrow{{\\mathrm{{O{other}}}}}+s\\overrightarrow{{\\mathrm{{OQ}}}}$。",
                     f"$\\vec{{a}},\\ \\vec{{b}}$ は一次独立なので係数を比較して、$k={ft(k)},\\ s={ft(s)}$。",
                     f"$\\overrightarrow{{\\mathrm{{OR}}}}={vcomb(al, be)}$。"],
              alt=[f"メネラウスの定理を $\\triangle\\mathrm{{O{other if other == 'A' else 'B'}P}}$ などに用いて $\\mathrm{{OR}}:\\mathrm{{RP}}$ を求め、$\\overrightarrow{{\\mathrm{{OR}}}}={ft(k)}\\overrightarrow{{\\mathrm{{OP}}}}$ として確かめられる。"],
              pc=[("OP 上の点として表している", 1), (f"{other}Q 上の点として表している", 1), ("一次独立を根拠に係数比較し、正しく答えている", 2)],
              pit=["係数比較の根拠（$\\vec{a},\\ \\vec{b}$ が一次独立）を書かない。", "内分点の公式で $m$ と $n$ の位置を逆にする。"],
              chk=(f"[({fp(k)})*Rational({n},{m + n}), ({fp(k)})*Rational({m},{m + n})]", f"[{fp(al)}, {fp(be)}]", None, "intermediate"))


@gen("standard_practice", 4, ["computation", "application"])
def b_series_game(r):
    p = r.choice([F(1, 3), F(2, 3), F(2, 5), F(3, 5), F(1, 4), F(3, 4)])
    k = r.choice([2, 3, 4])
    ask = r.choice(["win", "len"])
    qq = 1 - p
    if ask == "win":
        P = sum(math.comb(k - 1 + j, j) * p ** k * qq ** j for j in range(k))
        what = "A が優勝する確率"
        expr = "+".join(f"binomial({k - 1 + j},{j})*({fp(p)})**{k}*({fp(qq)})**{j}" for j in range(k))
        stp = [f"A が優勝するのは、最後の試合に A が勝ち、それまでに A が ${k - 1}$ 勝、B が $j$ 勝（$j=0,\\ \\cdots,\\ {k - 1}$）している場合。",
               f"確率は $\\displaystyle\\sum_{{j=0}}^{{{k - 1}}}{{}}_{{{k - 1}+j}}\\mathrm{{C}}_{{j}}\\left({ft(p)}\\right)^{{{k}}}\\left({ft(qq)}\\right)^{{j}}$。"]
    else:
        L = 2 * k - 1
        P = math.comb(L - 1, k - 1) * (p ** k * qq ** (k - 1) + qq ** k * p ** (k - 1))
        what = f"ちょうど ${L}$ 試合目で優勝が決まる確率"
        expr = f"binomial({L - 1},{k - 1})*(({fp(p)})**{k}*({fp(qq)})**{k - 1}+({fp(qq)})**{k}*({fp(p)})**{k - 1})"
        stp = [f"${L}$ 試合目で決まるのは、${L - 1}$ 試合目までに両者が ${k - 1}$ 勝ずつし、${L}$ 試合目に勝った方が優勝する場合。",
               f"A が優勝：${{}}_{{{L - 1}}}\\mathrm{{C}}_{{{k - 1}}}\\left({ft(p)}\\right)^{{{k}}}\\left({ft(qq)}\\right)^{{{k - 1}}}$、B が優勝も同様に加える。"]
    return num(f"A と B が試合をくり返し、先に ${k}$ 勝した方を優勝とする。1試合で A が勝つ確率は ${ft(p)}$ で、引き分けはなく、各試合の結果は独立とする。{what}を求めなさい。",
               fs(P), f"優勝が決まる試合（最後の試合）の勝者を固定し、それまでの勝敗の並べ方を数える。答えは ${ft(P)}$。", d=3, disp=f"${ft(P)}$",
               ap="優勝が決まった後は試合をしないので、「最後の試合は優勝する側が勝つ」と固定して、それ以前の試合の勝敗の並べ方を組合せで数える。",
               steps=stp + [f"計算して ${ft(P)}$。"],
               alt=["優勝が決まった後も試合を続けると考えても、優勝者は変わらない。" + (f"そこで ${2 * k - 1}$ 試合すべてを行ったとして「A が ${k}$ 勝以上する確率」を求めても同じ値になる。" if ask == "win" else "樹形図で小さい場合を確かめる方法もある。")],
               pc=[("最後の試合の勝者を固定して場合分けしている", 2), ("組合せの数と確率の積を正しく立式している", 1), ("正しく計算している", 1)],
               pit=["最後の試合を含めて組合せを数え、優勝決定後の試合まで数えてしまう。", "B が優勝する場合を加え忘れる（試合数を問う場合）。" if ask == "len" else "$j$ の範囲を誤り、B が先に優勝する場合まで含める。"],
               chk=(expr, fp(P)))


@gen("standard_practice", 4, ["computation", "cross_unit"], rel=["HS-MATH3-U03"])
def b_volume(r):
    kind = r.choice(["para", "between"])
    x = sp.Symbol("x")
    if kind == "para":
        a = r.choice([1, 2, 3])
        c = r.randint(1, 5)
        fx = a * x * (c - x)
        tex = f"{'' if a == 1 else a}x({c}-x)"
        V = sp.pi * sp.integrate(fx ** 2, (x, 0, c))
        stem = f"放物線 $y={tex}$ と $x$ 軸で囲まれた部分を、$x$ 軸のまわりに1回転してできる回転体の体積 $V$ を求めなさい。"
        expr = f"pi*integrate(({a}*x*({c}-x))**2, [x, 0, {c}])"
        stp = [f"$x$ 軸との交点は $x=0,\\ {c}$。", f"$V=\\pi\\displaystyle\\int_0^{{{c}}}\\{{{tex}\\}}^2dx$。", f"展開して積分すると $V={sp.latex(V)}$。"]
    else:
        k = r.randint(1, 4)
        V = sp.pi * sp.integrate((k * x) ** 2 - x ** 4, (x, 0, k))
        stem = f"放物線 $y=x^2$ と直線 $y={'' if k == 1 else k}x$ で囲まれた部分を、$x$ 軸のまわりに1回転してできる回転体の体積 $V$ を求めなさい。"
        expr = f"pi*integrate(({k}*x)**2-x**4, [x, 0, {k}])"
        stp = [f"交点は $x=0,\\ {k}$。$0\\leqq x\\leqq{k}$ で直線が上、どちらも $y\\geqq0$。",
               f"$V=\\pi\\displaystyle\\int_0^{{{k}}}\\{{({'' if k == 1 else k}x)^2-(x^2)^2\\}}dx$（外側の円板から内側の円板を除く）。", f"計算して $V={sp.latex(V)}$。"]
    return sa(stem, f"$V={sp.latex(V)}$", f"回転体の体積は $V=\\pi\\displaystyle\\int y^2dx$。答えは ${sp.latex(V)}$。", d=3,
              v=[str(V)],
              ap="$x$ 軸のまわりの回転体は、$x$ 軸に垂直な断面が円（または円環）になる。断面積 $\\pi y^2$ を積分する（数学Ⅲ 積分法との融合）。",
              steps=stp,
              alt=["断面積を求めてから積分する、という手順を図にかいて確かめる。" + ("2つの曲線の間の部分は、$\\pi\\int(y_1-y_2)^2dx$ ではなく $\\pi\\int(y_1^2-y_2^2)dx$ であることを図で確認する。" if kind == "between" else "対称性（直線 $x=" + ft(F(c, 2)) + "$ に関して対称）を使い、半分の区間の2倍として計算してもよい。")],
              pc=[("体積の積分の式を正しく立てている", 2), ("積分を正しく計算している", 2)],
              pit=["$\\pi$ をかけ忘れる、または $y$ を2乗し忘れる。", "2曲線の間を回転するとき、差を2乗してしまう（$(y_1-y_2)^2$）。"],
              chk=(expr, str(V), None, "intermediate"))


@gen("standard_practice", 4, ["computation", "written_reasoning"])
def b_vec_foot(r):
    while True:
        p, q = r.randint(1, 5), r.randint(1, 5)
        d = r.randint(-p * q + 1, p * q - 1)
        den = p * p - 2 * d + q * q
        if den > 0 and d * d < p * p * q * q and (p, q) != (1, 1):
            break
    t = F(p * p - d, den)
    al, be = 1 - t, t
    return sa(f"$\\triangle\\mathrm{{OAB}}$ において、$\\overrightarrow{{\\mathrm{{OA}}}}=\\vec{{a}},\\ \\overrightarrow{{\\mathrm{{OB}}}}=\\vec{{b}}$、$|\\vec{{a}}|={p},\\ |\\vec{{b}}|={q},\\ \\vec{{a}}\\cdot\\vec{{b}}={d}$ とする。O から直線 AB に下ろした垂線を OH とするとき、$\\overrightarrow{{\\mathrm{{OH}}}}$ を $\\vec{{a}},\\ \\vec{{b}}$ で表しなさい。",
              f"$\\overrightarrow{{\\mathrm{{OH}}}}={vcomb(al, be)}$",
              f"$\\overrightarrow{{\\mathrm{{OH}}}}=(1-t)\\vec{{a}}+t\\vec{{b}}$ とおき、$\\overrightarrow{{\\mathrm{{OH}}}}\\cdot\\overrightarrow{{\\mathrm{{AB}}}}=0$ から $t={ft(t)}$。", d=3,
              v=[f"OH={fs(al)}a+{fs(be)}b"],
              ap="H は直線 AB 上の点なので $(1-t)\\vec{a}+t\\vec{b}$ と表せる。垂直条件は内積が 0。",
              steps=["H は直線 AB 上：$\\overrightarrow{\\mathrm{OH}}=(1-t)\\vec{a}+t\\vec{b}$。",
                     "$\\overrightarrow{\\mathrm{OH}}\\perp\\overrightarrow{\\mathrm{AB}}$ より $\\{(1-t)\\vec{a}+t\\vec{b}\\}\\cdot(\\vec{b}-\\vec{a})=0$。",
                     f"展開：$(1-t)(\\vec{{a}}\\cdot\\vec{{b}}-|\\vec{{a}}|^2)+t(|\\vec{{b}}|^2-\\vec{{a}}\\cdot\\vec{{b}})=0$、すなわち $(1-t)({d - p * p})+t({q * q - d})=0$。",
                     f"$t=\\dfrac{{{p * p - d}}}{{{den}}}" + ("" if F(p * p - d, den) == t and math.gcd(p * p - d, den) == 1 else f"={ft(t)}") + "$。", f"$\\overrightarrow{{\\mathrm{{OH}}}}={vcomb(al, be)}$。"],
              alt=["$\\overrightarrow{\\mathrm{AH}}$ は $\\overrightarrow{\\mathrm{AO}}$ の $\\overrightarrow{\\mathrm{AB}}$ への正射影なので、$\\overrightarrow{\\mathrm{AH}}=\\dfrac{\\overrightarrow{\\mathrm{AO}}\\cdot\\overrightarrow{\\mathrm{AB}}}{|\\overrightarrow{\\mathrm{AB}}|^2}\\overrightarrow{\\mathrm{AB}}$ から求めてもよい。"],
              pc=[("H を直線 AB 上の点として表している", 1), ("垂直条件を内積で立式している", 1), ("$t$ を求めて正しく答えている", 2)],
              pit=["垂直条件を $\\overrightarrow{\\mathrm{OH}}\\cdot\\overrightarrow{\\mathrm{OB}}=0$ などと取り違える。", "展開で $\\vec{a}\\cdot\\vec{b}$ の項の符号を誤る。"],
              chk=(f"solve((1-t)*({d}-{p * p})+t*({q * q}-{d}), t)", f"[{fp(t)}]", None, "intermediate"))


# ======================================================================
# C 思考力・記述応用
# ======================================================================

@gen("thinking_writing", 3, ["written_reasoning", "computation"])
def c_integral_eq(r):
    x, t, A, B = sp.symbols("x t A B")
    kind = r.choice(["const", "xt", "upper"])
    if kind == "const":
        p, q = r.choice([1, 2, 3, -1, 3]), r.randint(-4, 4)
        c = r.choice([2, 3, -1])
        K = sp.solve(sp.Eq(A, sp.integrate(p * t ** 2 + q * t + A, (t, 0, c))), A)[0]
        f = sp.expand(p * x ** 2 + q * x + K)
        stem = f"関数 $f(x)$ が $f(x)={poly(p, q, 0)}+\\displaystyle\\int_0^{{{c}}}f(t)\\,dt$ を満たすとき、$f(x)$ を求めなさい。"
        stp = [f"$\\displaystyle\\int_0^{{{c}}}f(t)\\,dt$ は定数なので $A$ とおくと、$f(x)={poly(p, q, 0)}+A$。",
               f"$A=\\displaystyle\\int_0^{{{c}}}(pt^2+qt+A)\\,dt$ に $p={p},\\ q={q}$ を代入して計算すると、$A$ の一次方程式になる。",
               f"解いて $A={lt(K)}$。", f"$f(x)={sp.latex(f)}$。"]
        chk = (f"expand({p}*x**2+({q})*x+({sp.sstr(K)})-({sp.sstr(f)}))", "0")
        alt = [f"求めた $f(x)$ を元の式に代入し、$\\displaystyle\\int_0^{{{c}}}f(t)\\,dt={lt(K)}$ となることを確かめる。"]
    elif kind == "xt":
        p, q = r.choice([1, 2, 3]), r.randint(-3, 3)
        sol = sp.solve([sp.Eq(A, sp.integrate(p * t ** 2 + q * t + A * t - B, (t, 0, 1))),
                        sp.Eq(B, sp.integrate(t * (p * t ** 2 + q * t + A * t - B), (t, 0, 1)))], [A, B], dict=True)[0]
        f = sp.expand(p * x ** 2 + q * x + sol[A] * x - sol[B])
        stem = f"関数 $f(x)$ が $f(x)={poly(p, q, 0)}+\\displaystyle\\int_0^{{1}}(x-t)f(t)\\,dt$ を満たすとき、$f(x)$ を求めなさい。"
        stp = ["$\\displaystyle\\int_0^1(x-t)f(t)\\,dt=x\\int_0^1f(t)\\,dt-\\int_0^1tf(t)\\,dt$（$x$ は積分変数ではないので外に出せる）。",
               f"$A=\\displaystyle\\int_0^1f(t)\\,dt,\\ B=\\int_0^1tf(t)\\,dt$ とおくと $f(x)={poly(p, q, 0)}+Ax-B$。",
               "これを $A,\\ B$ の定義式に代入して、$A,\\ B$ の連立一次方程式をつくる。",
               f"解いて $A={lt(sol[A])},\\ B={lt(sol[B])}$。$f(x)={sp.latex(f)}$。"]
        chk = (f"[{sp.sstr(sol[A])}, {sp.sstr(sol[B])}]", f"[{sp.sstr(sp.integrate(f.subs(x, t), (t, 0, 1)))}, {sp.sstr(sp.integrate(t * f.subs(x, t), (t, 0, 1)))}]")
        alt = ["求めた $f(x)$ で $\\displaystyle\\int_0^1 f(t)\\,dt$ と $\\displaystyle\\int_0^1 tf(t)\\,dt$ を計算し、$A,\\ B$ の値と一致することを確かめる。"]
    else:
        a1, a2 = r.sample([-3, -2, -1, 1, 2, 3, 4], 2)
        b, c = -(a1 + a2), a1 * a2
        k = r.choice([1, 2, 3])
        f = sp.expand(k * (2 * x + b))
        stem = f"定数 $a$ と関数 $f(x)$ が、すべての実数 $x$ について $\\displaystyle\\int_a^x f(t)\\,dt={k if k > 1 else ''}({poly(1, b, c)})$ を満たすとき、$f(x)$ と $a$ の値を求めなさい。"
        stp = ["両辺を $x$ で微分すると、左辺は $f(x)$（微分積分学の基本定理）。", f"$f(x)={sp.latex(f)}$。",
               f"両辺に $x=a$ を代入すると左辺は 0 なので、${poly(1, b, c, var='a')}=0$。", f"$(a{'-' if a1 > 0 else '+'}{abs(a1)})(a{'-' if a2 > 0 else '+'}{abs(a2)})=0$ より $a={min(a1, a2)},\\ {max(a1, a2)}$。"]
        chk = (f"solve(a**2+({b})*a+({c}), a)", f"[{a1}, {a2}]", "set")
        alt = [f"$a={a1}$ のとき $\\displaystyle\\int_{{{a1}}}^x f(t)\\,dt$ を実際に計算し、右辺と一致することを確かめる。"]
    ans = f"$f(x)={sp.latex(f)}$" + (f"、$a={min(a1, a2)},\\ {max(a1, a2)}$" if kind == "upper" else "")
    return desc(stem, ans, f"答えは {ans}。", [("積分を定数とおく（または微分する）方針を示している", 3), ("方程式を正しく立てている", 3), ("正しい答えを得ている", 2)],
                d=4, p=8, lines=10,
                ap=("定積分 $\\displaystyle\\int_a^b f(t)\\,dt$（上端・下端が定数）は定数なので文字でおく。" if kind != "upper" else "上端に $x$ を含む定積分は、$x$ で微分すると被積分関数になる。また $x=a$ を代入すると 0 になる。") + "これが積分方程式の2つの基本操作である。",
                steps=stp, alt=alt,
                pc=[("方針（定数とおく・微分する）", 3), ("方程式の立式", 3), ("答え", 2)],
                pit=["$\\displaystyle\\int_0^1(x-t)f(t)\\,dt$ の $x$ を積分の外に出さずに、そのまま定数とおいてしまう。" if kind == "xt" else ("$x=a$ を代入して $a$ の条件を得る手順を忘れる。" if kind == "upper" else "$\\displaystyle\\int_0^{c}f(t)\\,dt$ の計算で $A$ 自身の積分 $cA$ を落とす。"),
                     "最後に元の式に代入して確かめる検算を省く。"],
                chk=(chk[0], chk[1], chk[2] if len(chk) > 2 else None, "intermediate"))


RECUR = [("1の目が出たとき", F(1, 6)), ("3の倍数の目が出たとき", F(1, 3)), ("4以下の目が出たとき", F(2, 3)), ("1以外の目が出たとき", F(5, 6)),
         ("5以上の目が出たとき", F(1, 3)), ("1か2か3の目が出たとき", F(1, 2)), ("6の約数の目が出たとき", F(2, 3))]


@gen("thinking_writing", 3, ["cross_unit", "written_reasoning"], rel=["HS-MATHB-U01", "HS-MATHA-U01"])
def c_prob_recur(r):
    while True:
        ev_, rr = r.choice(RECUR)
        if rr != F(1, 2):
            break
    start = r.choice(["A", "B"])
    lam = 1 - 2 * rr
    sgn_ = 1 if start == "A" else -1
    lam_tex = f"\\left({ft(lam)}\\right)^n"
    ans = f"p_n=\\dfrac{{1}}{{2}}{'+' if sgn_ > 0 else '-'}\\dfrac{{1}}{{2}}{lam_tex}"
    pn = f"Rational(1,2)+({sgn_})*Rational(1,2)*({fp(lam)})**n"
    pn1 = f"Rational(1,2)+({sgn_})*Rational(1,2)*({fp(lam)})**(n+1)"
    p1 = F(1, 2) + sgn_ * F(1, 2) * lam
    return desc(f"2つの箱 A, B があり、1個の玉がはじめ箱 {start} に入っている。1回の操作では1個のさいころを投げ、{ev_}に限り玉をもう一方の箱へ移し、それ以外のときは玉を動かさない。$n$ 回の操作の後に玉が箱 A に入っている確率を $p_n$ とする。\n(1) $p_{{n+1}}$ を $p_n$ で表しなさい。\n(2) $p_n$ を $n$ の式で表しなさい。",
                f"(1) $p_{{n+1}}={coef(lam, True)}p_n+{ft(rr)}$　(2) ${ans}$",
                f"$n+1$ 回後に A にあるのは「$n$ 回後に A にあり移さない」か「$n$ 回後に B にあり移す」場合。$p_{{n+1}}=(1-{ft(rr)})p_n+{ft(rr)}(1-p_n)$。",
                [("$n$ 回後の状態で場合分けして漸化式を立てている", 3), ("漸化式を $p_{n+1}-\\dfrac{1}{2}=" + f"{coef(lam, True)}" + "\\left(p_n-\\dfrac{1}{2}\\right)$ の形に変形している", 2),
                 ("初期条件を用いて一般項を正しく求めている", 3)], d=4, p=8, lines=12,
                ap="確率の推移は「直前の状態で場合分け」すると漸化式になる。$p_{n+1}=ap_n+b$ 型は、特性方程式 $\\alpha=a\\alpha+b$ の解を引いて等比数列にする（数列との融合）。",
                steps=[f"1回の操作で玉を移す確率は ${ft(rr)}$、移さない確率は ${ft(1 - rr)}$。",
                       f"(1) $p_{{n+1}}={ft(1 - rr)}p_n+{ft(rr)}(1-p_n)={coef(lam, True)}p_n+{ft(rr)}$。",
                       f"(2) $\\alpha={coef(lam, True)}\\alpha+{ft(rr)}$ より $\\alpha=\\dfrac{{1}}{{2}}$。$p_{{n+1}}-\\dfrac{{1}}{{2}}={coef(lam, True)}\\left(p_n-\\dfrac{{1}}{{2}}\\right)$。",
                       f"$p_0={1 if start == 'A' else 0}$（または $p_1={ft(p1)}$）から、$p_n-\\dfrac{{1}}{{2}}={'' if sgn_ > 0 else '-'}\\dfrac{{1}}{{2}}{lam_tex}$。",
                       f"${ans}$。"],
                alt=[f"$n=1,\\ 2$ の場合を直接計算し（$p_1={ft(p1)}$ など）、求めた式に代入した値と一致することを確かめる。",
                     f"「$n$ 回のうち移す回数が偶数（または奇数）回である確率」と考え、二項定理で $\\dfrac{{1}}{{2}}\\{{(q+p)^n\\pm(q-p)^n\\}}$ と求めることもできる（$p$ は移す確率、$q=1-p$）。"],
                pc=[("漸化式の立式", 3), ("等比数列への変形", 2), ("一般項", 3)],
                pit=["「B にあって移す」場合を落とし、$p_{n+1}=" + f"{ft(1 - rr)}" + "p_n$ とする。", "初期条件（はじめにどちらの箱にあるか）を取り違え、符号を逆にする。"],
                chk=(f"simplify(({fp(lam)})*({pn})+({fp(rr)})-({pn1}))", "0", None, "intermediate"))


TRI = [(p, q, s) for p in range(2, 8) for q in range(2, 8) for s in range(2, 9) if p < q + s and q < p + s and s < p + q and p != q]


@gen("thinking_writing", 2, ["cross_unit", "written_reasoning", "multiple_solutions"], rel=["HS-MATH1-U04", "HS-MATHC-U01"])
def c_vec_triangle(r):
    p, q, s = r.choice(TRI)
    d = F(p * p + q * q - s * s, 2)
    S = sp.Rational(1, 2) * sp.sqrt(sp.Rational(p * p * q * q) - sp.Rational(d.numerator, d.denominator) ** 2)
    tmin = -d / (q * q)
    mn = sp.sqrt(sp.Rational(p * p) - sp.Rational(d.numerator, d.denominator) ** 2 / (q * q))
    return desc(f"$|\\vec{{a}}|={p},\\ |\\vec{{b}}|={q},\\ |\\vec{{a}}-\\vec{{b}}|={s}$ とする。\n(1) 内積 $\\vec{{a}}\\cdot\\vec{{b}}$ を求めなさい。\n(2) $\\overrightarrow{{\\mathrm{{OA}}}}=\\vec{{a}},\\ \\overrightarrow{{\\mathrm{{OB}}}}=\\vec{{b}}$ とするとき、$\\triangle\\mathrm{{OAB}}$ の面積 $S$ を求めなさい。\n(3) 実数 $t$ を動かすとき、$|\\vec{{a}}+t\\vec{{b}}|$ の最小値と、そのときの $t$ の値を求めなさい。",
                f"(1) ${ft(d)}$　(2) $S={sp.latex(S)}$　(3) $t={ft(tmin)}$ のとき最小値 ${sp.latex(mn)}$",
                f"(1) $|\\vec{{a}}-\\vec{{b}}|^2=|\\vec{{a}}|^2-2\\vec{{a}}\\cdot\\vec{{b}}+|\\vec{{b}}|^2$ より。(2) $S=\\dfrac{{1}}{{2}}\\sqrt{{|\\vec{{a}}|^2|\\vec{{b}}|^2-(\\vec{{a}}\\cdot\\vec{{b}})^2}}$。(3) $t$ の二次関数として平方完成。",
                [("(1) 大きさの条件を2乗して内積を求めている", 2), ("(2) 面積の公式（または余弦定理と三角形の面積）で正しく求めている", 3), ("(3) $t$ の二次関数として最小値と $t$ を正しく求めている", 3)],
                d=4, p=8, lines=14,
                ap="大きさの条件は2乗して内積に直す。三角形の面積は $\\dfrac{1}{2}\\sqrt{|\\vec{a}|^2|\\vec{b}|^2-(\\vec{a}\\cdot\\vec{b})^2}$（図形と計量の $\\dfrac{1}{2}ab\\sin\\theta$ と $\\sin^2\\theta+\\cos^2\\theta=1$ から導かれる）。",
                steps=[f"(1) ${s * s}={p * p}-2\\vec{{a}}\\cdot\\vec{{b}}+{q * q}$ より $\\vec{{a}}\\cdot\\vec{{b}}={ft(d)}$。",
                       f"(2) $S=\\dfrac{{1}}{{2}}\\sqrt{{{p * p}\\cdot{q * q}-\\left({ft(d)}\\right)^2}}={sp.latex(S)}$。",
                       f"(3) $|\\vec{{a}}+t\\vec{{b}}|^2={q * q}t^2{'+' if 2 * d >= 0 else '-'}{ft(abs(2 * d))}t+{p * p}$。",
                       f"平方完成すると $t={ft(tmin)}$ で最小値 ${sp.latex(mn ** 2)}$ をとる。", f"$|\\vec{{a}}+t\\vec{{b}}|\\geqq0$ なので、最小値は ${sp.latex(mn)}$。"],
                alt=[f"(2) 余弦定理で $\\cos\\angle\\mathrm{{AOB}}=\\dfrac{{{ft(d)}}}{{{p * q}}}$ を求め、$\\sin\\angle\\mathrm{{AOB}}$ を計算して $S=\\dfrac{{1}}{{2}}\\cdot{p}\\cdot{q}\\sin\\angle\\mathrm{{AOB}}$ としても同じ値になる。",
                     "(3) 最小となるのは $(\\vec{a}+t\\vec{b})\\perp\\vec{b}$ のとき（A から直線 OB に下ろした垂線の長さ）と図形的に考え、$S=\\dfrac{1}{2}\\cdot" + f"{q}" + "\\cdot(\\text{最小値})$ からも求められる。"],
                pc=[("(1) 内積", 2), ("(2) 面積", 3), ("(3) 最小値と $t$", 3)],
                pit=["$|\\vec{a}-\\vec{b}|^2$ の展開で内積の符号を誤る。", "(3) で2乗の最小値を答え、平方根をとり忘れる。"],
                chk=(f"[({p}**2+{q}**2-{s}**2)/2, Rational(1,2)*sqrt({p}**2*{q}**2-(({p}**2+{q}**2-{s}**2)/2)**2)]", f"[{fp(d)}, {sp.sstr(S)}]", None, "intermediate"))


@gen("thinking_writing", 2, ["application", "written_reasoning", "condition_check"])
def c_box_max(r):
    kind = r.choice(["sq", "sq", "rect"])
    x = sp.Symbol("x")
    if kind == "sq":
        L = r.choice([6, 9, 12, 15, 18, 24, 30, 36, 3, 21, 27])
        V = x * (L - 2 * x) ** 2
        x0 = sp.Rational(L, 6)
        dom = f"0<x<{lt(sp.Rational(L, 2))}"
        sheet = f"1辺の長さが ${L}$ cm の正方形の厚紙"
        dtex = f"V'=({L}-2x)^2-4x({L}-2x)=({L}-2x)({L}-6x)"
    else:
        k = r.choice([1, 2, 3, 4])
        a, b = 8 * k, 5 * k
        V = x * (a - 2 * x) * (b - 2 * x)
        x0 = sp.Integer(k)
        dom = f"0<x<{lt(sp.Rational(b, 2))}"
        sheet = f"縦 ${b}$ cm、横 ${a}$ cm の長方形の厚紙"
        dtex = f"V'=12x^2-{4 * (a + b)}x+{a * b}=4(3x-{10 * k})(x-{k})"
    Vmax = V.subs(x, x0)
    return desc(f"{sheet}の四隅から、1辺の長さが $x$ cm の正方形を切り取り、残りを折り曲げてふたのない直方体の箱を作る。箱の容積を $V$ cm$^3$ とする。\n(1) $V$ を $x$ の式で表し、$x$ のとりうる値の範囲を答えなさい。\n(2) $V$ の最大値と、そのときの $x$ の値を求めなさい。",
                f"(1) $V={sp.latex(sp.factor(V))}$、${dom}$　(2) $x={lt(x0)}$ のとき最大値 ${lt(Vmax)}$",
                f"${dtex}$。${dom}$ で増減を調べると $x={lt(x0)}$ で極大かつ最大。",
                [("(1) $V$ の式と $x$ の範囲（辺の長さが正）を正しく答えている", 2), ("(2) 微分して増減表をかいている", 3), ("(2) 範囲内の極値が最大であることを確かめ、最大値を答えている", 3)],
                d=4, p=8, lines=12,
                ap="図形の量を関数で表したら、まず変数の範囲（長さが正）を決める。最大値は範囲内の増減表で判断する（微分法の応用）。",
                steps=[f"(1) 箱の底面は {'1辺 ' + f'${L}-2x$' + ' の正方形' if kind == 'sq' else f'${b}-2x$ と ${a}-2x$ の長方形'}、高さ $x$。$V={sp.latex(sp.factor(V))}$。",
                       f"辺の長さが正なので ${dom}$。", f"(2) ${dtex}$。",
                       f"${dom}$ で $V'=0$ となるのは $x={lt(x0)}$ だけで、その前後で $V'$ は正から負に変わる。",
                       f"よって $x={lt(x0)}$ で最大値 $V={lt(Vmax)}$。"],
                alt=["範囲の端（$x\\to0$、$x\\to$ 上限）で $V\\to0$ となることを確かめ、範囲内の極大が最大であることを裏づける。" + ("" if kind == "rect" else f"また、相加平均と相乗平均の関係 $4x\\cdot({L}-2x)\\cdot({L}-2x)\\leqq\\left(\\dfrac{{2{L}}}{{3}}\\right)^3$（3つの正の数の和が一定）からも $x={lt(x0)}$ で最大と確かめられる。")],
                pc=[("(1) 式と範囲", 2), ("(2) 増減の調べ方", 3), ("(2) 最大値", 3)],
                pit=["$V'=0$ の解のうち、範囲外の解（" + (f"$x={lt(sp.Rational(L, 2))}$" if kind == "sq" else f"$x={lt(sp.Rational(10 * k, 3))}$") + "）も候補に入れてしまう。", "$x$ の範囲を書かずに極値を最大値と答える。"],
                chk=(f"[limit(diff({sp.sstr(V)}, x), x, {sp.sstr(x0)}), {sp.sstr(V).replace('x', '(' + sp.sstr(x0) + ')')}]", f"[0, {sp.sstr(Vmax)}]", None, "intermediate"))


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(stem, wrong, step, etype, tempt, fix, ans, expl, steps, ap, alt, pit, chk=None, d=3):
    return desc(f"{stem}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい答えを求めなさい。", ans, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい解答を途中式とともに示している", 3), ("最終的な答えが正しい", 1)], d=d, p=6, lines=8,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい途中式", 3), ("正しい答え", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix), chk=chk)


@gen("error_correction", 3, ["common_error", "concept"])
def d_cond_prob(r):
    while True:
        r1, w1, r2, w2 = r.randint(1, 5), r.randint(1, 5), r.randint(1, 5), r.randint(1, 5)
        if F(r1, r1 + w1) != F(r2, r2 + w2):
            break
    pa = r.choice([F(1, 2), F(1, 3), F(2, 3)])
    seltxt = {F(1, 2): "硬貨を投げて表なら袋 A、裏なら袋 B", F(1, 3): "さいころを投げて1か2の目なら袋 A、それ以外なら袋 B", F(2, 3): "さいころを投げて4以下の目なら袋 A、それ以外なら袋 B"}[pa]
    ga, gb = F(r1, r1 + w1), F(r2, r2 + w2)
    num_ = pa * ga
    den = num_ + (1 - pa) * gb
    P = num_ / den
    mode = r.choice(["joint", "reverse"])
    if mode == "joint":
        wrong = f"袋 A を選び、赤玉が出る確率なので ${ft(pa)}\\times{ft(ga)}={ft(num_)}$。"
        step, tempt = "「A を選び赤玉が出る確率」$P(\\text{A}\\cap\\text{赤})$ を答えとした部分", "「赤玉であったとき」という条件の意味を考えず、2つの出来事が両方起こる確率を求めている。条件付き確率では、条件の事象の確率で割る必要がある。"
    else:
        wrong = f"袋 A から赤玉が出る確率なので ${ft(ga)}$。"
        step, tempt = "$P_{\\text{A}}(\\text{赤})$（袋 A を選んだときに赤玉が出る確率）を答えとした部分", "「A のとき赤」と「赤のとき A」を同じものと考えている。条件と結果を入れかえると確率は一般に変わる。"
        if ga == P:
            wrong = f"袋 A を選び、赤玉が出る確率なので ${ft(pa)}\\times{ft(ga)}={ft(num_)}$。"
            step, tempt = "「A を選び赤玉が出る確率」$P(\\text{A}\\cap\\text{赤})$ を答えとした部分", "「赤玉であったとき」という条件の意味を考えず、2つの出来事が両方起こる確率を求めている。"
    return err_item(f"袋 A には赤玉 ${r1}$ 個と白玉 ${w1}$ 個、袋 B には赤玉 ${r2}$ 個と白玉 ${w2}$ 個が入っている。{seltxt} を選び、その袋から玉を1個取り出したところ赤玉であった。このとき、袋 A から取り出した確率を求めよ。", wrong,
                    step, "concept", tempt,
                    f"求めるのは $P_{{\\text{{赤}}}}(\\text{{A}})=\\dfrac{{P(\\text{{A}}\\cap\\text{{赤}})}}{{P(\\text{{赤}})}}=\\dfrac{{{ft(num_)}}}{{{ft(den)}}}={ft(P)}$。",
                    f"${ft(P)}$", f"分母 $P(\\text{{赤}})={ft(den)}$ は、袋 A・袋 B の場合の和。",
                    [f"$P(\\text{{A}}\\cap\\text{{赤}})={ft(pa)}\\times{ft(ga)}={ft(num_)}$。", f"$P(\\text{{B}}\\cap\\text{{赤}})={ft(1 - pa)}\\times{ft(gb)}={ft((1 - pa) * gb)}$。",
                     f"$P(\\text{{赤}})={ft(den)}$。", f"$P_{{\\text{{赤}}}}(\\text{{A}})={ft(P)}$。"],
                    "「〜であったとき」は条件付き確率。分母は「条件として与えられた事象（赤玉が出た）」の確率である。",
                    ["全体を（分母の最小公倍数などの）回数で表した表をつくり、赤玉が出た回数のうち袋 A からの回数の割合として確かめる。"],
                    ["条件付き確率の分母を 1（全体）のままにする。", "$P_A(B)$ と $P_B(A)$ を取り違える。"],
                    chk=(f"({fp(pa)})*({fp(ga)})/(({fp(pa)})*({fp(ga)})+({fp(1 - pa)})*({fp(gb)}))", fp(P), None, "intermediate"))


@gen("error_correction", 2, ["common_error", "computation"])
def d_dice_max(r):
    n = r.choice([2, 3, 4, 5])
    k = r.randint(2, 6)
    kind = r.choice(["max", "min"])
    if kind == "max":
        P = F(k ** n - (k - 1) ** n, 6 ** n)
        wr = F(k ** n, 6 ** n)
        what = f"最大値が ${k}$ である"
        wrong = f"すべての目が ${k}$ 以下であればよいので、$\\left(\\dfrac{{{k}}}{{6}}\\right)^{{{n}}}={ft(wr)}$。"
        fix = f"「すべて ${k}$ 以下」には最大値が ${k - 1}$ 以下の場合も含まれる。$\\left(\\dfrac{{{k}}}{{6}}\\right)^{{{n}}}-\\left(\\dfrac{{{k - 1}}}{{6}}\\right)^{{{n}}}={ft(P)}$。"
        expr = f"Rational({k}**{n}-{k - 1}**{n}, 6**{n})"
    else:
        k = min(k, 5)
        P = F((7 - k) ** n - (6 - k) ** n, 6 ** n)
        wr = F((7 - k) ** n, 6 ** n)
        what = f"最小値が ${k}$ である"
        wrong = f"すべての目が ${k}$ 以上であればよいので、$\\left(\\dfrac{{{7 - k}}}{{6}}\\right)^{{{n}}}={ft(wr)}$。"
        fix = f"「すべて ${k}$ 以上」には最小値が ${k + 1}$ 以上の場合も含まれる。$\\left(\\dfrac{{{7 - k}}}{{6}}\\right)^{{{n}}}-\\left(\\dfrac{{{6 - k}}}{{6}}\\right)^{{{n}}}={ft(P)}$。"
        expr = f"Rational({7 - k}**{n}-{6 - k}**{n}, 6**{n})"
    return err_item(f"1個のさいころを ${n}$ 回投げるとき、出た目の{what}確率を求めよ。", wrong,
                    "「すべて〜以下（以上）」の確率をそのまま答えとした部分", "concept",
                    "「最大値が $k$」を「どの目も $k$ を超えない」と言いかえたところで止まり、$k$ が少なくとも1回出るという条件を落としている。",
                    fix, f"${ft(P)}$", "「最大値（最小値）がちょうど $k$」＝「すべて $k$ 以下（以上）」から「すべて $k\\mp1$ 以下（以上）」を除いたもの。",
                    [("すべて $" + str(k) + "$ 以下の確率と、すべて $" + str(k - 1) + "$ 以下の確率を求める。") if kind == "max" else ("すべて $" + str(k) + "$ 以上の確率と、すべて $" + str(k + 1) + "$ 以上の確率を求める。"),
                     "差をとる。", f"答えは ${ft(P)}$。"],
                    "「ちょうど」の条件は、包含関係にある2つの事象の差で表す。",
                    [f"$n=2$ などの小さい場合に、目の組を表にして数えると、生徒の式では「{('最大値' if kind == 'max' else '最小値')}が $k$ でない組」も数えていることがわかる。"],
                    ["「以下」と「ちょうど」を区別しない。"],
                    chk=(expr, fp(P), None, "intermediate"))


@gen("error_correction", 3, ["common_error", "computation"])
def d_vec_expand(r):
    while True:
        p, q = r.randint(1, 5), r.randint(1, 5)
        d = r.choice([x for x in range(-p * q + 1, p * q) if x != 0])
        s, t = r.choice([1, 2, 3]), r.choice([1, 2, 3, -1, -2])
        val2 = s * s * p * p + 2 * s * t * d + t * t * q * q
        wr2 = s * s * p * p + t * t * q * q
        if val2 > 0 and val2 != wr2:
            break
    vt = vcomb(s, t)
    val = sp.sqrt(val2)
    wrong = f"$|{vt}|^2={c1(s * s)}|\\vec{{a}}|^2+{c1(t * t)}|\\vec{{b}}|^2={wr2}$ より、$|{vt}|={sp.latex(sp.sqrt(wr2))}$。"
    return err_item(f"$|\\vec{{a}}|={p},\\ |\\vec{{b}}|={q},\\ \\vec{{a}}\\cdot\\vec{{b}}={d}$ のとき、$|{vt}|$ を求めよ。", wrong,
                    f"$|{vt}|^2$ を展開した部分", "formula",
                    "$(sa+tb)^2$ を $s^2a^2+t^2b^2$ とする文字式の誤りと同じで、内積の項 $2st\\,\\vec{a}\\cdot\\vec{b}$ を忘れている。$\\vec{a}\\cdot\\vec{b}$ が与えられているのに使っていないことにも注目する。",
                    f"$|{vt}|^2={c1(s * s)}|\\vec{{a}}|^2{'+' if 2 * s * t >= 0 else '-'}{abs(2 * s * t)}\\vec{{a}}\\cdot\\vec{{b}}+{c1(t * t)}|\\vec{{b}}|^2={val2}$ より $|{vt}|={sp.latex(val)}$。",
                    f"${sp.latex(val)}$", "内積は分配法則が成り立つので、展開すると $\\vec{a}\\cdot\\vec{b}$ の項が2つ現れる。",
                    [f"$|{vt}|^2=({vt})\\cdot({vt})$。", f"$={c1(s * s)}|\\vec{{a}}|^2{'+' if s * t > 0 else '-'}{abs(2 * s * t)}\\vec{{a}}\\cdot\\vec{{b}}+{c1(t * t)}|\\vec{{b}}|^2$。",
                     f"$={s * s * p * p}{'+' if 2 * s * t * d >= 0 else '-'}{abs(2 * s * t * d)}+{t * t * q * q}={val2}$。", f"$|{vt}|={sp.latex(val)}$。"],
                    "大きさを求めるときは $|\\vec{v}|^2=\\vec{v}\\cdot\\vec{v}$ として、内積の分配法則で展開する。",
                    ["$\\vec{a}\\cdot\\vec{b}=0$（垂直）の場合だけ生徒の式は正しい。与えられた内積が 0 でないことを確かめれば、誤りに気づける。"],
                    ["内積の項を落とす。", "$2st$ の係数の $2$ を落とす。"],
                    chk=(f"sqrt({s}**2*{p}**2+2*{s}*({t})*({d})+({t})**2*{q}**2)", str(val), None, "intermediate"))


@gen("error_correction", 2, ["common_error", "condition_check"])
def d_tangent_external(r):
    c = r.randint(-3, 3)
    p = r.randint(-3, 3)
    h = r.randint(1, 3)
    q = p * p + c - h * h
    t1, t2 = p - h, p + h
    lines = []
    for tt in (t1, t2):
        m_, n_ = 2 * tt, -tt * tt + c
        lines.append(f"y={poly(m_, n_)}" if m_ != 0 else f"y={n_}")
    curve = f"x^2{'+' if c > 0 else ''}{c if c else ''}"
    wl = f"y={poly(2 * p, q - 2 * p * p)}" if p != 0 else f"y={q}"
    wrong = f"$y'=2x$ より、点 $({p},\\ {q})$ における傾きは $2\\times({p})={2 * p}$。よって接線は ${wl}$。"
    return err_item(f"点 $\\mathrm{{P}}({p},\\ {q})$ から放物線 $y={curve}$ に引いた接線の方程式をすべて求めよ。", wrong,
                    f"点 P での微分係数 $2\\times({p})$ を傾きとした部分", "concept",
                    "「接線の傾きは微分係数」という知識を、曲線上にない点 P にそのまま当てはめている。点 P は曲線上の点ではない（$" + f"{p}^2{'+' if c >= 0 else ''}{c}={p * p + c}\\neq{q}" + "$）。",
                    f"接点を $(t,\\ t^2{'+' if c >= 0 else ''}{c})$ とおくと接線は $y=2tx-t^2{'+' if c >= 0 else ''}{c}$。これが P を通るので $t^2-{2 * p}t{'+' if q - c >= 0 else '-'}{abs(q - c)}=0$、$t={t1},\\ {t2}$。",
                    f"${lines[0]}$、${lines[1]}$",
                    f"接点の $x$ 座標は $t={t1},\\ {t2}$ の2つ。",
                    [f"P が曲線上にあるかを確かめる：$x={p}$ のとき $y={p * p + c}\\neq{q}$ なので P は曲線外。",
                     f"接点 $(t,\\ t^2{'+' if c >= 0 else ''}{c})$ での接線：$y=2t(x-t)+t^2{'+' if c >= 0 else ''}{c}=2tx-t^2{'+' if c >= 0 else ''}{c}$。",
                     f"P を通る：${q}=2t\\cdot({p})-t^2{'+' if c >= 0 else ''}{c}$ より $t={t1},\\ {t2}$。",
                     f"接線は ${lines[0]}$ と ${lines[1]}$。"],
                    "曲線外の点から引く接線は、接点を文字でおいてから、その接線が与えられた点を通る条件で接点を決める。",
                    ["接線を $y=m(x-" + f"({p})" + ")" + f"+({q})" + "$ とおき、放物線の式と連立した二次方程式の判別式が 0 になる条件から $m$ を求めても同じ結果になる。"],
                    ["与えられた点が曲線上にあるかを確かめずに、その点の微分係数を傾きにする。"],
                    chk=(f"solve(t**2-2*({p})*t+({q})-({c}), t)", f"[{t1}, {t2}]", "set", "intermediate"))


GENERATORS = [a_abs_integral, a_dice_extreme, a_vec_norm, a_cond_prob, a_repeated_trial,
              b_tangent_area, b_vec_intersection, b_series_game, b_volume, b_vec_foot,
              c_integral_eq, c_prob_recur, c_vec_triangle, c_box_max,
              d_cond_prob, d_dice_max, d_vec_expand, d_tangent_external]
