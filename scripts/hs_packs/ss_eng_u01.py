"""単元パック：二次試験対策　英語　和訳・説明問題（下線部和訳・内容説明）。

例文・長文はすべてこのパックのためのオリジナル英文（調査などの具体的な数値は用いていない）。
"""
from banks._common import desc, mc, stim
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem,
                         tp)

UNIT_ID = "SS-ENG-U01"

PREREQUISITES = [
    ("HS-ENG-U09", "パラグラフの構成とディスコースマーカーから、段落の役割と筆者の主張をつかめること"),
    ("HS-ENG-U06", "関係代名詞 what・関係副詞・非制限用法を見分け、修飾関係を正しく取れること"),
    ("HS-ENG-U08", "仮定法過去・過去完了と、if の省略による倒置（Were it not for / Had S p.p.）を読めること"),
    ("HS-ENG-U07", "the 比較級, the 比較級、no more … than、not so much A as B などの比較構文の意味を取れること"),
]
EXTENSIONS = [
    ("SS-ENG-U02", "構文を見抜いて日本語にする力を逆向きに使い、和文英訳・自由英作文で正確な英文を組み立てる"),
    ("SS-JPN-U01", "指示内容を具体化し「～ということ。」でまとめる説明答案の型を、現代文の記述問題にも生かす"),
    ("CT-ENG-U01", "精読で身につけた構文の読み取りを、共通テストの速読（言いかえの照合）で正確さの裏づけとして使う"),
]


# ======================================================================
# 下線部和訳の例文（オリジナル）
#   wrongs: (誤訳, 誤りの理由, 誤りの種類, 誤りの箇所)
# ======================================================================

SENT = [
    dict(key="UNTIL", en="It was not until she moved abroad that she realized how much her hometown meant to her.",
         pt="It is not until A that B「A して初めて B」（強調構文）、how much ～ mean to 人「人にとってどれほど大切か」",
         ok="彼女は海外に引っ越して初めて、故郷が自分にとってどれほど大切なものであったかに気づいた。",
         wrongs=[("彼女は海外に引っ越すまでは、故郷が自分にとってどれほど大切かに気づいていた。", "not until の否定を読み落とし、「～するまで気づいていた」と肯定にしている。「～するまで気づかなかった」＝「～して初めて気づいた」である。", "interpretation", "It was not until … that"),
                 ("彼女が海外に引っ越さなかったのは、故郷が自分にとってとても大切だと気づいたからだ。", "not を moved に結びつけ、強調構文を理由を述べる文と取り違えている。", "concept", "It was not until … that"),
                 ("彼女は海外に引っ越したとき、故郷がどれだけ多くの意味をもつかを理解した。", "「～して初めて」というニュアンスが抜けている。また mean to 人 を「多くの意味をもつ」と直訳し、「人にとって大切だ」という意味を取れていない。", "interpretation", "how much her hometown meant to her")],
         keys=[("It was not until … that ～ を「…して初めて～」と訳している", 2), ("how much her hometown meant to her を「故郷が自分にとってどれほど大切か」と訳している", 1), ("過去の出来事として自然な日本語にしている", 1)]),
    dict(key="SOMUCH", en="What matters is not so much how many books you read as how carefully you think about them.",
         pt="関係代名詞 what の節が主語、not so much A as B「A というよりむしろ B」、how の間接疑問",
         ok="大切なのは、何冊の本を読むかというよりも、むしろそれらについてどれほど注意深く考えるかである。",
         wrongs=[("大切なのは、何冊の本を読むかと同じくらい、それらについてどれほど注意深く考えるかである。", "not so much A as B を as … as の同等比較と取り違えている。", "concept", "not so much A as B"),
                 ("大切なのは、多くの本を読むことであり、それらについて注意深く考えることではない。", "A と B の重みを逆にしている。not so much A as B では B（注意深く考えること）に重点がある。", "interpretation", "not so much A as B"),
                 ("何冊の本を読むかは問題ではなく、それらをどれほど注意深く選ぶかが問題である。", "think about them を「選ぶ」と言いかえており、原文にない内容になっている。", "interpretation", "how carefully you think about them")],
         keys=[("What matters を「大切なのは」と主語として訳している", 1), ("not so much A as B を「A というよりむしろ B」と訳している", 2), ("how many / how carefully の間接疑問を「何冊～か」「どれほど～か」と訳している", 1)]),
    dict(key="WALK", en="A few minutes' walk brought us to a small lake surrounded by tall trees.",
         pt="無生物主語＋bring O to 場所「（主語）によって O は～に着く」、過去分詞の後置修飾",
         ok="数分歩くと、私たちは高い木々に囲まれた小さな湖に着いた。",
         wrongs=[("数分歩いて、私たちは高い木々を囲んでいる小さな湖に着いた。", "surrounded は過去分詞で「囲まれた」という受け身の意味。湖が木々を囲んでいるのではない。", "concept", "surrounded by tall trees"),
                 ("数分間の散歩のあと、私たちは高い木々に囲まれた小さな湖を持ってきた。", "bring O to 場所 は「O を～に連れて行く」。無生物主語の文では「…すると O は～に着く」と訳す。「持ってきた」は誤り。", "interpretation", "brought us to"),
                 ("私たちは、高い木々に囲まれた小さな湖まで数分歩いて行くつもりだ。", "brought は過去形で、予定ではなく過去の出来事を述べている。", "interpretation", "brought")],
         keys=[("無生物主語の文を「数分歩くと、私たちは～に着いた」のように訳している", 2), ("surrounded by tall trees を「高い木々に囲まれた」と湖を修飾する形で訳している", 1), ("過去の出来事として自然な日本語にしている", 1)]),
    dict(key="ONLYAFTER", en="Only after the experiment had been repeated many times did the researchers accept the result.",
         pt="Only after ～ が文頭に出たことによる倒置（did＋S＋原形）「～して初めて…」",
         ok="実験が何度も繰り返されたあとになって初めて、研究者たちはその結果を受け入れた。",
         wrongs=[("研究者たちは、何度も繰り返した実験のあとでだけ、その結果を受け入れなかった。", "did は否定ではなく、Only を文頭に置いたことによる倒置（did＋主語＋原形）である。", "concept", "did the researchers accept"),
                 ("実験が何度も繰り返されたあとで、研究者たちはその結果を受け入れたのだろうか。", "did the researchers accept は疑問文ではなく、Only ～ が文頭に出たための倒置である。", "concept", "did the researchers accept"),
                 ("研究者たちが実験を何度も繰り返したのは、その結果を受け入れたあとだけだった。", "時間の前後関係を逆にしている。結果を受け入れたのは、実験を繰り返したあとである。", "logic", "Only after the experiment had been repeated")],
         keys=[("Only after ～ を「～して初めて」と訳している", 2), ("倒置（did the researchers accept）を平叙文の意味で正しく訳している", 1), ("受け身 had been repeated を正しく訳している", 1)]),
    dict(key="IDEA", en="The idea that intelligence is fixed at birth has been challenged by many recent studies.",
         pt="同格の that「～という考え」、challenge「異議を唱える・疑問を投げかける」の受け身",
         ok="知能は生まれたときに決まっているという考えは、近年の多くの研究によって疑問視されている。",
         wrongs=[("知能を生まれたときに決めた考えは、近年の多くの研究によって疑問視されている。", "that は関係代名詞ではなく同格の接続詞で、that 以下（知能は生まれつき決まっている）が idea の内容を表す。", "concept", "The idea that"),
                 ("知能は生まれたときに決まっているという考えは、近年の多くの研究に挑戦してきた。", "has been challenged は受け身で「（考えが）疑問を投げかけられてきた」の意味。考えが研究に挑むのではない。", "interpretation", "has been challenged by"),
                 ("近年の多くの研究によって、知能は生まれたときに決まっていることが確かめられた。", "challenge は「異議を唱える・疑問を投げかける」で、確かめたのではない。意味が逆になっている。", "interpretation", "has been challenged")],
         keys=[("同格の that を「～という考え」と訳している", 2), ("challenge を「異議を唱える・疑問視する」の意味で、受け身として訳している", 2)]),
    dict(key="WHALE", en="A whale is no more a fish than a horse is.",
         pt="no more A than B「B でないのと同様に A でない」（両方を否定する）",
         ok="クジラが魚でないのは、馬が魚でないのと同じである。",
         wrongs=[("クジラは馬ほど魚らしくはない。", "no more A than B を「B ほど A でない」という程度の差と取り違えている。no more … than は両方を否定する。", "concept", "no more … than"),
                 ("クジラは、馬と同じくらい魚である。", "no more … than の否定の意味を読み落としている。両者とも魚ではないことを述べている。", "concept", "no more … than"),
                 ("クジラは、馬より少しも大きくない魚である。", "大きさの比較ではなく、「魚であるかどうか」の比較である。", "interpretation", "no more a fish")],
         keys=[("no more A than B を「B でないのと同様に A でない」と訳している", 3), ("a whale と a horse の対応を正しくとらえている", 1)]),
    dict(key="SEEN", en="Seen from the top of the hill, the town looked much smaller than I had expected.",
         pt="過去分詞で始まる分詞構文「～から見ると」、look＋形容詞「～に見える」、比較級の強調 much",
         ok="丘の頂上から見ると、その町は思っていたよりもずっと小さく見えた。",
         wrongs=[("丘の頂上から見ていたので、その町は私が予想したよりずっと小さかった。", "Seen は過去分詞で、町が「見られる」側である。また looked「～に見えた」を「～だった」と断定している。", "concept", "Seen from"),
                 ("その町が丘の頂上から見られたことは、私が予想していたよりずっと少なかった。", "much smaller を「見られた回数が少ない」と取り違えている。smaller は町の見た目の大きさの比較である。", "interpretation", "looked much smaller"),
                 ("丘の頂上から見ると、その町は私が予想していたよりずっと大きく見えた。", "smaller（より小さい）を「大きい」と逆に訳している。", "interpretation", "much smaller")],
         keys=[("分詞構文 Seen from ～ を「～から見ると」と訳している", 2), ("looked much smaller than I had expected を「思っていたよりずっと小さく見えた」と訳している", 2)]),
    dict(key="WERE", en="Were it not for the support of local volunteers, the festival could not be held every year.",
         pt="Were it not for ～（＝If it were not for ～）「～がなければ」、仮定法過去の帰結 could",
         ok="地元のボランティアの支援がなければ、その祭りを毎年開くことはできないだろう。",
         wrongs=[("地元のボランティアの支援がなかったので、その祭りは毎年は開かれなかった。", "Were it not for ～ は仮定法（If it were not for ～ の if を省略した倒置）で、現在の事実に反する仮定である。過去の事実を述べた文ではない。", "concept", "Were it not for"),
                 ("地元のボランティアの支援があったとしても、その祭りを毎年開くことはできないだろう。", "Were it not for は「～がなければ」で、「～があっても」という譲歩ではない。", "interpretation", "Were it not for"),
                 ("地元のボランティアは支援しなかったのか。その祭りは毎年は開かれない。", "Were it は疑問文ではなく、仮定法の if の省略による倒置である。", "concept", "Were it not for")],
         keys=[("Were it not for ～ を「～がなければ」と訳している", 2), ("could not be held を仮定法の帰結（～できないだろう）として訳している", 2)]),
    dict(key="WHETHER", en="It is difficult to know whether the changes we see today are part of a long natural cycle.",
         pt="形式主語 It … to do、名詞節の whether「～かどうか」、目的格の関係代名詞の省略（the changes we see）",
         ok="今日私たちが目にしている変化が、長い自然の周期の一部なのかどうかを知るのは難しい。",
         wrongs=[("今日私たちが目にしている変化が長い自然の周期の一部であろうとなかろうと、それを知るのは難しい。", "whether 節は know の目的語となる名詞節「～かどうか」である。「～であろうとなかろうと」という譲歩の副詞節ではない。", "concept", "whether"),
                 ("今日の変化を見ることは難しいが、それは長い自然の周期の一部である。", "It は形式主語で to know 以下を指す。we see today は changes を修飾する節で、「見ることが難しい」のではない。", "concept", "It is difficult to know"),
                 ("今日私たちが目にしている変化は、長い自然の周期の一部であることがよく知られている。", "difficult to know（知るのが難しい）を「よく知られている」と逆の意味にしている。", "interpretation", "difficult to know")],
         keys=[("形式主語 It … to know を「～を知るのは難しい」と訳している", 1), ("whether 節を「～かどうか」と訳している", 2), ("the changes we see today を「今日私たちが目にしている変化」と訳している", 1)]),
    dict(key="BRAIN", en="The more we learn about the brain, the more we realize how little we understand it.",
         pt="the 比較級, the 比較級「～すればするほど…」、how little「いかにわずかしか～ないか」",
         ok="脳について知れば知るほど、私たちはそれをいかにわずかしか理解していないかを思い知る。",
         wrongs=[("脳について多くを学べば、私たちはそれを少し理解できるようになる。", "the 比較級, the 比較級 の構文を読み落とし、how little（いかにわずかしか～ないか）を「少し理解できる」と肯定的に訳している。", "concept", "the more …, the more"),
                 ("脳について知れば知るほど、私たちはそれをよく理解していることに気づく。", "how little は「ほとんど理解していない」という否定的な意味で、よく理解しているのではない。", "interpretation", "how little we understand it"),
                 ("私たちは脳について多くを学んだが、それ以上に、それがいかに小さいかを理解した。", "little は理解の程度を表し、脳の大きさではない。また比例の構文を読み落としている。", "interpretation", "how little")],
         keys=[("the 比較級, the 比較級 を「～すればするほど…」と訳している", 2), ("how little we understand it を「いかにわずかしか理解していないか」と訳している", 2)]),
    dict(key="HOWEVER", en="However carefully you plan a trip, something unexpected is bound to happen.",
         pt="However＋副詞＋S V「どれほど～しても」（譲歩）、be bound to do「必ず～する」",
         ok="どれほど注意深く旅行の計画を立てても、何か予想外のことが必ず起こるものだ。",
         wrongs=[("しかし、注意深く旅行の計画を立てれば、予想外のことは起こらないはずだ。", "However は「しかし」ではなく、However＋副詞＋S V で「どれほど～しても」という譲歩を表す。また意味が逆になっている。", "concept", "However carefully"),
                 ("どれほど注意深く旅行の計画を立てても、何か予想外のことに縛られる。", "be bound to do は「必ず～する・～するに違いない」。「縛られる」と直訳するのは誤り。", "interpretation", "is bound to happen"),
                 ("旅行の計画をどのように注意深く立てたかによって、予想外のことが起こるかどうかが決まる。", "However carefully は方法を問う「どのように」ではなく、程度に関係なく、という譲歩である。", "concept", "However carefully")],
         keys=[("However＋副詞＋S V を「どれほど～しても」と訳している", 2), ("be bound to do を「必ず～する」と訳している", 2)]),
    dict(key="CAREFUL", en="You cannot be too careful when you choose words in a foreign language.",
         pt="cannot … too ～「いくら～してもしすぎることはない」、総称の you",
         ok="外国語で言葉を選ぶときは、どれほど注意してもしすぎることはない。",
         wrongs=[("外国語で言葉を選ぶときは、注意しすぎてはいけない。", "cannot … too ～ は「いくら～してもしすぎることはない」で、注意しすぎを禁じる意味ではない。", "concept", "cannot be too careful"),
                 ("外国語で言葉を選ぶときは、あまり注意深くなれない。", "too を「あまり」と訳し、cannot を能力の否定ととらえている。決まった構文として読む必要がある。", "concept", "cannot be too careful"),
                 ("外国語では、注意深い人ほど言葉を選ぶことができない。", "構文の意味を取り違え、原文にない比例の意味を加えている。", "interpretation", "cannot be too careful")],
         keys=[("cannot be too ～ を「いくら～してもしすぎることはない」と訳している", 3), ("when 節を正しく訳している", 1)]),
    dict(key="NOTALL", en="Not all of the information on the Internet is reliable, so it is important to check where it comes from.",
         pt="部分否定 Not all「すべてが～というわけではない」、形式主語 it … to do、where の間接疑問",
         ok="インターネット上の情報がすべて信頼できるわけではないので、その情報の出どころを確かめることが大切だ。",
         wrongs=[("インターネット上の情報はすべて信頼できないので、その情報の出どころを確かめることが大切だ。", "Not all は部分否定「すべてが～というわけではない」で、全部が信頼できないという全否定ではない。", "concept", "Not all"),
                 ("インターネット上の情報がすべて信頼できるわけではないので、インターネットがどこから来たのかを確かめることが大切だ。", "where it comes from の it は the information を指す。インターネットの起源を確かめるのではない。", "interpretation", "where it comes from"),
                 ("インターネット上の情報がすべて信頼できるわけではないが、それがどこから来るかは重要ではない。", "so（だから）を逆接と取り違え、it is important を否定している。", "logic", "so it is important")],
         keys=[("Not all を部分否定（すべてが～というわけではない）として訳している", 2), ("形式主語の構文と、where it comes from の it（情報）を正しく訳している", 2)]),
    dict(key="PHONE", en="The rapid spread of smartphones has enabled people to share information instantly, but it has also made it harder for them to concentrate on a single task.",
         pt="無生物主語＋enable O to do「O が～できるようにする」、make it harder for 人 to do（形式目的語）",
         ok="スマートフォンが急速に普及したことで、人々は情報を瞬時に共有できるようになったが、一つの作業に集中することがより難しくもなった。",
         wrongs=[("スマートフォンは急速に人々に広まり、情報を瞬時に共有したが、それは一つの作業に集中するのをより難しくした。", "enable O to do の O（people）が共有する主体であることを読み落とし、スマートフォンが共有したことにしている。", "concept", "has enabled people to share"),
                 ("スマートフォンが急速に普及したことで、人々は情報を瞬時に共有できるようになったが、その情報が人々を一つの作業に集中させた。", "made it harder for them to concentrate の it は形式目的語で to concentrate 以下を指す。集中させたのではなく、集中しにくくした。", "concept", "made it harder for them to concentrate"),
                 ("スマートフォンが急速に普及したので、人々はすぐに情報を共有しなければならなくなり、一つの作業に集中する必要がなくなった。", "enable は「～できるようにする」で、義務（～しなければならない）ではない。後半も原文にない内容である。", "interpretation", "has enabled")],
         keys=[("無生物主語の文を「～したことで、人々は…できるようになった」と訳している", 2), ("make it harder for 人 to do の形式目的語を正しく訳している", 2)]),
    dict(key="CHAR", en="Our character is shaped less by what happens to us than by how we respond to it.",
         pt="less A than B「A よりもむしろ B」、関係代名詞 what・間接疑問 how の名詞節",
         ok="私たちの人格は、自分の身に何が起こるかよりも、むしろそれにどう対応するかによって形づくられる。",
         wrongs=[("私たちの人格は、自分がどう対応するかよりも、自分の身に起こることによって形づくられる。", "less A than B は「A よりむしろ B」で、重点は B（どう対応するか）にある。A と B の重みが逆になっている。", "concept", "less by … than by"),
                 ("私たちの人格は、自分の身に起こることによっても、それへの対応によっても、ほとんど形づくられない。", "less … than を両方の否定と取り違えている。比べたうえで B のほうが人格を形づくると述べている。", "concept", "less by … than by"),
                 ("私たちの人格が小さくなるのは、自分の身に起こることのためではなく、それに対する反応のためである。", "less を「小さくなる」と読み、shaped（形づくられる）を見落としている。", "interpretation", "is shaped less")],
         keys=[("less A than B を「A よりもむしろ B」と訳している", 2), ("what happens to us / how we respond to it を名詞節として正しく訳している", 2)]),
    dict(key="NOTTHAT", en="It is not that she dislikes her job, but that she feels she has stopped learning anything new from it.",
         pt="It is not that A but that B「A というわけではなく B ということだ」、stop doing「～するのをやめる（～しなくなる）」",
         ok="彼女は自分の仕事が嫌いだというわけではなく、そこから新しいことを何も学ばなくなったと感じているのだ。",
         wrongs=[("彼女が仕事を嫌っていないことは、彼女がそこから何も新しいことを学ばなくなったと感じていることと同じだ。", "It is not that A but that B は「A というわけではなく B ということだ」という構文で、A と B を等しいと述べているのではない。", "concept", "It is not that … but that"),
                 ("彼女は仕事が嫌いではないが、そこから新しいことを学ぶのをやめるべきだと感じている。", "has stopped learning は「学ぶことがなくなった（現在完了）」であり、「やめるべきだ」という判断ではない。", "interpretation", "has stopped learning"),
                 ("彼女は仕事が嫌いなので、そこから新しいことを学ぶのをやめたと感じている。", "It is not that ～ の否定を読み落とし、「嫌いなので」と逆の意味にしている。", "interpretation", "It is not that")],
         keys=[("It is not that A but that B を「A というわけではなく B なのだ」と訳している", 2), ("has stopped learning anything new を「新しいことを何も学ばなくなった」と訳している", 2)]),
]
SBY = {s["key"]: s for s in SENT}

