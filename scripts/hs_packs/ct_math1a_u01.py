"""単元パック：共通テスト対策　数学Ⅰ・A　数と式・二次関数・図形と計量。"""
import math

import sympy as sp

from banks._common import desc, figure, mc, num, plane, sa, shape, table
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, poly, summary,
                         theorem, tp)

UNIT_ID = "CT-MATH1A-U01"

PREREQUISITES = [
    ("HS-MATH1-U01", "根号を含む式の計算・絶対値の場合分け・一次不等式を、時間をかけずに正確に処理できること"),
    ("HS-MATH1-U03", "平方完成、定義域があるときの最大・最小、判別式と二次不等式を使いこなせること"),
    ("HS-MATH1-U04", "鈍角までの三角比、正弦定理・余弦定理・三角形の面積の公式を使えること"),
    ("HS-MATH1-U02", "条件を集合（区間）として表し、必要条件・十分条件を判定できること"),
]
EXTENSIONS = [
    ("CT-MATH1A-U02", "同じ数学Ⅰ・Aの試験で、データの分析・確率・図形の性質の大問に同じ「状況→式」の読み方を使う"),
    ("CT-MATH2BC-U01", "最大・最小を微分で求める問題、三角関数の問題へと、関数の扱い方が発展する"),
    ("HS-MATH2-U06", "3次関数の増減・最大・最小では、定義域と極値の位置を比べる考え方をそのまま使う"),
    ("SS-MATH-U02", "二次試験の記述式計算では、本単元の場合分けや条件の確認を答案として書き切る力が求められる"),
]


# ----------------------------------------------------------------------
# 共通の小道具
# ----------------------------------------------------------------------

def L(e):
    """sympy の式を LaTeX に。"""
    return sp.latex(sp.nsimplify(e))


def fr(p, q):
    f = sp.Rational(p, q)
    if f.q == 1:
        return str(f.p)
    s = "-" if f < 0 else ""
    return f"{s}\\dfrac{{{abs(f.p)}}}{{{f.q}}}"


def deg(a):
    return sp.pi * a / 180


def cst(k):
    return "" if k == 0 else (f"+{k}" if k > 0 else f"{k}")


TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (9, 40, 41)]

# 余弦定理で 60°・120° になる整数辺の三角形 (a, b, c, C)
ANG_TRI = [(3, 8, 7, 60), (5, 8, 7, 60), (7, 15, 13, 60), (8, 15, 13, 60), (16, 21, 19, 60), (5, 21, 19, 60),
           (3, 5, 7, 120), (7, 8, 13, 120), (5, 16, 19, 120), (11, 24, 31, 120), (6, 10, 14, 120), (9, 15, 21, 120),
           (6, 16, 14, 60), (10, 16, 14, 60)]


