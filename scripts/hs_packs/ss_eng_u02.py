"""単元パック：二次試験対策　英語　自由英作文・和文英訳。

例文・意見文・模範解答はすべてこのパックのためのオリジナル。資料の数値はすべて架空である。
"""
from fractions import Fraction

from banks._common import desc, mc, order
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem,
                         tp)

UNIT_ID = "SS-ENG-U02"

PREREQUISITES = [
    ("HS-ENG-U10", "和文和訳で日本語を言いかえる手順と、主張→理由→結論の意見文の基本構成を使えること"),
    ("HS-ENG-U02", "現在完了・過去完了と、時・条件の副詞節の時制を正しく使い分けられること"),
    ("HS-ENG-U07", "倍数表現・the 比較級, the 比較級 などの比較構文を英文で書けること"),
    ("HS-ENG-U08", "仮定法過去・過去完了・as if を使って、事実に反する内容を書けること"),
]
EXTENSIONS = [
    ("SS-ENG-U01", "英文を組み立てる側から構文を理解し、英文和訳で構文を見抜く力として逆向きに生かす"),
    ("SS-JPN-U01", "主張→根拠→結論の論述の型と、字数・条件を満たす答案作りを日本語の記述問題にも使う"),
    ("SS-SOC-U01", "資料の数値を比較表現で正確に述べ、原因を一つ挙げて論じる手順を地歴公民の論述に生かす"),
]


def cap(s):
    return s[0].upper() + s[1:]


# ======================================================================
# A 用のデータ
# ======================================================================

# 和文和訳：(日本語, 適切な英語, [(誤り, 理由)])
REPHRASE = [
    ("彼は顔が広い。", "He knows a lot of people.",
     [("His face is wide.", "慣用句を直訳しており、英語では顔の大きさの話になってしまう。「知り合いが多い」と言いかえて訳す。"),
      ("He has a big face.", "直訳で、顔の大きさを述べる文になる。"), ("He is famous for his face.", "顔が有名だという意味になり、「知り合いが多い」という意味が伝わらない。")]),
    ("この仕事は骨が折れる。", "This job is very hard.",
     [("This job breaks my bones.", "慣用句を直訳しており、実際に骨折する意味になる。「とても大変だ」と言いかえる。"),
      ("This job is dangerous for my bones.", "骨への危険の話ではない。「骨が折れる」は「苦労が多い」という意味である。"), ("This job has broken bones.", "仕事が骨折しているという意味不明な文になる。")]),
    ("最近は猫も杓子もスマートフォンを持っている。", "These days almost everyone has a smartphone.",
     [("These days cats and spoons have smartphones.", "「猫も杓子も」は「だれもかれも」という慣用句で、直訳すると意味が通らない。"),
      ("These days even cats have smartphones.", "猫の話ではなく、「ほとんどすべての人」という意味である。"), ("These days only some people have smartphones.", "「だれもかれも」と逆の意味になっている。")]),
    ("彼は口が重い。", "He doesn't talk much.",
     [("His mouth is heavy.", "慣用句の直訳で、英語では意味が伝わらない。「あまり話さない」と言いかえる。"),
      ("He talks too much.", "「口が重い」と逆の意味（口が軽い・おしゃべり）になっている。"), ("He has a heavy voice.", "声の質の話ではない。")]),
    ("その知らせを聞いて、胸がいっぱいになった。", "I was deeply moved by the news.",
     [("My chest became full when I heard the news.", "慣用句の直訳で、英語では体の状態を述べる文になる。「深く感動した」と言いかえる。"),
      ("I was full after hearing the news.", "full は「満腹の」の意味になり、感動を表さない。"), ("The news filled my chest.", "直訳で、知らせが胸を物理的に満たすという意味不明な文になる。")]),
    ("試験が近づくと、気が気でない。", "I feel very nervous as the exam approaches.",
     [("As the exam approaches, my mind is not my mind.", "慣用句の直訳で、英語では意味をなさない。「とても不安だ」と言いかえる。"),
      ("I don't care about the exam as it approaches.", "「気にしない」と逆の意味になっている。"), ("I feel relaxed as the exam approaches.", "「気が気でない（落ち着かない）」と逆の意味である。")]),
    ("彼の話は耳が痛かった。", "What he said was hard to hear because it was true.",
     [("My ears hurt when he talked.", "慣用句の直訳で、実際に耳が痛むという意味になる。「（本当のことなので）聞くのがつらい」と言いかえる。"),
      ("His story was too loud.", "音の大きさの話ではない。"), ("I didn't hear his story.", "話を聞かなかったという意味になり、元の日本語と合わない。")]),
    ("あのレストランは値段の割においしい。", "The food at that restaurant is good for the price.",
     [("That restaurant is delicious for its price.", "店そのものがおいしいことになる。英語では料理（the food）を主語にする。"),
      ("That restaurant's price is delicious.", "値段がおいしいという意味不明な文になる。"), ("That restaurant is expensive but delicious.", "「値段の割に」は「値段のわりに質がよい」という意味で、高いとは言っていない。")]),
    ("雨が降ろうが降るまいが、試合は行われる。", "The game will be held whether it rains or not.",
     [("If it rains or not, the game will be held.", "「～であろうとなかろうと」という譲歩の副詞節には if は使えず、whether を使う。"),
      ("Whether it will rain or not, the game will be held.", "時・条件・譲歩を表す副詞節では、未来のことも現在形で表す（whether it rains）。"),
      ("The game will be held unless it rains.", "unless は「雨が降らない限り」で、雨なら中止という逆の意味になる。")]),
    ("彼女は手が離せない。", "She is too busy to do anything else right now.",
     [("Her hands cannot be separated.", "慣用句の直訳で、手が離れないという意味になる。「忙しくてほかのことができない」と言いかえる。"),
      ("She cannot leave her hand.", "直訳で、英語として意味をなさない。"), ("She has nothing to do right now.", "「手が離せない（忙しい）」と逆の意味である。")]),
    ("日本人は議論が苦手だと言われる。", "It is often said that Japanese people are not good at debating.",
     [("Japanese is said to be weak in discussion.", "Japanese 単独では「日本語」の意味になる。「日本人」は Japanese people。"),
      ("People say Japanese people are good at debating.", "「苦手だ」と逆の意味になっている。"), ("Japanese people are said bad debate.", "be said to be ～ の形になっておらず、bad debate も語法として誤り。")]),
    ("その映画は期待外れだった。", "The movie was not as good as I had expected.",
     [("The movie was outside of my expectation.", "「外れ」を outside と直訳しており、英語では意味が伝わらない。「期待したほどよくなかった」と言いかえる。"),
      ("The movie was better than I had expected.", "「期待以上」で、逆の意味になっている。"), ("I didn't expect to see the movie.", "見るつもりがなかったという意味になり、映画の評価を述べていない。")]),
]

# 文法・語法：(正しい文, [(誤りの文, 理由)])
GRAMMAR = [
    ("I have lived in this town since I was ten.",
     [("I live in this town since I was ten.", "「10歳のときから（今まで）」という継続は現在完了で表す。"),
      ("I have lived in this town for I was ten.", "for の後ろには期間を表す語句がくる。節をとるのは since。"), ("I lived in this town since I was ten.", "since とともに使う継続の内容は、過去形ではなく現在完了にする。")]),
    ("Each of the students has a laptop.",
     [("Each of the students have a laptop.", "each は単数扱いなので、動詞は has。"),
      ("Each students has a laptop.", "each の直後の名詞は単数形（each student）。"), ("Every of the students has a laptop.", "every は of を続けて使えない。each of を使う。")]),
    ("I'll call you when I get home.",
     [("I'll call you when I will get home.", "時を表す副詞節では、未来のことも現在形で表す。"),
      ("I'll call you when I got home.", "未来の出来事なので過去形は使えない。"), ("I call you when I will get home.", "主節は未来を表す will が必要で、when 節は現在形にする。")]),
    ("She gave me some good advice.",
     [("She gave me a good advice.", "advice は不可算名詞なので a をつけない。"),
      ("She gave me some good advices.", "advice は不可算名詞なので複数形にしない。"), ("She gave me many good advice.", "不可算名詞には many ではなく much / a lot of を使う。")]),
    ("The number of foreign visitors has increased.",
     [("The number of foreign visitors have increased.", "主語の中心は the number（数）で単数なので、has を使う。"),
      ("A number of foreign visitor has increased.", "a number of ～ は「多くの～」で、後ろは複数名詞・複数扱いになる。"), ("The number of foreign visitors has been increased.", "increase（増える）は自動詞として使い、受け身にしない。")]),
    ("I am looking forward to seeing you.",
     [("I am looking forward to see you.", "look forward to の to は前置詞なので、後ろは動名詞にする。"),
      ("I am looking forward seeing you.", "look forward to の to が抜けている。"), ("I look forward to see you.", "to は前置詞なので、後ろは動名詞（seeing）にする。")]),
    ("It is important for young people to read newspapers.",
     [("It is important that young people to read newspapers.", "that 節の中には主語と動詞が必要で、to 不定詞は置けない。"),
      ("It is important for young people reading newspapers.", "形式主語 it に対応する真主語は to 不定詞（to read）にする。"), ("Young people are important to read newspapers.", "important は人を主語にして「～するのが大切だ」の意味では使えない。")]),
    ("Most Japanese people use trains every day.",
     [("Most of Japanese people use trains every day.", "most of の後ろには the / my などで限定された名詞がくる。"),
      ("Almost Japanese people use trains every day.", "almost は副詞なので、名詞を直接修飾できない（almost all Japanese people なら可）。"),
      ("The most Japanese people use trains every day.", "「大部分の」の意味では the をつけない。the most は最上級になる。")]),
    ("I was surprised at the news.",
     [("I was surprising at the news.", "人が驚くときは過去分詞 surprised を使う。surprising は「（物事が）驚くべき」。"),
      ("I surprised at the news.", "surprise は「驚かせる」という他動詞なので、「驚く」は be surprised。"), ("The news was surprised me.", "be 動詞と過去形の動詞を並べることはできない。The news surprised me. が正しい。")]),
    ("Smartphones enable us to get information easily.",
     [("Smartphones enable us getting information easily.", "enable O to do の形で、動名詞は使わない。"),
      ("Smartphones enable that we get information easily.", "enable は that 節を目的語にとらない。"), ("Smartphones enable to us get information easily.", "enable O to do の語順になっていない。")]),
    ("There are fewer cars on this street than before.",
     [("There are less cars on this street than before.", "cars は可算名詞の複数形なので、less ではなく fewer を使う。"),
      ("There is fewer cars on this street than before.", "主語 cars は複数なので There are にする。"), ("There are fewer car on this street than before.", "fewer の後ろの可算名詞は複数形（cars）にする。")]),
    ("If I had studied harder, I could have passed the exam.",
     [("If I studied harder, I could have passed the exam.", "過去の事実に反する仮定は、if 節を過去完了（had studied）にする。"),
      ("If I had studied harder, I could pass the exam yesterday.", "yesterday（過去）の結果なので could have passed にする。"), ("If I would have studied harder, I could have passed the exam.", "if 節には would have を使わず、過去完了を使う。")]),
]

