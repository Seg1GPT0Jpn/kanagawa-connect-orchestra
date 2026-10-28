"""単元パック：英語コミュニケーションⅠ 分詞と分詞構文（分詞の形容詞的用法・分詞構文・付帯状況の with）。"""
from banks._common import desc, mc, order, sa
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem,
                         tp)

UNIT_ID = "HS-ENG-U05"


# ======================================================================
# 授業プリント
# ======================================================================

LESSON = lesson(
    goals=["名詞と分詞の関係（する側か、される側か）から、現在分詞と過去分詞を使い分けて名詞を修飾できる。",
           "分詞構文の作り方を理解し、文脈から「時・理由・条件・譲歩・付帯状況」の意味を判断して、接続詞を使った文と書きかえられる。",
           "完了分詞構文・独立分詞構文・付帯状況の with を正しく使える。"],
    duration=50,
    readiness=["現在分詞・過去分詞による名詞の後置修飾（the boy playing tennis など）を中学で学習している。",
               "when / because / if / though などの接続詞の意味がわかる。", "受け身（be＋過去分詞）と完了形（have＋過去分詞）の形がわかる。"],
    flow=[("導入：する側か、される側か", 5, "an exciting game と excited fans を比べ、分詞の形が名詞との関係で決まることに気づかせる"),
          ("分詞の形容詞的用法", 10, "現在分詞（能動・進行）と過去分詞（受け身・完了）の判断と、前置・後置の位置を確認する（例題1）"),
          ("分詞構文の作り方と意味", 18, "接続詞の文から分詞構文を作る手順を示し、意味を文脈で判断させる（例題2）"),
          ("完了・独立分詞構文と付帯状況の with", 10, "Having＋過去分詞、It being ～、with O＋分詞を整理する（例題3）"),
          ("まとめと確認", 7, "確認問題3問、問題プリントA の課題指示")],
    sections=[
        intro("in1", "分詞は「動詞から作った形容詞・副詞」",
              "分詞には現在分詞（～ing）と過去分詞（-ed など）の2つがある。分詞は動詞から作られているが、名詞を修飾して形容詞のように働いたり、文全体に情報を加えて副詞のように働いたりする。どちらの分詞を使うかは、修飾される名詞（または文の主語）と分詞の関係が「する側」か「される側」かで決まる。",
              bullets=["an exciting game：試合が（人を）わくわくさせる → 試合は「する側」なので現在分詞。",
                       "excited fans：ファンが（試合に）わくわくさせられる → ファンは「される側」なので過去分詞。",
                       "Seen from the sky, the island looks like a heart.：島は「見られる側」なので過去分詞で始まる分詞構文。"],
              points=[tp("2つの語句を板書し、「だれが、だれを」わくわくさせるのかを生徒に説明させる。", ask="excited fans のファンは、わくわくさせる側か、させられる側か。",
                         expect="させられる側（わくわくした気持ちになっている）。", timing="導入の冒頭"),
                      tp("この単元のすべての問題は「名詞（主語）と分詞の関係が能動か受け身か」の判断に帰着することを最初に予告する。")]),
        definition("df1", "分詞の形容詞的用法",
                   "分詞は名詞を修飾する。現在分詞は「～している（能動・進行）」、過去分詞は「～された・～されている（受け身）」または自動詞の場合「～してしまった（完了）」を表す。",
                   bullets=["分詞1語だけで修飾するときは名詞の前：a sleeping baby（眠っている赤ちゃん）、a broken window（割れた窓）",
                            "分詞が目的語や修飾語を伴うときは名詞の後ろ：the boy playing the guitar（ギターをひいている少年）、a car made in Germany（ドイツで作られた車）",
                            "自動詞の過去分詞は完了を表す：fallen leaves（落ち葉）",
                            "感情を表す動詞（excite, surprise, bore, interest など）は「（人を）～させる」の意味なので、人を～させるものは現在分詞（exciting）、～させられる人は過去分詞（excited）。"],
                   conditions=["分詞の判断は日本語の訳ではなく、名詞と動詞の関係で行う（「書かれた本」でも「本が書く」のではないので written）。",
                               "～ing が名詞の前にあっても、用途を表す動名詞の場合がある（a sleeping car＝寝台車、a car for sleeping）。"],
                   points=[tp("「名詞＋be 動詞＋分詞」の文を作って関係を確かめるテストを教える（The baby is sleeping. ／ The window was broken.）。",
                              ask="a broken window で、The window broke something. と The window was broken. のどちらが成り立つか。", expect="The window was broken.（受け身）なので過去分詞。")]),
        theorem("th1", "分詞構文の意味と形",
                "［接続詞＋S＋V］, S＋V.　→　［分詞 ～］, S＋V.（分詞の意味上の主語＝主節の主語）",
                ["時（～するとき・～していると）：Opening the box, she found a letter.",
                 "理由（～なので）：Feeling sick, he stayed home.",
                 "条件（～すれば）：Turning left, you will see the bank.",
                 "譲歩（～だけれども）：Living near the sea, he cannot swim.（譲歩はあまり多くない）",
                 "付帯状況（～しながら）・連続動作（そして～する）：She sat on the bench, reading a book.",
                 "完了分詞構文 Having＋過去分詞：主節より前の時。独立分詞構文：分詞の主語が主節の主語と違うときは、分詞の前に主語を残す（It being fine, ...）。"],
                body="分詞構文には接続詞がないので、どの意味になるかは主節との内容のつながりで判断する。否定語 not / never は分詞の直前に置く（Not knowing what to say, ...）。",
                points=[tp("意味の判断では「主節との関係を日本語で言ってみる」ことを習慣にさせる。", ask="Living near the sea, he cannot swim. は「住んでいるので泳げない」で意味が通るか。",
                           expect="通らない。「住んでいるのに泳げない」なので譲歩。", caution="分詞構文の意味は1つに決まらないこともあるが、試験では文脈に最も合うものを選ばせる。")]),
        derivation("dv1", "分詞構文を作る手順（なぜその形になるのか）",
                   ["① 接続詞の節と主節の主語を比べる。Because she was tired, she went to bed early. では、どちらも she。",
                    "② 接続詞 Because を取る（意味は主節とのつながりで伝わるので省ける）。",
                    "③ 主語が同じなので、従属節の主語 she を取る（主節の主語が分詞の意味上の主語になる）。",
                    "④ 従属節の動詞を分詞にする。was → being。Being tired, she went to bed early.",
                    "⑤ Being は省略されることが多い：Tired, she went to bed early.（受け身の Being＋過去分詞も Being を省いて過去分詞で始める）",
                    "⑥ 時がずれるとき（従属節が主節より前）は Having＋過去分詞。主語が異なるときは主語を残す（独立分詞構文）。",
                    "⑦ 確かめ：できた分詞構文を接続詞の文に戻し、主語・時制・能動か受け身かが元の文と一致するかを確認する。"],
                   body="手順③で主語を取れるのは、主節と主語が同じときだけである。主語が違うのに取ってしまうと、分詞の動作を主節の主語がしていることになり、意味がおかしくなる（Arriving at the station, the train had left. は「電車が駅に着いた」と読めてしまう）。",
                   points=[tp("手順を黒板で1行ずつ消していく形で実演し、何を消して何を変えたかを生徒に言わせる。", timing="定理の説明の後",
                              ask="As it was rainy, we stayed home. で it を取ってよいか。", expect="取れない。主節の主語 we と違うので It being rainy, ... とする。")]),
        definition("df2", "付帯状況の with",
                   "with＋O＋分詞（または形容詞・副詞・前置詞句）で「O が～している状態で・O を～したまま」という付帯状況を表す。分詞の選び方は、O と分詞の関係で決める。",
                   bullets=["O が「～している」（能動）なら現在分詞：with her dog following her（犬が後からついてきて）",
                            "O が「～されている」（受け身）なら過去分詞：with his arms folded（腕を組んで＝腕が組まれた状態で）",
                            "形容詞・副詞・前置詞句も置ける：with your mouth full（口にものを入れたまま）、with the light on（明かりをつけたまま）、with a book in her hand"],
                   conditions=["with her eyes closed の closed は、目が「閉じられた」状態を表す。「目が閉じている」という日本語につられて closing にしない。"],
                   points=[tp("with O＋分詞の O と分詞の間に be 動詞を入れて文を作り、能動か受け身かを確かめさせる（Her eyes were closed.）。",
                              caution="with his arms folding のような誤りが多い。腕は自分で組むのではなく「組まれる」側。")]),
        example("ex1", "例題1　分詞の形容詞的用法",
                "（　）内の動詞を適切な形にしなさい。(1) The girl (dance) on the stage is my cousin.　(2) This is a temple (build) in the 8th century.",
                ["(1) 少女は「踊っている」側（The girl is dancing.）なので現在分詞 dancing。後ろに on the stage が続くので名詞の後ろに置く。",
                 "(2) 寺は「建てられた」側（The temple was built.）なので過去分詞 built。"],
                "(1) dancing　(2) built",
                thinking="修飾される名詞を主語にして、be 動詞＋分詞の文が能動（進行形）か受け身かを確かめる。",
                points=[tp("(2) を「建てた寺」と訳して building を選ぶ生徒がいる。日本語の「た」は過去分詞の目印ではないことを確認する。")],
                misconceptions=[("This is a temple building in the 8th century.", "寺は建てられる側なので過去分詞 built。building は「建てている」で、寺が何かを建てることになる")]),
        example("ex2", "例題2　分詞構文への書きかえと意味",
                "次の文を分詞構文に書きかえなさい。(1) As I didn't know what to do, I asked my teacher.　(2) When the city is seen from the tower, it looks beautiful.",
                ["(1) 主語はどちらも I。接続詞と主語を取り、didn't know を分詞にする。否定語 not は分詞の前に置く。", "(1) Not knowing what to do, I asked my teacher.",
                 "(2) 主語は the city と it（同じもの）。is seen は受け身なので Being seen となり、Being を省く。主節の主語は代名詞 it を名詞に戻す。", "(2) Seen from the tower, the city looks beautiful."],
                "(1) Not knowing what to do, I asked my teacher.　(2) Seen from the tower, the city looks beautiful.",
                thinking="①主語が同じか、②能動か受け身か、③否定語や時のずれがあるか、の3点を確かめてから分詞の形を決める。",
                points=[tp("(2) で主節の it を the city に戻す理由（分詞構文に名詞がなくなるため）を確認させる。", ask="Seen from the tower, it looks beautiful. で it が何を指すかわかるか。", expect="わからない。名詞に戻す必要がある。")]),
        example("ex3", "例題3　完了分詞構文・独立分詞構文・付帯状況の with",
                "（　）に適切な語句を入れなさい。(1) (　　) finished the report, he went home.　(2) (　　) no bus, we had to walk.　(3) He listened to me with his arms (fold).",
                ["(1) レポートを終えたのは帰宅より前なので完了分詞構文 Having。", "(2) 「バスがなかった」の主語は there 構文なので There being。",
                 "(3) 腕は「組まれた」状態なので過去分詞 folded。"],
                "(1) Having　(2) There being　(3) folded",
                thinking="時のずれ・主語の違い・O と分詞の関係を、それぞれ元の文に戻して確かめる。",
                points=[tp("(2) は As there was no bus, ... に戻させ、there を残す理由を考えさせる。")],
                misconceptions=[("Being no bus, we had to walk.", "主節の主語 we とは違う「there 構文」なので there を残し There being no bus とする")]),
        board("bd1", "板書案",
              [("① 分詞の形容詞的用法", ["名詞が「する側」→ ～ing", "名詞が「される側」→ 過去分詞", "1語 → 名詞の前（a sleeping baby）", "語句を伴う → 名詞の後ろ", "exciting game ／ excited fans"]),
               ("② 分詞構文", ["接続詞を取る → 主語を取る → 分詞に", "Being は省略可（Tired, ...）", "Not ＋ 分詞", "Having＋過去分詞 ＝ 主節より前", "主語が違う → 残す（It being ～）"]),
               ("③ 付帯状況の with", ["with O ＋ 分詞", "O が～している → ～ing", "O が～されている → 過去分詞", "with her eyes closed", "with her dog following her"])],
              points=[tp("板書は3列に分け、すべての列に「する側／される側」の判断を書く。②の手順は矢印で上から下へ示し、③の例は be 動詞テストの文を添える。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("分詞の判断は日本語訳ではなく、名詞＋be 動詞＋分詞の文を作るテストで行わせる。", ask="the language spoken in Brazil で The language is spoken. は成り立つか。", expect="成り立つので過去分詞。"),
               tp("感情の分詞は「人だから過去分詞、物だから現在分詞」と覚えさせない。The boring teacher（退屈させる先生）のように人でも現在分詞になる。", caution="機械的な覚え方は誤りのもと。"),
               tp("分詞構文の意味は、主節とのつながりを日本語で言わせてから選ばせる。", timing="例題2の後"),
               tp("分詞構文の主語の一致を必ず確認させる。主語が違うのに省いた誤答（懸垂分詞）は、問題プリント D で扱う。"),
               tp("完了分詞構文は U04 の完了不定詞・完了動名詞と同じ「主節より前」の考え方であることを関連づける。")],
              misconceptions=[("I was very exciting at the concert.", "わくわくさせられたのは私なので excited。exciting だと「私が人をわくわくさせる」の意味になる"),
                              ("Seeing from the hill, the town looks small.", "町は「見られる」側なので Seen from the hill, ..."),
                              ("Being rainy, the game was canceled.", "雨なのは the game ではないので It being rainy, ... とする")]),
        summary("sm1", "まとめ",
                ["分詞の形は、名詞（主語・O）との関係が能動（する側）なら現在分詞、受け身（される側）なら過去分詞。",
                 "分詞構文は接続詞と主語を取り、動詞を分詞にして作る。意味（時・理由・条件・譲歩・付帯状況）は主節とのつながりで判断する。",
                 "主節より前の時は Having＋過去分詞、主語が違えば主語を残す。with O＋分詞で付帯状況を表す。"]),
        check("ck1", "確認問題",
              [("「割れた窓」を英語で表しなさい。", "a broken window"),
               ("Because I had lost my key, I couldn't get in. を分詞構文に書きかえなさい。", "Having lost my key, I couldn't get in."),
               ("He was reading with his legs (cross). の（　）内を適切な形にしなさい。", "crossed（脚は組まれた状態）")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

# (英文, 和訳, 原形, ing, 過去分詞, 3単現, 'ing' or 'pp')
MOD = [
    ("The man (　　) in front of the gate is my uncle.", "門の前に立っている男性は私のおじだ。", "stand", "standing", "stood", "stands", "ing"),
    ("This is a picture (　　) by a famous artist.", "これは有名な画家によって描かれた絵だ。", "paint", "painting", "painted", "paints", "pp"),
    ("The language (　　) in Brazil is Portuguese.", "ブラジルで話されている言語はポルトガル語だ。", "speak", "speaking", "spoken", "speaks", "pp"),
    ("Who is the girl (　　) the piano?", "ピアノをひいている少女はだれですか。", "play", "playing", "played", "plays", "ing"),
    ("My father bought a (　　) car last week.", "父は先週、中古車を買った。", "use", "using", "used", "uses", "pp"),
    ("The boy (　　) a red cap is my brother.", "赤い帽子をかぶっている男の子は私の弟だ。", "wear", "wearing", "worn", "wears", "ing"),
    ("We found a window (　　) by the strong wind.", "私たちは強風で割れた窓を見つけた。", "break", "breaking", "broken", "breaks", "pp"),
    ("Do you know the woman (　　) with Mr. Sato?", "佐藤先生と話している女性を知っていますか。", "talk", "talking", "talked", "talks", "ing"),
    ("The letter (　　) yesterday has not arrived yet.", "昨日送った手紙はまだ届いていない。", "send", "sending", "sent", "sends", "pp"),
    ("Look at the (　　) baby.", "眠っている赤ちゃんを見て。", "sleep", "sleeping", "slept", "sleeps", "ing"),
    ("There were many people (　　) for the bus.", "バスを待っている人がたくさんいた。", "wait", "waiting", "waited", "waits", "ing"),
    ("He showed me some photos (　　) in Okinawa.", "彼は沖縄で撮った写真を何枚か見せてくれた。", "take", "taking", "taken", "takes", "pp"),
    ("Be careful of the (　　) water.", "沸騰しているお湯に気をつけて。", "boil", "boiling", "boiled", "boils", "ing"),
    ("I have a friend (　　) Kenta.", "私には健太という名前の友達がいる。", "name", "naming", "named", "names", "pp"),
]


@gen("basic_check", 5, ["computation", "condition_check"])
def participle_modifier(r):
    s, jp, base, ing, pp, s3, kind = r.choice(MOD)
    before = s.split("(　　)")[0].split()
    noun = s.split("(　　) ")[1].split()[0].rstrip(".?") if before[-1] in ("a", "the") else before[-1]
    ok = ing if kind == "ing" else pp
    if kind == "ing":
        rel = f"{noun} は自分で動作をする側（能動・進行：the {noun} is {ing} が成り立つ）"
        other = (pp, f"過去分詞にすると {noun} が「～される」側（受け身）になる。{noun} は自分で動作をしている側なので現在分詞。")
    else:
        rel = f"{noun} は動作を受ける側（受け身：the {noun} is / was {pp} が成り立つ）"
        other = (ing, f"現在分詞にすると {noun} が自分で動作をする側になる。{noun} は動作を受ける側なので過去分詞。")
    wrongs = [other, (base, "動詞の原形は、そのままでは名詞を修飾できない。"),
              (s3, "3人称単数現在形は述語動詞の形で、関係代名詞なしに名詞を修飾することはできない。")]
    return mc(f"日本語の意味になるように、（　）に入る最も適切なものを選びなさい。\n{jp}\n{s}", [ok] + [w for w, _ in wrongs],
              f"{ok} が入る。{rel}である。", d=1,
              ap="修飾される名詞を主語にして「名詞＋be 動詞＋分詞」の文を作り、進行形（能動）か受け身かを確かめる。",
              steps=[f"修飾される名詞 {noun} を確認する。", f"{rel}。", f"よって{'現在分詞' if kind == 'ing' else '過去分詞'}の {ok} を選ぶ。"],
              alt=[f"関係代名詞を使って書きかえてみる（the {noun} which / who {'is ' + ing if kind == 'ing' else 'is / was ' + pp} …）と、能動か受け身かがはっきりする。"],
              pc=[("名詞と分詞の関係（能動・受け身）を判断している", 1), ("正しい分詞を選んでいる", 1)],
              pit=["日本語の「～た」につられて、能動の関係なのに過去分詞を選ぶ。", "「～している」以外の訳のときに現在分詞を見落とす。"],
              why={w: (reason, "現在分詞と過去分詞（能動・受け身）の混同") for w, reason in wrongs})


# (英文, 和訳, ing, 過去分詞, 原形, 第3の誤答, その理由, 'ing' or 'pp', 説明の主体)
EMO = [
    ("The game was really (　　).", "その試合は本当にわくわくするものだった。", "exciting", "excited", "excite", "excitement", "名詞 excitement は主語 The game とイコールの関係にならず、補語として意味が通らない。", "ing", "試合が人をわくわくさせる"),
    ("We were (　　) at the news.", "私たちはその知らせに驚いた。", "surprising", "surprised", "surprise", "surprisingly", "副詞 surprisingly は補語になれない。", "pp", "私たちが驚かされた"),
    ("His speech was so (　　) that many students fell asleep.", "彼の話はとても退屈で、多くの生徒が眠ってしまった。", "boring", "bored", "bore", "boredom", "名詞 boredom は so ～ that の間に置けず、補語としても意味が通らない。", "ing", "話が人を退屈させる"),
    ("I'm (　　) in Japanese history.", "私は日本の歴史に興味がある。", "interesting", "interested", "interest", "interestingly", "副詞 interestingly は補語になれない。", "pp", "私が興味を持たされている"),
    ("She looked (　　) after the long walk.", "長い散歩の後、彼女は疲れているように見えた。", "tiring", "tired", "tire", "tiredness", "名詞 tiredness は look の補語として「疲れているように見える」の意味にならない。", "pp", "彼女が疲れさせられた"),
    ("The result of the test was (　　).", "テストの結果はがっかりするものだった。", "disappointing", "disappointed", "disappoint", "disappointingly", "副詞 disappointingly は補語になれない。", "ing", "結果が人をがっかりさせる"),
    ("I was (　　) by his explanation.", "私は彼の説明で混乱した。", "confusing", "confused", "confuse", "confusion", "名詞 confusion は主語 I とイコールの関係にならない。", "pp", "私が混乱させられた"),
    ("The view from the top was (　　).", "頂上からの眺めはすばらしかった。", "amazing", "amazed", "amaze", "amazingly", "副詞 amazingly は補語になれない。", "ing", "眺めが人を驚嘆させる"),
    ("Are you (　　) with your new room?", "新しい部屋に満足していますか。", "satisfying", "satisfied", "satisfy", "satisfaction", "名詞 satisfaction は主語 you とイコールの関係にならない。", "pp", "あなたが満足させられている"),
    ("It was a (　　) experience for all of us.", "それは私たち全員にとって衝撃的な経験だった。", "shocking", "shocked", "shock", "shockingly", "副詞 shockingly は名詞 experience を修飾できない。", "ing", "経験が人に衝撃を与える"),
    ("The (　　) children ran out into the yard.", "わくわくした子どもたちが庭へ駆け出した。", "exciting", "excited", "excite", "excitedly", "副詞 excitedly は名詞 children を修飾できない。", "pp", "子どもたちがわくわくさせられている"),
    ("Everyone was (　　) to hear the news.", "その知らせを聞いて、みんながっかりした。", "disappointing", "disappointed", "disappoint", "disappointment", "名詞 disappointment は主語 Everyone とイコールの関係にならない。", "pp", "みんながっかりさせられた"),
]


@gen("basic_check", 5, ["concept", "common_error"])
def emotion_participle(r):
    s, jp, ing, pp, base, w3, w3r, kind, who = r.choice(EMO)
    ok, other = (ing, pp) if kind == "ing" else (pp, ing)
    if kind == "ing":
        oreason = f"{pp} は「（人が）～させられる・～した気持ちになる」の意味。この文は{who}関係なので現在分詞。"
    else:
        oreason = f"{ing} は「（人を）～させる」の意味。この文は{who}関係なので過去分詞。"
    wrongs = [(other, oreason), (base, f"動詞の原形 {base} は「（人を）～させる」という動詞で、補語や修飾語にはならない。"), (w3, w3r)]
    return mc(f"日本語の意味になるように、（　）に入る最も適切なものを選びなさい。\n{jp}\n{s}", [ok] + [w for w, _ in wrongs],
              f"{ok} が入る。感情を表す動詞は「（人を）～させる」の意味。この文は{who}関係である。", d=2,
              ap="感情を表す動詞は「（人を）～させる」の意味であることを思い出し、名詞（主語）が「させる側」か「させられる側」かを判断する。",
              steps=[f"動詞 {base} の意味は「（人を）～させる」。", f"この文は{who}関係である。", f"させる側なら ～ing、させられる側なら過去分詞なので、{ok}。"],
              alt=[f"{ok} を使った文を「～させる」「～させられる」を使った日本語に言いかえて、意味が通るかを確かめる。"],
              pc=[("させる側・させられる側を判断している", 1), ("正しい形を選んでいる", 1)],
              pit=["「わくわくする」という日本語から exciting を選び、人の気持ちにも使ってしまう。", "「人なら過去分詞」と機械的に決める。"],
              why={w: (reason, "感情を表す分詞（～ing と過去分詞）の混同") for w, reason in wrongs})


LABELS = {
    "時": "「～するとき・～していると」",
    "理由": "「～なので」",
    "条件": "「～すれば」",
    "譲歩": "「～だけれども」",
    "付帯状況": "「～しながら」",
    "連続動作": "「～して、そして…」",
}

# 正しい意味ごとの誤答（文脈上はっきり成り立たないものだけを選ぶ）
DIST = {
    "時": ["理由", "条件", "譲歩"],
    "理由": ["条件", "譲歩", "連続動作"],
    "条件": ["理由", "譲歩", "付帯状況"],
    "譲歩": ["理由", "条件", "付帯状況"],
    "付帯状況": ["理由", "条件", "譲歩"],
    "連続動作": ["理由", "条件", "譲歩"],
}

# (英文, 正しい意味, 前後の関係の説明)
CONST = [
    ("Opening the box, she found a letter inside.", "時", "箱を開けたときに、手紙を見つけた"),
    ("Having a bad cold, she stayed home from school.", "理由", "ひどいかぜをひいていることが、学校を休んだ原因になっている"),
    ("Turning to the left, you will see the post office.", "条件", "左に曲がれば郵便局が見える（主節が will を使った未来の内容）"),
    ("Living near the sea, he cannot swim.", "譲歩", "海の近くに住んでいるのに泳げない（予想に反する内容）"),
    ("Not knowing what to say, I kept silent.", "理由", "何を言えばよいかわからないことが、黙っていた原因になっている"),
    ("Written in easy English, this book is good for beginners.", "理由", "やさしい英語で書かれていることが、初心者に向いている理由になっている"),
    ("Arriving at the station, we found that the train had already left.", "時", "駅に着いたときに、電車が出たことがわかった"),
    ("Admitting what you say, I still think you are wrong.", "譲歩", "言うことは認めるが、それでもまちがっていると思う（still が対立を示す）"),
    ("Born in Kyoto, she knows the city very well.", "理由", "京都で生まれたことが、町をよく知っている理由になっている"),
    ("Using this app, you can learn new words easily.", "条件", "このアプリを使えば、簡単に単語を覚えられる"),
    ("She sat on the sofa, reading a magazine.", "付帯状況", "ソファーに座るのと雑誌を読むのが同時に行われている"),
    ("The train left Tokyo at nine, arriving in Osaka at noon.", "連続動作", "東京を出て、そして正午に大阪に着いたという順に起きたできごと"),
    ("Walking along the river, I saw a big fish jump.", "時", "川沿いを歩いているときに、大きな魚がはねるのを見た"),
    ("Taking this bus, you will get to the museum in ten minutes.", "条件", "このバスに乗れば博物館に着く（主節が will を使った未来の内容）"),
]


@gen("basic_check", 5, ["concept", "condition_check"])
def construction_meaning(r):
    s, ok, note = r.choice(CONST)
    wrongs = DIST[ok]
    lab = lambda k: f"{k}{LABELS[k]}"
    why = {lab(w): (f"{lab(w)}と読むと、「{note}」という前後の関係を表せず、文脈に合わない。", f"分詞構文の意味（{w}と{ok}）の取り違え") for w in wrongs}
    first = s.split(",")[0] if not s.startswith(("She sat", "The train")) else s.split(", ")[1].rstrip(".")
    return mc(f"次の英文の分詞構文（{first}）が表す意味として、最も適切なものを選びなさい。\n{s}", [lab(ok)] + [lab(w) for w in wrongs],
              f"{lab(ok)}。{note}。", d=2,
              ap="分詞構文の部分と主節の内容を日本語で並べ、「とき」「ので」「れば」「けれども」「ながら」のどれでつなぐと自然かを試す。",
              steps=["分詞構文の部分と主節を分けて、それぞれの意味をとる。", f"前後の関係を確かめる：{note}。", f"よって{lab(ok)}。"],
              alt=["選んだ意味の接続詞（when / because / if / though など）を使った文に書きかえ、自然な英文になるかを確かめる。"],
              pc=[("主節との関係を正しくとらえている", 1), ("意味を正しく選んでいる", 1)],
              pit=["分詞構文はいつも「～して」「～しながら」と訳し、理由や譲歩の関係を見落とす。"], why=why)


# (英文, 和訳, 原形, ing, 過去分詞, 'ing' or 'pp', O)
WITH = [
    ("He was standing there with his arms (　　).", "彼は腕を組んでそこに立っていた。", "fold", "folding", "folded", "pp", "his arms"),
    ("She sat on the chair with her legs (　　).", "彼女は脚を組んでいすに座っていた。", "cross", "crossing", "crossed", "pp", "her legs"),
    ("He fell asleep with the TV (　　) on.", "彼はテレビをつけたまま寝てしまった。", "leave", "leaving", "left", "pp", "the TV"),
    ("She came into the room with her dog (　　) her.", "彼女は犬を後ろに従えて部屋に入ってきた。", "follow", "following", "followed", "ing", "her dog"),
    ("I can't study with my brother (　　) so loudly.", "弟がそんなに大声で歌っていては勉強できない。", "sing", "singing", "sung", "ing", "my brother"),
    ("She was running with her hair (　　) in the wind.", "彼女は髪を風になびかせて走っていた。", "blow", "blowing", "blown", "ing", "her hair"),
    ("The girl was sitting with her eyes (　　) on the stage.", "少女は舞台に目を向けたまま座っていた。", "fix", "fixing", "fixed", "pp", "her eyes"),
    ("He walked out with tears (　　) down his cheeks.", "彼はほおに涙を流しながら出て行った。", "stream", "streaming", "streamed", "ing", "tears"),
    ("She answered the phone with a baby (　　) in her arms.", "彼女は赤ちゃんを腕の中で眠らせたまま電話に出た。", "sleep", "sleeping", "slept", "ing", "a baby"),
    ("The dog ran toward me with its tail (　　).", "犬はしっぽを振りながら私の方へ走ってきた。", "wag", "wagging", "wagged", "ing", "its tail"),
    ("He sat still with his eyes (　　), thinking hard.", "彼は目を閉じてじっと座り、懸命に考えていた。", "close", "closing", "closed", "pp", "his eyes"),
    ("I couldn't sleep with the dog (　　) all night.", "犬が一晩中ほえていたので眠れなかった。", "bark", "barking", "barked", "ing", "the dog"),
    ("He came home with his shoes (　　) with mud.", "彼は靴を泥だらけにして帰ってきた。", "cover", "covering", "covered", "pp", "his shoes"),
]


@gen("basic_check", 5, ["computation", "concept"])
def with_attendant(r):
    s, jp, base, ing, pp, kind, o = r.choice(WITH)
    ok = ing if kind == "ing" else pp
    if kind == "ing":
        rel = f"{o} が自分で動作をしている（能動：{o} is {ing} が成り立つ）"
        other = (pp, f"過去分詞にすると {o} が「～される」側になる。{o} は自分で動作をしているので現在分詞。")
    else:
        rel = f"{o} が動作を受けた状態にある（受け身：{o} is / was {pp} が成り立つ）"
        other = (ing, f"現在分詞にすると {o} が自分で動作をすることになる。{o} は動作を受けた状態なので過去分詞。")
    wrongs = [other, (base, "with O の後ろに動詞の原形を置いて付帯状況を表すことはできない。"),
              (f"to {base}", "with O to do は「～すべき O を持って」の意味になり、付帯状況「O が～している（された）状態で」を表さない。")]
    return mc(f"日本語の意味になるように、（　）に入る最も適切なものを選びなさい。\n{jp}\n{s}", [ok] + [w for w, _ in wrongs],
              f"{ok} が入る。付帯状況の with O＋分詞で、{rel}関係である。", d=2,
              ap=f"with の後ろの O（{o}）と分詞の間に be 動詞を入れ、進行形（能動）と受け身のどちらが成り立つかを確かめる。",
              steps=[f"with の後ろの O は {o}。", f"{rel}。", f"能動なら現在分詞、受け身なら過去分詞なので {ok}。"],
              alt=[f"「{o} {'is/was ' + ing if kind == 'ing' else 'is/was ' + pp}」という文を作り、意味が通るかを確かめる。"],
              pc=[("O と分詞の関係を判断している", 1), ("正しい形を選んでいる", 1)],
              pit=["「目を閉じて」「腕を組んで」の日本語につられて現在分詞を選ぶ。"],
              why={w: (reason, "付帯状況の with での能動・受け身の混同") for w, reason in wrongs})


# ======================================================================
# B 標準演習
# ======================================================================

# (元の文, 答え, 別解, 説明)
RW = [
    ("When I opened the door, I saw a cat.", "Opening the door, I saw a cat.", [], "主語が同じ I なので、接続詞と主語を取り、opened を現在分詞にする。"),
    ("Because she was tired, she went to bed early.", "Being tired, she went to bed early.", ["Tired, she went to bed early."], "主語が同じなので接続詞と主語を取り、was を Being にする。Being は省略してもよい。"),
    ("As I didn't know his address, I couldn't write to him.", "Not knowing his address, I couldn't write to him.", [], "否定語 not は分詞の直前に置く。"),
    ("After he had finished lunch, he went out.", "Having finished lunch, he went out.", [], "had finished は主節 went より前の時なので、完了分詞構文 Having finished にする。"),
    ("As this book is written in easy English, it is easy to read.", "Written in easy English, this book is easy to read.", ["Being written in easy English, this book is easy to read."],
     "受け身 is written は Being written となり、Being を省いて過去分詞で始める。主節の it は名詞 this book に戻す。"),
    ("If you turn right at the corner, you will find the shop.", "Turning right at the corner, you will find the shop.", [], "主語が同じ you なので、接続詞と主語を取り、turn を現在分詞にする。"),
    ("Because it was rainy, we stayed at home.", "It being rainy, we stayed at home.", [], "従属節の主語 it と主節の主語 we が違うので、it を残す（独立分詞構文）。"),
    ("While I was walking in the park, I met an old friend of mine.", "Walking in the park, I met an old friend of mine.", [], "主語が同じなので接続詞と主語を取り、was walking を walking にする。"),
    ("As he had lived in London for years, he spoke English well.", "Having lived in London for years, he spoke English well.", [], "had lived は主節 spoke より前から続いていたことなので、完了分詞構文にする。"),
    ("When the city is seen from the plane, it looks like a toy town.", "Seen from the plane, the city looks like a toy town.", ["Being seen from the plane, the city looks like a toy town."],
     "受け身なので過去分詞 Seen で始め、主節の it を the city に戻す。"),
    ("Since there was no bus, we had to walk.", "There being no bus, we had to walk.", [], "there 構文の there を残し、was を being にする（独立分詞構文）。"),
    ("As she was born in Hokkaido, she is used to the cold.", "Born in Hokkaido, she is used to the cold.", ["Being born in Hokkaido, she is used to the cold."],
     "受け身 was born の Being は省略するのが普通で、過去分詞 Born で始める。"),
]


@gen("standard_practice", 5, ["computation", "condition_check"])
def make_construction(r):
    src, ans, v, why_s = r.choice(RW)
    return sa(f"次の英文を、分詞構文を使ってほぼ同じ意味の英文に書きかえなさい。\n{src}", ans,
              f"{why_s}", d=3, v=v,
              ap="①主語が主節と同じか、②能動か受け身か、③主節より前の時か、④否定語があるか、の4点を確かめてから分詞の形を決める。",
              steps=["接続詞を取る。", "主語が主節と同じなら取り、違えば残す。", "動詞を分詞にする（受け身なら過去分詞、前の時なら Having＋過去分詞、否定は Not＋分詞）。", f"答え：{ans}"],
              alt=["書きかえた文に接続詞と主語を補って元に戻し、主語・時制・能動か受け身かが一致するかを確かめる。"],
              pc=[("分詞の形（現在分詞・過去分詞・完了形）が正しい", 2), ("主語・否定語の扱いが正しい", 2)],
              pit=["主語が違うのに主語を省く。", "受け身なのに現在分詞で始める。", "not を分詞の後ろに置く。"])


# (英文, 和訳, 正答, [(誤答, 理由)])
CFORM = [
    ("(　　) from a distance, the rock looks like a lion's face.", "遠くから見ると、その岩はライオンの顔のように見える。", "Seen",
     [("Seeing", "現在分詞にすると、主語 the rock が何かを見る側になる。岩は「見られる」側。"),
      ("Having seen", "能動の完了分詞構文で、岩が見る側になるうえ、主節より前の時を表してしまう。"),
      ("To see", "不定詞にすると「見るために」という目的の意味になり、文意に合わない。")]),
    ("(　　) all my money, I couldn't buy the ticket.", "お金をすべて使ってしまっていたので、私はチケットを買えなかった。", "Having spent",
     [("Spent", "過去分詞で始めると、主語 I が「使われた」側になる。"),
      ("Spending", "単純な現在分詞では、主節と同じ時になり、「使ってしまっていた」という前の時を表せない。"),
      ("Having been spent", "受け身の完了形で、主語 I が「使われた」ことになる。")]),
    ("(　　) what to do, she asked her teacher for advice.", "どうしたらよいかわからなかったので、彼女は先生に助言を求めた。", "Not knowing",
     [("Knowing not", "否定語 not は分詞の前に置く。"), ("Not known", "過去分詞にすると、主語 she が「知られていない」側になる。"),
      ("Don't knowing", "分詞構文を don't で否定することはできない。")]),
    ("(　　) in a hurry, the letter had many mistakes.", "急いで書かれたので、その手紙には多くのまちがいがあった。", "Written",
     [("Writing", "現在分詞にすると、主語 the letter が何かを書く側になる。手紙は「書かれた」側。"),
      ("Having written", "能動の完了形で、手紙が何かを書いたことになる。"), ("To write", "不定詞にすると「書くために」の意味になり、文意に合わない。")]),
    ("(　　) a fine day, we went on a picnic.", "天気のよい日だったので、私たちはピクニックに行った。", "It being",
     [("Being", "主語を省くと分詞の主語は主節の we になり、「私たちが晴れた日だった」という意味になる。"),
      ("It was", "節をコンマだけで主節につなぐことはできない。接続詞が必要。"), ("It been", "been だけでは分詞構文にならない。現在分詞 being を使う。")]),
    ("(　　) by the noise, the baby began to cry.", "物音に驚いて、赤ちゃんは泣き出した。", "Surprised",
     [("Surprising", "現在分詞にすると、赤ちゃんが人を驚かせる側になる。"), ("Having surprised", "能動の完了形で、赤ちゃんが何かを驚かせたことになる。"),
      ("To surprise", "不定詞にすると「驚かせるために」の意味になる。")]),
    ("(　　) up in the countryside, I know the names of many plants.", "いなかで育ったので、私は多くの植物の名前を知っている。", "Brought",
     [("Bringing", "現在分詞にすると、主語 I が（だれかを）育てる側になる。"), ("Having brought", "能動の完了形で、主語 I がだれかを育てたことになる。"),
      ("To bring", "不定詞にすると「育てるために」の意味になる。")]),
    ("(　　) no money with me, I couldn't buy lunch.", "お金を持っていなかったので、昼食を買えなかった。", "Having",
     [("Had", "過去形だけでは、主語のない節にも分詞構文にもならない。"), ("Being had", "受け身にすると主語 I が「持たれる」側になり、意味が通らない。"),
      ("To have", "不定詞にすると「持つために」の意味になる。")]),
    ("(　　) by her parents, she decided to study abroad.", "両親に励まされて、彼女は留学することに決めた。", "Encouraged",
     [("Encouraging", "現在分詞にすると、彼女が（だれかを）励ます側になる。"), ("Having encouraged", "能動の完了形で、彼女がだれかを励ましたことになる。"),
      ("To encourage", "不定詞にすると「励ますために」の意味になる。")]),
    ("Generally (　　), Japanese trains are very punctual.", "一般的に言えば、日本の電車は時間にとても正確だ。", "speaking",
     [("spoken", "generally speaking は慣用的な分詞構文で、過去分詞にはしない。"), ("speak", "動詞の原形ではこの慣用表現にならない。"),
      ("to speak", "generally to speak という表現はない。")]),
    ("(　　) from his accent, he must be from Osaka.", "なまりから判断すると、彼は大阪出身にちがいない。", "Judging",
     [("Judged", "過去分詞にすると「判断される」の意味になり、judging from ～「～から判断すると」の慣用表現にならない。"),
      ("Judge", "動詞の原形で文を始めると命令文になり、主節とつながらない。"), ("Judgment", "名詞では from 以下とつながらず、主節を修飾できない。")]),
    ("(　　) on the weather, the event will be held on Sunday.", "天気しだいで、催しは日曜日に行われる。", "Depending",
     [("Depended", "depend は自動詞で、過去分詞を受け身の意味で使えない。"), ("Depend", "動詞の原形で文を始めると命令文になり、主節とつながらない。"),
      ("Dependent", "dependent は be dependent on の形で使う形容詞で、この位置で「～しだいで」の意味にならない。")]),
    ("(　　) his age, he looks very young.", "年齢を考えると、彼はとても若く見える。", "Considering",
     [("Considered", "過去分詞にすると「考えられた」の意味になり、considering ～「～を考えると」の表現にならない。"),
      ("Consider", "動詞の原形で文を始めると命令文になり、主節とつながらない。"), ("Consideration", "名詞では目的語 his age をとれない。")]),
]


@gen("standard_practice", 5, ["condition_check", "common_error"])
def construction_form(r):
    s, jp, ok, wrongs = r.choice(CFORM)
    return mc(f"日本語の意味になるように、（　）に入る最も適切なものを選びなさい。\n{jp}\n{s}", [ok] + [w for w, _ in wrongs],
              f"{ok} が入る。主節の主語と分詞の関係（能動・受け身）、時のずれ、主語の一致、慣用表現かどうかを確かめて形を決める。", d=3,
              ap="分詞構文の意味上の主語は主節の主語。その主語が「する側」か「される側」か、主節より前の時か、を確かめる。",
              steps=["主節の主語を確認する。", "主語と分詞の関係（能動・受け身）と、時のずれ・主語の違い・慣用表現かを判断する。", f"答え：{ok}"],
              alt=["選んだ形を接続詞の文（When / Because など）に戻し、主語と時制・態が日本語と一致するかを確かめる。"],
              pc=[("主語と分詞の関係を正しく判断している", 2), ("正しい形を選んでいる", 2)],
              pit=["主節の主語を確かめずに、日本語の訳だけで現在分詞を選ぶ。", "Having＋過去分詞の必要な「前の時」を見落とす。"],
              why={w: (reason, "分詞構文の形（態・時・主語）の誤り") for w, reason in wrongs})


ORDERS = [
    ("公園で走っている少年は私の弟だ。", ["the boy", "running", "in the park", "is", "my brother"], "running in the park が the boy を後ろから修飾する。"),
    ("これは50年前に建てられた家だ。", ["this", "is", "a house", "built", "fifty years ago"], "過去分詞 built が a house を後ろから修飾する（家は建てられる側）。"),
    ("何を言えばよいかわからず、私は黙っていた。", ["not", "knowing", "what to say,", "I", "kept", "silent"], "否定の分詞構文は Not＋分詞。"),
    ("彼女は目を閉じて音楽を聞いていた。", ["she", "was listening to", "music", "with", "her eyes", "closed"], "付帯状況の with O＋過去分詞（目は閉じられた状態）。"),
    ("宿題を終えてから、私はテレビを見た。", ["having", "finished", "my homework,", "I", "watched", "TV"], "主節より前の時は完了分詞構文 Having＋過去分詞。"),
    ("遠くから見ると、その岩は人の顔のように見える。", ["seen", "from", "a distance,", "the rock", "looks like", "a human face"], "岩は見られる側なので過去分詞 Seen で始める。"),
    ("彼はソファーに座って新聞を読んでいた。", ["he", "sat", "on the sofa,", "reading", "a newspaper"], "付帯状況の分詞構文は主節の後ろに置くことが多い。"),
    ("その知らせに驚いて、彼女は一言も言えなかった。", ["surprised", "at", "the news,", "she", "couldn't", "say a word"], "彼女は驚かされた側なので過去分詞 Surprised で始める。"),
    ("犬がしっぽを振りながら私の方へ走ってきた。", ["the dog", "ran", "toward me", "with", "its tail", "wagging"], "付帯状況の with O＋現在分詞（しっぽが振れている）。"),
    ("天気がよかったので、私たちは海へ行った。", ["it", "being", "fine,", "we", "went", "to the sea"], "主節の主語と違う it を残す独立分詞構文。"),
    ("今朝、英語で書かれた手紙が届いた。", ["a letter", "written", "in English", "arrived", "this morning"], "過去分詞 written が a letter を後ろから修飾する。"),
]


@gen("standard_practice", 5, ["application", "computation"])
def build_order(r):
    jp, parts, point = r.choice(ORDERS)
    sent = " ".join(parts)
    sent = sent[0].upper() + sent[1:] + "."
    return order(f"日本語に合うように、語句を並べかえて英文を完成させなさい。ただし、文頭にくる語も小文字で示してあり、コンマは語句に含めてある。\n{jp}", parts,
                 f"{sent}　{point}", d=3, p=4,
                 ap="分詞のまとまり（分詞＋目的語・修飾語）を先に作り、それが名詞を修飾するのか、文全体にかかる分詞構文なのかを決める。",
                 steps=["分詞と、それに続く語句のまとまりを作る。", "名詞を修飾するなら名詞の直後、分詞構文なら文頭（または主節の後ろ）に置く。", f"ポイント：{point}", f"完成文：{sent}"],
                 alt=["完成した英文を和訳し直して、日本語と一致するかを確かめる。"],
                 pc=[("分詞のまとまりを正しく作っている", 2), ("全体の語順が正しい", 2)],
                 pit=["語句を伴う分詞を名詞の前に置く。", "付帯状況の with の後ろで O と分詞の順を逆にする。"])


# (分詞構文の文, 正答, [(誤答, 理由)])
CLAUSE = [
    ("Having lost my key, I couldn't get into the house.", "Because I had lost my key, I couldn't get into the house.",
     [("Because I lose my key, I couldn't get into the house.", "完了分詞構文は主節より前の時を表すので、過去完了 had lost が必要。現在形では時制が合わない。"),
      ("Though I had lost my key, I couldn't get into the house.", "譲歩にすると「鍵をなくしたのに入れなかった」となり、前後の因果関係に合わない。"),
      ("After I couldn't get into the house, I had lost my key.", "できごとの前後関係が逆になっている。鍵をなくしたのが先。")]),
    ("Seen from the tower, the city looks beautiful.", "When the city is seen from the tower, it looks beautiful.",
     [("When the city sees the tower, it looks beautiful.", "能動にすると「町が塔を見る」となる。過去分詞 Seen は町が「見られる」側であることを示す。"),
      ("Though the city is seen from the tower, it looks beautiful.", "譲歩にすると「塔から見られるのに美しく見える」となり、意味が通らない。"),
      ("When I saw the city from the tower, it looked beautiful.", "主節の時制 looks（現在）を looked（過去）に変えてしまっている。")]),
    ("Not feeling well, she left school early.", "As she didn't feel well, she left school early.",
     [("As she felt well, she left school early.", "否定語 not が抜けていて、意味が逆になる。"),
      ("Though she didn't feel well, she left school early.", "譲歩にすると「気分が悪かったのに早退した」となり、因果関係に合わない。"),
      ("If she doesn't feel well, she left school early.", "条件にすると主節の過去の事実と合わず、時制も一致しない。")]),
    ("Written in simple English, the book is easy to read.", "As the book is written in simple English, it is easy to read.",
     [("As the book writes in simple English, it is easy to read.", "能動にすると「本が書く」ことになる。本は「書かれた」側。"),
      ("Though the book is written in simple English, it is easy to read.", "譲歩にすると「やさしい英語で書かれているのに読みやすい」となり、因果関係に合わない。"),
      ("As the book was written in simple English, it was easy to read.", "主節の時制 is（現在）を was（過去）に変えてしまっている。")]),
    ("Turning left at the bank, you will see the library.", "If you turn left at the bank, you will see the library.",
     [("Though you turn left at the bank, you will see the library.", "譲歩にすると「左に曲がるのに見える」となり、意味が通らない。"),
      ("If the bank turns left, you will see the library.", "分詞の意味上の主語は主節の主語 you であり、the bank ではない。"),
      ("If you turned left at the bank, you would see the library.", "現実にありうる道案内で、仮定法にする根拠がない。主節の will とも合わない。")]),
    ("It being Sunday, the shop was closed.", "As it was Sunday, the shop was closed.",
     [("As the shop was Sunday, it was closed.", "分詞の主語は残された It で、主節の主語 the shop ではない。"),
      ("Though it was Sunday, the shop was closed.", "譲歩にすると「日曜日なのに閉まっていた」となり、因果関係に合わない。"),
      ("As it is Sunday, the shop was closed.", "主節が過去（was closed）なので、従属節も過去形 was にする。")]),
    ("Having been told the news, he was not surprised.", "As he had been told the news, he was not surprised.",
     [("As he had told the news, he was not surprised.", "能動にすると「彼が知らせを伝えた」側になる。Having been told は「知らされていた」という受け身。"),
      ("Though he had been told the news, he was not surprised.", "譲歩にすると「知らされていたのに驚かなかった」となり、因果関係に合わない。"),
      ("As he is told the news, he was not surprised.", "完了分詞構文は主節より前の時なので、過去完了 had been told にする。")]),
    ("Living in the country, I rarely see tall buildings.", "As I live in the country, I rarely see tall buildings.",
     [("Though I live in the country, I rarely see tall buildings.", "譲歩にすると「いなかに住んでいるのに高い建物をめったに見ない」となり、因果関係に合わない。"),
      ("If I lived in the country, I would rarely see tall buildings.", "事実を述べる文で、仮定法にする根拠がない。主節の時制も変わっている。"),
      ("As I am lived in the country, I rarely see tall buildings.", "live は自動詞なので受け身にできない。")]),
    ("The sun having set, we went home.", "After the sun had set, we went home.",
     [("After we had set the sun, we went home.", "分詞の主語は残された The sun で、主節の主語 we ではない。"),
      ("Though the sun had set, we went home.", "譲歩にすると「日が沈んだのに帰った」となり、文脈に合わない。"),
      ("After the sun sets, we went home.", "完了分詞構文は主節（過去）より前の時なので、過去完了 had set にする。")]),
    ("Born in Canada, she speaks both English and French.", "As she was born in Canada, she speaks both English and French.",
     [("As she bore in Canada, she speaks both English and French.", "能動にすると「彼女が産んだ」側になる。Born は「生まれた（産まれた）」という受け身。"),
      ("Though she was born in Canada, she speaks both English and French.", "譲歩にすると「カナダで生まれたのに両方話す」となり、因果関係に合わない。"),
      ("As she is born in Canada, she speaks both English and French.", "生まれたのは過去のことなので was born にする。")]),
]


@gen("standard_practice", 5, ["concept", "computation"])
def construction_to_clause(r):
    s, ok, wrongs = r.choice(CLAUSE)
    return mc(f"次の英文とほぼ同じ意味を表す英文として、最も適切なものを選びなさい。\n{s}", [ok] + [w for w, _ in wrongs],
              f"「{ok}」が正しい。分詞構文の意味上の主語・態（能動か受け身か）・時（主節と同じか前か）・主節との意味の関係を、すべて保って書きかえている。", d=3,
              ap="分詞構文を接続詞の文に戻すときは、①主語、②態（能動・受け身）、③時制、④接続詞の意味、の4点を1つずつ確かめる。",
              steps=["分詞の意味上の主語（主節の主語、または残された主語）を確認する。", "分詞が現在分詞か過去分詞か、完了形かを確認する。",
                     "主節とのつながりから接続詞を決める。", f"4点がすべて一致する「{ok}」を選ぶ。"],
              alt=["選んだ文から、もう一度分詞構文を作り直して、問題文と一致するかを確かめる。"],
              pc=[("主語・態・時制を正しく対応させている", 2), ("接続詞の意味を正しく判断している", 2)],
              pit=["完了分詞構文を戻すときに過去完了にしない。", "接続詞を when / because に決めつけ、文脈を確かめない。"],
              why={w: (reason, "分詞構文と接続詞の文の対応（主語・態・時制・意味）の誤り") for w, reason in wrongs})


# ======================================================================
# C 思考力・記述応用
# ======================================================================

PAIRS = [
    ("I saw a boy crossing the street.", "I saw a boy cross the street.",
     "どちらも知覚動詞 see＋O＋C の文。Aは現在分詞で「少年が通りを渡っているところを見た」と、動作の途中の一場面を表す。Bは原形不定詞で「少年が通りを渡るのを（最初から最後まで）見た」と、動作の全体を表す。"),
    ("The movie was boring.", "I was bored with the movie.",
     "bore は「（人を）退屈させる」という動詞。Aは映画が人を退屈させる側なので現在分詞 boring で「その映画は退屈だった」。Bは私が退屈させられた側なので過去分詞 bored で「私はその映画に退屈した」。"),
    ("Look at the sleeping baby.", "We booked a sleeping car.",
     "Aの sleeping は現在分詞で、baby が「眠っている」という状態を表す（The baby is sleeping. が成り立つ）。Bの sleeping は動名詞で、「眠るための車両（寝台車）」という用途を表す（The car is sleeping. は成り立たない）。"),
    ("Seeing the dog, the girl ran away.", "Seen from here, the dog looks like a bear.",
     "Aは現在分詞で、主語 the girl が犬を「見る」側なので「犬を見て、少女は逃げ出した」。Bは過去分詞で、主語 the dog が「見られる」側なので「ここから見ると、その犬はクマのように見える」。"),
    ("Look at the fallen leaves.", "Look at the falling leaves.",
     "fall は自動詞。Aの過去分詞 fallen は完了を表し「落ちてしまった葉（落ち葉）」。Bの現在分詞 falling は進行を表し「今まさに落ちている葉（舞い落ちる葉）」。"),
    ("Who is that dancing girl?", "I need new dancing shoes.",
     "Aの dancing は現在分詞で「踊っている少女」（The girl is dancing. が成り立つ）。Bの dancing は動名詞で「踊るための靴（ダンスシューズ）」という用途を表す（The shoes are dancing. は成り立たない）。"),
    ("The girl singing on the stage is my sister.", "The song sung by the girl is popular.",
     "Aは現在分詞で、少女が「歌っている」側（能動）なので「舞台で歌っている少女は私の姉（妹）だ」。Bは過去分詞で、歌が「歌われる」側（受け身）なので「その少女が歌った歌は人気がある」。"),
    ("He sat with his arms folded.", "He sat there, folding his arms.",
     "Aは付帯状況の with O＋過去分詞で、腕が「組まれた状態」で座っていたことを表し「彼は腕を組んで座っていた」。Bは分詞構文で、主語の彼が「腕を組む」動作をしながら座っていたことを表し「彼はそこに座って腕を組んでいた」。Aは状態、Bは主語の動作に重点がある。"),
]


@gen("thinking_writing", 4, ["written_reasoning", "concept"])
def explain_difference(r):
    a, b, model = r.choice(PAIRS)
    return desc(f"次の2つの英文A・Bの意味の違いを、分詞（または動名詞）の働きに触れながら日本語で説明しなさい。\nA：{a}\nB：{b}", model,
                "分詞の形（現在分詞・過去分詞）は、名詞（主語）との関係が能動か受け身か、進行か完了かで決まる。～ing には分詞と動名詞の2つの働きがあるので、名詞との関係で見分ける。",
                [("Aの形とその働きを正しく説明している", 3), ("Bの形とその働きを正しく説明している", 3), ("A・Bの和訳がそれぞれ正しい", 2)], d=4, p=8, lines=6,
                ap="A・Bで形の違う部分を見つけ、名詞（主語）を主語にした be 動詞の文（The baby is sleeping. など）が成り立つかを試す。",
                steps=["A・Bで違う部分を特定する。", "それぞれ、名詞との関係（能動・受け身、進行・完了、用途）を確かめる。", "和訳を示しながら違いを説明する。"],
                alt=["関係代名詞を使った文（a girl who is dancing ／ shoes for dancing など）に書きかえて違いを示す方法もある。"],
                pc=[("Aの説明", 3), ("Bの説明", 3), ("和訳", 2)],
                pit=["和訳だけを書き、形の違いの根拠を示さない。", "～ing をすべて「～している」と訳す。"])


# (関係詞の文, 答え, 説明)
REL = [
    ("The girl who is playing the piano is my sister.", "The girl playing the piano is my sister.", "主格の関係代名詞＋be 動詞（who is）を省くと、現在分詞が名詞を後ろから修飾する形になる。"),
    ("This is a car which was made in Germany.", "This is a car made in Germany.", "which was を省くと、過去分詞 made が名詞を後ろから修飾する形になる（車は作られる側）。"),
    ("The students who were invited to the party were all first-year students.", "The students invited to the party were all first-year students.", "who were を省くと、過去分詞 invited が名詞を後ろから修飾する形になる。"),
    ("Do you know the man who is talking with Ms. Kato?", "Do you know the man talking with Ms. Kato?", "who is を省くと、現在分詞 talking が名詞を後ろから修飾する形になる。"),
    ("The bridge which was built last year is already famous.", "The bridge built last year is already famous.", "which was を省くと、過去分詞 built が名詞を後ろから修飾する形になる。"),
    ("Look at the bird which is flying over the lake.", "Look at the bird flying over the lake.", "which is を省くと、現在分詞 flying が名詞を後ろから修飾する形になる。"),
    ("Most of the people who live in this town work in the city.", "Most of the people living in this town work in the city.",
     "主格の関係代名詞＋一般動詞（who live）は、動詞を現在分詞 living にして書きかえられる（進行の意味でなくても、能動の関係なら現在分詞）。"),
    ("The books which were left on the desk belong to Ken.", "The books left on the desk belong to Ken.", "which were を省くと、過去分詞 left が名詞を後ろから修飾する形になる。"),
]


@gen("thinking_writing", 3, ["cross_unit", "written_reasoning"], rel=["HS-ENG-U06", "JH-ENG-G3-U02"])
def relative_to_participle(r):
    s, ans, why_s = r.choice(REL)
    return desc(f"次の英文を、関係代名詞を使わずに分詞を使ってほぼ同じ意味の英文に書きかえなさい。また、現在分詞・過去分詞のどちらを使ったか、その理由を関係代名詞の節と比べて説明しなさい。\n{s}",
                f"{ans}　{why_s}", f"関係代名詞の節が「名詞が～している（する）」なら現在分詞、「名詞が～される（された）」なら過去分詞で書きかえられる。{why_s}",
                [("分詞を使った英文を正しく書いている", 4), ("現在分詞・過去分詞を選んだ理由を、能動・受け身の関係で説明している", 3), ("関係代名詞の節との対応を示している", 1)], d=4, p=8, lines=5,
                ap="関係代名詞の節の中の動詞が、先行詞にとって能動か受け身かを確かめる。who is / which was など「関係代名詞＋be 動詞」は省いて分詞だけを残せる。",
                steps=["先行詞と関係代名詞の節を確認する。", "節の動詞が能動（する側）か受け身（される側）かを判断する。", "関係代名詞（と be 動詞）を省き、分詞を名詞の直後に置く。", f"答え：{ans}"],
                alt=["書きかえた文に関係代名詞と be 動詞を補って元に戻し、意味が変わらないかを確かめる。"],
                pc=[("分詞を使った英文", 4), ("理由の説明", 3), ("関係代名詞の節との対応", 1)],
                pit=["受け身の関係なのに現在分詞を使う（a car making in Germany）。", "関係代名詞だけを省き、be 動詞を残す。"])


# (分詞構文, 答え, 説明)
TOCLAUSE = [
    ("Having lived in Kyoto for ten years, he knows the city very well.", "Because he has lived in Kyoto for ten years, he knows the city very well.（Because の代わりに As も可）",
     "京都に10年住んでいることが、町をよく知っている理由になっている。完了分詞構文は主節 knows（現在）より前から続くことなので、現在完了 has lived にする。"),
    ("Not having received an answer, I wrote to her again.", "Because I had not received an answer, I wrote to her again.（As も可）",
     "返事が来ていなかったことが、もう一度手紙を書いた理由。完了分詞構文は主節 wrote（過去）より前のことなので、過去完了 had not received にする。"),
    ("Left alone in the room, the little boy began to cry.", "When the little boy was left alone in the room, he began to cry.",
     "部屋に一人残されたときに泣き出した、という時の関係。過去分詞 Left は男の子が「残された」側であることを示すので、受け身 was left にする。"),
    ("Living next door, she rarely visits us.", "Though she lives next door, she rarely visits us.",
     "隣に住んでいるのにめったに訪ねてこない、という予想に反する関係なので譲歩の Though を使う。主節が現在形なので lives にする。"),
    ("Following this map, you will find the station easily.", "If you follow this map, you will find the station easily.",
     "地図に従えば駅が見つかる、という条件の関係。主節が will を使った未来の内容なので、条件の副詞節では現在形 follow にする。"),
    ("The bus being late, we missed the first class.", "Because the bus was late, we missed the first class.",
     "バスが遅れたことが授業に遅れた理由。分詞の前の The bus が意味上の主語（独立分詞構文）なので、従属節の主語は the bus にする。"),
    ("Seen from space, the earth looks blue.", "When the earth is seen from space, it looks blue.（If も可）",
     "宇宙から見ると青く見える、という時（条件）の関係。過去分詞 Seen は地球が「見られる」側であることを示すので、受け身 is seen にする。"),
]


@gen("thinking_writing", 3, ["written_reasoning", "condition_check"])
def construction_to_conj(r):
    s, ans, why_s = r.choice(TOCLAUSE)
    return desc(f"次の英文を、適切な接続詞を使ってほぼ同じ意味の英文に書きかえなさい。また、その接続詞を選んだ理由と、動詞の形（時制・態）の決め方を説明しなさい。\n{s}",
                f"{ans}　{why_s}", f"分詞構文には接続詞がないので、主節との意味のつながりから接続詞を決める。時制は主節に合わせ、完了分詞構文なら主節より前の時にする。{why_s}",
                [("接続詞を使った英文を正しく書いている", 4), ("接続詞を選んだ理由を、主節との関係で説明している", 2), ("時制・態の決め方を説明している", 2)], d=4, p=8, lines=5,
                ap="分詞構文と主節を日本語で並べて、「とき」「ので」「れば」「けれども」のどれでつなぐと自然かを考え、次に時制と態を決める。",
                steps=["分詞構文と主節の意味の関係を判断し、接続詞を決める。", "分詞の意味上の主語を補う（主節の主語、または残された主語）。",
                       "時制（主節と同じ時か、前の時か）と態（能動か受け身か）を決める。", f"答え：{ans}"],
                alt=["書きかえた文から、もう一度分詞構文を作り直して、元の文と一致するかを確かめる。"],
                pc=[("接続詞を使った英文", 4), ("接続詞の選択理由", 2), ("時制・態の説明", 2)],
                pit=["Having＋過去分詞を戻すときに、主節と同じ時制にしてしまう。", "過去分詞で始まる分詞構文を能動の文に戻す。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(task, wrong, step, etype, tempt, fix, ans, expl, steps, ap, alt, pit, d=3):
    return desc(f"{task}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい英文に書き直しなさい。", ans, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい英文に直している", 3), ("文法の規則を説明している", 1)], d=d, p=6, lines=5,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい英文", 3), ("規則の説明", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix))


# (和文, 誤答, 正答, 誤りの箇所, 規則, 誤りやすい理由)
VOICE_ERR = [
    ("これは英語で書かれた本だ。", "This is a book writing in English.", "This is a book written in English.", "writing",
     "本は「書かれる」側なので過去分詞 written を使う。", "「書かれた」の「書く」に注目して、現在分詞を使った。"),
    ("私はそのコンサートでとてもわくわくした。", "I was very exciting at the concert.", "I was very excited at the concert.", "exciting",
     "私は「わくわくさせられた」側なので過去分詞 excited を使う。exciting は「人をわくわくさせる」。", "日本語の「わくわくする」から exciting を選んだ。"),
    ("川で泳いでいる少年を見て。", "Look at the boy swum in the river.", "Look at the boy swimming in the river.", "swum",
     "少年は「泳いでいる」側（能動・進行）なので現在分詞 swimming を使う。", "分詞は過去分詞を使うものと思い込み、swim の過去分詞を使った。"),
    ("その映画はとても退屈で、私は眠ってしまった。", "The movie was so bored that I fell asleep.", "The movie was so boring that I fell asleep.", "bored",
     "映画は人を「退屈させる」側なので現在分詞 boring を使う。", "「退屈した」という自分の気持ちから bored を選んだ。"),
    ("丘から見ると、その町は小さく見える。", "Seeing from the hill, the town looks small.", "Seen from the hill, the town looks small.", "Seeing",
     "分詞構文の意味上の主語は主節の主語 the town。町は「見られる」側なので過去分詞 Seen で始める。", "「見ると」を見る人（自分）の動作と考えた。"),
    ("彼女は脚を組んで座っていた。", "She was sitting with her legs crossing.", "She was sitting with her legs crossed.", "crossing",
     "with O＋分詞で、脚は「組まれた」状態なので過去分詞 crossed を使う。", "「脚を組んで」という日本語から、動作を表す現在分詞を選んだ。"),
    ("スペイン語はメキシコで話されている言語だ。", "Spanish is the language speaking in Mexico.", "Spanish is the language spoken in Mexico.", "speaking",
     "言語は「話される」側なので過去分詞 spoken を使う。", "「話されている」の「～している」から現在分詞を選んだ。"),
    ("その犬は家の前を通り過ぎる男性にほえた。", "The dog barked at a man walked past the house.", "The dog barked at a man walking past the house.", "walked",
     "男性は「歩いている」側（能動）なので現在分詞 walking を使う。walked だと文の中に動詞が2つ並んでしまう。", "過去の文なので、修飾語の動詞も過去形にした。"),
    ("私は科学に興味がある。", "I'm interesting in science.", "I'm interested in science.", "interesting",
     "私は「興味を持たされている」側なので過去分詞 interested を使う。interesting は「人に興味を持たせる（おもしろい）」。", "「興味がある」という日本語から interesting を選んだ。"),
]


@gen("error_correction", 4, ["common_error", "condition_check"])
def err_voice(r):
    jp, wrong, fix, where, rule, tempt = r.choice(VOICE_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"分詞「{where}」", "concept", tempt, fix, fix, f"{rule}正しくは {fix}",
                    ["分詞が修飾する名詞（または分詞構文の主語・with の O）を確認する。", "その名詞が「する側」か「される側」かを判断する。", f"正しい英文：{fix}"],
                    "分詞の形は日本語の「～している」「～た」ではなく、名詞と分詞の関係（能動か受け身か）で決める。",
                    ["名詞を主語にして be 動詞＋分詞の文を作り（The book is written. など）、意味が通るかを確かめる。"],
                    ["日本語の訳語だけで現在分詞・過去分詞を決める。"], d=3)


# (和文, 誤答, 正答, 誤りの箇所, 種類, 規則, 誤りやすい理由)
SUBJ_ERR = [
    ("雨だったので、試合は中止された。", "Being rainy, the game was canceled.", "It being rainy, the game was canceled.", "Being rainy", "logic",
     "主語を省くと分詞の意味上の主語は主節の the game になり、「試合が雨だった」ことになる。主語が違うので It を残す（It was rainy, so the game was canceled. も可）。", "主語を省くのが分詞構文の作り方だと覚え、主語が同じかを確かめなかった。"),
    ("駅に着くと、電車はすでに出発していた。", "Arriving at the station, the train had already left.", "Arriving at the station, I found that the train had already left.", "the train", "logic",
     "主節の主語 the train が分詞の意味上の主語になり、「電車が駅に着いた」ことになる。駅に着いた人（I）を主節の主語にする。", "日本語の文の形をそのまま英語にし、主語の一致を確かめなかった。"),
    ("窓から外を見ると、雪が降っていた。", "Looking out of the window, it was snowing.", "Looking out of the window, I saw that it was snowing.", "it was snowing", "logic",
     "分詞の意味上の主語が主節の it になってしまう。外を見た人（I）を主節の主語にする。", "日本語の「雪が降っていた」をそのまま主節にした。"),
    ("日が沈んだので、私たちはキャンプ場に戻った。", "Having set, we went back to the campsite.", "The sun having set, we went back to the campsite.", "Having set", "logic",
     "沈んだのは the sun で、主節の主語 we と違うので、分詞の前に The sun を残す。", "主語を省くと we が沈んだことになることに気づかなかった。"),
    ("バスがなかったので、私たちは歩いて帰った。", "Being no bus, we walked home.", "There being no bus, we walked home.", "Being no bus", "logic",
     "there 構文の分詞構文では there を残して There being とする。", "there を主語と考えず、省いてしまった。"),
    ("彼の住所を知らなかったので、手紙を書けなかった。", "Knowing not his address, I couldn't write to him.", "Not knowing his address, I couldn't write to him.", "Knowing not", "notation",
     "分詞構文を否定するときは、not を分詞の直前に置く。", "do not の not と同じように動詞の後ろに置けると考えた。"),
]


@gen("error_correction", 3, ["common_error", "written_reasoning"])
def err_subject(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(SUBJ_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", etype, tempt, fix, fix, rule,
                    ["分詞の動作をするのはだれ（何）かを確認する。", "それが主節の主語と同じかを確かめ、違えば主語を残すか、主節の主語を変える。", f"正しい英文：{fix}"],
                    "分詞構文の意味上の主語は、主語を残さない限り主節の主語になる。分詞の動作をするものと主節の主語が一致しているかを必ず確かめる。",
                    ["分詞構文を接続詞の文に戻し（As it was rainy, ... など）、主語が何になるかを確かめる。"],
                    ["主節の主語と分詞の主語が違うのに、分詞の主語を省く。"], d=3)


# (和文, 誤答, 正答, 誤りの箇所, 規則, 誤りやすい理由)
TENSE_ERR = [
    ("以前その本を読んだことがあったので、私は話の筋を知っていた。", "Reading the book before, I knew the story.", "Having read the book before, I knew the story.", "Reading",
     "読んだのは主節 knew より前のことなので、完了分詞構文 Having read を使う。", "主節が過去形なので、分詞も過去のことを表せると考えた。"),
    ("3年間アメリカに住んでいたので、彼は英語が上手だ。", "Living in America for three years, he speaks English well.", "Having lived in America for three years, he speaks English well.", "Living",
     "住んでいたのは主節 speaks より前の期間なので、完了分詞構文 Having lived を使う。", "「住んでいた」の継続の意味を、現在分詞で表せると考えた。"),
    ("一度もそこに行ったことがなかったので、私は道に迷った。", "Never being there before, I got lost.", "Never having been there before, I got lost.", "being",
     "経験がなかったのは主節 got lost より前のことなので、Never having been を使う。", "「行ったことがない」の経験の意味を、完了形にしなかった。"),
    ("以前先生に注意されたことがあったので、彼は二度と遅刻しなかった。", "Being warned by the teacher before, he was never late again.", "Having been warned by the teacher before, he was never late again.", "Being warned",
     "注意されたのは主節より前のことなので、受け身の完了分詞構文 Having been warned を使う。", "受け身にすることに気をとられ、時のずれを見落とした。"),
    ("昨夜よく眠れなかったので、今日は眠い。", "Not sleeping well last night, I feel sleepy today.", "Not having slept well last night, I feel sleepy today.", "sleeping",
     "昨夜のことは主節 feel（今日）より前なので、Not having slept を使う。", "last night があれば過去のことだとわかると考え、完了形にしなかった。"),
    ("財布をなくしてしまっていたので、昼食が買えなかった。", "Losing my wallet, I couldn't buy lunch.", "Having lost my wallet, I couldn't buy lunch.", "Losing",
     "財布をなくしたのは昼食を買おうとしたときより前なので、Having lost を使う。", "分詞構文はいつも現在分詞で始めると思い込んだ。"),
]


@gen("error_correction", 3, ["common_error", "computation"])
def err_tense(r):
    jp, wrong, fix, where, rule, tempt = r.choice(TENSE_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"分詞「{where}」", "concept", tempt, fix, fix, rule,
                    ["分詞構文の内容と主節の内容の時を比べる。", "分詞構文の内容が主節より前なら Having＋過去分詞にする（否定は Not / Never を前に置く）。", f"正しい英文：{fix}"],
                    "分詞構文の内容が主節より前の時なら、完了分詞構文（Having＋過去分詞）を使う。",
                    ["接続詞の文に戻し（As I had read ... など）、従属節の時制が主節より前（過去完了・現在完了）になるかを確かめる。"],
                    ["主節より前のことなのに、単純な現在分詞を使う。"], d=3)


GENERATORS = [participle_modifier, emotion_participle, construction_meaning, with_attendant,
              make_construction, construction_form, build_order, construction_to_clause,
              explain_difference, relative_to_participle, construction_to_conj,
              err_voice, err_subject, err_tense]
