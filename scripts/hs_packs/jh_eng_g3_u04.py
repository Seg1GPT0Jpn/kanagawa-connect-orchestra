"""単元パック：中学3年 英語 間接疑問文と文構造。"""
from banks._common import desc, mc, order, sa
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem,
                         tp)

UNIT_ID = "JH-ENG-G3-U04"

PREREQUISITES = [
    ("JH-ENG-G1-U03", "疑問詞（what / where / when / who / how など）を使った疑問文。間接疑問文は、この疑問文の語順を〈疑問詞＋主語＋動詞〉に組みかえて作る。"),
    ("JH-ENG-G2-U02", "不定詞〈to＋動詞の原形〉。It is ～ for … to ―. や want / tell ＋人＋to ～ は不定詞の使い方の発展。"),
    ("JH-ENG-G1-U02", "人称代名詞の目的格（me / him / her / us / them）。SVOO・SVOC や for … の「…」には目的格を使う。"),
    ("JH-ENG-G2-U03", "接続詞 because。It is ～ for … to ―. で意見を述べ、because で理由をそえる。"),
]
EXTENSIONS = [
    ("JH-ENG-G3-U07", "条件英作文で、It is important for us to ～ because …. の形で意見と理由を書いたり、Could you tell me where ～? と丁寧にたずねたりする。"),
    ("JH-ENG-G3-U06", "長文読解で、SVOC（make A B）や間接疑問文をふくむ文の意味を正確にとる。"),
    ("HS-ENG-U01", "高校では、5文型として文の構造を整理し、知覚動詞・使役動詞（have / get）や whether / if を使った間接疑問へ広げる。"),
]


def cap(s):
    return s[0].upper() + s[1:]


# ======================================================================
# 授業プリント
# ======================================================================

