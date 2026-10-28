"""単元パック：化学基礎 物質量と化学反応式（物質量・モル濃度・化学反応の量的関係）。"""
import re
from decimal import ROUND_HALF_UP, Decimal

import sympy as sp

from banks._common import desc, num, sa, table
from hs_pack_lib import board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem, tp

UNIT_ID = "HS-CHEB-U02"

AW = {"H": "1.0", "C": "12", "N": "14", "O": "16", "Na": "23", "Mg": "24", "Al": "27", "S": "32", "Cl": "35.5", "K": "39", "Ca": "40",
      "Fe": "56", "Cu": "64", "Zn": "65"}
NA = sp.Rational("6.0") * sp.Integer(10) ** 23
VM = sp.Rational("22.4")
STP = "標準状態（0 ℃、$1.013\\times10^5$ Pa）"


# ----------------------------------------------------------------------
# 化学式・数値の補助
# ----------------------------------------------------------------------

def parse(f):
    """'Ca(OH)2' → {'Ca':1,'O':2,'H':2}"""
    def grp(s, i):
        out = {}
        while i < len(s):
            if s[i] == "(":
                sub, i = grp(s, i + 1)
                m = re.match(r"\d+", s[i:])
                k = int(m.group()) if m else 1
                i += len(m.group()) if m else 0
                for e, c in sub.items():
                    out[e] = out.get(e, 0) + c * k
            elif s[i] == ")":
                return out, i + 1
            else:
                m = re.match(r"([A-Z][a-z]?)(\d*)", s[i:])
                out[m.group(1)] = out.get(m.group(1), 0) + int(m.group(2) or 1)
                i += len(m.group())
        return out, i
    return grp(f, 0)[0]


def M(f):
    return sum((sp.Rational(AW[e]) * c for e, c in parse(f).items()), sp.Integer(0))


def M_expr(f):
    return "+".join(f"{AW[e]}*{c}" if c > 1 else AW[e] for e, c in parse(f).items())


def tex(f):
    return "\\mathrm{" + re.sub(r"(\d+)", lambda m: "_" + (m.group(1) if len(m.group(1)) == 1 else "{" + m.group(1) + "}"), f) + "}"


def aw_note(*fs):
    els = []
    for f in fs:
        for e in parse(f):
            if e not in els:
                els.append(e)
    order = list(AW)
    els.sort(key=order.index)
    return "原子量は " + "、".join(f"{e}＝{AW[e]}" for e in els) + " とする。"


def dec(x):
    x = sp.Rational(x)
    d = Decimal(int(x.p)) / Decimal(int(x.q))
    dn = d.normalize()
    if len(dn.as_tuple().digits) == 1 and abs(d) < 10:
        dn = d.quantize(Decimal(1).scaleb(dn.adjusted() - 1))
    return format(dn, "f")


def clean(x, digits=3):
    """有限小数で、有効数字 digits 桁以内に収まるか。"""
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


NAMES = {"H2O": "水", "CO2": "二酸化炭素", "NH3": "アンモニア", "CH4": "メタン", "O2": "酸素", "N2": "窒素", "H2": "水素", "NaCl": "塩化ナトリウム",
         "NaOH": "水酸化ナトリウム", "CaCO3": "炭酸カルシウム", "H2SO4": "硫酸", "HCl": "塩化水素", "C6H12O6": "グルコース", "C2H6O": "エタノール",
         "C3H8": "プロパン", "Ca(OH)2": "水酸化カルシウム", "KOH": "水酸化カリウム", "MgO": "酸化マグネシウム", "Na2CO3": "炭酸ナトリウム",
         "Mg": "マグネシウム", "Al": "アルミニウム", "Fe": "鉄", "Zn": "亜鉛", "Cu": "銅", "C2H6": "エタン", "AlCl3": "塩化アルミニウム",
         "ZnCl2": "塩化亜鉛", "MgCl2": "塩化マグネシウム", "CaCl2": "塩化カルシウム", "H2O2": "過酸化水素", "Na": "ナトリウム", "KClO3": "塩素酸カリウム",
         "KCl": "塩化カリウム", "Al2O3": "酸化アルミニウム", "FeCl2": "塩化鉄(Ⅱ)", "CuO": "酸化銅(Ⅱ)", "Cl2": "塩素", "KNO3": "硝酸カリウム",
         "CuSO4": "硫酸銅(Ⅱ)", "C12H22O11": "スクロース", "C2H4": "エチレン", "NaHCO3": "炭酸水素ナトリウム"}
GASES = {"CO2", "NH3", "CH4", "O2", "N2", "H2", "C3H8", "C2H6", "Cl2", "C2H4"}


def nm(f):
    return f"{NAMES[f]} ${tex(f)}$"


# 化学反応式（係数, 化学式）
RXN = [
    [(1, "CH4"), (2, "O2"), None, (1, "CO2"), (2, "H2O")],
    [(1, "C3H8"), (5, "O2"), None, (3, "CO2"), (4, "H2O")],
    [(2, "H2"), (1, "O2"), None, (2, "H2O")],
    [(2, "C2H6"), (7, "O2"), None, (4, "CO2"), (6, "H2O")],
    [(1, "C2H6O"), (3, "O2"), None, (2, "CO2"), (3, "H2O")],
    [(2, "Al"), (6, "HCl"), None, (2, "AlCl3"), (3, "H2")],
    [(1, "Zn"), (2, "HCl"), None, (1, "ZnCl2"), (1, "H2")],
    [(1, "Mg"), (2, "HCl"), None, (1, "MgCl2"), (1, "H2")],
    [(4, "Al"), (3, "O2"), None, (2, "Al2O3")],
    [(1, "N2"), (3, "H2"), None, (2, "NH3")],
    [(1, "CaCO3"), (2, "HCl"), None, (1, "CaCl2"), (1, "H2O"), (1, "CO2")],
    [(2, "H2O2"), None, (2, "H2O"), (1, "O2")],
    [(1, "C6H12O6"), (6, "O2"), None, (6, "CO2"), (6, "H2O")],
    [(2, "Na"), (2, "H2O"), None, (2, "NaOH"), (1, "H2")],
    [(2, "KClO3"), None, (2, "KCl"), (3, "O2")],
    [(2, "Cu"), (1, "O2"), None, (2, "CuO")],
    [(2, "Mg"), (1, "O2"), None, (2, "MgO")],
    [(1, "C2H4"), (3, "O2"), None, (2, "CO2"), (2, "H2O")],
    [(1, "Fe"), (2, "HCl"), None, (1, "FeCl2"), (1, "H2")],
]


def sides(rx):
    k = rx.index(None)
    return rx[:k], rx[k + 1:]


def eq_tex(rx, blanks=False):
    lhs, rhs = sides(rx)

    def term(c, f):
        if blanks:
            return f"\\square\\,{tex(f)}"
        return (str(c) if c > 1 else "") + tex(f)
    return "+".join(term(*t) for t in lhs) + "\\longrightarrow " + "+".join(term(*t) for t in rhs)


def species(rx):
    return [t for t in rx if t]


# ======================================================================
# 授業プリント
# ======================================================================

