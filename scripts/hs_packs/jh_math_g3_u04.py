"""単元パック：中学3年 関数 y=ax^2（神奈川県公立高校入試形式）。"""
import re
import unicodedata
from fractions import Fraction as Fr

from banks._common import figure, mc, num
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem, tp)

UNIT_ID = "JH-MATH-G3-U04"

PREREQUISITES = [
    ("JH-MATH-G1-U04", "比例 $y=ax$ の式とグラフ、関数・変域・座標の考え方。$y=ax^2$ は「$y$ が $x^2$ に比例する」関数である。"),
    ("JH-MATH-G2-U03", "一次関数の変化の割合と直線の式の求め方。放物線上の2点を通る直線の式や、変化の割合の比較に使う。"),
    ("JH-MATH-G3-U03", "二次方程式の解き方。$y$ の値から $x$ の値を求めたり、放物線と直線の交点を求めたりするときに使う。"),
]
EXTENSIONS = [
    ("HS-MATH1-U03", "高校の二次関数 $y=a(x-p)^2+q$ で、放物線の平行移動・最大値と最小値・二次不等式へ発展する。"),
    ("HS-MATH2-U06", "高校の微分法で、変化の割合の考えを「区間を限りなく小さくした変化の割合（微分係数）」へ発展させる。"),
    ("JH-MATH-G3-U07", "三平方の定理と組み合わせ、放物線上の点どうしの距離や図形の性質を調べる。"),
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


def fpy(v):
    v = Fr(v)
    return str(v.numerator) if v.denominator == 1 else f"Rational({v.numerator},{v.denominator})"


def par(v):
    s = ftex(v)
    return f"({s})" if Fr(v) < 0 else s


def MARK(stem, v, e, expr, **kw):
    """あいう方式（0〜9 のマーク）で答える数値問題。v は 0 以上の整数か既約分数。"""
    v = Fr(v)
    assert v >= 0
    if v.denominator == 1:
        n = int(v)
        return num(stem, str(n), e, mark=("int", n), chk=(expr, str(n), None, "answer"), **kw)
    p, q = v.numerator, v.denominator
    return num(stem, f"${ftex(v)}$", e, mark=("frac", p, q), chk=(expr, f"Rational({p},{q})", None, "answer"), **kw)


def axx(a):
    """ax^2 の表記。"""
    a = Fr(a)
    if a == 1:
        return "x^2"
    if a == -1:
        return "-x^2"
    if a.denominator == 1:
        return f"{a.numerator}x^2"
    return f"{'-' if a < 0 else ''}\\dfrac{{{abs(a.numerator)}}}{{{a.denominator}}}x^2"


def Y(a):
    return f"y={axx(a)}"


def rhs(m, b):
    m, b = Fr(m), Fr(b)
    if m == 0:
        return ftex(b)
    s = "x" if m == 1 else "-x" if m == -1 else f"{ftex(m)}x"
    if b > 0:
        s += "+" + ftex(b)
    elif b < 0:
        s += ftex(b)
    return s


def L(m, b):
    return f"$y={rhs(m, b)}$"


def pt(x, y):
    return f"({ftex(x)},\\,{ftex(y)})"


SEL4 = "次の1〜4の中から1つ選び，その番号を答えなさい。"
A_POS = [Fr(1), Fr(2), Fr(3), Fr(1, 2), Fr(1, 3), Fr(1, 4), Fr(2, 3), Fr(3, 2), Fr(3, 4)]
A_ALL = A_POS + [-a for a in A_POS]


def nz(r, lo, hi, excl=(0,)):
    return r.choice([v for v in range(lo, hi + 1) if v not in excl])


def parab_svg(curves, pts=(), segs=(), xr=(-5, 5), yr=(-1, 10), W=230, H=210, labels=()):
    """放物線の図（入試の図と同じく目もりなし。x・y 方向の縮尺は別々）。curves=[(a, ラベル)]。"""
    pad = 16
    x0, x1 = xr
    y0, y1 = yr
    sx = (W - 2 * pad) / (x1 - x0)
    sy = (H - 2 * pad) / (y1 - y0)
    X = lambda x: pad + (float(x) - x0) * sx  # noqa: E731
    Yc = lambda y: pad + (y1 - float(y)) * sy  # noqa: E731
    f = lambda v: f"{v:.1f}"  # noqa: E731
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="serif" font-size="12">',
           '<defs><marker id="pa" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#000"/></marker></defs>',
           f'<line x1="{f(X(x0))}" y1="{f(Yc(0))}" x2="{f(X(x1) + 4)}" y2="{f(Yc(0))}" stroke="#000" marker-end="url(#pa)"/>',
           f'<line x1="{f(X(0))}" y1="{f(Yc(y0))}" x2="{f(X(0))}" y2="{f(Yc(y1) - 4)}" stroke="#000" marker-end="url(#pa)"/>',
           f'<text x="{f(X(x1) - 2)}" y="{f(Yc(0) + 14)}" font-style="italic">x</text>',
           f'<text x="{f(X(0) + 5)}" y="{f(Yc(y1) + 2)}" font-style="italic">y</text>',
           f'<text x="{f(X(0) - 12)}" y="{f(Yc(0) + 13)}">O</text>']
    for a, lab in curves:
        a = float(a)
        d, n = [], 160
        for i in range(n + 1):
            x = x0 + (x1 - x0) * i / n
            y = a * x * x
            if y0 <= y <= y1:
                d.append((X(x), Yc(y)))
            elif d and d[-1] is not None:
                d.append(None)
        paths, cur = [], []
        for p in d:
            if p is None:
                if len(cur) > 1:
                    paths.append(cur)
                cur = []
            else:
                cur.append(p)
        if len(cur) > 1:
            paths.append(cur)
        for c in paths:
            out.append('<path d="M' + " L".join(f"{f(px)},{f(py)}" for px, py in c) + '" fill="none" stroke="#000" stroke-width="1.4"/>')
        if lab and paths:
            px, py = paths[-1][-1]
            out.append(f'<text x="{f(min(px + 3, W - 14))}" y="{f(py + 12 if a > 0 else py - 4)}">{lab}</text>')
    for (ax, ay), (bx, by) in segs:
        out.append(f'<line x1="{f(X(ax))}" y1="{f(Yc(ay))}" x2="{f(X(bx))}" y2="{f(Yc(by))}" stroke="#000" stroke-width="1"/>')
    for x, y, lab in pts:
        out.append(f'<circle cx="{f(X(x))}" cy="{f(Yc(y))}" r="2.3" fill="#000"/>')
        if lab:
            out.append(f'<text x="{f(X(x) + 5)}" y="{f(Yc(y) + 4 if float(x) >= 0 else Yc(y) - 5)}">{lab}</text>')
    for x, y, t in labels:
        out.append(f'<text x="{f(X(x))}" y="{f(Yc(y))}">{t}</text>')
    out.append("</svg>")
    return "".join(out)


def ab_fig(a, p, q, extra=(), extra_segs=()):
    """放物線 y=ax^2 上の2点 A(p, ap^2)、B(q, aq^2) と直線 AB の図。"""
    ya, yb = a * p * p, a * q * q
    xm = max(abs(p), abs(q)) + 1.2
    ymax = float(max(ya, yb)) * 1.15 + 0.5
    m, n = a * (p + q), -a * p * q
    xs = [-xm, xm]
    seg_pts = [(x, m * Fr(x).limit_denominator(1000) + n) for x in (p - (q - p) * Fr(1, 6), q + (q - p) * Fr(1, 6))]
    pts = [(p, ya, "A"), (q, yb, "B")] + list(extra)
    return figure(f"放物線 {Y(a)} と、放物線上の2点 A、B を通る直線",
                  parab_svg([(a, "")], pts=pts, segs=[(seg_pts[0], seg_pts[1])] + list(extra_segs),
                            xr=(xs[0], xs[1]), yr=(-ymax * 0.12, ymax)))


# ----------------------------------------------------------------------
# 授業プリント
# ----------------------------------------------------------------------

_LESSON_FIG = figure("y=x^2、y=2x^2、y=-x^2 のグラフ",
                     parab_svg([(1, "y=x²"), (2, "y=2x²"), (-1, "y=−x²")], xr=(-3.2, 3.2), yr=(-6, 8), W=230, H=230))
_EX_FIG = figure("放物線 y=1/2 x^2 上の2点 A(−2, 2)、B(4, 8) と直線 AB",
                 parab_svg([(Fr(1, 2), "")], pts=[(-2, 2, "A"), (4, 8, "B")], segs=[((-3, 1), (5, 9))], xr=(-5, 5.5), yr=(-1.2, 10)))

