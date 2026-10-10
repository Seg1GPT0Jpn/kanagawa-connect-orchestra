"""単元パック：数学Ⅰ 集合と命題（集合・命題と条件・必要条件と十分条件・対偶と背理法）。"""
from fractions import Fraction
from math import gcd

from banks._common import desc, mc, ms, num, sa
from hs_pack_lib import (board, check, definition, example, frac, gen, guide, intro, lesson, nonzero, poly, proof, summary,
                         theorem, tp)

UNIT_ID = "HS-MATH1-U02"

OPT = ["必要十分条件である", "必要条件であるが十分条件ではない", "十分条件であるが必要条件ではない", "必要条件でも十分条件でもない"]


def opt_of(pq, qp):
    """p⇒q（十分）と q⇒p（必要）の真偽から選択肢を返す。"""
    return {(True, True): OPT[0], (False, True): OPT[1], (True, False): OPT[2], (False, False): OPT[3]}[(pq, qp)]


def opt_flags(o):
    return {OPT[0]: (True, True), OPT[1]: (False, True), OPT[2]: (True, False), OPT[3]: (False, False)}[o]


def ns_why(pq, qp, ce_pq, ce_qp, wrong):
    """必要・十分の誤答選択肢の理由。"""
    wpq, wqp = opt_flags(wrong)
    parts = []
    if wpq != pq:
        parts.append("「$p\\Rightarrow q$」は" + ("真なので、$p$ は十分条件である" if pq else f"偽（反例：{ce_pq}）なので、$p$ は十分条件ではない"))
    if wqp != qp:
        parts.append("「$q\\Rightarrow p$」は" + ("真なので、$p$ は必要条件である" if qp else f"偽（反例：{ce_qp}）なので、$p$ は必要条件ではない"))
    mis = "必要と十分の取り違え" if (wpq, wqp) == (qp, pq) else "一方の向きの真偽の判定の誤り"
    return ("。".join(parts) + "。", mis)


def fset(xs):
    xs = sorted(xs)
    return "\\emptyset" if not xs else "\\{" + ",\\ ".join(map(str, xs)) + "\\}"


def cst(k):
    return "" if k == 0 else (f"+{k}" if k > 0 else f"{k}")


def quad0(a, b):
    """(x-a)(x-b)=0 を展開した左辺。"""
    return poly(1, -(a + b), a * b)


