"""単元パック：物理 熱力学（気体の状態方程式、気体分子運動論、熱力学第一法則と気体の状態変化・熱効率）。"""
from decimal import ROUND_HALF_UP, Decimal

import sympy as sp

from banks._common import desc, figure, mc, num, plane
from hs_pack_lib import board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem, tp

UNIT_ID = "HS-PHY-U02"

R = sp.Rational(831, 100)
RS = "気体定数を $8.31\\,\\mathrm{J/(mol\\cdot K)}$ とする。"
KB = sp.Rational(138, 100) * sp.Rational(1, 10 ** 23)
NA = sp.Rational(60, 10) * 10 ** 23
G = sp.Rational("9.8")
MONO = "単原子分子理想気体"


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


def sci(mant, e):
    """表示用 mant×10^e の LaTeX と厳密値。"""
    return f"{mant}\\times10^{{{e}}}", Q(mant) * sp.Integer(10) ** e


def Ktx(T):
    return f"{T}\\,\\mathrm{{K}}"


# ----------------------------------------------------------------------
# 図
# ----------------------------------------------------------------------

def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="serif" font-size="12">'
            '<defs><marker id="ah" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#000"/></marker></defs>'
            f'{body}</svg>')


def cylinder_svg():
    body = '<line x1="60" y1="20" x2="60" y2="170" stroke="#000" stroke-width="2"/><line x1="180" y1="20" x2="180" y2="170" stroke="#000" stroke-width="2"/>'
    body += '<line x1="60" y1="170" x2="180" y2="170" stroke="#000" stroke-width="2"/>'
    body += '<rect x="61" y="70" width="118" height="16" fill="#9fb3c8" stroke="#000"/><text x="110" y="82">ピストン</text>'
    body += '<rect x="61" y="86" width="118" height="83" fill="#eef3f8"/><text x="100" y="135">気体</text>'
    body += '<line x1="120" y1="60" x2="120" y2="30" stroke="#000" marker-end="url(#ah)"/><text x="126" y="44">p₀</text>'
    body += '<path d="M 70 190 q 8 -10 16 0 q 8 10 16 0 q 8 -10 16 0" fill="none" stroke="#c0392b"/><text x="122" y="194">加熱</text>'
    return svg(240, 200, body)


def box_svg():
    body = '<rect x="20" y="20" width="160" height="120" fill="#f7f7f7" stroke="#000" stroke-width="1.5"/>'
    body += '<text x="186" y="84">壁 S</text><text x="90" y="156">L</text>'
    for (x, y) in [(60, 50), (120, 90), (80, 110), (150, 45), (45, 95)]:
        body += f'<circle cx="{x}" cy="{y}" r="4" fill="#1f4e79"/>'
    body += '<line x1="150" y1="45" x2="176" y2="45" stroke="#000" marker-end="url(#ah)"/><text x="150" y="38">v_x</text>'
    return svg(230, 165, body)