LESSON = lesson(
    goals=["$y$ が $x$ の2乗に比例する関数 $y=ax^2$ の意味を理解し、式・表・グラフで表すことができる。",
           "$y=ax^2$ のグラフ（放物線）の特徴、変域、変化の割合を、一次関数と比べながら説明できる。",
           "放物線と直線の交点・三角形の面積や、身のまわりの「2乗に比例する」事象の問題を解くことができる。"],
    duration=100,
    readiness=["比例 $y=ax$ の式を、1組の $x$、$y$ の値から求められる。",
               "一次関数の変化の割合と、2点を通る直線の式を求められる。",
               "二次方程式 $x^2=k$ や $ax^2+bx+c=0$ を解くことができる。"],
    flow=[("導入：転がるボール", 10, "斜面を転がるボールの時間と距離の表から、$x$ が2倍・3倍になると $y$ が4倍・9倍になることを見つける"),
          ("2乗に比例する関数", 10, "$y=ax^2$ の定義、比例定数の求め方"),
          ("グラフ（放物線）の特徴", 20, "表から点をとってグラフをかき、軸・頂点・開き方・$a$ の符号との関係をまとめる"),
          ("変域", 15, "$x$ の変域に $0$ をふくむときの $y$ の変域（例題1）"),
          ("変化の割合", 20, "変化の割合 $a(p+q)$ を導き、一次関数と比べる（例題2）"),
          ("放物線と直線・まとめ", 25, "2点を通る直線の式と三角形の面積（例題3）、確認問題")],
    sections=[
        intro("in1", "斜面を転がるボールの距離",
              "なめらかな斜面でボールを静かに転がすと、転がり始めてからの時間 $x$ 秒と転がった距離 $y$ m について、次のような関係が見られた（架空の測定値）。$x=1$ のとき $y=2$、$x=2$ のとき $y=8$、$x=3$ のとき $y=18$。",
              bullets=["$x$ が $2$ 倍、$3$ 倍になると、$y$ は $4$ 倍、$9$ 倍になる。", "$\\dfrac{y}{x^2}$ を計算すると、どれも $2$ で一定。つまり $y=2x^2$ と表せる。", "比例とも一次関数ともちがう、新しい関数である。"],
              points=[tp("表を板書し、$\\dfrac{y}{x}$ と $\\dfrac{y}{x^2}$ の両方を計算させて、一定になるのはどちらかを調べさせる。", ask="$y$ は $x$ に比例しているか。", expect="$\\dfrac{y}{x}$ が $2,\\ 4,\\ 6$ と変わるので比例ではない。$\\dfrac{y}{x^2}$ は $2$ で一定。", timing="導入の最初"),
                      tp("「$x$ が $n$ 倍になると $y$ は $n^2$ 倍」という言い方を、面積（正方形の1辺と面積）の例とも結びつける。")]),
        definition("df1", "2乗に比例する関数",
                   "$y$ が $x$ の関数で、$y=ax^2$（$a$ は $0$ でない定数）と表されるとき、$y$ は $x$ の2乗に比例するという。$a$ を比例定数という。",
                   formula="$$y=ax^2\\qquad(a\\neq0),\\qquad a=\\dfrac{y}{x^2}$$",
                   conditions=["$x$ の値が $n$ 倍になると、$y$ の値は $n^2$ 倍になる。", "1組の $x$、$y$ の値（$x\\neq0$）がわかれば、$a=\\dfrac{y}{x^2}$ で比例定数が求められる。",
                               "$x$ と $-x$ に対する $y$ の値は等しい（$a(-x)^2=ax^2$）。"],
                   points=[tp("比例 $y=ax$ との違いを、$a=\\dfrac{y}{x}$ と $a=\\dfrac{y}{x^2}$ の対比で板書する。", caution="比例定数を $\\dfrac{y}{x}$ で求める誤りが多い。")]),
        theorem("th1", "$y=ax^2$ のグラフの特徴",
                "$$y=ax^2\\ \\text{のグラフは、原点を頂点とし、}y\\text{ 軸を軸とする放物線}$$",
                ["原点を通り、$y$ 軸について対称な曲線（放物線）である。", "$a>0$ のとき上に開き、$y\\geqq0$。$a<0$ のとき下に開き、$y\\leqq0$。",
                 "$a$ の絶対値が大きいほど、グラフの開き方は小さい。", "$y=ax^2$ と $y=-ax^2$ のグラフは、$x$ 軸について対称である。",
                 "$a>0$ のとき、$x<0$ の範囲では $x$ が増加すると $y$ は減少し、$x>0$ の範囲では増加する。"],
                body="右の図は $y=x^2$、$y=2x^2$、$y=-x^2$ のグラフである。$y=2x^2$ は同じ $x$ に対して $y=x^2$ の $2$ 倍の高さになるので、開き方が小さくなる。",
                figure=_LESSON_FIG,
                points=[tp("表から点をとってなめらかな曲線で結ばせる。折れ線にしたり、原点付近をとがらせたりしないよう注意する。", ask="$x=0.5$ のとき $y=x^2$ の値はいくつか。", expect="$0.25$。原点付近はなだらかになる。")]),
        derivation("dv1", "$y=ax^2$ の変化の割合を導く",
                   ["$x$ の値が $p$ から $q$ まで増加するとき（$p\\neq q$）、$y$ の値は $ap^2$ から $aq^2$ まで変わる。",
                    "$y$ の増加量は $aq^2-ap^2=a(q^2-p^2)=a(q+p)(q-p)$（因数分解）。",
                    "変化の割合 $=\\dfrac{a(q+p)(q-p)}{q-p}=a(p+q)$。",
                    "したがって、$y=ax^2$ の変化の割合は一定ではなく、$x$ の範囲によって変わる。これは、グラフが直線でなく曲線であることを表している。",
                    "変化の割合 $a(p+q)$ は、グラフ上の2点 $(p,\\,ap^2)$、$(q,\\,aq^2)$ を通る直線の傾きに等しい。"],
                   points=[tp("$y=x^2$ で $1\\to3$、$3\\to5$ の変化の割合を数値で求め（$4$、$8$）、一定でないことを確かめてから文字で導く。", ask="一次関数の変化の割合と何がちがうか。", expect="一次関数はいつも $a$ で一定、$y=ax^2$ は範囲で変わる。")]),
        example("ex1", "例題1　変域",
                "関数 $y=2x^2$ で、$x$ の変域が $-1\\leqq x\\leqq3$ のときの $y$ の変域を求めなさい。",
                ["$x$ の変域に $0$ がふくまれるので、$x=0$ のとき $y$ は最小値 $0$ をとる。", "$x=-1$ のとき $y=2$、$x=3$ のとき $y=18$。大きい方の $18$ が最大値。", "$y$ の変域は $0\\leqq y\\leqq18$。"],
                "$0\\leqq y\\leqq18$",
                thinking="グラフをかいて、$x$ の変域の部分だけをなぞる。変域に $0$ がふくまれると、頂点（原点）が最小（または最大）になる。",
                points=[tp("両端だけを代入して $2\\leqq y\\leqq18$ とする誤りを示し、グラフのなぞり書きで確かめさせる。")],
                misconceptions=[("$x=-1$、$x=3$ を代入して $2\\leqq y\\leqq18$", "変域に $x=0$ がふくまれるので最小値は $0$。$0\\leqq y\\leqq18$")]),
        example("ex2", "例題2　変化の割合",
                "関数 $y=-x^2$ で、$x$ の値が $1$ から $4$ まで増加するときの変化の割合を求めなさい。",
                ["$x=1$ のとき $y=-1$、$x=4$ のとき $y=-16$。", "変化の割合 $=\\dfrac{-16-(-1)}{4-1}=\\dfrac{-15}{3}=-5$。", "公式 $a(p+q)=-1\\times(1+4)=-5$ でも確かめられる。"],
                "$-5$",
                thinking="変化の割合は $\\dfrac{y\\text{ の増加量}}{x\\text{ の増加量}}$。一次関数と同じ定義で計算する。",
                points=[tp("公式 $a(p+q)$ は検算として使わせ、まずは定義どおりの計算を書かせる。", timing="例題2のあと")]),
        example("ex3", "例題3　放物線と直線",
                "放物線 $y=\\dfrac{1}{2}x^2$ 上に2点 A、B があり、$x$ 座標はそれぞれ $-2$、$4$ である。直線 AB の式と、$\\triangle\\mathrm{OAB}$ の面積を求めなさい。",
                ["A $(-2,\\,2)$、B $(4,\\,8)$。", "傾き $=\\dfrac{8-2}{4-(-2)}=1$。$y=x+b$ に A を代入して $b=4$。直線 AB は $y=x+4$。",
                 "直線 AB と $y$ 軸の交点を C $(0,\\,4)$ とすると、$\\triangle\\mathrm{OAB}=\\triangle\\mathrm{OAC}+\\triangle\\mathrm{OBC}$。",
                 "$=\\dfrac{1}{2}\\times4\\times2+\\dfrac{1}{2}\\times4\\times4=4+8=12$。"],
                "$y=x+4$、面積 $12$",
                thinking="$y$ 軸で三角形を2つに分けると、底辺を OC（切片）、高さを A、B の $x$ 座標の絶対値にできる。",
                figure=_EX_FIG,
                points=[tp("傾きが変化の割合 $a(p+q)=\\dfrac{1}{2}\\times2=1$ と一致することを確認し、検算のしかたとして紹介する。")]),
        board("bd1", "板書案",
              [("① $y=ax^2$", ["$y$ は $x^2$ に比例", "$a=\\dfrac{y}{x^2}$", "$x$ が $n$ 倍 → $y$ は $n^2$ 倍", "グラフは放物線（頂点 O、軸は $y$ 軸）", "$a>0$ 上に開く、$a<0$ 下に開く"]),
               ("② 変域・変化の割合", ["変域に $0$ をふくむ → 最小（最大）は $0$", "例：$-1\\leqq x\\leqq3$ → $0\\leqq y\\leqq18$", "変化の割合 $=a(p+q)$", "一定ではない（一次関数との違い）"]),
               ("③ 放物線と直線", ["A $(p,\\,ap^2)$、B $(q,\\,aq^2)$", "傾き $a(p+q)$、切片 $-apq$", "$\\triangle\\mathrm{OAB}=\\dfrac{1}{2}\\times\\text{切片}\\times(q-p)$", "等積変形：O を通り AB に平行な直線"])],
              points=[tp("③の面積の公式は暗記させるのではなく、$y$ 軸で2つに分ける考え方とセットで板書する。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("$x$ の変域に $0$ をふくむかどうかを、毎回グラフをかいて確かめさせる。", caution="入試で最も多い誤答。両端の値だけで判断しない。"),
               tp("負の数を代入するときは $a\\times(-2)^2$ のようにかっこをつけさせる。", ask="$y=3x^2$ で $x=-2$ のとき $y$ はいくつか。", expect="$3\\times(-2)^2=12$。$-12$ ではない。"),
               tp("変化の割合は「2点を通る直線の傾き」であることをグラフで示し、一次関数との共通点と相違点を整理する。", timing="変化の割合の後"),
               tp("放物線と直線の問題では、まず点の座標を求めて図にかきこむ習慣をつける。")],
              misconceptions=[("比例定数を $a=\\dfrac{y}{x}$ で求める", "$y=ax^2$ では $a=\\dfrac{y}{x^2}$"),
                              ("$y=2x^2$、$-1\\leqq x\\leqq3$ のとき $2\\leqq y\\leqq18$", "$x=0$ で最小値 $0$ をとるので $0\\leqq y\\leqq18$"),
                              ("$y=ax^2$ の変化の割合はいつも $a$", "$x$ の範囲によって変わり、$a(p+q)$")]),
        summary("sm1", "まとめ",
                ["$y=ax^2$：$y$ は $x$ の2乗に比例。比例定数は $a=\\dfrac{y}{x^2}$。",
                 "グラフは原点を頂点、$y$ 軸を軸とする放物線。$a>0$ で上に開き、$|a|$ が大きいほど開き方が小さい。",
                 "変域に $x=0$ をふくむとき、$y$ の最小値（$a<0$ なら最大値）は $0$。",
                 "変化の割合は一定でなく、$x$ が $p$ から $q$ まで増加するとき $a(p+q)$。",
                 "放物線上の2点を通る直線は、傾き $a(p+q)$、切片 $-apq$。"]),
        check("ck1", "確認問題",
              [("$y$ は $x$ の2乗に比例し、$x=3$ のとき $y=-18$ である。$y$ を $x$ の式で表しなさい。", "$a=\\dfrac{-18}{9}=-2$ より $y=-2x^2$"),
               ("関数 $y=x^2$ で、$x$ の変域が $-3\\leqq x\\leqq2$ のときの $y$ の変域を求めなさい。", "$0\\leqq y\\leqq9$"),
               ("関数 $y=2x^2$ で、$x$ の値が $1$ から $3$ まで増加するときの変化の割合を求めなさい。", "$2\\times(1+3)=8$"),
               ("放物線 $y=x^2$ 上の2点 A $(-1,\\,1)$、B $(2,\\,4)$ を通る直線の式を求めなさい。", "$y=x+2$")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

@gen("basic_check", 4, ["computation", "concept"])
def a_find_a(r):
    a = r.choice(A_ALL)
    p = r.choice([v for v in range(-8, 9) if abs(v) >= 2 and (a * v * v).denominator == 1])
    q = a * p * p
    form = r.choice(["xy", "pt"])
    stem = (f"$y$ は $x$ の2乗に比例し，$x={p}$ のとき $y={ftex(q)}$ である。$y$ を $x$ の式で表したものとして正しいものを，" if form == "xy"
            else f"関数 $y=ax^2$ のグラフが点 ${pt(p, q)}$ を通るとき，この関数の式として正しいものを，")
    cands = [(f"${Y(Fr(q) / p)}$", "$a=\\dfrac{y}{x}$ で求めている。$y=ax^2$ では $a=\\dfrac{y}{x^2}$。", "比例との混同"),
             (f"${Y(Fr(p * p) / q)}$", "$a=\\dfrac{x^2}{y}$ と、分子と分母を逆にしている。", "比例定数の求め方の誤り"),
             (f"${Y(-a)}$", f"${par(p)}^2$ の符号を誤っている。負の数の2乗は正の数。" if p < 0 else "比例定数の符号を誤っている。", "符号の誤り"),
             (f"${Y(Fr(q) / (2 * p))}$", "$x^2$ を $2x$ と計算している。", "累乗の意味の誤り"),
             (f"${Y(q * p * p)}$", "$y$ に $x^2$ をかけている。", "比例定数の求め方の誤り")]
    return MC(stem + SEL4, f"${Y(a)}$", cands, f"$a=\\dfrac{{{ftex(q)}}}{{{par(p)}^2}}=\\dfrac{{{ftex(q)}}}{{{p * p}}}={ftex(a)}$。よって ${Y(a)}$。", d=2,
              ap="$y=ax^2$ に $x$、$y$ の値を代入して $a$ を求める。$a=\\dfrac{y}{x^2}$。",
              steps=[f"$y=ax^2$ に $x={p}$，$y={ftex(q)}$ を代入：${ftex(q)}=a\\times{par(p)}^2$。", f"${ftex(q)}={p * p}a$ より $a={ftex(a)}$。", f"${Y(a)}$。"],
              alt=[f"求めた式に $x={p}$ を代入して $y={ftex(q)}$ になるかを確かめる。"],
              pc=[("$y=ax^2$ に正しく代入している", 1), ("$a$ を正しく求めている", 1)],
              pit=["$a=\\dfrac{y}{x}$ と比例の式で求めてしまう。", "負の数の2乗を負にする。"],
              chk=(f"Rational({q.numerator},{p * p})", fpy(a), None, "intermediate"))


@gen("basic_check", 4, ["computation", "concept"])
def a_value(r):
    kind = r.choice(["val", "val", "times"])
    if kind == "val":
        a = r.choice(A_ALL)
        ok = [v for v in range(-9, 10) if abs(v) >= 2 and (a * v * v).denominator == 1]
        p = r.choice(ok)
        s = r.choice([v for v in ok if abs(v) != abs(p)])
        q, ans = a * p * p, a * s * s
        cands = [(f"$y={ftex(-ans)}$", f"${par(s)}^2$ を負の数にしている。" if s < 0 else "符号を誤っている。", "符号の誤り"),
                 (f"$y={ftex(a * s)}$", "$x^2$ でなく $x$ をかけている。", "比例との混同"),
                 (f"$y={ftex(q * Fr(s, p))}$", f"$x$ が ${ftex(Fr(s, p))}$ 倍になると $y$ も同じ倍率になると考えている。$y$ は $\\left({ftex(Fr(s, p))}\\right)^2$ 倍になる。", "比例との混同"),
                 (f"$y={ftex(a * 2 * s)}$", "$x^2$ を $2x$ と計算している。", "累乗の意味の誤り")]
        return MC(f"$y$ は $x$ の2乗に比例し，$x={p}$ のとき $y={ftex(q)}$ である。$x={s}$ のときの $y$ の値として正しいものを，" + SEL4, f"$y={ftex(ans)}$", cands,
                  f"$a=\\dfrac{{{ftex(q)}}}{{{p * p}}}={ftex(a)}$。${Y(a)}$ に $x={s}$ を代入して $y={ftex(a)}\\times{par(s)}^2={ftex(ans)}$。", d=2,
                  ap="まず比例定数 $a$ を求めて式をつくり、その式に $x$ の値を代入する。",
                  steps=[f"$a=\\dfrac{{{ftex(q)}}}{{{par(p)}^2}}={ftex(a)}$。", f"${Y(a)}$ に $x={s}$ を代入。", f"$y={ftex(a)}\\times{s * s}={ftex(ans)}$。"],
                  alt=[f"$x$ が ${ftex(Fr(s, p))}$ 倍になると $y$ は $\\left({ftex(Fr(s, p))}\\right)^2={ftex(Fr(s * s, p * p))}$ 倍になる、と考えても求められる。"],
                  pc=[("比例定数を正しく求めている", 1), ("$y$ の値を正しく求めている", 1)],
                  pit=["負の数の2乗の符号の誤り。", "$x$ の倍率と $y$ の倍率を同じにする。"],
                  chk=(f"{fpy(a)}*({s})**2", fpy(ans), None, "intermediate"))
    n = r.choice([2, 3, 4, 5, Fr(1, 2), Fr(1, 3), Fr(3, 2)])
    words = {2: "2倍", 3: "3倍", 4: "4倍", 5: "5倍", Fr(1, 2): "$\\dfrac{1}{2}$ 倍", Fr(1, 3): "$\\dfrac{1}{3}$ 倍", Fr(3, 2): "$\\dfrac{3}{2}$ 倍"}
    a = r.choice(A_ALL)

    def w(v):
        v = Fr(v)
        return f"${v.numerator}$ 倍" if v.denominator == 1 else f"$\\dfrac{{{v.numerator}}}{{{v.denominator}}}$ 倍"
    cands = [(w(n), "比例 $y=ax$ と同じように考えている。$y=ax^2$ では倍率が2乗になる。", "比例との混同"),
             (w(2 * n), "$n^2$ を $2n$ と計算している。", "累乗の意味の誤り"),
             (w(n ** 3), "3乗している。", "累乗の意味の誤り"),
             (w(1 / n), "反比例と混同している。", "反比例との混同"),
             (w(Fr(1) / (n * n)), "反比例と混同し、さらに2乗している。", "反比例との混同")]
    return MC(f"関数 ${Y(a)}$ で，$x$ の値が {words[n]}になると，$y$ の値は何倍になるか。正しいものを，" + SEL4, w(n * n), cands,
              f"$x$ を $nx$ にすると $y=a(nx)^2=n^2\\times ax^2$。$n={ftex(n)}$ なので $y$ は ${ftex(n * n)}$ 倍。", d=2,
              ap="$y=ax^2$ で $x$ を $n$ 倍にすると $y=a(nx)^2=n^2ax^2$。比例定数 $a$ の値には関係しない。",
              steps=["$x$ を $nx$ におきかえる。", "$a(nx)^2=n^2ax^2$。", f"$n={ftex(n)}$ なので ${ftex(n * n)}$ 倍。"],
              alt=["具体的な値（たとえば $x=1$ と $x=" + ftex(n) + "$）を代入して $y$ の値を比べる。"],
              pc=[("$x$ を $n$ 倍した式を考えている", 1), ("倍率を正しく求めている", 1)],
              pit=["比例と同じく $n$ 倍と答える。", "$a$ の値によって倍率が変わると考える。"],
              chk=(f"({fpy(n)})**2", fpy(n * n), None, "intermediate"))


@gen("basic_check", 4, ["computation"])
def a_rate(r):
    a = r.choice(A_ALL)
    while True:
        p = r.randint(-6, 5)
        q = p + r.randint(1, 5)
        if p + q != 0 and (a * p * p).denominator == 1 and (a * q * q).denominator == 1:
            break
        if (a * (p + q)).denominator == 1 and p + q != 0 and r.random() < 0.3:
            break
    ans = a * (p + q)
    yp, yq = a * p * p, a * q * q
    cands = [(f"${ftex(a * (q * q - p * p))}$", "$y$ の増加量を答えている。$x$ の増加量でわる必要がある。", "変化の割合と増加量の混同"),
             (f"${ftex(a)}$", "一次関数と同じように、変化の割合を比例定数 $a$ だと考えている。", "一次関数との混同"),
             (f"${ftex(-ans)}$", "ひく順番が分子と分母でそろっていない。", "符号の誤り"),
             (f"${ftex(a * (q - p))}$", "$a(q-p)$ と公式を覚え違えている。正しくは $a(p+q)$。", "公式の覚え違い"),
             (f"${ftex(a * (q * q + p * p) / (q - p))}$", "$y$ の値の差でなく和を使っている。", "増加量の意味の誤解")]
    return MC(f"関数 ${Y(a)}$ について，$x$ の値が ${p}$ から ${q}$ まで増加するときの変化の割合として正しいものを，" + SEL4, f"${ftex(ans)}$", cands,
              f"$x={p}$ のとき $y={ftex(yp)}$，$x={q}$ のとき $y={ftex(yq)}$。変化の割合 $=\\dfrac{{{ftex(yq)}-{par(yp)}}}{{{q}-{par(p)}}}={ftex(ans)}$。", d=2,
              ap="変化の割合 $=\\dfrac{y\\text{ の増加量}}{x\\text{ の増加量}}$。$y=ax^2$ では $a(p+q)$ で検算できる。",
              steps=[f"$x={p}$ のとき $y={ftex(yp)}$，$x={q}$ のとき $y={ftex(yq)}$。", f"$y$ の増加量 ${ftex(yq - yp)}$，$x$ の増加量 ${q - p}$。", f"変化の割合 $={ftex(ans)}$。"],
              alt=[f"公式 $a(p+q)={ftex(a)}\\times({p}{'+' if q >= 0 else ''}{q})={ftex(ans)}$ でも確かめられる。"],
              pc=[("$y$ の値を正しく求めている", 1), ("変化の割合を正しく求めている", 1)],
              pit=["$y$ の増加量を答えにする。", "変化の割合をいつも $a$ だと思う。"],
              chk=(f"({fpy(yq)}-({fpy(yp)}))/({q}-({p}))", fpy(ans), None, "intermediate"))


def _graph_statements(r):
    a = r.choice([Fr(1, 2), Fr(1), Fr(2), Fr(3), Fr(1, 3), Fr(3, 2)])
    b = r.choice([v for v in A_POS if v != a])
    big, small = max(a, b), min(a, b)
    T = [(f"関数 ${Y(-a)}$ のグラフは下に開いた放物線である。", "比例定数が負なので、グラフは下に開く。"),
         (f"関数 ${Y(a)}$ のグラフは $y$ 軸について対称である。", "$x$ と $-x$ に対する $y$ の値が等しいので、$y$ 軸について対称。"),
         (f"関数 ${Y(a)}$ と ${Y(-a)}$ のグラフは $x$ 軸について対称である。", "同じ $x$ に対する $y$ の値の符号が逆なので、$x$ 軸について対称。"),
         (f"関数 ${Y(big)}$ のグラフは，${Y(small)}$ のグラフより開き方が小さい。", "比例定数の絶対値が大きいほど開き方は小さい。"),
         (f"関数 ${Y(a)}$ で，$x<0$ の範囲では，$x$ の値が増加すると $y$ の値は減少する。", "$a>0$ のとき、$x<0$ の範囲ではグラフは右下がり。"),
         (f"関数 ${Y(-a)}$ の $y$ の値は，$0$ 以下である。", "$x^2\\geqq0$ に負の数をかけるので $y\\leqq0$。")]
    F = [(f"関数 ${Y(a)}$ のグラフは $x$ 軸について対称である。", "$y=ax^2$ のグラフは $y$ 軸について対称。"),
         (f"関数 ${Y(a)}$ の変化の割合は，いつも ${ftex(a)}$ である。", "変化の割合は $x$ の範囲によって変わり一定ではない。"),
         (f"関数 ${Y(small)}$ のグラフは，${Y(big)}$ のグラフより開き方が小さい。", "比例定数が小さい方が開き方は大きい。"),
         (f"関数 ${Y(a)}$ で，$x$ の値が増加すると $y$ の値はいつも増加する。", "$x<0$ の範囲では、$x$ が増加すると $y$ は減少する。"),
         (f"関数 ${Y(-a)}$ のグラフは上に開いた放物線である。", "比例定数が負なので、下に開く。"),
         (f"関数 ${Y(a)}$ のグラフは，点 $(1,\\,{ftex(-a)})$ を通る。", f"$x=1$ のとき $y={ftex(a)}$ なので、点 $(1,\\,{ftex(a)})$ を通る。"),
         (f"関数 ${Y(a)}$ のグラフは直線である。", "$y=ax^2$ のグラフは放物線という曲線である。")]
    return T, F


@gen("basic_check", 4, ["concept", "condition_check"])
def a_graph_props(r):
    T, F = _graph_statements(r)
    want_true = r.random() < 0.6
    if want_true:
        right = r.choice(T)
        wr = r.sample(F, 3)
        stem = "関数 $y=ax^2$ のグラフや性質について述べた文として正しいものを，"
        cands = [(t, why, "放物線の性質の誤解") for t, why in wr]
    else:
        right = r.choice(F)
        wr = r.sample(T, 3)
        stem = "関数 $y=ax^2$ のグラフや性質について述べた文として誤っているものを，"
        cands = [(t, "この文は正しい。" + why, "放物線の性質の誤解") for t, why in wr]
    return MC(stem + SEL4, right[0], cands, ("正しい。" if want_true else "誤り。") + right[1], d=2,
              ap="放物線の性質（頂点が原点、$y$ 軸について対称、$a$ の符号で開く向き、$|a|$ で開き方）に照らして判断する。迷ったら簡単なグラフをかく。",
              steps=["それぞれの文を、グラフの性質と照らし合わせる。", right[1], "条件に合うものを選ぶ。"],
              alt=["具体的な $x$ の値（$-2,\\ -1,\\ 0,\\ 1,\\ 2$）で表をつくり、文の内容が成り立つかを確かめる。"],
              pc=[("グラフの性質を根拠にしている", 1), ("正しく選んでいる", 1)],
              pit=["$y=ax^2$ でも変化の割合が一定だと考える。", "比例定数が大きいほど開き方も大きいと考える。"])


def _ineq(lo, hi):
    return f"${ftex(lo)}\\leqq y\\leqq {ftex(hi)}$"


@gen("basic_check", 4, ["condition_check", "computation"])
def a_domain(r):
    a = r.choice([Fr(v) for v in (1, 2, 3, -1, -2, -3)] + [Fr(1, 2), Fr(-1, 2)])
    while True:
        p = r.randint(-5, 1)
        q = r.randint(max(p + 2, 1), 5)
        if p < 0 < q and abs(p) != abs(q) and (a * p * p).denominator == 1 and (a * q * q).denominator == 1:
            break
    yp, yq = a * p * p, a * q * q
    if a > 0:
        lo, hi = Fr(0), max(yp, yq)
    else:
        lo, hi = min(yp, yq), Fr(0)
    naive = (min(yp, yq), max(yp, yq))
    cands = [(_ineq(*naive), "$x$ の変域の両端の値だけで判断している。変域に $x=0$ がふくまれるので、" + ("最小値は $0$。" if a > 0 else "最大値は $0$。"), "変域に0をふくむ場合の見落とし"),
             (_ineq(min(-yp, -yq, 0), max(-yp, -yq, 0)), "符号を逆にして計算している。", "符号の誤り"),
             (_ineq(a * p, a * q) if a * p < a * q else _ineq(a * q, a * p), "$x^2$ でなく $x$ をかけて計算している。", "比例との混同"),
             ((_ineq(Fr(0), min(yp, yq)) if a > 0 else _ineq(max(yp, yq), Fr(0))), "$x=0$ から遠い方の端で $y$ の" + ("最大値" if a > 0 else "最小値") + "をとることを見落とし、近い方の端の値を使っている。", "変域の端のとらえ違い"),
             (_ineq(Fr(p), Fr(q)), "$x$ の変域をそのまま $y$ の変域にしている。", "変域の意味の誤解")]
    return MC(f"関数 ${Y(a)}$ について，$x$ の変域が ${p}\\leqq x\\leqq {q}$ のときの $y$ の変域として正しいものを，" + SEL4, _ineq(lo, hi), cands,
              f"$x=0$ をふくむので，$x=0$ のとき $y$ は{'最小値' if a > 0 else '最大値'} $0$。$x={p}$ のとき $y={ftex(yp)}$，$x={q}$ のとき $y={ftex(yq)}$。$y$ の変域は {_ineq(lo, hi)}。", d=2,
              ap="グラフをかいて、$x$ の変域の部分だけをなぞる。$x$ の変域に $0$ がふくまれると、原点（頂点）で $y$ が最小（$a<0$ なら最大）になる。",
              steps=[f"$x$ の変域 ${p}\\leqq x\\leqq {q}$ は $x=0$ をふくむ。", f"$x=0$ のとき $y=0$。$x={p}$ のとき $y={ftex(yp)}$，$x={q}$ のとき $y={ftex(yq)}$。", f"{_ineq(lo, hi)}。"],
              alt=["$x=" + str(p) + ",\\ \\cdots,\\ " + str(q) + "$ の表をつくり、$y$ の最小・最大を読みとる。"],
              pc=[("$x=0$ をふくむことに注目している", 1), ("変域を正しく求めている", 1)],
              pit=["両端の値だけで $y$ の変域を決める。", "$a<0$ のとき、最大値と最小値を逆にする。"],
              chk=(f"Max({fpy(yp)},{fpy(yq)},0)", fpy(hi), None, "intermediate"))


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 4, ["condition_check", "computation"])
def b_domain_a(r):
    kind = r.choice(["a", "a", "k"])
    if kind == "a":
        while True:
            p = r.randint(-6, 0)
            q = r.randint(1, 6)
            if abs(p) != abs(q):
                break
        M = r.randint(1, 30)
        m2 = max(p * p, q * q)
        a = Fr(M, m2)
        stem = f"関数 $y=ax^2$ で，$x$ の変域が ${p}\\leqq x\\leqq {q}$ のとき，$y$ の変域は $0\\leqq y\\leqq {M}$ である。$a$ の値を求めなさい。"
        far = p if p * p > q * q else q
        steps = [f"$y$ の最小値が $0$，最大値が正なので $a>0$。", f"$x$ の変域で $|x|$ が最も大きいのは $x={far}$。そのとき $y$ は最大値 ${M}$。", f"$a\\times{par(far)}^2={M}$ より $a={ftex(a)}$。"]
        return MARK(stem, a, " ".join(steps), f"Rational({M},{m2})", d=3, p=4,
                    ap="グラフをかき、$y$ の最大値をとる $x$ の値（$0$ から最も遠い端）を見つけて代入する。",
                    steps=steps, alt=[f"求めた $a$ で ${Y(a)}$ の $x={p}$、$x={q}$ の値を計算し、変域が $0\\leqq y\\leqq {M}$ になることを確かめる。"],
                    pc=[("最大値をとる $x$ を正しく判断している", 2), ("$a$ を正しく求めている", 2)],
                    pit=["$0$ に近い方の端を代入する。", "$x$ の変域の右端を必ず最大と思いこむ。"])
    a = r.choice([Fr(1), Fr(2), Fr(1, 2), Fr(3), Fr(1, 3), Fr(1, 4)])
    p = r.randint(-6, -1)
    k = r.randint(abs(p) + 1, abs(p) + 6)
    M = a * k * k
    assert M.denominator == 1
    stem = f"関数 ${Y(a)}$ で，$x$ の変域が ${p}\\leqq x\\leqq k$ のとき，$y$ の変域は $0\\leqq y\\leqq {M}$ である。$k$ の値を求めなさい。"
    steps = [f"$x={p}$ のとき $y={ftex(a * p * p)}$ で，${M}$ より小さい。", f"したがって最大値 ${M}$ は $x=k$（$k>0$）のときにとる。", f"${ftex(a)}k^2={M}$，$k^2={k * k}$，$k>0$ より $k={k}$。"]
    return MARK(stem, k, " ".join(steps), f"sqrt(({M})/({fpy(a)}))", d=3, p=4,
                ap="左端 $x=" + str(p) + "$ での $y$ の値と最大値を比べ、最大値をとるのがどちらの端かを判断する。",
                steps=steps, alt=[f"$k={k}$ のとき、$x$ の変域 ${p}\\leqq x\\leqq{k}$ で $y$ の変域が $0\\leqq y\\leqq {M}$ になることをグラフで確かめる。"],
                pc=[("最大値をとる端を正しく判断している", 2), ("$k$ を正しく求めている", 2)],
                pit=["$k^2=" + str(k * k) + "$ から $k=\\pm" + str(k) + "$ のまま答える。", "左端で最大になると考える。"])


@gen("standard_practice", 4, ["computation", "cross_unit"], rel=["JH-MATH-G2-U03"])
def b_rate_equal(r):
    while True:
        p = r.randint(-4, 4)
        q = p + r.randint(1, 5)
        if p + q > 0:
            break
    m = r.choice([1, 2, 3, 4, 6, 8, Fr(1, 2), Fr(3, 2)])
    b = nz(r, -6, 6)
    a = Fr(m) / (p + q)
    stem = f"関数 $y=ax^2$ で，$x$ の値が ${p}$ から ${q}$ まで増加するときの変化の割合は，一次関数 $y={rhs(m, b)}$ の変化の割合に等しい。$a$ の値を求めなさい。"
    steps = [f"一次関数 $y={rhs(m, b)}$ の変化の割合は傾きの ${ftex(m)}$。", f"$y=ax^2$ の変化の割合は $\\dfrac{{a\\times{q}^2-a\\times{par(p)}^2}}{{{q}-{par(p)}}}=a({p}+{q})={p + q}a$。", f"${p + q}a={ftex(m)}$ より $a={ftex(a)}$。"]
    return MARK(stem, a, " ".join(steps), f"({fpy(m)})/({p}+{q})", d=3, p=4,
                ap="一次関数の変化の割合は一定で傾きに等しい（一次関数の単元）。$y=ax^2$ の変化の割合を $a$ の式で表して方程式をつくる。",
                steps=steps, alt=[f"求めた $a$ で $x={p}$、${q}$ の $y$ の値を計算し、変化の割合が ${ftex(m)}$ になるかを確かめる。"],
                pc=[("$y=ax^2$ の変化の割合を $a$ の式で表している", 2), ("方程式を解いて $a$ を求めている", 2)],
                pit=["一次関数の切片も変化の割合にふくめる。", "$y=ax^2$ の変化の割合を $a$ とする。"])


def _ab_params(r, need_int=True):
    while True:
        a = r.choice(A_POS + [Fr(-1), Fr(-1, 2), Fr(-2)])
        p = r.randint(-5, -1)
        q = r.randint(1, 5)
        if p + q == 0:
            continue
        ya, yb = a * p * p, a * q * q
        if need_int and (ya.denominator != 1 or yb.denominator != 1):
            continue
        return a, p, q, ya, yb


@gen("standard_practice", 4, ["computation"])
def b_line_ab(r):
    a, p, q, ya, yb = _ab_params(r)
    m, n = a * (p + q), -a * p * q
    cands = [(L(m, -n), "切片の符号を誤っている。$y=mx+b$ に点を代入した後の移項に注意する。", "移項の符号の誤り"),
             (L(-m, n), "傾きを求めるとき、ひく順番がそろっていない。", "符号の誤り"),
             (L(a * (q - p), n), "傾きを $a(q-p)$ としている。放物線上の2点を結ぶ直線の傾きは $a(p+q)$。", "公式の覚え違い"),
             (L(m, ya), "点 A の $y$ 座標をそのまま切片にしている。", "切片の意味の誤解"),
             (L(Fr(yb - ya), n), "$x$ の増加量でわっていない。", "傾きの求め方の誤り")]
    return MC(f"右の図のように，関数 ${Y(a)}$ のグラフ上に2点 A，B があり，点 A の $x$ 座標は ${p}$，点 B の $x$ 座標は ${q}$ である。2点 A，B を通る直線の式として正しいものを，" + SEL4,
              L(m, n), cands, f"A ${pt(p, ya)}$，B ${pt(q, yb)}$。傾き $=\\dfrac{{{ftex(yb)}-{par(ya)}}}{{{q}-{par(p)}}}={ftex(m)}$。$y={rhs(m, 0)}+b$ に A を代入して $b={ftex(n)}$。", d=3, p=4,
              fig=ab_fig(a, p, q),
              ap="まず A、B の $y$ 座標を求め、2点を通る直線の式を一次関数と同じ方法で求める。傾きは $a(p+q)$ で検算できる。",
              steps=[f"A ${pt(p, ya)}$，B ${pt(q, yb)}$。", f"傾き $\\dfrac{{{ftex(yb - ya)}}}{{{q - p}}}={ftex(m)}$。", f"$y={rhs(m, 0)}+b$ に A を代入して $b={ftex(n)}$。", f"直線 AB：$y={rhs(m, n)}$。"],
              alt=[f"傾きは $a(p+q)={ftex(a)}\\times({p}+{q})={ftex(m)}$、切片は $-apq={ftex(n)}$ でも求められる（式の検算に使う）。"],
              pc=[("A、B の座標を正しく求めている", 2), ("直線の式を正しく求めている", 2)],
              pit=["負の $x$ 座標を代入したときの2乗の符号の誤り。", "切片の移項の符号の誤り。"],
              chk=(f"({fpy(yb)}-({fpy(ya)}))/({q}-({p}))", fpy(m), None, "intermediate"))


@gen("standard_practice", 4, ["computation", "application"])
def b_triangle(r):
    while True:
        a, p, q, ya, yb = _ab_params(r)
        if a > 0:
            break
    n = -a * p * q
    S = n * (q - p) / 2
    return MARK(f"右の図のように，関数 ${Y(a)}$ のグラフ上に2点 A，B があり，点 A の $x$ 座標は ${p}$，点 B の $x$ 座標は ${q}$ である。原点を O とするとき，$\\triangle\\mathrm{{OAB}}$ の面積を求めなさい。ただし，座標の1目もりを $1$ cm とする。",
                S, f"直線 AB は $y={rhs(a * (p + q), n)}$。$y$ 軸との交点 C $(0,\\,{ftex(n)})$。$\\triangle\\mathrm{{OAB}}=\\dfrac{{1}}{{2}}\\times{ftex(n)}\\times{abs(p)}+\\dfrac{{1}}{{2}}\\times{ftex(n)}\\times{q}={ftex(S)}$ cm²。",
                f"Rational(1,2)*({fpy(n)})*({q}-({p}))", d=3, p=4, fig=ab_fig(a, p, q),
                ap="直線 AB と $y$ 軸の交点 C を求め、$\\triangle\\mathrm{OAB}$ を $y$ 軸で $\\triangle\\mathrm{OAC}$ と $\\triangle\\mathrm{OBC}$ に分ける。底辺 OC、高さは A、B の $x$ 座標の絶対値。",
                steps=[f"A ${pt(p, ya)}$，B ${pt(q, yb)}$。", f"直線 AB：$y={rhs(a * (p + q), n)}$，C $(0,\\,{ftex(n)})$。", f"$\\triangle\\mathrm{{OAC}}=\\dfrac{{1}}{{2}}\\times{ftex(n)}\\times{abs(p)}$，$\\triangle\\mathrm{{OBC}}=\\dfrac{{1}}{{2}}\\times{ftex(n)}\\times{q}$。", f"合計 ${ftex(S)}$ cm²。"],
                alt=["A、B から $x$ 軸に垂線をひいて台形をつくり、台形の面積から2つの直角三角形の面積をひいても求められる。"],
                pc=[("直線 AB の切片を求めている", 2), ("面積を正しく求めている", 2)],
                pit=["高さに負の $x$ 座標をそのまま使う。", "底辺を AB の長さにして高さが求められなくなる。"])


@gen("standard_practice", 4, ["application", "computation"])
def b_rolling(r):
    a = r.choice([Fr(1), Fr(2), Fr(3), Fr(1, 2), Fr(3, 2), Fr(5, 2)])
    t0 = r.choice([2, 3, 4])
    d0 = a * t0 * t0
    assert d0.denominator == 1
    kind = r.choice(["dist", "time", "speed"])
    intro_ = (f"なめらかな斜面でボールを静かに転がしたところ，転がり始めてから $x$ 秒間に転がる距離を $y$ m とすると，$y$ は $x$ の2乗に比例し，"
              f"転がり始めてから ${t0}$ 秒間に ${ftex(d0)}$ m 転がった（架空の実験）。")
    if kind == "dist":
        t = r.choice([v for v in range(1, 9) if v != t0])
        ans = a * t * t
        stem = intro_ + f"転がり始めてから ${t}$ 秒間に転がる距離は何 m か求めなさい。"
        steps = [f"$y=ax^2$ に $x={t0}$，$y={ftex(d0)}$ を代入して $a={ftex(a)}$。", f"${Y(a)}$ に $x={t}$ を代入。", f"$y={ftex(ans)}$ m。"]
        expr = f"{fpy(a)}*{t}**2"
    elif kind == "time":
        t = r.choice([v for v in range(1, 11) if v != t0])
        D = a * t * t
        if D.denominator != 1:
            t = 2 * t
            D = a * t * t
        ans = Fr(t)
        stem = intro_ + f"転がった距離が ${ftex(D)}$ m になるのは，転がり始めてから何秒後か求めなさい。"
        steps = [f"$a={ftex(a)}$，${Y(a)}$。", f"${ftex(D)}={ftex(a)}x^2$，$x^2={t * t}$。", f"$x>0$ より $x={t}$ 秒後。"]
        expr = f"sqrt(({fpy(D)})/({fpy(a)}))"
    else:
        t1 = r.randint(0, 4)
        t2 = t1 + r.randint(1, 4)
        ans = a * (t1 + t2)
        stem = intro_ + f"転がり始めて ${t1}$ 秒後から ${t2}$ 秒後までの間の平均の速さは毎秒何 m か求めなさい。"
        steps = [f"$a={ftex(a)}$。", f"${t1}$ 秒後までに ${ftex(a * t1 * t1)}$ m，${t2}$ 秒後までに ${ftex(a * t2 * t2)}$ m 転がる。", f"平均の速さ $=\\dfrac{{{ftex(a * t2 * t2)}-{ftex(a * t1 * t1)}}}{{{t2}-{t1}}}={ftex(ans)}$ m/s（変化の割合）。"]
        expr = f"({fpy(a)}*{t2}**2-{fpy(a)}*{t1}**2)/({t2}-{t1})"
    return MARK(stem, ans, " ".join(steps), expr, d=3, p=4,
                ap="与えられた1組の値から比例定数 $a$ を求めて式をつくる。平均の速さは「進んだ距離 ÷ かかった時間」で、変化の割合にあたる。",
                steps=steps, alt=["$x$ が $n$ 倍になると $y$ は $n^2$ 倍になることを使って、比例定数を求めずに考えることもできる。"],
                pc=[("比例定数を求めて式をつくっている", 2), ("問われている量を正しく求めている", 2)],
                pit=["平均の速さを $y$ の値÷時間で求める（区間の距離を使わない）。", "$x^2=k$ の負の解を答えにふくめる。"])


# ======================================================================
# C 思考力・記述応用
# ======================================================================

def _statements(r):
    a = r.choice([Fr(1), Fr(2), Fr(1, 2), Fr(3)])
    p = r.randint(1, 4)
    q = p + r.randint(1, 3)
    m = r.randint(-3, 3)
    T, F = _graph_statements(r)
    out = [(t, True, w) for t, w in T] + [(t, False, w) for t, w in F]
    out += [
        (f"関数 ${Y(a)}$ で，$x$ の変域が $-{p}\\leqq x\\leqq{q}$ のとき，$y$ の最小値は $0$ である。", True, "$x$ の変域に $0$ をふくむので、$x=0$ で最小値 $0$ をとる。"),
        (f"関数 ${Y(a)}$ で，$x$ の変域が $-{p}\\leqq x\\leqq{q}$ のとき，$y$ の最小値は ${ftex(a * p * p)}$ である。", False, "$x=0$ が変域にふくまれるので、最小値は $0$。"),
        (f"関数 ${Y(a)}$ で，$x$ の値が ${p}$ から ${q}$ まで増加するときの変化の割合は ${ftex(a * (p + q))}$ である。", True, f"$a(p+q)={ftex(a)}\\times{p + q}={ftex(a * (p + q))}$。"),
        (f"関数 ${Y(a)}$ と一次関数 $y={ftex(2 * a * (p + q))}x{'+' if m >= 0 else ''}{m}$ の，$x$ が ${p}$ から ${q}$ まで増加するときの変化の割合は等しい。", False,
         f"$y={axx(a)}$ の変化の割合は ${ftex(a * (p + q))}$、一次関数の変化の割合は ${ftex(2 * a * (p + q))}$ で等しくない。"),
    ]
    return out


@gen("thinking_writing", 3, ["written_reasoning", "condition_check", "concept"])
def c_xy_judge(r):
    S = _statements(r)
    tx, ty = r.choice([True, False]), r.choice([True, False])
    x = r.choice([s for s in S if s[1] == tx])
    y = r.choice([s for s in S if s[1] == ty and s is not x and s[0][:22] != x[0][:22]])
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
        why[c] = (" ".join(rs), "関数 $y=ax^2$ の性質の思いこみ")
    return mc("Kさんは，関数 $y=ax^2$ について次の X，Y のようにまとめた。X，Y の文の正誤の組み合わせとして最も適するものを，" + SEL4 + f"\nX　{x[0]}\nY　{y[0]}",
              [ans] + [c for c in XY if c != ans], f"X：{x[2]}　Y：{y[2]}", d=4, p=8, why=why,
              ap="それぞれの文を、グラフの性質・変域・変化の割合の求め方に照らして確かめる。簡単なグラフや表をかいて判断するとよい。",
              steps=[f"X：{x[2]}", f"Y：{y[2]}", f"よって {ans}。"],
              alt=["具体的な値を代入して表をつくり、文の内容が成り立つかを確かめる。"],
              pc=[("X の正誤を根拠をもって判断している", 4), ("Y の正誤を根拠をもって判断している", 4)],
              pit=["変域の両端だけで最小値を決める。", "$y=ax^2$ の変化の割合を一定だと考える。"])


@gen("thinking_writing", 3, ["cross_unit", "application"], rel=["JH-MATH-G2-U05", "JH-MATH-G2-U03"])
def c_equal_area(r):
    while True:
        a, p, q, ya, yb = _ab_params(r)
        if a > 0 and p + q > 0:
            break
    m = a * (p + q)
    xP = p + q
    yP = a * xP * xP
    ask_y = r.random() < 0.4
    ans = yP if ask_y else Fr(xP)
    stem = (f"右の図のように，関数 ${Y(a)}$ のグラフ上に2点 A，B があり，点 A の $x$ 座標は ${p}$，点 B の $x$ 座標は ${q}$ である。"
            f"関数 ${Y(a)}$ のグラフ上に，原点 O と異なる点 P を，直線 AB に対して O と同じ側にとる。$\\triangle\\mathrm{{PAB}}$ の面積が $\\triangle\\mathrm{{OAB}}$ の面積と等しくなるとき，"
            f"点 P の {'$y$ 座標' if ask_y else '$x$ 座標'}を求めなさい。")
    steps = [f"A ${pt(p, ya)}$，B ${pt(q, yb)}$ より，直線 AB の傾きは ${ftex(m)}$。",
             f"△PAB＝△OAB となるのは，AB を共通の底辺とみて高さが等しいとき。つまり P は O を通り AB に平行な直線 $y={rhs(m, 0)}$ 上にある（等積変形）。",
             f"${axx(a)}={rhs(m, 0)}$ を解くと $x=0,\\ x={xP}$。O と異なるので $x={xP}$。",
             f"P ${pt(xP, yP)}$。"]
    return MARK(stem, ans, " ".join(steps), f"{fpy(m)}/({fpy(a)})" if not ask_y else f"{fpy(a)}*({fpy(m)}/({fpy(a)}))**2", d=4, p=8,
                fig=ab_fig(a, p, q),
                ap="底辺 AB が共通なので、高さが等しければ面積は等しい。O を通り AB に平行な直線をひき、放物線との交点を求める（平行線と面積の単元の等積変形）。",
                steps=steps, alt=[f"P の $x$ 座標を $t$ とおき、直線 AB と $y$ 軸の交点を使って △PAB の面積を $t$ の式で表し、△OAB の面積と等しいとおいて方程式を解いてもよい。"],
                pc=[("平行線を使う方針を立てている", 3), ("平行な直線の式を求めている", 3), ("正しい座標を求めている", 2)],
                pit=["P を直線 AB の反対側にもとってしまう。", "平行な直線の傾きを $a$ にしてしまう。"])


@gen("thinking_writing", 2, ["cross_unit", "application"], rel=["JH-MATH-G2-U03", "JH-MATH-G3-U03"])
def c_catch_up(r):
    while True:
        a = r.choice([Fr(1, 2), Fr(1), Fr(3, 2), Fr(2), Fr(1, 4)])
        v = r.randint(1, 6)
        T = r.randint(2, 12)
        d = a * T * T - v * T
        if d > 0 and d.denominator == 1 and d <= 60:
            break
    stem = (f"ボールが斜面を転がり始めてから $x$ 秒間に転がる距離を $y$ m とすると，${Y(a)}$ の関係がある（架空の実験）。"
            f"ボールが転がり始めると同時に，ボールの ${ftex(d)}$ m 前方にいた Kさんが，ボールと同じ向きに秒速 ${v}$ m で歩き始めた。"
            "ボールが Kさんに追いつくのは，ボールが転がり始めてから何秒後か求めなさい。ただし，斜面は十分に長いものとする。")
    other = Fr(v) / a - T
    steps = [f"ボールのスタート地点を基準にすると，$x$ 秒後のボールの位置は ${axx(a)}$ m，Kさんの位置は $({v}x+{ftex(d)})$ m。",
             f"追いつくのは ${axx(a)}={v}x+{ftex(d)}$ のとき。",
             f"整理して解くと $x={T},\\ x={ftex(other)}$。",
             f"$x>0$ より ${T}$ 秒後。"]
    return MARK(stem, T, " ".join(steps), f"(({v})+sqrt(({v})**2+4*({fpy(a)})*({fpy(d)})))/(2*({fpy(a)}))", d=4, p=8,
                ap="ボールと Kさんの位置を同じ基準点から $x$ の式で表す（ボールは $y=ax^2$、Kさんは一次関数）。位置が等しくなる $x$ を二次方程式で求める。",
                steps=steps, alt=["2つのグラフ（放物線と直線）をかき、交点の $x$ 座標を読みとって確かめる（一次関数のグラフの単元とのつながり）。"],
                pc=[("2つの位置を $x$ の式で表している", 3), ("二次方程式をつくって解いている", 3), ("条件に合う解を選んでいる", 2)],
                pit=["Kさんの出発位置（前方の距離）を式に入れ忘れる。", "負の解を答えにふくめる。"])


@gen("thinking_writing", 2, ["application", "multiple_solutions"])
def c_two_parab(r):
    kind = r.choice(["gap", "square"])
    if kind == "gap":
        a = r.choice([Fr(2), Fr(3), Fr(1), Fr(3, 2)])
        b = r.choice([v for v in (Fr(1, 2), Fr(1, 3), Fr(1, 4), Fr(-1), Fr(-1, 2)) if v < a])
        t = r.randint(1, 6)
        Lg = (a - b) * t * t
        assert Lg.denominator == 1
        stem = (f"2つの関数 ${Y(a)}$，${Y(b)}$ のグラフがある。$x$ 座標が正の数 $t$ である点を，${Y(a)}$ のグラフ上に A，${Y(b)}$ のグラフ上に B とする。"
                f"線分 AB の長さが ${ftex(Lg)}$ になるとき，$t$ の値を求めなさい。ただし，座標の1目もりを $1$ cm とし，線分 AB の長さの単位は cm とする。")
        steps = [f"A $(t,\\,{ftex(a)}t^2)$，B $(t,\\,{ftex(b)}t^2)$。", f"AB $={ftex(a)}t^2-{par(b)}t^2={ftex(a - b)}t^2$。", f"${ftex(a - b)}t^2={ftex(Lg)}$，$t^2={t * t}$，$t>0$ より $t={t}$。"]
        ans = Fr(t)
        expr = f"sqrt(({fpy(Lg)})/({fpy(a - b)}))"
        fig = figure(f"2つの放物線 {Y(a)}、{Y(b)} と、x 座標が等しい2点 A、B",
                     parab_svg([(a, ""), (b, "")], pts=[(t, a * t * t, "A"), (t, b * t * t, "B")], segs=[((t, a * t * t), (t, b * t * t))],
                               xr=(-t - 1.5, t + 1.5), yr=(float(min(b * t * t, 0)) * 1.3 - 0.5, float(a * t * t) * 1.15 + 0.5)))
    else:
        a = r.choice([Fr(1, 2), Fr(1, 3), Fr(1, 4), Fr(2, 3), Fr(1), Fr(2), Fr(3, 2)])
        t = 2 / a
        ans = t
        stem = (f"関数 ${Y(a)}$ のグラフ上に，$x$ 座標が正の点 A と，A と $y$ 軸について対称な点 B をとる。A，B から $x$ 軸に垂線をひき，$x$ 軸との交点をそれぞれ D，C とする。"
                "四角形 ABCD が正方形になるとき，点 A の $x$ 座標を求めなさい。")
        steps = [f"A の $x$ 座標を $t$（$t>0$）とすると，A $(t,\\,{ftex(a)}t^2)$，B $(-t,\\,{ftex(a)}t^2)$。", f"AB $=2t$，AD $={ftex(a)}t^2$。",
                 f"正方形なので $2t={ftex(a)}t^2$，$t({ftex(a)}t-2)=0$。", f"$t>0$ より $t={ftex(t)}$。"]
        expr = f"2/({fpy(a)})"
        ya = float(a * t * t)
        fig = figure(f"放物線 {Y(a)} 上の2点 A、B と x 軸上の C、D でできる四角形",
                     parab_svg([(a, "")], pts=[(t, a * t * t, "A"), (-t, a * t * t, "B"), (-t, 0, "C"), (t, 0, "D")],
                               segs=[((t, a * t * t), (-t, a * t * t)), ((-t, a * t * t), (-t, 0)), ((t, a * t * t), (t, 0))],
                               xr=(-float(t) * 1.6, float(t) * 1.6), yr=(-ya * 0.15, ya * 1.5)))
    return MARK(stem, ans, " ".join(steps), expr, d=4, p=8, fig=fig,
                ap="点の座標を文字 $t$ で表し、長さを $t$ の式にする。条件から方程式をつくり、$t>0$ をみたす解を選ぶ。",
                steps=steps, alt=["求めた $t$ の値で点の座標を計算し、長さの条件が成り立つかを確かめる。"],
                pc=[("点の座標を $t$ で表している", 3), ("長さの条件から方程式をつくっている", 3), ("$t>0$ をみたす解を答えている", 2)],
                pit=["線分の長さを $y$ 座標の和にしてしまう（差をとる）。", "$t=0$ や負の解を答えにふくめる。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def _err_mc(stem, sol, right, cands, e, err, **kw):
    return MC(f"{stem}\n〔Kさんの解答〕\n{sol}\nKさんの解答の誤りを説明したものとして最も適するものを，" + SEL4, right, cands, e, err=err, **kw)


@gen("error_correction", 4, ["common_error", "condition_check"])
def d_domain_err(r):
    a = r.choice([Fr(v) for v in (1, 2, 3, -1, -2, -3)] + [Fr(1, 2), Fr(-1, 2)])
    while True:
        p = r.randint(-5, -1)
        q = r.randint(1, 5)
        if abs(p) != abs(q) and (a * p * p).denominator == 1 and (a * q * q).denominator == 1:
            break
    yp, yq = a * p * p, a * q * q
    lo, hi = (Fr(0), max(yp, yq)) if a > 0 else (min(yp, yq), Fr(0))
    sol = f"$x={p}$ のとき $y={ftex(yp)}$，$x={q}$ のとき $y={ftex(yq)}$\n答え　{_ineq(min(yp, yq), max(yp, yq))}"
    right = f"$x$ の変域に $x=0$ がふくまれるので，$y$ の{'最小値' if a > 0 else '最大値'}は $0$ になることを見落としている。"
    cands = [(f"$x={p}$ のときの $y$ の値の計算を誤っている。", f"$y={ftex(yp)}$ は正しく計算されている。", "誤りの箇所の見落とし"),
             ("$y$ の変域の大小の順番を逆にしている。", "Kさんは小さい方から順に正しく並べている。", "誤りの箇所の見落とし"),
             ("Kさんの解答に誤りはない。", "グラフをかくと、$x=0$ のとき $y=0$ となり、Kさんの変域からはみ出す。", "検算不足")]
    fix = _ineq(lo, hi)
    return _err_mc(f"〔問題〕関数 ${Y(a)}$ について，$x$ の変域が ${p}\\leqq x\\leqq {q}$ のときの $y$ の変域を求めなさい。", sol, right, cands, f"正しくは {fix}。",
                   dict(sol=sol, step="$y$ の最小値（最大値）の判断", type="condition", tempt="一次関数のときと同じように、$x$ の変域の両端の値だけで $y$ の変域が決まると思いこむ。", fix=fix),
                   d=3, p=6,
                   ap="グラフをかいて、$x$ の変域の部分をなぞる。一次関数とちがい、放物線は $x=0$ で向きが変わる。",
                   steps=[f"$x$ の変域 ${p}\\leqq x\\leqq {q}$ は $0$ をふくむ。", f"$x=0$ のとき $y=0$ が{'最小値' if a > 0 else '最大値'}。", f"{fix}。"],
                   alt=["$x=" + str(p) + "$ から $" + str(q) + "$ までの整数で表をつくり、$y$ の値の最小・最大を確かめる。"],
                   pc=[("誤りの原因を正しく指摘している", 3), ("正しい変域を求めている", 3)],
                   pit=["両端の値だけで判断する。"],
                   chk=(f"Min({fpy(yp)},{fpy(yq)},0)", fpy(lo), None, "intermediate"))


@gen("error_correction", 3, ["common_error", "written_reasoning"])
def d_rate_line(r):
    a = r.choice([Fr(v) for v in (1, 2, 3, -1, -2, -3)] + [Fr(1, 2), Fr(-1, 2)])
    while True:
        p = r.randint(-5, -1)
        q = r.randint(1, 5)
        if p + q != 0 and (a * p * p).denominator == 1 and (a * q * q).denominator == 1:
            break
    yp, yq = a * p * p, a * q * q
    where = r.randint(0, 3)
    ypw, yqw = yp, yq
    l1 = f"$x={p}$ のとき $y={ftex(a)}\\times{par(p)}^2={ftex(yp)}$"
    if where == 0:
        ypw = -yp
        l1 = f"$x={p}$ のとき $y={ftex(a)}\\times{par(p)}^2={ftex(ypw)}$"
    l2 = f"$x={q}$ のとき $y={ftex(yq)}$"
    dy = yqw - ypw
    l3 = f"$y$ の増加量は ${ftex(yqw)}-{par(ypw)}={ftex(dy)}$"
    if where == 1:
        dy = ypw - yqw
        l3 = f"$y$ の増加量は ${ftex(ypw)}-{par(yqw)}={ftex(dy)}$"
    l4 = f"変化の割合は $\\dfrac{{{ftex(dy)}}}{{{q}-{par(p)}}}={ftex(Fr(dy) / (q - p))}$"
    if where == 2:
        l4 = f"変化の割合は $\\dfrac{{{ftex(dy)}}}{{{q}-{par(p)}}}=\\dfrac{{{ftex(dy)}}}{{{q + p}}}={ftex(Fr(dy) / (q + p))}$"
    if where == 3:
        l4 = f"変化の割合は $\\dfrac{{{ftex(dy)}}}{{{q}-{par(p)}}}={ftex(Fr(dy) / (q - p) + (1 if a > 0 else -1))}$"
    ans = a * (p + q)
    # 3行目以外の誤りでは 2 行目までは正しい
    lines = [l1, l2, l3, l4]
    idx = {0: 0, 1: 2, 2: 3, 3: 3}[where]
    if where == 3:
        assert Fr(dy) / (q - p) + (1 if a > 0 else -1) != ans
    sol = "\n".join(f"{i + 1}行目　{t}" for i, t in enumerate(lines))
    LINES4 = ["1行目", "2行目", "3行目", "4行目"]
    ok = {0: f"1行目は、$x={p}$ のときの $y$ の値を正しく計算している。", 1: f"2行目は、$x={q}$ のときの $y$ の値を正しく計算している。",
          2: "3行目は、$y$ の増加量を（後の値）−（前の値）で正しく計算している。", 3: "4行目は、増加量の比を正しく計算している。"}
    why = {LINES4[i]: (ok[i], "誤りの箇所の見落とし") for i in range(4) if i != idx}
    info = {0: ("1行目（負の数の2乗の符号）", "sign", "負の数の2乗を負の数としてしまう。"),
            1: ("3行目（ひく順番）", "sign", "$y$ の増加量を（前の値）−（後の値）で計算してしまう。"),
            2: ("4行目（$x$ の増加量）", "calculation", "$x$ の増加量を求めるとき、負の数をひく計算を誤る。"),
            3: ("4行目（わり算の計算）", "calculation", "分数のわり算で計算ミスをする。")}[where]
    fix = f"$\\dfrac{{{ftex(yq)}-{par(yp)}}}{{{q}-{par(p)}}}={ftex(ans)}$"
    return mc(f"〔問題〕関数 ${Y(a)}$ について，$x$ の値が ${p}$ から ${q}$ まで増加するときの変化の割合を求めなさい。\n〔Kさんの解答〕\n{sol}\nKさんの解答で，誤りが最初に生じた行として最も適するものを，" + SEL4,
              LINES4, f"誤りが最初に生じたのは{LINES4[idx]}。正しくは {fix}。", d=3, p=6, keep=True, ai=idx, why=why,
              err=dict(sol=sol, step=info[0], type=info[1], tempt=info[2], fix=fix),
              ap="1行ずつ計算し直して比べる。最後に公式 $a(p+q)$ で答えを検算すると、誤りがあるかどうかがすぐ分かる。",
              steps=[f"$x={p}$ のとき $y={ftex(yp)}$，$x={q}$ のとき $y={ftex(yq)}$。", f"$y$ の増加量 ${ftex(yq - yp)}$，$x$ の増加量 ${q - p}$。", f"変化の割合 ${ftex(ans)}$。"],
              alt=[f"公式 $a(p+q)={ftex(a)}\\times({p}+{q})={ftex(ans)}$ で検算する。"],
              pc=[("誤りの行を正しく指摘している", 3), ("正しい変化の割合を求めている", 3)],
              pit=["負の数の2乗の符号の誤り。", "ひく順番をそろえない。"],
              chk=(f"({fpy(yq)}-({fpy(yp)}))/({q}-({p}))", fpy(ans), None, "intermediate"))


A_EXPL = {
    "lin": "$y=ax^2$ の比例定数を $\\dfrac{y}{x}$ で求めている。正しくは $\\dfrac{y}{x^2}$。",
    "sq": "負の数の2乗を負の数として計算している。",
    "inv": "$a=\\dfrac{x^2}{y}$ と、分子と分母を逆にしている。",
    "two": "$x^2$ を $2x$ として計算している。",
}


@gen("error_correction", 3, ["common_error", "condition_check"])
def d_find_a_err(r):
    kind = r.choice(list(A_EXPL))
    for _ in range(200):
        a = r.choice(A_ALL)
        p = nz(r, -6, 6, (0, 1, -1, 2))
        if kind == "sq" and p > 0:
            p = -p
        q = a * p * p
        if q.denominator != 1:
            continue
        aw = {"lin": Fr(q) / p, "sq": -a, "inv": Fr(p * p) / q, "two": Fr(q) / (2 * p)}[kind]
        if aw != a:
            break
    else:
        raise AssertionError("no params")
    if kind == "lin":
        line = f"${ftex(q)}=a\\times{par(p)}$ より $a={ftex(aw)}$"
    elif kind == "sq":
        line = f"${ftex(q)}=a\\times{par(p)}^2=-{p * p}a$ より $a={ftex(aw)}$"
    elif kind == "inv":
        line = f"$a=\\dfrac{{{par(p)}^2}}{{{ftex(q)}}}={ftex(aw)}$"
    else:
        line = f"${ftex(q)}=a\\times{par(p)}^2=a\\times{2 * p}$ より $a={ftex(aw)}$"
    sol = f"{line}\n答え　${Y(aw)}$"
    others = [k for k in A_EXPL if k != kind]
    r.shuffle(others)
    cands = [(A_EXPL[k], "Kさんの解答では、このような計算はしていない。", "誤りの箇所の見落とし") for k in others[:2]]
    cands.append(("Kさんの解答に誤りはない。", f"Kさんの式に $x={p}$ を代入すると $y={ftex(aw * p * p)}$ となり、${ftex(q)}$ にならない。", "検算不足"))
    fix = f"${ftex(q)}=a\\times{par(p)}^2={p * p}a$ より $a={ftex(a)}$，${Y(a)}$"
    info = {"lin": ("比例定数の求め方", "concept", "比例 $y=ax$ の求め方と混同しやすい。"),
            "sq": ("負の数の2乗", "sign", f"${par(p)}^2$ のかっこを意識せず $-{p * p}$ としてしまう。"),
            "inv": ("比例定数の式（分子と分母）", "formula", "$a$ を求める式の分子と分母を取り違える。"),
            "two": ("累乗の計算", "calculation", "$x^2$ を「$x$ の2倍」と取り違える。")}[kind]
    return _err_mc(f"〔問題〕$y$ は $x$ の2乗に比例し，$x={p}$ のとき $y={ftex(q)}$ である。$y$ を $x$ の式で表しなさい。", sol, A_EXPL[kind], cands, f"正しくは {fix}。",
                   dict(sol=sol, step=info[0], type=info[1], tempt=info[2], fix=fix), d=3, p=6,
                   ap="Kさんの答えの式に $x=" + str(p) + "$ を代入して、$y=" + ftex(q) + "$ になるかを確かめる。ならなければ、どこで誤ったかをさがす。",
                   steps=[f"Kさんの誤り：{A_EXPL[kind]}", f"正しくは {fix}。"],
                   alt=[f"$x={p}$ のとき $y={ftex(q)}$ なので、$a=\\dfrac{{y}}{{x^2}}=\\dfrac{{{ftex(q)}}}{{{p * p}}}$ と直接求めてもよい。"],
                   pc=[("誤りの原因を正しく指摘している", 3), ("正しい式を求めている", 3)],
                   pit=["比例の式と混同する。", "負の数の2乗を負にする。"],
                   chk=(f"Rational({q.numerator},{p * p})", fpy(a), None, "intermediate"))


GENERATORS = [a_find_a, a_value, a_rate, a_graph_props, a_domain,
              b_domain_a, b_rate_equal, b_line_ab, b_triangle, b_rolling,
              c_xy_judge, c_equal_area, c_catch_up, c_two_parab,
              d_domain_err, d_rate_line, d_find_a_err]


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


GENERATORS = [_robust(g) for g in GENERATORS]
