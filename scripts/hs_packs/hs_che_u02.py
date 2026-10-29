"""単元パック：化学 化学反応とエネルギー・化学平衡（反応エンタルピー・反応速度・化学平衡・電離平衡）。"""
import math
import re
from decimal import ROUND_HALF_UP, Decimal

import sympy as sp

from banks._common import desc, figure, mc, num, plane, sa, table
from hs_pack_lib import board, check, definition, derivation, example, figure_explain, gen, guide, intro, lesson, summary, theorem, tp

UNIT_ID = "HS-CHE-U02"

LOGS = "$\\log_{10}2=0.30$、$\\log_{10}3=0.48$ とする。"
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


def sci(x, n=2):
    x = sp.nsimplify(x)
    d = Decimal(str(sp.N(x, 40)))
    e = d.adjusted()
    r = d.quantize(Decimal(1).scaleb(e - n + 1), rounding=ROUND_HALF_UP)
    if r.adjusted() != e:
        e = r.adjusted()
        r = d.quantize(Decimal(1).scaleb(e - n + 1), rounding=ROUND_HALF_UP)
    return f"{format(r.scaleb(-e), 'f')}\\times10^{{{e}}}"


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


def intq(stem, val, expr, e, unit=None, **kw):
    """整数で厳密に求まる答え（反応エンタルピーなど）。"""
    if unit:
        kw["unit"] = unit
    return num(stem, str(int(val)), e, chk=(expr, str(int(val))), **kw)


def err_item(stem, wrong, step, etype, tempt, fix, ans, expl, steps, ap, alt, pit, chk=None, d=3):
    return desc(f"{stem}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい答えを求めなさい。", ans, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい考え方・途中の式を示している", 3), ("最終的な答えが正しい", 1)], d=d, p=6, lines=6,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい考え方", 3), ("正しい答え", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix), chk=chk)


def sgn(v):
    return f"+{v}" if v > 0 else f"{v}"


def cf(c):
    c = sp.Rational(c)
    if c == 1:
        return ""
    if c.q == 1:
        return str(c)
    return f"\\dfrac{{{c.p}}}{{{c.q}}}"


PH = {"g": "気", "l": "液", "s": "固"}


def sp_tex(f, ph):
    if f == "C":
        return "\\mathrm{C}\\text{(黒鉛)}"
    return f"{tex(f)}\\text{{({PH[ph]})}}"


def te(lhs, rhs, dH=None):
    """熱化学反応式（エンタルピー変化を付記）。lhs/rhs = [(係数, 化学式, 状態)]"""
    s = "+".join(cf(c) + sp_tex(f, ph) for c, f, ph in lhs) + "\\longrightarrow " + "+".join(cf(c) + sp_tex(f, ph) for c, f, ph in rhs)
    if dH is not None:
        s += f"\\quad \\Delta H={dH}\\ \\mathrm{{kJ}}"
    return s


def eqm(lhs, rhs):
    return "+".join(cf(c) + tex(f) for c, f in lhs) + "\\rightleftharpoons " + "+".join(cf(c) + tex(f) for c, f in rhs)


# 生成エンタルピー（kJ/mol、25 ℃）
HF = {("CO2", "g"): -394, ("H2O", "l"): -286, ("H2O", "g"): -242, ("CH4", "g"): -75, ("C2H6", "g"): -84, ("C3H8", "g"): -105, ("C2H4", "g"): 52,
      ("C2H2", "g"): 227, ("NH3", "g"): -46, ("CO", "g"): -111, ("C2H5OH", "l"): -277, ("CH3OH", "l"): -239, ("NO", "g"): 90, ("HCl", "g"): -92,
      ("H2", "g"): 0, ("O2", "g"): 0, ("N2", "g"): 0, ("C", "s"): 0}
FNAME = {"CO2": "二酸化炭素", "H2O": "水", "CH4": "メタン", "C2H6": "エタン", "C3H8": "プロパン", "C2H4": "エチレン", "C2H2": "アセチレン", "NH3": "アンモニア",
         "CO": "一酸化炭素", "C2H5OH": "エタノール", "CH3OH": "メタノール", "NO": "一酸化窒素", "HCl": "塩化水素", "H2": "水素", "O2": "酸素", "N2": "窒素", "C": "黒鉛"}
FUELS = {"CH4": (1, 4, 0, "g"), "C2H6": (2, 6, 0, "g"), "C3H8": (3, 8, 0, "g"), "C2H4": (2, 4, 0, "g"), "C2H2": (2, 2, 0, "g"), "C2H5OH": (2, 6, 1, "l"),
         "CH3OH": (1, 4, 1, "l")}
MW = {"CH4": 16, "C2H6": 30, "C3H8": 44, "C2H4": 28, "C2H2": 26, "C2H5OH": 46, "CH3OH": 32, "H2": 2, "CO": 28}


def comb_eq(f):
    x, y, z, ph = FUELS[f]
    o2 = sp.Rational(x) + sp.Rational(y, 4) - sp.Rational(z, 2)
    return [(1, f, ph), (o2, "O2", "g")], [(x, "CO2", "g"), (sp.Rational(y, 2), "H2O", "l")]


def dH_of(lhs, rhs):
    return sum(c * HF[(f, ph)] for c, f, ph in rhs) - sum(c * HF[(f, ph)] for c, f, ph in lhs)


def comb_H(f):
    return dH_of(*comb_eq(f))


# ----------------------------------------------------------------------
# 図
# ----------------------------------------------------------------------

def _profile(R, P, top):
    def f(x):
        if x <= 2:
            return R
        if x <= 5:
            return R + (top - R) * (1 - math.cos(math.pi * (x - 2) / 3)) / 2
        if x <= 8:
            return top - (top - P) * (1 - math.cos(math.pi * (x - 5) / 3)) / 2
        return P
    return f


def energy_fig(Ea, dH, cat=None, caption="反応の進行とエンタルピー（概形）"):
    hi = max(Ea, Ea - dH) * 1.15
    lo = min(0, dH)
    sc = 8.0 / (hi - lo)
    R = 1.0 + (0 - lo) * sc
    P = 1.0 + (dH - lo) * sc
    top = R + Ea * sc
    curves = [(_profile(R, P, top), "")]
    labels = [(0.3, R + 0.35, "反応物"), (8.3, P + 0.35, "生成物"), (4.2, top + 0.4, "遷移状態")]
    if cat:
        curves.append((_profile(R, P, R + cat * sc), ""))
        labels.append((4.4, R + cat * sc - 0.6, "触媒あり"))
    svg = plane(xr=(0, 10.5), yr=(0, 10.5), unit=20, grid=False, ticks=False, curves=curves,
                segments=[((1.2, R), (1.2, top)), ((1.0, top), (5.0, top)), ((9.2, R), (9.2, P)), ((2.0, R), (9.4, R))],
                labels=labels + [(1.35, (R + top) / 2, "Ea"), (9.35, (R + P) / 2, "ΔH")], xl="反応の進行", yl="H")
    alt = f"反応の進行に伴うエンタルピーの変化。反応物から遷移状態まで {Ea} kJ（活性化エネルギー Ea）上がり、生成物は反応物より {abs(dH)} kJ {'低い（発熱反応、ΔH＜0）' if dH < 0 else '高い（吸熱反応、ΔH＞0）'}。"
    if cat:
        alt += f"触媒を用いた経路（低い山）の活性化エネルギーは {cat} kJ。"
    return figure(alt, svg=svg, caption=caption)


# ======================================================================
# 授業プリント
# ======================================================================

