"""単元パック：中学3年 式の展開と因数分解（神奈川県公立高校入試形式）。"""
import re
import unicodedata
from fractions import Fraction as Fr

from banks._common import figure, mc, num
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, proof, summary, theorem, tp)

UNIT_ID = "JH-MATH-G3-U01"

PREREQUISITES = [
    ("JH-MATH-G2-U01", "単項式・多項式の加減と乗除、分配法則。展開はすべて分配法則のくり返しである。文字式による説明（証明）の書き方も使う。"),
    ("JH-MATH-G1-U02", "同類項をまとめる、かっこの前の符号に注意してかっこをはずす、などの一次式の計算。"),
    ("JH-MATH-G1-U01", "正負の数の四則計算と素因数分解。因数分解で「積が q、和が p になる2数」を探すときに使う。"),
]
EXTENSIONS = [
    ("JH-MATH-G3-U03", "因数分解を使って二次方程式を解く（$AB=0$ ならば $A=0$ または $B=0$）。平方の形への変形は解の公式の導出にもつながる。"),
    ("JH-MATH-G3-U02", "乗法公式を根号をふくむ式の計算（$(\\sqrt{a}+\\sqrt{b})^2$ など）に使う。"),
    ("HS-MATH1-U01", "高校の数と式で、3乗の展開・因数分解やたすきがけの因数分解に発展する。"),
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


def MARK(stem, v, e, expr, **kw):
    v = Fr(v)
    assert v >= 0
    if v.denominator == 1:
        n = int(v)
        return num(stem, str(n), e, mark=("int", n), chk=(expr, str(n), None, "answer"), **kw)
    p, q = v.numerator, v.denominator
    return num(stem, f"$\\dfrac{{{p}}}{{{q}}}$", e, mark=("frac", p, q), chk=(expr, f"Rational({p},{q})", None, "answer"), **kw)


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


def nz(r, lo, hi, ex=(0,)):
    return r.choice([v for v in range(lo, hi + 1) if v not in ex])


# ---- 多項式（{(xの次数, yの次数): 係数}） ----

def P(*terms):
    d = {}
    for c, i, j in terms:
        d[(i, j)] = d.get((i, j), 0) + c
    return {k: v for k, v in d.items() if v}


def lin(p, q, y=False):
    """p x + q（y=True なら p x + q y）。"""
    return P((p, 1, 0), (q, 0, 1) if y else (q, 0, 0))


def add(*ps):
    d = {}
    for p in ps:
        for k, v in p.items():
            d[k] = d.get(k, 0) + v
    return {k: v for k, v in d.items() if v}


def sc(p, k):
    return {kk: v * k for kk, v in p.items() if v * k}


def mul(p, q):
    d = {}
    for (i1, j1), a in p.items():
        for (i2, j2), b in q.items():
            d[(i1 + i2, j1 + j2)] = d.get((i1 + i2, j1 + j2), 0) + a * b
    return {k: v for k, v in d.items() if v}


def mono(i, j, V):
    s = ""
    for name, e in ((V[0], i), (V[1], j)):
        if e == 1:
            s += name
        elif e > 1:
            s += f"{name}^{e}"
    return s


def _order(p):
    return sorted(p, key=lambda k: (-(k[0] + k[1]), -k[0]))


def tex(p, V=("x", "y")):
    if not p:
        return "0"
    out = []
    for k in _order(p):
        c = p[k]
        m = mono(*k, V)
        mag = abs(c)
        body = (m if mag == 1 and m else f"{mag}{m}")
        out.append(("-" if c < 0 else ("+" if out else "")) + body)
    return "".join(out)


def terms_tex(ts, V=("x", "y")):
    """同類項をまとめずに並べた式（ts=[(係数, i, j), ...]）。"""
    out = []
    for c, i, j in ts:
        if c == 0:
            continue
        m = mono(i, j, V)
        mag = abs(c)
        body = (m if mag == 1 and m else f"{mag}{m}")
        out.append(("-" if c < 0 else ("+" if out else "")) + body)
    return "".join(out) or "0"


def terms(p):
    return [(p[k], *k) for k in _order(p)]


def py(p, V=("x", "y")):
    if not p:
        return "0"
    parts = []
    for (i, j), c in p.items():
        m = "*".join([V[0]] * i + [V[1]] * j)
        parts.append(f"({c})" + (f"*{m}" if m else ""))
    return "+".join(parts)


def pf(p, V=("x", "y")):
    """かっこつき（項が2つ以上のとき）。"""
    t = tex(p, V)
    return f"({t})" if len(p) > 1 else t


def fac(k, fs, V=("x", "y")):
    """k × Π(多項式^指数) の LaTeX。fs=[(多項式, 指数)]。"""
    s = "" if k == 1 else ("-" if k == -1 else str(k))
    for p, e in fs:
        t = pf(p, V)
        if len(p) == 1 and e == 1:
            t = tex(p, V)
        s += t + (f"^{e}" if e > 1 else "")
    return s


def facpy(k, fs, V=("x", "y")):
    return f"({k})" + "".join(f"*(({py(p, V)})**{e})" for p, e in fs)


def ft(v):
    v = Fr(v)
    if v.denominator == 1:
        return str(v.numerator)
    return ("-" if v < 0 else "") + f"\\dfrac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def D(s):
    return f"${s}$"


VARS = [("x", "y"), ("a", "b")]


# ----------------------------------------------------------------------
# 図（SVG）
# ----------------------------------------------------------------------

def area_fig(a="a", b="b", sq=False):
    """(x+a)(x+b) の面積図。"""
    W, H = 260, 200
    x0, y0, X, A, B = 40, 20, 120, 70, 50 if not sq else 70
    lab = lambda x, y, t, s=13: f'<text x="{x}" y="{y}" text-anchor="middle" font-size="{s}" font-style="italic">{t}</text>'  # noqa: E731
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="serif">']
    o.append(f'<rect x="{x0}" y="{y0}" width="{X + A}" height="{X + B}" fill="#fff" stroke="#000" stroke-width="1.2"/>')
    o.append(f'<line x1="{x0 + X}" y1="{y0}" x2="{x0 + X}" y2="{y0 + X + B}" stroke="#000"/>')
    o.append(f'<line x1="{x0}" y1="{y0 + X}" x2="{x0 + X + A}" y2="{y0 + X}" stroke="#000"/>')
    bb = a if sq else b
    o += [lab(x0 + X / 2, y0 + X / 2 + 5, "x²", 15), lab(x0 + X + A / 2, y0 + X / 2 + 5, f"{a}x"), lab(x0 + X / 2, y0 + X + B / 2 + 5, f"{bb}x"),
          lab(x0 + X + A / 2, y0 + X + B / 2 + 5, f"{a}²" if sq else f"{a}{b}"),
          lab(x0 + X / 2, y0 - 5, "x"), lab(x0 + X + A / 2, y0 - 5, a), lab(x0 - 10, y0 + X / 2 + 4, "x"), lab(x0 - 10, y0 + X + B / 2 + 4, bb)]
    o.append("</svg>")
    return "".join(o)


# ----------------------------------------------------------------------
# 授業プリント
# ----------------------------------------------------------------------

LESSON = lesson(
    goals=["乗法公式を分配法則や面積図から導き，式の展開に使うことができる。",
           "共通因数をくくり出すことや乗法公式の逆を使って，式を因数分解することができる。",
           "展開・因数分解を数の計算のくふうや，整数の性質の証明に活用できる。"],
    duration=100,
    readiness=["分配法則 $a(b+c)=ab+ac$ を使ってかっこをはずせる（1・2年）。", "同類項をまとめ，かっこの前の $-$ に注意して計算できる（1・2年）。",
               "正負の数のかけ算・たし算ができ，ある数を2つの整数の積に分けられる。"],
    flow=[("導入：長方形の面積を2通りに表す", 10, "縦 $x+3$，横 $x+5$ の長方形の面積を，全体と4つの部分の和の2通りで表す"),
          ("多項式の乗法と乗法公式", 25, "$(a+b)(c+d)$ の展開，4つの乗法公式の導出（例題1）"),
          ("因数分解", 30, "共通因数，公式の逆，「積が $q$・和が $p$」の2数の探し方（例題2）"),
          ("式の計算の利用", 25, "数の計算のくふう，整数の性質の証明（例題3）"),
          ("まとめと確認", 10, "確認問題と問題プリントの指示")],
    sections=[
        intro("in1", "面積を2通りに表す",
              "縦が $x+3$，横が $x+5$ の長方形の面積は，そのまま $(x+3)(x+5)$ と表せる。一方，長方形を4つの部分に分けると，$x^2$，$5x$，$3x$，$15$ の和とも表せる。この2つが等しいことから，積の形の式を和の形の式に直す方法（展開）が見えてくる。逆に，和の形の式を積の形に直すことを因数分解という。",
              bullets=["展開：積の形 → 和の形　$(x+3)(x+5)=x^2+8x+15$", "因数分解：和の形 → 積の形　$x^2+8x+15=(x+3)(x+5)$"],
              figure=figure("縦 x+a，横 x+b の長方形を4つに分けた面積図", area_fig()),
              points=[tp("面積図の4つの部分の面積を生徒に言わせ，和の式を板書する。", ask="真ん中の $5x$ と $3x$ はまとめられるか。", expect="同類項なので $8x$ にまとめられる。", timing="導入")]),
        theorem("th1", "乗法公式",
                "$$\\begin{aligned}&(x+a)(x+b)=x^2+(a+b)x+ab\\\\&(x+a)^2=x^2+2ax+a^2\\\\&(x-a)^2=x^2-2ax+a^2\\\\&(x+a)(x-a)=x^2-a^2\\end{aligned}$$",
                ["$a$，$b$ は正の数でも負の数でもよい（$x$ のかわりに $2x$ や $3y$ などの式を入れてもよい）。",
                 "$(x+a)^2$ は $x^2+a^2$ ではない。真ん中の項 $2ax$ を忘れないこと。"],
                proof=["分配法則により，$(x+a)(x+b)=x(x+b)+a(x+b)=x^2+bx+ax+ab=x^2+(a+b)x+ab$。",
                       "この式で $b=a$ とおくと $(x+a)^2=x^2+2ax+a^2$。",
                       "$a$ を $-a$ におきかえると $(x-a)^2=x^2-2ax+a^2$。",
                       "$b=-a$ とおくと，$x$ の係数は $a+(-a)=0$，定数項は $a\\times(-a)=-a^2$ なので $(x+a)(x-a)=x^2-a^2$。"],
                points=[tp("4つの公式が，じつは1つ目の公式 $(x+a)(x+b)$ から導けることを確認させる。", caution="$(x-a)^2$ の定数項を $-a^2$ としてしまう誤りが多い。$(-a)^2=a^2$ を確認する。")]),
        derivation("dv1", "因数分解の考え方（公式の逆）",
                   ["多項式をいくつかの式の積の形に表すことを因数分解といい，積をつくっている1つ1つの式を因数という。",
                    "まず，すべての項に共通な因数（共通因数）があれば，かっこの外にくくり出す：$ma+mb=m(a+b)$。",
                    "$x^2+px+q$ の形なら，積が $q$，和が $p$ になる2つの数 $a$，$b$ を見つけて $(x+a)(x+b)$ とする（公式1の逆）。",
                    "$x^2+2ax+a^2$ は $(x+a)^2$，$x^2-2ax+a^2$ は $(x-a)^2$，$x^2-a^2$ は $(x+a)(x-a)$（公式2〜4の逆）。",
                    "因数分解できたら，展開してもとの式にもどるかを確かめる。共通因数が残っていないかも確かめる。"],
                   points=[tp("「積が $q$」を先に考え，その中から「和が $p$」の組を選ぶ順序を教える。", ask="$x^2-x-12$ では，積が $-12$ の組のうち和が $-1$ になるのはどれか。", expect="$3$ と $-4$。")]),
        definition("df1", "因数分解の手順",
                   "因数分解は，次の順に考えると見通しがよい。",
                   conditions=["① 共通因数があればくくり出す。", "② かっこの中が公式の形かどうか（項が2つなら $x^2-a^2$，3つなら $x^2+px+q$ や平方の形）を調べる。",
                               "③ 同じ式のかたまりは1つの文字におきかえて考える（例：$x+1=M$）。", "④ これ以上因数分解できないところまで行う。"],
                   points=[tp("$2x^2-8=2(x^2-4)$ で止めてしまう答案を示し，「最後まで」の意味を考えさせる。", caution="$x^2+9$ のような和の形は，中学校の範囲では因数分解できない。")]),
        example("ex1", "例題1　展開",
                "$(x+4)^2-(x+3)(x-3)$ を計算しなさい。",
                ["$(x+4)^2=x^2+8x+16$。", "$(x+3)(x-3)=x^2-9$。", "$x^2+8x+16-(x^2-9)=x^2+8x+16-x^2+9$。", "$=8x+25$。"],
                "$8x+25$",
                thinking="それぞれの積を乗法公式で展開してから，かっこの前の $-$ に注意してかっこをはずす。",
                points=[tp("ひく式の展開結果は必ずかっこに入れてから引くよう指導する。")],
                misconceptions=[("$x^2+8x+16-x^2-9$ としてしまう", "かっこの前が $-$ なので，$-9$ は $+9$ になる")]),
        example("ex2", "例題2　因数分解",
                "$3x^2-6x-24$ を因数分解しなさい。",
                ["共通因数 3 をくくり出す：$3(x^2-2x-8)$。", "積が $-8$，和が $-2$ になる2数は $2$ と $-4$。", "$3(x+2)(x-4)$。", "展開すると $3(x^2-2x-8)=3x^2-6x-24$ で，もとの式にもどる。"],
                "$3(x+2)(x-4)$",
                thinking="まず共通因数を探す。かっこの中は $x^2+px+q$ の形。",
                points=[tp("答えを展開して確かめる習慣をつけさせる。")]),
        example("ex3", "例題3　式の計算の利用",
                "連続する2つの奇数の積に1を加えると，4の倍数になることを証明しなさい。",
                ["$n$ を整数とすると，連続する2つの奇数は $2n-1$，$2n+1$ と表される。",
                 "$(2n-1)(2n+1)+1=4n^2-1+1=4n^2$。",
                 "$n^2$ は整数だから，$4n^2$ は4の倍数である。",
                 "したがって，連続する2つの奇数の積に1を加えると，4の倍数になる。"],
                "上の証明のとおり",
                thinking="奇数を文字で表し，乗法公式 $(x+a)(x-a)$ を使って展開する。「4×（整数）」の形を目指す。",
                points=[tp("数の計算のくふう（$103\\times97=(100+3)(100-3)=10000-9$）も同じ公式の利用であることを紹介する。", timing="例題3の後")]),
        board("bd1", "板書案",
              [("① 乗法公式", ["$(x+a)(x+b)=x^2+(a+b)x+ab$", "$(x+a)^2=x^2+2ax+a^2$", "$(x-a)^2=x^2-2ax+a^2$", "$(x+a)(x-a)=x^2-a^2$"]),
               ("② 因数分解", ["共通因数をくくり出す", "積が $q$・和が $p$ の2数", "平方の形・和と差の積", "最後まで・展開して確かめる"]),
               ("③ 利用", ["$103\\times97=100^2-3^2$", "$51^2=(50+1)^2$", "奇数 $2n+1$，偶数 $2n$", "4×（整数）→ 4の倍数"])],
              points=[tp("①と②を左右に並べ，矢印で「展開」「因数分解」が逆の操作であることを示す。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("計算の速さより正確さを優先させ，途中式の1行目に公式の形を書かせる。"),
               tp("負の数をふくむ「積が $q$・和が $p$」の2数は，積の符号から2数の符号を先に決めさせる。", ask="積が負のとき，2数の符号はどうなるか。", expect="一方が正，もう一方が負。"),
               tp("入試では展開・因数分解は4択の計算問題として出題される。誤りの選択肢は符号や $2ab$ の見落としなので，検算（数を代入する）を習慣にさせる。"),
               tp("証明では「$n$ を整数とすると」と文字の意味を必ず書かせる。", timing="例題3")],
              misconceptions=[("$(x+a)^2=x^2+a^2$", "$2ax$ の項が必要。面積図で4つの部分を確かめる"),
                              ("$2x^2-8=2(x^2-4)$ で因数分解は終わり", "$x^2-4=(x+2)(x-2)$ と最後まで分解する"),
                              ("$-(x-3)^2=-x^2-6x+9$", "$-(x^2-6x+9)=-x^2+6x-9$。すべての項の符号が変わる")]),
        summary("sm1", "まとめ",
                ["乗法公式は $(x+a)(x+b)$ の公式から導ける。", "因数分解は「共通因数 → 公式」の順に，最後まで行う。",
                 "答えは展開（または数の代入）で確かめる。", "数の計算のくふうや整数の証明に，展開・因数分解が使える。"]),
        check("ck1", "確認問題",
              [("$(x-6)(x+2)$ を展開しなさい。", "$x^2-4x-12$"), ("$x^2-10x+25$ を因数分解しなさい。", "$(x-5)^2$"),
               ("$98^2$ をくふうして計算しなさい。", "$(100-2)^2=10000-400+4=9604$")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

def _expand_cands(fa, fb, k, V, square, monic):
    """展開の誤答候補（文, 理由, 誤概念）。"""
    full = mul(fa, fb)
    lead = {kk: v for kk, v in full.items() if kk[0] + kk[1] == 2 and kk in ((2, 0),)}
    x2 = {(2, 0): full.get((2, 0), 0)}
    last = {kk: v for kk, v in full.items() if kk[0] == 0}
    mid = {kk: v for kk, v in full.items() if kk[0] == 1}
    c = []
    c.append((D(tex(add(x2, last), V)), "真ん中の項（外側どうし・内側どうしの積の和）を忘れている。", "乗法公式の誤用（$2ab$ の見落とし）"))
    c.append((D(tex(add(x2, mid, sc(last, -1)), V)), "最後の項の符号を誤っている。$(-a)\\times(-a)$ や $a\\times(-b)$ の符号を確かめる。", "符号の誤り"))
    c.append((D(tex(add(x2, sc(mid, -1), last), V)), "真ん中の項の符号を誤っている。", "符号の誤り"))
    if square and mid:
        c.append((D(tex(add(x2, {k_: v // 2 for k_, v in mid.items()}, last), V)), "真ん中の項を2倍していない。", "乗法公式の誤用（$2ab$ の見落とし）"))
    if monic and V[1] not in tex(full, V):
        a = fa.get((0, 0), 0)
        b = fb.get((0, 0), 0)
        c.append((D(tex(add(x2, P((a * b, 1, 0)), P((a + b, 0, 0))), V)), "$x$ の係数（和）と定数項（積）の役割を取り違えている。", "公式の取り違え"))
    c.append((D(tex(add(x2, sc(mid, 2), last), V)) if not square else None, "真ん中の項を2倍している。2倍するのは $(x+a)^2$ の形のときだけ。", "公式の取り違え"))
    c.append((D(tex(add(x2, mid, sc(last, 2)), V)), "最後の項の計算を誤っている。", "計算の誤り"))
    return c


@gen("basic_check", 6, ["computation"])
def a_expand(r):
    V = r.choice(VARS + [("x", "y")])
    y = r.random() < 0.3
    kind = r.choice(["sum_prod", "sum_prod", "sq_plus", "sq_minus", "sum_diff", "general"])
    if kind == "sum_prod":
        p = q_ = 1
        a = nz(r, -9, 9)
        b = nz(r, -9, 9, (0, a, -a))
        fa, fb = lin(1, a, y), lin(1, b, y)
        name = "$(x+a)(x+b)=x^2+(a+b)x+ab$"
    elif kind == "sq_plus":
        k = r.choice([1, 1, 2, 3])
        a = r.randint(1, 9)
        fa = fb = lin(k, a, y)
        name = "$(x+a)^2=x^2+2ax+a^2$"
    elif kind == "sq_minus":
        k = r.choice([1, 1, 2, 3])
        a = r.randint(1, 9)
        fa = fb = lin(k, -a, y)
        name = "$(x-a)^2=x^2-2ax+a^2$"
    elif kind == "sum_diff":
        k = r.choice([1, 1, 2, 3, 4])
        a = r.randint(1, 9)
        fa, fb = lin(k, a, y), lin(k, -a, y)
        name = "$(x+a)(x-a)=x^2-a^2$"
    else:
        p, q_ = r.choice([(2, 1), (1, 2), (3, 1), (2, 3), (3, 2)])
        a, b = nz(r, -7, 7), nz(r, -7, 7)
        fa, fb = lin(p, a, y), lin(q_, b, y)
        name = "分配法則 $(a+b)(c+d)=ac+ad+bc+bd$"
    full = mul(fa, fb)
    square = fa == fb
    monic = kind == "sum_prod"
    expr = (f"{pf(fa, V)}^2" if square else f"{pf(fa, V)}{pf(fb, V)}")
    right = D(tex(full, V))
    cands = _expand_cands(fa, fb, 1, V, square, monic)
    if kind == "sum_diff":
        cands.insert(0, (D(tex(add(full, sc({k_: v for k_, v in full.items() if k_[0] == 0}, -2)), V)), "最後の項の符号を誤っている。$a\\times(-a)=-a^2$。", "符号の誤り"))
        cands.append((D(tex(mul(fa, fa), V)), "$(x+a)^2$ の公式と取り違えている。", "公式の取り違え"))
    return MC(f"${expr}$ を展開した式として正しいものを，" + SEL4, right, cands, f"{name} を使うと ${expr}={tex(full, V)}$。", d=1,
              ap="どの乗法公式の形かを見分ける。$x$ のかわりに $2x$ や $3y$ が入っているときは，それを1つのかたまりとみて公式にあてはめる。",
              steps=[f"使う公式：{name}。", f"${expr}={tex(full, V)}$。"],
              alt=["分配法則で4つの積をすべて書き出し，同類項をまとめても同じ結果になる。", f"文字に数（たとえば ${V[0]}=1$）を代入して，両辺の値が等しいかを確かめる。"],
              pc=[("適切な公式（分配法則）を選んでいる", 1), ("正しく展開している", 1)],
              pit=["$(x+a)^2=x^2+a^2$ としてしまう。", "負の数の積の符号を誤る。"],
              chk=(f"({py(fa, V)})*({py(fb, V)})", py(full, V), "expand", "intermediate"))


def _pairs(q):
    out = []
    for a in range(-abs(q), abs(q) + 1):
        if a and q % a == 0:
            out.append((a, q // a))
    return out


@gen("basic_check", 6, ["computation"])
def a_factor(r):
    V = r.choice(VARS)
    x = V[0]
    kind = r.choice(["trin", "trin", "sq", "diff", "common"])
    if kind == "trin":
        m = nz(r, -9, 9)
        n = nz(r, -9, 9, (0, m, -m))
        poly_ = mul(lin(1, m), lin(1, n))
        right = D(fac(1, [(lin(1, m), 1), (lin(1, n), 1)], V))
        cands = [(D(fac(1, [(lin(1, -m), 1), (lin(1, -n), 1)], V)), "符号が逆になっている。展開すると $x$ の係数の符号が変わる。", "符号の誤り"),
                 (D(fac(1, [(lin(1, m), 1), (lin(1, -n), 1)], V)), "展開すると定数項の符号がもとの式と異なる。", "符号の誤り"),
                 (D(fac(1, [(lin(1, -m), 1), (lin(1, n), 1)], V)), "展開すると定数項の符号がもとの式と異なる。", "符号の誤り")]
        for a, b in _pairs(m * n):
            if a < b and a + b != m + n:
                cands.append((D(fac(1, [(lin(1, a), 1), (lin(1, b), 1)], V)), f"積は ${m * n}$ になるが，和が ${a + b}$ で ${m + n}$ にならない。", "和の条件の見落とし"))
        st = [f"積が ${m * n}$，和が ${m + n}$ になる2数を探すと ${m}$ と ${n}$。", f"${tex(poly_, V)}={right[1:-1]}$。"]
        fs, k = [(lin(1, m), 1), (lin(1, n), 1)], 1
        name = "$x^2+(a+b)x+ab=(x+a)(x+b)$"
    elif kind == "sq":
        a = nz(r, -9, 9)
        kk = r.choice([1, 1, 2, 3]) if abs(a) <= 5 else 1
        poly_ = mul(lin(kk, a), lin(kk, a))
        right = D(fac(1, [(lin(kk, a), 2)], V))
        cands = [(D(fac(1, [(lin(kk, -a), 2)], V)), "かっこの中の符号が逆。展開すると真ん中の項の符号が変わる。", "符号の誤り"),
                 (D(fac(1, [(lin(kk, a), 1), (lin(kk, -a), 1)], V)), "展開すると $x^2-a^2$ の形になり，真ん中の項が出てこない。", "公式の取り違え"),
                 (D(fac(1, [(lin(kk, 2 * a), 2)], V)), "真ん中の項の係数をそのまま使っている。$2a$ の半分が $a$。", "公式の誤用"),
                 (D(fac(1, [(lin(kk, a * a), 2)], V)), "定数項 $a^2$ をそのままかっこに入れている。", "公式の誤用")]
        st = [f"定数項 ${a * a}={abs(a)}^2$，真ん中の項 ${2 * kk * a}{x}=2\\times {kk if kk > 1 else ''}{x}\\times({a})$ から平方の形。", f"${tex(poly_, V)}={right[1:-1]}$。"]
        fs, k = [(lin(kk, a), 2)], 1
        name = "$x^2\\pm2ax+a^2=(x\\pm a)^2$"
    elif kind == "diff":
        kk = r.choice([1, 1, 2, 3, 4, 5])
        a = r.randint(1, 9)
        two = r.random() < 0.3
        f1, f2 = lin(kk, a, two), lin(kk, -a, two)
        poly_ = mul(f1, f2)
        right = D(fac(1, [(f1, 1), (f2, 1)], V))
        cands = [(D(fac(1, [(f2, 2)], V)), "展開すると真ん中の項が出てくるので，もとの式にならない。", "公式の取り違え"),
                 (D(fac(1, [(f1, 2)], V)), "展開すると真ん中の項が出てくるので，もとの式にならない。", "公式の取り違え"),
                 (D(fac(1, [(lin(kk, a * a, two), 1), (lin(kk, -a * a, two), 1)], V)), f"$a^2$ ではなく $a$ を使う。${a * a}={a}^2$。", "平方の見落とし"),
                 (D(fac(1, [(lin(a, kk, two), 1), (lin(a, -kk, two), 1)], V)) if a != kk else None, "係数と定数の位置が入れかわっている。", "公式の誤用")]
        st = [f"${tex(poly_, V)}=({tex(P((kk, 1, 0)), V)})^2-({tex(P((a, 0, 1)) if two else P((a, 0, 0)), V)})^2$ と見る。", f"和と差の積で ${right[1:-1]}$。"]
        fs, k = [(f1, 1), (f2, 1)], 1
        name = "$x^2-a^2=(x+a)(x-a)$"
    else:
        g = r.choice([2, 3, 4, 5, 6])
        b = nz(r, -9, 9)
        a1 = r.choice([1, 2, 3]) if g <= 3 else 1
        inner = lin(a1, b)
        poly_ = sc(mul(P((1, 1, 0)), inner), g)
        right = D(fac(g, [(P((1, 1, 0)), 1), (inner, 1)], V))
        cands = [(D(fac(g, [(add(P((a1, 2, 0)), P((b, 1, 0))), 1)], V)), f"かっこの中にまだ共通因数 ${x}$ が残っている。", "因数分解が不完全"),
                 (D(fac(1, [(P((1, 1, 0)), 1), (sc(inner, g), 1)], V)), f"かっこの中にまだ共通因数 ${g}$ が残っている。", "因数分解が不完全"),
                 (D(fac(g, [(P((1, 1, 0)), 1), (lin(a1, -b), 1)], V)), "かっこの中の符号が誤っている。", "符号の誤り"),
                 (D(fac(g, [(P((1, 1, 0)), 1), (lin(a1, b * g), 1)], V)), f"かっこの中の数を ${g}$ でわっていない。", "共通因数のくくり出しの誤り")]
        st = [f"各項に共通な因数は ${g}{x}$。", f"${tex(poly_, V)}={right[1:-1]}$。"]
        fs, k = [(P((1, 1, 0)), 1), (inner, 1)], g
        name = "共通因数をくくり出す $ma+mb=m(a+b)$"
    return MC(f"${tex(poly_, V)}$ を因数分解した式として正しいものを，" + SEL4, right, cands, f"{name} を使って ${right[1:-1]}$。", d=1,
              ap="まず共通因数を探す。項が3つなら「積が定数項・和が $x$ の係数」になる2数や平方の形，項が2つなら和と差の積の形を考える。",
              steps=st, alt=["選んだ答えを展開して，もとの式にもどるかを確かめる。"],
              pc=[("適切な因数分解の方法を選んでいる", 1), ("正しく因数分解している", 1)],
              pit=["符号を誤る。", "共通因数をくくり出したところで止めてしまう。"],
              chk=(facpy(k, fs, V), py(poly_, V), "expand", "intermediate"))


@gen("basic_check", 4, ["computation", "concept"])
def a_coef(r):
    kind = r.choice(["xcoef", "const", "sqmid", "diffc", "sqk"])
    if kind == "xcoef":
        a, b = nz(r, -9, 9), nz(r, -9, 9)
        if a + b <= 0:
            a, b = abs(a) + 1, abs(b)
        v = a + b
        stem = f"$(x{a:+d})(x{b:+d})$ を展開したとき，$x$ の係数を求めなさい。"
        st = ["$(x+a)(x+b)=x^2+(a+b)x+ab$ より，$x$ の係数は $a+b$。", f"${a}+({b})={v}$。"]
        expr = f"{a}+({b})"
    elif kind == "const":
        a = nz(r, -9, 9)
        b = r.choice([v for v in range(-9, 10) if v and v * a > 0 and v != a])
        v = a * b
        stem = f"$(x{a:+d})(x{b:+d})$ を展開したとき，定数項を求めなさい。"
        st = ["$(x+a)(x+b)=x^2+(a+b)x+ab$ より，定数項は $ab$。", f"${a}\\times({b})={v}$。"]
        expr = f"{a}*({b})"
    elif kind == "sqmid":
        c = r.randint(2, 12)
        v = 2 * c
        stem = f"$x^2+\\square x+{c * c}$ が $(x+a)^2$ の形に因数分解できるとき，$\\square$ にあてはまる正の数を求めなさい。"
        st = [f"${c * c}={c}^2$ なので $a={c}$。", f"真ん中の項は $2ax=2\\times{c}\\times x={v}x$。"]
        expr = f"2*{c}"
    elif kind == "diffc":
        c = r.randint(2, 15)
        v = c * c
        stem = f"$x^2-\\square=(x+{c})(x-{c})$ が成り立つとき，$\\square$ にあてはまる数を求めなさい。"
        st = ["$(x+a)(x-a)=x^2-a^2$。", f"$a={c}$ なので ${c}^2={v}$。"]
        expr = f"{c}**2"
    else:
        k, c = r.choice([2, 3, 4, 5]), r.randint(1, 9)
        v = 2 * k * c
        stem = f"$({k}x+{c})^2$ を展開したとき，$x$ の係数を求めなさい。"
        st = [f"$({k}x+{c})^2=({k}x)^2+2\\times{k}x\\times{c}+{c}^2$。", f"$x$ の係数は $2\\times{k}\\times{c}={v}$。"]
        expr = f"2*{k}*{c}"
    return MARK(stem, v, f"答えは ${v}$。", expr, d=1,
                ap="乗法公式の各項（$x^2$ の項・$x$ の項・定数項）が，もとの式のどの数からできるかを思い出す。",
                steps=st, alt=["実際に全体を展開して，求める項を読み取って確かめる。"],
                pc=[("公式の各項の意味を理解している", 1), ("正しい数を求めている", 1)],
                pit=["$x$ の係数と定数項を取り違える。", "$2ax$ の2を忘れる。"])


@gen("basic_check", 4, ["concept", "condition_check"])
def a_concept(r):
    kind = r.choice(["pair", "pair", "which_diff", "which_sq"])
    if kind == "pair":
        m = nz(r, -9, 9)
        n = nz(r, -9, 9, (0, m, -m))
        p, q = m + n, m * n
        right = f"${min(m, n)}$ と ${max(m, n)}$"
        cands = [(f"${-max(m, n)}$ と ${-min(m, n)}$", f"積は ${q}$ だが，和が ${-p}$ になる。", "和の符号の誤り")]
        for a, b in _pairs(q):
            if a < b and a + b != p:
                cands.append((f"${a}$ と ${b}$", f"積は ${q}$ だが，和が ${a + b}$ で ${p}$ にならない。", "和の条件の見落とし"))
        cands.append((f"${p}$ と ${q}$" if p != q else None, "係数そのものを答えている。積が定数項，和が $x$ の係数になる2数を探す。", "因数分解の考え方の誤解"))
        stem = f"$x^2{p:+d}x{q:+d}$ を $(x+a)(x+b)$ の形に因数分解するとき，$a$，$b$ にあてはまる2つの数の組として正しいものを，" + SEL4
        stem = stem.replace("+1x", "+x").replace("-1x", "-x").replace("+0x", "")
        e = f"積が ${q}$，和が ${p}$ になる2数は ${m}$ と ${n}$。"
        st = [f"積が ${q}$ になる2つの整数の組を書き出す。", f"その中で和が ${p}$ になるのは ${m}$ と ${n}$。"]
        ch = (f"({m})*({n})", str(q))
    elif kind == "which_diff":
        a = r.randint(2, 12)
        right = f"$x^2-{a * a}$"
        cands = [(f"$x^2+{a * a}$", "和の形なので，$(x+a)(x-a)$ の形にはならない。", "和と差の混同"),
                 (f"$x^2-{2 * a}x+{a * a}$", f"これは $(x-{a})^2$ と因数分解される。", "公式の取り違え"),
                 (f"$x^2+{2 * a}x+{a * a}$", f"これは $(x+{a})^2$ と因数分解される。", "公式の取り違え"),
                 (f"$x^2-{a}x$", f"これは共通因数 $x$ をくくり出して $x(x-{a})$ となる。", "公式の取り違え")]
        stem = "次の式のうち，$(x+a)(x-a)$（$a$ は正の整数）の形に因数分解できるものとして最も適するものを，" + SEL4
        e = f"$x^2-{a * a}=x^2-{a}^2=(x+{a})(x-{a})$。"
        st = ["$(x+a)(x-a)=x^2-a^2$ なので，「2乗−2乗」の形を探す。", e]
        ch = (f"(x+{a})*(x-{a})", f"x**2-{a * a}")
    else:
        a = r.randint(2, 10)
        sgn = r.choice([1, -1])
        right = f"$x^2{2 * a * sgn:+d}x+{a * a}$"
        cands = [(f"$x^2{a * sgn:+d}x+{a * a}$", f"真ん中の項が $2\\times{a}x$ になっていないので平方の形ではない。", "公式の誤用"),
                 (f"$x^2{2 * a * sgn:+d}x-{a * a}$", "定数項が負なので平方の形ではない。", "符号の誤り"),
                 (f"$x^2-{a * a}$", f"これは $(x+{a})(x-{a})$ と因数分解される。", "公式の取り違え"),
                 (f"$x^2{2 * a * sgn:+d}x+{2 * a}$", f"定数項が ${a}^2$ になっていない。", "公式の誤用")]
        stem = "次の式のうち，$(x+a)^2$ または $(x-a)^2$ の形に因数分解できるものとして最も適するものを，" + SEL4
        e = f"$x^2{2 * a * sgn:+d}x+{a * a}=(x{a * sgn:+d})^2$。"
        st = ["平方の形 $x^2\\pm2ax+a^2$ は，定数項が $a^2$，真ん中の項が $\\pm2ax$。", e]
        ch = (f"(x+({a * sgn}))**2", f"x**2+({2 * a * sgn})*x+{a * a}")
    return MC(stem, right, cands, e, d=1,
              ap="乗法公式を逆に見て，式の形（項の数・定数項・$x$ の係数）から因数分解の型を判断する。",
              steps=st, alt=["選んだものを実際に因数分解し，展開してもとにもどるかを確かめる。"],
              pc=[("公式の形を正しく見分けている", 1), ("正しいものを選んでいる", 1)],
              pit=["和の形 $x^2+a^2$ を $(x+a)(x-a)$ としてしまう。"],
              chk=ch + ("expand", "intermediate"))


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 5, ["computation", "common_error"])
def b_simplify(r):
    V = ("x", "y")
    kind = r.choice(["sq_minus_sd", "prod_minus_sq", "prod_minus_prod", "sq_minus_sq", "x_times"])
    a = nz(r, -8, 8)
    b = nz(r, -8, 8, (0, a, -a))
    c = nz(r, -8, 8, (0,))
    if kind == "sq_minus_sd":
        A, B = (lin(1, a), lin(1, a)), (lin(1, abs(b)), lin(1, -abs(b)))
    elif kind == "prod_minus_sq":
        A, B = (lin(1, a), lin(1, b)), (lin(1, c), lin(1, c))
    elif kind == "prod_minus_prod":
        d = nz(r, -8, 8, (0, c))
        A, B = (lin(1, a), lin(1, b)), (lin(1, c), lin(1, d))
    elif kind == "sq_minus_sq":
        c2 = nz(r, -8, 8, (0, a))
        A, B = (lin(1, a), lin(1, a)), (lin(1, c2), lin(1, c2))
    else:
        A, B = (P((1, 1, 0)), lin(1, a)), (lin(1, b), lin(1, -b))
    EA, EB = mul(*A), mul(*B)
    res = add(EA, sc(EB, -1))
    assert res

    def show(F):
        return f"{pf(F[0])}^2" if F[0] == F[1] else (f"{tex(F[0])}{pf(F[1])}" if len(F[0]) == 1 else f"{pf(F[0])}{pf(F[1])}")
    expr = f"{show(A)}-{show(B)}"
    lead = {(2, 0): EB.get((2, 0), 0)}
    w1 = add(EA, sc(lead, -1), add(EB, sc(lead, -1)))
    w2 = add(EA, sc(EB, -1), sc({k: v for k, v in EB.items() if k[0] == 0}, 2))
    sqA = A[0] == A[1]
    w3 = add({k: v for k, v in EA.items() if k[0] != 1}, sc(EB, -1)) if sqA else add(res, P((1, 0, 0)))
    w4 = add(res, sc({k: v for k, v in res.items() if k[0] == 1}, -2))
    cands = [(D(tex(w1)), "かっこの前の $-$ を，ひく式の最初の項にしかかけていない。", "かっこをはずすときの符号の誤り"),
             (D(tex(w2)), "ひく式の定数項の符号を誤っている。", "符号の誤り"),
             (D(tex(w3)), "$(x+a)^2$ の展開で真ん中の項を忘れている。" if sqA else "定数項の計算を誤っている。", "乗法公式の誤用" if sqA else "計算の誤り"),
             (D(tex(w4)), "$x$ の項の符号を誤っている。", "符号の誤り")]
    right = D(tex(res))
    return MC(f"${expr}$ を計算した結果として正しいものを，" + SEL4, right, cands, f"${tex(EA)}-({tex(EB)})={tex(res)}$。", d=2, p=4,
              ap="それぞれの積を乗法公式で展開し，ひく方の式はかっこに入れたまま引く。かっこの前が $-$ のときは，すべての項の符号を変える。",
              steps=[f"${show(A)}={tex(EA)}$。", f"${show(B)}={tex(EB)}$。", f"${tex(EA)}-({tex(EB)})={terms_tex(terms(EA) + [(-c_, i, j) for c_, i, j in terms(EB)])}$。", f"$={tex(res)}$。"],
              alt=["$x=1$ など数を代入し，もとの式と答えの値が等しいかを確かめる。"],
              pc=[("それぞれの積を正しく展開している", 2), ("かっこをはずして正しくまとめている", 2)],
              pit=["かっこの前の $-$ を一部の項にしかかけない。", "$(x+a)^2$ の $2ax$ を忘れる。"],
              chk=(f"({py(mul(*A))})-({py(mul(*B))})", py(res), "expand", "intermediate"))


@gen("standard_practice", 5, ["computation", "condition_check"])
def b_factor2(r):
    kind = r.choice(["common_then", "common_then", "subst", "two_var", "ab_diff"])
    V = r.choice(VARS)
    x, yv = V
    if kind == "common_then":
        g = r.choice([2, 3, 4, 5, -2, -3])
        m = nz(r, -7, 7)
        n = nz(r, -7, 7, (0, m, -m))
        inner = mul(lin(1, m), lin(1, n))
        poly_ = sc(inner, g)
        fs = [(lin(1, m), 1), (lin(1, n), 1)]
        right = D(fac(g, fs, V))
        cands = [(D(fac(g, [(inner, 1)], V)), "かっこの中がまだ因数分解できる。", "因数分解が不完全"),
                 (D(fac(g, [(lin(1, -m), 1), (lin(1, -n), 1)], V)), "かっこの中の符号が逆になっている。", "符号の誤り"),
                 (D(fac(1, [(lin(g, g * m), 1), (lin(1, n), 1)], V)), f"共通因数 ${g}$ が一方のかっこの中に残っている。", "因数分解が不完全"),
                 (D(fac(-g, fs, V)), "くくり出した数の符号が誤っている。", "符号の誤り")]
        st = [f"共通因数 ${g}$ をくくり出す：${fac(g, [(inner, 1)], V)}$。", f"積が ${m * n}$，和が ${m + n}$ の2数は ${m}$，${n}$。", f"${right[1:-1]}$。"]
        k = g
    elif kind == "subst":
        a = nz(r, -5, 5)
        m = nz(r, -6, 6)
        n = nz(r, -6, 6, (0, m, -m))
        M = lin(1, a)
        poly_ = add(mul(M, M), sc(M, m + n), P((m * n, 0, 0)))
        c1 = m + n
        mid_ = "" if c1 == 0 else (("+" if c1 == 1 else "-" if c1 == -1 else f"{c1:+d}") + pf(M, V))
        shown = f"{pf(M, V)}^2{mid_}{m * n:+d}"
        fs = [(lin(1, a + m), 1), (lin(1, a + n), 1)]
        fs = [f for f in fs if f[0]]
        right = D(fac(1, fs, V))
        cands = [(D(fac(1, [(lin(1, m), 1), (lin(1, n), 1)], V)), f"$M={tex(M, V)}$ とおいて因数分解した後，$M$ をもとにもどしていない。", "おきかえの戻し忘れ"),
                 (D(fac(1, [(lin(1, a - m), 1), (lin(1, a - n), 1)], V)), "おきかえた後の2数の符号を誤っている。", "符号の誤り"),
                 (D(fac(1, [(lin(1, a + m), 1), (lin(1, n), 1)], V)), "一方のかっこだけしか $M$ をもとにもどしていない。", "おきかえの戻し忘れ"),
                 (D(fac(1, [(lin(1, a + m * n), 1), (lin(1, a + m + n), 1)], V)), "和と積の役割を取り違えている。", "公式の取り違え")]
        st = [f"${tex(M, V)}=M$ とおくと，$M^2{m + n:+d}M{m * n:+d}$。".replace("+0M", "").replace("+1M", "+M").replace("-1M", "-M"),
              f"$=(M{m:+d})(M{n:+d})$。", f"$M$ をもとにもどして ${right[1:-1]}$。"]
        k = 1
    elif kind == "two_var":
        m = nz(r, -8, 8)
        n = nz(r, -8, 8, (0, m, -m))
        f1, f2 = lin(1, m, True), lin(1, n, True)
        poly_ = mul(f1, f2)
        fs = [(f1, 1), (f2, 1)]
        right = D(fac(1, fs, V))
        cands = [(D(fac(1, [(lin(1, -m, True), 1), (lin(1, -n, True), 1)], V)), "符号が逆になっている。", "符号の誤り"),
                 (D(fac(1, [(lin(1, m), 1), (lin(1, n), 1)], V)), f"${yv}$ が抜けている。展開しても ${yv}^2$ の項が出てこない。", "文字の見落とし"),
                 (D(fac(1, [(lin(1, m, True), 1), (lin(1, -n, True), 1)], V)), f"展開すると ${yv}^2$ の項の符号がもとの式と異なる。", "符号の誤り"),
                 (D(fac(1, [(P((1, 1, 0), (m, 0, 1)), 1), (P((1, 0, 1), (n, 1, 0)), 1)], V)), "文字の位置を誤っている。", "公式の誤用")]
        st = [f"${yv}$ をふくむ項を「数×${yv}$」とみて，積が ${m * n}$，和が ${m + n}$ の2数を探す：${m}$，${n}$。", f"${right[1:-1]}$。"]
        k = 1
    else:
        g = r.choice([2, 3, 5, 7])
        b = r.randint(1, 6)
        inner = P((1, 2, 0), (-b * b, 0, 0))
        poly_ = sc(inner, g)
        fs = [(lin(1, b), 1), (lin(1, -b), 1)]
        right = D(fac(g, fs, V))
        cands = [(D(fac(g, [(inner, 1)], V)), "かっこの中の $x^2-b^2$ がまだ因数分解できる。", "因数分解が不完全"),
                 (D(fac(g, [(lin(1, -b), 2)], V)), "展開すると真ん中の項が出てくる。", "公式の取り違え"),
                 (D(fac(1, [(lin(g, g * b), 1), (lin(1, -b), 1)], V)), f"共通因数 ${g}$ が一方のかっこの中に残っている。", "因数分解が不完全"),
                 (D(fac(g, [(lin(1, b * b), 1), (lin(1, -b * b), 1)], V)), f"${b * b}$ を ${b}^2$ と見ていない。", "平方の見落とし")]
        st = [f"共通因数 ${g}$ をくくり出す：${fac(g, [(inner, 1)], V)}$。", f"$x^2-{b * b}=(x+{b})(x-{b})$。", f"${right[1:-1]}$。"]
        k = g
    shown_expr = shown if kind == "subst" else tex(poly_, V)
    return MC(f"${shown_expr}$ を因数分解した式として正しいものを，" + SEL4, right, cands, f"${shown_expr}={right[1:-1]}$。", d=3, p=4,
              ap="①共通因数をくくり出す　②同じかたまりは1つの文字におきかえる　③公式の形にあてはめる，の順に考え，最後まで因数分解する。",
              steps=st, alt=["答えを展開して，もとの式にもどることを確かめる。"],
              pc=[("共通因数・おきかえなど方針を正しく選んでいる", 2), ("最後まで正しく因数分解している", 2)],
              pit=["共通因数をくくり出したところで止める。", "おきかえた文字をもとにもどし忘れる。"],
              chk=(facpy(k, fs, V), py(poly_, V), "expand", "intermediate"))


@gen("standard_practice", 5, ["computation", "application"])
def b_trick(r):
    kind = r.choice(["sd", "sq_plus", "sq_minus", "diff_sq", "value_sq", "value_diff"])
    if kind == "sd":
        base = r.choice([20, 30, 40, 50, 60, 70, 80, 100, 200])
        d = r.randint(1, 9)
        v = (base + d) * (base - d)
        stem = f"${base + d}\\times{base - d}$ を，乗法公式を利用してくふうして計算しなさい。"
        st = [f"${base + d}\\times{base - d}=({base}+{d})({base}-{d})$。", f"$={base}^2-{d}^2={base * base}-{d * d}={v}$。"]
        expr = f"{base + d}*{base - d}"
    elif kind == "sq_plus":
        base = r.choice([20, 30, 40, 50, 60, 70, 100])
        d = r.randint(1, 4)
        v = (base + d) ** 2
        stem = f"${base + d}^2$ を，乗法公式を利用してくふうして計算しなさい。"
        st = [f"${base + d}^2=({base}+{d})^2$。", f"$={base}^2+2\\times{base}\\times{d}+{d}^2={base * base}+{2 * base * d}+{d * d}={v}$。"]
        expr = f"{base + d}**2"
    elif kind == "sq_minus":
        base = r.choice([30, 40, 50, 60, 70, 80, 100, 200])
        d = r.randint(1, 4)
        v = (base - d) ** 2
        stem = f"${base - d}^2$ を，乗法公式を利用してくふうして計算しなさい。"
        st = [f"${base - d}^2=({base}-{d})^2$。", f"$={base}^2-2\\times{base}\\times{d}+{d}^2={base * base}-{2 * base * d}+{d * d}={v}$。"]
        expr = f"{base - d}**2"
    elif kind == "diff_sq":
        p = r.randint(30, 99)
        q = r.choice([v for v in range(11, p) if (p + v) % 10 == 0 or (p - v) % 10 == 0])
        v = p * p - q * q
        stem = f"${p}^2-{q}^2$ を，因数分解を利用してくふうして計算しなさい。"
        st = [f"${p}^2-{q}^2=({p}+{q})({p}-{q})$。", f"$={p + q}\\times{p - q}={v}$。"]
        expr = f"{p}**2-{q}**2"
    elif kind == "value_sq":
        a = r.randint(2, 9)
        t = r.choice([50, 100, 200, 1000, 30, 40])
        x0 = t - a
        v = t * t
        stem = f"$x={x0}$ のとき，$x^2+{2 * a}x+{a * a}$ の値を求めなさい。"
        st = [f"$x^2+{2 * a}x+{a * a}=(x+{a})^2$ と因数分解する。", f"$x={x0}$ を代入すると $({x0}+{a})^2={t}^2={v}$。"]
        expr = f"{x0}**2+{2 * a}*{x0}+{a * a}"
    else:
        s = r.choice([10, 20, 50, 100])
        x0 = r.randint(s // 2 + 1, s - 1) if s > 10 else r.randint(6, 9)
        y0 = s - x0
        if r.random() < 0.5:
            x0, y0 = x0 + Fr(1, 2), y0 - Fr(1, 2)
        v = x0 * x0 - y0 * y0
        assert v > 0 and v.denominator == 1
        xs, ys = (f"{float(x0):g}", f"{float(y0):g}")
        stem = f"$x={xs}$，$y={ys}$ のとき，$x^2-y^2$ の値を求めなさい。"
        st = ["$x^2-y^2=(x+y)(x-y)$ と因数分解する。", f"$x+y={s}$，$x-y={float(x0 - y0):g}$ なので，${s}\\times{float(x0 - y0):g}={v}$。"]
        expr = f"({xs})**2-({ys})**2"
    return MARK(stem, v, f"答えは ${v}$。", expr, d=2, p=4,
                ap="そのまま計算せず，数を「キリのよい数±小さい数」と見て乗法公式を使ったり，式を因数分解してから代入したりする。",
                steps=st, alt=["筆算で直接計算して，同じ結果になるかを確かめる。"],
                pc=[("乗法公式・因数分解を使う形に変形している", 2), ("正しい値を求めている", 2)],
                pit=["$(a+b)^2=a^2+b^2$ として計算する。", "因数分解せずに代入して計算ミスをする。"])


@gen("standard_practice", 5, ["computation", "multiple_solutions"])
def b_value(r):
    kind = r.choice(["x2y2", "diff2", "x2y_xy2", "x2_y2", "sumsq"])
    s = nz(r, -9, 9)
    p = nz(r, -12, 12)
    assert s * s - 4 * p >= 0  # x，y が実数として存在する
    if kind == "x2y2":
        v = s * s - 2 * p
        assert v > 0
        stem = f"$x+y={s}$，$xy={p}$ のとき，$x^2+y^2$ の値を求めなさい。"
        st = ["$(x+y)^2=x^2+2xy+y^2$ より，$x^2+y^2=(x+y)^2-2xy$。", f"$=({s})^2-2\\times({p})={s * s}{-2 * p:+d}={v}$。"]
        alt = ["$x$，$y$ を具体的に求められる場合は，その値を代入して確かめる。"]
        expr = f"({s})**2-2*({p})"
    elif kind == "diff2":
        v = s * s - 4 * p
        assert v >= 0
        stem = f"$x+y={s}$，$xy={p}$ のとき，$(x-y)^2$ の値を求めなさい。"
        st = ["$(x-y)^2=x^2-2xy+y^2=(x+y)^2-4xy$。", f"$={s * s}-4\\times({p})={v}$。"]
        alt = ["$x^2+y^2=(x+y)^2-2xy$ を先に求め，$(x-y)^2=x^2+y^2-2xy$ としてもよい。"]
        expr = f"({s})**2-4*({p})"
    elif kind == "x2y_xy2":
        v = s * p
        assert v > 0
        stem = f"$x+y={s}$，$xy={p}$ のとき，$x^2y+xy^2$ の値を求めなさい。"
        st = ["共通因数 $xy$ をくくり出すと，$x^2y+xy^2=xy(x+y)$。", f"$={p}\\times({s})={v}$。"]
        alt = ["$x$，$y$ の値を求めずに，式の形を変えてから代入するのがポイント。"]
        expr = f"({p})*({s})"
    elif kind == "x2_y2":
        d = nz(r, -9, 9)
        v = s * d
        assert v > 0
        stem = f"$x+y={s}$，$x-y={d}$ のとき，$x^2-y^2$ の値を求めなさい。"
        st = ["$x^2-y^2=(x+y)(x-y)$。", f"$={s}\\times({d})={v}$。"]
        alt = [f"連立方程式を解いて $x={ft(Fr(s + d, 2))}$，$y={ft(Fr(s - d, 2))}$ を求め，代入して確かめる。"]
        expr = f"({s})*({d})"
    else:
        a = r.randint(2, 9)
        b = nz(r, -9, 9, (0, a, -a))
        x0 = r.randint(1, 9)
        v = (x0 + a) ** 2 - (x0 + b) * (x0 - b)
        assert v > 0
        stem = f"$x={x0}$ のとき，$(x+{a})^2-(x{b:+d})(x{-b:+d})$ の値を求めなさい。"
        st = [f"式を簡単にすると $x^2+{2 * a}x+{a * a}-(x^2-{b * b})={2 * a}x+{a * a + b * b}$。", f"$x={x0}$ を代入して ${2 * a}\\times{x0}+{a * a + b * b}={v}$。"]
        alt = ["そのまま代入して計算しても同じ値になる（式を簡単にしてから代入する方が計算が楽）。"]
        expr = f"({x0}+{a})**2-({x0}+({b}))*({x0}-({b}))"
    return MARK(stem, v, f"答えは ${v}$。", expr, d=3, p=4,
                ap="求める式を，わかっている $x+y$ や $xy$ を使った形に変形してから代入する。",
                steps=st, alt=alt,
                pc=[("求める式を変形している", 2), ("正しい値を求めている", 2)],
                pit=["$x^2+y^2=(x+y)^2$ としてしまう。", "負の数を代入するときにかっこを忘れる。"])


# ======================================================================
# C 思考力・記述応用
# ======================================================================

PROOFS = [
    dict(claim="連続する2つの奇数の積に1を加えると，4の倍数になる",
         setup="$n$ を整数とすると，連続する2つの奇数は $2n-1$，$2n+1$ と表される。",
         calc="(2n-1)(2n+1)+1", a="4n^2-1+1", aw=["4n^2+1+1", "4n^2-4n-1+1", "2n^2-1+1"], res="4n^2",
         concl="$n^2$ は整数だから，$4n^2$ は（b）である。", b="4の倍数", bw=["奇数", "8の倍数", "6の倍数"]),
    dict(claim="連続する2つの偶数の積に1を加えると，奇数の2乗になる",
         setup="$n$ を整数とすると，連続する2つの偶数は $2n$，$2n+2$ と表される。",
         calc="2n(2n+2)+1", a="4n^2+4n+1", aw=["4n^2+2n+1", "4n^2+4n", "2n^2+4n+1"], res="(2n+1)^2",
         concl="$2n+1$ は奇数だから，$(2n+1)^2$ は（b）である。", b="奇数の2乗", bw=["偶数の2乗", "4の倍数", "偶数"]),
    dict(claim="連続する2つの整数で，大きい方の2乗から小さい方の2乗をひいた差は，2つの数の和に等しい",
         setup="$n$ を整数とすると，連続する2つの整数は $n$，$n+1$ と表される。",
         calc="(n+1)^2-n^2", a="n^2+2n+1-n^2", aw=["n^2+1-n^2", "n^2+n+1-n^2", "n^2+2n-1-n^2"], res="2n+1",
         concl="$2n+1=n+(n+1)$ だから，この差は（b）に等しい。", b="2つの数の和", bw=["2つの数の積", "2つの数の差", "大きい方の数の2倍"]),
    dict(claim="連続する3つの整数で，真ん中の数の2乗から1をひいた差は，両端の数の積に等しい",
         setup="$n$ を整数とすると，連続する3つの整数は $n-1$，$n$，$n+1$ と表される。",
         calc="(n-1)(n+1)", a="n^2+n-n-1", aw=["n^2-n-n+1", "n^2+n-n+1", "n^2-2n-1"], res="n^2-1",
         concl="両端の数の積 $(n-1)(n+1)$ は $n^2-1$ に等しいので，真ん中の数の2乗から1をひいた差は（b）に等しい。", b="両端の数の積", bw=["両端の数の和", "真ん中の数の2倍", "両端の数の差"]),
    dict(claim="連続する2つの偶数の2乗の差は，4の倍数になる",
         setup="$n$ を整数とすると，連続する2つの偶数は $2n$，$2n+2$ と表される。",
         calc="(2n+2)^2-(2n)^2", a="4n^2+8n+4-4n^2", aw=["4n^2+4-4n^2", "4n^2+4n+4-4n^2", "2n^2+8n+4-4n^2"], res="8n+4",
         concl="$8n+4=4(2n+1)$ で，$2n+1$ は整数だから，$8n+4$ は（b）である。", b="4の倍数", bw=["8の倍数", "奇数", "16の倍数"]),
    dict(claim="奇数の2乗から1をひいた差は，8の倍数になる",
         setup="$n$ を整数とすると，奇数は $2n+1$ と表される。",
         calc="(2n+1)^2-1", a="4n^2+4n+1-1", aw=["4n^2+1-1", "4n^2+2n+1-1", "2n^2+4n+1-1"], res="4n^2+4n",
         concl="$4n^2+4n=4n(n+1)$ で，$n(n+1)$ は連続する2つの整数の積だから偶数である。よって $4n(n+1)$ は（b）である。", b="8の倍数", bw=["奇数", "16の倍数", "4の倍数ではない数"]),
]


def _topy(s, v):
    s = s.replace("^", "**")
    s = re.sub(r"(\d)([a-z(])", r"\1*\2", s)
    s = re.sub(r"([a-z)])\(", r"\1*(", s)
    return s.replace("n", v)


@gen("thinking_writing", 4, ["written_reasoning", "concept"])
def c_proof_fill(r):
    T = r.choice(PROOFS)
    v = r.choice(["n", "m"])
    S = lambda t: t.replace("n", v)  # noqa: E731
    aw, bw = r.choice(T["aw"]), r.choice(T["bw"])

    def C(a, b):
        return f"（a）${S(a)}$　（b）{b}"
    right = C(T["a"], T["b"])
    cands = [(C(aw, T["b"]), f"（a）は，${S(T['calc'])}$ を正しく展開した式 ${S(T['a'])}$ である。", "展開の誤り"),
             (C(T["a"], bw), f"（b）は「{T['b']}」である。証明したいことがら（{T['claim']}）を結論として書く。", "結論の取り違え"),
             (C(aw, bw), f"（a）は ${S(T['a'])}$，（b）は「{T['b']}」である。", "展開と結論の誤り")]
    body = "\n".join([S(T["setup"]), f"${S(T['calc'])}$ $=$（a）$={S(T['res'])}$", S(T["concl"]), f"したがって，{T['claim']}。"])
    stem = f"「{T['claim']}」ことを，次のように証明した。\n〔証明〕\n{body}\n上の証明の（a）にあてはまる式と，（b）にあてはまることばの組み合わせとして最も適するものを，" + SEL4
    return MC(stem, right, cands, f"（a）${S(T['a'])}$，（b）{T['b']}。", d=4, p=8,
              ap="（a）は直前の式を乗法公式で展開した途中の式。（b）は証明したいことがら（結論）と同じことばになる。",
              steps=[S(T["setup"]), f"${S(T['calc'])}={S(T['a'])}={S(T['res'])}$。", f"結論は「{T['b']}」。"],
              alt=[f"${v}$ に具体的な整数（$1$，$2$ など）を代入して，（a）の式の値が ${S(T['calc'])}$ の値と等しいかを確かめる。"],
              pc=[("（a）の展開を正しく選んでいる", 4), ("（b）の結論を正しく選んでいる", 4)],
              pit=["乗法公式で真ん中の項を忘れる。", "証明したいことがらと異なる結論を書く。"],
              chk=(_topy(T["calc"], v), _topy(T["a"], v), "expand", "intermediate"))


@gen("thinking_writing", 3, ["cross_unit", "application"], rel=["JH-MATH-G1-U05"])
def c_path(r):
    kind = r.choice(["sq", "sq", "circle", "rect"])
    if kind == "sq":
        a = r.randint(5, 30)
        d = r.randint(1, 4)
        S = (a + 2 * d) ** 2 - a * a
        L = 4 * (a + d)
        assert S == d * L
        stem = (f"1辺が ${a}$ m の正方形の花だんのまわりに，幅 ${d}$ m の道がある。道の面積を $S$ m²，道の真ん中を通る線の長さを $\\ell$ m とすると，$S=d\\ell$（$d$ は道幅）が成り立つ。"
                f"この道の面積 $S$ は何 m² か，求めなさい。")
        st = [f"$S=({a}+2\\times{d})^2-{a}^2=({a + 2 * d})^2-{a}^2$。", f"$=({a + 2 * d}+{a})({a + 2 * d}-{a})={2 * a + 2 * d}\\times{2 * d}={S}$。", f"（確かめ）$\\ell=4\\times({a}+{d})={L}$，$d\\ell={d}\\times{L}={S}$。"]
        rel = ["JH-MATH-G1-U02"]
        return MARK(stem, S, f"$S={S}$ m²。", f"({a}+2*{d})**2-{a}**2", d=3, p=8, rel=rel,
                    ap="道の面積は「外側の正方形−内側の正方形」。2乗の差は因数分解 $A^2-B^2=(A+B)(A-B)$ で楽に計算できる。",
                    steps=st, alt=[f"道の真ん中の線の長さ $\\ell=4({a}+{d})$ を求め，$S=d\\ell$ を使っても求められる。"],
                    pc=[("道の面積を式に表している", 3), ("展開・因数分解を使って計算している", 3), ("正しい値", 2)],
                    pit=["外側の正方形の1辺を $a+d$ としてしまう（両側に道がある）。"])
    if kind == "rect":
        a, b = r.randint(4, 20), r.randint(4, 20)
        d = r.randint(1, 3)
        S = (a + 2 * d) * (b + 2 * d) - a * b
        L = 2 * (a + d) + 2 * (b + d)
        assert S == d * L
        stem = f"縦 ${a}$ m，横 ${b}$ m の長方形の土地のまわりに，幅 ${d}$ m の道がある。道の面積は何 m² か，求めなさい。"
        st = [f"外側の長方形は縦 ${a + 2 * d}$ m，横 ${b + 2 * d}$ m。", f"$S={a + 2 * d}\\times{b + 2 * d}-{a}\\times{b}={S}$。", f"（確かめ）道の真ん中の線の長さは $\\ell=2({a}+{d})+2({b}+{d})={L}$ で，$d\\ell={S}$。"]
        return MARK(stem, S, f"$S={S}$ m²。", f"({a}+2*{d})*({b}+2*{d})-{a}*{b}", d=3, p=8, rel=["JH-MATH-G1-U02"],
                    ap="外側の長方形の面積から内側の長方形の面積を引く。文字で $(a+2d)(b+2d)-ab=2d(a+b)+4d^2=d\\ell$ となることも確かめられる。",
                    steps=st, alt=["道を4つの長方形と4すみの正方形に分けて面積の和を求めてもよい。"],
                    pc=[("道の面積を式に表している", 3), ("正しく計算している", 3), ("正しい値", 2)],
                    pit=["外側の長方形の辺を $a+d$ としてしまう。"])
    rr = r.randint(2, 12)
    d = r.randint(1, 4)
    k = (rr + d) ** 2 - rr * rr
    right = f"${k}\\pi$ m²"
    cands = [(f"${d * d}\\pi$ m²", "道幅を半径とする円の面積を求めている。", "面積の求め方の誤り"),
             (f"${(rr + d) ** 2}\\pi$ m²", "外側の円の面積をそのまま答えている。内側の円の面積を引く。", "面積の求め方の誤り"),
             (f"${2 * rr * d}\\pi$ m²", "$(r+d)^2$ の展開で $d^2$ を落としている。", "乗法公式の誤用"),
             (f"${d * d + rr * rr}\\pi$ m²" if d * d + rr * rr != k else None, "$(r+d)^2=r^2+d^2$ として計算している。", "乗法公式の誤用"),
             (f"${2 * (rr + d) * d}\\pi$ m²", "道の外側の円周に道幅をかけている。真ん中の円周を使う。", "$S=d\\ell$ の誤用")]
    stem = f"半径 ${rr}$ m の円形の池のまわりに，幅 ${d}$ m の道がある。この道の面積として正しいものを，" + SEL4 + "ただし，円周率は $\\pi$ とする。"
    return MC(stem, right, cands, f"$\\pi({rr}+{d})^2-\\pi\\times{rr}^2=\\pi\\times({2 * rr * d}+{d * d})={k}\\pi$。", d=3, p=8, rel=["JH-MATH-G1-U05"],
              ap="道の面積は「外側の円−内側の円」。$\\pi(r+d)^2-\\pi r^2$ を乗法公式で展開して整理する（円の面積は1年の平面図形の内容）。",
              steps=[f"外側の円の半径は ${rr + d}$ m。", f"$S=\\pi\\times{rr + d}^2-\\pi\\times{rr}^2=\\pi({(rr + d) ** 2}-{rr * rr})={k}\\pi$。",
                     f"（確かめ）道の真ん中の円周 $\\ell=2\\pi\\times({rr}+\\dfrac{{{d}}}{{2}})$ に道幅 ${d}$ をかけても ${k}\\pi$。"],
              alt=[f"$\\pi(r+d)^2-\\pi r^2=\\pi d(2r+d)$ と因数分解して，$\\pi\\times{d}\\times{2 * rr + d}={k}\\pi$ と計算してもよい。"],
              pc=[("道の面積を式に表している", 3), ("乗法公式で正しく計算している", 3), ("正しい値", 2)],
              pit=["$(r+d)^2=r^2+d^2$ としてしまう。"],
              chk=(f"({rr}+{d})**2-{rr}**2", str(k), None, "intermediate"))


def _xy_pool(r):
    k = r.randint(2, 9)
    a, b = r.sample([v for v in range(-8, 9) if v], 2)
    m, n = r.randint(51, 99), r.randint(11, 49)
    return [
        ("$(a+b)^2=a^2+b^2$ は，どんな数 $a$，$b$ についても成り立つ。", False, "$(a+b)^2=a^2+2ab+b^2$ で，たとえば $a=b=1$ のとき左辺は 4，右辺は 2 になる。"),
        (f"$x^2+{2 * k}x+{k * k}$ は $(x+{k})^2$ と因数分解できる。", True, f"$(x+{k})^2=x^2+{2 * k}x+{k * k}$ である。"),
        (f"$x^2+{k * k}$ は $(x+{k})(x-{k})$ と因数分解できる。", False, f"$(x+{k})(x-{k})=x^2-{k * k}$ で，符号が異なる。"),
        (f"${m}^2-{n}^2$ は ${m + n}\\times{m - n}$ で計算できる。", True, "$a^2-b^2=(a+b)(a-b)$ を使っている。"),
        ("$2x^2-8$ を $2(x^2-4)$ と変形したところで，因数分解は完了している。", False, "$x^2-4=(x+2)(x-2)$ とさらに因数分解できるので，$2(x+2)(x-2)$ まで行う。"),
        (f"$(x{a:+d})(x{b:+d})$ を展開すると，$x$ の係数は ${a + b}$，定数項は ${a * b}$ になる。", True, "$(x+a)(x+b)=x^2+(a+b)x+ab$ である。"),
        (f"$(x{a:+d})(x{b:+d})$ を展開すると，$x$ の係数は ${a * b}$，定数項は ${a + b}$ になる。" if a * b != a + b else None, False, f"$x$ の係数は和 ${a + b}$，定数項は積 ${a * b}$ である。"),
        ("連続する2つの整数の積は，いつも偶数である。", True, "$n(n+1)$ で，$n$ と $n+1$ のどちらかは偶数だから，積は偶数である。"),
        ("$-(x-3)^2$ を展開すると $-x^2-6x+9$ になる。", False, "$-(x^2-6x+9)=-x^2+6x-9$ で，すべての項の符号が変わる。"),
        (f"$(x-{k})^2$ と $({k}-x)^2$ を展開すると，同じ式になる。", True, f"どちらも $x^2-{2 * k}x+{k * k}$ になる。"),
    ]


@gen("thinking_writing", 3, ["written_reasoning", "condition_check"])
def c_xy_judge(r):
    S = [s for s in _xy_pool(r) if s[0] is not None]
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
        why[ch] = (" ".join(rs), "乗法公式・因数分解の思いこみ")
    return mc("式の展開や因数分解について述べた次の X，Y の文の正誤の組み合わせとして最も適するものを，" + SEL4 + f"\nX　{x[0]}\nY　{y[0]}",
              [ans] + [ch for ch in XY if ch != ans], f"X：{x[2]}　Y：{y[2]}", d=4, p=8, why=why,
              ap="それぞれの文の式を実際に展開・因数分解したり，文字に数を代入したりして，成り立つかどうかを確かめる。",
              steps=[f"X：{x[2]}", f"Y：{y[2]}", f"よって {ans}。"],
              alt=["誤りだと思った文は，成り立たない例（反例）を1つ見つけて確かめる。"],
              pc=[("X の正誤を根拠をもって判断している", 4), ("Y の正誤を根拠をもって判断している", 4)],
              pit=["$(a+b)^2=a^2+b^2$ と思いこむ。", "因数分解を途中で止めてしまう。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

@gen("error_correction", 4, ["common_error", "written_reasoning", "computation"])
def d_line_err(r):
    V = ("x", "y")
    a = nz(r, -7, 7)
    sqA = r.random() < 0.6
    if sqA:
        FA = (lin(1, a), lin(1, a))
    else:
        b0 = nz(r, -7, 7, (0, a, -a))
        FA = (lin(1, a), lin(1, b0))
    c = nz(r, -7, 7, (0, a, -a))
    sdB = r.random() < 0.5
    FB = (lin(1, abs(c)), lin(1, -abs(c))) if sdB else (lin(1, c), lin(1, c))
    if not sqA and not sdB:
        FB = (lin(1, abs(c)), lin(1, -abs(c)))
        sdB = True
    EA, EB = mul(*FA), mul(*FB)
    res = add(EA, sc(EB, -1))
    where = r.choice([0, 1, 2, 3])
    showA = f"{pf(FA[0])}^2" if FA[0] == FA[1] else f"{pf(FA[0])}{pf(FA[1])}"
    showB = f"{pf(FB[0])}^2" if FB[0] == FB[1] else f"{pf(FB[0])}{pf(FB[1])}"
    KA, KB = EA, EB
    if where == 0:
        if sqA:
            KA = {k: v for k, v in EA.items() if k[0] != 1}
            info = ("1行目（$(x+a)^2$ の真ん中の項を忘れた）", "formula", "$(x+a)^2$ を「それぞれ2乗する」と覚えてしまいやすい。")
        else:
            KA = add(EA, sc({k: v for k, v in EA.items() if k[0] == 0}, -2))
            info = ("1行目（定数項の符号）", "sign", "負の数どうし・正と負の数の積の符号を急いで決めてしまう。")
    if where == 1:
        if sdB:
            KB = add(EB, sc({k: v for k, v in EB.items() if k[0] == 0}, -2))
            info = ("2行目（$(x+a)(x-a)$ の定数項の符号）", "sign", "$a\\times(-a)$ の符号を $+$ にしてしまいやすい。")
        else:
            KB = {k: v for k, v in EB.items() if k[0] != 1}
            info = ("2行目（$(x+c)^2$ の真ん中の項を忘れた）", "formula", "$(x+c)^2$ を「それぞれ2乗する」と覚えてしまいやすい。")
    l1 = f"${showA}={tex(KA)}$"
    l2 = f"${showB}={tex(KB)}$"
    seq = terms(KA) + [(-c_, i, j) for c_, i, j in terms(KB)]
    if where == 2:
        tb = terms(KB)
        seq = terms(KA) + [(-tb[0][0], tb[0][1], tb[0][2])] + list(tb[1:])
        info = ("3行目（かっこの前の $-$ を一部の項にしかかけていない）", "sign", "かっこをはずすとき，最初の項だけ符号を変えて，残りの項をそのまま写してしまいやすい。")
    l3 = f"与式 $={terms_tex(seq)}$"
    kres = P(*seq)
    if where == 3:
        lin_part = {k: v for k, v in kres.items() if k[0] == 1}
        kres = add(kres, sc({k: v for k, v in kres.items() if k[0] == 0}, -2)) if any(k[0] == 0 for k in kres) else add(kres, sc(lin_part, -2))
        info = ("4行目（同類項をまとめるときの符号）", "calculation", "項が多いと，符号を見落として計算してしまいやすい。")
    l4 = f"$={tex(kres)}$"
    assert kres != res
    sol = "\n".join(f"{i + 1}行目　{t}" for i, t in enumerate([l1, l2, l3, l4]))
    LINES4 = ["1行目", "2行目", "3行目", "4行目"]
    ok = {0: f"1行目は正しい。${showA}={tex(EA)}$。", 1: f"2行目は正しい。${showB}={tex(EB)}$。",
          2: "3行目は，1・2行目の式をもとに，かっこの前の $-$ に注意して正しくかっこをはずしている。", 3: "4行目は，3行目の式の同類項を正しくまとめている。"}
    why = {LINES4[i]: (ok[i], "誤りの箇所の見落とし") for i in range(4) if i != where}
    fix = f"${showA}-{showB}={tex(res)}$"
    return mc(f"〔問題〕${showA}-{showB}$ を計算しなさい。\n〔Kさんの解答〕\n{sol}\nKさんの解答で，誤りが最初に生じた行として最も適するものを，" + SEL4,
              LINES4, f"誤りが最初に生じたのは{LINES4[where]}。正しくは {fix}。", d=3, p=6, keep=True, ai=where, why=why,
              err=dict(sol=sol, step=info[0], type=info[1], tempt=info[2], fix=fix),
              ap="Kさんの各行を自分で計算し直して比べる。乗法公式の形と，かっこの前の $-$ の扱いに特に注意する。",
              steps=[f"${showA}={tex(EA)}$。", f"${showB}={tex(EB)}$。", f"${tex(EA)}-({tex(EB)})={tex(res)}$。"],
              alt=["$x=1$ などを代入し，もとの式の値と各行の式の値を比べると，どこで値が変わったかがわかる。"],
              pc=[("誤りの行を正しく指摘している", 3), ("正しい答えを求めている", 3)],
              pit=["$(x+a)^2$ の $2ax$ を忘れる。", "かっこの前の $-$ を一部の項にしかかけない。"],
              chk=(f"({py(EA)})-({py(EB)})", py(res), "expand", "intermediate"))


FERR_POOL = {
    "incomplete": "かっこの中がまだ因数分解できるのに，途中で止めている。",
    "sign": "かっこの中の数の符号を誤っている。展開すると $x$ の係数の符号がもとの式と異なる。",
    "nofactor": "和の形の式を，和と差の積の形に因数分解している。展開すると符号が異なる。",
    "common": "共通因数でくくり出したとき，かっこの中の項を共通因数でわっていない。",
    "square": "平方の形の式を，和と差の積の形に因数分解している。展開しても真ん中の項が出てこない。",
}


@gen("error_correction", 3, ["common_error", "condition_check"])
def d_factor_err(r):
    kind = r.choice(list(FERR_POOL))
    if kind == "incomplete":
        g, b = r.choice([2, 3, 5]), r.randint(1, 6)
        q = f"{g}x^2-{g * b * b}"
        sol = f"${q}={g}(x^2-{b * b})$"
        fix = f"${g}(x+{b})(x-{b})$"
        ch = (f"{g}*(x+{b})*(x-{b})", f"{g}*x**2-{g * b * b}")
        etype = "concept"
    elif kind == "sign":
        m, n = r.sample(range(1, 9), 2)
        q = f"x^2-{m + n}x+{m * n}"
        sol = f"${q}=(x+{m})(x+{n})$"
        fix = f"$(x-{m})(x-{n})$"
        ch = (f"(x-{m})*(x-{n})", f"x**2-{m + n}*x+{m * n}")
        etype = "sign"
    elif kind == "nofactor":
        a = r.randint(2, 9)
        q = f"x^2+{a * a}"
        sol = f"${q}=(x+{a})(x-{a})$"
        fix = f"$x^2+{a * a}$ は（中学校の範囲では）これ以上因数分解できない。$(x+{a})(x-{a})=x^2-{a * a}$ である"
        ch = (f"(x+{a})*(x-{a})", f"x**2-{a * a}")
        etype = "concept"
    elif kind == "common":
        g, b = r.choice([2, 3, 4, 5]), r.randint(2, 9)
        q = f"{g}x^2+{g * b}x"
        sol = f"${q}={g}x(x+{g * b})$"
        fix = f"${g}x(x+{b})$"
        ch = (f"{g}*x*(x+{b})", f"{g}*x**2+{g * b}*x")
        etype = "calculation"
    else:
        a = r.randint(2, 9)
        q = f"x^2-{2 * a}x+{a * a}"
        sol = f"${q}=(x+{a})(x-{a})$"
        fix = f"$(x-{a})^2$"
        ch = (f"(x-{a})**2", f"x**2-{2 * a}*x+{a * a}")
        etype = "formula"
    right = FERR_POOL[kind]
    cands = [(t, "Kさんの解答にはこの誤りはない。展開して，もとの式と比べると誤りの場所がわかる。", "誤りの種類の取り違え") for k, t in FERR_POOL.items() if k != kind]
    r.shuffle(cands)
    cands = cands[:2] + [("Kさんの解答に誤りはない。", "Kさんの答えを展開しても，もとの式にならない（または因数分解が最後まで行われていない）。", "検算不足")]
    stem = f"〔問題〕${q}$ を因数分解しなさい。\n〔Kさんの解答〕\n{sol}\nKさんの解答の誤りを説明したものとして最も適するものを，" + SEL4
    return MC(stem, right, cands, f"正しくは {fix}。", d=3, p=6,
              err=dict(sol=sol, step="因数分解の結果", type=etype, tempt="公式の形を急いで決めたり，途中の形で満足したりしやすい。", fix=fix),
              ap="Kさんの答えを展開して，もとの式にもどるかを調べる。もどっていても，まだ因数分解できる部分が残っていないかを確かめる。",
              steps=["Kさんの答えを展開してもとの式と比べる。", right, f"正しくは {fix}。"],
              alt=["$x$ に数を代入して，もとの式とKさんの答えの値が等しいかを調べる。"],
              pc=[("誤りの理由を正しく指摘している", 3), ("正しく因数分解している", 3)],
              pit=["符号を確かめずに公式にあてはめる。", "共通因数をくくり出したところで止める。"],
              chk=ch + ("expand", "intermediate"))


MERR = {
    "minus": "かっこの前の $-$ を，かっこの中のすべての項にかけていない。",
    "sq": "$(x-b)^2$ の展開で，真ん中の項 $-2bx$ を忘れている。",
    "sqsign": "$(x-b)^2$ の展開で，最後の項 $b^2$ の符号を $-$ にしている。",
    "dist": "$x(x+a)$ の展開で，$x$ を $a$ にかけ忘れている。",
}


@gen("error_correction", 3, ["common_error", "computation"])
def d_minus_err(r):
    a = r.randint(1, 9)
    b = r.randint(1, 9)
    kind = r.choice(list(MERR))
    X = P((1, 1, 0))
    A = mul(X, lin(1, a))
    B = mul(lin(1, -b), lin(1, -b))
    res = add(A, sc(B, -1))
    if kind == "minus":
        KA, KB = A, B
        seq = terms(KA) + [(-B[(2, 0)], 2, 0), (B[(1, 0)], 1, 0), (B[(0, 0)], 0, 0)]
    elif kind == "sq":
        KA, KB = A, P((1, 2, 0), (b * b, 0, 0))
        seq = terms(KA) + [(-c_, i, j) for c_, i, j in terms(KB)]
    elif kind == "sqsign":
        KA, KB = A, P((1, 2, 0), (-2 * b, 1, 0), (-b * b, 0, 0))
        seq = terms(KA) + [(-c_, i, j) for c_, i, j in terms(KB)]
    else:
        KA, KB = P((1, 2, 0), (a, 0, 0)), B
        seq = terms(KA) + [(-c_, i, j) for c_, i, j in terms(KB)]
    kres = P(*seq)
    assert kres != res
    sol = f"$x(x+{a})-(x-{b})^2$\n$={terms_tex(seq)}$\n$={tex(kres)}$"
    right = MERR[kind]
    cands = [(t, "Kさんの解答にはこの誤りはない。各項を1つずつ確かめると，誤りは別の場所にある。", "誤りの箇所の取り違え") for k, t in MERR.items() if k != kind]
    r.shuffle(cands)
    cands = cands[:2] + [("Kさんの解答に誤りはない。", f"正しく計算すると ${tex(res)}$ となり，Kさんの答えと異なる。", "検算不足")]
    fix = f"$x^2+{a}x-(x^2-{2 * b}x+{b * b})={tex(res)}$"
    return MC(f"〔問題〕$x(x+{a})-(x-{b})^2$ を計算しなさい。\n〔Kさんの解答〕\n{sol}\nKさんの解答の誤りを説明したものとして最も適するものを，" + SEL4,
              right, cands, f"正しくは {fix}。", d=3, p=6,
              err=dict(sol=sol, step="2行目の展開・かっこのはずし方", type="sign" if kind in ("minus", "sqsign") else ("formula" if kind == "sq" else "calculation"),
                       tempt="展開とかっこはずしを同時に行うと，符号や項を見落としやすい。", fix=fix),
              ap="$(x-b)^2$ をまずかっこつきで展開してから，かっこの前の $-$ ですべての項の符号を変える。Kさんの2行目の各項と比べる。",
              steps=[f"$x(x+{a})=x^2+{a}x$。", f"$(x-{b})^2=x^2-{2 * b}x+{b * b}$。", f"$x^2+{a}x-(x^2-{2 * b}x+{b * b})=x^2+{a}x-x^2+{2 * b}x-{b * b}={tex(res)}$。"],
              alt=["$x=1$ を代入して，もとの式とKさんの答えの値を比べる。"],
              pc=[("誤りの内容を正しく指摘している", 3), ("正しい答えを求めている", 3)],
              pit=["かっこの前の $-$ を一部の項にしかかけない。", "$(x-b)^2$ の真ん中の項を忘れる。"],
              chk=(f"x*(x+{a})-(x-{b})**2", py(res), "expand", "intermediate"))


GENERATORS = [a_expand, a_factor, a_coef, a_concept,
              b_simplify, b_factor2, b_trick, b_value,
              c_proof_fill, c_path, c_xy_judge,
              d_line_err, d_factor_err, d_minus_err]
GENERATORS = [robust(g) for g in GENERATORS]
