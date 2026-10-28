"""単元パック：中学2年 連立方程式（神奈川県公立高校入試形式）。"""
import re
import unicodedata
from fractions import Fraction as Fr

from banks._common import mc, num
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem, tp)

UNIT_ID = "JH-MATH-G2-U02"

PREREQUISITES = [
    ("JH-MATH-G1-U03", "一次方程式を等式の性質を使って解けること。文字を1つ消去した後は一次方程式を解く。"),
    ("JH-MATH-G2-U01", "多項式の加減と等式の変形ができること。加減法の計算や，$y=\\cdots$ の形への変形（代入法）に使う。"),
    ("JH-MATH-G1-U02", "数量の関係を文字式で表せること。文章題で2つの等式をつくるときに使う。"),
]
EXTENSIONS = [
    ("JH-MATH-G2-U03", "連立方程式の解を，2つの一次関数のグラフの交点の座標として読みとる。"),
    ("JH-MATH-G3-U03", "二次方程式の利用でも，数量を文字でおいて方程式をつくり，解が問題に適するかを確かめる。"),
    ("HS-MATH1-U01", "高校で一次不等式や文字をふくむ方程式を扱い，式の変形の力をさらに使う。"),
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


def dec(v):
    v = Fr(v)
    for k in range(0, 5):
        x = v * 10 ** k
        if x.denominator == 1:
            n = abs(int(x))
            s = str(n).rjust(k + 1, "0")
            out = s if k == 0 else s[:-k] + "." + s[-k:]
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


def nz(r, lo, hi):
    while True:
        v = r.randint(lo, hi)
        if v:
            return v


def term(c, v, first=False):
    """係数 c の項（c は Fraction でもよい）。"""
    c = Fr(c)
    if c == 0:
        return ""
    m = abs(c)
    if m == 1 and v:
        cs = ""
    elif m.denominator != 1:
        cs = f"\\dfrac{{{m.numerator}}}{{{m.denominator}}}"
    else:
        cs = str(m.numerator)
    sign = "-" if c < 0 else ("" if first else "+")
    return sign + cs + v


def dterm(c, v, first=False):
    """小数係数の項。"""
    c = Fr(c)
    if c == 0:
        return ""
    m = abs(c)
    cs = "" if (m == 1 and v) else dec(m)
    sign = "-" if c < 0 else ("" if first else "+")
    return sign + cs + v


def eq(a, b, c, X="x", Y="y", tf=term):
    lhs = tf(a, X, True) + tf(b, Y, not a)
    return f"{lhs}={ftex(c) if tf is term else dec(c)}"


def system(e1, e2):
    return f"$\\begin{{cases}}{e1}\\\\ {e2}\\end{{cases}}$"


def pair(x, y, X="x", Y="y"):
    return f"${X}={ftex(x)},\\ {Y}={ftex(y)}$"


def solve2(a, b, c, d, e, f):
    det = Fr(a * e - b * d)
    assert det != 0
    return (Fr(c * e - b * f) / det, Fr(a * f - c * d) / det)


def why_pair(E, cand, X="x", Y="y"):
    """候補の組がどちらの式を満たさないかの説明。"""
    x, y = cand
    msgs = []
    for k, (a, b, c) in enumerate(E):
        L = a * x + b * y
        if L != c:
            msgs.append(f"{'1つ目' if k == 0 else '2つ目'}の式に代入すると左辺は ${ftex(L)}$ となり，右辺の ${ftex(c)}$ と等しくない")
    return "。".join(msgs) + "。"


def pair_cands(E, x0, y0, extra=(), X="x", Y="y"):
    out = []
    for (cx, cy), mis in list(extra) + [((y0, x0), "x と y の値の取り違え"), ((x0, -y0), "符号の誤り"), ((-x0, y0), "符号の誤り"),
                                         ((-x0, -y0), "符号の誤り"), ((x0 + 1, y0), "計算の誤り"), ((x0, y0 - 1), "計算の誤り")]:
        if (cx, cy) == (x0, y0):
            continue
        w = why_pair(E, (cx, cy), X, Y)
        if not w.strip("。"):
            continue
        out.append((pair(cx, cy, X, Y), w, mis))
    return out


def rand_sys(r, lo=-6, hi=6, sol=(-6, 6), pos=False):
    x0 = r.randint(1, sol[1]) if pos else nz(r, *sol)
    y0 = r.randint(1, sol[1]) if pos else nz(r, *sol)
    while True:
        a, b, d, e = nz(r, lo, hi), nz(r, lo, hi), nz(r, lo, hi), nz(r, lo, hi)
        if a * e - b * d != 0 and (a, b) != (d, e):
            break
    return [(a, b, a * x0 + b * y0), (d, e, d * x0 + e * y0)], x0, y0


def solve_py(E, ask=None):
    t = ",".join(f"{fpy(a)}*x+({fpy(b)})*y-({fpy(c)})" for a, b, c in E)
    return f"solve([{t}],[x,y])" + (f"[{ask}]" if ask else "")


def _robust(g):
    import random as _random
    fn = g.fn

    def wrapped(r):
        for _ in range(80):
            try:
                return fn(r)
            except (AssertionError, ZeroDivisionError):
                r = _random.Random(r.random())
        return fn(r)
    wrapped.__name__ = fn.__name__
    g.fn = wrapped
    return g


# ----------------------------------------------------------------------
# 授業プリント
# ----------------------------------------------------------------------

LESSON = lesson(
    goals=["二元一次方程式とその解，連立方程式とその解の意味を理解し，解であるかどうかを代入して確かめられる。",
           "加減法・代入法を使い分けて，係数に分数・小数をふくむ連立方程式や $A=B=C$ の形の方程式を解ける。",
           "文章題で数量の関係を2つの等式に表し，連立方程式を解いて，その解が問題に適しているかを確かめられる。"],
    duration=100,
    readiness=["等式の性質を使って一次方程式を解ける（1年）。",
               "多項式の加法・減法と分配法則によるかっこのはずし方ができる（2年 式の計算）。",
               "等式を目的の文字について解ける（2年 式の計算）。",
               "代金・道のり・割合などの数量の関係を文字式で表せる（1年）。"],
    flow=[("導入：2つの条件から値を決める", 10, "おにぎりとパンの代金の問題を表にして考える"),
          ("二元一次方程式と連立方程式", 10, "解が無数にある方程式と，2つを組にしたときの解"),
          ("加減法", 20, "係数の絶対値をそろえて1つの文字を消去する（例題1）"),
          ("代入法と方程式の工夫", 20, "代入法，分数・小数の係数，$A=B=C$（例題2）"),
          ("連立方程式の利用", 30, "式のつくり方と解の確かめ（例題3）"),
          ("まとめと確認", 10, "確認問題と問題プリントの指示")],
    sections=[
        intro("in1", "2つの条件から2つの値を決める",
              "おにぎり1個とパン1個の値段がわからない。「おにぎり2個とパン1個で 380 円」だけでは，(おにぎり, パン)$=$(100, 180)，(120, 140)，… と，いくつも組が考えられる。しかし「おにぎり1個とパン2個で 400 円」という条件が加わると，組は1つに決まる。2つの条件を2つの方程式で表し，両方を同時に満たす値を求めるのが連立方程式である。",
              bullets=["1つの条件だけでは値の組は1つに決まらない。", "2つの条件を組にすると，両方を満たす組がただ1つに決まることが多い。"],
              points=[tp("最初に表をつくらせ，1つ目の条件を満たす組を何組か書き出させてから，2つ目の条件で絞りこむ。", ask="2つの条件を両方満たす組はどれか。", expect="おにぎり 120 円，パン 140 円。", timing="導入の5分")]),
        definition("df1", "二元一次方程式と連立方程式",
                   "2つの文字をふくむ一次方程式を二元一次方程式という。それを成り立たせる文字の値の組を，その方程式の解という。2つ以上の方程式を組にしたものを連立方程式といい，それらのどの方程式も成り立たせる文字の値の組を，連立方程式の解という。",
                   formula="$$\\begin{cases}2x+y=380\\\\ x+2y=400\\end{cases}\\quad\\text{の解は}\\quad x=120,\\ y=140$$",
                   conditions=["二元一次方程式 $x+y=5$ の解は，$(x,\\,y)=(1,\\,4),\\ (2,\\,3),\\ (0.5,\\,4.5),\\ \\ldots$ のように無数にある。",
                               "連立方程式の解は，2つの方程式の両方に代入して成り立つかどうかで確かめられる。"],
                   points=[tp("「解である」とは「代入すると等式が成り立つ」ことだと確認し，解の確かめを習慣にさせる。", ask="$x=2,\\ y=3$ は $2x+y=7$ と $x-y=1$ の連立方程式の解か。", expect="1つ目は成り立つが2つ目は $2-3=-1$ で成り立たないので，解ではない。")]),
        theorem("th1", "加減法と代入法",
                "$$A=B,\\ C=D\\ \\Longrightarrow\\ A+C=B+D,\\quad A-C=B-D$$",
                ["加減法：一方の文字の係数の絶対値をそろえ，2つの式を加えたりひいたりして，その文字を消去する。",
                 "代入法：一方の式を $y=\\cdots$（または $x=\\cdots$）の形にして他方の式に代入し，文字を消去する。代入するときは式にかっこをつける。",
                 "係数に分数があるときは分母の最小公倍数を，小数があるときは 10 や 100 を，両辺のすべての項にかけて整数にする。",
                 "$A=B=C$ の形の方程式は，$\\begin{cases}A=B\\\\ A=C\\end{cases}$ などの連立方程式になおして解く。"],
                body="どちらの方法も「2つの文字のうち1つを消去して，一次方程式にする」という考え方である。",
                proof=["$A=B$ と $C=D$ が同時に成り立つとき，等式の両辺に等しいものを加えても等式は成り立つので $A+C=B+C$。",
                       "$C=D$ なので，右辺の $C$ を $D$ におきかえて $A+C=B+D$。",
                       "同じように $A-C=B-D$ も成り立つ。",
                       "したがって，連立方程式の2つの式を辺どうし加えたりひいたりしてできる式も，もとの解で成り立つ。"],
                points=[tp("「消去」の意味を，係数がそろった2つの式をひくと $y$ がなくなる様子を板書で示して確認する。", caution="ひくときは右辺も含めてすべての項をひくこと。", timing="加減法の説明の直後"),
                        tp("代入法でかっこをつけ忘れる誤り（$3x-2y=5$ に $y=2x-1$ を代入して $3x-4x-1=5$ とする）を取り上げる。", ask="$-2y$ に $y=2x-1$ を代入するとどうなるか。", expect="$-2(2x-1)=-4x+2$。")]),
        derivation("dv1", "文章題で連立方程式をつくる手順",
                   ["何を $x,\\ y$ で表すかを決める（求めるものを文字でおくことが多い）。",
                    "問題文の中から，数量が等しい関係を2つ見つける（「合計」「全部で」「〜より…多い」など）。",
                    "表や図に整理して，それぞれの関係を等式に表す。",
                    "連立方程式を解く。",
                    "求めた解が問題に適しているか（自然数か，範囲に入っているか）を確かめて答える。"],
                   body="速さ・割合の問題では，単位（時間と分，％と小数）をそろえてから等式をつくる。",
                   points=[tp("等式をつくる前に，必ず表（または線分図）に整理させる。2つの関係が見えやすくなる。"),
                           tp("解の確かめでは，求めた値をもとの問題文の条件にあてはめて確かめさせる（つくった式に代入するだけでは，式のつくり方の誤りに気づけない）。", caution="式に代入して確かめるだけでは不十分。")]),
        example("ex1", "例題1　加減法",
                "連立方程式 $\\begin{cases}3x+2y=4\\\\ 5x+3y=7\\end{cases}$ を解きなさい。",
                ["$y$ の係数の絶対値を6にそろえる：上の式を3倍して $9x+6y=12$，下の式を2倍して $10x+6y=14$。",
                 "下の式から上の式をひく：$x=2$。", "$x=2$ を上の式に代入：$6+2y=4$ より $y=-1$。", "確かめ：$5\\times2+3\\times(-1)=7$。"],
                "$x=2,\\ y=-1$",
                thinking="係数の絶対値をそろえやすい文字を選ぶ。どちらの式を何倍するかを先に決める。",
                points=[tp("何倍するかを書いてから計算させると，右辺のかけ忘れが減る。", caution="左辺だけを何倍かして右辺を忘れる誤りが多い。")],
                misconceptions=[("上の式を3倍して $9x+6y=4$ とする", "右辺の4も3倍して $12$ にする")]),
        example("ex2", "例題2　係数に小数をふくむ連立方程式",
                "連立方程式 $\\begin{cases}0.3x+0.2y=1.6\\\\ y=x+3\\end{cases}$ を解きなさい。",
                ["上の式の両辺を10倍する：$3x+2y=16$。", "下の式を代入する：$3x+2(x+3)=16$。", "$5x+6=16$ より $x=2$。", "$y=2+3=5$。"],
                "$x=2,\\ y=5$",
                thinking="小数は両辺を10倍して整数の係数にする。$y=\\cdots$ の形の式があるときは代入法が便利。",
                points=[tp("10倍するときに右辺を忘れたり，一部の項だけを10倍したりする誤りを確認する。")]),
        example("ex3", "例題3　連立方程式の利用",
                "1個 80 円のおにぎりと1個 120 円のパンを合わせて 10 個買ったところ，代金の合計は 1040 円だった。おにぎりとパンをそれぞれ何個買ったか求めなさい。",
                ["おにぎりを $x$ 個，パンを $y$ 個とする。", "個数の関係：$x+y=10$。代金の関係：$80x+120y=1040$。",
                 "下の式を40でわると $2x+3y=26$。上の式を2倍してひくと $y=6$，$x=4$。", "どちらも自然数で，$80\\times4+120\\times6=1040$ となり問題に適する。"],
                "おにぎり4個，パン6個",
                thinking="「合わせて〜個」「代金の合計」の2つの関係を等式に表す。",
                points=[tp("個数・単価・代金を表に整理してから式をつくる手順を示す。", ask="代金の関係はどんな等式になるか。", expect="$80x+120y=1040$。")]),
        board("bd1", "板書案",
              [("① 連立方程式とは", ["二元一次方程式：解は無数", "2つ組にする → 解が決まる", "解の確かめ：両方に代入"]),
               ("② 解き方", ["加減法：係数の絶対値をそろえて消去", "代入法：かっこをつけて代入", "分数・小数 → すべての項に同じ数をかける", "$A=B=C$ → 2つの式に分ける"]),
               ("③ 利用", ["文字の決定 → 2つの関係 → 式 → 解く", "表・線分図で整理", "単位をそろえる（分と時間，％）", "解が問題に適するか確かめる"])],
              points=[tp("②の手順は，例題ごとに「どちらの文字を消去したか」を色で示して残す。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("加減法と代入法のどちらを使うかを，式の形（$y=\\cdots$ の形の式があるか，係数がそろえやすいか）で判断させる。", ask="どちらの方法が楽か，それはなぜか。", expect="$y=\\cdots$ の形があるので代入法。"),
               tp("求めた解は，もとの2つの式の両方に代入して確かめさせる。片方だけでは計算ミスを見落とす。"),
               tp("割合の文章題では，「昨年の人数」と「今年の人数」のどちらを文字でおいたかを最初に明記させる。", timing="利用の時間"),
               tp("速さの文章題では，時間を分と時間のどちらにそろえるかを決めてから式をつくらせる。", caution="時速と分の混在が多い。")],
              misconceptions=[("加減法で，式をひくときに右辺をひき忘れる", "辺どうしすべての項をひく"),
                              ("代入法で，かっこをつけずに代入する", "$-2y$ に $y=2x-1$ を代入するときは $-2(2x-1)$ とする"),
                              ("5% 増加を $0.5x$ と表す", "5% は $0.05$。増加後の量は $1.05x$")]),
        summary("sm1", "まとめ",
                ["連立方程式の解は，どの方程式も成り立たせる値の組。", "加減法・代入法で1つの文字を消去して一次方程式にする。",
                 "分数・小数の係数は，両辺のすべての項に同じ数をかけて整数にする。", "文章題は2つの関係を式にし，解が問題に適するかを確かめる。"]),
        check("ck1", "確認問題",
              [("連立方程式 $\\begin{cases}x+y=7\\\\ x-y=3\\end{cases}$ を解きなさい。", "$x=5,\\ y=2$"),
               ("連立方程式 $\\begin{cases}y=2x\\\\ 3x+y=10\\end{cases}$ を解きなさい。", "$x=2,\\ y=4$"),
               ("$x=1,\\ y=2$ は $2x+3y=8$ の解か。", "$2+6=8$ なので解である")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

@gen("basic_check", 4, ["condition_check", "concept"])
def a_check_sol(r):
    E, x0, y0 = rand_sys(r)
    cands = pair_cands(E, x0, y0)
    r.shuffle(cands)
    s = system(eq(*E[0]), eq(*E[1]))
    return MC(f"連立方程式 {s} の解として正しいものを，" + SEL4, pair(x0, y0), cands,
              f"$x={x0},\\ y={y0}$ は2つの式の両方を成り立たせる。", d=1,
              ap="連立方程式の解は，2つの式の両方を成り立たせる値の組。選択肢を代入して確かめる。",
              steps=[f"1つ目の式に代入：${E[0][0]}\\times({x0})+{E[0][1]}\\times({y0})={E[0][2]}$。", f"2つ目の式に代入：${E[1][0]}\\times({x0})+{E[1][1]}\\times({y0})={E[1][2]}$。", "両方成り立つので解である。"],
              alt=["加減法や代入法で実際に解いて，選択肢と比べる。"],
              pc=[("代入して確かめている", 1), ("両方の式を満たす組を選んでいる", 1)],
              pit=["1つ目の式だけを確かめて，2つ目の式を確かめない。"],
              chk=(f"solve([{E[0][0]}*x+({E[0][1]})*y-({E[0][2]}),{E[1][0]}*x+({E[1][1]})*y-({E[1][2]})],[x,y])", f"{{x:{x0},y:{y0}}}", None, "intermediate"))


def _elim_sys(r):
    """加減法向き：一方の文字の係数がそろう（またはそろえやすい）。"""
    x0, y0 = nz(r, -6, 6), nz(r, -6, 6)
    kind = r.choice(["same", "opp", "mult"])
    b = nz(r, -5, 5)
    a, d = nz(r, -5, 5), nz(r, -5, 5)
    if kind == "same":
        e = b
    elif kind == "opp":
        e = -b
    else:
        e = b * r.choice([2, 3, -2, -3])
    assert a * e - b * d != 0
    return [(a, b, a * x0 + b * y0), (d, e, d * x0 + e * y0)], x0, y0


def _sol_cands(E, x0, y0):
    (a, b, c), (d, e, f) = E
    extra = []
    try:
        extra.append((solve2(a, b, c, d, e, -f), "2つ目の式の右辺の符号の誤り"))
    except AssertionError:
        pass
    try:
        extra.append((solve2(a, b, c, d, -e, f), "消去するときの符号の誤り"))
    except AssertionError:
        pass
    extra = [(p, m) for p, m in extra if all(Fr(v).denominator == 1 for v in p)]
    return pair_cands(E, x0, y0, extra)


@gen("basic_check", 6, ["computation"])
def a_elim(r):
    E, x0, y0 = _elim_sys(r)
    s = system(eq(*E[0]), eq(*E[1]))
    (a, b, c), (d, e, f) = E
    return MC(f"連立方程式 {s} を解いた結果として正しいものを，" + SEL4, pair(x0, y0), _sol_cands(E, x0, y0),
              f"加減法で $y$ を消去すると $x={x0}$，これを代入して $y={y0}$。", d=2,
              ap="$y$ の係数の絶対値をそろえ，2つの式を加えるかひいて $y$ を消去する（加減法）。",
              steps=[f"$y$ の係数 ${b}$ と ${e}$ の絶対値をそろえる。", f"2つの式を加えるかひいて $y$ を消去し，$x={x0}$。", f"$x={x0}$ を1つ目の式に代入して $y={y0}$。", "両方の式に代入して確かめる。"],
              alt=["1つ目の式を $y=\\cdots$ の形にして2つ目の式に代入する代入法でも解ける。"],
              pc=[("1つの文字を正しく消去している", 1), ("解を正しく求めている", 1)],
              pit=["式をひくとき，右辺もひくのを忘れる。", "符号が同じなのに加えてしまう。"],
              chk=(f"solve([{a}*x+({b})*y-({c}),{d}*x+({e})*y-({f})],[x,y])", f"{{x:{x0},y:{y0}}}", None, "intermediate"))


@gen("basic_check", 5, ["computation"])
def a_subst(r):
    x0, y0 = nz(r, -6, 6), nz(r, -6, 6)
    m, n0 = nz(r, -4, 4), None
    n0 = y0 - m * x0
    a, b = nz(r, -5, 5), nz(r, -5, 5)
    assert a + b * m != 0
    c = a * x0 + b * y0
    rhs = term(m, "x", True) + (term(n0, "", False) if n0 else "")
    E = [(-m, 1, n0), (a, b, c)]
    s = system(f"y={rhs}", eq(a, b, c))
    extra = []
    if b != 0 and n0:
        # b*(mx) + n0 として計算（n0 に b をかけ忘れ）
        den = a + b * m
        wx = Fr(c - n0, den)
        if wx.denominator == 1 and wx != x0:
            extra.append(((wx, m * wx + n0), "かっこをつけずに代入し，定数項に係数をかけ忘れている"))
    return MC(f"連立方程式 {s} を解いた結果として正しいものを，" + SEL4, pair(x0, y0), pair_cands(E, x0, y0, extra),
              f"1つ目の式を2つ目の式に代入して ${term(a, 'x', True)}{term(b, '', False)}({rhs})={c}$。これを解いて $x={x0}$，$y={y0}$。", d=2,
              ap="$y=\\cdots$ の形の式があるときは，それを他方の式の $y$ にかっこをつけて代入する（代入法）。",
              steps=[f"代入：${term(a, 'x', True)}{term(b, '', False)}({rhs})={c}$。", f"かっこをはずして整理し，$x={x0}$。", f"1つ目の式に $x={x0}$ を代入して $y={y0}$。"],
              alt=["1つ目の式を移項して $x$ と $y$ の項を左辺に集め，加減法で解いてもよい。"],
              pc=[("かっこをつけて正しく代入している", 1), ("解を正しく求めている", 1)],
              pit=["かっこをつけずに代入し，定数項に係数をかけ忘れる。"],
              chk=(f"solve([y-({m})*x-({n0}),{a}*x+({b})*y-({c})],[x,y])", f"{{x:{x0},y:{y0}}}", None, "intermediate"))


@gen("basic_check", 5, ["computation"])
def a_mark(r):
    x0, y0 = r.randint(1, 9), r.randint(1, 9)
    while True:
        a, b, d, e = nz(r, -5, 5), nz(r, -5, 5), nz(r, -5, 5), nz(r, -5, 5)
        if a * e - b * d != 0 and (a, b) != (d, e):
            break
    E = [(a, b, a * x0 + b * y0), (d, e, d * x0 + e * y0)]
    ask = r.choice(["x", "y"])
    v = x0 if ask == "x" else y0
    s = system(eq(*E[0]), eq(*E[1]))
    return MARK(f"連立方程式 {s} の解のうち，${ask}$ の値を求めなさい。", v,
                f"解は $x={x0},\\ y={y0}$ なので，${ask}={v}$。", f"solve([{a}*x+({b})*y-({E[0][2]}),{d}*x+({e})*y-({E[1][2]})],[x,y])[{ask}]", d=2, p=2,
                ap=f"求めたい ${ask}$ が残るように，もう一方の文字を消去する。",
                steps=[f"{'$y$' if ask == 'x' else '$x$'} の係数の絶対値をそろえる。", f"2つの式を加えるかひいて消去し，${ask}={v}$。", "もう一方の文字も求め，両方の式に代入して確かめる。"],
                alt=["代入法で解いても同じ値になる。"],
                pc=[("1つの文字を正しく消去している", 1), ("正しい値を求めている", 1)],
                pit=["消去する文字を誤り，求めたい文字が消えてしまう。"])


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 5, ["computation", "condition_check"])
def b_frac_dec(r):
    x0, y0 = nz(r, -6, 6), nz(r, -6, 6)
    kind = r.choice(["dec", "frac", "dec2"])
    a2, b2 = nz(r, -5, 5), nz(r, -5, 5)
    E2 = (a2, b2, a2 * x0 + b2 * y0)
    if kind in ("dec", "dec2"):
        k = 10 if kind == "dec" else 100
        A, B = nz(r, -9, 9), nz(r, -9, 9)
        C = A * x0 + B * y0
        e1 = f"{dterm(Fr(A, k), 'x', True)}{dterm(Fr(B, k), 'y')}={dec(Fr(C, k))}"
        how = f"両辺を ${k}$ 倍して ${eq(A, B, C)}$"
        w = (solve2(A, B, Fr(C, k), a2, b2, E2[2]), f"右辺を{k}倍し忘れている")
    else:
        p, q = r.choice([(2, 3), (3, 4), (2, 5), (4, 3), (3, 2), (6, 4), (5, 2)])
        L = p * q // __import__("math").gcd(p, q)
        A, B = nz(r, -3, 3), nz(r, -3, 3)
        assert __import__("math").gcd(abs(A), p) == 1 and __import__("math").gcd(abs(B), q) == 1
        c = Fr(A, p) * x0 + Fr(B, q) * y0
        assert c.denominator == 1
        e1 = f"{'-' if A < 0 else ''}\\dfrac{{{abs(A) if abs(A) != 1 else ''}x}}{{{p}}}{'-' if B < 0 else '+'}\\dfrac{{{abs(B) if abs(B) != 1 else ''}y}}{{{q}}}={c}"
        A2, B2, C2 = A * L // p, B * L // q, c * L
        how = f"両辺に ${L}$ をかけて ${eq(A2, B2, C2)}$"
        w = (solve2(A2, B2, c, a2, b2, E2[2]), "分母をはらうとき，右辺に分母の最小公倍数をかけ忘れている")
        A, B, C = A2, B2, C2
    assert A * b2 - B * a2 != 0
    extra = []
    try:
        if all(Fr(v).denominator == 1 for v in w[0]):
            extra.append((w[0], w[1]))
    except Exception:
        pass
    Ecore = [(A, B, A * x0 + B * y0), E2]
    s = system(e1, eq(*E2))
    return MC(f"連立方程式 {s} を解いた結果として正しいものを，" + SEL4, pair(x0, y0), pair_cands(Ecore, x0, y0, extra),
              f"1つ目の式は，{how}。これと2つ目の式を連立して $x={x0},\\ y={y0}$。", d=3, p=4,
              ap="係数に小数・分数がある式は，両辺のすべての項に同じ数をかけて整数の係数になおしてから解く。",
              steps=[f"1つ目の式を整数の係数にする：{how}。", "加減法（または代入法）で1つの文字を消去する。", f"$x={x0},\\ y={y0}$。", "もとの式（小数・分数のある式）に代入して確かめる。"],
              alt=["小数のまま加減法を使うこともできるが，計算ミスが増えるので整数になおすのが確実。"],
              pc=[("係数を正しく整数になおしている", 2), ("解を正しく求めている", 2)],
              pit=["右辺に同じ数をかけ忘れる。", "一部の項だけに同じ数をかける。"],
              chk=(f"solve([{A}*x+({B})*y-({A * x0 + B * y0}),{a2}*x+({b2})*y-({E2[2]})],[x,y])", f"{{x:{x0},y:{y0}}}", None, "intermediate"))


@gen("standard_practice", 3, ["computation", "condition_check"])
def b_abc(r):
    x0, y0 = nz(r, -5, 5), nz(r, -5, 5)
    a, b, d, e = nz(r, -5, 5), nz(r, -5, 5), nz(r, -5, 5), nz(r, -5, 5)
    C = a * x0 + b * y0
    # 3つ目の式 C を数にし，2つ目の式を d x + e y + k の形にして合わせる
    k = C - (d * x0 + e * y0)
    assert a * e - b * d != 0
    mid = term(d, "x", True) + term(e, "y") + (term(k, "") if k else "")
    lhs = term(a, "x", True) + term(b, "y")
    E = [(a, b, C), (d, e, C - k)]
    w = (solve2(a, b, C, d, e, C), "2つ目の式の定数項を右辺に移すのを忘れている") if k else None
    extra = []
    if w and all(Fr(v).denominator == 1 for v in w[0]) and w[0] != (x0, y0):
        extra.append(w)
    return MC(f"方程式 ${lhs}={mid}={C}$ を解いた結果として正しいものを，" + SEL4, pair(x0, y0), pair_cands(E, x0, y0, extra),
              f"$\\begin{{cases}}{lhs}={C}\\\\ {mid}={C}\\end{{cases}}$ として解くと $x={x0},\\ y={y0}$。", d=3, p=4,
              ap="$A=B=C$ の形は，$A=C,\\ B=C$ のように2つの方程式に分けて連立方程式として解く。数だけの $C$ を使うと簡単になる。",
              steps=[f"$\\begin{{cases}}{lhs}={C}\\\\ {mid}={C}\\end{{cases}}$ と分ける。", f"2つ目の式を整理して ${eq(d, e, C - k)}$。", f"連立方程式を解いて $x={x0},\\ y={y0}$。"],
              alt=["$A=B$ と $A=C$ の組み合わせで解いても同じ解になる。"],
              pc=[("2つの方程式に正しく分けている", 2), ("解を正しく求めている", 2)],
              pit=["$A=B=C$ を3つの式すべて使おうとして混乱する。", "定数項の移項を忘れる。"],
              chk=(f"solve([{a}*x+({b})*y-({C}),{d}*x+({e})*y+({k})-({C})],[x,y])", f"{{x:{x0},y:{y0}}}", None, "intermediate"))


@gen("standard_practice", 4, ["condition_check", "computation"])
def b_param(r):
    x0, y0 = nz(r, -4, 4), nz(r, -4, 4)
    a0, b0 = r.randint(1, 7), r.randint(1, 7)
    assert a0 != b0 and x0 * x0 != y0 * y0
    kind = r.choice(["swap", "mix"])
    if kind == "swap":
        c1, c2 = a0 * x0 + b0 * y0, b0 * x0 + a0 * y0
        s = system(f"ax+by={c1}", f"bx+ay={c2}")
        e1, e2 = f"{term(x0, 'a', True)}{term(y0, 'b')}={c1}", f"{term(x0, 'b', True)}{term(y0, 'a')}={c2}"
        py = f"solve([{x0}*a+({y0})*b-({c1}),{x0}*b+({y0})*a-({c2})],[a,b])"
    else:
        k1, k2 = nz(r, -3, 3), nz(r, -3, 3)
        c1 = a0 * x0 + k1 * y0
        c2 = k2 * x0 + b0 * y0
        s = system(f"ax{term(k1, 'y')}={c1}", f"{term(k2, 'x', True)}+by={c2}")
        e1, e2 = f"{term(x0, 'a', True)}{term(k1 * y0, '')}={c1}", f"{term(k2 * x0, '', True)}{term(y0, 'b')}={c2}"
        py = f"solve([{x0}*a+({k1 * y0})-({c1}),{k2 * x0}+({y0})*b-({c2})],[a,b])"
    ask = r.choice(["a", "b"])
    v = a0 if ask == "a" else b0
    return MARK(f"$x,\\ y$ についての連立方程式 {s} の解が $x={x0},\\ y={y0}$ であるとき，${ask}$ の値を求めなさい。", v,
                f"解を代入すると ${e1}$，${e2}$。これを $a,\\ b$ についての連立方程式として解くと $a={a0},\\ b={b0}$。", f"{py}[{ask}]", d=3, p=4,
                ap="解 $x,\\ y$ を代入すると，$a,\\ b$ についての連立方程式ができる。文字の役割が入れかわることに注意する。",
                steps=[f"$x={x0},\\ y={y0}$ を代入：${e1}$，${e2}$。", "$a,\\ b$ についての連立方程式を解く。", f"$a={a0},\\ b={b0}$。"],
                alt=[f"求めた $a,\\ b$ をもとの連立方程式に入れ，実際に解いて $x={x0},\\ y={y0}$ になるかを確かめる。"],
                pc=[("解を代入して $a,\\ b$ の式をつくっている", 2), ("正しい値を求めている", 2)],
                pit=["$x,\\ y$ の値を代入する場所を取り違える（$a$ と $b$ の位置が式ごとにちがう）。"])


WORD_PRICE = [("鉛筆", "本", "ノート", "冊"), ("りんご", "個", "みかん", "個"), ("ケーキ", "個", "プリン", "個"), ("ボールペン", "本", "消しゴム", "個"), ("大人", "人", "中学生", "人")]


def _price_problem(r):
    it = r.choice(WORD_PRICE)
    x0 = r.choice(range(60, 400, 10))
    y0 = r.choice(range(50, 300, 10))
    assert x0 != y0
    p1, q1, p2, q2 = r.randint(1, 5), r.randint(1, 5), r.randint(1, 5), r.randint(1, 5)
    assert p1 * q2 - p2 * q1 != 0
    T1, T2 = p1 * x0 + q1 * y0, p2 * x0 + q2 * y0
    if it[0] == "大人":
        txt = f"ある美術館の入館料は，大人 {p1} 人と中学生 {q1} 人で {T1} 円，大人 {p2} 人と中学生 {q2} 人で {T2} 円である。大人1人の入館料を $x$ 円，中学生1人の入館料を $y$ 円とする。"
    else:
        txt = f"{it[0]} {p1} {it[1]}と{it[2]} {q1} {it[3]}の代金の合計は {T1} 円，{it[0]} {p2} {it[1]}と{it[2]} {q2} {it[3]}の代金の合計は {T2} 円である。{it[0]}1{it[1]}の値段を $x$ 円，{it[2]}1{it[3]}の値段を $y$ 円とする。"
    E = [(p1, q1, T1), (p2, q2, T2)]
    wrongs = [[(p1, q1, T1), (q2, p2, T2)], [(p1, q1, T2), (p2, q2, T1)], [(q1, p1, T1), (q2, p2, T2)]]
    names = (it[0] if it[0] != "大人" else "大人1人の入館料", it[2] if it[0] != "大人" else "中学生1人の入館料")
    return txt, E, x0, y0, wrongs, names


def _count_problem(r):
    it = r.choice(WORD_PRICE[:4])
    pa = r.choice(range(50, 200, 10))
    pb = r.choice(range(60, 250, 10))
    assert pa != pb
    x0, y0 = r.randint(2, 12), r.randint(2, 12)
    N, T = x0 + y0, pa * x0 + pb * y0
    txt = f"1{it[1]} {pa} 円の{it[0]}と1{it[3]} {pb} 円の{it[2]}を合わせて {N} {'個' if it[1] == it[3] == '個' else '点'}買ったところ，代金の合計は {T} 円だった。{it[0]}を $x$ {it[1]}，{it[2]}を $y$ {it[3]}買ったとする。"
    E = [(1, 1, N), (pa, pb, T)]
    wrongs = [[(1, 1, N), (pb, pa, T)], [(1, 1, T), (pa, pb, N)], [(pa, pb, N), (1, 1, T)]]
    return txt, E, x0, y0, wrongs, (it[0], it[2], it[1], it[3])


def _speed_problem(r):
    v1, v2 = r.choice([(4, 6), (3, 5), (4, 12), (3, 4), (5, 15), (4, 8), (2, 6)])
    t1, t2 = Fr(r.randint(1, 6), 2), Fr(r.randint(1, 6), 2)
    x0, y0 = v1 * t1, v2 * t2
    assert x0.denominator == 1 and y0.denominator == 1
    D, T = x0 + y0, t1 + t2
    Ttxt = f"{int(T)} 時間" if T.denominator == 1 else f"{int(T)} 時間 30 分"
    txt = f"A 地点から {dec(D)} km はなれた C 地点まで，途中の B 地点までは時速 {v1} km で歩き，B 地点から C 地点までは時速 {v2} km で走ったところ，全体で {Ttxt}かかった。A 地点から B 地点までの道のりを $x$ km，B 地点から C 地点までの道のりを $y$ km とする。"
    E = [(1, 1, D), (Fr(1, v1), Fr(1, v2), T)]
    wrongs = [[(1, 1, D), (v1, v2, T)], [(1, 1, T), (Fr(1, v1), Fr(1, v2), D)], [(1, 1, D), (Fr(1, v2), Fr(1, v1), T)]]
    return txt, E, int(x0), int(y0), wrongs, ("A 地点から B 地点まで", "B 地点から C 地点まで")


def _sys_txt(E):
    def side(a, b):
        def one(c, v, first):
            c = Fr(c)
            if c.denominator != 1:
                s = f"\\dfrac{{{v}}}{{{c.denominator}}}" if c.numerator == 1 else f"\\dfrac{{{c.numerator}{v}}}{{{c.denominator}}}"
                return s if first else "+" + s
            return term(c, v, first)
        return one(a, "x", True) + one(b, "y", False)
    return system(f"{side(E[0][0], E[0][1])}={ftex(E[0][2])}", f"{side(E[1][0], E[1][1])}={ftex(E[1][2])}")


@gen("standard_practice", 8, ["application", "computation"])
def b_word(r):
    maker = r.choice([_price_problem, _price_problem, _count_problem, _speed_problem])
    txt, E, x0, y0, wrongs, names = maker(r)
    kind = r.choice(["eq", "ans", "ans"])
    if kind == "eq":
        right = _sys_txt(E)
        reasons = ["2つ目の関係で，数量と文字の対応（どちらに $x$，どちらに $y$）を取り違えている。",
                   "右辺に入れる数量を2つの式で入れかえている。",
                   "係数と文字の対応を取り違えている。"]
        if maker is _speed_problem:
            reasons = ["時間の関係を「道のり × 速さ」としている。時間は 道のり ÷ 速さ で表す。",
                       "道のりの和と時間の和を取り違えている。",
                       "それぞれの道のりにかかる時間の速さを取り違えている。"]
        if maker is _count_problem:
            reasons = ["代金の関係で，値段と個数の対応を取り違えている。",
                       "個数の和と代金の和を取り違えている。",
                       "個数の関係と代金の関係の右辺を入れかえている。"]
        cands = [(_sys_txt(w), rs, "数量の関係の式への表し方の誤り") for w, rs in zip(wrongs, reasons)]
        return MC(txt + "$x,\\ y$ についての連立方程式をつくったものとして正しいものを，" + SEL4, right, cands,
                  f"2つの数量の関係を式に表すと {right}。", d=3, p=4,
                  ap="問題文の中から「合計」「全部で」など，等しい関係を2つ見つけて，それぞれ等式に表す。",
                  steps=["何を $x,\\ y$ としたかを確認する。", "1つ目の関係を等式に表す。", "2つ目の関係を等式に表す。", f"連立方程式は {right}。"],
                  alt=[f"答え（$x={x0},\\ y={y0}$）を選択肢の式に代入して，両方が成り立つものを選んでも確かめられる。"],
                  pc=[("1つ目の関係を正しく式にしている", 2), ("2つ目の関係を正しく式にしている", 2)],
                  pit=["速さの問題で，時間を道のり×速さとしてしまう。", "単価と個数の対応を取り違える。"])
    ask = r.choice(["x", "y"])
    v = x0 if ask == "x" else y0
    unit = {_price_problem: "円", _count_problem: (names[2] if ask == "x" else names[3]) if maker is _count_problem else "", _speed_problem: "km"}[maker]
    what = names[0] if ask == "x" else names[1]
    if maker is _count_problem:
        q = f"{what}を何{names[2] if ask == 'x' else names[3]}買ったか求めなさい。"
    elif maker is _speed_problem:
        q = f"{what}の道のりは何 km か求めなさい。"
    else:
        q = f"{what}は何円か求めなさい。" if what.endswith("入館料") else f"{what}1つの値段は何円か求めなさい。"
    s = _sys_txt(E)
    return MARK(txt + q, v, f"連立方程式 {s} を解くと $x={x0},\\ y={y0}$。これは問題に適する。", solve_py(E, ask), d=3, p=4, unit=unit or None,
                ap="2つの数量の関係を等式に表して連立方程式をつくり，解いた後に問題に適するかを確かめる。",
                steps=[f"連立方程式をつくる：{s}。", "係数を整数にしてから，加減法で1つの文字を消去する。", f"$x={x0},\\ y={y0}$。", "求めた値が問題の条件に合うかを確かめる。"],
                alt=["表をつくって，条件を満たす組を順に調べる方法でも確かめられる。"],
                pc=[("連立方程式を正しくつくっている", 2), ("正しく解いて答えている", 2)],
                pit=["求める文字を取り違える。", "単位（時間・分）をそろえずに式をつくる。"])


# ======================================================================
# C 思考力・記述応用
# ======================================================================

@gen("thinking_writing", 4, ["application", "computation", "condition_check"])
def c_word_hard(r):
    kind = r.choice(["pct", "pct", "minutes"])
    if kind == "pct":
        who = r.choice([("ある中学校の生徒数", "男子", "女子", "人"), ("ある店のケーキの販売数", "ショートケーキ", "チーズケーキ", "個"), ("ある町の図書館の利用者数", "大人", "子ども", "人")])
        x0, y0 = r.randint(5, 20) * 20, r.randint(5, 20) * 20
        p, q = r.choice([5, 10, 15, 20]), r.choice([5, 10, 15, 20])
        up_x, up_y = r.choice([1, -1]), r.choice([1, -1])
        assert up_x != up_y or r.random() < 0.3
        dx, dy = up_x * p * x0 // 100, up_y * q * y0 // 100
        D = dx + dy
        assert D != 0
        N = x0 + y0
        word = lambda u, pct: f"{pct}％{'増え' if u > 0 else '減り'}"
        txt = (f"{who[0]}は，昨年は{who[1]}と{who[2]}を合わせて {N} {who[3]}だった。今年は昨年と比べて，{who[1]}が{word(up_x, p)}，{who[2]}が{word(up_y, q)}，"
               f"全体では {abs(D)} {who[3]}{'増えた' if D > 0 else '減った'}。")
        ask = r.choice(["x", "y"])
        last = x0 if ask == "x" else y0
        now = x0 + dx if ask == "x" else y0 + dy
        tgt = r.choice(["last", "now"])
        nm = who[1] if ask == "x" else who[2]
        v = last if tgt == "last" else now
        q_ = f"{'昨年' if tgt == 'last' else '今年'}の{nm}は何{who[3]}か求めなさい。"
        sx = f"{'+' if up_x > 0 else '-'}\\dfrac{{{p}}}{{100}}x"
        sy = f"{'+' if up_y > 0 else '-'}\\dfrac{{{q}}}{{100}}y"
        s = f"$\\begin{{cases}}x+y={N}\\\\ {sx[1:] if sx[0] == '+' else sx}{sy}={D}\\end{{cases}}$"
        rate = 100 + (p * up_x if ask == "x" else q * up_y)
        extra_e = "" if tgt == "last" else f"今年の{nm}は ${last}\\times\\dfrac{{{rate}}}{{100}}={now}$ {who[3]}。"
        return MARK(txt + q_, v, f"昨年の{who[1]}を $x$ {who[3]}，{who[2]}を $y$ {who[3]}とすると {s}。これを解くと $x={x0},\\ y={y0}$。" + extra_e,
                    solve_py([(1, 1, N), (Fr(p * up_x, 100), Fr(q * up_y, 100), D)], ask) + ("" if tgt == "last" else f"*Rational({rate},100)"), d=4, p=8, unit=who[3],
                    ap="昨年の数を $x,\\ y$ とおくと式がつくりやすい。増減した数を割合で表し，「全体の増減」の関係を式にする。",
                    steps=[f"昨年の{who[1]}を $x$，{who[2]}を $y$ とする。", f"昨年の合計：$x+y={N}$。", "増減の関係：増減した数の和が全体の増減になる。",
                           f"連立方程式 {s} を解いて $x={x0},\\ y={y0}$。", f"答え：{v} {who[3]}。"],
                    alt=["今年の数を文字でおくこともできるが，割合のもとになる量（昨年）を文字でおくほうが式が簡単になる。"],
                    pc=[("昨年の合計の式をつくっている", 2), ("増減の関係を割合で正しく式にしている", 3), ("問われている量を正しく答えている", 3)],
                    pit=["増減した数ではなく今年の数を求めるとき，昨年の数を答えてしまう。", "減少を $+$ で表してしまう。"])
    v1, v2 = r.choice([(60, 180), (80, 200), (70, 210), (60, 150), (50, 150), (80, 240)])
    t1, t2 = r.randint(3, 15), r.randint(2, 10)
    x0, y0 = v1 * t1, v2 * t2
    D, T = x0 + y0, t1 + t2
    ask = r.choice(["x", "y"])
    v = x0 if ask == "x" else y0
    s = f"$\\begin{{cases}}x+y={D}\\\\ \\dfrac{{x}}{{{v1}}}+\\dfrac{{y}}{{{v2}}}={T}\\end{{cases}}$"
    return MARK(f"Kさんは家から {D} m はなれた駅まで行くのに，はじめは分速 {v1} m で歩き，途中から分速 {v2} m で走ったところ，ちょうど {T} 分で駅に着いた。Kさんが{'歩いた' if ask == 'x' else '走った'}道のりは何 m か求めなさい。", v,
                f"歩いた道のりを $x$ m，走った道のりを $y$ m とすると {s}。これを解くと $x={x0},\\ y={y0}$。", solve_py([(1, 1, D), (Fr(1, v1), Fr(1, v2), T)], ask), d=4, p=8, unit="m",
                ap="道のりの関係と時間の関係の2つを式にする。時間は 道のり ÷ 速さ。単位（m と分）がそろっていることを確かめる。",
                steps=["歩いた道のりを $x$ m，走った道のりを $y$ m とする。", f"道のり：$x+y={D}$。", f"時間：$\\dfrac{{x}}{{{v1}}}+\\dfrac{{y}}{{{v2}}}={T}$。", f"解いて $x={x0},\\ y={y0}$。"],
                alt=[f"歩いた時間を $a$ 分，走った時間を $b$ 分とおくと $a+b={T}$，${v1}a+{v2}b={D}$ となり，係数が整数のまま解ける。"],
                pc=[("道のりの式をつくっている", 3), ("時間の式をつくっている", 3), ("正しく答えている", 2)],
                pit=["時間の式を $" + str(v1) + "x+" + str(v2) + "y=" + str(T) + "$ としてしまう。"])


@gen("thinking_writing", 3, ["cross_unit", "concept"], rel=["JH-MATH-G2-U03"])
def c_graph(r):
    x0, y0 = nz(r, -5, 5), nz(r, -5, 5)
    m1 = nz(r, -3, 3)
    n1 = y0 - m1 * x0
    a, b = nz(r, -4, 4), nz(r, -4, 4)
    assert a + b * m1 != 0 and Fr(-a, b) != m1
    c = a * x0 + b * y0
    l1 = f"y={term(m1, 'x', True)}{term(n1, '') if n1 else ''}"
    l2 = eq(a, b, c)
    E = [(-m1, 1, n1), (a, b, c)]
    cands = [(f"$({ftex(cx)},\\,{ftex(cy)})$", why_pair(E, (cx, cy)) + "この点は2つの直線の両方の上にはない。", "交点と連立方程式の解の対応の誤り")
             for cx, cy in [(y0, x0), (x0, -y0), (-x0, y0), (0, n1), (-x0, -y0)] if (cx, cy) != (x0, y0) and why_pair(E, (cx, cy)).strip("。")]
    return MC(f"座標平面上に，2つの直線 $\\ell:\\ {l1}$ と $m:\\ {l2}$ がある。2直線 $\\ell,\\ m$ の交点の座標として正しいものを，" + SEL4 + "ただし，2直線の交点の座標は，2つの直線の式を組にした連立方程式の解として求められるものとする。",
              f"$({x0},\\,{y0})$", cands, f"連立方程式 {system(l1, l2)} を解くと $x={x0},\\ y={y0}$。交点は $({x0},\\,{y0})$。", d=4, p=8,
              ap="交点は2つの直線の両方の上にある点なので，その座標は2つの直線の式を同時に満たす。つまり連立方程式の解である（次の単元「一次関数」につながる考え方）。",
              steps=[f"連立方程式 {system(l1, l2)} をつくる。", "代入法で $y$ を消去する。", f"$x={x0},\\ y={y0}$。", f"交点は $({x0},\\,{y0})$。"],
              alt=["グラフを方眼にかいて交点を読みとり，連立方程式の解と一致することを確かめる。"],
              pc=[("交点を連立方程式の解として求めている", 4), ("正しく解いている", 4)],
              pit=["$y$ 切片を交点と取り違える。", "$x$ 座標と $y$ 座標を入れかえる。"],
              chk=(f"solve([y-({m1})*x-({n1}),{a}*x+({b})*y-({c})],[x,y])", f"{{x:{x0},y:{y0}}}", None, "intermediate"))


REASONS = [
    ("連立方程式 $\\begin{cases}2x+3y=7\\\\ 4x-y=7\\end{cases}$ を加減法で解くとき，下の式を3倍して上の式に加える理由",
     "$y$ の係数を $3$ と $-3$ にして，2つの式を加えると $y$ が消去され，$x$ だけの一次方程式になるから。",
     [("下の式を3倍すると，$x$ の係数が上の式と等しくなるから。", "3倍すると $x$ の係数は $12$ になり，上の式の $2$ とは等しくならない。"),
      ("式を3倍すると，解が3倍になって求めやすくなるから。", "両辺に同じ数をかけても，方程式の解は変わらない。"),
      ("加減法では，必ずどちらかの式を3倍しなければならないから。", "何倍するかは係数によって決まる。いつも3倍するわけではない。")]),
    ("「1個 50 円の品物と1個 80 円の品物を合わせて何個か買った」という文章題で，連立方程式を解いたら一方の個数が $2.5$ 個になった。この解を答えとしない理由",
     "個数は自然数（または0）でなければならないので，$2.5$ 個は問題に適さないから。",
     [("連立方程式の解は，必ず整数になるはずだから。", "連立方程式の解は整数とは限らない。問題の条件に合うかで判断する。"),
      ("小数の解は，計算をまちがえたときにしか出てこないから。", "計算が正しくても，問題の条件に合わない解が出ることはある。"),
      ("$2.5$ は2つの式のうち一方しか満たさないから。", "連立方程式の解は両方の式を満たしている。問題の条件（個数）に合わないことが理由である。")]),
    ("二元一次方程式 $x+y=10$ だけでは，$x,\\ y$ の値が1つに決まらない理由",
     "$x+y=10$ を満たす $x,\\ y$ の値の組は $(1,\\,9),\\ (2,\\,8),\\ (0.5,\\,9.5),\\ \\ldots$ のように無数にあるから。",
     [("$x$ と $y$ の係数が等しいから。", "係数が等しくなくても，二元一次方程式1つだけでは値の組は無数にある。"),
      ("右辺の $10$ が偶数だから。", "右辺の数によらず，解は無数にある。"),
      ("$x,\\ y$ が負の数になることもあるから。", "負の数を除いても，小数などをふくめると解は無数にある。")]),
    ("$3x-2y=8$ に $y=x-1$ を代入するとき，$3x-2(x-1)=8$ のようにかっこをつける理由",
     "$y$ は $x-1$ という式全体を表すので，$-2$ を $x$ と $-1$ の両方にかける必要があるから。",
     [("かっこをつけると，$x$ の係数が大きくなって解きやすくなるから。", "かっこは係数を大きくするためのものではない。"),
      ("かっこをつけないと，$x$ が消えてしまうから。", "かっこの有無で $x$ が消えるかどうかが決まるわけではない。"),
      ("代入法では，代入する式に必ず2をかけるから。", "かける数は代入する場所の係数で決まる。")]),
    ("係数に小数をふくむ方程式 $0.2x+0.3y=1.2$ を解くとき，両辺を10倍して $2x+3y=12$ としてよい理由",
     "等式の両辺に同じ数をかけても等式は成り立ち，解は変わらないから。",
     [("小数の係数のままでは，連立方程式の解が存在しないから。", "小数の係数でも解は存在する。計算を簡単にするために整数になおす。"),
      ("10倍すると，解も10倍になって整数になるから。", "両辺に同じ数をかけても解は変わらない。"),
      ("左辺だけを10倍すれば十分だから。", "左辺だけを10倍すると等式が成り立たなくなる。右辺も10倍する。")]),
    ("$A=B=C$ の形の方程式を，$\\begin{cases}A=C\\\\ B=C\\end{cases}$ という連立方程式になおして解いてよい理由",
     "$A=B=C$ は「$A$ と $C$ が等しく，$B$ と $C$ も等しい」ことを表しているので，2つの等式が同時に成り立つから。",
     [("$A=B=C$ は，$A+B=C$ と同じ意味だから。", "$A=B=C$ は3つの式の値が等しいことを表し，$A+B=C$ ではない。"),
      ("3つの式のうち1つは使わなくてよいので，どれを使っても答えが変わるから。", "どの2つの組を選んでも，同じ解が得られる。"),
      ("$A=C$ だけで解が決まるから。", "1つの二元一次方程式だけでは解は1つに決まらない。")]),
    ("2つの直線の交点の座標を，2つの直線の式を組にした連立方程式を解いて求められる理由",
     "交点は2つの直線の両方の上にある点なので，その座標は2つの式を同時に満たし，連立方程式の解になるから。",
     [("2つの直線の傾きが等しいとき，交点が1つに決まるから。", "傾きが等しい（平行な）2直線は交わらない。"),
      ("交点の座標はいつも整数だから。", "交点の座標は整数とは限らない。"),
      ("一方の直線の $y$ 切片が交点の $y$ 座標になるから。", "$y$ 切片が交点になるとは限らない。")]),
]


@gen("thinking_writing", 3, ["written_reasoning", "concept"])
def c_reason(r):
    q, right, ws = r.choice(REASONS)
    return MC(f"Kさんは，連立方程式について説明する文を考えた。{q}として最も適するものを，" + SEL4, right, [(t, w, "連立方程式の解き方・解の意味の誤解") for t, w in ws],
              f"理由：{right}", d=4, p=8,
              ap="等式の性質，連立方程式の解の意味（両方の式を同時に満たす），問題の条件に戻って考える。",
              steps=["説明されている操作や結論が何を目的としているかを考える。", "等式の性質・解の意味と照らし合わせる。", "結論につながる理由を選ぶ。"],
              alt=["具体的な数で操作を行い，選んだ理由が成り立つかを確かめる。"],
              pc=[("解の意味や等式の性質を理解している", 4), ("結論につながる理由を選んでいる", 4)],
              pit=["「必ず」「いつも」のような言い切りの文を確かめずに選ぶ。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

LINES4 = ["1行目", "2行目", "3行目", "4行目"]


@gen("error_correction", 4, ["common_error", "computation"])
def d_elim_lines(r):
    x0, y0 = nz(r, -5, 5), nz(r, -5, 5)
    a, d = r.randint(2, 5), r.randint(2, 5)
    b, e = nz(r, -5, 5), nz(r, -5, 5)
    assert a != d and a * e - b * d != 0 and abs(a * e - b * d) > 0
    c, f = a * x0 + b * y0, d * x0 + e * y0
    # x を消去：上×d − 下×a
    B1, C1 = b * d, c * d
    B2, C2 = e * a, f * a
    assert B1 != B2
    where = r.choice([0, 1, 2])
    l1 = f"上の式を ${d}$ 倍：${eq(a * d, B1, C1)}$"
    l2 = f"下の式を ${a}$ 倍：${eq(a * d, B2, C2)}$"
    yy = Fr(C1 - C2, B1 - B2)
    l3 = f"ひくと ${term(B1 - B2, 'y', True)}={C1 - C2}$，$y={ftex(yy)}$"
    xx = Fr(c - b * yy, a)
    l4 = f"$y={ftex(yy)}$ を上の式に代入して $x={ftex(xx)}$"
    if where == 0:
        l1 = f"上の式を ${d}$ 倍：${eq(a * d, B1, c)}$"
        wy = Fr(c - C2, B1 - B2)
        l3 = f"ひくと ${term(B1 - B2, 'y', True)}={c - C2}$，$y={ftex(wy)}$"
        l4 = f"$y={ftex(wy)}$ を上の式に代入して $x={ftex(Fr(c - b * wy, a))}$"
        step, etype, tempt = "1行目（右辺を何倍かし忘れた）", "calculation", "左辺の係数をそろえることに気をとられ，右辺にもかけることを忘れやすい。"
    elif where == 1:
        l2 = f"下の式を ${a}$ 倍：${eq(a * d, e * a, f)}$"
        wy = Fr(C1 - f, B1 - B2)
        l3 = f"ひくと ${term(B1 - B2, 'y', True)}={C1 - f}$，$y={ftex(wy)}$"
        l4 = f"$y={ftex(wy)}$ を上の式に代入して $x={ftex(Fr(c - b * wy, a))}$"
        step, etype, tempt = "2行目（右辺を何倍かし忘れた）", "calculation", "左辺の係数をそろえることに気をとられ，右辺にもかけることを忘れやすい。"
    else:
        wB = B1 + B2
        assert wB != 0
        wy = Fr(C1 - C2, wB)
        l3 = f"ひくと ${term(wB, 'y', True)}={C1 - C2}$，$y={ftex(wy)}$"
        l4 = f"$y={ftex(wy)}$ を上の式に代入して $x={ftex(Fr(c - b * wy, a))}$"
        step, etype, tempt = "3行目（$y$ の項のひき算の符号）", "sign", "式どうしをひくとき，負の係数をひく計算で符号を誤りやすい。"
    sol = "\n".join(f"{i + 1}行目　{t}" for i, t in enumerate([l1, l2, l3, l4]))
    ok = {0: "1行目は両辺を正しく何倍かしている。", 1: "2行目は両辺を正しく何倍かしている。", 2: "3行目は2つの式を正しくひいている。", 3: "4行目は前の行の値を正しく代入している。"}
    why = {LINES4[i]: (ok[i], "誤りの箇所の見落とし") for i in range(4) if i != where}
    fix = pair(x0, y0)
    s = system(eq(a, b, c), eq(d, e, f))
    return mc(f"〔問題〕連立方程式 {s} を解きなさい。\n〔Kさんの解答〕\n{sol}\nKさんの解答で，誤りが最初に生じた行として最も適するものを，" + SEL4,
              LINES4, f"誤りが最初に生じたのは{LINES4[where]}。正しい解は {fix}。", d=3, p=6, keep=True, ai=where, why=why,
              err=dict(sol=sol, step=step, type=etype, tempt=tempt, fix=fix),
              ap="各行を自分で計算し直して比べる。何倍かするときは両辺のすべての項にかけ，ひくときは各項の符号に注意する。",
              steps=[f"上の式を ${d}$ 倍：${eq(a * d, B1, C1)}$。", f"下の式を ${a}$ 倍：${eq(a * d, B2, C2)}$。", f"ひくと ${term(B1 - B2, 'y', True)}={C1 - C2}$，$y={y0}$。", f"代入して $x={x0}$。"],
              alt=["Kさんの答えをもとの2つの式に代入すると，一方が成り立たないことから誤りに気づける。"],
              pc=[("誤りの行を正しく指摘している", 3), ("正しい解を求めている", 3)],
              pit=["右辺を何倍かし忘れる。", "負の係数のひき算で符号を誤る。"],
              chk=(f"solve([{a}*x+({b})*y-({c}),{d}*x+({e})*y-({f})],[x,y])", f"{{x:{x0},y:{y0}}}", None, "intermediate"))


@gen("error_correction", 3, ["common_error", "condition_check"])
def d_subst(r):
    x0, y0 = nz(r, -5, 5), nz(r, -5, 5)
    m = nz(r, -3, 3)
    n = y0 - m * x0
    assert n != 0
    a, b = nz(r, -5, 5), r.choice([-5, -4, -3, -2, 2, 3, 4, 5])
    assert a + b * m != 0
    c = a * x0 + b * y0
    rhs = term(m, "x", True) + term(n, "")
    wrong_l = f"{term(a, 'x', True)}{term(b * m, 'x')}{term(n, '')}={c}"
    wx = Fr(c - n, a + b * m)
    assert wx != x0
    sol = f"${wrong_l}$\n${term(a + b * m, 'x', True)}={ftex(c - n)}$\n$x={ftex(wx)}$"
    right = f"$y$ に $({rhs})$ を代入するとき，かっこをつけずに ${b}$ を ${term(m, 'x', True)}$ にだけかけ，定数項 ${n}$ にかけ忘れている。"
    fix = pair(x0, y0)
    cands = [("Kさんの解答に誤りはない。", f"Kさんの $x$ の値は，もとの連立方程式の解 {fix} と一致しない。", "確かめ不足"),
             ("代入法ではなく，必ず加減法で解かなければならない。", "代入法で解いてよい。誤りの原因はかっこのつけ忘れである。", "解き方の選択の誤解"),
             ("代入する前に，1つ目の式の両辺を2倍しなければならない。", "その必要はない。$y=\\cdots$ の形のまま代入できる。", "手順の誤解"),
             ("移項するときに，$x$ の項の符号を変え忘れている。", "Kさんの移項は正しい。誤りは最初の代入の部分にある。", "誤りの箇所の見誤り")]
    return MC(f"〔問題〕連立方程式 {system(f'y={rhs}', eq(a, b, c))} を解きなさい。\n〔Kさんの解答（途中まで）〕\n{sol}\nKさんの解答の誤りを説明したものとして最も適するものを，" + SEL4,
              right, cands, f"正しくは ${term(a, 'x', True)}{term(b, '')}({rhs})={c}$ と代入し，解は {fix}。", d=3, p=6,
              err=dict(sol=sol, step="代入の部分（かっこのつけ忘れ）", type="notation", tempt="式を「そのまま書き写す」と，係数が式全体にかかることを忘れやすい。", fix=fix),
              ap="代入するときは，代入する式全体にかっこをつけ，係数をかっこ内のすべての項にかける。",
              steps=[f"正しい代入：${term(a, 'x', True)}{term(b, '')}({rhs})={c}$。", f"かっこをはずす：${term(a, 'x', True)}{term(b * m, 'x')}{term(b * n, '')}={c}$。", f"解いて $x={x0}$，$y={y0}$。"],
              alt=["求めた $x$ から $y$ を計算し，2つ目の式に代入して成り立つかを確かめる。"],
              pc=[("誤りの原因を正しく指摘している", 3), ("正しい解を求めている", 3)],
              pit=["かっこをつけずに代入する。"],
              chk=(f"solve([y-({m})*x-({n}),{a}*x+({b})*y-({c})],[x,y])", f"{{x:{x0},y:{y0}}}", None, "intermediate"))


@gen("error_correction", 3, ["common_error", "application"])
def d_word(r):
    kind = r.choice(["pct", "unit", "pct"])
    if kind == "pct":
        x0, y0 = r.randint(5, 15) * 20, r.randint(5, 15) * 20
        p, q = r.choice([5, 10, 15, 20]), r.choice([5, 10, 15, 20])
        N = x0 + y0
        D = (p * x0 - q * y0) // 100
        assert D != 0
        txt = f"〔問題〕ある中学校の昨年の生徒数は男子と女子を合わせて {N} 人だった。今年は昨年と比べて男子が {p}％増え，女子が {q}％減ったので，全体では {abs(D)} 人{'増えた' if D > 0 else '減った'}。昨年の男子と女子の人数を求めなさい。"
        sol = f"昨年の男子を $x$ 人，女子を $y$ 人とすると\n$\\begin{{cases}}x+y={N}\\\\ \\dfrac{{{p}}}{{100}}x+\\dfrac{{{q}}}{{100}}y={D}\\end{{cases}}$"
        right = f"女子は {q}％減ったので，減った人数は $-\\dfrac{{{q}}}{{100}}y$ と表すべきなのに，増えた場合と同じ $+\\dfrac{{{q}}}{{100}}y$ としている。"
        fix = f"$\\begin{{cases}}x+y={N}\\\\ \\dfrac{{{p}}}{{100}}x-\\dfrac{{{q}}}{{100}}y={D}\\end{{cases}}$"
        step, etype, tempt = "2つ目の式（減少の符号）", "sign", "「〜％」をそのまま加えてしまい，増加と減少で符号を変えることを忘れやすい。"
        cands = [("Kさんの式に誤りはない。", "女子は減っているので，その分は全体の増減に負の数として加わる。", "確かめ不足"),
                 (f"1つ目の式は，今年の人数の合計 ${N + D}$ を使うべきである。", "$x,\\ y$ は昨年の人数なので，1つ目の式は昨年の合計でよい。", "文字の意味の取り違え"),
                 (f"{p}％ は $\\dfrac{{{p}}}{{10}}$ と表すべきである。", f"{p}％ は $\\dfrac{{{p}}}{{100}}$ である。", "百分率の誤解"),
                 ("右辺の増えた人数（減った人数）は，昨年の合計にかけるべきである。", "右辺は全体の増減の人数そのものでよい。", "式の意味の誤解")]
    else:
        v1, v2 = r.choice([(4, 12), (3, 9), (4, 8), (5, 15)])
        t1, t2 = r.choice([30, 60, 90, 120]), r.choice([30, 60, 90])
        Dv = Fr(v1 * t1 + v2 * t2, 60)
        D = dec(Dv)
        assert D is not None and ("." not in D or len(D.split(".")[1]) <= 1)
        Tm = t1 + t2
        txt = f"〔問題〕{D} km はなれた地点まで，はじめは時速 {v1} km で歩き，途中から時速 {v2} km で走ったところ，全体で {Tm} 分かかった。歩いた道のりと走った道のりを求めなさい。"
        sol = f"歩いた道のりを $x$ km，走った道のりを $y$ km とすると\n$\\begin{{cases}}x+y={D}\\\\ \\dfrac{{x}}{{{v1}}}+\\dfrac{{y}}{{{v2}}}={Tm}\\end{{cases}}$"
        right = f"速さが時速（km/時）なので時間の単位は「時間」であるのに，右辺を {Tm} 分のまま使っている。右辺は $\\dfrac{{{Tm}}}{{60}}$ 時間にする必要がある。"
        fix = f"$\\begin{{cases}}x+y={D}\\\\ \\dfrac{{x}}{{{v1}}}+\\dfrac{{y}}{{{v2}}}={ftex(Fr(Tm, 60))}\\end{{cases}}$"
        step, etype, tempt = "2つ目の式（時間の単位）", "unit", "問題文に出てくる数をそのまま式に入れ，単位をそろえることを忘れやすい。"
        cands = [("Kさんの式に誤りはない。", "時速と分が混ざっており，単位がそろっていない。", "確かめ不足"),
                 (f"時間の式は ${v1}x+{v2}y={Tm}$ とすべきである。", "時間は 道のり÷速さ で表す。道のり×速さ は時間ではない。", "速さ・時間・道のりの関係の誤解"),
                 (f"1つ目の式の右辺は ${dec(Dv * 1000)}$ にすべきである。", "$x,\\ y$ を km で表しているので，1つ目の式は km のままでよい。", "単位の誤解"),
                 ("2つの式を加えて1つの式にすべきである。", "2つの関係は別々の式で表す。加えて1つにすると解が決まらない。", "連立方程式の意味の誤解")]
    return MC(f"{txt}\n〔Kさんがつくった連立方程式〕\n{sol}\nKさんがつくった連立方程式の誤りを説明したものとして最も適するものを，" + SEL4,
              right, cands, f"正しい連立方程式は {fix}。", d=3, p=6,
              err=dict(sol=sol, step=step, type=etype, tempt=tempt, fix=fix),
              ap="文字が表す量（昨年の人数か今年の人数か，km か m か，時間か分か）を確かめ，式の両辺の意味と単位がそろっているかを調べる。",
              steps=["文字が何を表しているかを確認する。", "それぞれの式の左辺と右辺が同じ量（同じ単位）を表しているかを調べる。", f"正しくは {fix}。"],
              alt=["正しい答えを求めて問題文の条件にあてはめ，Kさんの式では成り立たないことを確かめる。"],
              pc=[("誤りの原因を正しく指摘している", 3), ("正しい連立方程式をつくっている", 3)],
              pit=["減少を $+$ で表す。", "時速と分を混ぜて式をつくる。"])


GENERATORS = [a_check_sol, a_elim, a_subst, a_mark,
              b_frac_dec, b_abc, b_param, b_word,
              c_word_hard, c_graph, c_reason,
              d_elim_lines, d_subst, d_word]

GENERATORS = [_robust(g) for g in GENERATORS]
