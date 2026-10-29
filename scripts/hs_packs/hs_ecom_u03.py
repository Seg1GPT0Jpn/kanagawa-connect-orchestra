"""単元パック：英語コミュニケーションⅡ・Ⅲ　対話・スピーチ・講義の聞き取りと発信。

音声教材はないため、聞き取りの素材はすべて印刷したスクリプト（listening_script）として示す。
授業では教師がスクリプトを読み上げる（対話・スピーチは1回、講義は2回が目安）。読み上げができない場合は、
生徒がスクリプトを1回だけ通して読んでから設問に答えるなど、聞き取りに近い条件で取り組ませる。
対話・講義・スピーチはすべてこのパックのためのオリジナル英文（人名・場面は架空）。
"""
import zlib

from banks._common import desc, mc, stim, table
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem,
                         tp)

UNIT_ID = "HS-ECOM-U03"

NOTE = "（教師が読み上げる。音声がない場合はスクリプトとして読む）"


def lstim(id, content, title):
    return stim(id, content, "listening_script", f"{title}{NOTE}", source="オリジナル")


# ======================================================================
# 授業プリント
# ======================================================================

EX_DIALOG = ("Aya: The committee wants us to print 500 copies of the festival guide by Friday.\n"
             "Ben: Five hundred? The print shop already told us they're fully booked this week.\n"
             "Aya: Then maybe we could print some at school and post the rest online?\n"
             "Ben: That would work. I'll ask the teacher about using the school printer.")

