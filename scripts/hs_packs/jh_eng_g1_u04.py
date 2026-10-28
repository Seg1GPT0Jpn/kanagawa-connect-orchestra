"""単元パック：中学1年 英語 現在進行形・助動詞 can・命令文・Let's。"""
import random

from banks._common import desc, mc, order, sa
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem,
                         tp)

UNIT_ID = "JH-ENG-G1-U04"

PREREQUISITES = [
    ("JH-ENG-G1-U01", "be 動詞（am / are / is）を主語で使い分けられること、一般動詞の現在形と三人称単数現在の s、否定文・疑問文の作り方。"),
    ("JH-ENG-G1-U02", "主語になる代名詞（I / you / he / she / we / they）と、主語に合わせて be 動詞を選べること。"),
    ("JH-ENG-G1-U03", "what などの疑問詞を文の先頭に置く疑問文の語順（What are you doing? で使う）。"),
]
EXTENSIONS = [
    ("JH-ENG-G1-U05", "be 動詞を過去形（was / were）にすると過去進行形になり、「そのとき～していた」を表せる。"),
    ("JH-ENG-G2-U01", "will も can と同じ助動詞で、後ろに動詞の原形を置く。助動詞の文の作り方がそのまま使える。"),
    ("JH-ENG-G2-U03", "must / should など、ほかの助動詞と have to に広がる。Don't ～. と You must not ～. の比較にもつながる。"),
    ("HS-ENG-U03", "高校では can の「推量（～はありうる）」や can't「～のはずがない」など、助動詞の意味をさらに広げて学ぶ。"),
]

# 主語：(英語, be 動詞, 日本語, 代名詞)
SUBJ = [("I", "am", "私", "I"), ("You", "are", "あなた", "you"), ("He", "is", "彼", "he"), ("She", "is", "彼女", "she"),
        ("We", "are", "私たち", "we"), ("They", "are", "彼ら", "they"), ("Ken", "is", "ケン", "he"),
        ("My sister", "is", "私の姉", "she"), ("Yumi and Aya", "are", "ユミとアヤ", "they"), ("My parents", "are", "私の両親", "they"),
        ("Mr. Sato", "is", "佐藤先生", "he"), ("Tom", "is", "トム", "he")]
THIRD = [s for s in SUBJ if s[1] == "is"]
PLURAL = [s for s in SUBJ if s[1] == "are" and s[0] not in ("You", "We")]

# 動作：(原形, ing 形, 三単現, 目的語など, 日本語の目的語部分, て形, 辞書形)
ACT = [
    ("play", "playing", "plays", "tennis", "テニスを", "して", "する"),
    ("read", "reading", "reads", "a book", "本を", "読んで", "読む"),
    ("watch", "watching", "watches", "TV", "テレビを", "見て", "見る"),
    ("study", "studying", "studies", "English", "英語を", "勉強して", "勉強する"),
    ("make", "making", "makes", "a cake", "ケーキを", "作って", "作る"),
    ("write", "writing", "writes", "a letter", "手紙を", "書いて", "書く"),
    ("swim", "swimming", "swims", "in the pool", "プールで", "泳いで", "泳ぐ"),
    ("run", "running", "runs", "in the park", "公園で", "走って", "走る"),
    ("cook", "cooking", "cooks", "dinner", "夕食を", "作って", "作る"),
    ("use", "using", "uses", "a computer", "コンピューターを", "使って", "使う"),
    ("wash", "washing", "washes", "the dishes", "皿を", "洗って", "洗う"),
    ("sing", "singing", "sings", "a song", "歌を", "歌って", "歌う"),
    ("clean", "cleaning", "cleans", "the room", "部屋を", "掃除して", "掃除する"),
    ("draw", "drawing", "draws", "a picture", "絵を", "かいて", "かく"),
    ("listen", "listening", "listens", "to music", "音楽を", "聞いて", "聞く"),
    ("dance", "dancing", "dances", "on the stage", "ステージで", "踊って", "踊る"),
    ("sit", "sitting", "sits", "on the bench", "ベンチに", "座って", "座る"),
    ("practice", "practicing", "practices", "the piano", "ピアノを", "練習して", "練習する"),
    ("ride", "riding", "rides", "a bike", "自転車に", "乗って", "乗る"),
    ("eat", "eating", "eats", "lunch", "昼食を", "食べて", "食べる"),
]

# can と使う動作：(原形, 三単現, 目的語など, 日本語「～ことができる」の前の部分)
CAN_ACT = [
    ("play", "plays", "the guitar", "ギターをひく"), ("swim", "swims", "fast", "速く泳ぐ"),
    ("speak", "speaks", "English", "英語を話す"), ("cook", "cooks", "curry", "カレーを作る"),
    ("ride", "rides", "a unicycle", "一輪車に乗る"), ("read", "reads", "Chinese", "中国語を読む"),
    ("make", "makes", "sushi", "すしを作る"), ("run", "runs", "very fast", "とても速く走る"),
    ("sing", "sings", "English songs", "英語の歌を歌う"), ("use", "uses", "this computer", "このコンピューターを使う"),
    ("jump", "jumps", "high", "高く跳ぶ"), ("write", "writes", "kanji well", "漢字を上手に書く"),
    ("draw", "draws", "pictures well", "絵を上手にかく"), ("dance", "dances", "very well", "とても上手に踊る"),
]

ING_RULE = {
    "plain": "そのまま ing をつける",
    "e": "語尾の e をとって ing をつける",
    "double": "「短母音＋子音字」で終わるので、最後の子音字を重ねて ing をつける",
    "ie": "語尾の ie を y にかえて ing をつける",
}
ING = [
    ("play", "playing", "plain"), ("read", "reading", "plain"), ("watch", "watching", "plain"), ("study", "studying", "plain"),
    ("cook", "cooking", "plain"), ("sing", "singing", "plain"), ("walk", "walking", "plain"), ("eat", "eating", "plain"),
    ("listen", "listening", "plain"), ("clean", "cleaning", "plain"), ("visit", "visiting", "plain"), ("teach", "teaching", "plain"),
    ("speak", "speaking", "plain"), ("sleep", "sleeping", "plain"), ("help", "helping", "plain"), ("enjoy", "enjoying", "plain"),
    ("make", "making", "e"), ("write", "writing", "e"), ("use", "using", "e"), ("dance", "dancing", "e"), ("ride", "riding", "e"),
    ("come", "coming", "e"), ("take", "taking", "e"), ("have", "having", "e"), ("practice", "practicing", "e"), ("drive", "driving", "e"),
    ("close", "closing", "e"), ("give", "giving", "e"),
    ("run", "running", "double"), ("swim", "swimming", "double"), ("sit", "sitting", "double"), ("get", "getting", "double"),
    ("cut", "cutting", "double"), ("put", "putting", "double"), ("begin", "beginning", "double"), ("stop", "stopping", "double"),
    ("shop", "shopping", "double"), ("plan", "planning", "double"),
    ("lie", "lying", "ie"), ("tie", "tying", "ie"),
]
ING_BY = {k: [x for x in ING if x[2] == k] for k in ING_RULE}


def cap(s):
    return s[0].upper() + s[1:]


def mid(s):
    """文中に置くときの主語（代名詞と My ～ は小文字に、I・人名はそのまま）。"""
    if s.split()[0] in ("You", "He", "She", "We", "They", "My", "Our", "Your"):
        return s[0].lower() + s[1:]
    return s


def local(key):
    return random.Random(key)


# ======================================================================
# 授業プリント
# ======================================================================

