"""単元パック：物理 力学（運動量と力積・反発係数、等速円運動、単振動、万有引力とケプラーの法則）。"""
import math
from decimal import ROUND_HALF_UP, Decimal

import sympy as sp

from banks._common import desc, figure, mc, num, plane
from hs_pack_lib import board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem, tp

UNIT_ID = "HS-PHY-U01"

G = sp.Rational("9.8")
GS = "重力加速度の大きさを $9.8\\,\\mathrm{m/s^2}$ とする。"
RE = sp.Rational(64, 10) * 10 ** 6
RS = "地球の半径を $6.4\\times10^6\\,\\mathrm{m}$、地表での重力加速度の大きさを $9.8\\,\\mathrm{m/s^2}$ とし、地球の自転の影響は無視する。"


# ----------------------------------------------------------------------
# 数値の整形（有効数字）と検算
# ----------------------------------------------------------------------

def Q(s):
    return sp.Rational(s)


def dec(x):
    x = sp.Rational(x)
    d = Decimal(int(x.p)) / Decimal(int(x.q))
    return format(d.normalize(), "f")


def sig(x, n=2):
    """有効数字 n 桁に四捨五入した表記。桁が大きい・小さいときは a×10^k の LaTeX を返す。"""
    x = sp.nsimplify(x)
    if x == 0:
        return "0"
    d = Decimal(str(sp.N(x, 40)))
    e = d.adjusted()
    r = d.quantize(Decimal(1).scaleb(e - n + 1), rounding=ROUND_HALF_UP)
    if r.adjusted() != e:
        e = r.adjusted()
        r = d.quantize(Decimal(1).scaleb(e - n + 1), rounding=ROUND_HALF_UP)
    if e >= n or e <= -4:
        return f"{format(r.scaleb(-e), 'f')}\\times10^{{{e}}}"
    return format(r, "f")


def is_exact(s, x):
    try:
        return "times" not in s and sp.Rational(s) == sp.nsimplify(x)
    except (TypeError, ValueError):
        return False


def bestn(x):
    if is_exact(sig(x, 2), x):
        return 2
    return 3 if is_exact(sig(x, 3), x) else 2


def numq(stem, x, expr, e, unit, n=None, **kw):
    """数値の答えの問題。x は厳密値、expr はそれを求める式（検算用）。"""
    n = n or bestn(x)
    s = sig(x, n)
    exact = is_exact(s, x)
    if not exact and "有効数字" not in stem:
        stem += f"有効数字{n}桁で答えなさい。"
    ans = s if "times" not in s else f"${s}$"
    xs = str(sp.sympify(x))
    chk = (expr, xs) if exact else (expr, xs, None, "intermediate")
    return num(stem, ans, e, unit=unit, chk=chk, **kw)


def t(x, n=None):
    return sig(x, n or bestn(x))


def P(x):
    return f"({sp.nsimplify(x)})"


def iv(n):
    """整数の測定値を有効数字2桁で表示（10 未満は 3.0 のように小数第1位まで）。"""
    return f"{n}.0" if abs(n) < 10 else f"{n}"


def fin(x, places=2):
    """小数第 places 位までで割り切れるか。"""
    return (sp.Rational(x) * 10 ** places).q == 1


SIN = {30: sp.Rational(1, 2), 45: sp.sqrt(2) / 2, 60: sp.sqrt(3) / 2}
COS = {30: sp.sqrt(3) / 2, 45: sp.sqrt(2) / 2, 60: sp.Rational(1, 2)}
SIN_TEX = {30: "\\dfrac{1}{2}", 45: "\\dfrac{\\sqrt{2}}{2}", 60: "\\dfrac{\\sqrt{3}}{2}"}
COS_TEX = {30: "\\dfrac{\\sqrt{3}}{2}", 45: "\\dfrac{\\sqrt{2}}{2}", 60: "\\dfrac{1}{2}"}


# ----------------------------------------------------------------------
# 図
# ----------------------------------------------------------------------

def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="serif" font-size="12">'
            '<defs><marker id="ah" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#000"/></marker></defs>'
            f'{body}</svg>')


def arrow(x1, y1, x2, y2, lab="", lx=0, ly=-6, color="#000"):
    s = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="1.5" marker-end="url(#ah)"/>'
    if lab:
        s += f'<text x="{(x1 + x2) / 2 + lx}" y="{(y1 + y2) / 2 + ly}" text-anchor="middle">{lab}</text>'
    return s


def collision_svg(la, lb, va, vb=""):
    """一直線上の2球の衝突前の図。va, vb は速度のラベル（vb='' なら B は静止）。"""
    body = '<line x1="10" y1="70" x2="290" y2="70" stroke="#000"/>'
    body += '<circle cx="80" cy="55" r="15" fill="#cfdcec" stroke="#000"/><circle cx="210" cy="55" r="15" fill="#f3d9c6" stroke="#000"/>'
    body += f'<text x="80" y="59" text-anchor="middle">A</text><text x="210" y="59" text-anchor="middle">B</text>'
    body += f'<text x="80" y="90" text-anchor="middle">{la}</text><text x="210" y="90" text-anchor="middle">{lb}</text>'
    body += arrow(70, 25, 120, 25, va)
    body += arrow(220, 25, 170, 25, vb) if vb else '<text x="210" y="28" text-anchor="middle">静止</text>'
    return svg(300, 100, body)


def circle_svg():
    body = '<circle cx="110" cy="100" r="70" fill="none" stroke="#000" stroke-width="1.2"/>'
    body += '<circle cx="110" cy="100" r="2.5" fill="#000"/><text x="96" y="114">O</text>'
    body += '<line x1="110" y1="100" x2="180" y2="100" stroke="#000" stroke-dasharray="4 3"/><text x="140" y="94">r</text>'
    body += '<circle cx="180" cy="100" r="6" fill="#cfdcec" stroke="#000"/>'
    body += arrow(180, 100, 180, 40, "v", 10, 0)
    body += arrow(174, 100, 130, 100, "F", 0, 16, "#1f4e79")
    body += '<path d="M 150 100 A 40 40 0 0 0 138 72" fill="none" stroke="#555"/><text x="152" y="80" font-size="11">ωt</text>'
    return svg(230, 190, body)


def conical_svg():
    body = '<line x1="40" y1="20" x2="220" y2="20" stroke="#000" stroke-width="2"/>'
    body += '<line x1="130" y1="20" x2="190" y2="140" stroke="#000" stroke-width="1.2"/>'
    body += '<line x1="130" y1="20" x2="130" y2="150" stroke="#000" stroke-dasharray="4 3"/>'
    body += '<ellipse cx="130" cy="140" rx="60" ry="14" fill="none" stroke="#555" stroke-dasharray="3 3"/>'
    body += '<circle cx="190" cy="140" r="7" fill="#cfdcec" stroke="#000"/>'
    body += '<text x="136" y="52">θ</text><text x="166" y="78">L</text><text x="200" y="128">m</text>'
    body += arrow(190, 147, 190, 185, "mg", 16, 4)
    return svg(260, 195, body)


def orbit_svg():
    body = '<circle cx="130" cy="110" r="38" fill="#cfdcec" stroke="#000"/><text x="118" y="114">地球</text>'
    body += '<circle cx="130" cy="110" r="90" fill="none" stroke="#000" stroke-dasharray="5 3"/>'
    body += '<circle cx="220" cy="110" r="6" fill="#f3d9c6" stroke="#000"/><text x="228" y="128">人工衛星</text>'
    body += '<line x1="130" y1="110" x2="214" y2="110" stroke="#000"/><text x="160" y="104">r</text>'
    body += arrow(220, 110, 220, 50, "v", 10, 0)
    return svg(290, 220, body)


def loop_svg():
    body = '<path d="M 10 30 Q 60 190 150 190 L 230 190" fill="none" stroke="#000" stroke-width="1.5"/>'
    body += '<circle cx="230" cy="140" r="50" fill="none" stroke="#000" stroke-width="1.5"/>'
    body += '<circle cx="18" cy="38" r="7" fill="#cfdcec" stroke="#000"/>'
    body += '<line x1="300" y1="30" x2="300" y2="190" stroke="#555"/><text x="306" y="110">h</text>'
    body += '<line x1="230" y1="140" x2="230" y2="90" stroke="#000" stroke-dasharray="3 3"/><text x="234" y="120">r</text>'
    body += '<text x="226" y="84">P</text><line x1="0" y1="190" x2="320" y2="190" stroke="#000"/>'
    return svg(330, 200, body)


def shm_svg(A=2, T=4):
    return plane((0, 8.6), (-A - 0.8, A + 0.8), unit=26, grid=True, ticks=True,
                 curves=[(lambda x: A * math.sin(2 * math.pi * x / T) if 0 <= x <= 8 else float("nan"), "")], xl="t", yl="x")


# ======================================================================
# 授業プリント
# ======================================================================