LESSON = lesson(
    goals=["対話を聞いて、話し手の最終的な決定と、間接的な発話（遠回しな断り・反語・控えめな同意）の意図を状況から推論できる。",
           "講義を聞いて、構成の合図（First / Another / However / So）を手がかりにワークシートへ要点をメモし、講師の主張と限定をとらえられる。",
           "意見を述べるスピーチの構成（主張 → 理由 → 予想される反論 → 再反論 → 結論）を聞き取り、同じ構成で自分の意見を英語で述べられる。",
           "丁寧な反対・聞き返し・譲歩・控えめな提案などのやりとりの表現を、相手と場面に合わせて使い分けられる。"],
    duration=50,
    readiness=["英作文で主張・理由・具体例・結論の構成で意見文を書ける（HS-ENG-U10）。",
               "助動詞（could / might / would）を使った丁寧な依頼・推量の表現を理解している（HS-ENG-U03）。",
               "論説文で譲歩と主張を区別して読める（HS-ECOM-U01）。"],
    flow=[("導入：言葉どおりに受け取ると誤る", 5, "Then what are we standing here for? の意図を考えさせ、字義と意図の違いに気づかせる"),
          ("対話の聞き取りと発話の意図", 12, "状況 → 字義 → 矛盾 → 意図の4段階で推論する（例題1）"),
          ("講義の要点把握", 13, "構成の合図とワークシートのメモ（記号・略語）で要点と限定をとらえる（例題2）"),
          ("意見を述べる発話とやりとりの表現", 15, "スピーチの5つの部分と、機能別のやりとりの表現を練習する（例題3）"),
          ("まとめと確認", 5, "確認問題3問、問題プリントの課題指示")],
    sections=[
        intro("in1", "聞き取りは「推論」、発信は「構成」",
              "高校3年の聞き取りでは、話し手が考えを遠回しに伝えたり、講師が主張を慎重に限定したりする英語を扱う。聞こえた語をそのまま答えにすると誤ることが多い。一方、発信では、意見を言うだけでなく、予想される反論に答え、相手との関係に合った表現を選ぶ力が求められる。この単元では、聞いた英語の構成を読み取る力と、同じ構成で自分の英語を組み立てる力を、表裏一体のものとして身につける。",
              bullets=["対話：最初に出た案ではなく、最後に合意した内容と、発話の本当の意図を答える。",
                       "講義：構成の合図で区切り、要点だけを記号でメモする。講師の may / seem / still debate は「限定」の合図。",
                       "スピーチ：Some people say … の後ろは予想される反論、However / But の後ろは再反論。",
                       "やりとり：内容が正しくても、表現が直接的すぎると失礼に響く。"],
              points=[tp("Then what are we standing here for? を板書し、「本当に理由を尋ねているのか」を問う。", ask="この発話に Because … と答えるのは適切か。",
                         expect="適切ではない。「ここに立っている場合ではない（早く行こう）」という促しである。", timing="導入の冒頭"),
                      tp("スクリプトは解答・解説編にだけ載っていることを伝え、まず聞いて（または1回だけ読んで）答え、後でスクリプトで根拠を確かめる流れを徹底する。")]),
        definition("df1", "聞き取りの3段階と講義の合図",
                   "聞き取りは、①先読み（設問と選択肢・ワークシートの見出しから、何を聞き取るかを決める）、②メモ（構成の合図で区切り、要点を記号・略語で書く）、③照合（選択肢の言いかえとメモを照らし合わせる）の3段階で行う。",
                   bullets=["導入の合図：Today I'd like to talk about … / Have you ever … ?",
                            "列挙の合図：First / Second / Another point is / A second reason is",
                            "転換・限定の合図：However / But / Of course … / It is important to understand the limits",
                            "結論の合図：So / In short / The story shows … / What this means is …",
                            "メモの記号：↑（増加）↓（減少）→（結果）×（否定・欠点）？（議論中）＝（定義）"],
                   conditions=["講義の具体例や数値はメモの補足にとどめ、見出しには要点（理由・利点・限界など）を書く。",
                               "講師が may / seem / suggest / still debate と言った内容は、断定せずに「？」をつけてメモする。"],
                   points=[tp("講義の最初の30秒だけを読み上げ、ワークシートの見出しを生徒自身に予測させる。", caution="すべてを書き取ろうとして、次の要点を聞き逃す生徒が多い。1つの欄は5語以内でメモさせる。")]),
        theorem("th1", "やりとりの表現と発話の意図",
                "丁寧な反対：I see your point, but … / With all due respect, …　聞き返し・確認：Sorry, I didn't quite catch … / Just to make sure, you mean … ?　譲歩：Admittedly … / I'll grant you that …　控えめな提案：How about …? / It might be worth …ing / Perhaps we could …　発言の申し出：Sorry to interrupt, but … / May I add something?",
                ["発話の意図は、字義（文の形）ではなく、状況の中で何をしようとしているか（依頼・断り・促し・同意）で決まる。",
                 "遠回しな断りは「理由＋代案」の形をとることが多い（I'd love to, but … Maybe next time?）。",
                 "Would you mind …? に応じるときは、「気にしない」の向きで答える（Not at all.）。"],
                body="英語の会話では、相手の面子（立場・気持ち）を傷つけないように、反対や依頼を和らげる表現が多く使われる。聞き手はその和らげの表現の奥にある意図を推論し、話し手は相手との関係（友人・先生・初対面の人）に合わせて表現を選ぶ。",
                points=[tp("同じ反対の内容を「You are wrong.」「I see your point, but …」の2通りで言わせ、聞き手としての印象の違いを話し合わせる。",
                           ask="先生に締め切りの延長を頼むとき、I want you to extend the deadline. が不適切なのはなぜか。", expect="want you to は相手への要求として直接的すぎる。Would it be possible to …? などで和らげる。")]),
        derivation("dv1", "意図の推論と意見スピーチの組み立て（なぜその手順なのか）",
                   ["① 状況を確かめる：誰と誰が、どんな関係で、何を決めようとしているか。意図は状況の中でしか決まらないからである。",
                    "② 字義を確かめる：文の形（疑問文・平叙文）と言葉どおりの意味を確認する。",
                    "③ 矛盾を探す：字義どおりに受け取ると状況と合わない点（理由を尋ねる場面ではないのに Why …? と言うなど）を探す。",
                    "④ 意図を決める：矛盾を解消する解釈（促し・断り・同意）を選び、直後の相手の反応（OK / Sure / Then …）で確かめる。",
                    "⑤ スピーチの組み立て1：主張を最初に述べ（Today I'd like to argue that …）、理由を2つ First / Second で示す。聞き手は一度しか聞けないので、合図で構成を見せる必要がある。",
                    "⑥ スピーチの組み立て2：予想される反論を Some people say … で自分から取り上げ、I understand that concern. However, … で再反論する。反論を先に処理すると、聞き手の疑問を残さずに主張を受け入れてもらいやすい。",
                    "⑦ スピーチの組み立て3：In short / So で主張をくり返し、聞き手への呼びかけ（I hope … / Let's …）で締める。"],
                   body="聞き取りで「反論 → 再反論」の構成に気づける生徒は、自分のスピーチでも同じ構成を使える。逆に、自分で反論を想定して話す練習をすると、聞き取りでも Some people say … の後ろを主張と取り違えなくなる。",
                   points=[tp("手順⑥を、例題3のスピーチの Some people say … と However … に色分けの線を引かせて確認する。",
                              ask="Some people say … の文は、話し手の主張か。", expect="主張ではない。話し手が予想する反論で、However の後ろで答えている。", timing="手順⑥の説明時")]),
        example("ex1", "例題1　対話の最終決定と発話の意図",
                f"次の対話を聞き、(1) 2人は案内冊子をどう準備するか、(2) Ben の Five hundred? の意図を答えなさい。\n{EX_DIALOG}",
                ["委員会の指示：金曜までに500部印刷。", "Ben の Five hundred? は数を聞き返しているのではなく、印刷所が今週は予約でいっぱいだと続けて、無理だと伝えている。",
                 "Aya の代案：一部を学校で印刷し、残りはオンラインで公開。", "Ben の That would work. で合意。"],
                "(1) 一部を学校で印刷し、残りはオンラインで公開する。(2) 500部を印刷所で金曜までに用意するのは難しいという懸念を示している。",
                thinking="Five hundred? は形は疑問だが、直後に理由（fully booked）が続くので、驚きと懸念の表明。最終決定は That would work. の直前の案。",
                points=[tp("(2) を「数を確認している」と答えた生徒に、Ben が次に何を言っているかを確認させる。")],
                misconceptions=[("Five hundred? は数を確かめる質問である。", "直後の理由とあわせて、難しいという懸念を伝えている"),
                                ("最初に出た「500部印刷する」が答えである。", "代案（学校で一部印刷＋オンライン）に That would work. で合意している")]),
        example("ex2", "例題2　講義のメモ",
                "講義の一部：“The placebo effect is a major reason why new medicines are tested carefully. In a typical trial, one group of patients receives the real drug and another receives a placebo. Only if the real drug works clearly better than the placebo can we say it is effective.” をワークシート（見出し：Use in medicine）に5語以内でメモしなさい。また、Only if … can we say … の意味を説明しなさい。",
                ["見出し Use in medicine に対応する要点は「新薬をプラセボと比べて試験する」。", "メモ例：new drug vs placebo → test（記号で比較を表す）。",
                 "Only if A can we say B は倒置で「A の場合に限って B と言える」。"],
                "メモ：new drug vs placebo（新薬とプラセボを比べる）　意味：本物の薬がプラセボよりはっきり効く場合に限って、その薬は効果があると言える。",
                thinking="具体的な手順（2つのグループ）は補足で、見出しの要点は「比較して試験する」こと。",
                points=[tp("メモを英語の語句と記号で書かせ、日本語の文で書き取ろうとする生徒には「5語以内」の制限を守らせる。", ask="メモを文で書くと何が困るか。",
                           expect="書いている間に次の要点を聞き逃す。")]),
        example("ex3", "例題3　意見を述べる発話",
                "「高校生にボランティア活動を義務づけるべきか」について、主張・理由・予想される反論・再反論・結論の5つの部分を含む英語のスピーチ（50語程度）を作りなさい。",
                ["主張：I believe volunteer work should be part of every high school student's schedule.", "理由：First, students learn to work with people of different ages.",
                 "反論：Some people say that students are already too busy.", "再反論：I understand that concern. However, even a few hours a term can make a difference.",
                 "結論：So, let's give every student the chance to help their community."],
                "I believe volunteer work should be part of every high school student's schedule. First, students learn to work with people of different ages. Some people say students are already too busy. I understand that concern. However, even a few hours a term can make a difference. So, let's give every student that chance.（50語）",
                thinking="反論を自分から取り上げ、I understand that concern. で受け止めてから However で答える。",
                points=[tp("ペアで1人がスピーチをし、もう1人が「主張・反論・再反論」をメモして言い返す活動を行う。", caution="反論を取り上げたまま再反論を忘れると、聞き手には反対意見を述べたように聞こえる。")]),
        board("bd1", "板書案",
              [("① 対話の推論", ["状況 → 字義 → 矛盾 → 意図", "最後の合意（That would work.）", "遠回しな断り：理由＋代案", "反語：What are we … for?", "控えめな同意：I might just do that."]),
               ("② 講義のメモ", ["先読み → メモ → 照合", "First / Another / However / So", "記号 ↑ ↓ → × ？ ＝", "may / seem / debate → ？", "1欄5語以内"]),
               ("③ 発信の型", ["主張 → 理由 → 反論 → 再反論 → 結論", "Some people say … / However …", "丁寧な反対：I see your point, but", "聞き返し：Sorry, I didn't catch", "提案：It might be worth …ing"])],
              points=[tp("③のスピーチの型は、問題プリント C のスピーチへの応答でもそのまま使うので、ノートに写させる。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("スクリプトの読み上げは、対話・スピーチは自然な速さで1回、講義は2回を目安にし、1回目は構成、2回目は細部をメモさせる。", timing="各聞き取りの前"),
               tp("意図を問う設問では、選択肢を「字義どおりの解釈」「状況に合う解釈」に分けさせ、字義どおりの選択肢が誤りの典型であることを示す。", caution="Five hundred? → 数の確認、What are we standing here for? → 理由の質問、と字義で選ぶ生徒が多い。"),
               tp("講義のワークシートの誤りは「別の見出しの内容」「講師が限定した内容の断定」「聞こえた語からの推測」の3種類が多いので、答え合わせでこの3つに分類させる。"),
               tp("スピーチへの応答を書かせるときは、相手の反論・再反論の部分に必ず触れさせ、I agree / I disagree の後に理由と、相手の論点への応答を入れさせる。", ask="話し手の再反論に納得できないとき、どう書けばよいか。", expect="I understand your point that …, but … の形で、再反論の弱点を示す。"),
               tp("やりとりの表現は、相手（友人・先生・初対面の人）と目的（依頼・反対・断り）のカードを引かせ、即興で言わせる練習を5分程度行う。")],
              misconceptions=[("疑問文の形の発話は、いつも情報を求める質問である。", "反語・促し・懸念の表明のこともある。状況と直後の反応で意図を決める"),
                              ("講師が例に挙げた内容は、ワークシートの要点として書く。", "例は補足。見出しには理由・利点・限界などの要点を書く"),
                              ("Some people say … の後ろは話し手の主張である。", "予想される反論。話し手の主張は However / But の後ろの再反論にある"),
                              ("内容が正しければ、表現の丁寧さは問題にならない。", "直接的すぎる表現（I want you to … / You are wrong.）は相手との関係を損なう")]),
        summary("sm1", "まとめ",
                ["対話は、最後に合意した内容と、状況から推論した発話の意図を答える（状況 → 字義 → 矛盾 → 意図）。",
                 "講義は、構成の合図で区切り、見出しに要点を記号でメモする。may / seem / still debate は限定として「？」をつける。",
                 "意見を述べるときは、主張 → 理由 → 予想される反論 → 再反論 → 結論の順に組み立て、合図の表現で構成を聞き手に示す。",
                 "やりとりでは、丁寧な反対・聞き返し・譲歩・控えめな提案などの表現を、相手と場面に合わせて選ぶ。"]),
        check("ck1", "確認問題",
              [("友人に誘われて断るとき、理由と代案を含めて英語で答えなさい（誘い：Want to come to the movies on Saturday?）。", "I'd love to, but I have a club match on Saturday. How about Sunday? など"),
               ("講義で “Scientists still debate how …” と聞いたとき、メモではどう扱うか。", "まだ結論の出ていない内容として「？」をつけ、断定しない。"),
               ("Do you mind waiting a few minutes? に快く応じる英語を答えなさい。", "Not at all. / No, not at all. Take your time. など（mind を否定する向きで答える）")]),
    ])


# ======================================================================
# 対話（聞き取り）
# ======================================================================

DIALOGS = [
    dict(key="ELEC", title="Choosing an Elective",
         script="Hana: Have you decided which elective to take next term? I'm torn between Environmental Science and Media Studies.\n"
                "Leo: I'm going for Media Studies. The teacher lets you make a short film as the final project instead of taking an exam.\n"
                "Hana: That sounds fun, but I've heard it takes a lot of time outside class. With the entrance exams coming up, I can't afford to spend every weekend editing videos.\n"
                "Leo: Fair point. Environmental Science has field trips, though. Aren't those on Saturdays too?\n"
                "Hana: Only twice a term, and they count toward the grade, so there's hardly any homework. I think that settles it.\n"
                "Leo: Well, if you change your mind, the deadline for switching is the end of next week.",
         qs=[("Hana が選ぶ可能性が最も高い選択科目はどれか。", "Environmental Science",
              [("Media Studies", "Leo が選ぶ科目で、Hana は授業外の時間がかかることを心配している。"), ("Both Environmental Science and Media Studies", "両方を取るという話は出ていない。"),
               ("Neither; she will decide at the end of next week", "Leo が変更の締め切りを伝えただけで、Hana は I think that settles it と決めている。")]),
             ("Hana が Media Studies について心配している点はどれか。", "It may take a lot of time outside class.",
              [("The final exam is very difficult.", "Media Studies は試験の代わりに短い映画を作る。"), ("Its field trips are held on Saturdays.", "土曜の校外学習は Environmental Science の話である。"),
               ("The teacher is said to be very strict.", "先生の厳しさについては話していない。")])],
         intent=("Hana の I think that settles it. の意図として最も適切なものはどれか。", "Environmental Science を選ぶことに決めたと伝えている。",
                 [("Media Studies を選ぶことに決めたと伝えている。", "直前で、Environmental Science は校外学習が少なく宿題もほとんどないと述べ、その流れで決めている。"),
                  ("まだ迷っているので、来週末まで考えると伝えている。", "settle は「決着をつける」。迷いが解消したことを表している。"),
                  ("Leo に Environmental Science を選ぶよう勧めている。", "Hana 自身の選択についての発言で、Leo への勧めではない。")],
                 "settle を「落ち着く・後回しにする」のような意味で受け取り、直前の Hana の発言の流れを確かめなかった。"),
         reply=("あなたが Leo だとして、Hana の判断を尊重しつつ、Media Studies のよさを控えめにもう一度伝える発話を英語で書きなさい。",
                "That makes sense with the exams coming up. But if you ever want to try filmmaking, maybe we could make a short video together after the exams.")),
    dict(key="PRES", title="Planning the Group Presentation",
         script="Kai: So, for our presentation on renewable energy, I was thinking each of us could cover one type: solar, wind, and geothermal.\n"
                "Mia: That would be easy to divide, but I'm worried it'll sound like three separate presentations. What if we organized it around a question instead, like \"Which energy source suits our city best?\"\n"
                "Kai: Hmm, that's more interesting, but doesn't it mean we'd all have to research every type?\n"
                "Mia: Not necessarily. We could still each research one type, and then meet to compare them using the same criteria: cost, reliability, and space.\n"
                "Kai: Oh, I see. So the research is divided, but the conclusion is shared. Let's do that. I'll draft the criteria table tonight.\n"
                "Mia: Great. I'll message Sota so he knows the plan.",
         qs=[("グループは発表をどのように構成することにしたか。", "Around one question, comparing the energy sources with the same criteria",
              [("As three separate talks on solar, wind, and geothermal energy", "Kai の最初の案で、Mia が別々の発表のように聞こえると心配して変更された。"),
               ("With every member researching all three types of energy", "Kai の心配だが、Mia が Not necessarily と答え、調べる分担は残すことになった。"),
               ("Around the cost of solar energy only", "費用は比較の基準の1つで、太陽光だけを扱うわけではない。")]),
             ("Kai が今夜することはどれか。", "Make a draft of the table of criteria.",
              [("Send a message to Sota about the plan.", "Sota に連絡するのは Mia である。"), ("Research all three energy sources.", "調べるのは1人1種類のままである。"),
               ("Choose the best energy source for the city.", "結論は全員で比べて出すことになっている。")])],
         intent=("Mia の Not necessarily. の意図として最も適切なものはどれか。", "全員がすべての種類を調べなくても、問いを中心にした発表はできると伝えている。",
                 [("全員がすべての種類を調べる必要があると認めている。", "necessarily を否定する形で、「必ずしもそうではない」と Kai の心配を打ち消している。"),
                  ("問いを中心にする案を取り下げている。", "直後に、分担を残したまま比べる方法を示して、自分の案を続けている。"),
                  ("Kai の最初の案に賛成している。", "最初の案（3人が別々に発表）には、別々の発表に聞こえると心配を示している。")],
                 "Not を聞いて「いいえ（あなたの言う通りではない）＝案をやめる」と短絡し、直後の説明を聞かなかった。"),
         reply=("あなたが Sota だとして、Mia からの連絡に返信し、計画に賛成したうえで、比較の基準を1つ加えることを控えめに提案する発話を英語で書きなさい。",
                "Sounds like a great plan. Could we also add the effect on the environment as a criterion? I think our audience would be interested in that.")),
    dict(key="LIBR", title="A Request at the Library",
         script="Student: Excuse me, I'd like to borrow this book on climate history, but the label says \"Reference Only.\"\n"
                "Librarian: Right. Reference books have to stay in the library, I'm afraid, because many students need them for their reports.\n"
                "Student: I see. The thing is, I need it for an essay that's due on Monday, and the library is closed this weekend.\n"
                "Librarian: Hmm. I can't let you take it home, but you're welcome to photocopy up to two chapters. The copier is next to the entrance.\n"
                "Student: Two chapters should be enough, actually. The parts I need are chapters three and five.\n"
                "Librarian: Then you're all set. Just bring the book back to this desk when you're done.",
         qs=[("生徒が次にする可能性が最も高いことはどれか。", "Copy two chapters of the book.",
              [("Take the book home for the weekend.", "司書は持ち帰りを認めていない。"), ("Come back to the library on Saturday.", "図書館は今週末は閉まっている。"),
               ("Ask his teacher to change the deadline.", "締め切りの変更は話題になっていない。")]),
             ("生徒がその本を借りられない理由はどれか。", "It has to stay in the library because many students need it.",
              [("Someone else has already borrowed it.", "ほかの人が借りているとは言っていない。"), ("The library is closed this weekend.", "これは生徒が本を必要とする事情で、借りられない理由ではない。"),
               ("He has not returned some other books.", "返却の遅れは話題になっていない。")])],
         intent=("司書の I can't let you take it home, but you're welcome to photocopy up to two chapters. の意図として最も適切なものはどれか。", "持ち出しは断るが、代わりの方法を提案している。",
                 [("特別に本を持ち帰ることを許可している。", "I can't let you take it home（持ち帰らせることはできない）と断っている。"),
                  ("コピーも禁止されていると伝えている。", "you're welcome to photocopy（どうぞコピーしてください）とコピーを勧めている。"),
                  ("月曜日までに返すなら貸すと言っている。", "返却の期限つきで貸すとは言っていない。")],
                 "生徒の事情（週末は閉館）に応じた発言なので、特別に許可したのだろうと思いこみ、I can't let you … を聞き落とした。"),
         reply=("あなたが生徒だとして、コピーを終えた後、司書にお礼を述べ、ほかの章も必要になった場合にどうすればよいかを丁寧に尋ねる発話を英語で書きなさい。",
                "Thank you so much for your help. If I find that I need another chapter later, would it be all right to come back and copy it next week?")),
    dict(key="ESSY", title="Feedback on an Essay",
         script="Ms. Lee: I read your essay on school uniforms. Your argument is clear, and I like the example from your sister's school.\n"
                "Ryo: Thank you. Is there anything I should change before I hand in the final version?\n"
                "Ms. Lee: Well, you write that \"most students\" dislike uniforms. Where does that come from?\n"
                "Ryo: Oh... that's just from talking to my friends.\n"
                "Ms. Lee: Then I'd be careful with that phrase. Either find a survey or say \"many of my friends.\" Otherwise, a reader might wonder how you know.\n"
                "Ryo: That makes sense. I'll check whether the student council has done a survey.",
         qs=[("Ms. Lee が指摘している問題点はどれか。", "A claim in the essay is not supported by evidence.",
              [("The essay does not have a clear argument.", "Ms. Lee は主張が明確だと述べている。"), ("The example from his sister's school is not relevant.", "Ms. Lee はその例を気に入っている。"),
               ("The essay is too long.", "長さについては話していない。")]),
             ("Ryo がまずしようとしていることはどれか。", "Find out whether the student council has survey data.",
              [("Remove the example about his sister's school.", "その例は評価されており、削除の話は出ていない。"), ("Ask his friends about uniforms again.", "友人に聞くことが根拠として弱いと指摘された。"),
               ("Hand in the essay without any changes.", "That makes sense と指摘を受け入れ、調べると言っている。")])],
         intent=("Ms. Lee の Where does that come from? の意図として最も適切なものはどれか。", "「ほとんどの生徒」という主張の根拠を尋ねている。",
                 [("その表現をどこで習ったかを尋ねている。", "直後のやりとり（友人と話しただけ → 調査を探すか表現を変える）から、表現の出どころではなく主張の根拠を問うている。"),
                  ("姉の学校の例の出どころを尋ねている。", "that は直前の \"most students\" dislike uniforms を指している。"),
                  ("その主張に賛成していることを伝えている。", "根拠を問い、表現に注意するよう助言しており、賛成の表明ではない。")],
                 "come from を「（語句を）どこから持ってきたか」と字義どおりに受け取り、論拠を問う表現だと気づかなかった。"),
         reply=("あなたが Ryo だとして、生徒会に、制服についての調査結果があるかを丁寧に尋ねるメッセージを英語で書きなさい。",
                "Hello, I'm writing an essay on school uniforms. Would it be possible to see the results of any survey the student council has done on this topic?")),
    dict(key="TRAN", title="The Delayed Express",
         script="Woman: The announcement said the express is delayed because of strong winds. Should we wait, or take the local train?\n"
                "Man: The local stops at every station. It'll take at least forty minutes longer than the express usually does.\n"
                "Woman: But nobody knows how long the delay will be. The last time this happened, we waited over an hour.\n"
                "Man: True. And the local leaves in two minutes from Platform 3.\n"
                "Woman: Then what are we standing here for?",
         qs=[("2人がこの後とる行動として最も適切なものはどれか。", "Take the local train.",
              [("Wait for the express.", "遅れがどれだけ続くかわからず、前回は1時間以上待ったので、待たない流れになっている。"), ("Take a bus instead.", "バスは話題になっていない。"),
               ("Go back home.", "帰宅する話は出ていない。")]),
             ("女性が急行を待ちたくない理由はどれか。", "Nobody knows how long the delay will last.",
              [("The local train is faster than the express.", "各駅停車は少なくとも40分長くかかる。"), ("The express has been canceled.", "急行は運休ではなく遅れている。"),
               ("She wants to stop at every station.", "各駅に止まることは欠点として述べられている。")])],
         intent=("女性の Then what are we standing here for? の意図として最も適切なものはどれか。", "すぐに各駅停車に乗ろうと促している。",
                 [("ここで待っている理由を本当に知りたがっている。", "形は疑問文だが、2分後に出る各駅停車の話を受けた反語で、「ここに立っている場合ではない」という意味である。"),
                  ("急行を待つべきだと主張している。", "遅れの長さがわからないと述べており、待つことには否定的である。"),
                  ("ホームの番号を確かめたがっている。", "番号は男性がすでに伝えている。")],
                 "疑問文の形なので情報を求める質問だと考え、直前の「2分後に出る」という状況との関係を考えなかった。"),
         reply=("あなたが女性だとして、各駅停車に乗った後、待ち合わせの相手に到着が遅れることを知らせ、待たせることを詫びるメッセージを英語で書きなさい。",
                "Sorry, the express was delayed by strong winds, so we're on the local train. We'll be about forty minutes late. Please don't wait outside in the cold.")),
    dict(key="DEBT", title="Joining the Debate Team",
         script="Man: Did you see the poster? The debate team is looking for new members.\n"
                "Woman: I did. I'd love to improve my English, but I'm not sure I'd be any good at arguing with people.\n"
                "Man: Debate isn't really about arguing, though. You often have to defend a side you don't agree with, so it's more about listening carefully and finding weak points in the other team's logic.\n"
                "Woman: Hmm, I hadn't thought of it that way. Do they practice every day?\n"
                "Man: Just Tuesdays and Thursdays. You could come and watch on Thursday before you decide.\n"
                "Woman: I might just do that.",
         qs=[("男性によると、ディベートで主に大切なことは何か。", "Listening carefully and finding weak points in the other side's logic",
              [("Arguing for your own personal opinions", "自分が賛成しない側を弁護することも多いと述べている。"), ("Speaking English as fast as possible", "話す速さについては述べていない。"),
               ("Winning arguments with your friends", "ディベートは人と言い争うことではないと述べている。")]),
             ("女性がこの後する可能性が最も高いことはどれか。", "Watch a practice on Thursday.",
              [("Join the team on Tuesday without watching.", "まず見学してから決めるよう勧められ、それに応じている。"), ("Decide not to join the team.", "I might just do that. で見学に前向きである。"),
               ("Make a new poster for the debate team.", "ポスター作りの話は出ていない。")])],
         intent=("女性の I might just do that. の意図として最も適切なものはどれか。", "木曜日に見学に行くつもりであることを控えめに伝えている。",
                 [("見学には行かないと遠回しに断っている。", "might は控えめな言い方だが、just do that（そうしてみる）と見学に応じている。"),
                  ("すぐに入部すると決めている。", "that は「木曜日に見学してから決める」ことを指しており、入部を決めたわけではない。"),
                  ("男性に一緒に入部するよう頼んでいる。", "依頼の表現は使われていない。")],
                 "might（かもしれない）を聞いて「行かない可能性が高い＝断り」と受け取り、just do that が何を指すかを確かめなかった。"),
         reply=("あなたが女性だとして、木曜日の練習を見学した後、ディベート部の部長に、入部したい気持ちと不安な点を伝え、質問する発話を英語で書きなさい。",
                "Thank you for letting me watch. I'd like to join, but I'm a little worried about speaking in front of others. Is that common for new members?")),
]


def dstim(dl):
    return lstim(f"EC3D-{dl['key']}", dl["script"], f"対話“{dl['title']}”")


# ======================================================================
# 講義（聞き取り・ワークシート）
# ======================================================================

LECTURES = [
    dict(key="BEES", title="How Honeybees Share Directions",
         text="Today I want to talk about one of the most remarkable forms of communication in the animal world: the honeybee's waggle dance. When a worker bee finds a good source of food, she returns to the hive and performs a dance on the vertical surface of the honeycomb. She runs in a straight line while shaking her body from side to side, then circles back and repeats the run, again and again.\n"
              "The dance carries two key pieces of information. First, the direction of the straight run tells the other bees which way to fly. The angle of the run, measured from straight up, matches the angle between the food and the sun. So if the bee runs straight up, the food is in the direction of the sun. Second, the length of the run tells them how far away the food is: the longer she waggles, the farther they need to fly.\n"
              "What makes this so impressive is that the bees are translating a direction relative to the sun into a direction relative to gravity, in the darkness of the hive. And because the sun moves across the sky during the day, bees seem to adjust their dances to account for this.\n"
              "Scientists still debate how much the other bees rely on the dance itself and how much on smell. But the waggle dance remains a striking example of how a small insect can communicate abstract information.",
         rows=[("Where the dance is done", "On the vertical surface of the honeycomb"), ("Angle of the run", "Direction of the food relative to the sun"),
               ("Length of the run", "Distance to the food"), ("Running straight up", "Food is in the direction of the sun"),
               ("Still debated", "How much bees rely on the dance and on smell")],
         fake=["The type of flower the food comes from", "How many bees should fly together"],
         main="Honeybees use the waggle dance to tell other bees both the direction and the distance of food.",
         main_wrong=[("Bees always fly straight toward the sun to find food.", "太陽の方向にえさ場があるのは、まっすぐ上に進むダンスの場合だけである。"),
                     ("Scientists have completely explained how bees find food.", "においの役割など、まだ議論されている点があると述べている。"),
                     ("The dance shows which flowers smell the sweetest.", "講義で述べられていない内容である。")],
         trues=["The length of the waggle run is related to the distance to the food.", "Bees appear to change their dances as the sun moves across the sky."],
         falses=[("The dance is performed outside the hive in the sunlight.", "巣の中の暗い場所で、垂直な巣板の上で行うと述べている。"),
                 ("A longer waggle run means the food is closer.", "長く体を振るほど遠くまで飛ぶ必要があると述べており、逆である。"),
                 ("Scientists agree that smell plays no role at all.", "においにどの程度頼るかはまだ議論されていると述べている。")],
         org=("ダンスの様子 → ダンスが伝える2つの情報（方向・距離）→ 驚くべき点 → まだ議論されている点",
              [("問題提起 → 原因の分析 → 解決策 → 結論", "原因や解決策を述べる講義ではなく、ダンスのしくみを説明している。"),
               ("2つの説の比較 → 講師が支持する説", "においの説はまだ議論されていると最後に触れるだけで、説の比較は中心ではない。"),
               ("歴史的な経緯 → 現在の課題 → 将来の予測", "歴史や将来の予測は述べられていない。")]),
         q2=("講師が、断定を避けてまだ結論が出ていないこととして述べている内容はどれか。", "仲間のハチがダンスとにおいのどちらにどの程度頼っているか",
             [("直進の向きの角度が、太陽に対するえさ場の方向を表すこと", "講師は The angle of the run … matches … と断定的に説明している。"),
              ("ダンスが巣板の垂直な面で行われること", "講義の冒頭で断定的に述べている事実である。"),
              ("直進の長さが、えさ場までの距離を表すこと", "Second, the length of the run tells them … と断定的に説明している。")]),
         summary="ミツバチは巣の中の垂直な巣板の上でダンスを行い、直進の向きの角度で太陽に対するえさ場の方向を、直進の長さでえさ場までの距離を仲間に伝える。においの役割にはまだ議論があるが、小さな昆虫が抽象的な情報を伝える見事な例である。",
         skeys=[("方向（太陽に対する角度）の伝え方を述べている", 3), ("距離（直進の長さ）の伝え方を述べている", 3), ("においの役割はまだ議論されていることに触れている", 2)]),
    dict(key="VERT", title="Farms That Grow Up, Not Out",
         text="Most of us picture farms as wide fields under an open sky. But in some cities, lettuce and herbs are now being grown indoors, on shelves stacked one above another inside large buildings. This is called vertical farming.\n"
              "Supporters point to several advantages. Because the plants are grown indoors, crops can be produced all year round, regardless of the weather. Many vertical farms grow plants without soil, feeding the roots with water that contains nutrients, and much of this water is collected and reused, so they can use far less water than traditional farms. And since the farms can be built in cities, food does not have to travel long distances to reach consumers.\n"
              "However, there is a significant drawback. Sunlight is free, but the LED lights that replace it are not. Lighting, along with heating and cooling, uses a great deal of electricity, which makes vertical farming expensive and, depending on how the electricity is produced, not always better for the environment. This is one reason why most vertical farms grow leafy greens, which grow quickly and sell for a good price, rather than staple crops like wheat or rice.\n"
              "So, vertical farming is not going to replace traditional agriculture. But as lighting becomes more efficient and more electricity comes from renewable sources, it may become a valuable way to grow certain crops close to where people live.",
         rows=[("Definition", "Growing crops indoors on stacked shelves"), ("Advantage 1", "Crops can be grown all year round"),
               ("Advantage 2", "Far less water is used because it is reused"), ("Advantage 3", "Food travels shorter distances"),
               ("Drawback", "Lighting and temperature control use a lot of electricity"), ("Typical crops", "Leafy greens that grow quickly")],
         fake=["Wheat and rice grown in large amounts", "Crops grown without any light"],
         main="Vertical farming has real advantages, but because it uses so much energy, it will grow only certain crops alongside traditional farms.",
         main_wrong=[("Vertical farms will soon replace traditional farms.", "講師は従来の農業に置きかわることはないと述べている。"),
                     ("Vertical farms are always better for the environment.", "電力の作り方によっては必ずしも環境によくないと述べている。"),
                     ("LED lights are the cheapest way to grow plants.", "LED の照明は電力を多く使い、費用がかかると述べている。")],
         trues=["Many vertical farms reuse the water they give to plants.", "Most vertical farms grow leafy greens rather than wheat or rice."],
         falses=[("Vertical farms depend on good weather.", "屋内なので天候に関係なく一年中生産できると述べている。"),
                 ("Vertical farms need very little electricity.", "照明や冷暖房に多くの電力を使うと述べている。"),
                 ("The speaker believes vertical farming has no future.", "照明の効率化や再生可能エネルギーの普及で、価値ある方法になるかもしれないと述べている。")],
         org=("定義 → 3つの利点 → 大きな欠点 → 限定つきの見通し",
              [("問題提起 → 原因 → 解決策 → 結論", "原因を分析する講義ではなく、新しい農法の利点と欠点を比べている。"),
               ("欠点 → 利点 → 全面的な推奨", "利点を先に述べ、最後も「置きかわらない」と限定しており、全面的な推奨ではない。"),
               ("歴史 → 現在の広がり → 将来の予測", "農法の歴史は述べられていない。")]),
         q2=("講師が最後の段落で、may を使って慎重に述べている内容はどれか。", "将来、特定の作物を都市の近くで育てる価値ある方法になるかもしれないこと",
             [("垂直農法が従来の農業に置きかわらないこと", "is not going to replace と断定的に述べている。"),
              ("多くの垂直農場が水を集めて再利用していること", "第2段落で断定的に説明している利点である。"),
              ("照明や冷暖房に多くの電力を使うこと", "第3段落で断定的に述べている欠点である。")]),
         summary="垂直農法は屋内の棚で作物を育てる方法で、一年中生産でき、水を再利用して節約でき、輸送距離も短い。しかし照明や温度管理に多くの電力を使うので費用がかかり、育てる作物も限られる。従来の農業に置きかわるものではないが、特定の作物を都市の近くで育てる方法として価値が高まる可能性がある。",
         skeys=[("利点（一年中生産・水の節約・輸送距離）を述べている", 3), ("電力を多く使うという欠点を述べている", 3), ("置きかわらないが特定の作物で価値が高まりうるという限定つきの結論に触れている", 2)]),
    dict(key="LOAN", title="Why Languages Borrow Words",
         text="Every language borrows words from other languages. English is a good example: a large share of its vocabulary comes from French and Latin, and in recent decades it has also taken words from Japanese, such as tsunami, karaoke, and emoji.\n"
              "Why do languages borrow? The most common reason is need. When people meet a new object, food, or idea, their language may not have a word for it, and the simplest solution is to use the word that comes with it. A second reason is prestige. If a language is associated with power, learning, or fashion, speakers may borrow its words even when they already have their own. For centuries after the Norman Conquest, French was the language of the ruling class in England, and many French words entered English through law, government, and cooking.\n"
              "Borrowed words rarely stay exactly the same. They usually change to fit the sounds and grammar of the new language. Japanese speakers, for instance, add vowels to English words, so that \"strike\" becomes \"sutoraiku.\" Meanings can change, too. In Japanese, \"mansion\" usually refers to an ordinary apartment building, not a large, grand house as in English.\n"
              "Some people worry that borrowing damages a language. But history suggests the opposite: borrowing is one of the ways languages stay alive and keep up with a changing world.",
         rows=[("Example", "Tsunami, karaoke, and emoji in English"), ("Reason 1", "Need: no word for a new thing or idea"),
               ("Reason 2", "Prestige of the other language"), ("Change 1", "Sounds change to fit the new language"),
               ("Change 2", "Meanings can change"), ("Speaker's view", "Borrowing helps languages stay alive")],
         fake=["Borrowed words must keep their original spelling", "Only English borrows words from other languages"],
         main="Languages borrow words out of need and prestige, adapt them in sound and meaning, and stay alive through this process.",
         main_wrong=[("Borrowing words damages a language over time.", "講師は、歴史はその逆を示していると述べている。"),
                     ("Japanese has borrowed more words than any other language.", "講義で述べられていない比較である。"),
                     ("Borrowed words always keep their original meaning.", "mansion の例で、意味が変わることもあると述べている。")],
         trues=["French became an important language in England after the Norman Conquest.", "Japanese speakers often add vowels to words borrowed from English."],
         falses=[("English has never borrowed words from Japanese.", "tsunami、karaoke、emoji などを借りていると述べている。"),
                 ("People borrow words only when they have no word of their own.", "威信のために、自分の言語に語があっても借りることがあると述べている。"),
                 ("In Japanese, \"mansion\" usually means a large, grand house.", "日本語ではふつうの集合住宅を指すと述べている。")],
         org=("身近な例 → 借用の2つの理由 → 借用語の変化（音・意味）→ 懸念への講師の見解",
              [("問題提起 → 原因 → 解決策 → 結論", "解決策を示す講義ではない。"),
               ("借用の欠点 → 利点 → 両論の併記", "欠点を論じる部分はなく、最後に講師は懸念に反論している。"),
               ("英語の歴史 → 日本語の歴史 → 2言語の比較", "2つの言語の歴史を比べる構成ではない。")]),
         q2=("講師が最後に Some people worry that borrowing damages a language. を取り上げたのはなぜか。", "よくある懸念を示したうえで、借用は言語を生かすものだという自分の見解を述べるため",
             [("借用が言語を損なうことに同意するため", "直後に But history suggests the opposite と反論している。"),
              ("借用語を減らすよう聞き手に求めるため", "借用を減らすべきだとは述べていない。"),
              ("借用語の意味が変わる例を加えるため", "意味の変化の例（mansion）は前の段落で述べ終えている。")]),
         summary="言語は、新しい物や考えを表す語がないという必要や、相手の言語の威信から語を借りる。借りた語は新しい言語の音や文法に合わせて形を変え、意味が変わることもある。借用は言語を損なうのではなく、変化する世界に対応して言語が生き続ける方法の一つである。",
         skeys=[("借用の2つの理由（必要・威信）を述べている", 3), ("借用語が音や意味の面で変化することを述べている", 3), ("借用は言語を生かすという講師の見解に触れている", 2)]),
    dict(key="TIME", title="How Clocks Came to Agree",
         text="Today, it seems natural that the clocks in a country all show the same time. But for most of history, each town kept its own time, based on the position of the sun. When the sun was highest in the sky, it was noon. Because the sun reaches its highest point at different moments in different places, a town to the east would be a few minutes ahead of a town to the west.\n"
              "For centuries, this caused few problems, because people rarely traveled fast enough to notice. The railways changed that. In the nineteenth century, trains could carry passengers between cities in a matter of hours, and having each station use its own local time made timetables confusing and even dangerous. Railway companies began to adopt a single standard time for their lines, and over time, governments followed.\n"
              "Eventually, the world was divided into time zones, most of them one hour apart, measured from a starting line that passes through Greenwich in London. Within each zone, everyone uses the same clock time, even though it may not match the sun exactly.\n"
              "The story shows how a new technology can change something as basic as our sense of time. And today, with smartphones that adjust their clocks automatically when we land in a new country, we rarely think about the problem the railways had to solve.",
         rows=[("Before standard time", "Each town kept its own time based on the sun"), ("Why towns differed", "The sun is highest at different moments in different places"),
               ("What changed things", "Fast railway travel in the nineteenth century"), ("Problem", "Timetables became confusing and even dangerous"),
               ("Solution", "Standard time and time zones"), ("Starting line", "A line passing through Greenwich in London")],
         fake=["Clocks set by the position of the moon", "A single time zone for the whole world"],
         main="Fast railway travel made local, sun-based time impractical, which led to standard time and time zones.",
         main_wrong=[("Towns have always used the same time as one another.", "かつては各町が独自の時刻を使っていたと述べており、逆である。"),
                     ("Time zones match the position of the sun exactly everywhere.", "時間帯の時刻は太陽と正確には一致しないことがあると述べている。"),
                     ("Smartphones were the reason time zones were created.", "スマートフォンは現代の例で、標準時のきっかけは鉄道である。")],
         trues=["A town to the east used to be a few minutes ahead of a town to the west.", "Railway companies adopted standard time before many governments did."],
         falses=[("Most time zones are thirty minutes apart.", "ほとんどの時間帯は1時間ずつ離れていると述べている。"),
                 ("Local time caused serious problems long before the railways.", "鉄道以前は、速く移動しなかったので問題はほとんどなかったと述べている。"),
                 ("Clock time within a time zone always matches the sun exactly.", "太陽と正確には一致しないことがあると述べている。")],
         org=("昔の状況 → 変化のきっかけ（鉄道）→ 解決策（標準時・時間帯）→ 現代への教訓",
              [("定義 → 利点 → 欠点 → 見通し", "利点と欠点を比べる講義ではない。"),
               ("2つの説の比較 → 講師の支持する説", "説の比較は述べられていない。"),
               ("現代の問題 → 原因 → 解決策の提案", "現代の問題を解決する提案ではなく、過去の変化を説明している。")]),
         q2=("講師が最後の段落で伝えようとしていることとして最も適切なものはどれか。", "新しい技術は、時間の感覚のような基本的なものまで変えうること",
             [("スマートフォンの時計は信頼できないこと", "スマートフォンは時計が自動で合う便利な例として挙げられている。"),
              ("鉄道は今でも時刻の混乱を起こしていること", "混乱は19世紀の話で、今では意識することもないと述べている。"),
              ("時間帯の数を減らすべきであること", "時間帯の数についての提案はしていない。")]),
         summary="かつて各町は太陽の位置にもとづく独自の時刻を使っていたが、19世紀に鉄道で速く移動できるようになると、時刻表が混乱し危険にもなった。そこで鉄道会社が標準時を採用し、やがて世界はグリニッジを基準とする時間帯に分けられた。新しい技術が時間の感覚さえ変えた例である。",
         skeys=[("かつては町ごとに太陽にもとづく時刻を使っていたことを述べている", 2), ("鉄道による高速移動が混乱を生んだことを述べている", 3), ("標準時・時間帯の導入という解決に触れている", 3)]),
    dict(key="PLAC", title="The Placebo Effect",
         text="Imagine that you have a headache, and a doctor gives you a pill. You take it, and twenty minutes later you feel better. But what if the pill contained no medicine at all, just sugar? Surprisingly, this happens quite often. When people feel better after receiving a treatment that has no active ingredient, we call it the placebo effect.\n"
              "Why does it happen? One important factor is expectation. If we believe a treatment will help, we may pay less attention to our pain or feel less anxious, and that can change how we feel. Even details like the color of a pill or the confidence of the doctor seem to make a difference in some studies.\n"
              "The placebo effect is a major reason why new medicines are tested carefully. In a typical trial, one group of patients receives the real drug and another receives a placebo, and usually neither the patients nor the doctors know who is getting which. Only if the real drug works clearly better than the placebo can we say it is effective.\n"
              "It is important to understand the limits, though. A placebo may help with how we feel, such as pain, tiredness, or nausea, but it cannot shrink a tumor or cure an infection. So the placebo effect reminds us that the mind can influence the body, but it is not a replacement for real medical treatment.",
         rows=[("Definition", "Feeling better after a treatment with no active ingredient"), ("Main factor", "Expectation that the treatment will help"),
               ("Details that may matter", "The color of a pill or the doctor's confidence"), ("Use in medicine", "New drugs are compared with a placebo"),
               ("Limit", "It cannot cure an infection or shrink a tumor")],
         fake=["Placebos contain a small amount of medicine", "Doctors always tell patients who receives the placebo"],
         main="The placebo effect shows that expectations can change how we feel, which is why drugs are tested against placebos, but it cannot replace real treatment.",
         main_wrong=[("Placebos can cure most illnesses.", "感染症を治したり腫瘍を小さくしたりはできないと述べている。"),
                     ("Sugar pills are a kind of medicine.", "有効成分がないものをプラセボと呼ぶと述べている。"),
                     ("The color of a pill is the most important factor in medicine.", "一部の研究で影響が見られるという細部で、言いすぎである。")],
         trues=["In many trials, neither the patients nor the doctors know who receives the placebo.", "A placebo may reduce pain or tiredness."],
         falses=[("A placebo can cure an infection.", "感染症は治せないと述べている。"),
                 ("New drugs are tested without being compared with anything.", "プラセボと比べて試験すると述べている。"),
                 ("Expectation has no effect on how people feel.", "期待は重要な要因の一つだと述べている。")],
         org=("身近な例による導入 → 定義 → 原因 → 医学での利用 → 限界",
              [("問題提起 → 解決策 → 全面的な推奨", "最後に限界を述べており、全面的な推奨ではない。"),
               ("2つの治療法の比較 → 講師の支持する治療法", "治療法を比べる講義ではない。"),
               ("歴史 → 現在の課題 → 将来の予測", "歴史や将来の予測は述べられていない。")]),
         q2=("講師が、seem や in some studies を使って慎重に述べている内容はどれか。", "錠剤の色や医師の自信が影響すること",
             [("新薬がプラセボと比べて試験されること", "第3段落で断定的に説明している。"),
              ("プラセボで感染症を治すことはできないこと", "cannot と断定的に述べている。"),
              ("プラセボには有効成分がないこと", "定義として断定的に述べている。")]),
         summary="有効成分のない治療で体調がよくなるプラセボ効果は、治療が効くという期待などによって起こる。そのため新薬はプラセボと比べて試験される。プラセボは痛みなどの感じ方には影響しうるが、病気そのものを治すことはできず、実際の治療の代わりにはならない。",
         skeys=[("プラセボ効果の定義と、期待という要因を述べている", 3), ("新薬の試験でプラセボと比べることに触れている", 2), ("感じ方には影響するが病気は治せないという限界を述べている", 3)]),
]


def lect_stim(lc):
    return lstim(f"EC3L-{lc['key']}", lc["text"], f"講義“{lc['title']}”")


def worksheet(lc, blank=None, filled=None):
    rows = []
    for i, (lab, val) in enumerate(lc["rows"]):
        if i == blank:
            rows.append([lab, "（　①　）"])
        elif filled and i in filled:
            rows.append([lab, filled[i]])
        else:
            rows.append([lab, val])
    return table(rows, header=["Item", "Notes"], caption=f"Worksheet: {lc['title']}")


# ======================================================================
# 意見を述べるスピーチ（聞き取り）
# ======================================================================

SPEECHES = [
    dict(key="COOK", title="Every Student Should Learn to Cook",
         script="Good afternoon. Today I'd like to argue that cooking should be a required subject for every high school student. First, cooking is a basic life skill. In a few years, many of us will live on our own, and if we can't cook, we'll depend on convenience stores and fast food, which are often expensive and unhealthy. Second, cooking teaches skills that go beyond the kitchen, such as planning, managing time, and working with others. Some people say that our schedules are already full and there's no time for another subject. I understand that concern. However, cooking lessons don't need to be long. Even one class every two weeks would give us the basics. In short, learning to cook is an investment in our health and independence, and our schools should make room for it. Thank you.",
         claim=("Cooking should be a required subject for all high school students.",
                [("Students should eat at convenience stores less often.", "理由の中の一部（コンビニに頼ることの問題）で、主張そのものではない。"),
                 ("Cooking classes should be long and held every day.", "短い授業で十分だと述べており、逆である。"),
                 ("Students' schedules are already too full.", "話し手が取り上げた予想される反論で、主張ではない。")]),
         counter=("Students' schedules are already too full for another subject.",
                  [("Cooking is too dangerous for high school students.", "安全面の反論は取り上げていない。"),
                   ("Convenience store food is healthy enough.", "話し手はコンビニの食事は不健康なことが多いと述べており、反論として取り上げていない。"),
                   ("Cooking cannot be taught in a classroom.", "このような反論は取り上げていない。")]),
         rebut=("By saying that short lessons, such as one class every two weeks, would be enough",
                [("By saying that other subjects are less important than cooking", "ほかの教科を軽視する発言はしていない。"),
                 ("By saying that students can learn to cook at home instead", "家庭で学べばよいとは述べていない。それでは主張と矛盾する。"),
                 ("By saying that schedules are not really full", "予定が詰まっていることは I understand that concern と認めている。")]),
         resp="I agree that cooking is an important life skill. However, I think it should be an elective rather than a required subject, because some students already cook at home. Even short lessons take time that could be used for subjects students choose themselves."),
    dict(key="BNCH", title="Our Town Needs More Benches",
         script="Hello, everyone. I want to talk about something small that makes a big difference: benches. In our town, there are very few places to sit down along the main streets. This might not matter much to young people, but for older residents, parents with small children, and anyone carrying heavy bags, a place to rest can decide whether they go out at all. When people can rest, they walk more, shop more, and talk with their neighbors more. Some people argue that benches attract people who stay for hours and make a street feel messy. That can happen, but it's a question of design and maintenance, not a reason to have no benches at all. Well-placed, well-kept benches make a street friendlier for everyone. I hope the town council will add more of them. Thank you.",
         claim=("The town should add more benches along its main streets.",
                [("Young people do not need places to rest.", "This might not matter much to young people と述べるだけで、主張ではない。"),
                 ("Benches make streets feel messy.", "話し手が取り上げた予想される反論で、主張ではない。"),
                 ("Older residents should go out more often.", "外出を勧める主張ではなく、休める場所が外出を左右すると述べている。")]),
         counter=("Benches attract people who stay for hours and make streets feel messy.",
                  [("Benches are too expensive for the town to buy.", "費用の反論は取り上げていない。"),
                   ("Young people never use benches.", "このような反論は取り上げていない。"),
                   ("Benches block the way for people walking.", "通行の妨げという反論は取り上げていない。")]),
         rebut=("By saying that the problem can be solved through good design and maintenance",
                [("By saying that people who stay for hours are welcome", "長居する人を歓迎するとは述べていない。"),
                 ("By saying that messy streets are not a problem", "散らかることが起こりうると認めたうえで、設計と管理の問題だと答えている。"),
                 ("By saying that benches should be removed at night", "夜間の撤去は提案していない。")]),
         resp="I agree with the speaker. My grandmother often says she cannot walk to the station without resting. As the speaker said, the problem of messy benches can be solved by cleaning them regularly, so I hope the council will add benches near the station and the hospital."),
    dict(key="GRAD", title="Grading Group Work Fairly",
         script="Thank you for listening. My point today is simple: in group projects, each student should receive an individual grade. At the moment, everyone in a group gets the same grade. This seems fair at first, but it often isn't. In many groups, one or two members do most of the work, while others contribute very little and still receive the same reward. Over time, this discourages the hardest workers and teaches the others that they can rely on someone else. Of course, some people will say that individual grades destroy the team spirit that group work is meant to build. But I'm not suggesting we stop grading the group as a whole. Teachers could combine a group grade with an individual grade based on each member's own report. That way, students are encouraged both to cooperate and to take responsibility. Thank you.",
         claim=("Each student in a group project should receive an individual grade.",
                [("Group projects should be stopped completely.", "グループ活動をやめるべきだとは述べていない。"),
                 ("Everyone in a group should get the same grade.", "現在のやり方で、話し手はそれが公平でないことが多いと述べている。"),
                 ("Individual grades destroy team spirit.", "話し手が取り上げた予想される反論で、主張ではない。")]),
         counter=("Individual grades would destroy the team spirit that group work is meant to build.",
                  [("Teachers do not have time to grade each student.", "教師の負担という反論は取り上げていない。"),
                   ("The hardest workers do not care about grades.", "このような反論は取り上げていない。"),
                   ("Group work is not useful for learning.", "このような反論は取り上げていない。")]),
         rebut=("By suggesting that a group grade be combined with an individual grade",
                [("By saying that team spirit is not important", "チームワークの価値は否定していない。"),
                 ("By saying that students should work alone instead", "個人作業にすべきだとは述べていない。"),
                 ("By saying that only the hardest workers should be graded", "全員に個人の成績をつけるべきだと述べている。")]),
         resp="I partly agree with the speaker. It is unfair when one member does all the work. However, a grade based on each member's report may not show who actually helped the team. I think students should also evaluate one another, so that both cooperation and responsibility are reflected in the grade."),
    dict(key="DICT", title="Let's Keep Paper Dictionaries",
         script="Good morning. Most of my classmates use apps to look up words, and I understand why: apps are fast and light. But I believe paper dictionaries still deserve a place in our classrooms. When you look up a word in a paper dictionary, your eyes pass over the words around it, and you often notice related expressions or example sentences you weren't looking for. This kind of accidental learning rarely happens on a small screen that shows only the answer. Paper dictionaries also don't send notifications that break your concentration. Some might say that paper dictionaries are heavy and slow. That's true, but in class we don't need to carry them far, and the time spent searching isn't wasted if we learn more along the way. So, let's not throw away our paper dictionaries just yet. Thank you.",
         claim=("Paper dictionaries should still be used in classrooms.",
                [("Dictionary apps should be banned at school.", "アプリを禁止すべきだとは述べていない。アプリの利点も認めている。"),
                 ("Paper dictionaries are faster than apps.", "紙の辞書は遅いという反論を That's true と認めている。"),
                 ("Students should carry dictionaries everywhere.", "授業では遠くまで持ち運ぶ必要がないと述べている。")]),
         counter=("Paper dictionaries are heavy and slow to use.",
                  [("Paper dictionaries are too expensive.", "値段の反論は取り上げていない。"),
                   ("Paper dictionaries do not have example sentences.", "例文に気づけることは紙の辞書の利点として述べている。"),
                   ("Apps send too many notifications.", "これは紙の辞書の利点を述べる部分で、反論ではない。")]),
         rebut=("By admitting it is true, but saying that they are not carried far in class and searching time is not wasted",
                [("By saying that paper dictionaries are actually light", "That's true と、重く遅いことを認めている。"),
                 ("By saying that apps are even slower", "アプリは速いと認めている。"),
                 ("By saying that students should study only at home", "家だけで勉強すべきだとは述べていない。")]),
         resp="I disagree with the speaker. I understand that paper dictionaries can lead to accidental learning, but many apps also show example sentences and related words. If we turn off notifications, apps let us look up more words in the same time, so I think apps are better for class."),
]


def spstim(sp):
    return lstim(f"EC3S-{sp['key']}", sp["script"], f"スピーチ“{sp['title']}”")


# ======================================================================
# やりとりの表現（印刷したやりとり）
# ======================================================================

# (場面と目的, 相手の発話, 適切な応答, [(誤答, 理由)])
RESPONSES = [
    ("班での話し合い。あなたは反対の立場で、相手を尊重しながら代案を示したい。", "I think we should hold the welcome party outdoors. What do you think?",
     "I see your point, but what if it rains? An indoor room might be safer.",
     [("No. Your idea is wrong.", "相手を直接否定するだけで、理由も代案もなく、失礼に響く。"), ("You're welcome. I'm glad you like it.", "お礼への応答で、意見を求められた場面に合わない。"),
      ("I think so too. Let's hold it outdoors.", "賛成しており、反対の立場で代案を示すという目的に合わない。")]),
    ("先生の説明の中の数を聞き取れなかったので、聞き返したい。", "Make sure your summary is no more than a hundred words.",
     "Sorry, I didn't quite catch the word limit. Could you say it again?",
     [("Yes, I'm sure about that.", "make sure を「確信している」と取り違えた応答で、聞き返しになっていない。"), ("Sorry, I can't write a summary.", "要約ができないと伝えており、聞き返しではない。"),
      ("How many words did you write?", "先生が書いた語数を尋ねており、場面に合わない。")]),
    ("あまり話したことのない同級生に、前日の授業のノートを見せてもらいたい。", "Hi. You were absent yesterday, weren't you?",
     "Yes, I was. Would it be all right if I borrowed your notes for a few minutes?",
     [("Yes. Give me your notes.", "命令文で、親しくない相手への頼み方として直接的すぎる。"), ("Yes, I was. Could I lend you my notes?", "lend（貸す）と borrow（借りる）が逆で、自分のノートを貸す申し出になっている。"),
      ("Yes, I was. You should show me your notes.", "should は「～すべきだ」と相手に義務を課す言い方で、頼みごとに合わない。")]),
    ("相手に少し待ってほしいと頼まれ、快く応じたい。", "Do you mind waiting a few minutes? I'm almost done.",
     "Not at all. Take your time.",
     [("Yes, I do. Take your time.", "Do you mind …? に Yes と答えると「気にする（嫌だ）」の意味になり、Take your time と矛盾する。"),
      ("I'm afraid I can't wait.", "断っており、快く応じるという目的に合わない。"), ("No, thank you. I'm full.", "食べ物を勧められたときの断り方で、場面に合わない。")]),
    ("話し合いの途中で、相手の発言に関連する点を付け加えたい。", "...and that's why I think the budget should go to new books.",
     "Sorry to interrupt, but may I add something about the budget?",
     [("Stop talking. It's my turn now.", "相手の発言を乱暴にさえぎっており、失礼である。"), ("Excuse me, could you say that again?", "聞き返しの表現で、付け加える目的に合わない。"),
      ("Thank you for your time. That's all.", "発表や話し合いを締めくくる表現で、場面に合わない。")]),
    ("長い説明を聞いた後、自分の理解が正しいかを確かめたい。", "So the bus leaves at nine, but we'll meet at the station first, and then walk to the stop together.",
     "So, if I understand correctly, we'll meet at the station before nine and walk to the bus stop together?",
     [("I have no idea what you mean.", "理解できないと突き放す言い方で、確認になっていない。"), ("That's a good question.", "相手は質問をしていないので、場面に合わない。"),
      ("Let me finish what I was saying.", "自分の話を続けたいときの表現で、場面に合わない。")]),
    ("ディベートで、相手の主張の一部を認めたうえで反論したい。", "Online classes save students a lot of travel time.",
     "That's true, but they also make it harder for students to ask questions on the spot.",
     [("That's true, so online classes are always better.", "相手の主張を全面的に認めており、反論になっていない。"), ("I don't care about travel time.", "相手の論点を無視しており、反論として不適切で失礼である。"),
      ("You're right. I have nothing more to say.", "反論を放棄しており、目的に合わない。")]),
    ("相手の話が抽象的なので、具体例を求めたい。", "Many jobs will change a lot because of AI.",
     "Could you give me an example of a job that might change?",
     [("Yes, AI is very interesting.", "感想を述べるだけで、具体例を求めていない。"), ("I'm sorry, but I don't have a job.", "自分の仕事の有無は話題と関係がない。"),
      ("Why do you always talk about AI?", "相手を責めるような言い方で、具体例を求めていない。")]),
    ("友人の誘いを、関係を損なわないように断りたい。", "We're going to karaoke after school. Want to come?",
     "I'd love to, but I have to finish my report today. Maybe next time?",
     [("No. I don't want to go with you.", "直接的すぎて、相手を拒絶しているように響く。"), ("Yes, I'd love to. See you later, then.", "誘いを受けており、断るという目的に合わない。"),
      ("I'm sorry to hear that.", "悪い知らせへの応答で、誘いへの返事になっていない。")]),
    ("発表後の質疑応答で、すぐには答えられない質問を受けた。誠実に対応したい。", "Do you know how many schools in Japan have already introduced this system?",
     "That's a good question. I'm not sure, but I'll look into it and let you know.",
     [("That question is not important.", "質問者を軽んじる言い方で、誠実な対応ではない。"), ("Yes, I do.", "知っていると答えながら数を示しておらず、不誠実である。"),
      ("I don't know. Next question, please.", "突き放すような言い方で、調べて答えるなどの誠実さがない。")]),
    ("友人が残念な結果を伝えてきたので、気持ちに寄り添いたい。", "I failed my driving test again.",
     "Oh no, that must be frustrating. I'm sure you'll pass next time.",
     [("Congratulations! You must be happy.", "合格したときの応答で、場面と逆である。"), ("Why did you fail? It's easy.", "相手を責めるような言い方で、寄り添っていない。"),
      ("I passed mine on the first try.", "自分の自慢になり、相手の気持ちに寄り添っていない。")]),
    ("班の作業が進まないので、控えめに提案したい。", "We've been talking for an hour, and we still haven't started the research.",
     "How about dividing the topics so that each of us researches one?",
     [("You must divide the topics right now.", "must で相手に命令しており、控えめな提案ではない。"), ("Why didn't you divide the topics earlier?", "相手を責めており、提案になっていない。"),
      ("I'm sorry, I didn't do any research.", "謝罪で、作業を進める提案になっていない。")]),
]

FUNC_NAMES = ["丁寧な反対", "確認・聞き返し", "譲歩", "話題の転換", "具体例・説明の要求", "要約・まとめ", "発言の申し出", "控えめな提案"]
FUNC_EXPR = [
    ("I see where you're coming from, but I'm not sure I agree.", "丁寧な反対"),
    ("With all due respect, I think the numbers tell a different story.", "丁寧な反対"),
    ("Sorry, I didn't quite catch that. Could you say it again?", "確認・聞き返し"),
    ("Just to make sure I understand, you mean the deadline is Friday?", "確認・聞き返し"),
    ("Admittedly, the plan has some weaknesses.", "譲歩"),
    ("I'll grant you that it's expensive.", "譲歩"),
    ("On a different note, has anyone checked the budget?", "話題の転換"),
    ("Moving on to the next point, let's look at the schedule.", "話題の転換"),
    ("Could you be a bit more specific?", "具体例・説明の要求"),
    ("What would that look like in practice?", "具体例・説明の要求"),
    ("To sum up, we agree on the goal but not on the method.", "要約・まとめ"),
    ("So what it comes down to is a question of time.", "要約・まとめ"),
    ("If I could just jump in here for a second, ...", "発言の申し出"),
    ("May I add something to what Ken just said?", "発言の申し出"),
    ("It might be worth considering a smaller venue.", "控えめな提案"),
    ("Perhaps we could try asking the teachers first?", "控えめな提案"),
]
FUNC_SAMPLE = {}
for _e, _f in FUNC_EXPR:
    FUNC_SAMPLE.setdefault(_f, _e)

# (場面, 生徒の発話, 正しい発話, 誤りの箇所, 型, 説明, なぜ誤りやすいか)
EXPR_ERR = [
    ("先生に、レポートの締め切りを延ばしてもらえないか頼む。", "I want you to extend the deadline.", "Would it be possible to extend the deadline for my report?", "I want you to", "concept",
     "want 人 to do は相手への要求として直接的で、目上の人への依頼には不適切。Would it be possible to …? などで和らげる。", "「～してほしい」を want you to とそのまま英語にした。"),
    ("友人の意見に賛成する。", "I'm agree with you.", "I agree with you.", "I'm agree", "formula",
     "agree は動詞なので be 動詞は不要。", "日本語の「賛成です」の「です」を be 動詞で表そうとした。"),
    ("ディスカッションで相手の意見に反対する。", "You are wrong. Online classes are bad.", "I see your point, but I think online classes make it harder to ask questions.", "You are wrong.", "logic",
     "相手を直接否定するだけで理由がない。相手の論点を認めたうえで、理由を示して反対する。", "反対の意見を言うことだけに集中し、理由と相手への配慮を忘れた。"),
    ("相手の発言が聞き取れなかったので聞き返す。", "What? Say again.", "Sorry, could you say that again?", "What? Say again.", "concept",
     "ぶっきらぼうな命令の形で、失礼に響く。Sorry, could you …? と依頼の形にする。", "日本語の「え？もう一回」を短くそのまま英語にした。"),
    ("スピーチで意見を述べる。", "I think that we should to recycle more.", "I think that we should recycle more.", "should to", "formula",
     "助動詞 should の後ろは動詞の原形で、to は不要。", "have to / ought to と混同した。"),
    ("相手の言ったことを確かめる。", "You mean the meeting is on Friday, don't you mean?", "You mean the meeting is on Friday, right?", "don't you mean?", "notation",
     "付加疑問は don't you? の形で、mean はくり返さない。会話では , right? が自然。", "付加疑問を作るときに、元の動詞まで重ねてしまった。"),
    ("提案に条件つきで賛成する。", "I'm for it, unless we have enough money.", "I'm for it, as long as we have enough money.", "unless", "logic",
     "unless は「～でない限り」で、条件が逆になる。「～さえすれば」は as long as。", "unless を「もし～なら」の if と同じ意味だと思った。"),
    ("Would you mind if I opened the door? と頼まれ、快く許可する。", "Yes, of course. Go ahead.", "Not at all. Go ahead.", "Yes, of course.", "interpretation",
     "Would you mind …? は「気にしますか」と尋ねているので、Yes は「気にする（やめてほしい）」の意味になる。許可するなら Not at all. などと答える。", "日本語の「はい、どうぞ」につられて Yes と答えた。"),
    ("話し合いで、自分の意見を述べてよいか尋ねる。", "Excuse me, can I say my opinion?", "Excuse me, may I share my opinion?", "say my opinion", "concept",
     "opinion は say と結びつけるより、give / share / express と結びつけるのが自然。", "日本語の「意見を言う」を語ごとに英語に置きかえた。"),
    ("友人を励ます。", "Don't worry. You can do it if you will try.", "Don't worry. You can do it if you try.", "if you will try", "formula",
     "条件を表す if 節では、未来のことでも現在形を使う。", "「やってみれば」が未来のことなので will を入れた。"),
]


# ======================================================================
# A 基本確認
# ======================================================================

@gen("basic_check", 6, ["concept", "condition_check"])
def a_response(r):
    scene, prompt, ok, wrongs = r.choice(RESPONSES)
    return mc(f"次の場面で、相手の発話に対する応答として最も適切なものを選びなさい。\n［場面］{scene}\n相手：{prompt}\nあなた：（　　）", [ok] + [w for w, _ in wrongs],
              f"{ok}　場面の目的と相手との関係に合った表現で応じている。", d=2,
              ap="まず場面の目的（反対・聞き返し・依頼・断り・提案など）と相手との関係（友人・先生・初対面）を確かめ、その目的を果たす表現を選ぶ。",
              steps=["場面の目的と相手との関係を確認する。", "相手の発話の意図（意見を求める・頼む・誘う）を確認する。", "目的に合わない応答、失礼な応答を消す。", f"答え：{ok}"],
              alt=["選んだ応答の後に、相手がどう返すかを想像して、やりとりが自然に続くかを確かめる。"],
              pc=[("場面の目的をとらえている", 1), ("適切な応答を選んでいる", 1)],
              pit=["内容は合っていても、直接的すぎて失礼な表現を選ぶ。", "Do you mind …? に Yes で応じる。"],
              why={w: (reason, "場面・目的に合わない応答") for w, reason in wrongs})


@gen("basic_check", 6, ["concept", "computation"])
def a_function(r):
    expr, f = r.choice(FUNC_EXPR)
    wrongs = r.sample([x for x in FUNC_NAMES if x != f], 3)
    why = {w: (f"「{w}」の表現は、例えば “{FUNC_SAMPLE[w]}” のような形になる。この表現は「{f}」の働きをしている。", "やりとりの表現の機能の取り違え") for w in wrongs}
    return mc(f"話し合いの中で使われる次の表現の働きとして最も適切なものを選びなさい。\n{expr}", [f] + wrongs,
              f"「{f}」。{expr} は話し合いの中でこの働きをする典型的な表現である。", d=2,
              ap="表現の中心の語句（but / make sure / admittedly / on a different note / specific / sum up / jump in / might be worth）に注目し、話し合いの流れの中で何をしているかを考える。",
              steps=["表現の中心となる語句を確認する。", "その語句が話し合いの中で果たす働き（反対・確認・譲歩・転換・要求・まとめ・申し出・提案）を考える。", f"働きは「{f}」。"],
              alt=["同じ働きの別の表現を自分で1つ言い、意味の方向が同じかを確かめる。"],
              pc=[("中心の語句に気づいている", 1), ("働きを正しく選んでいる", 1)],
              pit=["丁寧な反対（I see …, but）を同意と取り違える。", "譲歩（Admittedly）を反対と取り違える。"], why=why)


@gen("basic_check", 5, ["computation", "concept"])
def a_dialog_detail(r):
    dl = r.choice(DIALOGS)
    q, ok, wrongs = r.choice(dl["qs"])
    return mc(f"対話“{dl['title']}”を聞き、問いに答えなさい。\n{q}最も適切なものを選びなさい。", [ok] + [w for w, _ in wrongs],
              f"{ok}　対話の途中で出た案や事情ではなく、最後の合意・決定と、その理由をとらえる。", d=2, stim=dstim(dl),
              ap="設問を先読みし、聞き取る情報（決定・理由・次の行動）を決める。途中で却下された案や、相手の事情を答えに選ばないよう、候補ごとに〇×をメモする。",
              steps=["設問を先読みし、何を聞き取るかを決める。", "対話に出てきた候補・理由をメモする。", "却下された案や関係のない事情に×をつける。", f"答え：{ok}"],
              alt=["選んだ答えの直後に、相手の同意（That would work. / Then you're all set. など）や行動の宣言（I'll …）があるかを確かめる。"],
              pc=[("候補と理由を聞き取っている", 1), ("正しい答えを選んでいる", 1)],
              pit=["最初に出た案や、相手の事情をそのまま答える。"], why={w: (reason, "途中の案・事情への引きずられ") for w, reason in wrongs})


@gen("basic_check", 3, ["condition_check", "common_error"])
def a_dialog_intent(r):
    dl = r.choice(DIALOGS)
    q, ok, wrongs, _ = dl["intent"]
    return mc(f"対話“{dl['title']}”を聞き、問いに答えなさい。\n{q}", [ok] + [w for w, _ in wrongs],
              f"{ok}　字義どおりではなく、状況と直後の反応から発話の意図を推論する。", d=2, stim=dstim(dl),
              ap="状況 → 字義 → 矛盾 → 意図の順に考える。字義どおりに受け取ると状況と合わない点を探し、直後の相手の反応で確かめる。",
              steps=["発話の前の状況（何を決めようとしているか）を確認する。", "発話の字義を確認する。", "字義どおりだと状況と合わない点を探す。", f"意図：{ok}"],
              alt=["選んだ意図を、より直接的な英語（Let's take the local train. など）に言いかえて、対話の流れに合うかを確かめる。"],
              pc=[("状況と字義の食い違いに気づいている", 1), ("意図を正しく選んでいる", 1)],
              pit=["疑問文の形の発話を、情報を求める質問と考える。", "might / not necessarily などの控えめな表現を否定や断りと考える。"],
              why={w: (reason, "字義どおりの解釈") for w, reason in wrongs})


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 5, ["concept", "computation"])
def b_lecture_notes(r):
    lc = r.choice(LECTURES)
    i = r.randrange(len(lc["rows"]))
    lab, ok = lc["rows"][i]
    others = [(j, v) for j, (_, v) in enumerate(lc["rows"]) if j != i]
    picks = r.sample(others, 2)
    fake = r.choice(lc["fake"])
    why = {v: (f"講義では {lc['rows'][j][0]} の内容として述べられており、{lab} の欄の内容ではない。", "ワークシートの見出しの取り違え") for j, v in picks}
    why[fake] = ("講義で述べられていない内容である。", "聞こえた語からの推測")
    return mc(f"講義“{lc['title']}”を聞き、ワークシートの空欄①（{lab}）に入る内容として最も適切なものを選びなさい。", [ok] + [v for _, v in picks] + [fake],
              f"{ok}　{lab} に当たる内容は、講義の構成の合図（First / Second / However / So など）の後で述べられている。", d=3, stim=lect_stim(lc), tbl=worksheet(lc, blank=i),
              ap="ワークシートの見出しの順から講義の構成を予測し、空欄の見出しに当たる話が始まる合図を待って聞く。",
              steps=["ワークシートの見出しと空欄の位置を確認する。", "講義の構成（定義 → 利点 → 欠点など）を予測する。", f"{lab} に当たる部分を聞き取る。", f"答え：{ok}"],
              alt=["ほかの欄の内容を順に確認し、残りの選択肢がどの欄の内容か、講義にない内容かを特定して消去する。"],
              pc=[("講義の構成をとらえている", 2), ("空欄の内容を選んでいる", 2)],
              pit=["別の見出しの内容を、聞こえた順番だけで選ぶ。", "講義に出てきた語を含むだけの、述べられていない内容を選ぶ。"], why=why)