LESSON = lesson(
    goals=["「今～しているところ」を、be 動詞（am / are / is）＋動詞の ing 形で表し、否定文・疑問文も作れる。",
           "助動詞 can を使って「～できる」「～してもよい」「～してくれますか」を表し、can の後ろは必ず動詞の原形にできる。",
           "命令文（～しなさい／～してはいけない）と Let's ～.（～しよう）を場面に合わせて使い分けられる。"],
    duration=50,
    readiness=["be 動詞 am / are / is を主語に合わせて選べる（中1）。", "一般動詞の現在形と三人称単数現在の s（plays, watches）を使える（中1）。",
               "小学校の外国語で、Let's play soccer. や I can swim. などの表現を聞いたり話したりした経験がある。",
               "小学校の国語で、「～している」「～できる」「～しなさい」など文末の言い方で意味が変わることを学んでいる。"],
    flow=[("導入：今まさにしていること", 5, "教師が黒板に字を書きながら What am I doing? と問いかけ、I'm writing. を引き出す"),
          ("現在進行形の形と ing のつけ方", 13, "be＋ing の形、ing のつけ方4パターン、否定文・疑問文（例題1）"),
          ("助動詞 can", 12, "can＋原形、否定 can't、疑問 Can ～?、依頼・許可の Can you ～? / Can I ～?（例題2）"),
          ("命令文と Let's", 12, "動詞の原形で始める、Be ～.、Don't ～.、Please、Let's ～. と答え方（例題3）"),
          ("まとめと確認", 8, "4つの形の「動詞の形」を表で比べ、確認問題3問")],
    sections=[
        intro("in1", "「動詞の形」で伝わる意味が変わる",
              "これまでに学んだ現在形（I play tennis.）は「ふだんテニスをする」という習慣を表しました。この単元では、動詞の前に be 動詞や can を置いたり、主語を省いたりすることで、「今～している」「～できる」「～しなさい」「～しよう」という新しい意味を表す方法を学びます。どの形でも、動詞がどんな形（原形・ing 形）になるのかに注目しましょう。",
              bullets=["I play tennis.（ふだんテニスをする）", "I am playing tennis now.（今テニスをしている）",
                       "I can play tennis.（テニスができる）", "Play tennis.（テニスをしなさい）／Let's play tennis.（テニスをしよう）"],
              points=[tp("4つの文を並べて板書し、日本語の意味の違いを生徒に言わせてから、英語ではどこが変わったかを探させる。",
                         ask="play の前やあとで何が変わっているか。", expect="am がついて playing になった、can がついた、主語がなくなった、Let's がついた。",
                         timing="導入の冒頭")]),
        definition("df1", "現在進行形：be 動詞＋動詞の ing 形",
                   "「今～しているところだ」と、話している時点で進行中の動作を表すときは、〈am / are / is＋動詞の ing 形〉を使います。be 動詞は主語に合わせて選びます。",
                   formula="主語＋am / are / is＋動詞の ing 形 ～.",
                   bullets=["否定文：be 動詞の後ろに not（He is not reading. → He isn't reading.）", "疑問文：be 動詞を主語の前に出す（Is he reading? ― Yes, he is. / No, he isn't.）",
                            "疑問詞：What are you doing? ― I'm making a cake.",
                            "ing のつけ方：①そのまま（play → playing）②e をとる（make → making）③子音字を重ねる（run → running）④ie → y（lie → lying）"],
                   conditions=["know（知っている）、like（好きだ）、want（ほしい）、have（持っている）など「状態」を表す動詞はふつう進行形にしない。",
                               "have が「食べる」の意味のときは進行形にできる（I'm having lunch.）。"],
                   points=[tp("be 動詞と ing 形は「2つでセット」であることを強調し、どちらか一方を落とす誤りに注意させる。",
                              caution="I playing ～. や I am play ～. が最も多い誤り。"),
                           tp("ing のつけ方は、4つのグループに分けてカードで分類させると定着しやすい。", timing="定義の説明後")]),
        definition("df2", "助動詞 can：can＋動詞の原形",
                   "can は動詞の前に置いて「～できる」という意味を加える助動詞です。主語が何であっても can の形は変わらず、後ろの動詞はいつも原形にします。",
                   formula="主語＋can＋動詞の原形 ～.",
                   bullets=["否定文：can't（cannot）＋原形（She can't swim.）", "疑問文：Can を主語の前に出す（Can she swim? ― Yes, she can. / No, she can't.）",
                            "Can you ～?：「～してくれますか」という依頼にもなる（Can you help me? ― Sure.）",
                            "Can I ～?：「～してもいいですか」という許可を求める表現（Can I use this pen? ― Sure.）"],
                   conditions=["can の後ろに to はつけない（× can to swim）。", "主語が三人称単数でも cans や can swims にはしない。",
                               "否定文・疑問文で do / does は使わない（× Do you can ～? / × He doesn't can ～.）。"],
                   points=[tp("三人称単数の s がつかない理由を「s は can が引き受けているわけではなく、助動詞の後ろはいつも原形」と言葉で整理させる。",
                              ask="He plays tennis. を can の文にするとどうなるか。", expect="He can play tennis.（plays の s が消える）")]),
        theorem("th1", "命令文と Let's ～.",
                "命令文：動詞の原形 ～.／Be＋形容詞 ～.／Don't＋動詞の原形 ～.／Let's＋動詞の原形 ～.",
                ["命令文は主語の you を省き、動詞の原形で文を始める（Open the window.）。",
                 "be 動詞の命令文は原形の Be で始める（Be quiet.）。am / are / is では始めない。",
                 "「～してはいけない」は Don't を文頭に置く（Don't run here.）。be 動詞でも Don't be ～.（Don't be late.）。",
                 "Please を文頭か文末（カンマのあと）に置くと、ていねいな言い方になる。",
                 "Let's ～.（～しよう）への答え方は Yes, let's. / No, let's not. など。"],
                body="命令文も can の文も、動詞はいつも原形です。この単元で動詞の形が変わるのは現在進行形（ing 形）だけ、と整理すると覚えやすくなります。",
                points=[tp("Be quiet. のように be 動詞の原形が文頭に来ることに驚く生徒が多い。「命令文は原形で始める」という規則から Be になることを確認させる。",
                           ask="You are quiet. を「静かにしなさい」という命令文にすると？", expect="Be quiet.")]),
        derivation("dv1", "文の作り方（なぜその形になるのか）",
                   ["① ふつうの文 He plays tennis. から始める（現在形：ふだんの習慣）。",
                    "② 「今している」を表すには、進行中であることを示す be 動詞 is を置き、動詞を ing 形にする：He is playing tennis now.",
                    "③ 否定文・疑問文は be 動詞の文と同じルールで作る：He isn't playing tennis. ／ Is he playing tennis?",
                    "④ 「できる」を表すには can を動詞の前に置く。助動詞の後ろは原形なので plays → play：He can play tennis.",
                    "⑤ can の否定文・疑問文は can 自身を使う（do / does は不要）：He can't play tennis. ／ Can he play tennis?",
                    "⑥ 相手に直接「～しなさい」と言うときは主語 You を省き、原形で始める：Play tennis.　「～しよう」は Let's を前に置く：Let's play tennis."],
                   body="be 動詞の文・can の文は「be 動詞や can を動かす・not をつける」、一般動詞の文は「do / does を使う」。どちらのルールを使うかは、文の中に be 動詞や can があるかどうかで決まります。",
                   points=[tp("①～⑥を1つの文から順に変形していく様子を板書で示し、どこで動詞の形が変わるかを色で示す。",
                              ask="③で does を使わないのはなぜか。", expect="文の中に be 動詞 is があるから。", timing="導出の説明時")]),
        example("ex1", "例題1　現在進行形の文を作る",
                "次の英文を、（　）内の指示に従って書きかえなさい。(1) My brother washes the dishes.（文末に now を加えて現在進行形に）　(2) They are swimming in the river.（疑問文にして、Yes で答える）",
                ["(1) 主語 My brother は三人称単数なので be 動詞は is。", "(1) washes の s をとって原形 wash にもどしてから ing をつける：washing。",
                 "(2) be 動詞 are を主語の前に出す：Are they swimming in the river?", "(2) 答えは主語を代名詞にして be 動詞で答える：Yes, they are."],
                "(1) My brother is washing the dishes now.　(2) Are they swimming in the river? ― Yes, they are.",
                thinking="進行形にするときは「be 動詞を主語で選ぶ」「動詞を原形にもどしてから ing」の2点を確かめる。",
                points=[tp("washes にそのまま ing をつけて washesing とする誤りを予想させ、「三単現の s と ing は同時につかない」ことを確認する。")],
                misconceptions=[("My brother is washesing the dishes now.", "ing は原形 wash につける。washing。"),
                                ("Do they swimming in the river?", "be 動詞の文なので Are を主語の前に出す。")]),
        example("ex2", "例題2　can の文を作る",
                "日本語に合う英文を書きなさい。(1) 私の姉は一輪車に乗ることができます。　(2) この辞書を使ってもいいですか。",
                ["(1) 主語は My sister。「乗ることができる」は can＋原形 ride。", "(1) 三人称単数でも can の後ろは原形のまま：My sister can ride a unicycle.",
                 "(2) 「～してもいいですか」は Can I ～? で表す。", "(2) Can I use this dictionary?"],
                "(1) My sister can ride a unicycle.　(2) Can I use this dictionary?",
                thinking="主語が三人称単数でも can の後ろは原形。「～してもいいですか」は自分（I）の動作の許可を求める文になる。",
                points=[tp("(2) を Can you use ～? と書く生徒に、「使うのはだれか」を問い返して主語を考えさせる。",
                           ask="辞書を使いたいのはだれか。", expect="自分なので I。")]),
        example("ex3", "例題3　命令文と Let's",
                "場面に合う英文を書きなさい。(1) 図書館で大声で話している友だちに「ここでは静かにして」と言う。　(2) 放課後、友だちを「いっしょに体育館でバスケットボールをしよう」と誘う。",
                ["(1) 「静かな」は形容詞 quiet なので、be 動詞の命令文 Be quiet. を使う。場所 here を加える。",
                 "(2) 相手を誘うので Let's＋動詞の原形。play basketball in the gym。"],
                "(1) Be quiet here, please.（Please be quiet here. も可）　(2) Let's play basketball in the gym (after school).",
                thinking="命令文は「何をしてほしいか」を動詞の原形で始める。形容詞を使うときは Be を補う。",
                points=[tp("(1) を Quiet here. や Don't noisy. とする誤りを取り上げ、形容詞だけでは命令文にならないことを確認する。")],
                misconceptions=[("Don't noisy here.", "noisy は形容詞なので be が必要。Don't be noisy here."),
                                ("Let's playing basketball.", "Let's の後ろは原形。Let's play basketball.")]),
        board("bd1", "板書案",
              [("① 現在進行形", ["am / are / is ＋ ing", "He is playing tennis now.", "否定：isn't playing", "疑問：Is he playing ～?", "ing：play→playing", "make→making / run→running", "lie→lying"]),
               ("② can", ["can ＋ 原形（s なし）", "He can play tennis.", "否定：can't play", "疑問：Can he play ～?", "Can you ～?（依頼）", "Can I ～?（許可）"]),
               ("③ 命令文・Let's", ["原形で始める：Open the door.", "Be quiet.（形容詞は Be）", "Don't run here.", "Please ～. / ～, please.", "Let's play.", "― Yes, let's. / No, let's not."])],
              points=[tp("3列の最後に「動詞の形」を赤で囲み、ing 形になるのは①だけ、②③は原形であることを一目でわかるようにする。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("現在進行形の導入では、実際に動作をしながら What am I doing? と問いかけ、「今」の感覚をつかませる。", timing="導入"),
               tp("ing のつけ方の「子音字を重ねる」は、run, swim, sit, get, stop など中1でよく使う語に限って練習させる。",
                  caution="visit → visitting のような誤りは、無理に規則を説明せず「そのままつける語」として覚えさせる。"),
               tp("can の疑問文に Yes で答えるとき、Yes, I can. の can を省けないことを口頭練習で確認する。", ask="Can you swim? に「はい」と答えると？", expect="Yes, I can."),
               tp("命令文は強い言い方にもなるので、Please をつけたり、Can you ～? を使ったりするとていねいになることを場面練習で体験させる。"),
               tp("問題プリント D の誤答例は、「be 動詞と do / does の混同」「can の後ろの s」「Let's の後ろの ing」の3種類にまとめて振り返らせる。")],
              misconceptions=[("I am play tennis now.", "進行形は be 動詞＋ing 形。I am playing tennis now."),
                              ("She can plays the piano.", "can の後ろは原形。She can play the piano."),
                              ("Don't noisy.", "形容詞の命令文には be が必要。Don't be noisy."),
                              ("I'm knowing the answer.", "know は状態を表す動詞で進行形にしない。I know the answer.")]),
        summary("sm1", "まとめ",
                ["現在進行形 ＝ am / are / is＋ing 形。「今～しているところ」。否定・疑問は be 動詞の文のルール。",
                 "can＋動詞の原形。主語が何でも形は同じ。否定は can't、疑問は Can を前に。依頼 Can you ～?、許可 Can I ～?",
                 "命令文は原形で始める（形容詞なら Be ～.）。禁止は Don't ～.、誘いは Let's ～.（Yes, let's. / No, let's not.）"]),
        check("ck1", "確認問題",
              [("swim と make を ing 形にしなさい。", "swimming, making"),
               ("Tom can (swim / swims) fast. の（　）から正しい語を選びなさい。", "swim（can の後ろは原形）"),
               ("「遅れてはいけません」を英語で書きなさい（late を使う）。", "Don't be late.")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

@gen("basic_check", 4, ["computation", "common_error"])
def ing_spelling(r):
    k1, k2 = r.sample(list(ING_RULE), 2)
    a, b = r.choice(ING_BY[k1]), r.choice(ING_BY[k2])
    return sa(f"次の2つの動詞を、現在進行形で使う ing 形にしなさい。\n(1) {a[0]}　(2) {b[0]}", f"(1) {a[1]}　(2) {b[1]}",
              f"(1) {a[0]} は{ING_RULE[k1]}：{a[1]}。(2) {b[0]} は{ING_RULE[k2]}：{b[1]}。", d=1,
              v=[f"{a[1]}, {b[1]}", f"{a[1]} {b[1]}", f"(1){a[1]} (2){b[1]}"],
              ap="動詞の語尾を見て、①そのまま ②e をとる ③子音字を重ねる ④ie を y にかえる、のどのグループかを先に決める。",
              steps=[f"{a[0]} の語尾を確認する → {ING_RULE[k1]}。", f"{b[0]} の語尾を確認する → {ING_RULE[k2]}。", f"答え：{a[1]}、{b[1]}"],
              alt=["書いた ing 形を声に出して読み、もとの動詞の発音（母音の長さ）が変わっていないかを確かめる。"],
              pc=[("(1) を正しく書いている", 1), ("(2) を正しく書いている", 1)],
              pit=["e で終わる語にそのまま ing をつける（makeing）。", "子音字を重ねる語を重ねずに書く（runing, swiming）。"])


@gen("basic_check", 4, ["computation", "condition_check"])
def prog_be(r):
    s, be, sj, _ = r.choice(SUBJ)
    v, ing, v3, obj, jo, jte, _ = r.choice(ACT)
    other_be = {"am": "is", "is": "are", "are": "is"}[be]
    if s in ("I", "We", "You"):
        sent = f"{s} (　　) {obj} now."
    else:
        sent = f"{r.choice(['Look!', 'Look!', 'Oh,'])} {s} (　　) {obj} now." if r.random() < 0.5 else f"{s} (　　) {obj} now."
    jp = f"{sj}は今、{jo}{jte}います。"
    why = {f"{other_be} {ing}": (f"主語 {s} に合う be 動詞は {be}。{other_be} は主語に合わない。", "主語と be 動詞の対応"),
           f"{be} {v}": ("be 動詞の後ろの動詞は ing 形にしないと進行形にならない。原形をそのまま置くことはできない。", "進行形の形（be＋ing）"),
           ing: ("ing 形だけでは文の動詞にならない。進行形には be 動詞が必要。", "進行形の形（be＋ing）")}
    return mc(f"日本語に合うように、（　）に入る最も適切なものを選びなさい。\n{jp}\n{sent}", [f"{be} {ing}"] + list(why),
              f"「今～している」は be 動詞＋ing 形。主語 {s} に合う be 動詞は {be} なので {be} {ing}。", d=1,
              ap="①主語を見て be 動詞（am / are / is）を決める、②動詞が ing 形になっているかを確かめる、の2段階で選ぶ。",
              steps=[f"主語は {s} → be 動詞は {be}。", f"「今～している」なので {v} を ing 形 {ing} にする。", f"答え：{be} {ing}"],
              alt=[f"選んだ形で否定文（{s} {be} not {ing} ～.）を作ってみて、形がくずれないかを確かめる。"],
              pc=[("主語に合う be 動詞を選んでいる", 1), ("動詞を ing 形にしている", 1)],
              pit=["be 動詞か ing 形のどちらかを落とす。", "複数の主語（Yumi and Aya など）に is を使う。"], why=why)


@gen("basic_check", 4, ["computation", "concept"])
def can_form(r):
    s, _, sj, _ = r.choice([x for x in SUBJ if x[0] not in ("We",)])
    v, v3, obj, jp_v = r.choice(CAN_ACT)
    kind = r.choice(["aff", "neg"])
    if kind == "aff":
        jp = f"{sj}は{jp_v}ことができます。"
        ok = f"can {v}"
        why = {f"can {v3}": ("can の後ろの動詞はいつも原形。主語が何でも s はつけない。", "助動詞の後ろの動詞の形"),
               f"cans {v}": ("can は主語によって形が変わらない。cans という形はない。", "助動詞の形"),
               f"can to {v}": ("can の後ろに to は置かない。can の直後に動詞の原形を置く。", "助動詞の後ろの形")}
    else:
        jp = f"{sj}は{jp_v}ことができません。"
        ok = f"can't {v}"
        why = {f"don't can {v}" if s not in THIRD_NAMES else f"doesn't can {v}": ("can の文の否定は can の後ろに not をつける（can't / cannot）。do / does は使わない。", "一般動詞の否定文との混同"),
               f"can't {v3}": ("can't の後ろの動詞も原形。s はつけない。", "助動詞の後ろの動詞の形"),
               f"{'am' if s == 'I' else 'is' if s in THIRD_NAMES else 'are'} not can {v}": ("can は be 動詞といっしょに使わない。can の後ろに not をつける。", "be 動詞の否定文との混同")}
    return mc(f"日本語に合うように、（　）に入る最も適切なものを選びなさい。\n{jp}\n{s} (　　) {obj}.", [ok] + list(why),
              f"「～できる」は can＋動詞の原形、「～できない」は can't（cannot）＋動詞の原形。答えは {ok}。", d=1,
              ap="can があるときは、主語が何であっても後ろの動詞は原形。否定は can の後ろに not をつける。",
              steps=["日本語から「できる」か「できない」かを確認する。", f"can（can't）の後ろに原形 {v} を置く。", f"答え：{ok}"],
              alt=["can を取り除いた文（現在形）と比べ、三単現の s が消えていることを確かめる。"],
              pc=[("can / can't を正しく選んでいる", 1), ("後ろの動詞を原形にしている", 1)],
              pit=["主語が三人称単数のとき、can の後ろの動詞に s をつける。", "否定文に do / does を使う。"], why=why)


THIRD_NAMES = {s[0] for s in THIRD}

IMP = [
    ("窓を開けてください。", "(　　) open the window.", "Please",
     [("Let's", "Let's は「いっしょに～しよう」という誘いで、相手に頼む「～してください」にはならない。"),
      ("Don't", "Don't は「～してはいけない」という禁止になり、意味が逆になる。"),
      ("Can", "Can で始めると疑問文になるので、文末は ? になる。")]),
    ("気をつけて。道がぬれているよ。", "(　　) careful. The road is wet.", "Be",
     [("Are", "命令文は動詞の原形で始める。are は原形ではない。"),
      ("Do", "careful は形容詞なので、一般動詞の do ではなく be 動詞の原形 Be が必要。"),
      ("Is", "命令文は動詞の原形で始める。is は原形ではない。")]),
    ("この川で泳いではいけません。", "(　　) swim in this river.", "Don't",
     [("Not", "禁止の命令文は Don't で始める。Not だけでは文にならない。"),
      ("Doesn't", "命令文の相手は you なので、doesn't は使わない。"),
      ("Let's", "Let's は「泳ごう」という誘いになり、意味が逆になる。")]),
    ("授業に遅れてはいけません。", "Don't (　　) late for class.", "be",
     [("are", "Don't の後ろは動詞の原形。late は形容詞なので be 動詞の原形 be を置く。"),
      ("is", "Don't の後ろは動詞の原形。is は原形ではない。"),
      ("being", "Don't の後ろは原形。ing 形は置かない。")]),
    ("いっしょに歌を歌おう。", "Let's (　　) a song together.", "sing",
     [("singing", "Let's の後ろは動詞の原形。ing 形は置かない。"),
      ("sings", "Let's の後ろは動詞の原形。s はつけない。"),
      ("to sing", "Let's の後ろに to は置かない。")]),
    ("ここで写真をとらないでください。", "Please (　　) take pictures here.", "don't",
     [("not", "禁止の命令文は don't を使う。not だけでは命令文にならない。"),
      ("aren't", "take は一般動詞なので be 動詞の否定 aren't は使えない。"),
      ("can't", "Please can't ～ という形はない。禁止を頼むときは Please don't ～.")]),
    ("手を洗いなさい。", "(　　) your hands.", "Wash",
     [("Washing", "命令文は動詞の原形で始める。ing 形では命令文にならない。"),
      ("Washes", "命令文は動詞の原形で始める。s はつけない。"),
      ("You washing", "主語＋ing 形だけでは文にならず、命令文にもならない。")]),
    ("今日は公園へ行こう。", "(　　) go to the park today.", "Let's",
     [("Let", "「～しよう」は Let's（Let us の短縮形）。Let だけでは「～させる」の意味になり、文が成り立たない。"),
      ("Don't", "Don't は「行ってはいけない」という禁止になり、意味が逆になる。"),
      ("Are", "Are で始めると be 動詞の疑問文になるが、後ろが go のままでは文が成り立たない。")]),
    ("お年寄りに親切にしなさい。", "(　　) kind to old people.", "Be",
     [("Do", "kind は形容詞なので、be 動詞の原形 Be が必要。"),
      ("Are", "命令文は原形で始める。are は原形ではない。"),
      ("Being", "命令文は原形で始める。ing 形は使わない。")]),
    ("廊下を走ってはいけません。", "Don't (　　) in the hallway.", "run",
     [("running", "Don't の後ろは原形。ing 形は置かない。"),
      ("runs", "Don't の後ろは原形。s はつけない。"),
      ("to run", "Don't の後ろに to は置かない。")]),
    ("ここに名前を書いてください。", "(　　) your name here, please.", "Write",
     [("Writing", "命令文は原形で始める。ing 形は使わない。"),
      ("Writes", "命令文は原形で始める。s はつけない。"),
      ("To write", "命令文は原形で始める。to はつけない。")]),
    ("恥ずかしがらないで。", "Don't (　　) shy.", "be",
     [("are", "Don't の後ろは原形。shy は形容詞なので be を置く。"),
      ("do", "shy は形容詞なので、一般動詞 do ではなく be が必要。"),
      ("is", "Don't の後ろは原形。is は原形ではない。")]),
    ("お昼ごはんを食べよう。", "Let's (　　) lunch.", "have",
     [("having", "Let's の後ろは原形。ing 形は置かない。"),
      ("has", "Let's の後ろは原形。has は三人称単数現在の形。"),
      ("to have", "Let's の後ろに to は置かない。")]),
]


@gen("basic_check", 4, ["concept", "condition_check"])
def imperative(r):
    jp, s, ok, wrongs = r.choice(IMP)
    return mc(f"日本語の意味になるように、（　）に入る最も適切なものを選びなさい。\n{jp}\n{s}", [ok] + [w for w, _ in wrongs],
              f"{ok} が入る。命令文・Let's・Don't の文では、動詞はいつも原形。形容詞を使う命令文は be 動詞の原形 Be（be）を使う。", d=1,
              ap="日本語が「～しなさい」「～してはいけない」「～しよう」のどれかを確かめ、空所の後ろが動詞か形容詞かを見る。",
              steps=["日本語から文の種類（命令・禁止・誘い・依頼）を決める。", "空所の後ろの語が動詞か形容詞かを確かめる。", f"答え：{ok}"],
              alt=["完成した英文を日本語に訳し直して、問題の日本語と一致するかを確かめる。"],
              pc=[("文の種類を正しく判断している", 1), ("正しい語を選んでいる", 1)],
              pit=["形容詞（careful, quiet など）の前に Be を置くのを忘れる。", "Let's や Don't の後ろに ing 形や to を置く。"],
              why={w: (reason, "命令文の形") for w, reason in wrongs})


@gen("basic_check", 4, ["concept", "condition_check"])
def response(r):
    kind = r.choice(["prog_you", "prog_3", "can_you", "can_3", "lets"])
    yes = r.random() < 0.5
    if kind == "prog_you":
        v, ing, _, obj, jo, jte, _ = r.choice(ACT)
        q = f"Are you {ing} {obj} now?"
        ok = "Yes, I am." if yes else "No, I'm not."
        wrong = {("Yes, I do." if yes else "No, I don't."): ("Are you ～? は be 動詞の疑問文なので、do ではなく am を使って答える。", "be 動詞と一般動詞の答え方の混同"),
                 ("Yes, I'm." if yes else "No, I amn't."): (("I'm のような短縮形は文の最後には置けない。Yes, I am. と答える。" if yes else "am not は短縮できないので、I'm not とする。"), "短縮形の使い方"),
                 ("Yes, you are." if yes else "No, you aren't."): ("you でたずねられたら、自分のことなので I で答える。", "答えの主語")}
    elif kind == "prog_3":
        s, be, _, pr = r.choice(THIRD)
        v, ing, _, obj, jo, jte, _ = r.choice(ACT)
        q = f"Is {mid(s)} {ing} {obj}?"
        ok = f"Yes, {pr} is." if yes else f"No, {pr} isn't."
        wrong = {(f"Yes, {pr} does." if yes else f"No, {pr} doesn't."): ("Is ～? は be 動詞の疑問文なので、does ではなく is を使って答える。", "be 動詞と一般動詞の答え方の混同"),
                 (f"Yes, {pr}'s." if yes else f"No, {pr} not."): (("he's のような短縮形は文の最後には置けない。" if yes else "is が抜けている。isn't か is not が必要。"), "短縮形の使い方"),
                 (f"Yes, {pr} can." if yes else f"No, {pr} can't."): ("Is ～? の疑問文には is を使って答える。can は Can ～? の答えに使う。", "疑問文と答えの対応")}
    elif kind == "can_you":
        v, v3, obj, jp_v = r.choice(CAN_ACT)
        q = f"Can you {v} {obj}?"
        ok = "Yes, I can." if yes else "No, I can't."
        wrong = {("Yes, I do." if yes else "No, I don't."): ("Can ～? の疑問文には can を使って答える。", "一般動詞の答え方との混同"),
                 ("Yes, I am." if yes else "No, I'm not."): ("Can ～? の疑問文には can を使って答える。am は be 動詞の疑問文の答え。", "be 動詞の答え方との混同"),
                 ("Yes, you can." if yes else "No, you can't."): ("you でたずねられたら、自分のことなので I で答える。", "答えの主語")}
    elif kind == "can_3":
        s, be, _, pr = r.choice(THIRD)
        v, v3, obj, jp_v = r.choice(CAN_ACT)
        q = f"Can {mid(s)} {v} {obj}?"
        ok = f"Yes, {pr} can." if yes else f"No, {pr} can't."
        wrong = {(f"Yes, {pr} does." if yes else f"No, {pr} doesn't."): ("Can ～? の疑問文には can を使って答える。", "一般動詞の答え方との混同"),
                 (f"Yes, {pr} cans." if yes else f"No, {pr} isn't."): (("can は主語によって形が変わらない。cans という形はない。" if yes else "Can ～? の疑問文には can't で答える。isn't は be 動詞の疑問文の答え。"), "助動詞の形"),
                 (f"Yes, {pr} is." if yes else f"No, {pr} don't."): (("Can ～? の疑問文には can で答える。" if yes else f"Can ～? の疑問文には can't で答える。また {pr} に don't は使わない。"), "疑問文と答えの対応")}
    else:
        what = r.choice([("play", "basketball after school"), ("eat", "lunch under the tree"), ("study", "English together"),
                         ("go", "to the library"), ("watch", "the soccer game on TV"), ("clean", "the classroom together"),
                         ("make", "a poster for the school festival"), ("walk", "to the station")])
        q = f"Let's {what[0]} {what[1]}."
        ok = "Yes, let's." if yes else "No, let's not."
        wrong = {("Yes, I am." if yes else "No, I'm not."): ("Let's ～. の誘いには be 動詞で答えない。Yes, let's. / No, let's not. を使う。", "Let's への答え方"),
                 ("Yes, I do." if yes else "No, let's don't."): (("Let's ～. の誘いには do で答えない。" if yes else "let's の否定は let's not。don't は使わない。"), "Let's への答え方"),
                 ("Yes, you can." if yes else "No, you can't."): ("Yes, you can. は Can I ～?（～してもいいですか）への答えで、誘いへの答えにならない。", "疑問文と答えの対応")}
    yn = "「はい」" if yes else "「いいえ」"
    return mc(f"次の英文に{yn}と答えるとき、最も適切なものを選びなさい。\n{q}", [ok] + list(wrong),
              f"答え：{ok}。たずねる文で使われた be 動詞・can・Let's に合わせて答える。", d=2,
              ap="問いかけの文が何で始まっているか（Are / Is / Can / Let's）を見て、答えに使う語を決める。",
              steps=["問いかけの文の最初の語を確認する。", "you でたずねられたら I、人の名前なら he / she で答える。", f"答え：{ok}"],
              alt=["答えの文に省略された部分を補ってみる（Yes, I am playing. のように）と、正しい組み合わせかを確かめられる。"],
              pc=[("答えに使う語（be 動詞・can・let's）を正しく選んでいる", 1), ("主語・肯定否定が正しい", 1)],
              pit=["be 動詞の疑問文に do / does で答える。", "Yes, I'm. のように短縮形で文を終える。"], why=wrong)


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 4, ["computation", "application"])
def prog_rewrite(r):
    s, be, sj, pr = r.choice(SUBJ)
    v, ing, v3, obj, jo, jte, _ = r.choice(ACT)
    kind = r.choice(["prog", "neg", "q"]) if s not in ("I", "We") else r.choice(["prog", "neg"])
    pres = v3 if be == "is" else v
    sl = mid(s)
    con = {"am": "'m", "are": "'re", "is": "'s"}
    if kind == "prog":
        stem = f"次の英文を、文末に now を加えて現在進行形の文に書きかえなさい。\n{s} {pres} {obj}."
        ans = f"{s} {be} {ing} {obj} now."
        v_ = [f"{s}{con[be]} {ing} {obj} now."] if s in ("I", "You", "He", "She", "We", "They") else []
        stp = [f"主語 {s} に合う be 動詞は {be}。", f"{pres} を原形 {v} にもどして ing をつける：{ing}。", f"答え：{ans}"]
    elif kind == "neg":
        stem = f"次の英文を否定文に書きかえなさい。\n{s} {be} {ing} {obj} now."
        ans = f"{s} {be} not {ing} {obj} now."
        short = {"am": None, "are": "aren't", "is": "isn't"}[be]
        v_ = ([f"{s} {short} {ing} {obj} now."] if short else []) + ([f"{s}{con[be]} not {ing} {obj} now."] if s in ("I", "You", "He", "She", "We", "They") else [])
        stp = ["現在進行形は be 動詞の文なので、be 動詞の後ろに not を置く。", "ing 形はそのまま残す。", f"答え：{ans}"]
    else:
        stem = f"次の英文を疑問文に書きかえ、さらに Yes で答える文も書きなさい。\n{s} {be} {ing} {obj} now."
        ans = f"{cap(be)} {sl} {ing} {obj} now? ― Yes, {'I am' if s == 'You' else pr + ' ' + be}."
        v_ = []
        stp = ["be 動詞を主語の前に出す。", "答えは主語を代名詞にして、be 動詞を使う。", f"答え：{ans}"]
    return sa(stem, ans, f"現在進行形は be 動詞の文と同じルールで否定文・疑問文を作る。答え：{ans}", d=2, p=4, v=v_ or None,
              ap="現在進行形の文は be 動詞の文。否定は be 動詞の後ろに not、疑問は be 動詞を主語の前に出す。do / does は使わない。",
              steps=stp,
              alt=["書きかえた文を日本語に訳し、「～している」「～していない」「～していますか」の意味になっているかを確かめる。"],
              pc=[("be 動詞の位置・形が正しい", 2), ("ing 形と語順が正しい", 2)],
              pit=["否定文・疑問文で do / does を使う。", "三単現の s を残したまま ing をつける。"])


@gen("standard_practice", 4, ["computation", "condition_check"])
def can_rewrite(r):
    s, be, sj, pr = r.choice([x for x in SUBJ if x[0] not in ("I", "We")])
    v, v3, obj, jp_v = r.choice(CAN_ACT)
    if s == "She" and obj == "the piano":
        s, pr = "Ken", "he"
    pres = v3 if be == "is" else v
    sl = mid(s)
    kind = r.choice(["aff", "neg", "q"])
    if kind == "aff":
        stem = f"次の英文を、can を使って「～することができる」という意味の文に書きかえなさい。\n{s} {pres} {obj}."
        ans = f"{s} can {v} {obj}."
        v_ = None
        stp = ["動詞の前に can を置く。", f"can の後ろは原形なので {pres} → {v}。", f"答え：{ans}"]
    elif kind == "neg":
        stem = f"次の英文を、can't を使って「～することができない」という意味の文に書きかえなさい。\n{s} {pres} {obj}."
        ans = f"{s} can't {v} {obj}."
        v_ = [f"{s} cannot {v} {obj}."]
        stp = ["動詞の前に can't を置く。do / does は使わない。", f"can't の後ろは原形なので {pres} → {v}。", f"答え：{ans}"]
    else:
        ansr = "I can" if s == "You" else f"{pr} can"
        stem = f"次の英文を、can を使って「～することができますか」とたずねる文に書きかえ、Yes で答える文も書きなさい。\n{s} {pres} {obj}."
        ans = f"Can {sl} {v} {obj}? ― Yes, {ansr}."
        v_ = None
        stp = ["Can を文の先頭に置き、主語を続ける。", f"動詞は原形 {v} にする。", f"答えは can を使う：Yes, {ansr}.", f"答え：{ans}"]
    return sa(stem, ans, f"can の文では、主語が何であっても can の後ろは動詞の原形。否定は can't、疑問は Can を主語の前に出す。答え：{ans}", d=2, p=4, v=v_,
              ap="can を加えると後ろの動詞は原形にもどる。否定文・疑問文は can 自身を使って作り、do / does は使わない。",
              steps=stp,
              alt=["can を取り除いて元の文にもどし、三単現の s の有無以外が同じかどうかを確かめる。"],
              pc=[("can（can't / Can）の位置が正しい", 2), ("動詞を原形にしている", 2)],
              pit=["三単現の s を残す（can plays）。", "Does he can ～? のように do / does を使う。"])


@gen("standard_practice", 4, ["cross_unit", "concept"], rel=["JH-ENG-G1-U03"])
def what_doing(r):
    who = r.choice([("you", "are", "I'm", "do"), ("he", "is", "He's", "does"), ("she", "is", "She's", "does"),
                    ("they", "are", "They're", "do"), ("Ken", "is", "He's", "does"), ("your mother", "is", "She's", "does"),
                    ("your brothers", "are", "They're", "do"), ("Emi", "is", "She's", "does")])
    s, be, ans_s, do = who
    v, ing, v3, obj, jo, jte, _ = r.choice(ACT)
    other_be = "is" if be == "are" else "are"
    ok = f"What {be} {s} doing?"
    why = {f"What {do} {s} doing?": (f"ing 形を使う進行形の疑問文には be 動詞が必要。{do} は一般動詞の疑問文で使う。", "be 動詞と do / does の混同"),
           f"What {be} {s} do?": ("答えが「今～している」なので、たずねる文も進行形 doing にする。What ～ do? だと動作の内容は聞けるが進行形にならない。", "進行形の形"),
           f"What {other_be} {s} doing?": (f"主語 {s} に合う be 動詞は {be}。", "主語と be 動詞の対応")}
    return mc(f"次の対話が成り立つように、A の（　）に入る最も適切なものを選びなさい。\nA：(　　)\nB：{ans_s} {ing} {obj}.", [ok] + list(why),
              f"B が「今～している」と答えているので、A は What＋be 動詞＋主語＋doing? でたずねる。答え：{ok}", d=3,
              ap="B の答えの形（主語と be 動詞＋ing）から、A のたずね方を逆算する。疑問詞 What は文の先頭。",
              steps=[f"B の答え {ans_s} {ing} ～ は現在進行形。", f"主語 {s} に合う be 動詞は {be}。", f"「何をしているか」なので What {be} {s} doing? とする。"],
              alt=["選んだ疑問文の What を答えの部分（" + f"{ing} {obj}" + "）に置きかえて、B の文と同じ形になるかを確かめる。"],
              pc=[("B の答えが現在進行形だと気づいている", 2), ("be 動詞と doing を正しく使った疑問文を選んでいる", 2)],
              pit=["What do you doing? のように do と ing を組み合わせる。", "答えの主語（I）につられて、疑問文の be 動詞を am にする。"], why=why)


ORDERS = [
    ("ユキは今、図書館で勉強しています。", ["Yuki", "is", "studying", "in", "the library", "now"], "現在進行形：主語＋is＋ing 形＋場所＋now"),
    ("あなたは今、何をしているのですか。", ["what", "are", "you", "doing", "now"], "疑問詞 What＋be 動詞＋主語＋doing"),
    ("私の兄は今、ギターをひいていません。", ["my brother", "is", "not", "playing", "the guitar", "now"], "現在進行形の否定文：is の後ろに not"),
    ("彼らは公園でサッカーをしているのですか。", ["are", "they", "playing", "soccer", "in", "the park"], "現在進行形の疑問文：Are を主語の前に"),
    ("私の祖母はとても上手に料理ができます。", ["my grandmother", "can", "cook", "very", "well"], "can＋原形 cook"),
    ("あなたはこの漢字が読めますか。", ["can", "you", "read", "this", "kanji"], "can の疑問文：Can＋主語＋原形"),
    ("私の弟は速く泳ぐことができません。", ["my brother", "can't", "swim", "fast"], "can の否定文：can't＋原形"),
    ("あなたの消しゴムを使ってもいいですか。", ["can", "I", "use", "your", "eraser"], "許可を求める Can I ～?"),
    ("私を手伝ってくれますか。", ["can", "you", "help", "me"], "依頼の Can you ～?"),
    ("この部屋で食べ物を食べてはいけません。", ["don't", "eat", "food", "in", "this", "room"], "禁止の命令文：Don't＋原形"),
    ("授業中は静かにしなさい。", ["be", "quiet", "during", "the", "class"], "be 動詞の命令文：Be＋形容詞"),
    ("放課後、テニスをしましょう。", ["let's", "play", "tennis", "after", "school"], "Let's＋原形"),
    ("どうぞ、あなたの名前をここに書いてください。", ["please", "write", "your", "name", "here"], "Please＋命令文"),
    ("会議に遅れないでください。", ["please", "don't", "be", "late", "for", "the meeting"], "Please＋Don't be＋形容詞"),
]


@gen("standard_practice", 4, ["application", "computation"])
def build_order(r):
    jp, parts, pat = r.choice(ORDERS)
    sent = cap(" ".join(parts)) + ("?" if jp.endswith("か。") else ".")
    return order(f"日本語に合うように、次の語句を並べかえて英文を完成させなさい。ただし、文頭にくる語も小文字で示してある。\n{jp}", parts,
                 f"{sent}　ポイント：{pat}。", d=2, p=4,
                 ap="日本語が「～している」「～できる」「～しなさい・～しよう」のどれかを見て、文の型を先に決める。次に主語と動詞の部分を作る。",
                 steps=[f"文の型を決める：{pat}。", "文頭にくる語（主語・Can・Don't・Let's など）を決める。", "動詞の後ろに目的語、場所・時を表す語句の順に並べる。", f"完成文：{sent}"],
                 alt=["完成した英文を日本語に訳し直して、問題の日本語と一致するかを確かめる。"],
                 pc=[("文頭と動詞の部分の語順が正しい", 2), ("目的語・修飾語句の順序が正しい", 2)],
                 pit=["疑問文で be 動詞や Can を主語の後ろに置いたままにする。", "場所と時を表す語句の順（場所 → 時）を逆にする。"])


SITU = [
    ("図書館で、友だちが大きな声で話している。注意するとき。", "Please be quiet here.",
     [("Let's talk loudly here.", "「ここで大声で話そう」と誘う意味になり、注意にならない。"),
      ("You can talk loudly here.", "「ここで大声で話してもいい」と許可する意味になる。"),
      ("Are you quiet here?", "「ここでは静かですか」とたずねる文で、注意にならない。")]),
    ("重い荷物を運んでいて、友だちに手伝ってほしいとき。", "Can you help me?",
     [("Can I help you?", "「手伝いましょうか」と申し出る文で、自分が手伝う側になる。"),
      ("Don't help me.", "「手伝わないで」という禁止で、意味が逆になる。"),
      ("I'm helping you.", "「私があなたを手伝っている」という意味で、頼む文にならない。")]),
    ("友だちのペンを借りたいとき。", "Can I use your pen?",
     [("Can you use my pen?", "使うのが相手になってしまい、「私のペンを使えますか」の意味になる。"),
      ("Use my pen.", "「私のペンを使いなさい」という命令で、自分が借りる場面に合わない。"),
      ("I'm using your pen.", "「あなたのペンを使っている」という報告で、許可を求める文にならない。")]),
    ("雨の日の昼休み、友だちを教室でのトランプに誘うとき。", "Let's play cards in the classroom.",
     [("Don't play cards in the classroom.", "「教室でトランプをしてはいけない」という禁止になる。"),
      ("Are you playing cards in the classroom?", "「教室でトランプをしているのですか」とたずねる文で、誘いにならない。"),
      ("You can't play cards in the classroom.", "「教室ではトランプができない（してはいけない）」という意味になる。")]),
    ("電話がかかってきたが、母は手が離せない。「母は今、夕食を作っています」と伝えるとき。", "My mother is cooking dinner now.",
     [("My mother cooks dinner now.", "現在形は「ふだん～する」という習慣を表すので、「今作っている最中」を伝えられない。"),
      ("My mother can cook dinner.", "「母は夕食を作ることができる」という能力の意味になる。"),
      ("Let's cook dinner now.", "「今、夕食を作ろう」という誘いになり、母の様子を伝えていない。")]),
    ("プールの近くで、走っている小さな子どもに注意するとき。", "Don't run here.",
     [("Let's run here.", "「ここで走ろう」という誘いになり、注意にならない。"),
      ("You are running here.", "「あなたはここで走っている」という事実を述べただけで、注意の文にならない。"),
      ("Can you run here?", "「ここで走れますか」とたずねる文になる。")]),
    ("留学生に、自分ができることを紹介するとき（けん玉）。", "I can play kendama.",
     [("I'm playing kendama.", "「今けん玉をしている」という意味で、できることの紹介にならない。"),
      ("Let's play kendama.", "「けん玉をしよう」という誘いになる。"),
      ("Play kendama.", "「けん玉をしなさい」という命令になる。")]),
    ("テストの前、緊張している友だちを励ますとき。", "Don't be nervous.",
     [("Don't nervous.", "nervous は形容詞なので、Don't の後ろに be が必要。"),
      ("You aren't nervous.", "「あなたは緊張していない」と事実を述べる文で、励ましにならない。"),
      ("Can you be nervous?", "「緊張できますか」という意味の文になり、場面に合わない。")]),
    ("「あの鳥を見て！」と友だちに声をかけるとき。", "Look at that bird!",
     [("Looking at that bird!", "ing 形では命令文にならない。命令文は動詞の原形で始める。"),
      ("Let's looking at that bird!", "Let's の後ろは原形。また、驚いて声をかける場面には命令文が合う。"),
      ("You can look that bird!", "look は「～を見る」というときに at が必要で、命令の意味にもならない。")]),
    ("友だちから「いっしょに買い物に行こう」と誘われたが、宿題があって断るとき。", "No, let's not. I have a lot of homework.",
     [("No, I'm not. I have a lot of homework.", "Let's ～. への答えに be 動詞は使わない。"),
      ("No, let's don't. I have a lot of homework.", "let's の否定は let's not。don't は使わない。"),
      ("Yes, let's. I have a lot of homework.", "宿題があって断る場面なのに「そうしよう」と賛成している。")]),
    ("妹に「部屋をきれいにしなさい」と言うとき。", "Clean your room.",
     [("Cleaning your room.", "ing 形では命令文にならない。"),
      ("You cleaning your room.", "be 動詞がなく文として成り立たない。命令文は原形で始める。"),
      ("Let's cleaning your room.", "Let's の後ろは原形で、ing 形は置かない。")]),
    ("「父は今、新聞を読んでいるところです」と伝えるとき。", "My father is reading a newspaper now.",
     [("My father reads a newspaper now.", "現在形は習慣を表すので、「今読んでいるところ」を伝えられない。"),
      ("My father is read a newspaper now.", "be 動詞の後ろは ing 形にしないと進行形にならない。"),
      ("My father can read a newspaper now.", "「父は今、新聞を読むことができる」という可能の意味になる。")]),
]


@gen("standard_practice", 4, ["application", "concept"])
def situation(r):
    sit, ok, wrongs = r.choice(SITU)
    return mc(f"次の場面で言う英文として最も適切なものを選びなさい。\n場面：{sit}", [ok] + [w for w, _ in wrongs],
              f"「{ok}」が場面に合う。命令文・Don't ～.・Let's ～.・Can you ～? / Can I ～?・現在進行形のどれが場面の目的（注意・依頼・許可・誘い・様子の報告）に合うかで選ぶ。", d=2,
              ap="場面で話し手がしたいこと（注意する・頼む・許可を求める・誘う・今の様子を伝える）を先に決める。",
              steps=["場面の目的を日本語でまとめる。", "目的に合う文の型を決める（Don't ～. / Can you ～? / Can I ～? / Let's ～. / be＋ing）。", f"答え：{ok}"],
              alt=["選択肢を日本語に訳して、場面のせりふとして自然かどうかを1つずつ確かめる。"],
              pc=[("場面の目的を正しく読み取っている", 2), ("目的に合う文の型を選んでいる", 2)],
              pit=["Can you ～?（依頼）と Can I ～?（許可）を取り違える。", "今の様子を伝えるのに現在形を使う。"],
              why={w: (reason, "場面と表現の対応") for w, reason in wrongs})


# ======================================================================
# C 思考力・記述応用
# ======================================================================

PAIRS = [
    ("Ken plays tennis.", "Ken is playing tennis now.",
     "A は現在形で「ケンは（ふだん）テニスをする」という習慣を表す。B は現在進行形（is＋playing）で「ケンは今テニスをしているところだ」という、話している時点で進行中の動作を表す。"),
    ("She can play the guitar.", "She is playing the guitar.",
     "A は can＋原形で「彼女はギターをひくことができる」という能力を表し、今ひいているかどうかはわからない。B は現在進行形で「彼女は（今）ギターをひいている」という進行中の動作を表す。"),
    ("Can you open the window?", "Can you swim?",
     "どちらも Can you ～? の形だが、A は「窓を開けてくれますか」という相手への依頼、B は「あなたは泳げますか」という能力をたずねる文。場面と動詞の内容から意味を判断する。"),
    ("Open the window.", "Let's open the window.",
     "A は命令文で「窓を開けなさい」と相手だけに動作を求める。B は Let's ～. で「（いっしょに）窓を開けよう」と、話し手も含めて誘う文になる。"),
    ("You are quiet.", "Be quiet.",
     "A は主語 You と be 動詞 are がある肯定文で「あなたは静かだ」という状態を述べる。B は主語がなく be 動詞の原形 Be で始まる命令文で「静かにしなさい」と相手に求める。"),
    ("Are you cooking?", "Do you cook?",
     "A は現在進行形の疑問文で「（今）料理をしているのですか」と今の動作をたずねる。B は一般動詞の現在形の疑問文で「（ふだん）料理をしますか」と習慣をたずねる。"),
    ("Can I use your bike?", "Can you use your bike?",
     "A は主語が I で「あなたの自転車を使ってもいいですか」と自分の動作の許可を求める。B は主語が you で「あなたは自分の自転車を使えますか（使ってくれますか）」と相手の動作についてたずねる。主語がだれかで意味が変わる。"),
    ("Don't eat here.", "Let's not eat here.",
     "A は Don't ～. で「ここで食べてはいけない」と相手に禁止する。B は Let's not ～. で「ここで食べるのはやめよう」と、話し手も含めて提案する。"),
    ("I have a dog.", "I am having lunch.",
     "A の have は「持っている・飼っている」という状態を表すので進行形にしない。B の have は「食べる」という動作を表すので進行形にでき、「私は昼食を食べているところだ」の意味になる。"),
    ("Please sit down.", "Sit down.",
     "どちらも命令文で「座ってください（座りなさい）」の意味だが、A は Please をつけることで、相手にていねいにお願いする言い方になる。B は please がないので、場面によっては強い指示に聞こえる。"),
]


@gen("thinking_writing", 3, ["written_reasoning", "concept"])
def explain_difference(r):
    a, b, model = r.choice(PAIRS)
    return desc(f"次の2つの英文 A・B の意味の違いを、文の形（動詞の形や文頭の語）に注目して日本語で説明しなさい。\nA：{a}\nB：{b}", model,
                "動詞の前に be 動詞や can があるか、主語があるか、文頭に何があるかで文の意味が変わる。",
                [("A の文の形と意味を正しく説明している", 3), ("B の文の形と意味を正しく説明している", 3), ("違いを生む形の部分（be＋ing・can・主語の有無など）を指摘している", 2)], d=3, p=8, lines=5,
                ap="2つの文で違っている部分に印をつけ、その部分がどんな意味を加えるのか（今している・できる・しなさい・しよう）を考える。",
                steps=["A と B を見比べ、違う部分を見つける。", "その部分の働き（進行中・能力・依頼・命令・誘い・状態など）を確かめる。", "それぞれの和訳を示して違いを説明する。"],
                alt=["それぞれの文に合う場面（だれが、いつ、何のために言うか）を考えて、場面の違いから説明する方法もある。"],
                pc=[("A の説明", 3), ("B の説明", 3), ("形の違いの指摘", 2)],
                pit=["和訳だけを書き、どの形が意味の違いを生んでいるかを書かない。", "現在形と現在進行形の違いを「今」の有無だけで説明し、習慣という意味に触れない。"])


STATE = [
    ("私は今、その答えを知っています。", "I know the answer now.", "know（知っている）は動作ではなく状態を表す動詞なので、「今」のことでも進行形にせず現在形で表す。"),
    ("私の弟は今、新しい自転車をほしがっています。", "My brother wants a new bike now.", "want（ほしい）は気持ちの状態を表す動詞なので進行形にせず、主語が三人称単数なので wants とする。"),
    ("ケンは今、昼食を食べています。", "Ken is having lunch now.", "この have は「食べる」という動作を表すので、進行形にできる。主語が三人称単数なので is having。"),
    ("私たちは今、音楽室で歌を歌っています。", "We are singing songs in the music room now.", "sing は動作を表す動詞なので、「今～している」は現在進行形 are singing で表す。"),
    ("彼女はネコが大好きです。", "She likes cats very much.", "like（好きだ）は状態を表す動詞なので進行形にしない。ふだんからの気持ちなので現在形 likes。"),
    ("私の姉は自分の部屋をもっています。", "My sister has her own room.", "この have は「持っている」という状態を表すので進行形にしない。主語が三人称単数なので has。"),
    ("父は今、車を洗っています。", "My father is washing his car now.", "wash は動作を表す動詞なので、「今～している」は現在進行形 is washing で表す。"),
    ("佐藤先生は私の兄を知っています。", "Mr. Sato knows my brother.", "know は状態を表す動詞なので進行形にしない。主語が三人称単数なので knows。"),
]


@gen("thinking_writing", 2, ["condition_check", "written_reasoning"])
def state_verbs(r):
    jp, ans, why_s = r.choice(STATE)
    return desc(f"次の日本語を英語に直しなさい。また、現在形と現在進行形のどちらを使ったか、その理由を説明しなさい。\n{jp}", f"{ans}　理由：{why_s}",
                "現在進行形にできるのは、始まりと終わりのある「動作」を表す動詞。know / like / want / have（持っている）など「状態」を表す動詞はふつう進行形にしない。",
                [("正しい英文を書いている", 4), ("動詞が動作か状態かに触れて理由を説明している", 3), ("主語に合う動詞の形（be 動詞・三単現）になっている", 1)], d=4, p=8, lines=4,
                ap="日本語の「～している」がいつも進行形になるとは限らない。動詞が「動作」か「状態」かを先に確かめる。",
                steps=["日本語の動詞が動作か状態かを判断する。", "動作なら be＋ing、状態なら現在形を選ぶ。", "主語に合わせて be 動詞・三単現の s を決める。", f"答え：{ans}"],
                alt=["「～しているところだ」と言いかえて自然かどうかを試す（「知っているところだ」は不自然なので状態動詞）。"],
                pc=[("英文", 4), ("理由の説明", 3), ("主語との一致", 1)],
                pit=["日本語の「～している」につられて I'm knowing ～. と書く。", "状態動詞を現在形にしたとき、三単現の s を落とす。"])


FORM_SUBJ = [("My brother", "私の兄"), ("Emi", "エミ"), ("Our teacher", "私たちの先生"), ("Tom", "トム"), ("My cousin", "私のいとこ")]
FORM_ACT = [("play", "plays", "playing", "the guitar"), ("swim", "swims", "swimming", "in the sea"), ("make", "makes", "making", "curry"),
            ("study", "studies", "studying", "Chinese"), ("write", "writes", "writing", "a story"), ("run", "runs", "running", "in the park"),
            ("dance", "dances", "dancing", "on the stage"), ("draw", "draws", "drawing", "manga"), ("watch", "watches", "watching", "baseball games")]


@gen("thinking_writing", 3, ["cross_unit", "written_reasoning"], rel=["JH-ENG-G1-U01"])
def three_forms(r):
    s, sj = r.choice(FORM_SUBJ)
    v, v3, ing, obj = r.choice(FORM_ACT)
    model = (f"(1) {v3}　(2) {v}　(3) {ing}。理由：(1) 主語 {s} は三人称単数で、ふだんの習慣を表す現在形なので s（es）をつける。"
             f"(2) can の後ろの動詞は、主語に関係なくいつも原形。(3) is があり now があるので、be 動詞＋ing 形の現在進行形にする。")
    return desc(f"（　）内の動詞 {v} を、それぞれ適切な形に直しなさい。また、(1)～(3) で形が変わる理由を説明しなさい。\n(1) {s} (　　) {obj} every week.\n(2) {s} can (　　) {obj}.\n(3) {s} is (　　) {obj} now.",
                model, "同じ主語・同じ動詞でも、動詞の前に何があるか（何もない・can・be 動詞）で動詞の形が決まる。前の単元で学んだ三人称単数現在のルールと、この単元の can・進行形のルールを区別する。",
                [("(1)～(3) の形をすべて正しく書いている", 3), ("三単現の s をつける理由を説明している", 2), ("can の後ろが原形になる理由を説明している", 2), ("進行形になる理由を説明している", 1)], d=4, p=8, lines=5,
                ap="主語が三人称単数であることを確認したうえで、動詞の直前に何があるか（何もない／can／is）を見る。",
                steps=[f"(1) 動詞の前に何もない現在形 → 三単現 {v3}。", f"(2) can の後ろ → 原形 {v}。", f"(3) is＋～＋now → ing 形 {ing}。", "それぞれの理由をまとめる。"],
                alt=["(1)～(3) を否定文にしてみる（doesn't＋原形／can't＋原形／isn't＋ing 形）と、どのルールの文かがはっきりする。"],
                pc=[("3つの形", 3), ("三単現の理由", 2), ("can の理由", 2), ("進行形の理由", 1)],
                pit=["(2) で can の後ろにも s をつける（can plays）。", "(3) で三単現の s を残したまま ing をつける。"])


WRITE = [
    ("あなたの学校に来た留学生のアレックスを、週末に地域の夏祭りへ誘う。", "Let's go to the summer festival this weekend. We can eat takoyaki there.",
     "誘いの Let's＋原形と、祭りでできることを can＋原形で書いている。"),
    ("クラスの友だちを、昼休みに校庭でのドッジボールに誘う。", "Let's play dodgeball in the schoolyard at lunchtime. We can play with our classmates.",
     "Let's＋原形で誘い、can で「みんなでできる」ことを付け加えている。"),
    ("海外の友だちに、あなたの町の公園を紹介して、いっしょに行こうと誘う。", "Let's go to Midori Park. You can see many beautiful flowers there.",
     "Let's＋原形で誘い、公園でできることを You can ～. で紹介している。"),
    ("部活動の後輩を、週末の自主練習に誘う。", "Let's practice together this Saturday. We can use the gym in the morning.",
     "Let's＋原形で誘い、練習の条件（できること）を can＋原形で示している。"),
    ("家族を、日曜日に近くの山へのハイキングに誘う。", "Let's go hiking on Sunday. We can see Mt. Fuji from the top.",
     "Let's＋原形で誘い、山の上でできることを can＋原形で伝えている。"),
    ("友だちを、図書館でのいっしょの宿題に誘う。", "Let's do our homework in the library. We can use the dictionaries there.",
     "Let's＋原形で誘い、図書館でできることを can＋原形で伝えている。"),
    ("留学生を、あなたの家での料理パーティーに誘う。", "Let's cook together at my house. I can make okonomiyaki.",
     "Let's＋原形で誘い、自分ができることを I can ～. で伝えている。"),
    ("友だちを、放課後の文化祭のポスター作りに誘う。", "Let's make a poster for the school festival after school. You can draw pictures well.",
     "Let's＋原形で誘い、相手が得意なことを You can ～. で伝えて誘う理由にしている。"),
]


@gen("thinking_writing", 2, ["application", "written_reasoning"])
def write_invite(r):
    sit, model, point = r.choice(WRITE)
    return desc(f"次の場面で、相手に伝える英文を2文で書きなさい。ただし、1文目は Let's を使って誘い、2文目は can を使ってその場所や活動でできることを伝えること。\n場面：{sit}",
                f"（解答例）{model}", f"（解答例の解説）{point} Let's の後ろも can の後ろも動詞の原形にする。",
                [("1文目が Let's＋動詞の原形で、場面に合う誘いになっている", 3), ("2文目が can＋動詞の原形で、場面に合う内容になっている", 3), ("つづり・語順・文頭の大文字・ピリオドが正しい", 2)], d=4, p=8, lines=4,
                ap="まず日本語で「何に誘うか」「そこで何ができるか」を決めてから英語にする。どちらの文も動詞は原形。",
                steps=["誘う内容（動詞＋場所・時）を決め、Let's ～. の文を書く。", "その場所や活動でできることを決め、主語（We / You / I）＋can＋原形で書く。", "2文のつながり（誘い → 理由）が自然かを見直す。"],
                alt=["2文目を「どうして誘うのか」の理由として書き、相手が来たくなる内容になっているかを読み手の立場で確かめる。"],
                pc=[("Let's の文", 3), ("can の文", 3), ("表記の正確さ", 2)],
                pit=["Let's going ～. や We can to ～. のように原形以外を置く。", "Let's のアポストロフィを落とす（Lets）。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(task, wrong, step, etype, tempt, fix, expl, steps, ap, alt, pit):
    return desc(f"{task}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい英文に書き直しなさい。", fix, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい英文に直している", 3), ("文法のルールを説明している", 1)], d=3, p=6, lines=4,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい英文", 3), ("ルールの説明", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix))


PROG_ERR = [
    ("私は今、テレビを見ています。", "I am watch TV now.", "I am watching TV now.", "watch", "concept",
     "現在進行形は be 動詞＋ing 形。am の後ろの動詞を watching にする。", "be 動詞を置いたことで「進行形にした」と安心し、ing をつけ忘れた。"),
    ("彼らは今、野球をしています。", "They playing baseball now.", "They are playing baseball now.", "playing の前", "concept",
     "ing 形だけでは文の動詞にならない。主語 They に合う be 動詞 are が必要。", "日本語の「～している」を ing だけで表せると考えた。"),
    ("私の妹はプールで泳いでいます。", "My sister is swiming in the pool.", "My sister is swimming in the pool.", "swiming", "notation",
     "swim は「短母音＋子音字」で終わるので、m を重ねて swimming とする。", "そのまま ing をつければよいと考えた。"),
    ("母は今、ケーキを作っています。", "My mother is makeing a cake now.", "My mother is making a cake now.", "makeing", "notation",
     "e で終わる動詞は e をとって ing をつける。making。", "そのまま ing をつけた。"),
    ("あなたは今、宿題をしているのですか。", "Do you doing your homework now?", "Are you doing your homework now?", "Do", "concept",
     "現在進行形は be 動詞の文なので、疑問文は be 動詞 Are を主語の前に出す。", "一般動詞 do があるので、疑問文に Do を使うと考えた。"),
    ("ケンは今、手紙を書いていません。", "Ken doesn't writing a letter now.", "Ken isn't writing a letter now.", "doesn't", "concept",
     "現在進行形の否定文は be 動詞の後ろに not。is not（isn't）を使う。", "三人称単数の否定文は doesn't と覚えていた。"),
    ("私はその女の子の名前を知っています。", "I'm knowing the girl's name.", "I know the girl's name.", "I'm knowing", "concept",
     "know は状態を表す動詞なので進行形にしない。現在形 know を使う。", "日本語の「知っている」の「～している」につられた。"),
    ("トムは今、川沿いを走っています。", "Tom is runing along the river now.", "Tom is running along the river now.", "runing", "notation",
     "run は「短母音＋子音字」で終わるので、n を重ねて running とする。", "子音字を重ねるルールを忘れた。"),
    ("ユミとアヤは今、歌を歌っています。", "Yumi and Aya is singing a song now.", "Yumi and Aya are singing a song now.", "is", "condition",
     "主語 Yumi and Aya は2人（複数）なので be 動詞は are。", "直前の Aya（1人）につられて is にした。"),
    ("彼は今、昼食を食べているのですか。", "Is he eats lunch now?", "Is he eating lunch now?", "eats", "concept",
     "現在進行形の疑問文は Is＋主語＋ing 形。eats を eating にする。", "主語が he なので三単現の s をつけると考えた。"),
]


@gen("error_correction", 4, ["common_error", "computation"])
def err_progressive(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(PROG_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", etype, tempt, fix, f"{rule}正しくは {fix}",
                    ["文が現在進行形（be 動詞＋ing 形）の形になっているかを確認する。", f"「{where}」の部分の誤りを見つける：{rule}", f"正しい英文：{fix}"],
                    "現在進行形は「主語に合う be 動詞」と「正しくつづった ing 形」の2つがそろって初めて成り立つ。両方を1つずつ確かめる。",
                    ["直した文を否定文や疑問文にしてみて、be 動詞の文として形がくずれないかを確かめる。"],
                    ["be 動詞か ing 形のどちらかを落とす。", "ing のつづり（e をとる・子音字を重ねる）を誤る。"])


CAN_ERR = [
    ("私の父は中国語を話すことができます。", "My father can speaks Chinese.", "My father can speak Chinese.", "can speaks", "concept",
     "can の後ろの動詞は、主語が三人称単数でも原形。speaks を speak にする。", "主語が My father（三人称単数）なので s をつけると考えた。"),
    ("あなたはスキーができますか。", "Do you can ski?", "Can you ski?", "Do you can", "concept",
     "can の文の疑問文は Can を主語の前に出す。do は使わない。", "一般動詞の疑問文と同じように Do を使った。"),
    ("彼女は速く走ることができません。", "She doesn't can run fast.", "She can't run fast.", "doesn't can", "concept",
     "can の文の否定は can の後ろに not をつける（can't / cannot）。doesn't は使わない。", "三人称単数の否定文は doesn't と覚えていた。"),
    ("私はピアノをひくことができます。", "I can to play the piano.", "I can play the piano.", "can to", "concept",
     "can の直後に動詞の原形を置く。to は不要。", "「～すること」の to と混同した。"),
    ("ケンはギターをひくことができます。", "Ken cans play the guitar.", "Ken can play the guitar.", "cans", "concept",
     "can は主語によって形が変わらない。cans という形はない。", "三単現の s を can につければよいと考えた。"),
    ("トムは日本語を読むことができますか。― はい、できます。", "Can Tom read Japanese? ― Yes, he does.", "Can Tom read Japanese? ― Yes, he can.", "he does", "concept",
     "Can ～? の疑問文には can を使って答える。", "一般動詞の疑問文の答え方（does）と混同した。"),
    ("あなたのノートを見てもいいですか。", "Can you see your notebook?", "Can I see your notebook?", "you", "interpretation",
     "「～してもいいですか」と自分の動作の許可を求めるときは Can I ～? を使う。Can you ～? では見るのが相手になる。", "「あなたの」につられて主語を you にした。"),
    ("私の兄は泳げません。", "My brother can't swims.", "My brother can't swim.", "swims", "concept",
     "can't の後ろの動詞も原形。swims を swim にする。", "主語が三人称単数なので s をつけると考えた。"),
]


@gen("error_correction", 3, ["common_error", "condition_check"])
def err_can(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(CAN_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", etype, tempt, fix, f"{rule}正しくは {fix}",
                    ["can の後ろの動詞が原形になっているかを確認する。", "否定文・疑問文・答えの文で do / does を使っていないかを確認する。", f"正しい英文：{fix}"],
                    "can の文では、①後ろの動詞は原形、②否定・疑問・答えは can 自身を使う、の2点をいつも確かめる。",
                    ["can を取り除いた文と比べ、can があるときに変わる部分（三単現の s が消える・do / does が不要）を確かめる。"],
                    ["三人称単数の主語につられて、can の後ろの動詞に s をつける。", "一般動詞のルール（do / does）を can の文に持ちこむ。"])


IMP_ERR = [
    ("図書館では静かにしなさい。", "Quiet in the library.", "Be quiet in the library.", "Quiet", "concept",
     "quiet は形容詞なので、命令文にするには be 動詞の原形 Be を文頭に置く。", "日本語の「静かに」が動作のように感じられ、形容詞だけで命令文になると考えた。"),
    ("ここで泳いではいけません。", "Not swim here.", "Don't swim here.", "Not", "concept",
     "禁止の命令文は Don't＋動詞の原形で表す。", "「～ない」を not だけで表せると考えた。"),
    ("いっしょにサッカーをしよう。", "Let's playing soccer together.", "Let's play soccer together.", "playing", "concept",
     "Let's の後ろは動詞の原形。playing を play にする。", "「～しよう」という動作を ing で表そうとした。"),
    ("授業に遅れてはいけません。", "Don't late for class.", "Don't be late for class.", "Don't late", "concept",
     "late は形容詞なので、Don't の後ろに be が必要。", "Don't の後ろに形容詞をそのまま置けると考えた。"),
    ("ドアを閉めなさい。", "Closes the door.", "Close the door.", "Closes", "concept",
     "命令文は動詞の原形で始める。s はつけない。", "相手を「1人」と考えて三単現の s をつけた。"),
    ("「放課後、買い物に行こう。」「いいえ、やめておこう。」", "Let's go shopping after school. ― No, let's don't.", "Let's go shopping after school. ― No, let's not.", "let's don't", "notation",
     "Let's ～. の否定（～しないでおこう）は let's not を使う。", "Don't ～. の否定と同じように don't を使えると考えた。"),
    ("お年寄りに親切にしなさい。", "Are kind to old people.", "Be kind to old people.", "Are", "concept",
     "命令文は動詞の原形で始めるので、be 動詞は原形 Be を使う。", "相手は you なので are を使うと考えた。"),
    ("この部屋で写真をとらないでください。", "Please not take pictures in this room.", "Please don't take pictures in this room.", "not", "concept",
     "禁止の命令文は don't＋原形。Please をつけても don't は必要。", "Please がつくと Don't の do が不要になると考えた。"),
]


@gen("error_correction", 3, ["common_error", "condition_check"])
def err_imperative(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(IMP_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", etype, tempt, fix, f"{rule}正しくは {fix}",
                    ["文頭の語（動詞の原形・Be・Don't・Let's）が正しいかを確認する。", f"「{where}」の部分の誤りを見つける：{rule}", f"正しい英文：{fix}"],
                    "命令文・Don't ～.・Let's ～. では、動詞はいつも原形。形容詞を使うときは be を補う。",
                    ["直した文を声に出して読み、文頭が動詞の原形（または Be・Don't・Let's）になっているかを確かめる。"],
                    ["形容詞の前の Be（be）を落とす。", "Let's の後ろに ing 形を置く。"])


GENERATORS = [ing_spelling, prog_be, can_form, imperative, response,
              prog_rewrite, can_rewrite, what_doing, build_order, situation,
              explain_difference, state_verbs, three_forms, write_invite,
              err_progressive, err_can, err_imperative]
