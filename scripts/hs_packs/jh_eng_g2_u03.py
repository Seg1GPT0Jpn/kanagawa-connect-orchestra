"""単元パック：中学2年 英語 接続詞（when / if / because / that）・There is / are・must / have to / should。"""
from banks._common import desc, mc, order, sa, table
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem,
                         tp)

UNIT_ID = "JH-ENG-G2-U03"

PREREQUISITES = [
    ("JH-ENG-G1-U01", "be 動詞を主語の数で使い分けられること（is / are）。There is / are は後ろの名詞の数で be 動詞を選ぶ。"),
    ("JH-ENG-G1-U04", "助動詞 can の文の作り方（can＋原形、否定 can't、疑問 Can ～?）。must / should も同じ型で使う。"),
    ("JH-ENG-G1-U05", "過去形（was / were と一般動詞の過去形）。There was / were や had to、when 節の過去の文で使う。"),
    ("JH-ENG-G2-U01", "will / be going to の未来表現。I think (that) it will rain. や、when / if 節では未来でも現在形を使うことと比べる。"),
]
EXTENSIONS = [
    ("JH-ENG-G3-U04", "I know that ～. の that 節から、I know where he lives. のような間接疑問文へ広がる。"),
    ("JH-ENG-G3-U05", "if を使った「もし～なら」の文が、事実に反する仮定（If I were ～, I would ～.）の仮定法につながる。"),
    ("HS-ENG-U03", "高校では must の「～にちがいない」、should の「～のはずだ」など推量の意味や、助動詞＋have＋過去分詞を学ぶ。"),
]


def cap(s):
    return s[0].upper() + s[1:]


# ======================================================================
# 授業プリント
# ======================================================================