LESSON = lesson(
    goals=["集合の共通部分・和集合・補集合を求め、ド・モルガンの法則と要素の個数の公式を使える。",
           "命題の真偽を判定し、偽の命題には反例を挙げられる。条件を集合で表して必要条件・十分条件を判定できる。",
           "命題の逆・裏・対偶をつくり、対偶を利用した証明と背理法による証明を書ける。"],
    duration=100,
    readiness=["中学で学んだ「仮定と結論」「証明の書き方」を知っている。", "不等式の範囲を数直線上に表せる。", "倍数・約数の意味を説明できる。"],
    flow=[("導入：「ならば」の正しさ", 10, "日常の「〜ならば〜」の例で、正しい・正しくないを判定させ、反例の役割に気づかせる"),
          ("集合", 20, "集合の表し方、共通部分・和集合・補集合、ド・モルガンの法則、要素の個数（例題1）"),
          ("命題と条件", 20, "命題の真偽と反例、条件と集合の対応、条件の否定"),
          ("必要条件・十分条件", 20, "集合の包含関係で判定する（例題2）"),
          ("逆・裏・対偶", 15, "対偶の真偽が一致する理由と、対偶を利用した証明（例題3）"),
          ("背理法", 10, "$\\sqrt{2}$ が無理数であることの証明"),
          ("まとめと確認", 5, "確認問題3問、問題プリントA の課題指示")],
    sections=[
        intro("in1", "「ならば」はいつ正しいか",
              "「雨が降ったならば、地面がぬれる」は正しいと考えられるが、「地面がぬれているならば、雨が降った」は正しいとは限らない（打ち水をしたかもしれない）。このように、「ならば」でつながれた文の正しさは向きによって変わる。数学では、条件を満たすものの集まり（集合）を使うと、この正しさを図で判定できる。",
              bullets=["1つでも反例があれば「ならば」の文は偽である。", "条件 $p$ を満たすものの集合を $P$ とすると、「$p\\Rightarrow q$」が真であることは $P\\subset Q$ と同じである。"],
              points=[tp("日常の例を2〜3個挙げ、逆向きにすると正しくなくなる例を生徒に考えさせる。", ask="「〜ならば〜」の向きを逆にすると正しくなくなる例を挙げよ。", expect="「正三角形ならば二等辺三角形」の逆。", timing="導入の冒頭"),
                      tp("反例は「仮定を満たし、結論を満たさないもの」であることを最初にはっきり言葉で示す。", caution="仮定を満たさない例を反例として挙げる誤りが多い。")]),
        definition("df1", "集合の演算",
                   "集合 $A,\\ B$ について、$A$ と $B$ の両方に属する要素全体を共通部分 $A\\cap B$、少なくとも一方に属する要素全体を和集合 $A\\cup B$ という。全体集合 $U$ の要素のうち $A$ に属さないもの全体を $A$ の補集合 $\\overline{A}$ という。",
                   formula="$$A\\cap B=\\{x\\mid x\\in A\\ \\text{かつ}\\ x\\in B\\},\\quad A\\cup B=\\{x\\mid x\\in A\\ \\text{または}\\ x\\in B\\}$$",
                   conditions=["$A$ のすべての要素が $B$ の要素であるとき、$A\\subset B$（$A$ は $B$ の部分集合）", "要素をもたない集合を空集合といい、$\\emptyset$ で表す"],
                   points=[tp("ベン図を必ずかき、$A\\cap B$、$A\\cup B$、$\\overline{A}$ を塗り分けて確認させる。")]),
        theorem("th1", "ド・モルガンの法則と要素の個数",
                "$$\\overline{A\\cup B}=\\overline{A}\\cap\\overline{B},\\qquad \\overline{A\\cap B}=\\overline{A}\\cup\\overline{B},\\qquad n(A\\cup B)=n(A)+n(B)-n(A\\cap B)$$",
                ["要素の個数の公式は、$A,\\ B$ が有限集合のときに使う", "$A\\cap B=\\emptyset$ のときは $n(A\\cup B)=n(A)+n(B)$"],
                proof=["$x\\in\\overline{A\\cup B}$ とは、「$x\\in A$ または $x\\in B$」ではないこと、すなわち「$x\\notin A$ かつ $x\\notin B$」である。",
                       "これは $x\\in\\overline{A}\\cap\\overline{B}$ と同じ意味なので、$\\overline{A\\cup B}=\\overline{A}\\cap\\overline{B}$。2つ目も同様に示せる。",
                       "$n(A)+n(B)$ では、$A\\cap B$ の要素を2回数えている。",
                       "そこで1回分の $n(A\\cap B)$ を引くと、$A\\cup B$ の要素をちょうど1回ずつ数えたことになる。"],
                points=[tp("ド・モルガンの法則は「全体に線を引くと、$\\cup$ と $\\cap$ が入れかわる」と言語化させる。", ask="$\\overline{A\\cap B}$ は $\\overline{A}\\cap\\overline{B}$ と等しいか。", expect="等しくない。$\\overline{A}\\cup\\overline{B}$ と等しい。")]),
        definition("df2", "命題・条件と必要条件・十分条件",
                   "正しいか正しくないかが定まる文や式を命題という。2つの条件 $p,\\ q$ について、命題「$p\\Rightarrow q$」が真であるとき、$p$ は $q$ であるための十分条件、$q$ は $p$ であるための必要条件という。「$p\\Rightarrow q$」と「$q\\Rightarrow p$」がともに真のとき、$p$ は $q$ であるための必要十分条件である（$p\\iff q$）。",
                   formula="$$p\\Rightarrow q\\ \\text{が真}\\iff P\\subset Q\\quad(P,\\ Q\\ \\text{はそれぞれ}\\ p,\\ q\\ \\text{を満たすもの全体の集合})$$",
                   conditions=["矢印の出発点にある方が十分条件、矢印の先にある方が必要条件", "偽であることを示すには反例を1つ挙げればよい", "条件の否定：「$p$ かつ $q$」の否定は「$\\overline{p}$ または $\\overline{q}$」"],
                   points=[tp("「$p\\Rightarrow q$」の矢印をかき、「十分 → 必要」の向きを図で覚えさせる。", caution="必要と十分を逆に答える誤りが最も多い。"),
                           tp("集合 $P$ が $Q$ に含まれる図を見せ、「小さい方が十分条件、大きい方が必要条件」と確認させる。")]),
        theorem("th2", "対偶の真偽",
                "$$p\\Rightarrow q\\ \\text{が真}\\iff \\overline{q}\\Rightarrow\\overline{p}\\ \\text{が真}$$",
                ["逆「$q\\Rightarrow p$」、裏「$\\overline{p}\\Rightarrow\\overline{q}$」の真偽は、もとの命題と一致するとは限らない", "逆と裏は互いに対偶なので、真偽が一致する"],
                proof=["「$p\\Rightarrow q$」が真であることは $P\\subset Q$ と同値である。", "$P\\subset Q$ のとき、$Q$ の外側にある要素は $P$ の外側にもある。すなわち $\\overline{Q}\\subset\\overline{P}$。",
                       "逆に $\\overline{Q}\\subset\\overline{P}$ なら、同じ理由で $P\\subset Q$。", "$\\overline{Q}\\subset\\overline{P}$ は「$\\overline{q}\\Rightarrow\\overline{p}$」が真であることと同値。よって両者の真偽は一致する。"],
                points=[tp("ベン図で $P\\subset Q$ をかき、外側（補集合）どうしの包含関係が逆向きになることを示す。", timing="対偶の導入時")]),
        proof("pf1", "背理法：$\\sqrt{2}$ は無理数である",
              ["$\\sqrt{2}$ が有理数であると仮定すると、1以外に正の公約数をもたない自然数 $m,\\ n$ を用いて $\\sqrt{2}=\\dfrac{m}{n}$ と表せる。",
               "両辺を2乗して分母を払うと $m^2=2n^2$。よって $m^2$ は偶数であり、$m$ も偶数である（$m$ が奇数なら $m^2$ も奇数になるから）。",
               "$m=2k$（$k$ は自然数）とおくと $4k^2=2n^2$、すなわち $n^2=2k^2$。よって $n$ も偶数である。",
               "$m,\\ n$ がともに偶数となり、1以外に正の公約数をもたないことに矛盾する。したがって $\\sqrt{2}$ は無理数である。"],
              body="背理法は「結論を否定して仮定すると矛盾が生じる」ことを示す証明法である。結論が「〜でない」の形のとき（無理数である＝有理数でない）に特に有効である。",
              points=[tp("最初の仮定「既約分数で表せる」が、最後の矛盾の相手になっていることを矢印で板書して示す。", ask="最後に出てきた矛盾は、どの仮定と食い違っているか。", expect="$m,\\ n$ が1以外に公約数をもたないこと。")]),
        example("ex1", "例題1　倍数の個数",
                "1から100までの整数のうち、2または3で割り切れる数の個数を求めよ。",
                ["2の倍数の集合を $A$、3の倍数の集合を $B$ とする。$n(A)=50$、$n(B)=33$。", "$A\\cap B$ は6の倍数の集合で、$100\\div6=16$ 余り $4$ より $n(A\\cap B)=16$。",
                 "$n(A\\cup B)=50+33-16=67$。"],
                "$67$ 個",
                thinking="「または」は和集合。2回数えた6の倍数を引く。",
                points=[tp("6の倍数を引く理由を、ベン図の重なりを指して説明させる。")],
                misconceptions=[("$50+33=83$ 個とする", "6の倍数を2回数えているので、$n(A\\cap B)=16$ を引く")]),
        example("ex2", "例題2　必要条件・十分条件",
                "実数 $x$ について、$p$：$|x-1|<2$、$q$：$x<4$ とする。$p$ は $q$ であるための何条件か。",
                ["$P=\\{x\\mid -1<x<3\\}$、$Q=\\{x\\mid x<4\\}$。", "$P\\subset Q$ なので「$p\\Rightarrow q$」は真。", "$x=-5$ は $q$ を満たすが $p$ を満たさないので「$q\\Rightarrow p$」は偽。"],
                "十分条件であるが必要条件ではない",
                thinking="条件を集合（数直線上の範囲）に直し、どちらがどちらに含まれるかを見る。",
                points=[tp("数直線上に $P,\\ Q$ を上下にずらしてかき、包含関係を目で確かめさせる。")]),
        example("ex3", "例題3　対偶を利用した証明",
                "整数 $n$ について、$n^2$ が奇数ならば $n$ は奇数であることを証明せよ。",
                ["対偶「$n$ が偶数ならば $n^2$ は偶数」を示す。", "$n$ が偶数のとき、整数 $k$ を用いて $n=2k$ と表せる。", "$n^2=4k^2=2\\cdot2k^2$ で、$2k^2$ は整数なので $n^2$ は偶数。",
                 "対偶が真なので、もとの命題も真である。"],
                "（証明は手順のとおり）",
                thinking="「$n^2$ が奇数」から $n$ について直接言うのは難しい。$n$ についての条件から $n^2$ を調べる向き（対偶）なら計算できる。",
                points=[tp("答案の最初に「対偶を示す」と宣言し、最後に「対偶が真なのでもとの命題も真」と結ぶ形を徹底させる。")]),
        board("bd1", "板書案",
              [("① 集合", ["$A\\cap B$：かつ　$A\\cup B$：または", "$\\overline{A\\cup B}=\\overline{A}\\cap\\overline{B}$", "$n(A\\cup B)=n(A)+n(B)-n(A\\cap B)$", "例：$50+33-16=67$"]),
               ("② 必要・十分", ["$p\\Rightarrow q$ 真 $\\iff P\\subset Q$", "$p$：十分条件　$q$：必要条件", "偽 → 反例を1つ", "例題2：$P\\subset Q$ → 十分"]),
               ("③ 対偶・背理法", ["逆 $q\\Rightarrow p$　裏 $\\overline{p}\\Rightarrow\\overline{q}$", "対偶 $\\overline{q}\\Rightarrow\\overline{p}$（真偽一致）", "背理法：結論を否定 → 矛盾", "$\\sqrt{2}=\\dfrac{m}{n}$ → $m,\\ n$ ともに偶数"])],
              points=[tp("板書の②では、集合の包含図と矢印を並べてかき、十分・必要の位置関係を対応させる。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("反例を挙げる問題では、「仮定を満たすか」「結論を満たさないか」の2点を答案に明記させる。"),
               tp("条件の否定では「かつ」と「または」、「すべて」と「ある」が入れかわることを、ド・モルガンの法則と結びつけて説明する。", ask="「$x>0$ かつ $y>0$」の否定は何か。", expect="「$x\\leqq0$ または $y\\leqq0$」"),
               tp("$>$ の否定は $\\leqq$（$<$ ではない）ことを、数直線の境界の点で確認させる。", caution="$x>2$ の否定を $x<2$ とする誤りが多い。"),
               tp("背理法の答案では「〜と仮定する」「これは矛盾である」「したがって〜」の3つの言葉を必ず書かせる。", timing="背理法の演習中"),
               tp("逆が真であることを、もとの命題が真である根拠に使う誤り（逆と対偶の混同）を、問題プリントDで取り上げる。")],
              misconceptions=[("「$x=1\\Rightarrow x^2=1$」が真なので、$x=1$ は $x^2=1$ であるための必要条件", "矢印の出発点の $x=1$ は十分条件"),
                              ("「すべての $x$ で $P$」の否定を「すべての $x$ で $P$ でない」とする", "否定は「ある $x$ で $P$ でない」"),
                              ("$\\overline{A\\cap B}=\\overline{A}\\cap\\overline{B}$", "$\\overline{A\\cap B}=\\overline{A}\\cup\\overline{B}$")]),
        summary("sm1", "まとめ",
                ["$n(A\\cup B)=n(A)+n(B)-n(A\\cap B)$。補集合はド・モルガンの法則で $\\cup$ と $\\cap$ が入れかわる。",
                 "「$p\\Rightarrow q$」が真 $\\iff P\\subset Q$。出発点が十分条件、矢印の先が必要条件。偽は反例1つで示す。",
                 "対偶はもとの命題と真偽が一致する。直接示しにくいときは対偶や背理法を使う。"]),
        check("ck1", "確認問題",
              [("1から50までの整数のうち、3でも5でも割り切れない数の個数を求めよ。", "$n(A\\cup B)=16+10-3=23$ より $50-23=27$ 個"),
               ("実数 $x$ について、$x^2=9$ は $x=3$ であるための何条件か。", "必要条件であるが十分条件ではない（反例 $x=-3$）"),
               ("命題「$x>2$ ならば $x>1$」の対偶を答えよ。", "「$x\\leqq1$ ならば $x\\leqq2$」")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

SET_OPS = ["A\\cap B", "A\\cup B", "\\overline{A}\\cap B", "A\\cap\\overline{B}", "\\overline{A\\cup B}"]


@gen("basic_check", 5, ["computation", "concept"])
def set_ops(r):
    N = r.randint(10, 20)
    p, q = r.sample([2, 3, 4, 5, 6], 2)
    A = {x for x in range(1, N + 1) if x % p == 0}
    B = {x for x in range(1, N + 1) if x % q == 0}
    U = set(range(1, N + 1))
    op = r.choice(SET_OPS)
    res = {"A\\cap B": A & B, "A\\cup B": A | B, "\\overline{A}\\cap B": (U - A) & B, "A\\cap\\overline{B}": A & (U - B), "\\overline{A\\cup B}": U - (A | B)}[op]
    l = p * q // gcd(p, q)
    fp, fq, fl = f"floor({N}/{p})", f"floor({N}/{q})", f"floor({N}/{l})"
    cnt_py = {"A\\cap B": fl, "A\\cup B": f"{fp}+{fq}-{fl}", "\\overline{A}\\cap B": f"{fq}-{fl}", "A\\cap\\overline{B}": f"{fp}-{fl}", "\\overline{A\\cup B}": f"{N}-({fp}+{fq}-{fl})"}[op]
    how = {"A\\cap B": "$A$ と $B$ の両方に属する要素を選ぶ。", "A\\cup B": "$A$ と $B$ の少なくとも一方に属する要素を、重複しないように並べる。",
           "\\overline{A}\\cap B": "$B$ の要素のうち、$A$ に属さないものを選ぶ。", "A\\cap\\overline{B}": "$A$ の要素のうち、$B$ に属さないものを選ぶ。",
           "\\overline{A\\cup B}": "$U$ の要素のうち、$A$ にも $B$ にも属さないものを選ぶ（ド・モルガンの法則より $\\overline{A}\\cap\\overline{B}$ と同じ）。"}[op]
    return sa(f"$U=\\{{1,\\ 2,\\ 3,\\ \\cdots,\\ {N}\\}}$ を全体集合とし、その部分集合を $A={fset(A)}$、$B={fset(B)}$ とする。集合 ${op}$ を、要素を書き並べる方法で表しなさい。",
              f"${fset(res)}$", how + f"${op}={fset(res)}$。", d=1 if op in SET_OPS[:2] else 2,
              ap="記号の意味（$\\cap$：かつ、$\\cup$：または、上線：補集合）を確認し、ベン図に要素を書きこんでから読み取る。",
              steps=[f"ベン図をかき、$A\\cap B={fset(A & B)}$ を重なりの部分に書く。", how, f"${op}={fset(res)}$。"],
              alt=[f"$A$ は ${p}$ の倍数、$B$ は ${q}$ の倍数の集合なので、要素の個数を倍数の個数から計算し（${len(res)}$ 個）、書き並べた個数と一致するか確かめる。"],
              pc=[("記号の意味を正しく読み取っている", 1), ("要素をもれなく正しく書き並べている", 1)],
              pit=["$\\cap$ と $\\cup$ を取り違える。", "補集合を全体集合 $U$ ではなく $A\\cup B$ の中で考えてしまう。"],
              chk=(cnt_py, str(len(res)), None, "intermediate"))


@gen("basic_check", 4, ["computation"])
def set_count(r):
    N = r.choice([50, 60, 80, 100, 120, 150, 200])
    p, q = r.sample([2, 3, 4, 5, 6, 7, 9], 2)
    while p % q == 0 or q % p == 0:
        p, q = r.sample([2, 3, 4, 5, 6, 7, 9], 2)
    l = p * q // gcd(p, q)
    np_, nq, nl = N // p, N // q, N // l
    ask = r.choice(["or", "neither", "only", "and"])
    val = {"or": np_ + nq - nl, "neither": N - (np_ + nq - nl), "only": np_ - nl, "and": nl}[ask]
    q_txt = {"or": f"${p}$ または ${q}$ で割り切れる数", "neither": f"${p}$ でも ${q}$ でも割り切れない数",
             "only": f"${p}$ で割り切れるが ${q}$ では割り切れない数", "and": f"${p}$ でも ${q}$ でも割り切れる数"}[ask]
    py = {"or": f"floor({N}/{p})+floor({N}/{q})-floor({N}/{l})", "neither": f"{N}-(floor({N}/{p})+floor({N}/{q})-floor({N}/{l}))",
          "only": f"floor({N}/{p})-floor({N}/{l})", "and": f"floor({N}/{l})"}[ask]
    last = {"or": f"$n(A\\cup B)={np_}+{nq}-{nl}={val}$。", "neither": f"$n(\\overline{{A\\cup B}})={N}-({np_}+{nq}-{nl})={val}$。",
            "only": f"$n(A\\cap\\overline{{B}})=n(A)-n(A\\cap B)={np_}-{nl}={val}$。", "and": f"$n(A\\cap B)={val}$。"}[ask]
    return num(f"1から{N}までの整数のうち、{q_txt}は何個あるか求めなさい。", str(val), last, d=2,
               ap=f"${p}$ の倍数の集合を $A$、${q}$ の倍数の集合を $B$ とおき、求める集合を $A,\\ B$ と記号で表してから個数の公式を使う。両方で割り切れる数は ${p}$ と ${q}$ の最小公倍数 ${l}$ の倍数である。",
               steps=[f"$n(A)={np_}$、$n(B)={nq}$。", f"$A\\cap B$ は ${l}$ の倍数の集合で、$n(A\\cap B)={nl}$。", last],
               alt=["ベン図の4つの部分（$A$ だけ、$B$ だけ、両方、どちらでもない）の個数をすべて書きこみ、合計が " + str(N) + " になることを確かめる。"],
               pc=[("$n(A),\\ n(B),\\ n(A\\cap B)$ を正しく求めている", 1), ("求める集合を正しく表して個数を計算している", 1)],
               pit=[f"$A\\cap B$ を ${p * q}$ の倍数としてしまう（最小公倍数は ${l}$）。" if l != p * q else "両方で割り切れる数を引き忘れる。", "割り算の商の切り捨てを誤る。"],
               chk=(py, str(val)))


def ns_template(r):
    """(p, q, p⇒q, q⇒p, p⇒q の反例, q⇒p の反例, 変数の説明)"""
    t = r.choice(["sq", "gt", "abs", "quad", "sum", "nei", "xy"])
    if t == "sq":
        a = nonzero(r, -6, 6)
        return f"$x={a}$", f"$x^2={a * a}$", True, False, None, f"$x={-a}$", "実数 $x$"
    if t == "gt":
        a, b = r.sample(range(-5, 8), 2)
        return f"$x>{a}$", f"$x>{b}$", a > b, b > a, (f"$x={b}$" if a < b else None), (f"$x={a}$" if a > b else None), "実数 $x$"
    if t == "abs":
        c, d = r.randint(-4, 4), r.randint(1, 5)
        return f"$|{poly(1, -c)}|<{d}$", f"${c - d}<x<{c + d}$", True, True, None, None, "実数 $x$"
    if t == "quad":
        a, b = r.sample(range(-5, 6), 2)
        return f"${quad0(a, b)}=0$", f"$x={a}$", False, True, f"$x={b}$", None, "実数 $x$"
    if t == "sum":
        a, b = r.randint(-3, 4), r.randint(-3, 4)
        return f"$x>{a}$ かつ $y>{b}$", f"$x+y>{a + b}$", True, False, None, f"$x={a - 1},\\ y={b + 2}$", "実数 $x,\\ y$"
    if t == "nei":
        b = r.randint(2, 6)
        a = r.randint(-b + 1, b - 1)
        return f"$x>{a}$", f"$|x|<{b}$", False, False, f"$x={b}$", f"$x={-b + 1}$", "実数 $x$"
    return "$xy=0$", "$x=0$", False, True, "$x=1,\\ y=0$", None, "実数 $x,\\ y$"


@gen("basic_check", 5, ["concept", "condition_check"])
def nec_suff(r):
    p, q, pq, qp, ce_pq, ce_qp, var = ns_template(r)
    if r.random() < 0.5:
        p, q, pq, qp, ce_pq, ce_qp = q, p, qp, pq, ce_qp, ce_pq
    right = opt_of(pq, qp)
    wrongs = [o for o in OPT if o != right]
    return mc(f"{var}に関する2つの条件 $p$：{p}、$q$：{q} について、$p$ は $q$ であるための何条件か。正しいものを選びなさい。", [right] + wrongs,
              f"「$p\\Rightarrow q$」は{'真' if pq else '偽（反例：' + ce_pq + '）'}、「$q\\Rightarrow p$」は{'真' if qp else '偽（反例：' + ce_qp + '）'}。", d=2,
              ap="「$p\\Rightarrow q$」と「$q\\Rightarrow p$」の真偽を別々に調べる。$p\\Rightarrow q$ が真なら $p$ は十分条件、$q\\Rightarrow p$ が真なら $p$ は必要条件。",
              steps=[f"「$p\\Rightarrow q$」：{'真。' if pq else '偽。反例 ' + ce_pq + ' は $p$ を満たすが $q$ を満たさない。'}",
                     f"「$q\\Rightarrow p$」：{'真。' if qp else '偽。反例 ' + ce_qp + ' は $q$ を満たすが $p$ を満たさない。'}", f"よって $p$ は $q$ であるための{right}。"],
              alt=["条件を満たすものの集合 $P,\\ Q$ を数直線（またはベン図）にかき、$P\\subset Q$ か $Q\\subset P$ かを図で判定する。"],
              pc=[("2つの向きの真偽を正しく判定している", 1), ("必要・十分を正しく対応させている", 1)],
              why={w: ns_why(pq, qp, ce_pq, ce_qp, w) for w in wrongs})


def prop_template(r):
    """(P, Q, notP, notQ, 文脈)"""
    t = r.choice(["mul", "sq", "sum", "le"])
    if t == "mul":
        m = r.choice([2, 3, 4, 5])
        k = m * r.choice([2, 3, 4])
        return f"$n$ は ${k}$ の倍数", f"$n$ は ${m}$ の倍数", f"$n$ は ${k}$ の倍数でない", f"$n$ は ${m}$ の倍数でない", "整数 $n$"
    if t == "sq":
        a = nonzero(r, -7, 7)
        return f"$x={a}$", f"$x^2={a * a}$", f"$x\\neq{a}$", f"$x^2\\neq{a * a}$", "実数 $x$"
    if t == "sum":
        a, b = r.randint(-3, 5), r.randint(-3, 5)
        return f"$x>{a}$ かつ $y>{b}$", f"$x+y>{a + b}$", f"$x\\leqq {a}$ または $y\\leqq {b}$", f"$x+y\\leqq {a + b}$", "実数 $x,\\ y$"
    a = r.randint(-5, 5)
    b = a + r.randint(1, 4)
    return f"$x\\leqq {a}$", f"$x<{b}$", f"$x>{a}$", f"$x\\geqq {b}$", "実数 $x$"


@gen("basic_check", 3, ["concept"])
def converse_inverse(r):
    P, Q, nP, nQ, ctx = prop_template(r)
    forms = {"逆": f"「{Q} ならば {P}」", "裏": f"「{nP} ならば {nQ}」", "対偶": f"「{nQ} ならば {nP}」", "否定の誤用": f"「{P} ならば {nQ}」"}
    ask = r.choice(["逆", "裏", "対偶"])
    right = forms[ask]
    wrongs = [v for k, v in forms.items() if k != ask]
    def reason(k):
        if k == "否定の誤用":
            return ("仮定はそのままで結論だけを否定したもので、逆・裏・対偶のどれでもない（もとの命題の否定とも異なる）。", "結論だけを否定すればよいという誤解")
        return (f"これはもとの命題の{k}である。{ask}は{'仮定と結論を入れかえたもの' if ask == '逆' else ('仮定と結論をそれぞれ否定したもの' if ask == '裏' else '仮定と結論を入れかえ、それぞれ否定したもの')}。", "逆・裏・対偶の定義の混同")
    return mc(f"{ctx}についての命題「{P} ならば {Q}」の{ask}として正しいものを選びなさい。", [right] + wrongs,
              f"命題「$p\\Rightarrow q$」に対して、逆は「$q\\Rightarrow p$」、裏は「$\\overline{{p}}\\Rightarrow\\overline{{q}}$」、対偶は「$\\overline{{q}}\\Rightarrow\\overline{{p}}$」。", d=2,
              ap="仮定 $p$ と結論 $q$ を確認し、定義（逆：入れかえ、裏：否定、対偶：入れかえて否定）に当てはめる。否定では「かつ」と「または」、$>$ と $\\leqq$ が入れかわる。",
              steps=[f"$p$：{P}、$q$：{Q}。", f"$\\overline{{p}}$：{nP}、$\\overline{{q}}$：{nQ}。", f"{ask}は {right}。"],
              alt=["逆・裏・対偶の関係を四角形の図（もとの命題・逆・裏・対偶を頂点に置く）にかいて確かめる。"],
              pc=[("仮定・結論とその否定を正しくつくっている", 1), ("定義に当てはめて正しく選んでいる", 1)],
              why={forms[k]: reason(k) for k in forms if k != ask})


@gen("basic_check", 3, ["concept", "condition_check"])
def negation(r):
    t = r.choice(["all", "exist", "and", "range"])
    if t == "all":
        a, b = nonzero(r, -6, 6), r.randint(-5, 8)
        f = poly(1, a, b)
        right = f"ある実数 $x$ について ${f}\\leqq 0$"
        ws = [f"すべての実数 $x$ について ${f}\\leqq 0$", f"すべての実数 $x$ について ${f}<0$", f"ある実数 $x$ について ${f}>0$"]
        stem = f"すべての実数 $x$ について ${f}>0$"
        rs = [("「すべて」を否定すると「ある」になる。「すべての $x$ で成り立たない」はより強い主張である。", "全称の否定を全称のままにする誤り"),
              ("「すべて」が「ある」に変わっていないうえ、$>$ の否定は $\\leqq$（$<$ ではない）。", "不等号の否定の誤り"),
              ("結論の不等号を否定していない。「ある $x$ について $>0$」はもとの命題が真でも偽でも成り立ちうる。", "結論の否定もれ")]
    elif t == "exist":
        k = r.choice([2, 3, 5, 6, 7, 8, 10, 12])
        right = f"すべての整数 $n$ について $n^2\\neq {k}$"
        ws = [f"ある整数 $n$ について $n^2\\neq {k}$", f"すべての整数 $n$ について $n^2={k}$", f"ある整数 $n$ について $n^2>{k}$"]
        stem = f"ある整数 $n$ について $n^2={k}$"
        rs = [("「ある」を否定すると「すべて」になる。「ある $n$ で等しくない」はもとの命題と同時に成り立ちうる。", "存在の否定を存在のままにする誤り"),
              ("「ある」を「すべて」に変えただけで、結論 $n^2=" + str(k) + "$ を否定していない。", "結論の否定もれ"),
              ("$=$ の否定は $\\neq$ であり、$>$ ではない。また「ある」も否定されていない。", "等号の否定の誤り")]
    elif t == "and":
        a, b = r.randint(-4, 5), r.randint(-4, 5)
        right = f"$x\\leqq {a}$ または $y\\leqq {b}$"
        ws = [f"$x\\leqq {a}$ かつ $y\\leqq {b}$", f"$x<{a}$ または $y<{b}$", f"$x>{a}$ または $y>{b}$"]
        stem = f"$x>{a}$ かつ $y>{b}$"
        rs = [("「かつ」の否定は「または」になる（ド・モルガンの法則）。", "かつ・またはの入れかえ忘れ"),
              ("$>$ の否定は $\\leqq$ であり、境界の値（$x=" + str(a) + "$ など）を含む。", "不等号の否定で等号を落とす誤り"),
              ("各条件を否定していない。「かつ」を「または」に変えただけである。", "条件の否定もれ")]
    else:
        a = r.randint(-5, 3)
        b = a + r.randint(2, 6)
        right = f"$x<{a}$ または ${b}<x$"
        ws = [f"$x<{a}$ かつ ${b}<x$", f"$x\\leqq {a}$ または ${b}\\leqq x$", f"${a}<x<{b}$"]
        stem = f"${a}\\leqq x\\leqq {b}$"
        rs = [("「かつ」に直すと、両方を満たす $x$ は存在しない（空集合）。否定は「または」でつなぐ。", "かつ・またはの入れかえ忘れ"),
              (f"$x={a}$ はもとの条件を満たすので、否定に含めてはいけない。", "境界の扱いの誤り"),
              ("もとの範囲の内側を表しており、否定（範囲の外側）になっていない。", "否定の意味の誤解")]
    return mc(f"「{stem}」の否定として正しいものを選びなさい。", [right] + ws, f"否定は {right}。", d=2,
              ap="「すべて」と「ある」、「かつ」と「または」を入れかえ、個々の条件を否定する（$>$ の否定は $\\leqq$）。",
              steps=["否定の規則：「すべて」と「ある」、「かつ」と「または」をそれぞれ入れかえ、$>$ は $\\leqq$ に、$=$ は $\\neq$ に変える。", f"これに従うと {right}。"],
              alt=["数直線やベン図で、もとの条件を満たす部分と満たさない部分を塗り分け、選択肢がちょうど「満たさない部分」を表すかを確かめる。"],
              pc=[("「すべて／ある」「かつ／または」を正しく入れかえている", 1), ("個々の条件を正しく否定している", 1)],
              why={w: rr for w, rr in zip(ws, rs)})


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 4, ["concept", "condition_check"])
def counterexample(r):
    t = r.choice(["sq", "quad", "abs", "mul"])
    if t == "sq":
        a = r.randint(1, 6)
        prop = f"実数 $x$ について、$x^2>{a * a}$ ならば $x>{a}$"
        right, ws = f"$x={-a - 1}$", [f"$x={a + 1}$", f"$x={a}$", "$x=0$"]
        why = {ws[0]: ("$x=" + str(a + 1) + "$ は仮定も結論も満たすので反例ではない。", "結論を満たす例を反例とする誤り"),
               ws[1]: (f"$x={a}$ は仮定 $x^2>{a * a}$ を満たさないので反例ではない。", "仮定を満たさない例を反例とする誤り"),
               ws[2]: ("$x=0$ は仮定を満たさないので反例ではない。", "仮定を満たさない例を反例とする誤り")}
        chk = (f"[({-a - 1})**2-{a * a}, {-a - 1}-{a}]", f"[{2 * a + 1}, {-2 * a - 1}]", None, "intermediate")
    elif t == "quad":
        a, b = r.sample(range(-5, 6), 2)
        prop = f"実数 $x$ について、${quad0(a, b)}=0$ ならば $x={a}$"
        cand = [a, a + b, -b, a * b, b + 1, a - 1]
        ws_v = []
        for v in cand:
            if v not in (a, b) and v not in ws_v:
                ws_v.append(v)
        ws_v = ws_v[:2]
        right, ws = f"$x={b}$", [f"$x={a}$"] + [f"$x={v}$" for v in ws_v]
        why = {ws[0]: (f"$x={a}$ は結論を満たすので反例ではない。", "結論を満たす例を反例とする誤り")}
        for v, w in zip(ws_v, ws[1:]):
            why[w] = (f"$x={v}$ を代入すると左辺は ${(v - a) * (v - b)}$ で $0$ にならず、仮定を満たさない。", "仮定を満たさない例を反例とする誤り")
        chk = (f"solve((x-({a}))*(x-({b})), x)", f"[{a}, {b}]", "set", "intermediate")
    elif t == "abs":
        a = r.randint(2, 6)
        prop = f"実数 $x$ について、$x<{a}$ ならば $|x|<{a}$"
        right, ws = f"$x={-a - 1}$", [f"$x={a - 1}$", f"$x={a + 1}$", "$x=0$"]
        why = {ws[0]: (f"$x={a - 1}$ は $|x|={a - 1}<{a}$ で結論を満たすので反例ではない。", "結論を満たす例を反例とする誤り"),
               ws[1]: (f"$x={a + 1}$ は仮定 $x<{a}$ を満たさないので反例ではない。", "仮定を満たさない例を反例とする誤り"),
               ws[2]: ("$x=0$ は結論 $|x|<" + str(a) + "$ を満たすので反例ではない。", "結論を満たす例を反例とする誤り")}
        chk = (f"Abs({-a - 1})-{a}", "1", None, "intermediate")
    else:
        m = r.choice([2, 3, 4, 5, 6])
        t1 = r.choice([1, 3, 5])
        prop = f"整数 $n$ について、$n$ が ${m}$ の倍数ならば $n$ は ${2 * m}$ の倍数"
        right = f"$n={m * t1}$"
        ws = [f"$n={2 * m * r.choice([1, 2, 3])}$", f"$n={m * t1 + 1}$", f"$n={2 * m * r.choice([4, 5])}$"]
        why = {ws[0]: ("仮定と結論をともに満たすので反例ではない。", "結論を満たす例を反例とする誤り"),
               ws[1]: (f"${m}$ の倍数ではないので仮定を満たさず、反例ではない。", "仮定を満たさない例を反例とする誤り"),
               ws[2]: ("仮定と結論をともに満たすので反例ではない。", "結論を満たす例を反例とする誤り")}
        chk = (f"[Mod({m * t1},{m}), Mod({m * t1},{2 * m})]", f"[0, {m}]", None, "intermediate")
    return mc(f"命題「{prop}」は偽である。この命題の反例になっているものを選びなさい。", [right] + ws,
              f"反例は「仮定を満たすが結論を満たさない」もの。{right} がこれに当たる。", d=3,
              ap="反例の条件は2つ：(1) 仮定を満たす、(2) 結論を満たさない。各選択肢についてこの2点を確かめる。",
              steps=["各選択肢が仮定を満たすか調べる。", "仮定を満たすもののうち、結論を満たさないものを探す。", f"{right} は仮定を満たし、結論を満たさない。"],
              alt=["仮定・結論を満たす範囲を数直線上にかき、「仮定の範囲にあって結論の範囲の外」にある値を探す。"],
              pc=[("反例の2つの条件を理解している", 2), ("正しい反例を選んでいる", 2)],
              why=why, chk=chk)


CTX = [("電車で通学している", "バスで通学している"), ("運動部に所属している", "習い事をしている"), ("数学が好きと答えた", "英語が好きと答えた"),
       ("犬を飼っている", "猫を飼っている"), ("朝食にパンを食べた", "朝食に牛乳を飲んだ")]


@gen("standard_practice", 4, ["computation", "application"])
def venn_count(r):
    ca, cb = r.choice(CTX)
    both, aonly, bonly, neither = r.randint(2, 12), r.randint(3, 15), r.randint(3, 15), r.randint(1, 10)
    N, nA, nB = both + aonly + bonly + neither, both + aonly, both + bonly
    ask = r.choice(["both", "neither", "exactly"])
    if ask == "both":
        given = f"{ca}生徒は {nA} 人、{cb}生徒は {nB} 人、どちらにも当てはまらない生徒は {neither} 人であった。両方に当てはまる生徒は何人か。"
        val, py = both, f"{nA}+{nB}-({N}-{neither})"
        st = [f"$n(A\\cup B)={N}-{neither}={N - neither}$。", f"$n(A\\cap B)=n(A)+n(B)-n(A\\cup B)={nA}+{nB}-{N - neither}={both}$。"]
    elif ask == "neither":
        given = f"{ca}生徒は {nA} 人、{cb}生徒は {nB} 人、両方に当てはまる生徒は {both} 人であった。どちらにも当てはまらない生徒は何人か。"
        val, py = neither, f"{N}-({nA}+{nB}-{both})"
        st = [f"$n(A\\cup B)={nA}+{nB}-{both}={N - neither}$。", f"$n(\\overline{{A\\cup B}})={N}-{N - neither}={neither}$。"]
    else:
        given = f"{ca}生徒は {nA} 人、{cb}生徒は {nB} 人、両方に当てはまる生徒は {both} 人であった。どちらか一方だけに当てはまる生徒は何人か。"
        val, py = aonly + bonly, f"({nA}-{both})+({nB}-{both})"
        st = [f"$A$ だけ：${nA}-{both}={aonly}$、$B$ だけ：${nB}-{both}={bonly}$。", f"合計 ${aonly}+{bonly}={val}$。"]
    return num(f"ある学年の生徒 {N} 人に調査を行ったところ、{given}（数値は架空の設定である）", str(val), " ".join(st), d=3,
               ap=f"{ca}生徒の集合を $A$、{cb}生徒の集合を $B$ とおき、ベン図の4つの部分に分けて考える。",
               steps=[f"$n(U)={N}$、$n(A)={nA}$、$n(B)={nB}$ とする。"] + st,
               alt=["ベン図の重なりの部分を $x$ 人とおき、4つの部分の人数の合計が全体の人数になるという方程式を立てて解く。"],
               pc=[("集合を設定し、与えられた人数を正しく対応させている", 2), ("公式またはベン図から正しく求めている", 2)],
               pit=["$n(A)+n(B)$ を $n(A\\cup B)$ としてしまう（重なりを2回数える）。", "「どちらにも当てはまらない」人数を全体から引き忘れる。"],
               chk=(py, str(val)))


@gen("standard_practice", 4, ["condition_check", "computation"])
def ns_param(r):
    c, d = r.randint(-3, 4), r.randint(1, 4)
    suff = r.random() < 0.5
    w = r.randint(2 * d + 1, 2 * d + 5) if suff else r.randint(1, 2 * d - 1)
    lo, hi = (c + d - w, c - d) if suff else (c - d, c + d - w)
    kind = "十分条件" if suff else "必要条件"
    incl = "P\\subset Q" if suff else "Q\\subset P"
    ans = f"${lo}\\leqq a\\leqq {hi}$" if lo < hi else f"$a={lo}$"
    cond = (f"$a\\leqq {c - d}$ かつ $a+{w}\\geqq {c + d}$" if suff else f"$a\\geqq {c - d}$ かつ $a+{w}\\leqq {c + d}$")
    return sa(f"$a$ を定数とする。実数 $x$ に関する条件 $p$：$|{poly(1, -c)}|<{d}$、$q$：$a<x<a+{w}$ について、$p$ が $q$ であるための{kind}となるような $a$ の値の範囲を求めなさい。",
              ans, f"$P=\\{{x\\mid {c - d}<x<{c + d}\\}}$、$Q=\\{{x\\mid a<x<a+{w}\\}}$。${incl}$ となる条件は {cond}。", d=3,
              ap=f"$p$ が $q$ の{kind}であることは、集合で ${incl}$ と言いかえられる。数直線に $P$ を固定してかき、$Q$ を動かして含まれる条件を端点で表す。",
              steps=[f"$|{poly(1, -c)}|<{d}$ より $P$：${c - d}<x<{c + d}$。", f"{kind}であるための条件は ${incl}$。",
                     f"端点を比べて {cond}。", f"これを解いて {ans}。"],
              alt=[f"境界の値（$a={lo}$、$a={hi}$）のときに図をかき、端点が一致しても含まれる（どちらも端点を含まない開区間なので）ことを確かめる。"],
              pc=[("$P$ を正しく求めている", 1), ("包含関係の向きを正しく判断している", 1), ("端点の条件を立てて正しく解いている", 2)],
              pit=["十分条件と必要条件で包含関係の向きを逆にする。", "端点で等号を含めてよいかの判断を誤る。"],
              chk=(f"[{c}-{d}, {c}+{d}, {lo}, {hi}]", f"[{c - d}, {c + d}, {(c + d - w) if suff else (c - d)}, {(c - d) if suff else (c + d - w)}]", None, "intermediate"))


@gen("standard_practice", 4, ["condition_check", "computation"])
def set_inclusion(r):
    c, d = r.randint(-4, 5), r.randint(2, 5)
    L = r.randint(1, 2 * d - 1)
    ask = r.choice(["sub", "empty", "meet"])
    Bset = f"\\{{x\\mid |{poly(1, -c)}|\\leqq {d}\\}}"
    Aset = f"\\{{x\\mid a\\leqq x\\leqq a+{L}\\}}"
    if ask == "sub":
        q_txt, ans = "$A\\subset B$", f"${c - d}\\leqq a\\leqq {c + d - L}$"
        st = [f"$A\\subset B$ となるのは、$A$ の左端が $B$ の左端以上、右端が $B$ の右端以下のとき：$a\\geqq {c - d}$ かつ $a+{L}\\leqq {c + d}$。", f"よって {ans}。"]
        vals = (c - d, c + d - L)
    elif ask == "empty":
        q_txt, ans = "$A\\cap B=\\emptyset$", f"$a<{c - d - L},\\ {c + d}<a$"
        st = [f"共通部分がないのは、$A$ が $B$ の完全に左にある（$a+{L}<{c - d}$）か、完全に右にある（$a>{c + d}$）とき。", f"よって {ans}。"]
        vals = (c - d - L, c + d)
    else:
        q_txt, ans = "$A\\cap B\\neq\\emptyset$", f"${c - d - L}\\leqq a\\leqq {c + d}$"
        st = ["共通部分が空集合になる場合（$A$ が $B$ の完全に左か右にある場合）を除けばよい。", f"$a+{L}<{c - d}$ または $a>{c + d}$ の否定をとり、{ans}。"]
        vals = (c - d - L, c + d)
    return sa(f"$a$ を定数とし、実数を要素とする集合 $A={Aset}$、$B={Bset}$ を考える。{q_txt} となるような $a$ の値の範囲を求めなさい。", ans,
              f"$B$ は ${c - d}\\leqq x\\leqq {c + d}$。" + st[0], d=3,
              ap="$B$ を数直線上の区間として求め、幅 $" + str(L) + "$ の区間 $A$ を左右に動かしながら、端点どうしの位置関係を不等式で表す。",
              steps=[f"$|{poly(1, -c)}|\\leqq {d}$ より $B$：${c - d}\\leqq x\\leqq {c + d}$。"] + st,
              alt=["境界の値（$a=" + str(vals[0]) + "$、$a=" + str(vals[1]) + "$）のときの図をかき、端点が重なる場合を含めるかどうかを確かめる（両方とも端点を含む閉区間）。"],
              pc=[("$B$ を正しく求めている", 1), ("端点の位置関係を正しい不等式で表している", 2), ("範囲を正しく答えている", 1)],
              pit=["端点が一致する場合を含めるかどうか（等号の有無）を誤る。", "$A\\cap B=\\emptyset$ を「かつ」でつないでしまう（左右どちらか一方でよい）。"],
              chk=(f"[{c}-{d}, {c}+{d}]", f"[{c - d}, {c + d}]", None, "intermediate"))


def truth_template(r):
    """(P, Q, もとの命題の真偽, 逆の真偽, 文脈)"""
    t = r.choice(["sq", "gt", "mul", "sum", "sqlt"])
    if t == "sq":
        a = nonzero(r, -6, 6)
        return f"$x={a}$", f"$x^2={a * a}$", True, False, "実数 $x$"
    if t == "gt":
        a, b = r.sample(range(-5, 8), 2)
        return f"$x>{a}$", f"$x>{b}$", a > b, b > a, "実数 $x$"
    if t == "mul":
        m = r.choice([2, 3, 4, 5])
        k = m * r.choice([2, 3])
        if r.random() < 0.5:
            return f"$n$ が ${k}$ の倍数", f"$n$ は ${m}$ の倍数", True, False, "整数 $n$"
        return f"$n$ が ${m}$ の倍数", f"$n$ は ${k}$ の倍数", False, True, "整数 $n$"
    if t == "sum":
        a, b = r.randint(-3, 4), r.randint(-3, 4)
        return f"$x>{a}$ かつ $y>{b}$", f"$x+y>{a + b}$", True, False, "実数 $x,\\ y$"
    a = r.randint(1, 6)
    return f"$x^2<{a * a}$", f"$x<{a}$", True, False, "実数 $x$"


@gen("standard_practice", 4, ["concept", "condition_check"])
def four_truth(r):
    P, Q, t_orig, t_conv, ctx = truth_template(r)
    labels = {"もとの命題": t_orig, "逆": t_conv, "裏": t_conv, "対偶": t_orig}
    texts = {"もとの命題": f"もとの命題「{P} ならば {Q}」", "逆": f"逆「{Q} ならば {P}」", "裏": "裏", "対偶": "対偶"}
    texts["裏"] = f"裏（もとの命題の仮定と結論をそれぞれ否定したもの）"
    texts["対偶"] = f"対偶（逆の仮定と結論をそれぞれ否定したもの）"
    correct = [texts[k] for k in labels if labels[k]]
    wrong = [texts[k] for k in labels if not labels[k]]
    tv = lambda b: "真" if b else "偽"  # noqa: E731
    reasons = {"もとの命題": ("もとの命題は偽である（仮定を満たし結論を満たさない反例が存在する）。", "真偽の判定の誤り"),
               "逆": ("逆は偽である（仮定と結論を入れかえた命題には反例が存在する）。", "真偽の判定の誤り"),
               "裏": ("裏は逆の対偶なので、逆と真偽が一致し、偽である。", "逆・裏・対偶の真偽の関係の誤解"),
               "対偶": ("対偶はもとの命題と真偽が一致するので、偽である。", "逆・裏・対偶の真偽の関係の誤解")}
    why = {texts[k]: reasons[k] for k in labels if not labels[k]}
    return ms(f"{ctx}についての命題「{P} ならば {Q}」について、もとの命題・逆・裏・対偶のうち、真であるものをすべて選びなさい。", correct, wrong,
              f"もとの命題は{tv(t_orig)}、逆は{tv(t_conv)}。対偶はもとの命題と、裏は逆と真偽が一致する。", d=3,
              ap="4つすべてを調べる必要はない。もとの命題と逆の真偽を調べれば、対偶（もとの命題と一致）と裏（逆と一致）の真偽が決まる。",
              steps=[f"もとの命題：{tv(t_orig)}。", f"逆「{Q} ならば {P}」：{tv(t_conv)}。", f"対偶は{tv(t_orig)}、裏は{tv(t_conv)}。"],
              alt=["条件を集合で表し、$P\\subset Q$（もとの命題）と $Q\\subset P$（逆）が成り立つかを数直線やベン図で確かめる。"],
              pc=[("もとの命題と逆の真偽を正しく判定している", 2), ("対偶・裏の真偽を関係から正しく判断している", 2)],
              why=why)


# ======================================================================
# C 思考力・記述応用
# ======================================================================

@gen("thinking_writing", 3, ["written_reasoning", "concept"])
def proof_contra(r):
    if r.random() < 0.5:
        k = r.choice([2, 3, 5])
        res = {2: "$n=2m+1$", 3: "$n=3m+1$ または $n=3m+2$", 5: "$n=5m+1,\\ 5m+2,\\ 5m+3,\\ 5m+4$ のいずれか"}[k]
        sq = {2: "$n^2=4m^2+4m+1=2(2m^2+2m)+1$", 3: "$n^2=3(3m^2+2m)+1$ または $n^2=3(3m^2+4m+1)+1$",
              5: "$n^2$ を5で割った余りは順に $1,\\ 4,\\ 4,\\ 1$（例：$(5m+2)^2=5(5m^2+4m)+4$）"}[k]
        stem = f"整数 $n$ について、「$n^2$ が ${k}$ の倍数ならば、$n$ は ${k}$ の倍数である」ことを、対偶を利用して証明しなさい。"
        contra = f"「$n$ が ${k}$ の倍数でないならば、$n^2$ は ${k}$ の倍数でない」"
        steps = [f"対偶{contra}を証明する。", f"$n$ が ${k}$ の倍数でないとき、整数 $m$ を用いて {res} と表せる。", f"{sq}。",
                 f"いずれの場合も $n^2$ は ${k}$ で割り切れない。よって対偶は真であり、もとの命題も真である。"]
        chk = (f"expand(({k}*m+1)**2-{k}*({k}*m**2+2*m))", "1", "expand", "intermediate")
        alt = [f"$n^2$ を ${k}$ で割った余りを、$n$ を ${k}$ で割った余りごとに表にまとめると、余りが $0$ になるのは $n$ が ${k}$ の倍数のときだけだと分かる。"]
    else:
        a = r.randint(-3, 6)
        stem = f"実数 $x,\\ y$ について、「$x+y>{2 * a}$ ならば、$x>{a}$ または $y>{a}$」であることを、対偶を利用して証明しなさい。"
        contra = f"「$x\\leqq {a}$ かつ $y\\leqq {a}$ ならば、$x+y\\leqq {2 * a}$」"
        steps = [f"結論「$x>{a}$ または $y>{a}$」の否定は「$x\\leqq {a}$ かつ $y\\leqq {a}$」、仮定の否定は「$x+y\\leqq {2 * a}$」。", f"対偶{contra}を証明する。",
                 f"$x\\leqq {a}$、$y\\leqq {a}$ の辺々を加えて $x+y\\leqq {2 * a}$。", "よって対偶は真であり、もとの命題も真である。"]
        chk = None
        alt = [f"背理法で「$x+y>{2 * a}$ かつ $x\\leqq {a}$ かつ $y\\leqq {a}$」と仮定し、辺々を加えて矛盾を導いてもよい。"]
    return desc(stem, f"対偶{contra}を示す（解答の手順を参照）。", "直接示すのが難しいので、真偽が一致する対偶を証明する。",
                rubric=[("対偶を正しくつくっている（否定の仕方が正しい）", 2), ("対偶の仮定を式で表している", 2), ("対偶の結論を正しく導いている", 3), ("「対偶が真なのでもとの命題も真」と結論を述べている", 1)],
                d=4, p=8, lines=10,
                ap="もとの命題の仮定から直接結論を導くのは難しい。対偶にすると、仮定が「〜でない」「〜以下」のような扱いやすい形になる。",
                steps=steps, alt=alt,
                pc=[("対偶の作成", 2), ("仮定の式表現", 2), ("結論の導出", 3), ("結び", 1)],
                pit=["対偶ではなく逆を証明してしまう。", "「または」の否定を「または」のままにする。", "最後に「もとの命題も真」と結論を書き忘れる。"],
                chk=chk, kind="proof")


@gen("thinking_writing", 3, ["written_reasoning", "condition_check"])
def proof_irrational(r):
    p = r.choice([2, 3, 5, 7])
    a, b = nonzero(r, -5, 5), nonzero(r, -4, 4)
    if (a, b, p) == (1, 1, 2):
        b = 2
    bterm = ("" if b == 1 else ("-" if b == -1 else str(b))) + f"\\sqrt{{{p}}}"
    num_ = f"{a}{'+' if b > 0 else ''}{bterm}"
    top, den = (f"r{cst(-a)}", b) if b > 0 else (f"{a}-r", -b)
    solved = f"\\sqrt{{{p}}}={top}" if den == 1 else f"\\sqrt{{{p}}}=\\dfrac{{{top}}}{{{den}}}"
    return desc(f"$\\sqrt{{{p}}}$ が無理数であることを用いて、${num_}$ が無理数であることを背理法によって証明しなさい。",
                f"${num_}$ が有理数 $r$ であると仮定すると、${solved}$ は有理数となり矛盾する。よって ${num_}$ は無理数である。",
                "結論を否定して有理数と仮定し、$\\sqrt{" + str(p) + "}$ について解くと、有理数の四則計算の結果が有理数になることから矛盾が生じる。",
                rubric=[("結論を否定して「有理数 $r$ である」と仮定している", 2), ("$\\sqrt{" + str(p) + "}$ について正しく解いている", 2),
                        ("右辺が有理数である理由（有理数の四則計算、$" + str(b) + "\\neq0$）を述べている", 2), ("矛盾を指摘して結論を述べている", 2)],
                d=4, p=8, lines=10,
                ap="「無理数である」は「有理数でない」ということなので、否定の「有理数である」を仮定して矛盾を導く（背理法）。",
                steps=[f"${num_}$ が有理数であると仮定し、$r$ とおく：${num_}=r$。", f"$\\sqrt{{{p}}}$ について解くと、${solved}$。",
                       f"$r$ と ${a}$ は有理数であり、有理数どうしの和・差・積・商（$0$ で割る場合を除く）は有理数なので、右辺は有理数である。", f"これは $\\sqrt{{{p}}}$ が無理数であることに矛盾する。よって ${num_}$ は無理数である。"],
                alt=["一般に「有理数 $a$、$0$ でない有理数 $b$ と無理数 $\\alpha$ について $a+b\\alpha$ は無理数」と示しておけば、同じ形の問題すべてに使える。"],
                pc=[("仮定の設定", 2), ("式変形", 2), ("有理数である理由", 2), ("矛盾と結論", 2)],
                pit=["「有理数と無理数の和は無理数だから」と、示すべきことを根拠に使ってしまう。", f"${b}$ で割るときに $0$ でないことを確認しない。"],
                chk=(f"solve({a}+({b})*x-r, x)", f"[(r-({a}))/({b})]", None, "intermediate"), kind="proof")


@gen("thinking_writing", 2, ["cross_unit", "condition_check"], rel=["HS-MATH1-U03", "HS-MATH1-U01"])
def cross_quad(r):
    target = r.choice(OPT)
    for _ in range(500):
        a = r.randint(-5, 3)
        b = a + r.randint(2, 6)
        c, d = r.randint(-5, 6), r.randint(1, 5)
        lo, hi = c - d, c + d
        pq = lo <= a and b <= hi
        qp = a <= lo and hi <= b
        if opt_of(pq, qp) == target:
            break
    right = opt_of(pq, qp)
    def pick(inside, outside):
        """inside の開区間にあり outside の開区間にない値（整数を優先）。"""
        for t in list(range(-20, 21)) + [Fraction(2 * k + 1, 2) for k in range(-20, 20)]:
            if inside[0] < t < inside[1] and not (outside[0] < t < outside[1]):
                return f"$x={t}$" if not isinstance(t, Fraction) else f"$x={frac(t.numerator, t.denominator)}$"
        return None
    ce_pq = None if pq else pick((a, b), (lo, hi))
    ce_qp = None if qp else pick((lo, hi), (a, b))
    wrongs = [o for o in OPT if o != right]
    return mc(f"実数 $x$ に関する条件 $p$：${quad0(a, b)}<0$、$q$：$|{poly(1, -c)}|<{d}$ について、$p$ は $q$ であるための何条件か。正しいものを選びなさい。",
              [right] + wrongs, f"$P=\\{{x\\mid {a}<x<{b}\\}}$、$Q=\\{{x\\mid {lo}<x<{hi}\\}}$ の包含関係から判断する。", d=4, p=8,
              ap="二次不等式（二次関数の単元）と絶対値の不等式（数と式の単元）をそれぞれ解いて集合 $P,\\ Q$ を数直線上の範囲として求め、包含関係を調べる。",
              steps=[f"${quad0(a, b)}=({poly(1, -a)})({poly(1, -b)})<0$ より $P$：${a}<x<{b}$。", f"$-{d}<{poly(1, -c)}<{d}$ より $Q$：${lo}<x<{hi}$。",
                     f"$P\\subset Q$ は{'成り立つ' if pq else '成り立たない（反例 ' + ce_pq + '）'}。$Q\\subset P$ は{'成り立つ' if qp else '成り立たない（反例 ' + ce_qp + '）'}。", f"よって{right}。"],
              alt=["2つの範囲を同じ数直線の上下にかき、端点の位置を比べる。端点がすべて一致すれば必要十分条件である。"],
              pc=[("$P$（二次不等式）を正しく解いている", 2), ("$Q$（絶対値の不等式）を正しく解いている", 2), ("包含関係から正しく判断している", 4)],
              why={w: ns_why(pq, qp, ce_pq, ce_qp, w) for w in wrongs},
              chk=(f"solve((x-({a}))*(x-({b})), x)", f"[{a}, {b}]", "set", "intermediate"))


@gen("thinking_writing", 2, ["written_reasoning", "condition_check"])
def ns_reason(r):
    t = r.choice(["sq", "gt", "quad", "abs", "both"])
    if t == "sq":
        a = r.randint(1, 7)
        p, q, pq, qp, ce = f"$x^2={a * a}$", f"$x={a}$", False, True, f"$x={-a}$"
        rq = f"「$q\\Rightarrow p$」：$x={a}$ なら $x^2={a * a}$ で真。"
        rp = f"「$p\\Rightarrow q$」：反例 {ce}（$x^2={a * a}$ を満たすが $x\\neq{a}$）があり偽。"
    elif t == "gt":
        a = r.randint(1, 6)
        p, q, pq, qp, ce = f"$x>{a}$", f"$x^2>{a * a}$", True, False, f"$x={-a - 1}$"
        rp = f"「$p\\Rightarrow q$」：$x>{a}>0$ なら両辺は正なので2乗して $x^2>{a * a}$。真。"
        rq = f"「$q\\Rightarrow p$」：反例 {ce}（$x^2={(a + 1) ** 2}>{a * a}$ だが $x<{a}$）があり偽。"
    elif t == "quad":
        a, b = r.sample(range(-5, 6), 2)
        p, q, pq, qp, ce = f"${quad0(a, b)}=0$", f"$x={a}$", False, True, f"$x={b}$"
        rp = f"「$p\\Rightarrow q$」：${quad0(a, b)}=({poly(1, -a)})({poly(1, -b)})=0$ の解は $x={a},\\ {b}$。反例 {ce} があり偽。"
        rq = f"「$q\\Rightarrow p$」：$x={a}$ を代入すると $0$ になるので真。"
    elif t == "abs":
        a = r.randint(1, 6)
        p, q, pq, qp, ce = f"$|x|<{a}$", f"$x<{a}$", True, False, f"$x={-a - 1}$"
        rp = f"「$p\\Rightarrow q$」：$|x|<{a}$ なら $-{a}<x<{a}$ なので $x<{a}$。真。"
        rq = f"「$q\\Rightarrow p$」：反例 {ce}（$x<{a}$ だが $|x|={a + 1}$）があり偽。"
    else:
        p, q, pq, qp, ce = "$x+y>0$ かつ $xy>0$", "$x>0$ かつ $y>0$", True, True, None
        rp = "「$p\\Rightarrow q$」：$xy>0$ より $x,\\ y$ は同符号。両方負なら $x+y<0$ となり矛盾するので両方正。真。"
        rq = "「$q\\Rightarrow p$」：$x>0,\\ y>0$ なら $x+y>0$、$xy>0$。真。"
    right = opt_of(pq, qp)
    var = "実数 $x,\\ y$" if t == "both" else "実数 $x$"
    return desc(f"{var}に関する条件 $p$：{p}、$q$：{q} について、$p$ は $q$ であるための何条件か。理由（偽であるものには反例）も示して答えなさい。",
                f"$p$ は $q$ であるための{right}。{rp}{rq}", f"{rp}{rq}",
                rubric=[("「$p\\Rightarrow q$」の真偽を正しく判定している", 2), ("「$q\\Rightarrow p$」の真偽を正しく判定している", 2),
                        ("真であるものには理由、偽であるものには正しい反例を示している", 2), ("必要・十分を正しく対応させて結論を述べている", 2)],
                d=4, p=8, lines=8,
                ap="2つの向きを別々に調べる。真なら理由を、偽なら「仮定を満たし結論を満たさない」反例を1つ挙げる。",
                steps=[rp, rq, f"よって $p$ は $q$ であるための{right}。"],
                alt=["条件を満たす集合 $P,\\ Q$ をかき、包含関係から結論を確かめる。"],
                pc=[("$p\\Rightarrow q$", 2), ("$q\\Rightarrow p$", 2), ("理由・反例", 2), ("結論", 2)],
                pit=["反例として、仮定を満たさない値を挙げる。", "必要と十分を逆に答える。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(stem, wrong, step, etype, tempt, fix, ans, expl, steps, ap, alt, pit, chk=None, d=3):
    return desc(f"{stem}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい答えを求めなさい。", ans, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい解答を途中式とともに示している", 3), ("最終的な答えが正しい", 1)], d=d, p=6, lines=6,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい途中式", 3), ("正しい答え", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix), chk=chk)


@gen("error_correction", 3, ["common_error", "concept"])
def err_negation(r):
    t = r.choice(["all", "and", "range", "exist"])
    if t == "all":
        a, b = nonzero(r, -6, 6), r.randint(1, 9)
        f = poly(1, a, b)
        stem, wrong, right = f"「すべての実数 $x$ について ${f}>0$」", f"すべての実数 $x$ について ${f}\\leqq 0$", f"ある実数 $x$ について ${f}\\leqq 0$"
        why = "「すべて」の否定は「ある」になる。生徒の解答は「すべての $x$ で成り立たない」という、より強い主張になっている。"
        tempt = "結論の不等号だけを否定すればよいと考え、「すべて」の部分を否定し忘れた。"
    elif t == "and":
        a, b = r.randint(-4, 6), r.randint(-4, 6)
        stem, wrong, right = f"「$x\\geqq {a}$ かつ $y\\geqq {b}$」", f"$x<{a}$ かつ $y<{b}$", f"$x<{a}$ または $y<{b}$"
        why = "ド・モルガンの法則により「かつ」の否定は「または」になる。"
        tempt = "個々の条件を否定することに注意が向き、「かつ」を「または」に変え忘れた。"
    elif t == "range":
        a = r.randint(-5, 3)
        b = a + r.randint(2, 6)
        stem, wrong, right = f"「${a}<x<{b}$」", f"${a}\\geqq x\\geqq {b}$", f"$x\\leqq {a}$ または ${b}\\leqq x$"
        why = f"「${a}<x<{b}$」は「$x>{a}$ かつ $x<{b}$」の意味なので、否定は「$x\\leqq {a}$ または $x\\geqq {b}$」。生徒の式を満たす $x$ は存在しない。"
        tempt = "不等号の向きをそれぞれ逆にすれば否定になると考え、つながった不等式のまま書いてしまった。"
    else:
        k = r.choice([2, 3, 5, 6, 7, 10])
        stem, wrong, right = f"「ある自然数 $n$ について $n^2={k}$」", f"ある自然数 $n$ について $n^2\\neq {k}$", f"すべての自然数 $n$ について $n^2\\neq {k}$"
        why = "「ある」の否定は「すべて」になる。生徒の解答は、もとの命題と同時に成り立ちうる。"
        tempt = "結論の否定だけで十分だと考え、「ある」を「すべて」に変えるのを忘れた。"
    return err_item(f"{'命題' if t in ('all', 'exist') else '条件'}{stem}の否定を答えなさい。", f"否定は「{wrong}」", "否定のつくり方", "logic", tempt,
                    f"否定は「{right}」", f"「{right}」", why,
                    ["否定の規則：「すべて」と「ある」、「かつ」と「または」をそれぞれ入れかえ、$>$ は $\\leqq$ に、$\\geqq$ は $<$ に変える。", why, f"否定は「{right}」。"],
                    "否定をつくるときは、量（すべて・ある）、つなぎ（かつ・または）、個々の条件の3か所をすべて変える。",
                    ["数直線やベン図で、もとの条件を満たす部分と満たさない部分を塗り分け、答えが「満たさない部分」全体を表しているか確かめる。"],
                    ["量やつなぎの言葉を否定し忘れる。"])


@gen("error_correction", 3, ["common_error", "condition_check"])
def err_inverse(r):
    t = r.choice(["sq", "gt", "mul", "sum"])
    if t == "sq":
        a = r.randint(1, 7)
        P, Q, nP, nQ = f"$x={a}$", f"$x^2={a * a}$", f"$x\\neq{a}$", f"$x^2\\neq{a * a}$"
        ce, ctx = f"$x={-a}$", "実数 $x$"
    elif t == "gt":
        b = r.randint(-4, 4)
        a = b + r.randint(1, 4)
        P, Q, nP, nQ = f"$x>{a}$", f"$x>{b}$", f"$x\\leqq {a}$", f"$x\\leqq {b}$"
        ce, ctx = f"$x={a}$", "実数 $x$"
    elif t == "mul":
        m = r.choice([2, 3, 5])
        k = m * r.choice([2, 3, 4])
        P, Q, nP, nQ = f"$n$ が ${k}$ の倍数", f"$n$ は ${m}$ の倍数", f"$n$ が ${k}$ の倍数でない", f"$n$ は ${m}$ の倍数でない"
        ce, ctx = f"$n={m}$", "整数 $n$"
    else:
        a, b = r.randint(-3, 4), r.randint(-3, 4)
        P, Q, nP, nQ = f"$x>{a}$ かつ $y>{b}$", f"$x+y>{a + b}$", f"$x\\leqq {a}$ または $y\\leqq {b}$", f"$x+y\\leqq {a + b}$"
        ce, ctx = f"$x={a - 1},\\ y={b + 2}$", "実数 $x,\\ y$"
    wrong = f"対偶は「{nP} ならば {nQ}」である。{ce} が反例となるので対偶は偽。よって、もとの命題も偽である。"
    return err_item(f"{ctx}についての命題「{P} ならば {Q}」の対偶をつくり、もとの命題の真偽を答えなさい。", wrong, "対偶のつくり方（裏をつくっている）", "concept",
                    "「否定する」ことだけを覚えていて、仮定と結論を入れかえることを忘れた。その結果、裏の真偽をもとの命題の真偽と誤って結びつけた。",
                    f"対偶は「{nQ} ならば {nP}」で真。よってもとの命題も真", f"対偶「{nQ} ならば {nP}」、もとの命題は真",
                    f"生徒がつくったのは裏であり、裏の真偽はもとの命題の真偽と一致するとは限らない。対偶「{nQ} ならば {nP}」は真なので、もとの命題も真である。",
                    [f"仮定 $p$：{P}、結論 $q$：{Q}。", f"対偶は $\\overline{{q}}\\Rightarrow\\overline{{p}}$：「{nQ} ならば {nP}」。", "対偶は真（もとの命題を直接確かめても真）。", "よってもとの命題は真。"],
                    "対偶は「入れかえて、否定する」。裏（否定だけ）や逆（入れかえだけ）と区別する。",
                    ["もとの命題を直接調べても真であることが確かめられる（条件を集合で表すと $P\\subset Q$）。"],
                    ["裏と対偶を混同する。", "裏や逆の真偽からもとの命題の真偽を判断する。"])


@gen("error_correction", 2, ["common_error", "concept"])
def err_nec_suff(r):
    p, q, pq, qp, ce_pq, ce_qp, var = ns_template(r)
    while pq == qp:
        p, q, pq, qp, ce_pq, ce_qp, var = ns_template(r)
    right = opt_of(pq, qp)
    swapped = opt_of(qp, pq)
    true_dir = "p\\Rightarrow q" if pq else "q\\Rightarrow p"
    wrong = f"「${true_dir}$」が真であり、逆は偽である。よって $p$ は $q$ であるための{swapped}。"
    return err_item(f"{var}に関する条件 $p$：{p}、$q$：{q} について、$p$ は $q$ であるための何条件か答えなさい。", wrong, "必要・十分の対応づけ", "concept",
                    "矢印の真偽は正しく判定できているが、「矢印の出発点が十分条件、行き先が必要条件」という対応を逆に覚えている。",
                    f"「${true_dir}$」が真なので、$p$ は{'十分条件' if pq else '必要条件'}。$p$ は $q$ であるための{right}", f"$p$ は $q$ であるための{right}",
                    f"「$p\\Rightarrow q$」が真のとき $p$ は十分条件、「$q\\Rightarrow p$」が真のとき $p$ は必要条件。",
                    [f"「$p\\Rightarrow q$」は{'真' if pq else '偽（反例 ' + str(ce_pq) + '）'}。", f"「$q\\Rightarrow p$」は{'真' if qp else '偽（反例 ' + str(ce_qp) + '）'}。", f"よって $p$ は{right}。"],
                    "集合で $P\\subset Q$ のとき、小さい方の $P$（$p$）が十分条件、大きい方の $Q$（$q$）が必要条件。",
                    ["「$p$ であれば十分 $q$ といえる」「$q$ であるためには $p$ が必要」と、言葉に当てはめて確かめる。"],
                    ["必要と十分を逆に答える。"])


@gen("error_correction", 2, ["common_error", "computation"])
def err_demorgan(r):
    N = r.choice([30, 40, 50, 60, 100])
    p, q = r.sample([2, 3, 4, 5, 6, 7], 2)
    while p % q == 0 or q % p == 0:
        p, q = r.sample([2, 3, 4, 5, 6, 7], 2)
    l = p * q // gcd(p, q)
    np_, nq, nl = N // p, N // q, N // l
    if r.random() < 0.5:
        target = "\\overline{A\\cap B}"
        right = N - nl
        wrongv = N - (np_ + nq - nl)
        wrong = f"$\\overline{{A\\cap B}}=\\overline{{A}}\\cap\\overline{{B}}=\\overline{{A\\cup B}}$ なので、$n(\\overline{{A\\cap B}})={N}-n(A\\cup B)={N}-({np_}+{nq}-{nl})={wrongv}$"
        fix = f"$\\overline{{A\\cap B}}=\\overline{{A}}\\cup\\overline{{B}}$ であり、$n(\\overline{{A\\cap B}})={N}-n(A\\cap B)={N}-{nl}={right}$"
        py = f"{N}-floor({N}/{l})"
        meaning = f"${p}$ と ${q}$ の少なくとも一方で割り切れない数"
    else:
        target = "\\overline{A}\\cup\\overline{B}"
        right = N - nl
        wrongv = N - (np_ + nq - nl)
        wrong = f"$\\overline{{A}}\\cup\\overline{{B}}=\\overline{{A\\cup B}}$ なので、${N}-({np_}+{nq}-{nl})={wrongv}$"
        fix = f"$\\overline{{A}}\\cup\\overline{{B}}=\\overline{{A\\cap B}}$ であり、${N}-{nl}={right}$"
        py = f"{N}-floor({N}/{l})"
        meaning = f"${p}$ で割り切れないか、または ${q}$ で割り切れない数"
    return err_item(f"$U=\\{{1,\\ 2,\\ \\cdots,\\ {N}\\}}$ を全体集合とし、${p}$ の倍数全体の集合を $A$、${q}$ の倍数全体の集合を $B$ とする。$n({target})$ を求めなさい。",
                    wrong, "ド・モルガンの法則の適用（$\\cap$ と $\\cup$ の入れかえ）", "logic",
                    "補集合をとると「それぞれに線を引く」ことは覚えているが、そのとき $\\cap$ と $\\cup$ が入れかわることを忘れている。",
                    fix, f"${right}$",
                    f"${target}$ は{meaning}の集合で、$A\\cap B$（${l}$ の倍数）の補集合である。",
                    [f"ド・モルガンの法則より $\\overline{{A\\cap B}}=\\overline{{A}}\\cup\\overline{{B}}$。", f"$A\\cap B$ は ${l}$ の倍数の集合で、$n(A\\cap B)={nl}$。", f"$n({target})={N}-{nl}={right}$。"],
                    "補集合の記号を分配するときは、$\\cap$ と $\\cup$ を入れかえる。ベン図で塗って確かめる。",
                    ["ベン図で $A\\cap B$ 以外の部分をすべて塗ると、$\\overline{A}$ と $\\overline{B}$ を合わせた部分（和集合）になることが分かる。"],
                    ["$\\overline{A\\cap B}=\\overline{A}\\cap\\overline{B}$ とする。"],
                    chk=(py, str(right)), d=3)


GENERATORS = [set_ops, set_count, nec_suff, converse_inverse, negation,
              counterexample, venn_count, ns_param, set_inclusion, four_truth,
              proof_contra, proof_irrational, cross_quad, ns_reason,
              err_negation, err_inverse, err_nec_suff, err_demorgan]
