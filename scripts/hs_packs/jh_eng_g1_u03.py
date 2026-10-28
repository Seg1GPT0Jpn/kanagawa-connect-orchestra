"""単元パック：中学1年 英語 疑問詞を使った疑問文（what / who / where / when / why / how・how many / how much・whose / which）。"""
import random

from banks._common import desc, mc, order, sa
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem,
                         tp)

UNIT_ID = "JH-ENG-G1-U03"

PREREQUISITES = [
    ("JH-ENG-G1-U01", "be 動詞の疑問文（Is ～?）と一般動詞の疑問文（Do / Does ～?）の語順。疑問詞を使った疑問文は、この語順の前に疑問詞を置いて作る。"),
    ("JH-ENG-G1-U02", "How many の後ろに置く名詞の複数形と、Whose ～? に答えるときの所有代名詞（mine, his など）や Ken's の形。"),
]
EXTENSIONS = [
    ("JH-ENG-G1-U05", "What did you do yesterday? のように、過去の文でも「疑問詞＋疑問文の語順」は同じで、do / does が did に変わる。"),
    ("JH-ENG-G2-U01", "What will you do? / Where are you going to go? のように、未来表現でも疑問詞を文頭に置く。"),
    ("JH-ENG-G3-U04", "I know where he lives. のような間接疑問文では、疑問詞の後ろがふつうの文の語順になる。この単元の語順と比べて学ぶ。"),
    ("HS-ENG-U06", "where・when・what などは、高校の関係詞の学習で、関係副詞や関係代名詞 what としても使われる。"),
]

# 疑問詞の意味
CAT_MEAN = {"What": "「何」をたずねる", "Who": "「だれ」をたずねる", "Where": "「どこ」（場所）をたずねる", "When": "「いつ」（時）をたずねる",
            "Why": "「なぜ」（理由）をたずねる", "How": "「どのように」（方法・手段）や「どんな様子」（状態）をたずねる",
            "Whose": "「だれの（もの）」（持ち主）をたずねる", "Which": "「どちら・どれ」（限られたものの中からの選択）をたずねる",
            "How many": "「いくつ・何人」（数）をたずねる", "How much": "「いくら」（値段）をたずねる", "How old": "「何歳」（年齢）をたずねる",
            "What time": "「何時」（時刻）をたずねる", "What day": "「何曜日」をたずねる", "What color": "「何色」をたずねる", "What sport": "「何のスポーツ」をたずねる"}
WORDS = ["What", "Who", "Where", "When", "Why", "How", "Whose", "Which"]

# 問答バンク：(種類, 疑問文, 答え, Yes / No での誤答, 疑問文の日本語, 誤答の選択肢から除く疑問詞)
QA = [
    ("Where", "Where do you live?", "I live in Kawasaki.", "Yes, I do.", "あなたはどこに住んでいますか。", ()),
    ("Where", "Where is my bag?", "It's on the desk.", "Yes, it is.", "私のかばんはどこにありますか。", ()),
    ("Where", "Where does your father work?", "He works at a hospital.", "Yes, he does.", "あなたのお父さんはどこで働いていますか。", ()),
    ("Where", "Where are Ken and Emi now?", "They're in the gym.", "Yes, they are.", "ケンとエミは今どこにいますか。", ()),
    ("Where", "Where do you play soccer?", "I play it in the park.", "Yes, I do.", "あなたはどこでサッカーをしますか。", ()),
    ("When", "When is Ken's birthday?", "It's October 3.", "Yes, it is.", "ケンの誕生日はいつですか。", ()),
    ("When", "When do you practice the piano?", "I practice it after dinner.", "Yes, I do.", "あなたはいつピアノを練習しますか。", ()),
    ("When", "When does your sister study English?", "She studies it before breakfast.", "Yes, she does.", "あなたのお姉さんはいつ英語を勉強しますか。", ()),
    ("What", "What do you have in your hand?", "I have a pen.", "Yes, I do.", "あなたは手に何を持っていますか。", ("Which",)),
    ("What", "What does your sister do on Sundays?", "She plays tennis.", "Yes, she does.", "あなたのお姉さんは日曜日に何をしますか。", ("Which",)),
    ("What", "What do you eat for breakfast?", "I eat rice and miso soup.", "Yes, I do.", "あなたは朝食に何を食べますか。", ("Which",)),
    ("What sport", "What sport do you like?", "I like volleyball.", "Yes, I do.", "あなたは何のスポーツが好きですか。", ("Which", "Whose")),
    ("What time", "What time does Ken get up?", "He gets up at six.", "Yes, he does.", "ケンは何時に起きますか。", ("Which", "Whose")),
    ("What time", "What time do you go to bed?", "I go to bed at ten.", "Yes, I do.", "あなたは何時に寝ますか。", ("Which", "Whose")),
    ("What day", "What day is it today?", "It's Wednesday.", "Yes, it is.", "今日は何曜日ですか。", ("Which", "Whose")),
    ("What color", "What color is your bike?", "It's blue.", "Yes, it is.", "あなたの自転車は何色ですか。", ("Which", "Whose")),
    ("Who", "Who is that woman?", "She's our new English teacher.", "Yes, she is.", "あの女性はだれですか。", ("What",)),
    ("Who", "Who is the boy by the door?", "He's my brother, Sota.", "Yes, he is.", "ドアのそばの男の子はだれですか。", ("What", "Which")),
    ("Who", "Who plays the guitar in your family?", "My father does.", "Yes, he does.", "あなたの家族ではだれがギターをひきますか。", ("What", "Which")),
    ("Who", "Who cleans this room?", "Aya and Mai do.", "Yes, they do.", "だれがこの部屋をそうじしますか。", ("What", "Which")),
    ("Whose", "Whose umbrella is this?", "It's mine.", "Yes, it is.", "これはだれのかさですか。", ("What", "Which")),
    ("Whose", "Whose shoes are these?", "They're my brother's.", "Yes, they are.", "これらはだれのくつですか。", ("What", "Which")),
    ("Whose", "Whose is this notebook?", "It's Ken's.", "Yes, it is.", "このノートはだれのものですか。", ("What", "Which")),
    ("Which", "Which do you like, cats or dogs?", "I like cats.", "Yes, I do.", "あなたはねことイヌのどちらが好きですか。", ("What", "Whose")),
    ("Which", "Which season do you like, summer or winter?", "I like winter.", "Yes, I do.", "あなたは夏と冬のどちらの季節が好きですか。", ("What", "Whose")),
    ("Which", "Which is your bike, this one or that one?", "That one is mine.", "Yes, it is.", "こちらとあちらのどちらがあなたの自転車ですか。", ("What", "Whose")),
    ("Why", "Why do you like summer?", "Because my birthday is in August.", "Yes, I do.", "あなたはなぜ夏が好きなのですか。", ()),
    ("Why", "Why is Ken absent today?", "Because he is sick.", "Yes, he is.", "ケンはなぜ今日休んでいるのですか。", ()),
    ("Why", "Why do you get up early?", "Because I walk my dog every morning.", "Yes, I do.", "あなたはなぜ早く起きるのですか。", ()),
    ("How", "How do you go to school?", "By bike.", "Yes, I do.", "あなたはどうやって学校に行きますか。", ()),
    ("How", "How is the weather in Osaka?", "It's sunny.", "Yes, it is.", "大阪の天気はどうですか。", ("What",)),
    ("How", "How does Ken come to school?", "He comes by bus.", "Yes, he does.", "ケンはどうやって学校に来ますか。", ()),
    ("How many", "How many cats do you have?", "I have three.", "Yes, I do.", "あなたはねこを何匹飼っていますか。", ()),
    ("How many", "How many brothers does Aya have?", "She has two.", "Yes, she does.", "アヤには兄弟が何人いますか。", ()),
    ("How much", "How much is this cap?", "It's 1,500 yen.", "Yes, it is.", "この帽子はいくらですか。", ()),
    ("How much", "How much are these apples?", "They're 300 yen.", "Yes, they are.", "これらのりんごはいくらですか。", ()),
    ("How old", "How old is your sister?", "She's fourteen.", "Yes, she is.", "あなたのお姉さんは何歳ですか。", ()),
    ("How old", "How old is this temple?", "It's about 800 years old.", "Yes, it is.", "このお寺はできてから何年ですか。", ()),
]
TWO = ["How many", "How much", "How old", "What time", "What day", "What color", "What sport"]


