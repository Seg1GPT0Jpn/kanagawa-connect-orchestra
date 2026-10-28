"""単元パック：中学2年 英語 不定詞と動名詞。"""
from banks._common import desc, mc, order, sa
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem,
                         tp)

UNIT_ID = "JH-ENG-G2-U02"

PREREQUISITES = [
    ("JH-ENG-G1-U01", "一般動詞の現在形と三人称単数現在の s。不定詞の to の後ろは、主語が何でも動詞の原形になることを確かめるための土台。"),
    ("JH-ENG-G1-U04", "動詞の ing 形のつづり（make → making、swim → swimming）。動名詞も同じつづりのルールで作る。"),
    ("JH-ENG-G1-U05", "過去形（went, enjoyed, decided など）。不定詞・動名詞を目的語にとる動詞は、過去の文で使うことが多い。"),
    ("JH-ENG-G1-U03", "疑問詞 Why を使った疑問文。Why ～? ― To ～.（～するためです）の答え方で使う。"),
]
EXTENSIONS = [
    ("JH-ENG-G2-U03", "There are many places to visit. のように、There is / are 構文と形容詞的用法の不定詞を組み合わせて使う。"),
    ("JH-ENG-G3-U04", "It is ～ for … to ―.、want ＋人＋to ～、原形不定詞（help / let / make）など、不定詞を使った文構造に広がる。"),
    ("HS-ENG-U04", "高校では、不定詞の意味上の主語・完了不定詞、動名詞の意味上の主語、remember / forget / try などの to と ing による意味の違いを学ぶ。"),
]


def cap(s):
    return s[0].upper() + s[1:]


# ======================================================================
# 授業プリント
# ======================================================================

