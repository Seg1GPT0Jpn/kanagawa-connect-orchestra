"""単元パック：中学2年 英語 未来表現（will・be going to・未来を表す語句）。"""
import random

from banks._common import desc, mc, order, sa
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem,
                         tp)

UNIT_ID = "JH-ENG-G2-U01"

PREREQUISITES = [
    ("JH-ENG-G1-U04", "助動詞 can＋動詞の原形の文の作り方（will も同じ助動詞）と、be 動詞の否定文・疑問文のルール。"),
    ("JH-ENG-G1-U05", "過去形と yesterday / last ～ など過去を表す語句。時を表す語句から時制を判断する力。"),
    ("JH-ENG-G1-U01", "be 動詞 am / are / is を主語に合わせて選べること（be going to の be で使う）。"),
]
EXTENSIONS = [
    ("JH-ENG-G2-U03", "when / if で始まる「時・条件」のまとまりの中では、未来のことでも現在形を使う（If it is sunny tomorrow, ～.）。"),
    ("JH-ENG-G2-U02", "be going to の to と、want to ～ / hope to ～ などの不定詞の to を区別して使えるようになる。"),
    ("HS-ENG-U02", "高校では未来進行形・未来完了形や、時・条件の副詞節の時制など、未来の表し方をさらに広げる。"),
    ("HS-ENG-U03", "will の推量・意志・習性など、助動詞の意味を詳しく学ぶ。"),
]

# 主語：(英語, be 動詞, 日本語, 代名詞)
SUBJ = [("I", "am", "私", "I"), ("You", "are", "あなた", "you"), ("He", "is", "彼", "he"), ("She", "is", "彼女", "she"),
        ("We", "are", "私たち", "we"), ("They", "are", "彼ら", "they"), ("Ken", "is", "ケン", "he"), ("Yumi", "is", "ユミ", "she"),
        ("Tom and Mike", "are", "トムとマイク", "they"), ("My friends", "are", "私の友だち", "they"), ("Mr. Brown", "is", "ブラウン先生", "he"),
        ("My sister", "is", "私の姉", "she")]
THIRD = [s for s in SUBJ if s[1] == "is"]

# 動作：(原形, 三単現, 過去形, ing 形, 目的語など, 日本語の目的語部分, 辞書形)
ACT = [
    ("play", "plays", "played", "playing", "tennis", "テニスを", "する"),
    ("study", "studies", "studied", "studying", "English", "英語を", "勉強する"),
    ("watch", "watches", "watched", "watching", "a soccer game", "サッカーの試合を", "見る"),
    ("clean", "cleans", "cleaned", "cleaning", "the classroom", "教室を", "掃除する"),
    ("buy", "buys", "bought", "buying", "a new racket", "新しいラケットを", "買う"),
    ("make", "makes", "made", "making", "dinner", "夕食を", "作る"),
    ("write", "writes", "wrote", "writing", "an email", "メールを", "書く"),
    ("go", "goes", "went", "going", "to the museum", "博物館へ", "行く"),
    ("read", "reads", "read", "reading", "this book", "この本を", "読む"),
    ("practice", "practices", "practiced", "practicing", "the guitar", "ギターを", "練習する"),
    ("swim", "swims", "swam", "swimming", "in the pool", "プールで", "泳ぐ"),
    ("take", "takes", "took", "taking", "pictures", "写真を", "とる"),
    ("cook", "cooks", "cooked", "cooking", "curry", "カレーを", "作る"),
    ("meet", "meets", "met", "meeting", "Emma", "エマに", "会う"),
    ("use", "uses", "used", "using", "the computer", "そのコンピューターを", "使う"),
    ("climb", "climbs", "climbed", "climbing", "Mt. Fuji", "富士山に", "登る"),
    ("visit", "visits", "visited", "visiting", "Kyoto", "京都を", "訪れる"),
]
FTIME = [("tomorrow", "明日"), ("next Sunday", "次の日曜日"), ("this weekend", "今週末"), ("next week", "来週"),
         ("tomorrow afternoon", "明日の午後"), ("next month", "来月"), ("the day after tomorrow", "あさって")]
PTIME = [("yesterday", "昨日"), ("last Sunday", "この前の日曜日"), ("last week", "先週"), ("two days ago", "2日前")]
HTIME = [("every Sunday", "毎週日曜日"), ("every day", "毎日"), ("on Saturdays", "毎週土曜日")]

PHRASES = [("明日の朝", "tomorrow morning", []), ("明日の午後", "tomorrow afternoon", []), ("来週", "next week", []), ("来月", "next month", []),
           ("来年", "next year", []), ("次の日曜日", "next Sunday", []), ("あさって", "the day after tomorrow", []),
           ("今週末", "this weekend", []), ("将来", "in the future", []), ("いつか", "someday", ["some day"]), ("もうすぐ", "soon", []),
           ("今夜", "tonight", ["this evening"]), ("今度の夏休み", "this summer vacation", ["this summer"])]


def cap(s):
    return s[0].upper() + s[1:]


def mid(s):
    if s.split()[0] in ("You", "He", "She", "We", "They", "My", "Our", "Your"):
        return s[0].lower() + s[1:]
    return s


def local(key):
    return random.Random(key)


# ======================================================================
# 授業プリント
# ======================================================================

