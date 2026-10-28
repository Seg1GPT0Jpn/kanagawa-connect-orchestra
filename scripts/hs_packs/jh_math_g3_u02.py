"""単元パック：中学3年 平方根（神奈川県公立高校入試形式）。"""
import math
import re
import unicodedata
from fractions import Fraction as Fr

from banks._common import figure, mc, num, shape
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem, tp)

UNIT_ID = "JH-MATH-G3-U02"

PREREQUISITES = [
    ("JH-MATH-G1-U01", "正の数・負の数の計算と累乗、素因数分解ができること。$\\sqrt{72}=\\sqrt{2^3\\times3^2}$ のように根号の中を整理するときに使う。"),
    ("JH-MATH-G3-U01", "乗法公式と因数分解。$(\\sqrt{3}+1)^2$ の展開や、式の値を因数分解してから代入する計算に使う。"),
    ("JH-MATH-G1-U05", "正方形の面積と1辺の長さの関係。面積が $2$ cm² の正方形の1辺の長さとして $\\sqrt{2}$ を導入する。"),
]
EXTENSIONS = [
    ("JH-MATH-G3-U03", "二次方程式 $x^2=k$ や $(x+p)^2=q$ を平方根の考えで解き、解の公式で根号をふくむ解を表す。"),
    ("JH-MATH-G3-U07", "三平方の定理で、直角三角形の辺の長さや対角線の長さを $a\\sqrt{b}$ の形で求める。"),
    ("HS-MATH1-U01", "高校の数と式で、実数・絶対値・分母の有理化（$\\dfrac{1}{\\sqrt{a}+\\sqrt{b}}$ の形）や二重根号へ発展する。"),
]


# ----------------------------------------------------------------------
# 共通ヘルパー
# ----------------------------------------------------------------------

def _norm(s):
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", s))


def MC(stem, right, cands, e, k=3, **kw):
    """正答 right と誤答候補 [(文, 理由, 誤概念)] から、重複を除いて k 個の誤答を選ぶ。"""
    seen, ws = {_norm(right)}, []
    for t, why, mis in cands:
        if _norm(t) in seen:
            continue
        seen.add(_norm(t))
        ws.append((t, why, mis))
        if len(ws) == k:
            break
    assert len(ws) == k, (stem, right, cands)
    return mc(stem, [right] + [w[0] for w in ws], e, why={w[0]: (w[1], w[2]) for w in ws}, **kw)


def ftex(v):
    v = Fr(v)
    if v.denominator == 1:
        return str(v.numerator)
    s = "-" if v < 0 else ""
    return f"{s}\\dfrac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def par(v):
    s = ftex(v)
    return f"({s})" if Fr(v) < 0 else s


def sqf(n):
    """n = a^2 b（b はできるだけ小さい自然数）となる (a, b)。"""
    a, b, k = 1, n, 2
    while k * k <= b:
        while b % (k * k) == 0:
            b //= k * k
            a *= k
        k += 1
    return a, b


def is_sq(n):
    return n >= 0 and math.isqrt(n) ** 2 == n


SQF = [2, 3, 5, 6, 7, 10, 11, 13, 14, 15]


# --- 根号をふくむ数（{根号の中: 係数} の辞書。根号の中 1 は有理数部分）---

def R(n, c=1):
    """c√n（自動で簡単にする）。"""
    a, b = sqf(n)
    return {b: Fr(c) * a} if c else {}


def add(*xs):
    out = {}
    for x in xs:
        for b, c in x.items():
            out[b] = out.get(b, Fr(0)) + c
    return {b: c for b, c in out.items() if c != 0}


def scal(x, k):
    return {b: c * Fr(k) for b, c in x.items() if c * Fr(k) != 0}


def mul(x, y):
    out = {}
    for b1, c1 in x.items():
        for b2, c2 in y.items():
            a, b = sqf(b1 * b2)
            out = add(out, {b: c1 * c2 * a})
    return out


def _term(b, c, first):
    neg = c < 0
    m = abs(c)
    if b == 1:
        body = ftex(m)
    elif m.denominator == 1:
        body = ("" if m == 1 else str(m)) + f"\\sqrt{{{b}}}"
    else:
        body = f"\\dfrac{{{'' if m.numerator == 1 else m.numerator}\\sqrt{{{b}}}}}{{{m.denominator}}}"
    if first:
        return ("-" if neg else "") + body
    return ("-" if neg else "+") + body


def tex(x):
    if not x:
        return "0"
    keys = sorted(x)
    return "".join(_term(b, x[b], i == 0) for i, b in enumerate(keys))


def T(x):
    return f"${tex(x)}$"


def py(x):
    if not x:
        return "0"
    return "+".join(f"({c.numerator})*sqrt({b})/({c.denominator})" for b, c in sorted(x.items()))


def val(x):
    return sum(float(c) * math.sqrt(b) for b, c in x.items())


def MARK(stem, x, e, expr, **kw):
    """あいう方式（0〜9 のマーク）で答える数値問題。x は 0 以上の有理数か、c√b（c>0）の形の数。"""
    if not isinstance(x, dict):
        x = {1: Fr(x)} if x else {}
    assert len(x) <= 1, x
    if not x or 1 in x:
        v = x.get(1, Fr(0))
        assert v >= 0
        if v.denominator == 1:
            n = int(v)
            return num(stem, str(n), e, mark=("int", n), chk=(expr, str(n), None, "answer"), **kw)
        p, q = v.numerator, v.denominator
        return num(stem, f"${ftex(v)}$", e, mark=("frac", p, q), chk=(expr, f"Rational({p},{q})", None, "answer"), **kw)
    (b, c), = x.items()
    assert c > 0
    if c.denominator == 1:
        m = ("root", b) if c == 1 else ("coef_root", int(c), b)
    else:
        assert c.numerator > 1  # 係数 1 のマーク欄（「1」をマークさせる形）は入試で使わない
        m = ("frac_root", c.numerator, b, c.denominator)
    return num(stem, T(x), e, mark=m, chk=(expr, py(x), None, "answer"), **kw)


SEL4 = "次の1〜4の中から1つ選び，その番号を答えなさい。"


def _robust(g):
    """選択肢が重複して誤答が足りないパラメータのときは、同じ乱数列から別のパラメータを引き直す。"""
    import random as _random
    fn = g.fn

    def wrapped(r):
        for _ in range(60):
            try:
                return fn(r)
            except AssertionError:
                r = _random.Random(r.random())
        return fn(r)
    wrapped.__name__ = fn.__name__
    g.fn = wrapped
    return g


# ----------------------------------------------------------------------
# 授業プリント
# ----------------------------------------------------------------------

_SQ_FIG = figure("方眼の上の、面積が 2 の正方形（1目もりの正方形の対角線を1辺とする）",
                 shape({"A": (1, 0), "B": (2, 1), "C": (1, 2), "D": (0, 1), "P": (0, 0), "Q": (2, 0), "R": (2, 2), "S": (0, 2)},
                       labels={"A": "A", "B": "B", "C": "C", "D": "D"},
                       segments=[("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")],
                       dashed=[("P", "Q"), ("Q", "R"), ("R", "S"), ("S", "P"), ("D", "B"), ("A", "C")], scale=48))

