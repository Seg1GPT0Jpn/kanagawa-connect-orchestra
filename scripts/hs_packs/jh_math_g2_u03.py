"""単元パック：中学2年 一次関数（神奈川県公立高校入試形式）。"""
import re
import unicodedata
from fractions import Fraction as Fr

from banks._common import figure, mc, num, plane
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem, tp)

UNIT_ID = "JH-MATH-G2-U03"

PREREQUISITES = [
    ("JH-MATH-G1-U04", "比例 $y=ax$ の式とグラフ、座標の読み書きができること。一次関数は比例に定数 $b$ を加えた関数である。"),
    ("JH-MATH-G2-U01", "等式の変形ができること。$2x+3y=6$ を $y=\\cdots$ の形に直してグラフをかくときに使う。"),
    ("JH-MATH-G2-U02", "連立方程式を解けること。2直線の交点の座標を求めるときに使う。"),
]
EXTENSIONS = [
    ("JH-MATH-G3-U04", "関数 $y=ax^2$ では変化の割合が一定でなくなる。一次関数との違いを比べ、放物線と直線の交点の問題へ進む。"),
    ("HS-MATH2-U03", "高校の図形と方程式で、直線の方程式・2直線の平行と垂直・点と直線の距離を学ぶ。"),
    ("HS-MATH1-U03", "高校の二次関数で、関数・定義域・値域の考え方をさらに深める。"),
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


def fpy(v):
    v = Fr(v)
    return str(v.numerator) if v.denominator == 1 else f"Rational({v.numerator},{v.denominator})"


def par(v):
    """負の数はかっこをつけて表す（代入の式用）。"""
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


def rhs(m, b):
    """mx+b の LaTeX（係数 0・±1・分数を整形）。"""
    m, b = Fr(m), Fr(b)
    if m == 0:
        return ftex(b)
    s = "x" if m == 1 else "-x" if m == -1 else f"{ftex(m)}x"
    if b > 0:
        s += "+" + ftex(b)
    elif b < 0:
        s += ftex(b)
    return s


def lin(m, b):
    return f"y={rhs(m, b)}"


def L(m, b):
    return f"${lin(m, b)}$"


def stdeq(p, q, c):
    """px+qy=c の LaTeX。"""
    def term(k, v, first):
        if k == 0:
            return ""
        mag = "" if abs(k) == 1 else str(abs(k))
        sign = "-" if k < 0 else ("" if first else "+")
        return f"{sign}{mag}{v}"
    return f"{term(p, 'x', True)}{term(q, 'y', p == 0)}={c}"


def pt(x, y):
    return f"$({ftex(x)},\\,{ftex(y)})$"


SEL4 = "次の1〜4の中から1つ選び，その番号を答えなさい。"


def clip_line(m, b, xr, yr):
    """直線 y=mx+b のうち、枠 xr×yr の中にある部分の両端（plane の lines は clipPath の id が
    冊子内の他の図と重なるため使わず、線分として自前で切り取る）。"""
    m, b = float(m), float(b)
    cand = []
    for x in xr:
        y = m * x + b
        if yr[0] - 1e-9 <= y <= yr[1] + 1e-9:
            cand.append((x, y))
    if m:
        for y in yr:
            x = (y - b) / m
            if xr[0] - 1e-9 <= x <= xr[1] + 1e-9:
                cand.append((x, y))
    cand = sorted(set((round(x, 6), round(y, 6)) for x, y in cand))
    return (cand[0], cand[-1])


def line_label(m, b, xr, yr, text):
    (x1, y1), (x2, y2) = clip_line(m, b, xr, yr)
    return (x2 - 0.2 * (x2 - x1) + 0.25, y2 - 0.2 * (y2 - y1) + 0.35, text)


def line_fig(m, b, extra_pts=()):
    """直線 y=mx+b を方眼つきの座標平面にかく（格子点を通る2点に印をつける）。"""
    m, b = Fr(m), Fr(b)
    q = m.denominator
    pts = [(0, b, "")]
    for x in (q, -q, 2 * q, -2 * q):
        y = m * x + b
        if -5 <= x <= 5 and -5 <= y <= 5:
            pts.append((x, y, ""))
            break
    pts += list(extra_pts)
    return figure(f"直線 {lin(m, b)} のグラフ", plane(xr=(-5, 5), yr=(-5, 5), unit=15,
                                                  segments=[clip_line(m, b, (-5, 5), (-5, 5))], points=[(float(x), float(y), t) for x, y, t in pts]))


# ----------------------------------------------------------------------
# 授業プリント
# ----------------------------------------------------------------------

LESSON = lesson(
    goals=["一次関数 $y=ax+b$ の意味を理解し、変化の割合が一定で $a$ に等しいことを説明できる。",
           "一次関数のグラフを傾きと切片からかき、グラフや条件から直線の式を求められる。",
           "二元一次方程式のグラフと連立方程式の解の関係を理解し、身のまわりの事象を一次関数を使って考察できる。"],
    duration=100,
    readiness=["比例 $y=ax$ の式とグラフ（原点を通る直線）を理解している。",
               "座標平面で点の座標を読んだり、点をとったりできる。",
               "等式の変形と連立方程式の解き方（加減法・代入法）が使える。"],
    flow=[("導入：水そうの水の量", 10, "水を入れ続けるときの時間と水の量の表から、比例との違いを考える"),
          ("一次関数の定義と変化の割合", 20, "$y=ax+b$ の定義、変化の割合が一定で $a$ に等しいことを導く"),
          ("グラフの傾きと切片", 20, "$y=ax$ のグラフを $b$ だけ平行移動したものとしてとらえ、傾き・切片でグラフをかく（例題1）"),
          ("直線の式の求め方", 20, "傾きと1点、2点から式を求める（例題2）"),
          ("方程式とグラフ", 15, "$ax+by=c$ のグラフ、連立方程式の解と交点（例題3）"),
          ("一次関数の利用とまとめ", 15, "道のりと時間のグラフを読み取る。確認問題")],
    sections=[
        intro("in1", "比例に「はじめの量」が加わると",
              "水そうにはじめから $4$ L の水が入っていて、そこへ毎分 $3$ L ずつ水を入れる。$x$ 分後の水の量を $y$ L とすると、$y=3x+4$ と表せる。水の量 $y$ は時間 $x$ に比例してはいないが、「比例する部分 $3x$」と「はじめの量 $4$」の和になっている。このように表される関数を一次関数という。",
              bullets=["$x$ が $1$ 増えるごとに $y$ は $3$ ずつ増える（増え方が一定）。", "$x=0$ のときの $y$ の値 $4$ が「はじめの量」にあたる。"],
              points=[tp("時間と水の量の表を板書し、$x$ が1増えるごとの $y$ の増え方を矢印で書きこませる。", ask="$y$ は $x$ に比例しているか。", expect="比例していない。$x$ が2倍になっても $y$ は2倍にならない。でも増え方は一定。", timing="導入の最初"),
                      tp("比例 $y=ax$ は $b=0$ の場合の一次関数であることを、ここで確認しておく。", caution="「比例は一次関数ではない」と考える生徒がいる。")]),
        definition("df1", "一次関数と変化の割合",
                   "$y$ が $x$ の関数で、$y$ が $x$ の一次式 $y=ax+b$（$a$、$b$ は定数、$a\\neq0$）で表されるとき、$y$ は $x$ の一次関数であるという。また、$x$ の増加量に対する $y$ の増加量の割合を変化の割合という。",
                   formula="$$\\text{変化の割合}=\\dfrac{y\\text{ の増加量}}{x\\text{ の増加量}}$$",
                   conditions=["一次関数 $y=ax+b$ の変化の割合は一定で、$a$ に等しい。", "$y$ の増加量 $=a\\times$（$x$ の増加量）。", "比例 $y=ax$ は、一次関数で $b=0$ の場合である。反比例 $y=\\dfrac{a}{x}$ は一次関数ではない。"],
                   points=[tp("「増加量」は（後の値）−（前の値）であり、減るときは負の数になることを確認する。", ask="$y=-2x+5$ で $x$ が $1$ から $4$ まで増加するとき、$y$ の増加量はいくつか。", expect="$-6$。$y$ は $3$ から $-3$ に変わる。")]),
        derivation("dv1", "一次関数の変化の割合が $a$ になることを導く",
                   ["一次関数 $y=ax+b$ で、$x$ の値が $p$ から $q$ まで増加するとする（$p\\neq q$）。",
                    "$x=p$ のとき $y=ap+b$、$x=q$ のとき $y=aq+b$。",
                    "$x$ の増加量は $q-p$、$y$ の増加量は $(aq+b)-(ap+b)=a(q-p)$。",
                    "変化の割合 $=\\dfrac{a(q-p)}{q-p}=a$。$p$、$q$ にどんな値を選んでも $a$ になるので、変化の割合は一定である。",
                    "したがって、グラフ上のどの2点を選んでも「右へ $1$ 進むと上へ $a$ 進む」。これがグラフの傾き $a$ の意味である。"],
                   points=[tp("文字 $p$、$q$ を使って説明することで「どの区間でも同じ」ことが示せる、という文字式による説明のよさを強調する（式の計算の単元とのつながり）。", caution="$b$ が引き算で消えることを、式を縦にそろえて書かせると理解しやすい。")]),
        theorem("th1", "一次関数のグラフ",
                "$$y=ax+b\\ \\text{のグラフは、傾き } a\\text{、切片 } b \\text{ の直線}$$",
                ["$y=ax$ のグラフを、$y$ 軸の正の方向に $b$ だけ平行移動した直線である。", "切片 $b$：グラフと $y$ 軸との交点 $(0,\\,b)$ の $y$ 座標。",
                 "$a>0$ のとき右上がり（$x$ が増加すると $y$ も増加）、$a<0$ のとき右下がり（$x$ が増加すると $y$ は減少）。", "傾きが等しい2直線は平行である。"],
                body="グラフをかくときは、切片 $(0,\\,b)$ をとり、そこから「右へ $1$（分母の数）進み、上へ $a$（分子の数）進む」点をとって2点を結ぶ。",
                points=[tp("$y=2x$ と $y=2x+3$ の表を並べ、同じ $x$ に対して $y$ がいつも $3$ 大きいことから平行移動を説明する。", ask="2つのグラフはどんな位置関係になるか。", expect="平行。$y=2x+3$ は $y=2x$ を上に $3$ ずらしたもの。")]),
        definition("df2", "方程式とグラフ",
                   "二元一次方程式 $ax+by=c$ の解 $(x,\\,y)$ を座標とする点の集まりは直線になる。これを方程式のグラフという。",
                   conditions=["$b\\neq0$ のとき、$y=-\\dfrac{a}{b}x+\\dfrac{c}{b}$ と変形でき、一次関数のグラフと同じ直線になる。",
                               "$y=k$ のグラフは $x$ 軸に平行な直線、$x=h$ のグラフは $y$ 軸に平行な直線。",
                               "連立方程式の解は、2つの方程式のグラフの交点の座標である。平行な2直線（交点なし）のとき、連立方程式は解をもたない。"],
                   points=[tp("$2x+3y=6$ では、$x=0$ と $y=0$ を代入して軸との交点 $(0,\\,2)$、$(3,\\,0)$ を求めるとグラフがすぐかけることを示す。")]),
        example("ex1", "例題1　グラフから式を読む",
                "右の図の直線の式を求めなさい。",
                ["$y$ 軸との交点が $(0,\\,1)$ なので、切片は $1$。", "点 $(0,\\,1)$ から右へ $2$ 進むと下へ $3$ 進んで点 $(2,\\,-2)$ を通るので、傾きは $-\\dfrac{3}{2}$。", "式は $y=-\\dfrac{3}{2}x+1$。"],
                "$y=-\\dfrac{3}{2}x+1$",
                thinking="切片は $y$ 軸との交点、傾きは「右へ進んだ量」に対する「上へ進んだ量」。格子点をはっきり通る2点を探す。",
                figure=line_fig(Fr(-3, 2), 1),
                points=[tp("下へ進むときは傾きが負になることを、矢印をかかせて確認する。")],
                misconceptions=[("傾きを $-\\dfrac{2}{3}$ とする", "（上下に進んだ量）÷（右へ進んだ量）なので $-\\dfrac{3}{2}$")]),
        example("ex2", "例題2　2点を通る直線の式",
                "2点 $(1,\\,-1)$、$(3,\\,5)$ を通る直線の式を求めなさい。",
                ["傾き $=\\dfrac{5-(-1)}{3-1}=\\dfrac{6}{2}=3$。", "$y=3x+b$ に $x=1$、$y=-1$ を代入すると $-1=3+b$、$b=-4$。", "式は $y=3x-4$。", "確かめ：$x=3$ のとき $y=9-4=5$ で、もう1つの点も通る。"],
                "$y=3x-4$",
                thinking="まず傾き（変化の割合）を求め、次にどちらか1点を代入して切片を求める。",
                points=[tp("連立方程式 $\\begin{cases}-1=a+b\\\\5=3a+b\\end{cases}$ を解く方法でも同じ式になることを示し、2通りの方法を比べさせる。", ask="どちらの方法が速いか。", expect="傾きを先に出す方が計算が少ない。")]),
        example("ex3", "例題3　2直線の交点",
                "2直線 $y=2x-1$、$x+y=5$ の交点の座標を求めなさい。",
                ["交点の座標は、連立方程式 $\\begin{cases}y=2x-1\\\\x+y=5\\end{cases}$ の解である。", "代入法：$x+(2x-1)=5$、$3x=6$、$x=2$。", "$y=2\\times2-1=3$。", "交点は $(2,\\,3)$。"],
                "$(2,\\,3)$",
                thinking="グラフの交点は、両方の直線上にある点。つまり両方の式を同時にみたす $(x,\\,y)$ である。",
                points=[tp("方眼にグラフをかかせ、計算で求めた交点と一致することを確かめさせる。", timing="例題3のあと")]),
        example("ex4", "例題4　一次関数の利用",
                "長さ $20$ cm の線香に火をつけると、毎分 $0.5$ cm ずつ短くなる。火をつけてから $x$ 分後の線香の長さを $y$ cm として、$y$ を $x$ の式で表し、線香が燃えつきるのは何分後か求めなさい。",
                ["$1$ 分で $0.5$ cm 短くなるので、$x$ 分では $0.5x$ cm 短くなる。", "$y=20-0.5x$、つまり $y=-0.5x+20$。", "燃えつきるのは $y=0$ のとき。$0=-0.5x+20$ より $x=40$。", "変域は $0\\leqq x\\leqq40$。"],
                "$y=-0.5x+20$、$40$ 分後",
                thinking="「はじめの量」が切片、「1分あたりの変化」が変化の割合（傾き）になる。",
                points=[tp("変域を考えることの大切さ（$x>40$ では式が意味をもたない）に触れる。")]),
        board("bd1", "板書案",
              [("① 一次関数", ["$y=ax+b$（$a\\neq0$）", "変化の割合 $=\\dfrac{y\\text{ の増加量}}{x\\text{ の増加量}}=a$（一定）", "比例は $b=0$ の場合", "$y$ の増加量 $=a\\times x$ の増加量"]),
               ("② グラフと式", ["傾き $a$、切片 $b$ の直線", "$a>0$ 右上がり、$a<0$ 右下がり", "傾きが等しい → 平行", "2点 → 傾き → 1点代入で $b$"]),
               ("③ 方程式とグラフ", ["$ax+by=c$ → $y=\\cdots$ に変形", "$y=k$：$x$ 軸に平行", "$x=h$：$y$ 軸に平行", "交点 ＝ 連立方程式の解"])],
              points=[tp("②では、例題1のグラフの横に「右へ $2$、下へ $3$」の階段をかいて傾きを示す。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("変化の割合と「$y$ の増加量」を混同する生徒が多い。増加量は割合×$x$ の増加量であることを、毎回式で確認させる。", caution="$x$ の増加量が $1$ でない問題で誤りやすい。"),
               tp("2点から傾きを求めるとき、分子と分母で引く順番をそろえることを徹底する。", ask="$\\dfrac{5-(-1)}{1-3}$ と計算するとどうなるか。", expect="$-3$ になってしまう。順番がそろっていないから。"),
               tp("$a<0$ の一次関数で $y$ の変域を求めるとき、$x$ の小さい方の端が $y$ の大きい方の端になることを、グラフをかいて確かめさせる。", timing="変域の問題の前"),
               tp("$ax+by=c$ のグラフをかくときは、$y=\\cdots$ に変形してから傾き・切片を読むか、軸との交点を求めるかを選ばせる。")],
              misconceptions=[("傾き $=\\dfrac{x\\text{ の増加量}}{y\\text{ の増加量}}$ とする", "傾き $=\\dfrac{y\\text{ の増加量}}{x\\text{ の増加量}}$"),
                              ("比例は一次関数ではない", "比例 $y=ax$ は $b=0$ の一次関数"),
                              ("$2x+3y=6$ の傾きは $2$", "$y=-\\dfrac{2}{3}x+2$ と変形して傾きは $-\\dfrac{2}{3}$")]),
        summary("sm1", "まとめ",
                ["一次関数 $y=ax+b$ の変化の割合は一定で $a$。", "グラフは傾き $a$、切片 $b$ の直線。傾きが等しい直線は平行。",
                 "直線の式は「傾き」と「通る1点」から求める。", "2直線の交点の座標は連立方程式の解。", "身のまわりの事象では「はじめの量」が切片、「一定の割合の変化」が傾きになる。"]),
        check("ck1", "確認問題",
              [("一次関数 $y=-4x+3$ で、$x$ の増加量が $3$ のときの $y$ の増加量を求めなさい。", "$-12$"),
               ("傾きが $2$ で、点 $(3,\\,1)$ を通る直線の式を求めなさい。", "$y=2x-5$"),
               ("方程式 $3x-y=2$ のグラフの傾きと切片を答えなさい。", "$y=3x-2$ と変形して、傾き $3$、切片 $-2$")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

SLOPES = [Fr(k) for k in (-5, -4, -3, -2, 2, 3, 4, 5)] + [Fr(p, q) for p, q in ((1, 2), (-1, 2), (2, 3), (-2, 3), (3, 4), (-3, 4), (1, 3), (-1, 3), (3, 2), (-3, 2))]


@gen("basic_check", 5, ["computation", "concept"])
def a_rate(r):
    kind = r.choice(["inc", "two"])
    if kind == "inc":
        m = r.choice(SLOPES)
        b = r.choice([v for v in range(-9, 10) if v])
        d = r.choice([k for k in range(2, 13) if (m * k).denominator == 1])
        ans = m * d
        cands = [(f"${ftex(-ans)}$", "符号が逆になっている。$a$ が負なら $y$ は減少し、増加量は負の数になる。" if m < 0 else "増加量の符号を逆にしている。$a>0$ なので $y$ は増加する。", "増加量の符号の誤り"),
                 (f"${ftex(m)}$", "変化の割合（$x$ の増加量が $1$ のときの $y$ の増加量）をそのまま答えている。", "変化の割合と増加量の混同"),
                 (f"${ftex(ans + b)}$", "切片 $b$ まで加えている。$b$ は増加量の計算では引き算で消える。", "切片の扱いの誤り"),
                 (f"${ftex(Fr(d) / m)}$", "$x$ の増加量を変化の割合でわっている。", "割合の向きの誤り"),
                 (f"${ftex(m * d * 2)}$", "増加量を2倍している。", "計算の誤り")]
        return MC(f"一次関数 ${lin(m, b)}$ で，$x$ の増加量が ${d}$ のときの $y$ の増加量として正しいものを，" + SEL4, f"${ftex(ans)}$", cands,
                  f"$y$ の増加量 $=a\\times$（$x$ の増加量）$={par(m)}\\times{d}={ftex(ans)}$。", d=1,
                  ap="一次関数 $y=ax+b$ の変化の割合は一定で $a$。$y$ の増加量 $=a\\times$（$x$ の増加量）。",
                  steps=[f"変化の割合は $a={ftex(m)}$。", f"$y$ の増加量 $={par(m)}\\times{d}={ftex(ans)}$。"],
                  alt=[f"たとえば $x=0$ と $x={d}$ の $y$ の値 ${ftex(b)}$、${ftex(m * d + b)}$ を求めて差をとっても ${ftex(ans)}$ になる。"],
                  pc=[("変化の割合が $a$ であることを使っている", 1), ("増加量を正しく計算している", 1)],
                  pit=["変化の割合そのものを答えてしまう。", "$a<0$ のとき符号を落とす。"],
                  chk=(f"({fpy(m)})*{d}", fpy(ans), None, "intermediate"))
    m = r.choice(SLOPES)
    p = r.randint(-4, 3)
    q = p + r.choice([k for k in range(1, 7) if (m * k).denominator == 1])
    b = r.choice([v for v in range(-6, 7) if v])
    s, t = m * p + b, m * q + b
    cands = [(f"${ftex(t - s)}$", "$y$ の増加量を答えている。$x$ の増加量でわる必要がある。", "変化の割合と増加量の混同"),
             (f"${ftex(Fr(q - p) / (t - s))}$", "$\\dfrac{x\\text{ の増加量}}{y\\text{ の増加量}}$ と、分子と分母を逆にしている。", "割合の向きの誤り"),
             (f"${ftex(-m)}$", "引く順番が分子と分母でそろっておらず、符号が逆になっている。", "増加量の符号の誤り"),
             (f"${ftex(Fr(t + s, q + p) if q + p else t + s)}$", "増加量ではなく値の和を使っている。", "増加量の意味の誤解")]
    return MC(f"$y$ は $x$ の一次関数で，$x={p}$ のとき $y={ftex(s)}$，$x={q}$ のとき $y={ftex(t)}$ である。この一次関数の変化の割合として正しいものを，" + SEL4,
              f"${ftex(m)}$", cands,
              f"変化の割合 $=\\dfrac{{{ftex(t)}-{par(s)}}}{{{q}-{par(p)}}}=\\dfrac{{{ftex(t - s)}}}{{{q - p}}}={ftex(m)}$。", d=2,
              ap="変化の割合 $=\\dfrac{y\\text{ の増加量}}{x\\text{ の増加量}}$。分子・分母で引く順番をそろえる。",
              steps=[f"$x$ の増加量：${q}-{par(p)}={q - p}$。", f"$y$ の増加量：${ftex(t)}-{par(s)}={ftex(t - s)}$。", f"変化の割合：$\\dfrac{{{ftex(t - s)}}}{{{q - p}}}={ftex(m)}$。"],
              alt=[f"式を $y=ax+b$ とおき、連立方程式 ${ftex(s)}={par(p)}a+b$，${ftex(t)}={q}a+b$ を解いて $a={ftex(m)}$ を求めてもよい。"],
              pc=[("増加量を正しく求めている", 1), ("変化の割合を正しく求めている", 1)],
              pit=["$x$ の増加量と $y$ の増加量を逆にわる。", "負の数を引くときの符号の誤り。"],
              chk=(f"Rational({fpy(t - s)},1)/({q}-({p}))", fpy(m), None, "intermediate"))


@gen("basic_check", 5, ["concept", "condition_check"])
def a_std_form(r):
    p = r.randint(1, 6)
    q = r.choice([v for v in range(-6, 7) if v and abs(v) != p])
    c = r.choice([v for v in range(-12, 13) if v])
    m, k = Fr(-p, q), Fr(c, q)

    def ans(a, b):
        return f"傾き ${ftex(a)}$，切片 ${ftex(b)}$"
    cands = [(ans(-m, k), "$y=\\cdots$ に変形するとき、$px$ を移項した符号の変化を忘れている。", "移項の符号の誤り"),
             (ans(Fr(p, 1), c), "$x$ の係数と右辺の数をそのまま傾き・切片としている。$y=\\cdots$ の形に変形してから読む。", "式の形の確認不足"),
             (ans(m, c), "切片を求めるとき、右辺を $y$ の係数でわり忘れている。", "等式の変形の誤り"),
             (ans(Fr(q, -p), k), "傾きの分子と分母を逆にしている。", "傾きのとらえ違い"),
             (ans(-m, -k), "変形の符号をすべて逆にしている。", "等式の変形の誤り")]
    return MC(f"方程式 ${stdeq(p, q, c)}$ のグラフの傾きと切片の組み合わせとして正しいものを，" + SEL4, ans(m, k), cands,
              f"${stdeq(p, q, c)}$ を $y$ について解くと ${lin(m, k)}$。傾き ${ftex(m)}$，切片 ${ftex(k)}$。", d=2,
              ap="方程式を $y=ax+b$ の形に変形すると、傾き $a$ と切片 $b$ を読み取れる。",
              steps=[f"${'' if p == 1 else p}x$ を移項：${'' if abs(q) == 1 else abs(q)}y$ の式に直す。", f"両辺を ${q}$ でわる：${lin(m, k)}$。", f"傾き ${ftex(m)}$，切片 ${ftex(k)}$。"],
              alt=[f"$x=0$ を代入すると $y={ftex(k)}$（切片）。$y$ 軸との交点ともう1点を求めて傾きを計算しても確かめられる。"],
              pc=[("$y$ について解いている", 1), ("傾きと切片を正しく読み取っている", 1)],
              pit=["$x$ の係数をそのまま傾きと思いこむ。", "$y$ の係数が負のとき、わる計算で符号を誤る。"],
              chk=(f"Rational({-p},{q})", fpy(m), None, "intermediate"))


GRAPH_SLOPES = [Fr(1), Fr(2), Fr(3), Fr(-1), Fr(-2), Fr(-3), Fr(1, 2), Fr(-1, 2), Fr(2, 3), Fr(-2, 3), Fr(3, 2), Fr(-3, 2), Fr(1, 3), Fr(-1, 3)]


@gen("basic_check", 5, ["concept"])
def a_graph_read(r):
    m = r.choice(GRAPH_SLOPES)
    b = r.choice([v for v in range(-3, 4) if v])
    cands = [(L(-m, b), "傾きの符号が逆。右下がりの直線は傾きが負、右上がりは正である。", "傾きの符号の読み違い"),
             (L(1 / m, b), "傾きを（右へ進む量）÷（上下に進む量）と逆に読んでいる。", "傾きの向きの誤り"),
             (L(m, -b), "切片の符号を読み違えている。$y$ 軸との交点の $y$ 座標が切片。", "切片の読み違い"),
             (L(-1 / m, b), "傾きの分子と分母を逆にし、符号も誤っている。", "傾きのとらえ違い"),
             (L(m, b + (1 if b < 3 else -1)), "$y$ 軸との交点を1目もりずらして読んでいる。", "切片の読み違い")]
    q, p = m.denominator, m.numerator
    return MC("右の図の直線の式として正しいものを，" + SEL4, L(m, b), cands,
              f"切片は ${b}$。右へ ${q}$ 進むと{'上' if p > 0 else '下'}へ ${abs(p)}$ 進むので，傾きは ${ftex(m)}$。式は ${lin(m, b)}$。", d=2,
              fig=line_fig(m, b),
              ap="$y$ 軸との交点から切片を読み、格子点をはっきり通るもう1点を見つけて「右へ進む量」と「上下に進む量」から傾きを求める。",
              steps=[f"$y$ 軸との交点は $(0,\\,{b})$ なので切片は ${b}$。", f"$(0,\\,{b})$ から右へ ${q}$ 進むと{'上' if p > 0 else '下'}へ ${abs(p)}$ 進む。", f"傾き ${ftex(m)}$、式は ${lin(m, b)}$。"],
              alt=[f"グラフが通る2点 $(0,\\,{b})$、$({q},\\,{b + p})$ を式に代入して確かめる。"],
              pc=[("切片を正しく読み取っている", 1), ("傾きを正しく読み取っている", 1)],
              pit=["傾きを（横）÷（縦）と逆に読む。", "右下がりなのに傾きを正の数にする。"],
              chk=(f"Rational({p},{q})", fpy(m), None, "intermediate"))


def _lin_situations(r):
    a, b = r.randint(80, 200), r.randint(100, 900)
    Lg, c = r.randint(12, 25), r.choice([Fr(1, 2), Fr(1), Fr(3, 2), Fr(2)])
    T, w = r.randint(5, 40), r.randint(2, 9)
    P = r.choice([12, 16, 20, 24, 30, 36])
    v = r.choice([60, 70, 75, 80, 90])
    cdec = {Fr(1, 2): "0.5", Fr(1): "1", Fr(3, 2): "1.5", Fr(2): "2"}[c]
    return [
        (f"1冊 ${a}$ 円のノートを $x$ 冊と，${b}$ 円の筆箱を1つ買うときの代金を $y$ 円とする。", f"$y={a}x+{b}$"),
        (f"長さ ${Lg}$ cm の線香に火をつけると毎分 ${cdec}$ cm ずつ短くなる。火をつけてから $x$ 分後の線香の長さを $y$ cm とする。", f"$y={Lg}-{cdec}x$"),
        (f"${T}$ L の水が入った水そうに毎分 ${w}$ L の割合で水を入れる。入れ始めてから $x$ 分後の水の量を $y$ L とする。", f"$y={w}x+{T}$"),
        (f"周の長さが ${P}$ cm の長方形で，縦の長さを $x$ cm，横の長さを $y$ cm とする。", f"$y={P // 2}-x$"),
        (f"分速 ${v}$ m で $x$ 分間歩いたときの道のりを $y$ m とする。", f"$y={v}x$（比例は一次関数の特別な場合）"),
    ]


def _nonlin_situations(r):
    S = r.choice([12, 18, 24, 30, 36, 48])
    D = r.choice([6, 10, 12, 15, 20, 30])
    return [
        (f"面積が ${S}$ cm² の長方形で，縦の長さを $x$ cm，横の長さを $y$ cm とする。", f"$y=\\dfrac{{{S}}}{{x}}$（反比例）"),
        ("1辺が $x$ cm の正方形の面積を $y$ cm² とする。", "$y=x^2$"),
        (f"${D}$ km の道のりを時速 $x$ km で進むときにかかる時間を $y$ 時間とする。", f"$y=\\dfrac{{{D}}}{{x}}$（反比例）"),
        ("半径が $x$ cm の円の面積を $y$ cm² とする。", "$y=\\pi x^2$"),
        ("1辺が $x$ cm の立方体の体積を $y$ cm³ とする。", "$y=x^3$"),
    ]


@gen("basic_check", 5, ["condition_check", "concept"])
def a_is_linear(r):
    lin_s, non_s = _lin_situations(r), _nonlin_situations(r)
    want_linear = r.random() < 0.55
    if want_linear:
        right = r.choice(lin_s)
        wrongs = r.sample(non_s, 3)
        stem = "次の文のうち，$y$ が $x$ の一次関数であるものとして最も適するものを，" + SEL4
        why = [(t, f"式は {f} となり，$y$ は $x$ の一次式で表されないので一次関数ではない。", "一次関数の定義の誤解") for t, f in wrongs]
    else:
        right = r.choice(non_s)
        wrongs = r.sample(lin_s, 3)
        stem = "次の文のうち，$y$ が $x$ の一次関数でないものとして最も適するものを，" + SEL4
        why = [(t, f"式は {f} と $y=ax+b$ の形で表されるので一次関数である。", "一次関数の定義の誤解") for t, f in wrongs]
    return MC(stem, right[0], why, f"正答の文の式は {right[1]}。{'一次関数である' if want_linear else '一次関数ではない'}。", d=2,
              ap="それぞれ $y$ を $x$ の式で表し、$y=ax+b$（$a\\neq0$）の形になるかを調べる。比例 $y=ax$ も一次関数にふくまれる。",
              steps=["それぞれの文について、$y$ を $x$ の式で表す。", f"正答の文：{right[1]}。", "$y=ax+b$ の形かどうかで判断する。"],
              alt=["$x$ を $1$ ずつ増やした表をつくり、$y$ の増え方が一定かどうかで判断することもできる。"],
              pc=[("$y$ を $x$ の式で表している", 1), ("一次関数かどうかを正しく判断している", 1)],
              pit=["比例は一次関数ではないと考える。", "反比例を一次関数と混同する。"])


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 4, ["computation"])
def b_two_points(r):
    m = r.choice(SLOPES)
    b = r.choice([v for v in range(-7, 8) if v])
    q = m.denominator
    xs = [x for x in range(-6, 7) if x % q == 0]
    x1, x2 = sorted(r.sample(xs, 2))
    if r.random() < 0.5:
        x1, x2 = x2, x1
    y1, y2 = m * x1 + b, m * x2 + b
    cands = [(L(-m, y1 + m * x1), "傾きを求めるとき、分子と分母で引く順番がそろっていない。", "増加量の符号の誤り"),
             (L(1 / m, y1 - x1 / m), "傾きを $\\dfrac{x\\text{ の増加量}}{y\\text{ の増加量}}$ と逆にしている。", "傾きの向きの誤り"),
             (L(m, y1 + m * x1), "切片を求める計算で移項の符号を誤っている。", "移項の符号の誤り"),
             (L(m, y1), "1点の $y$ 座標をそのまま切片にしている。切片は $x=0$ のときの $y$ の値。", "切片の意味の誤解"),
             (L(m, b + 1), "切片の計算を誤っている。", "計算の誤り")]
    return MC(f"2点 {pt(x1, y1)}，{pt(x2, y2)} を通る直線の式として正しいものを，" + SEL4, L(m, b), cands,
              f"傾き $=\\dfrac{{{ftex(y2)}-{par(y1)}}}{{{x2}-{par(x1)}}}={ftex(m)}$。${lin(m, 0)}+b$ に {pt(x1, y1)} を代入して $b={ftex(b)}$。式は ${lin(m, b)}$。",
              d=2, p=4,
              ap="2点を通る直線は、まず傾き（変化の割合）を求め、次に1点を代入して切片を求める。",
              steps=[f"傾き：$\\dfrac{{{ftex(y2 - y1)}}}{{{x2 - x1}}}={ftex(m)}$。", f"$y={rhs(m, 0)}+b$ に $x={x1}$，$y={ftex(y1)}$ を代入：${ftex(y1)}={ftex(m * x1)}+b$。", f"$b={ftex(b)}$，式は ${lin(m, b)}$。"],
              alt=[f"$y=ax+b$ に2点を代入した連立方程式を解いても求められる。最後にもう1点 {pt(x2, y2)} を代入して確かめる。"],
              pc=[("傾きを正しく求めている", 2), ("切片を正しく求めている", 2)],
              pit=["引く順番がそろわず傾きの符号を誤る。", "代入したあとの移項で符号を誤る。"],
              chk=(f"Rational({fpy(y2 - y1)},1)/({x2}-({x1}))", fpy(m), None, "intermediate"))


@gen("standard_practice", 4, ["computation", "condition_check"])
def b_slope_point(r):
    m = r.choice(SLOPES)
    q = m.denominator
    p = r.choice([x for x in range(-6, 7) if x % q == 0 and x])
    y0 = r.randint(-6, 6)
    b = y0 - m * p
    kind = r.choice(["par", "rate", "slope"])
    if kind == "par":
        c = r.choice([v for v in range(-8, 9) if v != b])
        cond = f"直線 ${lin(m, c)}$ に平行で，点 {pt(p, y0)} を通る直線"
        first = f"平行な直線は傾きが等しいので，傾きは ${ftex(m)}$。"
        extra = (L(m, c), "もとの直線の式をそのまま答えている。平行な直線は傾きは同じだが切片は異なる。", "平行の意味の誤解")
    elif kind == "rate":
        cond = f"$x$ の値が $1$ 増加すると $y$ の値が ${ftex(abs(m))}$ {'増加' if m > 0 else '減少'}し，$x={p}$ のとき $y={y0}$ となる一次関数"
        first = f"{'増加' if m > 0 else '減少'}なので変化の割合は ${ftex(m)}$。"
        extra = (L(abs(m), y0 - abs(m) * p), "「減少する」ことを傾きの符号に反映していない。", "増加・減少と符号の対応の誤り") if m < 0 else (L(m, y0), "$y$ の値をそのまま切片にしている。", "切片の意味の誤解")
    else:
        cond = f"傾きが ${ftex(m)}$ で，点 {pt(p, y0)} を通る直線"
        first = f"傾きは ${ftex(m)}$。"
        extra = (L(m, y0), "点の $y$ 座標をそのまま切片にしている。", "切片の意味の誤解")
    cands = [extra,
             (L(m, y0 + m * p), "切片を求めるときに移項の符号を誤っている。", "移項の符号の誤り"),
             (L(m, p - m * y0), "$x$ 座標と $y$ 座標を逆にして代入している。", "座標の読み違い"),
             (L(-m, y0 + m * p), "傾きの符号を逆にしている。", "傾きの符号の誤り"),
             (L(m, y0), "点の $y$ 座標をそのまま切片にしている。", "切片の意味の誤解")]
    return MC(f"{cond}の式として正しいものを，" + SEL4, L(m, b), cands,
              f"{first}$y={rhs(m, 0)}+b$ に $x={p}$，$y={y0}$ を代入して $b={ftex(b)}$。式は ${lin(m, b)}$。", d=3, p=4,
              ap="傾き（変化の割合）が分かれば、通る1点を $y=ax+b$ に代入して $b$ を求められる。",
              steps=[first, f"${y0}={ftex(m)}\\times{par(p)}+b$。", f"$b={ftex(b)}$，式は ${lin(m, b)}$。"],
              alt=[f"求めた式に $x={p}$ を代入して $y={y0}$ になるかを確かめる。"],
              pc=[("傾きを正しく決めている", 2), ("切片を正しく求めている", 2)],
              pit=["平行な直線の切片までもとの直線と同じにする。", "代入する $x$ と $y$ を取り違える。"],
              chk=(f"{y0}-({fpy(m)})*({p})", fpy(b), None, "intermediate"))


@gen("standard_practice", 4, ["computation", "cross_unit"], rel=["JH-MATH-G2-U02"])
def b_intersection(r):
    while True:
        x0, y0 = r.randint(-4, 6), r.randint(-4, 6)
        m1, m2 = r.sample([-3, -2, -1, 1, 2, 3], 2)
        if x0 and y0 and x0 != y0:
            break
    b1, b2 = y0 - m1 * x0, y0 - m2 * x0
    if r.random() < 0.5:
        # 2本目を px+qy=c の形で示す（y=m2x+b2 → -m2 x + y = b2）
        p_, q_ = (-m2, 1) if -m2 > 0 else (m2, -1)
        c_ = b2 if q_ == 1 else -b2
        eq2 = stdeq(p_, q_, c_)
    else:
        eq2 = lin(m2, b2)
    eq1 = lin(m1, b1)
    cands = [(pt(y0, x0), "$x$ 座標と $y$ 座標を逆にしている。", "座標の表し方の誤り"),
             (pt(-x0, y0), "$x$ を求める計算で符号を誤っている。", "移項の符号の誤り"),
             (pt(x0, -y0), "$y$ を求める計算で符号を誤っている。", "代入計算の誤り"),
             (pt(x0 + 1, m1 * (x0 + 1) + b1), "一方の直線上の点ではあるが、もう一方の直線上にはない。", "交点の意味の誤解")]
    return MC(f"2直線 ${eq1}$，${eq2}$ の交点の座標として正しいものを，" + SEL4, pt(x0, y0), cands,
              f"連立方程式を解くと $x={x0}$，$y={y0}$。交点は {pt(x0, y0)}。", d=3, p=4,
              ap="2直線の交点の座標は、2つの式を連立方程式として解いた解である（連立方程式の単元とのつながり）。",
              steps=[f"${eq1}$ を ${eq2}$ に代入して $x$ の方程式をつくる。", f"$x={x0}$。", f"$y={m1}\\times{par(x0)}{'+' if b1 >= 0 else ''}{b1}={y0}$。", f"交点 {pt(x0, y0)}。"],
              alt=["求めた座標を2つの式の両方に代入して、どちらも成り立つかを確かめる。"],
              pc=[("連立方程式をつくって解いている", 2), ("交点の座標を正しく答えている", 2)],
              pit=["一方の式だけに代入して確かめを終える。"],
              chk=(f"({b2}-({b1}))/(({m1})-({m2}))", str(x0), None, "intermediate"))


def _ineq(lo, hi, lo_s="\\leqq", hi_s="\\leqq"):
    return f"${ftex(lo)} {lo_s} y {hi_s} {ftex(hi)}$"


@gen("standard_practice", 4, ["condition_check", "computation"])
def b_domain(r):
    m = r.choice([-4, -3, -2, -1, 1, 2, 3, 4])
    b = r.randint(-6, 6)
    p = r.randint(-4, 2)
    q = p + r.randint(2, 5)
    fp, fq = m * p + b, m * q + b
    lo, hi = min(fp, fq), max(fp, fq)
    gp, gq = -m * p + b, -m * q + b
    cands = [(_ineq(p, q), "$x$ の変域をそのまま $y$ の変域にしている。", "変域の意味の誤解"),
             (_ineq(min(gp, gq), max(gp, gq)), "傾きの符号を逆にして計算している。", "代入計算の誤り"),
             (_ineq(min(m * p - b, m * q - b), max(m * p - b, m * q - b)), "切片の符号を逆にして計算している。", "代入計算の誤り"),
             (_ineq(min(b, fq), max(b, fq)), "$x=0$ のときの値を端にしている。端は $x$ の変域の両端で決まる。", "変域の端のとらえ違い"),
             (_ineq(lo, hi + 1), "端の値の計算を誤っている。", "計算の誤り")]
    return MC(f"一次関数 ${lin(m, b)}$ について，$x$ の変域が ${p}\\leqq x\\leqq {q}$ のとき，$y$ の変域として正しいものを，" + SEL4, _ineq(lo, hi), cands,
              f"$x={p}$ のとき $y={fp}$，$x={q}$ のとき $y={fq}$。{'傾きが負なので大小が入れかわり，' if m < 0 else ''}$y$ の変域は ${lo}\\leqq y\\leqq {hi}$。", d=3, p=4,
              ap="一次関数のグラフは直線なので、$y$ の変域は $x$ の変域の両端での $y$ の値で決まる。傾きが負のときは大小が入れかわる。",
              steps=[f"$x={p}$ のとき $y={m}\\times{par(p)}{'+' if b >= 0 else ''}{b}={fp}$。", f"$x={q}$ のとき $y={fq}$。", f"小さい方から並べて ${lo}\\leqq y\\leqq {hi}$。"],
              alt=["グラフをかき、$x$ の変域の部分だけをなぞって、$y$ 軸に投影した範囲を読み取る。"],
              pc=[("両端の $y$ の値を正しく求めている", 2), ("大小を正しく並べている", 2)],
              pit=["傾きが負のとき、$x$ の小さい方の値を $y$ の小さい方の端にしてしまう。"],
              chk=(f"{m}*({q})+({b})", str(fq), None, "intermediate"))


@gen("standard_practice", 4, ["application", "computation"])
def b_word(r):
    kind = r.choice(["drain", "fill", "spring", "candle", "price"])
    ask_x = r.random() < 0.5
    if kind == "drain":
        c = r.randint(2, 9)
        T = c * r.randint(8, 20)
        X = r.randint(2, T // c - 2)
        s = Fr(-c)
        intro_ = f"水が ${T}$ L 入った水そうから，毎分 ${c}$ L の割合で水を抜く。水を抜き始めてから $x$ 分後の水そうの水の量を $y$ L とする。"
        qy, qx = "水を抜き始めてから ${X}$ 分後の水の量は何 L か求めなさい。", "水の量が ${Y}$ L になるのは，水を抜き始めてから何分後か求めなさい。"
        conv = 1
    elif kind == "fill":
        c = r.randint(2, 9)
        T = r.randint(3, 30)
        X = r.randint(3, 15)
        s = Fr(c)
        intro_ = f"${T}$ L の水が入った水そうに，毎分 ${c}$ L の割合で水を入れる。水を入れ始めてから $x$ 分後の水そうの水の量を $y$ L とする。"
        qy, qx = "水を入れ始めてから ${X}$ 分後の水の量は何 L か求めなさい。", "水の量が ${Y}$ L になるのは，水を入れ始めてから何分後か求めなさい。"
        conv = 1
    elif kind == "spring":
        c = r.randint(1, 4)
        T = r.randint(8, 20)
        X = 10 * r.randint(2, 9)
        s = Fr(c, 10)
        intro_ = f"おもりをつるさないときの長さが ${T}$ cm のばねがあり，このばねは $10$ g のおもりをつるすごとに ${c}$ cm ずつのびる。$x$ g のおもりをつるしたときのばねの長さを $y$ cm とする。"
        qy, qx = "${X}$ g のおもりをつるしたときのばねの長さは何 cm か求めなさい。", "ばねの長さが ${Y}$ cm になるのは，何 g のおもりをつるしたときか求めなさい。"
        conv = 1
    elif kind == "candle":
        c = r.choice([1, 2, 3])
        T = c * r.randint(8, 15)
        X = r.randint(2, T // c - 2)
        s = Fr(-c)
        intro_ = f"長さ ${T}$ cm のろうそくに火をつけると，毎分 ${c}$ cm ずつ短くなる。火をつけてから $x$ 分後のろうそくの長さを $y$ cm とする。"
        qy, qx = "火をつけてから ${X}$ 分後のろうそくの長さは何 cm か求めなさい。", "ろうそくの長さが ${Y}$ cm になるのは，火をつけてから何分後か求めなさい。"
        conv = 1
    else:
        c = r.choice([20, 30, 40, 50])
        T = r.choice([300, 500, 800, 1000, 1200])
        X = r.randint(3, 15)
        s = Fr(c)
        intro_ = f"ある自転車の貸し出しは，基本料金が ${T}$ 円で，さらに $10$ 分借りるごとに ${c}$ 円かかる。借りる時間は $10$ 分単位とし，$10$ 分を $x$ 回分借りたときの料金を $y$ 円とする。"
        qy, qx = "${X10}$ 分借りたときの料金は何円か求めなさい。", "料金が ${Y}$ 円になるのは，何分借りたときか求めなさい。"
        conv = 10
    Y = s * X + T
    f = lin(s, T)
    common = dict(d=3, p=4, ap="「はじめの量」が切片、「一定の割合の変化」が傾き（変化の割合）になる。まず $y$ を $x$ の式で表す。",
                  pc=[("一次関数の式を正しくつくっている", 2), ("答えを正しく求めている", 2)])
    if ask_x:
        ans = X * conv
        steps = [f"式：${f}$。", f"$y={ftex(Y)}$ を代入：${ftex(Y)}={rhs(s, T)}$。", f"$x={X}$。"] + ([f"$x$ は「$10$ 分が何回分か」なので，${10 * X}$ 分。"] if conv == 10 else [])
        return MARK(intro_ + qx.replace("${Y}$", f"${ftex(Y)}$"), ans, f"${f}$ に $y={ftex(Y)}$ を代入して $x={X}$。" + (f"借りた時間は ${10 * X}$ 分。" if conv == 10 else ""),
                    f"{conv}*(({fpy(Y)})-({T}))/({fpy(s)})", steps=steps,
                    alt=[f"変化した量 ${ftex(abs(Y - T))}$ が、1単位あたりの変化 ${ftex(abs(s))}$ の何倍かを考えても求められる。"],
                    pit=["減っていく量なのに傾きを正の数にする。"] + (["$x$ の値を答えてしまい、分に直し忘れる。"] if conv == 10 else []), **common)
    return MARK(intro_ + qy.replace("${X}$", f"${X}$").replace("${X10}$", f"${10 * X}$"), Y,
                f"${f}$ に $x={X}$ を代入して $y={ftex(Y)}$。", f"({fpy(s)})*{X}+{T}",
                steps=[f"式：${f}$。", f"$x={X}$ を代入する。", f"$y={ftex(Y)}$。"],
                alt=["はじめの量に、変化した量（1単位あたりの変化 × 単位の数）を加える・引くと考えても求められる。"],
                pit=["減っていく量なのに変化の量を加えてしまう。"], **common)


# ======================================================================
# C 思考力・記述応用
# ======================================================================

@gen("thinking_writing", 4, ["application", "multiple_solutions", "computation"])
def c_triangle_area(r):
    while True:
        m1, m2 = r.sample([-3, -2, -1, 1, 2, 3, Fr(1, 2), Fr(-1, 2)], 2)
        x0 = r.choice([-4, -3, -2, 2, 3, 4])
        b1 = r.choice([v for v in range(-4, 6) if v])
        y0 = m1 * x0 + b1
        b2 = y0 - m2 * x0
        if y0.denominator != 1 or b2.denominator != 1 or not (-5 <= y0 <= 7) or not (-6 <= b2 <= 8) or b1 == b2 or b2 == 0:
            continue
        axis = r.choice(["y", "x"])
        if axis == "x":
            if y0 == 0:
                continue
            xi1, xi2 = Fr(-b1) / m1, Fr(-b2) / m2
            if xi1 == xi2 or max(abs(xi1), abs(xi2)) > 8:
                continue
            S = abs(xi1 - xi2) * abs(y0) / 2
        else:
            S = Fr(abs(b1 - b2) * abs(x0), 2)
        break
    pts = [(x0, y0, "P")]
    if axis == "y":
        pts += [(0, b1, "A"), (0, b2, "B")]
        how = f"底辺を $y$ 軸上の AB $=|{b1}-({b2})|={abs(b1 - b2)}$，高さを点 P と $y$ 軸との距離 ${abs(x0)}$ とみる"
        expr = f"Rational({abs(b1 - b2)}*{abs(x0)},2)"
        nm = "$y$ 軸"
    else:
        pts += [(xi1, 0, "A"), (xi2, 0, "B")]
        how = f"底辺を $x$ 軸上の AB $=|{ftex(xi1)}-{par(xi2)}|={ftex(abs(xi1 - xi2))}$，高さを点 P の $y$ 座標の絶対値 ${abs(int(y0))}$ とみる"
        expr = f"Abs(({fpy(xi1)})-({fpy(xi2)}))*{abs(int(y0))}/2"
        nm = "$x$ 軸"
    xs = [0] + [float(p[0]) for p in pts]
    ys = [0] + [float(p[1]) for p in pts]
    xr = (min(xs) - 2, max(xs) + 2)
    yr = (min(ys) - 2, max(ys) + 2)
    span = max(xr[1] - xr[0], yr[1] - yr[0])
    fig = figure("2直線と軸がつくる三角形", plane(xr=xr, yr=yr, unit=max(9, int(200 / span)), grid=False, ticks=False,
                                          segments=[clip_line(m1, b1, xr, yr), clip_line(m2, b2, xr, yr)],
                                          labels=[line_label(m1, b1, xr, yr, "ℓ"), line_label(m2, b2, xr, yr, "m")], points=[(float(a), float(b), c) for a, b, c in pts]))
    return MARK(f"右の図のように，2直線 ℓ：${lin(m1, b1)}$，m：${lin(m2, b2)}$ がある。2直線 ℓ，m の交点を P，ℓ，m と{nm}との交点をそれぞれ A，B とする。$\\triangle\\mathrm{{PAB}}$ の面積を求めなさい。ただし，座標の1目もりを $1$ cm とする。",
                S, f"P {pt(x0, y0)}。{how}と，面積は ${ftex(S)}$ cm²。", expr, d=4, p=8, fig=fig,
                ap="三角形の1辺が座標軸上にあるとき、その辺を底辺にすると、高さは残りの頂点と軸との距離（座標の絶対値）になる。",
                steps=[f"交点 P：連立方程式を解いて {pt(x0, y0)}。", f"A，B の座標を求める（{nm}との交点）。", how + "。", f"面積 $={ftex(S)}$。"],
                alt=["P を通り軸に平行な線で三角形を2つに分けて面積を求め、たし合わせても同じ結果になる。"],
                pc=[("交点 P の座標を求めている", 3), ("底辺と高さを正しくとらえている", 3), ("正しい面積", 2)],
                pit=["高さに負の座標をそのまま使う。", "底辺の長さを座標の差でなく和にする。"])


def travel_svg(D, v, t0, w):
    tA, tB = Fr(D, v), t0 + Fr(D, w)
    xmax = float(max(tA, tB)) * 1.08
    X = lambda t: 34 + float(t) / xmax * 210  # noqa: E731
    Y = lambda d: 150 - float(d) / D * 120  # noqa: E731
    s = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 270 175" width="270" height="175" font-family="serif" font-size="11">',
         '<defs><marker id="ta" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#000"/></marker></defs>',
         f'<line x1="34" y1="150" x2="258" y2="150" stroke="#000" marker-end="url(#ta)"/>',
         f'<line x1="34" y1="150" x2="34" y2="14" stroke="#000" marker-end="url(#ta)"/>',
         '<text x="250" y="166" font-style="italic">x</text><text x="246" y="166" font-size="9"></text><text x="38" y="16" font-style="italic">y</text>',
         '<text x="22" y="163">O</text><text x="228" y="166" font-size="9">（分）</text><text x="44" y="14" font-size="9">（m）</text>',
         f'<line x1="34" y1="{Y(D):.1f}" x2="{X(max(tA, tB)):.1f}" y2="{Y(D):.1f}" stroke="#888" stroke-dasharray="3 3"/>',
         f'<text x="2" y="{Y(D) + 4:.1f}" font-size="10">{D}</text>',
         f'<line x1="{X(t0):.1f}" y1="{Y(D):.1f}" x2="{X(t0):.1f}" y2="150" stroke="#888" stroke-dasharray="3 3"/>',
         f'<text x="{X(t0) - 4:.1f}" y="163" font-size="10">{t0}</text>',
         f'<line x1="{X(0):.1f}" y1="{Y(0):.1f}" x2="{X(tA):.1f}" y2="{Y(D):.1f}" stroke="#1f4e79" stroke-width="1.6"/>',
         f'<line x1="{X(t0):.1f}" y1="{Y(D):.1f}" x2="{X(tB):.1f}" y2="{Y(0):.1f}" stroke="#000" stroke-width="1.6" stroke-dasharray="6 3"/>',
         f'<text x="{X(tA * Fr(1, 3)) + 6:.1f}" y="{Y(D * Fr(1, 3)) - 2:.1f}" fill="#1f4e79" font-size="10">Aさん</text>',
         f'<text x="{X(t0 + (tB - t0) * Fr(3, 4)) + 4:.1f}" y="{Y(D * Fr(1, 4)) + 4:.1f}" font-size="10">Bさん</text>',
         "</svg>"]
    return "".join(s)


@gen("thinking_writing", 3, ["cross_unit", "application"], rel=["JH-MATH-G2-U02"])
def c_travel(r):
    while True:
        v = r.choice([50, 60, 70, 80])
        w = r.choice([v2 for v2 in (60, 75, 80, 90, 100, 120, 150) if v2 != v])
        t0 = r.randint(2, 8)
        x = r.randint(t0 + 3, 24)
        D = (v + w) * x - w * t0
        if 800 <= D <= 3000 and D % 10 == 0:
            break
    ask = r.choice(["time", "dist", "after"])
    if ask == "time":
        stem_q, ans, expr = "2人が出会うのは，Aさんが家を出発してから何分後か求めなさい。", x, f"({D}+{w}*{t0})/({v}+{w})"
    elif ask == "dist":
        stem_q, ans, expr = "2人が出会う地点は，家から何 m のところか求めなさい。", v * x, f"{v}*({D}+{w}*{t0})/({v}+{w})"
    else:
        stem_q, ans, expr = "2人が出会うのは，Bさんが図書館を出発してから何分後か求めなさい。", x - t0, f"({D}+{w}*{t0})/({v}+{w})-{t0}"
    stem = (f"Aさんの家と図書館は一本道で結ばれていて，その道のりは ${D}$ m である。Aさんは家を出発し，分速 ${v}$ m で図書館へ向かった。"
            f"Bさんは，Aさんが家を出発してから ${t0}$ 分後に図書館を出発し，分速 ${w}$ m で同じ道を家へ向かった。右の図は，Aさんが家を出発してから $x$ 分後の，"
            f"家から2人までの道のりを $y$ m として，2人の進むようすをグラフに表したものである。" + stem_q)
    return MARK(stem, ans, f"Aさん：$y={v}x$，Bさん：$y=-{w}x+{D + w * t0}$。連立して $x={x}$，$y={v * x}$。", expr, d=4, p=8,
                fig=figure("2人の進むようすを表すグラフ（実線がAさん，破線がBさん）", travel_svg(D, v, t0, w)),
                ap="2人のグラフをそれぞれ一次関数の式で表し、交点（出会う時刻と地点）を連立方程式で求める（連立方程式の単元とのつながり）。",
                steps=[f"Aさん：原点を通り傾き ${v}$ なので $y={v}x$。",
                       f"Bさん：点 $({t0},\\,{D})$ を通り傾き $-{w}$ なので $y=-{w}x+{D + w * t0}$。",
                       f"${v}x=-{w}x+{D + w * t0}$ を解いて $x={x}$，$y={v * x}$。",
                       f"求めるものは ${ans}$。"],
                alt=[f"Bさんが出発する時点で2人の間の道のりは ${D}-{v}\\times{t0}={D - v * t0}$ m。1分間に2人あわせて ${v + w}$ m ずつ近づくので，${D - v * t0}\\div{v + w}={x - t0}$ 分後に出会う。"],
                pc=[("2人のグラフの式を正しく表している", 3), ("連立方程式を解いて交点を求めている", 3), ("問われている量を正しく答えている", 2)],
                pit=["Bさんの式で、出発時刻のずれ（$x={t0}$ で $y={D}$）を考えない。", "時刻を求めたあと、問われている量（道のり・Bさんの経過時間）に直し忘れる。"])


def _statements(r):
    a = r.choice([2, 3, 4, 5])
    b = r.choice([1, 2, 3, 4, 5])
    p, q = r.choice([(2, 3), (3, 2), (1, 2), (3, 4), (2, 5)])
    k = r.randint(2, 6)
    return [
        (f"一次関数 $y=-{a}x+{b}$ では，$x$ の値が増加すると $y$ の値も増加する。", False, f"傾きが $-{a}$（負）なので、$x$ が増加すると $y$ は減少する。"),
        (f"一次関数 $y={a}x-{b}$ の変化の割合は，$x$ の値がどの範囲で変化しても ${a}$ である。", True, "一次関数の変化の割合は一定で、$x$ の係数に等しい。"),
        (f"2直線 $y={a}x+{b}$ と $y={a}x-{b}$ は1点で交わる。", False, "傾きが等しいので2直線は平行で、交わらない。"),
        (f"比例 $y={a}x$ は，一次関数 $y=ax+b$ で $b=0$ の場合である。", True, "比例は一次関数の特別な場合である。"),
        (f"方程式 ${p}x+{q}y={p * q * k}$ のグラフの傾きは $\\dfrac{{{p}}}{{{q}}}$ である。", False, f"$y=-\\dfrac{{{p}}}{{{q}}}x+{p * k}$ と変形できるので、傾きは $-\\dfrac{{{p}}}{{{q}}}$。"),
        (f"方程式 $y={k}$ のグラフは，点 $(0,\\,{k})$ を通り $x$ 軸に平行な直線である。", True, f"$x$ の値に関係なく $y={k}$ なので、$x$ 軸に平行な直線になる。"),
        (f"方程式 $x={k}$ のグラフは，$x$ 軸に平行な直線である。", False, f"$x={k}$ のグラフは点 $({k},\\,0)$ を通り $y$ 軸に平行な直線である。"),
        (f"反比例 $y=\\dfrac{{{a * k}}}{{x}}$ は一次関数である。", False, "$y$ が $x$ の一次式で表されないので、一次関数ではない。"),
        (f"連立方程式 $\\begin{{cases}}y={a}x+{b}\\\\y={a}x+{b + k}\\end{{cases}}$ は解をもたない。", True, "2つのグラフは傾きが等しく切片が異なる平行な直線で、交点がないので解はない。"),
        (f"一次関数 $y={a}x+{b}$ で，$x$ の増加量が ${k}$ のとき，$y$ の増加量は ${a * k + b}$ である。", False, f"$y$ の増加量は ${a}\\times{k}={a * k}$。切片は加えない。"),
        (f"一次関数 $y=-{a}x+{b}$ のグラフは，点 $(0,\\,{b})$ を通る右下がりの直線である。", True, f"切片 ${b}$、傾き $-{a}$（負）なので右下がり。"),
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
        why[c] = (" ".join(rs), "一次関数の性質の思いこみ")
    return mc("一次関数とそのグラフについて述べた次の X，Y の文の正誤の組み合わせとして最も適するものを，" + SEL4 + f"\nX　{x[0]}\nY　{y[0]}",
              [ans] + [c for c in XY if c != ans], f"X：{x[2]}　Y：{y[2]}", d=4, p=8, why=why,
              ap="それぞれの文を、式の形（傾き・切片）、変化の割合の定義、グラフの位置関係に照らして確かめる。具体的な数を代入して反例を探すのも有効。",
              steps=[f"X：{x[2]}", f"Y：{y[2]}", f"よって {ans}。"],
              alt=["方眼にグラフをかいたり、表をつくったりして、文の内容が成り立つかを確かめる。"],
              pc=[("X の正誤を根拠をもって判断している", 4), ("Y の正誤を根拠をもって判断している", 4)],
              pit=["式の形だけを見て、$y=\\cdots$ に変形せずに傾きを読む。", "変化の割合と $y$ の増加量を混同する。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def _err_mc(stem, sol, right, cands, e, err, **kw):
    return MC(f"{stem}\n〔Kさんの解答〕\n{sol}\nKさんの解答の誤りを説明したものとして最も適するものを，" + SEL4, right, cands, e, err=err, **kw)


@gen("error_correction", 4, ["common_error", "computation"])
def d_two_points(r):
    while True:
        m = r.choice([Fr(k) for k in (-4, -3, -2, 2, 3, 4)] + [Fr(1, 2), Fr(-1, 2), Fr(2, 3), Fr(-2, 3)])
        b = r.choice([v for v in range(-6, 7) if v])
        q = m.denominator
        xs = [x for x in range(-6, 7) if x % q == 0 and x]
        x1, x2 = sorted(r.sample(xs, 2))
        y1, y2 = m * x1 + b, m * x2 + b
        kind = r.choice(["inv", "order", "sign"])
        if kind == "inv" and abs(m) != 1:
            mw = Fr(x2 - x1) / (y2 - y1)
            slope_line = f"傾き $=\\dfrac{{{x2}-{par(x1)}}}{{{ftex(y2)}-{par(y1)}}}={ftex(mw)}$"
            bw = y1 - mw * x1
            break
        if kind == "order":
            mw = (y2 - y1) / Fr(x1 - x2)
            slope_line = f"傾き $=\\dfrac{{{ftex(y2)}-{par(y1)}}}{{{x1}-{par(x2)}}}={ftex(mw)}$"
            bw = y1 - mw * x1
            break
        if kind == "sign":
            mw = m
            slope_line = f"傾き $=\\dfrac{{{ftex(y2)}-{par(y1)}}}{{{x2}-{par(x1)}}}={ftex(m)}$"
            bw = y1 + m * x1
            if bw != b:
                break
    if kind == "sign":
        sub = f"$y={rhs(m, 0)}+b$ に $x={x1}$，$y={ftex(y1)}$ を代入して ${ftex(y1)}={ftex(m * x1)}+b$，$b={ftex(y1)}+{par(m * x1)}={ftex(bw)}$"
    else:
        sub = f"$y={rhs(mw, 0)}+b$ に $x={x1}$，$y={ftex(y1)}$ を代入して $b={ftex(bw)}$"
    sol = f"{slope_line}\n{sub}\n答え　${lin(mw, bw)}$"
    texts = {
        "inv": ("傾きを $\\dfrac{x\\text{ の増加量}}{y\\text{ の増加量}}$ と，分子と分母を逆にして求めている。", "傾きを求める式（分子と分母の取り違え）", "formula", "「2点の座標の差をわる」ことだけを覚えていて、どちらを分子にするかをあいまいにしている。"),
        "order": ("傾きを求めるとき，分子と分母で引く順番がそろっていない。", "傾きを求める式（引く順番）", "sign", "分子は「後−前」、分母は「前−後」と、順番を意識せずに計算してしまう。"),
        "sign": ("切片を求めるとき，${}$ を移項した符号の変化を誤っている。".replace("${}$", f"${ftex(m * x1)}$"), "切片を求める移項の計算", "sign", "移項すると符号が変わることを忘れやすい。"),
    }
    right, step, etype, tempt = texts[kind]
    cands = [(texts[k][0], f"Kさんの解答のこの部分は正しく計算されている。", "誤りの箇所の見落とし") for k in texts if k != kind]
    cands += [("代入する点は，$x$ 座標が大きい方の点でなければならない。", "どちらの点を代入しても、正しく計算すれば同じ式になる。", "代入の条件の誤解"),
              ("Kさんの解答に誤りはない。", f"Kさんの式は点 {pt(x2, y2)} を通らない。", "検算不足")]
    fix = f"傾き ${ftex(m)}$，切片 ${ftex(b)}$ で ${lin(m, b)}$"
    return _err_mc(f"〔問題〕2点 {pt(x1, y1)}，{pt(x2, y2)} を通る直線の式を求めなさい。", sol, right, cands,
                   f"正しくは {fix}。", dict(sol=sol, step=step, type=etype, tempt=tempt, fix=fix), d=3, p=6,
                   ap="Kさんの答えの式に、もう1つの点の座標を代入して成り立つかを確かめると、誤りがあることがすぐ分かる。そのうえで、傾きと切片の計算を1つずつ見直す。",
                   steps=[f"正しい傾き：$\\dfrac{{{ftex(y2)}-{par(y1)}}}{{{x2}-{par(x1)}}}={ftex(m)}$。", f"$y={rhs(m, 0)}+b$ に {pt(x1, y1)} を代入：$b={ftex(b)}$。", f"正しい答え：${lin(m, b)}$。"],
                   alt=[f"Kさんの答えに $x={x2}$ を代入すると $y={ftex(mw * x2 + bw)}$ となり ${ftex(y2)}$ にならないので、どこかに誤りがあると分かる。"],
                   pc=[("誤りの箇所を正しく指摘している", 3), ("正しい式を求めている", 3)],
                   pit=["傾きの分子・分母の取り違え。", "移項の符号の誤り。"],
                   chk=(f"({fpy(y2)}-({fpy(y1)}))/({x2}-({x1}))", fpy(m), None, "intermediate"))


@gen("error_correction", 3, ["common_error", "condition_check"])
def d_parallel_steps(r):
    while True:
        m = r.choice([-3, -2, 2, 3, 4, -4])
        c = r.randint(-6, 6)
        p = r.choice([v for v in range(-4, 5) if v])
        q = r.randint(-6, 6)
        if p != q and q - m * p != c:
            break
    b = q - m * p
    where = r.randint(0, 3)
    m_used = m
    l1 = f"平行な直線は傾きが等しいので，傾きは ${m}$"
    if where == 0:
        m_used = -m
        l1 = f"平行な直線は傾きの符号が逆になるので，傾きは ${-m}$"
    l2 = f"$y={m_used}x+b$ に $x={p}$，$y={q}$ を代入して ${q}={m_used}\\times{par(p)}+b$"
    b_used = q - m_used * p
    if where == 1:
        l2 = f"$y={m_used}x+b$ に $x={q}$，$y={p}$ を代入して ${p}={m_used}\\times{par(q)}+b$"
        b_used = p - m_used * q
    l3 = f"$b={q}-({m_used * p})={b_used}$" if where != 1 else f"$b={p}-({m_used * q})={b_used}$"
    if where == 2:
        b_used = q + m_used * p
        l3 = f"$b={q}+({m_used * p})={b_used}$"
    l4 = f"答え　${lin(m_used, b_used)}$"
    if where == 3:
        l4 = f"答え　${lin(m_used, c)}$"
    sol = "\n".join(f"{i + 1}行目　{t}" for i, t in enumerate([l1, l2, l3, l4]))
    LINES4 = ["1行目", "2行目", "3行目", "4行目"]
    ok = {0: "1行目は正しい。平行な2直線は傾きが等しい。", 1: "2行目は、点の $x$ 座標と $y$ 座標を正しく代入している。",
          2: "3行目は、2行目の式から $b$ を正しく求めている。", 3: "4行目は、求めた傾きと切片を正しく式にしている。"}
    why = {LINES4[i]: (ok[i], "誤りの箇所の見落とし") for i in range(4) if i != where}
    info = {0: ("1行目（平行な直線の傾き）", "concept", "「平行」と「垂直」や「反対向き」の意味を混同している。"),
            1: ("2行目（$x$ と $y$ を逆に代入）", "notation", "座標 $(x,\\,y)$ の順番を意識せずに代入している。"),
            2: ("3行目（移項の符号）", "sign", "移項するときに符号を変え忘れる。"),
            3: ("4行目（もとの直線の切片を使った）", "concept", "平行な直線は切片まで同じだと思いこんでいる。")}[where]
    fix = f"傾き ${m}$，切片 ${b}$ で ${lin(m, b)}$"
    return mc(f"〔問題〕直線 ${lin(m, c)}$ に平行で，点 $({p},\\,{q})$ を通る直線の式を求めなさい。\n〔Kさんの解答〕\n{sol}\nKさんの解答で，誤りが最初に生じた行として最も適するものを，" + SEL4,
              LINES4, f"誤りが最初に生じたのは{LINES4[where]}。正しくは {fix}。", d=3, p=6, keep=True, ai=where, why=why,
              err=dict(sol=sol, step=info[0], type=info[1], tempt=info[2], fix=fix),
              ap="1行ずつ、自分で正しい計算をして比べる。最後に答えの式が点 $(p,\\,q)$ を通るか、もとの直線と傾きが等しいかを確かめる。",
              steps=[f"平行なので傾きは ${m}$。", f"${q}={m}\\times{par(p)}+b$。", f"$b={b}$。", f"答え ${lin(m, b)}$。"],
              alt=[f"答えの式に $x={p}$ を代入して $y={q}$ になるかで検算する。"],
              pc=[("誤りの行を正しく指摘している", 3), ("正しい式を求めている", 3)],
              pit=["平行な直線の切片までもとの直線と同じにする。", "移項の符号の誤り。"],
              chk=(f"{q}-({m})*({p})", str(b), None, "intermediate"))


@gen("error_correction", 3, ["common_error", "condition_check", "cross_unit"], rel=["JH-MATH-G1-U04"])
def d_domain_err(r):
    m = r.choice([-4, -3, -2, -1, 1, 2, 3, 4])
    b = r.randint(-5, 5)
    p = r.randint(-4, 1)
    q = p + r.randint(2, 5)
    fp, fq = m * p + b, m * q + b
    open_left = r.random() < 0.5
    xs = f"{p}<x\\leqq {q}" if open_left else f"{p}\\leqq x<{q}"
    # 正しい y の変域：x=p（または q）の端が含まれるかどうかが y のどちらの端に対応するかを考える
    lo, hi = min(fp, fq), max(fp, fq)
    lo_open = (open_left and lo == fp) or ((not open_left) and lo == fq)
    hi_open = (open_left and hi == fp) or ((not open_left) and hi == fq)
    correct = f"{lo}{'<' if lo_open else '\\leqq '}y{'<' if hi_open else '\\leqq '}{hi}"
    kind = "order" if (m < 0 and r.random() < 0.5) else "strict"
    if kind == "order":
        a1, a2 = (fp, fq)
        wrong = f"{a1}{'<' if open_left else '\\leqq '}y{'\\leqq ' if open_left else '<'}{a2}"
        right = f"傾きが負なので，$x$ の小さい方の端 $x={p}$ に対応する $y={fp}$ が $y$ の大きい方の端になる。Kさんは大小を逆にしている。"
        step, etype, tempt = "$y$ の変域の大小の並べ方", "condition", "$x$ の変域と同じ順に $y$ の値を並べてしまう。"
        cands = [("$x$ の変域の端に「$<$」があるとき，$y$ の変域はすべて「$<$」にしなければならない。", "端が含まれるかどうかは、対応する端ごとに決まる。", "不等号の扱いの誤解"),
                 (f"$x={p}$ のときの $y$ の値の計算を誤っている。", f"$y={fp}$ は正しく計算されている。", "誤りの箇所の見落とし"),
                 ("Kさんの解答に誤りはない。", f"${fp}$ は ${fq}$ より大きいので、Kさんの不等式をみたす $y$ は存在しない。", "検算不足")]
    else:
        lo_w, hi_w = (not lo_open), (not hi_open)
        wrong = f"{lo}{'<' if lo_w else '\\leqq '}y{'<' if hi_w else '\\leqq '}{hi}"
        endp = p if open_left else q
        right = f"変域にふくまれない端は $x={endp}$ で，それに対応する $y={m * endp + b}$ の側に「$<$」をつけるべきなのに，反対側につけている。"
        step, etype, tempt = "不等号（$<$ と $\\leqq$）をつける位置", "condition", "$x$ の変域で左側に「$<$」があると、$y$ の変域でも左側に「$<$」をつけてしまう。"
        cands = [("傾きが負のときは，$y$ の変域の両端をどちらもふくめなければならない。", "端がふくまれるかどうかは、$x$ の変域の端がふくまれるかどうかで決まる。", "不等号の扱いの誤解"),
                 (f"$x={q}$ のときの $y$ の値の計算を誤っている。", f"$y={fq}$ は正しく計算されている。", "誤りの箇所の見落とし"),
                 ("Kさんの解答に誤りはない。", f"$x={endp}$ は変域にふくまれないので、$y={m * endp + b}$ もとらない。", "端の対応の見落とし")]
        if wrong == correct:
            raise AssertionError("同じ")
    sol = f"$x={p}$ のとき $y={fp}$，$x={q}$ のとき $y={fq}$\n答え　${wrong}$"
    fix = f"${correct}$"
    return _err_mc(f"〔問題〕一次関数 ${lin(m, b)}$ について，$x$ の変域が ${xs}$ のときの $y$ の変域を求めなさい。", sol, right, cands,
                   f"正しくは {fix}。", dict(sol=sol, step=step, type=etype, tempt=tempt, fix=fix), d=3, p=6,
                   ap="グラフをかき、$x$ の変域の両端に対応する点が「ふくまれる（●）」か「ふくまれない（○）」かを書きこんで、$y$ の範囲を読み取る（比例のグラフで学んだ変域の考え方とのつながり）。",
                   steps=[f"$x={p}$ のとき $y={fp}$，$x={q}$ のとき $y={fq}$。", f"{'傾きが負なので大小が入れかわる。' if m < 0 else '傾きが正なので大小はそのまま。'}", f"ふくまれない端に対応する $y$ の値には「$<$」をつけて ${correct}$。"],
                   alt=["グラフ上で、端の点を白丸・黒丸で表して $y$ 軸に投影すると、どちらの端に「$<$」がつくか一目で分かる。"],
                   pc=[("誤りの原因を正しく指摘している", 3), ("正しい変域を求めている", 3)],
                   pit=["傾きが負のときに大小を逆にし忘れる。", "不等号の位置を $x$ の変域と同じ側にしてしまう。"],
                   chk=(f"{m}*({p})+({b})", str(fp), None, "intermediate"))


GENERATORS = [a_rate, a_std_form, a_graph_read, a_is_linear,
              b_two_points, b_slope_point, b_intersection, b_domain, b_word,
              c_triangle_area, c_travel, c_xy_judge,
              d_two_points, d_parallel_steps, d_domain_err]


def _robust(g):
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


GENERATORS = [_robust(g) for g in GENERATORS]