@gen("standard_practice", 5, ["concept", "application"])
def b_lecture_content(r):
    lc = r.choice(LECTURES)
    if r.random() < 0.4:
        return mc(f"講義“{lc['title']}”を聞き、講師が最も伝えたいこととして最も適切なものを選びなさい。", [lc["main"]] + [w for w, _ in lc["main_wrong"]],
                  f"{lc['main']}　講義の最後の段落と、However / though で示される限界の両方を含めてまとめる。", d=3, stim=lect_stim(lc),
                  ap="講義の最後の部分（So / The story shows / reminds us）と、限界・議論中の点（However / though / still debate）の両方を含む選択肢を探す。",
                  steps=["講義の話題（最初の段落）を確認する。", "First / Second などで挙げられた要点をメモする。", "However / though の後ろの限界・欠点を確認する。", "結論を確認し、全体を含み、言いすぎていない選択肢を選ぶ。"],
                  alt=["選んだ選択肢が、講義の一部（具体例）だけになっていないか、always / completely などで言いすぎていないかを確かめる。"],
                  pc=[("講義の構成と結論をとらえている", 2), ("正しい選択肢を選んでいる", 2)],
                  pit=["印象に残った具体例を主旨として選ぶ。", "講師が限定した内容を断定した選択肢を選ぶ。"], why={w: (why, "主旨と部分・限定の混同") for w, why in lc["main_wrong"]})
    ok = r.choice(lc["trues"])
    return mc(f"講義“{lc['title']}”を聞き、講義の内容と一致するものを選びなさい。", [ok] + [w for w, _ in lc["falses"]],
              f"{ok}　講義の該当箇所の言いかえになっている。", d=3, stim=lect_stim(lc),
              ap="選択肢を先読みし、それぞれのキーワード（比較・否定・数・頻度）を講義で確かめる。",
              steps=["選択肢のキーワードを先読みする。", "講義の該当箇所を聞き取る。", "逆・言いすぎ・述べられていないものを消去する。", f"一致するのは：{ok}"],
              alt=["誤りの選択肢について、講義のどの部分と食い違うかをスクリプトで確かめる。"],
              pc=[("該当箇所を聞き取っている", 2), ("一致する選択肢を選んでいる", 2)],
              pit=["no / never / always / only などの強い語を聞き落とす。"], why={w: (why, "講義との照合不足") for w, why in lc["falses"]})


