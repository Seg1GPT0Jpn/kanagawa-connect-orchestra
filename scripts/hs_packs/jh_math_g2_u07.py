"""単元パック：中学2年 データの分布　四分位範囲と箱ひげ図（神奈川県公立高校入試形式）。"""
import itertools
import re
import unicodedata
from fractions import Fraction as Fr

from banks._common import figure, mc, num, table
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem, tp)

UNIT_ID = "JH-MATH-G2-U07"

PREREQUISITES = [
    ("JH-MATH-G1-U07", "データを小さい順に並べて中央値・範囲を求めること、ヒストグラムの見方。四分位数は中央値の考え方をくり返して求める。"),
    ("JH-MATH-G1-U01", "数の大小と、小数・分数の計算。2つの値の平均（真ん中の値）を求めるときに使う。"),
]
EXTENSIONS = [
    ("JH-MATH-G3-U08", "標本の箱ひげ図や代表値から、母集団の傾向を推定する。"),
    ("HS-MATH1-U05", "高校のデータの分析で、四分位偏差・外れ値・分散・標準偏差を使ってデータの散らばりを調べる。"),
    ("JH-MATH-G2-U06", "データの割合と確率の考え方を合わせて、起こりやすさや傾向を判断する。"),
]
FAKE = "（架空の資料）"


# ----------------------------------------------------------------------
# 共通ヘルパー
# ----------------------------------------------------------------------

def _norm(s):
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", s))


def MC(stem, right, cands, e, k=3, **kw):
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
    v = Fr(v)
    assert v >= 0
    if v.denominator == 1:
        n = int(v)
        return num(stem, str(n), e, mark=("int", n), chk=(expr, str(n), None, "answer"), **kw)
    p, q = v.numerator, v.denominator
    return num(stem, f"$\\dfrac{{{p}}}{{{q}}}$", e, mark=("frac", p, q), chk=(expr, f"Rational({p},{q})", None, "answer"), **kw)


def dec(v):
    v = Fr(v)
    if v.denominator == 1:
        return str(v.numerator)
    return f"{float(v):.10g}"


def fpy(v):
    v = Fr(v)
    return str(v.numerator) if v.denominator == 1 else f"Rational({v.numerator},{v.denominator})"


def robust(g):
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


SEL4 = "次の1〜4の中から1つ選び，その番号を答えなさい。"
SEL6 = "次の1〜6の中から1つ選び，その番号を答えなさい。"
KANA = "アイウエ"


