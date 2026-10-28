"""単元パック：中学2年 確率（神奈川県公立高校入試形式）。"""
import itertools
import math
import re
import unicodedata
from fractions import Fraction as Fr

from banks._common import figure, mc, num
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem, tp)

UNIT_ID = "JH-MATH-G2-U06"

PREREQUISITES = [
    ("JH-MATH-G1-U07", "多数回の試行で求めた相対度数を確率とみなす考え方（統計的確率）。この単元では、場合の数をもとに確率を求める。"),
    ("JH-MATH-G1-U01", "分数の計算と約分、倍数・約数・素数の判断。確率を既約分数で答えるときや、目の条件を調べるときに使う。"),
    ("JH-MATH-G1-U04", "座標の読み方。2つのさいころの目を点の座標とみなす問題で使う。"),
]
EXTENSIONS = [
    ("JH-MATH-G3-U08", "無作為に抽出するときの「どれも同様に確からしい」という考え方が、標本調査の土台になる。"),
    ("JH-MATH-G3-U04", "さいころの目で決まる点や直線と、関数のグラフを組み合わせた確率の問題に発展する。"),
    ("HS-MATHA-U01", "高校の場合の数と確率で、順列・組合せの公式や、和の法則・積の法則を使って確率を計算する。"),
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
        if t is None or _norm(t) in seen:
            continue
        seen.add(_norm(t))
        ws.append((t, why, mis))
        if len(ws) == k:
            break
    assert len(ws) == k, (stem, right, cands)
    return mc(stem, [right] + [w[0] for w in ws], e, why={w[0]: (w[1], w[2]) for w in ws}, **kw)


def MARK(stem, v, e, expr, **kw):
    """あいう方式（0〜9 のマーク）で答える数値問題。v は 0 以上の整数か既約分数。"""
    v = Fr(v)
    assert v >= 0
    if v.denominator == 1:
        n = int(v)
        return num(stem, str(n), e, mark=("int", n), chk=(expr, str(n), None, "answer"), **kw)
    p, q = v.numerator, v.denominator
    return num(stem, f"$\\dfrac{{{p}}}{{{q}}}$", e, mark=("frac", p, q), chk=(expr, f"Rational({p},{q})", None, "answer"), **kw)


def ft(v):
    """分数の LaTeX（$ なし）。"""
    v = Fr(v)
    if v.denominator == 1:
        return str(v.numerator)
    s = "-" if v < 0 else ""
    return f"{s}\\dfrac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def fd(c, t):
    """「c/t = 既約分数」の LaTeX。"""
    v = Fr(c, t)
    raw = f"\\dfrac{{{c}}}{{{t}}}"
    return raw if (v.numerator == c and v.denominator == t) else f"{raw}={ft(v)}"


SEL4 = "次の1〜4の中から1つ選び，その番号を答えなさい。"
SAME_DIE = "ただし，さいころの1から6までのどの目が出ることも同様に確からしいものとする。"
SAME_DICE = "ただし，大小2つのさいころはともに，1から6までのどの目が出ることも同様に確からしいものとする。"
SAME_COIN = "ただし，硬貨の表と裏の出方は同様に確からしいものとする。"
DICE = [(a, b) for a in range(1, 7) for b in range(1, 7)]
NAMES = "ABCDEF"


def pairs_txt(ps, lim=12):
    ps = list(ps)
    if len(ps) <= lim:
        return "，".join(f"$({a},\\,{b})$" for a, b in ps)
    return "，".join(f"$({a},\\,{b})$" for a, b in ps[:lim]) + " など"


def by_a(ps):
    """大きいさいころの目 a ごとの個数の内訳。"""
    cnt = {a: 0 for a in range(1, 7)}
    for a, _ in ps:
        cnt[a] += 1
    return "，".join(f"$a={a}$ のとき ${cnt[a]}$ 通り" for a in range(1, 7))


def robust(g):
    """選択肢が重複して誤答が足りないパラメータのときは、同じ乱数列から別のパラメータを引き直す。"""
    import random as _random
    fn = g.fn

    def wrapped(r):
        for _ in range(50):
            try:
                return fn(r)
            except AssertionError:
                r = _random.Random(r.random())
        return fn(r)
    wrapped.__name__ = fn.__name__
    g.fn = wrapped
    return g


# ----------------------------------------------------------------------
# 図（SVG）
# ----------------------------------------------------------------------

def coin_tree(n=3, heads=("A", "B", "C")):
    """n 枚の硬貨の樹形図。"""
    sp, dx = 20, 70
    leaves = 2 ** n
    H = leaves * sp + 30
    W = dx * n + 120
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="serif" font-size="12">']
    for L in range(n):
        o.append(f'<text x="{20 + dx * (L + 1)}" y="14" text-anchor="middle">{heads[L]}</text>')

    def y(L, i):
        return 24 + (i + 0.5) * (2 ** (n - L)) * sp
    for L in range(n):
        for i in range(2 ** L):
            px, py = 20 + dx * L + (8 if L else 0), y(L, i)
            for k in range(2):
                ci = 2 * i + k
                cx, cy = 20 + dx * (L + 1), y(L + 1, ci)
                o.append(f'<line x1="{px}" y1="{py:.1f}" x2="{cx - 9}" y2="{cy:.1f}" stroke="#000" stroke-width="0.9"/>')
                o.append(f'<text x="{cx}" y="{cy + 4:.1f}" text-anchor="middle">{"表" if k == 0 else "裏"}</text>')
    for i in range(leaves):
        bits = format(i, f"0{n}b")
        o.append(f'<text x="{20 + dx * n + 18}" y="{y(n, i) + 4:.1f}" font-size="11">（{"，".join("表" if b == "0" else "裏" for b in bits)}）</text>')
    o.append("</svg>")
    return "".join(o)


def dice_table(mark=lambda a, b: a + b == 7):
    """大小2つのさいころの目の和の表（条件を満たすマスに色）。"""
    c = 30
    W = H = c * 7 + 2
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="serif" font-size="12">']
    for a in range(1, 7):
        for b in range(1, 7):
            if mark(a, b):
                o.append(f'<rect x="{1 + c * b}" y="{1 + c * a}" width="{c}" height="{c}" fill="#d9d9d9"/>')
            o.append(f'<text x="{1 + c * b + c / 2}" y="{1 + c * a + c / 2 + 4}" text-anchor="middle">{a + b}</text>')
    for i in range(1, 7):
        o.append(f'<text x="{1 + c * i + c / 2}" y="{1 + c / 2 + 4}" text-anchor="middle">{i}</text>')
        o.append(f'<text x="{1 + c / 2}" y="{1 + c * i + c / 2 + 4}" text-anchor="middle">{i}</text>')
    o.append(f'<text x="{1 + c * 0.72}" y="{1 + c * 0.38}" text-anchor="middle" font-size="9">b</text>')
    o.append(f'<text x="{1 + c * 0.28}" y="{1 + c * 0.8}" text-anchor="middle" font-size="9">a</text>')
    o.append(f'<line x1="1" y1="1" x2="{1 + c}" y2="{1 + c}" stroke="#000" stroke-width="0.8"/>')
    for i in range(8):
        w = 1.4 if i in (0, 1, 7) else 0.8
        o.append(f'<line x1="{1 + c * i}" y1="1" x2="{1 + c * i}" y2="{1 + c * 7}" stroke="#000" stroke-width="{w}"/>')
        o.append(f'<line x1="1" y1="{1 + c * i}" x2="{1 + c * 7}" y2="{1 + c * i}" stroke="#000" stroke-width="{w}"/>')
    o.append("</svg>")
    return "".join(o)


# ----------------------------------------------------------------------
# 授業プリント
# ----------------------------------------------------------------------

LESSON = lesson(
    goals=["「同様に確からしい」の意味を理解し、起こりうる場合の数をもとに確率を求めることができる。",
           "樹形図や表を使って、もれや重なりなく場合の数を数えることができる。",
           "「〜でない確率」「少なくとも〜の確率」を、起こらない確率 $1-p$ を使って求め、その理由を説明できる。"],
    duration=100,
    readiness=["分数の約分ができる（確率は既約分数で答える）。",
               "倍数・約数・素数を判断できる。",
               "1年で学んだ「多数回の試行で、相対度数が一定の値に近づく」ことを知っている。"],
    flow=[("導入：どちらが起こりやすい？", 10, "2枚の硬貨で「表と裏が1枚ずつ」は 3 通りのうちの 1 つか、を考える"),
          ("確率の意味と求め方", 20, "同様に確からしい、確率 $p=\\dfrac{a}{n}$、確率の範囲 $0\\leqq p\\leqq 1$"),
          ("樹形図と場合の数", 20, "硬貨・並び方・代表の選び方を樹形図で数える（例題1）"),
          ("表を使う：2つのさいころ", 20, "36 通りの表で、和や差の条件を調べる（例題2）"),
          ("起こらない確率", 20, "$1-p$ の導出、「少なくとも」の確率（例題3）"),
          ("まとめと確認", 10, "確認問題と問題プリントの指示")],
    sections=[
        intro("in1", "「起こりやすさ」を数で表す",
              "1年では、ペットボトルのキャップを何回も投げて、表が出る割合（相対度数）を調べた。実験をしなくても、さいころや硬貨のように「どの結果が出ることも同じ程度に期待できる」ものなら、場合の数を数えるだけで起こりやすさを数で表すことができる。この単元では、その数（確率）の求め方と、もれなく数えるための道具（樹形図・表）を学ぶ。",
              bullets=["2枚の硬貨を投げると、「表・表」「表・裏」「裏・裏」の3通り……？", "硬貨に名前をつけて区別すると、本当は何通りあるかを考えよう。"],
              points=[tp("2枚の硬貨を実際に何十回も投げさせ、「表と裏が1枚ずつ」の割合が $\\dfrac{1}{3}$ ではなく $\\dfrac{1}{2}$ に近いことをクラス全体の結果で確かめる。",
                         ask="「表・表」「表・裏」「裏・裏」の3つは、同じくらい起こりやすいか。",
                         expect="「表・裏」は、10円玉が表で100円玉が裏の場合と、その逆の場合の2通りあるので起こりやすい。", timing="導入")]),
        definition("df1", "確率の意味と求め方",
                   "あることがらの起こることが期待される程度を表す数を、そのことがらの起こる確率という。どの結果が起こることも同じ程度に期待できるとき、それらは「同様に確からしい」という。",
                   formula="$$p=\\frac{a}{n}\\qquad\\left(\\frac{\\text{ことがら A の起こる場合の数}}{\\text{起こりうるすべての場合の数}}\\right)$$",
                   conditions=["起こりうるすべての場合が $n$ 通りあり、そのどれが起こることも同様に確からしいときに使える。",
                               "確率 $p$ の範囲は $0\\leqq p\\leqq 1$。必ず起こることがらの確率は 1、決して起こらないことがらの確率は 0。",
                               "確率 $\\dfrac{1}{6}$ は「6回に1回必ず起こる」という意味ではない。多数回くり返すと、起こる割合が $\\dfrac{1}{6}$ に近づくという意味である。"],
                   points=[tp("公式 $\\dfrac{a}{n}$ を使う前に「この $n$ 通りは同様に確からしいか」を必ず確かめる習慣をつけさせる。",
                              caution="2つのさいころの「和」の 2〜12 の 11 通りを同様に確からしいと考える誤りが非常に多い。")]),
        theorem("th1", "起こらない確率",
                "$$(\\text{A の起こらない確率})=1-(\\text{A の起こる確率})$$",
                ["起こりうるすべての場合が同様に確からしいとき、いつでも成り立つ。",
                 "「少なくとも1つは〜」の確率は、「1つも〜でない」確率を 1 から引くと求めやすい。"],
                proof=["起こりうるすべての場合の数を $n$、A の起こる場合の数を $a$ とする。",
                       "A の起こらない場合の数は $n-a$ である。",
                       "A の起こらない確率は $\\dfrac{n-a}{n}=\\dfrac{n}{n}-\\dfrac{a}{n}=1-\\dfrac{a}{n}$。",
                       "$\\dfrac{a}{n}=p$ なので、A の起こらない確率は $1-p$ である。"],
                points=[tp("「少なくとも1枚は表」を直接数える方法と、$1-$「すべて裏」で求める方法を両方やらせ、一致することを確かめさせる。",
                           ask="3枚の硬貨で「少なくとも1枚は表」となる場合を直接数えると何通りか。", expect="8 通りのうち、すべて裏の 1 通り以外なので 7 通り。")]),
        derivation("dv1", "場合の数の数え方（樹形図と積の考え）",
                   ["1枚目の硬貨の出方は表・裏の 2 通り。そのそれぞれについて、2枚目の出方も 2 通りある。",
                    "樹形図で枝分かれを順にかくと、2枚では $2\\times2=4$ 通り、3枚では $2\\times2\\times2=8$ 通りになる。",
                    "同じように、大小2つのさいころでは、大の6通りそれぞれに小の6通りがあるので $6\\times6=36$ 通り。",
                    "A，B，C の3人の並び方は、左はしが3通り、そのそれぞれで真ん中が2通り、右はしが1通りなので $3\\times2\\times1=6$ 通り。",
                    "4人から2人の代表を選ぶ（順番を考えない）ときは、「A と B」と「B と A」を同じものとみるので、並べた $4\\times3=12$ 通りを 2 でわって 6 通り。"],
                   points=[tp("樹形図は「どの順にかくか（1枚目→2枚目…）」を最初に決め、同じ形の枝が並ぶことに気づかせる。",
                              caution="代表の選び方で、AB と BA を別々に数えてしまう誤りが多い。順番を区別するかどうかを問題文から読み取らせる。")]),
        example("ex1", "例題1　樹形図を使う",
                "A，B，C の3枚の硬貨を同時に投げるとき，表が2枚，裏が1枚出る確率を求めなさい。",
                ["樹形図をかくと、表裏の出方は全部で $2\\times2\\times2=8$ 通りで、どれも同様に確からしい。",
                 "表が2枚・裏が1枚になるのは（表，表，裏）（表，裏，表）（裏，表，表）の 3 通り。",
                 "確率は $\\dfrac{3}{8}$。"],
                "$\\dfrac{3}{8}$",
                thinking="硬貨に A，B，C と名前をつけて区別し、樹形図で 8 通りをすべて書き出す。",
                figure=figure("3枚の硬貨 A，B，C の表裏の出方の樹形図", coin_tree(3)),
                points=[tp("「表の枚数は 0，1，2，3 の 4 通りだから $\\dfrac{1}{4}$」という誤答を取り上げ、なぜ誤りかを説明させる。")],
                misconceptions=[("表の枚数は 0〜3 枚の 4 通りなので $\\dfrac{1}{4}$", "4つの場合は同様に確からしくない。8 通りのうち 3 通りなので $\\dfrac{3}{8}$")]),
        example("ex2", "例題2　表を使う（2つのさいころ）",
                "大小2つのさいころを同時に投げるとき，出た目の数の和が7になる確率を求めなさい。",
                ["大きいさいころの目を $a$、小さいさいころの目を $b$ として、36 通りの表をかく。",
                 "和が7になるのは $(1,6),(2,5),(3,4),(4,3),(5,2),(6,1)$ の 6 通り（表の色のついたマス）。",
                 "確率は $\\dfrac{6}{36}=\\dfrac{1}{6}$。"],
                "$\\dfrac{1}{6}$",
                thinking="2つのさいころの問題では、縦に大、横に小の目をとった表をつくると、もれなく数えられる。",
                figure=figure("大小2つのさいころの目の和の表（和が7のマスに色）", dice_table()),
                points=[tp("表の右上から左下への斜めの並びが、和が等しいマスであることに気づかせる。", ask="和が 6 と 8 ではどちらが起こりやすいか。", expect="どちらも 5 通りで同じ。")]),
        example("ex3", "例題3　起こらない確率を使う",
                "赤玉3個と白玉2個が入った袋から，同時に2個の玉を取り出すとき，少なくとも1個は白玉である確率を求めなさい。",
                ["玉に 赤1，赤2，赤3，白1，白2 と番号をつけて区別する。取り出し方は全部で 10 通り。",
                 "「少なくとも1個は白玉」でないのは、2個とも赤玉のとき：$\\{赤1,赤2\\},\\{赤1,赤3\\},\\{赤2,赤3\\}$ の 3 通り。",
                 "2個とも赤玉である確率は $\\dfrac{3}{10}$。",
                 "求める確率は $1-\\dfrac{3}{10}=\\dfrac{7}{10}$。"],
                "$\\dfrac{7}{10}$",
                thinking="「少なくとも1個は白」は、白が1個の場合と2個の場合がある。反対の「2個とも赤」の方が数えやすい。",
                points=[tp("同じ色の玉にも番号をつけて区別する理由（区別しないと同様に確からしくならない）を確認する。", caution="同時に取り出すときは、{赤1，白1} と {白1，赤1} を同じものとして数える。")]),
        board("bd1", "板書案",
              [("① 確率の意味", ["同様に確からしい", "$p=\\dfrac{a}{n}$（$a$：A の場合の数）", "$0\\leqq p\\leqq 1$", "$\\dfrac16$ ＝ 多数回で割合が近づく"]),
               ("② 数え方", ["樹形図：硬貨 $2\\times2\\times2=8$", "表：さいころ2つ $6\\times6=36$", "同じ色の玉にも番号", "選ぶだけ（順番なし）は重なりに注意"]),
               ("③ 起こらない確率", ["(A でない)$=1-p$", "少なくとも1つ → $1-$(1つもない)", "直接数えて一致を確認", "答えは既約分数"])],
              points=[tp("②では、例題1の樹形図と例題2の表を並べてかき、「同様に確からしい場合をすべて並べる道具」としてまとめる。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("確率を求める答案には「全部で〇通り、そのうち〇通り」を必ず書かせる。入試のマーク式でも、途中の数え方が正確さを支える。"),
               tp("「同時に取り出す」「1個取り出してもどす」「もどさずに続けて取り出す」の違いを、同じ袋で比べさせる。",
                  ask="赤玉2個・白玉1個の袋から2個取り出すとき、もどす場合ともどさない場合で全部の場合の数はどう変わるか。",
                  expect="もどす場合は $3\\times3=9$ 通り、もどさない場合は $3\\times2=6$ 通り（同時なら 3 通り）。"),
               tp("入試の確率問題は「操作」のルールを読んで表をつくる形が多い。例をもとにルールを自分で1回たどらせてから数えさせる。", timing="例題2の後"),
               tp("くじ引きの順番による有利・不利がないことを、樹形図で確かめさせると「同様に確からしい」の理解が深まる。")],
              misconceptions=[("2つのさいころの和は 2〜12 の 11 通りなので、和が7の確率は $\\dfrac{1}{11}$", "和の11通りは同様に確からしくない。36 通りで考えて $\\dfrac{6}{36}=\\dfrac16$"),
                              ("確率が $\\dfrac16$ なら6回投げれば必ず1回出る", "確率は多数回くり返したときの割合の目安で、6回で必ず出るわけではない"),
                              ("「少なくとも1枚は表」は「1枚が表」の確率と同じ", "表が2枚以上の場合もふくむ。$1-$(すべて裏) で求める")]),
        summary("sm1", "まとめ",
                ["同様に確からしいとき、確率は $\\dfrac{\\text{A の起こる場合の数}}{\\text{すべての場合の数}}$。", "確率は $0$ 以上 $1$ 以下。",
                 "樹形図や表で、もれや重なりなく数える。同じ色の玉やカードも区別する。", "A の起こらない確率は $1-p$。「少なくとも」は起こらない方から考える。"]),
        check("ck1", "確認問題",
              [("1つのさいころを投げるとき，6の約数の目が出る確率を求めなさい。", "6の約数は 1，2，3，6 の 4 通りなので $\\dfrac{4}{6}=\\dfrac{2}{3}$"),
               ("2枚の硬貨を投げるとき，少なくとも1枚は裏が出る確率を求めなさい。", "$1-\\dfrac{1}{4}=\\dfrac{3}{4}$"),
               ("大小2つのさいころを投げるとき，同じ目が出る確率を求めなさい。", "36 通りのうち 6 通りなので $\\dfrac{1}{6}$")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

DIE_EV = [("偶数の目", lambda x: x % 2 == 0), ("奇数の目", lambda x: x % 2 == 1), ("3の倍数の目", lambda x: x % 3 == 0),
          ("4以上の目", lambda x: x >= 4), ("5以上の目", lambda x: x >= 5), ("2以下の目", lambda x: x <= 2),
          ("素数の目", lambda x: x in (2, 3, 5)), ("6の約数の目", lambda x: 6 % x == 0), ("4の約数の目", lambda x: 4 % x == 0),
          ("1でも6でもない目", lambda x: x not in (1, 6)), ("5の約数の目", lambda x: 5 % x == 0)]
COLORS = ["赤玉", "白玉", "青玉"]


@gen("basic_check", 6, ["computation"])
def a_single(r):
    kind = r.choice(["die", "card", "card", "bag"])
    if kind == "die":
        name, f = r.choice(DIE_EV)
        good = [x for x in range(1, 7) if f(x)]
        c, n = len(good), 6
        stem = f"1つのさいころを1回投げるとき，{name}が出る確率を求めなさい。{SAME_DIE}"
        lst = "，".join(map(str, good))
        st = ["起こりうる場合は 1〜6 の目の 6 通りで，どれも同様に確からしい。", f"{name}は ${lst}$ の ${c}$ 通り。", f"確率は ${fd(c, n)}$。"]
    elif kind == "card":
        n = r.randint(8, 20)
        ev = r.choice(["mul", "div", "ge", "le"])
        if ev == "mul":
            k = r.randint(2, 6)
            name, f = f"{k}の倍数", (lambda x, k=k: x % k == 0)
        elif ev == "div":
            m = r.choice([12, 18, 20, 24, 30, 36, 40])
            name, f = f"{m}の約数", (lambda x, m=m: m % x == 0)
        elif ev == "ge":
            t = r.randint(3, n - 1)
            name, f = f"{t}以上の数", (lambda x, t=t: x >= t)
        else:
            t = r.randint(2, n - 2)
            name, f = f"{t}より小さい数", (lambda x, t=t: x < t)
        good = [x for x in range(1, n + 1) if f(x)]
        c = len(good)
        assert 0 < c < n
        stem = f"1から{n}までの数字が1つずつ書かれた{n}枚のカードがある。このカードをよくきって1枚ひくとき，{name}が書かれたカードをひく確率を求めなさい。ただし，どのカードをひくことも同様に確からしいものとする。"
        lst = "，".join(map(str, good)) if c <= 10 else f"{good[0]}，{good[1]}，…，{good[-1]}"
        st = [f"カードのひき方は全部で ${n}$ 通りで，どれも同様に確からしい。", f"{name}は ${lst}$ の ${c}$ 枚。", f"確率は ${fd(c, n)}$。"]
    else:
        k = r.choice([2, 3])
        cnt = [r.randint(1, 7) for _ in range(k)]
        n = sum(cnt)
        i = r.randrange(k)
        neg = r.random() < 0.4
        c = n - cnt[i] if neg else cnt[i]
        bag = "と".join(f"{COLORS[j]}{cnt[j]}個" for j in range(k))
        name = f"{COLORS[i]}でない玉" if neg else COLORS[i]
        stem = f"袋の中に{bag}が入っている。この袋から玉を1個取り出すとき，{name}が出る確率を求めなさい。ただし，どの玉が取り出されることも同様に確からしいものとする。"
        st = [f"玉に番号をつけて区別すると，取り出し方は全部で ${n}$ 通り。", f"{name}の取り出し方は ${c}$ 通り。", f"確率は ${fd(c, n)}$。"]
    return MARK(stem, Fr(c, n), f"全部で ${n}$ 通り，そのうち ${c}$ 通りなので ${fd(c, n)}$。", f"Rational({c},{n})", d=1,
                ap="起こりうるすべての場合の数 $n$ と，ことがらが起こる場合の数 $a$ を数え，$\\dfrac{a}{n}$ を約分する。",
                steps=st,
                alt=[f"起こらない場合 ${n - c}$ 通りを数え，$1-\\dfrac{{{n - c}}}{{{n}}}={ft(Fr(c, n))}$ と確かめる。"],
                pc=[("すべての場合の数と，あてはまる場合の数を正しく数えている", 1), ("約分した確率を答えている", 1)],
                pit=["約分を忘れる。", "あてはまる数を数えもらす（境界の数を入れるかどうかに注意）。"])


COIN_SETS = {2: [("10円玉", 10), ("100円玉", 100)], 3: [("10円玉", 10), ("50円玉", 50), ("100円玉", 100)]}


@gen("basic_check", 5, ["computation", "concept"])
def a_coins(r):
    n = r.choice([2, 3, 3])
    coins = COIN_SETS[n]
    outs = list(itertools.product([1, 0], repeat=n))  # 1=表
    ev = r.choice(["exact", "exact", "atleast_h", "atleast_t", "spec", "money"])
    if ev == "exact":
        k = r.randint(0, n)
        name = {0: f"{n}枚とも裏", n: f"{n}枚とも表"}.get(k, f"表が{k}枚，裏が{n - k}枚")
        f = lambda o, k=k: sum(o) == k  # noqa: E731
    elif ev == "atleast_h":
        name, f = "少なくとも1枚は表", (lambda o: sum(o) >= 1)
    elif ev == "atleast_t":
        name, f = "少なくとも1枚は裏", (lambda o: sum(o) <= n - 1)
    elif ev == "spec":
        i, j = r.sample(range(n), 2)
        name = f"{coins[i][0]}が表で，{coins[j][0]}が裏"
        f = lambda o, i=i, j=j: o[i] == 1 and o[j] == 0  # noqa: E731
    else:
        tot = sorted({sum(v for (nm, v), b in zip(coins, o) if b) for o in outs})
        t = r.choice([x for x in tot if x > 0])
        name = f"表が出た硬貨の金額の合計が{t}円以上"
        f = lambda o, t=t: sum(v for (nm, v), b in zip(coins, o) if b) >= t  # noqa: E731
    good = [o for o in outs if f(o)]
    c, N = len(good), len(outs)
    assert 0 < c < N
    cn = "，".join(x[0] for x in coins)
    stem = f"{cn}の{n}枚の硬貨を同時に1回投げるとき，{name}になる確率を求めなさい。{SAME_COIN}"
    show = "，".join("（" + "，".join("表" if b else "裏" for b in o) + "）" for o in good)
    return MARK(stem, Fr(c, N), f"出方は全部で ${N}$ 通り，そのうち ${c}$ 通りなので ${fd(c, N)}$。", f"Rational({c},{N})", d=1,
                ap=f"硬貨を区別して樹形図をかくと，出方は $2^{n}={N}$ 通り。その中からあてはまるものを数える。",
                steps=[f"樹形図で（{cn}）の順に表裏を書くと，全部で ${N}$ 通り。", f"あてはまるのは {show} の ${c}$ 通り。", f"確率は ${fd(c, N)}$。"],
                alt=[f"あてはまらない ${N - c}$ 通りを数えて，$1-\\dfrac{{{N - c}}}{{{N}}}$ で確かめる。"],
                pc=[("樹形図などで出方を正しく数えている", 1), ("正しい確率を求めている", 1)],
                pit=["硬貨を区別せず，表の枚数だけで場合を数える。"])


@gen("basic_check", 5, ["computation"])
def a_count(r):
    kind = r.choice(["line", "pick2", "officer", "num2", "num3z", "menu", "dicesum"])
    if kind == "line":
        n = r.randint(3, 5)
        v = math.factorial(n)
        who = "，".join(NAMES[:n])
        stem = f"{who}の{n}人が横1列に並ぶとき，並び方は全部で何通りあるか，求めなさい。"
        st = [f"左はしは ${n}$ 通り，そのそれぞれについて次は ${n - 1}$ 通り，……と考える。", f"${'\\times'.join(str(i) for i in range(n, 0, -1))}={v}$ 通り。"]
        alt = ["A が左はしの場合の樹形図をかいて数え，その数を人数倍しても求められる。"]
        expr = f"factorial({n})"
    elif kind == "pick2":
        n = r.randint(4, 7)
        v = n * (n - 1) // 2
        who = "，".join(NAMES[:n]) if n <= 6 else f"7人"
        stem = f"{who}{'の' + str(n) + '人' if n <= 6 else ''}の中から2人の代表を選ぶとき，選び方は全部で何通りあるか，求めなさい。"
        st = [f"順番をつけて選ぶと ${n}\\times{n - 1}={n * (n - 1)}$ 通り。", f"代表は順番を区別しないので，同じ組が2回ずつ数えられている。${n * (n - 1)}\\div2={v}$ 通り。"]
        alt = ["樹形図で，A と組む相手，B と組む相手（A 以外）…と重ならないように数えても同じ。"]
        expr = f"{n}*{n - 1}/2"
    elif kind == "officer":
        n = r.randint(4, 7)
        v = n * (n - 1)
        stem = f"{n}人の中から，委員長と副委員長を1人ずつ選ぶとき，選び方は全部で何通りあるか，求めなさい。"
        st = [f"委員長の選び方は ${n}$ 通り。", f"そのそれぞれについて副委員長は残りの ${n - 1}$ 人から選ぶ。", f"${n}\\times{n - 1}={v}$ 通り。"]
        alt = ["委員長と副委員長は役割がちがうので，代表2人を選ぶ場合の2倍になることからも確かめられる。"]
        expr = f"{n}*{n - 1}"
    elif kind == "num2":
        n = r.randint(3, 6)
        cards = list(range(1, n + 1))
        even = r.random() < 0.5
        good = [(x, y) for x in cards for y in cards if x != y and (not even or y % 2 == 0)]
        v = len(good)
        lst = "，".join(map(str, cards))
        stem = f"{lst} の数字が1つずつ書かれた{n}枚のカードから2枚を続けて取り出し，1枚目を十の位，2枚目を一の位として2けたの整数をつくる。{'できる整数のうち，偶数' if even else 'できる2けたの整数'}は全部で何通りあるか，求めなさい。"
        if even:
            st = ["偶数になるのは，一の位が偶数のとき。", f"一の位の選び方は ${len([c for c in cards if c % 2 == 0])}$ 通り，そのそれぞれについて十の位は残りの ${n - 1}$ 通り。", f"${v}$ 通り。"]
        else:
            st = [f"十の位は ${n}$ 通り，一の位は残りの ${n - 1}$ 通り。", f"${n}\\times{n - 1}={v}$ 通り。"]
        alt = ["十の位ごとに樹形図をかいて書き出し，数えて確かめる。"]
        expr = str(v)
    elif kind == "num3z":
        k = r.randint(3, 5)
        cards = list(range(0, k))
        v = (k - 1) * (k - 1) * (k - 2)
        lst = "，".join(map(str, cards))
        stem = f"{lst} の数字が1つずつ書かれた{k}枚のカードから3枚を続けて取り出し，取り出した順に百の位，十の位，一の位として3けたの整数をつくる。百の位が0になるものは3けたの整数とはしないとき，できる3けたの整数は全部で何通りあるか，求めなさい。"
        st = [f"百の位には 0 が使えないので ${k - 1}$ 通り。", f"十の位は残りの ${k - 1}$ 通り（0 も使える），一の位は残りの ${k - 2}$ 通り。", f"${k - 1}\\times{k - 1}\\times{k - 2}={v}$ 通り。"]
        alt = [f"0 を百の位に置く場合もふくめた ${k}\\times{k - 1}\\times{k - 2}={k * (k - 1) * (k - 2)}$ 通りから，百の位が 0 の ${(k - 1) * (k - 2)}$ 通りを引いても求められる。"]
        expr = f"{k}*{k - 1}*{k - 2}-{k - 1}*{k - 2}"
    elif kind == "menu":
        m, d_, s = r.randint(2, 5), r.randint(2, 4), r.choice([0, 2, 3])
        v = m * d_ * (s if s else 1)
        extra = f"，デザートを{s}種類の中から1つ" if s else ""
        stem = f"ある店のランチでは，主食を{m}種類の中から1つ，飲み物を{d_}種類の中から1つ{extra}選ぶ。選び方は全部で何通りあるか，求めなさい。"
        st = [f"主食 ${m}$ 通りのそれぞれについて，飲み物が ${d_}$ 通りある。"] + ([f"さらにそれぞれにデザートが ${s}$ 通りある。"] if s else []) + [f"${v}$ 通り。"]
        alt = ["主食を1つ決めたときの樹形図をかき，枝の数を数えてから主食の種類の数だけかける。"]
        expr = f"{m}*{d_}*{s if s else 1}"
    else:
        s = r.randint(3, 11)
        good = [(a, b) for a, b in DICE if a + b == s]
        v = len(good)
        stem = f"大小2つのさいころを同時に1回投げるとき，出た目の数の和が{s}になる場合は全部で何通りあるか，求めなさい。"
        st = ["大きいさいころの目を $a$，小さいさいころの目を $b$ として表をつくる。", f"和が ${s}$ になるのは {pairs_txt(good)} の ${v}$ 通り。"]
        alt = ["表の斜めの並び（和が等しいマス）を数えて確かめる。"]
        expr = str(v)
    return MARK(stem, v, f"全部で ${v}$ 通り。", expr, d=1,
                ap="樹形図や表をかいて，もれや重なりがないように数える。「それぞれについて〇通り」ならかけ算が使える。",
                steps=st, alt=alt,
                pc=[("数え方（樹形図・表・かけ算）を正しく選んでいる", 1), ("正しい数を求めている", 1)],
                pit=["順番を区別しない選び方で，同じ組を2回数える。", "条件（0 を先頭に置けない，同じカードは使えない）を見落とす。"])


@gen("basic_check", 4, ["concept", "condition_check"])
def a_concept(r):
    kind = r.choice(["comp", "comp", "zero", "one", "meaning", "range"])
    if kind == "comp":
        q = r.randint(3, 13)
        p = r.choice([x for x in range(1, q) if math.gcd(x, q) == 1])
        X = r.choice("ABCD")
        right = f"$\\dfrac{{{q - p}}}{{{q}}}$"
        cands = [(f"$\\dfrac{{{p}}}{{{q}}}$", "これは起こる確率そのものである。", "起こる確率と起こらない確率の混同"),
                 (f"$\\dfrac{{{q + p}}}{{{q}}}$", "1 に加えている。確率は 1 をこえない。", "$1-p$ を $1+p$ とする誤り"),
                 (f"$\\dfrac{{{q}}}{{{p}}}$" if p > 1 else f"${q}$", "逆数にしている。確率は 1 をこえない。", "逆数との混同"),
                 (f"$\\dfrac{{{q - p}}}{{{p}}}$" if q - p != p and p > 1 else None, "分母が起こる場合の数になっている。分母はすべての場合の数。", "分母の取り違え")]
        stem = f"ことがら{X}の起こる確率が $\\dfrac{{{p}}}{{{q}}}$ であるとき，ことがら{X}の起こらない確率として正しいものを，" + SEL4
        e = f"起こらない確率は $1-\\dfrac{{{p}}}{{{q}}}=\\dfrac{{{q - p}}}{{{q}}}$。"
        st = ["(起こらない確率)$=1-$(起こる確率)。", e]
        ch = (f"1-Rational({p},{q})", f"Rational({q - p},{q})")
    elif kind in ("zero", "one"):
        t0 = r.randint(7, 9)
        k = r.randint(2, 5)
        zero = [f"{t0}以上の目が出る", f"{t0}の目が出る", "0の目が出る", "7の倍数の目が出る"]
        one = ["6以下の目が出る", "1以上の目が出る", f"{t0}より小さい目が出る", "6の目か6以外の目が出る"]
        mid = [(f"{k}以上の目が出る", f"確率は $\\dfrac{{{7 - k}}}{{6}}$ で，0 でも 1 でもない。"),
               ("偶数の目が出る", "確率は $\\dfrac{1}{2}$ である。"),
               (f"{k}の約数の目が出る", "確率は 0 でも 1 でもない。"),
               ("6の目が出る", "確率は $\\dfrac{1}{6}$ である。"),
               ("素数の目が出る", "2，3，5 の 3 通りなので確率は $\\dfrac{1}{2}$ である。")]
        r.shuffle(mid)
        if kind == "zero":
            right = r.choice(zero)
            other = (r.choice(one), "必ず起こることがらで，確率は 1 である。", "確率 0 と 1 の取り違え")
            stem = "1つのさいころを1回投げるとき，起こる確率が 0 であることがらとして最も適するものを，" + SEL4
            e = f"「{right}」ことは決して起こらないので，確率は 0。"
        else:
            right = r.choice(one)
            other = (r.choice(zero), "決して起こらないことがらで，確率は 0 である。", "確率 0 と 1 の取り違え")
            stem = "1つのさいころを1回投げるとき，起こる確率が 1 であることがらとして最も適するものを，" + SEL4
            e = f"「{right}」ことは必ず起こるので，確率は 1。"
        cands = [other] + [(m, w, "確率の値の判断の誤り") for m, w in mid]
        st = ["さいころの目は 1〜6 のどれかである。", "決して起こらないことがらの確率は 0，必ず起こることがらの確率は 1。", e]
        ch = None
    elif kind == "meaning":
        f = r.randint(1, 6)
        k = r.randint(2, 9)
        right = f"何回も投げ続けると，{f}の目が出る割合は $\\dfrac{{1}}{{6}}$ に近づいていく。"
        cands = [(f"6回投げると，{f}の目は必ず1回出る。", "6回投げても1回も出ないことも，2回以上出ることもある。", "確率を「必ずそうなる回数」と考える誤解"),
                 (f"${6 * k}$ 回投げると，{f}の目はちょうど ${k}$ 回出る。", "多数回でも，ちょうど $\\dfrac{1}{6}$ の回数になるとは限らない。割合がその値に近づくだけである。", "確率を「必ずそうなる回数」と考える誤解"),
                 (f"5回続けて{f}以外の目が出たら，次は必ず{f}の目が出る。", "さいころは前の結果を覚えていない。次に出る確率も $\\dfrac{1}{6}$ のままである。", "前の結果に影響されるという誤解"),
                 (f"{f}の目は，6回に1回ずつ規則正しく出る。", "目の出方には規則はない。", "確率を規則と考える誤解")]
        stem = f"1つのさいころを投げるとき，{f}の目が出る確率は $\\dfrac{{1}}{{6}}$ である。このことの意味を説明したものとして最も適するものを，" + SEL4
        e = "確率は，多数回の試行で起こる割合がその値に近づくことを表している。"
        st = ["確率は起こりやすさの程度を表す数である。", "少ない回数では，起こる割合は確率からずれることがある。", e]
        ch = None
    else:
        X = r.choice("ABCDE")
        right = "$0\\leqq p\\leqq 1$"
        cands = [("$0<p<1$", "必ず起こることがらは $p=1$，決して起こらないことがらは $p=0$ になるので，等号が必要。", "確率 0，1 の見落とし"),
                 ("$-1\\leqq p\\leqq 1$", "場合の数は 0 以上なので，確率が負になることはない。", "確率が負になるという誤解"),
                 ("$0\\leqq p\\leqq 100$", "百分率と混同している。確率は 1 をこえない。", "百分率との混同"),
                 ("$p\\geqq 0$", "上限がない。あてはまる場合の数はすべての場合の数をこえないので $p\\leqq 1$。", "上限の見落とし")]
        stem = f"ことがら{X}の起こる確率を $p$ とするとき，$p$ のとりうる値の範囲として正しいものを，" + SEL4
        e = "あてはまる場合の数 $a$ は $0\\leqq a\\leqq n$ なので，$0\\leqq \\dfrac{a}{n}\\leqq 1$。"
        st = ["$p=\\dfrac{a}{n}$ で，$a$ は 0 以上 $n$ 以下。", e]
        ch = None
    kw = dict(chk=ch + (None, "answer")) if ch else {}
    return MC(stem, right, cands, e, d=1,
              ap="確率の意味（$0\\leqq p\\leqq 1$，起こらない確率は $1-p$，多数回での割合）にもどって判断する。",
              steps=st,
              alt=["具体的な例（さいころ・硬貨）を思いうかべ，選択肢の内容が成り立つか確かめる。"],
              pc=[("確率の性質を正しく理解している", 1), ("正しいものを選んでいる", 1)],
              pit=["起こる確率と起こらない確率を取り違える。", "確率を「必ずその回数だけ起こる」と考える。"], **kw)


# ======================================================================
# B 標準演習
# ======================================================================

def dice_event(r):
    kind = r.choice(["sum", "sumle", "sumge", "summul", "prododd", "prodmul", "prodle", "gt", "eq", "div", "diff", "diffge", "sumprime"])
    if kind == "sum":
        s = r.randint(2, 12)
        return f"出た目の数の和が{s}になる", lambda a, b: a + b == s
    if kind == "sumle":
        s = r.randint(3, 11)
        return f"出た目の数の和が{s}以下になる", lambda a, b: a + b <= s
    if kind == "sumge":
        s = r.randint(4, 11)
        return f"出た目の数の和が{s}以上になる", lambda a, b: a + b >= s
    if kind == "summul":
        k = r.choice([3, 4, 5, 6])
        return f"出た目の数の和が{k}の倍数になる", lambda a, b: (a + b) % k == 0
    if kind == "prododd":
        return r.choice([("出た目の数の積が奇数になる", lambda a, b: a * b % 2 == 1), ("出た目の数の積が偶数になる", lambda a, b: a * b % 2 == 0)])
    if kind == "prodmul":
        k = r.choice([3, 4, 5, 6, 12])
        return f"出た目の数の積が{k}の倍数になる", lambda a, b: a * b % k == 0
    if kind == "prodle":
        m = r.randint(4, 20)
        return f"出た目の数の積が{m}以下になる", lambda a, b: a * b <= m
    if kind == "gt":
        return "$a$ が $b$ より大きくなる", lambda a, b: a > b
    if kind == "eq":
        return "$a$ と $b$ が等しくなる", lambda a, b: a == b
    if kind == "div":
        return r.choice([("$a$ が $b$ の倍数になる", lambda a, b: a % b == 0), ("$a$ が $b$ の約数になる", lambda a, b: b % a == 0)])
    if kind == "diff":
        k = r.randint(1, 5)
        return f"$a$ と $b$ の差が{k}になる", lambda a, b: abs(a - b) == k
    if kind == "diffge":
        k = r.randint(2, 4)
        return f"$a$ と $b$ の差が{k}以上になる", lambda a, b: abs(a - b) >= k
    return "出た目の数の和が素数になる", lambda a, b: a + b in (2, 3, 5, 7, 11)


@gen("standard_practice", 6, ["computation", "application"])
def b_two_dice(r):
    name, f = dice_event(r)
    good = [(a, b) for a, b in DICE if f(a, b)]
    c = len(good)
    assert 0 < c < 36
    stem = f"大小2つのさいころを同時に1回投げ，大きいさいころの出た目の数を $a$，小さいさいころの出た目の数を $b$ とする。このとき，{name}確率を求めなさい。{SAME_DICE}"
    return MARK(stem, Fr(c, 36), f"36 通りのうち ${c}$ 通りなので ${fd(c, 36)}$。", f"Rational({c},36)", d=2, p=4,
                ap="大小2つのさいころの目の出方は $6\\times6=36$ 通りで，どれも同様に確からしい。縦に $a$，横に $b$ の表をつくって数える。",
                steps=["目の出方は全部で 36 通り。", f"条件にあてはまる $(a,\\,b)$ は {pairs_txt(good)}（{by_a(good)}）の ${c}$ 通り。", f"確率は ${fd(c, 36)}$。"],
                alt=[f"あてはまらない場合 ${36 - c}$ 通りを数え，$1-\\dfrac{{{36 - c}}}{{36}}$ で確かめる。"],
                pc=[("36 通りの表などで正しく数えている", 2), ("約分した正しい確率", 2)],
                pit=["$(1,\\,2)$ と $(2,\\,1)$ を同じものとして数える。", "和の値（2〜12）を同様に確からしいと考える。"])


def _ball_setup(r):
    rd, wh = r.randint(2, 4), r.randint(1, 3)
    bl = r.choice([0, 0, 1, 2])
    balls = ["赤"] * rd + ["白"] * wh + ["青"] * bl
    txt = f"赤玉{rd}個，白玉{wh}個" + (f"，青玉{bl}個" if bl else "")
    return balls, txt, rd, wh, bl


@gen("standard_practice", 5, ["computation", "condition_check"])
def b_balls(r):
    balls, txt, rd, wh, bl = _ball_setup(r)
    n = len(balls)
    mode = r.choice(["sim", "sim", "rep", "norep"])
    idx = range(n)
    if mode == "sim":
        outs = [(i, j) for i, j in itertools.combinations(idx, 2)]
        how = "同時に2個の玉を取り出す"
    elif mode == "rep":
        outs = [(i, j) for i in idx for j in idx]
        how = "玉を1個取り出して色を調べてから袋にもどし，よくかき混ぜてもう1個取り出す"
    else:
        outs = [(i, j) for i in idx for j in idx if i != j]
        how = "玉を1個取り出し，それを袋にもどさずに続けてもう1個取り出す"
    evs = [("2個とも赤玉である", lambda x, y: x == y == "赤"),
           ("2個とも白玉である", lambda x, y: x == y == "白"),
           ("2個が同じ色である", lambda x, y: x == y),
           ("2個の色が異なる", lambda x, y: x != y),
           ("少なくとも1個は白玉である", lambda x, y: "白" in (x, y)),
           ("赤玉がちょうど1個である", lambda x, y: (x == "赤") != (y == "赤"))]
    if mode != "sim":
        evs.append(("1回目に赤玉，2回目に白玉が出る", lambda x, y: x == "赤" and y == "白"))
    r.shuffle(evs)
    for name, f in evs:
        good = [o for o in outs if f(balls[o[0]], balls[o[1]])]
        if 0 < len(good) < len(outs):
            break
    c, N = len(good), len(outs)
    assert 0 < c < N
    label = []
    cnt = {}
    for b in balls:
        cnt[b] = cnt.get(b, 0) + 1
        label.append(f"{b}{cnt[b]}")
    tot_txt = {"sim": f"番号をつけた ${n}$ 個から2個を選ぶ組は ${N}$ 通り（同じ組を2回数えない）",
               "rep": f"1回目 ${n}$ 通り，2回目も ${n}$ 通りで ${n}\\times{n}={N}$ 通り",
               "norep": f"1回目 ${n}$ 通り，2回目は残りの ${n - 1}$ 通りで ${n}\\times{n - 1}={N}$ 通り"}[mode]
    ex = "，".join(("{" if mode == "sim" else "（") + f"{label[i]}，{label[j]}" + ("}" if mode == "sim" else "）") for i, j in good[:8]) + (" など" if c > 8 else "")
    stem = f"袋の中に{txt}が入っている。この袋から{how}とき，{name}確率を求めなさい。ただし，どの玉が取り出されることも同様に確からしいものとする。"
    return MARK(stem, Fr(c, N), f"全部で ${N}$ 通り，そのうち ${c}$ 通りなので ${fd(c, N)}$。", f"Rational({c},{N})", d=3, p=4,
                ap="同じ色の玉にも番号をつけて区別する。「同時に」「もどす」「もどさない」で，すべての場合の数が変わることに注意する。",
                steps=[f"玉を {'，'.join(label)} と区別する。", f"取り出し方は，{tot_txt}。", f"あてはまるのは {ex} の ${c}$ 通り。", f"確率は ${fd(c, N)}$。"],
                alt=[f"あてはまらない場合 ${N - c}$ 通りを数えて $1-\\dfrac{{{N - c}}}{{{N}}}$ としても同じ結果になる。"],
                pc=[("すべての場合の数を取り出し方に合わせて正しく数えている", 2), ("正しい確率を求めている", 2)],
                pit=["同じ色の玉を区別せずに数える。", "もどす場合ともどさない場合の区別を見落とす。"])


@gen("standard_practice", 5, ["computation", "application"])
def b_cards(r):
    if r.random() < 0.5:
        n = r.randint(4, 6)
        cards = list(range(1, n + 1))
    else:
        cards = sorted(r.sample(range(1, 10), r.randint(4, 5)))
    lst = "，".join(map(str, cards))
    mode = r.choice(["num", "num", "pair"])
    if mode == "num":
        outs = [(x, y) for x in cards for y in cards if x != y]
        nums = sorted(10 * x + y for x, y in outs)
        T = r.choice(nums[2:-2])
        evs = [("偶数", lambda x, y: y % 2 == 0), ("奇数", lambda x, y: y % 2 == 1), ("3の倍数", lambda x, y: (10 * x + y) % 3 == 0),
               ("4の倍数", lambda x, y: (10 * x + y) % 4 == 0), (f"{T}以上", lambda x, y: 10 * x + y >= T),
               ("十の位の数が一の位の数より大きい数", lambda x, y: x > y), ("素数", lambda x, y: all((10 * x + y) % d for d in range(2, 10)))]
        head = f"{lst} の数字が1つずつ書かれた{len(cards)}枚のカードがある。このカードをよくきってから2枚を続けて取り出し，1枚目のカードの数字を十の位，2枚目のカードの数字を一の位として2けたの整数をつくる。"
        tail = "になる確率を求めなさい。"
        fmt = lambda o: str(10 * o[0] + o[1])  # noqa: E731
        totx = f"${len(cards)}\\times{len(cards) - 1}={len(outs)}$ 通り"
    else:
        outs = list(itertools.combinations(cards, 2))
        s0 = sorted({x + y for x, y in outs})
        t = r.choice(s0[1:-1]) if len(s0) > 2 else s0[0]
        evs = [("取り出した2枚のカードの数の和が偶数", lambda x, y: (x + y) % 2 == 0), ("取り出した2枚のカードの数の和が奇数", lambda x, y: (x + y) % 2 == 1),
               (f"取り出した2枚のカードの数の和が{t}以上", lambda x, y: x + y >= t), ("取り出した2枚のカードの数の積が偶数", lambda x, y: x * y % 2 == 0),
               ("取り出した2枚のカードの数の積が3の倍数", lambda x, y: x * y % 3 == 0)]
        head = f"{lst} の数字が1つずつ書かれた{len(cards)}枚のカードがある。このカードをよくきってから同時に2枚を取り出す。"
        tail = "になる確率を求めなさい。"
        fmt = lambda o: f"\\{{{o[0]},{o[1]}\\}}"  # noqa: E731
        totx = f"${len(cards)}\\times{len(cards) - 1}\\div2={len(outs)}$ 通り"
    r.shuffle(evs)
    for name, f in evs:
        good = [o for o in outs if f(*o)]
        if 0 < len(good) < len(outs):
            break
    c, N = len(good), len(outs)
    assert 0 < c < N
    stem = head + ("できた整数が" if mode == "num" else "") + name + tail + "ただし，どのカードが取り出されることも同様に確からしいものとする。"
    ex = "，".join(f"${fmt(o)}$" for o in good[:12]) + (" など" if c > 12 else "")
    return MARK(stem, Fr(c, N), f"全部で ${N}$ 通り，そのうち ${c}$ 通りなので ${fd(c, N)}$。", f"Rational({c},{N})", d=3, p=4,
                ap="カードの取り出し方を樹形図で書き出す。順番を考える（2けたの整数）か，考えない（同時に2枚）かで，すべての場合の数が変わる。",
                steps=[f"取り出し方は全部で {totx}。", f"あてはまるのは {ex} の ${c}$ 通り。", f"確率は ${fd(c, N)}$。"],
                alt=["十の位（または小さい方のカード）ごとに場合を分けて数え，合計して確かめる。"],
                pc=[("すべての場合の数を正しく求めている", 2), ("あてはまる場合を正しく数え，確率を求めている", 2)],
                pit=["同時に取り出すのに，順番を区別して数える（またはその逆）。", "同じカードを2回使う場合まで数える。"])


@gen("standard_practice", 4, ["computation", "concept"])
def b_people(r):
    kind = r.choice(["rep", "rep", "officer", "line", "janken"])
    if kind == "rep":
        n = r.randint(4, 6)
        P = NAMES[:n]
        outs = list(itertools.combinations(P, 2))
        name, f = r.choice([("A が選ばれる", lambda s: "A" in s), ("A と B がともに選ばれる", lambda s: "A" in s and "B" in s),
                            ("A と B の少なくとも一方が選ばれる", lambda s: "A" in s or "B" in s), ("A も B も選ばれない", lambda s: "A" not in s and "B" not in s)])
        stem = f"{'，'.join(P)} の{n}人の中から，くじびきで2人の代表を選ぶとき，{name}確率を求めなさい。ただし，どの2人が選ばれることも同様に確からしいものとする。"
        fmt = lambda s: "{" + "，".join(s) + "}"  # noqa: E731
        tot = f"2人の組は ${n}\\times{n - 1}\\div2={len(outs)}$ 通り"
    elif kind == "officer":
        n = r.randint(4, 6)
        P = NAMES[:n]
        outs = list(itertools.permutations(P, 2))
        name, f = r.choice([("A が委員長，B が副委員長に選ばれる", lambda s: s == ("A", "B")), ("A が委員長か副委員長のどちらかに選ばれる", lambda s: "A" in s),
                            ("A も B も選ばれない", lambda s: "A" not in s and "B" not in s), ("A が委員長に選ばれる", lambda s: s[0] == "A")])
        stem = f"{'，'.join(P)} の{n}人の中から，くじびきで委員長と副委員長を1人ずつ選ぶとき，{name}確率を求めなさい。ただし，どの選ばれ方も同様に確からしいものとする。"
        fmt = lambda s: f"（委員長 {s[0]}，副委員長 {s[1]}）"  # noqa: E731
        tot = f"選び方は ${n}\\times{n - 1}={len(outs)}$ 通り"
    elif kind == "line":
        n = r.randint(3, 4)
        P = NAMES[:n]
        outs = list(itertools.permutations(P))
        name, f = r.choice([("A が左はしに並ぶ", lambda s: s[0] == "A"), ("A と B がとなり合う", lambda s: abs(s.index("A") - s.index("B")) == 1),
                            ("A が B より左に並ぶ", lambda s: s.index("A") < s.index("B")), ("A が両はしのどちらかに並ぶ", lambda s: s[0] == "A" or s[-1] == "A")])
        stem = f"{'，'.join(P)} の{n}人が，くじびきで順番を決めて横1列に並ぶとき，{name}確率を求めなさい。ただし，どの並び方も同様に確からしいものとする。"
        fmt = lambda s: "".join(s)  # noqa: E731
        tot = f"並び方は ${'\\times'.join(str(i) for i in range(n, 0, -1))}={len(outs)}$ 通り"
    else:
        n = r.choice([2, 3, 3])
        P = NAMES[:n]
        outs = list(itertools.product("グチパ", repeat=n))
        beats = {"グ": "チ", "チ": "パ", "パ": "グ"}

        def winners(s):
            kinds = set(s)
            if len(kinds) != 2:
                return set()
            x, y = kinds
            w = x if beats[x] == y else y
            return {P[i] for i, h in enumerate(s) if h == w}
        opts = [("あいこになる", lambda s: not winners(s)), ("A だけが勝つ", lambda s: winners(s) == {"A"})]
        if n == 3:
            opts += [("1人だけが勝つ", lambda s: len(winners(s)) == 1), ("A がふくまれる2人が勝つ", lambda s: len(winners(s)) == 2 and "A" in winners(s)),
                     ("A が負けない（勝つかあいこになる）", lambda s: not winners(s) or "A" in winners(s))]
        name, f = r.choice(opts)
        stem = f"{'，'.join(P)} の{n}人が1回だけじゃんけんをするとき，{name}確率を求めなさい。ただし，それぞれがグー，チョキ，パーのどれを出すことも同様に確からしいものとする。"
        fmt = lambda s: "（" + "，".join(s) + "）"  # noqa: E731
        tot = f"手の出し方は $3^{n}={len(outs)}$ 通り"
    good = [s for s in outs if f(s)]
    c, N = len(good), len(outs)
    assert 0 < c < N
    ex = "，".join(fmt(s) for s in good[:9]) + (" など" if c > 9 else "")
    return MARK(stem, Fr(c, N), f"全部で ${N}$ 通り，そのうち ${c}$ 通りなので ${fd(c, N)}$。", f"Rational({c},{N})", d=3, p=4,
                ap="まず順番を区別するか（委員長と副委員長，並び方，じゃんけんの手）を判断し，樹形図ですべての場合を数える。",
                steps=[f"{tot}。", f"あてはまるのは {ex} の ${c}$ 通り。", f"確率は ${fd(c, N)}$。"],
                alt=[f"あてはまらない場合 ${N - c}$ 通りを数え，$1-\\dfrac{{{N - c}}}{{{N}}}$ でも確かめられる。"],
                pc=[("すべての場合の数を正しく求めている", 2), ("正しい確率を求めている", 2)],
                pit=["代表2人の選び方で，AB と BA を別々に数える。", "じゃんけんで，グー・チョキ・パーの3種類がそろったときのあいこを見落とす。"])


# ======================================================================
# C 思考力・記述応用
# ======================================================================

OP1 = [("$a$ と同じ数が書かれたカード", lambda x, a: x == a),
       ("$a$ の約数が書かれたカードをすべて", lambda x, a: a % x == 0),
       ("$a$ の倍数が書かれたカードをすべて", lambda x, a: x % a == 0)]
OP2 = [("$b$ と同じ数が書かれたカード", lambda x, b: x == b),
       ("$b$ の約数が書かれたカードをすべて", lambda x, b: b % x == 0),
       ("$b$ の倍数が書かれたカードをすべて", lambda x, b: x % b == 0),
       ("$b$ より大きい数が書かれたカードをすべて", lambda x, b: x > b)]


def _remain(N, i1, i2, a, b):
    s = [x for x in range(1, N + 1) if not OP1[i1][1](x, a)]
    return [x for x in s if not OP2[i2][1](x, b)]


def _op_combos():
    out = []
    for N in (6, 7, 8):
        for i1 in range(3):
            for i2 in range(4):
                if i1 == 0 and i2 == 0:
                    continue
                rem = {(a, b): _remain(N, i1, i2, a, b) for a, b in DICE}
                qs = []
                for k in range(0, N + 1):
                    qs.append((f"箱の中に残ったカードが{k}枚になる" if k else "箱の中にカードが1枚も残らない", lambda R, k=k: len(R) == k))
                for k in range(2, N):
                    qs.append((f"箱の中に残ったカードが{k}枚以上になる", lambda R, k=k: len(R) >= k))
                for m in range(1, N + 1):
                    qs.append((f"数字{m}が書かれたカードが箱の中に残る", lambda R, m=m: m in R))
                qs.append(("箱の中に残ったカードに書かれた数の和が奇数になる", lambda R: sum(R) % 2 == 1))
                for qi, (qt, f) in enumerate(qs):
                    good = [ab for ab in DICE if f(rem[ab])]
                    if 2 <= len(good) <= 34:
                        out.append((N, i1, i2, qt, tuple(good)))
    return out


OP_COMBOS = _op_combos()


@gen("thinking_writing", 4, ["application", "computation"])
def c_operation(r):
    N, i1, i2, qt, good = r.choice(OP_COMBOS)
    good = list(good)
    c = len(good)
    a0, b0 = r.choice([(a, b) for a, b in DICE if a != b and 1 < a])
    s1 = [x for x in range(1, N + 1) if OP1[i1][1](x, a0)]
    mid = [x for x in range(1, N + 1) if x not in s1]
    s2 = [x for x in mid if OP2[i2][1](x, b0)]
    rem = [x for x in mid if x not in s2]
    L = lambda xs: "，".join(map(str, xs)) if xs else "なし"  # noqa: E731
    ex = (f"〔例〕大きいさいころの出た目の数が{a0}，小さいさいころの出た目の数が{b0}のとき，"
          f"【操作1】で {L(s1)} のカードを取り出し，【操作2】で {L(s2)} のカードを取り出す（取り出すカードがないときは何もしない）。"
          f"このとき，箱の中には {L(rem)} のカードが残る。")
    stem = (f"箱の中に，1から{N}までの数字が1つずつ書かれた{N}枚のカードが入っている。大小2つのさいころを同時に1回投げ，大きいさいころの出た目の数を $a$，小さいさいころの出た目の数を $b$ として，次の【操作1】，【操作2】を順に行う。\n"
            f"【操作1】{OP1[i1][0]}箱から取り出す。\n【操作2】【操作1】の後，箱の中に残っているカードのうち，{OP2[i2][0]}箱から取り出す。\n{ex}\n"
            f"いま，箱の中に{N}枚のカードが入っている状態で，この操作を行うとき，{qt}確率を求めなさい。{SAME_DICE}")
    return MARK(stem, Fr(c, 36), f"36 通りのうち ${c}$ 通りなので ${fd(c, 36)}$。", f"Rational({c},36)", d=4, p=8,
                ap="まず $a$ の値ごとに【操作1】の後に残るカードを書き出す。次に，それぞれについて $b$ を 1〜6 と変えて【操作2】を行い，36 通りの表にまとめる。",
                steps=[f"$a=1$〜$6$ のそれぞれについて，【操作1】の後に残るカードを調べる。",
                       "そのそれぞれについて $b=1$〜$6$ で【操作2】を行い，残るカードを表にまとめる。",
                       f"条件にあてはまる $(a,\\,b)$ は {pairs_txt(good)}（{by_a(good)}）の ${c}$ 通り。",
                       f"確率は ${fd(c, 36)}$。"],
                alt=[f"あてはまらない $(a,\\,b)$ を数えて ${36 - c}$ 通りとなることを確かめ，$1-\\dfrac{{{36 - c}}}{{36}}$ と計算しても同じ。"],
                pc=[("【操作1】の後の残りを $a$ ごとに正しく調べている", 3), ("【操作2】まで行い，あてはまる場合を正しく数えている", 3), ("正しい確率", 2)],
                pit=["【操作2】で，【操作1】ですでに取り出したカードも取り出すと考える。", "約数・倍数に 1 や $a$ 自身をふくめ忘れる。"])


def _xy_pool(r):
    f = r.randint(1, 6)
    s1, s2 = r.sample([s for s in range(2, 13) if s != 7], 2)
    c1, c2 = (6 - abs(7 - s1)), (6 - abs(7 - s2))
    while c1 == c2:
        s2 = r.choice([s for s in range(2, 13) if s not in (s1, 14 - s1)])
        c2 = 6 - abs(7 - s2)
    q = r.randint(3, 11)
    p = r.choice([x for x in range(1, q) if math.gcd(x, q) == 1])
    rd, wh = r.randint(2, 6), r.randint(1, 6)
    while rd == wh:
        wh = r.randint(1, 6)
    n_k, k_w = r.randint(4, 9), r.randint(1, 3)
    return [
        (f"1つのさいころを投げるとき，{f}の目が出る確率は $\\dfrac{{1}}{{6}}$ なので，6回投げると{f}の目は必ず1回出る。", False, "6回投げても1回も出ないことがある。確率は多数回での割合の目安である。"),
        (f"大小2つのさいころを投げるとき，出た目の数の和が{s1}になる確率は，和が{s2}になる確率より大きい。", c1 > c2,
         f"和が{s1}になるのは ${c1}$ 通り，{s2}になるのは ${c2}$ 通りなので，{'正しい' if c1 > c2 else '誤り'}。"),
        ("2枚の硬貨を投げるとき，2枚とも表になる確率は $\\dfrac{1}{3}$ である。", False, "出方は（表，表）（表，裏）（裏，表）（裏，裏）の 4 通りなので $\\dfrac{1}{4}$。"),
        ("2枚の硬貨を投げるとき，表と裏が1枚ずつ出る確率は $\\dfrac{1}{2}$ である。", True, "4 通りのうち（表，裏）（裏，表）の 2 通りなので $\\dfrac{1}{2}$。"),
        (f"ことがら A の起こる確率が $\\dfrac{{{p}}}{{{q}}}$ のとき，A の起こらない確率は $\\dfrac{{{q - p}}}{{{q}}}$ である。", True, "起こらない確率は $1-p$ で求められる。"),
        (f"赤玉{rd}個と白玉{wh}個が入った袋から1個取り出すとき，赤玉が出る確率は $\\dfrac{{{rd}}}{{{wh}}}$ である。", False,
         f"分母はすべての玉の数 ${rd + wh}$ なので，$\\dfrac{{{rd}}}{{{rd + wh}}}$ が正しい。"),
        (f"{n_k}本のうち{k_w}本の当たりが入ったくじを，A，B の順に1本ずつ引く（引いたくじはもどさない）とき，A と B の当たる確率は等しい。", True,
         f"樹形図で調べると，どちらも $\\dfrac{{{k_w}}}{{{n_k}}}$ となり，引く順番による有利・不利はない。"),
        (f"{n_k}本のうち{k_w}本の当たりが入ったくじを，A，B の順に1本ずつ引く（引いたくじはもどさない）とき，先に引く A の方が当たりやすい。", False,
         f"どちらも当たる確率は $\\dfrac{{{k_w}}}{{{n_k}}}$ で等しい。"),
        ("3枚の硬貨を投げるとき，表が1枚出る確率と表が2枚出る確率は等しい。", True, "8 通りのうち，どちらも 3 通りなので $\\dfrac{3}{8}$ で等しい。"),
        ("大小2つのさいころを投げるとき，同じ目が出る確率は $\\dfrac{1}{36}$ である。", False, "同じ目は $(1,1)$〜$(6,6)$ の 6 通りなので $\\dfrac{6}{36}=\\dfrac{1}{6}$。"),
        ("確率が 0 であることがらは，決して起こらない。", True, "あてはまる場合が 0 通りのとき確率は 0 で，そのことがらは起こらない。"),
        ("場合の数の数え方によっては，確率が 1 より大きくなることがある。", False, "あてはまる場合の数はすべての場合の数以下なので，確率は 1 以下である。"),
    ]


@gen("thinking_writing", 3, ["written_reasoning", "condition_check", "concept"])
def c_xy_judge(r):
    S = _xy_pool(r)
    tx, ty = r.choice([True, False]), r.choice([True, False])
    x = r.choice([s for s in S if s[1] == tx])
    y = r.choice([s for s in S if s[1] == ty and s is not x])
    XY = ["X：正　Y：正", "X：正　Y：誤", "X：誤　Y：正", "X：誤　Y：誤"]
    ans = XY[(0 if tx else 2) + (0 if ty else 1)]
    why = {}
    for ch in XY:
        if ch == ans:
            continue
        cx, cy = ch.startswith("X：正"), ch.endswith("Y：正")
        rs = []
        if cx != tx:
            rs.append(f"X は{'正しい' if tx else '誤り'}。{x[2]}")
        if cy != ty:
            rs.append(f"Y は{'正しい' if ty else '誤り'}。{y[2]}")
        why[ch] = (" ".join(rs), "確率の意味や数え方の思いこみ")
    return mc("確率について述べた次の X，Y の文の正誤の組み合わせとして最も適するものを，" + SEL4 + f"\nX　{x[0]}\nY　{y[0]}",
              [ans] + [ch for ch in XY if ch != ans], f"X：{x[2]}　Y：{y[2]}", d=4, p=8, why=why,
              ap="それぞれの文について，樹形図や表で実際に場合の数を数えたり，確率の意味にもどったりして正誤を判断する。",
              steps=[f"X：{x[2]}", f"Y：{y[2]}", f"よって {ans}。"],
              alt=["正しいと思った文も，具体的な場合を書き出して数え，理由を言葉で説明できるか確かめる。"],
              pc=[("X の正誤を根拠をもって判断している", 4), ("Y の正誤を根拠をもって判断している", 4)],
              pit=["同様に確からしくない場合をもとに確率を計算する。", "確率を「必ずそうなる回数」と考える。"])


@gen("thinking_writing", 3, ["cross_unit", "application"], rel=["JH-MATH-G2-U03"])
def c_cross(r):
    kind = r.choice(["line", "line", "above", "eq", "num"])
    if kind == "line":
        m = r.choice([Fr(1), Fr(2), Fr(1, 2), Fr(3), Fr(-1), Fr(1, 3), Fr(-2)])
        cs = []
        for c0 in range(-6, 13):
            g = [(a, b) for a, b in DICE if b == m * a + c0]
            if 2 <= len(g):
                cs.append(c0)
        c0 = r.choice(cs)
        f = lambda a, b: b == m * a + c0  # noqa: E731
        mt = ("" if m == 1 else "-" if m == -1 else ft(m))
        line = f"y={mt}x" + (f"+{c0}" if c0 > 0 else (f"-{-c0}" if c0 < 0 else ""))
        name = f"点 P$(a,\\,b)$ が直線 ${line}$ 上にある"
        rel = ["JH-MATH-G2-U03"]
        hint = f"${line.replace('x', 'a').replace('y', 'b')}$ を満たす組を探す"
    elif kind == "above":
        c0 = r.randint(-2, 3)
        line = "y=x" + (f"+{c0}" if c0 > 0 else (f"-{-c0}" if c0 < 0 else ""))
        f = lambda a, b: b > a + c0  # noqa: E731
        name = f"点 P$(a,\\,b)$ が直線 ${line}$ より上側にある（直線上の点はふくまない）"
        rel = ["JH-MATH-G2-U03"]
        hint = f"$b>a{'+' + str(c0) if c0 > 0 else ('-' + str(-c0) if c0 < 0 else '')}$ を満たす組を数える"
    elif kind == "eq":
        k = r.choice([1, 2, 3])
        f = lambda a, b: (k * b) % a == 0  # noqa: E731
        bt = "b" if k == 1 else f"{k}b"
        name = f"$x$ についての方程式 $ax={bt}$ の解が整数になる"
        rel = ["JH-MATH-G1-U03"]
        hint = f"解 $x=\\dfrac{{{bt}}}{{a}}$ が整数になる，つまり ${bt}$ が $a$ の倍数になる組を数える"
    else:
        k = r.choice([3, 4, 6, 7, 8, 9])
        f = lambda a, b: (10 * a + b) % k == 0  # noqa: E731
        name = f"十の位の数が $a$，一の位の数が $b$ である2けたの整数 $10a+b$ が{k}の倍数になる"
        rel = ["JH-MATH-G2-U01"]
        hint = f"$11$〜$66$ の中で，各位が 1〜6 の {k} の倍数を探す"
    good = [(a, b) for a, b in DICE if f(a, b)]
    c = len(good)
    assert 0 < c < 36
    stem = f"大小2つのさいころを同時に1回投げ，大きいさいころの出た目の数を $a$，小さいさいころの出た目の数を $b$ とする。このとき，{name}確率を求めなさい。{SAME_DICE}"
    return MARK(stem, Fr(c, 36), f"36 通りのうち ${c}$ 通りなので ${fd(c, 36)}$。", f"Rational({c},36)", d=4, p=8, rel=rel,
                ap="さいころの目 $(a,\\,b)$ を条件の式に代入し，成り立つかどうかを36通りについて調べる。式の意味（グラフ・方程式・整数の性質）を先に整理すると数えやすい。",
                steps=[f"{hint}。", f"あてはまる $(a,\\,b)$ は {pairs_txt(good)}（{by_a(good)}）の ${c}$ 通り。", f"確率は ${fd(c, 36)}$。"],
                alt=["座標平面上に 36 個の点（または 36 マスの表）をかき，条件を満たす点に印をつけて数えて確かめる。"],
                pc=[("条件を $a$，$b$ の関係として正しくとらえている", 3), ("あてはまる場合を正しく数えている", 3), ("正しい確率", 2)],
                pit=["$a$ と $b$（$x$ 座標と $y$ 座標）を取り違える。", "境界（直線上・等号）をふくめるかどうかを読み落とす。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def _err_mc(stem, sol, right, cands, e, err, **kw):
    return MC(f"{stem}\n〔Kさんの解答〕\n{sol}\nKさんの解答の誤りを説明したものとして最も適するものを，" + SEL4, right, cands, e, err=err, **kw)


@gen("error_correction", 4, ["common_error", "concept"])
def d_equally(r):
    kind = r.choice(["coin2", "coin2b", "coin3", "dsum", "dsame", "bag"])
    if kind == "coin2":
        stem = f"〔問題〕2枚の硬貨を同時に投げるとき，1枚が表で1枚が裏になる確率を求めなさい。{SAME_COIN}"
        sol = "出方は（表，表），（表，裏），（裏，裏）の3通り。\nそのうち1枚が表で1枚が裏になるのは1通りなので，確率は $\\dfrac{1}{3}$"
        c, N, wrongv = 2, 4, Fr(1, 3)
        right = "硬貨を区別していないので，3通りは同様に確からしくない。（表，裏）と（裏，表）は別の場合として数えなければならない。"
    elif kind == "coin2b":
        stem = f"〔問題〕2枚の硬貨を同時に投げるとき，2枚とも表になる確率を求めなさい。{SAME_COIN}"
        sol = "出方は「2枚とも表」「1枚だけ表」「2枚とも裏」の3通り。\nそのうち2枚とも表は1通りなので，確率は $\\dfrac{1}{3}$"
        c, N, wrongv = 1, 4, Fr(1, 3)
        right = "「1枚だけ表」は2通りの出方をまとめたものなので，3通りは同様に確からしくない。全部で4通りとして考えなければならない。"
    elif kind == "coin3":
        k = r.choice([1, 2])
        stem = f"〔問題〕3枚の硬貨を同時に投げるとき，表がちょうど{k}枚出る確率を求めなさい。{SAME_COIN}"
        sol = f"表の枚数は 0 枚，1 枚，2 枚，3 枚の4通り。\nそのうち表が{k}枚は1通りなので，確率は $\\dfrac{{1}}{{4}}$"
        c, N, wrongv = 3, 8, Fr(1, 4)
        right = f"表の枚数の4通りは同様に確からしくない。硬貨を区別すると出方は8通りあり，表が{k}枚になるのはそのうち3通りである。"
    elif kind == "dsum":
        s = r.choice([x for x in range(3, 12) if x != 7])
        c = 6 - abs(7 - s)
        stem = f"〔問題〕大小2つのさいころを同時に投げるとき，出た目の数の和が{s}になる確率を求めなさい。{SAME_DICE}"
        sol = f"出た目の数の和は 2 から 12 までの11通り。\nそのうち和が{s}になるのは1通りなので，確率は $\\dfrac{{1}}{{11}}$"
        N, wrongv = 36, Fr(1, 11)
        right = f"和の11通りは同様に確からしくない。目の出方 36 通りをもとに考え，和が{s}になる ${c}$ 通りを数えなければならない。"
    elif kind == "dsame":
        stem = f"〔問題〕2つのさいころを同時に投げるとき，同じ目が出る確率を求めなさい。{SAME_DICE.replace('大小2つのさいころ', '2つのさいころ')}"
        sol = "2つのさいころの目の組は，{1，1}，{1，2}，…，{6，6} のように，順番を考えないと21通り。\nそのうち同じ目は6通りなので，確率は $\\dfrac{6}{21}=\\dfrac{2}{7}$"
        c, N, wrongv = 6, 36, Fr(2, 7)
        right = "順番を考えない21通りは同様に確からしくない。2つのさいころを区別すると36通りになり，そのうち同じ目は6通りである。"
    else:
        rd, wh = r.choice([(2, 1), (3, 1), (3, 2), (1, 3), (4, 1), (2, 3), (1, 2)])
        stem = f"〔問題〕赤玉{rd}個と白玉{wh}個が入った袋から1個取り出すとき，赤玉が出る確率を求めなさい。ただし，どの玉が取り出されることも同様に確からしいものとする。"
        sol = "取り出した玉の色は，赤か白の2通り。\nそのうち赤は1通りなので，確率は $\\dfrac{1}{2}$"
        c, N, wrongv = rd, rd + wh, Fr(1, 2)
        right = f"赤と白の2通りは同様に確からしくない。玉を区別すると取り出し方は ${rd + wh}$ 通りあり，赤玉はそのうち ${rd}$ 通りである。"
    v = Fr(c, N)
    cands = [("分母と分子が逆になっている。", f"Kさんの値 ${ft(wrongv)}$ は 1 より小さく，分母と分子の取り違えではない。", "計算の誤りとの混同"),
             ("確率は場合の数そのものなので，答えは通り数で表さなければならない。", "確率は（あてはまる場合の数）÷（すべての場合の数）で表す数である。", "確率と場合の数の混同"),
             ("約分を忘れている。", "約分の問題ではない。数えている場合そのものが同様に確からしくない。", "誤りの箇所の取り違え"),
             ("Kさんの解答に誤りはない。", f"正しく数えると確率は ${ft(v)}$ となり，Kさんの答えと異なる。", "検算不足")]
    r.shuffle(cands)
    fix = f"${fd(c, N)}$"
    return _err_mc(stem, sol, right, cands, f"正しくは {fix}。",
                   dict(sol=sol, step="すべての場合を数える1行目", type="concept", tempt="結果の「種類」を数えると簡単に見えるため，それらが同じ程度に起こるかを確かめずに使ってしまう。", fix=fix),
                   d=3, p=6,
                   ap="Kさんが数えた「すべての場合」が，どれも同じ程度に起こるか（同様に確からしいか）を確かめる。硬貨・さいころ・玉を区別して数え直す。",
                   steps=["Kさんの数えた場合を，区別した場合に分解すると，含まれる数がちがう。", "区別して数えた場合は同様に確からしい。", f"正しい確率は ${fd(c, N)}$。"],
                   alt=["実際に硬貨やさいころを多数回投げる実験をすると，相対度数が Kさんの値ではなく正しい値に近づくことからも確かめられる。"],
                   pc=[("誤りの理由（同様に確からしくない）を正しく指摘している", 3), ("正しい確率を求めている", 3)],
                   pit=["結果の種類の数を，すべての場合の数と考える。"],
                   chk=(f"Rational({c},{N})", f"Rational({v.numerator},{v.denominator})", None, "intermediate"))


@gen("error_correction", 3, ["common_error", "written_reasoning", "computation"])
def d_line_err(r):
    rd, wh = r.choice([(3, 2), (2, 3), (4, 2), (3, 3), (2, 2), (4, 1), (3, 1), (2, 4)])
    n = rd + wh
    T = n * (n - 1) // 2
    ev = r.choice(["rr", "diff"] + (["ww"] if wh >= 2 else []))
    F = {"rr": rd * (rd - 1) // 2, "diff": rd * wh, "ww": wh * (wh - 1) // 2}[ev]
    if F == 0 or F == T:
        ev, F = "diff", rd * wh
    name = {"rr": "2個とも赤玉である", "diff": "赤玉と白玉が1個ずつである", "ww": "2個とも白玉である"}[ev]
    where = r.randint(1, 3)
    Tk, Fk = T, F
    l1 = "赤玉と白玉に番号をつけて区別する"
    if where == 1:
        Tk = n * (n - 1)
        l2 = f"取り出し方は ${n}\\times{n - 1}={Tk}$ 通り"
    else:
        l2 = f"取り出し方は ${n}\\times{n - 1}\\div2={T}$ 通り"
    if where == 2:
        if ev == "diff":
            Fk = rd + wh
            l3 = f"{name}取り出し方は ${rd}+{wh}={Fk}$ 通り"
        else:
            k = rd if ev == "rr" else wh
            Fk = k * (k - 1)
            l3 = f"{name}取り出し方は ${k}\\times{k - 1}={Fk}$ 通り"
        if Fk == F:
            Fk = F + 1
            l3 = f"{name}取り出し方は ${Fk}$ 通り"
    else:
        l3 = f"{name}取り出し方は ${F}$ 通り"
    if where == 3:
        assert Fr(F, T) != Fr(1, 2)
        l4 = f"確率は $1-\\dfrac{{{F}}}{{{T}}}={ft(1 - Fr(F, T))}$"
    else:
        l4 = f"確率は $\\dfrac{{{Fk}}}{{{Tk}}}" + ("" if Fr(Fk, Tk).denominator == Tk and Fr(Fk, Tk).numerator == Fk else f"={ft(Fr(Fk, Tk))}") + "$"
    sol = "\n".join(f"{i + 1}行目　{t}" for i, t in enumerate([l1, l2, l3, l4]))
    LINES4 = ["1行目", "2行目", "3行目", "4行目"]
    ok = {0: "1行目は正しい。同じ色の玉を区別するのは，同様に確からしい場合をつくるために必要である。",
          1: f"2行目は正しい。同時に取り出すので，順番を考えない ${T}$ 通りである。",
          2: f"3行目は正しい。{name}取り出し方は ${F}$ 通りである。",
          3: "4行目は，3行目までの数を使って確率を正しく計算している。"}
    why = {LINES4[i]: (ok[i], "誤りの箇所の見落とし") for i in range(4) if i != where}
    info = {1: ("2行目（同時に取り出すのに順番を区別して数えた）", "concept", "「1個目，2個目」と考えるとかけ算だけで数えやすいが，同時に取り出すときは同じ組を2回数えてしまう。"),
            2: ("3行目（あてはまる場合の数え方）", "calculation", "色の組み合わせを数えるとき，たし算とかけ算，順番の有無を取り違えやすい。"),
            3: ("4行目（1から引いた）", "interpretation", "「少なくとも」などで使う $1-p$ の計算を，必要のない場面で使ってしまう。")}[where]
    fix = f"${fd(F, T)}$"
    return mc(f"〔問題〕赤玉{rd}個と白玉{wh}個が入った袋から，同時に2個の玉を取り出すとき，{name}確率を求めなさい。ただし，どの玉が取り出されることも同様に確からしいものとする。\n〔Kさんの解答〕\n{sol}\nKさんの解答で，誤りが最初に生じた行として最も適するものを，" + SEL4,
              LINES4, f"誤りが最初に生じたのは{LINES4[where]}。正しくは {fix}。", d=3, p=6, keep=True, ai=where, why=why,
              err=dict(sol=sol, step=info[0], type=info[1], tempt=info[2], fix=fix),
              ap="各行で数えている場合の数を，自分で玉に番号をつけて書き出した結果と比べる。同時に取り出すときは順番を考えないことに注意する。",
              steps=[f"取り出し方は全部で ${n}\\times{n - 1}\\div2={T}$ 通り。", f"{name}取り出し方は ${F}$ 通り。", f"確率は {fix}。"],
              alt=["樹形図で {赤1，赤2} のように組を書き出して，すべての場合とあてはまる場合を数え直す。"],
              pc=[("誤りの行を正しく指摘している", 3), ("正しい確率を求めている", 3)],
              pit=["同時に取り出すのに，順番を区別して数える。"],
              chk=(f"Rational({F},{T})", f"Rational({Fr(F, T).numerator},{Fr(F, T).denominator})", None, "intermediate"))


@gen("error_correction", 3, ["common_error", "condition_check"])
def d_atleast(r):
    kind = r.choice(["coin_wrongcomp", "coin_add", "dice_add", "ball_exact"])
    if kind == "coin_wrongcomp":
        n = r.choice([2, 3, 4])
        N = 2 ** n
        stem = f"〔問題〕{n}枚の硬貨を同時に投げるとき，少なくとも1枚は表が出る確率を求めなさい。{SAME_COIN}"
        sol = f"{n}枚とも表になる確率は $\\dfrac{{1}}{{{N}}}$\nよって，少なくとも1枚は表が出る確率は $1-\\dfrac{{1}}{{{N}}}=\\dfrac{{{N - 1}}}{{{N}}}$"
        right = f"「少なくとも1枚は表」が起こらないのは「{n}枚とも裏」の場合である。1 から引くのは{n}枚とも裏になる確率でなければならない。"
        c, T = N - 1, N
        tempt = "答えの数値は正しい値と一致してしまうため，考え方の誤りに気づきにくい。"
        wrong_pool = [("1 から引くのではなく，$\\dfrac{1}{" + str(N) + "}$ をそのまま答えるべきである。", "「少なくとも1枚は表」はほとんどの場合にあてはまるので，確率は大きくなる。", "余事象の考え方の誤解"),
                      ("硬貨の出方は全部で $" + str(2 * n) + "$ 通りである。", f"硬貨1枚に2通りずつあるので，全部で $2^{n}={N}$ 通りである。", "かけ算とたし算の混同")]
        etype = "logic"
    elif kind == "coin_add":
        n = r.choice([2, 3])
        N = 2 ** n
        stem = f"〔問題〕{n}枚の硬貨を同時に投げるとき，少なくとも1枚は表が出る確率を求めなさい。{SAME_COIN}"
        tot = Fr(n, 2)
        sol = f"1枚の硬貨が表になる確率は $\\dfrac{{1}}{{2}}$\n{n}枚あるので，$" + "+".join(["\\dfrac{1}{2}"] * n) + f"={ft(tot)}$"
        right = "2枚以上が同時に表になる場合を重ねて数えている。「すべて裏」になる確率を 1 から引いて求めなければならない。"
        c, T = N - 1, N
        tempt = "「どれか1枚が表」を，それぞれの確率をたせばよいと考えやすい。"
        wrong_pool = [("確率 $\\dfrac{1}{2}$ をたすのではなく，かけなければならない。", f"かけると $\\left(\\dfrac{{1}}{{2}}\\right)^{n}$ で，「すべて表」の確率になってしまう。", "積の考えの誤用"),
                      ("1枚の硬貨が表になる確率は $\\dfrac{1}{3}$ である。", "表と裏の2通りなので $\\dfrac{1}{2}$ で正しい。", "確率の基本の誤解")]
        etype = "concept"
    elif kind == "dice_add":
        f = r.randint(1, 6)
        stem = f"〔問題〕大小2つのさいころを同時に投げるとき，少なくとも一方のさいころで{f}の目が出る確率を求めなさい。{SAME_DICE}"
        sol = f"大きいさいころで{f}の目が出る確率は $\\dfrac{{1}}{{6}}$，小さいさいころで{f}の目が出る確率も $\\dfrac{{1}}{{6}}$\nよって $\\dfrac{{1}}{{6}}+\\dfrac{{1}}{{6}}=\\dfrac{{1}}{{3}}$"
        right = f"両方で{f}の目が出る $({f},\\,{f})$ を2回数えている。36 通りのうち，どちらにも{f}の目が出ない 25 通りを除いた 11 通りで考えなければならない。"
        c, T = 11, 36
        tempt = "それぞれの確率をたせば「どちらか」の確率になると考えやすい。"
        wrong_pool = [("$\\dfrac{1}{6}$ と $\\dfrac{1}{6}$ をかけて $\\dfrac{1}{36}$ としなければならない。", f"$\\dfrac{{1}}{{36}}$ は両方で{f}の目が出る確率である。", "積の考えの誤用"),
                      ("2つのさいころの目の出方は全部で12通りである。", "大の6通りそれぞれに小の6通りがあるので36通りである。", "かけ算とたし算の混同")]
        etype = "logic"
    else:
        rd, wh = r.choice([(3, 2), (2, 3), (4, 2), (3, 3), (2, 2), (3, 4)])
        n = rd + wh
        T = n * (n - 1) // 2
        one = rd * wh
        stem = f"〔問題〕赤玉{rd}個と白玉{wh}個が入った袋から同時に2個取り出すとき，少なくとも1個は白玉である確率を求めなさい。ただし，どの玉が取り出されることも同様に確からしいものとする。"
        sol = f"取り出し方は全部で ${T}$ 通り。\n白玉が1個ふくまれる取り出し方は ${rd}\\times{wh}={one}$ 通りなので，確率は ${fd(one, T)}$"
        right = "「少なくとも1個は白玉」には，2個とも白玉の場合もふくまれる。その場合を数えもらしている。"
        c, T = one + wh * (wh - 1) // 2, T
        tempt = "「少なくとも1個」を「ちょうど1個」と読みかえてしまいやすい。"
        wrong_pool = [("同時に取り出すので，取り出し方は全部で $" + str(n * (n - 1)) + "$ 通りとしなければならない。", f"同時に取り出すときは順番を考えないので ${T}$ 通りで正しい。", "順番の有無の混同"),
                      ("白玉が1個ふくまれる取り出し方は $" + str(rd + wh) + "$ 通りである。", f"赤 ${rd}$ 個のそれぞれと白 ${wh}$ 個のそれぞれの組なので ${rd}\\times{wh}$ 通りで正しい。", "かけ算とたし算の混同")]
        etype = "condition"
    v = Fr(c, T)
    cands = wrong_pool + [("Kさんの解答に誤りはない。", f"正しい考え方では，求める確率は ${ft(v)}$ になる。" if kind != "coin_wrongcomp" else "答えの値は正しいが，1 から引いている確率のことがらが誤っており，考え方が正しくない。", "検算不足")]
    fix = f"$1-(\\text{{起こらない確率}})={ft(v)}$"
    return _err_mc(stem, sol, right, cands, f"正しくは {fix}。",
                   dict(sol=sol, step="「少なくとも」の扱い", type=etype, tempt=tempt, fix=fix), d=3, p=6,
                   ap="「少なくとも1つ」の反対（起こらない場合）は「1つもない」。その確率を 1 から引くのが確実な方法である。",
                   steps=["求めることがらの反対のことがら（1つもない場合）を考える。", "その確率を求める。", f"1 から引いて ${ft(v)}$。"],
                   alt=["樹形図や表で，あてはまる場合を直接すべて数えて確かめる。"],
                   pc=[("誤りの理由を正しく指摘している", 3), ("正しい確率を求めている", 3)],
                   pit=["「少なくとも1つ」の確率を，それぞれの確率のたし算で求める。", "1 から引く確率のことがらを取り違える。"],
                   chk=(f"Rational({c},{T})", f"Rational({v.numerator},{v.denominator})", None, "intermediate"))


GENERATORS = [a_single, a_coins, a_count, a_concept,
              b_two_dice, b_balls, b_cards, b_people,
              c_operation, c_xy_judge, c_cross,
              d_equally, d_line_err, d_atleast]
GENERATORS = [robust(g) for g in GENERATORS]