# 構文の空所：(日本語, 英文, 正答, [(誤り, 理由)])
EXPR = [
    ("科学が発達すればするほど、私たちの生活は便利になる。", "(　　) science develops, the more convenient our lives become.", "The more",
     [("More", "the 比較級, the 比較級 の形で、前半にも the が必要である。"), ("As more", "as を使うなら As science develops, our lives become more convenient. の形になり、後半の the more と合わない。"),
      ("The most", "最上級ではなく比較級を使う構文である。")]),
    ("彼女は私の2倍の本を持っている。", "She has (　　) books as I do.", "twice as many",
     [("twice as much", "books は可算名詞なので many を使う。"), ("two times many", "倍数表現は「倍数＋as many as」の形にする。"), ("twice more as", "twice more は as と組み合わせられない。")]),
    ("その問題は難しすぎて、私には解けなかった。", "The problem was (　　) for me to solve.", "too difficult",
     [("so difficult", "so … that の形でなければ「難しすぎて～できない」を表せない。"), ("very difficult", "very では「～できない」という否定の結果を表せない。"),
      ("difficult enough", "difficult enough for me to solve は「解けるほど難しい」の意味で、逆になる。")]),
    ("若者が政治に関心をもつことが大切だ。", "It is important (　　) young people to take an interest in politics.", "for",
     [("of", "It is ～ of 人 to do は kind / careless など人の性質を表す形容詞に使う。important には for。"), ("that", "that を使うなら that young people take an interest … と主語＋動詞が続く。"),
      ("to", "to young people to take … では不定詞の意味上の主語を表せない。")]),
    ("彼が来るかどうかわからない。", "I don't know (　　) he will come.", "whether",
     [("that", "that では「彼が来ることを知らない」となり、「～かどうか」の意味にならない。"), ("what", "what の後ろは要素の欠けた節になるが、he will come は完全な文である。"),
      ("unless", "unless は「～しない限り」で、know の目的語になる名詞節をつくらない。")]),
    ("インターネットのおかげで、海外の友人と簡単に連絡が取れる。", "The Internet (　　) us to keep in touch with friends abroad easily.", "allows",
     [("makes", "make O 原形の形で、to は使わない。"), ("lets", "let O 原形の形で、to は使わない。"), ("has", "have O 原形の形で、to は使わない。また「～させる」の意味になり、日本語と合わない。")]),
    ("宿題を終えるのに3時間かかった。", "It (　　) me three hours to finish my homework.", "took",
     [("spent", "spend は人を主語にして I spent three hours finishing … の形で使う。"), ("needed", "It needed me three hours という形はない。"),
      ("made", "make には「（時間が）かかる」の意味がない。")]),
    ("もし私があなたなら、その申し出を受けるだろう。", "If I (　　) you, I would accept the offer.", "were",
     [("am", "現在の事実に反する仮定は仮定法過去で表す。"), ("will be", "if 節に will は使わない。また仮定法過去が必要である。"),
      ("had been", "had been は過去の事実に反する仮定（仮定法過去完了）で、主節の would accept と合わない。")]),
    ("彼女は医者になるために一生懸命勉強している。", "She is studying hard (　　) become a doctor.", "in order to",
     [("so that", "so that の後ろには主語と動詞が必要である（so that she can become …）。"), ("for", "for の後ろに動詞の原形は置けない。"),
      ("in order that", "in order that の後ろには主語と動詞が必要である。")]),
    ("私たちは環境を守るためにできることをすべきだ。", "We should do (　　) we can to protect the environment.", "what",
     [("that", "that には先行詞が必要だが、ここには先行詞がない。"), ("which", "which にも先行詞が必要である。"), ("how", "how では「どのようにできるか」になり、do の目的語として意味が通らない。")]),
    ("健康ほど大切なものはない。", "(　　) is more important than health.", "Nothing",
     [("Anything", "Anything is more important than health. は「何でも健康より大切だ」となり、逆の意味になる。"), ("Something", "「健康より大切なものがある」という意味になり、逆である。"),
      ("None of them", "them が指すものがなく、意味が通らない。")]),
    ("その知らせを聞いて、彼はうれしくて飛び上がった。", "The news made him so happy (　　) he jumped for joy.", "that",
     [("as", "so … as は否定文で「～ほど…ない」を表す形で、結果を表せない。"), ("which", "結果を表す so … that の that が必要である。"),
      ("because", "because では so と組み合わさらず、因果の向きも逆になる。")]),
]

# 意見文の点検：(テーマ, [(文, 役割)], 不適切な文の番号, 理由)
ESSAYS = [
    ("制服の必要性", [("I believe that high schools should keep school uniforms.", "主張"), ("First, uniforms save students time in the morning because they do not have to choose what to wear.", "理由1"),
                  ("Second, uniforms help families save money on clothes.", "理由2"), ("My favorite color is blue, so I like blue uniforms.", ""),
                  ("For these reasons, I think uniforms are a good idea.", "結論")], 3, "個人の好み（好きな色）を述べているだけで、制服を残すべき理由になっていない。"),
    ("オンライン授業", [("I do not think online classes should replace classes at school.", "主張"), ("In the classroom, students can ask questions and get answers immediately.", "理由1"),
                   ("Also, talking with classmates face to face helps us learn from each other.", "理由2"), ("Online classes are better because students can study anywhere.", ""),
                   ("Therefore, classes at school are still necessary.", "結論")], 3, "オンライン授業のほうがよいという、冒頭の主張と矛盾する内容である。"),
    ("都会での生活", [("I would rather live in a big city than in the countryside.", "主張"), ("There are many kinds of jobs in a big city.", "理由1"),
                 ("For example, my grandparents live in a small village.", ""), ("In addition, public transportation is convenient, so people do not need a car.", "理由2"),
                 ("For these reasons, city life is more attractive to me.", "結論")], 2, "For example で始まっているが、直前の理由（都会には仕事が多い）の具体例になっていない。"),
    ("ボランティアの必修化", [("I do not think volunteer work should be required for high school students.", "主張"), ("Volunteer work should come from people's own wish to help others.", "理由1"),
                     ("If it is required, students may do it only to get credit.", "理由2"), ("Volunteer work is a wonderful experience that every student must have.", ""),
                     ("For these reasons, it should be a choice, not a requirement.", "結論")], 3, "「すべての生徒が経験すべきだ」という内容は、必修に反対する主張と矛盾する。"),
    ("紙の本と電子書籍", [("I prefer paper books to e-books.", "主張"), ("For me, it is easier to remember what I read on paper.", "理由1"),
                    ("Also, paper books do not need batteries.", "理由2"), ("E-books are cheaper, so I buy all my books as e-books.", ""),
                    ("For these reasons, I will keep reading paper books.", "結論")], 3, "すべて電子書籍で買うという内容は、紙の本のほうが好きだという主張と矛盾する。"),
    ("部活動の意義", [("Club activities are important for high school students.", "主張"), ("Through club activities, students learn to work as a team.", "理由"),
                 ("For example, in my basketball team, we always discuss how to improve together.", "具体例"), ("Basketball is played in many countries around the world.", ""),
                 ("Therefore, I believe every student should try a club activity.", "結論")], 3, "バスケットボールについての一般的な事実で、部活動が大切だという主張を支えていない。"),
    ("早期の英語教育", [("I think children should start learning English in elementary school.", "主張"), ("Young children are not afraid of making mistakes when they speak.", "理由1"),
                   ("Also, starting early gives them more time to practice.", "理由2"), ("However, English is not necessary for most people, so children should not study it.", ""),
                   ("For these reasons, English lessons in elementary school are a good idea.", "結論")], 3, "英語を学ぶべきではないという結論を含み、冒頭の主張と矛盾する。However で反対意見を認める場合も、自分の主張に戻る必要がある。"),
    ("キャッシュレス決済", [("I think more stores in Japan should accept cashless payment.", "主張"), ("Paying by card or smartphone is usually faster than paying in cash.", "理由1"),
                     ("In addition, people do not have to carry a lot of coins.", "理由2"), ("I went to a convenience store yesterday.", ""),
                     ("For these reasons, cashless payment should become more common.", "結論")], 3, "昨日コンビニに行ったという出来事を述べるだけで、主張や理由とのつながりがない。"),
]
ROLE_WHY = {"主張": "冒頭で立場を明確に述べる文", "理由1": "主張を支える1つ目の理由", "理由2": "主張を支える2つ目の理由", "理由": "主張を支える理由",
            "具体例": "直前の理由を支える具体例", "結論": "主張をまとめ直す結論"}

# 語の選択：(日本語, 英文, 正答, [(誤り, 理由)])
WORDS = [
    ("その店でかさを借りた。", "I (　　) an umbrella from the shop.", "borrowed",
     [("lent", "lend は「貸す」。from the shop と合わない。"), ("borrow", "過去の出来事なので過去形にする。"), ("was borrowed", "受け身では「私が借りられた」になってしまう。")]),
    ("彼女は先生にその問題を説明してもらった。", "The teacher (　　) the problem to her.", "explained",
     [("explained her", "explain は人を直接目的語にとらない（explain A to 人）。"), ("told", "tell the problem to her は「問題を伝えた」で、「説明する」の意味にならない。"),
      ("said", "say は「説明する」の意味で物事を目的語にとらない。")]),
    ("空港行きのバスの運賃はいくらですか。", "What is the bus (　　) to the airport?", "fare",
     [("fee", "fee は入場料・授業料・専門家への謝礼などの料金で、乗り物の運賃は fare。"), ("salary", "salary は「給料」。"), ("tip", "tip は「心付け（チップ）」。")]),
    ("この10年で、その町の人口は増えた。", "The population of the town has (　　) over the past ten years.", "increased",
     [("raised", "raise は「～を上げる」という他動詞で、目的語が必要である。"), ("increasing", "has の後ろは過去分詞（has increased）にする。"),
      ("been increased", "increase（増える）は自動詞として使い、受け身にしない。")]),
    ("彼は燃費のよい車を買った。", "He bought an (　　) car that uses little gas.", "economical",
     [("economic", "economic は「経済の・経済学の」。「節約になる」は economical。"), ("economics", "economics は「経済学」という名詞。"),
      ("economically", "economically は副詞で、名詞 car を修飾できない。")]),
    ("私は彼女にその知らせを伝えた。", "I (　　) her the news.", "told",
     [("said", "say は人を目的語にとらない（say to 人）。"), ("talked", "talk は自動詞で、人と物の2つの目的語をとらない。"), ("spoke", "speak は人と物の2つの目的語をとらない。")]),
    ("明日晴れるといいな。", "I (　　) it will be sunny tomorrow.", "hope",
     [("wish", "wish は実現しそうにない願望に使い、後ろは仮定法（I wish it were …）になる。"), ("want", "want は that 節を目的語にとらない。"),
      ("expect", "expect は「予想する」で、願望ではない。")]),
    ("この部屋は昨年より家具が少ない。", "There is (　　) furniture in this room than last year.", "less",
     [("fewer", "fewer は可算名詞の複数形に使う。furniture は不可算名詞。"), ("few", "few は可算名詞に使い、比較の than と合わない。"),
      ("little", "原級 little は than と組み合わせられない。")]),
    ("彼女は私が今まで会った中で最も親切な人だ。", "She is the kindest person I have (　　) met.", "ever",
     [("never", "never では「一度も会ったことのない人の中で最も親切」となり、意味が通らない。"), ("already", "already は完了を表し、「今までに」の経験の意味にならない。"),
      ("yet", "yet は否定文・疑問文で使う。")]),
    ("その映画はとても面白かったので、2回見た。", "The movie was (　　) interesting that I watched it twice.", "so",
     [("such", "such は名詞を伴う（such an interesting movie that …）。"), ("very", "very では後ろの that と組み合わせて結果を表せない。"),
      ("too", "too … that という形はない。")]),
    ("多くの人がその計画に反対した。", "Many people (　　) the plan.", "opposed",
     [("objected", "object は自動詞で、object to the plan の形にする。"), ("were opposed", "be opposed to the plan の形にする必要がある。"),
      ("against", "against は前置詞で、動詞の位置に置けない。")]),
    ("彼は駅に到着した。", "He (　　) the station.", "reached",
     [("arrived", "arrive は自動詞で、arrive at the station の形にする。"), ("got", "get to the station の形にする必要がある。"), ("came", "come to the station の形にする必要がある。")]),
]

