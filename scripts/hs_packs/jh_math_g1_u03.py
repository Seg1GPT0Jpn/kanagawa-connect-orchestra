"""単元パック：中学1年 数学 一次方程式（等式の性質・一次方程式の解き方・比例式・方程式の利用）。

問題プリントは神奈川県公立高校入試（数学）の形式にそろえる：A・B は 1〜4 の選択か、あいう方式の数値マーク
（0 以上の整数・既約分数）。C・D も選択式（式の意味の読み取り・解の吟味・誤りの行や原因の指摘）。
"""
import math
from fractions import Fraction as Fr

from banks._common import mc, num
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, poly, summary,
                         theorem, tp)

UNIT_ID = "JH-MATH-G1-U03"

PREREQUISITES = [
    ("JH-MATH-G1-U02", "一次式の計算（分配法則でかっこをはずす、同類項をまとめる）と、数量の関係を等式で表すこと。方程式の両辺を整理する計算はこの単元の土台である。"),
    ("JH-MATH-G1-U01", "正負の数の四則計算。移項で符号が変わることや、両辺を負の数でわる計算で使う。小学校で学んだ比と比の値（$a:b$ の比の値は $\\dfrac{a}{b}$）、"
                       "速さ・時間・道のりの関係も前提とする。"),
]
EXTENSIONS = [
    ("JH-MATH-G2-U02", "連立方程式は、加減法・代入法で文字を1つ消去して、この単元の一次方程式に帰着させて解く。"),
    ("JH-MATH-G1-U04", "比例・反比例の式 $y=ax$、$y=\\dfrac{a}{x}$ で、$y$ の値から $x$ の値を求めるときに一次方程式を使う。"),
    ("JH-MATH-G3-U03", "二次方程式も「等式の性質で式を変形して解を求める」という考え方は同じで、解の吟味（問題に適するか）の手順もそのまま使う。"),
    ("HS-MATH1-U01", "高校の一次不等式は、一次方程式の解き方とほぼ同じ手順で解くが、両辺に負の数をかける（わる）と不等号の向きが変わる点が異なる。"),
]

MCQ = "として正しいものを，次の1〜4の中から1つ選び，その番号を答えなさい。"
SEL = "を，次の1〜4の中から1つ選び，その番号を答えなさい。"


def ft(x):
    x = Fr(x)
    if x.denominator == 1:
        return str(x.numerator)
    s = "-" if x < 0 else ""
    return f"{s}\\dfrac{{{abs(x.numerator)}}}{{{x.denominator}}}"


def M(x):
    return f"${ft(x)}$"


def X(x):
    return f"$x={ft(x)}$"


def lin(a, b, v="x"):
    return poly(a, b, var=v)


def lpy(a, b):
    return f"({a})*x+({b})"


def fpy(x):
    x = Fr(x)
    return str(x.numerator) if x.denominator == 1 else f"Rational({x.numerator},{x.denominator})"


def pick(correct, cands, k=4):
    ch, why = [correct], {}
    for t, rs, mi in cands:
        if t in ch:
            continue
        ch.append(t)
        why[t] = (rs, mi)
        if len(ch) == k:
            break
    if len(ch) < k:
        raise ValueError("誤答候補が足りません")
    return ch, why


def near(v, fmt=X):
    return [(fmt(Fr(v) + d), f"途中の計算で {abs(d)} だけずれている。求めた解をもとの方程式に代入して確かめれば防げる。", "計算の誤り") for d in (1, -1, 2, -2, 3, -3)]


def mark_of(v):
    v = Fr(v)
    return ("int", v.numerator) if v.denominator == 1 else ("frac", v.numerator, v.denominator)


def ans_str(v):
    v = Fr(v)
    return str(v.numerator) if v.denominator == 1 else f"{v.numerator}/{v.denominator}"


# ---------------------------------------------------------------------------
# 授業プリント
# ---------------------------------------------------------------------------

