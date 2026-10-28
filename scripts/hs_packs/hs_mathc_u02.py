"""単元パック：数学C 平面上の曲線と複素数平面（二次曲線・媒介変数表示・極形式・ド・モアブルの定理）。"""
from fractions import Fraction

import sympy as sp

from banks._common import desc, figure, mc, plane, sa
from hs_pack_lib import (board, check, definition, derivation, example, fr_py, frac, gen, guide, intro, lesson, nonzero,
                         summary, theorem, tp)

UNIT_ID = "HS-MATHC-U02"


# ----------------------------------------------------------------------
# 補助
# ----------------------------------------------------------------------

def atex(f):
    """π の有理数倍 f（Fraction）の LaTeX。"""
    f = Fraction(f)
    if f == 0:
        return "0"
    s = "-" if f < 0 else ""
    f = abs(f)
    n, d = f.numerator, f.denominator
    if d == 1:
        return s + ("\\pi" if n == 1 else f"{n}\\pi")
    if n == 1:
        return s + f"\\dfrac{{\\pi}}{{{d}}}"
    return s + f"\\dfrac{{{n}}}{{{d}}}\\pi"


def apy(f):
    f = Fraction(f)
    return f"pi*Rational({f.numerator},{f.denominator})"


def norm_arg(f):
    """偏角を 0 以上 2 未満（π 単位）に直す。"""
    f = Fraction(f) % 2
    return f


def polar_tex(r, f):
    """r(cos θ + i sin θ) の LaTeX（r は sympy の式）。"""
    A = atex(f)
    if Fraction(f) < 0:
        A = f"\\left({A}\\right)"
    head = "" if r == 1 else sp.latex(r)
    return f"{head}\\left(\\cos {A}+i\\sin {A}\\right)"


def ctex(z):
    """複素数 z（sympy）の a+bi 形の LaTeX。"""
    z = sp.nsimplify(sp.expand(z))
    re, im = sp.nsimplify(sp.re(z)), sp.nsimplify(sp.im(z))
    if im == 0:
        return sp.latex(re)
    neg = bool(im < 0)
    mag = -im if neg else im
    if mag == 1:
        mt = ""
    elif isinstance(mag, sp.Add):
        mt = f"\\left({sp.latex(mag)}\\right)"
    else:
        mt = sp.latex(mag)
    term = mt + "i"
    if re == 0:
        return ("-" if neg else "") + term
    return sp.latex(re) + ("-" if neg else "+") + term


def cpy(z):
    return sp.sstr(sp.nsimplify(sp.expand(z)))


def zval(r, f):
    return sp.nsimplify(sp.expand(r * (sp.cos(sp.pi * sp.Rational(f.numerator, f.denominator)) + sp.I * sp.sin(sp.pi * sp.Rational(f.numerator, f.denominator)))))


def nice_point(r):
    """極形式・a+bi 形の両方がきれいな複素数 (r, 偏角/π)。"""
    kind = r.choice(["six", "six", "four", "axis"])
    if kind == "six":
        f = Fraction(r.choice([1, 2, 4, 5, 7, 8, 10, 11]), 6)
        mod = 2 * r.randint(1, 3)
    elif kind == "four":
        f = Fraction(r.choice([1, 3, 5, 7]), 4)
        mod = r.randint(1, 3) * sp.sqrt(2)
    else:
        f = Fraction(r.choice([0, 1, 2, 3]), 2)
        mod = r.randint(1, 5)
    return sp.nsimplify(mod), f


def sqfrac(var, d):
    """var^2/d の LaTeX（d=1 なら var^2）。"""
    return f"{var}^2" if d == 1 else f"\\dfrac{{{var}^2}}{{{d}}}"


def sq_tex(n):
    return sp.latex(sp.sqrt(n))


def shift_sq(var, p):
    if p == 0:
        return f"{var}^2"
    return f"({var}{'-' if p > 0 else '+'}{abs(p)})^2"


def lin_tex(c, p, var="t"):
    """c*var+p の LaTeX。"""
    head = ("" if c == 1 else ("-" if c == -1 else str(c))) + var
    return head + ("" if p == 0 else (f"+{p}" if p > 0 else f"{p}"))


COS_TEX = {Fraction(1, 3): "\\dfrac{1}{2}", Fraction(1, 2): "0", Fraction(2, 3): "-\\dfrac{1}{2}"}


