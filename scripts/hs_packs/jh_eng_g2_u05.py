"""単元パック：中学2年 英語 受け身（受け身の形・過去分詞・by 以外の前置詞を伴う受け身）。"""
from banks._common import desc, mc, order, sa
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem,
                         tp)

UNIT_ID = "JH-ENG-G2-U05"

PREREQUISITES = [
    ("JH-ENG-G1-U01", "be 動詞（am / are / is）を主語に合わせて選び、be 動詞の文の否定文・疑問文を作れること。"),
    ("JH-ENG-G1-U05", "規則動詞・不規則動詞の過去形と be 動詞の過去形（was / were）。過去分詞は過去形と並べて覚える。"),
    ("JH-ENG-G1-U02", "目的格の代名詞（him / her / them など）と主格（he / she / they）の区別。能動態を受け身に書きかえるときに入れかえる。"),
]
EXTENSIONS = [
    ("JH-ENG-G3-U01", "現在完了形〈have / has＋過去分詞〉でも、この単元で覚えた過去分詞をそのまま使う。"),
    ("JH-ENG-G3-U02", "過去分詞が名詞の後ろに置かれ「～された…」と名詞を説明する形（a car made in Japan）に発展する。"),
    ("HS-ENG-U05", "高校では分詞と分詞構文として、過去分詞の「受け身の意味」を名詞の修飾や文の補足説明に広げて使う。"),
]

# 過去分詞の表：(原形, 過去形, 過去分詞, 種類)  種類 reg=規則 / same=不規則で過去形と同じ / diff=不規則で過去形と違う
PP = [
    ("use", "used", "used", "reg"), ("clean", "cleaned", "cleaned", "reg"), ("love", "loved", "loved", "reg"),
    ("visit", "visited", "visited", "reg"), ("invent", "invented", "invented", "reg"), ("paint", "painted", "painted", "reg"),
    ("carry", "carried", "carried", "reg"), ("study", "studied", "studied", "reg"), ("close", "closed", "closed", "reg"),
    ("stop", "stopped", "stopped", "reg"), ("plan", "planned", "planned", "reg"), ("call", "called", "called", "reg"),
    ("make", "made", "made", "same"), ("build", "built", "built", "same"), ("find", "found", "found", "same"),
    ("sell", "sold", "sold", "same"), ("teach", "taught", "taught", "same"), ("buy", "bought", "bought", "same"),
    ("catch", "caught", "caught", "same"), ("tell", "told", "told", "same"), ("send", "sent", "sent", "same"),
    ("hold", "held", "held", "same"), ("bring", "brought", "brought", "same"), ("read", "read", "read", "same"),
    ("write", "wrote", "written", "diff"), ("take", "took", "taken", "diff"), ("speak", "spoke", "spoken", "diff"),
    ("see", "saw", "seen", "diff"), ("give", "gave", "given", "diff"), ("eat", "ate", "eaten", "diff"),
    ("know", "knew", "known", "diff"), ("break", "broke", "broken", "diff"), ("steal", "stole", "stolen", "diff"),
    ("choose", "chose", "chosen", "diff"), ("draw", "drew", "drawn", "diff"), ("grow", "grew", "grown", "diff"),
    ("sing", "sang", "sung", "diff"), ("wear", "wore", "worn", "diff"), ("forget", "forgot", "forgotten", "diff"),
    ("throw", "threw", "thrown", "diff"), ("do", "did", "done", "diff"), ("ride", "rode", "ridden", "diff"),
]
PP_KIND = {"reg": "規則動詞なので ed をつける（過去形と同じ形）",
           "same": "不規則動詞だが、過去形と過去分詞が同じ形",
           "diff": "不規則動詞で、過去形と過去分詞の形が違う"}
PP_BY = {k: [x for x in PP if x[3] == k] for k in PP_KIND}

# 受け身の場面：(主語, 数 sg/pl, 原形, 過去分詞, 能動の形（主語に合わせた現在形・過去形）, 後ろの語句, 時制 pres/past, 日本語)
SCENE = [
    ("This room", "sg", "clean", "cleaned", "cleans", "every day", "pres", "この部屋は毎日掃除されます。"),
    ("These cars", "pl", "make", "made", "make", "in Japan", "pres", "これらの車は日本で作られています。"),
    ("English", "sg", "speak", "spoken", "speaks", "in many countries", "pres", "英語は多くの国で話されています。"),
    ("This temple", "sg", "build", "built", "built", "about 500 years ago", "past", "この寺はおよそ500年前に建てられました。"),
    ("These pictures", "pl", "take", "taken", "took", "by my father last year", "past", "これらの写真は昨年、父によってとられました。"),
    ("The letter", "sg", "write", "written", "wrote", "in English", "past", "その手紙は英語で書かれていました。"),
    ("The windows", "pl", "open", "opened", "open", "every morning", "pres", "その窓は毎朝開けられます。"),
    ("This song", "sg", "sing", "sung", "sings", "by many children", "pres", "この歌は多くの子どもたちに歌われています。"),
    ("These bags", "pl", "sell", "sold", "sell", "at that store", "pres", "これらのかばんはあの店で売られています。"),
    ("The window", "sg", "break", "broken", "broke", "yesterday", "past", "その窓は昨日割られました。"),
    ("The cakes", "pl", "eat", "eaten", "ate", "by the children", "past", "そのケーキは子どもたちに食べられました。"),
    ("The festival", "sg", "hold", "held", "held", "last weekend", "past", "そのお祭りは先週末に開かれました。"),
    ("These books", "pl", "read", "read", "read", "by many students", "pres", "これらの本はたくさんの生徒に読まれています。"),
    ("The dog", "sg", "find", "found", "found", "in the park", "past", "その犬は公園で見つけられました。"),
    ("Those boxes", "pl", "carry", "carried", "carried", "to the gym yesterday", "past", "あれらの箱は昨日体育館へ運ばれました。"),
    ("Japanese", "sg", "teach", "taught", "teaches", "at this school", "pres", "日本語はこの学校で教えられています。"),
    ("The doors", "pl", "close", "closed", "close", "at six every evening", "pres", "そのドアは毎晩6時に閉められます。"),
    ("This bike", "sg", "use", "used", "uses", "by my brother", "pres", "この自転車は兄に使われています。"),
]


def be_of(num, tense):
    return {("sg", "pres"): "is", ("pl", "pres"): "are", ("sg", "past"): "was", ("pl", "past"): "were"}[(num, tense)]


def ing_of(base):
    if base.endswith("e") and base not in ("see",):
        return base[:-1] + "ing"
    if base in ("stop", "plan"):
        return base + base[-1] + "ing"
    return base + "ing"


def cap(s):
    return s[0].upper() + s[1:]


def low(s):
    if s.split()[0] in ("This", "These", "The", "Those", "That", "Our", "My"):
        return s[0].lower() + s[1:]
    return s


# ======================================================================
# 授業プリント
# ======================================================================

