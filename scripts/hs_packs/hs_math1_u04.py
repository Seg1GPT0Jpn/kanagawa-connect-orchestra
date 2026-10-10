"""単元パック：数学Ⅰ 図形と計量（三角比）。"""
import sympy as sp

from banks._common import desc, figure, mc, plane, sa, shape
from hs_pack_lib import board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem, tp

UNIT_ID = "HS-MATH1-U04"

# 角度 → (sin, cos, tan) の厳密値
ANG = [0, 30, 45, 60, 90, 120, 135, 150, 180]


def tex(v):
    return sp.latex(sp.nsimplify(v))


def trig(fn, deg):
    f = {"sin": sp.sin, "cos": sp.cos, "tan": sp.tan}[fn]
    return sp.nsimplify(f(sp.pi * deg / 180))


def pyexpr(v):
    return str(sp.nsimplify(v))


LESSON = lesson(
    goals=["座標を用いて $0^\\circ\\leqq\\theta\\leqq180^\\circ$ の三角比を定義し、相互関係・$180^\\circ-\\theta$ の公式を説明できる。",
           "正弦定理・余弦定理を証明し、与えられた条件に応じて使い分けて三角形を解ける。",
           "三角形の面積を $\\dfrac{1}{2}bc\\sin A$ で求め、他の単元（二次関数など）と組み合わせて活用できる。"],
    duration=150,
    readiness=["三平方の定理と特別な直角三角形の辺の比（$1:1:\\sqrt{2}$、$1:2:\\sqrt{3}$）を使える。", "相似の考え方と円周角の定理を使える。"],
    flow=[("導入：測れない高さを測る", 10, "木の高さを影の長さと角度から求める場面で、三角比の必要性を示す"),
          ("鋭角の三角比", 20, "直角三角形での定義、特別な角の値の表をつくる"),
          ("鈍角への拡張と相互関係", 30, "単位円（半径1の半円）で定義を拡張し、相互関係・180°−θ の公式を導く"),
          ("正弦定理", 25, "外接円を使って証明し、例題で使い方を確認"),
          ("余弦定理", 30, "座標を使って証明し、辺・角を求める例題"),
          ("面積と活用", 25, "S=½bc sinA の導出、二次関数との融合問題を紹介"),
          ("まとめ", 10, "使い分けの表を板書し、問題プリントの課題を指示")],
    sections=[
        intro("in1", "三角比は「角」と「長さ」をつなぐ道具",
              "直角三角形では、1つの鋭角が決まると辺の長さの比が決まる（相似）。この比に名前をつけたものが三角比である。三角比を使うと、直接測れない長さや角を計算で求められる。",
              bullets=["測量・建築・物理（力の分解）など多くの場面で使われる。", "後に学ぶ三角関数（数学Ⅱ）・ベクトルの内積（数学C）の土台になる。"],
              points=[tp("相似な直角三角形をいくつか示し、「角が同じなら比は同じ」ことを実測で確かめさせる。", ask="大きさの違う2つの直角三角形で、（高さ）÷（斜辺）を比べるとどうなるか。", expect="ほぼ同じ値になる。")]),
        definition("df1", "三角比の定義（$0^\\circ\\leqq\\theta\\leqq180^\\circ$）",
                   "原点 O を中心とする半径 $r$ の円の上半分に点 P$(x,\\,y)$ をとり、$x$ 軸の正の向きと OP のなす角を $\\theta$ とする。",
                   formula="$$\\sin\\theta=\\dfrac{y}{r},\\qquad \\cos\\theta=\\dfrac{x}{r},\\qquad \\tan\\theta=\\dfrac{y}{x}\\ (x\\neq0)$$",
                   conditions=["$\\theta=90^\\circ$ のとき $x=0$ なので $\\tan90^\\circ$ は定義されない。", "$r=1$（単位円）にとると $\\sin\\theta=y,\\ \\cos\\theta=x$ となり、座標そのものになる。",
                               "鈍角では $x<0$ なので $\\cos\\theta<0,\\ \\tan\\theta<0$。"],
                   figure=figure("単位円の上半分と点P(cosθ, sinθ)", plane((-1.3, 1.3), (-0.3, 1.3), unit=70, grid=False, ticks=False,
                                                                      curves=[(lambda x: (1 - x * x) ** 0.5 if abs(x) <= 1 else float("nan"), "")],
                                                                      points=[(-0.5, 0.866, "P(cosθ, sinθ)")], segments=[((0, 0), (-0.5, 0.866)), ((-0.5, 0), (-0.5, 0.866))])),
                   points=[tp("直角三角形による定義と座標による定義が、鋭角では一致することを図で確認させる。"),
                           tp("鈍角の $\\cos$ が負になることを「点 P が $y$ 軸の左にある」ことと結びつける。", caution="「長さだから正」と考えて符号を落とす誤りが多い。")]),
        theorem("th1", "三角比の相互関係",
                "$$\\sin^2\\theta+\\cos^2\\theta=1,\\qquad \\tan\\theta=\\dfrac{\\sin\\theta}{\\cos\\theta},\\qquad 1+\\tan^2\\theta=\\dfrac{1}{\\cos^2\\theta}$$",
                ["$\\tan$ を含む式は $\\theta\\neq90^\\circ$ のとき", "$\\sin\\theta$ から $\\cos\\theta$ を求めるときは、$\\theta$ が鋭角か鈍角かで符号が決まる"],
                proof=["単位円上の点 P$(\\cos\\theta,\\,\\sin\\theta)$ は $x^2+y^2=1$ を満たすので $\\cos^2\\theta+\\sin^2\\theta=1$。",
                       "定義より $\\tan\\theta=\\dfrac{y}{x}=\\dfrac{\\sin\\theta}{\\cos\\theta}$。",
                       "第1式の両辺を $\\cos^2\\theta\\ (\\neq0)$ で割ると $\\tan^2\\theta+1=\\dfrac{1}{\\cos^2\\theta}$。"],
                points=[tp("3つの式は暗記ではなく「単位円の方程式」から1行で導けることを強調する。")]),
        derivation("dv1", "$180^\\circ-\\theta$ の三角比",
                   ["点 P$(\\cos\\theta,\\,\\sin\\theta)$ と $y$ 軸に関して対称な点は Q$(-\\cos\\theta,\\,\\sin\\theta)$。",
                    "OQ と $x$ 軸の正の向きのなす角は $180^\\circ-\\theta$。", "よって $\\sin(180^\\circ-\\theta)=\\sin\\theta,\\ \\cos(180^\\circ-\\theta)=-\\cos\\theta,\\ \\tan(180^\\circ-\\theta)=-\\tan\\theta$。"],
                   body="鈍角の三角比は、この公式で鋭角の三角比に直して求める。",
                   points=[tp("$\\sin$ だけ符号が変わらない理由を、点の $y$ 座標が変わらないことで説明する。")]),
        theorem("th2", "正弦定理",
                "$$\\dfrac{a}{\\sin A}=\\dfrac{b}{\\sin B}=\\dfrac{c}{\\sin C}=2R\\qquad(R\\text{ は外接円の半径})$$",
                ["1辺とその両端の角（または対角）が分かるとき、ほかの辺を求めるのに使う", "$\\sin B$ から $B$ を求めるときは、鋭角・鈍角の2通りがありうる"],
                proof=["$A$ が鋭角のとき：外接円の直径 BD を引くと、円周角の定理より $\\angle\\mathrm{BDC}=A$、$\\angle\\mathrm{BCD}=90^\\circ$。",
                       "直角三角形 BCD で $\\sin A=\\dfrac{a}{2R}$、よって $\\dfrac{a}{\\sin A}=2R$。",
                       "$A$ が鈍角のときは円に内接する四角形の性質から $\\angle\\mathrm{BDC}=180^\\circ-A$ となり、$\\sin(180^\\circ-A)=\\sin A$ より同じ式が成り立つ（直角のときは $a=2R$）。",
                       "B・C についても同様なので定理が成り立つ。"],
                figure=figure("外接円と直径BD", shape({"A": (-1.2, 1.6), "B": (-1.73, -1), "C": (1.73, -1), "D": (1.73, 1), "O": (0, 0)},
                                                       segments=[("A", "B"), ("B", "C"), ("C", "A"), ("B", "D"), ("D", "C")], circle=((0, 0), 2), scale=28)),
                points=[tp("証明の要点は「直径に対する円周角は直角」。中学の円周角の定理を想起させる。", ask="直径 BD を引くと、どの角が直角になるか。")]),
        theorem("th3", "余弦定理",
                "$$a^2=b^2+c^2-2bc\\cos A,\\qquad \\cos A=\\dfrac{b^2+c^2-a^2}{2bc}$$",
                ["2辺とその間の角から残りの辺を求めるとき", "3辺から角を求めるとき", "$A=90^\\circ$ のとき三平方の定理になる"],
                proof=["A を原点、AB を $x$ 軸上にとり、B$(c,\\,0)$、C$(b\\cos A,\\,b\\sin A)$ とする。",
                       "$a^2=\\mathrm{BC}^2=(b\\cos A-c)^2+(b\\sin A)^2=b^2(\\cos^2A+\\sin^2A)-2bc\\cos A+c^2$。",
                       "$\\cos^2A+\\sin^2A=1$ より $a^2=b^2+c^2-2bc\\cos A$。$A$ が鈍角でも同じ計算が成り立つ。"],
                points=[tp("三平方の定理の「補正項」が $-2bc\\cos A$ であり、$A$ が鈍角なら $\\cos A<0$ で $a^2$ が大きくなることを図で確認させる。")]),
        theorem("th4", "三角形の面積",
                "$$S=\\dfrac{1}{2}bc\\sin A=\\dfrac{1}{2}ca\\sin B=\\dfrac{1}{2}ab\\sin C$$",
                ["2辺とその間の角が分かるとき", "$\\sin$ を使う（$\\cos$ ではない）"],
                proof=["辺 AB を底辺とすると、高さは C から直線 AB に下ろした垂線の長さ $h=b\\sin A$（鈍角でも $\\sin(180^\\circ-A)=\\sin A$ より同じ）。", "$S=\\dfrac{1}{2}ch=\\dfrac{1}{2}bc\\sin A$。"],
                points=[tp("「高さ ＝ 斜辺 × sin」という見方を、図に高さを書き込ませて定着させる。")]),
        example("ex1", "例題1　正弦定理",
                "$\\triangle\\mathrm{ABC}$ で $a=6,\\ A=45^\\circ,\\ B=60^\\circ$ のとき、$b$ と外接円の半径 $R$ を求めよ。",
                ["正弦定理 $\\dfrac{a}{\\sin A}=\\dfrac{b}{\\sin B}$ より $b=\\dfrac{6\\sin60^\\circ}{\\sin45^\\circ}=\\dfrac{6\\cdot\\frac{\\sqrt3}{2}}{\\frac{\\sqrt2}{2}}=3\\sqrt6$。",
                 "$2R=\\dfrac{a}{\\sin A}=\\dfrac{6}{\\frac{\\sqrt2}{2}}=6\\sqrt2$ より $R=3\\sqrt2$。"],
                "$b=3\\sqrt6,\\ R=3\\sqrt2$", thinking="1辺と2角が分かっている → 正弦定理。",
                points=[tp("分数の中の分数の処理を丁寧に板書する。")]),
        example("ex2", "例題2　余弦定理で角を求める",
                "$\\triangle\\mathrm{ABC}$ で $a=7,\\ b=5,\\ c=3$ のとき、$A$ を求めよ。",
                ["$\\cos A=\\dfrac{b^2+c^2-a^2}{2bc}=\\dfrac{25+9-49}{30}=-\\dfrac{1}{2}$。", "$0^\\circ<A<180^\\circ$ より $A=120^\\circ$。"],
                "$A=120^\\circ$", thinking="3辺が分かっている → 余弦定理の変形 $\\cos A=\\dfrac{b^2+c^2-a^2}{2bc}$。",
                misconceptions=[("$\\cos A=-\\dfrac12$ だから $A=60^\\circ$", "$\\cos$ が負なら鈍角。$A=120^\\circ$")]),
        example("ex3", "例題3　面積",
                "$\\triangle\\mathrm{ABC}$ で $b=4,\\ c=5,\\ A=120^\\circ$ のとき、面積 $S$ を求めよ。",
                ["$S=\\dfrac12bc\\sin A=\\dfrac12\\cdot4\\cdot5\\cdot\\sin120^\\circ$。", "$\\sin120^\\circ=\\sin60^\\circ=\\dfrac{\\sqrt3}{2}$ より $S=5\\sqrt3$。"], "$5\\sqrt3$"),
        board("bd1", "板書案",
              [("① 定義と相互関係", ["単位円 P$(\\cos\\theta,\\sin\\theta)$", "$\\sin^2\\theta+\\cos^2\\theta=1$", "$\\tan\\theta=\\dfrac{\\sin\\theta}{\\cos\\theta}$", "$\\sin(180^\\circ-\\theta)=\\sin\\theta$", "$\\cos(180^\\circ-\\theta)=-\\cos\\theta$"]),
               ("② 正弦定理・余弦定理", ["$\\dfrac{a}{\\sin A}=2R$", "$a^2=b^2+c^2-2bc\\cos A$", "使い分け：", "1辺＋2角 → 正弦", "2辺＋間の角／3辺 → 余弦"]),
               ("③ 面積と活用", ["$S=\\dfrac12bc\\sin A$", "例 $b=4,c=5,A=120^\\circ$", "$S=5\\sqrt3$", "最大・最小 → 二次関数へ"])]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("$\\sin\\theta=\\dfrac12$ のような方程式では、$0^\\circ\\leqq\\theta\\leqq180^\\circ$ で解が2つあることを単位円の図で必ず確認させる。", caution="$30^\\circ$ だけを答える誤りが最も多い。"),
               tp("どの定理を使うかは「分かっているもの」と「求めたいもの」の組で決まることを、表にして整理させる。", ask="2辺とその間の角が分かっているとき、残りの辺は何で求めるか。", expect="余弦定理"),
               tp("答えの吟味（三角形の成立条件：2辺の和は他の1辺より大きい、角の和は $180^\\circ$）を習慣づける。"),
               tp("$\\sin$ の値から角を求めるときに2通りの候補が出たら、角の和や辺の大小関係でふるいにかける手順を示す。", timing="正弦定理の例題の後")],
              misconceptions=[("$\\sin\\theta=\\dfrac35$ のとき $\\cos\\theta=\\dfrac45$ と決めつける", "$\\theta$ が鈍角なら $\\cos\\theta=-\\dfrac45$"),
                              ("面積を $\\dfrac12bc\\cos A$ で計算する", "高さは $b\\sin A$。面積は $\\sin$ を使う")]),
        summary("sm1", "まとめ", ["三角比は単位円上の点の座標として定義すると鈍角まで扱える。", "正弦定理は外接円、余弦定理は座標（三平方の拡張）で証明できる。",
                                   "条件から定理を選ぶ：1辺＋2角 → 正弦定理、2辺＋間の角・3辺 → 余弦定理。面積は $\\dfrac12bc\\sin A$。"]),
        check("ck1", "確認問題", [("$\\cos150^\\circ$ の値は？", "$-\\dfrac{\\sqrt3}{2}$"), ("$\\sin\\theta=\\dfrac{\\sqrt2}{2}\\ (0^\\circ\\leqq\\theta\\leqq180^\\circ)$ を解け。", "$\\theta=45^\\circ,\\ 135^\\circ$"),
                                  ("$b=3,\\ c=8,\\ A=60^\\circ$ のとき $a$ は？", "$a^2=9+64-24=49$ より $a=7$")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

@gen("basic_check", 6, ["computation", "concept"])
def trig_value(r):
    th = r.choice(ANG)
    fn = r.choice(["sin", "cos", "tan"] if th != 90 else ["sin", "cos"])
    v = trig(fn, th)
    acute = th if th <= 90 else 180 - th
    note = "" if th <= 90 else f"$\\{fn}({th}^\\circ)=\\{fn}(180^\\circ-{acute}^\\circ)={'' if fn == 'sin' else '-'}\\{fn}{acute}^\\circ$ を使う。"
    return sa(f"単位円を用いて、$\\{fn}{th}^\\circ$ の値を求めなさい。", f"${tex(v)}$", f"$\\{fn}{th}^\\circ={tex(v)}$。" + note, d=1,
              ap="単位円上で角 $" + f"{th}" + "^\\circ$ の点の座標を考える（$\\cos$ は $x$ 座標、$\\sin$ は $y$ 座標、$\\tan$ は傾き）。",
              steps=[f"角 ${th}^\\circ$ の点は単位円上の $({tex(trig('cos', th))},\\,{tex(trig('sin', th))})$。", f"$\\{fn}{th}^\\circ={tex(v)}$。"],
              alt=["鈍角は $180^\\circ-\\theta$ の公式で鋭角に直して、特別な直角三角形の辺の比から求めてもよい。"],
              pc=[("点の座標（または鋭角への変換）を正しく考えている", 1), ("値（符号を含む）が正しい", 1)],
              pit=["鈍角の $\\cos,\\ \\tan$ の符号を正にしてしまう。"], chk=(f"{fn}(deg({th}))", pyexpr(v), None, "intermediate"))


TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (9, 40, 41)]


@gen("basic_check", 5, ["computation", "condition_check"])
def from_sin(r):
    a, b, c = r.choice(TRIPLES)
    if r.random() < 0.5:
        a, b = b, a
    obtuse = r.random() < 0.5
    cosv = sp.Rational(-b if obtuse else b, c)
    rng = "90^\\circ<\\theta<180^\\circ" if obtuse else "0^\\circ<\\theta<90^\\circ"
    return sa(f"$\\theta$ は ${rng}$ を満たし、$\\sin\\theta=\\dfrac{{{a}}}{{{c}}}$ である。相互関係を用いて $\\cos\\theta,\\ \\tan\\theta$ の値を求めなさい。",
              f"$\\cos\\theta={tex(cosv)},\\ \\tan\\theta={tex(sp.Rational(a, c) / cosv)}$",
              f"$\\cos^2\\theta=1-\\sin^2\\theta=\\dfrac{{{b * b}}}{{{c * c}}}$。" + ("鈍角なので $\\cos\\theta<0$。" if obtuse else "鋭角なので $\\cos\\theta>0$。"), d=2,
              ap="$\\sin$ と $\\cos$ を結ぶ式 $\\sin^2\\theta+\\cos^2\\theta=1$ を使う。$\\cos\\theta$ の符号は $\\theta$ の範囲で決める。",
              steps=[f"$\\cos^2\\theta=1-\\left(\\dfrac{{{a}}}{{{c}}}\\right)^2=\\dfrac{{{b * b}}}{{{c * c}}}$。", ("鈍角" if obtuse else "鋭角") + f"なので $\\cos\\theta={tex(cosv)}$。",
                     f"$\\tan\\theta=\\dfrac{{\\sin\\theta}}{{\\cos\\theta}}={tex(sp.Rational(a, c) / cosv)}$。"],
              alt=[f"斜辺 ${c}$、高さ ${a}$ の直角三角形をかき、三平方の定理で底辺 ${b}$ を求めてから、鈍角なら符号を負にする。"],
              pc=[("$\\cos^2\\theta$ を正しく求めている", 1), ("符号を範囲から正しく決めている", 1)],
              pit=["鈍角なのに $\\cos\\theta$ を正にする。"], chk=(f"sqrt(1-Rational({a},{c})**2)", f"Rational({b},{c})", None, "intermediate"))


@gen("basic_check", 4, ["concept", "condition_check"])
def supplementary(r):
    al = r.choice([10, 20, 25, 35, 40, 50, 55, 65, 70, 80])
    fn = r.choice(["sin", "cos", "tan"])
    th = 180 - al
    right = {"sin": f"$\\sin{al}^\\circ$", "cos": f"$-\\cos{al}^\\circ$", "tan": f"$-\\tan{al}^\\circ$"}[fn]
    pool = [f"$\\sin{al}^\\circ$", f"$-\\sin{al}^\\circ$", f"$\\cos{al}^\\circ$", f"$-\\cos{al}^\\circ$", f"$\\tan{al}^\\circ$", f"$-\\tan{al}^\\circ$"]
    same_fn = [x for x in pool if fn in x and x != right]
    others = [x for x in pool if fn not in x][:2]
    wrongs = same_fn[:1] + others
    why = {}
    for w in wrongs:
        if fn in w:
            why[w] = ("符号が逆。点を $y$ 軸について折り返すと $x$ 座標の符号だけが変わる（$\\sin$ は変わらず、$\\cos,\\ \\tan$ は符号が変わる）。", "$180^\\circ-\\theta$ の公式の符号の誤り")
        else:
            why[w] = ("$180^\\circ-\\theta$ の公式では三角比の種類は変わらない（$\\sin$ と $\\cos$ が入れかわるのは $90^\\circ-\\theta$ の公式）。", "$90^\\circ-\\theta$ の公式との混同")
    return mc(f"$\\{fn}{th}^\\circ$ と等しいものを選びなさい。", [right] + wrongs, f"$\\{fn}(180^\\circ-\\theta)$ の公式を使う。$\\{fn}{th}^\\circ={right[1:-1]}$。", d=2,
              ap="鈍角 $" + f"{th}" + "^\\circ$ を $180^\\circ-" + f"{al}" + "^\\circ$ と見て、$180^\\circ-\\theta$ の公式を使う。",
              steps=[f"${th}^\\circ=180^\\circ-{al}^\\circ$。", "$\\sin(180^\\circ-\\theta)=\\sin\\theta,\\ \\cos(180^\\circ-\\theta)=-\\cos\\theta,\\ \\tan(180^\\circ-\\theta)=-\\tan\\theta$。", f"よって {right}。"],
              alt=["単位円上で角 $" + f"{th}" + "^\\circ$ と $" + f"{al}" + "^\\circ$ の点が $y$ 軸に関して対称であることを図で確認する。"],
              pc=[("$180^\\circ-\\theta$ の形に直している", 1), ("符号を含めて正しい", 1)], why=why,
              chk=(f"{fn}(deg({th}))-({'' if fn == 'sin' else '-'}{fn}(deg({al})))", "0", None, "intermediate"))


SOLVE = [("sin", "\\dfrac{1}{2}", "Rational(1,2)", [30, 150]), ("sin", "\\dfrac{\\sqrt{3}}{2}", "sqrt(3)/2", [60, 120]), ("sin", "\\dfrac{\\sqrt{2}}{2}", "sqrt(2)/2", [45, 135]),
         ("sin", "1", "1", [90]), ("sin", "0", "0", [0, 180]), ("cos", "-\\dfrac{1}{2}", "-Rational(1,2)", [120]), ("cos", "\\dfrac{\\sqrt{2}}{2}", "sqrt(2)/2", [45]),
         ("cos", "-\\dfrac{\\sqrt{3}}{2}", "-sqrt(3)/2", [150]), ("tan", "-1", "-1", [135]), ("tan", "\\sqrt{3}", "sqrt(3)", [60]), ("tan", "-\\dfrac{1}{\\sqrt{3}}", "-1/sqrt(3)", [150]),
         ("cos", "0", "0", [90])]


@gen("basic_check", 5, ["computation", "condition_check"])
def solve_eq(r):
    fn, vt, vp, sols = r.choice(SOLVE)
    ans = ",\\ ".join(f"{s}^\\circ" for s in sols)
    return sa(f"$0^\\circ\\leqq\\theta\\leqq180^\\circ$ のとき、$\\{fn}\\theta={vt}$ を満たす $\\theta$ をすべて求めなさい。", f"$\\theta={ans}$",
              f"単位円で{'$y$ 座標' if fn == 'sin' else ('$x$ 座標' if fn == 'cos' else '傾き')}が ${vt}$ になる点を探す。", d=2,
              ap="$\\sin$ は $y$ 座標、$\\cos$ は $x$ 座標なので、単位円と直線の交点として角を読み取る。$\\sin$ では解が2つになることが多い。",
              steps=[{"sin": f"直線 $y={vt}$ と単位円（上半分）の交点を考える。", "cos": f"直線 $x={vt}$ と単位円の交点を考える。", "tan": f"原点を通る傾き ${vt}$ の直線と単位円の交点を考える。"}[fn],
                     f"交点に対応する角は $\\theta={ans}$。"],
              alt=["鋭角の解 $\\alpha$ を求め、$\\sin$ のときは $180^\\circ-\\alpha$ も解になるか確かめる。"],
              pc=[("単位円（または公式）を使って角を考えている", 1), ("すべての解を答えている", 1)],
              pit=["$\\sin\\theta=\\dfrac12$ で $30^\\circ$ だけを答える（$150^\\circ$ のもれ）。"],
              chk=(f"[{fn}(deg(t)) for t in []]" if False else f"[{', '.join(f'{fn}(deg({s}))' for s in sols)}]", f"[{', '.join([vp] * len(sols))}]", None, "intermediate"))


# ======================================================================
# B 標準演習
# ======================================================================

SINE_SET = [(45, 60), (30, 45), (60, 45), (30, 60), (45, 30), (60, 30), (30, 120), (45, 105), (120, 30), (135, 30)]


@gen("standard_practice", 6, ["computation"])
def sine_rule(r):
    A, B = r.choice(SINE_SET)
    a = r.choice([2, 3, 4, 6, 8, 10, 12])
    b = sp.nsimplify(a * sp.sin(sp.pi * B / 180) / sp.sin(sp.pi * A / 180))
    R = sp.nsimplify(a / (2 * sp.sin(sp.pi * A / 180)))
    return sa(f"$\\triangle\\mathrm{{ABC}}$ において、$a={a},\\ A={A}^\\circ,\\ B={B}^\\circ$ のとき、$b$ と外接円の半径 $R$ を求めなさい。", f"$b={tex(b)},\\ R={tex(R)}$",
              f"正弦定理 $\\dfrac{{a}}{{\\sin A}}=\\dfrac{{b}}{{\\sin B}}=2R$ を使う。", d=3,
              ap="1辺 $a$ と、その対角 $A$ と、求める辺の対角 $B$ が分かっている → 正弦定理。",
              steps=[f"$b=\\dfrac{{a\\sin B}}{{\\sin A}}=\\dfrac{{{a}\\cdot{tex(trig('sin', B))}}}{{{tex(trig('sin', A))}}}={tex(b)}$。", f"$2R=\\dfrac{{a}}{{\\sin A}}$ より $R={tex(R)}$。"],
              alt=[f"$C=180^\\circ-{A}^\\circ-{B}^\\circ={180 - A - B}^\\circ$ も求めておくと、余弦定理で $b$ を検算できる。"],
              pc=[("正弦定理の式を正しく立てている", 1), ("$b$ を正しく計算している", 2), ("$R$ を正しく求めている", 1)],
              pit=["$2R$ を $R$ と取り違える。", "分母の有理化を忘れる。"],
              chk=(f"[{a}*sin(deg({B}))/sin(deg({A})), {a}/(2*sin(deg({A})))]", f"[{pyexpr(b)}, {pyexpr(R)}]", None, "intermediate"))


@gen("standard_practice", 5, ["computation"])
def cosine_side(r):
    A = r.choice([60, 120, 90, 60, 120, 45, 135, 150, 30])
    b, c = r.randint(2, 9), r.randint(2, 9)
    a2 = sp.nsimplify(b * b + c * c - 2 * b * c * sp.cos(sp.pi * A / 180))
    a = sp.sqrt(a2)
    return sa(f"$\\triangle\\mathrm{{ABC}}$ において、$b={b},\\ c={c},\\ A={A}^\\circ$ のとき、$a$ を求めなさい。", f"$a={tex(a)}$",
              f"余弦定理 $a^2=b^2+c^2-2bc\\cos A$ を使う。", d=3,
              ap="2辺とその間の角が分かっている → 余弦定理で対辺を求める。",
              steps=[f"$a^2={b}^2+{c}^2-2\\cdot{b}\\cdot{c}\\cos{A}^\\circ$。", f"$\\cos{A}^\\circ={tex(trig('cos', A))}$ を代入して $a^2={tex(a2)}$。", f"$a>0$ より $a={tex(a)}$。"],
              alt=["座標を使う：A を原点、B を $(c,\\,0)$、C を $(b\\cos A,\\,b\\sin A)$ として BC の長さを2点間の距離で求めても同じ。"],
              pc=[("余弦定理の式を正しく立てている", 1), ("$\\cos A$ の値（符号）を正しく代入している", 2), ("$a$ を正しく求めている", 1)],
              pit=["鈍角で $\\cos A$ の符号を誤り、$-2bc\\cos A$ の符号処理を間違える。"],
              chk=(f"sqrt({b}**2+{c}**2-2*{b}*{c}*cos(deg({A})))", pyexpr(a), None, "intermediate"))


ANGLE_TRIPLES = [((7, 5, 3), 120), ((7, 8, 3), 60), ((13, 8, 15), 60), ((19, 5, 16), 120), ((14, 6, 10), 120), ((7, 3, 8), 60), ((13, 7, 8), 120),
                 ((5, 3, 4), 90), ((13, 5, 12), 90), ((21, 15, 24), 60)]


@gen("standard_practice", 4, ["computation"])
def cosine_angle(r):
    (a, b, c), A = r.choice(ANGLE_TRIPLES)
    k = r.choice([1, 1, 2])
    a, b, c = a * k, b * k, c * k
    cosA = sp.Rational(b * b + c * c - a * a, 2 * b * c)
    return sa(f"$\\triangle\\mathrm{{ABC}}$ において、$a={a},\\ b={b},\\ c={c}$ のとき、$A$ を求めなさい。", f"$A={A}^\\circ$",
              f"$\\cos A=\\dfrac{{b^2+c^2-a^2}}{{2bc}}={tex(cosA)}$。", d=3,
              ap="3辺が分かっていて角を求める → 余弦定理を $\\cos A$ について解いた形を使う。",
              steps=[f"$\\cos A=\\dfrac{{{b * b}+{c * c}-{a * a}}}{{2\\cdot{b}\\cdot{c}}}={tex(cosA)}$。", f"$0^\\circ<A<180^\\circ$ より $A={A}^\\circ$。"],
              alt=["最大辺の対角が最大角。$a$ が最大辺なので、$\\cos A$ の符号で鋭角・直角・鈍角の判定もできる。"],
              pc=[("$\\cos A$ の式を正しく立てて計算している", 2), ("角を正しく求めている", 2)],
              pit=["$\\cos A<0$ なのに鋭角を答える。"], chk=(f"acos(Rational({b * b + c * c - a * a},{2 * b * c}))*180/pi", str(A), None, "intermediate"))


@gen("standard_practice", 5, ["computation"])
def area(r):
    A = r.choice([30, 45, 60, 90, 120, 135, 150])
    b, c = r.randint(2, 10), r.randint(2, 10)
    S = sp.nsimplify(sp.Rational(1, 2) * b * c * sp.sin(sp.pi * A / 180))
    return sa(f"$\\triangle\\mathrm{{ABC}}$ において、$b={b},\\ c={c},\\ A={A}^\\circ$ のとき、面積 $S$ を求めなさい。", f"${tex(S)}$",
              f"$S=\\dfrac{{1}}{{2}}bc\\sin A$。", d=2,
              ap="2辺とその間の角が分かっている → 面積公式 $S=\\dfrac12bc\\sin A$。",
              steps=[f"$S=\\dfrac{{1}}{{2}}\\cdot{b}\\cdot{c}\\cdot\\sin{A}^\\circ$。", f"$\\sin{A}^\\circ={tex(trig('sin', A))}$ より $S={tex(S)}$。"],
              alt=[f"高さ $h=b\\sin A={tex(b * trig('sin', A))}$ を求めてから $\\dfrac12\\cdot c\\cdot h$ としてもよい。"],
              pc=[("面積公式を正しく使っている", 2), ("値が正しい", 2)], pit=["$\\cos A$ を使ってしまう。", "$\\dfrac12$ をかけ忘れる。"],
              chk=(f"Rational(1,2)*{b}*{c}*sin(deg({A}))", pyexpr(S), None, "intermediate"))


# ======================================================================
# C 思考力・記述応用
# ======================================================================

@gen("thinking_writing", 2, ["condition_check", "written_reasoning", "multiple_solutions"])
def ambiguous(r):
    a = r.choice([2, 3, 4, 6, 8])
    c1 = sp.nsimplify(a * (sp.sqrt(6) + sp.sqrt(2)) / 2)
    c2 = sp.nsimplify(a * (sp.sqrt(6) - sp.sqrt(2)) / 2)
    return desc(f"$\\triangle\\mathrm{{ABC}}$ において、$a={a},\\ b={a}\\sqrt{{2}},\\ A=30^\\circ$ のとき、$B$ と $c$ を求めなさい。",
                f"$B=45^\\circ$ のとき $c={tex(c1)}$、$B=135^\\circ$ のとき $c={tex(c2)}$",
                "正弦定理から $\\sin B=\\dfrac{\\sqrt2}{2}$。$B=45^\\circ,\\ 135^\\circ$ のどちらも $A+B<180^\\circ$ を満たすので、三角形は2つある。",
                [("正弦定理で $\\sin B$ を求めている", 2), ("$B$ の2つの候補を挙げ、どちらも適することを確かめている", 3), ("それぞれの場合の $c$ を正しく求めている", 3)], d=5, p=8, lines=10,
                ap="2辺と、その一方の対角が分かっている（2辺夾角ではない）ので、正弦定理で $\\sin B$ を求める。$\\sin$ の値から角を求めると2通りの候補が出るので、両方が三角形として成り立つか確かめる。",
                steps=[f"$\\dfrac{{{a}}}{{\\sin30^\\circ}}=\\dfrac{{{a}\\sqrt2}}{{\\sin B}}$ より $\\sin B=\\dfrac{{\\sqrt2}}{{2}}$。", "$B=45^\\circ$ または $135^\\circ$。どちらも $30^\\circ+B<180^\\circ$。",
                       f"$B=45^\\circ$ のとき $C=105^\\circ$。余弦定理 $a^2=b^2+c^2-2bc\\cos A$ より $c^2-{a}\\sqrt6\\,c+{a * a}=0$、大きい方の解 $c={tex(c1)}$。",
                       f"$B=135^\\circ$ のとき $C=15^\\circ$ で、小さい方の解 $c={tex(c2)}$。"],
                alt=["余弦定理 $a^2=b^2+c^2-2bc\\cos A$ を $c$ の二次方程式として解くと、2つの正の解が2つの三角形に対応する（正弦定理を使わない解法）。"],
                pc=[("$\\sin B$ の計算", 2), ("2通りの $B$ の吟味", 3), ("それぞれの $c$", 3)],
                pit=["$B=45^\\circ$ だけを答える。", "2つの $c$ と2つの $B$ の対応を取り違える（$B$ が大きいほど $C$ は小さく、$c$ も小さい）。"],
                chk=(f"solve(c**2-{a}*sqrt(6)*c+{a * a}, c)", f"[{pyexpr(c2)}, {pyexpr(c1)}]", "set", "intermediate"))


@gen("thinking_writing", 3, ["cross_unit", "written_reasoning"], rel=["HS-MATH1-U03"])
def min_bc(r):
    L = r.choice([4, 6, 8, 10, 12, 14])
    A = r.choice([60, 90, 120])
    cosA = trig("cos", A)
    k = 2 + 2 * cosA  # BC^2 = (2+2cos)x^2 - (2+2cos)L x + L^2
    m2 = sp.nsimplify(L * L - k * L * L / 4)
    return desc(f"$\\triangle\\mathrm{{ABC}}$ において、$\\mathrm{{AB}}+\\mathrm{{AC}}={L}$、$\\angle\\mathrm{{A}}={A}^\\circ$ である。$\\mathrm{{AB}}=x$ とするとき、辺 BC の長さの最小値と、そのときの $x$ を求めなさい。",
                f"$x={sp.Rational(L, 2)}$ のとき最小値 ${tex(sp.sqrt(m2))}$",
                f"余弦定理で $\\mathrm{{BC}}^2$ を $x$ の二次関数で表し、平方完成して最小値を求める。", [
                    ("余弦定理で $\\mathrm{BC}^2$ を $x$ で表している", 3), ("$x$ の変域を示している", 1), ("平方完成して最小値と $x$ を求めている", 3), ("$\\mathrm{BC}>0$ から平方根をとって答えている", 1)],
                d=4, p=8, lines=10,
                ap="BC は2辺とその間の角から余弦定理で表せる。すると $\\mathrm{BC}^2$ が $x$ の二次関数になるので、二次関数の最小値の問題に帰着する（BC が最小 ⇔ $\\mathrm{BC}^2$ が最小）。",
                steps=[f"$\\mathrm{{AC}}={L}-x\\ (0<x<{L})$。", f"$\\mathrm{{BC}}^2=x^2+({L}-x)^2-2x({L}-x)\\cos{A}^\\circ={tex(sp.expand(k * sp.Symbol('x') ** 2 - k * L * sp.Symbol('x') + L * L))}$。",
                       f"平方完成すると $x={sp.Rational(L, 2)}$ で最小値 ${tex(m2)}$。", f"よって BC の最小値は ${tex(sp.sqrt(m2))}$。"],
                alt=["AB＝AC（二等辺三角形）のとき最小になることは、対称性からも予想できる。答えの検算に使える。"],
                pc=[("$\\mathrm{BC}^2$ の式", 3), ("変域", 1), ("最小値の計算", 3), ("平方根", 1)],
                pit=["BC そのものではなく $\\mathrm{BC}^2$ の最小値を答えてしまう。"],
                chk=(f"expand(x**2+({L}-x)**2-2*x*({L}-x)*cos(deg({A})))", pyexpr(sp.expand(k * sp.Symbol('x') ** 2 - k * L * sp.Symbol('x') + L * L)), "expand", "intermediate"))


CHOOSE = [("1辺とその両端の角", "正弦定理（残りの角を先に求めてから）", "余弦定理", "面積公式 $\\dfrac12bc\\sin A$"),
          ("2辺とその間の角", "余弦定理", "正弦定理", "三平方の定理"),
          ("3辺", "余弦定理（$\\cos A$ を求める）", "正弦定理", "面積公式 $\\dfrac12bc\\sin A$"),
          ("1辺とその対角、および外接円の半径を求めたい", "正弦定理", "余弦定理", "三平方の定理")]


@gen("thinking_writing", 2, ["condition_check", "concept"])
def choose_law(r):
    given, right, w1, w2 = r.choice(CHOOSE)
    target = "外接円の半径" if "外接円" in given else "残りの辺や角"
    why = {w1: (f"{w1}はこの条件では未知数が2つ以上残り、直接は使えない（使うには他の量を先に求める必要がある）。", "定理の適用条件の取り違え"),
           w2: (f"{w2}は条件が合わない（直角三角形でない／角を求める道具ではない）。", "公式の適用条件の誤解")}
    return mc(f"三角形について「{given}」が分かっているとき、{target}を求めるために最初に使うのに最も適切なものを選びなさい。", [right, w1, w2],
              f"「{given}」の条件に合うのは{right}。", d=4, p=8,
              ap="各定理の式に含まれる量を確認し、分かっている量だけで未知数が1つになる式を選ぶ。",
              steps=["正弦定理：$\\dfrac{a}{\\sin A}=\\dfrac{b}{\\sin B}$（辺と対角の組が2つ）。", "余弦定理：$a^2=b^2+c^2-2bc\\cos A$（3辺と1角）。", f"「{given}」なら{right}。"],
              alt=["迷ったら三角形を描いて、分かっている辺・角に印をつけ、どの式なら未知数が1つになるかを確かめる。"],
              pc=[("各定理に含まれる量を確認している", 4), ("適切な定理を選んでいる", 4)], why=why)


@gen("thinking_writing", 3, ["written_reasoning", "concept"])
def proof_item(r):
    kind = r.choice(["tan", "supp", "area", "pyth", "comp", "cosl"])
    if kind == "tan":
        return desc("$\\theta\\neq90^\\circ$ のとき、$1+\\tan^2\\theta=\\dfrac{1}{\\cos^2\\theta}$ が成り立つことを証明しなさい。",
                    "$\\tan\\theta=\\dfrac{\\sin\\theta}{\\cos\\theta}$ より $1+\\tan^2\\theta=\\dfrac{\\cos^2\\theta+\\sin^2\\theta}{\\cos^2\\theta}=\\dfrac{1}{\\cos^2\\theta}$。",
                    "$\\sin^2\\theta+\\cos^2\\theta=1$ を $\\cos^2\\theta$ で割る、または $\\tan$ を $\\sin,\\ \\cos$ で表して通分する。",
                    [("$\\tan\\theta=\\dfrac{\\sin\\theta}{\\cos\\theta}$ を用いている", 3), ("通分（または割り算）を正しく行っている", 3), ("$\\sin^2\\theta+\\cos^2\\theta=1$ を使って結論を導いている", 2)],
                    d=4, p=8, kind="proof", lines=6, ap="既に示した $\\sin^2\\theta+\\cos^2\\theta=1$ と $\\tan$ の定義だけで示す。",
                    steps=["$1+\\tan^2\\theta=1+\\dfrac{\\sin^2\\theta}{\\cos^2\\theta}$。", "通分して $\\dfrac{\\cos^2\\theta+\\sin^2\\theta}{\\cos^2\\theta}$。", "分子は $1$ なので $\\dfrac{1}{\\cos^2\\theta}$。"],
                    alt=["$\\sin^2\\theta+\\cos^2\\theta=1$ の両辺を $\\cos^2\\theta\\ (\\neq0)$ で割る。"], pc=[("$\\tan$ の変形", 3), ("通分", 3), ("結論", 2)],
                    pit=["$\\cos\\theta\\neq0$（$\\theta\\neq90^\\circ$）の条件にふれない。"],
                    chk=("trigsimp(1+tan(theta)**2-1/cos(theta)**2)", "0", None, "intermediate"))
    if kind == "pyth":
        return desc("$0^\\circ\\leqq\\theta\\leqq180^\\circ$ のとき、$\\sin^2\\theta+\\cos^2\\theta=1$ が成り立つことを、三角比の定義にもとづいて証明しなさい。",
                    "半径 $r$ の円周上の点 P$(x,\\,y)$ で $\\sin\\theta=\\dfrac{y}{r},\\ \\cos\\theta=\\dfrac{x}{r}$。P は円周上にあるので $x^2+y^2=r^2$。よって $\\sin^2\\theta+\\cos^2\\theta=\\dfrac{x^2+y^2}{r^2}=1$。",
                    "定義に使う点 P が円周上にあることを式 $x^2+y^2=r^2$ で表す。",
                    [("三角比の定義を正しく書いている", 3), ("$x^2+y^2=r^2$ を用いている", 3), ("結論を導いている", 2)],
                    d=3, p=8, kind="proof", lines=6, ap="三角比は円周上の点の座標で定義したので、円の方程式（三平方の定理）がそのまま相互関係になる。",
                    steps=["P$(x,y)$、半径 $r$ をとる。", "$\\sin^2\\theta+\\cos^2\\theta=\\dfrac{y^2+x^2}{r^2}$。", "$x^2+y^2=r^2$ より $1$。"],
                    alt=["鋭角では直角三角形の三平方の定理 $a^2+b^2=c^2$ の両辺を $c^2$ で割っても示せる（鈍角を含めるには座標を使う）。"],
                    pc=[("定義", 3), ("円の方程式", 3), ("結論", 2)], pit=["鋭角の直角三角形だけで済ませ、鈍角の場合にふれない。"],
                    chk=("simplify(sin(theta)**2+cos(theta)**2)", "1", None, "intermediate"))
    if kind == "comp":
        return desc("$0^\\circ<\\theta<90^\\circ$ のとき、$\\sin(90^\\circ-\\theta)=\\cos\\theta,\\ \\cos(90^\\circ-\\theta)=\\sin\\theta$ を、直角三角形を用いて証明しなさい。",
                    "$\\angle\\mathrm{C}=90^\\circ,\\ \\angle\\mathrm{A}=\\theta$ の直角三角形 ABC では $\\angle\\mathrm{B}=90^\\circ-\\theta$。$\\sin(90^\\circ-\\theta)=\\dfrac{\\mathrm{AC}}{\\mathrm{AB}}=\\cos\\theta$、$\\cos(90^\\circ-\\theta)=\\dfrac{\\mathrm{BC}}{\\mathrm{AB}}=\\sin\\theta$。",
                    "1つの直角三角形で、2つの鋭角 $\\theta$ と $90^\\circ-\\theta$ を両方の立場から見る。",
                    [("直角三角形と角を正しく設定している", 2), ("$\\angle\\mathrm{B}=90^\\circ-\\theta$ を示している", 2), ("辺の比を両方の角について比べ、結論を導いている", 4)],
                    d=3, p=8, kind="proof", lines=6, ap="角 B から見た「対辺」は、角 A から見た「隣辺」であることに注目する。",
                    steps=["直角三角形 ABC（$C=90^\\circ$、$A=\\theta$）をとる。", "$B=90^\\circ-\\theta$。", "B から見た対辺 AC は A から見た隣辺なので $\\sin B=\\cos A$、同様に $\\cos B=\\sin A$。"],
                    alt=["単位円で、点 $(\\cos\\theta,\\sin\\theta)$ と直線 $y=x$ に関して対称な点が $(\\sin\\theta,\\cos\\theta)$ であることを使っても示せる。"],
                    pc=[("設定", 2), ("角の関係", 2), ("辺の比の比較", 4)], pit=["$180^\\circ-\\theta$ の公式と混同する。"],
                    chk=("simplify(sin(pi/2-theta)-cos(theta))", "0", None, "intermediate"))
    if kind == "cosl":
        return desc("$\\triangle\\mathrm{ABC}$ において、座標平面を用いて余弦定理 $a^2=b^2+c^2-2bc\\cos A$ を証明しなさい。",
                    "A を原点、B$(c,\\,0)$、C$(b\\cos A,\\,b\\sin A)$ とおく。$a^2=\\mathrm{BC}^2=(b\\cos A-c)^2+(b\\sin A)^2=b^2(\\sin^2A+\\cos^2A)-2bc\\cos A+c^2=b^2+c^2-2bc\\cos A$。",
                    "頂点を座標で表し、2点間の距離の公式で $a^2$ を計算する。",
                    [("座標の設定（特に C の座標）が正しい", 3), ("2点間の距離で $a^2$ を展開している", 3), ("$\\sin^2A+\\cos^2A=1$ を用いて結論を導いている", 2)],
                    d=4, p=8, kind="proof", lines=8, ap="三角比の定義から、A から長さ $b$、角 $A$ の位置にある点 C の座標は $(b\\cos A,\\,b\\sin A)$。",
                    steps=["A$(0,0)$、B$(c,0)$、C$(b\\cos A,b\\sin A)$。", "$a^2=(b\\cos A-c)^2+b^2\\sin^2A$。", "展開して相互関係を使う。"],
                    alt=["C から AB に垂線を下ろし、鋭角・鈍角で場合分けして三平方の定理を使う方法もある（座標を使うと場合分けが不要）。"],
                    pc=[("座標", 3), ("距離の計算", 3), ("結論", 2)], pit=["C の座標を $(b\\sin A,\\,b\\cos A)$ と取り違える。"],
                    chk=("trigsimp(expand((b*cos(theta)-c)**2+(b*sin(theta))**2-(b**2+c**2-2*b*c*cos(theta))))", "0", None, "intermediate"))
    if kind == "supp":
        return desc("単位円を用いて、$\\sin(180^\\circ-\\theta)=\\sin\\theta,\\ \\cos(180^\\circ-\\theta)=-\\cos\\theta$ を証明しなさい。",
                    "角 $\\theta$ に対応する単位円上の点を P$(\\cos\\theta,\\,\\sin\\theta)$ とする。P と $y$ 軸に関して対称な点 Q$(-\\cos\\theta,\\,\\sin\\theta)$ は単位円上にあり、OQ が $x$ 軸の正の向きとなす角は $180^\\circ-\\theta$。よって Q の座標は $(\\cos(180^\\circ-\\theta),\\,\\sin(180^\\circ-\\theta))$ でもあり、比べて示される。",
                    "$y$ 軸に関する対称移動で、$x$ 座標だけ符号が変わることを用いる。",
                    [("点 P と、$y$ 軸に関して対称な点 Q を正しく設定している", 3), ("OQ のなす角が $180^\\circ-\\theta$ であることを示している", 3), ("座標の比較から結論を導いている", 2)],
                    d=4, p=8, kind="proof", lines=7, ap="三角比を単位円上の点の座標として定義していることに立ち返る。",
                    steps=["P$(\\cos\\theta,\\sin\\theta)$ をとる。", "$y$ 軸対称な点 Q$(-\\cos\\theta,\\sin\\theta)$ は角 $180^\\circ-\\theta$ に対応。", "Q の座標を2通りに表して比べる。"],
                    alt=["鋭角 $\\theta$ のとき、直角三角形を左右に折り返した図で説明してもよい（ただし鈍角まで含む一般の証明には座標を用いる）。"],
                    pc=[("点の設定", 3), ("角の対応", 3), ("結論", 2)], pit=["図だけで説明し、座標の比較を書かない。"])
    return desc("$\\triangle\\mathrm{ABC}$ の面積 $S$ が $S=\\dfrac12bc\\sin A$ で表されることを、$A$ が鋭角の場合と鈍角の場合に分けて証明しなさい。",
                "C から直線 AB に垂線 CH を下ろす。$A$ が鋭角のとき、直角三角形 ACH で $\\mathrm{CH}=b\\sin A$。$A$ が鈍角のとき、H は BA の延長上にあり $\\mathrm{CH}=b\\sin(180^\\circ-A)=b\\sin A$。どちらの場合も $S=\\dfrac12\\cdot c\\cdot b\\sin A$。",
                "高さを $b$ と $A$ で表す。鈍角のときは外角 $180^\\circ-A$ を使う。",
                [("垂線を下ろして高さを考えている", 2), ("鋭角の場合の高さを正しく表している", 2), ("鈍角の場合を $180^\\circ-A$ を用いて正しく扱っている", 3), ("結論", 1)],
                d=4, p=8, kind="proof", lines=8, ap="三角形の面積＝底辺×高さ÷2。高さを三角比で表す。",
                steps=["垂線 CH を引く。", "鋭角：$\\mathrm{CH}=b\\sin A$。", "鈍角：$\\mathrm{CH}=b\\sin(180^\\circ-A)=b\\sin A$。", "$S=\\dfrac12c\\,\\mathrm{CH}=\\dfrac12bc\\sin A$。"],
                alt=["座標で A$(0,0)$、B$(c,0)$、C$(b\\cos A,\\,b\\sin A)$ とおけば、C の $y$ 座標が高さになり、場合分けなしで示せる。"],
                pc=[("垂線", 2), ("鋭角", 2), ("鈍角", 3), ("結論", 1)], pit=["鈍角の場合を省略する。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(stem, wrong, step, etype, tempt, fix, ans, expl, steps, ap, alt, pit, chk=None, d=3):
    return desc(f"{stem}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい答えを求めなさい。", ans, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい解答を途中式とともに示している", 3), ("最終的な答えが正しい", 1)], d=d, p=6, lines=6,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい途中式", 3), ("正しい答え", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix), chk=chk)


@gen("error_correction", 3, ["common_error", "condition_check"])
def err_one_solution(r):
    vt, vp, a1 = r.choice([("\\dfrac{1}{2}", "Rational(1,2)", 30), ("\\dfrac{\\sqrt{3}}{2}", "sqrt(3)/2", 60), ("\\dfrac{\\sqrt{2}}{2}", "sqrt(2)/2", 45),
                           ("\\dfrac{1}{\\sqrt{2}}", "1/sqrt(2)", 45)])
    a2 = 180 - a1
    rng = r.choice(["0^\\circ\\leqq\\theta\\leqq180^\\circ", "0^\\circ<\\theta<180^\\circ"])
    return err_item(f"${rng}$ のとき、$\\sin\\theta={vt}$ を解きなさい。", f"$\\sin{a1}^\\circ={vt}$ なので $\\theta={a1}^\\circ$",
                    "解を1つしか求めていない部分", "condition",
                    f"特別な直角三角形の知識で $\\sin{a1}^\\circ={vt}$ はすぐ思い出せるが、鈍角の範囲にも $\\sin$ が正になる角があることを意識していない。",
                    f"$\\sin(180^\\circ-{a1}^\\circ)=\\sin{a1}^\\circ$ なので $\\theta={a1}^\\circ,\\ {a2}^\\circ$", f"$\\theta={a1}^\\circ,\\ {a2}^\\circ$",
                    "単位円で直線 $y=" + vt + "$ と交わる点は2つある。",
                    [f"単位円と直線 $y={vt}$ の交点は2つ。", f"それぞれの角は ${a1}^\\circ$ と ${a2}^\\circ$。"],
                    "$0^\\circ\\leqq\\theta\\leqq180^\\circ$ では、$\\sin\\theta=k\\ (0<k<1)$ の解は必ず2つあることを単位円で確認する。",
                    [f"$\\sin{a2}^\\circ$ を計算して ${vt}$ になることを確かめれば、もれに気づける。"], ["範囲が $0^\\circ\\sim180^\\circ$ なら鈍角の解も探す。"],
                    chk=(f"[sin(deg({a1})), sin(deg({a2}))]", f"[{vp}, {vp}]", None, "intermediate"), d=2)


@gen("error_correction", 3, ["common_error", "condition_check"])
def err_cos_sign(r):
    a, b, c = r.choice(TRIPLES)
    if r.random() < 0.5:
        a, b = b, a
    return err_item(f"$\\sin\\theta=\\dfrac{{{a}}}{{{c}}}\\ (90^\\circ<\\theta<180^\\circ)$ のとき、$\\cos\\theta$ の値を求めなさい。",
                    f"$\\cos^2\\theta=1-\\dfrac{{{a * a}}}{{{c * c}}}=\\dfrac{{{b * b}}}{{{c * c}}}$ より $\\cos\\theta=\\dfrac{{{b}}}{{{c}}}$",
                    "最後に平方根をとる部分（符号の決定）", "sign",
                    "$\\cos^2\\theta$ から平方根をとるとき、正の値だけを書く習慣がある。$\\theta$ の範囲を見直していない。",
                    f"$\\theta$ は鈍角なので $\\cos\\theta<0$。$\\cos\\theta=-\\dfrac{{{b}}}{{{c}}}$", f"$\\cos\\theta=-\\dfrac{{{b}}}{{{c}}}$",
                    "平方根をとると $\\pm$ の2つが候補になり、範囲で符号を決める。",
                    [f"$\\cos^2\\theta=\\dfrac{{{b * b}}}{{{c * c}}}$ より $\\cos\\theta=\\pm\\dfrac{{{b}}}{{{c}}}$。", f"$90^\\circ<\\theta<180^\\circ$ では $\\cos\\theta<0$。", f"$\\cos\\theta=-\\dfrac{{{b}}}{{{c}}}$。"],
                    "平方根をとるときは必ず $\\pm$ を書いてから、範囲で一方を選ぶ。",
                    ["単位円で鈍角の点は $y$ 軸の左側にあるので $x$ 座標（$\\cos$）は負、と図で確認できる。"], ["範囲の条件を最後に見直す。"],
                    chk=(f"-sqrt(1-Rational({a},{c})**2)", f"-Rational({b},{c})", None, "intermediate"))


@gen("error_correction", 2, ["common_error", "computation"])
def err_cos_rule(r):
    b, c = r.choice([(3, 5), (5, 3), (7, 8), (5, 16), (6, 10), (3, 8), (4, 6), (2, 7)])
    good2 = b * b + c * c + b * c
    bad2 = b * b + c * c - b * c
    return err_item(f"$\\triangle\\mathrm{{ABC}}$ で $b={b},\\ c={c},\\ A=120^\\circ$ のとき、$a$ を求めなさい。",
                    f"$a^2={b}^2+{c}^2-2\\cdot{b}\\cdot{c}\\cdot\\dfrac12={bad2}$ より $a={tex(sp.sqrt(bad2))}$", "$\\cos120^\\circ$ の値を代入した部分", "sign",
                    "$\\cos60^\\circ=\\dfrac12$ をそのまま使ってしまい、$120^\\circ$ が鈍角で $\\cos$ が負になることを見落としている。",
                    f"$\\cos120^\\circ=-\\dfrac12$ より $a^2={b * b}+{c * c}+{b * c}={good2}$、$a={tex(sp.sqrt(good2))}$", f"$a={tex(sp.sqrt(good2))}$",
                    "鈍角の余弦は負。$-2bc\\cos A$ は正の値になる。",
                    ["$\\cos120^\\circ=-\\cos60^\\circ=-\\dfrac12$。", f"$a^2={b * b}+{c * c}-2\\cdot{b}\\cdot{c}\\cdot\\left(-\\dfrac12\\right)={good2}$。", f"$a={tex(sp.sqrt(good2))}$。"],
                    "$\\cos$ の値は符号まで確認してから代入する。",
                    [f"$A$ が鈍角なら $a$ は最大辺で、$a^2>b^2+c^2={b * b + c * c}$ になるはず。生徒の答え $a^2={bad2}$ はこれに反する（大小関係による検算）。"],
                    ["鈍角のとき $a^2>b^2+c^2$ になるかを確認する。"],
                    chk=(f"{b}**2+{c}**2-2*{b}*{c}*cos(deg(120))", str(good2), None, "intermediate"))


@gen("error_correction", 2, ["common_error", "concept"])
def err_area(r):
    A = r.choice([30, 60, 120, 150, 45, 135])
    b, c = r.randint(3, 9), r.randint(3, 9)
    S = sp.nsimplify(sp.Rational(1, 2) * b * c * sp.sin(sp.pi * A / 180))
    W = sp.nsimplify(sp.Rational(1, 2) * b * c * sp.cos(sp.pi * A / 180))
    return err_item(f"$\\triangle\\mathrm{{ABC}}$ で $b={b},\\ c={c},\\ A={A}^\\circ$ のとき、面積 $S$ を求めなさい。",
                    f"$S=\\dfrac12\\cdot{b}\\cdot{c}\\cos{A}^\\circ={tex(W)}$", "面積公式で $\\cos$ を用いた部分", "formula",
                    "余弦定理と面積公式がどちらも「2辺とその間の角」を使うため、$\\sin$ と $\\cos$ を混同しやすい。" + ("（鈍角では面積が負になり、明らかな誤りとなる。）" if A > 90 else ""),
                    f"$S=\\dfrac12\\cdot{b}\\cdot{c}\\sin{A}^\\circ={tex(S)}$", f"$S={tex(S)}$", "面積の高さは $b\\sin A$ なので、面積公式は $\\sin$ を使う。",
                    [f"高さは $b\\sin A$。", f"$S=\\dfrac12bc\\sin A=\\dfrac12\\cdot{b}\\cdot{c}\\cdot{tex(trig('sin', A))}={tex(S)}$。"],
                    "公式を思い出すときは「高さ＝斜辺×$\\sin$」という図の意味から復元する。",
                    ["面積は必ず正。$\\cos$ を使うと鈍角で負になることからも誤りに気づける。"], ["公式を意味（高さ）とセットで覚える。"],
                    chk=(f"Rational(1,2)*{b}*{c}*sin(deg({A}))", pyexpr(S), None, "intermediate"))


GENERATORS = [trig_value, from_sin, supplementary, solve_eq,
              sine_rule, cosine_side, cosine_angle, area,
              ambiguous, min_bc, choose_law, proof_item,
              err_one_solution, err_cos_sign, err_cos_rule, err_area]