LESSON = lesson(
    goals=["放物線・楕円・双曲線を「距離の条件」で定義し、標準形から焦点・準線・漸近線などを読み取れる。",
           "媒介変数表示された曲線を、媒介変数を消去したり $x,\\ y$ の範囲を調べたりして、方程式と結びつけられる。",
           "複素数を極形式で表し、積・商・累乗（ド・モアブルの定理）を回転と拡大の言葉で説明し、方程式 $z^n=w$ を解ける。"],
    duration=100,
    readiness=["2点間の距離の公式と円の方程式（数学Ⅱ）を使える。", "複素数の四則計算と $i^2=-1$（数学Ⅱ）を使える。",
               "三角関数の加法定理と、$\\dfrac{\\pi}{6},\\ \\dfrac{\\pi}{4},\\ \\dfrac{\\pi}{3}$ などの三角関数の値（数学Ⅱ）を使える。"],
    flow=[("導入：円錐の切り口と距離の条件", 10, "円錐を平面で切った断面の図で、円・楕円・放物線・双曲線を紹介する"),
          ("二次曲線の定義と標準形", 30, "放物線・楕円・双曲線を定義し、楕円の方程式を導出。例題1で焦点を求める"),
          ("媒介変数表示", 15, "円・楕円の媒介変数表示とサイクロイドを扱い、例題2で媒介変数を消去する"),
          ("複素数平面と極形式", 25, "複素数を点として表し、極形式・積と商の図形的意味（回転と拡大）を確認する"),
          ("ド・モアブルの定理", 15, "数学的帰納法で証明し、例題3・4で累乗と $z^n=w$ を扱う"),
          ("まとめと確認", 5, "確認問題3問、問題プリントA の課題指示")],
    sections=[
        intro("in1", "曲線を「条件」で定める",
              "円は「定点からの距離が一定な点の集合」として定義された。同じように、距離についての条件を変えると、放物線・楕円・双曲線という3種類の曲線が得られる。これらは、円錐を平面で切ったときの切り口として現れることから円錐曲線ともよばれ、方程式が $x,\\ y$ の2次式で表されるので二次曲線ともいう。",
              bullets=["放物線：定点（焦点）と定直線（準線）からの距離が等しい点の軌跡。", "楕円：2定点（焦点）からの距離の和が一定な点の軌跡。",
                       "双曲線：2定点（焦点）からの距離の差が一定（$0$ でない）な点の軌跡。"],
              points=[tp("糸の両端を2本のピンで留め、鉛筆で糸を張りながら楕円をかく実演をすると、「距離の和が一定」が体感できる。", ask="鉛筆の先から2本のピンまでの距離の和は、動かしても変わらないか。", expect="糸の長さが一定なので変わらない。", timing="導入の冒頭")]),
        definition("df1", "二次曲線の標準形",
                   "焦点を $x$ 軸上（放物線は $x$ 軸上の1点）にとると、それぞれの曲線は次の標準形で表される。",
                   formula="$$y^2=4px\\ \\ (\\text{焦点 }(p,\\,0),\\ \\text{準線 }x=-p),\\qquad \\dfrac{x^2}{a^2}+\\dfrac{y^2}{b^2}=1\\ \\ (a>b>0),\\qquad \\dfrac{x^2}{a^2}-\\dfrac{y^2}{b^2}=1\\ \\ (a>0,\\ b>0)$$",
                   conditions=["楕円（$a>b>0$）の焦点は $(\\pm\\sqrt{a^2-b^2},\\,0)$、長軸の長さ $2a$、短軸の長さ $2b$、焦点からの距離の和は $2a$。",
                               "$b>a>0$ の楕円は焦点が $y$ 軸上にあり $(0,\\,\\pm\\sqrt{b^2-a^2})$。",
                               "双曲線の焦点は $(\\pm\\sqrt{a^2+b^2},\\,0)$、漸近線は $y=\\pm\\dfrac{b}{a}x$、焦点からの距離の差は $2a$。右辺が $-1$ のときは焦点が $y$ 軸上 $(0,\\,\\pm\\sqrt{a^2+b^2})$ に移る。",
                               "放物線 $x^2=4py$ の焦点は $(0,\\,p)$、準線は $y=-p$。"],
                   figure=figure("楕円 x^2/9+y^2/5=1 と焦点 (±2, 0)", plane((-4, 4), (-3, 3), unit=24,
                                                                        curves=[(lambda x: (5 * (1 - x * x / 9)) ** 0.5 if abs(x) <= 3 else float("nan"), ""),
                                                                                (lambda x: -(5 * (1 - x * x / 9)) ** 0.5 if abs(x) <= 3 else float("nan"), "")],
                                                                        points=[(2, 0, "F"), (-2, 0, "F'")])),
                   points=[tp("楕円は $c^2=a^2-b^2$、双曲線は $c^2=a^2+b^2$ と符号が違うことを、表にして並べて板書する。", caution="楕円で $a^2+b^2$ を使う誤りが非常に多い。"),
                           tp("どちらの軸上に焦点があるかは「分母の大きい方の文字の軸」（楕円）、「右辺 $1$ と同符号の項の文字の軸」（双曲線）で判断させる。")]),
        derivation("dv1", "楕円の方程式の導出",
                   ["焦点を F$(c,\\,0)$、F'$(-c,\\,0)$（$c>0$）、距離の和を $2a$（$a>c$）とし、点 P$(x,\\,y)$ が $\\mathrm{PF}+\\mathrm{PF'}=2a$ を満たすとする。",
                    "$\\sqrt{(x+c)^2+y^2}=2a-\\sqrt{(x-c)^2+y^2}$ の両辺を2乗して整理すると $a\\sqrt{(x-c)^2+y^2}=a^2-cx$。",
                    "さらに両辺を2乗すると $a^2(x^2-2cx+c^2+y^2)=a^4-2a^2cx+c^2x^2$。",
                    "整理して $(a^2-c^2)x^2+a^2y^2=a^2(a^2-c^2)$。",
                    "$b=\\sqrt{a^2-c^2}\\ (>0)$ とおき、両辺を $a^2b^2$ で割ると $\\dfrac{x^2}{a^2}+\\dfrac{y^2}{b^2}=1$。（逆に、この式を満たす点は $\\mathrm{PF}+\\mathrm{PF'}=2a$ を満たすことも確かめられる。）"],
                   body="根号を含む式は、根号を1つずつ片側に移してから2乗するのが定石である。",
                   points=[tp("1回目の2乗の前に根号を1つ移項する理由を考えさせる。", ask="根号が2つある式をそのまま2乗するとどうなるか。", expect="根号どうしの積が残り、根号が消えない。"),
                           tp("$b^2=a^2-c^2$ という置きかえが、焦点の公式 $c=\\sqrt{a^2-b^2}$ の由来であることを確認する。", timing="導出の直後")]),
        example("ex1", "例題1　楕円の焦点",
                "楕円 $\\dfrac{x^2}{9}+\\dfrac{y^2}{5}=1$ の焦点の座標と、長軸・短軸の長さを求めよ。",
                ["$a^2=9,\\ b^2=5$ で、$9>5$ より焦点は $x$ 軸上。", "$c=\\sqrt{9-5}=2$。", "長軸の長さ $2\\cdot3=6$、短軸の長さ $2\\sqrt{5}$。"],
                "焦点 $(2,\\,0),\\ (-2,\\,0)$、長軸の長さ $6$、短軸の長さ $2\\sqrt{5}$",
                thinking="分母の大小で焦点のある軸を決め、$c^2=a^2-b^2$ を使う。",
                points=[tp("答えを出したら、楕円上の点 $(3,\\,0)$ から2焦点までの距離の和 $1+5=6$ が長軸の長さと一致することを確かめさせる。")],
                misconceptions=[("$c=\\sqrt{9+5}=\\sqrt{14}$ とする", "楕円は $c^2=a^2-b^2$。$a^2+b^2$ は双曲線")]),
        definition("df2", "媒介変数表示",
                   "曲線上の点 $(x,\\,y)$ を、別の変数 $t$ を用いて $x=f(t),\\ y=g(t)$ と表すことを曲線の媒介変数表示といい、$t$ を媒介変数という。",
                   formula="$$\\text{円 } x^2+y^2=r^2:\\ \\begin{cases}x=r\\cos\\theta\\\\ y=r\\sin\\theta\\end{cases}\\qquad \\text{楕円 } \\dfrac{x^2}{a^2}+\\dfrac{y^2}{b^2}=1:\\ \\begin{cases}x=a\\cos\\theta\\\\ y=b\\sin\\theta\\end{cases}$$",
                   conditions=["媒介変数を消去すると $x,\\ y$ の方程式が得られるが、$x,\\ y$ のとりうる値の範囲に制限がつくことがある（例：$x=t^2$ なら $x\\geqq0$）。",
                               "半径 $a$ の円が直線上をすべらずに転がるとき、円周上の定点が描く曲線（サイクロイド）は $x=a(\\theta-\\sin\\theta),\\ y=a(1-\\cos\\theta)$ と表される。"],
                   points=[tp("媒介変数 $t$ を時刻と考えると、点が曲線上を動くようすが表せることを説明する（物理の運動との関連）。"),
                           tp("消去した後に $x,\\ y$ の範囲を確認する習慣をつけさせる。", caution="範囲を落として、曲線の一部だけなのに全体を答える誤りが多い。")]),
        example("ex2", "例題2　媒介変数の消去",
                "$x=t^2+1,\\ y=2t^2-3$ で表される点 $(x,\\,y)$ が描く図形を求めよ。",
                ["第1式より $t^2=x-1$。", "第2式に代入して $y=2(x-1)-3=2x-5$。", "$t^2\\geqq0$ より $x\\geqq1$。"],
                "直線 $y=2x-5$ のうち $x\\geqq1$ の部分（半直線）",
                thinking="$t^2$ をひとまとまりとして消去する。$t^2\\geqq0$ から $x$ の範囲が出る。",
                points=[tp("「直線 $y=2x-5$」とだけ答えた答案を示し、どこが不十分かを考えさせる。", ask="$x=0$ となる $t$ はあるか。", expect="$t^2=-1$ となり、実数 $t$ はない。")]),
        definition("df3", "複素数平面と極形式",
                   "複素数 $z=a+bi$ を座標平面上の点 $(a,\\,b)$ に対応させた平面を複素数平面という。原点からの距離 $r=|z|=\\sqrt{a^2+b^2}$ を絶対値、実軸の正の向きから測った角 $\\theta$ を偏角（$\\arg z$）という。",
                   formula="$$z=r(\\cos\\theta+i\\sin\\theta)\\qquad (r=|z|,\\ \\theta=\\arg z)$$",
                   conditions=["$z\\neq0$ のとき偏角は $2\\pi$ の整数倍の差を除いて1つに決まる。問題では $0\\leqq\\theta<2\\pi$ などと範囲を指定することが多い。",
                               "偏角は $\\cos\\theta=\\dfrac{a}{r},\\ \\sin\\theta=\\dfrac{b}{r}$ の両方を満たす角として求める（$\\tan\\theta$ だけでは象限が決まらない）。"],
                   points=[tp("点 $z$ を図にかいてから偏角を読む手順を徹底させる。", caution="$\\tan\\theta=\\dfrac{b}{a}$ だけで角を決め、象限を誤る生徒が多い。")]),
        theorem("th1", "積・商の極形式とド・モアブルの定理",
                "$$z_1z_2=r_1r_2\\{\\cos(\\theta_1+\\theta_2)+i\\sin(\\theta_1+\\theta_2)\\},\\qquad (\\cos\\theta+i\\sin\\theta)^n=\\cos n\\theta+i\\sin n\\theta$$",
                ["$z_k=r_k(\\cos\\theta_k+i\\sin\\theta_k)$。商は $\\dfrac{z_1}{z_2}=\\dfrac{r_1}{r_2}\\{\\cos(\\theta_1-\\theta_2)+i\\sin(\\theta_1-\\theta_2)\\}$（$z_2\\neq0$）。",
                 "ド・モアブルの定理は $n$ が整数のとき成り立つ。",
                 "$\\cos\\theta+i\\sin\\theta$ をかけることは、原点のまわりに $\\theta$ だけ回転することを表す。点 $\\alpha$ のまわりの回転は $w=\\alpha+(z-\\alpha)(\\cos\\theta+i\\sin\\theta)$。"],
                body="積は「絶対値はかけ算、偏角はたし算」。累乗はその繰り返しである。",
                proof=["積：$z_1z_2=r_1r_2\\{(\\cos\\theta_1\\cos\\theta_2-\\sin\\theta_1\\sin\\theta_2)+i(\\sin\\theta_1\\cos\\theta_2+\\cos\\theta_1\\sin\\theta_2)\\}$ に加法定理を使う。",
                       "ド・モアブル（$n\\geqq1$）：$n=1$ では明らか。$n=k$ で成り立つと仮定する。",
                       "$(\\cos\\theta+i\\sin\\theta)^{k+1}=(\\cos k\\theta+i\\sin k\\theta)(\\cos\\theta+i\\sin\\theta)=\\cos(k+1)\\theta+i\\sin(k+1)\\theta$（積の公式）。よって $n=k+1$ でも成り立つ。",
                       "$n=0$ のときは両辺とも $1$。$n=-m$（$m\\geqq1$）のときは $(\\cos\\theta+i\\sin\\theta)^{-1}=\\cos(-\\theta)+i\\sin(-\\theta)$ を使って、$m$ の場合に帰着できる。"],
                points=[tp("積の公式の証明で加法定理の形がそのまま現れることを見せ、数学Ⅱとのつながりを強調する。", ask="$\\cos\\theta_1\\cos\\theta_2-\\sin\\theta_1\\sin\\theta_2$ は何に等しいか。", expect="$\\cos(\\theta_1+\\theta_2)$"),
                        tp("$i$ をかけると $\\dfrac{\\pi}{2}$ 回転になることを、具体的な点（例：$2+i\\to-1+2i$）で確かめさせる。")]),
        example("ex3", "例題3　ド・モアブルの定理による累乗",
                "$(\\sqrt{3}+i)^6$ を計算せよ。",
                ["$\\sqrt{3}+i=2\\left(\\cos\\dfrac{\\pi}{6}+i\\sin\\dfrac{\\pi}{6}\\right)$。", "ド・モアブルの定理より $(\\sqrt{3}+i)^6=2^6(\\cos\\pi+i\\sin\\pi)$。", "$=64\\cdot(-1)=-64$。"],
                "$-64$",
                thinking="展開すると大変なので、極形式に直して偏角を6倍する。",
                points=[tp("$r^n$ をかけ忘れる誤りが多いので、絶対値と偏角を別々に処理するよう指導する。")]),
        example("ex4", "例題4　方程式 $z^3=-8$",
                "方程式 $z^3=-8$ を解け。",
                ["$z=r(\\cos\\theta+i\\sin\\theta)$ とおくと $r^3(\\cos3\\theta+i\\sin3\\theta)=8(\\cos\\pi+i\\sin\\pi)$。",
                 "絶対値を比べて $r^3=8$、$r>0$ より $r=2$。", "偏角を比べて $3\\theta=\\pi+2k\\pi$、$\\theta=\\dfrac{\\pi}{3}+\\dfrac{2k\\pi}{3}$（$k=0,1,2$）。",
                 "$k=0,1,2$ に対応して $z=1+\\sqrt{3}i,\\ -2,\\ 1-\\sqrt{3}i$。"],
                "$z=1+\\sqrt{3}i,\\ -2,\\ 1-\\sqrt{3}i$",
                thinking="$z$ を極形式でおき、両辺の絶対値と偏角を比較する。偏角は $2\\pi$ の整数倍のずれを考える。",
                points=[tp("3つの解が原点を中心とする半径2の円周上に、正三角形の頂点として並ぶことを図で示す。"),
                        tp("$z^3+8=(z+2)(z^2-2z+4)=0$ と因数分解して解く方法（数学Ⅱ）でも同じ解になることを確かめさせる。")]),
        board("bd1", "板書案",
              [("① 二次曲線", ["放物線 $y^2=4px$：焦点 $(p,0)$、準線 $x=-p$", "楕円：$c^2=a^2-b^2$（和 $2a$）", "双曲線：$c^2=a^2+b^2$（差 $2a$）", "漸近線 $y=\\pm\\dfrac{b}{a}x$"]),
               ("② 媒介変数表示", ["円 $x=r\\cos\\theta,\\ y=r\\sin\\theta$", "楕円 $x=a\\cos\\theta,\\ y=b\\sin\\theta$", "消去したら範囲を確認", "例2：$y=2x-5\\ (x\\geqq1)$"]),
               ("③ 複素数平面", ["$z=r(\\cos\\theta+i\\sin\\theta)$", "積：絶対値は積、偏角は和", "$(\\cos\\theta+i\\sin\\theta)^n=\\cos n\\theta+i\\sin n\\theta$", "$z^n=w$：偏角に $2k\\pi$"])],
              points=[tp("①では楕円と双曲線の公式を左右に並べ、符号の違いを色チョークで強調する。③には $z^3=-8$ の3つの解を円周上に図示する。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("焦点の位置を答えるときは、分母の大小（楕円）や右辺の符号（双曲線）を確認してから計算させる。", caution="いつも $x$ 軸上と決めつける誤りが多い。"),
               tp("媒介変数を消去したら「$x,\\ y$ の範囲に制限はないか」を必ず自問させる。", ask="$x=\\cos\\theta$ なら $x$ はどんな範囲の値をとるか。", expect="$-1\\leqq x\\leqq1$"),
               tp("偏角は図をかいて象限を確認してから決めさせる。$\\tan$ の値だけで判断しない。", timing="極形式の導入時"),
               tp("$z^n=w$ では、偏角に $2k\\pi$ を加えることを忘れると解が1つしか得られないことを、$z^2=1$ の例で確認させる。"),
               tp("複素数の積を「回転と拡大」として図で説明すると、ド・モアブルの定理や回転の問題が直観的に理解しやすい。")],
              misconceptions=[("楕円の焦点を $c=\\sqrt{a^2+b^2}$ で求める", "楕円は $c^2=a^2-b^2$、双曲線が $c^2=a^2+b^2$"),
                              ("$-1+\\sqrt{3}i$ の偏角を $\\tan\\theta=-\\sqrt{3}$ から $-\\dfrac{\\pi}{3}$ とする", "点は第2象限にあるので $\\dfrac{2}{3}\\pi$"),
                              ("$\\{r(\\cos\\theta+i\\sin\\theta)\\}^n=r(\\cos n\\theta+i\\sin n\\theta)$ とする", "絶対値も $n$ 乗して $r^n$")]),
        summary("sm1", "まとめ",
                ["二次曲線は距離の条件で定義される。楕円 $c^2=a^2-b^2$、双曲線 $c^2=a^2+b^2$、放物線 $y^2=4px$ の焦点 $(p,\\,0)$。",
                 "媒介変数表示は消去して方程式にし、$x,\\ y$ の範囲を確認する。",
                 "極形式では積は「絶対値の積・偏角の和」。ド・モアブルの定理で累乗が計算でき、$z^n=w$ は偏角に $2k\\pi$ を加えて $n$ 個の解を求める。"]),
        check("ck1", "確認問題",
              [("放物線 $x^2=8y$ の焦点と準線を求めよ。", "$x^2=4\\cdot2y$ より焦点 $(0,\\,2)$、準線 $y=-2$"),
               ("$-2+2i$ を極形式で表せ（$0\\leqq\\theta<2\\pi$）。", "$2\\sqrt{2}\\left(\\cos\\dfrac{3}{4}\\pi+i\\sin\\dfrac{3}{4}\\pi\\right)$"),
               ("$(1+i)^8$ を計算せよ。", "$1+i=\\sqrt{2}\\left(\\cos\\dfrac{\\pi}{4}+i\\sin\\dfrac{\\pi}{4}\\right)$ より $(\\sqrt{2})^8(\\cos2\\pi+i\\sin2\\pi)=16$")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

@gen("basic_check", 5, ["computation", "concept"])
def parabola_focus(r):
    p = nonzero(r, -6, 6)
    axis = r.choice(["x", "y"])
    if axis == "x":
        eq, F, D = f"y^2={4 * p}x", f"({p},\\,0)", f"x={-p}"
        Fv = f"({p},0)"
    else:
        eq, F, D = f"x^2={4 * p}y", f"(0,\\,{p})", f"y={-p}"
        Fv = f"(0,{p})"
    other = "y" if axis == "x" else "x"
    return sa(f"放物線 ${eq}$ について、焦点の座標と準線の方程式をそれぞれ答えなさい。", f"焦点 ${F}$、準線 ${D}$",
              f"${eq}$ を ${'y^2=4px' if axis == 'x' else 'x^2=4py'}$ と比べると $4p={4 * p}$ より $p={p}$。", d=1, v=[f"{Fv}, {D}"],
              ap=f"標準形 ${'y^2=4px' if axis == 'x' else 'x^2=4py'}$ と係数を比べて $p$ を求める。焦点は ${axis}$ 軸上にある。",
              steps=[f"${4 * p}=4p$ より $p={p}$。", f"焦点は ${F}$。", f"準線は ${D}$。"],
              alt=[f"定義から確かめる：焦点 ${F}$ と準線 ${D}$ から等距離にある点 $({other}$ 軸上の頂点は原点$)$ を考えると、原点は両方から距離 ${abs(p)}$ で等しい。"],
              pc=[("焦点を正しく答えている", 1), ("準線を方程式で正しく答えている", 1)],
              pit=["$4p={4 * p}$ から $p={4 * p}$ としてしまう（$4$ で割り忘れ）。", "焦点がどちらの軸上にあるかを取り違える。"],
              chk=(f"Rational({4 * p}, 4)", str(p), None, "intermediate"))


ELL = [(5, 4), (5, 3), (13, 12), (13, 5), (10, 8), (10, 6), (17, 15), (17, 8), (3, 2), (4, 2), (4, 3), (5, 2), (6, 4), (7, 5), (6, 5), (3, 1)]


@gen("basic_check", 5, ["computation", "condition_check"])
def ellipse_focus(r):
    A, B = r.choice(ELL)
    swap = r.random() < 0.4
    a2, b2 = (B * B, A * A) if swap else (A * A, B * B)
    c = sp.sqrt(A * A - B * B)
    ct = sp.latex(c)
    if not swap:
        F = f"$({ct},\\,0),\\ (-{ct},\\,0)$"
    else:
        F = f"$(0,\\,{ct}),\\ (0,\\,-{ct})$"
    eq = f"{sqfrac('x', a2)}+{sqfrac('y', b2)}=1"
    ax = "$y$ 軸" if swap else "$x$ 軸"
    return sa(f"楕円 ${eq}$ の焦点の座標と、長軸の長さを求めなさい。", f"焦点 {F}、長軸の長さ ${2 * A}$",
              f"分母の大きい方は {'$y^2$' if swap else '$x^2$'} の ${A * A}$ なので焦点は{ax}上。$\\sqrt{{{A * A}-{B * B}}}={ct}$。", d=2,
              ap="分母の大きい方の文字の軸上に焦点がある。焦点までの距離は $\\sqrt{(\\text{大きい分母})-(\\text{小さい分母})}$。",
              steps=[f"分母を比べると ${A * A}>{B * B}$ で、大きい方は {'$y^2$' if swap else '$x^2$'} の分母。焦点は{ax}上。",
                     f"$\\sqrt{{{A * A}-{B * B}}}={ct}$ より焦点 {F}。", f"長軸の長さは $2\\sqrt{{{A * A}}}={2 * A}$。"],
              alt=[f"長軸の端の点（例：{'$(0,\\,' + str(A) + ')$' if swap else '$(' + str(A) + ',\\,0)$'}）から2焦点までの距離の和が長軸の長さ ${2 * A}$ と一致することで確かめられる。"],
              pc=[("焦点のある軸と座標を正しく答えている", 1), ("長軸の長さを正しく答えている", 1)],
              pit=["$\\sqrt{a^2+b^2}$ と双曲線の式を使ってしまう。", "分母の大小を確かめず、いつも $x$ 軸上に焦点をとる。"],
              chk=(f"sqrt({A * A}-{B * B})", sp.sstr(c), None, "intermediate"))


@gen("basic_check", 5, ["computation", "concept"])
def polar_form(r):
    mod, f = nice_point(r)
    z = zval(mod, f)
    return sa(f"複素数 $z={ctex(z)}$ の絶対値と偏角 $\\theta\\ (0\\leqq\\theta<2\\pi)$ を求め、$z$ を極形式で表しなさい。",
              f"$|z|={sp.latex(mod)}$、$\\theta={atex(f)}$、$z={polar_tex(mod, f)}$",
              f"$|z|={sp.latex(mod)}$。$\\cos\\theta=\\dfrac{{{sp.latex(sp.re(z))}}}{{{sp.latex(mod)}}},\\ \\sin\\theta=\\dfrac{{{sp.latex(sp.im(z))}}}{{{sp.latex(mod)}}}$ を満たす $\\theta$ は ${atex(f)}$。", d=2,
              ap="絶対値は原点からの距離。偏角は、点を複素数平面にかいて象限を確認してから $\\cos\\theta,\\ \\sin\\theta$ の値で決める。",
              steps=[f"$|z|=\\sqrt{{({sp.latex(sp.re(z))})^2+({sp.latex(sp.im(z))})^2}}={sp.latex(mod)}$。",
                     f"$z={sp.latex(mod)}\\left(\\dfrac{{{sp.latex(sp.re(z))}}}{{{sp.latex(mod)}}}+\\dfrac{{{sp.latex(sp.im(z))}}}{{{sp.latex(mod)}}}i\\right)$ と、絶対値でくくる。",
                     f"$\\cos\\theta={sp.latex(sp.nsimplify(sp.re(z) / mod))},\\ \\sin\\theta={sp.latex(sp.nsimplify(sp.im(z) / mod))}$ より $\\theta={atex(f)}$。"],
              alt=["複素数平面上に点をとり、実軸・虚軸と特別な直角三角形（$1:1:\\sqrt{2}$ や $1:2:\\sqrt{3}$）から偏角を読み取ってもよい。"],
              pc=[("絶対値を正しく求めている", 1), ("偏角を正しく求め、極形式で表している", 1)],
              pit=["$\\tan\\theta$ の値だけで偏角を決め、象限を誤る。", "偏角の範囲 $0\\leqq\\theta<2\\pi$ を守らず負の角で答える。"],
              chk=(f"[Abs({cpy(z)}), simplify(({sp.sstr(mod)})*(cos({apy(f)})+I*sin({apy(f)}))-({cpy(z)}))]", f"[{sp.sstr(mod)}, 0]", None, "intermediate"))


@gen("basic_check", 5, ["computation", "concept"])
def param_elim(r):
    kind = r.choice(["ellipse", "circle", "parabola"])
    if kind == "ellipse":
        a, b = r.sample([1, 2, 3, 4, 5, 6], 2)
        stem = f"x={'' if a == 1 else a}\\cos\\theta,\\ y={'' if b == 1 else b}\\sin\\theta"
        ans = f"{sqfrac('x', a * a)}+{sqfrac('y', b * b)}=1"
        expl = f"$\\cos\\theta=\\dfrac{{x}}{{{a}}},\\ \\sin\\theta=\\dfrac{{y}}{{{b}}}$ を $\\cos^2\\theta+\\sin^2\\theta=1$ に代入する。"
        steps = [f"$\\cos\\theta=\\dfrac{{x}}{{{a}}}$、$\\sin\\theta=\\dfrac{{y}}{{{b}}}$。", "$\\cos^2\\theta+\\sin^2\\theta=1$ に代入する。", f"${ans}$（楕円）。"]
        chk = (f"simplify(({a}*cos(theta))**2/{a * a}+({b}*sin(theta))**2/{b * b}-1)", "0")
        what = "楕円"
    elif kind == "circle":
        p, q, rad = nonzero(r, -4, 4), nonzero(r, -4, 4), r.randint(1, 5)
        stem = f"x={lin_tex(rad, p, '\\cos\\theta') if False else (str(p) + '+' + ('' if rad == 1 else str(rad)) + '\\cos\\theta')},\\ y={q}+{'' if rad == 1 else rad}\\sin\\theta"
        ans = f"{shift_sq('x', p)}+{shift_sq('y', q)}={rad * rad}"
        expl = f"$\\cos\\theta=\\dfrac{{x-({p})}}{{{rad}}},\\ \\sin\\theta=\\dfrac{{y-({q})}}{{{rad}}}$ を $\\cos^2\\theta+\\sin^2\\theta=1$ に代入する。"
        steps = [f"$x-({p})={rad}\\cos\\theta$、$y-({q})={rad}\\sin\\theta$。", "両辺を2乗して加えると、$\\cos^2\\theta+\\sin^2\\theta=1$ より $\\theta$ が消える。", f"${ans}$（中心 $({p},\\,{q})$、半径 ${rad}$ の円）。"]
        chk = (f"simplify((({p})+{rad}*cos(theta)-({p}))**2+(({q})+{rad}*sin(theta)-({q}))**2-{rad * rad})", "0")
        what = "円"
    else:
        p, q = nonzero(r, -4, 4), r.randint(-5, 5)
        c = r.choice([1, 2, -1, 3, -2])
        stem = f"x={lin_tex(1, p)},\\ y={lin_tex(c, q, 't^2')}"
        ans = f"y={'' if c == 1 else ('-' if c == -1 else c)}{shift_sq('x', p)}{'' if q == 0 else (f'+{q}' if q > 0 else q)}"
        expl = f"第1式より $t=x-({p})$。これを第2式に代入する。"
        steps = [f"$t=x{'-' if p > 0 else '+'}{abs(p)}$。", "第2式に代入して $t$ を消去する。", f"${ans}$（放物線）。"]
        chk = (f"expand(({c})*t**2+({q})-(({c})*((t+({p}))-({p}))**2+({q})))", "0")
        what = "放物線"
    return sa(f"媒介変数表示 ${stem}$ で表される曲線の方程式を、媒介変数を消去して $x,\\ y$ の式で表しなさい。", f"${ans}$", expl, d=2, v=[ans],
              ap=("三角関数で表されているときは $\\cos^2\\theta+\\sin^2\\theta=1$ を使って消去する。" if kind != "parabola"
                  else "一次式で表されている方から媒介変数 $t$ を $x$ で表し、もう一方に代入する。"),
              steps=steps,
              alt=[f"得られた方程式に、媒介変数表示の $x,\\ y$ を代入すると恒等的に成り立つことを確かめる（{what}の上の点であることの確認）。"],
              pc=[("消去の方針（関係式・代入）が正しい", 1), ("正しい方程式を答えている", 1)],
              pit=(["$\\cos\\theta=" + "\\dfrac{x}{a}" + "$ の分母を2乗し忘れる。"] if kind != "parabola" else ["$t=x-p$ の符号を誤る。"]),
              chk=chk + (None, "intermediate"))


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 5, ["computation"])
def demoivre_power(r):
    while True:
        mod, f = nice_point(r)
        if f.denominator > 2:
            break
    if mod > 3:
        mod = sp.nsimplify(mod / 2) if f.denominator == 6 else mod
    if f.denominator == 6 and mod not in (2, 4):
        mod = sp.Integer(2)
    n = r.randint(3, 8) if mod <= 2 else r.randint(3, 5)
    z = zval(mod, f)
    w = sp.nsimplify(sp.expand(z ** n))
    fn = norm_arg(f * n)
    return sa(f"ド・モアブルの定理を用いて、$\\left({ctex(z)}\\right)^{{{n}}}$ を $a+bi$（$a,\\ b$ は実数）の形で表しなさい。", f"${ctex(w)}$",
              f"${ctex(z)}={polar_tex(mod, f)}$ より、${n}$ 乗すると絶対値は $({sp.latex(mod)})^{{{n}}}={sp.latex(mod ** n)}$、偏角は ${atex(f * n)}$。", d=3, v=[ctex(w)],
              ap="そのまま展開すると計算量が多い。極形式に直し、絶対値を $n$ 乗・偏角を $n$ 倍する。",
              steps=[f"${ctex(z)}={polar_tex(mod, f)}$。",
                     f"$\\left({ctex(z)}\\right)^{{{n}}}={sp.latex(sp.expand(mod ** n))}\\left(\\cos {atex(f * n)}+i\\sin {atex(f * n)}\\right)$。",
                     f"${atex(f * n)}$ は ${atex(fn)}$ と同じ向きなので、値を代入して ${ctex(w)}$。"],
              alt=[f"偏角 ${atex(f)}$ を ${n}$ 倍した角が単位円のどこにあるかを図で確かめると、符号の誤りを防げる。"
                   if n > 4 else f"二項定理で展開しても同じ結果になる（$i^2=-1$ に注意）。"],
              pc=[("極形式に正しく直している", 1), ("ド・モアブルの定理を正しく使っている", 2), ("$a+bi$ の形で正しく答えている", 1)],
              pit=["絶対値を $n$ 乗し忘れる。", "偏角を $n$ 倍した後の三角関数の値の符号を誤る。"],
              chk=(f"expand(({cpy(z)})**{n})", cpy(w), None, "intermediate"))


@gen("standard_practice", 4, ["computation", "concept"])
def product_quotient(r):
    r1, r2 = r.randint(1, 6), r.randint(1, 4)
    f1 = Fraction(r.choice([1, 2, 3, 4, 5, 7, 8, 9, 10, 11]), r.choice([6, 4, 12])) if r.random() < 0.3 else Fraction(r.randint(1, 11), 6)
    f2 = Fraction(r.randint(1, 7), 4) if r.random() < 0.5 else Fraction(r.randint(1, 11), 6)
    if f1 == f2:
        f2 = f2 + Fraction(1, 2)
    kind = r.choice(["mul", "div"])
    if kind == "mul":
        R, F = sp.Integer(r1 * r2), norm_arg(f1 + f2)
        expr_py = f"({r1}*(cos({apy(f1)})+I*sin({apy(f1)})))*({r2}*(cos({apy(f2)})+I*sin({apy(f2)})))"
        op_t, rule = "z_1z_2", "絶対値は積、偏角は和"
        raw = f1 + f2
    else:
        R, F = sp.Rational(r1, r2), norm_arg(f1 - f2)
        expr_py = f"({r1}*(cos({apy(f1)})+I*sin({apy(f1)})))/({r2}*(cos({apy(f2)})+I*sin({apy(f2)})))"
        op_t, rule = "\\dfrac{z_1}{z_2}", "絶対値は商、偏角は差"
        raw = f1 - f2
    return sa(f"$z_1={polar_tex(sp.Integer(r1), f1)},\\ z_2={polar_tex(sp.Integer(r2), f2)}$ のとき、${op_t}$ を極形式で表しなさい。ただし偏角 $\\theta$ は $0\\leqq\\theta<2\\pi$ とする。",
              f"${op_t}={polar_tex(R, F)}$", f"{rule}。偏角は ${atex(raw)}$" + ("" if raw == F else f"、範囲に合わせて ${atex(F)}$") + "。", d=3,
              ap="極形式どうしの積・商は、絶対値と偏角を別々に計算できる（積：絶対値の積・偏角の和、商：絶対値の商・偏角の差）。",
              steps=[f"絶対値：${sp.latex(R)}$。", f"偏角：${atex(raw)}$。", ("" if raw == F else f"$2\\pi$ の整数倍を加えて $0\\leqq\\theta<2\\pi$ に直すと ${atex(F)}$。") or "偏角はすでに $0\\leqq\\theta<2\\pi$ の範囲にある。",
                     f"${op_t}={polar_tex(R, F)}$。"],
              alt=["$a+bi$ の形に直してから計算し、最後に極形式に戻しても同じ結果になるが、計算量が多い。極形式のまま計算する利点を確認するとよい。"],
              pc=[("絶対値を正しく求めている", 1), ("偏角を正しく求めている", 2), ("偏角の範囲を指定どおりに直している", 1)],
              pit=["商で偏角を和にしてしまう。", "偏角の範囲を $0\\leqq\\theta<2\\pi$ に直し忘れる。"],
              chk=(f"simplify({expr_py}-({sp.sstr(R)})*(cos({apy(F)})+I*sin({apy(F)})))", "0", None, "intermediate"))


ROT = [Fraction(1, 2), Fraction(-1, 2), Fraction(1, 3), Fraction(-1, 3), Fraction(2, 3), Fraction(1, 1), Fraction(1, 6), Fraction(-1, 6)]


@gen("standard_practice", 4, ["computation", "application"])
def rotation(r):
    f = r.choice(ROT)
    z = sp.Integer(r.randint(-4, 4)) + sp.I * r.randint(-4, 4)
    if f.denominator == 6:
        z = sp.Integer(nonzero(r, -4, 4)) * r.choice([1, sp.I])
    center = r.random() < 0.5 and f.denominator != 6
    al = sp.Integer(r.randint(-3, 3)) + sp.I * r.randint(-3, 3) if center else sp.Integer(0)
    if z == al:
        z = z + 2 + sp.I
    rotf = sp.nsimplify(sp.cos(sp.pi * sp.Rational(f.numerator, f.denominator)) + sp.I * sp.sin(sp.pi * sp.Rational(f.numerator, f.denominator)))
    w = sp.nsimplify(sp.expand(al + (z - al) * rotf))
    dirn = "反時計回りに" if f > 0 else "時計回りに"
    ang = atex(abs(f))
    where = f"点 $\\alpha={ctex(al)}$ のまわりに" if center else "原点のまわりに"
    return sa(f"複素数平面上で、点 $z={ctex(z)}$ を{where}{dirn} ${ang}$ だけ回転した点を表す複素数 $w$ を求めなさい。", f"$w={ctex(w)}$",
              (f"$w=\\alpha+(z-\\alpha)\\left\\{{\\cos\\left({atex(f)}\\right)+i\\sin\\left({atex(f)}\\right)\\right\\}}$ を計算する。" if center
               else f"$w=z\\left\\{{\\cos\\left({atex(f)}\\right)+i\\sin\\left({atex(f)}\\right)\\right\\}}$ を計算する。"), d=3, v=[ctex(w)],
              ap="原点のまわりの $\\theta$ 回転は $\\cos\\theta+i\\sin\\theta$ をかけること。中心が $\\alpha$ のときは、$\\alpha$ を原点に移してから回転し、元に戻す。",
              steps=([f"$z-\\alpha={ctex(z - al)}$（$\\alpha$ を原点に移す）。"] if center else [])
              + [f"$\\cos\\left({atex(f)}\\right)+i\\sin\\left({atex(f)}\\right)={ctex(rotf)}$。",
                 f"${'(z-\\alpha)' if center else 'z'}\\times({ctex(rotf)})={ctex(sp.expand((z - al) * rotf))}$。"]
              + ([f"$\\alpha$ を加えて元に戻すと $w={ctex(w)}$。"] if center else [f"$w={ctex(w)}$。"]),
              alt=["回転の前後で中心からの距離が変わらないこと（$|w-\\alpha|=|z-\\alpha|$）を計算して確かめる。" if center
                   else "回転の前後で原点からの距離が変わらないこと（$|w|=|z|$）を計算して確かめる。"],
              pc=[("回転を複素数の積で表している", 1), ("回転を表す複素数を正しく求めている", 1), ("$w$ を正しく計算している", 2)],
              pit=["時計回りの回転で偏角の符号を正にしてしまう。"] + (["中心 $\\alpha$ を引かずに $z$ をそのまま回転させる。"] if center else []),
              chk=(f"expand(({cpy(al)})+(({cpy(z)})-({cpy(al)}))*(cos({apy(f)})+I*sin({apy(f)})))", cpy(w), None, "intermediate"))


@gen("standard_practice", 4, ["computation", "condition_check"])
def hyperbola(r):
    a, b = r.randint(1, 6), r.randint(1, 6)
    side = r.choice([1, 1, -1])
    c = sp.sqrt(a * a + b * b)
    ct = sp.latex(c)
    eq = f"{sqfrac('x', a * a)}-{sqfrac('y', b * b)}={'1' if side == 1 else '-1'}"
    F = f"$({ct},\\,0),\\ (-{ct},\\,0)$" if side == 1 else f"$(0,\\,{ct}),\\ (0,\\,-{ct})$"
    sl = frac(b, a)
    asym = f"$y={sl}x,\\ y=-{sl}x$" if sl != "1" else "$y=x,\\ y=-x$"
    return sa(f"双曲線 ${eq}$ の焦点の座標と漸近線の方程式を求めなさい。", f"焦点 {F}、漸近線 {asym}",
              f"$\\sqrt{{{a * a}+{b * b}}}={ct}$。焦点は{'$x$' if side == 1 else '$y$'} 軸上。漸近線は右辺を $0$ とおいた ${sqfrac('x', a * a)}-{sqfrac('y', b * b)}=0$ から得られる。", d=3,
              ap="双曲線の焦点までの距離は $\\sqrt{a^2+b^2}$（楕円とは符号が違う）。右辺の符号で焦点のある軸が決まる。漸近線は右辺を $0$ にした式を因数分解する。",
              steps=[f"$a^2={a * a},\\ b^2={b * b}$、$\\sqrt{{a^2+b^2}}={ct}$。",
                     ("右辺が $1$ なので焦点は $x$ 軸上。" if side == 1 else "右辺が $-1$ なので焦点は $y$ 軸上。") + f"焦点 {F}。",
                     f"${sqfrac('x', a * a)}-{sqfrac('y', b * b)}=0$ より $\\left(\\dfrac{{x}}{{{a}}}-\\dfrac{{y}}{{{b}}}\\right)\\left(\\dfrac{{x}}{{{a}}}+\\dfrac{{y}}{{{b}}}\\right)=0$。",
                     f"漸近線 {asym}。"],
              alt=["$x$ が十分大きいとき $y=\\pm\\dfrac{b}{a}x\\sqrt{1-\\dfrac{a^2}{x^2}}$ が $\\pm\\dfrac{b}{a}x$ に近づくことから、漸近線を確かめられる（右辺が $1$ の場合）。"],
              pc=[("焦点のある軸を正しく判断している", 1), ("焦点の座標を正しく求めている", 1), ("漸近線を正しく求めている", 2)],
              pit=["$\\sqrt{a^2-b^2}$ と楕円の式を使う。", "右辺が $-1$ のとき焦点を $x$ 軸上にとる。", "漸近線の傾きを $\\dfrac{a}{b}$ と逆にする。"],
              chk=(f"[sqrt({a * a}+{b * b}), Rational({b},{a})]", f"[{sp.sstr(c)}, {fr_py(b, a)}]", None, "intermediate"))


@gen("standard_practice", 3, ["condition_check", "concept"])
def conic_from_def(r):
    kind = r.choice(["parabola", "ellipse", "hyperbola"])
    if kind == "parabola":
        p = nonzero(r, -5, 5)
        ax = r.choice(["x", "y"])
        if ax == "x":
            cond = f"点 F$({p},\\,0)$ と直線 $x={-p}$ からの距離が等しい点 P"
            ans, chk = f"y^2={4 * p}x", (f"expand((x-({p}))**2+y**2-(x+({p}))**2)", f"-{4 * p}*x+y**2", "expand", "intermediate")
            steps = [f"P$(x,\\,y)$ とすると $\\mathrm{{PF}}=\\sqrt{{(x-({p}))^2+y^2}}$、直線までの距離は $|x-({-p})|$。", "両辺を2乗して等しいとおく。", f"展開して整理すると ${ans}$。"]
        else:
            cond = f"点 F$(0,\\,{p})$ と直線 $y={-p}$ からの距離が等しい点 P"
            ans, chk = f"x^2={4 * p}y", (f"expand(x**2+(y-({p}))**2-(y+({p}))**2)", f"x**2-{4 * p}*y", "expand", "intermediate")
            steps = [f"P$(x,\\,y)$ とすると $\\mathrm{{PF}}=\\sqrt{{x^2+(y-({p}))^2}}$、直線までの距離は $|y-({-p})|$。", "両辺を2乗して等しいとおく。", f"展開して整理すると ${ans}$。"]
        what = "放物線"
    elif kind == "ellipse":
        A, B = r.choice(ELL[:8])
        c = int(sp.sqrt(A * A - B * B))
        cond = f"2点 F$({c},\\,0)$、F'$(-{c},\\,0)$ からの距離の和が ${2 * A}$ である点 P"
        ans = f"\\dfrac{{x^2}}{{{A * A}}}+\\dfrac{{y^2}}{{{B * B}}}=1"
        chk = (f"{A * A}-{c * c}", str(B * B), None, "intermediate")
        steps = [f"和が $2a={2 * A}$ なので $a={A}$。焦点が $(\\pm{c},\\,0)$ なので $c={c}$。", f"$b^2=a^2-c^2={A * A}-{c * c}={B * B}$。", f"${ans}$。"]
        what = "楕円"
    else:
        a = r.randint(1, 5)
        c = a + r.randint(1, 4)
        b2 = c * c - a * a
        cond = f"2点 F$({c},\\,0)$、F'$(-{c},\\,0)$ からの距離の差が ${2 * a}$ である点 P"
        ans = f"{sqfrac('x', a * a)}-\\dfrac{{y^2}}{{{b2}}}=1"
        chk = (f"{c * c}-{a * a}", str(b2), None, "intermediate")
        steps = [f"差が $2a={2 * a}$ なので $a={a}$。焦点が $(\\pm{c},\\,0)$ なので $c={c}$。", f"$b^2=c^2-a^2={c * c}-{a * a}={b2}$。", f"${ans}$。"]
        what = "双曲線"
    return sa(f"{cond} の軌跡の方程式を求めなさい。", f"${ans}$", f"{what}の定義そのものである。" + steps[-2], d=3, v=[ans],
              ap=f"条件は{what}の定義そのもの。" + ("定義から直接式を立てて2乗する。" if kind == "parabola" else "標準形の $a,\\ c$ を読み取り、$b^2$ を求める。"),
              steps=steps,
              alt=["P$(x,\\,y)$ とおいて距離の条件を式で表し、根号を1つずつ移項して2乗する方法（授業の導出）でも同じ式が得られる。" if kind != "parabola"
                   else "頂点が原点、焦点の位置から開く向きが分かるので、標準形 $y^2=4px$（または $x^2=4py$）に $p$ を当てはめても得られる。"],
              pc=[("曲線の種類と定数を正しく読み取っている", 2), ("正しい方程式を答えている", 2)],
              pit=["楕円で $b^2=a^2+c^2$、双曲線で $b^2=a^2-c^2$ と符号を取り違える。", "距離の和・差の $2a$ を $a$ と読み違える。"],
              chk=chk)


# ======================================================================
# C 思考力・記述応用
# ======================================================================

def _roots_case(r):
    while True:
        n = r.choice([2, 3, 3, 4, 6])
        j = r.choice([0, 1, 2, 3])
        if n in (4, 6) and j % 2 == 1:
            continue
        if n == 2 and j == 0:
            continue
        R = r.choice([1, 2]) if n >= 4 else r.choice([1, 2, 3])
        if not (n == 3 and j == 0 and R == 1):
            return n, Fraction(j, 2), sp.Integer(R)


@gen("thinking_writing", 4, ["written_reasoning", "cross_unit", "multiple_solutions"], rel=["HS-MATH2-U02"])
def roots_eq(r):
    n, phi, R = _roots_case(r)
    w = zval(R ** n, phi)
    angs = [Fraction(phi, n) + Fraction(2 * k, n) for k in range(n)]
    roots = [zval(R, a) for a in angs]
    rt = ",\\ ".join(ctex(z) for z in roots)
    return sa(f"方程式 $z^{{{n}}}={ctex(w)}$ を、$z$ を極形式で表す方法で解きなさい。考え方の過程も書くこと。", f"$z={rt}$",
              f"$z=r(\\cos\\theta+i\\sin\\theta)$ とおくと $r^{{{n}}}={sp.latex(R ** n)}$、${n}\\theta={atex(phi)}+2k\\pi$。$k=0,\\,1,\\,\\ldots,\\,{n - 1}$ で{n}個の解が得られる。", d=4, p=8,
              ap="$z$ を極形式でおき、ド・モアブルの定理で左辺を表す。右辺も極形式にして、絶対値と偏角を比べる。偏角は $2\\pi$ の整数倍のずれを考える。",
              steps=[f"$z=r(\\cos\\theta+i\\sin\\theta)\\ (r>0)$ とおくと $z^{{{n}}}=r^{{{n}}}(\\cos{n}\\theta+i\\sin{n}\\theta)$。",
                     f"右辺は ${polar_tex(R ** n, phi)}$。",
                     f"絶対値を比べて $r^{{{n}}}={sp.latex(R ** n)}$、$r>0$ より $r={R}$。",
                     f"偏角を比べて ${n}\\theta={atex(phi)}+2k\\pi$（$k$ は整数）、$0\\leqq\\theta<2\\pi$ の範囲で $\\theta=" + ",\\ ".join(atex(a) for a in angs) + "$。",
                     f"それぞれ $a+bi$ の形にして $z={rt}$。"],
              alt=[f"解は原点を中心とする半径 ${R}$ の円周上に、正{n}角形の頂点として等間隔に並ぶ（$n=2$ なら原点に関して対称な2点）。" if n > 2 else "解は原点に関して対称な2点になる。",
                   "因数分解（数学Ⅱ「複素数と方程式」）で解いて照合することもできる。例えば $z^3=8$ なら $(z-2)(z^2+2z+4)=0$。"],
              pc=[("$z$ を極形式でおきド・モアブルの定理を用いている", 2), ("絶対値を比較して $r$ を求めている", 1), ("偏角に $2k\\pi$ を加えて比較している", 2),
                  ("すべての解を正しく求めている", 3)],
              pit=["偏角に $2k\\pi$ を加え忘れ、解を1つしか求めない。", "$r^n$ の $n$ 乗根で $r>0$ を確認しない。"],
              chk=(f"solve(z**{n}-({cpy(w)}), z)", "[" + ", ".join(cpy(x) for x in roots) + "]", "set", "intermediate"))


@gen("thinking_writing", 3, ["cross_unit", "application"], rel=["HS-MATH2-U04"])
def ellipse_max(r):
    A, B = r.sample([1, 2, 3, 4, 5], 2)
    al, be = nonzero(r, -3, 3), nonzero(r, -3, 3)
    M2 = al * al * A * A + be * be * B * B
    Mt = sq_tex(M2)
    expr = f"{'' if al == 1 else ('-' if al == -1 else al)}x{'+' if be > 0 else '-'}{'' if abs(be) == 1 else abs(be)}y"
    return sa(f"点 $(x,\\,y)$ が楕円 ${sqfrac('x', A * A)}+{sqfrac('y', B * B)}=1$ 上を動くとき、${expr}$ の最大値と最小値を求めなさい。",
              f"最大値 ${Mt}$、最小値 $-{Mt}$",
              f"$x={A}\\cos\\theta,\\ y={B}\\sin\\theta$ とおくと ${expr}={al * A}\\cos\\theta{'+' if be * B > 0 else '-'}{abs(be * B)}\\sin\\theta$。三角関数の合成で振幅は $\\sqrt{{{(al * A) ** 2}+{(be * B) ** 2}}}={Mt}$。", d=4, p=8,
              ap="楕円上の点は媒介変数 $\\theta$ で $x=a\\cos\\theta,\\ y=b\\sin\\theta$ と表せる。すると式は $\\sin\\theta,\\ \\cos\\theta$ の1次式になり、三角関数の合成（数学Ⅱ）で最大・最小が分かる。",
              steps=[f"$x={'' if A == 1 else A}\\cos\\theta,\\ y={'' if B == 1 else B}\\sin\\theta\\ (0\\leqq\\theta<2\\pi)$ とおく。",
                     f"${expr}={al * A}\\cos\\theta{'+' if be * B > 0 else '-'}{abs(be * B)}\\sin\\theta$。",
                     f"合成すると ${Mt}\\sin(\\theta+\\alpha)$（$\\alpha$ は定数）。",
                     f"$-1\\leqq\\sin(\\theta+\\alpha)\\leqq1$ より、最大値 ${Mt}$、最小値 $-{Mt}$。"],
              alt=[f"${expr}=k$ とおき、直線と楕円が共有点をもつ条件（連立した2次方程式の判別式 $\\geqq0$）から $k$ の範囲を求めても同じ結果になる。"],
              pc=[("楕円を媒介変数で表している", 2), ("式を $\\theta$ の三角関数で表している", 2), ("合成して最大値・最小値を正しく求めている", 4)],
              pit=["$x=\\cos\\theta,\\ y=\\sin\\theta$ と、円の媒介変数表示をそのまま使ってしまう。", "合成の振幅を係数の和 $|" + f"{al * A}" + "|+|" + f"{be * B}" + "|$ と誤る。"],
              chk=(f"sqrt(({al * A})**2+({be * B})**2)", f"sqrt({M2})", None, "intermediate"))


SHAPES = [((1, Fraction(1, 2)), "$\\angle\\mathrm{A}=\\dfrac{\\pi}{2}$ の直角二等辺三角形"),
          ((1, Fraction(-1, 2)), "$\\angle\\mathrm{A}=\\dfrac{\\pi}{2}$ の直角二等辺三角形"),
          ((1, Fraction(1, 3)), "正三角形"), ((1, Fraction(-1, 3)), "正三角形"),
          ((2, Fraction(1, 2)), "$\\angle\\mathrm{A}=\\dfrac{\\pi}{2}$ の直角三角形（$\\mathrm{AC}=2\\mathrm{AB}$）"),
          ((2, Fraction(-1, 2)), "$\\angle\\mathrm{A}=\\dfrac{\\pi}{2}$ の直角三角形（$\\mathrm{AC}=2\\mathrm{AB}$）"),
          ((2, Fraction(1, 3)), "$\\angle\\mathrm{A}=\\dfrac{\\pi}{3},\\ \\mathrm{AC}=2\\mathrm{AB}$ の三角形（$\\angle\\mathrm{B}=\\dfrac{\\pi}{2}$ の直角三角形）")]


@gen("thinking_writing", 3, ["condition_check", "written_reasoning"])
def triangle_shape(r):
    (rho, f), name = r.choice(SHAPES)
    al = sp.Integer(r.randint(-3, 3)) + sp.I * r.randint(-3, 3)
    while True:
        d = sp.Integer(r.randint(-3, 3)) + sp.I * r.randint(-3, 3)
        if f.denominator == 3:
            d = sp.Integer(r.choice([-4, -2, 2, 4])) * r.choice([1, sp.I])
        if d != 0:
            break
    rot = zval(sp.Integer(rho), f)
    be = al + d
    ga = sp.nsimplify(sp.expand(al + d * rot))
    q = sp.nsimplify(sp.expand(rot))
    return sa(f"複素数平面上の3点 A$({ctex(al)})$、B$({ctex(be)})$、C$({ctex(ga)})$ を頂点とする $\\triangle\\mathrm{{ABC}}$ はどのような三角形か。$\\dfrac{{\\gamma-\\alpha}}{{\\beta-\\alpha}}$（$\\alpha,\\ \\beta,\\ \\gamma$ はそれぞれ A, B, C を表す複素数）を計算して、理由とともに答えなさい。",
              f"$\\dfrac{{\\gamma-\\alpha}}{{\\beta-\\alpha}}={ctex(q)}={polar_tex(sp.Integer(rho), f)}$ より、{name}",
              f"$\\dfrac{{\\gamma-\\alpha}}{{\\beta-\\alpha}}$ の絶対値は $\\dfrac{{\\mathrm{{AC}}}}{{\\mathrm{{AB}}}}={rho}$、偏角は $\\angle\\mathrm{{BAC}}$（向きつき）で ${atex(f)}$。", d=4, p=8,
              ap="$\\dfrac{\\gamma-\\alpha}{\\beta-\\alpha}$ は「$\\overrightarrow{\\mathrm{AB}}$ を何倍・何度回転すると $\\overrightarrow{\\mathrm{AC}}$ になるか」を表す。絶対値で辺の比、偏角で角 A が分かる。",
              steps=[f"$\\beta-\\alpha={ctex(d)}$、$\\gamma-\\alpha={ctex(ga - al)}$。",
                     f"$\\dfrac{{\\gamma-\\alpha}}{{\\beta-\\alpha}}=\\dfrac{{{ctex(ga - al)}}}{{{ctex(d)}}}={ctex(q)}$（分母の共役複素数を分母・分子にかける）。",
                     f"極形式で ${polar_tex(sp.Integer(rho), f)}$。", f"$\\mathrm{{AC}}:\\mathrm{{AB}}={rho}:1$、$\\angle\\mathrm{{BAC}}={atex(abs(f))}$。", f"よって{name}。"],
              alt=["3辺の長さ $|\\beta-\\alpha|,\\ |\\gamma-\\alpha|,\\ |\\gamma-\\beta|$ を計算し、三平方の定理や辺の比から形を判定しても同じ結論になる。"],
              pc=[("$\\dfrac{\\gamma-\\alpha}{\\beta-\\alpha}$ を正しく計算している", 3), ("絶対値と偏角を、辺の比と角に正しく読みかえている", 3), ("三角形の形を正しく答えている", 2)],
              pit=["偏角が負のとき、角の大きさを負の値で答える（角の大きさは絶対値）。", "絶対値が $1$ でないのに二等辺三角形と答える。"],
              chk=(f"simplify((({cpy(ga)})-({cpy(al)}))/(({cpy(be)})-({cpy(al)})))", cpy(q), None, "intermediate"))


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(stem, wrong, step, etype, tempt, fix, ans, expl, steps, ap, alt, pit, chk=None, d=3):
    return desc(f"{stem}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい答えを求めなさい。", ans, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい解答を途中式とともに示している", 3), ("最終的な答えが正しい", 1)], d=d, p=6, lines=6,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい途中式", 3), ("正しい答え", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix), chk=chk)


@gen("error_correction", 3, ["common_error", "concept"])
def err_arg(r):
    f = Fraction(r.choice([2, 4, 5, 7, 8, 10]), 6) if r.random() < 0.6 else Fraction(r.choice([3, 5]), 4)
    mod = sp.Integer(2 * r.randint(1, 3)) if f.denominator == 6 else r.randint(1, 3) * sp.sqrt(2)
    mod = sp.nsimplify(mod)
    z = zval(mod, f)
    # tan だけで決めた誤答：(-π/2, π/2) の角、負なら +2π
    wf = f - 1 if f > Fraction(1, 2) and f < Fraction(3, 2) else f
    wf = wf % 2
    if wf == f:
        wf = (f + 1) % 2
    re_, im_ = sp.re(z), sp.im(z)
    tanv = sp.nsimplify(im_ / re_)
    wrong = f"$|z|={sp.latex(mod)}$。$\\tan\\theta={sp.latex(tanv)}$ より $\\theta={atex(wf)}$。よって $z={polar_tex(mod, wf)}$"
    fix = f"点 $z$ は第{2 if (re_ < 0 and im_ > 0) else (3 if (re_ < 0 and im_ < 0) else (4 if im_ < 0 else 1))}象限にあるので、$\\cos\\theta={sp.latex(sp.nsimplify(re_ / mod))},\\ \\sin\\theta={sp.latex(sp.nsimplify(im_ / mod))}$ を満たす $\\theta={atex(f)}$。$z={polar_tex(mod, f)}$"
    return err_item(f"複素数 $z={ctex(z)}$ を極形式で表しなさい。ただし偏角 $\\theta$ は $0\\leqq\\theta<2\\pi$ とする。", wrong, "偏角を決める部分（$\\tan\\theta$ だけで判断）", "concept",
                    "$\\tan\\theta$ の値が同じ角は $\\pi$ ずつずれて2つあるのに、知っている角を1つ当てはめて象限を確かめていない。",
                    fix, f"$z={polar_tex(mod, f)}$", f"$\\tan\\theta$ の値だけでは偏角は決まらない。$\\cos\\theta,\\ \\sin\\theta$ の符号（点の象限）まで確認する。",
                    [f"$|z|={sp.latex(mod)}$。", f"$\\cos\\theta={sp.latex(sp.nsimplify(re_ / mod))}$、$\\sin\\theta={sp.latex(sp.nsimplify(im_ / mod))}$。", f"両方を満たす $\\theta={atex(f)}$。"],
                    "偏角は図をかいて象限を確認し、$\\cos\\theta$ と $\\sin\\theta$ の両方の値で決める。",
                    [f"生徒の答え ${polar_tex(mod, wf)}$ を $a+bi$ の形に戻すと ${ctex(zval(mod, wf))}$ となり、元の $z$ と一致しないことで誤りに気づける。"],
                    ["$\\tan\\theta$ だけで偏角を決める。"],
                    chk=(f"simplify(({sp.sstr(mod)})*(cos({apy(f)})+I*sin({apy(f)}))-({cpy(z)}))", "0", None, "intermediate"))


@gen("error_correction", 3, ["common_error", "condition_check"])
def err_conic_c(r):
    kind = r.choice(["ellipse", "hyperbola"])
    A, B = r.choice(ELL)
    if kind == "ellipse":
        eq = f"{sqfrac('x', A * A)}+{sqfrac('y', B * B)}=1"
        c, wc = sp.sqrt(A * A - B * B), sp.sqrt(A * A + B * B)
        wrong = f"$c=\\sqrt{{{A * A}+{B * B}}}={sp.latex(wc)}$ より、焦点は $({sp.latex(wc)},\\,0),\\ (-{sp.latex(wc)},\\,0)$"
        fix = f"楕円では $c=\\sqrt{{a^2-b^2}}=\\sqrt{{{A * A}-{B * B}}}={sp.latex(c)}$。焦点は $({sp.latex(c)},\\,0),\\ (-{sp.latex(c)},\\,0)$"
        rule, wrule = "楕円は $c^2=a^2-b^2$", "双曲線の関係 $c^2=a^2+b^2$"
        chk = (f"sqrt({A * A}-{B * B})", sp.sstr(c), None, "intermediate")
    else:
        a, b = r.randint(2, 6), r.randint(1, 5)
        if a == b:
            b = a - 1
        if b > a:
            a, b = b, a
        eq = f"\\dfrac{{x^2}}{{{a * a}}}-{sqfrac('y', b * b)}=1"
        c, wc = sp.sqrt(a * a + b * b), sp.sqrt(a * a - b * b)
        wrong = f"$c=\\sqrt{{{a * a}-{b * b}}}={sp.latex(wc)}$ より、焦点は $({sp.latex(wc)},\\,0),\\ (-{sp.latex(wc)},\\,0)$"
        fix = f"双曲線では $c=\\sqrt{{a^2+b^2}}=\\sqrt{{{a * a}+{b * b}}}={sp.latex(c)}$。焦点は $({sp.latex(c)},\\,0),\\ (-{sp.latex(c)},\\,0)$"
        rule, wrule = "双曲線は $c^2=a^2+b^2$", "楕円の関係 $c^2=a^2-b^2$"
        chk = (f"sqrt({a * a}+{b * b})", sp.sstr(c), None, "intermediate")
    name = "楕円" if kind == "ellipse" else "双曲線"
    return err_item(f"{name} ${eq}$ の焦点の座標を求めなさい。", wrong, "$c$ を求める式", "formula",
                    f"楕円と双曲線の公式はよく似ており、{wrule}を取り違えて覚えている。",
                    fix, f"$({sp.latex(c)},\\,0),\\ (-{sp.latex(c)},\\,0)$", f"{rule}。",
                    [f"{name}の焦点の公式を確認する：{rule}。", f"$c={sp.latex(c)}$。", f"焦点 $(\\pm{sp.latex(c)},\\,0)$。"],
                    "楕円では焦点が曲線の内側にあるので $c<a$、双曲線では焦点が頂点の外側にあるので $c>a$。図で大小を確かめると公式の符号を判断できる。",
                    [("楕円では焦点は長軸の端 $(\\pm" + f"{A}" + ",\\,0)$ より内側にあるはずで、生徒の値は外側にあるので誤りとわかる。") if kind == "ellipse"
                     else ("双曲線では焦点は頂点 $(\\pm" + f"{a}" + ",\\,0)$ より外側にあるはずで、生徒の値は内側にあるので誤りとわかる。")],
                    ["楕円と双曲線で $c^2$ の式を取り違える。"], chk=chk, d=2)


@gen("error_correction", 2, ["common_error", "computation"])
def err_demoivre(r):
    while True:
        mod, f = nice_point(r)
        if mod != 1 and f.denominator > 2:
            break
    if f.denominator == 6:
        mod = sp.Integer(2)
    n = r.randint(3, 6)
    z = zval(mod, f)
    w = sp.nsimplify(sp.expand(z ** n))
    ww = sp.nsimplify(sp.expand(mod * zval(sp.Integer(1), f * n)))
    wrong = f"${ctex(z)}={polar_tex(mod, f)}$ より、$\\left({ctex(z)}\\right)^{{{n}}}={sp.latex(mod)}\\left(\\cos {atex(f * n)}+i\\sin {atex(f * n)}\\right)={ctex(ww)}$"
    fix = f"$\\left({ctex(z)}\\right)^{{{n}}}=({sp.latex(mod)})^{{{n}}}\\left(\\cos {atex(f * n)}+i\\sin {atex(f * n)}\\right)={ctex(w)}$"
    return err_item(f"$\\left({ctex(z)}\\right)^{{{n}}}$ を計算しなさい。", wrong, "累乗した後の絶対値", "formula",
                    "ド・モアブルの定理 $(\\cos\\theta+i\\sin\\theta)^n=\\cos n\\theta+i\\sin n\\theta$ を、絶対値が $1$ でない場合にもそのまま当てはめた。",
                    fix, f"${ctex(w)}$", f"$\\{{r(\\cos\\theta+i\\sin\\theta)\\}}^n=r^n(\\cos n\\theta+i\\sin n\\theta)$。絶対値も ${n}$ 乗する。",
                    [f"${ctex(z)}={polar_tex(mod, f)}$。", f"絶対値は $({sp.latex(mod)})^{{{n}}}={sp.latex(sp.expand(mod ** n))}$、偏角は ${atex(f * n)}$。", f"${ctex(w)}$。"],
                    "積の性質「絶対値はかけ算」を $n$ 回くり返すと、絶対値は $r^n$ になる。",
                    [f"$|z^{{{n}}}|=|z|^{{{n}}}={sp.latex(sp.expand(mod ** n))}$ のはずだが、生徒の答えの絶対値は ${sp.latex(mod)}$ であり一致しない。"],
                    ["絶対値の $n$ 乗を忘れる。"], chk=(f"expand(({cpy(z)})**{n})", cpy(w), None, "intermediate"))


@gen("error_correction", 2, ["common_error", "condition_check"])
def err_param_range(r):
    kind = r.choice(["half", "trig"])
    if kind == "half":
        p, q = r.randint(-4, 4), r.randint(-4, 4)
        m = nonzero(r, -3, 3)
        stem = f"x=t^2{'' if p == 0 else (f'+{p}' if p > 0 else p)},\\ y={'' if m == 1 else ('-' if m == -1 else m)}t^2{'' if q == 0 else (f'+{q}' if q > 0 else q)}"
        k = q - m * p
        line = f"y={'' if m == 1 else ('-' if m == -1 else m)}x{'' if k == 0 else (f'+{k}' if k > 0 else k)}"
        rng = f"x\\geqq{p}"
        wrong = f"$t^2=x{'' if p == 0 else ('-' + str(p) if p > 0 else '+' + str(-p))}$ を代入して ${line}$。よって直線 ${line}$"
        fix = f"$t^2\\geqq0$ より $x\\geqq{p}$。よって直線 ${line}$ のうち $x\\geqq{p}$ の部分（半直線）"
        why = f"$t^2\\geqq0$ なので $x=t^2{'' if p == 0 else (f'+{p}' if p > 0 else p)}\\geqq{p}$。"
        chk = (f"expand(({m})*t**2+({q})-(({m})*(t**2+({p}))+({k})))", "0", None, "intermediate")
        ans = f"直線 ${line}$ の $x\\geqq{p}$ の部分"
    else:
        a = r.randint(1, 4)
        c = nonzero(r, -3, 3)
        stem = f"x={'' if a == 1 else a}\\cos\\theta,\\ y={'' if c == 1 else ('-' if c == -1 else c)}\\cos2\\theta"
        k2 = Fraction(2 * c, a * a)
        line = f"y={frac(k2.numerator, k2.denominator) if abs(k2) != 1 else ('' if k2 == 1 else '-')}x^2{'+' if -c > 0 else '-'}{abs(c)}"
        rng = f"-{a}\\leqq x\\leqq{a}"
        xa = "x" if a == 1 else f"\\dfrac{{x}}{{{a}}}"
        wrong = f"$\\cos2\\theta=2\\cos^2\\theta-1$ に $\\cos\\theta={xa}$ を代入して ${line}$。よって放物線 ${line}$"
        fix = f"$-1\\leqq\\cos\\theta\\leqq1$ より ${rng}$。よって放物線 ${line}$ のうち ${rng}$ の部分"
        why = f"$x={'' if a == 1 else a}\\cos\\theta$ で $-1\\leqq\\cos\\theta\\leqq1$ なので ${rng}$。"
        chk = (f"simplify(({c})*cos(2*theta)-(({fr_py(k2.numerator, k2.denominator)})*({a}*cos(theta))**2-({c})))", "0", None, "intermediate")
        ans = f"放物線 ${line}$ の ${rng}$ の部分"
    return err_item(f"媒介変数表示 ${stem}$ で表される点 $(x,\\,y)$ が描く図形を求めなさい。", wrong, "最後の結論（$x$ の範囲の検討もれ）", "condition",
                    "媒介変数を消去した式を求めた時点で解き終わったと考え、もとの媒介変数表示から生じる $x$ の範囲の制限を確認していない。",
                    fix, ans, why,
                    ["媒介変数を消去して $x,\\ y$ の関係式を求める。", "媒介変数のとりうる値から、$x$ のとりうる範囲を調べる。", f"${rng}$ の部分に限られる。"],
                    "消去した式は「必要条件」にすぎない。$x$ がどんな値をとれるかを確かめて、図形の範囲を決める。",
                    ["範囲外の $x$ の値（例えば範囲の外側の整数）を代入して、対応する媒介変数が存在しないことを確かめると、制限の必要性がはっきりする。"],
                    ["消去した式だけを答え、範囲を書かない。"], chk=chk)


GENERATORS = [parabola_focus, ellipse_focus, polar_form, param_elim,
              demoivre_power, product_quotient, rotation, hyperbola, conic_from_def,
              roots_eq, ellipse_max, triangle_shape,
              err_arg, err_conic_c, err_demoivre, err_param_range]
