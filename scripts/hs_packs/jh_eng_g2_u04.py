"""単元パック：中学2年 英語 比較（比較級・最上級・as ～ as・不規則変化）。"""
from banks._common import desc, mc, order, sa, table
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem,
                         tp)

UNIT_ID = "JH-ENG-G2-U04"

PREREQUISITES = [
    ("JH-ENG-G1-U01", "be 動詞の文と一般動詞の文の区別。Ken is tall. / Ken runs fast. のように、形容詞は be 動詞の後ろ、副詞は一般動詞の後ろに置くこと。"),
    ("JH-ENG-G1-U03", "疑問詞 which / who を使った疑問文。Which is longer, A or B? / Who runs the fastest? で使う。"),
    ("JH-ENG-G1-U02", "名詞の複数形。one of the ＋最上級＋複数名詞 や of the five students の形で使う。"),
]
EXTENSIONS = [
    ("JH-ENG-G3-U06", "グラフや表を読み取る長文問題で、比較級・最上級を使った説明文や設問が多く出る。"),
    ("JH-ENG-G3-U07", "条件英作文で「A と B のどちらがよいか」を、比較級を使って意見と理由として書く。"),
    ("HS-ENG-U07", "高校では、倍数表現（twice as ～ as）、比較級＋and＋比較級、the＋比較級, the＋比較級、no other ～ などの比較表現を学ぶ。"),
]


def cap(s):
    return s[0].upper() + s[1:]


# ======================================================================
# 授業プリント
# ======================================================================

