"""単元パック：中学1年 英語 be動詞と一般動詞の現在形（be動詞・一般動詞・3人称単数現在・否定文と疑問文）。"""
import random

from banks._common import desc, mc, order, sa
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem,
                         tp)

UNIT_ID = "JH-ENG-G1-U01"

PREREQUISITES = [
    ("JH-JPN-G1-U02", "英語の学習としてはこの単元が中学校で最初の単元である。小学校で「I like ～.」「I can ～.」などの表現に慣れ親しんでいることを前提に、国語で学ぶ「主語・述語の関係」を使って、文の中で「だれが（主語）」「どうする・どんなだ（述語）」を見分ける力を前提とする。"),
    ("JH-JPN-G1-U03", "名詞・動詞・形容詞といった品詞の区別。英語では「動作を表す語（一般動詞）」か「状態や性質を表す語（形容詞など）」かによって、be 動詞を使うかどうかが決まる。"),
]
EXTENSIONS = [
    ("JH-ENG-G1-U02", "主語が3人称単数か複数かの判断は、名詞の複数形と人称代名詞（he / she / they など）の学習で、さらに正確にできるようになる。"),
    ("JH-ENG-G1-U03", "What do you ～? / Where does he ～? のように、疑問詞を使った疑問文は「疑問詞＋この単元の疑問文」の形で作る。"),
    ("JH-ENG-G1-U05", "過去形では do / does が did に、am / is / are が was / were に変わるが、否定文・疑問文の作り方の仕組みはこの単元と同じである。"),
    ("HS-ENG-U02", "高校の「時制」では、現在形が「習慣・くり返し・変わらない事実」を表すことを、過去形・未来表現・完了形と比べながら深める。"),
]

# 主語：(英語, 種類, 日本語, 疑問文で聞かれたときに答えで使う代名詞)
# 種類：1s＝I、2＝you（1人）、3s＝3人称単数、pl＝複数
SUBJ = [
    ("I", "1s", "私は", None),
    ("You", "2", "あなたは", "I"),
    ("We", "pl", "私たちは", None),
    ("They", "pl", "彼らは", "they"),
    ("He", "3s", "彼は", "he"),
    ("She", "3s", "彼女は", "she"),
    ("My brother", "3s", "私の兄は", "he"),
    ("My sister", "3s", "私の姉は", "she"),
    ("Ken", "3s", "ケンは", "he"),
    ("Ms. Green", "3s", "グリーン先生は", "she"),
    ("Mr. Sato", "3s", "佐藤先生は", "he"),
    ("Tom and Emi", "pl", "トムとエミは", "they"),
    ("My parents", "pl", "私の両親は", "they"),
    ("You and Ken", "pl", "あなたとケンは", "we"),
    ("Yuki and I", "pl", "ユキと私は", None),
]
# 疑問文・会話で使う主語（相手にたずねる文なので my ではなく your を使う）
QSUBJ = [
    ("You", "2", "あなたは", "I"),
    ("Your brother", "3s", "あなたのお兄さんは", "he"),
    ("Your sister", "3s", "あなたのお姉さんは", "she"),
    ("Ken", "3s", "ケンは", "he"),
    ("Ms. Green", "3s", "グリーン先生は", "she"),
    ("Mr. Sato", "3s", "佐藤先生は", "he"),
    ("Tom and Emi", "pl", "トムとエミは", "they"),
    ("Your parents", "pl", "あなたのご両親は", "they"),
    ("You and Ken", "pl", "あなたとケンは", "we"),
]
Q3 = [s for s in QSUBJ if s[1] == "3s"]
S3 = [s for s in SUBJ if s[1] == "3s"]
SPL = [s for s in SUBJ if s[1] == "pl"]
NAMED3 = [s for s in S3 if s[0] not in ("He", "She")]
KIND_DESC = {"1s": "話し手自身（I）", "2": "話し相手（you）", "3s": "3人称単数（I・you 以外の1人・1つ）", "pl": "複数（2人以上・2つ以上）"}
PRON_KIND = {"I": "1s", "he": "3s", "she": "3s", "we": "pl", "they": "pl", "it": "3s"}

# be 動詞の後ろに続く語句：(英語, 日本語・肯定, 日本語・否定)
BC = [
    ("busy today", "今日、忙しいです", "今日、忙しくありません"),
    ("from Australia", "オーストラリア出身です", "オーストラリア出身ではありません"),
    ("in the library now", "今、図書館にいます", "今、図書館にいません"),
    ("good at cooking", "料理が得意です", "料理が得意ではありません"),
    ("hungry now", "今、おなかがすいています", "今、おなかがすいていません"),
    ("tired", "疲れています", "疲れていません"),
    ("in the music room", "音楽室にいます", "音楽室にいません"),
    ("from Osaka", "大阪出身です", "大阪出身ではありません"),
    ("kind to everyone", "みんなに親切です", "みんなに親切ではありません"),
    ("free this afternoon", "今日の午後、ひまです", "今日の午後、ひまではありません"),
    ("on the soccer team", "サッカー部に入っています", "サッカー部に入っていません"),
    ("at home now", "今、家にいます", "今、家にいません"),
]

# 一般動詞：(原形, 3単現, 後ろの語句, 日本語・肯定, 日本語・否定)
VP = [
    ("play", "plays", ("tennis", "after school"), "放課後テニスをします", "放課後テニスをしません"),
    ("study", "studies", ("math", "after dinner"), "夕食後に数学を勉強します", "夕食後に数学を勉強しません"),
    ("watch", "watches", ("TV", "in the morning"), "朝テレビを見ます", "朝テレビを見ません"),
    ("go", "goes", ("to the library by bus",), "バスで図書館に行きます", "バスで図書館に行きません"),
    ("have", "has", ("a dog",), "犬を飼っています", "犬を飼っていません"),
    ("like", "likes", ("Japanese food",), "日本食が好きです", "日本食が好きではありません"),
    ("speak", "speaks", ("French",), "フランス語を話します", "フランス語を話しません"),
    ("wash", "washes", ("the dishes", "after dinner"), "夕食後に皿を洗います", "夕食後に皿を洗いません"),
    ("live", "lives", ("near the station",), "駅の近くに住んでいます", "駅の近くに住んでいません"),
    ("do", "does", ("homework", "before dinner"), "夕食前に宿題をします", "夕食前に宿題をしません"),
    ("teach", "teaches", ("music",), "音楽を教えています", "音楽を教えていません"),
    ("read", "reads", ("comic books",), "マンガを読みます", "マンガを読みません"),
    ("use", "uses", ("a computer", "at home"), "家でコンピュータを使います", "家でコンピュータを使いません"),
    ("cook", "cooks", ("dinner", "on Sundays"), "日曜日に夕食を作ります", "日曜日に夕食を作りません"),
    ("get", "gets", ("up", "at six"), "6時に起きます", "6時に起きません"),
    ("know", "knows", ("Mr. Brown",), "ブラウンさんを知っています", "ブラウンさんを知りません"),
    ("need", "needs", ("a new bag",), "新しいかばんが必要です", "新しいかばんは必要ではありません"),
    ("enjoy", "enjoys", ("the summer festival",), "夏祭りを楽しみます", "夏祭りを楽しみません"),
]
SPECIAL = {"study": ("studys", "子音字＋y で終わる語は y を i にかえて es をつける"),
           "watch": ("watchs", "ch で終わる語には es をつける"),
           "go": ("gos", "o で終わる go には es をつける"),
           "have": ("haves", "have は不規則に has になる"),
           "wash": ("washs", "sh で終わる語には es をつける"),
           "teach": ("teachs", "ch で終わる語には es をつける"),
           "do": ("dos", "o で終わる do には es をつける"),
           "play": ("plaies", "母音字＋y で終わる語は、そのまま s をつける")}