@gen("standard_practice", 5, ["condition_check", "application"])
def b_speech(r):
    sp = r.choice(SPEECHES)
    kind = r.choice(["claim", "counter", "rebut"])
    q = {"claim": "話し手の主張として最も適切なものはどれか。",
         "counter": "話し手が自分から取り上げている、予想される反論はどれか。",
         "rebut": "話し手は、予想される反論にどのように答えているか。"}[kind]
    ok, wrongs = sp[kind]
    cue = {"claim": "Today I'd like to argue that … / My point today is … / I believe … の後ろと、結論の In short / So の後ろ",
           "counter": "Some people say / argue / might say … の後ろ",
           "rebut": "I understand that concern. However … / That can happen, but … / That's true, but … の後ろ"}[kind]
    return mc(f"スピーチ“{sp['title']}”を聞き、問いに答えなさい。\n{q}最も適切なものを選びなさい。", [ok] + [w for w, _ in wrongs],
              f"{ok}　手がかりは {cue}。", d=3, stim=spstim(sp),
              ap="スピーチを「主張 → 理由 → 予想される反論 → 再反論 → 結論」の5つに区切りながら聞く。区切りの合図を先に知っておく。",
              steps=["主張の合図（I'd like to argue / My point is / I believe）を聞き取る。", "理由の合図（First / Second）を聞き取る。",
                     "反論の合図（Some people say）と、再反論の合図（However / but）を聞き取る。", f"設問に当たる部分の手がかり：{cue}。", f"答え：{ok}"],
              alt=["スピーチの5つの部分を1行ずつメモし、選択肢がどの部分の言いかえか（または述べられていないか）を照合する。"],
              pc=[("スピーチの構成をとらえている", 2), ("正しい選択肢を選んでいる", 2)],
              pit=["Some people say … の後ろの反論を、話し手の主張と取り違える。", "理由の一部を主張として選ぶ。"],
              why={w: (reason, "スピーチの構成の取り違え") for w, reason in wrongs})


