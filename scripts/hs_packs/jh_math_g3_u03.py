"""単元パック：中学3年 二次方程式（神奈川県公立高校入試形式）。"""
import math
import re
import unicodedata
from fractions import Fraction as Fr

from banks._common import figure, mc, num, shape
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, poly, summary, theorem, tp)

UNIT_ID = "JH-MATH-G3-U03"

PREREQUISITES = [
    ("JH-MATH-G3-U01", "乗法公式と因数分解ができること。$x^2+bx+c=0$ を $(x-p)(x-q)=0$ と因数分解して解くときや、平方完成で使う。"),
    ("JH-MATH-G3-U02", "平方根の意味と根号の計算ができること。$x^2=k$ の解 $\\pm\\sqrt{k}$ や、解の公式の答えを簡単にするときに使う。"),
    ("JH-MATH-G1-U03", "一次方程式の解き方と、方程式を使って文章題を解く手順（数量を文字でおく・解を確かめる）。"),
]
EXTENSIONS = [
    ("JH-MATH-G3-U04", "関数 $y=ax^2$ で、$y$ の値から $x$ の値を求めたり、放物線と直線の交点を求めたりするときに二次方程式を解く。"),
    ("JH-MATH-G3-U07", "三平方の定理で辺の長さを文字でおくと、二次方程式を解いて長さを求める問題になる。"),
    ("HS-MATH1-U03", "高校の二次関数で、判別式 $D=b^2-4ac$ による解の個数の判定や、二次不等式へ発展する。"),
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
    a, b, k = 1, n, 2
    while k * k <= b:
        while b % (k * k) == 0:
            b //= k * k
            a *= k
        k += 1
    return a, b


def is_sq(n):
    return n >= 0 and math.isqrt(n) ** 2 == n


def MARK(stem, v, e, expr, **kw):
    """あいう方式（0〜9 のマーク）で答える数値問題。v は 0 以上の整数か既約分数。"""
    v = Fr(v)
    assert v >= 0
    if v.denominator == 1:
        n = int(v)
        return num(stem, str(n), e, mark=("int", n), chk=(expr, str(n), None, "answer"), **kw)
    p, q = v.numerator, v.denominator
    return num(stem, f"${ftex(v)}$", e, mark=("frac", p, q), chk=(expr, f"Rational({p},{q})", None, "answer"), **kw)


def EQ(a, b, c):
    return f"{poly(a, b, c)}=0"


def xs(*vals):
    """有理数の解の表記（小さい順、重解は1つ）。"""
    vs = sorted(set(Fr(v) for v in vals))
    return "$" + ",\\ ".join(f"x={ftex(v)}" for v in vs) + "$"


def lin(c, k):
    """x+k の形（係数 c は 1 のみ想定）。"""
    return "x" if k == 0 else f"x{'+' if k > 0 else '-'}{abs(k)}"


def sq_term(s, d):
    if d == 1:
        return str(s)
    return f"{'' if s == 1 else s}\\sqrt{{{d}}}"


def qf(B, s, d, den):
    """x=(B±s√d)/den を約分した表記。d=1 のときは有理数の2解。"""
    if d == 1:
        return xs(Fr(B + s, den), Fr(B - s, den))
    g = math.gcd(math.gcd(abs(B), s), abs(den))
    B, s, den = B // g, s // g, den // g
    if den < 0:
        B, den = -B, -den
    pm = f"\\pm{sq_term(s, d)}"
    if den == 1:
        return f"$x={'' if B == 0 else B}{pm}$"
    top = f"{'' if B == 0 else B}{pm}"
    return f"$x=\\dfrac{{{top}}}{{{den}}}$"


def qf_py(B, s, d, den):
    return f"({B}+{s}*sqrt({d}))/({den})"


def formula_parts(a, b, c):
    D = b * b - 4 * a * c
    s, d = sqf(D)
    return D, s, d


def formula_cands(a, b, c):
    """解の公式の典型的な誤答 [(文, 理由, 誤概念)]。"""
    D, s, d = formula_parts(a, b, c)
    out = [(qf(-b, s, d, a) if a != 1 else None, "分母を $2a$ でなく $a$ にしている。", "解の公式の覚え違い"),
           (qf(b, s, d, 2 * a) if b else None, "分子の $-b$ の符号を誤っている。$b$ が負のとき $-b$ は正になる。", "符号の誤り")]
    D2 = b * b + 4 * a * c
    if D2 > 0 and not is_sq(D2) and D2 != D:
        s2, d2 = sqf(D2)
        out.append((qf(-b, s2, d2, 2 * a), "根号の中を $b^2+4ac$ と計算している。$c$ が負のときの符号に注意する。", "符号の誤り"))
    g = math.gcd(b, 2 * a)
    if s > 1 or g > 1:
        out.append((f"$x={ftex(Fr(-b, 2 * a))}\\pm{sq_term(s, d)}$", "分子の $-b$ だけを分母でわり、根号の項をわっていない。", "約分の誤り"))
    D3 = b * b - a * c
    if a > 1 and D3 > 0 and not is_sq(D3) and D3 != D:
        s3, d3 = sqf(D3)
        out.append((qf(-b, s3, d3, 2 * a), "根号の中の $4ac$ の $4$ を落としている。", "解の公式の覚え違い"))
    if a > 1:
        out.append((qf(-b, s, d, 2), "分母を $2a$ でなく $2$ にしている。", "解の公式の覚え違い"))
    D4 = -b * b - 4 * a * c
    if D4 > 0 and not is_sq(D4):
        s4, d4 = sqf(D4)
        out.append((qf(-b, s4, d4, 2 * a), "$b^2$ を $-b^2$ と計算している。負の数の2乗は正。", "累乗の符号の誤り"))
    return out


SEL4 = "次の1〜4の中から1つ選び，その番号を答えなさい。"


def _robust(g):
    """選択肢が重複して誤答が足りないパラメータのときは、同じ乱数列から別のパラメータを引き直す。"""
    import random as _random
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


def _nz(r, lo, hi):
    return r.choice([v for v in range(lo, hi + 1) if v])


# ----------------------------------------------------------------------
# 授業プリント
# ----------------------------------------------------------------------

_ROAD_FIG = figure("縦 12 m、横 20 m の長方形の土地に、同じ幅 x m の道を縦と横に1本ずつつくった図",
                   shape({"A": (0, 6), "B": (0, 0), "C": (10, 0), "D": (10, 6), "E": (4, 6), "F": (4, 0), "G": (5, 6), "H": (5, 0),
                          "I": (0, 3), "J": (10, 3), "K": (0, 2), "L": (10, 2)},
                         labels={}, segments=[("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("E", "F"), ("G", "H"), ("I", "J"), ("K", "L")],
                         texts=[(4.1, 6.3, "x m"), (-1.6, 2.3, "x m"), (4.6, -0.8, "20 m"), (10.3, 3.2, "12 m")], scale=16))

LESSON = lesson(
    goals=["二次方程式の意味とその解の意味を理解し、因数分解・平方根の考え・解の公式を使って二次方程式を解くことができる。",
           "$AB=0$ ならば $A=0$ または $B=0$ であることや、平方完成から解の公式が導かれることを説明できる。",
           "身のまわりの問題を二次方程式を使って解き、求めた解が問題に適しているかを確かめることができる。"],
    duration=100,
    readiness=["乗法公式による展開と、因数分解（共通因数・和と積・平方の公式・和と差の公式）ができる。",
               "平方根の意味（$x^2=a$ をみたす $x$ は $\\pm\\sqrt{a}$）と、根号をふくむ数を簡単にする計算ができる。",
               "一次方程式を解き、文章題で数量を文字で表して方程式をつくることができる。"],
    flow=[("導入：道の幅を求める", 10, "長方形の土地に道をつくる問題から、$x^2$ をふくむ方程式が必要になることに気づく"),
          ("二次方程式と解の意味", 10, "二次方程式・解の定義、$x$ に値を代入して解かどうかを確かめる"),
          ("因数分解による解き方", 20, "$AB=0$ の性質と、因数分解による解き方（例題1）"),
          ("平方根の考えと平方完成", 20, "$x^2=k$、$(x+p)^2=q$ の形の解き方、平方完成（例題2）"),
          ("解の公式", 20, "平方完成から解の公式を導き、使う（例題3）"),
          ("二次方程式の利用とまとめ", 20, "道の幅の問題を解き、解の吟味をする（例題4）。確認問題")],
    sections=[
        intro("in1", "道の幅はどれだけにすればよい？",
              "縦 $12$ m、横 $20$ m の長方形の土地に、右の図のように同じ幅の道を縦と横に1本ずつつくり、残りを花だんにする。花だんの面積を $180$ m² にするには、道の幅を何 m にすればよいだろうか。道の幅を $x$ m とすると、道をはしに寄せて考えれば、花だんは縦 $(12-x)$ m、横 $(20-x)$ m の長方形と同じ面積になるので、$(12-x)(20-x)=180$ という方程式ができる。",
              bullets=["左辺を展開すると $x^2-32x+240=180$。$x^2$ の項がある方程式になる。", "これまでの一次方程式の解き方だけでは解けない。新しい解き方が必要になる。"],
              figure=_ROAD_FIG,
              points=[tp("道を土地のはしに寄せた図をかかせ、花だんの部分が1つの長方形にまとまることを確認する。", ask="花だんの縦と横の長さを $x$ を使って表すとどうなるか。", expect="縦 $12-x$、横 $20-x$。", timing="導入の最初"),
                      tp("この問題は例題4で解くことを予告し、授業の最後にもどってくる見通しをもたせる。")]),
        definition("df1", "二次方程式とその解",
                   "移項して整理すると $ax^2+bx+c=0$（$a$、$b$、$c$ は定数、$a\\neq0$）の形になる方程式を、$x$ についての二次方程式という。二次方程式を成り立たせる $x$ の値を、その二次方程式の解といい、解をすべて求めることを二次方程式を解くという。",
                   formula="$$ax^2+bx+c=0\\qquad(a\\neq0)$$",
                   conditions=["二次方程式の解は、ふつう2つある。$(x-3)^2=0$ のように解が1つの場合もある。",
                               "ある値が解かどうかは、方程式に代入して（左辺）＝（右辺）になるかで確かめられる。",
                               "式を整理したとき $x^2$ の項が消えれば一次方程式である。"],
                   points=[tp("$x=1,\\,2,\\,3,\\,\\cdots$ を $x^2-5x+6=0$ に順に代入させ、解が2つあることを発見させる。", ask="$x=2$ と $x=3$ のほかに解はあるか。", expect="見つからない。2つだけかもしれない。", caution="「解は必ず2つ」と思いこませないよう、重解の例も早めに示す。")]),
        theorem("th1", "因数分解による解き方の根拠",
                "$$AB=0\\ \\text{ならば}\\ A=0\\ \\text{または}\\ B=0$$",
                ["2つの数 $A$、$B$ の積が $0$ のとき、少なくとも一方は $0$ である。", "積が $0$ 以外の数（たとえば $AB=6$）のときには、この性質は使えない。",
                 "$(x-p)(x-q)=0$ ならば $x-p=0$ または $x-q=0$ なので、解は $x=p,\\ x=q$。"],
                body="$A\\neq0$ のとき、$AB=0$ の両辺を $A$ でわると $B=0$ となる。つまり、$A$ が $0$ でなければ $B$ が $0$ である。したがって $A=0$ または $B=0$ である。",
                points=[tp("$(x-2)(x-3)=2$ を「$x-2=2$ または $x-3=2$」としてしまう誤りを示し、右辺が $0$ であることが大切だと強調する。", ask="$x-2=2$ から得た $x=4$ を代入すると成り立つか。", expect="$2\\times1=2$ で成り立つが、$x-3=2$ からの $x=5$ は $3\\times2=6$ で成り立たない。")]),
        derivation("dv1", "平方完成から解の公式を導く",
                   ["$ax^2+bx+c=0$（$a\\neq0$）の両辺を $a$ でわる：$x^2+\\dfrac{b}{a}x+\\dfrac{c}{a}=0$。",
                    "定数項を移項する：$x^2+\\dfrac{b}{a}x=-\\dfrac{c}{a}$。",
                    "両辺に $x$ の係数の半分の2乗 $\\left(\\dfrac{b}{2a}\\right)^2$ を加える：$x^2+\\dfrac{b}{a}x+\\left(\\dfrac{b}{2a}\\right)^2=\\dfrac{b^2}{4a^2}-\\dfrac{c}{a}$。",
                    "左辺を $(x+\\cdots)^2$ の形にし、右辺を通分する：$\\left(x+\\dfrac{b}{2a}\\right)^2=\\dfrac{b^2-4ac}{4a^2}$。",
                    "$b^2-4ac\\geqq0$ のとき、平方根を考えて $x+\\dfrac{b}{2a}=\\pm\\dfrac{\\sqrt{b^2-4ac}}{2a}$。",
                    "$\\dfrac{b}{2a}$ を移項して、解の公式 $x=\\dfrac{-b\\pm\\sqrt{b^2-4ac}}{2a}$ が得られる。"],
                   body="具体的な方程式 $x^2+6x+2=0$ でも同じ手順をたどれる：$x^2+6x=-2$、$x^2+6x+9=-2+9$、$(x+3)^2=7$、$x=-3\\pm\\sqrt{7}$。",
                   points=[tp("先に数字の例（$x^2+6x+2=0$）で平方完成を行い、同じ手順を文字で行うと公式になる、という順で示す。", caution="「両辺に同じ数を加える」ことを忘れ、左辺だけに加える誤りが多い。", timing="解の公式を示す前")]),
        theorem("th2", "二次方程式の解の公式",
                "$$ax^2+bx+c=0\\ \\text{の解は}\\quad x=\\dfrac{-b\\pm\\sqrt{b^2-4ac}}{2a}$$",
                ["$a\\neq0$。根号の中 $b^2-4ac$ が負の数のときは、中学校で扱う数の範囲には解がない。", "答えは、根号の中をできるだけ小さい自然数にし、約分できるときは約分する。",
                 "因数分解できる方程式は因数分解で、$x^2=k$・$(x+p)^2=q$ の形は平方根の考えで解く方が速い。"],
                points=[tp("$2x^2+3x-1=0$ で $a=2$、$b=3$、$c=-1$ を確認してから代入させる。負の数はかっこをつけて代入する習慣をつける。", ask="$b^2-4ac$ の値はいくつか。", expect="$9-4\\times2\\times(-1)=17$。")]),
        example("ex1", "例題1　因数分解で解く",
                "二次方程式 $x^2-2x-15=0$ と $x^2=6x$ を解きなさい。",
                ["$x^2-2x-15=(x+3)(x-5)$ なので $(x+3)(x-5)=0$。$x+3=0$ または $x-5=0$ より $x=-3,\\ x=5$。",
                 "$x^2=6x$ は $x^2-6x=0$ と移項して、$x(x-6)=0$。$x=0,\\ x=6$。"],
                "$x=-3,\\ x=5$／$x=0,\\ x=6$",
                thinking="右辺を $0$ にして左辺を因数分解する。$x^2=6x$ を $x$ でわってはいけない。",
                points=[tp("$x^2=6x$ の両辺を $x$ でわって $x=6$ とする誤りをわざと示し、$x=0$ も解であることを代入で確かめさせる。")],
                misconceptions=[("$x^2=6x$ の両辺を $x$ でわって $x=6$", "$x=0$ のときは $x$ でわれないので、移項して因数分解し $x=0,\\ x=6$")]),
        example("ex2", "例題2　平方根の考えで解く",
                "二次方程式 $3x^2=24$ と $(x-2)^2=5$ を解きなさい。",
                ["$3x^2=24$ の両辺を $3$ でわって $x^2=8$。$x=\\pm\\sqrt{8}=\\pm2\\sqrt{2}$。",
                 "$(x-2)^2=5$ より $x-2=\\pm\\sqrt{5}$。$x=2\\pm\\sqrt{5}$。"],
                "$x=\\pm2\\sqrt{2}$／$x=2\\pm\\sqrt{5}$",
                thinking="（ある式）$^2=k$ の形なら、その式は $k$ の平方根 $\\pm\\sqrt{k}$ に等しい。",
                points=[tp("$(x-2)^2=5$ を展開してから解の公式で解いても同じ答えになることを示し、形を見て解き方を選ぶよさを感じさせる。")]),
        example("ex3", "例題3　解の公式で解く",
                "二次方程式 $2x^2+3x-1=0$ と $x^2+4x+1=0$ を解きなさい。",
                ["$a=2$、$b=3$、$c=-1$ を代入：$x=\\dfrac{-3\\pm\\sqrt{3^2-4\\times2\\times(-1)}}{2\\times2}=\\dfrac{-3\\pm\\sqrt{17}}{4}$。",
                 "$a=1$、$b=4$、$c=1$：$x=\\dfrac{-4\\pm\\sqrt{16-4}}{2}=\\dfrac{-4\\pm2\\sqrt{3}}{2}=-2\\pm\\sqrt{3}$。"],
                "$x=\\dfrac{-3\\pm\\sqrt{17}}{4}$／$x=-2\\pm\\sqrt{3}$",
                thinking="係数 $a$、$b$、$c$ を符号もふくめて読みとって代入する。最後に根号の中を簡単にし、約分する。",
                points=[tp("約分するときは分子の各項をすべて同じ数でわること（$-4$ と $2\\sqrt{3}$ の両方を $2$ でわる）を確認する。", caution="$\\dfrac{-4\\pm2\\sqrt{3}}{2}=-2\\pm2\\sqrt{3}$ とする誤りが多い。")]),
        example("ex4", "例題4　二次方程式の利用（解の吟味）",
                "導入の問題で、花だんの面積を $180$ m² にするための道の幅を求めなさい。",
                ["$(12-x)(20-x)=180$ を展開して整理すると $x^2-32x+60=0$。", "$(x-2)(x-30)=0$ より $x=2,\\ x=30$。",
                 "道の幅は土地の縦の長さ $12$ m より短いので $0<x<12$。$x=30$ は問題に適さない。", "道の幅は $2$ m。"],
                "$2$ m",
                thinking="方程式の解がそのまま答えになるとは限らない。$x$ の値の範囲を考えて、問題に適するかを確かめる。",
                points=[tp("$x=30$ のとき花だんの縦が $12-30=-18$ m になることを確認させ、解の吟味の必要性を実感させる。", ask="$x=30$ はなぜ答えにならないのか。", expect="道の幅が土地より広くなってしまうから。")]),
        board("bd1", "板書案",
              [("① 二次方程式と解", ["$ax^2+bx+c=0$（$a\\neq0$）", "解：方程式を成り立たせる $x$ の値", "$AB=0\\Rightarrow A=0$ または $B=0$", "$x^2-2x-15=0\\to(x+3)(x-5)=0$", "$x=-3,\\ x=5$"]),
               ("② 平方根・平方完成", ["$x^2=k\\to x=\\pm\\sqrt{k}$", "$(x+p)^2=q\\to x=-p\\pm\\sqrt{q}$", "$x^2+6x+2=0$", "$x^2+6x+9=-2+9$", "$(x+3)^2=7$、$x=-3\\pm\\sqrt{7}$"]),
               ("③ 解の公式と利用", ["$x=\\dfrac{-b\\pm\\sqrt{b^2-4ac}}{2a}$", "約分は分子の全部の項で", "利用：式をつくる→解く→吟味", "$x=2,\\ 30$ → $0<x<12$ より $2$ m"])],
              points=[tp("②の平方完成は、両辺に加える $9$ を色チョークで示し、左右で同じ数を加えていることを強調する。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("どの解き方を使うかの判断を毎回言わせる（因数分解できるか → $(\\ )^2=k$ の形か → 解の公式）。", ask="$x^2-7x=0$ はどの方法で解くか。", expect="共通因数 $x$ でくくって因数分解。"),
               tp("両辺を $x$ でわると解 $x=0$ を失うことを、代入による確かめで納得させる。", caution="入試でも頻出の誤り。"),
               tp("解の公式では、$b$ や $c$ が負のときにかっこをつけて代入させる。$-b$ の符号の誤りを防ぐ。", timing="例題3のあと"),
               tp("文章題では、最後に「$x$ の範囲」「自然数か」「長さは正か」などの条件で解を吟味し、答えに単位をつけさせる。")],
              misconceptions=[("$(x-2)(x-3)=2$ なので $x-2=2$ または $x-3=2$", "右辺が $0$ でないので、展開して $x^2-5x+4=0$ に直してから解く"),
                              ("$x^2=9$ の解は $x=3$", "$x=\\pm3$。負の数も2乗すると $9$ になる"),
                              ("$\\dfrac{-4\\pm2\\sqrt{3}}{2}=-2\\pm2\\sqrt{3}$", "分子のすべての項を $2$ でわって $-2\\pm\\sqrt{3}$")]),
        summary("sm1", "まとめ",
                ["二次方程式は $ax^2+bx+c=0$（$a\\neq0$）の形に整理できる方程式。解はふつう2つ。",
                 "因数分解できるときは、$AB=0$ ならば $A=0$ または $B=0$ を使って解く。",
                 "$x^2=k$、$(x+p)^2=q$ の形は平方根の考えで解く。平方完成でこの形に直せる。",
                 "解の公式 $x=\\dfrac{-b\\pm\\sqrt{b^2-4ac}}{2a}$ は平方完成から導かれ、どんな二次方程式にも使える。",
                 "文章題では、求めた解が問題に適しているかを必ず確かめる。"]),
        check("ck1", "確認問題",
              [("二次方程式 $x^2+x-12=0$ を解きなさい。", "$(x+4)(x-3)=0$ より $x=-4,\\ x=3$"),
               ("二次方程式 $(x+1)^2=6$ を解きなさい。", "$x=-1\\pm\\sqrt{6}$"),
               ("二次方程式 $x^2-3x+1=0$ を解きなさい。", "$x=\\dfrac{3\\pm\\sqrt{5}}{2}$"),
               ("連続する2つの自然数の積が $56$ のとき、小さい方の数を求めなさい。", "$x(x+1)=56$ より $x=7,\\ -8$。自然数なので $7$")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

@gen("basic_check", 4, ["computation"])
def a_factor_solve(r):
    kind = r.choice(["two", "two", "zero", "double"])
    if kind == "two":
        p, q = r.sample([v for v in range(-9, 10) if v], 2)
        b, c = -(p + q), p * q
        roots = (p, q)
        fact = f"({lin(1, -p)})({lin(1, -q)})"
        cands = [(xs(-p, -q), "因数分解した式の数をそのまま解にして、符号を逆にしている。$x-p=0$ から $x=p$。", "符号の誤り"),
                 (xs(-p, q), "片方の解の符号を誤っている。", "符号の誤り"),
                 (xs(p, -q), "片方の解の符号を誤っている。", "符号の誤り"),
                 (xs(b, c) if (b, c) != (p, q) else None, "$x$ の係数と定数項をそのまま解にしている。", "因数分解の意味の誤解")]
    elif kind == "zero":
        p = _nz(r, -9, 9)
        b, c = -p, 0
        roots = (0, p)
        fact = f"x({lin(1, -p)})"
        cands = [(xs(p), "両辺を $x$ でわってしまい、$x=0$ の解を落としている。", "解の見落とし"),
                 (xs(0, -p), "$x-p=0$ の解の符号を誤っている。", "符号の誤り"),
                 (xs(-p), "$x=0$ を落とし、さらに符号も誤っている。", "解の見落とし")]
    else:
        p = _nz(r, -8, 8)
        b, c = -2 * p, p * p
        roots = (p,)
        fact = f"({lin(1, -p)})^2"
        cands = [(xs(-p), "符号を誤っている。$(x-p)^2=0$ の解は $x=p$。", "符号の誤り"),
                 (xs(p, -p), "解は $x=p$ の1つだけなのに、$-p$ も解としている。", "重解の意味の誤解"),
                 (xs(p * p), "定数項をそのまま解にしている。", "因数分解の意味の誤解"),
                 (xs(-2 * p), "$x$ の係数をもとに答えている。", "因数分解の意味の誤解")]
    eq = EQ(1, b, c)
    return MC(f"二次方程式 ${eq}$ を解いた結果として正しいものを，" + SEL4, xs(*roots), cands,
              f"${eq}$ の左辺を因数分解すると ${fact}=0$。よって {xs(*roots)}。", d=2,
              ap="左辺を因数分解して $AB=0$ の形にし、「$A=0$ または $B=0$」を使う。",
              steps=[f"左辺を因数分解する：${fact}=0$。", "それぞれの因数が $0$ になる $x$ を求める。", f"{xs(*roots)}。"],
              alt=["求めた解をもとの方程式に代入して、左辺が $0$ になることを確かめる。"],
              pc=[("正しく因数分解している", 1), ("解を正しく求めている", 1)],
              pit=["$(x+3)(x-5)=0$ から $x=3,\\ x=-5$ と符号を逆にする。", "$x^2=6x$ の両辺を $x$ でわって $x=0$ を落とす。"],
              chk=(f"expand({fact.replace('^2', '**2').replace(')(', ')*(').replace('x(', 'x*(')})", f"x**2+({b})*x+({c})", None, "intermediate"))


def _surd_tex(c, b):
    """c√b（c は正の有理数）の表記。"""
    c = Fr(c)
    if b == 1:
        return ftex(c)
    if c.denominator == 1:
        return f"{'' if c == 1 else c.numerator}\\sqrt{{{b}}}"
    return f"\\dfrac{{{'' if c.numerator == 1 else c.numerator}\\sqrt{{{b}}}}}{{{c.denominator}}}"


def _sqrt_of(q):
    """正の有理数 q の正の平方根を c√b（b はできるだけ小さい自然数、分母は有理化）で返す。"""
    q = Fr(q)
    n, d = q.numerator, q.denominator
    a, b = sqf(n * d)
    return Fr(a, d), b


@gen("basic_check", 4, ["computation", "condition_check"])
def a_sqrt_solve(r):
    kind = r.choice(["ax2", "ax2", "shift", "shift"])
    if kind == "ax2":
        a = r.randint(2, 6)
        q = r.choice([Fr(v) for v in (2, 3, 5, 6, 7, 8, 12, 18, 20, 24, 27, 45, 50)] + [Fr(p, a) for p in (1, 2, 3, 5, 6, 7) if Fr(p, a).denominator > 1])
        c = q * a
        assert c.denominator == 1
        cc, bb = _sqrt_of(q)
        root = _surd_tex(cc, bb)
        form = r.choice(["eq", "minus"])
        eq = f"{a}x^2={c}" if form == "eq" else f"{a}x^2-{c}=0"
        right = f"$x=\\pm{root}$"
        cands = [(f"$x={root}$", "正の方の解だけを答えている。$x^2=k$ をみたす $x$ は $\\pm\\sqrt{k}$ の2つ。", "解の見落とし"),
                 (f"$x=\\pm{_surd_tex(*_sqrt_of(c))}$", f"両辺を ${a}$ でわるのを忘れている。", "等式の変形の誤り"),
                 (f"$x=\\pm{ftex(q)}$", "平方根をとらずに $x^2$ の値をそのまま答えている。", "平方根の意味の誤解"),
                 (f"$x=\\pm\\dfrac{{\\sqrt{{{c}}}}}{{{a}}}$" if not is_sq(int(c)) else None, f"$x^2=\\dfrac{{{c}}}{{{a}}}$ の平方根を $\\dfrac{{\\sqrt{{{c}}}}}{{{a}}}$ としている。分母の ${a}$ にも根号が必要。", "平方根の計算の誤り")]
        e = f"$x^2={ftex(q)}$ なので $x=\\pm\\sqrt{{{ftex(q)}}}=\\pm{root}$。"
        steps = [f"両辺を ${a}$ でわる：$x^2={ftex(q)}$。", f"$x=\\pm\\sqrt{{{ftex(q)}}}$。", f"根号の中を簡単にして（必要なら有理化して）$x=\\pm{root}$。"]
        chk = (f"{a}*({cc.numerator}*sqrt({bb})/{cc.denominator})**2", str(c), None, "intermediate")
    else:
        p = _nz(r, -6, 6)
        if r.random() < 0.4:
            t = r.randint(1, 6)
            q = t * t
            right = xs(-p + t, -p - t)
            cands = [(xs(p + t, p - t), "かっこの中の数の符号を誤っている。$x+p=\\pm t$ から $x=-p\\pm t$。", "符号の誤り"),
                     (xs(-p + t), "正の平方根だけを考え、もう1つの解を落としている。", "解の見落とし"),
                     (xs(-p + q, -p - q), "平方根をとらずに右辺の数をそのまま使っている。", "平方根の意味の誤解"),
                     (xs(p + t), "符号を誤り、もう1つの解も落としている。", "解の見落とし")]
        else:
            q = r.choice([2, 3, 5, 6, 7, 8, 12, 18, 20, 24, 27])
            s, d = sqf(q)
            rt = sq_term(s, d)
            right = f"$x={-p}\\pm{rt}$"
            cands = [(f"$x={p}\\pm{rt}$", "かっこの中の数の符号を誤っている。移項すると符号が変わる。", "符号の誤り"),
                     (f"$x={-p}+{rt}$", "正の平方根だけを考え、もう1つの解を落としている。", "解の見落とし"),
                     (f"$x={-p}\\pm{q}$", "平方根をとらずに右辺の数をそのまま使っている。", "平方根の意味の誤解"),
                     (f"$x=\\pm{sq_term(*sqf(q + p * p))}$" if not is_sq(q + p * p) else None, "左辺のかっこを無視して計算している。", "式の形の読み違い")]
        eq = f"({lin(1, p)})^2={q}"
        e = f"${lin(1, p)}=\\pm\\sqrt{{{q}}}$ より，{right}。"
        steps = [f"${lin(1, p)}$ を1つのまとまりとみて、${lin(1, p)}=\\pm\\sqrt{{{q}}}$。", f"${p}$ を移項する。", f"{right}。"]
        chk = (f"({-p}+sqrt({q})+({p}))**2", str(q), None, "intermediate")
    return MC(f"二次方程式 ${eq}$ を解いた結果として正しいものを，" + SEL4, right, cands, e, d=2,
              ap="（ある式）$^2=k$ の形なら、平方根の考えで「その式 $=\\pm\\sqrt{k}$」とする。展開する必要はない。",
              steps=steps, alt=["展開して $ax^2+bx+c=0$ の形に整理し、解の公式で解いても同じ答えになる。"],
              pc=[("平方根の考えを使っている", 1), ("$\\pm$ を忘れずに正しく解いている", 1)],
              pit=["$\\pm$ を忘れて解を1つしか書かない。", "移項したときの符号を誤る。"], chk=chk)


def _formula_eq(r, max_a=3):
    for _ in range(200):
        a = r.randint(1, max_a)
        b = r.randint(-7, 7)
        c = _nz(r, -6, 6)
        D = b * b - 4 * a * c
        if D > 0 and not is_sq(D) and D <= 120 and b != 0:
            return a, b, c
    raise AssertionError("no equation")


@gen("basic_check", 4, ["computation"])
def a_formula(r):
    a, b, c = _formula_eq(r)
    D, s, d = formula_parts(a, b, c)
    right = qf(-b, s, d, 2 * a)
    eq = EQ(a, b, c)
    return MC(f"二次方程式 ${eq}$ を解いた結果として正しいものを，" + SEL4, right, formula_cands(a, b, c),
              f"解の公式に $a={a}$，$b={b}$，$c={c}$ を代入して $x=\\dfrac{{{-b}\\pm\\sqrt{{{D}}}}}{{{2 * a}}}$。整理して {right}。", d=2,
              ap="因数分解できないので解の公式を使う。$a$、$b$、$c$ を符号もふくめて読みとる。",
              steps=[f"$a={a}$，$b={b}$，$c={c}$。", f"$b^2-4ac={par(b)}^2-4\\times{a}\\times{par(c)}={D}$。",
                     f"$x=\\dfrac{{{-b}\\pm\\sqrt{{{D}}}}}{{{2 * a}}}$。", f"根号の中を簡単にし、約分して {right}。"],
              alt=["求めた解の近似値を方程式に代入して、左辺がほぼ $0$ になるかを確かめる。"],
              pc=[("解の公式に正しく代入している", 1), ("根号・約分を正しく整理している", 1)],
              pit=["分母を $a$ にする。", "$-b$ の符号を誤る。", "約分で根号の項をわり忘れる。"],
              chk=(f"{a}*({qf_py(-b, s, d, 2 * a)})**2+({b})*({qf_py(-b, s, d, 2 * a)})+({c})", "0", None, "intermediate"))


@gen("basic_check", 4, ["concept", "condition_check"])
def a_is_solution(r):
    k = _nz(r, -6, 6)
    m = r.choice([v for v in range(-6, 7) if v not in (k, -k)])
    right_eq = EQ(1, -(k + m), k * m)
    wrongs = []
    m2 = r.choice([v for v in range(-6, 7) if v not in (k, -k)])
    wrongs.append((1, k - m2, -k * m2))  # 解は -k, m2（符号のわな）
    for _ in range(40):
        if len(wrongs) == 3:
            break
        p, q = r.sample([v for v in range(-7, 8) if v != k], 2)
        cand = (1, -(p + q), p * q)
        if cand not in wrongs and cand != (1, -(k + m), k * m):
            wrongs.append(cand)
    assert len(wrongs) == 3

    def val(e):
        return e[0] * k * k + e[1] * k + e[2]
    cands = [(f"${EQ(*w)}$", f"$x={k}$ を代入すると，左辺は ${val(w)}$ となり $0$ にならない。", "解の意味の誤解") for w in wrongs]
    return MC(f"次の二次方程式のうち，$x={k}$ を解にもつものを，" + SEL4, f"${right_eq}$", cands,
              f"$x={k}$ を代入すると，${right_eq}$ の左辺は ${k * k}{'+' if -(k + m) * k >= 0 else '-'}{abs(-(k + m) * k)}{'+' if k * m >= 0 else '-'}{abs(k * m)}=0$ となり成り立つ。", d=2,
              ap="「解」は方程式を成り立たせる値。$x={k}$ をそれぞれの左辺に代入して $0$ になるものを探す。",
              steps=[f"それぞれの方程式に $x={k}$ を代入する。", "左辺が $0$ になるものが答え。", f"${right_eq}$ は $({lin(1, -k)})({lin(1, -m)})=0$ と因数分解でき，解は $x={k},\\ {m}$。"],
              alt=["それぞれの方程式を因数分解して解を求め、その中に $x=" + str(k) + "$ があるかを調べてもよい。"],
              pc=[("代入して確かめる方法を使っている", 1), ("正しく選んでいる", 1)],
              pit=[f"$(x+{abs(k)})$ のような因数を見て、$x={abs(k)}$ が解だと符号を逆に判断する。" if k > 0 else f"$(x-{abs(k)})$ のような因数を見て、$x={abs(k)}$ が解だと符号を逆に判断する。", "代入したときの負の数の2乗の計算を誤る。"],
              chk=(f"({k})**2+({-(k + m)})*({k})+({k * m})", "0", None, "intermediate"))


@gen("basic_check", 4, ["concept", "computation"])
def a_complete_square(r):
    p = _nz(r, -6, 6)
    while True:
        c = _nz(r, -9, 9)
        q = p * p - c
        if q > 0 and not is_sq(q):
            break
    b = 2 * p
    eq = EQ(1, b, c)

    def sq(pp, qq):
        return f"$({lin(1, pp)})^2={qq}$"
    right = sq(p, q)
    cands = [(sq(p, -c), f"左辺に ${p * p}$ を加えたのに、右辺に加えていない。", "等式の性質の誤り"),
             (sq(b, b * b - c), "$x$ の係数をそのままかっこの中に入れている。かっこの中は係数の半分。", "平方完成の手順の誤り"),
             (sq(-p, q), "かっこの中の符号を誤っている。", "符号の誤り"),
             (sq(p, p * p + c), "定数項を移項するときの符号を誤っている。", "移項の符号の誤り")]
    return MC(f"二次方程式 ${eq}$ を $(x+p)^2=q$ の形に変形したものとして正しいものを，" + SEL4, right, cands,
              f"${poly(1, b, 0)}={-c}$。両辺に ${p * p}$ を加えて $({lin(1, p)})^2={q}$。", d=2,
              ap="定数項を移項し、両辺に「$x$ の係数の半分の2乗」を加えると、左辺が $(x+p)^2$ の形になる。",
              steps=[f"定数項を移項：${poly(1, b, 0)}={-c}$。", f"$x$ の係数 ${b}$ の半分 ${p}$ の2乗 ${p * p}$ を両辺に加える。", f"$({lin(1, p)})^2={q}$。"],
              alt=[f"答えの左辺を展開して $x^2{'+' if b > 0 else '-'}{abs(b)}x+{p * p}={q}$ となり、移項すると ${eq}$ にもどることを確かめる。"],
              pc=[("両辺に同じ数を加えている", 1), ("正しい形に変形している", 1)],
              pit=["左辺だけに数を加える。", "かっこの中に $x$ の係数をそのまま入れる。"],
              chk=(f"expand((x+({p}))**2-{q})", f"x**2+({b})*x+({c})", None, "intermediate"))


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 4, ["computation", "cross_unit"], rel=["JH-MATH-G3-U01"])
def b_expand_solve(r):
    kind = r.choice(["prod", "prod", "move", "two"])
    p, q = r.sample([v for v in range(-8, 9) if v], 2)
    B, C = -(p + q), p * q
    roots = (p, q)
    assert not (kind == "move" and B == 0)
    if kind == "prod":
        while True:
            a1 = _nz(r, -6, 6)
            a2 = B - a1
            k = C - a1 * a2
            if a2 and k and a1 != a2:
                break
        eq = f"({lin(1, a1)})({lin(1, a2)})={k}"
        steps = [f"左辺を展開：$x^2{'+' if B >= 0 else '-'}{abs(B)}x{'+' if a1 * a2 >= 0 else '-'}{abs(a1 * a2)}={k}$。", f"移項して整理：${EQ(1, B, C)}$。", f"因数分解：$({lin(1, -p)})({lin(1, -q)})=0$。", f"{xs(p, q)}。"]
        cands = [(xs(k - a1, k - a2), f"右辺が $0$ でないのに、それぞれのかっこを ${k}$ とおいている。$AB=0$ のときだけ $A=0$ または $B=0$ といえる。", "因数分解による解き方の条件の誤解"),
                 (xs(-a1, -a2), "右辺を $0$ とみなして、左辺のかっこからそのまま解を読んでいる。", "因数分解による解き方の条件の誤解"),
                 (xs(-p, -q), "解の符号を逆にしている。", "符号の誤り"),
                 (xs(p, -q), "片方の解の符号を誤っている。", "符号の誤り")]
    elif kind == "move":
        eq = f"x^2={poly(-B, -C)}"
        steps = [f"右辺を移項：${EQ(1, B, C)}$。", f"因数分解：$({lin(1, -p)})({lin(1, -q)})=0$。", f"{xs(p, q)}。"]
        cands = [(xs(-p, -q), "解の符号を逆にしている。", "符号の誤り"),
                 (xs(p, -q), "片方の解の符号を誤っている。", "符号の誤り"),
                 (xs(-p, q), "片方の解の符号を誤っている。", "符号の誤り"),
                 (xs(p + 1, q - 1) if (p + 1) * (q - 1) != p * q else None, "移項したときの符号を誤り、別の方程式を解いている。", "移項の符号の誤り")]
    else:
        m = r.choice([2, 3, -2, -3])
        eq = EQ(m, m * B, m * C)
        steps = [f"両辺を ${m}$ でわる：${EQ(1, B, C)}$。", f"因数分解：$({lin(1, -p)})({lin(1, -q)})=0$。", f"{xs(p, q)}。"]
        cands = [(xs(-p, -q), "解の符号を逆にしている。", "符号の誤り"),
                 (xs(p, -q), "片方の解の符号を誤っている。", "符号の誤り"),
                 (xs(m * p, m * q), f"両辺を ${m}$ でわらずに、解を ${m}$ 倍してしまっている。", "等式の性質の誤り"),
                 (xs(-p, q), "片方の解の符号を誤っている。", "符号の誤り")]
    return MC(f"二次方程式 ${eq}$ を解いた結果として正しいものを，" + SEL4, xs(*roots), cands,
              f"整理すると ${EQ(1, B, C)}$。$({lin(1, -p)})({lin(1, -q)})=0$ より {xs(p, q)}。", d=3, p=4,
              ap="まず展開・移項して $ax^2+bx+c=0$ の形に整理する（式の展開の単元とのつながり）。右辺が $0$ になってから因数分解する。",
              steps=steps, alt=["求めた解をもとの方程式（整理する前の形）に代入して、両辺が等しくなることを確かめる。"],
              pc=[("右辺を $0$ にして正しく整理している", 2), ("因数分解して正しく解いている", 2)],
              pit=["$(x+a)(x+b)=k$ のまま、$x+a=k$ とおいてしまう。", "移項したときの符号の誤り。"],
              chk=(f"({p})**2+({B})*({p})+({C})", "0", None, "intermediate"))


@gen("standard_practice", 4, ["condition_check", "computation"])
def b_param(r):
    k = _nz(r, -7, 7)
    m = r.choice([v for v in range(-8, 9) if v and v != k])
    A, C = -(k + m), k * m
    ask_c = r.random() < 0.5
    if ask_c:
        eq = f"x^2{'+' if A > 0 else '-' if A < 0 else '+'}{abs(A) if abs(A) != 1 else ''}x+c=0" if A else "x^2+c=0"
        unknown, val_ = "c", C
        cands_t = [(C, -m), (-C, m), (-C, -m), (C, k + m if k + m not in (m,) else -k)]
    else:
        eq = f"x^2+ax{'+' if C > 0 else '-'}{abs(C)}=0"
        unknown, val_ = "a", A
        cands_t = [(-A, m), (A, -m), (-A, -m), (A, C if C != m else -C)]

    def ch(v, w):
        return f"${unknown}={v}$，もう1つの解 $x={w}$"
    right = ch(val_, m)
    reasons = {0: "もう1つの解の符号を誤っている。", 1: f"${unknown}$ の値の符号を誤っている。", 2: f"${unknown}$ の値ともう1つの解の符号をどちらも誤っている。", 3: "もう1つの解の求め方を誤っている。"}
    cands = []
    for i, (v, w) in enumerate(cands_t):
        rs = []
        if v != val_:
            rs.append(f"${unknown}$ の値は ${val_}$。")
        if w != m:
            rs.append(f"もう1つの解は $x={m}$。")
        cands.append((ch(v, w), reasons[i] + " " + "".join(rs), "代入・符号の誤り"))
    full = EQ(1, A, C)
    return MC(f"$x$ についての二次方程式 ${eq}$ の解の1つが $x={k}$ であるとき，${unknown}$ の値と，もう1つの解の組み合わせとして正しいものを，" + SEL4,
              right, cands, f"$x={k}$ を代入して ${unknown}={val_}$。方程式は ${full}$，$({lin(1, -k)})({lin(1, -m)})=0$ より，もう1つの解は $x={m}$。", d=3, p=4,
              ap="「解の1つが $x=k$」は、$x=k$ を代入すると等式が成り立つということ。代入して文字の値を求め、もとの方程式を解き直す。",
              steps=[f"$x={k}$ を代入：${unknown}$ についての一次方程式を解いて ${unknown}={val_}$。", f"方程式は ${full}$。", f"$({lin(1, -k)})({lin(1, -m)})=0$ より，もう1つの解は $x={m}$。"],
              alt=[f"2つの解を $x={k},\\ x=t$ とすると，左辺は $(x{'-' if k > 0 else '+'}{abs(k)})(x-t)$ と因数分解できるので，係数を比べて $t={m}$ を求めることもできる。"],
              pc=[(f"代入して ${unknown}$ の値を求めている", 2), ("もう1つの解を正しく求めている", 2)],
              pit=["代入したときの負の数の計算を誤る。", "もう1つの解の符号を逆にする。"],
              chk=(f"({k})**2+({A})*({k})+({C})", "0", None, "intermediate"))


@gen("standard_practice", 4, ["application", "condition_check"])
def b_number_word(r):
    kind = r.choice(["consec2", "consec3", "sq_k", "diff"])
    if kind == "consec2":
        n = r.randint(4, 20)
        N = n * (n + 1)
        big = r.random() < 0.5
        stem = f"連続する2つの自然数があり，その積は ${N}$ である。この2つの自然数のうち，{'大きい' if big else '小さい'}方の数を求めなさい。"
        ans = n + 1 if big else n
        eqs = f"x(x+1)={N}"
        steps = [f"小さい方を $x$ とすると，大きい方は $x+1$。", f"${eqs}$，$x^2+x-{N}=0$，$(x-{n})(x+{n + 1})=0$。", f"$x={n},\\ x=-{n + 1}$。$x$ は自然数なので $x={n}$。", f"答えは ${ans}$。"]
        expr = f"{n}+{1 if big else 0}"
    elif kind == "consec3":
        n = r.randint(4, 12)
        dd = n * n - 2 * n - 3
        stem = f"連続する3つの自然数がある。最も小さい数の2乗は，残りの2つの数の和より ${dd}$ 大きい。最も小さい数を求めなさい。"
        ans = n
        steps = [f"最も小さい数を $x$ とすると，3つの数は $x,\\ x+1,\\ x+2$。", f"$x^2=(x+1)+(x+2)+{dd}$，$x^2-2x-{dd + 3}=0$。", f"$(x-{n})(x+{n - 2})=0$ より $x={n},\\ x=-{n - 2}$。", f"$x$ は自然数なので $x={n}$。"]
        expr = str(n)
    elif kind == "sq_k":
        k = r.randint(1, 8)
        x0 = r.randint(k + 1, k + 9)
        mm = x0 * (x0 - k)
        stem = f"ある自然数 $x$ を2乗した数は，$x$ を ${k}$ 倍した数より ${mm}$ 大きい。自然数 $x$ を求めなさい。"
        ans = x0
        steps = [f"$x^2={k}x+{mm}$，$x^2-{k}x-{mm}=0$。" if k > 1 else f"$x^2=x+{mm}$，$x^2-x-{mm}=0$。", f"$(x-{x0})(x+{x0 - k})=0$。", f"$x={x0},\\ x=-{x0 - k}$。自然数なので $x={x0}$。"]
        expr = str(x0)
    else:
        d = r.randint(2, 9)
        x0 = r.randint(2, 15)
        P = x0 * (x0 + d)
        big = r.random() < 0.5
        stem = f"大小2つの自然数があり，その差は ${d}$，積は ${P}$ である。{'大きい' if big else '小さい'}方の数を求めなさい。"
        ans = x0 + d if big else x0
        steps = [f"小さい方を $x$ とすると，大きい方は $x+{d}$。", f"$x(x+{d})={P}$，$x^2+{d}x-{P}=0$，$(x-{x0})(x+{x0 + d})=0$。", f"$x$ は自然数なので $x={x0}$。", f"答えは ${ans}$。"]
        expr = str(ans)
    return MARK(stem, ans, " ".join(steps), expr, d=3, p=4,
                ap="求める数を $x$ とおいて二次方程式をつくる。解が2つ出たら、「自然数」という条件に合うものだけを答える。",
                steps=steps, alt=["答えの数を問題文の条件にあてはめて、本当に成り立つかを確かめる。"],
                pc=[("正しく方程式をつくっている", 2), ("解を吟味して正しく答えている", 2)],
                pit=["負の解も答えに書いてしまう。", "小さい方と大きい方を取り違える。"])


def _box_svg():
    return shape({"A": (0, 0), "B": (8, 0), "C": (8, 8), "D": (0, 8), "a1": (2, 0), "a2": (2, 2), "a3": (0, 2), "b1": (6, 0), "b2": (6, 2), "b3": (8, 2),
                  "c1": (8, 6), "c2": (6, 6), "c3": (6, 8), "d1": (2, 8), "d2": (2, 6), "d3": (0, 6)},
                 labels={}, segments=[("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("a1", "a2"), ("a2", "a3"), ("b1", "b2"), ("b2", "b3"), ("c1", "c2"), ("c2", "c3"), ("d1", "d2"), ("d2", "d3")],
                 dashed=[("a2", "b2"), ("b2", "c2"), ("c2", "d2"), ("d2", "a2")], scale=13)


@gen("standard_practice", 4, ["application", "condition_check"])
def b_area_word(r):
    kind = r.choice(["road", "road", "box", "path"])
    if kind == "road":
        x0 = r.randint(1, 4)
        L = r.randint(8, 20)
        W = r.randint(L + 2, L + 16)
        S = (L - x0) * (W - x0)
        other = L + W - x0
        stem = (f"縦 ${L}$ m，横 ${W}$ m の長方形の土地に，同じ幅の道を縦と横に1本ずつ，土地の辺に平行につくり，残りの部分を花だんにする。"
                f"花だんの面積を ${S}$ m² にするには，道の幅を何 m にすればよいか求めなさい。")
        steps = [f"道の幅を $x$ m とすると，道をはしに寄せて考えて $({L}-x)({W}-x)={S}$。", f"展開して整理：$x^2-{L + W}x+{L * W - S}=0$。",
                 f"$(x-{x0})(x-{other})=0$ より $x={x0},\\ x={other}$。", f"$0<x<{L}$ なので $x={x0}$。"]
        ans, expr = x0, f"(({L}+{W})-sqrt(({L}+{W})**2-4*({L * W - S})))/2"
        fig = None
    elif kind == "box":
        c = r.randint(2, 5)
        t = r.randint(3, 12)
        side = 2 * c + t
        V = c * t * t
        stem = (f"正方形の厚紙の四すみから，1辺が ${c}$ cm の正方形を切り取り，残りを折り曲げてふたのない直方体の箱をつくったところ，"
                f"箱の容積は ${V}$ cm³ になった。もとの厚紙の1辺の長さは何 cm か求めなさい。")
        steps = [f"もとの1辺を $x$ cm とすると，箱の底面は1辺 $(x-{2 * c})$ cm の正方形，高さは ${c}$ cm。", f"${c}(x-{2 * c})^2={V}$，$(x-{2 * c})^2={t * t}$。",
                 f"$x-{2 * c}=\\pm{t}$ より $x={side},\\ x={2 * c - t}$。", f"底面の1辺 $x-{2 * c}$ は正なので $x>{2 * c}$。$x={side}$。"]
        ans, expr = side, f"{2 * c}+sqrt(Rational({V},{c}))"
        fig = figure("正方形の厚紙の四すみから正方形を切り取る図（点線で折り曲げる）", _box_svg())
    else:
        x0 = r.randint(1, 4)
        L = r.randint(4, 15)
        W = r.randint(L, L + 10)
        S = (L + 2 * x0) * (W + 2 * x0) - L * W
        stem = (f"縦 ${L}$ m，横 ${W}$ m の長方形の花だんのまわりに，同じ幅の通路をつくる。"
                f"通路の面積を ${S}$ m² にするには，通路の幅を何 m にすればよいか求めなさい。")
        steps = [f"通路の幅を $x$ m とすると，通路をふくめた長方形は縦 $({L}+2x)$ m，横 $({W}+2x)$ m。", f"$({L}+2x)({W}+2x)-{L * W}={S}$，$4x^2+{2 * (L + W)}x-{S}=0$。",
                 f"これを解くと $x={x0},\\ x={ftex(Fr(-S, 4 * x0))}$。", f"$x>0$ なので $x={x0}$。"]
        ans, expr = x0, f"(-{2 * (L + W)}+sqrt({4 * (L + W) ** 2}+16*{S}))/8"
        fig = None
    kw = dict(fig=fig) if fig else {}
    return MARK(stem, ans, " ".join(steps), expr, d=3, p=4,
                ap="求める長さを $x$ とおき、図の中の長さを $x$ で表して面積・体積の式をつくる。最後に $x$ の範囲で解を吟味する。",
                steps=steps, alt=["求めた答えを使って面積（体積）を計算し、問題の値になるかを確かめる。"],
                pc=[("長さを $x$ で表して方程式をつくっている", 2), ("解を吟味して正しく答えている", 2)],
                pit=["方程式の2つの解をどちらも答えにしてしまう。", "長さが正になる条件（範囲）を考えない。"], **kw)


@gen("standard_practice", 4, ["computation", "condition_check"])
def b_formula_arrange(r):
    for _ in range(300):
        kind = r.choice(["rhs", "paren", "sq"])
        if kind == "rhs":
            a, b, c = _formula_eq(r)
            if b == 0:
                continue
            eq = f"{a if a != 1 else ''}x^2={poly(-b, -c)}"
            step0 = f"右辺を移項して ${EQ(a, b, c)}$。"
            break
        if kind == "paren":
            a, b, c = _formula_eq(r)
            if b == 0 or c == 0:
                continue
            eq = f"x({lin(1, b) if a == 1 else poly(a, b)})={-c}"
            step0 = f"左辺を展開して移項すると ${EQ(a, b, c)}$。"
            break
        p = _nz(r, -4, 4)
        q = _nz(r, -5, 5)
        rr = r.randint(-6, 6)
        a, b, c = 1, 2 * p - q, p * p - rr
        D = b * b - 4 * a * c
        if D > 0 and not is_sq(D) and D <= 120 and b != 0:
            eq = f"({lin(1, p)})^2={poly(q, rr) if rr else poly(q, 0)}"
            step0 = f"左辺を展開して移項すると ${EQ(a, b, c)}$。"
            break
    else:
        raise AssertionError("no equation")
    D, s, d = formula_parts(a, b, c)
    right = qf(-b, s, d, 2 * a)
    return MC(f"二次方程式 ${eq}$ を解いた結果として正しいものを，" + SEL4, right, formula_cands(a, b, c),
              f"{step0} 解の公式より $x=\\dfrac{{{-b}\\pm\\sqrt{{{D}}}}}{{{2 * a}}}$。整理して {right}。", d=3, p=4,
              ap="まず $ax^2+bx+c=0$ の形に整理する。因数分解できないことを確かめたら、解の公式を使う。",
              steps=[step0, f"$a={a}$，$b={b}$，$c={c}$ を解の公式に代入。", f"$x=\\dfrac{{{-b}\\pm\\sqrt{{{D}}}}}{{{2 * a}}}$。", f"整理して {right}。"],
              alt=["近似値（$\\sqrt{2}\\fallingdotseq1.41$ など）で解の値を求め、もとの方程式に代入してほぼ成り立つかを確かめる。"],
              pc=[("正しく整理している", 2), ("解の公式で正しく解いている", 2)],
              pit=["移項したときの符号の誤り。", "約分で根号の項をわり忘れる。"],
              chk=(f"{a}*({qf_py(-b, s, d, 2 * a)})**2+({b})*({qf_py(-b, s, d, 2 * a)})+({c})", "0", None, "intermediate"))


# ======================================================================
# C 思考力・記述応用
# ======================================================================

def _statements(r):
    k = r.randint(2, 9)
    p = _nz(r, -5, 5)
    t = r.randint(2, 6)
    h = r.randint(1, 4)
    c0 = r.randint(1, 9)
    m = r.randint(2, 7)
    a2, b2, c2 = _formula_eq(r)
    D2, s2, d2 = formula_parts(a2, b2, c2)
    good = qf(-b2, s2, d2, 2 * a2)
    bad = qf(-b2, s2, d2, a2) if a2 > 1 else qf(b2, s2, d2, 2 * a2) if b2 else None
    out = [
        (f"二次方程式 $x^2={k * k}$ の解は $x={k}$ だけである。", False, f"$(-{k})^2={k * k}$ なので $x=-{k}$ も解。解は $x=\\pm{k}$。"),
        (f"二次方程式 $x^2={m}x$ の両辺を $x$ でわって，解は $x={m}$ だけであるといえる。", False, f"$x=0$ も解である。$x(x-{m})=0$ より $x=0,\\ x={m}$。"),
        (f"二次方程式 $({lin(1, -p)})^2=0$ の解は1つだけである。", True, f"$x{'-' if p > 0 else '+'}{abs(p)}=0$ より解は $x={p}$ の1つだけ。"),
        (f"二次方程式 $x^2+{2 * h}x={c0}$ は，$(x+{h})^2={c0 + h * h}$ と変形できる。", True, f"両辺に ${h * h}$ を加えると $(x+{h})^2={c0 + h * h}$。"),
        (f"二次方程式 $x^2+{2 * h}x={c0}$ は，$(x+{h})^2={c0}$ と変形できる。", False, f"左辺に ${h * h}$ を加えたら右辺にも加える必要があり，$(x+{h})^2={c0 + h * h}$。"),
        (f"$(x-{t})(x-{t + 1})=2$ ならば，$x-{t}=2$ または $x-{t + 1}=2$ である。", False, f"右辺が $0$ でないので，この考え方は使えない。$x={t + 3}$ を代入すると左辺は $3\\times2=6$ で成り立たない。"),
        ("二次方程式の解は，いつも2つある。", False, f"$(x-{t})^2=0$ のように解が1つの二次方程式もある。"),
        (f"二次方程式 $x^2-{2 * t + 1}x+{t * (t + 1)}=0$ の解は $x={t},\\ x={t + 1}$ である。", True, f"$(x-{t})(x-{t + 1})=0$ と因数分解できる。"),
        (f"二次方程式 ${EQ(a2, b2, c2)}$ の解は {good} である。", True, f"解の公式に $a={a2}$，$b={b2}$，$c={c2}$ を代入すると {good}。"),
    ]
    if bad:
        out.append((f"二次方程式 ${EQ(a2, b2, c2)}$ の解は {bad} である。", False, f"正しくは {good}。分母は $2a$，分子は $-b$ から始まる。"))
    return out


@gen("thinking_writing", 3, ["written_reasoning", "condition_check", "concept"])
def c_xy_judge(r):
    S = _statements(r)
    tx, ty = r.choice([True, False]), r.choice([True, False])
    x = r.choice([s for s in S if s[1] == tx])
    y = r.choice([s for s in S if s[1] == ty and s is not x and s[0][:20] != x[0][:20]])
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
        why[c] = (" ".join(rs), "二次方程式の解き方の思いこみ")
    return mc("Kさんは，二次方程式について次の X，Y のようにノートにまとめた。X，Y の文の正誤の組み合わせとして最も適するものを，" + SEL4 + f"\nX　{x[0]}\nY　{y[0]}",
              [ans] + [c for c in XY if c != ans], f"X：{x[2]}　Y：{y[2]}", d=4, p=8, why=why,
              ap="それぞれの文を、解の意味（代入すると成り立つ値）、$AB=0$ の性質、平方完成・解の公式の手順に照らして確かめる。具体的な値を代入して反例を探すのも有効。",
              steps=[f"X：{x[2]}", f"Y：{y[2]}", f"よって {ans}。"],
              alt=["文に出てくる方程式を実際に解いたり、値を代入したりして確かめる。"],
              pc=[("X の正誤を根拠をもって判断している", 4), ("Y の正誤を根拠をもって判断している", 4)],
              pit=["両辺を $x$ でわってよいと思いこむ。", "右辺が $0$ でなくても因数ごとに考えてしまう。"])


def _move_fig(L, M):
    w, h = 6.0, 6.0 * L / M if M else 4.0
    h = max(2.5, min(5.0, h))
    return shape({"A": (0, h), "B": (0, 0), "C": (w, 0), "D": (w, h), "P": (0, h * 0.45), "Q": (w * 0.4, 0)},
                 segments=[("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")], dashed=[("P", "Q")], scale=22)


@gen("thinking_writing", 3, ["cross_unit", "application", "condition_check"], rel=["JH-MATH-G3-U04", "JH-MATH-G2-U03"])
def c_moving_point(r):
    q = r.choice([1, 2, 3])
    while True:
        L = r.randint(5, 14)
        t = r.randint(1, L - 1)
        if 2 * t == L:
            continue
        S2 = q * t * (L - t)
        if S2 % 2 == 0:
            break
    S = S2 // 2
    M = q * L
    first = r.random() < 0.5
    ans = min(t, L - t) if first else max(t, L - t)
    stem = (f"右の図のような，AB $={L}$ cm，BC $={M}$ cm の長方形 ABCD がある。点 P は A を出発して辺 AB 上を毎秒 $1$ cm の速さで B まで動き，"
            f"点 Q は点 P と同時に B を出発して辺 BC 上を毎秒 ${q}$ cm の速さで C まで動く。2点が出発してから $x$ 秒後の $\\triangle\\mathrm{{PBQ}}$ の面積を考える。"
            f"$\\triangle\\mathrm{{PBQ}}$ の面積が ${S}$ cm² になるのは，2点が出発してから何秒後か。{'1回目' if first else '2回目'}の時刻を求めなさい。")
    return MARK(stem, ans, f"PB $={L}-x$，BQ $={'' if q == 1 else q}x$ なので $\\dfrac{{1}}{{2}}({L}-x)\\times{'' if q == 1 else q}x={S}$。整理して $x^2-{L}x+{t * (L - t)}=0$，$x={min(t, L - t)},\\ {max(t, L - t)}$。どちらも $0<x<{L}$ をみたすので，{'1回目' if first else '2回目'}は ${ans}$ 秒後。",
                f"{'(' + str(L) + '-sqrt(' + str(L * L - 4 * t * (L - t)) + '))/2' if first else '(' + str(L) + '+sqrt(' + str(L * L - 4 * t * (L - t)) + '))/2'}", d=4, p=8,
                fig=figure("長方形 ABCD と、辺 AB 上を動く点 P・辺 BC 上を動く点 Q", _move_fig(L, M)),
                ap="PB と BQ の長さを $x$ で表し、三角形の面積の式をつくる。面積は $x$ の二次式になる（関数 $y=ax^2$ の単元で学ぶ「2乗に比例する量」とのつながり）。$x$ の変域も確かめる。",
                steps=[f"$x$ 秒後，AP $=x$ cm なので PB $=({L}-x)$ cm，BQ $={'' if q == 1 else q}x$ cm（$0\\leqq x\\leqq {L}$）。",
                       f"$\\dfrac{{1}}{{2}}({L}-x)\\times{'' if q == 1 else q}x={S}$ を整理して $x^2-{L}x+{t * (L - t)}=0$。",
                       f"$(x-{min(t, L - t)})(x-{max(t, L - t)})=0$ より $x={min(t, L - t)},\\ x={max(t, L - t)}$。",
                       f"どちらも変域内なので，{'1回目' if first else '2回目'}は ${ans}$ 秒後。"],
                alt=[f"面積の式 $y=\\dfrac{{{q}}}{{2}}x({L}-x)$ に $x=1,\\ 2,\\ \\cdots$ を代入して表をつくり、面積が ${S}$ cm² になる時刻を探して確かめる。"],
                pc=[("PB・BQ を $x$ で表している", 3), ("二次方程式をつくって解いている", 3), ("変域を考えて正しく答えている", 2)],
                pit=["PB を $x$ と表してしまう（AP と取り違える）。", "解が2つあるときに、どちらが問われているかを確かめない。"])


@gen("thinking_writing", 2, ["application", "condition_check"])
def c_price(r):
    while True:
        P = r.choice([100, 120, 150, 200, 240, 250, 300, 400, 500])
        k = r.randint(2, 8)
        x0 = r.randint(1, 12)
        x2 = r.choice([v for v in range(-(P // 10) + 1, 16) if v and v != x0])
        N = k * P // 10 + k * (x0 + x2)
        if N - k * max(x0, x2) > 0 and k * P % 10 == 0:
            break
    S = (P + 10 * x0) * (N - k * x0)
    valid = sorted(v for v in (x0, x2) if v > 0)
    best = valid[0]
    ans = P + 10 * best
    stem = (f"ある店では，1個 ${P}$ 円で売ると1日に ${N}$ 個売れる品物がある。この品物は，1個の値段を $10$ 円値上げするごとに，1日に売れる個数が ${k}$ 個ずつ減るものとする。"
            f"1日の売上金額を ${S}$ 円にするために値段を値上げするとき，値上げした後の1個の値段として考えられるもののうち，最も安い値段は何円か求めなさい。ただし，消費税は考えないものとする。")
    roots_txt = f"$x={min(x0, x2)},\\ x={max(x0, x2)}$"
    return MARK(stem, ans, f"$10x$ 円値上げするとき $({P}+10x)({N}-{k}x)={S}$。解は {roots_txt}。値上げなので $x>0$，最も安いのは $x={best}$ で ${ans}$ 円。",
                f"{P}+10*{best}", d=4, p=8,
                ap="値上げの回数を $x$ とおき、（値段）×（売れる個数）＝（売上金額）の方程式をつくる。$x>0$ や「最も安い」という条件で解を選ぶ。",
                steps=[f"$10$ 円の値上げを $x$ 回行うと，値段は $({P}+10x)$ 円，売れる個数は $({N}-{k}x)$ 個。", f"$({P}+10x)({N}-{k}x)={S}$。",
                       f"展開して整理すると $x^2-{x0 + x2}x+{x0 * x2}=0$" .replace("-0x", "").replace("+-", "-").replace("--", "+") + f"，{roots_txt}。",
                       f"値上げするので $x>0$。考えられる値段 {'，'.join(f'${P + 10 * v}$ 円' for v in valid)} のうち，最も安いのは ${ans}$ 円。"],
                alt=[f"答えの値段 ${ans}$ 円のときの売れる個数 ${N - k * best}$ 個を求め、${ans}\\times{N - k * best}={S}$ になることを確かめる。"],
                pc=[("値段と個数を $x$ で表して方程式をつくっている", 3), ("方程式を正しく解いている", 3), ("条件に合う解を選んで値段で答えている", 2)],
                pit=["$x$ の値をそのまま答えて、値段に直し忘れる。", "値上げの条件（$x>0$）を考えずに解を選ぶ。"])


@gen("thinking_writing", 2, ["condition_check", "multiple_solutions"])
def c_relation(r):
    r1, r2 = r.sample([v for v in range(-5, 6) if v], 2)
    kind = r.choice(["shift", "times"])
    if kind == "shift":
        k = r.choice([v for v in range(-4, 5) if v])
        s1, s2 = r1 + k, r2 + k
        rel_t = f"それぞれ ${k}$ だけ大きい" if k > 0 else f"それぞれ ${-k}$ だけ小さい"
    else:
        k = r.choice([2, 3, -2, -1])
        s1, s2 = r1 * k, r2 * k
        rel_t = f"それぞれ ${k}$ 倍にした数" if k != -1 else "それぞれ符号を変えた数"
    assert s1 != s2 and s1 and s2
    A, B = -(s1 + s2), s1 * s2
    base = EQ(1, -(r1 + r2), r1 * r2)

    def ch(a, b):
        return f"$a={a}$，$b={b}$"
    cands = [(ch(-A, B), "$a$ の符号を誤っている。$(x-p)(x-q)=x^2-(p+q)x+pq$ なので $a=-(p+q)$。", "符号の誤り"),
             (ch(A, -B), "$b$ の符号を誤っている。", "符号の誤り"),
             (ch(-A, -B), "$a$、$b$ の符号をどちらも誤っている。", "符号の誤り"),
             (ch(-(r1 + r2 + (k if kind == 'shift' else 0)), r1 * r2 + (k if kind == 'shift' else 0)), "係数そのものに同じ操作をしている。解を変えてから方程式をつくり直す必要がある。", "解と係数の関係の誤解")]
    return MC(f"二次方程式 $x^2+ax+b=0$ の2つの解は，二次方程式 ${base}$ の2つの解より{rel_t}である。$a$，$b$ の値の組み合わせとして正しいものを，" + SEL4 if kind == "shift"
              else f"二次方程式 $x^2+ax+b=0$ の2つの解は，二次方程式 ${base}$ の2つの解を{rel_t}である。$a$，$b$ の値の組み合わせとして正しいものを，" + SEL4,
              ch(A, B), cands, f"${base}$ の解は $x={r1},\\ {r2}$。求める方程式の解は $x={s1},\\ {s2}$ なので $(x{'-' if s1 > 0 else '+'}{abs(s1)})(x{'-' if s2 > 0 else '+'}{abs(s2)})=0$，${EQ(1, A, B)}$。", d=4, p=8,
              ap="まずもとの方程式を解き、条件に合う新しい2つの解を求める。2つの解が $p$、$q$ の二次方程式は $(x-p)(x-q)=0$ と表せる。",
              steps=[f"${base}$ を解くと $x={r1},\\ {r2}$。", f"新しい解は $x={s1},\\ {s2}$。", f"$(x{'-' if s1 > 0 else '+'}{abs(s1)})(x{'-' if s2 > 0 else '+'}{abs(s2)})=0$ を展開して ${EQ(1, A, B)}$。", f"$a={A}$，$b={B}$。"],
              alt=[f"$x={s1}$，$x={s2}$ をそれぞれ $x^2+ax+b=0$ に代入して、$a$、$b$ の連立方程式を解いてもよい（連立方程式の解き方）。"],
              pc=[("もとの方程式を正しく解いている", 3), ("新しい解を正しく求めている", 2), ("$a$、$b$ を正しく求めている", 3)],
              pit=["係数に直接同じ操作をしてしまう。", "展開したときの符号を誤る。"],
              chk=(f"expand((x-({s1}))*(x-({s2})))", f"x**2+({A})*x+({B})", None, "intermediate"))


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def _err_mc(stem, sol, right, cands, e, err, **kw):
    return MC(f"{stem}\n〔Kさんの解答〕\n{sol}\nKさんの解答の誤りを説明したものとして最も適するものを，" + SEL4, right, cands, e, err=err, **kw)


EXPL = {
    "div": "両辺を $x$ でわっているため，$x=0$ という解を落としている。",
    "prod": "右辺が $0$ でないのに，左辺のそれぞれのかっこが右辺の数に等しいとしている。",
    "pm": "平方根を考えるときに，負の方を落としている。",
    "den": "解の公式の分母を $2a$ ではなく $a$ にしている。",
    "signb": "解の公式の分子の $-b$ の符号を誤っている。",
    "cs": "左辺に数を加えたのに，右辺に同じ数を加えていない。",
}


def _err_case(r, kind):
    if kind == "div":
        a = r.randint(1, 5)
        b = _nz(r, -9, 9)
        lhs = f"{'' if a == 1 else a}x^2={'' if b == 1 else '-' if b == -1 else b}x"
        prob = f"二次方程式 ${lhs}$ を解きなさい。"
        sol = f"両辺を $x$ でわって ${'' if a == 1 else a}x={b}$\n答え　{xs(Fr(b, a))}"
        fix = f"$x({'' if a == 1 else a}x{'-' if b > 0 else '+'}{abs(b)})=0$ より {xs(0, Fr(b, a))}"
        return prob, sol, fix, "両辺を $x$ でわった変形", "condition", "一次方程式のように両辺を同じ数でわる変形をしたくなる。$x=0$ のときはわれないことに気づきにくい。", f"{a}*0**2-({b})*0", "0"
    if kind == "prod":
        while True:
            p, q = r.sample([v for v in range(-6, 7) if v], 2)
            r1 = _nz(r, -8, 8)
            r2 = p + q - r1
            c = p * q - r1 * r2
            if c and r2 and r1 != r2 and {c + p, c + q} != {r1, r2}:
                break
        prob = f"二次方程式 $({lin(1, -p)})({lin(1, -q)})={c}$ を解きなさい。"
        sol = f"$x{'-' if p > 0 else '+'}{abs(p)}={c}$ または $x{'-' if q > 0 else '+'}{abs(q)}={c}$\n答え　{xs(c + p, c + q)}"
        fix = f"展開して整理すると ${EQ(1, -(p + q), p * q - c)}$，{xs(r1, r2)}"
        return prob, sol, fix, "因数分解による解き方の使い方", "concept", "「かっこが2つあれば、それぞれを右辺の数とおけばよい」と形だけで覚えてしまう。", f"({r1}-({p}))*({r1}-({q}))", str(c)
    if kind == "pm":
        p = _nz(r, -6, 6)
        q = r.choice([2, 3, 5, 6, 7, 10])
        prob = f"二次方程式 $({lin(1, p)})^2={q}$ を解きなさい。"
        sol = f"${lin(1, p)}=\\sqrt{{{q}}}$\n答え　$x={-p}+\\sqrt{{{q}}}$"
        fix = f"${lin(1, p)}=\\pm\\sqrt{{{q}}}$ より $x={-p}\\pm\\sqrt{{{q}}}$"
        return prob, sol, fix, "平方根の考え", "concept", "「$\\sqrt{\\ }$ をつける」ことだけを覚えていて、平方根が正と負の2つあることを忘れる。", f"({-p}-sqrt({q})+({p}))**2", str(q)
    if kind in ("den", "signb"):
        for _ in range(200):
            a, b, c = _formula_eq(r)
            if kind == "den" and a == 1:
                continue
            if kind == "signb" and b == 0:
                continue
            break
        else:
            raise AssertionError("no eq")
        D, s, d = formula_parts(a, b, c)
        prob = f"二次方程式 ${EQ(a, b, c)}$ を解きなさい。"
        if kind == "den":
            sol = f"$x=\\dfrac{{{-b}\\pm\\sqrt{{{par(b)}^2-4\\times{a}\\times{par(c)}}}}}{{{a}}}$\n答え　{qf(-b, s, d, a)}"
            tempt = "解の公式の分母を、$x^2$ の係数 $a$ だと覚え違えやすい。"
        else:
            sol = f"$x=\\dfrac{{{b}\\pm\\sqrt{{{par(b)}^2-4\\times{a}\\times{par(c)}}}}}{{{2 * a}}}$\n答え　{qf(b, s, d, 2 * a)}"
            tempt = "$-b$ に負の数を代入すると正になることを見落とし、$b$ の値をそのまま書いてしまう。"
        fix = f"$x=\\dfrac{{{-b}\\pm\\sqrt{{{D}}}}}{{{2 * a}}}$ より {qf(-b, s, d, 2 * a)}"
        return prob, sol, fix, "解の公式への代入", "formula", tempt, f"{par(b)}**2-4*{a}*({c})", str(D)
    h = _nz(r, -5, 5)
    while True:
        c = _nz(r, -9, 9)
        q = h * h - c
        if q > 0 and not is_sq(q) and -c != q:
            break
    prob = f"二次方程式 ${EQ(1, 2 * h, c)}$ を，$(x+p)^2=q$ の形に変形して解きなさい。"
    s_, d_ = sqf(q)
    sol = f"${poly(1, 2 * h, 0)}={-c}$\n$({lin(1, h)})^2={-c}$\n答え　" + (f"$x={-h}\\pm{sq_term(*sqf(-c))}$" if -c > 0 and not is_sq(-c) else ("答えなし" if -c < 0 else xs(-h + math.isqrt(-c), -h - math.isqrt(-c))))
    fix = f"両辺に ${h * h}$ を加えて $({lin(1, h)})^2={q}$，$x={-h}\\pm{sq_term(s_, d_)}$"
    return prob, sol, fix, "平方完成（両辺に同じ数を加える）", "calculation", "左辺を $(x+p)^2$ の形にすることに気をとられ、右辺にも同じ数を加えることを忘れる。", f"expand((x+({h}))**2-{q})", f"x**2+({2 * h})*x+({c})"


@gen("error_correction", 4, ["common_error", "condition_check"])
def d_err_explain(r):
    kind = r.choice(list(EXPL))
    prob, sol, fix, step, etype, tempt, ex_py, ans_py = _err_case(r, kind)
    others = [k for k in EXPL if k != kind]
    r.shuffle(others)
    cands = [(EXPL[k], "Kさんの解答では、このような誤りはしていない。", "誤りの箇所の見落とし") for k in others[:2]]
    cands.append(("Kさんの解答に誤りはない。", "Kさんの答えをもとの方程式に代入すると成り立たない（または解が足りない）。", "検算不足"))
    return _err_mc(f"〔問題〕{prob}", sol, EXPL[kind], cands, f"正しくは {fix}。",
                   dict(sol=sol, step=step, type=etype, tempt=tempt, fix=fix), d=3, p=6,
                   ap="Kさんの答えをもとの方程式に代入して確かめる。成り立たない解や、足りない解がないかを調べ、どの変形で誤ったかをさがす。",
                   steps=[f"Kさんの解答の誤り：{EXPL[kind]}", f"正しい解き方：{fix}。"],
                   alt=["別の解き方（因数分解・平方根の考え・解の公式）でも解いて、答えが一致するかを比べる。"],
                   pc=[("誤りの箇所を正しく指摘している", 3), ("正しい解を求めている", 3)],
                   pit=["両辺を $x$ でわって $x=0$ を落とす。", "$\\pm$ を忘れる。"],
                   chk=(ex_py, ans_py, None, "intermediate"))


@gen("error_correction", 3, ["common_error", "written_reasoning"])
def d_err_line(r):
    for _ in range(400):
        a = r.randint(1, 3)
        b = _nz(r, -8, 8)
        c = _nz(r, -6, 6)
        D, s, d = formula_parts(a, b, c)
        if D <= 0 or is_sq(D) or s < 2:
            continue
        g = math.gcd(math.gcd(abs(b), s), 2 * a)
        if g < 2:
            continue
        where = r.randint(0, 3)
        if where == 0:
            Dw = b * b + 4 * a * c
            if Dw <= 0 or is_sq(Dw) or Dw == D:
                continue
        break
    else:
        raise AssertionError("no eq")
    sub = f"$x=\\dfrac{{-{par(b)}\\pm\\sqrt{{{par(b)}^2-4\\times{a}\\times{par(c)}}}}}{{2\\times{a}}}$"
    Bv, Dv = -b, D
    l2 = None
    if where == 0:
        sub = f"$x=\\dfrac{{-{par(b)}\\pm\\sqrt{{{par(b)}^2-4\\times{a}\\times{par(-c)}}}}}{{2\\times{a}}}$"
        Dv = b * b + 4 * a * c
    if where == 1:
        Bv = b
    l2 = f"$x=\\dfrac{{{Bv}\\pm\\sqrt{{{Dv}}}}}{{{2 * a}}}$"
    sv, dv = sqf(Dv)
    l3 = f"$x=\\dfrac{{{Bv}\\pm{sq_term(sv, dv)}}}{{{2 * a}}}$"
    if where == 2:
        sv = s * s
        l3 = f"$x=\\dfrac{{{Bv}\\pm{sv}\\sqrt{{{dv}}}}}{{{2 * a}}}$"
    gg = math.gcd(math.gcd(abs(Bv), sv), 2 * a)
    if where == 3:
        l4 = f"$x={ftex(Fr(Bv, 2 * a))}\\pm{sq_term(sv, dv)}$" if Fr(Bv, 2 * a).denominator == 1 else f"$x=\\dfrac{{{Bv // gg}\\pm{sq_term(sv, dv)}}}{{{2 * a // gg}}}$"
    else:
        l4 = qf(Bv, sv, dv, 2 * a)
    sol = "\n".join(f"{i + 1}行目　{t}" for i, t in enumerate([sub, l2, l3, l4]))
    LINES4 = ["1行目", "2行目", "3行目", "4行目"]
    ok = {0: "1行目は、$a$、$b$、$c$ を正しく解の公式に代入している。", 1: "2行目は、1行目の式を正しく計算している。",
          2: "3行目は、根号の中を正しく簡単にしている。", 3: "4行目は、分子のすべての項を同じ数でわって正しく約分している。"}
    why = {LINES4[i]: (ok[i], "誤りの箇所の見落とし") for i in range(4) if i != where}
    info = {0: ("1行目（$c$ の代入の符号）", "sign", "負の数をかっこなしで扱い、符号を写し間違える。"),
            1: ("2行目（$-b$ の計算）", "sign", "$-b$ に負の数が入ると正になることを見落とす。"),
            2: ("3行目（根号の外に出す数）", "calculation", "根号の外に出すとき、2乗の数のまま出してしまう。"),
            3: ("4行目（約分）", "calculation", "分子の一部の項だけを分母でわってしまう。")}[where]
    right = qf(-b, s, d, 2 * a)
    fix = f"$x=\\dfrac{{{-b}\\pm\\sqrt{{{D}}}}}{{{2 * a}}}$ より {right}"
    assert l4 != right or where == 3
    return mc(f"〔問題〕二次方程式 ${EQ(a, b, c)}$ を解の公式を使って解きなさい。\n〔Kさんの解答〕\n{sol}\nKさんの解答で，誤りが最初に生じた行として最も適するものを，" + SEL4,
              LINES4, f"誤りが最初に生じたのは{LINES4[where]}。正しくは {fix}。", d=3, p=6, keep=True, ai=where, why=why,
              err=dict(sol=sol, step=info[0], type=info[1], tempt=info[2], fix=fix),
              ap="1行ずつ自分で計算し直して比べる。$a$、$b$、$c$ の符号、$-b$ の値、根号の外に出す数、約分のしかたを順に確かめる。",
              steps=[f"$a={a}$，$b={b}$，$c={c}$。", f"$b^2-4ac={D}$，$-b={-b}$。", f"$\\sqrt{{{D}}}={sq_term(s, d)}$。", f"約分して {right}。"],
              alt=["求めた解の近似値をもとの方程式に代入し、左辺がほぼ $0$ になるかで確かめる。"],
              pc=[("誤りの行を正しく指摘している", 3), ("正しい解を求めている", 3)],
              pit=["$-b$ の符号の誤り。", "約分で一部の項だけをわる。"],
              chk=(f"{par(b)}**2-4*{a}*({c})", str(D), None, "intermediate"))


@gen("error_correction", 3, ["common_error", "condition_check"])
def d_err_word(r):
    kind = r.choice(["consec", "road", "diff"])
    if kind == "consec":
        n = r.randint(4, 15)
        N = n * (n + 1)
        prob = f"連続する2つの自然数があり，その積は ${N}$ である。小さい方の数を求めなさい。"
        sol = f"小さい方の数を $x$ とすると $x(x+1)={N}$\n$x^2+x-{N}=0$，$(x-{n})(x+{n + 1})=0$\n答え　${n}$ と $-{n + 1}$"
        right = f"$x=-{n + 1}$ は自然数ではないので，問題に適さない解を答えにふくめている。"
        fix = f"$x={n},\\ -{n + 1}$ のうち，自然数は $x={n}$。答えは ${n}$"
        cx = (f"{n}*({n}+1)", str(N))
    elif kind == "diff":
        d = r.randint(2, 8)
        x0 = r.randint(3, 12)
        P = x0 * (x0 + d)
        prob = f"大小2つの自然数があり，その差は ${d}$，積は ${P}$ である。小さい方の数を求めなさい。"
        sol = f"小さい方の数を $x$ とすると $x(x+{d})={P}$\n$x^2+{d}x-{P}=0$，$(x-{x0})(x+{x0 + d})=0$\n答え　${x0}$ と $-{x0 + d}$"
        right = f"$x=-{x0 + d}$ は自然数ではないので，問題に適さない解を答えにふくめている。"
        fix = f"自然数なので $x={x0}$。答えは ${x0}$"
        cx = (f"{x0}*({x0}+{d})", str(P))
    else:
        x0 = r.randint(1, 4)
        L = r.randint(8, 16)
        W = r.randint(L + 2, L + 12)
        S = (L - x0) * (W - x0)
        other = L + W - x0
        prob = f"縦 ${L}$ m，横 ${W}$ m の長方形の土地に，同じ幅の道を縦と横に1本ずつつくり，残りの花だんの面積を ${S}$ m² にしたい。道の幅を求めなさい。"
        sol = f"道の幅を $x$ m とすると $({L}-x)({W}-x)={S}$\n$x^2-{L + W}x+{L * W - S}=0$，$(x-{x0})(x-{other})=0$\n答え　${x0}$ m と ${other}$ m"
        right = f"道の幅は土地の縦 ${L}$ m より短いので，$x={other}$ は問題に適さない。"
        fix = f"$0<x<{L}$ なので $x={x0}$。答えは ${x0}$ m"
        cx = (f"({L}-{x0})*({W}-{x0})", str(S))
    cands = [("方程式のつくり方を誤っている。", "Kさんがつくった方程式は、問題の数量の関係を正しく表している。", "誤りの箇所の見落とし"),
             ("方程式の因数分解を誤っている。", "Kさんの因数分解は正しく、方程式の解も正しい。", "誤りの箇所の見落とし"),
             ("Kさんの解答に誤りはない。", "方程式の解が、そのまま問題の答えになるとは限らない。条件に合うかを確かめる必要がある。", "解の吟味の不足")]
    return _err_mc(f"〔問題〕{prob}", sol, right, cands, f"正しくは {fix}。",
                   dict(sol=sol, step="解の吟味", type="condition", tempt="方程式を正しく解けたことで安心し、問題の条件（自然数・長さの範囲）と照らし合わせることを忘れる。", fix=fix),
                   d=3, p=6,
                   ap="方程式の解を、問題の条件（自然数か、長さとして正しい範囲にあるか）と照らし合わせて吟味する。",
                   steps=["方程式と解は正しい。", "それぞれの解が問題の条件に合うかを調べる。", f"{fix}。"],
                   alt=["答えの数を問題文にあてはめ、すべての条件が成り立つかを確かめる。"],
                   pc=[("誤りの原因（解の吟味の不足）を指摘している", 3), ("正しい答えを求めている", 3)],
                   pit=["負の数や範囲外の値を答えにふくめる。"],
                   chk=(cx[0], cx[1], None, "intermediate"))


GENERATORS = [a_factor_solve, a_sqrt_solve, a_formula, a_is_solution, a_complete_square,
              b_expand_solve, b_param, b_number_word, b_area_word, b_formula_arrange,
              c_xy_judge, c_moving_point, c_price, c_relation,
              d_err_explain, d_err_line, d_err_word]

GENERATORS = [_robust(g) for g in GENERATORS]