# ======================================================================
# B・C・D 用のデータ
# ======================================================================

# 和文英訳（短文）：(日本語, 模範解答, [別解], 構文のポイント)
TRANS = [
    ("その国を訪れて初めて、私はその文化の豊かさに気づいた。", "It was not until I visited the country that I realized how rich its culture was.",
     ["Only after I visited the country did I realize how rich its culture was.", "I did not realize how rich the culture of the country was until I visited it."], "「～して初めて」＝It was not until … that ～、間接疑問 how rich ～ was"),
    ("年をとるにつれて、時間がたつのが速く感じられるようになる。", "As we grow older, time seems to pass more quickly.",
     ["The older we get, the faster time seems to pass."], "比例の as「～するにつれて」、seem to do"),
    ("彼女がどれほど努力したかは、結果を見ればわかる。", "You can tell how hard she worked by looking at the results.",
     ["The results show how hard she worked."], "間接疑問 how hard ～、無生物主語での言いかえ"),
    ("どんなに忙しくても、毎日少しは本を読むようにしている。", "No matter how busy I am, I try to read a little every day.",
     ["However busy I am, I try to read a little every day."], "No matter how / However＋形容詞＋S V「どんなに～でも」、try to do"),
    ("電車が遅れたせいで、私は会議に間に合わなかった。", "Because the train was delayed, I was late for the meeting.",
     ["The delay of the train made me late for the meeting.", "I couldn't get to the meeting on time because the train was delayed."], "理由の because 節、be late for ～／無生物主語 make O C"),
    ("自分の意見を英語で表現するのは、思っていたより難しかった。", "Expressing my opinions in English was more difficult than I had expected.",
     ["It was harder than I had expected to express my opinions in English."], "動名詞の主語／形式主語、比較 than I had expected"),
    ("この写真を見ると、子どものころを思い出す。", "This picture reminds me of my childhood.",
     ["When I look at this picture, I remember my childhood."], "無生物主語 remind 人 of ～"),
    ("睡眠不足は集中力の低下につながる。", "Lack of sleep leads to poor concentration.",
     ["If you do not get enough sleep, you cannot concentrate well."], "lead to ～「～につながる」。和文和訳で「眠らないと集中できない」と言いかえてもよい"),
    ("外国を旅行するときは、その国の習慣を尊重することが大切だ。", "When you travel abroad, it is important to respect the customs of the country you visit.",
     ["It is important to respect local customs when you travel abroad."], "形式主語 it … to do、総称の you"),
    ("宿題をしていれば、先生にしかられなかっただろうに。", "If I had done my homework, I would not have been scolded by my teacher.",
     ["If I had done my homework, my teacher would not have scolded me."], "仮定法過去完了"),
    ("インターネットのおかげで、私たちは世界中の人々と簡単に交流できる。", "The Internet allows us to communicate easily with people all over the world.",
     ["Thanks to the Internet, we can easily communicate with people around the world."], "無生物主語 allow O to do／thanks to ～"),
    ("必要なのはお金ではなく、時間だ。", "What we need is not money but time.",
     ["It is not money but time that we need."], "関係代名詞 what／not A but B／強調構文"),
    ("彼は、まるで何も起こらなかったかのように話し続けた。", "He kept talking as if nothing had happened.",
     ["He went on talking as though nothing had happened."], "as if＋仮定法過去完了、keep doing"),
    ("その問題について、もっと多くの人が考えるべきだ。", "More people should think about the problem.",
     ["More people need to think about the issue."], "「もっと多くの人が」を主語 More people にする"),
]

# 並べかえ：(日本語, [正しい順の語句], 完成文, ポイント)
ORDERS = [
    ("その本を読んで初めて、私は問題の深刻さに気づいた。", ["it was not until", "I read the book", "that", "I realized", "how serious", "the problem was"],
     "It was not until I read the book that I realized how serious the problem was.", "It was not until … that ～、間接疑問"),
    ("人は年をとればとるほど、変化を受け入れるのが難しくなる。", ["the older", "people get", "the harder", "it is", "for them", "to accept change"],
     "The older people get, the harder it is for them to accept change.", "the 比較級, the 比較級、形式主語"),
    ("大切なのは、何を言うかではなく、どう言うかだ。", ["what matters", "is", "not", "what you say", "but", "how you say it"],
     "What matters is not what you say but how you say it.", "関係代名詞 what、not A but B"),
    ("スマートフォンのおかげで、私たちはどこにいても働けるようになった。", ["smartphones", "have made it", "possible", "for us", "to work", "wherever we are"],
     "Smartphones have made it possible for us to work wherever we are.", "make it possible for 人 to do（形式目的語）"),
    ("もしあのとき彼の助言に従っていたら、今ごろもっと幸せだろう。", ["if I had", "followed his advice", "then,", "I would be", "happier", "now"],
     "If I had followed his advice then, I would be happier now.", "混合仮定法（if 節は過去完了、主節は would＋原形）"),
    ("どれほど努力しても、すぐに結果が出るとは限らない。", ["no matter", "how hard", "you try,", "you will not", "always", "see results immediately"],
     "No matter how hard you try, you will not always see results immediately.", "No matter how ～、部分否定 not always"),
    ("外国語を学ぶことで、私たちは自国の文化をよりよく理解できる。", ["learning", "a foreign language", "helps us", "understand", "our own culture", "better"],
     "Learning a foreign language helps us understand our own culture better.", "動名詞の主語、help O 原形"),
    ("その知らせを聞いて、彼女はうれしくて言葉が出なかった。", ["the news", "made her", "so happy", "that", "she could not", "say a word"],
     "The news made her so happy that she could not say a word.", "無生物主語 make O C、so … that"),
    ("私がその町を訪れたのは、10年ぶりだった。", ["it was", "the first time", "in ten years", "that", "I had visited", "the town"],
     "It was the first time in ten years that I had visited the town.", "the first time in ～ years「～年ぶり」"),
    ("環境問題は、一国だけで解決できるものではない。", ["environmental problems", "are not", "something", "that", "one country", "can solve alone"],
     "Environmental problems are not something that one country can solve alone.", "関係代名詞 that、something の後置修飾"),
    ("彼が言ったことは、私が予想していたこととまったく違っていた。", ["what he said", "was", "completely different", "from", "what", "I had expected"],
     "What he said was completely different from what I had expected.", "関係代名詞 what、be different from ～"),
    ("その問題を解決するのに何が必要かを考えることが大切だ。", ["it is", "important", "to think about", "what", "is needed", "to solve the problem"],
     "It is important to think about what is needed to solve the problem.", "形式主語、疑問詞 what の間接疑問"),
]

# 意見文の空所：(テーマ, 本文, 正答, [(誤り, 理由)])
GAPS = [
    ("高校生のアルバイト", "I think high school students should be allowed to have part-time jobs. (　　) For example, working at a shop teaches them how to talk politely with customers. For this reason, part-time jobs can be a valuable experience.",
     "First, they can learn social skills that they cannot learn at school.",
     [("However, studying is the most important thing for students.", "However で主張と反対の内容を述べており、直後の For example（主張を支える例）とつながらない。"),
      ("My friend works at a convenience store.", "個人的な事実で理由になっておらず、直後の For example が何の例かわからなくなる。"),
      ("In conclusion, part-time jobs are popular.", "結論の表現で、理由と例が続く位置には合わない。人気があることは主張の理由にもならない。")]),
    ("動物園の役割", "Some people say that zoos are cruel to animals. (　　) Many zoos today protect animals that are in danger of disappearing from the wild. Therefore, I believe zoos still play an important role.",
     "However, I think zoos are necessary.",
     [("For example, lions sleep most of the day.", "ライオンの習性の話で、反対意見への反論にも主張にもなっていない。"), ("In addition, animals in zoos are often unhappy.", "反対意見に同調する内容で、後ろの結論（動物園は重要だ）と矛盾する。"),
      ("As a result, zoos should be closed.", "後ろの Therefore 以下の結論と逆の内容である。")]),
    ("在宅勤務", "Working from home has both advantages and disadvantages. On the one hand, workers do not have to spend time commuting. (　　) For example, some people feel lonely because they rarely talk with their coworkers.",
     "On the other hand, it can be difficult to communicate with others.",
     [("In addition, workers can save money on transportation.", "利点の追加で、直後の例（孤独を感じる）と合わない。On the one hand に対応する On the other hand が必要。"), ("For these reasons, everyone should work from home.", "まとめの表現で、直後に例が続く位置に合わない。"),
      ("As a result, commuting takes a long time.", "在宅勤務の欠点を述べる流れになっていない。")]),
    ("給食と弁当", "I prefer school lunch to bringing a lunch box from home. First, school lunch is well balanced, so it is good for our health. (　　) Parents do not have to get up early to make lunch every morning.",
     "Second, it saves our families time.",
     [("For example, I like curry and rice.", "個人の好みで、直後の説明（親が早起きしなくてよい）と合わない。"), ("However, lunch boxes are more delicious.", "主張と反対の内容で、直後の文が給食の利点の説明になっていることと合わない。"),
      ("In conclusion, school lunch is better.", "結論の後ろに理由の説明が続くことになり、構成が崩れる。")]),
    ("歴史を学ぶ意味", "Some students think history is useless because it is about the past. (　　) By learning how people solved problems in the past, we can find ideas for solving problems today. That is why I believe history is worth studying.",
     "However, I believe history can help us understand the present.",
     [("In fact, history is a boring subject.", "反対意見に同調しており、後ろの結論（歴史は学ぶ価値がある）と矛盾する。"), ("For example, I learned many dates in history class.", "年号を覚えたことは、歴史が現在に役立つという流れを支えていない。"),
      ("As a result, many students do not study history.", "後ろの内容（歴史から今の問題を解く手がかりを得る）とつながらない。")]),
    ("公共交通機関の利用", "I think more people should use public transportation instead of cars. First, buses and trains produce less carbon dioxide per person than cars. Second, they can reduce traffic jams in cities. (　　)",
     "For these reasons, using public transportation is better for both the environment and our cities.",
     [("However, cars are more comfortable than buses.", "主張と反対の内容で文章が終わってしまい、結論がなくなる。"), ("For example, I take the train to school.", "理由2の後ろに個人の例を置いても、文章のまとめにならない。"),
      ("Third, I want to buy a new car someday.", "Third で理由を加える形だが、内容が主張と矛盾している。")]),
    ("電子書籍と紙の本", "Some people believe that e-books will completely replace paper books. (　　) Many readers still enjoy the feel of paper and find it easier to concentrate on a printed page. Therefore, paper books will not disappear.",
     "However, I do not think this will happen.",
     [("In fact, e-books are becoming more popular.", "直後の文は「紙の本はなくならない」根拠なので、反対の立場を示す文が必要である。"), ("For example, I read e-books every day.", "電子書籍を毎日読む例は、紙の本がなくならないという結論を支えない。"),
      ("As a result, bookstores are closing.", "後ろの結論（紙の本はなくならない）と逆の方向の内容である。")]),
    ("留学の価値", "I believe studying abroad is a valuable experience for young people. (　　) Living in a foreign country, they have to use another language every day and solve problems by themselves. Through such experiences, they become more independent and confident.",
     "This is because it helps them grow as people.",
     [("However, studying abroad is expensive.", "反対の要素を述べたまま、後ろの文で利点の説明に戻っており、流れが不自然である。"), ("For example, my sister likes traveling.", "旅行が好きだという例は、留学の価値の説明にならない。"),
      ("In conclusion, studying abroad is valuable.", "結論の後ろに理由の説明が続くことになり、構成が崩れる。")]),
]