LESSON = lesson(
    goals=["〈to＋動詞の原形〉（不定詞）の3つの用法（名詞的・副詞的・形容詞的）を見分け、日本語の意味に合わせて使える。",
           "動詞の ing 形（動名詞）を「～すること」の意味で、主語・目的語・前置詞の後ろに使える。",
           "want / decide / hope は to ～、enjoy / finish / practice は ～ing、like / start / begin は両方、と目的語の形を動詞ごとに使い分けられる。"],
    duration=50,
    readiness=["一般動詞の原形・過去形・三人称単数現在の形を区別できる（中1）。",
               "動詞の ing 形を正しくつづれる（make → making、run → running）（中1 現在進行形）。",
               "小学校の外国語で I want to ～. や I like playing ～. などの表現を聞いたり話したりした経験がある。",
               "小学校の国語で、「～すること」「～するために」「～するための」のように、言葉の後ろにつく語で意味が変わることを学んでいる。"],
    flow=[("導入：「～すること」を英語で", 5, "I like tennis. → I like to play tennis. / I like playing tennis. と、動作を「名詞のかたまり」にする発想を示す"),
          ("不定詞の3用法", 15, "名詞的（～すること）・副詞的（～するために／～して）・形容詞的（～するための）を例文で比べる（例題1）"),
          ("動名詞", 8, "ing 形が「～すること」になる場合。主語・目的語・前置詞の後ろ（例題2）"),
          ("目的語は to か ing か", 14, "want 型・enjoy 型・like 型の3グループと、stop ～ing / stop to ～ の違い（例題3）"),
          ("まとめと確認", 8, "板書の3列で整理し、確認問題3問")],
    sections=[
        intro("in1", "動作を「かたまり」にして文にはめこむ",
              "英語の文には、ふつう動詞が1つしか入りません。では「私はテニスをすることが好きだ」のように、動詞 like の中にもう1つの動作「テニスをする」を入れたいときはどうすればよいでしょうか。この単元では、動詞を〈to＋動詞の原形〉（不定詞）や〈動詞の ing 形〉（動名詞）に変えて、名詞や修飾語のかたまりとして文にはめこむ方法を学びます。",
              bullets=["I like tennis.（テニスが好きだ：tennis は名詞）", "I like to play tennis.（テニスをすることが好きだ：to play tennis が名詞のかたまり）",
                       "I like playing tennis.（同じ意味：playing tennis が名詞のかたまり）", "× I like play tennis.（動詞が2つ並んでしまい、文にならない）"],
              points=[tp("4つ目の × の文を最初に見せ、なぜ文にならないのかを生徒に考えさせてから、to や ing を使う理由につなげる。",
                         ask="I like play tennis. はどこがおかしいか。", expect="like と play の2つの動詞が並んでいる。",
                         timing="導入の冒頭")]),
        definition("df1", "不定詞〈to＋動詞の原形〉の3つの用法",
                   "〈to＋動詞の原形〉を不定詞といいます。主語や時制に関係なく、to の後ろの動詞はいつも原形です。文の中での働きによって、次の3つの用法に分けられます。",
                   formula="to＋動詞の原形（主語・時制に関係なく原形）",
                   bullets=["名詞的用法「～すること」：I want to be a doctor.（医者になることを望む → 医者になりたい）／My dream is to travel abroad.",
                            "副詞的用法①目的「～するために」：I went to the park to play tennis.",
                            "副詞的用法②感情の原因「～して」：I was happy to see you.（あなたに会えてうれしかった）",
                            "形容詞的用法「～するための・～すべき」：I have a lot of homework to do.／I want something to drink."],
                   conditions=["to の後ろは原形：× to plays、× to played、× to playing。",
                               "形容詞的用法は、修飾する名詞の後ろに置く（homework to do）。something などに形容詞がつくときは something cold to drink の順。",
                               "副詞的用法②は glad / happy / sad / surprised など感情を表す語の後ろで使う。"],
                   points=[tp("用法の見分け方は「訳してみる」が基本。to ～ の部分を「～すること」「～するために」「～するための」に当てはめ、自然な日本語になるものを選ばせる。",
                              ask="I went to the park to play tennis. の to play を「～すること」と訳すとどうなるか。", expect="「テニスをすることの公園へ行った」となり不自然。「するために」が合う。"),
                           tp("to の後ろの動詞が過去形や三単現にならないことを、主語・時制を変えた例文で確認する。",
                              caution="He wants to plays ～. / I wanted to went ～. が多い誤り。", timing="定義の説明後")]),
        definition("df2", "動名詞〈動詞の ing 形〉「～すること」",
                   "動詞の ing 形は、進行形のほかに「～すること」という名詞の働きもします。これを動名詞といいます。名詞と同じように、文の主語・目的語・補語になり、前置詞の後ろにも置けます。",
                   formula="動詞の ing 形（＝～すること）",
                   bullets=["主語：Playing soccer is fun.（サッカーをすることは楽しい）※主語の動名詞は単数扱いで is",
                            "目的語：I enjoyed singing.（歌うことを楽しんだ）",
                            "補語：My hobby is taking pictures.（私の趣味は写真をとることだ）",
                            "前置詞の後ろ：I'm good at cooking.／Thank you for helping me.／How about going to the zoo?"],
                   conditions=["前置詞（at / in / for / about / before / after / without など）の後ろには、不定詞ではなく動名詞を置く。",
                               "be 動詞＋ing でも、「～している」（進行形）か「～すること」（動名詞）かは意味で判断する（My hobby is reading. は動名詞）。"],
                   points=[tp("「進行形の ing」と「動名詞の ing」は形が同じなので、be 動詞の後ろの ing を訳し分ける練習をさせる。",
                              ask="He is reading. と My hobby is reading. の ing の違いは？", expect="前は「読んでいる」（進行形）、後は「読むこと」（動名詞）。")]),
        theorem("th1", "目的語に to ～ をとる動詞・～ing をとる動詞",
                "want / hope / decide / need / plan＋to ～　｜　enjoy / finish / practice / stop＋～ing　｜　like / love / start / begin＋どちらも",
                ["want, hope, decide, need, plan, wish などは、目的語に不定詞（to ～）だけをとる（× want playing）。",
                 "enjoy, finish, practice, stop, give up などは、目的語に動名詞（～ing）だけをとる（× enjoy to play）。",
                 "like, love, start, begin などは、どちらをとってもほぼ同じ意味になる。",
                 "stop は注意：stop talking は「話すのをやめる」（目的語）、stop to talk は「話すために立ち止まる（手を止める）」（副詞的用法の目的）で意味が変わる。"],
                body="どの動詞がどちらをとるかは、最終的には動詞ごとに覚える必要があります。次の「導出」で、覚えるときの手がかりを確かめましょう。",
                points=[tp("3グループをカードに書いて分類させる活動が効果的。過去形（enjoyed, decided）でも同じルールであることを確認する。", timing="定理の説明時")]),
        derivation("dv1", "なぜ want は to、enjoy は ing なのか（覚えるための手がかり）",
                   ["① to はもともと「～へ（向かって）」という方向を表す前置詞。不定詞の to にも「これから～する」という、未来に向かう感じが残っている。",
                    "② want（～したい）・hope（～を望む）・decide（～することに決める）・plan（～する計画だ）は、どれも「まだしていない、これからすること」を目的語にとる → to ～ と相性がよい。",
                    "③ enjoy（楽しむ）・finish（終える）・practice（練習する）・stop（やめる）は、「実際にしている（していた）こと」が目的語になる → ～ing と相性がよい。",
                    "④ stop を例に確かめる：stop talking は「（していた）話すことをやめる」、stop to talk は「これから話すために立ち止まる」。②③の手がかりと一致する。",
                    "⑤ ただし like / start / begin のようにどちらもとれる動詞もあるので、この手がかりは「覚えるための目安」として使い、例文ごと覚える。"],
                   body="手がかりは「to＝これから（未来）」「ing＝実際の動作（現実）」。迷ったときに思い出す道具にしましょう。",
                   points=[tp("②③の動詞を生徒に分類させてから手がかりを示すと、「なるほど」という納得が生まれやすい。",
                              ask="decide は「これから」と「実際にしている」のどちらに近いか。", expect="これから（決めた時点ではまだしていない）。",
                              caution="手がかりは例外のない規則ではないので、「必ずそうなる」と言い切らない。", timing="導出の説明時")]),
        example("ex1", "例題1　不定詞の用法を見分ける",
                "次の英文の下線部（to ～）の用法を答え、文全体を日本語に訳しなさい。(1) My sister went to Canada to study English.　(2) I have no time to watch TV.　(3) Ken decided to join the soccer team.",
                ["(1) to study は「英語を勉強するために」とカナダへ行った目的を表す → 副詞的用法。",
                 "(2) to watch TV は名詞 time を後ろから説明して「テレビを見る（ための）時間」→ 形容詞的用法。",
                 "(3) to join は decided の目的語で「入部することを決めた」→ 名詞的用法。"],
                "(1) 副詞的用法：私の姉は英語を勉強するためにカナダへ行った。　(2) 形容詞的用法：私にはテレビを見る時間がない。　(3) 名詞的用法：ケンはサッカー部に入ることに決めた。",
                thinking="to ～ の前の語を見る。動詞の目的語なら名詞的、名詞の後ろで名詞を説明していれば形容詞的、文が完成したあとに目的や理由を足していれば副詞的。",
                points=[tp("「to ～ を取り除いても文が成り立つか」を確かめさせる。(1)(2) は取っても文が成り立つ（修飾語）、(3) は取ると decided の目的語がなくなる（名詞）。",
                           ask="(3) から to join ～ を取ると？", expect="Ken decided. で何を決めたかわからなくなる。")],
                misconceptions=[("(2) を「私はテレビを見るために時間がない」と訳す", "to watch TV は time を説明する形容詞的用法。「テレビを見る時間」。")]),
        example("ex2", "例題2　動名詞を使う",
                "日本語に合うように（　）内の語を適切な形にして英文を完成させなさい。(1) 私の兄は料理をするのが得意です。My brother is good at (cook).　(2) 雨がやみました。It stopped (rain).　(3) 毎朝走ることは健康によい。(Run) every morning is good for your health.",
                ["(1) at は前置詞。前置詞の後ろは動名詞 → cooking。",
                 "(2) stop の目的語は動名詞。「雨が降ることをやめた」→ raining。",
                 "(3) 文の主語「走ること」→ 動名詞 Running。n を重ねるつづりに注意。主語の動名詞は単数扱いなので is。"],
                "(1) cooking　(2) raining　(3) Running",
                thinking="前置詞の後ろ・enjoy / finish / stop の後ろ・文の主語の「～すること」は動名詞が基本。",
                points=[tp("(1) で to cook とする誤りを取り上げ、「前置詞の後ろに to ～ は置けない」ことを確認する。")],
                misconceptions=[("My brother is good at cook.", "前置詞 at の後ろは名詞か動名詞。cooking。"),
                                ("Runing every morning ～", "run は n を重ねて running。")]),
        example("ex3", "例題3　to ～ か ～ing か",
                "（　）内から正しいものを選びなさい。(1) We enjoyed (to swim / swimming) in the sea.　(2) I hope (to see / seeing) you again.　(3) He started (to cry / crying).",
                ["(1) enjoy は動名詞だけを目的語にとる → swimming。",
                 "(2) hope は不定詞だけを目的語にとる → to see。「また会うこと」はこれからのこと。",
                 "(3) start はどちらもとれる → to cry / crying のどちらも正しい。"],
                "(1) swimming　(2) to see　(3) どちらも正しい（He started to cry. / He started crying.）",
                thinking="動詞が want 型・enjoy 型・like 型のどれかを思い出す。迷ったら「これから」か「実際にしている」かを手がかりにする。",
                points=[tp("(3) のように「どちらも正しい」問題をまぜ、すべて1つに決まるわけではないことを意識させる。",
                           ask="(3) で to cry と crying の意味はちがうか。", expect="ほとんど同じ（泣き出した）。")]),
        board("bd1", "板書案",
              [("① 不定詞 to＋原形", ["名詞的：～すること", "I want to be a doctor.", "副詞的：～するために／～して", "I went there to play tennis.", "I was glad to see you.",
                                      "形容詞的：～するための", "homework to do / something to drink"]),
               ("② 動名詞 ～ing", ["～すること（名詞の働き）", "主語：Playing soccer is fun.", "目的語：I enjoyed singing.", "補語：My hobby is reading.",
                                  "前置詞の後ろ：good at cooking", "Thank you for helping me."]),
               ("③ 目的語は to？ ing？", ["to だけ：want / hope / decide / plan / need", "ing だけ：enjoy / finish / practice / stop", "両方：like / love / start / begin",
                                       "手がかり：to＝これから、ing＝実際の動作", "stop talking（話をやめる）", "stop to talk（話すために立ち止まる）"])],
              points=[tp("③の列は動詞カードを貼って生徒に分類させ、最後に手がかり（これから／実際の動作）を赤で書き加える。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("不定詞の用法名（名詞的など）を覚えることが目的ではない。「訳し分けて意味がとれる」「場面に合わせて使える」ことを重視する。", timing="授業全体"),
               tp("副詞的用法は Why ～? ― To ～. の対話で導入すると、目的を表す感覚がつかみやすい。", ask="Why did you go to the library?", expect="To borrow some books."),
               tp("形容詞的用法は「名詞の後ろから説明する」語順が日本語と逆になる。something cold to drink の語順は特に練習させる。",
                  caution="cold something to drink のように形容詞を前に出す誤りが多い。"),
               tp("動名詞の主語は単数扱い（Reading books is fun.）。books につられて are にする誤りに注意させる。"),
               tp("問題プリント D の誤答例は「to の後ろの形」「enjoy / want の目的語の取り違え」「前置詞の後ろの形」の3種類にまとめて振り返らせる。")],
              misconceptions=[("I enjoyed to play tennis.", "enjoy の目的語は動名詞。I enjoyed playing tennis."),
                              ("I want playing soccer.", "want の目的語は不定詞。I want to play soccer."),
                              ("She went to the shop to bought some milk.", "to の後ろは原形。to buy。"),
                              ("I'm interested in learn history.", "前置詞の後ろは動名詞。learning。")]),
        summary("sm1", "まとめ",
                ["不定詞＝to＋動詞の原形。名詞的（～すること）・副詞的（～するために／～して）・形容詞的（～するための）の3用法。",
                 "動名詞＝動詞の ing 形で「～すること」。主語・目的語・補語・前置詞の後ろに置ける。主語のときは単数扱い。",
                 "want / hope / decide は to ～、enjoy / finish / practice / stop は ～ing、like / start / begin は両方。stop to ～ は「～するために立ち止まる」。"]),
        check("ck1", "確認問題",
              [("I have a lot of homework to do. の to do の用法を答えなさい。", "形容詞的用法（homework を説明して「するべき宿題」）"),
               ("We finished (to clean / cleaning) the room. の正しいほうを選びなさい。", "cleaning（finish の目的語は動名詞）"),
               ("「手伝ってくれてありがとう」を英語で書きなさい（help を使う）。", "Thank you for helping me.")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

# (日本語, 空所つき英文, 原形, ing 形, 支配する動詞)
INF_OBJ = [
    ("私はこの夏、北海道を訪れたい。", "I want (　　) Hokkaido this summer.", "visit", "visiting", "want"),
    ("ケンは英語の先生になることに決めた。", "Ken decided (　　) an English teacher.", "become", "becoming", "decide"),
    ("私たちは来年、新しい家を建てる計画です。", "We are planning (　　) a new house next year.", "build", "building", "plan"),
    ("彼女はいつか宇宙へ行きたいと望んでいる。", "She hopes (　　) to space someday.", "go", "going", "hope"),
    ("あなたはもっと水を飲む必要があります。", "You need (　　) more water.", "drink", "drinking", "need"),
    ("私の姉はパリで美術を勉強したがっている。", "My sister wants (　　) art in Paris.", "study", "studying", "want"),
    ("私たちはその試合に勝ちたかった。", "We wanted (　　) the game.", "win", "winning", "want"),
    ("父は毎朝走ることに決めた。", "My father decided (　　) every morning.", "run", "running", "decide"),
    ("私は将来、海外で働きたい。", "I want (　　) abroad in the future.", "work", "working", "want"),
    ("あなたは昼食に何を食べたいですか。", "What do you want (　　) for lunch?", "eat", "eating", "want"),
    ("彼らは駅で会う約束をした。", "They promised (　　) at the station.", "meet", "meeting", "promise"),
    ("私はまたあなたに会えることを望んでいます。", "I hope (　　) you again.", "see", "seeing", "hope"),
    ("トムは日本の歴史について学びたがっている。", "Tom wants (　　) about Japanese history.", "learn", "learning", "want"),
    ("私たちは夏休みにキャンプへ行く計画を立てた。", "We planned (　　) camping during the summer vacation.", "go", "going", "plan"),
]


@gen("basic_check", 4, ["computation", "condition_check"])
def inf_object(r):
    jp, s, base, ing, gv = r.choice(INF_OBJ)
    ok = f"to {base}"
    why = {ing: (f"{gv} は目的語に不定詞（to ～）をとる動詞で、動名詞（～ing）はとらない。", "目的語に to をとる動詞と ing をとる動詞の区別"),
           base: (f"{gv} の後ろに動詞の原形をそのまま置くと、動詞が2つ並んで文にならない。to が必要。", "不定詞の形"),
           f"to {ing}": ("to の後ろの動詞は原形にする。to＋ing 形という形にはならない。", "不定詞の形（to＋原形）")}
    return mc(f"日本語に合うように、（　）に入る最も適切なものを選びなさい。\n{jp}\n{s}", [ok] + list(why),
              f"{gv} は「（これから）～すること」を目的語にとる動詞で、不定詞 to＋原形を使う。答えは {ok}。", d=1,
              ap=f"空所の直前の動詞 {gv} が、目的語に to ～ をとるか ～ing をとるかを思い出す。",
              steps=[f"空所の前の動詞は {gv}（want / hope / decide / plan / need の仲間）。", "この仲間は目的語に不定詞をとる。", f"to の後ろは原形なので {ok}。"],
              alt=[f"「{jp}」は「これから～すること」を表しているので、未来に向かう to ～ が合う、と手がかりから確かめる。"],
              pc=[("不定詞を選ぶべきだと判断している", 1), ("to＋原形の形を選んでいる", 1)],
              pit=["want / hope の後ろに ing 形を置く。", "to の後ろの動詞を ing 形や三単現にする。"], why=why)


# (日本語, 空所つき英文, 原形, ing 形, 動詞, stop か)
GER_OBJ = [
    ("私たちはパーティーで歌うことを楽しんだ。", "We enjoyed (　　) at the party.", "sing", "singing", "enjoy"),
    ("ケンは昨夜、宿題をし終えましたか。", "Did Ken finish (　　) his homework last night?", "do", "doing", "finish"),
    ("突然、赤ちゃんが泣きやんだ。", "Suddenly the baby stopped (　　).", "cry", "crying", "stop"),
    ("私の妹は毎日ピアノをひく練習をしている。", "My sister practices (　　) the piano every day.", "play", "playing", "practice"),
    ("午後には雨がやんだ。", "It stopped (　　) in the afternoon.", "rain", "raining", "stop"),
    ("私は昨夜、その本を読み終えた。", "I finished (　　) the book last night.", "read", "reading", "finish"),
    ("彼らは海で泳ぐのを楽しんだ。", "They enjoyed (　　) in the sea.", "swim", "swimming", "enjoy"),
    ("祖母は毎朝、散歩を楽しんでいる。", "My grandmother enjoys (　　) every morning.", "walk", "walking", "enjoy"),
    ("私たちは教室をそうじし終えた。", "We finished (　　) the classroom.", "clean", "cleaning", "finish"),
    ("弟は10時にテレビゲームをするのをやめた。", "My brother stopped (　　) video games at ten.", "play", "playing", "stop"),
    ("ユミは毎日、英語の歌を歌う練習をしている。", "Yumi practices (　　) English songs every day.", "sing", "singing", "practice"),
    ("あなたは料理をすることを楽しみますか。", "Do you enjoy (　　)?", "cook", "cooking", "enjoy"),
    ("私は手紙を書き終えて、それを母に見せた。", "I finished (　　) the letter and showed it to my mother.", "write", "writing", "finish"),
]


@gen("basic_check", 4, ["computation", "common_error"])
def gerund_object(r):
    jp, s, base, ing, gv = r.choice(GER_OBJ)
    if gv == "stop":
        to_reason = ("stop to ～ は「～するために立ち止まる（手を止める）」という副詞的用法の意味になり、日本語の「～するのをやめる」に合わない。", "stop ～ing と stop to ～ の意味の違い")
    else:
        to_reason = (f"{gv} は目的語に動名詞（～ing）をとる動詞で、不定詞（to ～）はとらない。", "目的語に to をとる動詞と ing をとる動詞の区別")
    why = {f"to {base}": to_reason,
           base: (f"{gv} の後ろに動詞の原形をそのまま置くと、動詞が2つ並んで文にならない。", "動名詞の形"),
           f"to {ing}": ("to＋ing 形という形はない。ここでは ing 形だけを置く。", "不定詞と動名詞の混同")}
    return mc(f"日本語に合うように、（　）に入る最も適切なものを選びなさい。\n{jp}\n{s}", [ing] + list(why),
              f"{gv} は目的語に動名詞（～ing）をとる動詞。答えは {ing}。", d=1,
              ap=f"空所の前の動詞 {gv} が enjoy / finish / practice / stop の仲間かどうかを確かめる。",
              steps=[f"空所の前の動詞は {gv}。", "enjoy / finish / practice / stop は目的語に動名詞をとる。", f"{base} を ing 形にする：{ing}。"],
              alt=["「実際にしている（していた）動作」を楽しむ・終える・やめる、という意味なので ing が合う、と手がかりから確かめる。"],
              pc=[("動名詞を選ぶべきだと判断している", 1), ("ing 形を正しく選んでいる", 1)],
              pit=["enjoy や finish の後ろに to ～ を置く。", "stop to ～ と stop ～ing の意味の違いを考えずに選ぶ。"], why=why)


USE_N = "名詞的用法（～すること）"
USE_ADV = "副詞的用法（～するために／～して）"
USE_ADJ = "形容詞的用法（～するための／～すべき）"
USE_GER = "動名詞（～すること）"
# (英文, 下線部, 用法, 和訳)
USES = [
    ("I want to be a nurse in the future.", "to be", USE_N, "私は将来、看護師になりたい。"),
    ("My dream is to travel around the world.", "to travel", USE_N, "私の夢は世界中を旅行することだ。"),
    ("Ken decided to buy a new bike.", "to buy", USE_N, "ケンは新しい自転車を買うことに決めた。"),
    ("She likes to draw pictures.", "to draw", USE_N, "彼女は絵をかくことが好きだ。"),
    ("We began to clean the park.", "to clean", USE_N, "私たちは公園をそうじし始めた。"),
    ("I went to the library to borrow some books.", "to borrow", USE_ADV, "私は本を借りるために図書館へ行った。"),
    ("Tom got up early to catch the first train.", "to catch", USE_ADV, "トムは始発電車に乗るために早起きした。"),
    ("We were glad to hear the news.", "to hear", USE_ADV, "私たちはその知らせを聞いてうれしかった。"),
    ("My mother went to the store to buy some eggs.", "to buy", USE_ADV, "母は卵を買うために店へ行った。"),
    ("I was surprised to see him there.", "to see", USE_ADV, "私はそこで彼に会って驚いた。"),
    ("Aya studies hard to become a doctor.", "to become", USE_ADV, "アヤは医者になるために一生けんめい勉強している。"),
    ("I have a lot of homework to do today.", "to do", USE_ADJ, "私には今日するべき宿題がたくさんある。"),
    ("Do you want something to drink?", "to drink", USE_ADJ, "何か飲むものがほしいですか。"),
    ("There are many places to visit in Kyoto.", "to visit", USE_ADJ, "京都には訪れるべき場所がたくさんある。"),
    ("He had no time to eat breakfast.", "to eat", USE_ADJ, "彼には朝食を食べる時間がなかった。"),
    ("Please give me something to write with.", "to write", USE_ADJ, "何か書くもの（筆記用具）をください。"),
    ("It's time to go to bed.", "to go", USE_ADJ, "寝る時間ですよ。"),
]


@gen("basic_check", 4, ["concept", "condition_check"])
def which_use(r):
    en, part, use, jp = r.choice(USES)
    wrongs = [u for u in (USE_N, USE_ADV, USE_ADJ) if u != use] + [USE_GER]
    reasons = {
        USE_N: "to ～ が動詞の目的語や補語になっているときが名詞的用法。この文の to ～ は名詞の働きをしていない。",
        USE_ADV: "to ～ が「～するために」と目的を表したり、感情の原因を表したりするときが副詞的用法。この文はそれに当たらない。",
        USE_ADJ: "to ～ が直前の名詞を後ろから説明しているときが形容詞的用法。この文の to ～ は名詞を説明していない。",
        USE_GER: "動名詞は動詞の ing 形。下線部は〈to＋動詞の原形〉なので不定詞である。",
    }
    why = {w: (reasons[w], "不定詞の用法の見分け方") for w in wrongs}
    hint = {USE_N: "動詞の目的語（または be 動詞の後ろの補語）になっていて「～すること」と訳せる",
            USE_ADV: "文の要素がそろったあとに「～するために」「～して」という意味を加えている",
            USE_ADJ: "直前の名詞を後ろから説明して「～するための」「～すべき」と訳せる"}[use]
    return mc(f"次の英文の［　］の部分の働きとして最も適切なものを選びなさい。\n{en.replace(part, '［' + part + '］', 1)}", [use] + wrongs,
              f"「{jp}」と訳せる。［{part}］は{hint}ので、{use}。", d=2,
              ap="［　］の部分を「～すること」「～するために／～して」「～するための」に当てはめて訳し、自然な日本語になるものを選ぶ。",
              steps=[f"［{part}］の前にある語を確かめる。", f"{hint}。", f"答え：{use}"],
              alt=[f"全文を訳して確かめる：{jp}"],
              pc=[("［　］の部分の働きを正しく捉えている", 1), ("用法を正しく選んでいる", 1)],
              pit=["名詞の後ろにある形容詞的用法を「～するために」と訳してしまう。", "to ～ と ～ing を区別せず、どちらも「動名詞」と考える。"], why=why)


# (日本語, 空所つき英文, 原形, ing, 前置詞, 過去形)
PREP = [
    ("私の兄は料理をするのが得意です。", "My brother is good at (　　).", "cook", "cooking", "at"),
    ("私は日本の歴史を学ぶことに興味がある。", "I'm interested in (　　) Japanese history.", "learn", "learning", "in"),
    ("宿題を手伝ってくれてありがとう。", "Thank you for (　　) me with my homework.", "help", "helping", "for"),
    ("明日、映画を見に行くのはどうですか。", "How about (　　) to the movies tomorrow?", "go", "going", "about"),
    ("寝る前に歯をみがきなさい。", "Brush your teeth before (　　) to bed.", "go", "going", "before"),
    ("夕食を食べたあとで、私は宿題をした。", "I did my homework after (　　) dinner.", "eat", "eating", "after"),
    ("彼女はさよならを言わずに部屋を出た。", "She left the room without (　　) goodbye.", "say", "saying", "without"),
    ("私をパーティーに招待してくれてありがとう。", "Thank you for (　　) me to the party.", "invite", "inviting", "for"),
    ("私は絵をかくのが得意ではない。", "I'm not good at (　　) pictures.", "draw", "drawing", "at"),
    ("ケンはギターをひくことに興味がある。", "Ken is interested in (　　) the guitar.", "play", "playing", "in"),
    ("いっしょに昼食を食べるのはどう？", "How about (　　) lunch together?", "have", "having", "about"),
    ("私の姉は泳ぐのが得意です。", "My sister is good at (　　).", "swim", "swimming", "at"),
    ("家を出る前に窓を閉めなさい。", "Close the windows before (　　) home.", "leave", "leaving", "before"),
]


@gen("basic_check", 4, ["condition_check", "concept"])
def prep_gerund(r):
    jp, s, base, ing, prep = r.choice(PREP)
    why = {base: (f"{prep} は前置詞。前置詞の後ろに動詞の原形はそのまま置けない。", "前置詞の後ろの形"),
           f"to {base}": (f"前置詞 {prep} の後ろには不定詞（to ～）を置けない。名詞の働きをする動名詞を使う。", "前置詞の後ろの形"),
           f"to {ing}": ("to＋ing 形という形はない。前置詞の後ろには ing 形だけを置く。", "不定詞と動名詞の混同")}
    return mc(f"日本語に合うように、（　）に入る最も適切なものを選びなさい。\n{jp}\n{s}", [ing] + list(why),
              f"{prep} は前置詞で、前置詞の後ろには名詞か動名詞を置く。答えは {ing}。", d=1,
              ap="空所の直前が前置詞（at / in / for / about / before / after / without）かどうかを確かめる。",
              steps=[f"空所の直前の {prep} は前置詞。", "前置詞の後ろに動作を置くときは動名詞（～ing）にする。", f"答え：{ing}"],
              alt=[f"動名詞の代わりに名詞を入れてみる（例：good at tennis）と、前置詞の後ろが名詞の位置だとわかる。"],
              pc=[("前置詞の後ろだと気づいている", 1), ("動名詞を選んでいる", 1)],
              pit=["前置詞の後ろに動詞の原形を置く（good at cook）。", "Thank you for to help ～ のように to を入れる。"], why=why)


TO_VERBS = ["wanted", "decided", "hoped", "planned"]
ING_VERBS = ["enjoyed", "finished", "practiced"]
# (主語, 原形, ing, 残り)
ACTS2 = [
    ("We", "clean", "cleaning", "the classroom"), ("Ken", "play", "playing", "the guitar"), ("My sister", "write", "writing", "a story"),
    ("They", "sing", "singing", "the song"), ("I", "read", "reading", "the comic book"), ("Yumi", "make", "making", "a cake"),
    ("The children", "draw", "drawing", "pictures"), ("My father", "wash", "washing", "the car"),
]


@gen("basic_check", 4, ["concept", "condition_check"])
def which_verb(r):
    s, base, ing, rest = r.choice(ACTS2)
    if r.random() < 0.5:
        ok = r.choice(TO_VERBS)
        wrongs = r.sample(ING_VERBS, 3)
        sent = f"{s} (　　) to {base} {rest}."
        expl = f"空所の後ろは不定詞 to {base}。不定詞を目的語にとる動詞は {ok}。enjoy / finish / practice は動名詞しかとらない。"
        kind = "不定詞"
    else:
        ok = r.choice(["enjoyed", "finished", "stopped"])
        wrongs = r.sample(TO_VERBS, 3)
        sent = f"{s} (　　) {ing} {rest}."
        expl = f"空所の後ろは動名詞 {ing}。動名詞を目的語にとる動詞は {ok}。want / decide / hope / plan は不定詞しかとらない。"
        kind = "動名詞"
    base_of = {"wanted": "want", "decided": "decide", "hoped": "hope", "planned": "plan",
               "enjoyed": "enjoy", "finished": "finish", "practiced": "practice", "stopped": "stop"}
    why = {w: (f"{base_of[w]} は目的語に{'動名詞（～ing）' if kind == '不定詞' else '不定詞（to ～）'}だけをとるので、空所の後ろの{kind}は続かない。",
               "目的語に to をとる動詞と ing をとる動詞の区別") for w in wrongs}
    return mc(f"次の英文の（　）に入る語として、文法的に正しいものを1つ選びなさい。\n{sent}", [ok] + wrongs,
              expl, d=2,
              ap=f"空所の後ろが不定詞（to ～）か動名詞（～ing）かを先に見て、それを目的語にとれる動詞を探す。",
              steps=[f"空所の後ろは{kind}。", f"選択肢の動詞を「to をとる仲間」と「ing をとる仲間」に分ける。", f"{kind}をとれるのは {ok}。"],
              alt=["選んだ動詞の文を日本語に訳して、意味も自然かどうかを確かめる。"],
              pc=[("空所の後ろの形を確認している", 1), ("正しい動詞を選んでいる", 1)],
              pit=["意味だけで選び、動詞が to と ing のどちらをとるかを確かめない。", "過去形になっていると、もとの動詞が何かわからなくなる。"], why=why)


# ======================================================================
# B 標準演習
# ======================================================================

# (日本語, 使う語, 答え, 別解)
JP_EN = [
    ("私は本を借りるために図書館へ行きました。", "library / borrow", "I went to the library to borrow some books.", ["I went to the library to borrow books."]),
    ("ケンは写真をとるために早起きしました。", "get / take", "Ken got up early to take pictures.", ["Ken got up early to take some pictures."]),
    ("私はその知らせを聞いてうれしかった。", "glad / hear", "I was glad to hear the news.", ["I was glad to hear that news."]),
    ("私には今日するべき宿題がたくさんあります。", "homework / do", "I have a lot of homework to do today.", ["I have much homework to do today."]),
    ("何か冷たい飲み物がほしいです。", "something / drink", "I want something cold to drink.", ["I'd like something cold to drink."]),
    ("私の夢は世界中を旅行することです。", "dream / travel", "My dream is to travel around the world.", ["My dream is traveling around the world."]),
    ("英語を話すことは楽しい。", "speak / fun", "Speaking English is fun.", ["To speak English is fun."]),
    ("私たちはその試合に負けて悲しかった。", "sad / lose", "We were sad to lose the game.", []),
    ("私の趣味は切手を集めることです。", "hobby / collect", "My hobby is collecting stamps.", ["My hobby is to collect stamps."]),
    ("姉は英語を勉強するためにカナダへ行きました。", "Canada / study", "My sister went to Canada to study English.", []),
    ("彼には朝食を食べる時間がありませんでした。", "time / eat", "He had no time to eat breakfast.", ["He didn't have time to eat breakfast."]),
    ("私たちは雨の中を走るのをやめた。", "stop / run", "We stopped running in the rain.", []),
    ("父は来年、車を買うことに決めました。", "decide / buy", "My father decided to buy a car next year.", []),
    ("私は友だちとおしゃべりをして楽しみました。", "enjoy / talk", "I enjoyed talking with my friends.", ["I enjoyed talking with my friend."]),
]


@gen("standard_practice", 4, ["computation", "application"])
def jp_to_en(r):
    jp, words, ans, vs = r.choice(JP_EN)
    return sa(f"日本語に合うように、（　）内の語を参考にして英文を書きなさい。語は必要に応じて形を変えてよい。\n{jp}（{words}）", ans,
              f"不定詞（to＋原形）か動名詞（～ing）かを、日本語の意味と前の語から判断する。答え：{ans}", d=2, p=4, v=vs or None,
              ap="日本語の「～すること」「～するために」「～して」「～するための」のどれに当たるかを見て、不定詞・動名詞のどちらを使うかを決める。",
              steps=["日本語から文の骨組み（主語＋動詞）を決める。", "もう1つの動作を、不定詞か動名詞のかたまりにする。", "かたまりを置く位置（目的語・名詞の後ろ・文の後ろ）を決める。", f"答え：{ans}"],
              alt=["書いた英文の to ～ や ～ing の部分を日本語に訳して、問題の日本語と一致するかを確かめる。"],
              pc=[("文の骨組み（主語・動詞・時制）が正しい", 2), ("不定詞・動名詞の形と位置が正しい", 2)],
              pit=["to の後ろの動詞を過去形にする（to borrowed）。", "形容詞的用法で名詞の前に to ～ を置く。"])


# (英文1, 英文2（空所つき）, 答え, ポイント)
REWRITE = [
    ("I like to cook.", "I like (　　).", "cooking", "like は不定詞も動名詞もとれる。to cook → cooking。"),
    ("Ken can swim well.", "Ken is good at (　　).", "swimming", "「上手に泳げる」＝「泳ぐことが得意」。前置詞 at の後ろは動名詞。"),
    ("Let's go fishing this weekend.", "How about (　　) fishing this weekend?", "going", "How about ～ing? は「～するのはどうですか」という誘い。about は前置詞なので動名詞。"),
    ("She started to sing.", "She started (　　).", "singing", "start は不定詞も動名詞もとれる。"),
    ("I began to learn Chinese last year.", "I began (　　) Chinese last year.", "learning", "begin は不定詞も動名詞もとれる。"),
    ("My hobby is to take pictures.", "My hobby is (　　) pictures.", "taking", "補語の「～すること」は不定詞でも動名詞でも表せる。"),
    ("Mika plays tennis very well.", "Mika is good at (　　) tennis.", "playing", "「上手にする」＝「することが得意」。at の後ろは動名詞。"),
    ("Thank you. You helped me.", "Thank you for (　　) me.", "helping", "Thank you for ～ing. で「～してくれてありがとう」。for は前置詞なので動名詞。"),
    ("I love to read comics.", "I love (　　) comics.", "reading", "love は不定詞も動名詞もとれる。"),
    ("Can you dance well?", "Are you good at (　　)?", "dancing", "「上手に踊れるか」＝「踊ることが得意か」。at の後ろは動名詞。"),
    ("Reading books is interesting.", "(　　) read books is interesting.", "To", "主語の「～すること」は動名詞でも不定詞でも表せる。Reading → To read。"),
    ("He likes playing baseball.", "He likes (　　) play baseball.", "to", "like は不定詞もとれる。playing → to play。"),
]


@gen("standard_practice", 4, ["condition_check", "computation"])
def rewrite(r):
    a, b, ans, point = r.choice(REWRITE)
    return sa(f"2つの英文がほぼ同じ意味になるように、（　）に適切な1語を入れなさい。\n{a}\n{b}", ans,
              f"{point}答え：{ans}", d=2, p=4,
              ap="2つの文で形が変わった部分を見つけ、空所が不定詞（to ～）と動名詞（～ing）のどちらの形になるかを、直前の語から決める。",
              steps=["1文目と2文目で同じ意味を表している部分を対応させる。", "空所の直前の語（動詞・前置詞）が何をとるかを確かめる。", f"答え：{ans}"],
              alt=["完成した2文目を日本語に訳し、1文目の意味と一致するかを確かめる。"],
              pc=[("空所に入る形（to か ing か）を正しく判断している", 2), ("つづりを含めて正しく書いている", 2)],
              pit=["前置詞の後ろに原形を置く。", "ing のつづり（swiming, danceing）を誤る。"])


ORDERS = [
    ("私は将来、科学者になりたい。", ["I", "want", "to", "be", "a scientist", "in the future"], "want to＋原形（名詞的用法）"),
    ("ケンは英語を勉強するためにアメリカへ行った。", ["Ken", "went", "to America", "to", "study", "English"], "to＋原形を文の後ろに置いて目的を表す（副詞的用法）"),
    ("私には今日するべきことがたくさんある。", ["I", "have", "a lot of", "things", "to", "do", "today"], "名詞 things の後ろに to do（形容詞的用法）"),
    ("何か温かい食べ物がほしいですか。", ["do", "you", "want", "something", "hot", "to", "eat"], "something＋形容詞＋to＋原形"),
    ("私の姉は写真をとることが得意です。", ["my sister", "is", "good", "at", "taking", "pictures"], "前置詞 at の後ろは動名詞"),
    ("私たちはいっしょに歌うことを楽しんだ。", ["we", "enjoyed", "singing", "together"], "enjoy＋動名詞"),
    ("あなたにまた会えてうれしいです。", ["I'm", "happy", "to", "see", "you", "again"], "感情＋to＋原形（副詞的用法：原因）"),
    ("私の夢は自分の店を持つことです。", ["my", "dream", "is", "to", "have", "my own shop"], "be 動詞の後ろの to＋原形（名詞的用法）"),
    ("早寝早起きは健康によい。", ["going", "to bed", "early", "is", "good", "for", "your health"], "動名詞のかたまりが主語（単数扱い is）"),
    ("彼はさよならを言わずに出ていった。", ["he", "went", "out", "without", "saying", "goodbye"], "前置詞 without の後ろは動名詞"),
    ("京都には見るべき場所がたくさんある。", ["there", "are", "many", "places", "to", "see", "in Kyoto"], "名詞 places の後ろに to see（形容詞的用法）"),
    ("手紙を書き終えましたか。", ["did", "you", "finish", "writing", "the letter"], "finish＋動名詞"),
]


@gen("standard_practice", 4, ["application", "computation"])
def build_order(r):
    jp, parts, pat = r.choice(ORDERS)
    sent = cap(" ".join(parts)) + ("?" if jp.endswith("か。") else ".")
    return order(f"日本語に合うように、次の語句を並べかえて英文を完成させなさい。ただし、文頭にくる語も小文字で示してある。\n{jp}", parts,
                 f"{sent}　ポイント：{pat}。", d=2, p=4,
                 ap="まず文の骨組み（主語＋動詞）を作り、残った to ～ や ～ing のかたまりをどこに置くかを考える。",
                 steps=["主語と動詞を決める。", f"不定詞・動名詞のかたまりを作る：{pat}。", "かたまりを目的語・名詞の後ろ・文の後ろのいずれかに置く。", f"完成文：{sent}"],
                 alt=["完成した英文を日本語に訳し直して、問題の日本語と一致するかを確かめる。"],
                 pc=[("文の骨組み（主語・動詞）の語順が正しい", 2), ("不定詞・動名詞のかたまりの位置が正しい", 2)],
                 pit=["形容詞的用法の to ～ を名詞の前に置く。", "something hot の語順を hot something にする。"])


# (日本語, 正しい英文, [(誤った英文, 理由)])
ADJ_USE = [
    ("私は何か冷たい飲み物がほしい。", "I want something cold to drink.",
     [("I want cold something to drink.", "something を説明する形容詞は something の後ろに置く。"),
      ("I want something cold drink.", "drink の前に to がないと、名詞を説明する形容詞的用法にならない。"),
      ("I want something cold drinking.", "名詞を後ろから説明して「飲むための」を表すのは to＋原形。")]),
    ("私には今日するべき仕事がたくさんある。", "I have a lot of work to do today.",
     [("I have a lot of work do today.", "do の前に to がないと、work を説明できない。"),
      ("I have a lot of work doing today.", "「するべき仕事」は to＋原形で表す。"),
      ("I have a lot of work to doing today.", "to の後ろは動詞の原形。to＋ing 形にはならない。")]),
    ("彼には昼食を食べる時間がなかった。", "He had no time to eat lunch.",
     [("He had no time eat lunch.", "eat の前に to がないと、time を説明できない。"),
      ("He had no time to ate lunch.", "to の後ろは動詞の原形。ate は過去形。"),
      ("He had no to eat lunch time.", "to ～ は説明する名詞 time の後ろに置く。")]),
    ("何か読むものを持っていますか。", "Do you have anything to read?",
     [("Do you have anything read?", "read の前に to がないと、anything を説明できない。"),
      ("Do you have to read anything?", "「何かを読まなければなりませんか」という意味になり、日本語に合わない。"),
      ("Do you have anything to reading?", "to の後ろは動詞の原形。")]),
    ("私は何かおもしろい読み物がほしい。", "I want something interesting to read.",
     [("I want interesting something to read.", "something を説明する形容詞は something の後ろに置く。"),
      ("I want something to read interesting.", "形容詞は something の直後、その後ろに to＋原形を置く。"),
      ("I want something interesting reading.", "「読むための」は to＋原形で表す。")]),
    ("彼女にはやるべき宿題がたくさんある。", "She has a lot of homework to do.",
     [("She has a lot of homework do.", "do の前に to がないと、homework を説明できない。"),
      ("She has a lot of homework to does.", "to の後ろは主語に関係なく原形。does は使わない。"),
      ("She has a lot of to do homework.", "to ～ は説明する名詞 homework の後ろに置く。")]),
    ("今日は何も食べるものがない。", "I have nothing to eat today.",
     [("I have nothing eat today.", "eat の前に to がないと、nothing を説明できない。"),
      ("I have nothing to eating today.", "to の後ろは動詞の原形。"),
      ("I have nothing for eat today.", "「～するための」は to＋原形で表す。for＋動詞の原形という形はない。")]),
]


@gen("standard_practice", 4, ["concept", "application"])
def adj_use(r):
    jp, ok, wrongs = r.choice(ADJ_USE)
    return mc(f"日本語に合う英文として最も適切なものを選びなさい。\n{jp}", [ok] + [w for w, _ in wrongs],
              f"「～するための（名詞）」は、名詞の後ろに to＋原形を置く形容詞的用法で表す。答え：{ok}", d=3,
              ap="説明される名詞（something / time / homework など）を見つけ、その後ろに to＋原形が続いているかを確かめる。",
              steps=["日本語の「～する（ための）＋名詞」の部分を見つける。", "英語では名詞を先に言い、後ろに to＋原形を置く。", f"答え：{ok}"],
              alt=["選んだ英文の to ～ の部分を「～するための」と訳して、日本語と一致するかを確かめる。"],
              pc=[("名詞の後ろに to＋原形を置く形を理解している", 2), ("正しい英文を選んでいる", 2)],
              pit=["形容詞を something の前に置く。", "have to（～しなければならない）と、have＋名詞＋to ～ を混同する。"],
              why={w: (reason, "形容詞的用法の語順") for w, reason in wrongs})


# (疑問文, 原形, ing, 残り)
WHY_Q = [
    ("Why did you go to the park?", "play", "playing", "tennis with my friends"),
    ("Why did you get up early this morning?", "catch", "catching", "the first bus"),
    ("Why did Ken go to the library?", "study", "studying", "for the test"),
    ("Why are you saving money?", "buy", "buying", "a new bike"),
    ("Why did your sister go to Australia?", "learn", "learning", "English"),
    ("Why did you call Yumi last night?", "ask", "asking", "about the homework"),
    ("Why did they go to the station?", "meet", "meeting", "their grandmother"),
    ("Why are you studying so hard?", "become", "becoming", "a doctor"),
    ("Why did you go to the supermarket?", "buy", "buying", "some vegetables"),
]


@gen("standard_practice", 4, ["cross_unit", "concept"], rel=["JH-ENG-G1-U03"])
def why_to(r):
    q, base, ing, rest = r.choice(WHY_Q)
    ok = f"To {base} {rest}."
    why = {f"To {ing} {rest}.": ("to の後ろは動詞の原形。to＋ing 形にはならない。", "不定詞の形"),
           f"Because to {base} {rest}.": ("because の後ろには〈主語＋動詞〉が続く。because と to ～ を組み合わせることはできない。", "理由の答え方（because）と目的の答え方（to）の混同"),
           f"{cap(base)} {rest}.": ("動詞の原形で始めると「～しなさい」という命令文になり、理由・目的の答えにならない。", "命令文との混同")}
    return mc(f"次の対話が成り立つように、B の（　）に入る最も適切なものを選びなさい。\nA：{q}\nB：(　　)", [ok] + list(why),
              f"Why ～?（なぜ～）に「～するためです」と目的を答えるときは、To＋動詞の原形 ～. で答えられる（副詞的用法）。答え：{ok}", d=2,
              ap="Why の疑問文には、Because ＋主語＋動詞 ～. か、To＋動詞の原形 ～. で答える。選択肢がどちらの形として正しいかを確かめる。",
              steps=["A は Why で理由・目的をたずねている。", "目的を答える形は To＋原形 ～.（～するためです）。", f"答え：{ok}"],
              alt=[f"Because を使って答える文（Because I wanted to {base} {rest}. など）に言いかえて、意味が合うかを確かめる。"],
              pc=[("Why の疑問文への答え方を理解している", 2), ("To＋原形の形を選んでいる", 2)],
              pit=["Because to ～. のように because と不定詞を組み合わせる。", "To＋ing 形にする。"], why=why)


# ======================================================================
# C 思考力・記述応用
# ======================================================================

PAIRS = [
    ("He stopped talking.", "He stopped to talk.",
     "A は stop＋動名詞で「彼は話すのをやめた」（していたことをやめる）。B の to talk は目的を表す副詞的用法で「彼は話すために立ち止まった（手を止めた）」という意味になる。stop の後ろが動名詞か不定詞かで意味が変わる。"),
    ("I have a book to read.", "I have to read a book.",
     "A の to read は名詞 a book を後ろから説明する形容詞的用法で「私には読む（ための）本がある」。B は have to＋原形で「私は本を読まなければならない」という義務を表す。have の後ろに名詞があるかどうかで文の形が違う。"),
    ("I went to the park to play tennis.", "I like to play tennis.",
     "A の to play は went to the park という動作の目的を表す副詞的用法で「テニスをするために公園へ行った」。B の to play は like の目的語になる名詞的用法で「テニスをすることが好きだ」。"),
    ("I need something to eat.", "I need to eat something.",
     "A の to eat は something を説明する形容詞的用法で「何か食べるものが必要だ」と、必要なのが「もの」であることを表す。B の to eat は need の目的語になる名詞的用法で「何かを食べる必要がある」と、必要なのが「食べること」であることを表す。"),
    ("My brother is reading.", "My hobby is reading.",
     "A の reading は be 動詞と組み合わさった現在進行形で「兄は（今）読書をしている」。B の reading は「読書（読むこと）」という動名詞で、主語 my hobby と同じものを表す補語になっている。同じ is＋ing でも働きが違う。"),
    ("I was happy to see her.", "I wanted to see her.",
     "A の to see は感情を表す happy の原因を表す副詞的用法で「彼女に会えてうれしかった」（実際に会った）。B の to see は wanted の目的語になる名詞的用法で「彼女に会いたかった」（会ったかどうかはわからない）。"),
    ("Ken went to the store to buy milk.", "Ken has no money to buy milk.",
     "A の to buy は店へ行った目的を表す副詞的用法で「ケンは牛乳を買うために店へ行った」。B の to buy は名詞 money を説明する形容詞的用法で「ケンには牛乳を買うお金がない」。"),
]


@gen("thinking_writing", 3, ["written_reasoning", "concept"])
def explain_difference(r):
    a, b, model = r.choice(PAIRS)
    return desc(f"次の2つの英文 A・B の意味の違いを、不定詞・動名詞の働き（用法）に注目して日本語で説明しなさい。\nA：{a}\nB：{b}", model,
                "to ～ や ～ing の前に何があるか（動詞・名詞・be 動詞）を見ると、そのかたまりの働きと意味が決まる。",
                [("A の形と意味を正しく説明している", 3), ("B の形と意味を正しく説明している", 3), ("違いを生む働き（用法）を指摘している", 2)], d=3, p=8, lines=5,
                ap="2つの文で違う部分に印をつけ、to ～ や ～ing が「動詞の目的語」「名詞の説明」「目的・原因」「進行形」のどれになっているかを考える。",
                steps=["A と B を見比べ、違う部分を見つける。", "それぞれの to ～ / ～ing の働きを判断する。", "和訳を示して意味の違いを説明する。"],
                alt=["それぞれの文が使われる場面（だれが、どんな状況で言うか）を考えて、場面の違いから説明する方法もある。"],
                pc=[("A の説明", 3), ("B の説明", 3), ("用法の違いの指摘", 2)],
                pit=["和訳だけを書き、どの形が違いを生んでいるかを書かない。", "形容詞的用法と副詞的用法を区別せずに「～するために」と訳す。"])


FORM3 = [
    ("play", "playing", "tennis", "the park"), ("swim", "swimming", "in the sea", "the beach"), ("take", "taking", "pictures", "the zoo"),
    ("read", "reading", "books", "the library"), ("sing", "singing", "songs", "the music room"), ("draw", "drawing", "pictures", "the art museum"),
    ("run", "running", "with my dog", "the river"), ("study", "studying", "math", "the library"),
]


@gen("thinking_writing", 3, ["condition_check", "written_reasoning"])
def three_forms(r):
    base, ing, obj, place = r.choice(FORM3)
    model = (f"(1) to {base}　(2) {ing}　(3) to {base}。理由：(1) want は目的語に不定詞だけをとる（これからしたいこと）。"
             f"(2) enjoy は目的語に動名詞だけをとる（実際にしたことを楽しむ）。(3) went to {place} という動作のあとに「～するために」と目的を加える副詞的用法なので to＋原形。")
    return desc(f"（　）内の動詞 {base} を、それぞれ適切な形（to＋原形 または ～ing）に直しなさい。また、そう判断した理由を説明しなさい。\n(1) I want (　　) {obj} tomorrow.\n(2) I enjoyed (　　) {obj} yesterday.\n(3) I went to {place} (　　) {obj}.",
                model, "空所の前にある語（want / enjoy / 文の終わった動作）によって、to ～ と ～ing のどちらを使うかが決まる。",
                [("(1)～(3) の形をすべて正しく書いている", 3), ("want と enjoy の目的語の違いを説明している", 3), ("(3) が目的を表す副詞的用法であることを説明している", 2)], d=4, p=8, lines=5,
                ap="空所の直前の語が「to をとる動詞」「ing をとる動詞」か、それとも文がすでに完成していて目的を付け足しているのかを見分ける。",
                steps=[f"(1) want は to をとる → to {base}。", f"(2) enjoy は ing をとる → {ing}。", f"(3) 「～するために」の目的 → to {base}。", "それぞれの理由をまとめる。"],
                alt=["それぞれの文を日本語に訳し、「～したい」「～して楽しんだ」「～するために行った」と自然に読めるかを確かめる。"],
                pc=[("3つの形", 3), ("目的語の違いの理由", 3), ("副詞的用法の理由", 2)],
                pit=["(2) を to ～ にする（enjoyed to ～）。", "(3) を ing 形にして「～しに」の意味を表そうとする。"])


DREAMS = [
    ("医者", "I want to be a doctor in the future. I'm going to study science hard to help sick people.",
     "want to be で将来の夢、be going to で予定、to help で目的を表している。"),
    ("料理人", "I want to be a cook. I will go to France to learn French cooking.",
     "want to be で夢、will で未来の行動、to learn で目的を表している。"),
    ("サッカー選手", "My dream is to be a soccer player. I'm going to practice every day to become a better player.",
     "My dream is to ～ で夢、be going to で予定、to become で目的を表している。"),
    ("先生", "I want to be an English teacher. I will study abroad to improve my English.",
     "want to be で夢、will で未来の行動、to improve で目的を表している。"),
    ("獣医", "I want to be a vet in the future. I'm going to read a lot of books about animals to learn about them.",
     "want to be で夢、be going to で予定、to learn で目的を表している。"),
    ("宇宙飛行士", "My dream is to go to space. I will study hard to become an astronaut.",
     "My dream is to ～ で夢、will で未来の行動、to become で目的を表している。"),
]


@gen("thinking_writing", 2, ["cross_unit", "written_reasoning", "application"], rel=["JH-ENG-G2-U01"])
def write_dream(r):
    job, model, point = r.choice(DREAMS)
    return desc(f"「{job}になりたい」という将来の夢について、英語で2文書きなさい。ただし、次の条件を守ること。\n・1文目は want to か My dream is to を使って夢を書く。\n・2文目は will か be going to を使い、さらに「～するために」を表す to＋動詞の原形を入れて、夢のためにすることを書く。",
                f"（解答例）{model}", f"（解答例の解説）{point} 未来表現（will / be going to）の後ろも、不定詞の to の後ろも動詞の原形にする。",
                [("1文目が want to / My dream is to＋原形で夢を表している", 3), ("2文目に will / be going to と目的の to＋原形が正しく使われている", 3), ("つづり・語順・大文字・ピリオドが正しい", 2)], d=4, p=8, lines=4,
                ap="前の単元の未来表現（will / be going to）と、この単元の不定詞（名詞的・副詞的）を組み合わせる。どちらの後ろも動詞の原形。",
                steps=["夢を want to be ～. か My dream is to ～. で書く。", "夢のためにする行動を will / be going to＋原形で書く。", "その行動の目的を to＋原形で文の後ろに加える。", "2文のつながりが自然かを見直す。"],
                alt=["書いた2文目から「～するために」の部分を取り除いても文が成り立つかを確かめる（成り立てば副詞的用法として正しく付け加えられている）。"],
                pc=[("夢の文", 3), ("未来表現と目的の不定詞", 3), ("表記の正確さ", 2)],
                pit=["will to study ～ のように will の後ろに to を入れる。", "I'm going to studying ～ のように原形以外を置く。"])


HOBBY = [
    ("読書", "My hobby is reading books. I enjoy reading in my room on weekends.", "My hobby is reading（補語の動名詞）と enjoy reading（目的語の動名詞）"),
    ("サッカー", "Playing soccer is fun for me. I practice kicking the ball every day.", "Playing soccer（主語の動名詞）と practice kicking（目的語の動名詞）"),
    ("料理", "I'm good at cooking. I like making curry for my family.", "good at cooking（前置詞の後ろの動名詞）と like making（目的語の動名詞）"),
    ("写真", "My hobby is taking pictures. I'm interested in taking pictures of birds.", "My hobby is taking（補語の動名詞）と interested in taking（前置詞の後ろの動名詞）"),
    ("音楽", "Listening to music is my favorite thing. I enjoy listening to music after dinner.", "Listening to music（主語の動名詞）と enjoy listening（目的語の動名詞）"),
    ("ダンス", "I'm good at dancing. I practice dancing with my friends after school.", "good at dancing（前置詞の後ろの動名詞）と practice dancing（目的語の動名詞）"),
]


@gen("thinking_writing", 2, ["application", "written_reasoning"])
def write_hobby(r):
    hb, model, point = r.choice(HOBBY)
    return desc(f"あなたの趣味が「{hb}」だとして、それを紹介する英文を2文書きなさい。ただし、2文とも動名詞を使い、主語・目的語・前置詞の後ろのうち、異なる2つの位置に動名詞を置くこと。",
                f"（解答例）{model}", f"（解答例の解説）{point}を使っている。主語の動名詞は単数扱いで is を使う。",
                [("1文目に動名詞を正しく使っている", 3), ("2文目に、1文目と異なる位置で動名詞を正しく使っている", 3), ("つづり・語順・大文字・ピリオドが正しい", 2)], d=4, p=8, lines=4,
                ap="動名詞を置ける位置（主語・目的語・補語・前置詞の後ろ）を思い出し、2つの文で違う位置を選ぶ。",
                steps=["使う位置を2つ決める（例：主語と、enjoy の目的語）。", "1文目を書く（Playing ～ is ～. など）。", "2文目を書く（I enjoy ～ing ～. など）。", "動名詞の位置が条件どおり異なっているかを見直す。"],
                alt=["書いた動名詞を名詞（soccer, music など）に置きかえても文が成り立つかを確かめると、名詞の位置に正しく置けているかがわかる。"],
                pc=[("1文目の動名詞", 3), ("2文目の動名詞（異なる位置）", 3), ("表記の正確さ", 2)],
                pit=["主語の動名詞の後ろを are にする。", "enjoy to ～ や good at play のように、動名詞以外を置く。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(task, wrong, step, etype, tempt, fix, expl, steps, ap, alt, pit):
    return desc(f"{task}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい英文に書き直しなさい。", fix, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい英文に直している", 3), ("文法のルールを説明している", 1)], d=3, p=6, lines=4,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい英文", 3), ("ルールの説明", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix))


OBJ_ERR = [
    ("私たちは公園でバドミントンをして楽しんだ。", "We enjoyed to play badminton in the park.", "We enjoyed playing badminton in the park.", "enjoyed to play", "concept",
     "enjoy は目的語に動名詞だけをとる。to play を playing にする。", "「～すること」は to ～ で表すと覚えていて、どの動詞にも使えると考えた。"),
    ("私は将来、パイロットになりたい。", "I want being a pilot in the future.", "I want to be a pilot in the future.", "want being", "concept",
     "want は目的語に不定詞だけをとる。being を to be にする。", "「～すること」を ing で表せると考え、want にも使った。"),
    ("ケンはもう手紙を書き終えた。", "Ken finished to write the letter.", "Ken finished writing the letter.", "finished to write", "concept",
     "finish は目的語に動名詞だけをとる。to write を writing にする。", "日本語の「書き終える」を「書くことを終える」と考え、不定詞を使った。"),
    ("私の兄はアメリカに留学することに決めた。", "My brother decided studying in America.", "My brother decided to study in America.", "decided studying", "concept",
     "decide は目的語に不定詞だけをとる。studying を to study にする。", "enjoy などと同じように ing をとると考えた。"),
    ("彼女は毎日ギターをひく練習をしている。", "She practices to play the guitar every day.", "She practices playing the guitar every day.", "practices to play", "concept",
     "practice は目的語に動名詞だけをとる。to play を playing にする。", "「～する練習」を「～するための練習」と考え、不定詞を使った。"),
    ("私はまたあなたに会いたいと思っている。", "I hope seeing you again.", "I hope to see you again.", "hope seeing", "concept",
     "hope は目的語に不定詞だけをとる。seeing を to see にする。", "like などと同じように ing もとれると考えた。"),
    ("トムは日本語を話したがっている。", "Tom wants to speaks Japanese.", "Tom wants to speak Japanese.", "to speaks", "concept",
     "to の後ろは主語に関係なく動詞の原形。speaks を speak にする。", "主語 Tom が三人称単数なので、後ろの動詞にも s をつけると考えた。"),
    ("私は昨日、新しい靴を買いたかった。", "I wanted to bought new shoes yesterday.", "I wanted to buy new shoes yesterday.", "to bought", "concept",
     "to の後ろは時制に関係なく動詞の原形。bought を buy にする。", "過去の文なので、後ろの動詞も過去形にすると考えた。"),
]


@gen("error_correction", 4, ["common_error", "condition_check"])
def err_object(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(OBJ_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", etype, tempt, fix, f"{rule}正しくは {fix}",
                    ["文の動詞が目的語に to ～ と ～ing のどちらをとるかを確認する。", f"「{where}」の部分の誤りを見つける：{rule}", f"正しい英文：{fix}"],
                    "want / hope / decide は to ～、enjoy / finish / practice は ～ing。to の後ろはいつも原形。この2点を1つずつ確かめる。",
                    ["直した文を日本語に訳し直し、「これからすること」なら to ～、「実際にしている動作」なら ～ing になっているかを手がかりで確かめる。"],
                    ["動詞ごとに to と ing のどちらをとるかを確かめずに書く。", "to の後ろの動詞を主語や時制に合わせて変化させる。"])


PREP_ERR = [
    ("私の姉はテニスをするのが得意です。", "My sister is good at play tennis.", "My sister is good at playing tennis.", "at play", "concept",
     "at は前置詞。前置詞の後ろに動作を置くときは動名詞にする。play を playing にする。", "「テニスをする」をそのまま play tennis と並べた。"),
    ("手伝ってくれてありがとう。", "Thank you for help me.", "Thank you for helping me.", "for help", "concept",
     "for は前置詞なので、後ろの動詞は動名詞 helping にする。", "help を名詞（手助け）と同じように考え、me を後ろに置いた。"),
    ("放課後、図書館へ行くのはどうですか。", "How about go to the library after school?", "How about going to the library after school?", "about go", "concept",
     "How about の about は前置詞。後ろの動詞は going にする。", "Let's go ～. と同じように原形を続けた。"),
    ("私は外国の文化を学ぶことに興味があります。", "I'm interested in to learn foreign cultures.", "I'm interested in learning foreign cultures.", "in to learn", "concept",
     "前置詞 in の後ろに不定詞は置けない。動名詞 learning にする。", "「学ぶこと」は to learn で表せると覚えていた。"),
    ("寝る前に宿題を終わらせなさい。", "Finish your homework before go to bed.", "Finish your homework before going to bed.", "before go", "concept",
     "ここでの before は前置詞。後ろの動詞は動名詞 going にする。（before you go to bed のように主語＋動詞を続けることもできる）", "before の後ろに動詞の原形をそのまま置けると考えた。"),
    ("英語の本を読むことは楽しい。", "Reading English books are fun.", "Reading English books is fun.", "are", "condition",
     "動名詞のかたまりが主語のときは単数扱い。be 動詞は is にする。", "直前の books（複数）につられて are にした。"),
    ("彼はひと言も言わずに出ていった。", "He went out without say a word.", "He went out without saying a word.", "without say", "concept",
     "without は前置詞。後ろの動詞は動名詞 saying にする。", "日本語の「言わずに」を、without＋原形で表せると考えた。"),
]


@gen("error_correction", 3, ["common_error", "computation"])
def err_prep(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(PREP_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", etype, tempt, fix, f"{rule}正しくは {fix}",
                    ["前置詞（at / for / about / in / before / without）の後ろの動詞の形を確認する。", "動名詞が主語のときは、be 動詞が単数扱いになっているかを確認する。", f"正しい英文：{fix}"],
                    "前置詞の後ろは名詞の位置。動作を置くときは名詞の働きをする動名詞にする。",
                    ["直した動名詞の部分を名詞（tennis, the library など）に置きかえても文が成り立つかを確かめる。"],
                    ["前置詞の後ろに原形や to ～ を置く。", "動名詞の主語の後ろの be 動詞を、直前の名詞につられて are にする。"])


USE_ERR = [
    ("私は牛乳を買うためにその店へ行った。", "I went to the store for buy some milk.", "I went to the store to buy some milk.", "for buy", "concept",
     "「～するために」と目的を表すときは to＋原形を使う（副詞的用法）。for buy という形はない。", "日本語の「～のために」を for で表そうとした。"),
    ("私には今日するべき宿題がたくさんある。", "I have a lot of to do homework today.", "I have a lot of homework to do today.", "to do homework", "notation",
     "「するべき宿題」は名詞 homework の後ろに to do を置く（形容詞的用法）。", "日本語の語順（するべき→宿題）のまま英語にした。"),
    ("何か温かい飲み物がほしい。", "I want hot something to drink.", "I want something hot to drink.", "hot something", "notation",
     "something を説明する形容詞は something の後ろに置く。something hot to drink の順。", "日本語の「温かい何か」の語順につられた。"),
    ("私はその知らせを聞いて驚いた。", "I was surprised hearing the news.", "I was surprised to hear the news.", "hearing", "concept",
     "感情の原因「～して」は、感情を表す語の後ろに to＋原形を置いて表す（副詞的用法）。", "「～して」を ing 形で表せると考えた。"),
    ("私の夢は歌手になることです。", "My dream is be a singer.", "My dream is to be a singer.", "is be", "concept",
     "be 動詞の後ろに「～すること」を置くときは、to＋原形（または動名詞）にする。is be のように動詞を2つ並べることはできない。", "「～になること」の「こと」を表す to を落とした。"),
    ("ユミは英語を勉強するためにイギリスへ行った。", "Yumi went to the U.K. to studied English.", "Yumi went to the U.K. to study English.", "to studied", "concept",
     "to の後ろは時制に関係なく原形。studied を study にする。", "過去の文なので、to の後ろの動詞も過去形にすると考えた。"),
]


@gen("error_correction", 3, ["common_error", "concept"])
def err_usage(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(USE_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", etype, tempt, fix, f"{rule}正しくは {fix}",
                    ["日本語の「～するために」「～するための」「～して」「～すること」のどれに当たるかを確認する。", f"「{where}」の部分の誤りを見つける：{rule}", f"正しい英文：{fix}"],
                    "不定詞の3用法は、どれも〈to＋原形〉の形。意味（ために／ための／して／こと）に合わせて、置く位置を決める。",
                    ["直した英文の to ～ の部分を日本語に訳して、問題の日本語の意味と一致するかを確かめる。"],
                    ["「～のために」を for で表す。", "形容詞的用法の to ～ を名詞の前に置く。"])


GENERATORS = [inf_object, gerund_object, which_use, prep_gerund, which_verb,
              jp_to_en, rewrite, build_order, adj_use, why_to,
              explain_difference, three_forms, write_dream, write_hobby,
              err_object, err_prep, err_usage]