# 3単現のつづり：(原形, 3単現, 意味, 規則)
R_S = "ふつうはそのまま s をつける"
R_ES = "s・x・sh・ch・o で終わる語には es をつける"
R_IES = "子音字（a・i・u・e・o 以外）＋y で終わる語は、y を i にかえて es をつける"
R_YS = "母音字（a・i・u・e・o）＋y で終わる語は、そのまま s をつける"
R_HAS = "have は例外で has になる"
SPELL = [
    ("play", "plays", "（スポーツなどを）する", R_YS), ("enjoy", "enjoys", "楽しむ", R_YS), ("stay", "stays", "滞在する", R_YS),
    ("buy", "buys", "買う", R_YS), ("say", "says", "言う", R_YS),
    ("study", "studies", "勉強する", R_IES), ("try", "tries", "やってみる", R_IES), ("cry", "cries", "泣く", R_IES),
    ("fly", "flies", "飛ぶ", R_IES), ("carry", "carries", "運ぶ", R_IES),
    ("go", "goes", "行く", R_ES), ("do", "does", "する", R_ES), ("watch", "watches", "見る", R_ES), ("teach", "teaches", "教える", R_ES),
    ("catch", "catches", "捕まえる", R_ES), ("wash", "washes", "洗う", R_ES), ("push", "pushes", "押す", R_ES),
    ("fix", "fixes", "修理する", R_ES), ("pass", "passes", "手渡す", R_ES), ("finish", "finishes", "終える", R_ES),
    ("have", "has", "持っている", R_HAS),
    ("like", "likes", "好きである", R_S), ("make", "makes", "作る", R_S), ("run", "runs", "走る", R_S), ("swim", "swims", "泳ぐ", R_S),
    ("eat", "eats", "食べる", R_S), ("write", "writes", "書く", R_S), ("open", "opens", "開ける", R_S), ("help", "helps", "手伝う", R_S),
    ("come", "comes", "来る", R_S), ("speak", "speaks", "話す", R_S), ("sing", "sings", "歌う", R_S), ("walk", "walks", "歩く", R_S),
]


# ----------------------------------------------------------------------
# 文を作る道具
# ----------------------------------------------------------------------

def be(kind):
    return {"1s": "am", "3s": "is"}.get(kind, "are")


def be_neg(kind):
    return {"1s": "am not", "3s": "isn't"}.get(kind, "aren't")


def be_neg_full(kind):
    return {"1s": "am not", "3s": "is not"}.get(kind, "are not")


def do(kind):
    return "does" if kind == "3s" else "do"


def low(s):
    return s if s in ("I", "Ken", "Ms. Green", "Mr. Sato", "Tom and Emi", "Yuki and I") else s[0].lower() + s[1:]


def cap(s):
    return s[0].upper() + s[1:]


def rest(v):
    return " ".join(v[2])


def vform(subj, v):
    return v[1] if subj[1] == "3s" else v[0]


def be_aff(S, C):
    return f"{S[0]} {be(S[1])} {C[0]}."


def be_neg_s(S, C, full=False):
    if S[1] == "1s":
        return ("I am not" if full else "I'm not") + f" {C[0]}."
    return f"{S[0]} {be_neg_full(S[1]) if full else be_neg(S[1])} {C[0]}."


def be_q(S, C):
    return f"{cap(be(S[1]))} {low(S[0])} {C[0]}?"


def gv_aff(S, V):
    return f"{S[0]} {vform(S, V)} {rest(V)}."


def gv_neg(S, V, full=False):
    aux = ("does not" if full else "doesn't") if S[1] == "3s" else ("do not" if full else "don't")
    return f"{S[0]} {aux} {V[0]} {rest(V)}."


def gv_q(S, V):
    return f"{cap(do(S[1]))} {low(S[0])} {V[0]} {rest(V)}?"


def jp(S, X, neg=False, q=False):
    body = X[2] if (neg and len(X) == 3) else X[4] if neg else (X[1] if len(X) == 3 else X[3])
    return f"{S[2]}{body}{'か' if q else ''}。"


def short(pron, is_be, yes):
    k = PRON_KIND[pron]
    if is_be:
        if yes:
            return f"Yes, {pron} {be(k)}."
        return "No, I'm not." if pron == "I" else f"No, {pron} {be_neg(k)}."
    return f"Yes, {pron} {do(k)}." if yes else f"No, {pron} {do(k)}n't."


def local(key):
    return random.Random(key)


def pick_v(r, exclude=()):
    return r.choice([v for v in VP if v[0] not in exclude])


# ======================================================================
# 授業プリント
# ======================================================================