# 和文英訳（長め）：(日本語, 模範解答, [別解], 和文和訳のポイント, 採点基準)
LONG = [
    ("人は失って初めて、当たり前だと思っていたものの価値に気づくものだ。健康もその一つである。",
     "It is not until we lose something that we realize the value of what we have taken for granted. Health is one example.",
     ["We do not realize the value of what we have taken for granted until we lose it. Health is one such thing."],
     "「失って初めて気づく」→「失うまで気づかない」と言いかえてもよい。「当たり前だと思う」は take ～ for granted。",
     [("「失って初めて」を It is not until … that ～ / not … until などで表している", 2), ("「当たり前だと思っていたもの」を what we have taken for granted などで表している", 2), ("「価値に気づく」を realize the value of ～ で表している", 2), ("2文目を正しく続け、時制・数・冠詞に誤りがない", 2)]),
    ("言葉は時代とともに変わるものだ。若者の言葉づかいを嘆く大人も、若いころは同じように批判されていたのかもしれない。",
     "Languages change over time. Adults who complain about the way young people speak may have been criticized in the same way when they were young.",
     ["Language changes with the times. The adults who criticize how young people talk might have been criticized in the same way when they were young."],
     "「言葉づかいを嘆く」→「若者の話し方に不満を言う」と言いかえる。「～されていたのかもしれない」は過去の推量 may have been＋過去分詞。",
     [("「言葉は時代とともに変わる」を Languages change over time などで表している", 2), ("「～を嘆く大人」を関係代名詞の節で表している", 2), ("「批判されていたのかもしれない」を may have been＋過去分詞で表している", 3), ("時制・数・冠詞に誤りがない", 1)]),
    ("旅の楽しみは、目的地に着くことだけではない。途中で思いがけない人や場所に出会うことにもある。",
     "The pleasure of traveling lies not only in reaching your destination but also in coming across people and places you did not expect along the way.",
     ["Traveling is enjoyable not only because you reach your destination but also because you meet unexpected people and see unexpected places on the way."],
     "2文を「A だけでなく B にもある」の1文にまとめると、not only A but also B が使える。「～にある」は lie in ～。",
     [("「楽しみは～にある」を lie in ～ などで表している", 2), ("not only A but also B などで「～だけでなく…にも」を表している", 3), ("「思いがけない人や場所に出会う」を自然な英語で表している", 2), ("文法・語法に誤りがない", 1)]),
    ("私たちが毎日捨てている食べ物の量を知ったら、多くの人は驚くだろう。まずは、必要以上に買わないことから始めてはどうだろうか。",
     "Many people would be surprised if they knew how much food we throw away every day. Why don't we start by not buying more than we need?",
     ["If people knew the amount of food we throw away each day, many of them would be surprised. How about starting by not buying too much?"],
     "「知ったら驚くだろう」は実際には知らない前提なので仮定法過去が自然。「量」は how much food ～ の間接疑問で表せる。",
     [("「～を知ったら驚くだろう」を仮定法（would … if … knew）で表している", 2), ("「食べ物の量」を how much food ～ / the amount of food ～ で表している", 3), ("「必要以上に買わないことから始める」を start by not buying more than we need などで表している", 2), ("文法・語法に誤りがない", 1)]),
    ("科学技術がいくら進歩しても、人と人とが直接会って話すことの大切さは変わらないだろう。",
     "No matter how much technology advances, the importance of meeting and talking with people face to face will not change.",
     ["However much technology develops, meeting and talking with people in person will always be important."],
     "「いくら～しても」は No matter how much / However much。「直接会って話すこと」は動名詞＋face to face / in person。",
     [("「いくら～しても」を No matter how much / However much で表している", 3), ("「直接会って話すことの大切さ」を the importance of ～ing face to face などで表している", 3), ("will not change など、未来の推量を表している", 1), ("文法・語法に誤りがない", 1)]),
    ("自分の意見をはっきり述べることは、相手を尊重しないことではない。むしろ、相手を対等な存在として扱っていることの表れである。",
     "Stating your opinion clearly does not mean that you do not respect the other person. Rather, it shows that you treat him or her as an equal.",
     ["Expressing your opinion clearly is not a sign of disrespect. On the contrary, it shows that you see the other person as your equal."],
     "「～することは…ではない」は does not mean that ～ で表すと自然。「むしろ」は Rather / On the contrary。",
     [("「～することは…ではない」を does not mean that ～ などで表している", 2), ("「相手を尊重する」を respect the other person などで表している", 2), ("「むしろ」を Rather などで表し、前文とのつながりを示している", 2), ("「対等な存在として扱う」を treat … as an equal などで表している", 2)]),
    ("この町に引っ越してきて5年になるが、いまだに近所の人の名前をほとんど知らない。",
     "It has been five years since I moved to this town, but I still hardly know the names of my neighbors.",
     ["Five years have passed since I moved to this town, but I still know very few of my neighbors' names."],
     "「～して5年になる」は It has been five years since ～。「ほとんど知らない」は hardly know / know very few。",
     [("「引っ越してきて5年になる」を It has been five years since ～ などで表している", 3), ("「いまだに」を still で表している", 1), ("「ほとんど知らない」を hardly know / know very few などで表している", 2), ("文法・語法（時制・冠詞）に誤りがない", 2)]),
    ("失敗を恐れて何もしないよりは、挑戦して失敗するほうがずっとよい。",
     "It is much better to try and fail than to do nothing because you are afraid of failing.",
     ["Trying and failing is far better than doing nothing for fear of failure."],
     "「A するより B するほうがよい」は It is better to B than to A。比較級の強調は much / far。",
     [("「～するほうが…よりずっとよい」を It is much better to A than to B などで表している", 3), ("「失敗を恐れて」を because you are afraid of failing / for fear of failure で表している", 3), ("文法・語法に誤りがない", 2)]),
]

# 自由英作文：(テーマ, 模範解答)
TOPICS = [
    ("「大学の授業はすべてオンラインで行うべきだ」という意見",
     "I disagree with the idea that all university classes should be held online. It is true that online classes save time because students do not have to travel to campus. However, a university is not only a place to receive knowledge but also a place to exchange ideas. In a classroom, students can discuss questions with professors and classmates and learn from different points of view. For these reasons, I believe that classes on campus should remain an important part of university life."),
    ("「小学生に自分専用のスマートフォンを持たせるべきか」",
     "I do not think elementary school children should have their own smartphones. First, smartphones can easily take away time for playing outside and sleeping, which are important for children's growth. Second, young children are not yet able to protect themselves from dangers on the Internet. Of course, parents may want to contact their children in an emergency, but a simple phone without Internet access is enough for that purpose. Therefore, children should wait until they are older."),
    ("「人生において、お金と時間のどちらがより大切か」",
     "I think time is more important than money. Money can be earned again if we lose it, but time that has passed never comes back. For example, my grandfather often says that he regrets not spending more time with his family when he was busy working. Of course, we need a certain amount of money to live, but having more money does not always make us happier. Therefore, I want to use my time carefully for the people I love."),
    ("「AI が翻訳をしてくれる時代に、外国語を学ぶ必要はあるか」",
     "I believe we still need to learn foreign languages even though AI can translate for us. Translation tools are useful, but they cannot fully replace the experience of talking directly with people from other cultures. When we learn a language, we also learn how its speakers think and what they value. In addition, being able to speak without a device helps us build trust with others more quickly. For these reasons, learning foreign languages will remain important."),
    ("「将来住むなら、都会と地方のどちらがよいか」",
     "In the future, I would like to live in the countryside rather than in a big city. First, the countryside is quieter and has more nature, so I could relax after work and enjoy outdoor activities such as hiking. Second, housing is usually cheaper there, so I could live in a larger house. Some people may worry that life in the countryside is inconvenient, but online shopping and remote work have made it much easier. For these reasons, I would choose the countryside."),
    ("「生徒を試験の点数だけで評価すべきか」",
     "I do not think students should be judged only by their test scores. Tests can measure how much knowledge students have, but they cannot show other important abilities such as creativity, teamwork, and leadership. For example, a student who is not good at tests may be excellent at organizing school events. If schools focus only on scores, such students may lose confidence in themselves. Therefore, schools should evaluate students in various ways, including their projects and activities."),
]
ESSAY_RUBRIC = [("立場を冒頭で明確に述べている", 2), ("理由を2つ程度、具体例や説明を伴って述べている", 3), ("構成（主張→理由→結論）とつなぎの表現が適切である", 1), ("文法・語法が正しく、指定の語数を満たしている", 2)]

# 和文英訳の誤答：(日本語, 誤答, 正答, 誤りの箇所, 理由, 種類)
TERR = [
    ("私は昨日、図書館で本を3冊借りた。", "I borrowed three book at the library yesterday.", "I borrowed three books at the library yesterday.", "three book", "book は可算名詞なので、three の後ろは複数形 books にする。", "notation"),
    ("彼女は3年前からピアノを習っている。", "She learns the piano since three years ago.", "She has been learning the piano for three years.", "learns … since three years ago", "過去から現在まで続いていることは現在完了（進行形）で表す。また since three years ago とは言わず、for three years とする。", "concept"),
    ("明日雨が降ったら、試合は中止になるだろう。", "If it will rain tomorrow, the game will be canceled.", "If it rains tomorrow, the game will be canceled.", "If it will rain", "条件を表す副詞節では、未来のことも現在形で表す。", "concept"),
    ("その知らせを聞いて、私はとても興奮した。", "I was very exciting to hear the news.", "I was very excited to hear the news.", "exciting", "人が「興奮する」ときは過去分詞 excited を使う。exciting は「（物事が）わくわくさせる」。", "concept"),
    ("日本では多くの人が電車で通勤している。", "In Japan, many people commute by a train.", "In Japan, many people commute by train.", "by a train", "交通手段を表す by の後ろの名詞には冠詞をつけない。", "notation"),
    ("私の兄は医者になった。", "My brother became doctor.", "My brother became a doctor.", "became doctor", "doctor は可算名詞の単数なので、冠詞 a が必要である。", "notation"),
    ("彼は私に、いつ帰ってくるのかとたずねた。", "He asked me when would I come back.", "He asked me when I would come back.", "when would I come back", "間接疑問では疑問詞の後ろを主語＋動詞の語順にする。", "concept"),
    ("私の意見では、若者はもっと新聞を読むべきだ。", "In my opinion, young people should read newspaper more.", "In my opinion, young people should read newspapers more.", "read newspaper", "newspaper は可算名詞なので、一般論では複数形 newspapers にする。", "notation"),
    ("その問題は難しすぎて、私には解けなかった。", "The problem was too difficult for me to solve it.", "The problem was too difficult for me to solve.", "to solve it", "too … to do の文では、主語 The problem が solve の目的語にあたるので、it を重ねて置かない。", "concept"),
    ("夏休みに、私はたくさんの宿題をしなければならなかった。", "I had to do many homeworks during summer vacation.", "I had to do a lot of homework during summer vacation.", "many homeworks", "homework は不可算名詞なので複数形にせず、many ではなく a lot of / much を使う。", "notation"),
    ("その話を聞いて、彼は青ざめた。", "His face became blue when he heard the story.", "He turned pale when he heard the story.", "His face became blue", "「青ざめる」を色の名前のまま直訳している。英語では pale（青白い）を使い、turn pale などと表す。", "interpretation"),
    ("私の趣味は写真を撮ることだ。", "My hobby is take pictures.", "My hobby is taking pictures.", "is take pictures", "be 動詞の補語に動詞の原形は置けない。動名詞 taking か不定詞 to take にする。", "concept"),
    ("彼女は先週から病気で寝ている。", "She is sick in bed since last week.", "She has been sick in bed since last week.", "is sick … since last week", "since とともに過去から現在まで続く状態を表すときは、現在完了にする。", "concept"),
    ("私の家は駅から歩いて10分です。", "My house is 10 minutes walk from the station.", "My house is a ten-minute walk from the station.", "10 minutes walk", "「歩いて10分」は a ten-minute walk（または ten minutes' walk）とする。名詞の前に置くときは minute を単数形にしてハイフンでつなぐ。", "notation"),
]
TTEMPT = {
    "notation": "日本語には名詞の単数・複数や冠詞の区別がないので、英語でも数や冠詞を意識せずに書いてしまったため。",
    "concept": "日本語の語順や時制の感覚のまま、英語の構文・時制のきまりを確かめずに書いたため。",
    "interpretation": "日本語の表現を1語ずつ英語に置きかえ、英語として意味が通るかを確かめなかったため。",
}

