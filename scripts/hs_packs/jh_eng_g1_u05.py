"""単元パック：中学1年 英語 過去形（規則動詞・不規則動詞・be 動詞の過去形・過去進行形）。"""
import random

from banks._common import desc, mc, order, sa
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem,
                         tp)

UNIT_ID = "JH-ENG-G1-U05"

PREREQUISITES = [
    ("JH-ENG-G1-U01", "一般動詞と be 動詞の現在形、do / does を使う否定文・疑問文の作り方（過去形では did にかわる）。"),
    ("JH-ENG-G1-U04", "現在進行形 am / are / is＋ing 形と ing のつけ方（be 動詞を過去形にすると過去進行形になる）。"),
    ("JH-ENG-G1-U03", "what / where / when などの疑問詞で始まる疑問文の語順（Where did you go? で使う）。"),
]
EXTENSIONS = [
    ("JH-ENG-G2-U01", "過去・現在に続いて、will / be going to で未来のことを表し、時を表す語句で時制を使い分ける。"),
    ("JH-ENG-G2-U05", "不規則動詞の活用（原形・過去形・過去分詞）を覚えておくと、受け身の過去分詞にそのまま使える。"),
    ("JH-ENG-G3-U01", "現在完了形 have＋過去分詞は、過去の出来事が今とつながっていることを表す。過去形との違いが学習の中心になる。"),
    ("HS-ENG-U02", "高校では過去完了形や時・条件の副詞節など、時制の使い分けをさらに深める。"),
]

# 主語：(英語, was / were, 日本語, 代名詞)
SUBJ = [("I", "was", "私", "I"), ("You", "were", "あなた", "you"), ("He", "was", "彼", "he"), ("She", "was", "彼女", "she"),
        ("We", "were", "私たち", "we"), ("They", "were", "彼ら", "they"), ("Ken", "was", "ケン", "he"), ("Yumi", "was", "ユミ", "she"),
        ("My brother", "was", "私の兄", "he"), ("Tom and Mike", "were", "トムとマイク", "they"), ("My friends", "were", "私の友だち", "they"),
        ("Ms. Green", "was", "グリーン先生", "she")]
THIRD = [s for s in SUBJ if s[1] == "was" and s[0] != "I"]

# 動作：(原形, 過去形, ing 形, 三単現, 目的語など, 日本語の目的語部分, 「～した」, て形)
ACT = [
    ("play", "played", "playing", "plays", "tennis", "テニスを", "した", "して"),
    ("go", "went", "going", "goes", "to the library", "図書館へ", "行った", "行って"),
    ("eat", "ate", "eating", "eats", "breakfast", "朝食を", "食べた", "食べて"),
    ("make", "made", "making", "makes", "a cake", "ケーキを", "作った", "作って"),
    ("watch", "watched", "watching", "watches", "a movie", "映画を", "見た", "見て"),
    ("study", "studied", "studying", "studies", "math", "数学を", "勉強した", "勉強して"),
    ("write", "wrote", "writing", "writes", "a letter", "手紙を", "書いた", "書いて"),
    ("read", "read", "reading", "reads", "a magazine", "雑誌を", "読んだ", "読んで"),
    ("clean", "cleaned", "cleaning", "cleans", "the kitchen", "台所を", "掃除した", "掃除して"),
    ("buy", "bought", "buying", "buys", "some flowers", "花を", "買った", "買って"),
    ("swim", "swam", "swimming", "swims", "in the sea", "海で", "泳いだ", "泳いで"),
    ("visit", "visited", "visiting", "visits", "the museum", "博物館を", "訪れた", "訪れて"),
    ("take", "took", "taking", "takes", "pictures", "写真を", "とった", "とって"),
    ("listen", "listened", "listening", "listens", "to the radio", "ラジオを", "聞いた", "聞いて"),
    ("cook", "cooked", "cooking", "cooks", "lunch", "昼食を", "作った", "作って"),
    ("practice", "practiced", "practicing", "practices", "the piano", "ピアノを", "練習した", "練習して"),
    ("sing", "sang", "singing", "sings", "songs", "歌を", "歌った", "歌って"),
    ("draw", "drew", "drawing", "draws", "a picture", "絵を", "かいた", "かいて"),
    ("run", "ran", "running", "runs", "in the park", "公園で", "走った", "走って"),
    ("use", "used", "using", "uses", "the computer", "そのコンピューターを", "使った", "使って"),
]
ACT_ING = [a for a in ACT if a[0] != "go"]
TIME = [("yesterday", "昨日"), ("last Sunday", "この前の日曜日"), ("last night", "昨夜"), ("two days ago", "2日前"),
        ("last week", "先週"), ("this morning", "今朝"), ("last Saturday", "この前の土曜日")]
PTIME = [("at seven last night", "昨夜7時に"), ("at that time", "そのとき"), ("at three yesterday afternoon", "昨日の午後3時に"),
         ("when the phone rang", "電話が鳴ったとき"), ("at ten this morning", "今朝10時に")]

# 規則動詞：(原形, 過去形, つづりの型)
REG_RULE = {"ed": "そのまま ed をつける", "d": "e で終わるので d だけをつける", "ied": "「子音字＋y」で終わるので y を i にかえて ed をつける",
            "dbl": "「短母音＋子音字」で終わるので最後の子音字を重ねて ed をつける"}
REG = [("play", "played", "ed"), ("watch", "watched", "ed"), ("walk", "walked", "ed"), ("visit", "visited", "ed"), ("help", "helped", "ed"),
       ("clean", "cleaned", "ed"), ("cook", "cooked", "ed"), ("open", "opened", "ed"), ("enjoy", "enjoyed", "ed"), ("listen", "listened", "ed"),
       ("talk", "talked", "ed"), ("want", "wanted", "ed"), ("start", "started", "ed"), ("finish", "finished", "ed"), ("stay", "stayed", "ed"),
       ("use", "used", "d"), ("like", "liked", "d"), ("live", "lived", "d"), ("dance", "danced", "d"), ("practice", "practiced", "d"),
       ("arrive", "arrived", "d"), ("close", "closed", "d"), ("move", "moved", "d"),
       ("study", "studied", "ied"), ("try", "tried", "ied"), ("carry", "carried", "ied"), ("cry", "cried", "ied"),
       ("stop", "stopped", "dbl"), ("plan", "planned", "dbl"), ("drop", "dropped", "dbl")]
IRR = [("go", "went"), ("come", "came"), ("see", "saw"), ("eat", "ate"), ("have", "had"), ("get", "got"), ("make", "made"),
       ("take", "took"), ("buy", "bought"), ("write", "wrote"), ("give", "gave"), ("know", "knew"), ("run", "ran"), ("swim", "swam"),
       ("sing", "sang"), ("speak", "spoke"), ("tell", "told"), ("say", "said"), ("find", "found"), ("leave", "left"), ("meet", "met"),
       ("sleep", "slept"), ("teach", "taught"), ("think", "thought"), ("do", "did"), ("begin", "began"), ("drink", "drank"),
       ("sit", "sat"), ("stand", "stood"), ("catch", "caught"), ("bring", "brought"), ("lose", "lost"), ("feel", "felt"),
       ("put", "put"), ("cut", "cut"), ("win", "won"), ("fly", "flew"), ("draw", "drew"), ("ride", "rode"), ("forget", "forgot"),
       ("send", "sent"), ("hear", "heard"), ("wear", "wore")]

# -ed の発音
PRON = {"t": "[t]（ト）", "d": "[d]（ド）", "id": "[id]（イド）"}
PRON_WHY = {"t": "原形が [t] 以外の無声音（[k] [p] [s] [ʃ] [tʃ] など）で終わる", "d": "原形が [d] 以外の有声音（母音や [l] [n] [v] [z] など）で終わる",
            "id": "原形が [t] または [d] の音で終わる"}
