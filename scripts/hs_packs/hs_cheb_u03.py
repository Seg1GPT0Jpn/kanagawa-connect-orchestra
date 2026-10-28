"""単元パック：化学基礎 酸と塩基・酸化還元（pH・中和滴定・酸化数・電池）。"""
import math
import re
from decimal import ROUND_HALF_UP, Decimal

import sympy as sp

from banks._common import desc, figure, mc, num, plane, sa
from hs_pack_lib import board, check, definition, derivation, example, figure_explain, gen, guide, intro, lesson, summary, theorem, tp

UNIT_ID = "HS-CHEB-U03"

KW = "水のイオン積を $K_{\\mathrm{w}}=1.0\\times10^{-14}\\ (\\mathrm{mol/L})^2$ とする。"


# ----------------------------------------------------------------------
# 補助
# ----------------------------------------------------------------------

def tex(f):
    return "\\mathrm{" + re.sub(r"(\d+)", lambda m: "_" + (m.group(1) if len(m.group(1)) == 1 else "{" + m.group(1) + "}"), f) + "}"


def dec(x):
    x = sp.Rational(x)
    d = Decimal(int(x.p)) / Decimal(int(x.q))
    dn = d.normalize()
    if len(dn.as_tuple().digits) == 1 and abs(d) < 10:
        dn = d.quantize(Decimal(1).scaleb(dn.adjusted() - 1))
    return format(dn, "f")


def vfmt(x):
    """体積の表示（小数第1位以上まで書く：10 → 10.0、12.5 → 12.5、6.25 → 6.25）。"""
    x = sp.Rational(x)
    d = Decimal(int(x.p)) / Decimal(int(x.q))
    q = d.quantize(Decimal("0.1"))
    return format(q, "f") if q == d else format(d.normalize(), "f")


def clean(x, digits=3):
    x = sp.Rational(x)
    q = x.q
    for p in (2, 5):
        while q % p == 0:
            q //= p
    if q != 1:
        return False
    d = Decimal(int(x.p)) / Decimal(int(x.q))
    return len(d.normalize().as_tuple().digits) <= digits


def sig(x, n=2):
    x = sp.nsimplify(x)
    d = Decimal(str(sp.N(x, 40)))
    e = d.adjusted()
    r = d.quantize(Decimal(1).scaleb(e - n + 1), rounding=ROUND_HALF_UP)
    if r.adjusted() != e:
        e = r.adjusted()
        r = d.quantize(Decimal(1).scaleb(e - n + 1), rounding=ROUND_HALF_UP)
    if e >= n + 1 or e < -3:
        return f"{format(r.scaleb(-e), 'f')}\\times10^{{{e}}}"
    if e >= n:
        return format(r.quantize(Decimal(1)), "f")
    return format(r, "f")


def sci(k):
    """1.0×10^{-k} の表記。"""
    return f"1.0\\times10^{{-{k}}}"


def numq(stem, x, expr, e, unit=None, n=2, **kw):
    s = sig(x, n)
    try:
        exact = "times" not in s and sp.Rational(s) == sp.nsimplify(x)
    except (TypeError, ValueError):
        exact = False
    if not exact and "有効数字" not in stem:
        stem += f"有効数字{n}桁で答えなさい。"
    ans = s if "times" not in s else f"${s}$"
    chk = (expr, str(sp.nsimplify(x))) if exact else (expr, str(sp.nsimplify(x)), None, "intermediate")
    if unit:
        kw["unit"] = unit
    return num(stem, ans, e, chk=chk, **kw)


def err_item(stem, wrong, step, etype, tempt, fix, ans, expl, steps, ap, alt, pit, chk=None, d=3):
    return desc(f"{stem}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい答えを求めなさい。", ans, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい考え方・途中の式を示している", 3), ("最終的な答えが正しい", 1)], d=d, p=6, lines=6,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい考え方", 3), ("正しい答え", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix), chk=chk)


# 酸・塩基：化学式 → (名称, 水溶液の名称, 価数, 強弱)
ACIDS = {"HCl": ("塩化水素", "塩酸", 1, "強"), "HNO3": ("硝酸", "硝酸", 1, "強"), "H2SO4": ("硫酸", "硫酸", 2, "強"),
         "CH3COOH": ("酢酸", "酢酸水溶液", 1, "弱"), "(COOH)2": ("シュウ酸", "シュウ酸水溶液", 2, "弱"), "H2S": ("硫化水素", "硫化水素水", 2, "弱")}
BASES = {"NaOH": ("水酸化ナトリウム", "水酸化ナトリウム水溶液", 1, "強"), "KOH": ("水酸化カリウム", "水酸化カリウム水溶液", 1, "強"),
         "Ca(OH)2": ("水酸化カルシウム", "水酸化カルシウム水溶液", 2, "強"), "Ba(OH)2": ("水酸化バリウム", "水酸化バリウム水溶液", 2, "強"),
         "NH3": ("アンモニア", "アンモニア水", 1, "弱"), "Cu(OH)2": ("水酸化銅(Ⅱ)", "", 2, "弱")}


# ----------------------------------------------------------------------
# 滴定曲線（図）
# ----------------------------------------------------------------------

def _curve(kind):
    def ss(v):
        nh = 1.0 - 0.1 * v
        tot = 10 + v
        if abs(nh) < 1e-9:
            return 7.0
        return min(7.0, -math.log10(nh / tot)) if nh > 0 else max(7.0, 14 + math.log10(-nh / tot))

    pa, eqa = 0.5 * (4.76 + 1.0), 14 - 0.5 * (9.24 - math.log10(0.05))
    eqb = 0.5 * (9.25 - math.log10(0.05))

    def wa(v):
        if v <= 1e-9:
            return pa
        if v < 10 - 1e-9:
            return min(eqa, max(pa, 4.76 + math.log10(v / (10 - v))))
        if abs(v - 10) < 1e-9:
            return eqa
        return max(eqa, 14 + math.log10((0.1 * v - 1) / (10 + v)))

    def wb(v):
        if v < 10 - 1e-9:
            return min(eqb, -math.log10((1.0 - 0.1 * v) / (10 + v)))
        if abs(v - 10) < 1e-9:
            return eqb
        return max(eqb, 14 - (4.75 + math.log10(1 / (0.1 * v - 1))))
    return {"ss": ss, "wa": wa, "wb": wb}[kind]


def titration_fig(kind, caption):
    f = _curve(kind)
    eq = f(10)
    svg = plane(xr=(0, 20), yr=(0, 14), unit=11, curves=[(f, "")], points=[(10, eq, "中和点")], grid=False,
                polygons=[[(0, 8.0), (20, 8.0), (20, 9.8), (0, 9.8)], [(0, 3.1), (20, 3.1), (20, 4.4), (0, 4.4)]],
                labels=[(12.6, 10.4, "PP"), (12.6, 5.0, "MO")], xl="V[mL]", yl="pH")
    return figure("滴定曲線。横軸は滴下量 V（mL）、縦軸は pH。帯は指示薬の変色域（PP：フェノールフタレイン 約8.0〜9.8、MO：メチルオレンジ 約3.1〜4.4）。", svg=svg, caption=caption)


# ======================================================================
# 授業プリント
# ======================================================================