@gen("standard_practice", 5, ["concept", "common_error"])
def b_lecture_org(r):
    lc = r.choice(LECTURES)
    if r.random() < 0.5:
        ok, wrongs = lc["org"]
        return mc(f"講義“{lc['title']}”を聞き、講義の構成を表したものとして最も適切なものを選びなさい。", [ok] + [w for w, _ in wrongs],
                  f"{ok}　各段落の最初の合図（Today / First / However / So など）で区切ると、この順になる。", d=3, stim=lect_stim(lc),
                  ap="講義を段落ごとに区切り、それぞれの段落が何をしているか（導入・定義・理由・欠点・結論）を一言でメモしてから選ぶ。",
                  steps=["各段落の最初の合図を聞き取る。", "段落ごとの働きを一言でメモする。", "メモの順と一致する選択肢を選ぶ。", f"答え：{ok}"],
                  alt=["誤りの選択肢の各部分（例：解決策・歴史）が、講義のどこかで実際に述べられているかを確かめて消去する。"],
                  pc=[("段落ごとの働きをとらえている", 2), ("構成を正しく選んでいる", 2)],
                  pit=["一般的な「問題 → 原因 → 解決策」の型に当てはめて選ぶ。"], why={w: (reason, "講義の構成の取り違え") for w, reason in wrongs})
    q, ok, wrongs = lc["q2"]
    return mc(f"講義“{lc['title']}”を聞き、問いに答えなさい。\n{q}", [ok] + [w for w, _ in wrongs],
              f"{ok}　講師の言い方（断定か、may / seem / still debate などで限定しているか）や、発言の位置づけに注意する。", d=3, stim=lect_stim(lc),
              ap="講師が断定している内容と、限定・推測・反論の前置きとして述べている内容を区別しながら聞く。",
              steps=["設問が講義のどの部分を問うているかを確認する。", "その部分の講師の言い方（is / cannot か、may / seem / still debate か）を聞き取る。", "前後の発言とのつながりを確かめる。", f"答え：{ok}"],
              alt=["選択肢ごとに、講義の該当する文をスクリプトで探し、言い方の強さに印をつけて比べる。"],
              pc=[("講師の言い方の違いに気づいている", 2), ("正しい選択肢を選んでいる", 2)],
              pit=["講師が限定して述べた内容を、断定された事実としてメモする。"], why={w: (reason, "断定と限定の区別の誤り") for w, reason in wrongs})