# 意見文の誤答：(テーマ, 誤答, 問題点, 種類, 書き直し例)
EERR = [
    ("高校生はアルバイトをすべきか",
     "I think high school students should have part-time jobs. Students can earn money and learn about work. However, working too much can make students tired and hurt their grades. So high school students should not work.",
     "冒頭の主張（アルバイトをすべきだ）と結論（すべきではない）が矛盾している。譲歩（However 以下）の内容に引きずられて、結論が逆になっている。", "logic",
     "I think high school students should be allowed to have part-time jobs. Students can earn money and learn about work. It is true that working too much can make students tired and hurt their grades. However, if they work only a few hours a week, they can learn the value of money without hurting their studies. Therefore, I think part-time jobs are good for high school students."),
    ("将来、都会に住みたいか",
     "I want to live in a big city. There are many stores and hospitals. My uncle lives in Osaka. For these reasons, I want to live in a big city.",
     "My uncle lives in Osaka. は理由も具体例も支えておらず、論理のつながりがない。また理由が1つだけで説明が足りないのに For these reasons と複数の理由をまとめている。", "logic",
     "I want to live in a big city. First, there are many stores and hospitals, so daily life is convenient. For example, my uncle in Osaka can go to a hospital within ten minutes on foot. Second, there are more kinds of jobs in a big city. For these reasons, I want to live in a big city."),
    ("英語を学ぶことは大切か",
     "Learning English is important. Because we can talk with people from other countries. For example, many tourists come to Japan.",
     "Because ～ だけで文を終えており、主節のない不完全な文（断片）になっている。また例が理由とどうつながるかが説明されていない。", "concept",
     "Learning English is important because it allows us to talk with people from other countries. For example, many tourists now visit Japan, and if we can speak English, we can help them and learn about their cultures."),
    ("制服は必要か",
     "I think school uniforms are good. First, students don't have to choose clothes every morning. Second, uniforms show which school students belong to, so they behave well outside school. In conclusion, uniforms are good, and they are also cheaper than buying many clothes.",
     "結論の段落で、本論で述べていない新しい理由（服を買うより安い）を加えている。結論は主張のまとめにとどめる。", "logic",
     "I think school uniforms are good. First, students don't have to choose clothes every morning. Second, uniforms show which school students belong to, so they behave well outside school. Third, uniforms can be cheaper than buying many clothes. In conclusion, uniforms are good for both students and their families."),
    ("インターネットは危険か",
     "Some people say that the Internet is dangerous. I agree with them. The Internet is very useful because we can find information quickly. Therefore, the Internet is dangerous.",
     "理由（すぐに情報が見つかって便利だ）が、主張（インターネットは危険だ）を支えておらず、むしろ逆の方向の内容である。", "logic",
     "Some people say that the Internet is dangerous. I agree with them. On the Internet, false information spreads quickly, and it is often hard to tell whether something is true. Therefore, we should be careful when we use the Internet."),
    ("友人に勧めたい本（理由を2つ挙げること）",
     "The book I recommend is a novel about a girl who travels around the world. It is very interesting. It is not boring at all. So you should read it.",
     "「理由を2つ挙げる」という条件に対し、interesting と not boring at all は同じ内容の言いかえで、実質的に理由が1つしかない。具体性もない。", "condition",
     "The book I recommend is a novel about a girl who travels around the world. First, the story is exciting because she meets many people and solves problems with them. Second, it teaches readers about the cultures of different countries. So you should read it."),
    ("学校へのスマートフォン持ち込み",
     "Students should be allowed to bring smartphones to school. In my opinion, smartphones are bad for students' eyes. They can also contact their parents in an emergency. So smartphones should be allowed.",
     "1つ目の理由（目に悪い）が、持ち込みを認めるべきだという主張と逆の方向の内容で、主張を支えていない。", "logic",
     "Students should be allowed to bring smartphones to school. First, they can contact their parents in an emergency, such as an earthquake. Second, they can use them to look up information during lessons when the teacher allows it. So smartphones should be allowed."),
    ("宿題は必要か",
     "Homework should be abolished. All students hate homework, and no student learns anything from it. So schools should stop giving homework.",
     "All students / no student と根拠なく言い切っており、言いすぎ（過度の一般化）である。採点者に反例を思い浮かべられ、説得力を失う。", "logic",
     "I think schools should give less homework. Many students are busy with club activities, and too much homework can leave them little time to rest. In addition, students learn more when they have time to review what they really need. So schools should reduce the amount of homework."),
]

# ======================================================================
# 架空の資料（数値の比較）
# ======================================================================

DATA_TOPICS = [
    ("Midori 町を訪れた外国人旅行者数", "the number of foreign tourists who visited Midori Town", "人",
     {"up": ("the town has become well known through social media", "Photos of its old streets and local food posted online may have made many people want to visit."),
      "down": ("traveling has become more expensive", "When transportation and hotels cost more, people may choose to travel less often.")}),
    ("ある高校で自転車通学をしている生徒数", "the number of students who come to a high school by bicycle", "人",
     {"up": ("more students have become interested in their health and the environment", "Riding a bicycle is good exercise, and it does not produce carbon dioxide."),
      "down": ("a new bus route to the school may have been opened", "If students can take a bus easily, fewer of them may choose to ride a bicycle, especially on rainy days.")}),
    ("ある市立図書館の年間貸出冊数", "the number of books borrowed from a city library in a year", "冊",
     {"up": ("the library has started events such as reading sessions for children", "Such events may have brought in families who did not use the library before."),
      "down": ("more people now read news and stories on their smartphones", "They may no longer feel the need to borrow printed books.")}),
    ("ある商店街の1日あたりの来客数", "the number of visitors to a shopping street per day", "人",
     {"up": ("the street has started holding monthly markets", "These events may attract people who usually shop at large malls."),
      "down": ("a large shopping mall may have opened nearby", "Many people may prefer a mall where they can buy everything in one place.")}),
]
YEARS = [(2005, 2015), (2010, 2020), (2014, 2024), (2000, 2020), (2012, 2022)]
BASES = [200, 300, 400, 500, 600, 800, 1200, 1500, 2000, 2400]
MULT = {2: "twice", 3: "three times", 4: "four times"}


def dec(x):
    f = Fraction(x).limit_denominator(1000)
    return str(f.numerator) if f.denominator == 1 else f"{float(f):g}"


def make_data(r):
    jp, en, unit, reasons = r.choice(DATA_TOPICS)
    y1, y2 = r.choice(YEARS)
    kind = r.choice(["times", "up", "down"])
    while True:
        a = r.choice(BASES)
        if kind == "times":
            k = r.choice([2, 3, 4])
            b, p = a * k, None
        elif kind == "up":
            p = r.choice([20, 25, 30, 40, 60])
            k = None
            b = a * (100 + p) // 100
            if a * (100 + p) % 100:
                continue
        else:
            p = r.choice([20, 25, 30, 40, 60, 75])
            k = None
            b = a * (100 - p) // 100
            if a * (100 - p) % 100:
                continue
        break
    return dict(jp=jp, en=en, unit=unit, reasons=reasons, y1=y1, y2=y2, kind=kind, a=a, b=b, k=k, p=p)


def data_line(d):
    return f"［架空の資料］{d['jp']}：{d['y1']}年 {d['a']:,}{d['unit']}、{d['y2']}年 {d['b']:,}{d['unit']}"


def data_chk(d):
    if d["kind"] == "times":
        return (f"Rational({d['b']},{d['a']})", str(d["k"]), None, "intermediate")
    if d["kind"] == "up":
        return (f"({d['b']}-{d['a']})*100/{d['a']}", str(d["p"]), None, "intermediate")
    return (f"({d['a']}-{d['b']})*100/{d['a']}", str(d["p"]), None, "intermediate")


def data_calc(d):
    a, b = d["a"], d["b"]
    if d["kind"] == "times":
        return f"{b:,}÷{a:,}＝{d['k']}（倍）"
    if d["kind"] == "up":
        return f"（{b:,}－{a:,}）÷{a:,}×100＝{d['p']}（%の増加）"
    return f"（{a:,}－{b:,}）÷{a:,}×100＝{d['p']}（%の減少）"


# ======================================================================
# 授業プリント
# ======================================================================

EXL = LONG[6]
EXT = TOPICS[3]