TEMPT = {
    "concept": "構文の形（倒置・強調構文・比較構文・仮定法など）に気づかず、単語の意味を前から順につないで訳したため。",
    "interpretation": "語の意味を文脈で確かめず、最初に思いついた訳語や日本語の語感に引きずられたため。",
    "logic": "節と節の論理関係（因果・逆接・時間の前後）を確かめずに訳したため。",
}

# ======================================================================
# 述語動詞を見抜く長い文（オリジナル）
# ======================================================================

MAINV = [
    ("The students who took part in the program that the city started last year say that it changed the way they think about their town.", "say", "The students",
     [("took part", "主語 The students を修飾する関係代名詞 who の節の中の動詞である。"), ("started", "program を修飾する関係代名詞 that の節の中の動詞である。"),
      ("changed", "say の目的語になる that 節の中の動詞である。"), ("think", "the way を修飾する節（they think about their town）の中の動詞である。")]),
    ("What matters is not so much how many books you read as how carefully you think about them.", "is", "What matters",
     [("matters", "主語になる名詞節 What matters の中の動詞である。"), ("read", "how many books you read という名詞節の中の動詞である。"),
      ("think", "how carefully you think about them という名詞節の中の動詞である。")]),
    ("What the speaker said at the end of the meeting made those who had doubted the plan change their minds.", "made", "What the speaker said at the end of the meeting",
     [("said", "主語になる名詞節 What the speaker said の中の動詞である。"), ("had doubted", "those を修飾する関係代名詞 who の節の中の動詞である。"),
      ("change", "make O 原形 の形で、目的語 those の動作を表す原形不定詞である。")]),
    ("Anyone who has ever tried to learn a musical instrument knows how hard it is to keep practicing when progress seems slow.", "knows", "Anyone",
     [("has ever tried", "Anyone を修飾する関係代名詞 who の節の中の動詞である。"), ("learn", "tried の目的語になる不定詞 to learn の一部である。"),
      ("seems", "when 節の中の動詞である。"), ("is", "knows の目的語になる how hard it is … の節の中の動詞である。")]),
    ("The fact that the store, which had been popular for decades, closed so suddenly surprised everyone who lived in the neighborhood.", "surprised", "The fact",
     [("closed", "fact の内容を表す同格の that 節の中の動詞である。"), ("had been", "the store を説明する非制限用法の which 節の中の動詞である。"),
      ("lived", "everyone を修飾する関係代名詞 who の節の中の動詞である。")]),
    ("Children who are allowed to make mistakes while they are young often grow into adults who are not afraid of new challenges.", "grow", "Children",
     [("are allowed", "Children を修飾する関係代名詞 who の節の中の動詞である。"), ("make", "are allowed to make の不定詞の一部である。"),
      ("are not", "adults を修飾する関係代名詞 who の節の中の動詞である。")]),
    ("One reason why so many people feel tired after using social media for hours is that they constantly compare themselves with others.", "is", "One reason",
     [("feel", "reason を修飾する関係副詞 why の節の中の動詞である。"), ("using", "前置詞 after の目的語になる動名詞である。"),
      ("compare", "補語になる that 節の中の動詞である。")]),
    ("Whether the new rule that the town introduced will actually reduce waste depends on how seriously each household follows it.", "depends", "Whether the new rule … will actually reduce waste",
     [("introduced", "rule を修飾する関係代名詞 that の節の中の動詞である。"), ("will reduce", "主語になる名詞節 Whether … の中の動詞である。"),
      ("follows", "前置詞 on の目的語になる how 節の中の動詞である。")]),
    ("The scientist, who had spent ten years on the project, said that what surprised her most was the speed at which the results appeared.", "said", "The scientist",
     [("had spent", "The scientist を説明する非制限用法の who 節の中の動詞である。"), ("surprised", "名詞節 what surprised her most の中の動詞である。"),
      ("was", "said の目的語になる that 節の中の動詞である。"), ("appeared", "speed を修飾する前置詞＋関係代名詞 at which の節の中の動詞である。")]),
    ("People living in large cities, where trains run every few minutes, rarely feel the need to own a car.", "feel", "People",
     [("living", "People を後ろから修飾する現在分詞である。"), ("run", "large cities を説明する非制限用法の関係副詞 where の節の中の動詞である。"),
      ("own", "need を修飾する不定詞 to own の一部である。")]),
    ("Those who say that they have no time to read are often the people who need books the most.", "are", "Those",
     [("say", "Those を修飾する関係代名詞 who の節の中の動詞である。"), ("have", "say の目的語になる that 節の中の動詞である。"),
      ("need", "the people を修飾する関係代名詞 who の節の中の動詞である。"), ("read", "time を修飾する不定詞 to read の一部である。")]),
]

# ======================================================================
# 語・構文の働きの識別（オリジナル）
# ======================================================================

FUNC = [
    ("There is little evidence that the new method works better.", "that", "同格の接続詞（evidence の内容を表す）",
     [("関係代名詞", "that の後ろ（the new method works better）は主語も目的語も欠けていない完全な文なので、関係代名詞ではない。"),
      ("強調構文の that", "It is ～ that の形になっていない。"), ("so … that 構文の that", "前に so がなく、程度・結果の意味もない。")]),
    ("The book that I borrowed from the library was full of useful ideas.", "that", "関係代名詞（目的格）",
     [("同格の接続詞", "that の後ろは borrowed の目的語が欠けた不完全な文なので、同格の接続詞ではない。"),
      ("強調構文の that", "It is ～ that の形になっていない。"), ("形式主語 it の真主語を導く接続詞", "文頭に形式主語 it がない。")]),
    ("It was in this small village that the famous writer spent his childhood.", "that", "強調構文の that",
     [("関係代名詞", "that の後ろは spent his childhood まで要素のそろった完全な文で、欠けている要素がない。"),
      ("形式主語 it の真主語を導く接続詞", "It was と that を取り除くと The famous writer spent his childhood in this small village. という文が成り立つので、強調構文である。"),
      ("同格の接続詞", "that の前に内容を説明される名詞（fact / idea など）がない。")]),
    ("It is surprising that so few people know about the danger.", "that", "形式主語 it の真主語（名詞節）を導く接続詞",
     [("強調構文の that", "It is と that を取り除いた Surprising so few people know … は文として成り立たないので、強調構文ではない。"),
      ("関係代名詞", "that の後ろは完全な文で、修飾される名詞もない。"), ("同格の接続詞", "that の前に内容を説明される名詞がない。")]),
    ("As we grow older, our memories of childhood become less clear.", "As", "比例「～するにつれて」",
     [("理由「～なので」", "grow older と become less clear がともに変化を表しており、一方が進むと他方も進む比例の関係である。"),
      ("様態「～のように」", "「年をとるように記憶がぼやける」では意味が通らない。"), ("譲歩「～だけれども」", "譲歩の as は形容詞＋as＋S V の語順（Young as he is）になる。")]),
    ("Leave the books as they are.", "as", "様態「～のように・～のままに」",
     [("理由「～なので」", "「本がそうなので置いておけ」では意味が通らない。as they are で「（今の）ままに」の意味。"),
      ("比例「～するにつれて」", "変化を表す語がなく、比例の意味にならない。"), ("時「～するときに」", "時を表すなら when を使うのがふつうで、ここでは状態の様子を表している。")]),
    ("Walking along the river, I found a small bird with a broken wing.", "Walking", "分詞構文（「～していると」）",
     [("動名詞（主語）", "文の主語は I で、Walking … river のあとにコンマがあり、動詞 found の主語にはなっていない。"),
      ("名詞を後ろから修飾する現在分詞", "Walking の前に修飾される名詞がない。"), ("進行形をつくる現在分詞", "be 動詞と結びついていない。")]),
    ("Walking along the river every morning keeps my grandfather healthy.", "Walking", "動名詞（文の主語）",
     [("分詞構文", "keeps の主語がほかになく、Walking … morning が主語になっている。"),
      ("名詞を後ろから修飾する現在分詞", "Walking の前に修飾される名詞がない。"), ("進行形をつくる現在分詞", "be 動詞と結びついていない。")]),
    ("The man walking along the river is my uncle.", "walking", "名詞を後ろから修飾する現在分詞",
     [("分詞構文", "walking … river は直前の The man を説明しており、文全体を修飾する副詞の働きではない。"),
      ("動名詞", "The man walking … で「歩いている男性」となり、名詞として働いているのではない。"),
      ("進行形をつくる現在分詞", "is の補語は my uncle で、walking は be 動詞と結びついていない。")]),
    ("What surprised me was his calm voice.", "What", "関係代名詞（「～すること・もの」）",
     [("疑問詞「何が」", "文全体は疑問文ではなく、What surprised me（私を驚かせたこと）が was の主語になっている。"),
      ("感嘆文の what", "感嘆文なら What a calm voice he had! のように what＋名詞の形になる。"), ("関係副詞", "What の節の中で What 自体が surprised の主語になっており、副詞の働きではない。")]),
    ("I asked him what he wanted for his birthday.", "what", "疑問詞（間接疑問）",
     [("関係代名詞", "ask 人 ～ は「人に～を尋ねる」で、尋ねる内容（何が欲しいのか）を表す間接疑問である。"),
      ("感嘆文の what", "what の後ろに名詞がなく、感嘆の意味もない。"), ("強調構文の一部", "It is ～ that の形になっていない。")]),
    ("I found it difficult to explain the rule in English.", "it", "形式目的語（to explain 以下を指す）",
     [("前に出た名詞を指す代名詞", "前に it が指せる名詞がなく、後ろの to explain the rule in English を受けている。"),
      ("強調構文の it", "it の後ろに that 節がない。"), ("天候・時間を表す it", "天候や時間の話をしていない。")]),
    ("It was not until midnight that the rain stopped.", "It", "強調構文の it（not until midnight を強調）",
     [("時間を表す it", "It was midnight だけなら時間の it だが、not until … that の形で「真夜中になって初めて雨がやんだ」を表す強調構文である。"),
      ("形式主語の it", "It was と that を取り除いて語順を整えると The rain did not stop until midnight. という文になるので、形式主語ではなく強調構文である。"),
      ("前に出た名詞を指す代名詞", "文頭の it が指す名詞が前にない。")]),
    ("Had I known the truth, I would have acted differently.", "Had", "仮定法過去完了の if の省略による倒置（＝If I had known）",
     [("疑問文の助動詞", "文末が疑問符ではなく、後半の would have acted と組み合わさる仮定の条件である。"),
      ("「持っていた」という意味の動詞", "Had＋主語＋過去分詞（known）の形で、所有の意味ではない。"),
      ("使役の have", "have O 原形 / 過去分詞 の形ではなく、Had の直後に主語 I がある。")]),
    ("So small was the room that we could hardly move.", "So", "so … that 構文の so（強調のための倒置）",
     [("接続詞「だから」", "文頭の So の直後が形容詞 small で、was the room と倒置されている。so … that「とても～なので…」の so である。"),
      ("「同様に」の so（So do I）", "So＋助動詞＋主語 で同意を表す形ではない。"), ("目的の so that", "「～するために」の意味にならない。")]),
    ("Most of the guests, who had traveled a long way, were tired.", "who", "非制限用法の関係代名詞（補足説明）",
     [("制限用法の関係代名詞", "コンマで区切られており、客全体について補足説明している。「遠くから来た客のうちの大半」と限定する意味ではない。"),
      ("疑問詞", "間接疑問の節ではなく、直前の the guests を説明している。"), ("関係副詞", "who は節の中で had traveled の主語になっており、副詞の働きではない。")]),
]