# ======================================================================
# C 思考力・記述応用
# ======================================================================

@gen("thinking_writing", 4, ["written_reasoning", "application"])
def c_lecture_summary(r):
    lc = r.choice(LECTURES)
    lim = r.choice([100, 120])
    return desc(f"講義“{lc['title']}”を聞き、講師の話の要点を日本語{lim}字以内でまとめなさい。講師が限定している点にも触れること。", lc["summary"],
                "ワークシートの見出しの順に要点をつなぎ、例の細部は除き、講師の限定（議論中・欠点・限界）を結論に添える。",
                lc["skeys"], d=4, p=8, grid=lim, stim=lect_stim(lc),
                ap="ワークシートのメモを見出しの順に並べ、要点だけを残す。最後に、講師が However / though / still debate で示した限定を1文で加える。",
                steps=["講義をワークシートの見出しに沿ってメモする。", "具体例・数値の細部を除き、要点だけを残す。", "要点を論理の接続（～ので・～が・そのため）でつなぐ。", "講師の限定を加え、字数内に整える。"],
                alt=["まず英語で講義の主旨を1文で書き、それを日本語に直してから要点を加える方法もある。"],
                pc=[(k, v) for k, v in lc["skeys"]],
                pit=["講義の順番どおりに細部まで書き、字数が足りなくなる。", "講師が限定した内容を断定して書く。"])