LESSON = lesson(
    goals=["平方根の意味を理解し、正の数には平方根が2つあること、根号 $\\sqrt{\\ }$ を使った表し方を説明できる。",
           "$\\sqrt{a}\\times\\sqrt{b}=\\sqrt{ab}$ などの性質を根拠に、根号をふくむ式の乗除・加減・分母の有理化ができる。",
           "有理数と無理数の違いを理解し、平方根の大小比較や近似値を使った考察ができる。"],
    duration=100,
    readiness=["正の数・負の数の乗法と累乗（$(-3)^2=9$、$-3^2=-9$）ができる。",
               "自然数を素因数分解できる（$72=2^3\\times3^2$）。",
               "分数の約分・通分と、分配法則・乗法公式による式の展開ができる。"],
    flow=[("導入：面積が 2 の正方形", 10, "方眼の上で面積 $2$ の正方形をかき、1辺の長さを考える"),
          ("平方根の定義と根号", 15, "平方根・根号の定義、$(\\sqrt{a})^2=a$、負の数の平方根がないこと"),
          ("大小と有理数・無理数", 15, "$a<b$ ならば $\\sqrt{a}<\\sqrt{b}$、有理数・無理数の区別、近似値"),
          ("乗法・除法の性質と変形", 20, "$\\sqrt{a}\\times\\sqrt{b}=\\sqrt{ab}$ の証明、$a\\sqrt{b}$ の形への変形（例題1）"),
          ("分母の有理化と加減", 20, "分母の有理化、同じ数の根号をふくむ項の加減（例題2・3）"),
          ("式の値とまとめ", 20, "乗法公式を使った計算と式の値（例題4）、確認問題")],
    sections=[
        intro("in1", "面積が 2 の正方形の1辺は？",
              "方眼の1目もりを $1$ cm とする。右の図のように、4つの正方形の対角線を結んでできる正方形 ABCD の面積は、大きな正方形（面積 $4$）の半分で $2$ cm² である。では、この正方形の1辺の長さは何 cm だろうか。$1^2=1$、$2^2=4$ なので、1辺の長さは $1$ と $2$ の間にあり、2乗すると $2$ になる数である。",
              bullets=["$1.4^2=1.96$、$1.5^2=2.25$ なので、1辺は $1.4$ と $1.5$ の間。", "さらに調べると $1.41^2=1.9881$、$1.42^2=2.0164$。どこまで調べても終わらない。", "このような数を、根号 $\\sqrt{\\ }$ を使って $\\sqrt{2}$ と表す。"],
              figure=_SQ_FIG,
              points=[tp("方眼紙で実際に面積 $2$ の正方形をかかせ、1辺を定規で測らせる（約 $1.4$ cm）。", ask="面積が $2$ cm² の正方形の1辺は何 cm か。", expect="$1.4$ cm くらい。ちょうどの数は書けない。", timing="導入の最初"),
                      tp("電卓で $1.41421356\\cdots$ と表示させ、小数がどこまでも続くことに気づかせる。", caution="「$\\sqrt{2}=1.41$」と等号で書かないよう、近似値であることを強調する。")]),
        definition("df1", "平方根と根号",
                   "2乗すると $a$ になる数を、$a$ の平方根という。正の数 $a$ の平方根は正と負の2つあり、絶対値が等しい。正の方を $\\sqrt{a}$、負の方を $-\\sqrt{a}$ と表し、まとめて $\\pm\\sqrt{a}$ と書く。記号 $\\sqrt{\\ }$ を根号といい、$\\sqrt{a}$ を「ルート $a$」と読む。",
                   formula="$$(\\sqrt{a})^2=a,\\qquad(-\\sqrt{a})^2=a\\qquad(a>0)$$",
                   conditions=["$0$ の平方根は $0$ だけである（$\\sqrt{0}=0$）。", "負の数を2乗すると正の数になるので、負の数の平方根はない（中学校の範囲）。",
                               "$\\sqrt{a}$ は正の数（$a>0$ のとき）。$\\sqrt{9}=3$ であり、$\\sqrt{9}=\\pm3$ ではない。", "$a>0$ のとき $\\sqrt{a^2}=a$、$\\sqrt{(-a)^2}=a$。"],
                   points=[tp("「$9$ の平方根」と「$\\sqrt{9}$」の違いを対比させる。", ask="$9$ の平方根は何か。$\\sqrt{9}$ はいくつか。", expect="$9$ の平方根は $\\pm3$、$\\sqrt{9}$ は $3$。", caution="「$\\sqrt{9}=\\pm3$」と書く誤りがとても多い。")]),
        definition("df2", "平方根の大小、有理数と無理数",
                   "$a$、$b$ が正の数で $a<b$ ならば $\\sqrt{a}<\\sqrt{b}$ である（面積の大きい正方形ほど1辺も長い）。また、整数 $m$ と $0$ でない整数 $n$ を使って分数 $\\dfrac{m}{n}$ の形で表せる数を有理数、表せない数を無理数という。",
                   conditions=["$\\sqrt{2}$、$\\sqrt{3}$、$\\sqrt{5}$、円周率 $\\pi$ は無理数。無理数を小数で表すと、循環しない無限小数になる。",
                               "$\\sqrt{4}=2$、$\\sqrt{0.09}=0.3$、$\\sqrt{\\dfrac{4}{9}}=\\dfrac{2}{3}$ のように、根号を使っていても有理数のものがある。",
                               "大小を比べるときは、それぞれを2乗して比べるか、$3=\\sqrt{9}$ のように根号の形にそろえる。"],
                   points=[tp("$3$ と $\\sqrt{10}$、$2\\sqrt{3}$ と $3\\sqrt{2}$ を2乗して比べる方法を示す。", ask="$2\\sqrt{3}$ と $3\\sqrt{2}$ はどちらが大きいか。", expect="2乗すると $12$ と $18$ なので $3\\sqrt{2}$ の方が大きい。")]),
        theorem("th1", "根号をふくむ数の乗法・除法",
                "$$\\sqrt{a}\\times\\sqrt{b}=\\sqrt{ab},\\qquad \\dfrac{\\sqrt{a}}{\\sqrt{b}}=\\sqrt{\\dfrac{a}{b}},\\qquad \\sqrt{a^2b}=a\\sqrt{b}$$",
                ["$a$、$b$ は正の数。", "根号の中を素因数分解し、2乗の形になっている部分を根号の外に出す（$\\sqrt{72}=\\sqrt{6^2\\times2}=6\\sqrt{2}$）。",
                 "答えは、根号の中をできるだけ小さい自然数にして表す。", "加法では $\\sqrt{a}+\\sqrt{b}=\\sqrt{a+b}$ は成り立たない（$\\sqrt{9}+\\sqrt{16}=7$、$\\sqrt{25}=5$）。"],
                proof=["$\\sqrt{a}\\times\\sqrt{b}$ を2乗すると、$(\\sqrt{a}\\times\\sqrt{b})^2=(\\sqrt{a})^2\\times(\\sqrt{b})^2=a\\times b=ab$。",
                       "したがって $\\sqrt{a}\\times\\sqrt{b}$ は、2乗すると $ab$ になる数、つまり $ab$ の平方根である。",
                       "$\\sqrt{a}>0$、$\\sqrt{b}>0$ なので、$\\sqrt{a}\\times\\sqrt{b}>0$。$ab$ の平方根のうち正の方だから、$\\sqrt{a}\\times\\sqrt{b}=\\sqrt{ab}$。",
                       "同じように $\\left(\\dfrac{\\sqrt{a}}{\\sqrt{b}}\\right)^2=\\dfrac{a}{b}$ で正の数だから、$\\dfrac{\\sqrt{a}}{\\sqrt{b}}=\\sqrt{\\dfrac{a}{b}}$。",
                       "また $\\sqrt{a^2b}=\\sqrt{a^2}\\times\\sqrt{b}=a\\sqrt{b}$（$a>0$）。"],
                points=[tp("「平方根の定義（2乗すると $ab$）」と「正の数であること」の2点で説明が完成することを強調する。", ask="$\\sqrt{2}\\times\\sqrt{3}$ が $\\sqrt{6}$ になる理由を説明できるか。", expect="2乗すると $6$ になる正の数だから。")]),
        derivation("dv1", "分母の有理化を導く",
                   ["$\\dfrac{a}{\\sqrt{b}}$ の分母と分子に $\\sqrt{b}$ をかける（分数の値は変わらない）。",
                    "分母は $\\sqrt{b}\\times\\sqrt{b}=(\\sqrt{b})^2=b$ となり、根号がなくなる。",
                    "よって $\\dfrac{a}{\\sqrt{b}}=\\dfrac{a\\sqrt{b}}{b}$。たとえば $\\dfrac{6}{\\sqrt{3}}=\\dfrac{6\\sqrt{3}}{3}=2\\sqrt{3}$。",
                    "分母に根号をふくまない形に直すことを、分母を有理化するという。近似値の計算（$\\dfrac{1}{\\sqrt{2}}=\\dfrac{\\sqrt{2}}{2}\\fallingdotseq\\dfrac{1.414}{2}$）が楽になる。"],
                   points=[tp("分母と分子に同じ数をかけても値が変わらないこと（小学校の分数の性質）を根拠として確認する。", caution="分子だけに $\\sqrt{b}$ をかける誤りが多い。")]),
        example("ex1", "例題1　$a\\sqrt{b}$ の形に変形する",
                "$\\sqrt{72}$ と $\\sqrt{0.27}$ を、根号の中ができるだけ小さい自然数になるように変形しなさい。",
                ["$72=2^3\\times3^2=6^2\\times2$ なので $\\sqrt{72}=6\\sqrt{2}$。",
                 "$0.27=\\dfrac{27}{100}=\\dfrac{3^2\\times3}{10^2}$ なので $\\sqrt{0.27}=\\dfrac{3\\sqrt{3}}{10}$。"],
                "$6\\sqrt{2}$、$\\dfrac{3\\sqrt{3}}{10}$",
                thinking="根号の中を素因数分解し、同じ数が2つそろった組（2乗）を見つけて外に出す。",
                points=[tp("$72=4\\times18$ と分けて $2\\sqrt{18}$ で止まってしまう例を示し、根号の中に2乗の因数が残っていないかを必ず確かめさせる。")],
                misconceptions=[("$\\sqrt{72}=2\\sqrt{18}$ で終わりにする", "$18=3^2\\times2$ なので、さらに $6\\sqrt{2}$ まで変形する")]),
        example("ex2", "例題2　分母の有理化と乗除",
                "$\\sqrt{6}\\times\\sqrt{15}\\div\\sqrt{5}$ と $\\dfrac{10}{\\sqrt{5}}$ を計算しなさい。",
                ["$\\sqrt{6}\\times\\sqrt{15}\\div\\sqrt{5}=\\sqrt{\\dfrac{6\\times15}{5}}=\\sqrt{18}=3\\sqrt{2}$。",
                 "$\\dfrac{10}{\\sqrt{5}}=\\dfrac{10\\times\\sqrt{5}}{\\sqrt{5}\\times\\sqrt{5}}=\\dfrac{10\\sqrt{5}}{5}=2\\sqrt{5}$。"],
                "$3\\sqrt{2}$、$2\\sqrt{5}$",
                thinking="乗除はまとめて1つの根号の中で計算し、最後に $a\\sqrt{b}$ の形にする。",
                points=[tp("$\\dfrac{10}{\\sqrt{5}}$ は「$10=2\\times5=2\\times\\sqrt{5}\\times\\sqrt{5}$ なので約分できる」という見方も紹介する。", timing="例題2のあと")]),
        example("ex3", "例題3　根号をふくむ式の加減",
                "$\\sqrt{50}-\\sqrt{8}+\\dfrac{6}{\\sqrt{2}}$ を計算しなさい。",
                ["$\\sqrt{50}=5\\sqrt{2}$、$\\sqrt{8}=2\\sqrt{2}$、$\\dfrac{6}{\\sqrt{2}}=\\dfrac{6\\sqrt{2}}{2}=3\\sqrt{2}$。",
                 "$5\\sqrt{2}-2\\sqrt{2}+3\\sqrt{2}=(5-2+3)\\sqrt{2}=6\\sqrt{2}$。"],
                "$6\\sqrt{2}$",
                thinking="根号の中を同じ数にそろえると、文字式の同類項と同じように係数どうしを計算できる。",
                points=[tp("$\\sqrt{2}$ を文字 $x$ に置きかえると $5x-2x+3x=6x$ と同じ計算であることを示す。", ask="$2\\sqrt{3}+3\\sqrt{2}$ はまとめられるか。", expect="根号の中が違うのでまとめられない。")]),
        example("ex4", "例題4　乗法公式と式の値",
                "$x=\\sqrt{5}+2$ のとき、$x^2-4x+4$ の値を求めなさい。",
                ["$x^2-4x+4=(x-2)^2$ と因数分解する。", "$x-2=\\sqrt{5}$ なので、$(x-2)^2=(\\sqrt{5})^2=5$。"],
                "$5$",
                thinking="そのまま代入すると計算が長くなる。式を因数分解して、$x-2$ の値を利用する（式の展開と因数分解の単元とのつながり）。",
                points=[tp("直接代入した計算 $(\\sqrt{5}+2)^2-4(\\sqrt{5}+2)+4$ と比べ、因数分解の効果を実感させる。")]),
        board("bd1", "板書案",
              [("① 平方根の意味", ["2乗して $a$ になる数 → $a$ の平方根", "$a>0$：$\\pm\\sqrt{a}$（2つ）", "$\\sqrt{9}=3$（$\\pm$ はつかない）", "負の数の平方根はない", "有理数：$\\dfrac{m}{n}$ で表せる数"]),
               ("② 乗除と変形", ["$\\sqrt{a}\\sqrt{b}=\\sqrt{ab}$（2乗して $ab$、正の数）", "$\\sqrt{a^2b}=a\\sqrt{b}$", "$\\sqrt{72}=6\\sqrt{2}$", "有理化：$\\dfrac{a}{\\sqrt{b}}=\\dfrac{a\\sqrt{b}}{b}$"]),
               ("③ 加減と式の値", ["$\\sqrt{\\ }$ の中をそろえて係数を計算", "$5\\sqrt{2}-2\\sqrt{2}+3\\sqrt{2}=6\\sqrt{2}$", "$\\sqrt{a}+\\sqrt{b}\\neq\\sqrt{a+b}$", "式の値：因数分解してから代入"])],
              points=[tp("③の「$\\sqrt{a}+\\sqrt{b}\\neq\\sqrt{a+b}$」には、$\\sqrt{9}+\\sqrt{16}=7$、$\\sqrt{25}=5$ の反例を赤で書きそえる。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("「平方根」と「根号のついた数」を区別させる。$a$ の平方根は2つ、$\\sqrt{a}$ は正の1つ。", caution="$\\sqrt{(-3)^2}=-3$ とする誤りが入試でも多い。"),
               tp("$a\\sqrt{b}$ の形にするときは、根号の中を素因数分解してから2乗の組を外に出す手順を毎回書かせる。", ask="$\\sqrt{48}$ を変形しなさい。", expect="$48=4^2\\times3$ なので $4\\sqrt{3}$。"),
               tp("加減と乗除のルールの違いを表にまとめる。乗除は根号の中どうし、加減は係数どうし。", timing="例題3のあと"),
               tp("入試では答えを「根号の中をできるだけ小さい自然数」「分母に根号をふくまない」形で答えることを確認する。")],
              misconceptions=[("$\\sqrt{2}+\\sqrt{3}=\\sqrt{5}$", "加法では根号の中どうしをたせない。$\\sqrt{2}+\\sqrt{3}$ はこれ以上簡単にならない"),
                              ("$16$ の平方根は $4$", "$16$ の平方根は $\\pm4$。$\\sqrt{16}=4$ と区別する"),
                              ("$\\dfrac{6}{\\sqrt{3}}=6\\sqrt{3}$", "分母と分子の両方に $\\sqrt{3}$ をかけて $\\dfrac{6\\sqrt{3}}{3}=2\\sqrt{3}$")]),
        summary("sm1", "まとめ",
                ["正の数 $a$ の平方根は $\\pm\\sqrt{a}$ の2つ。$0$ の平方根は $0$、負の数の平方根はない。",
                 "$a<b$ ならば $\\sqrt{a}<\\sqrt{b}$。大小は2乗して比べる。分数で表せない数が無理数。",
                 "$\\sqrt{a}\\times\\sqrt{b}=\\sqrt{ab}$、$\\sqrt{a^2b}=a\\sqrt{b}$。答えは根号の中をできるだけ小さい自然数に。",
                 "分母の有理化：分母と分子に同じ根号をかける。", "加減は根号の中をそろえて係数を計算する。式の値は因数分解を利用する。"]),
        check("ck1", "確認問題",
              [("$\\sqrt{75}$ を $a\\sqrt{b}$ の形に変形しなさい。", "$5\\sqrt{3}$"),
               ("$\\dfrac{12}{\\sqrt{6}}$ の分母を有理化しなさい。", "$2\\sqrt{6}$"),
               ("$\\sqrt{27}+\\sqrt{12}-\\sqrt{3}$ を計算しなさい。", "$3\\sqrt{3}+2\\sqrt{3}-\\sqrt{3}=4\\sqrt{3}$"),
               ("$4$ と $\\sqrt{15}$ はどちらが大きいか。", "$4=\\sqrt{16}$ なので $4$ の方が大きい")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

@gen("basic_check", 4, ["concept", "condition_check"])
def a_root_meaning(r):
    kind = r.choice(["roots", "roots", "dec", "expr"])
    if kind == "roots":
        if r.random() < 0.5:
            k = r.randint(4, 15)
            N = k * k
            x = {1: Fr(k)}
        else:
            a, b = r.choice([2, 3, 4, 5]), r.choice([2, 3, 5, 6, 7])
            N = a * a * b
            x = R(N)
        s = tex(x)
        cands = [(f"${s}$", "正の方の平方根だけを答えている。負の数も2乗すると正の数になるので、平方根は2つある。", "平方根は1つだという思いこみ"),
                 (f"$-{s}$", "負の方の平方根だけを答えている。", "平方根は1つだという思いこみ"),
                 (f"$\\pm{N * N}$", f"${N}$ を2乗した数を答えている。平方根は「2乗すると ${N}$ になる数」である。", "平方と平方根の混同"),
                 (f"$\\pm{N // 2 if N % 2 == 0 else N * 2}$", f"「2乗する」ことと「2でわる・2倍する」ことを混同している。", "平方の意味の誤解")]
        return MC(f"${N}$ の平方根として正しいものを，" + SEL4, f"$\\pm{s}$", cands,
                  f"2乗すると ${N}$ になる数は ${s}$ と $-{s}$ の2つ。まとめて $\\pm{s}$。", d=1,
                  ap="「$a$ の平方根」は2乗すると $a$ になる数。正の数の平方根は正と負の2つある。",
                  steps=[f"$({s})^2={N}$、$(-{s})^2={N}$ を確かめる。", f"平方根は $\\pm{s}$。"],
                  alt=[f"$x^2={N}$ をみたす $x$ を求めると考えても、$x=\\pm{s}$ となる。"],
                  pc=[("正と負の2つがあることを理解している", 1), ("値を正しく求めている", 1)],
                  pit=["正の方だけを答える。", "根号の中を簡単にし忘れる。"],
                  chk=(f"({py(x)})**2", str(N), None, "intermediate"))
    if kind == "dec":
        k = r.randint(1, 9)
        if r.random() < 0.5:
            N = f"0.{k * k:02d}"
            s, w1 = f"0.{k}", f"0.0{k}"
            nv, sv = f"Rational({k * k},100)", f"Rational({k},10)"
            alt_ = f"${N}=\\dfrac{{{k * k}}}{{100}}$ と分数に直すと、平方根は $\\pm\\dfrac{{{k}}}{{10}}=\\pm{s}$ と分かる。"
        else:
            N = f"{k * k * 100}"
            s, w1 = f"{k * 10}", f"{k * 100}"
            nv, sv = str(k * k * 100), str(k * 10)
            alt_ = f"${N}={k * k}\\times100$ と考え、$\\sqrt{{{k * k}}}\\times\\sqrt{{100}}={k}\\times10$ としてもよい。"
        cands = [(f"$\\pm{w1}$", "位取りを誤っている。答えを2乗して確かめると、もとの数にならない。", "小数・位取りの誤り"),
                 (f"${s}$", "正の方の平方根だけを答えている。", "平方根は1つだという思いこみ"),
                 (f"$-{s}$", "負の方の平方根だけを答えている。", "平方根は1つだという思いこみ"),
                 (f"$\\pm{k}$", "小数点や0の位置を考えずに答えている。", "位取りの誤り")]
        return MC(f"${N}$ の平方根として正しいものを，" + SEL4, f"$\\pm{s}$", cands,
                  f"${s}^2={N}$ なので，${N}$ の平方根は $\\pm{s}$。", d=2,
                  ap="答えの候補を2乗して、もとの数になるかを確かめる。小数は位取りに注意する。",
                  steps=[f"${s}\\times{s}={N}$ を確かめる。", f"平方根は $\\pm{s}$。"],
                  alt=[alt_],
                  pc=[("位取りを正しく考えている", 1), ("正と負の2つを答えている", 1)],
                  pit=["$0.09$ の平方根を $\\pm0.03$ とする。", "負の方を忘れる。"],
                  chk=(f"({sv})**2", nv, None, "intermediate"))
    m = r.choice([2, 3, 5, 6, 7, 10, 11])
    k = r.randint(2, 9)
    forms = [(f"\\sqrt{{(-{k})^2}}", k, f"$(-{k})^2={k * k}$ なので $\\sqrt{{{k * k}}}={k}$。"),
             (f"-\\sqrt{{{k}^2}}", -k, f"$\\sqrt{{{k}^2}}={k}$ なので $-{k}$。"),
             (f"(-\\sqrt{{{m}}})^2", m, f"負の数の2乗は正の数。$(-\\sqrt{{{m}}})^2=(\\sqrt{{{m}}})^2={m}$。"),
             (f"-(\\sqrt{{{m}}})^2", -m, f"$(\\sqrt{{{m}}})^2={m}$ にマイナスがついて $-{m}$。"),
             (f"-\\sqrt{{(-{k})^2}}", -k, f"$\\sqrt{{(-{k})^2}}=\\sqrt{{{k * k}}}={k}$ にマイナスがついて $-{k}$。")]
    ex, v, why = r.choice(forms)
    a = abs(v)
    cands = [(f"${-v}$", "符号を誤っている。根号の中を先に計算し、根号の前の符号は最後に考える。", "根号と符号の扱いの誤り"),
             (f"$\\pm{a}$", "$\\sqrt{\\ }$ のついた数は1つの値を表す。$\\pm$ をつけるのは「平方根」を答えるときだけ。", "平方根と根号の混同"),
             (f"${v * a}$", "2乗と根号の関係を逆に使い、さらに2乗している。", "平方と平方根の混同"),
             (f"${-v * a}$", "2乗と根号の関係を誤り、符号も逆にしている。", "平方と平方根の混同")]
    return MC(f"${ex}$ を計算した結果として正しいものを，" + SEL4, f"${v}$", cands, why, d=2,
              ap="$\\sqrt{\\ }$ は「2乗すると中の数になる正の数」。$(\\sqrt{a})^2=a$、$a>0$ のとき $\\sqrt{a^2}=a$ を使う。",
              steps=["根号の中（またはかっこの中）を先に計算する。", why],
              alt=["2乗する前後の数を具体的に書き出して確かめる。たとえば $\\sqrt{(-3)^2}=\\sqrt{9}=3$。"],
              pc=[("根号の中・かっこの中を正しく計算している", 1), ("符号を正しく決めている", 1)],
              pit=["$\\sqrt{(-a)^2}=-a$ としてしまう。", "$\\sqrt{\\ }$ の値に $\\pm$ をつける。"],
              chk=(ex.replace("\\sqrt", "sqrt").replace("{", "(").replace("}", ")").replace("^", "**"), str(v), None, "intermediate"))


@gen("basic_check", 4, ["computation"])
def a_simplify(r):
    kind = r.choice(["fwd", "fwd", "back", "frac"])
    a = r.randint(2, 8)
    b = r.choice(SQF[:8])
    n = a * a * b
    if kind == "fwd":
        x = R(n)
        steps = [f"${n}$ を素因数分解して、2乗の因数を見つける：${n}={a}^2\\times{b}$。", f"$\\sqrt{{{n}}}=\\sqrt{{{a}^2}}\\times\\sqrt{{{b}}}={a}\\sqrt{{{b}}}$。"]
        return MARK(f"$\\sqrt{{{n}}}$ を，根号の中ができるだけ小さい自然数になるように変形しなさい。", x,
                    f"${n}={a}^2\\times{b}$ なので $\\sqrt{{{n}}}={a}\\sqrt{{{b}}}$。", f"sqrt({n})", d=1,
                    ap="根号の中を素因数分解し、2乗になっている部分（同じ数の組）を根号の外に出す。",
                    steps=steps, alt=[f"答えを2乗して $({a}\\sqrt{{{b}}})^2={a * a}\\times{b}={n}$ になることを確かめる。"],
                    pc=[("2乗の因数を見つけている", 1), ("正しく変形している", 1)],
                    pit=["2乗の因数の一部しか外に出さない（$\\sqrt{72}=2\\sqrt{18}$ で止める）。", "外に出す数を2乗のまま書く。"])
    if kind == "back":
        return MARK(f"${a}\\sqrt{{{b}}}$ を $\\sqrt{{a}}$ の形に表すとき，$a$ にあてはまる自然数を求めなさい。", n,
                    f"${a}\\sqrt{{{b}}}=\\sqrt{{{a}^2}}\\times\\sqrt{{{b}}}=\\sqrt{{{a * a}\\times{b}}}=\\sqrt{{{n}}}$。", f"{a}**2*{b}", d=1,
                    ap="根号の外の数は、2乗して根号の中に入れる。$a\\sqrt{b}=\\sqrt{a^2b}$。",
                    steps=[f"${a}=\\sqrt{{{a * a}}}$ と考える。", f"${a}\\sqrt{{{b}}}=\\sqrt{{{a * a}\\times{b}}}=\\sqrt{{{n}}}$。"],
                    alt=[f"両辺を2乗すると $({a}\\sqrt{{{b}}})^2={n}$ となり、$a={n}$ と分かる。"],
                    pc=[("外の数を2乗して中に入れている", 1), ("正しい値", 1)],
                    pit=[f"${a}$ を2乗せずに ${a}\\times{b}={a * b}$ とする。"])
    c = r.choice([q for q in (2, 3, 4, 5, 6, 7, 9, 10) if math.gcd(q, a * b) == 1])
    x = {b: Fr(a, c)}
    numer, denom = n, c * c
    return MARK(f"$\\sqrt{{\\dfrac{{{numer}}}{{{denom}}}}}$ を，分母に根号をふくまず，根号の中ができるだけ小さい自然数になるように変形しなさい。", x,
                f"$\\sqrt{{\\dfrac{{{numer}}}{{{denom}}}}}=\\dfrac{{\\sqrt{{{numer}}}}}{{\\sqrt{{{denom}}}}}=\\dfrac{{{a}\\sqrt{{{b}}}}}{{{c}}}$。", f"sqrt(Rational({numer},{denom}))", d=2,
                ap="$\\sqrt{\\dfrac{a}{b}}=\\dfrac{\\sqrt{a}}{\\sqrt{b}}$ と分けて、分子・分母をそれぞれ簡単にする。",
                steps=[f"$\\sqrt{{\\dfrac{{{numer}}}{{{denom}}}}}=\\dfrac{{\\sqrt{{{numer}}}}}{{\\sqrt{{{denom}}}}}$。", f"$\\sqrt{{{denom}}}={c}$、$\\sqrt{{{numer}}}={a}\\sqrt{{{b}}}$。", f"答えは $\\dfrac{{{a}\\sqrt{{{b}}}}}{{{c}}}$。"],
                alt=[f"答えを2乗して $\\dfrac{{{a * a}\\times{b}}}{{{c * c}}}=\\dfrac{{{numer}}}{{{denom}}}$ になることを確かめる。"],
                pc=[("分子・分母に分けて考えている", 1), ("正しく変形している", 1)],
                pit=["分母の根号をはずし忘れる。", "分子の2乗の因数を外に出し忘れる。"])


@gen("basic_check", 3, ["computation"])
def a_mul_div(r):
    kind = r.choice(["mul", "div", "coef", "three"])
    if kind == "mul":
        p, q = r.sample([2, 3, 5, 6, 7, 8, 10, 12, 14, 15, 18, 20, 21, 24, 27, 30], 2)
        x = R(p * q)
        ex, e, expr = f"\\sqrt{{{p}}}\\times\\sqrt{{{q}}}", f"$\\sqrt{{{p}\\times{q}}}=\\sqrt{{{p * q}}}={tex(x)}$。", f"sqrt({p})*sqrt({q})"
    elif kind == "div":
        q = r.choice([2, 3, 5, 6, 7])
        t = r.choice([2, 3, 6, 8, 12, 18, 20, 24, 27, 45, 50])
        p = q * t
        x = R(t)
        ex, e, expr = f"\\sqrt{{{p}}}\\div\\sqrt{{{q}}}", f"$\\sqrt{{\\dfrac{{{p}}}{{{q}}}}}=\\sqrt{{{t}}}={tex(x)}$。", f"sqrt({p})/sqrt({q})"
    elif kind == "coef":
        a, c = r.randint(2, 5), r.randint(2, 5)
        b, d = r.sample([2, 3, 5, 6, 7, 10], 2)
        x = mul(R(b, a), R(d, c))
        ex, e, expr = f"{a}\\sqrt{{{b}}}\\times{c}\\sqrt{{{d}}}", f"$({a}\\times{c})\\sqrt{{{b}\\times{d}}}={a * c}\\sqrt{{{b * d}}}={tex(x)}$。", f"{a}*sqrt({b})*{c}*sqrt({d})"
    else:
        p, q = r.sample([2, 3, 5, 6, 7, 10], 2)
        s = r.choice([v for v in (2, 3, 5, 6, 7, 10) if v not in (p, q)])
        ex = f"\\sqrt{{{p * s}}}\\times\\sqrt{{{q * s}}}\\div\\sqrt{{{s}}}"
        x = R(p * q * s)
        e, expr = f"$\\sqrt{{\\dfrac{{{p * s}\\times{q * s}}}{{{s}}}}}=\\sqrt{{{p * q * s}}}={tex(x)}$。", f"sqrt({p * s})*sqrt({q * s})/sqrt({s})"
    return MARK(f"${ex}$ を計算しなさい。", x, e, expr, d=2,
                ap="乗除は $\\sqrt{a}\\times\\sqrt{b}=\\sqrt{ab}$、$\\sqrt{a}\\div\\sqrt{b}=\\sqrt{\\dfrac{a}{b}}$ で1つの根号にまとめ、最後に $a\\sqrt{b}$ の形にする。",
                steps=["1つの根号にまとめる（係数は係数どうしかける）。", e.strip("。")],
                alt=["先にそれぞれを $a\\sqrt{b}$ の形にしてからかけても、同じ結果になる。"],
                pc=[("1つの根号にまとめている", 1), ("根号の中をできるだけ小さくしている", 1)],
                pit=["根号の中を簡単にし忘れる。", "係数どうしのかけ算を忘れる。"])


@gen("basic_check", 3, ["computation", "condition_check"])
def a_rationalize(r):
    b = r.choice([2, 3, 5, 6, 7, 10])
    kind = r.choice(["k", "k", "ck", "rr"])
    if kind == "k":
        k = r.choice([v for v in range(1, 21) if v != b])
        x = {b: Fr(k, b)}
        ex = f"\\dfrac{{{k}}}{{\\sqrt{{{b}}}}}"
        steps = [f"分母と分子に $\\sqrt{{{b}}}$ をかける：$\\dfrac{{{k}\\times\\sqrt{{{b}}}}}{{\\sqrt{{{b}}}\\times\\sqrt{{{b}}}}}=\\dfrac{{{k}\\sqrt{{{b}}}}}{{{b}}}$。", f"約分して ${tex(x)}$。"]
        expr = f"{k}/sqrt({b})"
    elif kind == "ck":
        c = r.randint(2, 5)
        k = r.choice([v for v in range(2, 31) if v % c == 0 or v % b == 0])
        x = {b: Fr(k, c * b)}
        ex = f"\\dfrac{{{k}}}{{{c}\\sqrt{{{b}}}}}"
        steps = [f"分母と分子に $\\sqrt{{{b}}}$ をかける：$\\dfrac{{{k}\\sqrt{{{b}}}}}{{{c}\\times{b}}}=\\dfrac{{{k}\\sqrt{{{b}}}}}{{{c * b}}}$。", f"約分して ${tex(x)}$。"]
        expr = f"{k}/({c}*sqrt({b}))"
    else:
        a = r.choice([v for v in (2, 3, 5, 6, 7, 10, 14, 15) if v != b])
        x = R(a * b, Fr(1, b))
        ex = f"\\dfrac{{\\sqrt{{{a}}}}}{{\\sqrt{{{b}}}}}"
        steps = [f"分母と分子に $\\sqrt{{{b}}}$ をかける：$\\dfrac{{\\sqrt{{{a}}}\\times\\sqrt{{{b}}}}}{{{b}}}=\\dfrac{{\\sqrt{{{a * b}}}}}{{{b}}}$。", f"根号の中と約分を整理して ${tex(x)}$。"]
        expr = f"sqrt({a})/sqrt({b})"
    return MARK(f"${ex}$ の分母を有理化しなさい。", x, steps[0].replace("をかける：", "をかけて ") + f" よって ${tex(x)}$。", expr, d=2,
                ap="分母と分子に同じ数（分母の根号）をかけても値は変わらない。$\\sqrt{b}\\times\\sqrt{b}=b$ で分母の根号が消える。",
                steps=steps,
                alt=[f"答えの近似値と、もとの式の近似値を電卓で比べて等しいことを確かめる。"],
                pc=[("分母と分子に同じ根号をかけている", 1), ("約分まで正しくしている", 1)],
                pit=["分子だけに根号をかける。", "最後の約分を忘れる。"])


def _cmp_pool(k):
    """k の近くの数の候補 [(tex, 2乗の値)]。"""
    pool = [(f"{k}", Fr(k * k))]
    for d in (1, 2, 3, -1, -2, -3):
        n = k * k + d
        if n > 1 and not is_sq(n):
            a, b = sqf(n)
            if a == 1:
                pool.append((f"\\sqrt{{{n}}}", Fr(n)))
    for b in (2, 3, 5, 6, 7):
        for a in range(2, k + 1):
            v = a * a * b
            if (k - 1) ** 2 < v < (k + 1) ** 2 and v != k * k:
                pool.append((f"{a}\\sqrt{{{b}}}", Fr(v)))
    for m in (2 * k - 1, 2 * k + 1):
        pool.append((f"\\dfrac{{{m}}}{{2}}", Fr(m * m, 4)))
    out, seen = [], set()
    for t, v in pool:
        if v not in seen:
            seen.add(v)
            out.append((t, v))
    return out


@gen("basic_check", 3, ["concept", "computation"])
def a_compare(r):
    k = r.randint(2, 6)
    pool = _cmp_pool(k)
    assert len(pool) >= 4
    four = r.sample(pool, 4)
    big = r.random() < 0.5
    best = max(four, key=lambda t: t[1]) if big else min(four, key=lambda t: t[1])
    word = "最も大きい" if big else "最も小さい"
    sq = lambda t: f"$({t[0]})^2={ftex(t[1])}$"  # noqa: E731
    cands = [(f"${t[0]}$", f"2乗すると {sq(t)}。正答の {sq(best)} の方が{'大きい' if big else '小さい'}。", "大小の比べ方の誤り") for t in four if t is not best]
    return MC(f"次の数のうち，{word}ものを，" + SEL4, f"${best[0]}$", cands,
              "それぞれ2乗すると " + "，".join(sq(t) for t in four) + f"。正の数どうしは2乗が{'大きい' if big else '小さい'}ほど{'大きい' if big else '小さい'}ので，{word}のは ${best[0]}$。", d=2,
              ap="正の数どうしは、2乗した値で大小を比べられる。$a\\sqrt{b}$ は $\\sqrt{a^2b}$、整数 $k$ は $\\sqrt{k^2}$ と考えてもよい。",
              steps=["それぞれの数を2乗する。", "2乗した値を比べる。", f"{word}のは ${best[0]}$。"],
              alt=["$\\sqrt{2}\\fallingdotseq1.414$、$\\sqrt{3}\\fallingdotseq1.732$ などの近似値を使って小数で比べてもよい。"],
              pc=[("2乗して比べる方法を使っている", 1), ("正しく選んでいる", 1)],
              pit=["$a\\sqrt{b}$ の係数だけを見て大小を決める。", "分数を小数に直さずに見た目で比べる。"],
              chk=(str(best[1]), str(best[1]), None, "intermediate"))


def _rat_pool(r):
    k = r.randint(2, 9)
    p, q = r.choice([(1, 2), (2, 3), (3, 4), (1, 3), (2, 5), (3, 5), (4, 7)])
    m = r.choice([2, 3, 5, 7])
    s = r.choice([2, 3])
    d = r.randint(1, 9)
    rat = [(f"\\sqrt{{{k * k}}}", f"$\\sqrt{{{k * k}}}={k}$ で整数（有理数）。"),
           (f"\\sqrt{{\\dfrac{{{p * p}}}{{{q * q}}}}}", f"$\\sqrt{{\\dfrac{{{p * p}}}{{{q * q}}}}}=\\dfrac{{{p}}}{{{q}}}$ で分数で表せる（有理数）。"),
           (f"\\sqrt{{0.{d * d:02d}}}" if d * d < 10 else f"\\sqrt{{0.{d * d}}}", f"$({'0.' + str(d)})^2={'0.' + format(d * d, '02d')}$ なので値は $0.{d}$（有理数）。"),
           (f"(\\sqrt{{{m}}})^2", f"$(\\sqrt{{{m}}})^2={m}$（有理数）。"),
           (f"\\sqrt{{{m}}}\\times\\sqrt{{{m * s * s}}}", f"$\\sqrt{{{m * m * s * s}}}={m * s}$（有理数）。"),
           (f"\\dfrac{{{p}}}{{{q}}}", "分数で表されているので有理数（小数で表すと循環小数または有限小数）。")]
    n2 = r.choice([2, 3, 5, 6, 7, 10, 11])
    d2 = r.choice([2, 3, 5, 6, 7, 8])
    irr = [(f"\\sqrt{{{n2}}}", f"${n2}$ は自然数の2乗ではないので $\\sqrt{{{n2}}}$ は無理数。"),
           ("\\pi", "円周率 $\\pi$ は無理数。"),
           (f"1+\\sqrt{{{n2}}}", f"有理数 $1$ に無理数 $\\sqrt{{{n2}}}$ を加えた数は無理数。"),
           (f"\\sqrt{{0.{d2}}}", f"$0.{d2}=\\dfrac{{{d2 * 10}}}{{100}}$ で、${d2 * 10}$ は自然数の2乗ではないので無理数（$0.{d2}$ を $0.0{d2}$ と見誤らない）。"),
           (f"\\dfrac{{\\sqrt{{{m}}}}}{{2}}", f"$\\sqrt{{{m}}}$ は無理数なので、それを $2$ でわった数も無理数。")]
    return rat, irr


@gen("basic_check", 3, ["condition_check", "concept"])
def a_rational(r):
    rat, irr = _rat_pool(r)
    want_irr = r.random() < 0.5
    if want_irr:
        right = r.choice(irr)
        wr = r.sample(rat, 3)
        stem = "次の数のうち，無理数であるものを，"
    else:
        right = r.choice(rat)
        wr = r.sample(irr, 3)
        stem = "次の数のうち，有理数であるものを，"
    cands = [(f"${t}$", why, "有理数・無理数の区別の誤り") for t, why in wr]
    return MC(stem + SEL4, f"${right[0]}$", cands, right[1], d=2,
              ap="有理数は「整数 $m$ と $0$ でない整数 $n$ で $\\dfrac{m}{n}$ と表せる数」。根号がついていても、計算すると整数や分数になるものは有理数。",
              steps=["それぞれの数を、できるだけ簡単な形に直す。", right[1]],
              alt=["根号の中が「自然数の2乗」や「分数で、分子・分母がともに自然数の2乗」かどうかで判断する。"],
              pc=[("それぞれを簡単な形に直している", 1), ("正しく判断している", 1)],
              pit=["根号がついているだけで無理数と判断する。", "$\\sqrt{0.4}$ を $0.2$ と誤る。"])


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 4, ["computation"])
def b_add_sub(r):
    b = r.choice([2, 3, 5, 6, 7])
    while True:
        ks = r.sample([1, 2, 3, 4, 5], 3)
        signs = [1, r.choice([1, -1]), r.choice([1, -1])]
        use_frac = r.random() < 0.5
        coef = sum(s * k for s, k in zip(signs, ks))
        if coef > 0:
            break
    parts, steps_parts, expr_parts = [], [], []
    for i, (s, k) in enumerate(zip(signs, ks)):
        sign = "" if i == 0 else ("+" if s > 0 else "-")
        if use_frac and i == 2:
            num_ = k * b
            parts.append(f"{sign}\\dfrac{{{num_}}}{{\\sqrt{{{b}}}}}")
            steps_parts.append(f"$\\dfrac{{{num_}}}{{\\sqrt{{{b}}}}}=\\dfrac{{{num_}\\sqrt{{{b}}}}}{{{b}}}={'' if k == 1 else k}\\sqrt{{{b}}}$")
            expr_parts.append(f"{'+' if s > 0 else '-'}{num_}/sqrt({b})")
        else:
            n = k * k * b
            parts.append(f"{sign}\\sqrt{{{n}}}")
            steps_parts.append(f"$\\sqrt{{{n}}}={'' if k == 1 else k}\\sqrt{{{b}}}$")
            expr_parts.append(f"{'+' if s > 0 else '-'}sqrt({n})")
    x = {b: Fr(coef)}
    ex = "".join(parts)
    comb = "".join(("" if i == 0 else ("+" if s > 0 else "-")) + f"{'' if k == 1 else k}\\sqrt{{{b}}}" for i, (s, k) in enumerate(zip(signs, ks)))
    return MARK(f"${ex}$ を計算しなさい。", x, f"{'，'.join(steps_parts)} より，${comb}={tex(x)}$。", "".join(expr_parts), d=3, p=4,
                ap="それぞれの項を $a\\sqrt{b}$ の形にして根号の中をそろえ、係数どうしを計算する。分母に根号があれば有理化する。",
                steps=["各項を変形する：" + "，".join(steps_parts) + "。", f"${comb}$。", f"係数を計算して ${tex(x)}$。"],
                alt=[f"$\\sqrt{{{b}}}$ を文字 $t$ とみると、同類項をまとめる計算と同じになる。"],
                pc=[("各項を $a\\sqrt{b}$ の形に直している", 2), ("係数の計算が正しい", 2)],
                pit=["根号の中どうしをたしたりひいたりする。", "有理化を忘れて項がそろわない。"])


def _expand_case(r):
    kind = r.choice(["sq1", "sq2", "diff1", "diff2", "pq"])
    a = r.choice([2, 3, 5, 6, 7])
    if kind == "sq1":
        b = r.choice([v for v in range(-5, 6) if v])
        ex = f"(\\sqrt{{{a}}}{'+' if b > 0 else '-'}{abs(b)})^2"
        x = add({1: Fr(a + b * b)}, R(a, 2 * b))
        w = [(T({1: Fr(a + b * b)}), "まん中の項 $2ab$ を忘れている。$(a+b)^2=a^2+2ab+b^2$。", "乗法公式の誤り"),
             (T(add({1: Fr(a + b * b)}, R(a, b))), "まん中の項を $2$ 倍していない。", "乗法公式の誤り"),
             (T(add({1: Fr(a + b * b)}, R(a, -2 * b))), "まん中の項の符号を誤っている。", "符号の誤り"),
             (T(add({1: Fr(a - b * b)}, R(a, 2 * b))), f"${par(b)}^2$ を負の数にしている。", "符号の誤り")]
        steps = [f"$(\\sqrt{{{a}}})^2+2\\times{par(b)}\\times\\sqrt{{{a}}}+{par(b)}^2$", f"$={a}{'+' if 2 * b > 0 else '-'}{abs(2 * b)}\\sqrt{{{a}}}+{b * b}={tex(x)}$"]
        py_ex = f"(sqrt({a})+({b}))**2"
    elif kind == "sq2":
        c = r.choice([v for v in (2, 3, 5, 6, 7, 10) if v != a])
        sgn = r.choice([1, -1])
        ex = f"(\\sqrt{{{a}}}{'+' if sgn > 0 else '-'}\\sqrt{{{c}}})^2"
        x = add({1: Fr(a + c)}, R(a * c, 2 * sgn))
        w = [(T({1: Fr(a + c)}), "まん中の項 $2ab$ を忘れている。", "乗法公式の誤り"),
             (T(add({1: Fr(a + c)}, R(a * c, -2 * sgn))), "まん中の項の符号を誤っている。", "符号の誤り"),
             ((f"${a + c}{'+' if sgn > 0 else '-'}2\\sqrt{{{a * c}}}$", "根号の中ができるだけ小さい自然数になっていない。", "根号の変形の不足") if sqf(a * c)[0] > 1
              else (T(add({1: Fr(a + c)}, R(a * c, sgn))), "まん中の項を2倍していない。", "乗法公式の誤り")),
             (T(add({1: Fr(a * a + c * c)}, R(a * c, 2 * sgn))), "$(\\sqrt{a})^2$ を $a^2$ としている。", "平方根の意味の誤り")]
        steps = [f"$(\\sqrt{{{a}}})^2{'+' if sgn > 0 else '-'}2\\sqrt{{{a}}}\\sqrt{{{c}}}+(\\sqrt{{{c}}})^2$", f"$={a + c}{'+' if sgn > 0 else '-'}2\\sqrt{{{a * c}}}={tex(x)}$"]
        py_ex = f"(sqrt({a})+({sgn})*sqrt({c}))**2"
    elif kind == "diff1":
        b = r.randint(1, 5)
        ex = f"(\\sqrt{{{a}}}+{b})(\\sqrt{{{a}}}-{b})"
        x = {1: Fr(a - b * b)} if a != b * b else {}
        w = [(T({1: Fr(a + b * b)}), "$-b^2$ の符号を誤っている。$(a+b)(a-b)=a^2-b^2$。", "乗法公式の誤り"),
             (T({1: Fr(a * a - b * b)}), "$(\\sqrt{a})^2$ を $a^2$ としている。", "平方根の意味の誤り"),
             (T({1: Fr(a - 2 * b)}), "$b^2$ を $2b$ としている。", "累乗の誤り"),
             (T({1: Fr(b * b - a)}), "ひく順番が逆になっている。", "符号の誤り")]
        steps = [f"$(\\sqrt{{{a}}})^2-{b}^2$", f"$={a}-{b * b}={tex(x)}$"]
        py_ex = f"(sqrt({a})+{b})*(sqrt({a})-{b})"
    elif kind == "diff2":
        c = r.choice([v for v in (2, 3, 5, 6, 7, 10, 11) if v != a])
        k = r.randint(2, 4)
        ex = f"({k}\\sqrt{{{a}}}+\\sqrt{{{c}}})({k}\\sqrt{{{a}}}-\\sqrt{{{c}}})"
        x = {1: Fr(k * k * a - c)}
        w = [(T({1: Fr(k * a - c)}), f"$({k}\\sqrt{{{a}}})^2$ を ${k}\\times{a}$ としている。係数も2乗する。", "累乗の誤り"),
             (T({1: Fr(k * k * a + c)}), "$-b^2$ の符号を誤っている。", "乗法公式の誤り"),
             (T({1: Fr(c - k * k * a)}), "ひく順番が逆になっている。", "符号の誤り"),
             (T({1: Fr(k * a * a - c)}), "$(\\sqrt{a})^2$ を $a^2$ としている。", "平方根の意味の誤り")]
        steps = [f"$({k}\\sqrt{{{a}}})^2-(\\sqrt{{{c}}})^2$", f"$={k * k * a}-{c}={tex(x)}$"]
        py_ex = f"({k}*sqrt({a})+sqrt({c}))*({k}*sqrt({a})-sqrt({c}))"
    else:
        p, q = r.sample([v for v in range(-5, 6) if v], 2)
        ex = f"(\\sqrt{{{a}}}{'+' if p > 0 else '-'}{abs(p)})(\\sqrt{{{a}}}{'+' if q > 0 else '-'}{abs(q)})"
        x = add({1: Fr(a + p * q)}, R(a, p + q))
        w = [(T({1: Fr(a + p * q)}), "まん中の項 $(p+q)\\sqrt{a}$ を忘れている。", "乗法公式の誤り"),
             (T(add({1: Fr(a + p * q)}, R(a, p * q))), "まん中の項の係数を $p\\times q$ にしている。$(x+p)(x+q)=x^2+(p+q)x+pq$。", "乗法公式の誤り"),
             (T(add({1: Fr(a + p + q)}, R(a, p * q))), "和と積を取り違えている。", "乗法公式の誤り"),
             (T(add({1: Fr(a - p * q)}, R(a, p + q))), "定数項の符号を誤っている。", "符号の誤り"),
             (T(add({1: Fr(a + p * q)}, R(a, -(p + q)))), "まん中の項の符号を誤っている。", "符号の誤り")]
        steps = [f"$(\\sqrt{{{a}}})^2+({ftex(p)}{'+' if q > 0 else ''}{ftex(q)})\\sqrt{{{a}}}+{par(p)}\\times{par(q)}$", f"$={tex(x)}$"]
        py_ex = f"(sqrt({a})+({p}))*(sqrt({a})+({q}))"
    return ex, x, w, steps, py_ex


@gen("standard_practice", 4, ["computation", "cross_unit"], rel=["JH-MATH-G3-U01"])
def b_expand(r):
    ex, x, w, steps, py_ex = _expand_case(r)
    return MC(f"${ex}$ を計算した結果として正しいものを，" + SEL4, T(x), w,
              f"乗法公式を使う。{steps[0]}{steps[1]}。", d=3, p=4,
              ap="$\\sqrt{a}$ を1つの文字とみて乗法公式（式の展開と因数分解の単元）を使い、最後に $(\\sqrt{a})^2=a$ で整理する。",
              steps=["使う乗法公式を決める。", steps[0] + "。", steps[1] + "。"],
              alt=["$\\sqrt{2}\\fallingdotseq1.41$ などの近似値を代入して、もとの式と答えの値がほぼ等しいかを確かめる。"],
              pc=[("適切な乗法公式を使っている", 2), ("$(\\sqrt{a})^2=a$ を使って正しく整理している", 2)],
              pit=["$(a+b)^2$ のまん中の項 $2ab$ を忘れる。", "$(k\\sqrt{a})^2$ で係数を2乗し忘れる。"],
              chk=(py_ex, py(x), None, "intermediate"))


@gen("standard_practice", 3, ["condition_check", "computation"])
def b_count(r):
    kind = r.choice(["between", "less", "range2"])
    if kind == "between":
        p = r.randint(2, 8)
        q = p + r.randint(1, 2)
        ans = q * q - p * p - 1
        stem = f"${p}<\\sqrt{{n}}<{q}$ をみたす自然数 $n$ は何個あるか求めなさい。"
        e = f"各辺を2乗して ${p * p}<n<{q * q}$。$n={p * p + 1},\\ \\cdots,\\ {q * q - 1}$ の ${ans}$ 個。"
        expr = f"{q * q}-{p * p}-1"
        steps = [f"各辺は正の数なので2乗しても大小は変わらない：${p * p}<n<{q * q}$。", f"自然数 $n$ は ${p * p + 1}$ から ${q * q - 1}$ まで。", f"個数は ${q * q - 1}-{p * p + 1}+1={ans}$。"]
    elif kind == "less":
        q = r.randint(3, 9)
        incl = r.random() < 0.5
        ans = q * q if incl else q * q - 1
        stem = f"$\\sqrt{{n}}{'\\leqq ' if incl else '<'}{q}$ をみたす自然数 $n$ は何個あるか求めなさい。"
        e = f"2乗して $n{'\\leqq ' if incl else '<'}{q * q}$。自然数 $n$ は $1$ から ${ans}$ までの ${ans}$ 個。"
        expr = str(ans)
        steps = [f"両辺を2乗して $n{'\\leqq ' if incl else '<'}{q * q}$。", f"自然数 $n$ は $1,\\ 2,\\ \\cdots,\\ {ans}$。", f"個数は ${ans}$。"]
    else:
        a = r.randint(2, 60)
        b = a + r.randint(10, 80)
        lo, hi = math.isqrt(a) + 1, math.isqrt(b - 1)
        ans = hi - lo + 1
        assert ans >= 1
        stem = f"$\\sqrt{{{a}}}<n<\\sqrt{{{b}}}$ をみたす自然数 $n$ は何個あるか求めなさい。"
        e = f"各辺を2乗して ${a}<n^2<{b}$。$n^2$ は ${', '.join(str(k * k) for k in range(lo, hi + 1))}$ なので，$n$ は ${ans}$ 個。"
        expr = f"{hi}-{lo}+1"
        steps = [f"各辺を2乗して ${a}<n^2<{b}$。", f"これをみたす平方数は ${'，'.join(str(k * k) for k in range(lo, hi + 1))}$。", f"$n={'，'.join(str(k) for k in range(lo, hi + 1))}$ の ${ans}$ 個。"]
    return MARK(stem, ans, e, expr, d=3, p=4,
                ap="正の数どうしの大小は、2乗しても変わらない。各辺を2乗して根号をはずし、条件をみたす自然数を数える。",
                steps=steps, alt=["条件の境目の数（たとえば $\\sqrt{n}$ がちょうど整数になる $n$）を書き出し、ふくむかどうかを1つずつ確かめる。"],
                pc=[("各辺を2乗して根号をはずしている", 2), ("端をふくむかどうかを正しく判断して数えている", 2)],
                pit=["不等号に等号がないのに、端の数まで数える。", "$n$ の個数を数えるとき、引き算だけして $1$ を足し忘れる（または引き忘れる）。"])


@gen("standard_practice", 3, ["condition_check", "concept"])
def b_square_n(r):
    kind = r.choice(["mul", "div", "sub"])
    if kind == "mul":
        s = r.choice([2, 3, 5, 6, 7, 10, 14, 15])
        t = r.randint(2, 6)
        k = s * t * t
        ans = s
        stem = f"$\\sqrt{{{k}n}}$ が自然数となるような自然数 $n$ のうち，最も小さいものを求めなさい。"
        e = f"${k}={t}^2\\times{s}$。$\\sqrt{{{k}n}}={t}\\sqrt{{{s}n}}$ が自然数になるには，$n={s}$ が最小。"
        steps = [f"${k}$ を素因数分解して ${k}={t}^2\\times{s}$。", f"根号の中が自然数の2乗になるには，${s}$ をもう1つかければよい。", f"$n={s}$ のとき $\\sqrt{{{k * s}}}={t * s}$。"]
        expr = str(s)
    elif kind == "div":
        s = r.choice([2, 3, 5, 6, 7, 10, 11])
        t = r.randint(2, 7)
        k = s * t * t
        ans = s
        stem = f"$\\sqrt{{\\dfrac{{{k}}}{{n}}}}$ が自然数となるような自然数 $n$ のうち，最も小さいものを求めなさい。"
        e = f"${k}={t}^2\\times{s}$。$n={s}$ のとき $\\sqrt{{{t * t}}}={t}$ で，これが最小の $n$。"
        steps = [f"${k}={t}^2\\times{s}$。", f"$\\dfrac{{{k}}}{{n}}$ が自然数の2乗になるには，$n$ が ${s}$ をふくむ ${k}$ の約数でなければならない。", f"最小は $n={s}$（$\\dfrac{{{k}}}{{{s}}}={t * t}$）。"]
        expr = str(s)
    else:
        M = r.randint(20, 120)
        largest = r.random() < 0.5
        if largest:
            if is_sq(M):
                M += 1
            ans = M - 1
            stem = f"$\\sqrt{{{M}-n}}$ が自然数となるような自然数 $n$ のうち，最も大きいものを求めなさい。"
            e = f"${M}-n$ が自然数の2乗で最も小さいのは $1$。$n={M}-1={ans}$。"
            steps = [f"${M}-n$ は自然数の2乗（$1,\\ 4,\\ 9,\\ \\cdots$）。", f"$n$ を最も大きくするには ${M}-n=1$。", f"$n={ans}$。"]
            expr = f"{M}-1"
        else:
            m = math.isqrt(M - 1)
            ans = M - m * m
            stem = f"$\\sqrt{{{M}-n}}$ が自然数となるような自然数 $n$ のうち，最も小さいものを求めなさい。"
            e = f"${M}$ より小さい最大の平方数は ${m * m}$。${M}-n={m * m}$ より $n={ans}$。"
            steps = [f"$n\\geqq 1$ なので ${M}-n\\leqq {M - 1}$。", f"${M - 1}$ 以下で最大の平方数は ${m}^2={m * m}$。", f"$n={M}-{m * m}={ans}$。"]
            expr = f"{M}-{m * m}"
    return MARK(stem, ans, e, expr, d=3, p=4,
                ap="根号の中が「自然数の2乗」になれば、根号がはずれて自然数になる。素因数分解して、2乗の組にならない因数に注目する。",
                steps=steps, alt=["答えの $n$ を実際に代入して根号がはずれることを確かめ、それより小さい（大きい）$n$ ではうまくいかないことを確かめる。"],
                pc=[("根号の中が自然数の2乗になる条件をとらえている", 2), ("最小（最大）の $n$ を正しく求めている", 2)],
                pit=["根号の中の数をすべて素因数分解せずに考える。", "$\\sqrt{0}=0$ は自然数でないことを見落とす。"])


@gen("standard_practice", 3, ["computation", "cross_unit"], rel=["JH-MATH-G3-U01"])
def b_value(r):
    kind = r.choice(["shift", "xy_sum", "xy_diff", "xy_prod", "xy_mix"])
    if kind == "shift":
        a = r.choice([2, 3, 5, 6, 7, 10, 11, 13])
        b = r.choice([v for v in range(-4, 5) if v])
        target = r.randint(1, 15)
        q = target - a + b * b
        P, Q = -2 * b, q
        xs = f"\\sqrt{{{a}}}{'+' if b > 0 else '-'}{abs(b)}"
        f_ = "x^2" + (f"{'+' if P > 0 else '-'}{abs(P)}x" if P else "") + (f"{'+' if Q > 0 else '-'}{abs(Q)}" if Q else "")
        x = {1: Fr(target)}
        stem = f"$x={xs}$ のとき，${f_}$ の値を求めなさい。"
        e = f"${f_}=(x{'-' if b > 0 else '+'}{abs(b)})^2{'+' if q - b * b >= 0 else '-'}{abs(q - b * b)}$。$x{'-' if b > 0 else '+'}{abs(b)}=\\sqrt{{{a}}}$ なので ${a}{'+' if q - b * b >= 0 else '-'}{abs(q - b * b)}={target}$。"
        expr = f"(sqrt({a})+({b}))**2+({P})*(sqrt({a})+({b}))+({Q})"
        steps = [f"${f_}=(x{'-' if b > 0 else '+'}{abs(b)})^2{'+' if q - b * b >= 0 else '-'}{abs(q - b * b)}$ と変形する。", f"$x{'-' if b > 0 else '+'}{abs(b)}=\\sqrt{{{a}}}$ を代入：$(\\sqrt{{{a}}})^2{'+' if q - b * b >= 0 else '-'}{abs(q - b * b)}$。", f"$={target}$。"]
    else:
        a, c = sorted(r.sample([2, 3, 5, 6, 7, 10, 11], 2), reverse=True)
        xs, ys = f"\\sqrt{{{a}}}+\\sqrt{{{c}}}", f"\\sqrt{{{a}}}-\\sqrt{{{c}}}"
        if kind == "xy_sum":
            f_, x = "x^2-y^2", R(a * c, 4)
            e = f"$x^2-y^2=(x+y)(x-y)$。$x+y=2\\sqrt{{{a}}}$，$x-y=2\\sqrt{{{c}}}$ なので $4\\sqrt{{{a * c}}}={tex(x)}$。"
            steps = ["$x^2-y^2=(x+y)(x-y)$ と因数分解する。", f"$x+y=2\\sqrt{{{a}}}$，$x-y=2\\sqrt{{{c}}}$。", f"$2\\sqrt{{{a}}}\\times2\\sqrt{{{c}}}=4\\sqrt{{{a * c}}}={tex(x)}$。"]
            expr = f"(sqrt({a})+sqrt({c}))**2-(sqrt({a})-sqrt({c}))**2"
        elif kind == "xy_diff":
            f_, x = "x^2+y^2", {1: Fr(2 * (a + c))}
            e = f"$x^2+y^2=(x+y)^2-2xy=(2\\sqrt{{{a}}})^2-2\\times{a - c}={tex(x)}$。"
            steps = [f"$x+y=2\\sqrt{{{a}}}$，$xy=(\\sqrt{{{a}}})^2-(\\sqrt{{{c}}})^2={a - c}$。", "$x^2+y^2=(x+y)^2-2xy$。", f"${4 * a}-{2 * (a - c)}={2 * (a + c)}$。"]
            expr = f"(sqrt({a})+sqrt({c}))**2+(sqrt({a})-sqrt({c}))**2"
        elif kind == "xy_prod":
            f_, x = "xy", {1: Fr(a - c)}
            e = f"$xy=(\\sqrt{{{a}}}+\\sqrt{{{c}}})(\\sqrt{{{a}}}-\\sqrt{{{c}}})={a}-{c}={a - c}$。"
            steps = ["和と差の積の公式 $(a+b)(a-b)=a^2-b^2$ を使う。", f"$(\\sqrt{{{a}}})^2-(\\sqrt{{{c}}})^2={a}-{c}$。", f"$={a - c}$。"]
            expr = f"(sqrt({a})+sqrt({c}))*(sqrt({a})-sqrt({c}))"
        else:
            f_, x = "x^2y+xy^2", R(a, 2 * (a - c))
            e = f"$x^2y+xy^2=xy(x+y)={a - c}\\times2\\sqrt{{{a}}}={tex(x)}$。"
            steps = ["$x^2y+xy^2=xy(x+y)$ と因数分解する。", f"$xy={a - c}$，$x+y=2\\sqrt{{{a}}}$。", f"${a - c}\\times2\\sqrt{{{a}}}={tex(x)}$。"]
            expr = f"(sqrt({a})+sqrt({c}))**2*(sqrt({a})-sqrt({c}))+(sqrt({a})+sqrt({c}))*(sqrt({a})-sqrt({c}))**2"
        stem = f"$x={xs}$，$y={ys}$ のとき，${f_}$ の値を求めなさい。"
    return MARK(stem, x, e, expr, d=3, p=4,
                ap="そのまま代入すると計算が長くなる。式を因数分解したり、$x+y$、$xy$ などの計算しやすい値を先に求めたりしてから代入する（式の展開と因数分解の単元とのつながり）。",
                steps=steps, alt=["そのまま代入して乗法公式で展開しても同じ値になる（計算量が多いので、確かめに使う）。"],
                pc=[("式を因数分解（変形）して計算しやすくしている", 2), ("正しい値", 2)],
                pit=["そのまま代入して展開し、符号や $2ab$ の項で誤る。", "$(\\sqrt{a})^2=a$ を $2a$ や $a^2$ とする。"])


@gen("standard_practice", 3, ["concept", "computation"])
def b_int_part(r):
    kind = r.choice(["root", "coef", "plus", "minus"])
    if kind == "root":
        n = r.choice([v for v in range(5, 200) if not is_sq(v)])
        ans = math.isqrt(n)
        ex, expr = f"\\sqrt{{{n}}}", f"floor(sqrt({n}))"
        steps = [f"${ans}^2={ans * ans}$，${ans + 1}^2={(ans + 1) ** 2}$。", f"${ans * ans}<{n}<{(ans + 1) ** 2}$ なので ${ans}<\\sqrt{{{n}}}<{ans + 1}$。"]
    elif kind == "coef":
        a, b = r.randint(2, 6), r.choice([2, 3, 5, 6, 7])
        n = a * a * b
        ans = math.isqrt(n)
        ex, expr = f"{a}\\sqrt{{{b}}}", f"floor({a}*sqrt({b}))"
        steps = [f"${a}\\sqrt{{{b}}}=\\sqrt{{{n}}}$ と表す。", f"${ans * ans}<{n}<{(ans + 1) ** 2}$ なので ${ans}<{a}\\sqrt{{{b}}}<{ans + 1}$。"]
    elif kind == "plus":
        n = r.choice([v for v in range(3, 90) if not is_sq(v)])
        c = r.randint(1, 6)
        k = math.isqrt(n)
        ans = k + c
        ex, expr = f"{c}+\\sqrt{{{n}}}", f"floor({c}+sqrt({n}))"
        steps = [f"${k}<\\sqrt{{{n}}}<{k + 1}$。", f"各辺に ${c}$ を加えて ${k + c}<{c}+\\sqrt{{{n}}}<{k + c + 1}$。"]
    else:
        n = r.choice([v for v in range(3, 90) if not is_sq(v)])
        k = math.isqrt(n)
        c = k + r.randint(1, 6)
        ans = c - k - 1
        ex, expr = f"{c}-\\sqrt{{{n}}}", f"floor({c}-sqrt({n}))"
        steps = [f"${k}<\\sqrt{{{n}}}<{k + 1}$。", f"各辺に $-1$ をかけると不等号の向きが変わる：$-{k + 1}<-\\sqrt{{{n}}}<-{k}$。", f"各辺に ${c}$ を加えて ${c - k - 1}<{c}-\\sqrt{{{n}}}<{c - k}$。"]
    return MARK(f"$a<{ex}<a+1$ をみたす整数 $a$ を求めなさい。", ans, "　".join(steps) + f" よって $a={ans}$。", expr, d=3, p=4,
                ap="$\\sqrt{n}$ をはさむ連続する2つの整数を、平方数 $k^2<n<(k+1)^2$ から見つける。",
                steps=steps + [f"$a={ans}$。"],
                alt=["$\\sqrt{2}\\fallingdotseq1.414$ などの近似値や電卓で値を確かめてもよい。"],
                pc=[("$\\sqrt{n}$ をはさむ整数を正しく見つけている", 2), ("式の形に合わせて $a$ を求めている", 2)],
                pit=["$c-\\sqrt{n}$ のとき、不等号の向きを変えずに計算する。", "$a\\sqrt{b}$ の形のまま $a$ を答えにする。"])


# ======================================================================
# C 思考力・記述応用
# ======================================================================

def _statements(r):
    k = r.randint(2, 9)
    m = r.choice([2, 3, 5, 6, 7])
    p, q = r.sample([2, 3, 5, 7], 2)
    d = r.randint(2, 9)
    e = r.choice([2, 3, 5, 6, 7, 8])
    return [
        (f"${k * k}$ の平方根は ${k}$ と $-{k}$ である。", True, f"${k}^2={k * k}$，$(-{k})^2={k * k}$ なので正しい。"),
        (f"$\\sqrt{{{k * k}}}=\\pm{k}$ である。", False, f"$\\sqrt{{{k * k}}}$ は正の方の平方根なので ${k}$。"),
        (f"$\\sqrt{{(-{k})^2}}=-{k}$ である。", False, f"$\\sqrt{{(-{k})^2}}=\\sqrt{{{k * k}}}={k}$。"),
        (f"$-{k * k}$ の平方根は $\\pm{k}$ である。", False, "負の数を2乗すると正の数になるので、2乗して負の数になる数はない。負の数の平方根はない。"),
        (f"$\\sqrt{{{p}}}+\\sqrt{{{q}}}=\\sqrt{{{p + q}}}$ である。", False, f"$\\sqrt{{{p}}}+\\sqrt{{{q}}}$ を2乗すると ${p + q}+2\\sqrt{{{p * q}}}$ となり ${p + q}$ にならない。"),
        (f"$\\sqrt{{{p}}}\\times\\sqrt{{{q}}}=\\sqrt{{{p * q}}}$ である。", True, f"$(\\sqrt{{{p}}}\\times\\sqrt{{{q}}})^2={p * q}$ で正の数なので正しい。"),
        (f"$\\sqrt{{0.{d * d:02d}}}$ は有理数である。" if d * d < 10 else f"$\\sqrt{{0.{d * d}}}$ は有理数である。", True, f"$\\sqrt{{0.{d * d:02d}}}=0.{d}$ で有理数。" if d * d < 10 else f"$\\sqrt{{0.{d * d}}}=0.{d}$ で有理数。"),
        (f"$\\sqrt{{0.{e}}}$ は有理数である。", False, f"$0.{e}=\\dfrac{{{e * 10}}}{{100}}$ で ${e * 10}$ は自然数の2乗ではないので、$\\sqrt{{0.{e}}}$ は無理数。"),
        (f"$\\dfrac{{{m * 2}}}{{\\sqrt{{{m}}}}}=2\\sqrt{{{m}}}$ である。", True, f"分母を有理化すると $\\dfrac{{{m * 2}\\sqrt{{{m}}}}}{{{m}}}=2\\sqrt{{{m}}}$。"),
        (f"${k}$ は $\\sqrt{{{k * k + 1}}}$ より大きい。", False, f"${k}=\\sqrt{{{k * k}}}$ で ${k * k}<{k * k + 1}$ なので ${k}$ の方が小さい。"),
        ("円周率 $\\pi$ は無理数である。", True, "円周率 $\\pi$ は分数で表すことのできない無理数である。"),
        ("$0$ の平方根は $0$ だけである。", True, "2乗して $0$ になる数は $0$ だけである。"),
        (f"${m}\\sqrt{{{m + 1 if m + 1 not in (4, 8) else m + 3}}}$ は根号の中ができるだけ小さい自然数になっている。" if sqf(m + 1 if m + 1 not in (4, 8) else m + 3)[0] == 1 else f"$\\sqrt{{{m * 4}}}$ は根号の中ができるだけ小さい自然数になっている。",
         sqf(m + 1 if m + 1 not in (4, 8) else m + 3)[0] == 1,
         "根号の中に自然数の2乗の因数がないので、これ以上簡単にならない。" if sqf(m + 1 if m + 1 not in (4, 8) else m + 3)[0] == 1 else f"$\\sqrt{{{m * 4}}}=2\\sqrt{{{m}}}$ と変形できる。"),
    ]


@gen("thinking_writing", 3, ["written_reasoning", "condition_check", "concept"])
def c_xy_judge(r):
    S = _statements(r)
    tx, ty = r.choice([True, False]), r.choice([True, False])
    x = r.choice([s for s in S if s[1] == tx])
    y = r.choice([s for s in S if s[1] == ty and s is not x])
    XY = ["X：正　Y：正", "X：正　Y：誤", "X：誤　Y：正", "X：誤　Y：誤"]
    ans = XY[(0 if tx else 2) + (0 if ty else 1)]
    why = {}
    for c in XY:
        if c == ans:
            continue
        cx, cy = c.startswith("X：正"), c.endswith("Y：正")
        rs = []
        if cx != tx:
            rs.append(f"X は{'正しい' if tx else '誤り'}。{x[2]}")
        if cy != ty:
            rs.append(f"Y は{'正しい' if ty else '誤り'}。{y[2]}")
        why[c] = (" ".join(rs), "平方根の性質の思いこみ")
    return mc("Kさんは，平方根について学んだことを次の X，Y のようにまとめた。X，Y の文の正誤の組み合わせとして最も適するものを，" + SEL4 + f"\nX　{x[0]}\nY　{y[0]}",
              [ans] + [c for c in XY if c != ans], f"X：{x[2]}　Y：{y[2]}", d=4, p=8, why=why,
              ap="それぞれの文を、平方根の定義（2乗すると $a$ になる数）、$\\sqrt{a}$ は正の数であること、有理数の定義に照らして確かめる。2乗して確かめる・具体的な数で反例を探すのが有効。",
              steps=[f"X：{x[2]}", f"Y：{y[2]}", f"よって {ans}。"],
              alt=["それぞれの数を2乗したり、近似値を電卓で求めたりして、文の内容が成り立つかを確かめる。"],
              pc=[("X の正誤を根拠をもって判断している", 4), ("Y の正誤を根拠をもって判断している", 4)],
              pit=["「平方根」と「$\\sqrt{\\ }$ のついた数」を混同する。", "根号がついていれば無理数だと思いこむ。"])


@gen("thinking_writing", 3, ["cross_unit", "computation"], rel=["JH-MATH-G3-U01"])
def c_decimal_part(r):
    n = r.choice([v for v in range(5, 120) if not is_sq(v) and sqf(v)[0] == 1])
    k = math.isqrt(n)
    kind = r.choice(["a", "a_c", "xy"])
    if kind == "a":
        f_ = f"a^2+{2 * k}a"
        x = {1: Fr(n - k * k)}
        e = f"$a=\\sqrt{{{n}}}-{k}$。$a^2+{2 * k}a=a(a+{2 * k})=(\\sqrt{{{n}}}-{k})(\\sqrt{{{n}}}+{k})={n}-{k * k}={n - k * k}$。"
        expr = f"(sqrt({n})-{k})**2+{2 * k}*(sqrt({n})-{k})"
        steps = [f"${k}<\\sqrt{{{n}}}<{k + 1}$ より，整数部分は ${k}$，小数部分 $a=\\sqrt{{{n}}}-{k}$。", f"$a^2+{2 * k}a=a(a+{2 * k})$ と因数分解する。", f"$a+{2 * k}=\\sqrt{{{n}}}+{k}$ なので $(\\sqrt{{{n}}}-{k})(\\sqrt{{{n}}}+{k})={n}-{k * k}={n - k * k}$。"]
        q = f"$\\sqrt{{{n}}}$ の小数部分を $a$ とするとき，${f_}$ の値を求めなさい。"
    elif kind == "a_c":
        c = r.randint(1, 9)
        f_ = f"a^2+{2 * k}a+{c}"
        x = {1: Fr(n - k * k + c)}
        e = f"$a^2+{2 * k}a+{c}=(a+{k})^2-{k * k}+{c}$。$a+{k}=\\sqrt{{{n}}}$ なので ${n}-{k * k}+{c}={n - k * k + c}$。"
        expr = f"(sqrt({n})-{k})**2+{2 * k}*(sqrt({n})-{k})+{c}"
        steps = [f"小数部分 $a=\\sqrt{{{n}}}-{k}$，つまり $a+{k}=\\sqrt{{{n}}}$。", f"$a^2+{2 * k}a+{c}=(a+{k})^2-{k * k}+{c}$ と変形する。", f"$(\\sqrt{{{n}}})^2-{k * k}+{c}={n - k * k + c}$。"]
        q = f"$\\sqrt{{{n}}}$ の小数部分を $a$ とするとき，${f_}$ の値を求めなさい。"
    else:
        f_ = "x(x+y)"
        x = R(n, k)
        e = f"$x={k}$，$y=\\sqrt{{{n}}}-{k}$。$x+y=\\sqrt{{{n}}}$ なので $x(x+y)={k}\\sqrt{{{n}}}$。"
        expr = f"{k}*({k}+sqrt({n})-{k})"
        steps = [f"${k}<\\sqrt{{{n}}}<{k + 1}$ より $x={k}$，$y=\\sqrt{{{n}}}-{k}$。", f"$x+y=\\sqrt{{{n}}}$。", f"$x(x+y)={k}\\sqrt{{{n}}}$。"]
        q = f"$\\sqrt{{{n}}}$ の整数部分を $x$，小数部分を $y$ とするとき，${f_}$ の値を求めなさい。"
    stem = (f"Kさんは「$\\sqrt{{{n}}}$ は整数部分と小数部分に分けられる。たとえば，${k}<\\sqrt{{{n}}}<{k + 1}$ だから，$\\sqrt{{{n}}}$ の整数部分は ${k}$ である。」と考えた。" + q)
    return MARK(stem, x, e, expr, d=4, p=8,
                ap="小数部分は「もとの数 − 整数部分」で表せる。小数そのものは求められないので、根号をふくむ式のまま、因数分解を利用して計算する（式の展開と因数分解の単元とのつながり）。",
                steps=steps, alt=["$a$ の式をそのまま代入して展開しても求められる。根号の項が打ち消し合うことを確かめよう。"],
                pc=[("整数部分を正しく求めている", 2), ("小数部分を根号を使って表している", 3), ("式を変形して正しい値を求めている", 3)],
                pit=["小数部分を $0.\\cdots$ と近似値で表して計算しようとする。", f"整数部分を ${k + 1}$ と誤る。"])


@gen("thinking_writing", 2, ["application", "computation"])
def c_squares(r):
    b = r.choice([2, 3, 5, 6, 7])
    kind = r.choice(["width", "perim", "three"])
    if kind == "three":
        p, q, s = r.sample([1, 2, 3, 4, 5], 3)
        areas = [p * p * b, q * q * b, s * s * b]
        x = {b: Fr(p + q + s)}
        stem = (f"面積がそれぞれ ${areas[0]}$ cm²，${areas[1]}$ cm²，${areas[2]}$ cm² の3つの正方形の紙を，すき間なく重ならないように，下の辺をそろえて横一列に並べた。"
                "並べた図形全体の横の長さは何 cm か求めなさい。")
        e = f"1辺はそれぞれ $\\sqrt{{{areas[0]}}}={tex(R(areas[0]))}$，$\\sqrt{{{areas[1]}}}={tex(R(areas[1]))}$，$\\sqrt{{{areas[2]}}}={tex(R(areas[2]))}$。合計 ${tex(x)}$ cm。"
        expr = f"sqrt({areas[0]})+sqrt({areas[1]})+sqrt({areas[2]})"
        steps = ["それぞれの正方形の1辺は、面積の正の平方根。", e.split("。")[0] + "。", f"横の長さは ${tex(x)}$ cm。"]
    else:
        p, q = r.sample([1, 2, 3, 4, 5, 6], 2)
        a1, a2 = p * p * b, q * q * b
        if kind == "width":
            x = {b: Fr(p + q)}
            stem = (f"面積が ${a1}$ cm² の正方形 A と，面積が ${a2}$ cm² の正方形 B の紙を，すき間なく重ならないように，下の辺をそろえて横に並べた。"
                    "並べた図形全体の横の長さは何 cm か求めなさい。")
            e = f"A の1辺 $\\sqrt{{{a1}}}={tex(R(a1))}$，B の1辺 $\\sqrt{{{a2}}}={tex(R(a2))}$。横の長さは ${tex(x)}$ cm。"
            expr = f"sqrt({a1})+sqrt({a2})"
            steps = ["正方形の1辺は面積の正の平方根。", e.split("。")[0] + "。", f"${tex(R(a1))}+{tex(R(a2))}={tex(x)}$。"]
        else:
            x = {b: Fr(2 * (p + q) + 2 * max(p, q))}
            stem = (f"面積が ${a1}$ cm² の正方形 A と，面積が ${a2}$ cm² の正方形 B の紙を，すき間なく重ならないように，下の辺をそろえて横に並べた。"
                    "並べてできた図形の周の長さは何 cm か求めなさい。")
            e = (f"A の1辺 ${tex(R(a1))}$，B の1辺 ${tex(R(a2))}$。周の長さは，横の長さの2倍と，高い方の正方形の1辺の2倍の和になり，"
                 f"$2({tex(R(a1))}+{tex(R(a2))})+2\\times{tex(R(max(a1, a2)))}={tex(x)}$ cm。")
            expr = f"2*(sqrt({a1})+sqrt({a2}))+2*sqrt({max(a1, a2)})"
            steps = [f"A の1辺 ${tex(R(a1))}$ cm，B の1辺 ${tex(R(a2))}$ cm。",
                     "横向きの辺の長さの合計は、上側・下側ともに A と B の1辺の和。縦向きの辺の長さの合計は、高い方の正方形の1辺の2倍になる。",
                     f"$2\\times{tex({b: Fr(p + q)})}+2\\times{tex(R(max(a1, a2)))}={tex(x)}$。"]
    return MARK(stem, x, e, expr, d=4, p=8,
                ap="正方形の1辺の長さは面積の正の平方根。$a\\sqrt{b}$ の形にそろえれば、長さをたし合わせられる。",
                steps=steps, alt=["近似値（$\\sqrt{2}\\fallingdotseq1.41$ など）で長さを求め、答えの近似値と比べて確かめる。"],
                pc=[("それぞれの1辺の長さを平方根で表している", 3), ("根号の中をそろえて計算している", 3), ("正しい答え", 2)],
                pit=["面積をそのまま足してから平方根をとる（$\\sqrt{a}+\\sqrt{b}=\\sqrt{a+b}$ としてしまう）。", "1辺を求めるとき $\\sqrt{\\ }$ の中を簡単にし忘れて、たし算ができない。"])


@gen("thinking_writing", 2, ["condition_check", "multiple_solutions"])
def c_n_count(r):
    kind = r.choice(["sub", "sub2", "two_digit", "div"])
    if kind == "sub":
        M = r.randint(20, 150)
        ans = math.isqrt(M - 1)
        stem = f"$\\sqrt{{{M}-n}}$ の値が自然数となるような自然数 $n$ は全部で何個あるか求めなさい。"
        lst = [M - k * k for k in range(1, ans + 1)]
        e = f"${M}-n$ が $1^2,\\ 2^2,\\ \\cdots,\\ {ans}^2$ のいずれかになればよい（${M}-n\\leqq{M - 1}$）。$n={', '.join(map(str, lst[:6]))}{',\\cdots' if len(lst) > 6 else ''}$ の ${ans}$ 個。"
        expr = f"floor(sqrt({M}-1))"
        steps = [f"$n\\geqq1$ なので $1\\leqq{M}-n\\leqq{M - 1}$。", f"この範囲の平方数は $1^2$ から ${ans}^2={ans * ans}$ まで。", f"それぞれに $n$ が1つずつ対応するので ${ans}$ 個。"]
    elif kind == "sub2":
        M = r.randint(15, 80)
        sqs = [k * k for k in range(0, 10) if k * k <= M - 2 and (M - k * k) % 2 == 0]
        ans = len(sqs)
        assert ans >= 1
        stem = f"$\\sqrt{{{M}-2n}}$ の値が整数となるような自然数 $n$ は全部で何個あるか求めなさい。"
        e = f"${M}-2n$ は ${M - 2}$ 以下で ${M}$ と偶奇が同じ平方数（$0$ をふくむ）：${', '.join(map(str, sqs))}$。$n$ は ${ans}$ 個。"
        expr = str(ans)
        steps = [f"$n\\geqq1$ なので ${M}-2n\\leqq{M - 2}$。また $\\sqrt{{0}}=0$ も整数なので $0$ もふくめる。", f"${M}-2n$ は ${M}$ から偶数をひいた数なので，${M}$ と偶奇が同じ。", f"あてはまる平方数は ${', '.join(map(str, sqs))}$ で ${ans}$ 個。"]
    elif kind == "two_digit":
        s = r.choice([2, 3, 5, 6, 7, 10, 11, 13])
        t = r.randint(1, 4)
        k = s * t * t
        ns = [s * j * j for j in range(1, 10) if 10 <= s * j * j <= 99]
        ans = len(ns)
        assert ans >= 1
        stem = f"$\\sqrt{{{k}n}}$ の値が自然数となるような2けたの自然数 $n$ は全部で何個あるか求めなさい。"
        e = f"${k}={t}^2\\times{s}$ なので，$n={s}\\times(\\text{{自然数}})^2$ の形。2けたのものは ${', '.join(map(str, ns))}$ の ${ans}$ 個。" if t > 1 else f"$n={s}\\times(\\text{{自然数}})^2$ の形。2けたのものは ${', '.join(map(str, ns))}$ の ${ans}$ 個。"
        expr = str(ans)
        steps = [f"${k}$ を素因数分解し，2乗の組にならない因数 ${s}$ を見つける。", f"$n={s}j^2$（$j$ は自然数）の形なら根号の中が自然数の2乗になる。", f"2けたのものは ${', '.join(map(str, ns))}$ の ${ans}$ 個。"]
    else:
        K = r.choice([v for v in range(24, 400) if sum(1 for t in range(1, 21) if v % (t * t) == 0) >= 2])
        ts = [t for t in range(1, 21) if K % (t * t) == 0]
        ans = len(ts)
        stem = f"$\\sqrt{{\\dfrac{{{K}}}{{n}}}}$ の値が自然数となるような自然数 $n$ は全部で何個あるか求めなさい。"
        ns = [K // (t * t) for t in ts]
        e = f"$\\dfrac{{{K}}}{{n}}=t^2$（$t$ は自然数）となればよい。$t^2$ は ${K}$ の約数で ${', '.join(str(t * t) for t in ts)}$，$n={', '.join(map(str, ns))}$ の ${ans}$ 個。"
        expr = str(ans)
        steps = [f"$\\sqrt{{\\dfrac{{{K}}}{{n}}}}=t$ とおくと $n=\\dfrac{{{K}}}{{t^2}}$。", f"$t^2$ が ${K}$ の約数になる $t$ は ${', '.join(map(str, ts))}$。", f"$n={', '.join(map(str, ns))}$ の ${ans}$ 個。"]
    return MARK(stem, ans, e, expr, d=4, p=8,
                ap="根号の中が「自然数（整数）の2乗」になる場合を、もれなく書き出す。範囲の端（$0$ をふくむか、$n$ が自然数か）に注意する。",
                steps=steps, alt=["条件をみたす $n$ を小さい順に表にして、根号の中の値と並べて書き出して数える。"],
                pc=[("根号の中が自然数の2乗になる条件を式で表している", 3), ("範囲の端を正しく扱っている", 3), ("正しい個数", 2)],
                pit=["$\\sqrt{0}=0$ を整数としてふくめるかどうかを確かめない。", "$n$ が自然数（$1$ 以上）であることを使わずに数えすぎる。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def _err_mc(stem, sol, right, cands, e, err, **kw):
    return MC(f"{stem}\n〔Kさんの解答〕\n{sol}\nKさんの解答の誤りを説明したものとして最も適するものを，" + SEL4, right, cands, e, err=err, **kw)


EXPL = {
    "add": "根号の中どうしをたしている。$\\sqrt{a}+\\sqrt{b}$ と $\\sqrt{a+b}$ は等しくない。",
    "out": "根号の外に出す数を、2乗のまま（平方根をとらずに）書いている。",
    "rat": "分母を有理化するとき、分子だけに根号をかけ、分母にかけていない。",
    "mulrad": "根号の中どうしをかけるべきところで、根号の中どうしをたしている。",
    "sq": "$(a+b)^2$ を展開するときに、まん中の項 $2ab$ を忘れている。",
    "like": "根号の中が異なる項の係数どうしと根号の中どうしをまとめている。根号の中が異なる項はまとめられない。",
}


def _err_case(r, kind):
    if kind == "add":
        b = r.choice([2, 3, 5])
        p, q = r.sample([1, 2, 3, 4], 2)
        A, B = p * p * b, q * q * b
        prob = f"$\\sqrt{{{A}}}+\\sqrt{{{B}}}$ を計算しなさい。"
        sol = f"$\\sqrt{{{A}}}+\\sqrt{{{B}}}=\\sqrt{{{A}+{B}}}=\\sqrt{{{A + B}}}$" + (f"$={tex(R(A + B))}$" if sqf(A + B)[0] > 1 else "")
        fix = f"${tex(R(A))}+{tex(R(B))}={tex({b: Fr(p + q)})}$"
        return prob, sol, fix, "根号の中どうしの加法", "formula", "乗法の $\\sqrt{a}\\sqrt{b}=\\sqrt{ab}$ と同じように、加法でもまとめられると思いこむ。", f"sqrt({A})+sqrt({B})", py({b: Fr(p + q)})
    if kind == "out":
        a, b = r.randint(2, 6), r.choice([2, 3, 5, 6, 7])
        n = a * a * b
        prob = f"$\\sqrt{{{n}}}$ を，根号の中ができるだけ小さい自然数になるように変形しなさい。"
        sol = f"$\\sqrt{{{n}}}=\\sqrt{{{a * a}\\times{b}}}={a * a}\\sqrt{{{b}}}$"
        fix = f"$\\sqrt{{{n}}}=\\sqrt{{{a}^2\\times{b}}}={a}\\sqrt{{{b}}}$"
        return prob, sol, fix, "根号の外に出す数", "calculation", f"${a * a}$ を根号の外に出すときに、${a * a}$ の平方根 ${a}$ にすることを忘れやすい。", f"sqrt({n})", f"{a}*sqrt({b})"
    if kind == "rat":
        b = r.choice([2, 3, 5, 6, 7])
        k = b * r.randint(2, 4)
        prob = f"$\\dfrac{{{k}}}{{\\sqrt{{{b}}}}}$ の分母を有理化しなさい。"
        sol = f"$\\dfrac{{{k}}}{{\\sqrt{{{b}}}}}={k}\\sqrt{{{b}}}$"
        fix = f"$\\dfrac{{{k}\\times\\sqrt{{{b}}}}}{{\\sqrt{{{b}}}\\times\\sqrt{{{b}}}}}=\\dfrac{{{k}\\sqrt{{{b}}}}}{{{b}}}={k // b}\\sqrt{{{b}}}$"
        return prob, sol, fix, "分母の有理化", "calculation", "「分母の根号を分子に移す」と覚えてしまい、分母と分子に同じ数をかける意味を忘れる。", f"{k}/sqrt({b})", f"{k // b}*sqrt({b})"
    if kind == "mulrad":
        a, c = r.randint(2, 5), r.randint(2, 5)
        b, d = r.choice([(2, 3), (2, 5), (3, 7), (2, 11), (3, 10)])
        prob = f"${a}\\sqrt{{{b}}}\\times{c}\\sqrt{{{d}}}$ を計算しなさい。"
        sol = f"${a}\\sqrt{{{b}}}\\times{c}\\sqrt{{{d}}}={a * c}\\sqrt{{{b + d}}}$"
        fix = f"$({a}\\times{c})\\sqrt{{{b}\\times{d}}}={a * c}\\sqrt{{{b * d}}}$"
        return prob, sol, fix, "根号の中どうしの乗法", "formula", "係数どうしはかけたので、根号の中も同じ計算でよいと思い、たし算と取り違える。", f"{a}*sqrt({b})*{c}*sqrt({d})", f"{a * c}*sqrt({b * d})"
    if kind == "sq":
        a, c = r.sample([2, 3, 5, 6, 7], 2)
        prob = f"$(\\sqrt{{{a}}}+\\sqrt{{{c}}})^2$ を計算しなさい。"
        sol = f"$(\\sqrt{{{a}}}+\\sqrt{{{c}}})^2=(\\sqrt{{{a}}})^2+(\\sqrt{{{c}}})^2={a + c}$"
        x = add({1: Fr(a + c)}, R(a * c, 2))
        fix = f"$(\\sqrt{{{a}}})^2+2\\sqrt{{{a}}}\\sqrt{{{c}}}+(\\sqrt{{{c}}})^2={tex(x)}$"
        return prob, sol, fix, "乗法公式の展開", "formula", "$(a+b)^2=a^2+b^2$ と思いこみ、まん中の項を落とす。", f"(sqrt({a})+sqrt({c}))**2", py(x)
    p, q = r.sample([2, 3, 4, 5], 2)
    b, d = r.choice([(2, 3), (2, 5), (3, 7), (2, 11), (3, 10), (5, 6)])
    prob = f"${p}\\sqrt{{{b}}}+{q}\\sqrt{{{d}}}$ を計算しなさい。"
    sol = f"${p}\\sqrt{{{b}}}+{q}\\sqrt{{{d}}}={p + q}\\sqrt{{{b + d}}}$"
    fix = f"根号の中が異なるので，${p}\\sqrt{{{b}}}+{q}\\sqrt{{{d}}}$ のままで，これ以上計算できない"
    return prob, sol, fix, "根号の中が異なる項の加法", "concept", "文字式の $2a+3a=5a$ のような計算を、根号の中が異なる項にも当てはめてしまう。", f"{p}*sqrt({b})+{q}*sqrt({d})", f"{p}*sqrt({b})+{q}*sqrt({d})"


@gen("error_correction", 4, ["common_error", "computation"])
def d_err_explain(r):
    kind = r.choice(list(EXPL))
    prob, sol, fix, step, etype, tempt, ex_py, ans_py = _err_case(r, kind)
    others = [k for k in EXPL if k != kind]
    r.shuffle(others)
    cands = [(EXPL[k], "Kさんの解答では、このような計算はしていない。", "誤りの箇所の見落とし") for k in others[:2]]
    cands.append(("Kさんの解答に誤りはない。", "答えを2乗したり近似値で確かめたりすると、もとの式の値と一致しない。", "検算不足"))
    return _err_mc(f"〔問題〕{prob}", sol, EXPL[kind], cands, f"正しくは {fix}。",
                   dict(sol=sol, step=step, type=etype, tempt=tempt, fix=fix), d=3, p=6,
                   ap="Kさんの式の両辺を近似値（$\\sqrt{2}\\fallingdotseq1.41$ など）で計算して、等しくなるかどうかを確かめると、誤りが見つかる。",
                   steps=[f"Kさんの解答の誤り：{EXPL[kind]}", f"正しい計算：{fix}。"],
                   alt=["乗法・除法は根号の中どうし、加法・減法は根号の中をそろえて係数どうし、というルールの違いを確かめる。"],
                   pc=[("誤りの箇所を正しく指摘している", 3), ("正しい計算をしている", 3)],
                   pit=["$\\sqrt{a}+\\sqrt{b}=\\sqrt{a+b}$ としてしまう。", "根号の外に出す数を2乗のまま書く。"],
                   chk=(ex_py, ans_py, None, "intermediate"))


@gen("error_correction", 3, ["common_error", "written_reasoning"])
def d_err_line(r):
    b = r.choice([2, 3, 5, 6, 7])
    while True:
        p, q, m = r.randint(2, 5), r.randint(2, 4), r.randint(1, 4)
        if p - m + q > 0 and p != q:
            break
    P, Q, K = p * p * b, q * q * b, m * b
    where = r.randint(0, 3)
    sb = f"\\sqrt{{{b}}}"
    co = lambda c: f"{'' if c == 1 else c}{sb}"  # noqa: E731
    # 正しい流れ
    pp, qq, mm = p, q, m
    l1 = f"$\\sqrt{{{P}}}={co(p)}$，$\\sqrt{{{Q}}}={co(q)}$"
    if where == 0:
        pp = p * p
        l1 = f"$\\sqrt{{{P}}}={co(p * p)}$，$\\sqrt{{{Q}}}={co(q)}$"
    l2 = f"$\\dfrac{{{K}}}{{\\sqrt{{{b}}}}}=\\dfrac{{{K}\\sqrt{{{b}}}}}{{{b}}}={co(m)}$"
    if where == 1:
        mm = K
        l2 = f"$\\dfrac{{{K}}}{{\\sqrt{{{b}}}}}={co(K)}$"
    l3 = f"（与式）$={co(pp)}-{co(mm)}+{co(qq)}$"
    sign_flip = False
    if where == 2:
        sign_flip = True
        l3 = f"（与式）$={co(pp)}+{co(mm)}+{co(qq)}$"
    tot = pp + mm + qq if sign_flip else pp - mm + qq
    if where == 3:
        tot = pp - mm + qq + r.choice([1, -1, 2])
        if tot == 0:
            tot = pp - mm + qq + 3
    l4 = f"$={tex({b: Fr(tot)})}$" if tot else "$=0$"
    sol = "\n".join(f"{i + 1}行目　{t}" for i, t in enumerate([l1, l2, l3, l4]))
    LINES4 = ["1行目", "2行目", "3行目", "4行目"]
    ok = {0: "1行目は、根号の中の2乗の因数を正しく外に出している。", 1: "2行目は、分母と分子に同じ根号をかけて正しく有理化している。",
          2: "3行目は、問題の式の符号のとおりに正しく並べている。", 3: "4行目は、3行目の係数を正しく計算している。"}
    why = {LINES4[i]: (ok[i], "誤りの箇所の見落とし") for i in range(4) if i != where}
    info = {0: ("1行目（根号の外に出す数）", "calculation", f"${p * p}$ の平方根をとって ${p}$ にすることを忘れやすい。"),
            1: ("2行目（分母の有理化）", "calculation", "分子にだけ根号をかけてしまう。"),
            2: ("3行目（項の符号）", "sign", "変形した項を書き写すときに、もとの式の「−」を落とす。"),
            3: ("4行目（係数の計算）", "calculation", "根号をふくむ項の係数どうしの計算でうっかりミスをする。")}[where]
    correct = {b: Fr(p - m + q)}
    fix = f"${co(p)}-{co(m)}+{co(q)}={tex(correct)}$"
    return mc(f"〔問題〕$\\sqrt{{{P}}}-\\dfrac{{{K}}}{{\\sqrt{{{b}}}}}+\\sqrt{{{Q}}}$ を計算しなさい。\n〔Kさんの解答〕\n{sol}\nKさんの解答で，誤りが最初に生じた行として最も適するものを，" + SEL4,
              LINES4, f"誤りが最初に生じたのは{LINES4[where]}。正しくは {fix}。", d=3, p=6, keep=True, ai=where, why=why,
              err=dict(sol=sol, step=info[0], type=info[1], tempt=info[2], fix=fix),
              ap="1行ずつ、自分で正しく計算した結果と比べる。$a\\sqrt{b}$ の変形は2乗して、有理化は分母をかけ直して確かめられる。",
              steps=[f"$\\sqrt{{{P}}}={co(p)}$，$\\sqrt{{{Q}}}={co(q)}$。", f"$\\dfrac{{{K}}}{{\\sqrt{{{b}}}}}={co(m)}$。", f"${co(p)}-{co(m)}+{co(q)}={tex(correct)}$。"],
              alt=[f"各行の式を近似値で計算し、もとの式の近似値と一致しなくなる最初の行を探す。"],
              pc=[("誤りの行を正しく指摘している", 3), ("正しい答えを求めている", 3)],
              pit=["根号の外に出す数を2乗のまま書く。", "有理化で分子だけに根号をかける。"],
              chk=(f"sqrt({P})-{K}/sqrt({b})+sqrt({Q})", py(correct), None, "intermediate"))


RT_EXPL = {
    "pos": "正の方の平方根だけを答えていて、負の方の平方根を落としている。",
    "neg_sq": "$\\sqrt{(-a)^2}$ は正の数 $a$ になるのに、負の数を答えている。",
    "neg_num": "負の数には平方根がないのに、平方根を答えている。",
    "dec": "小数の位取りを誤っている。答えを2乗してももとの数にならない。",
    "root_of_root": "$\\sqrt{\\ }$ の値を求めただけで、その数の平方根を求めていない。",
}


@gen("error_correction", 3, ["common_error", "condition_check"])
def d_err_root(r):
    kind = r.choice(list(RT_EXPL))
    k = r.randint(2, 9)
    if kind == "pos":
        prob, sol, fix = f"${k * k}$ の平方根を求めなさい。", f"$\\sqrt{{{k * k}}}={k}$ なので，答えは ${k}$", f"$\\pm{k}$"
        step, etype, tempt, cx = "平方根の個数", "concept", "「$\\sqrt{\\ }$ をつけた数」と「平方根」を同じものだと思いこむ。", (f"{k}**2", str(k * k))
    elif kind == "neg_sq":
        prob, sol, fix = f"$\\sqrt{{(-{k})^2}}$ を簡単にしなさい。", f"$\\sqrt{{(-{k})^2}}=-{k}$", f"$\\sqrt{{(-{k})^2}}=\\sqrt{{{k * k}}}={k}$"
        step, etype, tempt, cx = "根号の値の符号", "sign", "$\\sqrt{a^2}=a$ をそのまま $a=-" + str(k) + "$ に当てはめてしまう。", (f"sqrt((-{k})**2)", str(k))
    elif kind == "neg_num":
        prob, sol, fix = f"$-{k * k}$ の平方根を求めなさい。", f"${k}^2={k * k}$ なので，答えは $\\pm{k}$", "2乗して負の数になる数はないので，平方根はない"
        step, etype, tempt, cx = "平方根が存在する条件", "condition", "符号を無視して、絶対値の平方根を答えてしまう。", (f"(-{k})**2", str(k * k))
    elif kind == "dec":
        prob = f"$0.{k * k:02d}$ の平方根を求めなさい。" if k * k < 10 else f"$0.{k * k}$ の平方根を求めなさい。"
        num_s = f"0.{k * k:02d}" if k * k < 10 else f"0.{k * k}"
        sol, fix = f"答えは $\\pm0.0{k}$", f"$(0.{k})^2={num_s}$ なので $\\pm0.{k}$"
        step, etype, tempt, cx = "小数の位取り", "calculation", "整数の $\\sqrt{" + str(k * k) + "}=" + str(k) + "$ に小数点をそのままつけてしまう。", (f"Rational('0.{k}')**2", f"Rational('{num_s}')")
    else:
        m = r.randint(2, 4)
        prob = f"$\\sqrt{{{m ** 4}}}$ の平方根を求めなさい。"
        sol, fix = f"$\\sqrt{{{m ** 4}}}={m * m}$ なので，答えは $\\pm{m * m}$", f"$\\sqrt{{{m ** 4}}}={m * m}$ で，${m * m}$ の平方根は $\\pm{m}$"
        step, etype, tempt, cx = "何の平方根を求めるか", "interpretation", "問題文の「$\\sqrt{" + str(m ** 4) + "}$ の平方根」を「$" + str(m ** 4) + "$ の平方根」と読みかえてしまう。", (f"sqrt({m ** 4})", str(m * m))
    others = [x for x in RT_EXPL if x != kind]
    r.shuffle(others)
    cands = [(RT_EXPL[x], "Kさんの解答には、このような誤りはない。", "誤りの箇所の見落とし") for x in others[:2]]
    cands.append(("Kさんの解答に誤りはない。", "答えを2乗して、問題の数になるかを確かめると誤りがわかる。", "検算不足"))
    return _err_mc(f"〔問題〕{prob}", sol, RT_EXPL[kind], cands, f"正しくは {fix}。",
                   dict(sol=sol, step=step, type=etype, tempt=tempt, fix=fix), d=3, p=6,
                   ap="平方根の定義「2乗すると $a$ になる数」に戻り、Kさんの答えを2乗して確かめる。$\\sqrt{a}$ は正の数であることにも注意する。",
                   steps=[f"Kさんの解答の誤り：{RT_EXPL[kind]}", f"正しくは {fix}。"],
                   alt=["答えの候補を実際に2乗して、問題の数になるか、条件（正の数かどうか）をみたすかを確かめる。"],
                   pc=[("誤りの原因を正しく指摘している", 3), ("正しい答えを求めている", 3)],
                   pit=["平方根を1つしか答えない。", "$\\sqrt{(-a)^2}=-a$ とする。"],
                   chk=(cx[0], cx[1], None, "intermediate"))


GENERATORS = [a_root_meaning, a_simplify, a_mul_div, a_rationalize, a_compare, a_rational,
              b_add_sub, b_expand, b_count, b_square_n, b_value, b_int_part,
              c_xy_judge, c_decimal_part, c_squares, c_n_count,
              d_err_explain, d_err_line, d_err_root]

GENERATORS = [_robust(g) for g in GENERATORS]