# ======================================================================
# 多義語の文脈判断（オリジナル）
# ======================================================================

WORDS = [
    ("What [[u:matters]] most is how you treat other people.", "matters", "重要である", [("物質", "ここでは主語 What の後ろの述語動詞で、名詞「物質」ではない。"), ("問題", "動詞として使われており、名詞の「問題」ではない。"), ("事柄", "名詞の意味であり、述語の位置に合わない。")]),
    ("Women [[u:account for]] about half of the club's members.", "account for", "（割合を）占める", [("説明する", "目的語が割合（about half of …）なので「説明する」では意味が通らない。"), ("責任を負う", "人数の割合について述べており、責任の話ではない。"), ("報告する", "account for に「報告する」の意味はなく、文脈にも合わない。")]),
    ("The new rule will [[u:apply to]] all students from April.", "apply to", "適用される・当てはまる", [("申し込む", "「申し込む」は apply for。規則が主語なので申し込む主体になれない。"), ("塗る", "「塗る」は apply O to ～ の形で、規則には使わない。"), ("応用する", "規則が生徒を「応用する」では意味が通らない。")]),
    ("She could not [[u:figure out]] why the machine had stopped.", "figure out", "理解する・わかる", [("計算する", "why 節（理由）が目的語なので、計算の意味ではない。"), ("図に描く", "figure の名詞の意味（図）に引きずられている。"), ("姿を現す", "figure out にこの意味はない。")]),
    ("The government must [[u:address]] the problem of rising prices.", "address", "（問題に）取り組む", [("住所を書く", "address の名詞の意味（住所）に引きずられている。目的語が problem である。"), ("演説する", "address には「演説する」の意味もあるが、目的語が problem なので「取り組む」が合う。"), ("呼びかける", "問題に呼びかけるのでは意味が通らない。")]),
    ("We [[u:owe]] much of our knowledge to earlier scientists.", "owe", "（～は…の）おかげである", [("借金がある", "owe A to B は「A を B に負っている」で、知識を借金したのではない。文脈から「おかげ」と訳す。"), ("所有する", "own（所有する）と混同している。"), ("返す", "owe は負っている状態を表し、返す行為ではない。")]),
    ("The two theories differ in one important [[u:respect]].", "respect", "点", [("尊敬", "in … respect で「～の点で」。尊敬の意味では文が通らない。"), ("敬意", "理論の違いを述べる文で、敬意は関係がない。"), ("関係", "with respect to（～に関して）と混同している。")]),
    ("He would be the [[u:last]] person to tell a lie.", "last", "（～する）最もありそうにない", [("最後の", "the last person to do は「最も～しそうにない人」という決まった表現である。"), ("最近の", "last week の「この前の」の意味と混同している。"), ("長続きする", "動詞 last（続く）の意味と混同している。")]),
    ("The company failed to [[u:meet]] the demand for its new product.", "meet", "（需要を）満たす", [("会う", "目的語が demand（需要）なので「会う」では意味が通らない。"), ("出迎える", "需要を出迎えるのでは意味が通らない。"), ("間に合う", "meet the deadline（締め切りに間に合う）と混同している。")]),
    ("These [[u:figures]] show that the population is getting older.", "figures", "数字・数値", [("人物", "show that 人口が高齢化している、という内容から統計の数字を指す。"), ("図形", "図形が人口の高齢化を示すのでは意味が通らない。"), ("姿", "人の姿の意味では文脈に合わない。")]),
    ("Visitors are asked to [[u:observe]] the rules of the library.", "observe", "（規則を）守る", [("観察する", "目的語が rules なので「守る」の意味になる。"), ("述べる", "規則を述べるよう求められるのでは文脈に合わない。"), ("祝う", "observe a holiday（祝日を祝う）の意味で、規則には使わない。")]),
    ("We need to find a [[u:means]] of reducing waste.", "means", "手段・方法", [("意味する", "a means of doing の形で名詞として使われている。"), ("平均", "mean（平均）と混同している。"), ("資産", "a man of means（資産家）の意味もあるが、of reducing waste と合わない。")]),
    ("The old bridge [[u:gave way]] under the weight of the truck.", "gave way", "崩れた", [("道を譲った", "give way には「道を譲る」の意味もあるが、under the weight of the truck（トラックの重みで）から「崩れる」と判断する。"), ("道を教えた", "橋が道を教えるのでは意味が通らない。"), ("手放した", "橋が何かを手放す話ではない。")]),
]


# ======================================================================
# 長文（オリジナル）。下線部 u: kind="trans"（和訳）/ "exp"（内容説明）
# ======================================================================

def _u(text, kind, model, keys, mc_ok, mc_wrongs, pt=None, q=None, bad=None):
    return dict(text=text, kind=kind, model=model, keys=keys, mc_ok=mc_ok, mc_wrongs=mc_wrongs, pt=pt, q=q, bad=bad or [])