@gen("thinking_writing", 3, ["cross_unit", "written_reasoning"], rel=["HS-ENG-U10", "CT-ENG-U02"])
def c_respond_speech(r):
    sp = r.choice(SPEECHES)
    n = r.choice([50, 60])
    return desc(f"スピーチ“{sp['title']}”を聞き、話し手の主張に対するあなたの意見を英語{n}語程度で述べなさい。賛成・反対・部分的な賛成のいずれかの立場を明らかにし、話し手が取り上げた反論か再反論のどちらかに必ず触れること。",
                f"（解答例）{sp['resp']}",
                "立場 → 理由 → 話し手の反論・再反論への応答 → 結論の順に組み立てる。I agree / I disagree / I partly agree で始め、I understand that … , but … で相手の論点に応じる。",
                [("立場を明確にしている", 2), ("具体的な理由を述べている", 3), ("話し手の反論・再反論に触れ、文法・語数が適切である", 3)], d=4, p=8, lines=7, stim=spstim(sp),
                ap="まず話し手の主張・反論・再反論をメモし、自分の立場を決める。相手の再反論に納得できるかどうかを考えると、自分の理由が見つかりやすい。",
                steps=["話し手の主張・理由・反論・再反論をメモする。", "自分の立場（賛成・反対・部分的な賛成）を決める。", "自分の経験や具体例を使って理由を1つ以上考える。",
                       "話し手の反論または再反論に触れる文（As the speaker said … / I understand that …, but …）を入れて、語数を確かめる。"],
                alt=["部分的な賛成の立場をとり、話し手の主張の一部を認めたうえで、別の方法（選択科目にする、互いに評価するなど）を提案する書き方もできる。"],
                pc=[("立場", 2), ("理由", 3), ("相手の論点への応答と言語の正確さ", 3)],
                pit=["話し手の主張をくり返すだけで、自分の理由がない。", "話し手の反論・再反論に触れずに終わる。"])