LESSON = lesson(
    goals=["共通テストの「日常の事象を数学化する」問題で、変数・定義域・関数をすばやく設定できる。",
           "定義域つき・文字を含む二次関数の最大・最小を、軸と区間の位置関係から迷わず処理できる。",
           "測量・図形の状況から、正弦定理・余弦定理・面積公式のどれを使うかを判断し、時間内に計算を終えられる。"],
    duration=100,
    readiness=["平方完成と、定義域があるときの最大・最小（数学Ⅰ 二次関数）を一人で解ける。",
               "$0^\\circ\\leqq\\theta\\leqq180^\\circ$ の三角比の値（$30^\\circ,\\ 45^\\circ,\\ 60^\\circ$ とその補角）を即答できる。",
               "正弦定理・余弦定理・面積公式 $S=\\dfrac{1}{2}bc\\sin A$ を書ける。"],
    flow=[("導入：共通テストの大問の読み方", 10, "問題文の状況を「変数・定義域・式」の3点に整理する枠組みを示す"),
          ("日常の事象の数学化", 20, "例題1（価格設定と売上）で、変数の置き方と定義域の確認を全員で行う"),
          ("最大・最小の場合分け", 25, "軸と区間の位置関係による場合分けを導出し、例題2（動く区間）を扱う"),
          ("三角比の活用", 25, "測量の公式を導出し、例題3（2地点からの仰角）を解く。正弦・余弦定理の選び方を整理"),
          ("時間戦略と典型的なわな", 15, "誘導の使い方・検算の入れ方・典型ミスを問題プリントDで確認"),
          ("まとめと確認", 5, "確認問題3問と、問題プリントA・Bの課題指示")],
    sections=[
        intro("in1", "共通テストの大問をどう読むか",
              "共通テストの数学Ⅰ・Aでは、商品の価格設定や建物の高さの測量のような「日常の状況」が長い文章で示され、それを式に直すところから始まる問題が多い。計算そのものは教科書の基本レベルであることがほとんどで、差がつくのは「状況を正しく式にできるか」と「定義域や条件を見落とさないか」である。本時は、状況を数学の問題に翻訳する手順を型として身につけ、二次関数と図形と計量の典型的な出題に当てはめる。",
              bullets=["読む順序：①何を変数にするか（問題文が指定していればそれに従う） ②変数の動ける範囲（定義域） ③求めたい量を変数の式で表す。",
                       "誘導（「(1) で求めた式を使って…」）は解法の設計図である。前の小問の結果を次の小問でどう使うかを意識して読む。",
                       "マーク式なので、答えの形（分数・根号・整数の桁数）が解答欄から読み取れる。形が合わないときは途中に誤りがある合図。"],
              points=[tp("最初に「この問題で、変数と定義域はどこに書いてあるか」を生徒に探させ、下線を引かせる。", ask="価格を $x$ 円とするとき、$x$ はどんな範囲を動くか。", expect="売れる個数が正であることから上限が決まる。", timing="導入の冒頭"),
                      tp("共通テストでは計算量より読解量が多いことを伝え、問題文を読みながら図や表に情報を書き込む習慣をつけさせる。", caution="問題文を最後まで読まずに計算を始めると、後半で条件の追加に気づいて解き直すことになる。")]),
        definition("df1", "数学化の3ステップ",
                   "状況を数学の問題に直すときは、次の3つを必ず答案（計算用紙）に書き出す。",
                   formula="$$\\text{① 変数 }x\\text{ を決める}\\ \\longrightarrow\\ \\text{② 定義域 }\\alpha\\leqq x\\leqq\\beta\\ \\longrightarrow\\ \\text{③ 目的の量 }y=f(x)$$",
                   conditions=["定義域は「長さ・個数・価格が正」「仕入れの上限」などの現実の制約から決まる。",
                               "③の式が二次関数になれば、平方完成して軸と定義域の位置を比べる。図形の量なら三角比の公式に当てはめる。"],
                   points=[tp("②の定義域を書かずに③に進む生徒が多い。定義域の確認だけで正誤が分かれる問題が毎年のように出ることを強調する。", caution="頂点が定義域の外にあるのに頂点の値を答える誤りが典型。")]),
        theorem("th1", "定義域つきの最大・最小（下に凸の場合）",
                "$$f(x)=a(x-p)^2+q\\ (a>0),\\ \\alpha\\leqq x\\leqq\\beta\\ \\text{の最小値}=\\begin{cases}f(\\beta) & (\\beta<p)\\\\ q & (\\alpha\\leqq p\\leqq\\beta)\\\\ f(\\alpha) & (p<\\alpha)\\end{cases}$$",
                ["最大値は、軸から遠い方の端点でとる（区間の中央 $\\dfrac{\\alpha+\\beta}{2}$ と軸 $p$ の大小で決まる）。",
                 "区間の端が文字 $a$ を含むとき（動く区間）は、軸が区間の「右・中・左」のどこにあるかで3つに場合分けする。"],
                body="共通テストでは、区間や軸に文字を含む形で出題され、場合分けの境界を答えさせることが多い。",
                proof=["$a>0$ のとき、$f(x)=a(x-p)^2+q$ の値は $|x-p|$ が大きいほど大きい。",
                       "軸 $x=p$ が区間内にあれば、区間内で $|x-p|$ が最小となる $x=p$ で最小値 $q$ をとる。",
                       "軸が区間より右（$\\beta<p$）なら、区間全体で $f$ は減少するので右端 $x=\\beta$ で最小。軸が左（$p<\\alpha$）なら増加するので左端で最小。",
                       "最大値は $|x-p|$ が最大となる点、すなわち軸から遠い方の端点でとる。"],
                points=[tp("場合分けを覚えさせるのではなく、「グラフの略図に区間を太線でかき、軸を左から右へ動かす」図を板書で示す。", ask="軸が区間の右にあるとき、区間内でグラフは増加・減少のどちらか。", expect="減少する。だから右端で最小。")]),
        theorem("th2", "三角形の決定と公式の選び方",
                "$$\\dfrac{a}{\\sin A}=\\dfrac{b}{\\sin B}=\\dfrac{c}{\\sin C}=2R,\\qquad a^2=b^2+c^2-2bc\\cos A,\\qquad S=\\dfrac{1}{2}bc\\sin A$$",
                ["「2辺とその間の角」→ 余弦定理で残りの辺、面積公式で面積。", "「3辺」→ 余弦定理で角の余弦。", "「1辺と2角」または外接円の半径 → 正弦定理。",
                 "$0^\\circ<\\theta<180^\\circ$ では $\\sin\\theta>0$ だが、$\\cos\\theta$ と $\\tan\\theta$ は鈍角で負になる。"],
                proof=["$\\triangle\\mathrm{ABC}$ で、頂点 $\\mathrm{C}$ から直線 $\\mathrm{AB}$ に垂線 $\\mathrm{CH}$ を下ろすと、$\\mathrm{CH}=b\\sin A$、$\\mathrm{AH}=b\\cos A$（$A$ が鈍角のときは $\\mathrm{H}$ が辺 $\\mathrm{AB}$ の延長上にあり、$\\cos A<0$ がそのまま向きを表す）。",
                       "面積は $S=\\dfrac{1}{2}\\cdot c\\cdot\\mathrm{CH}=\\dfrac{1}{2}bc\\sin A$。",
                       "$\\mathrm{BH}=c-b\\cos A$ なので、三平方の定理より $a^2=(b\\sin A)^2+(c-b\\cos A)^2=b^2+c^2-2bc\\cos A$。",
                       "外接円の直径 $\\mathrm{BD}$ をとると円周角の定理より $\\angle\\mathrm{BDC}=A$（または $180^\\circ-A$）、$\\angle\\mathrm{BCD}=90^\\circ$ なので $a=2R\\sin A$。"],
                points=[tp("公式は「与えられた情報」で選ぶ。問題文の与えられた量に印をつけ、表の左列（与えられた量）から右列（公式）を引く練習をさせる。", ask="2辺とその間の角が分かっているとき、最初に使う公式は何か。", expect="余弦定理（残りの辺）か面積公式。")]),
        derivation("dv1", "2地点からの仰角による高さの公式（測量）",
                   ["塔の根元を $\\mathrm{H}$、高さを $h$ とする。地点 $\\mathrm{A}$ から仰角 $\\alpha$、塔に向かって $d$ だけ進んだ地点 $\\mathrm{B}$ から仰角 $\\beta$（$\\alpha<\\beta$）で頂上が見えるとする。",
                    "$\\mathrm{AH}=\\dfrac{h}{\\tan\\alpha}$、$\\mathrm{BH}=\\dfrac{h}{\\tan\\beta}$ である（直角三角形の定義）。",
                    "$\\mathrm{AH}-\\mathrm{BH}=d$ より $h\\left(\\dfrac{1}{\\tan\\alpha}-\\dfrac{1}{\\tan\\beta}\\right)=d$。",
                    "よって $h=\\dfrac{d\\tan\\alpha\\tan\\beta}{\\tan\\beta-\\tan\\alpha}$。$\\alpha=30^\\circ,\\ \\beta=60^\\circ$ なら $h=\\dfrac{\\sqrt{3}}{2}d$。"],
                   body="公式として覚えるより、「水平距離を高さで表して差をとる」という立式の流れを身につける。正弦定理を使って $\\triangle\\mathrm{ABP}$（$\\mathrm{P}$ は頂上）から $\\mathrm{BP}$ を求める別解もある。",
                   points=[tp("目の高さ（測量器の高さ）が与えられたときは、最後に足すことを忘れないよう、図の地面に線を引かせる。", caution="目の高さの加算忘れは、毎年の定期考査・模試で最も多い失点の一つ。")],
                   figure=figure("2地点A, Bから塔の頂上Pを見上げる図", shape({"A": (0, 0), "B": (3.0, 0), "H": (5.2, 0), "P": (5.2, 3.0)},
                                                                    segments=[("A", "H"), ("H", "P"), ("A", "P"), ("B", "P")], texts=[(1.2, -0.45, "d"), (5.35, 1.4, "h")], scale=30))),
        example("ex1", "例題1　価格設定と売上（日常の事象の数学化）",
                "ある店では、1個 $200$ 円の商品が1日に $400$ 個売れる。価格を $10$ 円上げるごとに売れる個数は $10$ 個ずつ減るとする。価格を $10x$ 円上げる（$x$ は $0\\leqq x<40$ の整数）とき、1日の売上金額が最大になる価格と、そのときの売上金額を求めよ。",
                ["価格は $200+10x$ 円、売れる個数は $400-10x$ 個（$400-10x>0$ より $x<40$）。",
                 "売上 $y=(200+10x)(400-10x)=-100x^2+2000x+80000$。",
                 "$y=-100(x-10)^2+90000$。軸 $x=10$ は定義域内。",
                 "$x=10$ のとき最大。価格 $300$ 円、売上 $90000$ 円。"],
                "価格 $300$ 円のとき、売上金額は最大で $90000$ 円",
                thinking="変数 $x$ は「値上げの回数」。定義域（個数が正）を先に書き、売上を $x$ の二次関数で表す。",
                points=[tp("答えは「$x$ の値」ではなく「価格」で問われていることに注意させる。", ask="$x=10$ は答えか。", expect="いいえ。価格 $200+10\\cdot10=300$ 円が答え。")],
                misconceptions=[("$x=10$ を答えとして書く", "問われているのは価格なので $200+10x=300$ 円に直す")]),
        example("ex2", "例題2　動く区間での最小値",
                "$f(x)=x^2-4x+5$ の $a\\leqq x\\leqq a+2$ における最小値 $m(a)$ を求めよ。",
                ["$f(x)=(x-2)^2+1$、軸 $x=2$。", "(i) $a+2<2$ すなわち $a<0$ のとき：区間で減少し、$m(a)=f(a+2)=a^2+1$。",
                 "(ii) $a\\leqq2\\leqq a+2$ すなわち $0\\leqq a\\leqq2$ のとき：$m(a)=f(2)=1$。", "(iii) $2<a$ のとき：区間で増加し、$m(a)=f(a)=a^2-4a+5$。"],
                "$a<0$ のとき $a^2+1$、$0\\leqq a\\leqq2$ のとき $1$、$2<a$ のとき $a^2-4a+5$",
                thinking="区間を動かすと考えるより、「軸が区間の右・中・左のどこにあるか」と読みかえる。",
                figure=figure("y=(x-2)^2+1 のグラフと軸 x=2", plane((-1, 5), (-1, 6), unit=16, curves=[(lambda x: (x - 2) ** 2 + 1, "")], points=[(2, 1, "(2,1)")], segments=[((2, -1), (2, 6))])),
                points=[tp("場合分けの境界 $a=0,\\ 2$ で、両側の式の値が一致する（$m(0)=1$、$m(2)=1$）ことを検算として確かめさせる。", ask="$a=0$ のとき (i) の式と (ii) の値は一致するか。", expect="$0^2+1=1$ で一致する。")]),
        example("ex3", "例題3　2地点からの仰角",
                "平らな地面に立つ塔の頂上を、地点 $\\mathrm{A}$ から見上げると仰角が $30^\\circ$、塔に向かって $40\\,\\mathrm{m}$ 進んだ地点 $\\mathrm{B}$ から見上げると仰角が $60^\\circ$ であった。目の高さを無視して、塔の高さを求めよ。",
                ["塔の高さを $h$ m とすると、$\\mathrm{AH}=\\sqrt{3}h$、$\\mathrm{BH}=\\dfrac{h}{\\sqrt{3}}$。", "$\\sqrt{3}h-\\dfrac{h}{\\sqrt{3}}=40$ より $\\dfrac{2h}{\\sqrt{3}}=40$。", "$h=20\\sqrt{3}$。"],
                "$20\\sqrt{3}\\,\\mathrm{m}$",
                thinking="水平距離を $h$ で表し、その差が $40\\,\\mathrm{m}$ であることを式にする。",
                points=[tp("別解として、$\\triangle\\mathrm{ABP}$ が $\\angle\\mathrm{APB}=30^\\circ$ の二等辺三角形（$\\mathrm{BP}=40$）であることに気づけば、$h=40\\sin60^\\circ$ と一瞬で求まることを紹介する。")]),
        board("bd1", "板書案",
              [("① 数学化の3ステップ", ["変数 → 定義域 → 目的の式", "例1：値上げ $10x$ 円", "$y=(200+10x)(400-10x)$", "$=-100(x-10)^2+90000$", "価格 $300$ 円で最大"]),
               ("② 動く区間の最小値", ["軸 $x=2$ と区間 $[a,\\,a+2]$", "(i) $a<0$：$f(a+2)$", "(ii) $0\\leqq a\\leqq2$：$1$", "(iii) $2<a$：$f(a)$", "境界で値が一致 → 検算"]),
               ("③ 測量と三角比", ["$\\mathrm{AH}=h/\\tan\\alpha$", "$\\mathrm{BH}=h/\\tan\\beta$", "差 $=d$ から $h$", "$30^\\circ,\\ 60^\\circ,\\ d=40$", "$h=20\\sqrt{3}$"])],
              points=[tp("左列に「型」、中央に場合分けの図、右列に測量の図を置き、3つの大問タイプが同じ「変数→定義域→式」の流れで解けることを視覚的に示す。")]),
        guide("gd1", "指導ガイド（時間戦略と典型的なわな）",
              [tp("大問1つの目安時間を示し、計算が重い小問は後回しにしてよいことを伝える。", ask="途中の小問が解けないとき、後の小問は解けないか。", expect="誘導の結果が問題文に書かれていれば、それを使って先に進める。", timing="まとめの前"),
               tp("答えの形（マーク欄の桁数・分数か根号か）を検算に使う方法を、例題の答えで確認させる。"),
               tp("鈍角の三角比で $\\cos,\\ \\tan$ の符号を落とす誤り、余弦定理で $-2bc\\cos A$ の符号を誤る誤りを、問題プリントDで扱う。", caution="$\\cos120^\\circ=-\\dfrac{1}{2}$ を代入するとき、$-2bc\\cdot\\left(-\\dfrac{1}{2}\\right)=+bc$ となる。"),
               tp("$\\sqrt{(a-3)^2}=a-3$ のように根号を外す誤りは、数と式の小問で頻出。$\\sqrt{A^2}=|A|$ を毎回書かせる。")],
              misconceptions=[("頂点が定義域の外にあっても、頂点の値を最大値・最小値とする", "軸と定義域の位置関係を確かめ、外にあれば端点の値を比べる"),
                              ("$0^\\circ\\leqq\\theta\\leqq180^\\circ$ で $\\sin\\theta=\\dfrac{3}{5}$ なら $\\cos\\theta=\\dfrac{4}{5}$ だけ", "鈍角の場合もあるので $\\cos\\theta=\\pm\\dfrac{4}{5}$"),
                              ("$\\sqrt{(a-3)^2}=a-3$", "$\\sqrt{(a-3)^2}=|a-3|$。$a<3$ なら $3-a$")]),
        summary("sm1", "まとめ",
                ["状況の問題は「変数 → 定義域 → 目的の式」の3ステップで数学化する。",
                 "二次関数の最大・最小は、軸と区間の位置関係で決まる。動く区間は3つに場合分けし、境界で値が一致するか検算する。",
                 "図形の問題は、与えられた量（2辺と間の角／3辺／1辺と2角）で公式を選ぶ。鈍角では $\\cos,\\ \\tan$ が負。",
                 "時間戦略：誘導を設計図として使い、答えの形で検算する。"]),
        check("ck1", "確認問題",
              [("$y=-2x^2+12x\\ (0\\leqq x\\leqq2)$ の最大値を求めよ。", "$y=-2(x-3)^2+18$。軸 $x=3$ は区間の右外なので、区間で増加。最大値は $x=2$ のとき $16$"),
               ("$90^\\circ<\\theta<180^\\circ$、$\\sin\\theta=\\dfrac{5}{13}$ のとき $\\cos\\theta$ を求めよ。", "$\\cos\\theta=-\\dfrac{12}{13}$"),
               ("$b=3,\\ c=5,\\ A=120^\\circ$ の三角形で $a$ を求めよ。", "$a^2=9+25+15=49$ より $a=7$")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

@gen("basic_check", 5, ["computation", "condition_check"])
def abs_int_count(r):
    k = r.choice([1, 2, 3])
    a = r.randint(-9, 15)
    b = r.randint(2, 11)
    strict = r.choice([True, False])
    lo, hi = sp.Rational(a - b, k), sp.Rational(a + b, k)
    if strict:
        cnt = int(sp.ceiling(hi) - sp.floor(lo) - 1)
        expr = f"ceiling(Rational({a + b},{k}))-floor(Rational({a - b},{k}))-1"
    else:
        cnt = int(sp.floor(hi) - sp.ceiling(lo) + 1)
        expr = f"floor(Rational({a + b},{k}))-ceiling(Rational({a - b},{k}))+1"
    rel = "<" if strict else "\\leqq "
    inner = f"{'' if k == 1 else k}x{'-' if a > 0 else '+'}{abs(a)}" if a != 0 else f"{'' if k == 1 else k}x"
    rng = f"{fr(a - b, k)}{rel}x{rel}{fr(a + b, k)}"
    return num(f"不等式 $|{inner}|{rel}{b}$ を満たす整数 $x$ の個数を求めなさい。", str(cnt),
               f"$-{b}{rel}{inner}{rel}{b}$ より ${rng}$。この範囲の整数は ${cnt}$ 個。", d=2,
               ap="$|A|<c\\ (c>0)$ は $-c<A<c$ と同値。まず $x$ の範囲を求め、端点が整数かどうか（等号を含むか）に注意して数える。",
               steps=[f"$-{b}{rel}{inner}{rel}{b}$ と絶対値を外す。", f"各辺に ${a}$ を加えて ${k}$ で割ると ${rng}$。" if k > 1 else f"各辺に ${a}$ を加えて ${rng}$。",
                      f"範囲内の整数を数えて ${cnt}$ 個。"],
               alt=["数直線上で、中心 $x=" + fr(a, k) + "$ からの距離が $" + fr(b, k) + "$ " + ("未満" if strict else "以下") + "の点の集まりと読みかえて、両端の整数を確かめてもよい。"],
               pc=[("絶対値を外して $x$ の範囲を正しく求めている", 1), ("端点の扱いに注意して個数を正しく数えている", 1)],
               pit=["端点が整数のとき、等号の有無で個数が1つずつ変わることを見落とす。", "$|A|<c$ を $A<c$ だけにしてしまう。"],
               chk=(expr, str(cnt)))


SYM_PAIRS = [(3, 1), (5, 3), (2, 1), (5, 1), (7, 5), (7, 3), (3, 2), (6, 5), (7, 6), (11, 7), (13, 11), (15, 13), (6, 2), (10, 6), (15, 11), (15, 5), (14, 6)]


@gen("basic_check", 5, ["computation"])
def sym_expr(r):
    p, q = r.choice(SYM_PAIRS)
    s = sp.Rational(2 * (p + q), p - q)
    kind = r.choice(["sum", "sq", "cube"] if s <= 8 else ["sum", "sq"])
    sq = "1" if q == 1 else f"\\sqrt{{{q}}}"
    xt = f"\\dfrac{{\\sqrt{{{p}}}+{sq}}}{{\\sqrt{{{p}}}-{sq}}}"
    yt = f"\\dfrac{{\\sqrt{{{p}}}-{sq}}}{{\\sqrt{{{p}}}+{sq}}}"
    X = f"(sqrt({p})+sqrt({q}))/(sqrt({p})-sqrt({q}))"
    Y = f"(sqrt({p})-sqrt({q}))/(sqrt({p})+sqrt({q}))"
    target, val, ex = {"sum": ("x+y", s, f"{X}+{Y}"), "sq": ("x^2+y^2", s * s - 2, f"({X})**2+({Y})**2"),
                       "cube": ("x^3+y^3", s ** 3 - 3 * s, f"({X})**3+({Y})**3")}[kind]
    return num(f"2つの数 $x={xt}$ と $y={yt}$ について、対称式の性質を利用して ${target}$ の値を求めなさい。", str(val),
               f"$x+y={L(s)}$、$xy=1$。" + {"sum": "", "sq": f"$x^2+y^2=(x+y)^2-2xy={L(val)}$。", "cube": f"$x^3+y^3=(x+y)^3-3xy(x+y)={L(val)}$。"}[kind], d=2,
               ap="$x,\\ y$ を別々に有理化して代入するより、対称式 $x+y,\\ xy$ を先に求めて、目的の式をそれらで表す方が速く確実。",
               steps=[f"$xy=1$（互いに逆数）。", f"$x+y=\\dfrac{{(\\sqrt{{{p}}}+{sq})^2+(\\sqrt{{{p}}}-{sq})^2}}{{{p}-{q}}}=\\dfrac{{{2 * (p + q)}}}{{{p - q}}}={L(s)}$。",
                      {"sum": f"よって $x+y={L(s)}$。", "sq": f"$x^2+y^2=(x+y)^2-2xy={L(s * s)}-2={L(val)}$。",
                       "cube": f"$x^3+y^3=(x+y)^3-3xy(x+y)={L(s ** 3)}-{L(3 * s)}={L(val)}$。"}[kind]],
               alt=[f"分母を有理化すると $x={L(sp.radsimp((sp.sqrt(p) + sp.sqrt(q)) ** 2 / (p - q)))}$、$y={L(sp.radsimp((sp.sqrt(p) - sp.sqrt(q)) ** 2 / (p - q)))}$。直接代入しても同じ値になる（根号の項が打ち消し合う）。"],
               pc=[("$x+y$ と $xy$ を正しく求めている", 1), ("対称式の変形で目的の値を求めている", 1)],
               pit=["$x^2+y^2=(x+y)^2$ と $-2xy$ を忘れる。", "有理化で分母を $p+q$ としてしまう（正しくは $p-q$）。"],
               chk=(ex, str(val)))


@gen("basic_check", 5, ["concept", "condition_check"])
def trig_obtuse(r):
    a, b, c = r.choice(TRIPLES)
    if r.random() < 0.5:
        a, b = b, a
    kind = r.choice(["sin_cos", "sin_tan", "cos_sin", "tan_cos"])
    if kind == "sin_cos":
        given, cond, ask, ans, ex = f"\\sin\\theta={fr(a, c)}", "90^\\circ<\\theta<180^\\circ", "\\cos\\theta", fr(-b, c), f"-sqrt(1-Rational({a},{c})**2)"
        stp = [f"$\\cos^2\\theta=1-\\sin^2\\theta=1-\\dfrac{{{a * a}}}{{{c * c}}}=\\dfrac{{{b * b}}}{{{c * c}}}$。", "$\\theta$ は鈍角なので $\\cos\\theta<0$。", f"$\\cos\\theta={fr(-b, c)}$。"]
    elif kind == "sin_tan":
        given, cond, ask, ans, ex = f"\\sin\\theta={fr(a, c)}", "90^\\circ<\\theta<180^\\circ", "\\tan\\theta", fr(-a, b), f"Rational({a},{c})/(-sqrt(1-Rational({a},{c})**2))"
        stp = [f"$\\cos^2\\theta=1-\\dfrac{{{a * a}}}{{{c * c}}}=\\dfrac{{{b * b}}}{{{c * c}}}$、鈍角なので $\\cos\\theta={fr(-b, c)}$。", f"$\\tan\\theta=\\dfrac{{\\sin\\theta}}{{\\cos\\theta}}={fr(-a, b)}$。"]
    elif kind == "cos_sin":
        given, cond, ask, ans, ex = f"\\cos\\theta={fr(-b, c)}", "0^\\circ\\leqq\\theta\\leqq180^\\circ", "\\sin\\theta", fr(a, c), f"sqrt(1-Rational({-b},{c})**2)"
        stp = [f"$\\sin^2\\theta=1-\\cos^2\\theta=\\dfrac{{{a * a}}}{{{c * c}}}$。", "$0^\\circ\\leqq\\theta\\leqq180^\\circ$ では $\\sin\\theta\\geqq0$。", f"$\\sin\\theta={fr(a, c)}$。"]
    else:
        given, cond, ask, ans, ex = f"\\tan\\theta={fr(-a, b)}", "0^\\circ\\leqq\\theta\\leqq180^\\circ", "\\cos\\theta", fr(-b, c), f"-1/sqrt(1+Rational({a},{b})**2)"
        stp = [f"$1+\\tan^2\\theta=\\dfrac{{1}}{{\\cos^2\\theta}}$ より $\\cos^2\\theta=\\dfrac{{{b * b}}}{{{c * c}}}$。", "$\\tan\\theta<0$ なので $\\theta$ は鈍角で $\\cos\\theta<0$。", f"$\\cos\\theta={fr(-b, c)}$。"]
    return sa(f"${cond}$ で ${given}$ のとき、${ask}$ の値を求めなさい。", f"${ans}$", "相互関係で2乗の値を求め、角の範囲から符号を決める。", d=2,
              v=[ans.replace("\\dfrac{", "").replace("}{", "/").replace("}", "")],
              ap="三角比の相互関係 $\\sin^2\\theta+\\cos^2\\theta=1$、$1+\\tan^2\\theta=\\dfrac{1}{\\cos^2\\theta}$ で大きさを決め、符号は角の範囲（鋭角か鈍角か）で決める。",
              steps=stp,
              alt=[f"単位円（半径 ${c}$ の円）上に $x$ 座標 $\\pm{b}$、$y$ 座標 ${a}$ の点をとり、直角三角形 ${a}:{b}:{c}$ を図にかいて符号を読み取ってもよい。"],
              pc=[("相互関係で2乗の値を正しく求めている", 1), ("角の範囲から符号を正しく決めている", 1)],
              pit=["鈍角なのに $\\cos\\theta,\\ \\tan\\theta$ を正としてしまう。", "$0^\\circ\\leqq\\theta\\leqq180^\\circ$ で $\\sin\\theta$ に負の値を含めてしまう。"],
              chk=(ex, ans.replace("\\dfrac{", "Rational(").replace("}{", ",").replace("}", ")").replace("-Rational(", "-Rational(")))


@gen("basic_check", 5, ["computation", "concept"])
def cos_law_angle(r):
    a, b, c, C = r.choice(ANG_TRI)
    if r.random() < 0.5:
        a, b = b, a
    P, Q, R = r.choice([("A", "B", "C"), ("B", "C", "A"), ("C", "A", "B")])  # R が求める角、PQ がその対辺
    sides = {"".join(sorted(Q + R)): a, "".join(sorted(R + P)): b, "".join(sorted(P + Q)): c}
    txt = "、".join(f"$\\mathrm{{{k}}}={sides[k]}$" for k in ("AB", "BC", "AC"))
    cosv = sp.Rational(a * a + b * b - c * c, 2 * a * b)
    return num(f"$\\triangle\\mathrm{{ABC}}$ において {txt} である。$\\angle\\mathrm{{{R}}}$ の大きさを求めなさい（単位は度）。", str(C),
               f"$\\cos {R}=\\dfrac{{{a}^2+{b}^2-{c}^2}}{{2\\cdot{a}\\cdot{b}}}={L(cosv)}$ より ${C}^\\circ$。", d=2, disp=f"${C}^\\circ$",
               ap=f"3辺が分かっていて角を求めるので、余弦定理を $\\cos$ について解いた形を使う。$\\angle\\mathrm{{{R}}}$ の対辺は $\\mathrm{{{''.join(sorted(P + Q))}}}$。",
               steps=[f"$\\angle\\mathrm{{{R}}}$ をはさむ辺は $\\mathrm{{{''.join(sorted(Q + R))}}}={a}$、$\\mathrm{{{''.join(sorted(R + P))}}}={b}$、対辺は $\\mathrm{{{''.join(sorted(P + Q))}}}={c}$。",
                      f"$\\cos {R}=\\dfrac{{{a * a}+{b * b}-{c * c}}}{{{2 * a * b}}}={L(cosv)}$。", f"$0^\\circ<{R}<180^\\circ$ より ${R}={C}^\\circ$。"],
               alt=[f"最大辺 ${max(a, b, c)}$ の2乗と他の2辺の2乗の和を比べると、鋭角三角形か鈍角三角形かを先に判定でき、答えの見当がつく。"],
               pc=[("余弦定理に正しく代入している", 1), ("$\\cos$ の値から角を正しく求めている", 1)],
               pit=["対辺と、角をはさむ2辺を取り違える。", f"$\\cos {R}={L(cosv)}$ から角を ${180 - C}^\\circ$ と取り違える。"],
               chk=(f"acos(Rational({a * a + b * b - c * c},{2 * a * b}))*180/pi", str(C)))


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 5, ["application", "computation"])
def price_max(r):
    for _ in range(500):
        k = r.choice([2, 3, 4, 5, 6, 8, 10])
        p = r.choice(range(100, 410, 10))
        c = r.choice([0, 0, 50, 60, 80, 100])
        if c >= p:
            continue
        t = r.randint(2, 12)
        num10 = k * (p - c + 20 * t)
        if num10 % 10:
            continue
        N = num10 // 10
        if N - k * t <= 0 or N > 2000:
            continue
        break
    price = p + 10 * t
    sold = N - k * t
    val = (price - c) * sold
    what = "売上金額" if c == 0 else "利益"
    cost = "" if c == 0 else f"仕入れ値は1個 ${c}$ 円で、売れ残りは出ないものとする。"
    T = f"(({p}+10*x)-({c}))*({N}-{k}*x)"
    return sa(f"ある店で1個 ${p}$ 円で売っている商品は、1日に ${N}$ 個売れる。価格を $10$ 円上げるごとに、1日に売れる個数は ${k}$ 個ずつ減るとする。{cost}価格を $10x$ 円上げるとき、1日の{what}が最大になる価格と、そのときの{what}を求めなさい。ただし、$x$ は売れる個数が正となる範囲の0以上の整数とする。",
              f"価格 ${price}$ 円、{what} ${val}$ 円", f"{what} $y=({p - c}+10x)({N}-{k}x)$ は $x={t}$ で最大。", d=3,
              ap="数学化の3ステップ：変数（値上げ回数 $x$）、定義域（売れる個数が正）、目的の量（" + what + "）を $x$ の二次関数で表して平方完成する。",
              steps=[f"価格 ${p}+10x$ 円、売れる個数 ${N}-{k}x$ 個（${N}-{k}x>0$）。",
                     (f"{what} $y=({p}+10x)({N}-{k}x)$。" if c == 0 else f"{what} $y=({p}+10x-{c})({N}-{k}x)=({p - c}+10x)({N}-{k}x)$。"),
                     f"展開して $y={poly(-10 * k, 10 * N - k * (p - c), (p - c) * N)}$、軸 $x={t}$ は定義域内。",
                     f"$x={t}$ のとき最大。価格 ${price}$ 円、{what} ${val}$ 円。"],
              alt=[f"$y=({p - c}+10x)({N}-{k}x)=0$ となる $x$ は $x=-{fr(p - c, 10)},\\ {fr(N, k)}$。放物線の軸はその中点なので $x=\\dfrac{{1}}{{2}}\\left(-{fr(p - c, 10)}+{fr(N, k)}\\right)={t}$ と、展開せずに求められる。"],
              pc=[("価格と個数を $x$ で正しく表している", 1), ("目的の量を二次関数として正しく立式している", 1), ("最大となる価格と最大値を正しく答えている", 2)],
              pit=["答えを $x$ の値のまま書く（問われているのは価格）。", "利益を求めるのに仕入れ値を引き忘れる。" if c else "展開の計算で符号を誤る。"],
              chk=(f"[solve(diff({T}, x), x)[0], ({p}+10*{t}-({c}))*({N}-{k}*{t})]", f"[{t}, {val}]", None, "intermediate"))


@gen("standard_practice", 5, ["computation", "condition_check"])
def sine_law(r):
    A = r.choice([30, 45, 60, 120, 135, 150])
    kind = r.choice(["R", "side", "side2"])
    if kind == "side2" and A >= 150:
        kind = "R"
    sA = sp.sin(deg(A))
    if kind == "R":
        R = r.randint(2, 9)
        a = sp.nsimplify(2 * R * sA)
        stem = f"$\\triangle\\mathrm{{ABC}}$ において $\\mathrm{{BC}}={L(a)}$、$\\angle\\mathrm{{A}}={A}^\\circ$ である。$\\triangle\\mathrm{{ABC}}$ の外接円の半径 $R$ を求めなさい。"
        ans, ex, expv = str(R), f"({a})/(2*sin(deg({A})))", str(R)
        stp = [f"正弦定理 $\\dfrac{{\\mathrm{{BC}}}}{{\\sin A}}=2R$。", f"$\\sin{A}^\\circ={L(sA)}$。", f"$2R={L(a)}\\div{L(sA)}={2 * R}$ より $R={R}$。"]
    elif kind == "side":
        R = r.randint(2, 9)
        a = sp.nsimplify(2 * R * sA)
        stem = f"外接円の半径が ${R}$ の $\\triangle\\mathrm{{ABC}}$ で $\\angle\\mathrm{{A}}={A}^\\circ$ のとき、辺 $\\mathrm{{BC}}$ の長さを求めなさい。"
        ans, ex, expv = L(a), f"2*{R}*sin(deg({A}))", str(a)
        stp = [f"正弦定理 $\\mathrm{{BC}}=2R\\sin A$。", f"$\\mathrm{{BC}}=2\\cdot{R}\\cdot{L(sA)}={L(a)}$。"]
    else:
        B = r.choice([b for b in (30, 45, 60, 135, 120) if b + A < 180 and b != A])
        b = r.randint(2, 8)
        sB = sp.sin(deg(B))
        a = sp.nsimplify(sp.radsimp(b * sA / sB))
        stem = f"$\\triangle\\mathrm{{ABC}}$ において $\\mathrm{{CA}}={b}$、$\\angle\\mathrm{{A}}={A}^\\circ$、$\\angle\\mathrm{{B}}={B}^\\circ$ である。辺 $\\mathrm{{BC}}$ の長さを求めなさい。"
        ans, ex, expv = L(a), f"{b}*sin(deg({A}))/sin(deg({B}))", str(a)
        stp = [f"$\\dfrac{{\\mathrm{{BC}}}}{{\\sin A}}=\\dfrac{{\\mathrm{{CA}}}}{{\\sin B}}$（$\\mathrm{{BC}}$ は $\\angle\\mathrm{{A}}$ の対辺、$\\mathrm{{CA}}$ は $\\angle\\mathrm{{B}}$ の対辺）。",
               f"$\\mathrm{{BC}}=\\dfrac{{{b}\\sin{A}^\\circ}}{{\\sin{B}^\\circ}}={b}\\cdot{L(sA)}\\div{L(sB)}$。", f"$\\mathrm{{BC}}={L(a)}$。"]
    return sa(stem, f"${ans}$", "正弦定理 $\\dfrac{a}{\\sin A}=\\dfrac{b}{\\sin B}=2R$ を使う。", d=3,
              ap="与えられているのが「1辺とその対角」や外接円の半径なので、正弦定理を選ぶ。どの辺がどの角の対辺かを図で確かめてから代入する。",
              steps=stp,
              alt=["外接円の中心 O と弦 BC でつくる二等辺三角形で、中心角が $2A$（$A$ が鈍角なら $360^\\circ-2A$）になることから、余弦定理で $\\mathrm{BC}$ を確かめることもできる。"],
              pc=[("正弦定理を正しい対応で立式している", 2), ("三角比の値を代入して正しく計算している", 2)],
              pit=["対辺の対応を誤り、$\\dfrac{\\mathrm{BC}}{\\sin B}$ のように立式する。", "$\\sin" + str(A) + "^\\circ$ の値（鈍角の正弦は正）を誤る。"],
              chk=(ex, expv))


TRI_SET = [(5, 7, 8), (3, 5, 7), (5, 6, 7), (4, 5, 6), (2, 3, 4), (13, 14, 15), (5, 5, 6), (7, 8, 9), (6, 7, 8), (3, 7, 8), (4, 6, 8), (6, 8, 10), (5, 5, 8), (4, 13, 15)]


@gen("standard_practice", 5, ["computation", "application"])
def tri_area_r(r):
    a, b, c = r.choice(TRI_SET)
    kind = r.choice(["cos", "S", "r", "R"])
    s2 = sp.Rational(a + b + c, 2)
    S = sp.sqrt(s2 * (s2 - a) * (s2 - b) * (s2 - c))
    cosC = sp.Rational(a * a + b * b - c * c, 2 * a * b)
    sinC = sp.sqrt(1 - cosC ** 2)
    rin = sp.radsimp(2 * S / (a + b + c))
    Rc = sp.radsimp(sp.Rational(a * b * c, 4) / S)
    q = {"cos": ("$\\cos C$ の値", cosC, f"Rational({a * a + b * b - c * c},{2 * a * b})"),
         "S": ("面積 $S$", S, f"Rational(1,2)*{a}*{b}*sqrt(1-Rational({a * a + b * b - c * c},{2 * a * b})**2)"),
         "r": ("内接円の半径 $r$", rin, f"2*(Rational(1,2)*{a}*{b}*sqrt(1-Rational({a * a + b * b - c * c},{2 * a * b})**2))/({a + b + c})"),
         "R": ("外接円の半径 $R$", Rc, f"{c}/(2*sqrt(1-Rational({a * a + b * b - c * c},{2 * a * b})**2))")}[kind]
    stp = [f"余弦定理：$\\cos C=\\dfrac{{{a}^2+{b}^2-{c}^2}}{{2\\cdot{a}\\cdot{b}}}={L(cosC)}$。"]
    if kind != "cos":
        stp.append(f"$\\sin C=\\sqrt{{1-\\cos^2C}}={L(sinC)}$（$\\sin C>0$）。")
    if kind in ("S", "r"):
        stp.append(f"$S=\\dfrac{{1}}{{2}}\\cdot{a}\\cdot{b}\\cdot\\sin C={L(S)}$。")
    if kind == "r":
        stp.append(f"$S=\\dfrac{{1}}{{2}}r(a+b+c)$ より $r=\\dfrac{{2S}}{{{a + b + c}}}={L(rin)}$。")
    if kind == "R":
        stp.append(f"正弦定理 $\\dfrac{{c}}{{\\sin C}}=2R$ より $R=\\dfrac{{{c}}}{{2\\sin C}}={L(Rc)}$。")
    return sa(f"$\\triangle\\mathrm{{ABC}}$ において $a={a},\\ b={b},\\ c={c}$ である（$a=\\mathrm{{BC}},\\ b=\\mathrm{{CA}},\\ c=\\mathrm{{AB}}$）。{q[0]} を求めなさい。",
              f"${L(q[1])}$", "3辺 → 余弦定理で $\\cos$ → 相互関係で $\\sin$ → 面積・半径、の順に求める。", d=3,
              ap="3辺が与えられたら、まず1つの角の余弦を余弦定理で求める。そこから $\\sin$、面積、内接円・外接円の半径へと「一本道」で進める。",
              steps=stp,
              alt=[f"面積はヘロンの公式 $S=\\sqrt{{s(s-a)(s-b)(s-c)}}$（$s={L(s2)}$）でも求められ、$S={L(S)}$ と一致することで検算できる。"],
              pc=[("余弦定理で $\\cos C$ を正しく求めている", 2), ("目的の量まで正しく計算している", 2)],
              pit=["$\\sin C$ を求めるとき根号を外し忘れる、または負の値をとる。", "内接円の公式で $S=r(a+b+c)$ と $\\dfrac{1}{2}$ を落とす。"],
              chk=(q[2], str(q[1])))


@gen("standard_practice", 5, ["application", "computation"])
def tower_height(r):
    al, be = r.choice([(30, 60), (30, 45), (45, 60)])
    d = r.choice([10, 12, 18, 20, 24, 30, 36, 40, 50, 60])
    e = r.choice([0, 0, 2])
    h = sp.radsimp(d * sp.tan(deg(al)) * sp.tan(deg(be)) / (sp.tan(deg(be)) - sp.tan(deg(al))))
    H = sp.nsimplify(sp.expand(h + e))
    HT = f"({L(H)})" if isinstance(H, sp.Add) else L(H)
    eye = "" if e == 0 else f"仰角は地面からの高さ ${e}\\,\\mathrm{{m}}$ に置いた測量器で測ったものとする。"
    return sa(f"平らな地面に垂直に立つ電波塔の頂上 $\\mathrm{{P}}$ を、地点 $\\mathrm{{A}}$ から見上げた仰角は ${al}^\\circ$ であった。電波塔に向かってまっすぐ ${d}\\,\\mathrm{{m}}$ 進んだ地点 $\\mathrm{{B}}$ から見上げた仰角は ${be}^\\circ$ であった。{eye}電波塔の高さを求めなさい。",
              f"${HT}\\,\\mathrm{{m}}$", f"測量器の位置からの高さを $h$ とすると $\\dfrac{{h}}{{\\tan{al}^\\circ}}-\\dfrac{{h}}{{\\tan{be}^\\circ}}={d}$。", d=3,
              ap="高さを $h$ とおき、2地点から塔の根元までの水平距離を $h$ と $\\tan$ で表す。その差が進んだ距離になる。",
              steps=[f"水平距離は $\\mathrm{{A}}$ から $\\dfrac{{h}}{{\\tan{al}^\\circ}}$、$\\mathrm{{B}}$ から $\\dfrac{{h}}{{\\tan{be}^\\circ}}$。",
                     f"$h\\left(\\dfrac{{1}}{{\\tan{al}^\\circ}}-\\dfrac{{1}}{{\\tan{be}^\\circ}}\\right)={d}$ を解いて $h={L(h)}$。"]
              + ([f"測量器の高さ ${e}\\,\\mathrm{{m}}$ を加えて ${HT}\\,\\mathrm{{m}}$。"] if e else []),
              alt=[f"$\\triangle\\mathrm{{ABP}}$ で $\\angle\\mathrm{{APB}}={be - al}^\\circ$ なので、正弦定理 $\\dfrac{{\\mathrm{{BP}}}}{{\\sin{al}^\\circ}}=\\dfrac{{{d}}}{{\\sin{be - al}^\\circ}}$ から $\\mathrm{{BP}}$ を求め、$h=\\mathrm{{BP}}\\sin{be}^\\circ$ としても同じ値になる。"],
              pc=[("水平距離を高さで正しく表している", 1), ("方程式を立てて正しく解いている", 2), ("有理化・測量器の高さを含めて正しく答えている", 1)],
              pit=["$\\tan$ と $\\dfrac{1}{\\tan}$ を取り違えて、水平距離を $h\\tan\\alpha$ とする。"] + (["測量器の高さを加え忘れる。"] if e else ["分母の有理化を忘れる。"]),
              chk=(f"{d}*tan(deg({al}))*tan(deg({be}))/(tan(deg({be}))-tan(deg({al})))+{e}", str(H)))


# ======================================================================
# C 思考力・記述応用
# ======================================================================

@gen("thinking_writing", 3, ["written_reasoning", "condition_check"])
def moving_interval(r):
    p = r.randint(-2, 4)
    q = r.randint(-3, 6)
    w = r.choice([1, 2, 3, 4])
    a = sp.Symbol("a")
    f = lambda t: sp.expand((t - p) ** 2 + q)  # noqa: E731
    left, right = f(a + w), f(a)
    b1 = p - w
    return desc(f"$a$ を定数とする。関数 $f(x)={poly(1, -2 * p, p * p + q)}$ の $a\\leqq x\\leqq a+{w}$ における最小値 $m(a)$ を、$a$ の値の範囲で場合分けして求めなさい。",
                f"$a<{b1}$ のとき $m(a)={sp.latex(left)}$、${b1}\\leqq a\\leqq{p}$ のとき $m(a)={q}$、${p}<a$ のとき $m(a)={sp.latex(right)}$",
                f"$f(x)=(x{cst(-p) if p else ''})^2{cst(q)}$、軸 $x={p}$ と区間 $[a,\\,a+{w}]$ の位置関係で3つに分ける。" if p else f"$f(x)=x^2{cst(q)}$、軸 $x=0$ と区間の位置関係で3つに分ける。",
                rubric=[("平方完成して軸を求めている", 1), ("軸が区間の右・中・左にある3つの場合に、境界を正しく分けている", 3),
                        ("各場合の最小値を正しく求めている", 3), ("結論を整理して答えている", 1)], d=4, p=8, lines=10,
                ap="区間が動くので、「軸が区間の右にある／区間内にある／区間の左にある」の3通りで最小値をとる点が変わる。条件を $a$ の不等式で書く。",
                steps=[f"軸は $x={p}$。", f"(i) $a+{w}<{p}$ すなわち $a<{b1}$：区間で減少、$m(a)=f(a+{w})={sp.latex(left)}$。",
                       f"(ii) $a\\leqq{p}\\leqq a+{w}$ すなわち ${b1}\\leqq a\\leqq{p}$：$m(a)=f({p})={q}$。", f"(iii) ${p}<a$：区間で増加、$m(a)=f(a)={sp.latex(right)}$。"],
                alt=[f"検算：境界 $a={b1}$ で (i) の式の値は ${left.subs(a, b1)}$、$a={p}$ で (iii) の式の値は ${right.subs(a, p)}$ となり、どちらも (ii) の ${q}$ と一致する。$m(a)$ が境界でつながることを確かめられる。"],
                pc=[("軸の確認", 1), ("場合分けの境界", 3), ("各場合の最小値", 3), ("結論", 1)],
                pit=["(i) で $f(a)$ を答える（軸が区間の右にあるとき、軸に近いのは右端 $a+" + str(w) + "$）。", "境界 $a=" + str(b1) + "$、$a=" + str(p) + "$ をどの場合にも入れない。"],
                chk=(f"[expand((a+{w}-({p}))**2+({q})), expand((a-({p}))**2+({q}))]", f"[{left}, {right}]", "expand", "intermediate"))


@gen("thinking_writing", 3, ["cross_unit", "written_reasoning"], rel=["HS-MATH1-U03", "HS-MATH1-U04"])
def bc_min(r):
    A = r.choice([60, 90, 120])
    Lt = r.choice([2, 4, 6, 8, 10, 12, 14, 16])
    x = sp.Symbol("x")
    cA = sp.cos(deg(A))
    bc2 = sp.expand(x ** 2 + (Lt - x) ** 2 - 2 * x * (Lt - x) * cA)
    mn2 = bc2.subs(x, sp.Rational(Lt, 2))
    mn = sp.sqrt(mn2)
    return desc(f"$\\triangle\\mathrm{{ABC}}$ は $\\mathrm{{AB}}+\\mathrm{{AC}}={Lt}$、$\\angle\\mathrm{{A}}={A}^\\circ$ を満たしながら形を変える。$\\mathrm{{AB}}=x$ とおくとき、辺 $\\mathrm{{BC}}$ の長さの最小値と、そのときの $x$ の値を求めなさい。考え方を説明しながら答えること。",
                f"$x={fr(Lt, 2)}$ のとき、$\\mathrm{{BC}}$ の最小値 ${L(mn)}$",
                f"余弦定理より $\\mathrm{{BC}}^2={sp.latex(bc2)}$（$0<x<{Lt}$）。平方完成して最小値を求め、最後に正の平方根をとる。",
                rubric=[("余弦定理で $\\mathrm{BC}^2$ を $x$ の式で表している", 3), ("$x$ の変域 $0<x<" + str(Lt) + "$ を明示している", 1),
                        ("平方完成して $\\mathrm{BC}^2$ の最小値を求めている", 3), ("$\\mathrm{BC}>0$ から平方根をとって答えている", 1)], d=4, p=8, lines=10,
                ap="辺の長さは根号を含むので、2乗した $\\mathrm{BC}^2$ を $x$ の二次関数として扱う（$\\mathrm{BC}>0$ なので、$\\mathrm{BC}$ が最小 ⇔ $\\mathrm{BC}^2$ が最小）。",
                steps=[f"$\\mathrm{{AC}}={Lt}-x$、辺の長さは正なので $0<x<{Lt}$。",
                       f"余弦定理：$\\mathrm{{BC}}^2=x^2+({Lt}-x)^2-2x({Lt}-x)\\cos{A}^\\circ={sp.latex(bc2)}$。",
                       f"平方完成すると軸は $x={fr(Lt, 2)}$ で定義域内。最小値 $\\mathrm{{BC}}^2={L(mn2)}$。",
                       f"$\\mathrm{{BC}}>0$ より最小値 $\\mathrm{{BC}}={L(mn)}$（$x={fr(Lt, 2)}$）。"],
                alt=[f"$\\mathrm{{BC}}^2$ は $x$ と ${Lt}-x$ を入れかえても変わらない（対称）ので、軸は $x={fr(Lt, 2)}$ と予想でき、平方完成の結果を検算できる。"],
                pc=[("余弦定理による立式", 3), ("変域の明示", 1), ("平方完成と最小値", 3), ("平方根をとった結論", 1)],
                pit=["$\\cos" + str(A) + "^\\circ$ の値や符号を誤る。", "$\\mathrm{BC}^2$ の最小値をそのまま $\\mathrm{BC}$ の最小値として答える。"],
                chk=(f"sqrt(Rational({Lt},2)**2*2-2*Rational({Lt},2)**2*cos(deg({A})))", str(mn), None, "intermediate"))


@gen("thinking_writing", 2, ["cross_unit", "condition_check"], rel=["HS-MATH1-U02"])
def nec_suf(r):
    a = r.randint(-3, 6)
    b = r.randint(1, 4)
    P0, P1 = a - b, a + b
    rel = r.choice(["eq", "PinQ", "QinP", "none"])
    if rel == "eq":
        m, n = P0, P1
    elif rel == "PinQ":
        m, n = P0 - r.randint(0, 2), P1 + r.randint(1, 2)
    elif rel == "QinP":
        m, n = P0 + r.randint(0, 1), P1 - r.randint(1, b)
        if m >= n:
            m, n = P0, P1 - 1
    else:
        sh = r.choice([-1, 1]) * r.randint(1, 2 * b - 1)
        m, n = P0 + sh, P1 + sh
    choices = {"eq": "必要十分条件である", "PinQ": "十分条件であるが、必要条件ではない", "QinP": "必要条件であるが、十分条件ではない", "none": "必要条件でも十分条件でもない"}
    right = choices[rel]
    wrong = [v for k, v in choices.items() if k != rel]
    reason = {"必要十分条件である": ("$P=Q$ のときに限り必要十分条件。ここでは2つの区間が一致しない。", "区間の比較の誤り"),
              "十分条件であるが、必要条件ではない": ("$p\\Rightarrow q$ が真になるのは $P\\subset Q$ のとき。ここでは $P$ が $Q$ に含まれない（または逆向きも成り立つ）。", "包含関係の向きの取り違え"),
              "必要条件であるが、十分条件ではない": ("$q\\Rightarrow p$ だけが真になるのは $Q\\subset P$（$Q\\neq P$）のとき。ここではそうなっていない。", "包含関係の向きの取り違え"),
              "必要条件でも十分条件でもない": ("$P,\\ Q$ の一方が他方に含まれているので、少なくとも一方の命題は真である。", "反例の探し方の誤り")}
    Pq = f"{poly(1, -(m + n), m * n)}\\leqq0"
    inner = f"x{'-' if a > 0 else '+'}{abs(a)}" if a else "x"
    return mc(f"実数 $x$ に関する2つの条件 $p:\\ |{inner}|\\leqq{b}$、$q:\\ {Pq}$ について、$p$ は $q$ であるための何か。正しいものを選びなさい。",
              [right] + wrong, f"$p$ の表す集合 $P$ は ${P0}\\leqq x\\leqq{P1}$、$q$ の表す集合 $Q$ は ${m}\\leqq x\\leqq{n}$。", d=4, p=8, keep=True,
              ap="条件を、それを満たす $x$ の集合（区間）で表す。$p\\Rightarrow q$ が真 ⇔ $P\\subset Q$。数直線に2つの区間をかいて包含関係を見る。",
              steps=[f"$|{inner}|\\leqq{b}$ ⇔ $-{b}\\leqq {inner}\\leqq{b}$ ⇔ ${P0}\\leqq x\\leqq{P1}$。",
                     f"${Pq}$ ⇔ $(x{cst(-m) if m else ''})(x{cst(-n) if n else ''})\\leqq0$ ⇔ ${m}\\leqq x\\leqq{n}$。",
                     f"$P$ と $Q$ を比べると、{ {'eq': '$P=Q$ である', 'PinQ': '$P$ は $Q$ に含まれ、$P\\neq Q$ である', 'QinP': '$Q$ は $P$ に含まれ、$Q\\neq P$ である', 'none': 'どちらも他方に含まれない'}[rel]}。", f"よって「{right}」。"],
              alt=["反例を探す方法：$p$ を満たすが $q$ を満たさない $x$（$p\\Rightarrow q$ の反例）と、その逆の反例が存在するかを、区間の端の近くの値で調べる。"],
              pc=[("2つの条件を区間で表している", 4), ("包含関係から正しく判定している", 4)],
              pit=["$p\\Rightarrow q$ が真のとき「$p$ は $q$ の必要条件」と、必要・十分を逆に覚えている。", "区間の端点（等号を含むか）を確認せずに包含関係を判断する。"],
              why={w: reason[w] for w in wrong},
              chk=(f"solve(x**2-({m + n})*x+({m * n}), x)", f"[{m}, {n}]" if m != n else f"[{m}]", "set", "intermediate"))


@gen("thinking_writing", 2, ["written_reasoning", "condition_check"])
def root_place(r):
    for _ in range(200):
        t = r.randint(2, 6)
        k = r.choice([0, 1, 1, 2, 2, 3])
        c = t * (t - 1)
        lo = max(t, k)
        if k == 0:
            U = None
            break
        U = sp.Rational(k * k + c, 2 * k - 1)
        if U > lo:
            break
    where = "ともに正となる" if k == 0 else f"ともに ${k}$ より大きくなる"
    fk = "f(0)=m+" + str(c) + ">0" if k == 0 else f"f({k})={k * k + c}-{2 * k - 1}m>0" if k > 1 else f"f(1)={1 + c}-m>0"
    ans = f"$m>{lo}$" if U is None else f"${lo}<m<{L(U)}$"
    return desc(f"$x$ の2次方程式 $x^2-2mx+m+{c}=0$ が、異なる2つの実数解をもち、それらが{where}ような定数 $m$ の値の範囲を求めなさい。グラフを用いて、必要な条件を説明すること。",
                ans, f"$f(x)=x^2-2mx+m+{c}$ とおき、判別式・軸・境界での値の3条件を連立する。", d=4, p=8, lines=10,
                rubric=[("判別式・軸の位置・端の値の3条件を挙げ、その理由をグラフで説明している", 3), ("判別式の条件を正しく解いている", 2),
                        ("3条件の共通部分を正しく求めている", 2), ("結論を正しく書いている", 1)],
                ap=f"解の配置の問題は、$y=f(x)$ のグラフ（下に凸）が $x$ 軸の{('正の部分' if k == 0 else f' $x>{k}$ の部分')}と異なる2点で交わる条件に読みかえる。①判別式 $D>0$ ②軸の位置 ③境界での $f$ の値の符号、の3つで決まる。",
                steps=[f"$\\dfrac{{D}}{{4}}=m^2-m-{c}=(m-{t})(m+{t - 1})>0$ より $m<-{t - 1},\\ {t}<m$。",
                       f"軸 $x=m$ が {('$x>0$' if k == 0 else f'$x>{k}$')} の範囲にある：$m>{k}$。",
                       f"${fk}$" + (f"（$m>{t}$ ならつねに成り立つ）。" if k == 0 else f" より $m<{L(U)}$。"),
                       f"共通部分は {ans}。"],
                alt=["解と係数の関係を使う方法：2解を $\\alpha,\\ \\beta$ とし、" + ("$\\alpha+\\beta>0$、$\\alpha\\beta>0$ と $D>0$ を連立しても同じ結論になる。" if k == 0 else f"$(\\alpha-{k})+(\\beta-{k})>0$、$(\\alpha-{k})(\\beta-{k})>0$ と $D>0$ を連立しても同じ結論になる（数学Ⅱ）。")],
                pc=[("3条件の提示と説明", 3), ("判別式の処理", 2), ("共通部分", 2), ("結論", 1)],
                pit=["軸の条件を書き忘れ、2解がともに境界より小さい場合を含めてしまう。", "$D\\geqq0$ として重解を含めてしまう（「異なる2つの実数解」に反する）。"],
                chk=(f"solve(m**2-m-{c}, m)", f"[{t}, {1 - t}]", "set", "intermediate"))


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(stem, wrong, step, etype, tempt, fix, ans, expl, steps, ap, alt, pit, chk=None, d=3):
    return desc(f"{stem}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい答えを求めなさい。", ans, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい解答を途中式とともに示している", 3), ("最終的な答えが正しい", 1)], d=d, p=6, lines=6,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい途中式", 3), ("正しい答え", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix), chk=chk)


@gen("error_correction", 3, ["common_error", "condition_check"])
def err_sqrt_abs(r):
    q = r.choice([-5, -4, -3, -2, -1, 1, 2])
    p = q + r.randint(3, 8)
    if p == 0:
        p += 1
    a0 = r.randint(q + 1, p - 1)
    e1 = poly(1, -2 * p, p * p, var="a")
    e2 = poly(1, -2 * q, q * q, var="a")
    wrong = f"$\\sqrt{{{e1}}}+\\sqrt{{{e2}}}=\\sqrt{{(a{cst(-p)})^2}}+\\sqrt{{(a{cst(-q) if q else ''})^2}}=(a{cst(-p)})+(a{cst(-q) if q else ''})=2a{cst(-(p + q)) if p + q else ''}$"
    fix = f"$\\sqrt{{(a{cst(-p)})^2}}=|a{cst(-p)}|={p}-a$、$\\sqrt{{(a{cst(-q) if q else ''})^2}}=|a{cst(-q) if q else ''}|=a{cst(-q) if q else ''}$ より、和は ${p - q}$"
    return err_item(f"${q}<a<{p}$ のとき、$P=\\sqrt{{{e1}}}+\\sqrt{{{e2}}}$ を簡単にしなさい。", wrong, "根号を外す部分（$\\sqrt{A^2}=A$ としたところ）", "sign",
                    "$\\sqrt{x^2}=x$ は $x\\geqq0$ のときにだけ正しいが、文字式になると符号を確かめずに機械的に外しやすい。",
                    fix, f"$P={p - q}$", f"$\\sqrt{{A^2}}=|A|$。$a<{p}$ なので $a-{p}<0$、$a>{q}$ なので $a{cst(-q) if q else ''}>0$。",
                    [f"$\\sqrt{{{e1}}}=|a{cst(-p)}|$、$\\sqrt{{{e2}}}=|a{cst(-q) if q else ''}|$。", f"${q}<a<{p}$ より $a{cst(-p)}<0$、$a{cst(-q) if q else ''}>0$。",
                     f"$P=-(a{cst(-p)})+(a{cst(-q) if q else ''})={p - q}$。"],
                    "根号の中が完全平方式なら $\\sqrt{A^2}=|A|$ として絶対値をつけ、条件から $A$ の符号を判定してから外す。",
                    [f"範囲内の値 $a={a0}$ を代入して確かめる：$P=|{a0 - p}|+|{a0 - q}|={p - q}$。生徒の式では $2\\cdot{a0}{cst(-(p + q)) if p + q else ''}={2 * a0 - p - q}$ となり一致しない。"],
                    ["$\\sqrt{A^2}=A$ と、絶対値をつけずに外す。"],
                    chk=(f"sqrt(({a0}-({p}))**2)+sqrt(({a0}-({q}))**2)", str(p - q), None, "intermediate"), d=2)


@gen("error_correction", 3, ["common_error", "condition_check"])
def err_obtuse(r):
    a, b, c = r.choice(TRIPLES)
    if r.random() < 0.5:
        a, b = b, a
    wrong = f"$\\cos^2\\theta=1-\\left({fr(a, c)}\\right)^2={fr(b * b, c * c)}$ より $\\cos\\theta={fr(b, c)}$、$\\tan\\theta={fr(a, b)}$"
    fix = f"$\\cos\\theta=\\pm{fr(b, c)}$。$\\theta$ が鋭角なら $\\cos\\theta={fr(b, c)},\\ \\tan\\theta={fr(a, b)}$、鈍角なら $\\cos\\theta={fr(-b, c)},\\ \\tan\\theta={fr(-a, b)}$"
    return err_item(f"$0^\\circ\\leqq\\theta\\leqq180^\\circ$ で $\\sin\\theta={fr(a, c)}$ のとき、$\\cos\\theta$ と $\\tan\\theta$ の値を求めなさい。", wrong,
                    "$\\cos^2\\theta$ から $\\cos\\theta$ を求めた部分（正の値だけをとった）", "condition",
                    "鋭角の三角比に慣れているため、$\\sin\\theta>0$ の角が鈍角でもありうることを忘れ、正の平方根だけをとってしまう。",
                    fix, f"$\\cos\\theta={fr(b, c)},\\ \\tan\\theta={fr(a, b)}$ または $\\cos\\theta={fr(-b, c)},\\ \\tan\\theta={fr(-a, b)}$",
                    f"$0^\\circ\\leqq\\theta\\leqq180^\\circ$ で $\\sin\\theta={fr(a, c)}$ を満たす $\\theta$ は、鋭角と鈍角の2つある。",
                    [f"$\\cos^2\\theta={fr(b * b, c * c)}$ より $\\cos\\theta=\\pm{fr(b, c)}$。", f"$\\cos\\theta={fr(b, c)}$ のとき $\\tan\\theta={fr(a, b)}$。",
                     f"$\\cos\\theta={fr(-b, c)}$ のとき $\\tan\\theta={fr(-a, b)}$。"],
                    "角の範囲が $0^\\circ\\leqq\\theta\\leqq180^\\circ$ なら、$\\sin\\theta$ の値1つに対して $\\theta$ は2つありうる。単位円で $y$ 座標が等しい2点を確認する。",
                    [f"単位円上で $y={fr(a, c)}$ となる点は第1象限と第2象限に1つずつあり、$x$ 座標は $\\pm{fr(b, c)}$ である。図をかけば2通りあることが一目で分かる。"],
                    ["角の範囲を確かめずに $\\cos\\theta>0$ とする。"],
                    chk=(f"solve(x**2-(1-Rational({a},{c})**2), x)", f"[Rational({b},{c}), Rational({-b},{c})]", "set", "intermediate"))


@gen("error_correction", 2, ["common_error", "application"])
def err_domain(r):
    for _ in range(300):
        k = r.choice([1, 2, 4, 5])
        v = r.choice(range(150, 401, 10))
        N = 2 * k * v
        hi = v - r.choice([20, 30, 40, 50, 60, 80])
        lo = hi - r.choice([50, 60, 80, 100])
        if lo > 0:
            break
    R = lambda x: x * (N - k * x)  # noqa: E731
    wrong = f"$y=x({N}-{k}x)={'-' if k == 1 else f'-{k}'}(x-{v})^2+{R(v)}$ より、$x={v}$ のとき最大で、売上金額は ${R(v)}$ 円"
    fix = f"軸 $x={v}$ は定義域 ${lo}\\leqq x\\leqq{hi}$ の右外にあるので、定義域で $y$ は増加する。$x={hi}$ のとき最大で ${R(hi)}$ 円"
    return err_item(f"ある商品を1個 $x$ 円で売ると、1日に $({N}-{k}x)$ 個売れることが分かっている。ただし、仕入れ先との取り決めにより、価格は ${lo}\\leqq x\\leqq{hi}$ の範囲で決めなければならない。1日の売上金額 $y$ 円が最大となる価格と、そのときの売上金額を求めなさい。",
                    wrong, "最大値の判断（軸が定義域の外にあることを確かめていない）", "condition",
                    "「売上の最大＝頂点」という型に慣れていると、問題文の途中にある定義域の条件を読み落としやすい。共通テストでは条件が文章の中に埋め込まれる。",
                    fix, f"価格 ${hi}$ 円、売上金額 ${R(hi)}$ 円",
                    f"$y=-{k if k > 1 else ''}(x-{v})^2+{R(v)}$、上に凸で軸 $x={v}>{hi}$。",
                    [f"平方完成：$y={'-' if k == 1 else f'-{k}'}(x-{v})^2+{R(v)}$、軸 $x={v}$。", f"定義域 ${lo}\\leqq x\\leqq{hi}$ は軸の左側にあり、$y$ は増加する。", f"$x={hi}$ で最大値 ${hi}\\times{N - k * hi}={R(hi)}$。"],
                    "数学化の3ステップの②（定義域）を、立式の前に必ず書き出す。",
                    [f"定義域の両端の値 $y({lo})={R(lo)}$、$y({hi})={R(hi)}$ を計算して比べても、右端で最大と確かめられる。"],
                    ["頂点の $x$ 座標が定義域に入っているかを確かめない。"],
                    chk=(f"Max({lo}*({N}-{k}*{lo}), {hi}*({N}-{k}*{hi}))", str(R(hi)), None, "intermediate"))


@gen("error_correction", 2, ["common_error", "computation"])
def err_cos_sign(r):
    tri = r.choice([t for t in ANG_TRI])
    b, c, a, A = tri
    if r.random() < 0.5:
        b, c = c, b
    cA = sp.Rational(1, 2) if A == 60 else sp.Rational(-1, 2)
    wsq = b * b + c * c - 2 * b * c * (-cA)
    wrong_val = sp.sqrt(wsq)
    wrong = (f"$a^2={b}^2+{c}^2-2\\cdot{b}\\cdot{c}\\cos{A}^\\circ={b * b}+{c * c}-{b * c}={wsq}$ より $a={L(wrong_val)}$" if A == 120
             else f"$a^2={b}^2+{c}^2-2\\cdot{b}\\cdot{c}\\cos{A}^\\circ={b * b}+{c * c}+{b * c}={wsq}$ より $a={L(wrong_val)}$")
    fix = f"$\\cos{A}^\\circ={L(cA)}$ なので $a^2={b * b}+{c * c}{'+' if A == 120 else '-'}{b * c}={a * a}$、$a={a}$"
    return err_item(f"$\\triangle\\mathrm{{ABC}}$ において $b={b},\\ c={c},\\ A={A}^\\circ$ のとき、$a$ を求めなさい。", wrong,
                    f"$\\cos{A}^\\circ$ の値を代入した部分（符号）", "sign",
                    "$\\cos120^\\circ=-\\dfrac{1}{2}$ と $\\cos60^\\circ=\\dfrac{1}{2}$ を取り違えたり、$-2bc\\cos A$ の符号と $\\cos A$ の符号を二重に処理したりしやすい。",
                    fix, f"$a={a}$", f"$\\cos{A}^\\circ={L(cA)}$ を代入すると、$-2bc\\cos A={'+' if A == 120 else '-'}{b * c}$。",
                    [f"$a^2=b^2+c^2-2bc\\cos A$。", f"$\\cos{A}^\\circ={L(cA)}$ を代入：$-2\\cdot{b}\\cdot{c}\\cdot\\left({L(cA)}\\right)={'+' if A == 120 else '-'}{b * c}$。", f"$a^2={a * a}$、$a>0$ より $a={a}$。"],
                    "余弦定理では、$\\cos A$ の値をかっこごと代入し、符号の処理を1回で行う。",
                    [f"角 $A$ が{'鈍角' if A == 120 else '鋭角'}なので、$a^2$ は $b^2+c^2={b * b + c * c}$ より{'大きく' if A == 120 else '小さく'}なるはずである。生徒の値 ${wsq}$ はこれに反するので誤りに気づける。"],
                    ["$\\cos" + str(A) + "^\\circ$ の符号を誤る。"],
                    chk=(f"sqrt({b}**2+{c}**2-2*{b}*{c}*cos(deg({A})))", str(a), None, "intermediate"))


GENERATORS = [abs_int_count, sym_expr, trig_obtuse, cos_law_angle,
              price_max, sine_law, tri_area_r, tower_height,
              moving_interval, bc_min, nec_suf, root_place,
              err_sqrt_abs, err_obtuse, err_domain, err_cos_sign]
