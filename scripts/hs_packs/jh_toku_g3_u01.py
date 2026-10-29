"""単元パック：中学3年 特色検査（自己表現検査）対策　教科横断型　資料読解と論理的思考（神奈川県公立高校入試形式）。

資料・会話・場面の設定はすべてこの教材のためのオリジナルで，表とグラフの数値はすべて「架空の資料」である。
論理の問題（順番・担当・数あて・まちがった発言）は，すべての場合をプログラムで調べ（総当たり），
答えがただ1つに決まることを確かめてから出題している。数量の答えも，すべてプログラムで計算している。
"""
import itertools
import random as _random
from fractions import Fraction as Fr

from banks._common import desc, figure, mc, num, stim, table
from hs_pack_lib import board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem, tp

UNIT_ID = "JH-TOKU-G3-U01"

PREREQUISITES = [
    ("JH-MATH-G1-U07", "相対度数（割合）と代表値（平均値）。資料の数値から割合や平均を計算して比べるときに使う。"),
    ("JH-MATH-G2-U06", "場合の数を落ちなく数える方法（樹形図・表）。条件に合う並び方をすべて調べるときの土台になる。"),
    ("JH-JPN-G2-U04", "主張と根拠の関係。資料から言えること（事実）と言えないこと（推測）を区別するときに使う。"),
    ("JH-MATH-G2-U01", "文字式による説明。2けたの整数を 10a+b と表し，数の性質を調べるときに使う。"),
]
EXTENSIONS = [
    ("JH-TOKU-G3-U02", "資料から読み取った事実を根拠にして，字数の条件の中で自分の考えを書く。"),
    ("EX-KNG-MOCK-MATH", "入試の数学 問3の資料の問題や「すべて選んだときの組み合わせ」の問題で，複数の条件を一つずつ確かめる力を使う。"),
    ("HS-MATH1-U05", "高校のデータの分析では，分散・標準偏差・相関係数を使って，複数の資料をより詳しく比べる。"),
    ("HS-MATHA-U01", "高校の場合の数と確率では，条件を満たす場合を落ちなく，重なりなく数える方法を体系的に学ぶ。"),
]

FAKE = "（架空の資料）"
SEL4 = "最も適するものを次の1〜4の中から1つ選び，その番号を答えなさい。"
DT = ["data_interpretation", "thinking"]
TH = ["thinking"]
DC = ["data_interpretation", "calculation"]


# ----------------------------------------------------------------------
# 共通ヘルパー
# ----------------------------------------------------------------------

def MC(stem, right, cands, e, nw=3, **kw):
    """cands=[(誤答の文, 理由, 誤概念)]。重複を除いて nw 個の誤答を使う。正答は出力時にシャッフルされる。"""
    seen, ws = {right}, []
    for t, why, mis in cands:
        if t in seen:
            continue
        seen.add(t)
        ws.append((t, why, mis))
        if len(ws) == nw:
            break
    assert len(ws) == nw, (stem[:40], right, cands)
    return mc(stem, [right] + [w[0] for w in ws], e, why={w[0]: (w[1], w[2]) for w in ws}, **kw)


def MARK(stem, v, e, expr, **kw):
    """あいう方式（0〜9のマーク）で答える整数の問題。"""
    v = Fr(v)
    assert v >= 0 and v.denominator == 1, v
    n = int(v)
    return num(stem, str(n), e, mark=("int", n), chk=(expr, str(n), None, "answer"), **kw)


def robust(g):
    """条件に合うデータが作れなかったとき（AssertionError）は，別の乱数で作り直す。"""
    fn = g.fn

    def wrapped(r):
        for _ in range(80):
            try:
                return fn(r)
            except AssertionError:
                r = _random.Random(r.random())
        return fn(r)
    wrapped.__name__ = fn.__name__
    g.fn = wrapped
    return g


def dec(v):
    v = Fr(v)
    if v.denominator == 1:
        return str(v.numerator)
    s = f"{float(v):.6f}".rstrip("0")
    assert Fr(s) == v, v
    return s


