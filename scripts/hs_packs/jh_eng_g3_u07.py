"""単元パック：中学3年 英語 条件英作文（条件に合う英文・意見と理由・語順整序）。

英文の例・解答例・資料はすべてこのパックのためのオリジナル。資料の数値は架空のもの。
"""
from banks._common import desc, mc, order, sa, stim, table
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem,
                         tp)

UNIT_ID = "JH-ENG-G3-U07"

PREREQUISITES = [
    ("JH-ENG-G2-U03", "接続詞 because / if / when と助動詞 should。意見の理由や条件を英文で書くときの土台になる。"),
    ("JH-ENG-G2-U02", "不定詞・動名詞（want to ～, like ～ing, to ～「～するために」）。将来の夢や好きなことを書くときに使う。"),
    ("JH-ENG-G3-U03", "関係代名詞（who / which / that）で名詞を後ろから説明する形。語順整序で特によく問われる。"),
    ("JH-ENG-G3-U04", "間接疑問文（Do you know where he lives?）と SVOO・SVOC の語順。語順整序の中心になる文型。"),
]
EXTENSIONS = [
    ("HS-ENG-U10", "高校の「論理・表現」では、和文英訳や、主張・理由・結論の構成をもつ意見文へと発展する。"),
    ("SS-ENG-U02", "大学入試の自由英作文では、語数の多い意見文を、論理の流れと正確な文法で書く力が求められる。"),
    ("HS-ENG-U01", "語順整序で身につけた「主語＋動詞＋目的語・補語」の感覚を、高校では5文型として整理し直す。"),
]


def cap(s):
    return s[0].upper() + s[1:]


# ======================================================================
# 授業プリント
# ======================================================================

