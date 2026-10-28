"""単元パック：中学3年 英語 分詞の後置修飾（現在分詞・過去分詞による修飾、接触節）。"""
from banks._common import desc, mc, order, sa
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem,
                         tp)

UNIT_ID = "JH-ENG-G3-U02"

PREREQUISITES = [
    ("JH-ENG-G1-U04", "動詞の ing 形のつづりと、現在進行形 be＋ing 形の「～している」という意味。現在分詞の修飾はこの意味をそのまま使う。"),
    ("JH-ENG-G2-U05", "過去分詞の形と、受け身 be＋過去分詞の「～される（された）」という意味。過去分詞の修飾はこの意味をそのまま使う。"),
    ("JH-ENG-G2-U02", "不定詞の形容詞的用法（something to drink）で、名詞を後ろから説明する語順に一度ふれていること。"),
]
EXTENSIONS = [
    ("JH-ENG-G3-U03", "接触節（the picture I took）は、目的格の関係代名詞 which / that を使った the picture which I took と同じ意味。関係代名詞で名詞を後ろから説明する形に広がる。"),
    ("HS-ENG-U05", "高校の「分詞と分詞構文」で、分詞が名詞の説明だけでなく文全体に情報を加える分詞構文や、SVOC の C になる分詞へと発展する。"),
    ("HS-ENG-U06", "高校の「関係詞」で、関係代名詞の省略や前置詞＋関係代名詞など、名詞を後ろから説明する形をさらに詳しく学ぶ。"),
]


def cap(s):
    return s[0].upper() + s[1:]


# ======================================================================
# 授業プリント
# ======================================================================

