"""単元パック：英語コミュニケーションⅠ 比較（倍数表現・比較級を用いた最上級表現・the 比較級, the 比較級）。"""
import random

from banks._common import desc, mc, order, sa
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem,
                         tp)

UNIT_ID = "HS-ENG-U07"


def local(key):
    """問題文から決まる乱数（同じ問題文なら同じ選択肢になるようにする）。"""
    return random.Random(key)


def cap(s):
    return s[0].upper() + s[1:]


def mid(x):
    """文中に置くときの主語（This / The を小文字にする）。"""
    return x[0].lower() + x[1:] if x.split()[0] in ("This", "The") else x


# ======================================================================
# 授業プリント
# ======================================================================

LESSON = lesson(
    goals=["倍数表現（X times as ～ as …／X times the 名詞 of …）を使って、2つのものの差を正確に表せる。",
           "原級・比較級を使って最上級と同じ内容を表す4つの言いかえ（No other ～ / than any other ～ など）を書ける。",
           "the＋比較級 ～, the＋比較級 … の構文を、元になる2つの文から組み立てて使える。"],
    duration=50,
    readiness=["形容詞・副詞の原級・比較級・最上級の作り方（-er / -est、more / most、不規則変化）を中学で学習している。",
               "as ～ as …、比較級＋than …、the＋最上級＋in / of … の基本形を使える。",
               "可算名詞・不可算名詞の区別と、many / much の使い分けができる。"],
    flow=[("導入：数字で比べる", 5, "「この橋はあの橋の3倍の長さ」を英語でどう言うかを考えさせ、as ～ as の前に倍数を置く発想に導く"),
          ("倍数表現と比較級の強調", 12, "X times as ～ as、half as ～ as、twice the size of と、much / far / even による強調を整理する（例題1）"),
          ("最上級の意味を表す4つの形", 13, "No other ～ as / than、than any other ～、than all the other ～ を導出し、単数・複数の区別を確認する（例題2）"),
          ("the 比較級, the 比較級", 13, "2つの文から構文を組み立てる手順を示し、the more books のように名詞がついてくることを確認する（例題3）"),
          ("まとめと確認", 7, "確認問題3問、問題プリントA の課題指示")],
    sections=[
        intro("in1", "比較は「差」を正確に伝えるための表現",
              "「この橋はあの橋より長い」と言うだけでは、どのくらい長いのかが伝わらない。英語の比較表現は、as ～ as（同じ程度）や比較級（どちらがより～か）を土台にして、倍数・差の大きさ・順位まで正確に伝える仕組みを持っている。論説文やグラフの説明では、こうした表現が筆者の主張の根拠として繰り返し使われる。",
              bullets=["This bridge is longer than that one.（長さの大小だけ）",
                       "This bridge is three times as long as that one.（3倍という比率まで）",
                       "No other bridge in the city is as long as this one.（市内で最も長いという順位）"],
              points=[tp("3つの英文を順に板書し、伝わる情報が増えていくことを確認させる。", ask="2文目と3文目は、1文目に比べてどんな情報が増えているか。",
                         expect="2文目は比率（3倍）、3文目は「いちばん長い」という順位。", timing="導入の冒頭"),
                      tp("比較の単元は中学の復習に見えるが、高校では「書きかえ」と「語順」で差がつくことを最初に伝える。")]),
        definition("df1", "倍数表現と比較級の強調",
                   "「A は B の X 倍～だ」は、as ～ as … の前に倍数を置いて表す。2倍は twice、3倍以上は three times, four times …、半分は half を使う。名詞を使って「X times the 名詞 of …」と表すこともできる。",
                   formula="A is X times as 原級 as B ／ A is X times the 名詞（size / length / height など）of B",
                   bullets=["This box is twice as heavy as that one.（この箱はあの箱の2倍の重さだ）",
                            "My room is half as large as yours.（私の部屋はあなたの部屋の半分の広さだ）",
                            "This lake is three times the size of that one.（この湖はあの湖の3倍の大きさだ）",
                            "数えられる名詞の数を比べるときは X times as many＋複数名詞 as …、量なら X times as much＋不可算名詞 as …",
                            "比較級の強調：much / far / even / still / a lot＋比較級（very は比較級を強められない）"],
                   conditions=["as と as の間は必ず原級（three times as heavier as は誤り）。",
                               "差を数字で示すときは「数字＋比較級＋than」（three years older than）。by を使って older than … by three years とも言える。"],
                   points=[tp("very は原級を強め、much / far は比較級を強める、という対応を表にして示す。", caution="「とても」を very と訳す習慣から、very taller と書く誤りが非常に多い。")]),
        theorem("th1", "比較級・原級を使って最上級の意味を表す",
                "A is the 最上級 ＋名詞 in … ＝ No other 単数名詞 in … is as 原級 as A ＝ No other 単数名詞 in … is 比較級 than A ＝ A is 比較級 than any other 単数名詞 in … ＝ A is 比較級 than all the other 複数名詞 in …",
                ["no other・any other の後ろは単数名詞、all the other の後ろは複数名詞。",
                 "比べる集団の中に A 自身が含まれるので、other（ほかの）が必要になる。",
                 "Nothing is as 原級 as A ／ Nothing is 比較級 than A も「A ほど～なものはない」という最上級の意味になる。"],
                body="例：Mt. Fuji is the highest mountain in Japan. → No other mountain in Japan is as high as Mt. Fuji. ／ Mt. Fuji is higher than any other mountain in Japan.",
                points=[tp("4つの形を縦に並べて板書し、変わる部分（as 原級 as ／ 比較級 than、単数／複数）に色をつける。",
                           ask="than any other の後ろの名詞はなぜ単数形なのか。", expect="any other mountain は「ほかのどの1つの山をとっても」という意味だから。")]),
        derivation("dv1", "the＋比較級 ～, the＋比較級 … の組み立て",
                   ["① 元になる2つの文を作る：You read many books. ／ You learn much.",
                    "② それぞれの文で、比べたい語（形容詞・副詞・many / much）を比較級にする：many → more、much → more。",
                    "③ 比較級に the をつけて、それぞれの節の先頭に出す。比較級が名詞を修飾しているときは名詞も一緒に出す（the more books）。",
                    "④ 残りの語順（主語＋動詞）はそのまま後ろに続ける：the more books you read ／ the more you learn。",
                    "⑤ 2つの節をコンマでつなぐ：The more books you read, the more you learn.（読めば読むほど多くを学ぶ）",
                    "⑥ 前半は条件（「～すればするほど」）にあたるので、未来のことでも現在形を使う。"],
                   body="この構文の the は冠詞ではなく「その分だけ」という程度を表す副詞である。そのため、前半の変化に比例して後半も変化するという意味になる。主語・動詞が明らかなときは省略されることもある（The sooner, the better.）。",
                   points=[tp("2つの文を板書し、比較級を矢印で文頭に移動させる様子を実演する。", ask="The more you read books, … はなぜ不自然か。",
                              expect="more は books を修飾しているので、books も一緒に前に出す必要がある。", timing="手順③の説明時")]),
        example("ex1", "例題1　倍数表現",
                "日本語に合うように英文を書きなさい。(1) この箱はあの箱の3倍の重さだ。(2) 私の兄は私の2倍の数の本を持っている。",
                ["(1) 「重い」は heavy。as heavy as that one の前に three times を置く。", "(1) This box is three times as heavy as that one.",
                 "(2) 本の「数」を比べるので as many books as を使う。2倍は twice。", "(2) My brother has twice as many books as I do."],
                "(1) This box is three times as heavy as that one.　(2) My brother has twice as many books as I do.（as I have / as me も可）",
                thinking="まず「何を比べているか」（重さ・数・量）を決め、as ～ as の間に入る語（原級の形容詞か many＋名詞か）を選んでから倍数を前に置く。",
                points=[tp("(2) で as many as books と書く誤りを取り上げ、many books がひとまとまりで as と as の間に入ることを確認する。")],
                misconceptions=[("This box is three times heavier as that one.", "as ～ as の間は原級。three times as heavy as that one とする")]),
        example("ex2", "例題2　最上級と同じ内容を表す書きかえ",
                "次の文とほぼ同じ意味になるように、空所に適切な語を入れなさい。Lake Biwa is the largest lake in Japan.\n(1) No other (　　) in Japan is (　　) than Lake Biwa.\n(2) Lake Biwa is larger than (　　) (　　) lake in Japan.",
                ["(1) No other の後ろは単数名詞なので lake。後ろに than があるので比較級 larger。",
                 "(2) than any other の後ろは単数名詞なので any other。"],
                "(1) lake, larger　(2) any, other",
                thinking="no other / any other の後ろは単数名詞、all the other の後ろは複数名詞。as があれば原級、than があれば比較級。",
                points=[tp("(2) を all the other を使った形にも書きかえさせ、名詞が lakes と複数形になることを対比させる。", ask="all the other を使うと、名詞はどうなるか。",
                           expect="Lake Biwa is larger than all the other lakes in Japan. と複数形になる。")]),
        example("ex3", "例題3　the 比較級, the 比較級",
                "日本語に合うように英文を書きなさい。高く登れば登るほど、空気は冷たくなった。",
                ["元の2つの文：We climbed high. ／ The air became cold.", "high → higher、cold → colder とし、the をつけて節の先頭に出す。",
                 "The higher we climbed, the colder the air became."],
                "The higher we climbed, the colder the air became.",
                thinking="2つの文を作ってから、変化する語だけを the＋比較級にして文頭に出す。主語と動詞の語順は変えない。",
                points=[tp("後半を the air became colder のように比較級を後ろに残したままにする誤りを取り上げ、両方の節で the＋比較級が先頭に来ることを確認する。")],
                misconceptions=[("The higher we climbed, the air became colder.", "後半も the＋比較級を先頭に出す：the colder the air became")]),
        board("bd1", "板書案",
              [("① 倍数・強調", ["A is X times as 原級 as B", "twice ／ three times ／ half", "X times as many＋複数名詞 as", "X times the size of B", "much / far / even＋比較級（very ×）"]),
               ("② 最上級の意味", ["the 最上級＋名詞 in …", "＝ No other 単数 … as 原級 as A", "＝ No other 単数 … 比較級 than A", "＝ A 比較級 than any other 単数", "＝ A 比較級 than all the other 複数"]),
               ("③ the 比較級, the 比較級", ["You read many books.", "You learn much.", "→ the more books you read,", "　 the more you learn", "前半は現在形（条件）"])],
              points=[tp("②の列は単数・複数を色分けし、生徒自身に「other の後ろは何形か」を声に出して確認させる。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("倍数表現では「as と as の間は原級」を最優先で確認させる。", ask="three times as large as の large を larger にしてよいか。", expect="as ～ as の間は原級なので larger は不可。"),
               tp("比較の対象をそろえる（The population of Tokyo is larger than that of Osaka.）ことを、論説文の読解と関連づけて説明する。", caution="than Osaka と書くと「人口」と「大阪」を比べたことになる。"),
               tp("最上級の書きかえでは、単数・複数を間違えた答案が最も多い。any other と all the other を必ずセットで練習させる。", timing="例題2の後"),
               tp("the 比較級構文は、元の2つの文を書かせてから組み立てさせると、名詞の置き忘れや語順の誤りが減る。"),
               tp("問題プリント D の誤答例を使い、very＋比較級、二重比較（more taller）、than any other＋複数名詞を重点的に扱う。")],
              misconceptions=[("This problem is very more difficult than that one.", "比較級は very では強められない。much more difficult とする"),
                              ("Ken is taller than any other students in his class.", "any other の後ろは単数名詞。any other student"),
                              ("The more you study hard, the better you will do.", "hard を比較級にして先頭に出す。The harder you study, the better you will do.")]),
        summary("sm1", "まとめ",
                ["倍数表現は X times as 原級 as …。数は as many＋複数名詞、量は as much＋不可算名詞。比較級の強調は much / far / even。",
                 "最上級の意味は No other 単数 … as 原級 / 比較級 than、than any other 単数、than all the other 複数 でも表せる。",
                 "the＋比較級 ～, the＋比較級 … は2つの文の比較級を先頭に出して作る。名詞がついていれば一緒に出す。"]),
        check("ck1", "確認問題",
              [("「この部屋はあの部屋の半分の広さだ」を英語にしなさい。", "This room is half as large as that one."),
               ("Ken is the tallest boy in his class. を than any other を使って書きかえなさい。", "Ken is taller than any other boy in his class."),
               ("（　）に入る語を答えなさい。The (　　) you start, the sooner you will finish.（早く始めるほど早く終わる）", "sooner（earlier も可）")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

MULT = [
    ("This bridge", "long", "longer", "longest", "length", "that one", "この橋はあの橋の{m}の長さがある。"),
    ("My room", "large", "larger", "largest", "size", "yours", "私の部屋はあなたの部屋の{m}の広さだ。"),
    ("This box", "heavy", "heavier", "heaviest", "weight", "that one", "この箱はあの箱の{m}の重さだ。"),
    ("The tower", "tall", "taller", "tallest", "height", "the hotel next to it", "その塔は隣のホテルの{m}の高さだ。"),
    ("This lake", "deep", "deeper", "deepest", "depth", "that pond", "この湖はあの池の{m}の深さがある。"),
    ("The new library", "big", "bigger", "biggest", "size", "the old one", "新しい図書館は古い図書館の{m}の大きさだ。"),
    ("This train", "fast", "faster", "fastest", "speed", "that bus", "この列車はあのバスの{m}の速さで走る。"),
    ("The red rope", "long", "longer", "longest", "length", "the blue one", "赤いロープは青いロープの{m}の長さだ。"),
    ("Ken's bag", "heavy", "heavier", "heaviest", "weight", "mine", "ケンのかばんは私のかばんの{m}の重さだ。"),
    ("This park", "large", "larger", "largest", "size", "the one near the station", "この公園は駅の近くの公園の{m}の広さだ。"),
]
MULTS = [("twice", "2倍"), ("three times", "3倍"), ("half", "半分"), ("four times", "4倍")]


@gen("basic_check", 5, ["computation", "condition_check"])
def multiple_form(r):
    S, pos, comp, sup, noun, other, jp = r.choice(MULT)
    m, mj = r.choice(MULTS)
    s = f"{S} {'runs' if S == 'This train' else 'is'} {m} as (　　) as {other}."
    if S == "This train":
        s = f"{S} runs {m} as (　　) as {other}."
    why = {comp: (f"as ～ as の間には原級が入る。比較級 {comp} は than とともに使う形である。", "倍数表現で比較級を使う誤り"),
           sup: (f"最上級 {sup} は the とともに「いちばん～」を表す形で、as ～ as の間には入らない。", "原級と最上級の混同"),
           noun: (f"{noun} は名詞で、as ～ as の間には形容詞・副詞の原級が入る。名詞を使うなら {m} the {noun} of … の形になる。", "倍数表現の2つの形の混同")}
    return mc(f"日本語の意味になるように、（　）に入る最も適切なものを選びなさい。\n{jp.format(m=mj)}\n{s}", [pos, comp, sup, noun],
              f"{pos} が入る。倍数表現は「{m} as＋原級＋as …」の形で、as と as の間は原級。", d=1,
              ap="（　）の前後に as があることに注目する。as ～ as の間に入る形は1つしかない。",
              steps=["（　）の前後が as ～ as になっていることを確認する。", "as ～ as の間には原級が入る。", f"倍数 {m} は as ～ as の前に置かれている。答えは {pos}。"],
              alt=[f"名詞を使った言いかえ {S} {'runs at' if S == 'This train' else 'is'} {m} the {noun} of {other}. を思い出し、形容詞を使う場合は原級になることを確かめる。"],
              pc=[("as ～ as の構文に気づいている", 1), ("原級を選んでいる", 1)],
              pit=["「3倍長い」という日本語につられて比較級を選ぶ。"], why=why)


EMPH = [
    ("This problem is (　　) more difficult than the last one.", "この問題は前の問題よりずっと難しい。"),
    ("Today is (　　) colder than yesterday.", "今日は昨日よりずっと寒い。"),
    ("She can swim (　　) faster than I can.", "彼女は私よりずっと速く泳げる。"),
    ("The new phone is (　　) lighter than the old one.", "新しい電話は古いものよりずっと軽い。"),
    ("Living in the city is (　　) more convenient than living here.", "都会での生活はここでの生活よりずっと便利だ。"),
    ("Your idea is (　　) better than mine.", "あなたの考えは私の考えよりずっとよい。"),
    ("The second test was (　　) easier than the first one.", "2回目のテストは1回目よりずっと易しかった。"),
    ("This road is (　　) wider than that one.", "この道路はあの道路よりずっと広い。"),
    ("He speaks English (　　) more fluently than his brother.", "彼は兄よりずっと流ちょうに英語を話す。"),
    ("Tickets are (　　) cheaper online than at the station.", "チケットは駅よりオンラインのほうがずっと安い。"),
]


@gen("basic_check", 5, ["concept", "common_error"])
def emphasis(r):
    s, jp = r.choice(EMPH)
    ok = r.choice(["much", "far", "even", "a lot"])
    dbl = "more" if " more " not in s else "most"
    why = {"very": ("very は原級を強める副詞で、比較級を強めることはできない。", "very と much の働きの混同"),
           "so": ("so は原級を強める（so cold）語で、比較級の前には置けない。", "原級の強調と比較級の強調の混同")}
    if dbl == "more":
        why["more"] = ("more を比較級の前に置くと more colder のような二重の比較級になる。-er の比較級に more は重ねない。", "二重比較")
    else:
        why["most"] = ("most は最上級を作る語で、比較級 more ～ の前には置けない。", "比較級と最上級の混同")
    return mc(f"日本語の意味になるように、（　）に入る最も適切なものを選びなさい。\n{jp}\n{s}", [ok] + list(why),
              f"{ok} が入る。比較級を強めるときは much / far / even / a lot などを使い、very は使わない。", d=2,
              ap="（　）の直後が比較級であることを確認し、比較級を強められる語を選ぶ。",
              steps=["（　）の直後の語が比較級であることを確認する。", "比較級を強める語は much / far / even / still / a lot などである。", f"選択肢の中でそれにあたるのは {ok}。"],
              alt=["選択肢を入れた英文を音読し、very colder のように「原級を強める語＋比較級」になっていないかを確かめる。"],
              pc=[("（　）の後ろが比較級であることに気づいている", 1), ("比較級を強める語を選んでいる", 1)],
              pit=["「ずっと」「とても」を very と訳してしまう。"], why=why)


# (前半, 後半, 空所1の(正答, [(誤答, 種類)]), 空所2の(正答, [(誤答, 種類)]), 和訳)
THE_MORE = [
    ("The {0} we grow,", "the {1} we become.", ("older", [("old", "pos"), ("oldest", "sup"), ("more older", "dbl")]),
     ("wiser", [("wise", "pos"), ("wisest", "sup"), ("more wiser", "dbl")]), "年をとるほど、人は賢くなる。"),
    ("The {0} you study,", "the {1} your grades will be.", ("harder", [("hard", "pos"), ("hardest", "sup"), ("more harder", "dbl")]),
     ("better", [("good", "pos"), ("best", "sup"), ("more better", "dbl")]), "一生懸命勉強するほど、成績はよくなる。"),
    ("The {0} we climbed,", "the {1} it became.", ("higher", [("high", "pos"), ("highest", "sup"), ("more higher", "dbl")]),
     ("colder", [("cold", "pos"), ("coldest", "sup"), ("more colder", "dbl")]), "高く登るほど、寒くなった。"),
    ("The {0} you start,", "the {1} you will finish.", ("sooner", [("soon", "pos"), ("soonest", "sup"), ("more sooner", "dbl")]),
     ("earlier", [("early", "pos"), ("earliest", "sup"), ("more earlier", "dbl")]), "早く始めるほど、早く終わるだろう。"),
    ("The {0} you drive,", "the {1} you will be.", ("more carefully", [("carefully", "pos"), ("most carefully", "sup"), ("carefuller", "form")]),
     ("safer", [("safe", "pos"), ("safest", "sup"), ("more safer", "dbl")]), "注意して運転するほど、安全になる。"),
    ("The {0} I waited,", "the {1} I got.", ("longer", [("long", "pos"), ("longest", "sup"), ("more longer", "dbl")]),
     ("more nervous", [("nervous", "pos"), ("most nervous", "sup"), ("nervouser", "form")]), "待てば待つほど、私は緊張してきた。"),
    ("The {0} you speak,", "the {1} it is to understand you.", ("faster", [("fast", "pos"), ("fastest", "sup"), ("more faster", "dbl")]),
     ("more difficult", [("difficult", "pos"), ("most difficult", "sup"), ("difficulter", "form")]), "あなたが速く話すほど、言っていることを理解するのが難しくなる。"),
    ("The {0} the city is,", "the {1} the rent tends to be.", ("bigger", [("big", "pos"), ("biggest", "sup"), ("more bigger", "dbl")]),
     ("more expensive", [("expensive", "pos"), ("most expensive", "sup"), ("expensiver", "form")]), "都市が大きいほど、家賃は高くなる傾向がある。"),
    ("The {0} you sleep,", "the {1} you will feel tomorrow.", ("better", [("well", "pos"), ("best", "sup"), ("more better", "dbl")]),
     ("fresher", [("fresh", "pos"), ("freshest", "sup"), ("more fresher", "dbl")]), "よく眠るほど、明日はすっきりした気分になるだろう。"),
    ("The {0} it got,", "the {1} the stars looked.", ("darker", [("dark", "pos"), ("darkest", "sup"), ("more darker", "dbl")]),
     ("brighter", [("bright", "pos"), ("brightest", "sup"), ("more brighter", "dbl")]), "暗くなるほど、星は明るく見えた。"),
]
KIND_WHY = {
    "pos": ("the ～, the … の構文では、the の後ろに比較級が入る。原級では「～すればするほど」の比例の意味を表せない。", "the 比較級構文の形の誤り"),
    "sup": ("最上級は「いちばん～」を表す形で、the ～, the … の比例の構文には使えない。", "比較級と最上級の混同"),
    "dbl": ("-er の比較級に more を重ねると二重の比較級になり、誤り。", "二重比較"),
    "form": ("つづりの長い語や -ly の副詞は more をつけて比較級にする。-er をつけた形は存在しない。", "比較級の作り方の誤り"),
}


@gen("basic_check", 5, ["computation", "concept"])
def the_more_form(r):
    a, b, s1, s2, jp = r.choice(THE_MORE)
    slot = r.choice([0, 1])
    ok, wrongs = (s1, s2)[slot]
    fill = [s1[0], s2[0]]
    fill[slot] = "(　　)"
    s = f"{a.format(*fill)} {b.format(*fill)}"
    full = cap(f"{a.format(s1[0], s2[0])} {b.format(s1[0], s2[0])}")
    return mc(f"日本語の意味になるように、（　）に入る最も適切なものを選びなさい。\n{jp}\n{s}", [ok] + [w for w, _ in wrongs],
              f"{ok} が入る。「the＋比較級 ～, the＋比較級 …」で「～すればするほど…」を表す。完成文：{full}", d=2,
              ap="文頭の The と、コンマの後ろの the に注目する。この形は「the＋比較級」が2つ並ぶ構文である。",
              steps=["The ～, the … の形から「～すればするほど…」の構文だと判断する。", "the の後ろには比較級が入る。", f"比較級の正しい形は {ok}。"],
              alt=["元になる文（例：We grow old.）を考え、比べたい語を比較級にして the をつけ、文頭に出したかを確かめる。"],
              pc=[("構文に気づいている", 1), ("比較級の正しい形を選んでいる", 1)],
              pit=["the があるので最上級を選んでしまう。"], why={w: KIND_WHY[k] for w, k in wrongs})


# (主語, 単数名詞, 複数名詞, 原級, 比較級, 範囲, 和訳の主語, 最上級)
SUPS = [
    ("Ken", "student", "students", "tall", "taller", "in our class", "ケンはクラスでいちばん背が高い", "tallest"),
    ("Lake Biwa", "lake", "lakes", "large", "larger", "in Japan", "琵琶湖は日本でいちばん大きな湖だ", "largest"),
    ("Mt. Fuji", "mountain", "mountains", "high", "higher", "in Japan", "富士山は日本でいちばん高い山だ", "highest"),
    ("The Shinano River", "river", "rivers", "long", "longer", "in Japan", "信濃川は日本でいちばん長い川だ", "longest"),
    ("Yuki", "runner", "runners", "fast", "faster", "on the team", "ユキはチームでいちばん速い走者だ", "fastest"),
    ("This watch", "watch", "watches", "expensive", "more expensive", "in the store", "この腕時計は店でいちばん高価だ", "most expensive"),
    ("This room", "room", "rooms", "bright", "brighter", "in the school", "この部屋は学校でいちばん明るい", "brightest"),
    ("Mika", "singer", "singers", "popular", "more popular", "in the club", "ミカは部でいちばん人気のある歌い手だ", "most popular"),
    ("This dictionary", "book", "books", "useful", "more useful", "in the library", "この辞書は図書室でいちばん役に立つ本だ", "most useful"),
    ("Taro", "player", "players", "good", "better", "on the team", "タロウはチームでいちばん上手な選手だ", "best"),
]


def art(noun):
    return ("an " if noun[0] in "aeiou" else "a ") + noun


@gen("basic_check", 5, ["condition_check", "common_error"])
def other_noun(r):
    X, sg, pl, pos, comp, place, jp, _ = r.choice(SUPS)
    t = r.randrange(4)
    if t == 0:
        s, ok = f"No other (　　) {place} is {comp} than {mid(X)}.", sg
    elif t == 1:
        s, ok = f"No other (　　) {place} is as {pos} as {mid(X)}.", sg
    elif t == 2:
        s, ok = f"{X} is {comp} than any other (　　) {place}.", sg
    else:
        s, ok = f"{X} is {comp} than all the other (　　) {place}.", pl
    lead = "all the other" if t == 3 else ("No other" if t < 2 else "any other")
    if ok == sg:
        why = {pl: (f"{lead} の後ろは可算名詞の単数形。「ほかのどの1つをとっても」という意味になる。", "no other / any other の後ろの名詞の数の誤り"),
               art(sg): (f"{lead} は名詞の前につく限定詞の働きをするので、さらに a / an を重ねることはできない。", "限定詞の重複"),
               f"the {sg}": (f"{lead} の後ろに the を重ねることはできない。", "限定詞の重複")}
    else:
        why = {sg: ("all the other の後ろは複数形。「ほかのすべての～」と集団全体を指すからである。", "all the other の後ろの名詞の数の誤り"),
               art(sg): ("all the other の後ろに a / an を置くことはできず、名詞は複数形になる。", "限定詞の重複"),
               f"the {sg}": ("all the other の the と重なり、名詞も単数形なので誤り。", "限定詞の重複")}
    return mc(f"（　）に入る最も適切なものを選びなさい。\n（意味：{jp}。）\n{s}", [ok] + list(why),
              f"{ok} が入る。no other / any other の後ろは単数名詞、all the other の後ろは複数名詞。", d=2,
              ap="（　）の直前が No other / any other か、all the other かを確認する。",
              steps=[f"（　）の直前は {lead}。", "no other・any other の後ろは単数名詞、all the other の後ろは複数名詞。", f"答えは {ok}。"],
              alt=[f"最上級の文 {X} is the {_sup(X)} {sg} {place}. に戻して、意味が同じになるかを確かめる。"],
              pc=[("直前の語句を確認している", 1), ("名詞の単数・複数を正しく選んでいる", 1)],
              pit=["「ほかの生徒たち」という日本語から、any other の後ろを複数形にする。"], why=why)


def _sup(X):
    for row in SUPS:
        if row[0] == X:
            return row[7]
    return ""


# ======================================================================
# B 標準演習
# ======================================================================

FORMS = [
    ("No other", lambda X, sg, pl, pos, comp, pl_: f"No other {sg} {pl_} is {comp} than {mid(X)}."),
    ("No other", lambda X, sg, pl, pos, comp, pl_: f"No other {sg} {pl_} is as {pos} as {mid(X)}."),
    (None, lambda X, sg, pl, pos, comp, pl_: f"{X} is {comp} than any other {sg} {pl_}."),
    (None, lambda X, sg, pl, pos, comp, pl_: f"{X} is {comp} than all the other {pl} {pl_}."),
]
FORM_HINT = ["No other … 比較級 than", "No other … as 原級 as", "than any other", "than all the other"]


@gen("standard_practice", 5, ["computation", "condition_check"])
def rewrite_superlative(r):
    X, sg, pl, pos, comp, place, jp, sup = r.choice(SUPS)
    k = r.randrange(4)
    ans = FORMS[k][1](X, sg, pl, pos, comp, place)
    base = f"{X} is the {sup} {sg} {place}."
    head = "No other" if k < 2 else f"{X} is {comp} than"
    hint = {0: "（than を使うこと）", 1: "（as を使うこと）", 2: "（any を使うこと）", 3: "（all を使うこと）"}[k]
    return sa(f"次の英文とほぼ同じ意味になるように、書き出しに続けて英文を完成させなさい。{hint}\n{base}\n→ {head} ______", ans,
              f"最上級の文は、{FORM_HINT[k]} の形で書きかえられる。{'no other・any other の後ろは単数名詞' if k < 3 else 'all the other の後ろは複数名詞'}。", d=3,
              ap="書き出しと指定の語から、4つの書きかえの形（No other … than／No other … as … as／than any other／than all the other）のどれを使うかを決める。",
              steps=[f"使う形を決める：{FORM_HINT[k]}。", f"{'原級' if k == 1 else '比較級'}の形（{pos if k == 1 else comp}）を用意する。",
                     f"名詞の数を決める：{'複数形 ' + pl if k == 3 else '単数形 ' + sg}。", f"完成文：{ans}"],
              alt=["完成した文を和訳し、「～ほど…なものはほかにない」「ほかのどの～よりも…」が元の最上級の意味と一致するかを確かめる。"],
              pc=[("形の選択（原級・比較級）が正しい", 2), ("名詞の単数・複数が正しい", 2)],
              pit=["than any other の後ろを複数形にする。", "No other … as 原級 as の形で比較級を使う。"])


ORDERS = [
    ("この湖はあの湖の3倍の深さがある。", ["this lake", "is", "three times", "as deep", "as", "that one"], "倍数表現 X times as 原級 as"),
    ("この部屋はあの部屋の半分の広さだ。", ["this room", "is", "half", "as large", "as", "that one"], "倍数表現 half as 原級 as"),
    ("この本はあの本の2倍のページ数がある。", ["this book", "has", "twice", "as many", "pages", "as", "that one"], "数の倍数 twice as many＋複数名詞 as"),
    ("早く出発すればするほど、早く着くだろう。", ["the earlier", "we leave", "the sooner", "we will", "arrive"], "the 比較級 ～, the 比較級 …"),
    ("ケンはクラスのほかのどの生徒よりも速く走る。", ["Ken", "runs", "faster", "than", "any", "other", "student", "in our class"], "比較級＋than any other＋単数名詞"),
    ("彼は学者というよりむしろ作家だ。", ["he", "is", "not so much", "a scholar", "as", "a writer"], "not so much A as B「A というよりむしろ B」"),
    ("財布には千円しか入っていなかった。", ["I", "had", "no more than", "1,000 yen", "in", "my wallet"], "no more than「わずか～しか」"),
    ("その会議には500人もの人が出席した。", ["no less than", "500 people", "attended", "the", "meeting"], "no less than「～も（多く）」"),
    ("私の兄は私より3歳年上だ。", ["my brother", "is", "three years", "older", "than", "I am"], "差を表す数字＋比較級＋than"),
    ("時間ほど大切なものはない。", ["nothing", "is", "more", "important", "than", "time"], "Nothing is 比較級 than …（最上級の意味）"),
    ("彼女はチームで最も速い走者の一人だ。", ["she", "is", "one", "of the fastest", "runners", "on", "the team"], "one of the 最上級＋複数名詞"),
    ("ジョンはクラスのほかのすべての生徒より背が高い。", ["John", "is", "taller", "than", "all", "the other", "students", "in his class"], "比較級＋than all the other＋複数名詞"),
    ("この湖はあの湖の5倍の大きさだ。", ["this lake", "is", "five times", "the size", "of", "that one"], "倍数表現 X times the 名詞 of"),
]


@gen("standard_practice", 5, ["application", "computation"])
def build_order(r):
    jp, parts, pat = r.choice(ORDERS)
    if parts[0].startswith("the "):
        sent = f"{cap(parts[0])} {parts[1]}, {' '.join(parts[2:])}."
    else:
        sent = cap(" ".join(parts)) + "."
    return order(f"日本語に合うように、語句を並べかえて英文を完成させなさい。ただし、文頭にくる語も小文字で示してある。\n{jp}", parts,
                 f"{sent}　ポイントは{pat}。", d=3, p=4,
                 ap="日本語からどの比較の構文を使うかを先に決め、その構文の骨組み（as ～ as、比較級＋than など）を作ってから残りの語句を入れる。",
                 steps=[f"使う構文を決める：{pat}。", "主語と動詞を決める。", "構文の骨組みに沿って残りの語句を並べる。", f"完成文：{sent}"],
                 alt=["完成した英文を和訳し直して、日本語と一致するかを確かめる。"],
                 pc=[("構文の骨組みが正しい", 2), ("語句の順序がすべて正しい", 2)],
                 pit=["倍数を as ～ as の後ろに置く。", "many と名詞を離してしまう。"])


IDIOM = [
    ("This smartphone is superior (　　) the old model in many ways.", "to", "このスマートフォンは多くの点で古い型より優れている。",
     [("than", "superior・inferior・senior・junior など -or で終わるラテン語由来の比較の形容詞は、than ではなく to で比較の対象を示す。"),
      ("from", "superior は from をとらない。比較の対象は to で示す。"), ("with", "superior は with をとらない。比較の対象は to で示す。")]),
    ("I prefer tea (　　) coffee.", "to", "私はコーヒーより紅茶が好きだ。",
     [("than", "prefer A to B「B より A を好む」では、比較の対象を to で示す。"), ("from", "prefer は from で比較の対象を示さない。"), ("for", "prefer A for B という比較の形はない。")]),
    ("Ms. Kato is three years senior (　　) me.", "to", "加藤さんは私より3歳年上だ。",
     [("than", "senior は than ではなく to で比較の対象を示す。"), ("from", "senior は from をとらない。"), ("for", "senior は for をとらない。")]),
    ("This hotel is inferior (　　) that one in service.", "to", "このホテルはサービスの点であのホテルに劣る。",
     [("than", "inferior は than ではなく to で比較の対象を示す。"), ("from", "inferior は from をとらない。"), ("with", "inferior は with をとらない。")]),
    ("She knows (　　) than to believe such a story.", "better", "彼女はそんな話を信じるほど愚かではない。",
     [("more", "know better than to do「～するほど愚かではない」は better を使う決まった表現。"), ("best", "than の前には比較級が必要で、最上級は使えない。"),
      ("good", "than の前には比較級が必要で、原級は使えない。")]),
    ("Of the two sisters, Emi is (　　) taller.", "the", "2人の姉妹のうち、エミのほうが背が高い。",
     [("a", "「2つのうちで～のほうが」と1つに特定するときは the＋比較級（the taller of the two）。"), ("more", "taller はすでに比較級なので more を重ねられない。"),
      ("most", "most を比較級 taller の前に置くことはできない。")]),
    ("I like him all the (　　) for his honesty.", "more", "彼は正直なので、私はなおさら彼が好きだ。",
     [("most", "all the＋比較級＋for ～「～だからなおさら」の形で、最上級は使えない。"), ("much", "all the の後ろには比較級が入る。much は原級。"),
      ("many", "all the の後ろには比較級が入る。many は原級で、しかも数えられる名詞の数を表す語。")]),
    ("The population of Tokyo is larger than (　　) of Osaka.", "that", "東京の人口は大阪の人口より多い。",
     [("it", "it は前に出た名詞そのもの（東京の人口）を指してしまう。別の都市の人口を指すには that of を使う。"),
      ("those", "those は複数名詞を受ける。the population は単数なので that を使う。"), ("this", "比較の対象として前の名詞の代わりをするのは that。this は使わない。")]),
    ("The ears of a rabbit are longer than (　　) of a cat.", "those", "ウサギの耳はネコの耳より長い。",
     [("that", "that は単数名詞を受ける。the ears は複数なので those を使う。"), ("it", "it は単数で、しかも前の名詞そのものを指す。"),
      ("them", "them は代名詞の目的格で、後ろに of ～ をつけて名詞の代わりをすることはできない。")]),
    ("I would rather stay home (　　) go out tonight.", "than", "今夜は出かけるより家にいたい。",
     [("to", "would rather A than B「B するより A したい」では than を使う。"), ("as", "would rather の比較の対象は than で示す。"),
      ("from", "would rather の比較の対象は than で示す。")]),
    ("This lake is twice the (　　) of that one.", "size", "この湖はあの湖の2倍の大きさだ。",
     [("large", "twice the ～ of … の形では the の後ろに名詞が入る。large は形容詞。"), ("larger", "the の後ろに名詞が入る形で、比較級は使えない。"),
      ("largest", "最上級を使うと「2倍」という意味にならない。名詞 size が必要。")]),
    ("Which do you like better, summer (　　) winter?", "or", "夏と冬では、どちらのほうが好きですか。",
     [("than", "Which … better, A or B? の形で選択肢を示すので or を使う。"), ("and", "and では「どちらか」を選ばせる疑問文にならない。"),
      ("to", "Which … better の疑問文では、選択肢を to でつながない。")]),
    ("Taro is the (　　) of the two brothers.", "older", "タロウは2人の兄弟のうち年上のほうだ。",
     [("oldest", "2人（2つ）の中で比べるときは the＋比較級を使う。最上級は3つ以上の中で使う。"), ("old", "the old of … という形は比較の意味を表さない。"),
      ("more older", "older に more を重ねると二重の比較級になる。")]),
    ("He is (　　) a genius than I am.", "no more", "私が天才でないのと同様に、彼も天才ではない。",
     [("no less", "no less A than B は「B に劣らず A だ」という肯定の意味になり、日本語と逆になる。"),
      ("much more", "much more a genius than I am では「私よりずっと天才だ」という意味になる。"),
      ("not more", "not more A than B は「B ほど A ではない」で、両者をともに否定する意味にはならない。")]),
]


@gen("standard_practice", 5, ["condition_check", "concept"])
def idiom_fill(r):
    s, ok, jp, wrongs = r.choice(IDIOM)
    return mc(f"日本語の意味になるように、（　）に入る最も適切なものを選びなさい。\n{jp}\n{s}", [ok] + [w for w, _ in wrongs],
              f"{ok} が入る。比較の決まった表現では、比較の対象を示す語（than / to / or）や、比較級・名詞の形が決まっている。", d=3,
              ap="空所の前後から、どの比較の決まった形（-or の形容詞＋to、the 比較級 of the two、that / those of など）が使われているかを判断する。",
              steps=["空所の前後の語句と日本語の意味を確認する。", "使われている比較の決まった形を特定する。", f"その形に合う {ok} を選ぶ。"],
              alt=["選択肢を入れた英文を1つずつ和訳し、日本語と一致するものを選ぶ。"],
              pc=[("比較の決まった形に気づいている", 2), ("正しい語を選んでいる", 2)],
              pit=["比較の対象はいつも than で示すと思い込む。"], why={w: (reason, "比較の決まった表現の語法の誤り") for w, reason in wrongs})


EXPRS = ["no more than", "no less than", "not more than", "not less than"]
NOBJ = [
    ("{E} {n} students came to the lecture.", "講演に来た生徒", "人", ["20", "30", "40"]),
    ("I spent {E} {n} yen on lunch.", "私が昼食に使ったお金", "円", ["500", "800", "1,000"]),
    ("The trip took {E} {n} hours.", "旅行にかかった時間", "時間", ["3", "5", "6"]),
    ("The festival attracted {E} {n} visitors.", "祭りの来場者", "人", ["2,000", "3,000", "5,000"]),
    ("He read {E} {n} books last summer.", "彼が去年の夏に読んだ本", "冊", ["10", "20", "30"]),
    ("The repair cost {E} {n} yen.", "修理代", "円", ["3,000", "5,000", "10,000"]),
]
EXPR_JP = {
    "no more than": "は、わずか{n}{u}だった（少ないという気持ち）。",
    "no less than": "は、{n}{u}にものぼった（多いという気持ち）。",
    "not more than": "は、多くても{n}{u}だった（{n}{u}以下）。",
    "not less than": "は、少なくとも{n}{u}だった（{n}{u}以上）。",
}
EXPR_RULE = {
    "no more than": "no more than＝only。no が「差がゼロ」を表し、「多い」の反対の「少ない」という話し手の気持ちが加わる",
    "no less than": "no less than＝as many / much as。no が「差がゼロ」を表し、「少ない」の反対の「多い」という話し手の気持ちが加わる",
    "not more than": "not more than＝at most。「～より多くはない」という客観的な上限を表す",
    "not less than": "not less than＝at least。「～より少なくはない」という客観的な下限を表す",
}


@gen("standard_practice", 5, ["concept", "common_error"])
def no_more_than(r):
    tmpl, subj, u, ns = r.choice(NOBJ)
    n = r.choice(ns)
    e = r.choice(EXPRS)
    s = tmpl.replace("{E}", e).replace("{n}", n)
    s = cap(s)
    opts = {x: subj + EXPR_JP[x].format(n=n, u=u) for x in EXPRS}
    return mc(f"次の英文の意味として最も適切なものを選びなさい。\n{s}", [opts[e]] + [opts[x] for x in EXPRS if x != e],
              f"{EXPR_RULE[e]}。", d=3,
              ap="no と not のどちらが使われているか、more と less のどちらが使われているかの2点を確かめる。no は話し手の気持ち（少ない・多い）、not は客観的な範囲（以下・以上）を表す。",
              steps=[f"使われている表現は {e}。", f"{EXPR_RULE[e]}。", "その意味に合う和訳を選ぶ。"],
              alt=[f"{e} を {'only' if e == 'no more than' else 'as many / much as' if e == 'no less than' else 'at most' if e == 'not more than' else 'at least'} に置きかえて意味を確かめる。"],
              pc=[("no と not の違いを理解している", 2), ("more と less の違いを理解している", 2)],
              pit=["no more than を「～以下」、not more than を「わずか」と取り違える。"],
              why={opts[x]: (f"この和訳は {x} の意味である。{EXPR_RULE[x]}。問題文は {e}。", "no / not と more / less の組み合わせの混同") for x in EXPRS if x != e})


# ======================================================================
# C 思考力・記述応用
# ======================================================================

PAIRS = [
    ("He has no more than 1,000 yen.", "He has not more than 1,000 yen.",
     "Aの no more than は only と同じで「彼はわずか1,000円しか持っていない」と、少ないという話し手の気持ちを表す。Bの not more than は at most と同じで「彼が持っているのは多くても1,000円だ」と、金額の上限を客観的に述べている。"),
    ("No less than 300 people came.", "Not less than 300 people came.",
     "Aの no less than は as many as と同じで「300人もの人が来た」と、多いという話し手の気持ちを表す。Bの not less than は at least と同じで「少なくとも300人は来た」と、人数の下限を客観的に述べている。"),
    ("He is not so much a scholar as a writer.", "He is not so much a writer as a scholar.",
     "not so much A as B は「A というよりむしろ B」の意味で、B のほうに重点がある。Aは「彼は学者というよりむしろ作家だ」、Bは「彼は作家というよりむしろ学者だ」となり、A と B を入れかえると意味が逆になる。"),
    ("She is the tallest girl in the class.", "She is one of the tallest girls in the class.",
     "Aは「彼女はクラスでいちばん背の高い女子だ」で、1位が彼女1人に決まる。Bは one of the＋最上級＋複数名詞で「彼女はクラスで最も背の高い女子の1人だ」となり、背の高い上位のグループに含まれることを表すだけで、1位とは限らない。"),
    ("He is no more a genius than I am.", "He is no less a genius than his father.",
     "Aは A is no more B than C is (B) の形で「私が天才でないのと同様に、彼も天才ではない」と両方を否定する。Bは no less B than C で「彼は父親に劣らず天才だ」と、両方が天才であることを肯定する。"),
    ("This is the most interesting book I have ever read.", "I have never read a more interesting book than this.",
     "Aは最上級＋経験の完了形で「これは私が今まで読んだ中でいちばんおもしろい本だ」。Bは never＋比較級で「これよりおもしろい本を読んだことがない」となり、比較級を使って同じ最上級の意味を表している。2つはほぼ同じ意味である。"),
    ("I have three times as many books as you.", "You have a third as many books as I do.",
     "Aは「私はあなたの3倍の数の本を持っている」。Bは「あなたは私の3分の1の数の本を持っている」。主語を入れかえ、倍数を3倍から3分の1にしたので、2つは同じ事実を表している。"),
    ("Emi is the taller of the two.", "Emi is the tallest of the three.",
     "Aは2人の中で比べているので the＋比較級を使い「エミは2人のうちで背が高いほうだ」。Bは3人の中で比べているので the＋最上級を使い「エミは3人の中でいちばん背が高い」。比べる数が2つか3つ以上かで比較級と最上級を使い分けている。"),
]


@gen("thinking_writing", 4, ["written_reasoning", "concept"])
def explain_pair(r):
    a, b, model = r.choice(PAIRS)
    return desc(f"次の2つの英文A・Bの意味を比べ、違い（または同じ意味になる理由）を、使われている比較の形に触れながら日本語で説明しなさい。\nA：{a}\nB：{b}", model,
                "比較の表現は、no / not、比較級 / 最上級、A と B の順序などの小さな違いで意味が大きく変わる。形の違いを根拠にして意味を説明する。",
                [("Aの形と意味を正しく説明している", 3), ("Bの形と意味を正しく説明している", 3), ("2つの関係（違い・同じ点）を明確に述べている", 2)], d=4, p=8, lines=6,
                ap="2つの文で違う部分（no / not、more / less、語順、比較級 / 最上級）を先に丸で囲み、その部分の働きを説明する。",
                steps=["A・B で形が違う部分を見つける。", "それぞれの形が表す意味を確認する。", "和訳を示し、違い（または同じになる理由）をまとめる。"],
                alt=["それぞれの文を only / at most / at least / rather などを使った別の表現に言いかえて、意味の違いを示す。"],
                pc=[("Aの説明", 3), ("Bの説明", 3), ("関係のまとめ", 2)],
                pit=["和訳だけを並べ、どの形が意味の違いを生んでいるかを説明しない。"])


CTX = [
    dict(title="ある高校の図書室で先月貸し出された本の冊数（架空の資料）", cats=["novels", "science books", "history books", "art books"],
         cats_jp=["小説", "科学の本", "歴史の本", "美術の本"], unit="冊",
         s1=lambda k, a, b: f"{k} as many {a} as {b} were borrowed last month.",
         s2=lambda a: f"{cap(a)} were borrowed more often than any other kind of book."),
    dict(title="ある美術館の曜日別の来館者数（架空の資料）", cats=["Sunday", "Saturday", "Friday", "Monday"],
         cats_jp=["日曜日", "土曜日", "金曜日", "月曜日"], unit="人",
         s1=lambda k, a, b: f"{cap(k)} as many people visited the museum on {a} as on {b}.",
         s2=lambda a: f"More people visited the museum on {a} than on any other day."),
    dict(title="ある高校の部活動の部員数（架空の資料）", cats=["the soccer club", "the brass band", "the art club", "the chess club"],
         cats_jp=["サッカー部", "吹奏楽部", "美術部", "チェス部"], unit="人",
         s1=lambda k, a, b: f"{cap(a)} has {k} as many members as {b}.",
         s2=lambda a: f"{cap(a)} has more members than any other club."),
]
KWORD = {2: "twice", 3: "three times", 4: "four times"}


@gen("thinking_writing", 3, ["cross_unit", "application", "computation"], rel=["HS-MATH1-U05", "HS-ENG-U09"])
def data_sentences(r):
    c = r.choice(CTX)
    k = r.choice([2, 3, 4])
    low = r.choice([10, 12, 15, 20, 24, 30])
    top = k * low
    idx = list(range(4))
    r.shuffle(idx)
    ti, li, m1, m2 = idx
    vals = [0] * 4
    vals[ti], vals[li] = top, low
    mids = r.sample(range(low + 1, top), 2)
    vals[m1], vals[m2] = mids
    rows = "、".join(f"{c['cats_jp'][i]} {vals[i]}{c['unit']}" for i in range(4))
    a, b = c["cats"][ti], c["cats"][li]
    s1 = cap(c["s1"](KWORD[k], a, b))
    s2 = c["s2"](a)
    return desc(f"次の表（{c['title']}）を見て、指示に従って英文を書きなさい。\n［表］{rows}\n(1) {c['cats_jp'][ti]}と{c['cats_jp'][li]}の数を、倍数表現を使って比べる英文を1文書きなさい。\n(2) {c['cats_jp'][ti]}がいちばん多いことを、最上級を使わずに比較級を使って1文で書きなさい。",
                f"(1) {s1}　(2) {s2}",
                f"{vals[ti]}÷{vals[li]}＝{k} なので {KWORD[k]} as many … as を使う。(2) は「比較級＋than any other＋単数名詞」で最上級の意味を表す。",
                [("(1) 倍率を正しく読み取り、倍数表現を正しく使っている", 4), ("(2) 比較級を使って最上級の意味を正しく表している", 4)], d=4, p=8, lines=5,
                ap="まず表の数値から倍率を計算し、次に「数」を比べるので as many＋複数名詞 as を使うことを決める。(2) は than any other を使う。",
                steps=[f"倍率を計算する：{vals[ti]}÷{vals[li]}＝{k}。", f"(1) {KWORD[k]} as many … as の形で書く：{s1}",
                       f"(2) いちばん多いことを than any other で表す：{s2}"],
                alt=[f"(1) は少ない側（{c['cats_jp'][li]}）を主語にして、{'half' if k == 2 else 'a third' if k == 3 else 'a quarter'} as many … as の形で書くこともできる。",
                     "(2) は No other … を主語にして書くこともできる。"],
                pc=[("倍率の読み取り", 2), ("倍数表現の形", 2), ("than any other の形と単数名詞", 4)],
                pit=["数の比較で as many を使わず as much や as large を使う。", "than any other の後ろを複数形にする。"],
                chk=(f"{vals[ti]}/{vals[li]}", str(k), None, "intermediate"))


THE_COMP = [
    ("年をとればとるほど、時間が早く過ぎるように感じる。", "The older we get, the faster time seems to pass.", "We get old. ／ Time seems to pass fast."),
    ("高く登れば登るほど、空気は薄くなった。", "The higher we climbed, the thinner the air became.", "We climbed high. ／ The air became thin."),
    ("本を読めば読むほど、知識が増える。", "The more books you read, the more knowledge you gain.", "You read many books. ／ You gain much knowledge."),
    ("その問題について考えれば考えるほど、わからなくなった。", "The more I thought about the problem, the more confused I became.", "I thought a lot about the problem. ／ I became confused."),
    ("練習を重ねれば重ねるほど、自信がついた。", "The more I practiced, the more confident I felt.", "I practiced a lot. ／ I felt confident."),
    ("部屋が広ければ広いほど、家賃は高くなる。", "The larger the room is, the higher the rent will be.", "The room is large. ／ The rent will be high."),
    ("外国語を早く学び始めるほど、上達も早い。", "The earlier you start learning a foreign language, the faster you will improve.", "You start learning a foreign language early. ／ You will improve fast."),
    ("友達が多ければ多いほど、学校生活は楽しくなる。", "The more friends you have, the more enjoyable your school life will be.", "You have many friends. ／ Your school life will be enjoyable."),
]


@gen("thinking_writing", 3, ["cross_unit", "written_reasoning"], rel=["JH-ENG-G2-U04", "HS-ENG-U10"])
def compose_the_more(r):
    jp, ans, base = r.choice(THE_COMP)
    return desc(f"次の日本語を「the＋比較級 ～, the＋比較級 …」の構文を使って英語に直しなさい。また、その英文を、元になる2つの文からどのように組み立てたかを説明しなさい。\n{jp}",
                f"{ans}　（元の2つの文：{base} それぞれの文の比べたい語を比較級にし、the をつけて節の先頭に出した。比較級が名詞を修飾している場合は名詞も一緒に前に出す。）",
                "the＋比較級の構文は、2つの文の比較級を the とともに文頭に出して作る。主語と動詞の語順はそのまま残す。",
                [("英文が正しい", 4), ("元になる2つの文を示している", 2), ("比較級を the とともに先頭に出す手順を説明している", 2)], d=4, p=8, lines=6,
                ap="まず日本語を2つの文に分け、それぞれを英語にする。次に比べたい語を比較級にして the をつけ、節の先頭に移動する。",
                steps=[f"元になる2つの文を作る：{base}", "比べたい語を比較級にする（many / much / a lot → more、old → older など）。",
                       "the＋比較級（＋名詞）を節の先頭に出し、残りは主語＋動詞の順に並べる。", f"2つの節をコンマでつなぐ：{ans}"],
                alt=["As 主語＋動詞＋比較級, 主語＋動詞＋比較級.（As we get older, time seems to pass faster.）のように as を使って書いても、ほぼ同じ意味を表せる。"],
                pc=[("英文", 4), ("元の2つの文", 2), ("組み立て方の説明", 2)],
                pit=["比較級が修飾する名詞を後ろに残す（The more you read books）。", "後半の比較級を文末に残す。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(task, wrong, step, etype, tempt, fix, expl, steps, ap, alt, pit):
    return desc(f"{task}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい英文に書き直しなさい。", fix, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい英文に直している", 3), ("比較の規則を説明している", 1)], d=3, p=6, lines=5,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい英文", 3), ("規則の説明", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix))


FORM_ERR = [
    ("この問題はあの問題よりずっと難しい。", "This problem is very more difficult than that one.", "This problem is much more difficult than that one.", "very", "concept",
     "比較級を強めるのは much / far / even などで、very は使えない。", "「ずっと」「とても」を very で表す習慣につられた。"),
    ("彼はクラスでいちばん背が高い。", "He is the most tallest student in his class.", "He is the tallest student in his class.", "most tallest", "formula",
     "tallest はすでに最上級なので most を重ねない（二重最上級）。", "長い語の most ～ の形と、-est の形を同時に使った。"),
    ("この箱はあの箱の3倍の重さだ。", "This box is three times as heavier as that one.", "This box is three times as heavy as that one.", "as heavier as", "formula",
     "倍数表現の as ～ as の間は原級。", "「3倍重い」という日本語から比較級を使った。"),
    ("エミは姉より2歳年下だ。", "Emi is younger two years than her sister.", "Emi is two years younger than her sister.", "younger two years", "notation",
     "差を表す数字は比較級の直前に置く（two years younger than）。", "日本語の「年下だ、2歳」の語順につられた。"),
    ("今日は昨日よりもっと暑い。", "Today is more hotter than yesterday.", "Today is even hotter than yesterday.", "more hotter", "formula",
     "hotter はすでに比較級なので more を重ねない。「もっと」と強めるなら even / much を使う。", "「もっと」を more で表そうとした。"),
    ("このスマートフォンは古い型より優れている。", "This smartphone is superior than the old model.", "This smartphone is superior to the old model.", "superior than", "concept",
     "superior は than ではなく to で比較の対象を示す。", "「～より」をすべて than で表すと思い込んだ。"),
    ("私の部屋はあなたの部屋の半分の広さだ。", "My room is half as larger as yours.", "My room is half as large as yours.", "as larger as", "formula",
     "half as ～ as の間も原級。", "「半分」と比べているので比較級が必要だと考えた。"),
    ("この本はあの本の2倍のページ数がある。", "This book has twice as many page as that one.", "This book has twice as many pages as that one.", "many page", "notation",
     "many の後ろの可算名詞は複数形。", "倍数表現の語順に気をとられ、名詞の数を確認しなかった。"),
    ("彼女は2人のうちで背が高いほうだ。", "She is the tallest of the two.", "She is the taller of the two.", "the tallest", "condition",
     "2人（2つ）の中で比べるときは the＋比較級。最上級は3つ以上の中で使う。", "the があるので最上級を使うと考えた。"),
]


@gen("error_correction", 5, ["common_error", "computation"])
def err_form(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(FORM_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", etype, tempt, fix, f"{rule}正しくは {fix}",
                    ["比較の形（原級・比較級・最上級）と、それを強める語・差を表す語の位置を確認する。", f"「{where}」の部分を直す。", f"正しい英文：{fix}"],
                    "比較の形の誤りは、①as ～ as の間は原級か、②比較級・最上級に more / most を重ねていないか、③強める語は much / far / even か、の順に点検する。",
                    ["直した英文を和訳し直し、日本語の意味と一致するかを確かめる。"],
                    ["very＋比較級、more＋-er、most＋-est の形を書いてしまう。"])


STRUCT_ERR = [
    ("ケンはクラスのほかのどの生徒よりも背が高い。", "Ken is taller than any other students in his class.", "Ken is taller than any other student in his class.", "any other students", "notation",
     "any other の後ろは単数名詞。", "「ほかの生徒たち」という日本語から複数形にした。"),
    ("クラスでマイほど親切な生徒はいない。", "No other students in the class is as kind as Mai.", "No other student in the class is as kind as Mai.", "No other students", "notation",
     "no other の後ろは単数名詞で、動詞も is で受ける。", "「ほかの生徒たち」という日本語から複数形にした。"),
    ("一生懸命勉強すればするほど、よい成績がとれる。", "The more you study hard, the better grades you will get.", "The harder you study, the better grades you will get.", "The more you study hard", "formula",
     "比べているのは hard（一生懸命さ）なので、hard を比較級 harder にして the とともに先頭に出す。", "「もっと」を the more で表し、hard を元の位置に残した。"),
    ("年をとればとるほど、賢くなる。", "The older we grow, we become wiser.", "The older we grow, the wiser we become.", "we become wiser", "formula",
     "後半も the＋比較級を節の先頭に出す。", "前半だけで構文が完成したと考え、後半を普通の語順で書いた。"),
    ("東京の人口は大阪の人口より多い。", "The population of Tokyo is larger than Osaka.", "The population of Tokyo is larger than that of Osaka.", "than Osaka", "logic",
     "比べるのは「東京の人口」と「大阪の人口」なので、than の後ろも人口を表す that of Osaka にする。", "日本語の「大阪より多い」という言い方につられ、比べる対象をそろえなかった。"),
    ("彼はチームで最もうまい選手の1人だ。", "He is one of the best player on the team.", "He is one of the best players on the team.", "the best player", "notation",
     "one of the＋最上級の後ろは複数名詞。", "「1人」という日本語につられて単数形にした。"),
    ("私の犬の耳は私の猫の耳より長い。", "My dog's ears are longer than my cat.", "My dog's ears are longer than those of my cat.", "than my cat", "logic",
     "比べるのは耳どうしなので、than の後ろは those of my cat（または my cat's）にする。", "比べる対象をそろえることを忘れた。"),
    ("私はあなたの2倍の数の本を持っている。", "I have twice as many books than you.", "I have twice as many books as you do.", "than you", "formula",
     "as many ～ as の形なので、後ろも as で受ける。than は比較級とともに使う。", "「～より」の意味から than を使った。"),
    ("健康ほど大切なものはない。", "Nothing is so important than health.", "Nothing is as important as health.", "so important than", "formula",
     "as（so）～ as を使うか、比較級＋than を使うか、どちらかにそろえる（Nothing is more important than health. も可）。", "原級の構文と比較級の構文を混ぜてしまった。"),
]


@gen("error_correction", 5, ["common_error", "condition_check"])
def err_structure(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(STRUCT_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", etype, tempt, fix, f"{rule}正しくは {fix}",
                    ["構文の型（as ～ as／比較級＋than／the 比較級, the 比較級／one of the 最上級）を確認する。", f"「{where}」の部分を、構文の型と比べる対象に合わせて直す。", f"正しい英文：{fix}"],
                    "比較の文は、①構文の型がそろっているか（as と as、比較級と than）、②比べる対象がそろっているか、③名詞の単数・複数が正しいか、を順に点検する。",
                    ["直した英文の比べる対象（何と何を比べているか）に下線を引き、同じ種類のものになっているかを確かめる。"],
                    ["any other / no other の後ろを複数形にする。", "than の後ろで比べる対象をそろえない。"])


GENERATORS = [multiple_form, emphasis, the_more_form, other_noun,
              rewrite_superlative, build_order, idiom_fill, no_more_than,
              explain_pair, data_sentences, compose_the_more,
              err_form, err_structure]
