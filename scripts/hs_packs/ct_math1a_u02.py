"""単元パック：共通テスト対策　数学Ⅰ・A　データの分析・場合の数と確率・図形の性質。"""
from fractions import Fraction
from math import comb, factorial, gcd

import sympy as sp

from banks._common import desc, figure, mc, num, sa, shape, table
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem, tp)

UNIT_ID = "CT-MATH1A-U02"

PREREQUISITES = [
    ("HS-MATH1-U05", "四分位数・箱ひげ図・分散・標準偏差・相関係数の定義と計算、仮説検定の考え方を理解していること"),
    ("HS-MATHA-U01", "順列・組合せ、確率の基本性質、条件付き確率と乗法定理を使えること"),
    ("HS-MATHA-U02", "チェバ・メネラウスの定理、角の二等分線の性質、方べきの定理を使えること"),
]
EXTENSIONS = [
    ("CT-MATH2BC-U02", "確率変数・二項分布・統計的な推測（推定・検定）へと、データと確率の考え方が発展する"),
    ("HS-MATHB-U02", "確率分布・正規分布を用いた推定・仮説検定で、本単元の条件付き確率や検定の考え方を使う"),
    ("CT-MATH1A-U01", "図形の性質の問題で、三角比（余弦定理・面積公式）と組み合わせた融合問題に取り組む"),
]


# ----------------------------------------------------------------------
# 小道具
# ----------------------------------------------------------------------

def L(e):
    return sp.latex(sp.nsimplify(e))


def fr(p, q):
    f = Fraction(p, q)
    if f.denominator == 1:
        return str(f.numerator)
    s = "-" if f < 0 else ""
    return f"{s}\\dfrac{{{abs(f.numerator)}}}{{{f.denominator}}}"


def fpy(p, q):
    f = Fraction(p, q)
    return str(f.numerator) if f.denominator == 1 else f"Rational({f.numerator},{f.denominator})"


def fnum(f):
    """Fraction → 整数または有限小数の文字列。"""
    f = Fraction(f)
    if f.denominator == 1:
        return str(f.numerator)
    return str(float(f)).rstrip("0").rstrip(".")