LESSON = lesson(
    goals=["will＋動詞の原形で、未来の予想や、その場で決めた意志（～します）を表し、否定文 won't・疑問文 Will ～? も作れる。",
           "be going to＋動詞の原形で、前から決めている予定や、今の状況から確実に起こりそうなことを表せる。",
           "tomorrow, next ～, this weekend などの未来を表す語句を使い、時を表す語句に合う動詞の形を選べる。"],
    duration=50,
    readiness=["助動詞 can＋動詞の原形の文と、その否定文・疑問文を作れる（中1）。", "be 動詞 am / are / is を主語に合わせて選べる（中1）。",
               "過去形と、yesterday / last ～ など過去を表す語句を使える（中1）。",
               "小学校の外国語で I want to ～. / I'm going to ～.（夏休みの予定など）の表現にふれている。"],
    flow=[("導入：週末の予定", 5, "教師が週末の予定を I'm going to ～. で話し、過去・現在の文と何が違うかに気づかせる"),
          ("will の文", 13, "will＋原形、won't、Will ～?、予想と意志、Will you ～?（依頼）（例題1）"),
          ("be going to の文", 13, "be 動詞の選び方、否定文・疑問文、予定と確実な予測（例題2）"),
          ("未来を表す語句と使い分け", 11, "時を表す語句で時制を判断する、will と be going to の使い分け（例題3）"),
          ("まとめと確認", 8, "過去・現在・未来の表を完成させ、確認問題3問")],
    sections=[
        intro("in1", "英語で「これから」のことを言うには",
              "英語の動詞には「未来形」という特別な形はありません。その代わりに、動詞の原形の前に will を置いたり、be going to を置いたりして、これから起こることを表します。どちらも後ろの動詞は原形です。この単元では、2つの言い方の作り方と使い分け、そして未来を表す語句を学びます。",
              bullets=["I play tennis every Sunday.（いつもの習慣）", "I played tennis yesterday.（過去）",
                       "I will play tennis tomorrow.（明日テニスをします）", "I'm going to play tennis next Sunday.（次の日曜日にテニスをする予定です）"],
              points=[tp("過去・現在・未来の3つの文を並べて板書し、「時を表す語句」と「動詞の部分」を色分けさせる。",
                         ask="tomorrow の文で、play の形は変わっているか。", expect="変わっていない（原形のまま）。前に will がついた。", timing="導入の冒頭")]),
        definition("df1", "will＋動詞の原形",
                   "will は can と同じ助動詞です。主語が何であっても will の形は変わらず、後ろの動詞は原形にします。「～だろう」という未来の予想や、「～します」というその場で決めた意志を表します。",
                   formula="主語＋will＋動詞の原形 ～.／否定：will not（won't）＋原形／疑問：Will＋主語＋原形 ～?",
                   bullets=["予想：It will be sunny tomorrow.（明日は晴れるでしょう）", "その場で決めた意志：The phone is ringing. ― I'll get it.（私が出ます）",
                            "短縮形：I will → I'll、you will → you'll、will not → won't", "答え方：Will he come? ― Yes, he will. / No, he won't.",
                            "依頼：Will you open the window? ― Sure.（窓を開けてくれますか）"],
                   conditions=["will の後ろに to はつけない。三人称単数でも wills や will plays にはしない。",
                               "形容詞や名詞を続けるときは be が必要（× It will sunny. → It will be sunny.）。"],
                   points=[tp("can の文と並べて「助動詞＋原形」のルールが同じであることを確認させる。",
                              ask="He can swim. と同じ形で「彼は泳ぐでしょう」と言うと？", expect="He will swim."),
                           tp("It will be ～. の be を落とす誤りが多い。「will の後ろは動詞の原形。形容詞の前には be の原形 be が必要」と説明する。",
                              caution="It will rainy. / I will busy. などの誤り。")]),
        definition("df2", "be going to＋動詞の原形",
                   "be going to は「～する予定だ・～するつもりだ」と、前から決めている予定を表します。また、今の状況から「（このままだと）～しそうだ」と確実に予測できることにも使います。be 動詞は主語に合わせて選びます。",
                   formula="主語＋am / are / is＋going to＋動詞の原形 ～.",
                   bullets=["否定文：be 動詞の後ろに not（I'm not going to watch TV tonight.）", "疑問文：be 動詞を主語の前に出す（Are you going to visit Kyoto? ― Yes, I am.）",
                            "疑問詞：What are you going to do this weekend?", "状況からの予測：Look at those dark clouds. It's going to rain."],
                   conditions=["be 動詞を落とさない（× I going to ～.）。", "to の後ろは原形（× He is going to plays ～.）。",
                               "否定文・疑問文で do / does は使わない（× Do you going to ～?）。"],
                   points=[tp("be going to の文は「be 動詞の文」なので、否定文・疑問文は be 動詞のルールで作ることを、現在進行形の文と比べて確認する。")]),
        theorem("th1", "will と be going to の使い分けと、未来を表す語句",
                "前から決めている予定 → be going to ／ その場で決めた意志 → will ／ 未来の予想 → will（状況に根拠がある予測は be going to も）",
                ["未来を表す語句：tomorrow, tonight, next ～（next week / next Sunday）, this weekend, the day after tomorrow, in the future, someday, soon",
                 "時を表す語句が過去（yesterday, last ～, ～ ago）なら過去形、未来なら will / be going to を使う。",
                 "next や last の前に on / in などの前置詞はつけない（× on next Sunday）。"],
                body="実際には will と be going to のどちらも使える場面が多くあります。迷ったときは「前から決めていた予定か、その場で決めたことか」を考えると選びやすくなります。",
                points=[tp("電話が鳴った場面（I'll get it.）と、旅行の計画を話す場面（I'm going to visit Okinawa this summer.）を寸劇で示し、決めたタイミングの違いに気づかせる。",
                           ask="電話が鳴ってから「私が出ます」と決めたのはいつか。", expect="鳴った瞬間（その場）。だから will。")]),
        derivation("dv1", "未来の文の作り方（なぜその形になるのか）",
                   ["① 現在の文 Ken plays tennis. から始める。",
                    "② will は助動詞なので、can と同じく動詞の前に置き、後ろを原形にする：Ken will play tennis tomorrow.（plays → play）",
                    "③ 否定文・疑問文は will 自身を使う：Ken won't play tennis. ／ Will Ken play tennis?",
                    "④ be going to では、主語に合う be 動詞を置き、going to の後ろに原形を置く：Ken is going to play tennis next Sunday.",
                    "⑤ be going to の文は be 動詞の文なので、否定文・疑問文は be 動詞のルール：Ken isn't going to play ～. ／ Is Ken going to play ～?",
                    "⑥ どちらの文でも、未来を表す語句（tomorrow, next Sunday など）を文末に置くことが多い。"],
                   body="will の文は「can の文」、be going to の文は「be 動詞の文」と同じルールで否定文・疑問文を作ります。新しいルールではなく、これまでのルールの組み合わせです。",
                   points=[tp("②と④を並べて、どちらも最後は「動詞の原形」になっていることを確認させ、原形以外を置く誤りを防ぐ。",
                              ask="⑤で does を使わないのはなぜか。", expect="文の中に be 動詞 is があるから。", timing="導出の説明時")]),
        example("ex1", "例題1　will の文",
                "日本語に合う英文を書きなさい。(1) 明日は雨が降るでしょう。（rainy を使って）　(2) 私の兄は今夜、家にいないでしょう。",
                ["(1) 天気の主語は It。rainy は形容詞なので be が必要：It will be rainy tomorrow.",
                 "(2) 「いないでしょう」は will not（won't）。「家にいる」は be at home：My brother won't be at home tonight."],
                "(1) It will be rainy tomorrow.　(2) My brother won't (will not) be at home tonight.",
                thinking="will の後ろは動詞の原形。形容詞や場所を表す語句が続くときは be を入れる。",
                points=[tp("(1) を It will rainy. とする誤りを予想させ、「rainy は形容詞なので動詞が必要」と確認させる。rain（動詞）を使えば It will rain tomorrow. と言えることも補足する。")],
                misconceptions=[("It will rainy tomorrow.", "rainy は形容詞なので be が必要。It will be rainy tomorrow."),
                                ("My brother will not at home tonight.", "at home の前に be が必要。My brother will not be at home tonight.")]),
        example("ex2", "例題2　be going to の文",
                "次の英文を、（　）内の指示に従って書きかえなさい。(1) Yumi visits her aunt.（next Sunday を加えて be going to の文に）　(2) They are going to play baseball this weekend.（疑問文にして、No で答える）",
                ["(1) 主語 Yumi に合う be 動詞は is。to の後ろは原形 visit：Yumi is going to visit her aunt next Sunday.",
                 "(2) be 動詞 are を主語の前に出す：Are they going to play baseball this weekend?", "(2) 答えは be 動詞を使う：No, they aren't."],
                "(1) Yumi is going to visit her aunt next Sunday.　(2) Are they going to play baseball this weekend? ― No, they aren't.",
                thinking="be going to の be は主語で決まる。to の後ろは原形。疑問文は be 動詞を前に出す。",
                points=[tp("(1) で visits の s を残す誤りに注意させる。「to の後ろは原形」を声に出して確認する。")],
                misconceptions=[("Yumi is going to visits her aunt next Sunday.", "to の後ろは原形。visit。"),
                                ("Do they going to play baseball this weekend?", "be going to の疑問文は be 動詞を前に出す。Are they ～?")]),
        example("ex3", "例題3　時を表す語句と動詞の形",
                "（　）内の語を適切な形にしなさい。必要なら語を補うこと。(1) I (see) Ken at the station yesterday.　(2) I (see) Ken at the station tomorrow.",
                ["(1) yesterday は過去を表すので過去形。see は不規則動詞で saw。",
                 "(2) tomorrow は未来を表すので will＋原形：will see（予定なら am going to see も可）。"],
                "(1) saw　(2) will see（am going to see）",
                thinking="まず時を表す語句を見つけ、過去・現在・未来のどれかを決めてから動詞の形を決める。",
                points=[tp("時を表す語句に下線を引く習慣をつけさせる。yesterday / tomorrow を入れかえるだけで動詞の形が変わることを体験させる。")]),
        board("bd1", "板書案",
              [("① will", ["will＋原形（主語で変化なし）", "It will be sunny tomorrow.", "否定：won't＋原形", "疑問：Will he come?", "― Yes, he will. / No, he won't.", "その場で決めた意志：I'll get it."]),
               ("② be going to", ["am / are / is＋going to＋原形", "I'm going to visit Kyoto.", "否定：isn't going to ～", "疑問：Are you going to ～?", "― Yes, I am.", "予定・状況からの予測"]),
               ("③ 時を表す語句", ["過去：yesterday / last ～ / ～ ago", "現在：every day / usually", "未来：tomorrow / next ～", "this weekend / tonight", "in the future / someday", "× on next Sunday"])],
              points=[tp("①②の列で「後ろは原形」を赤で囲み、③の列で時を表す語句と動詞の形を線で結ばせる。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("週末の予定をペアで What are you going to do this weekend? ― I'm going to ～. と言い合わせ、be 動詞の入れ忘れをペアで指摘させる。", timing="例題2の後"),
               tp("Will you ～? は「～してくれますか」という依頼にもなることを、教室での具体的な依頼（Will you open the door?）で体験させる。",
                  ask="Will you open the door? にどう答えるか。", expect="Sure. / All right. / OK."),
               tp("It will be ～. の be を落とす誤りは、will の後ろに「動詞」があるかを確かめさせることで防ぐ。"),
               tp("will と be going to の使い分けは、厳密に区別させすぎず、まずは「どちらも未来を表し、後ろは原形」を確実にする。", caution="使い分けだけを問う問題は、場面がはっきりしているものに限る。"),
               tp("問題プリント D の誤答例は「原形にしていない」「be 動詞の入れ忘れ」「時を表す語句と時制の不一致」の3種類に分類させる。")],
              misconceptions=[("He will plays tennis.", "will の後ろは原形。He will play tennis."),
                              ("I going to visit Kyoto.", "be 動詞が必要。I'm going to visit Kyoto."),
                              ("It will sunny tomorrow.", "sunny は形容詞なので be が必要。It will be sunny tomorrow."),
                              ("I will visit my aunt last Sunday.", "last Sunday は過去。I visited my aunt last Sunday.")]),
        summary("sm1", "まとめ",
                ["will＋原形：未来の予想・その場で決めた意志。否定は won't、疑問は Will ～?。形容詞の前は will be。",
                 "be going to＋原形：前から決めている予定・状況からの予測。be 動詞は主語で選び、否定・疑問は be 動詞のルール。",
                 "時を表す語句（yesterday / every day / tomorrow など）で過去・現在・未来を判断し、動詞の形を決める。"]),
        check("ck1", "確認問題",
              [("She (will / wills) (come / comes) to the party. の（　）から正しい語を選びなさい。", "will, come"),
               ("「私は来週、京都を訪れる予定です」を be going to を使って書きなさい。", "I'm going to visit Kyoto next week."),
               ("Will you help me? に「いいですよ」と答える表現を1つ書きなさい。", "Sure. / All right. / OK. など")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

@gen("basic_check", 4, ["computation", "condition_check"])
def will_form(r):
    s, be, sj, _ = r.choice(SUBJ)
    v, v3, past, ing, obj, jo, jd = r.choice(ACT)
    t, tj = r.choice(FTIME)
    if r.random() < 0.5:
        jp = f"{sj}は{tj}、{jo}{jd}{'つもりです' if s == 'I' else 'でしょう'}。"
        ok = f"will {v}"
        why = {f"will {v3}": ("will の後ろの動詞はいつも原形。主語が何でも s はつけない。", "助動詞の後ろの動詞の形"),
               f"wills {v}": ("will は主語によって形が変わらない。wills という形はない。", "助動詞の形"),
               f"will {past}" if past != v else f"will to {v}": (("will の後ろは原形。過去形は置かない。" if past != v else "will の後ろに to は置かない。"), "助動詞の後ろの動詞の形")}
    else:
        jp = f"{sj}は{tj}、{jo}{jp_neg(jd)}{'つもりです' if s == 'I' else 'でしょう'}。"
        ok = f"won't {v}"
        do_neg = "doesn't" if be == "is" else "don't"
        why = {f"{do_neg} will {v}": ("will の文の否定は will の後ろに not をつける（won't / will not）。do / does は使わない。", "一般動詞の否定文との混同"),
               f"won't {v3}": ("won't の後ろの動詞も原形。s はつけない。", "助動詞の後ろの動詞の形"),
               f"will {v} not": ("not は will の直後に置く（will not）。動詞の後ろには置かない。", "否定文の語順")}
    return mc(f"日本語に合うように、（　）に入る最も適切なものを選びなさい。\n{jp}\n{s} (　　) {obj} {t}.", [ok] + list(why),
              f"{t}（{tj}）は未来を表すので will を使う。will の後ろは主語に関係なく動詞の原形。答え：{ok}", d=1,
              ap="will は can と同じ助動詞。主語が何であっても形は変わらず、後ろの動詞は原形。否定は will not（won't）。",
              steps=[f"{t} は未来 → will を使う。", f"will（won't）の後ろは原形 {v}。", f"答え：{ok}"],
              alt=["will を can に置きかえても文の形が成り立つかを確かめる（どちらも助動詞＋原形）。"],
              pc=[("will / won't を正しく使っている", 1), ("後ろの動詞を原形にしている", 1)],
              pit=["主語が三人称単数のとき、will の後ろの動詞に s をつける。", "否定文に don't / doesn't を使う。"], why=why)


def jp_neg(jd):
    """辞書形 → 「～しない」の形。"""
    if jd.endswith("する"):
        return jd[:-2] + "しない"
    if jd == "会う":
        return "会わない"
    table = {"る": "らない", "う": "わない", "く": "かない", "む": "まない", "ぐ": "がない", "つ": "たない"}
    if jd in ("見る", "訪れる"):
        return jd[:-1] + "ない"
    return jd[:-1] + table.get(jd[-1], "ない")


@gen("basic_check", 4, ["computation", "common_error"])
def going_to_form(r):
    s, be, sj, _ = r.choice(SUBJ)
    v, v3, past, ing, obj, jo, jd = r.choice(ACT)
    t, tj = r.choice(FTIME)
    jp = f"{sj}は{tj}、{jo}{jd}予定です。"
    if r.random() < 0.5:
        other = {"am": "is", "is": "are", "are": "is"}[be]
        do = "does" if be == "is" else "do"
        stem = f"日本語に合うように、（　）に入る最も適切なものを選びなさい。\n{jp}\n{s} (　　) going to {v} {obj} {t}."
        ok = be
        why = {other: (f"主語 {s} に合う be 動詞は {be}。", "主語と be 動詞の対応"),
               do: ("be going to の文には be 動詞が必要。do / does は使わない。", "be 動詞と do / does の混同"),
               "will": ("will と going to を続けて置くことはできない。be going to の be には主語に合う be 動詞を置く。", "will と be going to の混同")}
        pt = "be 動詞"
    else:
        stem = f"日本語に合うように、（　）に入る最も適切なものを選びなさい。\n{jp}\n{s} {be} going to (　　) {obj} {t}."
        ok = v
        why = {v3: ("going to の後ろの動詞は原形。三単現の s はつけない。", "be going to の後ろの動詞の形"),
               ing: ("going to の後ろは原形。ing 形は置かない。", "be going to の後ろの動詞の形")}
        why[past if past != v else f"to {v}"] = (("going to の後ろは原形。過去形は置かない。" if past != v else "to はすでにあるので、もう1つ to を置く必要はない。"), "be going to の後ろの動詞の形")
        pt = "動詞の形"
    return mc(stem, [ok] + list(why),
              f"「～する予定だ」は be going to＋動詞の原形。be 動詞は主語 {s} に合わせて {be}、to の後ろは原形 {v}。答え：{ok}", d=1,
              ap="be going to の文は、①主語に合う be 動詞、②to の後ろの原形、の2か所を確かめる。",
              steps=[f"主語 {s} → be 動詞は {be}。", f"going to の後ろは原形 → {v}。", f"{pt}として正しいのは {ok}。"],
              alt=[f"完成した文を疑問文（{cap(be)} {mid(s)} going to {v} ～?）にしてみて、be 動詞の文として形がくずれないかを確かめる。"],
              pc=[("主語に合う be 動詞を判断している", 1), ("to の後ろの原形を判断している", 1)],
              pit=["be 動詞を落とす（I going to ～）。", "to の後ろの動詞に s や ing をつける。"], why=why)


@gen("basic_check", 4, ["concept", "condition_check"])
def time_words(r):
    s, be, sj, _ = r.choice([x for x in SUBJ if x[0] in ("I", "We", "They", "You", "My friends", "Tom and Mike")])
    v, v3, past, ing, obj, jo, jd = r.choice([a for a in ACT if a[2] != a[0]])
    kind = r.choice(["past", "future", "habit"])
    t, tj = r.choice({"past": PTIME, "future": FTIME, "habit": HTIME}[kind])
    ok = {"past": past, "future": f"will {v}", "habit": v}[kind]
    labels = {past: ("過去", "yesterday / last ～ / ～ ago などの過去を表す語句"), f"will {v}": ("未来", "tomorrow / next ～ などの未来を表す語句"),
              v: ("現在の習慣", "every ～ / on ～s などのくり返しを表す語句")}
    why = {w: (f"{w} は{labels[w][0]}を表す形で、{labels[w][1]}と使う。この文の {t} は{ {'past': '過去', 'future': '未来', 'habit': '現在の習慣'}[kind]}を表す。", "時を表す語句と時制の対応")
           for w in labels if w != ok}
    why[f"will {past}"] = ("will の後ろは原形。過去形を置くことはできない。", "助動詞の後ろの動詞の形")
    return mc(f"（　）に入る最も適切なものを選びなさい。\n{s} (　　) {obj} {t}.", [ok] + list(why),
              f"{t}（{tj}）は{ {'past': '過去', 'future': '未来', 'habit': '現在の習慣'}[kind]}を表すので {ok}。", d=2,
              ap="まず文末の時を表す語句に下線を引き、過去・現在・未来のどれかを決めてから動詞の形を選ぶ。",
              steps=[f"時を表す語句は {t}（{tj}）。", f"{ {'past': '過去', 'future': '未来', 'habit': '現在の習慣'}[kind]}の文なので {ok} を選ぶ。"],
              alt=["選んだ形で文を日本語に訳し、「～した」「～する（いつも）」「～するだろう」が時を表す語句と合うかを確かめる。"],
              pc=[("時を表す語句から時制を判断している", 1), ("正しい形を選んでいる", 1)],
              pit=["動詞の形だけを見て、時を表す語句を確かめない。", "will の後ろに過去形を置く。"], why=why)


@gen("basic_check", 4, ["concept", "condition_check"])
def future_response(r):
    kind = r.choice(["will_you", "will_3", "going_you", "going_3"])
    yes = r.random() < 0.5
    v, v3, past, ing, obj, jo, jd = r.choice(ACT)
    t, tj = r.choice(FTIME)
    if kind in ("will_you", "will_3"):
        if kind == "will_you":
            q, a = f"Will you {v} {obj} {t}?", "I"
            wrong_subj = "you"
        else:
            s, be, sj, a = r.choice(THIRD)
            q = f"Will {mid(s)} {v} {obj} {t}?"
            wrong_subj = "I"
        ok = f"Yes, {a} will." if yes else f"No, {a} won't."
        why = {(f"Yes, {a} {'do' if a == 'I' else 'does'}." if yes else f"No, {a} {'don' if a == 'I' else 'doesn'}'t."): ("Will ～? の疑問文には will を使って答える。", "一般動詞の答え方との混同"),
               (f"Yes, {a} {'am' if a == 'I' else 'is'}." if yes else f"No, {a} {'am not' if a == 'I' else 'isn' + chr(39) + 't'}."): ("Will ～? の疑問文には will を使って答える。be 動詞は使わない。", "be 動詞の答え方との混同"),
               (f"Yes, {wrong_subj} will." if yes else f"No, {wrong_subj} won't."): ("答えの主語は、たずねられた人を代名詞にしたもの（you → I、人の名前 → he / she）。", "答えの主語")}
    else:
        if kind == "going_you":
            q, a, ab = f"Are you going to {v} {obj} {t}?", "I", "am"
            wrong_subj, wb = "you", "are"
        else:
            s, be, sj, a = r.choice(THIRD)
            q, ab = f"Is {mid(s)} going to {v} {obj} {t}?", "is"
            wrong_subj, wb = "I", "am"
        ok = f"Yes, {a} {ab}." if yes else (f"No, I'm not." if a == "I" else f"No, {a} isn't.")
        why = {(f"Yes, {a} {'do' if a == 'I' else 'does'}." if yes else f"No, {a} {'don' if a == 'I' else 'doesn'}'t."): ("be going to の疑問文は be 動詞の文なので、be 動詞で答える。do / does は使わない。", "be 動詞と do / does の混同"),
               (f"Yes, {a} will." if yes else f"No, {a} won't."): ("Are / Is ～ going to ～? の疑問文には be 動詞で答える。will は Will ～? の答え。", "疑問文と答えの対応"),
               (f"Yes, {a} going." if yes else f"No, {a} not going."): ("答えの文では be 動詞を使い、going は省く。", "答えの形")}
    yn = "「はい」" if yes else "「いいえ」"
    return mc(f"次の質問に{yn}と答えるとき、最も適切なものを選びなさい。\n{q}", [ok] + list(why),
              f"答え：{ok}。質問の文頭（Will / Are / Is）に合わせて答え、主語は代名詞にする。", d=2,
              ap="質問の最初の語を見る。Will ～? なら will、Are / Is ～ going to ～? なら be 動詞で答える。",
              steps=["質問の文頭を確認する。", "答えの主語を決める（you → I、人の名前 → he / she）。", f"答え：{ok}"],
              alt=["答えの省略部分を補ってみて（No, I won't play ～. / Yes, I am going to ～.）、質問と同じ形になっているかを確かめる。"],
              pc=[("答えに使う語（will / be 動詞）を正しく選んでいる", 1), ("主語・肯定否定が正しい", 1)],
              pit=["be going to の疑問文に will や do で答える。", "you でたずねられたのに you で答える。"], why=why)


@gen("basic_check", 4, ["computation", "common_error"])
def phrases(r):
    items = r.sample(PHRASES, 3)
    stem = "次の日本語を、未来を表す英語の語句にしなさい。\n" + "　".join(f"({i}) {jp}" for i, (jp, _, _) in enumerate(items, 1))
    ans = "　".join(f"({i}) {en}" for i, (_, en, _) in enumerate(items, 1))
    alts = [x[2] for x in items]
    note = "".join(f"（{jp} は {' / '.join(v)} も可）" for jp, _, v in items if v)
    return sa(stem, ans, f"未来を表す語句：{'、'.join(f'{jp}＝{en}' for jp, en, _ in items)}。{note}", d=1,
              v=[", ".join(x[1] for x in items)],
              ap="next ～（次の～）、tomorrow ～（明日の～）、this ～（今度の～）の組み合わせで考える。前置詞（on / in）は next / this / tomorrow の前につけない。",
              steps=[f"{jp} → {en}" for jp, en, _ in items],
              alt=["書いた語句を I will ～ ＋語句. の文に入れて読み、未来の文として自然かを確かめる。"],
              pc=[("3つのうち2つ以上を正しく書いている", 1), ("3つすべてを正しく書いている", 1)],
              pit=["on next Sunday のように前置詞をつける。", "あさってを next tomorrow とする。"])


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 4, ["computation", "application"])
def future_rewrite(r):
    s, be, sj, pr = r.choice(SUBJ)
    v, v3, past, ing, obj, jo, jd = r.choice(ACT)
    t, tj = r.choice(FTIME)
    pres = v3 if be == "is" else v
    con = {"am": "'m", "are": "'re", "is": "'s"}
    pron = s in ("I", "You", "He", "She", "We", "They")
    kind = r.choice(["will", "will_neg", "will_q", "going", "going_neg", "going_q"]) if s not in ("I", "We") else r.choice(["will", "will_neg", "going", "going_neg"])
    a = "I" if s == "You" else pr
    if kind == "will":
        stem = f"次の英文を、will を使って「{tj}～するでしょう（～します）」という未来の文に書きかえなさい。文末に {t} を加えること。\n{s} {pres} {obj}."
        ans = f"{s} will {v} {obj} {t}."
        v_ = [f"{s}'ll {v} {obj} {t}."] if pron else None
        stp = ["動詞の前に will を置く。", f"will の後ろは原形：{pres} → {v}。", f"文末に {t} を加える：{ans}"]
    elif kind == "will_neg":
        stem = f"次の英文を否定文に書きかえなさい。\n{s} will {v} {obj} {t}."
        ans = f"{s} won't {v} {obj} {t}."
        v_ = [f"{s} will not {v} {obj} {t}."]
        stp = ["will の後ろに not を置く（won't）。do / does は使わない。", "動詞は原形のまま。", f"答え：{ans}"]
    elif kind == "will_q":
        stem = f"次の英文を疑問文に書きかえ、さらに Yes で答える文も書きなさい。\n{s} will {v} {obj} {t}."
        ans = f"Will {mid(s)} {v} {obj} {t}? ― Yes, {a} will."
        v_ = None
        stp = ["Will を主語の前に出す。", "動詞は原形のまま。", f"答えも will を使う：Yes, {a} will.", f"答え：{ans}"]
    elif kind == "going":
        stem = f"次の英文を、be going to を使って「{tj}～する予定だ」という文に書きかえなさい。文末に {t} を加えること。\n{s} {pres} {obj}."
        ans = f"{s} {be} going to {v} {obj} {t}."
        v_ = [f"{s}{con[be]} going to {v} {obj} {t}."] if pron else None
        stp = [f"主語 {s} に合う be 動詞は {be}。", f"going to の後ろは原形：{pres} → {v}。", f"答え：{ans}"]
    elif kind == "going_neg":
        stem = f"次の英文を否定文に書きかえなさい。\n{s} {be} going to {v} {obj} {t}."
        ans = f"{s} {be} not going to {v} {obj} {t}."
        short = {"am": None, "are": "aren't", "is": "isn't"}[be]
        v_ = ([f"{s} {short} going to {v} {obj} {t}."] if short else []) + ([f"{s}{con[be]} not going to {v} {obj} {t}."] if pron else [])
        stp = ["be going to の文は be 動詞の文なので、be 動詞の後ろに not を置く。", "going to 以下はそのまま。", f"答え：{ans}"]
    else:
        stem = f"次の英文を疑問文に書きかえ、さらに No で答える文も書きなさい。\n{s} {be} going to {v} {obj} {t}."
        neg = "No, I'm not." if a == "I" else f"No, {a} {'aren' if be == 'are' else 'isn'}'t."
        ans = f"{cap(be)} {mid(s)} going to {v} {obj} {t}? ― {neg}"
        v_ = None
        stp = ["be 動詞を主語の前に出す。", "going to 以下はそのまま。", f"答えは be 動詞を使う：{neg}", f"答え：{ans}"]
    return sa(stem, ans, f"will の文は助動詞の文（can と同じ）、be going to の文は be 動詞の文のルールで否定文・疑問文を作る。答え：{ans}", d=2, p=4, v=v_ or None,
              ap="will の文か be going to の文かを確かめる。will は will 自身を、be going to は be 動詞を使って否定文・疑問文を作る。",
              steps=stp,
              alt=["書きかえた文の動詞が原形になっているか、do / does を使っていないかを最後に見直す。"],
              pc=[("will / be 動詞の位置と形が正しい", 2), ("動詞を原形にし、語順が正しい", 2)],
              pit=["三単現の s を残したまま will や going to の後ろに置く。", "be going to の疑問文で Do / Does を使う。"])


WH = [
    ("What", "do", "this weekend", "I'm going to visit my grandparents.", "Where"),
    ("Where", "go", "this summer", "I'm going to go to Hokkaido.", "What"),
    ("What time", "leave", "tomorrow morning", "I'm going to leave at seven.", "Where"),
    ("Who", "meet", "at the station", "I'm going to meet my cousin.", "What time"),
    ("How long", "stay", "in Okinawa", "I'm going to stay there for five days.", "Who"),
    ("What", "buy", "for Emi's birthday", "I'm going to buy a cap for her.", "How long"),
    ("When", "visit", "the museum", "I'm going to visit it next Saturday.", "Who"),
    ("How", "go", "to the stadium", "I'm going to go there by bike.", "Who"),
    ("What", "cook", "for dinner", "I'm going to cook spaghetti.", "When"),
    ("Where", "practice", "after school", "I'm going to practice in the gym.", "What"),
]


@gen("standard_practice", 4, ["cross_unit", "concept"], rel=["JH-ENG-G1-U03"])
def wh_future(r):
    wh, v, rest, ans, wrong_wh = r.choice(WH)
    ok = f"{wh} are you going to {v} {rest}?"
    why = {f"{wh} do you going to {v} {rest}?": ("be going to の疑問文には be 動詞が必要。do は使わない。", "be 動詞と do の混同"),
           f"{wh} are you going to {v}ing {rest}?" if not v.endswith("e") else f"{wh} are you going to {v[:-1]}ing {rest}?": ("going to の後ろは原形。ing 形は置かない。", "be going to の後ろの動詞の形"),
           f"{wrong_wh} are you going to {v} {rest}?": (f"B の答えの中心と合わないので、{wrong_wh} ではなく {wh} でたずねる文が合う。", "疑問詞と答えの対応")}
    return mc(f"次の対話が成り立つように、A の（　）に入る最も適切なものを選びなさい。\nA：(　　)\nB：{ans}", [ok] + list(why),
              f"B は be going to で予定を答えているので、A も be going to の疑問文。B の答えの中心に合う疑問詞は {wh}。答え：{ok}", d=3,
              ap="B の答えのどの部分が「たずねられた情報」かを見つけて疑問詞を決め、B と同じ be going to の形でたずねる。",
              steps=["B の答えの中心（場所・時・人・物など）を見つける。", f"それをたずねる疑問詞は {wh}。", f"疑問詞＋are you going to＋原形：{ok}"],
              alt=["選んだ疑問文の疑問詞の部分に B の答えを当てはめて、普通の文にもどるかを確かめる。"],
              pc=[("疑問詞を正しく選んでいる", 2), ("be going to の疑問文の形を選んでいる", 2)],
              pit=["What do you going to ～? のように do と going to を組み合わせる。", "答えの内容に合わない疑問詞を選ぶ。"], why=why)


ORDERS = [
    ("明日は雨が降るでしょう。", ["it", "will", "rain", "tomorrow"], "will＋原形 rain"),
    ("私は来週、おじを訪ねる予定です。", ["I'm", "going", "to", "visit", "my uncle", "next", "week"], "be going to＋原形"),
    ("ケンは今夜、家にいないでしょう。", ["Ken", "won't", "be", "at home", "tonight"], "won't＋be＋場所"),
    ("あなたはこの週末、何をするつもりですか。", ["what", "are", "you", "going", "to", "do", "this", "weekend"], "疑問詞＋are you going to＋原形"),
    ("窓を開けてくれますか。", ["will", "you", "open", "the", "window"], "依頼の Will you ～?"),
    ("彼女はその会議に出ないでしょう。", ["she", "will", "not", "join", "the", "meeting"], "will not＋原形"),
    ("私たちはあさって、富士山に登る予定です。", ["we", "are", "going", "to", "climb", "Mt. Fuji", "the day after tomorrow"], "be going to と未来を表す語句"),
    ("その試合は何時に始まるでしょうか。", ["what", "time", "will", "the", "game", "start"], "疑問詞＋will＋主語＋原形"),
    ("私の姉は来年、大学生になります。", ["my sister", "will", "be", "a college student", "next", "year"], "will＋be＋名詞"),
    ("彼らは放課後、テニスをする予定ではありません。", ["they", "aren't", "going", "to", "play", "tennis", "after", "school"], "be going to の否定文"),
    ("あの黒い雲を見て。雨が降りそうだ。", ["look at", "those", "dark clouds", "it's", "going", "to", "rain"], "状況からの予測 be going to"),
    ("私は将来、医者になるでしょう。", ["I", "will", "be", "a doctor", "in", "the", "future"], "will be＋名詞＋in the future"),
    ("あなたは明日、学校に来ますか。", ["will", "you", "come", "to", "school", "tomorrow"], "Will＋主語＋原形"),
    ("ユミは今度の日曜日、ケーキを作る予定です。", ["Yumi", "is", "going", "to", "make", "a cake", "next", "Sunday"], "is going to＋原形"),
]


@gen("standard_practice", 4, ["application", "computation"])
def build_order(r):
    jp, parts, pat = r.choice(ORDERS)
    if parts[0] == "look at":
        sent = "Look at those dark clouds. It's going to rain."
    else:
        sent = cap(" ".join(parts)) + ("?" if jp.endswith("か。") else ".")
    return order(f"日本語に合うように、次の語句を並べかえて英文を完成させなさい。ただし、文頭にくる語も小文字で示してある。\n{jp}", parts,
                 f"{sent}　ポイント：{pat}。", d=2, p=4,
                 ap="日本語の「～でしょう・～します」なら will、「～する予定です」なら be going to と考え、主語と動詞の部分を先に作る。",
                 steps=[f"文の型を決める：{pat}。", "主語と will / be going to の部分を並べ、後ろに動詞の原形を置く。", "目的語・場所・時を表す語句を後ろに並べる。", f"完成文：{sent}"],
                 alt=["完成した英文を日本語に訳し直して、問題の日本語と一致するかを確かめる。"],
                 pc=[("主語と will / be going to＋原形の語順が正しい", 2), ("目的語・修飾語句の順序が正しい", 2)],
                 pit=["be going to の be や to を落とす。", "疑問文で will や be 動詞を主語の後ろに置いたままにする。"])


SITU = [
    ("電話が鳴った。家族に「私が出るよ」と言うとき。", "I'll answer it.",
     [("I answered it.", "過去形で「私が出た」となり、これからする意志を表さない。"),
      ("Will you answer it?", "「あなたが出てくれますか」と相手に頼む文になる。"),
      ("I won't answer it.", "「私は出ない」という意味になり、場面と逆になる。")]),
    ("重い荷物を運んでいる先生に「お手伝いします」と申し出るとき。", "I'll help you.",
     [("Will you help me?", "「手伝ってくれますか」と相手に頼む文になる。"),
      ("I helped you.", "過去形で「手伝った」となり、これからの申し出にならない。"),
      ("You'll help me.", "「あなたは私を手伝うだろう」という意味になり、申し出にならない。")]),
    ("友だちに「窓を閉めてくれる？」と頼むとき。", "Will you close the window?",
     [("I'll close the window.", "「私が窓を閉めます」という意志を表す文で、頼む文にならない。"),
      ("Did you close the window?", "「窓を閉めましたか」と過去のことをたずねる文になる。"),
      ("You won't close the window.", "「あなたは窓を閉めないだろう」という意味になる。")]),
    ("夏休みの計画を聞かれ、「前から決めていた沖縄旅行の予定」を話すとき。", "I'm going to visit Okinawa this summer.",
     [("I visited Okinawa this summer.", "過去形で「この夏、沖縄を訪れた」となり、これからの予定にならない。"),
      ("I'm going to visited Okinawa this summer.", "going to の後ろは原形。visited は使えない。"),
      ("Are you going to visit Okinawa this summer?", "相手の予定をたずねる文で、自分の予定を伝えていない。")]),
    ("空が真っ黒な雲でおおわれている。「雨が降りそうだ」と言うとき。", "It's going to rain.",
     [("It rained.", "過去形で「雨が降った」となり、これから起こることを表さない。"),
      ("It's going to rainy.", "going to の後ろは動詞の原形。rainy は形容詞なので、使うなら going to be rainy となる。"),
      ("It isn't going to rain.", "「雨は降らないだろう」という意味になり、場面と逆になる。")]),
    ("天気予報で「明日は晴れるでしょう」と伝えるとき。", "It will be sunny tomorrow.",
     [("It will sunny tomorrow.", "sunny は形容詞なので be が必要。"),
      ("It was sunny tomorrow.", "tomorrow は未来なので過去形 was は使えない。"),
      ("Will it be sunny tomorrow?", "「明日は晴れますか」とたずねる文で、予報を伝えていない。")]),
    ("友だちに「明日、あなたは家にいますか」とたずねるとき。", "Will you be at home tomorrow?",
     [("Will you at home tomorrow?", "at home の前に be が必要。"),
      ("Were you at home tomorrow?", "tomorrow は未来なので過去形 were は使えない。"),
      ("Do you will be at home tomorrow?", "will の疑問文は Will を主語の前に出す。do は使わない。")]),
    ("「父は来週、出張でいないので会えない」と伝えるとき（父は家にいないでしょう）。", "My father won't be at home next week.",
     [("My father doesn't will be at home next week.", "will の否定は won't（will not）。doesn't は使わない。"),
      ("My father wasn't at home next week.", "next week は未来なので過去形は使えない。"),
      ("My father will be at home next week.", "「家にいるでしょう」となり、伝えたい内容と逆になる。")]),
    ("友だちから「あとで電話してね」と言われ、「わかった、電話するよ」と答えるとき。", "OK. I'll call you later.",
     [("OK. I called you later.", "過去形で「電話した」となり、これからの約束にならない。"),
      ("OK. Will you call me later?", "「あとで電話してくれる？」と相手に頼み返す文になる。"),
      ("OK. I'll calling you later.", "will の後ろは原形。ing 形は置かない。")]),
    ("「兄は来年、高校生になります」と伝えるとき。", "My brother will be a high school student next year.",
     [("My brother will a high school student next year.", "名詞の前には be が必要。"),
      ("My brother was a high school student next year.", "next year は未来なので過去形 was は使えない。"),
      ("My brother wills be a high school student next year.", "will は主語によって形が変わらない。wills という形はない。")]),
]


@gen("standard_practice", 4, ["application", "concept"])
def situation(r):
    sit, ok, wrongs = r.choice(SITU)
    return mc(f"次の場面で言う英文として最も適切なものを選びなさい。\n場面：{sit}", [ok] + [w for w, _ in wrongs],
              f"「{ok}」が場面に合う。場面の目的（予想・その場の意志・予定・依頼）と、時（過去か未来か）の両方から判断する。", d=2,
              ap="①場面が過去のことか未来のことか、②話し手が「予想する・申し出る・予定を伝える・頼む」のどれをしたいのか、の2点を確かめる。",
              steps=["場面の時（未来か過去か）を確認する。", "話し手の目的に合う形（I'll ～. / Will you ～? / be going to / won't）を決める。", f"答え：{ok}"],
              alt=["選択肢を日本語に訳して、場面のせりふとして自然かどうかを1つずつ確かめる。"],
              pc=[("場面の時と目的を正しく読み取っている", 2), ("目的に合う文の型を選んでいる", 2)],
              pit=["I'll ～.（申し出）と Will you ～?（依頼）を取り違える。", "形容詞や名詞の前の be を落とした選択肢を選ぶ。"],
              why={w: (reason, "場面と表現の対応") for w, reason in wrongs})


PLAN_A = [("go shopping with my mother", "母と買い物に行く"), ("visit my grandparents", "祖父母を訪ねる"), ("practice the piano", "ピアノを練習する"),
          ("watch a movie with my sister", "姉と映画を見る"), ("clean my room", "自分の部屋を掃除する")]
PLAN_B = [("play soccer in the park", "公園でサッカーをする"), ("go to the library", "図書館へ行く"), ("make a cake", "ケーキを作る"),
          ("go fishing", "つりに行く")]


@gen("standard_practice", 4, ["application", "concept"])
def dialog(r):
    (sat, satj), (sun, sunj) = r.sample(PLAN_A, 2)
    together, togj = r.choice(PLAN_B)
    text = (f"Ken: What are you going to do this weekend, Mika?\n"
            f"Mika: I'm going to {sat} on Saturday.\n"
            f"Ken: Will you be free on Sunday? I'm going to {together} with Taro.\n"
            f"Mika: Sorry, I won't be free. I'm going to {sun} on Sunday.\n"
            f"Ken: OK. Maybe next time.")
    ok = f"ミカは日曜日に{sunj}予定である。"
    wrongs = {f"ミカは日曜日に{satj}予定である。": f"{satj}のは土曜日の予定（I'm going to {sat} on Saturday.）。",
              f"ミカは日曜日にケンたちと{togj}予定である。": "ミカは Sorry, I won't be free. と答えており、ケンたちとは出かけない。",
              f"ケンは土曜日に{togj}予定である。": f"ケンが{togj}のは日曜日（Will you be free on Sunday? に続く文）。"}
    return mc(f"次の対話を読んで、内容に合うものを1つ選びなさい。\n{text}", [ok] + list(wrongs),
              f"Mika の I'm going to {sun} on Sunday. から、ミカは日曜日に{sunj}予定だとわかる。won't be free は「ひまではないだろう」という意味。", d=3,
              ap="それぞれの予定が「だれの」「何曜日の」ものかを、be going to / will の文から整理してから選択肢と比べる。",
              steps=["ミカの土曜日・日曜日の予定、ケンの日曜日の予定を表に整理する。", "Sorry, I won't be free. が「日曜日はひまではない」という断りであることを確かめる。", f"表と一致する「{ok}」を選ぶ。"],
              alt=["選択肢ごとに、根拠になる英文に下線を引いてから判断する。"],
              pc=[("それぞれの予定の曜日と人物を正しく読み取っている", 2), ("won't be free の意味を理解して選んでいる", 2)],
              pit=["曜日を取り違える。", "Will you be free on Sunday? を「日曜日にひまだ」という事実と読みちがえる。"],
              why={k: (v, "対話の内容の読み取り") for k, v in wrongs.items()})


# ======================================================================
# C 思考力・記述応用
# ======================================================================

PAIRS = [
    ("I play tennis on Sundays.", "I'm going to play tennis next Sunday.",
     "A は現在形で「私は（毎週）日曜日にテニスをする」という習慣を表す。B は be going to で「次の日曜日にテニスをする予定だ」という、前から決めている未来の予定を表す。"),
    ("I'll help you.", "Will you help me?",
     "A は will を使った肯定文で「（私が）あなたを手伝います」という話し手の意志（申し出）を表す。B は Will you ～? の疑問文で「（あなたが）私を手伝ってくれますか」と相手に頼む依頼の文になる。"),
    ("He won't come to the party.", "He doesn't come to the party.",
     "A は will not（won't）で「彼はパーティーに来ないだろう」と、これからのことを予想している。B は現在形の否定文で「彼は（いつも）そのパーティーには来ない」という習慣を表す。"),
    ("I called Ken yesterday.", "I'll call Ken tomorrow.",
     "A は過去形 called と yesterday で「昨日ケンに電話した」という過去の出来事。B は will＋原形 call と tomorrow で「明日ケンに電話します」という未来の意志を表す。"),
    ("I'm playing tennis now.", "I'm going to play tennis tomorrow.",
     "A は現在進行形 am playing で「今テニスをしているところだ」。B は be going to＋原形 play で「明日テニスをする予定だ」。どちらも I'm で始まるが、後ろが ing 形か going to＋原形かで意味が変わる。"),
    ("It will be sunny tomorrow.", "It was sunny yesterday.",
     "A は will be と tomorrow で「明日は晴れるでしょう」という未来の予想。B は was と yesterday で「昨日は晴れていた」という過去の様子。時を表す語句に合わせて be 動詞の形が変わっている。"),
    ("Will you be at home tomorrow?", "Are you at home now?",
     "A は will を使った疑問文で「明日、家にいますか（いる予定ですか）」と未来のことをたずねる。B は be 動詞の現在形の疑問文で「今、家にいますか」と現在の状態をたずねる。"),
    ("I'll answer the phone.", "I answer the phone.",
     "A は will で「（今鳴っている）電話に私が出ます」と、その場で決めた意志を表す。B は現在形で「（ふだん）私が電話に出る」という習慣を表す。"),
]


@gen("thinking_writing", 3, ["written_reasoning", "concept"])
def explain_difference(r):
    a, b, model = r.choice(PAIRS)
    return desc(f"次の2つの英文 A・B の意味の違いを、動詞の部分の形と時を表す語句に注目して日本語で説明しなさい。\nA：{a}\nB：{b}", model,
                "will・be going to・現在形・過去形・現在進行形は、それぞれ表す時と意味が違う。時を表す語句も手がかりになる。",
                [("A の形と意味を正しく説明している", 3), ("B の形と意味を正しく説明している", 3), ("違いを生む形や語句を指摘している", 2)], d=3, p=8, lines=5,
                ap="2つの文の動詞部分と時を表す語句に下線を引き、それぞれが過去・現在・未来のどれを、どんな気持ち（予想・意志・予定・依頼）で表しているかを考える。",
                steps=["A と B の動詞部分・時を表す語句を比べる。", "それぞれの形が表す時と意味を確かめる。", "和訳を示して違いを説明する。"],
                alt=["それぞれの文が使われる場面（だれが、いつ、何のために言うか）を考えて、場面の違いから説明する方法もある。"],
                pc=[("A の説明", 3), ("B の説明", 3), ("形の違いの指摘", 2)],
                pit=["和訳だけを書き、どの形が違いを生んでいるかを書かない。", "will と be going to をまったく同じ意味だと説明し、場面の違いに触れない。"])


IFS = [
    ("If it (be) sunny tomorrow, we (go) on a picnic.", "is", "will go", "if", "明日晴れたら、私たちはピクニックに行くでしょう。"),
    ("If you (be) free this evening, I (show) you my new game.", "are", "will show", "if", "今晩ひまなら、新しいゲームを見せてあげるよ。"),
    ("When Ken (come) home, I (give) him this letter.", "comes", "will give", "when", "ケンが帰ってきたら、この手紙を渡します。"),
    ("If it (rain) next Sunday, the game (be) canceled.", "rains", "will be", "if", "次の日曜日に雨が降ったら、試合は中止になるでしょう。"),
    ("When I (finish) my homework, I (call) you.", "finish", "will call", "when", "宿題が終わったら、あなたに電話します。"),
    ("If we (leave) now, we (catch) the train.", "leave", "will catch", "if", "今出発すれば、電車に間に合うでしょう。"),
    ("When my sister (arrive) at the station, she (send) me a message.", "arrives", "will send", "when", "姉は駅に着いたら、私にメッセージを送るでしょう。"),
    ("If you (need) help, I (help) you.", "need", "will help", "if", "助けが必要なら、私が手伝います。"),
]


@gen("thinking_writing", 2, ["cross_unit", "written_reasoning"], rel=["JH-ENG-G2-U03", "HS-ENG-U02"])
def if_clause(r):
    s, a1, a2, conj, jp = r.choice(IFS)
    model = f"前半 {a1}、後半 {a2}。理由：{conj} で始まる「時・条件」を表すまとまりの中では、未来のことでも現在形を使う（will は使わない）。主節（後半）は未来のことなので will＋原形にする。"
    return desc(f"次の英文の（　）内の語を適切な形に直しなさい（必要なら語を補うこと）。また、前半と後半で形が違う理由を説明しなさい。\n{s}\n（意味：{jp}）",
                model, f"{conj} の節（時・条件を表すまとまり）の中では、未来の内容でも現在形を使う。この規則は2年の接続詞の単元で詳しく学び、高校の時制の単元にもつながる。",
                [("前半を現在形（主語に合う形）にしている", 3), ("後半を will＋原形にしている", 2), ("時・条件のまとまりの中では未来でも現在形を使うことを説明している", 3)], d=4, p=8, lines=5,
                ap=f"文を {conj} のまとまりと、それ以外（主節）に分ける。主節は未来なので will、{conj} のまとまりは現在形にする。",
                steps=[f"{conj} ～ のまとまりと主節に分ける。", f"{conj} のまとまりの中は現在形：{a1}。", f"主節は未来のことなので will＋原形：{a2}。", "理由をまとめる。"],
                alt=[f"日本語でも「明日晴れる{'なら' if conj == 'if' else 'とき'}」のように、条件の部分は「晴れるだろうなら」とは言わないことと比べて確かめる。"],
                pc=[("前半の形", 3), ("後半の形", 2), ("理由", 3)],
                pit=["If it will be sunny tomorrow のように、条件の中にも will を使う。", "前半の主語が三人称単数のとき、s を落とす。"])


WRITE = [
    ("この週末の予定", "I'm going to visit my grandmother in Chiba this weekend. I'll help her in her garden. It will be a lot of fun.",
     "be going to で決めている予定、will で意志と予想を書いている。"),
    ("今度の夏休みにしたいこと", "I'm going to go to Hokkaido with my family this summer. We'll see many beautiful flowers there. I think it will be cool.",
     "be going to で予定、will で予想（We'll see / it will be cool）を書いている。"),
    ("将来の夢", "I want to be a nurse in the future. I'm going to study hard to be a good nurse. I'll help many sick people.",
     "be going to で決めていること、will で将来の意志を書いている。"),
    ("明日の部活動", "We are going to have a practice game tomorrow. I'll do my best. I think we will win the game.",
     "be going to で予定、will で意志と予想を書いている。"),
    ("家族の誕生日の計画", "My mother's birthday is next Sunday. I'm going to make a cake for her. She will be very happy.",
     "be going to で予定、will で予想（She will be happy）を書いている。"),
    ("次の休日の過ごし方", "I'm going to go to the city library next Saturday. I'll read some books about space. I won't play video games that day.",
     "be going to で予定、will / won't で意志を書いている。"),
    ("学校行事（合唱コンクール）に向けて", "Our chorus contest will be next month. Our class is going to practice every morning. We'll sing well.",
     "will で予想・意志、be going to で予定を書いている。"),
    ("修学旅行でしたいこと", "We are going to visit Kyoto on our school trip. I'm going to see many old temples. I'll buy some presents for my family.",
     "be going to で予定、will で意志を書いている。"),
]


@gen("thinking_writing", 3, ["application", "written_reasoning"])
def write_plan(r):
    topic, model, point = r.choice(WRITE)
    return desc(f"次のテーマについて、未来のことを伝える英文を3文で書きなさい。ただし、be going to と will をそれぞれ1回以上使い、未来を表す語句を1つ以上入れること。\nテーマ：{topic}",
                f"（解答例）{model}", f"（解答例の解説）{point} be going to も will も後ろは動詞の原形。形容詞や名詞の前には be を入れる。",
                [("be going to＋原形を正しく使っている", 2), ("will＋原形を正しく使っている", 2), ("未来を表す語句を正しく使っている", 2), ("3文の内容がテーマに合い、つながりが自然である", 2)], d=4, p=8, lines=5,
                ap="まず日本語で「決めている予定」「その日にすること・気持ち」「予想」を考え、予定は be going to、意志や予想は will に割りふる。",
                steps=["テーマに合う予定を1つ決め、be going to で書く。", "その日にすることや予想を will で書く。", "未来を表す語句（this weekend / next ～ / tomorrow など）を入れる。", "3文のつながりを見直す。"],
                alt=["書いた3文の動詞部分に下線を引き、will / going to の後ろがすべて原形になっているか、be の入れ忘れがないかを確かめる。"],
                pc=[("be going to の文", 2), ("will の文", 2), ("未来を表す語句", 2), ("内容のまとまり", 2)],
                pit=["I going to ～. のように be 動詞を落とす。", "It will fun. のように be を落とす。"])


TRANS = [
    ("明日は寒くなるでしょう。", "It will be cold tomorrow.", "cold は形容詞なので、will の後ろに be の原形 be が必要。"),
    ("私は来週、テストのために勉強するつもりです。", "I'm going to study for the test next week.", "前から決めている予定なので be going to＋原形 study（I will study ～. も可）。"),
    ("彼は今夜、テレビを見ないでしょう。", "He won't watch TV tonight.", "will の否定は won't（will not）＋原形。主語が三人称単数でも watch のまま。"),
    ("あなたは次の日曜日、ひまですか（ひまになりますか）。", "Will you be free next Sunday?", "free は形容詞なので be が必要。疑問文は Will を主語の前に出す（Are you going to be free ～? も可）。"),
    ("私の兄は来年、20歳になります。", "My brother will be twenty years old next year.", "年齢を表す語句の前に be が必要。主語が三人称単数でも will be。"),
    ("私たちはこの週末、キャンプに行く予定です。", "We are going to go camping this weekend.", "予定なので be going to。主語 We に合う be 動詞は are、to の後ろは原形 go。"),
    ("その店はあさって開くでしょう。", "The shop will open the day after tomorrow.", "open は動詞なので will＋原形 open。the day after tomorrow の前に前置詞はつけない。"),
    ("ユミは明日、学校に遅れないでしょう。", "Yumi won't be late for school tomorrow.", "late は形容詞なので won't の後ろに be が必要。"),
]


@gen("thinking_writing", 2, ["condition_check", "written_reasoning"])
def choose_form(r):
    jp, ans, why_s = r.choice(TRANS)
    return desc(f"次の日本語を英語に直しなさい。また、動詞の部分をその形にした理由を説明しなさい。\n{jp}", f"{ans}　理由：{why_s}",
                "will / be going to の後ろは動詞の原形。形容詞・名詞・場所を表す語句が続くときは be を入れる。be going to の be は主語に合わせる。",
                [("正しい英文を書いている", 4), ("will / be going to の後ろの形（原形・be の必要性）に触れて理由を説明している", 3), ("未来を表す語句を正しく使っている", 1)], d=4, p=8, lines=4,
                ap="日本語の述語が動作（～する）か、状態・様子（～だ・～になる・～にいる）かを考える。状態・様子なら will be ～ の形になる。",
                steps=["未来の文であることを確かめ、will か be going to かを決める。", "述語が動詞か、形容詞・名詞かを判断し、必要なら be を入れる。", "否定・疑問の形を整える。", f"答え：{ans}"],
                alt=["同じ内容を現在の文（It is cold. / He doesn't watch TV.）にしてから未来の形にかえ、be が必要かどうかを確かめる。"],
                pc=[("英文", 4), ("理由の説明", 3), ("未来を表す語句", 1)],
                pit=["It will cold. のように be を落とす。", "be going to の be を主語に合わせない。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(task, wrong, step, etype, tempt, fix, expl, steps, ap, alt, pit):
    return desc(f"{task}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい英文に書き直しなさい。", fix, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい英文に直している", 3), ("文法のルールを説明している", 1)], d=3, p=6, lines=4,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい英文", 3), ("ルールの説明", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix))


WILL_ERR = [
    ("ケンは明日、サッカーをするでしょう。", "Ken will plays soccer tomorrow.", "Ken will play soccer tomorrow.", "plays", "concept",
     "will の後ろの動詞は、主語が三人称単数でも原形。", "主語が Ken（三人称単数）なので s をつけると考えた。"),
    ("明日は晴れるでしょう。", "It will sunny tomorrow.", "It will be sunny tomorrow.", "will sunny", "concept",
     "sunny は形容詞なので、will の後ろに be が必要。", "日本語の「晴れる」を動詞のように感じ、sunny だけで足りると考えた。"),
    ("私は来年、北海道を訪れるつもりです。", "I will to visit Hokkaido next year.", "I will visit Hokkaido next year.", "will to", "concept",
     "will の直後に動詞の原形を置く。to は不要。", "be going to の to と混同した。"),
    ("彼女はその会議に来ないでしょう。", "She doesn't will come to the meeting.", "She won't come to the meeting.", "doesn't will", "concept",
     "will の文の否定は will の後ろに not（won't / will not）。doesn't は使わない。", "三人称単数の否定文は doesn't と覚えていた。"),
    ("トムは明日、来ますか。", "Does Tom will come tomorrow?", "Will Tom come tomorrow?", "Does Tom will", "concept",
     "will の疑問文は Will を主語の前に出す。does は使わない。", "一般動詞の疑問文と同じように Does を使った。"),
    ("あなたは今夜、家にいますか。", "Will you at home tonight?", "Will you be at home tonight?", "you at home", "concept",
     "at home（家に）の前に be が必要。Will you be at home ～?", "be 動詞の文の「いる」が will の文では消えると考えた。"),
    ("私の妹は来月、10歳になります。", "My sister wills be ten next month.", "My sister will be ten next month.", "wills", "concept",
     "will は主語によって形が変わらない。wills という形はない。", "三単現の s を will につけた。"),
    ("私は明日、早く起きるつもりです。", "I will getting up early tomorrow.", "I will get up early tomorrow.", "getting", "concept",
     "will の後ろは原形。getting を get にする。", "これからの動作なので ing 形を使うと考えた。"),
]


@gen("error_correction", 4, ["common_error", "computation"])
def err_will(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(WILL_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", etype, tempt, fix, f"{rule}正しくは {fix}",
                    ["will の後ろが動詞の原形になっているかを確認する。", "否定文・疑問文で do / does を使っていないか、形容詞・場所の前に be があるかを確認する。", f"正しい英文：{fix}"],
                    "will の文では、①will の形は変わらない、②後ろは動詞の原形、③否定・疑問は will 自身を使う、の3点をいつも確かめる。",
                    ["will を can に置きかえて読み、can の文としても正しい形かどうかで確かめる。"],
                    ["will の後ろの動詞に s・ing・to をつける。", "形容詞や場所の前の be を落とす。"])


GOING_ERR = [
    ("私は来週、おばを訪ねる予定です。", "I going to visit my aunt next week.", "I'm going to visit my aunt next week.", "I going", "concept",
     "be going to には be 動詞が必要。主語 I なので am（I'm）。", "going to だけで「予定」を表せると考えた。"),
    ("彼らは明日、テニスをする予定です。", "They is going to play tennis tomorrow.", "They are going to play tennis tomorrow.", "is", "condition",
     "主語 They は複数なので be 動詞は are。", "be going to の be はいつも is だと考えた。"),
    ("ユミは今度の日曜日、ケーキを作る予定です。", "Yumi is going to makes a cake next Sunday.", "Yumi is going to make a cake next Sunday.", "makes", "concept",
     "going to の後ろは原形。makes を make にする。", "主語が三人称単数なので s をつけると考えた。"),
    ("あなたはこの週末、買い物に行く予定ですか。", "Do you going to go shopping this weekend?", "Are you going to go shopping this weekend?", "Do", "concept",
     "be going to の疑問文は be 動詞 Are を主語の前に出す。", "一般動詞 go があるので Do を使うと考えた。"),
    ("私は今夜、テレビを見るつもりはありません。", "I'm not going watch TV tonight.", "I'm not going to watch TV tonight.", "going watch", "notation",
     "be going to の to を落とさない。going to＋原形。", "going と動詞の間の to を書き忘れた。"),
    ("私の兄は来年、高校生になる予定です。", "My brother is going to a high school student next year.", "My brother is going to be a high school student next year.", "going to a", "concept",
     "名詞の前には be が必要。going to be＋名詞。", "be 動詞 is がすでにあるので、もう be は不要だと考えた。"),
    ("私たちは次の夏、海で泳ぐ予定です。", "We are going to swimming in the sea next summer.", "We are going to swim in the sea next summer.", "swimming", "concept",
     "going to の後ろは原形。swimming を swim にする。", "現在進行形 are swimming と混同した。"),
    ("ケンは明日、図書館へ行く予定ではありません。", "Ken doesn't going to go to the library tomorrow.", "Ken isn't going to go to the library tomorrow.", "doesn't", "concept",
     "be going to の否定文は be 動詞の後ろに not（isn't）。", "三人称単数の否定文は doesn't と覚えていた。"),
]


@gen("error_correction", 3, ["common_error", "condition_check"])
def err_going(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(GOING_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", etype, tempt, fix, f"{rule}正しくは {fix}",
                    ["主語に合う be 動詞があるかを確認する。", "going to の後ろが動詞の原形か、to が抜けていないかを確認する。", f"正しい英文：{fix}"],
                    "be going to の文は「be 動詞の文」。①主語に合う be 動詞、②going to＋原形、③否定・疑問は be 動詞のルール、を確かめる。",
                    ["直した文を疑問文・否定文にしてみて、be 動詞の文として形がくずれないかを確かめる。"],
                    ["be 動詞を落とす。", "going to の後ろに ing 形や三単現の形を置く。"])


TIME_ERR = [
    ("私は昨日、祖母を訪ねました。", "I will visit my grandmother yesterday.", "I visited my grandmother yesterday.", "will visit", "interpretation",
     "yesterday は過去を表すので、will ではなく過去形 visited を使う。", "「訪ねる」という動作を未来の形で書いてしまい、時を表す語句と照らし合わせなかった。"),
    ("私たちは次の日曜日、動物園へ行く予定です。", "We went to the zoo next Sunday.", "We are going to go to the zoo next Sunday.", "went", "interpretation",
     "next Sunday は未来なので、過去形ではなく be going to（または will）を使う。", "「行く」を以前の出来事と同じように過去形で書いた。"),
    ("明日、雨が降ったら、私は家にいます。", "If it will rain tomorrow, I will stay home.", "If it rains tomorrow, I will stay home.", "will rain", "condition",
     "if で始まる条件のまとまりの中では、未来のことでも現在形を使う。主語 it なので rains。", "tomorrow があるので、if のまとまりの中にも will が必要だと考えた。"),
    ("次の日曜日に私は京都を訪れます。", "I will visit Kyoto on next Sunday.", "I will visit Kyoto next Sunday.", "on next Sunday", "notation",
     "next ～ の前には on などの前置詞をつけない。", "曜日の前には on をつけると覚えていた。"),
    ("ケンが来たら、出発しましょう。", "When Ken will come, let's start.", "When Ken comes, let's start.", "will come", "condition",
     "when で始まる時を表すまとまりの中では、未来のことでも現在形を使う。主語 Ken なので comes。", "これから来ることなので will が必要だと考えた。"),
    ("私の姉は2日前に東京へ行きました。", "My sister is going to go to Tokyo two days ago.", "My sister went to Tokyo two days ago.", "is going to go", "interpretation",
     "two days ago は過去を表すので、過去形 went を使う。", "「行く」という予定の言い方と過去の出来事を区別しなかった。"),
    ("彼は来年、中学生になります。", "He will be a junior high school student last year.", "He will be a junior high school student next year.", "last year", "interpretation",
     "「来年」は next year。last year は「去年」で、will と矛盾する。", "next と last の意味を取り違えた。"),
    ("あさって、私たちは試合をします。", "We will have a game next tomorrow.", "We will have a game the day after tomorrow.", "next tomorrow", "notation",
     "「あさって」は the day after tomorrow。next tomorrow という言い方はない。", "「明日の次」を next tomorrow と直訳した。"),
]


@gen("error_correction", 3, ["common_error", "condition_check"])
def err_time(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(TIME_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", etype, tempt, fix, f"{rule}正しくは {fix}",
                    ["時を表す語句に下線を引き、過去・現在・未来のどれかを確認する。", "動詞の形が時を表す語句と合っているか、条件・時のまとまりの中かどうかを確認する。", f"正しい英文：{fix}"],
                    "時を表す語句と動詞の形を照らし合わせる。when / if のまとまりの中は、未来のことでも現在形。",
                    ["正しい英文を日本語に訳し直し、問題の日本語の「時」と一致するかを確かめる。"],
                    ["時を表す語句を確かめずに動詞の形を決める。", "when / if のまとまりの中に will を入れる。"])


GENERATORS = [will_form, going_to_form, time_words, future_response, phrases,
              future_rewrite, wh_future, build_order, situation, dialog,
              explain_difference, if_clause, write_plan, choose_form,
              err_will, err_going, err_time]
