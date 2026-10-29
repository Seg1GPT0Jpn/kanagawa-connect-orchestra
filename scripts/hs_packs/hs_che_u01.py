"""単元パック：化学 物質の状態（気体・溶液）（気体の法則・蒸気圧・希薄溶液の性質）。"""
import math
import re
from decimal import ROUND_HALF_UP, Decimal

import sympy as sp

from banks._common import desc, figure, mc, num, plane
from hs_pack_lib import board, check, definition, derivation, example, figure_explain, gen, guide, intro, lesson, summary, theorem, tp

UNIT_ID = "HS-CHE-U01"

RTXT = "気体定数を $R=8.3\\times10^{3}\\ \\mathrm{Pa\\cdot L/(K\\cdot mol)}$ とする。"
R_ = sp.Rational("8.3") * 1000
TIMES, FR5, FR45 = "\\times", "\\dfrac{1}{5}", "\\dfrac{4}{5}"
KB_W, KF_W, KF_B = sp.Rational("0.52"), sp.Rational("1.85"), sp.Rational("5.12")


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


def sigv(x, n=2):
    """sig と同じ丸めをした値（sympy の有理数）。"""
    s = sig(x, n)
    if "times" in s:
        a, e = re.match(r"(-?[\d.]+)\\times10\^\{(-?\d+)\}", s).groups()
        return sp.Rational(a) * sp.Integer(10) ** int(e)
    return sp.Rational(s)


def sci(x, n=2):
    """常に a×10^b の形で表す。"""
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


def err_item(stem, wrong, step, etype, tempt, fix, ans, expl, steps, ap, alt, pit, chk=None, d=3):
    return desc(f"{stem}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい答えを求めなさい。", ans, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい考え方・途中の式を示している", 3), ("最終的な答えが正しい", 1)], d=d, p=6, lines=6,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい考え方", 3), ("正しい答え", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix), chk=chk)


def pa(a, e):
    """(表示, 値) a×10^e Pa"""
    return f"{a}\\times10^{{{e}}}", sp.Rational(a) * sp.Integer(10) ** e


def kelvin(t):
    return t + 273


# 水の飽和蒸気圧（アントワン式による値を有効数字2桁に丸めて用いる）
def water_vp(t):
    p_mmhg = 10 ** (8.07131 - 1730.63 / (233.426 + t))
    return sigv(sp.Rational(round(p_mmhg * 101325 / 760)), 2)


def antoine_kpa(A, B, C):
    return lambda t: 10 ** (A - B / (C + t)) * 101.325 / 760


# ----------------------------------------------------------------------
# 図
# ----------------------------------------------------------------------

def vp_fig():
    ether = antoine_kpa(6.92032, 1064.07, 228.8)
    etoh = antoine_kpa(8.20417, 1642.89, 230.3)
    water = antoine_kpa(8.07131, 1730.63, 233.426)
    svg = plane(xr=(0, 10.5), yr=(-0.8, 11.5), unit=24, grid=False, ticks=False,
                curves=[(lambda x: ether(10 * x) / 10, ""), (lambda x: etoh(10 * x) / 10, ""), (lambda x: water(10 * x) / 10, "")],
                segments=[((0, 10.13), (10.4, 10.13))],
                labels=[(0.4, 10.5, "1.013×10⁵ Pa"), (1.2, 7.2, "ジエチルエーテル"), (5.0, 4.6, "エタノール"), (8.2, 2.6, "水")]
                + [(x - 0.25, -0.6, f"{10 * x}") for x in range(2, 11, 2)],
                xl="t[℃]", yl="p[×10⁴Pa]")
    return figure("ジエチルエーテル・エタノール・水の蒸気圧曲線（概形）。横軸は温度 t（℃、0〜100）、縦軸は飽和蒸気圧（×10⁴ Pa）。水平線は大気圧 1.013×10⁵ Pa。各曲線が水平線と交わる温度が沸点（約 34 ℃、約 78 ℃、100 ℃）。",
                  svg=svg, caption="蒸気圧曲線と沸点（概形）")


def cooling_fig():
    def f(x):
        if x <= 4.0:
            return 9.0 - 1.4 * x
        if x <= 4.4:
            return 3.4 + (x - 4.0) / 0.4 * 2.2
        return 5.6 - 0.28 * (x - 4.4)
    ax = (9.0 - 5.6 - 0.28 * 4.4) / (1.4 - 0.28)
    ay = 9.0 - 1.4 * ax
    svg = plane(xr=(0, 11), yr=(0, 10), unit=20, grid=False, ticks=False, curves=[(f, "")],
                segments=[((ax, ay), (4.4, 5.6))],
                points=[(4.0, 3.4, "B"), (4.4, 5.6, "C"), (ax, ay, "A"), (10.5, 5.6 - 0.28 * 6.1, "D")],
                labels=[(5.0, 7.0, "（Cから先は溶媒だけが凝固）")], xl="時間", yl="温度")
    return figure("溶液の冷却曲線（概形）。温度が下がり続けて点Bで最低になり（過冷却）、凝固が始まると点Cまで上がる。その後はゆるやかに下がり続ける（点D）。C以降の直線を左へ延長した線と、はじめの冷却の線との交点が点A。",
                  svg=svg, caption="溶液の冷却曲線（概形）")


# ======================================================================
# 授業プリント
# ======================================================================

