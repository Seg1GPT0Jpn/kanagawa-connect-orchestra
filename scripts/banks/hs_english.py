"""フェーズ3：高校英語（英語コミュニケーションⅠ・論理・表現Ⅰ）自習プリント 10単元（各6問）。"""
from ._common import desc, mc, order, sa, stim, unit_set

PHASE = 3
Q = "（　）に入る最も適切なものを選びなさい。\n"
O = "日本語に合うように、語句を並べかえなさい。ただし、文頭にくる語も小文字で示してある。\n"
W = ["writing", "grammar"]
R = ["reading"]


def U(unit_id, items, **kw):
    return unit_set(unit_id, items, track="high_school", out=f"data/high_school/english/{unit_id.lower()}.json", **kw)


SETS = [
    U("HS-ENG-U01", [
        mc(Q + "The news made her (　　).", ["happy", "happily", "happiness", "to happy"], "make O C（O を C にする）。C には形容詞が入る。", d=1),
        mc(Q + "Please (　　) the matter with your parents before you decide.", ["discuss", "discuss about", "discuss on", "discuss with about"],
           "discuss は他動詞なので前置詞をつけずに目的語をとる。", d=2),
        mc(Q + "She (　　) on the sofa and fell asleep.", ["lay", "laid", "lain", "layed"], "自動詞 lie（横になる）の過去形は lay。他動詞 lay（横たえる）の過去形 laid と区別する。", d=3),
        mc("次の英文と同じ文型の文を選びなさい。\nMy uncle bought me a watch.", ["She showed us the way.", "He became a doctor.", "They found the box empty.", "I walked to school."],
           "問題文は SVOO。She showed us the way. も SVOO。became a doctor は SVC、found the box empty は SVOC、walked は SV。", d=2),
        mc(Q + "We should (　　) the problem seriously.", ["consider", "consider about", "think", "talk"], "consider は他動詞。think・talk は about が必要。", d=2),
        sa("次の英文を、下線部に注意して日本語に訳しなさい。\nI found [[u:the book easy]].", "私はその本が簡単だとわかった。", "SVOC の文で、O＝the book、C＝easy。「O が C だとわかる」。", d=3, k=["translation", "grammar"],
           v=["その本は簡単だとわかった。", "私はその本が易しいとわかった。"]),
    ]),
    U("HS-ENG-U02", [
        mc(Q + "I (　　) to the library when I met Ken.", ["was going", "have gone", "go", "had gone"], "過去のある時点で進行中だった動作は過去進行形。", d=1),
        mc(Q + "By the time we arrived, the movie (　　).", ["had already started", "has already started", "already starts", "will already start"],
           "過去のある時点（arrived）より前に完了していたことは過去完了。", d=2),
        mc(Q + "I'll call you when I (　　) home.", ["get", "will get", "got", "am getting"], "時・条件を表す副詞節の中では、未来のことも現在形で表す。", d=2),
        mc(Q + "She (　　) English for five years by next March.", ["will have studied", "has studied", "studies", "had studied"], "未来のある時点までの継続は未来完了。", d=3),
        mc(Q + "It (　　) since last night.", ["has been raining", "is raining", "was raining", "rains"], "過去から現在まで続いている動作は現在完了進行形。", d=2),
        mc("次の英文の誤りを含む部分を選びなさい。\nI have visited Kyoto last year.", ["have visited", "Kyoto", "last", "year"],
           "last year のように過去の一時点を示す語句は現在完了と一緒に使えない。正しくは I visited Kyoto last year.", d=3, k=["grammar", "thinking"], keep=True),
    ]),
    U("HS-ENG-U03", [
        mc(Q + "He (　　) be at home. I saw him at the station a minute ago.", ["can't", "must", "should", "may"], "駅で見たばかりなので「家にいるはずがない」。can't は強い否定の推量。", d=2),
        mc(Q + "You (　　) have told me earlier. I could have helped you.", ["should", "must", "can't", "need"], "should have＋過去分詞で「～すべきだったのに（しなかった）」。", d=2),
        mc(Q + "She (　　) have left already. Her coat is gone.", ["must", "can't", "need not", "should not"], "must have＋過去分詞で「～したにちがいない」。", d=2),
        mc(Q + "I (　　) to play tennis every weekend when I was a student.", ["used", "would", "use", "was used"], "used to＋動詞の原形で「（以前は）よく～したものだ」。", d=2),
        mc(Q + "You (　　) not come if you don't want to.", ["need", "must", "should", "ought"], "need not＋動詞の原形で「～する必要はない」。", d=3),
        mc("次の英文の意味として最も適切なものを選びなさい。\nYou may well be surprised.", ["あなたが驚くのももっともだ。", "あなたは驚くかもしれない。", "あなたは驚いてもよい。", "あなたは驚かないほうがよい。"],
           "may well＋動詞の原形は「～するのももっともだ」「たぶん～だろう」。", d=4, k=["grammar", "translation"]),
    ]),
    U("HS-ENG-U04", [
        mc(Q + "It is kind (　　) you to help me.", ["of", "for", "to", "with"], "人の性質を表す形容詞（kind など）の後は of＋人。", d=2),
        mc(Q + "I remember (　　) him at the party last year.", ["meeting", "to meet", "meet", "met"], "remember ～ing は「（過去に）～したことを覚えている」。remember to ～は「（これから）忘れずに～する」。", d=2),
        mc(Q + "Don't forget (　　) the letter on your way to school.", ["to mail", "mailing", "mail", "mailed"], "forget to ～「～するのを忘れる」（これからすること）。", d=2),
        mc(Q + "He seems (　　) ill last week.", ["to have been", "to be", "being", "having been"], "述語動詞（seems＝現在）より前のことを表すのは完了不定詞 to have＋過去分詞。", d=3),
        mc(Q + "I am looking forward to (　　) you again.", ["seeing", "see", "seen", "be seeing"], "look forward to の to は前置詞なので後ろは動名詞。", d=2),
        mc(Q + "Would you mind (　　) the window?", ["opening", "to open", "open", "opened"], "mind は目的語に動名詞をとる。", d=1),
    ]),
    U("HS-ENG-U05", [
        mc(Q + "(　　) from the hill, the town looks beautiful.", ["Seen", "Seeing", "To see", "Having seen"], "主語 the town が「見られる」ので受け身の分詞構文（Being）seen。", d=3),
        mc(Q + "(　　) tired, I went to bed early.", ["Feeling", "Felt", "To feel", "Being felt"], "「疲れを感じたので」と理由を表す分詞構文。主語 I が feel するので現在分詞。", d=2),
        mc(Q + "She sat on the bench with her eyes (　　).", ["closed", "closing", "close", "to close"], "with＋名詞＋分詞の付帯状況。目は「閉じられた」状態なので過去分詞。", d=3),
        mc(Q + "I heard my name (　　) in the crowd.", ["called", "calling", "call", "to call"], "hear＋O＋過去分詞で「O が～されるのを聞く」。", d=3),
        mc(Q + "(　　) finished my homework, I went out to play.", ["Having", "Being", "Had", "Have"], "主節より前のことを表すのは完了形の分詞構文 Having＋過去分詞。", d=3),
        sa("次の英文を、接続詞を使ってほぼ同じ意味の文に書きかえなさい。\nWalking along the street, I met an old friend.", "While I was walking along the street, I met an old friend.",
           "分詞構文は時・理由・付帯状況などを表す。ここでは「通りを歩いていると」と時を表す。When I was walking ～ でもよい。", d=3, k=["grammar", "thinking"],
           v=["When I was walking along the street, I met an old friend."]),
    ]),
    U("HS-ENG-U06", [
        mc(Q + "(　　) he said was not true.", ["What", "That", "Which", "Who"], "先行詞をふくむ関係代名詞 what（～すること・もの）。", d=2),
        mc(Q + "This is the house (　　) I was born.", ["where", "which", "what", "who"], "場所を表す先行詞の後で、後ろが完全な文なので関係副詞 where。", d=2),
        mc(Q + "I have a friend, (　　) lives in London.", ["who", "that", "what", "whom"], "コンマの後の非制限用法では that は使えない。", d=2),
        mc(Q + "This is the reason (　　) I came here.", ["why", "which", "where", "how"], "reason の後の関係副詞は why。", d=1),
        mc(Q + "(　　) comes first will get the prize.", ["Whoever", "Whatever", "Whichever", "However"], "「来た人はだれでも」の複合関係代名詞 whoever。", d=3),
        mc(Q + "He said nothing, (　　) made her angry.", ["which", "what", "that", "who"], "前の文全体を先行詞とする非制限用法の which。", d=3),
    ]),
    U("HS-ENG-U07", [
        mc(Q + "This room is three times as (　　) as that one.", ["large", "larger", "largest", "more large"], "倍数表現は X times as＋原級＋as。", d=2),
        mc(Q + "The more you practice, the (　　) you will become.", ["better", "good", "best", "more good"], "the＋比較級 ～, the＋比較級 …「～すればするほど…」。", d=2),
        mc(Q + "No other mountain in Japan is (　　) than Mt. Fuji.", ["higher", "high", "highest", "as high"], "否定語＋比較級＋than で最上級の意味。", d=2),
        mc(Q + "She is (　　) taller than her sister.", ["much", "very", "more", "so"], "比較級を強めるのは much / far / even など。very は比較級を修飾しない。", d=2),
        mc(Q + "He is not so much a teacher (　　) a friend to us.", ["as", "than", "but", "that"], "not so much A as B で「A というよりむしろ B」。", d=3),
        mc("次の英文と最も近い意味を表すものを選びなさい。\nShe is the last person to tell a lie.", ["She would never tell a lie.", "She told the last lie.", "She is the last person who told a lie.", "She often tells lies."],
           "the last＋名詞＋to 不定詞で「最も～しそうにない」。", d=4, k=["grammar", "thinking"]),
    ]),
    U("HS-ENG-U08", [
        mc(Q + "If I (　　) the answer, I would tell you.", ["knew", "know", "had known", "will know"], "現在の事実に反する仮定は仮定法過去。", d=1),
        mc(Q + "If I had studied harder, I (　　) the exam.", ["would have passed", "would pass", "will pass", "passed"], "過去の事実に反する仮定は仮定法過去完了。主節は would have＋過去分詞。", d=2),
        mc(Q + "If I had taken that train, I (　　) here now.", ["wouldn't be", "wouldn't have been", "won't be", "am not"], "条件節は過去、主節は現在（now）の事実に反する混合仮定法。", d=4, k=["grammar", "thinking"]),
        mc(Q + "He talks as if he (　　) everything.", ["knew", "knows", "had known", "will know"], "as if＋仮定法過去で「まるで～であるかのように」（主節と同時）。", d=2),
        mc(Q + "(　　) your help, I couldn't have finished the work.", ["Without", "With", "Unless", "If"], "Without ～「～がなければ（なかったら）」は仮定法の条件を表す。", d=2),
        mc(Q + "It's time you (　　) to bed.", ["went", "go", "will go", "have gone"], "It's time＋仮定法過去で「もう～してもよいころだ」。", d=3),
    ]),
    U("HS-ENG-U09", [
        mc("What is the main idea of the passage?", ["Short naps can improve our performance if we take them properly.", "We should sleep as long as possible during the day.",
                                                     "Naps are harmful for students.", "Only children need naps."],
           "第1段落で主題を示し、最終段落で短い昼寝を正しく取ることの利点をまとめている。", d=2, k=R, st="NAP"),
        mc("According to the passage, how long should a nap be?", ["About 15 to 20 minutes", "More than one hour", "About three hours", "Exactly five minutes"],
           "第2段落に a nap of about 15 to 20 minutes is ideal とある。", d=1, k=R, st="NAP"),
        mc("Why does the writer say long naps are not good?", ["Because they can make us feel sleepy and affect sleep at night.", "Because they are too short.", "Because they make us hungry.", "Because they are not allowed at school."],
           "第3段落で、長い昼寝はぼんやりした状態にし、夜の睡眠にも影響すると述べている。", d=2, k=R, st="NAP"),
        mc("本文中の [[u:However]]（第3段落冒頭）のはたらきとして最も適切なものを選びなさい。", ["前の段落の内容に対して、注意点（反対の側面）を示す", "前の内容の具体例を示す", "結論をまとめる", "時間の順序を示す"],
           "However は逆接のディスコースマーカー。第2段落の利点に対して、長い昼寝の問題点を示している。", d=3, k=["reading", "thinking"], st="NAP"),
        mc("本文の内容に合うものを選びなさい。", ["Some schools and companies have started to encourage short naps.", "The writer thinks naps should be banned.",
                                                 "Naps are useful only in the evening.", "A nap after 6 p.m. is the best."],
           "第2段落に Some schools and companies have started to encourage short naps. とある。", d=2, k=R, st="NAP"),
        desc("本文の要旨を日本語 60 字以内でまとめなさい。", "15〜20分程度の短い昼寝は集中力や作業の効率を高めるが、長い昼寝や遅い時間の昼寝は逆効果なので、正しく取ることが大切だ。",
             "主題（短い昼寝の効果）と条件（長すぎない・遅すぎない）をまとめる。", [("短い昼寝の利点を書いている", 2), ("長い・遅い昼寝の問題点（条件）を書いている", 2), ("字数内で自然な日本語である", 1)],
             d=4, k=["reading", "translation"], grid=60, st="NAP"),
    ], stimuli=[stim("NAP",
                     "Many people feel sleepy in the early afternoon. Some of them drink coffee, but there is another way to stay sharp: taking a short nap.\n\n"
                     "Research suggests that a nap of about 15 to 20 minutes is ideal. It can help us focus better and work more efficiently for the rest of the day. Some schools and companies have started to encourage short naps for this reason.\n\n"
                     "However, longer naps are not always good. If we sleep for more than 30 minutes, we may wake up feeling sleepy and slow. Naps taken late in the afternoon can also make it hard to fall asleep at night.\n\n"
                     "In short, a nap can be a powerful tool if we take it properly. Keep it short, and take it before about 3 p.m.",
                     "passage", "次の英文を読んで、あとの問いに答えなさい。", source="オリジナル", glossary=[("efficiently", "効率よく"), ("properly", "適切に")])]),
    U("HS-ENG-U10", [
        sa("次の日本語を英語に直しなさい。\n彼が来るかどうかはわからない。", "I don't know whether he will come.", "「～かどうか」は whether / if。名詞節の中では未来のことは will で表す。", d=3, k=W,
           v=["I don't know if he will come.", "I'm not sure whether he will come."]),
        sa("次の日本語を英語に直しなさい。\nこの本を読めば、日本の歴史がよくわかるでしょう。", "This book will help you understand Japanese history well.",
           "無生物主語の構文を使うと自然な英語になる。If you read this book, you will understand Japanese history well. でもよい。", d=4, k=W,
           v=["If you read this book, you will understand Japanese history well."]),
        order(O + "私は彼に宿題を手伝ってもらった。", ["I had", "him", "help me", "with my homework"], "have＋人＋動詞の原形で「人に～してもらう」。", d=3, k=W),
        desc("「高校生はアルバイトをするべきだ」という意見について、賛成か反対かを明らかにし、理由を2つ挙げて60語程度の英語で書きなさい。",
             "I agree with the opinion. First, students can learn the value of money by working. They will understand how hard it is to earn money. Second, they can communicate with people of different ages. This experience will help them when they start working in the future. For these reasons, I think high school students should have part-time jobs.",
             "主張→理由1→理由2→まとめ、の構成で書く。First, / Second, / For these reasons, などのつなぎの語を使うと論理が明確になる。",
             [("立場を明確に示している", 2), ("理由を2つ、具体的に述べている", 4), ("論理の展開がわかりやすい（つなぎの語など）", 2), ("文法・語彙の誤りが少ない", 2)], d=5, k=W, p=10, lines=8),
        desc("次のグラフの内容を説明する英文を2文で書きなさい。\n［グラフ］ある高校の生徒が通学に使う手段：自転車 45%、電車 35%、バス 15%、徒歩 5%",
             "The most popular way to get to school is by bike, which 45 percent of the students use. The train is the second, at 35 percent.",
             "最も多いもの、2番目に多いものなど、数値を入れて説明する。the most popular / the second など比較・最上級の表現を使う。",
             [("数値を正しく用いて説明している", 2), ("比較・最上級などを適切に使っている", 2), ("文法・語彙の誤りが少ない", 1)], d=4, k=["writing", "data_interpretation"], lines=3),
        mc("意見文の構成として最も適切なものを選びなさい。", ["主張 → 理由・具体例 → 結論（主張の再確認）", "具体例 → 感想 → 質問", "結論 → 質問 → 主張", "理由だけを並べる"],
           "英語の論理的な文章は、最初に主張（topic sentence）を述べ、理由・具体例で支え、最後に結論で主張を再確認するのが基本。", d=2, k=W),
    ]),
]