def median(xs):
    xs = sorted(xs)
    n = len(xs)
    return Fraction(xs[n // 2]) if n % 2 else Fraction(xs[n // 2 - 1] + xs[n // 2], 2)


def quartiles(xs):
    xs = sorted(xs)
    n = len(xs)
    return median(xs[: n // 2]), median(xs), median(xs[(n + 1) // 2:])


def ratio(p, q):
    g = gcd(p, q)
    return f"{p // g}:{q // g}"


def boxplot_svg(groups, lo, hi, step=10):
    """groups=[(名前, (最小, Q1, 中央, Q3, 最大)), ...] の横向き箱ひげ図。"""
    W, left, right = 360, 46, 14
    rowh = 34
    H = rowh * len(groups) + 34
    X = lambda v: left + (v - lo) * (W - left - right) / (hi - lo)  # noqa: E731
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="serif" font-size="11">']
    ybase = rowh * len(groups) + 8
    out.append(f'<line x1="{X(lo):.1f}" y1="{ybase}" x2="{X(hi):.1f}" y2="{ybase}" stroke="#000"/>')
    for v in range(lo, hi + 1, step):
        out.append(f'<line x1="{X(v):.1f}" y1="{ybase}" x2="{X(v):.1f}" y2="{ybase + 4}" stroke="#000"/>')
        out.append(f'<text x="{X(v) - 6:.1f}" y="{ybase + 16}" font-size="9">{v}</text>')
        out.append(f'<line x1="{X(v):.1f}" y1="4" x2="{X(v):.1f}" y2="{ybase}" stroke="#e3e3e3" stroke-width="0.6"/>')
    for i, (name, (mn, q1, md, q3, mx)) in enumerate(groups):
        yc = rowh * i + rowh / 2 + 4
        out.append(f'<text x="4" y="{yc + 4:.1f}">{name}</text>')
        out.append(f'<line x1="{X(mn):.1f}" y1="{yc:.1f}" x2="{X(q1):.1f}" y2="{yc:.1f}" stroke="#000"/>')
        out.append(f'<line x1="{X(q3):.1f}" y1="{yc:.1f}" x2="{X(mx):.1f}" y2="{yc:.1f}" stroke="#000"/>')
        for v in (mn, mx):
            out.append(f'<line x1="{X(v):.1f}" y1="{yc - 6:.1f}" x2="{X(v):.1f}" y2="{yc + 6:.1f}" stroke="#000"/>')
        out.append(f'<rect x="{X(q1):.1f}" y="{yc - 10:.1f}" width="{X(q3) - X(q1):.1f}" height="20" fill="#cfdcec" stroke="#000"/>')
        out.append(f'<line x1="{X(md):.1f}" y1="{yc - 10:.1f}" x2="{X(md):.1f}" y2="{yc + 10:.1f}" stroke="#000" stroke-width="2"/>')
    out.append("</svg>")
    return "".join(out)


LESSON_BOX = [("A組", (32, 48, 58, 70, 94)), ("B組", (40, 52, 61, 66, 82))]


LESSON = lesson(
    goals=["箱ひげ図・散布図・要約統計量から「確実に言えること」と「言えないこと」を区別して判断できる。",
           "表や樹形図で状況を整理し、条件付き確率（原因の確率を含む）を正しく立式できる。",
           "図形の大問で、チェバ・メネラウス・方べき・角の二等分線のどれを使うかを図から判断し、比を素早く求められる。"],
    duration=100,
    readiness=["四分位数・四分位範囲を自分で求められる（数学Ⅰ データの分析）。",
               "条件付き確率 $P_A(B)=\\dfrac{P(A\\cap B)}{P(A)}$ の意味を説明できる（数学A）。",
               "メネラウスの定理を、三角形と直線を指定されれば使える（数学A 図形の性質）。"],
    flow=[("導入：3分野の大問に共通する読み方", 10, "資料・状況・図のどこに条件が書かれているかを探す練習"),
          ("データの分析", 25, "箱ひげ図の読み取り（例題1）と、変量変換・相関係数の公式の導出"),
          ("条件付き確率", 25, "表と樹形図による整理、原因の確率（例題2）"),
          ("図形の性質", 25, "メネラウスの定理の証明と、比の連鎖（例題3）"),
          ("時間戦略と典型的なわな", 10, "正誤判定の選択肢の検討順序、問題プリントDの誤答例"),
          ("まとめと確認", 5, "確認問題3問と課題指示")],
    sections=[
        intro("in1", "資料を「読む」問題で何が問われるか",
              "共通テストのデータの分析では、複数の箱ひげ図や散布図、表が示され、「次の記述のうち正しいもの」を選ばせる問題が中心になる。確率では、会話文や設定の説明から条件を読み取り、条件付き確率を立式する力が問われる。図形の性質では、図の中から定理を適用できる三角形と直線を見つけ出す力が差になる。いずれも、計算の前に「資料から何が確実に言えるか」「何が条件として与えられているか」を整理することが出発点である。",
              bullets=["データ：箱ひげ図から分かるのは5つの値（最小値・$Q_1$・中央値・$Q_3$・最大値）と、それによる「全体の約25%ずつ」の区切りだけ。平均値や個々の値は分からない。",
                       "確率：「〜であったとき」「〜という条件のもとで」は条件付き確率の合図。分母になる事象を最初に決める。",
                       "図形：比を求める問題は、メネラウス（三角形＋1本の直線）かチェバ（三角形＋1点で交わる3本の線）を疑う。"],
              points=[tp("最初に3つの資料（箱ひげ図・表・図）を並べて見せ、「この資料から確実に言えること」を1つずつ挙げさせる。", ask="箱ひげ図から平均値は分かるか。", expect="分からない。分かるのは5つの値だけ。", timing="導入"),
                      tp("正誤判定問題では、選択肢を「資料だけで判定できるもの」と「判定できないもの」に分けて考えると、時間を節約できることを伝える。", caution="「判定できない」は「誤り」として扱われる（正しいとは言えない）。")]),
        definition("df1", "箱ひげ図と変量変換の基本",
                   "データを小さい順に並べたとき、中央値で前半・後半に分け（データの個数が奇数なら中央値は含めない）、前半の中央値を第1四分位数 $Q_1$、後半の中央値を第3四分位数 $Q_3$ という。$Q_3-Q_1$ を四分位範囲という。",
                   formula="$$y=ax+b\\ \\text{のとき}\\quad \\overline{y}=a\\overline{x}+b,\\quad s_y^2=a^2s_x^2,\\quad s_y=|a|s_x$$",
                   conditions=["箱の中（$Q_1$ から $Q_3$）には、データの約半数が入る。ひげの長さは個数ではなく値の広がりを表す。",
                               "$u=ax+b,\\ v=cy+d$ のとき、共分散は $s_{uv}=ac\\,s_{xy}$、相関係数は $ac>0$ なら $r_{uv}=r_{xy}$、$ac<0$ なら $r_{uv}=-r_{xy}$。"],
                   points=[tp("「ひげが長い＝人数が多い」という誤解を、具体的なデータで否定する。", ask="ひげの長さが2倍なら、そこに入る人数も2倍か。", expect="いいえ。各区間に入る人数はほぼ同じで、値の広がりが違うだけ。")]),
        derivation("dv1", "変量変換の公式の導出",
                   ["$y_i=ax_i+b\\ (i=1,\\ \\dots,\\ n)$ とする。平均は $\\overline{y}=\\dfrac{1}{n}\\sum(ax_i+b)=a\\overline{x}+b$。",
                    "偏差は $y_i-\\overline{y}=a(x_i-\\overline{x})$ となり、$b$ が消える（平行移動は散らばりに影響しない）。",
                    "分散は $s_y^2=\\dfrac{1}{n}\\sum a^2(x_i-\\overline{x})^2=a^2s_x^2$。標準偏差は正なので $s_y=|a|s_x$。",
                    "同様に $u=ax+b,\\ v=cy+d$ なら $s_{uv}=ac\\,s_{xy}$、$r_{uv}=\\dfrac{ac\\,s_{xy}}{|a|s_x\\cdot|c|s_y}$ となり、相関係数は符号だけが変わりうる。"],
                   body="共通テストでは「単位を変える」「基準点からの差で考える」などの変換が頻出する。公式を覚えるより、偏差がどう変わるかで判断できるようにする。",
                   points=[tp("標準偏差で $|a|$ と絶対値がつく理由を、$a=-2$ の例で確認させる。", caution="$s_y=as_x$ とすると負の標準偏差が出てしまう。")]),
        theorem("th1", "条件付き確率と乗法定理",
                "$$P_A(B)=\\dfrac{P(A\\cap B)}{P(A)},\\qquad P(A\\cap B)=P(A)\\,P_A(B)$$",
                ["$P(A)>0$ のときに定義される。", "原因の確率：結果 $E$ が起きたとき原因が $H$ である確率は $P_E(H)=\\dfrac{P(H)P_H(E)}{P(H)P_H(E)+P(\\overline{H})P_{\\overline{H}}(E)}$。"],
                body="「〜であったとき」の部分が分母の事象になる。表で整理すれば、分母は「その行（列）の合計」、分子は「その行と列が交わるマス」である。",
                proof=["すべての根元事象が同様に確からしいとき、$A$ が起きたという条件のもとでは、$A$ の要素だけが起こりうる結果になる。",
                       "そのうち $B$ も起きているのは $A\\cap B$ の要素なので、$P_A(B)=\\dfrac{n(A\\cap B)}{n(A)}$。",
                       "分母・分子を全体の要素の個数 $n(U)$ で割ると $P_A(B)=\\dfrac{P(A\\cap B)}{P(A)}$。",
                       "両辺に $P(A)$ をかければ乗法定理 $P(A\\cap B)=P(A)P_A(B)$ が得られる。"],
                points=[tp("樹形図の枝に確率を書き、「枝に沿ってかける」「同じ結果に至る枝をたす」の2つの操作で原因の確率を計算させる。", ask="陽性になる経路は何本あるか。", expect="「病気で陽性」と「病気でないのに陽性」の2本。")]),
        theorem("th2", "メネラウスの定理",
                "$$\\dfrac{\\mathrm{AR}}{\\mathrm{RB}}\\cdot\\dfrac{\\mathrm{BP}}{\\mathrm{PC}}\\cdot\\dfrac{\\mathrm{CQ}}{\\mathrm{QA}}=1$$",
                ["$\\triangle\\mathrm{ABC}$ の辺またはその延長が、頂点を通らない1本の直線と点 $\\mathrm{R}$（直線 AB 上）、$\\mathrm{P}$（直線 BC 上）、$\\mathrm{Q}$（直線 CA 上）で交わるとき。",
                 "頂点 → 分点 → 頂点 → 分点 … と、三角形を一周する順に比をかける。"],
                proof=["頂点 $\\mathrm{C}$ を通り直線 $\\mathrm{PR}$ に平行な直線を引き、直線 $\\mathrm{AB}$ との交点を $\\mathrm{D}$ とする。",
                       "平行線と線分の比の性質より $\\dfrac{\\mathrm{BP}}{\\mathrm{PC}}=\\dfrac{\\mathrm{BR}}{\\mathrm{RD}}$、$\\dfrac{\\mathrm{CQ}}{\\mathrm{QA}}=\\dfrac{\\mathrm{DR}}{\\mathrm{RA}}$。",
                       "したがって $\\dfrac{\\mathrm{AR}}{\\mathrm{RB}}\\cdot\\dfrac{\\mathrm{BP}}{\\mathrm{PC}}\\cdot\\dfrac{\\mathrm{CQ}}{\\mathrm{QA}}=\\dfrac{\\mathrm{AR}}{\\mathrm{RB}}\\cdot\\dfrac{\\mathrm{BR}}{\\mathrm{RD}}\\cdot\\dfrac{\\mathrm{DR}}{\\mathrm{RA}}=1$。"],
                points=[tp("どの三角形とどの直線に適用するかを、図に色をつけて確認させる。求めたい比の線分を「辺」にもつ三角形を選ぶのがコツ。", ask="BP:PE を求めたいとき、どの三角形に適用するか。", expect="BE を辺にもつ三角形 ABE と、直線 DC。")],
                figure=figure("三角形ABCと、辺AB上の点R・辺CA上の点Q・辺BCの延長上の点Pを通る直線", shape({"A": (1.0, 3.0), "B": (0.0, 0.0), "C": (3.0, 0.0), "P": (6.0, 0.0), "Q": (2.0, 1.5), "R": (2.0 / 3, 2.0)},
                                                                                           segments=[("A", "B"), ("B", "C"), ("C", "A"), ("C", "P"), ("R", "P")], scale=34))),
        example("ex1", "例題1　箱ひげ図の読み取り",
                "下の箱ひげ図は、A組・B組（各39人）の数学のテストの得点を表したものである（架空の資料）。次の記述の正誤を判定せよ。(a) 四分位範囲はA組の方が大きい。(b) B組では、60点以上の生徒が20人以上いる。(c) A組の平均点はB組の平均点より低い。",
                ["(a) A組 $70-48=22$、B組 $66-52=14$。A組の方が大きいので正しい。",
                 "(b) B組の中央値は $61$ 点。39人の中央値は小さい方から20番目なので、20番目以降の20人は $61$ 点以上。よって正しい。",
                 "(c) 箱ひげ図から平均値は分からないので、正しいとは言えない。"],
                "(a) 正しい　(b) 正しい　(c) 判断できない（正しいとは言えない）",
                thinking="箱ひげ図から分かるのは5つの値だけ。人数についての記述は、中央値・四分位数が何番目の値かを考える。",
                figure=figure("A組とB組の得点の箱ひげ図", boxplot_svg(LESSON_BOX, 30, 100))),
        example("ex2", "例題2　原因の確率（検査の陽性）",
                "ある病気にかかっている人の割合は $2\\%$ である。ある検査は、病気の人を $95\\%$ の確率で陽性と判定し、病気でない人を $10\\%$ の確率で誤って陽性と判定する（架空の設定）。検査で陽性となった人が実際に病気である確率を求めよ。",
                ["$P(\\text{病気かつ陽性})=0.02\\times0.95=0.019$。", "$P(\\text{病気でなく陽性})=0.98\\times0.10=0.098$。",
                 "$P(\\text{陽性})=0.019+0.098=0.117$。", "求める確率は $\\dfrac{0.019}{0.117}=\\dfrac{19}{117}$。"],
                "$\\dfrac{19}{117}$（約 $16\\%$）",
                thinking="「陽性となったとき」なので、分母は陽性になるすべての場合。樹形図で2つの経路を求めてたす。",
                points=[tp("答えが約16%と意外に小さいことを話題にし、「病気でない人が圧倒的に多いので、誤った陽性の人数が多くなる」ことを人数（10000人で考える）で説明させる。", ask="10000人が検査を受けると、陽性は何人か。", expect="病気で陽性190人、病気でなく陽性980人の計1170人。")],
                misconceptions=[("陽性なら $95\\%$ の確率で病気である", "$95\\%$ は「病気のとき陽性になる確率」で、条件と結果が逆")]),
        example("ex3", "例題3　メネラウスの定理で比を求める",
                "$\\triangle\\mathrm{ABC}$ の辺 $\\mathrm{AB}$ を $2:1$ に内分する点を $\\mathrm{D}$、辺 $\\mathrm{AC}$ を $3:2$ に内分する点を $\\mathrm{E}$ とし、線分 $\\mathrm{BE}$ と $\\mathrm{CD}$ の交点を $\\mathrm{P}$ とする。$\\mathrm{BP}:\\mathrm{PE}$ を求めよ。",
                ["$\\triangle\\mathrm{ABE}$ と直線 $\\mathrm{DC}$ にメネラウスの定理を使う。", "$\\dfrac{\\mathrm{AD}}{\\mathrm{DB}}\\cdot\\dfrac{\\mathrm{BP}}{\\mathrm{PE}}\\cdot\\dfrac{\\mathrm{EC}}{\\mathrm{CA}}=1$。",
                 "$\\dfrac{2}{1}\\cdot\\dfrac{\\mathrm{BP}}{\\mathrm{PE}}\\cdot\\dfrac{2}{5}=1$ より $\\dfrac{\\mathrm{BP}}{\\mathrm{PE}}=\\dfrac{5}{4}$。"],
                "$\\mathrm{BP}:\\mathrm{PE}=5:4$",
                thinking="求める比 BP:PE の線分 BE を辺にもつ三角形を選ぶ。直線 DC がその三角形を横切っている。",
                points=[tp("$\\mathrm{EC}:\\mathrm{CA}$ は $2:5$（$\\mathrm{EC}:\\mathrm{EA}$ ではない）ことを、図で頂点から頂点までたどって確認させる。", caution="一周のたどり方を誤ると逆数の比が出る。")],
                misconceptions=[("$\\dfrac{\\mathrm{EC}}{\\mathrm{CA}}$ を $\\dfrac{2}{3}$ とする", "C は直線 AE の延長上の点で、CA は AC 全体の長さ $5$ にあたる")]),
        board("bd1", "板書案",
              [("① データ", ["箱ひげ図：5つの値だけ", "39人 → 中央値は20番目", "平均は分からない", "$y=ax+b$：$s_y=|a|s_x$", "相関係数は符号だけ変わる"]),
               ("② 条件付き確率", ["「〜のとき」→ 分母", "$P_A(B)=\\dfrac{P(A\\cap B)}{P(A)}$", "樹形図：かける・たす", "陽性 $0.019+0.098$", "答 $\\dfrac{19}{117}$"]),
               ("③ 図形の比", ["三角形＋直線 → メネラウス", "3本が1点 → チェバ", "頂点→分点→頂点 で一周", "$\\triangle\\mathrm{ABE}$ と直線 DC", "BP:PE $=5:4$"])],
              points=[tp("3列とも「最初に何を決めるか」（資料で分かること／分母の事象／適用する三角形）を1行目に書き、手順の共通点を意識させる。")]),
        guide("gd1", "指導ガイド（時間戦略と典型的なわな）",
              [tp("正誤判定の選択肢は、計算の要らないもの（資料から直接読めるもの）から先に判定させる。", timing="データの分析の演習中"),
               tp("条件付き確率では、問題文の「〜であったとき」に下線を引かせ、その事象を分母にする習慣をつけさせる。", ask="この問題で、分母になる事象は何か。"),
               tp("図形の比の問題では、メネラウスの定理を使う三角形を答案に明記させる（記述式の二次試験でも必要）。", caution="三角形を書かずに式だけ書くと、たどる順序を誤っても気づけない。"),
               tp("円順列・同じものを含む順列など、数え方の公式を使うときは「区別できるか」「回転して同じものを同一視するか」を毎回確認させる。")],
              misconceptions=[("ひげが長い区間には人数が多い", "各区間（最小値〜$Q_1$ など）に入る人数はほぼ等しい。ひげの長さは値の広がり"),
                              ("$P_A(B)$ と $P(A\\cap B)$ を同じものとする", "条件付き確率は「$A$ の中での割合」なので、分母は $P(A)$"),
                              ("方べきの定理を $\\mathrm{PA}\\cdot\\mathrm{AB}=\\mathrm{PC}\\cdot\\mathrm{CD}$ とする", "点 P から円との2つの交点までの長さの積：$\\mathrm{PA}\\cdot\\mathrm{PB}=\\mathrm{PC}\\cdot\\mathrm{PD}$")]),
        summary("sm1", "まとめ",
                ["箱ひげ図は5つの値と「約25%ずつ」の区切りだけを表す。平均値や個々の値について断定する選択肢は「正しいとは言えない」。",
                 "変量変換 $y=ax+b$：平均は $a\\overline{x}+b$、標準偏差は $|a|s_x$、相関係数は符号だけが変わりうる。",
                 "条件付き確率は「条件の事象」を分母に。原因の確率は樹形図の経路の確率の比。",
                 "比の問題はメネラウス・チェバ。適用する三角形を明記し、頂点→分点の順に一周する。"]),
        check("ck1", "確認問題",
              [("変量 $x$ の標準偏差が $6$ のとき、$y=-3x+20$ の標準偏差を求めよ。", "$|-3|\\times6=18$"),
               ("赤玉3個・白玉2個から1個ずつ2回、戻さずに取り出す。1回目が白玉であったとき、2回目が赤玉である確率は。", "残り4個のうち赤玉3個なので $\\dfrac{3}{4}$"),
               ("円の外部の点 P から引いた直線が円と A, B で交わり（PA=4, AB=5）、別の直線が C, D で交わる（PC=3）。CD を求めよ。", "$4\\cdot9=3(3+\\mathrm{CD})$ より $\\mathrm{CD}=9$")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

@gen("basic_check", 5, ["computation"])
def quartile_calc(r):
    n = r.choice([9, 10, 11, 12, 13])
    xs = sorted(r.sample(range(28, 99), n))
    q1, md, q3 = quartiles(xs)
    kind = r.choice(["q1", "q3", "iqr", "md"])
    name, val, ex = {"q1": ("第1四分位数", q1, "[0]"), "q3": ("第3四分位数", q3, "[2]"), "md": ("中央値", md, "[1]"),
                     "iqr": ("四分位範囲", q3 - q1, "")}[kind]
    data = "，".join(map(str, xs))
    expr = f"quartiles([{', '.join(map(str, xs))}])[2]-quartiles([{', '.join(map(str, xs))}])[0]" if kind == "iqr" else f"quartiles([{', '.join(map(str, xs))}]){ex}"
    lower, upper = xs[: n // 2], xs[(n + 1) // 2:]
    return num(f"ある高校の {n} 人の生徒について、1週間の読書時間（分）を小さい順に並べると次のようになった（架空のデータ）。{data}　このデータの{name}を求めなさい。",
               fnum(val), f"中央値 ${fnum(md)}$、$Q_1={fnum(q1)}$、$Q_3={fnum(q3)}$。", d=2, unit="分",
               ap="四分位数は「中央値で前半・後半に分け、それぞれの中央値をとる」。データの個数が奇数のときは、中央値そのものは前半にも後半にも入れない。",
               steps=[f"データは {n} 個。中央値は {'小さい方から ' + str(n // 2 + 1) + ' 番目' if n % 2 else str(n // 2) + ' 番目と ' + str(n // 2 + 1) + ' 番目の平均'} で ${fnum(md)}$。",
                      f"前半 {len(lower)} 個（{'，'.join(map(str, lower))}）の中央値 $Q_1={fnum(q1)}$。",
                      f"後半 {len(upper)} 個（{'，'.join(map(str, upper))}）の中央値 $Q_3={fnum(q3)}$。"]
               + ([f"四分位範囲 $Q_3-Q_1={fnum(q3 - q1)}$。"] if kind == "iqr" else []),
               alt=["データの個数 $n$ から「何番目の値か」を先に決めておく方法：$n=" + str(n) + "$ のとき、$Q_1$ は前半 " + str(len(lower)) + " 個の真ん中にあたる。番号で確認してから値を読むと、読み違いを防げる。"],
               pc=[("中央値で正しく前半・後半に分けている", 1), (f"{name}を正しく求めている", 1)],
               pit=["データの個数が奇数のとき、中央値を前半・後半の両方に含めてしまう。", "四分位範囲を $Q_3-Q_1$ ではなく最大値 $-$ 最小値（範囲）と混同する。"],
               chk=(expr, fnum(val)))


CONTEXTS_LIN = [("英語のテストの得点", "点", "換算点"), ("ある地点の最高気温（℃）", "℃", "華氏温度に近い指標"), ("1日の歩数（百歩単位）", "百歩", "指標")]


@gen("basic_check", 5, ["computation", "concept"])
def lin_transform(r):
    m = r.randint(40, 75)
    s = r.randint(3, 14)
    a = r.choice([2, 3, 5, -2, -3, -1, 4])
    b = r.choice([-40, -20, -10, 5, 10, 20, 30, 50])
    kind = r.choice(["mean", "var", "sd"])
    name, val, ex = {"mean": ("平均値", a * m + b, f"{a}*{m}+({b})"), "var": ("分散", a * a * s * s, f"({a})**2*{s * s}"),
                     "sd": ("標準偏差", abs(a) * s, f"Abs({a})*sqrt({s * s})")}[kind]
    return num(f"変量 $x$ のデータの平均値が ${m}$、分散が ${s * s}$ である（架空のデータ）。各値を $y={'' if a == 1 else ('-' if a == -1 else a)}x{'+' if b > 0 else ''}{b}$ によって新しい変量 $y$ に変換したとき、$y$ の{name}を求めなさい。",
               str(val), f"$y=ax+b$ のとき {name}は " + {"mean": "$a\\overline{x}+b$", "var": "$a^2s_x^2$", "sd": "$|a|s_x$"}[kind] + "。", d=2,
               ap="変量変換では、平均値は式どおり $a\\overline{x}+b$ に変わるが、散らばり（分散・標準偏差）は平行移動 $b$ の影響を受けず、倍率 $a$ の影響だけを受ける。",
               steps=[f"$a={a},\\ b={b}$、$\\overline{{x}}={m}$、$s_x^2={s * s}$（$s_x={s}$）。",
                      {"mean": f"$\\overline{{y}}={a}\\times{m}{'+' if b > 0 else ''}{b}={val}$。", "var": f"$s_y^2=({a})^2\\times{s * s}={val}$。",
                       "sd": f"$s_y=|{a}|\\times{s}={val}$。"}[kind]],
               alt=["偏差で考える：$y_i-\\overline{y}=" + str(a) + "(x_i-\\overline{x})$ なので、偏差は $" + str(a) + "$ 倍、偏差の2乗は $" + str(a * a) + "$ 倍になる。ここから分散・標準偏差の変化が分かる。"],
               pc=[("変換の公式を正しく選んでいる", 1), ("値を正しく計算している", 1)],
               pit=["分散・標準偏差にも $b$ を加えてしまう。", "分散を $a$ 倍（$a^2$ 倍ではなく）にする、または標準偏差を負の値にする。"],
               chk=(ex, str(val)))


TABLE_CTX = [
    ("通学方法", ("自転車", "自転車以外"), "朝食", ("毎日食べる", "食べない日がある")),
    ("部活動", ("運動部", "運動部以外"), "睡眠時間", ("7時間以上", "7時間未満")),
    ("学年", ("1年生", "2年生"), "図書館の利用", ("週1回以上", "週1回未満")),
    ("スマートフォンの使用時間", ("2時間以上", "2時間未満"), "小テストの結果", ("合格", "不合格")),
]


@gen("basic_check", 5, ["computation", "concept"])
def cond_table(r):
    rn, rows, cn, cols = r.choice(TABLE_CTX)
    t = [[r.randint(6, 45) for _ in range(2)] for _ in range(2)]
    i, j = r.randint(0, 1), r.randint(0, 1)
    by_row = r.choice([True, False])
    if by_row:
        den = sum(t[i])
        cond, ev = f"{rn}が「{rows[i]}」", f"{cn}が「{cols[j]}」"
    else:
        den = t[0][j] + t[1][j]
        cond, ev = f"{cn}が「{cols[j]}」", f"{rn}が「{rows[i]}」"
    nm = t[i][j]
    N = sum(map(sum, t))
    tb = table([[rows[0], t[0][0], t[0][1], sum(t[0])], [rows[1], t[1][0], t[1][1], sum(t[1])],
                ["計", t[0][0] + t[1][0], t[0][1] + t[1][1], N]], header=[f"{rn}＼{cn}", cols[0], cols[1], "計"], caption="架空の調査結果（人）")
    return sa(f"ある高校の生徒 {N} 人に、{rn}と{cn}について調査した結果が下の表である（架空のデータ）。この中から1人を選ぶとき、選んだ生徒の{cond}であったという条件のもとで、{ev}である条件付き確率を求めなさい。",
              f"${fr(nm, den)}$", f"条件の事象（{cond}）の人数 {den} 人のうち、{ev}は {nm} 人。", d=2, tbl=tb, v=[f"{Fraction(nm, den).numerator}/{Fraction(nm, den).denominator}"],
              ap="「〜という条件のもとで」の部分が分母になる。表では、その行（または列）の合計が分母、交わるマスが分子。",
              steps=[f"条件の事象：{cond}の生徒は {den} 人。", f"そのうち{ev}の生徒は {nm} 人。", f"条件付き確率は $\\dfrac{{{nm}}}{{{den}}}={fr(nm, den)}$。"],
              alt=[f"確率の式で：$P(A\\cap B)=\\dfrac{{{nm}}}{{{N}}}$、$P(A)=\\dfrac{{{den}}}{{{N}}}$ として $\\dfrac{{P(A\\cap B)}}{{P(A)}}$ を計算しても同じ値になる（全体の人数 {N} が約分で消える）。"],
              pc=[("分母となる条件の事象の人数を正しく選んでいる", 1), ("条件付き確率を正しく求めている", 1)],
              pit=[f"分母を全体の人数 {N} にしてしまう（これは $P(A\\cap B)$）。", "行と列を取り違え、逆の条件付き確率を求める。"],
              chk=(f"Rational({nm},{den})", fpy(nm, den)))


@gen("basic_check", 5, ["computation", "condition_check"])
def count_basic(r):
    kind = r.choice(["circle", "multiset", "path", "committee"])
    if kind == "circle":
        n = r.randint(5, 9)
        val = 2 * factorial(n - 2)
        stem = f"{n} 人が円形のテーブルのまわりに等間隔に座る。特定の2人 $\\mathrm{{A}},\\ \\mathrm{{B}}$ が隣り合う座り方は何通りあるか。ただし、回転して一致する座り方は同じものとみなす。"
        steps = ["A と B をひとまとまりにして、$" + str(n - 1) + "$ 個のものの円順列と考える：$(" + str(n - 1) + "-1)!=" + str(factorial(n - 2)) + "$ 通り。",
                 f"まとまりの中で A, B の並び方が $2$ 通り。", f"$2\\times{factorial(n - 2)}={val}$ 通り。"]
        ex = f"2*factorial({n - 2})"
        ap = "回転して一致するものを同じとみなすので円順列。隣り合う2人は1つのまとまりとして数え、最後にまとまりの中の並び方をかける。"
        pit = ["円順列なのに $(n-1)!$ ではなく $n!$ で数える。", "まとまりの中の並び方 $2$ 通りをかけ忘れる。"]
        alt = [f"A の席を固定して考える：B は A の左右どちらかの $2$ 通り、残り ${n - 2}$ 人の並び方は ${n - 2}!$ 通りで、$2\\times{n - 2}!={val}$ 通り。"]
    elif kind == "multiset":
        word, cnts = r.choice([("SUCCESS", (3, 2, 1, 1)), ("BANANA", (3, 2, 1)), ("COMMITTEE", (2, 2, 2, 1, 1, 1)), ("STATISTICS", (3, 3, 2, 1, 1)),
                               ("KANAGAWA", (4, 1, 1, 1, 1)), ("YOKOHAMA", (2, 2, 1, 1, 1, 1)), ("ASSESSMENT", (4, 2, 1, 1, 1, 1))])
        n = len(word)
        den = 1
        for c in cnts:
            den *= factorial(c)
        val = factorial(n) // den
        stem = f"英単語 {word} の {n} 文字をすべて1列に並べる。並べ方は何通りあるか。"
        dtex = "\\,".join(f"{c}!" for c in cnts if c > 1)
        steps = [f"{n} 文字のうち、同じ文字の個数は " + "、".join(str(c) for c in cnts if c > 1) + " 個ずつ。",
                 f"同じものを含む順列：$\\dfrac{{{n}!}}{{{dtex}}}$。", f"${val}$ 通り。"]
        ex = f"factorial({n})/({'*'.join(f'factorial({c})' for c in cnts)})"
        ap = "同じ文字は区別できないので、すべて区別したときの $n!$ を、同じ文字どうしの入れかえの数で割る。"
        pit = ["同じ文字を区別して $n!$ 通りとする。", "同じ文字の個数を数え間違える。"]
        alt = [f"文字を置く場所を選ぶ方法：最も多い文字の置き場所を組合せで選び、残りの場所に次の文字を…と順に選んで積をとっても ${val}$ 通りになる。"]
    elif kind == "path":
        p, q = r.randint(4, 7), r.randint(3, 5)
        a, b = r.randint(1, p - 1), r.randint(1, q - 1)
        val = comb(a + b, a) * comb(p - a + q - b, p - a)
        stem = f"南北に走る道が ${p + 1}$ 本、東西に走る道が ${q + 1}$ 本、碁盤の目のように通る町で、南西の角 $\\mathrm{{S}}$ から北東の角 $\\mathrm{{G}}$ まで、東または北へ進む最短経路で行く。$\\mathrm{{S}}$ から東へ ${a}$ 区画、北へ ${b}$ 区画の交差点 $\\mathrm{{P}}$ を必ず通る経路は何通りあるか。"
        steps = [f"S から P まで：東 ${a}$、北 ${b}$ の並べ方 ${{}}_{{{a + b}}}\\mathrm{{C}}_{{{a}}}={comb(a + b, a)}$ 通り。",
                 f"P から G まで：東 ${p - a}$、北 ${q - b}$ の並べ方 ${{}}_{{{p - a + q - b}}}\\mathrm{{C}}_{{{p - a}}}={comb(p - a + q - b, p - a)}$ 通り。", f"積の法則で ${val}$ 通り。"]
        ex = f"binomial({a + b},{a})*binomial({p - a + q - b},{p - a})"
        ap = "最短経路は「東」「北」の並べ方で決まる。P を必ず通るので、S→P と P→G に分けて積の法則を使う。"
        pit = ["S→P と P→G の場合の数を足してしまう（積の法則を使う場面）。", "区画の数と道の本数を取り違える。"]
        alt = ["交差点ごとに「そこへ至る経路の数」を書き込んでいく方法（左と下の数の和）で数えても、同じ値になる。"]
    else:
        mm, w = r.randint(4, 7), r.randint(3, 5)
        k = r.randint(3, min(5, mm))
        val = comb(mm + w, k) - comb(mm, k)
        stem = f"男子 {mm} 人、女子 {w} 人の中から {k} 人の委員を選ぶ。女子が少なくとも1人含まれる選び方は何通りあるか。"
        steps = [f"全体：${{}}_{{{mm + w}}}\\mathrm{{C}}_{{{k}}}={comb(mm + w, k)}$ 通り。", f"女子が1人も含まれない（男子だけ）：${{}}_{{{mm}}}\\mathrm{{C}}_{{{k}}}={comb(mm, k)}$ 通り。", f"${comb(mm + w, k)}-{comb(mm, k)}={val}$ 通り。"]
        ex = f"binomial({mm + w},{k})-binomial({mm},{k})"
        ap = "「少なくとも1人」は余事象（1人もいない）を全体から引くと速い。"
        pit = ["女子1人を先に選んでから残りを選ぶ（${}_{" + str(w) + "}\\mathrm{C}_1\\times{}_{" + str(mm + w - 1) + "}\\mathrm{C}_{" + str(k - 1) + "}$）と、重複して数えてしまう。"]
        alt = ["女子の人数で場合分けして（1人、2人、…）、それぞれの選び方を足しても同じ値になる。"]
    return num(stem, str(val), steps[-1], d=2, ap=ap, steps=steps, alt=alt,
               pc=[("数え方（公式）を正しく選んでいる", 1), ("正しい値を求めている", 1)], pit=pit, chk=(ex, str(val)))


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 5, ["computation", "concept"])
def corr_summary(r):
    for _ in range(300):
        sx, sy = r.randint(3, 15), r.randint(3, 15)
        sxy = r.choice([-1, 1]) * r.randint(2, sx * sy - 1)
        rr = sxy / (sx * sy)
        if 0.2 < abs(rr) < 0.97:
            break
    from decimal import ROUND_HALF_UP, Decimal
    ans = str(Decimal(repr(rr)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
    kind = r.choice(["r", "r", "cov"])
    tb = table([["$x$（数学の得点）", sx], ["$y$（物理の得点）", sy]], header=["変量", "標準偏差"], caption="架空の資料")
    strength = "強い正の相関" if rr >= 0.7 else "正の相関" if rr > 0.2 else "強い負の相関" if rr <= -0.7 else "負の相関"
    if kind == "r":
        return num(f"ある学年の生徒について、数学の得点 $x$ と物理の得点 $y$ の標準偏差は下の表のとおりで、$x$ と $y$ の共分散は ${sxy}$ であった（架空の資料）。$x$ と $y$ の相関係数を、小数第3位を四捨五入して小数第2位まで求めなさい。",
                   ans, f"$r=\\dfrac{{s_{{xy}}}}{{s_xs_y}}=\\dfrac{{{sxy}}}{{{sx}\\times{sy}}}\\fallingdotseq{ans}$。{strength}がある。", d=3, tbl=tb,
                   ap="相関係数は共分散を2つの標準偏差の積で割ったもの。値は必ず $-1\\leqq r\\leqq1$ になるので、範囲外になれば計算ミスと分かる。",
                   steps=[f"$s_xs_y={sx}\\times{sy}={sx * sy}$。", f"$r=\\dfrac{{{sxy}}}{{{sx * sy}}}={rr:.4f}\\cdots$。", f"小数第3位を四捨五入して ${ans}$。"],
                   alt=["符号と大きさの見当をつけてから計算する：共分散が" + ("正" if sxy > 0 else "負") + "なので $r$ も" + ("正" if sxy > 0 else "負") + "。$|s_{xy}|$ が $s_xs_y$ に近いほど $|r|$ は $1$ に近い。"],
                   pc=[("相関係数の定義式に正しく代入している", 2), ("正しく四捨五入している", 2)],
                   pit=["分母を分散の積 $s_x^2s_y^2$ にしてしまう。", "共分散の符号を落とす。"],
                   chk=(f"floor(Rational({sxy},{sx * sy})*100+Rational(1,2))/100" if sxy > 0 else f"-floor(Rational({-sxy},{sx * sy})*100+Rational(1,2))/100", ans))
    rr2 = Fraction(r.choice([-1, 1]) * r.choice([2, 3, 4, 5, 6, 7, 8, 9]), 10)
    cov = rr2 * sx * sy
    return num(f"ある学年の生徒について、数学の得点 $x$ と物理の得点 $y$ の標準偏差は下の表のとおりで、相関係数は ${fnum(rr2)}$ であった（架空の資料）。$x$ と $y$ の共分散を求めなさい。",
               fnum(cov), f"$s_{{xy}}=r\\,s_xs_y={fnum(rr2)}\\times{sx}\\times{sy}={fnum(cov)}$。", d=3, tbl=tb,
               ap="相関係数の定義 $r=\\dfrac{s_{xy}}{s_xs_y}$ を共分散について解く。",
               steps=[f"$s_{{xy}}=r\\,s_xs_y$。", f"$={fnum(rr2)}\\times{sx * sy}={fnum(cov)}$。"],
               alt=["求めた共分散を定義式に戻し、$\\dfrac{" + fnum(cov) + "}{" + str(sx * sy) + "}=" + fnum(rr2) + "$ となるかで検算する。"],
               pc=[("定義式を共分散について正しく解いている", 2), ("正しく計算している", 2)],
               pit=["標準偏差の代わりに分散をかけてしまう。", "相関係数の符号を落とす。"],
               chk=(f"Rational({rr2.numerator},{rr2.denominator})*{sx}*{sy}", fnum(cov)))


@gen("standard_practice", 5, ["computation", "application"])
def bayes_test(r):
    p = r.choice([1, 2, 4, 5, 10, 20])
    se = r.choice([80, 90, 95, 98, 99])
    fp = r.choice([2, 4, 5, 10, 20])
    kind = r.choice(["post", "post", "pos"])
    a, b = p * se, (100 - p) * fp
    if kind == "post":
        val = Fraction(a, a + b)
        q = "検査で陽性と判定された人が、実際にその病気にかかっている確率"
    else:
        val = Fraction(a + b, 10000)
        q = "無作為に選んだ1人が検査で陽性と判定される確率"
    return sa(f"ある病気にかかっている人の割合は ${p}\\%$ である。ある検査は、病気にかかっている人を ${se}\\%$ の確率で陽性と判定し、病気にかかっていない人を ${fp}\\%$ の確率で誤って陽性と判定する（架空の設定）。{q}を求めなさい。",
              f"${fr(val.numerator, val.denominator)}$", f"陽性になる確率 $P(E)=\\dfrac{{{p}}}{{100}}\\cdot\\dfrac{{{se}}}{{100}}+\\dfrac{{{100 - p}}}{{100}}\\cdot\\dfrac{{{fp}}}{{100}}=\\dfrac{{{a + b}}}{{10000}}$。", d=3,
              v=[f"{val.numerator}/{val.denominator}"],
              ap="樹形図で「病気／病気でない」→「陽性／陰性」と枝分かれさせ、枝の確率をかける。陽性になる経路は2本あるので足す。" + ("「陽性と判定されたとき」なので、陽性全体を分母にする。" if kind == "post" else ""),
              steps=[f"病気かつ陽性：$\\dfrac{{{p}}}{{100}}\\times\\dfrac{{{se}}}{{100}}=\\dfrac{{{a}}}{{10000}}$。", f"病気でなく陽性：$\\dfrac{{{100 - p}}}{{100}}\\times\\dfrac{{{fp}}}{{100}}=\\dfrac{{{b}}}{{10000}}$。",
                     f"陽性の確率：$\\dfrac{{{a + b}}}{{10000}}$。"] + ([f"求める確率：$\\dfrac{{{a}}}{{{a + b}}}={fr(val.numerator, val.denominator)}$。"] if kind == "post" else [f"約分して ${fr(val.numerator, val.denominator)}$。"]),
              alt=[f"10000人の集団で考える：病気 ${p * 100}$ 人のうち陽性 ${a}$ 人、病気でない ${(100 - p) * 100}$ 人のうち陽性 ${b}$ 人。人数の比で確率が求められる。"],
              pc=[("2つの経路の確率を正しく求めている", 2), ("求める確率を正しく立式・計算している", 2)],
              pit=[f"検査の精度 ${se}\\%$ をそのまま答えにしてしまう（条件と結果が逆）。", "誤って陽性となる経路を足し忘れる。"],
              chk=(f"Rational({a},10000)/Rational({a + b},10000)" if kind == "post" else f"Rational({p},100)*Rational({se},100)+Rational({100 - p},100)*Rational({fp},100)",
                   fpy(val.numerator, val.denominator)))


def _five(r):
    while True:
        v = sorted(r.sample(range(20, 100), 5))
        if v[1] - v[0] >= 4 and v[4] - v[3] >= 4 and v[2] - v[1] >= 3 and v[3] - v[2] >= 3:
            return tuple(v)


def _box_pool(r, G, S):
    pool = []  # (文, 真偽, 理由)
    for g in G:
        mn, q1, md, q3, mx = S[g]
        for h in G:
            if h == g:
                continue
            m2 = S[h]
            pool.append((f"{g}の範囲は{h}の範囲より大きい", (mx - mn) > (m2[4] - m2[0]), f"範囲は {g} が ${mx}-{mn}={mx - mn}$、{h} が ${m2[4]}-{m2[0]}={m2[4] - m2[0]}$。"))
            pool.append((f"{g}の四分位範囲は{h}の四分位範囲より大きい", (q3 - q1) > (m2[3] - m2[1]), f"四分位範囲は {g} が ${q3 - q1}$、{h} が ${m2[3] - m2[1]}$。"))
            pool.append((f"{g}の第1四分位数は{h}の中央値より大きい", q1 > m2[2], f"{g} の $Q_1={q1}$、{h} の中央値 ${m2[2]}$。"))
        t = r.randint(md - 6, md + 6)
        if t != md:
            pool.append((f"{g}では、{t}点以上の生徒が20人以上いる", md >= t, f"{g} の中央値は ${md}$ 点で、39人の中央値は小さい方から20番目の値。中央値が {t} 点{'以上なので20番目以降の20人は' + str(t) + '点以上' if md >= t else '未満なので、' + str(t) + '点以上の生徒は19人以下'}。"))
        u = r.randint(q3 - 5, q3 + 5)
        if u != q3:
            pool.append((f"{g}では、{u}点以上の生徒が10人以上いる", q3 >= u, f"{g} の $Q_3={q3}$ 点。39人の $Q_3$ は大きい方から10番目の値なので、{'$Q_3\\geqq' + str(u) + '$ より10人以上が' + str(u) + '点以上' if q3 >= u else '$Q_3<' + str(u) + '$ より' + str(u) + '点以上の生徒は9人以下'}。"))
    pool.append((f"1組の平均点は{S['1組'][2]}点である", None, "箱ひげ図からは平均値は分からない。中央値と平均値は一般に異なる。"))
    return pool


@gen("standard_practice", 5, ["concept", "condition_check"])
def boxplot_mc(r):
    G = ["1組", "2組", "3組"]
    while True:
        S = {g: _five(r) for g in G}
        pool = _box_pool(r, G, S)
        if any(x[1] is True for x in pool) and sum(1 for x in pool if x[1] is not True) >= 3:
            break
    trues = [x for x in pool if x[1] is True]
    falses = [x for x in pool if x[1] is not True]
    right = r.choice(trues)
    wrongs = r.sample(falses, 3)
    tb = table([[g] + list(S[g]) for g in G], header=["", "最小値", "第1四分位数", "中央値", "第3四分位数", "最大値"], caption="架空の資料（各組39人）")
    return mc("ある高校の1組・2組・3組（各39人）の数学の小テストの得点を、箱ひげ図と表にまとめた（架空の資料）。この資料から確実に正しいといえるものを、次のうちから一つ選びなさい。",
              [right[0]] + [w[0] for w in wrongs], right[2] + "よって正しい。", d=3, tbl=tb,
              fig=figure("3つの組の得点の箱ひげ図", boxplot_svg([(g, S[g]) for g in G], 20, 100)),
              ap="箱ひげ図から分かるのは5つの値だけ。人数に関する記述は、39人の中央値が20番目、$Q_1$ が10番目、$Q_3$ が30番目（大きい方から10番目）の値であることを使って判定する。",
              steps=["各選択肢が、5つの値だけで判定できるかを確認する。", "判定できるものは、表の値で比較する。", f"正しいのは「{right[0]}」。{right[2]}"],
              alt=["人数の記述は、具体的に「何番目の値か」を図に書き込んで確かめる。平均値や個々の値についての記述は、それだけで「確実に正しい」とはいえない。"],
              pc=[("各記述を5つの値で判定している", 2), ("正しい記述を選んでいる", 2)],
              why={w[0]: ((w[2] + ("よって誤り。" if w[1] is False else "正しいとは判断できない。")), "箱ひげ図の読み取りの誤り" if w[1] is False else "箱ひげ図から分からない情報の断定") for w in wrongs},
              pit=["ひげの長さを人数の多さと誤解する。", "箱ひげ図から平均値を読み取れると考える。"])


@gen("standard_practice", 5, ["computation", "condition_check"])
def ratio_theorems(r):
    kind = r.choice(["mene_bp", "mene_cp", "ceva"])
    p, q = r.sample(range(1, 6), 2)
    s_, t_ = r.sample(range(1, 6), 2)
    if kind == "ceva":
        val = Fraction(q * t_, p * s_)
        stem = (f"$\\triangle\\mathrm{{ABC}}$ の辺 $\\mathrm{{AB}}$ を ${p}:{q}$ に内分する点を $\\mathrm{{D}}$、辺 $\\mathrm{{BC}}$ を ${s_}:{t_}$ に内分する点を $\\mathrm{{E}}$ とする。"
                f"線分 $\\mathrm{{AE}}$ と $\\mathrm{{CD}}$ の交点を $\\mathrm{{P}}$ とし、直線 $\\mathrm{{BP}}$ と辺 $\\mathrm{{CA}}$ の交点を $\\mathrm{{F}}$ とするとき、$\\mathrm{{CF}}:\\mathrm{{FA}}$ を求めなさい。")
        target = "\\mathrm{CF}:\\mathrm{FA}"
        steps = ["3本の線分 AE, CD, BF が1点 P で交わるので、チェバの定理を使う。", "$\\dfrac{\\mathrm{AD}}{\\mathrm{DB}}\\cdot\\dfrac{\\mathrm{BE}}{\\mathrm{EC}}\\cdot\\dfrac{\\mathrm{CF}}{\\mathrm{FA}}=1$。",
                 f"$\\dfrac{{{p}}}{{{q}}}\\cdot\\dfrac{{{s_}}}{{{t_}}}\\cdot\\dfrac{{\\mathrm{{CF}}}}{{\\mathrm{{FA}}}}=1$ より $\\dfrac{{\\mathrm{{CF}}}}{{\\mathrm{{FA}}}}={fr(val.numerator, val.denominator)}$。"]
        ap = "三角形の3つの頂点から引いた線分が1点で交わる配置なので、チェバの定理。頂点→分点→頂点…と一周する順に比をかける。"
        chk = f"Rational({q},{p})*Rational({t_},{s_})"
        alt = "面積比で確かめる方法：$\\triangle\\mathrm{PAB}:\\triangle\\mathrm{PBC}:\\triangle\\mathrm{PCA}$ を比で表すと、$\\mathrm{CF}:\\mathrm{FA}=\\triangle\\mathrm{PBC}:\\triangle\\mathrm{PAB}$ として同じ比が得られる。"
    elif kind == "mene_bp":
        val = Fraction(q * (s_ + t_), p * t_)
        stem = (f"$\\triangle\\mathrm{{ABC}}$ の辺 $\\mathrm{{AB}}$ を ${p}:{q}$ に内分する点を $\\mathrm{{D}}$、辺 $\\mathrm{{AC}}$ を ${s_}:{t_}$ に内分する点を $\\mathrm{{E}}$ とし、"
                f"線分 $\\mathrm{{BE}}$ と $\\mathrm{{CD}}$ の交点を $\\mathrm{{P}}$ とする。$\\mathrm{{BP}}:\\mathrm{{PE}}$ を求めなさい。")
        target = "\\mathrm{BP}:\\mathrm{PE}"
        steps = ["線分 BE を辺にもつ $\\triangle\\mathrm{ABE}$ と、直線 DC にメネラウスの定理を使う。", "$\\dfrac{\\mathrm{AD}}{\\mathrm{DB}}\\cdot\\dfrac{\\mathrm{BP}}{\\mathrm{PE}}\\cdot\\dfrac{\\mathrm{EC}}{\\mathrm{CA}}=1$。",
                 f"$\\dfrac{{{p}}}{{{q}}}\\cdot\\dfrac{{\\mathrm{{BP}}}}{{\\mathrm{{PE}}}}\\cdot\\dfrac{{{t_}}}{{{s_ + t_}}}=1$ より $\\dfrac{{\\mathrm{{BP}}}}{{\\mathrm{{PE}}}}={fr(val.numerator, val.denominator)}$。"]
        ap = "求める比の線分 BE を辺にもつ三角形（$\\triangle\\mathrm{ABE}$）を選び、それを横切る直線 DC にメネラウスの定理を使う。"
        chk = f"Rational({q},{p})*Rational({s_ + t_},{t_})"
        alt = "ベクトル（数学C）や、点 E を通り AB に平行な補助線を引いて相似比で求めても、同じ比になる。"
    else:
        val = Fraction(t_ * (p + q), s_ * q)
        stem = (f"$\\triangle\\mathrm{{ABC}}$ の辺 $\\mathrm{{AB}}$ を ${p}:{q}$ に内分する点を $\\mathrm{{D}}$、辺 $\\mathrm{{AC}}$ を ${s_}:{t_}$ に内分する点を $\\mathrm{{E}}$ とし、"
                f"線分 $\\mathrm{{BE}}$ と $\\mathrm{{CD}}$ の交点を $\\mathrm{{P}}$ とする。$\\mathrm{{CP}}:\\mathrm{{PD}}$ を求めなさい。")
        target = "\\mathrm{CP}:\\mathrm{PD}"
        steps = ["線分 CD を辺にもつ $\\triangle\\mathrm{ACD}$ と、直線 EB にメネラウスの定理を使う。", "$\\dfrac{\\mathrm{AE}}{\\mathrm{EC}}\\cdot\\dfrac{\\mathrm{CP}}{\\mathrm{PD}}\\cdot\\dfrac{\\mathrm{DB}}{\\mathrm{BA}}=1$。",
                 f"$\\dfrac{{{s_}}}{{{t_}}}\\cdot\\dfrac{{\\mathrm{{CP}}}}{{\\mathrm{{PD}}}}\\cdot\\dfrac{{{q}}}{{{p + q}}}=1$ より $\\dfrac{{\\mathrm{{CP}}}}{{\\mathrm{{PD}}}}={fr(val.numerator, val.denominator)}$。"]
        ap = "求める比の線分 CD を辺にもつ三角形（$\\triangle\\mathrm{ACD}$）を選び、それを横切る直線 BE にメネラウスの定理を使う。"
        chk = f"Rational({t_},{s_})*Rational({p + q},{q})"
        alt = "点 D を通り AC に平行な補助線を引き、相似な三角形の比から求めても、同じ比になる。"
    ans = ratio(val.numerator, val.denominator)
    return sa(stem, f"${target}={ans}$", steps[-1], d=3, v=[ans],
              ap=ap, steps=steps + [f"よって ${target}={ans}$。"], alt=[alt],
              pc=[("適用する定理と三角形（直線）を正しく選んでいる", 2), ("比を正しく求めている", 2)],
              pit=["一周する順序を誤り、逆数の比を求めてしまう。", "$\\dfrac{\\mathrm{EC}}{\\mathrm{CA}}$ の CA を AE と取り違える（全体の長さを使う場面）。"],
              chk=(chk, fpy(val.numerator, val.denominator), None, "intermediate"))


# ======================================================================
# C 思考力・記述応用
# ======================================================================

@gen("thinking_writing", 3, ["written_reasoning", "concept"])
def lottery(r):
    n = r.randint(5, 15)
    a = r.randint(2, min(5, n - 2))
    first = r.choice(["A", "B"])
    return desc(f"{n} 本のくじの中に当たりくじが {a} 本ある。$\\mathrm{{A}}$ が先に1本引き、引いたくじを戻さずに続けて $\\mathrm{{B}}$ が1本引く。"
                f"(1) $\\mathrm{{B}}$ が当たる確率を求め、くじを引く順番によって当たりやすさが変わらないことを説明しなさい。"
                f"(2) $\\mathrm{{B}}$ が当たったとき、$\\mathrm{{A}}$ も当たっていた条件付き確率を求めなさい。",
                f"(1) ${fr(a, n)}$（$\\mathrm{{A}}$ が当たる確率 ${fr(a, n)}$ と等しい）　(2) ${fr(a - 1, n - 1)}$",
                "(1) A の結果で場合分けして乗法定理で求める。(2) $P_B(A)=\\dfrac{P(A\\cap B)}{P(B)}$。", d=4, p=8, lines=10,
                rubric=[("A の当たり・はずれで場合分けし、乗法定理で $P(B)$ を求めている", 3), ("$P(A)=P(B)$ であることを結論として述べている", 1),
                        ("$P(A\\cap B)$ を正しく求めている", 2), ("条件付き確率を正しく求めている", 2)],
                ap="B の結果は A の結果に左右されるので、A が「当たり」「はずれ」の2つの場合に分けて乗法定理を使う。(2) は「B が当たったとき」なので $P(B)$ が分母。",
                steps=[f"$P(A\\cap B)=\\dfrac{{{a}}}{{{n}}}\\cdot\\dfrac{{{a - 1}}}{{{n - 1}}}$、$P(\\overline{{A}}\\cap B)=\\dfrac{{{n - a}}}{{{n}}}\\cdot\\dfrac{{{a}}}{{{n - 1}}}$。",
                       f"$P(B)=\\dfrac{{{a}({a - 1})+{n - a}\\cdot{a}}}{{{n}\\cdot{n - 1}}}=\\dfrac{{{a}\\cdot{n - 1}}}{{{n}\\cdot{n - 1}}}={fr(a, n)}$。これは $P(A)={fr(a, n)}$ に等しい。",
                       f"$P_B(A)=\\dfrac{{P(A\\cap B)}}{{P(B)}}=\\dfrac{{{a * (a - 1)}}}{{{n * (n - 1)}}}\\div{fr(a, n)}={fr(a - 1, n - 1)}$。"],
                alt=[f"対称性による説明：{n} 本のくじを A, B, … の順に並べると考えれば、2番目の位置に当たりが来る確率は1番目と同じく ${fr(a, n)}$。(2) は「B の当たりくじ1本を除いた残り {n - 1} 本から A が引いた」と考えて ${fr(a - 1, n - 1)}$ と直接求めることもできる。"],
                pc=[("場合分けと乗法定理", 3), ("順番によらないことの結論", 1), ("$P(A\\cap B)$", 2), ("条件付き確率", 2)],
                pit=["A の結果を考えずに $P(B)=" + fr(a, n - 1) + "$ などとする。", "(2) で分母を $P(A)$ にして $P_A(B)$ を求めてしまう（結果は同じ値になるが、理由を説明できない）。"],
                chk=(f"[Rational({a},{n})*Rational({a - 1},{n - 1})+Rational({n - a},{n})*Rational({a},{n - 1}), Rational({a},{n})*Rational({a - 1},{n - 1})/Rational({a},{n})]",
                     f"[{fpy(a, n)}, {fpy(a - 1, n - 1)}]", None, "intermediate"))


@gen("thinking_writing", 3, ["cross_unit", "written_reasoning"], rel=["HS-MATH1-U04", "HS-MATHA-U02"])
def bisector_len(r):
    A = r.choice([60, 90, 120])
    b, c = r.sample(range(2, 10), 2)
    sA, sh = sp.sin(sp.pi * A / 180), sp.sin(sp.pi * A / 360)
    AD = sp.nsimplify(sp.radsimp(b * c * sA / ((b + c) * sh)))
    BC2 = b * b + c * c - 2 * b * c * sp.cos(sp.pi * A / 180)
    BC = sp.sqrt(sp.nsimplify(BC2))
    BD = sp.radsimp(BC * sp.Rational(c, b + c))
    return desc(f"$\\triangle\\mathrm{{ABC}}$ において $\\mathrm{{AB}}={c},\\ \\mathrm{{AC}}={b},\\ \\angle\\mathrm{{A}}={A}^\\circ$ とする。$\\angle\\mathrm{{A}}$ の二等分線と辺 $\\mathrm{{BC}}$ の交点を $\\mathrm{{D}}$ とするとき、線分 $\\mathrm{{BD}}$ と $\\mathrm{{AD}}$ の長さを求めなさい。求め方も説明すること。",
                f"$\\mathrm{{BD}}={L(BD)}$、$\\mathrm{{AD}}={L(AD)}$",
                f"余弦定理で BC、角の二等分線の性質で BD、面積の分割で AD を求める。", d=4, p=8, lines=12,
                rubric=[("余弦定理で BC を求めている", 2), ("角の二等分線の性質 BD:DC=AB:AC を用いて BD を求めている", 2),
                        ("$\\triangle\\mathrm{ABC}=\\triangle\\mathrm{ABD}+\\triangle\\mathrm{ADC}$ の面積の関係から AD の方程式を立てている", 3), ("AD を正しく求めている", 1)],
                ap="角の二等分線は「辺の比」（図形の性質）と「面積の分割」（三角比の面積公式）の両方で使える。BD は比で、AD は面積で求める。",
                steps=[f"余弦定理：$\\mathrm{{BC}}^2={c}^2+{b}^2-2\\cdot{c}\\cdot{b}\\cos{A}^\\circ={L(BC2)}$、$\\mathrm{{BC}}={L(BC)}$。",
                       f"$\\mathrm{{BD}}:\\mathrm{{DC}}=\\mathrm{{AB}}:\\mathrm{{AC}}={c}:{b}$ より $\\mathrm{{BD}}={L(BC)}\\times\\dfrac{{{c}}}{{{b + c}}}={L(BD)}$。",
                       f"面積：$\\dfrac{{1}}{{2}}\\cdot{c}\\cdot{b}\\sin{A}^\\circ=\\dfrac{{1}}{{2}}\\cdot{c}\\cdot\\mathrm{{AD}}\\sin{A // 2}^\\circ+\\dfrac{{1}}{{2}}\\cdot{b}\\cdot\\mathrm{{AD}}\\sin{A // 2}^\\circ$。",
                       f"$\\mathrm{{AD}}=\\dfrac{{{b * c}\\sin{A}^\\circ}}{{{b + c}\\sin{A // 2}^\\circ}}={L(AD)}$。"],
                alt=[f"検算：$\\triangle\\mathrm{{ABD}}$ で余弦定理 $\\mathrm{{BD}}^2=\\mathrm{{AB}}^2+\\mathrm{{AD}}^2-2\\,\\mathrm{{AB}}\\cdot\\mathrm{{AD}}\\cos{A // 2}^\\circ$ に求めた値を代入すると、両辺が一致することを確かめられる。"],
                pc=[("BC の計算", 2), ("BD の計算", 2), ("面積による立式", 3), ("AD の値", 1)],
                pit=["BD:DC を AC:AB と逆にしてしまう。", f"面積の式で $\\sin{A // 2}^\\circ$ ではなく $\\sin{A}^\\circ$ を使ってしまう。"],
                chk=(f"[sqrt({c}**2+{b}**2-2*{c}*{b}*cos(deg({A})))*Rational({c},{b + c}), {b * c}*sin(deg({A}))/({b + c}*sin(deg({A}/2)))]", f"[{BD}, {AD}]", None, "intermediate"))


@gen("thinking_writing", 2, ["cross_unit", "written_reasoning"], rel=["HS-MATH1-U05", "HS-MATHA-U01"])
def coin_test(r):
    n, k = r.choice([(8, 7), (8, 6), (10, 9), (10, 8), (10, 7), (12, 10), (12, 9), (9, 8), (9, 7), (11, 9), (11, 8), (12, 11), (7, 6)])
    tot = sum(comb(n, i) for i in range(k, n + 1))
    P = Fraction(tot, 2 ** n)
    sig = P < Fraction(5, 100)
    approx = f"{float(P):.3f}"
    concl = ("$0.05$ より小さいので、仮説「表と裏の出やすさは同じ」は誤りと判断する。すなわち、このコインは表が出やすいと判断してよい" if sig
             else "$0.05$ より大きいので、仮説「表と裏の出やすさは同じ」は誤りとはいえない。すなわち、このコインは表が出やすいとは判断できない")
    terms = "+".join(f"{{}}_{{{n}}}\\mathrm{{C}}_{{{i}}}" for i in range(k, n + 1))
    return desc(f"あるコインを {n} 回投げたところ、表が {k} 回出た。このコインは表が出やすいといえるかを、有意水準 $5\\%$ で考える。"
                f"「表と裏の出やすさは同じ（表が出る確率は $\\dfrac{{1}}{{2}}$）」という仮説を立てるとき、この仮説のもとで表が {k} 回以上出る確率を求め、どのように判断できるかを説明しなさい。",
                f"確率は ${fr(P.numerator, P.denominator)}\\fallingdotseq{approx}$。{concl}。",
                f"反復試行の確率：$\\dfrac{{{terms}}}{{2^{{{n}}}}}=\\dfrac{{{tot}}}{{{2 ** n}}}$。", d=4, p=8, lines=10,
                rubric=[("仮説のもとでの確率を反復試行で正しく立式している", 3), ("確率を正しく計算している", 2),
                        ("有意水準 $0.05$ と比較している", 1), ("比較の結果から適切に結論を述べている", 2)],
                ap="仮説検定の考え方：仮説が正しいとしたとき、実際に起きたこと（またはそれ以上に極端なこと）が起こる確率を計算する。その確率が有意水準より小さければ「めったに起こらないことが起きた」と考え、仮説を誤りと判断する。",
                steps=[f"表が $i$ 回出る確率は ${{}}_{{{n}}}\\mathrm{{C}}_i\\left(\\dfrac{{1}}{{2}}\\right)^{{{n}}}$。",
                       f"{k} 回以上：$\\dfrac{{{terms}}}{{{2 ** n}}}=\\dfrac{{{tot}}}{{{2 ** n}}}={fr(P.numerator, P.denominator)}\\fallingdotseq{approx}$。",
                       f"{concl}。"],
                alt=["コインを投げる実験をくり返すシミュレーション（表計算ソフトの乱数など）で、表が" + str(k) + "回以上出る相対度数を調べても、およその確率を確かめられる。"],
                pc=[("反復試行の立式", 3), ("確率の計算", 2), ("有意水準との比較", 1), ("結論", 2)],
                pit=["「ちょうど" + str(k) + "回」の確率だけを計算し、それより極端な場合を足し忘れる。", "仮説が否定できないことを「仮説が正しいと証明された」と述べてしまう。"],
                chk=(f"({'+'.join(f'binomial({n},{i})' for i in range(k, n + 1))})/2**{n}", fpy(P.numerator, P.denominator), None, "intermediate"))


@gen("thinking_writing", 2, ["written_reasoning", "computation"])
def add_mean_point(r):
    n = r.choice([4, 9, 14, 19, 24, 29])
    u, w = r.randint(2, 9), r.randint(2, 9)
    vx, vy = (n + 1) * u, (n + 1) * w
    c0 = r.choice([-1, 1]) * r.randint(1, int(sp.sqrt(u * w - 1)))
    cov = (n + 1) * c0
    rv = sp.nsimplify(sp.Rational(cov) / sp.sqrt(vx * vy))
    return desc(f"2つの変量 $x,\\ y$ の {n} 個のデータ（架空のデータ）について、$x$ の分散は ${vx}$、$y$ の分散は ${vy}$、共分散は ${cov}$ である。"
                f"このデータに、$x$ の値が $x$ の平均値と等しく、$y$ の値が $y$ の平均値と等しい1組のデータを加えて {n + 1} 個のデータとする。"
                f"加えた後の $x$ の分散、共分散、相関係数をそれぞれ求め、相関係数が変化するかどうかを理由とともに説明しなさい。",
                f"$x$ の分散 ${n * u}$、共分散 ${n * cov // (n + 1)}$、相関係数は変わらず ${L(rv)}$",
                "平均値は変わらず、加えたデータの偏差は $0$ なので、偏差の2乗の和・偏差の積の和は変わらない。個数だけが $" + str(n) + "\\to" + str(n + 1) + "$ になる。", d=4, p=8, lines=10,
                rubric=[("平均値が変わらず、加えたデータの偏差が $0$ であることを述べている", 2), ("分散と共分散がそれぞれ $\\dfrac{" + str(n) + "}{" + str(n + 1) + "}$ 倍になることを示し、値を求めている", 3),
                        ("相関係数を計算し、分子・分母で倍率が打ち消し合うことを説明している", 3)],
                ap="平均値と等しい値を加えても平均値は変わらない。分散・共分散は「偏差の2乗の和（偏差の積の和）÷個数」なので、和は変わらず個数だけが増える。",
                steps=[f"加えたデータの偏差は $x,\\ y$ ともに $0$。平均値は変わらない。",
                       f"偏差の2乗の和は ${n}\\times{vx}={n * vx}$ のまま。新しい分散は $\\dfrac{{{n * vx}}}{{{n + 1}}}={n * u}$。",
                       f"偏差の積の和は ${n}\\times({cov})={n * cov}$ のまま。新しい共分散は $\\dfrac{{{n * cov}}}{{{n + 1}}}={n * cov // (n + 1)}$。",
                       f"相関係数 $\\dfrac{{{n * cov // (n + 1)}}}{{\\sqrt{{{n * u}}}\\sqrt{{{n * w}}}}}={L(rv)}$。分子・分母がともに $\\dfrac{{{n}}}{{{n + 1}}}$ 倍されるので変わらない。"],
                alt=["定義式 $r=\\dfrac{\\sum(x_i-\\overline{x})(y_i-\\overline{y})}{\\sqrt{\\sum(x_i-\\overline{x})^2}\\sqrt{\\sum(y_i-\\overline{y})^2}}$ で考えると、個数 $n$ が式に現れないので、偏差 $0$ のデータを加えても $r$ は変わらないことが直接分かる。"],
                pc=[("偏差が0であることの指摘", 2), ("分散・共分散の値", 3), ("相関係数の説明", 3)],
                pit=["分散も平均と同じく変わらないと考える。", "散布図の点が増えたので相関が強くなると直感で判断する。"],
                chk=(f"[Rational({n * vx},{n + 1}), Rational({n * cov},{n + 1}), Rational({cov},1)/sqrt({vx}*{vy})]", f"[{n * u}, {n * cov // (n + 1)}, {rv}]", None, "intermediate"))


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(stem, wrong, step, etype, tempt, fix, ans, expl, steps, ap, alt, pit, chk=None, d=3, tbl=None):
    kw = {"tbl": tbl} if tbl else {}
    return desc(f"{stem}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい答えを求めなさい。", ans, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい解答を途中式とともに示している", 3), ("最終的な答えが正しい", 1)], d=d, p=6, lines=6,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい途中式", 3), ("正しい答え", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix), chk=chk, **kw)


@gen("error_correction", 3, ["common_error", "concept"])
def err_cond(r):
    rn, rows, cn, cols = r.choice(TABLE_CTX)
    t = [[r.randint(8, 40) for _ in range(2)] for _ in range(2)]
    i, j = r.randint(0, 1), r.randint(0, 1)
    N = sum(map(sum, t))
    den = sum(t[i])
    nm = t[i][j]
    tb = table([[rows[0], t[0][0], t[0][1], sum(t[0])], [rows[1], t[1][0], t[1][1], sum(t[1])],
                ["計", t[0][0] + t[1][0], t[0][1] + t[1][1], N]], header=[f"{rn}＼{cn}", cols[0], cols[1], "計"], caption="架空の調査結果（人）")
    wrong = f"{rn}が「{rows[i]}」で{cn}が「{cols[j]}」の生徒は {nm} 人なので、求める確率は $\\dfrac{{{nm}}}{{{N}}}{'=' + fr(nm, N) if Fraction(nm, N).denominator != N else ''}$"
    return err_item(f"下の表は、ある高校の生徒 {N} 人について{rn}と{cn}を調べた結果である（架空のデータ）。1人を選んだところ、{rn}が「{rows[i]}」であった。この生徒の{cn}が「{cols[j]}」である確率を求めなさい。",
                    wrong, "分母を全体の人数にしたところ", "concept",
                    "「〜であった」という条件が文の前半にあると、それが分母を変える条件だと気づきにくい。表の交わるマスの人数を全体で割る計算は、同時確率 $P(A\\cap B)$ になってしまう。",
                    f"条件「{rows[i]}」の生徒 {den} 人の中での割合なので、$\\dfrac{{{nm}}}{{{den}}}={fr(nm, den)}$",
                    f"${fr(nm, den)}$", f"条件付き確率 $P_A(B)=\\dfrac{{n(A\\cap B)}}{{n(A)}}$。分母は {rows[i]}の人数 {den}。",
                    [f"条件の事象 $A$：{rn}が「{rows[i]}」→ {den} 人。", f"$A\\cap B$：さらに{cn}が「{cols[j]}」→ {nm} 人。", f"$P_A(B)=\\dfrac{{{nm}}}{{{den}}}={fr(nm, den)}$。"],
                    "「〜であった」「〜のとき」に下線を引き、その事象を分母にする。",
                    [f"確率の式で確かめる：$P(A\\cap B)=\\dfrac{{{nm}}}{{{N}}}$、$P(A)=\\dfrac{{{den}}}{{{N}}}$ より $P_A(B)=\\dfrac{{{nm}}}{{{den}}}$。生徒の答えは $P(A\\cap B)$ を求めたことになる。"],
                    ["条件付き確率と同時確率を混同する。"],
                    chk=(f"Rational({nm},{den})", fpy(nm, den), None, "intermediate"), d=2, tbl=tb)


@gen("error_correction", 3, ["common_error", "condition_check"])
def err_circle(r):
    n = r.randint(5, 9)
    correct = factorial(n - 1) - 2 * factorial(n - 2)
    wrong_v = factorial(n) - 2 * factorial(n - 1)
    wrong = f"全員の並び方は ${n}!={factorial(n)}$ 通り。A と B が隣り合う並び方は、2人をまとめて $2\\times{n - 1}!={2 * factorial(n - 1)}$ 通り。よって隣り合わない並び方は ${factorial(n)}-{2 * factorial(n - 1)}={wrong_v}$ 通り"
    return err_item(f"$\\mathrm{{A}},\\ \\mathrm{{B}}$ を含む {n} 人が、円形のテーブルのまわりに等間隔に座る。$\\mathrm{{A}}$ と $\\mathrm{{B}}$ が隣り合わない座り方は何通りあるか。ただし、回転して一致する座り方は同じものとみなす。",
                    wrong, "全体の数え方（1列に並べる順列で数えたところ）", "formula",
                    "「隣り合わない＝全体－隣り合う」という方針は正しいため、全体と隣り合う場合の両方を、無意識に1列の順列 $n!$ の考え方で数えてしまう。",
                    f"全体は円順列で $({n}-1)!={factorial(n - 1)}$ 通り、隣り合うのは $2\\times({n - 1}-1)!={2 * factorial(n - 2)}$ 通り。隣り合わないのは ${correct}$ 通り",
                    f"${correct}$ 通り", "回転して一致するものを同じとみなすので、円順列 $(n-1)!$ で数える。",
                    [f"全体：$({n}-1)!={factorial(n - 1)}$ 通り。", f"隣り合う：A, B をまとめて ${n - 1}$ 個の円順列 $({n - 1}-1)!={factorial(n - 2)}$、まとまりの中で $2$ 通り → ${2 * factorial(n - 2)}$ 通り。",
                     f"隣り合わない：${factorial(n - 1)}-{2 * factorial(n - 2)}={correct}$ 通り。"],
                    "円順列では、1人の席を固定して残りを並べると考えれば、1列の順列との違いがはっきりする。",
                    [f"A の席を固定する方法：B は A の両隣以外の ${n - 3}$ 席から選び、残り ${n - 2}$ 人は ${n - 2}!$ 通り。${n - 3}\\times{factorial(n - 2)}={correct}$ 通りで一致する。生徒の答え ${wrong_v}$ は、これのちょうど ${n}$ 倍（回転の分だけ重複）になっている。"],
                    ["回転を同一視する条件を読み落とし、$n!$ で数える。"],
                    chk=(f"factorial({n - 1})-2*factorial({n - 2})", str(correct), None, "intermediate"))


@gen("error_correction", 2, ["common_error", "computation"])
def err_quartile(r):
    while True:
        n = r.choice([9, 11, 13])
        xs = sorted(r.sample(range(20, 90), n))
        q1, md, q3 = quartiles(xs)
        h = n // 2
        wq1, wq3 = median(xs[: h + 1]), median(xs[h:])
        if wq1 != q1 and wq3 != q3:
            break
    kind = r.choice(["q1", "q3"])
    name = "第1四分位数" if kind == "q1" else "第3四分位数"
    part = xs[: h + 1] if kind == "q1" else xs[h:]
    wv = wq1 if kind == "q1" else wq3
    cv = q1 if kind == "q1" else q3
    right_part = xs[:h] if kind == "q1" else xs[h + 1:]
    wrong = f"中央値は ${fnum(md)}$。{'前半' if kind == 'q1' else '後半'}は {'，'.join(map(str, part))} の {len(part)} 個なので、{name}は ${fnum(wv)}$"
    return err_item(f"次の {n} 個のデータ（架空）の{name}を求めなさい。{'，'.join(map(str, xs))}", wrong, f"{'前半' if kind == 'q1' else '後半'}のデータに中央値を含めたところ", "concept",
                    "データの個数が奇数のとき、中央値をどちらに入れるかの約束を覚えていないと、半分ずつに分けようとして中央値を含めてしまう。",
                    f"中央値 ${fnum(md)}$ を除いた{'前半' if kind == 'q1' else '後半'} {len(right_part)} 個（{'，'.join(map(str, right_part))}）の中央値で ${fnum(cv)}$",
                    f"${fnum(cv)}$", "データの個数が奇数のとき、中央値は前半・後半のどちらにも含めない。",
                    [f"{n} 個の中央値は {h + 1} 番目の ${fnum(md)}$。", f"{'前半' if kind == 'q1' else '後半'}は中央値を除いた {h} 個：{'，'.join(map(str, right_part))}。", f"その中央値は ${fnum(cv)}$。"],
                    "四分位数を求める前に、前半・後半それぞれのデータの個数（ここでは " + str(h) + " 個ずつ）を書き出して確かめる。",
                    [f"前半と後半の個数が等しく {h} 個ずつになっているかを確認すれば、中央値を含めた誤りに気づける（生徒の解答では {len(part)} 個と {h} 個で個数がそろわない）。"],
                    ["中央値を前半・後半の両方に含めてしまう。"],
                    chk=(f"quartiles([{', '.join(map(str, xs))}])[{0 if kind == 'q1' else 2}]", fnum(cv), None, "intermediate"))


@gen("error_correction", 2, ["common_error", "computation"])
def err_power(r):
    kind = r.choice(["secant", "tangent"])
    if kind == "secant":
        for _ in range(500):
            a, b, c = r.randint(2, 8), r.randint(2, 12), r.randint(2, 9)
            if c != a and (a * (a + b)) % c == 0:
                x = a * (a + b) // c - c
                wx = Fraction(a * b, c)
                if x > 0 and wx != x:
                    break
        wrong = f"$\\mathrm{{PA}}\\cdot\\mathrm{{AB}}=\\mathrm{{PC}}\\cdot\\mathrm{{CD}}$ より ${a}\\cdot{b}={c}\\cdot\\mathrm{{CD}}$、$\\mathrm{{CD}}={fr(wx.numerator, wx.denominator)}$"
        return err_item(f"円の外部の点 $\\mathrm{{P}}$ を通る2本の直線が、円とそれぞれ2点 $\\mathrm{{A,\\ B}}$、$\\mathrm{{C,\\ D}}$ で交わっている（$\\mathrm{{P}}$ に近い方が $\\mathrm{{A}}$、$\\mathrm{{C}}$）。$\\mathrm{{PA}}={a},\\ \\mathrm{{AB}}={b},\\ \\mathrm{{PC}}={c}$ のとき、$\\mathrm{{CD}}$ の長さを求めなさい。",
                        wrong, "方べきの定理の式を立てたところ", "formula",
                        "円の内部で2弦が交わる場合の「交点で分けられた2つの部分の積」の形を、外部の点の場合にもそのまま当てはめてしまう。",
                        f"$\\mathrm{{PA}}\\cdot\\mathrm{{PB}}=\\mathrm{{PC}}\\cdot\\mathrm{{PD}}$ より ${a}\\cdot{a + b}={c}({c}+\\mathrm{{CD}})$、$\\mathrm{{CD}}={x}$",
                        f"$\\mathrm{{CD}}={x}$", "方べきの定理は「点 P から円との2つの交点までの距離の積」が一定。",
                        [f"$\\mathrm{{PB}}=\\mathrm{{PA}}+\\mathrm{{AB}}={a + b}$。", f"$\\mathrm{{PA}}\\cdot\\mathrm{{PB}}={a}\\cdot{a + b}={a * (a + b)}$。",
                         f"${c}({c}+\\mathrm{{CD}})={a * (a + b)}$ より $\\mathrm{{CD}}={x}$。"],
                        "方べきの定理の両辺は、どちらも「点 P を端点とする線分」の積になっていることを確認する。",
                        [f"$\\triangle\\mathrm{{PAC}}\\sim\\triangle\\mathrm{{PDB}}$（円に内接する四角形 ABDC の性質から角が等しい）より $\\mathrm{{PA}}:\\mathrm{{PD}}=\\mathrm{{PC}}:\\mathrm{{PB}}$。これを変形しても同じ式になる。"],
                        ["P を端点としない線分（AB, CD）を式に使う。"],
                        chk=(f"Rational({a * (a + b)},{c})-{c}", str(x), None, "intermediate"))
    for _ in range(500):
        a, b = r.randint(1, 9), r.randint(2, 15)
        t2 = a * (a + b)
        tt = sp.sqrt(t2)
        wt = sp.sqrt(a * b)
        if tt != wt:
            break
    wrong = f"$\\mathrm{{PT}}^2=\\mathrm{{PA}}\\cdot\\mathrm{{AB}}={a}\\cdot{b}={a * b}$ より $\\mathrm{{PT}}={L(wt)}$"
    return err_item(f"円の外部の点 $\\mathrm{{P}}$ から円に接線を引き、接点を $\\mathrm{{T}}$ とする。また、$\\mathrm{{P}}$ を通る直線が円と2点 $\\mathrm{{A,\\ B}}$ で交わり（$\\mathrm{{P}}$ に近い方が $\\mathrm{{A}}$）、$\\mathrm{{PA}}={a},\\ \\mathrm{{AB}}={b}$ である。$\\mathrm{{PT}}$ の長さを求めなさい。",
                    wrong, "方べきの定理の式を立てたところ（AB を使った部分）", "formula",
                    "「外側の部分×中の部分」と覚えていると、PB（P から遠い交点まで）ではなく AB（弦の長さ）を使ってしまう。",
                    f"$\\mathrm{{PT}}^2=\\mathrm{{PA}}\\cdot\\mathrm{{PB}}={a}\\cdot{a + b}={t2}$ より $\\mathrm{{PT}}={L(tt)}$",
                    f"$\\mathrm{{PT}}={L(tt)}$", "接線の場合の方べきの定理：$\\mathrm{PT}^2=\\mathrm{PA}\\cdot\\mathrm{PB}$。",
                    [f"$\\mathrm{{PB}}={a}+{b}={a + b}$。", f"$\\mathrm{{PT}}^2={a}\\times{a + b}={t2}$。", f"$\\mathrm{{PT}}>0$ より $\\mathrm{{PT}}={L(tt)}$。"],
                    "方べきの定理に出てくる線分は、すべて点 P を端点とする。",
                    ["接弦定理から $\\triangle\\mathrm{PTA}\\sim\\triangle\\mathrm{PBT}$ が分かり、$\\mathrm{PT}:\\mathrm{PA}=\\mathrm{PB}:\\mathrm{PT}$ から同じ式が導ける。"],
                    ["弦 AB の長さを PB の代わりに使う。"],
                    chk=(f"sqrt({a}*({a}+{b}))", str(tt), None, "intermediate"))


GENERATORS = [quartile_calc, lin_transform, cond_table, count_basic,
              corr_summary, bayes_test, boxplot_mc, ratio_theorems,
              lottery, bisector_len, coin_test, add_mean_point,
              err_cond, err_circle, err_quartile, err_power]