LESSON = lesson(
    goals=["運動量と力積の関係を運動方程式から導き、衝突・分裂で運動量保存則と反発係数を使い分けて速度を求められる。",
           "等速円運動の角速度・周期・向心加速度を定義し、向心力を「実在の力の合力」として見つけて運動方程式を立てられる。",
           "単振動を等速円運動の正射影として理解し、$F=-kx$ から周期 $T=2\\pi\\sqrt{\\dfrac{m}{k}}$ を導いてばね振り子・単振り子に適用できる。",
           "万有引力の法則と円軌道の運動方程式から、人工衛星の速さ・周期とケプラーの第3法則を導ける。"],
    duration=100,
    readiness=["運動方程式 $ma=F$ を、物体ごとに力を図示して立てられる（物理基礎）。",
               "運動エネルギー・位置エネルギーと力学的エネルギー保存則を使える（物理基礎）。",
               "弧度法と三角関数 $\\sin\\omega t$、$\\cos\\omega t$ のグラフをかける（数学Ⅱ）。"],
    flow=[("導入：ビリヤードと人工衛星", 5, "衝突・回転・振動・天体の運動が、すべて運動方程式から説明できることを予告する"),
          ("運動量と力積", 15, "力積 $F\\Delta t=\\Delta p$ の導出、平均の力、運動量保存則（作用反作用から導く）"),
          ("衝突と反発係数", 15, "反発係数の定義、弾性衝突・非弾性衝突と運動エネルギーの損失（例題1）"),
          ("等速円運動", 20, "角速度・周期、向心加速度の導出、向心力の見つけ方、円錐振り子（例題2）"),
          ("単振動", 20, "等速円運動の正射影、$a=-\\omega^2x$、ばね振り子と単振り子の周期"),
          ("万有引力", 15, "万有引力の法則、$GM=gR^2$、人工衛星とケプラーの法則（例題3）"),
          ("まとめ", 10, "保存則と運動方程式の使い分けを板書で整理し、課題を指示")],
    sections=[
        intro("in1", "「保存される量」と「回る・揺れる運動」",
              "ビリヤードの球がぶつかると、衝突の間にはたらく力は複雑で、時間とともに大きく変わる。それでも衝突の前後だけを比べれば、速度を正確に予言できる。その鍵が運動量の保存である。また、円運動や振り子の往復運動、地球のまわりを回る人工衛星も、物理基礎で学んだ運動方程式 $ma=F$ を「回る運動」「揺れる運動」に当てはめることで統一的に扱える。",
              bullets=["衝突・分裂：力の詳細がわからなくても、運動量保存則と反発係数で前後を結ぶ。",
                       "円運動・単振動・天体の運動：加速度の向きと大きさを正しくとらえ、運動方程式を立てる。"],
              points=[tp("静止した球に同じ質量の球を正面衝突させる実演（または動画）で、当てた球が止まり当てられた球が同じ速さで動き出すことを観察させる。",
                         ask="当てた球が止まったのはなぜだろうか。ぶつかる直前の「勢い」はどこへ行ったか。",
                         expect="相手の球に移った、という答えが出る。これを運動量の保存として定式化する。", timing="授業の冒頭")]),
        definition("df1", "運動量と力積",
                   "質量 $m$〔kg〕の物体が速度 $\\vec{v}$〔m/s〕で運動しているとき、$\\vec{p}=m\\vec{v}$ を運動量という。物体に力 $\\vec{F}$ が時間 $\\Delta t$ だけはたらくとき、$\\vec{F}\\Delta t$ を力積という。",
                   formula="$$\\vec{p}=m\\vec{v}\\ \\mathrm{[kg\\cdot m/s]},\\qquad m\\vec{v'}-m\\vec{v}=\\vec{F}\\Delta t\\ \\mathrm{[N\\cdot s]}$$",
                   conditions=["運動量の変化は、その間に受けた力積に等しい。運動量も力積も向きをもつ量（ベクトル）である。",
                               "力が変化するときは、$F$ を平均の力 $\\overline{F}$ と読みかえる。$F$−$t$ グラフの面積が力積を表す。",
                               "一直線上では正の向きを決め、向きを符号で表す。はね返る運動では、衝突後の速度の符号が変わる。",
                               "単位：$1\\,\\mathrm{N\\cdot s}=1\\,\\mathrm{kg\\cdot m/s}$。"],
                   points=[tp("運動方程式 $m\\dfrac{v'-v}{\\Delta t}=F$ の両辺に $\\Delta t$ をかけるだけで力積の式が得られることを、生徒自身に導かせる。",
                              ask="卵を床に落とすと割れるが、座布団の上なら割れにくいのはなぜか。",
                              expect="運動量の変化（力積）は同じだが、止まるまでの時間が長いので平均の力が小さい。"),
                           tp("壁ではね返るボールの運動量の変化を、「正の向き」を決めて符号つきで計算させる。",
                              caution="速さの差 $m(v-v')$ として計算し、はね返りでは和になることを見落とす誤りが多い。")]),
        theorem("th1", "運動量保存則",
                "$$m_1\\vec{v_1}+m_2\\vec{v_2}=m_1\\vec{v_1'}+m_2\\vec{v_2'}$$",
                ["物体系に外力がはたらかない（または外力の力積が無視できる）とき、系全体の運動量の和は保存される。",
                 "衝突・分裂・合体のように、物体どうしが互いに及ぼし合う力（内力）だけで速度が変わる場合に使える。",
                 "ある方向にだけ外力がない場合は、その方向の成分について運動量が保存される。",
                 "運動量が保存されても、運動エネルギーが保存されるとは限らない（一般に衝突で減少する）。"],
                body="衝突の間の力がどれほど複雑でも、作用・反作用の法則により2物体が受ける力積は大きさが等しく向きが逆なので、和をとると打ち消し合う。",
                proof=["衝突の間に A が B から受ける力を $\\vec{F}$ とすると、作用・反作用の法則より B が A から受ける力は $-\\vec{F}$。2つの力がはたらく時間 $\\Delta t$ は等しい。",
                       "A について：$m_1\\vec{v_1'}-m_1\\vec{v_1}=\\vec{F}\\Delta t$。B について：$m_2\\vec{v_2'}-m_2\\vec{v_2}=-\\vec{F}\\Delta t$。",
                       "2式を辺々加えると右辺は $\\vec{0}$ になり、$m_1\\vec{v_1}+m_2\\vec{v_2}=m_1\\vec{v_1'}+m_2\\vec{v_2'}$ が得られる。"],
                figure=figure("なめらかな水平面上で、質量 m₁ の球 A が速度 v₁ で、質量 m₂ の球 B が速度 v₂ で向かい合って進み、正面衝突する直前の図",
                              collision_svg("m₁", "m₂", "v₁", "v₂"), caption="衝突の前後で運動量の和は変わらない"),
                points=[tp("証明で作用・反作用の法則のどこを使ったかを確認させ、「内力の力積は系全体では打ち消し合う」とまとめる。", timing="証明の直後",
                           ask="摩擦のある床の上での衝突でも運動量保存則を使ってよいのはどんなときか。",
                           expect="衝突時間がきわめて短く、摩擦力の力積が衝突の力積に比べて無視できるとき。")]),
        definition("df2", "反発係数（はね返り係数）",
                   "一直線上で2物体が衝突するとき、衝突後に離れる速さと衝突前に近づく速さの比を反発係数 $e$ という。床や壁との衝突では、相手の速度を 0 とみなす。",
                   formula="$$e=-\\dfrac{v_1'-v_2'}{v_1-v_2}\\qquad(0\\leqq e\\leqq1),\\qquad \\text{床・壁：}\\ e=\\dfrac{|v'|}{|v|}$$",
                   conditions=["$e=1$：弾性衝突（運動エネルギーが保存される）。$0\\leqq e<1$：非弾性衝突。$e=0$：完全非弾性衝突（衝突後に一体となる）。",
                               "速度は向きを含めた値（符号つき）で代入する。速さ（大きさ）だけを代入すると誤る。",
                               "高さ $h$ から落とした球が床で $e$ ではね返ると、はね返りの高さは $e^2h$ になる。",
                               "なめらかな面との斜めの衝突では、面に平行な速度成分は変わらず、垂直な成分だけが $e$ 倍になって向きが逆になる。"],
                   points=[tp("運動量保存則と反発係数の式を連立すると、2物体の衝突後の速度が必ず決まることを確認させる（未知数2つ、式2つ）。",
                              ask="質量が等しい2球が弾性衝突すると、衝突後の速度はどうなるか。", expect="速度が入れかわる。")]),
        definition("df3", "等速円運動",
                   "半径 $r$〔m〕の円周上を一定の速さ $v$ で回る運動を等速円運動という。中心のまわりに単位時間あたりに回転する角を角速度 $\\omega$〔rad/s〕、1周にかかる時間を周期 $T$〔s〕という。",
                   formula="$$v=r\\omega,\\qquad T=\\dfrac{2\\pi}{\\omega}=\\dfrac{2\\pi r}{v},\\qquad a=r\\omega^2=\\dfrac{v^2}{r},\\qquad m\\dfrac{v^2}{r}=F$$",
                   conditions=["加速度の向きは常に円の中心向き（向心加速度）。速さは一定でも速度の向きが変わるので、加速度は 0 ではない。",
                               "向心力 $F$ は新しい種類の力ではない。張力・重力・垂直抗力・摩擦力・万有引力など、実際にはたらく力の「中心向きの成分の和」である。",
                               "回転数 $n$〔回/s〕を用いると $\\omega=2\\pi n$。角は弧度法（rad）で表す。",
                               "物体とともに回転する立場から見ると、中心から外向きに大きさ $m\\dfrac{v^2}{r}$ の慣性力（遠心力）を考えて、力のつり合いとして扱える。2つの立場を混ぜない。"],
                   figure=figure("半径 r の円周上を速さ v で回る物体。速度 v は円の接線方向、向心力 F は中心 O の向き", circle_svg(),
                                 caption="速度は接線方向、加速度と向心力は中心向き"),
                   points=[tp("「向心力」を力の図にもう1本書き加える誤りを防ぐため、まず実在の力だけを図示し、その合力が中心を向くことを確かめさせる。",
                              ask="糸につけたおもりを水平面内で回すとき、おもりにはたらく力は何と何か。",
                              expect="重力と糸の張力の2つだけ。その合力が向心力になる。",
                              caution="「重力・張力・向心力の3つ」と答える生徒が多い。")]),
        derivation("dv1", "向心加速度 $a=\\dfrac{v^2}{r}$ の導出",
                   ["速さ $v$ で回る物体が、短い時間 $\\Delta t$ に角 $\\Delta\\theta=\\omega\\Delta t$ だけ回転したとする。速度ベクトルも同じ角 $\\Delta\\theta$ だけ向きを変える。",
                    "速度の変化 $\\Delta\\vec{v}$ は、2辺が $v$ で頂角 $\\Delta\\theta$ の二等辺三角形の底辺。$\\Delta\\theta$ が小さいとき、その大きさは弧の長さで近似でき $|\\Delta\\vec{v}|\\fallingdotseq v\\Delta\\theta$。",
                    "加速度の大きさは $a=\\dfrac{|\\Delta\\vec{v}|}{\\Delta t}=v\\dfrac{\\Delta\\theta}{\\Delta t}=v\\omega$。$v=r\\omega$ を用いて $a=r\\omega^2=\\dfrac{v^2}{r}$。",
                    "$\\Delta t\\to0$ のとき、$\\Delta\\vec{v}$ の向きは速度に垂直、すなわち円の中心を向く。"],
                   body="同じ結果は、位置を $x=r\\cos\\omega t$、$y=r\\sin\\omega t$ と表し、時間で2回微分して $\\vec{a}=-\\omega^2\\vec{r}$ を得ることでも確かめられる（数学Ⅲの微分）。",
                   points=[tp("速度ベクトルを円の外に平行移動して始点をそろえ、$\\Delta\\vec{v}$ が中心を向くことを図で示す。",
                              ask="速さが一定なのに加速度があるのはなぜか。", expect="速度の向きが変化しているから（加速度は速度の変化率）。")]),
        theorem("th2", "単振動",
                "$$x=A\\sin\\omega t,\\quad v=A\\omega\\cos\\omega t,\\quad a=-\\omega^2x,\\qquad F=-Kx\\ \\Rightarrow\\ T=2\\pi\\sqrt{\\dfrac{m}{K}}$$",
                ["単振動は、等速円運動（半径 $A$、角速度 $\\omega$）を直径上に正射影した運動である。$A$ を振幅、$\\omega$ を角振動数という。",
                 "物体にはたらく合力が、つり合いの位置からの変位 $x$ に比例し逆向き（復元力 $F=-Kx$）のとき、物体は単振動をする。",
                 "ばね振り子：$T=2\\pi\\sqrt{\\dfrac{m}{k}}$（鉛直につるしても同じ）。単振り子（振れ角が小さいとき）：$T=2\\pi\\sqrt{\\dfrac{L}{g}}$。",
                 "周期は振幅によらない（等時性）。速さはつり合いの位置で最大 $A\\omega$、加速度の大きさは両端で最大 $A\\omega^2$。"],
                body="ばね振り子では運動方程式 $ma=-kx$ と $a=-\\omega^2x$ を比べて $\\omega=\\sqrt{\\dfrac{k}{m}}$。単振り子では、振れ角 $\\theta$ が小さいとき接線方向の力が $-mg\\sin\\theta\\fallingdotseq-\\dfrac{mg}{L}x$ となり、$K=\\dfrac{mg}{L}$ の単振動とみなせる。",
                proof=["等速円運動する点の加速度は中心向きで大きさ $A\\omega^2$。これを $x$ 軸上に射影すると $a=-A\\omega^2\\sin\\omega t=-\\omega^2x$。",
                       "運動方程式 $ma=-Kx$ に $a=-\\omega^2x$ を代入すると $m\\omega^2=K$、よって $\\omega=\\sqrt{\\dfrac{K}{m}}$。",
                       "周期は $T=\\dfrac{2\\pi}{\\omega}=2\\pi\\sqrt{\\dfrac{m}{K}}$。$A$ を含まないので、振幅によらない。"],
                figure=figure("単振動の x−t グラフ。振幅 2、周期 4 の正弦曲線", shm_svg(), caption="x−t グラフ：振幅 A と周期 T を読む"),
                points=[tp("鉛直ばね振り子では重力があっても周期が変わらない理由を、「つり合いの位置からの変位」で式を立て直して確かめさせる。",
                           ask="ばね振り子を月面に持っていくと周期はどうなるか。単振り子ではどうか。",
                           expect="ばね振り子は変わらない。単振り子は $g$ が小さいので長くなる。")]),
        theorem("th3", "万有引力の法則とケプラーの法則",
                "$$F=G\\dfrac{Mm}{r^2},\\qquad GM=gR^2,\\qquad m\\dfrac{v^2}{r}=G\\dfrac{Mm}{r^2}\\ \\Rightarrow\\ v=\\sqrt{\\dfrac{GM}{r}},\\quad \\dfrac{T^2}{r^3}=\\dfrac{4\\pi^2}{GM}$$",
                ["$G$ は万有引力定数（約 $6.67\\times10^{-11}\\,\\mathrm{N\\cdot m^2/kg^2}$）。$r$ は2物体の中心間の距離（地表からの高さではない）。",
                 "地表では重力 $mg$ が万有引力に等しいとみなせるので $mg=G\\dfrac{Mm}{R^2}$、すなわち $GM=gR^2$（$R$ は地球の半径）。",
                 "ケプラーの法則：第1法則（惑星は太陽を1つの焦点とする楕円軌道を描く）、第2法則（面積速度一定）、第3法則（$\\dfrac{T^2}{a^3}$ はすべての惑星で等しい）。",
                 "万有引力による位置エネルギーは $U=-G\\dfrac{Mm}{r}$（無限遠を基準）。地表から無限遠に飛び去るのに必要な最小の速さ（第2宇宙速度）は $\\sqrt{2gR}$。"],
                proof=["人工衛星（質量 $m$）が地球（質量 $M$）を中心とする半径 $r$ の等速円運動をしているとき、向心力は万有引力である：$m\\dfrac{v^2}{r}=G\\dfrac{Mm}{r^2}$。",
                       "よって $v=\\sqrt{\\dfrac{GM}{r}}$。周期は $T=\\dfrac{2\\pi r}{v}=2\\pi\\sqrt{\\dfrac{r^3}{GM}}$。",
                       "両辺を2乗して $\\dfrac{T^2}{r^3}=\\dfrac{4\\pi^2}{GM}$。右辺は中心天体だけで決まるので、円軌道についてケプラーの第3法則が導かれる。"],
                figure=figure("地球を中心とする半径 r の円軌道を、速さ v で回る人工衛星", orbit_svg(), caption="万有引力が向心力になる"),
                points=[tp("$r$ に「地表からの高さ」を代入する誤りを防ぐため、図に地球の中心を必ずかかせ、$r=R+h$ と書かせる。",
                           caution="高さ $h=R$ の衛星の軌道半径は $2R$ である。")]),
        example("ex1", "例題1　反発係数を用いた衝突",
                "なめらかな水平面上で、右向きに速さ $4.0\\,\\mathrm{m/s}$ で進む質量 $2.0\\,\\mathrm{kg}$ の球 A が、静止している質量 $3.0\\,\\mathrm{kg}$ の球 B に正面衝突した。反発係数を $0.50$ とするとき、衝突後の A、B の速度と、衝突による運動エネルギーの減少量を求めよ。",
                ["右向きを正とし、衝突後の速度を $v_{\\mathrm{A}}'$、$v_{\\mathrm{B}}'$ とする。運動量保存：$2.0\\times4.0=2.0v_{\\mathrm{A}}'+3.0v_{\\mathrm{B}}'$。",
                 "反発係数：$v_{\\mathrm{B}}'-v_{\\mathrm{A}}'=0.50\\times(4.0-0)=2.0$。",
                 "連立して $v_{\\mathrm{A}}'=0.40\\,\\mathrm{m/s}$、$v_{\\mathrm{B}}'=2.4\\,\\mathrm{m/s}$（どちらも右向き）。",
                 "運動エネルギー：衝突前 $\\dfrac12\\times2.0\\times4.0^2=16\\,\\mathrm{J}$、衝突後 $\\dfrac12\\times2.0\\times0.40^2+\\dfrac12\\times3.0\\times2.4^2=0.16+8.64=8.8\\,\\mathrm{J}$。減少量 $7.2\\,\\mathrm{J}$。"],
                "A：右向き $0.40\\,\\mathrm{m/s}$、B：右向き $2.4\\,\\mathrm{m/s}$、減少量 $7.2\\,\\mathrm{J}$",
                thinking="未知数が2つなので式も2つ必要。運動量保存則と反発係数の式を、同じ「正の向き」で立てる。",
                figure=figure("右向きに進む球 A（2.0 kg、4.0 m/s）と静止している球 B（3.0 kg）", collision_svg("2.0 kg", "3.0 kg", "4.0 m/s")),
                misconceptions=[("運動量が保存されるので、運動エネルギーも保存される", "運動エネルギーが保存されるのは $e=1$ のときだけ。$e<1$ では熱や音として失われる")],
                points=[tp("衝突後の速度の符号から「A は止まらず、B に追い越されて右に進む」ことを読み取らせ、$v_{\\mathrm{B}}'\\geqq v_{\\mathrm{A}}'$（すり抜けない）を確認させる。")]),
        example("ex2", "例題2　円錐振り子",
                "長さ $L$ の軽い糸の一端を天井に固定し、他端に質量 $m$ のおもりをつけて、糸が鉛直方向と角 $\\theta$ をなすように水平面内で等速円運動させた。糸の張力の大きさ $S$ と、円運動の周期 $T$ を求めよ。重力加速度の大きさを $g$ とする。",
                ["おもりにはたらく力は重力 $mg$ と張力 $S$ だけ。円の半径は $r=L\\sin\\theta$。",
                 "鉛直方向のつり合い：$S\\cos\\theta=mg$ より $S=\\dfrac{mg}{\\cos\\theta}$。",
                 "水平方向（中心向き）の運動方程式：$mr\\omega^2=S\\sin\\theta$、すなわち $mL\\sin\\theta\\,\\omega^2=\\dfrac{mg}{\\cos\\theta}\\sin\\theta$。",
                 "$\\omega=\\sqrt{\\dfrac{g}{L\\cos\\theta}}$、$T=\\dfrac{2\\pi}{\\omega}=2\\pi\\sqrt{\\dfrac{L\\cos\\theta}{g}}$。"],
                "$S=\\dfrac{mg}{\\cos\\theta}$、$T=2\\pi\\sqrt{\\dfrac{L\\cos\\theta}{g}}$",
                thinking="鉛直方向は加速度 0（つり合い）、水平方向は中心向きの加速度 $r\\omega^2$。方向ごとに使う式が違う。",
                figure=figure("天井から長さ L の糸でつるしたおもり m が、鉛直と角 θ をなして水平面内で円運動する円錐振り子", conical_svg()),
                points=[tp("周期が質量によらないこと、$\\theta\\to0$ で単振り子の周期 $2\\pi\\sqrt{\\dfrac{L}{g}}$ に近づくことを確かめさせ、式の検算の習慣をつける。")]),
        example("ex3", "例題3　人工衛星の速さと周期",
                "地表からの高さが地球の半径 $R$ に等しい円軌道を回る人工衛星の速さと周期を求めよ。" + RS,
                ["軌道半径は $r=R+R=2R=1.28\\times10^7\\,\\mathrm{m}$。",
                 "$m\\dfrac{v^2}{r}=G\\dfrac{Mm}{r^2}$ と $GM=gR^2$ より $v=\\sqrt{\\dfrac{gR^2}{2R}}=\\sqrt{\\dfrac{gR}{2}}=\\sqrt{\\dfrac{9.8\\times6.4\\times10^6}{2}}\\fallingdotseq5.6\\times10^3\\,\\mathrm{m/s}$。",
                 "$T=\\dfrac{2\\pi r}{v}=\\dfrac{2\\times3.14\\times1.28\\times10^7}{5.6\\times10^3}\\fallingdotseq1.4\\times10^4\\,\\mathrm{s}$（約4時間）。"],
                "速さ 約 $5.6\\times10^3\\,\\mathrm{m/s}$、周期 約 $1.4\\times10^4\\,\\mathrm{s}$",
                thinking="万有引力定数 $G$ や地球の質量 $M$ が与えられていないときは、$GM=gR^2$ で置きかえる。",
                misconceptions=[("軌道半径に地表からの高さ $R$ を使う", "万有引力の $r$ は地球の中心からの距離。$r=R+h=2R$")]),
        board("bd1", "板書案",
              [("① 運動量と衝突", ["$\\vec{p}=m\\vec{v}$", "$m\\vec{v'}-m\\vec{v}=\\vec{F}\\Delta t$", "外力なし → $\\sum m\\vec{v}$ 一定",
                                   "$e=-\\dfrac{v_1'-v_2'}{v_1-v_2}$", "$e=1$ 弾性／$e=0$ 一体", "床：$h'=e^2h$"]),
               ("② 円運動・単振動", ["$v=r\\omega$、$T=\\dfrac{2\\pi}{\\omega}$", "$a=r\\omega^2=\\dfrac{v^2}{r}$（中心向き）", "向心力＝実在の力の合力",
                                     "$x=A\\sin\\omega t$、$a=-\\omega^2x$", "$F=-Kx\\Rightarrow T=2\\pi\\sqrt{\\dfrac{m}{K}}$", "単振り子 $2\\pi\\sqrt{\\dfrac{L}{g}}$"]),
               ("③ 万有引力", ["$F=G\\dfrac{Mm}{r^2}$（$r$ は中心間）", "$GM=gR^2$", "円軌道 $v=\\sqrt{\\dfrac{GM}{r}}$", "$\\dfrac{T^2}{r^3}=$ 一定（ケプラー第3）",
                               "$U=-G\\dfrac{Mm}{r}$", "第1宇宙速度 $\\sqrt{gR}$、第2 $\\sqrt{2gR}$"])]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("衝突の問題では「運動量保存＋反発係数」、衝突以外の区間では「力学的エネルギー保存」と、区間ごとに使う法則を分けさせる。弾丸が振り子に打ち込まれる問題が典型。", timing="例題1のあと"),
               tp("円運動の運動方程式は「中心向きを正」として $m\\dfrac{v^2}{r}=$（中心向きの力の和）と書く型を徹底する。",
                  ask="鉛直面内の円運動の最高点で、糸の張力 $S$ と重力 $mg$ はどちら向きか。", expect="どちらも中心（下）向き。$m\\dfrac{v^2}{r}=S+mg$。"),
               tp("単振動の周期を求めるときは「つり合いの位置を原点にとり、合力を $-Kx$ の形に整理する」という手順を示す。"),
               tp("天体の問題では、与えられた定数（$G$ と $M$、または $g$ と $R$）を確認させてから式を選ばせる。", caution="地表からの高さと軌道半径の取り違えが最も多い。")],
              misconceptions=[("円運動している物体には、運動の向き（接線方向）に力がはたらいている", "等速円運動では接線方向の力は 0。合力は中心を向き、速度の向きだけを変える"),
                              ("単振動の周期は振幅が大きいほど長い", "$T=2\\pi\\sqrt{\\dfrac{m}{K}}$ は振幅によらない。振幅が大きいと速さも大きくなる"),
                              ("人工衛星は重力がはたらいていないので落ちてこない", "万有引力は常にはたらき、それが向心力になって円軌道を描く（落ち続けているが地表に届かない）")]),
        summary("sm1", "まとめ", ["運動量の変化は力積に等しい。外力がなければ系の運動量は保存され、衝突では反発係数の式と連立して速度を求める。",
                                   "等速円運動の加速度は中心向きで $\\dfrac{v^2}{r}$。向心力は実在の力の合力として見つける。",
                                   "復元力 $F=-Kx$ を受ける物体は単振動をし、周期 $2\\pi\\sqrt{\\dfrac{m}{K}}$ は振幅によらない。",
                                   "万有引力 $G\\dfrac{Mm}{r^2}$ を向心力とする円運動から、衛星の速さ・周期とケプラーの第3法則が導かれる。"]),
        check("ck1", "確認問題", [("質量 $0.50\\,\\mathrm{kg}$ の物体が速さ $6.0\\,\\mathrm{m/s}$ で運動している。運動量の大きさは？", "$3.0\\,\\mathrm{kg\\cdot m/s}$"),
                                  ("高さ $1.0\\,\\mathrm{m}$ から落とした球が床ではね返り、$0.36\\,\\mathrm{m}$ の高さまで上がった。反発係数は？", "$e=\\sqrt{0.36}=0.60$"),
                                  ("半径 $2.0\\,\\mathrm{m}$ の円周上を速さ $4.0\\,\\mathrm{m/s}$ で等速円運動する物体の加速度の大きさは？", "$\\dfrac{4.0^2}{2.0}=8.0\\,\\mathrm{m/s^2}$"),
                                  ("ばね振り子のおもりの質量を4倍にすると、周期は何倍になるか。", "2倍"),
                                  ("2物体間の距離を3倍にすると、万有引力の大きさは何倍になるか。", "$\\dfrac{1}{9}$ 倍")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

@gen("basic_check", 4, ["computation"])
def momentum_basic(r):
    kind = r.choice(["p", "impulse", "avgF", "dp"])
    if kind == "p":
        ms = r.choice(["0.20", "0.50", "1.5", "2.0", "4.0", "60"])
        vs = r.choice(["3.0", "4.0", "5.0", "8.0", "10", "20"])
        m, v = Q(ms), Q(vs)
        return numq(f"質量 {ms} kg の物体が、一直線上を速さ {vs} m/s で運動している。この物体の運動量の大きさは何 kg·m/s か。", m * v, f"{P(m)}*{P(v)}",
                    "$p=mv$。", "kg·m/s", d=1, ap="運動量は「質量×速度」。運動の勢いを表す量で、向きは速度と同じ。",
                    steps=[f"$p=mv={ms}\\times{vs}$。", f"$p={t(m * v)}\\,\\mathrm{{kg\\cdot m/s}}$。"],
                    alt=["単位 $\\mathrm{kg\\cdot m/s}$ が「質量×速度」の組み立てになっているかで確かめる。"],
                    pc=[("$p=mv$ を用いている", 1), ("値が正しい", 1)], pit=["運動エネルギー $\\dfrac12mv^2$ と混同する。"])
    if kind == "impulse":
        Fs = r.choice(["2.0", "5.0", "10", "20"])
        dts = r.choice(["0.10", "0.50", "2.0", "3.0"])
        ms = r.choice(["0.50", "2.0", "4.0", "5.0"])
        F, dt, m = Q(Fs), Q(dts), Q(ms)
        v = F * dt / m
        return numq(f"なめらかな水平面上に静止している質量 {ms} kg の物体に、水平方向に一定の力 {Fs} N を {dts} s 間加えた。力を加え終えたときの物体の速さは何 m/s か。",
                    v, f"{P(F)}*{P(dt)}/{P(m)}", "力積＝運動量の変化：$F\\Delta t=mv-0$。", "m/s", d=2,
                    ap="運動量の変化は受けた力積に等しい。初めは静止しているので、初めの運動量は 0。",
                    steps=[f"力積 $F\\Delta t={Fs}\\times{dts}={t(F * dt)}\\,\\mathrm{{N\\cdot s}}$。", f"$mv=F\\Delta t$ より $v=\\dfrac{{{t(F * dt)}}}{{{ms}}}={t(v)}\\,\\mathrm{{m/s}}$。"],
                    alt=[f"加速度 $a=\\dfrac{{F}}{{m}}$ を求め、$v=at$ としても同じ結果になる（力積の式は運動方程式から導かれる）。"],
                    pc=[("力積と運動量の関係を用いている", 1), ("値が正しい", 1)], pit=["力積 $F\\Delta t$ をそのまま速さとして答える。"])
    ms = r.choice(["0.10", "0.15", "0.20", "0.40"])
    vs = r.choice(["10", "20", "30"])
    ws = r.choice(["5.0", "10", "15"])
    m, v, w = Q(ms), Q(vs), Q(ws)
    if kind == "dp":
        I = m * (v + w)
        return numq(f"質量 {ms} kg のボールが、速さ {vs} m/s で壁に垂直に当たり、逆向きに速さ {ws} m/s ではね返った。ボールが壁から受けた力積の大きさは何 N·s か。",
                    I, f"{P(m)}*({P(w)}-(-{P(v)}))", "はね返った向きを正とすると、運動量の変化は $mw-m(-v)=m(v+w)$。", "N·s", d=2,
                    ap="向きが逆になる運動では、正の向きを決めて速度を符号つきで表す。運動量の変化は「後−前」。",
                    steps=[f"はね返った向きを正とすると、衝突前の速度 $-{vs}\\,\\mathrm{{m/s}}$、衝突後 $+{ws}\\,\\mathrm{{m/s}}$。",
                           f"力積＝$m(v'-v)={ms}\\times\\{{{ws}-(-{vs})\\}}={t(I)}\\,\\mathrm{{N\\cdot s}}$。"],
                    alt=["運動量のベクトルを矢印でかくと、変化 $\\Delta\\vec{p}$ は2本の矢印の長さの和になることが図からわかる。"],
                    pc=[("速度を符号つきで扱っている", 1), ("値が正しい", 1)], pit=["速さの差 $m(v-w)$ を計算してしまう。"])
    dts = r.choice(["0.010", "0.020", "0.050"])
    dt = Q(dts)
    F = m * (v + w) / dt
    return numq(f"質量 {ms} kg のボールが速さ {vs} m/s で壁に垂直に当たり、逆向きに速さ {ws} m/s ではね返った。ボールと壁が接触していた時間を {dts} s とするとき、ボールが壁から受けた平均の力の大きさは何 N か。",
                F, f"{P(m)}*({P(v)}+{P(w)})/{P(dt)}", "平均の力 $\\overline{F}=\\dfrac{\\Delta p}{\\Delta t}$。", "N", d=2,
                ap="まず運動量の変化（＝力積）を符号に注意して求め、接触時間で割る。",
                steps=[f"運動量の変化の大きさ ${ms}\\times({vs}+{ws})={t(m * (v + w))}\\,\\mathrm{{kg\\cdot m/s}}$。", f"$\\overline{{F}}=\\dfrac{{{t(m * (v + w))}}}{{{dts}}}={t(F)}\\,\\mathrm{{N}}$。"],
                alt=["接触時間が短いほど平均の力が大きくなる（反比例）ことから、答えの大きさの見当をつける。"],
                pc=[("運動量の変化を正しく求めている", 1), ("平均の力が正しい", 1)], pit=["はね返りの速さを引いてしまう。"])


E_LIST = ["0.20", "0.25", "0.40", "0.50", "0.60", "0.75", "0.80"]


@gen("basic_check", 3, ["computation", "condition_check"])
def collision_basic(r):
    kind = r.choice(["stick", "e", "floor_h", "floor_e", "wall"])
    if kind == "stick":
        m1, m2 = r.sample([1, 2, 3, 4, 5], 2)
        v1 = r.choice([2, 3, 4, 5, 6, 8, 10])
        V = sp.Rational(m1 * v1, m1 + m2)
        return numq(f"なめらかな水平面上で、速さ {iv(v1)} m/s で進む質量 {iv(m1)} kg の台車 A が、静止している質量 {iv(m2)} kg の台車 B に衝突し、両者は一体となって進んだ。一体となった後の速さは何 m/s か。",
                    V, f"Rational({m1}*{v1},{m1 + m2})", "運動量保存：$m_{\\mathrm{A}}v=(m_{\\mathrm{A}}+m_{\\mathrm{B}})V$。", "m/s", d=1,
                    ap="衝突では内力だけがはたらくので運動量が保存される。一体となる＝衝突後の速度が等しい（$e=0$）。",
                    steps=[f"${m1}\\times{v1}=({m1}+{m2})V$。", f"$V=\\dfrac{{{m1 * v1}}}{{{m1 + m2}}}={t(V)}\\,\\mathrm{{m/s}}$。"],
                    alt=["運動エネルギーの保存を使うと誤った値になることを確かめ、完全非弾性衝突ではエネルギーが失われることを確認する。"],
                    pc=[("運動量保存の式を立てている", 1), ("値が正しい", 1)], pit=["運動エネルギー保存の式を立てる。"])
    if kind == "e":
        while True:
            m1, m2 = r.sample([1, 2, 3, 4], 2)
            v1 = r.choice([2, 4, 5, 6, 8, 10])
            es = r.choice(E_LIST)
            e = Q(es)
            v1p = (m1 - e * m2) * v1 / (m1 + m2)
            v2p = (1 + e) * m1 * v1 / (m1 + m2)
            if fin(v1p) and fin(v2p) and v1p != 0 and is_exact(t(v1p), v1p) and is_exact(t(v2p), v2p):
                break
        d1 = "右向き" if v1p > 0 else "左向き"
        return numq(f"なめらかな水平面上で、右向きに速さ {iv(v1)} m/s で進む球 A が、静止している球 B に正面衝突した。衝突後、A は{d1}に速さ {t(abs(v1p))} m/s、B は右向きに速さ {t(v2p)} m/s で進んだ。A と B の間の反発係数はいくらか。",
                    e, f"-(({P(v1p)})-({P(v2p)}))/({v1}-0)", "$e=-\\dfrac{v_{\\mathrm{A}}'-v_{\\mathrm{B}}'}{v_{\\mathrm{A}}-v_{\\mathrm{B}}}$（符号つきの速度）。", "", d=2,
                    ap="反発係数は「離れる速さ÷近づく速さ」。右向きを正として速度を符号つきで代入する。",
                    steps=[f"右向きを正とすると $v_{{\\mathrm{{A}}}}={v1}$、$v_{{\\mathrm{{B}}}}=0$、$v_{{\\mathrm{{A}}}}'={dec(v1p)}$、$v_{{\\mathrm{{B}}}}'={dec(v2p)}$。",
                           f"$e=-\\dfrac{{{dec(v1p)}-{dec(v2p)}}}{{{v1}-0}}={t(e)}$。"],
                    alt=["離れる速さ（B の速度−A の速度）と近づく速さ（衝突前の相対速度）の比として直接求めてもよい。"],
                    pc=[("速度を符号つきで代入している", 1), ("値が正しい", 1)], pit=["A がはね返った場合に符号を無視して速さの差をとる。"])
    if kind in ("floor_h", "floor_e"):
        hs = r.choice(["1.0", "2.0", "2.5", "4.0", "5.0"])
        h = Q(hs)
        es = r.choice(["0.40", "0.50", "0.60", "0.80", "0.90"])
        e = Q(es)
        hp = e ** 2 * h
        if kind == "floor_h":
            return numq(f"高さ {hs} m の位置から小球を静かにはなしたところ、水平な床ではね返った。床と小球の間の反発係数を {es} とするとき、はね返った小球が達する最高点の床からの高さは何 m か。空気抵抗は無視する。",
                        hp, f"{P(e)}**2*{P(h)}", "床に当たる直前の速さ $\\sqrt{2gh}$、直後 $e\\sqrt{2gh}$。上がる高さは $e^2h$。", "m", d=2,
                        ap="はね返り直後の速さは $e$ 倍。高さは速さの2乗に比例するので $e^2$ 倍になる。",
                        steps=[f"直後の速さは直前の {es} 倍。", f"高さは速さの2乗に比例するので $h'=e^2h={es}^2\\times{hs}={t(hp)}\\,\\mathrm{{m}}$。"],
                        alt=["$g$ の値を使って $v=\\sqrt{2gh}$、$v'=ev$、$h'=\\dfrac{v'^2}{2g}$ と順に計算しても同じ（$g$ は約分される）。"],
                        pc=[("$e$ 倍の速さではね返ることを用いている", 1), ("高さが正しい", 1)], pit=["高さを $eh$ とする。"])
        return numq(f"高さ {hs} m の位置から小球を静かにはなしたところ、水平な床ではね返って高さ {dec(hp)} m まで上がった。床と小球の間の反発係数はいくらか。空気抵抗は無視する。",
                    e, f"sqrt({P(hp)}/{P(h)})", "$h'=e^2h$ より $e=\\sqrt{\\dfrac{h'}{h}}$。", "", d=2,
                    ap="速さは高さの平方根に比例する。反発係数は速さの比。",
                    steps=[f"$e^2=\\dfrac{{h'}}{{h}}=\\dfrac{{{dec(hp)}}}{{{hs}}}={dec(e ** 2)}$。", f"$e={t(e)}$。"],
                    alt=["床に当たる直前・直後の速さ $\\sqrt{2gh}$、$\\sqrt{2gh'}$ を実際に計算して比をとってもよい。"],
                    pc=[("$h'=e^2h$ の関係を用いている", 1), ("値が正しい", 1)], pit=["高さの比をそのまま反発係数とする。"])
    vs = r.choice(["4.0", "6.0", "8.0", "10", "12"])
    es = r.choice(E_LIST)
    v, e = Q(vs), Q(es)
    return numq(f"なめらかな水平面上を速さ {vs} m/s で進む小球が、鉛直な壁に垂直に衝突してはね返った。壁と小球の間の反発係数を {es} とするとき、はね返った直後の小球の速さは何 m/s か。",
                e * v, f"{P(e)}*{P(v)}", "壁との衝突では $v'=ev$（向きは逆）。", "m/s", d=1,
                ap="壁は動かないので、反発係数は「はね返る速さ÷当たる速さ」。",
                steps=[f"$v'=ev={es}\\times{vs}$。", f"$v'={t(e * v)}\\,\\mathrm{{m/s}}$（向きは衝突前と逆）。"],
                alt=["反発係数の定義式で壁の速度を 0 とおくと $e=-\\dfrac{v'}{v}$。符号から向きが逆とわかる。"],
                pc=[("$v'=ev$ を用いている", 1), ("値が正しい", 1)], pit=["$\\dfrac{v}{e}$ と割ってしまう。"])


@gen("basic_check", 4, ["computation"])
def circular_basic(r):
    kind = r.choice(["omega", "v", "a", "F", "rpm", "w_from_v"])
    if kind == "omega":
        Ts = r.choice(["0.50", "2.0", "4.0", "5.0", "10", "20"])
        T = Q(Ts)
        w = 2 * sp.pi / T
        return numq(f"一定の速さで円運動する物体が、周期 {Ts} s で回転している。角速度は何 rad/s か。円周率を $\\pi=3.14$ として計算してもよい。", w, f"2*pi/{P(T)}",
                    "$\\omega=\\dfrac{2\\pi}{T}$。", "rad/s", d=1, ap="1周（$2\\pi$ rad）を周期 $T$ で回るので、1秒あたりの回転角は $\\dfrac{2\\pi}{T}$。",
                    steps=[f"$\\omega=\\dfrac{{2\\pi}}{{{Ts}}}$。", f"$\\omega\\fallingdotseq{t(w)}\\,\\mathrm{{rad/s}}$。"],
                    alt=["回転数 $n=\\dfrac{1}{T}$ を求めて $\\omega=2\\pi n$ としても同じ。"],
                    pc=[("$\\omega=\\dfrac{2\\pi}{T}$ を用いている", 1), ("値が正しい", 1)], pit=["$2\\pi$ を忘れて $\\dfrac{1}{T}$ とする。"])
    if kind == "rpm":
        n = r.choice([30, 45, 60, 90, 120, 600])
        T = sp.Rational(60, n)
        return numq(f"回転台が1分間に {n} 回の割合で一様に回転している。回転の周期は何 s か。", T, f"Rational(60,{n})", "$T=\\dfrac{60}{n}$。", "s", d=1,
                    ap="1分（60 s）に $n$ 回転するので、1回転にかかる時間は $\\dfrac{60}{n}$ 秒。",
                    steps=[f"$T=\\dfrac{{60\\,\\mathrm{{s}}}}{{{n}}}$。", f"$T={t(T)}\\,\\mathrm{{s}}$。"],
                    alt=[f"回転数 $\\dfrac{{{n}}}{{60}}$ 回/s の逆数として求めても同じ。"],
                    pc=[("周期の意味を用いている", 1), ("値が正しい", 1)], pit=["回転数そのものを周期と答える。"])
    rs = r.choice(["0.50", "1.2", "2.0", "3.0", "4.0"])
    rr = Q(rs)
    if kind == "v":
        ws = r.choice(["2.0", "3.0", "4.0", "5.0"])
        w = Q(ws)
        return numq(f"半径 {rs} m の円周上を、角速度 {ws} rad/s で等速円運動する物体の速さは何 m/s か。", rr * w, f"{P(rr)}*{P(w)}", "$v=r\\omega$。", "m/s", d=1,
                    ap="1秒に回る角が $\\omega$ rad なので、進む弧の長さは $r\\omega$。",
                    steps=[f"$v=r\\omega={rs}\\times{ws}$。", f"$v={t(rr * w)}\\,\\mathrm{{m/s}}$。"],
                    alt=["周期 $T=\\dfrac{2\\pi}{\\omega}$ を求め、$v=\\dfrac{2\\pi r}{T}$ としても同じ。"],
                    pc=[("$v=r\\omega$ を用いている", 1), ("値が正しい", 1)], pit=["$\\dfrac{\\omega}{r}$ とする。"])
    if kind == "w_from_v":
        vs = r.choice(["2.0", "3.0", "6.0", "8.0", "12"])
        v = Q(vs)
        return numq(f"半径 {rs} m の円周上を、速さ {vs} m/s で等速円運動する物体の角速度は何 rad/s か。", v / rr, f"{P(v)}/{P(rr)}", "$\\omega=\\dfrac{v}{r}$。", "rad/s", d=1,
                    ap="$v=r\\omega$ を $\\omega$ について解く。",
                    steps=[f"$\\omega=\\dfrac{{v}}{{r}}=\\dfrac{{{vs}}}{{{rs}}}$。", f"$\\omega={t(v / rr)}\\,\\mathrm{{rad/s}}$。"],
                    alt=["1秒間に進む弧の長さ $v$ を半径で割ると回転角（rad）になる、という弧度法の定義から考えてもよい。"],
                    pc=[("$v=r\\omega$ を用いている", 1), ("値が正しい", 1)], pit=["$v\\times r$ とする。"])
    vs = r.choice(["2.0", "3.0", "4.0", "6.0", "10"])
    v = Q(vs)
    if kind == "a":
        a = v ** 2 / rr
        return numq(f"半径 {rs} m の円周上を、速さ {vs} m/s で等速円運動する物体の加速度の大きさは何 m/s² か。", a, f"{P(v)}**2/{P(rr)}", "$a=\\dfrac{v^2}{r}$（中心向き）。", "m/s²", d=2,
                    ap="速さが一定でも向きが変わるので加速度がある。大きさは $\\dfrac{v^2}{r}$、向きは中心向き。",
                    steps=[f"$a=\\dfrac{{v^2}}{{r}}=\\dfrac{{{vs}^2}}{{{rs}}}$。", f"$a={t(a)}\\,\\mathrm{{m/s^2}}$。"],
                    alt=["$\\omega=\\dfrac{v}{r}$ を求めて $a=r\\omega^2$ としても同じ。"],
                    pc=[("$a=\\dfrac{v^2}{r}$ を用いている", 1), ("値が正しい", 1)], pit=["速さが一定なので加速度は 0 と答える。", "$\\dfrac{v}{r}$ とする。"])
    ms = r.choice(["0.10", "0.20", "0.50", "2.0"])
    m = Q(ms)
    F = m * v ** 2 / rr
    return numq(f"質量 {ms} kg の小球が、半径 {rs} m の円周上を速さ {vs} m/s で等速円運動している。小球にはたらく向心力の大きさは何 N か。", F, f"{P(m)}*{P(v)}**2/{P(rr)}",
                "$F=m\\dfrac{v^2}{r}$。", "N", d=2, ap="円運動の運動方程式 $m\\dfrac{v^2}{r}=F$。$F$ は中心向きの合力。",
                steps=[f"$F=m\\dfrac{{v^2}}{{r}}={ms}\\times\\dfrac{{{vs}^2}}{{{rs}}}$。", f"$F={t(F)}\\,\\mathrm{{N}}$。"],
                alt=["加速度 $\\dfrac{v^2}{r}$ を先に求め、質量をかけても同じ。"],
                pc=[("円運動の運動方程式を用いている", 1), ("値が正しい", 1)], pit=["$v$ を2乗し忘れる。"])


@gen("basic_check", 3, ["computation"])
def shm_basic(r):
    kind = r.choice(["spring", "pend", "vmax", "amax", "phase", "freq"])
    if kind == "spring":
        ms, ks = r.choice([("0.10", "10"), ("0.40", "10"), ("0.90", "10"), ("0.50", "50"), ("1.6", "40"), ("2.5", "10"), ("0.20", "80"), ("1.0", "25")])
        m, k = Q(ms), Q(ks)
        T = 2 * sp.pi * sp.sqrt(m / k)
        return numq(f"ばね定数 {ks} N/m の軽いばねに質量 {ms} kg のおもりをつけ、なめらかな水平面上で単振動させた。周期は何 s か。円周率を $\\pi=3.14$ として計算してもよい。",
                    T, f"2*pi*sqrt({P(m)}/{P(k)})", "$T=2\\pi\\sqrt{\\dfrac{m}{k}}$。", "s", d=1,
                    ap="ばね振り子の周期は質量とばね定数だけで決まる。重い・ばねが柔らかいほど周期が長い。",
                    steps=[f"$\\sqrt{{\\dfrac{{m}}{{k}}}}=\\sqrt{{\\dfrac{{{ms}}}{{{ks}}}}}={t(sp.sqrt(m / k), 3)}$。", f"$T=2\\pi\\times{t(sp.sqrt(m / k), 3)}\\fallingdotseq{t(T)}\\,\\mathrm{{s}}$。"],
                    alt=["角振動数 $\\omega=\\sqrt{\\dfrac{k}{m}}$ を先に求め、$T=\\dfrac{2\\pi}{\\omega}$ としてもよい。"],
                    pc=[("周期の式を用いている", 1), ("値が正しい", 1)], pit=["$\\sqrt{\\dfrac{k}{m}}$ と分母分子を逆にする。"])
    if kind == "pend":
        Ls = r.choice(["0.40", "0.98", "1.6", "2.5", "3.6", "9.8"])
        L = Q(Ls)
        T = 2 * sp.pi * sp.sqrt(L / G)
        return numq(f"長さ {Ls} m の軽い糸におもりをつけた単振り子を、小さな振れ角で振動させた。周期は何 s か。" + GS + "円周率を $\\pi=3.14$ として計算してもよい。",
                    T, f"2*pi*sqrt({P(L)}/9.8)", "$T=2\\pi\\sqrt{\\dfrac{L}{g}}$。", "s", d=1,
                    ap="単振り子の周期は糸の長さと重力加速度で決まり、おもりの質量にはよらない。",
                    steps=[f"$T=2\\pi\\sqrt{{\\dfrac{{{Ls}}}{{9.8}}}}$。", f"$T\\fallingdotseq{t(T)}\\,\\mathrm{{s}}$。"],
                    alt=["長さ約 $1\\,\\mathrm{m}$ の振り子の周期が約 $2\\,\\mathrm{s}$ になることを目安に、答えの大きさを確かめる。"],
                    pc=[("単振り子の周期の式を用いている", 1), ("値が正しい", 1)], pit=["$\\sqrt{\\dfrac{g}{L}}$ と逆にする。"])
    if kind == "freq":
        Ts = r.choice(["0.20", "0.25", "0.50", "2.0", "4.0"])
        T = Q(Ts)
        return numq(f"単振動する物体の周期が {Ts} s である。振動数は何 Hz か。", 1 / T, f"1/{P(T)}", "$f=\\dfrac{1}{T}$。", "Hz", d=1,
                    ap="振動数は1秒あたりの振動の回数。周期の逆数。",
                    steps=[f"$f=\\dfrac{{1}}{{{Ts}}}$。", f"$f={t(1 / T)}\\,\\mathrm{{Hz}}$。"],
                    alt=["1秒間に周期 " + Ts + " s の振動が何回入るかを割り算で考える。"],
                    pc=[("$f=\\dfrac{1}{T}$ を用いている", 1), ("値が正しい", 1)], pit=["角振動数 $\\dfrac{2\\pi}{T}$ と混同する。"])
    As = r.choice(["0.020", "0.050", "0.10", "0.20"])
    ws = r.choice(["2.0", "3.0", "5.0", "10"])
    A, w = Q(As), Q(ws)
    if kind == "vmax":
        return numq(f"振幅 {As} m、角振動数 {ws} rad/s で単振動する物体の速さの最大値は何 m/s か。", A * w, f"{P(A)}*{P(w)}", "$v_{\\max}=A\\omega$（振動の中心で最大）。", "m/s", d=2,
                    ap="単振動は半径 $A$、角速度 $\\omega$ の等速円運動の正射影。円運動の速さ $A\\omega$ が速さの最大値。",
                    steps=[f"$v_{{\\max}}=A\\omega={As}\\times{ws}$。", f"$v_{{\\max}}={t(A * w)}\\,\\mathrm{{m/s}}$。"],
                    alt=["$v=A\\omega\\cos\\omega t$ の最大値として求めても同じ。"],
                    pc=[("$A\\omega$ を用いている", 1), ("値が正しい", 1)], pit=["$A\\omega^2$（加速度の最大値）と混同する。"])
    if kind == "amax":
        return numq(f"振幅 {As} m、角振動数 {ws} rad/s で単振動する物体の加速度の大きさの最大値は何 m/s² か。", A * w ** 2, f"{P(A)}*{P(w)}**2",
                    "$a=-\\omega^2x$ より、両端（$|x|=A$）で最大 $A\\omega^2$。", "m/s²", d=2,
                    ap="加速度は変位に比例して逆向き。変位が最大の振動の端で加速度の大きさも最大。",
                    steps=[f"$a_{{\\max}}=A\\omega^2={As}\\times{ws}^2$。", f"$a_{{\\max}}={t(A * w ** 2)}\\,\\mathrm{{m/s^2}}$。"],
                    alt=["等速円運動の向心加速度 $A\\omega^2$ が射影の最大値になる、と考えてもよい。"],
                    pc=[("$A\\omega^2$ を用いている", 1), ("値が正しい", 1)], pit=["振動の中心で加速度が最大と考える。"])
    k, lab = r.choice([(12, "\\dfrac{T}{12}"), (4, "\\dfrac{T}{4}"), (8, "\\dfrac{T}{8}"), (6, "\\dfrac{T}{6}")])
    x = A * sp.sin(2 * sp.pi / k)
    return numq(f"時刻 $t=0$ に原点を正の向きに通過し、振幅 {As} m、周期 $T$ で単振動する物体がある（$x=A\\sin\\dfrac{{2\\pi}}{{T}}t$）。時刻 $t={lab}$ における物体の位置 $x$ は何 m か。",
                x, f"{P(A)}*sin(2*pi/{k})", "$x=A\\sin\\dfrac{2\\pi}{T}t$ に代入する。", "m", d=2,
                ap="位相 $\\dfrac{2\\pi}{T}t$ を先に計算し、三角関数の値を使う。",
                steps=[f"位相は $\\dfrac{{2\\pi}}{{T}}\\times{lab}=\\dfrac{{2\\pi}}{{{k}}}$。", f"$x={As}\\times\\sin\\dfrac{{2\\pi}}{{{k}}}\\fallingdotseq{t(x)}\\,\\mathrm{{m}}$。"],
                alt=["等速円運動の図で、半径 $A$ の円周上の点が角 $\\dfrac{2\\pi}{" + str(k) + "}$ だけ回ったときの高さを読み取ってもよい。"],
                pc=[("位相を正しく求めている", 1), ("値が正しい", 1)], pit=["位相を度数法と弧度法で混同する。"])


@gen("basic_check", 3, ["computation", "condition_check"])
def gravity_basic(r):
    kind = r.choice(["ratio", "ratio", "g_h", "kepler", "F"])
    if kind == "ratio":
        a, b, n = r.choice([(1, 1, 2), (1, 1, 3), (2, 1, 2), (2, 2, 2), (3, 1, 3), (1, 1, 4), (4, 1, 2), (2, 3, 3)])
        val = sp.Rational(a * b, n * n)
        def ftx(x):
            x = sp.Rational(x)
            return f"{x.p}" if x.q == 1 else f"\\dfrac{{{x.p}}}{{{x.q}}}"
        right = f"${ftx(val)}$ 倍"
        cand = [(f"${ftx(sp.Rational(a * b, n))}$ 倍", "万有引力は距離の2乗に反比例する。距離の1乗で割っている。", "逆2乗則の誤解"),
                (f"${ftx(sp.Rational(a * b * n * n))}$ 倍", "距離が大きくなると引力は小さくなる。距離の2乗をかけてしまっている。", "距離と引力の関係の逆転"),
                (f"${ftx(sp.Rational(a + b, n * n))}$ 倍", "引力は2つの質量の「積」に比例する。和にしている。", "質量の積と和の混同"),
                (f"${ftx(sp.Rational(a * b, 2 * n))}$ 倍", "距離の2乗は $n^2$ であり $2n$ ではない。", "2乗の計算の誤り")]
        seen = {right}
        wr = []
        for c in cand:
            if c[0] not in seen:
                seen.add(c[0])
                wr.append(c)
        wr = wr[:3]
        chg = []
        if a != 1:
            chg.append(f"一方の質量を {a} 倍")
        if b != 1:
            chg.append(f"他方の質量を {b} 倍")
        chg.append(f"中心間の距離を {n} 倍")
        return mc(f"2つの物体の間にはたらく万有引力について、{'、'.join(chg)}にすると、万有引力の大きさはもとの何倍になるか。正しいものを選びなさい。",
                  [right] + [w[0] for w in wr], f"$F=G\\dfrac{{Mm}}{{r^2}}$ より $\\dfrac{{{a}\\times{b}}}{{{n}^2}}={ftx(val)}$ 倍。", d=2,
                  ap="万有引力は質量の積に比例し、距離の2乗に反比例する。変化する量ごとに倍率をかけ合わせる。",
                  steps=[f"質量の積は ${a}\\times{b}={a * b}$ 倍。", f"距離の2乗は ${n}^2={n * n}$ 倍なので、引力は $\\dfrac{{1}}{{{n * n}}}$ 倍。", f"合わせて ${ftx(val)}$ 倍。"],
                  alt=["もとの量を $M=m=r=1$ とおき、変化後の値を $F=G\\dfrac{Mm}{r^2}$ に代入して比べてもよい。"],
                  pc=[("逆2乗則を用いている", 1), ("正しい倍率を選んでいる", 1)], why={w[0]: (w[1], w[2]) for w in wr},
                  chk=(f"Rational({a}*{b},{n}**2)", str(val), None, "intermediate"))
    if kind == "g_h":
        k, hlab, rlab, sq = r.choice([(1, "地球の半径に等しい", "2R", "4"), (2, "地球の半径の2倍の", "3R", "9"),
                                      (3, "地球の半径の3倍の", "4R", "16"), (sp.Rational(1, 2), "地球の半径の半分の", "1.5R", "2.25")])
        gh = G / (1 + k) ** 2
        return numq(f"地表からの高さが{hlab}地点での重力加速度の大きさは何 m/s² か。地表での重力加速度の大きさを $9.8\\,\\mathrm{{m/s^2}}$ とし、地球の自転の影響は無視する。",
                    gh, f"9.8/(1+{P(k)})**2", "重力加速度は地球の中心からの距離の2乗に反比例する。", "m/s²", d=2,
                    ap="万有引力 $G\\dfrac{Mm}{r^2}=mg'$ より $g'=\\dfrac{GM}{r^2}$。$r$ は地球の中心からの距離。",
                    steps=[f"地球の中心からの距離は $r={rlab}$（$R$ は地球の半径）。",
                           f"$g'=g\\left(\\dfrac{{R}}{{r}}\\right)^2=\\dfrac{{9.8}}{{{sq}}}\\fallingdotseq{t(gh)}\\,\\mathrm{{m/s^2}}$。"],
                    alt=["$GM=gR^2$ を使い、$g'=\\dfrac{gR^2}{(R+h)^2}$ に代入して計算してもよい。"],
                    pc=[("中心からの距離で逆2乗則を用いている", 1), ("値が正しい", 1)], pit=["地表からの高さで割ってしまう。", "距離の1乗に反比例させる。"])
    if kind == "kepler":
        a, lab = r.choice([(4, "4"), (9, "9"), (16, "16"), (sp.Rational(1, 4), "\\dfrac{1}{4}"), (sp.Rational(1, 9), "\\dfrac{1}{9}")])
        ratio = sp.Rational(a) ** sp.Rational(3, 2)
        return numq(f"太陽のまわりを円軌道で公転する惑星 X の軌道半径は、地球の軌道半径の ${lab}$ 倍である。X の公転周期は地球の公転周期の何倍か。",
                    ratio, f"({P(a)})**Rational(3,2)", "ケプラーの第3法則 $\\dfrac{T^2}{r^3}=$ 一定。", "倍", d=2,
                    ap="周期の2乗が軌道半径の3乗に比例する。$T\\propto r^{\\frac{3}{2}}$。",
                    steps=[f"$\\left(\\dfrac{{T_{{\\mathrm{{X}}}}}}{{T}}\\right)^2=\\left({lab}\\right)^3$。", f"$\\dfrac{{T_{{\\mathrm{{X}}}}}}{{T}}=\\left({lab}\\right)^{{\\frac{{3}}{{2}}}}={t(ratio)}$ 倍。"],
                    alt=["円軌道の速さ $v=\\sqrt{\\dfrac{GM}{r}}$ と $T=\\dfrac{2\\pi r}{v}$ から $T\\propto r^{\\frac32}$ を導いて確かめる。"],
                    pc=[("第3法則を用いている", 1), ("値が正しい", 1)], pit=["周期が軌道半径に比例すると考える。"])
    m1, m2, rs = r.choice([(50, 60, "1.0"), (60, 60, "2.0"), (1000, 1000, "10"), (50, 50, "0.50"), (100, 200, "1.0")])
    rr = Q(rs)
    F = sp.Rational(667, 100) * sp.Rational(1, 10 ** 11) * m1 * m2 / rr ** 2
    return numq(f"質量 {m1} kg と {m2} kg の2つの物体が、中心間の距離 {rs} m だけ離れている。2物体の間にはたらく万有引力の大きさは何 N か。万有引力定数を $6.67\\times10^{{-11}}\\,\\mathrm{{N\\cdot m^2/kg^2}}$ とする。",
                F, f"Rational(667,100)*10**(-11)*{m1}*{m2}/{P(rr)}**2", "$F=G\\dfrac{m_1m_2}{r^2}$。", "N", n=2, d=2,
                ap="身近な物体どうしの万有引力はきわめて小さい。指数の計算をていねいに行う。",
                steps=[f"$F=6.67\\times10^{{-11}}\\times\\dfrac{{{m1}\\times{m2}}}{{{rs}^2}}$。", f"$F\\fallingdotseq{t(F, 2)}\\,\\mathrm{{N}}$。"],
                alt=["地球が物体を引く力（重さ）と比べて、何桁小さいかを確かめる。"],
                pc=[("万有引力の法則を用いている", 1), ("値が正しい", 1)], pit=["距離を2乗し忘れる。"])


CONCEPT = [
    ("なめらかな水平面上で、静止している2つの台車の間でばねを押し縮めてから静かにはなしたところ、台車は互いに逆向きに動き出した。正しいものを選びなさい。",
     "2台車の運動量の和は、はなす前もあとも 0 である",
     [("質量の大きい台車ほど大きい運動量をもって動き出す", "運動量保存より2台車の運動量は大きさが等しく逆向き。質量が大きい台車は速さが小さい。", "運動量と速さの混同"),
      ("2台車の運動エネルギーの和は 0 のまま保存される", "ばねの弾性エネルギーが運動エネルギーに変わるので、運動エネルギーの和は増える。保存されるのは運動量。", "運動量と運動エネルギーの混同"),
      ("内力がはたらいたので、運動量の和は変化する", "内力の力積は作用・反作用で打ち消し合うので、系全体の運動量は変わらない。", "内力と外力の区別の誤り")]),
    ("2つの球が一直線上で衝突するとき、反発係数 $e$ について正しいものを選びなさい。",
     "$e=1$ のとき、衝突の前後で運動エネルギーの和が保存される",
     [("$e=0$ のとき、2球は衝突後にもとの速さではね返る", "$e=0$ は完全非弾性衝突で、2球は一体となって進む（離れる速さが 0）。", "e の値の意味の取り違え"),
      ("$e$ は1より大きくなることもある", "外からエネルギーを与えない衝突では、離れる速さは近づく速さ以下なので $0\\leqq e\\leqq1$。", "反発係数の範囲の誤解"),
      ("$e<1$ の衝突では運動量の和も減少する", "外力がなければ $e$ の値によらず運動量は保存される。減少するのは運動エネルギー。", "運動量と運動エネルギーの混同")]),
    ("糸につけた小球を、なめらかな水平面上で等速円運動させている。小球にはたらく力について正しいものを選びなさい。",
     "水平方向には糸の張力だけがはたらき、それが向心力となっている",
     [("張力のほかに、向心力という力がはたらいている", "向心力は実在の力（ここでは張力）の合力に付けた名前で、別の力ではない。", "向心力を独立した力と考える誤り"),
      ("運動の向き（接線方向）に一定の力がはたらいている", "速さが一定なので接線方向の力は 0。中心向きの力が速度の向きだけを変える。", "運動の向きに力が必要という素朴概念"),
      ("中心から外向きの遠心力と張力がつり合い、合力は 0 である", "地面から見ると小球は加速度（中心向き）をもつので、合力は 0 ではない。遠心力は回転する立場での慣性力。", "観測者の立場の混同")]),
    ("等速円運動している糸の付いた小球で、糸が突然切れた。その直後の小球の運動として正しいものを選びなさい（なめらかな水平面上）。",
     "切れた瞬間の速度の向き（円の接線方向）に等速直線運動をする",
     [("円の中心から外向き（半径方向）に飛んでいく", "糸が切れると水平方向の力は 0 になり、慣性の法則により切れた瞬間の速度（接線方向）を保つ。", "遠心力で外に飛ぶという誤解"),
      ("しばらく円運動を続けてから直進する", "円運動を続けるには向心力が必要。力がなくなった瞬間から直進する。", "円運動の慣性という誤解"),
      ("円の中心に向かって進む", "中心向きの力（張力）がなくなるので、中心に向かう理由はない。", "力と運動の向きの混同")]),
    ("ばね振り子の単振動について、正しいものを選びなさい。",
     "振幅を2倍にしても周期は変わらない",
     [("振幅を2倍にすると周期も2倍になる", "$T=2\\pi\\sqrt{\\dfrac{m}{k}}$ は振幅を含まない（等時性）。振幅が大きいと速さも大きくなる。", "周期と振幅の混同"),
      ("振動の中心で加速度の大きさが最大になる", "$a=-\\omega^2x$ より、振動の中心（$x=0$）で加速度は 0。最大になるのは両端。", "速さと加速度の混同"),
      ("振動の両端で速さが最大になる", "両端では速度が 0 で向きが変わる。速さが最大になるのは振動の中心。", "位置と速さの関係の誤解")]),
    ("単振り子の周期について、正しいものを選びなさい。ただし振れ角は小さいものとする。",
     "糸の長さを4倍にすると、周期は2倍になる",
     [("おもりの質量を4倍にすると、周期は2倍になる", "$T=2\\pi\\sqrt{\\dfrac{L}{g}}$ はおもりの質量によらない。", "質量依存の誤解"),
      ("糸の長さを4倍にすると、周期は4倍になる", "周期は長さの平方根に比例する。$\\sqrt4=2$ 倍。", "比例関係の誤り"),
      ("重力加速度が小さい月面では、周期は短くなる", "$g$ が小さいほど周期は長くなる（分母に $g$）。", "g との関係の逆転")]),
    ("地球のまわりを円軌道で回る人工衛星について、正しいものを選びなさい。",
     "軌道半径が大きい衛星ほど、速さは小さく周期は長い",
     [("衛星には重力がはたらいていないので、等速円運動を続ける", "衛星には地球の万有引力がはたらき、それが向心力となって円軌道を描く。", "無重量状態の誤解"),
      ("軌道半径が大きい衛星ほど、速さが大きい", "$v=\\sqrt{\\dfrac{GM}{r}}$ より、軌道半径が大きいほど速さは小さい。", "速さと半径の関係の逆転"),
      ("衛星の速さは衛星の質量が大きいほど大きい", "運動方程式の両辺に衛星の質量 $m$ があり約分されるので、速さは衛星の質量によらない。", "質量依存の誤解")]),
    ("ケプラーの法則について、正しいものを選びなさい。",
     "惑星の公転周期の2乗は、楕円軌道の半長軸の3乗に比例する",
     [("惑星は太陽を中心とする円軌道を、一定の速さで公転する", "第1法則より軌道は太陽を焦点の1つとする楕円で、第2法則より太陽に近いほど速い。", "円軌道・等速の思い込み"),
      ("惑星は太陽から遠いところほど速く動く", "面積速度一定より、太陽に近いところで速く、遠いところで遅い。", "面積速度一定の誤解"),
      ("公転周期は、惑星の質量が大きいほど長い", "第3法則の比例定数は太陽の質量で決まり、惑星の質量によらない。", "質量依存の誤解")]),
    ("同じ速さで飛んできたボールを、グローブを引きながら受け止めると手が痛くないのはなぜか。正しいものを選びなさい。",
     "運動量の変化は同じだが、力がはたらく時間が長くなり、平均の力が小さくなるから",
     [("グローブを引くと、ボールの運動量の変化が小さくなるから", "どの受け止め方でもボールは止まるので、運動量の変化（＝力積）は同じ。", "力積と力の混同"),
      ("グローブを引くと、ボールの運動エネルギーが運動量に変わるから", "運動エネルギーと運動量は別の量で、互いに変わり合うものではない。", "物理量の混同"),
      ("グローブを引くと、作用・反作用の法則が成り立たなくなるから", "作用・反作用の法則はどんな場合にも成り立つ。", "法則の成立条件の誤解")]),
]


@gen("basic_check", 3, ["concept", "condition_check"])
def concept_mc(r):
    stem, right, wr = r.choice(CONCEPT)
    return mc(stem, [right] + [w[0] for w in wr], f"正しいのは「{right}」。" + wr[0][1], d=2,
              ap="保存される量（運動量・エネルギー）と、運動方程式で決まる量（加速度・周期）を区別して判断する。",
              steps=["各選択肢を、運動量保存則・運動方程式・周期の式などの法則に照らして確認する。", f"法則と矛盾しないのは「{right}」。"],
              alt=["誤りの選択肢が正しいと仮定して、極端な場合（質量 0、$e=0$、半径が非常に大きい など）を考えて矛盾を見つける。"],
              pc=[("判断の根拠となる法則を確認している", 1), ("正しい選択肢を選んでいる", 1)],
              why={w[0]: (w[1], w[2]) for w in wr})


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 4, ["computation", "application"])
def collision_1d(r):
    kind = r.choice(["after_A", "after_B", "loss", "head_on"])
    while True:
        m1, m2 = r.sample([1, 2, 3, 4, 5], 2)
        v1 = r.choice([2, 3, 4, 5, 6, 8, 10])
        v2 = 0 if kind != "head_on" else -r.choice([1, 2, 3, 4])
        es = r.choice(["0", "0.20", "0.40", "0.50", "0.60", "0.80", "1.0"]) if kind != "loss" else "0"
        e = Q(es)
        P0 = m1 * v1 + m2 * v2
        v1p = (P0 - e * m2 * (v1 - v2)) / (m1 + m2)
        v2p = (P0 + e * m1 * (v1 - v2)) / (m1 + m2)
        if kind == "loss" or (fin(v1p) and fin(v2p)):
            break
    fig = figure(f"右向きに進む球 A（{iv(m1)} kg）と球 B（{iv(m2)} kg）の衝突前の図",
                 collision_svg(f"{iv(m1)} kg", f"{iv(m2)} kg", f"{iv(v1)} m/s", f"{iv(-v2)} m/s" if v2 else ""))
    base = (f"図のように、なめらかな水平面上で右向きに速さ {iv(v1)} m/s で進む質量 {iv(m1)} kg の球 A が、"
            + (f"左向きに速さ {iv(-v2)} m/s で進んできた質量 {iv(m2)} kg の球 B と正面衝突した。" if v2 else f"静止している質量 {iv(m2)} kg の球 B に正面衝突した。"))
    if kind == "loss":
        V = sp.Rational(P0, m1 + m2)
        dK = sp.Rational(m1 * v1 ** 2, 2) - (m1 + m2) * V ** 2 / 2
        return numq(base + "衝突後、A と B は一体となって進んだ。衝突によって失われた運動エネルギーは何 J か。", dK,
                    f"Rational({m1}*{v1}**2,2)-({m1}+{m2})*Rational({P0},{m1 + m2})**2/2", "運動量保存で一体後の速さを求め、運動エネルギーの差をとる。", "J", d=3, fig=fig,
                    ap="衝突の前後で保存されるのは運動量。運動エネルギーは完全非弾性衝突で最も多く失われる。",
                    steps=[f"運動量保存：${m1}\\times{v1}=({m1}+{m2})V$ より $V={t(V, 3)}\\,\\mathrm{{m/s}}$。",
                           f"衝突前 $\\dfrac12\\times{m1}\\times{v1}^2={dec(sp.Rational(m1 * v1 ** 2, 2))}\\,\\mathrm{{J}}$、衝突後 $\\dfrac12\\times{m1 + m2}\\times V^2={t((m1 + m2) * V ** 2 / 2, 3)}\\,\\mathrm{{J}}$。",
                           f"失われた運動エネルギー $={t(dK)}\\,\\mathrm{{J}}$。"],
                    alt=[f"公式 $\\Delta K=\\dfrac12\\cdot\\dfrac{{m_1m_2}}{{m_1+m_2}}v^2=\\dfrac12\\times\\dfrac{{{m1 * m2}}}{{{m1 + m2}}}\\times{v1}^2$ で直接求めても同じ。"],
                    pc=[("運動量保存で一体後の速さを求めている", 2), ("運動エネルギーの差をとっている", 1), ("値が正しい", 1)], pit=["運動エネルギーが保存されるとして速さを求める。"])
    who = "A" if kind == "after_A" else ("B" if kind == "after_B" else r.choice(["A", "B"]))
    val = v1p if who == "A" else v2p
    elab = "この衝突は弾性衝突（反発係数 1）であった。" if e == 1 else ("衝突後、A と B は一体となって進んだ。" if e == 0 else f"A と B の間の反発係数は {es} である。")
    return numq(base + f"{elab}衝突後の {who} の速度は何 m/s か。右向きを正とし、向きは符号で表しなさい。", val,
                f"(({P0})-({P(e)})*{m2 if who == 'A' else -m1}*({v1}-({v2})))/({m1}+{m2})",
                "運動量保存則と反発係数の式を連立する。", "m/s", d=3, fig=fig,
                ap="未知数は衝突後の2つの速度。運動量保存則と反発係数の式の2本を、右向き正で立てて連立する。",
                steps=[f"運動量保存：${m1}\\times{v1}+{m2}\\times({v2})={m1}v_{{\\mathrm{{A}}}}'+{m2}v_{{\\mathrm{{B}}}}'$。",
                       f"反発係数：$v_{{\\mathrm{{B}}}}'-v_{{\\mathrm{{A}}}}'={es}\\times\\{{{v1}-({v2})\\}}$。",
                       f"連立して $v_{{\\mathrm{{A}}}}'={dec(v1p)}\\,\\mathrm{{m/s}}$、$v_{{\\mathrm{{B}}}}'={dec(v2p)}\\,\\mathrm{{m/s}}$。求める速度は ${t(val)}\\,\\mathrm{{m/s}}$。"],
                alt=["求めた2つの速度を運動量保存の式に代入し、衝突前の運動量の和に一致するかを確かめる。"],
                pc=[("運動量保存の式を立てている", 1), ("反発係数の式を符号に注意して立てている", 2), ("値が正しい", 1)],
                pit=["反発係数の式で速度の差の順序を逆にする。", "B の速度の向き（符号）を考えずに代入する。"])


@gen("standard_practice", 3, ["computation", "application"])
def split_recoil(r):
    kind = r.choice(["split", "boat", "ballistic", "sand"])
    if kind == "split":
        M = r.choice([3, 4, 5, 6, 10])
        m1 = r.choice([k for k in [1, 2, 3, 4] if k < M])
        v1 = r.choice([2, 3, 4, 6, 8, 12])
        v2 = sp.Rational(m1 * v1, M - m1)
        return numq(f"なめらかな水平面上に静止していた質量 {iv(M)} kg の物体が、内部の火薬の爆発によって2つに分裂した。質量 {iv(m1)} kg の部分が東向きに速さ {iv(v1)} m/s で動き出したとき、残りの部分の速さは何 m/s か。",
                    v2, f"Rational({m1}*{v1},{M}-{m1})", "分裂前の運動量 0 が保存される。", "m/s", d=2,
                    ap="分裂は内力による。初めの運動量は 0 なので、分裂後の2つの運動量は大きさが等しく逆向き。",
                    steps=[f"東向きを正とし、残りの部分の速度を $V$ とすると $0={m1}\\times{v1}+{M - m1}V$。", f"$V=-{t(v2)}\\,\\mathrm{{m/s}}$、速さは ${t(v2)}\\,\\mathrm{{m/s}}$（西向き）。"],
                    alt=["速さは質量に反比例する（$m_1v_1=m_2v_2$）ことから比で求めてもよい。"],
                    pc=[("運動量保存（和が 0）の式を立てている", 2), ("残りの質量を正しく用いている", 1), ("値が正しい", 1)], pit=["残りの質量を全体の質量 " + str(M) + " kg とする。"])
    if kind == "boat":
        m, M = r.choice([(50, 200), (60, 240), (40, 160), (50, 150), (60, 300), (45, 135)])
        v = r.choice([2, 3, 4, 5])
        V = sp.Rational(m * v, M)
        return numq(f"静水に浮かんで静止している質量 {M} kg のボートから、質量 {m} kg の人が水平方向に、岸に対して速さ {iv(v)} m/s で跳び出した。跳び出した直後のボートの速さは何 m/s か。水の抵抗は無視する。",
                    V, f"Rational({m}*{v},{M})", "人とボートの運動量の和は 0 のまま。", "m/s", d=2,
                    ap="人とボートを1つの系とみると、水平方向に外力ははたらかない。初めは静止しているので運動量の和は 0。",
                    steps=[f"人の向きを正とし、ボートの速度を $V$ とすると $0={m}\\times{v}+{M}V$。", f"$V=-{t(V)}\\,\\mathrm{{m/s}}$。速さは ${t(V)}\\,\\mathrm{{m/s}}$（人と逆向き）。"],
                    alt=["軽いほうが速く動く（速さは質量に反比例）ことから、$v\\times\\dfrac{" + str(m) + "}{" + str(M) + "}$ と比で求めてもよい。"],
                    pc=[("運動量保存の式を立てている", 2), ("向きを考えている", 1), ("値が正しい", 1)], pit=["人とボートの合計の質量で割ってしまう。"])
    if kind == "sand":
        M = r.choice([20, 30, 40, 50])
        m = r.choice([10, 20])
        v = r.choice([2, 3, 4, 5, 6])
        V = sp.Rational(M * v, M + m)
        return numq(f"なめらかな水平面上を速さ {iv(v)} m/s で進む質量 {M} kg の台車に、真上から質量 {m} kg の砂袋を静かに落としたところ、砂袋は台車の上で止まり、台車と一体となって進んだ。一体となった後の速さは何 m/s か。",
                    V, f"Rational({M}*{v},{M}+{m})", "水平方向の運動量が保存される。", "m/s", d=2,
                    ap="砂袋は鉛直に落ちてくるので水平方向の運動量は 0。鉛直方向には床からの力（外力）があるが、水平方向には外力がない。",
                    steps=[f"水平方向の運動量保存：${M}\\times{v}+{m}\\times0=({M}+{m})V$。", f"$V={t(V)}\\,\\mathrm{{m/s}}$。"],
                    alt=["鉛直方向は床から抗力（外力）を受けるので保存しないが、水平方向だけを考えればよいことを確認する。"],
                    pc=[("水平方向の運動量保存を用いている", 2), ("値が正しい", 2)], pit=["砂袋の落下の速さも運動量に加えてしまう。"])
    mg, M = r.choice([(10, "1.99"), (20, "1.98"), (10, "0.99"), (50, "2.95"), (20, "3.98"), (50, "4.95")])
    mm = sp.Rational(mg, 1000)
    Mk = Q(M)
    tot = mm + Mk
    vb = r.choice([200, 300, 400, 500])
    V = mm * vb / tot
    h = V ** 2 / (2 * G)
    return numq(f"質量 {M} kg の木片を軽い糸で天井からつるし、静止させた。質量 {mg} g の弾丸を水平に速さ {vb} m/s で木片に打ち込んだところ、弾丸は木片の中で止まり、両者は一体となって振れた。一体となった木片が最初の位置から上がる最大の高さは何 m か。" + GS,
                h, f"({P(mm)}*{vb}/{P(tot)})**2/(2*9.8)", "衝突は運動量保存、そのあとの振れは力学的エネルギー保存。", "m", d=3, ps=["cross_unit"], rel=["HS-PHYB-U02"],
                ap="2段階に分ける。打ち込む瞬間（衝突）は運動量保存、そのあと上がっていく間は力学的エネルギー保存。",
                steps=[f"運動量保存：${dec(mm)}\\times{vb}=({dec(mm)}+{M})V$ より $V={t(V, 3)}\\,\\mathrm{{m/s}}$。",
                       f"力学的エネルギー保存：$\\dfrac12(m+M)V^2=(m+M)gh$ より $h=\\dfrac{{V^2}}{{2g}}$。", f"$h\\fallingdotseq{t(h)}\\,\\mathrm{{m}}$。"],
                alt=["弾丸の運動エネルギーから一気に $h$ を求めると誤りになることを確かめ、衝突で失われるエネルギーを見積もる。"],
                pc=[("衝突で運動量保存を用いている", 2), ("振れでエネルギー保存を用いている", 1), ("値が正しい", 1)], pit=["衝突の前後で力学的エネルギーが保存されるとして計算する。", "質量の g を kg に直し忘れる。"])


@gen("standard_practice", 3, ["computation", "cross_unit"], rel=["HS-MATHC-U01"])
def momentum_2d(r):
    kind = r.choice(["perp", "oblique", "turn"])
    if kind == "perp":
        m1, m2 = r.sample([1, 2, 3, 4], 2)
        v1, v2 = r.choice([(3, 4), (4, 3), (6, 8), (8, 6), (2, 3), (4, 4), (6, 2)])
        p1, p2 = m1 * v1, m2 * v2
        V = sp.sqrt(p1 ** 2 + p2 ** 2) / (m1 + m2)
        return numq(f"なめらかな水平面上で、東向きに速さ {iv(v1)} m/s で進む質量 {iv(m1)} kg の物体 A と、北向きに速さ {iv(v2)} m/s で進む質量 {iv(m2)} kg の物体 B が衝突し、一体となって進んだ。一体となった後の速さは何 m/s か。",
                    V, f"sqrt(({m1}*{v1})**2+({m2}*{v2})**2)/({m1}+{m2})", "東西・南北の成分ごとに運動量が保存される。", "m/s", d=3,
                    ap="運動量はベクトル。成分ごとに保存の式を立てるか、ベクトルの和を三平方の定理で求める。",
                    steps=[f"東向き成分：${m1}\\times{v1}=({m1 + m2})V_x$、北向き成分：${m2}\\times{v2}=({m1 + m2})V_y$。",
                           f"運動量の大きさ $\\sqrt{{{p1}^2+{p2}^2}}={t(sp.sqrt(p1 ** 2 + p2 ** 2), 3)}\\,\\mathrm{{kg\\cdot m/s}}$。", f"$V=\\dfrac{{{t(sp.sqrt(p1 ** 2 + p2 ** 2), 3)}}}{{{m1 + m2}}}\\fallingdotseq{t(V)}\\,\\mathrm{{m/s}}$。"],
                    alt=["運動量ベクトルを矢印でかき、直角三角形の斜辺として合成運動量を求める図形的な方法でもよい。"],
                    pc=[("成分ごと（ベクトル）に運動量保存を考えている", 2), ("値が正しい", 2)], pit=["速さをそのまま足して質量で割る。"])
    if kind == "oblique":
        th = r.choice([30, 45, 60])
        vs = r.choice(["2.0", "4.0", "6.0", "10"])
        es = r.choice(["0.50", "0.60", "0.80", "0.40"])
        v, e = Q(vs), Q(es)
        vx, vy = v * COS[th], v * SIN[th]
        vp = sp.sqrt(vx ** 2 + (e * vy) ** 2)
        return numq(f"なめらかな水平な床に、小球が床と ${th}^\\circ$ の角をなす向きに速さ {vs} m/s で当たり、はね返った。床と小球の間の反発係数を {es} とするとき、はね返った直後の小球の速さは何 m/s か。",
                    vp, f"sqrt(({P(v)}*cos(deg({th})))**2+({P(e)}*{P(v)}*sin(deg({th})))**2)", "床に平行な成分は不変、垂直な成分は $e$ 倍。", "m/s", d=3,
                    ap="なめらかな床は水平方向に力を及ぼさないので、水平成分は変わらない。床に垂直な成分だけが $e$ 倍で逆向きになる。",
                    steps=[f"衝突前：水平成分 ${vs}\\cos{th}^\\circ$、鉛直成分 ${vs}\\sin{th}^\\circ$。",
                           f"衝突後：水平成分 ${vs}\\times{COS_TEX[th]}$、鉛直成分 ${es}\\times{vs}\\times{SIN_TEX[th]}$（上向き）。",
                           f"速さ $=\\sqrt{{(\\text{{水平}})^2+(\\text{{鉛直}})^2}}\\fallingdotseq{t(vp)}\\,\\mathrm{{m/s}}$。"],
                    alt=["$e=1$ なら速さが変わらないこと、$e=0$ なら水平成分だけが残ることを確かめ、答えがその間にあることを確認する。"],
                    pc=[("速度を床に平行・垂直に分解している", 2), ("値が正しい", 2)], pit=["速さ全体に $e$ をかける。"])
    ms = r.choice(["0.10", "0.20", "0.50"])
    vs = r.choice(["3.0", "5.0", "10", "20"])
    m, v = Q(ms), Q(vs)
    I = m * v * sp.sqrt(2)
    return numq(f"なめらかな水平面上を東向きに速さ {vs} m/s で進んでいた質量 {ms} kg の小球が、短い時間だけ力を受けて、北向きに同じ速さ {vs} m/s で進むようになった。小球が受けた力積の大きさは何 N·s か。",
                I, f"{P(m)}*{P(v)}*sqrt(2)", "$\\Delta\\vec{p}=m\\vec{v'}-m\\vec{v}$ をベクトルの差として求める。", "N·s", d=3,
                ap="速さが変わらなくても向きが変われば運動量は変化する。ベクトルの差をとる。",
                steps=[f"運動量の大きさはどちらも ${ms}\\times{vs}={t(m * v)}\\,\\mathrm{{kg\\cdot m/s}}$ で、向きが $90^\\circ$ 異なる。",
                       f"$|\\Delta\\vec{{p}}|=\\sqrt{{{t(m * v)}^2+{t(m * v)}^2}}={t(m * v)}\\sqrt{{2}}\\fallingdotseq{t(I)}\\,\\mathrm{{N\\cdot s}}$（向きは北西向き）。"],
                alt=["東向きを $x$、北向きを $y$ として成分で表すと $\\Delta\\vec{p}=(-mv,\\ mv)$。大きさは $\\sqrt2mv$。"],
                pc=[("運動量の変化をベクトルの差としている", 2), ("値が正しい", 2)], pit=["速さが変わらないので力積は 0 と答える。"])


@gen("standard_practice", 4, ["computation", "condition_check"])
def circular_apps(r):
    kind = r.choice(["curve", "top", "bottom", "conical", "turntable"])
    if kind == "curve":
        mus = r.choice(["0.40", "0.50", "0.60", "0.80"])
        rs = r.choice(["20", "40", "50", "80", "100"])
        mu, rr = Q(mus), Q(rs)
        v = sp.sqrt(mu * G * rr)
        return numq(f"水平な道路上の半径 {rs} m のカーブを、自動車が等速円運動で曲がる。タイヤと路面の間の静止摩擦係数を {mus} とするとき、横滑りせずに曲がれる最大の速さは何 m/s か。" + GS,
                    v, f"sqrt({P(mu)}*9.8*{P(rr)})", "向心力は静止摩擦力。$m\\dfrac{v^2}{r}\\leqq\\mu mg$。", "m/s", d=3,
                    ap="水平なカーブで中心向きにはたらく実在の力は、路面からの静止摩擦力だけ。その最大値が $\\mu mg$。",
                    steps=["中心向きの運動方程式：$m\\dfrac{v^2}{r}=f$（$f$ は静止摩擦力）。", "$f\\leqq\\mu N=\\mu mg$ より $v^2\\leqq\\mu gr$。",
                           f"$v_{{\\max}}=\\sqrt{{{mus}\\times9.8\\times{rs}}}\\fallingdotseq{t(v)}\\,\\mathrm{{m/s}}$。"],
                    alt=["答えが質量によらないことを確かめる（大型車でも条件は同じ）。"],
                    pc=[("向心力が静止摩擦力であるとしている", 2), ("最大摩擦力の条件で値を求めている", 2)], pit=["動摩擦力を使う。", "遠心力と摩擦力のつり合いと、運動方程式を混ぜて二重に数える。"])
    if kind == "top":
        Ls = r.choice(["0.40", "0.50", "0.90", "1.0", "1.6", "2.5"])
        L = Q(Ls)
        v = sp.sqrt(G * L)
        return numq(f"長さ {Ls} m の軽い糸の一端を固定し、他端につけた小球を鉛直面内で円運動させる。糸がたるまずに最高点を通過するために、最高点で小球がもつべき最小の速さは何 m/s か。" + GS,
                    v, f"sqrt(9.8*{P(L)})", "最高点で $m\\dfrac{v^2}{L}=S+mg$、$S\\geqq0$。", "m/s", d=3,
                    ap="最高点では張力も重力も中心（下）向き。糸がたるまない条件は張力 $S\\geqq0$。",
                    steps=["最高点の運動方程式：$m\\dfrac{v^2}{L}=S+mg$。", "$S=m\\dfrac{v^2}{L}-mg\\geqq0$ より $v\\geqq\\sqrt{gL}$。",
                           f"$v_{{\\min}}=\\sqrt{{9.8\\times{Ls}}}\\fallingdotseq{t(v)}\\,\\mathrm{{m/s}}$。"],
                    alt=["$S=0$ のとき重力だけで向心力をまかなう、と考えて $m\\dfrac{v^2}{L}=mg$ から直接求めてもよい。"],
                    pc=[("最高点の運動方程式を立てている", 2), ("$S\\geqq0$ の条件で値を求めている", 2)], pit=["最高点で速さ 0 でもよいと考える。"])
    if kind == "bottom":
        ms = r.choice(["0.10", "0.20", "0.50", "1.0"])
        Ls = r.choice(["0.50", "1.0", "2.0"])
        vs = r.choice(["2.0", "3.0", "4.0", "5.0"])
        m, L, v = Q(ms), Q(Ls), Q(vs)
        S = m * G + m * v ** 2 / L
        return numq(f"長さ {Ls} m の軽い糸に質量 {ms} kg の小球をつけて振り子にした。小球が最下点を速さ {vs} m/s で通過するときの糸の張力の大きさは何 N か。" + GS,
                    S, f"{P(m)}*9.8+{P(m)}*{P(v)}**2/{P(L)}", "最下点で中心（上）向きを正として $m\\dfrac{v^2}{L}=S-mg$。", "N", d=3,
                    ap="最下点の瞬間は半径 $L$ の円運動の一部。中心は真上にあるので、上向きを正として運動方程式を立てる。",
                    steps=["最下点の運動方程式：$m\\dfrac{v^2}{L}=S-mg$。", f"$S=mg+m\\dfrac{{v^2}}{{L}}={ms}\\times9.8+{ms}\\times\\dfrac{{{vs}^2}}{{{Ls}}}$。",
                           f"$S\\fallingdotseq{t(S)}\\,\\mathrm{{N}}$。"],
                    alt=["静止しているとき（$v=0$）は $S=mg$ になることで、式の形を確かめる。"],
                    pc=[("最下点の運動方程式を立てている", 2), ("値が正しい", 2)], pit=["張力を $mg$ とする（つり合いと考える）。"])
    if kind == "conical":
        Ls = r.choice(["0.50", "1.0", "1.6", "2.0"])
        th = r.choice([30, 45, 60])
        L = Q(Ls)
        T = 2 * sp.pi * sp.sqrt(L * COS[th] / G)
        return numq(f"図のように、長さ {Ls} m の軽い糸の一端を天井に固定し、他端におもりをつけて、糸が鉛直方向と ${th}^\\circ$ の角をなすように水平面内で等速円運動させた（円錐振り子）。図の円錐振り子の周期は何 s か。" + GS,
                    T, f"2*pi*sqrt({P(L)}*cos(deg({th}))/9.8)", "鉛直方向のつり合いと水平方向の運動方程式から $T=2\\pi\\sqrt{\\dfrac{L\\cos\\theta}{g}}$。", "s", d=4,
                    fig=figure("天井から長さ L の糸でつるしたおもりが、鉛直と角 θ をなして水平面内で円運動する円錐振り子", conical_svg()),
                    ap="おもりにはたらく力は重力と張力だけ。鉛直方向はつり合い、水平方向は中心向きの円運動。",
                    steps=["鉛直：$S\\cos\\theta=mg$。水平：$m(L\\sin\\theta)\\omega^2=S\\sin\\theta$。", "2式から $\\omega^2=\\dfrac{g}{L\\cos\\theta}$。",
                           f"$T=2\\pi\\sqrt{{\\dfrac{{{Ls}\\times\\cos{th}^\\circ}}{{9.8}}}}\\fallingdotseq{t(T)}\\,\\mathrm{{s}}$。"],
                    alt=["$\\theta\\to0$ で単振り子の周期 $2\\pi\\sqrt{\\dfrac{L}{g}}$ に近づくことから、式の形を確かめる。"],
                    pc=[("鉛直方向のつり合いを立てている", 1), ("水平方向の運動方程式を立てている", 2), ("値が正しい", 1)], pit=["円の半径を $L$ とする（正しくは $L\\sin\\theta$）。"])
    mus = r.choice(["0.20", "0.30", "0.40", "0.50"])
    rcm = r.choice([10, 20, 25, 40, 50])
    mu, rr = Q(mus), sp.Rational(rcm, 100)
    w = sp.sqrt(mu * G / rr)
    return numq(f"水平な回転円板の中心から {rcm} cm の位置に小物体を置き、円板の回転の角速度を少しずつ大きくした。小物体と円板の間の静止摩擦係数を {mus} とするとき、小物体が滑り出さない最大の角速度は何 rad/s か。" + GS,
                w, f"sqrt({P(mu)}*9.8/{P(rr)})", "$mr\\omega^2\\leqq\\mu mg$。", "rad/s", d=3,
                ap="円板とともに回る小物体の向心力は静止摩擦力。角速度が大きいほど必要な向心力が大きくなる。",
                steps=["中心向きの運動方程式：$mr\\omega^2=f\\leqq\\mu mg$。", "$\\omega^2\\leqq\\dfrac{\\mu g}{r}$。",
                       f"$\\omega_{{\\max}}=\\sqrt{{\\dfrac{{{mus}\\times9.8}}{{{dec(rr)}}}}}\\fallingdotseq{t(w)}\\,\\mathrm{{rad/s}}$。"],
                alt=["中心から遠いほど滑りやすい（$\\omega_{\\max}$ が小さい）ことを式から読み取り、経験と照らし合わせる。"],
                pc=[("向心力を静止摩擦力としている", 2), ("値が正しい", 2)], pit=["半径を cm のまま代入する。"])


@gen("standard_practice", 3, ["computation", "application"])
def shm_apps(r):
    kind = r.choice(["vert", "v_at_x", "vmax_k", "mass"])
    if kind == "vert":
        dcm = r.choice([1, 2, 4, 5, 8, 10, 20, 25])
        d = sp.Rational(dcm, 100)
        T = 2 * sp.pi * sp.sqrt(d / G)
        return numq(f"軽いばねの上端を天井に固定し、下端におもりをつるしたところ、ばねは自然の長さから {dcm} cm 伸びて静止した。このおもりを鉛直方向に単振動させたときの周期は何 s か。" + GS,
                    T, f"2*pi*sqrt({P(d)}/9.8)", "つり合い $kd=mg$ より $\\dfrac{m}{k}=\\dfrac{d}{g}$。", "s", d=3,
                    ap="質量もばね定数も与えられていないが、つり合いの式から比 $\\dfrac{m}{k}$ がわかる。",
                    steps=["つり合い：$kd=mg$ より $\\dfrac{m}{k}=\\dfrac{d}{g}$。", "$T=2\\pi\\sqrt{\\dfrac{m}{k}}=2\\pi\\sqrt{\\dfrac{d}{g}}$。",
                           f"$T=2\\pi\\sqrt{{\\dfrac{{{dec(d)}}}{{9.8}}}}\\fallingdotseq{t(T)}\\,\\mathrm{{s}}$。"],
                    alt=["同じ式が長さ $d$ の単振り子の周期と同じ形になることに注目して確かめる。"],
                    pc=[("つり合いから $\\dfrac{m}{k}$ を求めている", 2), ("値が正しい", 2)], pit=["鉛直ばね振り子では重力のぶん周期が変わると考える。"])
    if kind == "v_at_x":
        A, x = r.choice([(5, 3), (5, 4), (10, 6), (10, 8), (13, 5), (13, 12)])
        ws = r.choice(["2.0", "4.0", "5.0", "10"])
        w = Q(ws)
        v = w * sp.sqrt(sp.Rational(A ** 2 - x ** 2, 10000))
        return numq(f"振幅 {iv(A)} cm、角振動数 {ws} rad/s で単振動している物体が、振動の中心から {iv(x)} cm の位置を通過するときの速さは何 m/s か。",
                    v, f"{P(w)}*sqrt(Rational({A}**2-{x}**2,10000))", "$v=\\omega\\sqrt{A^2-x^2}$。", "m/s", d=3,
                    ap="単振動のエネルギー保存 $\\dfrac12mv^2+\\dfrac12Kx^2=\\dfrac12KA^2$ と $K=m\\omega^2$ から $v=\\omega\\sqrt{A^2-x^2}$。",
                    steps=[f"$\\sqrt{{A^2-x^2}}=\\sqrt{{{A}^2-{x}^2}}={sp.sqrt(A ** 2 - x ** 2)}\\,\\mathrm{{cm}}={dec(sp.sqrt(A ** 2 - x ** 2) / 100)}\\,\\mathrm{{m}}$。", f"$v={ws}\\times{dec(sp.sqrt(A ** 2 - x ** 2) / 100)}={t(v)}\\,\\mathrm{{m/s}}$。"],
                    alt=["等速円運動の図で、半径 $A$ の円の上で $x$ 軸への射影が $x$ となる点を考え、速度の成分を三角比で求めてもよい。"],
                    pc=[("$v=\\omega\\sqrt{A^2-x^2}$ を用いている", 2), ("単位を m に直して値が正しい", 2)], pit=["cm のまま答える。", "$\\omega(A-x)$ とする。"])
    if kind == "vmax_k":
        ks, ms = r.choice([("100", "1.0"), ("40", "0.10"), ("90", "0.10"), ("200", "2.0"), ("50", "0.50"), ("160", "0.40")])
        k, m = Q(ks), Q(ms)
        Acm = r.choice([2, 4, 5, 10])
        A = sp.Rational(Acm, 100)
        v = A * sp.sqrt(k / m)
        return numq(f"なめらかな水平面上で、ばね定数 {ks} N/m の軽いばねに質量 {ms} kg の物体をつけ、つり合いの位置から {iv(Acm)} cm 引いて静かにはなした。物体の速さの最大値は何 m/s か。",
                    v, f"{P(A)}*sqrt({P(k)}/{P(m)})", "$v_{\\max}=A\\omega=A\\sqrt{\\dfrac{k}{m}}$。", "m/s", d=3, ps=["multiple_solutions"],
                    ap="引いた距離が振幅。速さはつり合いの位置で最大となり $A\\omega$。",
                    steps=[f"$\\omega=\\sqrt{{\\dfrac{{{ks}}}{{{ms}}}}}={t(sp.sqrt(k / m), 3)}\\,\\mathrm{{rad/s}}$。", f"$v_{{\\max}}=A\\omega={dec(A)}\\times{t(sp.sqrt(k / m), 3)}\\fallingdotseq{t(v)}\\,\\mathrm{{m/s}}$。"],
                    alt=["弾性エネルギーの保存 $\\dfrac12kA^2=\\dfrac12mv_{\\max}{}^2$ から求めても同じ値になる。"],
                    pc=[("振幅を正しく読み取っている", 1), ("$A\\omega$ またはエネルギー保存を用いている", 2), ("値が正しい", 1)], pit=["振幅を cm のまま使う。"])
    Ts = r.choice(["0.40", "0.60", "1.2", "1.5", "2.0"])
    T0 = Q(Ts)
    f, lab = r.choice([(sp.Integer(4), "4倍"), (sp.Integer(9), "9倍"), (sp.Rational(1, 4), "$\\dfrac{1}{4}$ 倍"), (sp.Rational(9, 4), "$\\dfrac{9}{4}$ 倍")])
    T1 = T0 * sp.sqrt(f)
    return numq(f"ある軽いばねにおもりをつけたばね振り子の周期は {Ts} s であった。おもりの質量を{lab}にとりかえると、周期は何 s になるか。",
                T1, f"{P(T0)}*sqrt({P(f)})", "$T\\propto\\sqrt{m}$。", "s", d=2,
                ap="$T=2\\pi\\sqrt{\\dfrac{m}{k}}$ より、ばねが同じなら周期は質量の平方根に比例する。",
                steps=[f"$\\dfrac{{T'}}{{T}}=\\sqrt{{\\dfrac{{m'}}{{m}}}}=\\sqrt{{{f if f.q == 1 else chr(92) + 'dfrac{' + str(f.p) + '}{' + str(f.q) + '}'}}}={t(sp.sqrt(f))}$。", f"$T'={Ts}\\times{t(sp.sqrt(f))}={t(T1)}\\,\\mathrm{{s}}$。"],
                alt=["ばね定数を逆算してから新しい周期を計算しても同じになるが、比で考えると速い。"],
                pc=[("周期が質量の平方根に比例することを用いている", 2), ("値が正しい", 2)], pit=["周期が質量に比例するとする。"])


@gen("standard_practice", 3, ["computation", "application"])
def orbit_apps(r):
    kind = r.choice(["v1", "orbit_v", "period", "escape"])
    if kind == "v1":
        v = sp.sqrt(G * RE)
        return numq("地表すれすれを等速円運動する人工衛星の速さ（第1宇宙速度）は何 m/s か。" + RS + "空気抵抗は無視する。", v, "sqrt(9.8*Rational(64,10)*10**6)",
                    "$m\\dfrac{v^2}{R}=mg$ より $v=\\sqrt{gR}$。", "m/s", n=2, d=3,
                    ap="地表すれすれなら軌道半径は $R$、向心力は重力 $mg$。",
                    steps=["$m\\dfrac{v^2}{R}=mg$。", "$v=\\sqrt{gR}=\\sqrt{9.8\\times6.4\\times10^6}$。", f"$v\\fallingdotseq{t(v, 2)}\\,\\mathrm{{m/s}}$（約 7.9 km/s）。"],
                    alt=["$GM=gR^2$ を使い、$v=\\sqrt{\\dfrac{GM}{R}}$ に代入しても同じ式になる。"],
                    pc=[("重力を向心力として運動方程式を立てている", 2), ("値が正しい", 2)], pit=["指数の計算で平方根をとり誤る。"])
    if kind == "escape":
        v = sp.sqrt(2 * G * RE)
        return numq("地表から物体を打ち出し、地球の引力圏から無限遠まで飛び去らせるのに必要な最小の速さ（第2宇宙速度）は何 m/s か。" + RS + "空気抵抗は無視する。", v,
                    "sqrt(2*9.8*Rational(64,10)*10**6)", "$\\dfrac12mv^2-G\\dfrac{Mm}{R}\\geqq0$ より $v\\geqq\\sqrt{2gR}$。", "m/s", n=2, d=4,
                    ps=["cross_unit"], rel=["HS-PHYB-U02"],
                    ap="無限遠（$U=0$）に達したとき運動エネルギーが 0 以上であればよい。力学的エネルギー保存を使う。",
                    steps=["地表：$\\dfrac12mv^2-G\\dfrac{Mm}{R}$、無限遠：$\\dfrac12mv_\\infty{}^2+0\\geqq0$。", "$v^2\\geqq\\dfrac{2GM}{R}=2gR$。",
                           f"$v_{{\\min}}=\\sqrt{{2\\times9.8\\times6.4\\times10^6}}\\fallingdotseq{t(v, 2)}\\,\\mathrm{{m/s}}$（約 11 km/s）。"],
                    alt=["第1宇宙速度 $\\sqrt{gR}$ の $\\sqrt2$ 倍になることから確かめる。"],
                    pc=[("万有引力の位置エネルギーで力学的エネルギー保存を立てている", 2), ("値が正しい", 2)], pit=["位置エネルギーを $mgh$ で計算する（地表付近でしか使えない）。"])
    k = r.choice([2, 3, 4])
    hlab = {2: "地球の半径に等しい", 3: "地球の半径の2倍の", 4: "地球の半径の3倍の"}[k]
    rr = k * RE
    v = sp.sqrt(G * RE ** 2 / rr)
    if kind == "orbit_v":
        return numq(f"図のように、地表からの高さが{hlab}円軌道を回る人工衛星がある。この人工衛星の速さは何 m/s か。" + RS, v, f"sqrt(9.8*(Rational(64,10)*10**6)**2/({k}*Rational(64,10)*10**6))",
                    f"$v=\\sqrt{{\\dfrac{{GM}}{{r}}}}=\\sqrt{{\\dfrac{{gR}}{{{k}}}}}$。", "m/s", n=2, d=3, fig=figure("地球を中心とする半径 r の円軌道を回る人工衛星", orbit_svg()),
                    ap=f"軌道半径は地球の中心から測って $r={k}R$。$G$ と $M$ がないので $GM=gR^2$ を使う。",
                    steps=[f"$r=R+{'' if k == 2 else k - 1}R={k}R$。", f"$m\\dfrac{{v^2}}{{r}}=G\\dfrac{{Mm}}{{r^2}}$ と $GM=gR^2$ より $v=\\sqrt{{\\dfrac{{gR^2}}{{{k}R}}}}=\\sqrt{{\\dfrac{{gR}}{{{k}}}}}$。",
                           f"$v\\fallingdotseq{t(v, 2)}\\,\\mathrm{{m/s}}$。"],
                    alt=[f"第1宇宙速度 $\\sqrt{{gR}}\\fallingdotseq7.9\\times10^3\\,\\mathrm{{m/s}}$ の $\\dfrac{{1}}{{\\sqrt{{{k}}}}}$ 倍として求めてもよい。"],
                    pc=[("軌道半径を地球の中心から測っている", 2), ("値が正しい", 2)], pit=["軌道半径を地表からの高さとする。"])
    T = 2 * sp.pi * rr / v
    return numq(f"図のように、地表からの高さが{hlab}円軌道を回る人工衛星がある。この人工衛星の公転周期は何 s か。" + RS, T,
                f"2*pi*{k}*Rational(64,10)*10**6/sqrt(9.8*(Rational(64,10)*10**6)**2/({k}*Rational(64,10)*10**6))",
                "$T=\\dfrac{2\\pi r}{v}=2\\pi\\sqrt{\\dfrac{r^3}{gR^2}}$。", "s", n=2, d=4, fig=figure("地球を中心とする半径 r の円軌道を回る人工衛星", orbit_svg()),
                ap="円軌道の速さを求めてから、円周の長さを速さで割る。",
                steps=[f"$r={k}R$、$v=\\sqrt{{\\dfrac{{gR}}{{{k}}}}}\\fallingdotseq{t(v, 3)}\\,\\mathrm{{m/s}}$。", f"$T=\\dfrac{{2\\pi\\times{k}R}}{{v}}\\fallingdotseq{t(T, 2)}\\,\\mathrm{{s}}$。"],
                alt=["地表すれすれの衛星の周期（約 $5.1\\times10^3\\,\\mathrm{s}$）とケプラーの第3法則 $T\\propto r^{\\frac32}$ から、その $" + str(k) + "^{\\frac32}$ 倍として確かめる。"],
                pc=[("軌道半径を正しくとっている", 1), ("速さを求めている", 1), ("周期が正しい", 2)], pit=["軌道半径を地表からの高さとする。"])


# ======================================================================
# C 思考力・記述応用
# ======================================================================

@gen("thinking_writing", 3, ["written_reasoning", "concept"])
def derive_c(r):
    kind = r.choice(["mom", "centri", "shm", "kepler", "escape", "loss"])
    if kind == "mom":
        return desc("一直線上で2物体 A（質量 $m_1$）、B（質量 $m_2$）が衝突する。衝突の前後の速度をそれぞれ $v_1,\\ v_2$、$v_1',\\ v_2'$ とする。外力がはたらかないとき、運動量の和が保存されることを、作用・反作用の法則と力積の関係を用いて示しなさい。",
                    "衝突中に A が B から受ける力を $F$ とすると、作用・反作用の法則より B は A から $-F$ を受け、2力のはたらく時間 $\\Delta t$ は等しい。A：$m_1v_1'-m_1v_1=F\\Delta t$、B：$m_2v_2'-m_2v_2=-F\\Delta t$。辺々加えると $m_1v_1'+m_2v_2'-(m_1v_1+m_2v_2)=0$ となり、運動量の和は保存される。",
                    "2物体が受ける力積が大きさ等しく逆向きになることを使う。",
                    [("作用・反作用の法則で力が逆向き・等大であり、時間が等しいことを述べている", 3), ("各物体について力積と運動量の変化の式を立てている", 3), ("辺々加えて結論を導いている", 2)], d=3, p=8, kind="proof", lines=8,
                    ap="運動方程式を時間で積み重ねたものが力積の式。2物体の力積を足し合わせる。",
                    steps=["作用・反作用：$F$ と $-F$、同じ時間 $\\Delta t$。", "A・B それぞれ $\\Delta p=$ 力積。", "加えて右辺 0。"],
                    alt=["力が時間とともに変化する場合も、各瞬間で作用・反作用が成り立つので、$F$−$t$ グラフの面積（力積）が等しく逆符号になると説明できる。"],
                    pc=[("作用反作用", 3), ("力積の式", 3), ("結論", 2)], pit=["「力が等しいから速度の変化が等しい」と、質量を考えずに書く。"])
    if kind == "centri":
        return desc("半径 $r$ の円周上を速さ $v$ で等速円運動する物体の加速度について、短い時間 $\\Delta t$ の間の速度の変化を考えることにより、加速度の大きさが $\\dfrac{v^2}{r}$ で、向きが円の中心向きであることを説明しなさい。",
                    "時間 $\\Delta t$ の間に物体は角 $\\Delta\\theta=\\dfrac{v\\Delta t}{r}$ だけ回り、速度ベクトルも同じ角だけ向きを変える。速度の変化 $\\Delta\\vec{v}$ は2辺が $v$、頂角 $\\Delta\\theta$ の二等辺三角形の底辺で、$\\Delta\\theta$ が小さいとき大きさ $v\\Delta\\theta$。よって $a=\\dfrac{v\\Delta\\theta}{\\Delta t}=\\dfrac{v^2}{r}$。$\\Delta t\\to0$ で底辺は速度に垂直になるので、加速度は円の中心を向く。",
                    "速度ベクトルの始点をそろえ、変化分を二等辺三角形の底辺として扱う。",
                    [("回転角と速度の向きの変化が等しいことを述べている", 2), ("$|\\Delta\\vec{v}|\\fallingdotseq v\\Delta\\theta$ から $a=\\dfrac{v^2}{r}$ を導いている", 4), ("向きが中心向きであることを説明している", 2)], d=4, p=8, kind="proof", lines=8,
                    ap="速さが一定でも速度の向きが変わる。その変化の割合が加速度。",
                    steps=["$\\Delta\\theta=\\omega\\Delta t$。", "$|\\Delta\\vec{v}|\\fallingdotseq v\\Delta\\theta$。", "$a=v\\omega=\\dfrac{v^2}{r}$、中心向き。"],
                    alt=["位置を $(r\\cos\\omega t,\\ r\\sin\\omega t)$ と表し、2回微分して $\\vec{a}=-\\omega^2\\vec{r}$ を得る方法でも示せる（数学Ⅲ）。"],
                    pc=[("角", 2), ("大きさ", 4), ("向き", 2)], pit=["速さが一定なので加速度は 0 と書く。"],
                    chk=("expand(v*(v/r))", "v**2/r", "expand", "intermediate"))
    if kind == "shm":
        return desc("なめらかな水平面上で、ばね定数 $k$ のばねにつけた質量 $m$ の物体が、$x=A\\sin\\omega t$ で表される単振動をしている。（1）加速度 $a$ を $x$ を用いて表しなさい（$v=A\\omega\\cos\\omega t$、$a=-A\\omega^2\\sin\\omega t$ を用いてよい）。（2）運動方程式と比べて $\\omega$ を $m,\\ k$ で表し、周期が振幅によらないことを説明しなさい。",
                    "（1）$a=-A\\omega^2\\sin\\omega t=-\\omega^2x$。（2）物体にはたらく力はばねの弾性力 $-kx$ なので、運動方程式は $ma=-kx$。（1）と比べると $-m\\omega^2x=-kx$ がすべての $x$ で成り立つので $\\omega=\\sqrt{\\dfrac{k}{m}}$。周期 $T=\\dfrac{2\\pi}{\\omega}=2\\pi\\sqrt{\\dfrac{m}{k}}$ は $A$ を含まないので、振幅によらない。",
                    "単振動の加速度は $-\\omega^2x$。運動方程式の係数と比べる。",
                    [("（1）$a=-\\omega^2x$ を示している", 2), ("（2）運動方程式 $ma=-kx$ を立て、係数比較で $\\omega$ を求めている", 4), ("周期が振幅を含まないことを述べている", 2)], d=3, p=8, lines=8,
                    ap="単振動の条件は「加速度が変位に比例し逆向き」。比例定数が $\\omega^2$。",
                    steps=["$a=-\\omega^2x$。", "$ma=-kx$ と比べて $m\\omega^2=k$。", "$T=2\\pi\\sqrt{\\dfrac{m}{k}}$、$A$ を含まない。"],
                    alt=["次元解析：$\\sqrt{\\dfrac{m}{k}}$ の単位は $\\sqrt{\\dfrac{\\mathrm{kg}}{\\mathrm{N/m}}}=\\mathrm{s}$ で、時間の次元をもつことで確かめる。"],
                    pc=[("（1）", 2), ("（2）係数比較", 4), ("振幅", 2)], pit=["$\\omega=\\sqrt{\\dfrac{m}{k}}$ と逆にする。"],
                    chk=("2*pi/sqrt(Rational(9,4))", "4*pi/3", None, "intermediate"))
    if kind == "kepler":
        return desc("質量 $M$ の恒星のまわりを、質量 $m$ の惑星が半径 $r$、周期 $T$ の等速円運動をしているとする。万有引力の法則と円運動の運動方程式から $\\dfrac{T^2}{r^3}=\\dfrac{4\\pi^2}{GM}$ を導き、この結果がケプラーの第3法則とどのように対応するかを述べなさい。",
                    "向心力は万有引力なので $mr\\omega^2=G\\dfrac{Mm}{r^2}$、$\\omega=\\dfrac{2\\pi}{T}$ を代入すると $mr\\dfrac{4\\pi^2}{T^2}=G\\dfrac{Mm}{r^2}$。整理して $\\dfrac{T^2}{r^3}=\\dfrac{4\\pi^2}{GM}$。右辺は恒星の質量 $M$ だけで決まり、惑星の質量 $m$ を含まないので、同じ恒星のまわりのすべての惑星で $\\dfrac{T^2}{r^3}$ が等しい。これは「公転周期の2乗は軌道の半長軸の3乗に比例する」というケプラーの第3法則（円軌道の場合）である。",
                    "向心力＝万有引力。$m$ が約分されることに注目。",
                    [("円運動の運動方程式を万有引力で立てている", 3), ("$\\omega=\\dfrac{2\\pi}{T}$ を用いて正しく整理している", 3), ("右辺が惑星によらないこととケプラーの第3法則の対応を述べている", 2)], d=4, p=8, kind="proof", lines=8, ps=["cross_unit"], rel=["HS-MATH2-U04"],
                    ap="円運動の運動方程式 $mr\\omega^2=F$ に、$F$ として万有引力を入れる。",
                    steps=["$mr\\omega^2=G\\dfrac{Mm}{r^2}$。", "$\\omega=\\dfrac{2\\pi}{T}$ を代入して整理。", "右辺は $M$ のみ → 第3法則。"],
                    alt=["$v=\\sqrt{\\dfrac{GM}{r}}$ を先に求め、$T=\\dfrac{2\\pi r}{v}$ を2乗して導いてもよい。"],
                    pc=[("運動方程式", 3), ("整理", 3), ("対応", 2)], pit=["$\\omega=2\\pi T$ と周期と角速度の関係を誤る。"],
                    chk=("simplify((2*pi/sqrt(m/(r**3)))**2/r**3)", "4*pi**2/m", None, "intermediate"))
    if kind == "escape":
        return desc("地球（質量 $M$、半径 $R$）の表面から質量 $m$ の物体を鉛直上向きに速さ $v_0$ で打ち上げる。万有引力による位置エネルギーが $U=-G\\dfrac{Mm}{r}$（$r$ は地球の中心からの距離）であることを用いて、物体が地球に戻ってこないための $v_0$ の条件を求め、それが $\\sqrt{2gR}$ と表せることを示しなさい。空気抵抗と地球の自転は無視する。",
                    "力学的エネルギー保存より、距離 $r$ での速さを $v$ とすると $\\dfrac12mv_0{}^2-G\\dfrac{Mm}{R}=\\dfrac12mv^2-G\\dfrac{Mm}{r}$。無限遠（$r\\to\\infty$）まで到達するには、そこでの運動エネルギーが 0 以上であればよいので $\\dfrac12mv_0{}^2-G\\dfrac{Mm}{R}\\geqq0$、すなわち $v_0\\geqq\\sqrt{\\dfrac{2GM}{R}}$。地表で $mg=G\\dfrac{Mm}{R^2}$ より $GM=gR^2$ なので $v_0\\geqq\\sqrt{2gR}$。",
                    "無限遠で $U=0$。そこで運動エネルギーが負にならない条件。",
                    [("力学的エネルギー保存の式を万有引力の位置エネルギーで立てている", 3), ("無限遠での条件から不等式を導いている", 3), ("$GM=gR^2$ を用いて $\\sqrt{2gR}$ を示している", 2)], d=4, p=8, kind="proof", lines=8, ps=["cross_unit"], rel=["HS-PHYB-U02"],
                    ap="位置エネルギーの基準は無限遠。地表での力学的エネルギーが 0 以上なら無限遠まで行ける。",
                    steps=["エネルギー保存を立てる。", "$r\\to\\infty$ で $\\dfrac12mv^2\\geqq0$。", "$GM=gR^2$ を代入。"],
                    alt=["$mgh$ を使うと高さとともに重力が弱まることを無視することになり、誤った結果（無限に高い所へは届かない）になることを確かめる。"],
                    pc=[("保存の式", 3), ("条件", 3), ("書きかえ", 2)], pit=["位置エネルギーを $mgh$ として計算する。"],
                    chk=("sqrt(2*(a*b**2)/b)", "sqrt(2*a*b)", None, "intermediate"))
    return desc("なめらかな水平面上で、速さ $v$ で進む質量 $m_1$ の物体が静止している質量 $m_2$ の物体に衝突し、一体となった。（1）一体となった後の速さを求めなさい。（2）衝突で失われた運動エネルギー $\\Delta K$ を求め、$\\Delta K=\\dfrac{m_1m_2}{2(m_1+m_2)}v^2$ と表せることを示しなさい。（3）失われたエネルギーはどうなったと考えられるか述べなさい。",
                "（1）運動量保存 $m_1v=(m_1+m_2)V$ より $V=\\dfrac{m_1v}{m_1+m_2}$。（2）$\\Delta K=\\dfrac12m_1v^2-\\dfrac12(m_1+m_2)V^2=\\dfrac12m_1v^2-\\dfrac{m_1{}^2v^2}{2(m_1+m_2)}=\\dfrac{m_1v^2\\{(m_1+m_2)-m_1\\}}{2(m_1+m_2)}=\\dfrac{m_1m_2}{2(m_1+m_2)}v^2$。（3）物体の変形や、熱・音のエネルギーに変わった。",
                "運動量保存で $V$ を求め、運動エネルギーの差を通分して整理する。",
                [("（1）運動量保存から $V$ を求めている", 2), ("（2）運動エネルギーの差を正しく整理している", 4), ("（3）熱・音・変形などへの変換を述べている", 2)], d=3, p=8, lines=9, ps=["computation"],
                ap="保存されるのは運動量だけ。運動エネルギーは差をとって減少量を計算する。",
                steps=["$V=\\dfrac{m_1v}{m_1+m_2}$。", "$\\Delta K$ を通分。", "熱・音・変形。"],
                alt=["重心とともに動く立場で見ると、衝突前の相対運動のエネルギー $\\dfrac12\\cdot\\dfrac{m_1m_2}{m_1+m_2}v^2$ がすべて失われる、と解釈できる。"],
                pc=[("（1）", 2), ("（2）", 4), ("（3）", 2)], pit=["通分の際に $m_1{}^2$ の約分を誤る。"],
                chk=("simplify(Rational(1,2)*a*v**2-Rational(1,2)*(a+b)*(a*v/(a+b))**2-a*b*v**2/(2*(a+b)))", "0", None, "intermediate"))


@gen("thinking_writing", 3, ["cross_unit", "written_reasoning", "computation"], rel=["HS-PHYB-U02"])
def ballistic_c(r):
    mg, Ms = r.choice([(10, "0.99"), (20, "1.98"), (10, "1.99"), (50, "2.45"), (20, "0.98")])
    m = sp.Rational(mg, 1000)
    M = Q(Ms)
    vb = r.choice([100, 200, 250, 300, 400])
    V = m * vb / (m + M)
    h = V ** 2 / (2 * G)
    K0 = m * vb ** 2 / 2
    K1 = (m + M) * V ** 2 / 2
    ratio = K1 / K0
    return desc(f"質量 {Ms} kg の木片が、軽い糸で天井からつるされて静止している。質量 {mg} g の弾丸を水平に速さ {vb} m/s で打ち込んだところ、弾丸は木片の中で止まり、両者は一体となって振れ上がった。" + GS +
                "（1）弾丸が木片の中で止まった直後の、一体となった木片の速さ $V$ を求めなさい。（2）木片が上がる最大の高さ $h$ を求めなさい。（3）打ち込む前の弾丸の運動エネルギーのうち、一体となった直後に運動エネルギーとして残っている割合を求め、この衝突で力学的エネルギー保存則を使ってはいけない理由を述べなさい。数値は有効数字2桁で答えなさい。",
                f"（1）$V\\fallingdotseq{t(V, 2)}\\,\\mathrm{{m/s}}$　（2）$h\\fallingdotseq{t(h, 2)}\\,\\mathrm{{m}}$　（3）割合 $\\dfrac{{m}}{{m+M}}\\fallingdotseq{t(ratio, 2)}$（約 {t(ratio * 100, 2)} %）。弾丸が木片にめり込む間に、木片を変形させたり熱が発生したりして運動エネルギーの大部分が失われる（非弾性衝突）ので、衝突の前後では力学的エネルギーは保存されない。衝突の前後は運動量保存、衝突後に振れ上がる間は力学的エネルギー保存を用いる。",
                "衝突（運動量保存）と振れ上がり（力学的エネルギー保存）の2段階に分ける。",
                [("（1）運動量保存の式を立てて $V$ を求めている", 2), ("（2）振れ上がりで力学的エネルギー保存を用いて $h$ を求めている", 2), ("（3）割合を求めている", 2), ("（3）衝突で運動エネルギーが失われる理由と、法則の使い分けを述べている", 2)], d=4, p=8, lines=10,
                ap="打ち込む瞬間は非常に短い時間の衝突で、糸の張力・重力の力積は無視できる → 水平方向の運動量保存。",
                steps=[f"（1）${dec(m)}\\times{vb}=({dec(m)}+{Ms})V$、$V={t(V, 3)}\\,\\mathrm{{m/s}}$。", f"（2）$\\dfrac12(m+M)V^2=(m+M)gh$ より $h=\\dfrac{{V^2}}{{2g}}\\fallingdotseq{t(h, 2)}\\,\\mathrm{{m}}$。",
                       f"（3）$\\dfrac{{K_1}}{{K_0}}=\\dfrac{{\\frac12(m+M)V^2}}{{\\frac12mv^2}}=\\dfrac{{m}}{{m+M}}={t(ratio, 2)}$。"],
                alt=["（3）は $V=\\dfrac{mv}{m+M}$ を代入して文字式のまま整理すると $\\dfrac{m}{m+M}$ となり、数値を使わずに求められる。"],
                pc=[("（1）", 2), ("（2）", 2), ("（3）割合", 2), ("（3）理由", 2)], pit=["弾丸の運動エネルギーがすべて位置エネルギーになるとして $h$ を求める。", "g を kg に直し忘れる。"],
                chk=(f"({P(m)}*{vb}/({P(m)}+{P(M)}))**2/(2*9.8)", str(sp.nsimplify(h)), None, "intermediate"))


@gen("thinking_writing", 2, ["condition_check", "written_reasoning", "cross_unit"], rel=["HS-PHYB-U02"])
def loop_c(r):
    while True:
        rs = r.choice(["0.20", "0.40", "0.50", "1.0"])
        rr = Q(rs)
        k = r.choice([sp.Rational(3), sp.Rational(5, 2), sp.Rational(9, 4), sp.Rational(4), sp.Rational(11, 4)])
        h = k * rr
        if is_exact(t(h), h):
            break
    ms = r.choice(["0.10", "0.20", "0.50"])
    m = Q(ms)
    v2 = 2 * G * (h - 2 * rr)
    N = m * v2 / rr - m * G
    ok = h >= sp.Rational(5, 2) * rr
    hs = t(h)
    hc = t(sp.Rational(5, 2) * rr)
    if N == 0:
        res = f"（2）$N=m\\dfrac{{v^2}}{{r}}-mg=0$。（3）$N\\geqq0$ より $h\\geqq\\dfrac52r={hc}\\,\\mathrm{{m}}$。$h={hs}\\,\\mathrm{{m}}$ はちょうどこの条件の境目（$N=0$）なので、小球は P をぎりぎり通過できる。"
    elif ok:
        res = f"（2）$N=m\\dfrac{{v^2}}{{r}}-mg\\fallingdotseq{t(N, 2)}\\,\\mathrm{{N}}$。（3）$N\\geqq0$ より $h\\geqq\\dfrac52r={hc}\\,\\mathrm{{m}}$。$h={hs}\\,\\mathrm{{m}}$ はこれを満たすので、小球は最高点 P を通過できる。"
    else:
        res = f"（2）$N=m\\dfrac{{v^2}}{{r}}-mg$ を計算すると負になる（$N<0$）。（3）$N\\geqq0$ より $h\\geqq\\dfrac52r={hc}\\,\\mathrm{{m}}$。$h={hs}\\,\\mathrm{{m}}$ はこれを満たさないので、小球は P に達する前に軌道から離れる。"
    v2txt = f"$v^2=2g(h-2r)={dec(v2)}\\,\\mathrm{{m^2/s^2}}$" if v2 > 0 else "$v^2=2g(h-2r)\\leqq0$"
    return desc(f"図のように、なめらかな曲面の、床からの高さ {hs} m の位置に質量 {ms} kg の小球を置いて静かにはなすと、小球は曲面をすべり降り、床の上で半径 {rs} m のなめらかな円形ループの内側に入った。ループの最高点を P とする。" + GS +
                "（1）図のループで、小球が P に達したとすると、そこでの速さ $v$ の2乗はいくらになるか、力学的エネルギー保存則を用いて求めなさい。（2）P で小球がループから受ける垂直抗力 $N$ を、円運動の運動方程式から求めなさい。（3）小球が P を通過できるための高さ $h$ の条件を求め、この場合に通過できるかどうかを判断しなさい。",
                f"（1）{v2txt}　{res}",
                "エネルギー保存で速さ、円運動の運動方程式で垂直抗力、$N\\geqq0$ が離れない条件。",
                [("（1）力学的エネルギー保存で $v^2$ を求めている", 2), ("（2）P で中心向きの運動方程式 $m\\dfrac{v^2}{r}=N+mg$ を立てている", 2), ("（3）$N\\geqq0$ から $h\\geqq\\dfrac52r$ を導いている", 2), ("（3）与えられた $h$ で正しく判断している", 2)], d=5, p=8, lines=10,
                fig=figure("高さ h の曲面からすべり降りた小球が、半径 r の円形ループに入る。ループの最高点が P", loop_svg()),
                ap="P の高さは $2r$。P では垂直抗力も重力も中心（下）向き。ループから離れない条件は $N\\geqq0$。",
                steps=["（1）$mgh=mg\\cdot2r+\\dfrac12mv^2$ より $v^2=2g(h-2r)$。", "（2）$m\\dfrac{v^2}{r}=N+mg$ より $N=\\dfrac{2mg(h-2r)}{r}-mg=\\dfrac{mg(2h-5r)}{r}$。", "（3）$N\\geqq0\\iff h\\geqq\\dfrac52r$。"],
                alt=["最高点で必要な最小の速さ $\\sqrt{gr}$（$N=0$）を先に求め、エネルギー保存からその速さを得るのに必要な高さを逆算してもよい。"],
                pc=[("（1）", 2), ("（2）", 2), ("（3）条件", 2), ("（3）判断", 2)], pit=["P で速さが 0 より大きければ通過できる、と考える（$h>2r$ としてしまう）。"],
                chk=(f"2*9.8*({P(h)}-2*{P(rr)})", str(sp.nsimplify(v2)), None, "intermediate"))


@gen("thinking_writing", 2, ["multiple_solutions", "cross_unit", "written_reasoning"], rel=["HS-MATH3-U01"])
def bounce_c(r):
    hs, es = r.choice([("4.9", "0.50"), ("2.5", "0.60"), ("1.6", "0.50"), ("4.9", "0.80"), ("2.0", "0.40"), ("10", "0.60")])
    h, e = Q(hs), Q(es)
    t0 = sp.sqrt(2 * h / G)
    Ttot = t0 * (1 + e) / (1 - e)
    L = h * (1 + e ** 2) / (1 - e ** 2)
    return desc(f"高さ {hs} m の位置から小球を静かにはなしたところ、小球は水平な床で何度もはね返り、やがて静止した。床と小球の間の反発係数を {es} とし、空気抵抗と小球の大きさは無視する。" + GS +
                "（1）$n$ 回目にはね返った直後の速さを、最初に床に当たる直前の速さ $v_0$ と $e$ を用いて表しなさい。（2）小球が静止するまでに移動した道のりの合計を求めなさい。（3）小球が静止するまでの時間を求めなさい。（2）（3）は有効数字2桁で答えなさい。",
                f"（1）$e^nv_0$　（2）$h+2\\sum_{{n=1}}^{{\\infty}}e^{{2n}}h=h\\dfrac{{1+e^2}}{{1-e^2}}\\fallingdotseq{t(L, 2)}\\,\\mathrm{{m}}$　（3）$t_0=\\sqrt{{\\dfrac{{2h}}{{g}}}}$ として $t_0+2\\sum_{{n=1}}^{{\\infty}}e^nt_0=t_0\\dfrac{{1+e}}{{1-e}}\\fallingdotseq{t(Ttot, 2)}\\,\\mathrm{{s}}$",
                "はね返るたびに速さは $e$ 倍、高さは $e^2$ 倍、往復時間は $e$ 倍。無限等比級数の和を使う。",
                [("（1）はね返りごとに速さが $e$ 倍になることを用いている", 2), ("（2）高さが $e^2$ 倍の等比数列になることを用いて無限等比級数で和を求めている", 3), ("（3）往復時間が $e$ 倍の等比数列になることを用いて和を求めている", 3)], d=5, p=8, lines=10,
                ap="1回はね返ると速さ $e$ 倍 → 上がる高さ $e^2$ 倍、上がって戻る時間 $\\dfrac{2v}{g}$ も $e$ 倍。公比が1未満なので無限等比級数が収束する。",
                steps=["（1）$v_n=e^nv_0$。", f"（2）$n$ 回目のはね返り後に上下する道のり $2e^{{2n}}h$。和 $h+\\dfrac{{2e^2h}}{{1-e^2}}$。", f"（3）$n$ 回目のはね返り後の往復時間 $2e^nt_0$（$t_0={t(t0, 3)}\\,\\mathrm{{s}}$）。和 $t_0+\\dfrac{{2et_0}}{{1-e}}$。"],
                alt=["（2）は「失われる力学的エネルギー」で考えることはできない（エネルギーの総量 $mgh$ からは道のりが決まらない）ことを確認し、等比級数による方法の必要性を説明してもよい。",
                     "（3）は $e\\to1$ で時間が無限大、$e\\to0$ で $t_0$ になることで式を確かめる。"],
                pc=[("（1）", 2), ("（2）", 3), ("（3）", 3)], pit=["2回目以降の道のりを往復の2倍にし忘れる。", "時間を高さと同じ公比 $e^2$ で計算する。"],
                chk=(f"sqrt(2*{P(h)}/9.8)*(1+{P(e)})/(1-{P(e)})", str(sp.nsimplify(Ttot)), None, "intermediate"))


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(stem, wrong, step, etype, tempt, fix, ans, expl, steps, ap, alt, pit, chk=None, d=3, **kw):
    return desc(f"{stem}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい答えを求めなさい。", ans, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい解答を途中式とともに示している", 3), ("最終的な答えが正しい", 1)], d=d, p=6, lines=6,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい途中式", 3), ("正しい答え", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix), chk=chk, **kw)


@gen("error_correction", 3, ["common_error", "condition_check"])
def err_momentum(r):
    kind = r.choice(["bounce", "kecons", "esign"])
    if kind == "bounce":
        ms = r.choice(["0.10", "0.20", "0.50"])
        vs, ws = r.choice([("10", "6.0"), ("20", "10"), ("15", "5.0"), ("8.0", "4.0"), ("12", "8.0")])
        m, v, w = Q(ms), Q(vs), Q(ws)
        I = m * (v + w)
        return err_item(f"質量 {ms} kg のボールが、速さ {vs} m/s で壁に垂直に当たり、速さ {ws} m/s で逆向きにはね返った。ボールが壁から受けた力積の大きさを求めなさい。",
                        f"力積＝運動量の変化＝${ms}\\times{ws}-{ms}\\times{vs}={dec(m * w - m * v)}$。大きさは ${dec(abs(m * w - m * v))}\\,\\mathrm{{N\\cdot s}}$",
                        "衝突前後の速度を、向きを考えずに速さのまま代入した部分", "sign",
                        "運動量の変化を「後−前」と覚えているが、速度が向きをもつ量であることを意識せず、速さの数値をそのまま使っている。",
                        f"はね返った向きを正とすると、衝突前の速度は $-{vs}$。力積 $={ms}\\times{ws}-{ms}\\times(-{vs})={t(I)}\\,\\mathrm{{N\\cdot s}}$",
                        f"${t(I)}\\,\\mathrm{{N\\cdot s}}$", "運動量・力積はベクトル。逆向きの速度は符号を変えて代入する。",
                        ["正の向き（はね返った向き）を決める。", f"$\\Delta p={ms}\\times{ws}-{ms}\\times(-{vs})={t(I)}\\,\\mathrm{{N\\cdot s}}$。"],
                        "速度・運動量の矢印を図にかき、向きの異なる矢印の差をとる。",
                        ["もし生徒の答えが正しいなら、壁に当たって止まる（$v'=0$）場合より力積が小さくなり、はね返るほうが受ける力積が小さいという不自然な結論になる。"],
                        ["はね返りでは速さの「和」になると確認する。"], chk=(f"{P(m)}*({P(w)}+{P(v)})", str(I), None, "intermediate"), d=2)
    if kind == "kecons":
        m1, m2 = r.sample([1, 2, 3, 4], 2)
        v1 = r.choice([2, 3, 4, 6])
        V = sp.Rational(m1 * v1, m1 + m2)
        Vbad = v1 * sp.sqrt(sp.Rational(m1, m1 + m2))
        return err_item(f"なめらかな水平面上で、速さ {iv(v1)} m/s で進む質量 {iv(m1)} kg の台車が、静止している質量 {iv(m2)} kg の台車に衝突して連結し、一体となって進んだ。一体となった後の速さを求めなさい。",
                        f"エネルギー保存より $\\dfrac12\\times{m1}\\times{v1}^2=\\dfrac12\\times{m1 + m2}\\times V^2$、$V\\fallingdotseq{t(Vbad)}\\,\\mathrm{{m/s}}$",
                        "衝突の前後で運動エネルギーが保存されるとした部分", "condition",
                        "物理基礎で多用した「エネルギー保存」を、適用条件（非保存力がする仕事が 0）を確かめずに衝突に当てはめている。",
                        f"連結する衝突（完全非弾性衝突）では運動エネルギーは保存されない。運動量保存より ${m1}\\times{v1}=({m1}+{m2})V$、$V={t(V)}\\,\\mathrm{{m/s}}$",
                        f"${t(V)}\\,\\mathrm{{m/s}}$", "衝突で必ず使えるのは運動量保存則。運動エネルギーは $e=1$ のときだけ保存される。",
                        [f"運動量保存：${m1}\\times{v1}=({m1}+{m2})V$。", f"$V={t(V)}\\,\\mathrm{{m/s}}$。"],
                        "衝突・分裂では運動量保存、外力が保存力だけの区間では力学的エネルギー保存、と使える条件を確認する。",
                        [f"生徒の速さ {t(Vbad)} m/s で運動量を計算すると $({m1}+{m2})\\times{t(Vbad)}$ となり、衝突前の ${m1 * v1}\\,\\mathrm{{kg\\cdot m/s}}$ より大きく、運動量保存に反する。"],
                        ["連結・合体は運動エネルギーが失われる典型例と覚える。"], chk=(f"Rational({m1}*{v1},{m1}+{m2})", str(V), None, "intermediate"))
    while True:
        m1, m2 = r.sample([1, 2, 3], 2)
        v1 = r.choice([4, 6, 8, 10])
        e = Q(r.choice(["0.20", "0.40", "0.50"]))
        v1p = (m1 - e * m2) * v1 / (m1 + m2)
        v2p = (1 + e) * m1 * v1 / (m1 + m2)
        if v1p < 0 and fin(v1p) and fin(v2p) and is_exact(t(v1p), v1p) and is_exact(t(v2p), v2p):
            break
    bad = (v2p - abs(v1p)) / v1
    return err_item(f"なめらかな水平面上で、右向きに速さ {iv(v1)} m/s で進む球 A が静止している球 B に正面衝突したところ、A は左向きに速さ {t(abs(v1p))} m/s ではね返り、B は右向きに速さ {t(v2p)} m/s で進んだ。反発係数を求めなさい。",
                    f"$e=\\dfrac{{\\text{{B の速さ}}-\\text{{A の速さ}}}}{{\\text{{衝突前の速さ}}}}=\\dfrac{{{dec(v2p)}-{dec(abs(v1p))}}}{{{v1}}}={dec(bad)}$",
                    "A の衝突後の速度を、向き（符号）を考えずに速さで代入した部分", "sign",
                    "反発係数を「速さの差÷速さ」と覚え、衝突後に A が逆向きに動くと速度の符号が変わることを見落としている。",
                    f"右向きを正とすると $v_{{\\mathrm{{A}}}}'=-{dec(abs(v1p))}$。$e=-\\dfrac{{v_{{\\mathrm{{A}}}}'-v_{{\\mathrm{{B}}}}'}}{{v_{{\\mathrm{{A}}}}-v_{{\\mathrm{{B}}}}}}=\\dfrac{{{dec(v2p)}-(-{dec(abs(v1p))})}}{{{v1}}}={t(e)}$",
                    f"${t(e)}$", "反発係数の式には符号つきの速度を代入する。",
                    [f"右向き正：$v_{{\\mathrm{{A}}}}={v1}$、$v_{{\\mathrm{{A}}}}'=-{dec(abs(v1p))}$、$v_{{\\mathrm{{B}}}}'={dec(v2p)}$。", f"$e=\\dfrac{{{dec(v2p)}+{dec(abs(v1p))}}}{{{v1}}}={t(e)}$。"],
                    "離れる速さ（相対速度の大きさ）は、2球が逆向きに動くときは速さの和になる。",
                    [f"求めた $e$ と運動量保存の式から衝突後の速度を計算し直し、問題文の値（A：左向き {dec(abs(v1p))} m/s）が再現されるかを確かめる。"],
                    ["衝突後の向きを図にかいてから式を立てる。"], chk=(f"({P(v2p)}-({P(v1p)}))/{v1}", str(e), None, "intermediate"))


@gen("error_correction", 3, ["common_error", "concept"])
def err_circular(r):
    kind = r.choice(["rpm", "top", "vlin"])
    if kind == "rpm":
        n = r.choice([30, 60, 90, 120])
        rs = r.choice(["0.10", "0.20", "0.50"])
        rr = Q(rs)
        w = 2 * sp.pi * n / 60
        v = rr * w
        bad = rr * sp.Rational(n, 60)
        return err_item(f"半径 {rs} m の円板が、1分間に {n} 回の割合で一様に回転している。円板の縁の点の速さを求めなさい。",
                        f"1秒あたりの回転数は $\\dfrac{{{n}}}{{60}}={dec(sp.Rational(n, 60))}$ なので $\\omega={dec(sp.Rational(n, 60))}\\,\\mathrm{{rad/s}}$。$v=r\\omega={rs}\\times{dec(sp.Rational(n, 60))}={dec(bad)}\\,\\mathrm{{m/s}}$",
                        "回転数をそのまま角速度とした部分", "formula",
                        "回転数（回/s）と角速度（rad/s）の単位の違いを意識せず、1回転が $2\\pi$ rad であることを忘れている。",
                        f"$\\omega=2\\pi\\times\\dfrac{{{n}}}{{60}}\\fallingdotseq{t(w)}\\,\\mathrm{{rad/s}}$。$v=r\\omega\\fallingdotseq{t(v)}\\,\\mathrm{{m/s}}$",
                        f"${t(v)}\\,\\mathrm{{m/s}}$", "1回転は $2\\pi$ rad。$\\omega=2\\pi n$。",
                        [f"$n={dec(sp.Rational(n, 60))}\\,\\text{{回/s}}$。", f"$\\omega=2\\pi n\\fallingdotseq{t(w)}\\,\\mathrm{{rad/s}}$、$v=r\\omega\\fallingdotseq{t(v)}\\,\\mathrm{{m/s}}$。"],
                        "単位（回/s と rad/s）を書いて計算する。",
                        [f"1秒間に縁の点が進む距離は「円周 $2\\pi r$ × 回転数」なので、$2\\pi\\times{rs}\\times{dec(sp.Rational(n, 60))}$ と直接計算して確かめる。"],
                        ["回転数・周期・角速度の関係を整理しておく。"], chk=(f"{P(rr)}*2*pi*{n}/60", str(sp.nsimplify(v)), None, "intermediate"), d=2)
    if kind == "top":
        ms = r.choice(["0.10", "0.20", "0.50"])
        Ls = r.choice(["0.50", "1.0"])
        vs = r.choice(["4.0", "5.0", "6.0"])
        m, L, v = Q(ms), Q(Ls), Q(vs)
        S = m * v ** 2 / L - m * G
        bad = m * v ** 2 / L + m * G
        return err_item(f"長さ {Ls} m の軽い糸に質量 {ms} kg の小球をつけ、鉛直面内で円運動させた。小球が最高点を速さ {vs} m/s で通過するときの糸の張力の大きさを求めなさい。" + GS,
                        f"張力は向心力と重力を支えるので $S=m\\dfrac{{v^2}}{{L}}+mg={ms}\\times\\dfrac{{{vs}^2}}{{{Ls}}}+{ms}\\times9.8\\fallingdotseq{t(bad)}\\,\\mathrm{{N}}$",
                        "最高点で張力を「向心力＋重力」とした部分", "concept",
                        "最下点での式 $S=mg+m\\dfrac{v^2}{L}$ をそのまま最高点に当てはめ、最高点では重力も中心を向くことを考えていない。",
                        f"最高点では張力も重力も中心（下）向き。$m\\dfrac{{v^2}}{{L}}=S+mg$ より $S=m\\dfrac{{v^2}}{{L}}-mg\\fallingdotseq{t(S)}\\,\\mathrm{{N}}$",
                        f"${t(S)}\\,\\mathrm{{N}}$", "円運動の運動方程式は「中心向きの力の和＝$m\\dfrac{v^2}{r}$」。力の向きを図で確認する。",
                        ["最高点で中心向き（下向き）を正とする。", f"$m\\dfrac{{v^2}}{{L}}=S+mg$、$S={ms}\\times\\dfrac{{{vs}^2}}{{{Ls}}}-{ms}\\times9.8\\fallingdotseq{t(S)}\\,\\mathrm{{N}}$。"],
                        "最高点・最下点それぞれで、力の矢印と中心の位置を図にかいてから式を立てる。",
                        ["速さを $\\sqrt{gL}$ まで小さくすると張力は 0 になるはず（糸がたるむ直前）。生徒の式では張力が $2mg$ となり、この事実と合わない。"],
                        ["「向心力」を独立した力として加えない。"], chk=(f"{P(m)}*{P(v)}**2/{P(L)}-{P(m)}*9.8", str(S), None, "intermediate"))
    rs = r.choice(["0.50", "2.0", "4.0", "5.0"])
    vs = r.choice(["2.0", "4.0", "6.0", "10"])
    ms = r.choice(["0.20", "1.0", "2.0"])
    rr, v, m = Q(rs), Q(vs), Q(ms)
    F = m * v ** 2 / rr
    return err_item(f"質量 {ms} kg の物体が半径 {rs} m の円周上を速さ {vs} m/s で等速円運動している。物体にはたらく向心力の大きさを求めなさい。",
                    f"$F=m\\dfrac{{v}}{{r}}={ms}\\times\\dfrac{{{vs}}}{{{rs}}}={t(m * v / rr)}\\,\\mathrm{{N}}$",
                    "向心加速度を $\\dfrac{v}{r}$ とした部分", "formula",
                    "$v=r\\omega$ の $\\omega=\\dfrac{v}{r}$ と向心加速度 $\\dfrac{v^2}{r}$ を混同している。",
                    f"向心加速度は $\\dfrac{{v^2}}{{r}}$。$F=m\\dfrac{{v^2}}{{r}}={ms}\\times\\dfrac{{{vs}^2}}{{{rs}}}={t(F)}\\,\\mathrm{{N}}$",
                    f"${t(F)}\\,\\mathrm{{N}}$", "$a=r\\omega^2=\\dfrac{v^2}{r}$。",
                    [f"$a=\\dfrac{{v^2}}{{r}}=\\dfrac{{{vs}^2}}{{{rs}}}={t(v ** 2 / rr)}\\,\\mathrm{{m/s^2}}$。", f"$F=ma={t(F)}\\,\\mathrm{{N}}$。"],
                    "単位で確かめる：$\\dfrac{v}{r}$ の単位は $\\mathrm{s^{-1}}$ で、加速度（$\\mathrm{m/s^2}$）にならない。",
                    ["$\\omega=\\dfrac{v}{r}$ を求めてから $a=r\\omega^2$ で計算し、同じ値になるかを確かめる。"],
                    ["公式は単位とともに覚える。"], chk=(f"{P(m)}*{P(v)}**2/{P(rr)}", str(F), None, "intermediate"), d=2)


@gen("error_correction", 2, ["common_error", "concept"])
def err_shm(r):
    kind = r.choice(["amp", "inv", "pmass"])
    if kind == "amp":
        Ts = r.choice(["0.50", "0.80", "1.2", "2.0"])
        k = r.choice([2, 3])
        return err_item(f"ばね振り子を振幅 5.0 cm で振動させたところ、周期は {Ts} s であった。同じばね振り子を振幅 {iv(5 * k)} cm で振動させたときの周期を求めなさい。",
                        f"振幅が {k} 倍になると、往復する距離も {k} 倍になるので、周期も {k} 倍の ${dec(Q(Ts) * k)}\\,\\mathrm{{s}}$ になる",
                        "周期が振幅に比例するとした部分", "concept",
                        "「長い距離を動くほど時間がかかる」という直観から、振幅が大きいと速さも大きくなることを考えていない。",
                        f"$T=2\\pi\\sqrt{{\\dfrac{{m}}{{k}}}}$ は振幅を含まない。周期は変わらず {Ts} s",
                        f"${Ts}\\,\\mathrm{{s}}$", "単振動の周期は振幅によらない（等時性）。振幅が大きいと最大の速さ $A\\omega$ も大きくなる。",
                        ["周期の式 $T=2\\pi\\sqrt{\\dfrac{m}{k}}$ を確認する。", f"$m,\\ k$ は変わらないので $T={Ts}\\,\\mathrm{{s}}$。"],
                        "式に含まれる量だけが周期を変える、と確認する。",
                        [f"振幅が {k} 倍になると最大の速さ $A\\omega$ も {k} 倍になり、距離と速さの増加が打ち消し合うので時間は同じ、と説明できる。"],
                        ["周期の式に何が含まれるかを確認する。"], chk=(f"{P(Q(Ts))}", str(Q(Ts)), None, "intermediate"), d=2)
    if kind == "inv":
        ms, ks = r.choice([("0.40", "10"), ("0.10", "40"), ("2.5", "10"), ("0.90", "10"), ("1.6", "40")])
        m, k = Q(ms), Q(ks)
        T = 2 * sp.pi * sp.sqrt(m / k)
        bad = 2 * sp.pi * sp.sqrt(k / m)
        return err_item(f"ばね定数 {ks} N/m の軽いばねに質量 {ms} kg のおもりをつけて単振動させた。周期を求めなさい。",
                        f"$T=2\\pi\\sqrt{{\\dfrac{{k}}{{m}}}}=2\\pi\\sqrt{{\\dfrac{{{ks}}}{{{ms}}}}}\\fallingdotseq{t(bad)}\\,\\mathrm{{s}}$",
                        "$\\sqrt{\\dfrac{k}{m}}$ とした部分", "formula",
                        "角振動数 $\\omega=\\sqrt{\\dfrac{k}{m}}$ と周期の式を混同し、分母と分子を逆にしている。",
                        f"$T=\\dfrac{{2\\pi}}{{\\omega}}=2\\pi\\sqrt{{\\dfrac{{m}}{{k}}}}=2\\pi\\sqrt{{\\dfrac{{{ms}}}{{{ks}}}}}\\fallingdotseq{t(T)}\\,\\mathrm{{s}}$",
                        f"${t(T)}\\,\\mathrm{{s}}$", "重いおもりほど動かしにくく周期が長いので、$m$ は分子。",
                        [f"$\\omega=\\sqrt{{\\dfrac{{k}}{{m}}}}$。", f"$T=\\dfrac{{2\\pi}}{{\\omega}}=2\\pi\\sqrt{{\\dfrac{{m}}{{k}}}}\\fallingdotseq{t(T)}\\,\\mathrm{{s}}$。"],
                        "次元で確かめる：$\\sqrt{\\dfrac{k}{m}}$ の単位は $\\mathrm{s^{-1}}$ で、時間にならない。",
                        ["おもりを重くすると振動がゆっくりになる、という経験と式が合うかどうかで確かめる。"], ["$\\omega$ と $T$ の関係を必ず経由する。"],
                        chk=(f"2*pi*sqrt({P(m)}/{P(k)})", str(sp.nsimplify(T)), None, "intermediate"))
    Ls = r.choice(["0.80", "1.2", "2.5", "1.6"])
    L = Q(Ls)
    T = 2 * sp.pi * sp.sqrt(L / G)
    return err_item(f"長さ {Ls} m の糸に質量 100 g のおもりをつけた単振り子と、同じ長さの糸に質量 400 g のおもりをつけた単振り子がある。それぞれの周期を求めなさい（振れ角は小さいとする）。" + GS,
                    "おもりが重いほど重力が大きく、速く引き戻されるので、400 g の振り子の周期は 100 g の振り子の周期の $\\dfrac12$ になる",
                    "周期がおもりの質量によるとした部分", "concept",
                    "重力（復元力）が質量に比例することだけに注目し、質量が大きいと加速しにくい（慣性が大きい）ことを考えていない。",
                    f"$T=2\\pi\\sqrt{{\\dfrac{{L}}{{g}}}}$ は質量を含まない。どちらも $T=2\\pi\\sqrt{{\\dfrac{{{Ls}}}{{9.8}}}}\\fallingdotseq{t(T)}\\,\\mathrm{{s}}$",
                    f"どちらも ${t(T)}\\,\\mathrm{{s}}$", "単振り子の復元力 $\\dfrac{mg}{L}x$ の $m$ と運動方程式の $m$ が約分される。",
                    ["運動方程式：$ma=-\\dfrac{mg}{L}x$。", f"$\\omega=\\sqrt{{\\dfrac{{g}}{{L}}}}$、$T\\fallingdotseq{t(T)}\\,\\mathrm{{s}}$（質量によらない）。"],
                    "運動方程式を立て、質量が約分されるかどうかを確かめる。",
                    ["自由落下で重い物も軽い物も同じ加速度で落ちることと同じ理由である、と結びつけて確かめる。"], ["素朴な直観より運動方程式を優先する。"],
                    chk=(f"2*pi*sqrt({P(L)}/9.8)", str(sp.nsimplify(T)), None, "intermediate"))


@gen("error_correction", 2, ["common_error", "condition_check"])
def err_gravity(r):
    kind = r.choice(["height", "inv", "kepler"])
    if kind == "height":
        g2 = G / 4
        return err_item("地表からの高さが地球の半径 $R$ に等しい地点での重力加速度の大きさを求めなさい。地表での重力加速度の大きさを $9.8\\,\\mathrm{m/s^2}$ とし、地球の自転の影響は無視する。",
                        "重力加速度は距離の2乗に反比例するので $g'=g\\left(\\dfrac{R}{h}\\right)^2$。高さ $h=R$ を代入すると $g'=g=9.8\\,\\mathrm{m/s^2}$",
                        "地表からの高さを距離 $r$ とした部分", "concept",
                        "万有引力の式の $r$ を「地表からの高さ」と取り違えている。地球全体の質量が中心に集まっているとみなせることを使っていない。",
                        "$r$ は地球の中心からの距離。地表では $r=R$、高さ $R$ の地点では $r=2R$。$g'=g\\left(\\dfrac{R}{2R}\\right)^2=\\dfrac{9.8}{4}\\fallingdotseq2.5\\,\\mathrm{m/s^2}$",
                        f"${t(g2, 2)}\\,\\mathrm{{m/s^2}}$（有効数字2桁）", "万有引力の $r$ は中心間の距離。",
                        ["$g'=\\dfrac{GM}{r^2}$、$r=2R$。", "$g'=\\dfrac{gR^2}{(2R)^2}=\\dfrac{g}{4}\\fallingdotseq2.5\\,\\mathrm{m/s^2}$。"],
                        "図に地球の中心をかき、距離を中心から測る。",
                        ["高さ 0（地表）で $g$ に戻ることを確かめる：$r=R$ を代入すると $g'=g$。"], ["$r=R+h$ と必ず書く。"],
                        chk=("9.8*(1/2)**2", str(g2), None, "intermediate"), d=2)
    if kind == "inv":
        k = r.choice([2, 3, 4])
        g2 = G / k ** 2
        return err_item(f"地球の中心からの距離が地球の半径の {k} 倍の地点での重力加速度の大きさを、有効数字2桁で求めなさい。地表での重力加速度の大きさを $9.8\\,\\mathrm{{m/s^2}}$ とし、地球の自転の影響は無視する。",
                        f"距離が {k} 倍になるので、重力加速度は $\\dfrac{{1}}{{{k}}}$ 倍の $\\dfrac{{9.8}}{{{k}}}\\fallingdotseq{t(G / k, 2)}\\,\\mathrm{{m/s^2}}$",
                        "距離に反比例するとした部分", "formula",
                        "「距離が大きいほど弱くなる」ことは覚えているが、逆2乗則（距離の2乗に反比例）であることを忘れている。",
                        f"$g'=\\dfrac{{GM}}{{r^2}}$ より距離の2乗に反比例。$g'=\\dfrac{{9.8}}{{{k}^2}}\\fallingdotseq{t(g2, 2)}\\,\\mathrm{{m/s^2}}$",
                        f"${t(g2, 2)}\\,\\mathrm{{m/s^2}}$", "万有引力は距離の2乗に反比例する。",
                        [f"$\\dfrac{{g'}}{{g}}=\\left(\\dfrac{{R}}{{{k}R}}\\right)^2=\\dfrac{{1}}{{{k * k}}}$。", f"$g'\\fallingdotseq{t(g2, 2)}\\,\\mathrm{{m/s^2}}$。"],
                        "法則の形 $F=G\\dfrac{Mm}{r^2}$ を書いてから比を計算する。",
                        ["光の明るさが光源からの距離の2乗に反比例するのと同じく、球面に広がる量は距離の2乗で薄まる、と結びつけて覚える。"], ["比を求めるときも式を書く。"],
                        chk=(f"9.8/{k}**2", str(g2), None, "intermediate"), d=2)
    a = r.choice([4, 9])
    T = sp.Rational(a) ** sp.Rational(3, 2)
    return err_item(f"太陽のまわりを円軌道で公転する惑星 X の軌道半径は、地球の軌道半径の {a} 倍である。X の公転周期は何年か。地球の公転周期を1年とする。",
                    f"ケプラーの第3法則より、周期は軌道半径に比例するので {a} 年",
                    "周期が軌道半径に比例するとした部分", "formula",
                    "「軌道が大きいほど周期が長い」という定性的な関係だけを覚えていて、2乗・3乗の関係を使っていない。",
                    f"$T^2\\propto r^3$ より $T=\\left({a}\\right)^{{\\frac{{3}}{{2}}}}={T}$ 年",
                    f"${T}$ 年", "ケプラーの第3法則は「周期の2乗が半径の3乗に比例」。",
                    [f"$\\left(\\dfrac{{T}}{{1}}\\right)^2=\\left(\\dfrac{{{a}r}}{{r}}\\right)^3={a ** 3}$。", f"$T=\\sqrt{{{a ** 3}}}={T}$ 年。"],
                    "法則を式（$\\dfrac{T^2}{r^3}=$ 一定）で書いてから代入する。",
                    [f"軌道が大きいと円周が {a} 倍になるだけでなく、速さも $\\dfrac{{1}}{{\\sqrt{{{a}}}}}$ 倍に遅くなるので、周期は $\\dfrac{{{a}}}{{1/\\sqrt{{{a}}}}}={T}$ 倍になる、と別の道筋で確かめる。"],
                    ["2乗・3乗の関係を言葉だけで覚えない。"], chk=(f"{a}**Rational(3,2)", str(T), None, "intermediate"), d=2)


GENERATORS = [momentum_basic, collision_basic, circular_basic, shm_basic, gravity_basic, concept_mc,
              collision_1d, split_recoil, momentum_2d, circular_apps, shm_apps, orbit_apps,
              derive_c, ballistic_c, loop_c, bounce_c,
              err_momentum, err_circular, err_shm, err_gravity]