LESSON = lesson(
    goals=["酸・塩基の定義と強弱・価数を説明し、水のイオン積を用いて強酸・強塩基の水溶液の pH を求められる。",
           "中和の量的関係（酸の出す $\\mathrm{H^+}$ の物質量＝塩基の出す $\\mathrm{OH^-}$ の物質量）を導き、中和滴定の器具・指示薬・計算を説明できる。",
           "酸化数を用いて酸化・還元を判断し、半反応式から酸化還元反応の量的関係を求められる。イオン化傾向から電池の正極・負極と反応を説明できる。"],
    duration=150,
    readiness=["物質量・モル濃度の計算（$n=cV$）ができる（前単元）。", "イオンの化学式・電子配置（前々単元）と、中学校で学んだ酸性・アルカリ性・中和を説明できる。",
               "$10^{-3}$ などの指数と、常用対数 $\\log_{10}10^{n}=n$ の意味が分かる。"],
    flow=[("導入：身のまわりの酸・塩基と電池", 8, "胃酸と制酸剤、乾電池を例に、この単元の2つの柱（中和・酸化還元）を示す"),
          ("酸・塩基の定義と強弱・価数", 17, "アレニウスとブレンステッド・ローリーの定義、電離度、価数"),
          ("水素イオン濃度と pH", 20, "水のイオン積、pH の定義、希釈と pH"),
          ("中和の量的関係と中和滴定", 30, "量的関係の導出、器具と操作、滴定曲線と指示薬、塩の水溶液の性質"),
          ("酸化と還元・酸化数", 25, "酸素・水素・電子の授受による定義、酸化数の決め方、酸化剤・還元剤"),
          ("半反応式と酸化還元滴定", 20, "電子の数を合わせてイオン反応式をつくる、$\\mathrm{KMnO_4}$ 滴定"),
          ("イオン化傾向と電池", 20, "金属の反応性、ダニエル電池の仕組み"),
          ("まとめと確認", 10, "確認問題、問題プリントの課題指示")],
    sections=[
        intro("in1", "「やりとりされる粒子」で反応を見る",
              "酸と塩基の反応（中和）は水素イオン $\\mathrm{H^+}$ のやりとり、酸化還元反応は電子 $\\mathrm{e^-}$ のやりとりとして統一的にとらえられる。"
              "どちらの反応でも「受け渡しされる粒子の物質量が等しい」という1つの原理から、中和滴定・酸化還元滴定の計算が導ける。電池は、酸化還元反応の電子のやりとりを導線に通して取り出す装置である。",
              bullets=["中和：酸が出す $\\mathrm{H^+}$ の物質量＝塩基が受け取る（出す $\\mathrm{OH^-}$ の）物質量。",
                       "酸化還元：還元剤が出す $\\mathrm{e^-}$ の物質量＝酸化剤が受け取る $\\mathrm{e^-}$ の物質量。"],
              points=[tp("中和と酸化還元を「何がやりとりされるか」で対比する表を、単元の最初に板書しておく。",
                         ask="胃薬（制酸剤）を飲むと胃の中で何が起こるか。", expect="胃酸（塩酸）が中和される。", timing="授業の冒頭")]),
        definition("df1", "酸・塩基の定義と強弱",
                   "アレニウスの定義では、水溶液中で $\\mathrm{H^+}$（$\\mathrm{H_3O^+}$）を生じる物質が酸、$\\mathrm{OH^-}$ を生じる物質が塩基である。"
                   "ブレンステッド・ローリーの定義では、$\\mathrm{H^+}$ を与える分子・イオンが酸、受け取る分子・イオンが塩基である。",
                   formula="$$\\text{電離度 }\\alpha=\\dfrac{\\text{電離した酸（塩基）の物質量}}{\\text{溶かした酸（塩基）の物質量}}\\quad(0<\\alpha\\leqq1),\\qquad [\\mathrm{H^+}]=(\\text{価数})\\times c\\times\\alpha$$",
                   conditions=["強酸（$\\mathrm{HCl}$、$\\mathrm{HNO_3}$、$\\mathrm{H_2SO_4}$）・強塩基（$\\mathrm{NaOH}$、$\\mathrm{KOH}$、$\\mathrm{Ca(OH)_2}$、$\\mathrm{Ba(OH)_2}$）は、うすい水溶液中でほぼ完全に電離する（$\\alpha\\fallingdotseq1$）。",
                               "弱酸（$\\mathrm{CH_3COOH}$、$\\mathrm{(COOH)_2}$ など）・弱塩基（$\\mathrm{NH_3}$ など）は一部しか電離しない（$\\alpha\\ll1$）。",
                               "価数は、酸1分子が出しうる $\\mathrm{H^+}$ の数、塩基1つが受け取りうる $\\mathrm{H^+}$ の数（出しうる $\\mathrm{OH^-}$ の数）。強弱と価数は無関係である。"],
                   points=[tp("「強い酸＝濃い酸」ではないことを確認する。強弱は電離度、濃さはモル濃度で表す別の量である。",
                              caution="酢酸 $\\mathrm{CH_3COOH}$ の H は4個あるが、価数は1である。")]),
        definition("df2", "水のイオン積と pH",
                   "水はわずかに電離しており、25 ℃ では水溶液中で常に $[\\mathrm{H^+}][\\mathrm{OH^-}]=1.0\\times10^{-14}\\ (\\mathrm{mol/L})^2$ が成り立つ（水のイオン積 $K_{\\mathrm{w}}$）。",
                   formula="$$\\mathrm{pH}=-\\log_{10}[\\mathrm{H^+}]\\qquad([\\mathrm{H^+}]=1.0\\times10^{-n}\\ \\mathrm{mol/L}\\ \\Longleftrightarrow\\ \\mathrm{pH}=n)$$",
                   conditions=["25 ℃ で中性は pH 7、酸性は pH < 7、塩基性は pH > 7。", "塩基性の水溶液は、まず $[\\mathrm{OH^-}]$ を求め、$K_{\\mathrm{w}}$ から $[\\mathrm{H^+}]$ を求めて pH を出す。",
                               "酸を水で $10$ 倍にうすめると pH は 1 大きくなるが、どれだけうすめても pH は 7 をこえない（塩基では 7 を下回らない）。"],
                   points=[tp("pH が 1 違うと $[\\mathrm{H^+}]$ が 10 倍違うことを、数直線に $10^{-1},\\,10^{-2},\\,\\dots$ を並べて実感させる。",
                              ask="pH 2 の塩酸と pH 4 の塩酸では、$[\\mathrm{H^+}]$ は何倍ちがうか。", expect="100 倍。")]),
        theorem("th1", "中和の量的関係",
                "$$a\\times c\\times V=b\\times c'\\times V'\\qquad(a,\\,b：\\text{酸・塩基の価数},\\ c,\\,c'：\\text{モル濃度},\\ V,\\,V'：\\text{体積})$$",
                ["酸と塩基が過不足なく中和するとき（中和点）に成り立つ。", "酸・塩基の強弱には関係しない（弱酸も中和の進行とともにすべて反応する）。",
                 "体積 $V,\\ V'$ は両辺で同じ単位ならよい（mL のままでも比が等しい）。"],
                proof=["酸 $c$ mol/L、$V$ L に含まれる酸の物質量は $cV$ mol。価数 $a$ の酸はこれから $\\mathrm{H^+}$ を $acV$ mol 出しうる。",
                       "同様に、塩基は $\\mathrm{OH^-}$ を $bc'V'$ mol 出しうる（$\\mathrm{H^+}$ を $bc'V'$ mol 受け取りうる）。",
                       "中和 $\\mathrm{H^+}+\\mathrm{OH^-}\\longrightarrow\\mathrm{H_2O}$ は 1:1 で進むので、過不足なく中和する条件は $acV=bc'V'$。",
                       "弱酸は一部しか電離していないが、$\\mathrm{H^+}$ が中和で消費されると電離が進み、最終的にはすべて反応するので、同じ式が成り立つ。"],
                points=[tp("式を覚えさせるのではなく、「$\\mathrm{H^+}$ の物質量＝$\\mathrm{OH^-}$ の物質量」から毎回立てさせる。",
                           ask="同じ濃度・同じ体積の塩酸と酢酸水溶液を中和するのに必要な NaOH の量は同じか。", expect="同じ（どちらも1価で物質量が等しい）。")]),
        figure_explain("fg1", "中和滴定と滴定曲線",
                       titration_fig("wa", "0.10 mol/L 酢酸水溶液 10 mL に 0.10 mol/L NaOH 水溶液を滴下したときの滴定曲線（概形）"),
                       "ホールピペットで酸の水溶液を一定体積はかりとってコニカルビーカーに入れ、ビュレットから塩基の水溶液を滴下する。中和点の前後で pH が急激に変化するので、その範囲に変色域をもつ指示薬を選ぶ。"
                       "弱酸と強塩基の中和点は塩基性側にあるのでフェノールフタレイン、強酸と弱塩基ではメチルオレンジ、強酸と強塩基ではどちらも使える。",
                       points=[tp("ホールピペット・ビュレットは使う溶液で共洗いし、メスフラスコ・コニカルビーカーは純水でぬれたまま使ってよい理由（溶質の物質量が変わるかどうか）を考えさせる。",
                                  ask="コニカルビーカーが水でぬれていても滴定結果が変わらないのはなぜか。", expect="中に入れた酸の物質量は変わらないから。")]),
        definition("df3", "酸化・還元と酸化数",
                   "物質が酸素を受け取る・水素を失う・電子を失う変化を酸化、その逆を還元という。酸化と還元は必ず同時に起こる。"
                   "原子の酸化の程度を表す数値を酸化数といい、酸化数が増加した原子は酸化され、減少した原子は還元された。",
                   formula="$$\\text{酸化数の決め方：単体 }0,\\ \\text{化合物の総和 }0,\\ \\text{イオンの総和}=\\text{電荷},\\ \\mathrm{H}=+1,\\ \\mathrm{O}=-2,\\ \\text{アルカリ金属}=+1$$",
                   conditions=["例外：過酸化水素 $\\mathrm{H_2O_2}$ の O は $-1$。", "単原子イオンの酸化数はイオンの電荷に等しい（$\\mathrm{Fe^{3+}}$ は $+3$）。",
                               "相手を酸化し自身は還元される物質を酸化剤、相手を還元し自身は酸化される物質を還元剤という。"],
                   points=[tp("$\\mathrm{KMnO_4}$、$\\mathrm{K_2Cr_2O_7}$、$\\mathrm{SO_4^{2-}}$ などで、未知数 $x$ の一次方程式として酸化数を求める練習をさせる。",
                              caution="多原子イオンでは「総和＝0」ではなく「総和＝イオンの電荷」とすることを忘れやすい。")]),
        derivation("dv1", "半反応式からイオン反応式をつくる（$\\mathrm{KMnO_4}$ と $\\mathrm{H_2O_2}$）",
                   ["酸化剤：$\\mathrm{MnO_4^-}$ → $\\mathrm{Mn^{2+}}$。Mn の酸化数は $+7\\to+2$ なので $5\\mathrm{e^-}$ を受け取る。",
                    "O の数を $\\mathrm{H_2O}$ で、H の数を $\\mathrm{H^+}$ で合わせる：$\\mathrm{MnO_4^-}+8\\mathrm{H^+}+5\\mathrm{e^-}\\longrightarrow\\mathrm{Mn^{2+}}+4\\mathrm{H_2O}$（両辺の電荷 $+2$ で一致）。",
                    "還元剤：$\\mathrm{H_2O_2}\\longrightarrow\\mathrm{O_2}+2\\mathrm{H^+}+2\\mathrm{e^-}$。",
                    "授受される電子の数をそろえる（最小公倍数 10）：酸化剤の式を 2 倍、還元剤の式を 5 倍して足し、$\\mathrm{e^-}$ を消去する。",
                    "$2\\mathrm{MnO_4^-}+5\\mathrm{H_2O_2}+6\\mathrm{H^+}\\longrightarrow2\\mathrm{Mn^{2+}}+5\\mathrm{O_2}+8\\mathrm{H_2O}$。よって $\\mathrm{KMnO_4}:\\mathrm{H_2O_2}=2:5$（物質量比）で反応する。"],
                   body="酸化還元滴定の計算は、「酸化剤が受け取る $\\mathrm{e^-}$ の物質量＝還元剤が出す $\\mathrm{e^-}$ の物質量」として、中和と同じ形で立てられる。",
                   points=[tp("半反応式は「酸化数の変化 → 電子の数 → O を $\\mathrm{H_2O}$ → H を $\\mathrm{H^+}$ → 電荷の確認」という手順で毎回組み立てさせる。", timing="例題3の前")]),
        theorem("th2", "イオン化傾向と電池",
                "$$\\mathrm{Li}>\\mathrm{K}>\\mathrm{Ca}>\\mathrm{Na}>\\mathrm{Mg}>\\mathrm{Al}>\\mathrm{Zn}>\\mathrm{Fe}>\\mathrm{Ni}>\\mathrm{Sn}>\\mathrm{Pb}>(\\mathrm{H_2})>\\mathrm{Cu}>\\mathrm{Hg}>\\mathrm{Ag}>\\mathrm{Pt}>\\mathrm{Au}$$",
                ["イオン化傾向の大きい金属ほど電子を失って陽イオンになりやすい（酸化されやすい）。",
                 "イオン化傾向の小さい金属の陽イオンを含む水溶液に、大きい金属を入れると、小さい方の金属が析出する（例：$\\mathrm{Zn}+\\mathrm{Cu^{2+}}\\longrightarrow\\mathrm{Zn^{2+}}+\\mathrm{Cu}$）。",
                 "2種類の金属で電池をつくると、イオン化傾向の大きい方が負極（酸化反応）、小さい方が正極（還元反応）になる。電子は負極から導線を通って正極へ流れる。"],
                body="ダニエル電池：負極 $\\mathrm{Zn}\\longrightarrow\\mathrm{Zn^{2+}}+2\\mathrm{e^-}$、正極 $\\mathrm{Cu^{2+}}+2\\mathrm{e^-}\\longrightarrow\\mathrm{Cu}$。素焼き板（セパレーター）は2つの水溶液がすぐに混ざるのを防ぎつつ、イオンを通して電気的なつり合いを保つ。",
                proof=["亜鉛板を硫酸銅(Ⅱ)水溶液に直接入れると、亜鉛の表面で電子が $\\mathrm{Cu^{2+}}$ に渡されて銅が析出する（電子は外に取り出せない）。",
                       "亜鉛と $\\mathrm{Cu^{2+}}$ を別々の容器に分け、導線でつなぐと、亜鉛が放出した電子は導線を通って銅板に達し、そこで $\\mathrm{Cu^{2+}}$ が受け取る。",
                       "この電子の流れが電流（向きは正極→負極）であり、化学エネルギーが電気エネルギーに変換される。"],
                points=[tp("「負極＝電子を押し出す側＝酸化」「正極＝電子を受け取る側＝還元」を、電子の流れの矢印をかきながら説明する。",
                           caution="電流の向きと電子の流れの向きが逆であることを必ず確認する。")]),
        example("ex1", "例題1　pH の計算",
                "(1) 0.010 mol/L の塩酸、(2) 0.0010 mol/L の水酸化ナトリウム水溶液の pH をそれぞれ求めよ。どちらも完全に電離し、$K_{\\mathrm{w}}=1.0\\times10^{-14}\\ (\\mathrm{mol/L})^2$ とする。",
                ["(1) HCl は1価の強酸：$[\\mathrm{H^+}]=1.0\\times10^{-2}$ mol/L → pH 2。",
                 "(2) NaOH は1価の強塩基：$[\\mathrm{OH^-}]=1.0\\times10^{-3}$ mol/L。",
                 "$[\\mathrm{H^+}]=\\dfrac{1.0\\times10^{-14}}{1.0\\times10^{-3}}=1.0\\times10^{-11}$ mol/L → pH 11。"],
                "(1) 2　(2) 11", thinking="塩基では $[\\mathrm{OH^-}]$ から $[\\mathrm{H^+}]$ を求めてから pH にする。",
                misconceptions=[("(2) $[\\mathrm{OH^-}]=10^{-3}$ だから pH 3", "pH は $[\\mathrm{H^+}]$ で決まる。$K_{\\mathrm{w}}$ から $[\\mathrm{H^+}]=10^{-11}$、pH 11")]),
        example("ex2", "例題2　中和滴定",
                "濃度不明の硫酸 10.0 mL を 0.100 mol/L の水酸化ナトリウム水溶液で滴定したところ、中和点までに 16.0 mL を要した。硫酸のモル濃度を求めよ。",
                ["$\\mathrm{H_2SO_4}$ は2価の酸、NaOH は1価の塩基。", "$2\\times c\\times\\dfrac{10.0}{1000}=1\\times0.100\\times\\dfrac{16.0}{1000}$。", "$c=0.0800$ mol/L。"],
                "$8.00\\times10^{-2}$ mol/L", thinking="$\\mathrm{H^+}$ の物質量＝$\\mathrm{OH^-}$ の物質量。硫酸の価数 2 を忘れない。",
                points=[tp("価数を書き忘れた答え（0.160 mol/L）と比べさせ、2倍の差が生じる理由を説明させる。")]),
        example("ex3", "例題3　酸化還元滴定",
                "硫酸酸性にした濃度不明の過酸化水素水 10.0 mL を、0.0200 mol/L の過マンガン酸カリウム水溶液で滴定したところ、8.00 mL で赤紫色が消えなくなった。過酸化水素水のモル濃度を求めよ。",
                ["$\\mathrm{MnO_4^-}$ 1 mol は $\\mathrm{e^-}$ を 5 mol 受け取り、$\\mathrm{H_2O_2}$ 1 mol は $\\mathrm{e^-}$ を 2 mol 出す。",
                 "$5\\times0.0200\\times\\dfrac{8.00}{1000}=2\\times c\\times\\dfrac{10.0}{1000}$。", "$c=0.0400$ mol/L。"],
                "$4.00\\times10^{-2}$ mol/L", thinking="電子の物質量のつり合いで立式する（中和の価数の代わりに、授受する電子の数を使う）。",
                points=[tp("$\\mathrm{KMnO_4}$ 自身の赤紫色が消えなくなる点が終点になる（指示薬が不要）ことを確認する。")]),
        example("ex4", "例題4　ダニエル電池",
                "ダニエル電池を放電させ、導線に電子が 0.20 mol 流れた。負極・正極の質量はそれぞれ何 g 変化するか。原子量は Cu＝64、Zn＝65 とする。",
                ["負極 $\\mathrm{Zn}\\longrightarrow\\mathrm{Zn^{2+}}+2\\mathrm{e^-}$：Zn が $0.20\\div2=0.10$ mol 溶け出す → $0.10\\times65=6.5$ g 減少。",
                 "正極 $\\mathrm{Cu^{2+}}+2\\mathrm{e^-}\\longrightarrow\\mathrm{Cu}$：Cu が 0.10 mol 析出 → $0.10\\times64=6.4$ g 増加。"],
                "負極 6.5 g 減少、正極 6.4 g 増加", thinking="電子の物質量から、半反応式の係数の比で金属の物質量を求める。"),
        board("bd1", "板書案",
              [("① 酸・塩基と pH", ["酸：$\\mathrm{H^+}$ を出す（与える）", "強弱＝電離度、価数＝$\\mathrm{H^+}$ の数", "$[\\mathrm{H^+}][\\mathrm{OH^-}]=1.0\\times10^{-14}$",
                                     "$\\mathrm{pH}=-\\log_{10}[\\mathrm{H^+}]$", "中和：$acV=bc'V'$", "指示薬は中和点の pH で選ぶ"]),
               ("② 酸化還元", ["酸化＝$\\mathrm{e^-}$ を失う＝酸化数↑", "還元＝$\\mathrm{e^-}$ を得る＝酸化数↓", "酸化数：H $+1$、O $-2$、総和＝電荷",
                               "半反応式：e⁻ → $\\mathrm{H_2O}$ → $\\mathrm{H^+}$", "$\\mathrm{e^-}$ の物質量のつり合い"]),
               ("③ 電池", ["イオン化傾向 大 → 負極（酸化）", "小 → 正極（還元）", "電子：負極 → 正極", "電流：正極 → 負極",
                           "ダニエル電池 Zn | $\\mathrm{Zn^{2+}}$ ‖ $\\mathrm{Cu^{2+}}$ | Cu"])]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("pH の計算では、「$[\\mathrm{H^+}]$ を $1.0\\times10^{-n}$ の形にする」ことを最初の目標にさせる。対数の計算が苦手な生徒には、指数を読むだけでよいことを示す。",
                  caution="塩基性の水溶液で $[\\mathrm{OH^-}]$ の指数をそのまま pH と答える誤りが多い。"),
               tp("中和の計算では、価数を必ず式に書かせる。特に $\\mathrm{H_2SO_4}$、$\\mathrm{(COOH)_2}$、$\\mathrm{Ba(OH)_2}$ で確認する。",
                  ask="0.10 mol/L の硫酸 10 mL と過不足なく中和する 0.10 mol/L NaOH 水溶液は何 mL か。", expect="20 mL"),
               tp("「酸化剤は自身が還元される」という逆向きの関係を、酸化数の矢印で毎回確認させる。", timing="酸化剤・還元剤の導入時"),
               tp("塩の水溶液の性質は「もとの酸・塩基の強い方の性質を示す」と整理し、中和点の pH と指示薬の選択に結びつける。")],
              misconceptions=[("弱酸は中和に必要な塩基が少なくてすむ", "中和の量的関係は価数と物質量で決まり、強弱には関係しない"),
                              ("酸を水で 1000 倍にうすめれば pH は 3 大きくなり、pH 8 にもなりうる", "酸をどれだけうすめても pH は 7 をこえない"),
                              ("電池ではイオン化傾向の大きい金属が正極になる", "イオン化傾向の大きい金属が電子を出す負極になる")]),
        summary("sm1", "まとめ", ["pH は $[\\mathrm{H^+}]$ で決まり、塩基性では $K_{\\mathrm{w}}$ を用いる。強弱（電離度）と価数・濃度を区別する。",
                                   "中和の量的関係は「$\\mathrm{H^+}$ の物質量＝$\\mathrm{OH^-}$ の物質量」。指示薬は中和点の pH で選ぶ。",
                                   "酸化還元は電子の授受で、酸化数の増減で判断する。半反応式の電子の数から量的関係が決まる。電池ではイオン化傾向の大きい金属が負極になる。"]),
        check("ck1", "確認問題", [("0.050 mol/L の硫酸（完全に電離）の pH は？", "$[\\mathrm{H^+}]=0.10$ mol/L より pH 1"),
                                  ("$\\mathrm{K_2Cr_2O_7}$ 中の Cr の酸化数は？", "$+6$"),
                                  ("0.10 mol/L 酢酸水溶液 10 mL の中和に必要な 0.10 mol/L NaOH 水溶液は？", "10 mL"),
                                  ("亜鉛と銅で電池をつくったとき、負極はどちらか。", "亜鉛（イオン化傾向が大きい）")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

@gen("basic_check", 5, ["computation", "condition_check"])
def ph_basic(r):
    form = r.choice(["a1", "a2", "b1", "b2", "rev"])
    if form == "a1":
        f = r.choice(["HCl", "HNO3"])
        k = r.randint(1, 5)
        return num(f"${sci(k)}$ mol/L の{ACIDS[f][1]}の pH を求めなさい。ただし、{ACIDS[f][0]}は完全に電離するものとする。", str(k),
                   f"1価の強酸なので $[\\mathrm{{H^+}}]={sci(k)}$ mol/L、pH＝{k}。", d=1,
                   ap="1価の強酸は完全に電離するので、$[\\mathrm{H^+}]$ はモル濃度と等しい。$[\\mathrm{H^+}]=1.0\\times10^{-n}$ なら pH＝$n$。",
                   steps=[f"$[\\mathrm{{H^+}}]=1\\times{sci(k)}\\times1={sci(k)}$ mol/L。", f"$\\mathrm{{pH}}=-\\log_{{10}}({sci(k)})={k}$。"],
                   alt=["pH 1 の強酸を 10 倍ずつうすめると pH が 1 ずつ大きくなる、という関係から確かめる。"],
                   pc=[("$[\\mathrm{H^+}]$ を正しく求めている", 1), ("pH が正しい", 1)], pit=["指数の符号のまま「pH＝−" + str(k) + "」と答える。"],
                   chk=(f"-log(10**(-{k}), 10)", str(k)))
    if form == "a2":
        k = r.randint(2, 5)
        return num(f"$5.0\\times10^{{-{k}}}$ mol/L の硫酸の pH を求めなさい。ただし、硫酸は完全に電離するものとする。", str(k - 1),
                   f"2価の強酸なので $[\\mathrm{{H^+}}]=2\\times5.0\\times10^{{-{k}}}={sci(k - 1)}$ mol/L、pH＝{k - 1}。", d=2,
                   ap="硫酸は2価の酸。1 mol から $\\mathrm{H^+}$ が 2 mol 生じる。",
                   steps=[f"$[\\mathrm{{H^+}}]=2\\times5.0\\times10^{{-{k}}}={sci(k - 1)}$ mol/L。", f"pH＝{k - 1}。"],
                   alt=["$\\mathrm{H_2SO_4}\\longrightarrow2\\mathrm{H^+}+\\mathrm{SO_4^{2-}}$ の電離式をかいて、$\\mathrm{H^+}$ の濃度が2倍になることを確かめる。"],
                   pc=[("価数 2 を用いている", 1), ("pH が正しい", 1)], pit=["価数を掛け忘れて、$[\\mathrm{H^+}]=5.0\\times10^{-" + str(k) + "}$ として計算する。"],
                   chk=(f"-log(2*5*10**(-{k}), 10)", str(k - 1)))
    if form == "b1":
        f = r.choice(["NaOH", "KOH"])
        k = r.randint(1, 5)
        return num(f"${sci(k)}$ mol/L の{BASES[f][1]}の pH を求めなさい。ただし、{BASES[f][0]}は完全に電離するものとする。{KW}", str(14 - k),
                   f"$[\\mathrm{{OH^-}}]={sci(k)}$ mol/L、$[\\mathrm{{H^+}}]={sci(14 - k)}$ mol/L、pH＝{14 - k}。", d=2,
                   ap="塩基の水溶液では、まず $[\\mathrm{OH^-}]$ を求め、水のイオン積から $[\\mathrm{H^+}]$ を求める。",
                   steps=[f"$[\\mathrm{{OH^-}}]={sci(k)}$ mol/L。", f"$[\\mathrm{{H^+}}]=\\dfrac{{1.0\\times10^{{-14}}}}{{{sci(k)}}}={sci(14 - k)}$ mol/L。", f"pH＝{14 - k}。"],
                   alt=[f"pOH＝$-\\log_{{10}}[\\mathrm{{OH^-}}]={k}$ を求め、pH＝14－pOH＝{14 - k} としてもよい。"],
                   pc=[("$[\\mathrm{H^+}]$ を正しく求めている", 1), ("pH が正しい", 1)], pit=["$[\\mathrm{OH^-}]$ の指数をそのまま pH とする。"],
                   chk=(f"14+log(10**(-{k}), 10)", str(14 - k)))
    if form == "b2":
        f = r.choice(["Ba(OH)2", "Ca(OH)2"])
        k = r.randint(2, 5)
        return num(f"$5.0\\times10^{{-{k}}}$ mol/L の{BASES[f][1]}の pH を求めなさい。ただし、{BASES[f][0]}は完全に電離するものとする。{KW}", str(15 - k),
                   f"$[\\mathrm{{OH^-}}]=2\\times5.0\\times10^{{-{k}}}={sci(k - 1)}$ mol/L、pH＝{15 - k}。", d=2,
                   ap=f"${tex(f)}$ は2価の塩基。$[\\mathrm{{OH^-}}]$ は濃度の2倍になる。",
                   steps=[f"$[\\mathrm{{OH^-}}]={sci(k - 1)}$ mol/L。", f"$[\\mathrm{{H^+}}]={sci(15 - k)}$ mol/L。", f"pH＝{15 - k}。"],
                   alt=[f"pOH＝{k - 1}、pH＝14－{k - 1}＝{15 - k}。"],
                   pc=[("価数を用いて $[\\mathrm{OH^-}]$ を求めている", 1), ("pH が正しい", 1)], pit=["価数 2 を掛け忘れる。"],
                   chk=(f"14+log(2*5*10**(-{k}), 10)", str(15 - k)))
    k = r.randint(1, 4)
    f = r.choice(["HCl", "HNO3"])
    return sa(f"pH が {k} の{ACIDS[f][1]}の水素イオン濃度 $[\\mathrm{{H^+}}]$ と、{ACIDS[f][0]}のモル濃度を答えなさい。ただし、{ACIDS[f][0]}は完全に電離するものとする。",
              f"$[\\mathrm{{H^+}}]={sci(k)}$ mol/L、モル濃度 ${sci(k)}$ mol/L", f"pH＝$n$ ⇔ $[\\mathrm{{H^+}}]=1.0\\times10^{{-n}}$。1価の強酸なのでモル濃度も等しい。", d=1,
              ap="pH の定義を逆にたどる。1価の強酸では $[\\mathrm{H^+}]$ とモル濃度が等しい。",
              steps=[f"$[\\mathrm{{H^+}}]=1.0\\times10^{{-{k}}}$ mol/L。", "1価の強酸で完全電離なので、モル濃度も同じ値。"],
              alt=["求めた濃度から pH を計算し直して、もとの値に戻るか確かめる。"],
              pc=[("$[\\mathrm{H^+}]$ が正しい", 1), ("モル濃度が正しい", 1)], pit=["$1.0\\times10^{" + str(k) + "}$ と指数の符号を誤る。"],
              chk=(f"-log(10**(-{k}), 10)", str(k), None, "intermediate"))


# 酸化数：(化学式TeX, 対象元素, 電荷, [(元素, 個数, 酸化数)], 対象の個数, 名称)
OX = [("H_2SO_4", "S", 0, [("H", 2, 1), ("O", 4, -2)], 1, "硫酸"), ("SO_2", "S", 0, [("O", 2, -2)], 1, "二酸化硫黄"), ("H_2S", "S", 0, [("H", 2, 1)], 1, "硫化水素"),
      ("SO_4^{2-}", "S", -2, [("O", 4, -2)], 1, "硫酸イオン"), ("HNO_3", "N", 0, [("H", 1, 1), ("O", 3, -2)], 1, "硝酸"), ("NO_2", "N", 0, [("O", 2, -2)], 1, "二酸化窒素"),
      ("NO", "N", 0, [("O", 1, -2)], 1, "一酸化窒素"), ("NH_3", "N", 0, [("H", 3, 1)], 1, "アンモニア"), ("NH_4^{+}", "N", 1, [("H", 4, 1)], 1, "アンモニウムイオン"),
      ("MnO_4^{-}", "Mn", -1, [("O", 4, -2)], 1, "過マンガン酸イオン"), ("MnO_2", "Mn", 0, [("O", 2, -2)], 1, "酸化マンガン(Ⅳ)"),
      ("K_2Cr_2O_7", "Cr", 0, [("K", 2, 1), ("O", 7, -2)], 2, "二クロム酸カリウム"), ("Cr_2O_7^{2-}", "Cr", -2, [("O", 7, -2)], 2, "二クロム酸イオン"),
      ("CrO_4^{2-}", "Cr", -2, [("O", 4, -2)], 1, "クロム酸イオン"), ("CO", "C", 0, [("O", 1, -2)], 1, "一酸化炭素"), ("CH_4", "C", 0, [("H", 4, 1)], 1, "メタン"),
      ("(COOH)_2", "C", 0, [("O", 4, -2), ("H", 2, 1)], 2, "シュウ酸"), ("C_2O_4^{2-}", "C", -2, [("O", 4, -2)], 2, "シュウ酸イオン"),
      ("Fe_2O_3", "Fe", 0, [("O", 3, -2)], 2, "酸化鉄(Ⅲ)"), ("HClO", "Cl", 0, [("H", 1, 1), ("O", 1, -2)], 1, "次亜塩素酸"),
      ("KClO_3", "Cl", 0, [("K", 1, 1), ("O", 3, -2)], 1, "塩素酸カリウム"), ("ClO_4^{-}", "Cl", -1, [("O", 4, -2)], 1, "過塩素酸イオン"),
      ("Cu_2O", "Cu", 0, [("O", 1, -2)], 2, "酸化銅(Ⅰ)"), ("Na_2SO_3", "S", 0, [("Na", 2, 1), ("O", 3, -2)], 1, "亜硫酸ナトリウム"),
      ("H_2O_2", "O", 0, [("H", 2, 1)], 2, "過酸化水素"), ("SO_3^{2-}", "S", -2, [("O", 3, -2)], 1, "亜硫酸イオン")]


def ox_value(item):
    _, _, q, others, k, _ = item
    return sp.Rational(q - sum(c * v for _, c, v in others), k)


def sgn_s(v):
    return f"+{v}" if v > 0 else str(v)


@gen("basic_check", 5, ["computation", "condition_check"])
def oxidation_number(r):
    item = r.choice(OX)
    ft, el, q, others, k, name = item
    v = ox_value(item)
    terms = "+".join(f"({sgn_s(o)})\\times{c}" for _, c, o in others)
    lhs = (f"{k}x" if k > 1 else "x") + "+" + terms
    where = "化合物なので総和は 0" if q == 0 else f"イオンなので総和はイオンの電荷 ${sgn_s(q)}$"
    lead = r.choice(["次の物質・イオンに含まれる", "次の化学式で表される物質（イオン）中の"])
    return num(f"{lead} {el} 原子の酸化数を求めなさい。\n$\\quad\\mathrm{{{ft}}}$（{name}）", sgn_s(v),
               f"{el} の酸化数を $x$ とすると ${lhs}={q}$、$x={sgn_s(v)}$。", d=2,
               ap="H は ＋1、O は −2（過酸化水素を除く）、アルカリ金属は ＋1 とし、酸化数の総和が 0（イオンなら電荷）になるように方程式を立てる。",
               steps=[f"{el} の酸化数を $x$ とおく。" + ("（$\\mathrm{H_2O_2}$ では H を ＋1 として O を求める。）" if ft == "H_2O_2" else ""),
                      f"{where}：${lhs}={q}$。", f"$x={sgn_s(v)}$。"],
               alt=["電子の授受で確かめる：$\\mathrm{" + ft + "}$ が生じる反応や半反応式で、何個の電子が出入りしたかと照らし合わせる。"],
               pc=[("方程式を正しく立てている", 1), ("酸化数が正しい（符号を含む）", 1)],
               pit=["多原子イオンの総和を 0 としてしまう。", "対象の原子が2個あるときに個数を掛け忘れる。", "正の酸化数に ＋ をつけない（＋も必ず書く）。"],
               chk=(f"solve({k}*x+({'+'.join(f'{c}*({o})' for _, c, o in others)})-({q}), x)[0]", str(v)))


AB_ITEMS = [("HCl", "acid"), ("HNO3", "acid"), ("H2SO4", "acid"), ("CH3COOH", "acid"), ("(COOH)2", "acid"), ("H2S", "acid"),
            ("NaOH", "base"), ("KOH", "base"), ("Ca(OH)2", "base"), ("Ba(OH)2", "base"), ("NH3", "base"), ("Cu(OH)2", "base")]


def ab_info(f, kind):
    d = ACIDS if kind == "acid" else BASES
    return d[f][0], d[f][2], d[f][3]


def ab_label(f, kind):
    nm_, val, st = ab_info(f, kind)
    return f"{val}価の{st}{'酸' if kind == 'acid' else '塩基'}"


@gen("basic_check", 3, ["concept", "condition_check"])
def acid_base_class(r):
    target_f, kind = r.choice(AB_ITEMS)
    lab = ab_label(target_f, kind)
    others = [x for x in AB_ITEMS if ab_label(*x) != lab]
    wrong = r.sample(others, 3)
    t = lambda f: f"${tex(f)}$"  # noqa: E731
    why = {}
    for f, k in wrong:
        nm_, val, st = ab_info(f, k)
        why[t(f)] = (f"{nm_} ${tex(f)}$ は{ab_label(f, k)}である。", "酸・塩基の強弱と価数の判断の誤り")
    nm_, val, st = ab_info(target_f, kind)
    return mc(f"次のうち、{lab}に分類されるものを1つ選びなさい。", [t(target_f)] + [t(f) for f, _ in wrong],
              f"{nm_} ${tex(target_f)}$ は{lab}。", d=2,
              ap="価数は1分子（1つ）あたりの $\\mathrm{H^+}$ を出す数（塩基は受け取る数・$\\mathrm{OH^-}$ の数）、強弱は電離度の大小で決まる。",
              steps=["各物質の価数を、出しうる $\\mathrm{H^+}$（または $\\mathrm{OH^-}$）の数から求める。", "強酸 $\\mathrm{HCl,\\ HNO_3,\\ H_2SO_4}$、強塩基はアルカリ金属と Ca・Ba の水酸化物、と整理する。",
                     f"条件に合うのは ${tex(target_f)}$。"],
              alt=["電離式をかいて、生じる $\\mathrm{H^+}$・$\\mathrm{OH^-}$ の数を確かめる（例：$\\mathrm{(COOH)_2}$ は H を2個出す）。"],
              pc=[("価数を正しく判断している", 1), ("強弱を正しく判断している", 1)], why=why,
              pit=["酢酸 $\\mathrm{CH_3COOH}$ の H の数（4個）を価数と考える。", "アンモニアは OH をもたないので塩基ではないと考える。"])


SERIES = ["Li", "K", "Ca", "Na", "Mg", "Al", "Zn", "Fe", "Ni", "Sn", "Pb", "H2", "Cu", "Hg", "Ag", "Pt", "Au"]
MNAME = {"Mg": "マグネシウム", "Zn": "亜鉛", "Fe": "鉄", "Cu": "銅", "Ag": "銀", "Pb": "鉛", "Sn": "スズ", "Au": "金", "Pt": "白金", "Ni": "ニッケル"}
SOLN = {"Cu": ("硫酸銅(Ⅱ)水溶液", "Cu^{2+}"), "Ag": ("硝酸銀水溶液", "Ag^{+}"), "Zn": ("硫酸亜鉛水溶液", "Zn^{2+}"), "Fe": ("硫酸鉄(Ⅱ)水溶液", "Fe^{2+}"),
        "Pb": ("硝酸鉛(Ⅱ)水溶液", "Pb^{2+}"), "Mg": ("硫酸マグネシウム水溶液", "Mg^{2+}")}


def rank(m):
    return SERIES.index(m)


@gen("basic_check", 4, ["concept", "application"])
def ionization_tendency(r):
    form = r.choice(["disp", "disp", "acid", "cell"])
    if form == "disp":
        pairs = [(m, s) for m in ("Mg", "Zn", "Fe", "Cu", "Ag", "Pb") for s in SOLN if m != s]
        yes = [p for p in pairs if rank(p[0]) < rank(p[1])]
        no = [p for p in pairs if rank(p[0]) > rank(p[1])]
        right = r.choice(yes)
        wrong = r.sample(no, 3)
        t = lambda p: f"{MNAME[p[0]]}板を{SOLN[p[1]][0]}に入れる"  # noqa: E731
        why = {t(p): (f"{MNAME[p[0]]}は{MNAME[p[1]]}よりイオン化傾向が小さいので、$\\mathrm{{{SOLN[p[1]][1]}}}$ に電子を渡せず、反応は起こらない。", "イオン化傾向の大小の取り違え") for p in wrong}
        m, s = right
        return mc("次の操作のうち、金属板の表面に別の金属が析出するものを選びなさい。", [t(right)] + [t(p) for p in wrong],
                  f"{MNAME[m]}は{MNAME[s]}よりイオン化傾向が大きいので、{MNAME[m]}が陽イオンになり、{MNAME[s]}が析出する。", d=2,
                  ap="入れる金属のイオン化傾向が、水溶液中の金属イオンのもとの金属より大きいときだけ反応が起こる。",
                  steps=["イオン化傾向の順：Li > K > Ca > Na > Mg > Al > Zn > Fe > Ni > Sn > Pb > (H₂) > Cu > Hg > Ag > Pt > Au。",
                         "各組み合わせで、金属板の金属と水溶液中のイオンの金属を比べる。", f"{MNAME[m]} > {MNAME[s]} の組み合わせだけが反応する。"],
                  alt=["電子の受け渡しで考える：イオン化傾向の大きい金属が電子を出し、小さい金属のイオンが電子を受け取る。"],
                  pc=[("イオン化傾向を比べている", 1), ("正しく選んでいる", 1)], why=why,
                  pit=["水溶液中のイオンの方が反応すると考え、向きを逆にする。"])
    if form == "acid":
        nono = r.choice(["Cu", "Ag", "Au", "Pt"])
        yes = r.sample(["Mg", "Zn", "Fe", "Ni"], 3)
        why = {MNAME[m]: (f"{MNAME[m]}は水素よりイオン化傾向が大きいので、希塩酸と反応して水素を発生する。", "水素との位置関係の取り違え") for m in yes}
        return mc("次の金属のうち、希塩酸に入れても水素を発生しないものを選びなさい。", [MNAME[nono]] + [MNAME[m] for m in yes],
                  f"{MNAME[nono]}は水素よりイオン化傾向が小さく、$\\mathrm{{H^+}}$ に電子を渡せないので反応しない。", d=2,
                  ap="希塩酸の $\\mathrm{H^+}$ を還元して水素にできるのは、水素よりイオン化傾向の大きい金属だけ。",
                  steps=["イオン化傾向の列で、水素 $(\\mathrm{H_2})$ の位置を確認する。", "水素より右（小さい）にある金属は希塩酸と反応しない。", f"よって{MNAME[nono]}。"],
                  alt=["身近な例で確かめる：銅の硬貨や銀の食器は、酢などの酸で溶けて水素を出すことはない。"],
                  pc=[("水素との比較をしている", 1), ("正しく選んでいる", 1)], why=why, pit=["イオン化傾向の列の H の位置を覚えていない。"])
    a, b = r.sample(["Mg", "Zn", "Fe", "Cu", "Ag", "Ni", "Sn"], 2)
    neg, pos = (a, b) if rank(a) < rank(b) else (b, a)
    right = f"{MNAME[neg]}が負極になり、{MNAME[neg]}が酸化される"
    w = [f"{MNAME[pos]}が負極になり、{MNAME[pos]}が酸化される", f"{MNAME[neg]}が正極になり、{MNAME[neg]}が還元される", f"{MNAME[neg]}が負極になり、{MNAME[neg]}が還元される"]
    why = {w[0]: (f"負極になるのはイオン化傾向の大きい{MNAME[neg]}。", "イオン化傾向と極の対応の誤り"),
           w[1]: (f"{MNAME[neg]}は電子を出す側なので負極。正極ではない。", "正極・負極の定義の誤り"),
           w[2]: ("負極では金属が電子を失って陽イオンになる（酸化）。", "酸化・還元の取り違え")}
    return mc(f"{MNAME[a]}板と{MNAME[b]}板を電解質の水溶液に浸して導線でつなぎ、電池をつくった。このときの説明として正しいものを選びなさい。", [right] + w,
              f"イオン化傾向は {MNAME[neg]} > {MNAME[pos]}。{MNAME[neg]}が電子を出して陽イオンになる（酸化）ので負極。", d=2,
              ap="イオン化傾向の大きい金属が電子を放出して負極になる。電子を失う変化は酸化。",
              steps=[f"イオン化傾向：{MNAME[neg]} > {MNAME[pos]}。", f"{MNAME[neg]}が電子を出す → 負極、酸化反応。", "電子は導線を通って正極へ流れる。"],
              alt=["ダニエル電池（Zn が負極、Cu が正極）と同じ考え方で判断する。"],
              pc=[("負極を正しく判断している", 1), ("酸化・還元を正しく判断している", 1)], why=why,
              pit=["「正」の字から、イオン化傾向の大きい方を正極と考える。"])


SALTS = {"neutral": [("塩化ナトリウム", "NaCl"), ("硝酸カリウム", "KNO3"), ("硫酸ナトリウム", "Na2SO4"), ("塩化カリウム", "KCl")],
         "basic": [("酢酸ナトリウム", "CH3COONa"), ("炭酸ナトリウム", "Na2CO3"), ("炭酸水素ナトリウム", "NaHCO3")],
         "acidic": [("塩化アンモニウム", "NH4Cl"), ("硫酸アンモニウム", "(NH4)2SO4"), ("硫酸水素ナトリウム", "NaHSO4")]}
SALT_WORD = {"neutral": "中性", "basic": "塩基性", "acidic": "酸性"}
SALT_WHY = {"neutral": "強酸と強塩基からなる正塩なので中性", "basic": "弱酸と強塩基からなる塩なので塩基性",
            "acidic": "強酸と弱塩基からなる塩（または酸性塩の硫酸水素ナトリウム）なので酸性"}


@gen("basic_check", 3, ["concept", "condition_check"])
def salt_property(r):
    t = r.choice(list(SALTS))
    right = r.choice(SALTS[t])
    wrongs = []
    for k in SALTS:
        if k != t:
            wrongs += r.sample(SALTS[k], 2 if not wrongs else 1)
    lab = lambda x: f"{x[0]} ${tex(x[1])}$"  # noqa: E731
    why = {}
    for x in wrongs:
        k = [kk for kk in SALTS if x in SALTS[kk]][0]
        why[lab(x)] = (f"{x[0]}は{SALT_WHY[k]}を示す。", "塩の水溶液の性質と、もとの酸・塩基の強弱の対応の誤り")
    return mc(f"次の塩のうち、その水溶液が{SALT_WORD[t]}を示すものを選びなさい。", [lab(right)] + [lab(x) for x in wrongs],
              f"{right[0]}は{SALT_WHY[t]}を示す。", d=2,
              ap="塩をつくっている酸と塩基を考え、強い方の性質が現れると整理する（強酸＋強塩基の正塩は中性）。",
              steps=["塩を陽イオンと陰イオンに分け、もとの塩基と酸を考える。", "強い方の性質を示す。", f"{right[0]}は{SALT_WORD[t]}。"],
              alt=["加水分解で考える：弱酸の陰イオン（$\\mathrm{CH_3COO^-}$ など）は水から $\\mathrm{H^+}$ を受け取って $\\mathrm{OH^-}$ を生じ、弱塩基の陽イオン（$\\mathrm{NH_4^+}$）は $\\mathrm{H^+}$ を与える。"],
              pc=[("もとの酸・塩基を正しく考えている", 1), ("正しく選んでいる", 1)], why=why,
              pit=["「H を含む酸性塩（$\\mathrm{NaHCO_3}$）は必ず酸性」と考える。"])


# ======================================================================
# B 標準演習
# ======================================================================

TA = ["HCl", "HNO3", "H2SO4", "CH3COOH", "(COOH)2"]
TB = ["NaOH", "KOH", "Ba(OH)2", "NH3"]


@gen("standard_practice", 5, ["computation", "application"])
def neutralization(r):
    for _ in range(300):
        fa, fb = r.choice(TA), r.choice(TB)
        a, b = ACIDS[fa][2], BASES[fb][2]
        ca = sp.Rational(r.choice(["0.100", "0.200", "0.0500", "0.150", "0.0800"]))
        cb = sp.Rational(r.choice(["0.100", "0.200", "0.0500", "0.250", "0.120"]))
        Va = sp.Rational(r.choice(["10.0", "20.0", "25.0", "15.0"]))
        Vb = a * ca * Va / (b * cb)
        if clean(Vb, 3) and 4 <= Vb <= 40:
            break
    unknown = r.choice(["Vb", "ca", "cb"])
    an, bn = ACIDS[fa][1], BASES[fb][1]
    eq = f"{a}\\times c_{{\\text{{酸}}}}\\times V_{{\\text{{酸}}}}={b}\\times c_{{\\text{{塩基}}}}\\times V_{{\\text{{塩基}}}}"
    common = dict(ap="酸が出す $\\mathrm{H^+}$ の物質量＝塩基が出す $\\mathrm{OH^-}$ の物質量（価数×モル濃度×体積）で式を立てる。強弱は関係しない。",
                  alt=["物質量を先に求める方法：酸（または塩基）の物質量を mmol 単位で出し、価数をかけて $\\mathrm{H^+}$・$\\mathrm{OH^-}$ の量をそろえる。"],
                  pc=[("価数を含めて式を立てている", 2), ("値が正しい", 2)], pit=["価数を掛け忘れる。", "弱酸・弱塩基では中和に必要な量が少ないと考える。"], d=3)
    if unknown == "Vb":
        return numq(f"{sig(ca, 3)} mol/L の{an} {vfmt(Va)} mL を過不足なく中和するには、{sig(cb, 3)} mol/L の{bn}が何 mL 必要か。", Vb,
                    f"{a}*{dec(ca)}*{dec(Va)}/({b}*{dec(cb)})", f"${a}\\times{sig(ca, 3)}\\times{vfmt(Va)}={b}\\times{sig(cb, 3)}\\times V$ より $V={sig(Vb, 3)}$ mL。", unit="mL", n=3,
                    steps=[f"{ACIDS[fa][0]}は{a}価、{BASES[fb][0]}は{b}価。", f"${a}\\times{sig(ca, 3)}\\times{vfmt(Va)}={b}\\times{sig(cb, 3)}\\times V$。", f"$V={sig(Vb, 3)}$ mL。"], **common)
    if unknown == "ca":
        return numq(f"濃度不明の{an} {vfmt(Va)} mL を、{sig(cb, 3)} mol/L の{bn}で滴定したところ、中和点までに {vfmt(Vb)} mL を要した。{an.replace('水溶液', '')}のモル濃度は何 mol/L か。", ca,
                    f"{b}*{dec(cb)}*{dec(Vb)}/({a}*{dec(Va)})", f"${a}\\times c\\times{vfmt(Va)}={b}\\times{sig(cb, 3)}\\times{vfmt(Vb)}$。", unit="mol/L", n=3,
                    steps=[f"{ACIDS[fa][0]}は{a}価、{BASES[fb][0]}は{b}価。", f"${a}\\times c\\times{vfmt(Va)}={b}\\times{sig(cb, 3)}\\times{vfmt(Vb)}$。", f"$c={sig(ca, 3)}$ mol/L。"], **common)
    return numq(f"{sig(ca, 3)} mol/L の{an} {vfmt(Va)} mL を、濃度不明の{bn}で滴定したところ、中和点までに {vfmt(Vb)} mL を要した。{bn.replace('水溶液', '')}のモル濃度は何 mol/L か。", cb,
                f"{a}*{dec(ca)}*{dec(Va)}/({b}*{dec(Vb)})", f"${eq}$ に代入する。", unit="mol/L", n=3,
                steps=[f"{ACIDS[fa][0]}は{a}価、{BASES[fb][0]}は{b}価。", f"${a}\\times{sig(ca, 3)}\\times{vfmt(Va)}={b}\\times c\\times{vfmt(Vb)}$。", f"$c={sig(cb, 3)}$ mol/L。"], **common)


@gen("standard_practice", 3, ["computation", "condition_check"])
def ph_dilute_weak(r):
    form = r.choice(["dil_a", "dil_b", "weak_a", "weak_b"])
    if form == "dil_a":
        p = r.randint(1, 3)
        k = r.randint(1, 6 - p - 1) if 6 - p - 1 >= 1 else 1
        return num(f"pH {p} の塩酸を水で $10^{{{k}}}$ 倍にうすめた。うすめた後の水溶液の pH を求めなさい。", str(p + k),
                   f"$[\\mathrm{{H^+}}]$ が $\\dfrac{{1}}{{10^{{{k}}}}}$ 倍の ${sci(p + k)}$ mol/L になるので pH {p + k}。", d=2,
                   ap="うすめると $[\\mathrm{H^+}]$ が小さくなる。$10$ 倍うすめるごとに pH は 1 ずつ大きくなる（7 に近づくまで）。",
                   steps=[f"もとの $[\\mathrm{{H^+}}]={sci(p)}$ mol/L。", f"$10^{{{k}}}$ 倍にうすめると ${sci(p + k)}$ mol/L。", f"pH＝{p + k}。"],
                   alt=["結果が 7 未満であることを確かめる（酸をうすめても中性・塩基性にはならない）。"],
                   pc=[("$[\\mathrm{H^+}]$ の変化を正しく考えている", 2), ("pH が正しい", 2)], pit=["pH を $10^{" + str(k) + "}$ 倍してしまう。"],
                   chk=(f"-log(10**(-{p})/10**{k}, 10)", str(p + k)))
    if form == "dil_b":
        p = r.randint(11, 13)
        k = r.randint(1, p - 9)
        return num(f"pH {p} の水酸化ナトリウム水溶液を水で $10^{{{k}}}$ 倍にうすめた。うすめた後の水溶液の pH を求めなさい。{KW}", str(p - k),
                   f"$[\\mathrm{{OH^-}}]$ が ${sci(14 - p)}$ から ${sci(14 - p + k)}$ mol/L になるので pH {p - k}。", d=3,
                   ap="塩基の水溶液では $[\\mathrm{OH^-}]$ がうすまる。$[\\mathrm{OH^-}]$ から $[\\mathrm{H^+}]$ を求め直す。",
                   steps=[f"もとの $[\\mathrm{{H^+}}]={sci(p)}$、$[\\mathrm{{OH^-}}]={sci(14 - p)}$ mol/L。", f"うすめた後 $[\\mathrm{{OH^-}}]={sci(14 - p + k)}$ mol/L。",
                          f"$[\\mathrm{{H^+}}]={sci(p - k)}$ mol/L、pH＝{p - k}。"],
                   alt=["塩基をうすめると pH は 7 に近づく（小さくなる）ことから、向きを確かめる。"],
                   pc=[("$[\\mathrm{OH^-}]$ で考えている", 2), ("pH が正しい", 2)], pit=["$[\\mathrm{H^+}]$ もうすまると考えて pH を大きくしてしまう。"],
                   chk=(f"14+log(10**(-{14 - p})/10**{k}, 10)", str(p - k)))
    combos = [("0.10", "0.010", 3), ("0.010", "0.10", 3), ("0.050", "0.020", 3), ("0.20", "0.0050", 3), ("0.10", "0.0010", 4), ("0.0010", "0.10", 4), ("0.020", "0.050", 3)]
    c, al, pH = r.choice(combos)
    if form == "weak_a":
        return num(f"{c} mol/L の酢酸水溶液の電離度を {al} とする。この水溶液の pH を求めなさい。", str(pH),
                   f"$[\\mathrm{{H^+}}]=c\\alpha={c}\\times{al}={sci(pH)}$ mol/L より pH {pH}。", d=3,
                   ap="弱酸は一部しか電離しない。$[\\mathrm{H^+}]=$（価数）×（モル濃度）×（電離度）。",
                   steps=[f"酢酸は1価の弱酸。", f"$[\\mathrm{{H^+}}]={c}\\times{al}={sci(pH)}$ mol/L。", f"pH＝{pH}。"],
                   alt=["同じ濃度の塩酸（完全電離）の pH と比べ、弱酸の方が pH が大きくなることを確かめる。"],
                   pc=[("電離度を用いて $[\\mathrm{H^+}]$ を求めている", 2), ("pH が正しい", 2)], pit=["電離度を無視して完全に電離したとして計算する。"],
                   chk=(f"-log({c}*{al}, 10)", str(pH)))
    return num(f"{c} mol/L のアンモニア水の電離度を {al} とする。この水溶液の pH を求めなさい。{KW}", str(14 - pH),
               f"$[\\mathrm{{OH^-}}]=c\\alpha={sci(pH)}$ mol/L、$[\\mathrm{{H^+}}]={sci(14 - pH)}$ mol/L より pH {14 - pH}。", d=3,
               ap="アンモニアは1価の弱塩基。$[\\mathrm{OH^-}]=c\\alpha$ を求めてから、水のイオン積を使う。",
               steps=[f"$[\\mathrm{{OH^-}}]={c}\\times{al}={sci(pH)}$ mol/L。", f"$[\\mathrm{{H^+}}]=\\dfrac{{1.0\\times10^{{-14}}}}{{{sci(pH)}}}={sci(14 - pH)}$ mol/L。", f"pH＝{14 - pH}。"],
               alt=[f"pOH＝{pH} を求めて、pH＝14－{pH} としてもよい。"],
               pc=[("$[\\mathrm{OH^-}]$ を求めている", 2), ("pH が正しい", 2)], pit=["$[\\mathrm{OH^-}]$ の指数をそのまま pH とする。"],
               chk=(f"14+log({c}*{al}, 10)", str(14 - pH)))


OXIDANTS = {"MnO4": ("過マンガン酸カリウム水溶液（硫酸酸性）", "\\mathrm{MnO_4^-}+8\\mathrm{H^+}+5\\mathrm{e^-}\\longrightarrow\\mathrm{Mn^{2+}}+4\\mathrm{H_2O}", 5),
            "Cr2O7": ("二クロム酸カリウム水溶液（硫酸酸性）", "\\mathrm{Cr_2O_7^{2-}}+14\\mathrm{H^+}+6\\mathrm{e^-}\\longrightarrow2\\mathrm{Cr^{3+}}+7\\mathrm{H_2O}", 6)}
REDUCTANTS = {"ox": ("シュウ酸水溶液", "\\mathrm{(COOH)_2}\\longrightarrow2\\mathrm{CO_2}+2\\mathrm{H^+}+2\\mathrm{e^-}", 2, "シュウ酸"),
              "h2o2": ("過酸化水素水", "\\mathrm{H_2O_2}\\longrightarrow\\mathrm{O_2}+2\\mathrm{H^+}+2\\mathrm{e^-}", 2, "過酸化水素"),
              "fe": ("硫酸鉄(Ⅱ)水溶液", "\\mathrm{Fe^{2+}}\\longrightarrow\\mathrm{Fe^{3+}}+\\mathrm{e^-}", 1, "硫酸鉄(Ⅱ)")}


@gen("standard_practice", 4, ["computation", "application"])
def redox_titration(r):
    for _ in range(300):
        ok = r.choice(["MnO4", "MnO4", "Cr2O7"])
        rk = r.choice(list(REDUCTANTS)) if ok == "MnO4" else "fe"
        o_name, o_half, ne_o = OXIDANTS[ok]
        r_name, r_half, ne_r, r_short = REDUCTANTS[rk]
        co = sp.Rational(r.choice(["0.0200", "0.0100", "0.0400", "0.0500"]))
        Vo = sp.Rational(r.choice(["8.00", "10.0", "12.0", "16.0", "20.0", "15.0"]))
        Vr = sp.Rational(r.choice(["10.0", "20.0", "25.0"]))
        cr = ne_o * co * Vo / (ne_r * Vr)
        if clean(cr, 3):
            break
    ask_o = r.random() < 0.3
    end = "赤紫色が消えなくなった" if ok == "MnO4" else "反応が完了した"
    halves = f"$${o_half}$$\n$${r_half}$$"
    common = dict(ap="酸化剤が受け取る電子の物質量＝還元剤が出す電子の物質量。半反応式から1 mol あたりの電子の数を読み取る。",
                  alt=["イオン反応式（電子を消去した式）をつくり、物質量の比（例：$\\mathrm{MnO_4^-}:\\mathrm{H_2O_2}=2:5$）から比例で求めてもよい。"],
                  pc=[("電子の数を正しく読み取っている", 2), ("電子の物質量のつり合いの式を立てている", 1), ("値が正しい", 1)],
                  pit=["電子の数（5 と 2 など）を逆に掛ける。", "体積の単位をそろえない。"], d=3)
    if ask_o:
        return numq(f"{sig(cr, 3)} mol/L の{r_name} {vfmt(Vr)} mL と過不足なく反応する {sig(co, 3)} mol/L の{o_name}は何 mL か。半反応式は次のとおりである。\n{halves}", Vo,
                    f"{ne_r}*{dec(cr)}*{dec(Vr)}/({ne_o}*{dec(co)})", f"${ne_o}\\times{sig(co, 3)}\\times V={ne_r}\\times{sig(cr, 3)}\\times{vfmt(Vr)}$。", unit="mL", n=3,
                    steps=[f"酸化剤 1 mol は電子を {ne_o} mol、還元剤 1 mol は電子を {ne_r} mol 授受する。", f"${ne_o}\\times{sig(co, 3)}\\times V={ne_r}\\times{sig(cr, 3)}\\times{vfmt(Vr)}$。",
                           f"$V={sig(Vo, 3)}$ mL。"], **common)
    return numq(f"濃度不明の{r_name} {vfmt(Vr)} mL をコニカルビーカーにとり、{sig(co, 3)} mol/L の{o_name}で滴定したところ、{vfmt(Vo)} mL 加えたところで{end}。{r_short}のモル濃度は何 mol/L か。半反応式は次のとおりである。\n{halves}",
                cr, f"{ne_o}*{dec(co)}*{vfmt(Vo)}/({ne_r}*{vfmt(Vr)})", f"${ne_o}\\times{sig(co, 3)}\\times{vfmt(Vo)}={ne_r}\\times c\\times{vfmt(Vr)}$。", unit="mol/L", n=3,
                steps=[f"酸化剤 1 mol は電子を {ne_o} mol 受け取り、還元剤 1 mol は電子を {ne_r} mol 出す。",
                       f"${ne_o}\\times{sig(co, 3)}\\times\\dfrac{{{vfmt(Vo)}}}{{1000}}={ne_r}\\times c\\times\\dfrac{{{vfmt(Vr)}}}{{1000}}$。", f"$c={sig(cr, 3)}$ mol/L。"], **common)


# (反応式TeX, {物質TeX: 役割}, 酸化剤の説明, 還元剤の説明)
AGENTS = [
    ("\\mathrm{Zn}+\\mathrm{CuSO_4}\\longrightarrow\\mathrm{ZnSO_4}+\\mathrm{Cu}", {"Zn": "red", "CuSO_4": "ox", "ZnSO_4": "prod", "Cu": "prod"}, "Cu：$+2\\to0$", "Zn：$0\\to+2$"),
    ("\\mathrm{Cl_2}+2\\mathrm{KI}\\longrightarrow2\\mathrm{KCl}+\\mathrm{I_2}", {"Cl_2": "ox", "KI": "red", "KCl": "prod", "I_2": "prod"}, "Cl：$0\\to-1$", "I：$-1\\to0$"),
    ("\\mathrm{SO_2}+2\\mathrm{H_2S}\\longrightarrow3\\mathrm{S}+2\\mathrm{H_2O}", {"SO_2": "ox", "H_2S": "red", "S": "prod", "H_2O": "prod"}, "S：$+4\\to0$", "S：$-2\\to0$"),
    ("\\mathrm{Fe_2O_3}+3\\mathrm{CO}\\longrightarrow2\\mathrm{Fe}+3\\mathrm{CO_2}", {"Fe_2O_3": "ox", "CO": "red", "Fe": "prod", "CO_2": "prod"}, "Fe：$+3\\to0$", "C：$+2\\to+4$"),
    ("2\\mathrm{Na}+2\\mathrm{H_2O}\\longrightarrow2\\mathrm{NaOH}+\\mathrm{H_2}", {"Na": "red", "H_2O": "ox", "NaOH": "prod", "H_2": "prod"}, "H：$+1\\to0$", "Na：$0\\to+1$"),
    ("\\mathrm{Mg}+2\\mathrm{HCl}\\longrightarrow\\mathrm{MgCl_2}+\\mathrm{H_2}", {"Mg": "red", "HCl": "ox", "MgCl_2": "prod", "H_2": "prod"}, "H：$+1\\to0$", "Mg：$0\\to+2$"),
    ("\\mathrm{Cu}+2\\mathrm{H_2SO_4}\\longrightarrow\\mathrm{CuSO_4}+\\mathrm{SO_2}+2\\mathrm{H_2O}", {"Cu": "red", "H_2SO_4": "ox", "CuSO_4": "prod", "SO_2": "prod"}, "S：$+6\\to+4$", "Cu：$0\\to+2$"),
    ("3\\mathrm{Cu}+8\\mathrm{HNO_3}\\longrightarrow3\\mathrm{Cu(NO_3)_2}+2\\mathrm{NO}+4\\mathrm{H_2O}", {"Cu": "red", "HNO_3": "ox", "NO": "prod", "Cu(NO_3)_2": "prod"}, "N：$+5\\to+2$", "Cu：$0\\to+2$"),
    ("\\mathrm{H_2O_2}+2\\mathrm{KI}+\\mathrm{H_2SO_4}\\longrightarrow\\mathrm{I_2}+2\\mathrm{H_2O}+\\mathrm{K_2SO_4}", {"H_2O_2": "ox", "KI": "red", "H_2SO_4": "none", "I_2": "prod"}, "O：$-1\\to-2$", "I：$-1\\to0$"),
    ("2\\mathrm{KMnO_4}+5\\mathrm{H_2O_2}+3\\mathrm{H_2SO_4}\\longrightarrow2\\mathrm{MnSO_4}+5\\mathrm{O_2}+8\\mathrm{H_2O}+\\mathrm{K_2SO_4}", {"KMnO_4": "ox", "H_2O_2": "red", "H_2SO_4": "none", "O_2": "prod"}, "Mn：$+7\\to+2$", "O：$-1\\to0$"),
]


@gen("standard_practice", 3, ["concept", "condition_check"])
def agent(r):
    eq, roles, oxs, reds = r.choice(AGENTS)
    want = r.choice(["ox", "red"])
    word = "酸化剤" if want == "ox" else "還元剤"
    right = [k for k, v in roles.items() if v == want][0]
    t = lambda s: f"$\\mathrm{{{s}}}$"  # noqa: E731
    why = {}
    for k, v in roles.items():
        if k == right:
            continue
        if v == "prod":
            why[t(k)] = ("生成物であり、反応を起こさせる側（酸化剤・還元剤）ではない。", "反応物と生成物の取り違え")
        elif v == "none":
            why[t(k)] = ("酸化数が変化しておらず、反応を酸性にするために加えられている。", "酸化数が変化しない物質を酸化剤・還元剤とする誤り")
        else:
            why[t(k)] = (f"この物質は{'還元剤' if v == 'red' else '酸化剤'}（{reds if v == 'red' else oxs} と酸化数が{'増加' if v == 'red' else '減少'}）。", "酸化剤と還元剤の取り違え")
    return mc(f"次の反応で、{word}としてはたらいている物質を選びなさい。\n$${eq}$$", [t(right)] + [t(k) for k in roles if k != right],
              f"酸化数の変化：{oxs}（還元された＝酸化剤）、{reds}（酸化された＝還元剤）。{word}は {t(right)}。", d=3,
              ap="反応の前後で酸化数が変化する原子を探す。酸化数が減少した原子を含む物質が酸化剤、増加した原子を含む物質が還元剤。",
              steps=["反応物の各原子の酸化数を求め、生成物と比べる。", f"{oxs}：還元された → 酸化剤。", f"{reds}：酸化された → 還元剤。"],
              alt=["電子の授受で確かめる：電子を受け取る物質が酸化剤、電子を与える物質が還元剤。"],
              pc=[("酸化数の変化を調べている", 2), ("正しく選んでいる", 2)], why=why,
              pit=["「酸化剤＝酸化される物質」と逆に覚えている。"])


CELLS = [("Zn", "Cu", 2, 2, "65", "64", "亜鉛板を硫酸亜鉛水溶液に、銅板を硫酸銅(Ⅱ)水溶液に浸し、素焼き板で仕切った電池（ダニエル電池）"),
         ("Zn", "Ag", 2, 1, "65", "108", "亜鉛板を硫酸亜鉛水溶液に、銀板を硝酸銀水溶液に浸し、素焼き板で仕切った電池"),
         ("Fe", "Cu", 2, 2, "56", "64", "鉄板を硫酸鉄(Ⅱ)水溶液に、銅板を硫酸銅(Ⅱ)水溶液に浸し、素焼き板で仕切った電池"),
         ("Mg", "Cu", 2, 2, "24", "64", "マグネシウム板を硫酸マグネシウム水溶液に、銅板を硫酸銅(Ⅱ)水溶液に浸し、素焼き板で仕切った電池")]


@gen("standard_practice", 3, ["computation", "application"])
def battery(r):
    neg, pos, zn, zp, mn, mp, desc_ = r.choice(CELLS)
    e = sp.Rational(r.choice(["0.10", "0.20", "0.050", "0.040", "0.020", "0.30"]))
    dneg = e / zn * sp.Rational(mn)
    dpos = e / zp * sp.Rational(mp)
    which = r.choice(["neg", "pos", "e"])
    halfn = f"\\mathrm{{{neg}}}\\longrightarrow\\mathrm{{{neg}^{{2+}}}}+2\\mathrm{{e^-}}"
    halfp = f"\\mathrm{{{pos}^{{{'2+' if zp == 2 else '+'}}}}}+{zp if zp > 1 else ''}\\mathrm{{e^-}}\\longrightarrow\\mathrm{{{pos}}}"
    note = f"原子量は {neg}＝{mn}、{pos}＝{mp} とする。"
    common = dict(ap="負極ではイオン化傾向の大きい金属が溶け出し（酸化）、正極では金属イオンが電子を受け取って析出する（還元）。電子の物質量と半反応式の係数の比で金属の物質量を求める。",
                  alt=["イオン化傾向から負極・正極を先に決め、半反応式を書いてから量的関係を考えると取り違えがない。"],
                  pc=[("負極・正極の反応を正しく書いている", 2), ("電子との物質量の比を用いている", 1), ("値が正しい", 1)],
                  pit=["負極と正極を逆にする。", "金属1 mol あたりの電子の数（価数）を掛け忘れる。"], d=3)
    if which == "neg":
        return numq(f"{desc_}を放電させたところ、導線を電子が {dec(e)} mol 流れた。負極の質量は何 g 減少するか。{note}", dneg,
                    f"{dec(e)}/{zn}*{mn}", f"負極 ${halfn}$ より、{neg} は電子の $\\dfrac{{1}}{{{zn}}}$ の物質量だけ溶け出す。", unit="g",
                    steps=[f"負極（{neg}）：${halfn}$。", f"溶け出す {neg}：${dec(e)}\\div{zn}={sig(e / zn, 3)}$ mol。", f"質量：${sig(e / zn, 3)}\\times{mn}={sig(dneg, 3)}$ g 減少。"], **common)
    if which == "pos":
        return numq(f"{desc_}を放電させたところ、導線を電子が {dec(e)} mol 流れた。正極の質量は何 g 増加するか。{note}", dpos,
                    f"{dec(e)}/{zp}*{mp}", f"正極 ${halfp}$ より、{pos} が析出する。", unit="g",
                    steps=[f"正極（{pos}）：${halfp}$。", f"析出する {pos}：${dec(e)}\\div{zp}={sig(e / zp, 3)}$ mol。", f"質量：${sig(e / zp, 3)}\\times{mp}={sig(dpos, 3)}$ g 増加。"], **common)
    return numq(f"{desc_}を放電させたところ、負極の質量が {dec(dneg)} g 減少した。このとき導線を流れた電子は何 mol か。{note}", e,
                f"{dec(dneg)}/{mn}*{zn}", f"溶け出した {neg} は $\\dfrac{{{dec(dneg)}}}{{{mn}}}$ mol、電子はその {zn} 倍。", unit="mol",
                steps=[f"負極（{neg}）：${halfn}$。", f"溶けた {neg}：$\\dfrac{{{dec(dneg)}}}{{{mn}}}={sig(e / zn, 3)}$ mol。", f"電子：${sig(e / zn, 3)}\\times{zn}={sig(e)}$ mol。"], **common)


INDIC = [("酢酸水溶液", "水酸化ナトリウム水溶液", "wa"), ("酢酸水溶液", "水酸化カリウム水溶液", "wa"), ("シュウ酸水溶液", "水酸化ナトリウム水溶液", "wa"),
         ("塩酸", "アンモニア水", "wb"), ("硫酸", "アンモニア水", "wb"), ("硝酸", "アンモニア水", "wb")]


@gen("standard_practice", 2, ["concept", "condition_check"])
def indicator(r):
    a, b, k = r.choice(INDIC)
    pp = "フェノールフタレイン：中和点が塩基性側にあるから"
    mo = "メチルオレンジ：中和点が酸性側にあるから"
    pp_bad = "フェノールフタレイン：中和点が酸性側にあるから"
    mo_bad = "メチルオレンジ：中和点が塩基性側にあるから"
    right = pp if k == "wa" else mo
    wrong = [mo, pp_bad, mo_bad] if k == "wa" else [pp, pp_bad, mo_bad]
    side = "塩基性" if k == "wa" else "酸性"
    salt = "弱酸と強塩基からなる塩" if k == "wa" else "強酸と弱塩基からなる塩"
    why = {w: (f"この滴定では中和点で生じる塩が{salt}なので、中和点は{side}側にある。{'フェノールフタレイン（変色域 約8.0〜9.8）' if k == 'wa' else 'メチルオレンジ（変色域 約3.1〜4.4）'}が適する。",
               "中和点の pH と指示薬の変色域の対応の誤り") for w in wrong}
    order = r.choice(["前", "後"])
    stem = (f"{a}を{b}で中和滴定する。" if order == "前" else f"{b}を加えて{a}を中和滴定する実験を行う。") + "用いる指示薬とその理由の組み合わせとして最も適当なものを選びなさい。"
    return mc(stem, [right] + wrong, f"中和点で生じる塩は{salt}で、水溶液は{side}を示す。", d=3,
              ap="中和点の水溶液は、生じる塩の性質によって中性とは限らない。中和点付近の pH の急変部分に変色域をもつ指示薬を選ぶ。",
              steps=[f"生じる塩は{salt}。", f"中和点は{side}側。", f"変色域が{side}側にある指示薬を選ぶ。"],
              alt=["滴定曲線をかいて、垂直に近い部分の pH 範囲と指示薬の変色域を重ねて判断する。"],
              pc=[("中和点の液性を判断している", 2), ("指示薬を正しく選んでいる", 2)], why=why,
              pit=["中和点は常に pH 7 だと考える。"])


# ======================================================================
# C 思考力・記述応用
# ======================================================================

CURVE_Q = [
    ("ss", "0.10 mol/L 塩酸 10 mL に 0.10 mol/L 水酸化ナトリウム水溶液を滴下したときの滴定曲線（概形）",
     "図の滴定曲線について、中和点の pH がおよそ 7 になる理由と、この滴定にフェノールフタレインとメチルオレンジのどちらの指示薬も使える理由を説明しなさい。",
     "強酸と強塩基の中和で生じる塩（NaCl）は水溶液中で中性を示すので、中和点の pH はおよそ 7 になる。中和点の前後では pH が約 3 から約 11 まで急激に変化し、その範囲にフェノールフタレイン（約 8.0〜9.8）とメチルオレンジ（約 3.1〜4.4）の変色域がどちらも含まれるため、どちらを使っても滴下量はほとんど変わらない。",
     [("生じる塩が中性であることを述べている", 3), ("中和点付近で pH が大きく変化することを述べている", 3), ("両方の変色域がその範囲に含まれることを述べている", 2)]),
    ("wa", "0.10 mol/L 酢酸水溶液 10 mL に 0.10 mol/L 水酸化ナトリウム水溶液を滴下したときの滴定曲線（概形）",
     "図の滴定曲線について、中和点の pH が 7 より大きくなる理由と、この滴定でメチルオレンジが指示薬として適さない理由を説明しなさい。",
     "弱酸と強塩基の中和で生じる酢酸ナトリウムは、水溶液中で酢酸イオンが水から $\\mathrm{H^+}$ を受け取って $\\mathrm{OH^-}$ を生じるため塩基性を示し、中和点の pH は 7 より大きくなる。pH の急変部分は塩基性側にあるので、変色域が酸性側（約 3.1〜4.4）のメチルオレンジは中和点よりかなり前で変色してしまい、終点を正しく示さない。",
     [("生じる塩が塩基性を示すことを述べている", 3), ("急変部分が塩基性側にあることを述べている", 2), ("メチルオレンジは中和点の前に変色してしまうことを述べている", 3)]),
    ("wb", "0.10 mol/L 塩酸 10 mL に 0.10 mol/L アンモニア水を滴下したときの滴定曲線（概形）",
     "図の滴定曲線について、中和点の pH が 7 より小さくなる理由と、この滴定でフェノールフタレインが指示薬として適さない理由を説明しなさい。",
     "強酸と弱塩基の中和で生じる塩化アンモニウムは、水溶液中でアンモニウムイオンが水に $\\mathrm{H^+}$ を与えるため酸性を示し、中和点の pH は 7 より小さくなる。pH の急変部分は酸性側にあり、中和点を過ぎても pH は 8 程度までしか上がらないので、変色域が塩基性側（約 8.0〜9.8）のフェノールフタレインでは終点を正しく判断できない。",
     [("生じる塩が酸性を示すことを述べている", 3), ("急変部分が酸性側にあることを述べている", 2), ("フェノールフタレインでは終点を判断できないことを述べている", 3)]),
]
GLASS_Q = [
    ("中和滴定で、ホールピペットとビュレットは使用する溶液で内部を数回すすいで（共洗いして）から使うが、コニカルビーカーとメスフラスコは純水でぬれたまま使ってよい。この理由を説明しなさい。",
     "ホールピペットとビュレットは、はかりとる溶液の濃度を変えてはいけない器具である。内部に水が残っていると溶液がうすまり、同じ体積でも含まれる溶質の物質量が変わってしまうので共洗いする。コニカルビーカーは、はかりとった溶質の物質量だけが問題で、水でぬれていても物質量は変わらない。メスフラスコは最後に水を加えて体積を合わせるので、はじめから水が入っていても影響しない。",
     [("ホールピペット・ビュレットでは溶液がうすまって物質量が変わることを述べている", 3), ("コニカルビーカーでは物質量が変わらないことを述べている", 3), ("メスフラスコは後で水を加えるので影響しないことを述べている", 2)],
     "それぞれの器具で、「溶液の濃度」と「溶質の物質量」のどちらが結果に影響するかを考える。"),
    ("「中和点」と「中性」は同じ意味ではない。このことを、酢酸水溶液と水酸化ナトリウム水溶液の中和を例にして説明しなさい。",
     "中和点は、酸の出す $\\mathrm{H^+}$ と塩基の出す $\\mathrm{OH^-}$ の物質量が等しくなり、過不足なく反応した点である。酢酸と水酸化ナトリウムの中和点では酢酸ナトリウムの水溶液になるが、酢酸イオンが水と反応して $\\mathrm{OH^-}$ を生じるため、水溶液は弱い塩基性を示す。したがって中和点でも pH は 7 にならず、中和点＝中性とは限らない。",
     [("中和点の意味（物質量の関係）を正しく述べている", 3), ("生じる塩が塩基性を示すことを述べている", 3), ("中和点と中性が一致しない理由をまとめている", 2)],
     "中和点は「量」の概念、中性は「pH」の概念であることを区別する。"),
    ("塩酸と酢酸水溶液が同じモル濃度・同じ体積あるとき、pH は塩酸の方が小さいが、中和に必要な水酸化ナトリウム水溶液の体積は等しい。この理由を説明しなさい。",
     "塩酸は強酸でほぼ完全に電離するが、酢酸は弱酸で一部しか電離しないので、$[\\mathrm{H^+}]$ は塩酸の方が大きく pH は小さい。一方、中和では $\\mathrm{H^+}$ が消費されると酢酸の電離が進み、最終的に酢酸はすべて反応する。どちらも1価の酸で物質量が等しいので、出しうる $\\mathrm{H^+}$ の物質量が等しく、必要な水酸化ナトリウムの量は等しい。",
     [("電離度のちがいで pH の差を説明している", 3), ("中和で弱酸の電離が進み、すべて反応することを述べている", 3), ("価数と物質量が等しいことから結論を導いている", 2)],
     "pH は「今どれだけ電離しているか」、中和の量は「最終的に出しうる $\\mathrm{H^+}$ の量」で決まる。"),
]


@gen("thinking_writing", 3, ["written_reasoning", "condition_check"])
def titration_reason(r):
    if r.random() < 0.5:
        kind, cap, stem, ans, rub = r.choice(CURVE_Q)
        return desc(stem, ans, "中和点で生じる塩の性質と、pH の急変部分の位置から考える。", rub, d=4, p=8, lines=8, fig=titration_fig(kind, cap),
                    ap="図から中和点（滴下量 10 mL）の pH と、急変部分の pH の範囲を読み取る。生じる塩がどの酸・塩基からできているかで液性が決まる。",
                    steps=["中和点で生じる塩を特定し、その水溶液の液性を考える。", "図から pH の急変する範囲を読み取る。", "指示薬の変色域が急変範囲に入っているかを確かめる。"],
                    alt=["塩の加水分解（弱酸の陰イオンが $\\mathrm{OH^-}$ を、弱塩基の陽イオンが $\\mathrm{H^+}$ を生じる）を、イオン反応式を用いて説明してもよい。"],
                    pc=[(a, b) for a, b in rub], pit=["中和点は常に pH 7 だと考える。", "指示薬の変色域を覚えていない。"])
    stem, ans, rub, ap = r.choice(GLASS_Q)
    return desc(stem, ans, "物質量・濃度・電離度といった概念のどれが関係しているかを区別して説明する。", rub, d=4, p=8, lines=8,
                ap=ap, steps=["問われている2つの事柄を、それぞれ何で決まるかに分ける。", "具体的な粒子（$\\mathrm{H^+}$・溶質）の物質量の変化で説明する。", "結論を1文でまとめる。"],
                alt=["具体的な数値（例：0.10 mol/L、10 mL）を仮定して計算し、説明を裏づけてもよい。"],
                pc=[(a, b) for a, b in rub], pit=["「濃度」と「物質量」を区別せずに説明する。"])


@gen("thinking_writing", 4, ["cross_unit", "computation", "written_reasoning"], rel=["HS-CHEB-U02"])
def back_titration(r):
    form = r.choice(["back", "mix", "mix"])
    if form == "back":
        cs = sp.Rational(r.choice(["0.050", "0.100", "0.0500"]))
        Vs = r.choice([50, 40, 25])
        nh = 2 * cs * Vs  # mmol of H+
        for _ in range(100):
            cn = sp.Rational(r.choice(["0.10", "0.20", "0.050"]))
            vn = sp.Rational(r.choice(["10.0", "12.0", "15.0", "16.0", "20.0", "8.0", "5.0"]))
            nnh3 = nh - cn * vn
            if nnh3 > 0:
                break
        Vml = nnh3 * sp.Rational("22.4")
        return desc(f"ある量のアンモニアを、{sig(cs)} mol/L の硫酸 {Vs} mL にすべて吸収させた。残った硫酸を {sig(cn)} mol/L の水酸化ナトリウム水溶液で滴定したところ、中和に {dec(vn)} mL を要した。"
                    f"吸収させたアンモニアの体積は標準状態で何 mL か。考え方も書き、有効数字2桁で答えなさい。標準状態の気体のモル体積は 22.4 L/mol とする。",
                    f"${sig(Vml)}$ mL", "硫酸の出す $\\mathrm{H^+}$ の物質量＝アンモニアが受け取る量＋NaOH が受け取る量。",
                    [("硫酸の $\\mathrm{H^+}$ の物質量（価数2）を求めている", 2), ("$\\mathrm{H^+}$ の総量＝$\\mathrm{NH_3}$＋NaOH の関係を立てている", 3),
                     ("アンモニアの物質量を求めている", 1), ("標準状態の体積に換算している", 2)],
                    d=5, p=8, lines=9,
                    ap="逆滴定：酸の $\\mathrm{H^+}$ は、まずアンモニアと、残りが NaOH と中和した。酸が出す $\\mathrm{H^+}$ の総量＝アンモニア＋NaOH が受け取る量。気体の体積への換算は前単元（物質量）の内容。",
                    steps=[f"硫酸の $\\mathrm{{H^+}}$：$2\\times{sig(cs)}\\times{Vs}={dec(nh)}$ mmol。", f"NaOH：${sig(cn)}\\times{dec(vn)}={dec(cn * vn)}$ mmol。",
                           f"$\\mathrm{{NH_3}}$（1価の塩基）：${dec(nh)}-{dec(cn * vn)}={dec(nnh3)}$ mmol。", f"体積：${dec(nnh3)}\\times10^{{-3}}\\times22.4\\times10^3={sig(Vml)}$ mL。"],
                    alt=["物質量を mol 単位で計算してもよい（mmol は計算を簡単にするための単位）。", "図（$\\mathrm{H^+}$ の総量を NH₃ と NaOH で分け合う帯図）をかくと関係が見やすい。"],
                    pc=[("硫酸", 2), ("関係式", 3), ("NH₃", 1), ("体積", 2)],
                    pit=["硫酸の価数 2 を忘れる。", "mmol と mL の換算で 1000 倍の誤りをする。"],
                    chk=(f"(2*{dec(cs)}*{Vs}-{dec(cn)}*{dec(vn)})*22.4", str(Vml), None, "intermediate"))
    c = sp.Rational(r.choice(["0.10", "0.20", "0.050"]))
    k = r.choice([2, 3])
    diff = sp.Rational(100, 1) * sp.Integer(10) ** (-k) / c  # mL difference giving [H+] = 10^-k in 100 mL total
    va = (100 + diff) / 2
    vb = (100 - diff) / 2
    acid_excess = r.random() < 0.6
    ion_ex = "$\\mathrm{H^+}$" if acid_excess else "$\\mathrm{OH^-}$"
    if acid_excess:
        Va, Vb = va, vb
        ans_ph = k
    else:
        Va, Vb = vb, va
        ans_ph = 14 - k
    return desc(f"{sig(c)} mol/L の塩酸 {dec(Va)} mL と {sig(c)} mol/L の水酸化ナトリウム水溶液 {dec(Vb)} mL を混合した。混合後の水溶液の pH を、考え方とともに求めなさい。"
                f"混合による体積の変化はなく、{KW}",
                f"pH {ans_ph}", "中和で残った $\\mathrm{H^+}$ または $\\mathrm{OH^-}$ の物質量を、混合後の全体積で割る。",
                [("$\\mathrm{H^+}$ と $\\mathrm{OH^-}$ の物質量をそれぞれ求めている", 2), ("余るイオンとその物質量を求めている", 2), ("全体積で割って濃度を求めている", 2), ("pH を正しく求めている", 2)],
                d=4, p=8, lines=8,
                ap="混合で $\\mathrm{H^+}+\\mathrm{OH^-}\\longrightarrow\\mathrm{H_2O}$ が起こり、多い方が余る。余ったイオンの濃度は「余った物質量÷混合後の体積」（物質量とモル濃度は前単元の内容）。",
                steps=[f"$\\mathrm{{H^+}}$：${sig(c)}\\times{vfmt(Va)}={dec(c * Va)}$ mmol、$\\mathrm{{OH^-}}$：${sig(c)}\\times{vfmt(Vb)}={dec(c * Vb)}$ mmol。",
                       f"{ion_ex} が ${dec(abs(c * Va - c * Vb))}$ mmol 余る。",
                       f"混合後 100 mL なので濃度は ${sci(k)}$ mol/L。", f"pH＝{ans_ph}。"],
                alt=["体積の差 " + dec(diff) + " mL 分だけ一方が余ると考え、その分を 100 mL にうすめた濃度を求めてもよい。"],
                pc=[("物質量", 2), ("余り", 2), ("濃度", 2), ("pH", 2)],
                pit=["混合後の体積で割らず、もとの体積で割る。", "塩基が余ったときに $[\\mathrm{OH^-}]$ の指数をそのまま pH とする。"],
                chk=(f"{'-' if acid_excess else '14+'}log(Abs({dec(c)}*{dec(Va)}-{dec(c)}*{dec(Vb)})/100, 10)", str(ans_ph), None, "intermediate"))


HALF = [("過マンガン酸カリウム（硫酸酸性）", "シュウ酸", "\\mathrm{MnO_4^-}+8\\mathrm{H^+}+5\\mathrm{e^-}\\longrightarrow\\mathrm{Mn^{2+}}+4\\mathrm{H_2O}",
         "\\mathrm{(COOH)_2}\\longrightarrow2\\mathrm{CO_2}+2\\mathrm{H^+}+2\\mathrm{e^-}", 5, 2,
         "2\\mathrm{MnO_4^-}+5\\mathrm{(COOH)_2}+6\\mathrm{H^+}\\longrightarrow2\\mathrm{Mn^{2+}}+10\\mathrm{CO_2}+8\\mathrm{H_2O}", "2:5", "2*(-1)+6*1-2*2"),
        ("過マンガン酸カリウム（硫酸酸性）", "過酸化水素", "\\mathrm{MnO_4^-}+8\\mathrm{H^+}+5\\mathrm{e^-}\\longrightarrow\\mathrm{Mn^{2+}}+4\\mathrm{H_2O}",
         "\\mathrm{H_2O_2}\\longrightarrow\\mathrm{O_2}+2\\mathrm{H^+}+2\\mathrm{e^-}", 5, 2,
         "2\\mathrm{MnO_4^-}+5\\mathrm{H_2O_2}+6\\mathrm{H^+}\\longrightarrow2\\mathrm{Mn^{2+}}+5\\mathrm{O_2}+8\\mathrm{H_2O}", "2:5", "2*(-1)+6*1-2*2"),
        ("過マンガン酸カリウム（硫酸酸性）", "鉄(Ⅱ)イオン", "\\mathrm{MnO_4^-}+8\\mathrm{H^+}+5\\mathrm{e^-}\\longrightarrow\\mathrm{Mn^{2+}}+4\\mathrm{H_2O}",
         "\\mathrm{Fe^{2+}}\\longrightarrow\\mathrm{Fe^{3+}}+\\mathrm{e^-}", 5, 1,
         "\\mathrm{MnO_4^-}+5\\mathrm{Fe^{2+}}+8\\mathrm{H^+}\\longrightarrow\\mathrm{Mn^{2+}}+5\\mathrm{Fe^{3+}}+4\\mathrm{H_2O}", "1:5", "(-1)+5*2+8*1-(2+5*3)"),
        ("二クロム酸カリウム（硫酸酸性）", "鉄(Ⅱ)イオン", "\\mathrm{Cr_2O_7^{2-}}+14\\mathrm{H^+}+6\\mathrm{e^-}\\longrightarrow2\\mathrm{Cr^{3+}}+7\\mathrm{H_2O}",
         "\\mathrm{Fe^{2+}}\\longrightarrow\\mathrm{Fe^{3+}}+\\mathrm{e^-}", 6, 1,
         "\\mathrm{Cr_2O_7^{2-}}+6\\mathrm{Fe^{2+}}+14\\mathrm{H^+}\\longrightarrow2\\mathrm{Cr^{3+}}+6\\mathrm{Fe^{3+}}+7\\mathrm{H_2O}", "1:6", "(-2)+6*2+14*1-(2*3+6*3)"),
        ("過酸化水素（硫酸酸性）", "ヨウ化物イオン", "\\mathrm{H_2O_2}+2\\mathrm{H^+}+2\\mathrm{e^-}\\longrightarrow2\\mathrm{H_2O}",
         "2\\mathrm{I^-}\\longrightarrow\\mathrm{I_2}+2\\mathrm{e^-}", 2, 2,
         "\\mathrm{H_2O_2}+2\\mathrm{I^-}+2\\mathrm{H^+}\\longrightarrow\\mathrm{I_2}+2\\mathrm{H_2O}", "1:2", "2*(-1)+2*1"),
        ("二酸化硫黄", "硫化水素", "\\mathrm{SO_2}+4\\mathrm{H^+}+4\\mathrm{e^-}\\longrightarrow\\mathrm{S}+2\\mathrm{H_2O}",
         "\\mathrm{H_2S}\\longrightarrow\\mathrm{S}+2\\mathrm{H^+}+2\\mathrm{e^-}", 4, 2,
         "\\mathrm{SO_2}+2\\mathrm{H_2S}\\longrightarrow3\\mathrm{S}+2\\mathrm{H_2O}", "1:2", "0"),
        ("二クロム酸カリウム（硫酸酸性）", "過酸化水素", "\\mathrm{Cr_2O_7^{2-}}+14\\mathrm{H^+}+6\\mathrm{e^-}\\longrightarrow2\\mathrm{Cr^{3+}}+7\\mathrm{H_2O}",
         "\\mathrm{H_2O_2}\\longrightarrow\\mathrm{O_2}+2\\mathrm{H^+}+2\\mathrm{e^-}", 6, 2,
         "\\mathrm{Cr_2O_7^{2-}}+3\\mathrm{H_2O_2}+8\\mathrm{H^+}\\longrightarrow2\\mathrm{Cr^{3+}}+3\\mathrm{O_2}+7\\mathrm{H_2O}", "1:3", "(-2)+8*1-2*3")]


@gen("thinking_writing", 3, ["written_reasoning", "multiple_solutions"])
def half_reaction(r):
    on, rn, oh, rh, eo, er, ionic, ratio, charge = r.choice(HALF)
    l = math.lcm(eo, er)
    return desc(f"{on}と{rn}の反応について、次の2つの半反応式から電子 $\\mathrm{{e^-}}$ を消去してイオン反応式をつくり、酸化剤と還元剤が反応する物質量の比を答えなさい。考え方も書きなさい。\n$${oh}$$\n$${rh}$$",
                f"$${ionic}$$ 酸化剤：還元剤＝{ratio}（物質量の比）",
                f"授受される電子の数を最小公倍数 {l} にそろえて足し合わせる。",
                [("電子の数をそろえる倍数を正しく選んでいる", 2), ("2式を足して電子を消去し、両辺の同じ物質を整理している", 3), ("物質量の比を正しく答えている", 2), ("電荷・原子の数のつり合いを確認している", 1)],
                d=4, p=8, lines=8,
                ap="酸化剤が受け取る電子の数と還元剤が出す電子の数が等しくなるように、それぞれの半反応式を整数倍する。",
                steps=[f"酸化剤 1 mol は電子 {eo} mol を受け取り、還元剤 1 mol は電子 {er} mol を出す。",
                       f"最小公倍数 {l} にそろえる：酸化剤の式を {l // eo} 倍、還元剤の式を {l // er} 倍する。",
                       "2式を足して $\\mathrm{e^-}$ を消去し、両辺に共通する $\\mathrm{H^+}$ や $\\mathrm{H_2O}$ を整理する。", f"${ionic}$。"],
                alt=[f"電子の物質量のつり合い ${eo}\\times n_{{\\text{{酸化剤}}}}={er}\\times n_{{\\text{{還元剤}}}}$ から、比 {ratio} を直接求めることもできる（イオン反応式をつくらない解法）。",
                     "完成した式で、両辺の電荷の総和と各原子の数が等しいことを確かめる。"],
                pc=[("倍数", 2), ("電子の消去と整理", 3), ("物質量の比", 2), ("確認", 1)],
                pit=["電子の数をそろえずに足し合わせる。", "両辺の $\\mathrm{H^+}$ を相殺し忘れる。"],
                chk=(charge, "0", None, "intermediate"))


# ======================================================================
# D 典型誤答訂正
# ======================================================================

@gen("error_correction", 3, ["common_error", "computation"])
def err_ph(r):
    form = r.choice(["base", "dilute", "weak"])
    if form == "base":
        f = r.choice(["NaOH", "KOH"])
        k = r.randint(1, 4)
        return err_item(f"${sci(k)}$ mol/L の{BASES[f][1]}の pH を求めなさい。{BASES[f][0]}は完全に電離し、{KW}",
                        f"$[\\mathrm{{OH^-}}]={sci(k)}$ mol/L なので pH＝{k}",
                        "$[\\mathrm{OH^-}]$ から直接 pH を求めた部分", "concept",
                        "pH の計算に慣れて「濃度の指数を読めば pH」と機械的に処理し、pH が $[\\mathrm{H^+}]$ で定義されることを忘れている。",
                        f"$[\\mathrm{{H^+}}]=\\dfrac{{1.0\\times10^{{-14}}}}{{{sci(k)}}}={sci(14 - k)}$ mol/L より pH＝{14 - k}", f"pH {14 - k}",
                        "pH は $[\\mathrm{H^+}]$ で定義される。塩基性の水溶液では水のイオン積から $[\\mathrm{H^+}]$ を求める。",
                        [f"$[\\mathrm{{OH^-}}]={sci(k)}$ mol/L。", f"$[\\mathrm{{H^+}}]={sci(14 - k)}$ mol/L。", f"pH＝{14 - k}。"],
                        "求めた pH が塩基性（7 より大きい）になっているかを確かめる。",
                        [f"誤答の pH {k} は酸性を表すので、塩基の水溶液としておかしいと気づける。"], ["$[\\mathrm{OH^-}]$ の指数をそのまま pH とする。"],
                        chk=(f"14+log(10**(-{k}), 10)", str(14 - k), None, "intermediate"), d=2)
    if form == "dilute":
        p = r.choice([4, 5, 6])
        k = r.choice([3, 4, 5])
        return err_item(f"pH {p} の塩酸を水で $10^{{{k}}}$ 倍にうすめたときの pH はおよそいくらか。",
                        f"10 倍うすめるごとに pH は 1 大きくなるので、pH＝{p}＋{k}＝{p + k}",
                        "うすめた後の pH を計算した部分", "condition",
                        "「10 倍うすめると pH が 1 大きくなる」という規則を、適用できる範囲（水の電離が無視できる範囲）をこえて使っている。",
                        f"$[\\mathrm{{H^+}}]$ は {sci(p + k)} mol/L 程度まで小さくなるが、水の電離による $1.0\\times10^{{-7}}$ mol/L の方が大きくなるので、pH はほぼ 7（わずかに 7 より小さい）",
                        "pH はほぼ 7（7 よりわずかに小さい）",
                        "酸をどれだけうすめても塩基性にはならない。$[\\mathrm{H^+}]$ が $10^{-7}$ mol/L 程度より小さくなると、水自身の電離による $\\mathrm{H^+}$ が無視できなくなる。",
                        [f"塩酸由来の $[\\mathrm{{H^+}}]$ は ${sci(p + k)}$ mol/L。", "水の電離による $[\\mathrm{H^+}]\\fallingdotseq1.0\\times10^{-7}$ mol/L の方が大きい。", "pH はほぼ 7。"],
                        "規則を使う前に、結果が化学的にありうるか（酸性の水溶液が塩基性になっていないか）を確かめる。",
                        ["極端な場合を考える：純水にごくわずかの塩酸を加えても pH はほぼ 7 である。"], ["酸をうすめ続けると pH が 7 をこえると考える。"], d=3)
    c, al, pH = r.choice([("0.10", "0.010", 3), ("0.010", "0.10", 3), ("0.050", "0.020", 3), ("0.10", "0.0010", 4)])
    wrong = -sp.log(sp.Rational(c), 10)
    wtxt = sp.nsimplify(wrong)
    w_disp = str(wtxt) if wtxt.is_Integer else f"約 {float(wrong):.1f}"
    return err_item(f"{c} mol/L の酢酸水溶液（電離度 {al}）の pH を求めなさい。",
                    f"$[\\mathrm{{H^+}}]={c}$ mol/L なので pH＝{w_disp}",
                    "$[\\mathrm{H^+}]$ を求めた部分", "concept",
                    "強酸の計算と同じように、モル濃度をそのまま $[\\mathrm{H^+}]$ とし、電離度を使っていない。",
                    f"$[\\mathrm{{H^+}}]={c}\\times{al}={sci(pH)}$ mol/L より pH＝{pH}", f"pH {pH}",
                    "酢酸は弱酸で一部しか電離しない。$[\\mathrm{H^+}]=c\\alpha$。",
                    [f"$[\\mathrm{{H^+}}]=c\\alpha={c}\\times{al}$。", f"$={sci(pH)}$ mol/L。", f"pH＝{pH}。"],
                    "弱酸・弱塩基では必ず電離度をかける。",
                    ["同じ濃度の塩酸より pH が大きく（酸性が弱く）なっているかで確かめる。"], ["弱酸を完全に電離するとして計算する。"],
                    chk=(f"-log({c}*{al}, 10)", str(pH), None, "intermediate"), d=2)


@gen("error_correction", 4, ["common_error", "condition_check"])
def err_valence(r):
    form = r.choice(["h2so4", "base2", "ox", "weak"])
    if form == "weak":
        c = r.choice(["0.10", "0.20", "0.050"])
        V = r.choice(["10.0", "20.0", "25.0"])
        need = sp.Rational(c) * sp.Rational(V) / sp.Rational(c)
        return err_item(f"{c} mol/L の酢酸水溶液 {V} mL を過不足なく中和するのに必要な {c} mol/L の水酸化ナトリウム水溶液の体積を求めなさい。",
                        f"酢酸は弱酸で一部しか電離しないので、中和に必要な水酸化ナトリウム水溶液は {V} mL より少ない",
                        "弱酸の中和の量を判断した部分", "concept",
                        "pH（電離している $\\mathrm{H^+}$ の量）と、中和できる量（出しうる $\\mathrm{H^+}$ の総量）を混同している。",
                        f"中和が進むと酢酸の電離が進み、すべて反応する。$1\\times{c}\\times{V}=1\\times{c}\\times V$ より $V={vfmt(need)}$ mL", f"{vfmt(need)} mL",
                        "中和の量的関係は価数と物質量で決まり、酸・塩基の強弱には関係しない。",
                        ["酢酸は1価の酸、NaOH は1価の塩基。", f"$1\\times{c}\\times{V}=1\\times{c}\\times V$。", f"$V={vfmt(need)}$ mL。"],
                        "「H⁺ の物質量＝OH⁻ の物質量」で式を立て、強弱は使わない。",
                        ["同じ濃度・同じ体積の塩酸を中和する場合と比べ、必要量が同じになることを確かめる。"], ["電離度を中和の計算に使う。"],
                        chk=(f"{c}*{V}/{c}", str(need), None, "intermediate"), d=2)
    for _ in range(100):
        if form == "h2so4":
            fa, fb = r.choice(["H2SO4", "(COOH)2"]), r.choice(["NaOH", "KOH"])
        elif form == "base2":
            fa, fb = r.choice(["HCl", "HNO3"]), "Ba(OH)2"
        else:
            fa, fb = "(COOH)2", r.choice(["NaOH", "KOH"])
        a, b = ACIDS[fa][2], BASES[fb][2]
        ca = sp.Rational(r.choice(["0.100", "0.0500", "0.200"]))
        cb = sp.Rational(r.choice(["0.100", "0.200", "0.0500"]))
        Va = sp.Rational(r.choice(["10.0", "20.0", "25.0"]))
        Vb = a * ca * Va / (b * cb)
        wrongV = ca * Va / cb
        if clean(Vb, 3) and clean(wrongV, 3) and 2 <= Vb <= 60:
            break
    an, bn = ACIDS[fa][1], BASES[fb][1]
    return err_item(f"{sig(ca, 3)} mol/L の{an} {vfmt(Va)} mL を過不足なく中和するのに必要な {sig(cb, 3)} mol/L の{bn}は何 mL か。",
                    f"${sig(ca, 3)}\\times{vfmt(Va)}={sig(cb, 3)}\\times V$ より $V={sig(wrongV, 3)}$ mL",
                    "中和の式（価数）", "formula",
                    f"「濃度×体積」が等しいと覚えていて、{ACIDS[fa][0] if a == 2 else BASES[fb][0]}が2価であることを式に入れていない。",
                    f"${a}\\times{sig(ca, 3)}\\times{vfmt(Va)}={b}\\times{sig(cb, 3)}\\times V$ より $V={sig(Vb, 3)}$ mL", f"{sig(Vb, 3)} mL",
                    "中和では $\\mathrm{H^+}$ の物質量と $\\mathrm{OH^-}$ の物質量が等しい。それぞれ価数×物質量で求める。",
                    [f"{ACIDS[fa][0]}は{a}価、{BASES[fb][0]}は{b}価。", f"${a}\\times{sig(ca, 3)}\\times{vfmt(Va)}={b}\\times{sig(cb, 3)}\\times V$。", f"$V={sig(Vb, 3)}$ mL。"],
                    "中和の式には必ず価数を書く。",
                    [f"電離式（例：${tex(fa)}$ や ${tex(fb)}$）をかいて、1 mol から生じる $\\mathrm{{H^+}}$・$\\mathrm{{OH^-}}$ の数を確かめる。"], ["価数を掛け忘れる。"],
                    chk=(f"{a}*{dec(ca)}*{dec(Va)}/({b}*{dec(cb)})", str(Vb), None, "intermediate"), d=3)


@gen("error_correction", 3, ["common_error", "concept"])
def err_redox(r):
    form = r.choice(["ion_sum", "h2o2", "cell", "agent"])
    if form == "ion_sum":
        item = r.choice([x for x in OX if x[2] != 0])
        ft, el, q, others, k, name = item
        v = ox_value(item)
        wv = sp.Rational(0 - sum(c * o for _, c, o in others), k)
        lhs = (f"{k}x" if k > 1 else "x") + "+" + "+".join(f"({sgn_s(o)})\\times{c}" for _, c, o in others)
        return err_item(f"$\\mathrm{{{ft}}}$（{name}）中の {el} の酸化数を求めなさい。",
                        f"{el} の酸化数を $x$ とすると、総和は 0 なので ${lhs}=0$、$x={sgn_s(wv)}$",
                        "酸化数の総和を 0 とした部分", "condition",
                        "化合物の「総和 0」の規則を、イオンにもそのまま当てはめている。",
                        f"イオンなので総和は電荷 ${sgn_s(q)}$：${lhs}={q}$ より $x={sgn_s(v)}$", sgn_s(v),
                        "多原子イオンでは、酸化数の総和はイオンの電荷に等しい。",
                        [f"{el} の酸化数を $x$ とする。", f"総和＝電荷：${lhs}={q}$。", f"$x={sgn_s(v)}$。"],
                        "化学式の右上の電荷を確認してから方程式を立てる。",
                        ["既知の値と照合する（例：$\\mathrm{MnO_4^-}$ の Mn は $+7$、$\\mathrm{SO_4^{2-}}$ の S は $+6$）。"], ["イオンの電荷を無視する。"],
                        chk=(f"solve({k}*x+({'+'.join(f'{c}*({o})' for _, c, o in others)})-({q}), x)[0]", str(v), None, "intermediate"), d=2)
    if form == "h2o2":
        return err_item("過酸化水素 $\\mathrm{H_2O_2}$ 中の O と H の酸化数をそれぞれ求めなさい。",
                        "O は $-2$ なので、H の酸化数を $x$ とすると $2x+(-2)\\times2=0$、$x=+2$",
                        "O の酸化数を −2 とした部分", "condition",
                        "「O は −2」という規則を例外なく当てはめ、H が ＋2 という不自然な結果を見直していない。",
                        "H を ＋1 とすると $2\\times(+1)+2y=0$ より O は $-1$", "O は $-1$、H は $+1$",
                        "過酸化水素は O−O 結合をもつ過酸化物で、O の酸化数は例外的に −1 になる。H は ＋1 のまま。",
                        ["H は ＋1 と決める。", "O の酸化数を $y$ として $2\\times(+1)+2y=0$。", "$y=-1$。"],
                        "規則どうしが矛盾するときは、H＝＋1 を優先し、過酸化物の O を −1 とする。",
                        ["$\\mathrm{H_2O_2}$ が酸化剤（O：$-1\\to-2$）にも還元剤（O：$-1\\to0$）にもなることと結びつけて確かめる。"], ["H の酸化数が ＋2 になる不自然さに気づかない。"],
                        chk=("solve(2*1+2*x, x)[0]", "-1", None, "intermediate"), d=2)
    if form == "cell":
        neg, pos = r.choice([("Zn", "Cu"), ("Fe", "Cu"), ("Zn", "Ag"), ("Mg", "Zn")])
        return err_item(f"{MNAME[neg]}板と{MNAME[pos]}板を用いた電池で、負極・正極はどちらか。また、導線を流れる電子の向きを答えなさい。",
                        f"イオン化傾向の大きい{MNAME[neg]}が正極、{MNAME[pos]}が負極。電子は正極（{MNAME[neg]}）から負極（{MNAME[pos]}）へ流れる",
                        "正極・負極の判断", "concept",
                        "「イオン化傾向が大きい＝反応が活発＝プラス（正）」という言葉のイメージで判断している。",
                        f"{MNAME[neg]}が電子を出す負極、{MNAME[pos]}が正極。電子は負極（{MNAME[neg]}）から導線を通って正極（{MNAME[pos]}）へ流れる",
                        f"負極：{MNAME[neg]}、正極：{MNAME[pos]}。電子は{MNAME[neg]}から{MNAME[pos]}へ流れる。",
                        "イオン化傾向の大きい金属が電子を放出して陽イオンになる（酸化）。電子を送り出す電極が負極である。",
                        [f"イオン化傾向：{MNAME[neg]} > {MNAME[pos]}。", f"{MNAME[neg]}：${{\\mathrm{{{neg}}}}}\\longrightarrow\\mathrm{{{neg}^{{2+}}}}+2\\mathrm{{e^-}}$（負極）。",
                         f"電子は{MNAME[neg]}から{MNAME[pos]}へ。電流はその逆向き。"],
                        "「負極＝電子を出す＝酸化」とセットで判断する。",
                        ["ダニエル電池（Zn が負極）と比べて確かめる。"], ["電流の向きと電子の向きを混同する。"], d=2)
    eq, roles, oxs, reds = r.choice(AGENTS)
    ox = [k for k, v in roles.items() if v == "ox"][0]
    red = [k for k, v in roles.items() if v == "red"][0]
    return err_item(f"次の反応で、酸化剤としてはたらいている物質を答えなさい。\n$${eq}$$",
                    f"{reds} と酸化数が増加しているので、$\\mathrm{{{red}}}$ が酸化剤",
                    "酸化数の増加から酸化剤を判断した部分", "concept",
                    "「酸化された物質＝酸化剤」と、言葉の形から逆の対応で覚えている。",
                    f"{oxs} と酸化数が減少した（還元された）$\\mathrm{{{ox}}}$ が酸化剤", f"$\\mathrm{{{ox}}}$",
                    "酸化剤は相手を酸化し、自身は還元される（酸化数が減少する）物質である。",
                    [f"{reds}：酸化された → 還元剤 $\\mathrm{{{red}}}$。", f"{oxs}：還元された → 酸化剤 $\\mathrm{{{ox}}}$。"],
                    "「酸化剤は相手を酸化する薬」→ 自分は逆の還元、と言いかえて確認する。",
                    ["電子の授受で確かめる：電子を受け取る物質が酸化剤。"], ["酸化剤と還元剤を逆に覚える。"], d=2)


GENERATORS = [ph_basic, oxidation_number, acid_base_class, ionization_tendency, salt_property,
              neutralization, ph_dilute_weak, redox_titration, agent, battery, indicator,
              titration_reason, back_titration, half_reaction,
              err_ph, err_valence, err_redox]