def med(xs):
    s = sorted(xs)
    n = len(s)
    return Fr(s[n // 2]) if n % 2 else Fr(s[n // 2 - 1] + s[n // 2], 2)


def five(xs):
    """(最小値, 第1四分位数, 中央値, 第3四分位数, 最大値)。中学校の方法（奇数個のときは中央値を除いて前半・後半に分ける）。"""
    s = sorted(xs)
    n = len(s)
    lower, upper = s[:n // 2], s[(n + 1) // 2:]
    return (Fr(s[0]), med(lower), med(s), med(upper), Fr(s[-1]))


def is_int5(f):
    return all(v.denominator == 1 for v in f)


def int_data(r, n, lo, hi):
    """四分位数がすべて整数になるデータ（並べる前の順）。"""
    for _ in range(300):
        xs = [r.randint(lo, hi) for _ in range(n)]
        f = five(xs)
        if is_int5(f) and f[0] < f[1] < f[2] < f[3] < f[4]:
            return xs
    while True:  # n=11 なら四分位数は必ずデータの値になる
        xs = sorted(r.sample(range(lo, hi + 1), 11)) if hi - lo >= 11 else [lo + i for i in range(11)]
        r.shuffle(xs)
        return xs


def lst(xs):
    return "，".join(map(str, xs))


CTX = [("小テストの得点", "点", 0, 20), ("1か月に読んだ本の冊数", "冊", 0, 16), ("ハンドボール投げの記録", "m", 8, 34),
       ("通学にかかる時間", "分", 5, 40), ("1週間の家庭学習の時間", "時間", 2, 22), ("けん垂の回数", "回", 0, 18)]


def ctx(r):
    return r.choice(CTX)


def pos_txt(n):
    """n 個のデータの中央値・四分位数の位置の説明。"""
    if n % 2:
        h = n // 2
        a = f"中央値は小さい方から ${h + 1}$ 番目の値。中央値を除いた前半 ${h}$ 個，後半 ${h}$ 個に分ける"
    else:
        h = n // 2
        a = f"中央値は ${h}$ 番目と ${h + 1}$ 番目の値の平均。前半 ${h}$ 個，後半 ${h}$ 個に分ける"
    return a


# ----------------------------------------------------------------------
# 図（SVG）
# ----------------------------------------------------------------------

def _scale(lo, hi):
    span = hi - lo
    lab = 5 if span <= 40 else 10
    minor = 1 if span <= 40 else 2
    return lab, minor


def boxplot(groups, lo, hi, unit="", width=380, show_grid=True, lab=None):
    """groups=[(ラベル, (最小, Q1, 中央, Q3, 最大))]。横向きの箱ひげ図（目盛りつき）。"""
    lab0, minor = _scale(lo, hi)
    lab = lab or lab0
    L, R = 54, 14
    W = width
    rh = 38
    H = rh * len(groups) + 40
    X = lambda v: L + (float(v) - lo) / (hi - lo) * (W - L - R)  # noqa: E731
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="serif" font-size="12">']
    top, bot = 6, rh * len(groups) + 8
    if show_grid:
        v = lo
        while v <= hi:
            col = "#999" if v % lab == 0 else "#ccc"
            o.append(f'<line x1="{X(v):.1f}" y1="{top}" x2="{X(v):.1f}" y2="{bot}" stroke="{col}" stroke-width="0.5"/>')
            v += minor
    o.append(f'<line x1="{X(lo):.1f}" y1="{bot}" x2="{X(hi):.1f}" y2="{bot}" stroke="#000" stroke-width="1"/>')
    v = lo
    while v <= hi:
        h = 5 if v % lab == 0 else 3
        o.append(f'<line x1="{X(v):.1f}" y1="{bot}" x2="{X(v):.1f}" y2="{bot + h}" stroke="#000" stroke-width="0.8"/>')
        if v % lab == 0:
            o.append(f'<text x="{X(v):.1f}" y="{bot + 17}" text-anchor="middle" font-size="11">{v}</text>')
        v += minor
    if unit:
        o.append(f'<text x="{W - 4}" y="{bot + 31}" text-anchor="end" font-size="11">（{unit}）</text>')
    for i, (name, f) in enumerate(groups):
        cy = top + rh * i + rh / 2
        mn, q1, md, q3, mx = f
        o.append(f'<text x="6" y="{cy + 4:.1f}" font-size="12">{name}</text>')
        o.append(f'<line x1="{X(mn):.1f}" y1="{cy:.1f}" x2="{X(q1):.1f}" y2="{cy:.1f}" stroke="#000" stroke-width="1.2"/>')
        o.append(f'<line x1="{X(q3):.1f}" y1="{cy:.1f}" x2="{X(mx):.1f}" y2="{cy:.1f}" stroke="#000" stroke-width="1.2"/>')
        for v in (mn, mx):
            o.append(f'<line x1="{X(v):.1f}" y1="{cy - 6:.1f}" x2="{X(v):.1f}" y2="{cy + 6:.1f}" stroke="#000" stroke-width="1.2"/>')
        o.append(f'<rect x="{X(q1):.1f}" y="{cy - 11:.1f}" width="{X(q3) - X(q1):.1f}" height="22" fill="#fff" stroke="#000" stroke-width="1.2"/>')
        o.append(f'<line x1="{X(md):.1f}" y1="{cy - 11:.1f}" x2="{X(md):.1f}" y2="{cy + 11:.1f}" stroke="#000" stroke-width="1.6"/>')
    o.append("</svg>")
    return "".join(o)


def histogram(edges, counts, unit="", width=360, L=34, R=12):
    n = len(counts)
    T, B = 22, 34
    H = 180
    ymax = max(counts)
    ystep = 1 if ymax <= 8 else 2
    ytop = ymax + (ystep - ymax % ystep if ymax % ystep else 0)
    X = lambda i: L + i / n * (width - L - R)  # noqa: E731
    Y = lambda c: T + (1 - c / ytop) * (H - T - B)  # noqa: E731
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {H}" width="{width}" height="{H}" font-family="serif" font-size="11">']
    for c in range(0, ytop + 1, ystep):
        o.append(f'<line x1="{L}" y1="{Y(c):.1f}" x2="{width - R}" y2="{Y(c):.1f}" stroke="#ccc" stroke-width="0.5"/>')
        o.append(f'<text x="{L - 4}" y="{Y(c) + 4:.1f}" text-anchor="end">{c}</text>')
    for i, c in enumerate(counts):
        if c:
            o.append(f'<rect x="{X(i):.1f}" y="{Y(c):.1f}" width="{X(i + 1) - X(i):.1f}" height="{Y(0) - Y(c):.1f}" fill="#e6e6e6" stroke="#000" stroke-width="1"/>')
    o.append(f'<line x1="{L}" y1="{Y(0):.1f}" x2="{width - R}" y2="{Y(0):.1f}" stroke="#000"/>')
    o.append(f'<line x1="{L}" y1="{T}" x2="{L}" y2="{Y(0):.1f}" stroke="#000"/>')
    for i, e in enumerate(edges):
        o.append(f'<text x="{X(i):.1f}" y="{Y(0) + 14:.1f}" text-anchor="middle">{e}</text>')
    o.append(f'<text x="{L + 2}" y="{T - 10}" text-anchor="start" font-size="10">（人）</text>')
    if unit:
        o.append(f'<text x="{width - 2}" y="{Y(0) + 28:.1f}" text-anchor="end">（{unit}）</text>')
    o.append("</svg>")
    return "".join(o)


def lohi(fs):
    a = min(f[0] for f in fs)
    b = max(f[4] for f in fs)
    lo = int(a) // 5 * 5
    hi = -(-int(b + Fr(1, 2)) // 5) * 5
    if hi == lo:
        hi += 5
    return lo, hi


# ----------------------------------------------------------------------
# 授業プリント
# ----------------------------------------------------------------------

EX_DATA = [3, 5, 6, 8, 9, 11, 12, 14, 15, 17, 20]
EX_F = five(EX_DATA)

LESSON = lesson(
    goals=["四分位数・四分位範囲の意味を理解し、データから求めることができる。",
           "箱ひげ図をかき、箱ひげ図から最小値・四分位数・最大値を読み取ることができる。",
           "複数のデータの分布を箱ひげ図で比べ、根拠を示して傾向を説明できる。"],
    duration=100,
    readiness=["データを小さい順に並べ、中央値と範囲を求められる（1年）。", "ヒストグラムから分布の形（山の位置・広がり）を読み取れる（1年）。",
               "2つの数の平均（真ん中の値）を計算できる。"],
    flow=[("導入：平均値が同じでも", 10, "平均値が等しい2つのクラスの得点の散らばりのちがいを考える"),
          ("四分位数", 25, "四分位数の求め方（データが奇数個・偶数個）、四分位範囲（例題1）"),
          ("箱ひげ図", 25, "箱ひげ図のかき方と読み方、箱の中にふくまれるデータの割合（例題2）"),
          ("分布の比較", 25, "複数の箱ひげ図の比較、ヒストグラムとの対応、読み取れること・読み取れないこと（例題3）"),
          ("まとめと確認", 15, "確認問題と問題プリントの指示")],
    sections=[
        intro("in1", "散らばりのようすを比べるには",
              "1年では、データの分布をヒストグラムで表し、平均値・中央値・最頻値などの代表値で特徴をとらえた。しかし、代表値が同じでも、データの散らばりのようすが大きく異なることがある。範囲（最大値−最小値）は散らばりの目安になるが、極端な値が1つあるだけで大きく変わってしまう。この単元では、データを4つに区切る値（四分位数）を使って、散らばりのようすをより確かにとらえる方法を学ぶ。",
              bullets=["範囲は最大値と最小値の2つの値だけで決まる。", "データの中心付近の約半分が、どれくらいの幅に集まっているかを調べよう。"],
              points=[tp("平均値が同じ2つのデータ（例：どちらも平均 10 点）を板書し、「どちらのクラスの方が得点がそろっているか」を予想させる。",
                         ask="範囲だけで比べてよいか。1人だけ極端に高い得点の人がいたらどうなるか。", expect="範囲が大きくなってしまい、全体のようすを表さない。", timing="導入")]),
        definition("df1", "四分位数と四分位範囲",
                   "データを小さい順に並べ、個数が等しくなるように4つに分けたときの3つの区切りの値を四分位数という。小さい方から第1四分位数、第2四分位数（中央値）、第3四分位数という。",
                   formula="$$(\\text{四分位範囲})=(\\text{第3四分位数})-(\\text{第1四分位数})$$",
                   conditions=["まず中央値を求め、データを前半と後半に分ける。データの個数が奇数のときは、中央値を前半にも後半にもふくめない。",
                               "前半のデータの中央値が第1四分位数、後半のデータの中央値が第3四分位数。",
                               "四分位範囲は、中央付近の約半分のデータの散らばりの程度を表し、極端な値の影響を受けにくい。"],
                   points=[tp("前半・後半の中央値を求めるとき、さらに個数が偶数なら2つの値の平均をとることを、具体例で確認する。",
                              caution="データを小さい順に並べないまま4つに分けてしまう誤りが多い。")]),
        definition("df2", "箱ひげ図",
                   "最小値・第1四分位数・中央値・第3四分位数・最大値の5つの値を、1つの図に表したものを箱ひげ図という。",
                   conditions=["第1四分位数から第3四分位数までを長方形（箱）で表し、中央値の位置に線をひく。",
                               "最小値から箱まで、箱から最大値まで線（ひげ）をひく。",
                               "箱の長さが四分位範囲、左右のひげの端から端までの長さが範囲を表す。"],
                   figure=figure("箱ひげ図の各部分の名前", boxplot([("", EX_F)], 0, 20)),
                   points=[tp("箱ひげ図の各部分が、どの値に対応しているかを図に書きこませる。", ask="箱の中には、全体のおよそ何割のデータがふくまれるか。", expect="およそ半分（50%）。")]),
        derivation("dv1", "四分位数の求め方と、箱にふくまれるデータの割合",
                   ["データを小さい順に並べる。例：$3,5,6,8,9,11,12,14,15,17,20$（11 個）。",
                    "中央値は 6 番目の $11$。中央値を除いて、前半 $3,5,6,8,9$ と後半 $12,14,15,17,20$ に分ける。",
                    "前半の中央値 $6$ が第1四分位数、後半の中央値 $15$ が第3四分位数。四分位範囲は $15-6=9$。",
                    "第1四分位数・中央値・第3四分位数でデータはほぼ同じ個数ずつ4つに分かれるので、それぞれの区間には全体の約 25% ずつのデータがふくまれる。",
                    "したがって、箱（第1四分位数から第3四分位数まで）には全体の約 50% のデータがふくまれる。箱やひげの長さは、データの個数ではなく、散らばりの大きさを表している。"],
                   points=[tp("「区間の長さ」と「区間にふくまれるデータの個数」は別のものであることを強調する。",
                              caution="ひげが長い方にデータが多いと誤解する生徒が多い。どの区間にも約 25% ずつふくまれることを確認する。")]),
        example("ex1", "例題1　データが偶数個のとき",
                "次のデータは，10人の生徒の小テストの得点である。四分位数と四分位範囲を求めなさい。\n$4,\\ 7,\\ 8,\\ 10,\\ 11,\\ 13,\\ 14,\\ 16,\\ 17,\\ 19$（点）",
                ["データは小さい順に並んでいる。10 個なので、中央値は 5 番目と 6 番目の平均で $(11+13)\\div2=12$ 点。",
                 "前半は $4,7,8,10,11$、後半は $13,14,16,17,19$（それぞれ 5 個）。",
                 "第1四分位数は前半の中央値 $8$ 点、第3四分位数は後半の中央値 $16$ 点。",
                 "四分位範囲は $16-8=8$ 点。"],
                "第1四分位数 8 点，中央値 12 点，第3四分位数 16 点，四分位範囲 8 点",
                thinking="まず中央値でデータを前半・後半に分ける。偶数個なら、ちょうど半分ずつに分かれる。",
                points=[tp("偶数個と奇数個で、前半・後半の分け方がどう変わるかを比べさせる。")],
                misconceptions=[("中央値の 12 を前半にも後半にも入れて考える", "12 はデータの値ではないので、前半・後半は 5 個ずつ")]),
        example("ex2", "例題2　箱ひげ図をかく・読む",
                "例題1のデータの箱ひげ図をかきなさい。また，箱ひげ図から範囲を求めなさい。",
                ["5つの値は、最小値 4、第1四分位数 8、中央値 12、第3四分位数 16、最大値 19。",
                 "数直線の上に、8 から 16 までの箱をかき、12 の位置に線をひく。",
                 "箱の左はしから 4 まで、右はしから 19 までひげをひく。",
                 "範囲は $19-4=15$ 点。"],
                "下の図，範囲は 15 点",
                figure=figure("例題1のデータの箱ひげ図", boxplot([("", (Fr(4), Fr(8), Fr(12), Fr(16), Fr(19)))], 0, 20, unit="点")),
                points=[tp("目盛りを正確に読み、5つの値を対応させる練習をさせる。")]),
        example("ex3", "例題3　箱ひげ図で比べる",
                "右の図は，A組とB組（どちらも31人）の数学の小テストの得点を箱ひげ図に表したものである。B組の方が得点の高い生徒が多いといえる理由を，箱ひげ図をもとに説明しなさい。",
                ["A組の中央値は 11 点、B組の中央値は 14 点。", "B組の第1四分位数 11 点は A組の中央値と同じで、B組では約 75% の生徒が 11 点以上である。",
                 "A組で 11 点以上の生徒は約半分なので、B組の方が得点の高い生徒が多いといえる。"],
                "B組は中央値・四分位数がいずれも A組より大きく，B組では約 75% の生徒が 11 点以上であるが，A組では約 50% である。",
                thinking="中央値や箱の位置を比べる。何%の生徒がどこより上にいるかを言葉にする。",
                figure=figure("A組とB組の得点の箱ひげ図", boxplot([("A組", (Fr(3), Fr(7), Fr(11), Fr(14), Fr(19))), ("B組", (Fr(5), Fr(11), Fr(14), Fr(17), Fr(20)))], 0, 20, unit="点")),
                points=[tp("箱ひげ図から読み取れないこと（平均値、ちょうど何人か）と、読み取れること（約何%が〇点以上）を区別させる。", timing="例題3の後")]),
        board("bd1", "板書案",
              [("① 四分位数", ["小さい順に並べる", "中央値で前半・後半に分ける（奇数個は中央値を除く）", "前半の中央値＝第1四分位数", "後半の中央値＝第3四分位数"]),
               ("② 箱ひげ図", ["最小値・Q1・中央値・Q3・最大値", "箱の長さ＝四分位範囲（Q3−Q1）", "ひげの端から端＝範囲", "各区間に約 25% ずつ"]),
               ("③ 比べ方", ["中央値・箱の位置で全体の傾向", "箱の長さで中央付近の散らばり", "読み取れない：平均値・人数の細かい分布", "根拠を「約〇%が…」で説明"])],
              points=[tp("②の箱ひげ図は、①の例のデータからその場でかき、5つの値と図の部分を矢印で結んで示す。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("四分位数を求める手順（並べる→中央値→前半・後半→それぞれの中央値）を毎回声に出して確認させる。"),
               tp("箱ひげ図とヒストグラムを並べて示し、山が左に寄ると箱も左に寄ることなどを確かめさせる。",
                  ask="山が1つで左右対称なヒストグラムの箱ひげ図はどんな形になるか。", expect="中央値が箱のほぼ真ん中にあり、左右のひげの長さも同じくらいになる。"),
               tp("比べる問題では、「中央値が大きい」だけでなく「だから約半分以上が〇点以上」まで言わせる。"),
               tp("入試では、箱ひげ図から正しく読み取れる文をすべて選ぶ問題が多い。読み取れない文（平均値・最頻値など）を見分ける練習をする。", timing="まとめの前")],
              misconceptions=[("箱が長い方がデータの個数が多い", "箱の中のデータは、どちらも全体の約半分。長さは散らばりの大きさを表す"),
                              ("箱の中の線は平均値", "箱の中の線は中央値"),
                              ("奇数個のデータで、中央値を前半にも後半にもふくめる", "中学校では中央値を除いて前半・後半に分ける")]),
        summary("sm1", "まとめ",
                ["四分位数は、データを4等分する3つの値（第1四分位数・中央値・第3四分位数）。", "四分位範囲＝第3四分位数−第1四分位数。極端な値の影響を受けにくい。",
                 "箱ひげ図は5つの値で分布を表す。箱には約半分のデータがふくまれる。", "複数のデータは、箱ひげ図を並べて位置と広がりを比べる。"]),
        check("ck1", "確認問題",
              [("データ $2,4,5,7,8,10,13$ の第1四分位数と第3四分位数を求めなさい。", "中央値 7 を除き、前半 $2,4,5$ の中央値 4、後半 $8,10,13$ の中央値 10"),
               ("前の問題のデータの四分位範囲を求めなさい。", "$10-4=6$"),
               ("箱ひげ図の箱にふくまれるデータは，全体のおよそ何%か。", "およそ 50%")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

QNAME = {1: "第1四分位数", 2: "中央値", 3: "第3四分位数"}


@gen("basic_check", 6, ["computation"])
def a_quartiles(r):
    name, u, lo, hi = ctx(r)
    n = r.choice([7, 8, 9, 10, 11, 12, 13])
    xs = int_data(r, n, lo, hi)
    n = len(xs)
    s = sorted(xs)
    f = five(xs)
    k = r.choice([1, 2, 3, 1, 3])
    v = f[k]
    shown = xs if r.random() < 0.6 else s
    lower, upper = s[:n // 2], s[(n + 1) // 2:]
    stem = f"次のデータは，ある中学校の生徒{n}人の{name}を調べたものである。このデータの{QNAME[k]}を求めなさい。\n${lst(shown)}$（単位：{u}）"
    return MARK(stem, v, f"小さい順に並べると ${lst(s)}$。{QNAME[k]}は ${dec(v)}$ {u}。", fpy(v), d=1,
                ap="まずデータを小さい順に並べる。中央値で前半と後半に分け，前半の中央値が第1四分位数，後半の中央値が第3四分位数。",
                steps=[f"小さい順に並べる：${lst(s)}$。", pos_txt(n) + "。", f"前半 ${lst(lower)}$，後半 ${lst(upper)}$。",
                       f"第1四分位数 ${dec(f[1])}$，中央値 ${dec(f[2])}$，第3四分位数 ${dec(f[3])}$。"],
                alt=["並べたデータに区切りの線を入れ，4つの組の個数がそろっているかを確かめる。"],
                pc=[("小さい順に並べ，前半・後半に正しく分けている", 1), ("正しい値を求めている", 1)],
                pit=["並べ替えずに求める。", "データが奇数個のとき，中央値を前半・後半にふくめてしまう。"])


@gen("basic_check", 5, ["computation", "concept"])
def a_iqr(r):
    name, u, lo, hi = ctx(r)
    kind = r.choice(["iqr", "iqr", "range", "five"])
    if kind == "five":
        mn = r.randint(lo, lo + 4)
        q1 = mn + r.randint(1, 5)
        md = q1 + r.randint(1, 5)
        q3 = md + r.randint(1, 5)
        mx = q3 + r.randint(1, 6)
        ask = r.choice(["iqr", "range"])
        v = q3 - q1 if ask == "iqr" else mx - mn
        tbl = table([[str(mn), str(q1), str(md), str(q3), str(mx)]], header=["最小値", "第1四分位数", "中央値", "第3四分位数", "最大値"], caption=f"（単位：{u}）{FAKE}")
        stem = f"右の表は，ある学年の生徒の{name}について，最小値・四分位数・最大値をまとめたものである。このデータの{'四分位範囲' if ask == 'iqr' else '範囲'}を求めなさい。"
        e = f"{'四分位範囲＝第3四分位数−第1四分位数' if ask == 'iqr' else '範囲＝最大値−最小値'}で ${v}$ {u}。"
        st = [e]
        expr = f"{q3}-{q1}" if ask == "iqr" else f"{mx}-{mn}"
        return MARK(stem, v, e, expr, d=1, tbl=tbl,
                    ap="四分位範囲は「第3四分位数−第1四分位数」，範囲は「最大値−最小値」。",
                    steps=st, alt=["箱ひげ図をかいて，箱の長さ（またはひげの端から端）を目盛りで確かめる。"],
                    pc=[("どの値の差をとるかを正しく判断している", 1), ("正しく計算している", 1)],
                    pit=["四分位範囲と範囲を取り違える。"])
    n = r.choice([8, 9, 10, 11, 12, 14, 15])
    xs = int_data(r, n, lo, hi)
    n = len(xs)
    s = sorted(xs)
    f = five(xs)
    if kind == "iqr":
        v = f[3] - f[1]
        nm = "四分位範囲"
        st = [f"小さい順に並べる：${lst(s)}$。", pos_txt(n) + "。", f"第1四分位数 ${dec(f[1])}$，第3四分位数 ${dec(f[3])}$。", f"四分位範囲 ${dec(f[3])}-{dec(f[1])}={dec(v)}$。"]
        expr = f"{fpy(f[3])}-{fpy(f[1])}"
    else:
        v = f[4] - f[0]
        nm = "範囲"
        st = [f"最大値は ${s[-1]}$，最小値は ${s[0]}$。", f"範囲 ${s[-1]}-{s[0]}={v}$。"]
        expr = f"{s[-1]}-{s[0]}"
    stem = f"次のデータは，生徒{n}人の{name}である。このデータの{nm}を求めなさい。\n${lst(xs)}$（単位：{u}）"
    return MARK(stem, v, f"{nm}は ${dec(v)}$ {u}。", expr, d=1,
                ap="四分位範囲は「第3四分位数−第1四分位数」，範囲は「最大値−最小値」。まずデータを小さい順に並べる。",
                steps=st, alt=["範囲と四分位範囲の両方を求め，四分位範囲の方が小さく（等しく）なることを確かめる。"],
                pc=[("必要な値を正しく求めている", 1), ("差を正しく計算している", 1)],
                pit=["四分位範囲と範囲を取り違える。", "並べ替えずに最初と最後の値の差をとる。"])


def rand5(r, lo, hi):
    """lo〜hi の範囲の、5つの値がすべて異なる整数の組。"""
    span = hi - lo
    while True:
        v = sorted(r.sample(range(lo, hi + 1), 5))
        if v[4] - v[0] >= span * 0.45:
            return tuple(Fr(x) for x in v)


@gen("basic_check", 5, ["computation", "concept"])
def a_box_read(r):
    name, u, lo, hi = ctx(r)
    lo = lo // 5 * 5
    hi = -(-hi // 5) * 5
    f = rand5(r, lo, hi)
    k = r.choice(["min", "q1", "med", "q3", "max", "iqr", "range", "iqr"])
    nm = {"min": "最小値", "q1": "第1四分位数", "med": "中央値", "q3": "第3四分位数", "max": "最大値", "iqr": "四分位範囲", "range": "範囲"}[k]
    v = {"min": f[0], "q1": f[1], "med": f[2], "q3": f[3], "max": f[4], "iqr": f[3] - f[1], "range": f[4] - f[0]}[k]
    fig = figure(f"{name}の箱ひげ図", boxplot([("", f)], lo, hi, unit=u))
    stem = f"右の図は，ある中学校の2年生の{name}を箱ひげ図に表したものである。このデータの{nm}を求めなさい。"
    expr = {"iqr": f"{f[3]}-{f[1]}", "range": f"{f[4]}-{f[0]}"}.get(k, str(v))
    return MARK(stem, v, f"箱ひげ図から読み取ると，{nm}は ${dec(v)}$ {u}。", expr, d=1, fig=fig,
                ap="箱ひげ図の左のひげの端が最小値，箱の左はしが第1四分位数，箱の中の線が中央値，箱の右はしが第3四分位数，右のひげの端が最大値。",
                steps=[f"5つの値を読み取る：最小値 ${f[0]}$，第1四分位数 ${f[1]}$，中央値 ${f[2]}$，第3四分位数 ${f[3]}$，最大値 ${f[4]}$。", f"{nm}は ${dec(v)}$ {u}。"],
                alt=["目盛りを1つずつ数えて，読み取った値が正しいか確かめる。"],
                pc=[("図の各部分が表す値を正しく理解している", 1), ("正しい値を読み取っている", 1)],
                pit=["箱の長さ（四分位範囲）とひげの端から端（範囲）を取り違える。"])


@gen("basic_check", 4, ["concept", "condition_check"])
def a_terms(r):
    kind = r.choice(["box", "line", "iqr", "whisker", "pct", "q2"])
    if kind == "box":
        stem = "箱ひげ図の箱の部分が表している範囲として最も適するものを，" + SEL4
        right = "第1四分位数から第3四分位数まで"
        cands = [("最小値から最大値まで", "これは左右のひげの端から端までで，範囲を表す。", "箱とひげの取り違え"),
                 ("最小値から中央値まで", "箱の左はしは最小値ではなく第1四分位数である。", "部分の名前の誤解"),
                 ("平均値を中心とした範囲", "箱ひげ図に平均値はかかれない。", "平均値と中央値の混同"),
                 ("第1四分位数から中央値まで", "箱は第3四分位数まで続いている。", "部分の名前の誤解")]
        e = "箱は第1四分位数から第3四分位数までを表す。その長さが四分位範囲である。"
    elif kind == "line":
        stem = "箱ひげ図で，箱の中にひかれた線が表している値として最も適するものを，" + SEL4
        right = "中央値"
        cands = [("平均値", "箱ひげ図の箱の中の線は中央値を表す。平均値は箱ひげ図に表されない。", "平均値と中央値の混同"),
                 ("最頻値", "最頻値は箱ひげ図に表されない。", "代表値の混同"),
                 ("四分位範囲", "四分位範囲は箱の長さで表される。", "値と長さの混同"),
                 ("範囲", "範囲はひげの端から端までの長さである。", "値と長さの混同")]
        e = "箱の中の線は中央値（第2四分位数）を表す。"
    elif kind == "iqr":
        stem = "四分位範囲を求める式として正しいものを，" + SEL4
        right = "（第3四分位数）−（第1四分位数）"
        cands = [("（最大値）−（最小値）", "これは範囲である。", "範囲との混同"),
                 ("（第3四分位数）−（中央値）", "これは箱の右半分の長さである。", "定義の誤解"),
                 ("（第3四分位数）＋（第1四分位数）", "差ではなく和になっている。", "計算の誤り"),
                 ("（最大値）−（第1四分位数）", "最大値を使うのは誤り。", "定義の誤解")]
        e = "四分位範囲＝第3四分位数−第1四分位数。"
    elif kind == "whisker":
        stem = "箱ひげ図の左右のひげの端が表している値の組み合わせとして正しいものを，" + SEL4
        right = "左はし：最小値　右はし：最大値"
        cands = [("左はし：第1四分位数　右はし：第3四分位数", "これは箱の左右のはしである。", "箱とひげの取り違え"),
                 ("左はし：最大値　右はし：最小値", "数直線は右ほど大きいので，左が最小値である。", "数直線の向きの誤解"),
                 ("左はし：平均値　右はし：中央値", "ひげの端は最小値と最大値である。", "代表値の混同")]
        e = "左のひげの端は最小値，右のひげの端は最大値。"
    elif kind == "pct":
        p = r.choice([("最小値から第1四分位数まで", "約25%"), ("第1四分位数から第3四分位数まで", "約50%"), ("中央値から最大値まで", "約50%"),
                       ("最小値から第3四分位数まで", "約75%"), ("第3四分位数から最大値まで", "約25%"), ("第1四分位数から最大値まで", "約75%")])
        stem = f"箱ひげ図で，{p[0]}の区間にふくまれるデータの個数は，全体のおよそ何%か。最も適するものを，" + SEL4
        right = p[1]
        allp = ["約25%", "約50%", "約75%", "約100%", "約10%"]
        cands = [(x, f"四分位数でデータはほぼ同じ個数ずつ4つに分かれ，各区間に約25%ずつふくまれる。{p[0]}は{p[1]}。", "区間とデータの割合の関係の誤解") for x in allp if x != p[1]]
        e = f"各区間に約25%ずつなので，{p[0]}は{p[1]}。"
    else:
        stem = "四分位数について述べた文として正しいものを，" + SEL4
        right = "第2四分位数は中央値と同じ値である。"
        cands = [("第2四分位数は平均値と同じ値である。", "第2四分位数は中央値である。", "平均値と中央値の混同"),
                 ("第1四分位数は，いつもデータの最小値と等しい。", "第1四分位数は前半のデータの中央値である。", "定義の誤解"),
                 ("四分位数を求めるとき，データを小さい順に並べる必要はない。", "並べなければ4つに分けた区切りが求められない。", "手順の誤解"),
                 ("第3四分位数は，データの最大値の4分の3の値である。", "最大値の 3/4 倍ではなく，後半のデータの中央値である。", "「4分の3」の誤解")]
        e = "四分位数は第1・第2・第3の3つで，第2四分位数は中央値である。"
    return MC(stem, right, cands, e, d=1,
              ap="箱ひげ図の5つの値（最小値・第1四分位数・中央値・第3四分位数・最大値）と，各区間に約25%ずつのデータがふくまれることを思い出す。",
              steps=["箱ひげ図の各部分と5つの値を対応させる。", e],
              alt=["小さい例（8個程度のデータ）で箱ひげ図をかき，確かめる。"],
              pc=[("用語の意味を正しく理解している", 1), ("正しいものを選んでいる", 1)],
              pit=["箱の中の線を平均値と考える。", "範囲と四分位範囲を取り違える。"])


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 5, ["computation", "condition_check"])
def b_box_choose(r):
    name, u, lo, hi = ctx(r)
    n = r.choice([9, 10, 11, 12, 13])
    xs = int_data(r, n, lo, hi)
    n = len(xs)
    s = sorted(xs)
    f = five(xs)
    cands = []
    if n % 2:
        lo2, up2 = s[:n // 2 + 1], s[n // 2:]
        cands.append(((f[0], med(lo2), f[2], med(up2), f[4]), "中央値を前半・後半の両方にふくめて四分位数を求めている。", "四分位数の求め方の誤り"))
    cands.append(((f[0], f[1], Fr(sum(s), n), f[3], f[4]) if Fr(sum(s), n) not in (f[1], f[3]) and f[1] < Fr(sum(s), n) < f[3] else None, "箱の中の線が平均値になっている。中央値をかく。", "平均値と中央値の混同"))
    cands.append(((Fr(s[1]), f[1], f[2], f[3], Fr(s[-2])), "ひげの端が最小値・最大値になっていない。", "ひげの意味の誤解"))
    cands.append(((f[0], f[1] - 1, f[2], f[3] + 1, f[4]), "第1四分位数・第3四分位数の位置がずれている。", "四分位数の求め方の誤り"))
    cands.append(((f[0], f[1], f[2] + 1, f[3], f[4]) if f[2] + 1 < f[3] else None, "中央値の位置がずれている。", "中央値の求め方の誤り"))
    cands.append(((f[0], f[1] + 1, f[2], f[3] - 1, f[4]) if f[1] + 1 < f[2] < f[3] - 1 else None, "第1四分位数・第3四分位数の位置がずれている。", "四分位数の求め方の誤り"))
    seen = {f}
    wr = []
    for c, why, mis in cands:
        if c is None or c in seen or not (c[0] <= c[1] <= c[2] <= c[3] <= c[4]):
            continue
        seen.add(c)
        wr.append((c, why, mis))
        if len(wr) == 3:
            break
    assert len(wr) == 3
    pos = r.randrange(4)
    order = wr[:pos] + [(f, None, None)] + wr[pos:]
    lo_, hi_ = lohi([o[0] for o in order])
    fig = figure(f"{name}の箱ひげ図の候補 ア〜エ", boxplot([(KANA[i], o[0]) for i, o in enumerate(order)], lo_, hi_, unit=u))
    why = {KANA[i]: (o[1], o[2]) for i, o in enumerate(order) if i != pos}
    stem = f"次のデータは，生徒{n}人の{name}である。このデータを箱ひげ図に表したものとして最も適するものを，右の図のア〜エの中から1つ選んだものを，" + SEL4 + f"\n${lst(xs)}$（単位：{u}）"
    return mc(stem, list(KANA), f"5つの値は 最小値 ${f[0]}$，第1四分位数 ${dec(f[1])}$，中央値 ${dec(f[2])}$，第3四分位数 ${dec(f[3])}$，最大値 ${f[4]}$ なので{KANA[pos]}。",
              d=2, p=4, keep=True, ai=pos, why=why, fig=fig,
              ap="データから5つの値（最小値・第1四分位数・中央値・第3四分位数・最大値）を求め，箱ひげ図の各部分と照らし合わせる。",
              steps=[f"小さい順に並べる：${lst(s)}$。", pos_txt(n) + "。",
                     f"最小値 ${f[0]}$，第1四分位数 ${dec(f[1])}$，中央値 ${dec(f[2])}$，第3四分位数 ${dec(f[3])}$，最大値 ${f[4]}$。", f"これに合うのは{KANA[pos]}。"],
              alt=["まず最小値・最大値で候補をしぼり，次に中央値，最後に四分位数で決めると速い。"],
              pc=[("5つの値を正しく求めている", 2), ("正しい箱ひげ図を選んでいる", 2)],
              pit=["奇数個のデータで中央値をふくめて四分位数を求める。", "箱の中の線を平均値と考える。"])


def _groups_stats(r, k, lo, hi):
    out = []
    while len(out) < k:
        f = rand5(r, lo, hi)
        if all(f[2] != g[2] and f[3] - f[1] != g[3] - g[1] and f[4] - f[0] != g[4] - g[0] for g in out):
            out.append(f)
    return out


def _statements(r, names, fs, u, n):
    """箱ひげ図についての文（文, 正誤 or None=読み取れない, 理由）。"""
    out = []
    i, j = r.sample(range(len(fs)), 2)
    a, b = fs[i], fs[j]
    A, B = names[i], names[j]
    rngA, rngB = a[4] - a[0], b[4] - b[0]
    out.append((f"{A}の範囲は，{B}の範囲より大きい。", rngA > rngB, f"範囲は {A} が ${rngA}$ {u}，{B} が ${rngB}$ {u}。"))
    iqA, iqB = a[3] - a[1], b[3] - b[1]
    out.append((f"{A}の四分位範囲は，{B}の四分位範囲より大きい。", iqA > iqB, f"四分位範囲は {A} が ${iqA}$ {u}，{B} が ${iqB}$ {u}。"))
    out.append((f"{A}の中央値は，{B}の中央値より大きい。", a[2] > b[2], f"中央値は {A} が ${a[2]}$ {u}，{B} が ${b[2]}$ {u}。"))
    v = r.choice([a[2], a[3], a[1], a[2] + 1, a[2] - 1])
    out.append((f"{A}では，{v}{u}以上の生徒が半数以上いる。", a[2] >= v,
                f"{n}人（奇数）なので中央値は小さい方から ${(n + 1) // 2}$ 番目の値。{A}の中央値は ${a[2]}$ {u}なので，{'半数以上が' + str(v) + u + '以上である' if a[2] >= v else str(v) + u + '以上の生徒は半数未満である'}。"))
    out.append((f"{A}の最大値は，{B}の最大値より大きい。", a[4] > b[4], f"最大値は {A} が ${a[4]}$ {u}，{B} が ${b[4]}$ {u}。"))
    out.append((f"{A}の平均値は，{B}の平均値より大きい。", None, "平均値は箱ひげ図からは読み取れない。"))
    out.append((f"{A}で，ちょうど{a[2]}{u}の生徒は1人だけである。", None, "同じ値の生徒が何人いるかは，箱ひげ図からは読み取れない。"))
    out.append((f"{A}では，{a[3]}{u}以上の生徒は約4分の1である。", True, f"{a[3]} {u}は{A}の第3四分位数なので，それ以上の生徒は約25%。"))
    out.append((f"{A}では，{a[1]}{u}以下の生徒は約半数である。", False, f"{a[1]} {u}は第1四分位数なので，それ以下の生徒は約25%である。"))
    return out


@gen("standard_practice", 5, ["application", "written_reasoning"])
def b_compare(r):
    name, u, lo, hi = ctx(r)
    lo = lo // 5 * 5
    hi = -(-hi // 5) * 5
    k = r.choice([2, 3])
    names = ["A組", "B組", "C組"][:k]
    n = r.choice([29, 31, 33, 35])
    fs = _groups_stats(r, k, lo, hi)
    S = _statements(r, names, fs, u, n)
    trues = [s for s in S if s[1] is True]
    falses = [s for s in S if s[1] is not True]
    assert trues and len(falses) >= 3
    right = r.choice(trues)
    r.shuffle(falses)
    cands = [(t, ("読み取れない。" if v is None else "誤り。") + w, "箱ひげ図から読み取れることの判断の誤り" if v is None else "箱ひげ図の読み誤り") for t, v, w in falses]
    fig = figure(f"{'，'.join(names)}の{name}の箱ひげ図", boxplot(list(zip(names, fs)), lo, hi, unit=u))
    stem = f"右の図は，ある中学校の{'，'.join(names)}（各組{n}人）の{name}を箱ひげ図に表したものである。この図から読み取れることとして正しいものを，" + SEL4
    return MC(stem, right[0], cands, right[2], d=3, p=4, fig=fig,
              ap="各組の5つの値を読み取り，範囲・四分位範囲・中央値を計算して比べる。平均値や同じ値の人数など，箱ひげ図に表れないことは判断できない。",
              steps=["それぞれの組の最小値・四分位数・中央値・最大値を読み取る。", "選択肢の文ごとに，必要な値を計算して比べる。", f"正しいのは「{right[0]}」。{right[2]}"],
              alt=["「半数以上」は中央値，「約4分の1」は第1・第3四分位数に注目すると，読み取りが速い。"],
              pc=[("必要な値を正しく読み取っている", 2), ("正しい文を選んでいる", 2)],
              pit=["平均値を箱ひげ図から読み取ろうとする。", "箱の長さで人数を比べる。"])


@gen("standard_practice", 5, ["computation", "concept"])
def b_freq_table(r):
    name, u, lo, hi = ctx(r)
    w = 5 if hi - lo <= 30 else 10
    base = lo // w * w
    m = r.choice([5, 6, 7])
    edges = [base + w * i for i in range(m + 1)]
    for _ in range(200):
        cnt = [r.randint(1, 9) for _ in range(m)]
        n = sum(cnt)
        k = r.choice([1, 2, 3])
        ranks = {2: ([n // 2] if n % 2 else [n // 2, n // 2 + 1])}
        h = n // 2
        lowr = list(range(1, h + 1))
        upr = list(range(n - h + 1, n + 1))
        ranks[1] = [lowr[h // 2]] if h % 2 else [lowr[h // 2 - 1], lowr[h // 2]]
        ranks[3] = [upr[h // 2]] if h % 2 else [upr[h // 2 - 1], upr[h // 2]]
        if n % 2:
            ranks[2] = [h + 1]

        def cls(rk):
            c = 0
            for i, x in enumerate(cnt):
                c += x
                if rk <= c:
                    return i
        cl = {cls(x) for x in ranks[k]}
        if len(cl) == 1:
            ci = cl.pop()
            break
    else:
        raise AssertionError
    lab = [f"{edges[i]}{u}以上{edges[i + 1]}{u}未満" for i in range(m)]
    rows = [[f"{edges[i]}以上〜{edges[i + 1]}未満", str(cnt[i])] for i in range(m)] + [["合計", str(n)]]
    tbl = table(rows, header=[f"階級（{u}）", "度数（人）"], caption=FAKE)
    right = lab[ci]
    cands = [(lab[i], f"{QNAME[k]}は小さい方から {'，'.join(map(str, ranks[k]))} 番目の値で，それがふくまれるのは「{right}」の階級である。", "順位と階級の対応の誤り")
             for i in sorted(range(m), key=lambda i: abs(i - ci)) if i != ci]
    cum = list(itertools.accumulate(cnt))
    stem = f"右の度数分布表は，ある中学校の2年生{n}人の{name}をまとめたものである。このデータの{QNAME[k]}がふくまれる階級として最も適するものを，" + SEL4
    return MC(stem, right, cands, f"{QNAME[k]}は小さい方から {'，'.join(map(str, ranks[k]))} 番目の値で，「{right}」の階級にふくまれる。", d=3, p=4, tbl=tbl,
              ap="データの個数から，中央値・第1四分位数・第3四分位数が小さい方から何番目の値かを求め，累積度数でその順位がふくまれる階級を探す。",
              steps=[f"{n}人なので，" + pos_txt(n) + "。", f"{QNAME[k]}は小さい方から {'，'.join(map(str, ranks[k]))} 番目の値。",
                     "累積度数：" + "，".join(f"{edges[i + 1]}{u}未満まで ${cum[i]}$ 人" for i in range(m)) + "。", f"よって「{right}」の階級。"],
              alt=["大きい方から数えて順位を確かめてもよい（第3四分位数は大きい方から数えた方が速い）。"],
              pc=[("何番目の値かを正しく求めている", 2), ("その順位がふくまれる階級を正しく選んでいる", 2)],
              pit=["度数がいちばん大きい階級（最頻値の階級）を選んでしまう。", "第1四分位数を全体の小さい方から4分の1の人数ではなく，前半の中央値として求めることを忘れる。"])


SUBS = [(), ("範囲",), ("四分位範囲",), ("中央値",), ("範囲", "四分位範囲"), ("範囲", "中央値"), ("四分位範囲", "中央値"), ("範囲", "四分位範囲", "中央値")]


def subname(sub):
    return "どれも変わらない" if not sub else "，".join(sub) + "（" + ("のみ" if len(sub) == 1 else "の" + ("3つ" if len(sub) == 3 else "2つ")) + "）"


@gen("standard_practice", 5, ["concept", "condition_check"])
def b_change(r):
    name, u, lo, hi = ctx(r)
    n = r.choice([9, 10, 11, 12])
    xs = sorted(int_data(r, n, lo, hi))
    n = len(xs)
    f0 = five(xs)
    kind = r.choice(["max", "min", "mid", "any"])
    if kind == "max":
        i = n - 1
        nv = xs[i] + r.randint(2, 8)
    elif kind == "min":
        i = 0
        nv = max(0, xs[0] - r.randint(1, 5))
        if nv == xs[0]:
            nv = xs[0] + 1
    elif kind == "mid":
        i = r.randrange(1, n - 1)
        nv = xs[i] + r.choice([-3, -2, -1, 1, 2, 3])
    else:
        i = r.randrange(n)
        nv = r.randint(lo, hi)
    assert nv != xs[i] and nv >= 0
    ys = xs[:]
    ys[i] = nv
    f1 = five(ys)
    ch = []
    if f1[4] - f1[0] != f0[4] - f0[0]:
        ch.append("範囲")
    if f1[3] - f1[1] != f0[3] - f0[1]:
        ch.append("四分位範囲")
    if f1[2] != f0[2]:
        ch.append("中央値")
    ch = tuple(ch)
    right = subname(ch)
    info = (f"範囲 ${dec(f0[4] - f0[0])}\\to{dec(f1[4] - f1[0])}$，四分位範囲 ${dec(f0[3] - f0[1])}\\to{dec(f1[3] - f1[1])}$，中央値 ${dec(f0[2])}\\to{dec(f1[2])}$")
    others = [s for s in SUBS if s != ch]
    r.shuffle(others)
    cands = [(subname(s), f"訂正の前後で，{info}。変わるのは「{right}」。", "データの変更と代表値・散らばりの関係の誤解") for s in others]
    stem = (f"次のデータは，生徒{n}人の{name}を小さい順に並べたものである。\n${lst(xs)}$（単位：{u}）\n"
            f"このうち，{xs[i]}{u}と記録されていた1人の値が誤りで，正しくは{nv}{u}であることがわかった。値を訂正したとき，範囲・四分位範囲・中央値のうち，訂正前と比べて値が変わるものをすべて選んだものとして最も適するものを，" + SEL4)
    return MC(stem, right, cands, f"{info}。", d=3, p=4,
              ap="訂正後のデータを小さい順に並べ直し，範囲・四分位範囲・中央値をもう一度求めて比べる。最大値・最小値だけが変わるときは，四分位範囲や中央値は変わらないことが多い。",
              steps=[f"訂正後のデータを並べ直す：${lst(sorted(ys))}$。", f"訂正前：範囲 ${dec(f0[4] - f0[0])}$，四分位範囲 ${dec(f0[3] - f0[1])}$，中央値 ${dec(f0[2])}$。",
                     f"訂正後：範囲 ${dec(f1[4] - f1[0])}$，四分位範囲 ${dec(f1[3] - f1[1])}$，中央値 ${dec(f1[2])}$。", f"変わるのは「{right}」。"],
              alt=["訂正した値が，並べたときの何番目に入るかを考え，四分位数・中央値の位置（何番目の値か）にかかわるかどうかで判断する。"],
              pc=[("訂正後の値を正しく求めている", 2), ("正しい組み合わせを選んでいる", 2)],
              pit=["訂正後に並べ直さずに計算する。", "最大値が変わると四分位範囲も変わると思いこむ。"])


# ======================================================================
# C 思考力・記述応用
# ======================================================================

CMB_CTX = [("1か月に読んだ本の冊数", "冊", 0, 12), ("1週間に運動した日数", "日", 0, 7), ("小テストの得点", "点", 0, 10), ("けん垂の回数", "回", 0, 15)]


@gen("thinking_writing", 4, ["application", "written_reasoning"])
def c_combo(r):
    name, u, lo, hi = r.choice(CMB_CTX)
    A = [r.randint(lo, hi) for _ in range(10)]
    B = [r.randint(lo, hi) for _ in range(10)]
    fa, fb = five(A), five(B)
    from collections import Counter
    ca, cb = Counter(A), Counter(B)

    def mode(c):
        m = max(c.values())
        ks = [k for k, v in c.items() if v == m]
        return ks[0] if len(ks) == 1 else None
    pool = [(f"A組とB組の中央値は等しい。", fa[2] == fb[2], f"中央値は A組 ${dec(fa[2])}$，B組 ${dec(fb[2])}$。"),
            (f"A組の中央値は，B組の中央値より大きい。", fa[2] > fb[2], f"中央値は A組 ${dec(fa[2])}$，B組 ${dec(fb[2])}$。"),
            (f"A組の四分位範囲は，B組の四分位範囲より大きい。", fa[3] - fa[1] > fb[3] - fb[1], f"四分位範囲は A組 ${dec(fa[3] - fa[1])}$，B組 ${dec(fb[3] - fb[1])}$。"),
            (f"B組の範囲は，A組の範囲より大きい。", fb[4] - fb[0] > fa[4] - fa[0], f"範囲は A組 ${dec(fa[4] - fa[0])}$，B組 ${dec(fb[4] - fb[0])}$。"),
            (f"A組の{u}の合計は，B組の{u}の合計より大きい。", sum(A) > sum(B), f"合計は A組 ${sum(A)}$，B組 ${sum(B)}$。"),
            (f"B組の第3四分位数は，A組の第3四分位数より大きい。", fb[3] > fa[3], f"第3四分位数は A組 ${dec(fa[3])}$，B組 ${dec(fb[3])}$。"),
            (f"B組の第1四分位数は，A組の第1四分位数より小さい。", fb[1] < fa[1], f"第1四分位数は A組 ${dec(fa[1])}$，B組 ${dec(fb[1])}$。")]
    ma, mb = mode(ca), mode(cb)
    if ma is not None and mb is not None:
        pool.append((f"A組の最頻値は，B組の最頻値より大きい。", ma > mb, f"最頻値は A組 ${ma}$，B組 ${mb}$。"))
    t = r.randint(lo + 2, hi - 2)
    na, nb = sum(x >= t for x in A), sum(x >= t for x in B)
    pool.append((f"{t}{u}以上の生徒は，A組の方がB組より多い。", na > nb, f"{t}{u}以上は A組 ${na}$ 人，B組 ${nb}$ 人。"))
    r.shuffle(pool)
    st = pool[:4]
    tv = tuple(i for i in range(4) if st[i][1])
    assert 1 <= len(tv) <= 3
    L = "ABCD"
    allsub = [s for k in (1, 2, 3) for s in itertools.combinations(range(4), k)]
    others = [s for s in allsub if s != tv]
    r.shuffle(others)
    opts = [tv] + others[:5]
    fmt = lambda s: "，".join(L[i] for i in s)  # noqa: E731
    why = {}
    for s in opts[1:]:
        wrong = [L[i] + "は" + ("正しい" if st[i][1] else "誤り") + "（" + st[i][2] + "）" for i in range(4) if (i in s) != (i in tv)]
        why[fmt(s)] = ("．".join(wrong) + "．", "資料の読み取りの誤り")
    tbl = table([["A組"] + [str(x) for x in A], ["B組"] + [str(x) for x in B]], header=["組＼番号"] + [str(i) for i in range(1, 11)], caption=f"（単位：{u}）{FAKE}")
    body = "\n".join(f"{L[i]}．{st[i][0]}" for i in range(4))
    stem = (f"右の資料は，A組とB組からそれぞれ10人ずつ選んだ生徒の{name}を調べたものである。この資料から読み取れることがらについて述べた次のA〜Dの中から，正しいものをすべて選んだときの組み合わせとして最も適するものを，" + SEL6 + "\n" + body)
    return mc(stem, [fmt(s) for s in opts], "正しいのは " + fmt(tv) + "。" + " ".join(st[i][2] for i in range(4)), d=4, p=8, tbl=tbl, why=why,
              ap="それぞれの組のデータを小さい順に並べ，中央値・四分位数・範囲などを求めてから，A〜Dの文を1つずつ判断する。",
              steps=[f"A組を並べる：${lst(sorted(A))}$。B組を並べる：${lst(sorted(B))}$。",
                     f"A組：最小値 ${fa[0]}$，第1四分位数 ${dec(fa[1])}$，中央値 ${dec(fa[2])}$，第3四分位数 ${dec(fa[3])}$，最大値 ${fa[4]}$。",
                     f"B組：最小値 ${fb[0]}$，第1四分位数 ${dec(fb[1])}$，中央値 ${dec(fb[2])}$，第3四分位数 ${dec(fb[3])}$，最大値 ${fb[4]}$。"]
              + [f"{L[i]}：{st[i][2]}{'正しい' if st[i][1] else '誤り'}。" for i in range(4)],
              alt=["2組の箱ひげ図をかいて並べると，中央値・四分位範囲・範囲の比較が見やすくなる。"],
              pc=[("2組の四分位数などを正しく求めている", 4), ("A〜Dの正誤を正しく判断している", 4)],
              pit=["データを並べ替えずに中央値を求める。", "10個のデータの中央値を，5番目の値だけで決めてしまう。"])


def _xy_pool(r):
    n = r.randint(10, 30)
    xs = int_data(r, r.choice([7, 9, 11]), 1, 30)
    f = five(xs)
    iq = f[3] - f[1]
    wrong_iq = f[4] - f[0]
    return [
        ("四分位範囲は，データの中に極端にかけはなれた値があっても，その影響を受けにくい。", True, "四分位範囲は中央付近の約半分のデータで決まり，最大値・最小値を使わない。"),
        ("範囲は，最大値と最小値だけで決まるので，極端にかけはなれた値の影響を受けやすい。", True, "範囲＝最大値−最小値なので，極端な値があると大きく変わる。"),
        ("2つの箱ひげ図を比べたとき，箱の長さが長い方が，データの個数が多い。", False, "箱にふくまれるのはどちらも全体の約半分で，長さは散らばりの大きさを表す。"),
        ("箱ひげ図から，データの平均値を読み取ることができる。", False, "箱ひげ図に表されるのは最小値・四分位数・中央値・最大値で，平均値は読み取れない。"),
        ("箱ひげ図の箱の部分には，全体のおよそ半分のデータがふくまれる。", True, "第1四分位数から第3四分位数までに約50%のデータがふくまれる。"),
        (f"{n}個のデータで，最大値だけをさらに大きな値に変えても，四分位範囲は変わらない。", True, "第1・第3四分位数は最大値を使わずに決まるので，四分位範囲は変わらない。"),
        (f"データ ${lst(xs)}$ の四分位範囲は ${dec(iq)}$ である。", True, f"並べると ${lst(sorted(xs))}$，第1四分位数 ${dec(f[1])}$，第3四分位数 ${dec(f[3])}$ で，差は ${dec(iq)}$。"),
        (f"データ ${lst(xs)}$ の四分位範囲は ${dec(wrong_iq)}$ である。", False, f"${dec(wrong_iq)}$ は範囲。四分位範囲は ${dec(f[3])}-{dec(f[1])}={dec(iq)}$。"),
        ("箱ひげ図で，左のひげが右のひげより長いとき，最小値から第1四分位数までにふくまれるデータの個数の方が多い。", False, "どちらのひげの区間にも約25%ずつのデータがふくまれる。長さは散らばりを表す。"),
        ("第2四分位数と中央値は，いつも同じ値である。", True, "第2四分位数は中央値のことである。"),
    ]


@gen("thinking_writing", 3, ["written_reasoning", "concept"])
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
        why[ch] = (" ".join(rs), "四分位数・箱ひげ図の意味の誤解")
    return mc("四分位数や箱ひげ図について述べた次の X，Y の文の正誤の組み合わせとして最も適するものを，" + SEL4 + f"\nX　{x[0]}\nY　{y[0]}",
              [ans] + [ch for ch in XY if ch != ans], f"X：{x[2]}　Y：{y[2]}", d=4, p=8, why=why,
              ap="四分位数・範囲・四分位範囲・箱ひげ図の定義にもどり，具体例を考えて正誤を判断する。",
              steps=[f"X：{x[2]}", f"Y：{y[2]}", f"よって {ans}。"],
              alt=["自分で小さいデータの例をつくり，箱ひげ図をかいて確かめる。"],
              pc=[("X の正誤を根拠をもって判断している", 4), ("Y の正誤を根拠をもって判断している", 4)],
              pit=["箱やひげの長さを，データの個数と考える。"])


def _inner(svg):
    """外側の <svg> タグを外して中身だけにする（図を1枚の SVG に合成するため）。"""
    return re.sub(r"^<svg[^>]*>", "", svg)[:-len("</svg>")]


SHAPES = {"右に長いすそ（山が左寄り）": [2, 6, 8, 5, 3, 2, 1, 1], "左に長いすそ（山が右寄り）": [1, 1, 2, 3, 5, 8, 6, 2],
          "山が中央に1つ": [1, 2, 4, 8, 8, 4, 2, 1], "ほぼ平ら": [4, 4, 4, 4, 4, 4, 4, 4]}


@gen("thinking_writing", 3, ["cross_unit", "application"], rel=["JH-MATH-G1-U07"])
def c_hist_box(r):
    name, u = r.choice([("ハンドボール投げの記録", "m"), ("通学にかかる時間", "分"), ("小テストの得点", "点"), ("1週間の家庭学習の時間", "時間")])
    w = r.choice([2, 5])
    edges = [w * i for i in range(9)]
    data = {}
    for key, base in SHAPES.items():
        cnt = [max(1, c + r.choice([-1, 0, 0, 1])) for c in base]
        xs = []
        for i, c in enumerate(cnt):
            xs += [r.randint(edges[i], edges[i + 1] - 1) for _ in range(c)] if w > 1 else [edges[i]] * c
        data[key] = (cnt, xs, five(xs))
    keys = list(SHAPES)
    target = r.choice(keys)
    order = keys[:]
    r.shuffle(order)
    pos = order.index(target)
    cnt = data[target][0]
    n = sum(cnt)
    hist = _inner(histogram(edges, cnt, unit=u, width=380, L=54, R=14))
    box = _inner(boxplot([(KANA[i], data[k][2]) for i, k in enumerate(order)], 0, edges[-1], unit=u, lab=w))
    TH = 180 + 8 + 38 * 4 + 40
    fig = figure(f"{name}のヒストグラムと，箱ひげ図の候補 ア〜エ", f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 {TH}" width="380" height="{TH}" font-family="serif" font-size="12"><g font-size="11">{hist}</g><g transform="translate(0,188)">{box}</g></svg>')
    reason = {"右に長いすそ（山が左寄り）": "データが小さい方に集まっているので，箱が左に寄り，右のひげが長い。",
              "左に長いすそ（山が右寄り）": "データが大きい方に集まっているので，箱が右に寄り，左のひげが長い。",
              "山が中央に1つ": "データが中央に集まっているので，箱が短く中央にあり，左右のひげがほぼ同じ長さ。",
              "ほぼ平ら": "データが全体に散らばっているので，箱が長く中央にある。"}
    why = {KANA[i]: (f"この箱ひげ図は「{k}」の分布に合う。{reason[k]}", "分布の形と箱ひげ図の対応の誤り") for i, k in enumerate(order) if i != pos}
    f = data[target][2]
    stem = (f"右の図の上は，ある中学校の生徒{n}人の{name}をヒストグラムに表したものである。たとえば，${edges[0]}$ 以上 ${edges[1]}$ 未満の階級の度数は ${cnt[0]}$ 人である。"
            f"このデータを箱ひげ図に表したものとして最も適するものを，図の下のア〜エの中から1つ選んだものを，" + SEL4)
    return mc(stem, list(KANA), f"ヒストグラムは「{target}」の形で，{reason[target]}よって{KANA[pos]}。", d=4, p=8, keep=True, ai=pos, why=why, fig=fig,
              ap="ヒストグラムの山の位置とすその広がりから，中央値や四分位数がどの階級にあるかを考え，箱の位置と長さを予想する（1年のヒストグラムとのつながり）。",
              steps=[f"度数の合計は ${n}$ 人。累積度数から，中央値・第1四分位数・第3四分位数がふくまれる階級を求める。",
                     f"実際の5つの値はおよそ 最小値 ${dec(f[0])}$，第1四分位数 ${dec(f[1])}$，中央値 ${dec(f[2])}$，第3四分位数 ${dec(f[3])}$，最大値 ${dec(f[4])}$。",
                     f"{reason[target]}よって{KANA[pos]}。"],
              alt=["最小値・最大値がふくまれる階級（いちばん左・右の柱）と，中央値の階級だけでも候補をしぼれる。"],
              pc=[("ヒストグラムから中央値・四分位数の階級を求めている", 4), ("正しい箱ひげ図を選んでいる", 4)],
              pit=["ヒストグラムの山の高さを箱の長さと結びつけてしまう。", "山の部分（データが多いところ）で箱が長くなると考える。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

@gen("error_correction", 4, ["common_error", "computation"])
def d_quart_err(r):
    name, u, lo, hi = ctx(r)
    n = r.choice([9, 11, 13])
    xs = int_data(r, n, lo, hi)
    n = len(xs)
    s = sorted(xs)
    f = five(xs)
    where = r.choice([0, 2, 2, 3])
    h = n // 2
    LINES4 = ["1行目", "2行目", "3行目", "4行目"]
    if where == 0:
        assert xs != s
        d = xs
        md = med(d)
        q1, q3 = med(d[:h]), med(d[h + 1:])
        assert q3 - q1 != f[3] - f[1] and q3 > q1
        l1 = f"データを並んでいる順のまま使う：${lst(d)}$"
        l2 = f"中央値は真ん中の ${h + 1}$ 番目で ${dec(md)}$"
        l3 = f"前半の中央値は ${dec(q1)}$，後半の中央値は ${dec(q3)}$"
        l4 = f"四分位範囲は ${dec(q3)}-{dec(q1)}={dec(q3 - q1)}$"
        info = ("1行目（並べ替えていない）", "concept", "データがすでに並んでいるように見えると，小さい順に並べる手順を省きやすい。")
    else:
        l1 = f"小さい順に並べる：${lst(s)}$"
        l2 = f"中央値は真ん中の ${h + 1}$ 番目で ${dec(f[2])}$"
        if where == 2:
            q1, q3 = med(s[:h + 1]), med(s[h:])
            assert q3 - q1 != f[3] - f[1]
            l3 = f"中央値をふくめた前半 ${lst(s[:h + 1])}$ の中央値は ${dec(q1)}$，後半 ${lst(s[h:])}$ の中央値は ${dec(q3)}$"
            l4 = f"四分位範囲は ${dec(q3)}-{dec(q1)}={dec(q3 - q1)}$"
            info = ("3行目（中央値を前半・後半にふくめた）", "concept", "前半・後半に分けるとき，真ん中の値をどちらに入れるか迷い，両方に入れてしまう。")
        else:
            q1, q3 = f[1], f[3]
            l3 = f"前半 ${lst(s[:h])}$ の中央値は ${dec(q1)}$，後半 ${lst(s[h + 1:])}$ の中央値は ${dec(q3)}$"
            l4 = f"四分位範囲は ${s[-1]}-{s[0]}={s[-1] - s[0]}$"
            info = ("4行目（範囲を求めた）", "formula", "「範囲」と「四分位範囲」の名前が似ているため取り違えやすい。")
    ok = {0: "1行目は正しい。まず小さい順に並べている。", 1: f"2行目は正しい。{n}個なので中央値は ${h + 1}$ 番目の値。",
          2: "3行目は正しい。中央値を除いた前半・後半それぞれの中央値を求めている。", 3: "4行目は，3行目で求めた値の差を正しく計算している。"}
    why = {LINES4[i]: (ok[i], "誤りの箇所の見落とし") for i in range(4) if i != where}
    sol = "\n".join(f"{i + 1}行目　{t}" for i, t in enumerate([l1, l2, l3, l4]))
    v = f[3] - f[1]
    fix = f"四分位範囲は ${dec(f[3])}-{dec(f[1])}={dec(v)}$ {u}"
    return mc(f"〔問題〕次のデータは，生徒{n}人の{name}である。このデータの四分位範囲を求めなさい。\n${lst(xs)}$（単位：{u}）\n〔Kさんの解答〕\n{sol}\nKさんの解答で，誤りが最初に生じた行として最も適するものを，" + SEL4,
              LINES4, f"誤りが最初に生じたのは{LINES4[where]}。正しくは {fix}。", d=3, p=6, keep=True, ai=where, why=why,
              err=dict(sol=sol, step=info[0], type=info[1], tempt=info[2], fix=fix),
              ap="四分位範囲を求める手順（並べる→中央値→中央値を除いて前半・後半→それぞれの中央値→差）と，Kさんの各行を順に照らし合わせる。",
              steps=[f"小さい順に並べる：${lst(s)}$。", f"中央値 ${dec(f[2])}$ を除き，前半 ${lst(s[:h])}$，後半 ${lst(s[h + 1:])}$。",
                     f"第1四分位数 ${dec(f[1])}$，第3四分位数 ${dec(f[3])}$。", fix + "。"],
              alt=["正しく求めた四分位数でデータが約25%ずつに分かれているか（各区間の個数）を数えて確かめる。"],
              pc=[("誤りの行を正しく指摘している", 3), ("正しい四分位範囲を求めている", 3)],
              pit=["並べ替えずに四分位数を求める。", "中央値を前半・後半にふくめる。", "範囲と四分位範囲を取り違える。"],
              chk=(f"{fpy(f[3])}-{fpy(f[1])}", fpy(v), None, "intermediate"))


@gen("error_correction", 3, ["common_error", "written_reasoning"])
def d_box_misread(r):
    name, u, lo, hi = ctx(r)
    lo = lo // 5 * 5
    hi = -(-hi // 5) * 5
    n = r.choice([30, 32, 35])
    for _ in range(200):
        fa, fb = rand5(r, lo, hi), rand5(r, lo, hi)
        if (fa[3] - fa[1]) != (fb[3] - fb[1]) and (fa[4] - fa[3]) != (fb[4] - fb[3]) and (fa[2] - fa[1]) != (fa[3] - fa[2]):
            break
    else:
        raise AssertionError
    longbox = "A組" if fa[3] - fa[1] > fb[3] - fb[1] else "B組"
    longwh = "A組" if fa[4] - fa[3] > fb[4] - fb[3] else "B組"
    left_long = fa[2] - fa[1] > fa[3] - fa[2]
    part = ("第1四分位数から中央値まで", "中央値から第3四分位数まで") if left_long else ("中央値から第3四分位数まで", "第1四分位数から中央値まで")
    sc = r.choice(["box", "whisker", "part", "mean"])
    if sc == "box":
        claim = f"{longbox}の箱の方が長いので，{longbox}の方が，箱の範囲にふくまれる生徒の人数が多い。"
        right = "どちらの組も，箱にふくまれる生徒は全体の約半分で，人数はほぼ同じである。箱の長さは散らばりの大きさを表している。"
        etype = "interpretation"
    elif sc == "whisker":
        claim = f"{longwh}の右のひげの方が長いので，{longwh}の方が，第3四分位数より大きい値の生徒の人数が多い。"
        right = "第3四分位数から最大値までには，どちらの組も全体の約25%の生徒がふくまれ，人数はほぼ同じである。ひげの長さは値の散らばりを表す。"
        etype = "interpretation"
    elif sc == "part":
        claim = f"A組の箱ひげ図では，{part[0]}の部分の方が{part[1]}の部分より長いので，{part[0]}にふくまれる生徒の方が多い。"
        right = "どちらの部分にも全体の約25%の生徒がふくまれる。長い方は，その部分の値が広く散らばっていることを表す。"
        etype = "interpretation"
    else:
        claim = f"箱の中の線の値から，A組の{name}の平均値は ${fa[2]}$ {u}である。"
        right = f"箱の中の線は中央値を表す。A組の中央値が ${fa[2]}$ {u}であることはわかるが，平均値は箱ひげ図からは読み取れない。"
        etype = "concept"
    pool = [("箱ひげ図の目盛りの読み取りを誤っている。", "値の読み取りではなく，図の部分が表す意味のとらえ方を誤っている。", "誤りの種類の取り違え"),
            ("2つの組の人数が異なるので，比べることができない。", f"どちらの組も{n}人で，人数は同じである。", "条件の読み落とし"),
            ("Kさんの考えに誤りはない。", "箱ひげ図の長さはデータの個数ではなく散らばりを表すので，Kさんの考えは誤りである。" if sc != "mean" else "箱の中の線は平均値ではない。", "検算不足"),
            ("箱の中の線は第1四分位数を表すので，その値で比べるべきである。", "箱の中の線は中央値を表す。", "部分の名前の誤解")]
    r.shuffle(pool)
    fig = figure(f"A組とB組の{name}の箱ひげ図", boxplot([("A組", fa), ("B組", fb)], lo, hi, unit=u))
    stem = f"右の図は，A組とB組（どちらも{n}人）の{name}を箱ひげ図に表したものである。Kさんはこの図を見て，次のように考えた。\n〔Kさんの考え〕\n{claim}\nKさんの考えの誤りを説明したものとして最も適するものを，" + SEL4
    fix = right
    return MC(stem, right, pool, right, d=3, p=6, fig=fig,
              err=dict(sol=claim, step="図の部分の長さを人数と結びつけた部分" if sc != "mean" else "箱の中の線を平均値とした部分", type=etype,
                       tempt="図の大きな部分ほど「たくさんある」と感じやすい。" if sc != "mean" else "代表値として平均値がいちばんなじみがあるため。", fix=fix),
              ap="箱ひげ図の各区間には，データが約25%ずつふくまれることを思い出し，Kさんが図のどの部分を何と結びつけたかを確かめる。",
              steps=["箱ひげ図で，最小値〜第1四分位数〜中央値〜第3四分位数〜最大値の各区間には，約25%ずつのデータがある。", "長さはデータの散らばり，区間の位置は値の大きさを表す。", right],
              alt=["実際に小さいデータの例をつくり，箱が長くても短くても，ふくまれる個数は同じになることを確かめる。"],
              pc=[("誤りの理由を正しく指摘している", 3), ("箱ひげ図の正しい読み方を説明できる", 3)],
              pit=["箱やひげの長さをデータの個数と考える。", "箱の中の線を平均値と考える。"])


@gen("error_correction", 3, ["common_error", "condition_check"])
def d_iqr_err(r):
    name, u, lo, hi = ctx(r)
    lo = lo // 5 * 5
    hi = -(-hi // 5) * 5
    f = rand5(r, lo, hi)
    iq = f[3] - f[1]
    sc = r.choice(["range", "q3min", "half", "medq1"])
    if sc == "range":
        kv, sol = f[4] - f[0], f"四分位範囲は，最大値−最小値で ${f[4]}-{f[0]}={f[4] - f[0]}$"
        right = "最大値と最小値の差は範囲である。四分位範囲は，第3四分位数から第1四分位数を引いて求めなければならない。"
        etype = "formula"
    elif sc == "q3min":
        kv, sol = f[3] - f[0], f"四分位範囲は，第3四分位数−最小値で ${f[3]}-{f[0]}={f[3] - f[0]}$"
        right = "引く値が最小値になっている。第1四分位数を引かなければならない。"
        etype = "formula"
    elif sc == "half":
        kv, sol = (f[3] - f[1]) / 2, f"四分位範囲は，(第3四分位数−第1四分位数)÷2 で $({f[3]}-{f[1]})\\div2={dec((f[3] - f[1]) / 2)}$"
        right = "2でわる必要はない。四分位範囲は第3四分位数と第1四分位数の差そのものである。"
        etype = "formula"
    else:
        kv, sol = f[2] - f[1], f"四分位範囲は，中央値−第1四分位数で ${f[2]}-{f[1]}={f[2] - f[1]}$"
        right = "中央値から第1四分位数を引くと，箱の左半分の長さになる。第3四分位数から第1四分位数を引かなければならない。"
        etype = "formula"
    assert kv != iq
    pool = [("目盛りの読み取りを誤っている。", "5つの値の読み取りは正しく，誤りは計算に使う値の選び方にある。", "誤りの種類の取り違え"),
            ("四分位範囲は，第3四分位数と第1四分位数の和である。", "四分位範囲は和ではなく差である。", "定義の誤解"),
            ("Kさんの解答に誤りはない。", f"四分位範囲は ${f[3]}-{f[1]}={iq}$ で，Kさんの答えと異なる。", "検算不足"),
            ("四分位範囲は，中央値の2倍で求めなければならない。", "中央値の2倍は四分位範囲とは関係がない。", "定義の誤解")]
    r.shuffle(pool)
    fig = figure(f"{name}の箱ひげ図", boxplot([("", f)], lo, hi, unit=u))
    fix = f"${f[3]}-{f[1]}={iq}$ {u}"
    stem = f"〔問題〕右の図は，ある学年の生徒の{name}を箱ひげ図に表したものである。このデータの四分位範囲を求めなさい。\n〔Kさんの解答〕\n{sol}\nKさんの解答の誤りを説明したものとして最も適するものを，" + SEL4
    return MC(stem, right, pool, f"正しくは {fix}。", d=3, p=6, fig=fig,
              err=dict(sol=sol, step="四分位範囲を求める式", type=etype, tempt="範囲・四分位範囲・箱の半分の長さなど，似た「長さ」が図の中にいくつもあるため。", fix=fix),
              ap="四分位範囲の定義（第3四分位数−第1四分位数）を確認し，箱ひげ図の箱の長さと一致するかを見る。",
              steps=[f"箱の左はし（第1四分位数）は ${f[1]}$，右はし（第3四分位数）は ${f[3]}$。", f"四分位範囲は {fix}。", right],
              alt=["箱の長さを目盛りで数えると，四分位範囲と一致することを確かめる。"],
              pc=[("誤りの理由を正しく指摘している", 3), ("正しい四分位範囲を求めている", 3)],
              pit=["範囲と四分位範囲を取り違える。"],
              chk=(f"{f[3]}-{f[1]}", str(iq), None, "intermediate"))


GENERATORS = [a_quartiles, a_iqr, a_box_read, a_terms,
              b_box_choose, b_compare, b_freq_table, b_change,
              c_combo, c_xy_judge, c_hist_box,
              d_quart_err, d_box_misread, d_iqr_err]
GENERATORS = [robust(g) for g in GENERATORS]