LESSON = lesson(
    goals=["主語に合わせて be 動詞（am / are / is）を正しく選び、「～です」「～にいる」を表す文を書ける。",
           "一般動詞の現在形を使い、主語が3人称単数のときは動詞に s / es をつけて書ける。",
           "be 動詞の文と一般動詞の文を区別して、否定文・疑問文を作り、Yes / No で答えられる。"],
    duration=50,
    readiness=["小学校の外国語で「I like ～.」「I play ～.」「Do you like ～?」などの表現を聞いたり話したりした経験がある。",
               "アルファベットの大文字・小文字を正しく書き分けられる。",
               "国語で「主語（だれが）」と「述語（どうする・どんなだ）」を見分けられる。",
               "スポーツ・食べ物・教科などの身近な英単語を、いくつか読んだり書いたりできる。"],
    flow=[("導入：2種類の動詞", 5, "I am Ken. と I play tennis. を比べ、「イコールでつなぐ動詞」と「動作を表す動詞」の2種類があることに気づかせる"),
          ("be 動詞と主語", 10, "am / are / is の使い分けを主語の種類で整理する（例題1）"),
          ("一般動詞と3単現", 13, "主語が3人称単数のとき動詞に s / es をつける規則と、つづりの変化を確認する（例題2）"),
          ("否定文・疑問文の作り方", 15, "be 動詞の文は be 動詞を動かし、一般動詞の文は do / does を使う理由を考える（例題3）"),
          ("まとめと確認", 7, "確認問題3問、問題プリントA の課題指示")],
    sections=[
        intro("in1", "英語の動詞には2つのグループがある",
              "日本語では「私はケンです」「私はテニスをします」のように、文の最後に述語がきます。英語では主語のすぐ後ろに動詞を置きますが、その動詞には大きく2つのグループがあります。1つは主語と後ろの語句を「イコール」でつなぐ be 動詞（am / are / is）、もう1つは play（する）、like（好きである）、have（持っている）のように動作や気持ちを表す一般動詞です。英語の文は、どちらか一方の動詞を1つだけ使って作ります。",
              bullets=["I am Ken.（私＝ケン）→ be 動詞の文", "I play tennis.（私はテニスをする）→ 一般動詞の文",
                       "I am play tennis. とは言わない。be 動詞と一般動詞は、ふつう1つの文に並べない。"],
              points=[tp("2つの文を板書し、日本語の「です」と「します」の違いから、英語の動詞にも2種類あることに気づかせる。",
                         ask="I am Ken. と I play tennis. で、am と play はそれぞれどんな働きをしているか。",
                         expect="am は「私＝ケン」をつなぐ。play は「テニスをする」という動作を表す。", timing="導入の冒頭"),
                      tp("「です」＝ am / are / is と1対1で覚えると、I am play tennis. の誤りが生まれることを先に伝えておく。",
                         caution="「私はテニスをします」の「です・ます」を be 動詞に置きかえようとする生徒が多い。")]),
        definition("df1", "be 動詞（am / are / is）",
                   "be 動詞は「主語＝後ろの語句」の関係を表したり、「（どこどこに）いる・ある」ことを表したりする動詞です。現在の文では、主語に合わせて am / are / is の3つの形を使い分けます。",
                   bullets=["主語が I のとき → am（I am a student.）", "主語が you のとき、主語が複数のとき → are（You are kind. / Tom and Emi are from Osaka.）",
                            "主語が3人称単数（I・you 以外の1人・1つ）のとき → is（Ken is busy. / This bag is new.）",
                            "短縮形：I'm / you're / he's / she's / it's / we're / they're、is not → isn't、are not → aren't"],
                   conditions=["「Yuki and I」は I をふくんでいても2人なので複数。be 動詞は are。",
                               "am not には、ふつう使われる短縮形がない。I'm not とする。"],
                   points=[tp("主語の種類を「I／you／3人称単数／複数」の4つの箱に分けて板書し、それぞれに am / are / is を当てはめる。",
                              ask="My parents は何人か。be 動詞はどれになるか。", expect="2人なので複数。are。")]),
        theorem("th1", "一般動詞の現在形と3人称単数現在（3単現）の s",
                "主語が3人称単数で現在の文 → 動詞に s / es をつける（play → plays, watch → watches, study → studies, have → has）",
                ["主語が I・you・複数のときは、動詞は原形（もとの形）のまま：I play / You play / They play。",
                 "主語が3人称単数（he / she / it / Ken / my mother など）のときだけ s / es をつける。",
                 "s・x・sh・ch・o で終わる語は es（goes, does, watches, washes, fixes）。",
                 "子音字＋y で終わる語は y を i にかえて es（studies, tries）。母音字＋y はそのまま s（plays, enjoys）。",
                 "have は例外で has。"],
                body="現在形は「いつもしていること（習慣）」や「今の状態・変わらない事実」を表します。Ken plays tennis after school. は「ケンは（ふだん）放課後にテニスをする」という意味です。",
                points=[tp("主語の後ろの動詞を見たら、まず「主語は3人称単数か」を確かめるくせをつけさせる。3人称単数を「he / she / it に置きかえられる主語」と言いかえると判断しやすい。",
                           ask="My sister を代名詞にかえると何になるか。そのとき動詞はどうなるか。", expect="she になるので3人称単数。動詞に s をつける。"),
                        tp("つづりの変化は、発音とあわせて練習する。watches・washes は「イズ」と1音節増えることを聞かせる。", timing="規則の説明直後")]),
        derivation("dv1", "否定文・疑問文の作り方（なぜ do / does が必要なのか）",
                   ["① be 動詞の文は、be 動詞が動ける。否定文は be 動詞の後ろに not（Ken is not busy.）、疑問文は be 動詞を主語の前に出す（Is Ken busy?）。",
                    "② 一般動詞の文には be 動詞がない。play などの一般動詞は、自分で前に出たり not を後ろにつけたりできない。",
                    "③ そこで、否定や疑問の「印」として助けの語 do を使う。否定文は do not（don't）を動詞の前に置き、疑問文は Do を文の先頭に置く（You don't play tennis. / Do you play tennis?）。",
                    "④ 主語が3人称単数のときは、do も3単現の形 does になる（Ken doesn't play tennis. / Does Ken play tennis?）。",
                    "⑤ does が3単現の s を引き受けたので、後ろの動詞は原形にもどる。s は1つの文に1つだけ（Does Ken plays ～? は誤り）。",
                    "⑥ 答えの文でも、聞かれたときと同じ語を使う。Is ～? には is / isn't、Does ～? には does / doesn't で答える。"],
                   body="この仕組みを知っていると、「be 動詞の文か、一般動詞の文か」を最初に判断するだけで、否定文・疑問文・答え方がすべて決まります。",
                   points=[tp("「does に s を取られたので、後ろの動詞は原形」というイメージを、plays → does play → Does ～ play? と矢印で板書して見せる。",
                              ask="Ken plays tennis. を疑問文にすると、plays の s はどこへ行くか。", expect="does の es になる。play は原形にもどる。",
                              timing="手順⑤の説明時")]),
        example("ex1", "例題1　be 動詞を選ぶ",
                "（　）に am / are / is のうち適切なものを入れなさい。(1) Tom and Emi (　) in the music room.　(2) My brother (　) good at cooking.　(3) I (　) from Osaka.",
                ["(1) 主語は Tom and Emi の2人なので複数 → are。", "(2) 主語は My brother の1人で、I でも you でもない3人称単数 → is。", "(3) 主語は I → am。"],
                "(1) are　(2) is　(3) am",
                thinking="be 動詞は主語で決まる。主語が何人（いくつ）か、I や you かを確かめる。",
                points=[tp("主語を代名詞に置きかえさせる（Tom and Emi → they、My brother → he）と、be 動詞が選びやすくなることを示す。")],
                misconceptions=[("Tom and Emi is in the music room.", "and で2人がつながっているので複数。are を使う。")]),
        example("ex2", "例題2　3単現の s をつける",
                "（　）内の動詞を適切な形にして、全文を書きなさい。(1) My sister (study) math after dinner.　(2) They (watch) TV in the morning.　(3) Ken (have) a dog.",
                ["(1) 主語 My sister は3人称単数。study は子音字＋y なので y を i にかえて es → studies。",
                 "(2) 主語 They は複数なので s はつけない → watch のまま。", "(3) 主語 Ken は3人称単数。have は例外で has。"],
                "(1) My sister studies math after dinner.　(2) They watch TV in the morning.　(3) Ken has a dog.",
                thinking="まず主語が3人称単数かを判断し、つけるときはつづりの規則を確かめる。",
                points=[tp("(2) のように「s をつけない」問題を必ず混ぜ、主語を見ずに s をつける習慣を防ぐ。", caution="「（　）内の語を変えなさい」と言われると、必ず形を変えようとする生徒がいる。")]),
        example("ex3", "例題3　否定文・疑問文に書きかえる",
                "次の文を (1) は否定文に、(2) は疑問文にして Yes で答えなさい。(1) Ms. Green speaks French.　(2) Your brother is busy today.",
                ["(1) speaks は一般動詞で、主語は3人称単数 → doesn't を動詞の前に置き、speaks を原形 speak にもどす。",
                 "(2) is は be 動詞 → is を主語の前に出す。答えは your brother を he で受けて is で答える。"],
                "(1) Ms. Green doesn't speak French.　(2) Is your brother busy today? ― Yes, he is.",
                thinking="最初に「be 動詞の文か、一般動詞の文か」を判断する。一般動詞なら do / does を使い、動詞は原形にする。",
                points=[tp("答えの文で your brother をそのまま使わず he で受けることを確認する（代名詞は次の単元で詳しく学ぶ）。")],
                misconceptions=[("Ms. Green doesn't speaks French.", "doesn't が3単現の s を引き受けるので、動詞は原形 speak。"),
                                ("Does your brother busy today?", "busy は動詞ではない。be 動詞の文なので Is ～? とする。")]),
        board("bd1", "板書案",
              [("① be 動詞", ["I → am", "you・複数 → are", "3人称単数 → is", "主語＝後ろの語句／～にいる", "否定：be＋not　疑問：be を前へ"]),
               ("② 一般動詞・3単現", ["I / you / 複数 → 原形 play", "3人称単数 → plays", "es：goes watches washes", "ies：studies tries", "have → has"]),
               ("③ 否定文・疑問文", ["一般動詞は do / does を借りる", "don't / doesn't＋原形", "Do / Does＋主語＋原形 ～?", "plays → does play（s は1つ）", "答えは同じ語で：Does ～? → does"])],
              points=[tp("板書は3列に分け、①と③を比べて「be 動詞の文は be 動詞が動く、一般動詞の文は do / does を使う」という対比が一目でわかるようにする。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("英文を見たら「be 動詞の文か一般動詞の文か」「主語は3人称単数か」の2つを、毎回声に出して確認させる。", ask="Tom and Emi play tennis. の主語は3人称単数か。", expect="2人なので複数。s はつけない。"),
               tp("be 動詞と一般動詞を並べる誤り（I am play ～.）は、日本語の「です・ます」を英語に置きかえようとすることから生まれると説明する。", caution="特に入学直後に多い。早めに例文で比べさせる。"),
               tp("does を使ったら動詞は原形、という規則は「s は1つの文に1つだけ」と短く言いかえて定着させる。", timing="例題3の後"),
               tp("答えの文では、名詞の主語を代名詞（he / she / they）で受けることを、会話練習の中で何度も使わせる。"),
               tp("問題プリント D の誤答例を使い、「s のつけ忘れ」「s のつけすぎ」「be 動詞と do の混同」の3種類に分けて整理させる。")],
              misconceptions=[("I am play soccer every day.", "一般動詞 play があるので be 動詞は不要。I play soccer every day."),
                              ("Ken don't like Japanese food.", "主語が3人称単数なので doesn't。Ken doesn't like Japanese food."),
                              ("Are you like music?", "like は一般動詞なので Do で始める。Do you like music?")]),
        summary("sm1", "まとめ",
                ["be 動詞は主語に合わせて am（I）／ are（you・複数）／ is（3人称単数）を使う。",
                 "一般動詞は、主語が3人称単数で現在の文のときだけ s / es をつける（studies, goes, has などのつづりに注意）。",
                 "否定文・疑問文は、be 動詞の文なら be 動詞を使い、一般動詞の文なら do / does を使って動詞を原形にする。"]),
        check("ck1", "確認問題",
              [("My parents (　) from Osaka. の（　）に入る be 動詞を答えなさい。", "are（主語 My parents は複数）"),
               ("Ken watches TV in the morning. を否定文にしなさい。", "Ken doesn't watch TV in the morning."),
               ("Do you and Ken like Japanese food? に Yes で答えなさい。", "Yes, we do.（you and Ken には we で答える）")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

BE_WHY = {"am": "am は主語が I のときだけ使う", "are": "are は主語が you のとき、または主語が複数のときに使う",
          "is": "is は主語が3人称単数（I・you 以外の1人・1つ）のときに使う",
          "be": "be は原形で、現在の文では主語に合わせて am / are / is のどれかに形を変える"}


@gen("basic_check", 4, ["computation", "concept"])
def choose_be(r):
    S = r.choice(SUBJ)
    C = r.choice(BC)
    ok = be(S[1])
    why = {w: (f"{BE_WHY[w]}。主語 {S[0]} は{KIND_DESC[S[1]]}なので {ok} を使う。", "主語と be 動詞の組み合わせの混同")
           for w in ("am", "are", "is", "be") if w != ok}
    return mc(f"日本語の意味になるように、（　）に入る be 動詞として正しいものを選びなさい。\n{jp(S, C)}\n{S[0]} (　) {C[0]}.",
              [ok] + [w for w in ("am", "are", "is", "be") if w != ok],
              f"主語 {S[0]} は{KIND_DESC[S[1]]}なので {ok}。{be_aff(S, C)}", d=1,
              ap="be 動詞は主語で決まる。主語が I か、you か、3人称単数か、複数かを確かめる。",
              steps=[f"主語を確認する：{S[0]}。", f"主語の種類を判断する：{KIND_DESC[S[1]]}。", f"I → am、you・複数 → are、3人称単数 → is の規則から {ok} を選ぶ。"],
              alt=["主語を代名詞（I / you / he / she / we / they）に置きかえてから be 動詞を選ぶと確かめやすい。"],
              pc=[("主語の種類を正しく判断している", 1), ("正しい be 動詞を選んでいる", 1)],
              pit=["and でつながった主語（Yuki and I など）を単数と考える。", "My parents のような複数形の主語に is を使う。"], why=why)


@gen("basic_check", 4, ["computation", "condition_check"])
def verb_in_sentence(r):
    form = r.choice(["aff", "aff", "neg", "q"])
    S = r.choice(QSUBJ if form == "q" else SUBJ)
    V = pick_v(r)
    if form == "aff":
        ans = vform(S, V)
        s = f"{S[0]} ({V[0]}) {rest(V)}."
        why_s = (f"主語 {S[0]} は3人称単数なので、{V[0]} を3単現の形 {ans} にする。" if S[1] == "3s"
                 else f"主語 {S[0]} は{KIND_DESC[S[1]]}なので、s はつけず原形 {ans} のまま。")
        J = jp(S, V)
    elif form == "neg":
        aux = "doesn't" if S[1] == "3s" else "don't"
        ans = V[0]
        s = f"{S[0]} {aux} ({V[0]}) {rest(V)}."
        why_s = f"{aux} の後ろの動詞は、主語に関係なく原形 {V[0]} にする。"
        J = jp(S, V, neg=True)
    else:
        ans = V[0]
        s = f"{cap(do(S[1]))} {low(S[0])} ({V[0]}) {rest(V)}?"
        why_s = f"{cap(do(S[1]))} で始まる疑問文では、動詞は原形 {V[0]} にする。"
        J = jp(S, V, q=True)
    return sa(f"日本語の意味になるように、（　）内の動詞を適切な形に直しなさい。形を変える必要がないときは、そのまま書きなさい。\n{J}\n{s}", ans,
              why_s, d=2,
              ap="①主語が3人称単数か、②動詞の前に do / does / don't / doesn't があるか、の2点を確かめる。",
              steps=["主語を確認し、3人称単数かどうかを判断する。", "動詞の前に do / does / don't / doesn't があるかを確かめる（あれば原形）。", f"答え：{ans}"],
              alt=["主語を he / she / they などの代名詞に置きかえて、He plays / They play のどちらの形になるかを口に出して確かめる。"],
              pc=[("主語と文の形（肯定・否定・疑問）を正しく判断している", 1), ("正しい形を書いている", 1)],
              pit=["主語を見ずに必ず s をつけてしまう。", "doesn't や Does の後ろの動詞にも s をつけてしまう。"])


@gen("basic_check", 4, ["computation"])
def spell_3s(r):
    base, s3, m, rule = r.choice(SPELL)
    return sa(f"次の動詞を、主語が3人称単数で現在の文のときの形（3単現の形）にしなさい。\n{base}（{m}）", s3,
              f"{rule}ので {s3}。", d=1,
              ap="語の終わりのつづり（s・x・sh・ch・o か、y か、それ以外か）を見て、s・es・ies のどれをつけるかを決める。have だけは例外。",
              steps=[f"語の終わりを確認する：{base}。", f"規則を当てはめる：{rule}。", f"答え：{s3}"],
              alt=["He で始まる短い文（He " + s3 + " ～.）を作って声に出し、発音とつづりが合っているかを確かめる。"],
              pc=[("つづりの規則を正しく選んでいる", 1), ("正しいつづりで書いている", 1)],
              pit=["子音字＋y と母音字＋y を区別せず、plaies や studys とする。", "go・do に s だけをつけて gos・dos とする。"])


@gen("basic_check", 4, ["condition_check", "common_error"])
def be_or_do(r):
    S = r.choice(QSUBJ)
    typ = r.choice(["q_be", "q_gv", "n_be", "n_gv"])
    if typ in ("q_be", "n_be"):
        C = r.choice(BC)
        if typ == "q_be":
            ok = cap(be(S[1]))
            stem = f"(　) {low(S[0])} {C[0]}?"
            J = jp(S, C, q=True)
            cands = ["Is", "Are", "Do", "Does"]
        else:
            ok = be_neg(S[1])
            stem = f"{S[0]} (　) {C[0]}."
            J = jp(S, C, neg=True)
            cands = [ok, "isn't" if ok != "isn't" else "aren't", "don't", "doesn't"]
        kindtxt = "be 動詞の文"
    else:
        V = pick_v(r)
        if typ == "q_gv":
            ok = cap(do(S[1]))
            stem = f"(　) {low(S[0])} {V[0]} {rest(V)}?"
            J = jp(S, V, q=True)
            cands = ["Do", "Does", "Is", "Are"]
        else:
            ok = "doesn't" if S[1] == "3s" else "don't"
            stem = f"{S[0]} (　) {V[0]} {rest(V)}."
            J = jp(S, V, neg=True)
            cands = ["don't", "doesn't", "isn't", "aren't"]
        kindtxt = f"一般動詞 {V[0]} の文"
    wrongs = [c for c in cands if c != ok]
    why = {}
    for w in wrongs:
        isbe_w = w.lower().startswith(("is", "are", "am"))
        isbe_ok = ok.lower().startswith(("is", "are", "am"))
        if isbe_w != isbe_ok:
            why[w] = (f"この文は{kindtxt}である。{'一般動詞の文では be 動詞ではなく do / does を使う' if isbe_w else 'be 動詞の文では do / does は使わず、be 動詞そのものを使う'}。",
                      "be 動詞の文と一般動詞の文の混同")
        else:
            why[w] = (f"主語 {S[0]} は{KIND_DESC[S[1]]}なので {ok} を使う。{w} は主語と合わない。", "主語と動詞の形の一致の誤り")
    return mc(f"日本語の意味になるように、（　）に入る最も適切なものを選びなさい。\n{J}\n{stem}", [ok] + wrongs,
              f"{kindtxt}で、主語 {S[0]} は{KIND_DESC[S[1]]}なので {ok}。", d=2,
              ap="まず be 動詞の文か一般動詞の文かを決め、次に主語に合う形を選ぶ。",
              steps=["（　）の後ろに一般動詞の原形があるかを確かめる。あれば do / does、なければ be 動詞を使う。", f"主語 {S[0]} の種類（{KIND_DESC[S[1]]}）から形を決める。", f"答え：{ok}"],
              alt=["選んだ語で肯定文にもどしてみて（例：Does ～ play? → ～ plays.）、もとの文として正しいかを確かめる。"],
              pc=[("be 動詞の文か一般動詞の文かを正しく判断している", 1), ("主語に合う形を選んでいる", 1)],
              pit=["一般動詞の疑問文を Are you ～? で始める。", "主語が3人称単数なのに don't を使う。"], why=why)


@gen("basic_check", 4, ["concept", "condition_check"])
def answer_reply(r):
    S = r.choice(QSUBJ)
    pron = S[3]
    isbe = r.random() < 0.5
    yes = r.random() < 0.5
    if isbe:
        C = r.choice(BC)
        qs = be_q(S, C)
    else:
        V = pick_v(r)
        qs = gv_q(S, V)
    ok = short(pron, isbe, yes)
    swap = short(pron, not isbe, yes)
    wrong_p = {"I": "you", "he": "she", "she": "he", "we": "they", "they": "he"}[pron]
    if wrong_p == "you":
        wp_text = f"Yes, you {'are' if isbe else 'do'}." if yes else f"No, you {'aren' if isbe else 'don'}'t."
    else:
        wp_text = short(wrong_p, isbe, yes)
    if yes:
        pol = f"Yes, {pron} {'am' if (isbe and pron == 'I') else ('is' if (isbe and PRON_KIND[pron] == '3s') else 'are' if isbe else do(PRON_KIND[pron]))}n't."
        pol = pol.replace("amn't", "am not")
    else:
        pol = f"No, {pron} {(be(PRON_KIND[pron]) if isbe else do(PRON_KIND[pron]))}."
    pron_reason = {"I": "you（あなた）と聞かれたら、答える人は自分のことなので I で答える",
                   "he": f"{S[0]} は男性1人なので he で受ける", "she": f"{S[0]} は女性1人なので she で受ける",
                   "we": "you and Ken と聞かれたら、答える人は自分をふくむ2人なので we で答える",
                   "they": f"{S[0]} は2人なので they で受ける"}[pron]
    why = {swap: (f"{'be 動詞' if isbe else 'do / does'}で聞かれた質問には、同じ{'be 動詞' if isbe else 'do / does'}で答える。", "be 動詞の文と一般動詞の文の混同"),
           wp_text: (f"{pron_reason}。", "答えの文の代名詞の選び方の誤り"),
           pol: ("Yes の後ろは肯定、No の後ろは否定の形にそろえる。", "Yes / No と肯定・否定の対応の誤り")}
    return mc(f"次の質問に対する答えとして、文法的に正しいものを選びなさい。\n{qs}", [ok, swap, wp_text, pol],
              f"{ok} が正しい。{pron_reason}。{'be 動詞' if isbe else 'do / does'}で聞かれているので、同じ語で答える。", d=2,
              ap="①質問の最初の語（be 動詞か do / does か）、②主語を受ける代名詞、③Yes なら肯定・No なら否定、の3点を確かめる。",
              steps=[f"質問の最初の語を確認する：{qs.split()[0]}。", f"主語 {low(S[0])} を受ける代名詞を決める：{pron}。", "Yes / No と肯定・否定がそろっているかを確かめる。", f"答え：{ok}"],
              alt=["答えの文を完全な文にのばしてみる（例：Yes, he is busy.）と、代名詞と動詞の形が正しいか確かめやすい。"],
              pc=[("質問と同じ種類の語で答えている", 1), ("代名詞と肯定・否定が正しい", 1)],
              pit=["Is ～? の質問に does で答える。", "you で聞かれたのに you で答える。"], why=why)


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 4, ["computation", "condition_check"])
def make_negative(r):
    S = r.choice(SUBJ)
    if r.random() < 0.45:
        C = r.choice(BC)
        src, ans, full = be_aff(S, C), be_neg_s(S, C), be_neg_s(S, C, full=True)
        how = f"be 動詞 {be(S[1])} の後ろに not を置く。"
        J = jp(S, C, neg=True)
    else:
        V = pick_v(r)
        src, ans, full = gv_aff(S, V), gv_neg(S, V), gv_neg(S, V, full=True)
        how = (f"一般動詞の文で主語が3人称単数なので、doesn't（does not）を動詞の前に置き、{V[1]} を原形 {V[0]} にもどす。" if S[1] == "3s"
               else f"一般動詞の文なので、don't（do not）を動詞 {V[0]} の前に置く。")
        J = jp(S, V, neg=True)
    v = [full] if full != ans else []
    return sa(f"次の英文を否定文に書きかえなさい。\n{src}\n（意味：{J}）", ans, f"{how}{ans}", d=2, v=v,
              ap="まず be 動詞の文か一般動詞の文かを判断する。be 動詞なら後ろに not、一般動詞なら don't / doesn't を使う。",
              steps=["文の動詞が be 動詞か一般動詞かを確かめる。", how, f"答え：{ans}" + (f"（{full} も可）" if v else "")],
              alt=["書きかえた否定文を肯定文にもどしてみて、もとの文と一致するかを確かめる。"],
              pc=[("be 動詞・一般動詞の区別に応じた否定の形にしている", 2), ("動詞の形（原形・be 動詞の形）が正しい", 2)],
              pit=["一般動詞の文に be 動詞の not を入れる（Ken is not play ～.）。", "doesn't の後ろの動詞に s を残す。"])


@gen("standard_practice", 4, ["computation", "concept"])
def make_question(r):
    S = r.choice(QSUBJ)
    yes = r.random() < 0.5
    pron = S[3]
    if r.random() < 0.45:
        C = r.choice(BC)
        q = be_q(S, C)
        isbe = True
        how = f"be 動詞 {be(S[1])} を主語の前に出す。"
    else:
        V = pick_v(r)
        q = gv_q(S, V)
        isbe = False
        how = (f"主語が3人称単数なので Does を文頭に置き、{V[1]} を原形 {V[0]} にもどす。" if S[1] == "3s"
               else f"一般動詞の文なので Do を文頭に置く。")
    src = (be_aff(S, C) if isbe else gv_aff(S, V))
    a2 = short(pron, isbe, yes)
    ans = f"{q}　{a2}"
    note = "（主語の You は質問では you のまま。答えるときは I にかえる）" if S[0] == "You" else ""
    return sa(f"次の英文を疑問文に書きかえ、その疑問文に {'Yes' if yes else 'No'} で答える文も書きなさい。{note}\n{src}", ans,
              f"{how}答えは {low(S[0])} を {pron} で受け、{'be 動詞' if isbe else 'do / does'}を使う。{ans}", d=3,
              ap="疑問文の作り方は be 動詞の文と一般動詞の文で違う。答えの文は、質問の最初の語と同じ種類の語を使い、主語は代名詞で受ける。",
              steps=["be 動詞の文か一般動詞の文かを判断する。", how, f"答えの文：主語を {pron} で受けて {a2}"],
              alt=["答えの文を完全な文（例：Yes, he plays tennis.）にのばしてみて、肯定・否定と動詞の形が合っているかを確かめる。"],
              pc=[("正しい疑問文を作っている", 2), ("正しい答えの文を書いている", 2)],
              pit=["Does の後ろの動詞に s を残す。", "答えの文で主語をそのまま繰り返したり、you で答えたりする。"])


@gen("standard_practice", 4, ["computation", "application"])
def change_subject(r):
    form = r.choice(["aff", "aff", "neg", "q"])
    if form == "q":
        S1 = ("You", "2", "あなたは", "I")
        S2 = r.choice([s for s in QSUBJ if s[0] != "You"])
    else:
        if r.random() < 0.5:
            S1 = r.choice([s for s in SUBJ if s[1] in ("1s", "pl")])
            S2 = r.choice(NAMED3)
        else:
            S1 = r.choice(NAMED3)
            S2 = r.choice([s for s in SUBJ if s[1] in ("1s", "pl") and s[0] not in ("You and Ken",)])
    isbe = r.random() < 0.4
    X = r.choice(BC) if isbe else pick_v(r)
    if form == "aff":
        f = be_aff if isbe else gv_aff
    elif form == "neg":
        f = be_neg_s if isbe else gv_neg
    else:
        f = be_q if isbe else gv_q
    src, ans = f(S1, X), f(S2, X)
    marked = src.replace(S1[0], f"[[u:{S1[0]}]]", 1) if form != "q" else src.replace(f" {low(S1[0])} ", f" [[u:{low(S1[0])}]] ", 1)
    sub2 = S2[0] if form != "q" else low(S2[0])
    v = []
    if form == "neg":
        v = [(be_neg_s if isbe else gv_neg)(S2, X, full=True)]
        if v[0] == ans:
            v = []
    if isbe:
        what = f"be 動詞を主語 {S2[0]} に合わせて {be(S2[1])}（否定なら {be_neg(S2[1])}）にする"
    elif form == "aff":
        what = f"主語 {S2[0]} は{KIND_DESC[S2[1]]}なので、動詞は {vform(S2, X)}"
    else:
        what = f"主語 {S2[0]} は{KIND_DESC[S2[1]]}なので、{do(S2[1])} を使い、動詞は原形 {X[0]} のまま"
    return sa(f"下線部を（　）内の語句にかえて、全文を書きかえなさい。\n{marked}　（{sub2}）", ans, f"{what}。{ans}", d=3, v=v,
              ap="主語がかわると、be 動詞の形、3単現の s、do と does の使い分けがかわる。主語の種類を先に判断する。",
              steps=[f"新しい主語 {S2[0]} の種類を判断する：{KIND_DESC[S2[1]]}。", f"{what}。", f"答え：{ans}"],
              alt=["新しい主語を代名詞（he / she / they など）に置きかえてから、動詞の形を決めると確かめやすい。"],
              pc=[("新しい主語の種類を正しく判断している", 2), ("動詞（be 動詞・do / does・3単現）の形が正しい", 2)],
              pit=["主語を3人称単数にかえたのに、動詞の s をつけ忘れる。", "主語を複数にかえたのに、doesn't や is を残す。"])


@gen("standard_practice", 4, ["application", "computation"])
def build_order(r):
    form = r.choice(["aff", "neg", "q"])
    S = r.choice(QSUBJ if form == "q" else SUBJ)
    isbe = r.random() < 0.35
    X = r.choice(BC) if isbe else pick_v(r)
    subj_parts = [low(S[0])]
    if isbe:
        tail = [X[0]]
        if form == "aff":
            parts = subj_parts + [be(S[1])] + tail
        elif form == "neg":
            parts = subj_parts + [be(S[1]), "not"] + tail
        else:
            parts = [be(S[1])] + subj_parts + tail
        J = jp(S, X, neg=form == "neg", q=form == "q")
    else:
        tail = list(X[2])
        if form == "aff":
            parts = subj_parts + [vform(S, X)] + tail
        elif form == "neg":
            parts = subj_parts + [do(S[1]), "not", X[0]] + tail
        else:
            parts = [do(S[1])] + subj_parts + [X[0]] + tail
        J = jp(S, X, neg=form == "neg", q=form == "q")
    sent = " ".join(parts)
    sent = cap(sent) + ("?" if form == "q" else ".")
    return order(f"日本語の意味を表す英文になるように、次の語句を正しい順に並べなさい。文の最初にくる語も小文字で示してある。\n{J}", parts,
                 f"{sent}　{'be 動詞の文' if isbe else '一般動詞の文'}の{'肯定文' if form == 'aff' else '否定文' if form == 'neg' else '疑問文'}の語順。", d=3, p=4,
                 ap="be 動詞の文か一般動詞の文かを確かめてから、肯定文・否定文・疑問文の語順の型に当てはめる。",
                 steps=["与えられた語句に be 動詞と do / does のどちらがあるかを確かめる。",
                        "否定文なら not の位置（be 動詞の後ろ／do・does の後ろ）、疑問文なら文頭の語を決める。", f"完成文：{sent}"],
                 alt=["完成した英文を日本語に訳し直して、問題の日本語と一致するかを確かめる。"],
                 pc=[("主語と動詞（be 動詞・do / does）の位置が正しい", 2), ("残りの語句の順序が正しい", 2)],
                 pit=["疑問文で do / does を文頭に置かず、主語から始めてしまう。", "not を一般動詞の後ろに置く。"])


def make_error(kind, r):
    """よくある誤りの文を作る。戻り値：dict(wrong, fix, jp, where, type, rule, tempt)"""
    if kind == "no_s":
        S, V = r.choice(S3), pick_v(r)
        return dict(wrong=f"{S[0]} {V[0]} {rest(V)}.", fix=gv_aff(S, V), jp=jp(S, V), where=V[0], type="condition",
                    rule=f"主語 {S[0]} は3人称単数なので、動詞を3単現の形 {V[1]} にする",
                    tempt="主語が I や you のときと同じ形のまま書き、主語の人称と数を確かめなかった。")
    if kind == "pl_s":
        S, V = r.choice(SPL), pick_v(r)
        return dict(wrong=f"{S[0]} {V[1]} {rest(V)}.", fix=gv_aff(S, V), jp=jp(S, V), where=V[1], type="condition",
                    rule=f"主語 {S[0]} は複数なので、動詞に s をつけず原形 {V[0]} のままにする",
                    tempt="主語が人の名前や名詞なら s をつけると思い込み、主語が2人以上であることを見落とした。")
    if kind == "does_s":
        S, V = r.choice(Q3), pick_v(r)
        return dict(wrong=f"Does {low(S[0])} {V[1]} {rest(V)}?", fix=gv_q(S, V), jp=jp(S, V, q=True), where=V[1], type="concept",
                    rule=f"Does が3単現の s を引き受けるので、後ろの動詞は原形 {V[0]} にする",
                    tempt="主語が3人称単数なので動詞にも s が必要だと考え、does と動詞の両方に s をつけた。")
    if kind == "doesnt_s":
        S, V = r.choice(S3), pick_v(r)
        return dict(wrong=f"{S[0]} doesn't {V[1]} {rest(V)}.", fix=gv_neg(S, V), jp=jp(S, V, neg=True), where=V[1], type="concept",
                    rule=f"doesn't の後ろの動詞は原形 {V[0]} にする（s は doesn't が引き受ける）",
                    tempt="肯定文の形 " + V[1] + " をそのまま残して、前に doesn't を加えただけにした。")
    if kind == "dont_3s":
        S, V = r.choice(S3), pick_v(r)
        return dict(wrong=f"{S[0]} don't {V[0]} {rest(V)}.", fix=gv_neg(S, V), jp=jp(S, V, neg=True), where="don't", type="condition",
                    rule=f"主語 {S[0]} は3人称単数なので、don't ではなく doesn't を使う",
                    tempt="「否定は don't」とだけ覚えていて、主語によって doesn't になることを忘れた。")
    if kind == "spell":
        S = r.choice(S3)
        V = r.choice([v for v in VP if v[0] in SPECIAL])
        bad, rule = SPECIAL[V[0]]
        return dict(wrong=f"{S[0]} {bad} {rest(V)}.", fix=gv_aff(S, V), jp=jp(S, V), where=bad, type="notation",
                    rule=f"{rule}ので {V[1]} とする",
                    tempt="3単現は「s をつける」とだけ覚えていて、語の終わりのつづりによる変化を確かめなかった。")
    if kind == "be_gv":
        S, V = r.choice(SUBJ), pick_v(r)
        return dict(wrong=f"{S[0]} {be(S[1])} {vform(S, V)} {rest(V)}.", fix=gv_aff(S, V), jp=jp(S, V), where=be(S[1]), type="concept",
                    rule=f"一般動詞 {V[0]} があるので be 動詞は不要。be 動詞と一般動詞はふつう1つの文に並べない",
                    tempt="日本語の「～します」「～です」を be 動詞で表そうとして、主語の後ろに必ず be 動詞を置いた。")
    if kind == "be_q_gv":
        S, V = r.choice(QSUBJ), pick_v(r)
        return dict(wrong=f"{cap(be(S[1]))} {low(S[0])} {V[0]} {rest(V)}?", fix=gv_q(S, V), jp=jp(S, V, q=True), where=cap(be(S[1])), type="concept",
                    rule=f"一般動詞 {V[0]} の文の疑問文は、be 動詞ではなく {cap(do(S[1]))} を文頭に置く",
                    tempt="「疑問文は be 動詞を前に出す」という be 動詞の文の規則を、一般動詞の文にも当てはめた。")
    if kind == "be_neg_gv":
        S, V = r.choice(SUBJ), pick_v(r)
        return dict(wrong=f"{S[0]} {be(S[1])} not {V[0]} {rest(V)}.", fix=gv_neg(S, V), jp=jp(S, V, neg=True), where=f"{be(S[1])} not", type="concept",
                    rule=f"一般動詞 {V[0]} の文の否定文は、be 動詞＋not ではなく {'doesn' if S[1] == '3s' else 'don'}'t を動詞の前に置く",
                    tempt="「否定文は not を入れる」とだけ考え、be 動詞の文の形をそのまま使った。")
    if kind == "do_q_be":
        S, C = r.choice(QSUBJ), r.choice(BC)
        return dict(wrong=f"{cap(do(S[1]))} {low(S[0])} {C[0]}?", fix=be_q(S, C), jp=jp(S, C, q=True), where=cap(do(S[1])), type="concept",
                    rule=f"{C[0]} の中に一般動詞はない。be 動詞の文なので、be 動詞 {be(S[1])} を主語の前に出す",
                    tempt="「疑問文は Do / Does で始める」と思い込み、be 動詞の文でも Do / Does を使った。")
    if kind == "do_neg_be":
        S, C = r.choice(SUBJ), r.choice(BC)
        dd = "doesn't" if S[1] == "3s" else "don't"
        return dict(wrong=f"{S[0]} {dd} {C[0]}.", fix=be_neg_s(S, C), jp=jp(S, C, neg=True), where=dd, type="concept",
                    rule=f"{C[0]} は動詞ではないので be 動詞の文。否定文は be 動詞の後ろに not を置く",
                    tempt="日本語の「～ではありません」「～していません」を、まとめて don't / doesn't で表そうとした。")
    # be_agree
    S, C = r.choice([s for s in SUBJ if s[1] != "2"]), r.choice(BC)
    ok = be(S[1])
    bad = {"am": "is", "is": "are", "are": "is"}[ok] if S[0] != "Yuki and I" else "am"
    return dict(wrong=f"{S[0]} {bad} {C[0]}.", fix=be_aff(S, C), jp=jp(S, C), where=bad, type="condition",
                rule=f"主語 {S[0]} は{KIND_DESC[S[1]]}なので、be 動詞は {ok}",
                tempt=("主語に I がふくまれているので am を選んだが、Yuki and I は2人で複数である。" if S[0] == "Yuki and I"
                       else "主語が何人（いくつ）か、I や you かを確かめずに be 動詞を選んだ。"))


ERR_LABEL = {"no_s": "3単現の s のつけ忘れ", "pl_s": "複数の主語に s をつける誤り", "does_s": "Does の後ろの動詞に s をつける誤り",
             "doesnt_s": "doesn't の後ろの動詞に s をつける誤り", "dont_3s": "3人称単数の主語に don't を使う誤り", "spell": "3単現のつづりの誤り",
             "be_gv": "be 動詞と一般動詞を並べる誤り", "be_q_gv": "一般動詞の疑問文を be 動詞で始める誤り", "be_neg_gv": "一般動詞の否定文に be 動詞＋not を使う誤り",
             "do_q_be": "be 動詞の疑問文を Do / Does で始める誤り", "do_neg_be": "be 動詞の否定文に don't / doesn't を使う誤り", "be_agree": "主語と be 動詞の組み合わせの誤り"}


@gen("standard_practice", 4, ["common_error", "concept"])
def correct_sentence(r):
    form = r.choice(["aff", "neg", "q"])
    S = r.choice(QSUBJ if form == "q" else SUBJ)
    isbe = r.random() < 0.4
    X = r.choice(BC) if isbe else pick_v(r)
    f = {("aff", True): be_aff, ("neg", True): be_neg_s, ("q", True): be_q, ("aff", False): gv_aff, ("neg", False): gv_neg, ("q", False): gv_q}[(form, isbe)]
    ok = f(S, X)
    kinds = r.sample(list(ERR_LABEL), 3)
    errs = [make_error(k, r) for k in kinds]
    texts = [e["wrong"] for e in errs]
    if len(set(texts + [ok])) < 4:
        errs = [make_error(k, local(ok + k)) for k in kinds]
        texts = [e["wrong"] for e in errs]
    why = {e["wrong"]: (f"{e['rule']}。正しくは {e['fix']}", ERR_LABEL[k]) for e, k in zip(errs, kinds)}
    return mc("次の英文のうち、文法的に正しいものを1つ選びなさい。", [ok] + texts,
              f"{ok} が正しい。ほかの3つは、" + "／".join(ERR_LABEL[k] for k in kinds) + " をふくんでいる。", d=3,
              ap="それぞれの文について、①be 動詞の文か一般動詞の文か、②主語は3人称単数か、③do / does の後ろは原形か、を順に確かめる。",
              steps=["各選択肢の動詞を見つけ、be 動詞の文か一般動詞の文かを判断する。", "主語と動詞の形（am / are / is、s の有無、do / does）が合っているかを確かめる。",
                     f"すべての条件を満たす {ok} を選ぶ。"],
              alt=["誤りだと思った選択肢を正しく直してみる。直せる箇所がはっきり言えれば、その選択肢は誤りだと確信できる。"],
              pc=[("誤りの選択肢の誤りを見抜いている", 2), ("正しい文を選んでいる", 2)],
              pit=["文全体の意味だけで判断し、動詞の形を確かめない。"], why=why)


# ======================================================================
# C 思考力・記述応用
# ======================================================================

@gen("thinking_writing", 4, ["written_reasoning", "condition_check"])
def explain_blanks(r):
    typ = r.choice(["q_gv", "neg_gv", "be_ans", "gv_ans"])
    S = r.choice(QSUBJ)
    pron = S[3]
    if typ == "q_gv":
        V = pick_v(r)
        a1, a2 = cap(do(S[1])), V[0]
        s = f"(　①　) {low(S[0])} (　②　) {rest(V)}?　［②には {V[0]} を適切な形にして入れる］"
        model = (f"①{a1}　②{a2}。{V[0]} は一般動詞なので、疑問文は be 動詞ではなく do / does を文頭に置く。主語 {S[0]} は{KIND_DESC[S[1]]}なので {do(S[1])} を使う。"
                 + ("does が3単現の s を引き受けるので、②の動詞は原形 " + V[0] + " にする。" if S[1] == "3s" else "do で始まる疑問文の動詞は原形のまま " + V[0] + " にする。"))
    elif typ == "neg_gv":
        S = r.choice(SUBJ)
        V = pick_v(r)
        a1 = "doesn't" if S[1] == "3s" else "don't"
        a2 = V[0]
        s = f"{S[0]} (　①　) (　②　) {rest(V)}.　［「～しない」という意味にする。②には {V[0]} を適切な形にして入れる］"
        model = (f"①{a1}　②{a2}。{V[0]} は一般動詞なので、否定文は be 動詞＋not ではなく don't / doesn't を動詞の前に置く。主語 {S[0]} は{KIND_DESC[S[1]]}なので {a1} を使い、"
                 + "その後ろの動詞は原形 " + V[0] + " にする" + ("（s は doesn't が引き受ける）。" if S[1] == "3s" else "。"))
    elif typ == "be_ans":
        C = r.choice(BC)
        a1 = cap(be(S[1]))
        a2 = "not" if pron == "I" else be_neg(PRON_KIND[pron])
        tail = "No, I'm (　②　)." if pron == "I" else f"No, {pron} (　②　)."
        s = f"(　①　) {low(S[0])} {C[0]}? ― {tail}"
        model = (f"①{a1}　②{a2}。{C[0]} の中に一般動詞はないので be 動詞の文である。主語 {low(S[0])} は{KIND_DESC[S[1]]}なので be 動詞は {be(S[1])} で、疑問文では文頭に出す。"
                 f"答えは {low(S[0])} を {pron} で受け、No の後ろなので否定の形 {('I' + chr(39) + 'm not') if pron == 'I' else pron + ' ' + a2} にする。")
    else:
        V = pick_v(r)
        a1 = cap(do(S[1]))
        a2 = do(PRON_KIND[pron])
        s = f"(　①　) {low(S[0])} {V[0]} {rest(V)}? ― Yes, {pron} (　②　)."
        model = (f"①{a1}　②{a2}。{V[0]} は一般動詞なので疑問文は do / does を文頭に置く。主語 {low(S[0])} は{KIND_DESC[S[1]]}なので {do(S[1])}。"
                 f"答えでは {low(S[0])} を {pron} で受け、質問と同じく do / does を使って {pron} に合う形 {a2} にする。")
    return desc(f"次の英文の（①）（②）に入る語をそれぞれ1語で答えなさい。また、その語を選んだ理由を、「be 動詞の文か一般動詞の文か」「主語の種類」の2点に触れて説明しなさい。\n{s}",
                model, "最初に be 動詞の文か一般動詞の文かを判断し、次に主語の種類から形を決める。疑問文・否定文の do / does の後ろの動詞は原形。",
                [("①の語が正しい", 2), ("②の語が正しい", 2), ("be 動詞の文か一般動詞の文かの判断を説明している", 2), ("主語の種類に触れて説明している", 2)], d=4, p=8, lines=5,
                ap="文の中に一般動詞があるかを先に確かめる。あれば do / does、なければ be 動詞。その後で主語の種類（I・you・3人称単数・複数）から形を決める。",
                steps=["文の中に一般動詞があるかを確かめ、be 動詞の文か一般動詞の文かを決める。", "主語の種類を判断する。", "①②に入る語を決め、理由を2点に分けて書く。"],
                alt=["答えを入れた文を肯定文にもどしてみて（例：Does Ken play ～? → Ken plays ～.）、もとの文として自然かを確かめる。"],
                pc=[("①の語", 2), ("②の語", 2), ("文の種類の判断の説明", 2), ("主語の種類の説明", 2)],
                pit=["理由として「疑問文だから」とだけ書き、be 動詞の文か一般動詞の文かに触れない。", "Does の後ろの動詞にも s をつける。"])


PRON_OF = {"Ken": "he", "My brother": "he", "Mr. Sato": "he", "Ms. Green": "she", "My sister": "she", "Tom and Emi": "they", "My parents": "they"}


@gen("thinking_writing", 3, ["cross_unit", "written_reasoning"], rel=["JH-ENG-G1-U02"])
def pronoun_rewrite(r):
    S = r.choice([s for s in SUBJ if s[0] in PRON_OF])
    pron = PRON_OF[S[0]]
    P = (cap(pron), PRON_KIND[pron], "", pron)
    form = r.choice(["q", "neg"])
    isbe = r.random() < 0.4
    X = r.choice(BC) if isbe else pick_v(r)
    src = (be_aff if isbe else gv_aff)(S, X).replace(S[0], f"[[u:{S[0]}]]", 1)
    if form == "q":
        ans = (be_q if isbe else gv_q)(P, X)
        how = (f"be 動詞の文なので、{be(P[1])} を主語 {pron} の前に出す" if isbe else
               f"一般動詞の文なので、{cap(do(P[1]))} を文頭に置き、動詞は原形 {X[0]} にする")
        what = "疑問文"
    else:
        ans = (be_neg_s if isbe else gv_neg)(P, X)
        how = (f"be 動詞の文なので、{be(P[1])} の後ろに not を置く" if isbe else
               f"一般動詞の文なので、{'doesn' if P[1] == '3s' else 'don'}'t を動詞の前に置き、動詞は原形 {X[0]} にする")
        what = "否定文"
    full = (be_neg_s if isbe else gv_neg)(P, X, full=True) if form == "neg" else None
    num = "2人なので複数" if pron == "they" else ("男性1人なので3人称単数" if pron == "he" else "女性1人なので3人称単数")
    model = f"{ans}　{S[0]} は{num}で、代名詞は {pron}。{how}。"
    return desc(f"次の英文の下線部を1語の代名詞にかえたうえで、全文を{what}に書きかえなさい。また、be 動詞か do / does か、どの形を使ったのかとその理由を説明しなさい。\n{src}",
                model, f"下線部の代名詞は {pron}（{num}）。{how}。" + (f"（{full} も可）" if full and full != ans else ""),
                [("正しい代名詞を選んでいる", 2), (f"正しい{what}を書いている", 3), ("be 動詞・do / does の選び方の理由を説明している", 3)], d=4, p=8, lines=5,
                ap="下線部が何人（いくつ）か、男性か女性かを考えて代名詞を決める。その代名詞が3人称単数か複数かで、be 動詞・do / does の形が決まる。",
                steps=[f"下線部 {S[0]} を代名詞にする：{pron}（{num}）。", "be 動詞の文か一般動詞の文かを判断する。", f"{how}。", f"答え：{ans}"],
                alt=["書きかえた文の代名詞をもとの名詞にもどして読み、もとの文の" + what + "として意味が通るかを確かめる。"],
                pc=[("代名詞", 2), (what, 3), ("理由の説明", 3)],
                pit=["Tom and Emi を he や she にする。", "代名詞にかえたあと、3人称単数かどうかの判断を誤る。"])


PROFILES = [("Aya", "she"), ("Mai", "she"), ("Emi", "she"), ("Lucy", "she"), ("Haruto", "he"), ("Sota", "he"), ("Ken", "he"), ("Tom", "he")]
TOWNS = ["Sendai", "Kobe", "Nagoya", "Fukuoka", "Sapporo", "Yokohama", "Kyoto", "Okinawa"]
INTRO_VP = [v for v in VP if v[0] in ("play", "have", "like", "speak", "live", "study", "watch", "read", "cook", "enjoy")]


@gen("thinking_writing", 3, ["cross_unit", "application"], rel=["JH-ENG-G1-U02"])
def intro_rewrite(r):
    name, pron = r.choice(PROFILES)
    town = r.choice(TOWNS)
    v1, v2 = r.sample(INTRO_VP, 2)
    P = (cap(pron), "3s", "", pron)
    I = ("I", "1s", "", None)
    src = f"I'm {name}. I am from {town}. {gv_aff(I, v1)} {gv_aff(I, v2)}"
    ans = f"This is {name}. {cap(pron)} is from {town}. {gv_aff(P, v1)} {gv_aff(P, v2)}"
    return desc(f"次の英文は、{name} さんが自分について書いた自己紹介です。これを、あなたが {name} さんをクラスのみんなに紹介する文章（4文）に書きかえなさい。1文目は This is {name}. とし、2文目以降の主語は代名詞にすること。\n{src}",
                ans, f"{name} さんは {pron} で受ける3人称単数。be 動詞は is、一般動詞は {v1[1]}・{v2[1]} のように3単現の形にする。",
                [("2文目以降の主語を正しい代名詞にしている", 2), ("be 動詞を is にしている", 2), ("一般動詞を3単現の形（つづりもふくむ）にしている", 3), ("1文目を This is ～. で書いている", 1)], d=4, p=8, lines=6,
                ap="自分（I）についての文を、ほかの人（3人称単数）についての文にすると、主語・be 動詞・一般動詞の形がすべてかわる。",
                steps=[f"{name} さんを受ける代名詞を決める：{pron}。", "I am → " + cap(pron) + " is にする。", f"一般動詞を3単現にする：{v1[0]} → {v1[1]}、{v2[0]} → {v2[1]}。", f"答え：{ans}"],
                alt=["書いた文章の代名詞を I にもどして読み、もとの自己紹介と内容が同じになっているかを確かめる。"],
                pc=[("代名詞", 2), ("be 動詞", 2), ("3単現", 3), ("This is ～.", 1)],
                pit=[f"{pron} にかえたのに、動詞を {v1[0]} のまま書く。", "I'm を He's / She's ではなく He am / She am と書く。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(e, ap, alt, pit, d=3):
    task = f"次の日本語を英語に直しなさい。\n{e['jp']}"
    return desc(f"{task}\n［ある生徒の解答］\n{e['wrong']}\n上の解答の誤りを指摘し、正しい英文に書き直しなさい。", e["fix"],
                f"「{e['where']}」の部分が誤り。{e['rule']}。正しくは {e['fix']}",
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい英文に直している", 3), ("規則を説明している", 1)], d=d, p=6, lines=5,
                ap=ap, steps=["文の動詞を見つけ、be 動詞の文か一般動詞の文かを判断する。", "主語の種類と、動詞・be 動詞・do / does の形が合っているかを確かめる。",
                              f"誤り「{e['where']}」を直す：{e['rule']}。", f"正しい英文：{e['fix']}"],
                alt=alt, pc=[("誤りの指摘", 2), ("正しい英文", 3), ("規則の説明", 1)], pit=pit,
                err=dict(sol=e["wrong"], step=f"「{e['where']}」の部分", type=e["type"], tempt=e["tempt"], fix=e["fix"]))


@gen("error_correction", 5, ["common_error", "condition_check"])
def err_be_do(r):
    e = make_error(r.choice(["be_gv", "be_q_gv", "be_neg_gv", "do_q_be", "do_neg_be", "be_agree"]), r)
    return err_item(e, "文の中に一般動詞があるかどうかで、be 動詞の文か一般動詞の文かを決める。否定文・疑問文の作り方はこの判断で決まる。",
                    ["直した英文を肯定文にもどしてみて、be 動詞と一般動詞が並んでいないか、主語と be 動詞の組み合わせが正しいかを確かめる。"],
                    ["日本語の「です・ます」を be 動詞に置きかえる。", "否定文・疑問文の作り方を、be 動詞の文と一般動詞の文で混同する。"])


@gen("error_correction", 5, ["common_error", "computation"])
def err_third_person(r):
    e = make_error(r.choice(["no_s", "pl_s", "does_s", "doesnt_s", "dont_3s", "spell"]), r)
    return err_item(e, "3単現の s は「主語が3人称単数」「現在の文」「肯定文」の3つがそろったときだけ動詞につく。does / doesn't を使ったら動詞は原形。",
                    ["主語を he / she / they などの代名詞に置きかえて読み、He plays / They play のどちらの形になるかを確かめる。"],
                    ["s のつけ忘れと、s のつけすぎ（Does ～ plays?）の両方に注意する。", "つづりの変化（studies, goes, has）を確かめない。"])


GENERATORS = [choose_be, verb_in_sentence, spell_3s, be_or_do, answer_reply,
              make_negative, make_question, change_subject, build_order, correct_sentence,
              explain_blanks, pronoun_rewrite, intro_rewrite,
              err_be_do, err_third_person]