def split_total(r, k, total=100, lo=5, hi=40, step=1):
    """合計 total（step の倍数ずつ）を k 個の異なる値に分ける。"""
    for _ in range(500):
        cuts = sorted(r.sample(range(1, total // step), k - 1))
        v = [b - a for a, b in zip([0] + cuts, cuts + [total // step])]
        v = [x * step for x in v]
        if min(v) >= lo and max(v) <= hi and len(set(v)) == k:
            return v
    raise AssertionError("split")


def bar_svg(labels, vals, unit, ymin=0, step=None, show_vals=True):
    """縦棒グラフ（SVG）。ymin>0 のときは縦軸が ymin から始まる。"""
    top = max(vals)
    step = step or (1 if top - ymin <= 10 else 2 if top - ymin <= 20 else 5)
    ymax = ((top - ymin) // step + 1) * step + ymin
    X0, Y0, PW, PH = 46, 168, 250, 140
    sc = PH / (ymax - ymin)
    n = len(vals)
    bw = PW / n
    o = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 200" width="320" height="200" font-family="serif" font-size="11">']
    y = ymin
    while y <= ymax:
        yy = Y0 - (y - ymin) * sc
        o.append(f'<line x1="{X0}" y1="{yy:.1f}" x2="{X0 + PW}" y2="{yy:.1f}" stroke="#bbb" stroke-width="0.6" stroke-dasharray="2,2"/>')
        o.append(f'<text x="{X0 - 5}" y="{yy + 4:.1f}" text-anchor="end">{y}</text>')
        y += step
    for i, (lab, v) in enumerate(zip(labels, vals)):
        x = X0 + i * bw + bw * 0.2
        h = (v - ymin) * sc
        o.append(f'<rect x="{x:.1f}" y="{Y0 - h:.1f}" width="{bw * 0.6:.1f}" height="{h:.1f}" fill="#d6e2f0" stroke="#000" stroke-width="1"/>')
        if show_vals:
            o.append(f'<text x="{x + bw * 0.3:.1f}" y="{Y0 - h - 3:.1f}" text-anchor="middle" font-size="10">{v}</text>')
        o.append(f'<text x="{x + bw * 0.3:.1f}" y="{Y0 + 15}" text-anchor="middle">{lab}</text>')
    o.append(f'<line x1="{X0}" y1="{Y0}" x2="{X0 + PW}" y2="{Y0}" stroke="#000"/><line x1="{X0}" y1="{Y0}" x2="{X0}" y2="{Y0 - PH - 6}" stroke="#000"/>')
    o.append(f'<text x="{X0 - 40}" y="{Y0 - PH - 12}">（単位：{unit}）</text></svg>')
    return "".join(o)


# ----------------------------------------------------------------------
# 論理パズルの総当たり
# ----------------------------------------------------------------------

def solve(cands, clues):
    return [c for c in cands if all(f(c) for _, f in clues)]


def build_unique(r, cands, secret, make_clue, lo=3, hi=5, tries=80):
    """secret だけが残るまで手がかりを加え，余分な手がかりを除く。総当たりで答えがただ1つであることを保証する。"""
    clues, cur = [], list(cands)
    for _ in range(tries):
        if len(cur) == 1:
            break
        c = make_clue(r)
        if c is None or not c[1](secret) or any(c[0] == x[0] for x in clues):
            continue
        nxt = [x for x in cur if c[1](x)]
        if len(nxt) < len(cur):
            clues.append(c)
            cur = nxt
    assert len(cur) == 1 and cur[0] == secret
    order = list(range(len(clues)))
    r.shuffle(order)
    for i in order:
        trial = [c for j, c in enumerate(clues) if j != i and c is not None]
        if len(solve(cands, trial)) == 1:
            clues[i] = None
    clues = [c for c in clues if c is not None]
    sol = solve(cands, clues)
    assert sol == [secret] and lo <= len(clues) <= hi, (len(clues), len(sol))
    return clues


# ---- 順番（4人）----
ORDER_SCN = [("学級の発表会で発表する順番", "発表"), ("リレーで走る順番", "リレー"), ("朝のスピーチをする順番", "スピーチ"),
             ("面接の練習を受ける順番", "面接の練習"), ("合唱コンクールでソロを歌う順番", "ソロ")]
NAMES5 = ["Aさん", "Bさん", "Cさん", "Dさん", "Eさん"]


def order_clue(names):
    def mk(r):
        t = r.random()
        X, Y = r.sample(names, 2)
        if t < 0.28:
            return (f"{X}の順番は{Y}より前である。", lambda p, X=X, Y=Y: p[X] < p[Y])
        if t < 0.48:
            return (f"{X}のすぐ次の順番が{Y}である。", lambda p, X=X, Y=Y: p[Y] == p[X] + 1)
        if t < 0.70:
            k = r.randint(1, 4)
            return (f"{X}は{k}番目ではない。", lambda p, X=X, k=k: p[X] != k)
        if t < 0.86:
            a, b = sorted((X, Y), key=names.index)
            return (f"{a}と{b}の順番は続いていない。", lambda p, a=a, b=b: abs(p[a] - p[b]) != 1)
        return (f"{X}は最初でも最後でもない。", lambda p, X=X: p[X] in (2, 3))
    return mk


def all_orders(names):
    return [dict(zip(pm, range(1, 5))) for pm in itertools.permutations(names)]


def seq_text(p):
    return "→".join(sorted(p, key=p.get))


# ---- 担当（4人×4つ）----
ASSIGN_SCN = [("文化祭の係", ["受付", "装飾", "会計", "放送"]), ("清掃の担当場所", ["教室", "廊下", "階段", "昇降口"]),
              ("班の中の役割", ["班長", "記録", "発表", "時間係"]), ("調べ学習のテーマ", ["環境", "福祉", "防災", "国際交流"]),
              ("体育祭の係", ["用具", "得点", "救護", "招集"])]


def assign_clue(names, roles):
    def mk(r):
        t = r.random()
        X, Y = r.sample(names, 2)
        P, Q = r.sample(roles, 2)
        if t < 0.35:
            return (f"{X}は{P}の担当ではない。", lambda a, X=X, P=P: a[X] != P)
        if t < 0.60:
            P, Q = sorted((P, Q), key=roles.index)
            return (f"{X}の担当は，{P}か{Q}のどちらかである。", lambda a, X=X, P=P, Q=Q: a[X] in (P, Q))
        X, Y = sorted((X, Y), key=names.index)
        if t < 0.80:
            return (f"{X}と{Y}のどちらかが{P}の担当である。", lambda a, X=X, Y=Y, P=P: P in (a[X], a[Y]))
        return (f"{P}の担当は，{X}でも{Y}でもない。", lambda a, X=X, Y=Y, P=P: P not in (a[X], a[Y]))
    return mk


def all_assign(names, roles):
    return [dict(zip(names, pm)) for pm in itertools.permutations(roles)]


# ---- 2けたの整数 ----
TWO = list(range(10, 100))


def digits(n):
    return n // 10, n % 10


def num_clue(r, kinds=None):
    t = r.choice(kinds or ["sum", "cmp", "mul", "rem", "swap", "par"])
    if t == "sum":
        s = r.randint(4, 15)
        return (f"十の位の数と一の位の数の和は{s}である。", lambda n, s=s: sum(digits(n)) == s)
    if t == "cmp":
        if r.random() < 0.5:
            return ("十の位の数は，一の位の数より大きい。", lambda n: digits(n)[0] > digits(n)[1])
        return ("十の位の数は，一の位の数より小さい。", lambda n: digits(n)[0] < digits(n)[1])
    if t == "mul":
        k = r.choice([3, 4, 6, 7, 8, 9])
        return (f"{k}の倍数である。", lambda n, k=k: n % k == 0)
    if t == "rem":
        k = r.choice([4, 5, 7])
        m = r.randint(1, k - 1)
        return (f"{k}でわると{m}あまる。", lambda n, k=k, m=m: n % k == m)
    if t == "swap":
        d = 9 * r.randint(1, 8)
        if r.random() < 0.5:
            return (f"十の位の数と一の位の数を入れかえてできる2けたの整数は，もとの数より{d}大きい。",
                    lambda n, d=d: digits(n)[1] > 0 and (10 * digits(n)[1] + digits(n)[0]) - n == d)
        return (f"十の位の数と一の位の数を入れかえてできる2けたの整数は，もとの数より{d}小さい。",
                lambda n, d=d: digits(n)[1] > 0 and n - (10 * digits(n)[1] + digits(n)[0]) == d)
    if r.random() < 0.5:
        return ("奇数である。", lambda n: n % 2 == 1)
    return ("偶数である。", lambda n: n % 2 == 0)


def pct_text(f):
    """割合 f（0〜1）を％で表す。割り切れないときは小数第1位までの概数。"""
    v = f * 100
    if v.denominator in (1, 2, 4, 5, 8, 10):
        return dec(v) + "％"
    return f"約{float(v):.1f}％"


def lst(xs):
    return "，".join(map(str, xs)) if xs else "なし"


# ----------------------------------------------------------------------
# 2つの資料（学年別の人数と割合）
# ----------------------------------------------------------------------
GRADES = ["1年生", "2年生", "3年生"]
TOPIC2 = ["地域の行事に参加したことがある", "1か月に3冊以上本を読む", "家の手伝いを毎日している",
          "将来つきたい仕事が決まっている", "ボランティア活動に参加したことがある", "毎日20分以上運動している"]


def grade_data(r, need_mismatch=False):
    """生徒数（20の倍数）と割合（5の倍数）。人数はすべて整数になる。"""
    for _ in range(300):
        n = r.sample(range(100, 221, 20), 3)
        p = r.sample(range(20, 76, 5), 3)
        c = [a * b // 100 for a, b in zip(n, p)]
        if len(set(c)) < 3:
            continue
        if need_mismatch and max(range(3), key=lambda i: p[i]) == max(range(3), key=lambda i: c[i]):
            continue
        return n, p, c
    raise AssertionError("grade_data")


def grade_tables(topic, n, p):
    t1 = table([[g, f"{a}"] for g, a in zip(GRADES, n)] + [["合計", f"{sum(n)}"]], header=["学年", "生徒数（人）"],
               caption="資料1　Kさんの学校の学年別の生徒数" + FAKE)
    t2 = table([[g, f"{b}"] for g, b in zip(GRADES, p)], header=["学年", f"「{topic}」と答えた人の割合（％）"],
               caption="資料2　全校生徒へのアンケートの結果" + FAKE)
    return t1, t2


def grade_stim(topic, n, p):
    t1, t2 = grade_tables(topic, n, p)
    return stim("TOKU-GRADE-" + "-".join(map(str, n + p)), "Kさんは，全校生徒に「" + topic + "」かどうかをたずねるアンケートを行い，次の資料1と資料2にまとめた。", "data",
                "資料1・資料2", source="オリジナル（架空の資料）", tbl=t1), t2


def grade_statements(r, topic, n, p, c):
    """(文, 正誤, 理由)。正誤はすべて数値から計算する。"""
    out = []
    G = GRADES
    imax = max(range(3), key=lambda i: c[i])
    pmax = max(range(3), key=lambda i: p[i])
    for i in range(3):
        out.append((f"「{topic}」と答えた人数が最も多いのは{G[i]}である。", i == imax,
                    f"人数は{G[0]}{c[0]}人，{G[1]}{c[1]}人，{G[2]}{c[2]}人で，最も多いのは{G[imax]}である。"))
    tot = sum(c)
    out.append((f"3つの学年を合わせると，「{topic}」と答えた人は{tot}人である。", True, f"{c[0]}+{c[1]}+{c[2]}={tot}（人）である。"))
    for dlt in r.sample([-20, -10, 10, 20, 30], 2):
        out.append((f"3つの学年を合わせると，「{topic}」と答えた人は{tot + dlt}人である。", False, f"{c[0]}+{c[1]}+{c[2]}={tot}（人）である。"))
    out.append((f"「{topic}」と答えた人の割合が最も高い{G[pmax]}は，その人数も3つの学年の中で最も多い。", pmax == imax,
                f"割合が最も高いのは{G[pmax]}（{p[pmax]}％）で，人数が最も多いのは{G[imax]}（{c[imax]}人）である。"))
    for i, j in itertools.permutations(range(3), 2):
        out.append((f"「{topic}」と答えた人数は，{G[i]}が{G[j]}の2倍以上である。", c[i] >= 2 * c[j],
                    f"{G[i]}は{c[i]}人，{G[j]}は{c[j]}人である。"))
    i, j = r.sample(range(3), 2)
    d = abs(c[i] - c[j])
    a, b = sorted((i, j))
    out.append((f"「{topic}」と答えた人数の差は，{G[a]}と{G[b]}で{d}人である。", True, f"{G[a]}は{c[a]}人，{G[b]}は{c[b]}人で，差は{d}人である。"))
    fd = abs(p[a] - p[b])
    if fd != d and fd > 0:
        out.append((f"「{topic}」と答えた人数の差は，{G[a]}と{G[b]}で{fd}人である。", False,
                    f"{fd}は割合の差（ポイント）である。人数は{G[a]}{c[a]}人，{G[b]}{c[b]}人で，差は{d}人である。"))
    q = r.choice(range(30, 71, 5))
    whole = Fr(tot, sum(n))
    if whole != Fr(q, 100):
        out.append((f"全校生徒のうち，「{topic}」と答えた人の割合は{q}％より高い。", whole > Fr(q, 100),
                    f"全校では{tot}÷{sum(n)}×100＝{pct_text(whole)}で，{q}％より{'高い' if whole > Fr(q, 100) else '低い'}。"))
    return out


# ======================================================================
# 授業プリントの例題（答えをプログラムで確かめる）
# ======================================================================

EX1_NAMES = ["Aさん", "Bさん", "Cさん", "Dさん"]
EX1_CLUES = [("Bさんの順番はDさんより前である。", lambda p: p["Bさん"] < p["Dさん"]),
             ("Aさんのすぐ次の順番がCさんである。", lambda p: p["Cさん"] == p["Aさん"] + 1),
             ("Dさんは4番目ではない。", lambda p: p["Dさん"] != 4)]
_ex1 = solve(all_orders(EX1_NAMES), EX1_CLUES)
assert len(_ex1) == 1 and seq_text(_ex1[0]) == "Bさん→Dさん→Aさん→Cさん", _ex1

EX3_CLUES = [("十の位の数と一の位の数の和は11である。", lambda n: sum(digits(n)) == 11),
             ("十の位の数は，一の位の数より大きい。", lambda n: digits(n)[0] > digits(n)[1]),
             ("3の倍数ではない。", lambda n: n % 3 != 0),
             ("7でわると1あまる。", lambda n: n % 7 == 1)]
_ex3 = solve(TWO, EX3_CLUES)
assert _ex3 == [92], _ex3
assert solve(TWO, EX3_CLUES[:1]) == [29, 38, 47, 56, 65, 74, 83, 92]
assert solve(TWO, EX3_CLUES[:2]) == [65, 74, 83, 92]
assert solve(TWO, EX3_CLUES[:3]) == [65, 74, 83, 92]  # 和が11なので3の倍数はない（3の条件は役に立たない）

# 例題2：1年120人・40％，2年160人・35％，3年140人・50％
_n2, _p2 = [120, 160, 140], [40, 35, 50]
_c2 = [a * b // 100 for a, b in zip(_n2, _p2)]
assert _c2 == [48, 56, 70] and sum(_c2) == 174 and sum(_n2) == 420


# ======================================================================
# 授業プリント
# ======================================================================

LESSON = lesson(
    goals=["表・グラフ・会話文など複数の資料から必要な数値を選び出し，組み合わせて判断することができる。",
           "順番・担当・数あてなどの条件を表に整理し，すべての場合を確かめて，答えがただ1つに決まることを説明できる。",
           "資料から言えること（事実）と言えないこと（推測・決めつけ）を区別し，割合と人数の取り違えなどの誤りを指摘できる。"],
    duration=50,
    readiness=["割合（％）・平均を求める計算（小学校5年・中学1年）ができる。",
               "表やグラフの題・単位・目盛りを確かめてから数値を読む習慣がある。",
               "樹形図や表を使って，場合を落ちなく数えることができる（中学2年 確率）。",
               "2けたの整数を 10a+b と表すことができる（中学2年 文字式）。"],
    flow=[("導入：この問題，何を使えば解ける？", 5, "資料が2つある問題を見せ，1つの資料だけでは答えが出ないことに気づかせる"),
          ("複数の資料を組み合わせる", 12, "割合×全体＝人数，合計÷人数＝平均の考え方で資料1・資料2を統合する（例題2）"),
          ("条件を表に整理する", 15, "順番の問題を表で整理し，ただ1つに決まることを確かめる（例題1）"),
          ("数の条件を順にしぼる", 10, "候補を書き出し，条件で消していく（例題3）"),
          ("まとめと確認", 8, "事実と推測の区別・確認問題・問題プリントの課題指示")],
    sections=[
        intro("in1", "特色検査の「資料読解」と「論理的思考」",
              "特色検査（自己表現検査）では，教科の枠をこえた問題が出されます。表やグラフ，生徒どうしの会話などの複数の資料を読み比べたり，"
              "いくつかの条件から順番や組み合わせを決めたりする問題です。特別な知識よりも，「資料のどこを見るか」「条件をどう整理するか」という"
              "考え方の手順が問われます。この単元では，資料を正確に読み，必要な数値を組み合わせ，条件から結論を導く手順を身につけます。",
              bullets=["資料読解：題・単位・調査の対象を確かめ，必要な数値を選び出す", "統合：2つ以上の資料を組み合わせて，1つの資料からは出ない答えを出す",
                       "条件整理：条件を表や図に整理し，すべての場合を確かめる", "検証：答えが条件をすべて満たし，ほかに答えがないことを確かめる"],
              points=[tp("資料1（人数）と資料2（割合）を見せ，「人数が最も多い学年」はどちらか一方の資料だけでは決められないことに気づかせる。",
                         ask="資料2だけで「答えた人数が最も多い学年」が分かるか。", expect="分からない。学年ごとの生徒数がちがうので，人数を計算する必要がある。",
                         timing="導入の冒頭")]),
        definition("df1", "資料を読むときの基本",
                   "資料の問題では，数値を読む前に，次の項目を確かめます。とくに，割合（％）と人数を取り違えないことが大切です。",
                   formula="人数＝全体の人数×割合　　平均＝合計÷個数（人数）",
                   bullets=["① 題：何について，だれを対象に調べたものか", "② 単位：人・％・百人・kg など（グラフの縦軸の単位と目盛りの始まり）",
                            "③ 比べる相手：同じ人数の集団どうしか，調べた時期はいつか", "④ 事実と推測：資料から言えるのは数値が示すことだけ。理由や将来のことは，資料だけでは言えない"],
                   conditions=["割合が高くても，全体の人数が少なければ，人数は少ないことがある。",
                               "グラフの縦軸が0から始まっていないときは，棒の高さの比が数量の比にならない。",
                               "人数がちがう集団の平均を合わせるときは，平均どうしをそのまま平均してはいけない。"],
                   points=[tp("「200人の30％」と「400人の20％」を計算させ，割合と人数のちがいを実感させる。",
                              ask="200人の30％と400人の20％では，どちらの人数が多いか。", expect="60人と80人で，400人の20％のほうが多い。",
                              caution="％の大小だけで人数を比べる生徒が多い。必ず人数に直してから比べさせる。")]),
        theorem("th1", "条件整理の手順（答えがただ1つであることの確かめ方）",
                "条件を表に整理 → 確実に決まるところから決める → 残りを場合分け → すべての条件で検算 → ほかの場合がないことを確認",
                ["「〜ではない」という条件は，表に×を書きこむ。", "「すぐ次」「となり」のように2人をまとめる条件は，ひとかたまりとして並べ方を数える。",
                 "場合分けをしたら，すべての場合を最後まで調べる（途中でやめない）。",
                 "答えが見つかっても，ほかの場合が条件に合わないことを確かめて，はじめて「ただ1つに決まる」と言える。"],
                body="数の条件では，まず候補を書き出し，条件を1つずつ当てはめて消していきます。どの条件でどの数が消えたかを書いておくと，見直しができます。",
                proof=["2けたの整数の十の位を a，一の位を b とすると，その数は 10a+b，入れかえた数は 10b+a と表せる。",
                       "差は (10a+b)−(10b+a)＝9a−9b＝9(a−b) である。",
                       "a−b は整数なので，入れかえた数ともとの数の差は必ず9の倍数になる。",
                       "したがって，「入れかえると○○大きい」という条件の○○が9の倍数でなければ，そのような数はない。"],
                points=[tp("4人の並び方は全部で 4×3×2×1＝24 通りしかないことを確認し，「すべての場合を調べる」ことが現実にできると実感させる。",
                           ask="4人の順番の決め方は全部で何通りあるか。", expect="24通り。")]),
        derivation("dv1", "全体の平均を求める式の導き方（平均の平均ではいけない理由）",
                   ["平均＝合計÷人数 なので，合計＝平均×人数 である。",
                    "1組（30人）の平均が60点なら合計は 60×30＝1800点，2組（20人）の平均が70点なら合計は 70×20＝1400点。",
                    "全体の合計は 1800＋1400＝3200点，全体の人数は 30＋20＝50人。",
                    "全体の平均は 3200÷50＝64点である。",
                    "一方，(60＋70)÷2＝65点とすると，人数が少ない2組の点数を，人数が多い1組と同じ重さで数えたことになり，正しくない。",
                    "したがって，人数がちがう集団をまとめるときは，いったん合計に直してから全体の人数でわる。"],
                   body="この考え方は，割合をまとめるとき（各学年の％から全校の％を求めるとき）にも同じように使います。",
                   points=[tp("2つの組の人数が同じときだけ，(60＋70)÷2 でも正しくなる理由を考えさせる。", timing="導出の最後")]),
        example("ex1", "例題1　条件から順番を決める",
                "Aさん，Bさん，Cさん，Dさんの4人が，発表の順番を決めた。次の条件がすべて成り立つとき，4人の順番を答えなさい。\n"
                "・Bさんの順番はDさんより前である。\n・Aさんのすぐ次の順番がCさんである。\n・Dさんは4番目ではない。",
                ["「AさんのすぐあとにCさん」なので，A・Cをひとかたまり［AC］として考える。［AC］の位置は1・2番目，2・3番目，3・4番目の3通り。",
                 "［AC］が1・2番目：残りの3・4番目にB，Dの順（BがDより前）→ Dが4番目になり，条件に合わない。",
                 "［AC］が2・3番目：1番目と4番目にB，D → BがDより前なので D が4番目になり，条件に合わない。",
                 "［AC］が3・4番目：1・2番目にB，Dの順 → B→D→A→C。すべての条件を満たす。",
                 "ほかの場合はすべて条件に合わないので，順番はただ1つに決まる。"],
                "Bさん→Dさん→Aさん→Cさん",
                thinking="2人をまとめる条件（すぐ次）から場合分けをすると，場合の数が少なくてすむ。",
                points=[tp("場合分けの3通りを表にして板書し，×になった理由（どの条件に反するか）を書きこませる。")],
                misconceptions=[("条件に合う並び方が1つ見つかったので，答えはそれで決まりである。", "ほかの並び方が条件に合わないことを確かめて，はじめてただ1つに決まると言える。")]),
        example("ex2", "例題2　2つの資料を組み合わせる",
                "資料1：生徒数は1年生120人，2年生160人，3年生140人。資料2：「地域の行事に参加したことがある」と答えた人の割合は，1年生40％，2年生35％，3年生50％。"
                "（架空の資料）　参加したことがある人数が最も多い学年と，全校での人数を答えなさい。",
                ["人数＝生徒数×割合 で学年ごとの人数を求める：1年生 120×0.4＝48人，2年生 160×0.35＝56人，3年生 140×0.5＝70人。",
                 "最も多いのは3年生（70人）。", "全校の人数は 48＋56＋70＝174人。",
                 "参考：全校の割合は 174÷420 で約41％。各学年の％の平均（約41.7％）とは一致しない。"],
                "3年生，174人",
                thinking="資料2の％だけでは人数は比べられない。資料1の生徒数と組み合わせて人数に直す。",
                points=[tp("「2年生は割合が最も低いが，人数は1年生より多い」ことに気づかせ，割合と人数のちがいを確認する。")],
                misconceptions=[("割合が最も低い2年生は，人数も最も少ない。", "2年生は56人で，1年生の48人より多い。生徒数がちがうので割合だけでは決められない。")]),
        example("ex3", "例題3　数の条件で候補をしぼる",
                "2けたの整数について，次のヒントがある。「十の位の数と一の位の数の和は11」「十の位の数は一の位の数より大きい」「7でわると1あまる」。この整数を求めなさい。",
                ["和が11の2けたの整数を書き出す：29，38，47，56，65，74，83，92。",
                 "十の位が一の位より大きいもの：65，74，83，92。",
                 "7でわると1あまるか調べる：65÷7＝9あまり2，74÷7＝10あまり4，83÷7＝11あまり6，92÷7＝13あまり1。",
                 "条件に合うのは92だけである。"],
                "92",
                thinking="最初に候補が少なくなる条件（和が11）で書き出し，残りの条件で1つずつ消す。",
                points=[tp("どの条件でどの数が消えたかを表に書かせ，見直しができる答案の書き方を示す。", timing="例題3の後")]),
        board("bd1", "板書案",
              [("① 資料を読む", ["題・単位・対象を確認", "人数＝全体×割合", "平均＝合計÷人数", "縦軸の始まりに注意", "事実と推測を分ける"]),
               ("② 条件を整理する", ["表に○×を書く", "「すぐ次」はひとかたまり", "場合分けは最後まで", "全条件で検算", "ほかの場合がないか確認"]),
               ("③ 数の条件", ["候補を書き出す", "1つずつ消す", "入れかえの差＝9(a−b)", "消した理由をメモ", "答えを全ヒントで確認"])],
              points=[tp("②の列を「条件整理チェックリスト」としてノートに写させ，問題プリントの C・D で使わせる。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("資料の問題では，選択肢を読む前に，題・単位・対象に印をつけさせる。", ask="資料2の数値の単位は何か。", expect="％（割合）。"),
               tp("「すべて選んだときの組み合わせ」の問題では，A〜Dの1つ1つに○×をつけてから組み合わせを選ばせる。", caution="途中で正しそうな組み合わせを選んでしまい，残りの確認を省く生徒が多い。"),
               tp("論理の問題では，答えが1つ見つかっても終わりにせず，ほかの場合がないかを確かめさせる。", timing="例題1の後"),
               tp("「理由」「これからどうなるか」は資料からは読み取れないことを，具体的な選択肢で確認させる。"),
               tp("会話文の空欄の問題では，空欄の前後の発言から，何を求めればよいか（人数か割合か，差か合計か）を先に確かめさせる。", timing="問題プリントB の前")],
              misconceptions=[("割合が高いほうが人数も多い。", "全体の人数がちがえば，割合が高くても人数が少ないことがある。"),
                              ("人数のちがう組の平均を合わせるときは，平均どうしを平均すればよい。", "合計に直して全体の人数でわる。"),
                              ("グラフの棒の高さが2倍なら，数量も2倍である。", "縦軸が0から始まっていないときは，高さの比と数量の比は一致しない。"),
                              ("条件に合う答えが1つ見つかれば，それが唯一の答えである。", "すべての場合を調べて，ほかの答えがないことを確かめる必要がある。")]),
        summary("sm1", "まとめ",
                ["資料は，題・単位・対象を確かめてから読む。割合と人数，平均と合計を区別し，必要なら資料を組み合わせて計算する。",
                 "条件の問題は，表に整理し，確実なところから決め，残りを場合分けしてすべて調べる。最後に，答えがただ1つであることを確かめる。",
                 "資料から言えるのは数値が示す事実だけで，理由や将来の予想は言えない。"]),
        check("ck1", "確認問題",
              [("生徒数150人の学年で，ある質問に「はい」と答えた人が40％のとき，「はい」と答えた人は何人か。", "150×0.4＝60（人）"),
               ("30人の組の平均が60点，20人の組の平均が70点のとき，2つの組を合わせた平均は何点か。", "(1800＋1400)÷50＝64（点）"),
               ("2けたの整数の十の位と一の位を入れかえた数ともとの数の差が，必ず9の倍数になる理由を式で示しなさい。", "(10a＋b)−(10b＋a)＝9(a−b) で，a−b は整数だから。")]),
    ])


# ======================================================================
# 問題ジェネレータ
# ======================================================================

# ---------------------------- A 基本確認 ----------------------------

SHARE_SCN = [
    dict(who="図書委員会", what="ある月の分類別の図書の貸出冊数", m="貸出冊数", u="冊", cats=["物語・小説", "科学", "歴史", "スポーツ・趣味", "その他"]),
    dict(who="生徒会", what="給食の人気メニューの投票結果", m="票数", u="票", cats=["カレーライス", "あげパン", "焼きそば", "ハンバーグ", "その他"]),
    dict(who="保健委員会", what="全校生徒の通学方法", m="人数", u="人", cats=["徒歩", "自転車", "バス", "電車", "その他"]),
    dict(who="環境委員会", what="ある週に回収した資源ごみの種類別の個数", m="個数", u="個", cats=["ペットボトル", "アルミ缶", "スチール缶", "びん", "紙パック"]),
    dict(who="放送委員会", what="昼の放送で流してほしい曲の種類のアンケート結果", m="人数", u="人", cats=["J-POP", "アニメの曲", "クラシック", "洋楽", "その他"]),
]


@robust
@gen("basic_check", 4, ["computation", "concept"])
def a_share(r):
    s = r.choice(SHARE_SCN)
    T = r.choice([200, 300, 400, 500, 600])
    p = split_total(r, 5, lo=5, hi=40)
    c = [T * x // 100 for x in p]
    tbl = table([[k, f"{v}"] for k, v in zip(s["cats"], c)] + [["合計", f"{T}"]], header=["種類", f"{s['m']}（{s['u']}）"],
                caption=f"資料1　{s['what']}" + FAKE)
    if r.random() < 0.55:
        i = r.randrange(5)
        stem = f"{s['who']}のKさんは，{s['what']}を調べ，次の資料1にまとめた。資料1で，「{s['cats'][i]}」の{s['m']}は，合計の何％にあたるか求めなさい。"
        v, expr = p[i], f"{c[i]}*100/{T}"
        st = [f"「{s['cats'][i]}」は{c[i]}{s['u']}，合計は{T}{s['u']}。", f"割合＝{c[i]}÷{T}＝{dec(Fr(c[i], T))}", f"百分率にすると {p[i]}％。"]
    else:
        i, j = sorted(r.sample(range(5), 2))
        stem = (f"{s['who']}のKさんは，{s['what']}を調べ，次の資料1にまとめた。資料1で，「{s['cats'][i]}」と「{s['cats'][j]}」の{s['m']}を合わせると，"
                f"合計の何％にあたるか求めなさい。")
        v, expr = p[i] + p[j], f"({c[i]}+{c[j]})*100/{T}"
        st = [f"2つを合わせると {c[i]}＋{c[j]}＝{c[i] + c[j]}{s['u']}。", f"割合＝{c[i] + c[j]}÷{T}＝{dec(Fr(c[i] + c[j], T))}", f"百分率にすると {v}％。"]
    return MARK(stem, v, f"{st[-1]}", expr, d=1, k=DC, tbl=tbl,
                ap="割合＝部分÷全体。全体（合計）が何かを資料で確かめ，最後に100倍して％にする。",
                steps=st, alt=[f"合計{T}{s['u']}の1％は{T // 100}{s['u']}なので，{s['m']}を{T // 100}でわっても％が求められる。"],
                pc=[("部分と全体を正しく選んでいる", 1), ("百分率に直している", 1)],
                pit=["全体ではなく，ほかの項目の値でわってしまう。", "100倍するのを忘れて小数のまま答える。"])


BAR_SCN = [
    dict(what="ある市の市民プールの月別利用者数", labels=["6月", "7月", "8月", "9月", "10月"], unit="百人", base=100, bu="人", sub="利用者数"),
    dict(what="Kさんの学校の図書室の月別来室者数", labels=["4月", "5月", "6月", "7月", "9月"], unit="十人", base=10, bu="人", sub="来室者数"),
    dict(what="ある商店街の祭りの来場者数", labels=["1年目", "2年目", "3年目", "4年目", "5年目"], unit="百人", base=100, bu="人", sub="来場者数"),
    dict(what="ある駅の自転車置き場の曜日別利用台数", labels=["月", "火", "水", "木", "金"], unit="十台", base=10, bu="台", sub="利用台数"),
    dict(what="ある公園の花だんで1週間ごとに咲いた花の数", labels=["1週目", "2週目", "3週目", "4週目", "5週目"], unit="十本", base=10, bu="本", sub="咲いた花の数"),
]


def bar_statements(s, v):
    L, B, bu, sub = s["labels"], s["base"], s["bu"], s["sub"]
    out = []
    mx = max(range(5), key=lambda i: v[i])
    for i in range(5):
        out.append((f"{sub}が最も多いのは{L[i]}である。", i == mx, f"最も多いのは{L[mx]}（{v[mx] * B}{bu}）である。"))
    diffs = [v[i + 1] - v[i] for i in range(4)]
    dm = max(range(4), key=lambda i: diffs[i])
    for i in range(4):
        out.append((f"{L[i]}から{L[i + 1]}にかけて，{sub}は減っている。", diffs[i] < 0, f"{L[i]}は{v[i] * B}{bu}，{L[i + 1]}は{v[i + 1] * B}{bu}である。"))
        if diffs[dm] > 0 and diffs.count(diffs[dm]) == 1:
            out.append((f"となり合う期間で比べると，{sub}の増え方が最も大きいのは{L[i]}から{L[i + 1]}にかけてである。", i == dm,
                        f"増え方が最も大きいのは{L[dm]}から{L[dm + 1]}にかけて（{diffs[dm] * B}{bu}増）である。"))
    for i, j in itertools.permutations(range(5), 2):
        if v[i] != 2 * v[j]:
            out.append((f"{L[i]}の{sub}は，{L[j]}の{sub}の2倍以上である。", v[i] >= 2 * v[j], f"{L[i]}は{v[i] * B}{bu}，{L[j]}は{v[j] * B}{bu}である。"))
    S = sum(v)
    for t in (S - 3, S + 2, S - 1):
        out.append((f"5つの期間の{sub}の合計は，{t * B}{bu}より多い。", S > t, f"合計は{S * B}{bu}である。"))
    return out


@robust
@gen("basic_check", 4, ["concept", "application"])
def a_bar(r):
    s = r.choice(BAR_SCN)
    v = [r.randint(3, 18) for _ in range(5)]
    assert len(set(v)) >= 4
    pool = bar_statements(s, v)
    tr = [x for x in pool if x[1]]
    fa = [x for x in pool if not x[1]]
    assert tr and len(fa) >= 3
    ok = r.choice(tr)
    wr = r.sample(fa, 3)
    fig = figure(f"グラフ1　{s['what']}（縦棒グラフ）", bar_svg(s["labels"], v, s["unit"]), caption=f"グラフ1　{s['what']}" + FAKE)
    return MC(f"グラフ1は，{s['what']}を表したものである。グラフ1から読み取れることとして{SEL4}", ok[0],
              [(w[0], f"誤り。{w[2]}", "グラフの読み取りの誤り") for w in wr], f"正しい。{ok[2]}", d=1, k=["data_interpretation"], fig=fig,
              ap=f"縦軸の単位が「{s['unit']}」であることを確かめ，目盛りの値を実際の数に直してから選択肢と比べる。",
              steps=[f"縦軸の単位（{s['unit']}）を確かめる。", "各期間の値を読み取る：" + "，".join(f"{a} {b * s['base']}{s['bu']}" for a, b in zip(s["labels"], v)) + "。",
                     "選択肢を1つずつ数値と照らし合わせる。", f"答え：{ok[0]}"],
              alt=["誤りの選択肢について，どの数値とくい違うかを書きこんでおくと，見直しのときに根拠を確かめられる。"],
              pc=[("単位を確かめて数値を読み取っている", 1), ("正しい選択肢を選んでいる", 1)],
              pit=["縦軸の単位（百人・十台など）を見落とし，目盛りの数をそのまま人数とする。", "増えた量と，その時点の量を取り違える。"])


@robust
@gen("basic_check", 4, ["condition_check", "concept"])
def a_order(r):
    what, short = r.choice(ORDER_SCN)
    names = sorted(r.sample(NAMES5, 4), key=NAMES5.index)
    cands = all_orders(names)
    secret = r.choice(cands)
    clues = build_unique(r, cands, secret, order_clue(names), lo=3, hi=5)
    k = r.randint(1, 4)
    ans = next(x for x in names if secret[x] == k)
    seq = seq_text(secret)
    body = "\n".join("・" + c[0] for c in clues)
    return MC(f"{'，'.join(names)}の4人が，{what}を決めた。次の〔条件〕がすべて成り立つとき，{k}番目になる人として{SEL4}\n〔条件〕\n{body}",
              ans, [(x, f"条件をすべて満たす順番は「{seq}」の1通りだけで，{x}は{secret[x]}番目である。", "条件の整理不足") for x in names if x != ans],
              f"条件をすべて満たす順番は「{seq}」の1通りだけである。{k}番目は{ans}。", d=2, k=TH,
              ap="「すぐ次」のように2人をまとめる条件や，「〜番目ではない」のように位置をしぼる条件から使い，表に整理する。",
              steps=["条件を1つずつ表に書きこむ（〜番目ではない → ×）。", "2人をまとめる条件があれば，ひとかたまりとして置き方を場合分けする。",
                     "残りの条件で場合を消していく。", f"残る順番は「{seq}」の1通り。{k}番目は{ans}。"],
              alt=[f"選んだ順番「{seq}」を条件の1つ1つに当てはめ，すべて成り立つことを確かめる。"],
              pc=[("条件を表などに整理している", 1), ("正しい人を選んでいる", 1)],
              pit=["「すぐ次」を「より後」と同じ意味に読んでしまう。", "条件に合う順番を1つ見つけた時点で，ほかの場合を調べずに終える。"])


FACT_SCN = [
    dict(q="休日に最も長い時間を使っていること", cats=["スポーツ", "読書", "ゲーム・動画", "家族との外出"]),
    dict(q="家庭での学習で主に使うもの", cats=["紙の教科書・問題集", "タブレット端末", "参考書", "塾の教材"]),
    dict(q="地域の防災訓練への参加", cats=["毎回参加する", "ときどき参加する", "参加したことがない", "訓練を知らない"]),
    dict(q="ごみを減らすために心がけていること", cats=["マイバッグを使う", "水筒を持ち歩く", "食べ残しをしない", "特にしていない"]),
]


@robust
@gen("basic_check", 4, ["concept", "condition_check"])
def a_fact(r):
    s = r.choice(FACT_SCN)
    v1 = split_total(r, 4, lo=8, hi=45)
    v2 = split_total(r, 4, lo=8, hi=45)
    assert all(a != b for a, b in zip(v1, v2))
    tbl = table([[c, f"{a}", f"{b}"] for c, a, b in zip(s["cats"], v1, v2)], header=["項目", "3年前（％）", "今年（％）"],
                caption=f"資料1　ある市の中学生への調査「{s['q']}」" + FAKE)
    i = r.randrange(4)
    d = v2[i] - v1[i]
    c = s["cats"][i]
    true_s = f"「{c}」と答えた人の割合は，3年前から今年にかけて{abs(d)}ポイント{'上がって' if d > 0 else '下がって'}いる。"
    j = r.choice([x for x in range(4) if x != i])
    dj = v2[j] - v1[j]
    false_s = f"「{s['cats'][j]}」と答えた人の割合は，3年前から今年にかけて{abs(dj) + r.choice([3, 4, 5])}ポイント{'上がって' if dj > 0 else '下がって'}いる。"
    cause = f"「{c}」と答えた人の割合が変わったのは，中学生の好みや考え方が変わったからである。"
    pred = f"これから先も，「{c}」と答える人の割合は{'上がり' if d > 0 else '下がり'}続けるだろう。"
    return MC(f"資料1は，ある市の中学生に「{s['q']}」をたずねた結果である。資料1から読み取れる事実として{SEL4}", true_s,
              [(false_s, f"誤り。「{s['cats'][j]}」は{v1[j]}％から{v2[j]}％で，変化は{abs(dj)}ポイントである。", "数値の読み誤り"),
               (cause, "変化の理由は資料1には示されていない。資料から言えない推測である。", "事実と推測の混同"),
               (pred, "将来のことは資料1からは分からない。資料から言えない予想である。", "事実と予想の混同")],
              f"正しい。「{c}」は{v1[i]}％から{v2[i]}％になり，{abs(d)}ポイント{'上がって' if d > 0 else '下がって'}いる。資料から言えるのは数値が示す事実だけである。",
              d=2, k=DT, tbl=tbl,
              ap="資料に書かれている数値だけで確かめられる文かどうかを考える。「〜からである」（理由）や「〜だろう」（予想）は，資料だけでは言えない。",
              steps=["それぞれの文が，事実・理由・予想のどれを述べているかを分ける。", "事実を述べている文は，数値で正誤を確かめる。",
                     f"「{c}」：{v1[i]}％ → {v2[i]}％ で {abs(d)}ポイントの変化。", f"答え：{true_s}"],
              alt=["理由や予想を述べた文に「資料のどこを見ればそう言えるか」と問いかけ，根拠となる数値がないことを確かめる。"],
              pc=[("事実と推測を区別している", 1), ("正しい事実を選んでいる", 1)],
              pit=["もっともらしい理由が書かれていると，資料から言えることだと思いこむ。", "ポイント（％の差）の計算をまちがえる。"])


PLAN_SCN = [("レンタサイクル", "時間", "時間"), ("市民体育館の卓球台の貸し出し", "時間", "時間"), ("公民館の会議室の利用", "時間", "時間"),
            ("ボート乗り場の貸しボート", "時間", "時間")]


@robust
@gen("basic_check", 4, ["computation", "cross_unit"], rel=["JH-MATH-G1-U03", "JH-MATH-G2-U03"])
def a_plan(r):
    name, u, _ = r.choice(PLAN_SCN)
    b1, b2 = sorted(r.sample(range(100, 801, 100), 2))
    r2 = r.choice([100, 150, 200])
    x0 = r.randint(2, 6)
    assert (b2 - b1) % x0 == 0
    r1 = r2 + (b2 - b1) // x0
    assert r1 % 10 == 0 and r1 <= 600
    f = r.choice(range(800, 3001, 100))
    tbl = table([["プランA", f"{b1}円", f"{r1}円"], ["プランB", f"{b2}円", f"{r2}円"], ["プランC", f"{f}円", "0円（何時間でも同じ）"]],
                header=["プラン", "基本料金", f"1{u}あたりの料金"], caption=f"資料1　{name}の料金表" + FAKE)
    if r.random() < 0.5:
        stem = f"資料1は，{name}の料金表である。プランAとプランBの料金が等しくなるのは，何{u}利用したときか求めなさい。ただし，利用する時間は1{u}単位とする。"
        e = f"{b1}＋{r1}x＝{b2}＋{r2}x より {r1 - r2}x＝{b2 - b1}，x＝{x0}。"
        return MARK(stem, x0, e, f"({b2}-{b1})/({r1}-{r2})", d=2, k=DC, tbl=tbl,
                    ap=f"利用時間を x {u}として，プランAとプランBの料金を x の式で表し，等しいとおいて方程式を解く。",
                    steps=[f"プランA：{b1}＋{r1}x（円），プランB：{b2}＋{r2}x（円）。", f"{b1}＋{r1}x＝{b2}＋{r2}x", f"{r1 - r2}x＝{b2 - b1}", f"x＝{x0}"],
                    alt=[f"{x0}{u}のとき，A は {b1 + r1 * x0}円，B は {b2 + r2 * x0}円で等しいことを代入して確かめる。",
                         f"1{u}ごとに A と B の差が {r1 - r2}円ずつ縮まり，はじめの差 {b2 - b1}円がなくなるのは {x0}{u}後，と考えてもよい。"],
                    pc=[("料金を式で表している", 1), ("方程式を正しく解いている", 1)],
                    pit=["基本料金を忘れて，1時間あたりの料金だけで比べる。"])
    h = r.randint(1, 8)
    costs = {"A": b1 + r1 * h, "B": b2 + r2 * h, "C": f}
    best = min(costs.values())
    assert list(costs.values()).count(best) == 1
    bp = min(costs, key=costs.get)
    stem = f"資料1は，{name}の料金表である。{h}{u}利用するとき，プランA〜Cのうち最も安いプランの料金は何円か求めなさい。"
    e = f"A：{b1}＋{r1}×{h}＝{costs['A']}円，B：{b2}＋{r2}×{h}＝{costs['B']}円，C：{f}円。最も安いのはプラン{bp}で{best}円。"
    bexpr = {"A": f"{b1}+{r1}*{h}", "B": f"{b2}+{r2}*{h}", "C": f"{f}"}[bp]
    return MARK(stem, best, e, bexpr, d=2, k=DC, tbl=tbl,
                ap="料金＝基本料金＋1時間あたりの料金×時間。3つのプランの料金をそれぞれ計算して比べる。",
                steps=[f"プランA：{b1}＋{r1}×{h}＝{costs['A']}（円）", f"プランB：{b2}＋{r2}×{h}＝{costs['B']}（円）", f"プランC：{f}（円）", f"最も安いのはプラン{bp}の{best}円。"],
                alt=["料金を表すグラフ（直線）をかき，利用時間のところで最も下にある直線を読み取って確かめる。"],
                pc=[("3つのプランの料金を計算している", 1), ("最も安い料金を選んでいる", 1)],
                pit=["基本料金を足し忘れる。", "最も安いプランの名前ではなく，2番目に安い料金を答える。"])


# ---------------------------- B 標準演習 ----------------------------

@robust
@gen("standard_practice", 4, ["application", "computation"])
def b_two(r):
    topic = r.choice(TOPIC2)
    n, p, c = grade_data(r)
    st, t2 = grade_stim(topic, n, p)
    pool = grade_statements(r, topic, n, p, c)
    tr = [x for x in pool if x[1]]
    fa = [x for x in pool if not x[1]]
    assert tr and len(fa) >= 3
    ok = r.choice(tr)
    wr = r.sample(fa, 3)
    return MC(f"資料1と資料2から読み取れることとして{SEL4}", ok[0], [(w[0], f"誤り。{w[2]}", "資料の統合の誤り") for w in wr],
              f"正しい。{ok[2]}", d=3, k=DT, stim=st, tbl=t2,
              ap="資料2の割合（％）と資料1の生徒数を組み合わせ，学年ごとの人数（生徒数×割合）を先に求めておく。",
              steps=[f"人数＝生徒数×割合：{GRADES[0]} {n[0]}×{p[0]}％＝{c[0]}人，{GRADES[1]} {n[1]}×{p[1]}％＝{c[1]}人，{GRADES[2]} {n[2]}×{p[2]}％＝{c[2]}人。",
                     "選択肢が人数・割合のどちらについて述べているかを確かめる。", "求めた人数や資料の割合と照らし合わせて正誤を判断する。", f"答え：{ok[0]}"],
              alt=["学年ごとの人数を表に書き加え，資料1・資料2・人数の3列で選択肢を確かめる。"],
              pc=[("学年ごとの人数を正しく求めている", 2), ("正しい選択肢を選んでいる", 2)],
              pit=["割合の大小だけで人数を比べる。", "割合の差（ポイント）を人数の差と取り違える。"])


AVG_SCN = [("数学の小テストの得点", "点"), ("ハンドボール投げの記録", "m"), ("1週間の読書時間", "分"), ("夏休みに読んだ本のページ数", "ページ")]


@robust
@gen("standard_practice", 4, ["computation", "cross_unit"], rel=["JH-MATH-G1-U07"])
def b_weighted(r):
    what, u = r.choice(AVG_SCN)
    lo, hi = {"点": (50, 85), "m": (14, 26), "分": (60, 150), "ページ": (300, 700)}[u]
    for _ in range(3000):
        ns = [r.randint(25, 35) for _ in range(3)]
        ms = [r.randint(lo, hi) for _ in range(3)]
        N, S = sum(ns), sum(a * b for a, b in zip(ns, ms))
        if S % N == 0 and len(set(ms)) == 3:
            break
    assert S % N == 0 and len(set(ms)) == 3
    M = S // N
    tbl_rows = [[f"{i + 1}組", f"{a}", f"{b}"] for i, (a, b) in enumerate(zip(ns, ms))]
    if r.random() < 0.5:
        tbl = table(tbl_rows, header=["組", "人数（人）", f"平均値（{u}）"], caption=f"資料1　3年生の組ごとの{what}の平均値" + FAKE)
        stem = f"資料1は，Kさんの学校の3年生の{what}を，組ごとにまとめたものである。資料1から，3年生全体（{N}人）の{what}の平均値を求めなさい。"
        e = f"合計は {ns[0]}×{ms[0]}＋{ns[1]}×{ms[1]}＋{ns[2]}×{ms[2]}＝{S}，全体の平均値は {S}÷{N}＝{M}（{u}）。"
        expr = f"({ns[0]}*{ms[0]}+{ns[1]}*{ms[1]}+{ns[2]}*{ms[2]})/{N}"
        v = M
        st = [f"組ごとの合計＝人数×平均値：{ns[0] * ms[0]}，{ns[1] * ms[1]}，{ns[2] * ms[2]}。", f"全体の合計：{S}。", f"全体の人数：{N}人。", f"平均値：{S}÷{N}＝{M}"]
    else:
        tbl_rows[2][2] = "？"
        tbl = table(tbl_rows + [["全体", f"{N}", f"{M}"]], header=["組", "人数（人）", f"平均値（{u}）"], caption=f"資料1　3年生の組ごとの{what}の平均値" + FAKE)
        stem = f"資料1は，Kさんの学校の3年生の{what}を，組ごとにまとめたものである。資料1で，3組の{what}の平均値は何{u}か求めなさい。"
        rest = S - ns[0] * ms[0] - ns[1] * ms[1]
        e = f"全体の合計は {M}×{N}＝{S}。3組の合計は {S}−{ns[0] * ms[0]}−{ns[1] * ms[1]}＝{rest}，平均値は {rest}÷{ns[2]}＝{ms[2]}（{u}）。"
        expr = f"({M}*{N}-{ns[0]}*{ms[0]}-{ns[1]}*{ms[1]})/{ns[2]}"
        v = ms[2]
        st = [f"全体の合計：{M}×{N}＝{S}。", f"1組と2組の合計：{ns[0] * ms[0]}＋{ns[1] * ms[1]}＝{ns[0] * ms[0] + ns[1] * ms[1]}。", f"3組の合計：{rest}。", f"3組の平均値：{rest}÷{ns[2]}＝{ms[2]}"]
    return MARK(stem, v, e, expr, d=3, k=DC, tbl=tbl,
                ap="平均値＝合計÷人数。人数がちがう組をまとめるときは，組ごとに合計（平均値×人数）に直してから考える。",
                steps=st, alt=[f"求めた値を使って全体の合計を計算し直し，{S}になることを確かめる。"],
                pc=[("平均値を合計に直している", 2), ("正しい値を求めている", 2)],
                pit=["3つの組の平均値をそのまま足して3でわる（人数のちがいを無視する）。"])


@robust
@gen("standard_practice", 4, ["condition_check", "application"])
def b_assign(r):
    what, roles = r.choice(ASSIGN_SCN)
    names = sorted(r.sample(NAMES5, 4), key=NAMES5.index)
    cands = all_assign(names, roles)
    secret = r.choice(cands)
    clues = build_unique(r, cands, secret, assign_clue(names, roles), lo=3, hi=5)
    body = "\n".join("・" + c[0] for c in clues)
    full = "，".join(f"{x}：{secret[x]}" for x in names)
    lead = f"{'，'.join(names)}の4人は，{what}（{'・'.join(roles)}）を1人1つずつ担当することになった。次の〔条件〕がすべて成り立つとき，"
    if r.random() < 0.5:
        X = r.choice(names)
        ans = secret[X]
        return MC(f"{lead}{X}の担当として{SEL4}\n〔条件〕\n{body}", ans,
                  [(x, f"条件をすべて満たす分担は「{full}」の1通りだけで，{X}の担当は{ans}である。", "条件の整理不足") for x in roles if x != ans],
                  f"条件をすべて満たす分担は「{full}」の1通りだけである。", d=3, k=TH,
                  ap="縦に人，横に担当の表をつくり，「〜ではない」には×，決まったところには○を書く。○が入ったら，同じ行と列のほかのますは×になる。",
                  steps=["条件を表に書きこむ。", "×が3つ並んだ行や列は，残りの1つが○に決まる。", "「どちらか」の条件は場合分けをして確かめる。", f"分担：{full}。"],
                  alt=["選んだ分担を条件の1つ1つに当てはめ，すべて成り立つこと，ほかの分担では成り立たないことを確かめる。"],
                  pc=[("条件を表に整理している", 2), ("正しい担当を選んでいる", 2)],
                  pit=["「XとYのどちらかがP」を「XもYもP」と読みちがえる。", "○を書いたあと，同じ列のほかのますに×を書き忘れる。"])
    P = r.choice(roles)
    ans = next(x for x in names if secret[x] == P)
    return MC(f"{lead}{P}を担当する人として{SEL4}\n〔条件〕\n{body}", ans,
              [(x, f"条件をすべて満たす分担は「{full}」の1通りだけで，{x}の担当は{secret[x]}である。", "条件の整理不足") for x in names if x != ans],
              f"条件をすべて満たす分担は「{full}」の1通りだけである。{P}は{ans}。", d=3, k=TH,
              ap="縦に人，横に担当の表をつくり，「〜ではない」には×，決まったところには○を書く。○が入ったら，同じ行と列のほかのますは×になる。",
              steps=["条件を表に書きこむ。", "×が3つ並んだ行や列は，残りの1つが○に決まる。", "「どちらか」の条件は場合分けをして確かめる。", f"分担：{full}。"],
              alt=["選んだ分担を条件の1つ1つに当てはめ，すべて成り立つこと，ほかの分担では成り立たないことを確かめる。"],
              pc=[("条件を表に整理している", 2), ("正しい人を選んでいる", 2)],
              pit=["「XとYのどちらかがP」を「XもYもP」と読みちがえる。", "○を書いたあと，同じ列のほかのますに×を書き忘れる。"])


@robust
@gen("standard_practice", 4, ["computation", "cross_unit"], rel=["JH-MATH-G2-U01"])
def b_number(r):
    N = r.choice(TWO)
    clues = build_unique(r, TWO, N, lambda rr: num_clue(rr), lo=2, hi=4, tries=120)
    body = "\n".join(f"ヒント{i + 1}　{c[0]}" for i, c in enumerate(clues))
    st = []
    cur = list(TWO)
    for i, c in enumerate(clues):
        cur = [x for x in cur if c[1](x)]
        st.append(f"ヒント{i + 1}までで残る数：{lst(cur) if len(cur) <= 12 else str(len(cur)) + '個'}")
    return MARK(f"Kさんは，2けたの整数を1つ思いうかべ，その数について次のヒントを出した。すべてのヒントに当てはまる2けたの整数を求めなさい。\n{body}",
                N, f"すべてのヒントに当てはまるのは{N}だけである。", f"{N}", d=3, k=TH,
                ap="候補が最も少なくなるヒント（各位の数の和，入れかえの差など）から使って候補を書き出し，残りのヒントで消していく。",
                steps=st + [f"答え：{N}"],
                alt=[f"{N}がすべてのヒントに当てはまることを1つずつ確かめる。入れかえの差は 9×(十の位−一の位) で計算できる。"],
                pc=[("候補を書き出している", 2), ("条件で正しくしぼりこんでいる", 2)],
                pit=["一の位が0の数（入れかえると1けたになる数）を候補に入れたり，見落としたりする。", "入れかえた数の差を，各位の数の差と取り違える。"])


TALK_SCN = [("清掃ボランティアの参加者数", "人"), ("読書週間に借りられた本の冊数", "冊"), ("あいさつ運動に参加した人数", "人"), ("リサイクル活動で集めた古紙の量", "kg")]


@robust
@gen("standard_practice", 4, ["application", "condition_check"])
def b_talk(r):
    what, u = r.choice(TALK_SCN)
    cls = ["1組", "2組", "3組", "4組"]
    a = [r.choice([20, 25, 40, 50]) for _ in range(4)]
    d = [5 * r.randint(1, 8) for _ in range(4)]
    b = [x + y for x, y in zip(a, d)]
    rate = [Fr(y, x) for x, y in zip(a, b)]
    im = max(range(4), key=lambda i: d[i])
    ib = max(range(4), key=lambda i: b[i])
    ir = max(range(4), key=lambda i: rate[i])
    assert d.count(d[im]) == 1 and b.count(b[ib]) == 1 and rate.count(rate[ir]) == 1
    tbl = table([[c, f"{x}", f"{y}"] for c, x, y in zip(cls, a, b)], header=["組", f"昨年（{u}）", f"今年（{u}）"], caption=f"資料1　3年生の組ごとの{what}" + FAKE)
    if r.random() < 0.5:
        assert len({im, ib, ir}) >= 2
        ok = f"{cls[im]}で，{d[im]}{u}"
        talk = f"Aさん「資料1を見ると，今年はどの組も昨年より増えていますね。」\nBさん「昨年と比べて増えた量がいちばん多いのは[[blank:　]]増えています。」"
        cands = [(f"{cls[ib]}で，{d[ib]}{u}", f"{cls[ib]}は今年の量が最も多い組で，増えた量が最も多いのは{cls[im]}（{d[im]}{u}）である。", "今年の量と増えた量の取り違え"),
                 (f"{cls[ir]}で，{d[ir]}{u}", f"{cls[ir]}は増えた割合が最も大きい組で，増えた量が最も多いのは{cls[im]}（{d[im]}{u}）である。", "増えた割合と増えた量の取り違え"),
                 (f"{cls[im]}で，{b[im]}{u}", f"{b[im]}{u}は{cls[im]}の今年の量で，増えた量は{b[im]}−{a[im]}＝{d[im]}{u}である。", "今年の量と増えた量の取り違え"),
                 (f"{cls[im]}で，{a[im]}{u}", f"{a[im]}{u}は{cls[im]}の昨年の量である。", "昨年の量と増えた量の取り違え")]
        e = "増えた量は " + "，".join(f"{c} {y}−{x}＝{z}" for c, x, y, z in zip(cls, a, b, d)) + f"。最も多いのは{cls[im]}の{d[im]}{u}。"
        key = "増えた量＝今年−昨年"
    else:
        ok = f"{cls[ir]}で，昨年の{dec(rate[ir])}倍に"
        talk = f"Aさん「資料1を見ると，今年はどの組も昨年より増えていますね。」\nBさん「昨年と比べた増え方の割合がいちばん大きいのは[[blank:　]]なっています。」"
        cands = [(f"{cls[im]}で，昨年の{dec(rate[im])}倍に", f"{cls[im]}は増えた量が最も多い組で，割合が最も大きいのは{cls[ir]}（{dec(rate[ir])}倍）である。", "増えた量と増えた割合の取り違え"),
                 (f"{cls[ib]}で，昨年の{dec(rate[ib])}倍に", f"{cls[ib]}は今年の量が最も多い組で，割合が最も大きいのは{cls[ir]}（{dec(rate[ir])}倍）である。", "今年の量と増えた割合の取り違え"),
                 (f"{cls[ir]}で，昨年の{dec(Fr(b[ir], a[ir]) + 1)}倍に", f"{cls[ir]}の今年の量は昨年の {b[ir]}÷{a[ir]}＝{dec(rate[ir])}倍である。", "倍の計算の誤り"),
                 (f"{cls[ir]}で，昨年の{dec(Fr(d[ir], a[ir]))}倍に", f"{dec(Fr(d[ir], a[ir]))}は増えた量が昨年の何倍かを表す値で，今年の量は昨年の{dec(rate[ir])}倍である。", "増えた量の割合と今年の量の割合の取り違え")]
        e = "今年÷昨年 は " + "，".join(f"{c} {y}÷{x}＝{dec(q)}" for c, x, y, q in zip(cls, a, b, rate)) + f"。最も大きいのは{cls[ir]}の{dec(rate[ir])}倍。"
        key = "今年が昨年の何倍か＝今年÷昨年"
    return MC(f"〔会話〕と資料1について，〔会話〕の中の[[blank:　]]にあてはまるものとして{SEL4}\n〔会話〕\n{talk}", ok, cands, e,
              d=3, k=DT, tbl=tbl,
              ap=f"空欄の前の言葉から，何を比べるのか（{key}）を先に確かめる。",
              steps=[f"空欄で求めるもの：{key}。", "4つの組それぞれについて計算する。", e],
              alt=["表に「増えた量」「今年÷昨年」の列を書き加えてから選択肢を確かめると，取り違えを防げる。"],
              pc=[("何を比べるかをとらえている", 2), ("正しく計算して選んでいる", 2)],
              pit=["増えた量・増えた割合・今年の量を取り違える。"])


# ---------------------------- C 思考力・記述 ----------------------------

@robust
@gen("thinking_writing", 3, ["condition_check", "application"])
def c_pairs(r):
    topic = r.choice(TOPIC2)
    n, p, c = grade_data(r)
    st, t2 = grade_stim(topic, n, p)
    pool = grade_statements(r, topic, n, p, c)
    tr = [x for x in pool if x[1]]
    fa = [x for x in pool if not x[1]]
    assert len(tr) >= 2 and len(fa) >= 4
    stmts = r.sample(tr, 2) + r.sample(fa, 4)
    r.shuffle(stmts)
    lab = "abcdef"
    m = dict(zip(lab, stmts))
    right = [k for k in lab if m[k][1]]
    ok = f"{right[0]}と{right[1]}"
    pairs = [f"{a}と{b}" for a, b in itertools.combinations(lab, 2)]
    pick = sorted(r.sample([x for x in pairs if x != ok], 7) + [ok], key=pairs.index)
    why = {}
    for ch in pick:
        if ch != ok:
            a, b = ch.split("と")
            why[ch] = ("　".join(f"{k}は誤り。{m[k][2]}" for k in (a, b) if not m[k][1]), "資料の統合の誤り")
    body = "\n".join(f"{k}．{m[k][0]}" for k in lab)
    return mc(f"資料1と資料2から読み取れることを，次のa〜fの中から2つ選んだときの組み合わせとして最も適するものを，あとの1〜8の中から1つ選び，その番号を答えなさい。\n{body}",
              pick, f"正しいのは{ok}。" + "　".join(f"{k}：{m[k][2]}" for k in lab), ai=pick.index(ok), keep=True, why=why, d=4, k=DT, p=6,
              stim=st, tbl=t2,
              ap="a〜fの1つ1つに○×をつけてから組み合わせを選ぶ。人数についての文は，生徒数×割合で人数を求めてから判断する。",
              steps=[f"学年ごとの人数：{GRADES[0]}{c[0]}人，{GRADES[1]}{c[1]}人，{GRADES[2]}{c[2]}人（合計{sum(c)}人）。",
                     "a〜fのそれぞれについて正誤を判断する。", f"○の2つを組み合わせる：{ok}。"],
              alt=["×をつけた文には，正しい数値を書きこんでおく。○が2つちょうどになることも確かめる。"],
              pc=[("1つ目の正しい文を選んでいる", 3), ("2つ目の正しい文を選んでいる", 3)],
              pit=["割合の大小で人数を比べる。", "全校の割合を，各学年の割合の平均で求める。"])


LIAR_SCN = [("学級の黒板に，誕生日のお祝いのメッセージをかいた", "メッセージをかいた"), ("教室の花びんの花を新しいものにかえた", "花をかえた"),
            ("学級文庫の本をきれいに並べ直した", "本を並べ直した"), ("落とし物の筆箱を職員室に届けた", "筆箱を届けた")]


def liar_stmt(r, S, names):
    others = [x for x in names if x != S]
    t = r.random()
    X, Y = sorted(r.sample(others, 2), key=names.index)
    if t < 0.25:
        return ("私ではありません。", lambda c, S=S: c != S)
    if t < 0.45:
        return (f"{X}です。", lambda c, X=X: c == X)
    if t < 0.7:
        return (f"{X}ではありません。", lambda c, X=X: c != X)
    if t < 0.85:
        return (f"{X}か{Y}のどちらかです。", lambda c, X=X, Y=Y: c in (X, Y))
    return (f"私か{X}のどちらかです。", lambda c, S=S, X=X: c in (S, X))


@robust
@gen("thinking_writing", 2, ["condition_check", "written_reasoning"])
def c_liar(r):
    act, short = r.choice(LIAR_SCN)
    names = ["Aさん", "Bさん", "Cさん", "Dさん"]
    st = [liar_stmt(r, S, names) for S in names]
    assert len({s[0] for s in st}) == 4
    sols = []
    for c in names:
        falses = [names[i] for i, s in enumerate(st) if not s[1](c)]
        if len(falses) == 1:
            sols.append((c, falses[0]))
    assert len(sols) == 1
    c0, L = sols[0]
    nf = {c: sum(1 for s in st if not s[1](c)) for c in names}
    body = "\n".join(f"{S}「{s[0]}」" for S, s in zip(names, st))
    lead = (f"Aさん，Bさん，Cさん，Dさんの4人のうち1人が，{act}。だれが{short}のかをたずねたところ，4人は次のように答えた。"
            f"4人のうち1人だけがまちがったことを言っていて，ほかの3人は正しいことを言っているとき，")
    common = dict(d=4, k=TH, p=6,
                  ap="「〇〇さんが" + short + "とすると」と1人ずつ仮定し，4人の発言のうちまちがっているものがいくつになるかを数える。ちょうど1つになる場合が答え。",
                  steps=[f"{c}が{short}とすると，まちがった発言は{nf[c]}つ。" for c in names] + [f"ちょうど1つになるのは{c0}の場合だけ。まちがっているのは{L}。"],
                  alt=[f"{c0}が{short}として，4人の発言を1つずつ確かめ，{L}の発言だけがまちがっていることを確認する。"],
                  pc=[("1人ずつ仮定して発言の正誤を調べている", 3), ("正しい人を選んでいる", 3)],
                  pit=["「私ではありません」のような発言を，発言した人以外についての情報だと思わない。", "まちがった発言が1つになる場合を1つ見つけて，ほかの場合を調べない。"])
    if r.random() < 0.5:
        return MC(f"{lead}{short}人として{SEL4}\n{body}", c0,
                  [(x, f"{x}が{short}とすると，まちがった発言が{nf[x]}つになり，「1人だけがまちがっている」に合わない。", "仮定と検証の不足") for x in names if x != c0],
                  f"{c0}が{short}とすると，まちがった発言は{L}の1つだけになる。ほかの人の場合はまちがった発言が1つにならない。", **common)
    return MC(f"{lead}まちがったことを言っている人として{SEL4}\n{body}", L,
              [(x, f"{x}だけがまちがっているとすると，ほかの3人の発言がすべて正しくなる{short}人がいない。", "仮定と検証の不足") for x in names if x != L],
              f"{c0}が{short}とすると，まちがった発言は{L}の1つだけになる。したがって，まちがっているのは{L}。", **common)


ROUTE_SCN = [("図書館", "9時"), ("市民体育館", "10時"), ("駅前の科学館", "13時"), ("祖父母の家", "8時")]


@robust
@gen("thinking_writing", 3, ["application", "cross_unit"], rel=["JH-MATH-G2-U03"])
def c_route(r):
    place, hh = r.choice(ROUTE_SCN)
    vw, vb, vs = 80, r.choice([200, 240]), r.choice([300, 400])
    tw = r.randint(18, 40)
    dw = vw * tw
    tb = r.randint(7, 15)
    db = vb * tb
    walk2 = r.randint(3, 8)
    wait = r.randint(2, 6)
    tbus = r.randint(4, 10)
    total_bus = walk2 + wait + tbus
    times = {"徒歩": tw, "自転車": tb, "バス": total_bus}
    assert len(set(times.values())) == 3 and tw > tb
    t1 = table([["徒歩", f"{dw}m", f"分速{vw}m"], ["自転車", f"{db}m", f"分速{vb}m"],
                ["バス", f"家からバス停まで{walk2 * vw}m（徒歩），バス停から{place}まで{tbus * vs}m", f"徒歩は分速{vw}m，バスは分速{vs}m"]],
               header=["行き方", "道のり", "速さ"], caption=f"資料1　Kさんの家から{place}までの行き方" + FAKE)
    st_ = stim("TOKU-ROUTE", f"資料2　バス停でバスを待つ時間は{wait}分である。" + FAKE, "data", "資料1・資料2", source="オリジナル（架空の資料）")
    fastest = min(times, key=times.get)
    stmts = []
    for mode, t in times.items():
        f = t + r.choice([-3, -2, 2, 3])
        stmts.append((f"{mode}で行くと，家を出てから{place}に着くまでに{t}分かかる。", True, f"{mode}は{t}分かかる。"))
        stmts.append((f"{mode}で行くと，家を出てから{place}に着くまでに{f}分かかる。", False, f"{mode}は{t}分かかる。"))
    for mode in times:
        stmts.append((f"3つの行き方のうち，最も早く着くのは{mode}である。", mode == fastest, f"かかる時間は徒歩{tw}分，自転車{tb}分，バス{total_bus}分で，最も早いのは{fastest}である。"))
    dd = tw - tb
    stmts.append((f"自転車で行くと，徒歩で行くより{dd}分早く着く。", True, f"{tw}−{tb}＝{dd}（分）である。"))
    stmts.append((f"自転車で行くと，徒歩で行くより{dd + r.choice([2, 4])}分早く着く。", False, f"{tw}−{tb}＝{dd}（分）である。"))
    lim = r.randint(20, 35)
    for mode, t in times.items():
        if t != lim:
            stmts.append((f"{hh}ちょうどに家を出て{mode}で行くと，{hh}{lim}分より前に{place}に着く。", t < lim, f"{mode}では{hh}{t}分に着く。"))
    tr = [s for s in stmts if s[1]]
    fa = [s for s in stmts if not s[1]]
    nt = r.randint(1, 3)
    assert len(tr) >= nt and len(fa) >= 4 - nt
    four = r.sample(tr, nt) + r.sample(fa, 4 - nt)
    r.shuffle(four)
    L = "ABCD"
    m = dict(zip(L, four))
    right = tuple(k for k in L if m[k][1])
    subs = [s for k in (1, 2, 3) for s in itertools.combinations(L, k)]
    others = r.sample([s for s in subs if s != right], 5)
    choices_t = sorted(others + [right], key=lambda s: (len(s), s))
    fmt = lambda s: "，".join(s)
    choices = [fmt(s) for s in choices_t]
    why = {}
    for s in choices_t:
        if s == right:
            continue
        bad = [f"{k}は{'正しい' if m[k][1] else '誤り'}（{m[k][2]}）" for k in L if (k in s) != m[k][1]]
        why[fmt(s)] = ("　".join(bad), "資料の統合の誤り")
    body = "\n".join(f"{k}．{m[k][0]}" for k in L)
    return mc(f"資料1と資料2をもとに，Kさんの家から{place}まで行くときについて述べた次のA〜Dの中から，正しいものをすべて選んだときの組み合わせとして最も適するものを，あとの1〜6の中から1つ選び，その番号を答えなさい。\n{body}",
              choices, f"かかる時間は，徒歩 {dw}÷{vw}＝{tw}分，自転車 {db}÷{vb}＝{tb}分，バス {walk2}＋{wait}＋{tbus}＝{total_bus}分（バス停まで{walk2}分，待ち{wait}分，乗車{tbus}分）。正しいのは{fmt(right)}。",
              ai=choices.index(fmt(right)), keep=True, why=why, d=4, k=DC, p=6, stim=st_, tbl=t1,
              ap="時間＝道のり÷速さ。バスは「バス停まで歩く時間＋待つ時間＋乗っている時間」の合計で考える。資料2の待ち時間を忘れない。",
              steps=[f"徒歩：{dw}÷{vw}＝{tw}（分）", f"自転車：{db}÷{vb}＝{tb}（分）",
                     f"バス：{walk2 * vw}÷{vw}＝{walk2}（分），待ち{wait}分，{tbus * vs}÷{vs}＝{tbus}（分），合計{total_bus}分", f"A〜Dの正誤を判断する：正しいのは{fmt(right)}。"],
              alt=["横軸を時間，縦軸を道のりにしたグラフをかき，3つの行き方を比べて確かめる。"],
              pc=[("3つの行き方の時間を正しく求めている", 3), ("正しい組み合わせを選んでいる", 3)],
              pit=["資料2のバスの待ち時間を足し忘れる。", "時間＝速さ÷道のり と逆に計算する。"])


@robust
@gen("thinking_writing", 2, ["written_reasoning", "common_error"])
def c_write(r):
    topic = r.choice(TOPIC2)
    n, p, c = grade_data(r, need_mismatch=True)
    st, t2 = grade_stim(topic, n, p)
    G = GRADES
    pm = max(range(3), key=lambda i: p[i])
    cm = max(range(3), key=lambda i: c[i])
    model = f"{G[pm]}は割合が{p[pm]}％で最も高いが，人数は{n[pm]}×{p[pm]}％＝{c[pm]}人で，{G[cm]}の{c[cm]}人より少ないから。"
    lo, hi = 40, 60
    assert lo <= len(model) <= hi, len(model)
    rub = [(f"{G[pm]}の人数を資料1の生徒数と資料2の割合から求めている", 3), (f"人数がより多い学年（{G[cm]}）と比べている", 3), ("字数の条件（40字以上60字以内）を守っている", 2)]
    return desc(f"資料1と資料2を見て，Kさんは「{G[pm]}は割合が最も高いので，「{topic}」と答えた人数も最も多い。」と考えた。Kさんの考えが正しくない理由を，"
                f"資料1と資料2の数値を用いて，40字以上60字以内で書きなさい。ただし，句読点や記号も1字に数える。",
                model, f"人数＝生徒数×割合 で求めると，{G[0]}{c[0]}人，{G[1]}{c[1]}人，{G[2]}{c[2]}人となり，最も多いのは{G[cm]}である。割合が最も高い学年が，人数も最も多いとはかぎらない。",
                rub, d=4, p=8, k=["data_interpretation", "writing"], grid=60, stim=st, tbl=t2,
                ap="割合だけでは人数が決まらないことに注目し，生徒数×割合で各学年の人数を計算して，具体的な数値で反例を示す。",
                steps=[f"各学年の人数：{G[0]} {n[0]}×{p[0]}％＝{c[0]}人，{G[1]} {n[1]}×{p[1]}％＝{c[1]}人，{G[2]} {n[2]}×{p[2]}％＝{c[2]}人。",
                       f"割合が最も高いのは{G[pm]}，人数が最も多いのは{G[cm]}で，一致しない。", "「割合は最も高いが，人数は〜より少ない」という形で，数値を入れて書く。",
                       f"字数を数える（模範解答は{len(model)}字）。"],
                alt=[f"「{G[cm]}は割合が{p[cm]}％と低いが，生徒数が{n[cm]}人と多いので，人数は{c[cm]}人で最も多いから。」のように，人数が最も多い学年の側から書いてもよい。"],
                pc=rub,
                pit=["「割合と人数はちがうから」とだけ書き，数値を使っていない。", "資料1か資料2の一方の数値しか使っていない。"])


# ---------------------------- D 典型誤答訂正 ----------------------------

@robust
@gen("error_correction", 3, ["common_error", "computation"])
def d_avg(r):
    t = r.randrange(3)
    if t == 0:
        what, u = r.choice(AVG_SCN[:3])
        lo, hi = {"点": (50, 85), "m": (14, 26), "分": (60, 150)}[u]
        for _ in range(3000):
            n1, n2 = r.sample(range(15, 41), 2)
            m1, m2 = r.sample(range(lo, hi + 1), 2)
            S, N = n1 * m1 + n2 * m2, n1 + n2
            if S % N == 0 and (m1 + m2) % 2 == 0 and S // N != (m1 + m2) // 2:
                break
        assert S % N == 0 and (m1 + m2) % 2 == 0 and S // N != (m1 + m2) // 2
        M = S // N
        tbl = table([["1組", f"{n1}", f"{m1}"], ["2組", f"{n2}", f"{m2}"]], header=["組", "人数（人）", f"平均値（{u}）"], caption=f"資料1　{what}の組ごとの平均値" + FAKE)
        kt = f"（{m1}＋{m2}）÷2＝{(m1 + m2) // 2}　答え　{(m1 + m2) // 2}{u}"
        q = f"1組と2組を合わせた{N}人の{what}の平均値を求める"
        ok = "2つの組の人数がちがうのに，平均値をそのまま足して2でわっている。"
        wrongs = [("平均値ではなく，中央値を求めなければならないのに平均値を求めている。", "問われているのは平均値であり，平均値を求めること自体は正しい。", "代表値の取り違え"),
                  ("足し算は正しいが，2ではなく3でわらなければならない。", "わる数の問題ではない。人数を考えて合計を求める必要がある。", "計算の手順の誤解"),
                  ("計算は正しく，Kさんの答えに誤りはない。", f"正しい平均値は（{n1}×{m1}＋{n2}×{m2}）÷{N}＝{M}{u}で，Kさんの答えとちがう。", "誤りの見落とし")]
        fix = f"（{n1}×{m1}＋{n2}×{m2}）÷{N}＝{S}÷{N}＝{M}（{u}）"
        typ = "concept"
    elif t == 1:
        what, u = r.choice([("図書室の貸出冊数", "冊"), ("清掃ボランティアの参加者数", "人"), ("古紙の回収量", "kg")])
        a = r.choice([40, 50, 80, 100, 200, 250])
        pct = r.choice([10, 20, 25, 30, 40, 50, 60])
        b = a * (100 + pct) // 100
        assert a * (100 + pct) % 100 == 0
        wrong = Fr(b - a, b) * 100
        assert wrong != pct
        tbl = table([["昨年", f"{a}"], ["今年", f"{b}"]], header=["年", f"{what}（{u}）"], caption=f"資料1　{what}" + FAKE)
        kt = f"（{b}−{a}）÷{b}×100＝{dec(wrong) if wrong.denominator in (1, 2, 4, 5, 8, 10, 20, 25, 40, 50) else str(round(float(wrong), 1)) + '…'}　答え　約{round(float(wrong))}％増えた"
        q = f"今年の{what}は昨年より何％増えたかを求める"
        ok = "もとにする量（昨年の値）ではなく，今年の値でわっている。"
        wrongs = [("増えた量ではなく，今年の値を100倍しなければならない。", f"増えた割合は（増えた量）÷（もとにする量）で求める。今年の値を100倍しても割合にはならない。", "割合の式の誤解"),
                  ("ひき算の順序が逆で，昨年の値から今年の値をひかなければならない。", "今年のほうが多いので，今年−昨年で増えた量を求めるのは正しい。", "差の向きの誤解"),
                  ("計算は正しく，Kさんの答えに誤りはない。", f"正しくは（{b}−{a}）÷{a}×100＝{pct}（％）で，Kさんの答えとちがう。", "誤りの見落とし")]
        fix = f"（{b}−{a}）÷{a}×100＝{pct}　答え　{pct}％増えた"
        typ = "formula"
    else:
        topic = r.choice(TOPIC2)
        for _ in range(3000):
            n1, n2 = r.sample(range(100, 241, 20), 2)
            p1, p2 = r.sample(range(20, 81, 5), 2)
            c1, c2 = n1 * p1 // 100, n2 * p2 // 100
            whole = Fr(c1 + c2, n1 + n2) * 100
            if whole != Fr(p1 + p2, 2) and (p1 + p2) % 2 == 0 and whole.denominator == 1:
                break
        assert whole != Fr(p1 + p2, 2) and (p1 + p2) % 2 == 0 and whole.denominator == 1
        tbl = table([["1年生", f"{n1}", f"{p1}"], ["2年生", f"{n2}", f"{p2}"]], header=["学年", "生徒数（人）", f"「{topic}」と答えた人の割合（％）"], caption="資料1　アンケートの結果" + FAKE)
        kt = f"（{p1}＋{p2}）÷2＝{(p1 + p2) // 2}　答え　{(p1 + p2) // 2}％"
        q = f"1年生と2年生を合わせた{n1 + n2}人のうち「{topic}」と答えた人の割合を求める"
        ok = "2つの学年の生徒数がちがうのに，割合をそのまま足して2でわっている。"
        wrongs = [("割合を足すのではなく，ひかなければならない。", "全体の割合を求めるのに，割合の差を求めても意味がない。", "計算の手順の誤解"),
                  ("2でわるのではなく，生徒数の合計でわらなければならない。", f"割合（％）を生徒数でわっても割合にはならない。人数に直して合計してから，全体の生徒数でわる。", "割合と人数の混同"),
                  ("計算は正しく，Kさんの答えに誤りはない。", f"正しくは（{c1}＋{c2}）÷{n1 + n2}×100＝{whole}（％）で，Kさんの答えとちがう。", "誤りの見落とし")]
        fix = f"人数は {n1}×{p1}％＝{c1}人，{n2}×{p2}％＝{c2}人。（{c1}＋{c2}）÷{n1 + n2}×100＝{whole}　答え　{whole}％"
        typ = "concept"
    return MC(f"資料1について，{q}問題で，Kさんは次のように解答した。Kさんの解答の誤りを説明したものとして{SEL4}\n［Kさんの解答］{kt}", ok, wrongs,
              f"{ok}正しい解答：{fix}", d=3, k=DC, tbl=tbl,
              ap="Kさんの式が，資料のどの数値を使っているか，使っていない数値はないかを確かめる。人数や，もとにする量を使っているかに注目する。",
              steps=["Kさんの式で使われている数値を確かめる。", "求めるものの定義（平均＝合計÷人数，増えた割合＝増えた量÷もとにする量）と比べる。", f"正しい解答：{fix}"],
              alt=["極端な例（片方の組が1人だけ，など）を考えると，Kさんの方法がおかしいことが確かめられる。"],
              pc=[("Kさんの式の問題点に気づいている", 3), ("誤りを正しく説明したものを選んでいる", 3)],
              pit=["人数がちがう集団の平均や割合を，そのまま平均してしまう。", "増えた割合を，今年の値をもとにして求めてしまう。"],
              err=dict(sol=kt, step="式を立てるところ", type=typ, tempt="平均や割合の数値だけを見て，人数やもとにする量を考えなかった。", fix=fix))


@robust
@gen("error_correction", 4, ["common_error", "written_reasoning"])
def d_line(r):
    N = r.choice(TWO)
    a, b = digits(N)
    s = a + b
    assert 4 <= s <= 15
    c1 = (f"十の位の数と一の位の数の和は{s}である。", lambda n, s=s: sum(digits(n)) == s)
    L1 = solve(TWO, [c1])
    assert 3 <= len(L1) <= 9
    pool = []
    if a != b:
        pool.append(("cmp", ("十の位の数は，一の位の数より大きい。", lambda n: digits(n)[0] > digits(n)[1]) if a > b else
                     ("十の位の数は，一の位の数より小さい。", lambda n: digits(n)[0] < digits(n)[1])))
    pool.append(("par", ("奇数である。", lambda n: n % 2 == 1) if N % 2 else ("偶数である。", lambda n: n % 2 == 0)))
    for k in (3, 4, 6, 7):
        if N % k == 0:
            pool.append(("mul", (f"{k}の倍数である。", lambda n, k=k: n % k == 0)))
    for k in (4, 5, 7):
        if N % k:
            pool.append(("rem", (f"{k}でわると{N % k}あまる。", lambda n, k=k, m=N % k: n % k == m)))
    assert len(pool) >= 2
    (k2, c2), (k3, c3) = r.sample(pool, 2)
    L2 = [x for x in L1 if c2[1](x)]
    L3 = [x for x in L2 if c3[1](x)]
    assert L3 == [N] and len(L2) > 1 and len(L2) < len(L1)
    j = r.choice([1, 2, 3])
    if j == 1:
        W1 = [x for x in L1 if digits(x)[0] >= digits(x)[1]] if r.random() < 0.5 else [x for x in L1 if digits(x)[1] != 0 and digits(x)[0] <= digits(x)[1]]
        assert W1 != L1 and N not in W1
        W2 = [x for x in W1 if c2[1](x)]
        W3 = [x for x in W2 if c3[1](x)]
        why_j = f"①：和が{s}になる2けたの整数は{lst(L1)}で，Kさんはこのうち{lst([x for x in L1 if x not in W1])}を書き落としている。"
    elif j == 2:
        W1 = L1
        W2 = [x for x in L1 if not c2[1](x)]
        W3 = [x for x in W2 if c3[1](x)]
        why_j = f"②：ヒント2「{c2[0]}」に当てはまる数は{lst(L2)}であるが，Kさんは当てはまらない数を残している（条件を逆に読んでいる）。"
    else:
        W1, W2 = L1, L2
        W3 = [x for x in L2 if not c3[1](x)]
        why_j = f"③：ヒント3「{c3[0]}」に当てはまる数は{lst(L3)}であるが，Kさんは当てはまらない数を残している（条件を逆に読んでいる）。"
    assert W3 != [N]
    concl = f"したがって，答えは{W3[0]}である。" if len(W3) == 1 else ("したがって，ヒントに当てはまる2けたの整数はない。" if not W3 else "したがって，答えは1つに決まらない。")
    lines = [f"①　ヒント1より，考えられる数は {lst(W1)}", f"②　ヒント2より，{lst(W2)}", f"③　ヒント3より，{lst(W3)}", f"④　{concl}"]
    marks = ["①", "②", "③", "④"]
    ok = marks[j - 1]
    good = {1: f"①は正しい。和が{s}になる2けたの整数は{lst(L1)}ですべてである。",
            2: "②は，①の数からヒント2に当てはまるものを正しく選んでいる。",
            3: "③は，②の数からヒント3に当てはまるものを正しく選んでいる。",
            4: "④は③の結果から導かれた結論で，誤りはそれより前の行で生じている。"}
    wrongs = [(mk, good[i + 1], "誤りの位置の取り違え") for i, mk in enumerate(marks) if i != j - 1]
    hints = f"ヒント1　{c1[0]}\nヒント2　{c2[0]}\nヒント3　{c3[0]}"
    kans = "\n".join(lines)
    return MC(f"2けたの整数について，次のヒント1〜3がある。\n{hints}\nKさんはこの整数を次のように求めた。Kさんの考えの中で，誤りが最初にある行として{SEL4}\n［Kさんの考え］\n{kans}",
              ok, wrongs, f"{why_j}正しくは，①{lst(L1)}，②{lst(L2)}，③{lst(L3)}で，答えは{N}。", d=3, k=TH,
              ap="①から順に，その行が前の行とヒントから正しく導かれているかを確かめる。①は，和の条件に合う数をすべて自分で書き出して比べる。",
              steps=[f"ヒント1に合う数をすべて書き出す：{lst(L1)}。", f"ヒント2でしぼる：{lst(L2)}。", f"ヒント3でしぼる：{lst(L3)}。",
                     f"Kさんの考えと比べ，最初にくい違うのは{ok}の行。"],
              alt=[f"正しい答え{N}が，Kさんのどの行で消えてしまったかを調べると，誤りの行が分かる。"],
              pc=[("各行を前の行とヒントから確かめている", 3), ("誤りが最初にある行を選んでいる", 3)],
              pit=["結論（④）がおかしいので④がまちがいだと考え，それより前の行を確かめない。", "一の位が0の数や，十の位が一の位より小さい数を書き落とす。"],
              err=dict(sol=kans.replace("\n", "　"), step=f"{ok}の行", type="condition" if j > 1 else "logic",
                       tempt="候補を書き出すときや条件を当てはめるときに，見直しをしなかった。", fix=f"①{lst(L1)}　②{lst(L2)}　③{lst(L3)}　答え {N}"))


CLAIM_T = {"COUNT": "調べた人数がちがうのに，割合の大小だけで人数の大小を決めている。",
           "AXIS": "縦軸の目盛りが0から始まっていないことに気づかず，棒の高さの比を数量の比としている。",
           "CAUSE": "2つのことがらに関係が見られることだけから，一方が他方の原因であると決めつけている。",
           "GEN": "一部の人を調べた結果だけから，それよりはるかに大きな集団全体について決めつけている。"}


@robust
@gen("error_correction", 3, ["common_error", "concept"])
def d_claim(r):
    typ = r.choice(list(CLAIM_T))
    kw = {}
    if typ == "COUNT":
        n1, n2 = r.sample(range(100, 241, 20), 2)
        p1, p2 = r.sample(range(20, 81, 5), 2)
        c1, c2 = n1 * p1 // 100, n2 * p2 // 100
        assert p1 > p2 and c1 < c2
        kw["tbl"] = table([["A中学校", f"{n1}", f"{p1}"], ["B中学校", f"{n2}", f"{p2}"]], header=["学校", "調べた人数（人）", "「読書が好き」と答えた人の割合（％）"],
                          caption="資料1　2つの中学校の調査結果" + FAKE)
        lead = "資料1は，2つの中学校で行った調査の結果である。"
        claim = "A中学校のほうが割合が高いので，「読書が好き」と答えた人数もA中学校のほうが多い。"
        fact = f"人数は，A中学校が{n1}×{p1}％＝{c1}人，B中学校が{n2}×{p2}％＝{c2}人で，B中学校のほうが多い。"
        fix = f"人数を比べると，A中学校{c1}人，B中学校{c2}人で，B中学校のほうが多い。"
    elif typ == "AXIS":
        y0 = r.choice([40, 50, 60, 80])
        v1 = y0 + r.randint(2, 5)
        k = r.randint(2, 4)
        v2 = y0 + (v1 - y0) * k
        assert v2 != v1 * k
        kw["fig"] = figure("グラフ1　縦軸が途中から始まる縦棒グラフ", bar_svg(["昨年", "今年"], [v1, v2], "百人", ymin=y0, step=(v2 - y0 + 4) // 5 or 1),
                           caption="グラフ1　ある美術館の夏休みの来館者数" + FAKE)
        lead = "グラフ1は，ある美術館の夏休みの来館者数を表したものである。"
        claim = f"今年の棒の高さは昨年の棒の高さの{k}倍なので，来館者数は昨年の{k}倍になった。"
        fact = f"縦軸は{y0}から始まっている。来館者数は昨年{v1 * 100}人，今年{v2 * 100}人で，{dec(Fr(v2, v1))}倍にすぎない。" if Fr(v2, v1).denominator in (1, 2, 4, 5, 8, 10, 20, 25, 40, 50) else \
            f"縦軸は{y0}から始まっている。来館者数は昨年{v1 * 100}人，今年{v2 * 100}人で，{k}倍よりずっと小さい。"
        fix = f"来館者数の比は {v2 * 100}÷{v1 * 100} で求める。昨年の{k}倍にはなっていない。"
    elif typ == "CAUSE":
        pairs = [("1日の睡眠時間が長い生徒", "朝食を毎日食べる割合が高い", "睡眠時間を長くすれば，だれでも朝食を食べるようになる",
                  "朝食を毎日食べる生徒の割合（％）", ("睡眠時間が長いグループ", "睡眠時間が短いグループ")),
                 ("1週間の運動時間が長い生徒", "体力テストの得点が高い", "運動時間を長くすれば，だれでも必ず体力テストの得点が上がる",
                  "体力テストの平均得点（点）", ("運動時間が長いグループ", "運動時間が短いグループ")),
                 ("家で本を読む時間が長い生徒", "国語のテストの平均点が高い", "本を読む時間を長くすれば，だれでも必ず国語の点数が上がる",
                  "国語のテストの平均点（点）", ("読書時間が長いグループ", "読書時間が短いグループ")),
                 ("地域の行事によく参加する生徒", "地域の人とよくあいさつを交わす割合が高い", "行事に参加させれば，だれでも地域の人とあいさつを交わすようになる",
                  "地域の人とよくあいさつを交わす生徒の割合（％）", ("よく参加するグループ", "あまり参加しないグループ"))]
        x, y, z, col, gl = r.choice(pairs)
        pct = r.randint(55, 85)
        kw["tbl"] = table([[gl[0], f"{pct}"], [gl[1], f"{pct - r.randint(15, 30)}"]], header=["グループ", col], caption="資料1　ある中学校の調査結果" + FAKE)
        lead = f"資料1は，ある中学校で，{x}ほど{y}という傾向を調べた結果である。"
        claim = f"資料1から，{z}と言える。"
        fact = "資料1は2つのことがらに関係があることを示しているだけで，どちらが原因かや，ほかの理由（生活習慣など）が関係しているかは分からない。"
        fix = f"資料1から言えるのは，{x}ほど{y}という傾向があることまでである。"
    else:
        n = r.choice([20, 25, 30, 35, 40])
        pct = r.choice([60, 70, 80])
        thing = r.choice(["毎日家で30分以上勉強している", "自分専用の辞書を持っている", "休日に図書館を利用している", "毎朝自分で起きている"])
        kw["tbl"] = table([["はい", f"{n * pct // 100}"], ["いいえ", f"{n - n * pct // 100}"]], header=["回答", "人数（人）"],
                          caption=f"資料1　Kさんの学級の{n}人への質問「{thing}か」の結果" + FAKE)
        assert n * pct % 100 == 0
        lead = f"資料1は，Kさんが自分の学級の{n}人にたずねた結果である。"
        claim = f"「はい」が{pct}％なので，日本の中学生の{pct}％が{thing}と言える。"
        fact = f"調べたのは1つの学級の{n}人だけであり，日本の中学生全体を代表しているとは言えない。"
        fix = f"資料1から言えるのは，Kさんの学級では{n}人中{n * pct // 100}人（{pct}％）が{thing}ということまでである。"
    ok = CLAIM_T[typ]
    wrongs = [(CLAIM_T[t], f"Kさんの誤りはこの点ではない。{fact}", "誤りの種類の取り違え") for t in CLAIM_T if t != typ]
    return MC(f"{lead}Kさんは，この資料から次のように考えた。Kさんの考えの誤りを説明したものとして{SEL4}\n［Kさんの考え］{claim}", ok, wrongs,
              f"{ok}{fact}", d=3, k=DT,
              ap="Kさんの考えが，資料のどの数値をもとにしているか，資料が示している範囲（だれを調べたか，何と何の関係か，目盛りはどこから始まるか）をこえていないかを確かめる。",
              steps=["資料の題・単位・調べた対象・目盛りを確かめる。", "Kさんの考えを，資料の数値で確かめ直す。", fact, f"誤りの種類：{ok}"],
              alt=["Kさんの考えを，資料から言える範囲の正しい文に直してみる：" + fix],
              pc=[("資料の示す範囲を確かめている", 3), ("誤りの種類を正しく選んでいる", 3)],
              pit=["もっともらしい結論だと，資料の範囲をこえていることに気づかない。"],
              err=dict(sol=claim, step="資料から結論を導くところ", type="interpretation",
                       tempt="資料の数値や見た目の印象だけで結論を急ぎ，資料が示している範囲を確かめなかった。", fix=fix), **kw)


GENERATORS = [a_share, a_bar, a_order, a_fact, a_plan,
              b_two, b_weighted, b_assign, b_number, b_talk,
              c_pairs, c_liar, c_route, c_write,
              d_avg, d_line, d_claim]
