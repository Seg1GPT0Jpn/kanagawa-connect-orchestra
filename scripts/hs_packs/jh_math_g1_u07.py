"""単元パック：中学1年 データの活用（神奈川県公立高校入試形式）。"""
import itertools
import math
import re
import unicodedata
from fractions import Fraction as Fr

from banks._common import figure, mc, num, table
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem, tp)

UNIT_ID = "JH-MATH-G1-U07"

PREREQUISITES = [
    ("JH-MATH-G1-U01", "正の数・負の数の四則計算ができること。平均値や相対度数を求める計算（わり算・小数の計算）で使う。小学校で学んだ平均・割合・ドットプロット・柱状グラフの見方も前提とする。"),
    ("JH-MATH-G1-U02", "数量を文字式で表せること。合計や平均を文字で表し、わからない値を求めるときに使う。"),
    ("JH-MATH-G1-U03", "一次方程式を解けること。平均値からわからないデータの値を求めるときに使う。"),
]
EXTENSIONS = [
    ("JH-MATH-G2-U06", "多数回の試行で求めた相対度数（統計的確率）から、場合の数にもとづく確率へ進む。"),
    ("JH-MATH-G2-U07", "中央値の考え方をもとに、四分位数・四分位範囲・箱ひげ図でデータの散らばりを比べる。"),
    ("JH-MATH-G3-U08", "標本の代表値や相対度数から、母集団の傾向を推定する。"),
    ("HS-MATH1-U05", "高校のデータの分析で、分散・標準偏差・相関係数を使ってデータを調べる。"),
]


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


def ftex(v):
    v = Fr(v)
    if v.denominator == 1:
        return str(v.numerator)
    s = "-" if v < 0 else ""
    return f"{s}\\dfrac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def fpy(v):
    v = Fr(v)
    return str(v.numerator) if v.denominator == 1 else f"Rational({v.numerator},{v.denominator})"


def dec(v, minp=0):
    """有限小数で表せる分数を小数の文字列にする（表せないときは None）。"""
    v = Fr(v)
    for k in range(0, 6):
        x = v * 10 ** k
        if x.denominator == 1:
            k2 = max(k, minp)
            n = int(x) * 10 ** (k2 - k)
            s = str(abs(n)).rjust(k2 + 1, "0")
            out = s if k2 == 0 else s[:-k2] + "." + s[-k2:]
            return ("-" if v < 0 else "") + out
    return None


def MARK(stem, v, e, expr, **kw):
    v = Fr(v)
    assert v >= 0
    if v.denominator == 1:
        n = int(v)
        return num(stem, str(n), e, mark=("int", n), chk=(expr, str(n), None, "answer"), **kw)
    p, q = v.numerator, v.denominator
    return num(stem, f"${ftex(v)}$", e, mark=("frac", p, q), chk=(expr, f"Rational({p},{q})", None, "answer"), **kw)


SEL4 = "次の1〜4の中から1つ選び，その番号を答えなさい。"
SEL6 = "次の1〜6の中から1つ選び，その番号を答えなさい。"
FAKE = "（架空の資料）"

# 度数分布表の題材：(名前, 単位, 階級の幅の候補, 最小の階級の下端の候補, 対象)
CTX = [
    ("ハンドボール投げの記録", "m", [4, 5], [8, 10, 12], "生徒"),
    ("通学時間", "分", [5, 10], [0, 5], "生徒"),
    ("1日の家庭学習の時間", "分", [15, 20, 30], [0], "生徒"),
    ("握力の記録", "kg", [4, 5], [14, 15, 16, 20], "生徒"),
    ("重さ", "g", [20, 25, 50], [100, 150, 200], "個"),
    ("1か月に図書室で借りた本の冊数", "冊", [2, 3], [0], "生徒"),
    ("上体起こしの回数", "回", [3, 4, 5], [10, 12, 15], "生徒"),
]


def grp(ctx):
    return "ある畑で収穫したじゃがいも" if ctx[4] == "個" else "ある学年の生徒"


def who(ctx):
    return "個" if ctx[4] == "個" else "人"


def cls(lo, w):
    return f"{lo} 以上 {lo + w} 未満"


def cls_tex(lo, w, u):
    return f"${lo}$ {u}以上 ${lo + w}$ {u}未満"


def rand_freqs(r, k, N, minf=0):
    """合計 N の度数（山型に近い形）。"""
    peak = r.uniform(1, k - 2)
    wts = [max(0.4, 3.2 - abs(i - peak) * r.uniform(0.9, 1.4)) for i in range(k)]
    f = [minf] * k
    for _ in range(N - minf * k):
        f[r.choices(range(k), weights=wts)[0]] += 1
    return f


def freq_setup(r, Ns=(20, 25, 40, 50), k=None):
    ctx = r.choice(CTX)
    w = r.choice(ctx[2])
    lo = r.choice(ctx[3])
    k = k or r.randint(5, 6)
    N = r.choice(Ns)
    f = rand_freqs(r, k, N, 1)
    return ctx, w, lo, k, N, f


def freq_tbl(ctx, w, lo, f, extra=None, total=True):
    """度数分布表。extra = [(列名, [値...], 合計欄)]。"""
    head = [f"階級（{ctx[1]}）", f"度数（{who(ctx)}）"] + [x[0] for x in (extra or [])]
    rows = []
    for i, fi in enumerate(f):
        rows.append([cls(lo + i * w, w), str(fi)] + [x[1][i] for x in (extra or [])])
    if total:
        rows.append(["計", str(sum(f))] + [x[2] for x in (extra or [])])
    return table(rows, header=head, caption=FAKE)