LESSON = lesson(
    goals=["ボイルの法則・シャルルの法則から気体の状態方程式 $pV=nRT$ を導き、気体の圧力・体積・物質量・分子量を求められる。",
           "混合気体の分圧の法則と飽和蒸気圧の意味を説明し、液体が共存するかどうかを判断して容器内の圧力を求められる。",
           "希薄溶液の蒸気圧降下・沸点上昇・凝固点降下・浸透圧を粒子の数で説明し、質量モル濃度を用いて計算できる。"],
    duration=150,
    readiness=["物質量・モル質量・モル濃度の計算ができる（化学基礎「物質量と化学反応式」）。",
               "絶対温度 $T\\,[\\mathrm{K}]=t\\,[{}^\\circ\\mathrm{C}]+273$ と、圧力の単位 Pa（$1\\ \\mathrm{Pa}=1\\ \\mathrm{N/m^2}$）を知っている。",
               "反比例・比例の式の扱い、指数（$10^{5}$ など）の計算ができる。"],
    flow=[("導入：風船・圧力鍋・融雪剤", 8, "身近な現象を気体と溶液の性質として見直す"),
          ("気体の法則と状態方程式", 30, "ボイル・シャルルの法則、状態方程式の導出、分子量の決定"),
          ("混合気体と分圧", 17, "分圧の法則、モル分率、平均分子量、水上置換"),
          ("蒸気圧と状態変化", 25, "気液平衡、蒸気圧曲線と沸点、容器内で液体が残るかの判断"),
          ("希薄溶液の性質", 35, "質量モル濃度、蒸気圧降下・沸点上昇・凝固点降下、冷却曲線、浸透圧、ヘンリーの法則"),
          ("実在気体", 10, "理想気体からのずれとその原因"),
          ("演習とまとめ", 25, "例題の解説、確認問題、問題プリントの課題指示")],
    sections=[
        intro("in1", "目に見えない粒子の運動を「圧力」「温度」で読む",
              "気体の圧力は、たくさんの分子が容器の壁に衝突することで生じる。温度を上げれば分子の運動が激しくなり、体積を小さくすれば衝突の回数が増える。"
              "この単元では、圧力・体積・温度・物質量の関係を1つの式（状態方程式）にまとめ、さらに液体の蒸発（蒸気圧）や溶液の性質（沸点上昇・凝固点降下・浸透圧）を、粒子の数という共通の見方で説明する。",
              bullets=["気体の法則は「理想気体」についての法則。実在の気体は高圧・低温でずれる。",
                       "希薄溶液の沸点上昇・凝固点降下・浸透圧は、溶質の種類によらず溶質粒子の数（物質量）だけで決まる。"],
              points=[tp("ペットボトルを冷凍庫で冷やすとへこむ、圧力鍋では 100 ℃ 以上で煮える、冬の道路に融雪剤（塩化カルシウム）をまく、などの例を挙げ、この単元の3つの柱（気体・蒸気圧・溶液）に分類させる。",
                         ask="山の上でご飯を炊くと、芯が残りやすいのはなぜか。", expect="気圧が低いので水が 100 ℃ より低い温度で沸騰するから。",
                         timing="授業の冒頭")]),
        definition("df1", "ボイルの法則・シャルルの法則・状態方程式",
                   "一定量の気体の体積 $V$ は、温度一定のとき圧力 $p$ に反比例し（ボイルの法則）、圧力一定のとき絶対温度 $T$ に比例する（シャルルの法則）。"
                   "これらをまとめると $\\dfrac{pV}{T}$ が一定になる（ボイル・シャルルの法則）。さらに物質量 $n$ を含めた式が気体の状態方程式である。",
                   formula="$$pV=nRT,\\qquad R=8.3\\times10^{3}\\ \\mathrm{Pa\\cdot L/(K\\cdot mol)}\\qquad\\left(T\\,[\\mathrm{K}]=t\\,[{}^\\circ\\mathrm{C}]+273\\right)$$",
                   conditions=["温度は必ず絶対温度（K）で代入する。セルシウス温度のまま使うと誤り。",
                               "$R$ の単位に合わせて、圧力は Pa、体積は L で代入する（mL は L に直す）。",
                               "分子量の決定：$n=\\dfrac{w}{M}$ を代入して $M=\\dfrac{wRT}{pV}$。気体の密度 $d=\\dfrac{w}{V}$ を使えば $M=\\dfrac{dRT}{p}$。"],
                   points=[tp("$R$ の値は「標準状態で 1 mol が 22.4 L」から $R=\\dfrac{1.013\\times10^5\\times22.4}{1\\times273}\\fallingdotseq8.31\\times10^{3}$ と求まることを、その場で計算させる。",
                              ask="0 ℃ を絶対温度で表すと何 K か。", expect="273 K", caution="−273 ℃ が 0 K。セルシウス温度の 0 ℃ を代入すると分母が 0 になる。")]),
        derivation("dv1", "状態方程式 $pV=nRT$ の導出",
                   ["ボイルの法則（$T$ 一定）：$pV=$ 一定。シャルルの法則（$p$ 一定）：$\\dfrac{V}{T}=$ 一定。",
                    "状態 $(p_1,V_1,T_1)$ から、温度を保って圧力を $p_2$ にすると体積は $V'=\\dfrac{p_1V_1}{p_2}$。",
                    "次に圧力を保って温度を $T_2$ にすると $V_2=V'\\times\\dfrac{T_2}{T_1}=\\dfrac{p_1V_1T_2}{p_2T_1}$。よって $\\dfrac{p_1V_1}{T_1}=\\dfrac{p_2V_2}{T_2}$（ボイル・シャルルの法則）。",
                    "同温・同圧で気体の体積は物質量に比例する（アボガドロの法則）ので、$\\dfrac{pV}{T}$ は $n$ に比例する：$\\dfrac{pV}{T}=nR$。",
                    "比例定数 $R$ は、標準状態（$1.013\\times10^5$ Pa、273 K）で 1 mol が 22.4 L を占めることから $R\\fallingdotseq8.3\\times10^{3}\\ \\mathrm{Pa\\cdot L/(K\\cdot mol)}$。"],
                   body="2段階の変化に分けて考えることで、2つの法則が1つの式にまとまる。状態方程式はどんな種類の（理想）気体にも同じ $R$ で成り立つ。",
                   points=[tp("「温度一定の変化」と「圧力一定の変化」の2段階に分ける図（$p$–$V$ の矢印）を板書し、途中の状態 $V'$ を必ず書かせる。", timing="導出の2段目")]),
        theorem("th1", "分圧の法則（ドルトンの法則）",
                "$$p_{\\text{全}}=p_{\\mathrm{A}}+p_{\\mathrm{B}}+\\cdots,\\qquad p_{\\mathrm{A}}=p_{\\text{全}}\\times\\dfrac{n_{\\mathrm{A}}}{n_{\\text{全}}}\\ (\\text{モル分率})$$",
                ["分圧とは、混合気体の成分が単独で全体積を占めたときに示す圧力である。",
                 "同温・同体積では、分圧の比＝物質量の比。同温・同圧では、体積の比＝物質量の比。",
                 "平均分子量：$\\overline{M}=M_{\\mathrm{A}}\\times\\dfrac{n_{\\mathrm{A}}}{n_{\\text{全}}}+M_{\\mathrm{B}}\\times\\dfrac{n_{\\mathrm{B}}}{n_{\\text{全}}}$（空気 $\\mathrm{N_2}:\\mathrm{O_2}=4:1$ なら約 28.8）。"],
                proof=["成分 A, B それぞれに状態方程式を立てる：$p_{\\mathrm{A}}V=n_{\\mathrm{A}}RT$、$p_{\\mathrm{B}}V=n_{\\mathrm{B}}RT$（同じ $V$ と $T$）。",
                       "混合気体全体についても $p_{\\text{全}}V=(n_{\\mathrm{A}}+n_{\\mathrm{B}})RT$ が成り立つ（理想気体の分子どうしは互いに影響しない）。",
                       "辺々を比べて $p_{\\text{全}}=p_{\\mathrm{A}}+p_{\\mathrm{B}}$。また $\\dfrac{p_{\\mathrm{A}}}{p_{\\text{全}}}=\\dfrac{n_{\\mathrm{A}}}{n_{\\mathrm{A}}+n_{\\mathrm{B}}}$。"],
                points=[tp("水上置換で集めた気体の圧力は「大気圧＝目的の気体の分圧＋水蒸気圧」であることを、分圧の法則の応用として扱う。",
                           ask="水上置換で集めた水素の分圧を求めるには、大気圧から何を引けばよいか。", expect="その温度の水の飽和蒸気圧。")]),
        definition("df2", "飽和蒸気圧と沸騰",
                   "密閉容器に液体を入れておくと、蒸発する分子の数と凝縮する分子の数が等しくなり、見かけ上蒸発が止まった状態（気液平衡）になる。このときの蒸気の圧力を飽和蒸気圧（蒸気圧）という。",
                   formula="$$\\text{容器内の蒸気の圧力}\\leqq\\text{その温度の飽和蒸気圧}\\qquad(\\text{等号のとき液体が共存できる})$$",
                   conditions=["飽和蒸気圧は温度だけで決まり、容器の体積・液体の量・他の気体の有無には関係しない。",
                               "飽和蒸気圧が外圧に等しくなる温度で沸騰が起こる。外圧が低いほど沸点は低い。",
                               "容器内の物質がすべて気体だと仮定して求めた圧力が飽和蒸気圧を上回るときは、一部が凝縮し、蒸気の圧力は飽和蒸気圧に等しくなる。"],
                   points=[tp("「すべて気体と仮定 → 飽和蒸気圧と比較 → 大きければ飽和蒸気圧に置き換える」という3段階の判断を、毎回書かせる。",
                              caution="飽和蒸気圧を「容器を小さくすれば上がる」と誤解しやすい。圧縮すると凝縮が進むだけで、蒸気の圧力は変わらない。")]),
        figure_explain("fg1", "蒸気圧曲線と沸点", vp_fig(),
                       "分子間力の小さい液体ほど蒸発しやすく、同じ温度での飽和蒸気圧が大きい。そのため、ジエチルエーテル・エタノール・水の順に、大気圧と等しくなる温度（沸点）が高くなる。"
                       "水の曲線上で、ある温度における飽和蒸気圧を読み取れば、その温度で水が共存しているときの水蒸気の分圧が分かる。",
                       points=[tp("グラフで「縦に読む（温度 → 蒸気圧）」と「横に読む（外圧 → 沸点）」の2通りの読み方を練習させる。",
                                  ask="外圧が $5\\times10^4$ Pa のとき、水は何 ℃ くらいで沸騰するか。", expect="約 80 ℃（曲線が $5\\times10^4$ Pa になる温度）。")]),
        definition("df3", "希薄溶液の性質",
                   "不揮発性の物質を溶かした溶液は、純溶媒より蒸気圧が低い（蒸気圧降下）。そのため沸点が高くなり（沸点上昇）、凝固点が低くなる（凝固点降下）。"
                   "これらの変化の大きさは、溶媒 1 kg あたりに溶けている溶質粒子の物質量（質量モル濃度）に比例する。",
                   formula="$$\\Delta t_{\\mathrm{b}}=K_{\\mathrm{b}}m,\\qquad \\Delta t_{\\mathrm{f}}=K_{\\mathrm{f}}m,\\qquad \\Pi V=nRT\\ (\\Pi=cRT)$$",
                   conditions=["質量モル濃度 $m\\,[\\mathrm{mol/kg}]=\\dfrac{\\text{溶質の物質量}}{\\text{溶媒の質量}\\,[\\mathrm{kg}]}$。分母は溶液ではなく溶媒の質量。",
                               "電解質は電離して粒子の数が増える。NaCl は $\\mathrm{Na^+}$ と $\\mathrm{Cl^-}$ で2倍、$\\mathrm{CaCl_2}$ は3倍の粒子数として計算する（完全に電離する場合）。",
                               "水：$K_{\\mathrm{b}}=0.52\\ \\mathrm{K\\cdot kg/mol}$、$K_{\\mathrm{f}}=1.85\\ \\mathrm{K\\cdot kg/mol}$。ベンゼン：$K_{\\mathrm{f}}=5.12\\ \\mathrm{K\\cdot kg/mol}$（凝固点 5.5 ℃）。",
                               "浸透圧 $\\Pi$ はモル濃度 $c$（mol/L）と絶対温度に比例する（ファントホッフの法則）。高分子の分子量の測定に向く。",
                               "ヘンリーの法則：溶解度の小さい気体では、一定温度で一定量の溶媒に溶ける気体の物質量（質量）はその気体の分圧に比例する。"],
                   points=[tp("「溶質の種類によらず粒子の数で決まる」性質であることを、ブドウ糖・尿素・食塩の比較で確認させる。",
                              ask="0.1 mol/kg のブドウ糖水溶液と 0.1 mol/kg の食塩水では、どちらの凝固点が低いか。", expect="食塩水（粒子の数が約2倍）。")]),
        example("ex1", "例題1　状態方程式と分子量",
                "ある気体 1.6 g を 27 ℃ で 0.83 L の容器に入れたところ、圧力が $3.0\\times10^{5}$ Pa になった。この気体の分子量を求めよ。$R=8.3\\times10^{3}\\ \\mathrm{Pa\\cdot L/(K\\cdot mol)}$ とする。",
                ["$T=27+273=300$ K。", "$M=\\dfrac{wRT}{pV}=\\dfrac{1.6\\times8.3\\times10^{3}\\times300}{3.0\\times10^{5}\\times0.83}$。", "$=16$。"],
                "16（例えばメタン $\\mathrm{CH_4}$）", thinking="$pV=\\dfrac{w}{M}RT$ を $M$ について解く。温度は絶対温度に直す。",
                misconceptions=[("$T=27$ を代入して $M\\fallingdotseq1.4$", "絶対温度 300 K を代入する")],
                points=[tp("答えが 16 になったら、どんな気体か（$\\mathrm{CH_4}$ など）を言わせ、計算結果の妥当性を確かめる習慣をつける。")]),
        example("ex2", "例題2　液体が残るかどうかの判断",
                "容積 8.3 L の真空容器に水 0.10 mol を入れ、27 ℃ に保った。容器内の圧力を求めよ。27 ℃ の水の飽和蒸気圧は $3.6\\times10^{3}$ Pa、$R=8.3\\times10^{3}\\ \\mathrm{Pa\\cdot L/(K\\cdot mol)}$ とする。",
                ["すべて水蒸気だと仮定すると $p=\\dfrac{0.10\\times8.3\\times10^{3}\\times300}{8.3}=3.0\\times10^{4}$ Pa。",
                 "これは飽和蒸気圧 $3.6\\times10^{3}$ Pa より大きいので、実際には一部が液体として残る。",
                 "液体が共存しているので、容器内の圧力は飽和蒸気圧に等しい。"],
                "$3.6\\times10^{3}$ Pa（液体の水が残る）", thinking="すべて気体と仮定 → 飽和蒸気圧と比較 → 判断。",
                misconceptions=[("$3.0\\times10^{4}$ Pa", "飽和蒸気圧をこえる圧力の水蒸気は存在できない。液体が共存し $3.6\\times10^{3}$ Pa")]),
        example("ex3", "例題3　凝固点降下と分子量",
                "ある非電解質 3.6 g を水 200 g に溶かした溶液の凝固点は $-0.185$ ℃ であった。この物質の分子量を求めよ。水のモル凝固点降下は 1.85 K·kg/mol とする。",
                ["$\\Delta t_{\\mathrm{f}}=0.185$ K より $m=\\dfrac{0.185}{1.85}=0.100$ mol/kg。", "溶質の物質量：$0.100\\times0.200=0.0200$ mol。", "$M=\\dfrac{3.6}{0.0200}=180$。"],
                "180", thinking="凝固点降下度 → 質量モル濃度 → 溶質の物質量 → 分子量の順に求める。",
                points=[tp("溶媒の質量を kg に直すこと、凝固点（−0.185 ℃）と凝固点降下度（0.185 K）を区別することを確認する。")]),
        figure_explain("fg2", "溶液の冷却曲線", cooling_fig(),
                       "溶液を冷やすと、凝固点より低くなってもすぐには凝固しない（過冷却、点B）。凝固が始まると凝固熱で温度が上がる（点C）。純溶媒なら凝固中は温度が一定だが、溶液では溶媒だけが凝固して溶液が濃くなるので、温度はゆるやかに下がり続ける。"
                       "このため溶液の凝固点は、C以降の直線を延長してはじめの冷却の線と交わる点Aの温度として読み取る。",
                       points=[tp("純溶媒と溶液の冷却曲線を並べてかき、凝固が始まった後の傾きのちがいを「溶液の濃縮」で説明させる。",
                                  ask="凝固が進むと、残った溶液の質量モル濃度はどうなるか。", expect="溶媒だけが固体になるので大きくなり、凝固点がさらに下がる。")]),
        board("bd1", "板書案",
              [("① 気体", ["$pV=nRT$（$T$ は K、$V$ は L）", "$R=8.3\\times10^3$ Pa·L/(K·mol)", "$M=\\dfrac{wRT}{pV}$", "分圧＝全圧×モル分率",
                          "水上置換：大気圧−水蒸気圧"]),
               ("② 蒸気圧", ["飽和蒸気圧は温度だけで決まる", "蒸気圧＝外圧 → 沸騰", "すべて気体と仮定して $p$ を計算", "$p>$ 飽和蒸気圧 → 液体が残る",
                            "→ 蒸気の圧力＝飽和蒸気圧"]),
               ("③ 希薄溶液", ["$m$＝溶質 mol ÷ 溶媒 kg", "$\\Delta t_{\\mathrm{b}}=K_{\\mathrm{b}}m$、$\\Delta t_{\\mathrm{f}}=K_{\\mathrm{f}}m$", "電解質は粒子数（NaCl ×2）",
                              "$\\Pi=cRT$（高分子の分子量）", "冷却曲線：延長線で凝固点"])]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("状態方程式に代入する前に、$p$（Pa）、$V$（L）、$T$（K）の単位をそろえる欄を答案に作らせる。",
                  caution="mL のまま代入する誤りと、セルシウス温度を代入する誤りが最も多い。"),
               tp("実在気体は、分子自身の体積と分子間力のために理想気体からずれる。高温・低圧ほど理想気体に近いことを、$\\dfrac{pV}{nRT}$ のグラフの概形で示す。",
                  ask="アンモニアと水素では、低温で理想気体からのずれが大きいのはどちらか。", expect="アンモニア（分子間力が大きい）。"),
               tp("ヘンリーの法則は「溶ける物質量が分圧に比例」。溶けた気体の体積を、そのときの圧力のもとで測ると圧力によらず一定になることも合わせて説明する。", timing="希薄溶液の終わり"),
               tp("沸点上昇・凝固点降下の計算では、溶質が電解質かどうかを最初に確認させる。")],
              misconceptions=[("飽和蒸気圧は、容器を圧縮すると大きくなる", "飽和蒸気圧は温度だけで決まる。圧縮すると凝縮が進み、蒸気の圧力は変わらない"),
                              ("質量モル濃度は溶液 1 kg あたりの溶質の物質量", "溶媒 1 kg あたり"),
                              ("どんな溶質でも同じ質量を溶かせば凝固点は同じだけ下がる", "粒子の物質量で決まるので、分子量や電離のしかたで変わる")]),
        summary("sm1", "まとめ", ["理想気体では $pV=nRT$。温度は K、体積は L、圧力は Pa で代入する。混合気体では分圧＝全圧×モル分率。",
                                   "飽和蒸気圧は温度だけで決まり、外圧と等しくなる温度で沸騰する。容器内で液体が残るかは「すべて気体と仮定した圧力」と飽和蒸気圧の比較で判断する。",
                                   "希薄溶液の沸点上昇・凝固点降下は質量モル濃度に、浸透圧はモル濃度と絶対温度に比例する。電解質は電離後の粒子数で考える。"]),
        check("ck1", "確認問題", [("27 ℃ は何 K か。", "300 K"),
                                  ("$\\mathrm{N_2}$ 0.40 mol と $\\mathrm{O_2}$ 0.10 mol の混合気体の全圧が $1.0\\times10^5$ Pa のとき、$\\mathrm{O_2}$ の分圧は？", "$2.0\\times10^4$ Pa"),
                                  ("外圧を下げると、水の沸点はどうなるか。", "低くなる"),
                                  ("0.10 mol/kg の塩化ナトリウム水溶液の凝固点降下度は？（$K_{\\mathrm{f}}=1.85$、完全電離）", "0.37 K")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

TEMPS = [0, 27, 47, 77, 127, 227, -73, 87, 57]


@gen("basic_check", 4, ["computation", "condition_check"])
def boyle_charles(r):
    form = r.choice(["boyle", "charles", "combined"])
    if form == "boyle":
        a1, e1 = r.choice([("1.0", 5), ("2.0", 5), ("3.0", 5), ("1.5", 5), ("6.0", 4), ("8.0", 4)])
        p1s, p1 = pa(a1, e1)
        V1 = sp.Rational(r.choice(["2.0", "3.0", "4.0", "6.0", "1.5", "5.0"]))
        V2 = sp.Rational(r.choice(["1.0", "2.5", "8.0", "10", "12", "0.50"]))
        if V2 == V1:
            V2 = V1 * 2
        p2 = p1 * V1 / V2
        return numq(f"温度を一定に保ったまま、${p1s}$ Pa で {dec(V1)} L を占める気体の体積を {dec(V2)} L にした。圧力は何 Pa になるか。", p2,
                    f"{p1}*{V1}/({V2})", f"ボイルの法則 $p_1V_1=p_2V_2$ より $p_2=\\dfrac{{{p1s}\\times{dec(V1)}}}{{{dec(V2)}}}$。", unit="Pa", d=1,
                    ap="温度一定なので、圧力と体積は反比例する（$pV=$ 一定）。",
                    steps=[f"$p_1V_1=p_2V_2$ に代入：${p1s}\\times{dec(V1)}=p_2\\times{dec(V2)}$。", f"$p_2={sig(p2)}$ Pa。"],
                    alt=[f"体積が $\\dfrac{{{dec(V2)}}}{{{dec(V1)}}}$ 倍になったので、圧力はその逆数倍になる、と考えて確かめる。"],
                    pc=[("ボイルの法則の式を立てている", 1), ("値が正しい", 1)], pit=["比例と反比例を取り違えて、圧力を体積と同じ倍率で変える。"])
    if form == "charles":
        t1, t2 = r.sample([0, 27, 77, 127, 227, -73, 327, 47], 2)
        T1, T2 = kelvin(t1), kelvin(t2)
        V1 = sp.Rational(r.choice(["2.0", "3.0", "4.0", "6.0", "1.2", "5.0", "8.0"]))
        V2 = V1 * T2 / T1
        return numq(f"圧力を一定に保ったまま、{t1} ℃ で {dec(V1)} L の気体を {t2} ℃ にした。体積は何 L になるか。", V2, f"{V1}*({t2}+273)/({t1}+273)",
                    f"シャルルの法則 $\\dfrac{{V_1}}{{T_1}}=\\dfrac{{V_2}}{{T_2}}$ より、$V_2={dec(V1)}\\times\\dfrac{{{T2}}}{{{T1}}}$。", unit="L", d=1,
                    ap="圧力一定なので、体積は絶対温度に比例する。温度は K に直してから比をとる。",
                    steps=[f"$T_1={t1}+273={T1}$ K、$T_2={t2}+273={T2}$ K。", f"$V_2={dec(V1)}\\times\\dfrac{{{T2}}}{{{T1}}}={sig(V2)}$ L。"],
                    alt=["状態方程式 $pV=nRT$ で $p,\\ n$ が一定なので $V\\propto T$、と考えても同じ。"],
                    pc=[("絶対温度に直している", 1), ("値が正しい", 1)], pit=["セルシウス温度の比で計算する。"])
    a1, e1 = r.choice([("1.0", 5), ("2.0", 5), ("1.5", 5), ("3.0", 5)])
    p1s, p1 = pa(a1, e1)
    a2, e2 = r.choice([("1.0", 5), ("2.0", 5), ("5.0", 5), ("4.0", 5), ("5.0", 4)])
    p2s, p2 = pa(a2, e2)
    t1, t2 = r.sample([27, 127, 77, 227, 0, 47], 2)
    V1 = sp.Rational(r.choice(["2.0", "3.0", "4.0", "6.0", "10"]))
    V2 = p1 * V1 * kelvin(t2) / (kelvin(t1) * p2)
    return numq(f"{t1} ℃、${p1s}$ Pa で {dec(V1)} L を占める気体を、{t2} ℃、${p2s}$ Pa にすると、体積は何 L になるか。", V2,
                f"{p1}*{V1}*({t2}+273)/(({t1}+273)*{p2})", f"$\\dfrac{{p_1V_1}}{{T_1}}=\\dfrac{{p_2V_2}}{{T_2}}$ より $V_2=\\dfrac{{p_1V_1T_2}}{{p_2T_1}}$。", unit="L", d=2,
                ap="物質量が一定なので、ボイル・シャルルの法則 $\\dfrac{pV}{T}=$ 一定 を使う。",
                steps=[f"$T_1={kelvin(t1)}$ K、$T_2={kelvin(t2)}$ K。", f"$V_2=\\dfrac{{{p1s}\\times{dec(V1)}\\times{kelvin(t2)}}}{{{p2s}\\times{kelvin(t1)}}}={sig(V2)}$ L。"],
                alt=["圧力の変化による倍率と、温度の変化による倍率を別々に求めてかけ合わせる（2段階の変化）。"],
                pc=[("ボイル・シャルルの法則の式を立てている", 1), ("値が正しい", 1)], pit=["温度を K に直し忘れる。", "圧力の比を逆にかける。"])


@gen("basic_check", 5, ["computation", "condition_check"])
def ideal_gas(r):
    form = r.choice(["n", "p", "V", "M"])
    t = r.choice(TEMPS)
    T = kelvin(t)
    if form == "n":
        ps, p = pa(*r.choice([("1.0", 5), ("2.0", 5), ("1.5", 5), ("3.0", 5), ("8.3", 4), ("5.0", 4)]))
        V = sp.Rational(r.choice(["1.0", "2.0", "5.0", "8.3", "10", "4.0", "3.0"]))
        n = p * V / (R_ * T)
        return numq(f"{t} ℃、${ps}$ Pa で {dec(V)} L を占める気体の物質量は何 mol か。{RTXT}", n, f"{p}*{V}/(8.3*10**3*({t}+273))",
                    f"$n=\\dfrac{{pV}}{{RT}}=\\dfrac{{{ps}\\times{dec(V)}}}{{8.3\\times10^{{3}}\\times{T}}}$。", unit="mol", d=1,
                    ap="状態方程式 $pV=nRT$ を $n$ について解く。温度は絶対温度に直す。",
                    steps=[f"$T={t}+273={T}$ K。", f"$n=\\dfrac{{{ps}\\times{dec(V)}}}{{8.3\\times10^{{3}}\\times{T}}}={sig(n)}$ mol。"],
                    alt=["単位で確かめる：$\\dfrac{\\mathrm{Pa\\cdot L}}{\\mathrm{Pa\\cdot L/(K\\cdot mol)}\\times\\mathrm{K}}=\\mathrm{mol}$。"],
                    pc=[("状態方程式に正しく代入している", 1), ("値が正しい", 1)], pit=["セルシウス温度のまま代入する。"])
    if form == "p":
        n = sp.Rational(r.choice(["0.10", "0.20", "0.50", "1.0", "0.25", "0.040", "2.0"]))
        V = sp.Rational(r.choice(["1.0", "2.0", "5.0", "8.3", "10", "4.0", "20"]))
        p = n * R_ * T / V
        return numq(f"{dec(n)} mol の気体を {dec(V)} L の容器に入れ、{t} ℃ に保った。容器内の圧力は何 Pa か。{RTXT}", p, f"{n}*8.3*10**3*({t}+273)/({V})",
                    f"$p=\\dfrac{{nRT}}{{V}}=\\dfrac{{{dec(n)}\\times8.3\\times10^{{3}}\\times{T}}}{{{dec(V)}}}$。", unit="Pa", d=1,
                    ap="状態方程式を $p$ について解く：$p=\\dfrac{nRT}{V}$。",
                    steps=[f"$T={T}$ K。", f"$p=\\dfrac{{{dec(n)}\\times8.3\\times10^{{3}}\\times{T}}}{{{dec(V)}}}={sig(p)}$ Pa。"],
                    alt=["標準状態（273 K、$1.013\\times10^5$ Pa）で 1 mol が 22.4 L であることと比べ、桁が妥当か確かめる。"],
                    pc=[("状態方程式に正しく代入している", 1), ("値が正しい", 1)], pit=["指数の計算で桁を誤る。"])
    if form == "V":
        n = sp.Rational(r.choice(["0.10", "0.20", "0.50", "1.0", "0.25", "0.30", "2.0"]))
        ps, p = pa(*r.choice([("1.0", 5), ("2.0", 5), ("8.3", 4), ("4.0", 5), ("5.0", 5)]))
        V = n * R_ * T / p
        return numq(f"{dec(n)} mol の気体は、{t} ℃、${ps}$ Pa で何 L を占めるか。{RTXT}", V, f"{n}*8.3*10**3*({t}+273)/({p})",
                    f"$V=\\dfrac{{nRT}}{{p}}$。", unit="L", d=1,
                    ap="状態方程式を $V$ について解く。$R$ の単位から、体積は L で求まる。",
                    steps=[f"$T={T}$ K。", f"$V=\\dfrac{{{dec(n)}\\times8.3\\times10^{{3}}\\times{T}}}{{{ps}}}={sig(V)}$ L。"],
                    alt=["圧力が大きいほど、温度が低いほど体積は小さくなることから、答えの大小を確かめる。"],
                    pc=[("状態方程式に正しく代入している", 1), ("値が正しい", 1)], pit=["体積を m³ や mL と取り違える。"])
    name, f, Mf = r.choice([("メタン", "CH4", 16), ("酸素", "O2", 32), ("窒素", "N2", 28), ("二酸化炭素", "CO2", 44), ("アルゴン", "Ar", 40), ("プロパン", "C3H8", 44),
                            ("アンモニア", "NH3", 17), ("ネオン", "Ne", 20)])
    n = sp.Rational(r.choice(["0.10", "0.20", "0.050", "0.25", "0.40"]))
    w = n * Mf
    V = sp.Rational(r.choice(["1.0", "2.0", "0.83", "4.15", "8.3", "5.0"]))
    p = sigv(n * R_ * T / V, 2)
    M = w * R_ * T / (p * V)
    return numq(f"ある気体 {dec(w)} g を {dec(V)} L の容器に入れて {t} ℃ に保つと、圧力は ${sci(p)}$ Pa であった。この気体の分子量を求めなさい。{RTXT}", M,
                f"{w}*8.3*10**3*({t}+273)/({p}*{V})", f"$M=\\dfrac{{wRT}}{{pV}}$ に代入する。", d=2,
                ap="$pV=\\dfrac{w}{M}RT$ を分子量 $M$ について解く。",
                steps=[f"$T={T}$ K。", f"$M=\\dfrac{{{dec(w)}\\times8.3\\times10^{{3}}\\times{T}}}{{{sci(p)}\\times{dec(V)}}}\\fallingdotseq{sig(M)}$。"],
                alt=[f"先に物質量 $n=\\dfrac{{pV}}{{RT}}$ を求め、$M=\\dfrac{{w}}{{n}}$ としてもよい。分子量 {Mf} の気体として、たとえば{name}が考えられる。"],
                pc=[("式を正しく立てている", 1), ("値が正しい", 1)], pit=["$w$ と $n$ を取り違え、質量をそのまま物質量として代入する。"])


@gen("basic_check", 4, ["computation", "concept"])
def partial_pressure(r):
    form = r.choice(["frac", "total", "avg"])
    gases = [("窒素", "N2", 28), ("酸素", "O2", 32), ("水素", "H2", 2), ("アルゴン", "Ar", 40), ("二酸化炭素", "CO2", 44), ("ヘリウム", "He", 4), ("メタン", "CH4", 16)]
    (na, fa, Ma), (nb, fb, Mb) = r.sample(gases, 2)
    a = sp.Rational(r.choice(["0.10", "0.20", "0.30", "0.40", "0.60", "0.80", "1.0"]))
    b = sp.Rational(r.choice(["0.10", "0.20", "0.30", "0.40", "0.050", "0.50"]))
    if form == "frac":
        ps, p = pa(*r.choice([("1.0", 5), ("2.0", 5), ("1.5", 5), ("3.0", 5), ("6.0", 5)]))
        pb = p * b / (a + b)
        return numq(f"{na} ${tex(fa)}$ {dec(a)} mol と{nb} ${tex(fb)}$ {dec(b)} mol からなる混合気体の全圧が ${ps}$ Pa であるとき、{nb}の分圧は何 Pa か。", pb,
                    f"{p}*{b}/({a}+{b})", f"モル分率 $\\dfrac{{{dec(b)}}}{{{dec(a + b)}}}$ を全圧にかける。", unit="Pa", d=1,
                    ap="分圧＝全圧×モル分率。モル分率はその成分の物質量÷全物質量。",
                    steps=[f"{nb}のモル分率：$\\dfrac{{{dec(b)}}}{{{dec(a)}+{dec(b)}}}=\\dfrac{{{dec(b)}}}{{{dec(a + b)}}}$。", f"分圧：${ps}\\times\\dfrac{{{dec(b)}}}{{{dec(a + b)}}}={sig(pb)}$ Pa。"],
                    alt=["もう一方の成分の分圧も求め、2つの分圧の和が全圧になることを確かめる。"],
                    pc=[("モル分率を求めている", 1), ("値が正しい", 1)], pit=["物質量の比ではなく質量の比で分ける。"])
    if form == "total":
        t = r.choice([27, 127, 77, 0, 227])
        V = sp.Rational(r.choice(["8.3", "10", "5.0", "4.15", "2.0", "16.6"]))
        p = (a + b) * R_ * kelvin(t) / V
        return numq(f"容積 {dec(V)} L の容器に{na} {dec(a)} mol と{nb} {dec(b)} mol を入れ、{t} ℃ に保った。容器内の全圧は何 Pa か。{RTXT}", p,
                    f"({a}+{b})*8.3*10**3*({t}+273)/({V})", f"全物質量 {dec(a + b)} mol を状態方程式に代入する。", unit="Pa", d=2,
                    ap="混合気体全体にも状態方程式が成り立つ。全物質量を使えば全圧が求まる（各分圧の和でもよい）。",
                    steps=[f"全物質量：${dec(a)}+{dec(b)}={dec(a + b)}$ mol。", f"$p=\\dfrac{{{dec(a + b)}\\times8.3\\times10^{{3}}\\times{kelvin(t)}}}{{{dec(V)}}}={sig(p)}$ Pa。"],
                    alt=["成分ごとに分圧を求めて足しても同じ結果になる（分圧の法則）。"],
                    pc=[("全物質量を用いている", 1), ("値が正しい", 1)], pit=["一方の成分の物質量だけで計算する。"])
    Mavg = (a * Ma + b * Mb) / (a + b)
    return numq(f"{na} ${tex(fa)}$ と{nb} ${tex(fb)}$ を物質量の比 {dec(a)}：{dec(b)} で混合した気体の平均分子量を求めなさい。分子量は ${tex(fa)}={Ma}$、${tex(fb)}={Mb}$ とする。",
                Mavg, f"({a}*{Ma}+{b}*{Mb})/({a}+{b})", "各成分の分子量にモル分率をかけて足す。", d=2, n=3,
                ap="平均分子量は、混合気体 1 mol あたりの質量。分子量×モル分率の和で求める。",
                steps=[f"モル分率：{na} $\\dfrac{{{dec(a)}}}{{{dec(a + b)}}}$、{nb} $\\dfrac{{{dec(b)}}}{{{dec(a + b)}}}$。",
                       f"$\\overline{{M}}={Ma}\\times\\dfrac{{{dec(a)}}}{{{dec(a + b)}}}+{Mb}\\times\\dfrac{{{dec(b)}}}{{{dec(a + b)}}}={sig(Mavg, 3)}$。"],
                alt=[f"混合気体 {dec(a + b)} mol の全質量 ${dec(a)}\\times{Ma}+{dec(b)}\\times{Mb}={dec(a * Ma + b * Mb)}$ g を全物質量で割る。"],
                pc=[("モル分率を用いている", 1), ("値が正しい", 1)], pit=["2つの分子量を単純に平均する。"])


VP_TRUE = ["液体の飽和蒸気圧は、温度が高いほど大きい。",
           "液体の飽和蒸気圧が外圧と等しくなる温度で、沸騰が起こる。",
           "一定温度では、液体の飽和蒸気圧は容器の体積や液体の量に関係しない。",
           "外圧を低くすると、液体の沸点は低くなる。",
           "分子間力の大きい液体ほど、同じ温度での飽和蒸気圧は小さい。",
           "気液平衡の状態では、単位時間あたりに蒸発する分子の数と凝縮する分子の数が等しい。",
           "不揮発性の物質を溶かした溶液の蒸気圧は、同じ温度の純溶媒の蒸気圧より低い。"]
VP_FALSE = [("一定温度で容器の体積を小さくすると、液体の飽和蒸気圧は大きくなる。", "飽和蒸気圧は温度だけで決まる。体積を小さくすると蒸気の一部が凝縮するだけで、蒸気の圧力は変わらない。", "飽和蒸気圧が体積に依存するという誤解"),
            ("気液平衡の状態では、蒸発も凝縮も起こっていない。", "気液平衡は、蒸発と凝縮が同じ速さで起こり続けている動的な平衡である。", "平衡を「反応の停止」と考える誤解"),
            ("外圧を高くすると、液体の沸点は低くなる。", "外圧が高いほど、飽和蒸気圧がその外圧に達する温度は高くなるので、沸点は高くなる。", "外圧と沸点の関係の取り違え"),
            ("分子間力の大きい液体ほど、同じ温度での飽和蒸気圧は大きい。", "分子間力が大きいほど分子は液体から飛び出しにくく、飽和蒸気圧は小さい。", "分子間力と蒸発しやすさの関係の取り違え"),
            ("容器内の液体の量を2倍にすると、同じ温度での飽和蒸気圧も2倍になる。", "飽和蒸気圧は液体の量に関係しない。", "飽和蒸気圧が量に比例するという誤解"),
            ("沸騰しているとき、液体の飽和蒸気圧は外圧より大きい。", "沸騰は飽和蒸気圧が外圧に等しくなったときに起こり、沸騰中の温度は一定に保たれる。", "沸騰の条件の誤解"),
            ("不揮発性の物質を溶かすと、溶液の蒸気圧は純溶媒より高くなる。", "溶質粒子があると溶媒分子が蒸発しにくくなり、蒸気圧は低くなる（蒸気圧降下）。", "蒸気圧降下の向きの誤り")]


@gen("basic_check", 3, ["concept", "condition_check"])
def vapor_concept(r):
    if r.random() < 0.5:
        right = r.choice(VP_TRUE)
        wrong = r.sample(VP_FALSE, 3)
        why = {w: (reason, mis) for w, reason, mis in wrong}
        return mc("蒸気圧と沸騰について述べた次の文のうち、正しいものを1つ選びなさい。", [right] + [w for w, _, _ in wrong],
                  f"正しいのは「{right}」。", d=2,
                  ap="飽和蒸気圧は「温度だけで決まる」「外圧と等しくなると沸騰」の2点を軸に、各文を判定する。",
                  steps=["各文が、温度以外の条件（体積・量）で飽和蒸気圧が変わると述べていないか確認する。", "沸点と外圧、分子間力と蒸気圧の向きを確認する。", "正しい文を選ぶ。"],
                  alt=["蒸気圧曲線のグラフをかいて、外圧の水平線との交点（沸点）がどう動くかで確かめる。"],
                  pc=[("飽和蒸気圧の性質を理解している", 1), ("正しく選んでいる", 1)], why=why,
                  pit=["気液平衡を「何も起こっていない状態」と考える。"])
    w, reason, mis = r.choice(VP_FALSE)
    rights = r.sample(VP_TRUE, 3)
    why = {x: ("この文は正しい。" + ("飽和蒸気圧は温度だけで決まる性質である。" if "関係しない" in x else "蒸気圧と沸騰の基本的な性質に合っている。"), "正しい記述を誤りと判断している") for x in rights}
    return mc("蒸気圧と沸騰について述べた次の文のうち、誤っているものを1つ選びなさい。", [w] + rights,
              f"誤っているのは「{w}」。{reason}", d=2,
              ap="飽和蒸気圧は温度だけで決まり、外圧と等しくなる温度で沸騰する。この原則に反する文を探す。",
              steps=["各文の主張を、飽和蒸気圧の定義と照らし合わせる。", f"「{w}」は原則に反する。", reason],
              alt=["具体例で確かめる：圧力鍋（外圧が高い）では 100 ℃ をこえても沸騰しない。"],
              pc=[("誤りの根拠を理解している", 1), ("正しく選んでいる", 1)], why=why, pit=["飽和蒸気圧と、容器内の蒸気の圧力を区別していない。"])


SOLUTES = [("グルコース", "C6H12O6", sp.Integer(180), 1), ("尿素", "CO(NH2)2", sp.Integer(60), 1), ("スクロース", "C12H22O11", sp.Integer(342), 1),
           ("塩化ナトリウム", "NaCl", sp.Rational("58.5"), 2), ("塩化カルシウム", "CaCl2", sp.Integer(111), 3), ("塩化カリウム", "KCl", sp.Rational("74.5"), 2)]


def solute_txt(nm_, f, Mf, i):
    kind = "式量" if i > 1 else "分子量"
    return f"{nm_} ${tex(f).replace('(NH_2)_2', '(NH_2)_2')}$（{kind} {dec(Mf)}）"


def pick_solution(r, mlist=("0.10", "0.20", "0.050", "0.25", "0.40", "0.30", "0.15")):
    for _ in range(200):
        nm_, f, Mf, i = r.choice(SOLUTES)
        m = sp.Rational(r.choice(mlist))
        W = r.choice([100, 200, 250, 500, 400])
        w = m * sp.Rational(W, 1000) * Mf
        if clean(w, 3):
            return nm_, f, Mf, i, m, W, w
    return "グルコース", "C6H12O6", sp.Integer(180), 1, sp.Rational("0.10"), 100, sp.Rational("1.8")


@gen("basic_check", 4, ["computation", "condition_check"])
def colligative_basic(r):
    nm_, f, Mf, i, m, W, w = pick_solution(r)
    elec = "（完全に電離するものとする）" if i > 1 else ""
    form = r.choice(["bp", "fp", "m"])
    if form == "m":
        return numq(f"{solute_txt(nm_, f, Mf, i)} {dec(w)} g を水 {W} g に溶かした水溶液の質量モル濃度は何 mol/kg か。", m, f"{w}/({Mf})/({W}/1000)",
                    f"溶質 $\\dfrac{{{dec(w)}}}{{{dec(Mf)}}}={dec(m * W / 1000)}$ mol を溶媒 {dec(sp.Rational(W, 1000))} kg で割る。", unit="mol/kg", d=1,
                    ap="質量モル濃度＝溶質の物質量÷溶媒の質量（kg）。分母は溶液ではなく溶媒。",
                    steps=[f"溶質：$\\dfrac{{{dec(w)}}}{{{dec(Mf)}}}={dec(m * W / 1000)}$ mol。", f"溶媒：{W} g＝{dec(sp.Rational(W, 1000))} kg。", f"$m={sig(m)}$ mol/kg。"],
                    alt=["溶媒 1 kg あたりに換算する：1000 g は " + f"{W} g の {sp.Rational(1000, W)} 倍なので、溶質の物質量も同じ倍率にする。"],
                    pc=[("溶質の物質量を求めている", 1), ("値が正しい", 1)], pit=["溶液の質量（溶質＋溶媒）で割る。", "g のまま割る。"])
    if form == "bp":
        dT = KB_W * m * i
        return numq(f"{solute_txt(nm_, f, Mf, i)} {dec(w)} g を水 {W} g に溶かした水溶液の沸点上昇度は何 K か{elec}。水のモル沸点上昇を 0.52 K·kg/mol とする。", dT,
                    f"0.52*{w}/({Mf})/({W}/1000)*{i}", f"$\\Delta t_{{\\mathrm{{b}}}}=K_{{\\mathrm{{b}}}}\\times{sig(m * i)}={sig(dT)}$ K。", unit="K", d=2,
                    ap="沸点上昇度は溶質粒子の質量モル濃度に比例する。電解質は電離後の粒子の数で考える。",
                    steps=[f"$m={sig(m)}$ mol/kg。" + (f"電離により粒子は {i} 倍で ${sig(m * i)}$ mol/kg。" if i > 1 else ""),
                           f"$\\Delta t_{{\\mathrm{{b}}}}=0.52\\times{sig(m * i)}={sig(dT)}$ K。"],
                    alt=["沸点そのものを問われたら、100 ℃ にこの値を加える。"],
                    pc=[("粒子の質量モル濃度を求めている", 1), ("値が正しい", 1)], pit=["電解質の電離を考えずに計算する。" if i > 1 else "溶媒の質量を kg に直し忘れる。"])
    dT = KF_W * m * i
    return numq(f"{solute_txt(nm_, f, Mf, i)} {dec(w)} g を水 {W} g に溶かした水溶液の凝固点は何 ℃ か{elec}。水の凝固点を 0 ℃、モル凝固点降下を 1.85 K·kg/mol とする。", -dT,
                f"-1.85*{w}/({Mf})/({W}/1000)*{i}", f"$\\Delta t_{{\\mathrm{{f}}}}=1.85\\times{sig(m * i)}={sig(dT)}$ K だけ 0 ℃ より低い。", unit="℃", d=2,
                ap="凝固点降下度 $\\Delta t_{\\mathrm{f}}=K_{\\mathrm{f}}m$ を求め、0 ℃ から引く。",
                steps=[f"粒子の質量モル濃度：${sig(m * i)}$ mol/kg。", f"$\\Delta t_{{\\mathrm{{f}}}}=1.85\\times{sig(m * i)}={sig(dT)}$ K。", f"凝固点：$0-{sig(dT)}={sig(-dT)}$ ℃。"],
                alt=["凝固点は必ず 0 ℃ より低くなる（負の値になる）ことで符号を確かめる。"],
                pc=[("凝固点降下度を求めている", 1), ("凝固点が正しい（符号を含む）", 1)], pit=["凝固点降下度をそのまま凝固点として正の値で答える。"])


# ======================================================================
# B 標準演習
# ======================================================================

LIQS = [("メタノール", "CH3OH", 32), ("エタノール", "C2H5OH", 46), ("アセトン", "CH3COCH3", 58), ("ジエチルエーテル", "C2H5OC2H5", 74), ("ヘキサン", "C6H14", 86),
        ("ベンゼン", "C6H6", 78)]


@gen("standard_practice", 4, ["computation", "application"])
def dumas(r):
    nm_, f, Mf = r.choice(LIQS)
    t = r.choice([87, 97])
    T = kelvin(t)
    Vml = r.choice([200, 250, 300, 500, 415])
    ps, p = pa(*r.choice([("1.0", 5), ("1.01", 5)]))
    w = sigv(p * sp.Rational(Vml, 1000) * Mf / (R_ * T), 3)
    M = w * R_ * T / (p * sp.Rational(Vml, 1000))
    return numq(f"沸点が {t} ℃ より低い揮発性の液体 X を、容積 {Vml} mL のフラスコに少量入れ、小さな穴をあけたアルミニウム箔でふたをして {t} ℃ の湯に浸した。X が完全に蒸発し、余分な蒸気が追い出された後、フラスコを室温まで冷やして凝縮した X の質量を測ると {dec(w)} g であった。"
                f"大気圧は ${ps}$ Pa とし、フラスコ内の空気の影響は無視する。X の分子量を求めなさい。{RTXT}",
                M, f"{w}*8.3*10**3*{T}/({p}*{Vml}/1000)", f"{t} ℃ でフラスコは X の蒸気で満たされ、その圧力は大気圧に等しい。$M=\\dfrac{{wRT}}{{pV}}$。", d=3,
                ap="湯に浸している間、フラスコ内は X の蒸気だけで満たされ、圧力は大気圧、温度は湯の温度、体積はフラスコの容積。冷やして凝縮した質量はこの蒸気の質量に等しい。",
                steps=[f"$p={ps}$ Pa、$V={dec(sp.Rational(Vml, 1000))}$ L、$T={T}$ K、$w={dec(w)}$ g。",
                       f"$M=\\dfrac{{{dec(w)}\\times8.3\\times10^{{3}}\\times{T}}}{{{ps}\\times{dec(sp.Rational(Vml, 1000))}}}\\fallingdotseq{sig(M)}$。"],
                alt=[f"分子量 {Mf} 付近の揮発性液体としては、{nm_} ${tex(f)}$ などが考えられる。",
                     "物質量 $n=\\dfrac{pV}{RT}$ を先に求めてから $M=\\dfrac{w}{n}$ としてもよい。"],
                pc=[("蒸気の $p,\\ V,\\ T$ を正しく読み取っている", 2), ("式を立てて分子量を求めている", 2)],
                pit=["温度を室温（冷やした後）で代入する。", "体積を mL のまま代入する。"])


@gen("standard_practice", 4, ["computation", "application"])
def mixing(r):
    gases = [("窒素", "N2"), ("酸素", "O2"), ("水素", "H2"), ("アルゴン", "Ar"), ("ヘリウム", "He")]
    (na, fa), (nb, fb) = r.sample(gases, 2)
    p1s, p1 = pa(*r.choice([("1.0", 5), ("2.0", 5), ("3.0", 5), ("1.5", 5), ("4.0", 5)]))
    p2s, p2 = pa(*r.choice([("1.0", 5), ("2.0", 5), ("5.0", 4), ("6.0", 4), ("3.0", 5)]))
    V1 = sp.Rational(r.choice(["1.0", "2.0", "3.0", "4.0"]))
    V2 = sp.Rational(r.choice(["1.0", "2.0", "3.0", "6.0"]))
    pa_ = p1 * V1 / (V1 + V2)
    pb_ = p2 * V2 / (V1 + V2)
    form = r.choice(["pa", "total", "heat"])
    stem = (f"容積 {dec(V1)} L の容器 A に${p1s}$ Pa の{na}を、容積 {dec(V2)} L の容器 B に${p2s}$ Pa の{nb}を入れ、温度を一定に保ったままコックを開いて"
            "両方の気体を混合した。コック部分の体積は無視する。")
    steps = [f"{na}：$p_1V_1=p_{{\\mathrm{{A}}}}(V_1+V_2)$ より $p_{{\\mathrm{{A}}}}=\\dfrac{{{p1s}\\times{dec(V1)}}}{{{dec(V1 + V2)}}}={sig(pa_)}$ Pa。",
             f"{nb}：$p_{{\\mathrm{{B}}}}=\\dfrac{{{p2s}\\times{dec(V2)}}}{{{dec(V1 + V2)}}}={sig(pb_)}$ Pa。"]
    if form == "pa":
        return numq(stem + f"混合後の{na}の分圧は何 Pa か。", pa_, f"{p1}*{V1}/({V1}+{V2})", "各気体は温度一定のまま全体積に広がる（ボイルの法則）。", unit="Pa", d=2,
                    ap="混合後の分圧は、その気体だけが全体積に広がったときの圧力。温度一定なのでボイルの法則を使う。",
                    steps=steps[:1], alt=["物質量の比で考える：同温では $pV$ が物質量に比例するので、$pV$ の値は混合の前後で保たれる。"],
                    pc=[("全体積に広がると考えている", 2), ("値が正しい", 2)], pit=["もとの圧力のまま変わらないと考える。", "体積を容器 A の分だけで考える。"])
    if form == "total":
        return numq(stem + "混合後の全圧は何 Pa か。", pa_ + pb_, f"({p1}*{V1}+{p2}*{V2})/({V1}+{V2})", "各分圧を求めて足す。", unit="Pa", d=3,
                    ap="それぞれの気体の分圧をボイルの法則で求め、分圧の法則で足し合わせる。",
                    steps=steps + [f"全圧：${sig(pa_)}+{sig(pb_)}={sig(pa_ + pb_)}$ Pa。"],
                    alt=["$p_{\\text{全}}(V_1+V_2)=p_1V_1+p_2V_2$ と一気に立ててもよい。"],
                    pc=[("各分圧を求めている", 2), ("全圧が正しい", 2)], pit=["2つの圧力を単純に足す、または単純平均する。"])
    t1, t2 = r.sample([27, 127, 77, 227, 0], 2)
    tot = (pa_ + pb_) * kelvin(t2) / kelvin(t1)
    stem = stem.replace("温度を一定に保ったまま", f"{t1} ℃ に保ったまま")
    return numq(stem + f"その後、全体を {t2} ℃ にした。このときの全圧は何 Pa か。", tot, f"({p1}*{V1}+{p2}*{V2})/({V1}+{V2})*({t2}+273)/({t1}+273)",
                "混合後の全圧を求め、体積一定で絶対温度に比例させる。", unit="Pa", d=3,
                ap="まず温度一定で混合後の全圧を求め、次に体積一定で温度を変える（圧力は絶対温度に比例）。",
                steps=steps + [f"{t1} ℃ での全圧：${sig(pa_ + pb_)}$ Pa。", f"{t2} ℃：${sig(pa_ + pb_)}\\times\\dfrac{{{kelvin(t2)}}}{{{kelvin(t1)}}}={sig(tot)}$ Pa。"],
                alt=["全物質量を $\\dfrac{p_1V_1+p_2V_2}{RT_1}$ で求め、状態方程式に $T_2$ を代入しても同じ。"],
                pc=[("混合後の全圧を求めている", 2), ("温度変化を正しく扱っている", 2)], pit=["温度の比をセルシウス温度でとる。"])


VP_T = [27, 37, 47, 57, 67, 77]


@gen("standard_practice", 4, ["computation", "condition_check"])
def vapor_container(r):
    t = r.choice(VP_T)
    T = kelvin(t)
    pv = water_vp(t)
    V = sp.Rational(r.choice(["8.3", "4.15", "16.6", "10", "5.0", "2.0"]))
    n = sp.Rational(r.choice(["0.010", "0.020", "0.050", "0.10", "0.0050", "0.0030", "0.0020"]))
    pall = n * R_ * T / V
    if abs(pall - pv) / pv < sp.Rational(1, 20):
        n = n * 2
        pall = n * R_ * T / V
    liquid = pall > pv
    ans = pv if liquid else pall
    with_n2 = r.random() < 0.4
    if with_n2:
        nn = sp.Rational(r.choice(["0.10", "0.20", "0.050"]))
        pn = nn * R_ * T / V
        return numq(f"容積 {dec(V)} L の真空容器に窒素 {dec(nn)} mol と水 {dec(n)} mol を入れ、{t} ℃ に保った。容器内の全圧は何 Pa か。{t} ℃ の水の飽和蒸気圧は ${sci(pv)}$ Pa とし、"
                    f"液体の水の体積と、窒素の水への溶解は無視する。{RTXT}", pn + ans, f"{nn}*8.3*10**3*{T}/({V})+Min({n}*8.3*10**3*{T}/({V}), {pv})",
                    "窒素の分圧と水蒸気の分圧を別々に求めて足す。水蒸気は飽和蒸気圧と比べて判断する。", unit="Pa", d=4,
                    ap="窒素は常に気体。水はすべて蒸発したと仮定した圧力と飽和蒸気圧を比べ、液体が残るかを判断してから分圧を足す。",
                    steps=[f"窒素の分圧：$\\dfrac{{{dec(nn)}\\times8.3\\times10^{{3}}\\times{T}}}{{{dec(V)}}}={sig(pn)}$ Pa。",
                           f"水がすべて気体なら：${sig(pall)}$ Pa。", (f"飽和蒸気圧 ${sci(pv)}$ Pa より大きいので液体が残り、水蒸気の分圧は ${sci(pv)}$ Pa。" if liquid
                                                                       else f"飽和蒸気圧 ${sci(pv)}$ Pa 以下なので、水はすべて気体。"),
                           f"全圧：${sig(pn + ans)}$ Pa。"],
                    alt=["飽和蒸気圧は他の気体（窒素）の有無に関係しないので、水だけを入れた場合と同じ判断ができる。"],
                    pc=[("窒素の分圧を求めている", 1), ("水が液体として残るかを正しく判断している", 2), ("全圧が正しい", 1)],
                    pit=["水がすべて気体であるとして計算する。", "窒素があると水の飽和蒸気圧が変わると考える。"])
    return numq(f"容積 {dec(V)} L の真空容器に水 {dec(n)} mol を入れ、{t} ℃ に保った。容器内の圧力は何 Pa か。{t} ℃ の水の飽和蒸気圧は ${sci(pv)}$ Pa とし、液体の水の体積は無視する。{RTXT}",
                ans, f"Min({n}*8.3*10**3*{T}/({V}), {pv})", "すべて気体と仮定した圧力と飽和蒸気圧を比べる。", unit="Pa", d=3,
                ap="すべて水蒸気と仮定して状態方程式で圧力を求め、飽和蒸気圧より大きければ液体が残るので、圧力は飽和蒸気圧に等しい。",
                steps=[f"すべて気体と仮定：$p=\\dfrac{{{dec(n)}\\times8.3\\times10^{{3}}\\times{T}}}{{{dec(V)}}}={sig(pall)}$ Pa。",
                       (f"飽和蒸気圧 ${sci(pv)}$ Pa をこえるので、一部が液体として残る。圧力は ${sci(pv)}$ Pa。" if liquid
                        else f"飽和蒸気圧 ${sci(pv)}$ Pa 以下なので、すべて気体で存在できる。圧力は ${sig(pall)}$ Pa。")],
                alt=["逆に、飽和蒸気圧で気体として存在できる最大の物質量 $n_{\\max}=\\dfrac{p_{\\text{飽和}}V}{RT}$ を求め、入れた量と比べてもよい。"],
                pc=[("すべて気体と仮定した圧力を求めている", 2), ("飽和蒸気圧と比較して判断している", 2)],
                pit=["飽和蒸気圧との比較をせずに状態方程式の値を答える。", "比較の向きを逆にする。"])


@gen("standard_practice", 3, ["computation", "application"])
def osmotic(r):
    t = r.choice([27, 37, 7, 17])
    T = kelvin(t)
    if r.random() < 0.5:
        nm_, f, Mf, i = r.choice(SOLUTES[:4] + SOLUTES[5:])
        c = sp.Rational(r.choice(["0.010", "0.020", "0.10", "0.050", "0.0010"]))
        Pi = c * i * R_ * T
        elec = "（完全に電離するものとする）" if i > 1 else ""
        return numq(f"{t} ℃ で、{c and dec(c)} mol/L の{nm_}水溶液の浸透圧は何 Pa か{elec}。{RTXT}", Pi, f"{c}*{i}*8.3*10**3*{T}",
                    (f"$\\Pi={i}cRT$（粒子は {i} 倍）。" if i > 1 else "$\\Pi=cRT$。"), unit="Pa", d=2,
                    ap="ファントホッフの法則 $\\Pi=cRT$。電解質は電離後の粒子のモル濃度を使う。",
                    steps=[f"粒子のモル濃度：${dec(c)}{TIMES + str(i) if i > 1 else ''}={dec(c * i)}$ mol/L。", f"$\\Pi={dec(c * i)}\\times8.3\\times10^{{3}}\\times{T}={sig(Pi)}$ Pa。"],
                    alt=["状態方程式 $pV=nRT$ と同じ形 $\\Pi V=nRT$ で、$V=1$ L あたりで考えてもよい。"],
                    pc=[("粒子のモル濃度を用いている", 2), ("値が正しい", 2)], pit=["電解質の電離を考えない。" if i > 1 else "温度を K に直し忘れる。"])
    Mtrue = r.choice([5000, 8000, 10000, 20000, 25000, 40000, 50000, 60000])
    w = sp.Rational(r.choice(["0.50", "1.0", "2.0", "0.80", "1.5"]))
    Vml = r.choice([100, 200, 50])
    Pi = sigv(w / Mtrue * R_ * T / sp.Rational(Vml, 1000), 2)
    M = w * R_ * T / (Pi * sp.Rational(Vml, 1000))
    return numq(f"あるタンパク質 {dec(w)} g を水に溶かして {Vml} mL とした水溶液の浸透圧は、{t} ℃ で ${sig(Pi) if 'times' in sig(Pi) else sig(Pi)}$ Pa であった。このタンパク質の分子量を求めなさい。{RTXT}",
                M, f"{w}*8.3*10**3*{T}/({Pi}*{Vml}/1000)", "$\\Pi V=\\dfrac{w}{M}RT$ より $M=\\dfrac{wRT}{\\Pi V}$。", d=3,
                ap="$\\Pi V=nRT$ に $n=\\dfrac{w}{M}$ を代入して $M$ について解く。$V$ は L。",
                steps=[f"$V={dec(sp.Rational(Vml, 1000))}$ L、$T={T}$ K。", f"$M=\\dfrac{{{dec(w)}\\times8.3\\times10^{{3}}\\times{T}}}{{{sig(Pi)}\\times{dec(sp.Rational(Vml, 1000))}}}\\fallingdotseq{sig(M)}$。"],
                alt=["凝固点降下では降下度が非常に小さく測定が難しい。浸透圧は高分子でも十分に測れる大きさになることを確認する。"],
                pc=[("式を正しく立てている", 2), ("値が正しい", 2)], pit=["体積を mL のまま代入する。"])


@gen("standard_practice", 3, ["concept", "computation"])
def colligative_compare(r):
    for _ in range(200):
        picks = r.sample(SOLUTES, 4)
        ms = [sp.Rational(r.choice(["0.10", "0.20", "0.050", "0.15", "0.30"])) for _ in picks]
        eff = [m * p[3] for m, p in zip(ms, picks)]
        if len(set(eff)) == 4:
            break
    form = r.choice(["bp", "fp_high", "vp_low"])
    if form == "bp":
        k = eff.index(max(eff))
        what = "沸点が最も高いもの"
        reason = "粒子の質量モル濃度が最も大きいので、沸点上昇度が最大になる。"
    elif form == "fp_high":
        k = eff.index(min(eff))
        what = "凝固点が最も高いもの"
        reason = "粒子の質量モル濃度が最も小さいので、凝固点降下度が最小（凝固点が最も高い）になる。"
    else:
        k = eff.index(max(eff))
        what = "同じ温度での蒸気圧が最も低いもの"
        reason = "粒子の質量モル濃度が最も大きいので、蒸気圧降下が最も大きい。"
    lab = [f"{dec(m)} mol/kg の{p[0]}水溶液" for m, p in zip(ms, picks)]
    why = {lab[j]: (f"溶質粒子の質量モル濃度は ${dec(ms[j])}\\times{picks[j][3]}={dec(eff[j])}$ mol/kg で、条件に合うものではない。", "粒子の数（電離）を考えない誤り")
           for j in range(4) if j != k}
    return mc(f"次の水溶液のうち、{what}を選びなさい。ただし、電解質は水溶液中で完全に電離するものとする。", [lab[k]] + [lab[j] for j in range(4) if j != k],
              f"{lab[k]}は、溶質粒子の質量モル濃度が ${dec(eff[k])}$ mol/kg。{reason}", d=3,
              ap="希薄溶液の性質は溶質の種類によらず、溶質粒子の質量モル濃度で決まる。電解質は電離で粒子が増える（NaCl・KCl は2倍、CaCl₂ は3倍）。",
              steps=["各水溶液の溶質粒子の質量モル濃度（質量モル濃度×電離で生じる粒子の数）を求める：" + "、".join(f"{p[0]} {dec(e)}" for p, e in zip(picks, eff)) + "（mol/kg）。",
                     "沸点上昇・凝固点降下・蒸気圧降下は、この値に比例する。", f"条件に合うのは{lab[k]}。"],
              alt=["粒子の数だけを比べる問題なので、$K_{\\mathrm{b}}$ や $K_{\\mathrm{f}}$ の値は不要であることを確認する。"],
              pc=[("粒子の質量モル濃度を比べている", 2), ("正しく選んでいる", 2)], why=why,
              pit=["質量モル濃度の数値だけを比べ、電離による粒子の増加を無視する。", "「凝固点が高い」と「凝固点降下度が大きい」を取り違える。"])


@gen("standard_practice", 2, ["computation", "application"])
def molar_mass_fp(r):
    solvent = r.choice(["水", "ベンゼン"])
    Kf = KF_W if solvent == "水" else KF_B
    if solvent == "水":
        Mtrue = r.choice([60, 92, 180, 342, 62])
    else:
        Mtrue = r.choice([128, 122, 154, 178, 92])
    w = sp.Rational(r.choice(["1.0", "2.0", "1.5", "3.0", "0.50", "2.5"]))
    W = r.choice([50, 100, 200, 250])
    dT = sigv(Kf * w / Mtrue / sp.Rational(W, 1000), 2)
    M = Kf * w / (dT * sp.Rational(W, 1000))
    fp = "0 ℃" if solvent == "水" else "5.5 ℃"
    return numq(f"ある非電解質 {dec(w)} g を{solvent} {W} g に溶かした溶液の凝固点は、純粋な{solvent}（凝固点 {fp}）より {dec(dT)} K 低かった。この非電解質の分子量を求めなさい。{solvent}のモル凝固点降下を {dec(Kf)} K·kg/mol とする。",
                M, f"{Kf}*{w}/({dT}*{W}/1000)", "$\\Delta t_{\\mathrm{f}}=K_{\\mathrm{f}}\\times\\dfrac{w/M}{W/1000}$ を $M$ について解く。", d=3,
                ap="凝固点降下度から質量モル濃度を求め、溶媒の質量から溶質の物質量を出し、質量÷物質量で分子量を求める。",
                steps=[f"$m=\\dfrac{{{dec(dT)}}}{{{dec(Kf)}}}$ mol/kg。", f"溶質の物質量：$m\\times{dec(sp.Rational(W, 1000))}$ mol。",
                       f"$M=\\dfrac{{{dec(w)}}}{{m\\times{dec(sp.Rational(W, 1000))}}}=\\dfrac{{{dec(Kf)}\\times{dec(w)}}}{{{dec(dT)}\\times{dec(sp.Rational(W, 1000))}}}\\fallingdotseq{sig(M)}$。"],
                alt=["1つの式 $M=\\dfrac{K_{\\mathrm{f}}w}{\\Delta t_{\\mathrm{f}}W'}$（$W'$ は溶媒の kg）にまとめて代入してもよい。"],
                pc=[("質量モル濃度を求めている", 2), ("分子量が正しい", 2)], pit=["溶媒の質量を g のまま使う。"])


# ======================================================================
# C 思考力・記述応用
# ======================================================================

RXN_W = [("亜鉛", "Zn", sp.Integer(65), "水素", "\\mathrm{Zn}+2\\mathrm{HCl}\\longrightarrow\\mathrm{ZnCl_2}+\\mathrm{H_2}", 1, "希塩酸"),
         ("マグネシウム", "Mg", sp.Integer(24), "水素", "\\mathrm{Mg}+2\\mathrm{HCl}\\longrightarrow\\mathrm{MgCl_2}+\\mathrm{H_2}", 1, "希塩酸"),
         ("過酸化水素", "H2O2", sp.Integer(34), "酸素", "2\\mathrm{H_2O_2}\\longrightarrow2\\mathrm{H_2O}+\\mathrm{O_2}", 2, "酸化マンガン(Ⅳ)を触媒とした過酸化水素水の分解")]
WVP = {20: "2.3", 25: "3.2", 27: "3.6", 30: "4.2"}


@gen("thinking_writing", 3, ["cross_unit", "computation", "written_reasoning"], rel=["HS-CHEB-U02"])
def over_water(r):
    nm_, f, Mf, gas, eq, k, how = r.choice(RXN_W)
    t = r.choice(list(WVP))
    T = kelvin(t)
    pvs, pv = pa(WVP[t], 3)
    pts, pt = pa(r.choice(["1.01", "1.00", "1.02"]), 5)
    Vml = r.choice([166, 249, 332, 415, 498, 83])
    n = (pt - pv) * sp.Rational(Vml, 1000) / (R_ * T)
    w = n * k * Mf
    src = f"{nm_}（${tex(f)}$）" if f != "H2O2" else nm_
    stem = (f"{how if f == 'H2O2' else src + 'に' + how + 'を加える反応'}で発生した{gas}を水上置換で捕集した。捕集びんの内と外の水面の高さを一致させて体積を測ると、{t} ℃ で {Vml} mL であった。"
            f"大気圧は ${pts}$ Pa、{t} ℃ の水の飽和蒸気圧は ${pvs}$ Pa とする。反応は ${eq}$ で表される。\n"
            f"(1) 水面の高さを一致させる理由と、{gas}の分圧の求め方を説明しなさい。\n(2) 反応した{nm_}の質量を求めなさい。{RTXT}原子量は H＝1.0、O＝16、Mg＝24、Zn＝65 とし、有効数字2桁で答えなさい。")
    return desc(stem, f"(1) 内外の水面の高さをそろえると、捕集びん内の気体の全圧が大気圧に等しくなる。捕集びん内には{gas}と水蒸気が混合しているので、{gas}の分圧＝大気圧−水の飽和蒸気圧＝${sig(pt - pv, 3)}$ Pa。"
                f"(2) {gas}：$n=\\dfrac{{{sig(pt - pv, 3)}\\times{dec(sp.Rational(Vml, 1000))}}}{{8.3\\times10^{{3}}\\times{T}}}\\fallingdotseq{sci(n, 3)}$ mol。{nm_}はその {k} 倍で、質量は約 ${sig(w)}$ g。",
                "水上置換で集めた気体は水蒸気との混合気体。目的の気体の分圧に状態方程式を適用する。",
                [("水面をそろえると全圧が大気圧になることを説明している", 2), ("分圧＝大気圧−水蒸気圧であることを説明している", 2), ("気体の物質量を状態方程式で求めている", 2),
                 ("係数の比を用いて質量を正しく求めている", 2)],
                d=4, p=8, lines=9,
                ap=f"捕集した気体は{gas}と飽和水蒸気の混合気体（分圧の法則）。水面をそろえると全圧が大気圧になる。物質量から反応式の係数の比で{nm_}の量を求める（物質量の計算は化学基礎の内容）。",
                steps=[f"{gas}の分圧：${pts}-{pvs}={sig(pt - pv, 3)}$ Pa。", f"$V={dec(sp.Rational(Vml, 1000))}$ L、$T={T}$ K。",
                       f"$n=\\dfrac{{pV}}{{RT}}\\fallingdotseq{sci(n, 3)}$ mol。", f"係数の比より{nm_}は ${k}n$ mol、質量 ${k}n\\times{Mf}\\fallingdotseq{sig(w)}$ g。"],
                alt=["水面の高さがそろっていない場合、内側の水面が高ければ内部の圧力は大気圧より水柱の分だけ低い、と考えると理由が説明しやすい。"],
                pc=[("水面", 2), ("分圧", 2), ("物質量", 2), ("質量", 2)],
                pit=["水蒸気圧を引かずに、大気圧をそのまま気体の圧力とする。", "過酸化水素の係数 2 を忘れる。" if k == 2 else "mL を L に直し忘れる。"],
                chk=(f"({pt}-{pv})*{Vml}/1000/(8.3*10**3*{T})*{k}*{Mf}", str(w), None, "intermediate"))


@gen("thinking_writing", 3, ["written_reasoning", "computation"])
def cooling_curve(r):
    solvent = r.choice(["水", "ベンゼン"])
    Kf = KF_W if solvent == "水" else KF_B
    Mtrue = r.choice([60, 180, 342]) if solvent == "水" else r.choice([128, 154, 178])
    w = sp.Rational(r.choice(["1.0", "2.0", "1.5", "3.0", "0.60"]))
    W = r.choice([100, 200, 50])
    dT = sigv(Kf * w / Mtrue / sp.Rational(W, 1000), 2)
    M = Kf * w / (dT * sp.Rational(W, 1000))
    return desc(f"ある非電解質 {dec(w)} g を{solvent} {W} g に溶かした溶液をゆっくり冷却し、温度変化を記録すると図のような冷却曲線が得られた。\n"
                "(1) 点B付近で、凝固点より低い温度になっても液体のままである状態を何というか。\n(2) 凝固が始まった後（C以降）も温度が下がり続ける理由を説明しなさい。\n"
                f"(3) この溶液の凝固点は図の点A〜Dのどの温度か。また、その温度が純粋な{solvent}の凝固点より {dec(dT)} K 低かったとき、この非電解質の分子量を求めなさい。"
                f"{solvent}のモル凝固点降下は {dec(Kf)} K·kg/mol とし、有効数字2桁で答えなさい。",
                f"(1) 過冷却。(2) 凝固では溶媒だけが固体になるので、残った溶液の濃度（質量モル濃度）が大きくなり、凝固点がさらに下がり続けるから。"
                f"(3) 点A（C以降の直線を延長し、はじめの冷却の線と交わる点の温度）。$M=\\dfrac{{{dec(Kf)}\\times{dec(w)}}}{{{dec(dT)}\\times{dec(sp.Rational(W, 1000))}}}\\fallingdotseq{sig(M)}$。",
                "過冷却がなければ凝固はAの温度で始まっていたはず、と考えて延長線から凝固点を読む。",
                [("(1) 過冷却と答えている", 1), ("(2) 溶媒のみが凝固し溶液が濃くなることを説明している", 3), ("(3) 凝固点を点Aと判断している", 2), ("(3) 分子量を正しく求めている", 2)],
                d=4, p=8, lines=9, fig=cooling_fig(),
                ap="純溶媒の冷却曲線（凝固中は温度一定）と比べる。溶液では、凝固が進むと溶液が濃くなることに注目する。",
                steps=["Bは凝固点より低いのに液体のまま（過冷却）。凝固が始まると凝固熱でCまで温度が上がる。", "溶媒だけが固体になるので、残りの溶液の質量モル濃度が増え、凝固点が下がり続ける。",
                       "過冷却がなければ凝固はA（延長線との交点）で始まるので、凝固点はAの温度。",
                       f"$m=\\dfrac{{{dec(dT)}}}{{{dec(Kf)}}}$ mol/kg、$M=\\dfrac{{{dec(w)}}}{{m\\times{dec(sp.Rational(W, 1000))}}}\\fallingdotseq{sig(M)}$。"],
                alt=["純溶媒の冷却曲線を並べてかき、凝固中の水平部分が溶液では右下がりになることを図で示して説明してもよい。"],
                pc=[("過冷却", 1), ("理由", 3), ("凝固点の読み取り", 2), ("分子量", 2)],
                pit=["最低点Bを凝固点と読む。", "Cの温度を凝固点と読む（Aよりわずかに低い）。"],
                chk=(f"{Kf}*{w}/({dT}*{W}/1000)", str(M), None, "intermediate"))


@gen("thinking_writing", 2, ["written_reasoning", "application"])
def henry(r):
    gas, s_mol, Mg = r.choice([("酸素", "1.4", 32), ("窒素", "0.70", 28), ("酸素", "1.2", 32), ("窒素", "0.62", 28)])
    s = sp.Rational(s_mol) / 1000
    t = r.choice([20, 25, 15])
    ptot = sp.Rational(r.choice(["2.0", "5.0", "3.0", "1.0"])) * 10 ** 5
    frac_ = sp.Rational(1, 5) if gas == "酸素" else sp.Rational(4, 5)
    Vw = sp.Rational(r.choice(["1.0", "2.0", "5.0", "10"]))
    p_part = ptot * frac_
    nmol = s * p_part / 10 ** 5 * Vw
    mass_mg = nmol * Mg * 1000
    return desc(f"{t} ℃ で、分圧 $1.0\\times10^{{5}}$ Pa の{gas}は水 1.0 L に ${s_mol}\\times10^{{-3}}$ mol 溶けるものとする。"
                f"空気（窒素と酸素の物質量の比 4：1）を、全圧 ${sci(ptot)}$ Pa で {t} ℃ の水 {dec(Vw)} L に接触させて十分な時間がたった。\n"
                f"(1) 水に溶けた{gas}の質量は何 mg か。原子量は N＝14、O＝16 とし、有効数字2桁で答えなさい。\n"
                f"(2) 溶けた{gas}の体積を、そのときの{gas}の分圧・温度のもとで測ると、分圧が2倍になっても変わらない。この理由をヘンリーの法則と状態方程式を用いて説明しなさい。",
                f"(1) {gas}の分圧は ${sci(ptot)}\\times{FR5 if gas == '酸素' else FR45}={sci(p_part)}$ Pa。溶ける物質量は分圧に比例し、"
                f"${s_mol}\\times10^{{-3}}\\times\\dfrac{{{sci(p_part)}}}{{1.0\\times10^{{5}}}}\\times{dec(Vw)}={sci(nmol)}$ mol、質量は約 ${sig(mass_mg)}$ mg。"
                "(2) 分圧が2倍になると溶ける物質量は2倍になるが、その分圧のもとで体積を測ると $V=\\dfrac{nRT}{p}$ より、$n$ と $p$ がともに2倍なので体積は変わらない。",
                "ヘンリーの法則：溶ける気体の物質量は分圧に比例。体積は測る圧力によって変わる。",
                [("分圧を正しく求めている", 2), ("溶ける物質量を分圧に比例させて求めている", 2), ("質量を正しく求めている", 1), ("(2) 物質量と圧力がともに2倍で体積一定となることを説明している", 3)],
                d=4, p=8, lines=8,
                ap="まず空気中の分圧をモル分率で求め、ヘンリーの法則（物質量は分圧に比例）を使う。体積については状態方程式 $V=\\dfrac{nRT}{p}$ で考える。",
                steps=[f"分圧：${sci(p_part)}$ Pa。", f"溶ける物質量：${s_mol}\\times10^{{-3}}\\times\\dfrac{{{sci(p_part)}}}{{1.0\\times10^{{5}}}}\\times{dec(Vw)}={sci(nmol)}$ mol。",
                       f"質量：${sci(nmol)}\\times{Mg}\\times10^{{3}}\\fallingdotseq{sig(mass_mg)}$ mg。", "(2) $V=\\dfrac{nRT}{p}$ で $n\\propto p$ なので $V$ は一定。"],
                alt=["標準状態に換算した体積で表すと、溶ける体積は分圧に比例する。どの条件で体積を測るかで表し方が変わる、とまとめてもよい。"],
                pc=[("分圧", 2), ("物質量", 2), ("質量", 1), ("説明", 3)],
                pit=["全圧をそのまま使い、分圧を求めない。", "水の体積をかけ忘れる。"],
                chk=(f"{s}*{p_part}/10**5*{Vw}*{Mg}*1000", str(mass_mg), None, "intermediate"))


REAL = [("アンモニア", "水素", "アンモニアは極性分子で分子間力（水素結合）が大きい"), ("二酸化炭素", "ヘリウム", "二酸化炭素は分子が大きく分子間力も大きい"),
        ("アンモニア", "ヘリウム", "アンモニアは極性分子で分子間力（水素結合）が大きい"), ("二酸化炭素", "水素", "二酸化炭素は分子が大きく分子間力も大きい"),
        ("メタン", "ヘリウム", "メタンはヘリウムより分子が大きく分子間力も大きい")]


@gen("thinking_writing", 2, ["written_reasoning", "concept"])
def real_gas(r):
    a, b, why_ = r.choice(REAL)
    cond = r.choice(["低温・高圧", "低温", "高圧"])
    return desc(f"実在気体の $Z=\\dfrac{{pV}}{{nRT}}$ の値は、理想気体では常に 1 である。{a}と{b}を比べると、{cond}の条件で 1 からのずれが大きいのは{a}である。\n"
                f"(1) 実在気体が理想気体からずれる2つの原因を挙げなさい。\n(2) {cond}でずれが大きくなる理由と、{a}のずれが{b}より大きい理由を説明しなさい。\n"
                "(3) 実在気体を理想気体に近づけるには、温度と圧力をどのようにすればよいか。",
                f"(1) 分子自身に体積があること、分子間に引力（分子間力）がはたらくこと。"
                f"(2) 低温では分子の熱運動が穏やかになり、分子間力の影響が相対的に大きくなる。高圧では分子どうしが接近し、分子間力の影響と、気体全体の体積に占める分子自身の体積の割合が大きくなる。{why_}ので、{b}よりずれが大きい。"
                "(3) 高温・低圧にする。",
                "理想気体は「分子の体積 0・分子間力なし」と仮定したモデル。実在気体はこの2点で異なる。",
                [("(1) 分子の体積と分子間力の2つを挙げている", 2), (f"(2) {cond}で影響が大きくなる理由を説明している", 3), (f"(2) {a}の分子間力・大きさに触れている", 2), ("(3) 高温・低圧と答えている", 1)],
                d=4, p=8, lines=8,
                ap="理想気体のモデルの2つの仮定（分子の体積が 0、分子間力がない）が、どの条件で成り立たなくなるかを考える。",
                steps=["理想気体の仮定：分子の体積 0、分子間力なし。", "低温：熱運動が弱く、分子間力で引き合う影響が目立つ（$Z<1$ になりやすい）。",
                       "高圧：分子間の距離が小さく、分子の体積と分子間力の影響が大きい。", f"{why_}。", "高温・低圧では両方の影響が小さくなる。"],
                alt=["分子間力が大きいと壁に衝突する勢いが弱まり、圧力が理想気体より小さくなる（$Z<1$）。分子の体積の影響が大きいと、分子が動ける空間が小さく $Z>1$ になる、と2つの効果に分けて説明してもよい。"],
                pc=[("原因", 2), ("条件の説明", 3), ("物質の比較", 2), ("条件", 1)],
                pit=["「低温・高圧ほど理想気体に近い」と逆に覚えている。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

@gen("error_correction", 4, ["common_error", "condition_check"])
def err_units(r):
    form = r.choice(["celsius_charles", "celsius_pv", "ml"])
    if form == "celsius_charles":
        t1, t2 = r.choice([(27, 127), (127, 27), (27, 327), (77, 227), (227, 27), (47, 127)])
        V1 = sp.Rational(r.choice(["3.0", "6.0", "2.0", "4.0", "1.2"]))
        wrong = V1 * t2 / t1
        right = V1 * kelvin(t2) / kelvin(t1)
        return err_item(f"圧力一定で、{t1} ℃ で {dec(V1)} L の気体を {t2} ℃ にしたときの体積を求めなさい。",
                        f"体積は温度に比例するので、${dec(V1)}\\times\\dfrac{{{t2}}}{{{t1}}}={sig(wrong)}$ L",
                        "温度の比をセルシウス温度でとった部分", "unit",
                        "「体積は温度に比例する」という言葉だけを覚えていて、その温度が絶対温度であることを確認していない。",
                        f"${dec(V1)}\\times\\dfrac{{{kelvin(t2)}}}{{{kelvin(t1)}}}={sig(right)}$ L", f"${sig(right)}$ L",
                        "シャルルの法則で体積が比例するのは絶対温度 $T=t+273$ である。",
                        [f"$T_1={kelvin(t1)}$ K、$T_2={kelvin(t2)}$ K。", f"$V_2={dec(V1)}\\times\\dfrac{{{kelvin(t2)}}}{{{kelvin(t1)}}}={sig(right)}$ L。"],
                        "気体の法則に温度を代入するときは、必ず K に直す。",
                        ["0 ℃ から 1 ℃ に温めると体積が無限倍になってしまう、という不合理から、セルシウス温度の比が使えないことを確かめる。"],
                        ["セルシウス温度の比で計算する。"], chk=(f"{V1}*({t2}+273)/({t1}+273)", str(right), None, "intermediate"), d=2)
    if form == "celsius_pv":
        t = r.choice([27, 127, 77, 227, 57])
        n = sp.Rational(r.choice(["0.10", "0.20", "0.50", "1.0"]))
        V = sp.Rational(r.choice(["8.3", "10", "5.0", "2.0"]))
        wrong = n * R_ * t / V
        right = n * R_ * kelvin(t) / V
        return err_item(f"{dec(n)} mol の気体を {dec(V)} L の容器に入れて {t} ℃ に保ったときの圧力を求めなさい。{RTXT}",
                        f"$p=\\dfrac{{nRT}}{{V}}=\\dfrac{{{dec(n)}\\times8.3\\times10^{{3}}\\times{t}}}{{{dec(V)}}}={sig(wrong)}$ Pa",
                        "$T$ に代入した値", "unit",
                        "問題文の温度の数値をそのまま $T$ に代入し、絶対温度への換算を忘れている。",
                        f"$T={t}+273={kelvin(t)}$ K を代入して $p={sig(right)}$ Pa", f"${sig(right)}$ Pa",
                        "状態方程式の $T$ は絶対温度（K）。$R$ の単位 Pa·L/(K·mol) からも K で代入する必要が分かる。",
                        [f"$T={kelvin(t)}$ K。", f"$p=\\dfrac{{{dec(n)}\\times8.3\\times10^{{3}}\\times{kelvin(t)}}}{{{dec(V)}}}={sig(right)}$ Pa。"],
                        "代入する前に、$R$ の単位に合わせて $p$（Pa）・$V$（L）・$T$（K）をそろえる。",
                        ["単位の約分で確かめる：$R$ の K と $T$ の K が約分されて Pa が残る。"], ["セルシウス温度を代入する。"],
                        chk=(f"{n}*8.3*10**3*({t}+273)/({V})", str(right), None, "intermediate"), d=2)
    t = r.choice([27, 127, 77])
    n = sp.Rational(r.choice(["0.010", "0.020", "0.050", "0.0050"]))
    Vml = r.choice([500, 250, 830, 415, 100])
    right = n * R_ * kelvin(t) / sp.Rational(Vml, 1000)
    wrong = n * R_ * kelvin(t) / Vml
    return err_item(f"{dec(n)} mol の気体を容積 {Vml} mL の容器に入れて {t} ℃ に保ったときの圧力を求めなさい。{RTXT}",
                    f"$p=\\dfrac{{{dec(n)}\\times8.3\\times10^{{3}}\\times{kelvin(t)}}}{{{Vml}}}={sig(wrong)}$ Pa",
                    "体積に代入した値", "unit",
                    "温度は K に直したが、体積の単位を $R$ の単位（L）に合わせることを見落としている。",
                    f"$V={dec(sp.Rational(Vml, 1000))}$ L を代入して $p={sig(right)}$ Pa", f"${sig(right)}$ Pa",
                    f"$R=8.3\\times10^{{3}}$ Pa·L/(K·mol) を使うときは体積を L で代入する。{Vml} mL＝{dec(sp.Rational(Vml, 1000))} L。",
                    [f"$V={dec(sp.Rational(Vml, 1000))}$ L。", f"$p=\\dfrac{{{dec(n)}\\times8.3\\times10^{{3}}\\times{kelvin(t)}}}{{{dec(sp.Rational(Vml, 1000))}}}={sig(right)}$ Pa。"],
                    "代入前に単位をそろえる欄（$p$［Pa］、$V$［L］、$T$［K］）を作る。",
                    ["誤答は 1000 分の1の値。小さな容器ほど圧力は大きくなるはずだ、という感覚と照らし合わせる。"], ["mL のまま代入する。"],
                    chk=(f"{n}*8.3*10**3*({t}+273)/({Vml}/1000)", str(right), None, "intermediate"), d=2)


@gen("error_correction", 3, ["common_error", "concept"])
def err_colligative(r):
    if r.random() < 0.5:
        nm_, f, Mf, i, m, W, w = pick_solution(r)
        while i == 1:
            nm_, f, Mf, i, m, W, w = pick_solution(r)
        wrong = KF_W * m
        right = KF_W * m * i
        return err_item(f"{solute_txt(nm_, f, Mf, i)} {dec(w)} g を水 {W} g に溶かした水溶液の凝固点降下度を求めなさい。{nm_}は完全に電離し、水のモル凝固点降下は 1.85 K·kg/mol とする。",
                        f"$m=\\dfrac{{{dec(w)}/{dec(Mf)}}}{{{dec(sp.Rational(W, 1000))}}}={sig(m)}$ mol/kg なので、$\\Delta t_{{\\mathrm{{f}}}}=1.85\\times{sig(m)}={sig(wrong)}$ K",
                        "質量モル濃度をそのまま用いた部分", "concept",
                        "質量モル濃度の計算に集中し、凝固点降下が溶質「粒子」の数で決まることと、電解質が電離して粒子が増えることを見落としている。",
                        f"電離で粒子は {i} 倍になるので $\\Delta t_{{\\mathrm{{f}}}}=1.85\\times{sig(m)}\\times{i}={sig(right)}$ K", f"${sig(right)}$ K",
                        f"{nm_}は電離して {i} 個のイオンになるので、粒子の質量モル濃度は ${sig(m * i)}$ mol/kg。",
                        [f"$m={sig(m)}$ mol/kg。", f"粒子の質量モル濃度：${sig(m)}\\times{i}={sig(m * i)}$ mol/kg。", f"$\\Delta t_{{\\mathrm{{f}}}}=1.85\\times{sig(m * i)}={sig(right)}$ K。"],
                        "溶質が電解質かどうかを最初に確認し、電離式から粒子の数を数える。",
                        [f"電離式をかいて確かめる：1 mol から {i} mol のイオンが生じる。"], ["電解質の電離を考えない。"],
                        chk=(f"1.85*{w}/({Mf})/({W}/1000)*{i}", str(right), None, "intermediate"), d=3)
    for _ in range(200):
        nm_, f, Mf, i, m, W, w = pick_solution(r, ("0.20", "0.25", "0.40", "0.30", "0.50"))
        if i == 1 and sig(KB_W * (w / Mf) / (sp.Rational(W + w) / 1000)) != sig(KB_W * m):
            break
    tot = W + w
    wrong_m = (w / Mf) / (sp.Rational(tot) / 1000)
    return err_item(f"{solute_txt(nm_, f, Mf, i)} {dec(w)} g を含む水溶液が全体で {dec(tot)} g ある。この水溶液の沸点上昇度を求めなさい。水のモル沸点上昇は 0.52 K·kg/mol とし、有効数字2桁で答えなさい。",
                    f"$m=\\dfrac{{{dec(w)}/{dec(Mf)}}}{{{dec(sp.Rational(tot) / 1000)}}}$ mol/kg として、$\\Delta t_{{\\mathrm{{b}}}}=0.52\\times m\\fallingdotseq{sig(KB_W * wrong_m)}$ K",
                    "質量モル濃度の分母", "concept",
                    "モル濃度（溶液の体積あたり）と混同し、質量モル濃度の分母も「溶液」の質量だと考えている。",
                    f"溶媒は ${dec(tot)}-{dec(w)}={W}$ g なので $m={sig(m)}$ mol/kg、$\\Delta t_{{\\mathrm{{b}}}}=0.52\\times{sig(m)}\\fallingdotseq{sig(KB_W * m)}$ K", f"${sig(KB_W * m)}$ K",
                    "質量モル濃度は「溶媒」1 kg あたりの溶質の物質量。溶液の質量から溶質の質量を引いて溶媒の質量を求める。",
                    [f"溶媒：${dec(tot)}-{dec(w)}={W}$ g。", f"$m=\\dfrac{{{dec(w / Mf)}}}{{{dec(sp.Rational(W, 1000))}}}={sig(m)}$ mol/kg。", f"$\\Delta t_{{\\mathrm{{b}}}}={sig(KB_W * m)}$ K。"],
                    "質量モル濃度の定義（溶質 mol ÷ 溶媒 kg）に戻って分母を確認する。",
                    ["溶質の質量が小さい希薄溶液では差が小さく見逃しやすいが、定義どおりに計算する。"], ["溶液の質量で割る。"],
                    chk=(f"0.52*{w}/({Mf})/({W}/1000)", str(KB_W * m), None, "intermediate"), d=3)


@gen("error_correction", 3, ["common_error", "condition_check"])
def err_vapor(r):
    if r.random() < 0.55:
        t = r.choice(VP_T)
        T = kelvin(t)
        pv = water_vp(t)
        for _ in range(50):
            V = sp.Rational(r.choice(["8.3", "4.15", "2.0", "5.0", "10"]))
            n = sp.Rational(r.choice(["0.10", "0.050", "0.20", "0.040"]))
            pall = n * R_ * T / V
            if pall > pv * 2:
                break
        return err_item(f"容積 {dec(V)} L の真空容器に水 {dec(n)} mol を入れ、{t} ℃ に保ったときの容器内の圧力を求めなさい。{t} ℃ の水の飽和蒸気圧は ${sci(pv)}$ Pa とし、液体の体積は無視する。{RTXT}",
                        f"$p=\\dfrac{{nRT}}{{V}}=\\dfrac{{{dec(n)}\\times8.3\\times10^{{3}}\\times{T}}}{{{dec(V)}}}={sig(pall)}$ Pa",
                        "状態方程式で求めた値をそのまま答えた部分", "condition",
                        "状態方程式は気体についての式であることを忘れ、入れた水がすべて気体になると無条件に仮定している。",
                        f"${sig(pall)}$ Pa は飽和蒸気圧 ${sci(pv)}$ Pa をこえるので液体が残り、圧力は ${sci(pv)}$ Pa", f"${sci(pv)}$ Pa",
                        "水蒸気の圧力は飽和蒸気圧をこえられない。すべて気体と仮定した値が飽和蒸気圧より大きければ、一部が凝縮して蒸気の圧力は飽和蒸気圧になる。",
                        [f"すべて気体と仮定すると ${sig(pall)}$ Pa。", f"飽和蒸気圧 ${sci(pv)}$ Pa と比べると大きい。", f"液体が共存するので ${sci(pv)}$ Pa。"],
                        "状態方程式で圧力を出したら、必ず飽和蒸気圧と比べる。",
                        [f"逆に、気体として存在できる最大量 $\\dfrac{{{sci(pv)}\\times{dec(V)}}}{{8.3\\times10^{{3}}\\times{T}}}$ mol を求め、{dec(n)} mol より少ないことを確かめる。"],
                        ["飽和蒸気圧との比較を忘れる。"], chk=(f"Min({n}*8.3*10**3*{T}/({V}), {pv})", str(pv), None, "intermediate"), d=3)
    nm_, f, Mf, gas, eq, k, how = RXN_W[r.choice([0, 1])]
    t = r.choice(list(WVP))
    T = kelvin(t)
    pvs, pv = pa(WVP[t], 3)
    pt = sp.Rational("1.01") * 10 ** 5
    Vml = r.choice([249, 415, 332, 166, 498, 581])
    wrong = pt * sp.Rational(Vml, 1000) / (R_ * T)
    right = (pt - pv) * sp.Rational(Vml, 1000) / (R_ * T)
    sci_ = lambda x: sci(x, 3)  # noqa: E731
    return err_item(f"{nm_}に希塩酸を加えて発生した水素を水上置換で集め、水面をそろえて体積を測ると {t} ℃ で {Vml} mL であった。大気圧は $1.01\\times10^{{5}}$ Pa、{t} ℃ の水の飽和蒸気圧は ${pvs}$ Pa とする。"
                    f"集めた水素の物質量を有効数字3桁で求めなさい。{RTXT}",
                    f"$n=\\dfrac{{1.01\\times10^{{5}}\\times{dec(sp.Rational(Vml, 1000))}}}{{8.3\\times10^{{3}}\\times{T}}}\\fallingdotseq{sci_(wrong)}$ mol",
                    "水素の圧力を大気圧とした部分", "condition",
                    "「水面をそろえたので圧力は大気圧」という手順は覚えているが、捕集した気体が水蒸気との混合気体であることを見落としている。",
                    f"水素の分圧は $1.01\\times10^{{5}}-{pvs}$ Pa なので $n\\fallingdotseq{sci_(right)}$ mol", f"${sci_(right)}$ mol",
                    "水上置換で集めた気体には飽和水蒸気が含まれる。大気圧＝水素の分圧＋水の飽和蒸気圧。",
                    [f"水素の分圧：$1.01\\times10^{{5}}-{pvs}={sig(pt - pv, 3)}$ Pa。", f"$n=\\dfrac{{{sig(pt - pv, 3)}\\times{dec(sp.Rational(Vml, 1000))}}}{{8.3\\times10^{{3}}\\times{T}}}\\fallingdotseq{sci_(right)}$ mol。"],
                    "水上置換では「全圧＝大気圧」「目的の気体の分圧＝大気圧−水蒸気圧」の2段階で考える。",
                    ["分圧の法則の式 $p_{\\text{全}}=p_{\\mathrm{H_2}}+p_{\\mathrm{H_2O}}$ を先に書いてから代入する。"], ["水蒸気圧を引き忘れる。"],
                    chk=(f"({pt}-{pv})*{Vml}/1000/(8.3*10**3*{T})", str(right), None, "intermediate"), d=3)


GENERATORS = [boyle_charles, ideal_gas, partial_pressure, vapor_concept, colligative_basic,
              dumas, mixing, vapor_container, osmotic, colligative_compare, molar_mass_fp,
              over_water, cooling_curve, henry, real_gas,
              err_units, err_colligative, err_vapor]
