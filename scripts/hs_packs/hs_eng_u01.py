"""単元パック：英語コミュニケーションⅠ 文型と動詞（5文型・自動詞と他動詞・紛らわしい動詞）。"""
import random

from banks._common import desc, mc, order, sa
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem,
                         tp)

UNIT_ID = "HS-ENG-U01"

PAT = {
    "SV": "第1文型（SV）",
    "SVC": "第2文型（SVC）",
    "SVO": "第3文型（SVO）",
    "SVOO": "第4文型（SVOO）",
    "SVOC": "第5文型（SVOC）",
}
CRIT = {
    "SV": "動詞の後ろに目的語も補語もなく、修飾語だけが続く",
    "SVC": "動詞の後ろに、主語とイコールの関係になる補語が続く",
    "SVO": "動詞の後ろに目的語が1つだけ続き、主語とイコールの関係にならない",
    "SVOO": "動詞の後ろに「（人）に」「（物）を」にあたる2つの目的語が続く",
    "SVOC": "動詞の後ろに目的語と、その目的語とイコールの関係になる補語が続く",
}
ROLE_LABEL = {"S": "主語（S）", "O": "目的語（O）", "C": "補語（C）", "M": "修飾語（M）"}
ROLE_DEF = {
    "S": "動作・状態の主体となる名詞（「～は」「～が」にあたる）",
    "O": "動詞の動作の対象となる名詞（「～を」「～に」にあたる）",
    "C": "主語または目的語の状態・性質を説明し、それとイコールの関係になる語句",
    "M": "取り除いても文の骨組みが成り立つ修飾語句（時・場所・様態などを表す）",
}

# 文型の例文バンク：(文型, [(語句, 要素)], 和訳)。要素は S / V / O / O1 / O2 / C / M。
SENT = [
    ("SV", [("The baby", "S"), ("slept", "V"), ("peacefully", "M"), ("in her mother's arms", "M")], "赤ちゃんは母親の腕の中で安らかに眠った。"),
    ("SV", [("My grandfather", "S"), ("walks", "V"), ("in the park", "M"), ("every morning", "M")], "祖父は毎朝、公園を散歩する。"),
    ("SV", [("A strange accident", "S"), ("happened", "V"), ("near our school", "M"), ("yesterday", "M")], "昨日、学校の近くで奇妙な事故が起きた。"),
    ("SV", [("The concert", "S"), ("will begin", "V"), ("at seven", "M")], "コンサートは7時に始まる。"),
    ("SV", [("Many birds", "S"), ("fly", "V"), ("south", "M"), ("in winter", "M")], "冬になると多くの鳥が南へ飛んでいく。"),
    ("SV", [("My older sister", "S"), ("works", "V"), ("at a hospital", "M"), ("in Yokohama", "M")], "姉は横浜の病院で働いている。"),
    ("SV", [("We", "S"), ("arrived", "V"), ("at the station", "M"), ("ten minutes late", "M")], "私たちは10分遅れて駅に着いた。"),
    ("SV", [("The children", "S"), ("laughed", "V"), ("loudly", "M")], "子どもたちは大声で笑った。"),
    ("SVC", [("Her face", "S"), ("turned", "V"), ("pale", "C"), ("at the news", "M")], "その知らせを聞いて、彼女の顔は青ざめた。"),
    ("SVC", [("This soup", "S"), ("tastes", "V"), ("a little salty", "C")], "このスープは少ししょっぱい。"),
    ("SVC", [("My cousin", "S"), ("became", "V"), ("a nurse", "C"), ("last year", "M")], "いとこは昨年、看護師になった。"),
    ("SVC", [("Your plan", "S"), ("sounds", "V"), ("interesting", "C")], "あなたの計画はおもしろそうだ。"),
    ("SVC", [("He", "S"), ("remained", "V"), ("silent", "C"), ("during the meeting", "M")], "彼は会議の間ずっと黙ったままだった。"),
    ("SVC", [("You", "S"), ("look", "V"), ("tired", "C"), ("today", "M")], "今日は疲れているように見えますね。"),
    ("SVC", [("She", "S"), ("stayed", "V"), ("calm", "C"), ("in the emergency", "M")], "彼女は緊急事態の中でも落ち着いていた。"),
    ("SVC", [("The milk", "S"), ("went", "V"), ("bad", "C"), ("in the heat", "M")], "暑さで牛乳が悪くなった。"),
    ("SVO", [("We", "S"), ("discussed", "V"), ("the problem", "O"), ("after class", "M")], "私たちは授業の後でその問題について話し合った。"),
    ("SVO", [("The students", "S"), ("entered", "V"), ("the classroom", "O"), ("quietly", "M")], "生徒たちは静かに教室に入った。"),
    ("SVO", [("I", "S"), ("really", "M"), ("enjoyed", "V"), ("the concert", "O"), ("last night", "M")], "昨夜のコンサートは本当に楽しかった。"),
    ("SVO", [("She", "S"), ("resembles", "V"), ("her mother", "O")], "彼女は母親に似ている。"),
    ("SVO", [("My father", "S"), ("reached", "V"), ("the airport", "O"), ("at noon", "M")], "父は正午に空港に着いた。"),
    ("SVO", [("Mr. Sato", "S"), ("married", "V"), ("my aunt", "O"), ("ten years ago", "M")], "佐藤さんは10年前に私のおばと結婚した。"),
    ("SVO", [("The team", "S"), ("won", "V"), ("the game", "O"), ("easily", "M")], "そのチームは楽々と試合に勝った。"),
    ("SVO", [("My brother", "S"), ("plays", "V"), ("the guitar", "O"), ("very well", "M")], "兄はギターをとても上手にひく。"),
    ("SVOO", [("My aunt", "S"), ("sent", "V"), ("me", "O1"), ("a birthday card", "O2")], "おばが私に誕生日カードを送ってくれた。"),
    ("SVOO", [("The teacher", "S"), ("asked", "V"), ("us", "O1"), ("a difficult question", "O2")], "先生は私たちに難しい質問をした。"),
    ("SVOO", [("Mr. Brown", "S"), ("teaches", "V"), ("us", "O1"), ("English", "O2")], "ブラウン先生は私たちに英語を教えている。"),
    ("SVOO", [("This app", "S"), ("will save", "V"), ("you", "O1"), ("a lot of time", "O2")], "このアプリを使えば、かなりの時間が節約できるだろう。"),
    ("SVOO", [("My father", "S"), ("cooked", "V"), ("us", "O1"), ("dinner", "O2"), ("last Sunday", "M")], "父はこの前の日曜日、私たちに夕食を作ってくれた。"),
    ("SVOO", [("Ken", "S"), ("lent", "V"), ("me", "O1"), ("his umbrella", "O2")], "ケンは私に傘を貸してくれた。"),
    ("SVOO", [("She", "S"), ("showed", "V"), ("the visitors", "O1"), ("the way to the museum", "O2")], "彼女は訪問者たちに博物館への道を教えた。"),
    ("SVOO", [("The repair", "S"), ("cost", "V"), ("me", "O1"), ("10,000 yen", "O2")], "その修理に1万円かかった。"),
    ("SVOC", [("The news", "S"), ("made", "V"), ("everyone", "O"), ("happy", "C")], "その知らせでみんなが喜んだ。"),
    ("SVOC", [("We", "S"), ("call", "V"), ("our dog", "O"), ("Shiro", "C")], "私たちは飼い犬をシロと呼んでいる。"),
    ("SVOC", [("She", "S"), ("left", "V"), ("the door", "O"), ("open", "C")], "彼女はドアを開けたままにした。"),
    ("SVOC", [("I", "S"), ("found", "V"), ("the movie", "O"), ("boring", "C")], "その映画は退屈だと思った。"),
    ("SVOC", [("The members", "S"), ("elected", "V"), ("Yuki", "O"), ("captain of the team", "C")], "部員たちはユキをチームのキャプテンに選んだ。"),
    ("SVOC", [("You", "S"), ("should keep", "V"), ("your room", "O"), ("clean", "C")], "部屋はきれいにしておくべきだ。"),
    ("SVOC", [("The long walk", "S"), ("made", "V"), ("us", "O"), ("hungry", "C")], "長い散歩で私たちはおなかがすいた。"),
    ("SVOC", [("Most people", "S"), ("consider", "V"), ("him", "O"), ("a genius", "C")], "たいていの人は彼を天才だと考えている。"),
]


def text(segs):
    return " ".join(w for w, _ in segs) + "."


def analysis(segs):
    out = []
    for w, role in segs:
        lab = {"O1": "O₁", "O2": "O₂"}.get(role, role)
        out.append(f"{w}＝{lab}")
    return "、".join(out)


def by_pattern(p, half=None):
    rows = [s for s in SENT if s[0] == p]
    if half == 0:
        return rows[:4]
    if half == 1:
        return rows[4:]
    return rows


def local(key):
    """問題文から決まる乱数（同じ問題文なら同じ選択肢になるようにする）。"""
    return random.Random(key)


# ======================================================================
# 授業プリント
# ======================================================================