LESSON = lesson(
    goals=["問題文の条件（語数・文の数・使う語句・書く内容）を読み取り、すべての条件を満たす英文を書ける。",
           "自分の意見を、立場 → 理由（because / First, Second）→ まとめ の型で、理由を2つ挙げて書ける。",
           "主語と動詞を先に決め、間接疑問・後置修飾・不定詞などの語順のきまりに従って語句を正しく並べられる。",
           "書いた英文を、条件・時制・3人称単数・名詞の数・冠詞の観点から見直して直せる。"],
    duration=50,
    readiness=["be 動詞・一般動詞の現在形と過去形を、主語と時に合わせて使い分けられる（中1）。",
               "because / if / when を使って2つの文をつなげられる（中2）。",
               "日本語で、自分の考えとその理由を話したり書いたりできる（小学校・国語）。",
               "英語の文は「主語＋動詞」から始まることを知っている（小学校外国語・中1）。"],
    flow=[("導入：条件を見落とすと0点？", 5, "条件を1つ満たしていない答案を見せ、どこが足りないかを考えさせる"),
          ("条件の読み取りと語順", 12, "条件の種類と下線の引き方、語順の基本（例題1 語順整序）"),
          ("意見と理由の型", 13, "立場 → 理由2つ → まとめの型、理由の選び方（例題2）"),
          ("日本語の言いかえ", 10, "英語にしやすい日本語に直してから書く（例題3）"),
          ("見直しとまとめ", 10, "見直しチェックリストで自分の英文を点検し、確認問題3問")],
    sections=[
        intro("in1", "条件英作文は「条件を守ること」から始まる",
              "条件英作文では、「理由を含めて2文以上で」「because を使って」「15語以上で」などの条件が必ずついています。どんなにすばらしい英文を書いても、条件を1つでも満たしていなければ、大きく減点されてしまいます。反対に、むずかしい単語を使わなくても、条件をすべて守り、文法の正しい英文を書けば、しっかり得点できます。まずは、条件を正確に読み取ることから始めましょう。",
              bullets=["条件には、必ず下線を引いて番号をつける（①語数 ②文の数 ③使う語句 ④書く内容）。",
                       "書き終えたら、番号ごとに「満たしているか」をチェックする。",
                       "知っている単語と、自信のある文法で書くのがいちばん安全。"],
              points=[tp("条件「理由を含めて2文以上」に対して I like summer. だけを書いた答案を見せ、何点になるかを予想させる。",
                         ask="この答案に足りないものは何か。", expect="理由がない。1文しかない。", timing="導入の冒頭")]),
        definition("df1", "条件の種類と読み取り方",
                   "条件英作文の条件は、大きく分けて次の4種類です。問題文を読んだら、条件に下線を引いて番号をつけ、何をいくつ書けばよいかをはっきりさせます。",
                   bullets=["① 量の条件：「15語以上」「2文以上」「3文で」など。語数には , や . は数えない。",
                            "② 語句の条件：「because を使って」「比較級を使って」「現在完了形で」など。",
                            "③ 内容の条件：「理由を1つ含めて」「賛成か反対かを明らかにして」「相手にたずねる文を入れて」など。",
                            "④ 場面の条件：「留学生へのメッセージ」「ALT の先生へのお礼」など。相手と場面に合った言い方を選ぶ。"],
                   conditions=["質問に答える問題では、まず質問に直接答える（Which ～? なら選んだものを、What did you ～? なら過去形で）。",
                               "I'm や don't などの短縮形は1語と数える（数え方の指示があるときはそれに従う）。"],
                   points=[tp("同じテーマで条件だけを変えた問題を3つ並べ、書く内容がどう変わるかを比べさせる。",
                              caution="質問の時制（did / will / have）と答えの時制がずれる誤りが多い。")]),
        theorem("th1", "意見と理由の型",
                "I think (that) ～. ／ I agree (disagree) with ～. → I have two reasons. First, ～. Second, ～. → For these reasons, ～.",
                ["最初の文で、立場（賛成・反対、選んだもの）をはっきり書く。",
                 "理由は because ～ で1文にするか、First, ～. Second, ～. で2つに分けて書く。",
                 "2つの理由は、違う観点（楽しさ・健康・時間・お金・人とのつながり など）から選ぶ。",
                 "具体例（For example, ～）や自分の経験を加えると、説得力が増す。",
                 "最後に、For these reasons, ～ / So ～ で立場をもう一度まとめる（語数に余裕があるとき）。"],
                body="この型を使えば、どんなテーマでも「何を書けばよいか」で迷わなくなります。理由が具体的であるほど、読み手に伝わる英文になります。",
                points=[tp("理由の観点カード（楽しさ・健康・時間・お金・人とのつながり・将来）を配り、テーマに合うものを2枚選ばせてから書かせる。",
                           ask="2つの理由が「楽しい」と「おもしろい」では、なぜよくないのか。", expect="同じ観点の言いかえで、理由が1つしかないのと同じだから。")]),
        definition("df2", "語順の基本",
                   "英語は語順で意味が決まる言語です。語順整序でも自由英作文でも、まず「主語＋動詞」を決め、そのあとに目的語や説明の語句を続けます。",
                   bullets=["基本：主語＋動詞＋（目的語・補語）＋（場所）＋（時）　例 I played tennis in the park yesterday.",
                            "間接疑問：疑問詞のあとは「主語＋動詞」の語順　例 Do you know where he lives?",
                            "名詞を後ろから説明：the girl playing the piano ／ the book I bought ／ a friend who lives in Osaka",
                            "SVOO・SVOC：show 人 物（I showed her my pictures.）／ make 人 形容詞（The news made us happy.）",
                            "It is ～ for 人 to …：It is fun for me to sing English songs."],
                   conditions=["語順整序では、文頭の語も小文字で示されることが多い。完成した文の最初の文字は大文字にする。",
                               "まず動詞を見つけ、その主語を決めると、残りの語句の位置が決まりやすい。"],
                   points=[tp("語句カードを使い、生徒にまず「動詞のカード」を見つけさせてから並べさせる。", timing="例題1の前")]),
        derivation("dv1", "条件英作文の書き方の手順（なぜこの順番がよいのか）",
                   ["① 条件に下線を引き、番号をつける → 何をいくつ書けばよいかがはっきりし、条件の見落としを防げる。",
                    "② 書く内容を日本語で短くメモする（立場・理由1・理由2）→ 英語を考える前に内容を決めておくと、途中で迷わない。",
                    "③ メモを「英語にしやすい日本語」に言いかえる（主語をはっきりさせる・やさしい言い方にする）→ 知っている単語と文法で書ける。",
                    "④ 主語と動詞を決めてから英文を書く → 語順の誤りが減る。",
                    "⑤ 見直す：条件 → 時制 → 3人称単数の s → 名詞の数（単数・複数）と冠詞 → つづり の順に点検する → よくある誤りを確実に直せる。"],
                   body="条件英作文の失点の多くは、①条件の見落とし、②日本語をそのまま直訳した不自然な英文、③基本的な文法の誤り、の3つから生まれます。この手順は、その3つを順番に防ぐためのものです。",
                   points=[tp("手順③の「日本語の言いかえ」を全員で練習する。「私の町には公園が多い」を主語のはっきりした日本語に直させる。",
                              ask="「私の町には公園が多い」の主語を「公園」にすると、どんな英文になるか。", expect="There are many parks in my town.")]),
        example("ex1", "例題1　語順整序（間接疑問）",
                "日本語に合うように、（　）内の語句を並べかえなさい。文頭にくる語も小文字で示しています。\nあなたは、そのお祭りがいつ始まるか知っていますか。\n（ the festival / do / when / know / starts / you ）",
                ["文の骨組みは「あなたは知っていますか」→ Do you know ～?",
                 "「お祭りがいつ始まるか」は間接疑問。疑問詞 when のあとは「主語＋動詞」の語順になる。",
                 "when the festival starts（3人称単数なので starts）を know の目的語として後ろに置く。"],
                "Do you know when the festival starts?",
                thinking="間接疑問では、疑問詞のあとをふつうの文の語順（主語＋動詞）にする。does を使わない。",
                points=[tp("Do you know when does the festival start? と書く生徒に、疑問文の語順になるのは文の最初の部分だけであることを確認させる。")],
                misconceptions=[("Do you know when does the festival start?", "間接疑問の部分は「主語＋動詞」の語順。when the festival starts とする。")]),
        example("ex2", "例題2　意見と理由を書く",
                "次の質問に、理由を2つ含めて、25語程度の英語で答えなさい。\nWhich do you like better, reading books or watching movies?",
                ["① 条件に下線：「理由を2つ」「25語程度」。",
                 "② 日本語メモ：立場＝本を読むほうが好き／理由1＝自分のペースで読める／理由2＝新しい言葉を学べる。",
                 "③ 型にあてはめる：I like ～ better. → First, ～. Second, ～.",
                 "④ 見直し：語数（26語）・3人称単数・名詞の数を確かめる。"],
                "I like reading books better. First, I can read at my own speed. Second, I can learn many new words from books. So reading is better for me.（26語）",
                thinking="質問の形（Which do you like better, A or B?）をそのまま使って答えの文を作り、理由を First / Second で2つ続ける。",
                points=[tp("理由の観点が重なっていないか（「楽しい」と「おもしろい」になっていないか）を、ペアで確認させる。",
                           ask="この2つの理由は、それぞれどんな観点か。", expect="1つ目は「時間・ペース」、2つ目は「学び」。")]),
        example("ex3", "例題3　日本語を言いかえてから英語にする",
                "次の日本語を英語に直しなさい。\n(1) 私の町には古いお寺がたくさんあります。　(2) 英語の歌を聞くのは私の楽しみです。",
                ["(1) 「町には」を主語にしない。「古いお寺がたくさんある」→ There are ～ で表す（My town has ～ も可）。",
                 "(1) many old temples は複数なので There are。場所 in my town を最後に置く。",
                 "(2) 「～するのは私の楽しみ」→「私は～を聞くことを楽しむ」と言いかえる。",
                 "(2) enjoy の後ろは動名詞：I enjoy listening to English songs.（Listening to English songs is fun for me. も可）"],
                "(1) There are many old temples in my town.　(2) I enjoy listening to English songs.",
                thinking="日本語の文の形のまま英語にしようとせず、主語と動詞がはっきりした日本語に言いかえてから書く。",
                points=[tp("(1) を My town is many old temples. と書く生徒に、「町＝お寺」という意味になってしまうことを確認させる。")],
                misconceptions=[("My town is many old temples.", "「町＝お寺」の意味になる。There are many old temples in my town. とする。"),
                                ("I enjoy to listen to English songs.", "enjoy の後ろは動名詞。listening にする。")]),
        board("bd1", "板書案",
              [("① 条件を読む", ["条件に下線＋番号", "量：語数・文の数", "語句：because・比較級など", "内容：理由・立場", "質問の時制に合わせる"]),
               ("② 意見と理由の型", ["I think (that) ～.", "I have two reasons.", "First, ～. Second, ～.", "For example, ～.", "For these reasons, ～."]),
               ("③ 語順と見直し", ["主語＋動詞を先に", "間接疑問：疑問詞＋S＋V", "名詞＋説明（後ろから）", "見直し：条件→時制→s", "→名詞の数・冠詞→つづり"])],
              points=[tp("③の見直しの順番は、毎回の英作文で生徒が自分で書き出せるように、ノートの表紙に貼らせる。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("最初の数回は、書き始める前に条件の番号と日本語メモを提出させ、条件の読み取りを習慣にする。", timing="授業全体"),
               tp("「日本語をそのまま英語に置きかえる」誤り（This town lives many people. など）は、主語と動詞を先に決める練習で減らす。",
                  ask="「この町には多くの人が住んでいる」で、住んでいるのはだれか。", expect="多くの人。だから主語は many people。"),
               tp("Because ～. だけの文（主節のない文）は、入試でも減点の多い誤り。because は文の後半に置くように指導する。",
                  caution="会話では Because ～. と答えることがあるが、英作文では I like ～ because ～. の形で書かせる。"),
               tp("語数の多い答案より、条件を満たした正確な答案が高く評価されることを伝え、自信のある表現で書かせる。"),
               tp("問題プリント D の誤答例は「文法の誤り」「条件の未達成」「語順の誤り」の3種類に分けて振り返らせる。")],
              misconceptions=[("I like summer. Because I can swim.", "Because ～ だけでは文にならない。I like summer because I can swim. と1文にする。"),
                              ("This town lives many people.", "住むのは人。Many people live in this town. とする。"),
                              ("Do you know where does he live?", "間接疑問は主語＋動詞の語順。Do you know where he lives?"),
                              ("理由を2つ書けと言われたので、同じ内容を2回書いた。", "違う観点の理由を2つ書く。")]),
        summary("sm1", "まとめ",
                ["条件に下線と番号をつけ、書き終えたら1つずつ満たしているかを確かめる。",
                 "意見文は、立場 → 理由（because / First, Second）→ まとめ の型で書く。理由は違う観点から2つ。",
                 "日本語は、主語と動詞がはっきりした「英語にしやすい日本語」に言いかえてから書く。",
                 "語順は「主語＋動詞」を先に決める。間接疑問は疑問詞＋主語＋動詞。",
                 "見直しは、条件 → 時制 → 3人称単数の s → 名詞の数・冠詞 → つづり の順。"]),
        check("ck1", "確認問題",
              [("「I like dogs. Because they are cute.」を正しい1文に直しなさい。", "I like dogs because they are cute."),
               ("「彼がだれか知っていますか」を英語に直しなさい。", "Do you know who he is?"),
               ("意見文で2つの理由を書くとき、注意することを1つ答えなさい。", "同じ内容の言いかえにならないよう、違う観点（楽しさ・健康・時間など）から理由を選ぶ。")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

# 語順整序（短い文）：(日本語, 正しい順の語句, 文末記号, ポイント)
ORD_SHORT = [
    ("私は兄に宿題を手伝ってもらいたい。", ["I", "want", "my brother", "to help", "me", "with", "my homework"], ".", "want 人 to ～「人に～してもらいたい」"),
    ("これは祖母が作ったケーキです。", ["this", "is", "the cake", "my grandmother", "made"], ".", "名詞のあとに「主語＋動詞」を続けて後ろから説明する（接触節）"),
    ("あなたは彼がどこに住んでいるか知っていますか。", ["do", "you", "know", "where", "he", "lives"], "?", "間接疑問は疑問詞のあとが「主語＋動詞」"),
    ("私にとって英語を話すことは楽しい。", ["it", "is", "fun", "for me", "to speak", "English"], ".", "It is ～ for 人 to …"),
    ("この歌は多くの若者に愛されています。", ["this song", "is", "loved", "by", "many", "young people"], ".", "受け身 be 動詞＋過去分詞"),
    ("彼女は私たちのクラスでいちばん背が高い。", ["she", "is", "the tallest", "in", "our", "class"], ".", "最上級＋in（範囲）"),
    ("私は鳥のように飛べたらいいのに。", ["I wish", "I could", "fly", "like", "a bird"], ".", "I wish＋主語＋過去形（仮定法）"),
    ("サッカーをしている男の子たちは私の友だちです。", ["the boys", "playing", "soccer", "are", "my", "friends"], ".", "現在分詞の後置修飾（名詞＋～ing＋語句）"),
    ("その知らせは私たちをとても幸せにした。", ["the news", "made", "us", "very", "happy"], ".", "make 人 形容詞（SVOC）"),
    ("私は彼に駅への道をたずねた。", ["I", "asked", "him", "the way", "to", "the station"], ".", "ask 人 物（SVOO）"),
    ("私はまだ昼食を食べていません。", ["I", "haven't", "eaten", "lunch", "yet"], ".", "現在完了の否定文＋yet"),
    ("あなたは今までに京都を訪れたことがありますか。", ["have", "you", "ever", "visited", "Kyoto"], "?", "現在完了（経験）の疑問文＋ever"),
]

# 語順整序（長い文）
ORD_LONG = [
    ("私は、生徒は毎日朝食を食べるべきだと思います。", ["I", "think", "that", "students", "should", "eat", "breakfast", "every day"], ".", "I think that＋主語＋should＋動詞の原形"),
    ("英語を勉強することは、私たちが多くの人と話す助けになります。", ["studying English", "helps", "us", "talk", "with", "many", "people"], ".", "動名詞の主語＋help 人 動詞の原形"),
    ("私が夏をいちばん好きな理由は、海で泳げることです。", ["the reason", "I", "like", "summer", "the best", "is", "that", "I can swim", "in the sea"], ".", "The reason (that) I ～ is that …"),
    ("私たちが住んでいる町には、美しい公園がたくさんあります。", ["the town", "we", "live in", "has", "a lot of", "beautiful", "parks"], ".", "名詞＋主語＋動詞（接触節）が主語になる文"),
    ("あなたがどの国を訪れたいか、私に教えてください。", ["please", "tell", "me", "which", "country", "you", "want", "to visit"], ".", "tell 人＋間接疑問（which＋名詞＋主語＋動詞）"),
    ("私は、将来多くの人を助けられる医者になりたいです。", ["I", "want", "to be", "a doctor", "who", "can", "help", "many people"], ".", "関係代名詞 who（主格）"),
    ("図書館で本を読むことは、家で読むよりも楽しいと思います。", ["I", "think", "reading", "in the library", "is", "more fun", "than", "reading at home"], ".", "動名詞の主語＋比較級＋than"),
    ("私にとって、毎朝早く起きることは難しいです。", ["it", "is", "difficult", "for me", "to get up", "early", "every morning"], ".", "It is ～ for 人 to …"),
    ("私たちの町のごみを減らすために、私たちは何ができるでしょうか。", ["what", "can", "we", "do", "to reduce", "the trash", "in our town"], "?", "疑問詞＋助動詞の疑問文＋to ～（目的）"),
    ("これは、私が今までに読んだ中でいちばんおもしろい本です。", ["this", "is", "the most", "interesting", "book", "I", "have", "ever", "read"], ".", "最上級＋名詞＋I have ever＋過去分詞"),
]


def build_sent(parts, end):
    return cap(" ".join(parts)) + end


@gen("basic_check", 5, ["computation", "application"])
def order_build(r):
    jp, parts, end, point = r.choice(ORD_SHORT)
    sent = build_sent(parts, end)
    return order(f"日本語の意味になるように、次の語句を並べかえて英文を作りなさい。文頭にくる語も小文字で示しています。\n{jp}", parts,
                 f"{sent}　ポイント：{point}。", d=2, p=2,
                 ap="まず語句の中から動詞を見つけ、その主語を決めて「主語＋動詞」の骨組みを作る。残りの語句は、文法のきまりに合わせて後ろに置く。",
                 steps=["日本語の文の「だれが・どうする」を確かめる。", "語句から動詞を見つけ、主語＋動詞を並べる。",
                        f"ポイントの形を使って残りの語句を並べる：{point}。", f"完成文：{sent}"],
                 alt=["完成した英文を日本語に訳し直して、問題の日本語と同じ意味になるかを確かめる。"],
                 pc=[("主語と動詞の位置が正しい", 1), ("残りの語句の順序が正しい", 1)],
                 pit=["日本語の語順のまま英語の語句を並べる。", "疑問文の語順と間接疑問の語順を混同する。"])


# 条件に合う英文：(条件, 正答, [(誤答, 理由)])
COND = [
    ("あなたが好きなスポーツとその理由を、because を使って1文で書く。", "I like basketball because I can play it with my friends.",
     [("I like basketball.", "理由が書かれておらず、because も使っていない。"),
      ("Because I can play basketball with my friends.", "because の部分だけで、主節（I like ～）のない不完全な文である。"),
      ("I like basketball, so I play it every day.", "so を使っており、because を使うという条件に合わない。")]),
    ("週末にしたことを、過去形を使って1文で書く。", "I visited my grandparents last Sunday.",
     [("I will visit my grandparents next Sunday.", "未来のことで、したこと（過去）ではない。"),
      ("I visit my grandparents every Sunday.", "現在形で習慣を表しており、過去形ではない。"),
      ("I am visiting my grandparents now.", "現在進行形で、過去形ではない。")]),
    ("将来の夢を、want to を使って1文で書く。", "I want to be a teacher in the future.",
     [("I want a new bike.", "将来の夢ではなく欲しい物を述べており、want to も使っていない。"),
      ("I wanted to be a pilot when I was little.", "小さいころの夢で、これからの将来の夢になっていない。"),
      ("I like my English teacher.", "好きな人を述べており、将来の夢を書いていない。")]),
    ("相手に何かをいっしょにしようと提案する文を1文で書く。", "Why don't we clean the park together next Saturday?",
     [("We cleaned the park together last Saturday.", "過去の出来事を述べており、提案になっていない。"),
      ("Do you like the park near our school?", "好みをたずねているだけで、提案になっていない。"),
      ("I cleaned the park by myself.", "自分がしたことを述べており、相手への提案ではない。")]),
    ("2つの季節を比べて、比較級を使って1文で書く。", "Summer is hotter than spring.",
     [("Summer is the hottest season.", "最上級で、比較級ではない。"),
      ("I like summer very much.", "2つのものを比べていない。"),
      ("Summer is hot, and spring is warm.", "2つの季節を述べているが、比較級を使っていない。")]),
    ("自分の経験を、現在完了形を使って1文で書く。", "I have climbed Mt. Fuji twice.",
     [("I climbed Mt. Fuji last year.", "過去形で、現在完了形ではない。"),
      ("I have to climb Mt. Fuji.", "have to は「～しなければならない」で、現在完了形ではない。"),
      ("I am going to climb Mt. Fuji.", "これからの予定で、経験を表していない。")]),
    ("相手に何かをしてくれるようにお願いする文を1文で書く。", "Could you open the window, please?",
     [("I opened the window.", "自分がしたことを述べており、お願いではない。"),
      ("Can I open the window?", "自分がしてよいか許可を求める文で、相手へのお願いではない。"),
      ("You opened the window.", "相手がしたことを述べているだけで、お願いではない。")]),
    ("自分の意見を、I think のあとに主語と動詞のそろった文を続けて書く。", "I think that reading books is important.",
     [("I think reading books.", "think のあとに主語と動詞のそろった文がない。"),
      ("Reading books is important.", "I think を使っていない。"),
      ("I think that important reading books.", "that のあとに動詞がなく、語順も誤っている。")]),
    ("留学生に、自分の町のよいところを There is / There are を使って1文で伝える。", "There is a beautiful lake in my town.",
     [("My town is beautiful.", "There is / There are を使っていない。"),
      ("There are a big park in my town.", "a big park は単数なので There is にする。"),
      ("There is many shops in my town.", "many shops は複数なので There are にする。")]),
    ("「もし明日～なら…」と、if を使って明日の予定を1文で書く。", "If it is sunny tomorrow, I will go fishing.",
     [("If it will be sunny tomorrow, I will go fishing.", "条件を表す if の中は、未来のことでも現在形（is）にする。"),
      ("I will go fishing tomorrow.", "if を使っていない。"),
      ("If it was sunny yesterday, I went fishing.", "昨日のことで、明日の予定ではない。")]),
    ("図書館へ行った目的を、to ～（～するために）を使って1文で書く。", "I went to the library to borrow some books.",
     [("I went to the library yesterday.", "行った目的が書かれていない。"),
      ("I like to go to the library.", "to go は「行くこと」の意味で、目的を表していない。"),
      ("I went to the library for borrow some books.", "for のあとに動詞の原形は置けない。目的は to borrow で表す。")]),
]


@gen("basic_check", 5, ["condition_check", "concept"])
def cond_select(r):
    cond, ok, wrongs = r.choice(COND)
    return mc(f"次の条件をすべて満たす英文として最も適切なものを選びなさい。\n条件：{cond}", [ok] + [w for w, _ in wrongs],
              f"{ok}　条件を「内容」「使う語句」「文の形」に分けて、すべて満たしているかを確かめる。", d=2,
              ap="条件を、①何を書くか（内容）、②何を使うか（語句・文法）、③文として完成しているか、の3つに分けて、選択肢を1つずつ点検する。",
              steps=["条件に下線を引き、内容・語句・文の形に分ける。", "各選択肢が指定の語句・文法を使っているかを確かめる。",
                     "内容が条件に合っているか、文として正しいかを確かめる。", f"すべて満たすのは：{ok}"],
              alt=["誤りの選択肢を、条件を満たすように直してみて、どの条件が欠けていたかを確かめる。"],
              pc=[("条件を分けて点検している", 1), ("正しい英文を選んでいる", 1)],
              pit=["指定の語句が入っていれば、内容や文の形を確かめずに選ぶ。"],
              why={w: (reason, "条件の読み落とし") for w, reason in wrongs})


# 意見・理由の表現：(（　）を含む英文, 正答, [(誤答, 理由)], 意味)
OPEX = [
    ("I like winter (　　) I can enjoy skiing.", "because",
     [("so", "so は結果を表す。「スキーができるから冬が好き」は理由なので because。"),
      ("but", "but は反対の内容をつなぐ語で、前後は反対の内容ではない。"),
      ("if", "if は「もし～なら」で、意味が合わない。")], "スキーを楽しめるので、私は冬が好きです。"),
    ("It was raining, (　　) I stayed home.", "so",
     [("because", "because を使うと「家にいたので雨が降っていた」となり、原因と結果が逆になる。"),
      ("but", "雨が降っていたことと家にいたことは反対の内容ではない。"),
      ("or", "or は「または」で、意味が合わない。")], "雨が降っていたので、私は家にいました。"),
    ("I (　　) with your idea.", "agree",
     [("think", "think with とは言わない。「～に賛成する」は agree with。"),
      ("say", "say with とは言わない。"),
      ("like", "like with とは言わない。like は目的語を直接とる。")], "私はあなたの考えに賛成です。"),
    ("In my (　　), we should use bikes more.", "opinion",
     [("think", "think は動詞なので my のあとに置けない。In my opinion で「私の意見では」。"),
      ("idea", "in my idea とは言わない。"),
      ("reason", "in my reason とは言わない。reason は「理由」。")], "私の意見では、私たちはもっと自転車を使うべきです。"),
    ("I have two reasons. (　　), it is good for our health. Second, it is fun.", "First",
     [("Then", "Then は「それから」で、理由を挙げ始める1つ目には使わない。"),
      ("Finally", "Finally は最後の項目を示す語で、1つ目の理由には使わない。"),
      ("But", "But は反対の内容をつなぐ語で、理由の列挙には使わない。")], "理由は2つあります。1つ目に、健康によいです。2つ目に、楽しいです。"),
    ("(　　) do you think so?", "Why",
     [("What", "What do you think so? とは言わない。理由をたずねるのは Why。"),
      ("How", "How do you think so? とは言わない。理由をたずねるのは Why。"),
      ("Where", "Where は場所をたずねる語で、意味が合わない。")], "なぜそう思うのですか。"),
    ("I think (　　) students should have more time to sleep.", "that",
     [("what", "what は「何」で、意見の内容の文を導く語ではない。"),
      ("because", "I think because ～ では、意見の内容がなくなってしまう。"),
      ("which", "which は「どちら」で、意見の内容の文を導く語ではない。")], "私は、生徒はもっと眠る時間をもつべきだと思います。"),
    ("For these (　　), I think school uniforms are necessary.", "reasons",
     [("reason", "these のあとは複数形の reasons にする。"),
      ("opinion", "For these opinion とは言わない。these のあとは複数形の名詞。"),
      ("because", "because は接続詞で、these のあとに置けない。")], "これらの理由から、私は制服は必要だと思います。"),
    ("Reading books is more interesting (　　) watching TV.", "than",
     [("as", "as は as ～ as の形で使う。比較級のあとは than。"),
      ("then", "then は「それから」。than とつづりが似ているが意味が違う。"),
      ("that", "比較級のあとに that は置けない。")], "本を読むことはテレビを見ることよりもおもしろいです。"),
    ("I'm (　　) of my town because it has a long history.", "proud",
     [("interested", "「～に興味がある」は be interested in で、of とは使わない。"),
      ("famous", "famous は「有名な」で、意味が合わない。famous of とも言わない。"),
      ("good", "「～が得意だ」は be good at で、意味も前置詞も合わない。")], "長い歴史があるので、私は自分の町を誇りに思っています。"),
    ("Some people say that summer is the best season. (　　), I don't agree.", "However",
     [("So", "So は結果を表す。前の内容と反対の意見を述べるので合わない。"),
      ("Because", "Because ～ は理由を表す語で、文の初めに置いてこの意味にはできない。"),
      ("For example", "For example は具体例を示す語で、反対の意見を導かない。")], "夏がいちばんよい季節だと言う人もいます。しかし、私は賛成しません。"),
]


@gen("basic_check", 5, ["concept", "common_error"])
def opinion_expr(r):
    s, ok, wrongs, jp = r.choice(OPEX)
    return mc(f"意見や理由を述べる文です。日本語の意味に合うように、（　）に入る最も適切な語を選びなさい。\n{s}\n（{jp}）", [ok] + [w for w, _ in wrongs],
              f"{ok}　{jp}", d=2,
              ap="日本語の意味から、前後の文の関係（理由・結果・反対・列挙）や決まった言い方（agree with / in my opinion など）を考える。",
              steps=["日本語の意味を確かめる。", "（　）の前後の語とのつながり（前置詞・語順）を確かめる。", f"意味と形の両方に合う語は {ok}。"],
              alt=["選んだ語を入れて英文を読み、日本語の意味と同じになるかを確かめる。"],
              pc=[("前後の関係を考えている", 1), ("正しい語を選んでいる", 1)],
              pit=["because と so を逆に使う。", "決まった言い方（agree with, in my opinion）を覚えていない。"],
              why={w: (reason, "意見・理由の表現の誤用") for w, reason in wrongs})


# 和文に合う英文：(日本語, 正答, [(誤答, 理由)])
JPMC = [
    ("私の兄は毎日サッカーをします。", "My brother plays soccer every day.",
     [("My brother play soccer every day.", "主語が3人称単数なので plays にする。"),
      ("My brother is play soccer every day.", "be 動詞と一般動詞の原形を並べることはできない。"),
      ("My brother plays the soccer every day.", "スポーツ名には the をつけない。")]),
    ("私はこの本をまだ読んでいません。", "I haven't read this book yet.",
     [("I haven't read this book already.", "否定文の「まだ」は yet。already は肯定文で「もう」。"),
      ("I haven't readed this book yet.", "read の過去分詞は read（readed という形はない）。"),
      ("I don't read this book yet.", "現在形では「まだ～していない」の意味にならない。現在完了を使う。")]),
    ("この寺は約400年前に建てられました。", "This temple was built about 400 years ago.",
     [("This temple built about 400 years ago.", "be 動詞がない。受け身は be 動詞＋過去分詞。"),
      ("This temple was build about 400 years ago.", "build の過去分詞は built。"),
      ("This temple is built about 400 years ago.", "過去のことなので be 動詞は was にする。")]),
    ("私は、ギターをひいている女の子を知っています。", "I know the girl playing the guitar.",
     [("I know the playing the guitar girl.", "2語以上の説明（playing the guitar）は名詞の後ろに置く。"),
      ("I know the girl plays the guitar.", "plays では1つの文に動詞が2つになる。playing か who plays にする。"),
      ("I know the girl played the guitar.", "「ひいている」は現在分詞 playing で表す。")]),
    ("彼がいつ来るか知っていますか。", "Do you know when he will come?",
     [("Do you know when will he come?", "間接疑問では疑問詞のあとを「主語＋動詞」の語順にする。"),
      ("Do you know when he come will?", "will は動詞の前に置く。"),
      ("Do you know he will come when?", "疑問詞 when は「いつ来るか」の部分の先頭に置く。")]),
    ("私にとって数学を勉強することは大切です。", "It is important for me to study math.",
     [("It is important for me study math.", "study の前に to が必要。"),
      ("It is important to me for study math.", "for のあとに動詞の原形は置けない。"),
      ("That is important for me to study math.", "この形の主語は It を使う。")]),
    ("もし私があなたなら、そのプレゼントを買うのに。", "If I were you, I would buy the present.",
     [("If I am you, I will buy the present.", "現実とちがう仮定なので、仮定法（were / would）を使う。"),
      ("If I were you, I will buy the present.", "仮定法では、後半も would＋動詞の原形にする。"),
      ("If I were you, I would bought the present.", "would のあとは動詞の原形 buy にする。")]),
    ("これは私の父が撮った写真です。", "This is the picture my father took.",
     [("This is the picture my father took it.", "the picture を後ろから説明する形では、it を重ねて置かない。"),
      ("This is the picture took my father.", "説明の部分は「主語＋動詞」の語順（my father took）にする。"),
      ("This is my father took the picture.", "文の形がくずれている。the picture を後ろから説明する形にする。")]),
    ("彼女は私たちのクラスでいちばん速く走ります。", "She runs the fastest in our class.",
     [("She runs the fastest of our class.", "「クラスで」のような範囲は in で表す。of は「～の中で」と複数のものを表すときに使う。"),
      ("She runs faster in our class.", "比較級では「いちばん」の意味にならない。"),
      ("She run the fastest in our class.", "主語が3人称単数なので runs にする。")]),
    ("母は私に部屋を掃除するように言いました。", "My mother told me to clean my room.",
     [("My mother told me clean my room.", "tell 人 to ～ の to が必要。"),
      ("My mother said me to clean my room.", "say は「人」を目的語にとって to ～ を続けることができない。"),
      ("My mother told to me clean my room.", "tell のすぐあとに「人」を置く。")]),
    ("私は3年間英語を勉強しています。", "I have studied English for three years.",
     [("I study English for three years.", "過去から今まで続いていることは、現在完了で表す。"),
      ("I have studied English since three years.", "期間は for、始まった時点は since で表す。"),
      ("I have study English for three years.", "have のあとは過去分詞 studied にする。")]),
]


@gen("basic_check", 5, ["computation", "common_error"])
def jp_choice(r):
    jp, ok, wrongs = r.choice(JPMC)
    return mc(f"次の日本語の意味を正しく表している英文を1つ選びなさい。\n{jp}", [ok] + [w for w, _ in wrongs],
              f"{ok}　主語と動詞の形、語順、決まった言い方を1つずつ確かめる。", d=2,
              ap="選択肢どうしの違う部分だけに注目し、そこで使われている文法のきまり（3人称単数・時制・語順・前置詞など）を確かめる。",
              steps=["選択肢を比べて、違っている部分に印をつける。", "その部分の文法のきまりを確かめる。", f"きまりに合っているのは：{ok}"],
              alt=["選んだ英文を日本語に訳し直して、問題の日本語と同じ意味になるかを確かめる。"],
              pc=[("違いの部分の文法を確かめている", 1), ("正しい英文を選んでいる", 1)],
              pit=["英文全体をなんとなく読んで、自然に見えるものを選ぶ。"],
              why={w: (reason, "文法のきまりの誤用") for w, reason in wrongs})


# ======================================================================
# B 標準演習
# ======================================================================

# 和文英訳：(日本語, 解答例, 別解, ポイント)
TRANS = [
    ("私は昨日から何も食べていません。", "I haven't eaten anything since yesterday.", ["I have not eaten anything since yesterday."],
     "過去から今まで続く状態は現在完了。否定文の「何も」は anything、起点は since。"),
    ("あなたは何回京都に行ったことがありますか。", "How many times have you been to Kyoto?", ["How many times have you visited Kyoto?", "How often have you been to Kyoto?"],
     "回数をたずねる How many times＋現在完了（経験）の疑問文。"),
    ("私は彼女がだれなのか知りません。", "I don't know who she is.", ["I do not know who she is."],
     "間接疑問：疑問詞 who のあとは「主語＋動詞」（she is）。"),
    ("これは日本でいちばん長い川です。", "This is the longest river in Japan.", [],
     "最上級 the longest＋名詞。範囲は in Japan。"),
    ("あなたの写真を私たちに見せてくれませんか。", "Could you show us your pictures?",
     ["Can you show us your pictures?", "Will you show us your pictures?", "Could you show your pictures to us?", "Can you show your pictures to us?",
      "Could you show us your picture?", "Can you show us your picture?"],
     "依頼の Could you ～? と、show 人 物（SVOO）の語順。"),
    ("その知らせを聞いて、私はうれしくなりました。", "The news made me happy.", ["I was happy to hear the news.", "I became happy when I heard the news."],
     "make 人 形容詞「人を～にする」（SVOC）。感情の原因を表す to 不定詞でもよい。"),
    ("私は医者になるために一生けんめい勉強しています。", "I am studying hard to become a doctor.",
     ["I'm studying hard to become a doctor.", "I study hard to become a doctor.", "I am studying hard to be a doctor.", "I study hard to be a doctor."],
     "目的を表す to 不定詞「～するために」。a doctor の a を忘れない。"),
    ("私には、海外に住んでいるおばがいます。", "I have an aunt who lives abroad.",
     ["I have an aunt that lives abroad.", "I have an aunt living abroad.", "I have an aunt who lives in a foreign country."],
     "関係代名詞 who（主格）で an aunt を後ろから説明する。who のあとの動詞は3人称単数。"),
    ("もっと時間があればいいのに。", "I wish I had more time.", ["I wish I could have more time."],
     "現在の事実とちがう願望は I wish＋主語＋過去形（仮定法）。"),
    ("この箱は重すぎて私には運べません。", "This box is too heavy for me to carry.", ["This box is so heavy that I can't carry it.", "This box is so heavy that I cannot carry it."],
     "too ～ for 人 to …「～すぎて人は…できない」。so ～ that 人 can't … でもよい。"),
    ("窓を開けてもいいですか。", "May I open the window?", ["Can I open the window?"],
     "許可を求める May I ～? / Can I ～?"),
]


@gen("standard_practice", 5, ["computation", "application"])
def translate_sa(r):
    jp, ans, v, point = r.choice(TRANS)
    kw = {"v": v} if v else {}
    return sa(f"次の日本語の意味を表す英文を書きなさい。\n{jp}", ans, f"{point}　解答例：{ans}", d=3, p=4, **kw,
              ap="日本語を「だれが・どうする」がはっきりした形に言いかえ、主語と動詞を決める。次に、使う文法（時制・構文・語順）を決めてから書く。",
              steps=["主語と動詞を決める。", f"使う文法を決める：{point}", "時制・3人称単数・名詞の数・冠詞を確かめる。", f"解答例：{ans}"],
              alt=["書いた英文を日本語に訳し直して、元の日本語と意味がずれていないかを確かめる。"] + ([f"別の表し方：{v[0]}"] if v else []),
              pc=[("主語と動詞・文の形が正しい", 2), ("ポイントの文法を正しく使っている", 2)],
              pit=["日本語の「～は」「～には」をそのまま主語にする。", "冠詞（a / the）や名詞の複数形を落とす。"])


# 対話の空所に条件に合う英文：(対話（空所は (　　)）, 話す人, 条件, 解答例)
REPLY = [
    ("A: What do you usually do on Sundays?\nB: (　　)", "B", "日曜日にふだんすることを1つ、主語と動詞のある5語以上の英文で答える。",
     "I usually play soccer with my friends."),
    ("A: I want to learn about Japanese culture. Do you have any ideas?\nB: (　　)", "B", "相手に何かをすすめる表現（Why don't you ～? / You should ～. など）を使い、具体的な活動を1つ提案する。",
     "Why don't you visit an old temple in Kyoto?"),
    ("A: I'm sorry I'm late.\nB: (　　)\nA: Thank you. The train stopped because of the snow.", "B", "相手を気づかい、遅れた理由をたずねる。",
     "That's OK. What happened?"),
    ("A: Which do you like better, cats or dogs?\nB: (　　)", "B", "どちらかを選び、理由を because を使って加える。",
     "I like dogs better because they are friendly."),
    ("A: (　　)\nB: I've lived here for ten years.", "A", "B の答えに合う質問を書く。",
     "How long have you lived here?"),
    ("A: Can you come to my birthday party on Saturday?\nB: (　　)\nA: That's too bad. Maybe next time.", "B", "ていねいに断り、その理由を伝える。",
     "I'm sorry, but I can't. I have to visit my grandmother."),
    ("A: (　　)\nB: It was built about one hundred years ago.", "A", "建物がいつ建てられたかをたずねる受け身の疑問文を書く。",
     "When was this building built?"),
    ("A: I have a cold.\nB: (　　)", "B", "should を使って、相手に助言をする。",
     "You should go to bed early today."),
    ("A: What do you want to be in the future?\nB: (　　)", "B", "なりたい職業と、その理由を1つ書く。",
     "I want to be a vet because I love animals."),
    ("A: Excuse me. (　　)\nB: Sure. It's next to the post office.", "A", "図書館の場所を、ていねいにたずねる。",
     "Could you tell me where the library is?"),
]


@gen("standard_practice", 5, ["condition_check", "application"])
def reply_write(r):
    dia, who, cond, sample = r.choice(REPLY)
    return desc(f"次の対話の（　　）に入る {who} の発言を、条件に合うように英語で書きなさい。\n{dia}\n条件：{cond}", f"（例）{sample}",
                "空所の前後の発言とのつながりを確かめ、条件に指定された表現・内容を入れて書く。解答例以外にも、条件と流れに合っていれば正解。",
                [("条件（内容・表現）を満たしている", 2), ("文法・語法が正しく、対話の流れに合っている", 2)], d=3, p=4, lines=2,
                ap="空所の直前の発言（何を言われたか）と直後の発言（何に答えているか）を確かめ、条件の表現を使って1文で書く。",
                steps=["空所の前後の発言を読み、会話の流れを確認する。", "条件に下線を引き、使う表現・書く内容を決める。",
                       "主語と動詞を決めて英文を書く。", "前後の発言とつながるか、条件を満たしているかを見直す。", f"解答例：{sample}"],
                alt=["条件を満たす別の表現（例：Why don't you ～? の代わりに You should ～. など）でも、流れに合っていれば正解になる。"],
                pc=[("条件を満たす内容・表現", 2), ("文法・流れ", 2)],
                pit=["直後の発言とのつながりを確かめずに書く。", "条件で指定された表現を使わない。"])


# 意見を支える理由：(意見, 正答, [(誤答, 理由)])
REASON = [
    ("Students should read books every day.", "Reading books helps us learn many new words.",
     [("I don't like reading books.", "自分の好みを述べているだけで、意見を支えていない（むしろ反対の立場の内容）。"),
      ("There is a library near my house.", "図書館が近いことは、毎日読むべき理由にならない。"),
      ("Some books are very expensive.", "本が高いことは、意見を支える理由にならない。")]),
    ("It is better to live in a city than in the country.", "There are many stores and hospitals near our homes in a city.",
     [("The air is clean in the country.", "田舎のよい点で、反対の立場の理由になる。"),
      ("My uncle lives in Tokyo.", "個人的な事実を述べているだけで、理由になっていない。"),
      ("I went to the country last summer.", "経験を述べているだけで、都会がよい理由になっていない。")]),
    ("We should use our own bags when we go shopping.", "It reduces the number of plastic bags we throw away.",
     [("Plastic bags are cheap.", "レジ袋が安いことは、自分の袋を使うべき理由にならない。"),
      ("My bag is blue.", "袋の色は理由と関係がない。"),
      ("Shopping is a lot of fun.", "買い物の楽しさは、自分の袋を使う理由にならない。")]),
    ("Junior high school students should have smartphones.", "They can contact their families quickly when something happens.",
     [("Some students use smartphones too much.", "持つことの問題点で、反対の立場の理由になる。"),
      ("My father has a new smartphone.", "個人的な事実で、中学生が持つべき理由にならない。"),
      ("Many smartphones are black.", "色は理由と関係がない。")]),
    ("Learning a foreign language is important.", "We can communicate with people from other countries.",
     [("English is difficult for me.", "自分にとって難しいことは、大切である理由にならない。"),
      ("I have a good dictionary.", "辞書を持っていることは理由にならない。"),
      ("Some people never travel abroad.", "外国に行かない人がいることは、むしろ反対の立場の内容になる。")]),
    ("We should eat breakfast every morning.", "It gives us energy to study and play in the morning.",
     [("I usually get up at seven.", "起きる時刻は、朝食を食べるべき理由にならない。"),
      ("Some people are too busy to eat breakfast.", "食べられない人がいることで、意見を支えていない。"),
      ("Bread is popular in Japan.", "パンの人気は、朝食を食べるべき理由と関係がない。")]),
    ("Our class should clean the beach as a volunteer activity.", "We can help protect sea animals and keep the beach beautiful.",
     [("The beach is far from our school.", "遠いことは、清掃をしない理由（反対の立場）になりうる。"),
      ("I like swimming in the sea.", "自分の好みで、清掃をするべき理由になっていない。"),
      ("It is very hot in summer.", "暑いことは、清掃をするべき理由にならない。")]),
    ("It is good to keep a pet.", "Taking care of a pet teaches us responsibility.",
     [("Pets need food every day.", "毎日えさが必要なことは、飼うことの大変さで、よい理由になっていない。"),
      ("My friend has a cat.", "友だちのことを述べているだけで、理由になっていない。"),
      ("Some pets are expensive.", "費用がかかることは、反対の立場の理由になる。")]),
    ("Students should join a club activity.", "They can make friends with students in other classes.",
     [("Club activities sometimes end late.", "遅くまで続くことは、反対の立場の理由になりうる。"),
      ("Our school has twenty clubs.", "部の数を述べているだけで、参加すべき理由にならない。"),
      ("I am in the art club.", "自分のことを述べているだけで、理由になっていない。")]),
    ("We should walk or ride bikes for short trips.", "It is good for our health and for the environment.",
     [("Cars are faster than bikes.", "車のよい点で、反対の立場の理由になる。"),
      ("I bought a new bike last year.", "自分の経験を述べているだけで、理由になっていない。"),
      ("It sometimes rains in June.", "雨が降ることは、歩くべき理由にならない。")]),
]


@gen("standard_practice", 5, ["concept", "application"])
def reason_select(r):
    op, ok, wrongs = r.choice(REASON)
    return mc(f"次の意見を支える理由として最も適切な英文を選びなさい。\n意見：{op}", [ok] + [w for w, _ in wrongs],
              f"{ok}　意見と理由を because でつないで読んだとき、意見を支える内容になっているものを選ぶ。", d=3,
              ap="「意見＋because＋選択肢」とつないで読み、意見を強める内容か、関係のない内容か、反対の立場の内容かを判断する。",
              steps=["意見の内容（何をすべきか・何がよいか）を確かめる。", "各選択肢を because でつないで読む。",
                     "個人的な事実・関係のない内容・反対の立場の内容を外す。", f"意見を支えるのは：{ok}"],
              alt=["正しい理由を、自分の経験や具体例でさらにくわしく説明できるかを考えて確かめる。"],
              pc=[("意見と理由のつながりを考えている", 2), ("正しい理由を選んでいる", 2)],
              pit=["意見と同じ話題の語句が入っているだけで、理由になっていない文を選ぶ。"],
              why={w: (reason, "理由と意見の論理的なつながりの誤解") for w, reason in wrongs})


@gen("standard_practice", 5, ["application", "computation"])
def order_long(r):
    jp, parts, end, point = r.choice(ORD_LONG)
    sent = build_sent(parts, end)
    return order(f"日本語に合うように、（　）内の語句を正しい順に並べかえて英文を完成させなさい。文頭にくる語も小文字で示しています。\n{jp}", parts,
                 f"{sent}　ポイント：{point}。", d=3, p=4,
                 ap="長い文では、まず文全体の「主語＋動詞」を見つける。次に、名詞を後ろから説明する部分や to ～ の部分をひとまとまりにしてから並べる。",
                 steps=["文全体の主語と動詞を決める。", "名詞を説明する部分（関係代名詞・分詞・接触節）や、to ～・that ～ のまとまりを作る。",
                        f"ポイントの形で全体を組み立てる：{point}。", f"完成文：{sent}"],
                 alt=["完成した英文を、意味のまとまりごとにスラッシュで区切って日本語に直し、問題の日本語と照らし合わせる。"],
                 pc=[("文全体の主語と動詞が正しい", 2), ("まとまりの中の語順が正しい", 2)],
                 pit=["名詞を説明する部分を名詞の前に置く。", "文全体の動詞と、説明の部分の動詞を取り違える。"])


# ======================================================================
# C 思考力・記述応用
# ======================================================================

# 意見文のテーマ：(質問, 解答例)
OPINION = [
    ("Which is better for a school trip, Kyoto or Okinawa?",
     "I think Kyoto is better for a school trip. First, we can see many old temples and learn about Japanese history. Second, we can try traditional food and culture there. So I want to go to Kyoto."),
    ("Should junior high school students have smartphones?",
     "I think they should have smartphones. First, they can contact their families when something happens. Second, they can use them to find information for their studies. But they should make rules for using them."),
    ("Is it better to study in the morning or at night?",
     "I think it is better to study in the morning. First, my head is clear after a good sleep. Second, it is quiet because my family is still sleeping. So I study for thirty minutes before breakfast."),
    ("Do you think it is good to have a pet?",
     "Yes, I do. First, pets make our lives happy. When I come home, my dog always runs to me. Second, taking care of a pet teaches us responsibility. For these reasons, I think having a pet is good."),
    ("Should students wear school uniforms?",
     "I think students should wear school uniforms. First, we don't have to choose our clothes every morning. Second, uniforms help us feel that we are members of the same school. So uniforms are good for us."),
    ("Is it better to live in a big city or in the country?",
     "I think it is better to live in the country. First, there is a lot of nature, and the air is clean. Second, people know each other and help each other. So I want to live in the country in the future."),
    ("Which do you like better, reading books or watching movies?",
     "I like watching movies better. First, I can enjoy beautiful pictures and music at the same time. Second, I can watch a whole story in about two hours. So I often watch movies with my family on weekends."),
    ("Should we use more bicycles in our town?",
     "Yes, I think so. First, bicycles do not make the air dirty. Second, riding a bicycle is good exercise. If our town makes safe bike lanes, more people will ride bicycles."),
]


@gen("thinking_writing", 4, ["written_reasoning", "multiple_solutions"])
def opinion_write(r):
    q, model = r.choice(OPINION)
    wc = len(model.split())
    lo, hi = r.choice([x for x in [(25, 35), (30, 40), (35, 45)] if x[0] <= wc <= x[1]])
    return desc(f"次の質問に対するあなたの考えを、英語で書きなさい。\n{q}\n条件：①最初に自分の立場や考えをはっきり書く　②理由を2つ書く　③全体で{lo}〜{hi}語",
                f"（解答例・{len(model.split())}語）{model}",
                "立場 → 理由1 → 理由2 →（まとめ）の型で書く。2つの理由は違う観点から選び、具体的な説明や経験を加える。解答例と反対の立場でも、条件を満たしていれば正解。",
                [("立場・考えがはっきり書かれている", 2), ("違う観点の理由が2つ書かれている", 3), ("文法・語法が正しい", 2), ("語数の条件を満たしている", 1)],
                d=4, p=8, lines=6,
                ap="書き始める前に、日本語で「立場・理由1・理由2」をメモする。理由は「楽しさ」「健康」「時間」「お金」「人とのつながり」など違う観点から選ぶ。",
                steps=["質問の形を使って、1文目で立場を書く（I think ～. / I like ～ better. / Yes, I do. など）。",
                       "First, ～. で1つ目の理由を書き、必要なら説明や経験を加える。", "Second, ～. で、違う観点の2つ目の理由を書く。",
                       "語数に余裕があれば、So ～ / For these reasons, ～ でまとめる。", f"語数（{lo}〜{hi}語）と文法を見直す。"],
                alt=["反対の立場で書いてもよい。書きやすい理由が2つ思いつく立場を選ぶのがこつ。", "First / Second の代わりに、because と Also を使って理由を2つ書く方法もある。"],
                pc=[("立場", 2), ("理由2つ", 3), ("文法", 2), ("語数", 1)],
                pit=["2つの理由が同じ内容の言いかえになる。", "Because ～. だけの文（主節のない文）を書く。"])


# 場面・目的に合わせて書く：(場面と課題, 条件, 解答例, 採点観点)
SITUATION = [
    ("あなたの学校に、オーストラリアから留学生のエマ（Emma）が来ます。日本の学校生活について伝えるメッセージを書きなさい。",
     "①あいさつの文を入れる　②学校生活について2つのことを伝える　③全体で3文以上",
     "Hi, Emma. Welcome to our school! We eat lunch in our classroom with our classmates. We also clean our school every day after lunch.",
     [("あいさつがある", 2), ("学校生活について2つのことを伝えている", 4), ("文法・語法が正しく、3文以上ある", 2)]),
    ("ALT のブラウン先生（Mr. Brown）が国に帰ることになりました。お礼のメッセージを書きなさい。",
     "①お礼の言葉を入れる　②先生との思い出を1つ、過去形で書く　③全体で3文以上",
     "Thank you for teaching us English, Mr. Brown. I enjoyed singing English songs with you in class. I will never forget your smile.",
     [("お礼の言葉がある", 2), ("思い出を過去形で書いている", 4), ("文法・語法が正しく、3文以上ある", 2)]),
    ("外国の友だちに、おすすめの日本の食べ物を紹介するメッセージを書きなさい。",
     "①食べ物の名前を入れる　②どんな食べ物かを説明する　③すすめる理由を1つ書く　④全体で3文以上",
     "I recommend okonomiyaki. It is like a pancake with cabbage, meat, and sauce. You should try it because you can cook it with your friends at the table.",
     [("食べ物とその説明がある", 3), ("すすめる理由がある", 3), ("文法・語法が正しく、3文以上ある", 2)]),
    ("あなたの町を訪れる外国の人に、おすすめの場所を1つ紹介する文章を書きなさい。",
     "①場所の名前を入れる　②そこでできることを2つ書く　③全体で3文以上",
     "Please visit Midori Park in my town. You can see beautiful flowers there in spring. You can also enjoy a picnic by the big pond.",
     [("場所の名前がある", 2), ("そこでできることを2つ書いている", 4), ("文法・語法が正しく、3文以上ある", 2)]),
    ("夏休みの思い出について、英語の授業で発表する原稿を書きなさい。",
     "①いつ・どこで・何をしたかを書く　②そのときの気持ちや感想を書く　③過去形を正しく使い、全体で3文以上",
     "Last August, I went to Hokkaido with my family. We visited a big farm and ate fresh ice cream. It was really delicious, and I want to go there again.",
     [("いつ・どこで・何をしたかを書いている", 3), ("気持ちや感想を書いている", 3), ("過去形が正しく、3文以上ある", 2)]),
    ("これからホームステイをする家族に、自己紹介のメールを書きなさい。",
     "①名前と年齢を書く　②好きなことや得意なことを1つ書く　③ホームステイでしたいことを1つ書く　④全体で4文以上",
     "Hello. My name is Saki, and I am fifteen years old. I like playing the piano. I want to talk with you a lot and learn about your culture. I'm looking forward to meeting you.",
     [("名前と年齢がある", 2), ("好きなこととしたいことを書いている", 4), ("文法・語法が正しく、4文以上ある", 2)]),
]


@gen("thinking_writing", 3, ["written_reasoning", "application", "multiple_solutions"])
def situation_write(r):
    task, cond, sample, rubric = r.choice(SITUATION)
    return desc(f"{task}\n条件：{cond}", f"（解答例）{sample}",
                "場面と相手を考え、条件を番号ごとに1文ずつ対応させて書く。解答例以外でも、条件を満たし文法が正しければ正解。",
                rubric, d=4, p=8, lines=6,
                ap="条件の番号ごとに、何を1文で書くかを日本語でメモしてから英語にする。相手（留学生・先生・家族）に合った言い方を選ぶ。",
                steps=["場面・相手・目的を確かめる。", "条件に番号をつけ、それぞれに対応する内容を日本語でメモする。",
                       "メモを英語にしやすい日本語に言いかえ、主語と動詞を決めて書く。", "条件をすべて満たしているか、文の数・時制・3人称単数を見直す。"],
                alt=["条件を満たしていれば、内容は自分の経験や身近な例に置きかえてよい（解答例は一例）。"],
                pc=[(c, v) for c, v in rubric],
                pit=["条件の1つ（文の数・指定の内容）を見落とす。", "相手を意識せず、日本語をそのまま英語にする。"])


# 読んだ英文や資料に答えて書く
MATERIALS = [
    dict(key="MAIL1", title="留学生からのメール",
         content="Hi! I'm Lucas from Brazil. I'm going to join your class next month. I love sports. What sports are popular at your school? Also, what should I bring on the first day? See you soon!",
         task="Lucas の2つの質問の両方に答える返事を、英語で3文以上書きなさい。",
         sample="Hi, Lucas. Soccer and basketball are popular at our school. On the first day, you should bring your gym shoes. We are looking forward to meeting you!",
         rubric=[("1つ目の質問（人気のスポーツ）に答えている", 3), ("2つ目の質問（持ち物）に答えている", 3), ("文法・語法が正しく、3文以上ある", 2)]),
    dict(key="MAIL2", title="ALT の先生からの質問",
         content="Ms. Brown: I want to try some Japanese food this weekend. What food do you recommend? Please tell me why.",
         task="Ms. Brown の質問に答え、すすめる食べ物と理由を英語で2文以上書きなさい。",
         sample="I recommend sushi. There are many kinds of fish, so you can enjoy different tastes. You can eat it at a sushi restaurant near the station.",
         rubric=[("すすめる食べ物を書いている", 2), ("すすめる理由を書いている", 4), ("文法・語法が正しく、2文以上ある", 2)]),
    dict(key="DATA1", title="自由な時間の過ごし方（架空の資料）",
         content="We asked 30 students in our class, \"How do you spend your free time?\" Each student chose one answer.",
         tbl=table([["Playing games", "12"], ["Playing sports", "9"], ["Reading books", "6"], ["Listening to music", "3"]], header=["Answer", "Students"]),
         task="資料からわかることを比較の表現を使って英語で1文書き、さらに自分の過ごし方を理由とともに英語で1〜2文書きなさい。",
         sample="Playing games is the most popular way to spend free time in our class. I usually spend my free time reading books because I like exciting stories.",
         rubric=[("資料の内容を比較の表現で正しく書いている", 3), ("自分の過ごし方と理由を書いている", 3), ("文法・語法が正しい", 2)]),
    dict(key="OPIN1", title="ある生徒の意見",
         content="Taro: I think homework is not necessary. We study for many hours at school, so we should use our time at home for other things, like sports or music.",
         task="Taro の意見に賛成か反対かを示し、理由を1つ挙げて、英語で2〜3文で書きなさい。",
         sample="I don't agree with Taro. Homework helps us remember what we learned at school. If we don't review, we will forget it soon.",
         rubric=[("賛成・反対の立場を示している", 2), ("理由を書いている", 4), ("文法・語法が正しく、2〜3文で書けている", 2)]),
    dict(key="ADV1", title="友だちからの相談",
         content="Mike: I want to make more Japanese friends, but I'm shy. What should I do?",
         task="Mike の相談に対して、具体的な助言を1つと、その理由を英語で2文以上書きなさい。",
         sample="You should join a club at school. You can make friends naturally when you enjoy the same activity with other students.",
         rubric=[("具体的な助言を書いている", 3), ("助言の理由を書いている", 3), ("文法・語法が正しく、2文以上ある", 2)]),
    dict(key="POST1", title="スピーチコンテストのお知らせ",
         content="English Speech Contest\nTheme: \"My Treasure\"\nSpeak for one or two minutes about something important to you.",
         task="このコンテストのスピーチの最初の部分として、あなたの宝物と、それが大切な理由を英語で3文以上書きなさい。",
         sample="Hello, everyone. My treasure is a baseball glove. My grandfather gave it to me when I was ten, and I have used it every day since then.",
         rubric=[("宝物を紹介している", 2), ("大切な理由を書いている", 4), ("文法・語法が正しく、3文以上ある", 2)]),
]


@gen("thinking_writing", 3, ["cross_unit", "written_reasoning"], rel=["JH-ENG-G3-U06", "HS-ENG-U10"])
def respond_material(r):
    m = r.choice(MATERIALS)
    st = stim(f"WR-{m['key']}", m["content"], "data" if m.get("tbl") else "passage", f"次の英文（{m['title']}）を読んで答えなさい。",
              source="オリジナル（架空の資料）" if m.get("tbl") else "オリジナル", tbl=m.get("tbl"))
    return desc(f"「{m['title']}」について答えなさい。\n{m['task']}", f"（解答例）{m['sample']}",
                "まず英文（資料）を読んで、何をたずねられているか・何が書かれているかを正確につかむ。そのうえで、条件に合わせて自分の答えを書く。",
                m["rubric"], d=4, p=8, lines=6, stim=st,
                ap="読む → 答える の2段階で考える。英文の質問文（What / Why / What should ～?）や資料の数値に印をつけ、答えるべきことをすべて書き出してから英語にする。",
                steps=["英文・資料を読み、質問や数値に印をつける。", "答えるべきこと（質問の数・条件）を確認する。",
                       "日本語でメモを作り、英語にしやすい形に言いかえる。", "条件を満たしているか、質問にすべて答えているかを見直す。"],
                alt=["解答例とちがう内容でも、質問にきちんと答え、条件を満たしていれば正解になる。"],
                pc=[(c, v) for c, v in m["rubric"]],
                pit=["質問が2つあるのに1つにしか答えない。", "英文や資料の内容を読み違えたまま書く。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

# 文法の誤り：(日本語, 誤答, 正答, 誤りの箇所, 種類, きまり, 誤りやすい理由)
ERR_SENT = [
    ("私の妹は毎朝ピアノを練習します。", "My sister practice the piano every morning.", "My sister practices the piano every morning.", "practice", "condition",
     "主語 my sister は3人称単数で現在の文なので、動詞に s をつける。", "主語が「私」ではないことを意識せず、動詞の形を確かめなかった。"),
    ("私は昨日その映画を見ました。", "I watch the movie yesterday.", "I watched the movie yesterday.", "watch", "condition",
     "yesterday があるので過去の文。動詞を過去形にする。", "時を表す語（yesterday）と動詞の時制を照らし合わせなかった。"),
    ("私は理科に興味があります。", "I am interesting in science.", "I am interested in science.", "interesting", "concept",
     "人が「興味をもっている」は interested。interesting は「（物事が）おもしろい」。", "-ing 形と -ed 形の意味の違いを確かめなかった。"),
    ("私は野球をするのが好きです。なぜなら楽しいからです。", "I like playing baseball. Because it is fun.", "I like playing baseball because it is fun.", "Because it is fun.", "notation",
     "because ～ だけでは文にならない。前の文とつないで1文にする。", "日本語の「なぜなら～からです。」に合わせて文を区切った。"),
    ("あなたはもう宿題を終えましたか。", "Have you finish your homework yet?", "Have you finished your homework yet?", "finish", "formula",
     "現在完了は have＋過去分詞。finish の過去分詞は finished。", "疑問文で Have を前に出したため、動詞を原形のままにした。"),
    ("私の町には大きな公園が2つあります。", "There is two big parks in my town.", "There are two big parks in my town.", "There is", "condition",
     "There is / There are は、後ろの名詞が複数なら are。two big parks は複数。", "There is をひとまとまりで覚えていて、後ろの名詞の数を確かめなかった。"),
    ("私は将来、先生になりたいです。", "I want to be teacher in the future.", "I want to be a teacher in the future.", "teacher", "notation",
     "数えられる名詞の単数形 teacher には a が必要。", "日本語の「先生」には冠詞がないので、そのまま書いた。"),
    ("私たちはもっと木を植えるべきだと思います。", "I think we should planting more trees.", "I think we should plant more trees.", "planting", "formula",
     "should などの助動詞のあとは動詞の原形。", "「植えること」という日本語から ～ing 形にしてしまった。"),
    ("私は泳ぐことが得意です。", "I am good at swim.", "I am good at swimming.", "swim", "formula",
     "at などの前置詞のあとに動詞を置くときは動名詞（～ing）にする。", "「泳ぐ」をそのまま動詞の原形で書いた。"),
    ("彼は私よりも背が高い。", "He is more tall than me.", "He is taller than me.", "more tall", "formula",
     "tall のような短い語の比較級は -er をつける（taller）。more は長い語に使う。", "比較級をすべて more ～ で作れると思いこんだ。"),
]


@gen("error_correction", 4, ["common_error", "condition_check"])
def err_sentence(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(ERR_SENT)
    return desc(f"次の日本語を英語にする問題で、ある生徒は次のように書いた。\n{jp}\n［ある生徒の英文］{wrong}\n誤りを1か所指摘して理由を説明し、正しい英文に書き直しなさい。",
                f"誤り：「{where}」の部分。{rule}　正しい英文：{fix}",
                f"{rule}",
                [("誤りの箇所とその理由を指摘している", 3), ("正しい英文に書き直している", 3)], d=3, p=6, lines=4,
                ap="見直しの順番（時制 → 3人称単数の s → 名詞の数・冠詞 → 動詞の形・語法）に沿って、英文を1語ずつ点検する。",
                steps=["主語と動詞の組み合わせ（3人称単数・時制）を確かめる。", "助動詞・前置詞のあとの動詞の形、名詞の数・冠詞を確かめる。",
                       f"誤りは「{where}」：{rule}", f"正しい英文：{fix}"],
                alt=["直した英文を日本語に訳し直して、元の日本語と意味が合っているかを確かめる。"],
                pc=[("誤りの指摘と理由", 3), ("正しい英文", 3)],
                pit=["誤りの箇所だけを直して、ほかの部分（時制・冠詞）を見直さない。"],
                err=dict(sol=wrong, step=f"「{where}」の部分", type=etype, tempt=tempt, fix=fix))


# 条件を満たしていない答案：(問題, 誤答, 問題点, 書き直し例, 種類)
ERR_COND = [
    ("質問 Which season do you like the best? に、理由を含めて2文以上の英語で答えなさい。", "I like spring the best.",
     "理由が書かれておらず、1文しかないので、「理由を含めて」「2文以上」の2つの条件を満たしていない。",
     "I like spring the best. The cherry blossoms are very beautiful, and I enjoy walking in the park then.", "condition"),
    ("質問 What did you do last weekend? に、英語1文で答えなさい。", "I play tennis with my friends.",
     "過去のことをたずねる質問（did）なのに、現在形で答えている。", "I played tennis with my friends.", "condition"),
    ("あなたが行ってみたい国とその理由を、want to と because を使って英語1文で書きなさい。", "I want to go to Italy. I like pizza.",
     "because を使っておらず、2文に分かれているので条件を満たしていない。", "I want to go to Italy because I want to eat real Italian pizza.", "condition"),
    ("「中学生は毎日日記を書くべきだ」という意見に賛成か反対かを示し、理由を2つ英語で書きなさい。", "Writing a diary is good and bad. It is good for English, but it takes time.",
     "賛成か反対かの立場がはっきり示されておらず、意見を支える理由も2つになっていない。",
     "I agree. First, writing a diary every day helps us improve our writing. Second, we can remember what we did and felt.", "logic"),
    ("質問 How do you come to school? に英語で答えなさい。", "I like my school because it is big.",
     "通学方法をたずねる質問に答えておらず、学校が好きな理由を書いている。", "I come to school by bike.", "interpretation"),
    ("自分の町を紹介する英文を、15語以上で書きなさい。", "My town is nice. It is big.",
     "6語しかなく、語数の条件（15語以上）を満たしていない。町のよさの具体的な説明もない。",
     "My town is near the sea, so we can eat fresh fish. There is also a big park where many people enjoy walking.", "condition"),
    ("質問 Do you think students should clean their classrooms? に、理由を1つ加えて英語で答えなさい。", "Yes, I think. Because clean.",
     "Yes, I think. は不自然な答え方で、Because clean. は主語も動詞もない不完全な文である。",
     "Yes, I do. We use our classrooms every day, so we should keep them clean ourselves.", "notation"),
    ("「サッカーをするのが好きだ」という文に続けて、その理由を First と Second を使って2つ英語で書きなさい。", "First, it is fun. Second, it is fun with my friends.",
     "2つの理由がどちらも「楽しい」で、同じ観点の言いかえになっている。", "First, it is fun. Second, it is good for my health.", "logic"),
]


@gen("error_correction", 3, ["common_error", "written_reasoning"])
def err_condition(r):
    task, wrong, problem, fix, etype = r.choice(ERR_COND)
    return desc(f"次の問題に、ある生徒は下のように答えた。\n［問題］{task}\n［ある生徒の答案］{wrong}\nこの答案が条件を満たしていない点を説明し、条件を満たす英文に書き直しなさい。",
                f"問題点：{problem}　書き直し例：{fix}",
                "問題文の条件に番号をつけ、答案が1つずつ満たしているかを確かめる。満たしていない条件を補うように書き直す。",
                [("満たしていない条件を正しく指摘している", 3), ("条件を満たす英文に書き直している", 3)], d=3, p=6, lines=5,
                ap="問題文の条件（量・語句・内容・質問への答え方）に下線と番号をつけ、答案と1つずつ照らし合わせる。",
                steps=["問題文の条件に番号をつける。", "答案が各条件を満たしているかを確かめる。", f"満たしていない点：{problem}", f"書き直し例：{fix}"],
                alt=["書き直した英文について、条件の番号ごとに「どこで満たしているか」を指し示して確かめる。"],
                pc=[("問題点の指摘", 3), ("書き直し", 3)],
                pit=["文法の誤りだけを探して、条件の見落としに気づかない。"],
                err=dict(sol=wrong, step="条件の読み取り", type=etype, tempt="英文を書くことに集中して、問題文の条件を最後に確かめなかった。", fix=fix))


# 語順の誤り：(日本語, 誤答, 正答, きまり)
ERR_ORDER = [
    ("あなたは彼がどこに住んでいるか知っていますか。", "Do you know where does he live?", "Do you know where he lives?",
     "間接疑問では、疑問詞のあとを「主語＋動詞」の語順にし、does は使わない。"),
    ("これは私が昨日買った本です。", "This is the book bought I yesterday.", "This is the book I bought yesterday.",
     "名詞を後ろから説明するときは「主語＋動詞」の語順（I bought）にする。"),
    ("私は彼女に私の写真を見せました。", "I showed my pictures her.", "I showed her my pictures.",
     "show 人 物 の順。物を先に置くなら show 物 to 人（I showed my pictures to her.）にする。"),
    ("私は何をすべきかわかりません。", "I don't know what should I do.", "I don't know what I should do.",
     "間接疑問では、疑問詞のあとを「主語＋助動詞＋動詞」の語順にする（what to do でもよい）。"),
    ("あの赤い帽子をかぶっている女の子はだれですか。", "Who is the wearing a red hat girl?", "Who is the girl wearing a red hat?",
     "2語以上の説明（wearing a red hat）は名詞の後ろに置く。"),
    ("私にとって英語の歌を歌うことは楽しいです。", "It is fun to me for sing English songs.", "It is fun for me to sing English songs.",
     "It is ～ for 人 to＋動詞の原形 の語順にする。"),
    ("彼はよくテニスをします。", "He plays often tennis.", "He often plays tennis.",
     "often のような頻度を表す語は、一般動詞の前に置く。"),
    ("私はこんなに美しい山を見たことがありません。", "I have seen never such a beautiful mountain.", "I have never seen such a beautiful mountain.",
     "never は have と過去分詞の間に置く。"),
]


@gen("error_correction", 3, ["common_error", "computation"])
def err_order(r):
    jp, wrong, fix, rule = r.choice(ERR_ORDER)
    return desc(f"日本語に合うように語句を並べかえる問題で、ある生徒は次のように答えた。\n{jp}\n［ある生徒の答え］{wrong}\n語順の誤りを指摘し、正しい英文に直しなさい。",
                f"誤り：{rule}　正しい英文：{fix}", rule,
                [("語順の誤りとそのきまりを指摘している", 3), ("正しい英文に直している", 3)], d=3, p=6, lines=4,
                ap="文全体の「主語＋動詞」を確かめたあと、間接疑問・名詞の後ろからの説明・副詞の位置など、語順のきまりがある部分を点検する。",
                steps=["文全体の主語と動詞を確かめる。", "語順のきまりがある部分（間接疑問・後置修飾・SVOO・副詞の位置）を見つける。",
                       f"きまり：{rule}", f"正しい英文：{fix}"],
                alt=["直した英文を、意味のまとまりごとに区切って日本語にし、問題の日本語と同じ意味になるかを確かめる。"],
                pc=[("誤りの指摘", 3), ("正しい英文", 3)],
                pit=["ふつうの疑問文の語順を、間接疑問の部分にも使う。"],
                err=dict(sol=wrong, step="語順", type="formula", tempt="日本語の語順やふつうの疑問文の語順に引きずられた。", fix=fix))


GENERATORS = [order_build, cond_select, opinion_expr, jp_choice,
              translate_sa, reply_write, reason_select, order_long,
              opinion_write, situation_write, respond_material,
              err_sentence, err_condition, err_order]
