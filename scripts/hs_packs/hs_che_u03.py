"""単元パック：化学 無機物質（典型元素・遷移元素・イオンの分離）。"""
import re
from decimal import ROUND_HALF_UP, Decimal

import sympy as sp

from banks._common import desc, figure, mc, num
from hs_pack_lib import board, check, definition, derivation, example, figure_explain, gen, guide, intro, lesson, summary, theorem, tp

UNIT_ID = "HS-CHE-U03"

AW = {"H": "1.0", "C": "12", "N": "14", "O": "16", "Na": "23", "Al": "27", "S": "32", "Cl": "35.5", "K": "39", "Ca": "40", "Mn": "55", "Fe": "56", "Cu": "64", "Zn": "65"}
STP = "標準状態（0 ℃、$1.013\\times10^5$ Pa）"


# ----------------------------------------------------------------------
# 補助
# ----------------------------------------------------------------------

def parse(f):
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


def tex(f):
    return "\\mathrm{" + re.sub(r"(\d+)", lambda m: "_" + (m.group(1) if len(m.group(1)) == 1 else "{" + m.group(1) + "}"), f) + "}"


def ion(s):
    """'Cu2+' → \\mathrm{Cu^{2+}}"""
    m = re.match(r"^(.*?)(\d?)([+-])$", s)
    base, n, sg = m.groups()
    return "\\mathrm{" + re.sub(r"(\d+)", r"_{\1}", base) + "^{" + n + sg + "}}"


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


# ----------------------------------------------------------------------
# 図：系統分離の流れ図
# ----------------------------------------------------------------------

SEP_STEPS = [("希塩酸を加える", "AgCl（白）"), ("ろ液に硫化水素を通じる（酸性）", "CuS（黒）"),
             ("ろ液を煮沸して H₂S を除き、希硝酸を加えた後、アンモニア水を過剰に加える", "Fe(OH)₃（赤褐）・Al(OH)₃（白）"),
             ("ろ液に硫化水素を通じる（塩基性）", "ZnS（白）"), ("ろ液に炭酸アンモニウム水溶液を加える", "CaCO₃・BaCO₃（白）"),
             ("ろ液を炎色反応で調べる", "Na⁺（黄）・K⁺（赤紫）")]


def _esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def flow_svg(rows, top="混合水溶液", w=540):
    """rows=[(操作, 沈殿)] を縦の流れ図にする。"""
    h = 40 + 46 * len(rows)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="sans-serif" font-size="10.5">',
           '<defs><marker id="fa" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#000"/></marker></defs>',
           f'<rect x="8" y="6" width="120" height="22" fill="#eef3f9" stroke="#333"/><text x="14" y="21">{_esc(top)}</text>']
    y = 28
    for i, (op, ppt) in enumerate(rows):
        out.append(f'<line x1="40" y1="{y}" x2="40" y2="{y + 40}" stroke="#000" marker-end="url(#fa)"/>')
        line1 = f"操作{i + 1}：" + op
        out.append(f'<text x="48" y="{y + 14}" font-size="9.5">{_esc(line1[:28])}</text>')
        if len(line1) > 28:
            out.append(f'<text x="58" y="{y + 26}" font-size="9.5">{_esc(line1[28:56])}</text>')
        out.append(f'<line x1="40" y1="{y + 34}" x2="350" y2="{y + 34}" stroke="#666" stroke-dasharray="3 2"/>')
        out.append(f'<rect x="350" y="{y + 24}" width="{w - 356}" height="20" fill="#fff" stroke="#333"/><text x="355" y="{y + 38}">{_esc(ppt)}</text>')
        y += 46
    out.append("</svg>")
    return "".join(out)


def sep_fig(rows, caption, top="混合水溶液", labels=None):
    disp = [(op, labels[i] if labels else ppt) for i, (op, ppt) in enumerate(rows)]
    alt = "陽イオンの系統分離の流れ図。" + "。".join(f"操作{i + 1}：{op} → 沈殿 {p}" for i, (op, p) in enumerate(disp)) + "。"
    return figure(alt, svg=flow_svg(disp, top), caption=caption)


# ======================================================================
# 授業プリント
# ======================================================================