LESSON = lesson(
    goals=["文の要素（S・V・O・C・M）を見分け、英文を5つの文型に分類できる。",
           "第4文型と第3文型の書きかえで、to と for を動詞の意味から使い分けられる。",
           "自動詞と他動詞の区別、lie / lay などの紛らわしい動詞の活用を正しく使える。"],
    duration=50,
    readiness=["be 動詞と一般動詞の区別ができる（中学1年）。", "SVOO・SVOC の文（give 人 物、make O C など）を中学で学習している。",
               "名詞・形容詞・副詞・前置詞の品詞の働きを説明できる。"],
    flow=[("導入：同じ動詞で意味が変わる", 5, "Call me a taxi. と Call me Ken. を比べ、語順と要素で意味が決まることに気づかせる"),
          ("文の要素と5文型", 15, "S・V・O・C・M の定義を確認し、文型を見分ける手順を板書で示す（例題1）"),
          ("第4文型と第3文型", 10, "to 型・for 型の動詞を、動作に相手が必要かどうかで分類する（例題2）"),
          ("自動詞と他動詞・紛らわしい動詞", 13, "discuss / talk about、lie / lay、rise / raise を活用表で整理する（例題3）"),
          ("まとめと確認", 7, "確認問題3問、問題プリントA の課題指示")],
    sections=[
        intro("in1", "なぜ文型を学ぶのか",
              "Call me a taxi. と Call me Ken. は、どちらも call me のあとに名詞が1つ続いている。しかし前者は「タクシーを呼んでください」、後者は「私をケンと呼んでください」という意味になる。英語は語の形がほとんど変化しない代わりに、語順と「文の中での役割（文の要素）」で意味が決まる言語である。文型は、その役割の組み合わせを5つの型に整理したものであり、長い文を正確に読むための骨組みになる。",
              bullets=["前者は me（に）と a taxi（を）が別のもの：第4文型（SVOO）。", "後者は me＝Ken の関係が成り立つ：第5文型（SVOC）。",
                       "動詞の後ろにどんな要素が続くかは、動詞ごとにある程度決まっている。"],
              points=[tp("2つの文を板書し、和訳を生徒に言わせてから「何が違うのか」を考えさせる。", ask="me と a taxi、me と Ken の関係はそれぞれどうなっているか。",
                         expect="me と a taxi は別のもの、me と Ken は同じ人物。", timing="導入の冒頭"),
                      tp("文型は「暗記する分類」ではなく「意味を正確に取るための道具」であることを最初に伝える。")]),
        definition("df1", "文の要素（S・V・O・C・M）",
                   "英文の骨組みを作る要素は、主語（S）・動詞（V）・目的語（O）・補語（C）の4つである。それ以外の、時・場所・様態などを表す語句は修飾語（M）と呼び、文型には数えない。",
                   bullets=["S（主語）：「～は」「～が」にあたる名詞。", "V（動詞）：助動詞を含めて1つの V と考える（will begin, should keep）。",
                            "O（目的語）：動作の対象となる名詞。「～を」「～に」と訳すことが多い。", "C（補語）：主語や目的語の状態・性質を説明する名詞・形容詞。S＝C、O＝C の関係が成り立つ。",
                            "M（修飾語）：前置詞＋名詞、副詞など。取り除いても文が成り立つ。"],
                   conditions=["前置詞の後ろの名詞は、前置詞の目的語であり、文の要素 O にはならない（at the station は全体で M）。",
                               "副詞は C にならないが、形容詞は C になれる（easy は C になれるが easily はなれない）。"],
                   points=[tp("「前置詞＋名詞」をかっこでくくって消す作業を、最初の数文は全員で声に出して行わせる。", caution="前置詞の後ろの名詞を O と数える誤りが最も多い。")]),
        theorem("th1", "5文型",
                "第1文型 SV ／ 第2文型 SVC（S＝C） ／ 第3文型 SVO ／ 第4文型 SVOO（O₁≠O₂） ／ 第5文型 SVOC（O＝C）",
                ["SVC と SVO の区別：動詞の後ろの語が主語とイコールなら C、別のものなら O。",
                 "SVOO と SVOC の区別：2つの名詞が別のもの（「人に」「物を」）なら SVOO、イコールの関係なら SVOC。",
                 "修飾語（M）は文型を決めるときには数えない。"],
                body="代表的な動詞：SVC は be, become, look, seem, sound, taste, turn, get, keep など。SVOO は give, send, show, teach, tell, buy, make など。SVOC は make, call, name, find, keep, leave, elect など。",
                points=[tp("同じ動詞でも複数の文型をとる（make は SVO・SVOO・SVOC すべてある）ので、「動詞を見て文型を決める」のではなく「後ろの要素を見て決める」ことを強調する。",
                           ask="make を使って SVO・SVOO・SVOC の文を1つずつ作れるか。", expect="She made a cake. / She made him a cake. / The news made him happy.")]),
        derivation("dv1", "文型を見分ける手順（なぜその文型と言えるのか）",
                   ["① 動詞（V）を見つける。助動詞があれば V に含める。V の前の名詞のまとまりが S。",
                    "② 前置詞＋名詞、副詞、時を表す語句など、取り除いても文が成り立つものを M としてかっこでくくる。",
                    "③ V の後ろに残った語句の数を数える。0 個なら SV。",
                    "④ 1個のとき：S とイコールの関係（He became a nurse. → He＝a nurse）なら C で SVC、そうでなければ O で SVO。",
                    "⑤ 2個のとき：2つが別のもの（me ≠ a card）なら SVOO、イコールの関係（the door＝open）なら SVOC。",
                    "⑥ 最後に和訳を作り、「S は C だ」「O が C の状態だ」と言いかえて意味が通るかで判断を確かめる。"],
                   body="手順④⑤のイコールの関係は、be 動詞をはさんで文が作れるかで確かめられる。The door was open. が成り立つので、She left the door open. は SVOC である。",
                   points=[tp("イコールの確かめ方として「be 動詞をはさむテスト」を必ず実演する。", ask="She showed the visitors the way. で the visitors were the way. は成り立つか。",
                              expect="成り立たないので SVOO。", timing="手順⑤の説明時")]),
        definition("df2", "自動詞と他動詞・紛らわしい動詞",
                   "目的語をとらない動詞を自動詞、目的語をとる動詞を他動詞という。日本語の「～について」「～に」につられて、他動詞に前置詞をつけたり、自動詞の前置詞を落としたりする誤りが多い。",
                   bullets=["他動詞（前置詞は不要）：discuss, enter, reach, marry, resemble, mention, attend, approach, contact, explain",
                            "自動詞（前置詞が必要）：talk about, arrive at / in, get to, apologize to, complain about, listen to",
                            "lie（横になる・ある）：lie – lay – lain – lying ／ lay（横たえる・置く）：lay – laid – laid – laying",
                            "rise（上がる）：rise – rose – risen ／ raise（上げる）：raise – raised – raised",
                            "sit（座る）：sit – sat – sat ／ seat（座らせる）：seat – seated – seated（be seated で「座る」）"],
                   conditions=["lie の過去形 lay と、lay の原形 lay は同じつづりなので、文脈と目的語の有無で判断する。",
                               "「嘘をつく」の lie は規則変化（lie – lied – lied – lying）。"],
                   points=[tp("自動詞・他動詞のペアは「自分が動く（自動詞）」「何かを動かす（他動詞）」と対比させて覚えさせる。", caution="lay を「横になる」の過去形と取り違える誤りが定期考査で頻出。")]),
        example("ex1", "例題1　文型を判断して訳す",
                "次の英文の文型を答え、日本語に訳しなさい。The students found the question difficult.",
                ["V は found。S は The students。", "後ろに the question と difficult の2つの語句が残る。",
                 "The question was difficult. が成り立つので the question＝difficult。よって SVOC。", "find O C は「O が C だとわかる・思う」。"],
                "第5文型（SVOC）。「生徒たちはその問題が難しいとわかった。」",
                thinking="動詞の後ろの2つの語句がイコールの関係かどうかを、be 動詞をはさんで確かめる。",
                points=[tp("difficult が形容詞であることに注目させ、「形容詞は O になれない」ことからも C だと判断できることを補足する。")],
                misconceptions=[("「生徒たちは難しい問題を見つけた。」と訳す", "difficult は the question を前から修飾していない。O＝C の関係なので「O が C だとわかる」と訳す")]),
        example("ex2", "例題2　第4文型から第3文型への書きかえ",
                "次の文を、ほぼ同じ意味の第3文型の文に書きかえなさい。(1) My grandmother made me a sweater.　(2) Ken showed me his photos.",
                ["(1) make は「相手がいなくても作れる」動作なので、相手は for で示す。", "(1) My grandmother made a sweater for me.",
                 "(2) show は「相手がいないと成り立たない」動作（相手への移動）なので、相手は to で示す。", "(2) Ken showed his photos to me."],
                "(1) My grandmother made a sweater for me.　(2) Ken showed his photos to me.",
                thinking="第4文型の O₂（物）を動詞の直後に出し、O₁（人）を前置詞の後ろに回す。前置詞は動詞の意味で決まる。",
                points=[tp("to 型（give, send, show, lend, teach, tell など）と for 型（buy, make, cook, find, get, choose など）を、動作の性質で分類させる。",
                           ask="「作る」は相手がいなくてもできるか。「貸す」はどうか。", expect="作るは1人でできる（for）、貸すは相手がいないとできない（to）。")]),
        example("ex3", "例題3　紛らわしい動詞",
                "（　）内から適切な語を選びなさい。(1) He (lay / laid) on the grass and looked at the sky.　(2) Prices have (risen / raised) a lot this year.",
                ["(1) 後ろに目的語がなく「横になった」の意味なので自動詞 lie の過去形 lay。", "(2) 後ろに目的語がなく「上がった」の意味なので自動詞 rise の過去分詞 risen。"],
                "(1) lay　(2) risen",
                thinking="まず後ろに目的語があるかを確認し、自動詞か他動詞かを決めてから、活用形を選ぶ。",
                points=[tp("活用表を板書し、lay が「lie の過去形」と「lay の原形」の2つの顔を持つことを色分けして示す。")]),
        board("bd1", "板書案",
              [("① 文の要素と5文型", ["S・V・O・C ＝ 骨組み、M ＝ 飾り", "前置詞＋名詞 → M（かっこでくくる）", "SV／SVC（S＝C）／SVO", "SVOO（O₁≠O₂）／SVOC（O＝C）", "be 動詞をはさんでイコールを確認"]),
               ("② SVOO → SVO", ["to 型：give, send, show, lend, teach, tell", "for 型：buy, make, cook, find, get, choose", "made me a sweater", "→ made a sweater for me"]),
               ("③ 自動詞・他動詞", ["discuss the problem（about 不要）", "arrive at ／ reach（at 不要）", "lie – lay – lain（横になる）", "lay – laid – laid（横たえる）", "rise – rose – risen ／ raise – raised – raised"])],
              points=[tp("板書は3列に分け、①で判断の手順、②で書きかえ、③で動詞の語法を整理する。③の活用表は生徒にノートへ写させて小テストにつなげる。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("文型の判断では、必ず先に M をかっこでくくらせる。M を消すと残りの要素が見えやすくなる。", ask="at the station は O か。", expect="前置詞の後ろなので M の一部。"),
               tp("SVC の動詞（look, sound, taste など）の後ろに副詞を置く誤り（look happily）を、C には形容詞が入るという規則で説明する。", caution="日本語の「楽しそうに見える」の「～に」につられやすい。"),
               tp("第4文型の書きかえでは、前置詞を選んだ理由（相手が必要か）を言葉で言わせる。", timing="例題2の後"),
               tp("自動詞・他動詞は、日本語訳ではなく「後ろに目的語を直接置けるか」で判断する習慣をつけさせる。"),
               tp("問題プリント D の誤答例を使い、「前置詞を足す誤り」と「前置詞を落とす誤り」の両方があることを示す。")],
              misconceptions=[("We discussed about the plan.", "discuss は他動詞なので about は不要。We discussed the plan."),
                              ("She looked happily.", "look は SVC をとるので C には形容詞。She looked happy."),
                              ("He laid on the bed.", "「横になった」は自動詞 lie の過去形 lay。He lay on the bed.")]),
        summary("sm1", "まとめ",
                ["文型は「V の後ろに何がいくつ続くか」と「イコールの関係があるか」で決める。M は数えない。",
                 "SVOO → SVO の書きかえは、相手が必要な動作は to、相手がいなくてもできる動作は for。",
                 "他動詞に前置詞は不要、自動詞には必要。lie / lay、rise / raise は目的語の有無で判断する。"]),
        check("ck1", "確認問題",
              [("She kept quiet during the class. の文型を答えなさい。", "第2文型（SVC）。She＝quiet の関係が成り立ち、during the class は M。"),
               ("My uncle bought me a camera. を第3文型に書きかえなさい。", "My uncle bought a camera for me."),
               ("lie（横になる）の過去形と過去分詞を答えなさい。", "過去形 lay、過去分詞 lain")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

@gen("basic_check", 5, ["computation", "concept"])
def identify_pattern(r):
    p = r.choice(list(PAT))
    _, segs, jp = r.choice(by_pattern(p, 0))
    s = text(segs)
    others = [q for q in PAT if q != p]
    why = {PAT[w]: (f"{PAT[w]}になるのは「{CRIT[w]}」場合である。この文は {analysis(segs)} と分析でき、{PAT[p]}にあたる。", f"{PAT[w]}と{PAT[p]}の判断基準の混同")
           for w in others}
    return mc(f"次の英文の文型として正しいものを選びなさい。\n{s}", [PAT[x] for x in PAT],
              f"{analysis(segs)}。{CRIT[p]}ので{PAT[p]}。和訳：{jp}", d=1, keep=True, ai=list(PAT).index(p),
              ap="まず動詞（V）を見つけ、前置詞＋名詞や副詞などの修飾語（M）をかっこでくくってから、V の後ろに残る要素を数える。",
              steps=["V を見つけ、その前の名詞のまとまりを S とする。", "修飾語（M）を取り除く。",
                     f"残った要素から判断する：{analysis(segs)}。", f"{CRIT[p]}ので{PAT[p]}。"],
              alt=[f"和訳「{jp}」を作り、「S は C だ」「O が C の状態だ」と言いかえられるかで、補語の有無を確かめる。"],
              pc=[("文の要素を正しく分析している", 1), ("文型を正しく判断している", 1)],
              pit=["前置詞の後ろの名詞を目的語（O）と数えてしまう。", "副詞を補語（C）と考えてしまう。"], why=why)


@gen("basic_check", 5, ["concept"])
def element_role(r):
    p = r.choice(list(PAT))
    _, segs, jp = r.choice(by_pattern(p, 1))
    cand = [i for i, (_, role) in enumerate(segs) if role not in ("V", "S")]
    i = r.choice(cand)
    w, role = segs[i]
    base = "O" if role in ("O1", "O2") else role
    words = dict((rl, x) for x, rl in segs)
    if role == "O" and p == "SVOC":
        reason = f"動詞の目的語で、後ろの補語 {words['C']} とイコールの関係（{w}＝{words['C']}）にある"
    elif role == "O":
        reason = f"動詞 {words['V']} の動作の対象となる名詞で、主語とイコールの関係にはない"
    elif role == "O1":
        reason = f"「（人）に」にあたる目的語で、後ろにもう1つの目的語 {words['O2']} が続く"
    elif role == "O2":
        reason = f"「（物）を」にあたる目的語で、直前の目的語 {words['O1']} とは別のものを指す"
    elif role == "C" and p == "SVC":
        reason = f"主語 {words['S']} の状態・性質を説明しており、{words['S']}＝{w} の関係が成り立つ"
    elif role == "C":
        reason = f"目的語 {words['O']} の状態・性質を説明しており、{words['O']}＝{w} の関係が成り立つ"
    else:
        reason = "取り除いても文の骨組みが成り立つ、時・場所・様態などを表す語句である"
    marked = " ".join(f"[[u:{x}]]" if k == i else x for k, (x, _) in enumerate(segs)) + "."
    others = [x for x in ("S", "O", "C", "M") if x != base]
    why = {ROLE_LABEL[o]: (f"{ROLE_LABEL[o]}は{ROLE_DEF[o]}。下線部 {w} は{reason}ので{ROLE_LABEL[base]}である。", f"{ROLE_LABEL[base]}と{ROLE_LABEL[o]}の区別")
           for o in others}
    return mc(f"次の英文の下線部は、文の要素として何にあたるか。最も適切なものを選びなさい。\n{marked}", [ROLE_LABEL[x] for x in ROLE_LABEL],
              f"下線部 {w} は{reason}。文全体は {analysis(segs)}（{PAT[p]}）。", d=2, keep=True, ai=list(ROLE_LABEL).index(base),
              ap="下線部が「なくても文が成り立つか」（M かどうか）、「主語や目的語とイコールの関係か」（C かどうか）を順に確かめる。",
              steps=[f"文の骨組みを分析する：{analysis(segs)}。", f"下線部 {w} の働きを確かめる：{reason}。", f"よって{ROLE_LABEL[base]}。"],
              alt=[f"和訳「{jp}」の中で、下線部がどの語句にあたり、どんな働きをしているかを確かめる。"],
              pc=[("下線部の働きを正しく説明できる", 1), ("文の要素を正しく答えている", 1)],
              pit=["形容詞の補語（C）を修飾語（M）と取り違える。", "前置詞＋名詞の中の名詞を目的語（O）とする。"], why=why)


TRANS = [
    ("We (　　) the station just before the train left.", "reached", "私たちは列車が出る直前に駅に着いた。",
     [("arrived", "arrive は自動詞なので、場所を表すには at が必要（arrived at the station）。"),
      ("got", "「～に着く」の get は自動詞で、to が必要（got to the station）。"),
      ("reached at", "reach は他動詞なので前置詞をつけずに目的語をとる。")]),
    ("Let's (　　) the plan for the school festival.", "discuss", "文化祭の計画について話し合おう。",
     [("discuss about", "discuss は他動詞なので about は不要。日本語の「～について」につられた誤り。"),
      ("talk", "talk は自動詞なので、話題を示すには about が必要（talk about the plan）。"),
      ("speak", "speak は話題を直接目的語にとらない。話題を示すには about が必要。")]),
    ("Ms. Tanaka (　　) a doctor from Kobe last spring.", "married", "田中さんは昨年の春、神戸出身の医師と結婚した。",
     [("married with", "marry は他動詞なので with は不要。「～と」につられた誤り。"),
      ("got married", "get married の後ろに相手を示すには to が必要（got married to）。"),
      ("married to", "married to は be married to「～と結婚している」の形で使う。動詞 marry は前置詞をつけない。")]),
    ("The students (　　) the hall one by one.", "entered", "生徒たちは1人ずつホールに入った。",
     [("entered into", "建物や部屋に入る意味の enter は他動詞で、into は不要。enter into は「（議論・契約など）を始める」の意味。"),
      ("went", "go は自動詞なので、場所を示すには into などの前置詞が必要。"),
      ("came", "come は自動詞なので、場所を示すには into などの前置詞が必要。")]),
    ("Please (　　) my question honestly.", "answer", "私の質問に正直に答えてください。",
     [("answer to", "動詞の answer は他動詞なので to は不要。「～に答える」の「に」につられた誤り。"),
      ("reply", "reply は自動詞なので、相手や質問を示すには to が必要（reply to my question）。"),
      ("respond", "respond は自動詞なので、to が必要（respond to my question）。")]),
    ("The boy (　　) his father in many ways.", "resembles", "その少年は多くの点で父親に似ている。",
     [("resembles to", "resemble は他動詞なので to は不要。「～に似ている」の「に」につられた誤り。"),
      ("resembles with", "resemble は他動詞なので with は不要。"),
      ("looks", "「～に似ている」の意味で look を使うときは like が必要（looks like his father）。")]),
    ("Our ship slowly (　　) the island.", "approached", "私たちの船はゆっくりとその島に近づいた。",
     [("approached to", "approach は他動詞なので to は不要。"),
      ("came", "come は自動詞なので、近づく先を示すには to や near などが必要。"),
      ("arrived", "arrive は自動詞で at / in が必要。また「着いた」になり「ゆっくり近づいた」という意味とも合わない。")]),
    ("He didn't (　　) the accident to anyone.", "mention", "彼はその事故のことをだれにも話さなかった。",
     [("mention about", "mention は他動詞なので about は不要。"),
      ("talk", "talk は自動詞で、話題を示すには about が必要。"),
      ("say", "say は発言の内容そのものを目的語にとり、話題（the accident）を目的語にはしない。")]),
    ("More than 300 people (　　) the meeting.", "attended", "300人を超える人がその会議に出席した。",
     [("attended to", "attend to は「～に注意を払う・～の世話をする」という別の意味になる。「出席する」の attend は他動詞。"),
      ("participated", "participate は自動詞なので in が必要（participated in the meeting）。"),
      ("took part", "take part の後ろに参加するものを示すには in が必要（took part in the meeting）。")]),
    ("Could you (　　) the rules of the game?", "explain", "そのゲームのルールを説明していただけますか。",
     [("explain about", "explain は他動詞なので about は不要。"),
      ("speak", "speak は自動詞で、ルールを直接目的語にとれない。"),
      ("talk", "talk は自動詞で、話題を示すには about が必要。")]),
    ("We (　　) about the trip all night.", "talked", "私たちは一晩中その旅行のことを話した。",
     [("discussed", "discuss は他動詞なので about と一緒には使わない（discussed the trip）。"),
      ("mentioned", "mention は他動詞なので about と一緒には使わない。"),
      ("considered", "consider は他動詞なので about と一緒には使わない。")]),
    ("Please (　　) me when you arrive in Tokyo.", "contact", "東京に着いたら私に連絡してください。",
     [("contact with", "動詞の contact は他動詞なので with は不要。"),
      ("get in touch", "get in touch の後ろに相手を示すには with が必要（get in touch with me）。"),
      ("reply", "reply は自動詞で to が必要。また「返事をする」で、文の意味にも合わない。")]),
    ("The plane (　　) at Narita Airport on time.", "arrived", "その飛行機は定刻に成田空港に到着した。",
     [("reached", "reach は他動詞なので前置詞 at をとらない（reached Narita Airport）。"),
      ("got", "「着く」の get は to をとる（got to Narita Airport）。at は使わない。"),
      ("entered", "enter は他動詞なので前置詞 at をとらない。また「入った」で意味も合わない。")]),
]


@gen("basic_check", 5, ["condition_check", "common_error"])
def trans_intrans(r):
    s, ok, jp, wrongs = r.choice(TRANS)
    return mc(f"日本語の意味になるように、（　）に入る最も適切なものを選びなさい。\n{jp}\n{s}", [ok] + [w for w, _ in wrongs],
              f"{ok} が入る。" + (f"{ok} は自動詞なので、後ろの前置詞とともに使う。" if ok in ("talked", "arrived") else
                                 f"{ok} は他動詞なので、前置詞をつけずに目的語をとる。"), d=2,
              ap="空所の後ろに名詞が直接続くか、前置詞が続くかを確認し、他動詞・自動詞のどちらが入るかを決める。",
              steps=["空所の直後を見て、名詞が直接続くか前置詞が続くかを確かめる。", "名詞が直接続くなら他動詞、前置詞が続くなら自動詞を選ぶ。",
                     f"選択肢の動詞の語法を確かめ、{ok} を選ぶ。"],
              alt=[f"選択肢を入れた英文を1つずつ読み、「動詞＋前置詞＋名詞」「動詞＋名詞」のどちらの形が正しいかを確かめる。"],
              pc=[("空所の後ろの形（名詞か前置詞か）を確認している", 1), ("動詞の語法から正しい語を選んでいる", 1)],
              pit=["日本語の「～について」「～に」「～と」につられて、他動詞に前置詞をつけてしまう。"],
              why={w: (reason, "自動詞と他動詞の区別") for w, reason in wrongs})


CONF = [
    ("The cat is (　　) on the sofa.", "lying", "猫がソファーの上で寝そべっている。",
     [("laying", "laying は他動詞 lay（横たえる）の ing 形で、目的語が必要。"),
      ("lay", "is の後ろで進行形にするには ing 形が必要。"),
      ("laid", "laid は lay（横たえる）の過去形・過去分詞で、is laid は「横たえられている」となり意味が合わない。")]),
    ("She (　　) her baby on the bed gently.", "laid", "彼女は赤ちゃんをそっとベッドに寝かせた。",
     [("lay", "lay は自動詞 lie の過去形（横になった）で、目的語 her baby をとれない。"),
      ("lied", "lied は「嘘をついた」の lie の過去形。"),
      ("lain", "lain は lie の過去分詞で、単独で過去の動詞としては使えない。")]),
    ("He (　　) down under a tree and slept for an hour.", "lay", "彼は木の下で横になり、1時間眠った。",
     [("laid", "laid は他動詞 lay（横たえる）の過去形で、目的語が必要。"),
      ("lied", "lied は「嘘をついた」の意味。"),
      ("lain", "lain は過去分詞なので、have などがなければ使えない。")]),
    ("The sun has already (　　).", "risen", "太陽はもう昇っている。",
     [("raised", "raised は他動詞 raise（上げる）の過去分詞で、目的語が必要。"),
      ("rose", "rose は過去形。has の後ろには過去分詞が必要。"),
      ("rised", "rise は不規則動詞で、rised という形はない。")]),
    ("Prices (　　) sharply last year.", "rose", "昨年、物価が急激に上がった。",
     [("raised", "raised は他動詞 raise の過去形で、目的語が必要。"),
      ("risen", "risen は過去分詞で、単独で過去の動詞としては使えない。"),
      ("rised", "rise は不規則動詞で、rised という形はない。")]),
    ("If you have a question, (　　) your hand.", "raise", "質問があれば手を挙げなさい。",
     [("rise", "rise は自動詞で、目的語 your hand をとれない。"),
      ("rose", "rose は rise の過去形。命令文には原形が必要で、しかも自動詞。"),
      ("arise", "arise は「（問題などが）生じる」という自動詞で、目的語をとれない。")]),
    ("Please (　　) down and wait for a moment.", "sit", "どうぞ座って少しお待ちください。",
     [("seat", "seat は他動詞（座らせる）で、目的語が必要（seat yourself）。"),
      ("sat", "命令文には原形が必要。sat は過去形・過去分詞。"),
      ("seated", "seated は seat の過去形・過去分詞で、命令文の動詞としては使えない。")]),
    ("The company was (　　) in 1950 by two brothers.", "founded", "その会社は1950年に2人の兄弟によって設立された。",
     [("found", "found（find の過去分詞）だと「発見された」となり、意味が通らない。「設立する」は found – founded – founded。"),
      ("finded", "find は不規則動詞で finded という形はない。"),
      ("founding", "was founding は進行形で、「設立されていた」という受け身の意味にならない。")]),
    ("Many leaves have (　　) on the ground.", "fallen", "たくさんの葉が地面に落ちている。",
     [("felled", "felled は「（木を）切り倒す」という他動詞 fell の過去分詞。"),
      ("fell", "fell は fall の過去形。have の後ろには過去分詞が必要。"),
      ("falled", "fall は不規則動詞で falled という形はない。")]),
    ("She has (　　) the book on the desk.", "laid", "彼女はその本を机の上に置いた。",
     [("lain", "lain は自動詞 lie の過去分詞で、目的語 the book をとれない。"),
      ("lay", "has の後ろには過去分詞が必要。lay は lie の過去形または lay の原形。"),
      ("lied", "lied は「嘘をつく」の lie の過去分詞。")]),
    ("Don't (　　) to me. I know the truth.", "lie", "私に嘘をつかないで。本当のことは知っているのだから。",
     [("lay", "lay は「横たえる・置く」の意味の他動詞（または lie の過去形）で、「嘘をつく」の意味はない。"),
      ("lied", "Don't の後ろには原形が必要。"),
      ("lying", "Don't の後ろには原形が必要。")]),
    ("The smoke was slowly (　　) into the sky.", "rising", "煙がゆっくりと空へ立ち昇っていた。",
     [("raising", "raising は他動詞 raise の ing 形で、目的語が必要。"),
      ("rose", "was の後ろで進行形にするには ing 形が必要。"),
      ("risen", "was risen という受け身の形は、自動詞 rise ではつくれない。")]),
]


@gen("basic_check", 5, ["computation", "common_error"])
def confusing_verbs(r):
    s, ok, jp, wrongs = r.choice(CONF)
    return mc(f"（　）に入る最も適切なものを選びなさい。\n{s}\n（意味：{jp}）", [ok] + [w for w, _ in wrongs],
              f"{ok} が入る。目的語の有無で自動詞・他動詞を決め、前後の形（have／be／命令文など）から活用形を選ぶ。", d=2,
              ap="①空所の後ろに目的語があるか（自動詞か他動詞か）、②空所の前に have・be 動詞などがあるか（原形・過去形・過去分詞・ing 形のどれか）、の2段階で考える。",
              steps=["空所の後ろに目的語があるかを確かめ、自動詞か他動詞かを決める。", "空所の前の形（have／be／Don't／過去の時を表す語句）から必要な活用形を決める。",
                     f"両方の条件を満たす {ok} を選ぶ。"],
              alt=["lie – lay – lain、lay – laid – laid、rise – rose – risen、raise – raised – raised の活用表を書き出し、条件に合う形を表から探す。"],
              pc=[("自動詞・他動詞を正しく判断している", 1), ("活用形を正しく選んでいる", 1)],
              pit=["lie の過去形 lay と、他動詞 lay の原形を取り違える。", "不規則動詞に -ed をつけてしまう。"],
              why={w: (reason, "紛らわしい動詞の意味・活用の混同") for w, reason in wrongs})


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 5, ["concept", "application"])
def same_pattern(r):
    p = r.choice(list(PAT))
    tgt = r.choice(by_pattern(p))
    rr = local(text(tgt[1]))
    ok = rr.choice([s for s in by_pattern(p) if s is not tgt])
    others = rr.sample([q for q in PAT if q != p], 3)
    wrongs = [(q, rr.choice(by_pattern(q))) for q in others]
    why = {text(s[1]): (f"この文は {analysis(s[1])} で{PAT[q]}。問題文は{PAT[p]}なので文型が異なる。", f"{PAT[q]}と{PAT[p]}の混同") for q, s in wrongs}
    return mc(f"次の英文と同じ文型の英文を、選択肢から1つ選びなさい。\n{text(tgt[1])}", [text(ok[1])] + [text(s[1]) for _, s in wrongs],
              f"問題文は {analysis(tgt[1])} で{PAT[p]}。{text(ok[1])} も {analysis(ok[1])} で{PAT[p]}。", d=3,
              ap="問題文の文型を先に決め、選択肢はそれぞれ M を取り除いて骨組みだけを比べる。",
              steps=[f"問題文を分析する：{analysis(tgt[1])} → {PAT[p]}。", "選択肢を1つずつ同じ手順で分析する。", f"{PAT[p]}になっている {text(ok[1])} を選ぶ。"],
              alt=["選択肢の動詞の後ろにある要素の数と、イコールの関係の有無だけを素早くメモして比べる。"],
              pc=[("問題文の文型を正しく判断している", 2), ("選択肢の文型を正しく判断して選んでいる", 2)],
              pit=["動詞が同じかどうか（made と made など）で判断してしまう。", "修飾語（M）を要素として数える。"],
              why=why)


TOFOR = [
    ("My aunt", "sent", "me", "a birthday card", "to"), ("Ken", "lent", "me", "his umbrella", "to"),
    ("She", "showed", "the visitors", "the way to the museum", "to"), ("Mr. Brown", "teaches", "us", "English", "to"),
    ("My grandfather", "told", "us", "an interesting story", "to"), ("Emi", "gave", "her brother", "a watch", "to"),
    ("I", "wrote", "my friend", "a long letter", "to"), ("He", "passed", "me", "the salt", "to"),
    ("My father", "bought", "me", "a new bike", "for"), ("My mother", "made", "us", "lunch", "for"),
    ("He", "cooked", "his family", "dinner", "for"), ("She", "found", "me", "a good seat", "for"),
    ("Mr. Tanaka", "chose", "his daughter", "a nice dress", "for"), ("My uncle", "built", "his son", "a tree house", "for"),
]
TO_WHY = "相手がいないと成り立たない動作（相手への移動を表す）なので to"
FOR_WHY = "相手がいなくても成り立つ動作を、相手のために行うので for"


@gen("standard_practice", 5, ["computation", "condition_check"])
def svoo_to_svo(r):
    S, V, O1, O2, prep = r.choice(TOFOR)
    ans = f"{S} {V} {O2} {prep} {O1}."
    why_p = TO_WHY if prep == "to" else FOR_WHY
    return sa(f"次の英文を、ほぼ同じ意味の第3文型（SVO）の英文に書きかえなさい。\n{S} {V} {O1} {O2}.", ans,
              f"{V} は{why_p}を使う。O₂（{O2}）を動詞の直後に置き、O₁（{O1}）を {prep} の後ろに回す。", d=2,
              ap="第4文型の O₁（人）と O₂（物）を入れかえ、人の前に前置詞を置く。前置詞は動詞の意味（相手が必要な動作か）で決める。",
              steps=[f"O₁＝{O1}、O₂＝{O2} を確認する。", f"{V} は{why_p}。", f"{S} {V} {O2} {prep} {O1}. とする。"],
              alt=[f"「{prep} 型」の代表的な動詞（{'give, send, show, lend, teach, tell' if prep == 'to' else 'buy, make, cook, find, get, choose'}）の一覧と照合して前置詞を確かめる。"],
              pc=[("語順（O₂ → 前置詞 → O₁）が正しい", 2), ("前置詞（to / for）を正しく選んでいる", 2)],
              pit=["前置詞を逆にする（bought a bike to me など）。", "O₁ と O₂ を入れかえずに前置詞だけ加える。"])


MEANING = [
    ("Please call me a taxi.", "タクシーを呼んでください。",
     [("私をタクシーと呼んでください。", "SVOC と読むと me＝a taxi となり意味が通らない。me と a taxi は別のものなので SVOO（私にタクシーを呼ぶ）。"),
      ("タクシーで私に電話してください。", "a taxi の前に by などの前置詞がなく、「タクシーで」という手段の意味にはならない。"),
      ("私がタクシーを呼びましょう。", "Please で始まる命令文で、動作をするのは相手であり、話し手ではない。")]),
    ("Please call me Ken.", "私をケンと呼んでください。",
     [("私にケンを呼んでください。", "SVOO と読むと me と Ken が別人になるが、ここは me＝Ken の SVOC で「O を C と呼ぶ」。"),
      ("ケンに電話してください。", "me が目的語なので、電話する相手はケンではない。また me＝Ken の関係を無視している。"),
      ("ケンが私を呼んでいます。", "Please で始まる命令文で、Ken は主語ではない。")]),
    ("I found the test easy.", "そのテストは簡単だとわかった。",
     [("そのテストを簡単に見つけた。", "「簡単に」は副詞 easily の意味。easy は形容詞で、the test＝easy の SVOC。"),
      ("簡単なテストを見つけた。", "easy は the test を前から修飾していない。O＝C の関係なので「O が C だとわかる」。"),
      ("そのテストで簡単なものを見つけた。", "the test は find の目的語で、「テストで」という場所・手段の意味にはならない。")]),
    ("She made him a cake.", "彼女は彼にケーキを作ってあげた。",
     [("彼女は彼をケーキにした。", "SVOC と読むと him＝a cake となり意味が通らない。him と a cake は別のものなので SVOO。"),
      ("彼女は彼といっしょにケーキを作った。", "「いっしょに」を表す with がない。him は「彼に」にあたる目的語。"),
      ("彼女は彼にケーキを作らせた。", "「～させる」の make は make＋O＋動詞の原形の形をとる。a cake は名詞で動詞ではない。")]),
    ("Her words made him angry.", "彼女の言葉で彼は怒った。",
     [("彼女は怒って彼に話しかけた。", "主語は Her words で、怒ったのは him（him＝angry の SVOC）。"),
      ("彼女の言葉は彼に怒りを作り出させた。", "angry は形容詞で目的語になれない。make O C「O を C にする」の SVOC。"),
      ("彼は怒って彼女の言葉を書き直した。", "主語・目的語の関係が逆で、made を「書き直した」と読む根拠もない。")]),
    ("Leave me alone.", "私をひとりにしておいて。",
     [("私もひとりで出かけます。", "主語のない命令文であり、話し手が出かけるという意味ではない。alone は me の状態を表す補語（me＝alone）。"),
      ("ひとりで私のところを去りなさい。", "alone は me の状態を表す補語（me＝alone）で、相手の様子を表しているのではない。"),
      ("私にひとつ残しておいて。", "alone は「ひとつ」という意味の名詞ではない。SVOO と取り違えている。")]),
    ("Leave me some cake.", "ケーキを少し残しておいてね。",
     [("私をケーキのままにしておいて。", "SVOC と読むと me＝some cake となり意味が通らない。me と some cake は別のものなので SVOO。"),
      ("ケーキを持って私から離れて。", "「持って」を表す with がない。me は「私に」にあたる目的語。"),
      ("私はケーキを少し残した。", "主語のない命令文であり、残すのは相手である。")]),
    ("He grew tall.", "彼は背が高くなった。",
     [("彼は背の高いものを育てた。", "tall は形容詞で目的語になれない。grow＋形容詞は SVC で「～になる」。"),
      ("彼は高いところで育った。", "「高いところで」を表す前置詞句はない。tall は主語の状態を表す補語。"),
      ("彼は背の高さを伸ばそうとした。", "grew は過去形の事実を表し、「～しようとした」という意味はない。")]),
    ("He grew tomatoes.", "彼はトマトを育てた。",
     [("彼はトマトになった。", "SVC と読むと He＝tomatoes となり意味が通らない。tomatoes は目的語で SVO。"),
      ("彼はトマトのように大きくなった。", "「～のように」を表す like がない。"),
      ("彼はトマトで成長した。", "「～で」を表す前置詞がなく、tomatoes は grew の目的語である。")]),
    ("She appeared calm.", "彼女は落ち着いているように見えた。",
     [("彼女は静かに現れた。", "「静かに」と様態を表すなら副詞 calmly になる。calm は形容詞で、主語の状態を表す補語（SVC）。"),
      ("彼女は落ち着いた人を連れて現れた。", "calm は名詞を修飾しておらず、連れてくる意味もない。"),
      ("落ち着いた彼女が現れたのは意外だった。", "「意外だった」にあたる語はない。appear＋形容詞は「～のように見える」。")]),
    ("The leaves turned yellow.", "葉が黄色くなった。",
     [("葉が黄色いものを回した。", "yellow は形容詞で、turn の目的語ではない。turn＋形容詞は SVC で「～になる」。"),
      ("葉が黄色い方へ向いた。", "「～の方へ」を表す前置詞 to / toward がない。"),
      ("黄色い葉が向きを変えた。", "yellow は leaves を前から修飾していない。動詞の後ろの補語である。")]),
    ("She turned the page.", "彼女はページをめくった。",
     [("彼女はページになった。", "SVC と読むと She＝the page となり意味が通らない。the page は目的語で SVO。"),
      ("彼女はページの方を向いた。", "「～の方を」を表す to / toward がない。the page は turned の目的語。"),
      ("ページが彼女の方に向いた。", "主語は She で、動作をしたのは彼女である。")]),
]


@gen("standard_practice", 5, ["concept", "condition_check"])
def meaning(r):
    s, ok, wrongs = r.choice(MEANING)
    return mc(f"次の英文の意味として最も適切なものを選びなさい。\n{s}", [ok] + [w for w, _ in wrongs],
              f"「{ok}」が正しい。動詞の後ろの要素がイコールの関係か、別のものかで文型と意味が決まる。", d=3,
              ap="動詞の後ろの語句を確かめ、「S＝C」「O＝C」の関係があるか、2つの目的語が別のものかを判断してから訳す。",
              steps=["動詞と、その後ろの語句を確認する。", "be 動詞をはさんでイコールの関係が成り立つかを試す。", f"文型に合った訳「{ok}」を選ぶ。"],
              alt=["選択肢の和訳を英語の文型に戻してみて、問題文の語順・品詞と一致するかを確かめる。"],
              pc=[("文型を正しく判断している", 2), ("文型に合う意味を選んでいる", 2)],
              pit=["同じ動詞の別の文型の意味（call「呼ぶ」と「電話する」など）と取り違える。", "形容詞の補語を副詞のように訳す。"],
              why={w: (reason, "文型の取り違えによる誤訳") for w, reason in wrongs})


ORDERS = [
    ("このアプリを使えば、かなりの時間を節約できるだろう。", ["this app", "will", "save", "you", "a lot of", "time"], "SVOO（save O₁ O₂「O₁ の O₂ を省く」）"),
    ("その長い会議で、私たちはみんなとても疲れた。", ["the long meeting", "made", "all of us", "very", "tired"], "SVOC（make O C「O を C にする」）"),
    ("窓を開けたままにしておいてはいけません。", ["you", "must not", "leave", "the window", "open"], "SVOC（leave O C「O を C のままにしておく」）"),
    ("私たちはその赤ちゃんをハナと名づけた。", ["we", "named", "the", "baby", "Hana"], "SVOC（name O C「O を C と名づける」）"),
    ("祖母が私に手編みのセーターを送ってくれた。", ["my grandmother", "sent", "me", "a", "hand-knitted", "sweater"], "SVOO（send O₁ O₂）"),
    ("その問題はかなり簡単だとわかった。", ["I", "found", "the problem", "quite", "easy"], "SVOC（find O C「O が C だとわかる」）"),
    ("部屋はきれいにしておくべきだ。", ["you", "should", "keep", "your room", "clean"], "SVOC（keep O C「O を C にしておく」）"),
    ("このスープは少ししょっぱすぎる。", ["this soup", "tastes", "a little", "too", "salty"], "SVC（taste＋形容詞「～の味がする」）"),
    ("駅までの道を教えていただけますか。", ["could", "you", "tell", "me", "the way", "to the station"], "SVOO（tell O₁ O₂）"),
    ("先生は私たちに宿題を出さなかった。", ["our teacher", "didn't", "give", "us", "any", "homework"], "SVOO（give O₁ O₂）"),
    ("私たちは文化祭の計画について話し合った。", ["we", "discussed", "the plan", "for", "the school festival"], "SVO（discuss は他動詞で about は不要）"),
    ("子どもたちはとても静かにしていた。", ["the", "children", "kept", "very", "quiet"], "SVC（keep＋形容詞「～のままでいる」）"),
    ("彼らはユキをチームのキャプテンに選んだ。", ["they", "elected", "Yuki", "captain of", "the team"], "SVOC（elect O C「O を C に選ぶ」）"),
]


@gen("standard_practice", 5, ["application", "computation"])
def build_order(r):
    jp, parts, pat = r.choice(ORDERS)
    sent = " ".join(parts)
    return order(f"日本語に合うように、語句を並べかえて英文を完成させなさい。ただし、文頭にくる語も小文字で示してある。\n{jp}", parts,
                 f"{sent[0].upper() + sent[1:]}{'?' if parts[0] == 'could' else '.'}　文型は{pat}。", d=3, p=4,
                 ap="日本語から文型を先に決め、S → V → 残りの要素の順に並べる。最後に修飾語の位置を決める。",
                 steps=[f"文型を決める：{pat}。", "主語と動詞（助動詞を含む）を先頭に置く。", "目的語・補語を文型の順に並べる。", f"完成文：{sent}"],
                 alt=["完成した英文を和訳し直して、日本語と一致するかを確かめる。"],
                 pc=[("文型に合う語順で主語・動詞を並べている", 2), ("目的語・補語の順序が正しい", 2)],
                 pit=["SVOO の2つの目的語の順を逆にする。", "SVOC の補語を動詞の直後に置く。"])


# ======================================================================
# C 思考力・記述応用
# ======================================================================

PAIRS = [
    ("I found the book easy.", "I found the book easily.",
     "Aは SVOC で the book＝easy の関係があり「その本は簡単だとわかった」。Bは SVO＋M で easily は動詞 found を修飾し「その本を簡単に見つけた」。形容詞 easy は補語になれるが、副詞 easily は補語になれず修飾語として働く。"),
    ("Please call me a taxi.", "Please call me Ken.",
     "Aは SVOO で me と a taxi は別のものなので「私にタクシーを呼んでください」。Bは SVOC で me＝Ken の関係があり「私をケンと呼んでください」。2つの名詞がイコールかどうかで文型と call の意味が変わる。"),
    ("She made him a sandwich.", "She made him angry.",
     "Aは SVOO で him と a sandwich は別のものなので「彼女は彼にサンドイッチを作ってあげた」。Bは SVOC で him＝angry の関係があり「彼女は彼を怒らせた」。"),
    ("Leave me some cake.", "Leave me alone.",
     "Aは SVOO で me と some cake は別のものなので「ケーキを少し残しておいて」。Bは SVOC で me＝alone の関係があり「私をひとりにしておいて」。"),
    ("He grew tall.", "He grew tomatoes.",
     "Aは SVC で He＝tall の関係があり、grow は「～になる」の意味で「彼は背が高くなった」。Bは SVO で tomatoes は目的語、grow は「～を育てる」の意味で「彼はトマトを育てた」。"),
    ("She appeared calm.", "She appeared at the door.",
     "Aは SVC で She＝calm の関係があり「彼女は落ち着いているように見えた」。Bは SV で at the door は修飾語、appear は「現れる」の意味で「彼女は戸口に現れた」。"),
    ("The leaves turned yellow.", "She turned the page.",
     "Aは SVC で The leaves＝yellow の関係があり「葉が黄色くなった」。Bは SVO で the page は目的語、turn は「～をめくる」の意味で「彼女はページをめくった」。"),
    ("He kept quiet.", "He kept a diary.",
     "Aは SVC で He＝quiet の関係があり「彼は黙っていた」。Bは SVO で a diary は目的語で、He＝a diary は成り立たず「彼は日記をつけていた」。"),
    ("He got angry.", "He got a letter.",
     "Aは SVC で He＝angry の関係があり、get は「～になる」の意味で「彼は怒った」。Bは SVO で a letter は目的語、get は「～を受け取る」の意味で「彼は手紙を受け取った」。"),
    ("She left the room.", "She left the room clean.",
     "Aは SVO で「彼女は部屋を出た」。Bは SVOC で the room＝clean の関係があり、leave O C「O を C のままにしておく」の意味で「彼女は部屋をきれいなままにしておいた」。"),
]


@gen("thinking_writing", 4, ["written_reasoning", "concept"])
def explain_difference(r):
    a, b, model = r.choice(PAIRS)
    return desc(f"次の2つの英文A・Bの意味の違いを、それぞれの文型（文の要素）に触れながら日本語で説明しなさい。\nA：{a}\nB：{b}", model,
                "動詞は同じでも、後ろに続く要素の種類と、要素どうしがイコールの関係にあるかで文型が変わり、動詞の意味も変わる。",
                [("Aの文型を正しく判断し、根拠（イコールの関係の有無・品詞）を示している", 3), ("Bの文型を正しく判断し、根拠を示している", 3), ("A・Bの和訳がそれぞれ正しい", 2)], d=4, p=8, lines=6,
                ap="それぞれの文で V の後ろの要素を確認し、be 動詞をはさんでイコールの関係が成り立つかを試す。品詞（形容詞か副詞か、名詞か）にも注目する。",
                steps=["Aの動詞の後ろの要素を分析し、文型を決める。", "Bについても同じように分析する。", "文型の違いから、動詞の意味・和訳の違いを説明する。"],
                alt=["それぞれの文を別の言い方に書きかえて違いを示す方法もある（例：SVOO なら前置詞を使った SVO に、SVOC なら that 節や be 動詞の文に言いかえる）。"],
                pc=[("Aの文型と根拠", 3), ("Bの文型と根拠", 3), ("和訳", 2)],
                pit=["和訳だけを書き、文型の根拠を示さない。", "形容詞の補語を副詞のように訳す。"])


CAUS = [
    ("My mother made me (　　) my room.", "clean", "clean", "make＋O＋動詞の原形で「O に～させる」。O（me）が自分で掃除する（能動の関係）なので原形。", []),
    ("I heard my name (　　) from behind.", "call", "called", "hear＋O＋過去分詞で「O が～されるのを聞く」。my name は「呼ばれる」側（受け身の関係）なので過去分詞。", []),
    ("She had her bike (　　) at the shop.", "repair", "repaired", "have＋O＋過去分詞で「O を～してもらう」。her bike は「修理される」側（受け身の関係）なので過去分詞。", []),
    ("Let me (　　) you with your bags.", "help", "help", "let＋O＋動詞の原形で「O に（望みどおり）～させる」。O（me）が手伝う（能動の関係）なので原形。", []),
    ("We kept the fire (　　) all night.", "burn", "burning", "keep＋O＋現在分詞で「O を～している状態にしておく」。the fire が燃え続けている（能動・進行の関係）なので現在分詞。", []),
    ("I saw a boy (　　) across the street.", "run", "run", "see＋O＋原形で「O が～するのを（最初から最後まで）見る」。O（a boy）が走る（能動の関係）。進行中の場面を強調するなら現在分詞 running も可。", ["running"]),
    ("My parents want me (　　) a doctor.", "become", "to become", "want＋O＋to 不定詞で「O に～してほしい」。want は原形不定詞をとらない。", []),
    ("He got his brother (　　) him with his homework.", "help", "to help", "get＋O＋to 不定詞で「O に～してもらう」。get は make・have と違って to 不定詞をとる。", []),
    ("Please keep the door (　　).", "lock", "locked", "keep＋O＋過去分詞で「O を～された状態にしておく」。the door は「鍵をかけられる」側（受け身の関係）なので過去分詞。", []),
    ("I'll have the waiter (　　) us some water.", "bring", "bring", "have＋O＋動詞の原形で「O に～してもらう」。O（the waiter）が持ってくる（能動の関係）なので原形。", []),
]


@gen("thinking_writing", 3, ["cross_unit", "written_reasoning"], rel=["JH-ENG-G3-U04", "HS-ENG-U05"])
def causative_form(r):
    s, base, ans, why_s, alts = r.choice(CAUS)
    return desc(f"（　）内の動詞を適切な形に直して空所に入れなさい。また、その形を選んだ理由を、目的語（O）と補語（C）の関係に触れて説明しなさい。\n{s}　（{base}）",
                f"{ans}。{why_s}", f"第5文型 SVOC の C には、形容詞・名詞のほか、原形不定詞・to 不定詞・分詞が入る。{why_s}",
                [("適切な形を答えている", 3), ("O と C の関係（能動か受け身か）を説明している", 3), ("動詞の語法（原形・to 不定詞・分詞のどれをとるか）に触れている", 2)], d=4, p=8, lines=5,
                ap="第5文型の C に動詞が入るときは、①O が動作をする側か、される側か、②文の動詞がどの形（原形・to 不定詞・分詞）をとるか、の2点で形を決める。",
                steps=["文の動詞と O を確認する。", "O と C の関係が能動か受け身かを判断する。", "動詞の語法と合わせて形を決める。", f"答え：{ans}" + (f"（{'・'.join(alts)} も可）" if alts else "")],
                alt=["O と C の部分を独立した文にしてみる（例：I clean my room. ／ My name is called.）と、能動か受け身かがはっきりする。"],
                pc=[("適切な形", 3), ("O と C の関係の説明", 3), ("動詞の語法への言及", 2)],
                pit=["make・let・have の後ろに to をつける。", "O が「される」側なのに原形や現在分詞を入れる。"])


PASSIVE = [
    ("We call [[u:this bird]] a kiwi.", "This bird is called a kiwi.", "SVOC の O（this bird）が主語になり、C（a kiwi）は is called の後ろにそのまま残る。行為者が一般の人々なので by us は省くのが普通。",
     ["This bird is called a kiwi by us."]),
    ("Someone left [[u:the window]] open.", "The window was left open.", "SVOC の O（the window）が主語になり、C（open）は was left の後ろに残る。行為者が不明なので by someone は省く。",
     ["The window was left open by someone."]),
    ("The members elected [[u:Yuki]] captain.", "Yuki was elected captain by the members.", "SVOC の O（Yuki）が主語になり、C（captain）は was elected の後ろに残る。",
     ["Yuki was elected captain."]),
    ("Mr. Brown teaches [[u:us]] English.", "We are taught English by Mr. Brown.", "SVOO の O₁（us）を主語にすると、主格 We に変わり、O₂（English）は are taught の後ろに残る。", []),
    ("My aunt gave [[u:me]] this watch.", "I was given this watch by my aunt.", "SVOO の O₁（me）を主語にすると主格 I に変わり、O₂（this watch）は was given の後ろに残る。", []),
    ("My aunt gave me [[u:this watch]].", "This watch was given to me by my aunt.", "SVOO の O₂（this watch）を主語にすると、残った O₁ の前には to を置くのが普通（give は to 型の動詞）。",
     ["This watch was given me by my aunt."]),
    ("My father bought me [[u:this bike]].", "This bike was bought for me by my father.", "buy のような for 型の動詞は、O₂（物）を主語にした受け身が普通で、残った O₁ の前に for を置く。O₁（人）を主語にした受け身は一般に使わない。", []),
    ("The news made [[u:everyone]] happy.", "Everyone was made happy by the news.", "SVOC の O（everyone）が主語になり、C（happy）は was made の後ろに残る。", []),
    ("They made [[u:him]] wait for an hour.", "He was made to wait for an hour.", "make＋O＋原形の受け身では、原形が to 不定詞に変わる（was made to wait）。行為者 by them は省くのが普通。",
     ["He was made to wait for an hour by them."]),
    ("We found [[u:the box]] empty.", "The box was found empty.", "SVOC の O（the box）が主語になり、C（empty）は was found の後ろに残る。行為者 by us は省くのが普通。", ["The box was found empty by us."]),
]


@gen("thinking_writing", 3, ["cross_unit", "condition_check"], rel=["JH-ENG-G2-U05"])
def passive_rewrite(r):
    s, ans, why_s, v = r.choice(PASSIVE)
    return desc(f"次の英文を、下線部を主語にした受け身の文に書きかえなさい。また、書きかえによって文の要素（O・C）がどうなるかを説明しなさい。\n{s}",
                f"{ans}　{why_s}", f"受け身にできるのは目的語（O）だけで、補語（C）は主語にならない。{why_s}",
                [("受け身の文を正しく書いている（be 動詞の時制・過去分詞）", 4), ("残った O・C の位置や前置詞の扱いを説明している", 3), ("行為者（by ～）の扱いが適切である", 1)], d=4, p=8, lines=5,
                ap="受け身の主語になれるのは能動態の目的語（O）。主語にしなかった O や C は be＋過去分詞の後ろにそのまま残る。",
                steps=["下線部が O であることを確認する（C は主語にできない）。", "元の文の時制に合わせて be 動詞を決め、動詞を過去分詞にする。",
                       "残った要素（O または C）を過去分詞の後ろに置く。必要なら前置詞（to / for）や to 不定詞にする。", f"答え：{ans}"],
                alt=["書きかえた文を能動態に戻して、元の文と同じ意味になるかを確かめる。"],
                pc=[("受け身の形", 4), ("O・C の扱いの説明", 3), ("行為者の扱い", 1)],
                pit=["make＋O＋原形の受け身で to を落とす（He was made wait）。", "for 型の動詞で人を主語にした受け身を作る。"], v=v)


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(task, wrong, step, etype, tempt, fix, ans, expl, steps, ap, alt, pit, d=3):
    return desc(f"{task}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい英文に書き直しなさい。", ans, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい英文に直している", 3), ("語法の規則を説明している", 1)], d=d, p=6, lines=5,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい英文", 3), ("規則の説明", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix))


TRANS_ERR = [
    ("私たちは放課後その問題について話し合った。", "We discussed about the problem after school.", "We discussed the problem after school.", "discuss about", "discuss は他動詞", "「～について」につられて about を加えた。"),
    ("彼女は昨年、幼なじみと結婚した。", "She married with her childhood friend last year.", "She married her childhood friend last year.", "married with", "marry は他動詞", "「～と結婚する」の「と」につられて with を加えた。"),
    ("私たちは正午に頂上に着いた。", "We reached to the top at noon.", "We reached the top at noon.", "reached to", "reach は他動詞", "同じ意味の get to・arrive at との混同で前置詞を加えた。"),
    ("その少年は父親にとてもよく似ている。", "The boy resembles to his father very much.", "The boy resembles his father very much.", "resembles to", "resemble は他動詞", "「～に似ている」の「に」につられて to を加えた。"),
    ("先生はその規則を私たちに説明してくれた。", "Our teacher explained about the rule to us.", "Our teacher explained the rule to us.", "explained about", "explain は他動詞", "「～について説明する」という日本語につられて about を加えた。"),
    ("生徒たちは静かに教室に入った。", "The students entered into the classroom quietly.", "The students entered the classroom quietly.", "entered into", "「（場所）に入る」の enter は他動詞", "go into・come into との混同で into を加えた。"),
    ("彼はその事故のことには一言も触れなかった。", "He didn't mention about the accident at all.", "He didn't mention the accident at all.", "mention about", "mention は他動詞", "talk about との混同で about を加えた。"),
    ("私たちは10時に駅に着いた。", "We arrived the station at ten.", "We arrived at the station at ten.", "arrived the station", "arrive は自動詞で、場所の前に at / in が必要", "同じ意味の reach（他動詞）との混同で前置詞を落とした。"),
    ("明日、私に連絡してください。", "Please contact with me tomorrow.", "Please contact me tomorrow.", "contact with", "動詞の contact は他動詞", "get in touch with・名詞の contact with との混同で with を加えた。"),
    ("私たちはその計画について話した。", "We talked the plan.", "We talked about the plan.", "talked the plan", "talk は自動詞で、話題の前に about が必要", "同じ意味の discuss（他動詞）との混同で前置詞を落とした。"),
]


@gen("error_correction", 4, ["common_error", "condition_check"])
def err_transitive(r):
    jp, wrong, fix, where, rule, tempt = r.choice(TRANS_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", "concept", tempt, fix, fix,
                    f"{rule}。正しくは {fix}",
                    [f"動詞の語法を確認する：{rule}。", f"「{where}」の部分を直す。", f"正しい英文：{fix}"],
                    "日本語の助詞（「に」「と」「について」）ではなく、英語の動詞が目的語を直接とるか（他動詞か自動詞か）で前置詞の有無を決める。",
                    ["同じ意味の自動詞・他動詞のペア（discuss ／ talk about、reach ／ arrive at など）を並べて確認する。"],
                    ["日本語の助詞をそのまま前置詞に置きかえる。"], d=3)


LIE_ERR = [
    ("彼は木の下で横になった。", "He laid down under a tree.", "He lay down under a tree.", "laid", "concept",
     "「横になる」は自動詞 lie で、過去形は lay。laid は他動詞 lay（横たえる）の過去形で、目的語が必要。", "lie の過去形 lay と他動詞 lay が同じつづりなので、さらに過去形にしようとして laid とした。"),
    ("彼女は赤ちゃんをベッドに寝かせた。", "She lay her baby on the bed.", "She laid her baby on the bed.", "lay", "concept",
     "目的語 her baby をとるので他動詞 lay（横たえる）を使い、過去形は laid。lay は自動詞 lie の過去形で目的語をとれない。", "「寝る」から自動詞 lie を連想し、その過去形 lay を使った。"),
    ("物価が急に上がった。", "Prices raised suddenly.", "Prices rose suddenly.", "raised", "concept",
     "目的語がないので自動詞 rise（上がる）を使い、過去形は rose。raise は「～を上げる」の他動詞。", "rise と raise の意味の区別があいまいで、規則変化の raised を選んだ。"),
    ("質問がある人は手を挙げてください。", "Please rise your hand if you have a question.", "Please raise your hand if you have a question.", "rise", "concept",
     "目的語 your hand をとるので他動詞 raise を使う。rise は自動詞で目的語をとれない。", "「挙げる（上がる）」という意味だけで rise を選んだ。"),
    ("猫がソファーの上で寝そべっている。", "The cat is laying on the sofa.", "The cat is lying on the sofa.", "laying", "concept",
     "目的語がないので自動詞 lie を使い、ing 形は lying。laying は他動詞 lay の ing 形。", "lie の ing 形 lying（ie → y）のつづりに自信がなく、lay の ing 形 laying を使った。"),
    ("太陽はすでに昇っていた。", "The sun had already rose.", "The sun had already risen.", "rose", "notation",
     "had の後ろは過去分詞。rise の活用は rise – rose – risen。", "過去の出来事なので過去形を使えばよいと考え、過去完了の形（had＋過去分詞）を確認しなかった。"),
    ("どうぞおかけください。", "Please seat.", "Please sit down.", "seat", "concept",
     "seat は「～を座らせる」という他動詞で、目的語が必要。自分が座るなら sit を使う（Please be seated. / Please seat yourself. も可）。", "「着席」の seat という名詞のイメージから、自動詞のように使った。"),
]


@gen("error_correction", 3, ["common_error", "computation"])
def err_lie_lay(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(LIE_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"動詞「{where}」", etype, tempt, fix, fix, rule,
                    ["目的語があるかどうかを確認し、自動詞か他動詞かを決める。", "前後の形（過去・完了・進行・命令）から活用形を決める。", f"正しい英文：{fix}"],
                    "紛らわしい動詞は、①目的語の有無（自動詞か他動詞か）、②必要な活用形、の順に確かめる。",
                    ["lie – lay – lain – lying、lay – laid – laid – laying、rise – rose – risen、raise – raised – raised の活用表と照合する。"],
                    ["lie の過去形 lay と他動詞 lay を取り違える。"], d=3)


SVOO_ERR = [
    ("母は私に新しいかばんを買ってくれた。", "My mother bought a new bag to me.", "My mother bought a new bag for me.", "to me", "condition",
     "buy は相手がいなくても成り立つ動作なので、第3文型では for を使う（My mother bought me a new bag. も可）。", "第4文型の書きかえは「to を使う」とまとめて覚えていた。"),
    ("ケンは私にノートを見せてくれた。", "Ken showed his notebook for me.", "Ken showed his notebook to me.", "for me", "condition",
     "show は相手がいないと成り立たない動作なので to を使う（Ken showed me his notebook. も可）。", "「私のために見せてくれた」と考えて for を選んだ。"),
    ("父は私たちに夕食を作ってくれた。", "My father cooked dinner to us.", "My father cooked dinner for us.", "to us", "condition",
     "cook は相手がいなくても成り立つ動作なので for を使う（My father cooked us dinner. も可）。", "「私たちに」の「に」につられて to を選んだ。"),
    ("その規則を私に説明してください。", "Please explain me the rule.", "Please explain the rule to me.", "explain me the rule", "concept",
     "explain は第4文型（SVOO）をとらない動詞で、説明する相手は to で示す。", "teach me ～・tell me ～ と同じ形が使えると考えた。"),
    ("ユミは私に辞書を貸してくれた。", "Yumi lent her dictionary for me.", "Yumi lent her dictionary to me.", "for me", "condition",
     "lend は相手がいないと成り立たない動作なので to を使う（Yumi lent me her dictionary. も可）。", "「私のために貸してくれた」と考えて for を選んだ。"),
    ("彼は私に駅への道を教えてくれた。", "He taught me the way to the station.", "He told me the way to the station.", "taught", "concept",
     "teach は学問や技能を教える場合に使う。道や情報を教えるときは tell（または show）を使う（He showed me the way to the station. も可）。", "日本語の「教える」をすべて teach と訳した。"),
]


@gen("error_correction", 3, ["common_error", "condition_check"])
def err_svoo_prep(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(SVOO_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", etype, tempt, fix, fix, rule,
                    ["動詞がどの文型をとるか（SVOO をとれるか、to 型か for 型か）を確認する。", f"「{where}」の部分を直す。", f"正しい英文：{fix}"],
                    "第4文型をとる動詞かどうか、第3文型にするときの前置詞が to か for かを、動詞の意味（相手が必要な動作か）で判断する。",
                    ["正しい英文を第4文型（または第3文型）に書きかえて、両方の形が成り立つかを確かめる。"],
                    ["to と for を日本語の「に」「ために」だけで判断する。"], d=3)


GENERATORS = [identify_pattern, element_role, trans_intrans, confusing_verbs,
              same_pattern, svoo_to_svo, meaning, build_order,
              explain_difference, causative_form, passive_rewrite,
              err_transitive, err_lie_lay, err_svoo_prep]