LESSON = lesson(
    goals=["等式の性質を使って一次方程式を解き、移項がどの性質にもとづくかを説明できる。",
           "かっこ・分数・小数をふくむ一次方程式や比例式を、式を整理してから解ける。",
           "文章題で数量の関係を方程式に表して解き、求めた解が問題に適しているかを確かめられる。"],
    duration=50,
    readiness=["小学校で、□を使った式の□にあてはまる数を、逆算で求めたことがある。",
               "比 $a:b$ と比の値、等しい比の意味を知っている。",
               "一次式の計算（分配法則・同類項）と、正負の数の四則計算ができる。",
               "速さ・時間・道のりの関係を使って、簡単な問題を解ける。"],
    flow=[("導入：天びんと等式", 5, "天びんがつり合う様子から、両辺に同じ操作をしても等式が成り立つことを確かめる"),
          ("等式の性質と移項", 10, "等式の性質を確認し、移項がその性質からいえることを導く"),
          ("いろいろな方程式", 12, "例題1でかっこ・分数をふくむ方程式を解く。小数の場合は10倍する"),
          ("比例式", 6, "例題2で比例式の性質 $a:b=c:d$ ならば $ad=bc$ を使う"),
          ("方程式の利用", 12, "例題3で文章題を方程式に表し、解の吟味をする"),
          ("まとめと確認", 5, "確認問題3問、問題プリントAの課題指示")],
    sections=[
        intro("in1", "天びんのつり合いと方程式",
              "天びんの左の皿に同じ重さの箱3個と 2 g のおもり、右の皿に 14 g のおもりをのせたらつり合いました。"
              "箱1個の重さを $x$ g とすると、つり合いは $3x+2=14$ という等式で表せます。両方の皿から 2 g を取り除いても、"
              "両方を3等分しても天びんはつり合ったままなので、$3x=12$、$x=4$ と箱の重さが分かります。"
              "このように、文字の値によって成り立ったり成り立たなかったりする等式を方程式といい、方程式を成り立たせる文字の値をその方程式の解といいます。",
              bullets=["方程式を解くとは、等式の性質を使って「$x=\\square$」の形に変形すること。", "求めた解は、もとの方程式に代入して確かめられる。"],
              points=[tp("天びんの図をかき、「両方から同じだけ取る」「両方を同じ数で分ける」操作で、つり合いがくずれないことを確認させる。",
                         ask="天びんのつり合いを保ったまま、箱1個の重さを知るにはどうすればよいですか。", expect="両方から 2 g を取り、残りを3等分する。",
                         timing="授業の冒頭")]),
        definition("df1", "方程式とその解",
                   "$x$ の値によって成り立ったり成り立たなかったりする等式を、$x$ についての方程式という。方程式を成り立たせる $x$ の値を方程式の解といい、解を求めることを方程式を解くという。"
                   "移項して整理すると $ax=b\\ (a\\neq0)$ の形になる方程式を一次方程式という。",
                   formula="$$3x+2=14\\quad\\text{の解は}\\quad x=4\\qquad(3\\times4+2=14)$$",
                   conditions=["$x=4$ を代入すると左辺と右辺の値が等しくなる。", "$x=3$ を代入すると左辺は $11$、右辺は $14$ で等しくないので、$3$ は解ではない。"],
                   points=[tp("「解である」とは「代入すると両辺の値が等しくなる」ことだと、言葉で言えるようにさせる。")]),
        theorem("th1", "等式の性質",
                "$$A=B\\ \\text{ならば}\\quad A+C=B+C,\\quad A-C=B-C,\\quad AC=BC,\\quad \\dfrac{A}{C}=\\dfrac{B}{C}\\ (C\\neq0)$$",
                ["等式の両辺に同じ数をたしても、両辺から同じ数をひいても、等式は成り立つ。", "等式の両辺に同じ数をかけても、両辺を $0$ でない同じ数でわっても、等式は成り立つ。",
                 "等式の両辺を入れかえても、等式は成り立つ（$A=B$ ならば $B=A$）。"],
                body="わる数が $0$ でないという条件は、$0$ でわることができないために必要である。",
                points=[tp("「$0$ でない数でわる」の条件がなぜ必要かを、$0\\times3=0\\times5$ から $3=5$ が出てしまう例で考えさせる。",
                           ask="$0\\times3=0\\times5$ は正しい等式ですか。両辺を $0$ でわってよいでしょうか。", expect="正しい等式だが、$0$ でわると $3=5$ という誤った式になるのでわってはいけない。")]),
        derivation("dv1", "移項はなぜできるのか",
                   ["方程式 $5x-3=2x+9$ の両辺に $3$ をたす（等式の性質）：$5x=2x+9+3$。",
                    "両辺から $2x$ をひく（等式の性質）：$5x-2x=9+3$。",
                    "結果を見ると、左辺の $-3$ が右辺に $+3$ として、右辺の $2x$ が左辺に $-2x$ として移っている。",
                    "このように、等式の一方の辺の項を、符号を変えて他方の辺に移すことを移項という。移項は等式の性質から導かれる操作である。",
                    "整理すると $3x=12$。両辺を $3$ でわって $x=4$。"],
                   body="移項は「符号を変えて反対側へ」という操作だが、その根拠は「両辺に同じ数をたす（ひく）」という等式の性質である。",
                   points=[tp("移項の結果だけを覚えさせず、1回は等式の性質で両辺に同じ数をたす形を書かせてから、移項の便利さに気づかせる。",
                              caution="移項したのに符号を変え忘れる誤りが最も多い。")]),
        example("ex1", "例題1　かっこ・分数をふくむ方程式",
                "(1) $2(x-3)=x+4$ を解きなさい。\n(2) $\\dfrac{x}{3}-1=\\dfrac{x}{4}$ を解きなさい。",
                ["(1) かっこをはずす：$2x-6=x+4$。移項して $2x-x=4+6$、$x=10$。",
                 "(2) 分母の最小公倍数 $12$ を両辺にかける：$4x-12=3x$（$-1$ にも $12$ をかける）。",
                 "移項して $4x-3x=12$、$x=12$。"],
                "(1) $x=10$　(2) $x=12$",
                thinking="かっこははずし、分数は両辺に分母の最小公倍数をかけて整数の係数にしてから、移項して解く。",
                points=[tp("(2) で両辺に $12$ をかけるとき、分数でない項 $-1$ にもかけることを、矢印で示す。", caution="$4x-1=3x$ としてしまう誤りが多い。")],
                misconceptions=[("$\\dfrac{x}{3}-1=\\dfrac{x}{4}$ → $4x-1=3x$", "すべての項に $12$ をかけて $4x-12=3x$")]),
        example("ex2", "例題2　比例式",
                "比例式 $x:6=4:3$ を満たす $x$ の値を求めなさい。",
                ["比例式の性質 $a:b=c:d$ ならば $ad=bc$ を使う：$x\\times3=6\\times4$。", "$3x=24$、$x=8$。"],
                "$x=8$",
                thinking="比の値が等しいことから $\\dfrac{x}{6}=\\dfrac{4}{3}$。両辺に $6$ をかけても同じ結果になる。",
                points=[tp("$a:b=c:d$ ならば $ad=bc$ となる理由を、比の値 $\\dfrac{a}{b}=\\dfrac{c}{d}$ の両辺に $bd$ をかけて説明する。")]),
        example("ex3", "例題3　方程式の利用（過不足）",
                "何人かの生徒に鉛筆を配る。1人に3本ずつ配ると8本余り、1人に5本ずつ配ると4本たりない。生徒の人数を求めなさい。",
                ["生徒の人数を $x$ 人とする。鉛筆の本数を2通りに表す：$3x+8$（本）、$5x-4$（本）。",
                 "鉛筆の本数は等しいので $3x+8=5x-4$。",
                 "移項して $-2x=-12$、$x=6$。",
                 "解の吟味：人数は自然数で、$6$ は問題に適する（鉛筆は $26$ 本）。"],
                "$6$ 人",
                thinking="何を $x$ にするかを決め、同じ数量（鉛筆の本数）を2通りに表して等号で結ぶ。",
                points=[tp("答えを出したら、問題の条件（人数は自然数、本数は正など）に合うかを必ず確かめさせる（解の吟味）。",
                           ask="もし解が $x=6.5$ だったら、答えは何人と書けばよいですか。", expect="人数は自然数なので、問題に適する答えはない。")]),
        board("bd1", "板書案",
              [("① 等式の性質と移項", ["$A=B$ → $A\\pm C=B\\pm C$", "$AC=BC$、$\\dfrac{A}{C}=\\dfrac{B}{C}\\ (C\\neq0)$", "移項：符号を変えて反対の辺へ", "$5x-3=2x+9$ → $3x=12$ → $x=4$"]),
               ("② いろいろな方程式", ["かっこ → はずす", "分数 → 分母の最小公倍数をかける（全部の項に）", "小数 → 10倍、100倍", "比例式：$a:b=c:d$ → $ad=bc$"]),
               ("③ 方程式の利用", ["① $x$ を決める", "② 同じ数量を2通りに表す", "③ 方程式を解く", "④ 解の吟味（問題に合うか）"])],
              points=[tp("③の4つの手順は、文章題のたびに板書の同じ位置に掲示し、手順を意識させる。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("解いたら必ず代入して確かめる習慣をつけさせる。入試形式の選択問題でも、選んだ解を代入すれば正誤を自分で判断できる。", timing="例題1の後"),
               tp("分数・小数の係数をふくむ方程式では、「すべての項に同じ数をかける」ことを強調する。", caution="定数項へのかけ忘れが多い。"),
               tp("式の計算（分母は残す）と方程式（分母をはらってよい）の違いを、等号の有無で区別させる。",
                  ask="$\\dfrac{x}{2}+\\dfrac{x}{3}$ の計算で、6をかけて $3x+2x$ にしてよいですか。", expect="等式ではないので、かけてはいけない。"),
               tp("文章題では、「何を $x$ とするか」によって方程式の形が変わることを、2通りの立式で比べさせる。"),
               tp("解の吟味で、解が分数や負の数になったときの意味（問題に適さない／「−3年後」は「3年前」）を考えさせる。")],
              misconceptions=[("$3x+5=17$ → $3x=17+5$", "移項すると符号が変わるので $3x=17-5$"),
                              ("$x:4=6:3$ → $6x=12$", "外項の積＝内項の積なので $3x=24$"),
                              ("$-2x=8$ → $x=4$", "両辺を $-2$ でわって $x=-4$")]),
        summary("sm1", "まとめ",
                ["等式の性質：両辺に同じ数をたす・ひく・かける・$0$ でない同じ数でわる。移項はこの性質から導かれる。",
                 "かっこははずし、分数・小数は両辺に同じ数をかけて整数の係数にしてから解く。",
                 "比例式 $a:b=c:d$ ならば $ad=bc$。",
                 "文章題は「$x$ を決める → 同じ数量を2通りに表す → 解く → 解の吟味」の順に進める。"]),
        check("ck1", "確認問題",
              [("$4x-7=x+5$ を解きなさい。", "$3x=12$ より $x=4$"),
               ("$0.2x+0.5=0.7$ を解きなさい。", "両辺を10倍して $2x+5=7$、$x=1$"),
               ("$5:x=2:6$ を満たす $x$ を求めなさい。", "$2x=30$ より $x=15$")]),
    ])


def eq_tex(a, b, c, d):
    return f"{lin(a, b)}={lin(c, d)}"


# ======================================================================
# A 基本確認
# ======================================================================

@gen("basic_check", 5, ["computation"])
def a_solve(r):
    while True:
        x0 = r.choice([v for v in range(-9, 10) if v != 0])
        a, c = r.sample([-5, -4, -3, -2, 1, 2, 3, 4, 5, 6, 7], 2)
        b = r.randint(-12, 12)
        d = (a - c) * x0 + b
        if abs(d) <= 40 and b != 0 and d != 0:
            break
    eq = eq_tex(a, b, c, d)
    common = dict(ap="$x$ をふくむ項を左辺に、数の項を右辺に移項し（符号を変える）、$ax=b$ の形にしてから両辺を $x$ の係数でわる。",
                  steps=[f"移項する：${lin(a, 0)}{lin(-c, 0) if -c < 0 else '+' + lin(-c, 0)}={d}{-b:+d}$。", f"整理する：${lin(a - c, 0)}={d - b}$。", f"両辺を ${a - c}$ でわって $x={x0}$。"],
                  alt=[f"$x={x0}$ をもとの方程式に代入すると、左辺 ${a * x0 + b}$、右辺 ${c * x0 + d}$ で等しいので解であると確かめられる。"],
                  pc=[("正しく移項している", 1), ("正しい解を求めている", 1)],
                  pit=["移項するときに符号を変え忘れる。", "最後に $x$ の係数でわるとき、符号を誤る。"])
    if x0 > 0 and r.random() < 0.5:
        return num(f"方程式 ${eq}$ を解きなさい。", str(x0), f"移項して ${lin(a - c, 0)}={d - b}$、$x={x0}$。", d=1, mark=("int", x0),
                   chk=(f"solve(Eq({lpy(a, b)}, {lpy(c, d)}), x)[0]", str(x0)), **common)
    cands = [(X(Fr(d + b, a - c)), "数の項を移項するときに符号を変えていない。", "移項の符号の誤り"),
             (X(Fr(a - c, d - b)), "$ax=b$ から $x=\\dfrac{a}{b}$ としている。両辺を $x$ の係数でわるので $x=\\dfrac{b}{a}$。", "わる向きの誤り"),
             (X(-x0), "最後に係数でわるときに符号を誤っている。", "除法の符号の誤り"),
             (X(Fr(d - b, a + c)), "$x$ の項を移項するときに符号を変えていない。", "移項の符号の誤り")] + near(x0)
    ch, why = pick(X(x0), cands)
    return mc(f"方程式 ${eq}$ の解{MCQ}", ch, f"移項して ${lin(a - c, 0)}={d - b}$、$x={x0}$。", d=1, why=why,
              chk=(f"solve(Eq({lpy(a, b)}, {lpy(c, d)}), x)[0]", str(x0)), **common)


PROPS = ["たした", "ひいた", "かけた", "わった"]


@gen("basic_check", 4, ["concept", "condition_check"])
def a_property(r):
    k = r.randint(2, 9)
    m = r.randint(1, 9)
    kind = r.choice(PROPS)
    if kind == "たした":
        before, after = f"x-{k}={m}", f"x={m + k}"
    elif kind == "ひいた":
        before, after = f"x+{k}={m + k + r.randint(0, 5)}", None
        after = f"x={int(before.split('=')[1]) - k}"
    elif kind == "かけた":
        before, after = f"\\dfrac{{x}}{{{k}}}={m}", f"x={m * k}"
    else:
        before, after = f"{k}x={k * m}", f"x={m}"
    texts = {"たした": f"等式の両辺に ${k}$ をたしても，等式は成り立つ。", "ひいた": f"等式の両辺から ${k}$ をひいても，等式は成り立つ。",
             "かけた": f"等式の両辺に ${k}$ をかけても，等式は成り立つ。", "わった": f"等式の両辺を ${k}$ でわっても，等式は成り立つ。"}
    right = texts[kind]
    why = {}
    for o in PROPS:
        if o == kind:
            continue
        why[texts[o]] = (f"この性質を使うと ${before}$ は ${after}$ にならない。${before}$ から ${after}$ へは、両辺に同じ操作をして $x$ だけを残している。", "等式の性質の取り違え")
    ch = [right] + [texts[o] for o in PROPS if o != kind]
    return mc(f"方程式 ${before}$ を ${after}$ と変形した。このとき使った等式の性質として最も適するもの{SEL}", ch,
              f"左辺を $x$ だけにするには、" + {"たした": f"両辺に ${k}$ をたせ", "ひいた": f"両辺から ${k}$ をひけ", "かけた": f"両辺に ${k}$ をかけれ", "わった": f"両辺を ${k}$ でわれ"}[kind] + "ばよい。", d=2,
              ap="左辺の $x$ についている数（$+k$、$-k$、$\\times k$、$\\div k$）を消すには、その逆の操作を両辺にする。",
              steps=[f"左辺 ${before.split('=')[0]}$ で、$x$ にどんな操作がされているかを見る。", "その逆の操作を両辺に行えば $x$ だけが残る。", f"使った性質は「{right}」。"],
              alt=["選んだ性質で実際に両辺を変形し、" + f"${after}$" + " になるかを確かめる。"],
              pc=[("$x$ にされている操作を読み取っている", 1), ("正しい性質を選んでいる", 1)],
              pit=["$x-k$ の $-k$ を消すのに、両辺から $k$ をひいてしまう。", "わる数とかける数を取り違える。"],
              why=why)


@gen("basic_check", 4, ["computation", "common_error"])
def a_paren(r):
    while True:
        k = r.choice([2, 3, 4, 5, -2, -3])
        p = r.choice([-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        c = r.choice([1, 2, 3, -1, -2])
        x0 = r.choice([v for v in range(-8, 9) if v != 0])
        if k == c:
            continue
        d = k * (x0 + p) - c * x0
        if abs(d) <= 30:
            break
    kt = "-" if k == -1 else str(k)
    eq = f"{kt}({lin(1, p)})={lin(c, d)}"
    cands = [(X(Fr(d - p, k - c)), f"かっこをはずすとき、${k}$ を ${p}$ にかけ忘れている。", "分配法則のかけ忘れ"),
             (X(Fr(d + k * p, k - c)), "かっこをはずしたあと、数の項を移項するときの符号を誤っている。", "移項の符号の誤り"),
             (X(-x0), "最後に係数でわるときに符号を誤っている。", "除法の符号の誤り")] + near(x0)
    ch, why = pick(X(x0), cands)
    common = dict(ap="まずかっこをはずし（かっこの前の数をすべての項にかける）、次に移項して $ax=b$ の形にする。",
                  steps=[f"かっこをはずす：${lin(k, k * p)}={lin(c, d)}$。", f"移項して整理：${lin(k - c, 0)}={d - k * p}$。", f"$x={x0}$。"],
                  alt=[f"$x={x0}$ を代入：左辺 ${kt}({x0}{p:+d})={k * (x0 + p)}$、右辺 ${c * x0 + d}$ で一致する。"],
                  pc=[("かっこを正しくはずしている", 1), ("正しい解を求めている", 1)],
                  pit=["かっこの中の2つ目の項にかけ忘れる。", "負の数をかけるときに符号を変え忘れる。"])
    if x0 > 0 and r.random() < 0.4:
        return num(f"方程式 ${eq}$ を解きなさい。", str(x0), f"かっこをはずして ${lin(k, k * p)}={lin(c, d)}$、$x={x0}$。", d=2, mark=("int", x0),
                   chk=(f"solve(Eq({k}*(x+({p})), {lpy(c, d)}), x)[0]", str(x0)), **common)
    return mc(f"方程式 ${eq}$ の解{MCQ}", ch, f"かっこをはずして ${lin(k, k * p)}={lin(c, d)}$、移項して ${lin(k - c, 0)}={d - k * p}$、$x={x0}$。", d=2, why=why,
              chk=(f"solve(Eq({k}*(x+({p})), {lpy(c, d)}), x)[0]", str(x0)), **common)


@gen("basic_check", 4, ["computation", "concept"])
def a_proportion(r):
    form = r.choice(["xa", "ax", "bx", "shift"])
    a, b, c = r.randint(2, 12), r.randint(2, 12), r.randint(2, 9)
    if form == "xa":       # x : a = b : c
        stem, val = f"x:{a}={b}:{c}", Fr(a * b, c)
        eqn, py = f"{c}x={a}\\times{b}", f"Rational({a}*{b},{c})"
        wrong = Fr(a * c, b)
    elif form == "ax":     # a : x = b : c
        stem, val = f"{a}:x={b}:{c}", Fr(a * c, b)
        eqn, py = f"{b}x={a}\\times{c}", f"Rational({a}*{c},{b})"
        wrong = Fr(a * b, c)
    elif form == "bx":     # a : b = c : x
        stem, val = f"{a}:{b}={c}:x", Fr(b * c, a)
        eqn, py = f"{a}x={b}\\times{c}", f"Rational({b}*{c},{a})"
        wrong = Fr(a * c, b)
    else:                  # (x - k) : a = b : c
        k = r.randint(1, 6)
        stem, val = f"(x-{k}):{a}={b}:{c}", Fr(a * b, c) + k
        eqn, py = f"{c}(x-{k})={a}\\times{b}", f"Rational({a}*{b},{c})+{k}"
        wrong = Fr(a * b, c) - k
    if val <= 0:
        val = Fr(1)
    return num(f"比例式 ${stem}$ を満たす $x$ の値を求めなさい。", ans_str(val),
               f"外側の項の積と内側の項の積が等しいので ${eqn}$。よって $x={ft(val)}$。", d=2, mark=mark_of(val),
               ap="比例式 $a:b=c:d$ では $ad=bc$（外側の項の積＝内側の項の積）が成り立つ。これで一次方程式に直す。",
               steps=["外側の項の積と内側の項の積を等号で結ぶ。", f"${eqn}$。", f"$x={ft(val)}$（分数のときは既約分数にする）。"],
               alt=["比の値が等しいことから、分数の形の方程式 $\\dfrac{a}{b}=\\dfrac{c}{d}$ に直して解いてもよい。"],
               pc=[("$ad=bc$ の式を正しくつくっている", 1), ("正しい値を求めている", 1)],
               pit=[f"内側どうし・外側どうしを取り違え、$x={ft(wrong)}$ としてしまう。", "答えの分数を約分し忘れる。"],
               chk=(py, fpy(val)))


@gen("basic_check", 3, ["concept", "condition_check"])
def a_check(r):
    x0 = r.choice([v for v in range(-5, 7) if v != 0])

    def make(xs):
        a, c = r.sample([-3, -2, 1, 2, 3, 4, 5], 2)
        b = r.randint(-9, 9)
        d = (a - c) * xs + b
        return a, b, c, d
    used, eqs = set(), []
    for xs in [x0] + [x0 + 1, x0 - 1, -x0 if x0 != 0 else 2, x0 + 2]:
        if xs in used:
            continue
        used.add(xs)
        eqs.append((xs, make(xs)))
        if len(eqs) == 4:
            break
    right = f"${eq_tex(*eqs[0][1])}$"
    why = {}
    ch = [right]
    for xs, (a, b, c, d) in eqs[1:]:
        t = f"${eq_tex(a, b, c, d)}$"
        ch.append(t)
        why[t] = (f"$x={x0}$ を代入すると、左辺は ${a * x0 + b}$、右辺は ${c * x0 + d}$ で等しくない（この方程式の解は $x={xs}$）。", "解の意味の誤解")
    a, b, c, d = eqs[0][1]
    return mc(f"次の方程式のうち，$x={x0}$ が解であるもの{SEL}", ch,
              f"$x={x0}$ を代入すると、{right} の左辺は ${a * x0 + b}$、右辺は ${c * x0 + d}$ で等しい。", d=2,
              ap="「解である」とは、代入したとき左辺と右辺の値が等しくなること。各方程式に代入して両辺の値を比べる。",
              steps=[f"それぞれの方程式に $x=({x0})$ を代入する。", "左辺と右辺の値を計算して比べる。", f"等しくなるのは {right}。"],
              alt=["それぞれの方程式を実際に解いて、解が $x=" + f"{x0}" + "$ になるものを選んでもよい。"],
              pc=[("正しく代入している", 1), ("正しい方程式を選んでいる", 1)],
              pit=["負の数を代入するときにかっこをつけ忘れる。", "左辺の値だけを計算して判断する。"],
              why=why, chk=(f"solve(Eq({lpy(a, b)}, {lpy(c, d)}), x)[0]", str(x0), None, "intermediate"))


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 4, ["computation", "common_error"])
def b_frac_eq(r):
    form = r.choice(["F1", "F2"])
    while True:
        if form == "F1":   # x/p - k = x/q  →  (1/p - 1/q) x = k
            p, q = r.sample([2, 3, 4, 5, 6], 2)
            k = r.randint(1, 5) * r.choice([1, -1])
            x0 = Fr(k) / (Fr(1, p) - Fr(1, q))
            if x0.denominator == 1 and abs(x0) <= 60:
                L = p * q // math.gcd(p, q)
                eq = f"\\dfrac{{x}}{{{p}}}{'-' if k > 0 else '+'}{abs(k)}=\\dfrac{{x}}{{{q}}}"
                cleared = f"{lin(L // p, -L * k)}={lin(L // q, 0)}"
                wrong = Fr(k) / Fr(L // p - L // q, 1)  # 定数項にかけ忘れ
                py = f"solve(Eq(x/{p}-({k}), x/{q}), x)[0]"
                break
        else:              # (ax+b)/p = (cx+d)/q
            p, q = r.sample([2, 3, 4, 5, 6], 2)
            a, c = r.choice([1, 2, 3]), r.choice([1, 2, 3])
            b, d = r.randint(-6, 6), r.randint(-6, 6)
            den = q * a - p * c
            if den == 0:
                continue
            x0 = Fr(p * d - q * b, den)
            if x0.denominator == 1 and abs(x0) <= 30 and b != 0 and d != 0:
                eq = f"\\dfrac{{{lin(a, b)}}}{{{p}}}=\\dfrac{{{lin(c, d)}}}{{{q}}}"
                cleared = f"{q}({lin(a, b)})={p}({lin(c, d)})"
                wd = q * a - p * c
                wrong = Fr(p * d - b, wd) if wd else x0 + 1  # 分子の定数項にかけ忘れ
                py = f"solve(Eq(({lpy(a, b)})/{p}, ({lpy(c, d)})/{q}), x)[0]"
                break
    x0 = Fr(x0)
    cands = [(X(wrong), "両辺に分母の最小公倍数をかけるとき、分数でない項（または分子の一部）にかけ忘れている。", "分母をはらうときのかけ忘れ"),
             (X(-x0), "移項するときに符号を誤っている。", "移項の符号の誤り")] + near(x0)
    common = dict(ap="両辺に分母の最小公倍数をかけて、分数をふくまない方程式に直す。分子はかっこをつけたまま扱い、すべての項にかける。",
                  steps=[f"両辺に分母の最小公倍数をかける：${cleared}$。", "かっこをはずし、移項して整理する。", f"$x={ft(x0)}$。"],
                  alt=[f"$x={ft(x0)}$ をもとの方程式に代入し、左辺と右辺の値が等しくなることを確かめる。"],
                  pc=[("分母をはらった式が正しい", 2), ("正しい解を求めている", 2)],
                  pit=["分数でない項に最小公倍数をかけ忘れる。", "分子にかっこをつけずに計算し、符号を誤る。"])
    if x0 > 0 and r.random() < 0.5:
        return num(f"方程式 ${eq}$ を解きなさい。", ans_str(x0), f"両辺に分母の最小公倍数をかけて ${cleared}$。整理して $x={ft(x0)}$。", d=3,
                   mark=mark_of(x0), chk=(py, fpy(x0)), **common)
    ch, why = pick(X(x0), cands)
    return mc(f"方程式 ${eq}$ の解{MCQ}", ch, f"両辺に分母の最小公倍数をかけて ${cleared}$。整理して $x={ft(x0)}$。", d=3, why=why,
              chk=(py, fpy(x0)), **common)


def dec(n):
    """10分の n を小数表記に。"""
    s = "-" if n < 0 else ""
    n = abs(n)
    return f"{s}{n // 10}.{n % 10}" if n % 10 else f"{s}{n // 10}"


@gen("standard_practice", 4, ["computation", "common_error"])
def b_decimal_eq(r):
    while True:
        a, c = r.sample([2, 3, 4, 5, 6, 7, 8, 9, 12, 15], 2)
        x0 = r.choice([v for v in range(-9, 10) if v != 0])
        b = r.choice([v for v in range(-30, 31) if v % 10 != 0])
        d = (a - c) * x0 + b
        if d != 0 and abs(d) <= 60:
            break
    eq = f"{dec(a)}x{'+' if b > 0 else '-'}{dec(abs(b))}={dec(c)}x{'+' if d > 0 else '-'}{dec(abs(d))}"
    cleared = eq_tex(a, b, c, d)
    wrong = Fr(Fr(d, 10) - Fr(b, 10), a - c)
    cands = [(X(wrong), "両辺を10倍するとき、$x$ の項だけを10倍し、数の項を10倍し忘れている。", "10倍のかけ忘れ"),
             (X(Fr(d + b, a - c)), "移項するときに数の項の符号を変えていない。", "移項の符号の誤り"),
             (X(-x0), "最後に係数でわるときに符号を誤っている。", "除法の符号の誤り")] + near(x0)
    ch, why = pick(X(x0), cands)
    common = dict(ap="小数の係数は、両辺を10倍（または100倍）して整数に直してから解く。すべての項を10倍する。",
                  steps=[f"両辺を10倍する：${cleared}$。", f"移項して ${lin(a - c, 0)}={d - b}$。", f"$x={x0}$。"],
                  alt=[f"$x={x0}$ をもとの方程式に代入：左辺 ${ft(Fr(a * x0 + b, 10))}$、右辺 ${ft(Fr(c * x0 + d, 10))}$ で一致する。"],
                  pc=[("両辺を正しく10倍している", 2), ("正しい解を求めている", 2)],
                  pit=["$x$ の項だけ10倍して、数の項を10倍し忘れる。", "小数点の位置を誤って100倍と10倍が混ざる。"])
    py = f"solve(Eq({a}*x/10+Rational({b},10), {c}*x/10+Rational({d},10)), x)[0]"
    if x0 > 0 and r.random() < 0.5:
        return num(f"方程式 ${eq}$ を解きなさい。", str(x0), f"両辺を10倍して ${cleared}$。$x={x0}$。", d=3, mark=("int", x0), chk=(py, str(x0)), **common)
    return mc(f"方程式 ${eq}$ の解{MCQ}", ch, f"両辺を10倍して ${cleared}$。移項して $x={x0}$。", d=3, why=why, chk=(py, str(x0)), **common)


@gen("standard_practice", 4, ["computation", "concept"])
def b_param(r):
    while True:
        k = r.choice([v for v in range(-4, 6) if v not in (0, -1)])
        a = r.choice([v for v in range(-6, 7) if v != 0])
        c = r.choice([2, 3, 4, 5])
        b = c * k - a * (k + 1)
        if b != 0 and abs(b) <= 30:
            break
    eq = f"ax{'+' if b > 0 else '-'}{abs(b)}={c}x-a"
    cands = [(M(-a), "符号を誤っている。$a$ をふくむ項を移項するときに符号を変える。", "移項の符号の誤り"),
             (M(Fr(c * k + b, k + 1)), f"定数項 ${b}$ を移項するときに符号を変えていない。", "移項の符号の誤り"),
             (M(Fr(c * k - b, k - 1)) if k != 1 else M(a + 5), f"$-a$ を左辺に移項すると $+a$ になるので、$a$ の係数は $({k}+1)$。$({k}-1)$ としている。", "移項の符号の誤り")] + near(a, M)
    ch, why = pick(M(a), cands)
    return mc(f"$x$ についての方程式 ${eq}$ の解が $x={k}$ であるとき，$a$ の値{MCQ}", ch,
              f"$x={k}$ を代入すると ${k}a{b:+d}={c * k}-a$。$a$ についての方程式として解くと ${k + 1}a={c * k - b}$、$a={a}$。", d=3,
              ap="「解が $x=" + f"{k}" + "$」なので、方程式に $x=" + f"{k}" + "$ を代入すると等式が成り立つ。代入した式を $a$ についての方程式とみて解く。",
              steps=[f"$x={k}$ を代入：${k}a{b:+d}={c * k}-a$。", f"$a$ の項を左辺、数の項を右辺に移項：${k + 1}a={c * k - b}$。", f"$a={a}$。"],
              alt=[f"$a={a}$ をもとの方程式に入れて実際に解き、解が $x={k}$ になることを確かめる。"],
              pc=[("$x$ の値を代入している", 1), ("$a$ についての方程式をつくっている", 1), ("正しい値を求めている", 2)],
              pit=["代入したあと、$x$ と $a$ を取り違えて解く。", "$-a$ の移項で符号を変え忘れる。"],
              why=why, chk=(f"solve(Eq(a*({k})+({b}), {c}*({k})-a), a)[0]", str(a)))


def _word(r):
    kind = r.choice(["share", "buy", "age", "share", "buy"])
    if kind == "share":
        while True:
            x = r.randint(4, 15)
            p = r.randint(2, 6)
            rr = p + r.randint(1, 3)
            q, s = r.randint(1, 12), r.randint(1, 12)
            N = p * x + q
            if rr * x - s == N:
                break
            s = rr * x - N
            if 1 <= s <= 15:
                break
        item = r.choice([("色紙", "枚"), ("鉛筆", "本"), ("あめ", "個")])
        stem = (f"クラスの何人かでレクリエーションの準備をする。{item[0]}を1人に ${p}$ {item[1]}ずつ配ると ${q}$ {item[1]}余り，"
                f"1人に ${rr}$ {item[1]}ずつ配ると ${s}$ {item[1]}たりない。人数を求めなさい。")
        return stem, x, f"人数を $x$ 人とすると、{item[0]}の数は ${p}x+{q}$、${rr}x-{s}$ と表せるので ${p}x+{q}={rr}x-{s}$。$x={x}$。", \
            [f"人数を $x$ 人とおく。", f"{item[0]}の数を2通りに表す：${p}x+{q}$、${rr}x-{s}$。", f"${p}x+{q}={rr}x-{s}$ を解いて $x={x}$。", f"解の吟味：人数は自然数で問題に適する（{item[0]}は ${N}$ {item[1]}）。"], \
            f"{item[0]}の数を $y$ として $\\dfrac{{y-{q}}}{{{p}}}=\\dfrac{{y+{s}}}{{{rr}}}$ を解くと $y={N}$。人数は $({N}-{q})\\div{p}={x}$。", \
            f"Eq({p}*x+{q}, {rr}*x-{s})"
    if kind == "buy":
        while True:
            pa, pb = r.sample([60, 80, 90, 100, 120, 130, 150], 2)
            n = r.randint(8, 16)
            x = r.randint(1, n - 1)
            T = pa * x + pb * (n - x)
            if T % 10 == 0:
                break
        A, B = r.choice([("ドーナツ", "クッキー"), ("ノート", "ボールペン"), ("おにぎり", "サンドイッチ")])
        stem = f"1個 ${pa}$ 円の{A}と1個 ${pb}$ 円の{B}を合わせて ${n}$ 個買ったところ，代金の合計は ${T}$ 円だった。買った{A}の個数を求めなさい。"
        return stem, x, f"{A}を $x$ 個とすると、{B}は $({n}-x)$ 個。${pa}x+{pb}({n}-x)={T}$ を解いて $x={x}$。", \
            [f"{A}の個数を $x$ 個とおくと、{B}は $({n}-x)$ 個。", f"代金の合計：${pa}x+{pb}({n}-x)={T}$。", f"${pa - pb}x={T - pb * n}$ より $x={x}$。", f"解の吟味：$0<{x}<{n}$ で問題に適する。"], \
            f"{B}の個数を $x$ 個として ${pa}({n}-x)+{pb}x={T}$ を解き、$x={n - x}$ から{A}は ${x}$ 個と求めてもよい。", \
            f"Eq({pa}*x+{pb}*({n}-x), {T})"
    while True:
        C = r.randint(5, 14)
        k = r.choice([2, 3, 4])
        x = r.randint(1, 15)
        F = k * (C + x) - x
        if 28 <= F <= 50:
            break
    stem = f"現在，Kさんは ${C}$ 歳で，Kさんの父は ${F}$ 歳である。父の年齢がKさんの年齢の ${k}$ 倍になるのは，今から何年後か求めなさい。"
    return stem, x, f"$x$ 年後とすると ${F}+x={k}({C}+x)$。$x={x}$。", \
        [f"$x$ 年後とおくと、父は $({F}+x)$ 歳、Kさんは $({C}+x)$ 歳。", f"${F}+x={k}({C}+x)$。", f"${F}+x={k * C}+{k}x$ より $x={x}$。", "解の吟味：正の数なので「〜年後」として問題に適する。"], \
        f"年齢の差 ${F - C}$ 歳は変わらないことに着目し、父がKさんの ${k}$ 倍のとき、差はKさんの年齢の ${k - 1}$ 倍だから、そのときのKさんは ${F - C}\\div{k - 1}={C + x}$ 歳。", \
        f"Eq({F}+x, {k}*({C}+x))"


@gen("standard_practice", 4, ["application", "computation"])
def b_word(r):
    stem, x, e, steps, alt, eqpy = _word(r)
    return num(stem, str(x), e, d=3, mark=("int", x),
               ap="求めるものを $x$ とおき、問題の中の同じ数量（品物の数・代金・年齢の関係など）を $x$ を使って2通りに表し、等号で結ぶ。",
               steps=steps, alt=[alt],
               pc=[("方程式を正しくつくっている", 2), ("方程式を解いて正しい答えを求めている", 2)],
               pit=["「余る」「たりない」の符号を逆にする。", "解の吟味をせず、問題に合わない値を答える。"],
               chk=(f"solve({eqpy}, x)[0]", str(x)))


@gen("standard_practice", 4, ["application", "computation"])
def b_speed(r):
    kind = r.choice(["chase", "meet", "time_diff"])
    if kind == "chase":
        while True:
            v1, v2 = r.choice([50, 60, 70, 80]), r.choice([150, 180, 200, 210, 240, 250])
            x = r.randint(2, 20)
            if (x * (v2 - v1)) % v1 == 0 and 3 <= x * (v2 - v1) // v1 <= 25:
                t = x * (v2 - v1) // v1
                break
        stem = (f"妹が家を出発して，分速 ${v1}$ m で図書館に向かった。その ${t}$ 分後に，Kさんが家を出発して，同じ道を分速 ${v2}$ m の自転車で追いかけた。"
                f"Kさんが妹に追いつくのは，Kさんが家を出発してから何分後か求めなさい。ただし，図書館に着くまでに追いつくものとする。")
        e = f"Kさんが出発して $x$ 分後に追いつくとすると、${v1}({x if False else 'x'}+{t})={v2}x$。$x={x}$。"
        steps = ["Kさんが出発してから $x$ 分後に追いつくとおく。", f"妹が進んだ道のり ${v1}(x+{t})$ m と、Kさんが進んだ道のり ${v2}x$ m が等しい。",
                 f"${v1}(x+{t})={v2}x$ より ${v2 - v1}x={v1 * t}$、$x={x}$。"]
        alt = f"Kさんが出発したとき、妹は ${v1 * t}$ m 先にいる。1分間に ${v2 - v1}$ m ずつ差が縮まるので、${v1 * t}\\div{v2 - v1}={x}$（分）。"
        eqpy = f"Eq({v1}*(x+{t}), {v2}*x)"
        e = f"Kさんが出発して $x$ 分後に追いつくとすると、${v1}(x+{t})={v2}x$。$x={x}$。"
    elif kind == "meet":
        v1, v2 = r.choice([60, 70, 80, 90]), r.choice([50, 60, 75, 100, 120])
        x = r.randint(6, 20)
        D = (v1 + v2) * x
        stem = (f"A地点とB地点は ${D}$ m 離れている。KさんはA地点から分速 ${v1}$ m で，友人はB地点から分速 ${v2}$ m で，同時に出発して向かい合って歩いた。"
                "2人が出会うのは，出発してから何分後か求めなさい。")
        e = f"$x$ 分後に出会うとすると、${v1}x+{v2}x={D}$。$x={x}$。"
        steps = ["$x$ 分後に出会うとおく。", f"2人が歩いた道のりの和が ${D}$ m になる：${v1}x+{v2}x={D}$。", f"${v1 + v2}x={D}$、$x={x}$。"]
        alt = f"2人の間の距離は1分間に ${v1 + v2}$ m ずつ縮まるので、${D}\\div{v1 + v2}={x}$（分）。"
        eqpy = f"Eq({v1}*x+{v2}*x, {D})"
    else:
        while True:
            v1, v2 = r.choice([40, 50, 60, 75, 80]), r.choice([100, 120, 150, 200, 240, 250, 300])
            t = r.randint(4, 20)
            num_ = t * v1 * v2
            if num_ % (v2 - v1) == 0 and num_ // (v2 - v1) <= 6000:
                x = num_ // (v2 - v1)
                break
        stem = f"家から駅まで行くのに，分速 ${v1}$ m で歩くと，分速 ${v2}$ m で走るより ${t}$ 分多くかかる。家から駅までの道のりは何 m か求めなさい。"
        e = f"道のりを $x$ m とすると、$\\dfrac{{x}}{{{v1}}}-\\dfrac{{x}}{{{v2}}}={t}$。$x={x}$。"
        steps = ["道のりを $x$ m とおく。", f"かかる時間は歩くと $\\dfrac{{x}}{{{v1}}}$ 分、走ると $\\dfrac{{x}}{{{v2}}}$ 分。", f"$\\dfrac{{x}}{{{v1}}}-\\dfrac{{x}}{{{v2}}}={t}$ を解いて $x={x}$。"]
        alt = f"走ったときにかかる時間を $y$ 分として ${v1}(y+{t})={v2}y$ をつくり、$y$ を求めてから道のりを ${v2}y$ と計算してもよい。"
        eqpy = f"Eq(x/{v1}-x/{v2}, {t})"
    return num(stem, str(x), e, d=3, mark=("int", x),
               ap="道のり＝速さ×時間の関係を使い、「同じ道のり」「道のりの和」「時間の差」など、等しくなる数量を見つけて方程式をつくる。",
               steps=steps, alt=[alt],
               pc=[("方程式を正しくつくっている", 2), ("正しい答えを求めている", 2)],
               pit=["先に出発した人の時間を $x$ のままにして、出発時刻の差を加え忘れる。", "単位（分と時間、m と km）をそろえない。"],
               chk=(f"solve({eqpy}, x)[0]", str(x)))


# ======================================================================
# C 思考力・記述応用
# ======================================================================

@gen("thinking_writing", 3, ["written_reasoning", "multiple_solutions"])
def c_setup(r):
    while True:
        x = r.randint(5, 14)
        p = r.randint(2, 5)
        rr = p + r.randint(1, 3)
        q = r.randint(1, 10)
        N = p * x + q
        s = rr * x - N
        if 1 <= s <= 12:
            break
    ask = r.choice(["eqL", "meaning"])
    lead = (f"何人かの子どもにみかんを配る。1人に ${p}$ 個ずつ配ると ${q}$ 個余り，1人に ${rr}$ 個ずつ配ると ${s}$ 個たりない。"
            f"Kさんは子どもの人数を $x$ 人として，方程式 ${p}x+{q}={rr}x-{s}$ をつくった。")
    if ask == "eqL":
        right = f"$\\dfrac{{x-{q}}}{{{p}}}=\\dfrac{{x+{s}}}{{{rr}}}$"
        w = [(f"$\\dfrac{{x+{q}}}{{{p}}}=\\dfrac{{x-{s}}}{{{rr}}}$", "余りとたりない数の扱いが逆。余る場合は、配った数＝全体－余り。", "過不足の向きの誤り"),
             (f"${p}x-{q}={rr}x+{s}$", f"これはKさんと同じく人数を $x$ とした式（しかも符号が逆）で、みかんの個数を $x$ とした式ではない。", "文字の意味の取り違え"),
             (f"$\\dfrac{{x}}{{{p}}}-{q}=\\dfrac{{x}}{{{rr}}}+{s}$", f"人数は（みかんの個数－余り）÷{p} で求める。先にわってからひくと人数にならない。", "計算の順序の誤り")]
        stem = f"{lead}\nLさんは，みかんの個数を $x$ 個として方程式をつくった。Lさんがつくった方程式として最も適するもの{SEL}"
        e = f"みかんが $x$ 個のとき、人数は $\\dfrac{{x-{q}}}{{{p}}}$ 人とも $\\dfrac{{x+{s}}}{{{rr}}}$ 人とも表せるので、{right}。解くと $x={N}$（個）、人数は ${x}$ 人。"
        steps = ["Lさんの $x$ はみかんの個数。", f"人数を2通りに表す：${p}$ 個ずつ配ると ${q}$ 個余るので $\\dfrac{{x-{q}}}{{{p}}}$ 人、${rr}$ 個ずつだと ${s}$ 個たりないので $\\dfrac{{x+{s}}}{{{rr}}}$ 人。", f"等号で結んで {right}。"]
        chk = (f"solve(Eq((x-{q})/{p}, (x+{s})/{rr}), x)[0]", str(N), None, "intermediate")
    else:
        right = f"子ども全員に ${p}$ 個ずつ配ったあとに余るみかんの個数と，配る前のみかんの個数との差"
        right = f"みかん全体の個数を，${p}$ 個ずつ配る場合の考え方で表したもの"
        w = [(f"子ども1人がもらうみかんの個数", f"1人がもらう個数は ${p}$ 個または ${rr}$ 個で、$x$ をふくむ式ではない。", "式の意味の誤解"),
             (f"${p}$ 個ずつ配ったときに余るみかんの個数", f"余る個数は ${q}$ 個。${p}x+{q}$ は配った分と余りを合わせた全体。", "部分と全体の混同"),
             (f"子どもの人数を，${rr}$ 個ずつ配る場合の考え方で表したもの", "$x$ が人数なので、式はみかんの個数を表している。", "文字の意味の取り違え")]
        stem = f"{lead}\nこの方程式の左辺 ${p}x+{q}$ が表しているものとして最も適するもの{SEL}"
        e = f"${p}x$ は ${p}$ 個ずつ配った個数、${q}$ は余りなので、${p}x+{q}$ はみかん全体の個数を表す。右辺 ${rr}x-{s}$ も全体の個数を別の考え方で表したもの。"
        steps = ["$x$ は子どもの人数。", f"${p}x$ は ${p}$ 個ずつ配ったみかんの個数、${q}$ は余り。", f"${p}x+{q}$ はみかん全体の個数（${p}$ 個ずつ配る場合の見方）。"]
        chk = (f"solve(Eq({p}*x+{q}, {rr}*x-{s}), x)[0]", str(x), None, "intermediate")
    ch, why = pick(right, w)
    return mc(stem, ch, e, d=4,
              ap="文字 $x$ が何を表しているかを最初に確かめ、式の各部分がどの数量を表しているかを言葉で読む。",
              steps=steps, alt=[f"どちらの方程式を解いても、人数 ${x}$ 人・みかん ${N}$ 個という同じ結論になることを確かめる。"],
              pc=[("文字の表す数量を正しく読み取っている", 4), ("正しい式・意味を選んでいる", 4)],
              pit=["$x$ が人数か個数かを確かめずに式を読む。", "「余る」と「たりない」の符号を取り違える。"],
              why=why, chk=chk)


@gen("thinking_writing", 2, ["cross_unit", "application"], rel=["JH-MATH-G1-U04"])
def c_prop_cross(r):
    kind = r.choice(["direct", "inverse", "direct"])
    if kind == "direct":
        while True:
            a = r.choice([Fr(1, 2), Fr(2, 3), Fr(3, 2), Fr(3, 4), 2, 3, 4, 5, -2, -3])
            x1 = r.choice([2, 3, 4, 6, -2, -4])
            y1 = Fr(a) * x1
            if y1.denominator != 1:
                continue
            y2 = r.choice([v for v in range(-30, 31) if v not in (0, int(y1))])
            x2 = Fr(y2) / Fr(a)
            if x2 > 0:
                break
        stem = f"$y$ は $x$ に比例し，$x={x1}$ のとき $y={int(y1)}$ である。$y={y2}$ となるときの $x$ の値を求めなさい。"
        e = f"$y=ax$ に代入して $a={ft(a)}$。$y={ft(a)}x$ に $y={y2}$ を代入して ${y2}={ft(a)}x$、$x={ft(x2)}$。"
        steps = [f"$y=ax$ に $x={x1},\\ y={int(y1)}$ を代入して $a={ft(a)}$。", f"$y={ft(a)}x$ に $y={y2}$ を代入する。", f"一次方程式 ${y2}={ft(a)}x$ を解いて $x={ft(x2)}$。"]
        alt = f"比例では $x$ と $y$ の比が一定なので、比例式 ${x1}:{int(y1)}=x:{y2}$ を解いても同じ答えになる。"
        py = f"solve(Eq({fpy(a)}*x, {y2}), x)[0]"
    else:
        while True:
            k = r.choice([12, 18, 24, 30, 36, 48, 60])
            x1 = r.choice([d for d in (2, 3, 4, 6) if k % d == 0])
            y2 = r.choice([v for v in (1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 16) if v != k // x1])
            x2 = Fr(k, y2)
            break
        stem = f"$y$ は $x$ に反比例し，$x={x1}$ のとき $y={k // x1}$ である。$y={y2}$ となるときの $x$ の値を求めなさい。"
        e = f"$xy=a$ より $a={x1}\\times{k // x1}={k}$。$y=\\dfrac{{{k}}}{{x}}$ に $y={y2}$ を代入して ${y2}x={k}$、$x={ft(x2)}$。"
        steps = [f"$a=xy={x1}\\times{k // x1}={k}$。", f"$y=\\dfrac{{{k}}}{{x}}$ に $y={y2}$ を代入し、両辺に $x$ をかけて ${y2}x={k}$。", f"$x={ft(x2)}$。"]
        alt = f"反比例では $xy$ が一定なので、${x1}\\times{k // x1}=x\\times{y2}$ という方程式をすぐにつくってもよい。"
        py = f"solve(Eq({y2}*x, {k}), x)[0]"
    return num(stem, ans_str(x2), e, d=4, mark=mark_of(x2),
               ap="比例・反比例の式を決めてから、与えられた $y$ の値を代入して、$x$ についての一次方程式を解く。",
               steps=steps, alt=[alt],
               pc=[("比例定数を求めている", 3), ("一次方程式をつくっている", 2), ("正しい値を求めている", 3)],
               pit=["比例定数を $\\dfrac{x}{y}$ と逆に求める。", "反比例を比例と同じように比例式で解いてしまう。"],
               chk=(py, fpy(x2)))


@gen("thinking_writing", 3, ["condition_check", "written_reasoning"])
def c_judge(r):
    kind = r.choice(["frac", "age", "frac", "age"])
    if kind == "frac":
        while True:
            p = r.randint(3, 6)
            rr = p + r.randint(1, 3)
            q, s = r.randint(1, 9), r.randint(1, 9)
            x0 = Fr(q + s, rr - p)
            if x0.denominator != 1:
                break
        lead = (f"何人かの生徒にカードを配る。1人に ${p}$ 枚ずつ配ると ${q}$ 枚余り，1人に ${rr}$ 枚ずつ配ると ${s}$ 枚たりないという。"
                f"生徒の人数を $x$ 人として方程式 ${p}x+{q}={rr}x-{s}$ をつくって解くと，$x={ft(x0)}$ となった。")
        right = "人数は自然数でなければならないので，問題の条件に合う人数はない。"
        w = [(f"生徒の人数は ${ft(x0)}$ 人である。", "人数は自然数なので、分数の人数は答えにならない。", "解の吟味の欠如"),
             (f"四捨五入して，生徒の人数は ${round(float(x0))}$ 人である。", f"${round(float(x0))}$ 人では、配った結果が問題の条件（余り・不足の枚数）に合わない。", "解の吟味の誤解"),
             ("方程式のつくり方が誤っているので，つくり直せば自然数の解が得られる。", "方程式は正しくつくられている。条件そのものに合う人数がない。", "立式の誤解")]
        e = f"$x$ は人数を表すので自然数でなければならない。$x={ft(x0)}$ は自然数でないので、この条件を満たす人数はない。"
        chk = (f"solve(Eq({p}*x+{q}, {rr}*x-{s}), x)[0]", fpy(x0), None, "intermediate")
    else:
        while True:
            C = r.randint(8, 16)
            k = r.choice([3, 4, 5])
            y = r.randint(1, C - 2)
            F = k * (C - y) + y
            if 30 <= F <= 55:
                break
        lead = (f"現在，Kさんは ${C}$ 歳で，Kさんの父は ${F}$ 歳である。父の年齢がKさんの年齢の ${k}$ 倍になるのは何年後かを求めるために，"
                f"$x$ 年後として方程式 ${F}+x={k}({C}+x)$ をつくって解くと，$x={-y}$ となった。")
        right = f"$x={-y}$ は「${y}$ 年前」を表し，${y}$ 年前に父の年齢はKさんの年齢の ${k}$ 倍だった。"
        w = [("解が負の数なので，方程式のつくり方が誤っている。", "方程式は正しい。負の解は「〜年前」と読みかえられる。", "負の解の意味の誤解"),
             (f"${y}$ 年後に，父の年齢はKさんの年齢の ${k}$ 倍になる。", f"$x={-y}$ は ${y}$ 年後ではなく ${y}$ 年前を表す。", "符号の読み違い"),
             ("解が負の数なので，父の年齢がKさんの年齢の何倍かになることはない。", f"${y}$ 年前には父 ${F - y}$ 歳、Kさん ${C - y}$ 歳で、実際に ${k}$ 倍になっている。", "負の解の意味の誤解")]
        e = f"$x$ 年後の $x$ が負の数 ${-y}$ なので「${y}$ 年前」を表す。${y}$ 年前は父 ${F - y}$ 歳、Kさん ${C - y}$ 歳で、${F - y}={k}\\times{C - y}$ となり確かに ${k}$ 倍。"
        chk = (f"solve(Eq({F}+x, {k}*({C}+x)), x)[0]", str(-y), None, "intermediate")
    ch, why = pick(right, w)
    return mc(f"{lead}\nこの結果についての説明として最も適するもの{SEL}", ch, e, d=4,
              ap="方程式の解が、問題の中で何を表しているか（人数・年数など）にもどって考える。解が分数や負の数のときの意味を確かめる（解の吟味）。",
              steps=["$x$ が表すものと、その数がとりうる値（自然数・整数など）を確かめる。", "求めた解がその条件に合うかを調べる。", e],
              alt=["実際に数を入れて確かめる（人数なら近い自然数で配ってみる、年齢なら何年前の年齢を計算してみる）。"],
              pc=[("$x$ の意味と条件を確認している", 4), ("解の吟味にもとづいて正しく判断している", 4)],
              pit=["解が分数でもそのまま答えにする。", "負の解をすぐに「答えなし」とする。"],
              why=why, chk=chk)


@gen("thinking_writing", 2, ["application", "computation"])
def c_ratio_mix(r):
    while True:
        a, b = r.sample(range(2, 8), 2)
        if math.gcd(a, b) != 1:
            continue
        d, e = r.sample(range(1, 8), 2)
        if math.gcd(d, e) != 1:
            continue
        c = r.randint(3, 20)
        den = e * a - d * b
        if den <= 0:
            continue
        if (d * c) % den == 0:
            k = d * c // den
            if 2 <= k <= 15:
                break
    A, B = a * k, b * k
    item = r.choice([("赤玉", "白玉", "個"), ("男子", "女子", "人"), ("黒のカード", "白のカード", "枚")])
    stem = (f"箱の中に{item[0]}と{item[1]}が入っていて，その数の比は ${a}:{b}$ である。この箱に{item[1]}を ${c}$ {item[2]}加えたところ，"
            f"{item[0]}と{item[1]}の数の比は ${d}:{e}$ になった。はじめに箱に入っていた{item[0]}の数を求めなさい。") if item[0] != "男子" else (
            f"ある部の部員は男子と女子で，その人数の比は ${a}:{b}$ である。新たに女子が ${c}$ 人入部したところ，男子と女子の人数の比は ${d}:{e}$ になった。"
            "はじめの男子の人数を求めなさい。")
    return num(stem, str(A), f"はじめの数を ${a}x$、${b}x$ とおくと ${a}x:({b}x+{c})={d}:{e}$。${e * a}x={d}({b}x+{c})$ より $x={k}$、はじめの{item[0]}は ${A}$ {item[2]}。",
               d=4, mark=("int", A),
               ap=f"比が ${a}:{b}$ なので、はじめの数を ${a}x$、${b}x$ と1つの文字で表す。加えたあとの比で比例式をつくる。",
               steps=[f"はじめの数を ${a}x$、${b}x$ とおく。", f"加えたあと：${a}x:({b}x+{c})={d}:{e}$。", f"${e}\\times{a}x={d}({b}x+{c})$ より ${e * a - d * b}x={d * c}$、$x={k}$。",
                      f"はじめの{item[0]}は ${a}\\times{k}={A}$ {item[2]}。"],
               alt=[f"はじめの{item[0]}を $y$ として、{item[1]}を $\\dfrac{{{b}}}{{{a}}}y$ と表し、$y:\\left(\\dfrac{{{b}}}{{{a}}}y+{c}\\right)={d}:{e}$ を解いても同じ答えになる。"],
               pc=[("比を1つの文字で表している", 2), ("比例式をつくっている", 3), ("正しい答えを求めている", 3)],
               pit=[f"$x$ の値 ${k}$ をそのまま答えにしてしまう（求めるのは ${a}x$）。", "加えたのがどちらかを取り違える。"],
               chk=(f"{a}*solve(Eq({e}*{a}*x, {d}*({b}*x+{c})), x)[0]", str(A)))


# ======================================================================
# D 典型誤答訂正
# ======================================================================

LN = ["①", "②", "③"]


@gen("error_correction", 4, ["common_error", "computation"])
def d_line(r):
    while True:
        x0 = r.choice([v for v in range(-6, 8) if v != 0])
        a, c = r.sample([2, 3, 4, 5, 6, 7, -2, -3], 2)
        b = r.choice([v for v in range(-9, 10) if v != 0])
        d = (a - c) * x0 + b
        if d != 0 and abs(d) <= 30 and a - c != 1:
            break
    eq = eq_tex(a, b, c, d)
    where = r.choice([0, 0, 1, 2])
    good1 = f"{lin(a, 0)}{lin(-c, 0) if -c < 0 else '+' + lin(-c, 0)}={d}{-b:+d}"
    if where == 0:
        l1 = f"{lin(a, 0)}{lin(-c, 0) if -c < 0 else '+' + lin(-c, 0)}={d}{b:+d}"
        l2 = f"{lin(a - c, 0)}={d + b}"
        wx = Fr(d + b, a - c)
        typ, tempt = "sign", "左辺の数の項を右辺へ移すとき、符号を変えずにそのまま書いてしまった。"
        reason = f"①で ${b:+d}$ を右辺に移項するとき、符号を変えて ${-b:+d}$ にしていない。"
    elif where == 1:
        l1 = good1
        wa = a + c
        l2 = f"{lin(wa, 0)}={d - b}"
        wx = Fr(d - b, wa) if wa else Fr(d - b + 1)
        typ, tempt = "calculation", "$x$ の項を移項して符号を変えたのに、まとめるときに元の符号で計算してしまった。"
        reason = f"②で ${lin(a, 0)}{lin(-c, 0) if -c < 0 else '+' + lin(-c, 0)}$ を ${lin(wa, 0)}$ としている。正しくは ${lin(a - c, 0)}$。"
    else:
        l1 = good1
        l2 = f"{lin(a - c, 0)}={d - b}"
        wx = Fr(a - c, d - b)
        typ, tempt = "concept", "$ax=b$ の両辺を $a$ でわることと、$b$ を $a$ でわることを混同し、分数の上下を逆にした。"
        reason = f"③で $x=\\dfrac{{{a - c}}}{{{d - b}}}$ としている。${lin(a - c, 0)}={d - b}$ の両辺を ${a - c}$ でわるので $x=\\dfrac{{{d - b}}}{{{a - c}}}$。"
    l3 = f"x={ft(wx)}"
    lines = [l1, l2, l3]
    sol = "\n".join(f"{LN[i]}　${lines[i]}$" for i in range(3))
    opts = ["①の行", "②の行", "③の行", "どの行にも誤りはない"]
    idx = where
    why = {}
    for i, o in enumerate(opts):
        if i == idx:
            continue
        if i == 3:
            why[o] = (f"$x={ft(wx)}$ を代入すると両辺が等しくならないので、どこかに誤りがある。正しい解は $x={x0}$。", "誤りの見落とし")
        else:
            why[o] = ((f"{o}の変形は正しい。" if i < idx else f"{o}は前の行の誤りを引き継いでいるだけで、最初の誤りではない。") + f"最初の誤りは{opts[idx]}。", "誤りの位置の見落とし")
    return mc(f"Kさんは，方程式 ${eq}$ を次のように解いた。\n{sol}\nKさんの解き方で，誤りが最初に生じた行として最も適するもの{SEL}", opts,
              f"{reason}正しくは ${good1}$、${lin(a - c, 0)}={d - b}$、$x={x0}$。", d=3, keep=True, ai=idx,
              ap="移項で符号を変えているか、同類項のまとめが正しいか、最後のわり算の向きが正しいかを1行ずつ確かめる。",
              steps=[f"①：移項して ${good1}$ になっているか。", f"②：${lin(a - c, 0)}={d - b}$ になっているか。", f"③：両辺を ${a - c}$ でわって $x={x0}$ になっているか。"],
              alt=["Kさんの答えをもとの方程式に代入すると等式が成り立たないことから、誤りがあると分かる。各行の方程式に正しい解を代入し、成り立たなくなった最初の行を探す方法もある。"],
              pc=[("誤りの行を正しく指摘している", 3), ("誤りの理由を説明できる", 2), ("正しい解を求められる", 1)],
              pit=["移項したのに符号を変え忘れる。", "最後に $x=\\dfrac{a}{b}$ と逆にわる。"],
              why=why, err=dict(sol=sol, step=opts[idx], type=typ, tempt=tempt, fix=f"${good1}$、${lin(a - c, 0)}={d - b}$、$x={x0}$"),
              chk=(f"solve(Eq({lpy(a, b)}, {lpy(c, d)}), x)[0]", str(x0), None, "intermediate"))


@gen("error_correction", 3, ["common_error", "condition_check"])
def d_frac(r):
    while True:
        p, q = r.sample([2, 3, 4, 5, 6], 2)
        k = r.randint(1, 5)
        L = p * q // math.gcd(p, q)
        x0 = Fr(k) / (Fr(1, p) - Fr(1, q))
        wx = Fr(k) / Fr(L // p - L // q)
        if x0.denominator == 1 and wx != x0 and abs(x0) <= 60:
            break
    eq = f"\\dfrac{{x}}{{{p}}}-{k}=\\dfrac{{x}}{{{q}}}"
    sol = f"両辺に ${L}$ をかけて ${lin(L // p, -k)}={lin(L // q, 0)}$，移項して " + (f"${lin(L // p - L // q, 0)}={k}$，$x={ft(wx)}$" if L // p - L // q != 1 else f"$x={ft(wx)}$")
    right = f"両辺に ${L}$ をかけるとき，分数でない項 $-{k}$ にも ${L}$ をかけなければならないのに，かけていない。"
    ws = [(f"分母をはらうには，左辺だけに ${p}$ をかけ，右辺だけに ${q}$ をかけなければならない。", "等式の性質では、両辺に同じ数をかける。左辺と右辺に違う数をかけると等式が成り立たなくなる。", "等式の性質の誤解"),
          ("方程式では分母をはらってはいけない。", "方程式では両辺に同じ数をかけてよい（等式の性質）。分母をはらうのは正しい方法。", "式の計算との混同"),
          ("移項するときに，$x$ の項の符号を変え忘れている。", "$x$ の項の移項は正しい。誤りは定数項に最小公倍数をかけ忘れたこと。", "誤りの原因の取り違え")]
    ch = [right] + [w[0] for w in ws]
    why = {w[0]: (w[1], w[2]) for w in ws}
    return mc(f"方程式 ${eq}$ を解く問題で，Kさんは次のように答えた。\n［Kさんの解答］{sol}\nKさんの解答の誤りを説明したものとして最も適するもの{SEL}", ch,
              f"{right}正しくは ${lin(L // p, -L * k)}={lin(L // q, 0)}$、$x={ft(x0)}$。", d=3,
              ap="両辺に同じ数をかけるとき、左辺・右辺のすべての項にかけているかを確かめる。",
              steps=[f"両辺に ${L}$ をかける：${L}\\times\\dfrac{{x}}{{{p}}}-{L}\\times{k}={L}\\times\\dfrac{{x}}{{{q}}}$。", f"${lin(L // p, -L * k)}={lin(L // q, 0)}$。", f"$x={ft(x0)}$。"],
              alt=[f"Kさんの答え $x={ft(wx)}$ をもとの方程式に代入すると、左辺と右辺の値が等しくならないことから誤りに気づける。"],
              pc=[("誤りの原因を正しく選んでいる", 4), ("正しい解を求められる", 2)],
              pit=["分数の項にだけ最小公倍数をかける。"],
              why=why, err=dict(sol=sol, step=f"$-{k}$ に ${L}$ をかけなかった部分", type="calculation",
                                tempt="分母をはらうことに意識が向き、分母のない項にもかける必要があることを忘れた。", fix=f"${lin(L // p, -L * k)}={lin(L // q, 0)}$ より $x={ft(x0)}$"),
              chk=(f"solve(Eq(x/{p}-{k}, x/{q}), x)[0]", fpy(x0), None, "intermediate"))


@gen("error_correction", 3, ["common_error", "concept"])
def d_misc(r):
    kind = r.choice(["prop", "decimal", "divneg"])
    if kind == "prop":
        a, b, c = r.randint(2, 9), r.randint(2, 12), r.choice([2, 3, 4, 5])
        eq = f"x:{a}={b}:{c}"
        val = Fr(a * b, c)
        wv = Fr(a * c, b)
        sol = f"${b}x={a}\\times{c}$ より $x={ft(wv)}$"
        right = f"比例式では外側の項の積と内側の項の積が等しいので，${c}x={a}\\times{b}$ としなければならない。正しくは $x={ft(val)}$"
        ws = [("比例式は方程式ではないので，等式の性質は使えない。", "比例式は $ad=bc$ の形の方程式に直して解ける。", "比例式の誤解"),
              (f"$x$ の係数でわるとき，${a}\\times{c}$ を ${b}$ でわるのではなく，${b}$ を ${a}\\times{c}$ でわらなければならない。", "わり方は正しいが、もとにした積の組み合わせが誤っている。", "誤りの原因の取り違え"),
              ("解き方に誤りはなく，答えは正しい。", f"$x={ft(wv)}$ のとき比 $x:{a}$ の値と ${b}:{c}$ の値が等しくならない。", "誤りの見落とし")]
        typ, step, tempt = "formula", f"${b}x={a}\\times{c}$ とした部分", "外側どうし・内側どうしの組み合わせを取り違え、$x$ と同じ側の比の後ろの数をかけてしまった。"
        fix, chk = f"${c}x={a * b}$ より $x={ft(val)}$", (f"solve(Eq({c}*x, {a}*{b}), x)[0]", fpy(val), None, "intermediate")
        task = f"比例式 ${eq}$ を解く問題"
    elif kind == "decimal":
        while True:
            a, c = r.sample([2, 3, 4, 5, 6, 7, 8], 2)
            x0 = r.choice([v for v in range(-6, 7) if v != 0])
            b = r.choice([v for v in range(-20, 21) if v % 10 != 0])
            d = (a - c) * x0 + b
            if d != 0 and d % 10 != 0 and abs(d) <= 40:
                break
        eq = f"{dec(a)}x{'+' if b > 0 else '-'}{dec(abs(b))}={dec(c)}x{'+' if d > 0 else '-'}{dec(abs(d))}"
        wx = Fr(Fr(d, 10) - Fr(b, 10), a - c)
        sol = f"両辺を10倍して ${a}x{'+' if b > 0 else '-'}{dec(abs(b))}={c}x{'+' if d > 0 else '-'}{dec(abs(d))}$，$x={ft(wx)}$"
        right = "両辺を10倍するとき，数の項も10倍しなければならないのに，$x$ の項だけを10倍している。"
        ws = [("小数をふくむ方程式は，10倍してはいけない。", "等式の性質により、両辺を10倍してよい。", "等式の性質の誤解"),
              ("両辺を100倍しなければならない。", "小数第1位までなので10倍で整数になる。100倍しても解けるが、それは誤りの原因ではない。", "誤りの原因の取り違え"),
              ("解き方に誤りはなく，答えは正しい。", f"正しい解は $x={x0}$ である。", "誤りの見落とし")]
        typ, step, tempt = "calculation", "数の項を10倍しなかった部分", "$x$ の係数を整数にすることだけに意識が向き、数の項にも10をかける必要があることを忘れた。"
        fix, chk = f"${eq_tex(a, b, c, d)}$ より $x={x0}$", (f"solve(Eq({a}*x/10+Rational({b},10), {c}*x/10+Rational({d},10)), x)[0]", str(x0), None, "intermediate")
        task = f"方程式 ${eq}$ を解く問題"
    else:
        k = r.choice([2, 3, 4, 5, 6])
        m = r.choice([2, 3, 4, 5, 6, 7]) * k
        b = r.randint(1, 9)
        eq = f"{b}-{k}x={m + b}"
        val = -m // k
        sol = f"$-{k}x={m + b}-{b}$，$-{k}x={m}$，$x={m // k}$"
        right = f"$-{k}x={m}$ の両辺を $-{k}$ でわるので $x=-{m // k}$ となるのに，${k}$ でわっている。"
        ws = [(f"${b}$ を移項するときに符号を変え忘れている。", f"${b}$ を右辺に移して $-{b}$ としているので正しい。", "誤りの原因の取り違え"),
              ("両辺を負の数でわることはできないので，この方程式は解けない。", "$0$ でない数なら、負の数でもわってよい。", "等式の性質の誤解"),
              ("解き方に誤りはなく，答えは正しい。", f"$x={m // k}$ を代入すると左辺は ${b - m}$ となり右辺 ${m + b}$ と等しくない。", "誤りの見落とし")]
        typ, step, tempt = "sign", "最後に両辺をわった部分", "$x$ の係数の負の符号を見落とし、絶対値だけでわってしまった。"
        fix, chk = f"$-{k}x={m}$ より $x=-{m // k}$", (f"solve(Eq({b}-{k}*x, {m + b}), x)[0]", str(val), None, "intermediate")
        task = f"方程式 ${eq}$ を解く問題"
    ch = [right] + [w[0] for w in ws]
    why = {w[0]: (w[1], w[2]) for w in ws}
    return mc(f"{task}で，Kさんは次のように答えた。\n［Kさんの解答］{sol}\nKさんの解答の誤りを説明したものとして最も適するもの{SEL}", ch,
              f"{right.rstrip('。')}。", d=3,
              ap="Kさんの答えをもとの式に代入して誤りを確認し、どの手順が等式の性質（または比例式の性質）に反しているかを探す。",
              steps=["Kさんの答えを代入して、成り立たないことを確かめる。", "各手順が、等式の性質・比例式の性質にしたがっているかを確かめる。", f"正しくは {fix}。"],
              alt=["自分で最初から解いた答えとKさんの途中式を比べ、最初に食い違った場所を探す。"],
              pc=[("誤りの原因を正しく選んでいる", 4), ("正しい解を求められる", 2)],
              pit=["比例式で内側・外側の組み合わせを取り違える。", "負の係数でわるときに符号を落とす。"],
              why=why, err=dict(sol=sol, step=step, type=typ, tempt=tempt, fix=fix), chk=chk)


GENERATORS = [a_solve, a_property, a_paren, a_proportion, a_check,
              b_frac_eq, b_decimal_eq, b_param, b_word, b_speed,
              c_setup, c_prop_cross, c_judge, c_ratio_mix,
              d_line, d_frac, d_misc]