def median_class(lo, w, f):
    """中央値が入る階級の番号（同じ階級に入らないときは None）。"""
    N = sum(f)
    pos = [N // 2, N // 2 + 1] if N % 2 == 0 else [(N + 1) // 2]
    idx = []
    for p in pos:
        c = 0
        for i, fi in enumerate(f):
            c += fi
            if c >= p:
                idx.append(i)
                break
    return idx[0] if len(set(idx)) == 1 else None


def mode_idx(f):
    m = max(f)
    return f.index(m) if f.count(m) == 1 else None


def hist_svg(lo, w, f, u, unit_n="人"):
    k = len(f)
    ymax = max(f) + (2 - max(f) % 2)
    X0, Y0, W, H = 40, 160, 200, 130
    bw = W / k
    sc = H / ymax
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 200" width="280" height="200" font-family="serif" font-size="10">']
    step = 1 if ymax <= 8 else 2
    for y in range(0, ymax + 1, step):
        yy = Y0 - y * sc
        out.append(f'<line x1="{X0}" y1="{yy:.1f}" x2="{X0 + W}" y2="{yy:.1f}" stroke="#bbb" stroke-width="0.6" stroke-dasharray="2,2"/>')
        out.append(f'<text x="{X0 - 6}" y="{yy + 3:.1f}" text-anchor="end">{y}</text>')
    for i, fi in enumerate(f):
        x = X0 + i * bw
        out.append(f'<rect x="{x:.1f}" y="{Y0 - fi * sc:.1f}" width="{bw:.1f}" height="{fi * sc:.1f}" fill="#d6e2f0" stroke="#000" stroke-width="1"/>')
    for i in range(k + 1):
        x = X0 + i * bw
        out.append(f'<text x="{x:.1f}" y="{Y0 + 13}" text-anchor="middle">{lo + i * w}</text>')
    out.append(f'<line x1="{X0}" y1="{Y0}" x2="{X0 + W + 8}" y2="{Y0}" stroke="#000"/><line x1="{X0}" y1="{Y0}" x2="{X0}" y2="{Y0 - H - 8}" stroke="#000"/>')
    out.append(f'<text x="{X0 + W + 10}" y="{Y0 + 13}">({u})</text><text x="{X0 - 30}" y="{Y0 - H - 12}">({unit_n})</text></svg>')
    return "".join(out)


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

_EX_F = [2, 5, 8, 4, 1]
LESSON = lesson(
    goals=["度数分布表・ヒストグラムをつくり、階級・度数・相対度数・累積度数・累積相対度数を求めて分布の特徴を読み取れる。",
           "平均値・中央値・最頻値・範囲の意味を理解し、目的に応じて適切な代表値を選んで、その理由を説明できる。",
           "多数回の試行の結果から相対度数を求め、それを起こりやすさ（確率）の目安として使える。"],
    duration=100,
    readiness=["小学校で学んだ平均（合計 ÷ 個数）を求められる。",
               "小学校で学んだ割合（くらべる量 ÷ もとにする量）を小数で表せる。",
               "小学校で学んだドットプロット・度数分布表・柱状グラフ（ヒストグラム）を読める。",
               "小数のわり算を正しく計算できる。"],
    flow=[("導入：どちらのクラスがよく投げたといえるか", 10, "人数の違う2クラスのハンドボール投げの記録を比べる場面を示す"),
          ("度数分布表とヒストグラム", 20, "階級・度数・階級値、ヒストグラムのかき方（例題1）"),
          ("相対度数と累積相対度数", 15, "人数の違う集団を割合で比べる"),
          ("代表値と範囲", 25, "平均値・中央値・最頻値・範囲、度数分布表からの平均値（例題2）"),
          ("多数回の試行と確率", 15, "キャップ投げの実験から相対度数の安定を確かめる（例題3）"),
          ("まとめと確認", 15, "確認問題と問題プリントの指示")],
    sections=[
        intro("in1", "人数がちがう2つのクラスを比べる",
              "1組（20人）と2組（25人）のハンドボール投げの記録がある。「20 m 以上投げた人」は1組が6人、2組が7人だった。2組のほうがよく投げたといえるだろうか。人数がちがうので、人数そのものではなく、全体に対する割合で比べる必要がある。この単元では、データを表やグラフに整理し、割合や代表値を使って特徴を読み取る方法を学ぶ。",
              bullets=["1組は $6\\div20=0.30$、2組は $7\\div25=0.28$。割合で比べると1組のほうが大きい。",
                       "データの整理のしかた（表・グラフ）と、データ全体を1つの数で表す代表値を使い分けられるようにする。"],
              points=[tp("最初に人数だけで比べさせ、その後に割合で比べると結論が逆になることに気づかせる。", ask="7人のほうが多いから2組の勝ち、といってよいか。", expect="人数がちがうので割合で比べる必要がある。", timing="導入の5分")]),
        definition("df1", "度数分布表とヒストグラム",
                   "データをいくつかの区間に分けて、区間ごとの個数を表にまとめたものを度数分布表という。区間を階級、区間の幅を階級の幅、各階級に入るデータの個数を度数という。度数分布表を柱状のグラフに表したものをヒストグラムという。",
                   formula="$$\\text{相対度数}=\\dfrac{\\text{その階級の度数}}{\\text{度数の合計}}$$",
                   conditions=["階級の真ん中の値を階級値という。例：$10$ m 以上 $15$ m 未満の階級値は $12.5$ m。",
                               "最初の階級からその階級までの度数の合計を累積度数、相対度数の合計を累積相対度数という。",
                               "相対度数の合計は $1$ になり、最後の階級の累積相対度数も $1$ になる。",
                               "「以上」はその値をふくみ、「未満」はその値をふくまない。$15$ m ちょうどの記録は「$15$ m 以上 $20$ m 未満」の階級に入る。"],
                   points=[tp("境目の値（ちょうど 15 m など）がどの階級に入るかを必ず確認させる。", ask="15.0 m の記録はどの階級に入るか。", expect="15 m 以上 20 m 未満の階級。", caution="「未満」の読み落としが多い。"),
                           tp("ヒストグラムの柱は、すき間なく並べること、横軸は階級の境目の値で目もりをとることを確認する。")]),
        definition("df2", "代表値と範囲",
                   "データ全体の特徴を1つの数値で表したものを代表値という。代表値には平均値・中央値・最頻値がある。また、最大値から最小値をひいた値を範囲（レンジ）といい、データの散らばりの程度を表す。",
                   formula="$$\\text{平均値}=\\dfrac{\\text{データの値の合計}}{\\text{データの個数}},\\qquad \\text{範囲}=\\text{最大値}-\\text{最小値}$$",
                   conditions=["中央値（メジアン）：データを小さい順に並べたときの中央の値。個数が偶数のときは、中央にある2つの値の平均値。",
                               "最頻値（モード）：データの中で最も多く現れる値。度数分布表では、度数が最も大きい階級の階級値。",
                               "極端に大きい（小さい）値がふくまれると、平均値はその影響を受けやすいが、中央値は受けにくい。"],
                   points=[tp("中央値は「並べてから真ん中」。並べる前の真ん中をとる誤りを例で示す。", ask="データの個数が10個のとき、中央値は何番目と何番目の値の平均か。", expect="5番目と6番目。", timing="代表値の説明の直後")]),
        derivation("dv1", "度数分布表から平均値を求める式を導く",
                   ["度数分布表では、1つ1つのデータの値はわからない。", "そこで、各階級に入るデータはすべてその階級の階級値をとると考える。",
                    "すると、ある階級のデータの合計は（階級値）×（度数）で表せる。", "これをすべての階級について加えると、データの合計の近似値になる。",
                    "よって $\\text{平均値}=\\dfrac{(\\text{階級値}\\times\\text{度数})\\ \\text{の合計}}{\\text{度数の合計}}$。",
                    "この値は、もとのデータから求めた平均値と一致するとは限らない（近似値である）。"],
                   points=[tp("「階級値で代表させる」という考え方を、なぜそうするのか（個々の値が不明だから）とあわせて説明させる。", ask="わる数は階級の数か、度数の合計か。", expect="度数の合計（データの個数）。", caution="階級の数でわる誤りが多い。")]),
        theorem("th1", "多数回の試行と相対度数",
                "$$\\text{あることがらが起こった回数}\\div\\text{試行の回数}\\ \\longrightarrow\\ \\text{一定の値に近づく}$$",
                ["同じ条件で多数回の試行を行うと、あることがらの起こる相対度数は一定の値に近づいていく。",
                 "その一定の値を、そのことがらの起こりやすさの程度（確率）の目安と考える。",
                 "試行の回数が少ないときの相対度数は大きくばらつくので、目安にはしにくい。"],
                body="ペットボトルのキャップや画びょうのように、どの結果も同じ程度に起こるとはいえないものでも、実験をくり返せば起こりやすさを数で表せる。",
                proof=["キャップを100回、200回、…と投げ、表向きになった回数を記録する。", "回数が少ないうちは相対度数が大きく変わる。",
                       "回数を増やすと、相対度数の変化はしだいに小さくなり、ある値の近くにとどまるようになる。", "このとどまる値を確率の目安として使う。"],
                points=[tp("班ごとの実験結果を合計して回数を増やすと、相対度数が安定していく様子を表で確認させる。", timing="実験のまとめのとき"),
                        tp("「2通りの結果だから確率は $\\dfrac{1}{2}$」と考える誤りを取り上げる。", caution="表と裏が同じ程度に起こるとは限らない。")]),
        example("ex1", "例題1　度数分布表と相対度数",
                "下の度数分布表は、ある学級20人の通学時間をまとめたものである（架空の資料）。$0$ 分以上 $5$ 分未満から順に度数は $2,\\,5,\\,8,\\,4,\\,1$ 人で、階級の幅は $5$ 分である。(1) $10$ 分以上 $15$ 分未満の階級の相対度数を求めなさい。(2) $15$ 分未満の生徒の累積相対度数を求めなさい。",
                ["(1) 度数は $8$ 人、度数の合計は $20$ 人。", "$8\\div20=0.40$。", "(2) $15$ 分未満の累積度数は $2+5+8=15$（人）。", "$15\\div20=0.75$。"],
                "(1) $0.40$　(2) $0.75$",
                thinking="相対度数は「その階級の度数 ÷ 合計」、累積相対度数は「その階級までの度数の合計 ÷ 合計」。",
                figure=figure("通学時間のヒストグラム（0〜25分、5分ごと、度数2,5,8,4,1）", hist_svg(0, 5, _EX_F, "分")),
                points=[tp("累積相対度数は、相対度数を順に加えても、累積度数を合計でわっても求められることを両方示す。")],
                misconceptions=[("(2) を $8\\div20=0.40$ とする", "「15 分未満」は 0〜15 分のすべての階級をふくむので、累積度数 $15$ を使う")]),
        example("ex2", "例題2　代表値",
                "次のデータは、9人の生徒の1週間の読書時間（時間）である。$3,\\,7,\\,2,\\,5,\\,12,\\,4,\\,5,\\,1,\\,6$。平均値・中央値・最頻値・範囲を求め、このデータの代表値としてどれが適切か考えなさい。",
                ["小さい順に並べる：$1,\\,2,\\,3,\\,4,\\,5,\\,5,\\,6,\\,7,\\,12$。", "合計は $45$ なので平均値は $45\\div9=5$（時間）。",
                 "9個なので中央値は5番目の $5$ 時間。最頻値は2回現れる $5$ 時間。", "範囲は $12-1=11$（時間）。",
                 "このデータでは3つの代表値がそろって $5$ 時間であり、どれを使っても大きな差はない。"],
                "平均値 $5$ 時間、中央値 $5$ 時間、最頻値 $5$ 時間、範囲 $11$ 時間",
                thinking="中央値は必ず並べかえてから求める。極端な値（12時間）が平均値にどう影響するかも考える。",
                points=[tp("12 を 30 に変えると平均値は7時間になるが、中央値は5時間のまま変わらないことを確かめさせる。", ask="1人だけ極端に長いとき、どちらの代表値が全体の様子をよく表すか。", expect="中央値。極端な値の影響を受けにくいから。")]),
        example("ex3", "例題3　多数回の試行",
                "あるペットボトルのキャップを投げる実験で、2000回投げたうち表向きになったのは 880 回だった。(1) 表向きになる相対度数を求めなさい。(2) このキャップを 5000 回投げると、表向きになるのはおよそ何回と考えられるか。",
                ["(1) $880\\div2000=0.44$。", "(2) 表向きになる確率を $0.44$ と考える。", "$5000\\times0.44=2200$（回）。"],
                "(1) $0.44$　(2) およそ $2200$ 回",
                thinking="多数回の試行の相対度数を、起こりやすさの目安（確率）として使う。",
                points=[tp("「およそ」とつく理由（実際には毎回ちょうど2200回になるわけではない）を確認する。")]),
        board("bd1", "板書案",
              [("① 整理する", ["階級・階級の幅・度数・階級値", "ヒストグラム（柱はすき間なく）", "相対度数＝度数÷合計", "累積相対度数（最後は1）"]),
               ("② 代表値", ["平均値＝合計÷個数", "中央値：並べて真ん中", "最頻値：最も多い値（階級値）", "範囲＝最大値−最小値", "度数分布表の平均：階級値×度数"]),
               ("③ 確率の目安", ["回数を増やす → 相対度数が安定", "その値を確率の目安に", "例3　$0.44\\times5000=2200$"])],
              points=[tp("①〜③の列は、授業の進行に合わせて左から順に書き足していく。例題の数値は色を変えて残しておく。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("相対度数を求めるとき、わる数は「度数の合計」であることを毎回声に出して確認させる。", ask="わる数は何か。", expect="度数の合計（全体の人数）。"),
               tp("代表値の選び方は、極端な値の有無・分布の形・目的（多くの人に当てはまる値か、全体の合計を意識するか）で判断させる。", timing="例題2の後"),
               tp("度数分布表から求めた平均値は近似値であり、もとのデータの平均値とずれることがある理由を説明する。"),
               tp("最頻値を度数分布表から答えるときは、度数ではなく階級値を答えることを確認する。", caution="度数（人数）を答える誤りが多い。")],
              misconceptions=[("最頻値として、最も大きい度数（人数）を答える", "最頻値は値（階級値）であり、人数ではない"),
                              ("並べかえる前のデータの真ん中の値を中央値とする", "必ず小さい順に並べてから中央の値をとる"),
                              ("度数分布表の平均値を、階級値の合計 ÷ 階級の数で求める", "（階級値 × 度数）の合計を度数の合計でわる")]),
        summary("sm1", "まとめ",
                ["度数分布表・ヒストグラムでデータの分布を整理する。", "相対度数＝度数÷合計。人数がちがう集団は相対度数で比べる。",
                 "代表値（平均値・中央値・最頻値）と範囲を、データの特徴や目的に応じて使い分ける。", "多数回の試行で安定した相対度数を、確率の目安として使う。"]),
        check("ck1", "確認問題",
              [("度数の合計が25人で、ある階級の度数が7人のとき、その階級の相対度数を求めなさい。", "$7\\div25=0.28$"),
               ("データ $4,\\,9,\\,6,\\,1,\\,8,\\,3$ の中央値を求めなさい。", "並べると $1,3,4,6,8,9$。中央値は $(4+6)\\div2=5$"),
               ("$20$ 分以上 $30$ 分未満の階級の階級値を答えなさい。", "$25$ 分")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

def rf_cands(f, i, N, mind=2):
    cum = sum(f[:i + 1])
    out = [(dec(Fr(cum, N), mind) if cum < N else None, "その階級までの度数の合計をわっている。これは累積相対度数である。", "相対度数と累積相対度数の混同")]
    if i + 1 < len(f):
        out.append((dec(Fr(f[i + 1], N), mind), "1つ下の行の階級の度数を読んでいる。", "読み取る階級の誤り"))
    if i > 0:
        out.append((dec(Fr(f[i - 1], N), mind), "1つ上の行の階級の度数を読んでいる。", "読み取る階級の誤り"))
    out.append((dec(Fr(N - f[i], N), mind), "その階級以外の度数の合計をわっている。", "相対度数の意味の誤解"))
    out.append((dec(Fr(f[i], 100), mind), "度数を100でわっている。わる数は度数の合計である。", "相対度数の求め方の誤り"))
    return out


@gen("basic_check", 5, ["computation"])
def a_relfreq(r):
    ctx, w, lo, k, N, f = freq_setup(r)
    i = r.randrange(k)
    assert f[i] > 0
    v = Fr(f[i], N)
    right = dec(v, 2)
    lab = cls_tex(lo + i * w, w, ctx[1])
    tgt = "個" if ctx[4] == "個" else "生徒"
    return MC(f"次の表は，{grp(ctx)} ${N}$ {who(ctx)}の{ctx[0]}を度数分布表にまとめたものである。{lab}の階級の相対度数として正しいものを，" + SEL4,
              right, rf_cands(f, i, N), f"相対度数＝度数÷度数の合計＝${f[i]}\\div{N}={right}$。", d=1, tbl=freq_tbl(ctx, w, lo, f),
              ap="相対度数は，その階級の度数が全体のどれだけの割合にあたるかを表す。",
              steps=[f"{lab}の階級の度数を読むと ${f[i]}$ {who(ctx)}。", f"度数の合計は ${N}$ {who(ctx)}。", f"${f[i]}\\div{N}={right}$。"],
              alt=["相対度数をすべての階級で求めて合計が $1$ になるかを確かめると，読み取りの誤りに気づける。"],
              pc=[("その階級の度数を正しく読み取っている", 1), ("度数の合計でわっている", 1)],
              pit=["累積度数をわってしまう。", "わる数を度数の合計以外にしてしまう。"],
              chk=(f"Rational({f[i]},{N})", fpy(v), None, "intermediate"))


DATA_CTX = [
    ("10点満点の小テストの得点", "点", 0, 10),
    ("1か月に読んだ本の冊数", "冊", 0, 12),
    ("バスケットボールのフリースロー10本のうち成功した本数", "本", 0, 10),
    ("1週間に運動した日数", "日", 0, 7),
    ("1日のスマートフォンの使用時間", "分", 20, 150),
    ("通学にかかる時間", "分", 3, 40),
    ("反復横とびの回数", "回", 35, 65),
    ("ある店の1日に売れたパンの個数", "個", 20, 60),
]


def dlist(xs):
    return "$" + ",\\,".join(map(str, xs)) + "$"


@gen("basic_check", 4, ["computation"])
def a_mean(r):
    name, u, a, b = r.choice(DATA_CTX)
    n = r.randint(5, 9)
    xs = [r.randint(a, b) for _ in range(n)]
    s = sum(xs)
    need = (-s) % n
    xs[-1] += need
    if xs[-1] > b:
        xs[-1] -= n
    assert a <= xs[-1] <= b
    m = Fr(sum(xs), n)
    assert m.denominator == 1
    srt = sorted(xs)
    who_ = "日" if "1日に売れた" in name else "人"
    return MARK(f"次のデータは，{n}{who_}の{name}を調べたものである。このデータの平均値を求めなさい。\n{dlist(xs)}（単位：{u}）", m,
                f"合計は ${sum(xs)}$ {u}，個数は ${n}$ なので平均値は ${sum(xs)}\\div{n}={m}$（{u}）。", f"Rational({sum(xs)},{n})", d=1, p=2, unit=u,
                ap="平均値＝データの値の合計÷データの個数。",
                steps=[f"合計：${'+'.join(map(str, xs))}={sum(xs)}$。", f"個数：${n}$。", f"平均値：${sum(xs)}\\div{n}={m}$（{u}）。"],
                alt=[f"仮の平均を ${srt[n // 2]}$ として，各値との差の平均を加えて求めてもよい。"],
                pc=[("合計を正しく求めている", 1), ("個数でわって平均値を求めている", 1)],
                pit=["データの個数を数えまちがえる。", "合計の計算でたし忘れが起こる。"])


@gen("basic_check", 4, ["computation", "condition_check"])
def a_median(r):
    name, u, a, b = r.choice(DATA_CTX)
    n = r.randint(6, 11)
    for _t in range(400):
        xs = [r.randint(a, b) for _ in range(n)]
        s = sorted(xs)
        med = Fr(s[n // 2]) if n % 2 else Fr(s[n // 2 - 1] + s[n // 2], 2)
        if med.denominator == 1 and xs != s:
            break
    else:
        raise AssertionError("retry")
    who_ = "日" if "1日に売れた" in name else "人"
    pos = f"{(n + 1) // 2}番目の値" if n % 2 else f"{n // 2}番目と{n // 2 + 1}番目の値の平均値"
    return MARK(f"次のデータは，{n}{who_}の{name}を調べたものである。このデータの中央値を求めなさい。\n{dlist(xs)}（単位：{u}）", med,
                f"小さい順に並べると {dlist(s)}。データは ${n}$ 個なので，中央値は{pos}で ${med}$（{u}）。", fpy(med), d=2, p=2, unit=u,
                ap="中央値は，データを小さい順に並べたときの中央の値。個数が偶数なら中央の2つの値の平均値をとる。",
                steps=[f"小さい順に並べる：{dlist(s)}。", f"個数は ${n}$ なので，{pos}を見る。", f"中央値は ${med}$（{u}）。"],
                alt=["大きい順に並べても中央の値は同じになるので，逆順に並べて確かめられる。"],
                pc=[("データを小さい順に並べている", 1), ("中央値を正しく求めている", 1)],
                pit=["並べかえずに，書かれた順の真ん中の値を答える。", "個数が偶数のとき，中央の2つの平均をとり忘れる。"])


@gen("basic_check", 4, ["computation", "concept"])
def a_mode_range(r):
    name, u, a, b = r.choice(DATA_CTX)
    n = r.randint(7, 11)
    kind = r.choice(["mode", "range", "range"])
    xs = [r.randint(a, b) for _ in range(n)]
    if kind == "mode":
        m = r.choice(xs)
        for j in r.sample(range(n), 2):
            xs[j] = m
        cnt = {x: xs.count(x) for x in xs}
        top = max(cnt.values())
        assert list(cnt.values()).count(top) == 1 and top >= 3
        v = max(cnt, key=cnt.get)
        s = sorted(xs)
        who_ = "日" if "1日に売れた" in name else "人"
        return MARK(f"次のデータは，{n}{who_}の{name}を調べたものである。このデータの最頻値を求めなさい。\n{dlist(xs)}（単位：{u}）", v,
                    f"${v}$ が ${top}$ 回現れ，最も多い。最頻値は ${v}$（{u}）。", str(v), d=1, p=2, unit=u,
                    ap="最頻値はデータの中で最も多く現れる値。小さい順に並べると数えやすい。",
                    steps=[f"小さい順に並べる：{dlist(s)}。", f"それぞれの値の個数を数えると，${v}$ が ${top}$ 回で最も多い。", f"最頻値は ${v}$（{u}）。"],
                    alt=["値ごとに「正」の字で個数を数える表をつくって確かめる。"],
                    pc=[("値ごとの個数を数えている", 1), ("最頻値を正しく答えている", 1)],
                    pit=["最も多く現れた回数（個数）を答えてしまう。"])
    s = sorted(xs)
    assert s[-1] > s[0]
    v = s[-1] - s[0]
    who_ = "日" if "1日に売れた" in name else "人"
    return MARK(f"次のデータは，{n}{who_}の{name}を調べたものである。このデータの範囲を求めなさい。\n{dlist(xs)}（単位：{u}）", v,
                f"最大値は ${s[-1]}$，最小値は ${s[0]}$ なので，範囲は ${s[-1]}-{s[0]}={v}$（{u}）。", f"{s[-1]}-{s[0]}", d=1, p=2, unit=u,
                ap="範囲＝最大値−最小値。データの散らばりの程度を表す。",
                steps=[f"最大値：${s[-1]}$。", f"最小値：${s[0]}$。", f"範囲：${s[-1]}-{s[0]}={v}$（{u}）。"],
                alt=["小さい順に並べ，両端の値の差をとって確かめる。"],
                pc=[("最大値と最小値を正しく見つけている", 1), ("差を正しく求めている", 1)],
                pit=["最初の値と最後の値の差をとってしまう（並べかえていない）。"])


TERMS = [
    ("度数分布表で，データを整理するために用いる区間", "階級", [("度数", "度数は各階級に入るデータの個数。"), ("階級値", "階級値は階級の真ん中の値。"), ("範囲", "範囲は最大値と最小値の差。")]),
    ("度数分布表で，各階級に入っているデータの個数", "度数", [("階級", "階級はデータを分ける区間。"), ("相対度数", "相対度数は度数を度数の合計でわった値。"), ("階級の幅", "階級の幅は区間の大きさ。")]),
    ("度数分布表で，階級の真ん中の値", "階級値", [("中央値", "中央値はデータを並べたときの中央の値で，階級ごとの値ではない。"), ("平均値", "平均値はデータの合計を個数でわった値。"), ("階級の幅", "階級の幅は区間の大きさ。")]),
    ("ある階級の度数の，度数の合計に対する割合", "相対度数", [("累積度数", "累積度数は最初の階級からの度数の合計。"), ("累積相対度数", "累積相対度数は最初の階級からの相対度数の合計。"), ("階級値", "階級値は階級の真ん中の値。")]),
    ("最初の階級からある階級までの度数を合計したもの", "累積度数", [("相対度数", "相対度数は度数を度数の合計でわった値。"), ("度数", "度数は1つの階級に入るデータの個数。"), ("範囲", "範囲は最大値と最小値の差。")]),
    ("データの最大値から最小値をひいた値", "範囲", [("中央値", "中央値は並べたときの中央の値。"), ("階級の幅", "階級の幅は度数分布表の区間の大きさ。"), ("最頻値", "最頻値は最も多く現れる値。")]),
    ("データを小さい順に並べたときの中央の値", "中央値", [("平均値", "平均値は合計を個数でわった値。"), ("最頻値", "最頻値は最も多く現れる値。"), ("階級値", "階級値は階級の真ん中の値。")]),
    ("データの中で最も多く現れる値", "最頻値", [("中央値", "中央値は並べたときの中央の値。"), ("度数", "度数は個数であり，データの値ではない。"), ("平均値", "平均値は合計を個数でわった値。")]),
    ("度数分布表を，階級の幅を横，度数を縦とする長方形を並べて表したグラフ", "ヒストグラム", [("折れ線グラフ", "折れ線グラフは点を線で結んだグラフ。"), ("円グラフ", "円グラフは割合を扇形で表すグラフ。"), ("帯グラフ", "帯グラフは割合を長方形の長さで表すグラフ。")]),
    ("平均値・中央値・最頻値のように，データ全体の特徴を1つの数値で表したもの", "代表値", [("範囲", "範囲は散らばりの程度を表す値で，代表値とはよばない。"), ("階級", "階級はデータを分ける区間。"), ("相対度数", "相対度数はある階級の割合。")]),
]


@gen("basic_check", 3, ["concept"])
def a_terms(r):
    q, right, ws = r.choice(TERMS)
    return MC(f"{q}を何というか。最も適するものを，" + SEL4, right, [(t, w, "用語の意味の混同") for t, w in ws],
              f"{q}を「{right}」という。", d=1,
              ap="度数分布表のどの部分（区間・個数・割合）や，データのどんな値を指しているかを考える。",
              steps=["問題の文が「区間」「個数」「割合」「値」のどれを表しているかを考える。", "それぞれの用語の意味と比べる。", f"一致するのは「{right}」。"],
              alt=["実際の度数分布表を思いうかべ，どの欄にあたるかを確かめる。"],
              pc=[("用語の意味を理解している", 1), ("正しいものを選んでいる", 1)],
              pit=["度数（個数）と階級値（値）を取り違える。"])


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 4, ["computation", "condition_check"])
def b_class_mean(r):
    ctx, w, lo, k, N, f = freq_setup(r, Ns=(20, 25, 40, 50), k=r.randint(4, 6))
    cv = [lo + i * w + Fr(w, 2) for i in range(k)]
    tot = sum(c * x for c, x in zip(cv, f))
    m = tot / N
    right = dec(m)
    assert right is not None
    u = ctx[1]
    cands = [(dec(sum(Fr(lo + i * w) * x for i, x in enumerate(f)) / N), "階級値ではなく，各階級の下端の値（〜以上の値）を使っている。", "階級値の取り違え"),
             (dec(sum(cv) / k), "度数を考えず，階級値の平均をとっている。", "度数の重みの見落とし"),
             (dec(tot / k), "度数の合計ではなく，階級の数でわっている。", "わる数の誤り"),
             (dec(cv[mode_idx(f)] if mode_idx(f) is not None else cv[0] + w), "度数が最も多い階級の階級値（最頻値）を答えている。", "平均値と最頻値の混同"),
             (dec(sum(Fr(lo + (i + 1) * w) * x for i, x in enumerate(f)) / N), "各階級の上端の値（〜未満の値）を使っている。", "階級値の取り違え")]
    cands = [c for c in cands if c[0]]
    return MC(f"次の表は，{grp(ctx)} ${N}$ {who(ctx)}の{ctx[0]}を度数分布表にまとめたものである。この表から平均値を求めるとき，その値として正しいものを，" + SEL4 + "ただし，各階級に入るデータの値はすべてその階級の階級値とする。",
              f"{right} {u}", [(f"{t} {u}", a, b) for t, a, b in cands], f"(階級値 × 度数) の合計は ${dec(tot)}$，これを ${N}$ でわって ${right}$（{u}）。", d=3, p=4,
              tbl=freq_tbl(ctx, w, lo, f),
              ap="度数分布表では，各階級のデータをすべて階級値とみなして合計を求め，度数の合計でわる。",
              steps=["各階級の階級値：" + "，".join(f"${dec(c)}$" for c in cv) + "。", f"(階級値 × 度数) の合計：${dec(tot)}$。", f"平均値：${dec(tot)}\\div{N}={right}$（{u}）。"],
              alt=[f"仮の平均を中央付近の階級値 ${dec(cv[k // 2])}$ とし，(階級値 − 仮の平均) × 度数 の合計を ${N}$ でわって加えると，計算が楽になる。"],
              pc=[("階級値を正しく求めている", 1), ("(階級値 × 度数) の合計を求めている", 2), ("度数の合計でわっている", 1)],
              pit=["階級の数でわってしまう。", "階級の下端の値を使ってしまう。"],
              chk=(f"({'+'.join(f'{fpy(c)}*{x}' for c, x in zip(cv, f))})/{N}", fpy(m), None, "intermediate"))


@gen("standard_practice", 4, ["computation", "concept"])
def b_cumrel(r):
    ctx, w, lo, k, N, f = freq_setup(r, Ns=(20, 25, 50))
    kind = r.choice(["under", "over", "under"])
    u = ctx[1]
    if kind == "under":
        i = r.randrange(1, k - 1)
        cum = sum(f[:i + 1])
        v = Fr(cum, N)
        right = dec(v, 2)
        bound = lo + (i + 1) * w
        cands = [(dec(Fr(f[i], N), 2), "その階級だけの相対度数を求めている。「未満」なのでそれより前の階級もふくめる。", "累積の考え忘れ"),
                 (dec(Fr(sum(f[:i]), N), 2), "1つ手前の階級までしか加えていない。", "境目の値の扱いの誤り"),
                 (dec(Fr(sum(f[:i + 2]), N), 2), "1つ先の階級まで加えている。", "境目の値の扱いの誤り"),
                 (dec(Fr(N - cum, N), 2), f"${bound}$ {u}以上の割合を求めている。", "以上と未満の取り違え")]
        cands = [c for c in cands if c[0] != dec(Fr(0), 2)]
        return MC(f"次の表は，{grp(ctx)} ${N}$ {who(ctx)}の{ctx[0]}を度数分布表にまとめたものである。{ctx[0]}が ${bound}$ {u}未満である階級の累積相対度数として正しいものを，" + SEL4,
                  right, cands, f"${bound}$ {u}未満の累積度数は ${'+'.join(map(str, f[:i + 1]))}={cum}$。${cum}\\div{N}={right}$。", d=2, p=4,
                  tbl=freq_tbl(ctx, w, lo, f),
                  ap="累積相対度数は，最初の階級からその階級までの度数の合計を，度数の合計でわった値。",
                  steps=[f"${bound}$ {u}未満にふくまれる階級は，最初から{cls_tex(lo + i * w, w, u)}の階級まで。", f"累積度数：${cum}$。", f"${cum}\\div{N}={right}$。"],
                  alt=["各階級の相対度数を求めて順に加えても同じ値になる。"],
                  pc=[("ふくまれる階級を正しく判断している", 2), ("累積相対度数を正しく求めている", 2)],
                  pit=["その階級の相対度数だけを答える。", "「未満」の境目の階級を1つずらす。"],
                  chk=(f"Rational({cum},{N})", fpy(v), None, "intermediate"))
    i = r.randrange(1, k)
    cnt = sum(f[i:])
    pct = Fr(cnt * 100, N)
    assert pct.denominator == 1 and 0 < cnt < N
    bound = lo + i * w
    return MARK(f"次の表は，{grp(ctx)} ${N}$ {who(ctx)}の{ctx[0]}を度数分布表にまとめたものである。{ctx[0]}が ${bound}$ {u}以上である{'じゃがいも' if ctx[4] == '個' else '生徒'}は，全体の何％か求めなさい。", pct,
                f"${bound}$ {u}以上は ${'+'.join(map(str, f[i:]))}={cnt}$ {who(ctx)}。$\\dfrac{{{cnt}}}{{{N}}}\\times100={pct}$（％）。", f"Rational({cnt}*100,{N})", d=3, p=4, unit="％",
                tbl=freq_tbl(ctx, w, lo, f),
                ap="「〜以上」にふくまれる階級をすべて加え，度数の合計に対する割合を百分率で表す。",
                steps=[f"${bound}$ {u}以上にふくまれる階級：{cls_tex(bound, w, u)}の階級から最後まで。", f"度数の合計：${cnt}$ {who(ctx)}。", f"割合：${cnt}\\div{N}={dec(Fr(cnt, N), 2)}$，百分率で ${pct}$ ％。"],
                alt=[f"${bound}$ {u}未満の累積相対度数 ${dec(Fr(N - cnt, N), 2)}$ を $1$ からひいて求めてもよい。"],
                pc=[("ふくまれる階級を正しく判断している", 2), ("割合を百分率で正しく表している", 2)],
                pit=[f"${bound}$ {u}ちょうどの階級を「以上」にふくめ忘れる。", "小数のまま答えて百分率にしない。"])


@gen("standard_practice", 4, ["concept", "computation"])
def b_hist(r):
    ctx, w, lo, k, N, f = freq_setup(r, Ns=(20, 21, 25, 30, 31, 35))
    u = ctx[1]
    kind = r.choice(["median", "mode", "count"] if w % 2 == 0 else ["median", "count"])
    labs = [cls_tex(lo + i * w, w, u) for i in range(k)]
    fig = figure(f"{ctx[0]}のヒストグラム（{lo}{u}から{w}{u}ごと，度数 {','.join(map(str, f))}）", hist_svg(lo, w, f, u, who(ctx)))
    head = f"次の図は，{grp(ctx)} ${N}$ {who(ctx)}の{ctx[0]}をヒストグラムに表したものである。たとえば，{lo} {u}以上 {lo + w} {u}未満の{'じゃがいも' if ctx[4] == '個' else '生徒'}は {f[0]} {who(ctx)}である。"
    if kind == "median":
        mi = median_class(lo, w, f)
        assert mi is not None
        pos = f"{(N + 1) // 2}番目" if N % 2 else f"{N // 2}番目と{N // 2 + 1}番目"
        mo = mode_idx(f)
        cands = [(labs[j], f"中央値は小さい方から{pos}の値で，この階級には入らない。" + ("この階級は度数が最も大きい階級（最頻値の階級）である。" if j == mo else ""), "中央値と最頻値の混同" if j == mo else "中央値の位置の誤り") for j in sorted(range(k), key=lambda j: (j != mo, abs(j - mi))) if j != mi]
        cum = [sum(f[:j + 1]) for j in range(k)]
        return MC(head + "中央値がふくまれる階級として正しいものを，" + SEL4, labs[mi], cands,
                  f"${N}$ {who(ctx)}なので中央値は小さい方から{pos}の値。累積度数より，その値は{labs[mi]}の階級に入る。", d=3, p=4, fig=fig,
                  ap="中央値はデータを小さい順に並べたときの中央の値。小さい方から何番目かを求め，累積度数でその位置の階級を探す。",
                  steps=[f"データの個数は ${N}$ なので，中央値は小さい方から{pos}。", "累積度数：" + "，".join(f"${c}$" for c in cum) + "。", f"{pos}の値は{labs[mi]}の階級に入る。"],
                  alt=["大きい方から数えても，同じ階級にたどりつくことを確かめる。"],
                  pc=[("中央値が何番目の値かを求めている", 2), ("累積度数から階級を判断している", 2)],
                  pit=["度数が最も大きい階級を中央値の階級と考えてしまう。", "横軸の真ん中の階級を選んでしまう。"])
    if kind == "mode":
        mo = mode_idx(f)
        assert mo is not None
        v = lo + mo * w + Fr(w, 2)
        return MARK(head + f"このヒストグラムから最頻値を求めなさい。ただし，最頻値は度数が最も大きい階級の階級値とする。", v,
                    f"度数が最も大きいのは{labs[mo]}の階級（${f[mo]}$ {who(ctx)}）で，その階級値は $\\dfrac{{{lo + mo * w}+{lo + (mo + 1) * w}}}{{2}}={ftex(v)}$（{u}）。", fpy(v), d=2, p=4, unit=u, fig=fig,
                    ap="度数分布表・ヒストグラムでは，最も高い柱の階級の階級値を最頻値とする。",
                    steps=[f"最も高い柱は{labs[mo]}の階級。", f"階級値は両端の平均：$({lo + mo * w}+{lo + (mo + 1) * w})\\div2={ftex(v)}$。", f"最頻値は ${ftex(v)}$ {u}。"],
                    alt=["階級値は「下端 ＋ 階級の幅の半分」としても求められる。"],
                    pc=[("最も度数の大きい階級を見つけている", 2), ("階級値を答えている", 2)],
                    pit=["度数（人数）を答えてしまう。", "階級の下端の値を答えてしまう。"])
    i = r.randrange(1, k - 1)
    j = r.randrange(i + 1, k + 1)
    cnt = sum(f[i:j])
    assert cnt > 0
    a_, b_ = lo + i * w, lo + j * w
    return MARK(head + f"{ctx[0]}が ${a_}$ {u}以上 ${b_}$ {u}未満の{'じゃがいも' if ctx[4] == '個' else '生徒'}は何{who(ctx)}か求めなさい。", cnt,
                f"${a_}$ {u}以上 ${b_}$ {u}未満にふくまれる柱の度数は ${'+'.join(map(str, f[i:j]))}={cnt}$（{who(ctx)}）。", "+".join(map(str, f[i:j])), d=2, p=4, unit=who(ctx), fig=fig,
                ap="横軸の目もりで範囲にふくまれる柱を選び，その高さ（度数）を加える。",
                steps=[f"ふくまれる柱：{'，'.join(labs[i:j])}。", "それぞれの高さ：" + "，".join(f"${x}$" for x in f[i:j]) + "。", f"合計：${cnt}$ {who(ctx)}。"],
                alt=[f"全体 ${N}$ から，範囲の外にある柱の度数をひいて求めてもよい。"],
                pc=[("ふくまれる柱を正しく選んでいる", 2), ("度数を正しく合計している", 2)],
                pit=["「未満」の境目の柱までふくめてしまう。"])


TRIAL_OBJ = [("ペットボトルのキャップ", "表向き", "裏向き"), ("画びょう", "針が上向き", "針が下向き"),
             ("紙コップ", "横向き", "横向き以外"), ("プラスチック製のスプーン", "表向き", "裏向き")]
TRIAL_P = [Fr(x, 100) for x in (32, 34, 36, 38, 42, 44, 46, 54, 56, 58, 62, 64, 66, 68, 72)]
TRIAL_N = [100, 200, 500, 1000, 2000]


@gen("standard_practice", 4, ["concept", "computation", "cross_unit"], rel=["JH-MATH-G2-U06"])
def b_trial(r):
    obj, yes, no = r.choice(TRIAL_OBJ)
    p = r.choice(TRIAL_P)
    cs = []
    for n in TRIAL_N:
        if n == 2000:
            cs.append(int(p * n))
        else:
            sd = math.sqrt(n) * r.uniform(0.6, 1.6) * r.choice([1, -1])
            cs.append(int(round(float(p) * n + sd)))
    kind = r.choice(["rf", "est", "count", "count"])
    rows = [["投げた回数（回）"] + [str(n) for n in TRIAL_N], [f"{yes}になった回数（回）"] + [str(c) for c in cs]]
    tbl = table(rows, caption=FAKE)
    head = f"Kさんの班は，ある{obj}を投げて{yes}になる回数を調べる実験を行い，その結果を次の表にまとめた。"
    if kind == "rf":
        j = r.choice([1, 2, 3])
        n, c = TRIAL_N[j], cs[j]
        v = Fr(c, n)
        right = dec(v)
        cands = [(dec(Fr(n - c, n)), f"{no}になった相対度数を求めている。", "求めることがらの取り違え"),
                 (dec(Fr(c, 2000)), "最後の試行回数 2000 回でわっている。", "わる数の誤り"),
                 (dec(Fr(cs[j - 1], TRIAL_N[j - 1])), f"{TRIAL_N[j - 1]} 回のときの相対度数を求めている。", "読み取る列の誤り"),
                 (dec(Fr(cs[j + 1], TRIAL_N[j + 1])), f"{TRIAL_N[j + 1]} 回のときの相対度数を求めている。", "読み取る列の誤り")]
        return MC(head + f"{n} 回投げたときの，{yes}になった相対度数として正しいものを，" + SEL4, right, cands,
                  f"${c}\\div{n}={right}$。", d=2, p=4, tbl=tbl,
                  ap="相対度数＝そのことがらが起こった回数÷投げた回数。",
                  steps=[f"{n} 回投げたとき，{yes}になったのは ${c}$ 回。", f"${c}\\div{n}={right}$。"],
                  alt=[f"{no}の相対度数 ${dec(Fr(n - c, n))}$ を $1$ からひいても求められる。"],
                  pc=[("回数を正しく読み取っている", 2), ("相対度数を正しく求めている", 2)],
                  pit=["別の列の数を使ってしまう。"],
                  chk=(f"Rational({c},{n})", fpy(v), None, "intermediate"))
    if kind == "est":
        right = dec(p, 2)
        cands = [(dec(Fr(cs[0], 100), 2), "試行回数が少ない 100 回のときの相対度数を使っている。回数が少ないと相対度数はばらつく。", "少ない試行回数での判断"),
                 ("0.50", f"結果が「{yes}」と「{no}」の2通りだから $\\dfrac{{1}}{{2}}$ と考えている。2通りが同じ程度に起こるとは限らない。", "同様に確からしいことの誤認"),
                 (dec(1 - p, 2), f"{no}になる相対度数を答えている。", "求めることがらの取り違え"),
                 (dec(Fr(sum(cs), 5 * 2000), 3), "回数の合計を不適切な数でわっている。", "相対度数の求め方の誤り")]
        return MC(head + f"この結果から，この{obj}を1回投げるとき，{yes}になる確率はどのくらいと考えられるか。最も適するものを，" + SEL4, right, cands,
                  f"投げた回数が多いほど相対度数は安定する。2000 回のときの相対度数 ${cs[-1]}\\div2000={right}$ を確率の目安とする。", d=3, p=4, tbl=tbl,
                  ap="多数回の試行で相対度数が一定の値に近づくとき，その値を確率の目安と考える。最も回数が多いときの相対度数を使う。",
                  steps=["各回数での相対度数を求めると，回数が増えるほど変化が小さくなる。", f"最も回数が多い 2000 回の相対度数は ${right}$。", f"確率はおよそ ${right}$ と考えられる。"],
                  alt=["1000 回と 2000 回の相対度数がほぼ同じであることを確かめ，安定していることを確認する。"],
                  pc=[("回数が多いときの相対度数を使うと判断している", 2), ("相対度数を正しく求めている", 2)],
                  pit=["結果が2通りなので確率は $\\dfrac{1}{2}$ と考えてしまう。", "回数の少ない実験の結果を使ってしまう。"])
    M = r.choice([1500, 2500, 3000, 4000, 5000, 6000, 10000])
    v = p * M
    assert v.denominator == 1
    return MARK(head + f"この結果から，この{obj}を {M} 回投げるとき，{yes}になるのはおよそ何回と考えられるか求めなさい。ただし，2000 回投げたときの相対度数を{yes}になる確率と考えるものとする。", v,
                f"確率を ${cs[-1]}\\div2000={dec(p, 2)}$ と考えると，${M}\\times{dec(p, 2)}={v}$（回）。", f"{M}*Rational({cs[-1]},2000)", d=3, p=4, unit="回",
                tbl=tbl,
                ap="多数回の試行の相対度数を確率とみなし，(投げる回数) × (確率) で回数を見積もる。次の学年の確率の単元で学ぶ「確率の求め方」とつながる考え方である。",
                steps=[f"2000 回のときの相対度数：${cs[-1]}\\div2000={dec(p, 2)}$。", f"{M} 回投げるときの見積もり：${M}\\times{dec(p, 2)}={v}$。", f"およそ ${v}$ 回。"],
                alt=[f"比例式 $2000:{cs[-1]}={M}:x$ を解いても同じ結果になる。"],
                pc=[("確率の目安を正しく求めている", 2), ("回数を正しく見積もっている", 2)],
                pit=["100 回のときなど，回数の少ないときの相対度数を使ってしまう。"])


def _stats(xs):
    s = sorted(xs)
    n = len(s)
    med = Fr(s[n // 2]) if n % 2 else Fr(s[n // 2 - 1] + s[n // 2], 2)
    cnt = {x: xs.count(x) for x in xs}
    top = max(cnt.values())
    modes = [x for x, c in cnt.items() if c == top]
    return {"mean": Fr(sum(xs), n), "median": med, "range": s[-1] - s[0], "mode": modes[0] if len(modes) == 1 and top > 1 else None}


STAT_NAME = {"mean": "平均値", "median": "中央値", "range": "範囲", "mode": "最頻値"}
COMBO = ["X：正　Y：正", "X：正　Y：誤", "X：誤　Y：正", "X：誤　Y：誤"]


@gen("standard_practice", 4, ["concept", "condition_check"])
def b_compare(r):
    name, u, a, b = r.choice(DATA_CTX[:4])
    n1, n2 = r.randint(6, 9), r.randint(6, 9)
    g1 = [r.randint(a, b) for _ in range(n1)]
    g2 = [r.randint(a, b) for _ in range(n2)]
    S1, S2 = _stats(g1), _stats(g2)
    keys = [k for k in ("mean", "median", "range", "mode") if S1[k] is not None and S2[k] is not None and S1[k] != S2[k]]
    assert len(keys) >= 2
    kx, ky = r.sample(keys, 2)
    tx, ty = r.choice([True, False]), r.choice([True, False])

    def stmt(k, t):
        big = S1[k] > S2[k]
        if big == t:
            return f"{STAT_NAME[k]}は，Aグループのほうが大きい。"
        return f"{STAT_NAME[k]}は，Bグループのほうが大きい。"
    X, Y = stmt(kx, tx), stmt(ky, ty)
    right = COMBO[[(True, True), (True, False), (False, True), (False, False)].index((tx, ty))]

    def fmt(v):
        return dec(v) or f"${ftex(v)}$"
    facts = {k: f"{STAT_NAME[k]}はAが {fmt(S1[k])} {u}，Bが {fmt(S2[k])} {u}" for k in (kx, ky)}
    why = {}
    for c, (vx, vy) in zip(COMBO, [(True, True), (True, False), (False, True), (False, False)]):
        if c == right:
            continue
        bad = []
        if vx != tx:
            bad.append(f"Xは{'正しい' if tx else '誤り'}（{facts[kx]}）")
        if vy != ty:
            bad.append(f"Yは{'正しい' if ty else '誤り'}（{facts[ky]}）")
        why[c] = ("。".join(bad) + "。", "代表値・範囲の求め方や比べ方の誤り")
    return mc(f"次のデータは，AグループとBグループの生徒の{name}を調べたものである。\nAグループ（{n1}人）：{dlist(g1)}\nBグループ（{n2}人）：{dlist(g2)}\n（単位：{u}）\nこのデータについて述べた次のX，Yの文の正誤の組み合わせとして最も適するものを，あとの1〜4の中から1つ選び，その番号を答えなさい。\nX：{X}\nY：{Y}",
              [right] + [c for c in COMBO if c != right], f"{facts[kx]}，{facts[ky]}。よって {right}。", d=3, p=4, why=why,
              ap="それぞれのグループについて，文に出てくる値を実際に求めてから比べる。中央値・最頻値は小さい順に並べると求めやすい。",
              steps=[f"Aを並べる：{dlist(sorted(g1))}，Bを並べる：{dlist(sorted(g2))}。", f"{facts[kx]}。", f"{facts[ky]}。", f"よって {right}。"],
              alt=["平均値は合計を比べてから個数でわる。個数がちがうときは合計だけで比べてはいけないことに注意して確かめる。"],
              pc=[("Xの正誤を正しく判断している", 2), ("Yの正誤を正しく判断している", 2)],
              pit=["人数がちがうのに合計で平均を比べてしまう。", "並べかえずに中央値を判断する。"])


# ======================================================================
# C 思考力・記述応用
# ======================================================================

LETTERS = ["A", "B", "C", "D"]


@gen("thinking_writing", 4, ["condition_check", "written_reasoning"])
def c_combo(r):
    ctx = r.choice([c for c in CTX if c[4] != "個"])
    w = r.choice(ctx[2])
    lo = r.choice(ctx[3])
    k = 5
    N1, N2 = 25, 20
    f1, f2 = rand_freqs(r, k, N1, 1), rand_freqs(r, k, N2, 1)
    u = ctx[1]
    m1, m2 = mode_idx(f1), mode_idx(f2)
    md1, md2 = median_class(lo, w, f1), median_class(lo, w, f2)
    assert None not in (m1, m2, md1, md2)
    labs = [cls_tex(lo + i * w, w, u) for i in range(k)]
    st = []
    # 1 最頻値
    st.append((f"最頻値は，1組のほうが大きい。", m1 > m2, f"最頻値は1組が{labs[m1]}の階級値，2組が{labs[m2]}の階級値"))
    # 2 ある階級の相対度数
    i = r.randrange(k)
    rf1, rf2 = Fr(f1[i], N1), Fr(f2[i], N2)
    assert rf1 != rf2
    st.append((f"{labs[i]}の階級の相対度数は，1組のほうが大きい。", rf1 > rf2, f"その階級の相対度数は1組が ${dec(rf1, 2)}$，2組が ${dec(rf2, 2)}$"))
    # 3 中央値の階級
    st.append(("中央値がふくまれる階級は，1組と2組で同じである。", md1 == md2, f"中央値の階級は1組が{labs[md1]}，2組が{labs[md2]}"))
    # 4 未満の累積相対度数
    j = r.randrange(1, k - 1)
    c1, c2 = Fr(sum(f1[:j + 1]), N1), Fr(sum(f2[:j + 1]), N2)
    assert c1 != c2
    bnd = lo + (j + 1) * w
    st.append((f"記録が ${bnd}$ {u}未満の生徒の割合は，2組のほうが大きい。", c2 > c1, f"${bnd}$ {u}未満の累積相対度数は1組が ${dec(c1, 2)}$，2組が ${dec(c2, 2)}$"))
    order = list(range(4))
    r.shuffle(order)
    st = [st[o] for o in order]
    truth = frozenset(LETTERS[t] for t in range(4) if st[t][1])
    assert len(truth) >= 1
    subs = [frozenset(c) for n in range(1, 5) for c in itertools.combinations(LETTERS, n)]

    def name(s):
        return "，".join(sorted(s))
    others = [s for s in subs if s != truth]
    others.sort(key=lambda s: (len(s ^ truth), r.random()))
    pick = others[:5]
    why = {}
    for s in pick:
        bad = sorted(s ^ truth)
        why[name(s)] = ("；".join(f"{x}は{'正しい' if x in truth else '誤り'}（{st[LETTERS.index(x)][2]}）" for x in bad) + "。", "相対度数・代表値の読み取りの誤り")
    rows = [[cls(lo + q * w, w), str(f1[q]), str(f2[q])] for q in range(k)] + [["計", str(N1), str(N2)]]
    tbl = table(rows, header=[f"階級（{u}）", "1組（人）", "2組（人）"], caption=FAKE)
    body = "\n".join(f"{LETTERS[t]}．{st[t][0]}" for t in range(4))
    exp = "；".join(f"{LETTERS[t]}は{'正しい' if st[t][1] else '誤り'}（{st[t][2]}）" for t in range(4))
    return mc(f"Kさんは，1組 ${N1}$ 人と2組 ${N2}$ 人の{ctx[0]}を調べ，次の度数分布表にまとめた。この表から読み取れることとして正しいものを次のA〜Dの中からすべて選んだときの組み合わせとして最も適するものを，あとの1〜6の中から1つ選び，その番号を答えなさい。ただし，最頻値は度数が最も大きい階級の階級値とする。\n{body}",
              [name(truth)] + [name(s) for s in pick], exp + f"。よって正しいのは {name(truth)}。", d=4, p=8, why=why, tbl=tbl,
              ap="人数がちがう2つの組を比べるときは，度数ではなく相対度数（累積相対度数）で比べる。中央値の階級は累積度数で何番目かを確かめる。",
              steps=[f"1組（${N1}$ 人）の中央値は13番目，2組（${N2}$ 人）の中央値は10番目と11番目の平均値。",
                     "各文に必要な相対度数・累積相対度数・階級を求める。", exp + "。", f"正しいものは {name(truth)}。"],
              alt=["相対度数の列を表に書き加えてから，1つずつ文を判定すると見落としが減る。"],
              pc=[("相対度数で比べることを理解している", 3), ("各文の正誤を正しく判断している", 3), ("正しい組み合わせを選んでいる", 2)],
              pit=["人数がちがうのに，度数をそのまま比べてしまう。", "中央値の階級を，度数が最も大きい階級と取り違える。"])


@gen("thinking_writing", 3, ["cross_unit", "computation"], rel=["JH-MATH-G1-U03"])
def c_unknown(r):
    kind = r.choice(["missing", "join", "combine"])
    if kind == "missing":
        n = r.randint(5, 8)
        name, u, a, b = r.choice(DATA_CTX[:4] + DATA_CTX[6:])
        xs = [r.randint(a, b) for _ in range(n)]
        m = r.randint(a + 1, b - 1)
        x = m * n - sum(xs[:-1])
        assert a <= x <= b and x not in xs[:-1]
        shown = xs[:-1] + ["x"]
        r.shuffle(shown)
        stem = f"次のデータは，{n}人の{name}を調べたものである。このデータの平均値は ${m}$ {u}であった。$x$ の値を求めなさい。\n{dlist(shown)}（単位：{u}）"
        e = f"合計は ${m}\\times{n}={m * n}$。${sum(xs[:-1])}+x={m * n}$ より $x={x}$。"
        expr = f"{m}*{n}-{sum(xs[:-1])}"
        eq = f"$\\dfrac{{{sum(xs[:-1])}+x}}{{{n}}}={m}$"
        v = x
    elif kind == "join":
        n = r.randint(4, 9)
        m = r.randint(50, 80)
        d = r.randint(1, 3)
        v = m + d * (n + 1)
        u = "点"
        stem = f"ある班の ${n}$ 人の数学のテストの平均点は ${m}$ 点だった。この班に1人が加わって ${n + 1}$ 人で平均点を求めると，平均点はもとより ${d}$ 点高くなった。加わった1人の得点は何点か求めなさい。"
        e = f"もとの合計は ${m}\\times{n}={m * n}$，加わった後の合計は ${m + d}\\times{n + 1}={(m + d) * (n + 1)}$。差は ${v}$ 点。"
        expr = f"{m + d}*{n + 1}-{m}*{n}"
        eq = f"$\\dfrac{{{m * n}+x}}{{{n + 1}}}={m + d}$"
    else:
        n1, n2 = r.randint(10, 30), r.randint(10, 30)
        m1, m2 = r.randint(50, 80), r.randint(50, 80)
        tot = m1 * n1 + m2 * n2
        assert n1 != n2 and m1 != m2 and tot % (n1 + n2) == 0
        v = tot // (n1 + n2)
        u = "点"
        stem = f"1組 ${n1}$ 人の数学のテストの平均点は ${m1}$ 点，2組 ${n2}$ 人の平均点は ${m2}$ 点だった。2つの組を合わせた ${n1 + n2}$ 人の平均点は何点か求めなさい。"
        e = f"合計は ${m1}\\times{n1}+{m2}\\times{n2}={tot}$。${tot}\\div{n1 + n2}={v}$（点）。"
        expr = f"({m1}*{n1}+{m2}*{n2})/{n1 + n2}"
        eq = f"$\\dfrac{{{m1}\\times{n1}+{m2}\\times{n2}}}{{{n1 + n2}}}$"
    return MARK(stem, v, e, expr, d=4, p=8, unit=u,
                ap="平均値から合計を復元する（合計＝平均値×個数）。わからない値を文字でおき，一次方程式をつくる（一次方程式の単元とのつながり）。",
                steps=["合計＝平均値×個数 の関係を使う。", f"式をつくる：{eq}。", "一次方程式を解く（または計算する）。", f"答え：${v}$ {u}。"],
                alt=["基準の値からの過不足（仮の平均との差）を合計して考える方法でも求められる。" if kind != "combine" else "2つの平均の差を人数の比で分ける考え方でも確かめられる（単純に平均の平均をとってはいけない）。"],
                pc=[("合計＝平均値×個数 を使っている", 3), ("式を正しくつくっている", 3), ("正しい値を求めている", 2)],
                pit=["2つの組の平均点をそのまま平均してしまう（人数がちがうと誤り）。" if kind == "combine" else "平均値から合計にもどすことに気づかない。"])


REASONS = [
    ("1組（30人）と2組（36人）で，記録が 20 m 以上の生徒の多さを比べるとき，度数ではなく相対度数を使う理由",
     "2つの組は人数（度数の合計）がちがうので，全体に対する割合で比べないと公平に比べられないから。",
     [("相対度数を使うと，必ず差が大きくなって比べやすくなるから。", "相対度数を使っても差が大きくなるとは限らない。目的は割合で公平に比べること。"),
      ("度数は小数で表せないので，比べることができないから。", "度数どうしは比べられるが，人数がちがうと公平な比較にならない。"),
      ("相対度数の合計はいつも人数と等しくなるから。", "相対度数の合計は $1$ である。")]),
    ("ある会社の社員10人の年収のデータに，1人だけ極端に高い年収がふくまれるとき，代表値として平均値より中央値が適している理由",
     "平均値は極端に大きい値の影響を受けて大きくなるが，中央値は並べたときの中央の値なので，その影響を受けにくいから。",
     [("中央値はいつも平均値より大きいから。", "中央値と平均値の大小は，データによって変わる。"),
      ("平均値は個数が偶数のときには求められないから。", "平均値は個数に関係なく求められる。"),
      ("中央値は最も多く現れる値だから。", "最も多く現れる値は最頻値である。")]),
    ("ペットボトルのキャップを投げる実験で，表向きになる確率を 20 回の結果ではなく 2000 回の結果から考える理由",
     "試行の回数が多くなるほど相対度数のばらつきが小さくなり，一定の値に近づくから。",
     [("20 回では，表向きの相対度数が必ず $0.5$ になってしまうから。", "20 回でも相対度数は $0.5$ になるとは限らない。"),
      ("2000 回投げると，表向きと裏向きが必ず同じ回数になるから。", "同じ回数になるとは限らない。キャップは表裏が同じ程度に出るとはいえない。"),
      ("回数が多いほど，表向きになる回数が少なくなるから。", "回数が増えると相対度数が安定するのであって，回数が減るわけではない。")]),
    ("靴屋が，次に仕入れる靴のサイズを決めるときに，売れた靴のサイズの代表値として最頻値を使う理由",
     "最も多く売れたサイズを知りたいので，最も多く現れる値である最頻値が目的に合っているから。",
     [("最頻値はいつも平均値と等しくなるから。", "最頻値と平均値は一般に等しくない。"),
      ("平均値は靴のサイズのデータでは計算できないから。", "平均値は計算できるが，実際にはないサイズになることもあり目的に合わない。"),
      ("最頻値は極端な値の影響をまったく受けないので，いつも最もよい代表値だから。", "目的によって適する代表値は変わる。いつも最頻値が最もよいとはいえない。")]),
    ("度数分布表から求めた平均値が，もとのデータから求めた平均値と一致しないことがある理由",
     "度数分布表では，各階級のデータをすべて階級値とみなして計算するので，実際の値とのずれが生じるから。",
     [("度数分布表では，データの個数が変わってしまうから。", "度数分布表にしてもデータの個数（度数の合計）は変わらない。"),
      ("度数分布表では，最大値と最小値を除いて計算するから。", "最大値・最小値を除くことはしない。"),
      ("度数分布表では，相対度数の合計が $1$ にならないから。", "相対度数の合計は $1$ になる。")]),
    ("同じデータでも，ヒストグラムの階級の幅を変えると分布の形の見え方が変わることがある理由",
     "階級の幅によって，どのデータが同じ階級にまとめられるかが変わり，各階級の度数が変わるから。",
     [("階級の幅を変えると，データの個数が変わるから。", "データの個数（度数の合計）は変わらない。"),
      ("階級の幅を変えると，データの値そのものが変わるから。", "データの値は変わらない。"),
      ("階級の幅を変えると，平均値が必ず大きくなるから。", "もとのデータの平均値は階級の幅によって変わらない。")]),
    ("あるクラスのデータで，平均値は 5.2 冊だが，中央値は 3 冊であった。このとき「半分以上の生徒は 5 冊以上読んでいる」といえない理由",
     "中央値が 3 冊なので，小さい順に並べると半分の生徒は 3 冊以下であり，5 冊以上の生徒は半分に満たないから。",
     [("平均値が 5.2 冊なので，ちょうど半分の生徒が 5.2 冊だから。", "平均値はデータの半分の位置を表す値ではない。"),
      ("中央値は最も多く現れる値なので，3 冊の生徒が最も多いから。", "中央値と最頻値を取り違えている。"),
      ("平均値と中央値の差が大きいときは，データが正しくないから。", "極端な値があると平均値と中央値は大きくちがうことがあり，データが正しくないとはいえない。")]),
    ("累積相対度数の表で，最後の階級の累積相対度数がいつも $1$ になる理由",
     "最後の階級までの度数の合計は度数の合計そのものなので，それを度数の合計でわると $1$ になるから。",
     [("最後の階級の度数は，いつも $1$ であるから。", "最後の階級の度数が $1$ とは限らない。"),
      ("相対度数は，どの階級でも $1$ より大きくなるから。", "相対度数は $0$ 以上 $1$ 以下の値である。"),
      ("階級の幅がすべて等しいから。", "階級の幅は累積相対度数が $1$ になる理由と関係ない。")]),
    ("1組と2組の記録の分布を1つのグラフで比べるとき，ヒストグラムを2つ並べるより，度数折れ線（度数分布多角形）を重ねてかくほうがよい理由",
     "度数折れ線は線で表すので，2つを同じ図に重ねてかいても見やすく，分布の山の位置や広がりのちがいを比べやすいから。",
     [("度数折れ線をかくと，データの個数が多くなるから。", "グラフの種類を変えてもデータの個数は変わらない。"),
      ("度数折れ線では，平均値をグラフから正確に読み取れるから。", "度数折れ線から平均値を正確に読み取ることはできない。"),
      ("ヒストグラムは，人数が同じ集団にしか使えないから。", "ヒストグラムは人数に関係なく使える。重ねると見にくいことが理由である。")]),
]


@gen("thinking_writing", 3, ["written_reasoning", "concept"])
def c_reason(r):
    q, right, ws = r.choice(REASONS)
    return MC(f"Kさんは，データの活用について説明する文を考えた。{q}として最も適するものを，" + SEL4, right, [(t, w, "代表値・相対度数の意味の誤解") for t, w in ws],
              f"理由：{right}", d=4, p=8,
              ap="平均値・中央値・最頻値・相対度数が，それぞれ何を表す値なのか（定義）にもどって考える。",
              steps=["説明に使われている値の定義を確認する。", "その値がもつ性質（極端な値の影響・割合で比べられる・多数回で安定する など）を考える。", "結論につながる理由を選ぶ。"],
              alt=["具体的な数値の例をつくって，選んだ理由が成り立つかを確かめる。"],
              pc=[("値の定義を正しく理解している", 4), ("結論につながる理由を正しく選んでいる", 4)],
              pit=["「いつも」「必ず」のような言い切りの文を，確かめずに選んでしまう。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

LINES4 = ["1行目", "2行目", "3行目", "4行目"]


@gen("error_correction", 4, ["common_error", "condition_check"])
def d_median(r):
    name, u, a, b = r.choice([d for d in DATA_CTX if d[3] - d[2] >= 12])
    n = r.choice([6, 8, 10, 7, 9])
    where = r.choice([0, 2, 3]) if n % 2 == 0 else r.choice([0, 2])
    for _t in range(400):
        xs = [r.randint(a, b) for _ in range(n)]
        s = sorted(xs)
        med = Fr(s[n // 2]) if n % 2 else Fr(s[n // 2 - 1] + s[n // 2], 2)
        if len(set(xs)) == n and med.denominator == 1 and xs[(n - 1) // 2] != s[(n - 1) // 2] and xs[n // 2] != s[n // 2]:
            break
    else:
        raise AssertionError("retry")
    pos_txt = f"{(n + 1) // 2}番目" if n % 2 else f"{n // 2}番目と{n // 2 + 1}番目"
    l1 = f"小さい順に並べると {dlist(s)}"
    l2 = f"データの個数は ${n}$ 個"
    l3 = f"中央値は小さい方から{pos_txt}の値"
    l4 = f"中央値は ${med}$ {u}" if n % 2 else f"中央値は $({s[n // 2 - 1]}+{s[n // 2]})\\div2={med}$ {u}"
    if where == 0:
        l1 = f"データの順に {dlist(xs)} と考える"
        wv = Fr(xs[n // 2]) if n % 2 else Fr(xs[n // 2 - 1] + xs[n // 2], 2)
        l4 = f"中央値は ${dec(wv)}$ {u}" if n % 2 else f"中央値は $({xs[n // 2 - 1]}+{xs[n // 2]})\\div2={dec(wv)}$ {u}"
        step, etype, tempt = "1行目（データを小さい順に並べていない）", "concept", "「真ん中の値」という言葉から，書かれた順のまま真ん中を見てしまう。"
    elif where == 2:
        if n % 2:
            bad = (n - 1) // 2
            l3 = f"中央値は小さい方から{bad}番目の値"
            l4 = f"中央値は ${s[bad - 1]}$ {u}"
        else:
            l3 = f"中央値は小さい方から{n // 2}番目の値"
            l4 = f"中央値は ${s[n // 2 - 1]}$ {u}"
        step, etype, tempt = "3行目（中央の位置を誤った）", "condition", "個数を2でわった数を，そのまま中央の位置と考えてしまう。"
    else:
        l4 = f"中央値は ${s[n // 2 - 1]}+{s[n // 2]}={s[n // 2 - 1] + s[n // 2]}$ {u}"
        step, etype, tempt = "4行目（2つの値の平均をとっていない）", "calculation", "中央の2つの値を見つけたことで安心し，2でわるのを忘れる。"
    sol = "\n".join(f"{i + 1}行目　{t}" for i, t in enumerate([l1, l2, l3, l4]))
    ok = {0: "1行目は正しく小さい順に並べている。", 1: "2行目のデータの個数は正しい。",
          2: f"3行目は正しい。{n}個のデータの中央は{pos_txt}である。", 3: "4行目は，3行目の位置の値を正しく使っている。"}
    why = {LINES4[i]: (ok[i], "誤りの箇所の見落とし") for i in range(4) if i != where}
    fix = f"{dlist(s)} と並べ，{pos_txt}{'の値' if n % 2 else 'の値の平均'}をとって中央値は ${med}$ {u}"
    return mc(f"〔問題〕次のデータの中央値を求めなさい。\n{dlist(xs)}（単位：{u}）\n〔Kさんの解答〕\n{sol}\nKさんの解答で，誤りが最初に生じた行として最も適するものを，" + SEL4,
              LINES4, f"誤りが最初に生じたのは{LINES4[where]}。正しくは {fix}。", d=3, p=6, keep=True, ai=where, why=why,
              err=dict(sol=sol, step=step, type=etype, tempt=tempt, fix=fix),
              ap="中央値の求め方「並べる → 個数 → 中央の位置 → 値（偶数なら2つの平均）」の各段階を1行ずつ確かめる。",
              steps=[f"小さい順に並べる：{dlist(s)}。", f"個数は ${n}$。", f"中央は{pos_txt}。", f"中央値は ${med}$ {u}。"],
              alt=["求めた中央値より小さい値と大きい値の個数が等しいかを数えて確かめる。"],
              pc=[("誤りの行を正しく指摘している", 3), ("正しい中央値を求めている", 3)],
              pit=["並べかえを省く。", "個数が偶数のとき，2つの値の平均をとり忘れる。"],
              chk=(fpy(med), fpy(med), None, "intermediate"))


@gen("error_correction", 3, ["common_error", "computation"])
def d_mean_table(r):
    ctx, w, lo, k, N, f = freq_setup(r, Ns=(20, 25, 40), k=r.randint(4, 5))
    u = ctx[1]
    cv = [lo + i * w + Fr(w, 2) for i in range(k)]
    tot = sum(c * x for c, x in zip(cv, f))
    m = tot / N
    kind = r.choice(["classes", "lower", "plain"])
    if kind == "classes":
        wv = tot / k
        sol = f"(階級値 × 度数) の合計は ${dec(tot)}$。階級は ${k}$ つなので，${dec(tot)}\\div{k}={dec(wv) or ftex(wv)}$。答え ${dec(wv) or ftex(wv)}$ {u}"
        right = f"度数の合計 ${N}$ ではなく，階級の数 ${k}$ でわっている。"
        step, etype, tempt = "わる数", "concept", "表の行の数（階級の数）が目に入りやすく，データの個数と取り違える。"
    elif kind == "lower":
        lt = sum(Fr(lo + i * w) * x for i, x in enumerate(f))
        wv = lt / N
        sol = f"各階級の値を {', '.join(str(lo + i * w) for i in range(k))} として，(値 × 度数) の合計は ${dec(lt)}$。${dec(lt)}\\div{N}={dec(wv)}$。答え ${dec(wv)}$ {u}"
        right = "各階級の値として，階級値（真ん中の値）ではなく，階級の下端の値を使っている。"
        step, etype, tempt = "各階級の値", "concept", "表の左に書かれている「〜以上」の数をそのまま使いやすい。"
    else:
        wv = sum(cv) / k
        sol = f"階級値は {', '.join(dec(c) for c in cv)}。これらの平均は ${dec(sum(cv))}\\div{k}={dec(wv) or ftex(wv)}$。答え ${dec(wv) or ftex(wv)}$ {u}"
        right = "度数を考えずに階級値の平均をとっている。各階級値に度数をかけて合計する必要がある。"
        step, etype, tempt = "合計の求め方", "concept", "「平均＝合計÷個数」を階級値だけに当てはめてしまう。"
    assert wv != m
    cands = [("Kさんの解答に誤りはない。", f"正しい平均値は ${dec(m)}$ {u}で，Kさんの答えと一致しない。", "確かめ不足"),
             ("階級値ではなく，各階級の上端の値を使うべきである。", "度数分布表の平均値では階級値（真ん中の値）を使う。", "階級値の意味の誤解"),
             ("最後に，求めた値を階級の幅でわるべきである。", "階級の幅でわる手順はない。", "平均値の求め方の誤解"),
             ("相対度数の合計でわるべきである。", "相対度数の合計は $1$ なので，わっても値は変わらず，意味のない操作である。", "相対度数の意味の誤解")]
    if kind == "lower":
        cands = cands[0:1] + cands[2:] + cands[1:2]
    fix = f"(階級値 × 度数) の合計 ${dec(tot)}$ を度数の合計 ${N}$ でわって ${dec(m)}$ {u}"
    return MC(f"〔問題〕次の度数分布表は，{grp(ctx)} ${N}$ {who(ctx)}の{ctx[0]}をまとめたものである。この表から，{ctx[0]}の平均値を求めなさい。ただし，各階級に入るデータの値はすべてその階級の階級値とする。\n〔Kさんの解答〕\n{sol}\nKさんの解答の誤りを説明したものとして最も適するものを，" + SEL4,
              right, cands, f"正しくは {fix}。", d=3, p=6, tbl=freq_tbl(ctx, w, lo, f),
              err=dict(sol=sol, step=step, type=etype, tempt=tempt, fix=fix),
              ap="度数分布表からの平均値＝(階級値 × 度数) の合計 ÷ 度数の合計。Kさんの式のどこがこの式とちがうかを探す。",
              steps=["階級値：" + "，".join(f"${dec(c)}$" for c in cv) + "。", f"(階級値 × 度数) の合計：${dec(tot)}$。", f"度数の合計 ${N}$ でわる：${dec(m)}$ {u}。"],
              alt=["求めた平均値が，最も度数の大きい階級の近くにあるかを確かめると，大きなずれに気づける。"],
              pc=[("誤りの原因を正しく指摘している", 3), ("正しい平均値を求めている", 3)],
              pit=["階級の数でわる。", "階級の下端の値を使う。"],
              chk=(f"({'+'.join(f'{fpy(c)}*{x}' for c, x in zip(cv, f))})/{N}", fpy(m), None, "intermediate"))


@gen("error_correction", 3, ["common_error", "concept"])
def d_relfreq(r):
    ctx, w, lo, k, N, f = freq_setup(r, Ns=(20, 25, 50))
    u = ctx[1]
    kind = r.choice(["over", "mode", "compare"])
    if kind == "over":
        i = r.randrange(2, k)
        bound = lo + i * w
        cnt = sum(f[i:])
        wcnt = sum(f[i + 1:])
        assert f[i] > 0
        sol = f"${bound}$ {u}以上の{'個数' if ctx[4] == '個' else '人数'}は，{cls_tex(bound, w, u)}の階級より後の階級の度数の合計で ${wcnt}$。$\\dfrac{{{wcnt}}}{{{N}}}={dec(Fr(wcnt, N), 2)}$　答え ${dec(Fr(wcnt, N), 2)}$"
        right = f"「${bound}$ {u}以上」には${bound}$ {u}ちょうどからの階級（{cls_tex(bound, w, u)}）もふくまれるのに，その階級を除いている。"
        task = f"{ctx[0]}が ${bound}$ {u}以上である割合（相対度数）"
        fix = f"$\\dfrac{{{cnt}}}{{{N}}}={dec(Fr(cnt, N), 2)}$"
        step, etype, tempt = "ふくめる階級", "condition", "「以上」と「より大きい」を同じ意味と思いやすい。"
    elif kind == "mode":
        mo = mode_idx(f)
        assert mo is not None
        cvv = lo + mo * w + Fr(w, 2)
        sol = f"度数が最も大きいのは{cls_tex(lo + mo * w, w, u)}の階級で，その度数は ${f[mo]}$。答え 最頻値は ${f[mo]}$ {u}"
        right = "最頻値として度数（個数）を答えている。最頻値はその階級の階級値で表す。"
        task = "最頻値（度数が最も大きい階級の階級値）"
        fix = f"最頻値は ${ftex(cvv)}$ {u}"
        step, etype, tempt = "答える値", "concept", "「最も多い」という言葉から，度数（人数）の大きさを答えてしまう。"
    else:
        i = r.randrange(k)
        N2 = r.choice([x for x in (20, 25, 50) if x != N])
        f2 = r.randint(1, N2 // 2)
        assert f2 != f[i] and Fr(f2, N2) != Fr(f[i], N)
        bigger_c = f2 > f[i]
        bigger_r = Fr(f2, N2) > Fr(f[i], N)
        assert bigger_c != bigger_r
        lab = cls_tex(lo + i * w, w, u)
        sol = f"{lab}の階級の度数は，表の学年が ${f[i]}$，別の学年が ${f2}$。度数の大きい{'別の学年' if bigger_c else '表の学年'}のほうが，この階級の割合が大きい。"
        right = f"度数の合計がちがう（${N}$ と ${N2}$）のに度数をそのまま比べている。相対度数で比べる必要がある。"
        task = f"{lab}の階級の割合が大きいのは，表の学年（${N}$ {who(ctx)}）と，同じ階級の度数が ${f2}$ {who(ctx)}である別の学年（${N2}$ {who(ctx)}）のどちらか"
        fix = f"相対度数は表の学年 ${dec(Fr(f[i], N), 2)}$，別の学年 ${dec(Fr(f2, N2), 2)}$ なので，{'表の学年' if not bigger_r else '別の学年'}のほうが大きい"
        step, etype, tempt = "比べる値", "concept", "度数の大小がそのまま割合の大小になると思いこみやすい。"
    cands = [("Kさんの解答に誤りはない。", f"正しくは {fix}。", "確かめ不足"),
             ("度数の合計ではなく，階級の数でわるべきである。", "相対度数は度数の合計でわる。階級の数でわるのは誤り。", "相対度数の求め方の誤解"),
             ("相対度数は百分率で答えなければならないので，100 をかけるべきである。", "相対度数は小数で表すのがふつうで，百分率にすることは誤りの原因ではない。", "表し方の誤解"),
             ("累積度数を使うべきである。", "累積度数を使うかどうかは問題の求めるものによる。ここでの誤りの原因は別にある。", "累積度数の意味の誤解")]
    return MC(f"〔問題〕次の度数分布表は，{grp(ctx)} ${N}$ {who(ctx)}の{ctx[0]}をまとめたものである。{task}を求めなさい。\n〔Kさんの解答〕\n{sol}\nKさんの解答の誤りを説明したものとして最も適するものを，" + SEL4,
              right, cands, f"正しくは {fix}。", d=3, p=6, tbl=freq_tbl(ctx, w, lo, f),
              err=dict(sol=sol, step=step, type=etype, tempt=tempt, fix=fix),
              ap="問題の条件（以上・未満，最頻値の意味，合計のちがい）をもう一度読み，Kさんの解答と照らし合わせる。",
              steps=["問題が求めているものを確認する。", "Kさんがどの値を使ったかを確認する。", f"正しくは {fix}。"],
              alt=["表に相対度数・累積相対度数の列を書き加えて，結果を確かめる。"],
              pc=[("誤りの原因を正しく指摘している", 3), ("正しい答えを求めている", 3)],
              pit=["「以上」「未満」の境目の扱いをまちがえる。", "最頻値として度数を答える。", "合計がちがう集団を度数で比べる。"])


GENERATORS = [a_relfreq, a_mean, a_median, a_mode_range, a_terms,
              b_class_mean, b_cumrel, b_hist, b_trial, b_compare,
              c_combo, c_unknown, c_reason,
              d_median, d_mean_table, d_relfreq]

GENERATORS = [_robust(g) for g in GENERATORS]