def cap(s):
    return s[0].upper() + s[1:]


def local(key):
    return random.Random(key)


# ======================================================================
# 授業プリント
# ======================================================================

LESSON = lesson(
    goals=["what / who / where / when / why / how / whose / which の意味を区別し、たずねたい内容に合う疑問詞を選べる。",
           "「疑問詞＋疑問文の語順（be 動詞・do / does＋主語＋…）」で疑問文を組み立てられる。How many＋複数形、What time などのまとまりも使える。",
           "疑問詞を使った疑問文には Yes / No ではなく、たずねられた内容を具体的に答えられる。"],
    duration=50,
    readiness=["小学校の外国語で What do you like? / When is your birthday? / Where is ～? などのやりとりを経験している。",
               "be 動詞の疑問文（Is ～?）と一般動詞の疑問文（Do / Does ～?）を作れる。",
               "名詞の複数形と所有代名詞（mine, yours など）を使える。"],
    flow=[("導入：Yes / No では答えられない質問", 5, "Do you live in Yokohama? と Where do you live? を比べ、たずねる内容の違いに気づかせる"),
          ("疑問詞の意味", 10, "8つの疑問詞と How many / What time などのまとまりを整理する"),
          ("疑問文の組み立て", 15, "「疑問詞＋疑問文の語順」を、下線部をたずねる疑問文づくりで練習する（例題1・2）"),
          ("答え方と主語をたずねる Who", 13, "答え方の型と、Who plays ～? ― Ken does. の語順を確認する（例題3）"),
          ("まとめと確認", 7, "確認問題3問、問題プリントA の課題指示")],
    sections=[
        intro("in1", "「はい・いいえ」で答えられない質問をする",
              "Do you live in Yokohama? には Yes / No で答えられますが、相手がどこに住んでいるかを知らないときは、この質問はできません。そんなときは「どこ」にあたる疑問詞 where を使って Where do you live? とたずねます。疑問詞を使うと、場所・時・人・数・理由などを具体的にたずねることができ、会話を大きく広げられます。",
              bullets=["Do you live in Yokohama? ― Yes, I do.（Yes / No で答える）", "Where do you live? ― I live in Kawasaki.（場所を具体的に答える）",
                       "疑問詞はいつも文の先頭に置く。後ろは、これまで学んだ疑問文の語順になる。"],
              points=[tp("2つの質問を板書し、どちらの質問なら相手の住所を知らなくてもたずねられるかを考えさせる。",
                         ask="Where do you live? に Yes, I do. と答えられるか。", expect="答えられない。場所を答える必要がある。", timing="導入の冒頭")]),
        definition("df1", "疑問詞とその意味",
                   "疑問詞は、たずねたい内容によって使い分けます。後ろに名詞や形容詞を続けて、ひとまとまりで使うものもあります。",
                   bullets=["what（何）：What do you have? ／ what＋名詞：What sport / What color / What time（何時）/ What day（何曜日）",
                            "who（だれ）：Who is that woman?", "where（どこ）：Where do you live?", "when（いつ）：When is your birthday?",
                            "why（なぜ）：Why do you like summer? ― Because ～.", "how（どのように・どんな様子）：How do you go to school? ― By bike.",
                            "how many＋複数形（いくつ）：How many cats do you have? ／ how much（いくら）：How much is this cap? ／ how old（何歳）",
                            "whose（だれの・だれのもの）：Whose umbrella is this? ― It's mine. ／ which（どちら）：Which do you like, cats or dogs?"],
                   conditions=["How many の後ろの数えられる名詞は複数形にする（How many cat は誤り）。",
                               "交通手段を答えるときは by bus / by bike のように a や the をつけない。"],
                   points=[tp("疑問詞を日本語の「何・だれ・どこ・いつ・なぜ・どのように・だれの・どちら」と対応させたカードを作り、ペアで出し合わせる。",
                              caution="when（いつ）と where（どこ）、who（だれ）と whose（だれの）のつづりと意味の混同が多い。")]),
        theorem("th1", "疑問詞を使った疑問文の語順",
                "疑問詞（＋名詞）＋ be 動詞 ＋主語 ～?　／　疑問詞（＋名詞）＋ do / does ＋主語＋動詞の原形 ～?",
                ["be 動詞の文：Where is Ken now?（Is Ken ～? の前に Where）", "一般動詞の文：Where does Ken live?（Does Ken live ～? の前に Where。live は原形）",
                 "how many などのまとまりは、名詞までをまとめて文頭に置く：How many cats do you have?",
                 "主語をたずねる who / what は、疑問詞がそのまま主語になり、ふつうの文と同じ語順：Who plays the guitar? ― My father does."],
                body="答えるときは Yes / No を使わず、たずねられた内容（場所・時・数など）を答えます。答えの文でも主語は代名詞で受けるのがふつうです（Where does Ken live? ― He lives in Kobe.）。",
                points=[tp("「疑問詞＋いつもの疑問文」というイメージを、Does Ken live in Kobe? の in Kobe を消して Where を前に置く操作で見せる。",
                           ask="Ken lives in Kobe. の in Kobe をたずねる疑問文はどう作るか。", expect="Does Ken live in Kobe? にして、in Kobe を Where にかえて文頭へ。")]),
        derivation("dv1", "下線部をたずねる疑問文の作り方（なぜその語順になるのか）",
                   ["① もとの文を Yes / No でたずねる疑問文にする：Ken lives in Kobe. → Does Ken live in Kobe?",
                    "② たずねたい部分（下線部）を、内容に合う疑問詞にかえる：in Kobe は場所 → where。",
                    "③ 疑問詞を文の先頭に移す。下線部があった場所には何も残さない：Where does Ken live?",
                    "④ 数をたずねるときは、名詞もいっしょに前に出す：Ken has three cats. → How many cats does Ken have?",
                    "⑤ 主語そのものをたずねるときは、主語を who にかえるだけで、do / does は使わない：Ken plays the guitar. → Who plays the guitar?",
                    "⑥ 最後に、答えの文として成り立つか（Where ～? → He lives in Kobe.）を確かめる。"],
                   body="この手順を使うと、どんな疑問詞の疑問文も「Yes / No の疑問文＋疑問詞」という同じ考え方で作れます。",
                   points=[tp("手順①〜③を板書で色分けし、下線部が「消えて」疑問詞として先頭に「移動する」様子を矢印で示す。", timing="例題1の前"),
                           tp("⑤の主語をたずねる Who は例外的に見えるが、「主語を who にかえるだけ」と考えれば自然であることを確認する。",
                              ask="Who does play the guitar? としないのはなぜか。", expect="who が主語なので、ふつうの文の語順のまま主語を入れかえるだけだから。")]),
        example("ex1", "例題1　下線部をたずねる疑問文",
                "下線部をたずねる疑問文を書きなさい。(1) My sister gets up [[u:at six]].　(2) This bike is [[u:Aya's]].　(3) Ken has [[u:three]] dictionaries.",
                ["(1) 時刻なので What time。Does your sister get up at six? の at six を What time にして文頭へ。", "(2) 持ち主なので Whose。名詞 bike もいっしょに前に出す。",
                 "(3) 数なので How many。名詞 dictionaries（複数形）もいっしょに前に出す。"],
                "(1) What time does your sister get up?　(2) Whose bike is this?　(3) How many dictionaries does Ken have?",
                thinking="Yes / No の疑問文を作ってから、下線部を疑問詞にかえて先頭に移す。",
                points=[tp("(1) で My sister が質問では your sister になることに触れ、会話の場面を意識させる。")],
                misconceptions=[("What time your sister gets up?", "疑問詞の後ろは疑問文の語順。does を入れ、動詞は原形 get。")]),
        example("ex2", "例題2　答えに合う疑問詞を選ぶ",
                "（　）に入る疑問詞を答えなさい。(1) (　) do you practice the piano? ― After dinner.　(2) (　) is the weather in Osaka? ― It's sunny.　(3) (　) do you like, cats or dogs? ― I like cats.",
                ["(1) 答えが「夕食後に」という時なので When。", "(2) 答えが天気の様子なので How。", "(3) 2つの中から選んでいるので Which。"],
                "(1) When　(2) How　(3) Which",
                thinking="答えの文が「何を」伝えているか（時・様子・選択など）から、疑問詞を逆算する。",
                points=[tp("(2) を What is the weather? としない理由は、英語では天気の様子を how でたずねるからであると簡潔に伝える。")]),
        example("ex3", "例題3　主語をたずねる Who と答え方",
                "下線部をたずねる疑問文を書き、その疑問文に答える文も書きなさい。[[u:My mother]] cooks dinner on Sundays.",
                ["主語 My mother をたずねるので Who を使う。", "Who が主語になるので do / does は使わず、Who cooks dinner on Sundays? とする（who は3人称単数あつかいで cooks）。",
                 "答えは「主語＋does」で、My mother does. とする。"],
                "Who cooks dinner on Sundays? ― My mother does.",
                thinking="たずねる部分が主語か、それ以外かで語順が変わる。",
                points=[tp("答えの My mother does. の does は cooks dinner on Sundays をくり返さないための語であることを説明する。")],
                misconceptions=[("Who does cook dinner on Sundays?", "主語をたずねる who の後ろには、ふつう do / does を入れない。Who cooks ～?")]),
        board("bd1", "板書案",
              [("① 疑問詞の意味", ["what 何／who だれ", "where どこ／when いつ", "why なぜ → Because ～.", "how どのように・どんな様子", "whose だれの／which どちら"]),
               ("② 語順", ["Does Ken live in Kobe?", "→ Where does Ken live?", "疑問詞＋疑問文の語順", "How many＋複数形＋do / does ～?", "主語をたずねる：Who plays ～?"]),
               ("③ 答え方", ["Yes / No は使わない", "Where ～? → in ～ / at ～", "How ～? → By bus.（a / the なし）", "Whose ～? → It's mine. / It's Ken's.", "Who ～? → My father does."])],
              points=[tp("②の列は、もとの文から疑問文ができるまでを矢印でつなぎ、生徒がノートに同じ手順で書けるようにする。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("答えの文から疑問詞を考える練習（逆算）を多く取り入れる。", ask="It's 1,500 yen. はどんな質問への答えか。", expect="How much is ～? への答え。"),
               tp("疑問詞の後ろの語順（do / does の入れ忘れ、動詞の s の残し）は、前の単元の疑問文の作り方に立ち返って確認させる。", caution="Where you live? のように do を落とす誤りが多い。"),
               tp("How many の後ろは複数形、How much は値段、という区別を、買い物の場面設定で練習させる。", timing="例題1の後"),
               tp("Who が主語の疑問文は、答え方（～ does.）とセットで練習する。"),
               tp("問題プリント D では「語順の誤り」と「答え方の誤り」に分けて整理させる。")],
              misconceptions=[("Where you live?", "疑問詞の後ろは疑問文の語順。Where do you live?"),
                              ("How many cat do you have?", "How many の後ろは複数形。How many cats ～?"),
                              ("Where do you live? ― Yes, I do.", "疑問詞の疑問文には Yes / No で答えない。I live in ～.")]),
        summary("sm1", "まとめ",
                ["疑問詞はたずねる内容で選ぶ：何 what／だれ who／どこ where／いつ when／なぜ why／どのように how／だれの whose／どちら which。",
                 "語順は「疑問詞（＋名詞）＋ be 動詞／do・does ＋主語 ～?」。主語をたずねる who は「Who＋動詞 ～?」。",
                 "答えは Yes / No を使わず、たずねられた内容を具体的に答える。"]),
        check("ck1", "確認問題",
              [("Aya lives in Nagoya. の in Nagoya をたずねる疑問文を書きなさい。", "Where does Aya live?"),
               ("How (　) is this T-shirt? ― It's 2,000 yen. の（　）に入る語を答えなさい。", "much"),
               ("Whose bag is this? に「私のもの」と答える文を書きなさい。", "It's mine.")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

def word_reason(w):
    return f"{w} は{CAT_MEAN[w]}疑問詞"


@gen("basic_check", 5, ["concept", "condition_check"])
def choose_wh(r):
    cat, q, a, yn, jq, ex = r.choice(QA)
    first = q.split()[0]
    stem_q = "(　)" + q[len(first):]
    pool = [w for w in WORDS if w != first and w not in ex]
    rr = local(q)
    wrongs = rr.sample(pool, 3)
    why = {w: (f"{word_reason(w)}。答え「{a}」は{CAT_MEAN[cat]}質問への答えなので合わない。", "疑問詞の意味の混同") for w in wrongs}
    return mc(f"対話が成り立つように、（　）に入る最も適切な疑問詞を選びなさい。\n{stem_q} ― {a}", [first] + wrongs,
              f"答え「{a}」から、{CAT_MEAN[cat]}質問だとわかる。よって {first}。疑問文の意味：{jq}", d=2,
              ap="答えの文が何を伝えているか（場所・時・人・数・理由・方法・持ち主・選択）に注目して、疑問詞を逆算する。",
              steps=[f"答えの文「{a}」が伝えている内容を確かめる。", f"その内容をたずねる疑問詞を選ぶ：{CAT_MEAN[cat]} → {first}。", "疑問詞を入れた文を訳し、答えと対応しているかを確かめる。"],
              alt=[f"選んだ疑問詞を入れた質問「{q}」と答えを続けて読み、日本語の会話（{jq}）として自然かを確かめる。"],
              pc=[("答えの内容を正しく読み取っている", 1), ("正しい疑問詞を選んでいる", 1)],
              pit=["where と when、who と whose のように、つづりの似た疑問詞を取り違える。", "空所の後ろの名詞（time, color など）を見落とす。"], why=why)


@gen("basic_check", 5, ["concept", "common_error"])
def choose_answer(r):
    cat, q, a, yn, jq, ex = r.choice(QA)
    rr = local(q + "ans")
    others = [x for x in QA if x[0] != cat and x[0].split()[0] != cat.split()[0]]
    d1, d2 = rr.sample(others, 2)
    why = {yn: ("疑問詞を使った疑問文には、Yes / No で答えない。たずねられた内容を具体的に答える。", "Yes / No 疑問文と疑問詞の疑問文の混同"),
           d1[2]: (f"「{d1[2]}」は{CAT_MEAN[d1[0]]}質問（例：{d1[1]}）への答えで、この質問とは対応しない。", "疑問詞の意味の取り違え"),
           d2[2]: (f"「{d2[2]}」は{CAT_MEAN[d2[0]]}質問（例：{d2[1]}）への答えで、この質問とは対応しない。", "疑問詞の意味の取り違え")}
    return mc(f"次の質問に対する答えとして最も適切なものを選びなさい。\n{q}", [a] + list(why),
              f"{q} は{CAT_MEAN[cat]}質問（{jq}）。答えは {a}", d=2,
              ap="質問の最初の疑問詞（とその後ろの名詞）を見て、何をたずねているかを決めてから答えを選ぶ。",
              steps=[f"疑問詞を確認する：{cat}。", f"何をたずねているかを確かめる：{CAT_MEAN[cat]}。", f"その内容を答えている {a} を選ぶ。"],
              alt=["選んだ答えから逆に質問を作ってみて、問題の質問と一致するかを確かめる。"],
              pc=[("質問の意味を正しく理解している", 1), ("正しい答えを選んでいる", 1)],
              pit=["疑問詞で始まる質問に Yes / No で答えてしまう。"], why=why)


HOWS = [
    ("How many", "(　) brothers does Aya have?", "She has two.", "アヤには兄弟が何人いますか。"),
    ("How many", "(　) cats do you have?", "I have three.", "あなたはねこを何匹飼っていますか。"),
    ("How many", "(　) classes do you have on Monday?", "We have six.", "あなたたちは月曜日に授業がいくつありますか。"),
    ("How many", "(　) CDs does your father have?", "He has about a hundred.", "あなたのお父さんはCDを何枚持っていますか。"),
    ("How much", "(　) is this T-shirt?", "It's 2,000 yen.", "このTシャツはいくらですか。"),
    ("How much", "(　) are these apples?", "They're 300 yen.", "これらのりんごはいくらですか。"),
    ("How much", "(　) is the ticket?", "It's 800 yen.", "そのチケットはいくらですか。"),
    ("How old", "(　) is your grandfather?", "He's seventy.", "あなたのおじいさんは何歳ですか。"),
    ("How old", "(　) are you?", "I'm thirteen.", "あなたは何歳ですか。"),
    ("What time", "(　) do you go to bed?", "At ten.", "あなたは何時に寝ますか。"),
    ("What time", "(　) does the movie start?", "It starts at two.", "その映画は何時に始まりますか。"),
    ("What day", "(　) is it today?", "It's Friday.", "今日は何曜日ですか。"),
    ("What color", "(　) is your cap?", "It's red.", "あなたの帽子は何色ですか。"),
]


@gen("basic_check", 5, ["condition_check", "concept"])
def how_phrase(r):
    cat, q, a, jq = r.choice(HOWS)
    rr = local(q)
    pool = ["How many", "How much", "How old", "What time", "What day", "What color"]
    wrongs = rr.sample([w for w in pool if w != cat], 3)
    why = {w: (f"{w} は{CAT_MEAN[w]}表現。答え「{a}」とは対応しない。", "疑問詞のまとまりの意味の混同") for w in wrongs}
    return mc(f"対話が成り立つように、（　）に入る最も適切なものを選びなさい。\n{q} ― {a}", [cat] + wrongs,
              f"答え「{a}」は{CAT_MEAN[cat].replace('をたずねる', '')}を答えているので {cat}。疑問文の意味：{jq}", d=2,
              ap="答えに出てくる語（数・円・年齢・時刻・曜日・色）に注目して、どのまとまりでたずねたかを考える。",
              steps=[f"答え「{a}」が何を伝えているかを確かめる。", f"それをたずねる表現を選ぶ：{cat}（{CAT_MEAN[cat]}）。"],
              alt=["選んだ表現を入れた文を日本語に訳し、答えと会話が成り立つかを確かめる。"],
              pc=[("答えの内容を正しく読み取っている", 1), ("正しい表現を選んでいる", 1)],
              pit=["数をたずねる How many と値段をたずねる How much を取り違える。"], why=why)


WH_SUBJ = [("you", "2", "あなた"), ("your sister", "3s", "あなたのお姉さん"), ("Ken", "3s", "ケン"), ("Ms. Green", "3s", "グリーン先生"),
           ("Tom and Emi", "pl", "トムとエミ"), ("your parents", "pl", "あなたのご両親")]
WH_GV = [("Where", "live", "はどこに住んでいますか"), ("What time", "get up", "は何時に起きますか"), ("What", "study after dinner", "は夕食後に何を勉強しますか"),
         ("How", "go to school", "はどうやって学校に行きますか"), ("When", "practice the piano", "はいつピアノを練習しますか"),
         ("What sport", "like", "は何のスポーツが好きですか"), ("Why", "like winter", "はなぜ冬が好きなのですか"), ("What", "do on Sundays", "は日曜日に何をしますか")]
WH_BE = [("Where", "now", "は今どこにいますか"), ("How", "today", "は今日、調子はどうですか"), ("Why", "busy today", "はなぜ今日忙しいのですか")]


@gen("basic_check", 5, ["computation", "condition_check"], rel=[])
def aux_in_wh(r):
    S = r.choice(WH_SUBJ)
    if r.random() < 0.6:
        wh, rest, jt = r.choice(WH_GV)
        ok = "does" if S[1] == "3s" else "do"
        stem = f"{wh} (　) {S[0]} {rest}?"
        kind = "一般動詞の文"
    else:
        wh, rest, jt = r.choice(WH_BE)
        ok = "is" if S[1] == "3s" else "are"
        stem = f"{wh} (　) {S[0]} {rest}?"
        kind = "be 動詞の文"
    J = f"{S[2]}{jt}。"
    kd = {"2": "you", "3s": "3人称単数", "pl": "複数"}[S[1]]
    why = {}
    for w in ("do", "does", "is", "are"):
        if w == ok:
            continue
        if (w in ("do", "does")) != (ok in ("do", "does")):
            why[w] = (f"この文は{kind}である。{'一般動詞の文では be 動詞ではなく do / does を使う' if w in ('is', 'are') else 'be 動詞の文では do / does は使わない'}。", "be 動詞の文と一般動詞の文の混同")
        else:
            why[w] = (f"主語 {S[0]} は{kd}なので {ok} を使う。", "主語と do / does・be 動詞の形の一致の誤り")
    return mc(f"日本語の意味を表すように、（　）に入る最も適切な語を選びなさい。\n{J}\n{stem}", [ok] + list(why),
              f"{kind}で、主語 {S[0]} は{kd}なので {ok}。疑問詞の後ろは、ふつうの疑問文の語順になる。", d=2,
              ap="疑問詞の後ろは「Yes / No の疑問文」と同じ語順。一般動詞があれば do / does、なければ be 動詞を選び、主語に合わせる。",
              steps=["主語の後ろに一般動詞（原形）があるかを確かめる。", f"主語 {S[0]} の種類（{kd}）を確かめる。", f"答え：{ok}"],
              alt=["疑問詞を取り除いた Yes / No の疑問文（例：Does Ken live ～?）を作ってみて、その文が正しいかを確かめる。"],
              pc=[("be 動詞の文か一般動詞の文かを判断している", 1), ("主語に合う形を選んでいる", 1)],
              pit=["主語が3人称単数なのに do を選ぶ。", "一般動詞の文なのに is / are を選ぶ。"], why=why)


# ======================================================================
# B 標準演習
# ======================================================================

# 一般動詞：(原形, 3単現, 下線の前の語, 下線部, 下線の後ろの語, 疑問詞, 下線部の内容)
SLOT = [
    ("live", "lives", "", "in Yokohama", "", "Where", "場所"),
    ("play", "plays", "soccer", "in the park", "", "Where", "場所"),
    ("study", "studies", "math", "in the library", "", "Where", "場所"),
    ("get", "gets", "up", "at six", "", "What time", "時刻"),
    ("go", "goes", "to bed", "at ten", "", "What time", "時刻"),
    ("practice", "practices", "the piano", "after school", "", "When", "時"),
    ("play", "plays", "tennis", "on Sundays", "", "When", "時"),
    ("go", "goes", "to school", "by bike", "", "How", "手段"),
    ("come", "comes", "to school", "by bus", "", "How", "手段"),
    ("eat", "eats", "", "rice", "for breakfast", "What", "もの"),
    ("read", "reads", "", "comic books", "after dinner", "What", "もの"),
    ("like", "likes", "", "baseball", "", "What sport", "スポーツの種類"),
]
# (平叙文の主語, 種類, 疑問文での主語, 疑問文での種類)
SS = [("I", "1s", "you", "2"), ("We", "pl", "you", "2"), ("Ken", "3s", "Ken", "3s"), ("My sister", "3s", "your sister", "3s"),
      ("Tom and Emi", "pl", "Tom and Emi", "pl"), ("Ms. Green", "3s", "Ms. Green", "3s")]
BE_SLOT = [
    ("Ken is [[u:in the gym]] now.", "Where is Ken now?", "場所", "Where"),
    ("My birthday is [[u:May 20]].", "When is your birthday?", "日付", "When"),
    ("This bag is [[u:Aya's]].", "Whose bag is this?", "持ち主", "Whose"),
    ("That woman is [[u:Ms. Green]].", "Who is that woman?", "人", "Who"),
    ("My sister is [[u:fifteen]].", "How old is your sister?", "年齢", "How old"),
    ("It is [[u:Tuesday]] today.", "What day is it today?", "曜日", "What day"),
    ("My bike is [[u:black]].", "What color is your bike?", "色", "What color"),
    ("The weather in Sapporo is [[u:snowy]] today.", "How is the weather in Sapporo today?", "様子", "How"),
    ("Ken and Emi are [[u:in the music room]].", "Where are Ken and Emi?", "場所", "Where"),
    ("Aya is absent [[u:because she is sick]].", "Why is Aya absent?", "理由", "Why"),
]


def j(*xs):
    return " ".join(x for x in xs if x)


@gen("standard_practice", 5, ["computation", "application"])
def make_wh(r):
    if r.random() < 0.65:
        base, s3, pre, slot, post, wh, what = r.choice(SLOT)
        S = r.choice(SS)
        verb = s3 if S[1] == "3s" else base
        src = j(S[0], verb, pre, f"[[u:{slot}]]", post) + "."
        aux = "does" if S[3] == "3s" else "do"
        ans = j(wh, aux, S[2], base, pre, post) + "?"
        how = f"下線部は{what}なので {wh}。一般動詞の文なので、疑問詞の後ろは {aux} ＋ {S[2]} ＋ 動詞の原形 {base}"
    else:
        src, ans, what, wh = r.choice(BE_SLOT)
        how = f"下線部は{what}なので {wh}。be 動詞の文なので、疑問詞の後ろは be 動詞＋主語の語順"
    note = "（I / We は質問では you にかえる）" if src.startswith(("I ", "We ")) else ("（My は質問では your にかえる）" if src.startswith("My ") else "")
    return sa(f"下線部をたずねる疑問文を英語で書きなさい。{note}\n{src}", ans, f"{how}。{ans}", d=3,
              ap="①Yes / No の疑問文にする、②下線部を内容に合う疑問詞にかえる、③疑問詞を文頭に移す、の順に考える。",
              steps=["もとの文を Yes / No でたずねる疑問文にする。", f"下線部（{what}）を疑問詞 {wh} にかえる。", "疑問詞を文頭に移し、下線部があった所には何も残さない。", f"答え：{ans}"],
              alt=["作った疑問文に、もとの文を答えとして続けて読み、会話が成り立つかを確かめる。"],
              pc=[("正しい疑問詞を選んでいる", 2), ("疑問詞の後ろの語順（be 動詞・do / does・主語・動詞の原形）が正しい", 2)],
              pit=["疑問詞の後ろの do / does を落とす（Where Ken lives?）。", "下線部の語句を文末に残してしまう（Where do you live in Yokohama?）。"])


COUNT_N = [("cat", "cats", "ねこ"), ("dictionary", "dictionaries", "辞書"), ("brother", "brothers", "兄弟"), ("box", "boxes", "箱"),
           ("watch", "watches", "腕時計"), ("pencil", "pencils", "鉛筆"), ("knife", "knives", "ナイフ"), ("photo", "photos", "写真"), ("key", "keys", "かぎ")]
PRICE = [("this cap", "is", "1,500 yen"), ("these shoes", "are", "4,000 yen"), ("this T-shirt", "is", "2,000 yen"), ("these apples", "are", "300 yen"),
         ("that bag", "is", "3,500 yen"), ("those pens", "are", "500 yen")]


@gen("standard_practice", 4, ["computation", "cross_unit"], rel=["JH-ENG-G1-U02"])
def count_question(r):
    if r.random() < 0.65:
        sg, pl, m = r.choice(COUNT_N)
        num = r.choice(["two", "three", "four", "five"])
        S = r.choice([("I", "you", "do"), ("Ken", "Ken", "does"), ("My father", "your father", "does"), ("We", "you", "do"), ("Aya", "Aya", "does")])
        verb = "has" if S[2] == "does" else "have"
        src = f"{S[0]} {verb} [[u:{num}]] {pl}."
        ans = f"How many {pl} {S[2]} {S[1]} have?"
        how = f"数をたずねるので How many。後ろの名詞は複数形 {pl} のまま前に出す。一般動詞 have の疑問文なので {S[2]} ＋ {S[1]} ＋ have"
    else:
        thing, be, price = r.choice(PRICE)
        disp = cap(thing)
        src = f"{disp} {be} [[u:{price}]]."
        ans = f"How much {be} {thing}?"
        how = f"値段をたずねるので How much。be 動詞の文なので How much ＋ {be} ＋ {thing}"
    note = "（I / We は質問では you、My は your にかえる）" if src.startswith(("I ", "We ", "My ")) else ""
    return sa(f"下線部をたずねる疑問文を英語で書きなさい。{note}\n{src}", ans, f"{how}。{ans}", d=3,
              ap="数なら How many＋複数形の名詞、値段なら How much を使う。疑問詞のまとまりを文頭に置き、後ろは疑問文の語順にする。",
              steps=["下線部が数か値段かを確かめる。", "How many なら、後ろの名詞（複数形）もいっしょに文頭に出す。", "後ろを疑問文の語順にする。", f"答え：{ans}"],
              alt=["作った疑問文に、もとの文を答えとして続けて読み、会話が成り立つかを確かめる。"],
              pc=[("How many / How much を正しく選んでいる", 2), ("名詞の形と語順が正しい", 2)],
              pit=["How many の後ろの名詞を単数形にする。", "名詞を文末に残す（How many do you have cats?）。"])


ORDERS = [
    ("あなたはふだん何時に起きますか。", ["what", "time", "do", "you", "usually", "get", "up"]),
    ("あなたのお兄さんはどこでテニスをしますか。", ["where", "does", "your", "brother", "play", "tennis"]),
    ("あなたは何匹のイヌを飼っていますか。", ["how", "many", "dogs", "do", "you", "have"]),
    ("これはだれのラケットですか。", ["whose", "racket", "is", "this"]),
    ("あなたはなぜ春が好きなのですか。", ["why", "do", "you", "like", "spring"]),
    ("あの背の高い男の人はだれですか。", ["who", "is", "that", "tall", "man"]),
    ("ケンはいつ図書館に行きますか。", ["when", "does", "Ken", "go", "to", "the library"]),
    ("あなたのお母さんはどうやって駅に行きますか。", ["how", "does", "your", "mother", "go", "to", "the station"]),
    ("あなたはどの教科がいちばん好きですか。", ["what", "subject", "do", "you", "like", "the best"]),
    ("このかばんはいくらですか。", ["how", "much", "is", "this", "bag"]),
    ("あなたの家族ではだれが夕食を作りますか。", ["who", "cooks", "dinner", "in", "your", "family"]),
    ("あなたは日曜日に何をしますか。", ["what", "do", "you", "do", "on", "Sundays"]),
    ("今日は何曜日ですか。", ["what", "day", "is", "it", "today"]),
]


@gen("standard_practice", 4, ["application", "computation"])
def build_order(r):
    jp, parts = r.choice(ORDERS)
    sent = cap(" ".join(parts)) + "?"
    return order(f"日本語の意味を表す疑問文になるように、次の語句を正しい順に並べなさい。文の最初にくる語も小文字で示してある。\n{jp}", parts,
                 f"{sent}　疑問詞（とその後ろの名詞）を文頭に置き、後ろは疑問文の語順にする。", d=3, p=4,
                 ap="まず疑問詞（how many＋名詞、what time などのまとまり）を文頭に置き、次に be 動詞または do / does、主語、動詞の順に並べる。",
                 steps=["疑問詞のまとまりを見つけて文頭に置く。", "be 動詞か do / does かを確かめ、その後ろに主語を置く。", f"完成文：{sent}"],
                 alt=["並べた疑問文に答える文を考えてみて（例：I get up at six.）、会話が成り立つかを確かめる。"],
                 pc=[("疑問詞のまとまりを文頭に置いている", 2), ("後ろの語順が正しい", 2)],
                 pit=["how many と名詞を離してしまう。", "主語をたずねる who の文に do / does を入れようとする。"])


@gen("standard_practice", 4, ["concept", "condition_check"])
def choose_question(r):
    cat, q, a, yn, jq, ex = r.choice(QA)
    rr = local(q + "q")
    others = [x for x in QA if x[0] != cat and x[0].split()[0] != cat.split()[0] and x[1].split()[0] != q.split()[0]]
    ds = rr.sample(others, 3)
    why = {d[1]: (f"{d[1]} は{CAT_MEAN[d[0]]}質問で、答えるなら「{d[2]}」のようになる。答え「{a}」とは対応しない。", "疑問詞の意味の取り違え") for d in ds}
    return mc(f"次の答えが返ってくる質問として、最も適切なものを選びなさい。\n― {a}", [q] + [d[1] for d in ds],
              f"答え「{a}」は{CAT_MEAN[cat]}質問への答えなので、{q}（{jq}）。", d=3,
              ap="答えの文が伝えている情報の種類（場所・時・数・人など）を見きわめ、それをたずねる疑問詞で始まる質問を選ぶ。",
              steps=[f"答え「{a}」が伝えている情報を確かめる。", f"その情報は{CAT_MEAN[cat]}質問への答えである。", f"{q} を選ぶ。"],
              alt=["選んだ質問と答えを続けて読み、主語や代名詞（you → I、your sister → she など）も対応しているかを確かめる。"],
              pc=[("答えの情報の種類を読み取っている", 2), ("適切な質問を選んでいる", 2)],
              pit=["答えの中の単語（at, in など）だけを見て、内容を確かめずに選ぶ。"], why=why)


OWN = [("私のもの", "It's mine.", "They're mine."), ("あなたのもの", "It's yours.", "They're yours."), ("彼のもの", "It's his.", "They're his."),
       ("彼女のもの", "It's hers.", "They're hers."), ("ケンのもの", "It's Ken's.", "They're Ken's."), ("私の姉のもの", "It's my sister's.", "They're my sister's."),
       ("私たちのもの", "It's ours.", "They're ours."), ("彼らのもの", "It's theirs.", "They're theirs.")]
OBJS = [("umbrella", "shoes"), ("racket", "glasses"), ("notebook", "pencils")]


@gen("standard_practice", 3, ["application", "concept"])
def answer_with_info(r):
    typ = r.choice(["whose", "whose", "which", "who"])
    if typ == "whose":
        info, a1, a2 = r.choice(OWN)
        sg, pl = r.choice(OBJS)
        if r.random() < 0.5:
            q, ans, v = f"Whose {sg} is this?", a1, [a1.replace("It's", "It is")]
        else:
            q, ans, v = f"Whose {pl} are these?", a2, [a2.replace("They're", "They are")]
        how = "持ち主を答えるので、所有代名詞（mine など）か「名前＋'s」を使う。this は it、these は they で受ける"
    elif typ == "which":
        a, b, ja, jb = r.choice([("tea", "coffee", "紅茶", "コーヒー"), ("summer", "winter", "夏", "冬"), ("math", "science", "数学", "理科"),
                                  ("cats", "dogs", "ねこ", "イヌ"), ("rice", "bread", "ごはん", "パン")])
        pick = r.choice([(a, ja), (b, jb)])
        q, info = f"Which do you like, {a} or {b}?", f"{pick[1]}が好き"
        ans, v = f"I like {pick[0]}.", [f"I like {pick[0]} better."]
        how = "Which は2つのうちのどちらかを選ばせる質問なので、選んだほうを I like ～. で答える"
    else:
        who, wj, kind = r.choice([("My father", "私の父", "does"), ("My mother", "私の母", "does"), ("My sister", "私の姉", "does"),
                                  ("My brother and I", "兄と私", "do"), ("My parents", "私の両親", "do")])
        act, aj = r.choice([("cooks dinner", "夕食を作る"), ("washes the dishes", "皿を洗う"), ("walks the dog", "イヌを散歩させる")])
        q, info = f"Who {act} in your family?", f"{wj}が{aj}"
        ans, v = f"{who} {kind}.", []
        how = f"Who が主語の質問には「主語＋does / do」で答える。{who} は{'3人称単数' if kind == 'does' else '複数'}なので {kind}"
    return sa(f"次の質問に、（　）内の内容で答える英文を書きなさい。\n{q}　（{info}）", ans, f"{how}。{ans}", d=2, v=v,
              ap="質問の疑問詞が何をたずねているかを確かめ、Yes / No を使わずに、その内容だけを答える文の型を選ぶ。",
              steps=[f"疑問詞を確認する：{q.split()[0]}。", how + "。", f"答え：{ans}"],
              alt=["答えの文を質問の後ろに続けて読み、主語・代名詞・動詞の形がそろっているかを確かめる。"],
              pc=[("答え方の型（所有代名詞・I like ～・主語＋does など）が正しい", 2), ("代名詞・動詞の形が正しい", 2)],
              pit=["Whose ～? に It's my. と答える（mine が正しい）。", "Who ～? に My father is. と答える（一般動詞の文なので does）。"])


# ======================================================================
# C 思考力・記述応用
# ======================================================================

SCENE = [  # (たずねたい内容, 疑問詞, 動詞句（原形）, 動詞句（3単現）, 理由の説明)
    ("毎朝何時に起きるか", "What time", "get up every morning", "gets up every morning", "時刻をたずねるので What time"),
    ("どこに住んでいるか", "Where", "live", "lives", "場所をたずねるので Where"),
    ("どうやって学校に来るか", "How", "come to school", "comes to school", "手段（方法）をたずねるので How"),
    ("朝食に何を食べるか", "What", "eat for breakfast", "eats for breakfast", "もの（何を）をたずねるので What"),
    ("いつピアノを練習するか", "When", "practice the piano", "practices the piano", "時をたずねるので When"),
    ("何のスポーツが好きか", "What sport", "like", "likes", "スポーツの種類をたずねるので What sport"),
    ("なぜ日本語を勉強しているのか", "Why", "study Japanese", "studies Japanese", "理由をたずねるので Why"),
]
TARGET = [("留学生のトムに、トム自身が", "you", "do"), ("留学生のトムに、トムのお姉さんが", "his sister", "does"), ("ALT のグリーン先生に、先生自身が", "you", "do"),
          ("友だちのアヤに、アヤのお父さんが", "her father", "does"), ("クラスメートのユキに、ケンとエミが", "Ken and Emi", "do")]


@gen("thinking_writing", 4, ["written_reasoning", "application"])
def write_question(r):
    what, wh, vp, vp3, wh_reason = r.choice(SCENE)
    who, subj, aux = r.choice(TARGET)
    ans = f"{wh} {aux} {subj} {vp}?"
    kind = {"you": "話し相手（2人称）", "his sister": "3人称単数", "her father": "3人称単数", "Ken and Emi": "複数"}[subj]
    model = (f"{ans}　{wh_reason} を文頭に置く。{vp.split()[0]} は一般動詞なので、疑問詞の後ろは Yes / No の疑問文と同じ「do / does＋主語＋動詞の原形」の語順にする。"
             f"主語 {subj} は{kind}なので {aux} を使い、動詞は原形 {vp.split()[0]} のままにする。")
    return desc(f"あなたは{who}{what}を英語でたずねたいと思っています。その質問を英語で1文で書きなさい。また、疑問詞の選び方と語順の組み立て方を、日本語で説明しなさい。",
                model, f"{wh_reason}。後ろは「{aux}＋{subj}＋{vp.split()[0]}」の語順。{('does の後ろの動詞は原形（' + vp3.split()[0] + ' ではない）') if aux == 'does' else ''}",
                [("正しい疑問詞を選んでいる", 2), ("語順（疑問詞＋do / does＋主語＋動詞の原形）が正しい", 3), ("疑問詞の選び方と語順を説明している", 3)], d=4, p=8, lines=6,
                ap="たずねたい内容から疑問詞を決め、その後ろを Yes / No の疑問文の語順にする。主語が3人称単数なら does。",
                steps=[f"たずねたい内容（{what}）から疑問詞を決める：{wh}。", f"主語を決める：{subj}（{kind}）→ {aux}。", f"語順を組み立てる：{ans}", "疑問詞の選び方と語順の理由を説明する。"],
                alt=[f"まず Yes / No の疑問文（{cap(aux)} {subj} {vp} ～?）を作ってから、たずねたい部分を {wh} にして文頭に置く方法でも確かめられる。"],
                pc=[("疑問詞", 2), ("語順", 3), ("説明", 3)],
                pit=["does を使ったのに動詞に s をつける。", "疑問詞の後ろに主語を置いてしまう（What time you get up?）。"])


@gen("thinking_writing", 3, ["cross_unit", "written_reasoning"], rel=["JH-ENG-G1-U02"])
def reverse_question(r):
    if r.random() < 0.65:
        sg, pl, m = r.choice(COUNT_N)
        num = r.choice(["two", "three", "four", "five"])
        S = r.choice([("I", "you", "do", "have"), ("My sister", "your sister", "does", "has"), ("We", "you", "do", "have")])
        b = f"{S[0]} {S[3]} {num} {pl}."
        ans = f"How many {pl} {S[2]} {S[1]} have?"
        model = (f"{ans}　答えが「{num}」という数なので、数をたずねる How many を使う。How many の後ろには数えられる名詞の複数形 {pl} を続け、"
                 f"「How many＋名詞」をひとまとまりで文頭に置く。後ろは一般動詞 have の疑問文の語順で「{S[2]}＋{S[1]}＋have」とする。")
        crit = "How many＋複数形の名詞をひとまとまりで文頭に置いている"
    else:
        info, a1, a2 = r.choice(OWN)
        sg, pl = r.choice(OBJS)
        plural = r.random() < 0.5
        b = a2 if plural else a1
        ans = f"Whose {pl} are these?" if plural else f"Whose {sg} is this?"
        model = (f"{ans}　答えが「{info}」と持ち主を伝えているので、持ち主をたずねる Whose を使う。答えの {'They' if plural else 'It'} から、"
                 f"たずねているものは{'複数（these）' if plural else '1つ（this）'}とわかるので、Whose {pl if plural else sg} {'are these' if plural else 'is this'}? とする。"
                 f"答えの {b.split()[-1].rstrip('.')} は「～のもの」を表す1語で、後ろに名詞は続かない。")
        crit = "Whose＋名詞と、this / these・be 動詞の数を正しくそろえている"
    return desc(f"次の対話の A の質問を、B の答えに合うように英語で書きなさい。また、疑問詞と名詞の形をそう決めた理由を説明しなさい。\nA: (　　　　　　　　　)\nB: {b}",
                model, "答えの情報（数・持ち主）から疑問詞を決め、名詞の数（単数・複数）を答えの文と合わせる。",
                [("正しい疑問詞を選んでいる", 2), (crit, 3), ("理由を説明している", 3)], d=4, p=8, lines=6,
                ap="B の答えが伝えている情報の種類と、名詞や代名詞が単数か複数かの両方に注目する。",
                steps=["B の答えが伝えている情報（数か持ち主か）を確かめる。", "疑問詞とその後ろの名詞の形（単数・複数）を決める。", f"語順を組み立てる：{ans}", "理由を説明する。"],
                alt=["書いた質問と B の答えを続けて読み、名詞の数（cats ↔ three、this ↔ It など）がそろっているかを確かめる。"],
                pc=[("疑問詞", 2), ("名詞の形と語順", 3), ("理由", 3)],
                pit=["How many の後ろを単数形にする。", "答えが They're ～. なのに Whose ～ is this? とする。"])


WHO_S = [("My father", "your father", "does"), ("My mother", "your mother", "does"), ("Aya", "Aya", "does"), ("Ken", "Ken", "does"),
         ("Tom and Emi", "Tom and Emi", "do"), ("My grandparents", "your grandparents", "do")]
WHO_V = [("cooks", "cook", "dinner on Sundays"), ("plays", "play", "the piano in your family"), ("washes", "wash", "the dishes after dinner"),
         ("walks", "walk", "the dog every morning"), ("teaches", "teach", "English at your school")]


@gen("thinking_writing", 3, ["cross_unit", "written_reasoning"], rel=["JH-ENG-G1-U01"])
def who_subject(r):
    S, sq, aux = r.choice(WHO_S)
    v3, v, rest = r.choice(WHO_V)
    verb = v3 if aux == "does" else v
    rest_src = rest.replace("in your family", "in my family").replace("at your school", "at my school")
    src = f"[[u:{S}]] {verb} {rest_src}."
    q = f"Who {v3} {rest}?"
    a = f"{S} {aux}."
    model = (f"{q}　― {a}　下線部は文の主語なので、主語を Who にかえるだけでよく、do / does は使わない（ふつうの文と同じ語順）。"
             f"Who は3人称単数としてあつかうので、動詞は {v3} にする。答えは「主語＋do / does」の形で、{S} は{'3人称単数' if aux == 'does' else '複数'}なので {aux} を使う。")
    return desc(f"次の英文の下線部をたずねる疑問文を書き、その疑問文に答える文も書きなさい。また、この疑問文の語順が、Where do you live? のような疑問文と違う理由を説明しなさい。\n{src}",
                model, "主語をたずねる Who は、それ自体が主語になるので「Who＋動詞（3単現）～?」の語順になる。",
                [("正しい疑問文を書いている", 3), ("正しい答えの文を書いている", 2), ("語順が違う理由（Who が主語であること）を説明している", 3)], d=4, p=8, lines=6,
                ap="下線部が文の主語か、主語以外かを確かめる。主語なら、その位置に Who を入れるだけでよい。",
                steps=["下線部が主語であることを確かめる。", f"主語を Who にかえる：{q}", f"答えの文を「主語＋do / does」で作る：{a}", "Where do you live? との違い（主語以外をたずねると do / does が必要）を説明する。"],
                alt=[f"Who を答えの {S} にもどすと「{S} {verb} {rest_src}.」というふつうの文になることから、語順がふつうの文と同じだと確かめられる。"],
                pc=[("疑問文", 3), ("答えの文", 2), ("理由", 3)],
                pit=["Who does cook ～? のように do / does を入れる。", f"答えを {S} is. のように be 動詞で答える。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(task, wrong, where, etype, tempt, fix, rule, ap, alt, pit):
    return desc(f"{task}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しく書き直しなさい。", fix,
                f"「{where}」の部分が誤り。{rule}。正しくは {fix}",
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しく書き直している", 3), ("規則を説明している", 1)], d=3, p=6, lines=5,
                ap=ap, steps=["疑問詞が何をたずねているか、後ろの語順が正しいかを確かめる。", f"誤り「{where}」を見つける：{rule}。", f"正しく直す：{fix}"],
                alt=alt, pc=[("誤りの指摘", 2), ("正しい英文", 3), ("規則の説明", 1)], pit=pit,
                err=dict(sol=wrong, step=f"「{where}」の部分", type=etype, tempt=tempt, fix=fix))


@gen("error_correction", 5, ["common_error", "condition_check"])
def err_wh_order(r):
    kind = r.choice(["no_aux", "aux_s", "be_gv", "be_order", "many_sg", "much_count", "do_3s"])
    S = r.choice([s for s in WH_SUBJ])
    if kind in ("aux_s", "do_3s"):
        S = r.choice([s for s in WH_SUBJ if s[1] == "3s"])
    wh, rest, jt = r.choice(WH_GV)
    J = f"{S[2]}{jt}。"
    aux = "does" if S[1] == "3s" else "do"
    fix = f"{wh} {aux} {S[0]} {rest}?"
    v0 = rest.split()[0]
    v3 = {"go": "goes", "do": "does", "study": "studies", "practice": "practices"}.get(v0, v0 + "s")
    rest3 = " ".join([v3] + rest.split()[1:])
    if kind == "no_aux":
        wrong = f"{wh} {S[0]} {rest3 if S[1] == '3s' else rest}?"
        return err_item(f"次の日本語を英語に直しなさい。\n{J}", wrong, f"{wh} {S[0]}", "logic", "ふつうの文の前に疑問詞を置けば疑問文になると考え、do / does を入れなかった。",
                        fix, f"疑問詞の後ろは疑問文の語順にする。一般動詞の文なので {aux} を主語の前に置き、動詞は原形にする",
                        "疑問詞の後ろは「Yes / No の疑問文」と同じ語順になる。", ["疑問詞を取り除いて Yes / No の疑問文として正しいかを確かめる。"],
                        ["疑問詞の後ろの do / does を落とす。"])
    if kind == "aux_s":
        wrong = f"{wh} does {S[0]} {rest3}?"
        return err_item(f"次の日本語を英語に直しなさい。\n{J}", wrong, v3, "concept", "主語が3人称単数なので、動詞にも s が必要だと考えた。",
                        fix, f"does が3単現の s を引き受けるので、動詞は原形 {v0} にする",
                        "do / does を使った疑問文では、動詞はいつも原形にする。", ["does と動詞の両方に s がついていないかを確かめる。"],
                        ["does と動詞の s を二重につける。"])
    if kind == "do_3s":
        wrong = f"{wh} do {S[0]} {rest}?"
        return err_item(f"次の日本語を英語に直しなさい。\n{J}", wrong, "do", "condition", "「疑問文は do で始める」とだけ覚えていて、主語による使い分けを確かめなかった。",
                        fix, f"主語 {S[0]} は3人称単数なので do ではなく does を使う",
                        "疑問詞の後ろの do / does は、主語が3人称単数かどうかで決まる。", ["主語を he / she に置きかえて、does になるかを確かめる。"],
                        ["主語が3人称単数なのに do を使う。"])
    if kind == "be_gv":
        bev = "is" if S[1] == "3s" else "are"
        wrong = f"{wh} {bev} {S[0]} {rest}?"
        return err_item(f"次の日本語を英語に直しなさい。\n{J}", wrong, bev, "concept", "「～ですか」という日本語につられて、be 動詞で疑問文を作った。",
                        fix, f"{v0} は一般動詞なので be 動詞ではなく {aux} を使う",
                        "疑問詞の後ろに be 動詞を使うか do / does を使うかは、文の中に一般動詞があるかで決まる。", ["be 動詞と一般動詞が同じ文に並んでいないかを確かめる。"],
                        ["一般動詞の文に be 動詞を使う。"])
    if kind == "be_order":
        w, f, jj = r.choice([("How old you are?", "How old are you?", "あなたは何歳ですか。"), ("Where Ken is now?", "Where is Ken now?", "ケンは今どこにいますか。"),
                             ("When your birthday is?", "When is your birthday?", "あなたの誕生日はいつですか。"), ("Who that girl is?", "Who is that girl?", "あの女の子はだれですか。"),
                             ("How much this bag is?", "How much is this bag?", "このかばんはいくらですか。"), ("What color your car is?", "What color is your car?", "あなたの車は何色ですか。")])
        return err_item(f"次の日本語を英語に直しなさい。\n{jj}", w, w.split()[-1].rstrip("?"), "logic", "ふつうの文の語順のまま、前に疑問詞を置いた。",
                        f, "be 動詞の文の疑問文なので、疑問詞の後ろは「be 動詞＋主語」の語順にする",
                        "疑問詞の後ろは疑問文の語順。be 動詞の文なら be 動詞を主語の前に出す。", ["疑問詞を取り除いた部分が Is ～? / Are ～? の形になっているかを確かめる。"],
                        ["be 動詞を文末に残す。"])
    if kind == "many_sg":
        sg, pl, m = r.choice(COUNT_N)
        w, f = f"How many {sg} do you have?", f"How many {pl} do you have?"
        return err_item(f"次の日本語を英語に直しなさい。\nあなたは{m}をいくつ持っていますか。", w, f"How many {sg}", "condition", "日本語の「いくつ」には名詞の形の変化がないので、単数形のままにした。",
                        f, f"How many の後ろの数えられる名詞は複数形にするので {pl}",
                        "How many は「いくつ」と数をたずねるので、後ろの名詞は複数形になる。", ["答えの文（I have three ～s.）を考えると、複数形が必要なことがわかる。"],
                        ["How many の後ろを単数形にする。"])
    if kind == "much_count":
        sg, pl, m = r.choice(COUNT_N)
        w, f = f"How much {pl} do you have?", f"How many {pl} do you have?"
        return err_item(f"次の日本語を英語に直しなさい。\nあなたは{m}をいくつ持っていますか。", w, "How much", "concept", "「どれくらい」という意味から、数をたずねるときにも How much を使った。",
                        f, "数えられる名詞の数をたずねるときは How many を使う。How much は値段（や数えられないものの量）をたずねる",
                        "How many は数、How much は値段をたずねる。", ["答えが「3つ」なのか「300円」なのかを考えて、どちらの質問かを確かめる。"],
                        ["How many と How much を取り違える。"])
    return None


ANS_ERR = [
    ("Whose racket is this?", "It's my.", "It's mine.", "my", "concept", "「～のもの」は所有代名詞 mine。my は後ろに名詞が必要", "my と mine の区別があいまいだった。"),
    ("Whose bag is this?", "It's Ken.", "It's Ken's.", "Ken", "concept", "持ち主を答えるので「名前＋'s」で「ケンのもの」とする", "人の名前を答えればよいと考え、's をつけ忘れた。"),
    ("Whose shoes are these?", "It's hers.", "They're hers.", "It's", "condition", "these（複数）でたずねているので、They're で答える", "Whose ～? の答えはいつも It's ～. だと思い込んだ。"),
    ("How do you go to school?", "By a bus.", "By bus.", "a bus", "notation", "交通手段を表す by の後ろの名詞には a / the をつけない", "名詞の前には a をつけるものだと考えた。"),
    ("How does your father go to work?", "He goes by the car.", "He goes by car.", "the car", "notation", "交通手段を表す by の後ろの名詞には a / the をつけない", "名詞の前には a / the をつけるものだと考えた。"),
    ("Who cooks dinner in your family?", "My father is.", "My father does.", "is", "concept", "cooks は一般動詞なので、答えは be 動詞ではなく does で受ける", "答えの短い文はいつも be 動詞で作れると考えた。"),
    ("Who plays the piano in your family?", "My sisters does.", "My sisters do.", "does", "condition", "主語 My sisters は複数なので does ではなく do", "質問の plays に合わせて、答えも3人称単数の形にした。"),
    ("Which do you like, tea or coffee?", "Yes, I like tea.", "I like tea.", "Yes", "interpretation", "Which の疑問文は2つから選ばせる質問なので、Yes / No を使わずに選んだほうを答える", "Do you like ～? と同じように Yes / No で答え始めた。"),
    ("How many brothers do you have?", "I have two brother.", "I have two brothers.", "two brother", "condition", "two の後ろの数えられる名詞は複数形にするので brothers", "質問の中の名詞の形を確かめず、単数形で書いた。"),
    ("How old is your brother?", "He's fifteen years.", "He's fifteen.", "fifteen years", "notation", "年齢は数だけで答えるか、years old まで言う（He's fifteen years old.）", "years だけで年齢を表せると考えた。"),
]


@gen("error_correction", 5, ["common_error", "computation"])
def err_wh_answer(r):
    if r.random() < 0.45:
        cat, q, a, yn, jq, ex = r.choice(QA)
        return err_item(f"次の質問に英語で答えなさい。\n{q}", yn, yn.split(",")[0], "interpretation",
                        "Do you ～? / Is ～? の質問と同じように、Yes / No で答え始めてしまった。", f"（解答例）{a}",
                        f"{cat} で始まる疑問文は{CAT_MEAN[cat]}質問なので、Yes / No ではなく内容を答える",
                        "疑問詞で始まる質問には、Yes / No ではなく、たずねられた内容（場所・時・数など）を答える。",
                        ["答えの文を質問の後ろに続けて読み、たずねられた内容に答えているかを確かめる。"],
                        ["疑問詞の質問に Yes / No で答える。"])
    q, w, f, where, et, rule, tempt = r.choice(ANS_ERR)
    if where == "fifteen years":
        f = "He's fifteen. または He's fifteen years old."
    return err_item(f"次の質問に対する答えとして正しい英文を書きなさい。\n{q}", w, where, et, tempt, f, rule,
                    "答えの文は、質問の疑問詞（何をたずねているか）と、主語・名詞の数・動詞の種類に合わせて作る。",
                    ["答えの文を完全な文にのばしてみて（例：It's mine. ← It's my racket.）、形が正しいかを確かめる。"],
                    ["所有代名詞・名詞の数・do / does の使い分けを確かめない。"])


GENERATORS = [choose_wh, choose_answer, how_phrase, aux_in_wh,
              make_wh, count_question, build_order, choose_question, answer_with_info,
              write_question, reverse_question, who_subject,
              err_wh_order, err_wh_answer]