LESSON = lesson(
    goals=["形容詞・副詞の比較級（-er / more ～）と最上級（-est / most ～）を、つづりのルールと不規則変化に注意して作れる。",
           "〈比較級＋than ～〉〈the＋最上級＋in / of ～〉〈as＋原級＋as ～〉を使って、2つ以上のものを比べる文を作れる。",
           "Which ～ better, A or B? / Who ～ the ～est? などの疑問文に答え、表やデータを比較の文で説明できる。"],
    duration=50,
    readiness=["形容詞（tall, big, beautiful など）と副詞（fast, well など）を文の中で使える（中1）。",
               "which / who を使った疑問文を作り、答えられる（中1）。",
               "小学校の外国語で、What's your favorite ～? や I like ～. などで好きなものを伝えた経験がある。",
               "小学校の算数で、表やグラフから「いちばん大きい」「同じ」などを読み取ることができる。"],
    flow=[("導入：2人の身長を比べる", 5, "教師と生徒の身長を比べ、I'm taller than you. を引き出す"),
          ("比較級・最上級の作り方", 12, "-er / -est のつづり4パターン、more / most、不規則変化（例題1）"),
          ("比較級・最上級の文", 13, "than、the＋最上級＋in / of、Which ～, A or B?、like ～ better / the best（例題2）"),
          ("as ～ as", 10, "as＋原級＋as、not as ～ as の意味（例題3）"),
          ("まとめと確認", 10, "表を見て比較の文を作る活動と、確認問題3問")],
    sections=[
        intro("in1", "「どちらが」「どれがいちばん」「同じくらい」を英語で",
              "身長、年齢、好きな季節など、私たちはふだんから2つ以上のものを比べて話しています。英語では、形容詞や副詞の形を変えることで「より～」「いちばん～」を表し、as ～ as で「同じくらい～」を表します。この単元では、形の変え方と、比べる相手を示す語（than / in / of / as）の使い方を学びます。",
              bullets=["Ken is tall.（ケンは背が高い）", "Ken is taller than Tom.（ケンはトムより背が高い）",
                       "Ken is the tallest in his class.（ケンはクラスでいちばん背が高い）", "Ken is as tall as his father.（ケンは父親と同じくらい背が高い）"],
              points=[tp("4つの文を並べ、tall の形と、その後ろの語（than / in / as）がセットで変わっていることに気づかせる。",
                         ask="tall がどう変わったか、後ろに何がついたかを探そう。", expect="taller＋than、the tallest＋in、as tall as。", timing="導入の冒頭")]),
        definition("df1", "比較級・最上級の作り方",
                   "形容詞・副詞のもとの形を原級といいます。比較級（より～）と最上級（いちばん～）は、語の長さやつづりによって作り方が決まっています。",
                   formula="原級 → 比較級（-er / more ～）→ 最上級（-est / most ～）",
                   bullets=["ふつうの語：-er / -est（tall → taller → tallest）",
                            "e で終わる語：-r / -st（large → larger → largest）",
                            "〈短母音＋子音字〉で終わる語：子音字を重ねる（big → bigger → biggest、hot → hotter → hottest）",
                            "〈子音字＋y〉で終わる語：y を i にかえる（easy → easier → easiest、early → earlier → earliest）",
                            "長い語（beautiful, interesting, difficult, popular など）：more / most をつける",
                            "不規則変化：good / well → better → best、many / much → more → most、bad → worse → worst"],
                   conditions=["-er と more を同時に使わない（× more taller）。", "長い語に -er / -est をつけない（× beautifuller）。",
                               "最上級の前には、ふつう the をつける（the tallest）。"],
                   points=[tp("つづりのルールは ing 形（running, making）と似ていることを思い出させ、比べながら覚えさせる。",
                              ask="big の比較級は？ run の ing 形と何が似ている？", expect="bigger。どちらも最後の子音字を重ねる。"),
                           tp("good と well がどちらも better / best になることを、例文（Ken is a good player. / Ken plays well.）で確認する。", timing="定義の説明後")]),
        theorem("th1", "比較の3つの文の形",
                "A＋動詞＋比較級＋than B.｜A＋動詞＋the＋最上級＋in / of ～.｜A＋動詞＋as＋原級＋as B.",
                ["比較級の文：Ken is taller than Tom.（ケンはトムより背が高い）",
                 "最上級の文：in＋場所・集団（in my class, in Japan）、of＋複数を表す語句（of the three, of all）を使い分ける。",
                 "as ～ as の文：as と as の間は原級（as tall as）。not as ～ as は「…ほど～ではない」。",
                 "疑問文：Which is longer, A or B? ― A is.／Who runs the fastest in your class? ― Ken does.",
                 "好み：I like A better than B.（B より A が好き）／I like A the best of all.（すべての中で A がいちばん好き）"],
                body="than / in・of / as のどれを使うかは、「2つを比べる」「3つ以上の中でいちばん」「同じくらい」のどれを言いたいかで決まります。",
                points=[tp("in と of の使い分けは、「in＋1つの集まりの名前（my class）」「of＋数や all」と整理させる。",
                           ask="the tallest ( ) the five boys と the tallest ( ) my family にはそれぞれ何が入る？", expect="of と in。",
                           caution="of my class / in all のような誤りが多い。")]),
        derivation("dv1", "not as ～ as の意味はなぜ「…ほど～ではない」になるのか",
                   ["① Tom is as tall as Ken. は「トムはケンと同じくらいの背の高さだ」という意味。",
                    "② これを not で打ち消すと「トムはケンと同じくらいの背の高さではない」となる。",
                    "③ 英語の as ～ as は「少なくとも同じくらい～」という感じを表すので、その否定は「同じくらいまで届いていない」、つまり「ケンより低い」ことを表す。",
                    "④ したがって Tom is not as tall as Ken. ＝ Tom is shorter than Ken. ＝ Ken is taller than Tom. と言いかえられる。",
                    "⑤ 「ケンのほうが高い」という事実を、主語を変えたり、反対の意味の語（tall ⇔ short）を使ったりして、いろいろな形で表せる。"],
                   body="同じ事実を、比較級・as ～ as・反対語の3つの方法で言いかえられるようにしておくと、読み取り問題や書きかえ問題に強くなります。",
                   points=[tp("2人の生徒に前に出てもらい、実際に背の高さを比べながら④の3つの文を言わせると、意味の対応がはっきりする。",
                              ask="Tom is not as tall as Ken. のとき、背が高いのはどちらか。", expect="ケン。",
                              caution="「トムはケンほど背が高くない」を「トムのほうが高くない＝同じ」と誤解する生徒がいるので、図で示す。", timing="導出の説明時")]),
        example("ex1", "例題1　比較級・最上級を作る",
                "次の語の比較級と最上級を書きなさい。(1) hot　(2) easy　(3) popular　(4) good",
                ["(1) hot は〈短母音＋子音字〉で終わるので t を重ねる：hotter, hottest。",
                 "(2) easy は〈子音字＋y〉で終わるので y を i にかえる：easier, easiest。",
                 "(3) popular は長い語なので more / most をつける：more popular, most popular。",
                 "(4) good は不規則変化：better, best。"],
                "(1) hotter, hottest　(2) easier, easiest　(3) more popular, most popular　(4) better, best",
                thinking="語尾のつづりと語の長さを見て、4つのルールと不規則変化のどれに当たるかを先に決める。",
                points=[tp("(3) を popularer とする誤りを取り上げ、「長い語は more / most」の目安（3音節以上の語の多くと、-ful / -ous などで終わる語）を示す。")],
                misconceptions=[("hot → hoter, hotest", "子音字 t を重ねて hotter, hottest。"), ("good → gooder, goodest", "不規則変化。better, best。")]),
        example("ex2", "例題2　比較の文を作る",
                "日本語に合う英文を書きなさい。(1) この問題はあの問題より難しい。　(2) 富士山は日本でいちばん高い山です。　(3) あなたは夏と冬ではどちらが好きですか。",
                ["(1) difficult は長い語なので more difficult than。",
                 "(2) high の最上級 the highest。「日本で」は場所なので in Japan。",
                 "(3) 2つのうちどちらが好きかは Which do you like better, A or B?"],
                "(1) This question is more difficult than that one.　(2) Mt. Fuji is the highest mountain in Japan.　(3) Which do you like better, summer or winter?",
                thinking="2つを比べるなら比較級＋than、3つ以上の中でいちばんなら the＋最上級＋in / of。",
                points=[tp("(2) を of Japan とする誤りに注意させる。Japan は「1つの集まり（場所）」なので in。"),
                        tp("(3) の答え方 I like summer better. も口頭で練習させる。", ask="Which do you like better, summer or winter?", expect="I like summer better.")],
                misconceptions=[("This question is difficulter than that one.", "difficult は長い語なので more difficult。")]),
        example("ex3", "例題3　as ～ as の文",
                "2つの英文がほぼ同じ意味になるように、（　）に適切な語を入れなさい。(1) Aya is 155 cm tall. Mika is 155 cm tall, too. → Aya is (　) (　) (　) Mika.　(2) My bag is smaller than yours. → My bag is not (　) (　) (　) yours.",
                ["(1) 2人は同じ身長なので as＋原級＋as：as tall as。",
                 "(2) 「私のかばんはあなたのより小さい」＝「私のかばんはあなたのほど大きくない」：not as big as。"],
                "(1) as tall as　(2) as big as（not as large as も可）",
                thinking="as と as の間はいつも原級。not as ～ as は「…ほど～ではない」なので、反対の意味の語を使って書きかえる。",
                points=[tp("(2) で not as small as とすると意味が逆になることを、実物のかばんを使って確かめさせる。",
                           ask="My bag is not as small as yours. だと、小さいのはどちら？", expect="あなたのかばん（意味が逆になる）。")]),
        board("bd1", "板書案",
              [("① 形の作り方", ["tall → taller → tallest", "large → larger → largest", "big → bigger → biggest", "easy → easier → easiest",
                                 "beautiful → more ～ → most ～", "good / well → better → best", "many / much → more → most"]),
               ("② 比べる文", ["比較級＋than：taller than Tom", "the＋最上級＋in：in my class", "the＋最上級＋of：of the three / of all",
                               "Which is ～er, A or B?", "Who ～ the ～est? ― Ken does.", "like A better than B / like A the best"]),
               ("③ as ～ as", ["as＋原級＋as：同じくらい～", "as tall as Ken", "not as ～ as：…ほど～ではない", "Tom is not as tall as Ken.",
                               "＝ Tom is shorter than Ken.", "＝ Ken is taller than Tom."])],
              points=[tp("②の in と of は色を分けて書き、後ろにくる語の例を生徒に追加させる。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("導入では教師と生徒、生徒どうしの身長や持ち物を実際に比べさせ、比較級を体で覚えさせる。", timing="導入"),
               tp("more / most をつける語は、教科書に出る語（beautiful, interesting, difficult, popular, important, famous, useful, exciting）をまとめて示し、まず覚えさせる。",
                  caution="すべての長さの判断を音節で説明しようとすると混乱するので、中2では代表的な語を覚えることを優先する。"),
               tp("Who ～ the ～est? の答えは、一般動詞なら Ken does.、be 動詞なら Ken is. と、疑問文の動詞に合わせて答えることを確認する。",
                  ask="Who runs the fastest in your class?", expect="Ken does."),
               tp("表やグラフを使った活動で、比較級・最上級・as ～ as を同じ資料から作らせると、3つの形の使い分けが定着する。"),
               tp("問題プリント D の誤答例は「more＋-er の二重比較」「in / of の取り違え」「not as ～ as の意味の取り違え」の3つを中心にふり返らせる。")],
              misconceptions=[("Ken is more taller than Tom.", "-er と more は同時に使わない。taller than。"),
                              ("Mika is the tallest of her class.", "class は1つの集まりなので in her class。"),
                              ("Ken is as taller as Tom.", "as と as の間は原級。as tall as。"),
                              ("This is the goodest idea.", "good の最上級は best。the best idea。")]),
        summary("sm1", "まとめ",
                ["比較級は -er / more ～、最上級は -est / most ～。つづりのルール（e・重ねる・y→i）と不規則変化（good / well → better → best など）に注意。",
                 "2つを比べる：比較級＋than。3つ以上でいちばん：the＋最上級＋in（場所・集団）/ of（複数・all）。",
                 "同じくらい：as＋原級＋as。not as ～ as は「…ほど～ではない」。like A better than B／like A the best。"]),
        check("ck1", "確認問題",
              [("big の比較級と最上級を書きなさい。", "bigger, biggest"),
               ("This flower is the most beautiful (in / of) the five. の正しいほうを選びなさい。", "of（the five は複数を表す語句）"),
               ("「私の兄は父ほど背が高くない」を英語にしなさい。", "My brother is not as tall as my father.（My brother isn't as tall as our father. なども可）")]),
    ])


# ======================================================================
# 語彙データ
# ======================================================================

# (原級, 比較級, 最上級, ルール)
FORMS = [
    ("tall", "taller", "tallest", "plain"), ("long", "longer", "longest", "plain"), ("old", "older", "oldest", "plain"),
    ("young", "younger", "youngest", "plain"), ("small", "smaller", "smallest", "plain"), ("fast", "faster", "fastest", "plain"),
    ("high", "higher", "highest", "plain"), ("short", "shorter", "shortest", "plain"), ("cold", "colder", "coldest", "plain"),
    ("strong", "stronger", "strongest", "plain"), ("new", "newer", "newest", "plain"),
    ("large", "larger", "largest", "e"), ("nice", "nicer", "nicest", "e"), ("wide", "wider", "widest", "e"), ("cute", "cuter", "cutest", "e"),
    ("big", "bigger", "biggest", "double"), ("hot", "hotter", "hottest", "double"), ("thin", "thinner", "thinnest", "double"),
    ("happy", "happier", "happiest", "y"), ("easy", "easier", "easiest", "y"), ("busy", "busier", "busiest", "y"),
    ("early", "earlier", "earliest", "y"), ("heavy", "heavier", "heaviest", "y"), ("pretty", "prettier", "prettiest", "y"),
    ("beautiful", "more beautiful", "most beautiful", "more"), ("interesting", "more interesting", "most interesting", "more"),
    ("difficult", "more difficult", "most difficult", "more"), ("popular", "more popular", "most popular", "more"),
    ("important", "more important", "most important", "more"), ("famous", "more famous", "most famous", "more"),
    ("useful", "more useful", "most useful", "more"), ("exciting", "more exciting", "most exciting", "more"),
    ("good", "better", "best", "irr"), ("well", "better", "best", "irr"), ("many", "more", "most", "irr"),
    ("much", "more", "most", "irr"), ("bad", "worse", "worst", "irr"),
]
RULE = {"plain": "そのまま -er / -est をつける", "e": "e で終わるので -r / -st だけをつける",
        "double": "〈短母音＋子音字〉で終わるので、最後の子音字を重ねて -er / -est をつける",
        "y": "〈子音字＋y〉で終わるので、y を i にかえて -er / -est をつける", "more": "長い語なので more / most をつける",
        "irr": "不規則に変化する"}
FORM_BY = {k: [f for f in FORMS if f[3] == k] for k in RULE}


# ======================================================================
# A 基本確認
# ======================================================================

@gen("basic_check", 4, ["computation", "common_error"])
def spelling(r):
    k1, k2 = r.sample(list(RULE), 2)
    a, b = r.choice(FORM_BY[k1]), r.choice(FORM_BY[k2])
    ans = f"(1) {a[1]}, {a[2]}　(2) {b[1]}, {b[2]}"
    return sa(f"次の2つの語の比較級と最上級を書きなさい。\n(1) {a[0]}　(2) {b[0]}", ans,
              f"(1) {a[0]} は{RULE[k1]}：{a[1]}, {a[2]}。(2) {b[0]} は{RULE[k2]}：{b[1]}, {b[2]}。", d=1,
              v=[f"{a[1]}, {a[2]}, {b[1]}, {b[2]}", f"(1){a[1]},{a[2]} (2){b[1]},{b[2]}"],
              ap="語尾のつづり（e・〈短母音＋子音字〉・〈子音字＋y〉）、語の長さ、不規則変化かどうかを順に確かめる。",
              steps=[f"{a[0]}：{RULE[k1]}。", f"{b[0]}：{RULE[k2]}。", f"答え：{ans}"],
              alt=["書いた比較級を than の文（This is ～ than that.）に入れて読んでみて、不自然な形になっていないかを確かめる。"],
              pc=[("(1) の比較級・最上級が正しい", 1), ("(2) の比較級・最上級が正しい", 1)],
              pit=["子音字を重ねる語を重ねずに書く（biger）。", "長い語や不規則変化の語に -er をつける（beautifuller, gooder）。"])


# (主語, 補語前, 原級, 比較級, 比較の相手, 日本語, ルール)
THAN = [
    ("This bridge", "is", "long", "longer", "that one", "この橋はあの橋より長い。", "plain"),
    ("My bag", "is", "heavy", "heavier", "yours", "私のかばんはあなたのより重い。", "y"),
    ("Today", "is", "hot", "hotter", "yesterday", "今日は昨日より暑い。", "double"),
    ("This book", "is", "interesting", "more interesting", "that one", "この本はあの本よりおもしろい。", "more"),
    ("Soccer", "is", "popular", "more popular", "baseball in this class", "このクラスではサッカーのほうが野球より人気がある。", "more"),
    ("Your idea", "is", "good", "better", "mine", "あなたの考えは私のよりよい。", "irr"),
    ("This box", "is", "large", "larger", "that one", "この箱はあの箱より大きい。", "e"),
    ("My brother", "gets up", "early", "earlier", "me", "兄は私より早く起きる。", "y"),
    ("Ken", "runs", "fast", "faster", "Taro", "ケンはタロウより速く走る。", "plain"),
    ("This question", "is", "difficult", "more difficult", "that one", "この問題はあの問題より難しい。", "more"),
    ("Mika", "sings", "well", "better", "her sister", "ミカは姉より上手に歌う。", "irr"),
    ("This river", "is", "wide", "wider", "that river", "この川はあの川より幅が広い。", "e"),
    ("My dog", "is", "big", "bigger", "your dog", "私の犬はあなたの犬より大きい。", "double"),
    ("The weather today", "is", "bad", "worse", "yesterday", "今日の天気は昨日より悪い。", "irr"),
]


@gen("basic_check", 4, ["computation", "condition_check"])
def than_choice(r):
    s, v, base, comp, other, jp, rule = r.choice(THAN)
    sup = {"plain": base + "est", "y": base[:-1] + "iest", "double": base + base[-1] + "est", "e": base + "st",
           "more": "most " + base}.get(rule, {"good": "best", "well": "best", "bad": "worst"}.get(base))
    if rule == "more":
        wrongs = [base + "er", f"more {base}er", sup]
    elif rule == "irr":
        wrongs = [base + "er", f"more {comp}", sup]
    else:
        wrongs = [base, f"more {comp}", sup]
    reasons = {}
    for w in wrongs:
        if w == base:
            reasons[w] = ("than の前は比較級にする。原級のままでは比べる文にならない。", "比較級と than")
        elif w.startswith("more ") and w != f"more {base}":
            reasons[w] = ("more と -er（または不規則変化の比較級）を同時に使うことはできない。", "二重の比較級")
        elif w == sup:
            reasons[w] = ("than を使って2つを比べる文では最上級は使わない。最上級は「3つ以上の中でいちばん」のときに the をつけて使う。", "比較級と最上級の区別")
        else:
            reasons[w] = (f"{base} は{RULE[rule]}語で、{w} という形はない。", "比較級の作り方")
    return mc(f"日本語に合うように、（　）に入る最も適切なものを選びなさい。\n{jp}\n{s} {v} (　　) than {other}.", [comp] + wrongs,
              f"than があるので比較級。{base} は{RULE[rule]}ので {comp}。", d=1,
              ap="後ろに than があれば比較級。次に、もとの語のつづりや長さから比較級の作り方を決める。",
              steps=["空所の後ろに than があるので比較級を選ぶ。", f"{base} は{RULE[rule]}。", f"答え：{comp}"],
              alt=[f"選んだ文を「{s} は {other} より～」と訳して、日本語と一致するかを確かめる。"],
              pc=[("比較級を使う文だと判断している", 1), ("比較級の形を正しく選んでいる", 1)],
              pit=["more と -er を両方つける（more longer）。", "than の文に最上級を使う。"], why=reasons)


# (日本語, 空所の前, 空所の後, 正答)
IN_OF = [
    ("ケンはクラスでいちばん背が高い。", "Ken is the tallest", "his class", "in"),
    ("これは3つの中でいちばん古い寺だ。", "This is the oldest temple", "the three", "of"),
    ("信濃川は日本でいちばん長い川だ。", "The Shinano River is the longest river", "Japan", "in"),
    ("私は四季の中で春がいちばん好きだ。", "I like spring the best", "the four seasons", "of"),
    ("ユミは家族の中でいちばん早く起きる。", "Yumi gets up the earliest", "her family", "in"),
    ("この花はすべての中でいちばん美しい。", "This flower is the most beautiful", "all", "of"),
    ("アヤは5人の中でいちばん速く泳ぐ。", "Aya swims the fastest", "the five", "of"),
    ("これは私たちの町でいちばん人気のある店だ。", "This is the most popular shop", "our town", "in"),
    ("これは私たちの市でいちばん大きな公園だ。", "This is the biggest park", "our city", "in"),
    ("この問題はすべての問題の中でいちばん難しい。", "This question is the most difficult", "all the questions", "of"),
    ("彼はその3人の少年の中でいちばん若い。", "He is the youngest", "the three boys", "of"),
    ("ここは世界でいちばん暑い場所の1つだ。", "This is one of the hottest places", "the world", "in"),
]


@gen("basic_check", 4, ["condition_check", "concept"])
def in_or_of(r):
    jp, pre, post, ok = r.choice(IN_OF)
    other = "of" if ok == "in" else "in"
    kind = "場所や集団（1つの集まり）を表す語句" if ok == "in" else "複数のものを表す語句（数・all）"
    why = {other: (f"{post} は{kind}なので {ok} を使う。{other} は{'複数のものを表す語句（the three, all など）' if other == 'of' else '場所や集団を表す語句（my class, Japan など）'}の前に使う。", "最上級の in と of の使い分け"),
           "than": ("than は比較級の後ろで使う。最上級の文で範囲を表すときは in / of を使う。", "比較級と最上級の区別"),
           "as": ("as は as ～ as の形で使う。最上級の範囲を表すことはできない。", "as ～ as と最上級の混同")}
    return mc(f"日本語に合うように、（　）に入る最も適切な語を選びなさい。\n{jp}\n{pre} (　　) {post}.", [ok] + list(why),
              f"最上級の範囲は、{post} のような{kind}なので {ok}。", d=1,
              ap="最上級の後ろの「～の中で」が、1つの集まり（場所・集団）なら in、複数のもの（数・all）なら of。",
              steps=[f"空所の後ろは {post}。", f"これは{kind}。", f"答え：{ok}"],
              alt=[f"{post} を「～という場所・集団の中で」と言えるか、「～個（人）の中で」と言えるかで確かめる。"],
              pc=[("最上級の範囲を表す語だと判断している", 1), ("in / of を正しく選んでいる", 1)],
              pit=["the three を「3人というグループ」と考えて in にする。", "my class を「たくさんの人」と考えて of にする。"], why=why)


# (日本語, 主語, 動詞, 原級, 相手, 比較級, 最上級, 否定か)
AS_AS = [
    ("私の犬はあなたの犬と同じくらい大きい。", "My dog", "is", "big", "yours", "bigger", "biggest", False),
    ("ケンは父親と同じくらい背が高い。", "Ken", "is", "tall", "his father", "taller", "tallest", False),
    ("この本はあの本ほどおもしろくない。", "This book", "is not", "interesting", "that one", "more interesting", "most interesting", True),
    ("私は兄ほど速く走れない。", "I", "can't run", "fast", "my brother", "faster", "fastest", True),
    ("今日は昨日と同じくらい寒い。", "Today", "is", "cold", "yesterday", "colder", "coldest", False),
    ("ユミは姉と同じくらい上手にピアノをひく。", "Yumi", "plays the piano", "well", "her sister", "better", "best", False),
    ("この問題はあの問題ほど難しくない。", "This question", "is not", "difficult", "that one", "more difficult", "most difficult", True),
    ("私のかばんはあなたのかばんほど重くない。", "My bag", "is not", "heavy", "yours", "heavier", "heaviest", True),
    ("この町は私の町と同じくらい有名だ。", "This town", "is", "famous", "my town", "more famous", "most famous", False),
    ("トムはケンと同じくらい早く学校に来る。", "Tom", "comes to school", "early", "Ken", "earlier", "earliest", False),
]


@gen("basic_check", 4, ["concept", "condition_check"])
def as_as(r):
    jp, s, v, base, other, comp, sup, neg = r.choice(AS_AS)
    third = ("more " + comp) if not comp.startswith("more") else (base + "er")
    keys = [comp, sup, third]
    why = {comp: ("as と as の間は原級。比較級は than といっしょに使う。", "as ～ as の形"),
           sup: ("as と as の間は原級。最上級は the をつけて「いちばん」を表すときに使う。", "as ～ as の形"),
           third: ("このような形はない。また、as と as の間は原級をそのまま置く。", "比較級の作り方と as ～ as の形")}
    meaning = "「…ほど～ではない」" if neg else "「…と同じくらい～」"
    return mc(f"日本語に合うように、（　）に入る最も適切なものを選びなさい。\n{jp}\n{s} {v} as (　　) as {other}.", [base] + keys,
              f"{meaning}は {'not ' if neg else ''}as＋原級＋as で表す。as と as の間は原級 {base}。", d=1,
              ap="as ～ as の間は、比較級や最上級ではなく、もとの形（原級）を置く。",
              steps=["空所が as と as の間にあることを確認する。", "as と as の間は原級。", f"答え：{base}"],
              alt=[f"日本語の意味を確かめる：{'not があるので「…ほど～ではない」' if neg else '「同じくらい」'}になっているか。"],
              pc=[("as ～ as の形だと判断している", 1), ("原級を選んでいる", 1)],
              pit=["as の後ろに比較級を入れる（as taller as）。", "not as ～ as を「同じくらいではない＝反対」と誤解する。"], why=why)


# (日本語, 空所つき英文, 正答, [(誤答, 理由)])
IRR = [
    ("この映画はあの映画よりよい。", "This movie is (　　) than that one.", "better",
     [("gooder", "good の比較級は不規則に変化して better。"), ("more good", "good は more をつけず better にする。"), ("best", "than があるので比較級。best は最上級。")]),
    ("ミカはクラスでいちばん上手に英語を話す。", "Mika speaks English the (　　) in her class.", "best",
     [("better", "the と in her class があるので最上級。better は比較級。"), ("most well", "well の最上級は不規則に変化して best。"), ("wellest", "well の最上級は best。wellest という形はない。")]),
    ("私は姉より多くの本を持っている。", "I have (　　) books than my sister.", "more",
     [("many", "than があるので比較級。many の比較級は more。"), ("manier", "many の比較級は more。manier という形はない。"), ("most", "than があるので比較級。most は最上級。")]),
    ("今日の天気は昨日よりも悪い。", "The weather today is (　　) than yesterday.", "worse",
     [("badder", "bad の比較級は不規則に変化して worse。"), ("more bad", "bad は more をつけず worse にする。"), ("worst", "than があるので比較級。worst は最上級。")]),
    ("彼は私たちのチームでいちばんよい選手だ。", "He is the (　　) player on our team.", "best",
     [("goodest", "good の最上級は不規則に変化して best。"), ("better", "the があり「いちばん」なので最上級。better は比較級。"), ("most good", "good は most をつけず best にする。")]),
    ("私は冬より夏のほうが好きだ。", "I like summer (　　) than winter.", "better",
     [("gooder", "「～より…のほうが好き」は like ～ better than … で表す。gooder という形はない。"), ("best", "than があるので比較級。best は最上級。"), ("well", "than の前は比較級。well は原級。")]),
    ("ケンはトムより上手にギターをひく。", "Ken plays the guitar (　　) than Tom.", "better",
     [("weller", "well の比較級は不規則に変化して better。"), ("more well", "well は more をつけず better にする。"), ("good", "than の前は比較級。good は形容詞の原級。")]),
    ("彼はこの町でいちばんたくさんのお金を持っている。", "He has the (　　) money in this town.", "most",
     [("more", "the と in this town があるので最上級。more は比較級。"), ("much", "the があり「いちばん」なので最上級。much は原級。"), ("muchest", "much の最上級は most。muchest という形はない。")]),
    ("私は果物の中でリンゴがいちばん好きだ。", "I like apples the (　　) of all fruits.", "best",
     [("goodest", "good / well の最上級は不規則に変化して best。goodest という形はない。"), ("better", "the と of all fruits があるので最上級。better は比較級。"), ("good", "the があり「いちばん」なので最上級。good は原級。")]),
]


@gen("basic_check", 4, ["computation", "common_error"])
def irregular(r):
    jp, s, ok, wrongs = r.choice(IRR)
    return mc(f"日本語に合うように、（　）に入る最も適切なものを選びなさい。\n{jp}\n{s}", [ok] + [w for w, _ in wrongs],
              f"good / well → better → best、many / much → more → most、bad → worse → worst は不規則に変化する。答え：{ok}", d=2,
              ap="まず than があるか（比較級）、the と in / of があるか（最上級）を見て、次にもとの語が不規則変化の語かを確かめる。",
              steps=["比較級・最上級のどちらを使う文かを決める。", "もとの語（good / well / many / much / bad）を確かめる。", f"不規則変化の形を選ぶ：{ok}。"],
              alt=["選んだ語を原級にもどした文（This movie is good. など）を考えて、もとの語が何かを確かめる。"],
              pc=[("比較級か最上級かを判断している", 1), ("不規則変化の形を選んでいる", 1)],
              pit=["good に -er をつけて gooder にする。", "「～のほうが好き」に more を使う。"],
              why={w: (reason, "不規則変化と比較級・最上級の区別") for w, reason in wrongs})


# ======================================================================
# B 標準演習
# ======================================================================

NAMES = ["Ken", "Yumi", "Taro", "Mika", "Aya", "Sho", "Emi", "Riku"]


def make_people(r):
    names = r.sample(NAMES, 4)
    heights = r.sample(range(145, 172), 4)
    ages = [r.randint(12, 15) for _ in range(4)]
    i, j = r.sample(range(4), 2)
    ages[j] = ages[i]
    return names, heights, ages


def statements(names, heights, ages):
    """（文, 真偽, 根拠）のリスト。"""
    out = []
    n = len(names)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            a, b = names[i], names[j]
            ha, hb = heights[i], heights[j]
            out.append((f"{a} is taller than {b}.", ha > hb, f"{a} は {ha} cm、{b} は {hb} cm"))
            out.append((f"{a} is not as tall as {b}.", ha < hb, f"{a} は {ha} cm、{b} は {hb} cm"))
            if i < j:
                out.append((f"{a} is as old as {b}.", ages[i] == ages[j], f"{a} は {ages[i]} 歳、{b} は {ages[j]} 歳"))
            if ages[i] != ages[j]:
                out.append((f"{a} is younger than {b}.", ages[i] < ages[j], f"{a} は {ages[i]} 歳、{b} は {ages[j]} 歳"))
    tall = max(range(n), key=lambda k: heights[k])
    short = min(range(n), key=lambda k: heights[k])
    for k in range(n):
        out.append((f"{names[k]} is the tallest of the four.", k == tall, f"いちばん高いのは {names[tall]}（{heights[tall]} cm）"))
        out.append((f"{names[k]} is the shortest of the four.", k == short, f"いちばん低いのは {names[short]}（{heights[short]} cm）"))
    return out


@gen("standard_practice", 4, ["cross_unit", "application"], rel=["JH-ENG-G3-U06"])
def table_read(r):
    names, heights, ages = make_people(r)
    st = statements(names, heights, ages)
    trues = [s for s in st if s[1]]
    falses = [s for s in st if not s[1]]
    ok = r.choice(trues)
    wr = r.sample(falses, 3)
    tbl = table([(nm, f"{h} cm", f"{a} 歳") for nm, h, a in zip(names, heights, ages)], header=["名前", "身長", "年齢"], caption="4人の生徒の身長と年齢（架空の資料）")
    why = {w[0]: (f"表より、{w[2]}なので、この文の内容は正しくない。", "比較の文と資料の対応") for w in wr}
    return mc("次の表は4人の生徒の身長と年齢をまとめたものである。表の内容に合う英文を1つ選びなさい。", [ok[0]] + [w[0] for w in wr],
              f"表より、{ok[2]}なので「{ok[0]}」が正しい。", d=3, tbl=tbl,
              ap="英文の主語・比べる相手・比べる内容（身長か年齢か）を確かめ、表の数値と1つずつ照らし合わせる。",
              steps=["各選択肢の主語と比べる相手を確認する。", "taller / not as tall as / as old as / younger / the tallest などの意味を確かめる。", "表の数値と照らし合わせ、正しいものを選ぶ。"],
              alt=["正しいと選んだ文を、主語を入れかえた別の言い方（A is taller than B. → B is shorter than A.）にして、表と合うかもう一度確かめる。"],
              pc=[("比較表現の意味を正しく理解している", 2), ("表の数値と照合して正しい文を選んでいる", 2)],
              pit=["not as tall as を「同じくらい高い」と読みちがえる。", "身長と年齢の列を取り違える。"], why=why)


# (元の文, 空所つき文, 答え, 別解, ポイント)
REWRITE = [
    ("Ken is taller than Tom.", "Tom is (　　) than Ken.", "shorter", [], "主語を入れかえるときは反対の意味の語（tall ⇔ short）の比較級を使う。"),
    ("My bag is smaller than yours.", "Your bag is (　　) than mine.", "bigger", ["larger"], "主語を入れかえて、small の反対 big（large）の比較級を使う。"),
    ("Tom is younger than Ken.", "Ken is (　　) than Tom.", "older", [], "主語を入れかえて、young の反対 old の比較級を使う。"),
    ("This question is easier than that one.", "That question is (　　) difficult than this one.", "more", [], "easy の反対 difficult は長い語なので more difficult。"),
    ("Ken is taller than Tom.", "Tom is not as (　　) as Ken.", "tall", [], "「トムはケンほど背が高くない」。not as＋原級＋as。"),
    ("My room is larger than yours.", "Your room is not as (　　) as mine.", "large", ["big"], "「あなたの部屋は私の部屋ほど大きくない」。as と as の間は原級。"),
    ("Mika runs faster than Aya.", "Aya doesn't run as (　　) as Mika.", "fast", [], "「アヤはミカほど速く走らない」。as と as の間は原級。"),
    ("Aya is 150 cm tall. Emi is 150 cm tall, too.", "Aya is as (　　) as Emi.", "tall", [], "同じ身長なので as tall as。"),
    ("This movie is more interesting than that one.", "That movie is not as (　　) as this one.", "interesting", [], "「あの映画はこの映画ほどおもしろくない」。as と as の間は原級。"),
    ("Tokyo Skytree is taller than Tokyo Tower.", "Tokyo Tower is (　　) than Tokyo Skytree.", "shorter", ["lower"], "主語を入れかえて、反対の意味の語の比較級を使う。"),
]


@gen("standard_practice", 4, ["computation", "condition_check"])
def rewrite(r):
    a, b, ans, vs, point = r.choice(REWRITE)
    return sa(f"2つの英文がほぼ同じ意味になるように、（　）に適切な1語を入れなさい。\n{a}\n{b}", ans,
              f"{point}答え：{ans}", d=2, p=4, v=vs or None,
              ap="2文で主語が入れかわっているか、as ～ as になっているかを見て、反対の意味の語や原級を使う必要があるかを判断する。",
              steps=["1文目の事実（どちらが～か）を日本語で確かめる。", "2文目の形（比較級＋than か、not as ～ as か）を確かめる。", f"同じ事実になる語を入れる：{ans}。"],
              alt=["完成した2文目を日本語に訳し、1文目と同じ事実を表しているかを確かめる。"],
              pc=[("2文の関係（主語の入れかえ・as ～ as）を判断している", 2), ("正しい語を正しい形で書いている", 2)],
              pit=["主語を入れかえたのに同じ語の比較級を使い、意味が逆になる。", "not as ～ as の間に比較級を入れる。"])


ORDERS = [
    ("この橋は町でいちばん古い。", ["this bridge", "is", "the", "oldest", "in", "the town"], "the＋最上級＋in＋場所"),
    ("私は野球よりサッカーのほうが好きだ。", ["I", "like", "soccer", "better", "than", "baseball"], "like A better than B"),
    ("あなたのクラスでいちばん速く走るのはだれですか。", ["who", "runs", "the", "fastest", "in", "your class"], "Who＋動詞＋the＋最上級 ～?"),
    ("この本はあの本よりおもしろい。", ["this book", "is", "more", "interesting", "than", "that one"], "more＋長い語＋than"),
    ("ユミはお母さんと同じくらい背が高い。", ["Yumi", "is", "as", "tall", "as", "her mother"], "as＋原級＋as"),
    ("私の兄は父ほど速く泳げない。", ["my brother", "can't", "swim", "as", "fast", "as", "my father"], "not as＋原級＋as"),
    ("リンゴとバナナでは、どちらが好きですか。", ["which", "do", "you", "like", "better,", "apples", "or", "bananas"], "Which do you like better, A or B?"),
    ("これは3つの中でいちばん役に立つ辞書です。", ["this", "is", "the", "most", "useful", "dictionary", "of", "the three"], "the most＋長い語＋名詞＋of＋数"),
    ("富士山は日本でいちばん高い山です。", ["Mt. Fuji", "is", "the", "highest", "mountain", "in", "Japan"], "the＋最上級＋名詞＋in＋場所"),
    ("彼は世界でいちばん有名な歌手の1人です。", ["he", "is", "one", "of", "the", "most", "famous", "singers", "in", "the world"], "one of the＋最上級＋複数名詞"),
    ("今日は昨日より寒い。", ["it", "is", "colder", "today", "than", "yesterday"], "比較級＋than"),
    ("この2つのかばんでは、どちらが重いですか。", ["which", "is", "heavier,", "this bag", "or", "that one"], "Which is＋比較級, A or B?"),
]


@gen("standard_practice", 4, ["application", "computation"])
def build_order(r):
    jp, parts, pat = r.choice(ORDERS)
    sent = cap(" ".join(parts)).replace(" ,", ",") + ("?" if jp.endswith("か。") else ".")
    return order(f"日本語に合うように、次の語句を並べかえて英文を完成させなさい。ただし、文頭にくる語も小文字で示してある。\n{jp}", parts,
                 f"{sent}　ポイント：{pat}。", d=2, p=4,
                 ap="比べ方（2つを比べる・いちばん・同じくらい）を日本語から判断し、than / the＋最上級＋in・of / as ～ as のどの型かを先に決める。",
                 steps=[f"文の型を決める：{pat}。", "主語と動詞を決める。", "比較の部分と、比べる相手・範囲の順に並べる。", f"完成文：{sent}"],
                 alt=["完成した英文を日本語に訳し直して、問題の日本語と一致するかを確かめる。"],
                 pc=[("文の骨組み（主語・動詞・疑問詞）の語順が正しい", 2), ("比較の部分と相手・範囲の語順が正しい", 2)],
                 pit=["the を落として最上級を作る。", "Which の疑問文でカンマの後ろの A or B を先に置く。"])


# (問い, 正答, [(誤答, 理由)])
QA = [
    ("Which do you like better, dogs or cats?", "I like cats better.",
     [("I like cats the best.", "2つのうちどちらかを答えるので比較級 better を使う。the best は3つ以上の中でいちばんのとき。"),
      ("Yes, I like cats.", "Which でたずねられているので、Yes / No では答えない。"),
      ("Cats are better than.", "than の後ろに比べる相手がなく、文が成り立たない。")]),
    ("Who is the tallest in your family?", "My father is.",
     [("My father does.", "Who is ～? と be 動詞でたずねているので is で答える。"),
      ("My father is taller.", "最上級でたずねられているので、比較級で答えるのは合わない。"),
      ("Yes, my father is.", "Who でたずねられているので、Yes / No では答えない。")]),
    ("Who runs the fastest in your class?", "Ken does.",
     [("Ken is.", "Who runs ～? と一般動詞でたずねているので does で答える。"),
      ("Ken runs.", "一般動詞の疑問文には does を使って答え、runs だけで終えない。"),
      ("Yes, Ken does.", "Who でたずねられているので、Yes / No では答えない。")]),
    ("Which is longer, the Tone River or the Shinano River?", "The Shinano River is.",
     [("The Shinano River does.", "Which is ～? と be 動詞でたずねているので is で答える。"),
      ("The Shinano River is the longest.", "2つを比べる質問なので、最上級で答えるのは合わない。"),
      ("Yes, it is.", "Which でたずねられているので、Yes / No では答えない。")]),
    ("Which season do you like the best?", "I like spring the best.",
     [("I like spring better.", "the best でたずねられているので、the best で答える。"),
      ("Spring is.", "Which season do you like ～? と一般動詞でたずねているので、I like ～. で答える。"),
      ("Yes, I do.", "Which でたずねられているので、Yes / No では答えない。")]),
    ("Who can swim faster, Aya or Mika?", "Aya can.",
     [("Aya does.", "Who can ～? と can でたずねているので can で答える。"),
      ("Aya is.", "Who can ～? と can でたずねているので can で答える。"),
      ("Aya can the fastest.", "2人を比べる質問なので最上級は使わない。また、答えは Aya can. で文が終わる。")]),
    ("Which is the most popular sport in your class?", "Soccer is.",
     [("Soccer does.", "Which is ～? と be 動詞でたずねているので is で答える。"),
      ("Soccer is more popular.", "最上級でたずねられているので、比較級で答えるのは合わない。"),
      ("Yes, soccer is.", "Which でたずねられているので、Yes / No では答えない。")]),
    ("Who gets up earlier, you or your sister?", "My sister does.",
     [("My sister is.", "Who gets up ～? と一般動詞でたずねているので does で答える。"),
      ("My sister gets up the earliest.", "2人を比べる質問なので最上級は使わない。"),
      ("Yes, she does.", "Who でたずねられているので、Yes / No では答えない。")]),
]


@gen("standard_practice", 4, ["concept", "application"])
def answer_q(r):
    q, ok, wrongs = r.choice(QA)
    return mc(f"次の質問への答えとして最も適切なものを選びなさい。\n{q}", [ok] + [w for w, _ in wrongs],
              f"疑問詞（Which / Who）でたずねられたら Yes / No ではなく具体的に答え、質問の動詞（be 動詞・一般動詞・can）と比べ方（比較級・最上級）に合わせる。答え：{ok}", d=2,
              ap="①疑問詞の疑問文なので Yes / No は使わない、②質問の動詞（is / does / can）、③比較級か最上級か、の3点を確かめる。",
              steps=["疑問詞と、質問の動詞の種類を確認する。", "比較級（2つ）か最上級（3つ以上）かを確認する。", f"答え：{ok}"],
              alt=["答えの省略された部分を補ってみる（My father is the tallest in my family. など）と、組み合わせが正しいかを確かめられる。"],
              pc=[("質問の形（疑問詞・動詞）に合わせている", 2), ("比較級・最上級を質問に合わせている", 2)],
              pit=["一般動詞の質問に is で答える。", "Which の疑問文に Yes / No で答える。"],
              why={w: (reason, "比較の疑問文への答え方") for w, reason in wrongs})


JP_EN = [
    ("私の兄は私より3歳年上です。", "My brother is three years older than me.", ["My brother is three years older than I am.", "My brother is three years older than I."]),
    ("この問題はすべての中でいちばんやさしい。", "This question is the easiest of all.", []),
    ("私は数学より英語のほうが好きです。", "I like English better than math.", []),
    ("今日は昨日と同じくらい暑い。", "It is as hot today as yesterday.", ["Today is as hot as yesterday.", "It's as hot today as it was yesterday."]),
    ("この時計はあの時計ほど高価ではない。", "This watch is not as expensive as that one.", ["This watch isn't as expensive as that one."]),
    ("北海道は日本でいちばん大きい都道府県です。", "Hokkaido is the largest prefecture in Japan.", ["Hokkaido is the biggest prefecture in Japan."]),
    ("あなたの考えは私の考えよりよい。", "Your idea is better than mine.", []),
    ("ケンは家族の中でいちばん早く起きる。", "Ken gets up the earliest in his family.", ["Ken gets up earliest in his family."]),
    ("この映画はあの映画より人気がある。", "This movie is more popular than that one.", []),
    ("私のネコはあなたのネコと同じくらいかわいい。", "My cat is as cute as yours.", ["My cat is as cute as your cat."]),
    ("これは私の町でいちばん高い建物です。", "This is the tallest building in my town.", ["This is the highest building in my town."]),
]


@gen("standard_practice", 4, ["computation", "application"])
def jp_to_en(r):
    jp, ans, vs = r.choice(JP_EN)
    return sa(f"次の日本語を英語に直しなさい。\n{jp}", ans,
              f"比べ方（2つ・いちばん・同じくらい）に合わせて、比較級＋than／the＋最上級＋in・of／as＋原級＋as を使う。答え：{ans}", d=2, p=4, v=vs or None,
              ap="日本語の「～より」「いちばん」「同じくらい」「～ほど…ない」に注目して、文の型を決める。",
              steps=["日本語から比べ方を判断する。", "形容詞・副詞を比較級・最上級・原級のどれにするかを決め、つづりのルールで形を作る。", "比べる相手（than）や範囲（in / of）を加える。", f"答え：{ans}"],
              alt=["書いた英文を、主語を入れかえたり反対の意味の語を使ったりした別の言い方に書きかえ、同じ事実を表しているかを確かめる。"],
              pc=[("文の型（than / the＋最上級 / as ～ as）が正しい", 2), ("比較級・最上級の形と in / of などが正しい", 2)],
              pit=["the を落として最上級を作る。", "長い語に -er をつける。"])


# ======================================================================
# C 思考力・記述応用
# ======================================================================

@gen("thinking_writing", 3, ["written_reasoning", "application"])
def table_write(r):
    names, heights, ages = make_people(r)
    tall = max(range(4), key=lambda k: heights[k])
    i, j = next((k, m) for k in range(4) for m in range(k + 1, 4) if ages[k] == ages[m])
    a, b = r.sample(range(4), 2)
    if heights[a] < heights[b]:
        a, b = b, a
    model = (f"{names[a]} is taller than {names[b]}. {names[tall]} is the tallest of the four. {names[i]} is as old as {names[j]}.")
    tbl = table([(nm, f"{h} cm", f"{g} 歳") for nm, h, g in zip(names, heights, ages)], header=["名前", "身長", "年齢"], caption="4人の生徒の身長と年齢（架空の資料）")
    who = "・".join(names)
    return desc(f"次の表は {who} の4人の生徒の身長と年齢をまとめたものである。表の内容に合う英文を3つ書きなさい。ただし、1文目は比較級、2文目は最上級、3文目は as ～ as を使うこと。また、2文目で in と of のどちらを使ったか、その理由を日本語で書きなさい。",
                f"（解答例）{model}　理由：the four は「4人」という複数を表す語句なので of を使った。",
                "比較級は2人を比べる（than）、最上級は4人の中でいちばん（the＋最上級＋of the four）、as ～ as は同じ値の2人について使う。",
                [("比較級の文が正しく、表の内容に合っている", 2), ("最上級の文が正しく、表の内容に合っている", 2), ("as ～ as の文が正しく、表の内容に合っている", 2), ("in / of の理由を説明している", 2)], d=4, p=8, lines=6, tbl=tbl,
                ap="表から「2人の差」「いちばん」「同じ」を1つずつ見つけ、それぞれに合う比較の形を当てはめる。",
                steps=["表から、身長の差がある2人を選んで比較級の文を書く。", "いちばん背が高い（低い）人を見つけて最上級の文を書く。", "年齢が同じ2人を見つけて as old as の文を書く。", "最上級の範囲 the four に of を使う理由を書く。"],
                alt=["書いた3文を、主語を入れかえたり反対の意味の語（short / young）を使ったりして言いかえ、表と矛盾しないかを確かめる。"],
                pc=[("比較級の文", 2), ("最上級の文", 2), ("as ～ as の文", 2), ("in / of の理由", 2)],
                pit=["年齢が同じなのに older than を使う。", "the tallest in the four と書く。"])


PAIRS = [
    ("Ken is as tall as Tom.", "Ken is not as tall as Tom.",
     "A は as＋原級＋as で「ケンはトムと同じくらいの背の高さだ」という意味。B は not as ～ as で「ケンはトムほど背が高くない」、つまりトムのほうが背が高いという意味になる。"),
    ("I like dogs better than cats.", "I like dogs the best of all animals.",
     "A は like ～ better than … で「ネコより犬のほうが好きだ」と2つを比べている。B は like ～ the best of … で「すべての動物の中で犬がいちばん好きだ」と、3つ以上の中でいちばんであることを表す。"),
    ("Mika is the tallest in her class.", "Mika is taller than her classmate Aya.",
     "A は最上級で「ミカはクラスでいちばん背が高い」と、クラス全員の中でいちばんであることを表す。B は比較級で「ミカはクラスメートのアヤより背が高い」と、2人だけを比べている。B だけではミカがクラスでいちばんかどうかはわからない。"),
    ("This bag is bigger than that one.", "That bag is not as big as this one.",
     "A は「このかばんはあのかばんより大きい」、B は「あのかばんはこのかばんほど大きくない」。主語と形は違うが、どちらも「このかばんのほうが大きい」という同じ事実を表している。"),
    ("Ken is one of the best players on the team.", "Ken is the best player on the team.",
     "A は one of the＋最上級＋複数名詞で「ケンはチームでもっともよい選手の1人だ」と、上位の何人かのうちの1人であることを表す。B は「ケンはチームでいちばんよい選手だ」と、ただ1人のいちばんであることを表す。"),
    ("Taro runs faster than Riku.", "Taro runs as fast as Riku.",
     "A は比較級で「タロウはリクより速く走る」と、タロウのほうが速いことを表す。B は as＋原級＋as で「タロウはリクと同じくらい速く走る」と、2人の速さが同じくらいであることを表す。"),
]


@gen("thinking_writing", 3, ["written_reasoning", "concept"])
def explain_difference(r):
    a, b, model = r.choice(PAIRS)
    return desc(f"次の2つの英文 A・B の意味の違い（または同じ点）を、比較の形に注目して日本語で説明しなさい。\nA：{a}\nB：{b}", model,
                "比較級（2つを比べる）・最上級（3つ以上でいちばん）・as ～ as（同じくらい）・not as ～ as（…ほど～ない）のどれが使われているかで、表す事実が決まる。",
                [("A の形と意味を正しく説明している", 3), ("B の形と意味を正しく説明している", 3), ("2文の違い（または同じ点）を明確に述べている", 2)], d=3, p=8, lines=5,
                ap="2つの文で違う部分（比較級・最上級・as ～ as・not・one of）に印をつけ、それぞれがどんな事実を表すかを図や数直線にしてみる。",
                steps=["A と B で違う部分を見つける。", "それぞれの比較の形の意味を確かめる。", "和訳を示し、表している事実が同じか違うかを説明する。"],
                alt=["具体的な数値（身長など）を自分で仮に決めて、A・B が正しくなる場合を考えると、違いがはっきりする。"],
                pc=[("A の説明", 3), ("B の説明", 3), ("違い・同じ点の指摘", 2)],
                pit=["not as ～ as を「同じくらいではない＝どちらかわからない」と説明する。", "比較級の文から「いちばん」まで言えると考える。"])


PEOPLE5 = ["Ken", "Yumi", "Taro", "Mika", "Aya", "Sho", "Emi"]
REL = [("older", "younger", "oldest", "youngest", "年上である", "年上な", "年下な", "年上の"),
       ("taller", "shorter", "tallest", "shortest", "背が高い", "背が高い", "背が低い", "背が高い")]


@gen("thinking_writing", 2, ["condition_check", "written_reasoning"])
def deduce(r):
    a, b, c = r.sample(PEOPLE5, 3)
    comp, opp, sup, sup_opp, jp1, top_jp, bot_jp, ord_jp = r.choice(REL)
    form = r.choice(["chain", "notas"])
    if form == "chain":
        s1 = f"{a} is {comp} than {b}."
        s2 = f"{c} is {opp} than {b}."
    else:
        s1 = f"{b} is not as {'old' if comp == 'older' else 'tall'} as {a}."
        s2 = f"{b} is {comp} than {c}."
    # どちらの場合も a > b > c
    ask_top = r.random() < 0.5
    ans_name = a if ask_top else c
    q_word = sup if ask_top else sup_opp
    order_jp = f"{a} ＞ {b} ＞ {c}"
    model = (f"{ans_name}。理由：1文目から {a} のほうが {b} より{jp1}こと、2文目から {b} のほうが {c} より{jp1}ことがわかる。"
             f"したがって{ord_jp}順に {order_jp} となり、いちばん{top_jp if ask_top else bot_jp}のは {ans_name} である。")
    return desc(f"次の2つの英文から、3人のうち the {q_word} なのはだれかを答え、そう判断した理由を、それぞれの英文の意味にふれて日本語で説明しなさい。\n{s1}\n{s2}",
                model,
                "比較級・not as ～ as の文を「どちらが上か」に直して並べると、3人の順番がわかる。反対の意味の語（younger / shorter）や not as ～ as は向きを逆にして読む。",
                [("正しい人物を答えている", 2), ("1文目の意味（どちらが上か）を正しく説明している", 2), ("2文目の意味を正しく説明している", 2), ("3人の順番を示して結論を導いている", 2)], d=4, p=8, lines=5,
                ap="それぞれの英文を「（だれ）＞（だれ）」の不等号の形に直してから、3人を1列に並べる。",
                steps=["1文目を「どちらが上か」に直す。", "2文目を「どちらが上か」に直す（反対の語・not as ～ as は向きに注意）。", f"3人を並べる：{order_jp}。", f"答え：{ans_name}"],
                alt=["3人に仮の数値（年齢や身長）を当てはめて、2つの英文がどちらも正しくなるかを確かめる。"],
                pc=[("答え", 2), ("1文目の解釈", 2), ("2文目の解釈", 2), ("順番と結論", 2)],
                pit=["younger / shorter や not as ～ as の文を、向きを逆にせずに読む。", "最上級の the youngest を「いちばん年上」と取り違える。"])


ACTS = [
    ("サッカーをすること", "テレビでサッカーを見ること", "Playing soccer is more exciting than watching it on TV. I can enjoy it with my friends.",
     "動名詞 Playing soccer と watching it を主語・比べる相手にし、長い語 exciting を more exciting にしている。"),
    ("本を読むこと", "映画を見ること", "Reading books is more interesting than watching movies. I can imagine the story freely.",
     "動名詞 Reading books と watching movies を比べ、more interesting を使っている。"),
    ("自転車で学校へ行くこと", "歩いて学校へ行くこと", "Going to school by bike is faster than walking. But walking is better for my health.",
     "動名詞 Going と walking を比べ、faster と better（good の比較級）を使っている。"),
    ("英語を話すこと", "英語を書くこと", "Speaking English is more difficult than writing it for me. I want to practice speaking more.",
     "動名詞 Speaking と writing を比べ、more difficult を使っている。want to practice speaking で不定詞と動名詞も使っている。"),
    ("朝に勉強すること", "夜に勉強すること", "Studying in the morning is better than studying at night. My head is clearer in the morning.",
     "動名詞 Studying を主語と比べる相手にし、better と clearer を使っている。"),
]


@gen("thinking_writing", 2, ["cross_unit", "written_reasoning"], rel=["JH-ENG-G2-U02"])
def compare_acts(r):
    x, y, model, point = r.choice(ACTS)
    return desc(f"「{x}」と「{y}」を比べて、あなたの意見を英語で2文書きなさい。ただし、1文目は動名詞（～ing）を主語にした比較級の文にし、2文目でその理由を書くこと。",
                f"（解答例）{model}", f"（解答例の解説）{point} 主語の動名詞は単数扱いなので be 動詞は is。",
                [("1文目で動名詞を主語にし、比較級＋than を正しく使っている", 3), ("比べる相手も動名詞で表し、比較級の形（-er / more）が正しい", 2), ("2文目で意見に合う理由を書き、つづり・語順が正しい", 3)], d=4, p=8, lines=4,
                ap="前の単元の動名詞（～すること）を主語と than の後ろに置き、この単元の比較級でつなぐ。形容詞の長さで -er か more かを決める。",
                steps=["比べる2つの活動を動名詞のかたまりにする（Playing soccer / watching it）。", "使う形容詞を決め、比較級にする（exciting → more exciting）。", "〈動名詞＋is＋比較級＋than＋動名詞〉の文を書く。", "2文目で理由を書く。"],
                alt=["1文目を not as ～ as を使って逆の主語から書きかえ（Watching soccer on TV is not as exciting as playing it.）、同じ意見になるかを確かめる。"],
                pc=[("動名詞の主語と比較級", 3), ("比べる相手と形", 2), ("理由と表記", 3)],
                pit=["主語の動名詞の後ろを are にする。", "than の後ろを動詞の原形にして、比べる形がそろっていない。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(task, wrong, step, etype, tempt, fix, expl, steps, ap, alt, pit):
    return desc(f"{task}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい英文に書き直しなさい。", fix, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい英文に直している", 3), ("文法のルールを説明している", 1)], d=3, p=6, lines=4,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい英文", 3), ("ルールの説明", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix))


FORM_ERR = [
    ("ケンはトムより背が高い。", "Ken is more taller than Tom.", "Ken is taller than Tom.", "more taller", "formula",
     "tall は -er をつけて比較級にする語。more と -er を同時に使わない。", "「より～」を表す more もつければ、より比較らしくなると考えた。"),
    ("この犬はあの犬より大きい。", "This dog is biger than that one.", "This dog is bigger than that one.", "biger", "notation",
     "big は〈短母音＋子音字〉で終わるので g を重ねて bigger。", "そのまま -er をつければよいと考えた。"),
    ("この花はすべての中でいちばん美しい。", "This flower is the beautifulest of all.", "This flower is the most beautiful of all.", "beautifulest", "formula",
     "beautiful は長い語なので、最上級は most beautiful。", "どの語にも -est をつければよいと考えた。"),
    ("これはこの店でいちばんよいカメラだ。", "This is the goodest camera in this shop.", "This is the best camera in this shop.", "goodest", "formula",
     "good の最上級は不規則に変化して best。", "規則どおり -est をつけた。"),
    ("今日は昨日より忙しい。", "I am busyer today than yesterday.", "I am busier today than yesterday.", "busyer", "notation",
     "busy は〈子音字＋y〉で終わるので y を i にかえて busier。", "y をそのまま残して -er をつけた。"),
    ("私の姉は母より上手に料理をする。", "My sister cooks more better than my mother.", "My sister cooks better than my mother.", "more better", "formula",
     "better はすでに well の比較級なので more はつけない。", "better の前に more をつけると「もっと上手」が強調できると考えた。"),
    ("この問題はあの問題よりやさしい。", "This question is more easy than that one.", "This question is easier than that one.", "more easy", "formula",
     "easy は y を i にかえて -er をつける語。比較級は easier。", "「やさしい」が日本語では長い語なので more を使うと考えた。"),
    ("8月は1年でいちばん暑い月だ。", "August is the hotest month of the year.", "August is the hottest month of the year.", "hotest", "notation",
     "hot は〈短母音＋子音字〉で終わるので t を重ねて hottest。", "子音字を重ねるルールを忘れた。"),
]


@gen("error_correction", 4, ["common_error", "computation"])
def err_form(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(FORM_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", etype, tempt, fix, f"{rule}正しくは {fix}",
                    ["比較級・最上級の作り方（-er / more、つづりのルール、不規則変化）を確認する。", f"「{where}」の部分の誤りを見つける：{rule}", f"正しい英文：{fix}"],
                    "比較級・最上級は、①-er か more か、②つづりのルール（e・重ねる・y→i）、③不規則変化、の順に確かめる。",
                    ["直した語を原級→比較級→最上級の3つ並べて書き、変化の仕方がそろっているかを確かめる。"],
                    ["more と -er を両方つける。", "子音字を重ねる語・y を i にかえる語のつづりを誤る。"])


STRUCT_ERR = [
    ("ミカはクラスでいちばん速く泳ぐ。", "Mika swims the fastest of her class.", "Mika swims the fastest in her class.", "of her class", "condition",
     "her class は1つの集団を表すので in を使う。", "「クラスの中で」の「の」につられて of を使った。"),
    ("これは3つの中でいちばん小さい箱だ。", "This is the smallest box in the three.", "This is the smallest box of the three.", "in the three", "condition",
     "the three は複数のものを表す語句なので of を使う。", "「～の中で」をいつも in で表せると考えた。"),
    ("ユミは姉と同じくらい背が高い。", "Yumi is as taller as her sister.", "Yumi is as tall as her sister.", "as taller as", "formula",
     "as と as の間は原級。taller を tall にする。", "比べる文なので比較級を使うと考えた。"),
    ("この湖は日本でいちばん深い。", "This lake is deepest in Japan.", "This lake is the deepest in Japan.", "is deepest", "notation",
     "最上級を使って「いちばん～」というときは、ふつう the をつける。", "比較級と同じように the は不要だと考えた。"),
    ("彼は世界でいちばん有名な科学者の1人だ。", "He is one of the most famous scientist in the world.", "He is one of the most famous scientists in the world.", "scientist", "notation",
     "one of the＋最上級の後ろの名詞は複数形にする。", "「1人」という日本語につられて単数形にした。"),
    ("私は冬より夏のほうが好きだ。", "I like summer more better than winter.", "I like summer better than winter.", "more better", "formula",
     "「～より…のほうが好き」は like ～ better than … で表す。more は不要。", "more と better のどちらも「より」の意味なので、両方使えばよいと考えた。"),
]


@gen("error_correction", 3, ["common_error", "condition_check"])
def err_struct(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(STRUCT_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", etype, tempt, fix, f"{rule}正しくは {fix}",
                    ["比べ方（2つ・いちばん・同じくらい）と使う型を確認する。", f"「{where}」の部分の誤りを見つける：{rule}", f"正しい英文：{fix}"],
                    "比較の文では、than / the＋最上級＋in・of / as＋原級＋as のセットがくずれていないかを確かめる。",
                    ["直した文を日本語に訳し直し、比べる範囲や相手が問題の日本語と一致するかを確かめる。"],
                    ["最上級の範囲で in と of を取り違える。", "as ～ as の間に比較級を入れる。"])


MEAN_ERR = [
    ("私は兄ほど背が高くない。", "I am not as short as my brother.", "I am not as tall as my brother.", "short", "interpretation",
     "「兄ほど背が高くない」は not as tall as。not as short as だと「兄ほど背が低くない（自分のほうが高い）」と逆の意味になる。", "日本語の「高くない」を「低い」と考えて short を使った。"),
    ("「犬とネコではどちらが好きですか。」「犬のほうが好きです。」", "Which do you like better, dogs or cats? ― I like dogs the best.", "Which do you like better, dogs or cats? ― I like dogs better.", "the best", "concept",
     "2つのうちどちらかを答えるので比較級 better を使う。the best は3つ以上の中でいちばんのとき。", "「好き」と答えるときは the best だと覚えていた。"),
    ("「あなたの家族でいちばん早く起きるのはだれですか。」「父です。」", "Who gets up the earliest in your family? ― My father is.", "Who gets up the earliest in your family? ― My father does.", "is", "concept",
     "Who gets up ～? は一般動詞の疑問文なので does で答える。", "Who is ～? の答え方（～ is.）と混同した。"),
    ("私のかばんはあなたのかばんより軽い。", "My bag is heavier than yours.", "My bag is lighter than yours.", "heavier", "interpretation",
     "「軽い」は light、比較級は lighter。heavier だと「重い」で逆の意味になる。", "比べる言葉としてよく見る heavy を、意味を確かめずに使った。"),
    ("トムはケンより若い。", "Tom is older than Ken.", "Tom is younger than Ken.", "older", "interpretation",
     "「若い」は young の比較級 younger。older だと「年上」で逆の意味になる。", "年齢の比較は old を使うと覚えていて、意味の向きを確かめなかった。"),
    ("この映画はあの映画ほどおもしろくない。", "This movie is more interesting than that one.", "This movie is not as interesting as that one.", "more interesting than", "interpretation",
     "「…ほど～ではない」は not as＋原級＋as で表す。more interesting than だと「よりおもしろい」で逆の意味になる。", "「おもしろい」と「比べる」から比較級を使った。"),
]


@gen("error_correction", 3, ["common_error", "concept"])
def err_meaning(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(MEAN_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", etype, tempt, fix, f"{rule}正しくは {fix}",
                    ["日本語が表している事実（どちらが上か・2つか3つ以上か）を確認する。", f"「{where}」の部分の誤りを見つける：{rule}", f"正しい英文：{fix}"],
                    "比較の文は、形が正しくても意味の向きが逆になることがある。「どちらが上か」を日本語と英語で照らし合わせる。",
                    ["直した英文を、主語を入れかえた別の言い方にして、日本語の事実と一致するかを確かめる。"],
                    ["not as ～ as で反対の意味の語を使い、意味が逆になる。", "質問の動詞に合わせずに答える。"])


GENERATORS = [spelling, than_choice, in_or_of, as_as, irregular,
              table_read, rewrite, build_order, answer_q, jp_to_en,
              table_write, explain_difference, deduce, compare_acts,
              err_form, err_struct, err_meaning]