LESSON = lesson(
    goals=["〈名詞＋現在分詞（ing 形）＋語句〉で「～している…」、〈名詞＋過去分詞＋語句〉で「～された…」と、名詞を後ろから説明できる。",
           "説明される名詞が動作を「している」側か「される」側かで、現在分詞と過去分詞を使い分けられる。",
           "分詞が1語のときは名詞の前、語句がつくときは名詞の後ろに置くという語順の原則がわかる。",
           "〈名詞＋主語＋動詞〉の接触節（the picture my father took）で、「（主語）が～する（した）…」と名詞を説明できる。"],
    duration=50,
    readiness=["現在進行形（He is playing tennis.）と受け身（This car was made in Japan.）の文を作れる（中1・中2）。",
               "不規則動詞の過去分詞（made, written, taken, spoken など）を書ける（中2）。",
               "不定詞の形容詞的用法（I want something to drink.）で、名詞の後ろに説明を置く語順を知っている（中2）。",
               "国語で、「公園で走っている犬」のように名詞を前から説明する言い方（連体修飾）を知っている（小学校）。"],
    flow=[("導入：日本語と英語の語順の違い", 5, "「ピアノをひいている女の子」を英語にすると、どこに girl を置くか考えさせる"),
          ("現在分詞による後置修飾", 12, "名詞＋ing 形＋語句、1語なら前・語句つきなら後ろ（例題1）"),
          ("過去分詞による後置修飾", 12, "名詞＋過去分詞＋語句、ing 形との使い分け（例題2）"),
          ("接触節", 13, "名詞＋主語＋動詞。2つの文を1つにする手順（例題3）"),
          ("まとめと確認", 8, "3つの形を表で比べ、確認問題3問")],
    sections=[
        intro("in1", "英語は「名詞が先、説明があと」",
              "日本語では「ピアノをひいている女の子」のように、説明（ピアノをひいている）を名詞（女の子）の前に置きます。英語では、説明が2語以上になるとき、名詞を先に言ってから後ろに説明を続けます。the girl playing the piano（女の子 ← ピアノをひいている）。まず「だれ・何のことか」を言い、そのあとで詳しく説明するのが英語の語順です。",
              bullets=["the girl playing the piano（ピアノをひいている女の子）", "a car made in Japan（日本で作られた車）",
                       "the picture my father took（私の父がとった写真）"],
              points=[tp("日本語と英語の語順を矢印で比べさせ、英語では名詞の後ろから前の名詞に向かって説明が「かかる」ことを図で示す。",
                         ask="「ピアノをひいている女の子」を英語にするとき、最初に言うのはどの語か。", expect="the girl（女の子）。", timing="導入の冒頭")]),
        definition("df1", "現在分詞による修飾：名詞＋ing 形＋語句",
                   "動詞の ing 形（現在分詞）は「～している」という意味で名詞を説明できます。ing 形に語句がつくときは名詞の後ろに置きます。説明される名詞は、その動作を「している」側です。",
                   formula="名詞＋現在分詞（ing 形）＋語句 ＝「～している（名詞）」",
                   bullets=["The boy running in the park is my brother.（公園で走っている男の子は私の弟だ）",
                            "I have a friend living in Canada.（私にはカナダに住んでいる友だちがいる）",
                            "1語だけなら名詞の前：a sleeping baby（眠っている赤ちゃん）／ a crying girl（泣いている女の子）"],
                   conditions=["名詞のまとまり（the boy running in the park）は1つの名詞として、主語・目的語などになる。",
                               "主語が長くなっても、文の動詞（is / are など）は説明される名詞（boy）に合わせる。"],
                   points=[tp("The boy is running in the park.（文）と the boy running in the park（名詞のまとまり）を並べ、is の有無で文か名詞かが変わることを確認させる。",
                              caution="The boy is running in the park is my brother. のように is を残す誤りが多い。")]),
        definition("df2", "過去分詞による修飾：名詞＋過去分詞＋語句",
                   "過去分詞は「～された」「～されている」という受け身の意味で名詞を説明できます。語句がつくときは名詞の後ろに置きます。説明される名詞は、その動作を「される」側です。",
                   formula="名詞＋過去分詞＋語句 ＝「～された（名詞）」",
                   bullets=["This is a car made in Japan.（これは日本で作られた車だ）",
                            "I read a book written by Natsume Soseki.（私は夏目漱石によって書かれた本を読んだ）",
                            "1語だけなら名詞の前：a broken window（割れた窓）／ a used car（中古車）"],
                   conditions=["現在分詞か過去分詞かは、説明される名詞と動詞の関係で決める。名詞が動作を「する」→ ing 形、「される」→ 過去分詞。",
                               "過去分詞の形は受け身で学んだものと同じ（make - made - made、write - wrote - written）。"],
                   points=[tp("「名詞を主語にして文を作ると、進行形になるか受け身になるか」で ing 形と過去分詞を判断させる。",
                              ask="a letter (writing / written) in English。letter を主語にすると？", expect="The letter was written in English. と受け身になるので written。")]),
        theorem("th1", "接触節：名詞＋主語＋動詞",
                "名詞＋〈主語＋動詞 ～〉＝「（主語）が～する（した）（名詞）」",
                ["the picture my father took：私の父がとった写真", "the book I bought yesterday：私が昨日買った本",
                 "名詞のすぐ後ろに〈主語＋動詞〉を続ける。動詞の目的語にあたるのが前の名詞なので、目的語（it / them）はもう一度書かない。",
                 "動詞は文の時制に合わせてふつうの形（過去形・現在形）にする。分詞にはしない。"],
                body="接触節は、3年生で学ぶ目的格の関係代名詞（the picture which my father took）から which / that を省いた形と同じ意味になります。",
                points=[tp("This is the book I bought it. の it が二重になる誤りを取り上げ、book が bought の目的語の役割をしていることを矢印で示す。",
                           ask="I bought ～ の「～」にあたるのはどの語か。", expect="the book。だから it はいらない。")]),
        derivation("dv1", "2つの文を1つにして名詞を説明する手順（なぜその形になるのか）",
                   ["① Look at the girl. ＋ She is dancing on the stage. → 2つ目の文の She は the girl のこと。",
                    "② 2つ目の文から主語 She と be 動詞 is を取ると、dancing on the stage が残る。これを the girl の後ろに置く：Look at the girl dancing on the stage.",
                    "③ I have a bag. ＋ It was made in Italy. → It（＝a bag）と was を取ると made in Italy が残る：I have a bag made in Italy.",
                    "④ This is the cake. ＋ My mother made it. → it（＝the cake）を取ると my mother made が残る。これを the cake の後ろに置く：This is the cake my mother made.",
                    "⑤ ②③は「主語＋be 動詞」を取るので分詞が残り、④は目的語を取るので〈主語＋動詞〉が残る。どれも説明の部分が名詞の後ろに来る。"],
                   body="進行形の文から作れば現在分詞、受け身の文から作れば過去分詞、ふつうの文の目的語を取れば接触節になります。",
                   points=[tp("②③④の取り除く部分を色チョークで消していき、何が残るかを確認させる。",
                              ask="④で it を残すとどうなるか。", expect="cake と it が二重になってしまう。", timing="導出の説明時")]),
        example("ex1", "例題1　現在分詞で名詞を説明する",
                "日本語に合うように英文を書きなさい。(1) 向こうで走っている犬はケンの犬です。　(2) 私は木の下で本を読んでいる女の子を知っています。",
                ["(1) 「犬」は走っている側なので現在分詞 running。語句 over there がつくので後ろに置く：the dog running over there。",
                 "(1) このまとまりが主語。動詞は dog に合わせて is：The dog running over there is Ken's.",
                 "(2) 「女の子」は読んでいる側なので reading。the girl reading a book under the tree が know の目的語になる。"],
                "(1) The dog running over there is Ken's.　(2) I know the girl reading a book under the tree.",
                thinking="名詞を先に書き、そのあとに「ing 形＋語句」を続ける。",
                points=[tp("(1) で The dog is running over there is Ken's. とする生徒に、is が2つある文は成り立たないことを確認する。")],
                misconceptions=[("The running over there dog is Ken's.", "語句がつく分詞は名詞の後ろ。The dog running over there"),
                                ("I know the girl reads a book under the tree.", "reads にすると文の動詞が2つになる。reading にする。")]),
        example("ex2", "例題2　現在分詞か過去分詞か",
                "（　）内の動詞を適切な形にしなさい。(1) The language (speak) in Australia is English.　(2) Do you know the man (wear) a blue shirt?　(3) I found a bag (make) of paper.",
                ["(1) language は「話される」側（Languages are spoken.）なので過去分詞 spoken。",
                 "(2) man は「着ている」側（The man is wearing ～.）なので現在分詞 wearing。",
                 "(3) bag は「作られる」側（The bag was made of paper.）なので過去分詞 made。"],
                "(1) spoken　(2) wearing　(3) made",
                thinking="説明される名詞を主語にして、進行形（～している）になるか受け身（～される）になるかを考える。",
                points=[tp("(1) を speaking とする生徒に「言語が話しているのか、話されているのか」と問い返す。",
                           ask="language は話す側か、話される側か。", expect="話される側。だから過去分詞。")]),
        example("ex3", "例題3　接触節で名詞を説明する",
                "2つの文を、接触節を使って1つの文にしなさい。(1) This is the watch. My grandfather gave it to me.　(2) The movie was exciting. We saw it last night.",
                ["(1) it は the watch のこと。2つ目の文から it を取り、残りの my grandfather gave to me を the watch の後ろに置く。",
                 "(2) it は the movie のこと。we saw last night を the movie の後ろに置く。このまとまりが主語なので、文の動詞 was はそのあと。"],
                "(1) This is the watch my grandfather gave to me.　(2) The movie we saw last night was exciting.",
                thinking="前の名詞が動詞の目的語の役割をするので、it を書かない。",
                points=[tp("(2) は主語が長くなる例。The movie ～ last night までが主語で、was が文の動詞であることを下線で確認させる。")],
                misconceptions=[("This is the watch my grandfather gave it to me.", "it は the watch と重なるので不要。"),
                                ("The movie we saw it last night was exciting.", "it は the movie と重なるので不要。")]),
        board("bd1", "板書案",
              [("① 名詞＋ing 形", ["「～している…」（名詞がする側）", "the girl playing the piano", "a friend living in Canada", "1語なら前：a sleeping baby", "× The boy is running ～ is ～"]),
               ("② 名詞＋過去分詞", ["「～された…」（名詞がされる側）", "a car made in Japan", "a book written by Soseki", "1語なら前：a broken window", "判断：名詞を主語に → 進行形？受け身？"]),
               ("③ 接触節", ["名詞＋主語＋動詞", "the picture my father took", "the book I bought yesterday", "目的語 it / them は書かない", "→ 関係代名詞（which / that）の省略と同じ"])],
              points=[tp("3列とも「名詞 ← 説明」の矢印をそろえてかき、説明が後ろから前の名詞にかかる共通点を強調する。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("日本語と英語の語順の違いを、日本語の文を英語の語順に並べかえる活動（「女の子 ← ピアノをひいている」）で体験させる。", timing="導入"),
               tp("ing 形か過去分詞かで迷ったら、説明される名詞を主語にした文を作らせる。進行形なら ing、受け身なら過去分詞。",
                  ask="the window (breaking / broken) by Tom の window を主語にすると？", expect="The window was broken by Tom. なので broken。"),
               tp("長い主語の文では、主語のまとまりに下線を引き、文の動詞を丸で囲ませる。動詞の数（単数・複数）は説明される名詞に合わせる。",
                  caution="The students playing soccer is ～. のように近くの語につられた誤りに注意。"),
               tp("接触節は次の単元の関係代名詞の土台になる。ここでは「名詞のすぐ後ろに主語＋動詞」という形と、目的語を書かないことに集中させる。"),
               tp("問題プリント D の誤答例は「分詞の選び方」「be 動詞の残り」「語順（前か後ろか）」「接触節の目的語の重複」の4種類にまとめて振り返らせる。")],
              misconceptions=[("This is a car making in Japan.", "car は作られる側なので made。a car made in Japan。"),
                              ("The boy is running in the park is my brother.", "名詞のまとまりには is を入れない。The boy running in the park is my brother."),
                              ("This is the book I bought it yesterday.", "it は the book と重なる。This is the book I bought yesterday."),
                              ("I saw a sleeping on the sofa cat.", "語句がつく分詞は名詞の後ろ。a cat sleeping on the sofa。")]),
        summary("sm1", "まとめ",
                ["名詞＋現在分詞（ing 形）＋語句 ＝「～している（名詞）」。名詞が動作をする側。",
                 "名詞＋過去分詞＋語句 ＝「～された（名詞）」。名詞が動作をされる側。",
                 "分詞が1語なら名詞の前（a sleeping baby）、語句がつけば名詞の後ろ（a baby sleeping in the bed）。",
                 "接触節 ＝ 名詞＋主語＋動詞（the picture my father took）。目的語は書かない。"]),
        check("ck1", "確認問題",
              [("「英語で書かれた手紙」を英語にしなさい。", "a letter written in English"),
               ("Who is the boy (swimming / swum) in the river? の（　）から正しいほうを選びなさい。", "swimming（男の子は泳いでいる側）"),
               ("「これは私が昨日買ったペンです」を接触節を使って英語にしなさい。", "This is the pen I bought yesterday.")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

# (空所つき英文, 日本語, 原形, 現在分詞, 過去分詞, 文の動詞の形（誤り用）, 正解 ing / pp)
P = [
    ("The girl (　　) the piano is my sister.", "ピアノをひいている女の子は私の姉です。", "play", "playing", "played", "plays", "ing"),
    ("I have a friend (　　) in Canada.", "私にはカナダに住んでいる友だちがいます。", "live", "living", "lived", "lives", "ing"),
    ("The man (　　) a black hat is our new teacher.", "黒い帽子をかぶっている男性は私たちの新しい先生です。", "wear", "wearing", "worn", "wears", "ing"),
    ("Do you know the boy (　　) with Emi?", "エミと話している男の子を知っていますか。", "talk", "talking", "talked", "talks", "ing"),
    ("The dog (　　) over there is Ken's.", "向こうで走っている犬はケンの犬です。", "run", "running", "run", "ran", "ing"),
    ("Who is the woman (　　) a picture in the park?", "公園で絵をかいている女性はだれですか。", "draw", "drawing", "drawn", "draws", "ing"),
    ("The children (　　) in the pool look happy.", "プールで泳いでいる子どもたちは楽しそうです。", "swim", "swimming", "swum", "swam", "ing"),
    ("This is a car (　　) in Germany.", "これはドイツで作られた車です。", "make", "making", "made", "makes", "pp"),
    ("I read a book (　　) by a famous writer.", "私は有名な作家によって書かれた本を読みました。", "write", "writing", "written", "wrote", "pp"),
    ("The language (　　) in Mexico is Spanish.", "メキシコで話されている言語はスペイン語です。", "speak", "speaking", "spoken", "speaks", "pp"),
    ("Look at the window (　　) by the strong wind.", "強い風で割れた窓を見てください。", "break", "breaking", "broken", "broke", "pp"),
    ("These are pictures (　　) by my uncle in Hokkaido.", "これらはおじが北海道でとった写真です。", "take", "taking", "taken", "took", "pp"),
    ("We visited a temple (　　) about 400 years ago.", "私たちはおよそ400年前に建てられた寺を訪れました。", "build", "building", "built", "builds", "pp"),
    ("The singer (　　) by many young people is from Okinawa.", "多くの若者に愛されている歌手は沖縄出身です。", "love", "loving", "loved", "loves", "pp"),
    ("She showed me a letter (　　) in French.", "彼女は私にフランス語で書かれた手紙を見せてくれました。", "write", "writing", "written", "wrote", "pp"),
    ("Is this the bag (　　) at the station?", "これは駅で見つかったかばんですか。", "find", "finding", "found", "finds", "pp"),
    ("The students (　　) soccer in the schoolyard are my classmates.", "校庭でサッカーをしている生徒たちは私のクラスメートです。", "play", "playing", "played", "play", "ing"),
    ("The cake (　　) by my mother was delicious.", "母が作ったケーキはとてもおいしかった。", "make", "making", "made", "makes", "pp"),
]


def p_head(s):
    """空所の直前の名詞（説明される名詞）。"""
    return s.split(" (")[0].split()[-1]


@gen("basic_check", 5, ["condition_check", "computation"])
def ing_or_pp(r):
    s, jp, base, ing, pp, fin, k = r.choice(P)
    head = p_head(s)
    ok, other = (ing, pp) if k == "ing" else (pp, ing)
    rel_ok = "する側（進行形の関係）" if k == "ing" else "される側（受け身の関係）"
    why = {other: (f"{head} は動作を{rel_ok.split('（')[0].replace('側', '')}側なので {ok}。{other} では" + ("「～された」の意味になる。" if k == "ing" else "「（名詞が）～している」の意味になる。"), "現在分詞と過去分詞の区別"),
           fin: (f"{fin} は文の動詞の形。すでに文の動詞があるので、名詞を説明する部分は分詞にする。", "文の動詞と分詞の混同"),
           f"to {base}": (f"to {base} は「～するための・～すべき」という意味になり、日本語に合わない。", "不定詞との混同")}
    return mc(f"日本語に合うように、（　）に入る最も適切なものを選びなさい。\n{jp}\n{s}", [ok] + list(why),
              f"{head} は動作を{rel_ok}。答え：{ok}", d=1,
              ap=f"説明される名詞 {head} を主語にした文を考え、進行形（～している）になるか、受け身（～される）になるかで分詞を選ぶ。",
              steps=[f"説明される名詞は {head}。", f"{head} は動作を{rel_ok}。", f"答え：{ok}"],
              alt=[f"{cap(head)} {'is' if k == 'ing' else 'was'} {ok} ～. のように文にしてみて、意味が自然かどうかで確かめる。"],
              pc=[("名詞と動詞の関係を判断している", 1), ("正しい分詞を選んでいる", 1)],
              pit=["日本語の「～た」につられて過去形や過去分詞を選ぶ。", "名詞が動作を受ける側なのに ing 形を選ぶ。"], why=why)


POS = [
    ("ベッドで眠っている赤ちゃん", "a baby sleeping in the bed",
     [("a sleeping in the bed baby", "分詞に語句（in the bed）がつくときは名詞の後ろに置く。"),
      ("a baby slept in the bed", "slept は過去形（過去分詞）で、「眠っている」という進行中の意味にならない。"),
      ("a baby is sleeping in the bed", "is があると「赤ちゃんはベッドで眠っている」という文になり、名詞のまとまりにならない。")]),
    ("割れた窓", "a broken window",
     [("a broke window", "broke は過去形。名詞を説明するのは過去分詞 broken。"),
      ("a breaking window", "窓は「割られる」側なので過去分詞。breaking では「（何かを）割っている窓」になる。"),
      ("a window is broken", "is があると「窓は割れている」という文になり、名詞のまとまりにならない。")]),
    ("泣いている女の子", "a crying girl",
     [("a cried girl", "cried は過去形（過去分詞）で、「泣いている」の意味にならない。"),
      ("a girl cries", "cries は文の動詞の形で、「女の子が泣く」という文になってしまう。"),
      ("a girl is crying", "is があると「女の子が泣いている」という文になり、名詞のまとまりにならない。")]),
    ("日本で作られた車", "a car made in Japan",
     [("a made in Japan car", "分詞に語句（in Japan）がつくときは名詞の後ろに置く。"),
      ("a car making in Japan", "車は「作られる」側なので過去分詞 made。"),
      ("a car was made in Japan", "was があると「車が日本で作られた」という文になり、名詞のまとまりにならない。")]),
    ("木の下に立っている男の子", "the boy standing under the tree",
     [("the standing under the tree boy", "分詞に語句（under the tree）がつくときは名詞の後ろに置く。"),
      ("the boy stood under the tree", "stood は過去形で、「男の子が木の下に立った」という文になる。"),
      ("the boy stands under the tree", "stands は文の動詞の形で、名詞のまとまりにならない。")]),
    ("英語で書かれたメール", "an e-mail written in English",
     [("a written in English e-mail", "分詞に語句（in English）がつくときは名詞の後ろに置く。"),
      ("an e-mail writing in English", "メールは「書かれる」側なので過去分詞 written。"),
      ("an e-mail wrote in English", "wrote は過去形。名詞を説明するのは過去分詞 written。")]),
    ("ゆでた卵", "a boiled egg",
     [("a boil egg", "boil は動詞の原形で、名詞を説明する形になっていない。卵はゆでられる側なので過去分詞 boiled。"),
      ("an egg boil", "boil は動詞の原形で、名詞を説明する形になっていない。"),
      ("an egg is boiled", "is があると「卵がゆでられる」という文になり、名詞のまとまりにならない。")]),
    ("ステージで歌っている歌手", "the singer singing on the stage",
     [("the singing on the stage singer", "分詞に語句（on the stage）がつくときは名詞の後ろに置く。"),
      ("the singer sung on the stage", "sung は過去分詞で「歌われた」の意味になる。歌手は歌う側なので singing。"),
      ("the singer sings on the stage", "sings は文の動詞の形で、名詞のまとまりにならない。")]),
    ("盗まれた自転車", "a stolen bike",
     [("a stole bike", "stole は過去形。名詞を説明するのは過去分詞 stolen。"),
      ("a stealing bike", "自転車は「盗まれる」側なので過去分詞。stealing では「盗んでいる自転車」になる。"),
      ("a bike was stolen", "was があると「自転車が盗まれた」という文になり、名詞のまとまりにならない。")]),
    ("公園でボールを追いかけている犬", "a dog chasing a ball in the park",
     [("a chasing a ball in the park dog", "分詞に語句がつくときは名詞の後ろに置く。"),
      ("a dog chased a ball in the park", "chased は過去形で、「犬が公園でボールを追いかけた」という文になる。"),
      ("a dog is chasing a ball in the park", "is があると文になり、名詞のまとまりにならない。")]),
]


@gen("basic_check", 4, ["concept", "common_error"])
def position(r):
    jp, ok, wrongs = r.choice(POS)
    return mc(f"次の日本語の意味を表す英語の「名詞のまとまり」として、最も適切なものを選びなさい。\n{jp}", [ok] + [w for w, _ in wrongs],
              f"分詞が1語なら名詞の前、語句がつけば名詞の後ろに置く。名詞が動作をする側なら ing 形、される側なら過去分詞。答え：{ok}", d=2,
              ap="①分詞は1語か、語句がつくか（位置を決める）、②名詞が動作をする側か、される側か（ing 形か過去分詞かを決める）、の2点を確かめる。",
              steps=["分詞に語句がつくかどうかで、名詞の前か後ろかを決める。", "名詞と動作の関係で ing 形か過去分詞かを決める。", f"答え：{ok}"],
              alt=["選んだまとまりを主語にして短い文（～ is nice. など）を作り、文として成り立つかを確かめる。"],
              pc=[("位置（前か後ろか）を判断している", 1), ("分詞の形を判断している", 1)],
              pit=["語句がついた分詞を名詞の前に置く。", "be 動詞を入れて文にしてしまう。"],
              why={w: (reason, "分詞の位置と形") for w, reason in wrongs})


# 接触節：(日本語, 空所つき英文, 主語, 文の動詞, ing 形, 目的語の代名詞)
CC = [
    ("これは兄が京都でとった写真です。", "This is the picture (　　) in Kyoto.", "my brother", "took", "taking", "it"),
    ("私が昨日買った本はとてもおもしろい。", "The book (　　) yesterday is very interesting.", "I", "bought", "buying", "it"),
    ("あなたが作ったケーキはとてもおいしかった。", "The cake (　　) was very delicious.", "you", "made", "making", "it"),
    ("彼女が書いた手紙を読みましたか。", "Did you read the letter (　　)?", "she", "wrote", "writing", "it"),
    ("私たちが昨日見た映画はとても長かった。", "The movie (　　) yesterday was very long.", "we", "saw", "seeing", "it"),
    ("私が先週読んだ本はあなたのものです。", "The book (　　) last week is yours.", "I", "read", "reading", "it"),
    ("トムが育てているトマトは大きい。", "The tomatoes (　　) are big.", "Tom", "grows", "growing", "them"),
    ("私がいちばん好きな教科は英語です。", "The subject (　　) the best is English.", "I", "like", "liking", "it"),
    ("父が使っているコンピューターは古い。", "The computer (　　) is old.", "my father", "uses", "using", "it"),
    ("私たちが毎朝乗るバスはいつも混んでいます。", "The bus (　　) every morning is always crowded.", "we", "take", "taking", "it"),
    ("これらは姉が作った人形です。", "These are the dolls (　　).", "my sister", "made", "making", "them"),
    ("ケンがかいた絵は美術館に展示されています。", "The picture (　　) is shown in the museum.", "Ken", "drew", "drawing", "it"),
]


@gen("basic_check", 4, ["concept", "computation"])
def contact(r):
    jp, s, subj, v, ing, pron = r.choice(CC)
    ok = f"{subj} {v}"
    why = {f"{v} {subj}": ("接触節は〈名詞＋主語＋動詞〉の語順。動詞を主語の前に置くと文が成り立たない。", "接触節の語順"),
           f"{subj} {ing}": ("主語の後ろには文の動詞の形（現在形・過去形）が必要。ing 形だけでは動詞にならない。", "接触節の動詞の形"),
           f"{subj} {v} {pron}": (f"前の名詞が {v} の目的語の役割をしているので、{pron} をもう一度書くと目的語が重なる。", "目的語の重複")}
    return mc(f"日本語に合うように、（　）に入る最も適切なものを選びなさい。\n{jp}\n{s}", [ok] + list(why),
              f"「（主語）が～する（した）（名詞）」は〈名詞＋主語＋動詞〉で表す。答え：{ok}", d=2,
              ap="日本語の「～が…した（する）」の部分を見つけ、名詞のすぐ後ろに〈主語＋動詞〉の順で置く。目的語は書かない。",
              steps=["説明される名詞を確認する。", f"「～が…した（する）」の部分を〈主語＋動詞〉にする：{subj} {v}。", "名詞が目的語の役割をするので it / them は書かない。", f"答え：{ok}"],
              alt=[f"2つの文に分けてみる（～. {cap(subj)} {v} {pron}.）と、前の名詞と {pron} が同じものだとわかる。"],
              pc=[("主語＋動詞の語順が正しい", 1), ("目的語を重ねていない", 1)],
              pit=["目的語の it を残す。", "動詞を ing 形にする。"], why=why)


# (文, 説明の語句, 説明される名詞, ほかの名詞3つ)
MOD = [
    ("The girl talking with my brother in the library is Aya.", "talking with my brother in the library", "girl", ["brother", "library", "Aya"]),
    ("I bought a bag made in Italy at the store.", "made in Italy", "bag", ["Italy", "store", "I"]),
    ("The man standing next to my father is a doctor.", "standing next to my father", "man", ["father", "doctor", "is"]),
    ("Have you read the letter written by Ms. Green?", "written by Ms. Green", "letter", ["Ms. Green", "you", "read"]),
    ("The cat sleeping under the table belongs to my aunt.", "sleeping under the table", "cat", ["table", "aunt", "my"]),
    ("We ate the cookies my grandmother baked.", "my grandmother baked", "cookies", ["grandmother", "We", "ate"]),
    ("The song we sang at the festival was popular.", "we sang at the festival", "song", ["festival", "we", "popular"]),
    ("The children playing in the river are my cousins.", "playing in the river", "children", ["river", "cousins", "my"]),
    ("This is a picture painted by a girl in my class.", "painted by a girl in my class", "picture", ["girl", "class", "This"]),
    ("The book my teacher gave me is about space.", "my teacher gave me", "book", ["teacher", "me", "space"]),
    ("Do you know the boy riding a bike near the station?", "riding a bike near the station", "boy", ["bike", "station", "you"]),
    ("The temple built by the people of this town is famous.", "built by the people of this town", "temple", ["people", "town", "famous"]),
]


@gen("basic_check", 3, ["concept", "computation"])
def modified(r):
    s, phrase, ok, others = r.choice(MOD)
    why = {w: (f"「{phrase}」は、すぐ前の名詞 {ok} を後ろから説明している。{w} は{'説明の語句の中にある語' if w in phrase.split() or w in phrase else '文のほかの部分の語'}で、説明される語ではない。", "後置修飾のかかり先")
           for w in others}
    return mc(f"次の英文で、「{phrase}」の部分が説明している語として最も適切なものを選びなさい。\n{s}", [ok] + others,
              f"分詞や〈主語＋動詞〉のまとまりは、すぐ前の名詞を後ろから説明する。答え：{ok}", d=1,
              ap="説明の語句の始まり（分詞、または主語＋動詞）を見つけ、そのすぐ前にある名詞を確かめる。",
              steps=[f"説明の語句「{phrase}」の始まりを見つける。", f"そのすぐ前の名詞は {ok}。", f"答え：{ok}"],
              alt=[f"「{phrase}」を日本語にして、「～している／された／（主語）が…した {ok}」と自然につながるかを確かめる。"],
              pc=[("説明の語句の始まりを見つけている", 1), ("説明される名詞を選んでいる", 1)],
              pit=["説明の語句の中にある名詞（library など）を選ぶ。", "文の主語や述語の語を選ぶ。"], why=why)


MEAN = [
    ("The boy reading a book over there is my cousin.", "向こうで本を読んでいる男の子は私のいとこです。",
     [("その男の子は向こうで私のいとこの本を読んでいます。", "文の動詞は is で、my cousin は「男の子がだれか」を表す。本の持ち主ではない。"),
      ("向こうで私のいとこが読んでいる本は男の子向けです。", "reading の主体は boy。説明される名詞を取り違えている。"),
      ("向こうで本を読んだ男の子は私のいとこでした。", "reading は「読んでいる」、is は現在。時制を取り違えている。")]),
    ("I have a watch made in Switzerland.", "私はスイスで作られた時計を持っています。",
     [("私はスイスで時計を作りました。", "made in Switzerland は watch を説明する部分。私が作ったのではない。"),
      ("私はスイスで作っている時計を持っています。", "made は過去分詞で「作られた」。「作っている」は making。"),
      ("私はスイスで時計を持っています。", "made in Switzerland（スイスで作られた）が訳されていない。")]),
    ("The language spoken in Brazil is Portuguese.", "ブラジルで話されている言語はポルトガル語です。",
     [("ブラジルではポルトガル語を話す言語がある。", "spoken in Brazil は language を説明する部分。文の骨組みは The language is Portuguese。"),
      ("ブラジルで話している言語はポルトガル語です。", "spoken は過去分詞で「話されている」。言語が話すのではない。"),
      ("ポルトガル語はブラジルで話されていない言語です。", "否定の語はない。意味が逆になっている。")]),
    ("The picture my sister drew won a prize.", "姉がかいた絵は賞をとりました。",
     [("姉は絵をかいて賞をとりました。", "my sister drew は picture を説明する部分（接触節）。賞をとったのは絵。"),
      ("その絵は姉をかいて賞をとりました。", "drew の主語は my sister。絵がかいたのではない。"),
      ("姉がかいている絵は賞をとるでしょう。", "drew は過去形、won も過去形。時制を取り違えている。")]),
    ("Who is the woman talking with Mr. Sato?", "佐藤先生と話している女性はだれですか。",
     [("その女性はだれと佐藤先生について話していますか。", "talking with Mr. Sato は woman を説明する部分。たずねているのは女性がだれか。"),
      ("佐藤先生はだれと話していますか。", "話している女性がだれかをたずねる文で、佐藤先生の相手をたずねる文ではない。"),
      ("佐藤先生に話しかけられた女性はだれですか。", "talking は「話している」。女性が話している側。")]),
    ("I found a wallet dropped on the street.", "私は通りに落とされていた財布を見つけました。",
     [("私は通りで財布を落としました。", "dropped on the street は wallet を説明する部分。財布を落としたのは私ではない。"),
      ("私は通りで財布を落としている人を見つけました。", "人を表す語は英文にない。dropped は wallet を説明している。"),
      ("私は財布を見つけて通りに落としました。", "dropped は文の動詞ではない。動作は found の1つだけ。")]),
    ("The students cleaning the classroom look busy.", "教室を掃除している生徒たちは忙しそうです。",
     [("生徒たちは教室を掃除して、忙しく見せています。", "cleaning the classroom は students を説明する部分で、文の動詞は look。"),
      ("掃除された教室の生徒たちは忙しそうです。", "cleaning は「掃除している」で、生徒が掃除する側。"),
      ("教室を掃除した生徒たちは忙しかった。", "cleaning は「掃除している」、look は現在。時制を取り違えている。")]),
    ("This is the dog my family has kept for ten years.", "これは私の家族が10年間飼っている犬です。",
     [("これは10年間私の家族を守っている犬です。", "my family has kept は dog を説明する接触節。主語は my family で、kept の目的語が dog。"),
      ("この犬は私の家族で、10年間飼われていません。", "否定の語はない。文の骨組みは This is the dog。"),
      ("これは私の家族が10年前に飼った犬です。", "has kept for ten years は「10年間ずっと飼っている」という継続。")]),
]


@gen("basic_check", 4, ["concept", "common_error"])
def meaning(r):
    en, ok, wrongs = r.choice(MEAN)
    return mc(f"次の英文の意味として最も適切なものを選びなさい。\n{en}", [ok] + [w for w, _ in wrongs],
              f"名詞を後ろから説明している部分をひとまとまりにして読むと、文の骨組みがわかる。答え：{ok}", d=2,
              ap="①文の動詞を見つける、②主語のまとまり（名詞＋説明の部分）の範囲を決める、③説明の部分を名詞の前に訳す。",
              steps=["文の動詞（is / won / look など）を見つける。", "名詞と、それを後ろから説明する部分のまとまりを決める。", f"説明の部分 → 名詞 → 文の残り、の順に訳す。答え：{ok}"],
              alt=["説明の部分を（　）でくくって取り除き、残った文の骨組み（The boy is my cousin. など）を先に訳してから説明を加える。"],
              pc=[("文の骨組みを読み取っている", 1), ("説明の部分の意味と時制を読み取っている", 1)],
              pit=["分詞を文の動詞のように訳す。", "説明される名詞を取り違える。"],
              why={w: (reason, "後置修飾の読み取り") for w, reason in wrongs})


# ======================================================================
# B 標準演習
# ======================================================================

COMB = [
    ("Look at the girl. She is dancing on the stage.", "Look at the girl dancing on the stage.", "現在分詞：She is を取り dancing on the stage を後ろに置く"),
    ("I have a bag. It was made in Italy.", "I have a bag made in Italy.", "過去分詞：It was を取り made in Italy を後ろに置く"),
    ("This is the cake. My mother made it.", "This is the cake my mother made.", "接触節：it を取り my mother made を後ろに置く"),
    ("The boy is my brother. He is swimming in the river.", "The boy swimming in the river is my brother.", "現在分詞：主語 the boy の後ろに swimming in the river"),
    ("I read a book. It was written by Natsume Soseki.", "I read a book written by Natsume Soseki.", "過去分詞：It was を取り written by Natsume Soseki"),
    ("The movie was exciting. We saw it last night.", "The movie we saw last night was exciting.", "接触節：it を取り we saw last night を the movie の後ろに"),
    ("Do you know the man? He is wearing a blue cap.", "Do you know the man wearing a blue cap?", "現在分詞：He is を取り wearing a blue cap"),
    ("The pictures are beautiful. They were taken by my uncle.", "The pictures taken by my uncle are beautiful.", "過去分詞：They were を取り taken by my uncle を主語の後ろに"),
    ("This is the bike. I bought it last month.", "This is the bike I bought last month.", "接触節：it を取り I bought last month"),
    ("I have an uncle. He is living in Osaka.", "I have an uncle living in Osaka.", "現在分詞：He is を取り living in Osaka"),
    ("The language is English. It is spoken in New Zealand.", "The language spoken in New Zealand is English.", "過去分詞：It is を取り spoken in New Zealand を主語の後ろに"),
    ("The song is very popular. Ken sang it at the party.", "The song Ken sang at the party is very popular.", "接触節：it を取り Ken sang at the party を主語の後ろに"),
    ("The dog is Emi's. It is running in the garden.", "The dog running in the garden is Emi's.", "現在分詞：It is を取り running in the garden を主語の後ろに"),
    ("I found a key. It was lost by my sister.", "I found a key lost by my sister.", "過去分詞：It was を取り lost by my sister"),
]


@gen("standard_practice", 5, ["computation", "application"])
def combine(r):
    two, ans, pt = r.choice(COMB)
    return sa(f"次の2つの英文を、分詞による修飾または接触節を使って1つの文にしなさい。\n{two}", ans, f"{pt}。答え：{ans}", d=2, p=4,
              ap="2つ目の文の代名詞（he / she / it / they）が、1つ目の文のどの名詞を指すかを確かめる。そのうえで「主語＋be 動詞」または「目的語」を取り除き、残りを名詞の後ろに置く。",
              steps=["2つ目の文の代名詞が指す名詞を見つける。", "進行形なら主語＋be 動詞を取って ing 形、受け身なら主語＋be 動詞を取って過去分詞、ふつうの文で目的語なら目的語を取って接触節にする。", "残った部分を名詞のすぐ後ろに置く。", f"答え：{ans}"],
              alt=["完成した文を日本語に訳し、もとの2つの文の内容がすべて入っているかを確かめる。"],
              pc=[("形（現在分詞・過去分詞・接触節）を正しく選んでいる", 2), ("名詞の後ろの語順・文の動詞の位置が正しい", 2)],
              pit=["be 動詞を残してしまう（the boy is swimming ～ is ～）。", "接触節で it を残す。"])


@gen("standard_practice", 4, ["computation", "condition_check"])
def fill_form(r):
    s, jp, base, ing, pp, fin, k = r.choice(P)
    head = p_head(s)
    ok = ing if k == "ing" else pp
    stem = s.replace("(　　)", f"(　　)〔{base}〕")
    return sa(f"日本語に合うように、〔　〕内の動詞を適切な形にかえて（　）に入れなさい。\n{jp}\n{stem}", ok,
              f"{head} は動作を{'する側なので現在分詞' if k == 'ing' else 'される側なので過去分詞'} {ok}。", d=2, p=4,
              ap=f"{head} を主語にした文を作ると、進行形（{cap(head)} is {ing} ～）と受け身（{cap(head)} was {pp} ～）のどちらが日本語に合うかを考える。",
              steps=[f"説明される名詞は {head}。", f"{head} は動作を{'する' if k == 'ing' else 'される'}側。", f"{'現在分詞' if k == 'ing' else '過去分詞'}にする：{ok}"],
              alt=["日本語の「～している」「～された・～されている」にも注目して確かめる（ただし日本語の「た」だけで判断しない）。"],
              pc=[("ing 形か過去分詞かを正しく判断している", 2), ("つづりが正しい", 2)],
              pit=["過去分詞の代わりに過去形を書く（wrote）。", "ing 形のつづり（running, swimming）を誤る。"])


ORDERS = [
    ("ピアノをひいている女の子は私の妹です。", ["the girl", "playing", "the piano", "is", "my", "sister"]),
    ("これは日本で作られたカメラです。", ["this", "is", "a camera", "made", "in", "Japan"]),
    ("私が昨日買った本はとてもおもしろい。", ["the book", "I", "bought", "yesterday", "is", "very", "interesting"]),
    ("木の下で眠っているネコを見て。", ["look", "at", "the cat", "sleeping", "under", "the tree"]),
    ("これは夏目漱石によって書かれた本です。", ["this", "is", "a book", "written", "by", "Natsume Soseki"]),
    ("あなたが話していた男の子はだれですか。", ["who", "is", "the boy", "you", "were", "talking", "with"]),
    ("カナダで話されている言語は何ですか。", ["what", "are", "the languages", "spoken", "in", "Canada"]),
    ("私には東京に住んでいるおじがいます。", ["I", "have", "an uncle", "living", "in", "Tokyo"]),
    ("父がとった写真はとても美しい。", ["the pictures", "my father", "took", "are", "very", "beautiful"]),
    ("校門のそばに立っている先生は田中先生です。", ["the teacher", "standing", "by", "the school gate", "is", "Mr. Tanaka"]),
    ("これは祖母が私にくれた時計です。", ["this", "is", "the watch", "my grandmother", "gave", "me"]),
    ("英語で書かれたその手紙は読みやすかった。", ["the letter", "written", "in English", "was", "easy", "to read"]),
]


@gen("standard_practice", 4, ["application", "computation"])
def build_order(r):
    jp, parts = r.choice(ORDERS)
    sent = cap(" ".join(parts)) + ("?" if jp.endswith("か。") else ".")
    return order(f"日本語に合うように、次の語句を並べかえて英文を完成させなさい。ただし、文頭にくる語も小文字で示してある。\n{jp}", parts,
                 f"{sent}　ポイント：名詞を先に置き、その後ろに分詞＋語句（または主語＋動詞）を続ける。文の動詞はそのあと。", d=2, p=4,
                 ap="まず文の骨組み（主語＋動詞）を日本語から取り出し、説明される名詞の後ろに説明の語句を入れる。",
                 steps=["文の骨組み（だれが・どうする／何が・どうだ）を決める。", "説明される名詞を見つけ、その後ろに分詞＋語句、または主語＋動詞を置く。", "文の動詞と残りの語句を続ける。", f"完成文：{sent}"],
                 alt=["説明の部分を取り除いた短い文（The girl is my sister. など）が成り立つかを確かめる。"],
                 pc=[("名詞と説明の部分の語順が正しい", 2), ("文の動詞と残りの語句の位置が正しい", 2)],
                 pit=["日本語の語順のまま、説明の部分を名詞の前に置く。", "文の動詞を説明の部分より前に置く。"])


# (もとの文, 名詞のまとまり, 日本語, 種類)
CROSS = [
    ("The boy is running in the park.", "the boy running in the park", "公園で走っている男の子", "prog"),
    ("The letter was written in English.", "the letter written in English", "英語で書かれた手紙", "pass"),
    ("The girl is singing on the stage.", "the girl singing on the stage", "ステージで歌っている女の子", "prog"),
    ("The cars were made in Japan.", "the cars made in Japan", "日本で作られた車", "pass"),
    ("The baby is sleeping in the bed.", "the baby sleeping in the bed", "ベッドで眠っている赤ちゃん", "prog"),
    ("The window was broken by Tom.", "the window broken by Tom", "トムに割られた窓", "pass"),
    ("The man is waiting for a bus.", "the man waiting for a bus", "バスを待っている男性", "prog"),
    ("The pictures were taken in Hokkaido.", "the pictures taken in Hokkaido", "北海道でとられた写真", "pass"),
    ("The students are cleaning the classroom.", "the students cleaning the classroom", "教室を掃除している生徒たち", "prog"),
    ("The song is loved by many people.", "the song loved by many people", "多くの人に愛されている歌", "pass"),
    ("The dog is swimming in the river.", "the dog swimming in the river", "川で泳いでいる犬", "prog"),
    ("The bike was stolen last night.", "the bike stolen last night", "昨夜盗まれた自転車", "pass"),
]


@gen("standard_practice", 4, ["cross_unit", "concept"], rel=["JH-ENG-G2-U05", "JH-ENG-G1-U04"])
def from_sentence(r):
    s, ans, jp, k = r.choice(CROSS)
    form = "現在進行形（be＋ing 形）" if k == "prog" else "受け身（be＋過去分詞）"
    return sa(f"次の英文をもとに、「{jp}」という意味の名詞のまとまりを英語で書きなさい。また、もとの文が何という形の文かも答えなさい。\n{s}",
              f"{ans}（もとの文は{form}）", f"もとの文の be 動詞を取り除くと、{'ing 形' if k == 'prog' else '過去分詞'}以下が名詞を後ろから説明する形になる。答え：{ans}", d=2, p=4,
              v=[ans, cap(ans)],
              ap="もとの文が進行形か受け身かを確かめ、主語のすぐ後ろの be 動詞だけを取り除く。",
              steps=[f"もとの文は{form}。", "主語の後ろの be 動詞を取り除く。", f"残った形が名詞のまとまりになる：{ans}"],
              alt=["できた名詞のまとまりに be 動詞をもどすと、もとの文にもどることを確かめる。"],
              pc=[("名詞のまとまりを正しく書いている", 3), ("もとの文の形を答えている", 1)],
              pit=["be 動詞を残して文のままにする。", "進行形の文から過去分詞を作るなど、形を取り違える。"])


PEOPLE = [
    ("Ken", "boy", "walking a dog", "犬を散歩させている"), ("Taro", "boy", "riding a bike", "自転車に乗っている"),
    ("Jun", "boy", "playing the guitar", "ギターをひいている"), ("Sota", "boy", "eating an ice cream", "アイスクリームを食べている"),
    ("Aya", "girl", "reading a book", "本を読んでいる"), ("Emi", "girl", "taking pictures", "写真をとっている"),
    ("Yumi", "girl", "playing badminton", "バドミントンをしている"), ("Mika", "girl", "drawing a picture", "絵をかいている"),
    ("Mr. Brown", "man", "sitting on a bench", "ベンチに座っている"), ("Mr. Ito", "man", "running with a dog", "犬と走っている"),
    ("Ms. Green", "woman", "talking on the phone", "電話で話している"), ("Ms. Ono", "woman", "buying flowers", "花を買っている"),
]
NOUN_JP = {"boy": "男の子", "girl": "女の子", "man": "男性", "woman": "女性"}


@gen("standard_practice", 3, ["application", "concept"])
def who_is(r):
    g = r.choice(["boy", "girl", "man", "woman"])
    same = [p for p in PEOPLE if p[1] == g]
    target = r.choice(same)
    others = [p for p in same if p != target]
    pool = [p for p in PEOPLE if p != target]
    rest = r.sample(others, min(1, len(others))) + r.sample([p for p in pool if p not in others], 2)
    shown = [target] + rest
    order_ = shown[:]
    r.shuffle(order_)
    lines = "\n".join(f"・{p[0]}：{p[3]}" for p in order_)
    why = {p[0]: (f"{p[0]} は{p[3]}{NOUN_JP[p[1]]}。質問は {target[2]} の{NOUN_JP[g]}。", "分詞の意味の読み取り") for p in rest}
    return mc(f"公園にいる人たちと、その人たちがしていることを日本語でまとめたメモがある。メモを見て、英語の質問の答えとして最も適切なものを選びなさい。\n{lines}\n質問：Who is the {g} {target[2]}?",
              [target[0]] + [p[0] for p in rest],
              f"the {g} {target[2]} は「{target[3]}{NOUN_JP[g]}」。メモから {target[0]}。", d=2,
              ap=f"質問の the {g} の後ろの {target[2].split()[0]} 以下が、どんな{NOUN_JP[g]}かを説明している。その意味をメモと照らし合わせる。",
              steps=[f"説明される名詞は {g}（{NOUN_JP[g]}）。", f"説明の部分 {target[2]} ＝「{target[3]}」。", f"メモから答えを探す：{target[0]}。"],
              alt=[f"答えを入れて文にする（{target[0]} is {target[2]}.）と、メモの内容と一致するかを確かめられる。"],
              pc=[("説明の部分の意味を読み取っている", 2), ("メモと照らし合わせて正しく答えている", 1)],
              pit=["the のすぐ後ろの名詞（boy / girl）だけを見て、説明の部分を読まない。", "動作の内容を取り違える。"], why=why)


# ======================================================================
# C 思考力・記述応用
# ======================================================================

PAIRS = [
    ("The girl is talking with Ken.", "The girl talking with Ken is Aya.",
     "A は is がある現在進行形の文で、「その女の子はケンと話している」と述べている。B では talking with Ken が girl を後ろから説明する名詞のまとまり（ケンと話している女の子）になり、文の動詞は is で「ケンと話している女の子はアヤだ」という意味になる。"),
    ("the boy painting a picture", "the picture painted by the boy",
     "A は現在分詞 painting で、boy が絵を「かいている」側であることを表し「絵をかいている男の子」。B は過去分詞 painted で、picture が「かかれた」側であることを表し「その男の子によってかかれた絵」。説明される名詞が動作をする側かされる側かで分詞の形が変わる。"),
    ("a sleeping baby", "a baby sleeping on the sofa",
     "どちらも「眠っている赤ちゃん」だが、A は分詞 sleeping が1語なので名詞の前に置いている。B は sleeping on the sofa のように語句がついているので名詞の後ろに置き、「ソファーで眠っている赤ちゃん」となる。"),
    ("The car was made in Japan.", "a car made in Japan",
     "A は was がある受け身の文で「その車は日本で作られた」という文。B は be 動詞がなく、過去分詞 made in Japan が car を後ろから説明する名詞のまとまりで「日本で作られた車」。B は文の主語や目的語として使う。"),
    ("This is the picture my father took.", "This is the picture taken by my father.",
     "どちらも「これは父がとった写真だ」という内容。A は接触節 my father took で、主語 my father と動詞 took を名詞の後ろに置いている。B は過去分詞 taken by my father で、picture が「とられた」側として説明している。A は父を主語にした言い方、B は写真を中心にした受け身の言い方。"),
    ("an exciting game", "an excited boy",
     "A の exciting は「（人を）わくわくさせる」という意味で、game が人をわくわくさせる側なので現在分詞を使う（わくわくする試合）。B の excited は「わくわくさせられた」という意味で、boy が気持ちを受ける側なので過去分詞を使う（わくわくしている男の子）。"),
    ("I know the boy playing tennis.", "I know the boy plays tennis.",
     "A は playing tennis が boy を後ろから説明し「私はテニスをしている男の子を知っている」という意味。B は that が省略された形で「私はその男の子がテニスをすることを知っている」という意味になり、plays は boy を主語とする文の動詞。ing 形か動詞の形（plays）かで文の組み立てが変わる。"),
    ("the letter I wrote", "the letter written to me",
     "A は接触節で、I wrote が letter を説明し「私が書いた手紙」。B は過去分詞 written to me が letter を説明し「私にあてて書かれた手紙」。A は書いた人が私、B は受け取る人が私で、手紙を書いた人はほかの人である。"),
]


@gen("thinking_writing", 4, ["written_reasoning", "concept"])
def explain_pair(r):
    a, b, model = r.choice(PAIRS)
    return desc(f"次の英語 A・B の意味や組み立ての違いを、分詞の形・位置や文の動詞に注目して日本語で説明しなさい。\nA：{a}\nB：{b}", model,
                "be 動詞の有無で文か名詞のまとまりかが決まり、名詞が動作をする側なら現在分詞、される側なら過去分詞を使う。語句がつく分詞は名詞の後ろに置く。",
                [("A の組み立てと意味を正しく説明している", 3), ("B の組み立てと意味を正しく説明している", 3), ("違いを生む部分（分詞の形・位置・be 動詞・接触節など）を指摘している", 2)], d=3, p=8, lines=5,
                ap="A と B で違う部分に印をつけ、①文か名詞のまとまりか、②名詞が動作をする側かされる側か、③説明が名詞の前か後ろか、を確かめる。",
                steps=["A と B を見比べ、違う部分を見つける。", "それぞれの組み立て（文の動詞・説明される名詞・分詞の形）を確認する。", "和訳を示して違いを説明する。"],
                alt=["説明される名詞を主語にした文（進行形・受け身）に書きかえて比べると、違いを説明しやすい。"],
                pc=[("A の説明", 3), ("B の説明", 3), ("違いの指摘", 2)],
                pit=["和訳だけを書き、どの形が違いを生んでいるかを書かない。", "現在分詞と過去分詞の違いを「現在と過去」の時間の違いと説明する。"])


CHOOSE = [
    ("the window (break) by the ball", "broken", "window を主語にすると The window was broken by the ball. という受け身になる。窓は割られる側なので過去分詞。"),
    ("the children (play) in the snow", "playing", "children を主語にすると The children are playing in the snow. という進行形になる。子どもたちは遊んでいる側なので現在分詞。"),
    ("a language (speak) in many countries", "spoken", "language を主語にすると The language is spoken in many countries. という受け身になる。言語は話される側なので過去分詞。"),
    ("the woman (wait) at the bus stop", "waiting", "woman を主語にすると The woman is waiting at the bus stop. という進行形になる。女性は待っている側なので現在分詞。"),
    ("a house (build) 100 years ago", "built", "house を主語にすると The house was built 100 years ago. という受け身になる。家は建てられる側なので過去分詞。"),
    ("the bird (sing) in the tree", "singing", "bird を主語にすると The bird is singing in the tree. という進行形になる。鳥は歌っている側なので現在分詞。"),
    ("the dishes (wash) by my father", "washed", "dishes を主語にすると The dishes were washed by my father. という受け身になる。皿は洗われる側なので過去分詞。"),
    ("a girl (wear) a yellow dress", "wearing", "girl を主語にすると The girl is wearing a yellow dress. という進行形になる。女の子は着ている側なので現在分詞。"),
    ("the money (steal) from the shop", "stolen", "money を主語にすると The money was stolen from the shop. という受け身になる。お金は盗まれる側なので過去分詞。"),
    ("the train (leave) for Osaka", "leaving", "train を主語にすると The train is leaving for Osaka. という進行形になる。電車は出発する側なので現在分詞。"),
]


@gen("thinking_writing", 3, ["condition_check", "written_reasoning"])
def choose_explain(r):
    s, ans, why_s = r.choice(CHOOSE)
    return desc(f"次の名詞のまとまりの（　）内の動詞を、現在分詞（ing 形）か過去分詞のどちらか適切な形にしなさい。また、その形を選んだ理由を、説明される名詞と動詞の関係から説明しなさい。\n{s}",
                f"{ans}　理由：{why_s}",
                "説明される名詞を主語にした文を作り、進行形（する側）になれば現在分詞、受け身（される側）になれば過去分詞を使う。",
                [("正しい形を書いている", 4), ("名詞を主語にした文（進行形・受け身）を示すなど、関係を説明している", 3), ("つづりが正しい", 1)], d=4, p=8, lines=4,
                ap="説明される名詞（前の名詞）を主語にして文を作ってみる。進行形と受け身のどちらが自然かを考える。",
                steps=["説明される名詞を確認する。", "その名詞を主語にした文を作り、進行形か受け身かを判断する。", f"答え：{ans}"],
                alt=["by ～（～によって）がある場合は受け身の目印になるので、過去分詞を選ぶ根拠として使える。"],
                pc=[("形", 4), ("理由の説明", 3), ("つづり", 1)],
                pit=["「過去のことだから過去分詞」と時間で判断する。", "名詞と動詞の関係を逆にとらえる。"])


WRITE = [
    ("クラスの集合写真を見せながら、写っている友だちを紹介する。",
     "The boy standing next to me is Ken. The girl holding a flag is Aya.",
     "現在分詞 standing next to me と holding a flag で、それぞれの人を後ろから説明している。"),
    ("家にある大切な物を ALT の先生に紹介する。",
     "This is a watch made in Switzerland. It is the watch my grandfather gave me.",
     "1文目は過去分詞 made in Switzerland、2文目は接触節 my grandfather gave me で時計を説明している。"),
    ("修学旅行の写真を見せながら、思い出を話す。",
     "This is a temple built about 600 years ago. The picture I took there is my favorite.",
     "1文目は過去分詞 built about 600 years ago、2文目は接触節 I took there で名詞を説明している。"),
    ("好きな本を友だちにすすめる。",
     "This is a book written by a young Japanese writer. The story I like the best is about a boy living in a small town.",
     "過去分詞 written by ～、接触節 I like the best、現在分詞 living in a small town を使っている。"),
    ("公園の様子を、絵を見ていない人に電話で伝える。",
     "There is a man running with his dog. The children playing near the pond look very happy.",
     "現在分詞 running with his dog と playing near the pond で、人の様子を説明している。"),
    ("学校の文化祭で展示する作品を説明する。",
     "These are pictures painted by the students in our class. The picture my friend painted won a prize.",
     "過去分詞 painted by ～ と接触節 my friend painted で、作品を説明している。"),
    ("自分の町の名物料理を留学生に紹介する。",
     "This is a dish loved by the people in my town. The fish used in it is caught in the sea near here.",
     "過去分詞 loved by ～ と used in it で、料理と材料を説明している。"),
    ("部活動の仲間を新入生に紹介する。",
     "The girl wearing glasses is our captain. The boy she is talking with is our best player.",
     "現在分詞 wearing glasses と接触節 she is talking with で、2人の人物を説明している。"),
]


@gen("thinking_writing", 3, ["application", "written_reasoning"])
def write_describe(r):
    sit, model, point = r.choice(WRITE)
    return desc(f"次の場面で伝える英文を2文で書きなさい。ただし、2文とも名詞を後ろから説明する形（現在分詞・過去分詞・接触節のいずれか）を1つ以上使うこと。\n場面：{sit}",
                f"（解答例）{model}", f"（解答例の解説）{point} 説明される名詞のすぐ後ろに説明の部分を置き、文の動詞はそのあとに続けている。",
                [("1文目で後置修飾を正しく使い、場面に合っている", 3), ("2文目で後置修飾を正しく使い、内容がつながっている", 3), ("分詞のつづり・文の動詞の数（単数・複数）が正しい", 2)], d=4, p=8, lines=4,
                ap="伝えたい人や物（名詞）を決め、それを「何をしている」「何をされた」「だれが～した」で説明する。説明は名詞の後ろに置く。",
                steps=["説明したい名詞と、その説明（する側・される側・だれが～した）を日本語で決める。", "名詞＋分詞＋語句、または名詞＋主語＋動詞の形にする。", "文の動詞（is / are など）を説明される名詞に合わせて続ける。"],
                alt=["書いた文から説明の部分を取り除き、残った文（The boy is Ken. など）が正しいかを確かめる。"],
                pc=[("1文目", 3), ("2文目", 3), ("表記の正確さ", 2)],
                pit=["説明の部分に be 動詞を入れて、文の動詞が2つになる。", "接触節に it を残す。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(task, wrong, step, etype, tempt, fix, expl, steps, ap, alt, pit):
    return desc(f"{task}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい英文に書き直しなさい。", fix, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい英文に直している", 3), ("文法のルールを説明している", 1)], d=3, p=6, lines=4,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい英文", 3), ("ルールの説明", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix))


FORM_ERR = [
    ("川で泳いでいる男の子を見て。", "Look at the boy swam in the river.", "Look at the boy swimming in the river.", "swam", "concept",
     "男の子は「泳いでいる」側なので現在分詞 swimming。swam は過去形で、文の動詞が2つになってしまう。", "日本語の「泳いで」を過去の動作と考えた。"),
    ("これは日本で作られた車です。", "This is a car making in Japan.", "This is a car made in Japan.", "making", "concept",
     "車は「作られる」側なので過去分詞 made。making では「（何かを）作っている車」になる。", "分詞はいつも ing 形だと考えた。"),
    ("ピアノをひいている女の子は私の姉です。", "The girl played the piano is my sister.", "The girl playing the piano is my sister.", "played", "concept",
     "女の子は「ひいている」側なので現在分詞 playing。played では「ひかれた女の子」の意味になる。", "日本語の「～た」と「～ている」を区別しなかった。"),
    ("私は夏目漱石によって書かれた本を持っています。", "I have a book writing by Natsume Soseki.", "I have a book written by Natsume Soseki.", "writing", "concept",
     "本は「書かれる」側なので過去分詞 written。by ～ があるのも受け身の目印。", "書く動作を ing 形で表そうとした。"),
    ("メキシコで話されている言語はスペイン語です。", "The language speaking in Mexico is Spanish.", "The language spoken in Mexico is Spanish.", "speaking", "concept",
     "言語は「話される」側なので過去分詞 spoken。", "日本語の「話されている」の「ている」につられて ing 形にした。"),
    ("門のところに立っている女性は私のおばです。", "The woman is standing at the gate is my aunt.", "The woman standing at the gate is my aunt.", "is standing", "logic",
     "is standing があると文の動詞が2つになる。名詞を説明する部分には be 動詞を入れず、standing at the gate だけを置く。", "「立っている」を進行形 is standing で表そうとした。"),
    ("これらは父によってとられた写真です。", "These are pictures took by my father.", "These are pictures taken by my father.", "took", "formula",
     "名詞を説明するのは過去分詞。take の過去分詞は taken。took は過去形。", "過去形と過去分詞を区別していなかった。"),
    ("赤い帽子をかぶっている男の子はケンです。", "The boy wearing a red cap are Ken.", "The boy wearing a red cap is Ken.", "are", "condition",
     "文の主語は The boy（単数）なので be 動詞は is。説明の部分は動詞の数に関係しない。", "主語のまとまりが長く、複数のように感じた。"),
    ("トムと話している女の子を知っていますか。", "Do you know the girl talked with Tom?", "Do you know the girl talking with Tom?", "talked", "concept",
     "女の子は「話している」側なので現在分詞 talking。", "日本語の「話して」を過去形にした。"),
    ("母が焼いたパンはとてもおいしい。", "The bread baking by my mother is very good.", "The bread baked by my mother is very good.", "baking", "concept",
     "パンは「焼かれる」側なので過去分詞 baked。by my mother も受け身の目印。", "「焼いた」を ing 形で表そうとした。"),
]


@gen("error_correction", 5, ["common_error", "condition_check"])
def err_form(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(FORM_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", etype, tempt, fix, f"{rule}正しくは {fix}",
                    ["説明される名詞が動作をする側か、される側かを確認する。", f"「{where}」の部分の誤りを見つける：{rule}", f"正しい英文：{fix}"],
                    "後置修飾では、①名詞が動作をする側なら ing 形・される側なら過去分詞、②説明の部分に be 動詞を入れない、③文の動詞は説明される名詞に合わせる、の3点を確かめる。",
                    ["説明される名詞を主語にした文（進行形・受け身）を作って、分詞の形が正しいかを確かめる。"],
                    ["名詞と動作の関係を確かめずに分詞を選ぶ。", "説明の部分に be 動詞を残す。"])


USE_ERR = [
    ("これは私が昨日買った本です。", "This is the book I bought it yesterday.", "This is the book I bought yesterday.", "it", "logic",
     "the book が bought の目的語の役割をしているので、it をもう一度書くと目的語が重なる。", "bought の後ろには目的語が必要だと考えた。"),
    ("母が作ったケーキはとてもおいしかった。", "The cake my mother made it was delicious.", "The cake my mother made was delicious.", "it", "logic",
     "the cake が made の目的語の役割をしているので、it は不要。", "made の後ろに目的語が必要だと考えた。"),
    ("これは兄がとった写真です。", "This is the picture took my brother.", "This is the picture my brother took.", "took my brother", "notation",
     "接触節は〈名詞＋主語＋動詞〉の語順。my brother took にする。", "日本語の「とった兄」の順に引きずられた。"),
    ("私たちが昨夜見た映画はわくわくした。", "The movie we saw it last night was exciting.", "The movie we saw last night was exciting.", "it", "logic",
     "the movie が saw の目的語の役割をしているので、it は不要。", "saw の後ろに目的語が必要だと考えた。"),
    ("私は公園で走っている犬を見ました。", "I saw a running in the park dog.", "I saw a dog running in the park.", "a running in the park dog", "notation",
     "分詞に語句（in the park）がつくときは、名詞の後ろに置く。", "日本語と同じ語順で、説明を名詞の前に置いた。"),
    ("サッカーをしている生徒たちは私のクラスメートです。", "The students playing soccer is my classmates.", "The students playing soccer are my classmates.", "is", "condition",
     "文の主語は The students（複数）なので be 動詞は are。", "soccer（単数）の直後なので is にした。"),
    ("これは父が昨年買った車です。", "This is the car my father buying last year.", "This is the car my father bought last year.", "buying", "concept",
     "接触節は〈名詞＋主語＋動詞〉。主語 my father の後ろには文の動詞の形（ここでは過去形 bought）を置く。ing 形だけでは動詞にならない。", "現在分詞による修飾と混同した。"),
    ("私が話した女の子はアヤです。", "The girl I talked is Aya.", "The girl I talked with is Aya.", "talked", "logic",
     "「～と話す」は talk with ～。the girl が with の目的語にあたるので、with を残して I talked with とする。", "日本語の「話した女の子」には「と」がないので、with を落とした。"),
    ("私には大阪に住んでいるおばがいます。", "I have an aunt lives in Osaka.", "I have an aunt living in Osaka.", "lives", "concept",
     "lives にすると文の動詞が have と lives の2つになる。名詞を説明するのは現在分詞 living。", "「住んでいる」を現在形の動詞で表した。"),
]


@gen("error_correction", 5, ["common_error", "computation"])
def err_usage(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(USE_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", etype, tempt, fix, f"{rule}正しくは {fix}",
                    ["説明の部分の位置（名詞の前か後ろか）と語順を確認する。", "接触節で目的語が重なっていないか、文の動詞の数が主語に合っているかを確認する。", f"正しい英文：{fix}"],
                    "後置修飾の文では、説明される名詞・説明の部分・文の動詞の3つに分けて確かめる。接触節では前の名詞が目的語の役割をする。",
                    ["説明の部分を（　）でくくって取り除き、残った文が正しく成り立つかを確かめる。"],
                    ["接触節に it / them を残す。", "主語のまとまりの最後の語につられて、文の動詞の数を誤る。"])


GENERATORS = [ing_or_pp, position, contact, modified, meaning,
              combine, fill_form, build_order, from_sentence, who_is,
              explain_pair, choose_explain, write_describe,
              err_form, err_usage]
