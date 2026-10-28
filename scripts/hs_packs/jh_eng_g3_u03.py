"""単元パック：中学3年 英語 関係代名詞。"""
from banks._common import desc, mc, order, sa
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem,
                         tp)

UNIT_ID = "JH-ENG-G3-U03"

PREREQUISITES = [
    ("JH-ENG-G3-U02", "分詞の後置修飾と接触節（the book I read）。「名詞を後ろから説明する」という語順の考え方を、関係代名詞でさらに広げる。"),
    ("JH-ENG-G1-U02", "人称代名詞の格（he / him、it / they）。2つの文をつなぐとき、どの代名詞を関係代名詞にかえるかを判断する土台。"),
    ("JH-ENG-G1-U01", "三人称単数現在の s。主格の関係代名詞の後ろの動詞は、先行詞が単数か複数かで形が変わる。"),
    ("JH-ENG-G2-U03", "接続詞 that（I think that ～）。関係代名詞の that と形が同じなので、働きを見分ける必要がある。"),
]
EXTENSIONS = [
    ("JH-ENG-G3-U06", "長文の中の長い主語（The man who ～ is …）や説明文の定義（A ～ is a … which ―）を正確に読み取る力になる。"),
    ("JH-ENG-G3-U07", "条件英作文で、人や物を1文でくわしく説明するときに関係代名詞を使う。"),
    ("HS-ENG-U05", "高校では、whose・what・関係副詞（where / when）、前置詞＋関係代名詞、コンマのついた非制限用法へと発展する。"),
]


def cap(s):
    return s[0].upper() + s[1:]


# ======================================================================
# 授業プリント
# ======================================================================