ED = {"t": ["walked", "watched", "helped", "cooked", "looked", "finished", "stopped", "practiced", "danced", "liked", "talked", "washed", "jumped"],
      "d": ["played", "cleaned", "opened", "enjoyed", "listened", "lived", "used", "studied", "cried", "called", "stayed", "arrived", "moved"],
      "id": ["wanted", "visited", "started", "needed", "waited", "painted", "decided", "invited", "ended"]}


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
    goals=["規則動詞の過去形（-ed）を正しくつづり、-ed の3通りの発音を区別できる。",
           "よく使う不規則動詞の過去形を覚え、did を使う否定文・疑問文では動詞を原形にもどせる。",
           "be 動詞の過去形 was / were と、過去進行形 was / were＋ing 形を使い分けられる。"],
    duration=50,
    readiness=["一般動詞の現在形と do / does を使う否定文・疑問文を作れる（中1）。", "be 動詞 am / are / is と現在進行形を使える（中1）。",
               "yesterday, last ～, ～ ago など過去を表す語句の意味がわかる。",
               "小学校の外国語で I went to ～. / I enjoyed ～. / It was fun. などの表現にふれている。"],
    flow=[("導入：昨日の出来事", 5, "教師が週末の出来事を英語で話し、went, ate, was などの「過去の形」に気づかせる"),
          ("一般動詞の過去形", 15, "規則動詞のつづりと -ed の発音、不規則動詞、did を使う否定文・疑問文（例題1）"),
          ("be 動詞の過去形", 10, "was / were の使い分けと否定文・疑問文（例題2）"),
          ("過去進行形", 12, "was / were＋ing 形、「そのとき～していた」、過去形との違い（例題3）"),
          ("まとめと確認", 8, "現在・過去・進行形を表で比べ、確認問題3問")],
    sections=[
        intro("in1", "「過去」を表すと動詞の形が変わる",
              "日本語では「行く → 行った」のように文の終わりで過去を表します。英語では、動詞そのものの形をかえて過去を表します。I play tennis. の play を played にするだけで「テニスをした」という意味になります。この単元では、一般動詞・be 動詞・進行形のそれぞれを過去の形にする方法を学びます。",
              bullets=["I play tennis every day. → I played tennis yesterday.", "I go to the park. → I went to the park.（不規則動詞）",
                       "I am busy. → I was busy.", "I am reading. → I was reading at that time."],
              points=[tp("教師の週末の話を聞かせ、聞き取れた動詞を黒板に書き出させてから、現在の形と比べさせる。",
                         ask="went はどの動詞の形だと思うか。", expect="go の過去の形。", timing="導入の冒頭")]),
        definition("df1", "一般動詞の過去形",
                   "一般動詞の過去形は、主語が何であっても同じ形です。規則動詞は語尾に -ed をつけ、不規則動詞は1語ずつ形を覚えます。",
                   formula="主語＋動詞の過去形 ～.／否定：主語＋didn't＋動詞の原形 ～.／疑問：Did＋主語＋動詞の原形 ～?",
                   bullets=["-ed のつけ方：①そのまま（play → played）②e で終わる語は d（use → used）③子音字＋y は y → ied（study → studied）④短母音＋子音字は子音字を重ねる（stop → stopped）",
                            "-ed の発音：[t]（walked）、[d]（played）、[id]（wanted：原形が t / d の音で終わる語）",
                            "不規則動詞の例：go → went、see → saw、eat → ate、have → had、buy → bought、read → read（発音は [red]）",
                            "答え方：Did you ～? ― Yes, I did. / No, I didn't."],
                   conditions=["did / didn't を使ったら、動詞は必ず原形にもどす（× Did you went ～? / × I didn't went ～.）。",
                               "三人称単数の主語でも過去形に s はつかない（× He playeds）。"],
                   points=[tp("did は「過去を表す印」で、did が過去を引き受けるので後ろの動詞は原形にもどる、と説明する。",
                              ask="He went to Kyoto. を否定文にすると went はどうなるか。", expect="He didn't go to Kyoto.（went → go）",
                              caution="Did you went ～? の誤りは定期テストで最も多い。")]),
        definition("df2", "be 動詞の過去形と過去進行形",
                   "be 動詞の過去形は was と were の2つです。am / is の過去形が was、are の過去形が were です。過去進行形は be 動詞を過去形にした was / were＋ing 形で、「（過去のある時点で）～していた」を表します。",
                   formula="主語＋was / were ～.／主語＋was / were＋動詞の ing 形 ～.",
                   bullets=["I / he / she / it / 単数の名詞 → was", "you / we / they / 複数の名詞 → were",
                            "否定文：was not（wasn't）／were not（weren't）", "疑問文：Was / Were を主語の前に出す（Were you busy? ― Yes, I was.）",
                            "過去進行形の例：I was watching TV at eight last night.（昨夜8時にはテレビを見ていた）"],
                   conditions=["be 動詞の文では did を使わない（× I didn't busy. → I wasn't busy.）。",
                               "過去進行形は「過去の一時点でしている最中だった」こと。過去形は「（そのとき）～した」という出来事全体を表す。"],
                   points=[tp("「am と is → was、are → were」を現在形の対応表から導かせ、主語ごとに確認させる。",
                              ask="you が1人のときは was か were か。", expect="were（you はいつも are → were）。")]),
        theorem("th1", "過去の文を作るときの3つのルール",
                "一般動詞の文：過去形／didn't＋原形／Did ～＋原形?　be 動詞の文：was / were／wasn't / weren't／Was / Were ～?　過去進行形：was / were＋ing 形",
                ["文の中に be 動詞があるか、一般動詞だけかで、否定文・疑問文の作り方が決まる。",
                 "過去を表す語句（yesterday, last ～, ～ ago, then など）があれば過去の形にする。",
                 "疑問詞の疑問文も同じルール：Where did you go? ／ What were you doing then?"],
                body="現在形のルール（do / does と am / are / is）を、過去の形（did と was / were）にかえるだけです。新しく覚えることは少なく、「現在形の文の作り方」がそのまま使えます。",
                points=[tp("現在形と過去形の対応表（do / does → did、am / is → was、are → were）を作らせると、新しいルールが少ないことに気づける。")]),
        derivation("dv1", "否定文・疑問文の作り方（なぜ動詞が原形にもどるのか）",
                   ["① 現在形の否定文 He doesn't play tennis. では、does が「三人称単数・現在」を引き受け、play は原形になっていた。",
                    "② 過去の否定文でも同じしくみで、did が「過去」を引き受ける：He didn't play tennis yesterday.",
                    "③ だから did / didn't の後ろの動詞は原形にもどる。went → go、played → play。",
                    "④ be 動詞の文では、be 動詞そのものを過去形 was / were にし、not をつけたり前に出したりする（He wasn't busy. ／ Was he busy?）。",
                    "⑤ 過去進行形は be 動詞の文なので、④と同じルール：He wasn't playing tennis. ／ Was he playing tennis?"],
                   body="「過去を表すのは文の中で1か所だけ」と考えるとわかりやすくなります。did があれば動詞は原形、was / were があれば be 動詞が過去を担当しています。",
                   points=[tp("「過去の印は1つだけ」を合言葉に、Did ～ went? のように過去の印が2つある文を見つけさせる活動を行う。",
                              ask="Did you went ～? では過去の印がいくつあるか。", expect="did と went の2つ。", timing="導出の説明時")]),
        example("ex1", "例題1　一般動詞の過去形",
                "次の英文を、（　）内の指示に従って書きかえなさい。(1) Emi studies English every day.（every day を yesterday にかえて）　(2) Ken went to the zoo last Sunday.（疑問文にして、No で答える）",
                ["(1) study は「子音字＋y」で終わるので y を i にかえて ed：studied。", "(1) 過去形には三単現の s はつかない：Emi studied English yesterday.",
                 "(2) Did を主語の前に出し、went を原形 go にもどす：Did Ken go to the zoo last Sunday?", "(2) 答えは did を使う：No, he didn't."],
                "(1) Emi studied English yesterday.　(2) Did Ken go to the zoo last Sunday? ― No, he didn't.",
                thinking="過去を表す印（過去形・did）は文の中に1つ。did を使ったら動詞は原形にもどす。",
                points=[tp("(1) で studys の s を残して studysed などとする生徒がいるので、「まず原形にもどしてから過去形にする」手順を確認する。")],
                misconceptions=[("Did Ken went to the zoo last Sunday?", "did があるので went は原形 go にもどす。"),
                                ("Emi studyed English yesterday.", "子音字＋y で終わる語は y を i にかえて ed：studied。")]),
        example("ex2", "例題2　be 動詞の過去形",
                "日本語に合う英文を書きなさい。(1) 私たちは昨日とても疲れていました。　(2) あなたはそのとき図書館にいましたか。― いいえ、いませんでした。",
                ["(1) 主語 We なので be 動詞の過去形は were：We were very tired yesterday.", "(2) 主語 you なので Were を前に出す：Were you in the library then?",
                 "(2) 答えは主語を I にし、was を使う：No, I wasn't."],
                "(1) We were very tired yesterday.　(2) Were you in the library then? ― No, I wasn't.",
                thinking="形容詞（tired）や場所（in the library）が続くときは be 動詞の文。did は使わない。",
                points=[tp("(2) の答えで、Were you ～? に対して were ではなく was で答える理由（答えの主語が I になる）を確認させる。",
                           ask="Were you ～? に「はい」と答えると？", expect="Yes, I was.")]),
        example("ex3", "例題3　過去進行形と過去形",
                "日本語に合うように、（　）内の語を適切な形にしなさい。(1) 母が帰ってきたとき、私は宿題をしていました。When my mother came home, I (do) my homework.　(2) 昨夜、私は9時に寝ました。I (go) to bed at nine last night.",
                ["(1) 「～していた」は、ある時点で進行中だった動作なので過去進行形。主語 I なので was doing。",
                 "(2) 「寝た」は1回の出来事なので過去形。go は不規則動詞で went。"],
                "(1) was doing　(2) went",
                thinking="「その時点でしている最中だった」なら過去進行形、「～した」という出来事なら過去形。",
                figure=None,
                points=[tp("時間の線（タイムライン）を板書し、過去進行形は「点の前後に広がる帯」、過去形は「点」で表して違いを視覚化する。")],
                misconceptions=[("When my mother came home, I did my homework.", "「そのとき宿題をしていた最中」を表すには過去進行形 was doing を使う。")]),
        board("bd1", "板書案",
              [("① 一般動詞の過去形", ["played / used / studied / stopped", "-ed の発音：[t] [d] [id]", "go→went  see→saw  eat→ate", "否定：didn't＋原形", "疑問：Did ～＋原形?", "― Yes, I did. / No, I didn't."]),
               ("② be 動詞の過去形", ["am / is → was", "are → were", "I was busy.", "否定：wasn't / weren't", "疑問：Were you ～?", "― Yes, I was."]),
               ("③ 過去進行形", ["was / were＋ing", "I was reading then.", "（そのとき～していた）", "過去形＝点、過去進行形＝帯", "When ～, I was ～ing."])],
              points=[tp("①と②の列で、did と was / were のどちらが「過去の印」かを赤で示し、「過去の印は1つ」を強調する。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("不規則動詞は一度に全部覚えさせず、go / come / see / eat / have / make / take / buy など頻度の高いものから小テストで定着させる。", timing="単元の毎時間の帯活動"),
               tp("-ed の発音は、のどに手を当てて有声音・無声音を確かめさせると [t] と [d] の区別がつきやすい。",
                  ask="walk の最後の [k] を言うとき、のどはふるえるか。", expect="ふるえない（無声音）ので walked は [t]。"),
               tp("Did you ～? の答えでは did、Were you ～? の答えでは was / were を使うことを、ペアでの質問ゲームで反復させる。"),
               tp("過去進行形と過去形の違いは、日本語の「～していた」「～した」の違いと対応させて説明する。", caution="日本語の「～していた」が状態を表す場合（知っていた）は過去形 knew を使う。"),
               tp("問題プリント D の誤答例を「過去の印が2つある」「be 動詞と did の混同」「つづり」の3種類に分類させる。")],
              misconceptions=[("Did you went to the park?", "did があるので動詞は原形。Did you go to the park?"),
                              ("I didn't busy yesterday.", "busy は形容詞なので be 動詞の文。I wasn't busy yesterday."),
                              ("He goed to school.", "go は不規則動詞。He went to school."),
                              ("They was playing soccer.", "主語 They なので were。They were playing soccer.")]),
        summary("sm1", "まとめ",
                ["一般動詞の過去形：規則動詞は -ed（used / studied / stopped）、不規則動詞は1つずつ覚える。主語による変化はない。",
                 "否定文・疑問文は did を使い、動詞は原形にもどす（過去の印は1つ）。",
                 "be 動詞の過去形は was（am / is）と were（are）。過去進行形は was / were＋ing 形で「そのとき～していた」。"]),
        check("ck1", "確認問題",
              [("study, stop, buy の過去形を書きなさい。", "studied, stopped, bought"),
               ("Did she (come / came) to the party? の（　）から正しい語を選びなさい。", "come（did の後ろは原形）"),
               ("「私はそのとき、音楽を聞いていました」を英語で書きなさい。", "I was listening to music then (at that time).")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

@gen("basic_check", 4, ["computation", "common_error"])
def past_form(r):
    k = r.sample(list(REG_RULE), 2)
    regs = [r.choice([x for x in REG if x[2] == kk]) for kk in k]
    irr = r.choice(IRR)
    items = regs + [(irr[0], irr[1], "irr")]
    r.shuffle(items)
    stem = "次の動詞の過去形を書きなさい。\n" + "　".join(f"({i}) {x[0]}" for i, x in enumerate(items, 1))
    ans = "　".join(f"({i}) {x[1]}" for i, x in enumerate(items, 1))
    expl = "。".join(f"{x[0]} は" + (REG_RULE[x[2]] if x[2] != "irr" else "不規則動詞") + f"：{x[1]}" for x in items) + "。"
    return sa(stem, ans, expl, d=1, v=[", ".join(x[1] for x in items), " ".join(x[1] for x in items)],
              ap="まず規則動詞か不規則動詞かを見分ける。規則動詞なら語尾の形（e・子音字＋y・短母音＋子音字）で -ed のつけ方を決める。",
              steps=[f"{x[0]} → {x[1]}（" + (REG_RULE[x[2]] if x[2] != "irr" else "不規則動詞") + "）" for x in items],
              alt=["書いた過去形を使って I ～ yesterday. という短い文を声に出し、聞き覚えのある形かを確かめる。"],
              pc=[("規則動詞2つを正しく書いている", 1), ("不規則動詞を正しく書いている", 1)],
              pit=["不規則動詞に -ed をつける（goed, buyed）。", "y → ied や子音字を重ねるルールを忘れる（studyed, stoped）。"])


@gen("basic_check", 4, ["concept", "computation"])
def ed_pron(r):
    odd, base = r.sample(list(PRON), 2)
    same = r.sample(ED[base], 3)
    one = r.choice(ED[odd])
    why = {w: (f"{w} の -ed は{PRON[base]}と発音し、ほかの2つと同じ。{PRON_WHY[base]}語だから。", "-ed の発音の規則") for w in same}
    return mc(f"次の動詞の過去形のうち、-ed の部分の発音がほかの3つと異なるものを選びなさい。", [one] + same,
              f"{one} の -ed は{PRON[odd]}（{PRON_WHY[odd]}）。ほかの3つは{PRON[base]}（{PRON_WHY[base]}）。", d=2,
              ap="それぞれの原形の最後の音を確かめる。[t] [d] で終わるなら [id]、それ以外の無声音なら [t]、有声音なら [d]。",
              steps=["それぞれの原形にもどす。", "原形の最後の音を確かめ、[t] / [d] / [id] に分ける。", f"1つだけ違う {one}（{PRON[odd]}）を選ぶ。"],
              alt=["実際に声に出して読み、のどに手を当てて最後の音がふるえるか（有声音か）を確かめる。"],
              pc=[("原形の最後の音から -ed の発音を判断している", 1), ("異なるものを正しく選んでいる", 1)],
              pit=["つづりの最後の文字（e など）で判断し、音で判断しない。", "practiced や danced の最後の音（[s]）を有声音と考える。"], why=why)


BE_COMP = [("tired", "疲れていました"), ("hungry", "おなかがすいていました"), ("in the library", "図書館にいました"), ("happy", "うれしかったです"),
           ("at home", "家にいました"), ("late for school", "学校に遅刻しました"), ("excited", "わくわくしていました"), ("in Osaka", "大阪にいました"),
           ("sick in bed", "病気で寝ていました"), ("in the gym", "体育館にいました")]


@gen("basic_check", 4, ["computation", "condition_check"])
def be_past(r):
    s, wb, sj, _ = r.choice(SUBJ)
    comp, cj = r.choice(BE_COMP)
    t, tj = r.choice([x for x in TIME if not (comp == "late for school" and x[0] == "last night")])
    other = "were" if wb == "was" else "was"
    pres = {"I": "am"}.get(s, "is" if wb == "was" else "are")
    why = {other: (f"主語 {s} に合う be 動詞の過去形は {wb}。{other} は主語に合わない。", "主語と be 動詞の過去形の対応"),
           pres: (f"{t} は過去を表すので、現在形 {pres} ではなく過去形にする。", "時を表す語句と時制"),
           "did": (f"{comp} は動詞ではないので be 動詞が必要。did は一般動詞の過去の否定文・疑問文で使う。", "be 動詞と did の混同")}
    return mc(f"日本語に合うように、（　）に入る最も適切なものを選びなさい。\n{sj}は{tj}、{cj}。\n{s} (　　) {comp} {t}.", [wb] + list(why),
              f"{t}（{tj}）があるので過去の文。主語 {s} に合う be 動詞の過去形は {wb}。", d=1,
              ap="①時を表す語句で現在か過去かを決める、②主語で was / were を決める、の2段階で考える。",
              steps=[f"{t} があるので過去の文。", f"主語 {s} → {wb}（am / is → was、are → were）。", f"答え：{wb}"],
              alt=[f"現在の文 {s} {pres} {comp}. を作ってから、{pres} を過去形にして確かめる。"],
              pc=[("過去の文だと判断している", 1), ("主語に合う was / were を選んでいる", 1)],
              pit=["you に was を使う。", "形容詞や場所の前に did を置く。"], why=why)


@gen("basic_check", 4, ["computation", "common_error"])
def did_question(r):
    s, wb, sj, pr = r.choice([x for x in SUBJ if x[0] != "I"])
    v, past, ing, v3, obj, jo, jpast, jte = r.choice(ACT)
    t, tj = r.choice(TIME)
    if r.random() < 0.5:
        stem = f"日本語に合うように、（　）に入る最も適切なものを選びなさい。\n{sj}は{tj}、{jo}{jpast}のですか。\n(　　) {mid(s)} {v} {obj} {t}?"
        ok = "Did"
        why = {("Does" if wb == "was" else "Do"): (f"{t} は過去を表すので、現在の {'Does' if wb == 'was' else 'Do'} ではなく Did を使う。", "時を表す語句と時制"),
               cap(wb): (f"{v} は一般動詞なので、be 動詞 {cap(wb)} ではなく Did で疑問文を作る。", "be 動詞と did の混同"),
               "Didn't" if r.random() < 0.5 else "Done": ("「～したのですか」と単純にたずねる文なので Did を使う。", "疑問文の形")}
        if "Done" in why:
            why["Done"] = ("done は do の過去分詞で、疑問文の文頭には置けない。", "疑問文の形")
        else:
            why["Didn't"] = ("Didn't ～? は「～しなかったのですか」という否定の疑問文になり、日本語に合わない。", "疑問文の形")
        pts = ["文頭の語", "Did"]
    else:
        stem = f"日本語に合うように、（　）に入る最も適切なものを選びなさい。\n{sj}は{tj}、{jo}{jpast}のですか。\nDid {mid(s)} (　　) {obj} {t}?"
        ok = v
        why = {}
        if past != v:
            why[past] = ("Did があるので動詞は原形にもどす。過去の印は did の1つだけ。", "did の後ろの動詞の形")
        why[v3] = ("Did の後ろの動詞は原形。三単現の s はつけない。", "did の後ろの動詞の形")
        why[ing] = ("ing 形は be 動詞とともに使う。Did の後ろは原形。", "did の後ろの動詞の形")
        if past == v:
            why[f"to {v}"] = ("Did の後ろに to は置かない。", "did の後ろの動詞の形")
        pts = ["動詞の形", v]
    return mc(stem, [ok] + list(why),
              f"{t} があるので過去の一般動詞の疑問文。Did＋主語＋動詞の原形 ～? の形になる。答え：{ok}", d=2,
              ap="過去を表す語句と、文の動詞が一般動詞か be 動詞かを確かめる。一般動詞の過去の疑問文は Did＋主語＋原形。",
              steps=[f"{t} → 過去の文。", f"{v} は一般動詞 → Did を使う疑問文。", f"Did の後ろの動詞は原形。{pts[0]}は {pts[1]}。"],
              alt=[f"答えの文（Yes, {pr} did.）を作ってみて、疑問文と答えが対応しているかを確かめる。"],
              pc=[("過去の一般動詞の疑問文だと判断している", 1), ("正しい形を選んでいる", 1)],
              pit=["Did you went ～? のように、did と過去形を両方使う。", "一般動詞の文なのに Were / Was で始める。"], why=why)


@gen("basic_check", 4, ["computation", "condition_check"])
def past_prog(r):
    s, wb, sj, _ = r.choice(SUBJ)
    v, past, ing, v3, obj, jo, jpast, jte = r.choice(ACT_ING)
    t, tj = r.choice(PTIME)
    other = "were" if wb == "was" else "was"
    pres = {"I": "am"}.get(s, "is" if wb == "was" else "are")
    why = {f"{other} {ing}": (f"主語 {s} に合う be 動詞の過去形は {wb}。", "主語と be 動詞の過去形の対応"),
           f"{pres} {ing}": (f"{t} は過去の時点を表すので、現在進行形ではなく過去進行形にする。", "時を表す語句と時制"),
           f"{wb} {past if past != v else v + 's' if not v.endswith(('h', 's')) else v + 'es'}": ("was / were の後ろの動詞は ing 形にしないと過去進行形にならない。", "過去進行形の形")}
    return mc(f"日本語に合うように、（　）に入る最も適切なものを選びなさい。\n{sj}は{tj}、{jo}{jte}いました。\n{s} (　　) {obj} {t}.", [f"{wb} {ing}"] + list(why),
              f"「（過去のある時点で）～していた」は過去進行形 was / were＋ing 形。主語 {s} なので {wb} {ing}。", d=2,
              ap="「～していた」と過去の時点を表す語句から過去進行形と判断し、主語で was / were を決める。",
              steps=[f"{t}（{tj}）→ 過去のある時点。", "「～していた」→ 過去進行形（was / were＋ing 形）。", f"主語 {s} → {wb}。答え：{wb} {ing}"],
              alt=[f"現在進行形 {s} {pres} {ing} ～. を作り、be 動詞だけを過去形にして確かめる。"],
              pc=[("過去進行形だと判断している", 1), ("主語に合う was / were と ing 形を選んでいる", 1)],
              pit=["主語が複数なのに was を使う。", "was の後ろを過去形にする（was played）。"], why=why)


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 4, ["computation", "application"])
def past_rewrite(r):
    s, wb, sj, pr = r.choice(SUBJ)
    v, past, ing, v3, obj, jo, jpast, jte = r.choice(ACT)
    t, tj = r.choice(TIME)
    pres = v3 if wb == "was" and s != "I" else v
    kind = r.choice(["past", "neg", "q"]) if s != "I" else r.choice(["past", "neg"])
    if kind == "past":
        stem = f"次の英文の every day を {t} にかえて、過去の文に書きかえなさい。\n{s} {pres} {obj} every day."
        ans = f"{s} {past} {obj} {t}."
        v_ = None
        stp = [f"{t} は過去を表す。", f"{pres} を過去形 {past} にする（主語による変化はない）。", f"答え：{ans}"]
    elif kind == "neg":
        stem = f"次の英文を否定文に書きかえなさい。\n{s} {past} {obj} {t}."
        ans = f"{s} didn't {v} {obj} {t}."
        v_ = [f"{s} did not {v} {obj} {t}."]
        stp = ["一般動詞の過去の否定文は didn't＋原形。", f"{past} を原形 {v} にもどす。", f"答え：{ans}"]
    else:
        ans_s = "I" if s == "You" else pr
        stem = f"次の英文を疑問文に書きかえ、さらに No で答える文も書きなさい。\n{s} {past} {obj} {t}."
        ans = f"Did {mid(s)} {v} {obj} {t}? ― No, {ans_s} didn't."
        v_ = [f"Did {mid(s)} {v} {obj} {t}? ― No, {ans_s} did not."]
        stp = ["Did を主語の前に出す。", f"{past} を原形 {v} にもどす。", f"答えも did を使う：No, {ans_s} didn't.", f"答え：{ans}"]
    return sa(stem, ans, f"一般動詞の過去の文は、主語に関係なく過去形。否定文・疑問文は did を使い、動詞は原形にもどす。答え：{ans}", d=2, p=4, v=v_,
              ap="一般動詞の過去の否定文・疑問文では did が過去を表すので、動詞は原形にもどす。",
              steps=stp,
              alt=["書きかえた文の中に「過去の印」（過去形または did）が1つだけあるかを数えて確かめる。"],
              pc=[("did / 過去形の使い方が正しい", 2), ("動詞の形（原形・過去形）と語順が正しい", 2)],
              pit=["didn't の後ろも過去形のままにする。", "三単現の s を残したまま過去形にする。"])


WH = [
    ("Where", "go", "went", "to the aquarium", "last Sunday", "I went to the aquarium.", "When"),
    ("What", "eat", "ate", "curry and rice", "for dinner yesterday", "I ate curry and rice.", "Where"),
    ("What", "buy", "bought", "a new racket", "at the mall", "I bought a new racket.", "Who"),
    ("When", "visit", "visited", "last summer", "Okinawa", "I visited it last summer.", "Where"),
    ("Who", "meet", "met", "my old friend", "at the station", "I met my old friend.", "What time"),
    ("What time", "get", "got", "at six", "up this morning", "I got up at six.", "Where"),
    ("How", "come", "came", "by bus", "to school today", "I came by bus.", "Who"),
    ("Where", "find", "found", "under the desk", "your key", "I found it under the desk.", "When"),
    ("What", "make", "made", "a birthday card", "for your mother", "I made a birthday card.", "How"),
    ("Where", "take", "took", "at the beach", "these pictures", "I took them at the beach.", "Who"),
    ("When", "see", "saw", "last night", "the movie", "I saw it last night.", "Where"),
    ("What", "do", "did", "my homework", "after dinner", "I did my homework.", "Where"),
]


@gen("standard_practice", 4, ["cross_unit", "concept"], rel=["JH-ENG-G1-U03"])
def wh_past(r):
    wh, v, past, a, rest, ans, wrong_wh = r.choice(WH)
    ok = f"{wh} did you {v} {rest}?"
    why = {f"{wh} do you {v} {rest}?": ("B が過去形で答えているので、たずねる文も過去（did）にする。", "時制の対応"),
           f"{wh} did you {past} {rest}?": ("did を使ったら動詞は原形にもどす。過去の印は1つだけ。", "did の後ろの動詞の形"),
           f"{wrong_wh} did you {v} {rest}?": (f"B は「{a}」と答えているので、{wrong_wh} ではなく {wh} でたずねる文が合う。", "疑問詞と答えの対応")}
    return mc(f"次の対話が成り立つように、A の（　）に入る最も適切なものを選びなさい。\nA：(　　)\nB：{ans}", [ok] + list(why),
              f"B は「{a}」の部分で答えているので疑問詞は {wh}。過去の一般動詞の疑問文なので {wh}＋did＋主語＋原形。答え：{ok}", d=3,
              ap="B の答えのうち、どの部分が「たずねられた情報」なのかを見つけ、それに合う疑問詞を決める。時制は B の動詞（過去形）に合わせる。",
              steps=[f"B の答えの中心は「{a}」→ 疑問詞は {wh}。", f"B の動詞 {past} は過去形 → did を使う。", f"did の後ろは原形 {v}：{ok}"],
              alt=[f"選んだ疑問文の {wh} の位置に「{a}」を入れて普通の文にもどし、B の答えと同じ内容になるかを確かめる。"],
              pc=[("疑問詞を正しく選んでいる", 2), ("did＋原形の形を選んでいる", 2)],
              pit=["did の後ろも過去形にする。", "答えの内容と合わない疑問詞を選ぶ。"], why=why)


ORDERS = [
    ("私は昨日、おばの家を訪れました。", ["I", "visited", "my aunt's", "house", "yesterday"], "一般動詞の過去形 visited"),
    ("あなたはこの前の日曜日、どこへ行きましたか。", ["where", "did", "you", "go", "last", "Sunday"], "疑問詞＋did＋主語＋原形"),
    ("彼はその知らせを知りませんでした。", ["he", "didn't", "know", "the", "news"], "didn't＋原形 know"),
    ("その映画はおもしろかったですか。", ["was", "the", "movie", "interesting"], "be 動詞の過去の疑問文：Was＋主語"),
    ("私たちは昨日、学校にいませんでした。", ["we", "were", "not", "at", "school", "yesterday"], "be 動詞の過去の否定文：were not"),
    ("私が電話したとき、ケンは風呂に入っていました。", ["Ken", "was", "taking", "a bath", "when", "I", "called", "him"], "過去進行形＋when の節"),
    ("あなたはそのとき何をしていたのですか。", ["what", "were", "you", "doing", "then"], "疑問詞＋were＋主語＋doing"),
    ("彼女は昨夜、2時間勉強しました。", ["she", "studied", "for", "two hours", "last", "night"], "study → studied"),
    ("私の兄は先週、新しい自転車を買いました。", ["my brother", "bought", "a new bike", "last", "week"], "不規則動詞 buy → bought"),
    ("子どもたちは公園でサッカーをしていました。", ["the children", "were", "playing", "soccer", "in", "the park"], "過去進行形：were＋ing"),
    ("私は今朝、7時に起きました。", ["I", "got", "up", "at", "seven", "this", "morning"], "不規則動詞 get → got"),
    ("その試合はとてもわくわくするものでした。", ["the", "game", "was", "very", "exciting"], "be 動詞の過去形 was"),
    ("あなたは昨日、その本を読みましたか。", ["did", "you", "read", "the", "book", "yesterday"], "Did＋主語＋原形 read"),
    ("私たちはその店で何も買いませんでした。", ["we", "didn't", "buy", "anything", "at", "the shop"], "didn't＋原形、否定文の anything"),
]


@gen("standard_practice", 4, ["application", "computation"])
def build_order(r):
    jp, parts, pat = r.choice(ORDERS)
    sent = cap(" ".join(parts)) + ("?" if jp.endswith("か。") else ".")
    return order(f"日本語に合うように、次の語句を並べかえて英文を完成させなさい。ただし、文頭にくる語も小文字で示してある。\n{jp}", parts,
                 f"{sent}　ポイント：{pat}。", d=2, p=4,
                 ap="日本語の文末（～した／～しなかった／～したか／～していた）から文の型を決め、主語と動詞の部分から組み立てる。",
                 steps=[f"文の型を決める：{pat}。", "主語と動詞（did / was / were を含む）の部分を作る。", "目的語・場所・時の語句を後ろに並べる。", f"完成文：{sent}"],
                 alt=["完成した英文を日本語に訳し直して、問題の日本語と一致するかを確かめる。"],
                 pc=[("主語と動詞の部分の語順が正しい", 2), ("目的語・修飾語句の順序が正しい", 2)],
                 pit=["did の後ろに過去形を置く。", "場所と時を表す語句の順（場所 → 時）を逆にする。"])


@gen("standard_practice", 4, ["concept", "condition_check"])
def past_response(r):
    kind = r.choice(["did", "were_you", "was_3", "prog"])
    yes = r.random() < 0.5
    t, tj = r.choice(TIME)
    if kind == "did":
        s, wb, sj, pr = r.choice(THIRD + [("You", "were", "あなた", "you")])
        v, past, ing, v3, obj, *_ = r.choice(ACT)
        q = f"Did {mid(s)} {v} {obj} {t}?"
        a = "I" if s == "You" else pr
        ok = f"Yes, {a} did." if yes else f"No, {a} didn't."
        why = {(f"Yes, {a} {'was' if a in ('I', 'he', 'she') else 'were'}." if yes else f"No, {a} {'wasn' if a in ('I', 'he', 'she') else 'weren'}'t."): ("Did ～? の疑問文には did を使って答える。be 動詞は使わない。", "be 動詞と did の混同"),
               (f"Yes, {a} {past}." if yes and past != v else f"Yes, {a} does." if yes else f"No, {a} {'doesn' if a in ('he', 'she') else 'don'}'t."): ("Did ～? は過去の疑問文なので、答えも did（didn't）を使う。", "時制の対応"),
               (f"Yes, {'you' if s == 'You' else 'I'} did." if yes else f"No, {'you' if s == 'You' else 'I'} didn't."): ("答えの主語は、たずねられた人を代名詞にしたもの（you → I、人の名前 → he / she）。", "答えの主語")}
    elif kind == "were_you":
        comp = r.choice(["busy", "at home", "tired", "in the classroom", "hungry", "sick"])
        q = f"Were you {comp} {t}?"
        ok = "Yes, I was." if yes else "No, I wasn't."
        why = {("Yes, I were." if yes else "No, I weren't."): ("答えの主語は I なので、be 動詞は was を使う。", "主語と be 動詞の過去形の対応"),
               ("Yes, I did." if yes else "No, I didn't."): ("Were you ～? は be 動詞の疑問文なので、did ではなく was で答える。", "be 動詞と did の混同"),
               ("Yes, you were." if yes else "No, you weren't."): ("you でたずねられたら、自分のことなので I で答える。", "答えの主語")}
    elif kind == "was_3":
        s, wb, sj, pr = r.choice(THIRD)
        comp = r.choice(["kind", "at the party", "in the gym", "busy", "happy", "angry"])
        q = f"Was {mid(s)} {comp} {t}?"
        ok = f"Yes, {pr} was." if yes else f"No, {pr} wasn't."
        why = {(f"Yes, {pr} did." if yes else f"No, {pr} didn't."): ("Was ～? は be 動詞の疑問文なので、was で答える。", "be 動詞と did の混同"),
               (f"Yes, {pr} is." if yes else f"No, {pr} isn't."): ("過去の疑問文なので、答えも過去形 was を使う。", "時制の対応"),
               (f"Yes, {pr} were." if yes else f"No, {pr} weren't."): (f"主語 {pr} に合う be 動詞の過去形は was。", "主語と be 動詞の過去形の対応")}
    else:
        s, wb, sj, pr = r.choice([x for x in SUBJ if x[0] not in ("I", "We")])
        v, past, ing, v3, obj, *_ = r.choice(ACT_ING)
        pt, ptj = r.choice(PTIME[:3] + PTIME[4:])
        q = f"{cap(wb)} {mid(s)} {ing} {obj} {pt}?"
        a = "I" if s == "You" else pr
        ab = "was" if a in ("I", "he", "she") else "were"
        ok = f"Yes, {a} {ab}." if yes else f"No, {a} {ab}n't."
        why = {(f"Yes, {a} did." if yes else f"No, {a} didn't."): (f"{cap(wb)} ～ing? は過去進行形（be 動詞の文）の疑問文なので、be 動詞で答える。", "be 動詞と did の混同"),
               (f"Yes, {a} {ing}." if yes else f"No, {a} not {ing}."): ("答えの文では be 動詞（was / were）を使い、ing 形は省く。", "答えの形"),
               (f"Yes, {a} {'is' if ab == 'was' and a != 'I' else 'am' if a == 'I' else 'are'}." if yes else f"No, {a} {'isn' if ab == 'was' and a != 'I' else 'aren' if ab == 'were' else 'wasn'}'t."): ("過去の疑問文なので、答えも過去形の be 動詞を使う。", "時制の対応")}
        if not yes and a == "I":
            why.pop("No, I wasn't.", None)
            why["No, I'm not."] = ("過去の疑問文なので、答えも過去形の be 動詞を使う。", "時制の対応")
    yn = "「はい」" if yes else "「いいえ」"
    return mc(f"次の質問に{yn}と答えるとき、最も適切なものを選びなさい。\n{q}", [ok] + [w for w in why if w != ok][:3],
              f"答え：{ok}。質問の文頭（Did / Was / Were）に合わせ、答えの主語を代名詞にして答える。", d=2, p=4,
              ap="質問の最初の語（Did / Was / Were）を見て、答えに使う語を決める。答えの主語は代名詞にする。",
              steps=["質問の文頭を確認する（一般動詞の文か be 動詞の文か）。", "答えの主語を決める（you → I、人の名前 → he / she / they）。", f"答え：{ok}"],
              alt=["答えの文に省略された部分を補ってみて（Yes, I did go ～. は言わないが、No, I didn't go ～. は成り立つ）、形が正しいかを確かめる。"],
              pc=[("答えに使う語（did / was / were）を正しく選んでいる", 2), ("主語・時制が正しい", 2)],
              pit=["Were you ～? に Yes, I were. と答える。", "Did ～? に be 動詞で答える。"],
              why={w: why[w] for w in [w for w in why if w != ok][:3]})


DIARY_PLACE = [("the zoo", "動物園", ["took many pictures", "ate sandwiches", "saw a lot of animals"]),
               ("the beach", "海辺", ["swam in the sea", "ate sandwiches", "took many pictures"]),
               ("the city library", "市立図書館", ["read many books", "studied for two hours"]),
               ("Minato Park", "みなと公園", ["played badminton", "ate sandwiches", "walked for two hours"]),
               ("the science museum", "科学博物館", ["learned about dinosaurs", "saw a big rocket"])]
DIARY_WHO = [("my sister", "姉"), ("my friend Aya", "友だちのアヤ"), ("my father", "父"), ("my cousin", "いとこ")]
DIARY_WEATHER = [("sunny", "晴れ"), ("cloudy", "くもり")]  # 互いに両立しない天気だけを使う
DIARY_HOME = [("was cooking dinner", "夕食を作っていた"), ("was watching TV", "テレビを見ていた"), ("was reading a newspaper", "新聞を読んでいた"),
              ("was washing the car", "車を洗っていた")]
DIARY_HOMEWHO = [("my mother", "母"), ("my grandfather", "祖父"), ("my brother", "兄")]


@gen("standard_practice", 4, ["application", "concept"])
def diary(r):
    pl, plj, dos = r.choice(DIARY_PLACE)
    who, whoj = r.choice(DIARY_WHO)
    w, wj = r.choice(DIARY_WEATHER)
    dd = r.choice(dos)
    hw, hwj = r.choice(DIARY_HOMEWHO)
    hd, hdj = r.choice(DIARY_HOME)
    day, dayj = r.choice([("Last Sunday", "この前の日曜日"), ("Last Saturday", "この前の土曜日"), ("Yesterday", "昨日")])
    text = (f"{day}, I went to {pl} with {who}. It was {w}. We {dd} there. "
            f"When we came home, {hw} {hd}. I was tired, but I had a good time.")
    ok = f"筆者が帰宅したとき、{hwj}は{hdj}。"
    other_w = r.choice([x for x in DIARY_WEATHER if x[0] != w])
    other_hd = r.choice([x for x in DIARY_HOME if x[0] != hd])
    other_who = r.choice([x for x in DIARY_WHO if x[0] != who])
    wrongs = {f"{dayj}は{other_w[1]}{'だった' if other_w[1] in ('晴れ', 'くもり') else ''}。": f"本文は It was {w}. で、{wj}{'だった' if wj in ('晴れ', 'くもり') else ''}と書かれている。",
              f"筆者は{other_who[1]}といっしょに{plj}へ行った。": f"本文には with {who}（{whoj}と）とある。",
              f"筆者が帰宅したとき、{hwj}は{other_hd[1]}。": f"本文には {hw} {hd}（{hdj}）とある。過去進行形の動詞の部分を確かめる。"}
    return mc(f"次の英文は、中学生が書いた日記です。内容に合うものを1つ選びなさい。\n{text}", [ok] + list(wrongs),
              f"When we came home, {hw} {hd}. は過去進行形で「私たちが帰宅したとき、{hwj}は{hdj}」という意味。", d=3,
              ap="選択肢の内容（だれが・どこで・何を・どんな様子）を本文の中で1つずつ探し、動詞の形（過去形・過去進行形）にも注意して照らし合わせる。",
              steps=["選択肢ごとに、本文の該当する文を見つける。", f"When we came home, {hw} {hd}. は過去進行形で「（帰宅したとき）～していた」。", f"内容が一致する「{ok}」を選ぶ。"],
              alt=["本文を1文ずつ日本語に訳してメモし、選択肢と表にして比べる。"],
              pc=[("本文の該当箇所を見つけている", 2), ("過去形・過去進行形の意味を正しく読み取っている", 2)],
              pit=["過去進行形の文を「帰宅してから～した」と、順番の出来事として読んでしまう。", "選択肢の一部だけを見て判断する。"],
              why={k: (v, "本文の内容の読み取り") for k, v in wrongs.items()})


# ======================================================================
# C 思考力・記述応用
# ======================================================================

PAIRS = [
    ("I play the piano.", "I played the piano.",
     "A は現在形で「私は（ふだん）ピアノをひく」という今の習慣を表す。B は過去形 played で「私は（過去に）ピアノをひいた」という過去の出来事を表す。"),
    ("I was reading a book at nine.", "I read a book at nine.",
     "A は過去進行形で「9時には本を読んでいる最中だった」という、過去の一時点で進行中だった動作を表す。B は過去形で「9時に本を読んだ（読み始めた）」という過去の出来事を表す。"),
    ("Did you go to the park?", "Were you in the park?",
     "A は一般動詞 go の過去の疑問文で「公園へ行きましたか」と行動をたずねる。B は be 動詞の過去の疑問文で「公園にいましたか」と、そこにいたかどうか（状態）をたずねる。"),
    ("When I came home, my mother cooked dinner.", "When I came home, my mother was cooking dinner.",
     "A は過去形で「私が帰宅したとき（帰宅してから）、母は夕食を作った」という出来事の順番を表す。B は過去進行形で「私が帰宅したとき、母は夕食を作っている最中だった」という、その時点で進行中だった動作を表す。"),
    ("It is cold today.", "It was cold yesterday.",
     "A は be 動詞の現在形 is で「今日は寒い」という今の状態を表す。B は過去形 was で「昨日は寒かった」という過去の状態を表す。時を表す語句（today / yesterday）とも対応している。"),
    ("He didn't study.", "He wasn't studying.",
     "A は一般動詞の過去の否定文で「彼は勉強しなかった」と、勉強という出来事がなかったことを表す。B は過去進行形の否定文で「彼は（そのとき）勉強しているところではなかった」と、ある時点での様子を表す。"),
    ("What did you do?", "What were you doing?",
     "A は過去形の疑問文で「何をしましたか」と過去の行動をたずねる。B は過去進行形の疑問文で「（そのとき）何をしていましたか」と、過去の一時点で進行中だった動作をたずねる。"),
    ("I am busy now.", "I was busy then.",
     "A は be 動詞の現在形 am で「私は今忙しい」。B は過去形 was で「私はそのとき忙しかった」。どちらも be 動詞の文で、時を表す語句（now / then）に合わせて形がかわる。"),
]


@gen("thinking_writing", 3, ["written_reasoning", "concept"])
def explain_difference(r):
    a, b, model = r.choice(PAIRS)
    return desc(f"次の2つの英文 A・B の意味の違いを、動詞の形（時制）に注目して日本語で説明しなさい。\nA：{a}\nB：{b}", model,
                "動詞の形（現在形・過去形・過去進行形）と、be 動詞の文か一般動詞の文かによって、表す時と意味が変わる。",
                [("A の動詞の形と意味を正しく説明している", 3), ("B の動詞の形と意味を正しく説明している", 3), ("違いを生む形（過去形・was / were＋ing など）を指摘している", 2)], d=3, p=8, lines=5,
                ap="2つの文の動詞部分に下線を引き、それぞれがどの時制（現在・過去・過去進行形）か、be 動詞の文か一般動詞の文かを確かめる。",
                steps=["A と B の動詞部分を比べ、違いを見つける。", "それぞれの時制が表す意味（今の習慣・過去の出来事・過去の進行中の動作・状態）を確かめる。", "和訳を示して違いを説明する。"],
                alt=["それぞれの文を時間の線（タイムライン）に表し、点（過去形）と帯（過去進行形）の違いで説明する方法もある。"],
                pc=[("A の説明", 3), ("B の説明", 3), ("形の違いの指摘", 2)],
                pit=["和訳だけで、どの形が違いを生んでいるかを書かない。", "過去進行形と過去形を同じ意味だと考える。"])


FORM_SUBJ = [("Ken", "ケン"), ("My sister", "私の姉"), ("Emi", "エミ"), ("Our teacher", "私たちの先生"), ("Tom", "トム")]
FORM_ACT = [("play", "played", "playing", "plays", "soccer"), ("swim", "swam", "swimming", "swims", "in the river"),
            ("make", "made", "making", "makes", "lunch"), ("study", "studied", "studying", "studies", "science"),
            ("write", "wrote", "writing", "writes", "an email"), ("run", "ran", "running", "runs", "in the park"),
            ("read", "read", "reading", "reads", "comics"), ("watch", "watched", "watching", "watches", "the news"),
            ("practice", "practiced", "practicing", "practices", "kendo")]


@gen("thinking_writing", 3, ["cross_unit", "written_reasoning"], rel=["JH-ENG-G1-U01", "JH-ENG-G1-U04"])
def four_forms(r):
    s, sj = r.choice(FORM_SUBJ)
    v, past, ing, v3, obj = r.choice(FORM_ACT)
    model = (f"(1) {v3}　(2) {past}　(3) {ing}　(4) {v}。理由：(1) every Saturday は今の習慣で、主語 {s} は三人称単数なので現在形に s（es）をつける。"
             f"(2) yesterday があるので過去形。(3) was と at four yesterday があるので過去進行形の ing 形。(4) didn't の後ろは原形。")
    return desc(f"（　）内の動詞 {v} を、それぞれ適切な形に直しなさい。また、(1)～(4) で形が変わる理由を説明しなさい。\n(1) {s} (　　) {obj} every Saturday.\n(2) {s} (　　) {obj} yesterday.\n(3) {s} was (　　) {obj} at four yesterday.\n(4) {s} didn't (　　) {obj} last week.",
                model, "同じ主語・同じ動詞でも、時を表す語句と、動詞の前にある語（何もない・was・didn't）で形が決まる。前の単元で学んだ三単現・現在進行形のルールとあわせて整理する。",
                [("(1)～(4) の形をすべて正しく書いている", 4), ("時を表す語句から時制を判断した理由を書いている", 2), ("was＋ing・didn't＋原形の理由を書いている", 2)], d=4, p=8, lines=5,
                ap="それぞれの文の時を表す語句（every ～ / yesterday / at four yesterday / last week）と、動詞の直前の語（was / didn't）を確かめる。",
                steps=[f"(1) 現在の習慣・三人称単数 → {v3}。", f"(2) 過去の出来事 → {past}。", f"(3) was＋ing の過去進行形 → {ing}。", f"(4) didn't の後ろ → 原形 {v}。"],
                alt=["(1)～(4) をそれぞれ疑問文にしてみる（Does / Did / Was / Did）と、どのルールの文かがはっきりする。"],
                pc=[("4つの形", 4), ("時制の理由", 2), ("was＋ing・didn't＋原形の理由", 2)],
                pit=["(4) で didn't の後ろを過去形にする。", "(1) の三単現の s を忘れる。"])


WRITE = [
    ("この前の週末にしたこと", "Last Sunday was sunny. I went to the park with my brother. When we arrived there, many children were playing soccer.",
     "be 動詞の過去形 was、一般動詞の過去形 went、過去進行形 were playing を1文ずつ使っている。"),
    ("夏休みの思い出", "I visited my grandparents in Nagano this summer. It was cool there. One evening, we were watching fireworks by the river.",
     "visited（規則動詞の過去形）、was（be 動詞の過去形）、were watching（過去進行形）を使っている。"),
    ("昨日の放課後のこと", "I was very busy yesterday. After school, I practiced basketball for two hours. When I got home, my sister was doing her homework.",
     "was（be 動詞）、practiced（一般動詞の過去形）、was doing（過去進行形）を使っている。"),
    ("家族と出かけた日のこと", "Last Saturday, my family went to the aquarium. The dolphins were very cute. When we were watching the dolphin show, a dolphin jumped very high.",
     "went（不規則動詞の過去形）、were（be 動詞）、were watching（過去進行形）、jumped（規則動詞の過去形）を使っている。"),
    ("学校行事（運動会）の日のこと", "Our sports day was last Friday. I ran in the relay. When I was running, my friends were cheering for me.",
     "was（be 動詞）、ran（不規則動詞の過去形）、was running / were cheering（過去進行形）を使っている。"),
    ("雨の日の過ごし方", "It was rainy last Sunday. I stayed home and read a book. At three, my father was making pancakes for us.",
     "was（be 動詞）、stayed / read（過去形）、was making（過去進行形）を使っている。"),
    ("家族で出かけた冬の日のこと", "Last month, I went skiing with my family. It was difficult, but fun. When I was skiing, I fell down many times.",
     "went / fell（不規則動詞の過去形）、was（be 動詞）、was skiing（過去進行形）を使っている。"),
    ("友だちの誕生日パーティー", "Yesterday was Aya's birthday. We made a cake for her. When she came into the room, we were singing a birthday song.",
     "was（be 動詞）、made / came（不規則動詞の過去形）、were singing（過去進行形）を使っている。"),
]


@gen("thinking_writing", 2, ["application", "written_reasoning"])
def write_diary(r):
    topic, model, point = r.choice(WRITE)
    return desc(f"次のテーマについて、過去のことを伝える英文を3文で書きなさい。ただし、be 動詞の過去形・一般動詞の過去形・過去進行形をそれぞれ1回以上使うこと。\nテーマ：{topic}",
                f"（解答例）{model}", f"（解答例の解説）{point} 一般動詞の過去形は不規則動詞に注意し、過去進行形は「そのとき～していた」場面で使う。",
                [("be 動詞の過去形を正しく使っている", 2), ("一般動詞の過去形を正しく使っている", 2), ("過去進行形を正しく使い、場面に合っている", 2), ("3文の内容がテーマに合い、つながりが自然である", 2)], d=4, p=8, lines=5,
                ap="まず日本語で「いつ・どこで・何をした・そのときの様子」を決め、どの文にどの形を使うかを割りふってから英語にする。",
                steps=["テーマに合う出来事を1つ決める。", "様子・感想（It was ～. / I was ～.）を be 動詞の過去形で書く。", "したことを一般動詞の過去形で書く。", "「そのとき～していた」場面を過去進行形で書く。"],
                alt=["書いた3文の動詞に下線を引き、条件の3つの形がそろっているか、過去の印が各文に1つずつあるかを確かめる。"],
                pc=[("be 動詞の過去形", 2), ("一般動詞の過去形", 2), ("過去進行形", 2), ("内容のまとまり", 2)],
                pit=["不規則動詞に -ed をつける（goed, eated）。", "過去進行形の be 動詞を現在形（am / is）にする。"])


TRANS = [
    ("私は昨日、その答えを知りませんでした。", "I didn't know the answer yesterday.", "know は一般動詞なので、過去の否定文は didn't＋原形 know。be 動詞は使わない。"),
    ("あなたは昨夜、家にいましたか。", "Were you at home last night?", "「家にいた」は be 動詞で表す（at home）。主語 you なので Were を前に出す。"),
    ("ユミは今朝、学校に遅刻しました。", "Yumi was late for school this morning.", "late は形容詞なので be 動詞の文。主語 Yumi なので was。"),
    ("私たちは昨日、たくさんの星を見ました。", "We saw a lot of stars yesterday.", "see は不規則動詞で過去形は saw。一般動詞の肯定文なので did は使わない。"),
    ("トムはそのとき、手紙を書いていました。", "Tom was writing a letter then.", "「そのとき～していた」は過去進行形。主語 Tom なので was、write は e をとって writing。"),
    ("彼らは先週の日曜日、テニスをしませんでした。", "They didn't play tennis last Sunday.", "play は一般動詞なので、過去の否定文は didn't＋原形 play。"),
    ("その本はおもしろかったですか。", "Was the book interesting?", "interesting は形容詞なので be 動詞の文。主語 the book なので Was を前に出す。"),
    ("あなたは昨日、どこで昼ごはんを食べましたか。", "Where did you have (eat) lunch yesterday?", "eat / have は一般動詞なので、疑問詞＋did＋主語＋原形。"),
]


@gen("thinking_writing", 2, ["condition_check", "written_reasoning"])
def choose_form(r):
    jp, ans, why_s = r.choice(TRANS)
    return desc(f"次の日本語を英語に直しなさい。また、did と was / were のどちらを使ったか（または使わなかったか）、その理由を説明しなさい。\n{jp}", f"{ans}　理由：{why_s}",
                "文の中心が一般動詞なら did、形容詞や場所（at home など）が続くなら be 動詞 was / were を使う。過去進行形も be 動詞の文。",
                [("正しい英文を書いている", 4), ("一般動詞の文か be 動詞の文かに触れて理由を説明している", 3), ("主語に合う形・動詞の形が正しい", 1)], d=4, p=8, lines=4,
                ap="日本語の述語が「動作（～した）」か「状態・様子（～だった・～にいた）」かを考え、一般動詞の文か be 動詞の文かを先に決める。",
                steps=["述語が一般動詞か、形容詞・場所を表す語句かを判断する。", "一般動詞なら過去形（否定・疑問は did＋原形）、be 動詞なら was / were を使う。", "主語に合わせて形を整える。", f"答え：{ans}"],
                alt=["同じ内容を現在の文にしてみて、do / does を使う文か am / are / is を使う文かを確かめ、それを過去の形にかえる。"],
                pc=[("英文", 4), ("理由の説明", 3), ("形の正確さ", 1)],
                pit=["形容詞の文に did を使う（I didn't busy）。", "一般動詞の文に was / were を使う（I was go）。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(task, wrong, step, etype, tempt, fix, expl, steps, ap, alt, pit):
    return desc(f"{task}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい英文に書き直しなさい。", fix, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい英文に直している", 3), ("文法のルールを説明している", 1)], d=3, p=6, lines=4,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい英文", 3), ("ルールの説明", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix))


FORM_ERR = [
    ("私は昨日、京都へ行きました。", "I goed to Kyoto yesterday.", "I went to Kyoto yesterday.", "goed", "notation",
     "go は不規則動詞で、過去形は went。", "規則動詞と同じように -ed をつけた。"),
    ("彼は昨夜、2時間勉強しました。", "He studyed for two hours last night.", "He studied for two hours last night.", "studyed", "notation",
     "「子音字＋y」で終わる study は y を i にかえて ed をつける：studied。", "そのまま ed をつければよいと考えた。"),
    ("雨が急にやみました。", "The rain suddenly stoped.", "The rain suddenly stopped.", "stoped", "notation",
     "stop は「短母音＋子音字」で終わるので、p を重ねて stopped とする。", "e で終わる語と同じように d だけをつけた。"),
    ("私は新しいかばんを買いました。", "I buyed a new bag.", "I bought a new bag.", "buyed", "notation",
     "buy は不規則動詞で、過去形は bought。", "play → played と同じように考えた。"),
    ("私たちは祖父母の家を訪れました。", "We visitted our grandparents' house.", "We visited our grandparents' house.", "visitted", "notation",
     "visit は最後の音節に強勢がないので、t を重ねずに visited とする。", "stop → stopped のように子音字を重ねると考えた。"),
    ("彼女は朝食にパンを食べました。", "She eated bread for breakfast.", "She ate bread for breakfast.", "eated", "notation",
     "eat は不規則動詞で、過去形は ate。", "規則動詞と同じように -ed をつけた。"),
    ("ケンは昨日、サッカーをしました。", "Ken playsed soccer yesterday.", "Ken played soccer yesterday.", "playsed", "notation",
     "過去形には三単現の s はつかない。原形 play に ed をつけて played。", "主語が三人称単数なので s も必要だと考えた。"),
    ("私はその知らせを聞いて悲しくなりました。", "I feeled sad when I heard the news.", "I felt sad when I heard the news.", "feeled", "notation",
     "feel は不規則動詞で、過去形は felt。", "規則動詞と同じように -ed をつけた。"),
    ("私たちはその試合に勝ちました。", "We winned the game.", "We won the game.", "winned", "notation",
     "win は不規則動詞で、過去形は won。", "子音字を重ねて -ed をつける規則動詞だと考えた。"),
    ("父が私にこの時計をくれました。", "My father gived me this watch.", "My father gave me this watch.", "gived", "notation",
     "give は不規則動詞で、過去形は gave。", "e で終わる語なので d だけをつけた。"),
]


@gen("error_correction", 4, ["common_error", "computation"])
def err_form(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(FORM_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"動詞「{where}」", etype, tempt, fix, f"{rule}正しくは {fix}",
                    ["動詞が規則動詞か不規則動詞かを確認する。", f"「{where}」のつづりの誤りを見つける：{rule}", f"正しい英文：{fix}"],
                    "過去形を書くときは、①不規則動詞かどうか、②規則動詞なら語尾の形に合った -ed のつけ方か、の順に確かめる。",
                    ["不規則動詞の一覧表（原形 → 過去形）と照らし合わせて確かめる。"],
                    ["不規則動詞に -ed をつける。", "y → ied や子音字を重ねるルールを誤る。"])


DID_ERR = [
    ("あなたは昨日、公園へ行きましたか。", "Did you went to the park yesterday?", "Did you go to the park yesterday?", "went", "concept",
     "did を使ったら動詞は原形にもどす。過去の印は did の1つだけ。", "過去のことなので動詞も過去形にしなければならないと考えた。"),
    ("彼はその本を読みませんでした。", "He didn't read the book.", None, None, None, None, None),
    ("私は昨日、忙しくありませんでした。", "I didn't busy yesterday.", "I wasn't busy yesterday.", "didn't", "concept",
     "busy は形容詞なので be 動詞の文。否定は was not（wasn't）。", "過去の否定文はいつも didn't を使うと考えた。"),
    ("彼女はその知らせを知りませんでした。", "She didn't knew the news.", "She didn't know the news.", "knew", "concept",
     "didn't の後ろの動詞は原形にもどす。", "過去のことなので knew を使うと考えた。"),
    ("あなたは昨夜、テレビを見ましたか。", "Were you watch TV last night?", "Did you watch TV last night?", "Were", "concept",
     "watch は一般動詞なので、過去の疑問文は Did＋主語＋原形。", "be 動詞の過去 were と did の使い分けがあいまいだった。"),
    ("その映画はおもしろかったですか。", "Did the movie interesting?", "Was the movie interesting?", "Did", "concept",
     "interesting は形容詞なので be 動詞の文。主語 the movie に合う Was を前に出す。", "過去の疑問文はいつも Did で始めると考えた。"),
    ("ケンは今朝、朝食を食べませんでした。", "Ken doesn't eat breakfast this morning.", "Ken didn't eat breakfast this morning.", "doesn't", "concept",
     "this morning（今朝）の出来事は過去なので、doesn't ではなく didn't を使う。", "this（この）という語から現在の文だと考えた。"),
    ("あなたはどこでその写真をとったのですか。", "Where did you took the picture?", "Where did you take the picture?", "took", "concept",
     "疑問詞の疑問文でも did の後ろは原形。took を take にする。", "疑問詞があるとルールが変わると考えた。"),
    ("私たちは昨日、家にいませんでした。", "We didn't at home yesterday.", "We weren't at home yesterday.", "didn't", "concept",
     "「家にいた」は be 動詞で表すので、否定は were not（weren't）。", "過去の否定文はいつも didn't を使うと考えた。"),
]
DID_ERR = [x for x in DID_ERR if x[2]]


@gen("error_correction", 3, ["common_error", "condition_check"])
def err_did(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(DID_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", etype, tempt, fix, f"{rule}正しくは {fix}",
                    ["文の中心が一般動詞か、be 動詞（形容詞・場所が続く）かを確認する。", "did を使う文なら動詞を原形にし、be 動詞の文なら was / were を使う。", f"正しい英文：{fix}"],
                    "過去の否定文・疑問文は、①一般動詞の文か be 動詞の文か、②過去の印が1つだけか、の2点で確かめる。",
                    ["同じ内容を現在の文にしてみて（do / does の文か am / are / is の文か）、それを過去にかえて比べる。"],
                    ["did と過去形を両方使う。", "形容詞や場所の文に did を使う。"])


PROG_ERR = [
    ("私は昨夜9時にテレビを見ていました。", "I was watch TV at nine last night.", "I was watching TV at nine last night.", "watch", "concept",
     "過去進行形は was / were＋ing 形。watch を watching にする。", "was を置いたことで「過去進行形にした」と考え、ing をつけ忘れた。"),
    ("彼らはそのとき、サッカーをしていました。", "They was playing soccer then.", "They were playing soccer then.", "was", "condition",
     "主語 They は複数なので be 動詞の過去形は were。", "過去形の be 動詞はいつも was だと考えた。"),
    ("母が帰ってきたとき、私は本を読んでいました。", "When my mother came home, I am reading a book.", "When my mother came home, I was reading a book.", "am", "concept",
     "「母が帰ってきたとき」という過去の時点の話なので、be 動詞も過去形 was にする。", "「～している」から現在進行形を使った。"),
    ("あなたはそのとき、何をしていたのですか。", "What did you doing then?", "What were you doing then?", "did", "concept",
     "過去進行形の疑問文は be 動詞 were を主語の前に出す。did は使わない。", "過去の疑問文はいつも did を使うと考えた。"),
    ("私はその男性の名前を知っていました。", "I was knowing the man's name.", "I knew the man's name.", "was knowing", "concept",
     "know は状態を表す動詞なので進行形にしない。過去形 knew を使う。", "日本語の「知っていた」の「～していた」につられた。"),
    ("ユミはそのとき泳いでいませんでした。", "Yumi didn't swimming then.", "Yumi wasn't swimming then.", "didn't", "concept",
     "過去進行形の否定文は was not（wasn't）＋ing 形。", "過去の否定文には didn't を使うと考えた。"),
    ("私の兄は午後3時に走っていました。", "My brother was runing at three in the afternoon.", "My brother was running at three in the afternoon.", "runing", "notation",
     "run は「短母音＋子音字」で終わるので n を重ねて running とする。", "そのまま ing をつければよいと考えた。"),
    ("あなたは8時に宿題をしていましたか。", "Were you did your homework at eight?", "Were you doing your homework at eight?", "did", "concept",
     "過去進行形の疑問文は Were＋主語＋ing 形。did を doing にする。", "過去のことなので動詞も過去形にしなければならないと考えた。"),
]


@gen("error_correction", 3, ["common_error", "condition_check"])
def err_prog(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(PROG_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", etype, tempt, fix, f"{rule}正しくは {fix}",
                    ["「～していた」が進行中の動作か、状態か（know など）を確認する。", "進行中の動作なら was / were＋ing 形、主語に合う be 動詞かを確かめる。", f"正しい英文：{fix}"],
                    "過去進行形は「主語に合う was / were」と「正しくつづった ing 形」がそろって初めて成り立つ。否定・疑問も be 動詞の文のルール。",
                    ["直した文を現在進行形にもどしてみて（am / are / is＋ing）、be 動詞を過去にしただけの形になっているかを確かめる。"],
                    ["was / were の後ろに原形や過去形を置く。", "過去進行形の否定文・疑問文に did を使う。"])


GENERATORS = [past_form, ed_pron, be_past, did_question, past_prog,
              past_rewrite, wh_past, build_order, past_response, diary,
              explain_difference, four_forms, write_diary, choose_form,
              err_form, err_did, err_prog]
