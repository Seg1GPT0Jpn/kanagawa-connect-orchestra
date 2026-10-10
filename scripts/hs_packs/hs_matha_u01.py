"""単元パック：数学A 場合の数と確率（順列・組合せ・確率の基本性質・独立試行と反復試行・条件付き確率・期待値）。"""
from fractions import Fraction
from itertools import product
from math import comb, factorial, perm

from banks._common import desc, mc, num, sa, table
from hs_pack_lib import board, check, definition, derivation, example, frac, gen, guide, intro, lesson, summary, theorem, tp

UNIT_ID = "HS-MATHA-U01"


def ftex(f):
    f = Fraction(f)
    return frac(f.numerator, f.denominator)


def fans(f):
    f = Fraction(f)
    return str(f.numerator) if f.denominator == 1 else f"{f.numerator}/{f.denominator}"


def fpy(f):
    f = Fraction(f)
    return str(f.numerator) if f.denominator == 1 else f"Rational({f.numerator},{f.denominator})"


def P_(n, r):
    return f"{{}}_{{{n}}}\\mathrm{{P}}_{{{r}}}"


def C_(n, r):
    return f"{{}}_{{{n}}}\\mathrm{{C}}_{{{r}}}"


PS = [Fraction(1, 2), Fraction(1, 3), Fraction(2, 3), Fraction(1, 4), Fraction(3, 4), Fraction(2, 5), Fraction(3, 5), Fraction(4, 5), Fraction(1, 5)]