LESSON = lesson(
    goals=["周期表の族ごとに、典型元素の単体と化合物の性質・反応を、電子配置や酸化還元・酸塩基の考え方で説明できる。",
           "代表的な気体の製法・捕集法・乾燥剤を、気体の性質（水への溶けやすさ・密度・酸性/塩基性）から選べる。",
           "遷移元素（Fe・Cu・Ag・Zn・Cr・Mn など）のイオンの色・沈殿・錯イオンを整理し、金属イオンの系統分離の手順と理由を説明できる。",
           "硫酸・硝酸・炭酸ナトリウム・アンモニアなどの工業的製法の反応を理解し、原料と製品の量的関係を計算できる。"],
    duration=150,
    readiness=["周期表と電子配置・イオンの価数（化学基礎「物質の構成と化学結合」）を説明できる。",
               "酸・塩基、酸化還元、イオン化傾向（化学基礎「酸と塩基・酸化還元」）を使って反応を説明できる。",
               "化学反応式の係数から物質量の関係を求められる（化学基礎「物質量と化学反応式」）。"],
    flow=[("導入：身のまわりの無機物質", 8, "セメント・ガラス・肥料・電池などに使われる元素を周期表上に配置する"),
          ("典型元素（1・2・13族）", 20, "アルカリ金属・アルカリ土類金属・アルミニウム（両性）"),
          ("典型元素（14〜18族）", 27, "炭素とケイ素、窒素とリン、酸素と硫黄、ハロゲン、貴ガス"),
          ("気体の製法と性質", 20, "発生方法・捕集法・乾燥剤の選び方"),
          ("工業的製法", 20, "接触法・オストワルト法・アンモニアソーダ法と量的関係"),
          ("遷移元素と錯イオン", 25, "Fe・Cu・Ag・Zn・Cr・Mn の化合物、イオンの色、錯イオンの形"),
          ("金属イオンの分離と確認", 20, "沈殿反応の整理、系統分離の手順と理由、炎色反応"),
          ("まとめと確認", 10, "確認問題、問題プリントの課題指示")],
    sections=[
        intro("in1", "周期表を「性質の地図」として読む",
              "無機物質の性質は、ばらばらに暗記するものではない。同じ族の元素は価電子の数が同じなので、単体や化合物の性質がよく似ている。"
              "また、イオンになりやすさ（イオン化傾向）、酸化剤・還元剤としてのはたらき、酸・塩基としての性質という化学基礎の道具を使えば、多くの反応を予想できる。",
              bullets=["典型元素：族ごとの共通性と、周期を下るときの変化（金属性・酸化力）を押さえる。",
                       "遷移元素：最外殻電子が1〜2個で、すべて金属。複数の酸化数をとり、有色のイオンや錯イオンをつくるものが多い。",
                       "イオンの分離：沈殿・錯イオン・両性という性質の違いを組み合わせて、混合物から1種類ずつ取り出す。"],
              points=[tp("最初に白地図の周期表を配り、授業中に出てきた性質を族ごとに書き込ませる。",
                         ask="ナトリウムとカリウムの単体を石油中に保存する理由は何か。", expect="空気中の酸素や水と激しく反応するから。",
                         timing="授業の冒頭")]),
        definition("df1", "典型元素の性質の要点",
                   "1族（H を除く）のアルカリ金属は価電子1個で1価の陽イオンになりやすく、単体は水と反応して水素を発生する。2族元素は2価の陽イオンになる。"
                   "13族のアルミニウムは酸にも強塩基にも溶ける両性元素である。17族のハロゲンは1価の陰イオンになりやすく、単体は酸化力が強い。",
                   formula="$$\\text{酸化力}：\\mathrm{F_2}>\\mathrm{Cl_2}>\\mathrm{Br_2}>\\mathrm{I_2},\\qquad 2\\mathrm{Al}+2\\mathrm{NaOH}+6\\mathrm{H_2O}\\longrightarrow2\\mathrm{Na[Al(OH)_4]}+3\\mathrm{H_2}$$",
                   conditions=["Al・Zn・Sn・Pb は両性元素で、単体・酸化物・水酸化物が強塩基の水溶液にも溶ける。",
                               "Fe・Al・Ni は濃硝酸に対して不動態となり、内部まで溶けない。",
                               "HF は弱酸で、ガラス（$\\mathrm{SiO_2}$）を溶かすのでポリエチレン容器に保存する。他のハロゲン化水素の水溶液は強酸。",
                               "濃硫酸には吸湿性・脱水作用・（熱濃硫酸の）酸化作用がある。"],
                   points=[tp("「同じ族は似ている」を、Na と K、Cl と Br、O と S の組で確認させ、族の性質を1行で言わせる。",
                              ask="塩素水に臭化カリウム水溶液を加えると何が起こるか。", expect="$\\mathrm{Cl_2}$ の方が酸化力が強いので $\\mathrm{Br_2}$ が遊離し、溶液が褐色になる。")]),
        derivation("dv1", "ハロゲンの酸化力の順序を実験から確かめる",
                   ["臭化カリウム水溶液に塩素水を加えると、$\\mathrm{Cl_2}+2\\mathrm{KBr}\\longrightarrow2\\mathrm{KCl}+\\mathrm{Br_2}$ が起こり、溶液が褐色になる。→ 酸化力 $\\mathrm{Cl_2}>\\mathrm{Br_2}$。",
                    "ヨウ化カリウム水溶液に臭素水を加えると $\\mathrm{I_2}$ が遊離する（デンプンで青紫色）。→ $\\mathrm{Br_2}>\\mathrm{I_2}$。",
                    "逆に、塩化カリウム水溶液にヨウ素を加えても変化しない。→ $\\mathrm{I_2}$ は $\\mathrm{Cl^-}$ を酸化できない。",
                    "原子番号が小さいほど原子半径が小さく、電子を引きつける力が強い（陰イオンになりやすい）ことと一致する。",
                    "フッ素は水とも激しく反応して酸素を発生するほど酸化力が強い（$2\\mathrm{F_2}+2\\mathrm{H_2O}\\longrightarrow4\\mathrm{HF}+\\mathrm{O_2}$）。"],
                   body="「酸化力の強い単体が、弱い方の陰イオンから電子を奪って単体を遊離させる」という見方は、金属のイオン化傾向による置換反応と同じ構造である。",
                   points=[tp("イオン化傾向の実験（Zn 板を $\\mathrm{Cu^{2+}}$ 水溶液に入れる）と並べて板書し、電子の移動の向きを比べさせる。", timing="ハロゲンの学習時")]),
        theorem("th1", "気体の製法・捕集法・乾燥剤の選び方",
                "$$\\text{捕集}：\\begin{cases}\\text{水に溶けにくい}&\\to\\text{水上置換}\\\\ \\text{水に溶けやすく空気より重い}&\\to\\text{下方置換}\\\\ \\text{水に溶けやすく空気より軽い}&\\to\\text{上方置換}\\end{cases}$$",
                ["空気の平均分子量は約 29。分子量が 29 より大きい気体は空気より重い。",
                 "乾燥剤は、気体と反応しないものを選ぶ。酸性の気体に塩基性の乾燥剤（ソーダ石灰）は使えず、塩基性の $\\mathrm{NH_3}$ に酸性の乾燥剤（濃硫酸・十酸化四リン）は使えない。",
                 "$\\mathrm{NH_3}$ は塩化カルシウムとも反応するので、ソーダ石灰で乾燥させる。"],
                proof=["$\\mathrm{NH_3}$（分子量 17）は水に非常によく溶け、空気より軽い → 上方置換。",
                       "$\\mathrm{Cl_2}$（71）・$\\mathrm{HCl}$（36.5）・$\\mathrm{CO_2}$（44）・$\\mathrm{SO_2}$（64）・$\\mathrm{NO_2}$（46）は水に溶け、空気より重い → 下方置換。",
                       "$\\mathrm{H_2}$・$\\mathrm{O_2}$・$\\mathrm{NO}$ は水に溶けにくい → 水上置換（純度の高い気体が得られる）。"],
                points=[tp("気体ごとに「分子量」「水への溶解」「酸性・中性・塩基性」の3項目の表を作らせ、捕集法と乾燥剤をその表から導かせる。",
                           ask="塩化水素を水上置換で集められない理由は？", expect="水に非常によく溶けるから。")]),
        definition("df2", "遷移元素と錯イオン",
                   "遷移元素は3〜12族の元素で、すべて金属である。同じ元素が複数の酸化数をとり（$\\mathrm{Fe^{2+}}$ と $\\mathrm{Fe^{3+}}$ など）、有色のイオンが多い。"
                   "金属イオンに非共有電子対をもつ分子や陰イオン（配位子）が配位結合したイオンを錯イオンという。",
                   formula="$$[\\mathrm{Ag(NH_3)_2}]^+\\ (\\text{直線形}),\\quad [\\mathrm{Cu(NH_3)_4}]^{2+}\\ (\\text{正方形・深青色}),\\quad [\\mathrm{Zn(NH_3)_4}]^{2+}\\ (\\text{正四面体形}),\\quad [\\mathrm{Fe(CN)_6}]^{3-}\\ (\\text{正八面体形})$$",
                   conditions=["水溶液の色：$\\mathrm{Cu^{2+}}$ 青、$\\mathrm{Fe^{2+}}$ 淡緑、$\\mathrm{Fe^{3+}}$ 黄褐、$\\mathrm{MnO_4^-}$ 赤紫、$\\mathrm{CrO_4^{2-}}$ 黄、$\\mathrm{Cr_2O_7^{2-}}$ 赤橙。",
                               "$\\mathrm{Fe^{3+}}$ はチオシアン酸カリウムで血赤色、$\\mathrm{Fe^{2+}}$ はヘキサシアニド鉄(Ⅲ)酸カリウムで濃青色沈殿。",
                               "$\\mathrm{CrO_4^{2-}}$（黄）は酸性にすると $\\mathrm{Cr_2O_7^{2-}}$（赤橙）に変わり、塩基性にすると戻る。",
                               "アンモニア水を過剰に加えると、$\\mathrm{Ag^+}$・$\\mathrm{Cu^{2+}}$・$\\mathrm{Zn^{2+}}$ の水酸化物（酸化物）の沈殿はアンミン錯イオンとなって溶ける。"],
                   points=[tp("錯イオンの名称（配位数・配位子・中心金属・電荷）を、名前を分解して読む練習をさせる。",
                              ask="$[\\mathrm{Cu(NH_3)_4}]^{2+}$ の名称は？", expect="テトラアンミン銅(Ⅱ)イオン")]),
        figure_explain("fg1", "金属イオンの系統分離", sep_fig(SEP_STEPS, "陽イオンの系統分離の例"),
                       "多種類の金属イオンを含む水溶液に、試薬を順に加えて沈殿させ、ろ過して取り出していく。各段階の試薬は、特定のイオンだけを沈殿させるように選ぶ。"
                       "操作2で硫化水素を酸性で通じるのは、$\\mathrm{S^{2-}}$ の濃度を小さくして硫化物の溶けにくい $\\mathrm{Cu^{2+}}$ などだけを沈殿させるためである。"
                       "操作3で煮沸して硫化水素を除くのは、塩基性にしたときに $\\mathrm{Zn^{2+}}$ などが硫化物として沈殿するのを防ぐため、希硝酸を加えるのは操作2で還元された $\\mathrm{Fe^{2+}}$ を $\\mathrm{Fe^{3+}}$ に戻すためである。",
                       points=[tp("各操作の「目的（何を沈殿させるか）」と「なぜその順番か」をセットで説明させる。",
                                  ask="操作1と操作2の順序を逆にすると、どんな不都合が起こるか。", expect="$\\mathrm{Ag^+}$ も硫化物 $\\mathrm{Ag_2S}$（黒）として沈殿し、$\\mathrm{CuS}$ と分けられなくなる。")]),
        example("ex1", "例題1　両性と錯イオンを使った分離",
                "$\\mathrm{Al^{3+}}$ と $\\mathrm{Zn^{2+}}$ を含む水溶液から、$\\mathrm{Al^{3+}}$ だけを沈殿として分離したい。加える試薬と、そのとき起こる変化を説明せよ。",
                ["水酸化ナトリウム水溶液を過剰に加えると、$\\mathrm{Al(OH)_3}$ も $\\mathrm{Zn(OH)_2}$ も両性のため溶けてしまい、分離できない。",
                 "アンモニア水を過剰に加えると、$\\mathrm{Al(OH)_3}$ は白色沈殿のまま残る。",
                 "$\\mathrm{Zn(OH)_2}$ は $[\\mathrm{Zn(NH_3)_4}]^{2+}$ となって溶ける。"],
                "アンモニア水を過剰に加え、$\\mathrm{Al(OH)_3}$（白）をろ過して分離する。", thinking="「両性で溶けるか」と「アンミン錯イオンをつくるか」を表にして比べる。",
                misconceptions=[("水酸化ナトリウム水溶液を過剰に加える", "両方とも溶けるので分離できない")]),
        example("ex2", "例題2　接触法の量的関係",
                "硫黄 64 kg をすべて硫酸にすると、質量パーセント濃度 98 % の濃硫酸は何 kg 得られるか。原子量は H＝1.0、O＝16、S＝32 とする。",
                ["$\\mathrm{S}\\to\\mathrm{SO_2}\\to\\mathrm{SO_3}\\to\\mathrm{H_2SO_4}$ で、S 原子 1 個から $\\mathrm{H_2SO_4}$ 1 個ができる（S 原子の数は保存される）。",
                 "S：$\\dfrac{64\\times10^3}{32}=2.0\\times10^3$ mol → $\\mathrm{H_2SO_4}$ も $2.0\\times10^3$ mol＝196 kg。", "98 % の濃硫酸：$196\\div0.98=200$ kg。"],
                "200 kg", thinking="多段階の工業的製法では、注目する原子が最初から最後までいくつ受け継がれるかで考える。",
                points=[tp("各段階の反応式を足し合わせて全体の反応式 $\\mathrm{S}+\\dfrac32\\mathrm{O_2}+\\mathrm{H_2O}\\longrightarrow\\mathrm{H_2SO_4}$ を作らせ、1:1 の関係を確認させる。")]),
        example("ex3", "例題3　気体の発生と捕集",
                "塩化アンモニウムと水酸化カルシウムの混合物を加熱してアンモニアを発生させた。反応式を書き、捕集法と乾燥剤を理由とともに答えよ。",
                ["$2\\mathrm{NH_4Cl}+\\mathrm{Ca(OH)_2}\\longrightarrow\\mathrm{CaCl_2}+2\\mathrm{H_2O}+2\\mathrm{NH_3}$（弱塩基の塩＋強塩基 → 弱塩基の遊離）。",
                 "$\\mathrm{NH_3}$ は水に非常によく溶け、空気より軽い（分子量 17）→ 上方置換。",
                 "塩基性の気体なので、酸性の濃硫酸や、反応してしまう塩化カルシウムは使えない → ソーダ石灰。"],
                "上方置換で捕集し、ソーダ石灰で乾燥させる。", thinking="発生の原理（弱塩基の遊離）と、気体の性質（溶解性・密度・塩基性）を分けて考える。",
                misconceptions=[("濃硫酸で乾燥させる", "アンモニアと中和反応してしまう")]),
        board("bd1", "板書案",
              [("① 典型元素", ["アルカリ金属：石油中に保存", "Al・Zn・Sn・Pb：両性", "酸化力 F₂ > Cl₂ > Br₂ > I₂", "HF：弱酸、ガラスを溶かす",
                              "濃硫酸：吸湿性・脱水作用"]),
               ("② 気体", ["水に難溶 → 水上置換", "易溶・重い（M > 29）→ 下方", "易溶・軽い → 上方（NH₃）", "酸性気体 ⇔ 塩基性乾燥剤は×",
                          "NH₃ はソーダ石灰"]),
               ("③ 遷移元素と分離", ["Fe³⁺＋KSCN → 血赤色", "NH₃ 過剰で溶ける：Ag⁺・Cu²⁺・Zn²⁺", "NaOH 過剰で溶ける：Al³⁺・Zn²⁺・Pb²⁺",
                                    "HCl → AgCl、H₂S（酸性）→ CuS", "NH₃ → Fe(OH)₃・Al(OH)₃"])]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("沈殿の色は、「白が基本、硫化物は黒（ZnS 白・CdS 黄）、ハロゲン化銀は白→淡黄→黄」のように例外を中心に覚えさせる。",
                  caution="$\\mathrm{AgF}$ は水に溶けることを忘れやすい。"),
               tp("両性元素（ああすんなり：Al・Zn・Sn・Pb）と、アンモニア水過剰で溶けるイオン（Ag・Cu・Zn など）の重なりが Zn であることを、ベン図で確認させる。",
                  ask="NaOH 水溶液と NH₃ 水のどちらを過剰に加えても沈殿が溶けるイオンは？", expect="$\\mathrm{Zn^{2+}}$"),
               tp("工業的製法の計算では、全体の反応式を作るか、注目する原子の保存で考えるかを選ばせる。", timing="工業的製法の終わり"),
               tp("性質を覚えるだけでなく、「なぜそうなるか」（イオン化傾向・酸化力・酸塩基）を一言で添えさせる。")],
              misconceptions=[("アンモニアは濃硫酸で乾燥できる", "アンモニアは塩基性なので濃硫酸と反応する。ソーダ石灰を使う"),
                              ("鉄は濃硝酸によく溶ける", "鉄・アルミニウム・ニッケルは濃硝酸中で不動態となる"),
                              ("NaOH を過剰に加えれば Al³⁺ と Zn²⁺ を分離できる", "どちらも両性で溶ける。アンモニア水過剰なら Al(OH)₃ だけが残る")]),
        summary("sm1", "まとめ", ["典型元素は族ごとに性質が似ている。両性元素・不動態・ハロゲンの酸化力の順などは、電子配置と酸化還元・酸塩基で説明できる。",
                                   "気体の捕集法と乾燥剤は、水への溶けやすさ・空気との重さの比較・酸性/塩基性から選ぶ。",
                                   "遷移元素は複数の酸化数・有色のイオン・錯イオンが特徴。沈殿・両性・錯イオンの違いを組み合わせると、金属イオンを系統的に分離できる。",
                                   "工業的製法の量的関係は、注目する原子の保存（S → H₂SO₄、NH₃ → HNO₃ など）で考える。"]),
        check("ck1", "確認問題", [("Al・Zn・Sn・Pb のように酸にも強塩基にも溶ける元素を何というか。", "両性元素"),
                                  ("アンモニアの捕集法は？", "上方置換"),
                                  ("$\\mathrm{Fe^{3+}}$ を含む水溶液にチオシアン酸カリウム水溶液を加えると何色になるか。", "血赤色"),
                                  ("$\\mathrm{Ag^+}$ と $\\mathrm{Cu^{2+}}$ を含む水溶液に希塩酸を加えたときの沈殿は？", "AgCl（白色）")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

GAS = {"H2": ("水素", "亜鉛に希硫酸を加える", "水上置換", 2, "中性"),
       "O2": ("酸素", "過酸化水素水に酸化マンガン(Ⅳ)を加える", "水上置換", 32, "中性"),
       "Cl2": ("塩素", "酸化マンガン(Ⅳ)に濃塩酸を加えて加熱する", "下方置換", 71, "酸性"),
       "HCl": ("塩化水素", "塩化ナトリウムに濃硫酸を加えて加熱する", "下方置換", 36.5, "酸性"),
       "NH3": ("アンモニア", "塩化アンモニウムと水酸化カルシウムの混合物を加熱する", "上方置換", 17, "塩基性"),
       "CO2": ("二酸化炭素", "炭酸カルシウムに希塩酸を加える", "下方置換", 44, "酸性"),
       "SO2": ("二酸化硫黄", "銅に濃硫酸を加えて加熱する", "下方置換", 64, "酸性"),
       "H2S": ("硫化水素", "硫化鉄(Ⅱ)に希硫酸を加える", "下方置換", 34, "酸性"),
       "NO": ("一酸化窒素", "銅に希硝酸を加える", "水上置換", 30, "中性"),
       "NO2": ("二酸化窒素", "銅に濃硝酸を加える", "下方置換", 46, "酸性")}
COLLECT = {"水上置換": "水に溶けにくいので水上置換", "下方置換": "水に溶けやすく空気より重いので下方置換", "上方置換": "水に溶けやすく空気より軽いので上方置換"}


@gen("basic_check", 5, ["concept", "condition_check"])
def gas_prep(r):
    form = r.choice(["method", "method", "collect", "dry"])
    if form == "method":
        f = r.choice(list(GAS))
        others = r.sample([g for g in GAS if g != f and GAS[g][1] != GAS[f][1]], 3)
        why = {GAS[g][1]: (f"この方法で発生するのは{GAS[g][0]}である。", "気体の製法の取り違え") for g in others}
        return mc(f"{GAS[f][0]} ${tex(f)}$ を発生させる方法として最も適当なものを選びなさい。", [GAS[f][1]] + [GAS[g][1] for g in others],
                  f"{GAS[f][0]}は「{GAS[f][1]}」ことで発生する。", d=2,
                  ap="反応の種類（酸と金属、弱酸・弱塩基の遊離、揮発性の酸の遊離、酸化還元、分解）で製法を整理する。",
                  steps=["各方法で起こる反応と、発生する気体を考える。", f"{GAS[f][0]}が発生するのは「{GAS[f][1]}」方法。"],
                  alt=["反応式を書いて、生成物に目的の気体が含まれるかで確かめる。"],
                  pc=[("反応を正しく判断している", 1), ("正しく選んでいる", 1)], why=why,
                  pit=["銅と希硝酸（NO）・濃硝酸（NO₂）を取り違える。", "塩素の発生に希塩酸を使うと考える。"])
    if form == "collect":
        f = r.choice(list(GAS))
        right = COLLECT[GAS[f][2]]
        wrong = [v for k, v in COLLECT.items() if k != GAS[f][2]] + ["水に溶けやすいので水上置換"]
        why = {w: ("水に溶けやすい気体を水上置換で集めると、気体が水に溶けてしまう。" if w.startswith("水に溶けやすいので") else f"{GAS[f][0]}（分子量 {GAS[f][3]}）の水への溶けやすさ・空気（約 29）との重さの比較に合わない。",
                   "捕集法の選び方の誤り") for w in wrong}
        return mc(f"{GAS[f][0]} ${tex(f)}$ の捕集法とその理由の組み合わせとして最も適当なものを選びなさい。", [right] + wrong,
                  f"{GAS[f][0]}は{right}で集める。", d=2,
                  ap="水に溶けにくければ水上置換。溶けやすければ、分子量を空気の平均分子量（約 29）と比べて上方・下方を決める。",
                  steps=[f"{GAS[f][0]}の水への溶けやすさを考える。", f"分子量 {GAS[f][3]} を 29 と比べる。", f"→ {GAS[f][2]}。"],
                  alt=["水上置換で集められる気体は、水に溶けにくいものに限られる。純度が高く集められるので、可能ならば水上置換が選ばれる。"],
                  pc=[("溶解性と密度で判断している", 1), ("正しく選んでいる", 1)], why=why, pit=["分子量と空気の平均分子量の比較を逆にする。"])
    if r.random() < 0.5:
        right = "ソーダ石灰"
        wrong = ["濃硫酸", "十酸化四リン", "塩化カルシウム"]
        why = {"濃硫酸": ("濃硫酸は酸性で、塩基性のアンモニアと反応する。", "酸塩基の組み合わせの誤り"),
               "十酸化四リン": ("十酸化四リンは酸性の乾燥剤で、アンモニアと反応する。", "酸塩基の組み合わせの誤り"),
               "塩化カルシウム": ("塩化カルシウムは中性だが、アンモニアと反応して化合物をつくる。", "例外の見落とし")}
        return mc("アンモニアの乾燥剤として最も適当なものを選びなさい。", [right] + wrong, "アンモニアは塩基性の気体なので、塩基性の乾燥剤ソーダ石灰を用いる。", d=2,
                  ap="乾燥剤は気体と反応しないものを選ぶ。塩基性の気体には塩基性の乾燥剤。",
                  steps=["アンモニアは塩基性。", "酸性の乾燥剤（濃硫酸・十酸化四リン）は不可。", "塩化カルシウムもアンモニアと反応するので不可。", "→ ソーダ石灰。"],
                  alt=["ソーダ石灰は酸化カルシウムと水酸化ナトリウムの混合物で、酸性の気体（$\\mathrm{CO_2}$ など）を吸収するのにも使われる。"],
                  pc=[("酸塩基で判断している", 1), ("正しく選んでいる", 1)], why=why, pit=["塩化カルシウムがアンモニアと反応することを忘れる。"])
    f = r.choice(["Cl2", "HCl", "CO2", "SO2"])
    right = "濃硫酸"
    wrong = ["ソーダ石灰", "酸化カルシウム", "水酸化ナトリウム（固体）"]
    why = {w: (f"{w}は塩基性で、酸性の{GAS[f][0]}と反応してしまう。", "酸塩基の組み合わせの誤り") for w in wrong}
    return mc(f"{GAS[f][0]} ${tex(f)}$ の乾燥剤として最も適当なものを選びなさい。", [right] + wrong, f"{GAS[f][0]}は酸性の気体なので、酸性の乾燥剤である濃硫酸を用いる。", d=2,
              ap="酸性の気体には酸性または中性の乾燥剤を使う。塩基性の乾燥剤は気体と中和反応してしまう。",
              steps=[f"{GAS[f][0]}は酸性の気体。", "塩基性の乾燥剤（ソーダ石灰・酸化カルシウム・水酸化ナトリウム）は不可。", "→ 濃硫酸。"],
              alt=["中性の乾燥剤である塩化カルシウムも、酸性の気体の乾燥に使える。"],
              pc=[("酸塩基で判断している", 1), ("正しく選んでいる", 1)], why=why, pit=["気体の液性を考えずに乾燥剤を選ぶ。"])


PPT = {"AgCl": "白色", "AgBr": "淡黄色", "AgI": "黄色", "Ag2CrO4": "赤褐色", "PbCrO4": "黄色", "BaSO4": "白色", "CaCO3": "白色", "CuS": "黒色",
       "PbS": "黒色", "Ag2S": "黒色", "ZnS": "白色", "CdS": "黄色", "Fe(OH)3": "赤褐色", "Cu(OH)2": "青白色", "Zn(OH)2": "白色", "Al(OH)3": "白色",
       "Ag2O": "褐色", "PbI2": "黄色", "PbCl2": "白色", "BaCO3": "白色"}
ION_COL = {"Cu2+": "青色", "Fe2+": "淡緑色", "Fe3+": "黄褐色", "Ni2+": "緑色", "MnO4 -": "赤紫色", "CrO4 2-": "黄色", "Cr2O7 2-": "赤橙色",
           "Zn2+": "無色", "Al3+": "無色", "Ag+": "無色"}
COLORS = ["白色", "黒色", "黄色", "赤褐色", "青白色", "淡黄色", "褐色"]


def ion_tex(k):
    if " " in k:
        b, c = k.split()
        return "\\mathrm{" + re.sub(r"(\d+)", r"_{\1}", b) + "^{" + c + "}}"
    return ion(k)


@gen("basic_check", 4, ["concept"])
def colors(r):
    if r.random() < 0.6:
        right = r.choice(list(PPT))
        others = r.sample([p for p in PPT if p != right], 3)
        wrongs = []
        for p in others:
            c = r.choice([x for x in COLORS if x != PPT[p]])
            wrongs.append((p, c))
        lab = lambda p, c: f"${tex(p)}$：{c}"  # noqa: E731
        why = {lab(p, c): (f"${tex(p)}$ は{PPT[p]}である。", "沈殿の色の取り違え") for p, c in wrongs}
        return mc("沈殿とその色の組み合わせとして正しいものを選びなさい。", [lab(right, PPT[right])] + [lab(p, c) for p, c in wrongs],
                  f"${tex(right)}$ は{PPT[right]}の沈殿である。", d=2,
                  ap="沈殿の色は「白が基本」で、硫化物（黒、ただし ZnS 白・CdS 黄）、ハロゲン化銀（白・淡黄・黄）、クロム酸塩（黄・赤褐）などを例外として整理する。",
                  steps=["各沈殿の色を思い出す。", f"正しい組み合わせは ${tex(right)}$：{PPT[right]}。"],
                  alt=["沈殿のできる反応（例：$\\mathrm{Ag^+}+\\mathrm{Cl^-}\\longrightarrow\\mathrm{AgCl}$）を書いて、陽イオン・陰イオンの組で整理し直す。"],
                  pc=[("沈殿の色を知っている", 1), ("正しく選んでいる", 1)], why=why, pit=["ハロゲン化銀の色の順（白・淡黄・黄）を混同する。"])
    right = r.choice(list(ION_COL))
    others = r.sample([k for k in ION_COL if ION_COL[k] != ION_COL[right]], 3)
    cols_ = list(dict.fromkeys(ION_COL.values()))
    wrongs = [(k, r.choice([c for c in cols_ if c != ION_COL[k]])) for k in others]
    lab = lambda k, c: f"${ion_tex(k)}$：{c}"  # noqa: E731
    why = {lab(k, c): (f"${ion_tex(k)}$ の水溶液は{ION_COL[k]}である。", "イオンの色の取り違え") for k, c in wrongs}
    return mc("水溶液中のイオンとその色の組み合わせとして正しいものを選びなさい。", [lab(right, ION_COL[right])] + [lab(k, c) for k, c in wrongs],
              f"${ion_tex(right)}$ を含む水溶液は{ION_COL[right]}である。", d=2,
              ap="典型元素のイオンは無色のものが多く、遷移元素のイオンには有色のものが多い。",
              steps=["各イオンが典型元素か遷移元素かを確認する。", "遷移元素のイオンの色を思い出す。", f"正しいのは ${ion_tex(right)}$：{ION_COL[right]}。"],
              alt=["$\\mathrm{CrO_4^{2-}}$（黄）と $\\mathrm{Cr_2O_7^{2-}}$（赤橙）は pH で互いに変化することとあわせて覚える。"],
              pc=[("イオンの色を知っている", 1), ("正しく選んでいる", 1)], why=why, pit=["$\\mathrm{Fe^{2+}}$ と $\\mathrm{Fe^{3+}}$ の色を逆にする。"])


FLAME = {"Li": ("リチウム", "赤色"), "Na": ("ナトリウム", "黄色"), "K": ("カリウム", "赤紫色"), "Ca": ("カルシウム", "橙赤色"), "Sr": ("ストロンチウム", "紅色"),
         "Ba": ("バリウム", "黄緑色"), "Cu": ("銅", "青緑色")}


@gen("basic_check", 3, ["concept"])
def flame(r):
    k = r.choice(list(FLAME))
    others = r.sample([x for x in FLAME if x != k], 3)
    if r.random() < 0.5:
        why = {FLAME[o][0]: (f"{FLAME[o][0]}の炎色反応は{FLAME[o][1]}である。", "炎色反応の色の取り違え") for o in others}
        return mc(f"炎色反応で{FLAME[k][1]}を示す元素を選びなさい。", [FLAME[k][0]] + [FLAME[o][0] for o in others], f"{FLAME[k][0]}の炎色反応は{FLAME[k][1]}。", d=1,
                  ap="アルカリ金属・アルカリ土類金属（Be・Mg を除く）と銅は、特有の炎色反応を示す。",
                  steps=["Li 赤、Na 黄、K 赤紫、Ca 橙赤、Sr 紅、Ba 黄緑、Cu 青緑。", f"{FLAME[k][1]}は{FLAME[k][0]}。"],
                  alt=["花火の色（黄色は Na、赤は Sr や Li、緑は Ba や Cu）と結びつけて確かめる。"],
                  pc=[("炎色反応の色を知っている", 1), ("正しく選んでいる", 1)], why=why, pit=["K の赤紫と Li の赤を混同する。"])
    wrong = [(o, FLAME[o][1]) for o in others]
    cols_ = [FLAME[x][1] for x in FLAME]
    wl = []
    for o, c in wrong:
        wl.append((o, r.choice([x for x in cols_ if x != c])))
    lab = lambda e, c: f"{FLAME[e][0]}：{c}"  # noqa: E731
    why = {lab(o, c): (f"{FLAME[o][0]}の炎色反応は{FLAME[o][1]}である。", "炎色反応の色の取り違え") for o, c in wl}
    return mc("元素とその炎色反応の色の組み合わせとして正しいものを選びなさい。", [lab(k, FLAME[k][1])] + [lab(o, c) for o, c in wl], f"{FLAME[k][0]}は{FLAME[k][1]}。", d=1,
              ap="炎色反応の色を元素ごとに確認する。",
              steps=["Li 赤、Na 黄、K 赤紫、Ca 橙赤、Sr 紅、Ba 黄緑、Cu 青緑。", f"正しいのは {FLAME[k][0]}：{FLAME[k][1]}。"],
              alt=["炎色反応は、未知の水溶液に含まれる $\\mathrm{Na^+}$・$\\mathrm{K^+}$ などの確認（系統分離の最後の段階）に使われる。"],
              pc=[("炎色反応の色を知っている", 1), ("正しく選んでいる", 1)], why=why, pit=["Ca と Sr の色を混同する。"])


EL_TRUE = ["ナトリウムは空気中の酸素や水と反応しやすいので、石油（灯油）中に保存する。",
           "黄リンは空気中で自然発火するので、水中に保存する。",
           "フッ化水素酸はガラスを溶かすので、ポリエチレンの容器に保存する。",
           "濃硝酸は光や熱で分解しやすいので、褐色びんに入れて冷暗所に保存する。",
           "アルミニウムは、塩酸にも水酸化ナトリウム水溶液にも溶けて水素を発生する。",
           "鉄やアルミニウムを濃硝酸に入れると、表面にち密な酸化物の被膜ができて内部まで溶けない。",
           "フッ化水素の水溶液は、他のハロゲン化水素の水溶液と異なり弱酸である。",
           "塩素を水に溶かすと、一部が水と反応して塩化水素と次亜塩素酸を生じる。",
           "貴ガスの原子は安定な電子配置をもち、単原子分子として存在する。",
           "濃硫酸には脱水作用があり、スクロースに加えると炭化させる。",
           "銅は希塩酸には溶けないが、希硝酸には一酸化窒素を発生しながら溶ける。",
           "炭酸水素ナトリウムを加熱すると、炭酸ナトリウム・水・二酸化炭素が生じる。",
           "酸化カルシウムに水を加えると、多量の熱を発生して水酸化カルシウムになる。",
           "二酸化ケイ素は共有結合の結晶で、融点が高い。"]
EL_FALSE = [("ナトリウムは反応しにくいので、水中に保存する。", "ナトリウムは水と激しく反応して水素を発生するので、石油中に保存する。"),
            ("フッ化水素酸は、ガラスびんに入れて保存する。", "フッ化水素酸はガラスの主成分 $\\mathrm{SiO_2}$ を溶かすので、ポリエチレン容器に保存する。"),
            ("ハロゲンの単体の酸化力は、ヨウ素が最も強い。", "酸化力は $\\mathrm{F_2}>\\mathrm{Cl_2}>\\mathrm{Br_2}>\\mathrm{I_2}$ で、フッ素が最も強い。"),
            ("フッ化水素の水溶液は強酸である。", "フッ化水素は分子間の水素結合などのため電離度が小さく、弱酸である。"),
            ("アルミニウムは水酸化ナトリウム水溶液には溶けない。", "アルミニウムは両性元素で、強塩基の水溶液にも水素を発生して溶ける。"),
            ("鉄は濃硝酸によく溶けて水素を発生する。", "鉄は濃硝酸中で不動態となり、内部まで溶けない。また硝酸との反応では水素ではなく窒素酸化物が生じる。"),
            ("銅は希塩酸に溶けて水素を発生する。", "銅は水素よりイオン化傾向が小さいので、希塩酸とは反応しない。"),
            ("貴ガスは反応性が高く、二原子分子として存在する。", "貴ガスは安定な電子配置をもち、ほとんど反応せず単原子分子として存在する。"),
            ("黄リンは空気中で安定なので、ふたのない容器で保存できる。", "黄リンは空気中で自然発火するので、水中に保存する。"),
            ("炭酸ナトリウムを加熱すると、容易に分解して二酸化炭素を発生する。", "加熱で容易に分解するのは炭酸水素ナトリウムで、炭酸ナトリウムは加熱しても分解しにくい。")]


@gen("basic_check", 4, ["concept", "condition_check"])
def element_property(r):
    if r.random() < 0.5:
        right = r.choice(EL_TRUE)
        wrong = r.sample(EL_FALSE, 3)
        why = {w: (reason, "典型元素の性質の誤認") for w, reason in wrong}
        return mc("典型元素の単体や化合物について述べた次の文のうち、正しいものを選びなさい。", [right] + [w for w, _ in wrong], f"正しいのは「{right}」。", d=2,
                  ap="保存方法・両性・不動態・ハロゲンの性質など、理由とセットで覚えた性質に照らして判定する。",
                  steps=["各文の物質の性質を、反応性（酸化還元・イオン化傾向）や酸塩基の観点で確認する。", "誤りの文は、性質や理由が事実と逆になっている。", f"正しいのは「{right}」。"],
                  alt=["誤りの文それぞれについて、正しい性質に直した文を作ってみる。"],
                  pc=[("性質を正しく判断している", 1), ("正しく選んでいる", 1)], why=why, pit=["保存方法の理由を取り違える。"])
    w, reason = r.choice(EL_FALSE)
    rights = r.sample(EL_TRUE, 3)
    why = {x: ("この文は事実と合っている。", "正しい記述を誤りと判断している") for x in rights}
    return mc("典型元素の単体や化合物について述べた次の文のうち、誤っているものを選びなさい。", [w] + rights, f"誤っているのは「{w}」。{reason}", d=2,
              ap="各文の主張を、その物質の性質と理由に照らして検討する。",
              steps=["各文を検討する。", f"「{w}」は誤り。", reason],
              alt=["正しい文の理由（例：なぜ石油中に保存するのか）を説明できるか確かめる。"],
              pc=[("誤りを見抜いている", 1), ("正しく選んでいる", 1)], why=why, pit=["もっともらしい理由が添えられた誤文を見逃す。"])


IND = [("contact", "接触法", "硫黄", "S", "硫酸", "H2SO4", 1, 1), ("ostwald", "オストワルト法", "アンモニア", "NH3", "硝酸", "HNO3", 1, 1),
       ("solvay", "アンモニアソーダ法", "塩化ナトリウム", "NaCl", "炭酸ナトリウム", "Na2CO3", 2, 1), ("iron", "鉄鉱石の還元", "酸化鉄(Ⅲ)", "Fe2O3", "鉄", "Fe", 1, 2),
       ("alumina", "溶融塩電解", "酸化アルミニウム", "Al2O3", "アルミニウム", "Al", 1, 2), ("haber", "ハーバー・ボッシュ法", "水素", "H2", "アンモニア", "NH3", 3, 2)]
IND_EQ = {"contact": "\\mathrm{S}\\to\\mathrm{SO_2}\\to\\mathrm{SO_3}\\to\\mathrm{H_2SO_4}", "ostwald": "\\mathrm{NH_3}+2\\mathrm{O_2}\\longrightarrow\\mathrm{HNO_3}+\\mathrm{H_2O}",
          "solvay": "2\\mathrm{NaCl}+\\mathrm{CaCO_3}\\longrightarrow\\mathrm{Na_2CO_3}+\\mathrm{CaCl_2}", "iron": "\\mathrm{Fe_2O_3}+3\\mathrm{CO}\\longrightarrow2\\mathrm{Fe}+3\\mathrm{CO_2}",
          "alumina": "2\\mathrm{Al_2O_3}\\longrightarrow4\\mathrm{Al}+3\\mathrm{O_2}", "haber": "\\mathrm{N_2}+3\\mathrm{H_2}\\longrightarrow2\\mathrm{NH_3}"}


@gen("basic_check", 4, ["computation", "application"])
def industrial(r):
    key, proc, rn, rf, pn, pf, a, b = r.choice(IND)
    for _ in range(100):
        n = sp.Rational(r.choice(["1.0", "2.0", "5.0", "0.50", "4.0", "10", "3.0", "0.20", "8.0"])) * 1000
        w = n * a * M(rf) / 1000
        if clean(w, 3):
            break
    wp = n * b * M(pf) / 1000
    note = "（全体の反応を、S 原子 1 個から $\\mathrm{H_2SO_4}$ 1 個ができる変化とみなす）" if key == "contact" else ""
    return numq(f"{proc}により、{rn} ${tex(rf)}$ {dec(w)} kg からつくられる{pn} ${tex(pf)}$ は最大何 kg か。全体の反応は ${IND_EQ[key]}$ で表される{note}。{aw_note(rf, pf)}",
                wp, f"{w}*1000/({M(rf)})*{b}/({a})*({M(pf)})/1000", f"{rn}と{pn}の物質量の比は {a}：{b}。", unit="kg", d=2, n=max(2, min(3, len(Decimal(dec(wp)).normalize().as_tuple().digits))),
                ap="多段階の工業的製法でも、全体の反応式（または注目する原子の数の保存）から、原料と製品の物質量の比を求める。kg のままでも mol を kmol と読みかえれば同じ計算になる。",
                steps=[f"{rn}：$\\dfrac{{{dec(w)}\\times10^3}}{{{dec(M(rf))}}}={sig(n * a, 3)}$ mol。", f"物質量の比 {a}：{b} より{pn}は ${sig(n * b, 3)}$ mol。",
                       f"質量：${sig(n * b, 3)}\\times{dec(M(pf))}\\times10^{{-3}}={sig(wp, 3)}$ kg。"],
                alt=[f"質量の比例式 ${a}\\times{dec(M(rf))}:{b}\\times{dec(M(pf))}={dec(w)}:x$ で求めてもよい。"],
                pc=[("物質量の比を正しく用いている", 1), ("値が正しい", 1)], pit=["係数の比を考えず 1：1 とする。" if (a, b) != (1, 1) else "途中の物質の係数に惑わされる。"])


# ======================================================================
# B 標準演習
# ======================================================================

GROUPS = [("Ag+", 1, "AgCl", "希塩酸を加える"), ("Pb2+", 1, "PbCl2", "希塩酸を加える"), ("Cu2+", 2, "CuS", "硫化水素を通じる（酸性）"),
          ("Fe3+", 3, "Fe(OH)3", "アンモニア水を過剰に加える"), ("Al3+", 3, "Al(OH)3", "アンモニア水を過剰に加える"), ("Zn2+", 4, "ZnS", "硫化水素を通じる（塩基性）"),
          ("Ca2+", 5, "CaCO3", "炭酸アンモニウム水溶液を加える"), ("Ba2+", 5, "BaCO3", "炭酸アンモニウム水溶液を加える")]
def step_txt(g, first, has2):
    t = {1: "希塩酸を加えてろ過する", 2: ("塩酸で酸性にして硫化水素を通じてろ過する" if first else "硫化水素を通じてろ過する（酸性のまま）"),
         3: ("煮沸して硫化水素を追い出し、希硝酸を加えた後、アンモニア水を過剰に加えてろ過する" if has2 else "希硝酸を少量加えた後、アンモニア水を過剰に加えてろ過する"),
         4: "硫化水素を通じてろ過する", 5: "炭酸アンモニウム水溶液を加えてろ過する"}[g]
    if first:
        return t
    return ("ろ液を" if t.startswith("煮沸") else "ろ液に") + t


@gen("standard_practice", 5, ["concept", "application"])
def separation(r):
    for _ in range(100):
        picks = []
        for g in (1, 2, 3, 4, 5):
            if g == 3 or r.random() < 0.7:
                picks.append(r.choice([x for x in GROUPS if x[1] == g]))
        if len(picks) >= 3:
            break
    groups = [p[1] for p in picks]
    k = r.randrange(len(picks))
    target = picks[k]
    ions = "、".join(f"${ion(p[0])}$" for p in picks)
    steps_txt = "\n".join(f"操作{i + 1}：{step_txt(g, i == 0, 2 in groups)}。→ 沈殿{chr(65 + i)}" for i, g in enumerate(groups))
    right = f"${tex(target[2])}$"
    pool = ["AgCl", "PbCl2", "CuS", "Fe(OH)3", "Al(OH)3", "ZnS", "CaCO3", "BaCO3", "Zn(OH)2", "Cu(OH)2", "Ag2S", "Ca(OH)2"]
    wrong_f = r.sample([x for x in pool if x != target[2]], 3)
    why = {}
    for x in wrong_f:
        if x in [p[2] for p in picks]:
            why[f"${tex(x)}$"] = (f"${tex(x)}$ は別の操作で生じる沈殿である。", "操作と沈殿の対応の誤り")
        elif x == "Zn(OH)2" and "Zn2+" in [p[0] for p in picks]:
            why[f"${tex(x)}$"] = ("アンモニア水を過剰に加えると、$\\mathrm{Zn(OH)_2}$ はテトラアンミン亜鉛(Ⅱ)イオンとなって溶ける。", "錯イオンの形成の見落とし")
        elif x == "Cu(OH)2" and "Cu2+" in [p[0] for p in picks]:
            why[f"${tex(x)}$"] = ("銅(Ⅱ)イオンは酸性での硫化水素で CuS として除かれる。また過剰のアンモニア水では錯イオンとなって溶ける。", "操作の順序の見落とし")
        elif x == "Ag2S" and "Ag+" in [p[0] for p in picks]:
            why[f"${tex(x)}$"] = ("銀イオンは操作1（希塩酸）で AgCl として先に除かれている。", "操作の順序の見落とし")
        else:
            why[f"${tex(x)}$"] = (f"この混合水溶液と操作の組み合わせでは ${tex(x)}$ は生じない。", "含まれるイオンと沈殿の対応の誤り")
    return mc(f"{ions} を含む水溶液に、次の操作を順に行った。\n{steps_txt}\n沈殿{chr(65 + k)}の化学式として最も適当なものを選びなさい。", [right] + [f"${tex(x)}$" for x in wrong_f],
              f"操作{k + 1}では ${ion(target[0])}$ が ${tex(target[2])}$（{PPT.get(target[2], '白色')}）として沈殿する。", d=3,
              ap="各操作で沈殿するイオンは、それより前の操作で除かれていないもののうち、その試薬で沈殿をつくるもの。",
              steps=[f"操作{i + 1}：${ion(p[0])}$ → ${tex(p[2])}$。" for i, p in enumerate(picks)] + [f"沈殿{chr(65 + k)}は ${tex(target[2])}$。"],
              alt=["系統分離の6つの段階（HCl → H₂S 酸性 → NH₃ → H₂S 塩基性 → (NH₄)₂CO₃ → 炎色反応）を書き出し、含まれるイオンを当てはめる。"],
              pc=[("操作と沈殿の対応を理解している", 2), ("正しく選んでいる", 2)], why=why,
              pit=["硫化水素を酸性で通じたときに $\\mathrm{Zn^{2+}}$ も沈殿すると考える。", "アンモニア水過剰で $\\mathrm{Zn^{2+}}$ が沈殿すると考える。"])


AMPH = {"Al3+": ("白色", True, False), "Zn2+": ("白色", True, True), "Pb2+": ("白色", True, False), "Cu2+": ("青白色", False, True),
        "Ag+": ("褐色", False, True), "Fe3+": ("赤褐色", False, False), "Fe2+": ("緑白色", False, False), "Mg2+": ("白色", False, False)}


@gen("standard_practice", 4, ["concept", "condition_check"])
def amphoteric(r):
    for _ in range(100):
        t = r.choice(list(AMPH))
        others = r.sample([k for k in AMPH if AMPH[k] != AMPH[t]], 3)
        if len({AMPH[x] for x in others}) == 3:
            break
    col, naoh, nh3 = AMPH[t]
    stem = (f"ある金属イオンを含む水溶液に、水酸化ナトリウム水溶液を少量加えると{col}の沈殿が生じ、さらに過剰に加えると沈殿は{'溶けた' if naoh else '溶けなかった'}。"
            f"また、別にとった同じ水溶液にアンモニア水を過剰に加えると、生じた沈殿は{'溶けた' if nh3 else '溶けなかった'}。この金属イオンとして最も適当なものを選びなさい。")

    def desc_(k):
        c, a, b = AMPH[k]
        return f"${ion(k)}$ は{c}の沈殿を生じ、NaOH 過剰で{'溶ける' if a else '溶けない'}、NH₃ 過剰で{'溶ける' if b else '溶けない'}。"
    why = {f"${ion(k)}$": (desc_(k), "両性・錯イオン形成の判断の誤り") for k in others}
    return mc(stem, [f"${ion(t)}$"] + [f"${ion(k)}$" for k in others], desc_(t), d=3,
              ap="NaOH 過剰で溶ける：両性元素（Al・Zn・Sn・Pb）。NH₃ 過剰で溶ける：アンミン錯イオンをつくる Ag・Cu・Zn など。沈殿の色も手がかり。",
              steps=[f"沈殿の色：{col}。", f"NaOH 過剰で{'溶ける → 両性元素' if naoh else '溶けない → 両性元素ではない'}。",
                     f"NH₃ 過剰で{'溶ける → アンミン錯イオンをつくる' if nh3 else '溶けない → アンミン錯イオンをつくらない'}。", f"→ ${ion(t)}$。"],
              alt=["表（縦：イオン、横：NaOH 少量・過剰、NH₃ 少量・過剰）を作って整理しておくと、どの組み合わせの問題にも対応できる。"],
              pc=[("両性・錯イオンの判断をしている", 2), ("正しく選んでいる", 2)], why=why,
              pit=["$\\mathrm{Al^{3+}}$ がアンモニア水過剰で溶けると考える。", "$\\mathrm{Cu^{2+}}$ が NaOH 過剰で溶けると考える。"])


HALO_PAIR = [("Cl2", "KBr", True, "Br2"), ("Cl2", "KI", True, "I2"), ("Br2", "KI", True, "I2"), ("I2", "KCl", False, None), ("Br2", "KCl", False, None),
             ("I2", "KBr", False, None)]
HNAME = {"Cl2": "塩素水", "Br2": "臭素水", "I2": "ヨウ素ヨウ化カリウム水溶液", "KBr": "臭化カリウム水溶液", "KI": "ヨウ化カリウム水溶液", "KCl": "塩化カリウム水溶液"}
HALOGEN = {"F2": ("フッ素", "淡黄色の気体"), "Cl2": ("塩素", "黄緑色の気体"), "Br2": ("臭素", "赤褐色の液体"), "I2": ("ヨウ素", "黒紫色の固体")}


@gen("standard_practice", 3, ["concept", "application"])
def halogen(r):
    form = r.choice(["disp", "disp", "state"])
    if form == "disp":
        yes = [p for p in HALO_PAIR if p[2]]
        no = [p for p in HALO_PAIR if not p[2]]
        if r.random() < 0.5:
            right = r.choice(yes)
            wrong = no
            q = "反応が起こるもの"
        else:
            right = r.choice(no)
            wrong = r.sample(yes, 3)
            q = "反応が起こらないもの"
        lab = lambda p: f"{HNAME[p[0]]}に{HNAME[p[1]]}を加える"  # noqa: E731
        why = {lab(p): ((f"${tex(p[0])}$ の方が酸化力が強いので、${tex(p[3])}$ が遊離する反応が起こる。" if p[2] else f"${tex(p[0])}$ は ${tex(p[1])}$ の陰イオンより酸化力の弱いハロゲンなので、反応は起こらない。"),
                        "ハロゲンの酸化力の順序の誤り") for p in wrong}
        return mc(f"次の操作のうち、{q}を選びなさい。", [lab(right)] + [lab(p) for p in wrong],
                  ("酸化力の強いハロゲンの単体は、酸化力の弱いハロゲンの陰イオンを酸化して単体を遊離させる。" + (f"${tex(right[0])}$ は ${tex(right[3])}$ より酸化力が強い。" if right[2] else f"${tex(right[0])}$ は、水溶液中のハロゲン化物イオンのもとの単体より酸化力が弱いので、反応しない。")), d=2,
                  ap="酸化力 $\\mathrm{F_2}>\\mathrm{Cl_2}>\\mathrm{Br_2}>\\mathrm{I_2}$。加えた単体が、水溶液中の陰イオンのもとの単体より酸化力が強いときだけ反応する。",
                  steps=["加える単体と、水溶液中のハロゲン化物イオンのもとの単体を比べる。", "前者の酸化力が強ければ反応が起こる。", f"→ {lab(right)}。"],
                  alt=["電子の受け渡しで確かめる：例えば $\\mathrm{Cl_2}+2\\mathrm{Br^-}\\longrightarrow2\\mathrm{Cl^-}+\\mathrm{Br_2}$ では、$\\mathrm{Br^-}$ が電子を失い $\\mathrm{Cl_2}$ が受け取る。"],
                  pc=[("酸化力の順序を用いている", 2), ("正しく選んでいる", 2)], why=why, pit=["酸化力の順序を逆に覚えている。"])
    k = r.choice(list(HALOGEN))
    others = [x for x in HALOGEN if x != k]
    lab = lambda x, s: f"{HALOGEN[x][0]}：{s}"  # noqa: E731
    states = [HALOGEN[x][1] for x in HALOGEN]
    wl = [(x, r.choice([s for s in states if s != HALOGEN[x][1]])) for x in others]
    why = {lab(x, s): (f"{HALOGEN[x][0]}の単体は常温・常圧で{HALOGEN[x][1]}である。", "ハロゲン単体の状態・色の取り違え") for x, s in wl}
    return mc("ハロゲンの単体と、常温・常圧での色・状態の組み合わせとして正しいものを選びなさい。", [lab(k, HALOGEN[k][1])] + [lab(x, s) for x, s in wl],
              f"{HALOGEN[k][0]}の単体は{HALOGEN[k][1]}。", d=2,
              ap="原子番号が大きいほど分子量が大きく分子間力が強いので、気体 → 液体 → 固体と変わる（F₂・Cl₂ 気体、Br₂ 液体、I₂ 固体）。",
              steps=["F₂ 淡黄色の気体、Cl₂ 黄緑色の気体、Br₂ 赤褐色の液体、I₂ 黒紫色の固体。", f"正しいのは {HALOGEN[k][0]}：{HALOGEN[k][1]}。"],
              alt=["分子量と分子間力の関係から、状態の順序を説明できることを確認する。"],
              pc=[("状態・色を知っている", 2), ("正しく選んでいる", 2)], why=why, pit=["臭素を気体と考える。"])


TR_TRUE = ["$\\mathrm{Fe^{3+}}$ を含む水溶液にチオシアン酸カリウム水溶液を加えると、血赤色の溶液になる。",
           "$\\mathrm{Fe^{2+}}$ を含む水溶液にヘキサシアニド鉄(Ⅲ)酸カリウム水溶液を加えると、濃青色の沈殿が生じる。",
           "$\\mathrm{Fe^{3+}}$ を含む水溶液にヘキサシアニド鉄(Ⅱ)酸カリウム水溶液を加えると、濃青色の沈殿が生じる。",
           "硫酸銅(Ⅱ)五水和物は青色の結晶で、加熱して水和水を失うと白色の粉末になる。",
           "クロム酸イオンを含む黄色の水溶液を酸性にすると、二クロム酸イオンが生じて赤橙色になる。",
           "テトラアンミン銅(Ⅱ)イオンは深青色で、正方形の構造をもつ。",
           "ジアンミン銀(Ⅰ)イオンは直線形の構造をもつ。",
           "テトラアンミン亜鉛(Ⅱ)イオンは正四面体形の構造をもつ。",
           "ヘキサシアニド鉄(Ⅲ)酸イオンは正八面体形の構造をもつ。",
           "遷移元素の単体はすべて金属である。",
           "塩化銀の白色沈殿に光を当てると、分解して銀が遊離し、黒っぽくなる。"]
TR_FALSE = [("$\\mathrm{Fe^{2+}}$ を含む水溶液にチオシアン酸カリウム水溶液を加えると、血赤色の溶液になる。", "血赤色になるのは $\\mathrm{Fe^{3+}}$ の場合。$\\mathrm{Fe^{2+}}$ の検出にはヘキサシアニド鉄(Ⅲ)酸カリウムを用いる。"),
            ("硫酸銅(Ⅱ)の無水物は青色で、水を吸収すると白色になる。", "無水物が白色、五水和物が青色で、色の変化は逆である。"),
            ("二クロム酸イオンを含む水溶液を塩基性にすると、赤橙色が濃くなる。", "塩基性にするとクロム酸イオンが生じて黄色になる。"),
            ("テトラアンミン銅(Ⅱ)イオンは正四面体形の構造をもつ。", "テトラアンミン銅(Ⅱ)イオンは正方形。正四面体形はテトラアンミン亜鉛(Ⅱ)イオン。"),
            ("ジアンミン銀(Ⅰ)イオンは正方形の構造をもつ。", "配位数2のジアンミン銀(Ⅰ)イオンは直線形である。"),
            ("遷移元素には、非金属元素も金属元素も含まれる。", "遷移元素はすべて金属元素である。"),
            ("遷移元素のイオンは、すべて無色である。", "$\\mathrm{Cu^{2+}}$（青）・$\\mathrm{Fe^{3+}}$（黄褐）など、遷移元素のイオンには有色のものが多い。")]


@gen("standard_practice", 4, ["concept", "condition_check"])
def transition(r):
    if r.random() < 0.55:
        right = r.choice(TR_TRUE)
        wrong = r.sample(TR_FALSE, 3)
        why = {w: (reason, "遷移元素の性質の誤認") for w, reason in wrong}
        return mc("遷移元素とその化合物について述べた次の文のうち、正しいものを選びなさい。", [right] + [w for w, _ in wrong], f"正しいのは「{right}」。", d=3,
                  ap="鉄イオンの検出反応、銅・クロムの化合物の色の変化、錯イオンの形を整理しておく。",
                  steps=["各文の物質・反応を確認する。", "鉄の検出：Fe³⁺ は KSCN で血赤色、Fe²⁺ は K₃[Fe(CN)₆] で濃青色沈殿。", "錯イオンの形：配位数2は直線、Cu の4配位は正方形、Zn の4配位は正四面体、6配位は正八面体。",
                         f"正しいのは「{right}」。"],
                  alt=["誤りの文を、正しい内容に書き直してみる。"],
                  pc=[("性質を正しく判断している", 2), ("正しく選んでいる", 2)], why=why, pit=["$\\mathrm{Fe^{2+}}$ と $\\mathrm{Fe^{3+}}$ の検出試薬を混同する。"])
    w, reason = r.choice(TR_FALSE)
    rights = r.sample(TR_TRUE, 3)
    why = {x: ("この文は事実と合っている。", "正しい記述を誤りと判断している") for x in rights}
    return mc("遷移元素とその化合物について述べた次の文のうち、誤っているものを選びなさい。", [w] + rights, f"誤っているのは「{w}」。{reason}", d=3,
              ap="検出反応の試薬とイオンの組み合わせ、色の変化の向き、錯イオンの形を1つずつ確認する。",
              steps=["各文を検討する。", f"「{w}」は誤り。", reason],
              alt=["正しい文についても、その反応式や理由を説明できるか確かめる。"],
              pc=[("誤りを見抜いている", 2), ("正しく選んでいる", 2)], why=why, pit=["色の変化の向き（無水物と水和物など）を逆に覚えている。"])


GASRX = [("酸化マンガン(Ⅳ)", "MnO2", "塩素", "Cl2", "\\mathrm{MnO_2}+4\\mathrm{HCl}\\longrightarrow\\mathrm{MnCl_2}+\\mathrm{Cl_2}+2\\mathrm{H_2O}", 1, 1, "に濃塩酸を加えて加熱"),
         ("銅", "Cu", "二酸化窒素", "NO2", "\\mathrm{Cu}+4\\mathrm{HNO_3}\\longrightarrow\\mathrm{Cu(NO_3)_2}+2\\mathrm{NO_2}+2\\mathrm{H_2O}", 1, 2, "に濃硝酸を加え"),
         ("銅", "Cu", "一酸化窒素", "NO", "3\\mathrm{Cu}+8\\mathrm{HNO_3}\\longrightarrow3\\mathrm{Cu(NO_3)_2}+2\\mathrm{NO}+4\\mathrm{H_2O}", 3, 2, "に希硝酸を加え"),
         ("銅", "Cu", "二酸化硫黄", "SO2", "\\mathrm{Cu}+2\\mathrm{H_2SO_4}\\longrightarrow\\mathrm{CuSO_4}+\\mathrm{SO_2}+2\\mathrm{H_2O}", 1, 1, "に濃硫酸を加えて加熱"),
         ("塩化アンモニウム", "NH4Cl", "アンモニア", "NH3", "2\\mathrm{NH_4Cl}+\\mathrm{Ca(OH)_2}\\longrightarrow\\mathrm{CaCl_2}+2\\mathrm{H_2O}+2\\mathrm{NH_3}", 2, 2, "と十分な量の水酸化カルシウムの混合物を加熱"),
         ("炭酸カルシウム", "CaCO3", "二酸化炭素", "CO2", "\\mathrm{CaCO_3}+2\\mathrm{HCl}\\longrightarrow\\mathrm{CaCl_2}+\\mathrm{H_2O}+\\mathrm{CO_2}", 1, 1, "に十分な量の希塩酸を加え"),
         ("塩素酸カリウム", "KClO3", "酸素", "O2", "2\\mathrm{KClO_3}\\longrightarrow2\\mathrm{KCl}+3\\mathrm{O_2}", 2, 3, "に少量の酸化マンガン(Ⅳ)を加えて加熱"),
         ("アルミニウム", "Al", "水素", "H2", "2\\mathrm{Al}+2\\mathrm{NaOH}+6\\mathrm{H_2O}\\longrightarrow2\\mathrm{Na[Al(OH)_4]}+3\\mathrm{H_2}", 2, 3, "に十分な量の水酸化ナトリウム水溶液を加え"),
         ("塩化ナトリウム", "NaCl", "塩化水素", "HCl", "\\mathrm{NaCl}+\\mathrm{H_2SO_4}\\longrightarrow\\mathrm{NaHSO_4}+\\mathrm{HCl}", 1, 1, "に濃硫酸を加えて加熱"),
         ("亜鉛", "Zn", "水素", "H2", "\\mathrm{Zn}+\\mathrm{H_2SO_4}\\longrightarrow\\mathrm{ZnSO_4}+\\mathrm{H_2}", 1, 1, "に十分な量の希硫酸を加え")]


@gen("standard_practice", 4, ["computation", "application"], rel=["HS-CHEB-U02"])
def gas_amount(r):
    rn, rf, gn, gf, eq, a, b, how = r.choice(GASRX)
    if rf == "KClO3":
        aw = "原子量は O＝16、Cl＝35.5、K＝39 とする。"
    else:
        aw = aw_note(rf)
    for _ in range(100):
        n = sp.Rational(r.choice(["0.010", "0.020", "0.050", "0.10", "0.030", "0.040", "0.0050", "0.20"]))
        w = n * M(rf)
        if clean(w, 3):
            break
    V = n * b / a * sp.Rational("22.4")
    return numq(f"{rn} ${tex(rf)}$ {dec(w)} g{how}たところ、{rn}はすべて反応して{gn}が発生した。発生した{gn}の体積は{STP}で何 L か。反応は ${eq}$ で表される。{aw}標準状態の気体のモル体積は 22.4 L/mol とする。",
                V, f"{w}/({M(rf)})*{b}/({a})*22.4", f"{rn} {dec(n)} mol と係数の比 {a}：{b} から{gn}の物質量を求める。", unit="L", d=3, n=2,
                ap="反応式の係数の比から、原料の物質量と気体の物質量の関係を求める（物質量と気体の体積は化学基礎の内容）。",
                steps=[f"{rn}：$\\dfrac{{{dec(w)}}}{{{dec(M(rf))}}}={dec(n)}$ mol。", f"{gn}：${dec(n)}\\times\\dfrac{{{b}}}{{{a}}}={sig(n * b / a, 3)}$ mol。",
                       f"体積：${sig(n * b / a, 3)}\\times22.4={sig(V)}$ L。"],
                alt=[f"質量と体積の比例式 ${a}\\times{dec(M(rf))}\\,\\mathrm{{g}}:{b}\\times22.4\\,\\mathrm{{L}}={dec(w)}\\,\\mathrm{{g}}:V$ でもよい。"],
                pc=[("係数の比を正しく用いている", 2), ("体積が正しい", 2)], pit=["係数の比を 1：1 とする。", "濃硝酸と希硝酸の反応式を取り違える。"])


# ======================================================================
# C 思考力・記述応用
# ======================================================================

SEP_PAIRS = [("Ag+", "Cu2+", "希塩酸を加える", "AgCl", "白色", "$\\mathrm{Cu^{2+}}$ の塩化物は水に溶けるので沈殿しない。", "アンモニア水を過剰に加える", "どちらもアンミン錯イオンをつくって溶けてしまう"),
             ("Al3+", "Zn2+", "アンモニア水を過剰に加える", "Al(OH)3", "白色", "$\\mathrm{Zn^{2+}}$ は $[\\mathrm{Zn(NH_3)_4}]^{2+}$ となって溶ける。", "水酸化ナトリウム水溶液を過剰に加える", "どちらも両性で、水酸化物が溶けてしまう"),
             ("Fe3+", "Al3+", "水酸化ナトリウム水溶液を過剰に加える", "Fe(OH)3", "赤褐色", "$\\mathrm{Al(OH)_3}$ は両性なので $[\\mathrm{Al(OH)_4}]^-$ となって溶ける。", "アンモニア水を過剰に加える", "どちらも水酸化物として沈殿し、溶けない"),
             ("Cu2+", "Zn2+", "塩酸で酸性にして硫化水素を通じる", "CuS", "黒色", "酸性では $\\mathrm{S^{2-}}$ の濃度が小さく、$\\mathrm{ZnS}$ は沈殿しない。", "アンモニア水を過剰に加える", "どちらもアンミン錯イオンをつくって溶けてしまう"),
             ("Fe3+", "Zn2+", "アンモニア水を過剰に加える", "Fe(OH)3", "赤褐色", "$\\mathrm{Zn^{2+}}$ は $[\\mathrm{Zn(NH_3)_4}]^{2+}$ となって溶ける。", "（Zn²⁺ を除かずに）硫化水素を塩基性で通じる", "ZnS も沈殿し、鉄の沈殿と混ざってしまう"),
             ("Cu2+", "Fe3+", "アンモニア水を過剰に加える", "Fe(OH)3", "赤褐色", "$\\mathrm{Cu^{2+}}$ は深青色の $[\\mathrm{Cu(NH_3)_4}]^{2+}$ となって溶ける。", "水酸化ナトリウム水溶液を過剰に加える", "どちらも水酸化物として沈殿し、溶けない"),
             ("Mg2+", "Al3+", "水酸化ナトリウム水溶液を過剰に加える", "Mg(OH)2", "白色", "$\\mathrm{Al(OH)_3}$ は両性なので $[\\mathrm{Al(OH)_4}]^-$ となって溶ける。", "アンモニア水を過剰に加える", "どちらも白色の水酸化物として沈殿する"),
             ("Ag+", "Zn2+", "希塩酸を加える", "AgCl", "白色", "$\\mathrm{Zn^{2+}}$ の塩化物は水に溶けるので沈殿しない。", "アンモニア水を過剰に加える", "どちらもアンミン錯イオンをつくって溶けてしまう"),
             ("Pb2+", "Cu2+", "希塩酸を加える", "PbCl2", "白色", "$\\mathrm{Cu^{2+}}$ の塩化物は水に溶けるので沈殿しない。", "塩酸で酸性にして硫化水素を通じる", "PbS も CuS もともに黒色沈殿になってしまう"),
             ("Ca2+", "Na+", "炭酸アンモニウム水溶液を加える", "CaCO3", "白色", "ナトリウムの炭酸塩は水に溶けるので沈殿しない。", "塩酸で酸性にして硫化水素を通じる", "どちらも沈殿せず分離できない")]


@gen("thinking_writing", 4, ["written_reasoning", "condition_check"])
def separation_design(r):
    a, b, reagent, ppt, col, why_b, bad, bad_why = r.choice(SEP_PAIRS)
    if r.random() < 0.5:
        a_, b_ = a, b
    else:
        a_, b_ = b, a
    return desc(f"${ion(a_)}$ と ${ion(b_)}$ を含む水溶液から、${ion(a)}$ を沈殿として分離したい。\n(1) 加える試薬と操作を答え、生じる沈殿の化学式と色を書きなさい。\n"
                f"(2) そのとき ${ion(b)}$ が沈殿しない（または溶ける）理由を説明しなさい。\n(3) 「{bad}」方法では分離できない。その理由を説明しなさい。",
                f"(1) {reagent}。${tex(ppt)}$（{col}）が沈殿するので、ろ過して分離する。(2) {why_b}(3) {bad_why}ため。",
                "2つのイオンの「沈殿のでき方の違い」を探す。両性・錯イオン・塩化物や硫化物の溶けにくさのどれで差がつくかを考える。",
                [("(1) 適切な試薬・操作を答えている", 2), ("(1) 沈殿の化学式と色が正しい", 2), ("(2) もう一方のイオンが沈殿しない理由を説明している", 2), ("(3) 不適切な方法の理由を説明している", 2)],
                d=4, p=8, lines=8,
                ap="それぞれのイオンについて、塩化物・硫化物・水酸化物の沈殿のでき方と、NaOH 過剰・NH₃ 過剰での溶け方を表にして比べる。",
                steps=[f"${ion(a)}$ と ${ion(b)}$ の性質を比べる。", f"差がつく試薬：{reagent} → ${tex(ppt)}$（{col}）。", why_b, f"「{bad}」では、{bad_why}。"],
                alt=["別の試薬で分離できる場合もある（例：Cu²⁺ と Zn²⁺ は NaOH 過剰でも分離できる）。複数の方法を比べて、より確実な方法を選んだ理由を書いてもよい。"],
                pc=[("試薬", 2), ("沈殿", 2), ("理由", 2), ("不適の理由", 2)],
                pit=["両性元素とアンミン錯イオンをつくる元素を混同する。", "沈殿の色を書き忘れる。"])


IND_C = [("contact", "接触法では、硫黄を燃焼させて $\\mathrm{SO_2}$ とし、酸化バナジウム(Ⅴ) を触媒として $\\mathrm{SO_3}$ に酸化する。$\\mathrm{SO_3}$ は濃硫酸に吸収させて発煙硫酸とし、これを希硫酸でうすめて濃硫酸にする。",
          "S+O2→SO2、2SO2+O2→2SO3、SO3+H2O→H2SO4", "S", "H2SO4", 1, 1, "硫黄", "硫酸",
          "$\\mathrm{SO_3}$ を直接水に吸収させないのは、水との反応が激しく多量の熱が発生し、霧状になって吸収されにくいから。",
          "2SO₂＋O₂ ⇄ 2SO₃ は発熱反応で、低温ほど平衡は右に移動するが、低温では反応が遅いため、触媒を用いて適当な温度で反応させる。"),
         ("ostwald", "オストワルト法では、白金を触媒としてアンモニアを酸化して一酸化窒素とし、これをさらに酸化して二酸化窒素とする。二酸化窒素を水に吸収させると硝酸が得られ、同時に生じる一酸化窒素は再び酸化に使われる。",
          "4NH3+5O2→4NO+6H2O、2NO+O2→2NO2、3NO2+H2O→2HNO3+NO", "NH3", "HNO3", 1, 1, "アンモニア", "硝酸",
          "3NO₂＋H₂O → 2HNO₃＋NO で生じた NO をくり返し酸化して使うので、最終的に NH₃ の N 原子はすべて HNO₃ になる（全体で NH₃＋2O₂ → HNO₃＋H₂O）。",
          "アンモニアの酸化は触媒（白金）がないと進みにくい。触媒は反応を速くして、目的の NO を効率よく得るために用いる。"),
         ("solvay", "アンモニアソーダ法では、塩化ナトリウムの飽和水溶液にアンモニアと二酸化炭素を吹き込んで炭酸水素ナトリウムを沈殿させ、これを加熱して炭酸ナトリウムを得る。副生する塩化アンモニウムからはアンモニアが回収される。",
          "NaCl+H2O+NH3+CO2→NaHCO3+NH4Cl、2NaHCO3→Na2CO3+H2O+CO2", "NaCl", "Na2CO3", 2, 1, "塩化ナトリウム", "炭酸ナトリウム",
          "炭酸水素ナトリウムは、この条件で水に溶けにくいので沈殿として取り出せる。全体の反応は 2NaCl＋CaCO₃ → Na₂CO₃＋CaCl₂ で、NaCl 2 mol から Na₂CO₃ 1 mol が得られる。",
          "加熱で生じる CO₂ や、回収した NH₃ は再利用され、原料のむだが少ない。")]


def eqs_tex(s):
    def one(e):
        l, rr = e.split("→")
        def side(x):
            out = []
            for t in x.split("+"):
                m = re.match(r"(\d*)(.*)", t)
                out.append((m.group(1) if m.group(1) not in ("", "1") else "") + tex(m.group(2)))
            return "+".join(out)
        return f"${side(l)}\\longrightarrow{side(rr)}$"
    return "、".join(one(e) for e in s.split("、"))


@gen("thinking_writing", 3, ["cross_unit", "computation", "written_reasoning"], rel=["HS-CHE-U02", "HS-CHEB-U02"])
def industrial_explain(r):
    key, intro_, eqs, rf, pf, a, b, rn, pn, point1, point2 = r.choice(IND_C)
    for _ in range(100):
        n = sp.Rational(r.choice(["1.0", "2.0", "5.0", "0.50", "4.0", "10", "3.0"])) * 1000
        w = n * a * M(rf) / 1000
        if clean(w, 3):
            break
    wp = n * b * M(pf) / 1000
    extra = ""
    ans_extra = ""
    if key == "contact":
        extra = "また、得られた硫酸から質量パーセント濃度 98 % の濃硫酸をつくると、何 kg になるか。"
        ans_extra = f"98 % の濃硫酸は ${sig(wp, 3)}\\div0.98\\fallingdotseq{sig(wp / sp.Rational('0.98'), 3)}$ kg。"
    return desc(f"{intro_}主な反応は {eqs_tex(eqs)} である。\n(1) この製法の工夫について、次の観点から説明しなさい。"
                + ("「$\\mathrm{SO_3}$ を直接水に吸収させない理由」と「触媒と温度の関係」" if key == "contact" else ("「NO の再利用と全体の反応」と「触媒の役割」" if key == "ostwald" else "「炭酸水素ナトリウムが沈殿する理由と全体の反応」と「原料の再利用」"))
                + f"\n(2) {rn} {dec(w)} kg から得られる{pn}は最大何 kg か。{extra}{aw_note(rf, pf)}有効数字3桁で答えなさい。",
                f"(1) {point1}{point2}(2) {rn} ${sig(n * a, 3)}$ mol から{pn} ${sig(n * b, 3)}$ mol（物質量の比 {a}：{b}）、${sig(wp, 3)}$ kg。{ans_extra}",
                "工業的製法は「平衡・速度・原料の再利用」の工夫の組み合わせ。量的関係は注目する原子の保存で考える。",
                [("(1) 1つ目の観点を正しく説明している", 2), ("(1) 2つ目の観点を正しく説明している", 2), ("(2) 原料と製品の物質量の比を正しく用いている", 2), ("(2) 値が正しい", 2)],
                d=5, p=8, lines=10,
                ap="(1) は化学平衡・反応速度（前単元）の考え方を使う。(2) は全体の反応式をつくり、原料と製品の物質量の比を求める（物質量は化学基礎の内容）。",
                steps=["各段階の反応式を足し合わせ、途中の物質を消去して全体の反応式をつくる。", f"全体として{rn}と{pn}の物質量の比は {a}：{b}。",
                       f"{rn}：$\\dfrac{{{dec(w)}\\times10^3}}{{{dec(M(rf))}}}={sig(n * a, 3)}$ mol → {pn}：${sig(n * b, 3)}$ mol。", f"質量：${sig(wp, 3)}$ kg。" + ans_extra],
                alt=["注目する原子（S・N・Na）の数が最初から最後まで保存されると考えれば、全体の反応式をつくらなくても比が分かる。"],
                pc=[("観点1", 2), ("観点2", 2), ("比", 2), ("値", 2)],
                pit=["途中の反応式の係数（例：3NO₂ → 2HNO₃）をそのまま全体の比として使う。", "kg と g の換算を誤る。"],
                chk=(f"{w}*1000/({M(rf)})*{b}/({a})*({M(pf)})/1000", str(wp), None, "intermediate"))


SALTS = {"NaCl": ("塩化ナトリウム", "黄色", "白色沈殿（AgCl）", "変化なし", "無色"), "KCl": ("塩化カリウム", "赤紫色", "白色沈殿（AgCl）", "変化なし", "無色"),
         "CaCl2": ("塩化カルシウム", "橙赤色", "白色沈殿（AgCl）", "変化なし", "無色"), "BaCl2": ("塩化バリウム", "黄緑色", "白色沈殿（AgCl）", "変化なし", "無色"),
         "Na2SO4": ("硫酸ナトリウム", "黄色", "—", "白色沈殿（BaSO₄）", "無色"), "K2SO4": ("硫酸カリウム", "赤紫色", "—", "白色沈殿（BaSO₄）", "無色"),
         "CuSO4": ("硫酸銅(Ⅱ)", "青緑色", "—", "白色沈殿（BaSO₄）", "青色"), "CuCl2": ("塩化銅(Ⅱ)", "青緑色", "白色沈殿（AgCl）", "変化なし", "青色"),
         "NaBr": ("臭化ナトリウム", "黄色", "淡黄色沈殿（AgBr）", "変化なし", "無色"), "KI": ("ヨウ化カリウム", "赤紫色", "黄色沈殿（AgI）", "変化なし", "無色"),
         "LiCl": ("塩化リチウム", "赤色", "白色沈殿（AgCl）", "変化なし", "無色")}


@gen("thinking_writing", 3, ["written_reasoning", "application"])
def identify_salt(r):
    for _ in range(200):
        cands = r.sample(list(SALTS), 4)
        t = r.choice(cands)
        sig_ = lambda k: (SALTS[k][1], SALTS[k][2] if SALTS[k][2] != "—" else None, SALTS[k][3], SALTS[k][4])  # noqa: E731
        if sum(1 for c in cands if sig_(c) == sig_(t)) == 1:
            break
    nm_, fl, ag, ba, col = SALTS[t]
    obs = [f"水溶液は{col}であった。", f"白金線につけて炎色反応を調べると{fl}を示した。"]
    if ag != "—":
        obs.append(f"硝酸銀水溶液を加えると{ag.split('（')[0]}が生じた。")
    obs.append(f"塩化バリウム水溶液を加えると{'白色沈殿が生じ、この沈殿は希塩酸を加えても溶けなかった' if ba != '変化なし' else '変化は見られなかった'}。")
    names = "、".join(f"{SALTS[c][0]}" for c in cands)
    anion = "SO4" if "SO4" in t else ("Cl" if "Cl" in t else ("Br" if "Br" in t else "I"))
    if anion == "SO4":
        ionic = "\\mathrm{Ba^{2+}}+\\mathrm{SO_4^{2-}}\\longrightarrow\\mathrm{BaSO_4}"
    else:
        ionic = f"\\mathrm{{Ag^+}}+\\mathrm{{{anion}^-}}\\longrightarrow\\mathrm{{Ag{anion}}}"
    return desc(f"ある塩の水溶液 X について、次の観察を行った。X は {names} のいずれかである。\n" + "\n".join(f"〔観察{i + 1}〕{o}" for i, o in enumerate(obs))
                + "\n(1) X は何か。判断の根拠を、観察結果と結びつけて説明しなさい。\n(2) 観察のうち沈殿が生じた反応の1つを、イオン反応式で表しなさい。",
                f"(1) {nm_}。炎色反応の{fl}から陽イオンが決まり、" + ("硝酸銀で" + ag + "が生じたことから陰イオンが決まる。" if ag != "—" else "塩化バリウムで希塩酸に溶けない白色沈殿（BaSO₄）が生じたことから硫酸イオンを含む。")
                + f"(2) ${ionic}$",
                "陽イオンは炎色反応と水溶液の色、陰イオンは銀イオン・バリウムイオンとの沈殿で判断する。",
                [("(1) 物質名が正しい", 2), ("(1) 陽イオンの判断の根拠を述べている", 2), ("(1) 陰イオンの判断の根拠を述べている", 2), ("(2) イオン反応式が正しい", 2)],
                d=4, p=8, lines=8,
                ap="陽イオンと陰イオンを別々に特定する。炎色反応（Li 赤、Na 黄、K 赤紫、Ca 橙赤、Ba 黄緑、Cu 青緑）と、沈殿の色（AgCl 白・AgBr 淡黄・AgI 黄、BaSO₄ 白）を手がかりにする。",
                steps=[f"炎色反応 {fl} → 陽イオンを特定。", "沈殿反応 → 陰イオンを特定。", f"候補の中で両方に合うのは{nm_}。", f"イオン反応式：${ionic}$。"],
                alt=["候補を1つずつ観察結果と照らし合わせ、合わない観察を挙げて消去していく方法でもよい。"],
                pc=[("物質名", 2), ("陽イオン", 2), ("陰イオン", 2), ("反応式", 2)],
                pit=["炎色反応の色を取り違える。", "硫酸イオンの検出に硝酸銀を使えると考える。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

GAS_ERR = [("NH3", "アンモニア", "塩化アンモニウムと水酸化カルシウムの混合物を加熱して発生させ、濃硫酸に通して乾燥させてから水上置換で集める",
            "乾燥剤と捕集法", "アンモニアは塩基性なので濃硫酸と反応してしまう。また水に非常によく溶けるので水上置換では集められない",
            "ソーダ石灰で乾燥させ、上方置換で集める", "乾燥剤は気体と反応しないもの、捕集法は水への溶解性と密度で選ぶ。"),
           ("HCl", "塩化水素", "塩化ナトリウムに濃硫酸を加えて加熱して発生させ、ソーダ石灰で乾燥させてから上方置換で集める",
            "乾燥剤と捕集法", "塩化水素は酸性なので塩基性のソーダ石灰と反応する。また分子量 36.5 で空気より重い",
            "濃硫酸で乾燥させ、下方置換で集める", "酸性の気体に塩基性の乾燥剤は使えない。空気（約 29）より重い気体は下方置換。"),
           ("Cl2", "塩素", "酸化マンガン(Ⅳ)に希塩酸を加えて発生させ、水上置換で集める",
            "用いる酸と捕集法", "この反応には濃塩酸と加熱が必要である。また塩素は水に溶けやすく空気より重い",
            "酸化マンガン(Ⅳ)に濃塩酸を加えて加熱して発生させ、水・濃硫酸に順に通して精製・乾燥し、下方置換で集める", "反応の条件（濃度・加熱）と、気体の溶解性・密度を確認する。"),
           ("CO2", "二酸化炭素", "炭酸カルシウムに希塩酸を加えて発生させ、ソーダ石灰で乾燥させてから上方置換で集める",
            "乾燥剤と捕集法", "二酸化炭素は酸性の気体なので、塩基性のソーダ石灰に吸収されてしまう。また分子量 44 で空気より重い",
            "塩化カルシウムや濃硫酸で乾燥させ、下方置換（または水上置換）で集める", "酸性の気体の乾燥には酸性・中性の乾燥剤を使う。")]


@gen("error_correction", 3, ["common_error", "condition_check"])
def err_gas(r):
    f, nm_, wrong, step, reason, fix, expl = r.choice(GAS_ERR)
    lead = r.choice(["次の気体を実験室で得る方法を答えなさい。", "次の気体の発生・乾燥・捕集の方法を答えなさい。"])
    return err_item(f"{lead}\n{nm_} ${tex(f)}$", wrong, step, "condition",
                    "発生方法は覚えているが、気体の性質（酸性・塩基性、水への溶けやすさ、空気との重さの比較）から乾燥剤や捕集法を選ぶ手順を踏んでいない。",
                    fix, fix, f"{reason}。{expl}",
                    [f"{nm_}の性質：分子量 {GAS[f][3]}、{GAS[f][4]}の気体、水に{'溶けにくい' if GAS[f][2] == '水上置換' else '溶けやすい'}。", f"→ {fix}。"],
                    "気体の「液性」「水への溶解性」「分子量（29 との比較）」の3点を書き出してから方法を決める。",
                    ["乾燥剤と気体の組み合わせが中和反応にならないかを確かめる。"], ["酸性・塩基性の乾燥剤と気体の組み合わせを考えない。"], d=2)


SEP_ERR = [("Al3+", "Zn2+", "水酸化ナトリウム水溶液を過剰に加えると、$\\mathrm{Al(OH)_3}$ が沈殿して $\\mathrm{Zn^{2+}}$ と分離できる",
            "水酸化ナトリウム水溶液を過剰に加えるとした部分", "$\\mathrm{Al(OH)_3}$ も $\\mathrm{Zn(OH)_2}$ も両性のため、過剰の NaOH で溶けてしまう",
            "アンモニア水を過剰に加えると、$\\mathrm{Al(OH)_3}$ だけが沈殿し、$\\mathrm{Zn^{2+}}$ は $[\\mathrm{Zn(NH_3)_4}]^{2+}$ となって溶ける"),
           ("Cu2+", "Zn2+", "アンモニア水を過剰に加えると、$\\mathrm{Cu(OH)_2}$ が沈殿して $\\mathrm{Zn^{2+}}$ と分離できる",
            "アンモニア水を過剰に加えるとした部分", "$\\mathrm{Cu^{2+}}$ も $\\mathrm{Zn^{2+}}$ もアンミン錯イオンをつくって溶けてしまう",
            "塩酸で酸性にして硫化水素を通じると CuS（黒）だけが沈殿する（または NaOH 過剰で Cu(OH)₂ だけが残る）"),
           ("Ag+", "Pb2+", "希塩酸を加えると AgCl だけが沈殿し、$\\mathrm{Pb^{2+}}$ と分離できる",
            "希塩酸で AgCl だけが沈殿するとした部分", "$\\mathrm{Pb^{2+}}$ も $\\mathrm{PbCl_2}$（白）として沈殿する",
            "希塩酸で両方を沈殿させた後、熱湯を注ぐと PbCl₂ が溶け、AgCl が残るので分離できる"),
           ("Fe3+", "Al3+", "アンモニア水を過剰に加えると、$\\mathrm{Fe(OH)_3}$ だけが沈殿して $\\mathrm{Al^{3+}}$ と分離できる",
            "アンモニア水を過剰に加えるとした部分", "$\\mathrm{Al(OH)_3}$ はアンモニア水には溶けないので、$\\mathrm{Fe(OH)_3}$ と一緒に沈殿する",
            "水酸化ナトリウム水溶液を過剰に加えると、$\\mathrm{Fe(OH)_3}$（赤褐）だけが沈殿し、$\\mathrm{Al^{3+}}$ は $[\\mathrm{Al(OH)_4}]^-$ となって溶ける"),
           ("Ag+", "Cu2+", "最初に硫化水素を通じると CuS が沈殿し、その後に希塩酸を加えると AgCl が沈殿する",
            "操作の順序", "最初に硫化水素を通じると、$\\mathrm{Ag^+}$ も $\\mathrm{Ag_2S}$（黒）として CuS と一緒に沈殿してしまう",
            "先に希塩酸を加えて AgCl を沈殿させ、ろ液に硫化水素を通じて CuS を沈殿させる")]


@gen("error_correction", 4, ["common_error", "concept"])
def err_separation(r):
    a, b, wrong, step, reason, fix = r.choice(SEP_ERR)
    lead = r.choice(["分離する方法を答えなさい。", "分離するための試薬と操作を説明しなさい。"])
    return err_item(f"${ion(a)}$ と ${ion(b)}$ を含む水溶液から、それぞれのイオンを{lead}", wrong, step, "concept",
                    "1つのイオンの性質（沈殿をつくる・溶ける）だけを考え、もう一方のイオンが同じ試薬でどうなるかを確かめていない。",
                    fix, fix, f"{reason}。",
                    [f"${ion(a)}$ と ${ion(b)}$ のそれぞれについて、試薬を加えたときの変化を確認する。", reason + "。", f"→ {fix}。"],
                    "分離では「一方は沈殿し、もう一方は沈殿しない（溶ける）」試薬を選ぶ。両方のイオンについて必ず確かめる。",
                    ["NaOH 少量・過剰、NH₃ 少量・過剰、HCl、H₂S（酸性・塩基性）での変化の表をつくり、差がつく列を探す。"], ["もう一方のイオンの変化を確かめない。"], d=3)


@gen("error_correction", 3, ["common_error", "computation"])
def err_industrial(r):
    form = r.choice(["solvay", "contact98", "ostwald"])
    if form == "solvay":
        for _ in range(100):
            n = sp.Rational(r.choice(["1.0", "2.0", "4.0", "10", "5.0"])) * 1000
            w = n * 2 * M("NaCl") / 1000
            if clean(w, 4):
                break
        right = n * M("Na2CO3") / 1000
        wrong = right * 2
        return err_item(f"アンモニアソーダ法で、塩化ナトリウム {dec(w)} kg から得られる炭酸ナトリウムは最大何 kg か。全体の反応は $2\\mathrm{{NaCl}}+\\mathrm{{CaCO_3}}\\longrightarrow\\mathrm{{Na_2CO_3}}+\\mathrm{{CaCl_2}}$ で表される。{aw_note('NaCl', 'Na2CO3')}有効数字3桁で答えなさい。",
                        f"NaCl は $\\dfrac{{{dec(w)}\\times10^3}}{{58.5}}={sig(2 * n, 3)}$ mol なので、$\\mathrm{{Na_2CO_3}}$ も ${sig(2 * n, 3)}$ mol。${sig(2 * n, 3)}\\times106\\times10^{{-3}}={sig(wrong, 3)}$ kg",
                        "物質量の比を 1：1 とした部分", "calculation",
                        "物質量に直すところまではできているが、全体の反応式の係数（NaCl 2 mol から Na₂CO₃ 1 mol）を確認していない。",
                        f"$\\mathrm{{Na_2CO_3}}$ は NaCl の $\\dfrac{{1}}{{2}}$ の ${sig(n, 3)}$ mol で、${sig(right, 3)}$ kg", f"${sig(right, 3)}$ kg",
                        "Na 原子の数で考えると、$\\mathrm{Na_2CO_3}$ 1 個に Na が 2 個含まれるので、NaCl 2 mol から $\\mathrm{Na_2CO_3}$ 1 mol しか得られない。",
                        [f"NaCl：${sig(2 * n, 3)}$ mol。", f"係数の比 2：1 より $\\mathrm{{Na_2CO_3}}$：${sig(n, 3)}$ mol。", f"質量：${sig(n, 3)}\\times106\\times10^{{-3}}={sig(right, 3)}$ kg。"],
                        "注目する原子（Na）の数が保存されるかを確かめる。",
                        ["誤答では Na 原子の数が反応の前後で2倍に増えてしまう、という矛盾から誤りに気づける。"], ["係数の比を確認しない。"],
                        chk=(f"{w}*1000/(58.5)/2*106/1000", str(right), None, "intermediate"), d=3)
    if form == "contact98":
        for _ in range(100):
            n = sp.Rational(r.choice(["1.0", "2.0", "4.0", "10", "5.0", "3.0"])) * 1000
            w = n * 32 / 1000
            if clean(w, 3):
                break
        pure = n * 98 / 1000
        right = pure / sp.Rational("0.98")
        wrong = pure * sp.Rational("0.98")
        return err_item(f"接触法で、硫黄 {dec(w)} kg をすべて硫酸にしたとき、質量パーセント濃度 98 % の濃硫酸は何 kg 得られるか。原子量は H＝1.0、O＝16、S＝32 とする。有効数字3桁で答えなさい。",
                        f"$\\mathrm{{H_2SO_4}}$ は ${sig(n, 3)}$ mol で ${sig(pure, 3)}$ kg。98 % なので ${sig(pure, 3)}\\times0.98={sig(wrong, 3)}$ kg",
                        "濃度 98 % の扱い", "concept",
                        "「98 %」という数を見て機械的に掛けてしまい、濃硫酸（溶液）の質量と、その中の純粋な硫酸（溶質）の質量の関係を考えていない。",
                        f"溶液の質量 × 0.98 ＝ 硫酸の質量 なので、溶液は ${sig(pure, 3)}\\div0.98={sig(right, 3)}$ kg", f"${sig(right, 3)}$ kg",
                        "質量パーセント濃度は「溶質の質量÷溶液の質量」。純粋な硫酸より溶液（濃硫酸）の方が重くなるはずである。",
                        [f"S：${sig(n, 3)}$ mol → $\\mathrm{{H_2SO_4}}$：${sig(n, 3)}$ mol＝${sig(pure, 3)}$ kg。", f"濃硫酸の質量を $x$ とすると $0.98x={sig(pure, 3)}$。", f"$x={sig(right, 3)}$ kg。"],
                        "濃度の計算では、求める量が溶液か溶質かを先に決める。",
                        ["溶液の質量は溶質の質量より大きくなる、という大小関係で確かめる。"], ["濃度を掛けるか割るかを取り違える。"],
                        chk=(f"{w}*1000/32*98/1000/(98/100)", str(right), None, "intermediate"), d=3)
    for _ in range(100):
        n = sp.Rational(r.choice(["1.0", "2.0", "4.0", "10", "5.0", "3.0"])) * 1000
        w = n * 17 / 1000
        if clean(w, 3):
            break
    right = n * 63 / 1000
    wrong = n * sp.Rational(2, 3) * 63 / 1000
    return err_item(f"オストワルト法で、アンモニア {dec(w)} kg からつくられる硝酸は最大何 kg か。主な反応は $4\\mathrm{{NH_3}}+5\\mathrm{{O_2}}\\longrightarrow4\\mathrm{{NO}}+6\\mathrm{{H_2O}}$、$2\\mathrm{{NO}}+\\mathrm{{O_2}}\\longrightarrow2\\mathrm{{NO_2}}$、$3\\mathrm{{NO_2}}+\\mathrm{{H_2O}}\\longrightarrow2\\mathrm{{HNO_3}}+\\mathrm{{NO}}$ であり、生じた NO はすべて再利用されるものとする。原子量は H＝1.0、N＝14、O＝16 とする。有効数字3桁で答えなさい。",
                    f"$\\mathrm{{NH_3}}$ ${sig(n, 3)}$ mol → NO ${sig(n, 3)}$ mol → $\\mathrm{{NO_2}}$ ${sig(n, 3)}$ mol → $\\mathrm{{HNO_3}}$ はその $\\dfrac{{2}}{{3}}$ で ${sig(n * sp.Rational(2, 3), 3)}$ mol、${sig(wrong, 3)}$ kg",
                    "3NO₂ → 2HNO₃ の比をそのまま使った部分", "condition",
                    "3段目の式の係数だけを見て、生じた NO が再び酸化されて使われる（再利用される）という条件を反映していない。",
                    f"NO を再利用すると全体は $\\mathrm{{NH_3}}+2\\mathrm{{O_2}}\\longrightarrow\\mathrm{{HNO_3}}+\\mathrm{{H_2O}}$ で、$\\mathrm{{HNO_3}}$ は ${sig(n, 3)}$ mol、${sig(right, 3)}$ kg", f"${sig(right, 3)}$ kg",
                    "NO がすべて再利用されるので、N 原子はすべて HNO₃ になる。全体の反応式で NH₃：HNO₃＝1：1。",
                    ["3つの式を、NO と NO₂ が消えるように組み合わせると $\\mathrm{NH_3}+2\\mathrm{O_2}\\longrightarrow\\mathrm{HNO_3}+\\mathrm{H_2O}$。", f"$\\mathrm{{HNO_3}}$：${sig(n, 3)}$ mol。", f"${sig(n, 3)}\\times63\\times10^{{-3}}={sig(right, 3)}$ kg。"],
                    "問題文の条件（再利用など）を反映した全体の反応式をつくってから計算する。",
                    ["N 原子の数の保存で確かめる：NH₃ 1 個の N が最終的に HNO₃ 1 個になる。"], ["途中の式の係数だけで比を決める。"],
                    chk=(f"{w}*1000/17*63/1000", str(right), None, "intermediate"), d=3)


GENERATORS = [gas_prep, colors, flame, element_property, industrial,
              separation, amphoteric, halogen, transition, gas_amount,
              separation_design, industrial_explain, identify_salt,
              err_gas, err_separation, err_industrial]