LESSON = lesson(
    goals=["疑問詞で始まる疑問文を、文の一部として〈疑問詞＋主語＋動詞〉の語順（間接疑問文）で使える。",
           "SVOO（give A B）と SVOC（make A B / call A B）の文を、語順と意味の関係から区別して使える。",
           "It is ～ for … to ―.、want / tell / ask ＋人＋to ～、let / make / help ＋人＋動詞の原形 を正しい形で使える。"],
    duration=100,
    readiness=["疑問詞を使った疑問文（Where do you live? など）を正しい語順で作れる（中1）。",
               "不定詞〈to＋動詞の原形〉の名詞的・副詞的用法を理解している（中2）。",
               "人称代名詞の目的格（me / him / her / us / them）を使える（中1）。",
               "小学校の外国語で Where is ～? / What do you want? などのやり取りに慣れている。"],
    flow=[("導入：文の中に入る疑問文", 8, "Where is the station? と Do you know where the station is? を比べ、語順の変化に気づかせる"),
          ("間接疑問文", 20, "疑問詞＋主語＋動詞。do / does / did の消え方と動詞の形、疑問詞が主語の場合（例題1）"),
          ("SVOO と SVOC", 22, "give A B（A に B を）と make A B（A を B に）。to / for を使った言いかえ（例題2）"),
          ("不定詞を使った文構造", 25, "It is ～ for … to ―.、want / tell ＋人＋to ～、let / make / help ＋人＋原形（例題3）"),
          ("練習とまとめ", 25, "板書の3列で整理し、言いかえ・並べかえ練習、確認問題3問")],
    sections=[
        intro("in1", "英語の文の「骨組み」を見る",
              "英語は語順で意味が決まる言葉です。同じ make でも、She made a cake.（ケーキを作った）、She made me a cake.（私にケーキを作ってくれた）、She made me happy.（私を幸せにした）と、後ろに続く語の並び方で意味が変わります。また、Where is the station? という疑問文も、Do you know ～? の中に入れると Do you know where the station is? と語順が変わります。この単元では、こうした文の骨組み（文構造）を整理します。",
              bullets=["Where is the station?（駅はどこですか：ふつうの疑問文）",
                       "Do you know where the station is?（駅がどこにあるか知っていますか：間接疑問文）",
                       "She made me a cake.（私にケーキを作ってくれた：SVOO）",
                       "She made me happy.（私を幸せにした：SVOC）"],
              points=[tp("4つの例文を並べて板書し、「どの語の位置が変わったか」「何が増えたか」を生徒に見つけさせてから単元のテーマを示す。",
                         ask="Where is the station? と where the station is では何が違うか。", expect="is と the station の順番が入れかわっている。",
                         timing="導入の冒頭")]),
        definition("df1", "間接疑問文〈疑問詞＋主語＋動詞〉",
                   "疑問詞で始まる疑問文を、Do you know ～? / I don't know ～. / Please tell me ～. などの文の一部（目的語）として入れたものを間接疑問文といいます。疑問詞の後ろは、ふつうの文と同じ〈主語＋動詞〉の語順になります。",
                   formula="疑問詞＋主語＋動詞 ～（疑問文の語順にしない）",
                   bullets=["Where does he live? → Do you know where he lives?（does が消え、live に s がつく）",
                            "What is this? → I don't know what this is.（be 動詞は主語の後ろへ）",
                            "When did she come? → Please tell me when she came.（did が消え、come が過去形 came に）",
                            "Who made this cake? → Do you know who made this cake?（疑問詞が主語なので語順はそのまま）"],
                   conditions=["do / does / did は間接疑問文では使わない。そのぶん、動詞を主語と時制に合わせた形（lives / came）にする。",
                               "How old / What time / How many＋名詞 などは、ひとかたまりのまま先頭に置く：how old your sister is。",
                               "文の終わりの記号は、全体の文に合わせる（Do you know ～? は ?、I don't know ～. は .）。"],
                   points=[tp("does / did が消えるとき、その「三単現」「過去」の情報が動詞に移ることを、矢印で見せる。",
                              ask="Where does he live? の does の s はどこへ行ったか。", expect="live について lives になった。",
                              caution="where he live のように s を落とす誤りがとても多い。", timing="定義の説明後")]),
        definition("df2", "SVOO と SVOC",
                   "動詞の後ろに語が2つ並ぶ文には、2つの型があります。SVOO は「A に B を～する」で A ≠ B（人と物）、SVOC は「A を B に（と）する」で A ＝ B の関係があります。",
                   formula="SVOO：動詞＋A（人）＋B（物）〔A ≠ B〕　｜　SVOC：動詞＋A＋B〔A ＝ B〕",
                   bullets=["SVOO：My aunt gave me a watch.（おばは私に時計をくれた）→ My aunt gave a watch to me.",
                            "SVOO：My father bought me a bike. → My father bought a bike for me.",
                            "SVOC：We call our dog Kuro.（私たちは犬をクロと呼ぶ：our dog ＝ Kuro）",
                            "SVOC：The news made us sad.（その知らせは私たちを悲しくさせた：us ＝ sad）"],
                   conditions=["SVOO を〈物＋to / for＋人〉に言いかえるとき、give / show / tell / send / teach / lend は to、buy / make / cook / get は for。",
                               "SVOC の動詞は make（A を B にする）・call（A を B と呼ぶ）・name（A を B と名づける）・keep（A を B に保つ）など。",
                               "A の位置の代名詞は目的格（me / us / him）。"],
                   points=[tp("A と B の間に is を入れて意味が通れば SVOC（us is sad → 私たちが悲しい）、通らなければ SVOO（me is a watch ×）と確かめさせる。",
                              ask="She made him a cake. と She made him happy. で、him ＝ ? が成り立つのはどちらか。", expect="him ＝ happy の後者。後者が SVOC。")]),
        theorem("th1", "不定詞・原形不定詞を使う文構造",
                "It is ～ for … to ―.　｜　want / tell / ask＋人＋to ～　｜　let / make / help＋人＋動詞の原形",
                ["It is ～ for … to ―.「…にとって（…が）―することは～だ」：It is difficult for me to swim fast. (for の後ろは目的格)",
                 "want＋人＋to ～「人に～してほしい」、tell＋人＋to ～「人に～するように言う」、ask＋人＋to ～「人に～するように頼む」。",
                 "let＋人＋原形「人に（望みどおり）～させてあげる（許可）」、make＋人＋原形「人に（いやでも）～させる（強制）」。",
                 "help＋人＋原形「人が～するのを手伝う」（help＋人＋to ～ の形もある）。",
                 "let / make の後ろに to は置かない：× let me to go、× made us to run。"],
                body="It は形だけの主語で、本当の主語は to ― の部分です。to ― が長いので、文の後ろに回しています。",
                points=[tp("let と make の意味の違い（許可と強制）を、親子の会話の場面で演じ分けさせると定着しやすい。",
                           ask="My mother let me play games. と My mother made me study. で、気持ちが違うのはどこか。", expect="let は「させてくれた」（うれしい）、make は「させた」（いやでも）。",
                           timing="定理の説明時")]),
        derivation("dv1", "間接疑問文ができるまで（疑問文 → 文の一部）",
                   ["① もとの疑問文を書く：Where does Ken live?",
                    "② 疑問文を作るために主語の前に出していた does を取りのぞく：Where Ken live ?",
                    "③ does が表していた「三人称単数・現在」の情報を動詞に戻す：live → lives（did なら過去形に、do なら原形のまま）。",
                    "④ 〈疑問詞＋主語＋動詞〉の形ができる：where Ken lives",
                    "⑤ be 動詞・助動詞の場合は、主語の前に出ていた is / can などを主語の後ろに戻す：Where is the station? → where the station is ／ What can I do? → what I can do",
                    "⑥ 全体の文に入れる：Do you know where Ken lives?（終わりの記号は全体の文に合わせる）"],
                   body="間接疑問文は「疑問文になる前の、ふつうの文の語順に戻す」と考えると覚えやすくなります。疑問詞が主語のとき（Who made this?）は、もともと〈主語＋動詞〉の語順なので変える必要がありません。",
                   points=[tp("②③のステップを、カードを動かして見せる。does のカードを取ると、s のカードが live にくっつく、という見せ方が効果的。",
                              ask="When did you buy it? を I want to know ～. に入れると？", expect="I want to know when you bought it.",
                              caution="when you buy it と原形のままにする誤りに注意。did の「過去」の情報を bought に移す。", timing="導出の説明時")]),
        example("ex1", "例題1　間接疑問文を作る",
                "（　）の疑問文を文の一部にして、英文を完成させなさい。(1) Do you know (What does Yumi want?)?　(2) I don't know (Why was Ken angry?).　(3) Please tell me (Who wrote this letter?).",
                ["(1) does を取り、want を主語 Yumi に合わせて wants にする → what Yumi wants。",
                 "(2) was を主語 Ken の後ろへ戻す → why Ken was angry。",
                 "(3) 疑問詞 who が主語なので、語順はそのまま → who wrote this letter。"],
                "(1) Do you know what Yumi wants?　(2) I don't know why Ken was angry.　(3) Please tell me who wrote this letter.",
                thinking="もとの疑問文で、主語の前に出ている do / does / did / be 動詞 / 助動詞を見つけ、主語の後ろの正しい形に戻す。",
                points=[tp("(3) を who did write this letter や who this letter wrote にする誤りを取り上げ、疑問詞が主語の場合は語順を変えないことを確認する。")],
                misconceptions=[("Do you know what does Yumi want?", "間接疑問文では does を使わない。what Yumi wants。"),
                                ("I don't know why was Ken angry.", "be 動詞は主語の後ろ。why Ken was angry。")]),
        example("ex2", "例題2　SVOO と SVOC",
                "日本語に合うように英文を完成させなさい。(1) 兄は私にギターをくれた。My brother gave (　　).　(2) その映画は私を眠くさせた。The movie (　　) sleepy.　(3) (1) の文を to を使って書きかえなさい。",
                ["(1)「私に（A）ギターを（B）」で me ≠ a guitar → SVOO。gave me a guitar。",
                 "(2)「私を眠い状態に」で me ＝ sleepy → SVOC。made me sleepy。",
                 "(3) give は相手に届く動作なので to を使う → My brother gave a guitar to me."],
                "(1) me a guitar　(2) made me　(3) My brother gave a guitar to me.",
                thinking="動詞の後ろの2語が「人と物（A ≠ B）」なら SVOO、「A ＝ B」なら SVOC。",
                points=[tp("(3) で for を使う誤りが多い。buy / make など「（相手のために）～してあげる」動詞が for、give / show など「相手に届ける」動詞が to、と動作のイメージで分けさせる。",
                           ask="My mother made a cake (to / for) me. はどちらか。", expect="for（私のために作った）。")],
                misconceptions=[("The movie made sleepy me.", "SVOC は〈動詞＋A＋B〉の順。made me sleepy。")]),
        example("ex3", "例題3　不定詞・原形不定詞の文",
                "（　）内の語を並べかえなさい。(1) 私にとって早起きすることは簡単ではない。It is (easy / for / not / me / to) get up early.　(2) 先生は私たちに静かにするように言った。The teacher (us / told / be / to) quiet.　(3) 父は私に彼の自転車を使わせてくれた。My father (me / use / let) his bike.",
                ["(1) It is ～ for … to ―. の形。否定は is not → It is not easy for me to get up early.",
                 "(2) tell＋人＋to ～ → The teacher told us to be quiet.",
                 "(3) let＋人＋原形（許可）→ My father let me use his bike.（to は置かない）"],
                "(1) It is not easy for me to get up early.　(2) The teacher told us to be quiet.　(3) My father let me use his bike.",
                thinking="for … の後ろは to ―、tell / want / ask は人の後ろに to ～、let / make / help は人の後ろに原形。",
                points=[tp("(2) と (3) を比べて「tell は to がある、let は to がない」ことを強調し、後で make・help も同じグループに入れて表にまとめる。",
                           ask="My father let me to use his bike. はどこが誤りか。", expect="let の後ろの人の次は原形なので to が不要。")]),
        board("bd1", "板書案",
              [("① 間接疑問文", ["Where does he live?", "→ Do you know where he lives?", "疑問詞＋主語＋動詞", "does / did は消える → 動詞の形に",
                                "What is this? → what this is", "Who made it? → who made it（そのまま）"]),
               ("② SVOO と SVOC", ["SVOO：give me a watch（A ≠ B）", "→ give a watch to me", "to：give / show / tell / send / teach",
                                   "for：buy / make / cook / get", "SVOC：call our dog Kuro（A ＝ B）", "make us sad / keep the room clean"]),
               ("③ 不定詞・原形の文", ["It is ～ for 人 to ―.", "want / tell / ask＋人＋to ～", "let＋人＋原形（許可）",
                                     "make＋人＋原形（強制）", "help＋人＋原形（to も可）", "× let me to go"])],
              points=[tp("③の列は「to がいる動詞」「to がいらない動詞」を色分けして書き、最後に生徒に例文を1つずつ作らせる。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("文型の名前（SVOO など）を覚えさせるより、「A ≠ B か A ＝ B か」「to か原形か」といった判断の手がかりを使えることを重視する。", timing="授業全体"),
               tp("間接疑問文は、道案内の場面（Excuse me. Could you tell me where ～ is?）で使わせると、丁寧なたずね方として必要性が実感できる。",
                  ask="観光客に駅の場所を丁寧にたずねるには？", expect="Could you tell me where the station is?"),
               tp("SVOO の言いかえは、give 型（to）と buy 型（for）を動詞カードで分類させる。"),
               tp("It is ～ for … to ―. は、意見文の型として JH-ENG-G3-U07（条件英作文）でも使うことを予告し、because と組み合わせた例を示す。",
                  caution="for の後ろを主格（for I）にする誤り、to を落とす誤り（for me play）に注意。"),
               tp("問題プリント D の誤答例は「間接疑問文の語順」「SVOO / SVOC の語順・前置詞」「to の有無」の3種類にまとめて振り返らせる。")],
              misconceptions=[("Do you know where does he live?", "間接疑問文では does を使わず、where he lives。"),
                              ("My uncle bought a cap to me.", "buy は for を使う。bought a cap for me。"),
                              ("My mother made me to clean my room.", "make＋人＋原形。made me clean my room。"),
                              ("It is easy for I to swim.", "for の後ろは目的格。for me。")]),
        summary("sm1", "まとめ",
                ["間接疑問文は〈疑問詞＋主語＋動詞〉。do / does / did は消し、その情報を動詞の形に移す。疑問詞が主語ならそのまま。",
                 "SVOO（A に B を：A ≠ B）は〈物＋to / for＋人〉に言いかえられる。SVOC（A を B に：A ＝ B）は make / call / name / keep など。",
                 "It is ～ for … to ―.、want / tell / ask＋人＋to ～、let / make / help＋人＋原形。let / make の後ろに to は置かない。"]),
        check("ck1", "確認問題",
              [("Where did you buy it? を I want to know ～. の文に入れなさい。", "I want to know where you bought it."),
               ("My grandmother made me a sweater. を for を使って書きかえなさい。", "My grandmother made a sweater for me."),
               ("「母は私に彼女のスマートフォンを使わせてくれた」を let を使って英語にしなさい。", "My mother let me use her smartphone.")]),
    ],
)


# ======================================================================
# A 基本確認
# ======================================================================

R_Q = ("間接疑問文では、疑問詞の後ろを〈主語＋動詞〉の語順にする。疑問文の語順のままにしない。", "間接疑問文の語順")

# (もとの疑問文, 正しい間接疑問, [(誤り, 理由)])
INDIRECT = [
    ("Where does he live?", "where he lives",
     [("where does he live", R_Q), ("where he live", ("does を取ったら、三人称単数・現在の情報を動詞に移して lives にする。", "do / does / did が消えたときの動詞の形")),
      ("where lives he", ("一般動詞を主語の前に出す語順は英語にない。", "間接疑問文の語順"))]),
    ("What is this?", "what this is",
     [("what is this", R_Q), ("what this be", ("be 動詞は主語と時制に合わせて is にする。原形の be は使わない。", "be 動詞の形")),
      ("what does this is", ("be 動詞の文に does は使わない。また間接疑問文では does を使わない。", "be 動詞と一般動詞の混同"))]),
    ("When did she come to Japan?", "when she came to Japan",
     [("when did she come to Japan", R_Q), ("when she come to Japan", ("did を取ったら、過去の情報を動詞に移して came にする。", "do / does / did が消えたときの動詞の形")),
      ("when came she to Japan", ("一般動詞を主語の前に出す語順は英語にない。", "間接疑問文の語順"))]),
    ("Who is that man?", "who that man is",
     [("who is that man", R_Q), ("who that man", ("動詞 is がなく、文の形になっていない。", "be 動詞の脱落")),
      ("who does that man is", ("be 動詞の文に does は使わない。", "be 動詞と一般動詞の混同"))]),
    ("How old is your sister?", "how old your sister is",
     [("how old is your sister", R_Q), ("how your sister is old", ("how old は「何歳」というひとかたまりの疑問詞なので、切りはなさず先頭に置く。", "疑問詞のかたまり")),
      ("how old your sister", ("動詞 is がなく、文の形になっていない。", "be 動詞の脱落"))]),
    ("Why was Ken late?", "why Ken was late",
     [("why was Ken late", R_Q), ("why did Ken late", ("be 動詞の文に did は使わない。late は形容詞なので be 動詞が必要。", "be 動詞と一般動詞の混同")),
      ("why Ken late was", ("be 動詞は主語のすぐ後ろに置く。補語 late の後ろには置かない。", "間接疑問文の語順"))]),
    ("What time does the train leave?", "what time the train leaves",
     [("what time does the train leave", R_Q), ("what time the train leave", ("does を取ったら、動詞を三人称単数・現在の leaves にする。", "do / does / did が消えたときの動詞の形")),
      ("what the train leaves time", ("what time は「何時」というひとかたまりの疑問詞なので、切りはなさず先頭に置く。", "疑問詞のかたまり"))]),
    ("Who made this cake?", "who made this cake",
     [("who did make this cake", ("疑問詞 who が主語なので、もとから〈主語＋動詞〉の語順。did を加える必要はない。", "疑問詞が主語の場合")),
      ("who this cake made", ("this cake を主語の位置に置くと「このケーキがだれを作ったか」となり意味が変わる。", "疑問詞が主語の場合")),
      ("who make this cake", ("もとの疑問文は過去の made。動詞の時制を変えてはいけない。", "時制の保持"))]),
    ("What can I do for you?", "what I can do for you",
     [("what can I do for you", R_Q), ("what I do can for you", ("助動詞 can は動詞の前に置く：I can do。", "助動詞の位置")),
      ("what do I can do for you", ("助動詞 can のある文に do は使わない。", "助動詞と do の混同"))]),
    ("How many books do you have?", "how many books you have",
     [("how many books do you have", R_Q), ("how many you have books", ("how many＋名詞 はひとかたまりなので、books を切りはなさない。", "疑問詞のかたまり")),
      ("how many books you have them", ("books はすでに how many books として先頭にあるので、them をもう一度置かない。", "目的語の重複"))]),
    ("Where are your parents from?", "where your parents are from",
     [("where are your parents from", R_Q), ("where your parents is from", ("主語 your parents は複数なので be 動詞は are。", "主語と be 動詞の一致")),
      ("where do your parents from", ("be 動詞の文に do は使わない。", "be 動詞と一般動詞の混同"))]),
    ("What did Ken buy at the shop?", "what Ken bought at the shop",
     [("what did Ken buy at the shop", R_Q), ("what Ken buy at the shop", ("did を取ったら、過去の情報を動詞に移して bought にする。", "do / does / did が消えたときの動詞の形")),
      ("what Ken buys at the shop", ("もとの疑問文は過去（did）。現在形の buys にすると時制が変わる。", "時制の保持"))]),
    ("How much is this T-shirt?", "how much this T-shirt is",
     [("how much is this T-shirt", R_Q), ("how this T-shirt is much", ("how much は「いくら」というひとかたまりの疑問詞なので、切りはなさない。", "疑問詞のかたまり")),
      ("how much does this T-shirt", ("値段をたずねる文は be 動詞の文。does では文が成り立たない。", "be 動詞と一般動詞の混同"))]),
]

LEADS = [("Do you know ", "?"), ("I don't know ", "."), ("Please tell me ", "."), ("Can you tell me ", "?"), ("I want to know ", ".")]


@gen("basic_check", 4, ["computation", "condition_check"])
def indirect_choice(r):
    q, ok, wrongs = r.choice(INDIRECT)
    lead, end = r.choice(LEADS)
    return mc(f"次の疑問文を文の一部として入れるとき、（　）に入る最も適切なものを選びなさい。\n{q}\n{lead}(　　){end}", [ok] + [w for w, _ in wrongs],
              f"間接疑問文は〈疑問詞＋主語＋動詞〉の語順。答えは {lead}{ok}{end}", d=1,
              ap="もとの疑問文で主語の前に出ている do / does / did・be 動詞・助動詞を見つけ、ふつうの文の語順に戻す。",
              steps=[f"もとの疑問文 {q} の主語を見つける。", "do / does / did は取りのぞき、動詞の形（三単現・過去）に情報を移す。be 動詞・助動詞は主語の後ろに戻す。", f"答え：{ok}"],
              alt=["疑問詞のあとの部分だけを取り出して、ふつうの文（肯定文）として正しいかを確かめる。"],
              pc=[("〈疑問詞＋主語＋動詞〉の語順を理解している", 1), ("動詞の形まで正しいものを選んでいる", 1)],
              pit=["疑問文の語順のまま入れる。", "does / did を取ったあと、動詞の s や過去形を忘れる。"],
              why={w: reason for w, reason in wrongs})


P_SVC = "SVC（主語＋動詞＋補語：S ＝ C）"
P_SVO = "SVO（主語＋動詞＋目的語）"
P_SVOO = "SVOO（主語＋動詞＋A＋B：A に B を）"
P_SVOC = "SVOC（主語＋動詞＋A＋B：A を B に、A ＝ B）"
PAT_REASON = {
    P_SVC: "SVC は動詞の後ろが主語を説明する補語1つだけの文（She is happy. など）。",
    P_SVO: "SVO は動詞の後ろに目的語が1つだけの文。",
    P_SVOO: "SVOO は動詞の後ろに「人（A）」と「物（B）」が並び、A ≠ B の文。",
    P_SVOC: "SVOC は動詞の後ろの A と B の間に A ＝ B の関係がある文。",
}
# (英文, 文型, 分析)
PATTERNS = [
    ("We call the dog Max.", P_SVOC, "the dog ＝ Max（犬をマックスと呼ぶ）"),
    ("The song made me happy.", P_SVOC, "me ＝ happy（私を幸せにした）"),
    ("You should keep your room clean.", P_SVOC, "your room ＝ clean（部屋をきれいに保つ）"),
    ("They named the baby Hana.", P_SVOC, "the baby ＝ Hana（赤ちゃんをハナと名づけた）"),
    ("The news made everyone excited.", P_SVOC, "everyone ＝ excited（みんなをわくわくさせた）"),
    ("My aunt gave me a watch.", P_SVOO, "me ≠ a watch（私に時計を）"),
    ("Mr. Ito teaches us math.", P_SVOO, "us ≠ math（私たちに数学を）"),
    ("She made her son a sandwich.", P_SVOO, "her son ≠ a sandwich（息子にサンドイッチを）"),
    ("Ken told me an interesting story.", P_SVOO, "me ≠ an interesting story（私におもしろい話を）"),
    ("My father bought me a bike.", P_SVOO, "me ≠ a bike（私に自転車を）"),
    ("My sister became a nurse.", P_SVC, "My sister ＝ a nurse で、動詞の後ろは補語1つ"),
    ("You look tired today.", P_SVC, "You ＝ tired で、動詞の後ろは補語1つ"),
    ("This soup tastes good.", P_SVC, "This soup ＝ good で、動詞の後ろは補語1つ"),
    ("She made a sandwich for her son.", P_SVO, "目的語は a sandwich 1つ。for her son は修飾語"),
    ("We call our grandmother every Sunday.", P_SVO, "目的語は our grandmother 1つ（「電話する」の意味）。every Sunday は時を表す修飾語"),
    ("He gave a book to me.", P_SVO, "目的語は a book 1つ。to me は修飾語"),
]


@gen("basic_check", 4, ["concept", "condition_check"])
def pattern_identify(r):
    en, ok, why_txt = r.choice(PATTERNS)
    wrongs = [p for p in (P_SVC, P_SVO, P_SVOO, P_SVOC) if p != ok]
    why = {w: (f"{PAT_REASON[w]}この文は {why_txt} なので当てはまらない。", "文型の見分け方") for w in wrongs}
    return mc(f"次の英文の文の型として最も適切なものを選びなさい。\n{en}", [ok] + wrongs,
              f"{why_txt}。よって {ok}。", d=2,
              ap="動詞の後ろにいくつの語（名詞・形容詞）があるかを数え、2つなら A ＝ B が成り立つかを確かめる。to / for のついた語句は数えない。",
              steps=["文の動詞を見つける。", "動詞の後ろの語を、to / for などの前置詞のついた修飾語を除いて確かめる。", f"関係を調べる：{why_txt}。", f"答え：{ok}"],
              alt=["A と B の間に is を入れて意味が通るかを試す（通れば SVOC、通らなければ SVOO）。"],
              pc=[("動詞の後ろの語の数と関係を確かめている", 1), ("正しい型を選んでいる", 1)],
              pit=["make や call を見ると、いつも SVOC だと思いこむ。", "to me / for her son を目的語として数える。"], why=why)


# (SVOO の文, 空所つき SVO の文, 前置詞)
TOFOR = [
    ("My uncle gave me this watch.", "My uncle gave this watch (　　) me.", "to"),
    ("Please show me your notebook.", "Please show your notebook (　　) me.", "to"),
    ("Ms. Brown teaches us English.", "Ms. Brown teaches English (　　) us.", "to"),
    ("I sent my grandmother a letter.", "I sent a letter (　　) my grandmother.", "to"),
    ("Can you lend me your pen?", "Can you lend your pen (　　) me?", "to"),
    ("Ken told us a funny story.", "Ken told a funny story (　　) us.", "to"),
    ("My mother made me a cake.", "My mother made a cake (　　) me.", "for"),
    ("My father bought my sister a dress.", "My father bought a dress (　　) my sister.", "for"),
    ("I'll cook you dinner tonight.", "I'll cook dinner (　　) you tonight.", "for"),
    ("Could you get me a glass of water?", "Could you get a glass of water (　　) me?", "for"),
    ("Yumi made her friends some cookies.", "Yumi made some cookies (　　) her friends.", "for"),
    ("He handed me the ticket.", "He handed the ticket (　　) me.", "to"),
]


@gen("basic_check", 4, ["condition_check", "computation"])
def to_or_for(r):
    a, b, ok = r.choice(TOFOR)
    other = "for" if ok == "to" else "to"
    why = {other: (("to は give / show / teach / send / lend / tell / hand のように、物や情報が相手に届く動詞に使う。この動詞は「相手のために～してあげる」動詞なので for。")
                   if ok == "for" else ("for は buy / make / cook / get のように「相手のために～してあげる」動詞に使う。この動詞は物や情報が相手に届く動詞なので to。"),
                   "to と for の使い分け"),
           "of": ("of は SVOO の言いかえには使わない（この単元の動詞では of をとらない）。", "前置詞の選び方"),
           "with": ("with は「～といっしょに」「～を使って」の意味で、物を受け取る相手を表さない。", "前置詞の選び方")}
    return mc(f"2つの英文がほぼ同じ意味になるように、（　）に入る語を選びなさい。\n{a}\n{b}", [ok] + list(why),
              f"SVOO を〈物＋前置詞＋人〉に言いかえるとき、相手に届く動作の動詞は to、相手のためにする動作の動詞は for。答えは {ok}。", d=2,
              ap="動詞が「相手に渡す・届ける」動作か、「相手のために作る・買う」動作かを考える。",
              steps=["文の動詞を確かめる。", "give / show / teach / send / lend / tell / hand は to、buy / make / cook / get は for。", f"答え：{ok}"],
              alt=["「相手がいなくてもできる動作か」で確かめる。買う・作るは相手がいなくてもできる（for）、渡す・見せるは相手が必要（to）。"],
              pc=[("動詞の種類を判断している", 1), ("正しい前置詞を選んでいる", 1)],
              pit=["どの動詞にも to を使う。", "make を見ると SVOC と考え、前置詞を入れられないと思う。"], why=why)


ACTS = [
    ("英語を話す", "speak English", "spoke English", "difficult", "難しい"),
    ("速く泳ぐ", "swim fast", "swam fast", "easy", "簡単だ"),
    ("毎日本を読む", "read books every day", "read books every day", "important", "大切だ"),
    ("友だちとサッカーをする", "play soccer with friends", "played soccer with friends", "fun", "楽しい"),
    ("新しいことを学ぶ", "learn new things", "learned new things", "interesting", "おもしろい"),
    ("朝早く起きる", "get up early in the morning", "got up early in the morning", "hard", "大変だ"),
    ("その質問に答える", "answer the question", "answered the question", "easy", "簡単だ"),
    ("外国の文化を知る", "know about foreign cultures", "knew about foreign cultures", "important", "大切だ"),
    ("ギターをひく", "play the guitar", "played the guitar", "fun", "楽しい"),
]
PERS = [("me", "I", "私"), ("us", "we", "私たち"), ("him", "he", "彼"), ("her", "she", "彼女"), ("them", "they", "彼ら")]


@gen("basic_check", 4, ["computation", "cross_unit"], rel=["JH-ENG-G2-U02"])
def it_for_to(r):
    act_jp, vp, vp_past, adj, adj_jp = r.choice(ACTS)
    obj, subj, pjp = r.choice(PERS)
    ok = f"It is {adj} for {obj} to {vp}."
    w1 = f"It is {adj} for {obj} {vp}."
    w2 = f"It is {adj} for {subj} to {vp}."
    w3 = f"It is {adj} {obj} for to {vp}."
    why = {w1: ("to がないと、for の後ろの人と動詞の原形が直接並び、文が成り立たない。It is ～ for … to ―. の to が必要。", "It is ～ for … to ― の形"),
           w2: (f"for は前置詞なので、後ろの代名詞は目的格 {obj} にする。{subj} は主格。", "前置詞の後ろの代名詞の格"),
           w3: ("語順が誤り。〈for＋人〉を形容詞の後ろに置き、そのあとに〈to＋動詞の原形〉を続ける。", "It is ～ for … to ― の語順")}
    return mc(f"日本語に合う英文として最も適切なものを選びなさい。\n{pjp}にとって{act_jp}ことは{adj_jp}。", [ok] + list(why),
              f"「…にとって―することは～だ」は It is ～ for …（目的格）to ―（動詞の原形）. で表す。答え：{ok}", d=2,
              ap="It is ～ for … to ―. の型に、形容詞・人（目的格）・動作の順に当てはめる。",
              steps=[f"「{adj_jp}」→ It is {adj}。", f"「{pjp}にとって」→ for {obj}（目的格）。", f"「{act_jp}こと」→ to {vp}。", f"答え：{ok}"],
              alt=[f"To ～ を主語にした文（To {vp} is {adj} for {obj}.）を考え、主語の to ～ を後ろに回した形が It is ～ for … to ―. であることから確かめる。"],
              pc=[("It is ～ for … to ― の型を使っている", 1), ("代名詞の格と to の位置が正しいものを選んでいる", 1)],
              pit=["for の後ろに主格（I / he）を置く。", "to を落として for me play とする。"], why=why)


# (日本語, 空所つき英文, 原形, ing, 過去形, 三単現, 動詞)
BARE = [
    ("父は私に彼のカメラを使わせてくれた。", "My father let me (　　) his camera.", "use", "using", "used", "uses", "let"),
    ("母は弟に部屋をそうじさせた。", "My mother made my brother (　　) his room.", "clean", "cleaning", "cleaned", "cleans", "make"),
    ("あなたの写真を見せてください。", "Please let me (　　) your pictures.", "see", "seeing", "saw", "sees", "let"),
    ("先生は私たちにもう一度その文を書かせた。", "Our teacher made us (　　) the sentence again.", "write", "writing", "wrote", "writes", "make"),
    ("ケンは私が箱を運ぶのを手伝ってくれた。", "Ken helped me (　　) the box.", "carry", "carrying", "carried", "carries", "help"),
    ("自己紹介をさせてください。", "Let me (　　) myself.", "introduce", "introducing", "introduced", "introduces", "let"),
    ("その映画は私たちを笑わせた。", "The movie made us (　　).", "laugh", "laughing", "laughed", "laughs", "make"),
    ("姉は私が宿題をするのを手伝ってくれた。", "My sister helped me (　　) my homework.", "do", "doing", "did", "does", "help"),
    ("祖父母は私に夜おそくまで起きていさせてくれた。", "My grandparents let me (　　) up late.", "stay", "staying", "stayed", "stays", "let"),
    ("コーチは私たちに毎日走らせた。", "The coach made us (　　) every day.", "run", "running", "ran", "runs", "make"),
    ("私は母が夕食を作るのを手伝った。", "I helped my mother (　　) dinner.", "cook", "cooking", "cooked", "cooks", "help"),
    ("考えさせてください。", "Let me (　　) about it.", "think", "thinking", "thought", "thinks", "let"),
]


@gen("basic_check", 4, ["condition_check", "common_error"])
def bare_inf(r):
    jp, s, base, ing, past, third, v = r.choice(BARE)
    why = {ing: (f"{v}＋人の後ろには動詞の原形を置く。ing 形は使わない。", "原形不定詞の形"),
           past: (f"{v} の文が過去でも、人の後ろの動詞は原形のまま。過去形にはしない。", "原形不定詞の形")}
    if v == "help":
        why[third] = ("help＋人の後ろの動詞は、主語や人に関係なく原形（または to＋原形）。s はつけない。", "原形不定詞の形")
    else:
        why[f"to {base}"] = (f"{v}＋人＋動詞の原形 の形で、to は置かない（to を使うのは want / tell / ask）。", "let / make と want / tell の混同")
    meaning = {"let": "（望みどおり）～させてあげる", "make": "（いやでも）～させる", "help": "～するのを手伝う"}[v]
    return mc(f"日本語に合うように、（　）に入る最も適切なものを選びなさい。\n{jp}\n{s}", [base] + list(why),
              f"{v}＋人＋動詞の原形 で「人に{meaning}」。答えは {base}。", d=2,
              ap=f"動詞 {v} の後ろの〈人＋動詞〉で、動詞がどの形になるかを思い出す。",
              steps=[f"文の動詞は {v}（{meaning}）。", f"{v}＋人＋動詞の原形 の形を使う。", f"答え：{base}"],
              alt=[f"want / tell を使う文（～ want＋人＋to ～）と比べて、{v} は to がいらないグループであることを確かめる。"],
              pc=[("let / make / help＋人＋原形 の形を知っている", 1), ("原形を選んでいる", 1)],
              pit=["let / make の後ろに to を入れる。", "文が過去だからと、人の後ろの動詞まで過去形にする。"], why=why)


# ======================================================================
# B 標準演習
# ======================================================================

# (前の文, 疑問文, 答え, 別解)
COMBINE = [
    ("I don't know.", "Where is the post office?", "I don't know where the post office is.", []),
    ("Do you know?", "What does Mr. Smith like?", "Do you know what Mr. Smith likes?", []),
    ("Please tell me.", "When will the game start?", "Please tell me when the game will start.", []),
    ("I want to know.", "Why did Aya go to Canada?", "I want to know why Aya went to Canada.", []),
    ("Do you know?", "Who painted this picture?", "Do you know who painted this picture?", []),
    ("I don't know.", "How many students are there in this school?", "I don't know how many students there are in this school.", []),
    ("Can you tell me?", "What time does the shop open?", "Can you tell me what time the shop opens?", []),
    ("Do you know?", "Where are they going?", "Do you know where they are going?", []),
    ("I don't remember.", "What did I say to her?", "I don't remember what I said to her.", []),
    ("Tell me.", "How can I get to the museum?", "Tell me how I can get to the museum.", []),
    ("I wonder.", "Who is that tall boy?", "I wonder who that tall boy is.", []),
    ("Do you know?", "How long has Ken lived in Tokyo?", "Do you know how long Ken has lived in Tokyo?", []),
]


@gen("standard_practice", 4, ["computation", "cross_unit"], rel=["JH-ENG-G1-U03"])
def combine_indirect(r):
    a, q, ans, vs = r.choice(COMBINE)
    return sa(f"次の2つの英文を、間接疑問文を使って1つの英文にしなさい。\n{a}\n{q}", ans,
              f"疑問文を〈疑問詞＋主語＋動詞〉の語順にして、前の文の目的語の位置に入れる。答え：{ans}", d=3, p=4, v=vs or None,
              ap="中1で学んだ疑問詞の疑問文を、ふつうの文の語順に戻してから前の文につなげる。",
              steps=["疑問文の主語と、主語の前に出ている do / does / did・be 動詞・助動詞を見つける。",
                     "do / does / did は取り、動詞の形（三単現・過去）に情報を移す。be 動詞・助動詞は主語の後ろに戻す。",
                     "できた〈疑問詞＋主語＋動詞〉を前の文の後ろにつなぎ、終わりの記号を全体の文に合わせる。", f"答え：{ans}"],
              alt=["完成した文の疑問詞以下を取り出して、ふつうの文として正しいか（主語＋動詞の形がそろっているか）を確かめる。"],
              pc=[("〈疑問詞＋主語＋動詞〉の語順にしている", 2), ("動詞の形と文の終わりの記号が正しい", 2)],
              pit=["疑問文の語順のままつなぐ。", "前の文が Do you know? なのに、文の終わりをピリオドにする。"])


ORDERS = [
    ("私たちはこのねこをタマと呼んでいます。", ["we", "call", "this cat", "Tama"], "call A B（A を B と呼ぶ）"),
    ("その知らせは彼女を悲しませた。", ["the news", "made", "her", "sad"], "make A B（A を B にする）"),
    ("おばは私にすてきなかばんをくれた。", ["my aunt", "gave", "me", "a nice bag"], "give A B（A に B を）"),
    ("あなたは彼がどこに住んでいるか知っていますか。", ["do", "you", "know", "where", "he", "lives"], "間接疑問文 where he lives"),
    ("私にとって数学を勉強することはおもしろい。", ["it", "is", "interesting", "for", "me", "to", "study", "math"], "It is ～ for … to ―."),
    ("母は私に早く寝るように言った。", ["my mother", "told", "me", "to", "go", "to bed", "early"], "tell＋人＋to ～"),
    ("私はあなたにこの本を読んでほしい。", ["I", "want", "you", "to", "read", "this book"], "want＋人＋to ～"),
    ("父は私を遊園地に行かせてくれた。", ["my father", "let", "me", "go", "to the amusement park"], "let＋人＋原形"),
    ("窓を開けたままにしておいてください。", ["please", "keep", "the window", "open"], "keep A B（A を B のままにしておく）"),
    ("この映画は何時に始まるか教えてください。", ["please", "tell", "me", "what time", "the movie", "starts"], "tell me＋間接疑問文"),
    ("ケンは私が皿を洗うのを手伝ってくれた。", ["Ken", "helped", "me", "wash", "the dishes"], "help＋人＋原形"),
    ("グリーン先生は私たちに英語の歌を教えてくれた。", ["Ms. Green", "taught", "us", "an English song"], "teach A B（A に B を）"),
    ("私は彼女がだれなのか知らない。", ["I", "don't", "know", "who", "she", "is"], "間接疑問文 who she is"),
]


@gen("standard_practice", 4, ["application", "computation"])
def build_order(r):
    jp, parts, pat = r.choice(ORDERS)
    sent = cap(" ".join(parts)) + ("?" if jp.endswith("か。") and parts[0] in ("do", "can", "did") else ".")
    return order(f"日本語に合うように、次の語句を並べかえて正しい英文にしなさい。文頭にくる語も小文字で示してある。\n{jp}", parts,
                 f"{sent}　ポイント：{pat}。", d=2, p=4,
                 ap="まず文の主語と動詞を決め、動詞の後ろにどんな型（A＋B、人＋to ～、人＋原形、疑問詞＋主語＋動詞）が続くかを考える。",
                 steps=["主語と動詞を決める。", f"動詞の後ろの型を決める：{pat}。", "残りの語句を型に当てはめて並べる。", f"完成文：{sent}"],
                 alt=["完成した英文を日本語に訳し直し、「だれが・だれに（を）・何を・どうする」が問題の日本語と一致するかを確かめる。"],
                 pc=[("主語と動詞の語順が正しい", 2), ("動詞の後ろの型の語順が正しい", 2)],
                 pit=["SVOC の A と B の順番を逆にする。", "間接疑問文の部分を疑問文の語順にする。"])


# (もとの文, 空所つきの言いかえ, 答え, 別解, 説明)
REWRITE = [
    ("To swim in this river is dangerous.", "(　　) is dangerous to swim in this river.", "It", None, "To ～ の主語を後ろに回し、形だけの主語 It を置く。"),
    ("Playing the guitar is fun for me.", "It is fun for me (　　) play the guitar.", "to", None, "It is ～ for … to ―. の to。動名詞の主語を不定詞に言いかえる。"),
    ("I was happy because of your letter.", "Your letter made me (　　).", "happy", None, "「あなたの手紙が私を幸せにした」と SVOC（make A B）で言いかえる。"),
    ("I can't answer the question easily.", "It is not easy (　　) me to answer the question.", "for", None, "It is ～ for … to ―. の for。"),
    ("My mother said to me, \"Clean your room.\"", "My mother told me (　　) clean my room.", "to", None, "命令文を伝えるときは tell＋人＋to ～。"),
    ("My father said, \"You can use my computer.\"", "My father (　　) me use his computer.", "let", None, "「使ってもいい」という許可を let＋人＋原形 で表す。"),
    ("Our dog's name is Kuro.", "We (　　) our dog Kuro.", "call", ["named"], "「犬をクロと呼ぶ」と SVOC（call A B）で言いかえる。name（名づけた）も可。"),
    ("Tell me your address.", "Tell me (　　) you live.", "where", None, "「住所」を「どこに住んでいるか」と間接疑問文で言いかえる。"),
    ("Do you know his age?", "Do you know how (　　) he is?", "old", None, "「年齢」を「何歳か」（how old he is）と間接疑問文で言いかえる。"),
    ("Ms. Brown teaches us English.", "Ms. Brown teaches English (　　) us.", "to", None, "teach は相手に届く動作なので to。"),
    ("Please say, \"Please help me,\" to Ken.", "Please ask Ken (　　) help you.", "to", None, "頼むことを伝えるときは ask＋人＋to ～。"),
    ("The coach said to us, \"Run!\" We had to run.", "The coach (　　) us run.", "made", None, "「（いやでも）走らせた」は make＋人＋原形。"),
    ("I want to know the price of this bag.", "I want to know how (　　) this bag is.", "much", None, "「値段」を「いくらか」（how much this bag is）と間接疑問文で言いかえる。"),
]


@gen("standard_practice", 4, ["cross_unit", "condition_check"], rel=["JH-ENG-G2-U02"])
def rewrite(r):
    a, b, ans, vs, point = r.choice(REWRITE)
    return sa(f"2つの英文がほぼ同じ意味になるように、（　）に入る適切な1語を書きなさい。\n{a}\n{b}", ans,
              f"{point}答え：{ans}", d=3, p=4, v=vs,
              ap="2文目の型（It is ～ for … to ―.／SVOC／人＋to ～／人＋原形／間接疑問文）を見ぬいて、1文目の内容を当てはめる。",
              steps=["1文目と2文目で、同じ内容を表している部分を対応させる。", "2文目がどの文構造の型かを判断する。", f"空所に入る語を決める：{ans}"],
              alt=["完成した2文目を日本語に訳し、1文目の内容と一致するかを確かめる。"],
              pc=[("2文目の文構造の型を見ぬいている", 2), ("正しい1語を書いている", 2)],
              pit=["It is ～ の文で to と for を取りちがえる。", "let / make の文に to を入れる。"])


# (日本語, 空所つき英文, 原形, ing, 過去形, 動詞)
TELL = [
    ("母は私に部屋をそうじするように言った。", "My mother told me (　　) my room.", "clean", "cleaning", "cleaned", "tell"),
    ("私はあなたに私の家に来てほしい。", "I want you (　　) to my house.", "come", "coming", "came", "want"),
    ("ケンは私に窓を開けるように頼んだ。", "Ken asked me (　　) the window.", "open", "opening", "opened", "ask"),
    ("先生は私たちにもっと本を読むように言った。", "The teacher told us (　　) more books.", "read", "reading", "read", "tell"),
    ("両親は私に医者になってほしいと思っている。", "My parents want me (　　) a doctor.", "become", "becoming", "became", "want"),
    ("私は姉に宿題を手伝ってくれるように頼んだ。", "I asked my sister (　　) me with my homework.", "help", "helping", "helped", "ask"),
    ("コーチは私たちに水をたくさん飲むように言った。", "The coach told us (　　) a lot of water.", "drink", "drinking", "drank", "tell"),
    ("あなたは私に何をしてほしいですか。", "What do you want me (　　)?", "do", "doing", "did", "want"),
    ("祖母は私にもっとゆっくり話すように頼んだ。", "My grandmother asked me (　　) more slowly.", "speak", "speaking", "spoke", "ask"),
    ("私は弟にこの手紙を読んでほしかった。", "I wanted my brother (　　) this letter.", "read", "reading", "read", "want"),
]


@gen("standard_practice", 4, ["condition_check", "concept"])
def tell_to(r):
    jp, s, base, ing, past, v = r.choice(TELL)
    ok = f"to {base}"
    why = {base: (f"{v}＋人の後ろに動詞を続けるときは to＋原形にする。原形だけを置くのは let / make / help。", "want / tell と let / make の混同"),
           ing: (f"{v}＋人の後ろは to＋原形。ing 形は使わない。", "不定詞と動名詞の混同")}
    if past != base:
        why[past] = ("文が過去でも、人の後ろは to＋原形。過去形は置かない。", "不定詞の形")
    else:
        why[f"to {ing}"] = ("to の後ろは動詞の原形。to＋ing 形にはならない。", "不定詞の形")
    meaning = {"tell": "人に～するように言う", "want": "人に～してほしい", "ask": "人に～するように頼む"}[v]
    return mc(f"日本語に合うように、（　）に入る最も適切なものを選びなさい。\n{jp}\n{s}", [ok] + list(why),
              f"{v}＋人＋to＋動詞の原形 で「{meaning}」。答えは {ok}。", d=2, p=4,
              ap=f"文の動詞 {v} が、人の後ろに to ～ をとるグループか、原形をとるグループ（let / make / help）かを確かめる。",
              steps=[f"文の動詞は {v}。", f"{v}＋人＋to＋原形 で「{meaning}」。", f"答え：{ok}"],
              alt=[f"人を取りのぞいた文（{'I want to ～' if v == 'want' else v + ' ～'}）と比べ、「to ～ をするのはだれか」を考えると、人の後ろに to ～ が続く理由がわかる。"],
              pc=[("want / tell / ask＋人＋to ～ の形を知っている", 2), ("正しい形を選んでいる", 2)],
              pit=["let / make と同じように原形を置く。", "want＋人＋that ～ のように that を使う。"], why=why)


# (英文, 正しい訳, [(誤訳, 理由)])
MEANING = [
    ("The letter made my mother happy.", "その手紙は母を幸せな気持ちにした。",
     [("その手紙は母に幸せを作った。", "made A B（A ＝ B）は「A を B にする」。make を「作る」と訳すのは SVO・SVOO のとき。"),
      ("母はその手紙で幸せを作った。", "文の主語は The letter。母は A（目的語）の位置にある。"),
      ("母は幸せな手紙を作った。", "happy は letter ではなく my mother の状態を表している。")]),
    ("My grandmother made me a sweater.", "祖母は私にセーターを作ってくれた。",
     [("祖母は私をセーターにした。", "me ≠ a sweater なので SVOO（A に B を）。「A を B にする」ではない。"),
      ("祖母は私にセーターを作らせた。", "「作らせた」なら made me make a sweater。この文に動詞は made しかない。"),
      ("私は祖母にセーターを作った。", "主語は My grandmother。作ったのは祖母。")]),
    ("We named the cat Sora.", "私たちはそのねこをソラと名づけた。",
     [("私たちはソラという名前のねこにした。", "name A B は「A を B と名づける」。the cat ＝ Sora。"),
      ("ソラは私たちのねこに名前をつけた。", "主語は We。名づけたのは私たち。"),
      ("私たちはソラにねこの名前をたずねた。", "name は「名づける」で、たずねるの意味はない。")]),
    ("Please keep the door open.", "ドアを開けたままにしておいてください。",
     [("ドアを開けてください。", "keep A B は「A を B のままにしておく」。open の状態を保つ意味。"),
      ("開いているドアを持っていてください。", "keep the door open は SVOC。open は door の状態を表す補語。"),
      ("ドアを閉めないで、開けるのをやめてください。", "keep を「やめる」と訳すのは誤り。")]),
    ("My father let me drive his car.", "父は私に彼の車を運転させてくれた。",
     [("父は私に彼の車を運転させた（無理やり）。", "let は許可（させてくれた）。無理やりさせるのは make。"),
      ("父は私の車を運転した。", "drive の主語は me（私）。運転したのは私。"),
      ("父は私に彼の車を運転してほしかった。", "「～してほしい」は want＋人＋to ～。let は許可。")]),
    ("Our teacher made us write the report again.", "先生は私たちにもう一度レポートを書かせた。",
     [("先生は私たちのためにもう一度レポートを書いた。", "make＋人＋原形 は「人に～させる」。書いたのは私たち。"),
      ("先生は私たちがもう一度レポートを書くのを許した。", "許可は let。make は（いやでも）させる。"),
      ("先生は私たちにレポートを作ってくれた。", "made us write は使役。「作ってくれた」は SVOO の made us a report。")]),
    ("I don't know what she wants.", "私は彼女が何をほしがっているのか知らない。",
     [("私は彼女がほしいものを知っている。", "don't know は否定。「知らない」。"),
      ("彼女は何がほしいのか私に知らせない。", "主語は I。知らないのは私。"),
      ("私は何がほしいのか、彼女は知らない。", "what she wants の主語は she。ほしがっているのは彼女。")]),
    ("Do you know who broke the window?", "だれが窓を割ったのか知っていますか。",
     [("あなたは窓を割った人ですか。", "Do you know ～? は「～を知っていますか」とたずねる文。"),
      ("だれが窓を割るのか知っていますか。", "broke は過去形。「割った」。"),
      ("窓を割ったのはあなたですか、とだれが知っていますか。", "文の主語は you。who broke the window は know の目的語。")]),
]


@gen("standard_practice", 4, ["concept", "application"])
def meaning(r):
    en, ok, wrongs = r.choice(MEANING)
    return mc(f"次の英文の意味として最も適切なものを選びなさい。\n{en}", [ok] + [w for w, _ in wrongs],
              f"動詞の後ろの型（A＋B の関係、人＋原形、疑問詞＋主語＋動詞）を見ぬいて訳す。答え：{ok}", d=3, p=4,
              ap="文の主語と動詞を確かめ、動詞の後ろの語の並び方から文の型を判断してから訳す。",
              steps=["文の主語と動詞を見つける。", "動詞の後ろの型を判断する（A ＝ B か、A ≠ B か、人＋原形か、間接疑問文か）。", "型に合った訳し方で全体を訳す。", f"答え：{ok}"],
              alt=["選んだ日本語を英語に戻してみて、もとの英文と同じ形になるかを確かめる。"],
              pc=[("文の型を正しく判断している", 2), ("文全体を正しく訳している", 2)],
              pit=["make をいつも「作る」と訳す。", "let と make の意味（許可と強制）を区別しない。"],
              why={w: (reason, "文構造の読み取り") for w, reason in wrongs})


# ======================================================================
# C 思考力・記述応用
# ======================================================================

PAIRS = [
    ("She made him a cake.", "She made him happy.",
     "A は him ≠ a cake の SVOO で「彼女は彼にケーキを作ってあげた」。B は him ＝ happy の SVOC で「彼女は彼を幸せにした」。同じ made him の後ろに続く語が、物（名詞）か状態（形容詞）かで型と意味が変わる。"),
    ("My father made me stay home.", "My father let me stay home.",
     "A は make＋人＋原形で「父は私を（いやでも）家にいさせた」という強制。B は let＋人＋原形で「父は私が家にいることを許してくれた」という許可。形は同じでも、make は本人の意志に反して、let は本人の望みどおりにさせる。"),
    ("Who is that girl?", "I know who that girl is.",
     "A は「あの女の子はだれですか」と相手にたずねる疑問文で、is が主語の前に出ている。B は who that girl is が know の目的語になった間接疑問文で「私はあの女の子がだれか知っている」。文全体はふつうの文なので、疑問詞の後ろは〈主語＋動詞〉の語順になる。"),
    ("I want to read this book.", "I want you to read this book.",
     "A は want to ～ で「私はこの本を読みたい」（読むのは私）。B は want＋人＋to ～ で「私はあなたにこの本を読んでほしい」（読むのはあなた）。want と to の間の人が、to ～ の動作をする人になる。"),
    ("Ken told me to come at six.", "Ken told me that he would come at six.",
     "A は tell＋人＋to ～ で「ケンは私に6時に来るように言った」（来るのは私）。B は tell＋人＋that ～ で「ケンは私に、自分が6時に来ると言った」（来るのはケン）。to ～ の動作をするのは me、that 以下の動作をするのは he。"),
    ("Where does Yumi live?", "Please tell me where Yumi lives.",
     "A は「ユミはどこに住んでいますか」とたずねる疑問文で、does が主語の前に出ている。B は where Yumi lives が tell me の後ろに入った間接疑問文で「ユミがどこに住んでいるか教えてください」。does を使わず、三人称単数の s を lives につける。"),
]


@gen("thinking_writing", 4, ["written_reasoning", "concept"])
def explain_difference(r):
    a, b, model = r.choice(PAIRS)
    return desc(f"次の2つの英文 A・B の意味の違いを、文の形（文構造）に注目して日本語で説明しなさい。\nA：{a}\nB：{b}", model,
                "動詞の後ろに続く語の並び方（A ＝ B か、人＋原形か、人＋to ～ か、疑問詞＋主語＋動詞か）が、だれが何をするかを決める。",
                [("A の形と意味を正しく説明している", 3), ("B の形と意味を正しく説明している", 3), ("違いを生む文構造を指摘している", 2)], d=4, p=8, lines=5,
                ap="A と B で違う部分に印をつけ、それぞれの動詞の後ろの型を判断する。",
                steps=["A と B を見比べ、違う部分を見つける。", "それぞれの文の型（SVOO / SVOC、使役、want＋人＋to、間接疑問文など）を判断する。",
                       "和訳を示し、「だれが何をするか」「たずねているかどうか」などの違いを説明する。"],
                alt=["それぞれの文を、動作をする人が主語になる短い文に言いかえる（例：I read this book. / You read this book.）と、違いが説明しやすい。"],
                pc=[("A の説明", 3), ("B の説明", 3), ("文構造の指摘", 2)],
                pit=["和訳だけを書いて、どの形が違いを生んでいるかを書かない。", "let と make を同じ意味だと考える。"])


# (場面, 模範解答, ポイント)
SITUATIONS = [
    ("初めて来た町で、通りかかった人に駅がどこにあるかを丁寧にたずねる。", "Excuse me. Could you tell me where the station is?",
     "Where is the station? を where the station is にして、Could you tell me の後ろに入れている。"),
    ("バス停で、次のバスが何時に出るかを近くの人にたずねる。", "Excuse me. Could you tell me what time the next bus leaves?",
     "What time does the next bus leave? の does を取り、leave を leaves にしている。"),
    ("お店で、店員にこの T シャツがいくらかをたずねる。", "Excuse me. Could you tell me how much this T-shirt is?",
     "How much is this T-shirt? の is を主語 this T-shirt の後ろに戻している。"),
    ("新しく来た ALT の先生に、どこの出身かを丁寧にたずねる。", "Could you tell me where you are from?",
     "Where are you from? の are を主語 you の後ろに戻している。"),
    ("図書館で、司書の先生に、この本をいつ返せばよいかをたずねる。", "Could you tell me when I should return this book?",
     "When should I return this book? の助動詞 should を主語 I の後ろに戻している。"),
    ("観光客に、博物館が何時に開くかを知っているかたずねる。", "Do you know what time the museum opens?",
     "What time does the museum open? の does を取り、open を opens にしている。"),
    ("友だちに、ケンが昨日なぜ学校を休んだのか知っているかたずねる。", "Do you know why Ken was absent from school yesterday?",
     "Why was Ken absent from school yesterday? の was を主語 Ken の後ろに戻している。"),
]


@gen("thinking_writing", 3, ["application", "written_reasoning"])
def write_indirect(r):
    sit, model, point = r.choice(SITUATIONS)
    return desc(f"次の場面で、間接疑問文を使って英語で1文（Excuse me. などのあいさつは別に加えてよい）たずねなさい。また、もとの疑問文から語順をどのように変えたかを日本語で説明しなさい。\n場面：{sit}",
                f"（解答例）{model}　説明：{point}", f"（解答例の解説）{point} Could you tell me ～? や Do you know ～? を使うと、直接たずねるより丁寧になる。",
                [("場面に合った間接疑問文を正しい語順で書いている", 3), ("動詞の形・文の終わりの記号が正しい", 2), ("もとの疑問文からの語順の変化を説明している", 3)], d=4, p=8, lines=4,
                ap="まず場面に合うふつうの疑問文を作り、それを Could you tell me ～? / Do you know ～? の後ろに入れる。",
                steps=["場面に合う疑問詞の疑問文を作る。", "do / does / did を取る、または be 動詞・助動詞を主語の後ろに戻して〈疑問詞＋主語＋動詞〉にする。",
                       "Could you tell me ～? などの後ろにつなぎ、文の終わりを ? にする。", "語順の変化を説明する。"],
                alt=["書いた文の疑問詞以下だけを読んで、ふつうの文の語順（主語＋動詞）になっているかを確かめる。"],
                pc=[("間接疑問文", 3), ("動詞の形と記号", 2), ("語順の変化の説明", 3)],
                pit=["Could you tell me where is the station? のように疑問文の語順のまま入れる。", "does を取ったあと、動詞の s を落とす。"])


TOPICS = [
    ("中学生が毎日新聞を読むこと", "important", "It is important for junior high school students to read newspapers every day because they can learn about the world."),
    ("中学生が料理を習うこと", "useful", "It is useful for junior high school students to learn cooking because they can help their families."),
    ("中学生が外国語を2つ学ぶこと", "difficult", "It is difficult for junior high school students to learn two foreign languages because they have many other subjects."),
    ("中学生が部活動に参加すること", "good", "It is good for junior high school students to join club activities because they can make many friends."),
    ("中学生がボランティア活動をすること", "important", "It is important for junior high school students to do volunteer work because they can help people in their town."),
    ("中学生が朝早く起きること", "good", "It is good for junior high school students to get up early because they can have breakfast and study in the morning."),
]


@gen("thinking_writing", 3, ["cross_unit", "written_reasoning", "application"], rel=["JH-ENG-G2-U03"])
def write_opinion(r):
    topic, adj, model = r.choice(TOPICS)
    return desc(f"「{topic}」について、あなたの意見を英語1文で書きなさい。ただし、It is ～ for … to ―. の形を使い、because を使って理由も同じ文の中に書くこと。",
                f"（解答例）{model}", "（解答例の解説）It is の後ろに意見を表す形容詞、for の後ろに人（目的格または名詞）、to の後ろに動詞の原形を置き、because の後ろに〈主語＋動詞〉で理由を続ける。反対の意見（It is not ～ / It is difficult ～）でも、形と理由が正しければよい。",
                [("It is ～ for … to ―. の形を正しく使っている", 3), ("because の後ろに〈主語＋動詞〉で理由を書いている", 3), ("つづり・語順・大文字・ピリオドが正しい", 2)], d=4, p=8, lines=4,
                ap="中2で学んだ because（理由）と、この単元の It is ～ for … to ―.（意見）を組み合わせる。",
                steps=[f"意見を表す形容詞を決める（例：{adj}）。", "It is ～ for junior high school students to ― の形で意見を書く。",
                       "because の後ろに〈主語＋動詞〉で理由を続ける。", "for の後ろが目的格（または名詞）、to の後ろが原形かを見直す。"],
                alt=["書いた文を To ― is ～ for …. の形に戻してみて、主語と述語の関係が自然かを確かめる。"],
                pc=[("It is ～ for … to ― の形", 3), ("because による理由", 3), ("表記の正確さ", 2)],
                pit=["for の後ろに主格（for they）を置く。", "because のあとを名詞だけ（because friends）にする。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(task, wrong, step, etype, tempt, fix, expl, steps, ap, alt, pit):
    return desc(f"{task}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい英文に書き直しなさい。", fix, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい英文に直している", 3), ("文法のルールを説明している", 1)], d=3, p=6, lines=4,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい英文", 3), ("ルールの説明", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix))


IND_ERR = [
    ("あなたはこの店が何時に閉まるか知っていますか。", "Do you know what time does this store close?", "Do you know what time this store closes?", "does this store close", "concept",
     "間接疑問文では does を使わず〈疑問詞＋主語＋動詞〉にする。does の三人称単数・現在の情報を動詞に移して closes にする。", "もとの疑問文 What time does this store close? をそのまま入れた。"),
    ("私はケンがどこにいるのか知らない。", "I don't know where is Ken.", "I don't know where Ken is.", "where is Ken", "concept",
     "間接疑問文では be 動詞を主語の後ろに置く。", "Where is Ken? の語順のまま入れた。"),
    ("彼女がいつ日本に来たのか教えてください。", "Please tell me when she come to Japan.", "Please tell me when she came to Japan.", "come", "condition",
     "もとの疑問文 When did she come to Japan? の did を取ったら、過去の情報を動詞に移して came にする。", "did を取ったあと、動詞を原形のまま残した。"),
    ("あなたは彼が何を買ったか知っていますか。", "Do you know what did he buy?", "Do you know what he bought?", "did he buy", "concept",
     "間接疑問文では did を使わず、動詞を過去形 bought にする。", "What did he buy? をそのまま入れた。"),
    ("私はユミが何をほしがっているかわかる。", "I know what Yumi want.", "I know what Yumi wants.", "want", "condition",
     "主語 Yumi は三人称単数で現在の文なので wants にする。", "does を取ったときに s も消えると考えた。"),
    ("だれがこの絵をかいたか知っていますか。", "Do you know who did paint this picture?", "Do you know who painted this picture?", "who did paint", "concept",
     "疑問詞 who が主語なので、もとの疑問文 Who painted this picture? の語順のまま入れる。did は使わない。", "間接疑問文ではいつも語順を変えると考え、did を補った。"),
    ("あなたのお兄さんが何歳か教えてください。", "Please tell me how your brother is old.", "Please tell me how old your brother is.", "how your brother is old", "concept",
     "how old は「何歳」というひとかたまりの疑問詞なので、切りはなさずに先頭に置く。", "how だけを疑問詞と考えた。"),
]


@gen("error_correction", 4, ["common_error", "condition_check"])
def err_indirect(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(IND_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", etype, tempt, fix, f"{rule}正しくは {fix}",
                    ["もとの疑問文を書き出し、主語と、主語の前に出ている語を確かめる。", f"「{where}」の部分の誤りを見つける：{rule}", f"正しい英文：{fix}"],
                    "間接疑問文は〈疑問詞＋主語＋動詞〉。do / does / did を取ったら、その情報（三単現・過去）を動詞に移す。疑問詞が主語ならそのまま。",
                    ["直した文の疑問詞以下を取り出し、ふつうの肯定文として正しいかを確かめる。"],
                    ["疑問文の語順のまま入れる。", "do / does / did を取ったあと、動詞の形を直さない。"])


STR_ERR = [
    ("おじは私に腕時計をくれた。", "My uncle gave a watch me.", "My uncle gave me a watch.", "a watch me", "notation",
     "SVOO は〈動詞＋人＋物〉の順。物を先にするなら gave a watch to me と to が必要。", "日本語の「腕時計を私に」の順に並べた。"),
    ("その知らせは私たちを幸せにした。", "The news made happy us.", "The news made us happy.", "made happy us", "notation",
     "SVOC は〈動詞＋A＋B〉の順。A（us）を先、状態 B（happy）を後に置く。", "日本語の「幸せに・私たちを」の語順につられた。"),
    ("私たちは彼をタクと呼ぶ。", "We call him as Taku.", "We call him Taku.", "as", "concept",
     "call A B は「A を B と呼ぶ」。A と B の間に as は入れない。", "日本語の「～として」につられて as を入れた。"),
    ("母は私に帽子を買ってくれた。", "My mother bought a cap to me.", "My mother bought a cap for me.", "to me", "condition",
     "buy は「相手のために～してあげる」動詞なので、言いかえでは for を使う。", "give と同じように to を使うと考えた。"),
    ("その映画は私を悲しくさせた。", "The movie made I sad.", "The movie made me sad.", "I", "notation",
     "SVOC の A の位置は目的語なので、目的格 me にする。", "「私は悲しい」と考え、主格の I を使った。"),
    ("あなたのノートを私に見せてください。", "Please show your notebook for me.", "Please show your notebook to me.", "for me", "condition",
     "show は物や情報が相手に届く動詞なので to を使う。", "「私のために」と考え、for を使った。"),
]


@gen("error_correction", 3, ["common_error", "concept"])
def err_structure(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(STR_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", etype, tempt, fix, f"{rule}正しくは {fix}",
                    ["文の動詞の後ろの型（SVOO か SVOC か）を確かめる。", f"「{where}」の部分の誤りを見つける：{rule}", f"正しい英文：{fix}"],
                    "SVOO は〈人＋物〉、SVOC は〈A＋B（A ＝ B）〉。語順と、A の位置の代名詞の格、言いかえるときの to / for を確かめる。",
                    ["A と B の間に is を入れて、SVOO か SVOC かを確かめてから語順を見直す。"],
                    ["日本語の語順のまま並べる。", "to と for を区別しない。"])


INF_ERR = [
    ("母は私を友だちの家に行かせてくれた。", "My mother let me to go to my friend's house.", "My mother let me go to my friend's house.", "to go", "concept",
     "let＋人＋動詞の原形。to は置かない。", "want＋人＋to ～ と同じ形だと考えた。"),
    ("伊藤先生は私たちを走らせた。", "Mr. Ito made us to run.", "Mr. Ito made us run.", "to run", "concept",
     "make＋人＋動詞の原形（使役）。to は置かない。", "不定詞の to が必要だと考えた。"),
    ("私はあなたに手伝ってほしい。", "I want you help me.", "I want you to help me.", "you help", "concept",
     "want＋人＋to＋原形。to が必要。", "let / make と同じように原形を続けた。"),
    ("私にとってテニスをすることは楽しい。", "It is fun for me play tennis.", "It is fun for me to play tennis.", "me play", "formula",
     "It is ～ for … to ―. の to が抜けている。", "for me の後ろにすぐ動詞を置けると考えた。"),
    ("彼にとって速く走ることは難しい。", "It is difficult for he to run fast.", "It is difficult for him to run fast.", "for he", "notation",
     "for は前置詞なので、後ろの代名詞は目的格 him にする。", "「彼が」走るので主格 he を使った。"),
    ("先生は私たちに静かにするように言った。", "The teacher told us be quiet.", "The teacher told us to be quiet.", "us be", "concept",
     "tell＋人＋to＋原形。to が必要。", "命令文 Be quiet. をそのままつなげた。"),
]


@gen("error_correction", 3, ["common_error", "computation"])
def err_inf(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(INF_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", etype, tempt, fix, f"{rule}正しくは {fix}",
                    ["文の動詞（let / make / help か、want / tell / ask か、It is ～ for … to ― か）を確かめる。", f"「{where}」の部分の誤りを見つける：{rule}", f"正しい英文：{fix}"],
                    "to がいる型（It is ～ for … to ―、want / tell / ask＋人＋to ～）と、to がいらない型（let / make / help＋人＋原形）を区別する。",
                    ["直した文を「to がいる型」「to がいらない型」の表に当てはめて確かめる。"],
                    ["let / make の後ろに to を入れる。", "want / tell の後ろの to を落とす。"])


GENERATORS = [indirect_choice, pattern_identify, to_or_for, it_for_to, bare_inf,
              combine_indirect, build_order, rewrite, tell_to, meaning,
              explain_difference, write_indirect, write_opinion,
              err_indirect, err_structure, err_inf]