LESSON = lesson(
    goals=["「～される（された）」を〈be 動詞＋過去分詞〉で表し、主語・時制に合わせて be 動詞を選べる。",
           "よく使う動詞の過去分詞（規則変化・不規則変化）を、原形・過去形と組にして正しく書ける。",
           "能動態の文を受け身の文に書きかえ、否定文・疑問文・疑問詞の疑問文も作れる。",
           "be covered with / be made of・from / be known to / be interested in など、by 以外の前置詞を使う表現を使い分けられる。"],
    duration=50,
    readiness=["be 動詞 am / are / is / was / were を主語と時制に合わせて選べる（中1）。",
               "一般動詞の過去形（規則動詞の ed、不規則動詞 made, wrote など）を書ける（中1）。",
               "目的格の代名詞 him / her / them / me を使える（中1）。",
               "国語で「～される」「～られる」という受け身の言い方を知っている（小学校）。"],
    flow=[("導入：だれが？何が？", 5, "写真（架空の寺）を見せ、「この寺は500年前に建てられた」を英語でどう言うか考えさせる"),
          ("受け身の形と過去分詞", 13, "be 動詞＋過去分詞、過去分詞の3つのタイプ、能動態から受け身への書きかえ（例題1）"),
          ("否定文・疑問文・疑問詞", 10, "be 動詞の文のルールで作る。When was ～ built? など（例題2）"),
          ("by 以外の前置詞", 12, "be covered with / made of・from / known to / interested in / surprised at（例題3）"),
          ("まとめと確認", 10, "能動態と受け身の使い分けを話し合い、確認問題3問")],
    sections=[
        intro("in1", "「する側」から言うか、「される側」から言うか",
              "同じできごとでも、「ケンがこの窓を割った」と動作をした人から言うこともできれば、「この窓はケンに割られた」と動作を受けたものから言うこともできます。英語では、動作をする側を主語にした文を能動態、動作を受ける側を主語にした文を受け身（受動態）といいます。受け身は、話題にしたいのが「される側」のときや、だれがしたのかがわからない・言う必要がないときによく使われます。",
              bullets=["Ken broke this window.（ケンがこの窓を割った）― 能動態", "This window was broken by Ken.（この窓はケンによって割られた）― 受け身",
                       "English is spoken in many countries.（英語は多くの国で話されている）― だれが話すかは言わなくてもわかる"],
              points=[tp("2つの文の主語に下線を引かせ、「話題の中心」がだれ（何）かを比べさせる。",
                         ask="1つ目と2つ目の文で、文の主語は何か。", expect="1つ目は Ken、2つ目は this window。", timing="導入の冒頭")]),
        definition("df1", "受け身の形：be 動詞＋過去分詞",
                   "「～される」「～された」は、〈be 動詞＋過去分詞〉で表します。be 動詞は、主語の数（単数・複数）と時制（現在・過去）で選びます。動作をした人（行為者）を示すときは by ～ を後ろに置きます。",
                   formula="主語＋am / are / is / was / were＋過去分詞（＋by ～）.",
                   bullets=["現在：This room is cleaned every day.（この部屋は毎日掃除される）",
                            "過去：These pictures were taken by my father.（これらの写真は父によってとられた）",
                            "否定文：be 動詞の後ろに not（This room isn't cleaned on Sundays.）",
                            "疑問文：be 動詞を主語の前に出す（Was this temple built 500 years ago? ― Yes, it was.）",
                            "助動詞といっしょに：can / will の後ろは be＋過去分詞（Mt. Fuji can be seen from here. / The concert will be held next Sunday.）"],
                   conditions=["受け身の主語になるのは、能動態の文で目的語（～を）になっていたもの。",
                               "by ～ は、だれがしたかわからないとき・一般の人々（people / they）のとき・言わなくてもわかるときは省くのがふつう。",
                               "否定文・疑問文で do / does / did は使わない（be 動詞の文だから）。"],
                   points=[tp("「受け身＝be 動詞と過去分詞の2つでセット」と板書で囲み、どちらかを落とす誤りを予告しておく。",
                              caution="This room cleaned every day.（be 動詞が抜ける）や This room is clean every day.（過去分詞にしていない）が多い。"),
                           tp("by ～ を毎回つけようとする生徒に、English is spoken in Australia by people. が不自然である理由を考えさせる。",
                              ask="by people をつけると何がおかしいか。", expect="話すのは人に決まっているので、わざわざ言う必要がない。")]),
        definition("df2", "過去分詞の3つのタイプ",
                   "受け身で使う過去分詞は、動詞の「原形－過去形－過去分詞」の3つを組にして覚えます。規則動詞は過去形と同じ ed の形、不規則動詞は1語ずつ覚える必要があります。",
                   bullets=["① 規則動詞：過去形と同じ（use - used - used / study - studied - studied / stop - stopped - stopped）",
                            "② 不規則動詞で過去形と同じ形：make - made - made / build - built - built / teach - taught - taught / read - read - read",
                            "③ 不規則動詞で過去形と違う形：write - wrote - written / speak - spoke - spoken / take - took - taken / see - saw - seen / sing - sang - sung"],
                   points=[tp("③のタイプはリズムで音読させる（write, wrote, written）。過去分詞の語尾 -en / -n に注目させると覚えやすい。", timing="定義の説明後")]),
        theorem("th1", "by 以外の前置詞を使う受け身の表現",
                "be covered with ～ ／ be filled with ～ ／ be made of ～ ／ be made from ～ ／ be known to ～ ／ be interested in ～ ／ be surprised at ～",
                ["be covered with ～：～でおおわれている（The mountain is covered with snow.）",
                 "be filled with ～：～でいっぱいだ（The box was filled with toys.）",
                 "be made of ～：（材料が見てわかる）～でできている（This desk is made of wood.）",
                 "be made from ～：（原料の形が変わって見えない）～から作られる（Cheese is made from milk.）",
                 "be known to ～：～に知られている（The singer is known to young people.）",
                 "be interested in ～：～に興味がある／be surprised at ～：～に驚く"],
                body="これらは「だれがしたか」よりも「状態」や「気持ち」を表すので、行為者を示す by ではなく、意味に合った前置詞を使います。まとまった言い方として覚えましょう。",
                points=[tp("made of と made from は、実物（木の机とチーズ）を見せて「材料が見えるか」で区別させる。",
                           ask="紙は木から作られる。of と from のどちらか。", expect="from（紙を見ても木の形は残っていない）。")]),
        derivation("dv1", "能動態から受け身を作る手順（なぜその形になるのか）",
                   ["① 能動態の文 Many people visit this museum. で、目的語（動作を受けるもの）を見つける：this museum。",
                    "② それを新しい主語にする：This museum ～。",
                    "③ 「される」を表すため、動詞を〈be 動詞＋過去分詞〉にする。主語は単数、もとの動詞は現在形なので is visited。",
                    "④ もとの主語（動作をした人）は by の後ろに置く。代名詞なら目的格にする（they → them、she → her）：by many people。",
                    "⑤ 完成：This museum is visited by many people.",
                    "⑥ 否定文・疑問文は be 動詞の文のルールで作る：This museum isn't visited ～. ／ Is this museum visited ～?"],
                   body="もとの文の時制は be 動詞に、もとの動詞の意味は過去分詞に引きつがれます。visited（過去形）と visited（過去分詞）は同じ形でも、is の後ろにあれば受け身の過去分詞です。",
                   points=[tp("④で by she としてしまう誤りを予想させ、前置詞の後ろは目的格になるという1年生のルールにもどって確認する。",
                              ask="She wrote this letter. を受け身にすると by の後ろは？", expect="her（by her）。", timing="導出の説明時")]),
        example("ex1", "例題1　能動態を受け身に書きかえる",
                "次の英文を受け身の文に書きかえなさい。(1) My mother made these cookies.　(2) They speak French in this country.",
                ["(1) 目的語 these cookies を主語にする。複数で、もとの文が過去形なので be 動詞は were。",
                 "(1) made の過去分詞は made。行為者 My mother は by my mother にする：These cookies were made by my mother.",
                 "(2) 目的語 French を主語にする。言語名は単数あつかいで、現在形なので is。speak の過去分詞は spoken。",
                 "(2) They は「その国の人々」という一般の人なので、by them は省くのがふつう：French is spoken in this country."],
                "(1) These cookies were made by my mother.　(2) French is spoken in this country.",
                thinking="主語の数ともとの時制から be 動詞を決め、動詞を過去分詞にする。行為者が一般の人なら by ～ は省く。",
                points=[tp("(1) で was を選ぶ生徒には、新しい主語 these cookies が複数であることを確認させる。")],
                misconceptions=[("These cookies were make by my mother.", "be 動詞の後ろは過去分詞。made にする。"),
                                ("French is spoken in this country by them.", "誤りとは言えないが、一般の人を表す them は省くのが自然。")]),
        example("ex2", "例題2　受け身の疑問文と疑問詞",
                "次の英文を、(1) は疑問文にして No で答え、(2) は下線部をたずねる疑問文にしなさい。(1) This bridge was built by Mr. Ito.　(2) This bridge was built ten years ago.（下線部：ten years ago）",
                ["(1) be 動詞 was を主語の前に出す：Was this bridge built by Mr. Ito?",
                 "(1) 答えは主語を代名詞 it にして be 動詞で答える：No, it wasn't.",
                 "(2) 「いつ」をたずねるので When を文頭に置き、後ろは疑問文の語順：When was this bridge built?"],
                "(1) Was this bridge built by Mr. Ito? ― No, it wasn't.　(2) When was this bridge built?",
                thinking="受け身は be 動詞の文。疑問文は be 動詞を前に出し、答えにも be 動詞を使う。",
                points=[tp("Did this bridge built ～? と書く生徒に、文の中の be 動詞を探させて、be 動詞の文か一般動詞の文かを判断させる。",
                           ask="この文の中に be 動詞はあるか。", expect="was がある。だから was を前に出す。")],
                misconceptions=[("Did this bridge built by Mr. Ito?", "受け身は be 動詞の文なので Was を前に出す。"),
                                ("When did this bridge build?", "「建てられた」は受け身。When was this bridge built?")]),
        example("ex3", "例題3　by 以外の前置詞",
                "（　）に適切な前置詞を入れなさい。(1) The top of the mountain is covered (　) snow.　(2) This chair is made (　) wood.　(3) Butter is made (　) milk.　(4) This song is known (　) everyone in my town.",
                ["(1) 「～でおおわれている」は be covered with。", "(2) いすを見れば材料の木がわかるので made of。",
                 "(3) バターを見ても牛乳の形は残っていないので made from。", "(4) 「～に知られている」は be known to。"],
                "(1) with　(2) of　(3) from　(4) to",
                thinking="「状態」や「気持ち」を表す受け身は、by ではなく決まった前置詞と組にして覚える。",
                points=[tp("(4) を by にする生徒が多い。「知られている」は動作ではなく状態であることを確認する。")]),
        board("bd1", "板書案",
              [("① 受け身の形", ["be 動詞＋過去分詞", "This room is cleaned every day.", "These pictures were taken by Ken.", "否定：isn't / wasn't＋過去分詞", "疑問：Was ～ built? ― Yes, it was.", "can be seen / will be held"]),
               ("② 過去分詞", ["規則：use-used-used", "同じ：make-made-made", "build-built-built", "違う：write-wrote-written", "speak-spoke-spoken", "take-took-taken"]),
               ("③ by 以外", ["covered with（おおわれる）", "filled with（いっぱい）", "made of（材料）", "made from（原料）", "known to（知られる）", "interested in / surprised at"])],
              points=[tp("①の「be 動詞」と「過去分詞」を別の色で書き、どちらも欠かせないことを視覚的に示す。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("能動態と受け身は「同じできごとを別の側から言う」ことを、教室の物（黒板・窓）を使った実演で体験させる。", timing="導入"),
               tp("過去分詞の暗記は「原形－過去形－過去分詞」の3語セットで音読させる。過去形と過去分詞が違う語は特に重点的に。",
                  caution="過去形と過去分詞の取り違え（was wrote）が最も多い誤り。"),
               tp("疑問文・否定文で did / does を使う誤りには、「受け身は be 動詞の文」と短く言わせて定着させる。",
                  ask="This letter was written by Ken. を否定文にすると？", expect="This letter wasn't written by Ken."),
               tp("by ～ を省く場面（一般の人・わからない・言う必要がない）を具体例で確認し、機械的な書きかえに偏らないようにする。"),
               tp("問題プリント D の誤答例は「be 動詞の欠落」「過去分詞の形」「do / did の混用」「前置詞」の4種類にまとめて振り返らせる。")],
              misconceptions=[("This letter was wrote by Ken.", "be 動詞の後ろは過去分詞。written にする。"),
                              ("This room cleaned every day.", "be 動詞が必要。This room is cleaned every day."),
                              ("Did this picture painted by her?", "受け身の疑問文は be 動詞を前に出す。Was this picture painted by her?"),
                              ("This letter was written by she.", "by の後ろは目的格。by her。")]),
        summary("sm1", "まとめ",
                ["受け身 ＝ be 動詞＋過去分詞。「～される（された）」。be 動詞は主語の数と時制で選ぶ。",
                 "行為者は by ～。一般の人・わからない・言わなくてもわかるときは省く。",
                 "否定・疑問は be 動詞の文のルール（do / does / did は使わない）。助動詞の後ろは be＋過去分詞。",
                 "by 以外：covered with / filled with / made of（材料）/ made from（原料）/ known to / interested in / surprised at。"]),
        check("ck1", "確認問題",
              [("write, take, build の過去分詞を書きなさい。", "written, taken, built"),
               ("This song (loves / is loved) by many people. の（　）から正しいほうを選びなさい。", "is loved（歌は「愛される」側）"),
               ("「その箱はりんごでいっぱいでした」を英語にしなさい（box, apples を使う）。", "The box was filled with apples.")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

@gen("basic_check", 4, ["computation", "common_error"])
def pp_form(r):
    ks = ["reg", "same", "diff"]
    r.shuffle(ks)
    vs = [r.choice(PP_BY[k]) for k in ks]
    ans = "　".join(f"({i + 1}) {v[1]} - {v[2]}" for i, v in enumerate(vs))
    return sa("次の3つの動詞の過去形と過去分詞を、「過去形 - 過去分詞」の順に書きなさい。\n" + "　".join(f"({i + 1}) {v[0]}" for i, v in enumerate(vs)),
              ans, "　".join(f"({i + 1}) {v[0]} は{PP_KIND[v[3]]}：{v[1]} - {v[2]}。" for i, v in enumerate(vs)), d=1, p=3,
              ap="まず規則動詞（ed をつける）か不規則動詞かを見分ける。不規則動詞は「原形－過去形－過去分詞」を声に出して確かめる。",
              steps=[f"({i + 1}) {v[0]} → {PP_KIND[v[3]]} → {v[1]} - {v[2]}" for i, v in enumerate(vs)],
              alt=["過去分詞を受け身の文に入れてみる（This was ___ by ～.）と、形が正しいかを確かめやすい。"],
              pc=[("(1) を正しく書いている", 1), ("(2) を正しく書いている", 1), ("(3) を正しく書いている", 1)],
              pit=["不規則動詞の過去分詞に過去形を書く（wrote / took など）。", "規則動詞のつづり（studied, stopped）を誤る。"])


@gen("basic_check", 4, ["computation", "condition_check"])
def passive_be(r):
    s, num, base, pp, act, tail, tense, jp = r.choice(SCENE)
    be = be_of(num, tense)
    kind = r.choice(["tense", "num"])
    if kind == "tense":
        bad_be = be_of(num, "past" if tense == "pres" else "pres")
        bad_reason = (f"「{jp}」は{'現在' if tense == 'pres' else '過去'}のことなので、be 動詞は {be}。{bad_be} では時制が合わない。", "時制と be 動詞の対応")
    else:
        bad_be = be_of("pl" if num == "sg" else "sg", tense)
        bad_reason = (f"主語 {s} は{'単数' if num == 'sg' else '複数'}なので、be 動詞は {be}。{bad_be} は主語の数に合わない。", "主語の数と be 動詞の対応")
    ok = f"{be} {pp}"
    why = {f"{bad_be} {pp}": bad_reason,
           f"{be} {ing_of(base)}": (f"{be} {ing_of(base)} は進行形で「（主語が）～している」の意味になり、「～される」にならない。", "進行形と受け身の混同"),
           act: (f"{act} だけだと「{s} が～する（した）」という能動の意味になる。{s} は動作を受ける側なので受け身にする。", "能動態と受け身の区別")}
    return mc(f"日本語に合うように、（　）に入る最も適切なものを選びなさい。\n{jp}\n{s} (　　) {tail}.", [ok] + list(why),
              f"「～される（された）」は be 動詞＋過去分詞。主語 {s}（{'単数' if num == 'sg' else '複数'}）と時制（{'現在' if tense == 'pres' else '過去'}）から be 動詞は {be}、{base} の過去分詞は {pp}。答え：{ok}", d=1,
              ap="①主語は動作を「する側」か「受ける側」か、②主語の数と時制、の順に確かめて be 動詞と動詞の形を決める。",
              steps=[f"主語 {s} は動作を受ける側 → 受け身（be 動詞＋過去分詞）。", f"主語の数と時制から be 動詞は {be}。", f"{base} の過去分詞は {pp}。答え：{ok}"],
              alt=[f"選んだ文を能動態にもどしてみる（～ {act} {low(s)}.）と、{s} が目的語になることから受け身が正しいと確かめられる。"],
              pc=[("受け身の形を選んでいる", 1), ("主語・時制に合う be 動詞を選んでいる", 1)],
              pit=["日本語の「～される」を見落とし、能動の形を選ぶ。", "主語の数や時制を確かめずに is を選ぶ。"], why=why)


PREP_USE = {"with": "with は「～で（道具・中身）」を表し、covered / filled / pleased と組になる",
            "of": "of は made of（材料が見てわかる）で使う",
            "from": "from は made from（原料の形が変わる）で使う",
            "to": "to は known to（～に知られている）で使う",
            "in": "in は interested in（～に興味がある）で使う",
            "at": "at は surprised at（～に驚く）で使う",
            "by": "by は動作をした人（行為者）を示す前置詞で、この決まった言い方には使わない"}

WRONG_POOL = {"with": ["of", "to", "at"], "to": ["with", "in", "at"], "in": ["with", "to", "at", "of"], "at": ["to", "in", "of"]}

PREP = [
    ("山は雪でおおわれています。", "The mountain is covered (　　) snow.", "with", "be covered with ～（～でおおわれている）"),
    ("そのびんは水でいっぱいです。", "The bottle is filled (　　) water.", "with", "be filled with ～（～でいっぱいだ）"),
    ("この机は木でできています。", "This desk is made (　　) wood.", "of", "be made of ～（材料が見てわかる）"),
    ("チーズは牛乳から作られます。", "Cheese is made (　　) milk.", "from", "be made from ～（原料の形が変わる）"),
    ("その歌手は若い人たちに知られています。", "The singer is known (　　) young people.", "to", "be known to ～（～に知られている）"),
    ("私は日本の歴史に興味があります。", "I am interested (　　) Japanese history.", "in", "be interested in ～（～に興味がある）"),
    ("私たちはその知らせに驚きました。", "We were surprised (　　) the news.", "at", "be surprised at ～（～に驚く）"),
    ("この家は石でできています。", "This house is made (　　) stone.", "of", "be made of ～（材料が見てわかる）"),
    ("豆腐は大豆から作られます。", "Tofu is made (　　) soybeans.", "from", "be made from ～（原料の形が変わる）"),
    ("その箱はおもちゃでいっぱいでした。", "The box was filled (　　) toys.", "with", "be filled with ～（～でいっぱいだ）"),
    ("その通りは落ち葉でおおわれていました。", "The street was covered (　　) fallen leaves.", "with", "be covered with ～（～でおおわれている）"),
    ("私の姉は音楽に興味があります。", "My sister is interested (　　) music.", "in", "be interested in ～（～に興味がある）"),
    ("生徒たちは彼の話に驚きました。", "The students were surprised (　　) his story.", "at", "be surprised at ～（～に驚く）"),
    ("その物語は世界中の子どもたちに知られています。", "The story is known (　　) children all over the world.", "to", "be known to ～（～に知られている）"),
    ("紙は木から作られます。", "Paper is made (　　) wood.", "from", "be made from ～（原料の形が変わる）"),
]


@gen("basic_check", 4, ["concept", "condition_check"])
def prep_choice(r):
    jp, s, ok, phrase = r.choice(PREP)
    # 英語として成り立ちうる組み合わせ（covered by / covered in / made from wood など）は誤りの選択肢にしない
    pool = ["with", "to", "in", "at", "by"] if " made " in s else WRONG_POOL[ok]
    wrongs = r.sample(pool, 3)
    return mc(f"日本語に合うように、（　）に入る最も適切な前置詞を選びなさい。\n{jp}\n{s}", [ok] + wrongs,
              f"{phrase} というまとまった言い方なので {ok}。", d=1,
              ap="過去分詞（covered / filled / made / known / interested / surprised など）とセットになる前置詞を思い出す。made は「材料が見えるか」で of と from を区別する。",
              steps=[f"過去分詞と日本語の意味から、使う表現を決める：{phrase}。", f"答え：{ok}"],
              alt=["made of / made from の場合は、できあがった物を見て材料の形がわかるかを考えて確かめる。"],
              pc=[("表現を正しく判断している", 1), ("正しい前置詞を選んでいる", 1)],
              pit=["どの受け身にも by を使う。", "made of と made from を取り違える。"],
              why={w: (f"{PREP_USE[w]}。ここは {phrase}。", "by 以外の前置詞を伴う受け身") for w in wrongs})


MEANING = [
    ("This picture was painted by my grandfather.", "この絵は祖父によって描かれた。",
     [("この絵は祖父を描いた。", "主語 this picture が「描いた」ことになり、能動の意味になっている。"),
      ("この絵は祖父によって描かれている。", "was は過去なので「描かれた」。今のことのように訳している。"),
      ("この絵は祖父のために描かれた。", "by は「～によって」で、動作をした人を表す。「～のために」は for。")]),
    ("Many people are invited to the party.", "たくさんの人がそのパーティーに招待されている。",
     [("たくさんの人がそのパーティーに招待した。", "are invited は受け身なので「招待される」。能動の意味になっている。"),
      ("たくさんの人がそのパーティーに招待された。", "are は現在なので「招待されている」。過去の意味にはならない。"),
      ("たくさんの人がそのパーティーに行きたがっている。", "invite は「招待する」。意味を取り違えている。")]),
    ("The window wasn't broken by Tom.", "その窓はトムによって割られたのではなかった。",
     [("その窓はトムを割らなかった。", "主語 the window が動作をしたことになり、能動の意味になっている。"),
      ("トムはその窓を割った。", "wasn't は否定。「割られなかった」の意味で、肯定にはならない。"),
      ("その窓はトムによって割られていない（今も）。", "wasn't は過去の否定。今の状態を言う文ではない。")]),
    ("Is this computer used by your sister?", "このコンピューターはあなたのお姉さんに使われていますか。",
     [("このコンピューターはあなたのお姉さんを使いますか。", "主語 this computer が「使う」ことになり、能動の意味になっている。"),
      ("このコンピューターはあなたのお姉さんに使われましたか。", "Is は現在なので「使われていますか」。過去ではない。"),
      ("あなたのお姉さんはこのコンピューターを使っていません。", "Is で始まる疑問文なので、否定の平叙文にはならない。")]),
    ("These rooms are cleaned every Friday.", "これらの部屋は毎週金曜日に掃除される。",
     [("これらの部屋は毎週金曜日に掃除する。", "主語 these rooms が掃除をすることになり、能動の意味になっている。"),
      ("これらの部屋は毎週金曜日に掃除された。", "are は現在。every Friday と合わせて「（ふだん）掃除される」。"),
      ("これらの部屋は毎週金曜日はきれいだ。", "cleaned は動詞 clean の過去分詞で「掃除される」。形容詞 clean（きれいな）とは違う。")]),
    ("The letter was written in English.", "その手紙は英語で書かれていた。",
     [("その手紙は英語を書いた。", "主語 the letter が書いたことになり、能動の意味になっている。"),
      ("その手紙は英語で書かれている途中だった。", "was written は受け身の過去で、「書いている途中」という進行の意味はない。"),
      ("その手紙を英語で書きなさい。", "命令文ではない。主語 the letter と be 動詞 was がある受け身の文。")]),
    ("This song is sung by many children.", "この歌は多くの子どもたちに歌われている。",
     [("この歌は多くの子どもたちを歌っている。", "主語 this song が歌うことになり、能動の意味になっている。"),
      ("この歌は多くの子どもたちに歌われた。", "is は現在。「歌われている」が正しい。"),
      ("多くの子どもたちがこの歌を歌いたがっている。", "「～したがっている」の意味は文のどこにもない。")]),
    ("Were these cookies made by Emi?", "これらのクッキーはエミによって作られたのですか。",
     [("これらのクッキーはエミを作ったのですか。", "主語 these cookies が作ったことになり、能動の意味になっている。"),
      ("これらのクッキーはエミによって作られていますか。", "Were は過去なので「作られたのですか」。"),
      ("エミはこれらのクッキーを作りましたか。それとも買いましたか。", "「それとも買いましたか」にあたる語は英文にない。")]),
    ("Japanese is taught at that school.", "日本語はあの学校で教えられている。",
     [("日本語はあの学校で教えている。", "主語 Japanese が教えることになり、能動の意味になっている。"),
      ("日本語はあの学校で教えられた。", "is は現在なので「教えられている」。"),
      ("あの学校では日本語を学ばなければならない。", "「～しなければならない」の意味を表す語（must など）は英文にない。")]),
    ("The old castle is visited by a lot of tourists.", "その古い城には多くの観光客が訪れる（多くの観光客に訪問されている）。",
     [("その古い城は多くの観光客を訪問する。", "主語 the old castle が訪問することになり、能動の意味になっている。"),
      ("その古い城は多くの観光客に訪問された。", "is は現在。ふだんの様子を表している。"),
      ("その古い城には多くの観光客が住んでいる。", "visit は「訪れる」で「住む」ではない。")]),
]


@gen("basic_check", 4, ["concept", "common_error"])
def passive_meaning(r):
    en, ok, wrongs = r.choice(MEANING)
    return mc(f"次の英文の意味として最も適切なものを選びなさい。\n{en}", [ok] + [w for w, _ in wrongs],
              f"be 動詞＋過去分詞は「～される（された）」。be 動詞の時制と否定・疑問の形にも注意する。答え：{ok}", d=1,
              ap="be 動詞と過去分詞の組を見つけて「～される」と訳す。次に be 動詞から時制（現在・過去）と、否定・疑問かどうかを確かめる。",
              steps=["be 動詞＋過去分詞の部分を見つける → 受け身。", "be 動詞の形で時制・否定・疑問を確かめる。", f"答え：{ok}"],
              alt=["英文を能動態に書きかえてから訳し、選んだ日本語と同じできごとを表しているかを確かめる。"],
              pc=[("受け身の意味を読み取っている", 1), ("時制・否定・疑問を正しく読み取っている", 1)],
              pit=["「～される」と訳さず、主語が動作をしたように訳す。", "be 動詞の時制を見落とす。"],
              why={w: (reason, "受け身の意味の読み取り") for w, reason in wrongs})


@gen("basic_check", 4, ["concept", "condition_check"])
def q_answer(r):
    s, num, base, pp, act, tail, tense, jp = r.choice(SCENE)
    be = be_of(num, tense)
    pr = "it" if num == "sg" else "they"
    yes = r.random() < 0.5 or s == "English"  # 事実に反する答えにならないように
    do = {"pres": "does" if num == "sg" else "do", "past": "did"}[tense]
    neg = {"is": "isn't", "are": "aren't", "was": "wasn't", "were": "weren't"}
    ok = f"Yes, {pr} {be}." if yes else f"No, {pr} {neg[be]}."
    other_pr = "they" if pr == "it" else "it"
    pr_be = be_of("pl" if num == "sg" else "sg", tense)
    other_be = be_of(num, "past" if tense == "pres" else "pres")
    why = {(f"Yes, {pr} {do}." if yes else f"No, {pr} {do}n't."): (f"受け身の疑問文は be 動詞の文なので、{do} ではなく {be} を使って答える。", "be 動詞と do / does / did の混同"),
           (f"Yes, {other_pr} {pr_be}." if yes else f"No, {other_pr} {neg[pr_be]}."): (f"主語 {s} は{'単数' if num == 'sg' else '複数'}なので、代名詞は {pr} で受ける。", "答えの代名詞"),
           (f"Yes, {pr} {other_be}." if yes else f"No, {pr} {neg[other_be]}."): (f"疑問文の be 動詞は {cap(be)} なので、答えも {be} を使う。時制を変えない。", "疑問文と答えの時制")}
    yn = "「はい」" if yes else "「いいえ」"
    q = f"{cap(be)} {low(s)} {pp} {tail}?"
    return mc(f"次の疑問文に{yn}と答えるとき、最も適切なものを選びなさい。\n{q}", [ok] + list(why),
              f"受け身の疑問文には、主語を代名詞（{pr}）にして be 動詞（{be}）で答える。答え：{ok}", d=2,
              ap="疑問文の最初の be 動詞（Is / Are / Was / Were）と主語の数を確かめ、それに合わせて答える。",
              steps=[f"疑問文は {cap(be)} で始まる受け身の文。", f"主語 {s} を代名詞にする → {pr}。", f"答え：{ok}"],
              alt=[f"省略を補って答えの文を完全にする（{cap(pr)} {be}{'' if yes else ' not'} {pp} {tail}.）と、形が正しいかを確かめられる。"],
              pc=[("be 動詞で答えている", 1), ("代名詞・時制・肯定否定が正しい", 1)],
              pit=["受け身の疑問文に did / does で答える。", "複数の主語を it で受ける。"], why=why)


# ======================================================================
# B 標準演習
# ======================================================================

# 能動態：(能動態の文, 受け身の主語, 数, 時制, 過去分詞, by の後ろ（None なら省くのがふつう）, 補足の語句, 日本語の説明)
ACT = [
    ("Ken washes the dishes after dinner.", "The dishes", "pl", "pres", "washed", "Ken", "after dinner"),
    ("Many people love this song.", "This song", "sg", "pres", "loved", "many people", ""),
    ("My mother made this cake.", "This cake", "sg", "past", "made", "my mother", ""),
    ("Natsume Soseki wrote Botchan.", "Botchan", "sg", "past", "written", "Natsume Soseki", ""),
    ("Tom broke the window yesterday.", "The window", "sg", "past", "broken", "Tom", "yesterday"),
    ("She uses this computer every day.", "This computer", "sg", "pres", "used", "her", "every day"),
    ("They speak French in this country.", "French", "sg", "pres", "spoken", None, "in this country"),
    ("Mr. Tanaka teaches math.", "Math", "sg", "pres", "taught", "Mr. Tanaka", ""),
    ("He took these photos in Kyoto.", "These photos", "pl", "past", "taken", "him", "in Kyoto"),
    ("The students clean the classrooms every day.", "The classrooms", "pl", "pres", "cleaned", "the students", "every day"),
    ("My father built this doghouse.", "This doghouse", "sg", "past", "built", "my father", ""),
    ("Lisa sent these letters last week.", "These letters", "pl", "past", "sent", "Lisa", "last week"),
    ("Leonardo da Vinci painted the Mona Lisa.", "The Mona Lisa", "sg", "past", "painted", "Leonardo da Vinci", ""),
    ("Many young people read this magazine.", "This magazine", "sg", "pres", "read", "many young people", ""),
    ("Our teacher chose these books.", "These books", "pl", "past", "chosen", "our teacher", ""),
    ("They sell fresh fish at that store.", "Fresh fish", "sg", "pres", "sold", None, "at that store"),
    ("Aya plays the piano at the school concert every year.", "The piano", "sg", "pres", "played", "Aya", "at the school concert every year"),
    ("The children found the cat under the car.", "The cat", "sg", "past", "found", "the children", "under the car"),
]


def act_passive(e, neg=False, q=False):
    sent, subj, num, tense, pp, by, tail = e
    be = be_of(num, tense)
    by_s = f" by {by}" if by else ""
    tail_s = f" {tail}" if tail else ""
    if q:
        return f"{cap(be)} {low(subj)} {pp}{by_s}{tail_s}?"
    if neg:
        return f"{subj} {be} not {pp}{by_s}{tail_s}."
    return f"{subj} {be} {pp}{by_s}{tail_s}."


@gen("standard_practice", 4, ["computation", "application"])
def active_to_passive(r):
    e = r.choice(ACT)
    sent, subj, num, tense, pp, by, tail = e
    be = be_of(num, tense)
    ans = act_passive(e)
    v_ = None
    note = ""
    if by is None:
        v_ = [ans[:-1] + " by them." if not tail else f"{subj} {be} {pp} {tail} by them."]
        note = "もとの主語 They は「その国・その店の人々」という一般の人なので、by them は省くのがふつう。"
    elif by in ("her", "him"):
        note = f"もとの主語は代名詞なので、by の後ろでは目的格 {by} にする。"
    obj = subj if subj in ("Botchan", "French") else subj[0].lower() + subj[1:]
    return sa(f"次の英文を、目的語の {obj} を主語にした受け身の文に書きかえなさい。\n{sent}",
              ans, f"目的語を主語にし、動詞を be 動詞＋過去分詞にする。{note}答え：{ans}", d=2, p=4, v=v_,
              ap="①目的語を主語にする、②主語の数ともとの時制で be 動詞を決める、③動詞を過去分詞にする、④もとの主語を by ～ にする、の順で書く。",
              steps=[f"新しい主語：{subj}（{'単数' if num == 'sg' else '複数'}）。", f"もとの文は{'現在' if tense == 'pres' else '過去'}形 → be 動詞は {be}。",
                     f"動詞を過去分詞 {pp} にする。", (f"もとの主語は by {by} とする。" if by else "一般の人を表す They は省く。"), f"答え：{ans}"],
              alt=["書きかえた文をもう一度能動態にもどし、もとの文と同じになるかを確かめる。"],
              pc=[("主語と be 動詞（数・時制）が正しい", 2), ("過去分詞と by ～ の部分が正しい", 2)],
              pit=["もとの時制を見落として、過去の文に is / are を使う。", "代名詞を by she / by he のように主格のまま置く。"])


@gen("standard_practice", 4, ["computation", "condition_check"])
def passive_neg_q(r):
    e = r.choice(ACT)
    sent, subj, num, tense, pp, by, tail = e
    be = be_of(num, tense)
    pas = act_passive(e)
    kind = r.choice(["neg", "q"])
    neg_be = {"is": "isn't", "are": "aren't", "was": "wasn't", "were": "weren't"}[be]
    pr = "it" if num == "sg" else "they"
    if kind == "neg":
        ans = act_passive(e, neg=True)
        v_ = [ans.replace(f" {be} not ", f" {neg_be} ", 1)]
        stem = f"次の受け身の文を否定文に書きかえなさい。\n{pas}"
        stp = ["受け身は be 動詞の文なので、be 動詞の後ろに not を置く。", "過去分詞はそのまま残す。", f"答え：{ans}"]
    else:
        ans = act_passive(e, q=True) + f" ― No, {pr} {neg_be}."
        v_ = None
        stem = f"次の受け身の文を疑問文に書きかえ、No で答える文も書きなさい。\n{pas}"
        stp = [f"be 動詞 {be} を主語の前に出す。", f"答えは主語を代名詞 {pr} にして be 動詞で答える。", f"答え：{ans}"]
    return sa(stem, ans, f"受け身の否定文・疑問文は be 動詞の文のルールで作る。did / does は使わない。答え：{ans}", d=2, p=4, v=v_,
              ap="文の中の be 動詞を見つける。否定はその後ろに not、疑問はそれを主語の前に出す。",
              steps=stp,
              alt=["書きかえた文を日本語に訳し、「～されない」「～されますか（されましたか）」の意味になっているかを確かめる。"],
              pc=[("be 動詞の位置（not・語順）が正しい", 2), ("過去分詞・答えの文が正しい", 2)],
              pit=["Did ～ / Does ～ で疑問文を作る。", "否定文で過去分詞を原形にもどしてしまう。"])


ORDERS = [
    ("この寺はおよそ600年前に建てられました。", ["this temple", "was", "built", "about", "600 years", "ago"]),
    ("英語はたくさんの国で話されています。", ["English", "is", "spoken", "in", "many", "countries"]),
    ("これらの写真は私の兄によってとられました。", ["these pictures", "were", "taken", "by", "my", "brother"]),
    ("その部屋は毎日掃除されていますか。", ["is", "the room", "cleaned", "every", "day"]),
    ("この本は子どもたちに読まれていません。", ["this book", "is", "not", "read", "by", "children"]),
    ("その山は雪でおおわれていました。", ["the mountain", "was", "covered", "with", "snow"]),
    ("その歌手は世界中の人々に知られています。", ["the singer", "is", "known", "to", "people", "all over the world"]),
    ("このいすは木でできています。", ["this chair", "is", "made", "of", "wood"]),
    ("この手紙はいつ書かれたのですか。", ["when", "was", "this letter", "written"]),
    ("あなたはその知らせに驚きましたか。", ["were", "you", "surprised", "at", "the news"]),
    ("その箱は古い本でいっぱいでした。", ["the box", "was", "filled", "with", "old", "books"]),
    ("その試合は来週の土曜日に行われます。", ["the game", "will", "be", "held", "next", "Saturday"]),
    ("ここから美しい星が見えます。", ["beautiful stars", "can", "be", "seen", "from", "here"]),
    ("これらの車はどこで作られていますか。", ["where", "are", "these cars", "made"]),
]


@gen("standard_practice", 4, ["application", "computation"])
def build_order(r):
    jp, parts = r.choice(ORDERS)
    sent = cap(" ".join(parts)) + ("?" if jp.endswith("か。") else ".")
    return order(f"日本語に合うように、次の語句を並べかえて英文を完成させなさい。ただし、文頭にくる語も小文字で示してある。\n{jp}", parts,
                 f"{sent}　ポイント：受け身は be 動詞＋過去分詞。疑問文は be 動詞（疑問詞があればその後ろ）を主語の前に置く。", d=2, p=4,
                 ap="日本語の「～される（された）」「～でできている」などから受け身だと判断し、主語 → be 動詞 → 過去分詞の骨組みを先に作る。",
                 steps=["主語（動作を受けるもの）を決める。", "be 動詞（助動詞があれば助動詞＋be）と過去分詞を並べる。", "by ～ や前置詞の句、時や場所の語句を後ろに置く。", f"完成文：{sent}"],
                 alt=["完成した英文を日本語に訳し直して、問題の日本語と一致するかを確かめる。"],
                 pc=[("主語・be 動詞・過去分詞の語順が正しい", 2), ("前置詞の句・修飾語句の位置が正しい", 2)],
                 pit=["疑問文で be 動詞を主語の後ろに置いたままにする。", "can / will の後ろの be を落とす。"])


AUX = [
    ("その山の頂上から富士山が見えます。", "Mt. Fuji can (　　) from the top of the mountain.", "be seen",
     [("see", "can の後ろに see を置くと「富士山が見る」ことになる。富士山は「見られる」側。"),
      ("is seen", "can の後ろは動詞の原形。is は原形ではないので be にする。"),
      ("seen", "can の後ろに過去分詞だけを置くことはできない。be＋過去分詞にする。"),
      ("be see", "be の後ろは過去分詞 seen。原形 see では受け身にならない。")]),
    ("そのコンサートは来週の日曜日に開かれます。", "The concert will (　　) next Sunday.", "be held",
     [("held", "will の後ろに過去分詞だけを置くことはできない。be が必要。"),
      ("is held", "will の後ろは動詞の原形。is ではなく be にする。"),
      ("be hold", "be の後ろは過去分詞 held。原形 hold では受け身にならない。"),
      ("hold", "will hold だと「コンサートが開く」ことになる。コンサートは「開かれる」側。")]),
    ("この部屋は生徒が使うことができます。", "This room can (　　) by students.", "be used",
     [("use", "can use だと「部屋が使う」ことになる。部屋は「使われる」側。"),
      ("is used", "can の後ろは動詞の原形。is ではなく be にする。"),
      ("used", "can の後ろに過去分詞だけを置くことはできない。be が必要。"),
      ("be using", "be using は進行形の形で、受け身にならない。")]),
    ("新しい図書館が来年建てられます。", "A new library will (　　) next year.", "be built",
     [("build", "will build だと「図書館が建てる」ことになる。図書館は「建てられる」側。"),
      ("built", "will の後ろに過去分詞だけを置くことはできない。be が必要。"),
      ("is built", "will の後ろは動詞の原形。is ではなく be にする。"),
      ("be build", "be の後ろは過去分詞 built。")]),
    ("その手紙は明日送られるでしょう。", "The letter will (　　) tomorrow.", "be sent",
     [("send", "will send だと「手紙が送る」ことになる。手紙は「送られる」側。"),
      ("sent", "will の後ろに過去分詞だけを置くことはできない。be が必要。"),
      ("is sent", "will の後ろは動詞の原形。is ではなく be にする。"),
      ("be send", "be の後ろは過去分詞 sent。")]),
    ("この本は図書館で借りることができます。", "This book can (　　) at the library.", "be borrowed",
     [("borrow", "can borrow だと「本が借りる」ことになる。本は「借りられる」側。"),
      ("borrowed", "can の後ろに過去分詞だけを置くことはできない。be が必要。"),
      ("is borrowed", "can の後ろは動詞の原形。is ではなく be にする。"),
      ("be borrowing", "be borrowing は進行形の形で、受け身にならない。")]),
    ("その宿題は明日までに終えなければなりません。", "The homework must (　　) by tomorrow.", "be finished",
     [("finish", "must finish だと「宿題が終える」ことになる。宿題は「終えられる」側。"),
      ("finished", "must の後ろに過去分詞だけを置くことはできない。be が必要。"),
      ("is finished", "must の後ろは動詞の原形。is ではなく be にする。"),
      ("be finishing", "be finishing は進行形の形で、受け身にならない。")]),
    ("その窓は今夜閉められるでしょう。", "The windows will (　　) tonight.", "be closed",
     [("close", "will close だと「窓が閉める」ことになる。窓は「閉められる」側。"),
      ("closed", "will の後ろに過去分詞だけを置くことはできない。be が必要。"),
      ("are closed", "will の後ろは動詞の原形。are ではなく be にする。"),
      ("be closing", "be closing は進行形の形で、受け身にならない。")]),
]


@gen("standard_practice", 4, ["cross_unit", "condition_check"], rel=["JH-ENG-G2-U01", "JH-ENG-G1-U04"])
def aux_passive(r):
    jp, s, ok, wrongs = r.choice(AUX)
    ws = r.sample(wrongs, 3)
    return mc(f"日本語に合うように、（　）に入る最も適切なものを選びなさい。\n{jp}\n{s}", [ok] + [w for w, _ in ws],
              f"助動詞（can / will / must）の後ろは動詞の原形なので、受け身は〈助動詞＋be＋過去分詞〉になる。答え：{ok}", d=2,
              ap="助動詞の後ろは原形、という中1・中2のルールと、受け身は be＋過去分詞、というこの単元のルールを組み合わせる。",
              steps=["主語は動作を受ける側 → 受け身にする。", "助動詞の後ろなので be 動詞は原形 be。", f"be の後ろに過去分詞を置く。答え：{ok}"],
              alt=["助動詞を取った文（The concert is held ～.）を作ってから、is を be にもどして助動詞を前に置くと確かめられる。"],
              pc=[("受け身の意味だと判断している", 2), ("助動詞＋be＋過去分詞の形を選んでいる", 2)],
              pit=["助動詞の後ろに is / are を置く。", "be を落として助動詞の後ろに過去分詞だけを置く。"],
              why={w: (reason, "助動詞と受け身の組み合わせ") for w, reason in ws})


WH = [
    ("Who", "was", "this picture", "painted", "paint", " by", "It was painted by my aunt.", "だれ"),
    ("When", "was", "this school", "built", "build", "", "It was built in 1985.", "いつ"),
    ("Where", "are", "these cars", "made", "make", "", "They are made in Germany.", "どこ"),
    ("Who", "was", "this letter", "written", "write", " by", "It was written by my grandmother.", "だれ"),
    ("When", "was", "the festival", "held", "hold", "", "It was held last Saturday.", "いつ"),
    ("Where", "was", "your bike", "found", "find", "", "It was found near the station.", "どこ"),
    ("Who", "were", "these cookies", "made", "make", " by", "They were made by Emi.", "だれ"),
    ("When", "were", "these photos", "taken", "take", "", "They were taken last summer.", "いつ"),
    ("Where", "is", "this cheese", "made", "make", "", "It is made in Hokkaido.", "どこ"),
    ("Who", "is", "this song", "sung", "sing", " by", "It is sung by a popular band.", "だれ"),
    ("When", "was", "this book", "written", "write", "", "It was written about 100 years ago.", "いつ"),
    ("Where", "were", "the old coins", "found", "find", "", "They were found under the house.", "どこ"),
]
QW_JP = {"Who": "だれ（によって）", "When": "いつ", "Where": "どこ"}


@gen("standard_practice", 4, ["cross_unit", "application"], rel=["JH-ENG-G1-U03"])
def wh_passive(r):
    qw, be, subj, pp, base, by, answer, _ = r.choice(WH)
    ok = f"{qw} {be} {subj} {pp}{by}?"
    do = {"is": "does", "are": "do", "was": "did", "were": "did"}[be]
    other_qw = r.choice([x for x in QW_JP if x != qw])
    why = {f"{qw} {do} {subj} {base}{by}?": (f"{do} を使うと「{subj} が～する」という能動の疑問文になる。{subj} は動作を受ける側なので be 動詞＋過去分詞。", "能動態と受け身の区別"),
           f"{qw} {be} {subj} {base}{by}?": (f"be 動詞の後ろは過去分詞 {pp}。原形 {base} では受け身にならない。", "過去分詞の形"),
           f"{other_qw} {be} {subj} {pp}{' by' if other_qw == 'Who' else ''}?": (f"B は「{QW_JP[qw]}」を答えているので、疑問詞は {qw}。{other_qw} では答えと合わない。", "疑問詞と答えの対応")}
    return mc(f"次の対話が成り立つように、A の（　）に入る最も適切なものを選びなさい。\nA：(　　)\nB：{answer}", [ok] + list(why),
              f"B は受け身で「{QW_JP[qw]}」を答えているので、A は〈{qw}＋be 動詞＋主語＋過去分詞〉でたずねる。答え：{ok}", d=3,
              ap="B の答えの中で、新しい情報（人・時・場所）がどれかを見つけ、それをたずねる疑問詞を決める。その後ろは受け身の疑問文の語順。",
              steps=[f"B の答えの新しい情報 → 「{QW_JP[qw]}」→ 疑問詞 {qw}。", f"B の文は受け身（{be} {pp}）なので、A も受け身の疑問文。", f"答え：{ok}"],
              alt=["選んだ疑問文の疑問詞を B の答えの語句に置きかえ、平叙文にもどすと B の文になるかを確かめる。"],
              pc=[("疑問詞を正しく選んでいる", 2), ("受け身の疑問文の語順を選んでいる", 2)],
              pit=["一般動詞の疑問文と同じように did / does を使う。", "Who ～ by? の by を落とす（落としても通じるが、by があると「～によって」がはっきりする）。"], why=why)


# ======================================================================
# C 思考力・記述応用
# ======================================================================

PAIRS = [
    ("Ken broke the window.", "The window was broken by Ken.",
     "A は能動態で、動作をした「ケン」を主語にして「ケンが窓を割った」と述べている。B は受け身（was＋過去分詞 broken）で、動作を受けた「窓」を主語にして「窓はケンに割られた」と述べている。できごとは同じだが、A はケンの行動、B は窓に起きたことを話題の中心にしている。"),
    ("People speak English in Australia.", "English is spoken in Australia.",
     "どちらも「オーストラリアでは英語が話されている」という同じ内容を表す。A は能動態で一般の人々 People を主語にしている。B は受け身（is＋spoken）で English を主語にし、話すのが一般の人々であることは言わなくてもわかるので by people を省いている。話題が「英語」のときは B が自然。"),
    ("My sister is cleaning the room.", "The room is cleaned by my sister.",
     "A は is＋ing 形の現在進行形で「姉が（今）部屋を掃除している」という進行中の動作を表す。B は is＋過去分詞の受け身で「その部屋は（ふだん）姉によって掃除される」という意味。be 動詞の後ろが ing 形か過去分詞かで意味が変わる。"),
    ("This room is clean.", "This room is cleaned every day.",
     "A の clean は形容詞で「この部屋はきれいだ」という状態を表す。B の cleaned は動詞 clean の過去分詞で、is cleaned は受け身「この部屋は毎日掃除される」を表す。is の後ろが形容詞か過去分詞かで意味が違う。"),
    ("Who wrote this letter?", "Who was this letter written by?",
     "どちらも手紙を書いた人をたずねる。A は能動態で Who が主語になり「だれがこの手紙を書いたのか」。B は受け身（was＋written）で this letter が主語になり「この手紙はだれによって書かれたのか」。B は話題の中心を「手紙」にしたたずね方。"),
    ("This desk is made of wood.", "Paper is made from wood.",
     "どちらも wood（木）を使うが、A は机を見れば材料の木がわかるので made of（材料）。B は紙を見ても木の形は残っていないので made from（原料）。材料の形がそのまま見えるかどうかで of と from を使い分けている。"),
    ("I surprised my friend.", "I was surprised at the news.",
     "A は能動態で「私が友だちを驚かせた」と、私が驚かせる側。B は受け身（was＋surprised）で「私はその知らせに驚いた」と、私が驚かされる側。B のように気持ちを表す受け身では、決まった言い方として at を使うことが多い。"),
    ("The concert will be held next week.", "They will hold the concert next week.",
     "どちらも「来週コンサートが開かれる」という内容。A は受け身（will be＋held）でコンサートを主語にし、開く人は言っていない。B は能動態で They（主催する人たち）を主語にしている。コンサートのことを伝えたいときは A が自然。"),
]


@gen("thinking_writing", 3, ["written_reasoning", "concept"])
def explain_pair(r):
    a, b, model = r.choice(PAIRS)
    return desc(f"次の2つの英文 A・B の意味や働きの違いを、文の形（主語・be 動詞の後ろの語の形・前置詞など）に注目して日本語で説明しなさい。\nA：{a}\nB：{b}", model,
                "主語が動作をする側か受ける側か、be 動詞の後ろが過去分詞・ing 形・形容詞のどれかで、文の意味が決まる。",
                [("A の形と意味を正しく説明している", 3), ("B の形と意味を正しく説明している", 3), ("違いを生む形の部分を指摘している", 2)], d=3, p=8, lines=5,
                ap="2つの文の主語に下線を引き、動詞の部分（be 動詞＋過去分詞・ing 形・形容詞など）を比べる。",
                steps=["A と B の主語と動詞の部分を見比べる。", "それぞれ能動態・受け身・進行形・形容詞の文のどれかを判断する。", "和訳を示して、どの形が違いを生んでいるかを説明する。"],
                alt=["それぞれの文が自然に使われる場面（何を話題にしているか）を考えて、場面の違いから説明する方法もある。"],
                pc=[("A の説明", 3), ("B の説明", 3), ("形の違いの指摘", 2)],
                pit=["和訳だけを書き、形の違いに触れない。", "受け身を「主語が～した」と訳してしまう。"])


MADE = [
    ("この机は木でできています。", "This desk is made of wood.", "of", "机を見れば材料の木がわかる（材料の形や性質が残っている）ので made of を使う。"),
    ("チーズは牛乳から作られます。", "Cheese is made from milk.", "from", "チーズを見ても牛乳の形は残っていない（原料が変化している）ので made from を使う。"),
    ("豆腐は大豆から作られます。", "Tofu is made from soybeans.", "from", "豆腐を見ても大豆の形は残っていない（原料が変化している）ので made from を使う。"),
    ("この家は石でできています。", "This house is made of stone.", "of", "家を見れば材料の石がわかるので made of を使う。"),
    ("このいすはプラスチックでできています。", "This chair is made of plastic.", "of", "いすを見れば材料のプラスチックがわかるので made of を使う。"),
    ("紙は木から作られます。", "Paper is made from wood.", "from", "紙を見ても木の形は残っていない（原料が変化している）ので made from を使う。"),
    ("バターは牛乳から作られます。", "Butter is made from milk.", "from", "バターを見ても牛乳の形は残っていないので made from を使う。"),
    ("このコップはガラスでできています。", "This cup is made of glass.", "of", "コップを見れば材料のガラスがわかるので made of を使う。"),
    ("このジャムはいちごから作られています。", "This jam is made from strawberries.", "from", "ジャムでは、いちごはもとの形のままではない（原料が変化している）ので made from を使う。"),
    ("この人形は紙でできています。", "This doll is made of paper.", "of", "人形を見れば材料の紙がわかるので made of を使う。"),
]


@gen("thinking_writing", 2, ["condition_check", "written_reasoning"])
def made_of_from(r):
    jp, en, prep, why_s = r.choice(MADE)
    return desc(f"次の日本語を、made を使った英語に直しなさい。また、前置詞に of と from のどちらを使ったか、その理由を説明しなさい。\n{jp}", f"{en}　理由：{why_s}",
                "be made of ～ は材料がそのまま見てわかるとき、be made from ～ は原料の形や性質が変わって見えないときに使うのが基本。",
                [("正しい英文を書いている（be 動詞＋made＋前置詞）", 4), ("材料の形が見えるかどうかに触れて理由を説明している", 3), ("主語に合う be 動詞を使っている", 1)], d=4, p=8, lines=4,
                ap="できあがった物を思い浮かべ、材料の形や性質がそのまま残っているかを考える。",
                steps=["主語を決め、be 動詞＋made で「作られている」を表す。", "材料の形が見えるか → 見える：of／見えない：from。", f"答え：{en}"],
                alt=["物を分解したら材料にもどせるか（机 → 木の板）を考えると、of か from かを確かめやすい。"],
                pc=[("英文", 4), ("理由の説明", 3), ("be 動詞", 1)],
                pit=["どちらにも by を使う（made by は作った人を表す）。", "of と from を逆にする。"])


WRITE = [
    ("あなたの町の夏祭り", "The summer festival is held in our town every August. It is loved by many people.",
     "1文目で祭りがいつ・どこで開かれるかを is held で、2文目でどう思われているかを is loved で表している。"),
    ("学校の図書室", "Our school library is used by many students. A lot of new books are bought every year.",
     "is used で図書室の利用のされ方を、are bought で毎年本が買われていることを受け身で伝えている。"),
    ("あなたの家にある古い時計", "This clock was made about 80 years ago. It was given to my grandfather by his father.",
     "was made で作られた時期を、was given で祖父が受け取ったいきさつを、過去の受け身で表している。"),
    ("地元の名産品（りんご）", "These apples are grown in our town. They are sold all over Japan.",
     "are grown で育てられている場所、are sold で売られている範囲を受け身で伝えている。"),
    ("あなたの町にある古い寺", "This temple was built about 400 years ago. It is visited by many tourists every year.",
     "was built で建てられた時期を過去の受け身で、is visited で今のようすを現在の受け身で表している。"),
    ("お気に入りの歌", "My favorite song was written by a high school student. It is sung by many young people.",
     "was written で作者を by で示し、is sung で今の人気を受け身で伝えている。"),
    ("学校の文化祭", "Our school festival is held in October. Many posters are made by the students.",
     "is held で開かれる時期、are made で生徒が作るものを受け身で表している。"),
    ("家族で使っている車", "Our car was made in Japan. It is used by my father every day.",
     "was made で作られた場所、is used で使われ方を受け身で伝えている。"),
]


@gen("thinking_writing", 3, ["application", "written_reasoning"])
def write_intro(r):
    topic, model, point = r.choice(WRITE)
    return desc(f"次のものを、留学生に紹介する英文を2文で書きなさい。ただし、2文とも受け身（be 動詞＋過去分詞）を使うこと。\n紹介するもの：{topic}",
                f"（解答例）{model}", f"（解答例の解説）{point} 主語が「紹介するもの」になるので、受け身を使うと話題がぶれずに伝わる。",
                [("1文目が受け身の正しい文で、内容が場面に合っている", 3), ("2文目が受け身の正しい文で、1文目と内容がつながっている", 3), ("過去分詞のつづり・be 動詞の形・語順が正しい", 2)], d=4, p=8, lines=4,
                ap="紹介するものを主語にして、「いつ・どこで作られた／開かれる」「だれに使われる・愛される」など、される側から言える内容を考える。",
                steps=["紹介したい内容を日本語で2つ決める（いつ・どこで・だれに）。", "それぞれを〈主語＋be 動詞＋過去分詞〉で書く。", "時制（現在か過去か）と be 動詞が合っているかを見直す。"],
                alt=["書いた2文を能動態に書きかえてみて、受け身のほうが「紹介するもの」を中心に話せていることを確かめる。"],
                pc=[("1文目", 3), ("2文目", 3), ("表記の正確さ", 2)],
                pit=["be 動詞を落とす（It loved by ～）。", "過去分詞に過去形を書く（It was wrote ～）。"])


PVP = [
    ("write", "wrote", "written", "Ken (　　) this letter yesterday.", "This letter was (　　) by Ken."),
    ("take", "took", "taken", "My father (　　) these pictures last year.", "These pictures were (　　) by my father."),
    ("speak", "spoke", "spoken", "She (　　) to me in English.", "English is (　　) in many countries."),
    ("make", "made", "made", "Emi (　　) this cake for me.", "This cake was (　　) by Emi."),
    ("clean", "cleaned", "cleaned", "We (　　) our classroom after school.", "Our classroom is (　　) every day."),
    ("sing", "sang", "sung", "The children (　　) a song together.", "This song is (　　) at the festival every year."),
    ("break", "broke", "broken", "Tom (　　) the cup this morning.", "The cup was (　　) by Tom."),
    ("build", "built", "built", "They (　　) a new bridge last year.", "The bridge was (　　) ten years ago."),
    ("see", "saw", "seen", "I (　　) a rainbow yesterday.", "Many stars can be (　　) from here."),
    ("know", "knew", "known", "I (　　) the answer.", "This song is (　　) to everyone in Japan."),
]


@gen("thinking_writing", 2, ["cross_unit", "written_reasoning"], rel=["JH-ENG-G1-U05"])
def past_vs_pp(r):
    base, past, pp, s1, s2 = r.choice(PVP)
    same = past == pp
    model = (f"(1) {past}　(2) {pp}。理由：(1) は主語が動作をした人で、過去のできごとを述べる文なので過去形 {past}。"
             f"(2) は be 動詞があり、主語が動作を受ける側なので、受け身の〈be 動詞＋過去分詞〉にする。"
             + (f"{base} は過去形と過去分詞が同じ形 {pp} だが、(2) の {pp} は be 動詞の後ろにあるので過去分詞である。" if same else f"{base} は過去形 {past} と過去分詞 {pp} の形が違うので注意する。"))
    return desc(f"（　）内に動詞 {base} を適切な形に直して入れなさい。また、(1)(2) でその形になる理由を説明しなさい。\n(1) {s1}\n(2) {s2}", model,
                "中1で学んだ過去形と、この単元の過去分詞を区別する。be 動詞（や can be）の後ろにあるかどうかで判断する。",
                [("(1)(2) の形をどちらも正しく書いている", 3), ("(1) が過去形になる理由を説明している", 2), ("(2) が受け身の過去分詞になる理由を説明している", 3)], d=4, p=8, lines=5,
                ap="空所の前に be 動詞があるかを見る。ない → 文の動詞（過去形）、ある → 受け身の過去分詞。",
                steps=[f"(1) 主語が動作をした人・過去の文 → 過去形 {past}。", f"(2) be 動詞の後ろ・主語が動作を受ける → 過去分詞 {pp}。", "それぞれの理由をまとめる。"],
                alt=["(2) を能動態に書きかえてみると、もとの主語が動作をしたことがわかり、受け身であると確かめられる。"],
                pc=[("2つの形", 3), ("(1) の理由", 2), ("(2) の理由", 3)],
                pit=["(2) に過去形を入れる（was wrote）。", "過去形と過去分詞が同じ形の動詞で、どちらの働きかを説明できない。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(task, wrong, step, etype, tempt, fix, expl, steps, ap, alt, pit):
    return desc(f"{task}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい英文に書き直しなさい。", fix, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい英文に直している", 3), ("文法のルールを説明している", 1)], d=3, p=6, lines=4,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい英文", 3), ("ルールの説明", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix))


FORM_ERR = [
    ("この手紙はケンによって書かれました。", "This letter was wrote by Ken.", "This letter was written by Ken.", "wrote", "formula",
     "be 動詞の後ろは過去分詞。write の過去分詞は written。", "過去のことなので過去形 wrote を使えばよいと考えた。"),
    ("この部屋は毎日掃除されます。", "This room cleaned every day.", "This room is cleaned every day.", "cleaned の前", "concept",
     "受け身は be 動詞＋過去分詞。主語は単数で現在なので is が必要。", "日本語の「される」を cleaned だけで表せると考えた。"),
    ("英語は多くの国で話されています。", "English speaks in many countries.", "English is spoken in many countries.", "speaks", "concept",
     "英語は「話される」側なので受け身 is spoken にする。English speaks では英語が話すことになる。", "日本語の「話されて」の「話す」だけを訳した。"),
    ("これらの写真は昨年とられました。", "These pictures was taken last year.", "These pictures were taken last year.", "was", "condition",
     "主語 These pictures は複数なので be 動詞は were。", "past なので was と決めて、主語の数を確かめなかった。"),
    ("その寺は300年前に建てられました。", "The temple is built 300 years ago.", "The temple was built 300 years ago.", "is", "condition",
     "300 years ago は過去なので be 動詞は was。", "過去分詞 built が過去を表すと思い、be 動詞を現在のままにした。"),
    ("この自転車は兄に使われています。", "This bike is use by my brother.", "This bike is used by my brother.", "use", "formula",
     "be 動詞の後ろは過去分詞。use の過去分詞は used。", "be 動詞の後ろに原形を置いてしまった。"),
    ("この歌は多くの人に愛されています。", "This song is loving by many people.", "This song is loved by many people.", "loving", "concept",
     "「愛される」は受け身なので過去分詞 loved。loving（ing 形）では進行形の形になる。", "be 動詞の後ろは ing 形と覚えていた（進行形との混同）。"),
    ("その手紙は彼女によって送られました。", "The letter was sent by she.", "The letter was sent by her.", "by she", "notation",
     "前置詞 by の後ろの代名詞は目的格。she → her。", "能動態の主語 she をそのまま by の後ろに置いた。"),
    ("この本は多くの生徒に読まれています。", "This book is readed by many students.", "This book is read by many students.", "readed", "formula",
     "read は不規則動詞で、過去分詞はつづりが同じ read（発音は [red]）。", "規則動詞と同じように ed をつけた。"),
    ("その窓はトムによって割られました。", "The window was breaked by Tom.", "The window was broken by Tom.", "breaked", "formula",
     "break は不規則動詞で、過去分詞は broken。", "規則動詞と同じように ed をつけた。"),
    ("富士山はここから見ることができます。", "Mt. Fuji can seen from here.", "Mt. Fuji can be seen from here.", "can seen", "concept",
     "助動詞の後ろの受け身は can＋be＋過去分詞。be が必要。", "can の後ろに過去分詞を直接置けると考えた。"),
]


@gen("error_correction", 5, ["common_error", "computation"])
def err_form(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(FORM_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", etype, tempt, fix, f"{rule}正しくは {fix}",
                    ["文が受け身（be 動詞＋過去分詞）の形になっているかを確認する。", f"「{where}」の部分の誤りを見つける：{rule}", f"正しい英文：{fix}"],
                    "受け身は「主語の数・時制に合う be 動詞」と「正しい過去分詞」の2つがそろって成り立つ。両方を1つずつ確かめる。",
                    ["直した文を能動態にもどしてみて、もとの意味と合うかを確かめる。"],
                    ["be 動詞を落とす、または過去分詞の代わりに過去形・原形・ing 形を置く。", "主語の数や時制と be 動詞が合わない。"])


USE_ERR = [
    ("この絵はあなたのお姉さんによって描かれたのですか。", "Did this picture painted by your sister?", "Was this picture painted by your sister?", "Did", "concept",
     "受け身は be 動詞の文なので、疑問文は be 動詞 Was を主語の前に出す。", "過去の疑問文は Did で始めると覚えていた。"),
    ("この部屋は日曜日には掃除されません。", "This room doesn't cleaned on Sundays.", "This room isn't cleaned on Sundays.", "doesn't", "concept",
     "受け身の否定文は be 動詞の後ろに not。isn't（is not）を使う。", "三人称単数の否定文は doesn't と覚えていた。"),
    ("その川は落ち葉でおおわれていました。", "The river was covered of fallen leaves.", "The river was covered with fallen leaves.", "of", "notation",
     "「～でおおわれている」は be covered with ～。of は使わない。", "made of などの of と混同した。"),
    ("私は日本の歴史に興味があります。", "I am interesting in Japanese history.", "I am interested in Japanese history.", "interesting", "concept",
     "「（人が）興味がある」は be interested in。interesting は「（物事が）おもしろい」の意味。", "interest の ing 形と過去分詞を取り違えた。"),
    ("この机は木でできています。", "This desk makes of wood.", "This desk is made of wood.", "makes", "concept",
     "机は「作られる」側なので受け身 is made にする。makes では机が何かを作ることになる。", "日本語の「できている」を一般動詞の現在形で表そうとした。"),
    ("私の兄は音楽に興味があります。", "My brother is interested on music.", "My brother is interested in music.", "on", "condition",
     "「～に興味がある」は be interested in ～。前置詞は in。", "「～に」を on で表せると考えた。"),
    ("この寺はいつ建てられましたか。", "When did this temple build?", "When was this temple built?", "did ～ build", "concept",
     "寺は「建てられる」側なので受け身。疑問詞の後ろは was＋主語＋過去分詞。", "日本語の「建て」につられて能動の疑問文にした。"),
    ("私たちはその知らせに驚きました。", "We surprised at the news.", "We were surprised at the news.", "surprised の前", "concept",
     "「（人が）驚く」は be surprised at ～。be 動詞 were が必要。", "日本語の「驚いた」を過去形 surprised だけで表せると考えた。"),
    ("その箱はおもちゃでいっぱいでした。", "The box was filled of toys.", "The box was filled with toys.", "of", "notation",
     "「～でいっぱいだ」は be filled with ～。", "be full of ～ と混同した。"),
    ("これらの車は日本で作られていますか。― はい、そうです。", "Are these cars made in Japan? ― Yes, they do.", "Are these cars made in Japan? ― Yes, they are.", "they do", "concept",
     "受け身の疑問文には be 動詞で答える。Are で聞かれたら are。", "一般動詞の疑問文の答え方と混同した。"),
]


@gen("error_correction", 5, ["common_error", "condition_check"])
def err_usage(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(USE_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", etype, tempt, fix, f"{rule}正しくは {fix}",
                    ["否定文・疑問文で do / does / did を使っていないかを確認する。", "by 以外の前置詞を使う決まった言い方ではないかを確認する。", f"正しい英文：{fix}"],
                    "受け身は be 動詞の文。否定・疑問・答えはすべて be 動詞で作る。また、状態や気持ちを表す受け身は by 以外の前置詞と組にする。",
                    ["直した文を声に出して読み、be 動詞と過去分詞・前置詞の組み合わせが決まった言い方どおりかを確かめる。"],
                    ["受け身の疑問文・否定文に do / does / did を使う。", "どの受け身にも by を使う。"])


GENERATORS = [pp_form, passive_be, prep_choice, passive_meaning, q_answer,
              active_to_passive, passive_neg_q, build_order, aux_passive, wh_passive,
              explain_pair, made_of_from, write_intro, past_vs_pp,
              err_form, err_usage]
