"""単元パック：英語コミュニケーションⅠ 不定詞・動名詞（意味上の主語・完了不定詞・不定詞と動名詞で意味が変わる動詞）。"""
from banks._common import desc, mc, order, sa
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem,
                         tp)

UNIT_ID = "HS-ENG-U04"


# ======================================================================
# 授業プリント
# ======================================================================

LESSON = lesson(
    goals=["不定詞・動名詞の意味上の主語を、for / of ／所有格・目的格を使い分けて正しく表せる。",
           "完了不定詞（to have＋過去分詞）・完了動名詞（having＋過去分詞）が「述語動詞より前の時」を表すことを理解し、that 節と書きかえられる。",
           "remember / forget / stop / try / regret などで、不定詞と動名詞による意味の違いを説明できる。"],
    duration=50,
    readiness=["不定詞の名詞的・形容詞的・副詞的用法を中学で学習している。", "動名詞が「～すること」の意味で主語・目的語になることを知っている。",
               "現在形・過去形・現在完了・過去完了の形と意味を区別できる（HS-ENG-U02 時制）。"],
    flow=[("導入：だれが・いつ", 5, "Remember to call me. と I remember calling you. を比べ、形が違うと「いつのことか」が変わることに気づかせる"),
          ("意味上の主語", 12, "It is ～ for / of 人 to do の使い分けと、動名詞の所有格・目的格の主語を整理する（例題1）"),
          ("完了不定詞・完了動名詞", 13, "seem to do / seem to have done を that 節と対応させ、時のずれを図で確認する（例題2）"),
          ("意味が変わる動詞", 13, "不定詞＝これから、動名詞＝すでに・現実、という傾向で remember / forget / regret / try / stop を整理する（例題3）"),
          ("まとめと確認", 7, "確認問題3問、問題プリントA の課題指示")],
    sections=[
        intro("in1", "なぜ「だれが」「いつ」を意識するのか",
              "不定詞と動名詞は、動詞に「～すること」などの意味を持たせて文の一部にする形である。しかし動詞から作られているので、もとの動詞が持っていた「だれがするのか（主語）」と「いつのことか（時）」の情報が、形の上では見えにくくなる。この単元では、その2つの情報をどう表すかを学ぶ。",
              bullets=["Remember to call me.（これから電話することを忘れないで）と I remember calling you.（電話したことを覚えている）では、電話する時が逆になる。",
                       "It is kind of you to help me. の of you は、「助ける」のがだれかを示している。",
                       "He seems to have been rich. の to have been は、「金持ちだった」のが seems より前のことを示す。"],
              points=[tp("2つの remember の文を板書し、電話するのは「これから」か「もう済んだ」かを生徒に判断させる。", ask="Remember to call me. で、電話はもうかけたか。",
                         expect="まだかけていない。これからかける。", timing="導入の冒頭"),
                      tp("不定詞・動名詞は「動詞の働きを残した名詞・形容詞・副詞」なので、主語や時制の情報を別の方法で補う必要がある、と全体像を示す。")]),
        definition("df1", "意味上の主語",
                   "不定詞や動名詞の動作をする人が、文の主語と異なるときは、その人を「意味上の主語」として示す。示さない場合は、文の主語または一般の人が動作をすると解釈される。",
                   bullets=["不定詞：for＋人＋to do が基本。It is difficult for me to answer the question.（質問に答えるのは私には難しい）",
                            "人の性質・性格を評価する形容詞（kind, careless, wise, foolish, rude, brave, clever など）のときは of＋人。It was careless of him to lose the key.",
                            "動名詞：動名詞の前に所有格または目的格を置く。I'm sure of his winning.（彼が勝つことを確信している）／ Do you mind my opening the window?（私が窓を開けてもかまいませんか）",
                            "意味上の主語を示さないと、文の主語の動作になる。I'm sure of winning. は「（私が）勝つことを確信している」。"],
                   conditions=["of を使うのは「人＝形容詞」が成り立つとき（He was careless. が言える）。The question is difficult. のように行為が主語になる形容詞は for。",
                               "動名詞の意味上の主語は、文頭の主語の位置では所有格を使うのが普通（His coming late surprised us.）。目的語の位置では目的格もよく使われる。"],
                   points=[tp("for と of の判定には「人を主語にして be＋形容詞の文が言えるか」というテストを使わせる。", ask="It was kind of you ... で You were kind. は言えるか。It is difficult for you ... で You are difficult. は同じ意味になるか。",
                              expect="You were kind. は自然に言えるので of。You are difficult. は「あなたは気難しい」という別の意味になるので for。", caution="nice / good も人の性質を評価する場合は of をとる。")]),
        theorem("th1", "完了不定詞・完了動名詞が表す時",
                "to do／doing ＝ 述語動詞と同じ時（またはそれより後）　　to have＋過去分詞／having＋過去分詞 ＝ 述語動詞より前の時",
                ["He seems to be rich. ＝ It seems that he is rich.（seems と is は同じ「今」）",
                 "He seems to have been rich. ＝ It seems that he was rich.（was は seems より前）",
                 "He seemed to have been rich. ＝ It seemed that he had been rich.（述語動詞が過去なら、それより前は過去完了）",
                 "I'm ashamed of having been lazy. ＝ I'm ashamed that I was lazy.（完了動名詞も同じ考え方）"],
                body="完了不定詞・完了動名詞は「時のずれ」を表す目印である。seem / appear / be said / be believed / be thought などと組み合わせて、うわさや推測の内容がいつのことかを示すときによく使われる。",
                points=[tp("時間軸の図（過去 ― 現在）を板書し、述語動詞の位置と不定詞・動名詞の位置を矢印で示す。", ask="He seemed to have been rich. で、金持ちだったのはいつか。",
                           expect="seemed（過去）よりさらに前。", timing="定理の説明時")]),
        derivation("dv1", "that 節から完了不定詞が作られる仕組み",
                   ["① It seems that he was rich. から出発する。that 節の主語 he を文の主語にする。",
                    "② 主語を前に出すと、that 節の動詞 was は、seems の後ろで to 不定詞の形に変えなければならない（不定詞には時制がない）。",
                    "③ 単純に to be にすると He seems to be rich. となり、「今、金持ちのようだ」という意味になって、was が持っていた「過去」の情報が失われる。",
                    "④ そこで、述語動詞 seems より前であることを示すために、完了の形 have＋過去分詞を使い、to have been とする。",
                    "⑤ 結果：He seems to have been rich. 逆に、that 節の動詞が述語動詞と同じ時（is）なら、単純な to be でよい。",
                    "⑥ 確かめ：完了不定詞の文を that 節に戻し、述語動詞との時の前後が元の文と一致するかを確認する。"],
                   body="不定詞・動名詞は時制を持たないため、「前の時」は完了の形でしか表せない。これが完了不定詞・完了動名詞が必要になる理由である。ただし、remember doing のように動詞の意味そのものが過去を指す場合は、単純な動名詞で過去のことを表せる。",
                   points=[tp("②の「不定詞には時制がない」が要点。to was や to were が存在しないことを確認させてから④に進む。",
                              ask="It seems that he was rich. の was を不定詞にするとき、to was と書けるか。", expect="書けない。不定詞は to＋原形なので、過去は have＋過去分詞で表す。")]),
        definition("df2", "不定詞と動名詞で意味が変わる動詞",
                   "目的語に不定詞をとるか動名詞をとるかで意味が変わる動詞がある。一般に、不定詞は「これから行うこと（未来・意図）」、動名詞は「すでに行ったこと・実際に行っていること」を表しやすい。",
                   bullets=["remember to do「忘れずに～する」／ remember doing「～したことを覚えている」",
                            "forget to do「～するのを忘れる」／ forget doing「～したことを忘れる」（never forget doing の形が多い）",
                            "regret to do「残念ながら～する」／ regret doing「～したことを後悔する」",
                            "try to do「～しようと努める」／ try doing「試しに～してみる」",
                            "stop doing「～するのをやめる」／ stop to do「～するために立ち止まる・手を止める」（この to do は目的を表す副詞的用法）",
                            "目的語に不定詞だけをとる動詞：want, hope, decide, promise, refuse, plan, manage, afford など。動名詞だけをとる動詞：enjoy, finish, mind, avoid, give up, consider, suggest, deny など。"],
                   conditions=["look forward to doing, be used to doing, object to doing の to は前置詞なので、後ろは動名詞。",
                               "stop to do の to do は stop の目的語ではない。stop の目的語は動名詞だけである。"],
                   points=[tp("「不定詞＝これから、動名詞＝すでに」は傾向であって絶対の規則ではないこと（like to do / like doing はほぼ同じ意味など）も補足する。",
                              caution="stop to do を「～するのをやめる」と訳す誤りが非常に多い。")]),
        example("ex1", "例題1　意味上の主語",
                "（　）に for か of を入れなさい。(1) It was very nice (　　) you to invite me.　(2) It is hard (　　) young children to sit still for an hour.",
                ["(1) nice は人の性質を評価する形容詞。You were very nice. と言えるので of。",
                 "(2) hard は行為（じっと座っていること）の難しさを評価する。Young children are hard. とは言えないので for。"],
                "(1) of　(2) for",
                thinking="意味上の主語の人を主語にして「人 is 形容詞」の文が同じ意味で成り立つかを確かめる。",
                points=[tp("(2) で young children を主語にして言いかえると、Sitting still for an hour is hard for young children. となり、hard の主語は行為であることを確認させる。")],
                misconceptions=[("It was very nice for you to invite me.", "nice は人の性質の評価なので of you。for を使うと「あなたにとって」という別の意味になる")]),
        example("ex2", "例題2　完了不定詞への書きかえ",
                "次の文を、下線部を主語にしてほぼ同じ意味の文に書きかえなさい。(1) It seems that [[u:she]] lived in Canada as a child.　(2) It seemed that [[u:the man]] was very tired.",
                ["(1) lived（過去）は seems（現在）より前なので、完了不定詞 to have lived を使う。", "(1) She seems to have lived in Canada as a child.",
                 "(2) was（過去）は seemed（過去）と同じ時なので、単純な to be を使う。", "(2) The man seemed to be very tired."],
                "(1) She seems to have lived in Canada as a child.　(2) The man seemed to be very tired.",
                thinking="that 節の動詞の時が、述語動詞（seem）と同じか、それより前かを比べる。",
                points=[tp("(2) で to have been を選ぶ生徒が多い。「どちらも過去形だから同じ時」と述語動詞と比べる習慣をつけさせる。", ask="(2) で was と seemed はどちらが先か。", expect="同じ時（過去）。")]),
        example("ex3", "例題3　意味が変わる動詞",
                "（　）内の語を適切な形にしなさい。(1) I'll never forget (see) the sunrise from the top of Mt. Fuji.　(2) Please remember (turn) off the lights when you leave.",
                ["(1) 富士山頂から日の出を見たのはすでに経験したこと。never forget doing「～したことを決して忘れない」の形で seeing。",
                 "(2) 部屋を出るときに電気を消すのはこれから行うこと。remember to do「忘れずに～する」で to turn。"],
                "(1) seeing　(2) to turn",
                thinking="目的語の動作が「すでに行ったこと」か「これから行うこと」かを、文中の時の手がかり（never forget / when you leave）から判断する。",
                points=[tp("文中の時の手がかりに下線を引かせ、根拠を示して答える習慣をつけさせる。")],
                misconceptions=[("Please remember turning off the lights when you leave.", "これから行う動作なので remember to do。turning にすると「消したことを覚えておいて」となり意味が通らない")]),
        board("bd1", "板書案",
              [("① 意味上の主語", ["It is 形容詞 for 人 to do（行為の評価）", "It is 形容詞 of 人 to do（人の性質）", "テスト：人 is 形容詞 が言える → of", "動名詞：his / him ＋ doing", "I'm sure of his winning."]),
               ("② 時のずれ", ["to do / doing ＝ 述語動詞と同じ時", "to have p.p. / having p.p. ＝ 述語動詞より前", "seems to have been ＝ that he was", "seemed to have been ＝ that he had been"]),
               ("③ 意味が変わる動詞", ["to do ＝ これから／doing ＝ すでに", "remember / forget / regret", "try to do（努める）／ try doing（試す）", "stop doing（やめる）", "stop to do（～するために止まる）"])],
              points=[tp("板書は3列に分け、①は判定テスト、②は時間軸の図、③は「これから／すでに」の対比表として整理する。②の時間軸は生徒のノートにも必ず書かせる。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("for / of の判断は、形容詞の暗記に頼らず「人 is 形容詞」のテストで確かめさせる。", ask="It is necessary for you to go. で You are necessary. は同じ意味になるか。", expect="ならないので for。"),
               tp("完了不定詞は「過去形の代わり」ではなく「述語動詞より前」を表すことを強調する。seemed と組み合わさると過去完了に対応する。", caution="He seemed to have been ... を It seemed that he was ... と直す誤りが多い。"),
               tp("動名詞の意味上の主語を省くと、文の主語の動作になることを、Do you mind opening ...? と Do you mind my opening ...? の対比で示す。", timing="定義1の説明後"),
               tp("look forward to / be used to / object to の to は前置詞であることを、後ろに名詞（the party など）を置けることから確認させる。"),
               tp("問題プリント D の誤答例を使い、「不定詞と動名詞の取り違え」「時のずれの見落とし」の2種類の誤りを分類させる。")],
              misconceptions=[("I'm looking forward to see you.", "look forward to の to は前置詞なので動名詞を続ける。I'm looking forward to seeing you."),
                              ("He stopped to smoke.（たばこをやめた、のつもり）", "stop to do は「～するために立ち止まる」。やめたなら He stopped smoking."),
                              ("It was careless for him to forget it.", "careless は人の性質の評価なので of him。")]),
        summary("sm1", "まとめ",
                ["意味上の主語は、不定詞では for＋人（人の性質を評価する形容詞なら of＋人）、動名詞では所有格・目的格で示す。",
                 "完了不定詞・完了動名詞は述語動詞より前の時を表す。that 節に書きかえて時の関係を確かめる。",
                 "不定詞は「これから」、動名詞は「すでに・実際に」を表しやすい。remember / forget / regret / try / stop は形によって意味が変わる。"]),
        check("ck1", "確認問題",
              [("It was wise (　　) him to stay home. の（　）に入る前置詞を答えなさい。", "of（He was wise. が成り立つ、人の性質の評価）"),
               ("It seems that she was a nurse. を She を主語にして書きかえなさい。", "She seems to have been a nurse."),
               ("He stopped to talk to me. と He stopped talking to me. の意味の違いを答えなさい。", "前者は「私に話しかけるために立ち止まった」、後者は「私に話しかけるのをやめた」。")]),
    ])


# ======================================================================
# 共通の部品
# ======================================================================

def form_mc(s, jp, ok, wrongs, expl, ap, steps, alt, pit, mis, d=2, pc=None, intro_text="日本語の意味になるように、（　）に入る最も適切なものを選びなさい。"):
    return mc(f"{intro_text}\n{jp}\n{s}", [ok] + [w for w, _ in wrongs], expl, d=d,
              ap=ap, steps=steps, alt=alt, pc=pc or [("用いる形（不定詞・動名詞など）を正しく判断している", 1), ("正しい選択肢を選んでいる", 1)],
              pit=pit, why={w: (reason, mis) for w, reason in wrongs})


# ======================================================================
# A 基本確認
# ======================================================================

# (英文, 和訳, 動詞, 'to' or 'ing', 原形, ing形)
VERB_OBJ = [
    ("We decided (　　) the trip because of the typhoon.", "台風のため、私たちは旅行を延期することに決めた。", "decide", "to", "put off", "putting off"),
    ("My brother finally gave up (　　) for the bus and started walking.", "弟はついにバスを待つのをあきらめて歩き始めた。", "give up", "ing", "wait", "waiting"),
    ("Have you finished (　　) your report yet?", "レポートはもう書き終わりましたか。", "finish", "ing", "write", "writing"),
    ("She promised (　　) me by Friday.", "彼女は金曜日までに私に電話すると約束した。", "promise", "to", "call", "calling"),
    ("I really enjoyed (　　) with your family last weekend.", "先週末はあなたの家族と話せてとても楽しかった。", "enjoy", "ing", "talk", "talking"),
    ("He refused (　　) the reporter's question.", "彼はその記者の質問に答えるのを拒んだ。", "refuse", "to", "answer", "answering"),
    ("You should avoid (　　) too much sugar.", "砂糖のとりすぎは避けるべきだ。", "avoid", "ing", "eat", "eating"),
    ("We are planning (　　) a party for Ms. Mori.", "私たちは森先生のためにパーティーを開く計画を立てている。", "plan", "to", "hold", "holding"),
    ("Would you consider (　　) our club?", "私たちの部に入ることを考えてみてくれませんか。", "consider", "ing", "join", "joining"),
    ("I can't afford (　　) a new smartphone now.", "今は新しいスマートフォンを買う余裕がない。", "afford", "to", "buy", "buying"),
    ("The boy denied (　　) the window.", "その少年は窓を割ったことを否定した。", "deny", "ing", "break", "breaking"),
    ("She managed (　　) the last train.", "彼女はなんとか終電に間に合った。", "manage", "to", "catch", "catching"),
    ("Mika suggested (　　) the museum on Sunday.", "ミカは日曜日に博物館へ行こうと提案した。", "suggest", "ing", "visit", "visiting"),
    ("They agreed (　　) the cost of the party.", "彼らはパーティーの費用を分担することに同意した。", "agree", "to", "share", "sharing"),
    ("Please practice (　　) these words aloud.", "これらの単語を声に出して言う練習をしなさい。", "practice", "ing", "say", "saying"),
    ("He pretended (　　) asleep when his mother came in.", "母親が入ってきたとき、彼は眠っているふりをした。", "pretend", "to", "be", "being"),
]


@gen("basic_check", 5, ["computation", "condition_check"])
def verb_object_form(r):
    s, jp, v, kind, base, ing = r.choice(VERB_OBJ)
    to_v, to_ing = f"to {base}", f"to {ing}"
    if kind == "to":
        ok = to_v
        wrongs = [(ing, f"{v} は目的語に to 不定詞をとり、動名詞はとらない。"),
                  (base, f"{v} の後ろに動詞の原形を直接置くことはできない。"),
                  (to_ing, "不定詞の to の後ろには動詞の原形が続く。to＋ing 形にはならない。")]
        rule = f"{v} は目的語に to 不定詞だけをとる動詞（これから行うことを表す動詞に多い）"
    else:
        ok = ing
        wrongs = [(to_v, f"{v} は目的語に動名詞をとり、to 不定詞はとらない。"),
                  (base, f"{v} の後ろに動詞の原形を直接置くことはできない。"),
                  (to_ing, f"{v} の後ろに前置詞 to は不要。動名詞を直接続ける。")]
        rule = f"{v} は目的語に動名詞だけをとる動詞（すでに行っていること・やめる・避けることを表す動詞に多い）"
    return form_mc(s, jp, ok, wrongs, f"{ok} が入る。{rule}である。", d=1,
                   ap="空所の前の動詞が、目的語に不定詞をとる動詞か、動名詞をとる動詞かを確認する。",
                   steps=[f"空所の前の動詞 {v} を確認する。", f"{rule}。", f"よって {ok} を選ぶ。"],
                   alt=["「これから行うこと（未来・意図）」なら不定詞、「すでに行っている・行ったこと」なら動名詞という傾向から判断し、動詞の一覧で確かめる。"],
                   pit=["enjoy / finish / mind / avoid などの後ろに to 不定詞を置いてしまう。", "decide / hope / promise などの後ろに動名詞を置いてしまう。"],
                   mis="目的語に不定詞をとる動詞と動名詞をとる動詞の混同")


# (英文, 和訳, 'for' or 'of', 形容詞)
SUBJ = [
    ("It was careless (　　) you to leave your bag on the train.", "電車にかばんを置き忘れるなんて、あなたは不注意だった。", "of", "careless"),
    ("It is difficult (　　) beginners to read this book.", "初心者がこの本を読むのは難しい。", "for", "difficult"),
    ("It was very kind (　　) her to show me the way.", "道を教えてくれるとは、彼女はとても親切だった。", "of", "kind"),
    ("It is necessary (　　) us to check the data again.", "私たちはそのデータをもう一度確かめる必要がある。", "for", "necessary"),
    ("It was brave (　　) him to tell the truth.", "本当のことを話すとは、彼は勇気があった。", "of", "brave"),
    ("It is dangerous (　　) children to swim in this river.", "子どもがこの川で泳ぐのは危険だ。", "for", "dangerous"),
    ("It was rude (　　) him to leave without a word.", "何も言わずに立ち去るとは、彼は失礼だった。", "of", "rude"),
    ("It is important (　　) everyone to get enough sleep.", "だれにとっても十分な睡眠をとることは大切だ。", "for", "important"),
    ("It was wise (　　) you to bring an umbrella.", "傘を持ってきたのは賢明だったね。", "of", "wise"),
    ("It is impossible (　　) me to finish this work by noon.", "私がこの仕事を正午までに終えるのは不可能だ。", "for", "impossible"),
    ("It was generous (　　) them to donate so much money.", "あれほど多くのお金を寄付するとは、彼らは気前がよかった。", "of", "generous"),
    ("It is easy (　　) him to solve such a problem.", "彼にとってそのような問題を解くのはたやすい。", "for", "easy"),
    ("It was foolish (　　) me to believe that story.", "あの話を信じるなんて、私はばかだった。", "of", "foolish"),
    ("It is natural (　　) parents to worry about their children.", "親が子どものことを心配するのは当然だ。", "for", "natural"),
]


@gen("basic_check", 5, ["condition_check", "concept"])
def for_or_of(r):
    s, jp, ok, adj = r.choice(SUBJ)
    person = s.split("(　　) ")[1].split(" to ")[0]
    if ok == "of":
        test = f"{person} を主語にして「{person} was/is {adj}」と言え、人の性質・性格を評価している"
        other = ("for", f"{adj} は人の性質・性格を評価する形容詞なので、意味上の主語は of で示す。for を使うと人の性質の評価にならない。")
    else:
        test = f"{adj} は行為（to 以下）を評価しており、{person} を主語にして同じ意味の文は作れない"
        other = ("of", f"of を使うのは人の性質・性格を評価する形容詞のとき。{adj} は行為の難しさ・必要性などを評価するので for。")
    wrongs = [other, ("to", "不定詞の意味上の主語は to ではなく for / of で示す。"),
              ("with", "不定詞の意味上の主語を with で示すことはない。")]
    return form_mc(s, jp, ok, wrongs, f"{ok} が入る。{test}。", d=2,
                   ap="空所の後ろの人を主語にして「人 is 形容詞」の文が同じ意味で成り立つか（人の性質の評価か）を確かめる。",
                   steps=[f"形容詞 {adj} と、空所の後ろの人 {person} を確認する。", f"{test}。", f"よって {ok} を選ぶ。"],
                   alt=[f"It is {adj} ... の文を「～するとは（人は）{adj}だ」と訳せれば of、「（人が）～するのは{adj}だ」と訳せれば for と、和訳の形から確かめる。"],
                   pit=["kind / careless などの性質を表す形容詞でも for を使ってしまう。", "意味上の主語の前置詞を省いてしまう。"],
                   mis="意味上の主語を示す for と of の混同")


# (英文, 和訳, 述語動詞, 正答, [誤答3], 時の手がかり, 前の時か)
PERF = [
    ("The old man seems (　　) rich in his youth.", "その老人は若いころ裕福だったようだ。", "seems", "to have been", ["to be", "being", "having been"], "in his youth（若いころ）", True),
    ("Ken seems (　　) a bad cold now.", "ケンは今ひどいかぜをひいているようだ。", "seems", "to have", ["to have had", "having", "having had"], "now（今）", False),
    ("She appears (　　) her wallet on the train yesterday.", "彼女は昨日電車で財布をなくしたようだ。", "appears", "to have lost", ["to lose", "losing", "having lost"], "yesterday（昨日）", True),
    ("He is said (　　) a famous singer in his twenties.", "彼は20代のころ有名な歌手だったと言われている。", "is said", "to have been", ["to be", "being", "having been"], "in his twenties（20代のころ）", True),
    ("This castle is said (　　) about 400 years ago.", "この城は約400年前に建てられたと言われている。", "is said", "to have been built", ["to be built", "being built", "having been built"], "about 400 years ago（約400年前）", True),
    ("You seem (　　) a little tired today.", "今日は少し疲れているようですね。", "seem", "to be", ["to have been", "being", "having been"], "today（今日）", False),
    ("The singer is believed (　　) in this town as a child.", "その歌手は子どものころこの町に住んでいたと信じられている。", "is believed", "to have lived", ["to live", "living", "having lived"], "as a child（子どものころ）", True),
    ("My grandfather seems (　　) very healthy these days.", "祖父は最近とても元気なようだ。", "seems", "to be", ["to have been", "being", "having been"], "these days（最近）", False),
    ("The thief appears (　　) through the back door last night.", "泥棒は昨夜、裏口から入ったようだ。", "appears", "to have entered", ["to enter", "entering", "having entered"], "last night（昨夜）", True),
    ("Mr. Ito is said (　　) the best cook in this town now.", "伊藤さんは今この町でいちばんの料理人だと言われている。", "is said", "to be", ["to have been", "being", "having been"], "now（今）", False),
    ("They seemed (　　) the news before I told them.", "私が話す前に、彼らはその知らせを聞いていたようだった。", "seemed", "to have heard", ["to hear", "hearing", "having heard"], "before I told them（私が話す前に）", True),
    ("She seemed (　　) happy at the party yesterday.", "昨日のパーティーで彼女は楽しそうだった。", "seemed", "to be", ["to have been", "being", "having been"], "at the party yesterday（seemed と同じ昨日のパーティーの時点）", False),
]


@gen("basic_check", 5, ["computation", "concept"])
def perfect_infinitive(r):
    s, jp, mv, ok, wr, cue, earlier = r.choice(PERF)
    head = mv.split()[-1]
    why = []
    for w in wr:
        if w.startswith("to have"):
            why.append((w, f"完了不定詞は述語動詞 {mv} より前の時を表す。この文は {cue} から、述語動詞と同じ時のことなので単純な不定詞を使う。"))
        elif w.startswith("to "):
            why.append((w, f"単純な不定詞は述語動詞 {mv} と同じ時を表す。この文は {cue} から、述語動詞より前のことなので完了不定詞を使う。"))
        else:
            why.append((w, f"{head} の後ろには to 不定詞が続く。動名詞（～ing / having＋過去分詞）は置けない。"))
    rel = "述語動詞より前の時" if earlier else "述語動詞と同じ時"
    itform = "It " + ({"seem": "seems", "appear": "appears"}.get(mv, mv)) + " that"
    return form_mc(s, jp, ok, why, f"{ok} が入る。{cue} から、不定詞の内容は{rel}のことである。", d=2,
                   ap="述語動詞（seem / appear / be said など）の時と、不定詞が表す内容の時を、文中の時の手がかりで比べる。",
                   steps=[f"述語動詞 {mv} の時を確認する。", f"時の手がかり {cue} から、不定詞の内容は{rel}だと判断する。",
                          "前の時なら to have＋過去分詞、同じ時なら to＋原形を選ぶ。", f"答え：{ok}"],
                   alt=[f"{itform} ... の形の文に戻し、that 節の動詞の時制と述語動詞の時制を比べて確かめる。"],
                   pit=["過去を表す語句があるのに単純な to be を使う。", "seemed（過去）と同じ時のことに完了不定詞を使う。"],
                   mis="単純不定詞と完了不定詞が表す時の混同")


# (英文, 和訳, 動詞, 原形, ing形, 過去分詞, 'to'/'ing', 規則, もう一方の形の意味)
MEAN = [
    ("Please remember (　　) the plants while I'm away.", "留守の間、忘れずに植物に水をやってください。", "remember", "water", "watering", "watered", "to",
     "remember to do「（これから）忘れずに～する」", "remember doing「（過去に）～したことを覚えている」"),
    ("I clearly remember (　　) this song in elementary school.", "小学校でこの歌を歌ったことをはっきり覚えている。", "remember", "sing", "singing", "sung", "ing",
     "remember doing「（過去に）～したことを覚えている」", "remember to do「（これから）忘れずに～する」"),
    ("Don't forget (　　) your passport tomorrow.", "明日パスポートを忘れずに持ってきてね。", "forget", "bring", "bringing", "brought", "to",
     "forget to do「（これから）～するのを忘れる」", "forget doing「（過去に）～したことを忘れる」"),
    ("I will never forget (　　) Mt. Fuji for the first time.", "初めて富士山に登ったことを決して忘れないだろう。", "forget", "climb", "climbing", "climbed", "ing",
     "never forget doing「（過去に）～したことを決して忘れない」", "forget to do「（これから）～するのを忘れる」"),
    ("He stopped (　　) when the teacher came in.", "先生が入ってくると、彼は話すのをやめた。", "stop", "talk", "talking", "talked", "ing",
     "stop doing「～するのをやめる」", "stop to do「～するために立ち止まる・手を止める」"),
    ("On the way home, she stopped (　　) a magazine at the store.", "帰り道、彼女は雑誌を買うために店に立ち寄った。", "stop", "buy", "buying", "bought", "to",
     "stop to do「～するために立ち止まる・立ち寄る」（to do は目的を表す副詞的用法）", "stop doing「～するのをやめる」"),
    ("I regret (　　) my teacher a lie.", "先生に嘘をついたことを後悔している。", "regret", "tell", "telling", "told", "ing",
     "regret doing「（過去に）～したことを後悔する」", "regret to do「残念ながら～する」"),
    ("We regret (　　) you that the event has been canceled.", "残念ながら、催しが中止になったことをお知らせします。", "regret", "inform", "informing", "informed", "to",
     "regret to do「残念ながら～する」", "regret doing「～したことを後悔する」"),
    ("Try (　　) this button if the machine stops.", "機械が止まったら、試しにこのボタンを押してみて。", "try", "press", "pressing", "pressed", "ing",
     "try doing「試しに～してみる」", "try to do「～しようと努める」"),
    ("I tried hard (　　) the box, but it was too heavy.", "箱を持ち上げようと懸命に努めたが、重すぎた。", "try", "lift", "lifting", "lifted", "to",
     "try to do「～しようと努める」（実際にできたかどうかは別）", "try doing「試しに～してみる」（実際にやってみる）"),
    ("Try (　　) some salt if the soup tastes bland.", "スープの味が薄ければ、試しに塩を少し入れてみて。", "try", "add", "adding", "added", "ing",
     "try doing「試しに～してみる」", "try to do「～しようと努める」"),
    ("After the speech, he went on (　　) questions from the audience.", "スピーチの後、彼は続けて聴衆からの質問に答えた。", "go on", "answer", "answering", "answered", "to",
     "go on to do「（あることを終えて）続けて次に～する」", "go on doing「（同じことを）～し続ける」"),
    ("She went on (　　) even after the bell rang.", "チャイムが鳴った後も、彼女は書き続けた。", "go on", "write", "writing", "written", "ing",
     "go on doing「（同じことを）～し続ける」", "go on to do「続けて次に～する」"),
    ("Missing the bus means (　　) for an hour.", "バスに乗り遅れると1時間待つことになる。", "mean", "wait", "waiting", "waited", "ing",
     "mean doing「～することを意味する・～することになる」", "mean to do「～するつもりである」"),
    ("I meant (　　) you, but I forgot.", "あなたに電話するつもりだったのに、忘れてしまった。", "mean", "call", "calling", "called", "to",
     "mean to do「～するつもりである」", "mean doing「～することを意味する」"),
]


@gen("basic_check", 5, ["concept", "common_error"])
def meaning_change(r):
    s, jp, v, base, ing, pp, kind, rule, other = r.choice(MEAN)
    ok = f"to {base}" if kind == "to" else ing
    alt_form = ing if kind == "to" else f"to {base}"
    wrongs = [(alt_form, f"{alt_form} にすると {other} の意味になり、日本語の意味と合わない。"),
              (base, f"{v} の後ろに動詞の原形を直接置くことはできない。"),
              (pp, f"過去分詞・過去形の {pp} をこの位置に置いても、「～すること」「～するために」の意味にならない。")]
    return form_mc(s, jp, ok, wrongs, f"{ok} が入る。{rule}。", d=2,
                   ap="目的語の動作が「これから行うこと」か「すでに行ったこと・実際に行うこと」かを、日本語と文中の時の手がかりから判断する。",
                   steps=[f"動詞 {v} は、不定詞と動名詞で意味が変わる動詞であることを確認する。", f"日本語の意味から、{rule} の形が必要だと判断する。", f"答え：{ok}"],
                   alt=[f"選んだ形と反対の形（{alt_form}）を入れて訳してみると「{other}」となり、日本語と合わないことを確かめる。"],
                   pit=["remember / forget の後ろの形を、動作の時（これから・すでに）を考えずに選ぶ。", "stop to do を「～するのをやめる」と考える。"],
                   mis="不定詞と動名詞で意味が変わる動詞の取り違え")


# ======================================================================
# B 標準演習
# ======================================================================

# (元の文, 答え, 別解, 説明)
SEEM_RW = [
    ("It seems that he was ill last week.", "He seems to have been ill last week.", [], "was（過去）は seems（現在）より前なので完了不定詞。"),
    ("It seems that she is happy with the result.", "She seems to be happy with the result.", [], "is と seems は同じ現在なので単純な不定詞。"),
    ("It seemed that they had lost their way.", "They seemed to have lost their way.", [], "had lost（過去完了）は seemed（過去）より前なので完了不定詞。"),
    ("It is said that the temple was built in the 8th century.", "The temple is said to have been built in the 8th century.", [], "was built は is said より前なので完了不定詞。受け身なので to have been built。"),
    ("It is said that he is the richest man in the city.", "He is said to be the richest man in the city.", [], "is と is said は同じ現在なので単純な不定詞。"),
    ("It appears that the dog has eaten the cake.", "The dog appears to have eaten the cake.", [], "has eaten（現在完了）は appears より前のできごとを表すので完了不定詞。"),
    ("It seems that you know a lot about birds.", "You seem to know a lot about birds.", [], "know と seems は同じ現在なので単純な不定詞。主語が You なので seem になる。"),
    ("It is believed that the painting was stolen in 1990.", "The painting is believed to have been stolen in 1990.", [], "was stolen は is believed より前なので完了不定詞。受け身なので to have been stolen。"),
    ("It seemed that Tom was nervous.", "Tom seemed to be nervous.", [], "was と seemed は同じ過去なので単純な不定詞。"),
    ("It is thought that the writer lived here as a child.", "The writer is thought to have lived here as a child.", [], "lived は is thought より前なので完了不定詞。"),
    ("It appears that she has known him for years.", "She appears to have known him for years.", [], "has known（継続の現在完了）は過去から続くことを表すので完了不定詞。"),
    ("It seems that the shop is closed today.", "The shop seems to be closed today.", [], "is closed と seems は同じ現在なので単純な不定詞。"),
]


@gen("standard_practice", 5, ["computation", "condition_check"])
def seem_rewrite(r):
    src, ans, v, why_s = r.choice(SEEM_RW)
    subj = ans.split(" seem")[0].split(" appear")[0].split(" is ")[0]
    return sa(f"次の英文を、{subj} を主語にしてほぼ同じ意味の英文に書きかえなさい。\n{src}", ans,
              f"{why_s} that 節の主語を文の主語にし、that 節の動詞を to 不定詞に変える。", d=3, v=v,
              ap="that 節の動詞の時と、述語動詞（seem / appear / be said など）の時を比べ、同じなら to＋原形、前なら to have＋過去分詞にする。",
              steps=[f"that 節の主語 {subj} を文の主語にする。", "述語動詞の形を主語に合わせる（It seems → He seems など）。", f"時の関係を判断する：{why_s}", f"答え：{ans}"],
              alt=["書きかえた文を It seems that ... の形に戻し、元の文と時制が一致するかを確かめる。"],
              pc=[("主語と述語動詞の形が正しい", 2), ("単純不定詞・完了不定詞を正しく使い分けている", 2)],
              pit=["that 節が過去形なのに to be を使う。", "述語動詞が過去（seemed）で、that 節も同じ過去なのに完了不定詞を使う。"])


# (元の文, 空所つきの文, 正答, [(誤答, 理由)], 説明)
GER_SUBJ = [
    ("I'm sure that he will pass the exam.", "I'm sure of (　　) the exam.", "his passing",
     [("passing", "意味上の主語がないと、文の主語 I が合格するという意味になる。"), ("him to pass", "前置詞 of の後ろに不定詞は置けない。"),
      ("he will pass", "前置詞 of の後ろに主語と動詞のそろった節をそのまま置くことはできない。")],
     "合格するのは he なので、動名詞の前に意味上の主語 his を置く。"),
    ("Do you mind if I open the window?", "Do you mind (　　) the window?", "my opening",
     [("opening", "意味上の主語がないと、相手が開けることになり「窓を開けてくれませんか」という依頼の意味になる。"), ("me to open", "mind は不定詞を目的語にとらない。"),
      ("my open", "所有格 my の後ろには名詞か動名詞が必要。open は動詞の原形。")],
     "開けるのは話し手（I）なので、動名詞の前に意味上の主語 my を置く（目的格 me も可）。"),
    ("She is proud that her son is a doctor.", "She is proud of (　　) a doctor.", "her son being",
     [("her son to be", "前置詞 of の後ろに不定詞は置けない。"), ("being", "意味上の主語がないと、文の主語 She が医者であるという意味になる。"),
      ("her son has been", "前置詞 of の後ろに主語と動詞のそろった節を置くことはできない。")],
     "医者であるのは her son なので、動名詞 being の前に意味上の主語を置く。"),
    ("He is ashamed that he was lazy.", "He is ashamed of (　　) lazy.", "having been",
     [("being", "単純な動名詞は述語動詞 is と同じ時を表し、「今怠け者であることを恥じている」になる。was（過去）のことは完了動名詞で表す。"),
      ("to have been", "前置詞 of の後ろに不定詞は置けない。"), ("have been", "前置詞 of の後ろに動詞の原形（have）は置けない。")],
     "怠けていたのは恥じている今より前のことなので、完了動名詞 having been を使う。主語は文の主語と同じなので意味上の主語は不要。"),
    ("I remember that I saw her at the station.", "I remember (　　) her at the station.", "seeing",
     [("to see", "remember to do は「（これから）忘れずに～する」の意味になる。"), ("see", "remember の後ろに動詞の原形は置けない。"),
      ("seen", "過去分詞は remember の目的語にならない。")],
     "remember doing は「（過去に）～したことを覚えている」。会ったのは主語 I なので意味上の主語は不要。"),
    ("My father insisted that I should go to college.", "My father insisted on (　　) to college.", "my going",
     [("going", "意味上の主語がないと、父自身が大学へ行くことを主張した意味になる。"), ("me to go", "前置詞 on の後ろに不定詞は置けない。"),
      ("I should go", "前置詞 on の後ろに主語と動詞のそろった節を置くことはできない。")],
     "大学へ行くのは I なので、動名詞の前に意味上の主語 my を置く。"),
    ("He is proud that his father was a famous actor.", "He is proud of (　　) a famous actor.", "his father having been",
     [("his father being", "単純な動名詞は is と同じ時（今）を表すので、was（過去）の内容と時がずれる。"),
      ("having been", "意味上の主語がないと、文の主語 He が俳優だったという意味になる。"),
      ("his father to have been", "前置詞 of の後ろに不定詞は置けない。")],
     "俳優だったのは his father で、しかも誇りに思っている今より前のことなので、意味上の主語＋完了動名詞にする。"),
    ("Do you mind if my sister joins us?", "Do you mind (　　) us?", "my sister joining",
     [("joining", "意味上の主語がないと、相手が加わる意味になる。"), ("my sister to join", "mind は不定詞を目的語にとらない。"),
      ("my sister joins", "mind の目的語には動名詞が必要。主語と動詞のそろった形をそのまま置くことはできない。")],
     "加わるのは my sister なので、動名詞 joining の前に意味上の主語を置く。"),
    ("I'm surprised that she has never been abroad.", "I'm surprised at (　　) abroad.", "her never having been",
     [("never having been", "意味上の主語がないと、文の主語 I が海外に行ったことがないという意味になる。"),
      ("her never to have been", "前置詞 at の後ろに不定詞は置けない。"), ("she has never been", "前置詞 at の後ろに主語と動詞のそろった節を置くことはできない。")],
     "海外に行ったことがないのは she で、今までの経験（現在完了）なので、意味上の主語＋完了動名詞にする。否定語 never は動名詞の直前に置く。"),
    ("I don't like it when people talk loudly on the train.", "I don't like (　　) loudly on the train.", "people talking",
     [("talking", "意味上の主語がないと、自分が話すのが好きではないという意味になる。"), ("people talk", "like の目的語に主語と動詞のそろった形をそのまま置くことはできない。"),
      ("people's talk", "talk を名詞にすると、副詞 loudly で修飾できない。")],
     "話すのは people なので、動名詞 talking の前に意味上の主語（目的格の名詞）を置く。"),
    ("Do you remember that I told you this before?", "Do you remember (　　) you this before?", "my telling",
     [("telling", "意味上の主語がないと、相手（you）自身が話したことになり、目的語の you とも合わない。"),
      ("me to tell", "remember は「O に～してもらうことを覚えている」の意味で O＋to 不定詞をとらない。"),
      ("to tell", "remember to do は「（これから）忘れずに～する」の意味になり、before（以前）と合わない。")],
     "話したのは話し手（I）なので、動名詞 telling の前に意味上の主語 my を置く（目的格 me も可）。"),
]


@gen("standard_practice", 5, ["concept", "condition_check"])
def gerund_subject(r):
    a, b, ok, wrongs, why_s = r.choice(GER_SUBJ)
    return mc(f"2つの英文がほぼ同じ意味になるように、（　）に入る最も適切なものを選びなさい。\n{a}\n{b}", [ok] + [w for w, _ in wrongs],
              f"{ok} が入る。{why_s}", d=3,
              ap="that 節（if 節）の主語が文の主語と同じか違うか、that 節の動詞の時が述語動詞と同じか前かの2点を確認する。",
              steps=["前置詞・動詞の後ろなので、動名詞を使うことを確認する。", "動作をする人が文の主語と違えば、所有格・目的格で意味上の主語を示す。",
                     "時が述語動詞より前なら having＋過去分詞にする。", f"答え：{ok}"],
              alt=["選んだ形を that 節の文に戻して、元の文と主語・時制が一致するかを確かめる。"],
              pc=[("意味上の主語の有無を正しく判断している", 2), ("動名詞の形（単純・完了）を正しく選んでいる", 2)],
              pit=["意味上の主語を省いて、文の主語の動作にしてしまう。", "前置詞の後ろに不定詞や節を置く。"],
              why={w: (reason, "動名詞の意味上の主語・時の扱いの誤り") for w, reason in wrongs})


ORDERS = [
    ("この箱は重すぎて私には運べない。", ["this box", "is", "too", "heavy", "for me", "to carry"], "too ～ for 人 to do「～すぎて（人は）…できない」。主語 this box が carry の目的語にあたるので、文末に it は置かない。"),
    ("彼は若いころ有名な選手だったようだ。", ["he", "seems", "to have been", "a famous player", "in his youth"], "述語動詞 seems より前のことなので完了不定詞 to have been。"),
    ("またお会いできるのを楽しみにしています。", ["I'm", "looking forward", "to", "seeing", "you", "again"], "look forward to の to は前置詞なので動名詞 seeing が続く。"),
    ("傘を持ってきてくれるとは、あなたは親切ですね。", ["it", "is", "kind", "of you", "to bring", "me an umbrella"], "kind は人の性質の評価なので of you。"),
    ("私は早起きには慣れている。", ["I", "am", "used", "to", "getting up", "early"], "be used to の to は前置詞なので動名詞 getting up が続く。"),
    ("その川は子どもが泳ぐには危険だ。", ["the river", "is", "dangerous", "for children", "to swim", "in"], "意味上の主語 for children。主語 the river は swim in の目的語にあたるので、文末に in が残る。"),
    ("母は私が一人で海外に行くことに反対している。", ["my mother", "objects", "to", "my", "going abroad", "alone"], "object to の to は前置詞。行くのは私なので意味上の主語 my を置く。"),
    ("彼女はその知らせを聞いて泣かずにはいられなかった。", ["she", "couldn't", "help", "crying", "at", "the news"], "cannot help doing「～せずにはいられない」。"),
    ("この本は何度も読む価値がある。", ["this book", "is", "worth", "reading", "many", "times"], "be worth doing「～する価値がある」。"),
    ("彼は一人で旅行できるほど十分に年をとっている。", ["he", "is", "old", "enough", "to travel", "alone"], "形容詞＋enough to do「…できるほど十分～」。enough は形容詞の後ろに置く。"),
    ("私が窓を開けてもかまいませんか。", ["do", "you", "mind", "my", "opening", "the window"], "開けるのは私なので、動名詞 opening の前に意味上の主語 my を置く。"),
    ("彼女は何も言わずに部屋を出て行った。", ["she", "left", "the room", "without", "saying", "anything"], "前置詞 without の後ろは動名詞。"),
]


@gen("standard_practice", 5, ["application", "computation"])
def build_order(r):
    jp, parts, point = r.choice(ORDERS)
    sent = " ".join(parts)
    sent = sent[0].upper() + sent[1:] + ("?" if parts[0] == "do" else ".")
    return order(f"日本語に合うように、語句を並べかえて英文を完成させなさい。ただし、文頭にくる語も小文字で示してある。\n{jp}", parts,
                 f"{sent}　{point}", d=3, p=4,
                 ap="主語と述語動詞を先に決め、不定詞・動名詞のまとまりと、その意味上の主語（for 人・所有格）の位置を考える。",
                 steps=["主語と述語動詞を決める。", "不定詞・動名詞を使う部分と、意味上の主語の位置を決める。", f"ポイント：{point}", f"完成文：{sent}"],
                 alt=["完成した英文を和訳し直して、日本語と一致するかを確かめる。"],
                 pc=[("主語・述語動詞の語順が正しい", 2), ("不定詞・動名詞とその意味上の主語の位置が正しい", 2)],
                 pit=["前置詞の to の後ろに動詞の原形を置く。", "意味上の主語（for 人／所有格）の位置を誤る。"])


def _prep(w):
    return (w, "前置詞の後ろに動詞の原形を置くことはできない。")


# (英文, 和訳, 正答, [(誤答, 理由)], 規則)
IDIOM = [
    ("I'm looking forward to (　　) from you.", "お便りを楽しみにしています。", "hearing",
     [_prep("hear"), ("heard", "過去形・過去分詞では「～すること」という名詞の働きにならない。"), ("hears", "三人称単数現在形は述語動詞の形で、前置詞の目的語にならない。")],
     "look forward to doing「～するのを楽しみに待つ」。to は前置詞"),
    ("She is used to (　　) in front of many people.", "彼女は大勢の前で話すことに慣れている。", "speaking",
     [_prep("speak"), ("spoken", "過去分詞では「～すること」という名詞の働きにならない。"), ("spoke", "過去形は述語動詞の形で、前置詞の目的語にならない。")],
     "be used to doing「～することに慣れている」。to は前置詞（used to do「以前は～した」とは別の表現）"),
    ("When it comes to (　　) Italian food, Ken is the best in our class.", "イタリア料理を作ることにかけては、ケンがクラスでいちばんだ。", "cooking",
     [_prep("cook"), ("cooked", "過去形・過去分詞では「～すること」という名詞の働きにならない。"), ("cooks", "三人称単数現在形は前置詞の目的語にならない。")],
     "when it comes to doing「～することになると・～することにかけては」。to は前置詞"),
    ("What do you say to (　　) a break?", "ひと休みするのはどうですか。", "taking",
     [_prep("take"), ("taken", "過去分詞では「～すること」という名詞の働きにならない。"), ("took", "過去形は前置詞の目的語にならない。")],
     "What do you say to doing?「～するのはどうですか」。to は前置詞"),
    ("My grandfather objected to (　　) the old house.", "祖父はその古い家を売ることに反対した。", "selling",
     [_prep("sell"), ("sold", "過去形・過去分詞では「～すること」という名詞の働きにならない。"), ("sells", "三人称単数現在形は前置詞の目的語にならない。")],
     "object to doing「～することに反対する」。to は前置詞"),
    ("It is no use (　　) over spilt milk.", "こぼれたミルクを嘆いてもむだだ（覆水盆に返らず）。", "crying",
     [("to crying", "It is no use の後ろに前置詞 to は不要。動名詞を直接続ける。"), ("cry", "It is no use の後ろに動詞の原形は置けない。"), ("cried", "過去形・過去分詞では「～すること」の意味にならない。")],
     "It is no use doing「～してもむだだ」"),
    ("This movie is worth (　　) twice.", "この映画は2回見る価値がある。", "seeing",
     [("to see", "worth は前置詞と同じように名詞・動名詞を後ろにとり、不定詞はとらない。"), ("see", "worth の後ろに動詞の原形は置けない。"), ("seen", "過去分詞では「～すること」の意味にならない。")],
     "be worth doing「～する価値がある」"),
    ("I couldn't help (　　) when I heard the joke.", "その冗談を聞いて、笑わずにはいられなかった。", "laughing",
     [("to laugh", "cannot help doing の形で「～せずにはいられない」。この help は不定詞をとらない。"), ("laugh", "help の後ろに原形を置くと「笑うのを手伝う」の意味になり、文が成り立たない。"), ("laughed", "過去形・過去分詞は help の目的語にならない。")],
     "cannot help doing「～せずにはいられない」"),
    ("I don't feel like (　　) out tonight.", "今夜は出かける気がしない。", "going",
     [_prep("go"), ("to go", "feel like の like は前置詞なので、不定詞は続かない。"), ("gone", "過去分詞では「～すること」の意味にならない。")],
     "feel like doing「～したい気がする」。like は前置詞"),
    ("There is no (　　) what will happen tomorrow.", "明日何が起こるかはわからない。", "knowing",
     [("to know", "There is no doing の形で「～することはできない」。no の後ろに不定詞は置けない。"), ("know", "no の後ろに動詞の原形は置けない。"), ("known", "過去分詞では「～すること」の意味にならない。")],
     "There is no doing「～することはできない」"),
    ("On (　　) the news, she ran out of the room.", "その知らせを聞くとすぐ、彼女は部屋から駆け出した。", "hearing",
     [_prep("hear"), ("to hear", "前置詞 on の後ろに不定詞は置けない。"), ("heard", "過去形・過去分詞は前置詞の目的語にならない。")],
     "on doing「～するとすぐに」。on は前置詞"),
    ("It goes without (　　) that health is more important than money.", "健康がお金より大切なのは言うまでもない。", "saying",
     [_prep("say"), ("to say", "前置詞 without の後ろに不定詞は置けない。"), ("said", "過去形・過去分詞は前置詞の目的語にならない。")],
     "It goes without saying that ...「…は言うまでもない」"),
    ("He devoted his life to (　　) poor children.", "彼は貧しい子どもたちを助けることに生涯をささげた。", "helping",
     [_prep("help"), ("helped", "過去形・過去分詞では「～すること」の意味にならない。"), ("helps", "三人称単数現在形は前置詞の目的語にならない。")],
     "devote A to doing「A を～することにささげる」。to は前置詞"),
]


@gen("standard_practice", 5, ["condition_check", "common_error"])
def gerund_idiom(r):
    s, jp, ok, wrongs, rule = r.choice(IDIOM)
    return form_mc(s, jp, ok, wrongs, f"{ok} が入る。{rule}。", d=2,
                   ap="空所の前が前置詞（look forward to の to など）か、動名詞をとる決まった表現かを確認する。",
                   steps=["空所の前の語句が、前置詞や動名詞をとる慣用表現かを確認する。", f"{rule}。", f"答え：{ok}"],
                   alt=["空所に名詞（the news, the party など）を入れてみて文が成り立つなら、その to は前置詞であり、動詞なら動名詞にすると確かめる。"],
                   pit=["look forward to / be used to の to を不定詞の to と考え、原形を続ける。"],
                   mis="前置詞の to と不定詞の to の混同", pc=[("前置詞・慣用表現であることに気づいている", 2), ("正しい形を選んでいる", 2)])


# ======================================================================
# C 思考力・記述応用
# ======================================================================

PAIRS = [
    ("I remember locking the door.", "Remember to lock the door.",
     "Aは remember doing で「ドアに鍵をかけたことを覚えている」。鍵をかけたのは過去のこと。Bは remember to do で「忘れずにドアに鍵をかけなさい」。鍵をかけるのはこれからのこと。動名詞はすでに行ったこと、不定詞はこれから行うことを表す。"),
    ("He stopped smoking.", "He stopped to smoke.",
     "Aは stop の目的語が動名詞 smoking で「彼はたばこを吸うのをやめた」。Bの to smoke は stop の目的語ではなく目的を表す副詞的用法で「彼はたばこを吸うために立ち止まった（手を止めた）」。"),
    ("I'll never forget meeting her.", "Don't forget to meet her at the station.",
     "Aは forget doing で「彼女に会ったことを決して忘れないだろう」。会ったのは過去のこと。Bは forget to do で「駅で彼女と会うのを忘れないで」。会うのはこれからのこと。"),
    ("I regret telling him the news.", "I regret to tell you the news.",
     "Aは regret doing で「彼にその知らせを話したことを後悔している」。話したのは過去のこと。Bは regret to do で「残念ながらあなたにその知らせを伝えなければならない」。伝えるのはこれからのこと。"),
    ("She tried to open the window.", "She tried opening the window.",
     "Aは try to do で「彼女は窓を開けようと努めた」。実際に開いたかどうかはわからない。Bは try doing で「彼女は試しに窓を開けてみた」。実際に開けて、その結果を確かめたという意味になる。"),
    ("He seems to be rich.", "He seems to have been rich.",
     "Aは単純不定詞で、seems と同じ今のことを表し「彼は（今）金持ちのようだ」（＝It seems that he is rich.）。Bは完了不定詞で、seems より前のことを表し「彼は（以前）金持ちだったようだ」（＝It seems that he was rich.）。"),
    ("It is kind of you to help me.", "It is easy for you to help me.",
     "Aは kind が人の性質を評価する形容詞なので of you で、「手伝ってくれるとは、あなたは親切だ」（You are kind. が成り立つ）。Bは easy が行為を評価する形容詞なので for you で、「あなたにとって私を手伝うのは簡単だ」（You are easy. は同じ意味では成り立たない）。"),
    ("I'm sure of passing the exam.", "I'm sure of his passing the exam.",
     "Aは動名詞の意味上の主語がないので、文の主語 I が合格する意味で「私は（自分が）試験に合格すると確信している」。Bは意味上の主語 his があるので「私は彼が試験に合格すると確信している」。"),
    ("He went on talking about his trip.", "He went on to talk about his trip.",
     "Aは go on doing で「彼は旅行の話をし続けた」（同じ話を続けた）。Bは go on to do で「彼は（別の話を終えて）続けて旅行の話をした」（話題を次に移した）。"),
    ("I don't mind opening the window.", "I don't mind your opening the window.",
     "Aは意味上の主語がないので、文の主語 I が開けることになり「私は窓を開けてもかまわない」。Bは意味上の主語 your があるので「あなたが窓を開けてもかまわない」。"),
]


@gen("thinking_writing", 4, ["written_reasoning", "concept"])
def explain_difference(r):
    a, b, model = r.choice(PAIRS)
    return desc(f"次の2つの英文A・Bの意味の違いを、不定詞・動名詞の形や意味上の主語に触れながら日本語で説明しなさい。\nA：{a}\nB：{b}", model,
                "不定詞・動名詞の形、完了形かどうか、意味上の主語の有無によって、「いつのことか」「だれがするのか」が変わる。",
                [("Aの形とその働きを正しく説明している", 3), ("Bの形とその働きを正しく説明している", 3), ("A・Bの和訳がそれぞれ正しい", 2)], d=4, p=8, lines=6,
                ap="2つの文で違う部分（不定詞か動名詞か、完了形か、意味上の主語の有無）に下線を引き、その違いが「時」と「動作をする人」のどちらに関わるかを考える。",
                steps=["A・Bで形の違う部分を特定する。", "それぞれの形が表す意味（これから・すでに、同じ時・前の時、だれの動作か）を確認する。", "和訳を示しながら違いを説明する。"],
                alt=["それぞれの文を that 節や別の表現に書きかえて違いを示す方法もある（例：remember doing → remember that I did）。"],
                pc=[("Aの説明", 3), ("Bの説明", 3), ("和訳", 2)],
                pit=["和訳だけを書き、形の違いという根拠を示さない。", "stop to do の to do を stop の目的語と考える。"])


# (英文, 答え, 説明)
TIME_X = [
    ("He seems to have been a teacher.", "It seems that he was a teacher.（It seems that he has been a teacher. も可）",
     "完了不定詞 to have been は述語動詞 seems（現在）より前の時を表すので、that 節は過去形（または現在完了）になる。"),
    ("She seemed to be tired.", "It seemed that she was tired.",
     "単純不定詞 to be は述語動詞 seemed（過去）と同じ時を表すので、that 節も同じ過去形 was になる。"),
    ("They seemed to have finished the work.", "It seemed that they had finished the work.",
     "完了不定詞は述語動詞 seemed（過去）よりさらに前の時を表すので、that 節は過去完了 had finished になる。"),
    ("He seems to know the answer.", "It seems that he knows the answer.",
     "単純不定詞 to know は述語動詞 seems（現在）と同じ時を表すので、that 節は現在形 knows になる。"),
    ("The boy seemed to have seen a ghost.", "It seemed that the boy had seen a ghost.",
     "完了不定詞は述語動詞 seemed（過去）より前の時を表すので、that 節は過去完了 had seen になる。"),
    ("You seem to have lost weight.", "It seems that you have lost weight.（It seems that you lost weight. も可）",
     "完了不定詞は述語動詞 seem（現在）より前の時を表す。今に結果が残っているので現在完了が自然だが、過去形も可。"),
    ("She appears to have been sick for a week.", "It appears that she has been sick for a week.",
     "完了不定詞は appears（現在）より前から続く状態を表す。for a week（1週間）があるので、that 節は継続の現在完了 has been になる。"),
    ("The old man appeared to be lonely.", "It appeared that the old man was lonely.",
     "単純不定詞 to be は述語動詞 appeared（過去）と同じ時を表すので、that 節も過去形 was になる。"),
]


@gen("thinking_writing", 3, ["cross_unit", "written_reasoning"], rel=["HS-ENG-U02"])
def time_relation(r):
    s, ans, why_s = r.choice(TIME_X)
    return desc(f"次の英文を It で始まるほぼ同じ意味の英文に書きかえなさい。また、述語動詞と不定詞が表す時の関係を、時制の知識を使って説明しなさい。\n{s}",
                f"{ans}　{why_s}", f"単純不定詞は述語動詞と同じ時、完了不定詞は述語動詞より前の時を表す。that 節では、それを時制（現在・過去・現在完了・過去完了）で表し分ける。{why_s}",
                [("It ～ that ... の文を正しく書いている", 3), ("that 節の時制を正しく選んでいる", 3), ("述語動詞と不定詞の時の関係を説明している", 2)], d=4, p=8, lines=5,
                ap="まず述語動詞（seem / appear）の時制を確認し、不定詞が単純形か完了形かで、that 節の動詞がそれと同じ時か前の時かを決める。",
                steps=["述語動詞の時制（現在か過去か）を確認する。", "不定詞が単純形なら同じ時、完了形なら前の時と判断する。",
                       "that 節の動詞の時制を決める（現在より前→過去・現在完了、過去より前→過去完了）。", f"答え：{ans}"],
                alt=["書きかえた文から、もう一度不定詞を使った文に戻してみて、元の文と一致するかを確かめる。"],
                pc=[("It ～ that ... の形", 3), ("that 節の時制", 3), ("時の関係の説明", 2)],
                pit=["seemed to have done を It seemed that ... did（過去形）としてしまう。", "seemed to be を It seemed that ... had been としてしまう。"])


# (元の文, 答え, 説明)
GER_RW = [
    ("I'm sure that he will succeed.", "I'm sure of his succeeding.",
     "成功するのは he で文の主語 I と異なるので、意味上の主語 his を置く。will succeed はこれからのことで、単純な動名詞で表せる。"),
    ("She is proud that her father was a pilot.", "She is proud of her father having been a pilot.",
     "パイロットだったのは her father なので意味上の主語を置く。was は is proud より前の時なので完了動名詞 having been にする。"),
    ("He is ashamed that he cheated on the test.", "He is ashamed of having cheated on the test.",
     "不正をしたのは文の主語 he 自身なので意味上の主語は不要。cheated は is ashamed より前の時なので完了動名詞にする。"),
    ("I'm sorry that I am late.", "I'm sorry for being late.",
     "遅れているのは文の主語 I 自身なので意味上の主語は不要。am late は am sorry と同じ時なので単純な動名詞 being にする。"),
    ("Do you mind if I use your pen?", "Do you mind my using your pen?（Do you mind me using your pen? も可）",
     "使うのは話し手 I で、文の主語 you と異なるので意味上の主語 my（または me）を置く。"),
    ("I'm afraid that I will make mistakes.", "I'm afraid of making mistakes.",
     "まちがえるのは文の主語 I 自身なので意味上の主語は不要。これからのことなので単純な動名詞 making にする。"),
    ("She insisted that I should stay for dinner.", "She insisted on my staying for dinner.（She insisted on me staying for dinner. も可）",
     "残るのは I で、文の主語 she と異なるので意味上の主語 my（または me）を置く。"),
]


@gen("thinking_writing", 3, ["written_reasoning", "condition_check"])
def gerund_rewrite(r):
    s, ans, why_s = r.choice(GER_RW)
    return desc(f"次の英文を、動名詞を使ってほぼ同じ意味の英文に書きかえなさい。また、意味上の主語と時の扱いについて、書きかえの根拠を説明しなさい。\n{s}",
                f"{ans}　{why_s}", f"that 節（if 節）を動名詞句にするときは、①主語が文の主語と同じかどうか（意味上の主語の要否）、②時が述語動詞と同じか前か（単純形か完了形か）を判断する。{why_s}",
                [("動名詞を使った英文を正しく書いている（前置詞を含む）", 4), ("意味上の主語の要否を説明している", 2), ("時の扱い（単純形・完了形）を説明している", 2)], d=4, p=8, lines=5,
                ap="形容詞や動詞の後ろに続く前置詞（sure of / proud of / insist on など）を補い、その後ろに動名詞を置く。主語と時の2点をチェックする。",
                steps=["形容詞・動詞に続く前置詞を確認する（be sure of, be proud of, insist on など）。", "that 節の主語が文の主語と違えば、所有格（または目的格）で意味上の主語を示す。",
                       "that 節の時が述語動詞より前なら having＋過去分詞にする。", f"答え：{ans}"],
                alt=["書きかえた文を that 節の文に戻し、主語と時制が元の文と一致するかを確かめる。"],
                pc=[("動名詞を使った英文", 4), ("意味上の主語の説明", 2), ("時の扱いの説明", 2)],
                pit=["前置詞を落とす（be proud her father ...）。", "意味上の主語を省いて、文の主語の動作にしてしまう。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(task, wrong, step, etype, tempt, fix, ans, expl, steps, ap, alt, pit, d=3):
    return desc(f"{task}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい英文に書き直しなさい。", ans, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい英文に直している", 3), ("文法の規則を説明している", 1)], d=d, p=6, lines=5,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい英文", 3), ("規則の説明", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix))


# (和文, 誤答, 正答, 誤りの箇所, 種類, 規則, 誤りやすい理由)
FORM_ERR = [
    ("私は友達とテニスをして楽しんだ。", "I enjoyed to play tennis with my friends.", "I enjoyed playing tennis with my friends.", "enjoyed to play", "concept",
     "enjoy は目的語に動名詞だけをとる。", "like to play と同じように to 不定詞が使えると考えた。"),
    ("彼女は留学することに決めた。", "She decided studying abroad.", "She decided to study abroad.", "decided studying", "concept",
     "decide は目的語に to 不定詞だけをとる。", "「～すること」を動名詞で表せばよいと考え、動詞ごとの語法を確かめなかった。"),
    ("またお会いできるのを楽しみにしています。", "I'm looking forward to see you again.", "I'm looking forward to seeing you again.", "to see", "concept",
     "look forward to の to は前置詞なので、後ろは動名詞。", "to を不定詞の to と考え、原形を続けた。"),
    ("窓を閉めていただけませんか。", "Would you mind to close the window?", "Would you mind closing the window?", "mind to close", "concept",
     "mind は目的語に動名詞だけをとる。", "「～していただけませんか」を Would you like to ～? と同じ形で考えた。"),
    ("あんなことを言うなんて、彼は不注意だった。", "It was careless for him to say such a thing.", "It was careless of him to say such a thing.", "for him", "condition",
     "careless は人の性質を評価する形容詞なので、意味上の主語は of で示す。", "意味上の主語はいつも for で示すと覚えていた。"),
    ("私は朝早く起きることに慣れている。", "I'm used to get up early in the morning.", "I'm used to getting up early in the morning.", "to get up", "concept",
     "be used to の to は前置詞なので、後ろは動名詞。", "used to do（以前は～したものだ）と混同した。"),
    ("この問題は難しすぎて私には解けない。", "This problem is too difficult for me to solve it.", "This problem is too difficult for me to solve.", "solve it", "logic",
     "主語 this problem が solve の目的語にあたるので、目的語 it を重ねて置かない。", "solve は他動詞なので目的語が必要だと考え、it を補った。"),
    ("私は彼に会うのを避けた。", "I avoided to meet him.", "I avoided meeting him.", "avoided to meet", "concept",
     "avoid は目的語に動名詞だけをとる。", "「～するのを」を to 不定詞で表した。"),
    ("彼は試験に合格すると思っている。", "He expects passing the exam.", "He expects to pass the exam.", "expects passing", "concept",
     "expect は目的語に to 不定詞をとる（これから起こることを予期する）。", "「合格すること」を動名詞で表した。"),
    ("この映画は見る価値がある。", "This movie is worth to see.", "This movie is worth seeing.", "worth to see", "concept",
     "be worth の後ろは動名詞（または名詞）。", "「～する価値」を不定詞の形容詞的用法で表そうとした。"),
]


@gen("error_correction", 4, ["common_error", "condition_check"])
def err_form(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(FORM_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", etype, tempt, fix, fix,
                    f"{rule}正しくは {fix}",
                    [f"規則を確認する：{rule}", f"「{where}」の部分を直す。", f"正しい英文：{fix}"],
                    "動詞・形容詞・前置詞ごとに、後ろに続く形（不定詞か動名詞か、for か of か）が決まっている。日本語の「～すること」だけで形を決めない。",
                    ["直した英文の動詞・前置詞の語法を、授業プリントの一覧（不定詞だけをとる動詞・動名詞だけをとる動詞・前置詞の to）と照合する。"],
                    ["動名詞をとる動詞に to 不定詞を続ける。", "前置詞の to の後ろに原形を置く。"], d=3)


# (和文, 誤答, 正答, 誤りの箇所, 規則, 誤りやすい理由)
PERF_ERR = [
    ("彼は昨日具合が悪かったようだ。", "He seems to be sick yesterday.", "He seems to have been sick yesterday.", "to be",
     "yesterday のことは述語動詞 seems（現在）より前なので、完了不定詞 to have been を使う（＝It seems that he was sick yesterday.）。", "「～ようだ」の seem に注目して、不定詞が表す時を確かめなかった。"),
    ("その寺は千年前に建てられたと言われている。", "The temple is said to be built a thousand years ago.", "The temple is said to have been built a thousand years ago.", "to be built",
     "a thousand years ago のことは述語動詞 is said より前なので、完了不定詞の受け身 to have been built を使う。", "受け身の不定詞 to be built にすることに気をとられ、時のずれを見落とした。"),
    ("彼女は今は幸せそうだ。", "She seems to have been happy now.", "She seems to be happy now.", "to have been",
     "now は述語動詞 seems と同じ時なので、単純な不定詞 to be を使う。", "「幸せそうだ」を過去のことのように考え、完了不定詞を使った。"),
    ("彼らはすでに道に迷ってしまったようだった。", "They seemed to lose their way already.", "They seemed to have lost their way already.", "to lose",
     "道に迷ったのは seemed（過去）よりさらに前のことなので、完了不定詞 to have lost を使う（＝It seemed that they had lost their way already.）。", "seemed が過去形なので、それで「過去」は表せていると考えた。"),
    ("その画家は若いころパリに住んでいたと考えられている。", "The painter is thought to live in Paris in his youth.", "The painter is thought to have lived in Paris in his youth.", "to live",
     "in his youth（若いころ）のことは is thought より前なので、完了不定詞 to have lived を使う。", "is thought が現在形なので、不定詞も同じ時でよいと考えた。"),
    ("彼女は以前その歌手に会ったことがあるようだ。", "She seems to meet the singer before.", "She seems to have met the singer before.", "to meet",
     "経験（現在完了）の内容は seems より前の時なので、完了不定詞 to have met を使う（＝It seems that she has met the singer before.）。", "「会ったことがある」を不定詞でどう表すかがわからず、原形を使った。"),
    ("犯人は裏口から逃げたようだ。", "The criminal appears to escape through the back door.", "The criminal appears to have escaped through the back door.", "to escape",
     "逃げたのは appears（現在）より前のことなので、完了不定詞 to have escaped を使う。", "和文の「逃げた」の過去の意味を、不定詞の形に反映させなかった。"),
]


@gen("error_correction", 3, ["common_error", "computation"])
def err_perfect(r):
    jp, wrong, fix, where, rule, tempt = r.choice(PERF_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"不定詞「{where}」", "concept", tempt, fix, fix, rule,
                    ["述語動詞の時（現在か過去か）を確認する。", "不定詞が表す内容が、述語動詞と同じ時か前の時かを判断する。", f"正しい英文：{fix}"],
                    "不定詞の内容が述語動詞より前の時なら完了不定詞、同じ時なら単純不定詞を使う。It seems that ... に書きかえると時の関係がはっきりする。",
                    ["直した英文を It seems that ... の形に書きかえ、that 節の時制が和文の時と合うかを確かめる。"],
                    ["過去を表す語句があるのに単純な不定詞を使う。", "現在のことに完了不定詞を使う。"], d=3)


# (和文, 誤答, 正答, 誤りの箇所, 規則, 誤りやすい理由)
MEAN_ERR = [
    ("私は子どものころ京都を訪れたことを覚えている。", "I remember to visit Kyoto when I was a child.", "I remember visiting Kyoto when I was a child.", "to visit",
     "過去にしたことを覚えているときは remember doing。remember to do は「忘れずに～する」。", "「覚えている」の目的語を不定詞で表した。"),
    ("出かける前に忘れずに戸締まりをしなさい。", "Don't forget locking the door before you go out.", "Don't forget to lock the door before you go out.", "locking",
     "これから行うことを忘れないようにと言うときは forget to do。forget doing は「～したことを忘れる」。", "「戸締まりをすること」を動名詞で表した。"),
    ("健康のために彼はたばこをやめた。", "He stopped to smoke for his health.", "He stopped smoking for his health.", "to smoke",
     "「～するのをやめる」は stop doing。stop to do は「～するために立ち止まる」で、目的を表す副詞的用法。", "「やめた」の目的語を不定詞で表した。"),
    ("昨日彼女に秘密を話したことを後悔している。", "I regret to tell her the secret yesterday.", "I regret telling her the secret yesterday.", "to tell",
     "過去にしたことを後悔するときは regret doing（regret having told も可）。regret to do は「残念ながら～する」。", "「話したこと」を不定詞で表した。"),
    ("明日この手紙を忘れずに出してね。", "Remember posting this letter tomorrow.", "Remember to post this letter tomorrow.", "posting",
     "これから行うことを忘れずにするときは remember to do。remember doing は「～したことを覚えている」。", "「出すこと」を動名詞で表した。"),
    ("彼女は帰り道に花を買うために立ち止まった。", "She stopped buying flowers on her way home.", "She stopped to buy flowers on her way home.", "buying",
     "「～するために立ち止まる」は stop to do（目的を表す副詞的用法）。stop doing は「～するのをやめる」。", "「花を買う」を stop の目的語と考え、動名詞にした。"),
]


@gen("error_correction", 3, ["common_error", "concept"])
def err_meaning(r):
    jp, wrong, fix, where, rule, tempt = r.choice(MEAN_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", "interpretation", tempt, fix, fix, rule,
                    ["動詞が、不定詞と動名詞で意味が変わる動詞であることを確認する。", "和文の動作が「これから」か「すでに」か（stop は目的か、やめる対象か）を判断する。", f"正しい英文：{fix}"],
                    "remember / forget / regret / stop は、不定詞と動名詞で意味が変わる。和文の動作がいつのことかを先に確かめる。",
                    ["直した英文を和訳し直し、和文と意味が一致するか、反対の形にすると意味がどう変わるかを確かめる。"],
                    ["「～すること」を機械的に動名詞（または不定詞）にする。"], d=3)


GENERATORS = [verb_object_form, for_or_of, perfect_infinitive, meaning_change,
              seem_rewrite, gerund_subject, build_order, gerund_idiom,
              explain_difference, time_relation, gerund_rewrite,
              err_form, err_perfect, err_meaning]
