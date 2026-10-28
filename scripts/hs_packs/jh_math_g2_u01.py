"""単元パック：中学2年 式の計算（神奈川県公立高校入試形式）。"""
import math
import re
import unicodedata
from fractions import Fraction as Fr

from banks._common import mc, num
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem, tp)

UNIT_ID = "JH-MATH-G2-U01"

PREREQUISITES = [
    ("JH-MATH-G1-U02", "文字式の表し方と一次式の加減ができること。同類項をまとめる・分配法則でかっこをはずす計算の土台になる。"),
    ("JH-MATH-G1-U01", "正の数・負の数の四則計算と累乗ができること。係数の計算や $(-2x)^3$ のような累乗の符号の判断に使う。"),
    ("JH-MATH-G1-U03", "等式の性質を使って一次方程式を解けること。等式の変形は、方程式を解く手順と同じ考え方で行う。"),
]
EXTENSIONS = [
    ("JH-MATH-G2-U02", "多項式の加減と等式の変形を使って、連立方程式を加減法・代入法で解く。"),
    ("JH-MATH-G2-U03", "等式の変形で $ax+by=c$ を $y$ について解き、一次関数のグラフとして読む。"),
    ("JH-MATH-G3-U01", "単項式と多項式の乗法を広げて、式の展開・因数分解へ進む。"),
    ("HS-MATH1-U01", "高校の数と式で、多項式の展開・因数分解や式の値の計算を発展させる。"),
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


def MARK(stem, v, e, expr, **kw):
    v = Fr(v)
    assert v >= 0
    if v.denominator == 1:
        n = int(v)
        return num(stem, str(n), e, mark=("int", n), chk=(expr, str(n), None, "answer"), **kw)
    p, q = v.numerator, v.denominator
    return num(stem, f"${ftex(v)}$", e, mark=("frac", p, q), chk=(expr, f"Rational({p},{q})", None, "answer"), **kw)


SEL4 = "次の1〜4の中から1つ選び，その番号を答えなさい。"
CALC = "次の計算をした結果として正しいものを，" + SEL4
VARS = [("x", "y"), ("a", "b")]


def nz(r, lo, hi):
    while True:
        v = r.randint(lo, hi)
        if v:
            return v


# --- 多項式：{(xの指数, yの指数): 係数} ---------------------------------

def P(*terms):
    d = {}
    for c, e in terms:
        d[e] = d.get(e, 0) + Fr(c)
    return {k: v for k, v in d.items() if v != 0}


def padd(p, q, k=1):
    d = dict(p)
    for e, c in q.items():
        d[e] = d.get(e, 0) + k * c
    return {e: c for e, c in d.items() if c != 0}


def pscale(p, k):
    return {e: c * k for e, c in p.items() if c * k != 0}


def _vpart(e, V):
    out = ""
    for v, n in zip(V, e):
        if n == 1:
            out += v
        elif n > 1:
            out += f"{v}^{n}"
    return out


def _order(p):
    return sorted(p, key=lambda e: (-sum(e), -e[0]))


def ptex(p, V, keep_order=None):
    if not p:
        return "0"
    out = []
    for e in (keep_order or _order(p)):
        if e not in p:
            continue
        c = p[e]
        vp = _vpart(e, V)
        m = abs(c)
        if vp and m == 1:
            cs = ""
        elif m.denominator != 1:
            cs = f"\\dfrac{{{m.numerator}}}{{{m.denominator}}}"
        else:
            cs = str(m.numerator)
        sign = "-" if c < 0 else ("+" if out else "")
        out.append(sign + cs + vp)
    return "".join(out)


def ppy(p, V):
    if not p:
        return "0"
    parts = []
    for e, c in p.items():
        t = f"({fpy(c)})"
        for v, n in zip(V, e):
            if n:
                t += f"*{v}**{n}"
        parts.append(t)
    return "+".join(parts)


def peval(p, vals):
    return sum(c * Fr(vals[0]) ** e[0] * Fr(vals[1]) ** e[1] for e, c in p.items())


def mtex(c, e, V):
    """単項式（指数が負でもよい）の LaTeX。"""
    c = Fr(c)
    nume = tuple(max(0, n) for n in e)
    dene = tuple(max(0, -n) for n in e)
    num_v, den_v = _vpart(nume, V), _vpart(dene, V)
    s = "-" if c < 0 else ""
    m = abs(c)
    if not den_v:
        return s + ptex({nume: m}, V)
    top = (str(m.numerator) if (m.numerator != 1 or not num_v) else "") + num_v
    bot = (str(m.denominator) if m.denominator != 1 else "") + den_v
    return f"{s}\\dfrac{{{top}}}{{{bot}}}"


def mpy(c, e, V):
    t = f"({fpy(c)})"
    for v, n in zip(V, e):
        if n:
            t += f"*{v}**({n})"
    return t


def mono_in(c, e, V, paren_neg=True):
    """式の中に書く単項式（負ならかっこ）。"""
    t = mtex(c, e, V)
    return f"\\left({t}\\right)" if (paren_neg and Fr(c) < 0) else t


def lin(r, V, const=False, lo=-9, hi=9):
    a, b = nz(r, lo, hi), nz(r, lo, hi)
    terms = [(a, (1, 0)), (b, (0, 1))]
    if const:
        terms.append((nz(r, lo, hi), (0, 0)))
    return P(*terms)


def paren(p, V):
    return f"({ptex(p, V)})"


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
    goals=["単項式・多項式・項・係数・次数の意味を理解し，多項式の加法・減法を同類項をまとめて計算できる。",
           "単項式の乗法・除法を，係数どうし・文字どうしに分けて正しく計算でき，式の値を工夫して求められる。",
           "等式を目的の文字について解くことができ，文字式を使って数の性質を説明できる。"],
    duration=100,
    readiness=["分配法則 $a(b+c)=ab+ac$ を使ってかっこをはずせる（1年の文字式）。",
               "同類項をまとめて一次式の加法・減法ができる。",
               "正の数・負の数の乗法・除法と累乗の符号を正しく判断できる。",
               "等式の性質（両辺に同じ数を加える・ひく・かける・わる）を使える。"],
    flow=[("導入：カレンダーの数の性質", 10, "カレンダーで縦に並ぶ3つの数の和がいつも3の倍数になる理由を問う"),
          ("単項式と多項式・次数", 10, "用語の確認（項・係数・次数）"),
          ("多項式の加法・減法", 20, "同類項をまとめる，ひく式のかっこのはずし方，分数をふくむ式（例題1）"),
          ("単項式の乗法・除法", 20, "係数と文字に分けて計算する，除法は逆数をかける（例題2）"),
          ("等式の変形", 15, "目的の文字について解く（例題3）"),
          ("文字式による説明", 15, "整数の表し方と説明の書き方（導出）"),
          ("まとめと確認", 10, "確認問題と問題プリントの指示")],
    sections=[
        intro("in1", "カレンダーの数のふしぎ",
              "カレンダーで縦に並んだ3つの数（たとえば 5，12，19）の和を求めると $36$ になる。ほかの場所でも，和はいつも3の倍数になる。いくつか例を調べるだけでは「いつも」とはいえない。文字式を使えば，どの場所でも成り立つことを説明できる。この単元では，そのための式の計算を身につける。",
              bullets=["真ん中の数を $n$ とすると，3つの数は $n-7,\\ n,\\ n+7$ と表せる。", "和は $(n-7)+n+(n+7)=3n$ となり，3の倍数であることがわかる。"],
              points=[tp("まず生徒にいくつか例を計算させ，「いつも成り立つ」と言い切るには何が足りないかを考えさせる。", ask="10個の例で成り立てば，いつも成り立つといえるか。", expect="いえない。すべての場合を表す文字式が必要。", timing="導入の5分")]),
        definition("df1", "単項式・多項式と次数",
                   "数や文字をかけ合わせただけの式を単項式，単項式の和の形で表された式を多項式という。多項式の1つ1つの単項式を項という。",
                   formula="$$3x^2y\\ \\text{の次数は}\\ 2+1=3,\\qquad 4a^2-3ab+5\\ \\text{は2次式}$$",
                   conditions=["単項式の次数：かけ合わされている文字の個数。",
                               "多項式の次数：各項の次数のうちで最も大きいもの。",
                               "同類項：文字の部分が同じ項。$3xy$ と $-5xy$ は同類項だが，$x^2y$ と $xy^2$ は同類項ではない。"],
                   points=[tp("$x^2$ と $2x$ が同類項でないことを，$x=3$ を代入して値を比べさせて確認する。", ask="$x^2+2x$ は $3x^3$ や $3x^2$ にまとめられるか。", expect="まとめられない。文字の部分がちがう。", caution="次数のちがう項をまとめる誤りが多い。")]),
        theorem("th1", "多項式の加法・減法と単項式の乗法・除法",
                "$$-(a-b)=-a+b,\\qquad A\\div B=A\\times\\dfrac{1}{B},\\qquad x^m\\times x^n=x^{m+n}$$",
                ["ひく式は，かっこをはずすときにすべての項の符号を変える。",
                 "単項式の乗法は，係数の積に文字の積をかける。",
                 "単項式の除法は，わる式の逆数をかける乗法になおすか，分数の形にして約分する。",
                 "乗法と除法の混じった式は，1つの分数の形にまとめてから約分するとよい。"],
                body="どの計算も，1年で学んだ分配法則と，数の乗法・除法の決まりを文字の部分にまで広げたものである。",
                proof=["$x^2\\times x^3=(x\\times x)\\times(x\\times x\\times x)$ なので，$x$ を $2+3=5$ 個かけた $x^5$ になる。",
                       "$-(a-b)$ は $(-1)\\times(a-b)$ であり，分配法則から $-a+b$ となる。",
                       "$6x^2y\\div3x=\\dfrac{6\\times x\\times x\\times y}{3\\times x}=2xy$ のように，分数にして共通な文字を約分できる。"],
                points=[tp("除法で $\\dfrac{2}{3}x$ でわるときは，逆数が $\\dfrac{3}{2x}$ であり $\\dfrac{3}{2}x$ ではないことを強調する。", caution="逆数を $\\dfrac{3}{2}x$ とする誤りが多い。", timing="除法の説明の直後"),
                        tp("累乗の符号：$(-2x)^3=-8x^3$，$-2x^3$ との区別を確認する。", ask="$(-2x)^2$ と $-2x^2$ はどうちがうか。", expect="前者は $4x^2$，後者は $-2x^2$。")]),
        derivation("dv1", "文字式で整数の性質を説明する",
                   ["［例］2つの奇数の和は偶数になることを説明する。",
                    "$m,\\ n$ を整数とすると，2つの奇数は $2m+1,\\ 2n+1$ と表せる（2つの奇数は同じとは限らないので別の文字を使う）。",
                    "和は $(2m+1)+(2n+1)=2m+2n+2=2(m+n+1)$。",
                    "$m+n+1$ は整数なので，$2(m+n+1)$ は偶数である。",
                    "したがって，2つの奇数の和は偶数である。"],
                   body="説明は「文字で表す → 計算する → $2\\times$（整数）の形にする → 結論」の順に書く。",
                   points=[tp("「$m+n+1$ は整数なので」の一文を書き落とさないよう指導する。この一文があって初めて偶数と言える。", ask="なぜ $2(m+n+1)$ は偶数と言えるのか。", expect="$m+n+1$ が整数だから。"),
                           tp("2つの奇数を $2n+1,\\ 2n+1$ と同じ文字で表すと，同じ奇数の場合しか説明できないことに気づかせる。", caution="同じ文字を使う誤りが多い。")]),
        example("ex1", "例題1　分数をふくむ多項式の減法",
                "$\\dfrac{3x+y}{2}-\\dfrac{x-2y}{3}$ を計算しなさい。",
                ["通分する：$\\dfrac{3(3x+y)-2(x-2y)}{6}$。", "分子のかっこをはずす：$\\dfrac{9x+3y-2x+4y}{6}$。", "同類項をまとめる：$\\dfrac{7x+7y}{6}$。"],
                "$\\dfrac{7x+7y}{6}$",
                thinking="分子をかっこでくくってから通分し，ひく式の符号に注意する。",
                points=[tp("方程式ではないので，分母をはらって $9x+3y-2x+4y$ のように答えてはいけないことを確認する。", caution="方程式の「分母をはらう」と混同しやすい。")],
                misconceptions=[("$-2(x-2y)$ を $-2x-4y$ とする", "$-2\\times(-2y)=+4y$。ひく式はすべての項の符号が変わる"),
                                ("答えを $7x+7y$ とする", "式の計算では分母を消せない。$\\dfrac{7x+7y}{6}$ のまま答える")]),
        example("ex2", "例題2　乗法と除法の混じった計算",
                "$6a^2b\\div\\left(-\\dfrac{3}{2}ab^2\\right)\\times b^3$ を計算しなさい。",
                ["除法を逆数の乗法になおす：$6a^2b\\times\\left(-\\dfrac{2}{3ab^2}\\right)\\times b^3$。", "符号は負が1つなので $-$。",
                 "1つの分数にする：$-\\dfrac{6\\times2\\times a^2\\times b\\times b^3}{3\\times a\\times b^2}$。", "約分して $-4ab^2$。"],
                "$-4ab^2$",
                thinking="まず符号を決め，次に係数，最後に文字を約分する。",
                points=[tp("わる式の逆数は，係数だけでなく文字も分母に移ることを確認する。")]),
        example("ex3", "例題3　等式の変形",
                "等式 $3x-2y=6$ を $y$ について解きなさい。",
                ["$3x$ を移項する：$-2y=-3x+6$。", "両辺を $-2$ でわる：$y=\\dfrac{3}{2}x-3$。"],
                "$y=\\dfrac{3}{2}x-3$",
                thinking="解きたい文字以外を「数」とみて，一次方程式と同じ手順で $y=\\cdots$ の形にする。",
                points=[tp("両辺を $-2$ でわるとき，右辺のすべての項をわることを強調する。", caution="$-3x$ だけをわり，$6$ をわり忘れる誤りが多い。")],
                misconceptions=[("$y=\\dfrac{3}{2}x+6$ とする", "右辺の $6$ も $-2$ でわる必要がある")]),
        board("bd1", "板書案",
              [("① 加法・減法", ["項・係数・次数", "同類項：文字の部分が同じ", "$-(a-b)=-a+b$", "分数：通分 → 分子のかっこ → まとめる"]),
               ("② 乗法・除法", ["係数どうし・文字どうし", "$\\div B$ は $\\times\\dfrac{1}{B}$", "符号 → 係数 → 文字の順", "例2　$-4ab^2$"]),
               ("③ 変形と説明", ["目的の文字について解く", "右辺のすべての項をわる", "偶数 $2n$，奇数 $2n+1$", "結論：$2\\times$（整数）"])],
              points=[tp("③の説明の型（文字で表す → 計算 → 整数×の形 → 結論）は，枠で囲んで単元を通して残す。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("減法では，ひく式にかっこをつけてから計算させると符号の誤りが減る。", ask="$(2x+3y)-(x-y)$ の $-y$ はかっこをはずすと何になるか。", expect="$+y$。"),
               tp("式の値は，先に式を簡単にしてから代入すると計算が楽になることを体験させる。", timing="乗法・除法の後"),
               tp("文字式による説明では，最後に「したがって〜である」と結論を書くことを必ず求める。"),
               tp("等式の変形は，解きたい文字を左辺に残し，それ以外を右辺に集める手順を口に出して確認させる。")],
              misconceptions=[("$2x^2+3x=5x^3$ とする", "$x^2$ と $x$ は同類項ではないのでまとめられない"),
                              ("$8x^2\\div\\dfrac{2}{3}x$ を $8x^2\\times\\dfrac{3}{2}x$ とする", "$\\dfrac{2}{3}x=\\dfrac{2x}{3}$ の逆数は $\\dfrac{3}{2x}$"),
                              ("連続する2つの整数を $n,\\ m$ と表す", "連続する整数は $n,\\ n+1$ と1つの文字で表す")]),
        summary("sm1", "まとめ",
                ["同類項だけをまとめる。ひく式はすべての項の符号を変える。", "単項式の乗除は「符号 → 係数 → 文字」。除法は逆数の乗法に。",
                 "等式の変形は一次方程式と同じ手順。右辺のすべての項をわる。", "整数の性質は「文字で表す → 計算 → 整数×の形 → 結論」で説明する。"]),
        check("ck1", "確認問題",
              [("$(4a-3b)-(a-5b)$ を計算しなさい。", "$3a+2b$"),
               ("$12x^2y\\div(-4xy)$ を計算しなさい。", "$-3x$"),
               ("等式 $\\ell=2(a+b)$ を $a$ について解きなさい。", "$a=\\dfrac{\\ell}{2}-b$")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

@gen("basic_check", 4, ["concept", "computation"])
def a_degree(r):
    V = r.choice(VARS)
    kind = r.choice(["mono", "poly", "poly", "terms"])
    if kind == "mono":
        c = nz(r, -9, 9)
        e = (r.randint(1, 4), r.randint(1, 3))
        d = sum(e)
        return MARK(f"単項式 ${mtex(c, e, V)}$ の次数を求めなさい。", d,
                    f"かけ合わされている文字は ${V[0]}$ が ${e[0]}$ 個，${V[1]}$ が ${e[1]}$ 個で，合計 ${d}$ 個。次数は ${d}$。", f"{e[0]}+{e[1]}", d=1, p=2,
                    ap="単項式の次数は，かけ合わされている文字の個数。係数は関係ない。",
                    steps=[f"${V[0]}$ の個数：${e[0]}$。", f"${V[1]}$ の個数：${e[1]}$。", f"次数：${e[0]}+{e[1]}={d}$。"],
                    alt=[f"${mtex(c, e, V)}$ を ${abs(c)}\\times " + "\\times ".join([V[0]] * e[0] + [V[1]] * e[1]) + "$ のようにかけ算の形で書き，文字の個数を数える。"],
                    pc=[("文字の個数を正しく数えている", 1), ("次数を正しく答えている", 1)],
                    pit=["係数を次数にふくめてしまう。", "1つの文字の指数だけを答える。"])
    if kind == "poly":
        es = r.sample([(2, 1), (1, 2), (3, 0), (2, 0), (1, 1), (0, 2), (1, 0), (0, 1), (3, 1), (2, 2), (0, 3)], 3)
        p = P(*[(nz(r, -9, 9), e) for e in es], (nz(r, -9, 9), (0, 0)))
        d = max(sum(e) for e in p)
        return MARK(f"多項式 ${ptex(p, V)}$ の次数を求めなさい。", d,
                    f"各項の次数のうち最も大きいものは ${d}$ なので，この多項式は ${d}$ 次式。", f"Max({','.join(str(sum(e)) for e in p)})", d=2, p=2,
                    ap="多項式の次数は，各項の次数のうちで最も大きいもの。",
                    steps=["各項の次数：" + "，".join(f"${ptex({e: c}, V)}$ は ${sum(e)}$" for e, c in p.items()) + "。", f"最も大きいのは ${d}$。"],
                    alt=["項ごとに文字の個数を書き出して比べる。"],
                    pc=[("各項の次数を求めている", 1), ("最大のものを答えている", 1)],
                    pit=["各項の次数をすべて加えてしまう。", "最初の項の次数を答えてしまう。"])
    es = r.sample([(2, 1), (1, 2), (2, 0), (1, 1), (0, 2), (1, 0), (0, 1)], 2)
    cs = [nz(r, -9, 9) for _ in es] + [nz(r, -9, 9)]
    p = P(*zip(cs, es + [(0, 0)]))
    order = es + [(0, 0)]
    terms = [ptex({e: p[e]}, V) for e in order]
    pos = [ptex({e: abs(p[e])}, V) for e in order]
    right = "，".join(f"${t}$" for t in terms)
    cands = [("，".join(f"${t}$" for t in pos), "ひき算の記号「$-$」も項の符号にふくめる。負の項の符号を落としている。", "項の符号の見落とし"),
             ("，".join(f"${t}$" for t in terms[:2]), "数だけの項（定数項）も項である。", "定数項の見落とし"),
             ("，".join(f"${ptex({e: 1}, V)}$" if e != (0, 0) else f"${p[e]}$" for e in order), "係数を除いた文字の部分だけを書いている。", "項と文字の部分の混同")]
    return MC(f"多項式 ${ptex(p, V, order)}$ の項をすべて書き出したものとして正しいものを，" + SEL4, right, cands,
              f"${ptex(p, V, order)}=" + "+".join(f"({t})" for t in terms) + f"$ なので，項は {right}。", d=1,
              ap="多項式を単項式の和の形 $(\\ )+(\\ )+(\\ )$ に書き直すと，項が見える。",
              steps=["ひき算を負の数のたし算になおす。", "和の形で並んだ単項式が項である。", f"項は {right}。"],
              alt=["各項の符号を含めて書き，足し合わせるともとの式になるかを確かめる。"],
              pc=[("和の形に直している", 1), ("符号をふくめて正しく選んでいる", 1)],
              pit=["負の項の符号を落とす。", "定数項を項として数えない。"])


@gen("basic_check", 5, ["computation"])
def a_addsub(r):
    V = r.choice(VARS)
    kind = r.choice(["lin", "lin", "const", "quad"])
    if kind == "quad":
        p1 = P((nz(r, -6, 6), (2, 0)), (nz(r, -9, 9), (1, 0)), (nz(r, -9, 9), (0, 0)))
        p2 = P((nz(r, -6, 6), (2, 0)), (nz(r, -9, 9), (1, 0)), (nz(r, -9, 9), (0, 0)))
        V = (V[0], "y")
    else:
        p1 = lin(r, V, kind == "const")
        p2 = lin(r, V, kind == "const")
    op = r.choice([1, -1, -1])
    ans = padd(p1, p2, op)
    assert len(ans) >= 2
    keys = list(p2)
    first = keys[0]
    half = padd(p1, {e: (-c if e == first else c) for e, c in p2.items()}) if op == -1 else padd(p1, {e: (c if e == first else -c) for e, c in p2.items()})
    cands = [(f"${ptex(padd(p1, p2, -op), V)}$", "ひく式とたす式を取り違えている（符号の処理が逆）。", "加法と減法の取り違え"),
             (f"${ptex(half, V)}$", "かっこをはずすとき，最初の項の符号しか変えていない（または変えるべきでない項の符号を変えている）。", "かっこのはずし方の誤り"),
             (f"${ptex(pscale(ans, -1), V)}$", "すべての項の符号が逆になっている。", "符号の誤り"),
             (f"${ptex({e: (-c if e == _order(ans)[-1] else c) for e, c in ans.items()}, V)}$", "最後の項の符号の計算を誤っている。", "符号の誤り")]
    opstr = "+" if op == 1 else "-"
    return MC(f"${paren(p1, V)}{opstr}{paren(p2, V)}$ を計算した結果として正しいものを，" + SEL4, f"${ptex(ans, V)}$", cands,
              f"かっこをはずして同類項をまとめると ${ptex(ans, V)}$。", d=1,
              ap="かっこをはずしてから，同類項（文字の部分が同じ項）どうしをまとめる。ひく式はすべての項の符号を変える。",
              steps=[f"かっこをはずす：${ptex(p1, V)}" + "".join(("+" if op * c > 0 else "-") + ptex({e: abs(c)}, V) for e, c in p2.items()) + "$。", "同類項をまとめる。", f"答え：${ptex(ans, V)}$。"],
              alt=["縦書きの筆算で同類項を縦にそろえて計算して確かめる。"],
              pc=[("かっこを正しくはずしている", 1), ("同類項を正しくまとめている", 1)],
              pit=["ひく式の2番目以降の項の符号を変え忘れる。"],
              chk=(f"({ppy(p1, V)}){opstr}({ppy(p2, V)})", ppy(ans, V), None, "intermediate"))


def rand_mono(r, V, cmax=6, emax=2):
    return Fr(nz(r, -cmax, cmax)), (r.randint(0, emax), r.randint(0, emax))


@gen("basic_check", 4, ["computation"])
def a_mul(r):
    V = r.choice(VARS)
    kind = r.choice(["mm", "sq", "sq"])
    c1, e1 = Fr(nz(r, -5, 5)), (r.randint(1, 2), r.randint(0, 2))
    c2, e2 = Fr(nz(r, -6, 6)), (r.randint(0, 2), r.randint(1, 2))
    if kind == "sq":
        c = c1 ** 2 * c2
        e = (2 * e1[0] + e2[0], 2 * e1[1] + e2[1])
        expr = f"\\left({mtex(c1, e1, V)}\\right)^2\\times {mono_in(c2, e2, V)}"
        cands = [(f"${mtex(c1 * 2 * c2, e, V)}$", "2乗を「2倍」と考えて，係数を2倍している。", "累乗と乗法の混同"),
                 (f"${mtex(c1 * c2, e, V)}$", "かっこの中の係数を2乗していない。", "累乗の範囲の誤り"),
                 (f"${mtex(-c, e, V)}$", "符号を誤っている。2乗した数は正になる。", "符号の誤り"),
                 (f"${mtex(c, (e1[0] * 2 * max(e2[0], 1), e[1]), V)}$", "指数を加えるところでかけている。", "指数法則の誤り")]
        py = f"({mpy(c1, e1, V)})**2*({mpy(c2, e2, V)})"
    else:
        c = c1 * c2
        e = (e1[0] + e2[0], e1[1] + e2[1])
        expr = f"{mtex(c1, e1, V)}\\times {mono_in(c2, e2, V)}"
        cands = [(f"${mtex(-c, e, V)}$", "符号を誤っている。", "符号の誤り"),
                 (f"${mtex(c1 + c2, e, V)}$", "係数どうしをかけずに加えている。", "乗法と加法の混同"),
                 (f"${mtex(c, (e1[0] * max(e2[0], 1), e1[1] * max(e2[1], 1)), V)}$", "同じ文字の指数を加えずにかけている。", "指数法則の誤り"),
                 (f"${mtex(c, (max(e1[0], e2[0]), max(e1[1], e2[1])), V)}$", "同じ文字の個数を数え落としている。", "文字の積の誤り")]
        py = f"({mpy(c1, e1, V)})*({mpy(c2, e2, V)})"
    return MC(f"${expr}$ を計算した結果として正しいものを，" + SEL4, f"${mtex(c, e, V)}$", cands,
              f"係数は ${ftex(c)}$，文字は ${_vpart(e, V)}$ で，${mtex(c, e, V)}$。", d=2,
              ap="単項式の乗法は，係数どうしの積と文字どうしの積に分けて計算する。同じ文字の積は個数（指数）を加える。",
              steps=["符号を決める。", f"係数：${ftex(c)}$。", f"文字：${_vpart(e, V)}$。", f"答え：${mtex(c, e, V)}$。"],
              alt=["文字をすべて $x\\times x\\times\\cdots$ のように書き並べて数え，確かめる。"],
              pc=[("係数を正しく求めている", 1), ("文字の部分を正しく求めている", 1)],
              pit=["$(-3x)^2$ の係数を $-9$ や $-6$ にしてしまう。"],
              chk=(py, mpy(c, e, V), None, "intermediate"))


@gen("basic_check", 4, ["computation"])
def a_div(r):
    V = r.choice(VARS)
    q = Fr(nz(r, -6, 6))
    qe = (r.randint(0, 2), r.randint(0, 2))
    b = Fr(nz(r, -5, 5))
    be = (r.randint(1, 2), r.randint(0, 1))
    a = q * b
    ae = (qe[0] + be[0], qe[1] + be[1])
    kind = r.choice(["d", "d3"])
    if kind == "d":
        expr = f"{mtex(a, ae, V)}\\div {mono_in(b, be, V)}"
        c, e = q, qe
        py = f"({mpy(a, ae, V)})/({mpy(b, be, V)})"
        cands = [(f"${mtex(-c, e, V)}$", "符号を誤っている。", "符号の誤り"),
                 (f"${mtex(a * b, (ae[0] + be[0], ae[1] + be[1]), V)}$", "わり算をかけ算として計算している。", "除法と乗法の取り違え"),
                 (f"${mtex(c, (ae[0], ae[1]), V)}$", "係数だけをわり，文字をわっていない。", "文字の約分忘れ"),
                 (f"${mtex(1 / c, (-e[0], -e[1]), V)}$", "わられる式とわる式を逆にしている。", "除法の順序の誤り")]
    else:
        m = Fr(nz(r, -4, 4))
        me = (r.randint(0, 1), r.randint(1, 2))
        expr = f"{mtex(a, ae, V)}\\div {mono_in(b, be, V)}\\times {mono_in(m, me, V)}"
        c, e = q * m, (qe[0] + me[0], qe[1] + me[1])
        py = f"({mpy(a, ae, V)})/({mpy(b, be, V)})*({mpy(m, me, V)})"
        wc = a / (b * m)
        we = (ae[0] - be[0] - me[0], ae[1] - be[1] - me[1])
        cands = [(f"${mtex(wc, we, V)}$", "わる式とかける式をまとめて，わる式のように扱っている（左から順に計算していない）。", "計算の順序の誤り"),
                 (f"${mtex(-c, e, V)}$", "負の数の個数を数え誤り，符号を誤っている。", "符号の誤り"),
                 (f"${mtex(c, (qe[0], qe[1]), V)}$", "最後にかける単項式の文字をかけ忘れている。", "文字のかけ忘れ"),
                 (f"${mtex(a * m / b * -1, e, V)}$", "符号を誤っている。", "符号の誤り")]
    return MC(f"${expr}$ を計算した結果として正しいものを，" + SEL4, f"${mtex(c, e, V)}$", cands,
              f"1つの分数の形にして約分すると ${mtex(c, e, V)}$。", d=2,
              ap="除法はわる式の逆数をかける乗法になおすか，分数の形にして約分する。先に符号を決めるとよい。",
              steps=["符号を決める（負の数の個数を数える）。", "わる式を分母に，かける式を分子において1つの分数にする。", f"係数と文字を約分して ${mtex(c, e, V)}$。"],
              alt=["答えにわる式をかけて（かける式でわって），もとの式にもどるかを確かめる。"],
              pc=[("符号を正しく決めている", 1), ("係数・文字を正しく約分している", 1)],
              pit=["乗法と除法が混じった式を，右から計算してしまう。"],
              chk=(py, mpy(c, e, V), None, "intermediate"))


@gen("basic_check", 3, ["computation"])
def a_dist(r):
    V = r.choice(VARS)
    k, m = nz(r, 2, 5), nz(r, 2, 5)
    p1, p2 = lin(r, V, lo=-6, hi=6), lin(r, V, lo=-6, hi=6)
    ans = padd(pscale(p1, k), pscale(p2, m), -1)
    assert len(ans) == 2
    e0, e1 = (1, 0), (0, 1)
    w1 = padd(pscale(p1, k), {e0: -m * p2[e0], e1: m * p2[e1]})
    w2 = padd(pscale(p1, k), pscale(p2, m))
    w3 = padd(pscale(p1, k), {e0: -m * p2[e0], e1: -p2[e1]})
    cands = [(f"${ptex(w1, V)}$", f"$-{m}$ を2番目のかっこの第2項にかけるとき，符号を変えていない。", "分配法則の符号の誤り"),
             (f"${ptex(w2, V)}$", "ひき算をたし算として計算している。", "減法の符号の誤り"),
             (f"${ptex(w3, V)}$", f"$-{m}$ を2番目のかっこの第2項にかけ忘れている。", "分配法則のかけ忘れ"),
             (f"${ptex(pscale(ans, -1), V)}$", "すべての符号が逆になっている。", "符号の誤り")]
    return MC(f"${k}{paren(p1, V)}-{m}{paren(p2, V)}$ を計算した結果として正しいものを，" + SEL4, f"${ptex(ans, V)}$", cands,
              f"分配法則でかっこをはずすと ${ptex(pscale(p1, k), V)}" + "".join(("+" if -m * c > 0 else "-") + ptex({e: abs(m * c)}, V) for e, c in p2.items()) + f"$。まとめて ${ptex(ans, V)}$。", d=2,
              ap="分配法則でかっこをはずす。$-{m}$ は2番目のかっこのすべての項にかける。".replace("{m}", str(m)),
              steps=[f"${k}{paren(p1, V)}={ptex(pscale(p1, k), V)}$。", f"$-{m}{paren(p2, V)}={ptex(pscale(p2, -m), V)}$。", f"同類項をまとめて ${ptex(ans, V)}$。"],
              alt=[f"${V[0]}=1,\\ {V[1]}=1$ などを代入して，もとの式と答えの値が一致するかを確かめる。"],
              pc=[("かっこを正しくはずしている", 1), ("同類項を正しくまとめている", 1)],
              pit=["負の数をかけるとき，2番目の項の符号を変え忘れる。"],
              chk=(f"{k}*({ppy(p1, V)})-{m}*({ppy(p2, V)})", ppy(ans, V), None, "intermediate"))


# ======================================================================
# B 標準演習
# ======================================================================

PQ = [(2, 3), (3, 2), (3, 4), (4, 3), (2, 5), (5, 2), (3, 5), (5, 3), (4, 5), (5, 4), (2, 7), (7, 2), (3, 7), (7, 3), (5, 7), (7, 5), (7, 4), (4, 7)]


def frac_poly(numer, den, V):
    """分子 numer（多項式）/ den を約分した LaTeX。"""
    g = den
    for c in numer.values():
        g = math.gcd(g, int(c))
    n2 = pscale(numer, Fr(1, g))
    d2 = den // g
    if d2 == 1:
        return ptex(n2, V)
    lead = n2[_order(n2)[0]]
    if lead < 0 and all(c < 0 for c in n2.values()):
        return f"-\\dfrac{{{ptex(pscale(n2, -1), V)}}}{{{d2}}}"
    return f"\\dfrac{{{ptex(n2, V)}}}{{{d2}}}"


@gen("standard_practice", 5, ["computation", "condition_check"])
def b_frac(r):
    V = r.choice(VARS)
    p, q = r.choice(PQ)
    A, B = lin(r, V, lo=-7, hi=7), lin(r, V, lo=-7, hi=7)
    op = r.choice([-1, -1, 1])
    numer = padd(pscale(A, q), pscale(B, p), op)
    assert len(numer) == 2
    den = p * q
    right = f"${frac_poly(numer, den, V)}$"
    e1 = (0, 1)
    wsign = padd(pscale(A, q), {e: (p * c if e == e1 else -p * c) if op == -1 else (-p * c if e == e1 else p * c) for e, c in B.items()})
    wnum = numer
    wcross = padd(pscale(A, p), pscale(B, q), op)
    wden = padd(A, B, op)
    cands = [(f"${frac_poly(wsign, den, V)}$" if len(wsign) == 2 else None, "通分した後，ひく式の分子のかっこをはずすとき，2番目の項の符号を変えていない。", "かっこのはずし方の誤り"),
             (f"${ptex(wnum, V)}$", "方程式のように分母をはらってしまっている。式の計算では分母を消すことはできない。", "方程式と式の計算の混同"),
             (f"${frac_poly(wcross, den, V)}$" if len(wcross) == 2 else None, "通分するときに，分子にかける数を取り違えている。", "通分の誤り"),
             (f"${frac_poly(wden, p + q, V)}$" if len(wden) == 2 else None, "分子どうし・分母どうしをそのまま加減している。", "分数の加減の誤り")]
    opstr = "-" if op == -1 else "+"
    return MC(f"$\\dfrac{{{ptex(A, V)}}}{{{p}}}{opstr}\\dfrac{{{ptex(B, V)}}}{{{q}}}$ を計算した結果として正しいものを，" + SEL4, right, cands,
              f"通分して $\\dfrac{{{q}({ptex(A, V)}){opstr}{p}({ptex(B, V)})}}{{{den}}}=\\dfrac{{{ptex(numer, V)}}}{{{den}}}$。", d=3, p=4,
              ap="分母の最小公倍数で通分し，分子をかっこでくくってからかっこをはずす。式の計算なので分母は残る。",
              steps=[f"通分：$\\dfrac{{{q}({ptex(A, V)}){opstr}{p}({ptex(B, V)})}}{{{den}}}$。", f"分子のかっこをはずす：$\\dfrac{{{ptex(pscale(A, q), V)}{ptex(pscale(B, op * p), V) if ptex(pscale(B, op * p), V).startswith('-') else '+' + ptex(pscale(B, op * p), V)}}}{{{den}}}$。",
                     f"同類項をまとめて {right}。"],
              alt=[f"それぞれを $\\dfrac{{1}}{{{p}}}({ptex(A, V)})$ のように係数が分数の式とみて，${V[0]}$ の係数と ${V[1]}$ の係数を別々に計算してもよい。"],
              pc=[("正しく通分している", 1), ("分子のかっこを正しくはずしている", 2), ("同類項をまとめている", 1)],
              pit=["分母をはらって答えてしまう。", "ひく式の2番目の項の符号を変え忘れる。"],
              chk=(f"({ppy(A, V)})/{p}{opstr}({ppy(B, V)})/{q}", f"({ppy(numer, V)})/{den}", None, "intermediate"))


@gen("standard_practice", 4, ["computation", "condition_check"])
def b_value(r):
    V = r.choice(VARS)
    kind = r.choice(["lin", "mono"])
    xv = nz(r, -4, 4)
    yv = r.choice([nz(r, -4, 4), Fr(1, r.choice([2, 3])) * r.choice([1, -1])])
    if kind == "lin":
        k, m = nz(r, 2, 5), nz(r, 2, 4)
        p1, p2 = lin(r, V, lo=-5, hi=5), lin(r, V, lo=-5, hi=5)
        simp = padd(pscale(p1, k), pscale(p2, m), -1)
        assert len(simp) == 2
        expr = f"{k}{paren(p1, V)}-{m}{paren(p2, V)}"
        v = peval(simp, (xv, yv))
        wrong = [peval(padd(pscale(p1, k), pscale(p2, m)), (xv, yv)), peval(padd(pscale(p1, k), {e: (-m * c if e == (1, 0) else m * c) for e, c in p2.items()}), (xv, yv)), -v, peval(simp, (yv, xv))]
        wwhy = ["ひき算をたし算として計算した値である。", "2番目のかっこの第2項の符号を変え忘れた値である。", "符号を誤っている。", f"${V[0]}$ と ${V[1]}$ の値を入れかえて代入している。"]
        simp_t = ptex(simp, V)
        py = f"{k}*({ppy(p1, V)})-{m}*({ppy(p2, V)})"
    else:
        a = Fr(nz(r, -6, 6)) * r.choice([2, 3, 4])
        ae = (r.randint(2, 3), r.randint(1, 2))
        b = Fr(nz(r, -4, 4))
        be = (1, r.randint(0, 1))
        c, e = a / b, (ae[0] - be[0], ae[1] - be[1])
        expr = f"{mtex(a, ae, V)}\\div {mono_in(b, be, V)}"
        v = c * Fr(xv) ** e[0] * Fr(yv) ** e[1]
        wrong = [-v, c * Fr(yv) ** e[0] * Fr(xv) ** e[1], a * b * Fr(xv) ** (ae[0] + be[0]) * Fr(yv) ** (ae[1] + be[1]), v * 2]
        wwhy = ["符号を誤っている。", f"${V[0]}$ と ${V[1]}$ の値を入れかえて代入している。", "わり算をかけ算として計算した値である。", "係数の約分を誤っている。"]
        simp_t = mtex(c, e, V)
        py = f"({mpy(a, ae, V)})/({mpy(b, be, V)})"
    vals = f"${V[0]}={ftex(xv)},\\ {V[1]}={ftex(yv)}$"
    stem = f"{vals} のとき，${expr}$ の値を求めなさい。"
    common = dict(ap="式をできるだけ簡単にしてから代入すると，計算が楽になり誤りも減る。負の数はかっこをつけて代入する。",
                  steps=[f"式を簡単にする：${simp_t}$。", f"{vals} を代入する。", f"値は ${ftex(v)}$。"],
                  alt=["簡単にする前の式に直接代入して計算し，同じ値になるかを確かめる（計算は大変になる）。"],
                  pc=[("式を正しく簡単にしている", 2), ("正しく代入して値を求めている", 2)],
                  pit=["負の数をかっこをつけずに代入して符号を誤る。", "2乗の計算で符号を誤る。"])
    e_ = f"式を簡単にすると ${simp_t}$。これに代入して ${ftex(v)}$。"
    sub = py
    for var, val in zip(V, (xv, yv)):
        sub = re.sub(rf"\b{var}\b", f"({fpy(val)})", sub)
    if v >= 0:
        return MARK(stem + ("答えが分数のときは，それ以上約分できない形で答えること。" if Fr(v).denominator != 1 else ""), v, e_, sub, d=3, p=4, **common)
    cands = [(f"${ftex(w)}$", y, "式の値の計算の誤り") for w, y in zip(wrong, wwhy) if w != v]
    return MC(stem.replace("の値を求めなさい。", "の値として正しいものを，") + SEL4, f"${ftex(v)}$", cands, e_, d=3, p=4,
              chk=(sub, fpy(v), None, "intermediate"), **common)


SOLVE = [
    ("三角形の面積を表す等式 $S=\\dfrac{1}{2}ah$", "h", "h=\\dfrac{2S}{a}",
     [("h=\\dfrac{S}{2a}", "両辺に2をかけるべきところを2でわっている。"), ("h=\\dfrac{a}{2S}", "分母と分子を逆にしている。"), ("h=2S-a", "$a$ でわるべきところを $a$ をひいている。")]),
    ("円の周の長さを表す等式 $\\ell=2\\pi r$", "r", "r=\\dfrac{\\ell}{2\\pi}",
     [("r=\\dfrac{2\\pi}{\\ell}", "分母と分子を逆にしている。"), ("r=\\ell-2\\pi", "わるべきところをひいている。"), ("r=2\\pi\\ell", "わるべきところをかけている。")]),
    ("長方形の周の長さを表す等式 $\\ell=2(a+b)$", "a", "a=\\dfrac{\\ell}{2}-b",
     [("a=\\dfrac{\\ell-b}{2}", "$b$ も2でわってしまっている。先に両辺を2でわってから $b$ を移項する。"), ("a=2\\ell-b", "両辺を2でわるべきところを2倍している。"), ("a=\\dfrac{\\ell}{2}+b", "$b$ を移項するときに符号を変えていない。")]),
    ("2つの数 $a,\\ b$ の平均 $m$ を表す等式 $m=\\dfrac{a+b}{2}$", "b", "b=2m-a",
     [("b=\\dfrac{m}{2}-a", "両辺に2をかけるべきところを2でわっている。"), ("b=2m+a", "$a$ を移項するときに符号を変えていない。"), ("b=2(m-a)", "$a$ にも2をかけてしまっている。")]),
    ("台形の面積を表す等式 $S=\\dfrac{1}{2}(a+b)h$", "a", "a=\\dfrac{2S}{h}-b",
     [("a=\\dfrac{2S-b}{h}", "$b$ も $h$ でわってしまっている。"), ("a=\\dfrac{S}{2h}-b", "両辺に2をかけるべきところを2でわっている。"), ("a=\\dfrac{2S}{h}+b", "$b$ を移項するときに符号を変えていない。")]),
    ("直方体の体積を表す等式 $V=abc$", "c", "c=\\dfrac{V}{ab}",
     [("c=V-ab", "わるべきところをひいている。"), ("c=\\dfrac{ab}{V}", "分母と分子を逆にしている。"), ("c=Vab", "わるべきところをかけている。")]),
    ("円錐の体積を表す等式 $V=\\dfrac{1}{3}\\pi r^2h$", "h", "h=\\dfrac{3V}{\\pi r^2}",
     [("h=\\dfrac{V}{3\\pi r^2}", "両辺に3をかけるべきところを3でわっている。"), ("h=\\dfrac{\\pi r^2}{3V}", "分母と分子を逆にしている。"), ("h=3V-\\pi r^2", "わるべきところをひいている。")]),
    ("等式 $x=\\dfrac{2y-z}{3}$", "z", "z=2y-3x",
     [("z=3x-2y", "$-z$ を移項したときの符号の処理を誤っている。"), ("z=2y-\\dfrac{x}{3}", "両辺に3をかけるべきところを3でわっている。"), ("z=\\dfrac{2y-x}{3}", "$x$ と $z$ を入れかえただけで，変形していない。")]),
    ("速さ・時間・道のりの関係を表す等式 $\\ell=vt+5$", "t", "t=\\dfrac{\\ell-5}{v}",
     [("t=\\dfrac{\\ell}{v}-5", "$5$ を先に移項せずに $v$ でわり，$5$ をわり忘れている。"), ("t=\\dfrac{\\ell+5}{v}", "$5$ を移項するときに符号を変えていない。"), ("t=\\dfrac{v}{\\ell-5}", "分母と分子を逆にしている。")]),
]


@gen("standard_practice", 5, ["condition_check", "computation"])
def b_solve_for(r):
    if r.random() < 0.45:
        txt, var, right, ws = r.choice(SOLVE)
        return MC(f"{txt}を ${var}$ について解いたものとして正しいものを，" + SEL4, f"${right}$", [(f"${t}$", w, "等式の変形の手順の誤り") for t, w in ws],
                  f"等式の性質を使って ${var}$ だけを左辺に残すと ${right}$。", d=3, p=4,
                  ap=f"${var}$ 以外の文字を数とみて，一次方程式を解くときと同じ手順（移項・両辺に同じ数をかける・わる）で ${var}=\\cdots$ の形にする。",
                  steps=[f"${var}$ をふくむ項が左辺にくるように両辺を入れかえる。", "分数があれば両辺に分母をかけ，不要な項を移項する。", f"${var}$ の係数で両辺をわって ${right}$。"],
                  alt=["具体的な数（たとえば図形の辺の長さ）を代入して，もとの式と変形した式で同じ結果になるかを確かめる。"],
                  pc=[("変形の手順を正しく選んでいる", 2), ("正しい式を選んでいる", 2)],
                  pit=["両辺をわるとき，一部の項だけをわる。", "移項で符号を変え忘れる。"])
    V = r.choice(VARS)
    a, b = nz(r, -9, 9), nz(r, -9, 9)
    assert abs(b) != 1
    c = nz(r, -12, 12)
    tgt = r.choice([1, 0])
    xv, yv = V
    lhs = ptex(P((a, (1, 0)), (b, (0, 1))), V)
    if tgt == 1:
        sol = P((Fr(-a, b), (1, 0)), (Fr(c, b), (0, 0)))
        w1 = P((Fr(-a, b), (1, 0)), (c, (0, 0)))
        w2 = P((Fr(a, b), (1, 0)), (Fr(c, b), (0, 0)))
        w3 = P((Fr(-a, b), (1, 0)), (Fr(-c, b), (0, 0)))
        solved = yv
        py_sol = f"{fpy(Fr(-a, b))}*{xv}+{fpy(Fr(c, b))}"
    else:
        sol = P((Fr(-b, a), (0, 1)), (Fr(c, a), (0, 0)))
        assert abs(a) != 1
        w1 = P((Fr(-b, a), (0, 1)), (c, (0, 0)))
        w2 = P((Fr(b, a), (0, 1)), (Fr(c, a), (0, 0)))
        w3 = P((Fr(-b, a), (0, 1)), (Fr(-c, a), (0, 0)))
        solved = xv
        py_sol = f"{fpy(Fr(-b, a))}*{yv}+{fpy(Fr(c, a))}"
    coef = b if tgt == 1 else a
    cands = [(f"${solved}={ptex(w1, V)}$", f"両辺を ${coef}$ でわるとき，定数項 ${c}$ をわり忘れている。", "一部の項だけをわる誤り"),
             (f"${solved}={ptex(w2, V)}$", "移項するときに符号を変えていない。", "移項の符号の誤り"),
             (f"${solved}={ptex(w3, V)}$", "定数項の符号を誤っている。", "符号の誤り")]
    other = xv if tgt == 1 else yv
    return MC(f"等式 ${lhs}={c}$ を ${solved}$ について解いたものとして正しいものを，" + SEL4, f"${solved}={ptex(sol, V)}$", cands,
              f"${ptex({(1, 0) if tgt == 0 else (0, 1): coef}, V)}$ 以外の項を移項し，両辺を ${coef}$ でわると ${solved}={ptex(sol, V)}$。", d=3, p=4,
              ap=f"${other}$ を数とみて，${solved}$ についての一次方程式を解くつもりで変形する。",
              steps=[f"${ptex({(1, 0) if tgt == 1 else (0, 1): (a if tgt == 1 else b)}, V)}$ を移項する。", f"両辺を ${coef}$ でわる（右辺のすべての項をわる）。", f"${solved}={ptex(sol, V)}$。"],
              alt=[f"答えの式に ${other}$ の値を1つ代入して ${solved}$ を求め，もとの等式を満たすかを確かめる。"],
              pc=[("正しく移項している", 2), ("右辺のすべての項を係数でわっている", 2)],
              pit=["定数項をわり忘れる。", "移項で符号を変え忘れる。"],
              chk=(f"solve({a}*{xv}+{b}*{yv}-({c}),{solved})", f"[{py_sol}]", None, "intermediate"))


@gen("standard_practice", 3, ["computation"])
def b_mixed(r):
    V = r.choice(VARS)
    kind = r.choice(["cube", "frac"])
    if kind == "cube":
        c1, e1 = Fr(nz(r, -3, 3)), (1, r.randint(0, 1))
        c2, e2 = Fr(nz(r, -6, 6)) * 2, (r.randint(1, 2), r.randint(1, 2))
        c3, e3 = Fr(nz(r, -4, 4)), (r.randint(0, 1), r.randint(1, 2))
        c = c1 ** 3 / c2 * c3
        e = (3 * e1[0] - e2[0] + e3[0], 3 * e1[1] - e2[1] + e3[1])
        expr = f"\\left({mtex(c1, e1, V)}\\right)^3\\div {mono_in(c2, e2, V)}\\times {mono_in(c3, e3, V)}"
        py = f"({mpy(c1, e1, V)})**3/({mpy(c2, e2, V)})*({mpy(c3, e3, V)})"
        cands = [(f"${mtex(3 * c1 / c2 * c3, e, V)}$", "3乗を「3倍」として係数を計算している。", "累乗と乗法の混同"),
                 (f"${mtex(-c, e, V)}$", "符号を誤っている。負の数の3乗は負になる。", "累乗の符号の誤り"),
                 (f"${mtex(c1 ** 3 / (c2 * c3), (3 * e1[0] - e2[0] - e3[0], 3 * e1[1] - e2[1] - e3[1]), V)}$", "最後の単項式もわる式として扱っている。", "計算の順序の誤り"),
                 (f"${mtex(c1 / c2 * c3, e, V)}$", "かっこの中の係数を3乗していない。", "累乗の範囲の誤り")]
    else:
        p1, q1 = r.choice([(2, 3), (3, 4), (4, 9), (5, 6), (3, 8), (2, 5), (9, 4)])
        c1 = Fr(p1, q1) * r.choice([1, -1])
        e1 = (r.randint(1, 3), r.randint(1, 2))
        c2 = Fr(r.choice([1, 2, 3, 4]), r.choice([3, 5, 9, 2])) * r.choice([1, -1])
        assert c2.denominator != 1
        e2 = (r.randint(0, 2), r.randint(1, 2))
        c, e = c1 / c2, (e1[0] - e2[0], e1[1] - e2[1])
        expr = f"{mtex(c1, e1, V)}\\div {mono_in(c2, e2, V)}"
        py = f"({mpy(c1, e1, V)})/({mpy(c2, e2, V)})"
        cands = [(f"${mtex(c1 * c2, e, V)}$", "わる数の係数の逆数をかけるところで，そのままかけている。", "逆数の誤り"),
                 (f"${mtex(c1 / c2, (e1[0] + e2[0], e1[1] + e2[1]), V)}$", "係数は逆数にしたが，文字をわらずにかけている。", "逆数の範囲の誤り（文字も逆数になる）"),
                 (f"${mtex(-c, e, V)}$", "符号を誤っている。", "符号の誤り"),
                 (f"${mtex(c2 / c1, (-e[0], -e[1]), V)}$", "わられる式とわる式を逆にしている。", "除法の順序の誤り")]
    return MC(f"${expr}$ を計算した結果として正しいものを，" + SEL4, f"${mtex(c, e, V)}$", cands,
              f"わる式を逆数にしてかけ，1つの分数にして約分すると ${mtex(c, e, V)}$。", d=3, p=4,
              ap="累乗を先に計算し，除法は逆数の乗法になおして1つの分数にまとめる。符号 → 係数 → 文字の順に決める。",
              steps=["累乗のかっこを先に計算する。" if kind == "cube" else "わる式 $\\dfrac{\\ \\ }{\\ \\ }$ の逆数を考える（係数も文字も逆数になる）。", "1つの分数の形にまとめる。", f"約分して ${mtex(c, e, V)}$。"],
              alt=["答えにわる式をかけて，もとの式（わられる式）にもどるかを確かめる。"],
              pc=[("累乗・逆数を正しく扱っている", 2), ("正しく約分している", 2)],
              pit=["$\\dfrac{2}{3}x$ の逆数を $\\dfrac{3}{2}x$ としてしまう。", "$(-2x)^3$ の符号を $+$ にしてしまう。"],
              chk=(py, mpy(c, e, V), None, "intermediate"))


EXPLAIN = [
    ("連続する3つの整数の和は3の倍数である", "連続する3つの整数のうち最も小さい数を $n$ とすると，3つの整数は $n,\\ n+1,\\ n+2$ と表される。それらの和は（　　）となる。$n+1$ は整数なので，連続する3つの整数の和は3の倍数である。",
     "$3(n+1)$", [("$3n+3$", "計算は正しいが，$3\\times$（整数）の形になっていないので，3の倍数であることが示せない。", "説明の結論の形の誤り"), ("$3n$", "定数の部分 $1+2=3$ を加え忘れている。", "計算の誤り"), ("$3(n+2)$", "定数の部分の計算を誤っている。$3n+3=3(n+1)$。", "計算の誤り")]),
    ("2けたの自然数と，その数の十の位の数と一の位の数を入れかえた数の和は11の倍数である", "もとの自然数の十の位の数を $a$，一の位の数を $b$ とすると，もとの数は $10a+b$，入れかえた数は $10b+a$ と表される。それらの和は（　　）となる。$a+b$ は整数なので，この和は11の倍数である。",
     "$11(a+b)$", [("$11ab$", "和を積と取り違えている。", "計算の誤り"), ("$(a+b)+(b+a)$", "十の位の数を10倍していない。", "位取りの表し方の誤り"), ("$9(a+b)$", "差の場合と取り違えている。", "計算の誤り")]),
    ("2けたの自然数から，その数の十の位の数と一の位の数を入れかえた数をひいた差は9の倍数である", "もとの自然数の十の位の数を $a$，一の位の数を $b$ とすると，もとの数は $10a+b$，入れかえた数は $10b+a$ と表される。それらの差は（　　）となる。$a-b$ は整数なので，この差は9の倍数である。",
     "$9(a-b)$", [("$9(a+b)$", "$-(10b+a)=-10b-a$ の符号を誤っている。", "かっこのはずし方の誤り"), ("$11(a-b)$", "同類項のまとめ方を誤っている。", "計算の誤り"), ("$a-b$", "十の位の数を10倍していない。", "位取りの表し方の誤り")]),
    ("偶数と奇数の和は奇数である", "$m,\\ n$ を整数とすると，偶数は $2m$，奇数は $2n+1$ と表される。それらの和は（　　）となる。$m+n$ は整数なので，偶数と奇数の和は奇数である。",
     "$2(m+n)+1$", [("$2(m+n+1)$", "$+1$ を2でくくってしまっている。これでは偶数の形になる。", "計算の誤り"), ("$2m+2n$", "奇数の $+1$ を落としている。", "奇数の表し方の誤り"), ("$4mn+2m$", "和を積と取り違えている。", "計算の誤り")]),
    ("2つの奇数の和は偶数である", "$m,\\ n$ を整数とすると，2つの奇数は $2m+1,\\ 2n+1$ と表される。それらの和は（　　）となる。$m+n+1$ は整数なので，2つの奇数の和は偶数である。",
     "$2(m+n+1)$", [("$2(m+n)+1$", "定数の部分を $1+1=2$ と計算していない。", "計算の誤り"), ("$2m+2n+2$", "計算は正しいが，$2\\times$（整数）の形になっていないので，偶数であることが示せない。", "説明の結論の形の誤り"), ("$4(m+n)$", "定数の部分を落とし，係数も誤っている。", "計算の誤り")]),
    ("連続する2つの奇数の和は4の倍数である", "$n$ を整数とすると，連続する2つの奇数は $2n+1,\\ 2n+3$ と表される。それらの和は（　　）となる。$n+1$ は整数なので，連続する2つの奇数の和は4の倍数である。",
     "$4(n+1)$", [("$4n+4$", "計算は正しいが，$4\\times$（整数）の形になっていないので，4の倍数であることが示せない。", "説明の結論の形の誤り"), ("$2(2n+2)$", "$2\\times$（整数）の形なので偶数であることしか示せない。", "説明の結論の形の誤り"), ("$4(n+2)$", "定数の部分の計算を誤っている。", "計算の誤り")]),
    ("連続する5つの整数の和は，真ん中の数の5倍である", "連続する5つの整数のうち真ん中の数を $n$ とすると，5つの整数は $n-2,\\ n-1,\\ n,\\ n+1,\\ n+2$ と表される。それらの和は（　　）となる。したがって，連続する5つの整数の和は，真ん中の数の5倍である。",
     "$5n$", [("$5n+10$", "$n-2$ と $n-1$ の負の部分を加えていない。", "計算の誤り"), ("$5(n+2)$", "定数の部分の計算を誤っている。", "計算の誤り"), ("$5n-3$", "負の部分しか加えていない。", "計算の誤り")]),
    ("3けたの自然数で，百の位の数と一の位の数を入れかえた数ともとの数の差は99の倍数である", "もとの数の百の位の数を $a$，十の位の数を $b$，一の位の数を $c$ とすると，もとの数は $100a+10b+c$，入れかえた数は $100c+10b+a$ と表される。（もとの数）−（入れかえた数）は（　　）となる。$a-c$ は整数なので，この差は99の倍数である。",
     "$99(a-c)$", [("$99(a+c)$", "ひく式のかっこをはずすときの符号を誤っている。", "かっこのはずし方の誤り"), ("$99(a-c)+20b$", "十の位の $10b$ どうしが消えることを見落としている。", "計算の誤り"), ("$101(a-c)$", "同類項のまとめ方を誤っている。", "計算の誤り")]),
    ("奇数の2倍に偶数を加えると偶数になる", "$m,\\ n$ を整数とすると，奇数は $2m+1$，偶数は $2n$ と表される。奇数の2倍に偶数を加えた数は（　　）となる。$2m+n+1$ は整数なので，この数は偶数である。",
     "$2(2m+n+1)$", [("$2(2m+n)+1$", "奇数の $+1$ を2倍していない。", "分配法則の誤り"), ("$4m+2n+2$", "計算は正しいが，$2\\times$（整数）の形になっていない。", "説明の結論の形の誤り"), ("$2(m+n+1)$", "奇数を2倍していない。", "計算の誤り")]),
]


@gen("standard_practice", 3, ["written_reasoning", "concept"])
def b_explain_fill(r):
    claim, body, right, ws = r.choice(EXPLAIN)
    return MC(f"Kさんは「{claim}」ことを，次のように説明した。\n〔説明〕{body}\n（　　）にあてはまる式として最も適するものを，" + SEL4, right, ws,
              f"（　　）には {right} が入る。結論の形（倍数を表す形）になるようにくくる。", d=3, p=4,
              ap="式を計算したあと，「何の倍数か」「偶数か奇数か」が読み取れる形（$k\\times$（整数）や $2\\times$（整数）$+1$）にまとめる。",
              steps=["文字で表された数を，問題の指示どおりに加える（ひく）。", "同類項をまとめる。", f"結論が読み取れる形 {right} にくくる。"],
              alt=["文字に具体的な数を代入して，説明の式と実際の和（差）が一致するかを確かめる。"],
              pc=[("正しく計算している", 2), ("結論が読み取れる形を選んでいる", 2)],
              pit=["計算は正しいのに，結論が読み取れる形にくくっていない。"])


# ======================================================================
# C 思考力・記述応用
# ======================================================================

PROOFS = [
    ("連続する3つの偶数の和は6の倍数である",
     "$n$ を整数とすると，連続する3つの偶数は $2n,\\ $ (a) $,\\ 2n+4$ と表される。それらの和は $6n+6=$ (b) となる。(b) の中の $n+1$ は整数なので，連続する3つの偶数の和は6の倍数である。",
     ("$2n+2$", "$6(n+1)$"), [("$2n+1$", "連続する偶数は2ずつ大きくなる。$2n+1$ は奇数である。"), ("$n+2$", "$n+2$ は偶数とは限らない。")], [("$3(2n+2)$", "これでは3の倍数であることしか読み取れない。"), ("$6n+6$", "くくっていないので，6の倍数であることが読み取れない。")]),
    ("2けたの自然数と，その数の十の位の数と一の位の数を入れかえた数の和は11の倍数である",
     "もとの数の十の位の数を $a$，一の位の数を $b$ とすると，もとの数は (a)，入れかえた数は $10b+a$ と表される。和は $11a+11b=$ (b) となる。$a+b$ は整数なので，和は11の倍数である。",
     ("$10a+b$", "$11(a+b)$"), [("$ab$", "$ab$ は $a\\times b$ を表し，2けたの数を表さない。"), ("$a+b$", "十の位の数は10倍する必要がある。")], [("$11ab$", "和の計算を積と取り違えている。"), ("$11a+11b$", "くくっていないので，11の倍数であることが読み取れない。")]),
    ("連続する4つの整数の和は，2でわると1余る数の2倍になる",
     "最も小さい整数を $n$ とすると，4つの整数は $n,\\ n+1,\\ n+2,\\ $ (a) と表される。和は $4n+6=$ (b) となる。$2n+3$ は奇数なので，和は奇数の2倍である。",
     ("$n+3$", "$2(2n+3)$"), [("$n+4$", "連続する整数は1ずつ大きくなる。"), ("$3n$", "$3n$ は $n+2$ の次の整数ではない。")], [("$4(n+1)+2$", "この形では，奇数の2倍であることが読み取りにくい。"), ("$2(2n+6)$", "$4n+6$ を2でくくると $2(2n+3)$ になる。")]),
    ("連続する3つの奇数の和は3の倍数である",
     "$n$ を整数とすると，連続する3つの奇数は $2n-1,\\ $ (a) $,\\ 2n+3$ と表される。それらの和は (b) となる。$2n+1$ は整数なので，連続する3つの奇数の和は3の倍数である。",
     ("$2n+1$", "$3(2n+1)$"), [("$2n$", "$2n$ は偶数を表す。"), ("$2n+2$", "連続する奇数は2ずつ大きくなる。$2n-1$ の次は $2n+1$。")], [("$6n+3$", "くくっていないので，3の倍数であることが読み取れない。"), ("$3(2n+3)$", "定数の部分の計算を誤っている。$-1+1+3=3$。")]),
    ("2けたの自然数から，その数の十の位の数と一の位の数の和をひくと，9の倍数になる",
     "十の位の数を $a$，一の位の数を $b$ とすると，2けたの自然数は $10a+b$ と表される。この数から $a+b$ をひいた差は (a) となり，(b) と表される。$a$ は整数なので，差は9の倍数である。",
     ("$9a$", "$9\\times a$"), [("$9a+2b$", "$-(a+b)=-a-b$ の符号を誤っている。"), ("$11a+2b$", "ひき算をたし算として計算している。")], [("$9\\times(a+b)$", "$b$ は消えるので，$a+b$ は残らない。"), ("$10\\times a$", "差の計算を誤っている。")]),
    ("連続する2つの整数の和は奇数である",
     "$n$ を整数とすると，連続する2つの整数は $n,\\ $ (a) と表される。それらの和は (b) となる。$n$ は整数なので，$2n$ は偶数であり，(b) は奇数である。",
     ("$n+1$", "$2n+1$"), [("$m$", "連続する2つの整数は1つの文字で表せる。別の文字 $m$ では連続することが表せない。"), ("$n+2$", "連続する整数は1ずつ大きくなる。")], [("$2(n+1)$", "$n+(n+1)=2n+1$ であり，$2(n+1)=2n+2$ ではない。"), ("$2n$", "定数の $1$ を加え忘れている。")]),
    ("2けたの自然数から，その数の十の位の数と一の位の数を入れかえた数をひいた差は9の倍数である",
     "もとの数の十の位の数を $a$，一の位の数を $b$ とすると，もとの数は $10a+b$，入れかえた数は (a) と表される。差は $9a-9b=$ (b) となる。$a-b$ は整数なので，差は9の倍数である。",
     ("$10b+a$", "$9(a-b)$"), [("$ba$", "$ba$ は $b\\times a$ を表し，2けたの数を表さない。"), ("$10a+b$", "これはもとの数であり，入れかえた数ではない。")], [("$9(a+b)$", "$9a-9b$ を9でくくると $9(a-b)$ になる。"), ("$9a-9b$", "くくっていないので，9の倍数であることが読み取れない。")]),
    ("偶数と偶数の和は偶数である",
     "$m,\\ n$ を整数とすると，2つの偶数は $2m,\\ $ (a) と表される。それらの和は (b) となる。$m+n$ は整数なので，偶数と偶数の和は偶数である。",
     ("$2n$", "$2(m+n)$"), [("$2m$", "同じ文字を使うと，2つの偶数が等しい場合しか説明できない。"), ("$2n+1$", "$2n+1$ は奇数を表す。")], [("$2mn$", "和を積と取り違えている。"), ("$2m+2n$", "くくっていないので，偶数であることが読み取れない。")]),
    ("5の倍数と10の倍数の和は5の倍数である",
     "$m,\\ n$ を整数とすると，5の倍数は $5m$，10の倍数は (a) と表される。それらの和は (b) となる。$m+2n$ は整数なので，この和は5の倍数である。",
     ("$10n$", "$5(m+2n)$"), [("$10m$", "同じ文字を使うと，5の倍数を2倍した数の場合しか説明できない。"), ("$n+10$", "$n+10$ は10の倍数とは限らない。")], [("$5(m+n)$", "$10n=5\\times2n$ なので，かっこの中は $m+2n$ になる。"), ("$15mn$", "和を積と取り違えている。")]),
]


@gen("thinking_writing", 4, ["written_reasoning", "condition_check"])
def c_proof(r):
    claim, body, (ra, rb), was, wbs = r.choice(PROOFS)
    opts_a = [ra] + [w[0] for w in was]
    opts_b = [rb] + [w[0] for w in wbs]
    combos = [(a, b) for a in opts_a for b in opts_b]
    right = (ra, rb)
    others = [c for c in combos if c != right]
    others.sort(key=lambda c: ((c[0] != ra) + (c[1] != rb), opts_a.index(c[0]), opts_b.index(c[1])))
    pick = others[:5]

    def lab(c):
        return f"(a) {c[0]}　(b) {c[1]}"
    whyA = {w[0]: w[1] for w in was}
    whyB = {w[0]: w[1] for w in wbs}
    why = {}
    for c in pick:
        msg = []
        if c[0] != ra:
            msg.append(f"(a)：{whyA[c[0]]}")
        if c[1] != rb:
            msg.append(f"(b)：{whyB[c[1]]}")
        why[lab(c)] = ("　".join(msg), "文字式による説明の組み立ての誤り")
    return mc(f"Kさんは「{claim}」ことを，次のように説明した。\n〔説明〕{body}\n(a)，(b) にあてはまるものの組み合わせとして最も適するものを，次の1〜6の中から1つ選び，その番号を答えなさい。",
              [lab(right)] + [lab(c) for c in pick], f"(a) は {ra}，(b) は {rb}。", d=4, p=8, why=why,
              ap="(a) は数の表し方（偶数 $2n$，奇数 $2n+1$，2けたの数 $10a+b$ など），(b) は結論が読み取れる形（$k\\times$（整数）など）を考える。",
              steps=["問題の数を文字で正しく表す（(a)）。", "計算して同類項をまとめる。", "結論（〜の倍数・奇数など）が読み取れる形にくくる（(b)）。", f"(a) {ra}，(b) {rb}。"],
              alt=["文字に具体的な数（$n=1,2$ など）を代入して，説明の式が実際の数と一致するかを確かめる。"],
              pc=[("(a) の数の表し方が正しい", 4), ("(b) の結論の形が正しい", 4)],
              pit=["2つの異なる数を同じ文字で表してしまう。", "計算した式をくくらず，結論が読み取れない形のままにする。"])


@gen("thinking_writing", 3, ["computation", "application"])
def c_number(r):
    kind = r.choice(["sum2", "diff3", "cons"])
    if kind == "sum2":
        a, b = r.randint(1, 9), r.randint(1, 9)
        T = 11 * (a + b)
        return MARK(f"2けたの自然数 $A$ と，$A$ の十の位の数と一の位の数を入れかえた2けたの自然数 $B$ がある。$A+B={T}$ のとき，$A$ の十の位の数と一の位の数の和を求めなさい。", a + b,
                    f"十の位を $a$，一の位を $b$ とすると $A+B=(10a+b)+(10b+a)=11(a+b)$。$11(a+b)={T}$ より $a+b={a + b}$。", f"{T}/11", d=4, p=8,
                    ap="2けたの数を $10a+b$ と文字で表し，$A+B$ を文字式で計算すると $11(a+b)$ の形になる。",
                    steps=["$A=10a+b,\\ B=10b+a$ とおく。", "$A+B=11a+11b=11(a+b)$。", f"$11(a+b)={T}$ より $a+b={a + b}$。"],
                    alt=[f"具体的に $A$ をいくつか試して確かめてもよい（たとえば $A={10 * a + b}$ のとき $B={10 * b + a}$）。"],
                    pc=[("2けたの数を文字で表している", 3), ("$11(a+b)$ の形を導いている", 3), ("正しい値を求めている", 2)],
                    pit=["十の位の数を10倍し忘れる。"])
    if kind == "diff3":
        a = r.randint(3, 9)
        c = r.randint(1, a - 1)
        D = 99 * (a - c)
        return MARK(f"3けたの自然数 $A$ の百の位の数と一の位の数を入れかえた数を $B$ とする。$A$ の百の位の数は一の位の数より大きく，$A-B={D}$ である。$A$ の百の位の数と一の位の数の差を求めなさい。", a - c,
                    f"百の位を $a$，十の位を $b$，一の位を $c$ とすると $A-B=(100a+10b+c)-(100c+10b+a)=99(a-c)$。$99(a-c)={D}$ より $a-c={a - c}$。", f"{D}/99", d=4, p=8,
                    ap="3けたの数を $100a+10b+c$ と表し，$A-B$ を計算すると十の位が消えて $99(a-c)$ になる。",
                    steps=["$A=100a+10b+c,\\ B=100c+10b+a$ とおく。", "$A-B=99a-99c=99(a-c)$。", f"$99(a-c)={D}$ より $a-c={a - c}$。"],
                    alt=["具体的な3けたの数で $A-B$ を計算し，99の倍数になることを確かめる。"],
                    pc=[("3けたの数を文字で表している", 3), ("$99(a-c)$ の形を導いている", 3), ("正しい値を求めている", 2)],
                    pit=["ひく式のかっこをはずすときに符号を誤る。"])
    k = r.choice([3, 5, 7, 9])
    S = k * r.randint(5, 60)
    mid = S // k
    first = mid - k // 2
    return MARK(f"連続する ${k}$ つの整数の和が ${S}$ である。このとき，${k}$ つの整数のうち最も小さい数を求めなさい。", first,
                f"真ん中の数を $n$ とすると，和は ${k}n$ となる。${k}n={S}$ より $n={mid}$。最も小さい数は $n-{k // 2}={first}$。", f"{S}/{k}-{k // 2}", d=4, p=8,
                ap="真ん中の数を $n$ とおくと，前後の数が打ち消し合い，和は（個数）$\\times n$ という簡単な形になる。",
                steps=[f"真ん中の数を $n$ とすると，${k}$ つの整数は $n-{k // 2},\\ \\ldots,\\ n,\\ \\ldots,\\ n+{k // 2}$。", f"和は ${k}n$。", f"${k}n={S}$ より $n={mid}$。", f"最も小さい数は ${first}$。"],
                alt=[f"最も小さい数を $m$ とおくと，和は ${k}m+{k * (k - 1) // 2}$。${k}m+{k * (k - 1) // 2}={S}$ を解いても同じ結果になる。"],
                pc=[("整数を文字で表している", 3), ("和を簡単な式にしている", 3), ("正しい値を求めている", 2)],
                pit=["真ん中の数を答えてしまう。"])


@gen("thinking_writing", 3, ["cross_unit", "computation"], rel=["JH-MATH-G1-U06"])
def c_geometry(r):
    kind = r.choice(["cyl", "cone", "box"])
    ks = [Fr(2), Fr(3), Fr(1, 2), Fr(1, 3), Fr(3, 2), Fr(1, 4)]
    p, q = r.choice(ks), r.choice(ks)

    def word(k):
        return f"${ftex(k)}$ 倍"
    if kind in ("cyl", "cone"):
        v = p * p * q
        assert v != 1
        nm = "円柱" if kind == "cyl" else "円錐"
        vol = "\\pi r^2h" if kind == "cyl" else "\\dfrac{1}{3}\\pi r^2h"
        stem = f"底面の半径が $r$，高さが $h$ の{nm}Aがある。底面の半径を{word(p)}，高さを{word(q)}にした{nm}Bの体積は，{nm}Aの体積の何倍か求めなさい。答えが分数のときは，それ以上約分できない形で答えること。"
        e = f"Aの体積は ${vol}$。Bは半径 ${ftex(p)}r$，高さ ${ftex(q)}h$ なので，体積は $\\left({ftex(p)}\\right)^2\\times{ftex(q)}={ftex(v)}$ 倍。"
        st = [f"Aの体積：$V_A={vol}$。", f"Bの体積：半径 ${ftex(p)}r$，高さ ${ftex(q)}h$ を代入すると，$V_A$ の $\\left({ftex(p)}\\right)^2\\times{ftex(q)}$ 倍。", f"${ftex(v)}$ 倍。"]
        expr = f"({fpy(p)})**2*{fpy(q)}"
    else:
        s = r.choice(ks)
        v = p * q * s
        assert v != 1
        stem = f"縦 $a$，横 $b$，高さ $c$ の直方体Aがある。縦を{word(p)}，横を{word(q)}，高さを{word(s)}にした直方体Bの体積は，直方体Aの体積の何倍か求めなさい。答えが分数のときは，それ以上約分できない形で答えること。"
        e = f"Aの体積は $abc$，Bの体積は ${ftex(p)}a\\times{ftex(q)}b\\times{ftex(s)}c={ftex(v)}abc$ なので ${ftex(v)}$ 倍。"
        st = ["Aの体積：$abc$。", f"Bの体積：${ftex(p)}a\\times{ftex(q)}b\\times{ftex(s)}c$。", f"係数どうしをかけて ${ftex(v)}abc$，よって ${ftex(v)}$ 倍。"]
        expr = f"{fpy(p)}*{fpy(q)}*{fpy(s)}"
    return MARK(stem, v, e, expr, d=4, p=8,
                ap="体積を文字式で表し，単項式の乗法で係数だけを比べる（空間図形の体積の公式とのつながり）。",
                steps=st, alt=["$r=1,\\ h=1$ のように具体的な数を代入して体積を計算し，比を求めて確かめる。"],
                pc=[("体積を文字式で表している", 3), ("単項式の乗法を正しく行っている", 3), ("正しい倍率を求めている", 2)],
                pit=["半径を2倍にすると体積も2倍になると考えてしまう（2乗を忘れる）。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

LINES4 = ["1行目", "2行目", "3行目", "4行目"]


@gen("error_correction", 4, ["common_error", "computation"])
def d_frac_lines(r):
    V = r.choice(VARS)
    p, q = r.choice(PQ)
    A, B = lin(r, V, lo=-7, hi=7), lin(r, V, lo=-7, hi=7)
    numer = padd(pscale(A, q), pscale(B, p), -1)
    assert len(numer) == 2 and B[(0, 1)] != 0
    den = p * q
    where = r.choice([1, 2, 3])
    qa, pb = pscale(A, q), pscale(B, -p)
    exp_t = ptex(qa, V) + "".join(("+" if c > 0 else "-") + ptex({e: abs(c)}, V) for e, c in pb.items())
    l1 = f"$=\\dfrac{{{q}({ptex(A, V)})-{p}({ptex(B, V)})}}{{{den}}}$"
    l2 = f"$=\\dfrac{{{exp_t}}}{{{den}}}$"
    l3 = f"$=\\dfrac{{{ptex(numer, V)}}}{{{den}}}$"
    l4 = f"$={frac_poly(numer, den, V)}$" if frac_poly(numer, den, V) != f"\\dfrac{{{ptex(numer, V)}}}{{{den}}}" else None
    if where == 1:
        bad = {e: (-c if e == (0, 1) else c) for e, c in pb.items()}
        wexp = ptex(qa, V) + "".join(("+" if c > 0 else "-") + ptex({e: abs(c)}, V) for e, c in bad.items())
        wn = padd(qa, bad)
        assert len(wn) == 2
        l2 = f"$=\\dfrac{{{wexp}}}{{{den}}}$"
        l3 = f"$=\\dfrac{{{ptex(wn, V)}}}{{{den}}}$"
        l4 = f"$={frac_poly(wn, den, V)}$"
        step, etype, tempt = "2行目（ひく式の2番目の項の符号）", "sign", "かっこの前の $-$ を最初の項にだけかけてしまいやすい。"
    elif where == 2:
        wn = dict(numer)
        k0 = (1, 0)
        wn[k0] = numer[k0] + r.choice([1, -1, 2])
        wn = {e: c for e, c in wn.items() if c}
        assert len(wn) == 2
        l3 = f"$=\\dfrac{{{ptex(wn, V)}}}{{{den}}}$"
        l4 = f"$={frac_poly(wn, den, V)}$"
        step, etype, tempt = "3行目（同類項の計算）", "calculation", "正の数・負の数の加法で計算ミスをしやすい。"
    else:
        l4 = f"$={ptex(numer, V)}$"
        step, etype, tempt = "4行目（分母をはらった）", "concept", "方程式の解き方の「両辺に分母をかける」と混同しやすい。"
    if l4 is None:
        l4 = f"答え　$\\dfrac{{{ptex(numer, V)}}}{{{den}}}$"
        assert where != 3
    if where in (1, 2) and l4 == l3:
        l4 = "答え　$" + l3[2:]
    lines = [l1, l2, l3, l4]
    sol = f"$\\dfrac{{{ptex(A, V)}}}{{{p}}}-\\dfrac{{{ptex(B, V)}}}{{{q}}}$\n" + "\n".join(f"{i + 1}行目　{t}" for i, t in enumerate(lines))
    ok = {0: "1行目は分母の最小公倍数で正しく通分している。", 1: "2行目は分子のかっこを正しくはずしている。", 2: "3行目は同類項を正しくまとめている。", 3: "4行目は正しい。"}
    why = {LINES4[i]: (ok[i], "誤りの箇所の見落とし") for i in range(4) if i != where}
    fix = f"${frac_poly(numer, den, V)}$"
    return mc(f"〔問題〕$\\dfrac{{{ptex(A, V)}}}{{{p}}}-\\dfrac{{{ptex(B, V)}}}{{{q}}}$ を計算しなさい。\n〔Kさんの解答〕\n{sol}\nKさんの解答で，誤りが最初に生じた行として最も適するものを，" + SEL4,
              LINES4, f"誤りが最初に生じたのは{LINES4[where]}。正しい答えは {fix}。", d=3, p=6, keep=True, ai=where, why=why,
              err=dict(sol=sol, step=step, type=etype, tempt=tempt, fix=fix),
              ap="通分 → かっこをはずす → 同類項をまとめる → 約分 の各段階を，自分で計算し直して1行ずつ比べる。",
              steps=[f"通分：$\\dfrac{{{q}({ptex(A, V)})-{p}({ptex(B, V)})}}{{{den}}}$。", f"かっこをはずす：$\\dfrac{{{exp_t}}}{{{den}}}$。", f"まとめる：$\\dfrac{{{ptex(numer, V)}}}{{{den}}}$。", f"答え：{fix}。"],
              alt=[f"${V[0]}=1,\\ {V[1]}=0$ などを代入して，もとの式と各行の値が等しいかを確かめると，誤りの行がわかる。"],
              pc=[("誤りの行を正しく指摘している", 3), ("正しい答えを求めている", 3)],
              pit=["かっこの前の $-$ を最初の項にしかかけない。", "分母をはらってしまう。"],
              chk=(f"({ppy(A, V)})/{p}-({ppy(B, V)})/{q}", f"({ppy(numer, V)})/{den}", None, "intermediate"))


@gen("error_correction", 3, ["common_error", "concept"])
def d_div(r):
    V = r.choice(VARS)
    kind = r.choice(["recip", "order", "power"])
    if kind == "recip":
        n, d = r.choice([(2, 3), (3, 4), (4, 5), (2, 5), (3, 2), (5, 3)])
        c2 = Fr(n, d)
        e2 = (1, 0)
        c1 = Fr(nz(r, 2, 9)) * n
        e1 = (r.randint(2, 3), r.randint(0, 2))
        wc, we = c1 * Fr(d, n), (e1[0] + 1, e1[1])
        c, e = c1 / c2, (e1[0] - 1, e1[1])
        prob = f"{mtex(c1, e1, V)}\\div{mtex(c2, e2, V)}"
        sol = f"${prob}={mtex(c1, e1, V)}\\times\\dfrac{{{d}}}{{{n}}}{V[0]}={mtex(wc, we, V)}$"
        right = f"$\\dfrac{{{n}}}{{{d}}}{V[0]}=\\dfrac{{{n}{V[0]}}}{{{d}}}$ の逆数は $\\dfrac{{{d}}}{{{n}{V[0]}}}$ であるのに，係数だけを逆数にして $\\dfrac{{{d}}}{{{n}}}{V[0]}$ をかけている。"
        step, etype, tempt = "わる式の逆数", "concept", f"$\\dfrac{{{n}}}{{{d}}}{V[0]}$ の形を見て，分数の部分だけを逆数にしやすい。"
        py = f"({mpy(c1, e1, V)})/({mpy(c2, e2, V)})"
    elif kind == "order":
        a = Fr(nz(r, 2, 6)) * 6
        ae = (2, r.randint(1, 2))
        b = Fr(r.choice([2, 3]))
        be = (1, 0)
        m = Fr(r.choice([2, 3]))
        me = (0, 1)
        c, e = a / b * m, (ae[0] - 1, ae[1] + 1)
        wc, we = a / (b * m), (ae[0] - 1, ae[1] - 1)
        prob = f"{mtex(a, ae, V)}\\div{mtex(b, be, V)}\\times{mtex(m, me, V)}"
        sol = f"${prob}={mtex(a, ae, V)}\\div{mtex(b * m, (1, 1), V)}={mtex(wc, we, V)}$"
        right = "乗法と除法の混じった式を，先にかけ算の部分から計算している。左から順に計算する（わる式だけを分母におく）必要がある。"
        step, etype, tempt = "計算の順序", "logic", "かけ算を先にまとめると計算が楽に見えるため，順序の決まりを忘れやすい。"
        py = f"({mpy(a, ae, V)})/({mpy(b, be, V)})*({mpy(m, me, V)})"
    else:
        c1 = Fr(nz(r, 2, 4)) * r.choice([1, -1])
        e1 = (1, r.randint(1, 2))
        c2 = Fr(nz(r, 2, 6))
        e2 = (r.randint(1, 2), 0)
        c, e = c1 ** 2 * c2, (2 + e2[0], 2 * e1[1])
        wc = c1 * 2 * c2
        prob = f"\\left({mtex(c1, e1, V)}\\right)^2\\times{mtex(c2, e2, V)}"
        sol = f"${prob}={mtex(c1 * 2, (2, 2 * e1[1]), V)}\\times{mtex(c2, e2, V)}={mtex(wc, e, V)}$"
        right = f"$\\left({mtex(c1, e1, V)}\\right)^2$ の係数は $({ftex(c1)})^2={ftex(c1 ** 2)}$ であるのに，係数を2倍して ${ftex(c1 * 2)}$ としている。"
        step, etype, tempt = "累乗の係数", "calculation", "指数の2を「2倍」と読みかえてしまいやすい。"
        py = f"({mpy(c1, e1, V)})**2*({mpy(c2, e2, V)})"
    assert (wc, we if kind != "power" else e) != (c, e) or kind == "power"
    fix = f"${mtex(c, e, V)}$"
    cands = [("Kさんの解答に誤りはない。", f"正しい答えは {fix} で，Kさんの答えと一致しない。", "確かめ不足"),
             ("係数どうしを先にわり，文字どうしはかけ合わせるべきである。", "文字も係数と同じように約分する。文字だけかけ合わせるのは誤り。", "単項式の除法の誤解"),
             ("答えの符号を逆にするべきである。", "符号は正しく処理されている。誤りの原因は別にある。", "符号の誤解"),
             ("最後に分母をはらって整数の係数にするべきである。", "式の計算では分母をはらうことはできない。", "方程式との混同")]
    return MC(f"〔問題〕${prob}$ を計算しなさい。\n〔Kさんの解答〕\n{sol}\nKさんの解答の誤りを説明したものとして最も適するものを，" + SEL4,
              right, cands, f"正しくは ${prob}={mtex(c, e, V)}$。", d=3, p=6,
              err=dict(sol=sol, step=step, type=etype, tempt=tempt, fix=fix),
              ap="単項式の乗除は，1つの分数の形にまとめて約分するのが確実。わる式は係数も文字も分母に入る。累乗は係数にもかかる。",
              steps=["わる式を分母に，かける式を分子において1つの分数にする。" if kind != "power" else "先に累乗を計算する（係数も文字も2乗する）。", "符号・係数・文字の順に計算する。", f"正しくは {fix}。"],
              alt=["答えに具体的な数（たとえば $x=1,\\ y=1$ ではなく $x=2,\\ y=3$ など）を代入し，もとの式の値と比べて確かめる。"],
              pc=[("誤りの原因を正しく指摘している", 3), ("正しい答えを求めている", 3)],
              pit=["$\\dfrac{2}{3}x$ の逆数を $\\dfrac{3}{2}x$ とする。", "乗除の混じった式でかけ算を先にする。", "$(3x)^2$ を $6x^2$ とする。"],
              chk=(py, mpy(c, e, V), None, "intermediate"))


@gen("error_correction", 3, ["common_error", "condition_check"])
def d_transform(r):
    V = r.choice(VARS)
    a = nz(r, 2, 6) * r.choice([1, -1])
    b = r.choice([2, 3, 4, 5]) * r.choice([1, -1])
    c = nz(r, -12, 12)
    xv, yv = V
    kind = r.choice(["partial", "sign", "sign2"])
    sol_c = P((Fr(-a, b), (1, 0)), (Fr(c, b), (0, 0)))
    lhs = ptex(P((a, (1, 0)), (b, (0, 1))), V)
    l1 = f"${ptex({(0, 1): b}, V)}={ptex(P((-a, (1, 0)), (c, (0, 0))), V)}$"
    if kind == "partial":
        wrong = P((Fr(-a, b), (1, 0)), (c, (0, 0)))
        sol = f"{l1}\n${yv}={ptex(wrong, V)}$"
        right = f"両辺を ${b}$ でわるとき，右辺の ${ptex({(1, 0): -a}, V)}$ だけをわり，定数項 ${c}$ をわっていない。"
        step, etype, tempt = "両辺をわる部分", "calculation", "文字をふくむ項に目が行き，定数項をわり忘れやすい。"
    elif kind == "sign":
        wrong = P((Fr(a, b), (1, 0)), (Fr(c, b), (0, 0)))
        sol = f"${ptex({(0, 1): b}, V)}={ptex(P((a, (1, 0)), (c, (0, 0))), V)}$\n${yv}={ptex(wrong, V)}$"
        right = f"${ptex({(1, 0): a}, V)}$ を右辺に移項するとき，符号を変えていない。"
        step, etype, tempt = "移項する部分", "sign", "移項を「項を動かすだけ」と考え，符号を変えることを忘れやすい。"
    else:
        wrong = P((Fr(-a, -b), (1, 0)), (Fr(c, -b), (0, 0))) if b < 0 else P((Fr(-a, -b), (1, 0)), (Fr(-c, b), (0, 0)))
        assert wrong != sol_c
        sol = f"{l1}\n${yv}={ptex(wrong, V)}$"
        right = f"両辺を ${b}$ でわるとき，わる数の符号を誤り，右辺のすべての項の符号が逆になっている。"
        step, etype, tempt = "両辺をわる部分", "sign", "負の数でわるときの符号の処理を誤りやすい。"
    assert wrong != sol_c
    fix = f"${yv}={ptex(sol_c, V)}$"
    cands = [("Kさんの解答に誤りはない。", f"正しくは {fix} であり，Kさんの答えと一致しない。", "確かめ不足"),
             (f"等式の変形では，${xv}$ をふくむ項を移項してはいけない。", f"${yv}$ について解くので，${xv}$ をふくむ項は右辺に移項してよい。", "等式の性質の誤解"),
             (f"最後に ${yv}$ の係数を右辺にかけるべきである。", f"${yv}$ の係数でわる（またはその逆数をかける）のが正しい。", "わる操作とかける操作の混同"),
             (f"右辺をすべて ${xv}$ でわるべきである。", f"${xv}$ でわる必要はない。${yv}$ の係数でわる。", "わる数の誤解")]
    if kind != "partial":
        cands.insert(1, (f"両辺を ${b}$ でわるとき，定数項 ${c}$ をわり忘れている。", "定数項はわられている。誤りの原因は別にある。", "誤りの箇所の見誤り"))
    return MC(f"〔問題〕等式 ${lhs}={c}$ を ${yv}$ について解きなさい。\n〔Kさんの解答〕\n{sol}\nKさんの解答の誤りを説明したものとして最も適するものを，" + SEL4,
              right, cands, f"正しくは {fix}。", d=3, p=6,
              err=dict(sol=sol, step=step, type=etype, tempt=tempt, fix=fix),
              ap="等式の変形は一次方程式を解く手順と同じ。移項では符号が変わり，両辺をわるときは右辺のすべての項をわる。",
              steps=[f"${ptex({(1, 0): a}, V)}$ を移項：{l1}。", f"両辺を ${b}$ でわる：{fix}。"],
              alt=[f"${xv}$ に数を1つ代入して，Kさんの答えから求めた ${yv}$ がもとの等式を満たすかを確かめる。"],
              pc=[("誤りの原因を正しく指摘している", 3), ("正しく変形している", 3)],
              pit=["定数項をわり忘れる。", "移項で符号を変え忘れる。"],
              chk=(f"solve({a}*{xv}+({b})*{yv}-({c}),{yv})", f"[{fpy(Fr(-a, b))}*{xv}+{fpy(Fr(c, b))}]", None, "intermediate"))


GENERATORS = [a_degree, a_addsub, a_mul, a_div, a_dist,
              b_frac, b_value, b_solve_for, b_mixed, b_explain_fill,
              c_proof, c_number, c_geometry,
              d_frac_lines, d_div, d_transform]

GENERATORS = [_robust(g) for g in GENERATORS]