PASSAGES = [
    dict(key="FORGET", title="Why We Forget",
         paras=["Most people regard forgetting as a weakness, a sign that the brain is not working as well as it should. {1} Every day we take in far more information than we could ever use, and if the brain kept all of it, finding what really matters would become extremely difficult.",
                "Consider what happens when you move to a new house. For the first few weeks, you may find yourself walking toward the place where the light switch used to be. {2} In this sense, forgetting clears space so that more useful knowledge can take its place.",
                "This does not mean that all forgetting is good. Losing the memory of a friend's name or an important appointment can cause real trouble. {3} A healthy memory, researchers suggest, is one that keeps what is likely to be useful and lets go of the rest.",
                "{4}"],
         us={1: _u("Yet a growing number of researchers argue that forgetting is not so much a failure of memory as a necessary part of it.", "trans",
                   "しかし、忘れることは記憶の失敗というよりも、むしろ記憶に欠かせない一部であると主張する研究者が増えている。",
                   [("Yet を逆接「しかし」として訳している", 1), ("a growing number of researchers を「～する研究者が増えている（ますます多くの研究者）」と訳している", 2), ("not so much A as B を「A というよりむしろ B」と訳している", 3), ("it が memory を指すことを踏まえ「記憶の（に）」と訳している", 2)],
                   "しかし、忘れることは記憶の失敗というより、むしろ記憶に必要な一部だと主張する研究者が増えている。",
                   [("しかし、忘れることは記憶の失敗と同じくらい、記憶に必要な一部であると主張する研究者が増えている。", "not so much A as B を as … as の同等比較と取り違えている。", "構文の取り違え"),
                    ("それでも、忘れることは記憶の大きな失敗であり、必要なのは記憶の一部だけだと主張する研究者が増えている。", "not so much を「大きな」と読み、A というよりむしろ B という構文を崩している。", "構文の読み落とし"),
                    ("しかし、増え続ける研究者は、忘れることは記憶の失敗ではないので必要ないと主張している。", "a necessary part of it（記憶に必要な一部）を「必要ない」と逆に訳している。", "否定の範囲の取り違え")],
                   pt="not so much A as B「A というよりむしろ B」、a growing number of ～「ますます多くの～」、it＝memory"),
             2: _u("Only when the old habit fades does the new one become automatic.", "trans",
                   "古い習慣が薄れて初めて、新しい習慣が意識しなくてもできるようになる。",
                   [("Only when ～ を「～して初めて」と訳している", 3), ("倒置 does the new one become を平叙文の意味で訳している", 2), ("the new one を「新しい習慣」と具体化している", 2), ("automatic を「意識せずにできる・自然にできる」と文脈に合わせて訳している", 1)],
                   "古い習慣が薄れて初めて、新しい習慣が自然にできるようになる。",
                   [("古い習慣が薄れるときだけ、新しい習慣は自動的になるのだろうか。", "does the new one become は疑問文ではなく、Only when ～ が文頭に出たことによる倒置である。", "倒置と疑問文の混同"),
                    ("古い習慣が薄れても、新しい習慣は自動的にはならない。", "does を否定と取り違えている。この文に否定語はない。", "倒置の誤読"),
                    ("新しい習慣が自然にできるようになって初めて、古い習慣が薄れる。", "時間の前後関係が逆である。古い習慣が薄れることが先である。", "主従関係の取り違え")],
                   pt="Only when ～ による倒置（does＋S＋原形）「～して初めて…」、the new one＝the new habit"),
             3: _u("What matters is not whether we forget, but what we forget.", "exp",
                   "忘れること自体がよいか悪いかが問題なのではなく、役に立ちそうな情報を残してそれ以外を手放すというように、何を忘れて何を覚えておくかが重要だということ。",
                   [("「忘れるかどうか（忘れること自体）は問題ではない」ことを述べている", 2), ("「何を忘れるか（何を残すか）が重要だ」ことを述べている", 2), ("役に立ちそうなものを残し、それ以外を手放すという本文の内容で具体化している", 3), ("「～ということ。」の形で説明として成り立っている", 1)],
                   "忘れること自体が問題なのではなく、どの情報を忘れ、どの情報を残すかが重要だということ。",
                   [("友人の名前や約束を忘れることは問題なので、できるだけ何も忘れないようにすべきだということ。", "第3段落前半の具体例（困る物忘れ）だけを取り上げ、筆者の主張（何を忘れるかが大切）と逆の結論にしている。", "具体例と主張の混同"),
                    ("忘れるかどうかよりも、どれだけ多くの情報を覚えられるかが重要だということ。", "what we forget の what（何を）を「どれだけ多く」と取り違えている。", "疑問詞の意味の取り違え"),
                    ("忘れることは記憶の失敗なので、何を忘れたかを記録しておくことが重要だということ。", "第1段落で紹介された一般的な見方（忘却は弱さ）を筆者の主張と取り違えており、記録の話も本文にない。", "一般論と筆者の主張の混同")],
                   q="下線部(3)はどういうことか。本文の内容に即して、日本語で具体的に説明しなさい。",
                   bad=[("私たちが忘れるかどうかではなく、私たちが何を忘れるかが重要であるということ。", "下線部を直訳しただけで、「何を忘れるか」が何を意味するか（役に立ちそうなものを残し、残りを手放すこと）が説明されていない。", "interpretation"),
                        ("友人の名前や大事な約束を忘れると困るので、忘れないようにすることが大切だということ。", "直前の具体例（困る物忘れ）だけを根拠にし、「忘れるかどうかは問題ではない」という下線部の前半と矛盾する説明になっている。", "logic")]),
             4: _u("Seen in this light, the occasional lapse of memory that worries so many of us may be less a symptom of decline than evidence that the brain is doing its job.", "exp",
                   "多くの人が心配するときどきの物忘れは、脳が衰えている兆候というよりも、不要な情報を手放して有用な知識のための余地をつくるという、脳本来の働きがきちんと行われている証拠であるかもしれない、ということ。",
                   [("「脳の衰えの兆候」というより、と A の側を退けている", 2), ("「脳が本来の役割を果たしている証拠」であることを述べている", 2), ("その役割＝不要な情報を手放し有用な知識の余地をつくることだと、本文に即して具体化している", 3), ("may（かもしれない）の控えめな言い方を反映している", 1)],
                   "ときどきの物忘れは、脳の衰えの表れというより、脳が不要な情報を整理するという本来の働きをしている証拠かもしれない。",
                   [("ときどきの物忘れは脳の衰えの表れなので、多くの人が心配するのは当然である。", "less A than B の重点（B：脳が働いている証拠）を読み違え、A（衰えの兆候）を主張としている。", "less A than B の取り違え"),
                    ("物忘れが多い人ほど、脳が仕事を熱心にしている証拠である。", "occasional（ときどきの）物忘れについて述べており、多ければ多いほどよいとは言っていない。言いすぎである。", "言いすぎ"),
                    ("物忘れを心配する人は多いが、実際にはほとんどの人は物忘れをしない。", "物忘れをしないとは書かれていない。本文にない内容である。", "本文にない情報の読みこみ")],
                   q="下線部(4)で筆者は、多くの人が心配する物忘れをどのようなものとしてとらえ直しているか。本文の内容をふまえて、日本語で説明しなさい。",
                   bad=[("ときどきの物忘れは、衰退の症状というより、脳がその仕事をしている証拠かもしれない。", "下線部を直訳しただけで、「脳の仕事」が何を指すか（不要な情報を手放し、有用な知識の余地をつくること）が説明されていない。", "interpretation"),
                        ("物忘れは脳の衰えの症状であり、脳が仕事をしすぎている証拠でもある。", "less A than B を「A であり B でもある」と読み、A（衰えの症状）を退ける方向の意味を取り違えている。", "concept")])},
         refs=[("Every day we take in far more information than we could ever use, and if the brain kept all of it, finding what really matters would become extremely difficult.", "all of it",
                "私たちが毎日取りこむ情報のすべて",
                [("脳のすべて", "it は同じ文の前半の information を指す。脳そのものの話ではない。"), ("記憶の失敗のすべて", "直前の段落の a failure of memory ではなく、同じ文の前半の information を指す。"),
                 ("私たちが本当に大切だと思うことのすべて", "what really matters は it より後ろにある語句で、it の指示対象ではない。")]),
               ("This does not mean that all forgetting is good.", "This",
                "忘れることが、より役に立つ知識のための場所をあけるということ",
                [("新しい家に引っ越すこと", "This は引っ越しの例そのものではなく、その例から引き出された結論（忘却は場所をあける）を指す。"), ("友人の名前や約束を忘れて困ること", "This の後ろで述べられる内容であり、This が指すのは前の内容である。"),
                 ("古い照明のスイッチの位置を覚えていること", "例の一部にすぎず、筆者がまとめた考えではない。")]),
               ("A healthy memory, researchers suggest, is one that keeps what is likely to be useful and lets go of the rest.", "the rest",
                "役に立ちそうにない、残りの情報",
                [("役に立ちそうな情報", "それは keeps の目的語で、the rest はそれ以外のものを指す。"), ("研究者たちの残りの意見", "the rest は記憶が手放す情報のことで、研究者の意見ではない。"),
                 ("休息の時間", "rest には「休息」の意味もあるが、ここでは the rest で「残り」の意味である。")])],
         whys=[("筆者によれば、脳がすべての情報を保持すると困るのはなぜか。", "毎日、使いきれないほど多くの情報を取りこむので、本当に大切なものを見つけるのが非常に難しくなるから。",
                [("脳がすべての情報を保持すると、脳が疲れて病気になるから。", "病気になるとは書かれていない。"), ("友人の名前や約束を忘れてしまうから。", "それは忘れることで困る例で、保持しすぎることの問題ではない。"),
                 ("新しい家の照明のスイッチの位置を覚えられないから。", "引っ越しの例は、古い習慣が薄れる必要を示すものである。")]),
               ("筆者が新しい家に引っ越す例を挙げたのは、何を示すためか。", "古い習慣を忘れることで、新しい習慣が身につく余地が生まれることを示すため。",
                [("引っ越しをすると記憶力が弱まることを示すため。", "例は忘却の役割を示すもので、記憶力が弱まるとは述べていない。"), ("照明のスイッチは同じ場所につけるべきだと示すため。", "住宅の設計の話ではない。"),
                 ("忘れることはすべてよいことだと示すため。", "第3段落で、すべての忘却がよいわけではないと述べている。")])],
         summary="忘れることは記憶の失敗とみなされがちだが、不要な情報を手放して有用な知識の余地をつくる、記憶に必要な働きでもある。大切なのは何を忘れるかであり、ときどきの物忘れは脳が正常に働いている証拠かもしれない。",
         skeys=[("忘却は記憶に必要な一部だという主張を述べている", 3), ("不要な情報を手放して有用な知識の余地をつくるという理由を述べている", 2), ("何を忘れるかが大切（すべての忘却がよいわけではない）ことに触れている", 2), ("一般的な見方→筆者の主張の流れで字数内にまとめている", 1)]),
    dict(key="SILENCE", title="The Meaning of Silence",
         paras=["In many conversations, a pause of even a few seconds can make people uncomfortable. Someone quickly says something, anything, to fill the gap. {1}",
                "However, silence is not always empty. In some cultures, a short pause before answering shows that the listener is taking the question seriously. {2} When people from such different backgrounds talk to each other, a pause that one person intends as respect can be taken by the other as a lack of interest.",
                "{3} Each simply concludes that the other person is rude or unfriendly.",
                "The solution is not to decide which rule is correct. It is to recognize that the meaning of silence, like the meaning of words, depends on the people who share it. {4}"],
         us={1: _u("It is as if silence were an empty space that must be filled before it becomes embarrassing.", "trans",
                   "それはまるで、沈黙が、気まずいものになる前に埋めなければならない空白であるかのようだ。",
                   [("as if＋仮定法過去を「まるで～であるかのようだ」と訳している", 3), ("関係代名詞 that の節で empty space を修飾している", 2), ("before it becomes embarrassing（it＝silence）を正しく訳している", 2), ("自然な日本語になっている", 1)],
                   "まるで沈黙は、気まずくなる前に埋めなければならない空白であるかのようだ。",
                   [("沈黙が、気まずくなる前に埋めなければならない空白であったなら、どうなるだろうか。", "as if は「まるで～のようだ」であり、if だけの条件文として訳すのは誤り。", "as if と if の混同"),
                    ("沈黙は、気まずくなる前に埋めなければならない空白であるから、そう見える。", "were は仮定法で、事実ではないことを述べている。理由として断定するのは誤り。", "仮定法の見落とし"),
                    ("まるで沈黙が空白を埋めて、気まずさを生んでいるかのようだ。", "must be filled は受け身で、沈黙（空白）が埋められる側である。", "能動と受動の取り違え")],
                   pt="as if＋仮定法過去「まるで～であるかのようだ」、関係代名詞 that の節が space を修飾"),
             2: _u("To reply too quickly may even suggest that one has not thought about what the other person said.", "trans",
                   "あまりにすぐに返事をすることは、相手の言ったことについて考えていないということを示しさえするかもしれない。",
                   [("To reply too quickly を主語「あまりにすぐに返事をすることは」と訳している", 2), ("may even suggest を「示しさえするかもしれない」と訳している", 2), ("one を一般の人（その人・自分）として自然に訳している", 1), ("what the other person said を「相手の言ったこと」と訳している", 3)],
                   "あまりに早く答えると、相手の話をよく考えていないと受け取られることさえあるかもしれない。",
                   [("あまりにすぐに返事をするためには、相手の言ったことを考えないほうがよいかもしれない。", "To reply は主語（～すること）であり、「～するために」という目的の意味ではない。", "不定詞の用法の取り違え"),
                    ("相手が言ったことについて考えないなら、すぐに返事をしてもよいと示唆している。", "主語と目的語の関係を組みかえている。すぐに返事をすることが、考えていないことを示すのである。", "主語の取り違え"),
                    ("あまりにすぐに返事をすることは、相手が何も言わなかったことを示すかもしれない。", "has not thought の否定は thought（考えた）にかかる。相手が言わなかったのではない。", "否定の範囲の取り違え")],
                   pt="不定詞の名詞用法（主語）、may even「～さえするかもしれない」、one＝一般の人、関係代名詞 what"),
             3: _u("Misunderstandings of this kind are hard to notice, because neither speaker is aware that the other is following different rules.", "exp",
                   "一方の話し手が相手への敬意のつもりでとった間（沈黙）を、もう一方の話し手が関心のなさと受け取るという誤解であり、どちらの話し手も、相手が自分とは異なる会話の規則に従っていることに気づいていないため、気づきにくい。",
                   [("誤解の内容：敬意のつもりの沈黙が、関心のなさと受け取られること", 3), ("背景：沈黙の意味が異なる背景をもつ人どうしの会話であること", 1), ("理由：どちらも相手が別の規則に従っていると気づいていないこと", 3), ("問われた2点に分けて、説明として成り立つ形で答えている", 1)],
                   "敬意を示すつもりの沈黙が関心のなさと受け取られるような誤解で、互いに相手が異なる規則に従っていると知らないため気づきにくい。",
                   [("沈黙が気まずいので急いで話す人がいるという誤解で、話し手が相手の話を聞いていないため気づきにくい。", "第1段落の「沈黙を埋めようとする」場面と、this kind が指す第2段落の誤解を取り違えている。", "指示内容の取り違え"),
                    ("相手の言葉の意味を誤って理解する誤解で、外国語の単語の意味を知らないため気づきにくい。", "沈黙（間）の意味についての誤解であり、単語の意味の誤解ではない。", "本文にない情報の読みこみ"),
                    ("沈黙を敬意と受け取る誤解で、どちらの話し手も沈黙の規則をよく知っているため気づきにくい。", "neither speaker is aware（どちらも気づいていない）を読み違えており、理由が逆になっている。", "否定の読み落とし")],
                   q="下線部(3)の Misunderstandings of this kind とはどのような誤解か。また、それが気づきにくいのはなぜか。本文に即して日本語で説明しなさい。",
                   bad=[("この種の誤解は、どちらの話し手も相手が異なる規則に従っていることに気づいていないので、気づきにくい。", "下線部を訳しただけで、「この種の誤解」の具体的な内容（敬意のつもりの沈黙が関心のなさと受け取られること）が説明されていない。", "interpretation"),
                        ("相手が失礼で不親切だという誤解で、相手が本当に失礼だから気づきにくい。", "第3段落の「相手を失礼だと結論づける」は誤解の結果であり、誤解の内容ではない。また、相手が本当に失礼だとは述べていない。", "logic")]),
             4: _u("The more we are aware of this, the less likely we are to judge others by standards they never agreed to.", "trans",
                   "このことを意識すればするほど、私たちは、他人がまったく同意したことのない基準でその人たちを判断することが少なくなる。",
                   [("the 比較級, the 比較級 を「～すればするほど…」と訳している", 3), ("the less likely we are to judge を「判断しにくくなる・判断することが少なくなる」と訳している", 2), ("standards they never agreed to を「彼らが一度も同意したことのない基準」と訳している", 2), ("自然な日本語になっている", 1)],
                   "このことを意識するほど、他人が同意したこともない基準で他人を判断することが少なくなる。",
                   [("このことを意識すればするほど、私たちは他人が同意しなかった基準で他人を判断しやすくなる。", "the less likely は「～しにくくなる」で、判断しやすくなるのではない。", "比較の向きの取り違え"),
                    ("私たちがこのことをあまり意識しないのは、他人が基準に同意しないからだ。", "the 比較級, the 比較級 の構文を読み落とし、理由の文と取り違えている。", "構文の読み落とし"),
                    ("このことを意識すればするほど、他人は私たちが同意したことのない基準で私たちを判断しなくなる。", "judge の主語は we、they は others を指す。判断する側とされる側が逆である。", "代名詞の指示の取り違え")],
                   pt="the 比較級, the 比較級「～すればするほど…」、be likely to do、standards (that) they never agreed to（目的格の関係代名詞の省略）")},
         refs=[("Someone quickly says something, anything, to fill the gap.", "the gap",
                "会話の中に生じた数秒の間（沈黙）",
                [("話し手どうしの年齢の差", "年齢の話は本文にない。"), ("文化の違い", "文化の違いは第2段落以降の話題で、ここでは会話中の沈黙を指す。"),
                 ("話の内容のくい違い", "直前の a pause of even a few seconds を言いかえたもので、内容のくい違いではない。")]),
               ("Misunderstandings of this kind are hard to notice, because neither speaker is aware that the other is following different rules.", "this kind",
                "相手への敬意のつもりの間（沈黙）が、関心のなさと受け取られるような誤解",
                [("沈黙を埋めるために何でも話してしまう習慣", "第1段落の内容で、this kind が指す直前の誤解ではない。"), ("相手を失礼だと結論づけること", "これは誤解の結果として後ろの文で述べられている。"),
                 ("相手の外国語の発音を聞き取れないこと", "本文にない内容である。")]),
               ("The more we are aware of this, the less likely we are to judge others by standards they never agreed to.", "this",
                "沈黙の意味は、言葉の意味と同じように、それを共有する人々によって決まるということ",
                [("どちらの規則が正しいかを決めること", "筆者はそれが解決策ではないと述べている。this はその直後の文の内容を指す。"), ("沈黙は必ず埋めなければならないこと", "第1段落の多くの人の感じ方で、筆者の考えではない。"),
                 ("相手を失礼だと考えること", "第3段落の内容で、直前の文が述べる「気づくべきこと」ではない。")])],
         whys=[("本文によれば、ある文化で答える前に短い間を置くのはなぜか。", "相手の質問を真剣に受け止めていることを示すため。",
                [("沈黙が気まずいので、話題を探すため。", "第1段落の多くの会話の例で、この文化の間の意味ではない。"), ("相手の話に関心がないことを示すため。", "それは異なる背景の人による誤った受け取り方である。"),
                 ("相手の言葉の意味がわからないため。", "本文にない内容である。")]),
               ("筆者が、どちらの規則が正しいかを決めることを解決策としないのはなぜか。", "沈黙の意味は、言葉の意味と同じように、それを共有する人々によって決まるものであり、どちらか一方が正しいわけではないから。",
                [("どちらの規則も間違っているから。", "どちらも間違いだとは述べていない。"), ("会話では沈黙をできるだけ避けるべきだから。", "筆者は沈黙が空白とは限らないと述べている。"),
                 ("規則を決めるには時間がかかりすぎるから。", "時間の問題は本文にない。")])],
         summary="会話の沈黙は気まずい空白と思われがちだが、文化によっては真剣さや敬意を示す。沈黙の意味の違いは気づきにくい誤解を生むので、その意味は共有する人々によって決まると理解し、自分の基準で他人を判断しないことが大切だ。",
         skeys=[("沈黙は空白とは限らず、敬意や真剣さを示す場合もあることを述べている", 2), ("沈黙の意味の違いが気づきにくい誤解を生むことを述べている", 2), ("沈黙の意味は共有する人々によって決まると理解すべきだという主張を述べている", 3), ("字数内で論理の流れが整っている", 1)]),
    dict(key="NAVI", title="Finding Our Way",
         paras=["Not long ago, finding your way in an unfamiliar city meant studying a paper map, asking strangers for directions, and occasionally getting lost. Today, a smartphone tells us exactly where to turn. {1}",
                "When we follow a paper map, we have to connect the picture in our hands to the streets around us. We notice a church on the corner or the shape of a park, and gradually we build a mental picture of the area. {2}",
                "{3} Rather, the point is that tools which do our thinking for us can also take away chances to develop our own abilities. {4}"],
         us={1: _u("Few would deny that this has made travel easier, but some researchers wonder what we have lost in exchange.", "trans",
                   "このことによって旅行が楽になったことを否定する人はほとんどいないだろうが、その代わりに私たちが何を失ったのかと考える研究者もいる。",
                   [("Few would deny を「否定する人はほとんどいないだろう」と訳している", 3), ("this has made travel easier を「このことで旅行が楽になった」と訳している", 1), ("wonder what ～ を「何を～したのだろうかと考える」と訳している", 2), ("in exchange を「その代わりに・引きかえに」と訳している", 2)],
                   "このことで旅行が楽になったことはほぼ誰も否定しないだろうが、引きかえに何を失ったのかと考える研究者もいる。",
                   [("このことで旅行が楽になったことを否定する人が少しはいるが、何を失ったのかを知っている研究者もいる。", "few（無冠詞）は「ほとんどない」という否定的な意味で、a few（少しはある）とは異なる。wonder も「知っている」ではない。", "few と a few の混同"),
                    ("このことで旅行が楽になったと思う人はほとんどいないので、研究者は何を失ったのかを調べている。", "deny（否定する）を読み落として意味を逆にし、but を理由の接続と取り違えている。", "否定の読み落とし"),
                    ("旅行が楽になったことを否定する人はほとんどいないだろうが、研究者の中には、旅行で失った物を交換したいと考える人もいる。", "wonder what we have lost は「何を失ったのだろうかと思う」という間接疑問で、失った物を交換したいという意味ではない。", "間接疑問の誤読")],
                   pt="Few（準否定）「～する人はほとんどいない」、would の婉曲、wonder＋間接疑問、in exchange「その代わりに」"),
             2: _u("A voice that tells us when to turn left or right requires no such effort, and as a result we may arrive at our destination with little idea of where we have been.", "exp",
                   "紙の地図を使うときのように、手元の地図と周囲の通りを結びつけ、角の教会や公園の形などに気づきながら、頭の中にその地域の地図を少しずつ作り上げる努力がいらないということ。その結果、どこを通ってきたのかほとんどわからないまま目的地に着くおそれがある。",
                   [("手元の地図と周囲の通りを結びつける努力であることを述べている", 2), ("目印に気づき、頭の中に地域の地図を作り上げる努力であることを述べている", 2), ("音声の案内ではその努力が不要だと述べている", 1), ("結果：どこを通ってきたのかわからないまま目的地に着くおそれ", 3)],
                   "地図と周りの通りを照らし合わせて頭の中に地域の地図を作る努力が不要になり、どこを通ってきたかもよくわからないまま目的地に着くおそれがある。",
                   [("左右を教えてくれる声に従う努力が不要になり、目的地に着けなくなるおそれがある。", "声に従うことは努力として述べられておらず、目的地に着けないとも書かれていない。目的地には着くが道筋がわからないのである。", "結果の取り違え"),
                    ("見知らぬ人に道をたずねる努力が不要になり、人と話す機会が減るおそれがある。", "such effort は直前の段落の紙の地図を使う努力を指す。人と話す機会の話は本文にない。", "指示内容の取り違え"),
                    ("紙の地図を買う努力が不要になり、旅行の費用が安くなる。", "費用の話は本文になく、such effort の内容（地図と街を結びつける）とも合わない。", "本文にない情報の読みこみ")],
                   q="下線部(2)の no such effort とはどのような努力がいらないということか。本文に即して具体的に説明し、その結果どうなるおそれがあるかも述べなさい。",
                   bad=[("そのような努力を必要とせず、その結果、どこにいたのかほとんどわからないまま目的地に着くかもしれない。", "such effort を「そのような努力」と訳しただけで、指す内容（地図と通りを結びつけ、頭の中に地図を作る努力）を具体的に説明していない。", "interpretation"),
                        ("見知らぬ人に道をたずねたり、道に迷ったりする努力がいらず、旅行が楽になる。", "such effort が指すのは第2段落の紙の地図を使うときの努力であり、第1段落の内容と取り違えている。また結果（道筋がわからない）が書かれていない。", "interpretation")]),
             3: _u("This is not to say that we should throw away our phones.", "trans",
                   "だからといって、私たちが携帯電話を捨てるべきだというわけではない。",
                   [("This is not to say that ～ を「だからといって～というわけではない」と訳している", 4), ("should を「～すべきだ」と訳している", 2), ("This が前段落の内容を受けていることが伝わる訳になっている", 2)],
                   "だからといって、携帯電話を捨てるべきだというわけではない。",
                   [("これは、私たちが携帯電話を捨てるべきだと言うためのものではないと言ってはいけない。", "This is not to say は決まった表現で、「言ってはいけない」という禁止ではない。", "決まった表現の直訳"),
                    ("だから、私たちは携帯電話を捨てるべきだ。", "not を読み落とし、筆者の考えと逆の意味にしている。", "否定の読み落とし"),
                    ("これは、携帯電話を捨てるべきだと言うことのできない人のことである。", "This is not to say を人の説明と取り違えている。", "構文の取り違え")],
                   pt="This is not to say that ～「だからといって～というわけではない」"),
             4: _u("It is one thing to use a tool; it is quite another to depend on it so completely that we cannot manage without it.", "trans",
                   "道具を使うことと、それがなければやっていけないほど完全にそれに頼ることとは、まったく別のことである。",
                   [("It is one thing to A; it is another to B を「A と B は別のことだ」と訳している", 3), ("quite を「まったく」と訳している", 1), ("so completely that we cannot manage without it を正しく訳している", 3), ("manage without it を「それなしでやっていく」と訳している", 1)],
                   "道具を使うことと、それなしではやっていけないほど道具に頼りきることは、まったく別である。",
                   [("道具を一つ使うことは、それなしではやっていけないほど完全に別の道具に頼ることである。", "one thing / another を「一つの」「別の道具」と数として読んでおり、2つの行為が別物だという構文を見落としている。", "構文の読み落とし"),
                    ("道具を使うことは、それに完全に頼って、それなしではやっていけなくなることと同じである。", "one thing … another は「別のことだ」という対比であり、「同じである」は逆の意味である。", "対比の取り違え"),
                    ("道具を使うことは一つのことだが、それに頼りすぎると、道具が私たちなしではやっていけなくなる。", "we cannot manage without it の主語は we で、道具ではない。", "主語の取り違え")],
                   pt="It is one thing to A; it is (quite) another to B「A することと B することは（まったく）別のことだ」、so … that ～")},
         refs=[("Few would deny that this has made travel easier, but some researchers wonder what we have lost in exchange.", "this",
                "スマートフォンがどこで曲がればよいかを正確に教えてくれるようになったこと",
                [("紙の地図で道を調べ、見知らぬ人に道をたずねること", "かつての旅の様子であり、旅行を楽にしたものではない。"), ("ときどき道に迷うこと", "道に迷うことは旅行を楽にしない。"),
                 ("研究者が失ったものについて考えること", "this の後ろの内容で、this が指すのは前の文である。")]),
               ("A voice that tells us when to turn left or right requires no such effort, and as a result we may arrive at our destination with little idea of where we have been.", "no such effort",
                "手元の地図と周りの通りを結びつけ、目印に気づきながら頭の中に地域の地図を作る努力",
                [("音声の案内に従って左右に曲がる努力", "音声の案内そのものは、努力を必要としないものとして述べられている。"), ("目的地に早く着こうとする努力", "本文にない内容である。"),
                 ("携帯電話を捨てようとする努力", "第3段落の内容で、such effort が指す前の段落の内容ではない。")]),
               ("Rather, the point is that tools which do our thinking for us can also take away chances to develop our own abilities.", "tools which do our thinking for us",
                "道順を考えることなど、本来自分で考えるべきことを代わりにしてくれる道具（音声で道案内をするスマートフォンなど）",
                [("紙の地図", "紙の地図は、自分で考えることを求める道具として対比されている。"), ("私たちの代わりに旅行に行ってくれる道具", "do our thinking は「考えることを代わりにする」で、旅行を代わりにするのではない。"),
                 ("考えるための時間を与えてくれる道具", "考えることを肩代わりする道具であり、時間を与えるのではない。")])],
         whys=[("紙の地図を使う人が、だんだんとその地域のイメージを作り上げられるのはなぜか。", "手元の地図と周りの通りを結びつける中で、角の教会や公園の形などの目印に気づくから。",
                [("紙の地図には道順を読み上げる機能があるから。", "音声で案内するのはスマートフォンである。"), ("見知らぬ人がその地域の歴史を教えてくれるから。", "歴史を教わるとは書かれていない。"),
                 ("紙の地図のほうが情報が正確だから。", "正確さの比較は本文にない。")]),
               ("筆者が、考えることを代わりにしてくれる道具に注意を促すのはなぜか。", "そうした道具は、自分自身の能力を伸ばす機会を奪うこともあるから。",
                [("そうした道具は高価で、誰でも買えるわけではないから。", "値段の話は本文にない。"), ("そうした道具は、しばしば間違った道を教えるから。", "案内が間違うとは述べていない。"),
                 ("そうした道具を使うと、旅行が難しくなるから。", "第1段落で、旅行が楽になったことは否定しにくいと述べている。")])],
         summary="スマートフォンの道案内は旅行を楽にしたが、紙の地図のように周囲を観察して頭の中に地図を作る機会を奪う。携帯電話を捨てる必要はないが、考えることを代わりにする道具に頼りきると、自分の能力を伸ばす機会を失う。",
         skeys=[("道案内で旅行が楽になったという利点を述べている", 1), ("周囲を観察し頭の中に地図を作る機会が失われるという問題を述べている", 3), ("道具に頼りきると自分の能力を伸ばす機会を失うという主張を述べている", 3), ("携帯電話を捨てる必要はないという限定を含め、字数内にまとめている", 1)]),
    dict(key="VEG", title="Judging Food by Its Looks",
         paras=["Walk into any supermarket and you will see rows of vegetables that look almost identical: carrots of the same length, tomatoes of the same bright red. {1}",
                "Farmers know that stores are unwilling to buy vegetables with unusual shapes or small marks, even when they taste exactly the same. As a result, a considerable amount of perfectly good food is thrown away before it leaves the farm. {2}",
                "Some shops have begun to sell such vegetables at lower prices, and many customers have been happy to buy them. {3}",
                "{4} The question we should ask is not how vegetables look, but whether we are wasting what the earth has produced."],
         us={1: _u("What you will not see are the many vegetables that never reached the shelves simply because they did not look right.", "trans",
                   "目にすることがないのは、単に見た目がふさわしくないというだけの理由で、店の棚に一度も並ばなかった多くの野菜である。",
                   [("What you will not see を主語「目にすることがないのは」と訳している", 3), ("関係代名詞 that の節（never reached the shelves）で vegetables を修飾している", 2), ("simply because を「単に～という理由だけで」と訳している", 2), ("did not look right を「見た目がよくない・ふさわしくない」と文脈に合わせて訳している", 1)],
                   "見ることがないのは、見た目がよくないというだけで店頭に並ばなかった多くの野菜である。",
                   [("あなたは何を目にしないのだろうか。それは見た目のよい野菜である。", "What you will not see は疑問文ではなく、関係代名詞 what の節が文の主語になっている。", "関係代名詞 what と疑問詞の混同"),
                    ("見た目がよいという理由だけで棚に並んだ多くの野菜を、あなたは目にしないだろう。", "never reached（一度も届かなかった）と did not look right（見た目がよくなかった）の否定をどちらも読み落としている。", "否定の読み落とし"),
                    ("目にすることがないのは、単に見た目がよくないので棚に手が届かなかった多くの野菜である。", "reach the shelves は野菜が「棚に届く（並ぶ）」ことで、人の手が届く話ではない。", "語の意味の取り違え")],
                   pt="関係代名詞 what の節が主語（What you will not see）、simply because「単に～という理由で」"),
             2: _u("It is not the quality of the food that decides its fate, but its appearance.", "trans",
                   "食べ物の運命を決めるのは、その品質ではなく、見た目なのである。",
                   [("強調構文を「～するのは…である」と訳している", 3), ("not A but B を「A ではなく B」と訳している", 3), ("its を「その（食べ物の）」と正しく訳している", 2)],
                   "食べ物の行く末を決めるのは、品質ではなく見た目である。",
                   [("食べ物の品質ではないものが運命を決め、見た目も決める。", "It is … that の強調構文を見落とし、not A but B の対比を崩している。", "強調構文の見落とし"),
                    ("食べ物の運命を決めるのは、見た目ではなく品質である。", "not A but B の A と B を逆にしている。", "対比の取り違え"),
                    ("食べ物の品質が運命を決めないのは、その見た目のためである。", "but its appearance を理由と取り違えている。but は not A but B の対比である。", "構文の取り違え")],
                   pt="強調構文 It is not A that ～, but B「～するのは A ではなく B である」、its＝the food's"),
             3: _u("This suggests that the demand for perfect-looking food may have been created as much by the stores as by the shoppers themselves.", "exp",
                   "見た目のよくない野菜を安く売り始めた店があり、多くの客が喜んでそれを買ったということから、完璧な見た目の食べ物への需要は、買い物客自身だけでなく、店の側によっても同じくらい作り出されてきたのかもしれない、ということ。",
                   [("This＝見た目のよくない野菜を安く売ったら多くの客が喜んで買ったこと", 3), ("完璧な見た目の食べ物への需要が「作り出された」ものであること", 2), ("as much A as B：客だけでなく店も同じくらい関わっていること", 2), ("may have been（～かもしれない）の推量を反映している", 1)],
                   "見た目の悪い野菜も喜んで買う客が多いことから、完璧な見た目を求める傾向は、客だけでなく店によっても作られてきた可能性がある。",
                   [("客が完璧な見た目の野菜を強く求めているので、店はそれに応えるしかない。", "下線部は、需要を作ったのは客だけではないと示唆しており、客だけに原因を求めるのは逆である。", "主張と逆"),
                    ("店が完璧な見た目の野菜を安く売るようになったので、客が喜んで買った。", "安く売られたのは見た目のよくない野菜（such vegetables）である。", "指示内容の取り違え"),
                    ("見た目の悪い野菜は味が劣るので、店も客も買おうとしない。", "第2段落で味はまったく同じだと述べており、客が喜んで買ったという内容とも矛盾する。", "本文と逆")],
                   q="下線部(3)の This が指す内容を明らかにしたうえで、下線部全体の意味を日本語で説明しなさい。",
                   bad=[("このことは、完璧に見える食べ物への需要が、買い物客自身と同じくらい店によって作られたかもしれないことを示唆している。", "下線部を直訳しただけで、This の内容（見た目の悪い野菜を安く売ったら多くの客が喜んで買ったこと）を明らかにしていない。", "interpretation"),
                        ("見た目のよくない野菜を安く売ったら客が買ったので、完璧な見た目の食べ物への需要は、店ではなく買い物客によって作られたということ。", "as much by A as by B（B と同じくらい A によっても）を「A ではなく B」と取り違え、店の役割を否定している。", "concept")]),
             4: _u("Had we been willing to accept vegetables as they are, much of this waste could have been avoided.", "trans",
                   "もし私たちが野菜をありのままの姿で受け入れようとしていたならば、この無駄の多くは避けられただろうに。",
                   [("Had we been … を if の省略による倒置（仮定法過去完了）として「もし～だったならば」と訳している", 3), ("could have been avoided を「避けられただろうに」と訳している", 2), ("as they are を「ありのままの（姿で）」と訳している", 2), ("this waste を「この無駄」と訳している", 1)],
                   "私たちが野菜をありのままに受け入れていたなら、この無駄の多くは防げたはずだ。",
                   [("私たちは野菜をありのままの姿で受け入れてきたので、この無駄の多くを避けることができた。", "Had we been … は仮定法で、過去の事実に反する仮定である。実際には受け入れてこなかった。", "仮定法と直説法の混同"),
                    ("私たちは野菜をありのままの姿で受け入れようとしていたか。この無駄の多くは避けられた。", "Had we been は疑問文ではなく、if を省略した倒置である。", "倒置と疑問文の混同"),
                    ("野菜がありのままであれば、私たちはこの無駄の多くを受け入れることができた。", "主語と述語の関係を崩しており、avoided（避けられた）を「受け入れる」と取り違えている。", "語の意味の取り違え")],
                   pt="仮定法過去完了の倒置（Had＋S＋過去分詞＝If S had＋過去分詞）、as they are「ありのままの」")},
         refs=[("Some shops have begun to sell such vegetables at lower prices, and many customers have been happy to buy them.", "such vegetables",
                "形がふつうと違っていたり、小さな傷があったりする（見た目のよくない）野菜",
                [("同じ長さのニンジンや同じ赤さのトマト", "それは店に並ぶ見た目のそろった野菜で、such vegetables が指す野菜とは逆である。"), ("味の悪い野菜", "第2段落で、味はまったく同じだと述べている。"),
                 ("農家が自分で食べる野菜", "本文にない内容である。")]),
               ("This suggests that the demand for perfect-looking food may have been created as much by the stores as by the shoppers themselves.", "This",
                "見た目のよくない野菜を安く売ったところ、多くの客が喜んでそれを買ったこと",
                [("店が見た目の悪い野菜を買いたがらないこと", "第2段落の内容で、直前の文の内容ではない。"), ("見た目の悪い野菜の味がよいこと", "This は直前の文の出来事全体を指す。味のよさは直前の文に書かれていない。"),
                 ("農場で多くの食べ物が捨てられること", "第2段落の内容で、直前の文の内容ではない。")]),
               ("Had we been willing to accept vegetables as they are, much of this waste could have been avoided.", "this waste",
                "見た目がよくないというだけで、十分食べられる食べ物が農場を出る前に捨てられること",
                [("店が売れ残った野菜を捨てること", "本文で述べられているのは、農場を出る前に捨てられる食べ物である。"), ("客が買いすぎた野菜を家庭で捨てること", "家庭の話は本文にない。"),
                 ("野菜を安く売ることで店が損をすること", "waste は「無駄（にされる食べ物）」で、店の損失のことではない。")])],
         whys=[("本文によれば、多くの野菜が農場から出荷される前に捨てられるのはなぜか。", "店が、味は同じでも形の変わった野菜や小さな傷のある野菜を買おうとしないから。",
                [("形の変わった野菜は味が悪いから。", "第2段落で、味はまったく同じだと述べている。"), ("客が野菜をあまり食べなくなったから。", "本文にない内容である。"),
                 ("農家が野菜を作りすぎたから。", "作りすぎが原因だとは述べていない。")]),
               ("筆者が、見た目のよくない野菜を安く売る店の例を挙げたのは、何を示すためか。", "完璧な見た目への需要が、客だけでなく店によっても作られてきた可能性を示すため。",
                [("見た目のよくない野菜は安くしないと売れないことを示すため。", "多くの客が喜んで買ったことに重点があり、値段の話が主題ではない。"), ("客は見た目のよい野菜しか買わないことを示すため。", "多くの客が見た目のよくない野菜を喜んで買っており、逆である。"),
                 ("店が利益を上げる方法を示すため。", "利益の話は本文にない。")])],
         summary="店が見た目のそろった野菜しか買わないため、味の変わらない野菜が大量に捨てられている。見た目の悪い野菜を喜んで買う客も多く、完璧な見た目への需要は店が作り出した面もある。見た目ではなく、食べ物を無駄にしていないかを問うべきだ。",
         skeys=[("見た目を理由に、味の変わらない野菜が捨てられている現状を述べている", 2), ("見た目への需要は店によっても作られたという指摘を述べている", 3), ("見た目ではなく食べ物の無駄を問うべきだという主張を述べている", 2), ("字数内で論理の流れが整っている", 1)]),
    dict(key="READ", title="Reading Slowly in a Fast World",
         paras=["We read more words today than ever before: messages, news headlines, posts, and comments, one after another. {1}",
                "When we read on a screen, we tend to jump from one line to another, looking for key words. This is useful when we only need a piece of information. {2}",
                "Deep reading is slow by nature. It requires us to keep earlier sentences in mind, to question what the writer is saying, and to connect it with what we already know. {3}",
                "{4} Like a muscle, the ability weakens when it is not used."],
         us={1: _u("But reading more is not the same as reading well, and there are signs that the habit of skimming is changing the way we approach longer texts.", "trans",
                   "しかし、多く読むことはよく読むことと同じではなく、ざっと読む習慣が、私たちの長い文章への向き合い方を変えつつある兆しがある。",
                   [("reading more is not the same as reading well を正しく訳している", 2), ("signs that ～ を同格の that として「～という兆し」と訳している", 3), ("the way we approach longer texts を「長い文章への向き合い方」と訳している", 2), ("is changing（進行形）を「変えつつある」と訳している", 1)],
                   "だが、たくさん読むことはよく読むことと同じではなく、流し読みの習慣が長い文章の読み方を変えつつあるという兆候がある。",
                   [("しかし、多く読むことはよく読むことと同じで、ざっと読む習慣が長い文章への向き合い方を変えつつあるという兆しがある。", "is not the same as の not を読み落としている。", "否定の読み落とし"),
                    ("しかし、多く読むことはよく読むことと同じではなく、ざっと読む習慣を変えた兆しが、長い文章に近づいている。", "that は同格の接続詞で、that 以下が signs の内容である。the habit of skimming が that 節の主語である。", "同格の that の見落とし"),
                    ("しかし、より多く読むことはうまく読むことではないので、長い文章を読む方法を変えるべきだという兆しがある。", "「変えるべきだ」という提案は原文にない。is changing は変化が進行中であることを表す。", "本文にない情報の読みこみ")],
                   pt="動名詞の主語、the same as、同格の that（signs that ～）、the way we approach「～への向き合い方」"),
             2: _u("The trouble is that we may come to read everything in this way, including texts that ask us to follow a long argument or to imagine another person's feelings.", "exp",
                   "画面上でキーワードを探しながら行から行へと飛ばし読みするという読み方を、長い議論をたどったり、他人の気持ちを想像したりすることを求める文章にまで、私たちが用いるようになるおそれがあること。",
                   [("in this way＝キーワードを探して行から行へ飛ばし読みする読み方", 3), ("そうした読み方をあらゆる文章に用いるようになるおそれ", 2), ("長い議論をたどる・他人の気持ちを想像する文章も含まれることを述べている", 2), ("「～おそれがあること。」など問題点の説明として成り立っている", 1)],
                   "情報を拾うための飛ばし読みを、議論をたどったり人の気持ちを想像したりすべき文章にまで使うようになるかもしれないこと。",
                   [("画面では文章を読むのに時間がかかり、長い文章を読み終えられないこと。", "画面上の読み方は「速く飛ばし読みする」ことで、時間がかかるのではない。", "本文と逆"),
                    ("キーワードを探す読み方は、必要な情報を得るのにまったく役に立たないこと。", "第2段落で、情報の一部が必要なときには役立つ（useful）と述べている。", "本文と逆"),
                    ("長い議論を含む文章は、画面では表示できないこと。", "表示の問題は本文にない。読み方の問題である。", "本文にない情報の読みこみ")],
                   q="下線部(2)で筆者が述べている「問題（The trouble）」とは何か。in this way の内容を明らかにして、日本語で説明しなさい。",
                   bad=[("問題は、私たちがすべてをこのように読むようになるかもしれないことである。", "in this way の内容（キーワードを探して飛ばし読みする読み方）と、それがどんな文章にまで及ぶのかが説明されていない。", "interpretation"),
                        ("画面上の飛ばし読みは、必要な情報を探すときにも役に立たないということ。", "第2段落で、情報の一部だけが必要なときには役に立つと述べている。問題はその読み方を長い文章にまで使うことであり、飛ばし読みそのものではない。", "logic")]),
             3: _u("None of this can be done in a hurry.", "exp",
                   "前に読んだ文の内容を覚えておくこと、筆者の言っていることに疑問をもつこと、それを自分がすでに知っていることと結びつけることの、どれ一つとして急いで行うことはできないということ。",
                   [("前の文を覚えておくことを挙げている", 2), ("筆者の言うことに疑問をもつことを挙げている", 2), ("自分の知識と結びつけることを挙げている", 2), ("None（どれ一つとして～ない）の全否定を正しく訳している", 2)],
                   "前の文を覚えておくこと、筆者に問いを立てること、既知のことと結びつけることは、どれも急いではできない。",
                   [("前の文を覚えておくことなどの一部は、急いでもできる。", "None of this は全否定で「どれも～ない」。一部はできるという意味ではない。", "全否定と部分否定の混同"),
                    ("画面上でキーワードを探して読むことは、急いではできない。", "this は直前の、深い読みに必要な3つのことを指す。飛ばし読みは急いで行う読み方である。", "指示内容の取り違え"),
                    ("深く読むことは急ぐ必要がないので、時間があるときだけすればよい。", "「時間があるときだけすればよい」という主張は本文にない。", "本文にない情報の読みこみ")],
                   q="下線部(3)の None of this が指す内容を具体的に示して、下線部の意味を日本語で説明しなさい。",
                   bad=[("このことのどれも急いで行うことはできない。", "this の内容（前の文を覚えておく・筆者に疑問をもつ・知識と結びつける）を具体的に示していない。", "interpretation"),
                        ("深く読むことの一部は、急いで行うことができないということ。", "None of this は「どれ一つとして～ない」という全否定で、「一部は」とするのは誤り。", "concept")]),
             4: _u("It is not that we have lost the ability to read deeply, but that we are given fewer and fewer occasions to use it.", "trans",
                   "私たちが深く読む能力を失ってしまったというわけではなく、その能力を使う機会がますます少なくなっているということなのである。",
                   [("It is not that A but that B を「A というわけではなく B ということだ」と訳している", 3), ("fewer and fewer を「ますます少ない」と訳している", 2), ("are given … occasions を「機会を与えられる（機会がある）」と訳している", 2), ("it を「その能力」と具体化している", 1)],
                   "深く読む力を失ったわけではなく、その力を使う機会がどんどん減っているのだ。",
                   [("私たちが深く読む能力を失ったことは、それを使う機会がますます少なくなったことである。", "It is not that ～ but that … の否定を読み落とし、A と B を等しいとしている。", "構文の読み落とし"),
                    ("私たちは深く読む能力を失ったので、それを使う機会がますます減っている。", "能力を失ったわけではないと述べているので、理由として断定するのは逆である。", "否定の読み落とし"),
                    ("私たちが深く読む能力を失ったのではなく、能力を使う機会を少しずつ他人に与えているのだ。", "we are given は受け身で、私たちが機会を「与えられる」側である。", "能動と受動の取り違え")],
                   pt="It is not that A but that B「A というわけではなく B ということだ」、比較級 and 比較級「ますます～」")},
         refs=[("This is useful when we only need a piece of information.", "This",
                "画面上で、キーワードを探しながら行から行へ飛ばし読みすること",
                [("長い議論をたどること", "それは飛ばし読みでは扱いにくい文章として後で述べられる。"), ("メッセージやニュースの見出しを書くこと", "書くことの話ではない。"),
                 ("ゆっくり深く読むこと", "深い読みは第3段落の話題で、This の直前の内容ではない。")]),
               ("It requires us to keep earlier sentences in mind, to question what the writer is saying, and to connect it with what we already know.", "it",
                "筆者が言っていること",
                [("深い読み", "connect it の it は直前の what the writer is saying を指す。文頭の It（深い読み）とは別である。"), ("前の文", "earlier sentences は複数形で、単数の it では受けられない。"),
                 ("画面", "画面は第2段落の話題である。")]),
               ("Like a muscle, the ability weakens when it is not used.", "the ability",
                "深く読む能力",
                [("多くの言葉を読む能力", "直前の文の the ability to read deeply を受けている。"), ("キーワードを探す能力", "使われ続けている読み方で、弱まるとされる能力ではない。"),
                 ("筋肉を動かす能力", "Like a muscle はたとえであり、筋肉の能力の話ではない。")])],
         whys=[("筆者が、深い読みは本来ゆっくりしたものだと述べるのはなぜか。", "深い読みには、前の文を覚えておき、筆者の言うことに疑問をもち、自分の知識と結びつけることが必要で、どれも急いではできないから。",
                [("長い文章は画面に表示するのに時間がかかるから。", "表示の問題は本文にない。"), ("キーワードを探すのに時間がかかるから。", "キーワードを探すのは飛ばし読みの方法である。"),
                 ("ゆっくり読まないと目が疲れるから。", "本文にない内容である。")]),
               ("筆者が、深く読む能力を筋肉にたとえているのはなぜか。", "深く読む能力も筋肉と同じように、使わなければ弱まることを示すため。",
                [("読書は体を鍛えるのと同じくらい疲れることを示すため。", "疲れの話はしていない。"), ("深く読む能力は、一度失うと二度と戻らないことを示すため。", "二度と戻らないとは述べていない。"),
                 ("運動をすると読む能力が高まることを示すため。", "運動と読解力の関係は本文にない。")])],
         summary="私たちは多くの文字を読むが、画面での飛ばし読みが習慣になり、長い議論をたどったり他人の気持ちを想像したりする文章にまで及ぶおそれがある。深く読む能力は失われていないが、使う機会が減っており、使わなければ弱まる。",
         skeys=[("多く読むことはよく読むことと同じではないことを述べている", 1), ("飛ばし読みの習慣が深い読みを要する文章にまで及ぶおそれを述べている", 3), ("能力は失われていないが使う機会が減り、使わなければ弱まるという主張を述べている", 3), ("字数内で論理の流れが整っている", 1)]),
]
PBY = {p["key"]: p for p in PASSAGES}


