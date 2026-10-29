"""単元パック：物理 波動（正弦波の式、ドップラー効果、波の干渉、光の干渉と回折）。"""
import math
from decimal import ROUND_HALF_UP, Decimal

import sympy as sp

from banks._common import desc, figure, mc, num, plane
from hs_pack_lib import board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem, tp

UNIT_ID = "HS-PHY-U03"

V = 340
VS = "音の速さを $340\\,\\mathrm{m/s}$ とする。"


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
    """整数で厳密に表せる 10000 未満の値はそのまま、それ以外は有効数字 n 桁で答えにする。"""
    raw = sp.nsimplify(x).is_integer and (unit in ("個", "次", "回", "度") or 10 <= abs(x) < 10000)
    if n is None and raw:
        n = max(2, len(str(abs(int(x)))))
    n = n or bestn(x)
    s = str(int(x)) if (raw and n == max(2, len(str(abs(int(x)))))) else sig(x, n)
    exact = is_exact(s, x)
    if not exact and "有効数字" not in stem:
        stem += f"有効数字{n}桁で答えなさい。"
    ans = s if "times" not in s else f"${s}$"
    xs = str(sp.sympify(x))
    chk = (expr, xs) if exact else (expr, xs, None, "intermediate")
    return num(stem, ans, e, unit=unit, chk=chk, **kw)


def t(x, n=None):
    if n is None and sp.nsimplify(x).is_integer and 10 <= abs(x) < 10000:
        return str(int(x))
    return sig(x, n or bestn(x))


def P(x):
    return f"({sp.nsimplify(x)})"


def iv(n):
    return f"{n}.0" if abs(n) < 10 else f"{n}"


SIN = {30: sp.Rational(1, 2), 45: sp.sqrt(2) / 2, 60: sp.sqrt(3) / 2}


# ----------------------------------------------------------------------
# 図
# ----------------------------------------------------------------------

def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="serif" font-size="12">'
            '<defs><marker id="ah" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#000"/></marker></defs>'
            f'{body}</svg>')


def wave_svg(lam, A, pts=()):
    L = 2 * lam
    unit = max(14, min(30, int(260 / (L + 1))))
    return plane((0, L + 0.6), (-A - 1, A + 1), unit=unit, grid=True, ticks=True,
                 curves=[(lambda x: A * math.sin(2 * math.pi * x / lam) if 0 <= x <= L else float("nan"), "")],
                 points=list(pts), xl="x[m]", yl="y[cm]")


def young_svg():
    body = '<line x1="30" y1="20" x2="30" y2="180" stroke="#000" stroke-width="2"/>'
    body += '<rect x="28" y="70" width="4" height="10" fill="#fff"/><rect x="28" y="120" width="4" height="10" fill="#fff"/>'
    body += '<text x="8" y="80">S₁</text><text x="8" y="130">S₂</text>'
    body += '<line x1="250" y1="10" x2="250" y2="190" stroke="#000" stroke-width="2"/><text x="256" y="190">スクリーン</text>'
    body += '<line x1="30" y1="75" x2="250" y2="60" stroke="#1f4e79"/><line x1="30" y1="125" x2="250" y2="60" stroke="#1f4e79"/>'
    body += '<circle cx="250" cy="60" r="3" fill="#000"/><text x="256" y="58">P</text>'
    body += '<line x1="30" y1="100" x2="250" y2="100" stroke="#000" stroke-dasharray="4 3"/><text x="256" y="104">O</text>'
    body += '<text x="130" y="116">L</text><text x="36" y="104">d</text><text x="236" y="84">x</text>'
    body += '<line x1="30" y1="75" x2="58" y2="129" stroke="#c0392b" stroke-dasharray="2 2"/><text x="52" y="146" fill="#c0392b">d sinθ</text>'
    return svg(320, 200, body)


def doppler_svg(lab_s="v", lab_o=""):
    body = '<line x1="10" y1="80" x2="310" y2="80" stroke="#000"/>'
    body += '<circle cx="70" cy="60" r="12" fill="#f3d9c6" stroke="#000"/><text x="62" y="64">S</text><text x="50" y="100">音源</text>'
    body += '<rect x="235" y="45" width="24" height="30" fill="#cfdcec" stroke="#000"/><text x="241" y="64">O</text><text x="228" y="100">観測者</text>'
    for k in range(4):
        body += f'<path d="M {100 + 22 * k} 40 Q {110 + 22 * k} 60 {100 + 22 * k} 80" fill="none" stroke="#888"/>'
    if lab_s:
        body += f'<line x1="60" y1="30" x2="100" y2="30" stroke="#000" stroke-width="1.5" marker-end="url(#ah)"/><text x="70" y="24">{lab_s}</text>'
    if lab_o:
        body += f'<line x1="260" y1="30" x2="220" y2="30" stroke="#000" stroke-width="1.5" marker-end="url(#ah)"/><text x="232" y="24">{lab_o}</text>'
    return svg(320, 110, body)


def film_svg():
    body = '<rect x="20" y="70" width="260" height="40" fill="#e8f1f8" stroke="#000"/><text x="230" y="95">膜（n）</text>'
    body += '<text x="200" y="60">空気</text><text x="200" y="130">空気またはガラス</text>'
    body += '<line x1="60" y1="20" x2="90" y2="70" stroke="#c0392b" stroke-width="1.3"/><line x1="90" y1="70" x2="120" y2="20" stroke="#c0392b" stroke-width="1.3"/>'
    body += '<line x1="90" y1="70" x2="110" y2="110" stroke="#1f4e79" stroke-width="1.3"/><line x1="110" y1="110" x2="130" y2="70" stroke="#1f4e79" stroke-width="1.3"/>'
    body += '<line x1="130" y1="70" x2="160" y2="20" stroke="#1f4e79" stroke-width="1.3"/><text x="40" y="20">入射光</text><text x="150" y="20">反射光①②</text>'
    body += '<text x="16" y="94">d</text>'
    return svg(300, 140, body)


# ======================================================================
# 授業プリント
# ======================================================================

def _wave_eq_fig():
    return plane((0, 8.6), (-2.6, 2.6), unit=28, grid=True, ticks=True,
                 curves=[(lambda x: 2 * math.sin(2 * math.pi * x / 4) if 0 <= x <= 8 else float("nan"), "")],
                 labels=[(0.5, 2.3, "t=0 の波形"), (5.6, -2.3, "→ 速さ v")], xl="x", yl="y")