LESSON = lesson(
    goals=["和文英訳で、日本語を英語にしやすい日本語に言いかえ（和文和訳）、構文を決めてから、時制・数・冠詞まで正確な英文を書ける。",
           "自由英作文で、主張→理由（2つ）→結論の構成と語数配分を守り、論理の飛躍や矛盾のない意見文を書ける。",
           "架空の資料の数値を、倍数・増減の割合の表現で正確に英語にし、原因を1つ挙げて説明できる。"],
    duration=50,
    readiness=["和文和訳の手順と意見文の基本構成を知っている（HS-ENG-U10）。",
               "現在完了・過去完了、時・条件の副詞節の時制のきまりを使える（HS-ENG-U02）。",
               "倍数表現（twice as many as）・仮定法（If I had ～, I would have ～）を書ける（HS-ENG-U07・U08）。"],
    flow=[("導入：減点される答案、点が残る答案", 5, "同じ内容の2つの英作文答案を比べ、採点が「減点法」で行われることを示す"),
          ("和文英訳の手順", 15, "和文和訳 → 構文の決定 → 時制・数・冠詞の点検の3段階を例題1で実演する"),
          ("自由英作文の型", 15, "主張・理由・結論の構成と語数配分を確認し、例題2の答案を分析する"),
          ("資料の説明", 10, "倍数と増減の割合の表し方を例題3で練習する"),
          ("まとめと確認", 5, "確認問題3問、自己点検リストの使い方と問題プリントの取り組み方の指示")],
    sections=[
        intro("in1", "二次試験の英作文は「減点されない英文」を書く試験",
              "国公立大学の二次試験や私立大学の個別試験の英作文には、日本語の文を英語に直す和文英訳と、与えられたテーマについて自分の意見を書く自由英作文がある。どちらも多くの場合、文法・語法の誤りを1つずつ減点する方法で採点される。難しい単語や凝った構文を使って誤るよりも、自分が確実に使える表現で正確に書くほうが得点は高い。また自由英作文では、内容の一貫性（主張と理由・結論が食い違っていないか）と、問いの条件（語数・理由の数・立場の明示）を満たしているかが厳しく見られる。",
              bullets=["和文英訳：日本語の表面ではなく意味を訳す。直訳できない表現は、英語にしやすい日本語に言いかえる。",
                       "自由英作文：主張→理由→結論の型を守り、条件（語数・理由の数）を必ず満たす。",
                       "どちらも最後に「時制・数・冠詞・主語と動詞の一致」を点検する時間を残す。"],
              points=[tp("難しい語を使って文法を誤った答案と、平易な語で正確に書いた答案を並べ、どちらが減点が少ないかを考えさせる。",
                         ask="同じ内容を書くなら、知らない難しい語に挑戦するのと、知っている語で言いかえるのとでは、どちらが安全か。",
                         expect="知っている語で言いかえるほう。誤りは1つずつ減点されるので、確実に書ける表現を選ぶ。", timing="導入の冒頭"),
                      tp("試験時間のうち英作文にかける時間の目安（和文英訳1問8〜10分、自由英作文20分程度）と、見直しの時間を必ず残すことを伝える。",
                         caution="書きながら考えて構成が崩れ、結論が主張と食い違う答案が多い。")]),
        definition("df1", "和文和訳と、減点されやすい誤り",
                   "和文和訳とは、英語に直しにくい日本語（慣用句・省略・あいまいな主語）を、意味を変えずに英語にしやすい日本語へ言いかえることである。そのうえで、日本語にはない英語の文法上の区別（数・冠詞・時制）を補って書く。",
                   bullets=["慣用句は意味に直す：「顔が広い」→「知り合いが多い」→ He knows a lot of people.",
                            "主語を補う・決め直す：「この写真を見ると思い出す」→「この写真が私に思い出させる」→ This picture reminds me of ～.",
                            "数と冠詞：可算名詞の単数には a / the が必要。advice・homework・information・furniture は不可算名詞。",
                            "時制：「～から…している」は現在完了。時・条件の副詞節（when / if）では未来のことも現在形。",
                            "語法：explain A to 人、arrive at / reach、enable O to do、look forward to ～ing など、動詞ごとの形を守る。"],
                   conditions=["言いかえは意味を変えない範囲で行う。「期待外れ」を「期待以上」にするなど、逆の意味にならないよう訳し戻して確かめる。",
                               "自信のない構文は使わない。同じ内容を確実に書ける別の構文（No matter how ↔ However、It is not until ↔ not … until）を持っておく。"],
                   points=[tp("慣用句を含む日本語を3つ板書し、生徒に「小学生にもわかる日本語」に言いかえさせてから英訳させる。",
                              ask="「胸がいっぱいになる」を小学生にわかる日本語にすると？", expect="「とても感動する」→ be deeply moved"),
                           tp("不可算名詞と時制の誤りは、どの大学の採点でも確実に減点されることを強調する。",
                              caution="内容に気をとられて、many homeworks や since three years ago のような基本的な誤りを書く答案が多い。")]),
        theorem("th1", "自由英作文の構成と語数配分（100語の場合）",
                "主張（1文・約15語）→ 理由1＋説明・具体例（約30語）→ 理由2＋説明・具体例（約30語）→ 結論（1〜2文・約20語）",
                ["主張は第1文で、賛成・反対や選んだ立場をはっきり書く（I agree / I do not think / I would rather ～）。",
                 "理由は First, / Second, / In addition, などで示し、それぞれに説明か具体例を1文以上つける。",
                 "反対意見に触れるときは It is true that ～, but … / Of course ～, but … の形で認めてから自分の主張に戻る。",
                 "結論では主張を言いかえてまとめ、新しい理由を加えない。"],
                body="採点者は「主張が明確か」「理由が主張を支えているか」「結論が主張と一致しているか」を確認する。型を守れば、内容の一貫性は自然に保たれる。語数は指定の±10%程度に収める。",
                points=[tp("模範答案を4色で色分け（主張・理由・具体例・結論）させ、語数を数えさせる。",
                           ask="結論に新しい理由を書くと、どんな問題があるか。", expect="本論で説明されていない理由になり、主張のまとめでなくなる。構成が崩れる。")]),
        derivation("dv1", "和文英訳の3段階（なぜこの順に処理するのか）",
                   ["① 和文和訳：日本語の慣用句・省略・あいまいな主語を、意味を変えずに英語にしやすい日本語へ直す（「その国を訪れて初めて気づいた」→「その国を訪れるまで気づかなかった」）。",
                    "② 構文の決定：文の骨組み（主語・動詞）と、使う構文（It is not until … that ～、the 比較級, the 比較級、仮定法など）を決める。複数の書き方がある場合は、自分が最も確実に書けるものを選ぶ。",
                    "③ 点検：時制・数（単数・複数）・冠詞・主語と動詞の一致・語法（動詞の後ろの形）を1つずつ確かめる。最後に英文を日本語に訳し戻して、意味がずれていないかを確かめる。",
                    "この順に処理するのは、①を飛ばすと直訳による意味不明な英文になり、②を飛ばすと文の途中で構文が崩れ、③を飛ばすと減点の対象になる基本的な誤りが残るからである。とくに③は日本語にない区別なので、意識して点検しないと必ず見落とす。"],
                   body="和文英訳の答案の失点は「直訳」「構文の崩れ」「基本的な文法の誤り」の3つに集中する。3段階の手順は、この3つをそれぞれ防ぐためのものである。",
                   points=[tp("③の点検を、時制→数→冠詞→一致→語法の順にチェックリストとして答案の余白に書かせる。",
                              ask="この英文で、日本語にはない区別のために確認すべき箇所はどこか。", expect="名詞の単数・複数、冠詞、動詞の時制。", timing="例題1の解説時")]),
        example("ex1", "例題1　和文英訳（和文和訳と時制）",
                f"次の日本語を英語に訳しなさい。\n「{EXL[0]}」",
                ["① 和文和訳：「引っ越してきて5年になる」→「この町に引っ越して以来5年がたった」。「ほとんど知らない」→「ほんの少ししか知らない」。",
                 "② 構文：It has been five years since ～（現在完了）、but、still、hardly know。",
                 "③ 点検：since の後ろは過去形 moved、主節は has been（現在完了）。neighbors は複数形。"],
                EXL[1],
                thinking="「～して5年になる」は「～して以来5年がたつ」と言いかえると、It has been ～ since … の構文が使える。",
                points=[tp("Five years have passed since ～ も正解になることを示し、自分が確実に書ける構文を選べばよいと伝える。",
                           ask="I live in this town for five years. はなぜ誤りか。", expect="過去から現在まで続く状態は現在完了で表す。")],
                misconceptions=[("「5年になる」を現在形 is five years で書く。", "It has been five years since ～ のように現在完了で表す")]),
        example("ex2", "例題2　自由英作文（構成の分析）",
                f"テーマ：{EXT[0]}について、あなたの考えを70〜90語の英語で書きなさい。",
                ["主張（第1文）：I believe we still need to learn foreign languages even though AI can translate for us.",
                 "理由1：翻訳ツールは、異文化の人と直接話す経験を完全には置きかえられない。言語を学ぶと、その話し手の考え方や価値観も学べる。",
                 "理由2（In addition）：機器なしで話せると、より早く信頼関係を築ける。",
                 "結論（For these reasons）：主張を言いかえてまとめる。新しい理由は加えない。"],
                EXT[1],
                thinking="まず日本語で「主張・理由2つ・結論」のメモを作り、理由が主張を支えているか、2つの理由が同じ内容の言いかえになっていないかを確かめてから英語で書く。",
                points=[tp("模範答案の語数を数えさせ、各部分の語数配分を確認する。", ask="理由1と理由2は別の内容になっているか。",
                           expect="理由1は異文化理解、理由2は信頼関係で、別の観点になっている。")]),
        example("ex3", "例題3　資料の説明（倍数と増減の割合）",
                "［架空の資料］ある市立図書館の年間貸出冊数：2010年 1,200冊、2020年 3,600冊\nこの変化を英語1文で説明しなさい。",
                ["3,600÷1,200＝3 なので、2020年は2010年の3倍。",
                 "倍数表現：X times as large as ～／increase threefold。",
                 "増加率で表すなら（3,600－1,200）÷1,200×100＝200%の増加。300%の増加ではない。"],
                "The number of books borrowed from the library in 2020 was three times as large as that in 2010.",
                thinking="「3倍になった」と「200%増えた」は同じことを表す。increased by 300 percent と書くと誤りになる。",
                points=[tp("「3倍」と「300%増」を混同した答案を示し、増加率の計算式を確認する。", ask="3倍になったとき、増加率は何%か。", expect="200%。（3－1）×100。")]),
        board("bd1", "板書案",
              [("① 和文英訳の3段階", ["和文和訳（慣用句・主語）", "構文を決める（確実に書ける形）", "点検：時制・数・冠詞・一致・語法", "訳し戻して意味を確認"]),
               ("② 自由英作文の型", ["主張（第1文で立場）", "理由1＋説明・例", "理由2＋説明・例（別の観点）", "結論＝主張の言いかえ", "新しい理由は書かない"]),
               ("③ 資料の説明", ["X times as large as ～", "increased by p percent", "3倍＝200%の増加", "decreased by p percent", "原因は may / possible で控えめに"])],
              points=[tp("③の数値の言い表し方は、例題3の数値を残し、倍数と増加率の対応を矢印で示す。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("和文英訳では、いきなり英語を書かせず、余白に和文和訳の日本語を書かせる。言いかえた日本語が元の意味とずれていないかを隣の生徒と確認させる。"),
               tp("自由英作文は、書く前に日本語のメモ（主張・理由2つ・結論）を1分で作らせる。メモがない答案は構成が崩れやすい。", timing="問題プリント C の前"),
               tp("答案の見直しでは、時制・数・冠詞・一致の4項目に印をつけさせる。", ask="あなたの答案で、名詞に下線を引くと、冠詞や複数形が抜けているものはあるか。",
                  expect="a / the が抜けている単数の可算名詞、複数形にすべき名詞が見つかる。"),
               tp("譲歩（It is true that ～, but …）を使うときは、but の後ろで必ず自分の主張に戻るよう指導する。", caution="譲歩した内容に引きずられて、結論が主張と逆になる答案が多い。"),
               tp("資料の説明では、計算した倍数・割合を余白に書かせ、twice / three times / by ～ percent の対応を確かめさせる。")],
              misconceptions=[("難しい単語や構文を使うほど点が高い。", "誤りは1つずつ減点される。確実に書ける表現で正確に書くほうが得点は高い"),
                              ("自由英作文の結論で新しい理由を加えると説得力が増す。", "結論は主張のまとめ。新しい理由は本論で説明する"),
                              ("3倍になったことは increased by 300 percent と表せる。", "3倍は200%の増加。増加率＝（新－旧）÷旧×100")]),
        summary("sm1", "まとめ",
                ["和文英訳は「和文和訳 → 構文の決定 → 時制・数・冠詞・一致・語法の点検」の順に処理する。",
                 "自由英作文は主張→理由（別の観点で2つ）→結論の型と語数配分を守り、結論で主張と食い違わないようにする。",
                 "資料の数値は倍数（X times as large as）と増減の割合（by p percent）を区別し、原因は控えめな表現で述べる。"]),
        check("ck1", "確認問題",
              [("「彼は顔が広い」を英訳するとき、まずどのような日本語に言いかえるか。", "「彼は知り合いが多い」→ He knows a lot of people."),
               ("自由英作文の結論の段落で、してはいけないことは何か。", "本論で述べていない新しい理由を加えること（主張と食い違う結論を書くこと）"),
               ("1,500人が4,500人になった変化を、増加率で表すと何%の増加か。", "200%の増加（4,500÷1,500＝3倍）")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

@gen("basic_check", 4, ["concept", "common_error"])
def a_rephrase(r):
    jp, ok, wrongs = r.choice(REPHRASE)
    return mc(f"次の日本語の内容を最も適切に表している英文を選びなさい。\n「{jp}」", [ok] + [w for w, _ in wrongs],
              f"{ok}　日本語の慣用句や言い回しは、意味を平易な日本語に言いかえて（和文和訳して）から英語にする。", d=2,
              ap="日本語の表現を1語ずつ英語に置きかえず、「つまりどういう意味か」を平易な日本語に言いかえてから選ぶ。",
              steps=["日本語の慣用句・言い回しを見つける。", "その意味を平易な日本語に言いかえる。", "言いかえた日本語と同じ意味の英文を選ぶ。", f"答え：{ok}"],
              alt=["選んだ英文を日本語に訳し戻し、元の日本語と同じ意味になるかを確かめる。"],
              pc=[("言い回しの意味をとらえている", 1), ("適切な英文を選んでいる", 1)],
              pit=["慣用句を文字どおりに英語に置きかえた選択肢を選ぶ。"], why={w: (why, "直訳による意味のずれ") for w, why in wrongs})


@gen("basic_check", 4, ["computation", "common_error"])
def a_grammar(r):
    ok, wrongs = r.choice(GRAMMAR)
    return mc("次の英文のうち、文法・語法的に正しいものを1つ選びなさい。", [ok] + [w for w, _ in wrongs],
              f"{ok}　英作文の答案で減点されやすい時制・数・一致・語法の誤りを点検する。", d=2,
              ap="4つの文の違う箇所に注目し、時制・名詞の数・主語と動詞の一致・動詞の語法のどのきまりに関わるかを考える。",
              steps=["4つの文を比べ、異なっている箇所に印をつける。", "その箇所が関わる文法のきまり（時制・数・一致・語法）を思い出す。", "きまりに合わない文を消していく。", f"答え：{ok}"],
              alt=["正しいと判断した文について、なぜ正しいのかをきまりの言葉（例：時の副詞節は現在形）で説明できるかを確かめる。"],
              pc=[("文法のきまりを特定している", 1), ("正しい文を選んでいる", 1)],
              pit=["日本語に訳して意味が通れば正しいと判断し、形のきまりを確かめない。"], why={w: (why, "文法・語法のきまりの見落とし") for w, why in wrongs})


@gen("basic_check", 4, ["computation", "condition_check"])
def a_construction(r):
    jp, en, ok, wrongs = r.choice(EXPR)
    return mc(f"日本語に合うように、（　）に入る最も適切なものを選びなさい。\n{jp}\n{en}", [ok] + [w for w, _ in wrongs],
              f"{ok}。完成文：{en.replace('(　　)', ok)}", d=2,
              ap="日本語の中の構文の手がかり（～すればするほど、～倍、～すぎて…ない、～かどうか など）を見つけ、対応する英語の形を思い出す。",
              steps=["日本語の構文の手がかりを見つける。", "対応する英語の構文の形を思い出す。", "空所の前後の語（the / as / to / that など）と形が合うものを選ぶ。", f"答え：{ok}"],
              alt=["選んだ語句を入れた英文を日本語に訳し戻し、元の日本語と一致するかを確かめる。"],
              pc=[("構文の手がかりに気づいている", 1), ("正しい語句を選んでいる", 1)],
              pit=["空所の前後の語との形のつながりを確かめずに選ぶ。"], why={w: (why, "構文の形の取り違え") for w, why in wrongs})


@gen("basic_check", 4, ["condition_check", "concept"])
def a_essay_check(r):
    theme, sents, bad, reason = r.choice(ESSAYS)
    text = "\n".join(f"({i + 1}) {s}" for i, (s, _) in enumerate(sents))
    bad_s = sents[bad][0]
    others = [(s, role) for i, (s, role) in enumerate(sents) if i != bad]
    return mc(f"次の意見文（テーマ：{theme}）の中で、論理の流れから見て不適切な文を1つ選びなさい。\n{text}", [bad_s] + [s for s, _ in others],
              f"{bad_s}　{reason}", d=2,
              ap="まず第1文の主張を確認し、各文がその主張を支えているか（理由・具体例・結論）、矛盾していないかを1文ずつ確かめる。",
              steps=["第1文の主張（立場）を確認する。", "各文の役割（理由・具体例・結論）を書きこむ。", "主張を支えていない文、主張と矛盾する文を探す。", f"不適切な文：{bad_s}"],
              alt=["不適切と判断した文を取り除いて読み直し、文章の論理が通るかどうかで確かめる。"],
              pc=[("主張と各文の関係を確かめている", 1), ("不適切な文を選んでいる", 1)],
              pit=["英語として正しい文なら論理的にも適切だと考える。"],
              why={s: (f"{ROLE_WHY[role]}として、論理の流れに合っている。", "文の役割の見落とし") for s, role in others})


@gen("basic_check", 4, ["computation", "concept"])
def a_word(r):
    jp, en, ok, wrongs = r.choice(WORDS)
    return mc(f"日本語に合うように、（　）に入る最も適切な語句を選びなさい。\n{jp}\n{en}", [ok] + [w for w, _ in wrongs],
              f"{ok}。完成文：{en.replace('(　　)', ok)}", d=2,
              ap="空所の後ろの形（目的語を直接とるか、前置詞が必要か、名詞は可算か不可算か）と、語の意味の違いを確かめる。",
              steps=["空所の後ろの形を確認する（目的語・前置詞・名詞の種類）。", "選択肢の語の意味と語法の違いを思い出す。", f"両方に合う語：{ok}"],
              alt=["選んだ語で英文を音読し、辞書の例文で見たことのある形かを確かめる。"],
              pc=[("語法・意味の違いに注目している", 1), ("正しい語句を選んでいる", 1)],
              pit=["日本語の訳語だけで選び、動詞の後ろの形（前置詞の有無）を確かめない。"], why={w: (why, "語法・語の意味の区別の誤り") for w, why in wrongs})


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 5, ["computation", "application"])
def b_translate(r):
    jp, ans, alts, pt = r.choice(TRANS)
    hint = r.random() < 0.5
    stem = f"次の日本語を英語に訳しなさい。\n「{jp}」" + (f"\n（ヒント：{pt.split('、')[0]}）" if hint else "")
    return desc(stem, ans, f"ポイント：{pt}。別解：{' / '.join(alts)}",
                [("文の骨組み（主語・動詞）が正しい", 1), ("ポイントとなる構文・表現を正しく使っている", 2), ("時制・数・冠詞などに誤りがない", 1)], d=3, p=4, lines=3, v=alts,
                ap="和文和訳をして主語と動詞を決め、日本語の言い回しに対応する構文を選んでから書く。",
                steps=["英語にしやすい日本語に言いかえ、主語と動詞を決める。", f"使う構文・表現を決める：{pt}。", "時制・数・冠詞・語法を点検する。", f"解答例：{ans}"],
                alt=[f"別の書き方：{alts[0]}　自分が最も確実に書ける構文を選べばよい。"],
                pc=[("骨組み", 1), ("構文・表現", 2), ("時制・数・冠詞", 1)],
                pit=["日本語の語順のまま単語を並べる。", "名詞の数や冠詞を点検しない。"])


@gen("standard_practice", 5, ["computation", "condition_check"])
def b_order(r):
    jp, parts, full, pt = r.choice(ORDERS)
    return order(f"日本語に合うように、語句を並べかえて英文を完成させなさい（文頭の語も小文字で示してある）。\n{jp}", parts,
                 f"{full}　ポイント：{pt}。", d=3, p=4,
                 ap="まず文全体の骨組み（主語＋動詞）と、使われている構文（強調構文・比較・形式主語など）を見抜き、その形に語句をはめこむ。",
                 steps=[f"構文を見抜く：{pt}。", "主語と動詞を決める。", "構文の形に合わせて残りの語句を並べる。", f"完成文：{full}"],
                 alt=["完成した英文を和訳し直して、日本語と一致するかを確かめる。"],
                 pc=[("構文と骨組みを正しく組み立てている", 2), ("語順がすべて正しい", 2)],
                 pit=["日本語の語順のまま並べる。", "構文の決まった語順（the 比較級 S V, the 比較級 S V など）を崩す。"])


@gen("standard_practice", 5, ["computation", "condition_check"])
def b_data(r):
    d = make_data(r)
    S = cap(d["en"])
    a, b, y1, y2 = d["a"], d["b"], d["y1"], d["y2"]
    if d["kind"] == "times":
        k = d["k"]
        ok = f"{S} in {y2} was {MULT[k]} as large as that in {y1}."
        other = 3 if k == 2 else 2
        wr = [(f"{S} in {y2} was {MULT[other]} as large as that in {y1}.", f"{b:,}÷{a:,}＝{k} なので、{y2}年は{y1}年の{k}倍である。", "倍数の計算の誤り"),
              (f"{S} increased by {k * 100} percent from {y1} to {y2}.", f"{k}倍になったときの増加率は（{b:,}－{a:,}）÷{a:,}×100＝{(k - 1) * 100}%であり、{k * 100}%ではない。", "倍数と増加率の混同"),
              (f"{S} in {y1} was {MULT[k]} as large as that in {y2}.", "比べる年の向きが逆である。大きいのは後の年である。", "比較の向きの取り違え")]
    elif d["kind"] == "up":
        p = d["p"]
        ok = f"{S} increased by {p} percent from {y1} to {y2}."
        wr = [(f"{S} increased by {100 + p} percent from {y1} to {y2}.", f"{b:,}÷{a:,}×100＝{100 + p} は{y1}年を100としたときの値で、増加率は{p}%である。", "割合と増加率の混同"),
              (f"{S} decreased by {p} percent from {y1} to {y2}.", "数値は増えているので decreased は誤り。", "増減の向きの取り違え"),
              (f"{S} in {y2} was twice as large as that in {y1}.", f"{b:,}÷{a:,}＝{dec(Fraction(b, a))} 倍で、2倍ではない。", "倍数の計算の誤り")]
    else:
        p = d["p"]
        ok = f"{S} decreased by {p} percent from {y1} to {y2}."
        wr = [(f"{S} decreased by {100 - p} percent from {y1} to {y2}.", f"{b:,}÷{a:,}×100＝{100 - p} は残っている割合で、減少率は{p}%である。", "割合と減少率の混同"),
              (f"{S} increased by {p} percent from {y1} to {y2}.", "数値は減っているので increased は誤り。", "増減の向きの取り違え"),
              (f"{S} in {y2} was half of that in {y1}.", f"{b:,}÷{a:,}＝{dec(Fraction(b, a))} で、半分ではない。", "倍数の計算の誤り")]
    return mc(f"次の資料の内容を正しく表している英文を1つ選びなさい。\n{data_line(d)}", [ok] + [w for w, _, _ in wr],
              f"{ok}　{data_calc(d)}。", d=3,
              ap="英文を読む前に、2つの年の数値から倍数（後÷前）と増減率（（後－前）÷前×100）を計算しておく。",
              steps=["増えたか減ったかを確認する。", f"倍数・増減率を計算する：{data_calc(d)}。", "英文の表現（X times as large as / increased by p percent / decreased by p percent）と照合する。", f"答え：{ok}"],
              alt=[f"{y1}年の数値に倍数・割合をかけて {y2}年の数値（{b:,}）になるかを逆算して確かめる。"],
              pc=[("倍数・増減率を正しく計算している", 2), ("正しい英文を選んでいる", 2)],
              pit=["3倍を「300%の増加」とするなど、倍数と増加率を混同する。"], why={w: (why, mis) for w, why, mis in wr},
              chk=data_chk(d))


@gen("standard_practice", 5, ["concept", "application"])
def b_essay_gap(r):
    theme, text, ok, wrongs = r.choice(GAPS)
    return mc(f"次の意見文（テーマ：{theme}）の（　）に入る最も適切な文を選びなさい。\n{text}", [ok] + [w for w, _ in wrongs],
              f"{ok}　（　）の前後の文の役割（主張・理由・例・結論）と、つなぎの表現が示す論理関係から判断する。", d=3,
              ap="（　）の直前と直後の文の役割を確かめ、その間に入る文の役割（理由・反論・対比・結論）を先に決めてから選ぶ。",
              steps=["第1文の主張（または紹介されている意見）を確認する。", "（　）の直後の文の役割（例・説明・結論）を確認する。",
                     "（　）に必要な文の役割を決め、つなぎの表現と内容が合う選択肢を選ぶ。", f"答え：{ok}"],
              alt=["選んだ文を入れて全体を読み、主張→理由→例→結論の流れが一貫しているかを確かめる。"],
              pc=[("前後の文の役割をとらえている", 2), ("適切な文を選んでいる", 2)],
              pit=["つなぎの表現（However / For example / In conclusion）の意味を確かめずに、内容だけで選ぶ。"], why={w: (why, "論理展開の読み違い") for w, why in wrongs})


# ======================================================================
# C 思考力・記述応用
# ======================================================================

@gen("thinking_writing", 4, ["written_reasoning", "application"])
def c_long_translation(r):
    jp, ans, alts, note, keys = r.choice(LONG)
    show = r.random() < 0.5
    stem = f"次の日本語を英語に訳しなさい。\n「{jp}」"
    if show:
        stem += "\nただし、英語にしにくい部分をどのような日本語に言いかえたか（和文和訳）も簡潔に示すこと。"
        keys = list(keys)
        i = max(range(len(keys)), key=lambda j: keys[j][1])
        keys[i] = (keys[i][0], keys[i][1] - 1)
        keys = [("和文和訳の過程を適切に示している", 1)] + keys
    return desc(stem, (f"（和文和訳）{note}　（英訳）{ans}" if show else ans), f"{note}　別解：{alts[0]}",
                keys, d=4, p=8, lines=5, v=alts,
                ap="直訳しにくい部分（慣用句・あいまいな主語・日本語特有の言い回し）を先に見つけ、英語にしやすい日本語に言いかえてから構文を決める。",
                steps=["英語にしにくい部分に印をつけ、平易な日本語に言いかえる。", "文ごとに主語と動詞、使う構文を決める。", "英文を書き、時制・数・冠詞・一致・語法を点検する。", f"解答例：{ans}"],
                alt=[f"別解：{alts[0]}　構文が違っても、日本語の意味を正確に表し、文法の誤りがなければ得点になる。"],
                pc=list(keys),
                pit=["日本語の語順どおりに単語を置きかえ、英語として意味の通らない文になる。", "2文のつながり（指示語・接続の表現）を落とす。"])


@gen("thinking_writing", 3, ["written_reasoning", "condition_check"])
def c_opinion(r):
    theme, model = r.choice(TOPICS)
    words = r.choice(["80語程度", "70〜90語"])
    concede = r.random() < 0.5
    cond = "反対の立場に一度触れたうえで自分の主張に戻る文（譲歩）を1文含めること。" if concede else "理由を2つ挙げること。"
    rub = list(ESSAY_RUBRIC)
    if concede:
        rub = [("立場を冒頭で明確に述べている", 2), ("理由を具体例や説明を伴って述べている", 2), ("譲歩の文を含め、そのあと自分の主張に戻っている", 2), ("文法・語法が正しく、指定の語数を満たしている", 2)]
    return desc(f"{theme}について、あなたの考えを{words}の英語で書きなさい。{cond}", f"（解答例・{len(model.split())}語）{model}",
                "主張→理由（説明・具体例）→結論の型で書き、結論で主張と食い違わないようにする。語数は指定の±10%程度に収める。",
                rub, d=5, p=8, lines=10,
                ap="書く前に日本語で「主張・理由2つ（別の観点）・結論」のメモを作り、理由が主張を支えているか確かめてから英語にする。",
                steps=["立場を決める（理由が2つ書きやすい立場を選ぶ）。", "理由を2つ、別の観点から考え、それぞれに説明か具体例を加える。",
                       ("反対意見を It is true that ～, but … の形で1文入れ、主張に戻る。" if concede else "First, / Second, で理由を示す。"),
                       "For these reasons などで結論を書き、語数と文法を点検する。"],
                alt=["反対の立場でも答案は書ける。たとえば賛成・反対を入れかえ、同じ型（主張→理由→結論）で書いてみると、どちらの立場が書きやすいかを比べられる。"],
                pc=list(rub),
                pit=["譲歩した内容に引きずられ、結論が主張と逆になる。", "2つの理由が同じ内容の言いかえになっている。", "語数が大きく不足している。"])


@gen("thinking_writing", 3, ["cross_unit", "written_reasoning", "computation"], rel=["HS-ENG-U07", "CT-ENG-U01"])
def c_data_essay(r):
    d = make_data(r)
    S = cap(d["en"])
    a, b, y1, y2 = d["a"], d["b"], d["y1"], d["y2"]
    if d["kind"] == "times":
        trend = f"{S} rose from {a:,} in {y1} to {b:,} in {y2}. In other words, it became {MULT[d['k']]} as large."
        direction = "up"
    elif d["kind"] == "up":
        trend = f"{S} rose from {a:,} in {y1} to {b:,} in {y2}, an increase of {d['p']} percent."
        direction = "up"
    else:
        trend = f"{S} fell from {a:,} in {y1} to {b:,} in {y2}, a decrease of {d['p']} percent."
        direction = "down"
    reason, more = d["reasons"][direction]
    model = f"{trend} One possible reason is that {reason}. {more}"
    return desc(f"次の資料が示す変化を、倍数または増減の割合を用いて英語で説明し、その原因として考えられることを1つ挙げなさい（50〜60語程度）。\n{data_line(d)}",
                f"（解答例）{model}",
                f"数値の計算：{data_calc(d)}。比較・倍数表現（HS-ENG-U07）と、資料から必要な情報を読み取る力（CT-ENG-U01）を組み合わせる。原因は資料からは断定できないので、One possible reason is that ～ / may などの控えめな表現で述べる。",
                [("増減の傾向を正しい比較表現で述べている", 3), ("数値（倍数・割合）を正しく引用している", 2), ("原因として考えられることを1つ、論理的に述べている", 2), ("文法・語法が正しく、語数が適切である", 1)],
                d=4, p=8, lines=6,
                ap=f"まず倍数・増減率を計算し（{data_calc(d)}）、それを英語の表現（X times as large / an increase of p percent）に対応させる。原因は資料に書かれていないので推測として述べる。",
                steps=["増えたか減ったかを確認し、倍数・増減率を計算する。", "変化を1〜2文で述べる（年と数値を正しく引用する）。",
                       "原因として考えられることを One possible reason is that ～ で1つ挙げる。", "原因を補足する文を1文加え、語数と文法を点検する。"],
                alt=["倍数（X times as large）と増減率（increased by p percent）のどちらで書いても、計算が正しければ得点になる。両方の言い方で書けるか確かめておく。"],
                pc=[("傾向と比較表現", 3), ("数値の引用", 2), ("原因の説明", 2), ("文法・語数", 1)],
                pit=["3倍を increased by 300 percent と書く。", "原因を資料からわかる事実のように断定する。"],
                chk=data_chk(d))


# ======================================================================
# D 典型誤答訂正
# ======================================================================

@gen("error_correction", 5, ["common_error", "written_reasoning"])
def d_translation_err(r):
    jp, wrong, right, where, why, typ = r.choice(TERR)
    return desc(f"次の日本語を英語に訳す問題で、ある生徒は次のように答えた。\n「{jp}」\n［ある生徒の解答］\n{wrong}\nこの英文の誤りを指摘し、その理由を説明したうえで、正しい英文に直しなさい。",
                f"誤り：{where}。{why}　正しい英文：{right}",
                "英作文の採点では、時制・数・冠詞・語法の誤りは1つずつ減点される。日本語にない区別ほど意識して点検する。",
                [("誤りの箇所を特定している", 2), ("誤りの理由を文法のきまりに即して説明している", 2), ("正しい英文に直している", 2)], d=3, p=6, lines=4,
                ap="時制・名詞の数・冠詞・主語と動詞の一致・語法（動詞の後ろの形）の順に、生徒の英文を1か所ずつ点検する。",
                steps=["日本語の意味（時・数・状態の継続など）を確認する。", f"生徒の英文を点検し、誤りの箇所を見つける：{where}。", f"理由：{why}", f"正しい英文：{right}"],
                alt=["正しく直した英文を日本語に訳し戻し、元の日本語と意味が一致するかを確かめる。"],
                pc=[("誤りの箇所", 2), ("誤りの理由", 2), ("正しい英文", 2)],
                pit=["誤りの箇所だけを直し、直した結果ほかの部分（主語と動詞の一致など）が崩れていないかを確かめない。"],
                err=dict(sol=wrong, step=where, type=typ, tempt=TTEMPT[typ], fix=right))


@gen("error_correction", 5, ["common_error", "condition_check"])
def d_essay_err(r):
    theme, wrong, why, typ, fix = r.choice(EERR)
    tempt = {"logic": "書きながら考えたため、主張・理由・結論のつながりを最後に確かめなかった。",
             "concept": "日本語の「～だから。」の感覚で、Because 節だけを独立した文として書いてしまった。",
             "condition": "問いの条件（理由の数など）を書く前に確認せず、同じ内容を言いかえて数を満たしたつもりになった。"}[typ]
    return desc(f"テーマ「{theme}」についての意見文として、ある生徒は次のように書いた。\n［ある生徒の解答］\n{wrong}\nこの答案の問題点を指摘し、問題点を解消するように書き直しなさい。",
                f"問題点：{why}　書き直し例：{fix}",
                "自由英作文では、主張・理由・結論が一貫しているか、理由が主張を支えているか、問いの条件を満たしているかが採点される。",
                [("問題点を的確に指摘している", 2), ("問題点を解消した英文に書き直している", 3), ("書き直した英文の文法・語法が正しい", 1)], d=4, p=6, lines=7,
                ap="第1文の主張を確認し、各文が主張を支えているか、結論が主張と一致しているか、問いの条件を満たしているかを順に確かめる。",
                steps=["主張（第1文）を確認する。", "各文の役割（理由・例・結論）を書きこむ。", f"問題点を特定する：{why}", "主張を支える理由・例に差しかえ、結論を主張と一致させて書き直す。"],
                alt=["答案を日本語で「主張・理由・結論」の3行に要約し、つながらない箇所がどこかを確かめる方法もある。"],
                pc=[("問題点の指摘", 2), ("書き直し", 3), ("文法・語法", 1)],
                pit=["文法の誤りだけを探し、論理のつながりの問題に気づかない。"],
                err=dict(sol=wrong, step="主張・理由・結論のつながり", type=typ, tempt=tempt, fix=fix))


GENERATORS = [a_rephrase, a_grammar, a_construction, a_essay_check, a_word,
              b_translate, b_order, b_data, b_essay_gap,
              c_long_translation, c_opinion, c_data_essay,
              d_translation_err, d_essay_err]