def ptext(p):
    paras = []
    for para in p["paras"]:
        for k, u in p["us"].items():
            para = para.replace("{" + str(k) + "}", f"({k}) [[u:{u['text']}]]")
        paras.append(para)
    return "\n\n".join(paras)


def pstim(p):
    return stim(f"SS-RD-{p['key']}", ptext(p), "passage", f"次の英文（“{p['title']}”）を読んで、あとの問いに答えなさい。", source="オリジナル")


def head(p):
    return f"英文“{p['title']}”について答えなさい。"


def ulist(kind=None):
    return [(p, k, u) for p in PASSAGES for k, u in p["us"].items() if kind is None or u["kind"] == kind]


# ======================================================================
# 授業プリント
# ======================================================================

EX1 = SBY["SOMUCH"]

LESSON = lesson(
    goals=["下線部和訳で、主節の主語と述語動詞を確定し、構文（倒置・強調構文・比較構文・仮定法など）を見抜いてから、採点基準を満たす日本語に訳せる。",
           "指示語・言いかえ表現の内容を本文から特定し、「～ということ。」の形で具体的に説明できる。",
           "直訳だけの答案・具体例だけの答案・構文を取り違えた答案を、採点者の視点で点検して書き直せる。"],
    duration=50,
    readiness=["5文型と、関係詞・分詞・不定詞・動名詞による修飾関係を見分けられる（HS-ENG-U01・U04〜U06）。",
               "仮定法・比較構文の基本形（as if / Were it not for / the 比較級, the 比較級 / no more … than）を知っている（HS-ENG-U07・U08）。",
               "段落の役割（主張・具体例・譲歩）とディスコースマーカーの働きを知っている（HS-ENG-U09）。"],
    flow=[("導入：二次試験の和訳はどう採点されるか", 5, "構文ごとに配点される採点の仕組みと、「意味が何となく通る訳」が減点される理由を示す"),
          ("下線部和訳の手順", 15, "SV の確定 → 構文の特定 → 訳語の選択 → 日本語の調整の4段階を例題1で実演する"),
          ("内容説明の答案の型", 15, "指示語の特定と「～ということ。」の型を例題2で練習し、直訳との違いを比べる"),
          ("誤訳の点検", 10, "例題3で構文の取り違えを採点者の目で見つけ、書き直す"),
          ("まとめと確認", 5, "確認問題3問、時間配分の目安と問題プリントの取り組み方の指示")],
    sections=[
        intro("in1", "二次試験の和訳・説明問題は「構文ごとに点がつく」",
              "国公立大学の二次試験や私立大学の個別試験の英語では、下線部を日本語に訳す問題と、下線部の内容を日本語で説明する問題が中心になる。採点は「全体として意味が通るか」だけでなく、下線部に含まれる構文や語句ごとに配点される。たとえば not so much A as B を含む文なら、その構文を「A というよりむしろ B」と正しく訳せているかに点がつき、何となく意味の通る訳でも構文を取り違えていれば大きく減点される。説明問題では、下線部をそのまま訳しただけの答案は「説明」になっておらず、指示語の内容を本文から補って具体化しないと点にならない。",
              bullets=["和訳：構文・文法事項・語句の訳し方ごとに部分点がある。まず骨組み（S と V）を確定する。",
                       "内容説明：指示語（this / it / such）や抽象的な表現を、本文の具体的な内容で置きかえる。",
                       "どちらも「採点者が確認したい箇所」が答案に見える形で書かれていることが大切である。"],
              points=[tp("同じ英文に対する2つの答案（構文を正しく訳したぎこちない訳／構文を取り違えた自然な訳）を見せ、どちらが高く採点されるかを考えさせる。",
                         ask="自然な日本語だが構文を取り違えた訳と、少し硬いが構文どおりの訳では、どちらが点になるか。",
                         expect="構文どおりの訳。採点は構文ごとの部分点なので、意味を取り違えた自然な訳は点が入らない。", timing="導入の冒頭"),
                      tp("試験時間の中で和訳・説明問題にかける時間の目安（1問5〜8分）を示し、下書きに時間をかけすぎないよう伝える。",
                         caution="完璧な日本語を求めて推敲に時間を使い、長文の後半を読み切れない受験生が多い。")]),
        definition("df1", "下線部和訳で確認される主な構文",
                   "下線部和訳では、文の骨組み（主節の主語と述語動詞）と、日本語の語順どおりには訳せない構文が採点のポイントになる。代表的なものを次に挙げる。",
                   bullets=["強調構文：It is A that ～「～するのは A だ」。It is not until A that B「A して初めて B」。",
                            "比較構文：not so much A as B / less A than B「A というよりむしろ B」、no more A than B「B でないのと同様に A でない」、the 比較級, the 比較級「～すればするほど…」。",
                            "倒置：Only when / Only after ～＋助動詞＋S＋V「～して初めて…」、Were it not for ～ / Had S p.p.（if の省略）。",
                            "否定：Not all（部分否定）、Few / Little（準否定）、cannot … too ～「いくら～してもしすぎることはない」。",
                            "名詞節・同格：what 節が主語、the idea that ～（同格）、It is not that A but that B「A というわけではなく B だ」。"],
                   conditions=["構文の判断は形で行う。強調構文は It is と that を取り除いても文が成り立つ。同格の that の後ろは完全な文、関係代名詞の that の後ろは要素が欠けた文。",
                               "語の意味は文脈で決める。address the problem「問題に取り組む」、meet the demand「需要を満たす」のように、目的語との組み合わせで判断する。"],
                   points=[tp("強調構文と形式主語の構文を並べて板書し、「It is と that を消して文が残るか」で見分ける方法を確認する。",
                              ask="It is surprising that so few people know about the danger. は強調構文か。",
                              expect="It is と that を消すと Surprising so few people know … となり文にならないので、形式主語の構文である。"),
                           tp("比較構文は「どちらに重点があるか」を矢印で示させる。not so much A as B、less A than B はどちらも B に重点がある。",
                              caution="not so much A as B を as … as（同じくらい）と読む誤りが非常に多い。")]),
        theorem("th1", "内容説明の答案の型",
                "答案＝（指示語・抽象表現の中身を本文で具体化した内容）＋（下線部の構文が示す論理関係）＋「～ということ。」",
                ["指示語（this / it / such ～ / of this kind）は、原則として直前の文・段落から中身を探す。",
                 "下線部の否定・比較・対比（not A but B, less A than B）の向きを答案でも保つ。",
                 "理由を問われたら「～から。」、内容を問われたら「～ということ。」で結ぶ。",
                 "本文にない推測や一般論、具体例の細部（数値・固有の場面）だけで答案を作らない。"],
                body="説明問題は「下線部を読んでいない人にもわかるように書く」問題である。下線部の訳をそのまま書くと、this や such effort が何を指すのかが答案から読み取れず、採点者が確認したい中身が欠けてしまう。",
                points=[tp("下線部の直訳と模範答案を並べ、模範答案に「本文から補った語句」がいくつあるかを数えさせる。",
                           ask="直訳の答案に足りないものは何か。", expect="指示語の中身（具体的な内容）と、下線部の前後で述べられた理由や結果。")]),
        derivation("dv1", "下線部和訳の4段階（なぜこの順に処理するのか）",
                   ["① 骨組みの確定：主節の主語と述語動詞を探す。関係詞節・that 節・分詞・不定詞の中の動詞は述語動詞ではない。かっこでくくって外す。",
                    "② 構文の特定：倒置・強調構文・比較構文・仮定法・否定の範囲など、語順どおりに訳すと意味が変わる箇所に印をつける。",
                    "③ 訳語の選択：多義語（matter, address, meet, figure など）を文脈で決め、決まった構文は定訳（「～して初めて」「A というよりむしろ B」）で訳す。",
                    "④ 日本語の調整：無生物主語は「～によって／～すると」と人を主語に言いかえ、修飾関係が誤解されない語順に直す。最後に訳を英文と照合し、否定・比較の向きが保たれているか確かめる。",
                    "この順に処理するのは、①②を誤ると③④でどれほど自然な日本語にしても点にならないからである。採点は構文ごとに行われるので、骨組みと構文を先に固めれば、日本語が多少硬くても大きな失点はない。"],
                   body="和訳の失点の多くは、単語の意味を前から順につないで「それらしい日本語」を作ることから生じる。骨組みと構文を先に決め、日本語の調整を最後に回す手順を習慣にする。",
                   points=[tp("長い文の関係詞節・that 節をかっこでくくり、残った部分が S＋V になることを全員で確認する。",
                              ask="The students who took part in the program that the city started last year say that … の述語動詞はどれか。",
                              expect="say。took part と started は関係詞節の中、that 以下は say の目的語。", timing="例題1の前")]),
        example("ex1", "例題1　下線部和訳（比較構文）",
                f"次の英文を和訳しなさい。\n{EX1['en']}",
                ["① 骨組み：主語 What matters（大切なこと）、述語動詞 is。補語は not so much A as B の部分。",
                 "② 構文：not so much A as B「A というよりむしろ B」。A＝how many books you read、B＝how carefully you think about them（いずれも間接疑問の名詞節）。",
                 "③ 訳語：how many ～「何冊～か」、how carefully ～「どれほど注意深く～か」。",
                 "④ 調整：「大切なのは、～かというよりも、むしろ…かである。」の形に整える。"],
                EX1["ok"],
                thinking="not so much A as B は「A と B が同じくらい」ではない。重点は B にあることを、訳の「むしろ」で示す。",
                points=[tp("as … as と混同した誤訳（「同じくらい」）を示し、どの語で区別できるかを確認する。",
                           ask="not so much A as B と as much A as B はどう違うか。", expect="not so much A as B は B に重点、as much A as B は A と B が同程度。")],
                misconceptions=[("not so much A as B を「A と同じくらい B」と訳す。", "「A というよりむしろ B」。B に重点がある")]),
        example("ex2", "例題2　内容説明（指示語の具体化）",
                f"次の英文の下線部(3)はどういうことか。本文の内容に即して、日本語で具体的に説明しなさい。\n{ptext(PBY['FORGET'])}",
                ["下線部(3)の直訳は「大切なのは、私たちが忘れるかどうかではなく、何を忘れるかだ」。これだけでは説明にならない。",
                 "「何を忘れるか」の中身を本文で探す：直後の文に「役に立ちそうなものを残し、残りを手放す」とある。",
                 "not A but B の向きを保つ：「忘れること自体は問題ではない」＋「何を忘れて何を残すかが重要」。",
                 "「～ということ。」で結ぶ。"],
                PBY["FORGET"]["us"][3]["model"],
                thinking="下線部の前後で、筆者が言いかえ・具体化している文を探す。説明問題の答えは多くの場合、下線部の直後か直前にある。",
                points=[tp("直前の文（友人の名前を忘れると困る）だけで答案を作った例を示し、下線部の前半（忘れるかどうかは問題ではない）と矛盾することに気づかせる。",
                           ask="「忘れないことが大切だ」という答案は下線部と合っているか。", expect="合わない。下線部は「忘れるかどうか」は問題ではないと言っている。")]),
        example("ex3", "例題3　誤訳の点検（部分否定）",
                f"次の英文を、ある生徒は下のように訳した。誤りを指摘し、正しく訳しなさい。\n{SBY['NOTALL']['en']}\n［生徒の訳］{SBY['NOTALL']['wrongs'][0][0]}",
                ["Not all ～ は部分否定で「すべてが～というわけではない」。生徒の訳「すべて信頼できない」は全否定になっている。",
                 "後半の it is important to check where it comes from は形式主語の構文で、where it comes from の it は the information を指す。",
                 "前半と後半は so（だから）でつながる因果関係。"],
                SBY["NOTALL"]["ok"],
                thinking="not と all / always / every が組み合わさると部分否定になる。否定がどこまでかかるかを確認する。",
                points=[tp("部分否定と全否定（None of ～ / No ～）を対にして板書し、意味の違いを確認する。", timing="例題3の解説時")]),
        board("bd1", "板書案",
              [("① 和訳の4段階", ["S と V を確定（節はかっこでくくる）", "構文に印（倒置・強調・比較・仮定法・否定）", "訳語は文脈で決める", "日本語の調整は最後", "英文と照合（否定・比較の向き）"]),
               ("② 要注意の構文", ["It is not until A that B＝A して初めて B", "not so much A as B / less A than B＝むしろ B", "no more A than B＝B と同様 A でない", "Only when ～＋倒置＝～して初めて", "Not all＝部分否定"]),
               ("③ 内容説明の型", ["指示語の中身を本文で探す", "直訳だけでは説明にならない", "否定・対比の向きを保つ", "具体例だけで答えない", "「～ということ。」「～から。」で結ぶ"])],
              points=[tp("②の構文は、例題で使った英文をそのまま板書に残し、問題プリントで出会ったら板書と照合させる。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("和訳の答案は、まず英文に S・V の記号と構文の印をつけさせてから書かせる。印のない答案は書き直させる。", caution="いきなり日本語を書き始めると、倒置や強調構文を見落とす。"),
               tp("採点基準（部分点）を生徒に示し、自分の答案を自己採点させる。どの構文で点を落としたかを記録させる。", timing="問題プリント C・D の解説時"),
               tp("内容説明では、答案に本文から補った語句に下線を引かせる。下線がない答案は直訳である可能性が高い。",
                  ask="あなたの答案で、下線部に書かれていない語句はどれか。", expect="指示語の中身として補った語句（例：役に立ちそうなものを残し、残りを手放す）。"),
               tp("指定字数の8〜9割以上を目安に書かせる。短すぎる答案は要素の欠落、長すぎる答案は具体例の細部の書きすぎを疑わせる。"),
               tp("誤訳の典型（as if を if と読む、Had S p.p. を疑問文と読む、Few を a few と読む）は、問題プリント D で原因まで説明させる。")],
              misconceptions=[("自然な日本語なら多少意味がずれても点になる。", "採点は構文ごとの部分点。構文を取り違えた自然な訳は点にならない"),
                              ("内容説明は下線部を丁寧に訳せばよい。", "指示語・抽象表現の中身を本文で具体化しないと説明にならない"),
                              ("文頭の Only / Had / Were の後ろは疑問文である。", "否定語・only を含む語句が文頭に出たときや if の省略では、平叙文でも倒置が起こる")]),
        summary("sm1", "まとめ",
                ["和訳は「S・V の確定 → 構文の特定 → 訳語の選択 → 日本語の調整」の順。構文ごとに部分点がある。",
                 "比較・否定・倒置・強調の構文は、重点や否定の範囲を訳で保つ（むしろ B／～して初めて／すべてが～わけではない）。",
                 "内容説明は、指示語の中身を本文で具体化し、下線部の論理（not A but B など）を保って「～ということ。」で結ぶ。"]),
        check("ck1", "確認問題",
              [("It is not until A that B を訳すときの定訳は何か。", "「A して初めて B」"),
               ("Only after the meeting did he understand the problem. の did he understand は疑問文か。", "疑問文ではない。Only after ～ が文頭に出たことによる倒置で、「会議のあとになって初めて彼は問題を理解した」"),
               ("内容説明で下線部をそのまま訳しただけの答案が減点される理由は何か。", "指示語や抽象的な表現の中身が具体化されておらず、下線部の内容を説明したことにならないから")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

@gen("basic_check", 4, ["concept", "condition_check"])
def a_function(r):
    sent, word, ok, wrongs = r.choice(FUNC)
    marked = sent.replace(word, f"[[u:{word}]]", 1)
    return mc(f"次の英文の下線部 {word} の働きとして最も適切なものを選びなさい。\n{marked}", [ok] + [w for w, _ in wrongs],
              f"{ok}。形（前後の語順・欠けている要素・取り除いて文が成り立つか）から判断する。", d=2,
              ap="下線部の前後を見て、①後ろが完全な文か要素の欠けた文か、②前に修飾される名詞があるか、③取り除いても文が成り立つか、を確かめる。",
              steps=["下線部の後ろの節が完全な文か、主語・目的語が欠けた文かを確かめる。", "下線部の前に説明・修飾される名詞があるかを確かめる。",
                     "It is ～ that や倒置などの決まった形かどうかを確かめる。", f"答え：{ok}"],
              alt=["選んだ働きで全文を訳してみて、意味が通るかどうかで確かめる。"],
              pc=[("形の手がかりに気づいている", 1), ("正しい働きを選んでいる", 1)],
              pit=["that をいつも関係代名詞、-ing をいつも動名詞と決めつける。"], why={w: (why, "語の働きの形による識別不足") for w, why in wrongs})


@gen("basic_check", 4, ["computation", "common_error"])
def a_translation_mc(r):
    s = r.choice(SENT)
    wr = s["wrongs"]
    return mc(f"次の英文の和訳として最も適切なものを選びなさい。\n{s['en']}", [s["ok"]] + [w[0] for w in wr],
              f"{s['ok']}　ポイント：{s['pt']}。", d=2,
              ap="主節の S と V を確定し、構文（倒置・比較・否定・強調など）を特定してから、選択肢の訳がその構文を正しく反映しているかを見る。",
              steps=["主節の主語と述語動詞を確定する。", f"構文を特定する：{s['pt']}。", "選択肢の訳を、否定の範囲・比較の向き・時制で照合する。", f"答え：{s['ok']}"],
              alt=["選んだ訳を英語に戻すつもりで読み、原文の構文（否定・比較・倒置）がすべて訳に表れているかを確かめる。"],
              pc=[("構文を特定している", 1), ("正しい訳を選んでいる", 1)],
              pit=["日本語として自然な選択肢を、構文を確かめずに選ぶ。"], why={w[0]: (w[1], "構文・語の意味の取り違え") for w in wr})


@gen("basic_check", 4, ["computation", "concept"])
def a_main_verb(r):
    sent, ok, subj, wrongs = r.choice(MAINV)
    picks = r.sample(wrongs, 3)
    return mc(f"次の英文の、文全体の述語動詞（主節の主語に対応する動詞）として最も適切なものを選びなさい。\n{sent}", [ok] + [w for w, _ in picks],
              f"{ok}。主節の主語は {subj}。関係詞節・that 節・分詞・不定詞の中の動詞を外すと、残る述語動詞は {ok} である。", d=2,
              ap="関係詞節・名詞節・分詞・不定詞をかっこでくくり、残った部分から主語と述語動詞を探す。",
              steps=["関係詞（who / which / that / where / why）で始まる節をかっこでくくる。", "名詞節（what / whether / how / that ～）と、分詞・不定詞の句をくくる。",
                     f"残った骨組み：主語 {subj}、述語動詞 {ok}。"],
              alt=["主語を代名詞（It / They など）に置きかえ、述語動詞とつないだ短い文が成り立つかで確かめる。"],
              pc=[("節や句をくくって骨組みを取り出している", 1), ("述語動詞を選んでいる", 1)],
              pit=["文の最初に出てくる動詞を述語動詞と決めつける。"], why={w: (why, "節の中の動詞と主節の動詞の混同") for w, why in picks})


@gen("basic_check", 4, ["condition_check", "concept"])
def a_referent(r):
    p = r.choice(PASSAGES)
    sent, expr, ok, wrongs = r.choice(p["refs"])
    return mc(f"{head(p)}\n本文中の “{sent}” の {expr} が指す内容として最も適切なものを選びなさい。", [ok] + [w for w, _ in wrongs],
              f"{ok}。{expr} の指す内容は、原則として直前の文・段落から探す。", d=2, stim=pstim(p),
              ap=f"{expr} を含む文の直前を読み、文法的に受けられる（単数・複数、人・もの）語句と、意味が通る内容を探す。",
              steps=[f"{expr} を含む文の位置を本文で確かめる。", "直前の文・段落から候補を探す（単数・複数も確認）。", f"候補を {expr} の位置に入れて意味が通るか確かめる。", f"答え：{ok}"],
              alt=["選んだ内容を本文の該当箇所に代入して読み直し、前後の論理（理由・逆接・まとめ）と矛盾しないかを確かめる。"],
              pc=[("指示語の前の文脈を確認している", 1), ("正しい内容を選んでいる", 1)],
              pit=["指示語より後ろにある語句や、離れた段落の語句を選ぶ。"], why={w: (why, "指示内容の取り違え") for w, why in wrongs})


@gen("basic_check", 4, ["computation", "concept"])
def a_word_sense(r):
    sent, w, ok, wrongs = r.choice(WORDS)
    return mc(f"次の英文の下線部 {w} の文脈上の意味として最も適切なものを選びなさい。\n{sent}", [ok] + [x for x, _ in wrongs],
              f"「{ok}」。多義語の意味は、主語・目的語との組み合わせ（文脈）で決まる。", d=2,
              ap="下線部の品詞（動詞か名詞か）と、主語・目的語・前後の語句との組み合わせを確かめてから意味を決める。",
              steps=["下線部の品詞を確かめる。", "主語・目的語・前後の語句との組み合わせを確かめる。", f"文脈に合う意味：{ok}"],
              alt=["選んだ意味で全文を訳し、ほかの意味を入れた場合と比べて意味が通るかを確かめる。"],
              pc=[("品詞・組み合わせを確かめている", 1), ("文脈に合う意味を選んでいる", 1)],
              pit=["最初に覚えた意味（matter＝物質、address＝住所 など）をそのまま当てはめる。"], why={x: (why, "多義語の文脈判断の誤り") for x, why in wrongs})


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 5, ["computation", "application"])
def b_translate(r):
    s = r.choice(SENT)
    hint = r.random() < 0.5
    stem = (f"次の英文を、構文（{s['pt']}）に注意して和訳しなさい。\n{s['en']}" if hint else f"次の英文を和訳しなさい。\n{s['en']}")
    return desc(stem, s["ok"], f"ポイント：{s['pt']}。", s["keys"], d=3, p=4, lines=3,
                ap="主節の S と V を確定し、語順どおりに訳すと意味が変わる構文に印をつけてから訳す。",
                steps=["関係詞節・名詞節・分詞・不定詞をかっこでくくり、主節の S と V を確定する。", f"構文を特定する：{s['pt']}。",
                       "多義語・決まった表現の訳語を文脈で決める。", f"日本語を整える。解答例：{s['ok']}"],
                alt=["書いた訳を英文と1語ずつ対応させ、否定・比較の向き・時制が保たれているかを確かめる。"],
                pc=list(s["keys"]),
                pit=["単語の意味を前から順につないで、構文を見落とす。", "自然な日本語にしようとして、否定や比較の向きを変えてしまう。"])


@gen("standard_practice", 5, ["condition_check", "written_reasoning"])
def b_ref_desc(r):
    p = r.choice(PASSAGES)
    sent, expr, ok, wrongs = r.choice(p["refs"])
    return desc(f"{head(p)}\n本文中の “{sent}” の {expr} が指す内容を、日本語で具体的に説明しなさい。", ok,
                f"{expr} の指す内容は直前の文脈にある。{wrongs[0][0]} などと取り違えないよう、文法（単数・複数）と意味の両方で確かめる。",
                [("指示内容を本文の正しい箇所から特定している", 3), ("具体的に、日本語として自然に書いている", 1)], d=3, p=4, lines=2, stim=pstim(p),
                ap=f"{expr} を含む文の直前の文・段落を読み、{expr} の位置に入れて意味が通る内容を探す。",
                steps=[f"{expr} を含む文を本文で見つける。", "直前の文・段落から候補を探す。", f"候補を {expr} の位置に入れて読み、意味が通るかを確かめる。", f"解答例：{ok}"],
                alt=["誤りやすい候補（" + "／".join(w for w, _ in wrongs[:2]) + "）を入れた場合と比べ、前後の論理が成り立つのはどれかで確かめる。"],
                pc=[("指示内容の特定", 3), ("具体的な表現", 1)],
                pit=["指示語を「このこと」「それ」と訳しただけで、中身を書かない。", "指示語より後ろの内容を答える。"])


@gen("standard_practice", 5, ["concept", "application"])
def b_underline_mc(r):
    p, k, u = r.choice(ulist())
    what = "和訳" if u["kind"] == "trans" else "内容の説明"
    return mc(f"{head(p)}\n下線部({k})（{u['text']}）の{what}として最も適切なものを選びなさい。", [u["mc_ok"]] + [w for w, _, _ in u["mc_wrongs"]],
              f"{u['mc_ok']}　" + (f"ポイント：{u['pt']}。" if u["pt"] else "下線部の指示語・抽象表現の中身を本文から補って判断する。"), d=3, stim=pstim(p),
              ap="下線部の構文（否定・比較・倒置・強調）と指示語の中身を確かめ、選択肢がそれを正しく反映しているかを照合する。",
              steps=["下線部の主節の S と V、構文を確認する。", "指示語・抽象表現が本文のどこを受けているかを確かめる。",
                     "選択肢を「構文の取り違え・指示内容の取り違え・本文にない内容」の観点で点検する。", f"答え：{u['mc_ok']}"],
              alt=["選んだ選択肢を下線部の位置に置いて本文を読み直し、前後の文脈と矛盾しないかを確かめる。"],
              pc=[("構文・指示内容を確かめている", 2), ("正しい選択肢を選んでいる", 2)],
              pit=["下線部と同じ単語を多く含む選択肢を、構文を確かめずに選ぶ。"], why={w: (why, mis) for w, why, mis in u["mc_wrongs"]})


@gen("standard_practice", 5, ["concept", "condition_check"])
def b_reason_mc(r):
    p = r.choice(PASSAGES)
    q, ok, wrongs = r.choice(p["whys"])
    return mc(f"{head(p)}\n{q}最も適切なものを選びなさい。", [ok] + [w for w, _ in wrongs],
              f"{ok}　設問に関わる段落の論理（理由・結果・例示）を本文で確かめる。", d=3, stim=pstim(p),
              ap="設問のキーワードを本文で探し、その前後で because / so / as a result / For example などが示す論理関係を確かめる。",
              steps=["設問が問う内容（理由・目的）を確認する。", "本文の該当箇所を見つけ、理由や目的を述べた部分を特定する。",
                     "選択肢を「本文にない・本文と逆・別の段落の内容」で点検する。", f"答え：{ok}"],
              alt=["選んだ選択肢を「なぜなら～だから」と設問の文につなげ、本文の論理と一致するかを確かめる。"],
              pc=[("根拠となる箇所を特定している", 2), ("正しい選択肢を選んでいる", 2)],
              pit=["本文に出てくる語句を含むだけで、論理関係の合わない選択肢を選ぶ。"], why={w: (why, "本文の論理関係の読み違い") for w, why in wrongs})


# ======================================================================
# C 思考力・記述応用
# ======================================================================

@gen("thinking_writing", 4, ["written_reasoning", "application"])
def c_translate(r):
    p, k, u = r.choice(ulist("trans"))
    mode = r.choice(["plain", "struct"])
    if mode == "plain":
        stem = f"{head(p)}\n下線部({k})を和訳しなさい。\n{u['text']}"
        keys = u["keys"]
        ans = u["model"]
    else:
        stem = f"{head(p)}\n下線部({k})について、和訳の際に注意すべき構文・文法事項を1つ指摘したうえで、全体を和訳しなさい。\n{u['text']}"
        keys = [("注意すべき構文・文法事項を正しく指摘している", 2)] + [(t, v) for t, v in u["keys"][:-1]]
        tot = sum(v for _, v in keys)
        if tot > 8:
            keys = [(t, v) for t, v in keys[:-1]] + [(keys[-1][0], keys[-1][1] - (tot - 8))]
        ans = f"（構文）{u['pt']}。（和訳）{u['model']}"
    return desc(stem, ans, f"ポイント：{u['pt']}。下線部の前後の文脈（指示語・代名詞の指す内容）も踏まえて訳す。", keys, d=4, p=8, lines=4, stim=pstim(p),
                ap="主節の S と V を確定し、語順どおりに訳すと意味が変わる構文に印をつける。代名詞は本文で指す内容を確かめる。",
                steps=["関係詞節・名詞節・分詞・不定詞をかっこでくくり、骨組みを取り出す。", f"構文を特定する：{u['pt']}。",
                       "代名詞・指示語の指す内容を前後の文脈で確かめる。", f"日本語を整える。解答例：{u['model']}"],
                alt=[f"別の訳し方の例：{u['mc_ok']}　構文の意味が保たれていれば、語順や言い回しは変えてよい。"],
                pc=list(keys),
                pit=["構文を見落として、単語をつないだ訳にする。", "代名詞を「それ」と訳し、何を指すかが伝わらない訳にする。"])


@gen("thinking_writing", 3, ["written_reasoning", "condition_check"])
def c_explain(r):
    p, k, u = r.choice(ulist("exp"))
    base = (len(u["model"]) + 9) // 10 * 10
    lim = r.choice([base + 10, base + 30])
    return desc(f"{head(p)}\n{u['q']}（{lim}字以内）\n下線部({k})：{u['text']}", u["model"],
                "下線部の指示語・抽象表現の中身を本文で具体化し、下線部の論理（否定・比較・対比）を保って説明する。", u["keys"], d=4, p=8, grid=lim, stim=pstim(p),
                ap="下線部の指示語・抽象表現に印をつけ、その中身を直前・直後の文から探す。下線部の構文（not A but B、less A than B など）の向きを答案でも保つ。",
                steps=["下線部を一度直訳し、具体化が必要な語句（this / such / of this kind など）を確認する。", "その中身を本文から探し、日本語でまとめる。",
                       "下線部の論理関係（否定・比較・因果）を保って文を組み立てる。", "「～ということ。」などで結び、字数を調整する。"],
                alt=["先に採点ポイント（指示内容・論理・結論）を箇条書きにし、それを1文につなげる方法で書くと、要素の書きもらしを防げる。"],
                pc=list(u["keys"]),
                pit=["下線部を直訳しただけで答案にする。", "具体例の細部を書きすぎて、肝心の要素を字数内に入れられない。"])


@gen("thinking_writing", 3, ["cross_unit", "written_reasoning"], rel=["HS-ENG-U09", "HS-JPN-U08"])
def c_summary(r):
    p = r.choice(PASSAGES)
    lim = r.choice([120, 130, 150])
    return desc(f"{head(p)}\n本文の要旨を、筆者の主張がわかるように日本語{lim}字以内でまとめなさい。", p["summary"],
                "段落の役割（話題の提示・具体例・譲歩・主張）をつかみ、具体例の細部を除いて、筆者の主張とその根拠をまとめる。英語の段落構成の読み取り（HS-ENG-U09）と、日本語での要約の技術（HS-JPN-U08）を組み合わせる。",
                p["skeys"], d=4, p=8, grid=lim, stim=pstim(p),
                ap="各段落の役割を書きこみ、筆者の主張が述べられた段落（しばしば最終段落や It is not that … but that / The question is … の文）を中心にする。",
                steps=["各段落に役割（話題・具体例・譲歩・主張）を書きこむ。", "具体例（引っ越し・紙の地図・ニンジンなど）の細部を除く。",
                       "「一般的な見方・現状 → 筆者の指摘 → 主張」の順に1〜2文でまとめる。", "字数と、本文にない内容がないかを確かめる。"],
                alt=["まず筆者の主張を本文中の英文1文（下線部など）で特定し、それを日本語にしてから根拠を加える方法もある。"],
                pc=list(p["skeys"]),
                pit=["具体例を要旨に入れて字数を使ってしまう。", "第1段落の一般的な見方を筆者の主張と取り違える。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

@gen("error_correction", 5, ["common_error", "written_reasoning"])
def d_trans_err(r):
    s = r.choice(SENT)
    wrong, why, typ, where = r.choice(s["wrongs"])
    return desc(f"次の英文を和訳する問題で、ある生徒は次のように答えた。\n{s['en']}\n［ある生徒の解答］\n{wrong}\nこの訳の誤りを指摘し、正しい訳を書きなさい。",
                f"誤り：{why}　正しい訳：{s['ok']}",
                f"ポイント：{s['pt']}。誤りの箇所（{where}）の構文・語の意味を確かめて訳し直す。",
                [("誤りの箇所を特定している", 2), ("誤りの理由を構文・語の意味に即して説明している", 2), ("正しい訳を書いている", 2)], d=3, p=6, lines=5,
                ap="生徒の訳を英文と1語ずつ対応させ、否定の範囲・比較の向き・倒置・修飾関係のどこで食い違っているかを探す。",
                steps=["英文の S・V と構文を確認する。", f"生徒の訳と英文を照合し、食い違う箇所を見つける：{where}。", f"誤りの理由：{why}", f"正しい訳：{s['ok']}"],
                alt=["生徒の訳を英語に戻すとどんな英文になるかを考え、原文との違いから誤りを確かめる。"],
                pc=[("誤りの箇所", 2), ("誤りの理由", 2), ("正しい訳", 2)],
                pit=["誤りの箇所だけを直し、ほかの箇所の構文を確かめない。"],
                err=dict(sol=wrong, step=where, type=typ, tempt=TEMPT[typ], fix=s["ok"]))


@gen("error_correction", 5, ["common_error", "written_reasoning"])
def d_explain_err(r):
    p, k, u = r.choice(ulist("exp"))
    wrong, why, typ = r.choice(u["bad"])
    tempt = {"interpretation": "下線部を正確に訳せば説明になると考え、指示語・抽象表現の中身を本文から補う手間を省いたため。",
             "logic": "下線部の近くにある具体例や結果の文を、下線部の内容そのものと取り違えたため。",
             "concept": "下線部の構文（否定・比較）の意味を取り違えたまま説明を組み立てたため。"}[typ]
    return desc(f"{head(p)}\n{u['q']}\nこの問いに、ある生徒は次のように答えた。\n［ある生徒の解答］\n{wrong}\nこの解答の問題点を指摘し、適切な解答を書きなさい。（下線部({k})：{u['text']}）",
                f"問題点：{why}　適切な解答：{u['model']}",
                "内容説明では、指示語・抽象表現の中身を本文で具体化し、下線部の論理を保って説明する。",
                [("解答の問題点を的確に指摘している", 2), ("指示内容・論理を正しく具体化した解答を書いている", 3), ("説明の形（～ということ。など）が整っている", 1)], d=4, p=6, lines=6, stim=pstim(p),
                ap="生徒の解答に「本文から補った語句」があるか、下線部の否定・比較の向きと矛盾していないかを確かめる。",
                steps=["下線部の構文と、具体化が必要な語句を確認する。", f"生徒の解答の問題点を見つける：{why}", "本文から中身を補い、下線部の論理を保って書き直す。", f"適切な解答：{u['model']}"],
                alt=["模範解答の要素（採点ポイント）を箇条書きにし、生徒の解答に含まれている要素・欠けている要素を表にして比べる。"],
                pc=[("問題点の指摘", 2), ("適切な解答", 3), ("説明の形", 1)],
                pit=["生徒の解答の日本語の不自然さだけを直し、内容の欠落に気づかない。"],
                err=dict(sol=wrong, step=f"下線部({k})の説明", type=typ, tempt=tempt, fix=u["model"]))


GENERATORS = [a_function, a_translation_mc, a_main_verb, a_referent, a_word_sense,
              b_translate, b_ref_desc, b_underline_mc, b_reason_mc,
              c_translate, c_explain, c_summary,
              d_trans_err, d_explain_err]