def pv_svg(pts, closed=False, xmax=7, ymax=5):
    segs = [(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    if closed:
        segs.append((pts[-1], pts[0]))
    return plane((0, xmax), (0, ymax), unit=30, grid=True, ticks=True, segments=segs,
                 polygons=[pts] if closed else [[(pts[0][0], 0)] + list(pts) + [(pts[-1][0], 0)]],
                 points=[(x, y, lab) for (x, y), lab in zip(pts, "ABCD")], xl="V", yl="p")


# ======================================================================
# 授業プリント
# ======================================================================

LESSON = lesson(
    goals=["ボイル・シャルルの法則と気体の状態方程式 $pV=nRT$ を用いて、気体の圧力・体積・温度・物質量の関係を求められる。",
           "気体分子の運動から圧力を導き、絶対温度が分子の平均運動エネルギーに比例することを説明できる。",
           "熱力学第一法則 $\\Delta U=Q+W$ を定積・定圧・等温・断熱変化に適用し、$p$−$V$ グラフから仕事と熱効率を求められる。"],
    duration=100,
    readiness=["絶対温度 $T=t+273$、熱量 $Q=mc\\Delta T$ と内部エネルギーの考え方を説明できる（物理基礎）。",
               "物質量（mol）とアボガドロ定数、モル質量の計算ができる（化学基礎）。",
               "運動量と力積の関係 $m\\Delta v=F\\Delta t$ を使える（物理 力学）。"],
    flow=[("導入：自転車の空気入れはなぜ熱くなる？", 5, "圧縮すると温度が上がる現象を示し、仕事と熱と内部エネルギーの関係を予告する"),
          ("気体の法則と状態方程式", 20, "ボイルの法則・シャルルの法則・ボイル・シャルルの法則、$pV=nRT$、例題1"),
          ("気体分子運動論", 20, "壁に当たる分子の力積から圧力を導く、平均運動エネルギーと絶対温度、二乗平均速度（例題2）"),
          ("内部エネルギーと第一法則", 15, "単原子分子の内部エネルギー $\\dfrac32nRT$、$\\Delta U=Q+W$ と符号の約束"),
          ("気体の状態変化", 20, "定積・定圧・等温・断熱、モル比熱とマイヤーの関係、$p$−$V$ グラフの面積＝仕事"),
          ("熱機関と熱効率", 10, "サイクルと熱効率（例題3）、熱力学第二法則の考え方"),
          ("まとめ", 10, "4つの状態変化の $Q,\\ W,\\ \\Delta U$ を表に整理し、課題を指示")],
    sections=[
        intro("in1", "目に見えない分子の運動で、気体のふるまいを説明する",
              "自転車のタイヤに空気入れで空気を押しこむと、空気入れの筒が熱くなる。気体に仕事をすると温度が上がるのはなぜだろうか。気体は膨大な数の分子からなり、分子は絶えず飛び回って容器の壁に衝突している。この単元では、圧力・温度という目に見える量を分子の運動と結びつけ、熱と仕事によるエネルギーのやりとり（熱力学第一法則）を気体の状態変化に当てはめる。",
              bullets=["マクロな量（圧力・体積・温度）は、状態方程式 $pV=nRT$ で結ばれる。",
                       "ミクロな分子運動から、圧力と温度の意味（分子の運動エネルギー）がわかる。",
                       "気体が受け取る熱と仕事の和が、内部エネルギーの増加になる。"],
              points=[tp("注射器の先をふさいでピストンを押し込み、手ごたえ（圧力）が増すことと、急激に押すと中の空気が温まることを体験させる。",
                         ask="ピストンを押すと、なぜ押し返す力が大きくなるのだろうか。分子の立場で説明してみよう。",
                         expect="同じ数の分子が狭い空間に入るので、壁に当たる回数が増える。", timing="授業の冒頭")]),
        definition("df1", "気体の状態方程式",
                   "一定量の気体の圧力 $p$〔Pa〕、体積 $V$〔m³〕、絶対温度 $T$〔K〕の間には、ボイルの法則（$T$ 一定で $pV=$ 一定）とシャルルの法則（$p$ 一定で $\\dfrac{V}{T}=$ 一定）をまとめたボイル・シャルルの法則が成り立つ。物質量 $n$〔mol〕を含めると状態方程式になる。",
                   formula="$$\\dfrac{pV}{T}=\\text{一定},\\qquad pV=nRT\\qquad(R\\fallingdotseq8.31\\,\\mathrm{J/(mol\\cdot K)})$$",
                   conditions=["温度は必ず絶対温度 $T=t+273$〔K〕を用いる。セルシウス温度のまま比を計算してはいけない。",
                               "単位をそろえる：$1\\,\\mathrm{L}=1\\times10^{-3}\\,\\mathrm{m^3}$、$1\\,\\mathrm{kPa}=1\\times10^3\\,\\mathrm{Pa}$。",
                               "状態方程式に厳密に従う気体を理想気体という。実在の気体も、高温・低圧ではほぼ理想気体とみなせる。",
                               "分子数 $N$ を用いると $pV=Nk_{\\mathrm{B}}T$（$k_{\\mathrm{B}}=\\dfrac{R}{N_{\\mathrm{A}}}\\fallingdotseq1.38\\times10^{-23}\\,\\mathrm{J/K}$：ボルツマン定数）。"],
                   points=[tp("ボイル・シャルルの法則で解ける問題（物質量が一定）と、状態方程式が必要な問題（物質量が変わる・物質量を問う）を区別させる。",
                              ask="容器の弁を開いて気体の一部が逃げた場合、ボイル・シャルルの法則は使えるか。",
                              expect="物質量が変わるので使えない。状態方程式で前後の $n$ を比べる。"),
                           tp("比の計算でセルシウス温度を使う誤りを、$0\\,{}^\\circ\\mathrm{C}$ から $27\\,{}^\\circ\\mathrm{C}$ への変化で体積が「無限大倍」になるおかしさから気づかせる。",
                              caution="℃ を K に直し忘れる誤りは非常に多い。")]),
        theorem("th1", "気体分子運動論：圧力と温度の意味",
                "$$p=\\dfrac{Nm\\overline{v^2}}{3V},\\qquad \\dfrac12m\\overline{v^2}=\\dfrac32k_{\\mathrm{B}}T,\\qquad \\sqrt{\\overline{v^2}}=\\sqrt{\\dfrac{3RT}{M}}$$",
                ["$N$ は分子数、$m$ は分子1個の質量、$\\overline{v^2}$ は速さの2乗の平均、$M$ はモル質量〔kg/mol〕。",
                 "分子どうしの衝突や分子の大きさを無視し、壁との衝突は弾性衝突とみなす。",
                 "分子1個あたりの平均運動エネルギーは絶対温度に比例し、気体の種類によらない。",
                 "単原子分子理想気体の内部エネルギーは、分子の運動エネルギーの総和 $U=\\dfrac32nRT$。"],
                body="絶対温度とは、分子の熱運動の激しさ（平均運動エネルギー）を表す量である。同じ温度なら、軽い分子ほど速く運動している。",
                proof=["1辺 $L$ の立方体容器の中で、速度の $x$ 成分 $v_x$ の分子が壁 S に弾性衝突すると、運動量は $mv_x$ から $-mv_x$ に変わる。壁が受ける力積は $2mv_x$。",
                       "この分子は時間 $\\dfrac{2L}{v_x}$ ごとに壁 S に当たるので、時間 $t$ の間に壁が受ける力積は $2mv_x\\times\\dfrac{v_xt}{2L}=\\dfrac{mv_x{}^2}{L}t$。平均の力は $\\dfrac{mv_x{}^2}{L}$。",
                       "$N$ 個の分子について和をとると $F=\\dfrac{Nm\\overline{v_x{}^2}}{L}$。方向にかたよりがないので $\\overline{v_x{}^2}=\\dfrac13\\overline{v^2}$。",
                       "$p=\\dfrac{F}{L^2}=\\dfrac{Nm\\overline{v^2}}{3L^3}=\\dfrac{Nm\\overline{v^2}}{3V}$。これと $pV=Nk_{\\mathrm{B}}T$ を比べて $\\dfrac12m\\overline{v^2}=\\dfrac32k_{\\mathrm{B}}T$。"],
                figure=figure("1辺 L の立方体容器の中を飛び回る分子。速度の x 成分 v_x の分子が壁 S に衝突する", box_svg(), caption="壁が受ける力積の総和が圧力になる"),
                points=[tp("導出の各段階で「どの物理法則を使ったか」（運動量と力積、平均、等方性）を確認しながら進める。", timing="導出の直後",
                           ask="気体の温度を4倍にすると、分子の二乗平均速度は何倍になるか。", expect="$\\sqrt4=2$ 倍。")]),
        theorem("th2", "熱力学第一法則",
                "$$\\Delta U=Q+W\\qquad(W'=-W:\\ \\text{気体が外部にした仕事})$$",
                ["$Q$：気体が吸収した熱量（放出なら負）。$W$：気体が外部からされた仕事（膨張すると負）。",
                 "定圧変化で気体が外部にする仕事は $W'=p\\Delta V$。一般には $p$−$V$ グラフと $V$ 軸で囲まれた面積に等しい。",
                 "単原子分子理想気体の内部エネルギーの変化は、どの変化でも $\\Delta U=\\dfrac32nR\\Delta T$（温度だけで決まる）。",
                 "等温変化：$\\Delta U=0$ で $Q=W'$。断熱変化：$Q=0$ で $\\Delta U=W$（断熱圧縮で温度上昇、断熱膨張で温度低下）。"],
                body="第一法則はエネルギー保存則を、熱を含めて表したものである。気体を「エネルギーの財布」と考え、入ってくる熱と仕事の和が財布の中身（内部エネルギー）の増加になる、と読む。",
                points=[tp("符号の約束（$W$ はされた仕事）を、教科書・問題集によって $W'$（した仕事）で書く場合があることを示し、どちらで書いても「気体に入るエネルギー」を正として考えればよいとまとめる。",
                           caution="$\\Delta U=Q+W'$ と、した仕事を足してしまう誤りが多い。")]),
        derivation("dv1", "モル比熱とマイヤーの関係",
                   ["定積変化（$\\Delta V=0$）では仕事は 0 なので $Q=\\Delta U=\\dfrac32nR\\Delta T$。よって定積モル比熱 $C_V=\\dfrac{Q}{n\\Delta T}=\\dfrac32R$。",
                    "定圧変化では、気体がする仕事 $W'=p\\Delta V=nR\\Delta T$（状態方程式より）。",
                    "第一法則 $Q=\\Delta U+W'=\\dfrac32nR\\Delta T+nR\\Delta T=\\dfrac52nR\\Delta T$。よって定圧モル比熱 $C_p=\\dfrac52R$。",
                    "どの理想気体でも $C_p=C_V+R$（マイヤーの関係）。定圧では膨張して仕事をする分だけ、余分に熱が必要になる。"],
                   body="単原子分子理想気体では $C_V=\\dfrac32R\\fallingdotseq12.5\\,\\mathrm{J/(mol\\cdot K)}$、$C_p=\\dfrac52R\\fallingdotseq20.8\\,\\mathrm{J/(mol\\cdot K)}$。",
                   figure=figure("鉛直なシリンダーに閉じこめた気体。なめらかに動くピストンの上は大気圧 p₀。下から加熱すると定圧で膨張する", cylinder_svg(),
                                 caption="定圧変化：加えた熱の一部が仕事になる"),
                   points=[tp("同じ温度上昇でも定圧のほうが多くの熱を必要とする理由を、ピストンを押し上げる仕事に注目して説明させる。",
                              ask="定積と定圧で、気体を 1 K 上げるのに必要な熱量はどちらが大きいか。なぜか。",
                              expect="定圧。膨張して外部に仕事をする分だけ余分に熱が必要。")]),
        definition("df2", "熱機関と熱効率",
                   "熱を受け取って仕事をし、もとの状態に戻ることをくり返す装置を熱機関という。1サイクルの間に高温の物体から熱 $Q_{\\text{in}}$ を吸収し、外部に正味の仕事 $W'$ をし、低温の物体に熱 $Q_{\\text{out}}$ を放出するとき、熱効率は次の式で表される。",
                   formula="$$e=\\dfrac{W'}{Q_{\\text{in}}}=\\dfrac{Q_{\\text{in}}-Q_{\\text{out}}}{Q_{\\text{in}}}\\qquad(e<1)$$",
                   conditions=["1サイクルではもとの状態に戻るので $\\Delta U=0$、$W'=Q_{\\text{in}}-Q_{\\text{out}}$。",
                               "正味の仕事は、$p$−$V$ グラフでサイクルが囲む面積に等しい（時計回りなら外部に正の仕事）。",
                               "$Q_{\\text{in}}$ は、サイクルのうち熱を吸収する過程の熱量の和。放出する過程の熱は含めない。",
                               "熱力学第二法則：熱を100%仕事に変える熱機関はつくれない。熱は自然には低温から高温へ移らない（不可逆変化）。"],
                   figure=figure("p−V グラフ上の長方形のサイクル A→B→C→D→A。囲まれた面積が1サイクルの正味の仕事", pv_svg([(1, 1), (1, 3), (5, 3), (5, 1)], closed=True),
                                 caption="サイクルが囲む面積＝正味の仕事"),
                   points=[tp("$Q_{\\text{in}}$ に放熱過程を含めてしまう誤りを防ぐため、各過程の $Q$ の符号を表にまとめさせる。")]),
        example("ex1", "例題1　状態方程式",
                "容積 $8.31\\,\\mathrm{L}$ の容器に、温度 $27\\,{}^\\circ\\mathrm{C}$、圧力 $3.0\\times10^5\\,\\mathrm{Pa}$ の気体が入っている。気体の物質量を求めよ。また、容器を密閉したまま温度を $127\\,{}^\\circ\\mathrm{C}$ にすると、圧力はいくらになるか。" + RS,
                ["$T=27+273=300\\,\\mathrm{K}$、$V=8.31\\times10^{-3}\\,\\mathrm{m^3}$。",
                 "$n=\\dfrac{pV}{RT}=\\dfrac{3.0\\times10^5\\times8.31\\times10^{-3}}{8.31\\times300}=1.0\\,\\mathrm{mol}$。",
                 "体積一定なので $\\dfrac{p}{T}=$ 一定。$p'=3.0\\times10^5\\times\\dfrac{400}{300}=4.0\\times10^5\\,\\mathrm{Pa}$。"],
                "物質量 $1.0\\,\\mathrm{mol}$、圧力 $4.0\\times10^5\\,\\mathrm{Pa}$",
                thinking="単位を SI（Pa、m³、K）にそろえてから代入する。物質量一定ならボイル・シャルルの法則で比をとる。",
                misconceptions=[("温度が $27\\,{}^\\circ\\mathrm{C}$ から $127\\,{}^\\circ\\mathrm{C}$ になったので、圧力は約4.7倍になる", "比は絶対温度でとる。$\\dfrac{400}{300}$ 倍")]),
        example("ex2", "例題2　二乗平均速度",
                "温度 $300\\,\\mathrm{K}$ のヘリウム（モル質量 $4.0\\times10^{-3}\\,\\mathrm{kg/mol}$）と酸素（モル質量 $3.2\\times10^{-2}\\,\\mathrm{kg/mol}$）について、分子の二乗平均速度 $\\sqrt{\\overline{v^2}}$ をそれぞれ求めよ。" + RS,
                ["$\\dfrac12m\\overline{v^2}=\\dfrac32k_{\\mathrm{B}}T$ の両辺にアボガドロ定数をかけると $\\dfrac12M\\overline{v^2}=\\dfrac32RT$、$\\sqrt{\\overline{v^2}}=\\sqrt{\\dfrac{3RT}{M}}$。",
                 "ヘリウム：$\\sqrt{\\dfrac{3\\times8.31\\times300}{4.0\\times10^{-3}}}\\fallingdotseq1.4\\times10^3\\,\\mathrm{m/s}$。",
                 "酸素：$\\sqrt{\\dfrac{3\\times8.31\\times300}{3.2\\times10^{-2}}}\\fallingdotseq4.8\\times10^2\\,\\mathrm{m/s}$（ヘリウムの $\\dfrac{1}{\\sqrt8}$ 倍）。"],
                "ヘリウム 約 $1.4\\times10^3\\,\\mathrm{m/s}$、酸素 約 $4.8\\times10^2\\,\\mathrm{m/s}$",
                thinking="同じ温度では平均運動エネルギーが等しい。質量が8倍なら速さは $\\dfrac{1}{\\sqrt8}$ 倍。",
                misconceptions=[("モル質量を g/mol のまま代入する", "SI 単位では kg/mol。$4.0\\,\\mathrm{g/mol}=4.0\\times10^{-3}\\,\\mathrm{kg/mol}$")]),
        example("ex3", "例題3　サイクルの熱効率",
                "$1.0\\,\\mathrm{mol}$ の単原子分子理想気体を、図の長方形のサイクル A→B→C→D→A で変化させる。A は圧力 $1.0\\times10^5\\,\\mathrm{Pa}$、体積 $1.0\\times10^{-3}\\,\\mathrm{m^3}$、B は圧力 $3.0\\times10^5\\,\\mathrm{Pa}$（体積は A と同じ）、C は体積 $5.0\\times10^{-3}\\,\\mathrm{m^3}$（圧力は B と同じ）である。このサイクルの熱効率を求めよ。",
                ["正味の仕事＝長方形の面積 $=(3.0-1.0)\\times10^5\\times(5.0-1.0)\\times10^{-3}=800\\,\\mathrm{J}$。",
                 "A→B（定積・温度上昇）：$Q_{\\mathrm{AB}}=\\dfrac32V\\Delta p=\\dfrac32\\times1.0\\times10^{-3}\\times2.0\\times10^5=300\\,\\mathrm{J}$（吸収）。",
                 "B→C（定圧膨張）：$Q_{\\mathrm{BC}}=\\dfrac52p\\Delta V=\\dfrac52\\times3.0\\times10^5\\times4.0\\times10^{-3}=3000\\,\\mathrm{J}$（吸収）。C→D・D→A は放熱。",
                 "$e=\\dfrac{800}{300+3000}\\fallingdotseq0.24$。"],
                "約 $0.24$（24 %）",
                thinking="$nR\\Delta T=\\Delta(pV)$ を使うと、温度を求めなくても熱量が計算できる。吸収する過程だけを $Q_{\\text{in}}$ に入れる。",
                figure=figure("p−V グラフ上の長方形のサイクル A(1,1)→B(1,3)→C(5,3)→D(5,1)。目盛りは p が 10⁵ Pa、V が 10⁻³ m³", pv_svg([(1, 1), (1, 3), (5, 3), (5, 1)], closed=True)),
                points=[tp("各過程の $Q$、$W'$、$\\Delta U$ を表にまとめ、1サイクルで $\\Delta U$ の和が 0、$Q$ の和が $W'$ の和に等しいことを確かめさせる。")]),
        board("bd1", "板書案",
              [("① 気体の法則", ["$T=t+273$（必ず K）", "ボイル：$pV=$ 一定", "シャルル：$\\dfrac{V}{T}=$ 一定", "$pV=nRT$、$R=8.31$", "$pV=Nk_{\\mathrm{B}}T$"]),
               ("② 分子運動論", ["力積 $2mv_x$、間隔 $\\dfrac{2L}{v_x}$", "$p=\\dfrac{Nm\\overline{v^2}}{3V}$", "$\\dfrac12m\\overline{v^2}=\\dfrac32k_{\\mathrm{B}}T$",
                                  "$\\sqrt{\\overline{v^2}}=\\sqrt{\\dfrac{3RT}{M}}$（$M$ は kg/mol）", "$U=\\dfrac32nRT$（単原子）"]),
               ("③ 第一法則", ["$\\Delta U=Q+W$（$W$：された仕事）", "$W'=p\\Delta V$＝グラフの面積", "定積 $C_V=\\dfrac32R$、定圧 $C_p=\\dfrac52R$",
                               "等温 $\\Delta U=0$、断熱 $Q=0$", "$e=\\dfrac{W'}{Q_{\\text{in}}}$"])]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("状態変化の問題では、まず状態ごとに $(p,\\ V,\\ T)$ の表をつくらせ、次に過程ごとに $(Q,\\ W',\\ \\Delta U)$ の表をつくらせる。2つの表で整理すると見通しがよい。", timing="例題3の前"),
               tp("$\\Delta U=\\dfrac32nR\\Delta T$ は定積変化だけの式ではなく、どの変化でも使えることを強調する（内部エネルギーは温度だけで決まる）。",
                  ask="定圧変化で温度が $10\\,\\mathrm{K}$ 上がったとき、$\\Delta U$ は定積で $10\\,\\mathrm{K}$ 上がったときと比べてどうか。", expect="同じ。違うのは $Q$ と $W'$。"),
               tp("断熱圧縮で温度が上がる理由を、分子の立場（動いてくるピストンにはね返されると分子の速さが増す）でも説明させる。"),
               tp("熱効率の計算では、放熱過程の熱を $Q_{\\text{in}}$ に含めないよう、各過程の $Q$ の符号を確認させる。", caution="$Q$ の総和（＝正味の仕事）を分母にする誤りもある。")],
              misconceptions=[("温度が2倍になると体積も2倍になる（℃ のまま）", "比例するのは絶対温度。$10\\,{}^\\circ\\mathrm{C}\\to20\\,{}^\\circ\\mathrm{C}$ では $\\dfrac{293}{283}$ 倍にすぎない"),
                              ("等温変化では熱の出入りがない", "等温変化では $\\Delta U=0$ なので、した仕事と同じだけ熱を吸収している。熱の出入りがないのは断熱変化"),
                              ("同じ温度なら、重い分子ほど運動エネルギーが大きい", "平均運動エネルギーは温度だけで決まり、分子の種類によらない。重い分子は遅く動く")]),
        summary("sm1", "まとめ", ["気体の圧力・体積・絶対温度・物質量は $pV=nRT$ で結ばれる。温度は必ず K で扱う。",
                                   "圧力は分子が壁に与える力積の総和であり、絶対温度は分子1個の平均運動エネルギー $\\dfrac32k_{\\mathrm{B}}T$ に比例する。",
                                   "熱力学第一法則 $\\Delta U=Q+W$ を、定積・定圧・等温・断熱の各変化に当てはめる。単原子分子では $\\Delta U=\\dfrac32nR\\Delta T$。",
                                   "熱機関の熱効率は $e=\\dfrac{W'}{Q_{\\text{in}}}$ で、$p$−$V$ グラフでサイクルが囲む面積が正味の仕事。"]),
        check("ck1", "確認問題", [("$27\\,{}^\\circ\\mathrm{C}$ は何 K か。", "$300\\,\\mathrm{K}$"),
                                  ("温度一定で気体の体積を $\\dfrac12$ にすると、圧力は何倍になるか。", "2倍"),
                                  ("絶対温度を4倍にすると、分子の二乗平均速度は何倍になるか。", "2倍"),
                                  ("断熱変化で、気体が外部から $200\\,\\mathrm{J}$ の仕事をされた。内部エネルギーの変化は？", "$+200\\,\\mathrm{J}$（温度は上がる）"),
                                  ("$1.0\\,\\mathrm{mol}$ の単原子分子理想気体の温度を、定積で $10\\,\\mathrm{K}$ 上げるのに必要な熱量は？（$R=8.31$）", "$\\dfrac32\\times8.31\\times10\\fallingdotseq1.2\\times10^2\\,\\mathrm{J}$")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

TEMPS = [(27, 300), (127, 400), (77, 350), (-73, 200), (327, 600), (227, 500), (-23, 250), (177, 450)]


def ctx(c):
    return f"{c}\\,{{}}^\\circ\\mathrm{{C}}" if c >= 0 else f"-{-c}\\,{{}}^\\circ\\mathrm{{C}}"


@gen("basic_check", 4, ["computation"])
def gas_law_basic(r):
    kind = r.choice(["boyle", "charles", "combined", "isochoric"])
    if kind == "boyle":
        p1, V1, V2 = r.choice([("1.0", "6.0", "2.0"), ("2.0", "3.0", "4.0"), ("1.5", "4.0", "3.0"), ("3.0", "2.0", "6.0"), ("1.0", "5.0", "2.0"), ("2.4", "1.0", "3.0")])
        p2 = Q(p1) * Q(V1) / Q(V2)
        return numq(f"温度を一定に保ったまま、圧力 ${p1}\\times10^5\\,\\mathrm{{Pa}}$、体積 {V1} L の気体の体積を {V2} L に変えた。変化後の圧力は何 Pa か。",
                    p2 * 10 ** 5, f"{P(Q(p1))}*10**5*{P(Q(V1))}/{P(Q(V2))}", "ボイルの法則 $p_1V_1=p_2V_2$。", "Pa", d=1,
                    ap="温度一定ならボイルの法則。体積の比だけが必要なので、L のままでよい。",
                    steps=[f"$p_2=p_1\\times\\dfrac{{V_1}}{{V_2}}={p1}\\times10^5\\times\\dfrac{{{V1}}}{{{V2}}}$。", f"$p_2={t(p2 * 10 ** 5)}\\,\\mathrm{{Pa}}$。"],
                    alt=["体積が小さくなれば圧力は大きくなる（反比例）ことから、答えの大小を先に予想して確かめる。"],
                    pc=[("ボイルの法則を用いている", 1), ("値が正しい", 1)], pit=["体積の比を逆にかける。"])
    (c1, T1), (c2, T2) = r.sample(TEMPS, 2)
    if kind == "charles":
        V1 = r.choice(["2.0", "3.0", "6.0", "1.5", "12"])
        V2 = Q(V1) * sp.Rational(T2, T1)
        return numq(f"圧力を一定に保ったまま、温度 ${ctx(c1)}$、体積 {V1} L の気体の温度を ${ctx(c2)}$ に変えた。変化後の体積は何 L か。",
                    V2, f"{P(Q(V1))}*({c2}+273)/({c1}+273)", "シャルルの法則 $\\dfrac{V_1}{T_1}=\\dfrac{V_2}{T_2}$（絶対温度）。", "L", d=2,
                    ap="圧力一定なら体積は絶対温度に比例する。℃ を K に直してから比をとる。",
                    steps=[f"$T_1={c1}+273={T1}\\,\\mathrm{{K}}$、$T_2={c2}+273={T2}\\,\\mathrm{{K}}$。", f"$V_2={V1}\\times\\dfrac{{{T2}}}{{{T1}}}={t(V2)}\\,\\mathrm{{L}}$。"],
                    alt=["温度が上がれば体積は増え、下がれば減ることで、答えの大小を確かめる。"],
                    pc=[("絶対温度に直している", 1), ("値が正しい", 1)], pit=["セルシウス温度のまま比をとる。"])
    if kind == "isochoric":
        p1 = r.choice(["1.0", "1.5", "2.0", "3.0"])
        p2 = Q(p1) * sp.Rational(T2, T1)
        return numq(f"密閉した容器に入った気体の温度を ${ctx(c1)}$ から ${ctx(c2)}$ に変えた。はじめの圧力が ${p1}\\times10^5\\,\\mathrm{{Pa}}$ のとき、変化後の圧力は何 Pa か。容器の体積は変わらないものとする。",
                    p2 * 10 ** 5, f"{P(Q(p1))}*10**5*({c2}+273)/({c1}+273)", "体積一定なら $\\dfrac{p}{T}=$ 一定。", "Pa", d=2,
                    ap="体積と物質量が一定なら、圧力は絶対温度に比例する。",
                    steps=[f"$T_1={T1}\\,\\mathrm{{K}}$、$T_2={T2}\\,\\mathrm{{K}}$。", f"$p_2={p1}\\times10^5\\times\\dfrac{{{T2}}}{{{T1}}}={t(p2 * 10 ** 5)}\\,\\mathrm{{Pa}}$。"],
                    alt=["状態方程式 $pV=nRT$ で $n,\\ V$ が一定なら $p\\propto T$、と導いて確かめる。"],
                    pc=[("$p\\propto T$（絶対温度）を用いている", 1), ("値が正しい", 1)], pit=["セルシウス温度の比をかける。"])
    p1, V1, p2 = r.choice([("1.0", "4.0", "2.0"), ("2.0", "6.0", "1.0"), ("1.5", "2.0", "3.0"), ("3.0", "1.0", "1.5"), ("1.0", "9.0", "3.0")])
    V2 = Q(p1) * Q(V1) * T2 / (Q(p2) * T1)
    return numq(f"圧力 ${p1}\\times10^5\\,\\mathrm{{Pa}}$、温度 ${ctx(c1)}$ で体積 {V1} L の気体を、圧力 ${p2}\\times10^5\\,\\mathrm{{Pa}}$、温度 ${ctx(c2)}$ の状態にした。このときの体積は何 L か。",
                V2, f"{P(Q(p1))}*{P(Q(V1))}*({c2}+273)/({P(Q(p2))}*({c1}+273))", "ボイル・シャルルの法則 $\\dfrac{p_1V_1}{T_1}=\\dfrac{p_2V_2}{T_2}$。", "L", d=2,
                ap="物質量が一定なら $\\dfrac{pV}{T}$ は一定。圧力の比と絶対温度の比を両方かける。",
                steps=[f"$T_1={T1}\\,\\mathrm{{K}}$、$T_2={T2}\\,\\mathrm{{K}}$。", f"$V_2={V1}\\times\\dfrac{{{p1}}}{{{p2}}}\\times\\dfrac{{{T2}}}{{{T1}}}={t(V2)}\\,\\mathrm{{L}}$。"],
                alt=["まず温度一定で圧力だけ変え（ボイル）、次に圧力一定で温度だけ変える（シャルル）と2段階で計算しても同じ。"],
                pc=[("ボイル・シャルルの法則を用いている", 1), ("値が正しい", 1)], pit=["圧力の比を逆にする。", "℃ のまま計算する。"])


GASES = [("ヘリウム", "4.0\\times10^{-3}", sp.Rational(4, 1000)), ("水素", "2.0\\times10^{-3}", sp.Rational(2, 1000)),
         ("窒素", "2.8\\times10^{-2}", sp.Rational(28, 1000)), ("酸素", "3.2\\times10^{-2}", sp.Rational(32, 1000)), ("アルゴン", "4.0\\times10^{-2}", sp.Rational(40, 1000))]


@gen("basic_check", 3, ["computation", "concept"])
def kinetic_basic(r):
    kind = r.choice(["ke", "rms", "ratio_T", "ratio_gas"])
    if kind == "ke":
        T = r.choice([200, 250, 300, 400, 500, 600])
        K = sp.Rational(3, 2) * KB * T
        return numq(f"絶対温度 {T} K の理想気体の分子1個あたりの平均運動エネルギーは何 J か。ボルツマン定数を $1.38\\times10^{{-23}}\\,\\mathrm{{J/K}}$ とする。",
                    K, f"Rational(3,2)*Rational(138,100)*10**(-23)*{T}", "$\\dfrac12m\\overline{v^2}=\\dfrac32k_{\\mathrm{B}}T$。", "J", n=2, d=2,
                    ap="平均運動エネルギーは絶対温度だけで決まり、気体の種類によらない。",
                    steps=[f"$\\dfrac32k_{{\\mathrm{{B}}}}T=\\dfrac32\\times1.38\\times10^{{-23}}\\times{T}$。", f"$\\fallingdotseq{t(K, 2)}\\,\\mathrm{{J}}$。"],
                    alt=["1 mol あたりの運動エネルギー $\\dfrac32RT$ をアボガドロ定数で割っても同じ値になる。"],
                    pc=[("$\\dfrac32k_{\\mathrm{B}}T$ を用いている", 1), ("値が正しい", 1)], pit=["$\\dfrac32$ をかけ忘れる。"])
    if kind == "rms":
        name, Mtx, M = r.choice(GASES)
        T = r.choice([200, 300, 400, 600])
        v = sp.sqrt(3 * R * T / M)
        return numq(f"絶対温度 {T} K の{name}分子の二乗平均速度 $\\sqrt{{\\overline{{v^2}}}}$ は何 m/s か。{name}のモル質量を ${Mtx}\\,\\mathrm{{kg/mol}}$、" + RS,
                    v, f"sqrt(3*Rational(831,100)*{T}/{P(M)})", "$\\sqrt{\\overline{v^2}}=\\sqrt{\\dfrac{3RT}{M}}$。", "m/s", n=2, d=2,
                    ap="$\\dfrac12M\\overline{v^2}=\\dfrac32RT$（1 mol あたり）から求める。モル質量は kg/mol。",
                    steps=[f"$\\overline{{v^2}}=\\dfrac{{3\\times8.31\\times{T}}}{{{Mtx}}}$。", f"$\\sqrt{{\\overline{{v^2}}}}\\fallingdotseq{t(v, 2)}\\,\\mathrm{{m/s}}$。"],
                    alt=["分子1個の質量 $m=\\dfrac{M}{N_{\\mathrm{A}}}$ と $\\dfrac32k_{\\mathrm{B}}T$ を使って計算しても同じ。"],
                    pc=[("二乗平均速度の式を用いている", 1), ("値が正しい", 1)], pit=["モル質量を g/mol のまま代入する。"])
    if kind == "ratio_T":
        k, lab = r.choice([(4, "4倍"), (9, "9倍"), (sp.Rational(1, 4), "$\\dfrac14$ 倍"), (2, "2倍"), (16, "16倍")])
        ratio = sp.sqrt(k)
        return numq(f"理想気体の絶対温度を{lab}にすると、分子の二乗平均速度は何倍になるか。", ratio, f"sqrt({P(k)})", "$\\sqrt{\\overline{v^2}}\\propto\\sqrt{T}$。", "倍", d=1,
                    ap="平均運動エネルギー（速さの2乗）が絶対温度に比例する。速さは温度の平方根に比例。",
                    steps=["$\\dfrac12m\\overline{v^2}\\propto T$ より $\\sqrt{\\overline{v^2}}\\propto\\sqrt{T}$。", f"$\\sqrt{{{k}}}={t(ratio)}$ 倍。" if k != sp.Rational(1, 4) else "$\\sqrt{\\dfrac14}=0.50$ 倍。"],
                    alt=["$\\sqrt{\\dfrac{3RT}{M}}$ に $T$ と変化後の温度を代入して比をとっても同じ。"],
                    pc=[("速さが $\\sqrt{T}$ に比例することを用いている", 1), ("値が正しい", 1)], pit=["速さが温度に比例するとする。"])
    (n1, _, M1), (n2, _, M2) = r.sample(GASES, 2)
    ratio = sp.sqrt(M2 / M1)
    return numq(f"同じ温度の{n1}と{n2}について、{n1}分子の二乗平均速度は{n2}分子の何倍か。モル質量は、ヘリウム 4.0 g/mol、水素 2.0 g/mol、窒素 28 g/mol、酸素 32 g/mol、アルゴン 40 g/mol とする。",
                ratio, f"sqrt({P(M2)}/{P(M1)})", "同じ温度なら平均運動エネルギーが等しいので $\\sqrt{\\overline{v^2}}\\propto\\dfrac{1}{\\sqrt{M}}$。", "倍", d=2,
                ap="同じ温度 → 平均運動エネルギーが等しい → 軽い分子ほど速い。",
                steps=[f"$\\dfrac{{v_1}}{{v_2}}=\\sqrt{{\\dfrac{{M_2}}{{M_1}}}}=\\sqrt{{\\dfrac{{{dec(M2 * 1000)}}}{{{dec(M1 * 1000)}}}}}$。", f"$\\fallingdotseq{t(ratio)}$ 倍。"],
                alt=["それぞれの二乗平均速度を $\\sqrt{\\dfrac{3RT}{M}}$ で計算して比をとっても同じ（$T$ と $R$ は約分される）。"],
                pc=[("平均運動エネルギーが等しいことを用いている", 1), ("値が正しい", 1)], pit=["モル質量の比をそのまま答える（平方根をとり忘れる）。", "比を逆にする。"])


@gen("basic_check", 3, ["computation"])
def internal_basic(r):
    kind = r.choice(["U", "dU", "work"])
    if kind == "work":
        ps = r.choice(["1.0", "2.0", "1.5", "3.0"])
        V1, V2 = r.choice([("2.0", "5.0"), ("1.0", "3.0"), ("4.0", "6.0"), ("3.0", "8.0"), ("2.5", "4.5")])
        W = Q(ps) * 10 ** 5 * (Q(V2) - Q(V1)) / 1000
        return numq(f"圧力 ${ps}\\times10^5\\,\\mathrm{{Pa}}$ を一定に保ったまま、気体の体積が {V1} L から {V2} L に増加した。この間に気体が外部にした仕事は何 J か。",
                    W, f"{P(Q(ps))}*10**5*({P(Q(V2))}-{P(Q(V1))})*10**(-3)", "$W'=p\\Delta V$。", "J", d=2,
                    ap="定圧変化で気体がする仕事は圧力×体積変化。L を m³ に直す。",
                    steps=[f"$\\Delta V=({V2}-{V1})\\times10^{{-3}}\\,\\mathrm{{m^3}}$。", f"$W'=p\\Delta V={ps}\\times10^5\\times{dec(Q(V2) - Q(V1))}\\times10^{{-3}}={t(W)}\\,\\mathrm{{J}}$。"],
                    alt=["$p$−$V$ グラフで、水平な線分と $V$ 軸の間の長方形の面積として求めても同じ。"],
                    pc=[("$W'=p\\Delta V$ を用いている", 1), ("値が正しい", 1)], pit=["L を m³ に直し忘れて 1000 倍の値にする。"])
    n = r.choice(["0.50", "1.0", "2.0", "3.0", "0.20"])
    if kind == "U":
        T = r.choice([200, 300, 400, 500])
        U = sp.Rational(3, 2) * Q(n) * R * T
        return numq(f"{n} mol の{MONO}が絶対温度 {T} K にある。この気体の内部エネルギーは何 J か。" + RS,
                    U, f"Rational(3,2)*{P(Q(n))}*Rational(831,100)*{T}", "$U=\\dfrac32nRT$。", "J", n=2, d=1,
                    ap="単原子分子理想気体の内部エネルギーは、分子の運動エネルギーの総和 $\\dfrac32nRT$。",
                    steps=[f"$U=\\dfrac32\\times{n}\\times8.31\\times{T}$。", f"$U\\fallingdotseq{t(U, 2)}\\,\\mathrm{{J}}$。"],
                    alt=["分子1個の平均運動エネルギー $\\dfrac32k_{\\mathrm{B}}T$ に分子数 $nN_{\\mathrm{A}}$ をかけても同じ。"],
                    pc=[("$U=\\dfrac32nRT$ を用いている", 1), ("値が正しい", 1)], pit=["$\\dfrac52$ をかける。"])
    dT = r.choice([10, 20, 40, 50, 100])
    dU = sp.Rational(3, 2) * Q(n) * R * dT
    return numq(f"{n} mol の{MONO}の温度が {dT} K 上昇した。内部エネルギーの増加量は何 J か。" + RS,
                dU, f"Rational(3,2)*{P(Q(n))}*Rational(831,100)*{dT}", "$\\Delta U=\\dfrac32nR\\Delta T$（どの変化でも成り立つ）。", "J", n=2, d=1,
                ap="内部エネルギーは温度だけで決まる。どのような過程で温度が上がったかは関係ない。",
                steps=[f"$\\Delta U=\\dfrac32\\times{n}\\times8.31\\times{dT}$。", f"$\\Delta U\\fallingdotseq{t(dU, 2)}\\,\\mathrm{{J}}$。"],
                alt=["定積モル比熱 $C_V=\\dfrac32R$ を使い、$nC_V\\Delta T$ として求めても同じ。"],
                pc=[("$\\Delta U=\\dfrac32nR\\Delta T$ を用いている", 1), ("値が正しい", 1)], pit=["過程が書かれていないので求められないと考える。"])


@gen("basic_check", 4, ["computation", "condition_check"])
def first_law_basic(r):
    kind = r.choice(["gain", "lose", "adia_c", "adia_e", "isoT"])
    if kind == "gain":
        Qv, Wd = r.choice([(700, 300), (900, 360), (1500, 600), (450, 180), (2000, 800), (350, 500)])
        return numq(f"シリンダー内の理想気体が {Qv} J の熱を吸収し、同時にピストンを押して外部に {Wd} J の仕事をした。気体の内部エネルギーは何 J 増加したか（減少した場合は負の値で答えなさい）。",
                    sp.Integer(Qv - Wd), f"{Qv}-{Wd}", "$\\Delta U=Q+W$、$W=-W'$。", "J", d=2,
                    ap="気体に入るエネルギーを正とする。吸収した熱は正、外部にした仕事は気体から出ていくので負。",
                    steps=[f"$Q=+{Qv}\\,\\mathrm{{J}}$、$W=-{Wd}\\,\\mathrm{{J}}$。", f"$\\Delta U={Qv}-{Wd}={Qv - Wd}\\,\\mathrm{{J}}$。"],
                    alt=["$Q=\\Delta U+W'$（吸収した熱は内部エネルギーの増加と外部への仕事に分かれる）と読んで計算してもよい。"],
                    pc=[("仕事の符号を正しく扱っている", 1), ("値が正しい", 1)], pit=["した仕事を足して $" + str(Qv + Wd) + "\\,\\mathrm{J}$ とする。"])
    if kind == "lose":
        Wv, Qo = r.choice([(600, 250), (450, 450), (300, 500), (800, 200), (1000, 350)])
        return numq(f"ピストンを押してシリンダー内の理想気体を圧縮し、気体に {Wv} J の仕事をした。この間に気体は周囲へ {Qo} J の熱を放出した。気体の内部エネルギーは何 J 増加したか（減少した場合は負の値で答えなさい）。",
                    sp.Integer(Wv - Qo), f"{Wv}-{Qo}", "$\\Delta U=Q+W$ で $Q<0$、$W>0$。", "J", d=2,
                    ap="気体の立場で「された仕事」は正、「放出した熱」は負。",
                    steps=[f"$Q=-{Qo}\\,\\mathrm{{J}}$、$W=+{Wv}\\,\\mathrm{{J}}$。", f"$\\Delta U=-{Qo}+{Wv}={Wv - Qo}\\,\\mathrm{{J}}$。"],
                    alt=["$\\Delta U$ が正なら温度が上がり、負なら下がる、と温度変化の向きで答えの符号を確かめる。"],
                    pc=[("熱と仕事の符号を正しく扱っている", 1), ("値が正しい", 1)], pit=["放出した熱を正のまま足す。"])
    if kind in ("adia_c", "adia_e"):
        Wv = r.choice([120, 250, 300, 480, 600])
        comp = kind == "adia_c"
        dU = Wv if comp else -Wv
        return numq(f"理想気体を断熱{'圧縮' if comp else '膨張'}させたところ、気体は{'外部から ' + str(Wv) + ' J の仕事をされた' if comp else '外部に ' + str(Wv) + ' J の仕事をした'}。気体の内部エネルギーの変化は何 J か。増加を正、減少を負で答えなさい。",
                    sp.Integer(dU), f"0+({dU})", "断熱変化では $Q=0$ なので $\\Delta U=W$。", "J", d=2,
                    ap="断熱＝熱の出入りがない（$Q=0$）。内部エネルギーの変化は仕事だけで決まる。",
                    steps=["$Q=0$。", f"$\\Delta U=W={'+' if comp else ''}{dU}\\,\\mathrm{{J}}$（温度は{'上がる' if comp else '下がる'}）。"],
                    alt=["自転車の空気入れが熱くなる（断熱圧縮）、スプレー缶を使うと冷える（断熱膨張に近い）という経験と、符号を照らし合わせる。"],
                    pc=[("$Q=0$ としている", 1), ("符号を含めて値が正しい", 1)], pit=["断熱なので $\\Delta U=0$ とする（等温と混同）。"])
    Wd = r.choice([150, 240, 400, 520, 830])
    return numq(f"理想気体を、温度を一定に保ったままゆっくり膨張させたところ、気体は外部に {Wd} J の仕事をした。この間に気体が吸収した熱量は何 J か。",
                sp.Integer(Wd), f"{Wd}", "等温変化では $\\Delta U=0$ なので $Q=W'$。", "J", d=2,
                ap="理想気体の内部エネルギーは温度だけで決まる。温度一定なら $\\Delta U=0$。",
                steps=["等温なので $\\Delta U=0$。", f"$0=Q+(-{Wd})$ より $Q={Wd}\\,\\mathrm{{J}}$。"],
                alt=["吸収した熱がすべて外部への仕事に使われ、内部にエネルギーがたまらないので温度が変わらない、と解釈して確かめる。"],
                pc=[("等温で $\\Delta U=0$ としている", 1), ("値が正しい", 1)], pit=["等温なので熱の出入りがない（$Q=0$）とする。"])


@gen("basic_check", 3, ["computation"])
def efficiency_basic(r):
    kind = r.choice(["e", "qout", "qin", "e2"])
    Qin, W = r.choice([(1000, 300), (2000, 500), (1600, 400), (5000, 1200), (2500, 1000), (3000, 600), (4000, 1000)])
    if kind == "e":
        e = sp.Rational(W, Qin)
        return numq(f"ある熱機関は、1サイクルごとに高温の熱源から {Qin} J の熱を受け取り、正味 {W} J の仕事をする。熱効率を小数で答えなさい。",
                    e, f"Rational({W},{Qin})", "$e=\\dfrac{W'}{Q_{\\text{in}}}$。", "", d=1,
                    ap="熱効率＝（正味の仕事）÷（吸収した熱）。",
                    steps=[f"$e=\\dfrac{{{W}}}{{{Qin}}}$。", f"$e={t(e)}$。"],
                    alt=["放出する熱 $Q_{\\text{in}}-W'$ を求めて $1-\\dfrac{Q_{\\text{out}}}{Q_{\\text{in}}}$ で計算しても同じ。"],
                    pc=[("熱効率の定義を用いている", 1), ("値が正しい", 1)], pit=["$\\dfrac{Q_{\\text{in}}}{W'}$ と逆にする。"])
    if kind == "e2":
        Qo = Qin - W
        e = sp.Rational(W, Qin)
        return numq(f"ある熱機関は、1サイクルごとに高温の熱源から {Qin} J の熱を受け取り、低温の熱源へ {Qo} J の熱を捨てる。熱効率を小数で答えなさい。",
                    e, f"1-Rational({Qo},{Qin})", "$e=1-\\dfrac{Q_{\\text{out}}}{Q_{\\text{in}}}$。", "", d=2,
                    ap="1サイクルで $\\Delta U=0$ なので、正味の仕事は $Q_{\\text{in}}-Q_{\\text{out}}$。",
                    steps=[f"$W'={Qin}-{Qo}={W}\\,\\mathrm{{J}}$。", f"$e=\\dfrac{{{W}}}{{{Qin}}}={t(e)}$。"],
                    alt=["捨てた熱の割合 $\\dfrac{" + str(Qo) + "}{" + str(Qin) + "}$ を 1 から引く。"],
                    pc=[("正味の仕事を求めている", 1), ("値が正しい", 1)], pit=["$\\dfrac{Q_{\\text{out}}}{Q_{\\text{in}}}$ を熱効率とする。"])
    if kind == "qout":
        return numq(f"ある熱機関は、1サイクルごとに高温の熱源から {Qin} J の熱を受け取り、正味 {W} J の仕事をする。1サイクルで低温の熱源へ捨てる熱は何 J か。",
                    sp.Integer(Qin - W), f"{Qin}-{W}", "$Q_{\\text{out}}=Q_{\\text{in}}-W'$。", "J", d=1,
                    ap="1サイクルでもとの状態に戻るので、エネルギーの収支は $Q_{\\text{in}}=W'+Q_{\\text{out}}$。",
                    steps=["$\\Delta U=0$ より $Q_{\\text{in}}=W'+Q_{\\text{out}}$。", f"$Q_{{\\text{{out}}}}={Qin}-{W}={Qin - W}\\,\\mathrm{{J}}$。"],
                    alt=["熱効率 $e=\\dfrac{W'}{Q_{\\text{in}}}$ を求め、$(1-e)Q_{\\text{in}}$ としてもよい。"],
                    pc=[("エネルギーの収支を用いている", 1), ("値が正しい", 1)], pit=["仕事と熱を足す。"])
    e = sp.Rational(W, Qin)
    return numq(f"熱効率 {t(e)} の熱機関に、1サイクルで正味 {W} J の仕事をさせたい。高温の熱源から1サイクルあたり何 J の熱を受け取る必要があるか。",
                sp.Integer(Qin), f"{W}/{P(e)}", "$Q_{\\text{in}}=\\dfrac{W'}{e}$。", "J", d=2,
                ap="熱効率の定義式を $Q_{\\text{in}}$ について解く。",
                steps=[f"$Q_{{\\text{{in}}}}=\\dfrac{{W'}}{{e}}=\\dfrac{{{W}}}{{{t(e)}}}$。", f"$Q_{{\\text{{in}}}}={Qin}\\,\\mathrm{{J}}$。"],
                alt=["熱効率が1より小さいので、必要な熱は仕事より大きくなるはず、と大小関係で確かめる。"],
                pc=[("定義式を変形している", 1), ("値が正しい", 1)], pit=["$W'\\times e$ とする。"])


CONCEPT = [
    ("同じ温度のヘリウムと酸素の気体について、正しいものを選びなさい。",
     "分子1個あたりの平均運動エネルギーは等しい",
     [("酸素分子のほうが平均運動エネルギーが大きい", "平均運動エネルギー $\\dfrac32k_{\\mathrm{B}}T$ は温度だけで決まり、分子の種類によらない。", "質量と運動エネルギーの混同"),
      ("二乗平均速度は等しい", "運動エネルギーが等しいので、質量の小さいヘリウムのほうが速い。", "速さと運動エネルギーの混同"),
      ("ヘリウム分子のほうが平均運動エネルギーが大きい", "温度が同じなら平均運動エネルギーは同じ。速さが大きいのは質量が小さいためである。", "速さと運動エネルギーの混同")]),
    ("理想気体の等温変化について、正しいものを選びなさい。",
     "膨張するとき、気体が外部にした仕事と同じだけの熱を吸収する",
     [("熱の出入りはない", "熱の出入りがないのは断熱変化。等温では $\\Delta U=0$ なので $Q=W'$。", "等温と断熱の混同"),
      ("内部エネルギーは体積に比例して増える", "理想気体の内部エネルギーは温度だけで決まり、等温なら変化しない。", "内部エネルギーの決まり方の誤解"),
      ("圧力は一定に保たれる", "等温変化では $pV=$ 一定で、膨張すれば圧力は下がる。", "等温と定圧の混同")]),
    ("理想気体を断熱圧縮したときの変化について、正しいものを選びなさい。",
     "外部からされた仕事の分だけ内部エネルギーが増え、温度が上がる",
     [("熱の出入りがないので温度は変わらない", "$Q=0$ でも仕事 $W>0$ を受けるので $\\Delta U=W>0$、温度は上がる。", "断熱と等温の混同"),
      ("温度は下がる", "温度が下がるのは断熱膨張のとき。圧縮では仕事を受けて温度が上がる。", "膨張と圧縮の取り違え"),
      ("圧力は変わらない", "体積が減り温度が上がるので、圧力は大きくなる。", "状態方程式の誤用")]),
    ("$n$ mol の単原子分子理想気体の温度を $\\Delta T$ だけ上げるとき、正しいものを選びなさい。",
     "定圧で上げるほうが、定積で上げるより多くの熱が必要である",
     [("定積で上げるほうが多くの熱が必要である", "定圧では膨張して外部に仕事をする分だけ余分に熱が必要（$C_p=C_V+R$）。", "モル比熱の大小の取り違え"),
      ("どちらでも必要な熱は同じである", "$\\Delta U$ は同じだが、定圧では仕事 $nR\\Delta T$ の分だけ熱が多く必要。", "内部エネルギーと熱量の混同"),
      ("定圧で上げるときは内部エネルギーの増加が大きい", "$\\Delta U=\\dfrac32nR\\Delta T$ は過程によらず同じ。違うのは熱と仕事。", "内部エネルギーの決まり方の誤解")]),
    ("気体分子運動論で、容器の壁が気体から圧力を受ける理由として正しいものを選びなさい。",
     "多数の分子が壁に衝突してはね返るとき、壁に力積を与えるから",
     [("分子どうしが反発し合う力が壁に伝わるから", "理想気体のモデルでは分子間力を無視している。圧力は壁との衝突による力積で説明される。", "モデルの仮定の誤解"),
      ("分子が壁に付着して壁を押し広げるから", "分子は壁と弾性衝突してはね返る。付着するのではない。", "衝突のモデルの誤解"),
      ("気体の重さが壁にかかるから", "容器の壁が受ける圧力のほとんどは分子の衝突による。気体の重さによる圧力の差はふつう無視できる。", "圧力の原因の誤解")]),
    ("熱機関について正しいものを選びなさい。",
     "吸収した熱をすべて仕事に変える熱機関はつくれない",
     [("摩擦をなくせば熱効率を1にできる", "熱力学第二法則により、低温の熱源に熱を捨てる必要があるので $e<1$。", "第二法則の無理解"),
      ("1サイクルの間に内部エネルギーは増え続ける", "サイクルではもとの状態に戻るので、1サイクルで $\\Delta U=0$。", "サイクルの意味の誤解"),
      ("熱効率は、捨てた熱を吸収した熱で割った値である", "熱効率は正味の仕事を吸収した熱で割った値 $\\dfrac{W'}{Q_{\\text{in}}}$。", "定義の取り違え")]),
    ("$p$−$V$ グラフについて正しいものを選びなさい。",
     "グラフと $V$ 軸で囲まれた部分の面積は、気体が外部にした仕事の大きさを表す",
     [("グラフの傾きが気体のした仕事を表す", "仕事は $p\\Delta V$ の和なので、面積で表される。", "傾きと面積の取り違え"),
      ("体積が減る過程でも、気体は外部に正の仕事をする", "圧縮では気体は外部から仕事をされる（気体がした仕事は負）。", "仕事の符号の誤解"),
      ("始めと終わりの状態が同じなら、どの経路でも仕事は等しい", "仕事はグラフの面積なので経路によって変わる。経路によらないのは内部エネルギーの変化。", "状態量と過程量の混同")]),
    ("気体の温度について正しいものを選びなさい。",
     "絶対温度は、気体分子の平均運動エネルギーに比例する",
     [("セルシウス温度が2倍になると、分子の平均運動エネルギーも2倍になる", "比例するのは絶対温度。$10\\,{}^\\circ\\mathrm{C}$ と $20\\,{}^\\circ\\mathrm{C}$ では $\\dfrac{293}{283}$ 倍。", "セルシウス温度と絶対温度の混同"),
      ("温度が $0\\,{}^\\circ\\mathrm{C}$ のとき、分子は運動していない", "$0\\,{}^\\circ\\mathrm{C}=273\\,\\mathrm{K}$ でも分子は激しく運動している。", "温度の原点の誤解"),
      ("温度が高い気体ほど、分子1個の質量が大きい", "温度は運動の激しさを表し、分子の質量とは関係がない。", "温度の意味の誤解")]),
]


@gen("basic_check", 3, ["concept", "condition_check"])
def concept_mc(r):
    stem, right, wr = r.choice(CONCEPT)
    return mc(stem, [right] + [w[0] for w in wr], f"正しいのは「{right}」。" + wr[0][1], d=2,
              ap="状態量（$p,\\ V,\\ T,\\ U$）と過程によって決まる量（$Q,\\ W$）を区別し、第一法則と分子運動論に照らして判断する。",
              steps=["各選択肢を、状態方程式・第一法則・$\\dfrac32k_{\\mathrm{B}}T$ の関係で確認する。", f"矛盾しないのは「{right}」。"],
              alt=["誤りの選択肢が正しいとすると、エネルギー保存（第一法則）や状態方程式と矛盾する具体例をつくって消去する。"],
              pc=[("判断の根拠となる法則を確認している", 1), ("正しい選択肢を選んでいる", 1)],
              why={w[0]: (w[1], w[2]) for w in wr})


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 4, ["computation", "application"])
def state_apps(r):
    kind = r.choice(["cock", "leak", "piston", "tire"])
    if kind == "cock":
        while True:
            V1, V2 = r.sample([1, 2, 3, 4, 6], 2)
            p1, p2 = r.sample(["1.0", "2.0", "3.0", "4.0", "5.0"], 2)
            p = (Q(p1) * V1 + Q(p2) * V2) / (V1 + V2)
            if is_exact(t(p), p):
                break
        return numq(f"容積 {V1}.0 L の容器 A に圧力 ${p1}\\times10^5\\,\\mathrm{{Pa}}$ の気体が、容積 {V2}.0 L の容器 B に圧力 ${p2}\\times10^5\\,\\mathrm{{Pa}}$ の同じ温度の気体が入っている。A と B を細い管でつなぎ、コックを開いて十分に時間がたった。温度は変わらないものとして、全体の圧力は何 Pa か。",
                    p * 10 ** 5, f"({P(Q(p1))}*{V1}+{P(Q(p2))}*{V2})*10**5/({V1}+{V2})", "物質量の和が保存される：$p_{\\mathrm{A}}V_{\\mathrm{A}}+p_{\\mathrm{B}}V_{\\mathrm{B}}=p(V_{\\mathrm{A}}+V_{\\mathrm{B}})$。", "Pa", d=3,
                    ap="温度一定なら物質量は $pV$ に比例する。混ぜる前後で物質量の和は変わらない。",
                    steps=[f"$n\\propto pV$ より ${p1}\\times{V1}+{p2}\\times{V2}=p\\times{V1 + V2}$（$p$ は $10^5\\,\\mathrm{{Pa}}$ 単位）。",
                           f"$p={t(p)}\\times10^5\\,\\mathrm{{Pa}}$。"],
                    alt=["分圧で考える：A の気体は体積が $\\dfrac{" + str(V1 + V2) + "}{" + str(V1) + "}$ 倍に広がり、分圧は逆数倍。B も同様に求めて和をとる。"],
                    pc=[("物質量の保存を用いている", 2), ("値が正しい", 2)], pit=["2つの圧力の単純な平均をとる。"])
    (c1, T1), (c2, T2) = r.sample([x for x in TEMPS if x[1] >= 250], 2)
    if T2 < T1:
        (c1, T1), (c2, T2) = (c2, T2), (c1, T1)
    if kind == "leak":
        frac_ = sp.Rational(T1, T2)
        return numq(f"栓に小さな穴のあいた容器に空気が入っており、はじめ温度は ${ctx(c1)}$ であった。容器を ${ctx(c2)}$ まで加熱すると、内部の空気の一部が穴から外に出て、容器内の圧力は外の大気圧と等しいまま保たれた。加熱後に容器内に残っている空気の物質量は、はじめの何倍か。",
                    frac_, f"Rational({c1}+273,{c2}+273)", "$p,\\ V$ が一定なので $nT=$ 一定。", "倍", d=3,
                    ap="気体が出入りするのでボイル・シャルルの法則は使えない。状態方程式 $pV=nRT$ で $p,\\ V$ が一定とみる。",
                    steps=[f"$pV=n_1RT_1=n_2RT_2$。", f"$\\dfrac{{n_2}}{{n_1}}=\\dfrac{{T_1}}{{T_2}}=\\dfrac{{{T1}}}{{{T2}}}={t(frac_)}$ 倍。"],
                    alt=["加熱した空気が容器の外まで膨張すると考えると、体積は $\\dfrac{T_2}{T_1}$ 倍になり、そのうち容器に残るのは $\\dfrac{T_1}{T_2}$ の割合、と考えてもよい。"],
                    pc=[("状態方程式で物質量を比べている", 2), ("絶対温度の比で値を求めている", 2)], pit=["物質量が一定としてボイル・シャルルの法則を使う。"])
    if kind == "piston":
        V1 = r.choice(["2.0", "3.0", "4.0", "6.0"])
        ps = r.choice(["1.0", "2.0"])
        V2 = Q(V1) * sp.Rational(T2, T1)
        W = Q(ps) * 10 ** 5 * (V2 - Q(V1)) / 1000
        return numq(f"なめらかに動くピストンのついたシリンダーに、圧力 ${ps}\\times10^5\\,\\mathrm{{Pa}}$、温度 ${ctx(c1)}$、体積 {V1} L の気体が入っている。圧力を一定に保ったまま温度を ${ctx(c2)}$ にした。この間に気体が外部にした仕事は何 J か。",
                    W, f"{P(Q(ps))}*10**5*({P(Q(V1))}*Rational({T2},{T1})-{P(Q(V1))})*10**(-3)", "シャルルの法則で体積を求め、$W'=p\\Delta V$。", "J", d=3,
                    ap="定圧変化。まず変化後の体積をシャルルの法則で求め、体積の増加に圧力をかける。",
                    steps=[f"$V_2={V1}\\times\\dfrac{{{T2}}}{{{T1}}}={t(V2, 3)}\\,\\mathrm{{L}}$。", f"$\\Delta V={t(V2 - Q(V1), 3)}\\times10^{{-3}}\\,\\mathrm{{m^3}}$。",
                           f"$W'=p\\Delta V\\fallingdotseq{t(W)}\\,\\mathrm{{J}}$。"],
                    alt=["状態方程式から $W'=p\\Delta V=nR\\Delta T$ であることを使い、$\\dfrac{pV_1}{T_1}\\Delta T$ として計算しても同じ。"],
                    pc=[("変化後の体積を求めている", 1), ("$W'=p\\Delta V$ を単位をそろえて用いている", 2), ("値が正しい", 1)], pit=["L を m³ に直し忘れる。"])
    p1 = r.choice(["2.0", "2.4", "3.0", "1.8"])
    p2 = Q(p1) * sp.Rational(T2, T1)
    return numq(f"タイヤ（容積は一定とみなす）に空気が入っており、温度 ${ctx(c1)}$ で圧力は ${p1}\\times10^5\\,\\mathrm{{Pa}}$ であった。走行して空気の温度が ${ctx(c2)}$ に上がったとき、圧力は何 Pa になるか。空気は漏れないものとする。",
                p2 * 10 ** 5, f"{P(Q(p1))}*10**5*Rational({T2},{T1})", "体積・物質量一定 → $\\dfrac{p}{T}=$ 一定。", "Pa", d=2,
                ap="密閉・容積一定なので、圧力は絶対温度に比例する。",
                steps=[f"$T_1={T1}\\,\\mathrm{{K}}$、$T_2={T2}\\,\\mathrm{{K}}$。", f"$p_2={p1}\\times10^5\\times\\dfrac{{{T2}}}{{{T1}}}\\fallingdotseq{t(p2 * 10 ** 5)}\\,\\mathrm{{Pa}}$。"],
                alt=["分子の平均運動エネルギーが増え、壁に与える力積が大きくなるので圧力が上がる、と分子運動論の立場で説明して大小を確かめる。"],
                pc=[("$p\\propto T$（絶対温度）を用いている", 2), ("値が正しい", 2)], pit=["℃ の比をかける。"])


@gen("standard_practice", 3, ["computation", "cross_unit"], rel=["HS-CHEB-U02"])
def mole_apps(r):
    kind = r.choice(["n", "N", "mass", "M"])
    T = r.choice([300, 400, 250, 500])
    p = r.choice(["1.0", "2.0", "1.5", "3.0"])
    V = r.choice(["8.31", "16.6", "24.9", "4.155"])
    if kind == "n":
        n = Q(p) * 10 ** 5 * Q(V) / 1000 / (R * T)
        return numq(f"容積 {V} L の容器に、温度 {T} K、圧力 ${p}\\times10^5\\,\\mathrm{{Pa}}$ の理想気体が入っている。気体の物質量は何 mol か。" + RS,
                    n, f"{P(Q(p))}*10**5*{P(Q(V))}*10**(-3)/(Rational(831,100)*{T})", "$n=\\dfrac{pV}{RT}$。", "mol", d=2,
                    ap="状態方程式に SI 単位（Pa、m³、K）で代入する。",
                    steps=[f"$V={V}\\times10^{{-3}}\\,\\mathrm{{m^3}}$。", f"$n=\\dfrac{{{p}\\times10^5\\times{V}\\times10^{{-3}}}}{{8.31\\times{T}}}\\fallingdotseq{t(n)}\\,\\mathrm{{mol}}$。"],
                    alt=["標準状態（$273\\,\\mathrm{K}$、$1.013\\times10^5\\,\\mathrm{Pa}$）で 1 mol が約 22.4 L になることを目安に、答えの大きさを確かめる。"],
                    pc=[("状態方程式を用いている", 2), ("単位をそろえて値が正しい", 2)], pit=["L のまま代入して 1000 倍の値にする。"])
    if kind == "N":
        N = Q(p) * 10 ** 5 * Q(V) / 1000 / (KB * T)
        return numq(f"容積 {V} L の容器に、温度 {T} K、圧力 ${p}\\times10^5\\,\\mathrm{{Pa}}$ の理想気体が入っている。容器内の気体分子の数はいくらか。ボルツマン定数を $1.38\\times10^{{-23}}\\,\\mathrm{{J/K}}$ とする。",
                    N, f"{P(Q(p))}*10**5*{P(Q(V))}*10**(-3)/(Rational(138,100)*10**(-23)*{T})", "$pV=Nk_{\\mathrm{B}}T$ より $N=\\dfrac{pV}{k_{\\mathrm{B}}T}$。", "個", n=2, d=3,
                    ap="分子数を直接求めるときは、気体定数の代わりにボルツマン定数を使った状態方程式 $pV=Nk_{\\mathrm{B}}T$。",
                    steps=[f"$N=\\dfrac{{{p}\\times10^5\\times{V}\\times10^{{-3}}}}{{1.38\\times10^{{-23}}\\times{T}}}$。", f"$N\\fallingdotseq{t(N, 2)}$ 個。"],
                    alt=["物質量 $n=\\dfrac{pV}{RT}$ を求めてアボガドロ定数 $6.0\\times10^{23}\\,/\\mathrm{mol}$ をかけても、ほぼ同じ値になる（$k_{\\mathrm{B}}=\\dfrac{R}{N_{\\mathrm{A}}}$）。"],
                    pc=[("$pV=Nk_{\\mathrm{B}}T$ を用いている", 2), ("値が正しい", 2)], pit=["指数の計算を誤る。"])
    name, Mg = r.choice([("酸素", 32), ("窒素", 28), ("ヘリウム", 4), ("二酸化炭素", 44)])
    if kind == "mass":
        n = Q(p) * 10 ** 5 * Q(V) / 1000 / (R * T)
        m = n * Mg
        return numq(f"容積 {V} L の容器に、温度 {T} K、圧力 ${p}\\times10^5\\,\\mathrm{{Pa}}$ の{name}（モル質量 {Mg} g/mol）が入っている。容器内の{name}の質量は何 g か。" + RS,
                    m, f"{P(Q(p))}*10**5*{P(Q(V))}*10**(-3)/(Rational(831,100)*{T})*{Mg}", "物質量を求め、モル質量をかける。", "g", d=3,
                    ap="状態方程式で物質量を求め、化学基礎で学んだ「質量＝物質量×モル質量」を使う。",
                    steps=[f"$n=\\dfrac{{pV}}{{RT}}\\fallingdotseq{t(n, 3)}\\,\\mathrm{{mol}}$。", f"質量 $={t(n, 3)}\\times{Mg}\\fallingdotseq{t(m)}\\,\\mathrm{{g}}$。"],
                    alt=["$pV=\\dfrac{w}{M}RT$（$w$ は質量）と変形した式に代入して一度に求めてもよい。"],
                    pc=[("物質量を求めている", 2), ("質量に換算して値が正しい", 2)], pit=["モル質量をかけ忘れて物質量を答える。"])
    w = r.choice(["1.6", "3.2", "0.80", "2.0"])
    n = Q(p) * 10 ** 5 * Q(V) / 1000 / (R * T)
    M = Q(w) / n
    return numq(f"ある気体 {w} g を容積 {V} L の容器に入れたところ、温度 {T} K で圧力が ${p}\\times10^5\\,\\mathrm{{Pa}}$ になった。この気体のモル質量は何 g/mol か。" + RS,
                M, f"{P(Q(w))}/({P(Q(p))}*10**5*{P(Q(V))}*10**(-3)/(Rational(831,100)*{T}))", "$M=\\dfrac{w}{n}$、$n=\\dfrac{pV}{RT}$。", "g/mol", d=3,
                ap="状態方程式で物質量を求め、質量を物質量で割る。",
                steps=[f"$n=\\dfrac{{pV}}{{RT}}\\fallingdotseq{t(n, 3)}\\,\\mathrm{{mol}}$。", f"$M=\\dfrac{{{w}}}{{{t(n, 3)}}}\\fallingdotseq{t(M)}\\,\\mathrm{{g/mol}}$。"],
                alt=["$M=\\dfrac{wRT}{pV}$ と文字式で整理してから代入すると、計算の途中での丸め誤差が少ない。"],
                pc=[("物質量を求めている", 2), ("モル質量が正しい", 2)], pit=["L を m³ に直し忘れる。"])


@gen("standard_practice", 4, ["computation", "condition_check"])
def process_heat(r):
    kind = r.choice(["v_Q", "p_Q", "p_W", "p_dT", "p_dU"])
    n = r.choice(["0.50", "1.0", "2.0", "0.20", "4.0"])
    nn = Q(n)
    dT = r.choice([10, 20, 30, 50, 100])
    if kind == "v_Q":
        Qv = sp.Rational(3, 2) * nn * R * dT
        return numq(f"{n} mol の{MONO}を、体積を一定に保ったまま加熱し、温度を {dT} K 上げた。気体が吸収した熱量は何 J か。" + RS,
                    Qv, f"Rational(3,2)*{P(nn)}*Rational(831,100)*{dT}", "定積では $W=0$ なので $Q=\\Delta U=\\dfrac32nR\\Delta T$。", "J", d=2,
                    ap="体積一定なら気体は仕事をしない。吸収した熱はすべて内部エネルギーの増加になる。",
                    steps=["$W'=0$ より $Q=\\Delta U$。", f"$Q=\\dfrac32\\times{n}\\times8.31\\times{dT}\\fallingdotseq{t(Qv)}\\,\\mathrm{{J}}$。"],
                    alt=["定積モル比熱 $C_V=\\dfrac32R$ を用いて $Q=nC_V\\Delta T$ と計算しても同じ。"],
                    pc=[("$W'=0$ を用いている", 2), ("値が正しい", 2)], pit=["$\\dfrac52$ を使う（定圧と混同）。"])
    if kind == "p_Q":
        Qv = sp.Rational(5, 2) * nn * R * dT
        return numq(f"{n} mol の{MONO}を、圧力を一定に保ったまま加熱し、温度を {dT} K 上げた。気体が吸収した熱量は何 J か。" + RS,
                    Qv, f"Rational(5,2)*{P(nn)}*Rational(831,100)*{dT}", "$Q=\\Delta U+W'=\\dfrac32nR\\Delta T+nR\\Delta T=\\dfrac52nR\\Delta T$。", "J", d=3,
                    ap="定圧変化では膨張して外部に仕事 $p\\Delta V=nR\\Delta T$ をするので、その分の熱も必要。",
                    steps=[f"$\\Delta U=\\dfrac32nR\\Delta T$、$W'=p\\Delta V=nR\\Delta T$。", f"$Q=\\dfrac52\\times{n}\\times8.31\\times{dT}\\fallingdotseq{t(Qv)}\\,\\mathrm{{J}}$。"],
                    alt=["定圧モル比熱 $C_p=C_V+R=\\dfrac52R$（マイヤーの関係）を用いて $Q=nC_p\\Delta T$。"],
                    pc=[("仕事の分を含めて第一法則を用いている", 2), ("値が正しい", 2)], pit=["$\\dfrac32nR\\Delta T$ とする。"])
    if kind == "p_W":
        W = nn * R * dT
        return numq(f"{n} mol の理想気体を、圧力を一定に保ったまま加熱したところ、温度が {dT} K 上昇した。この間に気体が外部にした仕事は何 J か。" + RS,
                    W, f"{P(nn)}*Rational(831,100)*{dT}", "定圧では $W'=p\\Delta V=nR\\Delta T$。", "J", d=3,
                    ap="圧力も体積もわからないが、状態方程式 $pV=nRT$ の変化分をとると $p\\Delta V=nR\\Delta T$。",
                    steps=["$p\\Delta V=nR\\Delta T$（$p$ 一定で状態方程式の差をとる）。", f"$W'={n}\\times8.31\\times{dT}\\fallingdotseq{t(W)}\\,\\mathrm{{J}}$。"],
                    alt=["$p=1.0\\times10^5\\,\\mathrm{Pa}$ などと仮に決めて前後の体積を計算しても、同じ $W'$ が得られる（$p$ によらない）。"],
                    pc=[("$p\\Delta V=nR\\Delta T$ を用いている", 2), ("値が正しい", 2)], pit=["圧力や体積が与えられていないので求められないと考える。"])
    Qv = r.choice([500, 831, 1662, 2493, 4155, 1000])
    if kind == "p_dT":
        dTv = Qv / (sp.Rational(5, 2) * nn * R)
        return numq(f"{n} mol の{MONO}に、圧力を一定に保ったまま {Qv} J の熱を与えた。気体の温度は何 K 上昇するか。" + RS,
                    dTv, f"{Qv}/(Rational(5,2)*{P(nn)}*Rational(831,100))", "$Q=\\dfrac52nR\\Delta T$ を $\\Delta T$ について解く。", "K", d=3,
                    ap="定圧変化の吸熱量は $nC_p\\Delta T=\\dfrac52nR\\Delta T$。",
                    steps=[f"${Qv}=\\dfrac52\\times{n}\\times8.31\\times\\Delta T$。", f"$\\Delta T\\fallingdotseq{t(dTv)}\\,\\mathrm{{K}}$。"],
                    alt=["同じ熱を定積で与えた場合（$\\dfrac32$）の温度上昇より小さくなることで確かめる。"],
                    pc=[("定圧モル比熱を用いている", 2), ("値が正しい", 2)], pit=["$\\dfrac32nR$ で割る。"])
    dU = sp.Rational(3, 5) * Qv
    return numq(f"{MONO}に、圧力を一定に保ったまま {Qv} J の熱を与えた。気体の内部エネルギーの増加量は何 J か。",
                dU, f"Rational(3,5)*{Qv}", "定圧では $Q:\\Delta U:W'=\\dfrac52:\\dfrac32:1$。", "J", d=4,
                ap="定圧変化では $\\Delta U=\\dfrac32nR\\Delta T$、$Q=\\dfrac52nR\\Delta T$ なので、$\\Delta U=\\dfrac35Q$。",
                steps=["$\\dfrac{\\Delta U}{Q}=\\dfrac{\\frac32nR\\Delta T}{\\frac52nR\\Delta T}=\\dfrac35$。", f"$\\Delta U=\\dfrac35\\times{Qv}={t(dU)}\\,\\mathrm{{J}}$。"],
                alt=[f"残りの $\\dfrac25Q={t(sp.Rational(2, 5) * Qv)}\\,\\mathrm{{J}}$ が外部への仕事になることを確かめる。"],
                pc=[("$\\Delta U$ と $Q$ の比を導いている", 2), ("値が正しい", 2)], pit=["与えた熱がすべて内部エネルギーになるとする。"])


@gen("standard_practice", 3, ["computation", "concept"])
def pv_graph(r):
    kind = r.choice(["isobar", "line", "compress"])
    if kind == "isobar":
        p, V1, V2 = r.choice([(2, 1, 5), (3, 2, 6), (1, 1, 6), (4, 2, 5), (2, 3, 6)])
        pts = [(V1, p), (V2, p)]
        W = p * (V2 - V1) * 100
        desc_ = f"圧力 ${p}.0\\times10^5\\,\\mathrm{{Pa}}$ 一定で体積が ${V1}.0\\times10^{{-3}}\\,\\mathrm{{m^3}}$ から ${V2}.0\\times10^{{-3}}\\,\\mathrm{{m^3}}$ に変化"
    elif kind == "line":
        p1, p2, V1, V2 = r.choice([(1, 3, 1, 5), (4, 2, 1, 4), (1, 4, 2, 6), (3, 1, 2, 6), (2, 4, 1, 3)])
        pts = [(V1, p1), (V2, p2)]
        W = sp.Rational((p1 + p2) * (V2 - V1), 2) * 100
        desc_ = f"状態 A（圧力 ${p1}.0\\times10^5\\,\\mathrm{{Pa}}$、体積 ${V1}.0\\times10^{{-3}}\\,\\mathrm{{m^3}}$）から状態 B（圧力 ${p2}.0\\times10^5\\,\\mathrm{{Pa}}$、体積 ${V2}.0\\times10^{{-3}}\\,\\mathrm{{m^3}}$）まで、グラフ上で直線的に変化"
    else:
        p1, p2, V1, V2 = r.choice([(1, 3, 5, 2), (2, 4, 6, 2), (1, 2, 6, 3), (2, 2, 5, 1)])
        pts = [(V1, p1), (V2, p2)]
        W = -sp.Rational((p1 + p2) * (V1 - V2), 2) * 100
        desc_ = f"状態 A（圧力 ${p1}.0\\times10^5\\,\\mathrm{{Pa}}$、体積 ${V1}.0\\times10^{{-3}}\\,\\mathrm{{m^3}}$）から状態 B（圧力 ${p2}.0\\times10^5\\,\\mathrm{{Pa}}$、体積 ${V2}.0\\times10^{{-3}}\\,\\mathrm{{m^3}}$）まで、グラフ上で直線的に圧縮"
    lab = {"isobar": "圧力一定の水平な線分", "line": "A から B への直線（膨張）", "compress": "A から B への直線（圧縮）"}[kind]
    fig = figure(f"p−V グラフ。{lab}。A({pts[0][0]}, {pts[0][1]})、B({pts[1][0]}, {pts[1][1]})（目盛りは p が 10⁵ Pa、V が 10⁻³ m³）", pv_svg(pts))
    return numq(f"一定量の理想気体を、図の $p$−$V$ グラフのように{desc_}させた。図の過程で気体が外部にした仕事は何 J か。外部から仕事をされた場合は負の値で答えなさい。",
                W, f"{P(W / 100)}*10**5*10**(-3)", "気体がした仕事は $p$−$V$ グラフと $V$ 軸で囲まれた部分の面積（膨張なら正、圧縮なら負）。", "J", d=3, fig=fig,
                ap="$W'=p\\Delta V$ を細かく足し合わせたもの＝グラフの下の面積。目盛りの単位（$10^5\\times10^{-3}=100$ J）に注意。",
                steps=["グラフの下の部分（長方形または台形）の面積を目盛りで求める。", f"目盛り1マスは $10^5\\times10^{{-3}}=100\\,\\mathrm{{J}}$。",
                       f"$W'={t(W)}\\,\\mathrm{{J}}${'（圧縮なので負）' if W < 0 else ''}。"],
                alt=["台形の面積は「平均の圧力 × 体積変化」と同じなので、$\\dfrac{p_{\\mathrm{A}}+p_{\\mathrm{B}}}{2}\\times\\Delta V$ で計算してもよい。"],
                pc=[("面積が仕事を表すことを用いている", 2), ("符号を含めて値が正しい", 2)], pit=["$p_{\\mathrm{B}}V_{\\mathrm{B}}-p_{\\mathrm{A}}V_{\\mathrm{A}}$ を仕事とする。", "目盛りの $10^5$、$10^{-3}$ を忘れる。"])


@gen("standard_practice", 3, ["computation", "application"])
def kinetic_apps(r):
    kind = r.choice(["totalK", "rho", "pressure"])
    if kind == "totalK":
        p = r.choice(["1.0", "2.0", "1.5"])
        V = r.choice(["2.0", "4.0", "10", "3.0"])
        K = sp.Rational(3, 2) * Q(p) * 10 ** 5 * Q(V) / 1000
        return numq(f"圧力 ${p}\\times10^5\\,\\mathrm{{Pa}}$、体積 {V} L の{MONO}がある。気体分子の運動エネルギーの総和（内部エネルギー）は何 J か。",
                    K, f"Rational(3,2)*{P(Q(p))}*10**5*{P(Q(V))}*10**(-3)", "$U=\\dfrac32nRT=\\dfrac32pV$。", "J", d=2,
                    ap="温度も物質量も与えられていないが、状態方程式 $nRT=pV$ を使えば $U=\\dfrac32pV$。",
                    steps=["$U=\\dfrac32nRT=\\dfrac32pV$。", f"$U=\\dfrac32\\times{p}\\times10^5\\times{V}\\times10^{{-3}}={t(K)}\\,\\mathrm{{J}}$。"],
                    alt=["分子運動論の $pV=\\dfrac13Nm\\overline{v^2}$ から、運動エネルギーの総和 $\\dfrac12Nm\\overline{v^2}=\\dfrac32pV$ を直接導いてもよい。"],
                    pc=[("$U=\\dfrac32pV$ を導いている", 2), ("値が正しい", 2)], pit=["L を m³ に直し忘れる。"])
    if kind == "rho":
        p = r.choice(["1.0", "1.2", "2.0", "3.0"])
        rho = r.choice(["0.16", "1.2", "1.3", "0.090", "1.6"])
        v = sp.sqrt(3 * Q(p) * 10 ** 5 / Q(rho))
        return numq(f"圧力 ${p}\\times10^5\\,\\mathrm{{Pa}}$、密度 {rho} kg/m³ の理想気体がある。気体分子の二乗平均速度 $\\sqrt{{\\overline{{v^2}}}}$ は何 m/s か。",
                    v, f"sqrt(3*{P(Q(p))}*10**5/{P(Q(rho))})", "$p=\\dfrac{Nm\\overline{v^2}}{3V}=\\dfrac13\\rho\\overline{v^2}$。", "m/s", n=2, d=3,
                    ap="$\\dfrac{Nm}{V}$ は気体の密度 $\\rho$。分子運動論の圧力の式を密度で書き直す。",
                    steps=["$p=\\dfrac13\\rho\\overline{v^2}$ より $\\overline{v^2}=\\dfrac{3p}{\\rho}$。", f"$\\sqrt{{\\overline{{v^2}}}}=\\sqrt{{\\dfrac{{3\\times{p}\\times10^5}}{{{rho}}}}}\\fallingdotseq{t(v, 2)}\\,\\mathrm{{m/s}}$。"],
                    alt=["状態方程式を密度で表した $p=\\dfrac{\\rho RT}{M}$ を使えば、$\\sqrt{\\dfrac{3RT}{M}}$ と同じ式になることを確かめる。"],
                    pc=[("圧力の式を密度で表している", 2), ("値が正しい", 2)], pit=["3 をかけ忘れる。"])
    Nn = r.choice(["1.0", "2.0", "3.0", "5.0"])
    m = r.choice([("4.0", "6.6\\times10^{-27}", sp.Rational(66, 10) * sp.Rational(1, 10 ** 27))])
    vr = r.choice([1000, 1200, 1300, 1500])
    V = r.choice(["1.0", "2.0", "5.0"])
    N = Q(Nn) * 10 ** 23
    p = N * m[2] * vr ** 2 / (3 * Q(V) / 1000)
    return numq(f"体積 {V} L の容器に、ヘリウム分子（1個の質量 ${m[1]}\\,\\mathrm{{kg}}$）が ${Nn}\\times10^{{23}}$ 個入っており、分子の二乗平均速度は {vr} m/s である。容器の壁が受ける圧力は何 Pa か。",
                p, f"{P(N)}*{P(m[2])}*{vr}**2/(3*{P(Q(V))}*10**(-3))", "$p=\\dfrac{Nm\\overline{v^2}}{3V}$。", "Pa", n=2, d=3,
                ap="分子運動論で導いた圧力の式に代入する。体積は m³。",
                steps=[f"$p=\\dfrac{{{Nn}\\times10^{{23}}\\times{m[1]}\\times{vr}^2}}{{3\\times{V}\\times10^{{-3}}}}$。", f"$p\\fallingdotseq{t(p, 2)}\\,\\mathrm{{Pa}}$。"],
                alt=["気体の全運動エネルギー $\\dfrac12Nm\\overline{v^2}$ を求め、$p=\\dfrac{2}{3}\\cdot\\dfrac{(\\text{全運動エネルギー})}{V}$ としても同じ。"],
                pc=[("圧力の式を用いている", 2), ("値が正しい", 2)], pit=["3 で割り忘れる。", "L を m³ に直し忘れる。"])


@gen("standard_practice", 3, ["computation", "condition_check"])
def mix_adiabatic(r):
    kind = r.choice(["mix", "adia", "mixp"])
    if kind == "adia":
        n = r.choice(["0.50", "1.0", "2.0"])
        Wv = r.choice([300, 623, 831, 1246, 500])
        dT = Wv / (sp.Rational(3, 2) * Q(n) * R)
        return numq(f"{n} mol の{MONO}を断熱圧縮したところ、気体は外部から {Wv} J の仕事をされた。気体の温度は何 K 上昇したか。" + RS,
                    dT, f"{Wv}/(Rational(3,2)*{P(Q(n))}*Rational(831,100))", "$Q=0$ より $\\Delta U=W$、$\\dfrac32nR\\Delta T=W$。", "K", d=3,
                    ap="断熱なので、された仕事がすべて内部エネルギーの増加になる。内部エネルギーの増加から温度変化を求める。",
                    steps=[f"$\\Delta U=W={Wv}\\,\\mathrm{{J}}$。", f"$\\dfrac32\\times{n}\\times8.31\\times\\Delta T={Wv}$ より $\\Delta T\\fallingdotseq{t(dT)}\\,\\mathrm{{K}}$。"],
                    alt=["同じ温度上昇を定積加熱で起こすのに必要な熱が $W$ に等しい、と考えても同じ式になる。"],
                    pc=[("$\\Delta U=W$ としている", 2), ("値が正しい", 2)], pit=["断熱なので温度は変わらないとする。"])
    n1, n2 = r.sample([1, 2, 3, 4], 2)
    T1, T2 = r.sample([200, 300, 400, 500, 600], 2)
    T = sp.Rational(n1 * T1 + n2 * T2, n1 + n2)
    if kind == "mix":
        return numq(f"断熱容器の中が仕切りで2つの部屋に分けられ、一方に {n1}.0 mol、温度 {T1} K の{MONO}、他方に {n2}.0 mol、温度 {T2} K の同じ気体が入っている。仕切りに小さな穴をあけて十分に時間がたったとき、気体の温度は何 K になるか。容器全体の体積は変わらない。",
                    T, f"Rational({n1}*{T1}+{n2}*{T2},{n1}+{n2})", "$Q=0$、$W=0$ なので内部エネルギーの和が保存される。", "K", d=3,
                    ap="断熱容器・体積一定 → 外部との熱・仕事のやりとりがない。内部エネルギーの総和 $\\dfrac32nRT$ が保存される。",
                    steps=[f"$\\dfrac32R({n1}\\times{T1}+{n2}\\times{T2})=\\dfrac32R({n1}+{n2})T$。", f"$T=\\dfrac{{{n1 * T1 + n2 * T2}}}{{{n1 + n2}}}={t(T)}\\,\\mathrm{{K}}$。"],
                    alt=["物質量で重みをつけた温度の平均になっている。2つの温度の間の値になることで確かめる。"],
                    pc=[("内部エネルギーの保存を用いている", 2), ("値が正しい", 2)], pit=["2つの温度の単純平均をとる。"])
    V1, V2 = r.sample([1, 2, 3], 2)
    pf = R * (n1 + n2) * T / ((V1 + V2) * sp.Rational(1, 1000))
    return numq(f"断熱容器の中が仕切りで、容積 {V1}.0 L の部屋 A と容積 {V2}.0 L の部屋 B に分けられている。A には {n1}.0 mol、温度 {T1} K、B には {n2}.0 mol、温度 {T2} K の{MONO}が入っている。仕切りをとり除いて十分に時間がたったときの圧力は何 Pa か。" + RS,
                pf, f"Rational(831,100)*({n1}+{n2})*Rational({n1}*{T1}+{n2}*{T2},{n1}+{n2})/(({V1}+{V2})*10**(-3))", "内部エネルギーの保存で温度を求め、状態方程式で圧力を求める。", "Pa", n=2, d=4,
                ap="まず温度（内部エネルギー保存）、次に全体の状態方程式。$(n_1+n_2)T=n_1T_1+n_2T_2$ に注目すると計算が簡単になる。",
                steps=[f"$T=\\dfrac{{{n1}\\times{T1}+{n2}\\times{T2}}}{{{n1 + n2}}}={t(T, 3)}\\,\\mathrm{{K}}$。",
                       f"$p=\\dfrac{{(n_1+n_2)RT}}{{V}}=\\dfrac{{8.31\\times({n1}\\times{T1}+{n2}\\times{T2})}}{{{V1 + V2}.0\\times10^{{-3}}}}\\fallingdotseq{t(pf, 2)}\\,\\mathrm{{Pa}}$。"],
                alt=["混合後の $pV=\\dfrac23U$ と、$U$ が保存されることから、$p=\\dfrac{p_{\\mathrm{A}}V_{\\mathrm{A}}+p_{\\mathrm{B}}V_{\\mathrm{B}}}{V_{\\mathrm{A}}+V_{\\mathrm{B}}}$ と求めることもできる。"],
                pc=[("内部エネルギーの保存を用いている", 2), ("状態方程式で値を求めている", 2)], pit=["体積を A だけにする。", "L を m³ に直し忘れる。"])


# ======================================================================
# C 思考力・記述応用
# ======================================================================

@gen("thinking_writing", 3, ["written_reasoning", "concept"])
def derive_c(r):
    kind = r.choice(["press", "mayer", "work", "adia", "temp", "isoT"])
    if kind == "press":
        return desc("1辺 $L$ の立方体容器に、質量 $m$ の分子が $N$ 個入っている。分子は壁と弾性衝突し、分子どうしの衝突は無視できるとする。速度の $x$ 成分が $v_x$ の1個の分子に注目して、$x$ 軸に垂直な壁 S が受ける平均の力を求め、さらに気体の圧力が $p=\\dfrac{Nm\\overline{v^2}}{3V}$（$V=L^3$）となることを示しなさい。",
                    "分子が壁 S に1回衝突すると運動量は $mv_x\\to-mv_x$ と変化し、壁は力積 $2mv_x$ を受ける。分子は $\\dfrac{2L}{v_x}$ ごとに S に当たるので、時間 $t$ の間の衝突回数は $\\dfrac{v_xt}{2L}$、壁が受ける力積は $\\dfrac{mv_x{}^2}{L}t$。よって1個の分子による平均の力は $\\dfrac{mv_x{}^2}{L}$。$N$ 個では $F=\\dfrac{Nm\\overline{v_x{}^2}}{L}$。運動の方向にかたよりがないので $\\overline{v_x{}^2}=\\overline{v_y{}^2}=\\overline{v_z{}^2}=\\dfrac13\\overline{v^2}$。$p=\\dfrac{F}{L^2}=\\dfrac{Nm\\overline{v^2}}{3L^3}=\\dfrac{Nm\\overline{v^2}}{3V}$。",
                    "1回の衝突の力積 × 単位時間あたりの衝突回数 = 平均の力。",
                    [("1回の衝突で壁が受ける力積 $2mv_x$ を求めている", 2), ("衝突の間隔（回数）から平均の力を求めている", 3), ("$\\overline{v_x{}^2}=\\dfrac13\\overline{v^2}$ を用いて圧力の式を導いている", 3)], d=4, p=8, kind="proof", lines=9,
                    ps=["cross_unit"], rel=["HS-PHY-U01"],
                    ap="力学で学んだ「運動量の変化＝力積」を、壁と分子の衝突に使う。",
                    steps=["力積 $2mv_x$。", "回数 $\\dfrac{v_xt}{2L}$ → 平均の力 $\\dfrac{mv_x{}^2}{L}$。", "和と等方性 → $p=\\dfrac{Nm\\overline{v^2}}{3V}$。"],
                    alt=["次元で確かめる：$\\dfrac{Nm\\overline{v^2}}{V}$ の単位は $\\dfrac{\\mathrm{kg\\cdot m^2/s^2}}{\\mathrm{m^3}}=\\mathrm{N/m^2}=\\mathrm{Pa}$。"],
                    pc=[("力積", 2), ("平均の力", 3), ("圧力", 3)], pit=["力積を $mv_x$ とする（はね返りで2倍になることを忘れる）。"],
                    chk=("simplify(2*m*v*(v*t/(2*a))/t)", "m*v**2/a", None, "intermediate"))
    if kind == "mayer":
        return desc("$n$ mol の単原子分子理想気体について、定積モル比熱 $C_V=\\dfrac32R$、定圧モル比熱 $C_p=\\dfrac52R$ となることを、熱力学第一法則と状態方程式を用いて導きなさい。また、$C_p>C_V$ となる理由を述べなさい。",
                    "定積変化では仕事をしないので $Q=\\Delta U=\\dfrac32nR\\Delta T$、よって $C_V=\\dfrac{Q}{n\\Delta T}=\\dfrac32R$。定圧変化では気体が外部にする仕事が $W'=p\\Delta V$ で、状態方程式 $pV=nRT$ の変化分をとると $p\\Delta V=nR\\Delta T$。第一法則より $Q=\\Delta U+W'=\\dfrac32nR\\Delta T+nR\\Delta T=\\dfrac52nR\\Delta T$、よって $C_p=\\dfrac52R$。定圧では温度を上げるときに膨張して外部に仕事をするので、その分だけ余分に熱が必要になるから $C_p>C_V$ となる（$C_p-C_V=R$）。",
                    "$\\Delta U$ はどちらも $\\dfrac32nR\\Delta T$。違いは仕事の有無。",
                    [("定積で $C_V=\\dfrac32R$ を導いている", 2), ("定圧で $p\\Delta V=nR\\Delta T$ を示し $C_p=\\dfrac52R$ を導いている", 4), ("$C_p>C_V$ の理由を仕事と結びつけて述べている", 2)], d=3, p=8, kind="proof", lines=8,
                    ap="比熱は「1 mol を 1 K 上げるのに必要な熱」。第一法則で熱を内部エネルギーと仕事に分ける。",
                    steps=["定積：$Q=\\Delta U$。", "定圧：$Q=\\Delta U+nR\\Delta T$。", "差 $R$ は仕事の分。"],
                    alt=["$C_p-C_V=R$（マイヤーの関係）は単原子分子に限らず、どの理想気体でも成り立つことを、同じ議論で確かめる。"],
                    pc=[("定積", 2), ("定圧", 4), ("理由", 2)], pit=["定圧でも仕事を 0 とする。"],
                    chk=("Rational(3,2)+1", "Rational(5,2)", None, "intermediate"))
    if kind == "work":
        return desc("断面積 $S$ のシリンダーに、なめらかに動くピストンで気体を閉じこめた。気体の圧力 $p$ を一定に保ったままピストンが $\\Delta x$ だけ外側に動いたとき、気体がピストンにした仕事が $W'=p\\Delta V$ と表せることを示しなさい。また、圧力が変化する場合に、気体のした仕事が $p$−$V$ グラフの面積で表される理由を説明しなさい。",
                    "気体がピストンを押す力は $F=pS$ で、ピストンは力の向きに $\\Delta x$ 動くので、仕事は $W'=F\\Delta x=pS\\Delta x=p\\Delta V$（$\\Delta V=S\\Delta x$）。圧力が変化する場合は、体積変化を細かく区切ると各区間では圧力がほぼ一定とみなせ、各区間の仕事 $p\\Delta V$ は $p$−$V$ グラフの細い長方形の面積になる。それらを足し合わせると、グラフと $V$ 軸で囲まれた部分の面積になる。",
                    "仕事＝力×移動距離。力は圧力×面積。",
                    [("$F=pS$ と $W'=F\\Delta x$ から $p\\Delta V$ を導いている", 4), ("細かく区切って長方形の面積の和になることを説明している", 4)], d=3, p=8, lines=8, ps=["cross_unit"], rel=["HS-PHYB-U02"],
                    ap="物理基礎の「仕事＝力×距離」を、気体がピストンを押す場面に当てはめる。",
                    steps=["$F=pS$。", "$W'=pS\\Delta x=p\\Delta V$。", "区分けして面積の和。"],
                    alt=["$v$−$t$ グラフの面積が変位を表すことと同じ考え方（細かく分けて足し合わせる）であることを指摘してもよい。"],
                    pc=[("式の導出", 4), ("面積の説明", 4)], pit=["$W'=pV$（体積そのもの）と書く。"],
                    chk=("p*s*x", "p*(s*x)", "expand", "intermediate"))
    if kind == "adia":
        return desc("自転車の空気入れでタイヤに空気をすばやく押しこむと、空気入れの筒が熱くなる。この現象を、（1）熱力学第一法則を用いて、（2）気体分子の運動の立場から、それぞれ説明しなさい。",
                    "（1）すばやく押しこむので、熱が周囲に逃げる時間がなく断熱変化とみなせる（$Q=0$）。気体は外部から仕事 $W>0$ をされるので、$\\Delta U=Q+W=W>0$ となり内部エネルギーが増加し、温度が上がる。（2）気体分子が、内側に動いてくるピストンに衝突してはね返ると、はね返った後の速さは衝突前より大きくなる（動く壁から運動エネルギーを受け取る）。多くの分子の運動エネルギーが増すので、平均運動エネルギーに比例する絶対温度が上がる。",
                    "断熱圧縮：$Q=0$、$W>0$ → $\\Delta U>0$。",
                    [("（1）断熱変化とみなせる理由と $Q=0$ を述べている", 2), ("（1）第一法則から内部エネルギーの増加を導いている", 3), ("（2）動くピストンとの衝突で分子の速さが増すことを述べ、温度と結びつけている", 3)], d=4, p=8, lines=9,
                    ap="すばやい変化は熱が逃げる時間がない → 断熱。分子の立場では、近づいてくる壁ではね返ると速くなる。",
                    steps=["$Q=0$。", "$\\Delta U=W>0$ → 温度上昇。", "動く壁との衝突で分子が加速 → 平均運動エネルギー増。"],
                    alt=["逆に、スプレー缶から気体を勢いよく出すと缶が冷えるのは断熱膨張（$W<0$）である、と対比して説明してもよい。"],
                    pc=[("（1）断熱", 2), ("（1）第一法則", 3), ("（2）分子", 3)], pit=["「摩擦で熱くなる」とだけ書き、気体への仕事を説明しない。"])
    if kind == "temp":
        return desc("気体分子運動論で得られる $pV=\\dfrac13Nm\\overline{v^2}$ と、状態方程式 $pV=nRT$ を比べて、分子1個あたりの平均運動エネルギーが $\\dfrac32k_{\\mathrm{B}}T$（$k_{\\mathrm{B}}=\\dfrac{R}{N_{\\mathrm{A}}}$）となることを示しなさい。また、この結果から「絶対温度」が何を表す量だと解釈できるか述べなさい。",
                    "$\\dfrac13Nm\\overline{v^2}=nRT$。$N=nN_{\\mathrm{A}}$ を代入すると $\\dfrac13nN_{\\mathrm{A}}m\\overline{v^2}=nRT$、$m\\overline{v^2}=\\dfrac{3R}{N_{\\mathrm{A}}}T=3k_{\\mathrm{B}}T$。よって $\\dfrac12m\\overline{v^2}=\\dfrac32k_{\\mathrm{B}}T$。絶対温度は、気体分子の熱運動の平均運動エネルギーに比例する量、すなわち分子の運動の激しさを表す量だと解釈できる。",
                    "2つの式の $pV$ を等しいとおき、$N=nN_{\\mathrm{A}}$ を使う。",
                    [("2式を等しいとおき $N=nN_{\\mathrm{A}}$ を代入している", 3), ("$\\dfrac12m\\overline{v^2}=\\dfrac32k_{\\mathrm{B}}T$ を導いている", 3), ("温度の意味を分子の運動と結びつけて述べている", 2)], d=3, p=8, kind="proof", lines=8,
                    ap="ミクロ（分子運動論）とマクロ（状態方程式）の2つの $pV$ を等しいとおく。",
                    steps=["$\\dfrac13Nm\\overline{v^2}=nRT$。", "$N=nN_{\\mathrm{A}}$。", "$\\dfrac12m\\overline{v^2}=\\dfrac32k_{\\mathrm{B}}T$。"],
                    alt=["1 mol あたりで考えると $\\dfrac12M\\overline{v^2}=\\dfrac32RT$（$M=N_{\\mathrm{A}}m$）となり、二乗平均速度 $\\sqrt{\\dfrac{3RT}{M}}$ も同時に得られる。"],
                    pc=[("比較", 3), ("導出", 3), ("解釈", 2)], pit=["$N$ と $n$ を混同する。"],
                    chk=("simplify(3*n*r*t/(n*a)/2)", "Rational(3,2)*r*t/a", None, "intermediate"))
    return desc("理想気体を温度一定に保ったままゆっくり膨張させた。（1）この変化で内部エネルギーが変化しない理由を述べなさい。（2）気体が外部に仕事をしているのに温度が下がらない理由を、熱力学第一法則を用いて説明しなさい。（3）同じ体積まで断熱膨張させた場合と比べて、変化後の圧力はどちらが大きいか、理由とともに答えなさい。",
                "（1）理想気体の内部エネルギーは分子の運動エネルギーの総和で、絶対温度だけで決まる（単原子分子なら $\\dfrac32nRT$）。温度一定なので $\\Delta U=0$。（2）第一法則 $\\Delta U=Q+W$ で $\\Delta U=0$、外部に仕事をしたので $W<0$、よって $Q=-W>0$。外部にした仕事と同じだけの熱を外部から吸収しているので、温度が下がらない。（3）断熱膨張では $Q=0$ で $\\Delta U=W<0$ となり温度が下がる。同じ体積なら $p=\\dfrac{nRT}{V}$ で温度が高いほど圧力が大きいので、等温膨張のほうが変化後の圧力は大きい。",
                "等温：$\\Delta U=0$ → $Q=W'$。断熱：$Q=0$ → 温度低下。",
                [("（1）内部エネルギーが温度だけで決まることを述べている", 2), ("（2）$Q=W'$ を第一法則から導いている", 3), ("（3）断熱膨張で温度が下がることと状態方程式から正しく比較している", 3)], d=4, p=8, lines=10, ps=["multiple_solutions"],
                ap="等温と断熱の違いは、熱の出入りがあるかどうか。第一法則で $Q$ と $\\Delta U$ を比べる。",
                steps=["（1）$U$ は $T$ だけで決まる。", "（2）$Q=W'$。", "（3）断熱は温度低下 → 同じ $V$ で圧力が小さい。"],
                alt=["（3）は $p$−$V$ グラフで、断熱線のほうが等温線より急に下がることを図示して説明してもよい。"],
                pc=[("（1）", 2), ("（2）", 3), ("（3）", 3)], pit=["等温変化では熱の出入りがないと考える。"])


@gen("thinking_writing", 3, ["computation", "written_reasoning", "multiple_solutions"])
def cycle_c(r):
    p1, p2, V1, V2 = r.choice([(1, 3, 1, 5), (1, 2, 1, 4), (2, 4, 1, 3), (1, 3, 2, 6), (1, 4, 1, 3), (2, 3, 1, 5)])
    W = (p2 - p1) * (V2 - V1) * 100
    Qab = sp.Rational(3, 2) * V1 * (p2 - p1) * 100
    Qbc = sp.Rational(5, 2) * p2 * (V2 - V1) * 100
    Qcd = -sp.Rational(3, 2) * V2 * (p2 - p1) * 100
    Qda = -sp.Rational(5, 2) * p1 * (V2 - V1) * 100
    e = W / (Qab + Qbc)
    pts = [(V1, p1), (V1, p2), (V2, p2), (V2, p1)]
    fig = figure(f"p−V グラフ上の長方形サイクル。A({V1},{p1})→B({V1},{p2})→C({V2},{p2})→D({V2},{p1})→A。目盛りは p が 10⁵ Pa、V が 10⁻³ m³", pv_svg(pts, closed=True))
    return desc(f"一定量の{MONO}を、図のように A→B→C→D→A の順に変化させた。A の圧力は ${p1}.0\\times10^5\\,\\mathrm{{Pa}}$、体積は ${V1}.0\\times10^{{-3}}\\,\\mathrm{{m^3}}$、B の圧力は ${p2}.0\\times10^5\\,\\mathrm{{Pa}}$、C の体積は ${V2}.0\\times10^{{-3}}\\,\\mathrm{{m^3}}$ である。"
                "（1）図のサイクル1回で気体が外部にした正味の仕事を求めなさい。（2）図の各過程 A→B、B→C、C→D、D→A で気体が吸収した熱量を求めなさい（放出は負）。（3）このサイクルの熱効率を求め、計算で熱効率の分母に何を用いたか、その理由とともに述べなさい。",
                f"（1）${W}\\,\\mathrm{{J}}$　（2）A→B：${t(Qab)}\\,\\mathrm{{J}}$、B→C：${t(Qbc)}\\,\\mathrm{{J}}$、C→D：${t(Qcd)}\\,\\mathrm{{J}}$、D→A：${t(Qda)}\\,\\mathrm{{J}}$　（3）$e=\\dfrac{{{W}}}{{{t(Qab + Qbc)}}}\\fallingdotseq{t(e, 2)}$。分母は熱を吸収する過程（A→B と B→C）の熱量の和 $Q_{{\\text{{in}}}}$。熱効率は「高温の熱源から受け取った熱のうち仕事に変わった割合」なので、放出する過程の熱は含めない。",
                "各過程の $\\Delta U=\\dfrac32\\Delta(pV)$、$W'$＝グラフの下の面積、$Q=\\Delta U+W'$。",
                [("（1）長方形の面積から正味の仕事を求めている", 2), ("（2）各過程の熱量を第一法則から求めている", 3), ("（3）吸収した熱だけを分母にして熱効率を求め、理由を述べている", 3)], d=5, p=8, lines=12, fig=fig,
                ap="単原子分子では $\\Delta U=\\dfrac32nR\\Delta T=\\dfrac32\\Delta(pV)$。温度を求めなくても、$pV$ の変化から熱量を計算できる。",
                steps=[f"（1）$W'=({p2}-{p1})\\times10^5\\times({V2}-{V1})\\times10^{{-3}}={W}\\,\\mathrm{{J}}$。",
                       f"（2）A→B（定積）：$Q=\\dfrac32V_1\\Delta p={t(Qab)}\\,\\mathrm{{J}}$。B→C（定圧）：$Q=\\dfrac52p_2\\Delta V={t(Qbc)}\\,\\mathrm{{J}}$。C→D・D→A は同様に負。",
                       f"（3）$Q_{{\\text{{in}}}}={t(Qab + Qbc)}\\,\\mathrm{{J}}$、$e=\\dfrac{{{W}}}{{{t(Qab + Qbc)}}}\\fallingdotseq{t(e, 2)}$。"],
                alt=["（2）の4つの熱量の和が（1）の正味の仕事に等しい（1サイクルで $\\Delta U=0$）ことで検算できる。",
                     "各状態の温度を $T=\\dfrac{pV}{nR}$ で表してから、モル比熱を使って熱量を求める方法でもよい。"],
                pc=[("（1）", 2), ("（2）", 3), ("（3）", 3)], pit=["分母に4つの熱量の和（＝正味の仕事）を用いて $e=1$ とする。", "放出する熱を含めて分母を小さくする。"],
                chk=(f"({Qab}+{Qbc}+({Qcd})+({Qda}))", str(W), None, "intermediate"))


@gen("thinking_writing", 2, ["cross_unit", "condition_check", "written_reasoning"], rel=["HS-PHYB-U01"])
def piston_c(r):
    Mk = r.choice([2, 4, 5, 10])
    Sc = r.choice([20, 40, 50, 100])
    S = sp.Rational(Sc, 10000)
    p0 = 10 ** 5
    dhc = r.choice([2, 4, 5, 10])
    dh = sp.Rational(dhc, 100)
    p = p0 + Mk * G / S
    W = p * S * dh
    Qv = sp.Rational(5, 2) * W
    dU = sp.Rational(3, 2) * W
    return desc(f"図のように、断面積 {Sc} cm² の鉛直なシリンダーに、質量 {Mk}.0 kg のなめらかに動くピストンで{MONO}を閉じこめた。大気圧を $1.0\\times10^5\\,\\mathrm{{Pa}}$、" + "重力加速度の大きさを $9.8\\,\\mathrm{m/s^2}$ とする。"
                + f"図の気体をゆっくり加熱したところ、ピストンは {dhc}.0 cm 上昇した。（1）気体の圧力を、ピストンにはたらく力のつり合いから求めなさい。（2）気体が外部にした仕事を求めなさい。（3）気体が吸収した熱量と内部エネルギーの増加を求め、吸収した熱量が仕事より大きくなる理由を述べなさい。数値は有効数字2桁で答えなさい。",
                f"（1）$p=p_0+\\dfrac{{Mg}}{{S}}\\fallingdotseq{t(p, 2)}\\,\\mathrm{{Pa}}$　（2）$W'=pS\\Delta h\\fallingdotseq{t(W, 2)}\\,\\mathrm{{J}}$　（3）$Q=\\dfrac52W'\\fallingdotseq{t(Qv, 2)}\\,\\mathrm{{J}}$、$\\Delta U=\\dfrac32W'\\fallingdotseq{t(dU, 2)}\\,\\mathrm{{J}}$。吸収した熱の一部はピストンを押し上げる仕事に、残りは内部エネルギーの増加（温度上昇）に使われるので、$Q=\\Delta U+W'>W'$ となる。",
                "ピストンのつり合いで圧力、定圧変化として仕事と熱量。",
                [("（1）ピストンにはたらく力（大気・重力・気体）のつり合いを立てている", 2), ("（2）$W'=p\\Delta V$ を単位をそろえて求めている", 2), ("（3）$Q=\\dfrac52W'$、$\\Delta U=\\dfrac32W'$ を導いている", 2), ("（3）$Q>W'$ の理由を第一法則で述べている", 2)], d=4, p=8, lines=10,
                fig=figure("鉛直なシリンダーに閉じこめた気体。ピストンの上は大気圧 p₀。下から加熱する", cylinder_svg()),
                ap="ゆっくり加熱するのでピストンはつねにつり合い → 気体の圧力は一定（定圧変化）。",
                steps=[f"（1）$pS=p_0S+Mg$ より $p=1.0\\times10^5+\\dfrac{{{Mk}\\times9.8}}{{{dec(S)}}}\\fallingdotseq{t(p, 3)}\\,\\mathrm{{Pa}}$。",
                       f"（2）$\\Delta V=S\\Delta h={dec(S)}\\times{dec(dh)}\\,\\mathrm{{m^3}}$、$W'=p\\Delta V\\fallingdotseq{t(W, 3)}\\,\\mathrm{{J}}$。",
                       "（3）定圧なので $W'=nR\\Delta T$、$\\Delta U=\\dfrac32nR\\Delta T=\\dfrac32W'$、$Q=\\Delta U+W'=\\dfrac52W'$。"],
                alt=["（2）は、ピストンの位置エネルギーの増加 $Mg\\Delta h$ と大気を押しのける仕事 $p_0S\\Delta h$ の和として求めても同じ値になる。"],
                pc=[("（1）", 2), ("（2）", 2), ("（3）値", 2), ("（3）理由", 2)], pit=["気体の圧力を大気圧と同じとする（ピストンの重さを忘れる）。", "cm² を m² に直し忘れる。"],
                chk=(f"(10**5+{Mk}*Rational(98,10)/{P(S)})*{P(S)}*{P(dh)}", str(sp.nsimplify(W)), None, "intermediate"))


@gen("thinking_writing", 2, ["condition_check", "written_reasoning", "concept"])
def free_exp_c(r):
    V1, V2 = r.choice([(1, 1), (1, 2), (2, 1), (1, 3), (2, 3)])
    T = r.choice([300, 400, 250])
    p1 = r.choice(["1.2", "2.4", "3.6", "1.8"])
    p2 = Q(p1) * sp.Rational(V1, V1 + V2)
    return desc(f"断熱材でできた容器が仕切りで2つの部屋 A（容積 {V1}.0 L）、B（容積 {V2}.0 L）に分けられ、A には温度 {T} K、圧力 ${p1}\\times10^5\\,\\mathrm{{Pa}}$ の理想気体が入り、B は真空である。仕切りを急にとり除いたところ、気体は容器全体に広がった。"
                "（1）この変化で気体が吸収した熱 $Q$ と、気体がされた仕事 $W$ はそれぞれいくらか。理由とともに答えなさい。（2）変化後の気体の温度と圧力を求めなさい。（3）この変化を逆向きに（気体が自然に A だけに集まるように）起こすことができるかどうか、理由とともに述べなさい。",
                f"（1）$Q=0$（断熱容器なので熱の出入りがない）。$W=0$（真空中への膨張では気体が押しのける相手がなく、仕事をしない）。（2）$\\Delta U=Q+W=0$ で、理想気体の内部エネルギーは温度だけで決まるので温度は {T} K のまま。ボイルの法則より $p={p1}\\times10^5\\times\\dfrac{{{V1}}}{{{V1 + V2}}}={t(p2)}\\times10^5\\,\\mathrm{{Pa}}$。（3）起こらない。真空への自由膨張は不可逆変化であり、外部から仕事をしたり熱を移動させたりしない限り、気体が自然に一方の部屋に集まることはない（熱力学第二法則）。",
                "自由膨張：$Q=0$、$W=0$ → $\\Delta U=0$ → 温度不変。",
                [("（1）$Q=0$、$W=0$ をそれぞれ理由とともに述べている", 3), ("（2）温度不変とボイルの法則から圧力を求めている", 3), ("（3）不可逆変化であることを述べている", 2)], d=4, p=8, lines=10,
                ap="ピストンを押すときのように「押しのける相手」があるときに気体は仕事をする。真空には押しのける相手がない。",
                steps=["（1）断熱 → $Q=0$。真空 → $W=0$。", "（2）$\\Delta U=0$ → $T$ 一定 → $p_1V_1=p_2(V_1+V_2)$。", "（3）自然には逆向きに進まない。"],
                alt=["（2）は状態方程式 $pV=nRT$ で $n,\\ T$ が一定なので $p\\propto\\dfrac1V$ と考えても同じ。",
                     "分子の立場：分子は真空側へ飛んでいくだけで、壁にぶつかって速さを変える機会がないので、平均運動エネルギー（温度）は変わらない。"],
                pc=[("（1）", 3), ("（2）", 3), ("（3）", 2)], pit=["「膨張したので仕事をした」と考えて温度が下がるとする（断熱膨張と混同）。"],
                chk=(f"{P(Q(p1))}*Rational({V1},{V1 + V2})", str(p2), None, "intermediate"))


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(stem, wrong, step, etype, tempt, fix, ans, expl, steps, ap, alt, pit, chk=None, d=3, **kw):
    return desc(f"{stem}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい答えを求めなさい。", ans, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい解答を途中式とともに示している", 3), ("最終的な答えが正しい", 1)], d=d, p=6, lines=6,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい途中式", 3), ("正しい答え", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix), chk=chk, **kw)


@gen("error_correction", 3, ["common_error", "condition_check"])
def err_units(r):
    kind = r.choice(["celsius", "liter", "kpa"])
    if kind == "celsius":
        (c1, T1), (c2, T2) = r.sample([(27, 300), (127, 400), (77, 350), (227, 500), (327, 600), (177, 450)], 2)
        V1 = r.choice(["2.0", "3.0", "4.0", "6.0"])
        V2 = Q(V1) * sp.Rational(T2, T1)
        bad = Q(V1) * sp.Rational(c2, c1)
        return err_item(f"圧力一定のもとで、${ctx(c1)}$ で体積 {V1} L の気体を ${ctx(c2)}$ にした。体積を求めなさい。",
                        f"体積は温度に比例するので $V={V1}\\times\\dfrac{{{c2}}}{{{c1}}}\\fallingdotseq{t(bad)}\\,\\mathrm{{L}}$",
                        "セルシウス温度の比をとった部分", "unit",
                        "「体積は温度に比例する」という言葉だけを覚え、比例するのが絶対温度であることを忘れている。",
                        f"$T_1={T1}\\,\\mathrm{{K}}$、$T_2={T2}\\,\\mathrm{{K}}$。$V={V1}\\times\\dfrac{{{T2}}}{{{T1}}}={t(V2)}\\,\\mathrm{{L}}$",
                        f"${t(V2)}\\,\\mathrm{{L}}$", "シャルルの法則の温度は絶対温度。",
                        [f"$T_1={c1}+273={T1}\\,\\mathrm{{K}}$、$T_2={c2}+273={T2}\\,\\mathrm{{K}}$。", f"$V={V1}\\times\\dfrac{{{T2}}}{{{T1}}}={t(V2)}\\,\\mathrm{{L}}$。"],
                        "極端な場合で確かめる：$0\\,{}^\\circ\\mathrm{C}$ から始めると、℃ の比では体積が無限大になってしまい不合理。",
                        ["状態方程式 $V=\\dfrac{nRT}{p}$ に戻って考えれば、$T$ が絶対温度であることが明らか。"], ["温度は最初に K に直す習慣をつける。"],
                        chk=(f"{P(Q(V1))}*Rational({T2},{T1})", str(V2), None, "intermediate"), d=2)
    if kind == "liter":
        n, T, V = r.choice([("1.0", 300, "24.9"), ("2.0", 400, "16.6"), ("0.50", 300, "8.31"), ("1.0", 250, "10.0")])
        p = Q(n) * R * T / (Q(V) / 1000)
        bad = Q(n) * R * T / Q(V)
        return err_item(f"{n} mol の理想気体が、温度 {T} K で体積 {V} L の容器に入っている。圧力を求めなさい。" + RS,
                        f"$p=\\dfrac{{nRT}}{{V}}=\\dfrac{{{n}\\times8.31\\times{T}}}{{{V}}}\\fallingdotseq{t(bad)}\\,\\mathrm{{Pa}}$",
                        "体積を L のまま代入した部分", "unit",
                        "$R=8.31\\,\\mathrm{J/(mol\\cdot K)}$ が SI 単位（Pa・m³）を前提にしていることを意識していない。",
                        f"$V={V}\\times10^{{-3}}\\,\\mathrm{{m^3}}$。$p=\\dfrac{{{n}\\times8.31\\times{T}}}{{{V}\\times10^{{-3}}}}\\fallingdotseq{t(p)}\\,\\mathrm{{Pa}}$",
                        f"${t(p)}\\,\\mathrm{{Pa}}$", "$R=8.31$ を使うときは、Pa・m³・K・mol の SI 単位で代入する。",
                        [f"$V={V}\\,\\mathrm{{L}}={V}\\times10^{{-3}}\\,\\mathrm{{m^3}}$。", f"$p=\\dfrac{{nRT}}{{V}}\\fallingdotseq{t(p)}\\,\\mathrm{{Pa}}$。"],
                        "単位で確かめる：$\\mathrm{J}=\\mathrm{Pa\\cdot m^3}$ なので、$\\dfrac{\\mathrm{J}}{\\mathrm{L}}$ は Pa にならない。",
                        ["大気圧（約 $1\\times10^5\\,\\mathrm{Pa}$）と比べて、答えの桁が現実的かどうかを確かめる。"], ["代入前に単位を SI にそろえる。"],
                        chk=(f"{P(Q(n))}*Rational(831,100)*{T}/({P(Q(V))}*10**(-3))", str(p), None, "intermediate"), d=2)
    pk, V, T = r.choice([("100", "8.31", 300), ("200", "4.155", 250), ("150", "16.6", 400), ("300", "8.31", 600)])
    n = Q(pk) * 1000 * Q(V) / 1000 / (R * T)
    bad = Q(pk) * Q(V) / 1000 / (R * T)
    return err_item(f"圧力 {pk} kPa、温度 {T} K、体積 {V} L の理想気体の物質量を求めなさい。" + RS,
                    f"$n=\\dfrac{{pV}}{{RT}}=\\dfrac{{{pk}\\times{V}\\times10^{{-3}}}}{{8.31\\times{T}}}\\fallingdotseq{t(bad)}\\,\\mathrm{{mol}}$",
                    "圧力を kPa のまま代入した部分", "unit",
                    "体積は m³ に直したが、圧力の接頭語 k（$10^3$）を見落としている。",
                    f"$p={pk}\\times10^3\\,\\mathrm{{Pa}}$。$n=\\dfrac{{{pk}\\times10^3\\times{V}\\times10^{{-3}}}}{{8.31\\times{T}}}\\fallingdotseq{t(n)}\\,\\mathrm{{mol}}$",
                    f"${t(n)}\\,\\mathrm{{mol}}$", "$1\\,\\mathrm{kPa}=10^3\\,\\mathrm{Pa}$。",
                    [f"$p={pk}\\times10^3\\,\\mathrm{{Pa}}$、$V={V}\\times10^{{-3}}\\,\\mathrm{{m^3}}$。", f"$n\\fallingdotseq{t(n)}\\,\\mathrm{{mol}}$。"],
                    "すべての量の単位を書き出してから代入する。",
                    ["kPa と L の組み合わせでは $10^3\\times10^{-3}=1$ となるので、$pV$ の数値はそのまま J になる、と覚えておくと速い。"], ["接頭語（k、m など）を見落とさない。"],
                    chk=(f"{P(Q(pk))}*10**3*{P(Q(V))}*10**(-3)/(Rational(831,100)*{T})", str(n), None, "intermediate"), d=2)


@gen("error_correction", 3, ["common_error", "concept"])
def err_first(r):
    kind = r.choice(["sign", "cp", "isoT"])
    if kind == "sign":
        Qv, Wd = r.choice([(800, 300), (1200, 500), (600, 250), (1000, 400)])
        return err_item(f"気体に {Qv} J の熱を加えたところ、気体は膨張して外部に {Wd} J の仕事をした。内部エネルギーの変化を求めなさい。",
                        f"$\\Delta U=Q+W={Qv}+{Wd}={Qv + Wd}\\,\\mathrm{{J}}$", "外部にした仕事を $W$ として足した部分", "sign",
                        "$\\Delta U=Q+W$ の $W$ が「された仕事」であることを確認せず、問題文の「仕事」の数値をそのまま入れている。",
                        f"外部に仕事をしたので、された仕事は $W=-{Wd}\\,\\mathrm{{J}}$。$\\Delta U={Qv}+(-{Wd})={Qv - Wd}\\,\\mathrm{{J}}$",
                        f"${Qv - Wd}\\,\\mathrm{{J}}$（増加）", "気体に入るエネルギーを正、出ていくエネルギーを負とする。",
                        [f"$Q=+{Qv}\\,\\mathrm{{J}}$、$W=-{Wd}\\,\\mathrm{{J}}$。", f"$\\Delta U={Qv - Wd}\\,\\mathrm{{J}}$。"],
                        "エネルギーの出入りを矢印で図にかき、入るものと出るものを区別する。",
                        ["加えた熱が仕事として外に出ていくのだから、内部エネルギーの増加は加えた熱より小さいはず、と大小で確かめる。"], ["$W$ と $W'$ の定義を書いてから代入する。"],
                        chk=(f"{Qv}-{Wd}", str(Qv - Wd), None, "intermediate"), d=2)
    if kind == "cp":
        n, dT = r.choice([("1.0", 20), ("2.0", 10), ("0.50", 40), ("1.0", 50), ("2.0", 30)])
        Qv = sp.Rational(5, 2) * Q(n) * R * dT
        bad = sp.Rational(3, 2) * Q(n) * R * dT
        return err_item(f"{n} mol の{MONO}を、圧力を一定に保って加熱し、温度を {dT} K 上げた。吸収した熱量を求めなさい。" + RS,
                        f"$Q=\\dfrac32nR\\Delta T=\\dfrac32\\times{n}\\times8.31\\times{dT}\\fallingdotseq{t(bad)}\\,\\mathrm{{J}}$",
                        "定圧変化の熱量を $\\dfrac32nR\\Delta T$ とした部分", "condition",
                        "$\\Delta U=\\dfrac32nR\\Delta T$ と吸収した熱量を混同し、定圧では膨張による仕事の分も熱が必要であることを考えていない。",
                        f"定圧では $W'=nR\\Delta T$ も必要。$Q=\\Delta U+W'=\\dfrac52nR\\Delta T\\fallingdotseq{t(Qv)}\\,\\mathrm{{J}}$",
                        f"${t(Qv)}\\,\\mathrm{{J}}$", "$\\dfrac32nR\\Delta T$ は内部エネルギーの変化。定圧の熱量は $\\dfrac52nR\\Delta T$。",
                        [f"$\\Delta U=\\dfrac32nR\\Delta T$、$W'=nR\\Delta T$。", f"$Q=\\dfrac52\\times{n}\\times8.31\\times{dT}\\fallingdotseq{t(Qv)}\\,\\mathrm{{J}}$。"],
                        "変化の種類（定積・定圧・等温・断熱）を確認してから、$Q$・$W'$・$\\Delta U$ を表にまとめる。",
                        ["生徒の値は定積変化の熱量であり、定圧ではピストンを押し上げる分だけ多く必要になる、と比較して確かめる。"], ["$\\Delta U$ と $Q$ を区別する。"],
                        chk=(f"Rational(5,2)*{P(Q(n))}*Rational(831,100)*{dT}", str(Qv), None, "intermediate"))
    Wd = r.choice([200, 350, 500, 640])
    return err_item(f"理想気体を等温で膨張させたところ、気体は外部に {Wd} J の仕事をした。気体が吸収した熱量と、内部エネルギーの変化を求めなさい。",
                    f"温度が一定なので熱の出入りはなく $Q=0$。$\\Delta U=Q+W=0-{Wd}=-{Wd}\\,\\mathrm{{J}}$",
                    "「温度一定なので $Q=0$」とした部分", "concept",
                    "「温度が変わらない＝熱が出入りしない」と、温度と熱を混同している（熱の出入りがないのは断熱変化）。",
                    f"理想気体の内部エネルギーは温度だけで決まるので、等温では $\\Delta U=0$。$0=Q-{Wd}$ より $Q={Wd}\\,\\mathrm{{J}}$",
                    f"$Q={Wd}\\,\\mathrm{{J}}$、$\\Delta U=0$", "等温変化：$\\Delta U=0$、$Q=W'$。断熱変化：$Q=0$。",
                    ["等温 → $\\Delta U=0$。", f"$Q=W'={Wd}\\,\\mathrm{{J}}$。"],
                    "「温度」は状態を表す量、「熱」は移動するエネルギー、と区別する。",
                    [f"生徒の答えでは $\\Delta U<0$ となり温度が下がるはずで、「等温」という条件と矛盾する。"], ["等温と断熱を混同しない。"],
                    chk=(f"0+{Wd}", str(Wd), None, "intermediate"), d=2)


@gen("error_correction", 2, ["common_error", "computation"])
def err_kinetic(r):
    kind = r.choice(["sqrtT", "gram"])
    if kind == "sqrtT":
        T1, T2 = r.choice([(300, 1200), (200, 800), (250, 1000), (100, 900), (300, 2700)])
        v1 = r.choice([400, 500, 600, 1200])
        v2 = v1 * sp.sqrt(sp.Rational(T2, T1))
        return err_item(f"ある気体の分子の二乗平均速度は、{T1} K で {v1} m/s である。{T2} K での二乗平均速度を求めなさい。",
                        f"速さは絶対温度に比例するので ${v1}\\times\\dfrac{{{T2}}}{{{T1}}}={v1 * T2 // T1}\\,\\mathrm{{m/s}}$",
                        "速さが絶対温度に比例するとした部分", "formula",
                        "「温度は分子の運動の激しさを表す」ことを、速さに比例すると取り違えている。比例するのは運動エネルギー（速さの2乗）。",
                        f"$\\sqrt{{\\overline{{v^2}}}}\\propto\\sqrt{{T}}$ より ${v1}\\times\\sqrt{{\\dfrac{{{T2}}}{{{T1}}}}}={t(v2)}\\,\\mathrm{{m/s}}$",
                        f"${t(v2)}\\,\\mathrm{{m/s}}$", "$\\dfrac12m\\overline{v^2}=\\dfrac32k_{\\mathrm{B}}T$ より、速さは温度の平方根に比例。",
                        [f"温度は $\\dfrac{{{T2}}}{{{T1}}}={T2 // T1}$ 倍。", f"速さは $\\sqrt{{{T2 // T1}}}={sp.sqrt(T2 // T1)}$ 倍で ${t(v2)}\\,\\mathrm{{m/s}}$。"],
                        "比例関係の式（$\\overline{v^2}\\propto T$）を書いてから倍率を求める。",
                        ["$\\sqrt{\\dfrac{3RT}{M}}$ に $T$ を入れて、温度の比の平方根が出てくることを確かめる。"], ["運動エネルギーと速さを区別する。"],
                        chk=(f"{v1}*sqrt(Rational({T2},{T1}))", str(v2), None, "intermediate"), d=2)
    name, Mtx, M = r.choice(GASES)
    Mg = M * 1000
    T = r.choice([300, 400, 600])
    v = sp.sqrt(3 * R * T / M)
    bad = sp.sqrt(3 * R * T / Mg)
    return err_item(f"温度 {T} K の{name}分子の二乗平均速度を求めなさい。{name}のモル質量は {dec(Mg)} g/mol、" + RS,
                    f"$\\sqrt{{\\dfrac{{3RT}}{{M}}}}=\\sqrt{{\\dfrac{{3\\times8.31\\times{T}}}{{{dec(Mg)}}}}}\\fallingdotseq{t(bad, 2)}\\,\\mathrm{{m/s}}$",
                    "モル質量を g/mol のまま代入した部分", "unit",
                    "化学で使い慣れた g/mol の数値をそのまま使い、$R$ が SI 単位（kg）を前提にしていることを忘れている。",
                    f"$M={Mtx}\\,\\mathrm{{kg/mol}}$。$\\sqrt{{\\dfrac{{3\\times8.31\\times{T}}}{{{Mtx}}}}}\\fallingdotseq{t(v, 2)}\\,\\mathrm{{m/s}}$",
                    f"${t(v, 2)}\\,\\mathrm{{m/s}}$（有効数字2桁）", "SI 単位ではモル質量は kg/mol。",
                    [f"$M={dec(Mg)}\\,\\mathrm{{g/mol}}={Mtx}\\,\\mathrm{{kg/mol}}$。", f"$\\sqrt{{\\overline{{v^2}}}}\\fallingdotseq{t(v, 2)}\\,\\mathrm{{m/s}}$。"],
                    "単位で確かめる：$\\dfrac{\\mathrm{J/mol}}{\\mathrm{kg/mol}}=\\mathrm{m^2/s^2}$ となるのは kg を使ったときだけ。",
                    ["空気中の分子の速さが音速（約 340 m/s）と同程度〜数倍であることを目安に、答えの桁を確かめる。"], ["g/mol を kg/mol に直す。"],
                    chk=(f"sqrt(3*Rational(831,100)*{T}/{P(M)})", str(v), None, "intermediate"))


@gen("error_correction", 2, ["common_error", "concept"])
def err_graph(r):
    kind = r.choice(["pV", "eff"])
    if kind == "pV":
        p, V1, V2 = r.choice([(2, 1, 4), (3, 2, 5), (1, 2, 6), (4, 1, 3)])
        W = p * (V2 - V1) * 100
        return err_item(f"圧力 ${p}.0\\times10^5\\,\\mathrm{{Pa}}$ を一定に保ったまま、気体の体積を ${V1}.0\\times10^{{-3}}\\,\\mathrm{{m^3}}$ から ${V2}.0\\times10^{{-3}}\\,\\mathrm{{m^3}}$ にした。気体が外部にした仕事を求めなさい。",
                        f"$W'=pV={p}.0\\times10^5\\times{V2}.0\\times10^{{-3}}={p * V2 * 100}\\,\\mathrm{{J}}$",
                        "体積そのもの（変化後の $V$）をかけた部分", "formula",
                        "$W'=p\\Delta V$ の $\\Delta$（変化量）を落とし、状態方程式の $pV$ と混同している。",
                        f"$W'=p\\Delta V={p}.0\\times10^5\\times({V2}-{V1})\\times10^{{-3}}={W}\\,\\mathrm{{J}}$",
                        f"${W}\\,\\mathrm{{J}}$", "仕事は体積の「変化」で決まる。$p$−$V$ グラフの長方形の面積。",
                        [f"$\\Delta V=({V2}-{V1})\\times10^{{-3}}\\,\\mathrm{{m^3}}$。", f"$W'=p\\Delta V={W}\\,\\mathrm{{J}}$。"],
                        "$p$−$V$ グラフをかき、仕事がどの部分の面積かを確認する。",
                        ["体積が変化しなければ仕事は 0 のはず。$pV$ では体積が変わらなくても値が出てしまい不合理。"], ["$\\Delta$ をつけて式を書く。"],
                        chk=(f"{p}*10**5*({V2}-{V1})*10**(-3)", str(W), None, "intermediate"), d=2)
    Qin, Qout = r.choice([(1000, 700), (2000, 1500), (5000, 3000), (800, 600), (2500, 2000)])
    e = sp.Rational(Qin - Qout, Qin)
    return err_item(f"ある熱機関は1サイクルの間に、高温の熱源から {Qin} J の熱を吸収し、低温の熱源へ {Qout} J の熱を放出する。熱効率を求めなさい。",
                    f"$e=\\dfrac{{Q_{{\\text{{out}}}}}}{{Q_{{\\text{{in}}}}}}=\\dfrac{{{Qout}}}{{{Qin}}}={t(sp.Rational(Qout, Qin))}$",
                    "放出した熱を分子にした部分", "formula",
                    "熱効率の定義「仕事に変わった割合」を忘れ、与えられた2つの熱量で比をつくっている。",
                    f"正味の仕事 $W'={Qin}-{Qout}={Qin - Qout}\\,\\mathrm{{J}}$。$e=\\dfrac{{{Qin - Qout}}}{{{Qin}}}={t(e)}$",
                    f"${t(e)}$", "$e=\\dfrac{W'}{Q_{\\text{in}}}=1-\\dfrac{Q_{\\text{out}}}{Q_{\\text{in}}}$。",
                    [f"$W'=Q_{{\\text{{in}}}}-Q_{{\\text{{out}}}}={Qin - Qout}\\,\\mathrm{{J}}$。", f"$e=\\dfrac{{{Qin - Qout}}}{{{Qin}}}={t(e)}$。"],
                    "定義を言葉で書いてから式にする。",
                    ["生徒の答えと正しい答えの和が 1 になることに注目し、生徒は「捨てた熱の割合」を求めていたと確かめる。"], ["熱効率の分子は仕事。"],
                    chk=(f"1-Rational({Qout},{Qin})", str(e), None, "intermediate"), d=2)


GENERATORS = [gas_law_basic, kinetic_basic, internal_basic, first_law_basic, efficiency_basic, concept_mc,
              state_apps, mole_apps, process_heat, pv_graph, kinetic_apps, mix_adiabatic,
              derive_c, cycle_c, piston_c, free_exp_c,
              err_units, err_first, err_kinetic, err_graph]