LESSON = lesson(
    goals=["原点の振動 $y=A\\sin\\dfrac{2\\pi}{T}t$ から、$x$ 軸の正の向きに進む正弦波の式 $y=A\\sin2\\pi\\left(\\dfrac{t}{T}-\\dfrac{x}{\\lambda}\\right)$ を導き、式から波の要素を読み取れる。",
           "音源・観測者が動く場合のドップラー効果の式を、波長と波の速さの変化から導いて使える。",
           "2つの波源からの経路差と位相の関係から、干渉の条件（強め合い・弱め合い）を判断できる。",
           "ヤングの実験・回折格子・薄膜の干渉で、明線の条件を導き、波長や間隔を求められる。"],
    duration=100,
    readiness=["波の基本式 $v=f\\lambda$、$f=\\dfrac{1}{T}$ と、横波・縦波・重ね合わせの原理を説明できる（物理基礎）。",
               "弧度法と三角関数 $\\sin\\theta$ のグラフ、加法定理をかける（数学Ⅱ）。",
               "固定端反射で位相が $\\pi$ ずれる（山が谷になる）ことを説明できる（物理基礎）。"],
    flow=[("導入：救急車のサイレンとシャボン玉の色", 5, "ドップラー効果と光の干渉を、身近な現象として提示する"),
          ("正弦波の式", 20, "原点の単振動から波の式を導く、式から振幅・周期・波長・速さを読む（例題1）"),
          ("ドップラー効果", 25, "音源が動く場合（波長が変わる）・観測者が動く場合（相対速度が変わる）の導出、一般式（例題2）"),
          ("波の干渉", 15, "経路差と強め合い・弱め合いの条件、水面波の干渉"),
          ("光の干渉と回折", 25, "ヤングの実験（例題3）、回折格子、薄膜の干渉と反射での位相の変化"),
          ("まとめ", 10, "干渉の条件を「経路差（光路差）＋反射による位相の変化」で整理し、課題を指示")],
    sections=[
        intro("in1", "波の「式」と「重なり」で現象を予言する",
              "近づいてくる救急車のサイレンは高く、遠ざかると低く聞こえる。シャボン玉や水面の油膜には虹色の模様が見える。どちらも波の性質で説明できる。この単元では、波を時刻と位置の関数として式で表し、波源や観測者が動くときの振動数の変化（ドップラー効果）や、2つの波が重なるときの強め合い・弱め合い（干渉）を数量的に扱う。光の干渉や回折は、光が波であることの決定的な証拠でもある。",
              bullets=["正弦波の式 $y=A\\sin2\\pi\\left(\\dfrac{t}{T}-\\dfrac{x}{\\lambda}\\right)$ は、どの位置の媒質がいつどれだけ変位しているかを一つの式で表す。",
                       "干渉は「2つの波がどれだけずれて届くか（経路差）」で決まる。"],
              points=[tp("救急車が通り過ぎる音（録音）を聞かせ、通過の前後で音の高さがどう変わるかを確認させる。",
                         ask="救急車の運転手には、サイレンの高さが変わって聞こえるだろうか。", expect="変わらない。音源と観測者の相対的な運動が原因であると気づかせる。",
                         timing="授業の冒頭")]),
        definition("df1", "正弦波の式",
                   "原点 O の媒質が $y=A\\sin\\dfrac{2\\pi}{T}t$ で単振動し、その振動が速さ $v$ で $x$ 軸の正の向きに伝わるとき、位置 $x$ の媒質は原点より時間 $\\dfrac{x}{v}$ だけ遅れて同じ振動をする。",
                   formula="$$y=A\\sin\\dfrac{2\\pi}{T}\\left(t-\\dfrac{x}{v}\\right)=A\\sin2\\pi\\left(\\dfrac{t}{T}-\\dfrac{x}{\\lambda}\\right)$$",
                   conditions=["$v=\\dfrac{\\lambda}{T}$ を用いて書きかえた。$x$ 軸の負の向きに進む波では $-\\dfrac{x}{\\lambda}$ が $+\\dfrac{x}{\\lambda}$ になる。",
                               "$2\\pi\\left(\\dfrac{t}{T}-\\dfrac{x}{\\lambda}\\right)$ を位相という。位相が $2\\pi$ の整数倍だけ異なる2点は同じ振動状態（同位相）にある。",
                               "ある時刻 $t$ を固定すると $y$−$x$ グラフ（波形）、ある位置 $x$ を固定すると $y$−$t$ グラフ（その点の振動）になる。",
                               "距離 $\\Delta x$ 離れた2点の位相差は $2\\pi\\dfrac{\\Delta x}{\\lambda}$。半波長離れた2点は逆位相。"],
                   figure=figure("時刻 t=0 の正弦波の波形（y−x グラフ）。波は x 軸の正の向きに速さ v で進む", _wave_eq_fig(), caption="波形は時間とともに平行移動する"),
                   points=[tp("「位置 $x$ の点は、原点の $\\dfrac{x}{v}$ 秒前の振動をまねる」ことを、ロープの波の動画をコマ送りして確かめさせる。",
                              ask="原点から1波長離れた点の振動は、原点の振動と比べてどうなっているか。", expect="1周期遅れているので、同じ振動（同位相）。"),
                           tp("波形のグラフで、媒質の各点の速度の向きを「少し後の波形」をかいて判断させる。",
                              caution="横波の媒質が波の進む向きに動くと考える誤りが多い。")]),
        theorem("th1", "ドップラー効果",
                "$$f'=\\dfrac{V-u}{V-v}f$$",
                ["$V$：音の速さ、$f$：音源の振動数、$v$：音源の速度、$u$：観測者の速度。速度は「音源から観測者へ向かう向き」を正とする。",
                 "音源が観測者に近づく（$v>0$）と波長が短くなり高く聞こえる。観測者が音源に近づく（$u<0$）と、単位時間に受け取る波の数が増え高く聞こえる。",
                 "風がある場合は、音の速さ $V$ を風の速度だけ変える（風下向きに $V+w$）。音源と観測者がともに静止していれば、風があっても振動数は変わらない。",
                 "動く反射板で反射する音は、反射板をまず「観測者」、次に「音源」とみなして2段階で考える。"],
                body="音源が動くと空気中の波長が変わり、観測者が動くと観測者に対する音の速さが変わる。どちらも「音の速さ・波長・振動数」の関係 $V=f\\lambda$ に立ち返って導く。",
                proof=["音源が速さ $v$ で観測者に向かって動くとき、音源は1秒間に $f$ 個の波を出す。その間に先頭の波は $V$、音源は $v$ 進むので、$f$ 個の波は長さ $V-v$ の中に詰まる。",
                       "前方の波長は $\\lambda'=\\dfrac{V-v}{f}$。静止した観測者が聞く振動数は $f'=\\dfrac{V}{\\lambda'}=\\dfrac{V}{V-v}f$。",
                       "観測者が速さ $u$ で音源から遠ざかるとき（正の向き）、観測者に対する音の速さは $V-u$ になる。波長は $\\lambda'$ のままなので $f'=\\dfrac{V-u}{\\lambda'}=\\dfrac{V-u}{V-v}f$。"],
                figure=figure("左の音源 S が右向きに速さ v で動き、右の観測者 O に向かって音を出している", doppler_svg()),
                points=[tp("音源が動く場合と観測者が動く場合で、変化するもの（波長か、相対的な音の速さか）が違うことを表にまとめさせる。", timing="導出の直後",
                           ask="音源が近づく場合と、観測者が同じ速さで近づく場合とで、聞こえる振動数は等しいか。", expect="等しくない（式の形が違う）。")]),
        definition("df2", "波の干渉の条件",
                   "同じ振動数・同じ位相で振動する2つの波源 $\\mathrm{S_1}$、$\\mathrm{S_2}$ から出た波が点 P で重なるとき、経路差 $|\\mathrm{S_1P}-\\mathrm{S_2P}|$ によって強め合うか弱め合うかが決まる。",
                   formula="$$|\\mathrm{S_1P}-\\mathrm{S_2P}|=m\\lambda\\ \\text{（強め合う）},\\qquad |\\mathrm{S_1P}-\\mathrm{S_2P}|=\\left(m+\\dfrac12\\right)\\lambda\\ \\text{（弱め合う）}\\quad(m=0,1,2,\\cdots)$$",
                   conditions=["2つの波源が逆位相で振動する場合は、強め合いと弱め合いの条件が入れかわる。",
                               "光が屈折率 $n$ の媒質中を距離 $l$ 進むとき、真空中に換算した距離 $nl$ を光学距離という。経路差の代わりに光学距離の差（光路差）を用いる。",
                               "光が屈折率の小さい媒質から大きい媒質との境界で反射するとき、位相が $\\pi$ ずれる（半波長ずれたのと同じ）。大きい媒質から小さい媒質への反射では位相は変わらない。",
                               "水面波の干渉では、強め合う点を連ねた線（腹線）と弱め合う点を連ねた線（節線）が交互に並ぶ双曲線になる。"],
                   points=[tp("「経路差が半波長の奇数倍なら、山と谷が出会う」ことを、2つの円形波の図に山（実線）・谷（破線）をかき込んで確かめさせる。",
                              ask="2つの波源の垂直二等分線上の点は、強め合うか弱め合うか。", expect="経路差 0 なので強め合う（同位相の波源の場合）。")]),
        theorem("th2", "ヤングの実験と回折格子",
                "$$\\text{ヤング：}\\ \\dfrac{dx}{L}=m\\lambda\\ \\Rightarrow\\ \\Delta x=\\dfrac{L\\lambda}{d},\\qquad \\text{回折格子：}\\ d\\sin\\theta=m\\lambda$$",
                ["ヤングの実験：$d$ は2つのスリットの間隔、$L$ はスリットとスクリーンの距離、$x$ はスクリーン中央からの距離。$L\\gg d,\\ x$ のとき経路差は $\\dfrac{dx}{L}$ と近似できる。",
                 "明線の間隔 $\\Delta x=\\dfrac{L\\lambda}{d}$ は等間隔。波長が長い（赤い）光ほど間隔が広い。",
                 "回折格子：$d$ は格子定数（すじの間隔）。1 mm あたり $N$ 本なら $d=\\dfrac{1}{N}\\,\\mathrm{mm}$。$|\\sin\\theta|\\leqq1$ より、観測できる次数には上限がある。",
                 "光が細いすき間を通ってその後ろに回りこむ現象を回折という。すき間の幅が波長に近いほど回折は目立つ。"],
                body="ヤングの実験は1800年代初めに、光が波であることを示した実験である。回折格子では多数のスリットからの光が強め合う方向が鋭く決まるので、波長の精密な測定や分光に使われる。",
                proof=["スリット $\\mathrm{S_1}$、$\\mathrm{S_2}$ から点 P への経路差は、P の方向と中心線のなす角を $\\theta$ とすると $d\\sin\\theta$（$L\\gg d$ のとき、2つの経路はほぼ平行）。",
                       "$\\theta$ が小さいとき $\\sin\\theta\\fallingdotseq\\tan\\theta=\\dfrac{x}{L}$ なので、経路差は $\\dfrac{dx}{L}$。",
                       "明線の条件 $\\dfrac{dx}{L}=m\\lambda$ より $x_m=\\dfrac{mL\\lambda}{d}$。隣り合う明線の間隔は $\\Delta x=x_{m+1}-x_m=\\dfrac{L\\lambda}{d}$。"],
                figure=figure("ヤングの実験。間隔 d の2つのスリット S₁、S₂ と、距離 L 離れたスクリーン上の点 P（中央 O から x）。経路差 d sinθ", young_svg()),
                points=[tp("近似 $\\sin\\theta\\fallingdotseq\\tan\\theta$ が使える理由を、実際の数値（$d=0.2\\,\\mathrm{mm}$、$L=1\\,\\mathrm{m}$、$x=3\\,\\mathrm{mm}$）で角がきわめて小さいことから確かめさせる。")]),
        derivation("dv1", "薄膜の干渉（垂直入射）",
                   ["厚さ $d$、屈折率 $n$ の薄膜に光が垂直に入射する。膜の上面で反射する光①と、下面で反射する光②が重なる。",
                    "②は膜の中を往復するので、光路差は $2nd$。",
                    "空気中の薄膜（シャボン膜）では、①は空気→膜（小→大）の反射で位相が $\\pi$ ずれ、②は膜→空気（大→小）の反射で位相が変わらない。反射による位相のずれは差し引き半波長。",
                    "よって強め合う条件は $2nd=\\left(m+\\dfrac12\\right)\\lambda$、弱め合う条件は $2nd=m\\lambda$。両方の反射で位相がずれる場合（ガラス上の反射防止膜で $n_{\\text{膜}}<n_{\\text{ガラス}}$）は、条件が入れかわる。"],
                   body="白色光を当てると、膜の厚さに応じて強め合う波長が異なるので色づいて見える。シャボン玉の色の模様は膜の厚さの分布を表している。",
                   figure=figure("厚さ d、屈折率 n の薄膜に入射した光が、上面で反射する光①と下面で反射する光②に分かれる", film_svg()),
                   points=[tp("反射による位相の変化を「固定端反射（屈折率が大きい側）・自由端反射（小さい側）」とロープの波の反射に対応させて覚えさせる。",
                              caution="位相の変化を考えずに $2nd=m\\lambda$ を強め合いの条件とする誤りが多い。")]),
        example("ex1", "例題1　正弦波の式",
                "$x$ 軸の正の向きに進む正弦波が $y=0.20\\sin2\\pi\\left(\\dfrac{t}{0.50}-\\dfrac{x}{4.0}\\right)$〔m〕で表される（$t$ は s、$x$ は m）。この波の振幅・周期・波長・速さを求めよ。また、$x=1.0\\,\\mathrm{m}$ の点の、時刻 $t=0$ での変位を求めよ。",
                ["式 $y=A\\sin2\\pi\\left(\\dfrac{t}{T}-\\dfrac{x}{\\lambda}\\right)$ と比べて、$A=0.20\\,\\mathrm{m}$、$T=0.50\\,\\mathrm{s}$、$\\lambda=4.0\\,\\mathrm{m}$。",
                 "$v=\\dfrac{\\lambda}{T}=\\dfrac{4.0}{0.50}=8.0\\,\\mathrm{m/s}$。",
                 "$y=0.20\\sin2\\pi\\left(0-\\dfrac{1.0}{4.0}\\right)=0.20\\sin\\left(-\\dfrac{\\pi}{2}\\right)=-0.20\\,\\mathrm{m}$。"],
                "振幅 $0.20\\,\\mathrm{m}$、周期 $0.50\\,\\mathrm{s}$、波長 $4.0\\,\\mathrm{m}$、速さ $8.0\\,\\mathrm{m/s}$、変位 $-0.20\\,\\mathrm{m}$",
                thinking="一般形と係数を比べる。$t$ の係数から周期、$x$ の係数から波長が読める。",
                misconceptions=[("$t$ の分母 0.50 は振動数である", "$\\dfrac{t}{T}$ の形なので 0.50 は周期。振動数は $\\dfrac{1}{0.50}=2.0\\,\\mathrm{Hz}$")]),
        example("ex2", "例題2　ドップラー効果",
                "振動数 $680\\,\\mathrm{Hz}$ のサイレンを鳴らしながら、救急車が速さ $20\\,\\mathrm{m/s}$ で静止した観測者に近づいてくる。観測者が聞く音の振動数と、救急車の前方での音の波長を求めよ。また、救急車が通り過ぎて遠ざかるときに聞く振動数を求めよ。" + VS,
                ["近づくとき：前方の波長 $\\lambda'=\\dfrac{V-v}{f}=\\dfrac{340-20}{680}\\fallingdotseq0.47\\,\\mathrm{m}$。",
                 "$f'=\\dfrac{V}{\\lambda'}=\\dfrac{340}{340-20}\\times680=722.5\\fallingdotseq723\\,\\mathrm{Hz}$。",
                 "遠ざかるとき（$v=-20$）：$f''=\\dfrac{340}{340+20}\\times680\\fallingdotseq642\\,\\mathrm{Hz}$。"],
                "近づくとき 約 $723\\,\\mathrm{Hz}$（波長 約 $0.47\\,\\mathrm{m}$）、遠ざかるとき 約 $642\\,\\mathrm{Hz}$",
                thinking="音源が動くと波長が変わる。音の速さ $V$ は音源の速さによらない。",
                figure=figure("音源（救急車）が右向きに速さ v で、静止した観測者に近づく", doppler_svg()),
                points=[tp("通過の前後での振動数の変化（約 $723\\,\\mathrm{Hz}\\to642\\,\\mathrm{Hz}$）を、導入で聞いたサイレンの音の高さの変化と結びつける。")]),
        example("ex3", "例題3　ヤングの実験",
                "間隔 $0.20\\,\\mathrm{mm}$ の2つのスリットに波長 $6.0\\times10^{-7}\\,\\mathrm{m}$ の単色光を当て、スリットから $1.0\\,\\mathrm{m}$ 離れたスクリーン上に干渉縞をつくった。隣り合う明線の間隔を求めよ。また、装置全体を屈折率 $\\dfrac43$ の水中に入れると、間隔はどうなるか。",
                ["$\\Delta x=\\dfrac{L\\lambda}{d}=\\dfrac{1.0\\times6.0\\times10^{-7}}{0.20\\times10^{-3}}=3.0\\times10^{-3}\\,\\mathrm{m}$。",
                 "水中では光の波長が $\\dfrac{\\lambda}{n}=\\dfrac34\\lambda$ になる（振動数は変わらない）。",
                 "$\\Delta x'=\\dfrac34\\Delta x=2.25\\times10^{-3}\\fallingdotseq2.3\\times10^{-3}\\,\\mathrm{m}$。"],
                "$3.0\\,\\mathrm{mm}$、水中では約 $2.3\\,\\mathrm{mm}$（$\\dfrac34$ 倍に狭くなる）",
                thinking="単位を m にそろえる。媒質中では波長が $\\dfrac{1}{n}$ 倍になる。",
                misconceptions=[("水中では光の振動数が変わるので間隔が変わる", "振動数は光源で決まり変わらない。変わるのは速さと波長")]),
        board("bd1", "板書案",
              [("① 波の式・ドップラー", ["$y=A\\sin2\\pi\\left(\\dfrac{t}{T}-\\dfrac{x}{\\lambda}\\right)$", "$v=\\dfrac{\\lambda}{T}$、位相差 $2\\pi\\dfrac{\\Delta x}{\\lambda}$",
                                         "$f'=\\dfrac{V-u}{V-v}f$（S→O 正）", "音源が動く → 波長が変わる", "観測者が動く → 相対速度が変わる"]),
               ("② 干渉の条件", ["経路差 $=m\\lambda$：強め合う", "経路差 $=\\left(m+\\dfrac12\\right)\\lambda$：弱め合う", "逆位相の波源 → 入れかわる",
                                "光学距離 $nl$", "小→大の反射で位相 $\\pi$"]),
               ("③ 光の干渉・回折", ["ヤング：$\\Delta x=\\dfrac{L\\lambda}{d}$", "回折格子：$d\\sin\\theta=m\\lambda$", "薄膜：$2nd$＋反射の位相",
                                    "媒質中 $\\lambda'=\\dfrac{\\lambda}{n}$、$f$ 不変"])]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("ドップラー効果の式は丸暗記させず、毎回「音源から観測者へ向かう向きを正」と図にかかせてから代入させる。", timing="例題2の前"),
               tp("干渉の問題は「①経路差（光路差）」「②反射による位相のずれ」の2段階で判断する手順を徹底させる。",
                  ask="シャボン膜で、膜が非常に薄く $d\\to0$ になると、反射光は明るいか暗いか。", expect="光路差 0 だが位相が半波長ずれるので暗い（弱め合う）。"),
               tp("回折格子の問題では、1 mm あたりの本数から格子定数への換算と、$|\\sin\\theta|\\leqq1$ による次数の上限を必ず確認させる。"),
               tp("$y$−$x$ グラフと $y$−$t$ グラフを、同じ正弦波の式の「$t$ を止めたもの」「$x$ を止めたもの」として対比させる。", caution="グラフの横軸を確認せずに波長と周期を取り違える誤りが多い。")],
              misconceptions=[("音源が速く動くほど、音そのものも速く進む", "音の速さは媒質（空気）で決まり、音源の速さによらない。変わるのは波長"),
                              ("観測者が動いても、音源が同じ速さで動くのと同じ結果になる", "音源が動くと波長、観測者が動くと相対的な音の速さが変わり、式の形が異なる"),
                              ("光が水中に入ると振動数が小さくなる", "振動数は変わらず、速さと波長が $\\dfrac{1}{n}$ 倍になる")]),
        summary("sm1", "まとめ", ["$x$ 軸正の向きに進む正弦波は $y=A\\sin2\\pi\\left(\\dfrac{t}{T}-\\dfrac{x}{\\lambda}\\right)$。位置 $x$ の点は原点より $\\dfrac{x}{v}$ 遅れて振動する。",
                                   "ドップラー効果 $f'=\\dfrac{V-u}{V-v}f$。音源が動くと波長が、観測者が動くと相対的な音の速さが変わる。",
                                   "干渉は経路差（光路差）と反射による位相の変化で決まる。ヤングの実験 $\\Delta x=\\dfrac{L\\lambda}{d}$、回折格子 $d\\sin\\theta=m\\lambda$、薄膜 $2nd$。"]),
        check("ck1", "確認問題", [("$y=0.10\\sin2\\pi\\left(\\dfrac{t}{2.0}-\\dfrac{x}{6.0}\\right)$ で表される波の速さは？", "$\\dfrac{6.0}{2.0}=3.0\\,\\mathrm{m/s}$"),
                                  ("振動数 $500\\,\\mathrm{Hz}$ の音源が速さ $40\\,\\mathrm{m/s}$ で静止した観測者に近づく。聞こえる振動数は？（音速 $340\\,\\mathrm{m/s}$）", "$\\dfrac{340}{300}\\times500\\fallingdotseq567\\,\\mathrm{Hz}$"),
                                  ("同位相の2波源からの経路差が $1.5\\lambda$ の点では、強め合うか弱め合うか。", "弱め合う"),
                                  ("ヤングの実験でスリット間隔を半分にすると、明線の間隔は何倍になるか。", "2倍"),
                                  ("1 mm あたり 500 本のすじがある回折格子の格子定数は何 m か。", "$2.0\\times10^{-6}\\,\\mathrm{m}$")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

WAVES = [("0.20", "0.50", "4.0"), ("0.10", "2.0", "6.0"), ("0.050", "0.20", "1.0"), ("0.30", "4.0", "8.0"), ("0.40", "0.25", "2.0"), ("0.15", "1.0", "3.0"), ("0.20", "0.40", "1.2")]


def wave_tex(As, Ts, Ls, sign="-"):
    return f"y={As}\\sin2\\pi\\left(\\dfrac{{t}}{{{Ts}}}{sign}\\dfrac{{x}}{{{Ls}}}\\right)"


@gen("basic_check", 4, ["computation"])
def wave_eq_basic(r):
    As, Ts, Ls = r.choice(WAVES)
    A, T, L = Q(As), Q(Ts), Q(Ls)
    kind = r.choice(["v", "f", "y", "dir", "phase"])
    eq = wave_tex(As, Ts, Ls)
    base = f"$x$ 軸上を伝わる正弦波が ${eq}$〔m〕で表される（$t$ の単位は s、$x$ の単位は m）。"
    if kind == "v":
        return numq(base + "この波の速さは何 m/s か。", L / T, f"{P(L)}/{P(T)}", "式から $T$ と $\\lambda$ を読み、$v=\\dfrac{\\lambda}{T}$。", "m/s", d=1,
                    ap="一般形 $y=A\\sin2\\pi\\left(\\dfrac{t}{T}-\\dfrac{x}{\\lambda}\\right)$ と比べ、周期と波長を読み取る。",
                    steps=[f"$T={Ts}\\,\\mathrm{{s}}$、$\\lambda={Ls}\\,\\mathrm{{m}}$。", f"$v=\\dfrac{{\\lambda}}{{T}}=\\dfrac{{{Ls}}}{{{Ts}}}={t(L / T)}\\,\\mathrm{{m/s}}$。"],
                    alt=["位相 $2\\pi\\left(\\dfrac{t}{T}-\\dfrac{x}{\\lambda}\\right)$ が一定の点（例えば山）が $\\dfrac{x}{\\lambda}=\\dfrac{t}{T}+$定数 を満たして動くので、$\\dfrac{dx}{dt}=\\dfrac{\\lambda}{T}$ と求めてもよい。"],
                    pc=[("周期と波長を読み取っている", 1), ("値が正しい", 1)], pit=["$\\lambda\\times T$ とする。"])
    if kind == "f":
        return numq(base + "この波の振動数は何 Hz か。", 1 / T, f"1/{P(T)}", "$f=\\dfrac{1}{T}$。", "Hz", d=1,
                    ap="$\\dfrac{t}{T}$ の分母が周期。振動数はその逆数。",
                    steps=[f"$T={Ts}\\,\\mathrm{{s}}$。", f"$f=\\dfrac{{1}}{{{Ts}}}={t(1 / T)}\\,\\mathrm{{Hz}}$。"],
                    alt=["式を $y=A\\sin(2\\pi ft-\\cdots)$ と書きかえて、$t$ の係数 $2\\pi f$ から読んでもよい。"],
                    pc=[("周期を読み取っている", 1), ("値が正しい", 1)], pit=["周期をそのまま振動数とする。"])
    if kind == "dir":
        sgn = r.choice(["-", "+"])
        eq2 = wave_tex(As, Ts, Ls, sgn)
        right = "$x$ 軸の正の向き" if sgn == "-" else "$x$ 軸の負の向き"
        wrong_ = "$x$ 軸の負の向き" if sgn == "-" else "$x$ 軸の正の向き"
        wr = [(wrong_, "位相が一定の点の動きを調べると逆になる。$t$ が増えたとき位相を保つには、$x$ がどちらに動けばよいかを考える。", "符号と進む向きの対応の誤り"),
              ("$y$ 軸の正の向き", "$y$ は媒質の変位で、波が伝わる向きではない。波は $x$ 軸に沿って伝わる。", "変位と伝わる向きの混同"),
              ("どちらにも進まない（定常波）", "定常波は2つの逆向きの波の重ね合わせで、$\\sin\\cdot\\cos$ の積の形になる。この式は進行波。", "進行波と定常波の混同")]
        return mc(f"$x$ 軸上を伝わる正弦波が ${eq2}$〔m〕で表される（$t$ の単位は s、$x$ の単位は m）。この波の進む向きとして正しいものを選びなさい。",
                  [right] + [w[0] for w in wr], f"位相が一定になる点は {'$x$ が増える' if sgn == '-' else '$x$ が減る'}向きに動くので、{right}に進む。", d=2,
                  ap="山（位相一定の点）が時間とともにどちらへ動くかを考える。$\\dfrac{t}{T}-\\dfrac{x}{\\lambda}$ が一定なら、$t$ が増えると $x$ も増える。",
                  steps=["位相 $2\\pi\\left(\\dfrac{t}{T}" + sgn + "\\dfrac{x}{\\lambda}\\right)$ を一定に保つ $x$ の変化を調べる。", f"{right}に進む。"],
                  alt=["$t=0$ と $t=\\dfrac{T}{4}$ の波形をかいて、山の位置がどちらへ動いたかで確かめる。"],
                  pc=[("位相一定の点の動きを考えている", 1), ("正しい向きを選んでいる", 1)], why={w[0]: (w[1], w[2]) for w in wr})
    if kind == "phase":
        dx = r.choice([sp.Rational(1, 4), sp.Rational(1, 2), sp.Rational(3, 4), sp.Rational(1, 8), sp.Rational(3, 2)])
        dxv = L * dx
        ph = 2 * dx
        return numq(base + f"$x$ 軸上で {dec(dxv)} m 離れた2点の振動の位相差は、$\\pi$ の何倍か。", ph, f"2*{P(dxv)}/{P(L)}", "位相差 $=2\\pi\\dfrac{\\Delta x}{\\lambda}$。", "倍", d=2,
                    ap="1波長離れると位相が $2\\pi$ ずれる。距離が波長の何倍かを求める。",
                    steps=[f"$\\lambda={Ls}\\,\\mathrm{{m}}$、$\\dfrac{{\\Delta x}}{{\\lambda}}=\\dfrac{{{dec(dxv)}}}{{{Ls}}}={dec(dx)}$。", f"位相差 $=2\\pi\\times{dec(dx)}={t(ph)}\\pi$。"],
                    alt=["波形のグラフをかき、2点が山・谷・節のどの位置関係にあるかで確かめる（半波長なら逆位相）。"],
                    pc=[("位相差の式を用いている", 1), ("値が正しい", 1)], pit=["$\\pi\\dfrac{\\Delta x}{\\lambda}$ と2を落とす。"])
    xk = r.choice([sp.Rational(1, 4), sp.Rational(1, 2), sp.Rational(3, 4), sp.Rational(1, 8), sp.Rational(3, 8)])
    tk = r.choice([0, sp.Rational(1, 4), sp.Rational(1, 2)])
    xv, tv = L * xk, T * tk
    y = A * sp.sin(2 * sp.pi * (tk - xk))
    return numq(base + f"位置 $x={dec(xv)}\\,\\mathrm{{m}}$ の点の、時刻 $t={dec(tv)}\\,\\mathrm{{s}}$ における変位 $y$ は何 m か。", y,
                f"{P(A)}*sin(2*pi*({P(tv)}/{P(T)}-{P(xv)}/{P(L)}))", "式に代入して位相を計算する。", "m", d=2,
                ap="まず位相 $2\\pi\\left(\\dfrac{t}{T}-\\dfrac{x}{\\lambda}\\right)$ を計算してから、三角関数の値を求める。",
                steps=[f"$\\dfrac{{t}}{{T}}-\\dfrac{{x}}{{\\lambda}}={dec(tk)}-{dec(xk)}={dec(tk - xk)}$。", f"$y={As}\\sin(2\\pi\\times({dec(tk - xk)}))\\fallingdotseq{t(y)}\\,\\mathrm{{m}}$。"],
                alt=["$t=0$ の波形（$y=-A\\sin\\dfrac{2\\pi x}{\\lambda}$）をかき、時間 $t$ だけ平行移動させた波形から読み取ってもよい。"],
                pc=[("位相を正しく計算している", 1), ("値が正しい", 1)], pit=["$\\sin$ の中の符号を誤る。"])


@gen("basic_check", 4, ["computation", "condition_check"])
def doppler_basic(r):
    kind = r.choice(["s_app", "s_rec", "o_app", "o_rec", "lam"])
    while True:
        f = r.choice([400, 480, 500, 600, 640, 680, 720, 800, 900, 960])
        sp_ = r.choice([10, 17, 20, 30, 34, 40, 60, 68])
        if kind == "s_app":
            fp = sp.Rational(V * f, V - sp_)
        elif kind == "s_rec":
            fp = sp.Rational(V * f, V + sp_)
        elif kind == "o_app":
            fp = sp.Rational((V + sp_) * f, V)
        elif kind == "o_rec":
            fp = sp.Rational((V - sp_) * f, V)
        else:
            fp = sp.Rational(V - sp_, f)
        if fp.q == 1 or (kind == "lam" and is_exact(t(fp), fp)):
            break
    if kind == "lam":
        return numq(f"振動数 {f} Hz の音を出す音源が、速さ {sp_} m/s で一直線上を進んでいる。音源の進む向きの前方の空気中での音の波長は何 m か。" + VS,
                    fp, f"({V}-{sp_})/{f}", "前方では、1秒間に出た $f$ 個の波が長さ $V-v$ に詰まる。", "m", d=2, fig=figure("音源 S が右向きに動き、前方に音が伝わる", doppler_svg()),
                    ap="音源が動くと波長が変わる。音の速さ $V$ は変わらない。",
                    steps=[f"$\\lambda'=\\dfrac{{V-v}}{{f}}=\\dfrac{{{V}-{sp_}}}{{{f}}}$。", f"$\\lambda'={t(fp)}\\,\\mathrm{{m}}$。"],
                    alt=[f"静止時の波長 $\\dfrac{{{V}}}{{{f}}}$ と比べて短くなることを確かめる。"],
                    pc=[("波長の式を立てている", 1), ("値が正しい", 1)], pit=["$\\dfrac{V+v}{f}$ とする（後方の波長）。"])
    texts = {"s_app": (f"振動数 {f} Hz の音を出す音源が、静止している観測者に向かって速さ {sp_} m/s で近づいている。", f"\\dfrac{{{V}}}{{{V}-{sp_}}}\\times{f}", f"{V}*{f}/({V}-{sp_})",
                       "音源が近づく → 波長が短くなる → 高く聞こえる。"),
             "s_rec": (f"振動数 {f} Hz の音を出す音源が、静止している観測者から速さ {sp_} m/s で遠ざかっている。", f"\\dfrac{{{V}}}{{{V}+{sp_}}}\\times{f}", f"{V}*{f}/({V}+{sp_})",
                       "音源が遠ざかる → 観測者側の波長が長くなる → 低く聞こえる。"),
             "o_app": (f"静止している音源が振動数 {f} Hz の音を出している。観測者が速さ {sp_} m/s で音源に向かって近づいている。", f"\\dfrac{{{V}+{sp_}}}{{{V}}}\\times{f}", f"({V}+{sp_})*{f}/{V}",
                       "観測者が近づく → 観測者に対する音の速さが $V+u$ になる → 高く聞こえる。"),
             "o_rec": (f"静止している音源が振動数 {f} Hz の音を出している。観測者が速さ {sp_} m/s で音源から遠ざかっている。", f"\\dfrac{{{V}-{sp_}}}{{{V}}}\\times{f}", f"({V}-{sp_})*{f}/{V}",
                       "観測者が遠ざかる → 観測者に対する音の速さが $V-u$ になる → 低く聞こえる。")}
    st, form, expr, why = texts[kind]
    src_moves = kind.startswith("s")
    return numq(st + "観測者が聞く音の振動数は何 Hz か。" + VS, fp, expr, why, "Hz", d=2,
                fig=figure("音源 S と観測者 O が一直線上にある", doppler_svg("v" if src_moves else "", "" if src_moves else "u")),
                ap="音源から観測者へ向かう向きを正とし、$f'=\\dfrac{V-u}{V-v}f$ に符号つきで代入する。",
                steps=[f"{'音源の速度 $v=' + ('+' if kind == 's_app' else '-') + str(sp_) + '$、$u=0$' if src_moves else '観測者の速度 $u=' + ('-' if kind == 'o_app' else '+') + str(sp_) + '$、$v=0$'}。",
                       f"$f'={form}={t(fp)}\\,\\mathrm{{Hz}}$。"],
                alt=["近づけば高く、遠ざかれば低くなるはず、という定性的な結果と答えの大小が合うかを確かめる。"],
                pc=[("正の向きを決めて符号を正しく代入している", 1), ("値が正しい", 1)], pit=["分母と分子の符号を取り違える。", "音源が動く場合と観測者が動く場合の式を混同する。"])


@gen("basic_check", 3, ["concept", "computation"])
def interference_basic(r):
    lam = r.choice(["2.0", "4.0", "1.5", "3.0", "0.80"])
    L = Q(lam)
    k = r.choice([sp.Rational(1), sp.Rational(2), sp.Rational(3, 2), sp.Rational(5, 2), sp.Rational(1, 2), sp.Rational(3), sp.Rational(3, 4), sp.Rational(5, 4)])
    phase = r.choice(["同位相", "同位相", "逆位相"])
    d1 = r.choice([10, 12, 15, 20, 24])
    d1 = Q(d1)
    d2 = d1 + k * L
    if k.q == 1:
        res = "強め合う" if phase == "同位相" else "弱め合う"
    elif k.q == 2:
        res = "弱め合う" if phase == "同位相" else "強め合う"
    else:
        res = "強め合いも弱め合いもしない（中間の振幅になる）"
    opts = ["強め合う", "弱め合う", "強め合いも弱め合いもしない（中間の振幅になる）"]
    why_txt = {"強め合う": ("経路差が波長の整数倍（同位相の波源）または半波長の奇数倍（逆位相の波源）のときに強め合う。この点ではその条件を満たさない。", "干渉条件の取り違え"),
               "弱め合う": ("経路差が半波長の奇数倍（同位相の波源）または波長の整数倍（逆位相の波源）のときに弱め合う。この点ではその条件を満たさない。", "干渉条件の取り違え"),
               "強め合いも弱め合いもしない（中間の振幅になる）": ("経路差が半波長の整数倍になっているので、強め合うか弱め合うかのどちらかになる。", "経路差の計算の誤り")}
    wrong = [o for o in opts if o != res]
    return mc(f"水面上の2点 $\\mathrm{{S_1}}$、$\\mathrm{{S_2}}$ に置いた波源が、{phase}で波長 {lam} cm の波を出している。$\\mathrm{{S_1}}$ から {dec(d1)} cm、$\\mathrm{{S_2}}$ から {dec(d2)} cm の位置にある点 P で、2つの波はどうなるか。正しいものを選びなさい。",
              [res] + wrong, f"経路差 {dec(d2 - d1)} cm は波長の {dec(k)} 倍。{phase}の波源なので「{res}」。", d=2,
              ap="経路差が波長の何倍かを計算し、波源の位相（同位相か逆位相か）とあわせて判断する。",
              steps=[f"経路差 $|\\mathrm{{S_1P}}-\\mathrm{{S_2P}}|={dec(d2 - d1)}\\,\\mathrm{{cm}}={dec(k)}\\lambda$。", f"{phase}の波源なので「{res}」。"],
              alt=["2つの波源からの山の数を数え、P に山と山（または谷と谷）が届くか、山と谷が届くかで判断してもよい。"],
              pc=[("経路差を波長で表している", 1), ("正しく判断している", 1)], why={w: why_txt[w] for w in wrong},
              chk=(f"({P(d2)}-{P(d1)})/{P(L)}", str(k), None, "intermediate"))


@gen("basic_check", 3, ["computation"])
def young_basic(r):
    kind = r.choice(["dx", "lam", "ratio_d", "xm"])
    dmm = r.choice(["0.20", "0.25", "0.50", "0.40", "0.30"])
    Lm = r.choice(["1.0", "1.5", "2.0", "0.80"])
    lam_nm = r.choice([400, 450, 500, 600, 640, 700])
    d, Lr, lam = Q(dmm) / 1000, Q(Lm), sp.Rational(lam_nm, 10 ** 9)
    dx = Lr * lam / d
    if kind == "dx":
        return numq(f"ヤングの実験で、間隔 {dmm} mm の2つのスリットに波長 ${sig(lam, 2) if lam_nm % 100 == 0 else sig(lam, 3)}\\,\\mathrm{{m}}$ の単色光を当て、スリットから {Lm} m 離れたスクリーン上に干渉縞をつくった。隣り合う明線の間隔は何 m か。",
                    dx, f"{P(Lr)}*{P(lam)}/{P(d)}", "$\\Delta x=\\dfrac{L\\lambda}{d}$。", "m", n=2, d=2,
                    ap="単位を m にそろえて $\\Delta x=\\dfrac{L\\lambda}{d}$ に代入する。",
                    steps=[f"$d={dmm}\\times10^{{-3}}\\,\\mathrm{{m}}$。", f"$\\Delta x=\\dfrac{{{Lm}\\times{sig(lam, 3)}}}{{{dmm}\\times10^{{-3}}}}\\fallingdotseq{t(dx, 2)}\\,\\mathrm{{m}}$。"],
                    alt=["答えが mm 程度になる（目で見える縞の間隔）ことを目安に、桁を確かめる。"],
                    pc=[("明線の間隔の式を用いている", 1), ("値が正しい", 1)], pit=["mm を m に直し忘れる。"])
    if kind == "lam":
        dxs = sig(dx, 2)
        dxv = sp.nsimplify(Decimal(str(sp.N(dx, 30))).quantize(Decimal("0.0001")))
        lam2 = dxv * d / Lr
        return numq(f"ヤングの実験で、間隔 {dmm} mm の2つのスリットに単色光を当て、スリットから {Lm} m 離れたスクリーン上で、隣り合う明線の間隔を測ると {dec(dxv * 1000)} mm であった。光の波長は何 m か。",
                    lam2, f"{P(dxv)}*{P(d)}/{P(Lr)}", "$\\lambda=\\dfrac{d\\Delta x}{L}$。", "m", n=2, d=2,
                    ap="明線の間隔の式を波長について解く。",
                    steps=[f"$\\lambda=\\dfrac{{d\\Delta x}}{{L}}=\\dfrac{{{dmm}\\times10^{{-3}}\\times{dec(dxv * 1000)}\\times10^{{-3}}}}{{{Lm}}}$。", f"$\\lambda\\fallingdotseq{t(lam2, 2)}\\,\\mathrm{{m}}$。"],
                    alt=["可視光の波長（約 $4\\times10^{-7}$〜$7\\times10^{-7}\\,\\mathrm{m}$）の範囲に入るかで確かめる。"],
                    pc=[("式を変形している", 1), ("値が正しい", 1)], pit=["mm を m に直し忘れる。"])
    if kind == "xm":
        m = r.choice([2, 3, 4])
        x = m * dx
        return numq(f"ヤングの実験で、間隔 {dmm} mm の2つのスリットに波長 ${sig(lam, 3)}\\,\\mathrm{{m}}$ の単色光を当て、スリットから {Lm} m 離れたスクリーン上に干渉縞をつくった。スクリーン中央の明線を0番目として、{m} 番目の明線の中央からの距離は何 m か。",
                    x, f"{m}*{P(Lr)}*{P(lam)}/{P(d)}", "$x_m=\\dfrac{mL\\lambda}{d}$。", "m", n=2, d=2,
                    ap="明線の条件 $\\dfrac{dx}{L}=m\\lambda$ を $x$ について解く。",
                    steps=[f"$x_{m}=\\dfrac{{{m}L\\lambda}}{{d}}$。", f"$x_{m}\\fallingdotseq{t(x, 2)}\\,\\mathrm{{m}}$。"],
                    alt=["明線の間隔 $\\Delta x$ を求めて、その " + str(m) + " 倍としてもよい。"],
                    pc=[("明線の条件を用いている", 1), ("値が正しい", 1)], pit=["中央の明線を1番目と数えてずれる。"])
    k, lab = r.choice([(sp.Rational(1, 2), "半分"), (2, "2倍"), (3, "3倍"), (sp.Rational(1, 3), "$\\dfrac13$")])
    return numq(f"ヤングの実験で、スクリーンまでの距離と光の波長を変えずに、2つのスリットの間隔を{lab}{'' if lab.startswith('$') is False else ' 倍'}にした。隣り合う明線の間隔はもとの何倍になるか。",
                1 / sp.Rational(k), f"1/{P(k)}", "$\\Delta x=\\dfrac{L\\lambda}{d}$ は $d$ に反比例。", "倍", d=1,
                ap="明線の間隔の式で、変わる量だけに注目する。",
                steps=["$\\Delta x\\propto\\dfrac{1}{d}$。", f"$d$ が{lab}{'' if not lab.startswith('$') else ' 倍'}なので、$\\Delta x$ は ${t(1 / sp.Rational(k))}$ 倍。"],
                alt=["スリットを近づけると経路差が小さくなり、同じ経路差を得るには P を中央から遠ざける必要がある、と定性的に確かめる。"],
                pc=[("反比例の関係を用いている", 1), ("値が正しい", 1)], pit=["比例すると考える。"])


@gen("basic_check", 3, ["computation", "condition_check"])
def grating_basic(r):
    kind = r.choice(["d", "sin", "lam", "max"])
    N = r.choice([200, 250, 400, 500, 1000])
    d = sp.Rational(1, N * 1000)
    if kind == "d":
        return numq(f"1 mm あたり {N} 本のすじが等間隔に刻まれた回折格子の格子定数（すじの間隔）は何 m か。", d, f"1/({N}*1000)", "$d=\\dfrac{1}{N}\\,\\mathrm{mm}$。", "m", n=2, d=1,
                    ap="1 mm を本数で割ると、すじ1本あたりの間隔になる。単位を m にする。",
                    steps=[f"$d=\\dfrac{{1}}{{{N}}}\\,\\mathrm{{mm}}=\\dfrac{{1\\times10^{{-3}}}}{{{N}}}\\,\\mathrm{{m}}$。", f"$d={t(d, 2)}\\,\\mathrm{{m}}$。"],
                    alt=["$d\\times N=1\\,\\mathrm{mm}$ になることで確かめる。"],
                    pc=[("本数から間隔に換算している", 1), ("値が正しい", 1)], pit=["本数をそのまま間隔とする。"])
    lam_nm = r.choice([400, 450, 500, 600, 625, 700])
    lam = sp.Rational(lam_nm, 10 ** 9)
    if kind == "sin":
        m = r.choice([1, 2])
        s = m * lam / d
        if s >= 1:
            m, s = 1, lam / d
        return numq(f"1 mm あたり {N} 本のすじがある回折格子に、波長 ${sig(lam, 3)}\\,\\mathrm{{m}}$ の単色光を垂直に当てた。{m} 次の明線が見える方向と入射方向のなす角を $\\theta$ とするとき、$\\sin\\theta$ の値を求めなさい。",
                    s, f"{m}*{P(lam)}/{P(d)}", "$d\\sin\\theta=m\\lambda$。", "", d=2,
                    ap="格子定数を m で求めてから $d\\sin\\theta=m\\lambda$ に代入する。",
                    steps=[f"$d=\\dfrac{{1\\times10^{{-3}}}}{{{N}}}={t(d, 2)}\\,\\mathrm{{m}}$。", f"$\\sin\\theta=\\dfrac{{{m}\\lambda}}{{d}}={t(s)}$。"],
                    alt=["$\\sin\\theta$ が 1 を超えないことを確かめ、その次数の明線が実際に見えることを確認する。"],
                    pc=[("格子定数を求めている", 1), ("値が正しい", 1)], pit=["mm と m の換算を誤る。"])
    if kind == "lam":
        th = r.choice([30, 30, 45])
        m = 1
        lam2 = d * SIN[th] / m
        return numq(f"1 mm あたり {N} 本のすじがある回折格子に単色光を垂直に当てたところ、1 次の明線が入射方向と ${th}^\\circ$ の方向に見えた。光の波長は何 m か。",
                    lam2, f"{P(d)}*sin(deg({th}))", "$\\lambda=d\\sin\\theta$（$m=1$）。", "m", n=2, d=2,
                    ap="1次の明線の条件 $d\\sin\\theta=\\lambda$ を使う。",
                    steps=[f"$d={t(d, 2)}\\,\\mathrm{{m}}$。", f"$\\lambda=d\\sin{th}^\\circ\\fallingdotseq{t(lam2, 2)}\\,\\mathrm{{m}}$。"],
                    alt=["求めた波長が可視光の範囲（約 $4\\times10^{-7}$〜$7.7\\times10^{-7}\\,\\mathrm{m}$）にあるかどうかで、光の色の見当をつける。"],
                    pc=[("回折格子の式を用いている", 1), ("値が正しい", 1)], pit=["$\\sin$ と $\\cos$ を取り違える。"])
    mmax = int(sp.floor(d / lam))
    if d / lam == mmax:
        mmax -= 1
    return numq(f"1 mm あたり {N} 本のすじがある回折格子に、波長 ${sig(lam, 3)}\\,\\mathrm{{m}}$ の単色光を垂直に当てた。格子の片側で観測できる明線は、最大で何次までか。",
                sp.Integer(mmax), f"floor({P(d)}/{P(lam)}-Rational(1,10**9))", "$\\sin\\theta=\\dfrac{m\\lambda}{d}<1$ を満たす最大の $m$。", "次", d=3,
                ap="$|\\sin\\theta|\\leqq1$ なので、$m\\leqq\\dfrac{d}{\\lambda}$。$\\theta=90^\\circ$ ちょうどの方向はスクリーンに届かないので除く。",
                steps=[f"$\\dfrac{{d}}{{\\lambda}}=\\dfrac{{{t(d, 2)}}}{{{sig(lam, 3)}}}={t(d / lam, 3)}$。", f"$m<{t(d / lam, 3)}$ を満たす最大の整数は $m={mmax}$。"],
                alt=["$m=" + str(mmax + 1) + "$ を代入すると $\\sin\\theta\\geqq1$ となり、その次数の明線は存在しないことで確かめる。"],
                pc=[("$\\sin\\theta<1$ の条件を用いている", 2), ("値が正しい", 1)], pit=["$\\dfrac{d}{\\lambda}$ を四捨五入する。"])


CONCEPT = [
    ("音源が観測者に近づくときに音が高く聞こえる理由として、正しいものを選びなさい。",
     "音源の前方で音の波長が短くなるから",
     [("音源の速さの分だけ音の速さが大きくなるから", "音の速さは空気で決まり、音源の速さによらない。変わるのは波長。", "音速と音源の速さの混同"),
      ("音源が出す音の振動数そのものが大きくなるから", "音源自体の振動数は変わらない。観測される振動数が変わる。", "音源の振動数と観測振動数の混同"),
      ("音の振幅が大きくなるから", "振幅は音の大きさに関係し、高さ（振動数）とは別の量。", "振幅と振動数の混同")]),
    ("光が空気中から水中に入るとき、変化しないものを選びなさい。",
     "振動数",
     [("速さ", "水中では光の速さは $\\dfrac{c}{n}$ に小さくなる。", "振動数と速さの混同"),
      ("波長", "振動数が変わらず速さが小さくなるので、波長も $\\dfrac{1}{n}$ 倍になる。", "波長と振動数の混同"),
      ("進む向き（斜めに入射したとき）", "斜めに入射すると屈折して進む向きが変わる。", "屈折の見落とし")]),
    ("ヤングの実験で、明線の間隔を広くする方法として正しいものを選びなさい。",
     "スクリーンをスリットから遠ざける",
     [("スリットの間隔を広げる", "$\\Delta x=\\dfrac{L\\lambda}{d}$ は $d$ に反比例するので、間隔は狭くなる。", "比例・反比例の取り違え"),
      ("波長の短い光（青い光）に変える", "$\\Delta x$ は波長に比例するので、波長が短いと狭くなる。", "波長と間隔の関係の誤解"),
      ("装置全体を水中に入れる", "水中では波長が $\\dfrac{1}{n}$ 倍になり、間隔は狭くなる。", "媒質中の波長の誤解")]),
    ("シャボン膜に白色光を当てると色づいて見える理由として、正しいものを選びなさい。",
     "膜の表面と裏面で反射した光が干渉し、膜の厚さによって強め合う波長が異なるから",
     [("シャボン液に色素が含まれているから", "透明な液でも色づく。色は干渉によるもので、色素によるものではない。", "干渉色と色素の混同"),
      ("光が膜で回折して、色ごとに曲がる角度が違うから", "シャボン膜の色は2つの反射光の干渉による。回折格子とは別の現象。", "干渉と回折の混同"),
      ("膜の中で光の振動数が変わるから", "媒質中でも振動数は変わらない。変わるのは波長。", "振動数の不変性の誤解")]),
    ("$x$ 軸の正の向きに進む横波について、正しいものを選びなさい。",
     "媒質の各点は、その場で $y$ 軸方向に単振動している",
     [("媒質の各点は、波とともに $x$ 軸の正の向きに移動していく", "波が伝わっても媒質は移動しない。伝わるのは振動（エネルギー）。", "媒質の移動の誤解"),
      ("山の位置にある媒質の速さが最大である", "山（変位最大）の点は単振動の端なので速さは 0。速さが最大なのは変位 0 の点。", "変位と速さの関係の誤解"),
      ("1波長離れた2点は、逆向きに振動している", "1波長離れた2点は同位相。逆位相になるのは半波長離れた2点。", "位相差の誤解")]),
    ("2つの同位相の波源による水面波の干渉で、弱め合う点を連ねた線（節線）について正しいものを選びなさい。",
     "2つの波源からの距離の差が、半波長の奇数倍になる点の集まりである",
     [("2つの波源からの距離の差が、波長の整数倍になる点の集まりである", "距離の差が波長の整数倍の点では強め合う（腹線）。", "強め合いと弱め合いの条件の取り違え"),
      ("2つの波源を結ぶ線分の垂直二等分線である", "垂直二等分線上は距離の差が 0 で、強め合う（腹線）。", "経路差 0 の扱いの誤り"),
      ("波長を短くすると、節線の数は減る", "波長が短いほど、波源間に入る半波長の数が増え、節線は増える。", "波長と本数の関係の誤解")]),
    ("回折格子について正しいものを選びなさい。",
     "すじの間隔が狭い回折格子ほど、同じ次数の明線は大きな角度に現れる",
     [("すじの間隔が狭いほど、観測できる明線の次数は多くなる", "$m\\leqq\\dfrac{d}{\\lambda}$ なので、間隔 $d$ が狭いほど観測できる次数は少ない。", "格子定数と次数の関係の誤解"),
      ("白色光を当てると、1次の明線では紫の光が最も外側に現れる", "$\\sin\\theta=\\dfrac{\\lambda}{d}$ より波長の長い赤ほど外側に現れる。", "波長と回折角の関係の取り違え"),
      ("0次の明線（中央）は、白色光でも色に分かれる", "0次は経路差 0 なので全波長が同じ方向で強め合い、白色のまま。", "0次の明線の誤解")]),
    ("風が音源から観測者の向きに一定の速さで吹いている。音源と観測者がともに地面に対して静止しているとき、観測者が聞く音について正しいものを選びなさい。",
     "振動数は音源の振動数と変わらない",
     [("振動数は音源の振動数より大きくなる", "音源も観測者も静止していれば、1秒間に届く波の数は音源が出す数と等しい。", "風の効果の誤解"),
      ("振動数は音源の振動数より小さくなる", "風は音の速さと波長を同じ割合で変えるので、振動数は変わらない。", "風の効果の誤解"),
      ("音の速さは変わらない", "風下向きには音の速さが風の速さだけ大きくなる。", "媒質の運動の無視")]),
]


@gen("basic_check", 3, ["concept", "condition_check"])
def concept_mc(r):
    stem, right, wr = r.choice(CONCEPT)
    return mc(stem, [right] + [w[0] for w in wr], f"正しいのは「{right}」。" + wr[0][1], d=2,
              ap="波の速さ・振動数・波長のうち、何が媒質で決まり、何が波源で決まるかを区別して判断する。",
              steps=["$v=f\\lambda$、干渉の条件、ドップラー効果の仕組みに照らして各選択肢を確認する。", f"正しいのは「{right}」。"],
              alt=["誤りの選択肢が正しいとすると、どんな観測結果になるかを考え、実際の現象と比べて消去する。"],
              pc=[("判断の根拠を確認している", 1), ("正しい選択肢を選んでいる", 1)],
              why={w[0]: (w[1], w[2]) for w in wr})


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 4, ["computation", "application"])
def doppler_apps(r):
    kind = r.choice(["both", "reflect", "beat", "wind"])
    if kind == "both":
        while True:
            f = r.choice([500, 600, 640, 680, 720, 800, 900])
            vs, uo = r.sample([10, 20, 30, 40], 2)
            fp = sp.Rational((V + uo) * f, V - vs)
            if fp.q == 1:
                break
        return numq(f"振動数 {f} Hz の音を出す音源 S が速さ {vs} m/s で右向きに、観測者 O が速さ {uo} m/s で左向きに、一直線上を互いに近づく向きに進んでいる（S は O の左側）。O が聞く音の振動数は何 Hz か。" + VS,
                    fp, f"({V}+{uo})*{f}/({V}-{vs})", "S→O の向き（右向き）を正とすると、$v=+" + str(vs) + "$、$u=-" + str(uo) + "$。", "Hz", d=3,
                    fig=figure("音源 S が右向きに速さ v、観測者 O が左向きに速さ u で互いに近づく", doppler_svg("v", "u")),
                    ap="正の向きを「音源から観測者へ」と決め、音源・観測者の速度を符号つきで $f'=\\dfrac{V-u}{V-v}f$ に代入する。",
                    steps=[f"$v=+{vs}\\,\\mathrm{{m/s}}$、$u=-{uo}\\,\\mathrm{{m/s}}$。", f"$f'=\\dfrac{{{V}-(-{uo})}}{{{V}-{vs}}}\\times{f}={t(fp)}\\,\\mathrm{{Hz}}$。"],
                    alt=["まず音源の運動で波長 $\\lambda'=\\dfrac{V-v}{f}$ を求め、次に観測者に対する音の速さ $V+u$ を波長で割る、と2段階で計算しても同じ。"],
                    pc=[("速度の符号を正しく決めている", 2), ("値が正しい", 2)], pit=["観測者の速度の符号を誤る。"])
    if kind in ("reflect", "beat"):
        while True:
            f = r.choice([500, 510, 680, 850, 1000, 340])
            u = r.choice([10, 17, 20, 34])
            f2 = sp.Rational(f * (V + u), V - u)
            if f2.q == 1:
                break
        if kind == "reflect":
            return numq(f"静止した音源から振動数 {f} Hz の音を出し、音源に向かって速さ {u} m/s で近づいてくる大きな反射板に当てた。音源の位置で静止して聞く反射音の振動数は何 Hz か。" + VS,
                        f2, f"{f}*({V}+{u})/({V}-{u})", "反射板を「動く観測者」→「動く音源」と2段階で考える。", "Hz", d=4,
                        ap="反射板が受け取る振動数 $f_1$ を求め、反射板がその振動数の音を出しながら近づく音源になる、と考える。",
                        steps=[f"反射板が受け取る振動数：$f_1=\\dfrac{{{V}+{u}}}{{{V}}}\\times{f}$。", f"反射音：$f_2=\\dfrac{{{V}}}{{{V}-{u}}}f_1=\\dfrac{{{V}+{u}}}{{{V}-{u}}}\\times{f}={t(f2)}\\,\\mathrm{{Hz}}$。"],
                        alt=["反射板が静止していれば $f_2=f$ になることを確かめ、近づく場合は2回とも振動数が上がることから答えの大小を確かめる。"],
                        pc=[("反射板を観測者として扱っている", 1), ("反射板を音源として扱っている", 2), ("値が正しい", 1)], pit=["ドップラー効果を1回だけ考える。"])
        return numq(f"静止した音源から振動数 {f} Hz の音を出し、音源に向かって速さ {u} m/s で近づいてくる大きな反射板に当てた。音源のそばで静止している観測者には、音源からの直接音と反射音が重なってうなりが聞こえた。1秒あたりのうなりの回数は何回か。" + VS,
                    f2 - f, f"{f}*({V}+{u})/({V}-{u})-{f}", "うなりの回数＝2つの振動数の差。", "回", d=4,
                    ap="反射音の振動数を2段階のドップラー効果で求め、直接音との振動数の差をとる。",
                    steps=[f"反射音 $f_2=\\dfrac{{{V}+{u}}}{{{V}-{u}}}\\times{f}={t(f2)}\\,\\mathrm{{Hz}}$。", f"うなり $f_2-f={t(f2 - f)}$ 回/s。"],
                    alt=["$f_2-f=\\dfrac{2u}{V-u}f$ と式を整理してから代入しても同じ。"],
                    pc=[("反射音の振動数を求めている", 2), ("うなりを振動数の差で求めている", 2)], pit=["反射を1回のドップラー効果として計算する。"])
    while True:
        f = r.choice([500, 600, 680, 720, 800])
        w = r.choice([10, 20])
        vs = r.choice([10, 20, 30])
        fp = sp.Rational((V + w) * f, V + w - vs)
        if fp.q == 1 or is_exact(t(fp), fp):
            break
    return numq(f"風が音源から観測者の向きに速さ {w} m/s で吹いている。振動数 {f} Hz の音を出す音源が、静止した観測者に向かって地面に対して速さ {vs} m/s で近づいている。観測者が聞く音の振動数は何 Hz か。無風のときの音の速さを $340\\,\\mathrm{{m/s}}$ とする。",
                fp, f"({V}+{w})*{f}/({V}+{w}-{vs})", "風下向きの音の速さは $V+w$。これを $V$ の代わりに用いる。", "Hz", d=4,
                ap="風があると、地面に対する音の速さが変わる（風下向きに $V+w$）。音源・観測者の速度は地面に対して測る。",
                steps=[f"風下向きの音の速さ $V'={V}+{w}={V + w}\\,\\mathrm{{m/s}}$。", f"$f'=\\dfrac{{V'}}{{V'-v}}f=\\dfrac{{{V + w}}}{{{V + w}-{vs}}}\\times{f}\\fallingdotseq{t(fp)}\\,\\mathrm{{Hz}}$。"],
                alt=["空気（風）とともに動く立場で考えると、音源は空気に対して $v-w$、観測者は $-w$ で動く。これで計算しても同じ結果になる。"],
                pc=[("風による音の速さの変化を考えている", 2), ("値が正しい", 2)], pit=["風を音源の速さに加えてしまう。"])


@gen("standard_practice", 3, ["concept", "computation"])
def wave_graph(r):
    lam = r.choice([2, 4])
    A = r.choice([1, 2])
    pos = r.choice(["0", "q", "h", "3q"])
    xs = {"0": 0, "q": lam / 4, "h": lam / 2, "3q": 3 * lam / 4}[pos]
    ys = {"0": 0, "q": A, "h": 0, "3q": -A}[pos]
    dirn = r.choice(["+", "-"])
    fig = figure(f"時刻 t=0 の正弦波の波形。波長 {lam} m、振幅 {A} cm。点 P は x={xs} m の位置", wave_svg(lam, A, [(xs, ys, "P")]))
    slope_pos = pos == "0"
    if pos in ("q", "3q"):
        right = "速度は 0（瞬間的に静止している）"
    else:
        up = (slope_pos and dirn == "-") or (not slope_pos and dirn == "+")
        right = "$y$ 軸の正の向き" if up else "$y$ 軸の負の向き"
    opts = {"$y$ 軸の正の向き": ("波形を少し進めた図をかくと、P の変位はその向きには変化しない。", "媒質の速度の向きの判断の誤り"),
            "$y$ 軸の負の向き": ("波形を少し進めた図をかくと、P の変位はその向きには変化しない。", "媒質の速度の向きの判断の誤り"),
            "速度は 0（瞬間的に静止している）": ("速度が 0 になるのは山や谷（変位が最大）の点。P は変位が 0 の点で、速さは最大。", "変位と速度の関係の誤解"),
            "波の進む向き（$x$ 軸方向）": ("横波の媒質は $y$ 軸方向に振動し、$x$ 軸方向には移動しない。", "媒質の移動の誤解")}
    if right.startswith("速度"):
        opts["$y$ 軸の正の向き"] = ("山・谷の点は振動の端にあり、この瞬間の速度は 0。", "変位と速度の関係の誤解")
        opts["$y$ 軸の負の向き"] = ("山・谷の点は振動の端にあり、この瞬間の速度は 0。", "変位と速度の関係の誤解")
    wrong = [o for o in opts if o != right]
    return mc(f"図は、$x$ 軸の{'正' if dirn == '+' else '負'}の向きに進む正弦波の、時刻 $t=0$ における波形である。図の点 P（$x={xs}\\,\\mathrm{{m}}$）の媒質の、この瞬間の速度の向きとして正しいものを選びなさい。",
              [right] + wrong, f"波形をわずかに{'右' if dirn == '+' else '左'}へずらした図をかき、P の変位の変化を見ると「{right}」。", d=3, fig=fig,
              ap="少し時間がたったときの波形（波の進む向きにわずかにずらした波形）をかき、P の変位がどう変わるかを見る。",
              steps=[f"波形を{'右' if dirn == '+' else '左'}へわずかに平行移動させた図をかく。", "P の位置での変位の増減から速度の向きを判断する。", f"答え：{right}。"],
              alt=["「波の進む向きに見て、手前（上流側）の媒質の動きを、少し遅れてまねる」と考えると、P の手前側の変位がこれからの P の変位になる。"],
              pc=[("少し後の波形を考えている", 2), ("正しい向きを選んでいる", 2)], why={w: opts[w] for w in wrong})


@gen("standard_practice", 4, ["computation", "condition_check"])
def thin_film(r):
    kind = r.choice(["soap", "coat", "wedge", "soap_dark"])
    lam_nm = r.choice([480, 500, 560, 600, 640, 660])
    lam = sp.Rational(lam_nm, 10 ** 9)
    if kind in ("soap", "soap_dark"):
        n = r.choice(["1.2", "1.25", "1.5", "1.6"])
        nn = Q(n)
        if kind == "soap":
            d = lam / (4 * nn)
            return numq(f"空気中にある屈折率 {n} の薄い膜に、波長 ${sig(lam, 2)}\\,\\mathrm{{m}}$ の光を垂直に当てた。反射光が強め合うような膜の厚さのうち、最小のものは何 m か。",
                        d, f"{P(lam)}/(4*{P(nn)})", "膜の上面の反射で位相が $\\pi$ ずれるので、強め合う条件は $2nd=\\left(m+\\dfrac12\\right)\\lambda$。", "m", n=2, d=3,
                        fig=figure("厚さ d、屈折率 n の薄膜に入射した光が、上面で反射する光①と下面で反射する光②に分かれる", film_svg()),
                        ap="光路差 $2nd$ に加えて、反射による位相の変化を確認する。空気→膜（小→大）で位相が反転、膜→空気（大→小）では反転しない。",
                        steps=["位相のずれは差し引き半波長なので、強め合う条件は $2nd=\\left(m+\\dfrac12\\right)\\lambda$。", "最小は $m=0$：$d=\\dfrac{\\lambda}{4n}$。",
                               f"$d=\\dfrac{{{sig(lam, 2)}}}{{4\\times{n}}}\\fallingdotseq{t(d, 2)}\\,\\mathrm{{m}}$。"],
                        alt=["膜の中の波長 $\\dfrac{\\lambda}{n}$ の $\\dfrac14$ が最小の厚さ、と考えてもよい（往復で半波長＋反射で半波長＝1波長）。"],
                        pc=[("反射による位相の変化を考えている", 2), ("値が正しい", 2)], pit=["位相の変化を考えずに $2nd=\\lambda$ とする。"])
        d = lam / (2 * nn)
        return numq(f"空気中にある屈折率 {n} の薄い膜に、波長 ${sig(lam, 2)}\\,\\mathrm{{m}}$ の光を垂直に当てた。反射光が弱め合うような膜の厚さのうち、0 でない最小のものは何 m か。",
                    d, f"{P(lam)}/(2*{P(nn)})", "弱め合う条件は $2nd=m\\lambda$（$m=1,2,\\cdots$）。", "m", n=2, d=3,
                    ap="空気中の薄膜では反射による位相のずれが差し引き半波長。弱め合う条件は光路差が波長の整数倍。",
                    steps=["弱め合う条件 $2nd=m\\lambda$。", "0 でない最小は $m=1$：$d=\\dfrac{\\lambda}{2n}$。", f"$d\\fallingdotseq{t(d, 2)}\\,\\mathrm{{m}}$。"],
                    alt=["$d\\to0$ のとき反射光は弱め合う（暗く見える）ことと、弱め合いの条件 $m=0$ が対応していることを確かめる。"],
                    pc=[("弱め合う条件を位相の変化を含めて立てている", 2), ("値が正しい", 2)], pit=["$2nd=\\left(m+\\dfrac12\\right)\\lambda$ を弱め合いの条件とする。"])
    if kind == "coat":
        n = r.choice(["1.25", "1.3", "1.38", "1.2"])
        nn = Q(n)
        d = lam / (4 * nn)
        return numq(f"屈折率 1.5 のガラスの表面に、屈折率 {n} の薄い膜をつけて反射防止膜とする。波長 ${sig(lam, 2)}\\,\\mathrm{{m}}$ の光を垂直に当てたとき、反射光が弱め合う膜の厚さのうち最小のものは何 m か。",
                    d, f"{P(lam)}/(4*{P(nn)})", "膜の上面（空気→膜）も下面（膜→ガラス）も小→大の反射で、どちらも位相が反転する。", "m", n=2, d=4,
                    ap="2つの反射の両方で位相が反転するので、反射による位相のずれは打ち消し合う。弱め合う条件は $2nd=\\left(m+\\dfrac12\\right)\\lambda$。",
                    steps=[f"屈折率の大小：空気 1.0 < 膜 {n} < ガラス 1.5。2回とも位相反転。", "弱め合う条件 $2nd=\\left(m+\\dfrac12\\right)\\lambda$、最小は $m=0$ で $d=\\dfrac{\\lambda}{4n}$。",
                           f"$d\\fallingdotseq{t(d, 2)}\\,\\mathrm{{m}}$。"],
                    alt=["シャボン膜の場合と比べ、位相反転が2回あるので条件が入れかわる、と対比して確かめる。"],
                    pc=[("両方の反射で位相が反転することを判断している", 2), ("値が正しい", 2)], pit=["シャボン膜と同じ条件を使い、強め合いと弱め合いを取り違える。"])
    Lcm = r.choice([5, 10, 8, 12])
    Dum = r.choice([10, 20, 30, 50])
    Lr = sp.Rational(Lcm, 100)
    D = sp.Rational(Dum, 10 ** 6)
    dx = Lr * lam / (2 * D)
    return numq(f"2枚の平面ガラスを重ね、一端を接触させ、そこから {Lcm} cm 離れた他端に厚さ ${Dum}\\times10^{{-6}}\\,\\mathrm{{m}}$ の薄い紙をはさんで、くさび形の空気層をつくった。真上から波長 ${sig(lam, 2)}\\,\\mathrm{{m}}$ の光を当てて上から見ると、明暗の縞が見えた。隣り合う暗線の間隔は何 m か。",
                dx, f"{P(Lr)}*{P(lam)}/(2*{P(D)})", "空気層の厚さが $\\dfrac{\\lambda}{2}$ 変わるごとに縞が1本ずれる：$\\Delta x=\\dfrac{L\\lambda}{2D}$。", "m", n=2, d=4,
                ap="位置 $x$ での空気層の厚さは $\\dfrac{D}{L}x$。光路差 $2\\times$（厚さ）が $\\lambda$ 変わるごとに同じ明暗がくり返す。",
                steps=["位置 $x$ の厚さ $d=\\dfrac{D}{L}x$、光路差 $2d$。", "隣の暗線では $2\\Delta d=\\lambda$、$\\Delta d=\\dfrac{D}{L}\\Delta x$ より $\\Delta x=\\dfrac{L\\lambda}{2D}$。",
                       f"$\\Delta x=\\dfrac{{{dec(Lr)}\\times{sig(lam, 2)}}}{{2\\times{Dum}\\times10^{{-6}}}}\\fallingdotseq{t(dx, 2)}\\,\\mathrm{{m}}$。"],
                alt=["暗線の数を数えれば紙の厚さがわかる（$D=\\dfrac{\\lambda}{2}\\times$本数）という逆の使い方で、関係を確かめる。"],
                pc=[("厚さの変化と縞の関係を導いている", 2), ("値が正しい", 2)], pit=["光路差を往復の2倍にし忘れる。"])


@gen("standard_practice", 3, ["computation", "condition_check"])
def water_interf(r):
    kind = r.choice(["strong", "weak", "strong_anti"])
    while True:
        d = r.choice([6, 8, 9, 10, 12, 14])
        lam = r.choice([2, 3, 4, sp.Rational(5, 2)])
        q = sp.Rational(d) / lam
        if q.q != 1 and (2 * q).q != 1:
            break
    ns = 2 * int(sp.floor(q)) + 1
    nw = 2 * int(sp.floor(q + sp.Rational(1, 2)))
    if kind == "strong":
        return numq(f"水面上で {iv(d)} cm 離れた2点 $\\mathrm{{S_1}}$、$\\mathrm{{S_2}}$ から、同位相で波長 {iv(lam) if lam.q == 1 else dec(lam)} cm の波を送り出した。線分 $\\mathrm{{S_1S_2}}$ 上（両端を除く）で、波が強め合う点はいくつあるか。",
                    sp.Integer(ns), f"2*floor({d}/{P(lam)})+1", "線分上の点では経路差は $|2x-d|$ で、$-d$ から $d$ まで変化する。経路差 $=m\\lambda$ の点を数える。", "個", d=3,
                    ap="線分上の点 P について、$\\mathrm{S_1P}-\\mathrm{S_2P}$ は $-d<\\cdots<d$ の範囲の値をとる。その範囲に入る $m\\lambda$ の個数を数える。",
                    steps=[f"$|m\\lambda|<{d}$、すなわち $|m|<\\dfrac{{{d}}}{{{dec(lam)}}}={t(q, 3)}$。", f"$m=0,\\ \\pm1,\\ \\cdots,\\ \\pm{int(sp.floor(q))}$ の {ns} 個。"],
                    alt=["線分上では2つの波が逆向きに進んで定常波ができ、腹が半波長ごとに並ぶ。中点が腹なので、中点から半波長おきに腹を数えても同じ。"],
                    pc=[("経路差の範囲を考えている", 2), ("個数が正しい", 1)], pit=["$m$ の正の値だけを数える。"])
    if kind == "weak":
        return numq(f"水面上で {iv(d)} cm 離れた2点 $\\mathrm{{S_1}}$、$\\mathrm{{S_2}}$ から、同位相で波長 {iv(lam) if lam.q == 1 else dec(lam)} cm の波を送り出した。線分 $\\mathrm{{S_1S_2}}$ 上で、波が弱め合う点はいくつあるか。",
                    sp.Integer(nw), f"2*floor({d}/{P(lam)}+Rational(1,2))", "経路差 $=\\left(m+\\dfrac12\\right)\\lambda$ の点を、$-d$ から $d$ の範囲で数える。", "個", d=3,
                    ap="経路差が半波長の奇数倍になる点を数える。正負の両側に同じ数だけある。",
                    steps=[f"$\\left|m+\\dfrac12\\right|{dec(lam)}<{d}$。", f"条件を満たす $m+\\dfrac12$ は $\\pm\\dfrac12,\\ \\pm\\dfrac32,\\cdots$ のうち {nw} 個。"],
                    alt=["線分上の定常波で、節は腹と腹の中間にある。腹の数から節の数を数えても同じ。"],
                    pc=[("経路差の範囲を考えている", 2), ("個数が正しい", 1)], pit=["中点も弱め合うと数える。"])
    return numq(f"水面上で {iv(d)} cm 離れた2点 $\\mathrm{{S_1}}$、$\\mathrm{{S_2}}$ から、互いに逆位相で波長 {iv(lam) if lam.q == 1 else dec(lam)} cm の波を送り出した。線分 $\\mathrm{{S_1S_2}}$ 上で、波が強め合う点はいくつあるか。",
                sp.Integer(nw), f"2*floor({d}/{P(lam)}+Rational(1,2))", "逆位相の波源では、経路差 $=\\left(m+\\dfrac12\\right)\\lambda$ で強め合う。", "個", d=4,
                ap="波源が逆位相なら、強め合いと弱め合いの条件が入れかわる。",
                steps=["逆位相：強め合う条件は $|\\mathrm{S_1P}-\\mathrm{S_2P}|=\\left(m+\\dfrac12\\right)\\lambda$。", f"$\\left|m+\\dfrac12\\right|{dec(lam)}<{d}$ を満たす点は {nw} 個。"],
                alt=["中点では経路差 0 で、逆位相の波が出会うので弱め合う。中点が節になることから条件の入れかわりを確かめる。"],
                pc=[("逆位相で条件が入れかわることを用いている", 2), ("個数が正しい", 1)], pit=["同位相の場合の条件をそのまま使う。"])


@gen("standard_practice", 3, ["computation", "application", "cross_unit"], rel=["HS-MATH2-U04"])
def young_apps(r):
    kind = r.choice(["water", "plate", "white"])
    dmm = r.choice(["0.20", "0.25", "0.50"])
    Lm = r.choice(["1.0", "2.0", "1.5"])
    d, Lr = Q(dmm) / 1000, Q(Lm)
    if kind == "water":
        lam_nm = r.choice([480, 600, 640, 720])
        lam = sp.Rational(lam_nm, 10 ** 9)
        n = sp.Rational(4, 3)
        dx = Lr * lam / (n * d)
        return numq(f"ヤングの実験装置全体を屈折率 $\\dfrac43$ の水中に入れ、空気中での波長が ${sig(lam, 2)}\\,\\mathrm{{m}}$ の単色光を用いて実験した。スリット間隔 {dmm} mm、スリットとスクリーンの距離 {Lm} m のとき、隣り合う明線の間隔は何 m か。",
                    dx, f"{P(Lr)}*{P(lam)}/(Rational(4,3)*{P(d)})", "水中の波長は $\\dfrac{\\lambda}{n}$。$\\Delta x=\\dfrac{L\\lambda}{nd}$。", "m", n=2, d=3,
                    ap="媒質中では振動数は変わらず、波長が $\\dfrac{1}{n}$ 倍になる。",
                    steps=[f"水中の波長 $\\dfrac{{\\lambda}}{{n}}=\\dfrac34\\times{sig(lam, 2)}$。", f"$\\Delta x=\\dfrac{{L\\lambda}}{{nd}}\\fallingdotseq{t(dx, 2)}\\,\\mathrm{{m}}$。"],
                    alt=["空気中の間隔を先に求め、$\\dfrac34$ 倍しても同じ。"],
                    pc=[("水中の波長を用いている", 2), ("値が正しい", 2)], pit=["波長を $n$ 倍にする。"])
    if kind == "plate":
        lam_nm = r.choice([500, 600])
        lam = sp.Rational(lam_nm, 10 ** 9)
        n = r.choice(["1.5", "1.6", "1.4"])
        tum = r.choice([2, 3, 5, 6])
        tt = sp.Rational(tum, 10 ** 6)
        shift = (Q(n) - 1) * tt * Lr / d
        return numq(f"ヤングの実験で、スリット $\\mathrm{{S_1}}$ の直後を、厚さ ${tum}.0\\times10^{{-6}}\\,\\mathrm{{m}}$、屈折率 {n} の薄い透明板でおおった。スリット間隔 {dmm} mm、スクリーンまでの距離 {Lm} m とすると、干渉縞全体はどちらへ何 m ずれるか。ずれの大きさを答えなさい（向きは解説で述べる）。",
                    shift, f"({P(Q(n))}-1)*{P(tt)}*{P(Lr)}/{P(d)}", "板による光路差の増加 $(n-1)t$ を、幾何学的な経路差 $\\dfrac{dx}{L}$ で打ち消す位置に中央の明線が移る。", "m", n=2, d=4,
                    ap="中央の明線は光路差 0 の位置。$\\mathrm{S_1}$ 側の光路が $(n-1)t$ だけ長くなるので、幾何学的には $\\mathrm{S_1}$ 側に近い位置で光路差 0 になる。",
                    steps=["板による光路の増加は $nt-t=(n-1)t$。", "$\\mathrm{S_1}$ 側にずれた位置 $x$ で $\\dfrac{dx}{L}=(n-1)t$ となる。",
                           f"$x=\\dfrac{{(n-1)tL}}{{d}}\\fallingdotseq{t(shift, 2)}\\,\\mathrm{{m}}$（$\\mathrm{{S_1}}$ 側へずれる）。"],
                    alt=["ずれが明線間隔の何倍か（$\\dfrac{(n-1)t}{\\lambda}$ 倍）を計算すると、縞が何本分ずれたかがわかる。"],
                    pc=[("光路差の増加を求めている", 2), ("値が正しい", 2)], pit=["光路の増加を $nt$ とする。"])
    l1, l2 = 400, 700
    x1, x2 = Lr * sp.Rational(l1, 10 ** 9) / d, Lr * sp.Rational(l2, 10 ** 9) / d
    return numq(f"ヤングの実験で白色光を用いると、中央の明線の両側に色のついた縞が見える。スリット間隔 {dmm} mm、スクリーンまでの距離 {Lm} m のとき、1 番目の明線のうち、波長 $7.0\\times10^{{-7}}\\,\\mathrm{{m}}$ の赤い光と波長 $4.0\\times10^{{-7}}\\,\\mathrm{{m}}$ の紫の光の位置の差は何 m か。",
                x2 - x1, f"{P(Lr)}*(7*10**(-7)-4*10**(-7))/{P(d)}", "$x_1=\\dfrac{L\\lambda}{d}$ は波長に比例する。", "m", n=2, d=3,
                ap="1番目の明線の位置は波長に比例するので、赤（長い波長）ほど外側に現れる。",
                steps=[f"$x_{{\\text{{赤}}}}=\\dfrac{{L\\times7.0\\times10^{{-7}}}}{{d}}\\fallingdotseq{t(x2, 2)}\\,\\mathrm{{m}}$、$x_{{\\text{{紫}}}}\\fallingdotseq{t(x1, 2)}\\,\\mathrm{{m}}$。",
                       f"差 $\\fallingdotseq{t(x2 - x1, 2)}\\,\\mathrm{{m}}$。"],
                alt=["差は $\\dfrac{L(\\lambda_{\\text{赤}}-\\lambda_{\\text{紫}})}{d}$ で一度に計算できる。"],
                pc=[("波長ごとの明線の位置を求めている", 2), ("値が正しい", 2)], pit=["中央の明線にも色がつくと考える。"])


@gen("standard_practice", 3, ["computation", "condition_check"])
def refraction(r):
    kind = r.choice(["snell", "critical", "lam", "speed"])
    if kind == "snell":
        th1, n, th2, ntx = r.choice([(45, sp.sqrt(2), 30, "\\sqrt{2}"), (60, sp.sqrt(3), 30, "\\sqrt{3}"), (60, sp.sqrt(6) / 2, 45, "\\dfrac{\\sqrt{6}}{2}")])
        return numq(f"空気中から屈折率 ${ntx}$ の透明な物質の表面に、入射角 ${th1}^\\circ$ で光が入射した。屈折角は何度か。空気の屈折率を 1 とする。",
                    sp.Integer(th2), f"asin(sin(deg({th1}))/{P(n)})*180/pi", "屈折の法則 $\\sin\\theta_1=n\\sin\\theta_2$。", "度", d=2,
                    ap="屈折の法則 $n_1\\sin\\theta_1=n_2\\sin\\theta_2$。屈折率の大きい物質に入ると、法線に近づくように曲がる。",
                    steps=[f"$\\sin\\theta_2=\\dfrac{{\\sin{th1}^\\circ}}{{{ntx}}}={sp.latex(sp.nsimplify(sp.sin(sp.pi * th1 / 180) / n)).replace('frac', 'dfrac')}$。", f"$\\theta_2={th2}^\\circ$。"],
                    alt=["屈折角が入射角より小さいこと（法線に近づく）で、答えの大小を確かめる。"],
                    pc=[("屈折の法則を用いている", 2), ("角度が正しい", 2)], pit=["$\\sin\\theta_2=n\\sin\\theta_1$ と逆にする。"])
    if kind == "critical":
        n, ntx, th = r.choice([(sp.sqrt(2), "\\sqrt{2}", 45), (sp.Integer(2), "2.0", 30), (2 / sp.sqrt(3), "\\dfrac{2}{\\sqrt{3}}", 60)])
        return numq(f"屈折率 ${ntx}$ の透明な物質の中から空気との境界面に光が進むとき、全反射が起こる臨界角は何度か。空気の屈折率を 1 とする。",
                    sp.Integer(th), f"asin(1/{P(n)})*180/pi", "$n\\sin\\theta_c=1\\cdot\\sin90^\\circ$ より $\\sin\\theta_c=\\dfrac1n$。", "度", d=3,
                    ap="臨界角は屈折角が $90^\\circ$ になるときの入射角。屈折率の大きい側から小さい側へ進むときだけ全反射が起こる。",
                    steps=["$n\\sin\\theta_c=\\sin90^\\circ=1$。", f"$\\sin\\theta_c=\\dfrac{{1}}{{{ntx}}}$ より $\\theta_c={th}^\\circ$。"],
                    alt=["入射角が臨界角より大きいと、屈折の法則を満たす屈折角が存在しない（$\\sin\\theta_2>1$）ことから全反射を確かめる。"],
                    pc=[("全反射の条件を用いている", 2), ("角度が正しい", 2)], pit=["空気から物質に入る場合にも全反射が起こると考える。"])
    n = r.choice(["1.5", "1.33", "1.6", "2.4"])
    if kind == "lam":
        lam_nm = r.choice([480, 600, 630, 720])
        lam2 = sp.Rational(lam_nm, 10 ** 9) / Q(n)
        return numq(f"真空中での波長が ${sig(sp.Rational(lam_nm, 10 ** 9), 2)}\\,\\mathrm{{m}}$ の光が、屈折率 {n} の物質の中に入った。物質中での光の波長は何 m か。",
                    lam2, f"{lam_nm}*10**(-9)/{P(Q(n))}", "$\\lambda'=\\dfrac{\\lambda}{n}$（振動数は変わらない）。", "m", n=2, d=2,
                    ap="屈折率 $n$ の物質中では光の速さが $\\dfrac{c}{n}$ になり、振動数は変わらないので波長も $\\dfrac{1}{n}$ 倍。",
                    steps=["$\\lambda'=\\dfrac{\\lambda}{n}$。", f"$\\lambda'=\\dfrac{{{sig(sp.Rational(lam_nm, 10 ** 9), 2)}}}{{{n}}}\\fallingdotseq{t(lam2, 2)}\\,\\mathrm{{m}}$。"],
                    alt=["物質中の速さ $\\dfrac{c}{n}$ を振動数 $\\dfrac{c}{\\lambda}$ で割っても同じ。"],
                    pc=[("$\\lambda'=\\dfrac{\\lambda}{n}$ を用いている", 2), ("値が正しい", 2)], pit=["$n$ をかける。"])
    c = 3 * 10 ** 8
    v = c / Q(n)
    return numq(f"屈折率 {n} の物質中での光の速さは何 m/s か。真空中の光の速さを $3.0\\times10^8\\,\\mathrm{{m/s}}$ とする。",
                v, f"3*10**8/{P(Q(n))}", "$v=\\dfrac{c}{n}$。", "m/s", n=2, d=1,
                ap="絶対屈折率は「真空中の光の速さ ÷ 物質中の光の速さ」。",
                steps=["$v=\\dfrac{c}{n}$。", f"$v=\\dfrac{{3.0\\times10^8}}{{{n}}}\\fallingdotseq{t(v, 2)}\\,\\mathrm{{m/s}}$。"],
                alt=["屈折率が大きい物質ほど光が遅い（ダイヤモンド 2.4 では真空の半分以下）ことで、大小を確かめる。"],
                pc=[("屈折率の定義を用いている", 2), ("値が正しい", 2)], pit=["$c\\times n$ とする。"])


# ======================================================================
# C 思考力・記述応用
# ======================================================================

@gen("thinking_writing", 3, ["written_reasoning", "concept"])
def derive_c(r):
    kind = r.choice(["eq", "src", "obs", "young", "grating", "film"])
    if kind == "eq":
        return desc("原点 O の媒質が $y=A\\sin\\dfrac{2\\pi}{T}t$ で単振動し、その振動が速さ $v$ で $x$ 軸の正の向きに伝わっている。位置 $x$（$x>0$）の媒質の変位が $y=A\\sin2\\pi\\left(\\dfrac{t}{T}-\\dfrac{x}{\\lambda}\\right)$ と表されることを示しなさい。また、$x$ 軸の負の向きに進む場合の式を答えなさい。",
                    "振動が O から位置 $x$ まで伝わるのに時間 $\\dfrac{x}{v}$ かかるので、位置 $x$ の時刻 $t$ の変位は、O の時刻 $t-\\dfrac{x}{v}$ の変位に等しい。よって $y=A\\sin\\dfrac{2\\pi}{T}\\left(t-\\dfrac{x}{v}\\right)$。$vT=\\lambda$ より $\\dfrac{2\\pi}{T}\\cdot\\dfrac{x}{v}=\\dfrac{2\\pi x}{vT}=\\dfrac{2\\pi x}{\\lambda}$ なので $y=A\\sin2\\pi\\left(\\dfrac{t}{T}-\\dfrac{x}{\\lambda}\\right)$。負の向きに進む場合は、位置 $x$ の点が O より $\\dfrac{x}{v}$ だけ先に振動するので $y=A\\sin2\\pi\\left(\\dfrac{t}{T}+\\dfrac{x}{\\lambda}\\right)$。",
                    "位置 $x$ の点は、原点の振動を時間 $\\dfrac{x}{v}$ 遅れてまねる。",
                    [("伝わるのにかかる時間 $\\dfrac{x}{v}$ の遅れを用いている", 3), ("$vT=\\lambda$ を用いて式を書きかえている", 3), ("負の向きの場合を正しく答えている", 2)], d=3, p=8, kind="proof", lines=8,
                    ap="「位置 $x$ の現在＝原点の過去」と考える。",
                    steps=["遅れ $\\dfrac{x}{v}$。", "$t\\to t-\\dfrac{x}{v}$ と置きかえる。", "$v=\\dfrac{\\lambda}{T}$ で整理。"],
                    alt=["$t=0$ の波形を速さ $v$ で平行移動させると考えて、$y(x,t)=y(x-vt,0)$ から導いてもよい。"],
                    pc=[("遅れ", 3), ("書きかえ", 3), ("負の向き", 2)], pit=["遅れを $t+\\dfrac{x}{v}$ と逆にする。"],
                    chk=("expand(2*pi/s*(t-x/v)-2*pi*(t/s-x/(v*s)))", "0", "expand", "intermediate"))
    if kind == "src":
        return desc("振動数 $f$ の音を出す音源が、静止した観測者に向かって速さ $v$ で近づいている。音の速さを $V$ とするとき、観測者が聞く振動数が $f'=\\dfrac{V}{V-v}f$ となることを、音源の前方での波長の変化に注目して導きなさい。また、音源が近づいても音の速さが変わらない理由を述べなさい。",
                    "音源は1秒間に $f$ 個の波を出す。最初に出た波は1秒間に $V$ 進み、その間に音源は $v$ 進むので、1秒間に出た $f$ 個の波は長さ $V-v$ の区間に入る。前方の波長は $\\lambda'=\\dfrac{V-v}{f}$。観測者に届く音の速さは $V$ なので、$f'=\\dfrac{V}{\\lambda'}=\\dfrac{V}{V-v}f$。音の速さは媒質である空気の性質（温度など）で決まり、いったん空気中に出た音は音源の運動とは関係なく伝わるので、音源が動いても音の速さは変わらない。",
                    "$f$ 個の波が詰まる区間の長さを考える。",
                    [("1秒間の波の数と区間の長さ $V-v$ を正しく考えている", 3), ("波長と $f'$ の式を導いている", 3), ("音の速さが変わらない理由を媒質で説明している", 2)], d=3, p=8, kind="proof", lines=8,
                    ap="1秒間に出る波の数（$f$ 個）と、それが並ぶ長さに注目する。",
                    steps=["$f$ 個の波が長さ $V-v$。", "$\\lambda'=\\dfrac{V-v}{f}$。", "$f'=\\dfrac{V}{\\lambda'}$。"],
                    alt=["音源が1周期 $T$ の間に $vT$ 進むので、隣の波面との間隔が $VT-vT$ に縮む、と1周期で考えても同じ。"],
                    pc=[("区間の長さ", 3), ("導出", 3), ("理由", 2)], pit=["音の速さが $V+v$ になると考える。"],
                    chk=("simplify(a/((a-b)/c))", "a*c/(a-b)", None, "intermediate"))
    if kind == "obs":
        return desc("静止した音源が振動数 $f$ の音を出している。観測者が速さ $u$ で音源に近づくとき、観測者が聞く振動数が $f'=\\dfrac{V+u}{V}f$ となることを導きなさい（$V$ は音の速さ）。また、同じ速さ $u$ で音源が観測者に近づく場合と比べて、聞こえる振動数はどちらが大きいか、$V>u>0$ として示しなさい。",
                    "音源が静止しているので空気中の波長は $\\lambda=\\dfrac{V}{f}$ のまま。観測者に対する音の速さは $V+u$ になるので、観測者が1秒間に受け取る波の数は $f'=\\dfrac{V+u}{\\lambda}=\\dfrac{V+u}{V}f$。音源が近づく場合は $f''=\\dfrac{V}{V-u}f$。$\\dfrac{V}{V-u}-\\dfrac{V+u}{V}=\\dfrac{V^2-(V+u)(V-u)}{V(V-u)}=\\dfrac{u^2}{V(V-u)}>0$ なので、音源が近づく場合のほうが振動数は大きい。",
                    "観測者が動くと、波長は変わらず相対的な音の速さが変わる。",
                    [("波長が変わらないことと相対的な音の速さ $V+u$ を用いている", 3), ("$f'$ の式を導いている", 2), ("2つの場合の差を計算して大小を示している", 3)], d=4, p=8, kind="proof", lines=9, ps=["multiple_solutions"],
                    ap="観測者の立場では、音が速さ $V+u$ で向かってくるように見える。",
                    steps=["$\\lambda=\\dfrac{V}{f}$。", "$f'=\\dfrac{V+u}{\\lambda}$。", "差をとって通分。"],
                    alt=["$u$ が小さいとき両者はほぼ等しく（差は $u^2$ に比例）、$u$ が $V$ に近づくと音源が動く場合だけ振動数が非常に大きくなる、と極端な場合で確かめる。"],
                    pc=[("相対速度", 3), ("式", 2), ("比較", 3)], pit=["観測者が動いても波長が変わると考える。"],
                    chk=("simplify(a/(a-b)-(a+b)/a)", "b**2/(a*(a-b))", None, "intermediate"))
    if kind == "young":
        return desc("ヤングの実験で、スリット間隔を $d$、スリットとスクリーンの距離を $L$ とする。スクリーンの中央 O から距離 $x$ の点 P に届く2つの光の経路差が、$L$ が $d,\\ x$ に比べて十分大きいとき $\\dfrac{dx}{L}$ と近似できることを示し、隣り合う明線の間隔 $\\Delta x=\\dfrac{L\\lambda}{d}$ を導きなさい。",
                    "$\\mathrm{S_1P}=\\sqrt{L^2+\\left(x-\\dfrac{d}{2}\\right)^2}$、$\\mathrm{S_2P}=\\sqrt{L^2+\\left(x+\\dfrac{d}{2}\\right)^2}$。$\\mathrm{S_2P}^2-\\mathrm{S_1P}^2=2dx$ なので $\\mathrm{S_2P}-\\mathrm{S_1P}=\\dfrac{2dx}{\\mathrm{S_2P}+\\mathrm{S_1P}}$。$L\\gg d,\\ x$ のとき $\\mathrm{S_1P}+\\mathrm{S_2P}\\fallingdotseq2L$ なので、経路差 $\\fallingdotseq\\dfrac{dx}{L}$。明線の条件 $\\dfrac{dx}{L}=m\\lambda$ より $x_m=\\dfrac{mL\\lambda}{d}$、$\\Delta x=x_{m+1}-x_m=\\dfrac{L\\lambda}{d}$。",
                    "2乗の差をとってから近似する。",
                    [("2つの経路の長さを三平方の定理で表している", 2), ("差を $\\dfrac{2dx}{\\mathrm{S_1P}+\\mathrm{S_2P}}$ と変形し近似している", 4), ("明線の条件から間隔を導いている", 2)], d=4, p=8, kind="proof", lines=9,
                    ps=["cross_unit"], rel=["HS-MATH1-U04"],
                    ap="$\\sqrt{\\ }$ の差は扱いにくいので、$A-B=\\dfrac{A^2-B^2}{A+B}$ を使う。",
                    steps=["三平方の定理。", "$A^2-B^2=2dx$。", "$A+B\\fallingdotseq2L$。"],
                    alt=["P の方向と中心線のなす角 $\\theta$ を使い、経路差 $d\\sin\\theta$ と $\\sin\\theta\\fallingdotseq\\tan\\theta=\\dfrac{x}{L}$ で示してもよい。"],
                    pc=[("三平方", 2), ("近似", 4), ("間隔", 2)], pit=["近似の根拠を書かずに $\\dfrac{dx}{L}$ を用いる。"],
                    chk=("expand((x+d/2)**2-(x-d/2)**2)", "2*d*x", "expand", "intermediate"))
    if kind == "grating":
        return desc("格子定数 $d$ の回折格子に波長 $\\lambda$ の単色光を垂直に当てる。入射方向と角 $\\theta$ をなす方向で、隣り合うすじからの光の経路差が $d\\sin\\theta$ となることを説明し、明線の条件 $d\\sin\\theta=m\\lambda$ を導きなさい。また、ヤングの実験と比べて回折格子の明線が鋭く明るくなる理由を述べなさい。",
                    "格子から十分遠い点を見るとき、各すじから出る光はほぼ平行に進む。隣り合うすじから角 $\\theta$ の方向へ進む光の経路差は、間隔 $d$ と角 $\\theta$ でつくる直角三角形の辺 $d\\sin\\theta$ になる。これが波長の整数倍 $m\\lambda$ のとき、隣どうしが同位相になり、すべてのすじからの光が強め合うので $d\\sin\\theta=m\\lambda$ で明線となる。すじの数が多いと、条件から少しずれた方向では多数の光の位相が少しずつずれて打ち消し合うので、明線は細く鋭くなり、また多くの光が重なるので明るくなる。",
                    "隣どうしが同位相なら、すべてのすじが同位相になる。",
                    [("平行光と経路差 $d\\sin\\theta$ を説明している", 3), ("明線の条件を導いている", 2), ("多数のすじによって明線が鋭く明るくなる理由を述べている", 3)], d=4, p=8, lines=9,
                    ap="隣り合う2本だけを考えれば、全体の条件がわかる。",
                    steps=["平行光 → 経路差 $d\\sin\\theta$。", "$=m\\lambda$ で全体が同位相。", "多数のすじ → 鋭く明るい。"],
                    alt=["スリットが2本のヤングの実験の条件 $d\\sin\\theta=m\\lambda$ と同じ式であることを指摘し、違いは明線の幅と明るさにあると整理してもよい。"],
                    pc=[("経路差", 3), ("条件", 2), ("理由", 3)], pit=["隣り合うすじではなく両端のすじの経路差で条件を考える。"])
    return desc("空気中にある厚さ $d$、屈折率 $n$（$n>1$）のシャボン膜に、波長 $\\lambda$ の光を垂直に当てる。反射光が強め合う条件が $2nd=\\left(m+\\dfrac12\\right)\\lambda$（$m=0,1,2,\\cdots$）となることを、光路差と反射による位相の変化から説明しなさい。また、膜が非常に薄くなると反射光が暗く見える理由を述べなさい。",
                "膜の上面で反射する光①と、膜に入り下面で反射して戻る光②を比べる。②は膜の中を往復するので、光学距離の差（光路差）は $2nd$。①は空気（屈折率1）から膜（屈折率 $n$）への境界、すなわち屈折率の小さい側から大きい側への反射なので位相が $\\pi$ ずれる。②は膜から空気への反射なので位相は変わらない。反射による位相の差は半波長分なので、強め合う条件は $2nd+\\dfrac{\\lambda}{2}=(m+1)\\lambda$、すなわち $2nd=\\left(m+\\dfrac12\\right)\\lambda$。膜が非常に薄いと光路差 $2nd\\to0$ で、残るのは反射による半波長のずれだけなので、①と②は弱め合い、反射光は暗く見える。",
                "光路差 $2nd$ と、反射による半波長のずれを合わせて考える。",
                [("光路差が $2nd$ であることを説明している", 2), ("2つの反射での位相の変化の違いを説明している", 3), ("強め合う条件と、薄い膜で暗くなる理由を述べている", 3)], d=4, p=8, lines=9,
                ap="位相の変化：屈折率の小さい側→大きい側の反射で $\\pi$（固定端反射に相当）。",
                steps=["光路差 $2nd$。", "①で $\\pi$ ずれ、②はずれない。", "合わせて条件を立てる。"],
                alt=["ロープの波の固定端反射（山が谷になる）と自由端反射（山は山）にたとえて説明してもよい。"],
                pc=[("光路差", 2), ("位相", 3), ("条件と理由", 3)], pit=["位相の変化を両方の反射で考え、打ち消し合うとする。"])


@gen("thinking_writing", 3, ["multiple_solutions", "written_reasoning", "computation"])
def doppler_c(r):
    f, vs = r.choice([(576, 20), (288, 20), (720, 20), (285, 40), (570, 40), (432, 20)])
    f1 = sp.Rational(V * f, V - vs)
    f2 = sp.Rational(V * f, V + vs)
    return desc(f"線路のそばに立つ観測者のそばを、一定の振動数の警笛を鳴らし続けながら列車が一定の速さで通過した。列車が近づくときに聞こえた振動数は {t(f1)} Hz、遠ざかるときに聞こえた振動数は {t(f2)} Hz であった。" + VS +
                "（1）列車の速さ $v$ と、警笛の振動数 $f$ をそれぞれ求めなさい。（2）（1）の $f$ を、2つの観測値の比をとる方法とは別の方法でも求め、結果が一致することを確かめなさい。（3）列車の運転士には警笛が何 Hz に聞こえるか、理由とともに答えなさい。",
                f"（1）$\\dfrac{{f_1}}{{f_2}}=\\dfrac{{V+v}}{{V-v}}$ より $v=\\dfrac{{f_1-f_2}}{{f_1+f_2}}V={vs}\\,\\mathrm{{m/s}}$。$f=f_1\\dfrac{{V-v}}{{V}}={f}\\,\\mathrm{{Hz}}$。（2）$\\dfrac{{1}}{{f_1}}+\\dfrac{{1}}{{f_2}}=\\dfrac{{(V-v)+(V+v)}}{{Vf}}=\\dfrac{{2}}{{f}}$ より $f=\\dfrac{{2f_1f_2}}{{f_1+f_2}}={f}\\,\\mathrm{{Hz}}$ で一致する。（3）{f} Hz。運転士は音源とともに動いていて、音源との相対的な運動がないので、ドップラー効果は起こらない。",
                "近づくとき $f_1=\\dfrac{V}{V-v}f$、遠ざかるとき $f_2=\\dfrac{V}{V+v}f$。比をとると $f$ が消える。",
                [("（1）2つのドップラー効果の式を立てている", 2), ("（1）比から $v$、さらに $f$ を求めている", 2), ("（2）別の方法で $f$ を求めて一致を確かめている", 2), ("（3）相対運動がないことから答えている", 2)], d=4, p=8, lines=10,
                ap="未知数は $v$ と $f$ の2つ。2つの観測値から2本の式をつくる。",
                steps=[f"$f_1=\\dfrac{{{V}}}{{{V}-v}}f={t(f1)}$、$f_2=\\dfrac{{{V}}}{{{V}+v}}f={t(f2)}$。", f"比：$\\dfrac{{{V}+v}}{{{V}-v}}=\\dfrac{{{t(f1)}}}{{{t(f2)}}}$ → $v={vs}\\,\\mathrm{{m/s}}$。",
                       f"$f={t(f1)}\\times\\dfrac{{{V}-{vs}}}{{{V}}}={f}\\,\\mathrm{{Hz}}$。"],
                alt=["（2）の方法のほか、近づくときの前方の波長 $\\dfrac{V}{f_1}$ と遠ざかるときの後方の波長 $\\dfrac{V}{f_2}$ の平均が、静止時の波長 $\\dfrac{V}{f}$ になることから $f$ を求めることもできる。"],
                pc=[("（1）式", 2), ("（1）値", 2), ("（2）", 2), ("（3）", 2)], pit=["2つの観測値の単純平均を $f$ とする（正しくは調和平均）。"],
                chk=(f"2*{P(f1)}*{P(f2)}/({P(f1)}+{P(f2)})", str(f), None, "intermediate"))


@gen("thinking_writing", 2, ["cross_unit", "written_reasoning", "computation"], rel=["HS-MATH2-U04"])
def young_c(r):
    dmm, Lm, lam_nm = r.choice([("0.30", "1.5", 600), ("0.20", "1.0", 500), ("0.50", "2.0", 625), ("0.25", "1.0", 600), ("0.40", "2.0", 480)])
    d, Lr, lam = Q(dmm) / 1000, Q(Lm), sp.Rational(lam_nm, 10 ** 9)
    dx = Lr * lam / d
    xm = 3 * dx
    theta_ratio = xm / Lr
    return desc(f"ヤングの実験で、間隔 {dmm} mm の2つのスリットに波長 ${sig(lam, 3)}\\,\\mathrm{{m}}$ の単色光を当て、スリットから {Lm} m 離れたスクリーン上に干渉縞をつくった。"
                "（1）隣り合う明線の間隔を求めなさい。（2）中央から3番目の明線の位置 $x_3$ と、その方向の角 $\\theta$ について $\\tan\\theta=\\dfrac{x_3}{L}$ の値を求め、経路差を $\\dfrac{dx}{L}$ と近似してよい理由を述べなさい。（3）光源を、波長がより長い光に変えると縞の間隔はどうなるか、理由とともに答えなさい。数値は有効数字2桁で答えなさい。",
                f"（1）$\\Delta x=\\dfrac{{L\\lambda}}{{d}}\\fallingdotseq{t(dx, 2)}\\,\\mathrm{{m}}$　（2）$x_3=3\\Delta x\\fallingdotseq{t(xm, 2)}\\,\\mathrm{{m}}$、$\\tan\\theta=\\dfrac{{x_3}}{{L}}\\fallingdotseq{t(theta_ratio, 2)}$。角がきわめて小さいので $\\sin\\theta\\fallingdotseq\\tan\\theta$ とみなせ、経路差 $d\\sin\\theta\\fallingdotseq\\dfrac{{dx}}{{L}}$ と近似できる。（3）$\\Delta x=\\dfrac{{L\\lambda}}{{d}}$ は波長に比例するので、間隔は広くなる。",
                "$\\Delta x=\\dfrac{L\\lambda}{d}$。角が小さいことを数値で確かめる。",
                [("（1）間隔を単位をそろえて求めている", 2), ("（2）$x_3$ と $\\tan\\theta$ を求めている", 2), ("（2）$\\sin\\theta\\fallingdotseq\\tan\\theta$ の近似の根拠を述べている", 2), ("（3）波長との比例関係から答えている", 2)], d=4, p=8, lines=10,
                fig=figure("ヤングの実験。間隔 d の2つのスリットと、距離 L 離れたスクリーン上の点 P", young_svg()),
                ap="三角関数の近似：角 $\\theta$（rad）が小さいとき $\\sin\\theta\\fallingdotseq\\tan\\theta\\fallingdotseq\\theta$。",
                steps=[f"（1）$\\Delta x=\\dfrac{{{Lm}\\times{sig(lam, 3)}}}{{{dmm}\\times10^{{-3}}}}\\fallingdotseq{t(dx, 2)}\\,\\mathrm{{m}}$。", f"（2）$\\tan\\theta\\fallingdotseq{t(theta_ratio, 2)}$（角はおよそ ${t(theta_ratio * 180 / sp.pi, 2)}^\\circ$）。",
                       "（3）$\\lambda$ が大きいほど $\\Delta x$ は大きい。"],
                alt=["（2）は、$\\sin\\theta$ と $\\tan\\theta$ の差が $\\theta^3$ 程度の大きさしかないことを、三角関数のグラフ（原点付近で $y=x$ に接する）から説明してもよい。"],
                pc=[("（1）", 2), ("（2）値", 2), ("（2）近似", 2), ("（3）", 2)], pit=["mm を m に直し忘れる。", "近似の理由を「L が大きいから」だけで済ませる。"],
                chk=(f"{P(Lr)}*{P(lam)}/{P(d)}", str(sp.nsimplify(dx)), None, "intermediate"))


@gen("thinking_writing", 2, ["condition_check", "written_reasoning", "computation"])
def grating_c(r):
    N = r.choice([300, 400, 500, 600])
    d = sp.Rational(1, N * 1000)
    lr, lv = 700, 400
    m_r = int(sp.floor(d / sp.Rational(lr, 10 ** 9)))
    m_v = int(sp.floor(d / sp.Rational(lv, 10 ** 9)))
    s2r = 2 * sp.Rational(lr, 10 ** 9) / d
    s3v = 3 * sp.Rational(lv, 10 ** 9) / d
    overlap = s3v < s2r
    tail = "3次の紫の明線は2次の赤の明線より内側に現れるので、2次と3次のスペクトルは重なる。" if overlap else "3次の紫の明線は2次の赤の明線より外側に現れるので、2次と3次のスペクトルは重ならない。"
    if s2r >= 1 or s3v >= 1:
        tail = "2次の赤または3次の紫の明線のどちらかは $\\sin\\theta\\geqq1$ となり観測されないので、重なりは起こらない（観測できる次数の範囲で判断する）。"
    return desc(f"1 mm あたり {N} 本のすじがある回折格子に、波長 $4.0\\times10^{{-7}}\\,\\mathrm{{m}}$（紫）から $7.0\\times10^{{-7}}\\,\\mathrm{{m}}$（赤）までの光を含む白色光を垂直に当てた。"
                "（1）格子定数を求めなさい。（2）赤い光（$7.0\\times10^{-7}\\,\\mathrm{m}$）と紫の光（$4.0\\times10^{-7}\\,\\mathrm{m}$）について、片側で観測できる明線は最大で何次までか、それぞれ求めなさい。（3）2次の赤い光と3次の紫の光の $\\sin\\theta$ を比べ、2次と3次のスペクトルが重なるかどうかを判断しなさい。",
                f"（1）$d={sig(d, 2)}\\,\\mathrm{{m}}$　（2）赤：{m_r} 次まで、紫：{m_v} 次まで（$m<\\dfrac{{d}}{{\\lambda}}$）　（3）2次の赤：$\\sin\\theta=\\dfrac{{2\\lambda_{{\\text{{赤}}}}}}{{d}}={t(s2r, 2)}$、3次の紫：$\\sin\\theta=\\dfrac{{3\\lambda_{{\\text{{紫}}}}}}{{d}}={t(s3v, 2)}$。{tail}",
                "$\\sin\\theta=\\dfrac{m\\lambda}{d}$ は波長と次数の積で決まる。",
                [("（1）格子定数を求めている", 2), ("（2）$\\sin\\theta<1$ の条件で次数の上限を求めている", 3), ("（3）$\\sin\\theta$ を比べて重なりを正しく判断している", 3)], d=5, p=8, lines=10,
                ap="明線の方向は $m\\lambda$ の値で決まる。$2\\times700$ と $3\\times400$ のように、次数×波長を比べればよい。",
                steps=[f"（1）$d=\\dfrac{{1\\times10^{{-3}}}}{{{N}}}={sig(d, 2)}\\,\\mathrm{{m}}$。", f"（2）$\\dfrac{{d}}{{\\lambda_{{\\text{{赤}}}}}}={t(d / sp.Rational(lr, 10 ** 9), 3)}$、$\\dfrac{{d}}{{\\lambda_{{\\text{{紫}}}}}}={t(d / sp.Rational(lv, 10 ** 9), 3)}$。",
                       "（3）$m\\lambda$ の大小で方向の大小が決まる。"],
                alt=["$d$ によらず $2\\times7.0\\times10^{-7}>3\\times4.0\\times10^{-7}$ なので、両方が観測できる限り2次と3次は必ず重なる、と一般的に示すこともできる。"],
                pc=[("（1）", 2), ("（2）", 3), ("（3）", 3)], pit=["次数の上限で $\\dfrac{d}{\\lambda}$ を四捨五入する。", "波長の大小だけで判断し、次数を考えない。"],
                chk=(f"3*4*10**(-7)/{P(d)}", str(s3v), None, "intermediate"))


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(stem, wrong, step, etype, tempt, fix, ans, expl, steps, ap, alt, pit, chk=None, d=3, **kw):
    return desc(f"{stem}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい答えを求めなさい。", ans, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい解答を途中式とともに示している", 3), ("最終的な答えが正しい", 1)], d=d, p=6, lines=6,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい途中式", 3), ("正しい答え", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix), chk=chk, **kw)


@gen("error_correction", 3, ["common_error", "condition_check"])
def err_doppler(r):
    kind = r.choice(["sign", "obs", "reflect"])
    if kind == "sign":
        while True:
            f = r.choice([480, 600, 640, 680, 800])
            vs = r.choice([20, 40, 60])
            fp = sp.Rational(V * f, V - vs)
            if fp.q == 1:
                break
        bad = sp.Rational(V * f, V + vs)
        return err_item(f"振動数 {f} Hz の音源が、静止した観測者に速さ {vs} m/s で近づいている。観測者が聞く振動数を求めなさい。" + VS,
                        f"$f'=\\dfrac{{V}}{{V+v}}f=\\dfrac{{{V}}}{{{V}+{vs}}}\\times{f}\\fallingdotseq{t(bad, 3)}\\,\\mathrm{{Hz}}$", "分母を $V+v$ とした部分", "sign",
                        "公式の形だけを覚えていて、「音源から観測者へ向かう向きを正」という符号の約束を確認していない。",
                        f"近づく音源は $v=+{vs}$。$f'=\\dfrac{{{V}}}{{{V}-{vs}}}\\times{f}={t(fp)}\\,\\mathrm{{Hz}}$", f"${t(fp)}\\,\\mathrm{{Hz}}$",
                        "音源が近づくと前方の波長が縮み、振動数は大きくなる。",
                        [f"正の向き：音源→観測者。$v=+{vs}$。", f"$f'=\\dfrac{{V}}{{V-v}}f={t(fp)}\\,\\mathrm{{Hz}}$。"],
                        "近づくなら高く聞こえる、という定性的な結論と答えの大小を照合する。",
                        [f"生徒の答え {t(bad, 3)} Hz はもとの {f} Hz より低く、近づく音源で音が低くなるという結果は経験と矛盾する。"], ["式の前に図と正の向きをかく。"],
                        chk=(f"{V}*{f}/({V}-{vs})", str(fp), None, "intermediate"), d=2)
    if kind == "obs":
        while True:
            f = r.choice([510, 680, 850, 1020])
            u = r.choice([20, 34, 68])
            fp = sp.Rational((V + u) * f, V)
            if fp.q == 1:
                break
        bad = sp.Rational(V * f, V - u)
        return err_item(f"静止した音源が振動数 {f} Hz の音を出している。観測者が速さ {u} m/s で音源に近づくとき、観測者が聞く振動数を求めなさい。" + VS,
                        f"近づくので $f'=\\dfrac{{V}}{{V-u}}f=\\dfrac{{{V}}}{{{V}-{u}}}\\times{f}\\fallingdotseq{t(bad, 3)}\\,\\mathrm{{Hz}}$",
                        "音源が近づく場合の式を使った部分", "formula",
                        "「近づけば高くなる」という結果だけを覚え、音源が動く場合（波長が変わる）と観測者が動く場合（相対的な音の速さが変わる）の違いを区別していない。",
                        f"観測者が動く場合は波長は変わらず、相対的な音の速さが $V+u$。$f'=\\dfrac{{{V}+{u}}}{{{V}}}\\times{f}={t(fp)}\\,\\mathrm{{Hz}}$",
                        f"${t(fp)}\\,\\mathrm{{Hz}}$", "観測者が動く → 分子が変わる。音源が動く → 分母が変わる。",
                        [f"$\\lambda=\\dfrac{{{V}}}{{{f}}}$（変わらない）。", f"$f'=\\dfrac{{V+u}}{{\\lambda}}={t(fp)}\\,\\mathrm{{Hz}}$。"],
                        "何が動いているかを確かめ、変化するのが波長か相対速度かを判断する。",
                        ["一般式 $f'=\\dfrac{V-u}{V-v}f$ に、$v=0$、$u=-" + str(u) + "$（音源から観測者へ向かう向きが正）を代入しても同じ結果になる。"], ["一般式で符号を代入する。"],
                        chk=(f"({V}+{u})*{f}/{V}", str(fp), None, "intermediate"))
    while True:
        f = r.choice([500, 680, 850, 1000])
        u = r.choice([10, 17, 20])
        f2 = sp.Rational(f * (V + u), V - u)
        if f2.q == 1:
            break
    f1 = sp.Rational(f * (V + u), V)
    return err_item(f"静止した音源から振動数 {f} Hz の音を出し、速さ {u} m/s で音源に近づく反射板に当てた。音源の位置で聞く反射音の振動数を求めなさい。" + VS,
                    f"反射板は近づく観測者なので $f'=\\dfrac{{{V}+{u}}}{{{V}}}\\times{f}\\fallingdotseq{t(f1, 3)}\\,\\mathrm{{Hz}}$。反射音はこの振動数で戻ってくる。",
                    "反射板が音を出す段階のドップラー効果を考えていない部分", "concept",
                    "反射板で音が「はね返るだけ」と考え、反射板が動く音源として音を出し直していることを見落としている。",
                    f"反射板は振動数 $f_1=\\dfrac{{{V}+{u}}}{{{V}}}\\times{f}$ の音を出しながら近づく音源になる。$f_2=\\dfrac{{{V}}}{{{V}-{u}}}f_1={t(f2)}\\,\\mathrm{{Hz}}$",
                    f"${t(f2)}\\,\\mathrm{{Hz}}$", "動く反射板は「観測者」として受け取り、「音源」として出し直す。2回のドップラー効果。",
                    [f"受け取り：$f_1=\\dfrac{{{V}+{u}}}{{{V}}}\\times{f}$。", f"出し直し：$f_2=\\dfrac{{{V}}}{{{V}-{u}}}f_1={t(f2)}\\,\\mathrm{{Hz}}$。"],
                    "反射の各段階で、誰が音源で誰が観測者かを確認する。",
                    ["$f_2=\\dfrac{V+u}{V-u}f$ にまとめると、$u\\ll V$ のとき $f_2-f\\fallingdotseq\\dfrac{2u}{V}f$ となり、スピードガンの原理（変化が速さに比例）とも一致する。"], ["反射は2段階で考える。"],
                    chk=(f"{f}*({V}+{u})/({V}-{u})", str(f2), None, "intermediate"))


@gen("error_correction", 3, ["common_error", "concept"])
def err_wave(r):
    kind = r.choice(["vlt", "medium", "phase"])
    As, Ts, Ls = r.choice(WAVES)
    if kind == "vlt":
        v = Q(Ls) / Q(Ts)
        return err_item(f"$x$ 軸の正の向きに進む正弦波が ${wave_tex(As, Ts, Ls)}$〔m〕（$t$ は s、$x$ は m）で表される。この波の速さを求めなさい。",
                        f"$T={Ts}$、$\\lambda={Ls}$ なので $v=\\lambda T={Ls}\\times{Ts}={dec(Q(Ls) * Q(Ts))}\\,\\mathrm{{m/s}}$", "$v=\\lambda T$ とした部分", "formula",
                        "$v=f\\lambda$ を覚えているが、$f$ と $T$ の関係（逆数）を確認せずに $T$ をかけている。",
                        f"$v=f\\lambda=\\dfrac{{\\lambda}}{{T}}=\\dfrac{{{Ls}}}{{{Ts}}}={t(v)}\\,\\mathrm{{m/s}}$", f"${t(v)}\\,\\mathrm{{m/s}}$",
                        "1周期の間に1波長進むので $v=\\dfrac{\\lambda}{T}$。",
                        [f"$T={Ts}\\,\\mathrm{{s}}$、$\\lambda={Ls}\\,\\mathrm{{m}}$。", f"$v=\\dfrac{{\\lambda}}{{T}}={t(v)}\\,\\mathrm{{m/s}}$。"],
                        "単位で確かめる：$\\mathrm{m}\\times\\mathrm{s}$ は速さの単位にならない。",
                        ["式の位相 $\\dfrac{t}{T}-\\dfrac{x}{\\lambda}$ が一定の点の速さを求めると $\\dfrac{\\lambda}{T}$ になることで確かめる。"], ["単位を書いて計算する。"],
                        chk=(f"{P(Q(Ls))}/{P(Q(Ts))}", str(v), None, "intermediate"), d=2)
    if kind == "medium":
        lam_nm = r.choice([480, 600, 660])
        n = r.choice(["1.5", "1.2", "1.6"])
        lam2 = sp.Rational(lam_nm, 10 ** 9) / Q(n)
        bad = sp.Rational(lam_nm, 10 ** 9) * Q(n)
        return err_item(f"真空中での波長が ${sig(sp.Rational(lam_nm, 10 ** 9), 2)}\\,\\mathrm{{m}}$ の光が、屈折率 {n} のガラスの中に入った。ガラス中での波長を求めなさい。",
                        f"屈折率の分だけ大きくなるので ${sig(sp.Rational(lam_nm, 10 ** 9), 2)}\\times{n}\\fallingdotseq{t(bad, 2)}\\,\\mathrm{{m}}$", "屈折率をかけた部分", "concept",
                        "「光学距離＝$n\\times$距離」と「媒質中の波長」を混同し、どちらに $n$ をかけるのかを区別していない。",
                        f"振動数は変わらず速さが $\\dfrac{{c}}{{n}}$ になるので、波長も $\\dfrac{{1}}{{n}}$ 倍。$\\dfrac{{{sig(sp.Rational(lam_nm, 10 ** 9), 2)}}}{{{n}}}\\fallingdotseq{t(lam2, 2)}\\,\\mathrm{{m}}$",
                        f"${t(lam2, 2)}\\,\\mathrm{{m}}$", "媒質中では $\\lambda'=\\dfrac{\\lambda}{n}$。光学距離 $nl$ は「真空中なら何 m に相当するか」を表す別の量。",
                        ["$v=\\dfrac{c}{n}$、$f$ は不変。", f"$\\lambda'=\\dfrac{{v}}{{f}}=\\dfrac{{\\lambda}}{{n}}\\fallingdotseq{t(lam2, 2)}\\,\\mathrm{{m}}$。"],
                        "$v=f\\lambda$ に立ち返り、何が変わって何が変わらないかを確認する。",
                        ["光が遅くなるのに、1周期の間に進む距離（波長）が長くなるのは不自然、と気づけば誤りがわかる。"], ["$v=f\\lambda$ に立ち返る。"],
                        chk=(f"{lam_nm}*10**(-9)/{P(Q(n))}", str(lam2), None, "intermediate"), d=2)
    L = Q(Ls)
    dxk = r.choice([sp.Rational(1, 2), sp.Rational(1, 4), sp.Rational(3, 4)])
    dx = L * dxk
    ph = 2 * dxk
    return err_item(f"$x$ 軸の正の向きに進む正弦波が ${wave_tex(As, Ts, Ls)}$〔m〕（$t$ は s、$x$ は m）で表される。$x$ 軸上で {dec(dx)} m 離れた2点の振動の位相差を求めなさい。",
                    f"位相差は $\\pi\\times\\dfrac{{\\Delta x}}{{\\lambda}}=\\pi\\times\\dfrac{{{dec(dx)}}}{{{Ls}}}={dec(dxk)}\\pi$", "1波長で位相が $\\pi$ ずれるとした部分", "formula",
                    "半波長で逆位相（位相差 $\\pi$）になることと、1波長で位相差 $2\\pi$ になることを混同している。",
                    f"1波長で $2\\pi$ ずれるので $2\\pi\\times\\dfrac{{{dec(dx)}}}{{{Ls}}}={t(ph)}\\pi$", f"${t(ph)}\\pi$",
                    "位相差 $=2\\pi\\dfrac{\\Delta x}{\\lambda}$。",
                    [f"$\\dfrac{{\\Delta x}}{{\\lambda}}={dec(dxk)}$。", f"位相差 $=2\\pi\\times{dec(dxk)}={t(ph)}\\pi$。"],
                    "1波長離れた点は同じ振動をする（位相差 $2\\pi$）ことを基準に確かめる。",
                    ["式の中の $2\\pi\\dfrac{x}{\\lambda}$ に $x$ の差を代入すれば、位相差が直接得られる。"], ["式から位相差を読む。"],
                    chk=(f"2*{P(dx)}/{P(L)}", str(ph), None, "intermediate"), d=2)


@gen("error_correction", 2, ["common_error", "condition_check"])
def err_interf(r):
    kind = r.choice(["film", "young"])
    if kind == "film":
        lam_nm = r.choice([480, 600, 640])
        n = r.choice(["1.2", "1.5", "1.6"])
        lam = sp.Rational(lam_nm, 10 ** 9)
        d = lam / (4 * Q(n))
        bad = lam / (2 * Q(n))
        return err_item(f"空気中にある屈折率 {n} の薄膜に、波長 ${sig(lam, 2)}\\,\\mathrm{{m}}$ の光を垂直に当てた。反射光が強め合う最小の膜の厚さを求めなさい。",
                        f"強め合う条件は $2nd=m\\lambda$。最小は $m=1$ で $d=\\dfrac{{\\lambda}}{{2n}}\\fallingdotseq{t(bad, 2)}\\,\\mathrm{{m}}$", "強め合う条件を $2nd=m\\lambda$ とした部分", "condition",
                        "2波源の干渉条件（経路差＝$m\\lambda$）をそのまま当てはめ、膜の上面での反射で位相が反転することを考えていない。",
                        f"上面の反射（空気→膜）で位相が $\\pi$ ずれるので、強め合う条件は $2nd=\\left(m+\\dfrac12\\right)\\lambda$。最小は $m=0$ で $d=\\dfrac{{\\lambda}}{{4n}}\\fallingdotseq{t(d, 2)}\\,\\mathrm{{m}}$",
                        f"${t(d, 2)}\\,\\mathrm{{m}}$", "光の干渉では、光路差に加えて反射による位相の変化を必ず確認する。",
                        ["反射①：小→大で位相反転。反射②：大→小で反転なし。", f"$2nd=\\dfrac{{\\lambda}}{{2}}$ より $d={t(d, 2)}\\,\\mathrm{{m}}$。"],
                        "反射のたびに、屈折率の大小を確かめて位相の変化を書き込む。",
                        ["生徒の厚さでは $2nd=\\lambda$ となり、位相反転を合わせると半波長ずれて弱め合う。実際には暗く見えるはずで矛盾する。"], ["反射の位相変化を図に書き込む。"],
                        chk=(f"{P(lam)}/(4*{P(Q(n))})", str(d), None, "intermediate"))
    dmm, Lm, lam_nm = r.choice([("0.20", "1.0", 600), ("0.50", "2.0", 500), ("0.25", "1.5", 500)])
    d, Lr, lam = Q(dmm) / 1000, Q(Lm), sp.Rational(lam_nm, 10 ** 9)
    dx = Lr * lam / d
    bad = d * lam / Lr
    return err_item(f"ヤングの実験で、スリット間隔 {dmm} mm、スリットとスクリーンの距離 {Lm} m、光の波長 ${sig(lam, 2)}\\,\\mathrm{{m}}$ のとき、隣り合う明線の間隔を求めなさい。",
                    f"$\\Delta x=\\dfrac{{d\\lambda}}{{L}}=\\dfrac{{{dmm}\\times10^{{-3}}\\times{sig(lam, 2)}}}{{{Lm}}}\\fallingdotseq{t(bad, 2)}\\,\\mathrm{{m}}$", "$d$ と $L$ を入れかえた部分", "formula",
                    "式の形を導出なしで覚えたため、どの量が分母に来るかを取り違えている。",
                    f"$\\Delta x=\\dfrac{{L\\lambda}}{{d}}=\\dfrac{{{Lm}\\times{sig(lam, 2)}}}{{{dmm}\\times10^{{-3}}}}\\fallingdotseq{t(dx, 2)}\\,\\mathrm{{m}}$",
                    f"${t(dx, 2)}\\,\\mathrm{{m}}$", "経路差 $\\dfrac{dx}{L}=m\\lambda$ から導けば、$x=\\dfrac{mL\\lambda}{d}$ となる。",
                    ["明線の条件 $\\dfrac{dx}{L}=m\\lambda$。", f"$\\Delta x=\\dfrac{{L\\lambda}}{{d}}\\fallingdotseq{t(dx, 2)}\\,\\mathrm{{m}}$。"],
                    "経路差の式から導き直して確かめる。",
                    ["生徒の値はおよそ $10^{-10}\\,\\mathrm{m}$ で、原子の大きさ程度の縞は目で見えない。実際の縞は mm 程度であり、桁の点からも誤りとわかる。"], ["答えの桁が現実的か確かめる。"],
                    chk=(f"{P(Lr)}*{P(lam)}/{P(d)}", str(dx), None, "intermediate"), d=2)


@gen("error_correction", 2, ["common_error", "computation"])
def err_grating(r):
    kind = r.choice(["conv", "max"])
    N = r.choice([250, 400, 500])
    d = sp.Rational(1, N * 1000)
    if kind == "conv":
        lam_nm = r.choice([500, 600])
        lam = sp.Rational(lam_nm, 10 ** 9)
        s = lam / d
        return err_item(f"1 mm あたり {N} 本のすじがある回折格子に、波長 ${sig(lam, 2)}\\,\\mathrm{{m}}$ の光を垂直に当てた。1 次の明線の方向 $\\theta$ について $\\sin\\theta$ を求めなさい。",
                        f"格子定数は $d={N}\\,\\mathrm{{mm}}={N}\\times10^{{-3}}\\,\\mathrm{{m}}$。$\\sin\\theta=\\dfrac{{\\lambda}}{{d}}=\\dfrac{{{sig(lam, 2)}}}{{{N}\\times10^{{-3}}}}$", "格子定数を本数そのものとした部分", "unit",
                        "「1 mm あたり $N$ 本」を、すじの間隔と取り違えている。",
                        f"$d=\\dfrac{{1}}{{{N}}}\\,\\mathrm{{mm}}={t(d, 2)}\\,\\mathrm{{m}}$。$\\sin\\theta=\\dfrac{{\\lambda}}{{d}}={t(s)}$",
                        f"${t(s)}$", "1 mm を本数で割ったものが間隔。",
                        [f"$d=\\dfrac{{1\\times10^{{-3}}}}{{{N}}}={t(d, 2)}\\,\\mathrm{{m}}$。", f"$\\sin\\theta=\\dfrac{{{sig(lam, 2)}}}{{{t(d, 2)}}}={t(s)}$。"],
                        "本数が多いほど間隔は狭い、という関係を確認する。",
                        ["生徒の値では $\\sin\\theta$ がきわめて小さく、明線がほぼ中央に重なってしまう。実際の回折格子では明線は大きく離れて見えるので矛盾する。"], ["単位と意味を確認してから換算する。"],
                        chk=(f"{P(lam)}/{P(d)}", str(s), None, "intermediate"), d=2)
    lam_nm = 500
    lam = sp.Rational(lam_nm, 10 ** 9)
    q = d / lam
    mmax = int(sp.floor(q)) - (1 if q.q == 1 else 0)
    return err_item(f"1 mm あたり {N} 本のすじがある回折格子に、波長 $5.0\\times10^{{-7}}\\,\\mathrm{{m}}$ の光を垂直に当てた。片側で観測できる明線は最大で何次までか。",
                    f"$\\dfrac{{d}}{{\\lambda}}={t(q, 3)}$ なので、{'四捨五入して' if q.q != 1 else ''} {int(sp.ceiling(q)) if q.q != 1 else int(q)} 次まで観測できる",
                    "$m=\\dfrac{d}{\\lambda}$ の値をそのまま（または四捨五入して）上限とした部分", "condition",
                    "$\\sin\\theta\\leqq1$ の条件を等号を含めて扱い、$\\theta=90^\\circ$（スクリーンに届かない方向）や、条件を超える次数を含めてしまっている。",
                    f"$\\sin\\theta=\\dfrac{{m\\lambda}}{{d}}<1$ より $m<{t(q, 3)}$。最大は {mmax} 次",
                    f"{mmax} 次", "明線が観測される方向は $\\sin\\theta<1$ を満たす必要がある。",
                    [f"$m<\\dfrac{{d}}{{\\lambda}}={t(q, 3)}$。", f"最大の整数 $m={mmax}$。"],
                    "求めた次数で $\\sin\\theta$ を計算し、1 未満になることを確かめる。",
                    [f"$m={mmax + 1}$ を代入すると $\\sin\\theta={t((mmax + 1) / q, 3)}\\geqq1$ となり、その方向は存在しない。"], ["不等号の等号の有無を確認する。"],
                    chk=(f"floor({P(d)}/{P(lam)}-Rational(1,10**9))", str(mmax), None, "intermediate"), d=3)


GENERATORS = [wave_eq_basic, doppler_basic, interference_basic, young_basic, grating_basic, concept_mc,
              doppler_apps, wave_graph, thin_film, water_interf, young_apps, refraction,
              derive_c, doppler_c, young_c, grating_c,
              err_doppler, err_wave, err_interf, err_grating]