LESSON = lesson(
    goals=["接続詞 when / if / because / that を使って2つの文（〈主語＋動詞〉）をつなぎ、時・条件・理由・考えの内容を表せる。",
           "There is / are ～.（～がある・いる）を、後ろの名詞の数と時制に合わせて使い、否定文・疑問文も作れる。",
           "must / have to / should の意味と形を区別し、特に must not（禁止）と don't have to（不要）の違いを説明できる。"],
    duration=50,
    readiness=["be 動詞（is / are / was / were）を主語の数と時制に合わせて選べる（中1）。",
               "can＋動詞の原形の文と、その否定文・疑問文を作れる（中1）。",
               "will / be going to で未来のことを表せる（中2）。",
               "小学校の外国語で There is a park in my town. のような町紹介の表現にふれている。",
               "小学校の国語で「～とき」「もし～なら」「～から（理由）」のような、文と文をつなぐ言葉の働きを学んでいる。"],
    flow=[("導入：2つの文を1つに", 4, "I was watching TV. My mother came home. を「母が帰ってきたとき」でつなぐとどうなるか考える"),
          ("接続詞 when / if / because / that", 16, "4つの接続詞の意味と位置、カンマ、when / if 節の時制（例題1）"),
          ("There is / are", 12, "名詞の数で is / are、否定・疑問、There is ～ と ～ is … の使い分け（例題2）"),
          ("must / have to / should", 12, "義務・禁止・不要・助言の区別、has to / had to（例題3）"),
          ("まとめと確認", 6, "板書の3列で整理し、確認問題3問")],
    sections=[
        intro("in1", "文と文をつなぐ・ものの存在を伝える・ルールを伝える",
              "これまでは、1つの文に〈主語＋動詞〉が1組だけの文を中心に学んできました。この単元では、接続詞を使って〈主語＋動詞〉を2組ふくむ文を作ります。さらに、「～がある・いる」と存在を伝える There is / are の文と、「～しなければならない」「～すべきだ」とルールや助言を伝える助動詞を学びます。町の紹介や学校のきまりの説明など、身近な場面で使える表現です。",
              bullets=["I was watching TV when my mother came home.（母が帰ってきたとき、私はテレビを見ていた）",
                       "There are two parks in my town.（私の町には公園が2つある）",
                       "You must not run in the hallway.（廊下を走ってはいけない）"],
              points=[tp("1つ目の文で〈主語＋動詞〉が2組あることを色分けして見せ、接続詞が「つなぎ目」になっていることを確認させる。",
                         ask="この文の主語と動詞を全部見つけよう。", expect="I was watching と my mother came の2組。", timing="導入の冒頭")]),
        definition("df1", "接続詞 when / if / because / that",
                   "接続詞は〈主語＋動詞〉をふくむ2つのまとまりをつなぐ語です。when・if・because のまとまりは文の前半にも後半にも置けます。前半に置くときは、まとまりの終わりにカンマ（,）をつけます。",
                   formula="〈主語＋動詞 ～〉＋接続詞＋〈主語＋動詞 ～〉　／　接続詞＋〈主語＋動詞 ～〉, 〈主語＋動詞 ～〉",
                   bullets=["when「～するとき」：When I got home, my sister was cooking.",
                            "if「もし～ならば」：If you are free, let's play tennis.",
                            "because「～なので・～だから（理由）」：I stayed home because I had a cold.",
                            "that「～ということ」：I think (that) Ken is kind.（think / know / hope / say などの後ろ。that は省略できる）"],
                   conditions=["when / if のまとまりの中では、未来のことでも現在形で表す（If it rains tomorrow, ～. × If it will rain）。",
                               "because のまとまりだけで文を書くのは、Why ～? の答えのときに限る（Why ～? ― Because ～.）。",
                               "that のまとまりの動詞は、主節の時制や内容に合わせる（I think it will rain. など）。"],
                   points=[tp("when / if 節の中で未来でも現在形になることは、例文を口で何度も言わせて定着させる。",
                              caution="If it will be sunny tomorrow, ～ が最も多い誤り。", timing="定義の説明後"),
                           tp("that が省略された文（I think Ken is kind.）を見せ、think の後ろに〈主語＋動詞〉が続いていることに気づかせる。",
                              ask="I think Ken is kind. で think の目的語はどこまでか。", expect="Ken is kind 全体。")]),
        definition("df2", "There is / are ～.（～がある・いる）",
                   "「（ある場所に）～がある・いる」と、ものや人の存在を初めて相手に伝えるときは There is / are ～. を使います。be 動詞は後ろの名詞の数で決め、場所を表す語句はふつう文の後ろに置きます。",
                   formula="There is＋単数の名詞（数えられない名詞）＋場所.　／　There are＋複数の名詞＋場所.",
                   bullets=["There is a cat under the table.／There are three cats under the table.",
                            "過去：There was ～. ／ There were ～.",
                            "否定：There isn't a ～. ／ There aren't any ～.",
                            "疑問：Is there a ～? ― Yes, there is. / No, there isn't.　Are there any ～? ― Yes, there are. / No, there aren't.",
                            "数をたずねる：How many ～ are there in …? ― There are ～."],
                   conditions=["my bag / the book / Ken のように、相手もわかっている特定のものの場所を言うときは There is を使わず、My bag is on the desk. のように言う。",
                               "There の後ろの be 動詞が主語の数に合うかは、be 動詞の後ろの名詞で判断する。"],
                   points=[tp("There is ～. の主語は There ではなく後ろの名詞であることを、is / are の選び方から確認する。",
                              ask="There ( ) two books. で is と are のどちらか。決め手は？", expect="are。two books が複数だから。")]),
        theorem("th1", "must / have to / should の意味と形",
                "must＋原形（～しなければならない）｜ must not＋原形（～してはいけない）｜ have to＋原形（～しなければならない）｜ don't have to＋原形（～する必要はない）｜ should＋原形（～すべきだ・～したほうがよい）",
                ["must / should は助動詞なので、主語が何でも形は変わらず、後ろは原形（× musts、× must to）。",
                 "have to は主語が三人称単数なら has to、過去なら had to になる（must には過去形がないので、過去の義務は had to で表す）。",
                 "must not（mustn't）は「～してはいけない」という禁止。don't have to は「～する必要はない（しなくてもよい）」という不要。意味がまったく違う。",
                 "have to の否定文・疑問文は do / does / did を使う（Do I have to ～? ― No, you don't have to.）。",
                 "should は must よりやわらかく、「～したほうがいい」という助言を表すことが多い。"],
                body="助動詞（can / will / must / should）は、どれも〈助動詞＋原形〉という同じ型をしています。have to は形のうえでは一般動詞 have と同じルールで変化します。",
                points=[tp("must not と don't have to の違いは、「プールで走る」「日曜日に早起きする」などの具体的な場面で比べさせる。",
                           ask="日曜日は学校がない。「早起きしてはいけない」と「早起きしなくてもよい」はどちらが合う？", expect="早起きしなくてもよい＝You don't have to get up early.")]),
        derivation("dv1", "なぜ when / if の中では未来でも現在形なのか・なぜ don't have to は「不要」なのか",
                   ["① If it rains tomorrow, we will stay home. では、「明日雨が降る」は話し手が「（雨が降るという）条件」として設定している内容である。",
                    "② 「～ならば」の部分は、それが起きた場面を仮に「今」のこととして思い描いているので、英語では現在形で表すと考えるとわかりやすい。",
                    "③ 一方、その条件のもとで起きる結果（家にいる）はまだ先のことなので、主節には will を使う。",
                    "④ have to は「～しなければならない」。これを don't で打ち消すと「～しなければならない、ということはない」＝「～する必要はない」になる。",
                    "⑤ must not は must（しなければならない）の打ち消しではなく、not が後ろの動作を打ち消して「～しないことをしなければならない」＝「～してはいけない」になる。だから意味が大きく違う。"],
                   body="形のよく似た表現でも、何を打ち消しているのかを考えると意味の違いが説明できます。",
                   points=[tp("④⑤は「not がどこにかかるか」を矢印で板書すると理解しやすい。",
                              ask="You must not swim here. と You don't have to swim here. の違いを日本語で言うと？", expect="ここで泳いではいけない／ここで泳ぐ必要はない。",
                              caution="②は時制のルールを覚えるための説明で、すべての if 文にあてはまる規則ではないことに注意する。", timing="導出の説明時")]),
        example("ex1", "例題1　接続詞を使って2つの文をつなぐ",
                "（　）内の接続詞を使って、2つの文を1つの文にしなさい。(1) I was taking a bath. My father called me.（when）　(2) It will be sunny tomorrow. We will go to the beach.（if）　(3) I was tired. I went to bed early.（because）",
                ["(1) 「父が電話してきたとき」が when のまとまり：I was taking a bath when my father called me.",
                 "(2) 「晴れるなら」が if のまとまり。if の中は未来でも現在形 is：If it is sunny tomorrow, we will go to the beach.",
                 "(3) 理由は「疲れていた」なので because を前に：I went to bed early because I was tired."],
                "(1) I was taking a bath when my father called me.（When my father called me, I was taking a bath. も可）　(2) If it is sunny tomorrow, we will go to the beach.（We will go to the beach if it is sunny tomorrow. も可）　(3) I went to bed early because I was tired.",
                thinking="接続詞はどちらの文の前につくかを、意味（時・条件・理由）で判断する。if の中の will は現在形に変える。",
                points=[tp("(3) で I was tired because I went to bed early. と逆にする誤りを取り上げ、「理由はどちらか」を日本語で確かめさせる。",
                           ask="疲れていたから早く寝たのか、早く寝たから疲れていたのか。", expect="疲れていたから早く寝た。")],
                misconceptions=[("If it will be sunny tomorrow, we will go to the beach.", "if の中は未来でも現在形。If it is sunny tomorrow, ～."),
                                ("Because I was tired. I went to bed early.", "because のまとまりだけでは文にならない。1つの文にまとめる。")]),
        example("ex2", "例題2　There is / are の文",
                "日本語に合う英文を書きなさい。(1) 私の学校にはプールが1つあります。　(2) 箱の中にリンゴはいくつありますか。― 5つあります。　(3) 公園には子どもが1人もいませんでした。",
                ["(1) a pool は単数なので There is。場所 in my school は文の後ろ。",
                 "(2) 数をたずねるのは How many＋複数名詞＋are there ～? 答えは There are five.",
                 "(3) 過去で、children は複数なので There were。否定は weren't any。"],
                "(1) There is a pool in my school.　(2) How many apples are there in the box? ― There are five (apples).　(3) There weren't any children in the park.",
                thinking="be 動詞の後ろの名詞の数と、時制（今か過去か）の2つで is / are / was / were を決める。",
                points=[tp("(2) の How many の後ろの名詞を単数にする誤り（How many apple）に注意させる。"),
                        tp("(3) の children が child の複数形であることを確認し、were を選ぶ根拠にする。")],
                misconceptions=[("There is five apples in the box.", "five apples は複数なので There are。")]),
        example("ex3", "例題3　must / have to / should",
                "場面に合う英文を、（　）内の語を使って書きなさい。(1) 図書館で：「ここで食べ物を食べてはいけません」（must）　(2) 明日は休校です：「あなたは明日、学校へ来る必要はありません」（have）　(3) かぜをひいた友だちに：「あなたは家で休んだほうがいいよ」（should）",
                ["(1) 禁止は must not＋原形：You must not eat food here.",
                 "(2) 不要は don't have to＋原形：You don't have to come to school tomorrow.",
                 "(3) 助言は should＋原形：You should rest at home."],
                "(1) You must not eat food here.　(2) You don't have to come to school tomorrow.　(3) You should rest at home.（You should stay home and rest. も可）",
                thinking="禁止（してはいけない）か、不要（しなくてよい）か、助言（したほうがいい）かを、場面から先に決める。",
                points=[tp("(2) を You must not come to school tomorrow. とすると「来てはいけない」になることを、場面の違和感から気づかせる。",
                           ask="休校の日に学校へ行ったら怒られるのか。", expect="怒られるわけではない。行く必要がないだけ。")]),
        board("bd1", "板書案",
              [("① 接続詞", ["when：～とき", "if：もし～なら", "because：～なので", "that：～ということ（省略可）", "前半に置くとき → カンマ",
                             "when / if の中は未来でも現在形", "If it rains tomorrow, ～."]),
               ("② There is / are", ["There is＋単数（a cat）", "There are＋複数（two cats）", "過去：was / were", "否定：There aren't any ～.",
                                     "疑問：Is there ～? ― Yes, there is.", "How many ～ are there?", "特定のもの → My bag is ～."]),
               ("③ must / have to / should", ["must＋原形：しなければならない", "must not：してはいけない（禁止）", "have to / has to / had to", "don't have to：しなくてよい（不要）",
                                              "should：したほうがいい（助言）", "後ろはいつも原形"])],
              points=[tp("③の must not と don't have to は赤と青で色分けし、「禁止」と「不要」の違いが一目でわかるようにする。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("接続詞は「つなぎ目」。文中の〈主語＋動詞〉に下線を引かせ、2組あるかを毎回確認させる。", timing="接続詞の導入時"),
               tp("because と so（だから）の向きの違い（原因 because 結果／原因, so 結果）を、余裕があれば補足する。",
                  caution="because のまとまりを単独で書く誤りが作文で多いので、Why ～? の答え以外では使わないように指導する。"),
               tp("There is / are は、教室にあるものを使って Is there a clock in this room? と問答させると定着しやすい。",
                  ask="How many windows are there in this room?", expect="There are six windows."),
               tp("have to の三人称単数 has to と過去 had to は、must と並べた表で確認する。must には過去形がないことにふれる。"),
               tp("問題プリント D の誤答例は「if 節の will」「There is＋複数」「must not と don't have to の取り違え」の3つを中心にふり返らせる。")],
              misconceptions=[("If it will rain tomorrow, I will stay home.", "if の中は現在形。If it rains tomorrow, ～."),
                              ("There is many books on the desk.", "many books は複数なので There are。"),
                              ("You must not come tomorrow.（来なくてよい、のつもりで）", "不要は don't have to。You don't have to come tomorrow."),
                              ("She have to go now.", "主語が三人称単数なので has to。")]),
        summary("sm1", "まとめ",
                ["when（とき）・if（もし～なら）・because（～なので）・that（～ということ）で〈主語＋動詞〉をつなぐ。when / if の中は未来でも現在形。",
                 "There is＋単数／There are＋複数で「～がある・いる」。過去は was / were。特定のものには使わない。",
                 "must＝しなければならない、must not＝禁止、have to（has to / had to）＝しなければならない、don't have to＝不要、should＝助言。後ろはいつも原形。"]),
        check("ck1", "確認問題",
              [("「もし明日雨が降れば、家にいます」を英語にしなさい。", "If it rains tomorrow, I will stay home.（I will stay home if it rains tomorrow. も可）"),
               ("There (is / are) some eggs in the box. の正しいほうを選びなさい。", "are（some eggs が複数）"),
               ("You don't have to run. と You must not run. の意味の違いを答えなさい。", "前者は「走る必要はない」（不要）、後者は「走ってはいけない」（禁止）。")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

CONJ_WHY = {
    "when": "when は「～するとき」と時を表す。",
    "if": "if は「もし～ならば」と条件を表す。",
    "because": "because は「～なので」と理由を表す。",
    "that": "that は think / know / hope などの後ろで「～ということ」を表し、ここでは使えない。",
}
# (日本語, 空所つき英文, 正答)
CONJ = [
    ("母が帰宅したとき、私は宿題をしていた。", "I was doing my homework (　　) my mother came home.", "when"),
    ("もしひまなら、私を手伝ってくれませんか。", "(　　) you are free, can you help me?", "if"),
    ("熱があったので、私は学校を休んだ。", "I didn't go to school (　　) I had a fever.", "because"),
    ("私はケンが正しいと思う。", "I think (　　) Ken is right.", "that"),
    ("子どものころ、私はよく川で泳いだ。", "(　　) I was a child, I often swam in the river.", "when"),
    ("急げば、その電車に間に合いますよ。", "You can catch the train (　　) you hurry.", "if"),
    ("その本はとてもおもしろかったので、私は2回読んだ。", "I read the book twice (　　) it was very interesting.", "because"),
    ("私は、彼女が来週日本に来ることを知っている。", "I know (　　) she will come to Japan next week.", "that"),
    ("駅に着いたとき、雨が降っていた。", "It was raining (　　) I got to the station.", "when"),
    ("もし質問があれば、手をあげてください。", "(　　) you have any questions, please raise your hand.", "if"),
    ("道路がぬれていたので、私たちはゆっくり歩いた。", "We walked slowly (　　) the road was wet.", "because"),
    ("私は、あなたがそのテストに合格することを願っている。", "I hope (　　) you will pass the test.", "that"),
    ("父は若いころ、サッカー選手だった。", "My father was a soccer player (　　) he was young.", "when"),
    ("疲れているなら、早く寝なさい。", "(　　) you are tired, go to bed early.", "if"),
]


@gen("basic_check", 4, ["concept", "condition_check"])
def conj_choice(r):
    jp, s, ok = r.choice(CONJ)
    wrongs = [w for w in ("when", "if", "because", "that") if w != ok]
    if s.startswith("(　　)"):
        ok_c, wrongs_c = cap(ok), [cap(w) for w in wrongs]
    else:
        ok_c, wrongs_c = ok, wrongs
    jp_need = {"when": "「～とき」", "if": "「もし～なら」", "because": "「～なので」", "that": "「～ということ」"}[ok]
    why = {wc: (CONJ_WHY[w] + f"この文の日本語は{jp_need}を表しているので合わない。", "接続詞の意味") for w, wc in zip(wrongs, wrongs_c)}
    return mc(f"日本語に合うように、（　）に入る最も適切な語を選びなさい。\n{jp}\n{s}", [ok_c] + wrongs_c,
              f"日本語の{jp_need}に当たる接続詞は {ok}。答え：{ok_c}", d=1,
              ap="日本語の中で、2つの部分をつないでいる言葉（とき・もし～なら・ので・ということ）を探す。",
              steps=["日本語を2つのまとまりに分ける。", f"つなぎの言葉は{jp_need}。", f"答え：{ok_c}"],
              alt=["選んだ接続詞を入れた英文を日本語に訳し直し、問題の日本語と一致するかを確かめる。"],
              pc=[("2つのまとまりの関係（時・条件・理由・内容）を判断している", 1), ("正しい接続詞を選んでいる", 1)],
              pit=["when と if を取り違える（「～とき」と「もし～なら」）。", "because のまとまりを結果のほうにつける。"], why=why)


# (名詞句（英）, 単数か, 場所, 日本語)
THERE_N = [
    ("a big tree", True, "in the park", "公園に大きな木が1本"), ("two cats", False, "under the table", "テーブルの下にネコが2匹"),
    ("some milk", True, "in the glass", "コップに牛乳が少し"), ("many students", False, "in the gym", "体育館にたくさんの生徒"),
    ("a library", True, "near my house", "私の家の近くに図書館が1つ"), ("three bridges", False, "over the river", "その川に橋が3つ"),
    ("an old castle", True, "in the town", "その町に古い城が1つ"), ("some eggs", False, "in the fridge", "冷蔵庫に卵がいくつか"),
    ("a lot of water", True, "in the bottle", "びんに水がたくさん"), ("five children", False, "in the room", "部屋に子どもが5人"),
    ("a clock", True, "on the wall", "壁に時計が1つ"), ("a lot of people", False, "at the station", "駅にたくさんの人"),
]


@gen("basic_check", 4, ["computation", "condition_check"])
def there_be(r):
    np, sing, place, jp = r.choice(THERE_N)
    past = r.random() < 0.5
    ok = ("was" if sing else "were") if past else ("is" if sing else "are")
    jpv = "ありました" if past else "あります"
    if jp.endswith(("人", "匹", "生徒")):
        jpv = "いました" if past else "います"
    tword = " yesterday" if past else ""
    num_reason = "単数（または数えられない名詞）" if sing else "複数"
    wrongs = [w for w in ("is", "are", "was", "were") if w != ok]
    why = {}
    for w in wrongs:
        w_sing = w in ("is", "was")
        w_past = w in ("was", "were")
        reasons = []
        if w_sing != sing:
            reasons.append(f"{np} は{num_reason}なので、{w} は数が合わない")
        if w_past != past:
            reasons.append("過去のことなので現在形の " + w + " は合わない" if past else "今のことなので過去形の " + w + " は合わない")
        why[w] = ("。".join(reasons) + "。", "There is / are の be 動詞の選び方")
    return mc(f"日本語に合うように、（　）に入る最も適切な語を選びなさい。\n{('昨日、' if past else '')}{jp}{jpv}。\nThere (　　) {np} {place}{tword}.", [ok] + wrongs,
              f"There ～ の be 動詞は後ろの名詞 {np}（{num_reason}）と時制（{'過去' if past else '現在'}）で決まる。答え：{ok}", d=1,
              ap="There の後ろの be 動詞は、be 動詞の後ろにある名詞の数と、今のことか過去のことかの2つで決める。",
              steps=[f"be 動詞の後ろの名詞は {np} → {num_reason}。", f"時制は{'過去（yesterday）' if past else '現在'}。", f"答え：{ok}"],
              alt=[f"There を取って {np} を主語にした文（{cap(np)} {ok} {place}.）を考えると、be 動詞の数が確かめられる。"],
              pc=[("名詞の数を判断している", 1), ("時制も合わせて正しく選んでいる", 1)],
              pit=["a lot of people や many students のような複数名詞に is を使う。", "数えられない名詞（milk, water）に are を使う。"], why=why)


MODAL_MEAN = [
    ("ここで写真をとってはいけません。", "You (　　) take pictures here.", "must not"),
    ("明日は日曜日なので、早く起きる必要はありません。", "It's Sunday tomorrow. You (　　) get up early.", "don't have to"),
    ("暗くなる前に家に帰らなければなりません。", "You (　　) come home before dark.", "must"),
    ("かぜをひいているなら、医者にみてもらったほうがいいよ。", "You (　　) see a doctor if you have a cold.", "should"),
    ("プールのそばで走ってはいけません。", "You (　　) run near the pool.", "must not"),
    ("この本は今日返す必要はありません。", "You (　　) return this book today.", "don't have to"),
    ("試合に勝つために、私たちは毎日練習しなければならない。", "We (　　) practice every day to win the game.", "must"),
    ("寝る前にもっと水を飲んだほうがいいよ。", "You (　　) drink more water before bed.", "should"),
    ("授業中に携帯電話を使ってはいけません。", "You (　　) use your phone during class.", "must not"),
    ("私のために料理をする必要はありませんよ。", "You (　　) cook for me.", "don't have to"),
    ("あなたは今すぐ宿題を終わらせなければなりません。", "You (　　) finish your homework right now.", "must"),
    ("あなたはお母さんにお礼を言ったほうがいいよ。", "You (　　) say thank you to your mother.", "should"),
]
MODAL_DESC = {"must": "「～しなければならない」（義務）", "must not": "「～してはいけない」（禁止）",
              "don't have to": "「～する必要はない」（不要）", "should": "「～したほうがよい・～すべきだ」（助言）"}


@gen("basic_check", 4, ["concept", "condition_check"])
def modal_meaning(r):
    jp, s, ok = r.choice(MODAL_MEAN)
    wrongs = [w for w in MODAL_DESC if w != ok]
    why = {w: (f"{w} は{MODAL_DESC[w]}を表すので、日本語に合わない。", "must / have to / should の意味の区別") for w in wrongs}
    return mc(f"日本語に合うように、（　）に入る最も適切なものを選びなさい。\n{jp}\n{s}", [ok] + wrongs,
              f"日本語は{MODAL_DESC[ok]}を表しているので {ok}。", d=1,
              ap="日本語の文末が「～しなければならない」「～してはいけない」「～する必要はない」「～したほうがいい」のどれかを見る。",
              steps=["日本語の文末の意味を確かめる。", f"{MODAL_DESC[ok]}を表すのは {ok}。", f"答え：{ok}"],
              alt=["must not と don't have to で迷ったら、「してしまったら怒られるか（禁止）」「しなくても困らないだけか（不要）」を考える。"],
              pc=[("文末の意味を正しく判断している", 1), ("正しい表現を選んでいる", 1)],
              pit=["must not と don't have to を取り違える。", "should を「～しなければならない」と強く訳す。"], why=why)


# (主節, if / when, 主語, 原形, 三単現, 残り, 日本語)
IF_TENSE = [
    ("we will stay home", "If", "it", "rain", "rains", "tomorrow", "もし明日雨が降ったら、私たちは家にいるつもりだ。"),
    ("I will call you", "When", "I", "get", "get", "to the station", "駅に着いたら、あなたに電話します。"),
    ("let's go fishing", "If", "it", "be", "is", "sunny next Sunday", "もし今度の日曜日が晴れなら、つりに行こう。"),
    ("I will show him this picture", "When", "Ken", "come", "comes", "here tomorrow", "明日ケンがここに来たら、私は彼にこの写真を見せるつもりだ。"),
    ("you will be late", "If", "you", "miss", "miss", "the bus", "もしバスに乗り遅れたら、あなたは遅刻するだろう。"),
    ("she will be very happy", "If", "she", "win", "wins", "the race", "もしレースに勝てば、彼女はとても喜ぶだろう。"),
    ("I'll tell her the news", "When", "my sister", "come", "comes", "home", "姉が帰宅したら、私はその知らせを伝えるつもりだ。"),
    ("we can play outside", "If", "the snow", "stop", "stops", "soon", "もしすぐに雪がやめば、外で遊べる。"),
    ("I will buy a new bike", "When", "I", "be", "am", "sixteen", "16歳になったら、私は新しい自転車を買うつもりだ。"),
]


@gen("basic_check", 4, ["condition_check", "common_error"])
def if_tense(r):
    main, cj, subj, base, pres, rest, jp = r.choice(IF_TENSE)
    past = {"rain": "rained", "get": "got", "be": "was" if subj in ("it", "I", "she", "Ken") else "were", "come": "came", "miss": "missed",
            "win": "won", "stop": "stopped"}[base]
    ok = pres
    wrongs = [f"will {base}", past, base if base != pres else ("to " + base)]
    if base == "be":
        wrongs = ["will be", past, "be"]
    why = {wrongs[0]: (f"{cj.lower()} のまとまりの中では、未来のことでも will を使わず現在形で表す。", "時・条件を表す接続詞の中の時制"),
           wrongs[1]: ("これから先のことを表す文なので、過去形は使わない。", "時制の判断"),
           wrongs[2]: (f"主語 {subj} に合う現在形にする必要がある。" if base != pres or base == "be" else "to＋原形では文の動詞にならない。", "主語と動詞の一致")}
    return mc(f"日本語に合うように、（　）に入る最も適切なものを選びなさい。\n{jp}\n{cj} {subj} (　　) {rest}, {main}.", [ok] + wrongs,
              f"{cj.lower()}（{'もし～なら' if cj == 'If' else '～とき'}）のまとまりの中では、未来のことでも現在形を使う。主語 {subj} に合わせて {ok}。", d=2,
              ap=f"{cj} のまとまりの中か、外（主節）かを確かめる。中なら未来のことでも現在形。",
              steps=[f"空所は {cj} のまとまりの中にある。", "未来のことでも現在形で表す。", f"主語 {subj} に合わせて {ok}。"],
              alt=[f"主節（{main}）のほうは未来のことなので will などを使っていることと見比べ、{cj.lower()} の中だけ現在形になっていることを確かめる。"],
              pc=[("if / when の中では現在形を使うと判断している", 1), ("主語に合った形を選んでいる", 1)],
              pit=["日本語の「明日」「～したら」につられて will を入れる。", "三人称単数の s を落とす。"], why=why)


# (質問, 正答, [(誤答, 理由)])
THERE_QA = [
    ("Is there a convenience store near here?", "Yes, there is.",
     [("Yes, it is.", "Is there ～? には there を使って答える。"), ("Yes, there are.", "質問が Is there なので is で答える。"), ("Yes, I do.", "be 動詞の疑問文には do で答えない。")]),
    ("Are there any good restaurants in your town?", "Yes, there are.",
     [("Yes, they are.", "Are there ～? には there を使って答える。"), ("Yes, there is.", "質問が Are there なので are で答える。"), ("Yes, it does.", "be 動詞の疑問文には does で答えない。")]),
    ("Was there a big festival in your city last year?", "No, there wasn't.",
     [("No, it wasn't.", "Was there ～? には there を使って答える。"), ("No, there weren't.", "質問が Was there なので wasn't で答える。"), ("No, there didn't.", "be 動詞の疑問文には did で答えない。")]),
    ("Were there many people at the concert?", "Yes, there were.",
     [("Yes, they were.", "Were there ～? には there を使って答える。"), ("Yes, there was.", "質問が Were there なので were で答える。"), ("Yes, there did.", "be 動詞の疑問文には did で答えない。")]),
    ("How many students are there in your class?", "There are thirty-two.",
     [("There is thirty-two.", "thirty-two（students）は複数なので are。"), ("Yes, there are.", "How many でたずねられたら、Yes / No ではなく数を答える。"), ("They are thirty-two.", "「～人いる」は There are ～. で答える。")]),
    ("How many bedrooms are there in your house?", "There are three.",
     [("There is three.", "three（bedrooms）は複数なので are。"), ("Yes, there are three.", "How many の疑問文には Yes / No をつけずに数を答える。"), ("There are three bedroom.", "three のあとに名詞を言うなら複数形 bedrooms にする。")]),
    ("Is there any milk in the fridge?", "No, there isn't.",
     [("No, there aren't.", "milk は数えられない名詞で、質問も Is there なので isn't で答える。"), ("No, it isn't.", "Is there ～? には there を使って答える。"), ("No, there don't.", "be 動詞の疑問文には don't で答えない。")]),
    ("Are there any pictures on the wall?", "No, there aren't.",
     [("No, there isn't.", "質問が Are there なので aren't で答える。"), ("No, they aren't.", "Are there ～? には there を使って答える。"), ("No, there doesn't.", "be 動詞の疑問文には doesn't で答えない。")]),
]


@gen("basic_check", 4, ["computation", "concept"])
def there_qa(r):
    q, ok, wrongs = r.choice(THERE_QA)
    return mc(f"次の質問への答えとして最も適切なものを選びなさい。\n{q}", [ok] + [w for w, _ in wrongs],
              f"There is / are の疑問文には there と be 動詞を使って答え、How many ～ are there? には There are＋数. で答える。答え：{ok}", d=2,
              ap="質問の文頭（Is there / Are there / Was there / How many）を見て、答えに使う be 動詞と形を決める。",
              steps=["質問の be 動詞と時制を確認する。", "答えの主語は there にする（it / they にしない）。", f"答え：{ok}"],
              alt=["答えの省略された部分を補ってみる（Yes, there is a convenience store near here. など）と、組み合わせが正しいかを確かめられる。"],
              pc=[("there を使って答えることを理解している", 1), ("be 動詞の数・時制が合っている", 1)],
              pit=["Yes, it is. のように there 以外の主語で答える。", "How many の疑問文に Yes / No で答える。"],
              why={w: (reason, "There is / are の疑問文と答え方") for w, reason in wrongs})


# ======================================================================
# B 標準演習
# ======================================================================

# (主語, be 動詞の数, 原形, 三単現, 過去, 残り, 日本語主語)
HAVE_TO = [
    ("Ken", True, "clean", "cleans", "cleaned", "his room", "ケン"), ("I", False, "get", "get", "got", "up at six", "私"),
    ("My sister", True, "study", "studies", "studied", "for the test", "姉"), ("We", False, "walk", "walk", "walked", "to school", "私たち"),
    ("Tom", True, "help", "helps", "helped", "his mother", "トム"), ("They", False, "finish", "finish", "finished", "the work", "彼ら"),
    ("Yumi", True, "practice", "practices", "practiced", "the piano", "ユミ"), ("You", False, "wear", "wear", "wore", "a uniform", "あなた"),
]


@gen("standard_practice", 4, ["computation", "condition_check"])
def have_to_rewrite(r):
    s, third, base, v3, past, rest, sj = r.choice(HAVE_TO)
    kind = r.choice(["pres", "past", "neg", "q"])
    ht = "has to" if third else "have to"
    do = "Does" if third else "Do"
    dont = "doesn't" if third else "don't"
    sl = s if s in ("I", "Ken", "Tom", "Yumi") else s[0].lower() + s[1:]
    if kind == "pres":
        stem = f"次の英文を、have to を使ってほぼ同じ意味の文に書きかえなさい。\n{s} must {base} {rest}."
        ans = f"{s} {ht} {base} {rest}."
        stp = ["must＋原形 は have to＋原形 とほぼ同じ意味。", f"主語 {s} が{'三人称単数なので has to' if third else '三人称単数ではないので have to'}。", f"答え：{ans}"]
    elif kind == "past":
        stem = f"次の英文を、文末に yesterday を加えて過去の文に書きかえなさい。\n{s} must {base} {rest}."
        ans = f"{s} had to {base} {rest} yesterday."
        stp = ["must には過去形がないので、have to の過去形 had to を使う。", "had to の後ろは原形のまま。", f"答え：{ans}"]
    elif kind == "neg":
        stem = f"次の英文を、「～する必要はない」という意味の否定文に書きかえなさい。\n{s} {ht} {base} {rest}."
        ans = f"{s} {dont} have to {base} {rest}."
        stp = [f"have to の否定は {dont} have to（～する必要はない）。", f"{dont} の後ろは has ではなく原形 have。", f"答え：{ans}"]
    else:
        ansr = "I do" if s == "You" else ("you do" if s == "I" else ("we do" if s == "We" else ("they do" if s == "They" else ("he does" if s in ("Ken", "Tom") else "she does"))))
        stem = f"次の英文を疑問文に書きかえ、Yes で答える文も書きなさい。\n{s} {ht} {base} {rest}."
        ans = f"{do} {sl} have to {base} {rest}? ― Yes, {ansr}."
        stp = [f"have to の疑問文は {do} を主語の前に置き、has は原形 have にもどす。", f"答えは {do.lower()} を使う：Yes, {ansr}.", f"答え：{ans}"]
    return sa(stem, ans, f"have to は一般動詞 have と同じように変化する（has to / had to、否定・疑問は do / does / did）。答え：{ans}", d=2, p=4,
              ap="must は形が変わらない助動詞、have to は一般動詞の have と同じように主語・時制で変化する、という違いに注目する。",
              steps=stp,
              alt=["書きかえた文を日本語に訳し、「～しなければならない」「～しなければならなかった」「～する必要はない」の意味になっているかを確かめる。"],
              pc=[("have / has / had や do / does の形が正しい", 2), ("to の後ろを原形にし、語順が正しい", 2)],
              pit=["三人称単数の主語で have to のままにする。", "否定文で doesn't has to としてしまう。"])


# (元の文, 指示, 答え, 別解, ポイント)
THERE_RW = [
    ("My town has two big parks.", "There で始めて、ほぼ同じ意味の文に", "There are two big parks in my town.", [], "two big parks は複数なので There are。my town は in my town として文の後ろに置く。"),
    ("Our school has a large library.", "There で始めて、ほぼ同じ意味の文に", "There is a large library in our school.", ["There's a large library in our school."], "a large library は単数なので There is。"),
    ("There is ［a dog］ in the garden.", "［　］の部分を three dogs にかえた文に", "There are three dogs in the garden.", [], "three dogs は複数なので are にかえる。"),
    ("There are some books on the desk.", "否定文に", "There aren't any books on the desk.", ["There are not any books on the desk.", "There are no books on the desk."], "否定文では some を any にかえる。"),
    ("There is a bank near the station.", "疑問文に", "Is there a bank near the station?", [], "be 動詞 is を there の前に出す。"),
    ("There are many students in the gym.", "文末に yesterday を加えて過去の文に", "There were many students in the gym yesterday.", [], "過去で複数なので were。"),
    ("There are ［five］ rooms in this house.", "［　］の部分をたずねる疑問文に", "How many rooms are there in this house?", [], "数をたずねるので How many＋複数名詞＋are there ～?"),
    ("There is some water in the bottle.", "否定文に", "There isn't any water in the bottle.", ["There is not any water in the bottle.", "There is no water in the bottle."], "water は数えられない名詞なので is のまま。some を any にかえる。"),
    ("The week has seven days.", "There で始めて、ほぼ同じ意味の文に", "There are seven days in a week.", [], "seven days は複数なので There are。「1週間に」は in a week。"),
    ("There were some children in the park.", "疑問文に", "Were there any children in the park?", [], "be 動詞 were を there の前に出し、some を any にかえる。"),
]


@gen("standard_practice", 4, ["computation", "application"])
def there_rewrite(r):
    src, inst, ans, vs, point = r.choice(THERE_RW)
    return sa(f"次の英文を、{inst}書きかえなさい。\n{src}", ans,
              f"{point}答え：{ans}", d=2, p=4, v=vs or None,
              ap="There is / are の文では、be 動詞の後ろの名詞の数と時制で be 動詞を決める。否定・疑問は be 動詞の文のルールで作る。",
              steps=["be 動詞の後ろにくる名詞の数（単数・複数）を確認する。", "時制と文の種類（否定・疑問）に合わせて be 動詞の形と位置を決める。", f"答え：{ans}"],
              alt=["書きかえた文を日本語に訳して、「～がある（あった）」「～はない」「～はありますか」の意味になっているかを確かめる。"],
              pc=[("be 動詞の形（数・時制）が正しい", 2), ("語順と some / any などが正しい", 2)],
              pit=["複数の名詞に is を使う。", "否定文・疑問文で some を any にかえ忘れる。"])


ORDERS = [
    ("私が家に帰ったとき、弟は眠っていた。", ["my brother", "was", "sleeping", "when", "I", "came", "home"], "主節＋when＋主語＋動詞"),
    ("もし明日晴れたら、ハイキングに行こう。", ["if", "it", "is", "sunny", "tomorrow,", "let's", "go", "hiking"], "If＋主語＋現在形, 主節（if の中は未来でも現在形）"),
    ("私は、この本はおもしろいと思う。", ["I", "think", "that", "this book", "is", "interesting"], "think＋that＋主語＋動詞"),
    ("雨が降っていたので、私たちは家にいた。", ["we", "stayed", "home", "because", "it", "was", "raining"], "主節＋because＋理由"),
    ("机の上にペンが3本ある。", ["there", "are", "three", "pens", "on", "the desk"], "There are＋複数名詞＋場所"),
    ("この近くに郵便局はありますか。", ["is", "there", "a post office", "near", "here"], "Is there ～? の疑問文"),
    ("あなたのクラスには何人の生徒がいますか。", ["how", "many", "students", "are", "there", "in", "your class"], "How many＋複数名詞＋are there ～?"),
    ("あなたは今日、皿を洗う必要はありません。", ["you", "don't", "have", "to", "wash", "the dishes", "today"], "don't have to＋原形（不要）"),
    ("ここでサッカーをしてはいけません。", ["you", "must", "not", "play", "soccer", "here"], "must not＋原形（禁止）"),
    ("あなたはもっと野菜を食べたほうがいい。", ["you", "should", "eat", "more", "vegetables"], "should＋原形（助言）"),
    ("私の兄は昨日、早く起きなければならなかった。", ["my brother", "had", "to", "get", "up", "early", "yesterday"], "had to＋原形（過去の義務）"),
    ("私は、彼女がすぐに来ることを知っています。", ["I", "know", "that", "she", "will", "come", "soon"], "know＋that＋主語＋will＋原形"),
]


@gen("standard_practice", 4, ["application", "computation"])
def build_order(r):
    jp, parts, pat = r.choice(ORDERS)
    sent = cap(" ".join(parts)).replace(" ,", ",") + ("?" if jp.endswith("か。") else ".")
    return order(f"日本語に合うように、次の語句を並べかえて英文を完成させなさい。ただし、文頭にくる語も小文字で示してある。\n{jp}", parts,
                 f"{sent}　ポイント：{pat}。", d=2, p=4,
                 ap="文の型（接続詞の文・There is / are の文・助動詞の文）を先に決め、〈主語＋動詞〉のまとまりを作ってから並べる。",
                 steps=[f"文の型を決める：{pat}。", "〈主語＋動詞〉のまとまりを作る。", "場所・時を表す語句を最後に置く。", f"完成文：{sent}"],
                 alt=["完成した英文を日本語に訳し直して、問題の日本語と一致するかを確かめる。"],
                 pc=[("文の骨組み（主語・動詞・接続詞などの位置）が正しい", 2), ("残りの語句の順序が正しい", 2)],
                 pit=["接続詞のまとまりの中で主語と動詞の順を逆にする。", "must not / don't have to の語順をくずす。"])


# (文1, 文2, 接続詞, 答え, 別解)
COMBINE = [
    ("It was raining.", "We played soccer in the gym.", "because", "We played soccer in the gym because it was raining.", ["Because it was raining, we played soccer in the gym."]),
    ("I was reading a book.", "My friend visited me.", "when", "I was reading a book when my friend visited me.", ["When my friend visited me, I was reading a book."]),
    ("You are hungry.", "You can eat this bread.", "if", "If you are hungry, you can eat this bread.", ["You can eat this bread if you are hungry."]),
    ("Mika is a good singer.", "I think so.", "that", "I think that Mika is a good singer.", ["I think Mika is a good singer."]),
    ("I had a headache.", "I went to bed early.", "because", "I went to bed early because I had a headache.", ["Because I had a headache, I went to bed early."]),
    ("My father was a student.", "He lived in Osaka.", "when", "When my father was a student, he lived in Osaka.", ["My father lived in Osaka when he was a student."]),
    ("You have time.", "Please call me.", "if", "If you have time, please call me.", ["Please call me if you have time."]),
    ("The story is true.", "Everyone knows it.", "that", "Everyone knows that the story is true.", ["Everyone knows the story is true."]),
    ("The bus was late.", "Ken was late for school.", "because", "Ken was late for school because the bus was late.", ["Because the bus was late, Ken was late for school."]),
    ("I opened the door.", "The cat ran out.", "when", "When I opened the door, the cat ran out.", ["The cat ran out when I opened the door."]),
]


@gen("standard_practice", 4, ["application", "concept"])
def combine(r):
    a, b, cj, ans, vs = r.choice(COMBINE)
    role = {"because": "理由", "when": "時", "if": "条件", "that": "考え・知っている内容"}[cj]
    return sa(f"次の2つの英文を、{cj} を使って1つの文にしなさい。\n{a}　{b}", ans,
              f"{cj} は{role}を表すまとまりをつくる。{cj} のまとまりを前に置くときはカンマをつける。答え：{ans}", d=3, p=4, v=vs,
              ap=f"2つの文のうち、どちらが{role}を表しているかを決め、そちらの文の前に {cj} を置く。",
              steps=[f"{role}を表す文を見つける。", f"その文の前に {cj} を置く。", "もう一方の文とつなぎ、前半に置いたときはカンマをつける。", f"答え：{ans}"],
              alt=["完成した文を日本語に訳し、2つの文の関係（原因と結果、時、条件、考えの内容）が正しく表されているかを確かめる。"],
              pc=[("接続詞を正しい文の前に置いている", 2), ("語順・カンマ・代名詞が正しい", 2)],
              pit=["because を結果の文の前につけ、原因と結果を逆にする。", "that の文で think so の so を残す。"])


# (日本語, 空所つき英文, 正答, [(誤答, 理由)])
THINK_WILL = [
    ("私は、明日は雨が降ると思う。", "I think it (　　) tomorrow.", "will rain",
     [("rains", "that（省略）の後ろは if / when の中ではないので、未来のことは will で表す。"), ("will rains", "will の後ろは原形。"), ("is rain", "is と rain の2つの動詞を並べることはできない。")]),
    ("もし明日雨が降れば、試合は中止になるだろう。", "If it (　　) tomorrow, the game will be canceled.", "rains",
     [("will rain", "if の中では未来のことでも現在形を使う。"), ("rain", "主語 it は三人称単数なので s が必要。"), ("is raining", "未来の条件を表す if の中では、ふつう現在形 rains を使う。")]),
    ("私は、ケンが私たちを手伝ってくれると思う。", "I think Ken (　　) us.", "will help",
     [("helps", "これから先のことなので will を使う。helps は「ふだん手伝う」という意味になる。"), ("will helps", "will の後ろは原形。"), ("is help", "is と help の2つの動詞を並べることはできない。")]),
    ("ケンが来たら、出発しよう。", "When Ken (　　), let's start.", "comes",
     [("will come", "when の中では未来のことでも現在形を使う。"), ("come", "主語 Ken は三人称単数なので s が必要。"), ("came", "これから先のことなので過去形は使わない。")]),
    ("私は、彼女はそのニュースを聞いて喜ぶだろうと思う。", "I think she (　　) happy to hear the news.", "will be",
     [("is", "これから先のことなので will be を使う。"), ("will is", "will の後ろは原形 be。"), ("be", "主語 she の後ろに原形 be だけを置くことはできない。")]),
    ("私が駅に着いたら、メールします。", "I'll send you an e-mail when I (　　) to the station.", "get",
     [("will get", "when の中では未来のことでも現在形を使う。"), ("gets", "主語 I には s をつけない。"), ("got", "これから先のことなので過去形は使わない。")]),
    ("私は、その電車はすぐに来ると思う。", "I think the train (　　) soon.", "will come",
     [("comes", "that（省略）の後ろは if / when の中ではないので、未来のことは will で表す。"), ("will comes", "will の後ろは原形。"), ("coming", "ing 形だけでは文の動詞にならない。")]),
    ("もしあなたが忙しいなら、私が手伝います。", "If you (　　) busy, I'll help you.", "are",
     [("will be", "if の中では未来のことでも現在形を使う。"), ("is", "主語 you に合う be 動詞は are。"), ("be", "主語の後ろに原形 be をそのまま置くことはできない。")]),
]


@gen("standard_practice", 4, ["cross_unit", "condition_check"], rel=["JH-ENG-G2-U01"])
def think_will(r):
    jp, s, ok, wrongs = r.choice(THINK_WILL)
    return mc(f"日本語に合うように、（　）に入る最も適切なものを選びなさい。\n{jp}\n{s}", [ok] + [w for w, _ in wrongs],
              f"think (that) ～ の中では未来のことを will で表すが、if / when の中では未来のことでも現在形を使う。答え：{ok}", d=3,
              ap="空所が if / when のまとまりの中にあるのか、think (that) の後ろにあるのかを先に確かめる。",
              steps=["空所がどのまとまりの中にあるかを確認する。", "if / when の中なら現在形、think (that) の後ろで未来のことなら will＋原形。", f"答え：{ok}"],
              alt=["前の単元の未来表現（will / be going to）と比べ、if / when の中だけが例外的に現在形になることを確かめる。"],
              pc=[("空所のあるまとまりの種類を判断している", 2), ("時制と形を正しく選んでいる", 2)],
              pit=["if / when の中でも will を使う。", "think の後ろの未来のことを現在形で書く。"],
              why={w: (reason, "接続詞のまとまりの中の時制") for w, reason in wrongs})


# ======================================================================
# C 思考力・記述応用
# ======================================================================

PAIRS = [
    ("You must not bring lunch tomorrow.", "You don't have to bring lunch tomorrow.",
     "A は must not で「明日は昼食を持ってきてはいけない」という禁止を表す。B は don't have to で「明日は昼食を持ってくる必要はない（持ってきてもよい）」という不要を表す。A は持ってくると規則に反するが、B は持ってきても問題ない。"),
    ("If Ken comes, I will tell him.", "When Ken comes, I will tell him.",
     "A は if で「もしケンが来たら（来るかどうかはわからない）」という条件を表す。B は when で「ケンが来たときに（来ることはわかっている）」という時を表す。来るかどうかがわかっているかどうかが違う。"),
    ("There is a book on the desk.", "The book is on the desk.",
     "A は There is で「机の上に（ある）1冊の本がある」と、相手が知らないものの存在を初めて伝える。B は the book が主語で「その本は机の上にある」と、相手もわかっている特定の本の場所を伝える。"),
    ("I stayed home because it was cold.", "It was cold, so I stayed home.",
     "どちらも「寒かったので家にいた」という意味だが、A は because を理由（寒かった）の前に置き、B は so（だから）を結果（家にいた）の前に置いている。because は原因の側、so は結果の側につく。"),
    ("You must study hard.", "You should study hard.",
     "A は must で「一生けんめい勉強しなければならない」という強い義務を表す。B は should で「一生けんめい勉強したほうがいい」という助言を表し、A よりやわらかい言い方になる。"),
    ("I had to clean my room.", "I must clean my room.",
     "A は had to で「部屋をそうじしなければならなかった」という過去の義務を表す。B は must で「（今・これから）部屋をそうじしなければならない」という現在の義務を表す。must には過去形がないので、過去の義務は had to で表す。"),
]


@gen("thinking_writing", 3, ["written_reasoning", "concept"])
def explain_difference(r):
    a, b, model = r.choice(PAIRS)
    return desc(f"次の2つの英文 A・B の意味の違いを、使われている語句の働きに注目して日本語で説明しなさい。\nA：{a}\nB：{b}", model,
                "似た形でも、接続詞・助動詞・主語の選び方によって、伝わる内容（禁止か不要か、条件か時か、初めて伝えるか特定のものか）が変わる。",
                [("A の意味を、働きのわかる語句にふれて説明している", 3), ("B の意味を、働きのわかる語句にふれて説明している", 3), ("2文の違いをはっきり対比している", 2)], d=3, p=8, lines=5,
                ap="2つの文で違う語句に印をつけ、それぞれの語句がどんな意味を加えるのかを考える。",
                steps=["A と B で違う部分を見つける。", "それぞれの語句の働き（禁止・不要・条件・時・存在・場所・義務・助言など）を確かめる。", "和訳を示して違いを対比する。"],
                alt=["それぞれの文が自然に使われる場面を1つずつ考えて、場面の違いから説明する。"],
                pc=[("A の説明", 3), ("B の説明", 3), ("違いの対比", 2)],
                pit=["和訳だけを書き、どの語句が違いを生んでいるかを書かない。", "must not と don't have to を同じ意味だと考える。"])


RULES = [
    ("図書館", "In the library, you must not talk loudly. You don't have to bring your own books. You should return books on time.",
     "must not で禁止、don't have to で不要、should で助言を表している。"),
    ("プール", "At the pool, you must not run. You must take a shower before swimming. You should drink water after swimming.",
     "must not で禁止、must で義務、should で助言を表している。"),
    ("修学旅行", "On the school trip, you must come back to the hotel by six. You don't have to bring much money. You should take a lot of pictures.",
     "must で義務、don't have to で不要、should で助言を表している。"),
    ("音楽室", "In the music room, you must not eat or drink. You don't have to bring your own instrument. You should practice before class.",
     "must not で禁止、don't have to で不要、should で助言を表している。"),
    ("キャンプ", "At the camp, you must follow your leader. You don't have to bring a tent. You should bring a warm jacket.",
     "must で義務、don't have to で不要、should で助言を表している。"),
]


@gen("thinking_writing", 2, ["application", "written_reasoning"])
def write_rules(r):
    place, model, point = r.choice(RULES)
    return desc(f"日本に来たばかりの留学生に、「{place}」でのきまりや注意を英語で3文伝えなさい。ただし、must / must not のどちらかを1回以上、don't have to と should をそれぞれ1回以上使い、3文の内容がそれぞれ違うようにすること。",
                f"（解答例）{model}", f"（解答例の解説）{point} どの表現も後ろは動詞の原形。",
                [("must / must not を意味に合わせて正しく使っている", 2), ("don't have to を「不要」の意味で正しく使っている", 2), ("should を助言として正しく使っている", 2), ("場面に合った内容で、つづり・語順が正しい", 2)], d=4, p=8, lines=5,
                ap="場面で「してはいけないこと」「しなくてよいこと」「したほうがよいこと」を日本語で1つずつ考えてから英語にする。",
                steps=["場面のきまりを日本語で3つ考え、禁止・義務・不要・助言に分類する。", "それぞれに合う表現（must not / must / don't have to / should）を選ぶ。", "表現の後ろに動詞の原形を置いて英文にする。", "3文の内容と表現が条件を満たしているかを見直す。"],
                alt=["書いた must not の文を don't have to に入れかえると意味がどう変わるかを考え、選んだ表現が正しいかを確かめる。"],
                pc=[("must / must not", 2), ("don't have to", 2), ("should", 2), ("内容と表記", 2)],
                pit=["don't have to を「～してはいけない」の意味で使う。", "must to ～ や should to ～ のように to を入れる。"])


TOWNS = [
    ("みどり町", [("公園", "park", 3), ("図書館", "library", 1), ("駅", "station", 2), ("映画館", "movie theater", 0)]),
    ("さくら町", [("学校", "school", 4), ("病院", "hospital", 1), ("スーパーマーケット", "supermarket", 2), ("動物園", "zoo", 0)]),
    ("あおば町", [("神社", "shrine", 2), ("博物館", "museum", 1), ("コンビニエンスストア", "convenience store", 5), ("空港", "airport", 0)]),
    ("ひかり町", [("橋", "bridge", 3), ("城", "castle", 1), ("ホテル", "hotel", 2), ("遊園地", "amusement park", 0)]),
]
NUMW = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five"}


def plural(w):
    if w.endswith("y") and w[-2] not in "aeiou":
        return w[:-1] + "ies"
    if w.endswith(("s", "sh", "ch", "x")):
        return w + "es"
    return w + "s"


@gen("thinking_writing", 3, ["written_reasoning", "condition_check"])
def describe_town(r):
    name, rows = r.choice(TOWNS)
    rows = list(rows)
    r.shuffle(rows)
    lines = []
    for jp, en, n in rows:
        if n == 0:
            lines.append(f"There is no {en} in this town.")
        elif n == 1:
            lines.append(f"There is a{'n' if en[0] in 'aeiou' else ''} {en} in this town.")
        else:
            lines.append(f"There are {NUMW[n]} {plural(en)} in this town.")
    model = " ".join(lines)
    tbl = table([(jp, f"{n}") for jp, _, n in rows], header=["施設", "数"], caption=f"{name}の施設（架空の資料）")
    words = "、".join(f"{jp}＝{en}" for jp, en, _ in rows)
    return desc(f"次の表は、架空の町「{name}」にある施設の数をまとめたものである。表の内容を、There is / are を使って4文の英語で説明しなさい（数が 0 のものは「ない」ことを表すこと）。また、1つの文について is と are のどちらを選んだか、その理由を日本語で説明しなさい。\n（語句：{words}）",
                f"（解答例）{model}　理由の例：{rows[0][1]} が{'1つなので単数扱いで is' if rows[0][2] == 1 else ('2つ以上あって複数なので are' if rows[0][2] > 1 else '0 なので There is no ～（または There aren\'t any ～s）で「ない」ことを表す')}を使った。",
                "There is / are の be 動詞は、後ろの名詞の数で決まる。複数のときは名詞も複数形にする。数が 0 のときは There is no ～. や There isn't a ～. / There aren't any ～. で表す。",
                [("4つの施設をすべて There is / are で正しく表している", 4), ("複数形・数の言い方が正しい", 2), ("is / are を選んだ理由を名詞の数から説明している", 2)], d=4, p=8, lines=6, tbl=tbl,
                ap="表の数が 1 か、2 以上か、0 かで、There is / There are / There is no（isn't / aren't any）を使い分ける。",
                steps=["表の数を見て、施設ごとに単数・複数・0 に分ける。", "単数は There is a(n) ～、複数は There are＋数＋複数形 で書く。", "0 のものは There is no ～. などで「ない」ことを表す。", "1つの文を選び、is / are の理由を名詞の数から説明する。"],
                alt=["書いた文を Is there a ～? / How many ～ are there? の質問に答える形で読み直し、表の数と合っているかを確かめる。"],
                pc=[("4文の正しさ", 4), ("複数形と数", 2), ("理由の説明", 2)],
                pit=["2つ以上なのに名詞を単数形のままにする（two park）。", "数が 0 のものを There are zero ～ と書いて不自然になる。"])


OPINION = [
    ("夏と冬では、夏のほうが好きだ", "I think that summer is better than winter. There are many fun things to do, like swimming in the sea.",
     "I think that ～ で意見を述べ、There are many fun things to do で理由を、形容詞的用法の不定詞 to do を使って説明している。"),
    ("中学生は毎日本を読んだほうがいい", "I think that students should read books every day because there are many things to learn from books.",
     "I think that ～ と should で意見、because と There are many things to learn で理由を述べている。"),
    ("自分の町は住みやすい", "I think that my town is a good place to live because there are many parks to enjoy.",
     "I think that ～ で意見、because と There are many parks to enjoy で理由を述べている。to live / to enjoy は形容詞的用法。"),
    ("修学旅行は京都がよい", "I think that we should go to Kyoto on our school trip because there are many old temples to visit.",
     "I think that ～ と should で意見、because と There are many old temples to visit で理由を述べている。"),
    ("放課後に図書館を使うのはよい", "I think that the library is a good place to study after school because there are a lot of books to read there.",
     "I think that ～ で意見、because と There are a lot of books to read で理由を述べている。"),
]


@gen("thinking_writing", 2, ["cross_unit", "written_reasoning"], rel=["JH-ENG-G2-U02"])
def write_opinion(r):
    topic, model, point = r.choice(OPINION)
    return desc(f"「{topic}」という意見を、英語で書きなさい。ただし、I think that ～ を使い、さらに There is / are と〈名詞＋to＋動詞の原形〉（形容詞的用法の不定詞）を使って理由も述べること（1文でも2文でもよい）。",
                f"（解答例）{model}", f"（解答例の解説）{point}",
                [("I think that＋主語＋動詞 で意見を述べている", 3), ("There is / are と〈名詞＋to＋原形〉を正しく使って理由を述べている", 3), ("意見と理由のつながりが自然で、つづり・語順が正しい", 2)], d=4, p=8, lines=4,
                ap="前の単元の不定詞（名詞の後ろに to＋原形を置いて「～するための」）と、この単元の I think that ～ / There are ～ / because を組み合わせる。",
                steps=["意見を I think that ～. で書く。", "理由になる「～するための…がたくさんある」を There are many＋名詞＋to＋原形 で表す。", "because でつなぐか、2文目として続ける。", "be 動詞の数と to の後ろの原形を見直す。"],
                alt=["理由の文から to ～ の部分を取り除いて、名詞だけでも文が成り立つか（There are many parks.）を確かめると、形容詞的用法として正しく後ろに置けているかがわかる。"],
                pc=[("意見の文", 3), ("理由の文（There is / are＋名詞＋to ～）", 3), ("つながりと表記", 2)],
                pit=["There is many places ～ のように be 動詞の数を誤る。", "many to visit places のように to ～ を名詞の前に置く。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(task, wrong, step, etype, tempt, fix, expl, steps, ap, alt, pit):
    return desc(f"{task}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい英文に書き直しなさい。", fix, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい英文に直している", 3), ("文法のルールを説明している", 1)], d=3, p=6, lines=4,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい英文", 3), ("ルールの説明", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix))


CONJ_ERR = [
    ("もし明日晴れたら、私は泳ぎに行くつもりだ。", "If it will be sunny tomorrow, I will go swimming.", "If it is sunny tomorrow, I will go swimming.", "will be", "condition",
     "if のまとまりの中では、未来のことでも現在形を使う。will be を is にする。", "「明日」があるので未来の will が必要だと考えた。"),
    ("ケンが来たら、出発しましょう。", "When Ken will come, let's start.", "When Ken comes, let's start.", "will come", "condition",
     "when のまとまりの中では、未来のことでも現在形を使う。主語が三人称単数なので comes。", "これから先のことなので will が必要だと考えた。"),
    ("私はかぜをひいていたので、学校を休んだ。", "Because I had a cold. I didn't go to school.", "I didn't go to school because I had a cold.", "Because I had a cold.", "notation",
     "because のまとまりだけでは文として独立できない（Why ～? の答えの場合を除く）。1つの文にまとめる。", "日本語の「～ので。」で文を切ってしまった。"),
    ("宿題が終わったので、私はテレビを見た。", "I finished my homework because I watched TV.", "I watched TV because I finished my homework.", "because の位置", "logic",
     "because は理由の前に置く。理由は「宿題が終わった」なので、because I finished my homework とする。", "日本語の語順のまま、最初の文の後ろに because をつけた。"),
    ("私は、その映画はおもしろいと思う。", "I think that the movie interesting.", "I think that the movie is interesting.", "the movie interesting", "concept",
     "that の後ろには〈主語＋動詞〉が必要。動詞 is を入れる。", "think の後ろに名詞と形容詞を並べるだけでよいと考えた。"),
    ("駅に着いたとき、雨が降っていた。", "When I got to the station it was raining.", "When I got to the station, it was raining.", "station と it の間", "notation",
     "when のまとまりを文の前半に置くときは、まとまりの終わりにカンマをつける。", "日本語では読点を省いても意味が通じるので、カンマを忘れた。"),
]


@gen("error_correction", 4, ["common_error", "condition_check"])
def err_conj(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(CONJ_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", etype, tempt, fix, f"{rule}正しくは {fix}",
                    ["接続詞のまとまりと主節の〈主語＋動詞〉をそれぞれ確認する。", f"「{where}」の部分の誤りを見つける：{rule}", f"正しい英文：{fix}"],
                    "接続詞の文は、①2組の〈主語＋動詞〉がそろっているか、②when / if の中の時制、③理由・時の向き、④カンマ、の順に確かめる。",
                    ["直した文を日本語に訳し直し、時・条件・理由の関係が問題の日本語と一致するかを確かめる。"],
                    ["when / if の中に will を入れる。", "because のまとまりだけで文を終える。"])


THERE_ERR = [
    ("私の家の近くには公園が2つある。", "There is two parks near my house.", "There are two parks near my house.", "is", "condition",
     "two parks は複数なので be 動詞は are。", "There is ～ をひとまとまりで覚えていて、名詞の数を見なかった。"),
    ("箱の中にはリンゴがいくつかあった。", "There was some apples in the box.", "There were some apples in the box.", "was", "condition",
     "some apples は複数なので、過去形は were。", "some を「1つのまとまり」と考えて単数にした。"),
    ("この近くに駅はありますか。― はい、あります。", "Is there a station near here? ― Yes, it is.", "Is there a station near here? ― Yes, there is.", "it is", "concept",
     "Is there ～? の疑問文には there を使って答える。", "Is ～? の答えは it is だと考えた。"),
    ("あなたのかばんは机の上にあります。", "There is your bag on the desk.", "Your bag is on the desk.", "There is your bag", "concept",
     "your bag のように相手もわかっている特定のものの場所を言うときは There is を使わず、Your bag is ～. とする。", "日本語の「～がある」はいつも There is で表せると考えた。"),
    ("あなたのクラスには何人の生徒がいますか。", "How many student are there in your class?", "How many students are there in your class?", "student", "notation",
     "How many の後ろの名詞は複数形にする。", "1人ずつ数えるイメージで単数形にした。"),
    ("冷蔵庫に牛乳はありません。", "There aren't any milks in the fridge.", "There isn't any milk in the fridge.", "aren't any milks", "concept",
     "milk は数えられない名詞なので複数形にせず、be 動詞は is を使う。", "「牛乳」をたくさんあるものと考えて複数扱いにした。"),
]


@gen("error_correction", 3, ["common_error", "computation"])
def err_there(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(THERE_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", etype, tempt, fix, f"{rule}正しくは {fix}",
                    ["be 動詞の後ろの名詞の数（単数・複数・数えられない）を確認する。", f"「{where}」の部分の誤りを見つける：{rule}", f"正しい英文：{fix}"],
                    "There is / are の文では、①後ろの名詞の数、②時制、③答え方（there を使う）、④特定のものには使わない、を確かめる。",
                    ["直した文の be 動詞の後ろの名詞を主語にした文（Two parks are near my house.）を作ってみて、be 動詞の数が合っているかを確かめる。"],
                    ["複数の名詞に is / was を使う。", "特定のもの（my bag, the book）に There is を使う。"])


MODAL_ERR = [
    ("私たちは毎日教室をそうじしなければならない。", "We must to clean our classroom every day.", "We must clean our classroom every day.", "must to", "concept",
     "must は助動詞なので、直後に動詞の原形を置く。to は不要。", "have to と同じように to をつけた。"),
    ("私の姉は今日、早く帰宅しなければならない。", "My sister have to come home early today.", "My sister has to come home early today.", "have to", "condition",
     "主語 My sister は三人称単数なので has to にする。", "have to をひとまとまりの表現と考え、変化させなかった。"),
    ("明日は休みなので、早起きする必要はない。", "We have a holiday tomorrow, so we must not get up early.", "We have a holiday tomorrow, so we don't have to get up early.", "must not", "interpretation",
     "must not は「～してはいけない」（禁止）。「～する必要はない」（不要）は don't have to で表す。", "must（しなければならない）に not をつければ「しなくてよい」になると考えた。"),
    ("ケンは昨日、宿題をしなければならなかった。", "Ken musted do his homework yesterday.", "Ken had to do his homework yesterday.", "musted", "notation",
     "must には過去形がない。過去の義務は had to で表す。", "一般動詞と同じように ed をつければ過去形になると考えた。"),
    ("彼はその本を買う必要はない。", "He doesn't has to buy the book.", "He doesn't have to buy the book.", "doesn't has", "concept",
     "doesn't の後ろは原形なので has ではなく have。", "主語が三人称単数なので has を残した。"),
    ("あなたは先生に聞いたほうがいい。", "You should asked your teacher.", "You should ask your teacher.", "should asked", "concept",
     "should は助動詞なので、後ろは動詞の原形。", "過去のことのように感じて過去形にした。"),
]


@gen("error_correction", 3, ["common_error", "concept"])
def err_modal(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(MODAL_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", etype, tempt, fix, f"{rule}正しくは {fix}",
                    ["日本語が義務・禁止・不要・助言のどれかを確認する。", f"「{where}」の部分の誤りを見つける：{rule}", f"正しい英文：{fix}"],
                    "must / should は形が変わらない助動詞（後ろは原形）、have to は主語・時制で has to / had to に変わる。禁止と不要を取り違えない。",
                    ["直した文を日本語に訳し直して、「してはいけない」「しなくてよい」などの意味が問題の日本語と一致するかを確かめる。"],
                    ["must の後ろに to を入れる。", "must not を「しなくてよい」の意味で使う。"])


GENERATORS = [conj_choice, there_be, modal_meaning, if_tense, there_qa,
              have_to_rewrite, there_rewrite, build_order, combine, think_will,
              explain_difference, write_rules, describe_town, write_opinion,
              err_conj, err_there, err_modal]