LESSON = lesson(
    goals=["反応エンタルピーを熱化学反応式で表し、ヘスの法則・生成エンタルピー・結合エネルギーを用いて未知の反応エンタルピーを求められる。",
           "反応速度の表し方と速度式、活性化エネルギーと触媒のはたらきを説明できる。",
           "化学平衡の状態を平衡定数で表し、平衡定数を用いた量的計算とルシャトリエの原理による平衡移動の判断ができる。",
           "弱酸・弱塩基の電離平衡を電離定数で表し、pH・緩衝液・溶解度積の計算ができる。"],
    duration=200,
    readiness=["物質量・モル濃度・化学反応式の量的関係（化学基礎）と、気体の状態方程式（前単元）を使える。",
               "pH の定義と強酸・強塩基の pH の計算、中和と塩の性質（化学基礎「酸と塩基・酸化還元」）を説明できる。",
               "常用対数（$\\log_{10}2=0.30$ など）と、2次方程式・平方根の計算ができる。"],
    flow=[("導入：燃料の発熱とアンモニア合成", 10, "燃焼で出るエネルギーと、なかなか完全に進まない反応の例から単元の問いを立てる"),
          ("反応エンタルピーと熱化学反応式", 25, "エンタルピー変化 ΔH、燃焼・生成・中和・溶解エンタルピー、熱量の測定"),
          ("ヘスの法則と結合エネルギー", 30, "状態量としてのエンタルピー、生成エンタルピーと結合エネルギーからの計算"),
          ("反応速度", 30, "反応速度の定義、速度式、活性化エネルギー、温度・触媒の効果"),
          ("化学平衡と平衡定数", 35, "可逆反応、平衡定数の導出、平衡の量的計算"),
          ("平衡の移動", 20, "ルシャトリエの原理、工業的な条件の選び方"),
          ("電離平衡", 35, "電離定数、弱酸の pH、緩衝液、溶解度積"),
          ("演習とまとめ", 15, "確認問題、問題プリントの課題指示")],
    sections=[
        intro("in1", "反応の「エネルギー」「速さ」「行き着く先」",
              "化学反応を理解するには3つの問いがある。どれだけのエネルギーが出入りするか（反応エンタルピー）、どれだけ速く進むか（反応速度）、そしてどこまで進むか（化学平衡）である。"
              "メタンの燃焼は大きな熱を出して一気に進むが、窒素と水素からのアンモニア合成は、触媒があっても一部しか進まずに止まったように見える。この単元では、これらを定量的に扱う道具をそろえる。",
              bullets=["エネルギー：ヘスの法則で、測定しにくい反応のエンタルピー変化も計算できる。",
                       "速さと平衡：活性化エネルギー・触媒・平衡定数・ルシャトリエの原理を使い分ける。",
                       "電離平衡：化学基礎の pH の計算を、弱酸・弱塩基や緩衝液にまで広げる。"],
              points=[tp("「よく燃える（エネルギー）」「すぐ燃える（速さ）」「最後まで燃える（平衡）」は別の性質であることを、具体例で区別させてから入る。",
                         ask="紙は空気中で燃えれば大量の熱を出すのに、机の上の紙が勝手に燃えださないのはなぜか。", expect="反応が始まるのに必要なエネルギー（活性化エネルギー）をこえられないから。",
                         timing="授業の冒頭")]),
        definition("df1", "反応エンタルピーと熱化学反応式",
                   "一定圧力のもとで反応に伴って出入りする熱量は、物質のもつエンタルピー $H$ の変化 $\\Delta H$ で表す。発熱反応では $\\Delta H<0$、吸熱反応では $\\Delta H>0$ である。"
                   "化学反応式の右に $\\Delta H$ を書き添えたものを熱化学反応式という。",
                   formula="$$\\mathrm{CH_4}\\text{(気)}+2\\mathrm{O_2}\\text{(気)}\\longrightarrow\\mathrm{CO_2}\\text{(気)}+2\\mathrm{H_2O}\\text{(液)}\\quad\\Delta H=-891\\ \\mathrm{kJ}$$",
                   conditions=["物質の状態（気・液・固）を必ず書く。$\\mathrm{H_2O}$ が液体か気体かで $\\Delta H$ が変わる（蒸発に 44 kJ/mol 必要）。",
                               "燃焼エンタルピー：1 mol が完全燃焼するとき。生成エンタルピー：1 mol がその成分元素の単体から生成するとき。名称のついた反応エンタルピーは、注目する物質の係数を 1 にする。",
                               "中和エンタルピー（$\\mathrm{H^+}$ と $\\mathrm{OH^-}$ から水 1 mol）、溶解エンタルピー（1 mol が多量の水に溶けるとき）もある。",
                               "熱量の測定：$q\\,[\\mathrm{J}]=m\\,[\\mathrm{g}]\\times c\\,[\\mathrm{J/(g\\cdot K)}]\\times\\Delta t\\,[\\mathrm{K}]$（水溶液の比熱は 4.2 J/(g·K) とすることが多い）。"],
                   points=[tp("発熱反応で $\\Delta H$ が負になる理由を、「物質がエネルギーを失って外に放出した」とエンタルピー図で示して納得させる。",
                              ask="水が氷になる変化の $\\Delta H$ は正か負か。", expect="負（凝固では熱を放出する）。",
                              caution="発熱量を正の値で問う問題と、$\\Delta H$ を問う問題の符号の違いに注意させる。")]),
        theorem("th1", "ヘスの法則（総熱量保存の法則）",
                "$$\\Delta H_{\\text{反応}}=\\sum(\\text{生成物の生成エンタルピー})-\\sum(\\text{反応物の生成エンタルピー})$$",
                ["反応エンタルピーは、反応の最初と最後の状態だけで決まり、途中の経路によらない。",
                 "熱化学反応式は数式のように足したり引いたり、定数倍したりできる（$\\Delta H$ も同じように計算する）。",
                 "気体分子の反応では：$\\Delta H=\\sum(\\text{切れる結合の結合エネルギー})-\\sum(\\text{できる結合の結合エネルギー})$。"],
                proof=["エンタルピーは物質の状態だけで決まる量（状態量）なので、反応物の組と生成物の組それぞれに1つの値が決まる。",
                       "反応物をいったんすべて成分元素の単体に分解し（$-\\sum$ 反応物の生成エンタルピー）、",
                       "その単体から生成物をつくる（$+\\sum$ 生成物の生成エンタルピー）経路を考えると、",
                       "経路によらず変化量は同じなので、$\\Delta H_{\\text{反応}}=\\sum H_{\\mathrm{f}}(\\text{生成物})-\\sum H_{\\mathrm{f}}(\\text{反応物})$ が成り立つ。単体の生成エンタルピーは 0 とする。"],
                points=[tp("エンタルピー図（縦軸 $H$）に、単体の基準線・反応物・生成物の3段を書き、矢印の向きと符号を確認させる。",
                           ask="黒鉛の燃焼 $-394$ kJ/mol と CO の燃焼 $-283$ kJ/mol から、CO の生成エンタルピーは？", expect="$-394-(-283)=-111$ kJ/mol")]),
        definition("df2", "反応速度と速度式",
                   "反応速度は、単位時間あたりの反応物の濃度の減少量（または生成物の濃度の増加量）で表す。反応速度と濃度の関係を表した式を速度式（反応速度式）という。",
                   formula="$$v=-\\dfrac{\\Delta[\\mathrm{A}]}{\\Delta t},\\qquad v=k[\\mathrm{A}]^{a}[\\mathrm{B}]^{b}\\quad(k：\\text{反応速度定数})$$",
                   conditions=["速度式の次数 $a,\\ b$ は実験で決める。化学反応式の係数と一致するとは限らない。",
                               "同じ反応でも、着目する物質によって速度の数値が変わる（係数の比に比例）。",
                               "温度を上げると、活性化エネルギー以上のエネルギーをもつ分子の割合が増え、$k$ が大きくなる。",
                               "触媒は活性化エネルギーの小さい別の経路をつくって反応を速くするが、反応エンタルピーは変えない。"],
                   points=[tp("初速度法の表（濃度を2倍にしたら速度が何倍か）から次数を読み取る練習を、具体的な数で行う。",
                              ask="[A] を2倍にすると速度が4倍になった。A についての次数は？", expect="2次")]),
        figure_explain("fg1", "活性化エネルギーと触媒", energy_fig(120, -90, 60, "活性化エネルギーと触媒（概形）"),
                       "反応物が生成物に変わる途中では、エネルギーの高い不安定な状態（遷移状態）を通る。反応物から遷移状態までのエネルギー差が活性化エネルギーである。"
                       "触媒を用いると活性化エネルギーの小さい経路で反応が進むが、反応物と生成物のエンタルピーは変わらないので、$\\Delta H$ は変わらない。逆反応の活性化エネルギーは $E_{\\mathrm{a}}+|\\Delta H|$（発熱反応のとき）になる。",
                       points=[tp("図の山の高さ（$E_{\\mathrm{a}}$）と、両端の高さの差（$\\Delta H$）が別の量であることを、触媒の有無で比べさせる。",
                                  ask="この図で、逆反応の活性化エネルギーはいくらか。", expect="$120+90=210$ kJ")]),
        derivation("dv1", "平衡定数の導出（可逆反応 $\\mathrm{H_2}+\\mathrm{I_2}\\rightleftharpoons2\\mathrm{HI}$）",
                   ["正反応・逆反応がそれぞれ1段階で進むとみなすと、$v_1=k_1[\\mathrm{H_2}][\\mathrm{I_2}]$、$v_2=k_2[\\mathrm{HI}]^2$。",
                    "反応が進むと $v_1$ は小さく、$v_2$ は大きくなり、やがて $v_1=v_2$ になる（平衡状態：見かけ上反応が止まる）。",
                    "$k_1[\\mathrm{H_2}][\\mathrm{I_2}]=k_2[\\mathrm{HI}]^2$ より $\\dfrac{[\\mathrm{HI}]^2}{[\\mathrm{H_2}][\\mathrm{I_2}]}=\\dfrac{k_1}{k_2}=K$（温度だけで決まる定数）。",
                    "一般に $a\\mathrm{A}+b\\mathrm{B}\\rightleftharpoons c\\mathrm{C}+d\\mathrm{D}$ では $K=\\dfrac{[\\mathrm{C}]^c[\\mathrm{D}]^d}{[\\mathrm{A}]^a[\\mathrm{B}]^b}$（化学平衡の法則）。この関係は反応の途中経路によらず成り立つ。",
                    "気体の反応では分圧で表した圧平衡定数 $K_{\\mathrm{p}}$ も使う。固体の濃度は一定とみなし、式に含めない。"],
                   body="平衡定数は温度が一定なら、はじめの濃度の組み合わせによらず一定である。濃度・圧力を変えても $K$ は変わらず、$K$ を保つように平衡が移動する。",
                   points=[tp("「平衡＝反応が止まった状態」ではなく「正反応と逆反応の速さが等しい状態」であることを、$v_1,\\ v_2$ のグラフで示す。", timing="導出の2段目")]),
        theorem("th2", "ルシャトリエの原理（平衡移動の原理）",
                "$$\\text{条件の変化}\\ \\Longrightarrow\\ \\text{その変化をやわらげる向きに平衡が移動する}$$",
                ["濃度：加えた物質を減らす向き、除いた物質を補う向きに移動する。",
                 "圧力（気体）：圧縮すると気体分子の総数が減る向き、減圧すると増える向きに移動する。両辺の気体分子数が等しければ移動しない。",
                 "温度：加熱すると吸熱反応の向き、冷却すると発熱反応の向きに移動する（温度だけは $K$ そのものを変える）。",
                 "触媒は平衡に達するまでの時間を短くするが、平衡は移動させない。体積一定で貴ガスを加えても各分圧は変わらず移動しない。"],
                proof=["$\\mathrm{N_2}+3\\mathrm{H_2}\\rightleftharpoons2\\mathrm{NH_3}$ で、温度一定のまま体積を $\\dfrac12$ にすると、すべての濃度が2倍になる。",
                       "このとき $\\dfrac{[\\mathrm{NH_3}]^2}{[\\mathrm{N_2}][\\mathrm{H_2}]^3}$ は $\\dfrac{2^2}{2\\times2^3}=\\dfrac14$ 倍になり $K$ より小さくなる。",
                       "$K$ に戻るには分子の $[\\mathrm{NH_3}]$ が増える必要があるので、平衡は右（気体分子が減る向き）へ移動する。"],
                points=[tp("ルシャトリエの原理の結論を、平衡定数の式（濃度商と $K$ の比較）で必ず裏づけさせる。",
                           ask="アンモニア合成（発熱反応）を高温で行うのはなぜか。", expect="平衡は不利だが反応速度を大きくするため（触媒と組み合わせる）。")]),
        definition("df3", "電離平衡と電離定数",
                   "弱酸 HA は水溶液中で一部だけ電離し、$\\mathrm{HA}\\rightleftharpoons\\mathrm{H^+}+\\mathrm{A^-}$ の平衡が成り立つ。この平衡定数を電離定数 $K_{\\mathrm{a}}$ という。",
                   formula="$$K_{\\mathrm{a}}=\\dfrac{[\\mathrm{H^+}][\\mathrm{A^-}]}{[\\mathrm{HA}]}=\\dfrac{c\\alpha^2}{1-\\alpha}\\fallingdotseq c\\alpha^2,\\qquad \\alpha\\fallingdotseq\\sqrt{\\dfrac{K_{\\mathrm{a}}}{c}},\\qquad [\\mathrm{H^+}]=c\\alpha\\fallingdotseq\\sqrt{cK_{\\mathrm{a}}}$$",
                   conditions=["近似 $1-\\alpha\\fallingdotseq1$ は $\\alpha$ が十分小さい（濃度が大きすぎず小さすぎない）ときに使える。",
                               "弱塩基（アンモニア）でも同様に $[\\mathrm{OH^-}]\\fallingdotseq\\sqrt{cK_{\\mathrm{b}}}$。",
                               "緩衝液（弱酸とその塩の混合水溶液）では $[\\mathrm{H^+}]=K_{\\mathrm{a}}\\times\\dfrac{[\\mathrm{HA}]}{[\\mathrm{A^-}]}$ とみなせ、少量の酸・塩基を加えても pH がほとんど変わらない。",
                               "難溶性塩 $\\mathrm{AgCl}$ の飽和水溶液では $K_{\\mathrm{sp}}=[\\mathrm{Ag^+}][\\mathrm{Cl^-}]$（溶解度積）。イオン濃度の積が $K_{\\mathrm{sp}}$ をこえると沈殿が生じる。"],
                   points=[tp("同じ濃度の塩酸と弱酸の pH を並べて計算させ、電離度の違いが pH に表れることを確認する。",
                              caution="弱酸の $[\\mathrm{H^+}]$ をモル濃度そのもの（完全電離）として計算する誤りが多い。")]),
        derivation("dv2", "弱酸の $[\\mathrm{H^+}]\\fallingdotseq\\sqrt{cK_{\\mathrm{a}}}$ の導出",
                   ["濃度 $c$ の弱酸 HA の電離度を $\\alpha$ とすると、平衡時 $[\\mathrm{HA}]=c(1-\\alpha)$、$[\\mathrm{H^+}]=[\\mathrm{A^-}]=c\\alpha$。",
                    "$K_{\\mathrm{a}}=\\dfrac{c\\alpha\\cdot c\\alpha}{c(1-\\alpha)}=\\dfrac{c\\alpha^2}{1-\\alpha}$。",
                    "$\\alpha\\ll1$ なら $1-\\alpha\\fallingdotseq1$ として $K_{\\mathrm{a}}\\fallingdotseq c\\alpha^2$、$\\alpha\\fallingdotseq\\sqrt{\\dfrac{K_{\\mathrm{a}}}{c}}$。",
                    "よって $[\\mathrm{H^+}]=c\\alpha\\fallingdotseq\\sqrt{cK_{\\mathrm{a}}}$。うすめる（$c$ を小さくする）と $\\alpha$ は大きくなる。"],
                   points=[tp("求めた $\\alpha$ が 0.05 程度より小さいことを確かめ、近似が妥当かどうかを判断する習慣をつける。")]),
        example("ex1", "例題1　ヘスの法則",
                "黒鉛・水素・プロパン $\\mathrm{C_3H_8}$（気）の燃焼エンタルピーをそれぞれ $-394$、$-286$、$-2221$ kJ/mol（水は液体）とする。プロパンの生成エンタルピーを求めよ。",
                ["求める式：$3\\mathrm{C}\\text{(黒鉛)}+4\\mathrm{H_2}\\text{(気)}\\longrightarrow\\mathrm{C_3H_8}\\text{(気)}$。",
                 "経路：単体を燃焼させると $3\\times(-394)+4\\times(-286)=-2326$ kJ。プロパンの燃焼で同じ生成物になるので、",
                 "$\\Delta H=-2326-(-2221)=-105$ kJ。"],
                "$-105$ kJ/mol", thinking="反応物（単体）の燃焼エンタルピーの和 − 生成物の燃焼エンタルピーの和。生成エンタルピーのときと引く順が逆になる。",
                misconceptions=[("$-2221-(-2326)=+105$ kJ/mol", "燃焼エンタルピーから求めるときは「反応物側の燃焼 − 生成物側の燃焼」")]),
        example("ex2", "例題2　平衡定数と平衡時の物質量",
                "容積一定の容器に $\\mathrm{H_2}$ と $\\mathrm{I_2}$ を 1.0 mol ずつ入れ、ある温度に保つと $\\mathrm{H_2}+\\mathrm{I_2}\\rightleftharpoons2\\mathrm{HI}$ が平衡に達した。この温度での平衡定数を 64 として、生成した HI の物質量を求めよ。",
                ["$\\mathrm{H_2}$ が $x$ mol 反応したとすると、平衡時 $\\mathrm{H_2}:1.0-x$、$\\mathrm{I_2}:1.0-x$、$\\mathrm{HI}:2x$（mol）。",
                 "両辺の分子数が等しいので体積は約分され、$\\dfrac{(2x)^2}{(1.0-x)^2}=64$。",
                 "$\\dfrac{2x}{1.0-x}=8$（正の値をとる）より $x=0.80$。HI は $1.6$ mol。"],
                "1.6 mol", thinking="反応前・変化量・平衡時の表をつくり、平衡定数の式に代入する。",
                points=[tp("平方根をとるとき、$x<1.0$ の条件から正の根だけを選ぶ理由を言わせる。")]),
        example("ex3", "例題3　弱酸の pH と緩衝液",
                "(1) 0.10 mol/L の酢酸水溶液の pH を求めよ。(2) 酢酸と酢酸ナトリウムを 0.10 mol/L ずつ含む水溶液の pH を求めよ。酢酸の電離定数は $K_{\\mathrm{a}}=2.0\\times10^{-5}$ mol/L、$\\log_{10}2=0.30$ とする。",
                ["(1) $[\\mathrm{H^+}]=\\sqrt{0.10\\times2.0\\times10^{-5}}=\\sqrt{2.0}\\times10^{-3}$ mol/L。",
                 "$\\mathrm{pH}=3-\\dfrac12\\log_{10}2=3-0.15=2.85$。",
                 "(2) 酢酸イオンが多量にあるので酢酸の電離はおさえられ、$[\\mathrm{CH_3COOH}]\\fallingdotseq[\\mathrm{CH_3COO^-}]\\fallingdotseq0.10$ mol/L。",
                 "$[\\mathrm{H^+}]=K_{\\mathrm{a}}\\times\\dfrac{0.10}{0.10}=2.0\\times10^{-5}$ mol/L、$\\mathrm{pH}=5-0.30=4.70$。"],
                "(1) 2.85　(2) 4.70", thinking="弱酸単独では $\\sqrt{cK_{\\mathrm{a}}}$、緩衝液では $K_{\\mathrm{a}}\\times$（酸の濃度/塩の濃度）。",
                misconceptions=[("(1) 酢酸は 0.10 mol/L だから pH 1", "弱酸は一部しか電離しない。$[\\mathrm{H^+}]=\\sqrt{cK_{\\mathrm{a}}}$")]),
        board("bd1", "板書案",
              [("① エネルギー", ["発熱 $\\Delta H<0$、吸熱 $\\Delta H>0$", "状態（気・液・固）を書く", "ΔH＝Σ生成物 $H_{\\mathrm{f}}$ − Σ反応物 $H_{\\mathrm{f}}$",
                                "燃焼からなら 反応物 − 生成物", "結合：切る − できる"]),
               ("② 速さと平衡", ["$v=k[\\mathrm{A}]^a[\\mathrm{B}]^b$（次数は実験で）", "触媒：$E_{\\mathrm{a}}$↓、ΔH 不変", "平衡：$v_1=v_2$",
                                "$K=\\dfrac{[\\mathrm{C}]^c[\\mathrm{D}]^d}{[\\mathrm{A}]^a[\\mathrm{B}]^b}$", "ルシャトリエ：変化をやわらげる向き"]),
               ("③ 電離平衡", ["$K_{\\mathrm{a}}\\fallingdotseq c\\alpha^2$", "$[\\mathrm{H^+}]\\fallingdotseq\\sqrt{cK_{\\mathrm{a}}}$", "緩衝液 $[\\mathrm{H^+}]=K_{\\mathrm{a}}\\dfrac{[\\mathrm{HA}]}{[\\mathrm{A^-}]}$",
                              "$K_{\\mathrm{sp}}=[\\mathrm{Ag^+}][\\mathrm{Cl^-}]$", "積 > $K_{\\mathrm{sp}}$ → 沈殿"])]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("ヘスの法則の計算は「目的の式に登場する物質が、与えられた式のどこに何個あるか」を印で確認してから式を足し引きさせる。",
                  caution="燃焼エンタルピーを使うときと生成エンタルピーを使うときで、引き算の順序が逆になることを必ず確認する。"),
               tp("平衡の計算は、反応前・変化量・平衡時の3行の表を毎回書かせる。体積で割る（濃度にする）必要があるかを、両辺の係数の和で判断させる。",
                  ask="$\\mathrm{N_2O_4}\\rightleftharpoons2\\mathrm{NO_2}$ の $K$ を物質量だけで計算してよいか。", expect="よくない。両辺の係数の和が違うので体積が残る。"),
               tp("触媒は「速くするが平衡は動かさない」、温度は「速さも平衡も変える」と、2つの軸を表にして整理させる。", timing="平衡の移動の終わり"),
               tp("弱酸の pH では、まず電離度を求めて近似が使えるかを確かめさせ、強酸と同じ扱いをしていないかを点検させる。")],
              misconceptions=[("触媒を加えると平衡が右に移動し、生成物が増える", "触媒は正反応・逆反応の両方を同じように速くするので、平衡は移動しない"),
                              ("平衡状態では反応が止まっている", "正反応と逆反応が同じ速さで進んでいる（動的平衡）"),
                              ("発熱反応の ΔH は正の値", "発熱反応では物質のエンタルピーが減るので ΔH＜0")]),
        summary("sm1", "まとめ", ["反応エンタルピーは状態量の差なので経路によらない（ヘスの法則）。生成エンタルピー・燃焼エンタルピー・結合エネルギーから計算できる。",
                                   "反応速度は濃度・温度・触媒で変わる。触媒は活性化エネルギーを下げるが、ΔH と平衡は変えない。",
                                   "平衡状態では $K$ が一定。条件を変えると、その変化をやわらげる向きに平衡が移動する（温度だけは $K$ を変える）。",
                                   "弱酸では $[\\mathrm{H^+}]\\fallingdotseq\\sqrt{cK_{\\mathrm{a}}}$。緩衝液は弱酸とその塩の組み合わせで pH を保つ。溶解度積をこえると沈殿が生じる。"]),
        check("ck1", "確認問題", [("$\\mathrm{H_2O}$（液）の生成エンタルピーが $-286$ kJ/mol のとき、水素 2.0 g の燃焼で放出される熱量は？", "286 kJ"),
                                  ("触媒を加えると、反応エンタルピーはどうなるか。", "変わらない"),
                                  ("$\\mathrm{N_2}+3\\mathrm{H_2}\\rightleftharpoons2\\mathrm{NH_3}$（発熱）で温度を上げると平衡はどちらへ移動するか。", "左（吸熱の向き）"),
                                  ("$c=0.10$ mol/L、$K_{\\mathrm{a}}=1.0\\times10^{-5}$ mol/L の弱酸の pH は？", "$[\\mathrm{H^+}]=1.0\\times10^{-3}$ mol/L より 3")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

@gen("basic_check", 4, ["computation", "application"])
def heat_amount(r):
    form = r.choice(["release", "mass", "calor", "neut"])
    if form in ("release", "mass"):
        f = r.choice(list(FUELS) + ["H2", "CO"])
        if f == "H2":
            lhs, rhs = [(1, "H2", "g"), (sp.Rational(1, 2), "O2", "g")], [(1, "H2O", "l")]
        elif f == "CO":
            lhs, rhs = [(1, "CO", "g"), (sp.Rational(1, 2), "O2", "g")], [(1, "CO2", "g")]
        else:
            lhs, rhs = comb_eq(f)
        dH = dH_of(lhs, rhs)
        Mf = MW[f]
        n = sp.Rational(r.choice(["0.10", "0.20", "0.50", "0.25", "2.0", "1.5", "0.40"]))
        w = n * Mf
        Q = -dH * n
        if form == "release":
            return numq(f"次の熱化学反応式について、{FNAME[f]} {dec(w)} g が完全燃焼したときに放出される熱量は何 kJ か。\n$${te(lhs, rhs, dH)}$$\n{FNAME[f]}の分子量は {Mf} とする。",
                        Q, f"{w}/({Mf})*({-dH})", f"物質量 ${dec(n)}$ mol に $|\\Delta H|={-dH}$ kJ/mol をかける。", unit="kJ", d=1, n=3,
                        ap="熱化学反応式の $\\Delta H$ は、式の係数どおりの物質量（ここでは燃料 1 mol）が反応したときの値。物質量に比例させる。",
                        steps=[f"$n=\\dfrac{{{dec(w)}}}{{{Mf}}}={dec(n)}$ mol。", f"放出される熱量：${dec(n)}\\times{-dH}={sig(Q, 3)}$ kJ。"],
                        alt=["$\\Delta H$ で答える場合は、放出なので負の値 $" + sig(-Q, 3) + "$ kJ になることも確認する。"],
                        pc=[("物質量を求めている", 1), ("熱量が正しい", 1)], pit=["質量に直接 $\\Delta H$ をかける。"])
        return numq(f"次の熱化学反応式について、{FNAME[f]}を完全燃焼させて {sig(Q, 3)} kJ の熱を得るには、{FNAME[f]}が何 g 必要か。\n$${te(lhs, rhs, dH)}$$\n{FNAME[f]}の分子量は {Mf} とする。",
                    w, f"{Q}/({-dH})*{Mf}", f"必要な物質量 $\\dfrac{{{sig(Q, 3)}}}{{{-dH}}}={dec(n)}$ mol。", unit="g", d=2, n=max(2, len(Decimal(dec(w)).normalize().as_tuple().digits)),
                    ap="得たい熱量を 1 mol あたりの発熱量で割ると、必要な物質量が分かる。",
                    steps=[f"$n=\\dfrac{{{sig(Q, 3)}}}{{{-dH}}}={dec(n)}$ mol。", f"$w={dec(n)}\\times{Mf}={dec(w)}$ g。"],
                    alt=["比例式 $1\\ \\mathrm{mol}:" + str(-dH) + "\\ \\mathrm{kJ}=n:" + sig(Q, 3) + "\\ \\mathrm{kJ}$ で求めてもよい。"],
                    pc=[("物質量を求めている", 1), ("質量が正しい", 1)], pit=["熱量の比を質量の比と考える。"])
    if form == "calor":
        w = sp.Rational(r.choice(["2.0", "4.0", "1.0", "3.0"]))
        msol = r.choice([50, 100, 200])
        dT_true = sp.Rational(44500) * w / 40 / (msol * sp.Rational("4.2"))  # 実測値に近い温度上昇（溶解エンタルピー約 −44.5 kJ/mol）
        dT = sp.Rational(sig(dT_true, 3 if dT_true >= 10 else 2))
        q = msol * sp.Rational("4.2") * dT
        n = w / 40
        dH = -q / n / 1000
        return numq(f"水酸化ナトリウム NaOH（式量 40）の固体 {dec(w)} g を水に溶かして {msol} g の水溶液にしたところ、温度が {dec(dT)} K 上昇した。水溶液の比熱を 4.2 J/(g·K) とし、発生した熱はすべて水溶液の温度上昇に使われたものとして、NaOH の溶解エンタルピー（kJ/mol）を求めなさい。",
                    dH, f"-({msol}*4.2*{dT})/({w}/40)/1000", "$q=mc\\Delta t$ で熱量を求め、1 mol あたりに換算する。発熱なので負。", unit="kJ/mol", d=2,
                    ap="熱量 $q=mc\\Delta t$（質量は水溶液全体）。溶解エンタルピーは 1 mol あたりで、発熱なら $\\Delta H<0$。",
                    steps=[f"$q={msol}\\times4.2\\times{dec(dT)}={dec(q)}$ J。", f"NaOH：$\\dfrac{{{dec(w)}}}{{40}}={dec(n)}$ mol。",
                           f"$\\Delta H=-\\dfrac{{{dec(q)}}}{{{dec(n)}}}\\times10^{{-3}}\\fallingdotseq{sig(dH)}$ kJ/mol。"],
                    alt=["単位で確かめる：g × J/(g·K) × K ＝ J。最後に kJ に直す。"],
                    pc=[("熱量を求めている", 1), ("1 mol あたり・符号が正しい", 1)], pit=["発熱なのに ΔH を正の値で答える。", "J と kJ の換算を忘れる。"])
    c = sp.Rational(r.choice(["1.0", "0.50", "2.0"]))
    V = r.choice([50, 100, 25])
    dT = sp.Rational(sig(sp.Rational(56500) * c / 2000 / sp.Rational("4.2"), 2))
    q = 2 * V * sp.Rational("4.2") * dT
    n = c * sp.Rational(V, 1000)
    dH = -q / n / 1000
    return numq(f"{dec(c)} mol/L の塩酸 {V} mL と {dec(c)} mol/L の水酸化ナトリウム水溶液 {V} mL を混合したところ、温度が {dec(dT)} K 上昇した。水溶液の密度を 1.0 g/cm³、比熱を 4.2 J/(g·K) とし、熱の出入りはないものとして、中和エンタルピー（kJ/mol）を求めなさい。",
                dH, f"-(2*{V}*4.2*{dT})/({c}*{V}/1000)/1000", "混合液全体の質量で熱量を求め、生じた水 1 mol あたりに換算する。", unit="kJ/mol", d=2,
                ap="中和エンタルピーは水 1 mol が生じるときの値。生じた水の物質量＝反応した $\\mathrm{H^+}$ の物質量。",
                steps=[f"質量：${2 * V}$ g、熱量 $q={2 * V}\\times4.2\\times{dec(dT)}={dec(q)}$ J。", f"生じた水：${dec(c)}\\times\\dfrac{{{V}}}{{1000}}={dec(n)}$ mol。",
                       f"$\\Delta H=-\\dfrac{{{dec(q)}\\times10^{{-3}}}}{{{dec(n)}}}\\fallingdotseq{sig(dH)}$ kJ/mol。"],
                alt=["強酸と強塩基の中和エンタルピーは、酸・塩基の種類によらずほぼ一定（約 $-56$ kJ/mol）であることと比べて確かめる。"],
                pc=[("熱量を求めている", 1), ("1 mol あたり・符号が正しい", 1)], pit=["一方の溶液の質量だけで熱量を計算する。"])


ENTH_Q = [([(1, "CH4", "g"), (2, "O2", "g")], [(1, "CO2", "g"), (2, "H2O", "l")], -891),
          ([(1, "N2", "g"), (3, "H2", "g")], [(2, "NH3", "g")], -92),
          ([(1, "C", "s"), (1, "CO2", "g")], [(2, "CO", "g")], 172),
          ([(1, "H2O", "l")], [(1, "H2O", "g")], 44),
          ([(1, "H2", "g"), (sp.Rational(1, 2), "O2", "g")], [(1, "H2O", "l")], -286),
          ([(1, "N2", "g"), (1, "O2", "g")], [(2, "NO", "g")], 180),
          ([(1, "CH4", "g"), (1, "H2O", "g")], [(1, "CO", "g"), (3, "H2", "g")], 206)]


@gen("basic_check", 4, ["concept", "condition_check"])
def enthalpy_meaning(r):
    lhs, rhs, dH = r.choice(ENTH_Q)
    exo = dH < 0
    k = sp.Rational(r.choice([2, 3, sp.Rational(1, 2)]))
    right_pool = [f"この反応は{'発熱' if exo else '吸熱'}反応であり、生成物のエンタルピーの和は反応物のエンタルピーの和より {abs(dH)} kJ {'小さい' if exo else '大きい'}。",
                  f"逆向きの反応の $\\Delta H$ は ${sgn(-dH)}$ kJ である。",
                  f"すべての係数を ${cf(k)}$ 倍した式の $\\Delta H$ は ${sgn(dH * k)}$ kJ である。"]
    right = r.choice(right_pool)
    wrong = [(f"この反応は{'吸熱' if exo else '発熱'}反応である。", f"$\\Delta H{'<' if exo else '>'}0$ なので{'発熱' if exo else '吸熱'}反応。", "ΔH の符号と発熱・吸熱の対応の誤り"),
             (f"逆向きの反応の $\\Delta H$ は ${sgn(dH)}$ kJ である。", f"逆反応では符号が逆になり ${sgn(-dH)}$ kJ。", "逆反応で符号を変えない誤り"),
             (f"すべての係数を ${cf(k)}$ 倍した式の $\\Delta H$ は ${sgn(dH)}$ kJ のままである。", f"ΔH は物質量に比例するので ${sgn(dH * k)}$ kJ になる。", "ΔH が反応する量に比例することを忘れる誤り"),
             (f"生成物のエンタルピーの和は反応物のエンタルピーの和より {abs(dH)} kJ {'大きい' if exo else '小さい'}。", f"ΔH＝（生成物）−（反応物）＝${sgn(dH)}$ kJ なので逆。", "ΔH の定義の向きの誤り")]
    wrong = r.sample(wrong, 3)
    why = {w: (a, b) for w, a, b in wrong}
    return mc(f"次の熱化学反応式について述べた文のうち、正しいものを選びなさい。\n$${te(lhs, rhs, dH)}$$", [right] + [w for w, _, _ in wrong],
              f"正しいのは「{right}」。$\\Delta H$ は（生成物のエンタルピー）−（反応物のエンタルピー）で、反応する量に比例し、逆反応では符号が変わる。", d=2,
              ap="$\\Delta H<0$ は発熱、$\\Delta H>0$ は吸熱。$\\Delta H$ は係数どおりの物質量についての値で、式を逆にすると符号が逆、何倍かすると同じ倍率になる。",
              steps=[f"$\\Delta H={sgn(dH)}$ kJ なので{'発熱' if exo else '吸熱'}反応。", "逆反応の ΔH は符号を逆にする。", "係数を k 倍すると ΔH も k 倍。", "各文をこの3点で判定する。"],
              alt=["エンタルピー図（反応物と生成物の高さ）をかいて確かめる。"],
              pc=[("ΔH の符号の意味を理解している", 1), ("正しく選んでいる", 1)], why=why, pit=["ΔH の符号と発熱・吸熱を逆に覚えている。"])


@gen("basic_check", 4, ["computation", "concept"])
def rate_basic(r):
    form = r.choice(["avg", "scale", "coef"])
    if form == "avg":
        c1 = sp.Rational(r.choice(["0.80", "1.00", "0.60", "0.50", "1.20", "0.40"]))
        frac_ = sp.Rational(r.choice(["3/4", "1/2", "4/5", "2/3", "5/8"]))
        c2 = c1 * frac_
        dt = r.choice([10, 20, 40, 50, 60, 100])
        v = (c1 - c2) / dt
        sub = r.choice(["H2O2", "N2O5"])
        nm_ = "過酸化水素" if sub == "H2O2" else "五酸化二窒素"
        return _rate_avg(nm_, sub, c1, c2, dt)
    if form == "scale":
        a, b = r.choice([(1, 1), (2, 1), (1, 2), (2, 0), (1, 0), (0, 1), (2, 2)])
        pA = r.choice([2, 3, sp.Rational(1, 2)])
        pB = r.choice([2, 3, sp.Rational(1, 2)])
        fac = sp.Rational(pA) ** a * sp.Rational(pB) ** b
        def word(p):
            p = sp.Rational(p)
            return f"{p}倍" if p.q == 1 else "$\\dfrac{1}{2}$倍"
        rl = "v=k" + (f"[\\mathrm{{A}}]^{{{a}}}" if a > 1 else ("[\\mathrm{A}]" if a == 1 else "")) + (f"[\\mathrm{{B}}]^{{{b}}}" if b > 1 else ("[\\mathrm{B}]" if b == 1 else ""))
        return numq(f"反応 A＋B → C の反応速度が ${rl}$ で表されるとき、温度を変えずに [A] を{word(pA)}、[B] を{word(pB)}にすると、反応速度は何倍になるか。分数の場合は小数で答えなさい。",
                    fac, f"Rational({sp.Rational(pA)})**{a}*Rational({sp.Rational(pB)})**{b}", f"$({dec(sp.Rational(pA))})^{{{a}}}\\times({dec(sp.Rational(pB))})^{{{b}}}={dec(fac) if fac.q in (1, 2, 4, 8, 16) else fac}$ 倍。", d=2,
                    n=3, ap="速度式の各濃度を何倍かして代入する。次数が指数になる。温度一定なので $k$ は変わらない。",
                    steps=[f"[A] の寄与：$({dec(sp.Rational(pA))})^{{{a}}}$ 倍。", f"[B] の寄与：$({dec(sp.Rational(pB))})^{{{b}}}$ 倍。", f"合計：${dec(fac)}$ 倍。"],
                    alt=["具体的な濃度（例えば [A]＝[B]＝1）を代入して、前後の速度を比べてもよい。"],
                    pc=[("次数を指数として用いている", 1), ("値が正しい", 1)], pit=["次数を無視して濃度の倍率をそのまま掛ける。"])
    sub = r.choice([("2H2O2", "O2", 2, 1, "過酸化水素", "酸素", "2\\mathrm{H_2O_2}\\longrightarrow2\\mathrm{H_2O}+\\mathrm{O_2}"),
                    ("N2", "NH3", 1, 2, "窒素", "アンモニア", "\\mathrm{N_2}+3\\mathrm{H_2}\\longrightarrow2\\mathrm{NH_3}"),
                    ("H2", "NH3", 3, 2, "水素", "アンモニア", "\\mathrm{N_2}+3\\mathrm{H_2}\\longrightarrow2\\mathrm{NH_3}"),
                    ("2N2O5", "O2", 2, 1, "五酸化二窒素", "酸素", "2\\mathrm{N_2O_5}\\longrightarrow4\\mathrm{NO_2}+\\mathrm{O_2}"),
                    ("2N2O5", "NO2", 2, 4, "五酸化二窒素", "二酸化窒素", "2\\mathrm{N_2O_5}\\longrightarrow4\\mathrm{NO_2}+\\mathrm{O_2}")])
    _, _, ca, cb, na, nb, eq = sub
    v = sp.Rational(r.choice(["2.0", "4.0", "6.0", "1.2", "3.0", "8.0"])) / 10 ** r.choice([2, 3])
    vb = v * cb / ca
    return numq(f"反応 ${eq}$ において、ある時間における{na}の減少速度が ${sci(v)}$ mol/(L·s) であった。このときの{nb}の生成速度は何 mol/(L·s) か。", vb,
                f"{v}*{cb}/({ca})", f"速度の比は係数の比 {ca}：{cb}。", unit="mol/(L·s)", d=2,
                ap="同じ反応では、各物質の濃度の変化量の比は化学反応式の係数の比に等しい。",
                steps=[f"係数の比 {na}：{nb}＝{ca}：{cb}。", f"${sci(v)}\\times\\dfrac{{{cb}}}{{{ca}}}={sci(vb)}$ mol/(L·s)。"],
                alt=["反応式の係数で割った値 $\\dfrac{1}{\\text{係数}}\\times\\dfrac{\\Delta c}{\\Delta t}$ がどの物質でも等しい、と考えてもよい。"],
                pc=[("係数の比を用いている", 1), ("値が正しい", 1)], pit=["係数の比を逆に用いる。"])


def sigv_(x, n=2):
    s = sig(x, n)
    if "times" in s:
        a, e = re.match(r"(-?[\d.]+)\\times10\^\{(-?\d+)\}", s).groups()
        return sp.Rational(a) * sp.Integer(10) ** int(e)
    return sp.Rational(s)


def _rate_avg(nm_, sub, c1, c2, dt):
    c2v = sigv_(c2)
    v = (c1 - c2v) / dt
    return numq(f"{nm_} ${tex(sub)}$ の分解反応で、その濃度が {dec(c1)} mol/L から {dec(c2v)} mol/L まで減少するのに {dt} 秒かかった。この間の{nm_}の平均の分解速度は何 mol/(L·s) か。",
                v, f"({c1}-({c2v}))/({dt})", f"$v=-\\dfrac{{\\Delta c}}{{\\Delta t}}=\\dfrac{{{dec(c1)}-{dec(c2v)}}}{{{dt}}}$。", unit="mol/(L·s)", d=1,
                ap="反応速度は単位時間あたりの濃度の変化量。反応物では減少量を正の値で表す。",
                steps=[f"濃度の減少量：${dec(c1)}-{dec(c2v)}={dec(c1 - c2v)}$ mol/L。", f"$v=\\dfrac{{{dec(c1 - c2v)}}}{{{dt}}}={sig(v)}$ mol/(L·s)。"],
                alt=["単位で確かめる：mol/L ÷ s ＝ mol/(L·s)。"],
                pc=[("濃度変化を求めている", 1), ("速度が正しい", 1)], pit=["濃度そのものを時間で割る。"])


EQ_RX = [("H2+I2", [(1, "H2"), (1, "I2")], [(2, "HI")]),
         ("N2O4", [(1, "N2O4")], [(2, "NO2")]),
         ("NH3", [(1, "N2"), (3, "H2")], [(2, "NH3")]),
         ("SO3", [(2, "SO2"), (1, "O2")], [(2, "SO3")]),
         ("ester", [(1, "CH3COOH"), (1, "C2H5OH")], [(1, "CH3COOC2H5"), (1, "H2O")])]


def kunit(dn):
    if dn == 0:
        return ""
    if dn == 1:
        return "mol/L"
    if dn == -1:
        return "L/mol"
    if dn > 0:
        return f"(mol/L)^{dn}"
    return f"(L/mol)^{-dn}"


@gen("basic_check", 4, ["computation", "condition_check"])
def eq_constant(r):
    key, lhs, rhs = r.choice(EQ_RX)
    V = sp.Rational(r.choice(["1.0", "2.0", "0.50", "5.0", "10"]))
    amounts = {}
    for c, f in lhs + rhs:
        amounts[f] = sp.Rational(r.choice(["0.10", "0.20", "0.40", "0.50", "1.0", "0.30", "0.60", "2.0"]))
    if key == "ester":
        V = sp.Integer(1)
    conc = {f: amounts[f] / V for f in amounts}
    num_ = sp.Mul(*[conc[f] ** c for c, f in rhs])
    den = sp.Mul(*[conc[f] ** c for c, f in lhs])
    K = num_ / den
    dn = sum(c for c, _ in rhs) - sum(c for c, _ in lhs)
    unit = kunit(dn)
    names = "、".join(f"${tex(f)}$ {dec(amounts[f])} mol" for _, f in lhs + rhs)
    kexpr = "\\dfrac{" + "".join(f"[{tex(f)}]" + (f"^{c}" if c > 1 else "") for c, f in rhs) + "}{" + "".join(f"[{tex(f)}]" + (f"^{c}" if c > 1 else "") for c, f in lhs) + "}"
    vol = "（液体の混合物で、体積は約分されるものとする）" if key == "ester" else f"容積 {dec(V)} L の容器内で"
    expr = "(" + "*".join(f"({amounts[f]}/({V}))**{c}" for c, f in rhs) + ")/(" + "*".join(f"({amounts[f]}/({V}))**{c}" for c, f in lhs) + ")"
    return numq(f"反応 ${eqm(lhs, rhs)}$ が{vol}平衡状態にあり、{names} が存在している。この温度での平衡定数 $K$ を求めなさい。" + (f"単位は {unit} である。" if unit else ""),
                K, expr, f"$K={kexpr}$ に、各物質のモル濃度（物質量÷体積）を代入する。", d=2, n=2, **({"unit": unit} if unit else {}),
                ap="平衡定数の式に、平衡時のモル濃度を代入する。物質量のまま代入してよいのは、両辺の係数の和が等しいときだけ。",
                steps=[f"$K={kexpr}$。", "各濃度：" + "、".join(f"$[{tex(f)}]={dec(conc[f]) if sp.Rational(conc[f]).q in (1, 2, 4, 5, 8, 10, 20, 25, 50, 100) else sig(conc[f])}$" for _, f in lhs + rhs) + "（mol/L）。",
                       f"$K={sig(K)}$" + (f" {unit}" if unit else "") + "。"],
                alt=["単位は（濃度の単位）の（右辺の係数の和−左辺の係数の和）乗になることで確かめる。"],
                pc=[("平衡定数の式が正しい", 1), ("値が正しい", 1)], pit=["物質量のまま代入する（体積で割り忘れる）。", "係数を指数にし忘れる。"])


LCR = [("N2+3H2⇌2NH3", "\\mathrm{N_2}+3\\mathrm{H_2}\\rightleftharpoons2\\mathrm{NH_3}", -92, 4, 2, False, "NH3"),
       ("N2O4⇌2NO2", "\\mathrm{N_2O_4}\\rightleftharpoons2\\mathrm{NO_2}", 57, 1, 2, False, "NO2"),
       ("2SO2+O2⇌2SO3", "2\\mathrm{SO_2}+\\mathrm{O_2}\\rightleftharpoons2\\mathrm{SO_3}", -198, 3, 2, False, "SO3"),
       ("C+CO2⇌2CO", "\\mathrm{C}\\text{(黒鉛)}+\\mathrm{CO_2}\\rightleftharpoons2\\mathrm{CO}", 172, 1, 2, True, "CO"),
       ("H2+I2⇌2HI", "\\mathrm{H_2}+\\mathrm{I_2}\\rightleftharpoons2\\mathrm{HI}", None, 2, 2, False, "HI")]
CHANGES = ["heat", "cool", "compress", "expand", "catalyst", "ar_v", "ar_p", "add_solid"]
CH_TXT = {"heat": "温度を上げる", "cool": "温度を下げる", "compress": "温度一定で圧縮して全圧を高くする", "expand": "温度一定で体積を大きくして全圧を低くする",
          "catalyst": "触媒を加える", "ar_v": "体積を一定に保ってアルゴンを加える", "ar_p": "全圧を一定に保ってアルゴンを加える", "add_solid": "黒鉛を少量加える"}


def lc_dir(rx, ch):
    _, _, dH, gl, gr, solid, _ = rx
    if ch == "heat":
        return "右" if dH > 0 else "左", "吸熱反応の向きに移動する"
    if ch == "cool":
        return "右" if dH < 0 else "左", "発熱反応の向きに移動する"
    if ch == "compress":
        return ("移動しない", "両辺の気体分子の数が等しい") if gl == gr else (("右" if gr < gl else "左"), "気体分子の総数が減る向きに移動する")
    if ch == "expand":
        return ("移動しない", "両辺の気体分子の数が等しい") if gl == gr else (("右" if gr > gl else "左"), "気体分子の総数が増える向きに移動する")
    if ch == "catalyst":
        return "移動しない", "触媒は正反応と逆反応を同じように速めるだけで、平衡は移動させない"
    if ch == "ar_v":
        return "移動しない", "体積一定では各成分の分圧（濃度）が変わらない"
    if ch == "ar_p":
        return ("移動しない", "両辺の気体分子の数が等しい") if gl == gr else (("右" if gr > gl else "左"), "全圧一定で体積が増え、各成分の分圧の和が下がるので、気体分子の総数が増える向きに移動する")
    return "移動しない", "固体の量は平衡定数の式に含まれず、平衡に影響しない"


@gen("basic_check", 4, ["concept", "condition_check"])
def le_chatelier(r):
    for _ in range(100):
        rx = r.choice(LCR)
        ch = r.choice(CHANGES)
        if rx[2] is None and ch in ("heat", "cool"):
            continue
        if ch == "add_solid" and not rx[5]:
            continue
        break
    d, why_ = lc_dir(rx, ch)
    lab = {"右": f"右に移動する（${tex(rx[6])}$ が増える）", "左": f"左に移動する（${tex(rx[6])}$ が減る）", "移動しない": "移動しない"}
    dh = f"（正反応の $\\Delta H={sgn(rx[2])}$ kJ）" if rx[2] is not None else ""
    choices = [lab[d]] + [lab[k] for k in lab if k != d]
    reasons = {"右": "右への移動は", "左": "左への移動は"}
    why = {lab[k]: (f"{CH_TXT[ch]}と、{why_}ので、平衡は{'移動しない' if d == '移動しない' else d + 'に移動する'}。", "ルシャトリエの原理の適用の誤り") for k in lab if k != d}
    return mc(f"次の可逆反応が平衡状態にある{dh}。\n$${rx[1]}$$\nここで{CH_TXT[ch]}と、平衡はどうなるか。", choices,
              f"{why_}。よって平衡は{'移動しない' if d == '移動しない' else d + 'に移動する'}。", d=2,
              ap="ルシャトリエの原理：加えられた変化をやわらげる向きに平衡が移動する。温度は ΔH の符号、圧力は両辺の気体分子の数、触媒・体積一定の貴ガスは影響なし。",
              steps=[f"変化：{CH_TXT[ch]}。", f"判断の根拠：{why_}。", f"結論：{'移動しない' if d == '移動しない' else d + 'に移動'}。"],
              alt=["濃度商 $Q$ と平衡定数 $K$ の大小で考える：変化直後に $Q<K$ なら右、$Q>K$ なら左へ移動する（温度変化では $K$ 自体が変わる）。"],
              pc=[("適用すべき原理を判断している", 1), ("正しく選んでいる", 1)], why=why,
              pit=["触媒で平衡が右に移動すると考える。", "固体の物質や、体積一定で加えた貴ガスの影響を考えてしまう。"])


# ======================================================================
# B 標準演習
# ======================================================================

HESS_RX = [([(1, "C2H4", "g"), (1, "H2", "g")], [(1, "C2H6", "g")]),
           ([(1, "C2H2", "g"), (2, "H2", "g")], [(1, "C2H6", "g")]),
           ([(1, "C2H2", "g"), (1, "H2", "g")], [(1, "C2H4", "g")]),
           ([(1, "C2H4", "g"), (1, "H2O", "l")], [(1, "C2H5OH", "l")]),
           ([(4, "NH3", "g"), (5, "O2", "g")], [(4, "NO", "g"), (6, "H2O", "g")]),
           ([(1, "CO", "g"), (1, "H2O", "g")], [(1, "CO2", "g"), (1, "H2", "g")]),
           ([(1, "C", "s"), (1, "CO2", "g")], [(2, "CO", "g")]),
           ([(1, "CH4", "g"), (1, "H2O", "g")], [(1, "CO", "g"), (3, "H2", "g")])]


@gen("standard_practice", 5, ["computation", "application"])
def hess(r):
    form = r.choice(["form_from_comb", "rxn_from_form", "rxn_from_form", "two_eq"])
    if form == "form_from_comb":
        f = r.choice(list(FUELS))
        x, y, z, ph = FUELS[f]
        dc = comb_H(f)
        dhf = HF[(f, ph)]
        target_l = [(x, "C", "s"), (sp.Rational(y, 2), "H2", "g")] + ([(sp.Rational(z, 2), "O2", "g")] if z else [])
        return intq(f"黒鉛・水素・{FNAME[f]}の燃焼エンタルピーを、それぞれ $-394$ kJ/mol、$-286$ kJ/mol、${dc}$ kJ/mol とする（生成する水は液体）。{FNAME[f]}（{PH[ph]}）の生成エンタルピーは何 kJ/mol か。",
                    sp.Integer(dhf), f"{x}*(-394)+Rational({y},2)*(-286)-({dc})", f"$\\Delta H={x}\\times(-394)+{cf(sp.Rational(y, 2)) or '1'}\\times(-286)-({dc})={dhf}$ kJ/mol。",
                    unit="kJ/mol", d=3,
                    ap=f"求める式は ${te(target_l, [(1, f, ph)])}$。左辺の単体を燃焼させた経路と、いったん{FNAME[f]}をつくってから燃焼させた経路で、最終状態（$\\mathrm{{CO_2}}$ と $\\mathrm{{H_2O}}$）は同じ。",
                    steps=[f"単体の燃焼：${x}\\times(-394)+{cf(sp.Rational(y, 2)) or '1'}\\times(-286)={x * -394 + sp.Rational(y, 2) * -286}$ kJ。",
                           f"{FNAME[f]}の燃焼：${dc}$ kJ。", f"$\\Delta H_{{\\mathrm{{f}}}}=({x * -394 + sp.Rational(y, 2) * -286})-({dc})={dhf}$ kJ/mol。"],
                    alt=["熱化学反応式を3本書き、目的の式になるように「黒鉛の式×" + str(x) + "＋水素の式×" + str(sp.Rational(y, 2)) + "−" + FNAME[f] + "の式」と組み合わせても同じ。"],
                    pc=[("目的の式を正しく立てている", 1), ("経路の考え方で式を組み合わせている", 2), ("値と符号が正しい", 1)],
                    pit=["引き算の順序を逆にして符号を誤る。", "水素の係数（$\\frac{y}{2}$）を掛け忘れる。"])
    if form == "two_eq":
        sel = r.choice(["CO", "vap", "hydro"])
        if sel == "CO":
            e1 = te([(1, "C", "s"), (1, "O2", "g")], [(1, "CO2", "g")], -394)
            e2 = te([(1, "CO", "g"), (sp.Rational(1, 2), "O2", "g")], [(1, "CO2", "g")], -283)
            tgt = te([(1, "C", "s"), (sp.Rational(1, 2), "O2", "g")], [(1, "CO", "g")])
            ans, ex, how = -111, "-394-(-283)", "①−②"
        elif sel == "vap":
            e1 = te([(1, "H2", "g"), (sp.Rational(1, 2), "O2", "g")], [(1, "H2O", "l")], -286)
            e2 = te([(1, "H2", "g"), (sp.Rational(1, 2), "O2", "g")], [(1, "H2O", "g")], -242)
            tgt = te([(1, "H2O", "l")], [(1, "H2O", "g")])
            ans, ex, how = 44, "-242-(-286)", "②−①"
        else:
            f1, f2 = r.choice([("C2H4", "C2H6"), ("C2H2", "C2H4")])
            e1 = te(*comb_eq(f1), comb_H(f1))
            e2 = te(*comb_eq(f2), comb_H(f2))
            e3 = te([(1, "H2", "g"), (sp.Rational(1, 2), "O2", "g")], [(1, "H2O", "l")], -286)
            tgt = te([(1, f1, "g"), (1, "H2", "g")], [(1, f2, "g")])
            ans = comb_H(f1) - 286 - comb_H(f2)
            ex, how = f"({comb_H(f1)})+(-286)-({comb_H(f2)})", "①＋③−②"
            return intq(f"次の熱化学反応式①〜③を用いて、${tgt}$ の反応エンタルピー $\\Delta H$ を求めなさい。\n① ${e1}$\n② ${e2}$\n③ ${e3}$",
                        sp.Integer(ans), ex, f"{how} で目的の式が得られる。", unit="kJ", d=3,
                        ap="目的の式の左辺にある物質は与式の左辺から、右辺にある物質は与式の右辺から取り出すように、式を足し引きする。",
                        steps=[f"{FNAME[f1]}は目的の式の左辺 → ①をそのまま使う。水素も左辺 → ③をそのまま使う。", f"{FNAME[f2]}は右辺 → ②を逆向き（−②）にする。",
                               f"$\\Delta H={ex}={ans}$ kJ。"],
                        alt=["燃焼エンタルピーから求める公式：（反応物の燃焼エンタルピーの和）−（生成物の燃焼エンタルピーの和）を使っても同じ。"],
                        pc=[("組み合わせ方が正しい", 2), ("値と符号が正しい", 2)], pit=["式の向きを逆にしたときに ΔH の符号を変え忘れる。"])
        return intq(f"次の熱化学反応式①、②を用いて、${tgt}$ の反応エンタルピー $\\Delta H$ を求めなさい。\n① ${e1}$\n② ${e2}$", sp.Integer(ans), ex,
                    f"{how} で目的の式が得られる。", unit="kJ", d=2,
                    ap="目的の式に現れない物質（ここでは共通の生成物）が消えるように、2つの式を引き算する。",
                    steps=[f"目的の式は {how}。", f"$\\Delta H={ex}={ans}$ kJ。"],
                    alt=["エンタルピー図に3つの状態を書き、高さの差として求めてもよい。"],
                    pc=[("組み合わせ方が正しい", 2), ("値と符号が正しい", 2)], pit=["引き算の順序を逆にする。"])
    lhs, rhs = r.choice(HESS_RX)
    dH = dH_of(lhs, rhs)
    used = [(f, ph) for _, f, ph in lhs + rhs if HF[(f, ph)] != 0]
    data = "、".join(f"{FNAME[f]}（{PH[ph]}）${HF[(f, ph)]}$" for f, ph in dict.fromkeys(used))
    return intq(f"次の反応の反応エンタルピー $\\Delta H$ を求めなさい。\n$${te(lhs, rhs)}$$\n生成エンタルピー（kJ/mol）は {data} とし、単体の生成エンタルピーは 0 とする。",
                sp.Integer(dH), "(" + "+".join(f"({c})*({HF[(f, ph)]})" for c, f, ph in rhs) + ")-(" + "+".join(f"({c})*({HF[(f, ph)]})" for c, f, ph in lhs) + ")",
                "ΔH＝（生成物の生成エンタルピーの和）−（反応物の生成エンタルピーの和）。", unit="kJ", d=3,
                ap="ヘスの法則より、反応物をいったん単体にもどしてから生成物をつくる経路で考える。係数を掛けるのを忘れない。",
                steps=[f"生成物：${'+'.join(f'{cf(c) or 1}' + chr(92) + 'times(' + str(HF[(f, ph)]) + ')' for c, f, ph in rhs)}={sum(c * HF[(f, ph)] for c, f, ph in rhs)}$ kJ。",
                       f"反応物：${'+'.join(f'{cf(c) or 1}' + chr(92) + 'times(' + str(HF[(f, ph)]) + ')' for c, f, ph in lhs)}={sum(c * HF[(f, ph)] for c, f, ph in lhs)}$ kJ。",
                       f"$\\Delta H={sum(c * HF[(f, ph)] for c, f, ph in rhs)}-({sum(c * HF[(f, ph)] for c, f, ph in lhs)})={dH}$ kJ。"],
                alt=["生成エンタルピーの熱化学反応式を書いて、目的の式になるように足し引きしても同じ結果になる。"],
                pc=[("公式を正しく用いている", 2), ("係数を掛けている", 1), ("値と符号が正しい", 1)],
                pit=["反応物 − 生成物 と逆に計算する。", "係数を掛け忘れる。", "H₂O の液体と気体の値を取り違える。"])


BE = {"H-H": 436, "Cl-Cl": 243, "H-Cl": 432, "Br-Br": 193, "H-Br": 366, "O=O": 498, "O-H": 463, "N≡N": 945, "N-H": 391, "C-H": 416, "C=O": 804}
BE_TEX = {"H-H": "\\mathrm{H{-}H}", "Cl-Cl": "\\mathrm{Cl{-}Cl}", "H-Cl": "\\mathrm{H{-}Cl}", "Br-Br": "\\mathrm{Br{-}Br}", "H-Br": "\\mathrm{H{-}Br}",
          "O=O": "\\mathrm{O{=}O}", "O-H": "\\mathrm{O{-}H}", "N≡N": "\\mathrm{N{\\equiv}N}", "N-H": "\\mathrm{N{-}H}", "C-H": "\\mathrm{C{-}H}", "C=O": "\\mathrm{C{=}O}"}
BE_RX = [("2\\mathrm{HCl}", "\\mathrm{H_2}\\text{(気)}+\\mathrm{Cl_2}\\text{(気)}\\longrightarrow2\\mathrm{HCl}\\text{(気)}", {"H-H": 1, "Cl-Cl": 1}, {"H-Cl": 2}),
         ("2\\mathrm{HBr}", "\\mathrm{H_2}\\text{(気)}+\\mathrm{Br_2}\\text{(気)}\\longrightarrow2\\mathrm{HBr}\\text{(気)}", {"H-H": 1, "Br-Br": 1}, {"H-Br": 2}),
         ("2\\mathrm{NH_3}", "\\mathrm{N_2}\\text{(気)}+3\\mathrm{H_2}\\text{(気)}\\longrightarrow2\\mathrm{NH_3}\\text{(気)}", {"N≡N": 1, "H-H": 3}, {"N-H": 6}),
         ("2\\mathrm{H_2O}", "2\\mathrm{H_2}\\text{(気)}+\\mathrm{O_2}\\text{(気)}\\longrightarrow2\\mathrm{H_2O}\\text{(気)}", {"H-H": 2, "O=O": 1}, {"O-H": 4}),
         ("\\mathrm{CO_2}", "\\mathrm{CH_4}\\text{(気)}+2\\mathrm{O_2}\\text{(気)}\\longrightarrow\\mathrm{CO_2}\\text{(気)}+2\\mathrm{H_2O}\\text{(気)}", {"C-H": 4, "O=O": 2}, {"C=O": 2, "O-H": 4})]


@gen("standard_practice", 4, ["computation", "concept"])
def bond_energy(r):
    _, eq, brk, frm = r.choice(BE_RX)
    br = sum(BE[b] * k for b, k in brk.items())
    fo = sum(BE[b] * k for b, k in frm.items())
    dH = br - fo
    allb = list(brk) + list(frm)
    if r.random() < 0.5:
        data = "、".join(f"${BE_TEX[b]}$ {BE[b]}" for b in allb)
        return intq(f"次の反応の反応エンタルピー $\\Delta H$ を、結合エネルギー（kJ/mol）{data} を用いて求めなさい。\n$${eq}$$", sp.Integer(dH),
                    f"({'+'.join(f'{BE[b]}*{k}' for b, k in brk.items())})-({'+'.join(f'{BE[b]}*{k}' for b, k in frm.items())})",
                    "ΔH＝（切れる結合の結合エネルギーの和）−（できる結合の結合エネルギーの和）。", unit="kJ", d=3,
                    ap="反応物の結合をすべて切って原子にする（吸熱）→ 原子から生成物の結合をつくる（発熱）、という経路で考える。",
                    steps=[f"切れる結合：{'＋'.join(f'${BE_TEX[b]}$×{k}' for b, k in brk.items())}＝{br} kJ。",
                           f"できる結合：{'＋'.join(f'${BE_TEX[b]}$×{k}' for b, k in frm.items())}＝{fo} kJ。", f"$\\Delta H={br}-{fo}={dH}$ kJ。"],
                    alt=["エンタルピー図で、反応物 → ばらばらの原子（＋" + str(br) + " kJ）→ 生成物（−" + str(fo) + " kJ）とたどる。"],
                    pc=[("切れる結合・できる結合を正しく数えている", 2), ("値と符号が正しい", 2)],
                    pit=["できる − 切れる と逆に計算する。", "分子中の結合の数（$\\mathrm{NH_3}$ の N−H は3本など）を数え誤る。"])
    unk = r.choice(allb)
    data = "、".join(f"${BE_TEX[b]}$ {BE[b]}" for b in allb if b != unk)
    side = "切れる" if unk in brk else "できる"
    k = brk.get(unk) or frm.get(unk)
    return intq(f"次の反応の反応エンタルピーは $\\Delta H={dH}$ kJ である。結合エネルギー（kJ/mol）を {data} として、${BE_TEX[unk]}$ の結合エネルギーを求めなさい。\n$${eq}$$",
                sp.Integer(BE[unk]), f"({dH}-({br - (BE[unk] * k if side == '切れる' else 0)})+({fo - (BE[unk] * k if side == 'できる' else 0)}))/({k if side == '切れる' else -k})",
                f"{unk} は{side}結合で {k} 本。ΔH＝（切れる）−（できる）に代入して解く。", unit="kJ/mol", d=3,
                ap="ΔH＝（切れる結合の和）−（できる結合の和）の式で、求める結合エネルギーを $x$ とおく。",
                steps=[f"${BE_TEX[unk]}$ の結合エネルギーを $x$ とおく（{side}結合で {k} 本）。",
                       f"$({br - (BE[unk] * k if side == '切れる' else 0)}{'+' + str(k) + 'x' if side == '切れる' else ''})-({fo - (BE[unk] * k if side == 'できる' else 0)}{'+' + str(k) + 'x' if side == 'できる' else ''})={dH}$。",
                       f"$x={BE[unk]}$ kJ/mol。"],
                alt=["求めた値を使って ΔH を計算し直し、与えられた値に一致するか確かめる。"],
                pc=[("式を正しく立てている", 2), ("値が正しい", 2)], pit=["結合の本数を掛け忘れる。"])


@gen("standard_practice", 4, ["computation", "application"])
def eq_calc(r):
    form = r.choice(["HI", "HI", "N2O4c", "N2O4p", "ester"])
    if form == "HI":
        K = r.choice([4, 9, 36, 64])
        a = sp.Rational(r.choice(["0.50", "1.0", "2.0", "0.40", "0.20", "1.5"]))
        V = r.choice(["1.0", "2.0", "5.0", "10"])
        s = sp.sqrt(K)
        x = s * a / (2 + s)
        return numq(f"容積 {V} L の容器に水素と（気体の）ヨウ素を {dec(a)} mol ずつ入れて一定温度に保ったところ、$\\mathrm{{H_2}}+\\mathrm{{I_2}}\\rightleftharpoons2\\mathrm{{HI}}$ の平衡に達した。この温度の平衡定数を {K} として、生成したヨウ化水素の物質量を求めなさい。",
                    2 * x, f"2*sqrt({K})*{a}/(2+sqrt({K}))", "反応した $\\mathrm{H_2}$ を $x$ mol として平衡定数の式に代入する。", unit="mol", d=3,
                    ap="反応前・変化量・平衡時の表をつくる。両辺の係数の和が等しいので、体積は約分され物質量のまま代入できる。",
                    steps=[f"平衡時：$\\mathrm{{H_2}}={dec(a)}-x$、$\\mathrm{{I_2}}={dec(a)}-x$、$\\mathrm{{HI}}=2x$（mol）。", f"$\\dfrac{{(2x)^2}}{{({dec(a)}-x)^2}}={K}$。",
                           f"$\\dfrac{{2x}}{{{dec(a)}-x}}={s}$ より $x={sig(x, 3)}$。", f"HI：$2x={sig(2 * x)}$ mol。"],
                    alt=[f"求めた値を代入して $K$ に戻るか確かめる：$\\dfrac{{({sig(2 * x)})^2}}{{({sig(a - x)})^2}}={K}$。"],
                    pc=[("平衡時の物質量を文字で表している", 1), ("平衡定数の式を立てている", 1), ("値が正しい", 2)],
                    pit=["HI の係数 2 を忘れて $x$ を答える。", "負の平方根を選ぶ。"])
    if form == "N2O4c":
        n = sp.Rational(r.choice(["0.10", "0.20", "0.50", "1.0", "0.40"]))
        al = sp.Rational(r.choice(["0.20", "0.25", "0.40", "0.50", "0.10"]))
        V = sp.Rational(r.choice(["1.0", "2.0", "5.0", "10"]))
        Kc = (2 * n * al / V) ** 2 / (n * (1 - al) / V)
        return numq(f"容積 {dec(V)} L の容器に四酸化二窒素 $\\mathrm{{N_2O_4}}$ を {dec(n)} mol 入れて一定温度に保つと、$\\mathrm{{N_2O_4}}\\rightleftharpoons2\\mathrm{{NO_2}}$ の平衡に達し、$\\mathrm{{N_2O_4}}$ の {dec(al * 100)} % が解離した。この温度の平衡定数 $K$（mol/L）を求めなさい。",
                    Kc, f"(2*{n}*{al}/({V}))**2/({n}*(1-{al})/({V}))", f"$[\\mathrm{{N_2O_4}}]=\\dfrac{{{dec(n)}(1-{dec(al)})}}{{{dec(V)}}}$、$[\\mathrm{{NO_2}}]=\\dfrac{{2\\times{dec(n)}\\times{dec(al)}}}{{{dec(V)}}}$。",
                    unit="mol/L", d=3,
                    ap="解離度 α から平衡時の物質量を表し、体積で割って濃度にする（両辺の係数の和が異なるので体積は約分されない）。",
                    steps=[f"平衡時：$\\mathrm{{N_2O_4}}$ ${dec(n * (1 - al))}$ mol、$\\mathrm{{NO_2}}$ ${dec(2 * n * al)}$ mol。",
                           f"濃度：${dec(n * (1 - al) / V)}$ mol/L、${dec(2 * n * al / V)}$ mol/L。", f"$K=\\dfrac{{({dec(2 * n * al / V)})^2}}{{{dec(n * (1 - al) / V)}}}={sig(Kc)}$ mol/L。"],
                    alt=["一般式 $K=\\dfrac{4n\\alpha^2}{V(1-\\alpha)}$ を導いてから代入してもよい。"],
                    pc=[("平衡時の物質量を求めている", 1), ("濃度に直している", 1), ("値が正しい", 2)], pit=["物質量のまま代入する。", "$\\mathrm{NO_2}$ が $2n\\alpha$ になることを忘れる。"])
    if form == "N2O4p":
        al = sp.Rational(r.choice(["0.20", "0.25", "0.40", "0.50", "0.60"]))
        P = sp.Rational(r.choice(["1.0", "2.0", "0.50", "3.0"])) * 10 ** 5
        Kp = 4 * al ** 2 * P / (1 - al ** 2)
        return numq(f"$\\mathrm{{N_2O_4}}\\rightleftharpoons2\\mathrm{{NO_2}}$ の平衡で、全圧 ${sci(P)}$ Pa のとき $\\mathrm{{N_2O_4}}$ の解離度は {dec(al)} であった。圧平衡定数 $K_{{\\mathrm{{p}}}}$（Pa）を求めなさい。",
                    Kp, f"4*({al})**2*{P}/(1-({al})**2)", "モル分率から分圧を求め、$K_{\\mathrm{p}}=\\dfrac{p_{\\mathrm{NO_2}}^2}{p_{\\mathrm{N_2O_4}}}$ に代入する。", unit="Pa", d=4,
                    ap="はじめの $\\mathrm{N_2O_4}$ を 1 mol とすると、平衡時 $\\mathrm{N_2O_4}\\ 1-\\alpha$、$\\mathrm{NO_2}\\ 2\\alpha$、合計 $1+\\alpha$ mol。分圧＝全圧×モル分率。",
                    steps=[f"$p_{{\\mathrm{{N_2O_4}}}}=P\\times\\dfrac{{1-\\alpha}}{{1+\\alpha}}$、$p_{{\\mathrm{{NO_2}}}}=P\\times\\dfrac{{2\\alpha}}{{1+\\alpha}}$。",
                           "$K_{\\mathrm{p}}=\\dfrac{4\\alpha^2}{1-\\alpha^2}P$。", f"$=\\dfrac{{4\\times{dec(al)}^2}}{{1-{dec(al)}^2}}\\times{sci(P)}={sig(Kp)}$ Pa。"],
                    alt=["数値を直接分圧に代入して計算し、一般式の結果と一致するか確かめる。"],
                    pc=[("モル分率から分圧を求めている", 2), ("値が正しい", 2)], pit=["全物質量を 1 mol のままとして分圧を求める。"])
    a = sp.Rational(1)
    b = sp.Rational(r.choice(["1.0", "2.0", "3.0", "0.50"]))
    K = 4
    x = (4 * (a + b) - sp.sqrt(16 * (a + b) ** 2 - 48 * a * b)) / 6
    return numq(f"酢酸 1.0 mol とエタノール {dec(b)} mol を混合し、少量の濃硫酸を加えて一定温度に保つと、$\\mathrm{{CH_3COOH}}+\\mathrm{{C_2H_5OH}}\\rightleftharpoons\\mathrm{{CH_3COOC_2H_5}}+\\mathrm{{H_2O}}$ の平衡に達した。この温度の平衡定数を 4.0 として、生成した酢酸エチルの物質量を求めなさい。",
                x, f"(4*(1+{b})-sqrt(16*(1+{b})**2-48*{b}))/6", "生成した酢酸エチルを $x$ mol として2次方程式を解き、条件に合う解を選ぶ。", unit="mol", d=4,
                ap="反応前・変化量・平衡時の表をつくり、$\\dfrac{x^2}{(1.0-x)(" + dec(b) + "-x)}=4.0$ を解く（体積は約分される）。",
                steps=[f"平衡時：酢酸 $1.0-x$、エタノール ${dec(b)}-x$、酢酸エチル $x$、水 $x$（mol）。", f"$x^2=4.0(1.0-x)({dec(b)}-x)$ を整理して $3x^2-{dec(4 * (1 + b))}x+{dec(4 * b)}=0$。",
                       f"$0<x<{dec(min(a, b))}$ を満たす解は $x\\fallingdotseq{sig(x)}$ mol。"],
                alt=["もう一方の解が $x>" + dec(min(a, b)) + "$ となり、平衡時の物質量が負になるので不適であることを確認する。"],
                pc=[("平衡時の物質量を表している", 1), ("2次方程式を立てている", 1), ("適する解を選び値が正しい", 2)],
                pit=["2つの解のうち不適なものを選ぶ。", "水を平衡定数の式から除く（この反応では溶媒ではないので含める）。"])


def ph_pick(r):
    for _ in range(300):
        s = r.choice([1, 2, 3, 4])
        k = r.choice([3, 4])
        h = sp.Rational(s) / 10 ** k
        c = sp.Rational(r.choice(["0.10", "0.010", "0.040", "0.20", "0.050", "0.080", "0.16", "0.30"]))
        Ka = h ** 2 / c
        mant = Ka / sp.Integer(10) ** (sp.floor(sp.log(Ka, 10)))
        if mant.q == 1 or (mant * 10).q == 1:
            if h / c <= sp.Rational(1, 20):
                return s, k, h, c, Ka
    return 1, 3, sp.Rational(1, 1000), sp.Rational(1, 10), sp.Rational(1, 100000)


PH_LOG = {1: "0", 2: "0.30", 3: "0.48", 4: "0.60"}


@gen("standard_practice", 4, ["computation", "condition_check"])
def weak_acid(r):
    form = r.choice(["ph", "ph", "alpha", "base"])
    s, k, h, c, Ka = ph_pick(r)
    pH = k - sp.Rational(PH_LOG[s])
    if form == "ph":
        return sa(f"濃度 {dec(c)} mol/L の1価の弱酸 HA の水溶液の pH を、小数第2位まで求めなさい。HA の電離定数を $K_{{\\mathrm{{a}}}}={sci(Ka)}$ mol/L とし、電離度は 1 に比べて十分小さいものとする。{LOGS}",
                  f"{float(pH):.2f}", f"$[\\mathrm{{H^+}}]=\\sqrt{{cK_{{\\mathrm{{a}}}}}}={sci(h)}$ mol/L、pH＝${k}-\\log_{{10}}{s}={float(pH):.2f}$。", d=3,
                  ap="弱酸では $[\\mathrm{H^+}]=c\\alpha$、$\\alpha\\fallingdotseq\\sqrt{K_{\\mathrm{a}}/c}$ より $[\\mathrm{H^+}]\\fallingdotseq\\sqrt{cK_{\\mathrm{a}}}$。",
                  steps=[f"$cK_{{\\mathrm{{a}}}}={dec(c)}\\times{sci(Ka)}={sci(c * Ka)}$。", f"$[\\mathrm{{H^+}}]=\\sqrt{{{sci(c * Ka)}}}={sci(h)}$ mol/L。",
                         f"$\\mathrm{{pH}}=-\\log_{{10}}({sci(h)})={k}-\\log_{{10}}{s}={float(pH):.2f}$。"],
                  alt=[f"電離度 $\\alpha=\\dfrac{{[\\mathrm{{H^+}}]}}{{c}}={sig(h / c)}$ が 1 より十分小さく、近似が妥当であることを確認する。"],
                  pc=[("$[\\mathrm{H^+}]$ を正しく求めている", 2), ("pH が正しい", 2)], pit=["完全に電離するとして $[\\mathrm{H^+}]=c$ とする。", "平方根をとり忘れる。"],
                  chk=(f"sqrt({c}*{Ka})", str(h), None, "intermediate"))
    if form == "alpha":
        al = h / c
        return numq(f"濃度 {dec(c)} mol/L の1価の弱酸 HA の電離度を求めなさい。電離定数は $K_{{\\mathrm{{a}}}}={sci(Ka)}$ mol/L とし、電離度は 1 に比べて十分小さいものとする。",
                    al, f"sqrt({Ka}/({c}))", "$\\alpha\\fallingdotseq\\sqrt{\\dfrac{K_{\\mathrm{a}}}{c}}$。", d=3,
                    ap="$K_{\\mathrm{a}}=\\dfrac{c\\alpha^2}{1-\\alpha}\\fallingdotseq c\\alpha^2$ を $\\alpha$ について解く。",
                    steps=[f"$\\alpha^2=\\dfrac{{{sci(Ka)}}}{{{dec(c)}}}={sci(Ka / c)}$。", f"$\\alpha={sig(al)}$。"],
                    alt=["$1-\\alpha\\fallingdotseq1$ の近似を使わずに2次方程式を解いても、ほぼ同じ値になることを確かめる。"],
                    pc=[("近似式を立てている", 2), ("値が正しい", 2)], pit=["$\\alpha=\\dfrac{K_{\\mathrm{a}}}{c}$ と平方根をとり忘れる。"])
    pOH = pH
    pHb = 14 - pOH
    return sa(f"濃度 {dec(c)} mol/L のアンモニア水の pH を、小数第2位まで求めなさい。アンモニアの電離定数を $K_{{\\mathrm{{b}}}}={sci(Ka)}$ mol/L とし、電離度は 1 に比べて十分小さいものとする。{KW}{LOGS}",
              f"{float(pHb):.2f}",
              f"$[\\mathrm{{OH^-}}]=\\sqrt{{cK_{{\\mathrm{{b}}}}}}={sci(h)}$ mol/L、pOH＝{float(pOH):.2f}、pH＝14−pOH。", d=4,
              ap="弱塩基でも同様に $[\\mathrm{OH^-}]\\fallingdotseq\\sqrt{cK_{\\mathrm{b}}}$。pOH を求めて pH＝14−pOH。",
              steps=[f"$[\\mathrm{{OH^-}}]=\\sqrt{{{dec(c)}\\times{sci(Ka)}}}={sci(h)}$ mol/L。", f"pOH＝${k}-\\log_{{10}}{s}={float(pOH):.2f}$。",
                     f"pH＝$14-{float(pOH):.2f}={float(pHb):.2f}$。"],
              alt=["$[\\mathrm{H^+}]=\\dfrac{K_{\\mathrm{w}}}{[\\mathrm{OH^-}]}$ を求めてから pH を計算してもよい。"],
              pc=[("$[\\mathrm{OH^-}]$ を求めている", 2), ("pH が正しい", 2)], pit=["pOH をそのまま pH とする。"],
              chk=(f"sqrt({c}*{Ka})", str(h), None, "intermediate"))


def kunit_rate(order):
    return {1: "/s", 2: "L/(mol·s)", 3: "L²/(mol²·s)", 4: "L³/(mol³·s)"}[order]


@gen("standard_practice", 3, ["computation", "written_reasoning"])
def rate_data(r):
    a, b = r.choice([(1, 1), (2, 1), (1, 2), (2, 0), (1, 0), (0, 1), (0, 2)])
    v1 = sp.Rational(r.choice(["1.0", "2.0", "3.0", "4.0", "1.5", "2.5"])) / 1000
    A0, B0 = sp.Rational("0.10"), sp.Rational("0.10")
    kA, kB = r.choice([(2, 3), (3, 2), (2, 2), (2, 4)])
    k = v1 / (A0 ** a * B0 ** b)
    rows = [(A0, B0), (A0 * kA, B0), (A0, B0 * kB)]
    vs = [k * x ** a * y ** b for x, y in rows]
    tbl = table([[str(i + 1), dec(x), dec(y), sci(v, 2)] for i, ((x, y), v) in enumerate(zip(rows, vs))],
                header=["実験", "[A]（mol/L）", "[B]（mol/L）", "初速度 v（mol/(L·s)）"], caption="A＋B → C の初速度の測定（一定温度）")
    rl = "v=k" + (f"[\\mathrm{{A}}]^{{{a}}}" if a > 1 else ("[\\mathrm{A}]" if a == 1 else "")) + (f"[\\mathrm{{B}}]^{{{b}}}" if b > 1 else ("[\\mathrm{B}]" if b == 1 else ""))
    nA = sp.Rational(r.choice(["0.30", "0.20", "0.40", "0.050", "0.15"]))
    nB = sp.Rational(r.choice(["0.20", "0.30", "0.050", "0.40", "0.25"]))
    vn = k * nA ** a * nB ** b
    order = a + b
    return sa(f"表は、反応 A＋B → C の初速度を、A と B の濃度を変えて測定した結果である。\n(1) 速度式 $v=k[\\mathrm{{A}}]^x[\\mathrm{{B}}]^y$ の $x,\\ y$ を求めなさい。\n(2) 速度定数 $k$ を単位とともに求めなさい。\n(3) [A]＝{dec(nA)} mol/L、[B]＝{dec(nB)} mol/L のときの初速度を求めなさい。",
              f"(1) $x={a}$、$y={b}$（${rl}$）　(2) $k={sig(k)}$ {kunit_rate(order)}　(3) ${sci(vn)}$ mol/(L·s)",
              f"実験1と2の比から A の次数、実験1と3の比から B の次数が分かる。", d=4, tbl=tbl,
              ap="一方の濃度だけを変えた2つの実験を比べ、濃度の倍率と速度の倍率の関係（倍率の何乗か）から次数を決める。",
              steps=[f"実験1→2：[A] が {kA} 倍で v が ${dec(vs[1] / vs[0])}$ 倍 → $x={a}$。", f"実験1→3：[B] が {kB} 倍で v が ${dec(vs[2] / vs[0])}$ 倍 → $y={b}$。",
                     f"実験1の値を代入：$k=\\dfrac{{{sci(vs[0])}}}{{{'(0.10)' + ('^' + str(a) if a > 1 else '') if a else ''}{'(0.10)' + ('^' + str(b) if b > 1 else '') if b else ''}}}={sig(k)}$ {kunit_rate(order)}。".replace("dfrac{" + sci(vs[0]) + "}{}", "dfrac{" + sci(vs[0]) + "}{1}"),
                     f"(3) $v={sig(k)}" + (f"\\times{dec(nA)}" + (f"^{a}" if a > 1 else "") if a else "") + (f"\\times{dec(nB)}" + (f"^{b}" if b > 1 else "") if b else "") + f"={sci(vn)}$ mol/(L·s)。"],
              alt=["実験2や実験3の値で $k$ を求めても同じ値になることを確かめる。"],
              pc=[("次数を正しく決めている", 2), ("$k$ と単位が正しい", 1), ("初速度が正しい", 1)],
              pit=["化学反応式の係数（1, 1）をそのまま次数とする。", "k の単位を書き忘れる。"],
              chk=(f"{vs[0]}/((Rational(1,10))**{a}*(Rational(1,10))**{b})", str(k), None, "intermediate"))


# ======================================================================
# C 思考力・記述応用
# ======================================================================

@gen("thinking_writing", 3, ["cross_unit", "computation", "written_reasoning"], rel=["HS-CHEB-U03"])
def buffer(r):
    for _ in range(300):
        ca = sp.Rational(r.choice(["0.10", "0.20", "0.050", "0.15"]))
        cs = sp.Rational(r.choice(["0.10", "0.20", "0.050", "0.40"]))
        n = sp.Rational(r.choice(["0.010", "0.020", "0.025", "0.050", "0.0050"]))
        Ka = sp.Rational("2.0") / 10 ** 5
        if n >= cs:
            continue
        h1 = Ka * ca / cs
        h2 = Ka * (ca + n) / (cs - n)

        def ok(h):
            e = sp.floor(sp.log(h, 10))
            m = h / sp.Integer(10) ** e
            return m in (1, 2, 3, 4, 6, 8, 9)
        if ok(h1) and ok(h2) and h1 != h2:
            break

    def ph_of(h):
        e = int(sp.floor(sp.log(h, 10)))
        m = int(h / sp.Integer(10) ** e)
        lg = {1: 0, 2: sp.Rational("0.30"), 3: sp.Rational("0.48"), 4: sp.Rational("0.60"), 6: sp.Rational("0.78"), 8: sp.Rational("0.90"), 9: sp.Rational("0.96")}[m]
        return -e - lg
    p1, p2 = ph_of(h1), ph_of(h2)
    pw = -sp.log(n, 10)
    fmt = lambda p: f"{float(p):.2f}"  # noqa: E731
    return desc(f"酢酸 {dec(ca)} mol と酢酸ナトリウム {dec(cs)} mol を水に溶かして 1.0 L とした水溶液がある。酢酸の電離定数を $K_{{\\mathrm{{a}}}}=2.0\\times10^{{-5}}$ mol/L、{LOGS}\n"
                f"(1) この水溶液の pH を小数第2位まで求めなさい。\n(2) この水溶液に塩化水素 {dec(n)} mol を加えた（体積変化は無視）。pH を小数第2位まで求め、pH がほとんど変化しない理由をイオン反応式を用いて説明しなさい。",
                f"(1) $[\\mathrm{{H^+}}]=K_{{\\mathrm{{a}}}}\\times\\dfrac{{{dec(ca)}}}{{{dec(cs)}}}={sci(h1)}$ mol/L、pH {fmt(p1)}。"
                f"(2) $\\mathrm{{CH_3COO^-}}+\\mathrm{{H^+}}\\longrightarrow\\mathrm{{CH_3COOH}}$ により、加えた $\\mathrm{{H^+}}$ の大部分が酢酸イオンと結びついて酢酸になる。酢酸 ${dec(ca + n)}$ mol、酢酸イオン ${dec(cs - n)}$ mol となり、"
                f"$[\\mathrm{{H^+}}]={sci(h2)}$ mol/L、pH {fmt(p2)}。（同じ量の塩化水素を純水 1.0 L に加えると pH は約 {float(pw):.1f} になるので、変化はずっと小さい。）",
                "緩衝液では、多量にある酢酸イオンが加えた $\\mathrm{H^+}$ を受け取り、弱酸である酢酸に変える。",
                [("(1) 緩衝液の $[\\mathrm{H^+}]$ の式を用いて pH を求めている", 2), ("(2) 加えた $\\mathrm{H^+}$ が酢酸イオンと反応することを、イオン反応式で示している", 3),
                 ("(2) 反応後の物質量から pH を求めている", 2), ("純水の場合との比較など、変化が小さいことを示している", 1)],
                d=5, p=8, lines=10,
                ap="酢酸ナトリウムは完全に電離し、酢酸イオンが多量にあるため酢酸の電離はおさえられる。$[\\mathrm{CH_3COOH}]$ と $[\\mathrm{CH_3COO^-}]$ は加えた量のままとみなし、$[\\mathrm{H^+}]=K_{\\mathrm{a}}\\dfrac{[\\mathrm{CH_3COOH}]}{[\\mathrm{CH_3COO^-}]}$（pH の定義と強酸の扱いは化学基礎の内容）。",
                steps=[f"(1) $[\\mathrm{{H^+}}]=2.0\\times10^{{-5}}\\times\\dfrac{{{dec(ca)}}}{{{dec(cs)}}}={sci(h1)}$ mol/L、pH＝{fmt(p1)}。",
                       f"(2) 加えた $\\mathrm{{H^+}}$ {dec(n)} mol は $\\mathrm{{CH_3COO^-}}$ と反応：酢酸 ${dec(ca + n)}$ mol、酢酸イオン ${dec(cs - n)}$ mol。",
                       f"$[\\mathrm{{H^+}}]=2.0\\times10^{{-5}}\\times\\dfrac{{{dec(ca + n)}}}{{{dec(cs - n)}}}={sci(h2)}$ mol/L、pH＝{fmt(p2)}。"],
                alt=["$\\mathrm{pH}=\\mathrm{p}K_{\\mathrm{a}}+\\log_{10}\\dfrac{[\\mathrm{CH_3COO^-}]}{[\\mathrm{CH_3COOH}]}$ の形で計算してもよい。"],
                pc=[("(1)", 2), ("イオン反応式", 3), ("(2) の pH", 2), ("比較", 1)],
                pit=["加えた $\\mathrm{H^+}$ がそのまま残ると考える。", "酢酸の濃度を $c$、酢酸イオンを $c\\alpha$ のように弱酸単独の式で計算する。"],
                chk=(f"[2*10**(-5)*{ca}/({cs}), 2*10**(-5)*({ca}+{n})/({cs}-{n})]", f"[{h1}, {h2}]", None, "intermediate"))


@gen("thinking_writing", 3, ["written_reasoning", "computation"])
def energy_diagram(r):
    Ea = r.choice([60, 80, 100, 120, 150, 180, 75, 90])
    dH = r.choice([-40, -60, -90, -120, 30, 50, -25, 40])
    if dH > 0 and dH >= Ea:
        dH = -dH
    cat = Ea - r.choice([20, 30, 40])
    rev = Ea - dH
    return desc(f"図は、ある気体反応 A → B の進行に伴うエンタルピーの変化を表したもので、触媒がないときの活性化エネルギーは {Ea} kJ/mol、反応エンタルピーは $\\Delta H={sgn(dH)}$ kJ/mol である。"
                f"触媒を加えると活性化エネルギーは {cat} kJ/mol になった。\n(1) 触媒がないとき、逆反応 B → A の活性化エネルギーは何 kJ/mol か。\n(2) 触媒を加えたとき、逆反応の活性化エネルギーと反応エンタルピー、平衡の位置はどうなるか。理由とともに答えなさい。\n"
                "(3) 温度を上げると反応速度が大きくなる理由を、分子のエネルギーの分布にふれて説明しなさい。",
                f"(1) 逆反応では生成物から遷移状態までの差なので ${Ea}-({sgn(dH)})={rev}$ kJ/mol。"
                f"(2) 逆反応の活性化エネルギーは ${cat}-({sgn(dH)})={cat - dH}$ kJ/mol に小さくなる。反応物と生成物のエンタルピーは変わらないので $\\Delta H$ は ${sgn(dH)}$ kJ/mol のまま。触媒は正反応と逆反応を同じように速めるので、平衡の位置は変わらない（平衡に達するまでの時間が短くなる）。"
                "(3) 温度を上げると分子の運動エネルギーの分布が高エネルギー側に広がり、活性化エネルギー以上のエネルギーをもつ分子の割合が大きく増えるため、反応できる衝突が増える。",
                "活性化エネルギーは山の高さ、ΔH は両端の高さの差。触媒は山だけを低くする。",
                [("(1) 逆反応の活性化エネルギーを正しく求めている", 2), ("(2) ΔH と平衡が変わらない理由を述べている", 3), ("(2) 逆反応の活性化エネルギーの値", 1),
                 ("(3) 活性化エネルギー以上の分子の割合の増加で説明している", 2)],
                d=4, p=8, lines=10, fig=energy_fig(Ea, dH, cat, "反応の進行とエンタルピー（概形）"),
                ap="図で、反応物・遷移状態・生成物の3つの高さを確認する。逆反応は生成物から遷移状態へ上がる。",
                steps=[f"遷移状態は反応物より {Ea} kJ 高く、生成物は反応物より {abs(dH)} kJ {'低い' if dH < 0 else '高い'}。",
                       f"逆反応の活性化エネルギー：${Ea}-({sgn(dH)})={rev}$ kJ/mol。", f"触媒あり：${cat}-({sgn(dH)})={cat - dH}$ kJ/mol。ΔH は不変。",
                       "温度上昇で、$E_{\\mathrm{a}}$ をこえる分子の割合が増える。"],
                alt=["正反応と逆反応の活性化エネルギーの差が ΔH になる（$E_{\\mathrm{a,正}}-E_{\\mathrm{a,逆}}=\\Delta H$）ことを使って確かめる。"],
                pc=[("(1)", 2), ("(2) 理由", 3), ("(2) 値", 1), ("(3)", 2)],
                pit=["逆反応の活性化エネルギーを正反応と同じとする。", "触媒で ΔH も小さくなると考える。", "温度上昇の効果を「衝突回数の増加」だけで説明する。"],
                chk=(f"[{Ea}-({dH}), {cat}-({dH})]", f"[{rev}, {cat - dH}]", None, "intermediate"))


LC_EXPLAIN = [("N2+3H2⇌2NH3", "アンモニアの工業的製法（ハーバー・ボッシュ法）では、鉄を主成分とする触媒を用い、約 400〜500 ℃、$1\\times10^{7}$〜$3\\times10^{7}$ Pa 程度の高圧で反応させる。",
               "(1) 平衡の面から、アンモニアの生成に有利な温度・圧力の条件を理由とともに答えなさい。\n(2) それにもかかわらず、低温ではなく 400〜500 ℃ 程度で反応させる理由を、反応速度と触媒の役割にふれて説明しなさい。",
               "(1) 正反応は発熱反応なので低温ほど、また気体分子の数が減る反応（4 分子 → 2 分子）なので高圧ほど平衡が右に移動し、有利である。"
               "(2) 低温では平衡は有利でも反応速度が非常に小さく、平衡に達するまでに時間がかかりすぎる。そこで触媒を用いて活性化エネルギーを下げたうえで、ある程度高い温度にして速度を確保している。触媒は平衡の位置を変えないので、温度は収率と速度のかね合いで決まる。",
               [("(1) 低温を発熱反応で説明している", 2), ("(1) 高圧を気体分子数の減少で説明している", 2), ("(2) 低温では速度が小さいことを述べている", 2), ("(2) 触媒は平衡を変えず速度を上げることを述べている", 2)]),
              ("2SO2+O2⇌2SO3", "硫酸の工業的製法（接触法）では、酸化バナジウム(Ⅴ) $\\mathrm{V_2O_5}$ を触媒として、二酸化硫黄を酸素で酸化して三酸化硫黄にする（正反応は発熱反応）。",
               "(1) 平衡の面から、三酸化硫黄の生成に有利な温度・圧力の条件を理由とともに答えなさい。\n(2) 温度を低くしすぎない理由と、触媒を用いる理由を説明しなさい。",
               "(1) 正反応は発熱反応なので低温ほど、気体分子の数が減る反応（3 分子 → 2 分子）なので高圧ほど平衡が右に移動し、有利である。"
               "(2) 低温では反応速度が小さく、平衡に達するのに時間がかかるため。触媒は活性化エネルギーを下げて反応を速くするが、平衡の位置は変えないので、収率と速度の両方を考えて温度を選ぶ。",
               [("(1) 低温を発熱反応で説明している", 2), ("(1) 高圧を気体分子数の減少で説明している", 2), ("(2) 低温では速度が小さいことを述べている", 2), ("(2) 触媒の役割を正しく述べている", 2)]),
              ("N2O4⇌2NO2", "赤褐色の二酸化窒素 $\\mathrm{NO_2}$ と無色の四酸化二窒素 $\\mathrm{N_2O_4}$ の混合気体を注射器に入れ、平衡状態にした（$\\mathrm{N_2O_4}\\rightleftharpoons2\\mathrm{NO_2}$、正反応は吸熱反応）。",
               "(1) 注射器ごと氷水で冷やすと、気体の色はどうなるか。理由とともに答えなさい。\n(2) 温度を一定に保ったままピストンを押して体積を半分にすると、直後に色が濃くなり、その後少しうすくなる。この変化を説明しなさい。",
               "(1) 冷却すると発熱反応の向き（左向き）に平衡が移動し、赤褐色の $\\mathrm{NO_2}$ が減るので、色はうすくなる。"
               "(2) 体積を半分にした直後は $\\mathrm{NO_2}$ の濃度が2倍になるので色が濃くなる。その後、圧力の増加をやわらげるため気体分子の数が減る向き（左向き）に平衡が移動し、$\\mathrm{NO_2}$ が一部 $\\mathrm{N_2O_4}$ になるので少しうすくなる（それでも圧縮前よりは濃い）。",
               [("(1) 冷却で左に移動することを ΔH の符号から説明している", 3), ("(2) 直後に濃くなる理由（濃度の増加）を述べている", 2), ("(2) その後の平衡移動の向きと理由を述べている", 3)])]


@gen("thinking_writing", 2, ["written_reasoning", "concept"])
def lc_explain(r):
    _, intro_, qs, ans, rub = r.choice(LC_EXPLAIN)
    lead = r.choice(["", "次の文章を読んで、問いに答えなさい。\n"])
    return desc(f"{lead}{intro_}\n{qs}", ans, "平衡（どこまで進むか）と速度（どれだけ速く進むか）を分けて考える。", rub, d=4, p=8, lines=9,
                ap="ルシャトリエの原理で平衡の移動を判断し、反応速度（温度・触媒）の観点を別に考える。触媒は平衡を変えない。",
                steps=["正反応の ΔH の符号から、温度による平衡移動の向きを決める。", "両辺の気体分子の数から、圧力による移動の向きを決める。", "速度の観点（温度・触媒）を加えて、条件の選び方や観察結果を説明する。"],
                alt=["平衡定数の式で、濃度商 $Q$ と $K$ を比べる方法で平衡移動の向きを確かめてもよい。"],
                pc=[(a, b) for a, b in rub], pit=["平衡の有利さと反応の速さを区別せずに説明する。", "触媒で平衡が移動すると書く。"])


@gen("thinking_writing", 2, ["written_reasoning", "computation", "condition_check"])
def ksp(r):
    Ksp = sp.Rational("1.8") / 10 ** 10
    c1 = sp.Rational(r.choice(["1.0", "2.0", "4.0", "1.0", "5.0"])) / 10 ** r.choice([4, 5, 6])
    c2 = sp.Rational(r.choice(["1.0", "2.0", "4.0", "5.0"])) / 10 ** r.choice([4, 5, 6])
    V1, V2 = r.choice([(100, 100), (50, 50), (10, 10), (200, 200)])
    a, b = c1 / 2, c2 / 2
    prod = a * b
    ppt = prod > Ksp
    cl = sp.Rational(r.choice(["0.10", "0.010", "0.050"]))
    s = Ksp / cl
    return desc(f"25 ℃ における塩化銀 AgCl の溶解度積を $K_{{\\mathrm{{sp}}}}=1.8\\times10^{{-10}}\\ (\\mathrm{{mol/L}})^2$ とする。\n"
                f"(1) ${sci(c1)}$ mol/L の硝酸銀水溶液 {V1} mL と ${sci(c2)}$ mol/L の塩化ナトリウム水溶液 {V2} mL を混合したとき、塩化銀の沈殿は生じるか。計算の根拠とともに答えなさい（体積は和になるものとする）。\n"
                f"(2) {dec(cl)} mol/L の塩化ナトリウム水溶液に溶ける塩化銀の最大の物質量は、水溶液 1 L あたり何 mol か。また、純水に溶ける量と比べて小さくなる理由を説明しなさい。有効数字2桁で答えなさい。",
                f"(1) 混合直後 $[\\mathrm{{Ag^+}}]={sci(a)}$ mol/L、$[\\mathrm{{Cl^-}}]={sci(b)}$ mol/L、積は ${sci(prod)}$ $(\\mathrm{{mol/L}})^2$。これは $K_{{\\mathrm{{sp}}}}$ より{'大きいので沈殿が生じる' if ppt else '小さいので沈殿は生じない'}。"
                f"(2) $[\\mathrm{{Cl^-}}]\\fallingdotseq{dec(cl)}$ mol/L とみなすと、$[\\mathrm{{Ag^+}}]=\\dfrac{{1.8\\times10^{{-10}}}}{{{dec(cl)}}}={sci(s)}$ mol/L なので ${sci(s)}$ mol。"
                "塩化物イオンが多量にあると、$\\mathrm{AgCl}\\rightleftharpoons\\mathrm{Ag^+}+\\mathrm{Cl^-}$ の平衡が左に移動し（共通イオン効果）、溶ける量が小さくなる（純水では約 $1.3\\times10^{-5}$ mol）。",
                "イオン濃度の積と $K_{\\mathrm{sp}}$ を比べる。共通イオンがあると溶解度が下がる。",
                [("(1) 混合後の濃度（体積が2倍で半分）を求めている", 2), ("(1) 積と $K_{\\mathrm{sp}}$ を比べて判断している", 2), ("(2) 溶ける量を正しく求めている", 2), ("(2) 共通イオン効果で説明している", 2)],
                d=4, p=8, lines=9,
                ap="混合すると体積が2倍になり、各イオンの濃度は半分になる。$[\\mathrm{Ag^+}][\\mathrm{Cl^-}]>K_{\\mathrm{sp}}$ なら沈殿が生じる。",
                steps=[f"(1) $[\\mathrm{{Ag^+}}]={sci(c1)}\\times\\dfrac{{1}}{{2}}={sci(a)}$、$[\\mathrm{{Cl^-}}]={sci(b)}$ mol/L。", f"積 ${sci(prod)}$ と $1.8\\times10^{{-10}}$ を比較。",
                       f"(2) $[\\mathrm{{Ag^+}}]\\times{dec(cl)}=1.8\\times10^{{-10}}$ より ${sci(s)}$ mol/L。", "ルシャトリエの原理（共通イオン効果）で理由を述べる。"],
                alt=["純水への溶解度 $\\sqrt{1.8\\times10^{-10}}\\fallingdotseq1.3\\times10^{-5}$ mol/L を求め、数値で比べてもよい。"],
                pc=[("混合後の濃度", 2), ("判断", 2), ("溶解量", 2), ("理由", 2)],
                pit=["混合による濃度の変化（半分になる）を考えない。", "溶けた AgCl からの $\\mathrm{Cl^-}$ を足して計算を複雑にする（無視できる）。"],
                chk=(f"[{c1}/2*{c2}/2, Rational(18,10)*10**(-10)/({cl})]", f"[{prod}, {s}]", None, "intermediate"))


# ======================================================================
# D 典型誤答訂正
# ======================================================================

@gen("error_correction", 4, ["common_error", "computation"])
def err_hess(r):
    form = r.choice(["reverse", "coef", "bond"])
    if form == "reverse":
        lhs, rhs = r.choice(HESS_RX)
        dH = dH_of(lhs, rhs)
        used = [(f, ph) for _, f, ph in lhs + rhs if HF[(f, ph)] != 0]
        data = "、".join(f"{FNAME[f]}（{PH[ph]}）${HF[(f, ph)]}$" for f, ph in dict.fromkeys(used))
        sR = sum(c * HF[(f, ph)] for c, f, ph in rhs)
        sL = sum(c * HF[(f, ph)] for c, f, ph in lhs)
        return err_item(f"生成エンタルピー（kJ/mol）を {data} として、次の反応の反応エンタルピー $\\Delta H$ を求めなさい。\n$${te(lhs, rhs)}$$",
                        f"$\\Delta H=（\\text{{反応物}}）-（\\text{{生成物}}）={sL}-({sR})={sgn(-dH)}$ kJ",
                        "引き算の順序", "sign",
                        "燃焼エンタルピーから求めるときの「反応物 − 生成物」の形と混同し、生成エンタルピーでも同じ順に引いている。",
                        f"$\\Delta H=（\\text{{生成物}}）-（\\text{{反応物}}）={sR}-({sL})={dH}$ kJ", f"${dH}$ kJ",
                        "生成エンタルピーは単体を基準にしたエンタルピーなので、ΔH＝（生成物の和）−（反応物の和）。",
                        [f"生成物の和：${sR}$ kJ。", f"反応物の和：${sL}$ kJ。", f"$\\Delta H={sR}-({sL})={dH}$ kJ。"],
                        "エンタルピー図で、単体の基準から反応物・生成物の高さを書き、矢印の向きで符号を確かめる。",
                        ["生成エンタルピーの熱化学反応式を書いて目的の式を組み立て、同じ結果になるか確かめる。"], ["生成エンタルピーと燃焼エンタルピーで引く順序を混同する。"],
                        chk=(f"({sR})-({sL})", str(dH), None, "intermediate"), d=3)
    if form == "coef":
        cands = [x for x in HESS_RX if any(c != 1 for c, f, ph in x[0] + x[1] if HF[(f, ph)] != 0)]
        lhs, rhs = r.choice(cands)
        dH = dH_of(lhs, rhs)
        used = [(f, ph) for _, f, ph in lhs + rhs if HF[(f, ph)] != 0]
        data = "、".join(f"{FNAME[f]}（{PH[ph]}）${HF[(f, ph)]}$" for f, ph in dict.fromkeys(used))
        wR = sum(HF[(f, ph)] for c, f, ph in rhs)
        wL = sum(HF[(f, ph)] for c, f, ph in lhs)
        return err_item(f"生成エンタルピー（kJ/mol）を {data} として、次の反応の反応エンタルピー $\\Delta H$ を求めなさい。\n$${te(lhs, rhs)}$$",
                        f"$\\Delta H=({'+'.join('(' + str(HF[(f, ph)]) + ')' for c, f, ph in rhs)})-({'+'.join('(' + str(HF[(f, ph)]) + ')' for c, f, ph in lhs)})={wR - wL}$ kJ",
                        "係数を掛けずに足し合わせた部分", "calculation",
                        "生成エンタルピーが「1 mol あたり」の値であることを意識せず、物質ごとに1回ずつ足している。",
                        f"係数を掛けて $\\Delta H={dH}$ kJ", f"${dH}$ kJ",
                        "生成エンタルピーは 1 mol あたりの値なので、反応式の係数（物質量）を掛けてから足す。",
                        [f"生成物：${sum(c * HF[(f, ph)] for c, f, ph in rhs)}$ kJ（係数を掛ける）。", f"反応物：${sum(c * HF[(f, ph)] for c, f, ph in lhs)}$ kJ。", f"$\\Delta H={dH}$ kJ。"],
                        "単位で確かめる：kJ/mol × mol（係数）＝ kJ。",
                        ["係数を掛けた和を表にして整理すると見落としを防げる。"], ["係数を掛け忘れる。"],
                        chk=(f"({sum(c * HF[(f, ph)] for c, f, ph in rhs)})-({sum(c * HF[(f, ph)] for c, f, ph in lhs)})", str(dH), None, "intermediate"), d=3)
    _, eq, brk, frm = r.choice(BE_RX)
    br = sum(BE[b] * k for b, k in brk.items())
    fo = sum(BE[b] * k for b, k in frm.items())
    data = "、".join(f"${BE_TEX[b]}$ {BE[b]}" for b in list(brk) + list(frm))
    return err_item(f"結合エネルギー（kJ/mol）を {data} として、次の反応の反応エンタルピー $\\Delta H$ を求めなさい。\n$${eq}$$",
                    f"$\\Delta H=（\\text{{できる結合}}）-（\\text{{切れる結合}}）={fo}-{br}={sgn(fo - br)}$ kJ",
                    "引き算の順序", "sign",
                    "「生成物 − 反応物」という生成エンタルピーの形をそのまま結合エネルギーに当てはめている。結合エネルギーは結合を切るのに必要なエネルギー（正の値）であることを見落としている。",
                    f"$\\Delta H=（\\text{{切れる結合}}）-（\\text{{できる結合}}）={br}-{fo}={br - fo}$ kJ", f"${br - fo}$ kJ",
                    "結合を切るには吸熱（＋）、結合ができると発熱（−）。ΔH＝（切れる結合の和）−（できる結合の和）。",
                    [f"切れる結合の和：{br} kJ。", f"できる結合の和：{fo} kJ。", f"$\\Delta H={br}-{fo}={br - fo}$ kJ。"],
                    "原子にばらばらにする経路をエンタルピー図にかき、どちらが上向き（吸熱）かを確認する。",
                    ["身近な発熱反応（燃焼など）で ΔH が負になるかを確かめる。"], ["生成エンタルピーの公式の形と混同する。"],
                    chk=(f"{br}-{fo}", str(br - fo), None, "intermediate"), d=3)


@gen("error_correction", 3, ["common_error", "condition_check"])
def err_equilibrium(r):
    form = r.choice(["volume", "catalyst", "solid"])
    if form == "volume":
        n = sp.Rational(r.choice(["0.20", "0.50", "1.0", "0.40"]))
        al = sp.Rational(r.choice(["0.20", "0.25", "0.50", "0.40"]))
        V = sp.Rational(r.choice(["2.0", "5.0", "10", "4.0"]))
        wrong = (2 * n * al) ** 2 / (n * (1 - al))
        right = wrong / V
        return err_item(f"容積 {dec(V)} L の容器に $\\mathrm{{N_2O_4}}$ を {dec(n)} mol 入れて一定温度に保つと、$\\mathrm{{N_2O_4}}\\rightleftharpoons2\\mathrm{{NO_2}}$ の平衡に達し、$\\mathrm{{N_2O_4}}$ の {dec(al * 100)} % が解離した。平衡定数 $K$ を求めなさい。",
                        f"平衡時 $\\mathrm{{N_2O_4}}$ {dec(n * (1 - al))} mol、$\\mathrm{{NO_2}}$ {dec(2 * n * al)} mol なので $K=\\dfrac{{{dec(2 * n * al)}^2}}{{{dec(n * (1 - al))}}}={sig(wrong)}$ mol/L",
                        "物質量のまま平衡定数の式に代入した部分", "condition",
                        "$\\mathrm{H_2}+\\mathrm{I_2}\\rightleftharpoons2\\mathrm{HI}$ のように体積が約分できる例に慣れ、両辺の係数の和が異なる場合にも物質量で代入している。",
                        f"濃度に直して $K=\\dfrac{{({dec(2 * n * al / V)})^2}}{{{dec(n * (1 - al) / V)}}}={sig(right)}$ mol/L", f"${sig(right)}$ mol/L",
                        "平衡定数はモル濃度で定義される。両辺の係数の和が異なる反応では体積が約分されないので、必ず体積で割る。",
                        [f"$[\\mathrm{{N_2O_4}}]=\\dfrac{{{dec(n * (1 - al))}}}{{{dec(V)}}}$、$[\\mathrm{{NO_2}}]=\\dfrac{{{dec(2 * n * al)}}}{{{dec(V)}}}$ mol/L。",
                         f"$K=\\dfrac{{[\\mathrm{{NO_2}}]^2}}{{[\\mathrm{{N_2O_4}}]}}={sig(right)}$ mol/L。"],
                        "代入する前に「右辺の係数の和−左辺の係数の和」を計算し、0 でなければ濃度に直す。",
                        ["単位で確かめる：$K$ の単位が mol/L になるのは濃度で代入したときだけ。"], ["物質量のまま代入する。"],
                        chk=(f"(2*{n}*{al}/({V}))**2/({n}*(1-{al})/({V}))", str(right), None, "intermediate"), d=3)
    if form == "catalyst":
        rx = r.choice(LCR[:3])
        return err_item(f"可逆反応 ${rx[1]}$ が平衡状態にある。ここに触媒を加えると、${tex(rx[6])}$ の物質量はどうなるか。理由とともに答えなさい。",
                        f"触媒を加えると正反応が速くなるので、平衡が右に移動し、${tex(rx[6])}$ が増える",
                        "触媒が平衡を移動させるとした部分", "concept",
                        "「触媒は反応を速くする」ことから、正反応だけが速くなると考え、平衡の移動と結びつけている。",
                        f"触媒は正反応と逆反応の活性化エネルギーを同じだけ下げ、両方を同じように速くするので平衡は移動せず、${tex(rx[6])}$ の物質量は変わらない",
                        f"変わらない（平衡は移動しない）",
                        "触媒は反応エンタルピーも平衡定数も変えない。平衡に達するまでの時間が短くなるだけである。",
                        ["触媒は活性化エネルギーの小さい別の経路をつくる。", "正反応・逆反応ともに同じ経路を通るので、両方が速くなる。", "平衡定数は変わらず、平衡は移動しない。"],
                        "触媒の効果を「速さ」と「平衡」の2つの軸に分けて考える。",
                        ["エネルギー図で、触媒により山だけが低くなり、両端の高さ（ΔH）は変わらないことを確かめる。"], ["触媒で生成物が増えると考える。"], d=2)
    T = r.choice(["ある温度", "一定温度"])
    nCO = sp.Rational(r.choice(["0.20", "0.40", "0.60", "0.80"]))
    nCO2 = sp.Rational(r.choice(["0.10", "0.20", "0.40"]))
    nC = sp.Rational(r.choice(["0.50", "1.0", "2.0"]))
    V = sp.Rational(r.choice(["1.0", "2.0"]))
    right = (nCO / V) ** 2 / (nCO2 / V)
    wrong = (nCO / V) ** 2 / (nCO2 / V * nC)
    return err_item(f"容積 {dec(V)} L の容器内で、{T}において $\\mathrm{{C}}\\text{{(黒鉛)}}+\\mathrm{{CO_2}}\\rightleftharpoons2\\mathrm{{CO}}$ が平衡状態にあり、黒鉛 {dec(nC)} mol、$\\mathrm{{CO_2}}$ {dec(nCO2)} mol、CO {dec(nCO)} mol が存在する。平衡定数 $K$ を求めなさい。",
                    f"$K=\\dfrac{{[\\mathrm{{CO}}]^2}}{{[\\mathrm{{C}}][\\mathrm{{CO_2}}]}}$ に、黒鉛も物質量÷体積で代入して $K={sig(wrong)}$",
                    "黒鉛を平衡定数の式に含めた部分", "concept",
                    "反応式に出てくるすべての物質を機械的に式に入れてしまい、固体の濃度が一定とみなせることを考えていない。",
                    f"固体の黒鉛は式に含めず $K=\\dfrac{{[\\mathrm{{CO}}]^2}}{{[\\mathrm{{CO_2}}]}}={sig(right)}$ mol/L", f"${sig(right)}$ mol/L",
                    "固体（や溶媒として多量にある液体）の濃度は一定とみなせるので、平衡定数の式に含めない。",
                    [f"$[\\mathrm{{CO}}]={dec(nCO / V)}$、$[\\mathrm{{CO_2}}]={dec(nCO2 / V)}$ mol/L。", f"$K=\\dfrac{{({dec(nCO / V)})^2}}{{{dec(nCO2 / V)}}}={sig(right)}$ mol/L。"],
                    "平衡定数の式を書くとき、各物質の状態（固体・気体）を確認する。",
                    ["黒鉛を少し加えても平衡が移動しないことと、式に含めないことが対応していると確かめる。"], ["固体を式に含める。"],
                    chk=(f"({nCO}/({V}))**2/({nCO2}/({V}))", str(right), None, "intermediate"), d=3)


@gen("error_correction", 3, ["common_error", "concept"])
def err_weak_acid(r):
    s, k, h, c, Ka = ph_pick(r)
    pH = k - sp.Rational(PH_LOG[s])
    fmt = lambda p: f"{float(p):.2f}"  # noqa: E731
    if r.random() < 0.5:
        e = int(sp.floor(sp.log(c, 10)))
        mant = c / sp.Integer(10) ** e
        wrong_ph = -sp.log(c, 10)
        return err_item(f"濃度 {dec(c)} mol/L の1価の弱酸 HA の水溶液の pH を小数第2位まで求めなさい。電離定数は $K_{{\\mathrm{{a}}}}={sci(Ka)}$ mol/L とし、電離度は 1 に比べて十分小さいものとする。{LOGS}",
                        f"$[\\mathrm{{H^+}}]={dec(c)}$ mol/L なので pH＝{fmt(wrong_ph)}",
                        "$[\\mathrm{H^+}]$ を酸の濃度に等しいとした部分", "concept",
                        "化学基礎で学んだ強酸の計算（完全電離）をそのまま弱酸に当てはめ、電離定数を使っていない。",
                        f"$[\\mathrm{{H^+}}]=\\sqrt{{cK_{{\\mathrm{{a}}}}}}={sci(h)}$ mol/L より pH＝{fmt(pH)}", f"pH {fmt(pH)}",
                        "弱酸は一部しか電離しない。$[\\mathrm{H^+}]=c\\alpha\\fallingdotseq\\sqrt{cK_{\\mathrm{a}}}$ で求める。",
                        [f"$\\alpha=\\sqrt{{\\dfrac{{K_{{\\mathrm{{a}}}}}}{{c}}}}={sig(h / c)}$。", f"$[\\mathrm{{H^+}}]=c\\alpha={sci(h)}$ mol/L。", f"pH＝{fmt(pH)}。"],
                        "問題文に電離定数が与えられていたら、弱酸として電離平衡を考える合図である。",
                        ["電離度が 1 よりずっと小さいことから、$[\\mathrm{H^+}]$ が酸の濃度よりずっと小さくなることを確かめる。"], ["弱酸を完全電離として扱う。"],
                        chk=(f"sqrt({c}*{Ka})", str(h), None, "intermediate"), d=3)
    for _ in range(100):
        if sp.sqrt(Ka * 100 / c) <= sp.Rational(1, 10):
            break
        s, k, h, c, Ka = ph_pick(r)
    pH = k - sp.Rational(PH_LOG[s])
    c2 = c / 100
    h2 = sp.sqrt(c2 * Ka)
    pH2 = pH + 1
    return err_item(f"濃度 {dec(c)} mol/L の1価の弱酸 HA の水溶液の pH は {fmt(pH)} であった。この水溶液を水で 100 倍にうすめたときの pH を求めなさい。電離定数は $K_{{\\mathrm{{a}}}}={sci(Ka)}$ mol/L とし、うすめた後も電離度は 1 に比べて十分小さいものとする。",
                    f"10 倍うすめるごとに pH は 1 大きくなるので、pH＝{fmt(pH)}＋2＝{fmt(pH + 2)}",
                    "強酸の希釈の規則を当てはめた部分", "concept",
                    "強酸で成り立つ「10 倍うすめると pH が 1 大きくなる」という規則を、弱酸にも成り立つと考えている。",
                    f"$[\\mathrm{{H^+}}]=\\sqrt{{cK_{{\\mathrm{{a}}}}}}$ は $c$ が $\\dfrac{{1}}{{100}}$ になると $\\dfrac{{1}}{{10}}$ 倍になるので、pH は 1 だけ大きくなり {fmt(pH2)}", f"pH {fmt(pH2)}",
                    "弱酸ではうすめると電離度が大きくなるので、$[\\mathrm{H^+}]$ は $\\sqrt{c}$ に比例して減る。100 倍にうすめても $[\\mathrm{H^+}]$ は $\\dfrac{1}{10}$ 倍。",
                    [f"うすめた後 $c={sci(c2)}$ mol/L。", f"$[\\mathrm{{H^+}}]=\\sqrt{{{sci(c2)}\\times{sci(Ka)}}}={sci(h2)}$ mol/L。", f"pH＝{fmt(pH2)}。"],
                    "弱酸の希釈では電離度 $\\alpha=\\sqrt{K_{\\mathrm{a}}/c}$ も変わることを思い出す。",
                    [f"電離度が ${sig(h / c)}$ から ${sig(h2 / c2)}$ に大きくなることを計算して確かめる。"], ["強酸の希釈規則を弱酸に使う。"],
                    chk=(f"sqrt({c2}*{Ka})", str(h2), None, "intermediate"), d=3)


GENERATORS = [heat_amount, enthalpy_meaning, rate_basic, eq_constant, le_chatelier,
              hess, bond_energy, eq_calc, weak_acid, rate_data,
              buffer, energy_diagram, lc_explain, ksp,
              err_hess, err_equilibrium, err_weak_acid]