@gen("thinking_writing", 3, ["written_reasoning", "application"])
def c_dialog_reply(r):
    dl = r.choice(DIALOGS)
    q, model = dl["reply"]
    n = r.choice([20, 25])
    return desc(f"対話“{dl['title']}”を聞き、問いに答えなさい。\n{q}（{n}語程度。対話の内容に合わせ、相手との関係にふさわしい丁寧さで書くこと。）",
                f"（解答例）{model}",
                "対話の状況（決まったこと・相手との関係）を踏まえ、目的（提案・依頼・お詫び・質問）に合ったやりとりの表現を使う。",
                [("対話の内容と状況に合っている", 3), ("目的に合ったやりとりの表現（依頼・提案・お詫びなど）を適切に使っている", 3), ("文法・語数が適切である", 2)], d=4, p=8, lines=5, stim=dstim(dl),
                ap="対話で決まったことと、相手との関係（友人・先生・係の人）を確かめ、Would it be possible …? / Could we …? / Sorry, … などの表現から目的に合うものを選ぶ。",
                steps=["対話で決まったこと・残っている問題を確認する。", "発話の目的と、相手との関係を確認する。", "目的に合う表現を選び、対話の内容（曜日・時間・内容）を入れて文を組み立てる。", "語数と丁寧さを確かめる。"],
                alt=["書いた発話に相手がどう返すかを1文で考え、やりとりが自然に続くかを確かめる。"],
                pc=[("内容と状況", 3), ("やりとりの表現", 3), ("文法・語数", 2)],
                pit=["対話で決まった内容と矛盾することを書く。", "先生や係の人に対して直接的すぎる表現を使う。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

@gen("error_correction", 4, ["common_error", "condition_check"])
def d_note_err(r):
    lc = r.choice(LECTURES)
    i = r.randrange(len(lc["rows"]))
    lab, ok = lc["rows"][i]
    if r.random() < 0.5:
        wrong = r.choice(lc["fake"])
        why = "講義で述べられていない内容を、聞こえた語から推測して書いている。"
        etype = "interpretation"
        tempt = "講義に出てきた語（sun / water / words / time / pill など）から内容を想像して書いた。"
    else:
        j = r.choice([k for k in range(len(lc["rows"])) if k != i])
        wrong = lc["rows"][j][1]
        why = f"これは {lc['rows'][j][0]} の欄に入る内容で、{lab} の欄の内容ではない。"
        etype = "condition"
        tempt = "講義の構成の合図を聞き落とし、聞こえた順番で欄を埋めた。"
    return desc(f"講義“{lc['title']}”を聞き、ある生徒が次のワークシートにメモをとった。{lab} の欄のメモには誤りがある。誤りの理由を説明し、正しいメモに直しなさい。",
                f"誤りの理由：{why}　正しいメモ：{ok}",
                f"{lab} の欄には「{ok}」が入る。講義の構成の合図で区切り、見出しに対応する要点を聞き取る。",
                [("誤りの理由（別の欄の内容・講義にない内容）を説明している", 2), ("正しいメモに直している", 3), ("講義の該当箇所に触れている", 1)], d=3, p=6, lines=5,
                stim=lect_stim(lc), tbl=worksheet(lc, filled={i: wrong}),
                ap="誤りのあるメモが、講義のどの部分から来たのか（別の見出しの内容か、講義にない推測か）を確かめ、見出しに対応する部分を聞き直す。",
                steps=[f"{lab} の欄のメモ「{wrong}」が講義のどこに当たるかを確かめる。", f"誤りの理由：{why}", f"{lab} に対応する講義の部分を確認する。", f"正しいメモ：{ok}"],
                alt=["ワークシート全体を見直し、同じ内容が2つの欄に入っていないか、講義にない内容がないかを点検する。"],
                pc=[("誤りの理由", 2), ("正しいメモ", 3), ("該当箇所への言及", 1)],
                pit=["聞こえた順番だけで欄を埋める。"],
                err=dict(sol=wrong, step=f"{lab} の欄", type=etype, tempt=tempt, fix=ok))


@gen("error_correction", 3, ["common_error", "computation"])
def d_expr_err(r):
    scene, wrong, fix, where, etype, rule, tempt = r.choice(EXPR_ERR)
    return desc(f"次の場面で、ある生徒は英語で次のように言った。\n［場面］{scene}\n［ある生徒の発話］{wrong}\nこの発話の不適切な点を指摘し、場面にふさわしい英語に直しなさい。",
                fix, f"{rule}正しくは {fix}",
                [("不適切な箇所と理由を指摘している", 2), ("場面にふさわしい英語に直している", 3), ("規則・配慮の観点を説明している", 1)], d=3, p=6, lines=5,
                ap="①文法・語法として正しいか、②場面の目的と相手との関係に合っているか、の2つの観点で発話を点検する。",
                steps=[f"「{where}」の部分に注目する。", f"問題点：{rule}", f"正しい発話：{fix}"],
                alt=["直した発話を相手の立場で聞いたとき、どう感じるかを考えて、丁寧さが場面に合っているかを確かめる。"],
                pc=[("誤りの指摘", 2), ("正しい発話", 3), ("観点の説明", 1)],
                pit=["日本語の言い方をそのまま英語に置きかえる。", "文法が正しければ、相手との関係は考えなくてよいと思う。"],
                err=dict(sol=wrong, step=f"「{where}」の部分", type=etype, tempt=tempt, fix=fix))


@gen("error_correction", 3, ["common_error", "written_reasoning"])
def d_intent_err(r):
    dl = r.choice(DIALOGS)
    q, ok, wrongs, tempt = dl["intent"]
    wrong, reason = wrongs[0]
    return desc(f"対話“{dl['title']}”を聞き、問いに答えなさい。\n「{q}」という問いに、ある生徒は次のように答えた。\n［ある生徒の解答］{wrong}\nこの解答の誤りを、対話の状況に触れて指摘し、正しい解釈を書きなさい。",
                f"誤り：{reason}　正しい解釈：{ok}",
                "発話の意図は、字義ではなく、直前の状況と直後の反応から決まる。",
                [("解答の誤りを、対話の状況・前後の発話を根拠に指摘している", 3), ("正しい解釈を書いている", 3)], d=4, p=6, lines=5, stim=dstim(dl),
                ap="生徒の解釈を対話に当てはめ、前後の発話とつながるかを確かめる。つながらない点が誤りの根拠になる。",
                steps=["発話の前の状況を確認する。", "生徒の解釈を当てはめたとき、前後の発話と食い違う点を探す。", f"誤りの指摘：{reason}", f"正しい解釈：{ok}"],
                alt=["正しい解釈を、より直接的な英語に言いかえて対話に入れ、流れが自然になることを確かめる。"],
                pc=[("誤りの指摘", 3), ("正しい解釈", 3)],
                pit=["発話を字義どおりに受け取る。"],
                err=dict(sol=wrong, step="発話の意図の解釈", type="interpretation", tempt=tempt, fix=ok))


GENERATORS = [a_response, a_function, a_dialog_detail, a_dialog_intent,
              b_lecture_notes, b_lecture_content, b_speech, b_lecture_org,
              c_lecture_summary, c_respond_speech, c_dialog_reply,
              d_note_err, d_expr_err, d_intent_err]