LESSON = lesson(
    goals=["物質量（mol）とアボガドロ定数・モル質量・モル体積の関係を理解し、粒子の数・質量・気体の体積を相互に換算できる。",
           "モル濃度・質量パーセント濃度の意味を説明し、溶液の調製や希釈の計算ができる。",
           "化学反応式の係数が物質量の比を表すことを説明し、反応物・生成物の量的関係（過不足を含む）を求められる。"],
    duration=100,
    readiness=["原子の構造・原子量の意味（前単元）と、化学式から構成原子の数を読み取れる。",
               "中学校で学んだ化学反応式の書き方と質量保存の法則を説明できる。",
               "比例式・小数の計算・指数（$10^{23}$ など）の扱いができる。"],
    flow=[("導入：粒子を「まとめて数える」", 8, "鉛筆の「ダース」や紙の「連」を例に、膨大な数の粒子を束で数える必要性を示す"),
          ("物質量とアボガドロ定数", 15, "1 mol の定義、粒子の数との換算"),
          ("モル質量とモル体積", 20, "原子量・分子量・式量からモル質量へ、標準状態の気体 22.4 L/mol"),
          ("溶液の濃度", 17, "モル濃度・質量パーセント濃度、溶液の調製と希釈"),
          ("化学反応式と量的関係", 25, "係数＝物質量の比の導出、質量・体積の計算、過不足のある反応"),
          ("演習とまとめ", 15, "例題の解説、確認問題、問題プリントの課題指示")],
    sections=[
        intro("in1", "目に見えない粒子を「量」として扱う",
              "水 18 g の中には約 $6.0\\times10^{23}$ 個もの水分子がある。このように膨大な数の粒子を1個ずつ数えるのは不可能なので、化学では $6.02\\times10^{23}$ 個をひとまとまりとして扱う。"
              "このひとまとまりを単位にした量が物質量（単位 mol）である。物質量を使うと、粒子の数・質量・気体の体積・溶液の濃度を同じものさしで結びつけられる。",
              bullets=["化学反応式の係数は、反応する粒子の数の比であり、同時に物質量の比でもある。",
                       "この単元の計算は、中和（酸と塩基）・酸化還元の量的関係や、気体の法則・反応エンタルピーへと直接つながる。"],
              points=[tp("「1ダース＝12本」と同じように、「1 mol＝$6.0\\times10^{23}$ 個」は数の束であることを強調し、単位をそろえる感覚をもたせる。",
                         ask="米粒を1粒ずつ数えずに「何粒あるか」を知るにはどうすればよいか。", expect="100粒の質量を量って、全体の質量から割り出す。",
                         timing="授業の冒頭")]),
        definition("df1", "物質量とアボガドロ定数",
                   "$6.02214076\\times10^{23}$ 個の粒子の集団を 1 mol とし、mol を単位として表した粒子の量を物質量という。1 mol あたりの粒子の数をアボガドロ定数 $N_{\\mathrm{A}}$ という。",
                   formula="$$n\\,[\\mathrm{mol}]=\\dfrac{N\\,[\\text{個}]}{N_{\\mathrm{A}}\\,[/\\mathrm{mol}]},\\qquad N_{\\mathrm{A}}\\fallingdotseq6.0\\times10^{23}\\ /\\mathrm{mol}$$",
                   conditions=["何の粒子（原子・分子・イオン）の物質量かを必ず明示する。例：$\\mathrm{CO_2}$ 1 mol には O 原子が 2 mol 含まれる。",
                               "問題文で与えられた値（$6.0\\times10^{23}$ /mol など）を使う。"],
                   points=[tp("粒子の種類を言わずに「1 mol」と言わせない。$\\mathrm{H_2O}$ 1 mol 中の H 原子・O 原子・電子の物質量を言わせる練習をする。",
                              ask="$\\mathrm{H_2O}$ 0.50 mol に含まれる H 原子は何 mol か。", expect="1.0 mol")]),
        definition("df2", "モル質量・モル体積・モル濃度",
                   "1 mol あたりの質量をモル質量（g/mol）という。モル質量の数値は、原子量・分子量・式量に g/mol をつけたものに等しい。"
                   "気体 1 mol の体積をモル体積といい、標準状態（0 ℃、$1.013\\times10^5$ Pa）では気体の種類によらず約 22.4 L/mol である。"
                   "溶液 1 L あたりに溶けている溶質の物質量をモル濃度（mol/L）という。",
                   formula="$$n=\\dfrac{w\\,[\\mathrm{g}]}{M\\,[\\mathrm{g/mol}]},\\qquad n=\\dfrac{V\\,[\\mathrm{L}]}{22.4\\,[\\mathrm{L/mol}]}\\ (\\text{標準状態の気体}),\\qquad c\\,[\\mathrm{mol/L}]=\\dfrac{n\\,[\\mathrm{mol}]}{V_{\\text{溶液}}\\,[\\mathrm{L}]}$$",
                   conditions=["22.4 L/mol は標準状態の気体にだけ使える。0 ℃ の水やエタノールのような液体・固体には使えない。",
                               "モル濃度の分母は溶液の体積であり、溶媒（水）の体積ではない。",
                               "質量パーセント濃度＝溶質の質量÷溶液の質量×100。モル濃度に直すには、溶液 1 L の質量（密度×1000 mL）から考える。"],
                   points=[tp("3つの式を「物質量を中心にした換算図」（粒子数・質量・体積・濃度×体積が mol を介してつながる図）として板書する。",
                              caution="mL を L に直し忘れる誤りが非常に多い。単位をつけたまま計算させる。")]),
        derivation("dv1", "化学反応式の係数が物質量の比を表す理由",
                   ["$2\\mathrm{H_2}+\\mathrm{O_2}\\longrightarrow2\\mathrm{H_2O}$ は「$\\mathrm{H_2}$ 分子 2 個と $\\mathrm{O_2}$ 分子 1 個が反応して $\\mathrm{H_2O}$ 分子 2 個ができる」ことを表す。",
                    "粒子の数を $N_{\\mathrm{A}}$ 倍しても比は変わらないので、「$\\mathrm{H_2}$ 2 mol と $\\mathrm{O_2}$ 1 mol から $\\mathrm{H_2O}$ 2 mol」と読める。よって係数の比＝物質量の比。",
                    "質量に直すと $2\\times2.0=4.0$ g と $1\\times32=32$ g から $2\\times18=36$ g。$4.0+32=36$ で質量保存の法則も成り立つ。",
                    "標準状態の気体どうしなら体積も物質量に比例するので、係数の比＝気体の体積の比（$\\mathrm{H_2}$ 44.8 L と $\\mathrm{O_2}$ 22.4 L）。",
                    "ただし、係数の比は質量の比ではない（$\\mathrm{H_2}:\\mathrm{O_2}$ の質量比は $4.0:32=1:8$）。"],
                   body="量的関係の計算は、どんな問題でも「与えられた量 → 物質量 → 係数の比 → 求める物質の物質量 → 求める量」の順に進める。",
                   points=[tp("係数の比が「質量の比」ではないことを、上の数値で確かめさせる。", ask="水素 4.0 g と反応する酸素は何 g か。", expect="2.0 mol の半分の 1.0 mol なので 32 g。")]),
        theorem("th1", "量的関係の計算手順と過不足",
                "$$\\text{与えられた量}\\ \\xrightarrow{\\ \\div M,\\ \\div22.4,\\ \\times c\\ }\\ \\text{物質量}\\ \\xrightarrow{\\ \\times\\frac{\\text{係数}}{\\text{係数}}\\ }\\ \\text{求める物質の物質量}\\ \\xrightarrow{\\ \\times M,\\ \\times22.4\\ }\\ \\text{求める量}$$",
                ["反応物が2種類とも量で与えられたときは、どちらが過不足なく反応し、どちらが余るかを先に判定する。",
                 "生成物の量は、不足する方（すべて反応する方）の物質量で決まる。",
                 "溶液どうしの反応では、溶質の物質量＝モル濃度×溶液の体積（L）。"],
                proof=["$a\\mathrm{A}+b\\mathrm{B}\\longrightarrow\\cdots$ で A が $n_{\\mathrm{A}}$ mol、B が $n_{\\mathrm{B}}$ mol あるとする。",
                       "A がすべて反応するのに必要な B は $\\dfrac{b}{a}n_{\\mathrm{A}}$ mol。",
                       "$n_{\\mathrm{B}}>\\dfrac{b}{a}n_{\\mathrm{A}}$ なら B が余り、A がすべて反応する。逆なら A が余る。",
                       "生成物の物質量は、すべて反応する方の物質量と係数の比から求まる。"],
                points=[tp("過不足の判定は「一方がすべて反応すると仮定して、もう一方が足りるか」を調べる方法に統一する。", timing="例題3の前")]),
        example("ex1", "例題1　質量・粒子の数・体積の換算",
                "二酸化炭素 $\\mathrm{CO_2}$ 11 g について、(1) 物質量、(2) 分子の数、(3) 標準状態での体積を求めよ。原子量は C＝12、O＝16、アボガドロ定数は $6.0\\times10^{23}$ /mol とする。",
                ["分子量は $12+16\\times2=44$、モル質量 44 g/mol。", "(1) $\\dfrac{11}{44}=0.25$ mol。", "(2) $0.25\\times6.0\\times10^{23}=1.5\\times10^{23}$ 個。",
                 "(3) $0.25\\times22.4=5.6$ L。"],
                "(1) 0.25 mol　(2) $1.5\\times10^{23}$ 個　(3) 5.6 L", thinking="まず物質量に直し、そこから粒子の数・体積へ換算する。",
                points=[tp("どの換算も「物質量を経由する」ことを、換算図の矢印でたどらせる。")]),
        example("ex2", "例題2　溶液の調製と希釈",
                "水酸化ナトリウム NaOH（式量 40）を用いて 0.20 mol/L の水溶液を 250 mL つくりたい。NaOH は何 g 必要か。また、この水溶液 10 mL を水でうすめて全体を 100 mL にすると、モル濃度はいくらになるか。",
                ["必要な NaOH の物質量：$0.20\\times\\dfrac{250}{1000}=0.050$ mol。", "質量：$0.050\\times40=2.0$ g。",
                 "希釈しても溶質の物質量は変わらない：$0.20\\times\\dfrac{10}{1000}=2.0\\times10^{-3}$ mol。", "うすめた後：$\\dfrac{2.0\\times10^{-3}}{0.100}=0.020$ mol/L。"],
                "2.0 g、0.020 mol/L", thinking="溶質の物質量＝モル濃度×溶液の体積（L）。希釈の前後で溶質の物質量は一定。",
                misconceptions=[("NaOH 2.0 g を水 250 mL に溶かせばよい", "溶かしてからメスフラスコで全体を 250 mL にする（溶液の体積を 250 mL にする）")]),
        example("ex3", "例題3　過不足のある反応",
                "マグネシウム 0.36 g に 1.0 mol/L の塩酸 20 mL を加えた。発生する水素の標準状態での体積は何 mL か。$\\mathrm{Mg}+2\\mathrm{HCl}\\longrightarrow\\mathrm{MgCl_2}+\\mathrm{H_2}$、原子量は Mg＝24 とする。",
                ["Mg：$\\dfrac{0.36}{24}=0.015$ mol。HCl：$1.0\\times\\dfrac{20}{1000}=0.020$ mol。",
                 "Mg 0.015 mol がすべて反応するには HCl が 0.030 mol 必要 → HCl が不足。HCl 0.020 mol がすべて反応する（Mg は 0.010 mol 反応し、0.005 mol 余る）。",
                 "$\\mathrm{H_2}$ は HCl の $\\dfrac12$ で 0.010 mol。", "体積：$0.010\\times22.4=0.224$ L＝224 mL。"],
                "224 mL", thinking="両方の量が与えられている → 先に過不足を判定する。",
                misconceptions=[("Mg 0.015 mol から $\\mathrm{H_2}$ 0.015 mol（336 mL）", "HCl が不足するので、生成量は HCl の量で決まる")],
                points=[tp("過不足の判定をとばして Mg の量だけで計算する誤答を、あえて板書して比較させる。",
                           ask="もし塩酸が 40 mL なら、発生する水素は何 mL になるか。", expect="HCl 0.040 mol で Mg がすべて反応し、0.015 mol＝336 mL。")]),
        board("bd1", "板書案",
              [("① 物質量を中心に", ["粒子数 $N=n\\times N_{\\mathrm{A}}$", "質量 $w=n\\times M$", "気体 $V=n\\times22.4$ L（標準状態）", "溶質 $n=c\\times V$（L）",
                                    "何の粒子の mol かを明示"]),
               ("② 溶液の濃度", ["モル濃度＝溶質 mol ÷ 溶液 L", "質量％＝溶質 g ÷ 溶液 g ×100", "調製：溶かしてからメスフラスコで定容", "希釈：溶質の mol は一定",
                                "$c_1V_1=c_2V_2$"]),
               ("③ 反応の量的関係", ["係数の比＝物質量の比", "（気体の体積比にもなる）", "係数の比 ≠ 質量の比", "過不足：一方が全部反応と仮定",
                                     "生成量は不足する方で決まる"])]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("計算の途中で必ず単位を書かせ、mL→L、g→mol の換算ミスを単位の約分で発見できるようにする。",
                  caution="$c\\times V$ で mL のまま掛けて 1000 倍の答えを出す誤りが最も多い。"),
               tp("22.4 L/mol は「標準状態の気体」専用であることを、0 ℃ の水 1 mol（18 g、約 18 mL）と比べて実感させる。",
                  ask="水 1 mol の体積は 22.4 L か。", expect="液体なので約 18 mL。22.4 L は使えない。"),
               tp("過不足の問題では、表（反応前・変化量・反応後）を書かせると、余る物質の量まで一度に整理できる。", timing="例題3の解説時"),
               tp("有効数字は「与えられた数値の桁数に合わせる」ことを基本とし、問題文で指定があればそれに従わせる。")],
              misconceptions=[("係数の比は質量の比である", "係数の比は物質量（粒子の数）の比。質量の比にはモル質量をかける必要がある"),
                              ("1.0 mol/L の溶液は、溶質 1.0 mol を水 1.0 L に溶かしてつくる", "溶液全体の体積を 1.0 L にする。溶媒 1.0 L に溶かすと溶液は 1.0 L にならない"),
                              ("どんな物質でも 1 mol は 22.4 L", "22.4 L/mol は標準状態の気体だけ")]),
        summary("sm1", "まとめ", ["物質量（mol）は粒子の数を $6.0\\times10^{23}$ 個ずつの束で数えた量。質量・気体の体積・溶液の濃度は物質量を介して換算できる。",
                                   "モル濃度は溶液 1 L あたりの溶質の物質量。調製はメスフラスコで、希釈では溶質の物質量が保たれる。",
                                   "化学反応式の係数の比は物質量の比（気体なら体積の比）。量的関係は物質量に直して係数の比を使い、過不足があれば不足する方で生成量が決まる。"]),
        check("ck1", "確認問題", [("メタン $\\mathrm{CH_4}$（分子量 16）4.0 g の物質量は？", "0.25 mol"),
                                  ("標準状態で 2.24 L の酸素の物質量は？", "0.100 mol"),
                                  ("0.50 mol/L の塩化ナトリウム水溶液 200 mL に含まれる NaCl の物質量は？", "0.10 mol"),
                                  ("$2\\mathrm{H_2}+\\mathrm{O_2}\\longrightarrow2\\mathrm{H_2O}$ で、$\\mathrm{O_2}$ 0.30 mol と反応する $\\mathrm{H_2}$ は？", "0.60 mol")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

CMP = ["H2O", "CO2", "NH3", "CH4", "O2", "N2", "NaCl", "NaOH", "CaCO3", "H2SO4", "HCl", "C6H12O6", "C2H6O", "C3H8", "Ca(OH)2", "KOH", "MgO",
       "Na2CO3", "Mg", "Al", "Fe", "Cu", "KNO3", "C12H22O11", "NaHCO3"]
NS = ["0.10", "0.20", "0.25", "0.30", "0.40", "0.50", "0.60", "0.75", "0.80", "1.5", "2.0", "2.5", "0.050", "0.020"]


def pick_clean(r, f, digits=3, pool=NS):
    for _ in range(100):
        n = sp.Rational(r.choice(pool))
        w = n * M(f)
        if clean(w, digits):
            return n, w
    return sp.Rational("0.10"), sp.Rational("0.10") * M(f)


@gen("basic_check", 5, ["computation", "concept"])
def mass_mol(r):
    f = r.choice(CMP)
    Mf = M(f)
    kind = "粒子" if f in ("Mg", "Al", "Fe", "Cu") else ("式量" if f in ("NaCl", "NaOH", "CaCO3", "Ca(OH)2", "KOH", "MgO", "Na2CO3", "KNO3", "NaHCO3") else "分子量")
    unit_word = "原子量" if kind == "粒子" else kind
    n, w = pick_clean(r, f)
    form = r.choice(["m2n", "n2m", "M"])
    if form == "M":
        return numq(f"{nm(f)}の{unit_word}を求めなさい。{aw_note(f)}", Mf, M_expr(f), f"構成原子の原子量の和：{dec(Mf)}。", d=1, n=max(2, len(Decimal(dec(Mf)).normalize().as_tuple().digits)),
                    ap="化学式に含まれる各原子の原子量に、その原子の数をかけて足し合わせる。",
                    steps=["化学式から各原子の数を読み取る。" + ("かっこの外の数字は、かっこ内の原子すべてにかかる。" if "(" in f else ""), f"原子量×個数の和を計算して {dec(Mf)}。"],
                    alt=["モル質量（g/mol）として答えるときは、同じ数値に単位 g/mol をつける。"],
                    pc=[("原子の数を正しく読み取っている", 1), ("値が正しい", 1)], pit=["添字やかっこの外の数字を掛け忘れる。"])
    if form == "m2n":
        return numq(f"{nm(f)} {dec(w)} g の物質量は何 mol か。{aw_note(f)}", n, f"{dec(w)}/({M_expr(f)})",
                    f"モル質量 {dec(Mf)} g/mol。$\\dfrac{{{dec(w)}}}{{{dec(Mf)}}}={sig(n)}$（mol）。", unit="mol", d=1,
                    ap="物質量＝質量÷モル質量。モル質量は式量・分子量（原子量）に g/mol をつけたもの。",
                    steps=[f"モル質量は {dec(Mf)} g/mol。", f"$n=\\dfrac{{{dec(w)}\\,\\mathrm{{g}}}}{{{dec(Mf)}\\,\\mathrm{{g/mol}}}}={sig(n)}$ mol。"],
                    alt=[f"比例で考える：1 mol が {dec(Mf)} g なので、{dec(w)} g は $\\dfrac{{{dec(w)}}}{{{dec(Mf)}}}$ mol。"],
                    pc=[("モル質量を正しく求めている", 1), ("物質量が正しい", 1)], pit=["質量÷モル質量を逆に割る。"])
    return numq(f"{nm(f)} {dec(n)} mol の質量は何 g か。{aw_note(f)}", w, f"{dec(n)}*({M_expr(f)})",
                f"$w=nM={dec(n)}\\times{dec(Mf)}={dec(w)}$（g）。", unit="g", d=1, n=max(2, len(Decimal(dec(w)).normalize().as_tuple().digits)),
                ap="質量＝物質量×モル質量。",
                steps=[f"モル質量は {dec(Mf)} g/mol。", f"$w={dec(n)}\\,\\mathrm{{mol}}\\times{dec(Mf)}\\,\\mathrm{{g/mol}}={dec(w)}$ g。"],
                alt=["単位で確かめる：mol × g/mol ＝ g となり、求める量の単位になっている。"],
                pc=[("モル質量を正しく求めている", 1), ("質量が正しい", 1)], pit=["分子量を求めるときに原子の個数を掛け忘れる。"])


ATOMS_IN = [("CO2", "O", 2), ("H2O", "H", 2), ("NH3", "H", 3), ("CH4", "H", 4), ("H2SO4", "O", 4), ("C6H12O6", "C", 6), ("C3H8", "H", 8), ("N2", "N", 2),
            ("C2H6O", "H", 6), ("CaCl2", "Cl", 2)]


@gen("basic_check", 4, ["computation", "concept"])
def particles(r):
    form = r.choice(["n2N", "N2n", "atom"])
    if form == "atom":
        f, a, k = r.choice(ATOMS_IN)
        n = sp.Rational(r.choice(["0.10", "0.20", "0.25", "0.50", "1.5", "2.0", "0.30"]))
        N = n * k * NA
        word = "塩化物イオン $\\mathrm{Cl^-}$" if f == "CaCl2" else f" {a} 原子"
        return numq(f"{nm(f)} {dec(n)} mol に含まれる{word}の数は何個か。アボガドロ定数を $6.0\\times10^{{23}}$ /mol とし、有効数字2桁で答えなさい。",
                    N, f"{dec(n)}*{k}*6.0*10**23", f"1個の{'組成' if f == 'CaCl2' else '分子'}に {a} が {k} 個含まれるので、{a} の物質量は ${dec(n)}\\times{k}={dec(n * k)}$ mol。", unit="個", d=2,
                    ap="まず「何の粒子の物質量か」を考える。化学式1つあたりの原子の数をかけてから、アボガドロ定数をかける。",
                    steps=[f"{a} の物質量：${dec(n)}\\times{k}={dec(n * k)}$ mol。", f"個数：${dec(n * k)}\\times6.0\\times10^{{23}}={sig(N)}$ 個。"],
                    alt=[f"先に分子（組成式）の数 ${sig(n * NA)}$ 個を求め、{k} 倍してもよい。"],
                    pc=[("原子の物質量を正しく求めている", 1), ("個数が正しい", 1)], pit=["化学式1つあたりの原子の数を掛け忘れる。"])
    f = r.choice(["H2O", "CO2", "NH3", "CH4", "O2", "N2", "HCl", "C6H12O6"])
    if form == "n2N":
        n = sp.Rational(r.choice(["0.10", "0.20", "0.25", "0.40", "0.50", "1.5", "2.5", "0.030", "3.0"]))
        N = n * NA
        return numq(f"{nm(f)} {dec(n)} mol に含まれる分子の数は何個か。アボガドロ定数を $6.0\\times10^{{23}}$ /mol とし、有効数字2桁で答えなさい。", N, f"{dec(n)}*6.0*10**23",
                    f"$N=n\\times N_{{\\mathrm{{A}}}}={dec(n)}\\times6.0\\times10^{{23}}={sig(N)}$（個）。", unit="個", d=1,
                    ap="粒子の数＝物質量×アボガドロ定数。",
                    steps=[f"$N={dec(n)}\\,\\mathrm{{mol}}\\times6.0\\times10^{{23}}\\,/\\mathrm{{mol}}$。", f"$={sig(N)}$ 個。"],
                    alt=["指数の計算は「係数どうし」「10 の累乗どうし」に分けて計算すると誤りにくい。"],
                    pc=[("式が正しい", 1), ("値が正しい", 1)], pit=["係数が 10 以上になったときに指数を直し忘れる。"])
    k = r.choice(["1.2", "3.0", "4.5", "9.0", "1.5", "2.4", "6.0", "3.6", "1.8", "7.2"])
    e = r.choice([22, 23, 24])
    N = sp.Rational(k) * sp.Integer(10) ** e
    n = N / NA
    return numq(f"{nm(f)}の分子 ${k}\\times10^{{{e}}}$ 個の物質量は何 mol か。アボガドロ定数を $6.0\\times10^{{23}}$ /mol とする。", n, f"{k}*10**{e}/(6.0*10**23)",
                f"$n=\\dfrac{{{k}\\times10^{{{e}}}}}{{6.0\\times10^{{23}}}}={sig(n)}$（mol）。", unit="mol", d=2,
                ap="物質量＝粒子の数÷アボガドロ定数。",
                steps=[f"$n=\\dfrac{{{k}\\times10^{{{e}}}}}{{6.0\\times10^{{23}}}}$。", f"$={sig(n)}$ mol。"],
                alt=["$6.0\\times10^{23}$ 個が 1 mol なので、何倍にあたるかを考えてもよい。"],
                pc=[("式が正しい", 1), ("値が正しい", 1)], pit=["指数の引き算を誤る。"])


@gen("basic_check", 4, ["computation", "condition_check"])
def gas_volume(r):
    f = r.choice(sorted(GASES))
    form = r.choice(["n2V", "V2n", "w2V"])
    if form == "n2V":
        n = sp.Rational(r.choice(["0.10", "0.25", "0.50", "1.5", "2.0", "0.20", "0.050", "0.75", "3.0"]))
        V = n * VM
        return numq(f"{STP}で、{nm(f)} {dec(n)} mol の体積は何 L か。標準状態の気体のモル体積を 22.4 L/mol とする。", V, f"{dec(n)}*22.4",
                    f"$V={dec(n)}\\times22.4={dec(V)}$（L）。", unit="L", d=1, n=3,
                    ap="標準状態の気体では、体積＝物質量×22.4 L/mol。",
                    steps=[f"$V={dec(n)}\\,\\mathrm{{mol}}\\times22.4\\,\\mathrm{{L/mol}}$。", f"$={dec(V)}$ L。"],
                    alt=["気体の種類によらず、標準状態の気体 1 mol は 22.4 L なので比例で求めてもよい。"],
                    pc=[("式が正しい", 1), ("値が正しい", 1)], pit=["22.4 で割ってしまう。"])
    if form == "V2n":
        V = sp.Rational(r.choice(["1.12", "2.24", "4.48", "5.6", "11.2", "33.6", "0.448", "6.72", "8.96", "16.8"]))
        n = V / VM
        return numq(f"{STP}で {dec(V)} L を占める{NAMES[f]}の物質量は何 mol か。標準状態の気体のモル体積を 22.4 L/mol とする。", n, f"{dec(V)}/22.4",
                    f"$n=\\dfrac{{{dec(V)}}}{{22.4}}={sig(n)}$（mol）。", unit="mol", d=1,
                    ap="物質量＝体積÷22.4 L/mol（標準状態の気体）。",
                    steps=[f"$n=\\dfrac{{{dec(V)}\\,\\mathrm{{L}}}}{{22.4\\,\\mathrm{{L/mol}}}}$。", f"$={sig(n)}$ mol。"],
                    alt=["22.4 L が 1 mol なので、何倍・何分の1かを考えて暗算で確かめる。"],
                    pc=[("式が正しい", 1), ("値が正しい", 1)], pit=["気体の種類によってモル体積が変わると考える。"])
    n, w = pick_clean(r, f, 3, ["0.10", "0.20", "0.25", "0.50", "0.050", "1.5", "0.40"])
    V = n * VM
    return numq(f"{nm(f)} {dec(w)} g は、{STP}で何 L を占めるか。{aw_note(f)}標準状態の気体のモル体積を 22.4 L/mol とする。", V, f"{dec(w)}/({M_expr(f)})*22.4",
                f"物質量は $\\dfrac{{{dec(w)}}}{{{dec(M(f))}}}={dec(n)}$ mol。体積は ${dec(n)}\\times22.4={dec(V)}$ L。", unit="L", d=2, n=3,
                ap="質量 → 物質量 → 体積の順に、物質量を経由して換算する。",
                steps=[f"モル質量 {dec(M(f))} g/mol より $n={dec(n)}$ mol。", f"$V={dec(n)}\\times22.4={dec(V)}$ L。"],
                alt=[f"1 mol（{dec(M(f))} g）が 22.4 L という比例関係 ${dec(M(f))}:22.4={dec(w)}:V$ から求めてもよい。"],
                pc=[("物質量を正しく求めている", 1), ("体積が正しい", 1)], pit=["質量を直接 22.4 で割る。"])


SOLUTES = ["NaCl", "NaOH", "C6H12O6", "KNO3", "CuSO4", "C12H22O11", "Na2CO3", "KOH", "H2SO4"]


@gen("basic_check", 4, ["computation", "condition_check"])
def molarity(r):
    f = r.choice(SOLUTES)
    Vml = r.choice([100, 200, 250, 500, 1000])
    c = sp.Rational(r.choice(["0.10", "0.20", "0.50", "0.050", "1.0", "0.40", "0.25"]))
    n = c * sp.Rational(Vml, 1000)
    w = n * M(f)
    if not clean(w, 3):
        c, Vml = sp.Rational("0.10"), 500
        n = c * sp.Rational(Vml, 1000)
        w = n * M(f)
    if r.random() < 0.5:
        return numq(f"{nm(f)} {dec(w)} g を水に溶かして {Vml} mL の水溶液とした。この水溶液のモル濃度は何 mol/L か。{aw_note(f)}", c,
                    f"({dec(w)}/({M_expr(f)}))/({Vml}/1000)", f"溶質 $\\dfrac{{{dec(w)}}}{{{dec(M(f))}}}={dec(n)}$ mol を {Vml / 1000:g} L で割る。", unit="mol/L", d=2,
                    ap="モル濃度＝溶質の物質量（mol）÷溶液の体積（L）。体積は L に直す。",
                    steps=[f"溶質の物質量：$\\dfrac{{{dec(w)}}}{{{dec(M(f))}}}={dec(n)}$ mol。", f"溶液の体積：{Vml} mL＝{dec(sp.Rational(Vml, 1000))} L。",
                           f"$c=\\dfrac{{{dec(n)}}}{{{dec(sp.Rational(Vml, 1000))}}}={sig(c)}$ mol/L。"],
                    alt=["1 L あたりに換算する：1000 mL は " + f"{Vml} mL の {sp.Rational(1000, Vml)} 倍なので、溶質も同じ倍率でふやして考える。"],
                    pc=[("溶質の物質量を正しく求めている", 1), ("モル濃度が正しい", 1)], pit=["mL のまま割って 1000 分の1の値を答える。"])
    return numq(f"{sig(c)} mol/L の{NAMES[f]}水溶液を {Vml} mL つくるのに必要な{NAMES[f]} ${tex(f)}$ の質量は何 g か。{aw_note(f)}", w,
                f"{dec(c)}*{Vml}/1000*({M_expr(f)})", f"溶質の物質量 ${sig(c)}\\times{dec(sp.Rational(Vml, 1000))}={dec(n)}$ mol、質量 ${dec(n)}\\times{dec(M(f))}={dec(w)}$ g。",
                unit="g", d=2, n=max(2, min(3, len(Decimal(dec(w)).normalize().as_tuple().digits))),
                ap="必要な溶質の物質量＝モル濃度×溶液の体積（L）。それを質量に直す。",
                steps=[f"$n={sig(c)}\\,\\mathrm{{mol/L}}\\times{dec(sp.Rational(Vml, 1000))}\\,\\mathrm{{L}}={dec(n)}$ mol。", f"$w={dec(n)}\\times{dec(M(f))}={dec(w)}$ g。"],
                alt=["単位で確かめる：mol/L × L × g/mol ＝ g。"],
                pc=[("溶質の物質量を正しく求めている", 1), ("質量が正しい", 1)], pit=["体積を mL のまま掛ける。"])


def count_el(side):
    out = {}
    for c, f in side:
        for e, k in parse(f).items():
            out[e] = out.get(e, 0) + c * k
    return out


@gen("basic_check", 3, ["computation", "concept"])
def balance(r):
    rx = r.choice(RXN)
    sp_ = species(rx)
    coefs = [c for c, _ in sp_]
    names = "、".join(NAMES[f] for _, f in sp_)
    lhs, rhs = sides(rx)
    L, R = count_el(lhs), count_el(rhs)
    els = sorted(L)
    ans = "、".join(str(c) for c in coefs)
    lead = r.choice(["次の化学反応式の □ に係数を入れて、反応式を完成させなさい。係数が 1 のときも 1 と書き、左から順に答えなさい。",
                     "次の化学反応式の係数（□）を、最も簡単な整数比になるように左から順に答えなさい（1 も省略せずに書く）。"])
    return sa(f"{lead}\n$${eq_tex(rx, True)}$$", ans, f"完成した式：${eq_tex(rx)}$。", d=2,
              ap="最も複雑な化学式の係数を 1 とおき、両辺で各原子の数が等しくなるように順に決める（目算法）。分数になったら全体を整数倍する。",
              steps=[f"登場する物質：{names}。", "複雑な物質の係数を 1 とおき、その物質にしか含まれない原子から合わせていく。",
                     "O や H のように多くの物質に含まれる原子は最後に合わせる。", f"係数は {ans}。"],
              alt=["未定係数法：係数を $a,\\ b,\\ c,\\ \\dots$ とおき、原子ごとに等式を立てて解く。"],
              pc=[("原子の数を両辺で比べている", 1), ("係数がすべて正しい", 1)], pit=["化学式の添字を変えて数を合わせてしまう。", "最も簡単な整数比になっていない。"],
              chk=(f"[{', '.join(f'{L[e]}-{R[e]}' for e in els)}]", f"[{', '.join('0' for _ in els)}]", None, "intermediate"))


# ======================================================================
# B 標準演習
# ======================================================================

def stoich_pick(r, need_gas=None, given_not_solution=True):
    for _ in range(200):
        rx = r.choice(RXN)
        sp_ = species(rx)
        i, j = r.sample(range(len(sp_)), 2)
        ci, fi = sp_[i]
        cj, fj = sp_[j]
        if fi == "HCl" and given_not_solution:
            continue
        if need_gas is not None and (fj in GASES) != need_gas:
            continue
        return rx, (ci, fi), (cj, fj)
    raise RuntimeError


@gen("standard_practice", 5, ["computation", "application"])
def mass_mass(r):
    rx, (ci, fi), (cj, fj) = stoich_pick(r)
    ni, wi = pick_clean(r, fi, 3, ["0.10", "0.20", "0.25", "0.50", "0.050", "0.40", "1.0", "0.30", "0.60"])
    nj = ni * cj / ci
    wj = nj * M(fj)
    role = "反応する" if fj in [f for _, f in sides(rx)[0]] else "生成する"
    return numq(f"次の反応で、{nm(fi)} {dec(wi)} g が{'すべて反応する' if fi in [f for _, f in sides(rx)[0]] else '生成する'}とき、{role}{NAMES[fj]}の質量は何 g か。\n$${eq_tex(rx)}$$\n{aw_note(fi, fj)}",
                wj, f"{dec(wi)}/({M_expr(fi)})*{cj}/{ci}*({M_expr(fj)})",
                f"{NAMES[fi]} {dec(ni)} mol → 係数の比 {ci}:{cj} より {NAMES[fj]} ${sig(nj, 3)}$ mol → ${sig(wj)}$ g。", unit="g", d=3,
                ap="質量 → 物質量 → 係数の比 → 物質量 → 質量の順に換算する。係数の比は質量の比ではない。",
                steps=[f"{NAMES[fi]}の物質量：$\\dfrac{{{dec(wi)}}}{{{dec(M(fi))}}}={dec(ni)}$ mol。",
                       f"係数の比 ${NAMES[fi]}:{NAMES[fj]}={ci}:{cj}$ より、{NAMES[fj]}は ${dec(ni)}\\times\\dfrac{{{cj}}}{{{ci}}}={sig(nj, 3)}$ mol。",
                       f"質量：${sig(nj, 3)}\\times{dec(M(fj))}={sig(wj)}$ g。"],
                alt=[f"質量の比例式で解く：${ci}\\times{dec(M(fi))}\\,\\mathrm{{g}}:{cj}\\times{dec(M(fj))}\\,\\mathrm{{g}}={dec(wi)}\\,\\mathrm{{g}}:x\\,\\mathrm{{g}}$。"],
                pc=[("与えられた物質の物質量を求めている", 1), ("係数の比を正しく用いている", 2), ("質量が正しい", 1)],
                pit=["係数の比をそのまま質量の比として使う。", "係数を無視して 1:1 で計算する。"])


@gen("standard_practice", 4, ["computation", "application"])
def mass_gas(r):
    rx, (ci, fi), (cj, fj) = stoich_pick(r, need_gas=True)
    ni, wi = pick_clean(r, fi, 3, ["0.10", "0.20", "0.25", "0.50", "0.050", "0.40", "0.020", "0.30"])
    nj = ni * cj / ci
    V = nj * VM
    reac = fi in [f for _, f in sides(rx)[0]]
    return numq(f"次の反応で、{nm(fi)} {dec(wi)} g が{'すべて反応する' if reac else '生成する'}とき、{'生成する' if fj in [f for _, f in sides(rx)[1]] else '反応する'}{NAMES[fj]}の体積は{STP}で何 L か。\n$${eq_tex(rx)}$$\n{aw_note(fi)}標準状態の気体のモル体積を 22.4 L/mol とし、有効数字2桁で答えなさい。",
                V, f"{dec(wi)}/({M_expr(fi)})*{cj}/{ci}*22.4", f"{NAMES[fi]} {dec(ni)} mol → {NAMES[fj]} ${sig(nj, 3)}$ mol → ${sig(V)}$ L。", unit="L", d=3,
                ap="質量を物質量に直し、係数の比で気体の物質量を求めてから 22.4 L/mol をかける。",
                steps=[f"$n_{{\\text{{{NAMES[fi]}}}}}=\\dfrac{{{dec(wi)}}}{{{dec(M(fi))}}}={dec(ni)}$ mol。",
                       f"係数の比 {ci}:{cj} より $n_{{\\text{{{NAMES[fj]}}}}}={sig(nj, 3)}$ mol。", f"$V={sig(nj, 3)}\\times22.4={sig(V)}$ L。"],
                alt=[f"比例式 ${ci}\\times{dec(M(fi))}\\,\\mathrm{{g}}:{cj}\\times22.4\\,\\mathrm{{L}}={dec(wi)}\\,\\mathrm{{g}}:V$ でも求められる。"],
                pc=[("物質量を求めている", 1), ("係数の比を用いている", 2), ("体積が正しい", 1)],
                pit=["係数の比を使わずに、与えられた物質と同じ物質量として計算する。"])


@gen("standard_practice", 3, ["computation", "condition_check"])
def dilution(r):
    f = r.choice(["NaCl", "NaOH", "HCl", "H2SO4", "KNO3", "C6H12O6"])
    if r.random() < 0.55:
        c1 = sp.Rational(r.choice(["1.0", "2.0", "0.50", "0.10", "6.0", "3.0"]))
        V1 = r.choice([10, 20, 25, 50])
        V2 = r.choice([100, 200, 250, 500])
        c2 = c1 * V1 / V2
        return numq(f"{sig(c1)} mol/L の{'塩酸' if f == 'HCl' else NAMES[f] + '水溶液'} {V1} mL を正確にはかりとり、水を加えて全体を {V2} mL にした。うすめた後のモル濃度は何 mol/L か。", c2,
                    f"{dec(c1)}*{V1}/{V2}", f"$c_2=\\dfrac{{c_1V_1}}{{V_2}}=\\dfrac{{{sig(c1)}\\times{V1}}}{{{V2}}}={sig(c2)}$ mol/L。", unit="mol/L", d=2,
                    ap="水でうすめても、溶けている溶質の物質量は変わらない。",
                    steps=[f"溶質の物質量：${sig(c1)}\\times\\dfrac{{{V1}}}{{1000}}={sig(c1 * V1 / 1000)}$ mol。",
                           f"うすめた後：$\\dfrac{{{sig(c1 * V1 / 1000)}}}{{{dec(sp.Rational(V2, 1000))}}}={sig(c2)}$ mol/L。"],
                    alt=[f"体積が $\\dfrac{{{V2}}}{{{V1}}}$ 倍になったので、濃度は $\\dfrac{{{V1}}}{{{V2}}}$ 倍になる。"],
                    pc=[("溶質の物質量が一定であることを用いている", 2), ("値が正しい", 2)], pit=["加えた水の体積だけで割る。"])
    c1 = sp.Rational(r.choice(["0.10", "0.20", "0.50", "1.0"]))
    c2 = sp.Rational(r.choice(["0.30", "0.40", "0.60", "2.0"]))
    V1, V2 = r.choice([(100, 100), (100, 300), (200, 300), (150, 50), (100, 400), (250, 250)])
    c = (c1 * V1 + c2 * V2) / (V1 + V2)
    sol = "塩酸" if f == "HCl" else NAMES[f] + "水溶液"
    return numq(f"{sig(c1)} mol/L の{sol} {V1} mL と、{sig(c2)} mol/L の{sol} {V2} mL を混合した。混合後の水溶液のモル濃度は何 mol/L か。混合による体積の変化はないものとする。", c,
                f"({dec(c1)}*{V1}+{dec(c2)}*{V2})/({V1}+{V2})",
                f"溶質の合計 ${sig(c1 * V1 / 1000)}+{sig(c2 * V2 / 1000)}$ mol を {dec(sp.Rational(V1 + V2, 1000))} L で割る。", unit="mol/L", d=3,
                ap="混合後の溶質の物質量は、それぞれの溶液に含まれる溶質の物質量の和。体積も和になる（体積変化なし）。",
                steps=[f"溶質：${sig(c1)}\\times{dec(sp.Rational(V1, 1000))}+{sig(c2)}\\times{dec(sp.Rational(V2, 1000))}={sig((c1 * V1 + c2 * V2) / 1000)}$ mol。",
                       f"体積：{V1 + V2} mL＝{dec(sp.Rational(V1 + V2, 1000))} L。", f"$c={sig(c)}$ mol/L。"],
                alt=["加重平均として確かめる：混合後の濃度は2つの濃度の間にあり、体積の大きい方の濃度に近くなる。"],
                pc=[("溶質の物質量の和を求めている", 2), ("値が正しい", 2)], pit=["2つの濃度を単純平均する。"])


PCT = [("NaOH", "10", "1.1"), ("NaOH", "20", "1.2"), ("H2SO4", "98", "1.8"), ("H2SO4", "20", "1.1"), ("HCl", "20", "1.1"), ("NaCl", "10", "1.1"),
("KOH", "28", "1.3"), ("C6H12O6", "18", "1.1")]


@gen("standard_practice", 3, ["computation", "condition_check"])
def percent_molarity(r):
    f, p, d = r.choice(PCT)
    P, D = sp.Rational(p), sp.Rational(d)
    c = 1000 * D * P / 100 / M(f)
    if r.random() < 0.6:
        return numq(f"質量パーセント濃度 {p} %、密度 {d} g/cm³ の{NAMES[f]}水溶液がある。この水溶液のモル濃度は何 mol/L か。{aw_note(f)}有効数字2桁で答えなさい。",
                    c, f"1000*{d}*{p}/100/({M_expr(f)})", f"溶液 1 L（1000 cm³）について計算する。", unit="mol/L", d=3,
                    ap="溶液 1 L（1000 cm³）を考え、質量 → 溶質の質量 → 溶質の物質量の順に求める。",
                    steps=[f"溶液 1 L の質量：$1000\\times{d}={dec(1000 * D)}$ g。", f"溶質の質量：${dec(1000 * D)}\\times\\dfrac{{{p}}}{{100}}={dec(1000 * D * P / 100)}$ g。",
                           f"溶質の物質量：$\\dfrac{{{dec(1000 * D * P / 100)}}}{{{dec(M(f))}}}\\fallingdotseq{sig(c)}$ mol。よって ${sig(c)}$ mol/L。"],
                    alt=[f"公式 $c=\\dfrac{{1000\\times d\\times\\frac{{a}}{{100}}}}{{M}}$ に代入してもよいが、1 L で考える手順を理解しておく。"],
                    pc=[("溶液 1 L の質量を求めている", 1), ("溶質の質量・物質量を求めている", 2), ("値が正しい", 1)],
                    pit=["密度を使わずに、溶液 1 L を 1000 g とみなす。", "溶液の質量と溶質の質量を取り違える。"])
    return numq(f"{sig(c, 3)} mol/L の{NAMES[f]}水溶液の密度は {d} g/cm³ である。この水溶液の質量パーセント濃度は何 % か。{aw_note(f)}有効数字2桁で答えなさい。",
                sp.Rational(sig(c, 3)) * M(f) / (1000 * D) * 100, f"{sig(c, 3)}*({M_expr(f)})/(1000*{d})*100", "溶液 1 L について、溶質の質量÷溶液の質量×100。", unit="%", d=3,
                ap="溶液 1 L を考え、溶質の質量と溶液の質量をそれぞれ求めて比をとる。",
                steps=[f"溶質：${sig(c, 3)}\\times{dec(M(f))}$ g。", f"溶液：$1000\\times{d}={dec(1000 * D)}$ g。", "比をとって 100 倍する。"],
                alt=["逆向き（％ → mol/L）の計算をして、もとの濃度に戻るか検算する。"],
                pc=[("溶質の質量を求めている", 1), ("溶液の質量を求めている", 2), ("値が正しい", 1)], pit=["溶液の質量を 1000 g とする。"])


@gen("standard_practice", 3, ["computation", "condition_check"])
def excess(r):
    metal = r.choice([("Mg", 1, 1), ("Zn", 1, 1), ("Fe", 1, 1), ("Al", 2, 3)])
    f, a, h = metal
    rx = {"Mg": RXN[7], "Zn": RXN[6], "Fe": RXN[18], "Al": RXN[5]}[f]
    hcl_coef = 2 * a if f != "Al" else 6
    for _ in range(100):
        nm_ = sp.Rational(r.choice(["0.010", "0.020", "0.030", "0.015", "0.0050", "0.040"]))
        wm = nm_ * M(f)
        c = sp.Rational(r.choice(["0.50", "1.0", "2.0"]))
        Vml = r.choice([10, 20, 30, 40, 50])
        nh = c * sp.Rational(Vml, 1000)
        if clean(wm, 3) and nh * a != nm_ * hcl_coef:
            break
    need_hcl = nm_ * hcl_coef / a
    if nh >= need_hcl:
        h2 = nm_ * h / a
        lim = f"{NAMES[f]}"
        judge = f"{NAMES[f]}がすべて反応するのに必要な HCl は ${sig(need_hcl, 3)}$ mol で、塩酸中の HCl ${sig(nh, 3)}$ mol で足りる → HCl が余る。"
    else:
        h2 = nh * h / hcl_coef
        lim = "塩化水素"
        judge = f"{NAMES[f]}がすべて反応するには HCl が ${sig(need_hcl, 3)}$ mol 必要だが、${sig(nh, 3)}$ mol しかない → HCl が不足し、HCl がすべて反応する。"
    V = h2 * VM * 1000
    return numq(f"{nm(f)} {dec(wm)} g に {sig(c)} mol/L の塩酸 {Vml} mL を加えて反応させた。発生する水素の体積は{STP}で何 mL か。\n$${eq_tex(rx)}$$\n{aw_note(f)}標準状態の気体のモル体積を 22.4 L/mol とする。",
                V, f"Min({dec(nm_)}*{h}/{a}, {dec(nh)}*{h}/{hcl_coef})*22.4*1000", f"{judge}水素は {lim}の量で決まる。", unit="mL", d=4, n=3,
                ap="両方の反応物の量が与えられているので、まず物質量に直して過不足を判定する。生成量は不足する（すべて反応する）方で決まる。",
                steps=[f"{NAMES[f]}：$\\dfrac{{{dec(wm)}}}{{{dec(M(f))}}}={sig(nm_, 2)}$ mol。HCl：${sig(c)}\\times\\dfrac{{{Vml}}}{{1000}}={sig(nh, 2)}$ mol。",
                       judge, f"水素：${sig(h2, 3)}$ mol → ${sig(h2, 3)}\\times22.4\\times1000={sig(V, 3)}$ mL。"],
                alt=["反応前・変化量・反応後の表をつくると、余る物質の量も同時に分かる。"],
                pc=[("両方の物質量を求めている", 1), ("過不足を正しく判定している", 2), ("体積が正しい", 1)],
                pit=["過不足を判定せず、金属の量だけで計算する。", "L と mL の換算を誤る。"])


GAS_ID = ["H2", "N2", "O2", "CO2", "CH4", "NH3", "C3H8", "Cl2", "C2H6"]


@gen("standard_practice", 2, ["computation", "application"])
def molar_mass_gas(r):
    f = r.choice(GAS_ID)
    Mf = M(f)
    if r.random() < 0.5:
        n = sp.Rational(r.choice(["0.10", "0.20", "0.25", "0.050", "0.50"]))
        w, V = n * Mf, n * VM
        return numq(f"ある気体 {dec(w)} g の体積は、{STP}で {dec(V)} L であった。この気体の分子量を求めなさい。標準状態の気体のモル体積を 22.4 L/mol とする。", Mf,
                    f"{dec(w)}/({dec(V)}/22.4)", f"物質量 $\\dfrac{{{dec(V)}}}{{22.4}}={dec(n)}$ mol、モル質量 $\\dfrac{{{dec(w)}}}{{{dec(n)}}}={dec(Mf)}$ g/mol。", d=3, n=max(2, len(Decimal(dec(Mf)).normalize().as_tuple().digits)),
                    ap="体積から物質量を求め、質量÷物質量でモル質量を出す。モル質量の数値が分子量。",
                    steps=[f"$n=\\dfrac{{{dec(V)}}}{{22.4}}={dec(n)}$ mol。", f"$M=\\dfrac{{{dec(w)}}}{{{dec(n)}}}={dec(Mf)}$ g/mol。", f"分子量は {dec(Mf)}。"],
                    alt=[f"22.4 L あたりの質量（標準状態での 1 mol の質量）を比例で求めても同じ：${dec(w)}\\times\\dfrac{{22.4}}{{{dec(V)}}}$。",
                         f"分子量 {dec(Mf)} の気体としては、たとえば{NAMES[f]}（${tex(f)}$）が考えられる。"],
                    pc=[("物質量を求めている", 2), ("分子量が正しい", 2)], pit=["体積を 22.4 で割らずに質量を割る。"])
    rho = Mf / VM
    return numq(f"{STP}での密度が ${sig(rho, 3)}$ g/L の気体がある。この気体の分子量を整数で求めなさい（有効数字の扱いは考えなくてよい）。標準状態の気体のモル体積を 22.4 L/mol とする。",
                sp.Integer(round(float(sp.Rational(sig(rho, 3)) * VM))), f"floor({sig(rho, 3)}*22.4+Rational(1,2))",
                "1 mol（22.4 L）の質量＝密度×22.4。", d=3,
                ap="標準状態の気体 1 mol は 22.4 L。密度（1 L あたりの質量）に 22.4 をかけると 1 mol の質量になる。",
                steps=[f"$M={sig(rho, 3)}\\times22.4\\fallingdotseq{round(float(sp.Rational(sig(rho, 3)) * VM))}$ g/mol。", "その数値が分子量。"],
                alt=[f"分子量 {dec(Mf)} の気体としては、たとえば{NAMES[f]}が考えられる。密度が空気（平均分子量約 29）より大きいか小さいかも判断の手がかりになる。"],
                pc=[("密度×22.4 の式を立てている", 2), ("値が正しい", 2)], pit=["密度を 22.4 で割る。"])


# ======================================================================
# C 思考力・記述応用
# ======================================================================

PREP = [("NaCl", "塩化ナトリウム"), ("C6H12O6", "グルコース"), ("KNO3", "硝酸カリウム"), ("Na2CO3", "炭酸ナトリウム"), ("C12H22O11", "スクロース")]


@gen("thinking_writing", 3, ["written_reasoning", "condition_check"])
def preparation(r):
    hyd = r.random() < 0.3
    Vml = r.choice([100, 250, 500])
    c = sp.Rational(r.choice(["0.10", "0.20", "0.050", "0.40"]))
    n = c * sp.Rational(Vml, 1000)
    if hyd:
        name, Mh = "硫酸銅(Ⅱ)五水和物 $\\mathrm{CuSO_4\\cdot5H_2O}$（式量 250）", sp.Integer(250)
        w = n * Mh
        target = "硫酸銅(Ⅱ) $\\mathrm{CuSO_4}$"
        note = "五水和物 1 mol から $\\mathrm{CuSO_4}$ 1 mol が得られるので、水和水を含めた式量 250 で質量を計算する。"
    else:
        f, nm_ = r.choice(PREP)
        name, Mh = f"{nm_} ${tex(f)}$（{'式量' if f in ('NaCl', 'KNO3', 'Na2CO3') else '分子量'} {dec(M(f))}）", M(f)
        w = n * Mh
        target = f"{nm_}"
        note = ""
    return desc(f"{name}を用いて、{sig(c)} mol/L の{target}水溶液を {Vml} mL 調製したい。必要な質量を求め、正しい調製の手順を、使う器具の名称を含めて説明しなさい。また、「はかりとった固体を水 {Vml} mL に溶かす」方法ではいけない理由も述べなさい。",
                f"必要な質量は ${sig(c)}\\times\\dfrac{{{Vml}}}{{1000}}\\times{dec(Mh)}={sig(w, 3)}$ g。{note}この質量を正確にはかりとってビーカーで少量の水に溶かし、溶液を {Vml} mL のメスフラスコに移す。ビーカーを少量の水で洗って洗液もメスフラスコに入れ、標線まで水を加えてよく振り混ぜる。"
                f"水 {Vml} mL に溶かすと、溶液の体積は {Vml} mL ちょうどにはならない（溶質が溶けると体積が変わる）ため、モル濃度の定義（溶液 1 L あたりの物質量）に合わなくなる。",
                "モル濃度の分母は溶液の体積。体積を正確に合わせるにはメスフラスコを使う。",
                [("必要な質量を正しく求めている", 2), ("溶かしてからメスフラスコで標線まで合わせる手順を述べている", 3), ("洗液も移すなど溶質を失わない操作にふれている", 1),
                 ("水 " + str(Vml) + " mL に溶かしてはいけない理由を、溶液の体積で説明している", 2)],
                d=4, p=8, lines=9,
                ap="必要な溶質の物質量＝モル濃度×溶液の体積。モル濃度の定義が「溶液」の体積であることから、器具と手順を考える。",
                steps=[f"溶質の物質量：${sig(c)}\\times{dec(sp.Rational(Vml, 1000))}={sig(n)}$ mol。", f"質量：${sig(n)}\\times{dec(Mh)}={sig(w, 3)}$ g。",
                       "少量の水に溶かす → メスフラスコに移す → 洗液も加える → 標線まで水を加える → 振り混ぜる。", "水の体積で合わせると溶液の体積が定まらない。"],
                alt=["メスシリンダーで溶液の体積を合わせる方法は精度が低い。正確な濃度が必要なときはメスフラスコを使う、と比較して述べてもよい。"],
                pc=[("質量", 2), ("手順", 3), ("洗液", 1), ("理由", 2)],
                pit=["溶媒の水の体積をそろえれば良いと考える。", "水和物の水和水を式量に含め忘れる。"],
                chk=(f"{dec(c)}*{Vml}/1000*{dec(Mh)}", str(w), None, "intermediate"))


METALS2 = [("Mg", 2), ("Zn", 2), ("Fe", 2), ("Al", 3)]


@gen("thinking_writing", 4, ["cross_unit", "computation", "written_reasoning"], rel=["HS-CHEB-U01"])
def identify_metal(r):
    f, z = r.choice(METALS2)
    nmol = sp.Rational(r.choice(["0.010", "0.020", "0.0050", "0.040", "0.015", "0.030"]))
    w = nmol * M(f)
    if not clean(w, 3):
        nmol = sp.Rational("0.010")
        w = nmol * M(f)
    nh2 = nmol * z / 2
    Vml = nh2 * VM * 1000
    eq = "2\\mathrm{M}+6\\mathrm{HCl}\\longrightarrow2\\mathrm{MCl_3}+3\\mathrm{H_2}" if z == 3 else "\\mathrm{M}+2\\mathrm{HCl}\\longrightarrow\\mathrm{MCl_2}+\\mathrm{H_2}"
    cands = "Mg（24）、Al（27）、Fe（56）、Zn（65）、Cu（64）"
    ratio = "\\dfrac{2}{3}" if z == 3 else "1"
    return desc(f"{z}価の陽イオンになる金属 M の単体 {dec(w)} g に十分な量の塩酸を加えたところ、M はすべて溶けて水素が{STP}で {dec(Vml)} mL 発生した。反応は ${eq}$ で表される。"
                f"M の原子量を求め、M が何であるかを次の中から選び、考え方とともに答えなさい。（　）内は原子量、標準状態の気体のモル体積は 22.4 L/mol とする。\n候補：{cands}",
                f"水素 ${sig(nh2, 3)}$ mol より M は ${sig(nmol, 3)}$ mol。原子量は $\\dfrac{{{dec(w)}}}{{{sig(nmol, 3)}}}={dec(M(f))}$ で、M は {NAMES[f]}（{f}）。",
                f"水素の物質量から係数の比で M の物質量を求め、質量÷物質量でモル質量を出す。",
                [("水素の物質量を正しく求めている", 2), ("係数の比から M の物質量を求めている", 3), ("原子量を求め、金属を正しく特定している", 2), ("価数と反応式の関係にふれている", 1)],
                d=4, p=8, lines=8,
                ap=f"M は {z} 価の陽イオンになるので、反応式の係数比は M : $\\mathrm{{H_2}}$ ＝ {'2 : 3' if z == 3 else '1 : 1'}。水素の量から M の物質量を求め、原子量＝質量÷物質量を計算する（原子量と周期表の知識は前単元の内容）。",
                steps=[f"$n_{{\\mathrm{{H_2}}}}=\\dfrac{{{dec(Vml)}}}{{22400}}={sig(nh2, 3)}$ mol。",
                       f"係数の比より $n_{{\\mathrm{{M}}}}={sig(nh2, 3)}\\times{ratio}={sig(nmol, 3)}$ mol。",
                       f"原子量：$\\dfrac{{{dec(w)}}}{{{sig(nmol, 3)}}}={dec(M(f))}$。", f"候補から M は {NAMES[f]}。" + ("Cu は塩酸に溶けないことからも除外できる。" if f in ("Zn", "Fe") else "")],
                alt=["電子の授受で考える：M 1 mol は電子を " + str(z) + " mol 放出し、$\\mathrm{H^+}$ 2 mol が電子 2 mol を受け取って $\\mathrm{H_2}$ 1 mol になる。これから M と $\\mathrm{H_2}$ の物質量の比を求めてもよい（酸化還元の単元につながる）。"],
                pc=[("水素の物質量", 2), ("M の物質量", 3), ("原子量と特定", 2), ("価数", 1)],
                pit=["係数の比を使わず、M と水素を同じ物質量とする（3価の金属で誤る）。", "mL を L に直し忘れる。"],
                chk=(f"{dec(w)}/({dec(Vml)}/22400*{2 if z == 3 else 1}/{3 if z == 3 else 1})", AW[f], None, "intermediate"))


@gen("thinking_writing", 3, ["written_reasoning", "application"])
def data_table(r):
    c = sp.Rational(r.choice(["0.40", "0.80", "1.0", "1.2", "0.60"]))
    Vml = r.choice([25, 50, 100])
    nh = c * sp.Rational(Vml, 1000)
    lim = nh / 2 * 24
    step = lim / 4
    rows = []
    for k in range(1, 7):
        m = step * k
        h2 = min(m / 24, nh / 2) * VM * 1000
        rows.append([dec(m), sig(h2, 3)])
    Hmax = nh / 2 * VM * 1000
    return desc(f"濃度の分からない塩酸 {Vml} mL ずつを6つのビーカーに入れ、マグネシウムを {dec(step)} g、{dec(2 * step)} g、…と {dec(step)} g ずつ増やして加えて、発生した水素の体積（標準状態に換算）を測定した。結果は表のとおりである。"
                f"$\\mathrm{{Mg}}+2\\mathrm{{HCl}}\\longrightarrow\\mathrm{{MgCl_2}}+\\mathrm{{H_2}}$、原子量 Mg＝24、標準状態の気体のモル体積は 22.4 L/mol とする。\n"
                f"(1) 塩酸 {Vml} mL とちょうど過不足なく反応するマグネシウムの質量を求めなさい。\n(2) この塩酸のモル濃度を求めなさい。\n(3) 表の後半で水素の体積が増えなくなる理由を説明しなさい。",
                f"(1) {dec(lim)} g　(2) {sig(c)} mol/L　(3) 加えたマグネシウムが {dec(lim)} g をこえると塩酸中の HCl がすべて反応してしまい、HCl が不足するため。余分なマグネシウムは反応せずに残り、水素は HCl の量で決まる最大値 {sig(Hmax, 3)} mL のまま増えない。",
                "グラフ（表）の折れ曲がり点がちょうど過不足なく反応する点。そこでの量から HCl の物質量が分かる。",
                [("(1) 折れ曲がり点を読み取り、質量を正しく求めている", 3), ("(2) HCl の物質量から濃度を正しく求めている", 3), ("(3) HCl が不足することを説明している", 2)],
                d=5, p=8, lines=9, tbl=table(rows, header=["Mg の質量 [g]", "発生した $\\mathrm{H_2}$ [mL]"], caption="実験結果（測定値を理論値として扱う）"),
                ap="Mg の質量に比例して水素が増える範囲は Mg が不足（すべて反応）、一定になった範囲は HCl が不足。比例の直線と水平線の交点が過不足なく反応する点。",
                steps=[f"最大の水素の体積は {sig(Hmax, 3)} mL＝${sig(nh / 2, 3)}$ mol。", f"これと過不足なく反応する Mg も ${sig(nh / 2, 3)}$ mol＝{dec(lim)} g。",
                       f"HCl はその2倍の ${sig(nh, 3)}$ mol。濃度は $\\dfrac{{{sig(nh, 3)}}}{{{dec(sp.Rational(Vml, 1000))}}}={sig(c)}$ mol/L。", "後半は HCl が不足し、水素の量は一定。"],
                alt=["表の値をグラフにして、原点を通る直線部分と水平部分の交点を読み取ってもよい。", "前半の比例部分から「Mg 1 g あたりの水素の体積」を求め、最大値をそれで割っても (1) が得られる。"],
                pc=[("(1)", 3), ("(2)", 3), ("(3)", 2)],
                pit=["表の最後の Mg の質量をすべて反応したものとして計算する。", "HCl と $\\mathrm{H_2}$ の係数の比 2:1 を忘れる。"],
                chk=(f"[{dec(c)}*{Vml}/1000/2*24, {dec(c)}]", f"[{lim}, {c}]", None, "intermediate"))


# ======================================================================
# D 典型誤答訂正
# ======================================================================

LIQ = [("水", "H2O", "1.0"), ("エタノール", "C2H6O", "0.81")]
GAS_MASS = ["O2", "N2", "H2", "Cl2"]


@gen("error_correction", 3, ["common_error", "condition_check"])
def err_molar_volume(r):
    if r.random() < 0.45:
        name, f, d = r.choice(LIQ)
        n = sp.Rational(r.choice(["1.0", "2.0", "0.50", "3.0", "0.25"]))
        w = n * M(f)
        vol = w / sp.Rational(d)
        return err_item(f"{name} ${tex(f)}$ {dec(w)} g の、0 ℃・$1.013\\times10^5$ Pa での体積を求めなさい。{aw_note(f)}この条件での{name}の密度は {d} g/cm³ とする。",
                        f"物質量は $\\dfrac{{{dec(w)}}}{{{dec(M(f))}}}={dec(n)}$ mol。標準状態なので ${dec(n)}\\times22.4={dec(n * VM)}$ L",
                        "22.4 L/mol を使った部分", "condition",
                        "「0 ℃・$1.013\\times10^5$ Pa ＝ 標準状態 → 22.4 L/mol」と条件だけで判断し、物質が気体かどうかを確認していない。",
                        f"{name}はこの条件で液体なので、密度を使って ${dec(w)}\\div{d}\\fallingdotseq{sig(vol)}$ cm³",
                        f"約 ${sig(vol)}$ cm³（mL）",
                        "22.4 L/mol は標準状態の「気体」にだけ成り立つ。液体・固体の体積は密度から求める。",
                        [f"{name}の融点・沸点から、0 ℃ では液体である。", "液体の体積は 質量÷密度 で求める。", f"${dec(w)}\\div{d}\\fallingdotseq{sig(vol)}$ cm³。"],
                        "モル体積を使う前に「その物質は気体か」を必ず確認する。",
                        ["結果の大きさで確かめる：コップ1杯程度の液体が数十リットルになるはずがない。"], ["条件（温度・圧力）だけを見て 22.4 L/mol を使う。"],
                        chk=(f"{dec(w)}/{d}", str(vol), None, "intermediate"), d=2)
    f = r.choice(GAS_MASS)
    V = sp.Rational(r.choice(["5.6", "11.2", "2.24", "4.48", "33.6", "1.12"]))
    n = V / VM
    atom = f[0] if f != "Cl2" else "Cl"
    wa = n * sp.Rational(AW[atom])
    w = n * M(f)
    return err_item(f"{STP}で {dec(V)} L の{NAMES[f]} ${tex(f)}$ の質量を求めなさい。{aw_note(f)}標準状態の気体のモル体積を 22.4 L/mol とする。",
                    f"物質量は $\\dfrac{{{dec(V)}}}{{22.4}}={sig(n)}$ mol。{NAMES[f]}の原子量 {AW[atom]} をかけて ${sig(n)}\\times{AW[atom]}={sig(wa)}$ g",
                    "モル質量に原子量を用いた部分", "concept",
                    f"元素記号 {atom} の原子量をそのまま使い、{NAMES[f]}が二原子分子 ${tex(f)}$ であることを見落としている。",
                    f"${tex(f)}$ の分子量は {dec(M(f))}。${sig(n)}\\times{dec(M(f))}={sig(w)}$ g", f"${sig(w)}$ g",
                    f"気体の{NAMES[f]}は二原子分子 ${tex(f)}$ として存在するので、モル質量は {dec(M(f))} g/mol。",
                    [f"$n=\\dfrac{{{dec(V)}}}{{22.4}}={sig(n)}$ mol（${tex(f)}$ 分子の物質量）。", f"モル質量は分子量 {dec(M(f))} に g/mol をつけたもの。",
                     f"$w={sig(n)}\\times{dec(M(f))}={sig(w)}$ g。"],
                    "「何の粒子の物質量か」を明確にし、その粒子のモル質量をかける。",
                    ["1 mol（22.4 L）の質量が分子量の値になることから、比例で確かめる。"], ["単体の気体の分子式（$\\mathrm{O_2}$ など）を原子として扱う。"],
                    chk=(f"{dec(V)}/22.4*({M_expr(f)})", str(w), None, "intermediate"), d=2)


@gen("error_correction", 3, ["common_error", "concept"])
def err_concentration(r):
    if r.random() < 0.4:
        f = r.choice(["NaCl", "NaOH", "C6H12O6", "KNO3"])
        n = sp.Rational(r.choice(["0.10", "0.20", "0.50", "1.0"]))
        w = n * M(f)
        V = r.choice(["1.0", "0.50"])
        c = n / sp.Rational(V)
        return err_item(f"{nm(f)}を用いて、{sig(c)} mol/L の水溶液を {dec(sp.Rational(V) * 1000)} mL つくる方法を答えなさい。{aw_note(f)}",
                        f"{NAMES[f]} {dec(w)} g（{dec(n)} mol）をはかりとり、水 {dec(sp.Rational(V) * 1000)} mL に溶かす",
                        "水の体積で合わせている部分", "concept",
                        "モル濃度の「1 L あたり」を、溶媒である水の量と取り違えている。日常の「水○○ mL に溶かす」という表現にも引きずられやすい。",
                        f"{dec(w)} g を少量の水に溶かし、メスフラスコで溶液全体を {dec(sp.Rational(V) * 1000)} mL にする",
                        f"{dec(w)} g を少量の水に溶かしてメスフラスコに移し、標線まで水を加えて溶液全体を {dec(sp.Rational(V) * 1000)} mL にする。",
                        "モル濃度は溶液 1 L あたりの溶質の物質量。水 " + dec(sp.Rational(V) * 1000) + " mL に溶かすと溶液の体積はその値からずれる。",
                        [f"必要な溶質：${sig(c)}\\times{V}={dec(n)}$ mol＝{dec(w)} g。", "溶かしてからメスフラスコへ移す。", "標線まで水を加え、溶液の体積を合わせる。"],
                        "モル濃度の定義の分母が「溶液」の体積であることに立ち返る。",
                        ["定義式 $c=\\dfrac{n}{V_{\\text{溶液}}}$ に当てはめて、誤った方法では $V_{\\text{溶液}}$ が分からないことを確認する。"],
                        ["溶媒の体積と溶液の体積を混同する。"], chk=(f"{dec(c)}*{V}*({M_expr(f)})", str(w), None, "intermediate"), d=2)
    c1 = sp.Rational(r.choice(["1.0", "0.50", "2.0", "0.20"]))
    V1 = r.choice([10, 20, 25, 50])
    Vw = r.choice([90, 100, 150, 200, 80])
    wrong = c1 * V1 / Vw
    right = c1 * V1 / (V1 + Vw)
    return err_item(f"{sig(c1)} mol/L の塩酸 {V1} mL に水 {Vw} mL を加えてうすめた。うすめた後の塩酸のモル濃度を有効数字2桁で求めなさい。ただし、混合による体積の変化はないものとする。",
                    f"$\\dfrac{{{sig(c1)}\\times{V1}}}{{{Vw}}}={sig(wrong)}$ mol/L",
                    "割る体積（分母）", "concept",
                    "「水 " + str(Vw) + " mL でうすめた」という文から、加えた水の体積だけを分母にしてしまった。",
                    f"溶液の体積は ${V1}+{Vw}={V1 + Vw}$ mL なので $\\dfrac{{{sig(c1)}\\times{V1}}}{{{V1 + Vw}}}\\fallingdotseq{sig(right)}$ mol/L",
                    f"${sig(right)}$ mol/L",
                    "うすめた後の溶液の体積は、もとの溶液と加えた水の体積の和。溶質の物質量は変わらない。",
                    [f"溶質（HCl）：${sig(c1)}\\times\\dfrac{{{V1}}}{{1000}}={sig(c1 * V1 / 1000)}$ mol。", f"溶液：${V1 + Vw}$ mL。",
                     f"$c=\\dfrac{{{sig(c1 * V1 / 1000)}}}{{{dec(sp.Rational(V1 + Vw, 1000))}}}\\fallingdotseq{sig(right)}$ mol/L。"],
                    "希釈では「溶質の物質量が一定」「溶液全体の体積で割る」の2点を確認する。",
                    ["うすめた後の濃度は、もとの濃度より必ず小さく、体積の比 $\\dfrac{" + str(V1) + "}{" + str(V1 + Vw) + "}$ 倍になることで確かめる。"],
                    ["加えた水の体積だけで割る。"], chk=(f"{dec(c1)}*{V1}/({V1}+{Vw})", str(right), None, "intermediate"), d=2)


@gen("error_correction", 4, ["common_error", "computation"])
def err_stoich(r):
    for _ in range(100):
        rx, (ci, fi), (cj, fj) = stoich_pick(r)
        if ci != cj or M(fi) != M(fj):
            break
    ni, wi = pick_clean(r, fi, 3, ["0.10", "0.20", "0.50", "0.050", "0.40", "1.0", "0.25"])
    right = ni * cj / ci * M(fj)
    mode = r.choice(["mass_ratio", "ignore_coef"]) if ci != cj else "mass_ratio"
    if mode == "mass_ratio":
        wrong = wi * cj / ci
        sol = f"係数の比 {ci}:{cj} が質量の比なので、${dec(wi)}\\times\\dfrac{{{cj}}}{{{ci}}}={sig(wrong)}$ g"
        step = "係数の比を質量の比として使った部分"
        tempt = "係数の比が「量の比」であることは覚えているが、それが物質量の比であって質量の比ではないことを区別していない。"
    else:
        wrong = ni * M(fj)
        sol = f"{NAMES[fi]}は $\\dfrac{{{dec(wi)}}}{{{dec(M(fi))}}}={dec(ni)}$ mol なので、{NAMES[fj]}も {dec(ni)} mol。${dec(ni)}\\times{dec(M(fj))}={sig(wrong)}$ g"
        step = "物質量の比を 1:1 とした部分"
        tempt = "物質量に直すところまではできているが、係数を見ずに「同じ物質量だけ反応・生成する」と思い込んでいる。"
    if sig(wrong) == sig(right):
        wrong = wi
        sol = f"質量保存の法則より、{NAMES[fj]}も {dec(wi)} g"
        step = "質量保存の法則の使い方"
        tempt = "質量保存の法則（反応物の総質量＝生成物の総質量）を、個々の物質の質量が等しいことと取り違えている。"
    reac = fi in [f for _, f in sides(rx)[0]]
    return err_item(f"次の反応で、{nm(fi)} {dec(wi)} g が{'すべて反応する' if reac else '生成する'}とき、{'反応する' if fj in [f for _, f in sides(rx)[0]] else '生成する'}{NAMES[fj]}は何 g か。有効数字2桁で答えなさい。\n$${eq_tex(rx)}$$\n{aw_note(fi, fj)}",
                    sol, step, "formula" if mode == "mass_ratio" else "calculation", tempt,
                    f"${dec(ni)}\\times\\dfrac{{{cj}}}{{{ci}}}\\times{dec(M(fj))}\\fallingdotseq{sig(right)}$ g", f"${sig(right)}$ g",
                    "化学反応式の係数の比は物質量の比。質量に直すには、それぞれのモル質量をかける必要がある。",
                    [f"{NAMES[fi]}：$\\dfrac{{{dec(wi)}}}{{{dec(M(fi))}}}={dec(ni)}$ mol。", f"係数の比 {ci}:{cj} より {NAMES[fj]}は ${sig(ni * cj / ci, 3)}$ mol。",
                     f"質量：${sig(ni * cj / ci, 3)}\\times{dec(M(fj))}\\fallingdotseq{sig(right)}$ g。"],
                    "質量 → 物質量 → 係数の比 → 物質量 → 質量 の順を守る。",
                    [f"質量の比例式 ${ci}\\times{dec(M(fi))}:{cj}\\times{dec(M(fj))}={dec(wi)}:x$ を立てて検算する。"],
                    ["係数の比を質量の比とみなす。", "係数を無視する。"],
                    chk=(f"{dec(wi)}/({M_expr(fi)})*{cj}/{ci}*({M_expr(fj)})", str(right), None, "intermediate"), d=3)


GENERATORS = [mass_mol, particles, gas_volume, molarity, balance,
              mass_mass, mass_gas, dilution, percent_molarity, excess, molar_mass_gas,
              preparation, identify_metal, data_table,
              err_molar_volume, err_concentration, err_stoich]