LESSON = lesson(
    goals=["順列・組合せの公式を導き、条件のついた並べ方・選び方の総数を、重複や漏れなく数えられる。",
           "確率の基本性質（加法定理・余事象）を用い、独立な試行・反復試行の確率を求められる。",
           "条件付き確率と乗法定理を理解して活用し、期待値を求めて判断の根拠にできる。"],
    duration=100,
    readiness=["樹形図や表を使って、場合の数を数えられる（中学2年）。", "「同様に確からしい」ことを前提に、確率を求められる（中学2年）。", "集合の要素の個数の公式 $n(A\\cup B)=n(A)+n(B)-n(A\\cap B)$ を使える。"],
    flow=[("導入：数え上げの工夫", 5, "樹形図で数えると大変な例を示し、公式化の必要性を感じさせる"),
          ("順列と組合せ", 30, "積の法則から ${}_n\\mathrm{P}_r$、${}_n\\mathrm{C}_r$ を導き、円順列・同じものを含む順列を扱う（例題1）"),
          ("確率の基本性質", 20, "加法定理・余事象の確率"),
          ("独立な試行と反復試行", 15, "反復試行の確率の公式を導く（例題2）"),
          ("条件付き確率", 20, "表と式で条件付き確率を求め、乗法定理を使う（例題3）"),
          ("期待値とまとめ", 10, "期待値の定義と簡単な例、確認問題")],
    sections=[
        intro("in1", "なぜ数え方の公式が必要か",
              "5人を1列に並べる並び方を樹形図ですべて書き出すと $120$ 通りもあり、書き切るのは大変である。しかし、「1番目の選び方が5通り、そのそれぞれに2番目の選び方が4通り……」と考えれば、$5\\times4\\times3\\times2\\times1=120$ と計算で求められる。確率もまた「起こりうる場合の数」を正しく数えることから始まる。",
              bullets=["積の法則：A の起こり方が $m$ 通り、そのそれぞれに B の起こり方が $n$ 通りなら、A と B がともに起こるのは $mn$ 通り。", "確率では、根元事象が「同様に確からしい」ように数えることが大切である。"],
              points=[tp("最初に3人の並び方を樹形図で書かせ、枝の数がかけ算になっていることに気づかせる。", ask="樹形図の枝の数は、どのような計算で求められるか。", expect="$3\\times2\\times1$", timing="導入の冒頭"),
                      tp("「区別するもの・しないもの」「順序を考える・考えない」を問題ごとに必ず確認させる。", caution="区別の有無を確認しないことが、重複・漏れの最大の原因になる。")]),
        definition("df1", "順列と組合せ",
                   "異なる $n$ 個のものから $r$ 個を取り出して1列に並べたものを順列といい、その総数を ${}_n\\mathrm{P}_r$ で表す。順序を考えずに $r$ 個を取り出したものを組合せといい、その総数を ${}_n\\mathrm{C}_r$ で表す。",
                   formula="$${}_n\\mathrm{P}_r=n(n-1)(n-2)\\cdots(n-r+1)=\\dfrac{n!}{(n-r)!},\\qquad {}_n\\mathrm{C}_r=\\dfrac{{}_n\\mathrm{P}_r}{r!}=\\dfrac{n!}{r!(n-r)!}$$",
                   conditions=["$0!=1$、${}_n\\mathrm{C}_0=1$ と定める", "円順列：異なる $n$ 個を円形に並べる並べ方は $(n-1)!$ 通り（回転して一致するものは同じとみなす）",
                               "同じものを含む順列：$p$ 個、$q$ 個、$r$ 個の同じものを含む $n$ 個（$p+q+r=n$）の並べ方は $\\dfrac{n!}{p!q!r!}$ 通り"],
                   points=[tp("「並べる＝P、選ぶだけ＝C」と言葉で区別させる。", ask="5人から委員長と副委員長を選ぶのは P か C か。", expect="役割に区別があるので P。")]),
        derivation("dv1", "${}_n\\mathrm{C}_r=\\dfrac{{}_n\\mathrm{P}_r}{r!}$ の導出",
                   ["異なる $n$ 個から $r$ 個を取り出して並べる方法（${}_n\\mathrm{P}_r$ 通り）を、2段階に分けて数える。",
                    "まず $r$ 個を選ぶ（${}_n\\mathrm{C}_r$ 通り）。次に、選んだ $r$ 個を1列に並べる（$r!$ 通り）。",
                    "積の法則より ${}_n\\mathrm{P}_r={}_n\\mathrm{C}_r\\times r!$。", "よって ${}_n\\mathrm{C}_r=\\dfrac{{}_n\\mathrm{P}_r}{r!}$。"],
                   body="1つの組合せから $r!$ 通りの順列ができるので、順列の総数を $r!$ で割ると組合せの総数になる。同じ考え方で、円順列や同じものを含む順列の公式も「重複して数えた分で割る」と説明できる。",
                   points=[tp("A, B, C から2個選ぶ組合せ3通りそれぞれから2通りの順列ができることを、表にして見せる。")]),
        theorem("th1", "確率の基本性質",
                "$$P(A\\cup B)=P(A)+P(B)-P(A\\cap B),\\qquad P(\\overline{A})=1-P(A)$$",
                ["$A,\\ B$ が排反（同時に起こらない）なら $P(A\\cup B)=P(A)+P(B)$", "「少なくとも1つ」の確率は余事象「1つもない」を使うと求めやすい"],
                proof=["全事象 $U$ の根元事象がすべて同様に確からしいとき、$P(A)=\\dfrac{n(A)}{n(U)}$。",
                       "集合の要素の個数の公式 $n(A\\cup B)=n(A)+n(B)-n(A\\cap B)$ の両辺を $n(U)$ で割ると、加法定理が得られる。",
                       "$A$ と $\\overline{A}$ は排反で、$A\\cup\\overline{A}=U$ なので $P(A)+P(\\overline{A})=1$。"],
                points=[tp("「少なくとも」という言葉が出たら余事象を検討する、という習慣をつけさせる。", timing="余事象の例の後")]),
        theorem("th2", "独立な試行と反復試行の確率",
                "$${}_n\\mathrm{C}_r\\,p^r(1-p)^{n-r}$$",
                ["1回の試行で事象 $A$ の起こる確率を $p$ とし、この試行を独立に $n$ 回くり返すとき、$A$ がちょうど $r$ 回起こる確率", "各回の試行が互いに影響を与えない（独立である）ことが前提"],
                body="独立な試行では、それぞれの事象の確率の積が、それらがともに起こる確率になる。",
                proof=["$n$ 回のうち、$A$ が起こる $r$ 回の位置の選び方は ${}_n\\mathrm{C}_r$ 通りある。",
                       "位置を1つ決めたとき、その起こり方の確率は、独立性より $p^r(1-p)^{n-r}$。",
                       "これらは互いに排反なので、加えて ${}_n\\mathrm{C}_r\\,p^r(1-p)^{n-r}$。"],
                points=[tp("「どの回に起こるか」の選び方 ${}_n\\mathrm{C}_r$ をかけ忘れる誤りを、$n=3,\\ r=1$ の樹形図で確認させる。", caution="$p^r(1-p)^{n-r}$ だけを答える誤りが多い。")]),
        definition("df2", "条件付き確率と期待値",
                   "事象 $A$ が起こったときに事象 $B$ が起こる確率を、$A$ が起こったときの $B$ の条件付き確率といい、$P_A(B)$ で表す。また、変量 $X$ のとる値が $x_1,\\ \\cdots,\\ x_n$、それぞれの値をとる確率が $p_1,\\ \\cdots,\\ p_n$ のとき、$x_1p_1+\\cdots+x_np_n$ を $X$ の期待値という。",
                   formula="$$P_A(B)=\\dfrac{P(A\\cap B)}{P(A)},\\qquad P(A\\cap B)=P(A)P_A(B)\\ (\\text{乗法定理}),\\qquad E=\\sum_{k=1}^{n}x_kp_k$$",
                   conditions=["$P(A)>0$ のときに定義する", "$P_A(B)$ と $P(A\\cap B)$ は異なる（分母が全体か $A$ か）", "期待値は、試行を多数回くり返したときの1回あたりの平均値の目安"],
                   points=[tp("2×2 の表で、$P_A(B)$ は「$A$ の行だけを全体とみなす」ことを色分けして示す。", ask="$P_A(B)$ の分母は何か。", expect="$A$ が起こる場合の数（または $P(A)$）。")]),
        example("ex1", "例題1　条件のついた並べ方",
                "男子4人、女子3人が1列に並ぶとき、女子3人がすべて隣り合う並び方は何通りあるか。",
                ["女子3人をひとまとめにして1人とみなすと、男子4人とあわせて5人の並び方は $5!=120$ 通り。", "そのそれぞれについて、まとめた女子3人の中の並び方が $3!=6$ 通り。", "積の法則より $120\\times6=720$ 通り。"],
                "$720$ 通り",
                thinking="隣り合うものはひとまとめにして考え、最後にまとまりの中の並び方をかける。",
                points=[tp("まとまりの中の並び方 $3!$ をかけ忘れないよう、図で「箱の中も並べる」ことを強調する。")],
                misconceptions=[("$5!=120$ 通り", "まとまりの中の女子の並び方 $3!$ 通りをかける")]),
        example("ex2", "例題2　反復試行の確率",
                "1個のさいころを5回投げるとき、3の倍数の目がちょうど2回出る確率を求めよ。",
                ["1回で3の倍数の目が出る確率は $\\dfrac{2}{6}=\\dfrac{1}{3}$。", "5回のうち2回の位置の選び方は ${}_5\\mathrm{C}_2=10$ 通り。",
                 "求める確率は $10\\times\\left(\\dfrac{1}{3}\\right)^2\\left(\\dfrac{2}{3}\\right)^3=10\\times\\dfrac{1}{9}\\times\\dfrac{8}{27}=\\dfrac{80}{243}$。"],
                "$\\dfrac{80}{243}$",
                thinking="各回は独立で、同じ確率 $\\dfrac{1}{3}$ の試行を5回くり返す反復試行である。",
                points=[tp("$p$ と $1-p$ の指数の和が回数 $n$ になっているかを確かめさせる。")]),
        example("ex3", "例題3　条件付き確率",
                "袋 A には赤球3個と白球2個、袋 B には赤球1個と白球4個が入っている。硬貨を投げて表なら A、裏なら B から球を1個取り出す。取り出した球が赤球であったとき、それが袋 A から取り出された確率を求めよ。",
                ["A から赤球：$\\dfrac{1}{2}\\times\\dfrac{3}{5}=\\dfrac{3}{10}$。B から赤球：$\\dfrac{1}{2}\\times\\dfrac{1}{5}=\\dfrac{1}{10}$。",
                 "赤球を取り出す確率は $\\dfrac{3}{10}+\\dfrac{1}{10}=\\dfrac{2}{5}$。", "求める確率は $\\dfrac{3}{10}\\div\\dfrac{2}{5}=\\dfrac{3}{4}$。"],
                "$\\dfrac{3}{4}$",
                thinking="「赤球であった」という条件のもとでの確率なので、赤球が出るすべての場合を分母にする条件付き確率である。",
                points=[tp("樹形図をかき、赤球に至る2本の枝の確率の比 $3:1$ から答えが読み取れることを示す。")]),
        board("bd1", "板書案",
              [("① 数え方", ["${}_n\\mathrm{P}_r=\\dfrac{n!}{(n-r)!}$　並べる", "${}_n\\mathrm{C}_r=\\dfrac{{}_n\\mathrm{P}_r}{r!}$　選ぶ", "円順列 $(n-1)!$", "隣り合う → ひとまとめ：$5!\\times3!=720$"]),
               ("② 確率の性質", ["$P(A\\cup B)=P(A)+P(B)-P(A\\cap B)$", "$P(\\overline{A})=1-P(A)$", "反復試行 ${}_n\\mathrm{C}_rp^r(1-p)^{n-r}$", "例題2：$\\dfrac{80}{243}$"]),
               ("③ 条件付き確率・期待値", ["$P_A(B)=\\dfrac{P(A\\cap B)}{P(A)}$", "乗法定理 $P(A\\cap B)=P(A)P_A(B)$", "例題3：$\\dfrac{3}{10}\\div\\dfrac{2}{5}=\\dfrac{3}{4}$", "期待値 $E=\\sum x_kp_k$"])],
              points=[tp("③では樹形図を板書の中央に大きくかき、枝に確率を書きこむ。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("確率の問題では、同じ色の球でも「区別して」数えると根元事象が同様に確からしくなることを繰り返し確認する。", caution="区別しないで数えると、確率が正しく求まらない。"),
               tp("「少なくとも1回」の問題で、確率を回数倍する誤り（$n\\times\\dfrac{1}{6}$）を取り上げ、$n=7$ なら確率が1を超えてしまう矛盾を示す。", timing="余事象の後"),
               tp("グループ分けの問題では、組に区別がないとき同じ人数の組の数の階乗で割る理由を、具体例で書き出して確認させる。"),
               tp("条件付き確率では「何が分かったうえでの確率か」を言葉で書かせてから式を立てさせる。", ask="「赤球であったとき」は、何を全体とみなすことを意味するか。", expect="赤球が出る場合全体。"),
               tp("期待値は「平均的にどれくらいか」の目安であり、1回の結果を保証するものではないことを、くじの例で説明する。")],
              misconceptions=[("5人から委員3人を選ぶ方法を ${}_5\\mathrm{P}_3=60$ 通りとする", "役割の区別がないので ${}_5\\mathrm{C}_3=10$ 通り"),
                              ("さいころを3回投げて少なくとも1回6が出る確率を $3\\times\\dfrac{1}{6}=\\dfrac{1}{2}$ とする", "余事象を使い $1-\\left(\\dfrac{5}{6}\\right)^3=\\dfrac{91}{216}$"),
                              ("$P_A(B)$ を $P(A\\cap B)$ と同じものとして計算する", "分母を $P(A)$ にする")]),
        summary("sm1", "まとめ",
                ["並べる → ${}_n\\mathrm{P}_r$、選ぶ → ${}_n\\mathrm{C}_r=\\dfrac{{}_n\\mathrm{P}_r}{r!}$。重複して数えた分は割って調整する。",
                 "「少なくとも」は余事象。独立な試行は確率の積、反復試行は ${}_n\\mathrm{C}_rp^r(1-p)^{n-r}$。",
                 "条件付き確率 $P_A(B)=\\dfrac{P(A\\cap B)}{P(A)}$。期待値は「値×確率」の和。"]),
        check("ck1", "確認問題",
              [("7人から3人を選んで1列に並べる方法は何通りか。", "${}_7\\mathrm{P}_3=210$ 通り"),
               ("硬貨を4回投げて、表がちょうど3回出る確率を求めよ。", "${}_4\\mathrm{C}_3\\left(\\dfrac{1}{2}\\right)^4=\\dfrac{4}{16}=\\dfrac{1}{4}$"),
               ("1等100円が1本、2等50円が2本、はずれが7本のくじを1本引くときの賞金の期待値を求めよ。", "$100\\times\\dfrac{1}{10}+50\\times\\dfrac{2}{10}=20$ 円")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

@gen("basic_check", 5, ["computation", "concept"])
def perm_comb(r):
    kind = r.choice(["P", "C", "circle", "rep"])
    if kind == "P":
        n = r.randint(5, 10)
        k = r.randint(2, min(4, n - 1))
        stem = f"異なる {n} 冊の本から {k} 冊を選び、本棚に左から1列に並べる方法は何通りあるか。"
        val, py, how = perm(n, k), f"perm({n},{k})", f"${P_(n, k)}=" + "\\times".join(str(n - i) for i in range(k)) + f"={perm(n, k)}$"
        ap = "選んだ本を並べるので順序が区別される。異なる $n$ 個から $r$ 個を取る順列 ${}_n\\mathrm{P}_r$。"
    elif kind == "C":
        n = r.randint(5, 12)
        k = r.randint(2, min(5, n - 2))
        stem = f"{n} 人の部員の中から、大会に出場する {k} 人を選ぶ方法は何通りあるか。"
        val, py = comb(n, k), f"comb({n},{k})"
        how = f"${C_(n, k)}=\\dfrac{{{P_(n, k)}}}{{{k}!}}=\\dfrac{{{perm(n, k)}}}{{{factorial(k)}}}={comb(n, k)}$"
        ap = "出場する人を選ぶだけで、選んだ人の間に順序や役割の区別はない。組合せ ${}_n\\mathrm{C}_r$。"
    elif kind == "circle":
        n = r.randint(4, 8)
        stem = f"{n} 人が丸いテーブルのまわりに等間隔に座るとき、座り方は何通りあるか。ただし、回転して一致する座り方は同じとみなす。"
        val, py, how = factorial(n - 1), f"factorial({n - 1})", f"$({n}-1)!={n - 1}!={factorial(n - 1)}$"
        ap = "円順列では回転して同じになるものを区別しないので、1人の位置を固定して残りを並べる。"
    else:
        k, m = r.randint(3, 6), r.randint(2, 5)
        stem = f"1 から {k} までの {k} 種類の数字を、同じ数字をくり返し使ってもよいとして {m} 個並べてできる {m} 桁の数字の列は何通りあるか。"
        val, py, how = k ** m, f"{k}**{m}", f"${k}^{m}={k ** m}$"
        ap = "各桁に同じ数字を何度使ってもよいので、どの桁も選び方が同じ数ある（重複順列）。"
    return num(stem, str(val), how + "。", d=1 if kind != "circle" else 2,
               ap=ap, steps=["順序の区別・重複の有無を確認して、使う公式を決める。", how + "。"],
               alt=["小さい場合（人数や個数を減らした場合）で樹形図をかいて数え、公式の結果と一致するかを確かめる。"],
               pc=[("適切な数え方（公式）を選んでいる", 1), ("正しく計算している", 1)],
               pit=["順序を区別するかどうかを取り違え、P と C を混同する。", "円順列で回転を同一視せず $n!$ とする。"],
               chk=(py, str(val)))


def dice_event(r):
    t = r.choice(["sum", "sumge", "diff", "prod3", "prododd"])
    pairs = list(product(range(1, 7), repeat=2))
    if t == "sum":
        s = r.randint(3, 11)
        ok = [p for p in pairs if sum(p) == s]
        txt = f"出る目の和が ${s}$ になる"
    elif t == "sumge":
        s = r.randint(8, 11)
        ok = [p for p in pairs if sum(p) >= s]
        txt = f"出る目の和が ${s}$ 以上になる"
    elif t == "diff":
        d = r.randint(1, 4)
        ok = [p for p in pairs if abs(p[0] - p[1]) == d]
        txt = f"出る目の差（大きい方から小さい方を引いた値）が ${d}$ になる"
    elif t == "prod3":
        ok = [p for p in pairs if (p[0] * p[1]) % 3 == 0]
        txt = "出る目の積が $3$ の倍数になる"
    else:
        ok = [p for p in pairs if (p[0] * p[1]) % 2 == 1]
        txt = "出る目の積が奇数になる"
    return txt, ok


@gen("basic_check", 5, ["computation"])
def prob_basic(r):
    if r.random() < 0.65:
        txt, ok = dice_event(r)
        P = Fraction(len(ok), 36)
        stem = f"大小2個のさいころを同時に投げるとき、{txt}確率を求めなさい。"
        st = ["目の出方は全部で $6\\times6=36$ 通りで、同様に確からしい。", f"条件を満たす（大，小）の組は ${len(ok)}$ 通り：" + "，".join(f"$({a},\\ {b})$" for a, b in ok[:12]) + ("など。" if len(ok) > 12 else "。"),
              f"確率は $\\dfrac{{{len(ok)}}}{{36}}={ftex(P)}$。"]
        py = f"Rational({len(ok)},36)"
        ap = "大小2個のさいころの目の出方を $6\\times6$ の表に整理し、条件を満たすマスを数える。"
    else:
        N = r.choice([20, 30, 40, 50, 60, 100])
        p, q = r.sample([2, 3, 4, 5, 6, 7], 2)
        from math import gcd
        l = p * q // gcd(p, q)
        cnt = N // p + N // q - N // l
        P = Fraction(cnt, N)
        stem = f"1 から {N} までの整数が1つずつ書かれた {N} 枚のカードから1枚を引くとき、カードの数が ${p}$ の倍数または ${q}$ の倍数である確率を求めなさい。"
        st = [f"${p}$ の倍数は ${N // p}$ 枚、${q}$ の倍数は ${N // q}$ 枚、両方（${l}$ の倍数）は ${N // l}$ 枚。", f"$n(A\\cup B)={N // p}+{N // q}-{N // l}={cnt}$。", f"確率は $\\dfrac{{{cnt}}}{{{N}}}={ftex(P)}$。"]
        py = f"(floor({N}/{p})+floor({N}/{q})-floor({N}/{l}))/{N}"
        ap = "「または」なので和事象。両方の倍数（最小公倍数の倍数）を2回数えないよう、加法定理（要素の個数の公式）を使う。"
    return num(stem, fans(P), st[-1], d=2, disp=f"${ftex(P)}$",
               ap=ap, steps=st,
               alt=["余事象（条件を満たさない場合）の個数を数え、全体から引いて確かめる。"],
               pc=[("全体の場合の数と、条件を満たす場合の数を正しく数えている", 1), ("確率を約分して正しく答えている", 1)],
               pit=["2個のさいころを区別せず、全体を $21$ 通りとしてしまう（同様に確からしくない）。", "重なり（両方を満たす場合）を2回数える。"],
               chk=(py, fans(P)))


@gen("basic_check", 4, ["computation", "concept"])
def complement(r):
    t = r.choice(["dice", "bag", "coin"])
    if t == "dice":
        n, k = r.randint(2, 4), r.randint(1, 6)
        P = 1 - Fraction(5, 6) ** n
        stem = f"1個のさいころを {n} 回投げるとき、${k}$ の目が少なくとも1回出る確率を求めなさい。"
        st = [f"余事象は「{n} 回とも ${k}$ 以外の目が出る」こと。その確率は $\\left(\\dfrac{{5}}{{6}}\\right)^{n}={ftex(Fraction(5, 6) ** n)}$。", f"求める確率は $1-{ftex(Fraction(5, 6) ** n)}={ftex(P)}$。"]
        py = f"1-Rational(5,6)**{n}"
    elif t == "bag":
        a, b = r.randint(2, 5), r.randint(3, 6)
        m = r.randint(2, min(3, b))
        P = 1 - Fraction(comb(b, m), comb(a + b, m))
        stem = f"赤球 {a} 個と白球 {b} 個が入った袋から、同時に {m} 個の球を取り出すとき、少なくとも1個が赤球である確率を求めなさい。"
        st = [f"取り出し方は全部で ${C_(a + b, m)}={comb(a + b, m)}$ 通り。", f"余事象「{m} 個とも白球」は ${C_(b, m)}={comb(b, m)}$ 通り。", f"求める確率は $1-\\dfrac{{{comb(b, m)}}}{{{comb(a + b, m)}}}={ftex(P)}$。"]
        py = f"1-comb({b},{m})/comb({a + b},{m})"
    else:
        n = r.randint(3, 6)
        P = 1 - Fraction(1, 2 ** n)
        stem = f"{n} 枚の硬貨を同時に投げるとき、少なくとも1枚が表になる確率を求めなさい。"
        st = [f"余事象は「{n} 枚とも裏」で、その確率は $\\left(\\dfrac{{1}}{{2}}\\right)^{n}=\\dfrac{{1}}{{{2 ** n}}}$。", f"求める確率は $1-\\dfrac{{1}}{{{2 ** n}}}={ftex(P)}$。"]
        py = f"1-Rational(1,2)**{n}"
    return num(stem, fans(P), st[-1], d=2, disp=f"${ftex(P)}$",
               ap="「少なくとも1個（1回）」の場合を直接数えると場合分けが多くなる。余事象「1個も（1回も）ない」の確率を求めて $1$ から引く。",
               steps=st,
               alt=["「ちょうど1回」「ちょうど2回」……の確率をすべて求めて加えても同じ値になる（計算量は多い）。"],
               pc=[("余事象を正しく設定している", 1), ("余事象の確率を求め、1から引いている", 1)],
               pit=["確率を回数倍して求めてしまう。", "余事象を「すべて赤球（表）」と取り違える。"],
               chk=(py, fans(P)))


@gen("basic_check", 3, ["computation", "condition_check"])
def indep(r):
    p, q = r.choice(PS), r.choice(PS)
    ask = r.choice(["both", "atleast", "exactly"])
    val = {"both": p * q, "atleast": 1 - (1 - p) * (1 - q), "exactly": p * (1 - q) + (1 - p) * q}[ask]
    word = {"both": "2人とも命中する", "atleast": "少なくとも一方が命中する", "exactly": "一方だけが命中する"}[ask]
    how = {"both": f"${ftex(p)}\\times{ftex(q)}={ftex(val)}$",
           "atleast": f"$1-\\left(1-{ftex(p)}\\right)\\left(1-{ftex(q)}\\right)=1-{ftex((1 - p) * (1 - q))}={ftex(val)}$",
           "exactly": f"${ftex(p)}\\times{ftex(1 - q)}+{ftex(1 - p)}\\times{ftex(q)}={ftex(val)}$"}[ask]
    py = {"both": f"{fpy(p)}*{fpy(q)}", "atleast": f"1-(1-{fpy(p)})*(1-{fpy(q)})", "exactly": f"{fpy(p)}*(1-{fpy(q)})+(1-{fpy(p)})*{fpy(q)}"}[ask]
    return num(f"A さんと B さんが的に向かって1回ずつ矢を射る。A さんが命中する確率は ${ftex(p)}$、B さんが命中する確率は ${ftex(q)}$ で、2人の結果は互いに影響しない。{word}確率を求めなさい。",
               fans(val), how + "。", d=2, disp=f"${ftex(val)}$",
               ap="2人の試行は独立なので、それぞれの事象の確率の積が「ともに起こる」確率になる。複数の場合があるときは排反な場合に分けて加える。",
               steps=["2人の試行は独立である。", how + "。"],
               alt=["4通りの結果（命中・外れの組合せ）の確率をすべて表にし、合計が $1$ になることを確かめてから必要なものを加える。"],
               pc=[("独立性を用いて積で計算している", 1), ("場合を正しく選んで答えている", 1)],
               pit=["「少なくとも一方」を $p+q$ としてしまう（重なりを2回数える）。", "外れる確率 $1-p$ を使い忘れる。"],
               chk=(py, fans(val)))


CROSS = [("男子", "女子", "自転車で通学している", "自転車以外で通学している"), ("1年生", "2年生", "図書館をよく利用する", "図書館をあまり利用しない"),
         ("午前の来場者", "午後の来場者", "展示 A を見た", "展示 A を見なかった")]


@gen("basic_check", 3, ["computation", "concept"])
def cond_basic(r):
    g1, g2, c1, c2 = r.choice(CROSS)
    a, b, c, d = (r.randint(3, 25) for _ in range(4))
    N = a + b + c + d
    if r.random() < 0.5:
        q = f"選んだ人が{g1}であったとき、その人が{c1}人である"
        val, how = Fraction(a, a + b), f"$\\dfrac{{{a}}}{{{a}+{b}}}={ftex(Fraction(a, a + b))}$"
        py = f"Rational({a},{a + b})"
    else:
        q = f"選んだ人が{c1}人であったとき、その人が{g2}である"
        val, how = Fraction(c, a + c), f"$\\dfrac{{{c}}}{{{a}+{c}}}={ftex(Fraction(c, a + c))}$"
        py = f"Rational({c},{a + c})"
    rows = [[g1, str(a), str(b), str(a + b)], [g2, str(c), str(d), str(c + d)], ["計", str(a + c), str(b + d), str(N)]]
    return num(f"ある集団 {N} 人について調べた結果（架空のデータ）は、{g1}で{c1}人が {a} 人、{g1}で{c2}人が {b} 人、{g2}で{c1}人が {c} 人、{g2}で{c2}人が {d} 人であった（表にもまとめてある）。この中から1人を選ぶとき、{q}確率を求めなさい。",
               fans(val), how + "。", d=2, disp=f"${ftex(val)}$", tbl=table(rows, header=["", c1, c2, "計"]),
               ap="「〜であったとき」は条件付き確率。条件を満たす人だけを新しい全体とみなし、その中での割合を求める。",
               steps=["条件を満たす人の人数（分母）を表から読む。", "その中で求める事象が起こる人数（分子）を読む。", how + "。"],
               alt=[f"式 $P_A(B)=\\dfrac{{P(A\\cap B)}}{{P(A)}}$ を使い、全体 {N} 人を分母とした確率どうしの比として計算しても同じ値になる。"],
               pc=[("分母（条件を満たす人数）を正しく選んでいる", 1), ("正しく計算している", 1)],
               pit=[f"分母を全体の {N} 人にしてしまう（それは $P(A\\cap B)$）。"],
               chk=(py, fans(val)))


# ======================================================================
# B 標準演習
# ======================================================================

LET = "abcde"


@gen("standard_practice", 4, ["computation", "condition_check"])
def arrangement(r):
    t = r.choice(["word", "adj", "nonadj", "ends"])
    if t == "word":
        counts = r.choice([[2, 2, 1], [3, 2, 1], [2, 2, 2], [3, 1, 1], [3, 2], [2, 2, 1, 1], [4, 2, 1], [3, 3, 1]])
        letters = []
        for ch, c in zip(LET, counts):
            letters += [ch] * c
        n = len(letters)
        val = factorial(n)
        for c in counts:
            val //= factorial(c)
        den = "".join(f"{c}!" for c in counts if c > 1)
        stem = f"{n} 個の文字 {'，'.join(letters)} をすべて1列に並べる方法は何通りあるか。"
        how = f"$\\dfrac{{{n}!}}{{{den}}}={val}$"
        py = f"factorial({n})/(" + "*".join(f"factorial({c})" for c in counts) + ")"
        ap = "同じ文字を含むので、すべてを区別して並べた $n!$ 通りから、同じ文字どうしの入れかえで重複した分を割る。"
    elif t in ("adj", "nonadj"):
        n = r.randint(4, 8)
        adj = factorial(n - 1) * 2
        val = adj if t == "adj" else factorial(n) - adj
        stem = f"A，B を含む {n} 人が1列に並ぶとき、A と B が{'隣り合う' if t == 'adj' else '隣り合わない'}並び方は何通りあるか。"
        how = f"$({n}-1)!\\times2!={adj}$" if t == "adj" else f"${n}!-({n}-1)!\\times2!={factorial(n)}-{adj}={val}$"
        py = f"factorial({n - 1})*2" if t == "adj" else f"factorial({n})-factorial({n - 1})*2"
        ap = "隣り合うものはひとまとめにして考える。「隣り合わない」は全体から「隣り合う」を引く（余事象の考え）。"
    else:
        m, f = r.randint(2, 5), r.randint(2, 4)
        n = m + f
        val = perm(m, 2) * factorial(n - 2)
        stem = f"男子 {m} 人と女子 {f} 人が1列に並ぶとき、両端がともに男子である並び方は何通りあるか。"
        how = f"${P_(m, 2)}\\times{n - 2}!={perm(m, 2)}\\times{factorial(n - 2)}={val}$"
        py = f"perm({m},2)*factorial({n - 2})"
        ap = "条件のある位置（両端）から先に決め、残りの位置に残りの人を並べる。"
    return num(stem, str(val), how + "。", d=3,
               ap=ap, steps=["条件のある部分を先に処理する。", how + "。"],
               alt=["人数（文字数）を小さくした場合で書き出して数え、同じ考え方の式が正しいかを確かめる。"],
               pc=[("条件の処理の仕方が正しい", 2), ("正しく計算している", 2)],
               pit=["ひとまとめにしたものの中の並び方をかけ忘れる。", "同じものを含む順列で、割る数を誤る。"],
               chk=(py, str(val)))


@gen("standard_practice", 4, ["computation", "application"])
def comb_shapes(r):
    t = r.choice(["tri", "diag", "path", "pathvia"])
    if t == "tri":
        n = r.randint(5, 12)
        val, py = comb(n, 3), f"comb({n},3)"
        stem = f"円周上に異なる {n} 個の点がある。これらのうち3点を頂点とする三角形は何個できるか。"
        how = f"${C_(n, 3)}={val}$"
        ap = "円周上の3点は一直線上にないので、3点の選び方と三角形が1対1に対応する。"
    elif t == "diag":
        n = r.randint(5, 12)
        val, py = comb(n, 2) - n, f"comb({n},2)-{n}"
        stem = f"正 {n} 角形の対角線は何本あるか。"
        how = f"${C_(n, 2)}-{n}={comb(n, 2)}-{n}={val}$"
        ap = "2つの頂点を結ぶ線分の総数から、辺（となり合う頂点を結ぶ線分）の数を引く。"
    elif t == "path":
        a, b = r.randint(2, 6), r.randint(2, 5)
        val, py = comb(a + b, a), f"comb({a + b},{a})"
        stem = f"東西に {a + 1} 本、南北に {b + 1} 本の道が碁盤の目のように通っている。西南の角 P から東北の角 Q まで、東へ {a} 区画、北へ {b} 区画進む最短経路は何通りあるか。"
        how = f"${C_(a + b, a)}={val}$"
        ap = f"最短経路は「東」{a} 個と「北」{b} 個を1列に並べる並べ方と対応する（同じものを含む順列）。"
    else:
        a, b = r.randint(3, 6), r.randint(2, 5)
        c, d = r.randint(1, a - 1), r.randint(1, b - 1)
        val = comb(c + d, c) * comb(a - c + b - d, a - c)
        py = f"comb({c + d},{c})*comb({a - c + b - d},{a - c})"
        stem = f"東へ {a} 区画、北へ {b} 区画の碁盤の目の道で、西南の角 P から東北の角 Q まで最短経路で進む。P から東へ {c} 区画、北へ {d} 区画の交差点 R を必ず通る経路は何通りあるか。"
        how = f"${C_(c + d, c)}\\times{C_(a - c + b - d, a - c)}={comb(c + d, c)}\\times{comb(a - c + b - d, a - c)}={val}$"
        ap = "P→R と R→Q の2段階に分け、それぞれの最短経路の数をかける（積の法則）。"
    return num(stem, str(val), how + "。", d=3,
               ap=ap, steps=["数える対象を、選び方・並べ方に言いかえる。", how + "。"],
               alt=["小さい場合で図をかいて実際に数え、同じ考え方の式が成り立つかを確かめる。経路は交差点ごとに「そこまでの経路数」を書きこむ方法でも数えられる。"],
               pc=[("対象を選び方・並べ方に正しく言いかえている", 2), ("正しく計算している", 2)],
               pit=["対角線の数で辺を引き忘れる。", "経路の数を、区画数の積としてしまう。"],
               chk=(py, str(val)))


EVENTS = [("1個のさいころを投げて、3の倍数の目が出る", Fraction(1, 3)), ("1個のさいころを投げて、2以下の目が出る", Fraction(1, 3)),
          ("1個のさいころを投げて、偶数の目が出る", Fraction(1, 2)), ("1個のさいころを投げて、5以上の目が出る", Fraction(1, 3)),
          ("1個のさいころを投げて、1の目が出る", Fraction(1, 6)), ("あるバスケットボール選手がフリースローを1本投げて成功する（成功する確率を $\\dfrac{2}{3}$ とする）", Fraction(2, 3)),
          ("赤球1個と白球3個が入った袋から1個取り出して色を調べ、もとに戻す。赤球が出る", Fraction(1, 4))]


@gen("standard_practice", 4, ["computation", "concept"])
def repeated(r):
    ev, p = r.choice(EVENTS)
    n = r.randint(3, 6)
    k = r.randint(1, n - 1)
    atleast = r.random() < 0.3 and n <= 4
    if atleast:
        val = sum(comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k, n + 1))
        py = "+".join(f"comb({n},{i})*{fpy(p)}**{i}*(1-{fpy(p)})**{n - i}" for i in range(k, n + 1))
        how = "+".join(f"{C_(n, i)}\\left({ftex(p)}\\right)^{{{i}}}\\left({ftex(1 - p)}\\right)^{{{n - i}}}" for i in range(k, n + 1))
        word = f"{k} 回以上"
    else:
        val = comb(n, k) * p ** k * (1 - p) ** (n - k)
        py = f"comb({n},{k})*{fpy(p)}**{k}*(1-{fpy(p)})**{n - k}"
        how = f"{C_(n, k)}\\left({ftex(p)}\\right)^{{{k}}}\\left({ftex(1 - p)}\\right)^{{{n - k}}}"
        word = f"ちょうど {k} 回"
    return num(f"「{ev}」という試行を {n} 回くり返す。この事象が{word}起こる確率を求めなさい。", fans(val),
               f"${how}={ftex(val)}$。", d=3, disp=f"${ftex(val)}$",
               ap=f"各回は独立で、1回に起こる確率は ${ftex(p)}$。反復試行の確率 ${{}}_n\\mathrm{{C}}_r\\,p^r(1-p)^{{n-r}}$ を使う。" + ("「以上」は回数ごとの確率を加える。" if atleast else ""),
               steps=[f"1回の確率 $p={ftex(p)}$、起こらない確率 $1-p={ftex(1 - p)}$。", f"${how}$。", f"$={ftex(val)}$。"],
               alt=[f"$n={n}$ 回の結果を「○（起こる）」「×（起こらない）」の列として考え、○の位置の選び方 ${{}}_{{{n}}}\\mathrm{{C}}_r$ 通りのそれぞれの確率が等しいことを確かめる。"],
               pc=[("反復試行の式を正しく立てている", 2), ("正しく計算して約分している", 2)],
               pit=["${}_n\\mathrm{C}_r$ をかけ忘れる。", "起こらない確率 $1-p$ の指数を誤る。"],
               chk=(py, fans(val)))


@gen("standard_practice", 4, ["computation", "concept"])
def cond_bayes(r):
    rule, pA = r.choice([("硬貨を投げて表なら袋 A、裏なら袋 B", Fraction(1, 2)), ("さいころを投げて1か2の目なら袋 A、それ以外なら袋 B", Fraction(1, 3)),
                         ("さいころを投げて1から4の目なら袋 A、それ以外なら袋 B", Fraction(2, 3))])
    while True:
        r1, w1, r2, w2 = r.randint(1, 6), r.randint(1, 6), r.randint(1, 6), r.randint(1, 6)
        if Fraction(r1, r1 + w1) != Fraction(r2, r2 + w2):
            break
    ask_white = r.random() < 0.35
    c1, c2 = (w1, w2) if ask_white else (r1, r2)
    col = "白球" if ask_white else "赤球"
    a_ = pA * Fraction(c1, r1 + w1)
    b_ = (1 - pA) * Fraction(c2, r2 + w2)
    val = a_ / (a_ + b_)
    return num(f"袋 A には赤球 {r1} 個と白球 {w1} 個、袋 B には赤球 {r2} 個と白球 {w2} 個が入っている。{rule}を選び、選んだ袋から球を1個取り出す。取り出した球が{col}であったとき、それが袋 A から取り出されたものである確率を求めなさい。",
               fans(val), f"$\\dfrac{{{ftex(a_)}}}{{{ftex(a_)}+{ftex(b_)}}}={ftex(val)}$。", d=4, disp=f"${ftex(val)}$",
               ap=f"「{col}であった」ことが分かったうえでの確率なので条件付き確率。{col}が出るすべての場合（A から・B から）の確率を分母にする。",
               steps=[f"A を選んで{col}：${ftex(pA)}\\times\\dfrac{{{c1}}}{{{r1 + w1}}}={ftex(a_)}$。", f"B を選んで{col}：${ftex(1 - pA)}\\times\\dfrac{{{c2}}}{{{r2 + w2}}}={ftex(b_)}$。",
                      f"{col}が出る確率：${ftex(a_ + b_)}$。", f"求める確率：${ftex(a_)}\\div{ftex(a_ + b_)}={ftex(val)}$。"],
               alt=["樹形図の枝に確率を書きこみ、" + col + "に至る2本の枝の確率の比から答えを読み取る。"],
               pc=[("2つの場合の確率を乗法定理で正しく求めている", 2), ("条件付き確率の式を正しく立てて計算している", 2)],
               pit=[f"袋 A から{col}を取り出す確率 ${ftex(a_)}$ をそのまま答える。", f"袋 A の中の{col}の割合 $\\dfrac{{{c1}}}{{{r1 + w1}}}$ を答える。"],
               chk=(f"({fpy(pA)}*Rational({c1},{r1 + w1}))/({fpy(pA)}*Rational({c1},{r1 + w1})+{fpy(1 - pA)}*Rational({c2},{r2 + w2}))", fans(val)))


@gen("standard_practice", 4, ["computation", "application"])
def expectation(r):
    t = r.choice(["lot", "lot", "red", "max"])
    if t == "lot":
        T = r.choice([10, 20, 50, 100])
        c1, c2 = r.randint(1, 3), r.randint(2, 6)
        x1, x2 = r.choice([500, 1000, 2000, 300]), r.choice([100, 200, 50])
        val = Fraction(x1 * c1 + x2 * c2, T)
        stem = f"{T} 本のくじの中に、1等（{x1} 円）が {c1} 本、2等（{x2} 円）が {c2} 本あり、残りははずれ（0 円）である。このくじを1本引くときの賞金の期待値を求めなさい。"
        how = f"${x1}\\times\\dfrac{{{c1}}}{{{T}}}+{x2}\\times\\dfrac{{{c2}}}{{{T}}}={ftex(val)}$"
        py = f"{x1}*Rational({c1},{T})+{x2}*Rational({c2},{T})"
        unit = "円"
        st = ["賞金のとりうる値と確率の表をつくる。", how + "（円）。"]
    elif t == "red":
        a, b = r.randint(2, 6), r.randint(2, 6)
        m = r.randint(2, min(3, a + b - 1))
        terms_ = [(k, Fraction(comb(a, k) * comb(b, m - k), comb(a + b, m))) for k in range(0, m + 1) if k <= a and m - k <= b]
        val = sum(k * p for k, p in terms_)
        stem = f"赤球 {a} 個と白球 {b} 個が入った袋から同時に {m} 個の球を取り出すとき、取り出される赤球の個数の期待値を求めなさい。"
        how = "+".join(f"{k}\\times{ftex(p)}" for k, p in terms_ if k > 0) + f"={ftex(val)}"
        py = "+".join(f"{k}*comb({a},{k})*comb({b},{m - k})/comb({a + b},{m})" for k, _ in terms_ if k > 0)
        unit = "個"
        st = ["赤球の個数 $X$ のとりうる値は " + "，".join(str(k) for k, _ in terms_) + "。", "各値の確率：" + "，".join(f"$P(X={k})={ftex(p)}$" for k, p in terms_) + "。", f"期待値 ${how}$（個）。"]
        how = f"${how}$"
    else:
        n = r.choice([2, 3])
        dist = [(k, Fraction(k ** n - (k - 1) ** n, 6 ** n)) for k in range(1, 7)]
        val = sum(k * p for k, p in dist)
        stem = f"{n} 個のさいころを同時に投げるとき、出る目の最大値の期待値を求めなさい。"
        how = f"$\\sum k\\,P(X=k)={ftex(val)}$"
        py = "+".join(f"{k}*Rational({k ** n - (k - 1) ** n},{6 ** n})" for k in range(1, 7))
        unit = ""
        st = [f"最大値が $k$ 以下である確率は $\\left(\\dfrac{{k}}{{6}}\\right)^{n}$。", f"$P(X=k)=\\left(\\dfrac{{k}}{{6}}\\right)^{n}-\\left(\\dfrac{{k-1}}{{6}}\\right)^{n}$ より " + "，".join(f"$P(X={k})={ftex(p)}$" for k, p in dist) + "。", f"期待値 {how}。"]
    return num(stem, fans(val), st[-1], d=3 if t == "lot" else 4, disp=f"${ftex(val)}$" + (f" {unit}" if unit else ""),
               ap="とりうる値とその確率の表（確率分布）をつくり、「値 × 確率」の和を求める。確率の合計が $1$ になることも確かめる。",
               steps=st,
               alt=["確率の合計が $1$ になることを確かめてから期待値を計算すると、数え漏れに気づきやすい。"],
               pc=[("とりうる値と確率を正しく求めている", 2), ("期待値を正しく計算している", 2)],
               pit=["確率をかけずに値を平均してしまう。", "とりうる値の一部（0 円や 0 個など）を表から落とす（期待値には影響しないが、確率の合計の確認ができない）。"],
               chk=(py, fans(val)))


# ======================================================================
# C 思考力・記述応用
# ======================================================================

GROUPS = [(2, 2), (3, 3), (4, 4), (2, 2, 2), (3, 3, 3), (3, 2, 1), (4, 2), (4, 3), (2, 2, 1), (3, 3, 2), (4, 2, 2), (2, 2, 2, 2)]


@gen("thinking_writing", 3, ["written_reasoning", "condition_check"])
def groups(r):
    sizes = r.choice(GROUPS)
    labeled = r.random() < 0.4
    n = sum(sizes)
    ordered = factorial(n)
    for s_ in sizes:
        ordered //= factorial(s_)
    div = 1
    if not labeled:
        from collections import Counter
        for c in Counter(sizes).values():
            div *= factorial(c)
    val = ordered // div
    desc_sz = "、".join(f"{s_} 人" for s_ in sizes)
    if labeled:
        names = "ABCD"[: len(sizes)]
        target = "、".join(f"部屋 {nm} に {s_} 人" for nm, s_ in zip(names, sizes))
        stem = f"{n} 人を、{target}が入るように分ける方法は何通りあるか。考え方も説明しなさい。"
    else:
        stem = f"{n} 人を {desc_sz}の {len(sizes)} つの組に分ける方法は何通りあるか。ただし、組には名前や番号がなく区別しない。考え方も説明しなさい。"
    seq = []
    rest = n
    for s_ in sizes:
        seq.append(C_(rest, s_))
        rest -= s_
    prod_tex = "\\times".join(seq)
    from collections import Counter
    same = [k for k, c in Counter(sizes).items() if c > 1]
    reason = ("部屋に区別があるので、順に選んだ結果がそのまま異なる分け方になる。" if labeled else
              ("同じ人数の組が " + "、".join(f"{Counter(sizes)[k]} つ（{k} 人組）" for k in same) + "あり、組に区別がないので、その並べかえの数で割る。" if same else "人数がすべて異なるので、組に区別がなくても重複は生じない。"))
    return desc(stem, f"${val}$ 通り",
                f"順に選ぶと ${prod_tex}={ordered}$ 通り。" + reason + (f"よって ${ordered}\\div{div}={val}$ 通り。" if div > 1 else f"よって ${val}$ 通り。"),
                rubric=[("順に選ぶ方法の数を組合せで正しく表している", 2), ("組の区別の有無による重複を正しく判断している", 3), ("割る数（または割らない理由）を説明している", 2), ("答えが正しい", 1)],
                d=4, p=8, lines=8,
                ap="まず組（部屋）に区別があるとして、順に人を選ぶ方法を積の法則で数える。次に、組に区別がない場合は、同じ人数の組を入れかえただけの重複を考える。",
                steps=[f"区別があるとして順に選ぶ：${prod_tex}={ordered}$ 通り。", reason, f"答え：${val}$ 通り。"],
                alt=["人数を小さくした例（4人を2人ずつ2組に分けるなど）で実際に書き出し、割る必要がある理由を確かめる（4人なら3通り）。"],
                pc=[("順に選ぶ方法", 2), ("重複の判断", 3), ("割る数の説明", 2), ("答え", 1)],
                pit=["組に区別がないのに割り忘れる。", "人数の異なる組まで区別がないとして割ってしまう。"],
                chk=(f"({'*'.join(f'comb({n - sum(sizes[:i])},{sizes[i]})' for i in range(len(sizes)))})/{div}", str(val), None, "intermediate"))


@gen("thinking_writing", 3, ["written_reasoning", "computation"])
def max_min(r):
    n, k = r.randint(2, 4), r.randint(2, 6)
    is_max = r.random() < 0.6
    if is_max:
        val = Fraction(k ** n - (k - 1) ** n, 6 ** n)
        word, a_, b_ = f"最大値が ${k}$ ", f"すべて ${k}$ 以下", f"すべて ${k - 1}$ 以下"
        num_ = f"{k}^{n}-{k - 1}^{n}"
        py = f"Rational({k},6)**{n}-Rational({k - 1},6)**{n}"
    else:
        k = r.randint(1, 5)
        val = Fraction((7 - k) ** n - (6 - k) ** n, 6 ** n)
        word, a_, b_ = f"最小値が ${k}$ ", f"すべて ${k}$ 以上", f"すべて ${k + 1}$ 以上"
        num_ = f"{7 - k}^{n}-{6 - k}^{n}"
        py = f"Rational({7 - k},6)**{n}-Rational({6 - k},6)**{n}"
    return desc(f"1個のさいころを {n} 回投げるとき、出る目の{word}である確率を求めなさい。考え方も説明しなさい。",
                f"${ftex(val)}$", f"「{a_}」の確率から「{b_}」の確率を引く：$\\dfrac{{{num_}}}{{6^{n}}}={ftex(val)}$。",
                rubric=[(f"「{a_}」という事象を考えている", 2), (f"「{b_}」との差として表す理由を説明している", 3), ("確率を正しく計算している", 2), ("答えを約分して正しく答えている", 1)],
                d=4, p=8, lines=8,
                ap="「" + word.replace("$", "") + "」を直接数えると場合分けが多い。「" + a_.replace("$", "") + "」という事象から、「" + b_.replace("$", "") + "」の場合を除くと考える。",
                steps=[f"事象 $A$：{a_}。" + ("$P(A)=1$。" if Fraction(k if is_max else 7 - k, 6) == 1 else f"$P(A)=\\left({ftex(Fraction(k if is_max else 7 - k, 6))}\\right)^{n}$。"), f"事象 $B$：{b_}。$B\\subset A$ で、$P(B)=\\left({ftex(Fraction(k - 1 if is_max else 6 - k, 6))}\\right)^{n}$。",
                       f"{word}であるのは、$A$ が起こり $B$ が起こらないとき。", f"確率は $P(A)-P(B)=\\dfrac{{{num_}}}{{6^{n}}}={ftex(val)}$。"],
                alt=[f"{word}になる目の出方を、「{k} が出る回数」で場合分けして数えても同じ結果になる（反復試行の考え）。"],
                pc=[("事象 $A$ の設定", 2), ("差をとる理由", 3), ("計算", 2), ("答え", 1)],
                pit=[f"「少なくとも1回 ${k}$ が出る」ことと混同する。", f"「{word.replace('$', '')}」の確率を $\\left(\\dfrac{{1}}{{6}}\\right)^{n}$ などとする。"],
                chk=(py, fans(val), None, "intermediate"))


QS = [Fraction(1, 6), Fraction(1, 5), Fraction(1, 4), Fraction(1, 3), Fraction(2, 5), Fraction(1, 2), Fraction(3, 5), Fraction(2, 3), Fraction(3, 4), Fraction(4, 5), Fraction(5, 6)]


@gen("thinking_writing", 2, ["cross_unit", "application"], rel=["HS-MATH1-U03"])
def cross_quad(r):
    a, b = sorted(r.sample(QS, 2))
    f = lambda p: 2 * p * (1 - p)  # noqa: E731
    half = Fraction(1, 2)
    pts = [a, b] + ([half] if a <= half <= b else [])
    mx = max(pts, key=f)
    mn = min([a, b], key=f)
    eq_end = f(a) == f(b)
    mn_txt = f"$p={ftex(a)},\\ {ftex(b)}$ のとき最小値 ${ftex(f(a))}$" if eq_end else f"$p={ftex(mn)}$ のとき最小値 ${ftex(f(mn))}$"
    return sa(f"1回の試行で事象 $A$ が起こる確率を $p$ とする。この試行を独立に2回行うとき、$A$ がちょうど1回起こる確率を $f(p)$ とする。$p$ が ${ftex(a)}\\leqq p\\leqq {ftex(b)}$ の範囲を動くとき、$f(p)$ の最大値と最小値、およびそのときの $p$ の値を求めなさい。",
              f"$p={ftex(mx)}$ のとき最大値 ${ftex(f(mx))}$、{mn_txt}",
              f"$f(p)={C_(2, 1)}p(1-p)=-2\\left(p-\\dfrac{{1}}{{2}}\\right)^2+\\dfrac{{1}}{{2}}$。軸 $p=\\dfrac{{1}}{{2}}$ と区間の位置関係から判断する。", d=4, p=8,
              ap="反復試行の確率で $f(p)$ を $p$ の式に表すと二次関数になる（二次関数の単元）。平方完成して、軸と定義域の位置関係から最大・最小を調べる。",
              steps=[f"$f(p)={C_(2, 1)}p(1-p)=2p-2p^2$。", "平方完成：$f(p)=-2\\left(p-\\dfrac{1}{2}\\right)^2+\\dfrac{1}{2}$（上に凸、軸 $p=\\dfrac{1}{2}$）。",
                     f"区間 ${ftex(a)}\\leqq p\\leqq {ftex(b)}$ で、候補の値：" + "，".join(f"$f({ftex(x)})={ftex(f(x))}$" for x in pts) + "。",
                     f"最大値は $p={ftex(mx)}$ で ${ftex(f(mx))}$、最小値は軸から遠い端点でとる。"],
              alt=["$f(p)=2p(1-p)$ は $p$ と $1-p$ を入れかえても変わらない（$p=\\dfrac{1}{2}$ に関して対称）ことから、軸からの距離で比べてもよい。"],
              pc=[("$f(p)$ を反復試行の確率として正しく表している", 2), ("平方完成して軸を求めている", 2), ("区間での最大・最小を正しく判断している", 4)],
              pit=["${}_2\\mathrm{C}_1=2$ をかけ忘れ、$f(p)=p(1-p)$ とする。", "軸が区間外にあるのに頂点の値を最大値とする。"],
              chk=(f"[2*{fpy(mx)}*(1-{fpy(mx)}), Min(2*{fpy(a)}*(1-{fpy(a)}), 2*{fpy(b)}*(1-{fpy(b)}))]", f"[{fpy(f(mx))}, {fpy(min(f(a), f(b)))}]", None, "intermediate"))


@gen("thinking_writing", 2, ["written_reasoning", "condition_check"])
def test_bayes(r):
    while True:
        prev = r.choice([Fraction(1, 100), Fraction(2, 100), Fraction(5, 100), Fraction(3, 100), Fraction(1, 1000), Fraction(4, 100)])
        se = r.choice([Fraction(95, 100), Fraction(99, 100), Fraction(98, 100), Fraction(4, 5)])
        fp = r.choice([Fraction(5, 100), Fraction(2, 100), Fraction(1, 10), Fraction(1, 20), Fraction(3, 100)])
        if not (prev == Fraction(1, 10) and se == Fraction(9, 10) and fp == Fraction(1, 10)):
            break
    tp_ = prev * se
    fp_ = (1 - prev) * fp
    val = tp_ / (tp_ + fp_)
    pct = lambda f: f"{float(f) * 100:g}\\%"  # noqa: E731
    return desc(f"ある感染症の検査は、感染している人に行うと ${pct(se)}$ の確率で陽性となり、感染していない人に行っても ${pct(fp)}$ の確率で陽性となる（架空の設定）。感染している人の割合が全体の ${pct(prev)}$ である集団から1人を選んで検査したところ陽性であった。この人が実際に感染している確率を求め、その値について気づいたことを述べなさい。",
                f"${ftex(val)}$（約 ${float(val) * 100:.1f}\\%$）。陽性であっても実際には感染していない確率が約 ${100 - float(val) * 100:.1f}\\%$ あり、陽性の人のうち感染している人の割合は、検査が感染者を陽性とする確率 ${pct(se)}$ より小さい。感染している人の割合が小さいほど、この差は大きくなる。",
                "陽性となる確率を「感染していて陽性」と「感染していないが陽性」の和で求め、条件付き確率を計算する。",
                rubric=[("2つの場合（感染して陽性・感染していないが陽性）の確率を乗法定理で求めている", 3), ("条件付き確率の式を正しく立てている", 2), ("値を正しく計算している", 2), ("結果について妥当な考察を述べている", 1)],
                d=5, p=8, lines=10,
                ap="「陽性であった」ことが分かったうえでの確率なので条件付き確率。陽性となるすべての場合（感染している・いない）の確率を分母にする。",
                steps=[f"感染していて陽性：${ftex(prev)}\\times{ftex(se)}={ftex(tp_)}$。", f"感染していないが陽性：${ftex(1 - prev)}\\times{ftex(fp)}={ftex(fp_)}$。",
                       f"陽性となる確率：${ftex(tp_ + fp_)}$。", f"求める確率：${ftex(tp_)}\\div{ftex(tp_ + fp_)}={ftex(val)}\\fallingdotseq{float(val):.3f}$。"],
                alt=["集団を 10000 人などと具体的な人数で考え、各場合の人数を表にして割合を求めると、直感的に理解しやすい。"],
                pc=[("2つの場合の確率", 3), ("条件付き確率の式", 2), ("計算", 2), ("考察", 1)],
                pit=[f"検査の精度 ${pct(se)}$ をそのまま答えてしまう。", "感染していないが陽性となる場合を分母に入れ忘れる。"],
                chk=(f"({fpy(prev)}*{fpy(se)})/({fpy(prev)}*{fpy(se)}+(1-{fpy(prev)})*{fpy(fp)})", fpy(val), None, "intermediate"))


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(stem, wrong, step, etype, tempt, fix, ans, expl, steps, ap, alt, pit, chk=None, d=3):
    return desc(f"{stem}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい答えを求めなさい。", ans, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい解答を途中式とともに示している", 3), ("最終的な答えが正しい", 1)], d=d, p=6, lines=6,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい途中式", 3), ("正しい答え", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix), chk=chk)


@gen("error_correction", 3, ["common_error", "concept"])
def err_pc(r):
    if r.random() < 0.6:
        n = r.randint(5, 10)
        k = r.randint(2, 4)
        role = r.choice(["清掃当番", "実行委員", "代表選手", "調査係"])
        return err_item(f"{n} 人の中から {k} 人の{role}を選ぶ方法は何通りあるか。", f"${P_(n, k)}=" + "\\times".join(str(n - i) for i in range(k)) + f"={perm(n, k)}$ 通り",
                        "順列 P を使った部分", "concept",
                        "「選ぶ」問題でも、1人目・2人目……と順に選ぶ様子を思い浮かべて、順序を区別してしまった。",
                        f"選んだ {k} 人に順序や役割の区別はないので組合せ：${C_(n, k)}={comb(n, k)}$ 通り", f"${comb(n, k)}$ 通り",
                        f"順列では同じ {k} 人の組を ${k}!={factorial(k)}$ 回ずつ重複して数えている。",
                        [f"選ぶ {k} 人の間に区別はない。", f"${C_(n, k)}=\\dfrac{{{P_(n, k)}}}{{{k}!}}=\\dfrac{{{perm(n, k)}}}{{{factorial(k)}}}={comb(n, k)}$。"],
                        "選んだものの間に順序や役割の区別があるか（P）、ないか（C）を判断する。",
                        [f"たとえば A，B，… の {k} 人の組は、順列では ${k}!$ 通りの並びとして数えられていることを書き出して確かめる。"],
                        ["P と C を取り違える。"], chk=(f"perm({n},{k})/factorial({k})", str(comb(n, k)), None, "intermediate"), d=2)
    n = r.randint(4, 8)
    return err_item(f"{n} 人が円形のテーブルのまわりに座る座り方は何通りあるか。ただし、回転して一致するものは同じとみなす。", f"${n}!={factorial(n)}$ 通り",
                    "回転して一致するものを区別して数えた部分", "concept",
                    "1列に並べる順列と同じように考え、回転による重複を考えていない。",
                    f"回転して一致する {n} 通りずつが同じ座り方なので、${n}!\\div{n}=({n}-1)!={factorial(n - 1)}$ 通り", f"${factorial(n - 1)}$ 通り",
                    f"1列の並べ方 ${n}!$ 通りのうち、回転して一致するものが {n} 通りずつある。",
                    [f"1人の位置を固定する。", f"残りの {n - 1} 人の並べ方は $({n}-1)!={factorial(n - 1)}$ 通り。"],
                    "円順列は「1つを固定して残りを並べる」。",
                    ["3人の場合を図で書き出すと、$3!=6$ 通りではなく2通りしかないことが確かめられる。"],
                    ["回転による重複を割り忘れる。"], chk=(f"factorial({n})/{n}", str(factorial(n - 1)), None, "intermediate"), d=2)


@gen("error_correction", 3, ["common_error", "computation"])
def err_atleast(r):
    if r.random() < 0.6:
        n, k = r.randint(2, 5), r.randint(1, 6)
        P = 1 - Fraction(5, 6) ** n
        wrong = f"1回で ${k}$ の目が出る確率は $\\dfrac{{1}}{{6}}$ なので、{n} 回では ${n}\\times\\dfrac{{1}}{{6}}={ftex(Fraction(n, 6))}$"
        stem = f"1個のさいころを {n} 回投げるとき、${k}$ の目が少なくとも1回出る確率を求めなさい。"
        st = [f"余事象「{n} 回とも ${k}$ 以外」の確率は $\\left(\\dfrac{{5}}{{6}}\\right)^{n}={ftex(Fraction(5, 6) ** n)}$。", f"求める確率は $1-{ftex(Fraction(5, 6) ** n)}={ftex(P)}$。"]
        py = f"1-Rational(5,6)**{n}"
    else:
        p = r.choice([Fraction(1, 3), Fraction(1, 4), Fraction(2, 5), Fraction(1, 5)])
        n = r.randint(2, 3)
        P = 1 - (1 - p) ** n
        wrong = f"1回で当たる確率は ${ftex(p)}$ なので、{n} 回では ${n}\\times{ftex(p)}={ftex(n * p)}$"
        stem = f"当たる確率が ${ftex(p)}$ のくじを、引いたくじを毎回もとに戻して {n} 回引く。少なくとも1回当たる確率を求めなさい。"
        st = [f"余事象「{n} 回ともはずれ」の確率は $\\left({ftex(1 - p)}\\right)^{n}={ftex((1 - p) ** n)}$。", f"求める確率は $1-{ftex((1 - p) ** n)}={ftex(P)}$。"]
        py = f"1-(1-{fpy(p)})**{n}"
    return err_item(stem, wrong, "確率を回数倍した部分", "concept",
                    "「1回で $p$ なら $n$ 回で $n$ 倍」と比例のように考えた。2回以上起こる場合を重複して数えていることに気づいていない。",
                    st[-1], f"${ftex(P)}$",
                    "回数倍すると、2回以上起こる場合を重複して数えることになる（回数を増やすと確率が $1$ を超えることもある）。",
                    st, "「少なくとも1回」は余事象「1回も起こらない」の確率を $1$ から引いて求める。",
                    ["回数を大きくすると、回数倍の考え方では確率が $1$ を超えてしまい矛盾することから誤りに気づける。"],
                    ["確率を回数倍する。"], chk=(py, fans(P), None, "intermediate"))


@gen("error_correction", 2, ["common_error", "concept"])
def err_cond(r):
    g1, g2, c1, c2 = r.choice(CROSS)
    a, b, c, d = (r.randint(4, 25) for _ in range(4))
    N = a + b + c + d
    val = Fraction(a, a + b)
    wrong = f"{g1}で{c1}人は {a} 人なので、確率は $\\dfrac{{{a}}}{{{N}}}{'=' + ftex(Fraction(a, N)) if Fraction(a, N).denominator != N else ''}$"
    return err_item(f"ある集団 {N} 人のうち、{g1}で{c1}人が {a} 人、{g1}で{c2}人が {b} 人、{g2}で{c1}人が {c} 人、{g2}で{c2}人が {d} 人である（架空のデータ）。この中から1人を選ぶとき、選んだ人が{g1}であったときに、その人が{c1}人である確率を求めなさい。",
                    wrong, "分母を全体の人数にした部分", "concept",
                    "「{g1}かつ{c1}」の確率 $P(A\\cap B)$ と、「{g1}であったときの」条件付き確率 $P_A(B)$ を区別していない。".replace("{g1}", g1).replace("{c1}", c1),
                    f"{g1}は ${a}+{b}={a + b}$ 人なので、$P_A(B)=\\dfrac{{{a}}}{{{a + b}}}" + ("" if val.denominator == a + b else f"={ftex(val)}") + "$", f"${ftex(val)}$",
                    f"条件「{g1}であった」により、全体は {g1}の {a + b} 人にしぼられる。",
                    [f"条件を満たす人：{g1}の ${a + b}$ 人。", f"その中で{c1}人：${a}$ 人。", f"$P_A(B)=\\dfrac{{{a}}}{{{a + b}}}" + ("" if val.denominator == a + b else f"={ftex(val)}") + "$。"],
                    "「〜であったとき」の確率は、条件を満たすものだけを全体とみなして求める。",
                    [f"式 $P_A(B)=\\dfrac{{P(A\\cap B)}}{{P(A)}}=\\dfrac{{{a}/{N}}}{{{a + b}/{N}}}$ で計算しても同じ値になる。"],
                    ["条件付き確率の分母を全体にしてしまう。"], chk=(f"Rational({a},{N})/Rational({a + b},{N})", fans(val), None, "intermediate"))


@gen("error_correction", 2, ["common_error", "computation"])
def err_replace(r):
    a, b = r.randint(2, 6), r.randint(2, 6)
    n = a + b
    val = Fraction(a * (a - 1), n * (n - 1))
    wrong = f"1回目に赤球が出る確率は $\\dfrac{{{a}}}{{{n}}}$、2回目も $\\dfrac{{{a}}}{{{n}}}$ なので、$\\left(\\dfrac{{{a}}}{{{n}}}\\right)^2={ftex(Fraction(a * a, n * n))}$"
    return err_item(f"赤球 {a} 個と白球 {b} 個が入った袋から、1個ずつ2回続けて球を取り出す。ただし、取り出した球はもとに戻さない。2回とも赤球が出る確率を求めなさい。",
                    wrong, "2回目の確率を1回目と同じにした部分", "concept",
                    "球をもとに戻す場合（独立な試行）と同じように考え、1回目の結果で袋の中身が変わることを見落とした。",
                    f"2回目は赤球 ${a - 1}$ 個を含む ${n - 1}$ 個から取り出すので、$\\dfrac{{{a}}}{{{n}}}\\times\\dfrac{{{a - 1}}}{{{n - 1}}}={ftex(val)}$", f"${ftex(val)}$",
                    "もとに戻さないので、1回目に赤球が出たという条件のもとで2回目の確率を考える（乗法定理）。",
                    [f"1回目に赤球：$\\dfrac{{{a}}}{{{n}}}$。", f"1回目が赤球のとき、2回目に赤球：$\\dfrac{{{a - 1}}}{{{n - 1}}}$。", f"乗法定理より $\\dfrac{{{a}}}{{{n}}}\\times\\dfrac{{{a - 1}}}{{{n - 1}}}={ftex(val)}$。"],
                    "もとに戻さない取り出しは独立な試行ではない。条件付き確率を使って順にかける。",
                    [f"「同時に2個取り出す」と考えて $\\dfrac{{{C_(a, 2)}}}{{{C_(n, 2)}}}=\\dfrac{{{comb(a, 2)}}}{{{comb(n, 2)}}}$ としても同じ値 ${ftex(val)}$ になる。"],
                    ["もとに戻さないのに独立な試行として計算する。"],
                    chk=(f"comb({a},2)/comb({n},2)", fans(val), None, "intermediate"))


GENERATORS = [perm_comb, prob_basic, complement, indep, cond_basic,
              arrangement, comb_shapes, repeated, cond_bayes, expectation,
              groups, max_min, cross_quad, test_bayes,
              err_pc, err_atleast, err_cond, err_replace]