LESSON = lesson(
    goals=["主格の関係代名詞（who / which / that）を使って、「～する（人・物）」と名詞を後ろから説明できる。",
           "目的格の関係代名詞（which / that、省略も可）を使って、「…が～する（人・物）」と名詞を後ろから説明できる。",
           "先行詞が人か物か、関係代名詞が主格か目的格かを判断して、2つの文を1つにつなげられる。"],
    duration=50,
    readiness=["分詞の後置修飾・接触節で、名詞を後ろから説明する語順を理解している（中3）。",
               "人称代名詞の主格・目的格（he / him、she / her、it、they / them）を区別できる（中1）。",
               "主語が三人称単数のとき、現在形の動詞に s がつくことを理解している（中1）。",
               "小学校の国語で、「赤い帽子をかぶった男の子」のように、名詞をくわしくする言葉（修飾語）を学んでいる。"],
    flow=[("導入：日本語と英語の説明の順番", 5, "「ピアノをひく少女」を英語にするとき、説明が名詞の後ろにくることを確認する"),
          ("主格の関係代名詞", 12, "who（人）/ which（物）/ that（どちらも）＋動詞。2文を1文にする手順（例題1）"),
          ("目的格の関係代名詞", 12, "which / that＋主語＋動詞。省略できること（例題2）"),
          ("長い主語の文を読む", 13, "The boy who ～ is …. の文の動詞を見つける。関係代名詞の that と接続詞の that（例題3）"),
          ("まとめと確認", 8, "板書の3列で整理し、確認問題3問")],
    sections=[
        intro("in1", "名詞を後ろから説明する「長い説明」",
              "日本語では「ピアノをひいている少女」「私が昨日読んだ本」のように、説明はいつも名詞の前に置きます。英語では、2語以上の長い説明は名詞の後ろに置くのが基本です。前の単元では分詞や〈主語＋動詞〉（接触節）で名詞を後ろから説明しました。この単元では、who / which / that という「つなぎの語」（関係代名詞）を使って、名詞の後ろに〈動詞を含む説明〉をつける方法を学びます。",
              bullets=["a girl playing the piano（ピアノをひいている少女：分詞）",
                       "a girl who plays the piano（ピアノをひく少女：関係代名詞）",
                       "the book I read yesterday（私が昨日読んだ本：接触節）",
                       "the book which I read yesterday（同じ意味：関係代名詞）"],
              points=[tp("黒板に日本語「ピアノをひく少女」と英語 a girl who plays the piano を上下に並べ、矢印で「説明の向き」が逆になることを見せる。",
                         ask="日本語と英語で、「少女」はそれぞれどこにあるか。", expect="日本語は最後、英語は最初。",
                         timing="導入の冒頭")]),
        definition("df1", "主格の関係代名詞 who / which / that",
                   "説明される名詞を先行詞といいます。関係代名詞の後ろにすぐ動詞が続き、関係代名詞が説明の中で主語の働きをするものを主格の関係代名詞といいます。",
                   formula="先行詞（人）＋ who / that ＋動詞 ～　｜　先行詞（物・動物）＋ which / that ＋動詞 ～",
                   bullets=["I have a friend who lives in Canada.（私にはカナダに住んでいる友だちがいる）",
                            "This is the bus which goes to the airport.（これは空港へ行くバスです）",
                            "The girl that is singing on the stage is my sister.（舞台で歌っている少女は私の姉です）"],
                   conditions=["先行詞が人なら who（that も可）、物・動物なら which（that も可）。",
                               "関係代名詞の後ろの動詞は、先行詞に合わせる：a friend who lives ／ two friends who live。",
                               "関係代名詞の説明の中に、もとの主語（he / it など）をもう一度書かない。"],
                   points=[tp("「who の後ろの動詞の s」は、主語 I ではなく先行詞 a friend に合わせることを、単数・複数の例で比べさせる。",
                              ask="I have two friends who (live / lives) in Canada. はどちらか。", expect="先行詞が two friends（複数）なので live。",
                              caution="文の主語 I につられて live、先行詞を見ずに lives とする誤りが多い。", timing="定義の説明後")]),
        definition("df2", "目的格の関係代名詞 which / that（省略できる）",
                   "関係代名詞の後ろに〈主語＋動詞〉が続き、関係代名詞が説明の中で目的語の働きをするものを目的格の関係代名詞といいます。目的格の関係代名詞は省略でき、省略すると前の単元の接触節と同じ形になります。",
                   formula="先行詞（物）＋ which / that ＋主語＋動詞　｜　先行詞（人）＋ that ＋主語＋動詞（省略可）",
                   bullets=["This is the picture which I took in Okinawa.（これは私が沖縄でとった写真です）",
                            "The man that we met at the station was Mr. Brown.（私たちが駅で会った男性はブラウンさんだった）",
                            "This is the picture I took in Okinawa.（which を省略した形）"],
                   conditions=["目的格では、関係代名詞の後ろの動詞の目的語（it / him など）を書かない：× the picture which I took it。",
                               "先行詞が人の目的格は、中学校では that を使うことが多い（who も使われる）。",
                               "主格の関係代名詞は省略できない：× a friend lives in Canada（文の動詞が2つになってしまう）。"],
                   points=[tp("省略できるのは目的格だけ。「関係代名詞の後ろに主語があるか」を見る習慣をつけさせる。",
                              ask="the bus which goes to the airport の which を省略できるか。", expect="できない。which の後ろにすぐ動詞 goes がある主格だから。")]),
        theorem("th1", "関係代名詞の選び方",
                "先行詞が人か物か × 説明の中で主語か目的語か → who / which / that を選ぶ",
                ["人・主格：who / that（I know a boy who can swim fast.）",
                 "物・主格：which / that（I have a cat which has blue eyes.）",
                 "人・目的格：that（who も可）、または省略（the man that I met）",
                 "物・目的格：which / that、または省略（the book which I read）",
                 "that は人にも物にも、主格にも目的格にも使える。"],
                body="迷ったら、まず先行詞を見つけて「人か物か」、次に関係代名詞の直後を見て「動詞か、主語＋動詞か」を確かめます。",
                points=[tp("2×2 の表（人／物 × 主格／目的格）を板書し、例文を生徒に分類させる。that が全部のマスに入ることを最後に確認する。", timing="定理の説明時")]),
        derivation("dv1", "2つの文から関係代名詞の文ができるしくみ",
                   ["① 2つの文の中で、同じ人・物を指す語を見つける。I know a boy. ＋ He can speak French. では a boy と He。",
                    "② 2文目の代名詞を関係代名詞にかえる。He は人で主語なので who（主格）。",
                    "③ 関係代名詞を、説明したい名詞（先行詞 a boy）のすぐ後ろに移す → I know a boy who can speak French.",
                    "④ 目的語の場合：This is the bag. ＋ I bought it last week. では it が the bag と同じ物で目的語 → which（目的格）にかえる。",
                    "⑤ which は「つなぎの語」なので文の前に出し、先行詞の直後に置く → This is the bag which I bought last week.（it はもう which になったので書かない）",
                    "⑥ 先行詞が主語の位置にあるとき：The cake was delicious. ＋ My mother made it. → The cake which my mother made was delicious.（説明が主語の後ろに入りこみ、文の動詞 was はその後ろに来る）"],
                   body="関係代名詞は「代名詞（he / it）」と「接続詞（2つの文をつなぐ）」の2つの役目を1語で果たしています。だから、もとの代名詞を残すと同じものを2回言うことになるのです。",
                   points=[tp("⑤で it を消し忘れる生徒が多い。「which が it の代わりになったから、it は1回分しか書けない」と、代名詞の置きかえとして説明する。",
                              ask="This is the bag which I bought it. はどこがおかしいか。", expect="which と it が同じ物を2回指している。",
                              caution="「関係代名詞を足す」のではなく「代名詞を関係代名詞にかえる」と説明する。", timing="導出の説明時")]),
        example("ex1", "例題1　主格の関係代名詞で2つの文をつなぐ",
                "関係代名詞を使って、2つの文を1つにしなさい。(1) I have an aunt. She teaches music.　(2) Look at the house. It stands on the hill.",
                ["(1) an aunt と She が同じ人。She は主語 → 人・主格なので who（that）。an aunt の直後に置く。",
                 "(2) the house と It が同じ物。It は主語 → 物・主格なので which（that）。the house の直後に置く。",
                 "どちらも、関係代名詞の後ろの動詞（teaches / stands）は先行詞（単数）に合わせて s がついたまま。"],
                "(1) I have an aunt who teaches music.　(2) Look at the house which stands on the hill.（どちらも that も可）",
                thinking="2文目の主語が代名詞（he / she / it / they）になっていたら、主格の関係代名詞にかえる。",
                points=[tp("答えを日本語に訳させ、「音楽を教えているおば」「丘の上に立っている家」と、説明が前に来る日本語になることを確認する。")],
                misconceptions=[("I have an aunt who she teaches music.", "who が she の代わりなので、she は書かない。")]),
        example("ex2", "例題2　目的格の関係代名詞と省略",
                "日本語に合うように英文を完成させなさい。(1) これは私の兄がくれた時計です。This is the watch (　　) my brother gave me.　(2) 私たちが公園で会った女の子はエミでした。The girl (　　) we met in the park was Emi.　(3) (2) の文で関係代名詞を省略した文を書きなさい。",
                ["(1) the watch（物）の後ろに my brother gave（主語＋動詞）が続く → 物・目的格の which（that）。",
                 "(2) The girl（人）の後ろに we met（主語＋動詞）が続く → 人・目的格の that（who も可）。",
                 "(3) 目的格は省略できる。The girl we met in the park was Emi.（文の動詞は was）"],
                "(1) which（that）　(2) that（who）　(3) The girl we met in the park was Emi.",
                thinking="関係代名詞の後ろに〈主語＋動詞〉があり、その動詞の目的語が欠けていれば目的格。",
                points=[tp("(2) の文全体の動詞が was であることを確認し、「説明のかたまり」を（　）でくくらせる。",
                           ask="(2) で「女の子は」に対応する動詞はどれか。", expect="met ではなく was。")],
                misconceptions=[("This is the watch which my brother gave me it.", "which が it の代わり。it は書かない。")]),
        example("ex3", "例題3　長い主語の文を読む・that の働きを見分ける",
                "(1) 次の英文を日本語に訳しなさい。The boy who is talking with Ms. Green is my cousin.　(2) 次の2文の that の働きの違いを説明しなさい。A: I think that this book is interesting.　B: This is the book that I bought yesterday.",
                ["(1) The boy の後ろの who is talking with Ms. Green が説明のかたまり。そのあとの is が文の動詞。",
                 "(1) 「グリーン先生と話している少年は私のいとこです」。",
                 "(2) A の that は think の後ろで「～ということ」と文をつなぐ接続詞（that 以下に主語・目的語がそろっている）。",
                 "(2) B の that は the book を説明する目的格の関係代名詞（bought の目的語が欠けている）。"],
                "(1) グリーン先生と話している少年は、私のいとこです。　(2) A は接続詞（～ということ）、B は関係代名詞（the book を説明）。",
                thinking="関係代名詞の後ろの文は、必ず主語か目的語が1つ欠けている。欠けていなければ接続詞の that。",
                points=[tp("(2) は「that の後ろだけで文が完成しているか」を確かめさせる。A は this book is interesting で完成、B は I bought だけで目的語がない。",
                           ask="B の that の後ろ I bought yesterday に足りないものは？", expect="bought の目的語（何を買ったか）。")]),
        board("bd1", "板書案",
              [("① 主格（＋動詞）", ["人：a friend who lives in Canada", "物：the bus which goes to the airport", "that はどちらにも使える",
                                    "動詞は先行詞に合わせる", "a friend who lives／two friends who live", "省略できない"]),
               ("② 目的格（＋主語＋動詞）", ["物：the picture which I took", "人：the man that we met", "目的語を書かない", "× which I took it",
                                        "省略できる", "the picture I took"]),
               ("③ 文の動詞を見つける", ["The boy [who is talking with Ms. Green] is my cousin.", "［ ］が説明のかたまり", "文の動詞は［ ］の後ろ",
                                     "関係代名詞の that：後ろが欠けている", "接続詞の that：後ろが完全な文"])],
              points=[tp("③の列では、説明のかたまりを［ ］でくくり、文の主語と動詞に下線を引く作業を全員で行う。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("文法用語（主格・目的格）を覚えることより、「関係代名詞の直後が動詞か、主語＋動詞か」で見分けられることを重視する。", timing="授業全体"),
               tp("クイズ形式（Who am I? / What is this?）で、It is an animal which has a long nose. のように定義文を作らせると、主格の練習が楽しくできる。",
                  ask="What is this? It is a thing which we use when it rains.", expect="An umbrella."),
               tp("長い主語の文は音読のときに「説明のかたまり」の前後で区切らせる（The boy / who is talking with Ms. Green / is my cousin.）。"),
               tp("目的格の人の先行詞は、教科書によって that を中心に扱う。who を使っても誤りではないことを伝え、答え合わせで混乱させない。",
                  caution="whom は中学校では扱わないことが多い。質問が出たら「目的格の who の、かたい言い方」と軽く触れる程度にする。"),
               tp("問題プリント D の誤答例は「who / which の取り違え」「代名詞の重複」「動詞の形（先行詞との一致・文の動詞）」の3種類にまとめて振り返らせる。")],
              misconceptions=[("I have a dog who has long ears.", "先行詞が動物なので which（that）。"),
                              ("This is the book which I read it yesterday.", "which が it の代わり。it は書かない。"),
                              ("I have a friend who live in Canada.", "先行詞 a friend は単数なので lives。"),
                              ("The boy who is talking with Ms. Green my cousin.", "文の動詞 is が抜けている。説明のかたまりのあとに文の動詞を置く。")]),
        summary("sm1", "まとめ",
                ["関係代名詞は、名詞（先行詞）の後ろに〈動詞を含む説明〉をつける「つなぎの語」。説明は先行詞のすぐ後ろに置く。",
                 "主格：先行詞＋who（人）/ which（物）/ that＋動詞。動詞の形は先行詞に合わせる。省略できない。",
                 "目的格：先行詞＋which / that＋主語＋動詞。もとの目的語は書かない。省略できる。",
                 "長い主語の文は、説明のかたまりのあとにある文の動詞を見つけて読む。"]),
        check("ck1", "確認問題",
              [("I know a girl (　　) can speak three languages. の（　）に who と which のどちらが入るか。", "who（先行詞 a girl が人で、後ろに動詞 can speak が続く主格）"),
               ("This is the cake which I made it. の誤りを直しなさい。", "This is the cake which I made.（which が it の代わりなので it を消す）"),
               ("The bag that my father bought is blue. から、関係代名詞を省略しなさい。", "The bag my father bought is blue.（目的格なので省略できる）")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

# (空所つき英文, 先行詞の種類 "p"=人 / "t"=物・動物, 先行詞, 和訳)
SUBJ = [
    ("I have a friend (　　) lives in Canada.", "p", "a friend", "私にはカナダに住んでいる友だちがいる。"),
    ("Mr. Tanaka is a teacher (　　) teaches science at our school.", "p", "a teacher", "田中先生は私たちの学校で理科を教えている先生です。"),
    ("I know a boy (　　) can play the violin very well.", "p", "a boy", "私はバイオリンをとても上手にひける少年を知っている。"),
    ("The woman (　　) helped me at the station was very kind.", "p", "The woman", "駅で私を手伝ってくれた女性はとても親切だった。"),
    ("We need someone (　　) can speak Chinese.", "p", "someone", "私たちは中国語を話せる人が必要だ。"),
    ("She is the student (　　) won the speech contest.", "p", "the student", "彼女はスピーチコンテストで優勝した生徒です。"),
    ("He has an uncle (　　) works at a hospital.", "p", "an uncle", "彼には病院で働いているおじがいる。"),
    ("The children (　　) are playing in the park look happy.", "p", "The children", "公園で遊んでいる子どもたちは楽しそうだ。"),
    ("This is the bus (　　) goes to the airport.", "t", "the bus", "これは空港へ行くバスです。"),
    ("I have a dog (　　) has long ears.", "t", "a dog", "私は耳の長い犬を飼っている。"),
    ("The book (　　) is on the desk is mine.", "t", "The book", "机の上にある本は私のものです。"),
    ("Kyoto is a city (　　) has many old temples.", "t", "a city", "京都は古い寺がたくさんある都市です。"),
    ("I bought a watch (　　) was made in Switzerland.", "t", "a watch", "私はスイスで作られた腕時計を買った。"),
    ("Look at the house (　　) stands on the hill.", "t", "the house", "丘の上に立っている家を見てごらん。"),
    ("This is a song (　　) makes everyone happy.", "t", "a song", "これはみんなを幸せにする歌です。"),
    ("Do you know the cat (　　) is sleeping under the car?", "t", "the cat", "車の下で眠っているねこを知っていますか。"),
]

# (空所つき英文, 種類, 先行詞, 和訳, 代名詞の目的格)
OBJ = [
    ("This is the picture (　　) I took in Okinawa.", "t", "the picture", "これは私が沖縄でとった写真です。", "it"),
    ("The bike (　　) my father bought for me is blue.", "t", "The bike", "父が私に買ってくれた自転車は青い。", "it"),
    ("The movie (　　) we saw yesterday was exciting.", "t", "The movie", "私たちが昨日見た映画はわくわくした。", "it"),
    ("Is this the umbrella (　　) you lost at the park?", "t", "the umbrella", "これはあなたが公園でなくしたかさですか。", "it"),
    ("The letter (　　) Ken wrote made me happy.", "t", "The letter", "ケンが書いた手紙は私を幸せにした。", "it"),
    ("The curry (　　) we ate in Osaka was very good.", "t", "The curry", "私たちが大阪で食べたカレーはとてもおいしかった。", "it"),
    ("Show me the photos (　　) you took during your trip.", "t", "the photos", "あなたが旅行中にとった写真を見せて。", "them"),
    ("The cookies (　　) my sister baked were sweet.", "t", "The cookies", "姉が焼いたクッキーは甘かった。", "them"),
    ("The man (　　) we met at the station was Mr. Brown.", "p", "The man", "私たちが駅で会った男性はブラウンさんだった。", "him"),
    ("She is a singer (　　) many young people like.", "p", "a singer", "彼女は多くの若者が好きな歌手です。", "her"),
    ("The boy (　　) I saw in the library is Ken.", "p", "The boy", "私が図書館で見かけた少年はケンです。", "him"),
    ("Ms. Sato is the teacher (　　) all the students respect.", "p", "the teacher", "佐藤先生は生徒全員が尊敬している先生です。", "her"),
    ("The girl (　　) you invited to the party is my cousin.", "p", "The girl", "あなたがパーティーに招待した女の子は私のいとこです。", "her"),
]

PRON_SUBJ = {"p": ["he", "she", "they"], "t": ["it", "they"]}


def _fill(s, w):
    return s.replace("(　　)", w)


@gen("basic_check", 4, ["computation", "condition_check"])
def choose_rel(r):
    if r.random() < 0.55:
        s, kind, ante, jp = r.choice(SUBJ)
        case = "主格"
        pron = r.choice(PRON_SUBJ[kind])
        ok = r.choice(["who", "that"]) if kind == "p" else r.choice(["which", "that"])
        mismatch = "which" if kind == "p" else "who"
        why = {mismatch: (f"先行詞 {ante} は{'人' if kind == 'p' else '物・動物'}なので {mismatch} は使えない。{'人には who' if kind == 'p' else '物・動物には which'}を使う。", "先行詞（人・物）による使い分け"),
               "what": ("what は先行詞をふくむ特別な関係代名詞（高校で学ぶ）で、先行詞の後ろには置けない。", "疑問詞 what との混同"),
               pron: (f"{pron} はふつうの代名詞で、2つの文をつなぐ働きがない。動詞が2つ並んで文が成り立たない。", "代名詞と関係代名詞の混同")}
    else:
        s, kind, ante, jp, objp = r.choice(OBJ)
        case = "目的格"
        ok = "that" if kind == "p" else r.choice(["which", "that"])
        mismatch = "which" if kind == "p" else "who"
        pron = objp
        why = {mismatch: (f"先行詞 {ante} は{'人' if kind == 'p' else '物'}なので {mismatch} は使えない。", "先行詞（人・物）による使い分け"),
               "what": ("what は先行詞をふくむ特別な関係代名詞（高校で学ぶ）で、先行詞の後ろには置けない。", "疑問詞 what との混同"),
               pron: (f"{pron} はふつうの代名詞で、2つの文をつなぐ働きがない。", "代名詞と関係代名詞の混同")}
    kind_jp = "人" if kind == "p" else "物・動物"
    return mc(f"日本語の意味になるように、（　）に入る語として最も適切なものを選びなさい。\n{jp}\n{s}", [ok] + list(why),
              f"先行詞 {ante} は{kind_jp}で、空所の後ろには{'動詞' if case == '主格' else '〈主語＋動詞〉'}が続く{case}。答えは {ok}。", d=1,
              ap="空所の直前の名詞（先行詞）が人か物かを確かめ、次に空所の直後が動詞か〈主語＋動詞〉かを見る。",
              steps=[f"先行詞は {ante}（{kind_jp}）。", f"空所の直後は{'動詞' if case == '主格' else '主語＋動詞'} → {case}。", f"{kind_jp}・{case}に使える関係代名詞は {ok}。"],
              alt=[f"2つの文に分けてみる：空所の部分を {('he / she / it / they' if case == '主格' else 'him / her / it / them')} に戻して文が成り立つかを確かめる。"],
              pc=[("先行詞が人か物かを判断している", 1), ("正しい関係代名詞を選んでいる", 1)],
              pit=["先行詞が動物のときに who を使う。", "関係代名詞の代わりに he / it などの代名詞を置く。"], why=why)


CASE_S = "主格の関係代名詞（後ろに動詞が続く）"
CASE_O = "目的格の関係代名詞（後ろに主語＋動詞が続く）"
CASE_Q = "疑問詞（「だれ」「どれ」とたずねる語）"
CASE_C = "接続詞（「～ということ」と文をつなぐ語）"


@gen("basic_check", 4, ["concept", "condition_check"])
def subj_or_obj(r):
    if r.random() < 0.5:
        s, kind, ante, jp = r.choice(SUBJ)
        w = r.choice(["who", "that"]) if kind == "p" else r.choice(["which", "that"])
        ok, wrongs = CASE_S, [CASE_O, CASE_Q, CASE_C]
        nxt = s.split("(　　)")[1].split()[0]
        hint = f"直後に動詞 {nxt} が続き、{w} が説明の中で主語の働きをしている"
    else:
        s, kind, ante, jp, objp = r.choice(OBJ)
        w = "that" if kind == "p" else r.choice(["which", "that"])
        ok, wrongs = CASE_O, [CASE_S, CASE_Q, CASE_C]
        after = s.split("(　　)")[1].split()
        hint = f"直後に〈主語＋動詞〉（{after[0]} {after[1]}）が続き、{w} が動詞の目的語の働きをしている"
    reasons = {CASE_S: "主格なら関係代名詞の直後に動詞が続く。この文では直後に主語がある。",
               CASE_O: "目的格なら関係代名詞の直後に〈主語＋動詞〉が続く。この文では直後がすぐ動詞になっている。",
               CASE_Q: "疑問詞なら「だれ」「どれ」とたずねる意味になるが、この文はたずねる文ではなく、前の名詞を説明している。",
               CASE_C: f"接続詞の that なら後ろに完全な文が続くが、この文の［{w}］の後ろは主語か目的語が1つ欠けている。"}
    why = {x: (reasons[x], "関係代名詞の格の見分け方") for x in wrongs}
    sent = s.replace("(　　)", f"［{w}］")
    return mc(f"次の英文の［　］の語の働きとして最も適切なものを選びなさい。\n{sent}", [ok] + wrongs,
              f"［{w}］は先行詞 {ante} を説明する関係代名詞で、{hint}。和訳：{jp}", d=2,
              ap="［　］の語の直後を見て、動詞が来ているか、〈主語＋動詞〉が来ているかを確かめる。",
              steps=[f"［{w}］の直前の名詞 {ante} が先行詞。", f"{hint}。", f"答え：{ok}"],
              alt=[f"文全体を訳して確かめる：{jp}"],
              pc=[("［　］の直後の形を確かめている", 1), ("働きを正しく選んでいる", 1)],
              pit=["that をすべて接続詞と考える。", "関係代名詞の直後の名詞を見落とし、主格と目的格を取り違える。"], why=why)


# (英文, 先行詞, [ほかの名詞])
ANTE = [
    ("The girl who is talking with my mother is Yumi.", "The girl", ["my mother", "Yumi", "who"]),
    ("I read a book which my teacher gave me.", "a book", ["my teacher", "me", "I"]),
    ("The dog that is running in the park belongs to Ken.", "The dog", ["the park", "Ken", "that"]),
    ("We visited a museum which has many old pictures.", "a museum", ["many old pictures", "We", "which"]),
    ("Tom is the boy who broke the window yesterday.", "the boy", ["Tom", "the window", "yesterday"]),
    ("The cake that my sister made for me was delicious.", "The cake", ["my sister", "me", "that"]),
    ("I have a cousin who lives in New York.", "a cousin", ["New York", "I", "who"]),
    ("The song which we sang at the festival is popular.", "The song", ["we", "the festival", "which"]),
    ("Do you know the man that is standing by the gate?", "the man", ["you", "the gate", "that"]),
    ("This is the camera which my grandfather used.", "the camera", ["This", "my grandfather", "which"]),
    ("The students who joined the event cleaned the beach.", "The students", ["the event", "the beach", "who"]),
    ("I like the pictures that Emi painted in Hawaii.", "the pictures", ["Emi", "Hawaii", "I"]),
    ("The teacher who taught us English came from Australia.", "The teacher", ["us", "English", "Australia"]),
]


@gen("basic_check", 4, ["concept", "computation"])
def find_antecedent(r):
    en, ante, others = r.choice(ANTE)
    why = {}
    for o in others:
        if o in ("who", "which", "that"):
            why[o] = (f"{o} は関係代名詞そのもの。先行詞は関係代名詞の直前にある、説明される名詞。", "先行詞と関係代名詞の混同")
        else:
            why[o] = (f"{o} は関係代名詞より後ろ（説明の中）または文の別の位置にある語で、関係代名詞が説明している名詞ではない。", "先行詞の位置")
    return mc(f"次の英文で、関係代名詞が説明している名詞（先行詞）を選びなさい。\n{en}", [ante] + others,
              f"関係代名詞の直前にある {ante} が先行詞。関係代名詞以下が {ante} を後ろから説明している。", d=1,
              ap="who / which / that を見つけ、そのすぐ前にある名詞を見る。",
              steps=["文の中の関係代名詞を見つける。", "そのすぐ前にある名詞が先行詞。", f"答え：{ante}"],
              alt=["関係代名詞以下の説明を先行詞の前に回して日本語に訳し、意味が通るかを確かめる。"],
              pc=[("関係代名詞の位置を確かめている", 1), ("先行詞を正しく選んでいる", 1)],
              pit=["関係代名詞の後ろにある名詞を先行詞と考える。", "文の主語をいつも先行詞だと思いこむ。"], why=why)


# (空所つき英文, 先行詞, 単数か, 単数形, 複数形, ing 形)
AGREE = [
    ("I have a friend who (　　) in Canada.", "a friend", True, "lives", "live", "living"),
    ("I have two cousins who (　　) in Hokkaido.", "two cousins", False, "live", "lives", "living"),
    ("This is the train which (　　) to Sendai.", "the train", True, "goes", "go", "going"),
    ("The students who (　　) the brass band practice every day.", "The students", False, "join", "joins", "joining"),
    ("The man who (　　) next to us is a doctor.", "The man", True, "lives", "live", "living"),
    ("I like stories which (　　) happy endings.", "stories", False, "have", "has", "having"),
    ("Tom has a sister who (　　) English at a high school.", "a sister", True, "teaches", "teach", "teaching"),
    ("We have a cat which (　　) fish very much.", "a cat", True, "likes", "like", "liking"),
    ("The buses which (　　) to the stadium are always crowded.", "The buses", False, "go", "goes", "going"),
    ("My uncle has a shop which (　　) old books.", "a shop", True, "sells", "sell", "selling"),
    ("The boy who (　　) talking with Ms. Green is Ken.", "The boy", True, "is", "are", "being"),
    ("The books which (　　) on the table are mine.", "The books", False, "are", "is", "being"),
    ("The girl who (　　) standing by the window is my classmate.", "The girl", True, "is", "are", "being"),
    ("I know some people who (　　) French.", "some people", False, "speak", "speaks", "speaking"),
]


@gen("basic_check", 4, ["condition_check", "common_error"])
def verb_agree(r):
    s, ante, sg, ok, other, ing = r.choice(AGREE)
    base = ok if not sg else other
    to_form = f"to {base if base not in ('is', 'are') else 'be'}"
    num_jp = "単数" if sg else "複数"
    why = {other: (f"先行詞 {ante} は{num_jp}。主格の関係代名詞の後ろの動詞は先行詞に合わせるので {ok} になる。", "先行詞と動詞の一致"),
           ing: (f"{ing} だけでは文の動詞にならない。関係代名詞の後ろには形の整った動詞が必要。", "ing 形と動詞の区別"),
           to_form: ("不定詞（to ～）は動詞の働きをしないので、関係代名詞の後ろの動詞として使えない。", "不定詞と動詞の区別")}
    return mc(f"（　）に入る語句として正しいものを選びなさい。\n{s}", [ok] + list(why),
              f"主格の関係代名詞の後ろの動詞は、先行詞 {ante}（{num_jp}）に合わせる。答えは {ok}。", d=2,
              ap="関係代名詞の後ろの動詞の主語は先行詞。先行詞が単数か複数かを確かめる。",
              steps=[f"関係代名詞の直前の先行詞は {ante}。", f"{ante} は{num_jp}。", f"現在の文なので、{num_jp}に合う形は {ok}。"],
              alt=[f"関係代名詞を先行詞に置きかえて文を作る（{ante} {ok} ～.）と、主語と動詞の形が合っているか確かめられる。"],
              pc=[("先行詞が単数か複数かを判断している", 1), ("正しい動詞の形を選んでいる", 1)],
              pit=["文の主語（I / We など）に合わせて動詞の形を決める。", "先行詞を見ずに、いつも s をつける。"], why=why)


@gen("basic_check", 4, ["condition_check", "concept"])
def omit_possible(r):
    o = r.choice(OBJ)
    subs = r.sample(SUBJ, 3)
    ok = _fill(o[0], "which" if o[1] == "t" else "that")
    wrongs = [_fill(s[0], "who" if s[1] == "p" else "which") for s in subs]
    why = {}
    for s, w in zip(subs, wrongs):
        nxt = s[0].split("(　　)")[1].split()[0]
        why[w] = (f"関係代名詞の直後に動詞 {nxt} が続く主格。主格を省略すると文の動詞が2つになり、文が成り立たない。", "主格の関係代名詞は省略できない")
    return mc("次の英文のうち、関係代名詞を省略しても正しい英文になるものを1つ選びなさい。", [ok] + wrongs,
              f"省略できるのは目的格の関係代名詞。{ok} は関係代名詞の後ろに〈主語＋動詞〉が続く目的格なので省略できる。", d=2,
              ap="それぞれの関係代名詞の直後を見て、〈主語＋動詞〉が続いている（目的格）ものを探す。",
              steps=["4つの文の関係代名詞の直後を確かめる。", "直後が動詞なら主格（省略できない）、主語＋動詞なら目的格（省略できる）。", f"答え：{ok}"],
              alt=["関係代名詞を消した文を読んでみて、名詞の後ろに〈主語＋動詞〉が続く接触節の形になっていれば正しい。"],
              pc=[("目的格だけが省略できることを理解している", 1), ("正しい文を選んでいる", 1)],
              pit=["主格の who / which も省略できると考える。", "that だけが省略できると思いこむ。"], why=why)


# ======================================================================
# B 標準演習
# ======================================================================

# (1文目, 2文目, 答え, 別解)
COMBINE = [
    ("I have a friend.", "She can play the guitar well.", "I have a friend who can play the guitar well.", ["I have a friend that can play the guitar well."]),
    ("This is the train.", "It goes to Tokyo.", "This is the train which goes to Tokyo.", ["This is the train that goes to Tokyo."]),
    ("I met a girl.", "She came from Australia.", "I met a girl who came from Australia.", ["I met a girl that came from Australia."]),
    ("The cake was delicious.", "My mother made it.", "The cake which my mother made was delicious.", ["The cake that my mother made was delicious.", "The cake my mother made was delicious."]),
    ("This is the camera.", "I bought it in Kyoto.", "This is the camera which I bought in Kyoto.", ["This is the camera that I bought in Kyoto.", "This is the camera I bought in Kyoto."]),
    ("The boy is my brother.", "He is swimming in the river.", "The boy who is swimming in the river is my brother.", ["The boy that is swimming in the river is my brother."]),
    ("The man was very kind.", "I asked him the way.", "The man that I asked the way was very kind.", ["The man who I asked the way was very kind.", "The man I asked the way was very kind."]),
    ("I have a dog.", "It has white legs.", "I have a dog which has white legs.", ["I have a dog that has white legs."]),
    ("The book is very popular.", "Mr. Smith wrote it.", "The book which Mr. Smith wrote is very popular.", ["The book that Mr. Smith wrote is very popular.", "The book Mr. Smith wrote is very popular."]),
    ("Do you know the woman?", "She is talking with Ken.", "Do you know the woman who is talking with Ken?", ["Do you know the woman that is talking with Ken?"]),
    ("These are the pictures.", "My father took them in Canada.", "These are the pictures which my father took in Canada.", ["These are the pictures that my father took in Canada.", "These are the pictures my father took in Canada."]),
    ("The students cleaned the park.", "They live in this town.", "The students who live in this town cleaned the park.", ["The students that live in this town cleaned the park."]),
    ("She is a singer.", "Everyone in Japan knows her.", "She is a singer that everyone in Japan knows.", ["She is a singer who everyone in Japan knows.", "She is a singer everyone in Japan knows."]),
    ("The bag is heavy.", "It is on the chair.", "The bag which is on the chair is heavy.", ["The bag that is on the chair is heavy."]),
]


@gen("standard_practice", 5, ["computation", "application"])
def combine(r):
    a, b, ans, vs = r.choice(COMBINE)
    return sa(f"関係代名詞を使って、次の2つの英文を1つの英文にしなさい。\n{a}\n{b}", ans,
              f"2文目の代名詞を関係代名詞にかえ、同じ人・物を指す1文目の名詞（先行詞）のすぐ後ろに説明として置く。答え：{ans}", d=2, p=4, v=vs,
              ap="2つの文で同じ人・物を指す語を見つけ、2文目のほうを関係代名詞にかえる。",
              steps=["1文目と2文目で同じ人・物を指す語（先行詞と代名詞）を見つける。",
                     "代名詞が主語なら主格、目的語なら目的格。先行詞が人か物かで who / which / that を決める。",
                     "関係代名詞を先行詞の直後に置き、2文目の残りを続ける（もとの代名詞は書かない）。",
                     f"答え：{ans}"],
              alt=["完成した文を日本語に訳し、2つの文の内容がすべて入っているかを確かめる。"],
              pc=[("正しい関係代名詞を選んでいる", 2), ("先行詞の直後に置き、語順が正しい（代名詞を重ねていない）", 2)],
              pit=["もとの代名詞（it / him）を残してしまう。", "先行詞が文の主語のとき、説明を文の最後に置いてしまう。"])


ORDERS = [
    ("私にはフランス語を話せるおじがいる。", ["I", "have", "an uncle", "who", "can speak", "French"], "an uncle の後ろに who can speak French"),
    ("これは京都へ行く電車です。", ["this", "is", "the train", "which", "goes", "to Kyoto"], "the train の後ろに which goes to Kyoto"),
    ("私が昨日読んだ本はおもしろかった。", ["the book", "which", "I", "read", "yesterday", "was", "interesting"], "主語 The book の後ろに説明 which I read yesterday、そのあと文の動詞 was"),
    ("向こうで走っている少年はケンです。", ["the boy", "who", "is running", "over there", "is", "Ken"], "主語 The boy の後ろに説明、そのあと文の動詞 is"),
    ("あれは私の父が建てた家です。", ["that is", "the house", "that", "my father", "built"], "the house の後ろに目的格の that my father built"),
    ("これは多くの人に愛されている歌ですか。", ["is", "this", "a song", "which", "many people", "love"], "a song の後ろに which many people love（目的格）"),
    ("私たちが駅で会った女性は先生でした。", ["the woman", "that", "we", "met", "at the station", "was", "a teacher"], "主語の後ろに that we met at the station、そのあと was"),
    ("彼は長い耳をした犬を飼っている。", ["he", "has", "a dog", "which", "has long ears"], "a dog の後ろに which has long ears（主格）"),
    ("あなたがとった写真を見せてください。", ["please", "show", "me", "the pictures", "you", "took"], "the pictures の後ろに you took（目的格の省略）"),
    ("英語を教えてくれた先生はカナダ出身です。", ["the teacher", "who", "taught", "us", "English", "is", "from Canada"], "主語 The teacher の後ろに who taught us English"),
    ("私には医者になりたい友だちがいる。", ["I", "have", "a friend", "who", "wants", "to be", "a doctor"], "a friend の後ろに who wants to be a doctor"),
    ("あなたが探しているかぎはこれですか。", ["is", "this", "the key", "that", "you", "are looking for"], "the key の後ろに that you are looking for（for の目的語が欠けている）"),
]


@gen("standard_practice", 4, ["application", "computation"])
def build_order(r):
    jp, parts, pat = r.choice(ORDERS)
    sent = cap(" ".join(parts)) + ("?" if jp.endswith("か。") else ".")
    return order(f"日本語の意味を表すように、次の語句を正しく並べかえなさい。文頭にくる語も小文字で示してある。\n{jp}", parts,
                 f"{sent}　ポイント：{pat}。", d=2, p=4,
                 ap="まず文の骨組み（主語＋動詞）を決め、説明される名詞（先行詞）のすぐ後ろに関係代名詞の説明のかたまりを置く。",
                 steps=["日本語から先行詞と、それを説明する部分を見つける。", "説明の部分を〈関係代名詞＋動詞〉または〈関係代名詞＋主語＋動詞〉の順に並べる。",
                        "説明のかたまりを先行詞の直後に置き、文の残りを続ける。", f"完成文：{sent}"],
                 alt=["説明のかたまりを［ ］でくくって取り除き、残った部分だけで文の骨組みが成り立つかを確かめる。"],
                 pc=[("説明のかたまりの語順が正しい", 2), ("かたまりを先行詞の直後に置き、文全体の語順が正しい", 2)],
                 pit=["日本語の語順につられて、説明を先行詞の前に置く。", "主語が長いとき、文の動詞を説明の中に入れてしまう。"])


# (英文, 正しい訳, [(誤訳, 理由)])
MEANING = [
    ("The boy who Emi likes plays soccer.", "エミが好きな少年はサッカーをする。",
     [("エミのことが好きな少年はサッカーをする。", "who の後ろに Emi likes（主語＋動詞）が続く目的格。好きなのはエミのほうで、少年は好かれている側。"),
      ("少年はエミが好きで、サッカーをする。", "who Emi likes は The boy を説明するかたまり。文の動詞は plays だけ。"),
      ("サッカーをする少年はエミが好きだ。", "文の動詞は plays。「エミが好き」は少年の説明で、主語と述語の関係を取り違えている。")]),
    ("The girl who likes Ken is my sister.", "ケンのことが好きな女の子は私の妹です。",
     [("ケンが好きになった女の子は私の妹です。", "who の直後に動詞 likes が続く主格。好きなのは女の子のほう。"),
      ("女の子はケンが好きで、私の妹です。", "who likes Ken は The girl を説明するかたまり。並べた2つの文として訳していない。"),
      ("ケンが好きなのは私の妹の女の子です。", "文の主語は The girl、文の動詞は is。主語を取り違えている。")]),
    ("I want a dog which can swim.", "私は泳ぐことができる犬がほしい。",
     [("私は泳ぐことができるので、犬がほしい。", "which can swim は理由ではなく、a dog を説明している。"),
      ("私は犬といっしょに泳ぎたい。", "泳ぐのは犬。which の後ろは a dog の説明。"),
      ("犬は泳ぐことができるものがほしい。", "文の主語は I。want の目的語が a dog which can swim。")]),
    ("The man that I helped yesterday sent me a letter.", "私が昨日助けた男性が、私に手紙を送ってくれた。",
     [("昨日私を助けてくれた男性が、私に手紙を送ってくれた。", "that の後ろに I helped（主語＋動詞）が続く目的格。助けたのは私。"),
      ("私は昨日男性を助けて、手紙を送った。", "文の主語は The man で、手紙を送ったのは男性。"),
      ("男性は私に、昨日助けたという手紙を送った。", "that I helped yesterday は The man を説明するかたまり。手紙の内容ではない。")]),
    ("This is the house which my grandfather built.", "これは私の祖父が建てた家です。",
     [("これは私の祖父を建てた家です。", "which の後ろは my grandfather built（主語＋動詞）。建てたのは祖父。"),
      ("これは家で、私の祖父が建てています。", "built は過去形。また、which 以下は the house を説明するかたまり。"),
      ("私の祖父はこの家を建てるつもりです。", "文は This is ～ で「これは～です」。未来の意味もない。")]),
    ("The students who cleaned the room went home.", "部屋をそうじした生徒たちは家に帰った。",
     [("生徒たちが家に帰った部屋をそうじした。", "文の動詞は went。cleaned the room は The students の説明。"),
      ("生徒たちは部屋をそうじするために家に帰った。", "who 以下は目的ではなく、The students を説明している。"),
      ("部屋をそうじした人は、生徒たちの家に行った。", "主語は The students。went home は「家に帰った」。")]),
    ("Do you know the woman who is talking with Mr. Ito?", "伊藤先生と話している女性を知っていますか。",
     [("伊藤先生が話している女性を知っていますか。", "who の直後に is talking が続く主格。話しているのは女性。"),
      ("あなたは伊藤先生と話している女性ですか。", "Do you know ～? は「～を知っていますか」とたずねる文。"),
      ("女性は伊藤先生と話していることを知っていますか。", "the woman who ～ は know の目的語のかたまり。「～ということ」の意味はない。")]),
    ("The picture that Aya painted won a prize.", "アヤがかいた絵が賞をとった。",
     [("アヤが賞をとった絵をかいた。", "文の動詞は won で、主語は The picture。賞をとったのは絵。"),
      ("アヤをかいた絵が賞をとった。", "that の後ろに Aya painted（主語＋動詞）が続く目的格。かいたのはアヤ。"),
      ("その絵には、アヤが賞をとったところがかかれている。", "that Aya painted は The picture を説明するかたまり。絵の内容ではない。")]),
    ("I have a friend who has visited Spain twice.", "私には2回スペインを訪れたことがある友だちがいる。",
     [("私は2回スペインを訪れた友だちを持っていた。", "have は現在形。has visited は友だちの経験を表している。"),
      ("私の友だちは2回、私をスペインに連れて行った。", "who has visited Spain twice は a friend の経験を説明している。"),
      ("私は友だちと2回スペインを訪れたことがある。", "訪れたのは友だち。who 以下は a friend の説明。")]),
]


@gen("standard_practice", 4, ["concept", "application"])
def meaning(r):
    en, ok, wrongs = r.choice(MEANING)
    return mc(f"次の英文の意味として最も適切なものを選びなさい。\n{en}", [ok] + [w for w, _ in wrongs],
              f"関係代名詞以下が先行詞を後ろから説明している。説明のかたまりと文の動詞を区別して訳す。答え：{ok}", d=3,
              ap="関係代名詞以下の説明のかたまりを［ ］でくくり、主格か目的格かを確かめてから、文全体の主語と動詞を見つける。",
              steps=["関係代名詞と先行詞を見つける。", "直後が動詞なら「～する（先行詞）」、主語＋動詞なら「…が～する（先行詞）」と訳す。", "説明のかたまりの外にある、文全体の動詞を見つけて訳す。", f"答え：{ok}"],
              alt=["選んだ日本語を英語に戻してみて、主語・動詞・説明の関係がもとの英文と一致するかを確かめる。"],
              pc=[("説明のかたまり（主格・目的格）を正しく訳している", 2), ("文全体の主語と動詞を正しく捉えている", 2)],
              pit=["主格と目的格を取り違え、「だれがだれを」を逆に訳す。", "説明の中の動詞を文全体の動詞と考える。"],
              why={w: (reason, "関係代名詞の文の構造の読み取り") for w, reason in wrongs})


# (関係代名詞の文, 空所つきの言いかえ, 答え, 説明)
REWRITE = [
    ("The boy who is running over there is Ken.", "The boy (　　) over there is Ken.", "running", "〈who is＋ing〉は現在分詞の後置修飾で言いかえられる。"),
    ("This is a car which was made in Germany.", "This is a car (　　) in Germany.", "made", "〈which was＋過去分詞〉は過去分詞の後置修飾で言いかえられる。"),
    ("The language which is spoken in Mexico is Spanish.", "The language (　　) in Mexico is Spanish.", "spoken", "〈which is＋過去分詞〉→ 過去分詞 spoken だけで名詞を説明できる。"),
    ("Look at the girl who is dancing on the stage.", "Look at the girl (　　) on the stage.", "dancing", "〈who is＋ing〉→ 現在分詞 dancing。"),
    ("I got a letter which was written in English.", "I got a letter (　　) in English.", "written", "〈which was＋過去分詞〉→ 過去分詞 written。"),
    ("The book which I read last night was sad.", "The book (　　) read last night was sad.", "I", "目的格の関係代名詞 which は省略でき、〈主語＋動詞〉が直接名詞を説明する接触節になる。"),
    ("The man that we saw in the park was a singer.", "The man (　　) saw in the park was a singer.", "we", "目的格の that を省略した接触節。"),
    ("The dog sleeping on the sofa is Max.", "The dog (　　) is sleeping on the sofa is Max.", "which", "現在分詞の後置修飾は〈which / that is＋ing〉で言いかえられる。先行詞は動物なので which（that も可）。"),
    ("This is a temple built about 600 years ago.", "This is a temple (　　) was built about 600 years ago.", "which", "過去分詞の後置修飾は〈which / that was＋過去分詞〉で言いかえられる。先行詞は物なので which（that も可）。"),
    ("The woman playing the piano is my aunt.", "The woman (　　) is playing the piano is my aunt.", "who", "現在分詞の後置修飾は〈who / that is＋ing〉で言いかえられる。先行詞は人なので who（that も可）。"),
    ("These are the photos my brother took.", "These are the photos (　　) my brother took.", "which", "接触節は目的格の関係代名詞を補って言いかえられる。先行詞は物なので which（that も可）。"),
    ("Is this the bag you bought yesterday?", "Is this the bag (　　) you bought yesterday?", "which", "接触節に目的格の which（that も可）を補う。"),
    ("The students living in this dormitory come from Asia.", "The students (　　) live in this dormitory come from Asia.", "who", "現在分詞 living は〈who live〉で言いかえられる。先行詞は人なので who（that も可）。"),
]


@gen("standard_practice", 4, ["cross_unit", "condition_check"], rel=["JH-ENG-G3-U02"])
def rewrite_participle(r):
    a, b, ans, point = r.choice(REWRITE)
    vs = ["that"] if ans in ("which", "who") else None
    return sa(f"2つの英文がほぼ同じ意味になるように、（　）に入る適切な1語を書きなさい。\n{a}\n{b}", ans,
              f"{point}答え：{ans}", d=2, p=4, v=vs,
              ap="前の単元の分詞の後置修飾・接触節と、関係代名詞の文は言いかえができる。どの形とどの形が対応するかを考える。",
              steps=["1文目の名詞を説明している部分（分詞・接触節・関係代名詞）を見つける。",
                     "〈who / which is＋ing〉↔ 現在分詞、〈which was＋過去分詞〉↔ 過去分詞、目的格の関係代名詞 ↔ 省略（接触節）の対応を思い出す。",
                     f"空所に入る語を決める：{ans}"],
              alt=["完成した2文目を日本語に訳して、1文目と同じ意味になるかを確かめる。"],
              pc=[("分詞・接触節と関係代名詞の対応に気づいている", 2), ("正しい1語を書いている", 2)],
              pit=["先行詞が人なのに which を書く。", "主格の関係代名詞を省略できると考え、関係代名詞なしで動詞を続ける。"])


# (空所つき英文, 先行詞（主語）, 単数か, 惑わす名詞)
MAINV = [
    ("The book which my friends recommended (　　) very interesting.", "The book", True, "my friends"),
    ("The girls who live next to me (　　) good at tennis.", "The girls", False, "me"),
    ("The man who teaches my sisters (　　) from London.", "The man", True, "my sisters"),
    ("The pictures that Ken took in Hokkaido (　　) beautiful.", "The pictures", False, "Ken"),
    ("The boy who is talking with the girls (　　) my brother.", "The boy", True, "the girls"),
    ("The cookies which my aunt made (　　) delicious.", "The cookies", False, "my aunt"),
    ("The bike that those students use (　　) old.", "The bike", True, "those students"),
    ("The people who work at this store (　　) very kind.", "The people", False, "this store"),
    ("The song which the children sang (　　) popular in Japan.", "The song", True, "the children"),
    ("The students that Mr. Ito teaches (　　) in the science club.", "The students", False, "Mr. Ito"),
]


@gen("standard_practice", 3, ["condition_check", "common_error"])
def main_verb(r):
    s, head, sg, trap = r.choice(MAINV)
    ok, other = ("is", "are") if sg else ("are", "is")
    why = {other: (f"文の主語は先行詞 {head}（{'単数' if sg else '複数'}）。説明の中の {trap} につられて {other} にしてはいけない。", "長い主語と動詞の一致"),
           "be": ("be は原形で、文の動詞として主語のすぐ後には使えない。現在の文では is / are にする。", "be 動詞の形"),
           "am": ("am は主語が I のときだけ使う。", "be 動詞の形")}
    return mc(f"（　）に入る語として正しいものを選びなさい。\n{s}", [ok] + list(why),
              f"関係代名詞の説明のかたまりの後ろに、文全体の動詞が来る。主語は {head} なので {ok}。", d=3, p=4,
              ap="関係代名詞から空所の前までを［ ］でくくり、文全体の主語がどの名詞かを確かめる。",
              steps=["関係代名詞の説明のかたまりを［ ］でくくる。", f"［ ］の外の主語は {head}（{'単数' if sg else '複数'}）。", f"be 動詞は {ok}。"],
              alt=[f"説明のかたまりを取り除いた短い文（{head} (　　) ～.）にして、主語と be 動詞の形を確かめる。"],
              pc=[("文全体の主語を見つけている", 2), ("主語に合う be 動詞を選んでいる", 2)],
              pit=[f"空所の直前の名詞（{trap}）に合わせて be 動詞を決める。", "説明の中の動詞を文の動詞と考え、be 動詞を入れなくてよいと考える。"], why=why)


# ======================================================================
# C 思考力・記述応用
# ======================================================================

PAIRS = [
    ("I know the girl who likes Tom.", "I know the girl Tom likes.",
     "A の who は直後に動詞 likes が続く主格で「トムのことが好きな女の子」、つまり好きなのは女の子。B は目的格の関係代名詞が省略された形で、the girl の後ろに Tom likes（主語＋動詞）が続き「トムが好きな女の子」、つまり好きなのはトムで、女の子は好かれている側。"),
    ("The man who called Ken is my father.", "The man Ken called is my father.",
     "A の who は主格で「ケンに電話をかけた男性」（電話をかけたのは男性）。B は目的格の省略で「ケンが電話をかけた男性」（電話をかけたのはケン）。どちらも文の動詞は is で、「その男性は私の父だ」という点は同じ。"),
    ("The boy who helped Yumi was Ken.", "The boy that Yumi helped was Ken.",
     "A の who は直後に動詞 helped が続く主格で「ユミを助けた少年」（助けたのは少年）。B の that は直後に Yumi helped（主語＋動詞）が続く目的格で「ユミが助けた少年」（助けたのはユミ）。"),
    ("The girl who is talking with Emi is my sister.", "The girl that Emi is talking about is my sister.",
     "A の who は主格で「エミと話している女の子」（女の子が話している）。B の that は目的格で、about の目的語が欠けており「エミが（話題にして）話している女の子」（話しているのはエミで、女の子は話題）。"),
    ("She is the singer who loves my brother.", "She is the singer my brother loves.",
     "A の who は主格で「私の兄のことを愛している歌手」（愛しているのは歌手）。B は目的格の省略で「私の兄が愛している（大好きな）歌手」（愛しているのは兄）。"),
    ("The dog which chased the cat is Pochi.", "The dog which the cat chased is Pochi.",
     "A の which は直後に動詞 chased が続く主格で「ねこを追いかけた犬」（追いかけたのは犬）。B の which は直後に the cat chased（主語＋動詞）が続く目的格で「ねこが追いかけた犬」（追いかけたのはねこ）。"),
    ("The teacher who Ms. Mori met in Canada is Mr. White.", "The teacher who met Ms. Mori in Canada is Mr. White.",
     "A の who は直後に Ms. Mori met（主語＋動詞）が続く目的格で「森先生がカナダで会った先生」。B の who は直後に動詞 met が続く主格で「カナダで森先生に会った先生」。会うという動作の主語が入れかわっている。"),
]


@gen("thinking_writing", 4, ["written_reasoning", "concept"])
def explain_difference(r):
    a, b, model = r.choice(PAIRS)
    return desc(f"次の2つの英文 A・B の意味の違いを、関係代名詞（または省略された関係代名詞）の働きに注目して、日本語で説明しなさい。\nA：{a}\nB：{b}", model,
                "関係代名詞の直後が動詞なら主格（先行詞が動作をする側）、〈主語＋動詞〉なら目的格（先行詞が動作を受ける側）。この違いで「だれがだれに」が入れかわる。",
                [("A の説明のかたまりの意味を正しく説明している", 3), ("B の説明のかたまりの意味を正しく説明している", 3), ("主格・目的格の違いが意味の違いを生むことを指摘している", 2)], d=3, p=8, lines=5,
                ap="A・B それぞれの説明のかたまりを［ ］でくくり、その中の動詞の主語がだれかを確かめる。",
                steps=["A と B の先行詞を見つける。", "それぞれの関係代名詞（または省略）の直後が動詞か、主語＋動詞かを確かめる。",
                       "説明の中の動作を「だれがする」かを書き出す。", "和訳を示して違いを説明する。"],
                alt=["それぞれの説明のかたまりを、先行詞を代名詞にして1つの文に戻す（例：She likes Tom. / Tom likes her.）と、違いがはっきりする。"],
                pc=[("A の説明", 3), ("B の説明", 3), ("違いを生む文法の指摘", 2)],
                pit=["和訳だけを書いて、なぜ意味が違うのかを説明しない。", "目的格の省略に気づかず、B を「トムと女の子が好き」などと訳す。"])


# (A の文, B の文, 模範解答)
THAT = [
    ("I think that the movie is exciting.", "This is the movie that I saw last week.",
     "A の that は think の目的語になる文をつなぐ接続詞で、後ろの the movie is exciting は主語・補語がそろった完全な文。B の that は the movie を説明する目的格の関係代名詞で、後ろの I saw last week には saw の目的語が欠けている。"),
    ("Ken knows that the girl lives in Osaka.", "Ken knows the girl that lives in Osaka.",
     "A の that は「～ということ」を表す接続詞で、後ろの the girl lives in Osaka は完全な文（ケンはその女の子が大阪に住んでいることを知っている）。B の that は the girl を説明する主格の関係代名詞で、後ろに主語がなくすぐ動詞 lives が続く（ケンは大阪に住んでいる女の子を知っている）。"),
    ("I hope that you will like the present.", "I hope you will like the present that I chose.",
     "A の that は hope の後ろで文をつなぐ接続詞で、後ろの you will like the present は完全な文。B の that は the present を説明する目的格の関係代名詞で、後ろの I chose には chose の目的語が欠けている。"),
    ("She said that the bus was late.", "She took the bus that was late.",
     "A の that は said の後ろで「～ということ」と文をつなぐ接続詞で、後ろの the bus was late は完全な文。B の that は the bus を説明する主格の関係代名詞で、後ろに主語がなくすぐ was が続く。"),
    ("We know that the teacher came from Kenya.", "We know the teacher that came from Kenya.",
     "A の that は「～ということ」の接続詞で、後ろの the teacher came from Kenya は完全な文。B の that は the teacher を説明する主格の関係代名詞で、後ろに主語がなくすぐ came が続く。"),
    ("I was surprised that the store was closed.", "This is the store that my uncle opened.",
     "A の that は感情（surprised）の理由を表す文をつなぐ接続詞で、後ろの the store was closed は完全な文。B の that は the store を説明する目的格の関係代名詞で、後ろの my uncle opened には opened の目的語が欠けている。"),
]


@gen("thinking_writing", 3, ["cross_unit", "written_reasoning"], rel=["JH-ENG-G2-U03"])
def that_explain(r):
    a, b, model = r.choice(THAT)
    return desc(f"次の A・B の英文の that の働きはそれぞれ何か答えなさい。また、そう判断した理由を、that の後ろの文の形に注目して説明しなさい。\nA：{a}\nB：{b}", model,
                "接続詞の that の後ろは主語・動詞・目的語のそろった完全な文、関係代名詞の that の後ろは主語か目的語が1つ欠けた文になる。",
                [("A の that の働きを正しく答えている", 2), ("B の that の働きを正しく答えている", 2), ("that の後ろの文が完全か、何が欠けているかを根拠に説明している", 4)], d=4, p=8, lines=5,
                ap="that の後ろだけを取り出して、1つの文として完成しているか（主語・目的語がそろっているか）を確かめる。",
                steps=["A・B それぞれ that の後ろの部分を書き出す。", "主語・動詞・目的語がそろっているかを確かめる。",
                       "そろっていれば接続詞、主語か目的語が欠けていれば関係代名詞と判断する。", "関係代名詞なら、先行詞と主格・目的格を書き添える。"],
                alt=["that を省いても文が成り立つか、which / who に置きかえられるかを試す（置きかえられれば関係代名詞）。"],
                pc=[("A の働き", 2), ("B の働き", 2), ("文の形にもとづく根拠", 4)],
                pit=["that をすべて「あれ」や「～ということ」と訳す。", "関係代名詞の that の後ろで、欠けている語に気づかない。"])


# (語, 模範解答, 解説)
DEFINE = [
    ("辞書（dictionary）", "A dictionary is a book which tells us the meanings of words.", "物を説明するので which（that）。tells は先行詞 a book に合わせて s がつく。"),
    ("パイロット（pilot）", "A pilot is a person who flies planes.", "人を説明するので who（that）。flies は a person に合わせて三単現。"),
    ("冷蔵庫（refrigerator）", "A refrigerator is a machine which keeps food cold.", "物を説明するので which（that）。keeps は a machine に合わせる。"),
    ("図書館員（librarian）", "A librarian is a person who works at a library.", "人を説明するので who（that）。works は a person に合わせる。"),
    ("時計（clock）", "A clock is a thing which tells us the time.", "物を説明するので which（that）。tells は a thing に合わせる。"),
    ("料理人（cook）", "A cook is a person who makes food at a restaurant.", "人を説明するので who（that）。makes は a person に合わせる。"),
    ("かさ（umbrella）", "An umbrella is a thing which we use when it rains.", "目的格の which（that）を使い、we use の目的語を欠かせている。"),
    ("ペンギン（penguin）", "A penguin is a bird which cannot fly but can swim well.", "動物を説明するので which（that）。"),
]


@gen("thinking_writing", 3, ["application", "written_reasoning"])
def write_definition(r):
    word, model, point = r.choice(DEFINE)
    return desc(f"英語のクイズを作ります。「{word}」がどんなものかを、関係代名詞を使って英語1文で説明しなさい。ただし、文は〈A（An）～ is a … who / which ―.〉の形にすること。また、who と which のどちらを使ったか、その理由を日本語で書きなさい。",
                f"（解答例）{model}　理由：{point}", f"（解答例の解説）{point} 説明のかたまりは、a person / a thing などの先行詞のすぐ後ろに置く。",
                [("先行詞に合った関係代名詞を使い、正しい語順で書いている", 3), ("関係代名詞の後ろの動詞の形（三単現など）が正しい", 2), ("関係代名詞を選んだ理由を説明している", 2), ("つづり・大文字・ピリオドが正しい", 1)], d=4, p=8, lines=4,
                ap="「～は、…する人（物）です」と日本語で説明を考えてから、先行詞 a person / a thing / a machine などを決め、その後ろに説明を置く。",
                steps=["日本語で「～は、…する人（物）です」という説明を考える。", "先行詞（a person / a thing など）を決め、人なら who、物・動物なら which を選ぶ。",
                       "関係代名詞の後ろに動詞（先行詞に合わせた形）を続ける。", "理由を「先行詞が人（物）だから」と書く。"],
                alt=["書いた文を Who am I? / What is this? のクイズとして読み上げ、答えが1つに決まるかを確かめる（説明が足りているかの確認）。"],
                pc=[("関係代名詞と語順", 3), ("動詞の形", 2), ("理由の説明", 2), ("表記", 1)],
                pit=["人を説明するのに which を使う。", "a person who fly のように、動詞の三単現の s を落とす。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(task, wrong, step, etype, tempt, fix, expl, steps, ap, alt, pit):
    return desc(f"{task}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい英文に書き直しなさい。", fix, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい英文に直している", 3), ("文法のルールを説明している", 1)], d=3, p=6, lines=4,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい英文", 3), ("ルールの説明", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix))


CHOICE_ERR = [
    ("私は耳の長い犬を飼っています。", "I have a dog who has long ears.", "I have a dog which has long ears.", "who",
     "先行詞 a dog は動物なので、who ではなく which（that）を使う。", "ペットを家族のように感じ、人と同じ who を使った。"),
    ("これは私のおじが住んでいる家です。", "This is the house who my uncle lives in.", "This is the house which my uncle lives in.", "who",
     "先行詞 the house は物なので which（that）を使う。", "直後の my uncle（人）につられて who を選んだ。"),
    ("私には歌の上手な姉がいます。", "I have a sister which sings well.", "I have a sister who sings well.", "which",
     "先行詞 a sister は人なので who（that）を使う。", "who と which の使い分けを、先行詞を見ずに決めた。"),
    ("向こうで走っている男の子はタクです。", "The boy which is running over there is Taku.", "The boy who is running over there is Taku.", "which",
     "先行詞 The boy は人なので who（that）を使う。", "関係代名詞はどれも同じと考え、which を使った。"),
    ("あなたが昨日会った女性は私の母です。", "The woman what you met yesterday is my mother.", "The woman that you met yesterday is my mother.", "what",
     "先行詞の後ろに what は置けない。人の目的格は that（who も可）を使う。", "日本語の「何」以外にも what が使えると思った。"),
    ("私がいちばん好きな教科は理科です。", "The subject who I like the best is science.", "The subject which I like the best is science.", "who",
     "先行詞 The subject は物（教科）なので which（that）を使う。", "直後の I（人）につられて who を選んだ。"),
    ("ケンにはテニスの上手な友だちがたくさんいる。", "Ken has many friends which play tennis well.", "Ken has many friends who play tennis well.", "which",
     "先行詞 many friends は人なので who（that）を使う。", "先行詞が複数のときは which だと誤解した。"),
]


@gen("error_correction", 4, ["common_error", "condition_check"])
def err_choice(r):
    jp, wrong, fix, where, rule, tempt = r.choice(CHOICE_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"関係代名詞「{where}」の部分", "condition", tempt, fix, f"{rule}正しくは {fix}",
                    ["先行詞を見つけ、人か物・動物かを確かめる。", f"「{where}」の誤りを見つける：{rule}", f"正しい英文：{fix}"],
                    "関係代名詞は、関係代名詞の後ろの語ではなく、直前の先行詞が人か物かで決まる。",
                    ["直した関係代名詞を that に置きかえても文が成り立つかを確かめる（that は人にも物にも使える）。"],
                    ["関係代名詞の後ろの名詞（主語）を見て who / which を決める。", "動物の先行詞に who を使う。"])


DOUBLE_ERR = [
    ("これは私が昨日買ったかばんです。", "This is the bag which I bought it yesterday.", "This is the bag which I bought yesterday.", "it",
     "which が it の代わりになっているので、bought の後ろの it は書かない。", "もとの文 I bought it yesterday. をそのまま後ろにつなげた。"),
    ("私たちが駅で会った男性は親切だった。", "The man that we met him at the station was kind.", "The man that we met at the station was kind.", "him",
     "that が him の代わりになっているので、met の後ろの him は書かない。", "met の後ろに目的語がないと不自然に感じ、him を補った。"),
    ("私にはロンドンに住んでいる友だちがいる。", "I have a friend who she lives in London.", "I have a friend who lives in London.", "she",
     "who が she の代わり（主語）になっているので、she は書かない。", "who を接続詞のように考え、後ろにもとの文を完全な形で続けた。"),
    ("母が作ったケーキはおいしかった。", "The cake which my mother made it was delicious.", "The cake which my mother made was delicious.", "it",
     "which が it の代わり（made の目的語）なので、it は書かない。", "My mother made it. を関係代名詞の後ろにそのまま入れた。"),
    ("あなたがとった写真を見せてください。", "Please show me the pictures you took them.", "Please show me the pictures you took.", "them",
     "目的格の関係代名詞が省略された形で、the pictures が took の目的語にあたる。them は書かない。", "関係代名詞が省略されていて、目的語が欠けていることに気づかなかった。"),
    ("これは東京へ行くバスです。", "This is the bus which it goes to Tokyo.", "This is the bus which goes to Tokyo.", "it",
     "which が it の代わり（主語）なので、it は書かない。", "主語がないと文にならないと考え、it を入れた。"),
]


@gen("error_correction", 3, ["common_error", "concept"])
def err_double(r):
    jp, wrong, fix, where, rule, tempt = r.choice(DOUBLE_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"代名詞「{where}」の部分", "concept", tempt, fix, f"{rule}正しくは {fix}",
                    ["関係代名詞（または省略された関係代名詞）が、もとの文のどの代名詞の代わりかを確かめる。", f"同じものを指す「{where}」が重なっている：{rule}", f"正しい英文：{fix}"],
                    "関係代名詞は代名詞の役目をもっている。関係代名詞にかえた代名詞は、もう書かない。",
                    ["直した文を2つの文に分けて、関係代名詞が代名詞 1 つ分の働きをしていることを確かめる。"],
                    ["もとの文の代名詞を残したまま関係代名詞をつける。", "目的格の関係代名詞を省略したとき、目的語が欠けていることに気づかない。"])


AGREE_ERR = [
    ("私にはピアノをひく友だちがいる。", "I have a friend who play the piano.", "I have a friend who plays the piano.", "play", "calculation",
     "who の後ろの動詞の主語は先行詞 a friend（三人称単数）なので plays にする。", "文の主語 I に合わせて、動詞に s をつけなかった。"),
    ("この町に住んでいる人々は親切です。", "The people who lives in this town are kind.", "The people who live in this town are kind.", "lives", "calculation",
     "先行詞 The people は複数なので live にする。", "who の後ろの動詞にはいつも s がつくと思いこんだ。"),
    ("私が昨日読んだ本はおもしろかった。", "The book which I read yesterday interesting.", "The book which I read yesterday was interesting.", "interesting の前", "logic",
     "The book が文の主語、which I read yesterday は説明のかたまり。文の動詞 was が抜けている。", "read を文の動詞と考え、文がもう完成していると思った。"),
    ("ケンが描いた絵は美しい。", "The pictures that Ken painted is beautiful.", "The pictures that Ken painted are beautiful.", "is", "calculation",
     "文の主語は The pictures（複数）なので be 動詞は are。", "直前の Ken（単数）につられて is にした。"),
    ("向こうで話している女の子たちは私のクラスメートです。", "The girls who is talking over there are my classmates.", "The girls who are talking over there are my classmates.", "who is", "calculation",
     "先行詞 The girls は複数なので、who の後ろの be 動詞は are。", "who を単数のように考えて is にした。"),
    ("トムが作ったロボットは動きます。", "The robot Tom made it moves.", "The robot Tom made moves.", "it", "concept",
     "目的格の関係代名詞が省略された形。the robot が made の目的語にあたるので it は不要。文の動詞 moves の主語は The robot。", "Tom made it. と The robot moves. を両方完全な文の形で残そうとした。"),
]


@gen("error_correction", 3, ["common_error", "computation"])
def err_agree(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(AGREE_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", etype, tempt, fix, f"{rule}正しくは {fix}",
                    ["説明のかたまりを［ ］でくくり、先行詞と文全体の主語・動詞を確かめる。", f"「{where}」の部分の誤りを見つける：{rule}", f"正しい英文：{fix}"],
                    "関係代名詞の後ろの動詞は先行詞に、文全体の動詞は文の主語（先行詞）に合わせる。説明のかたまりの中と外を分けて考える。",
                    ["説明のかたまりを取り除いた短い文と、関係代名詞を先行詞に置きかえた文の2つを作り、それぞれ主語と動詞が合っているかを確かめる。"],
                    ["関係代名詞の後ろの動詞を、文の主語や直前の名詞に合わせる。", "長い主語の文で、文全体の動詞を書き忘れる。"])


GENERATORS = [choose_rel, subj_or_obj, find_antecedent, verb_agree, omit_possible,
              combine, build_order, meaning, rewrite_participle, main_verb,
              explain_difference, that_explain, write_definition,
              err_choice, err_double, err_agree]
