"""単元パック：英語コミュニケーションⅠ 関係詞（関係代名詞 what・関係副詞・非制限用法・複合関係詞）。"""
from banks._common import desc, mc, order, sa
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem,
                         tp)

UNIT_ID = "HS-ENG-U06"


# ======================================================================
# 授業プリント
# ======================================================================

LESSON = lesson(
    goals=["関係詞の後ろの文が「不完全（名詞が欠けている）」か「完全」かを見て、関係代名詞・関係副詞・what を使い分けられる。",
           "制限用法と非制限用法の意味の違いを説明し、前の文全体を受ける , which を使える。",
           "複合関係詞（whoever / whatever / however など）を、名詞節と譲歩の副詞節の2つの働きで読み分けられる。"],
    duration=50,
    readiness=["主格・目的格の関係代名詞 who / which / that を使って名詞を修飾できる（中学3年）。",
               "自動詞と他動詞の区別ができ、動詞の後ろに目的語が必要かどうかを判断できる（HS-ENG-U01）。", "前置詞の後ろには名詞（目的語）が来ることを知っている。"],
    flow=[("導入：「欠けているもの」を探す", 5, "the town I visited と the town I was born を比べ、後ろの文に何が欠けているかに注目させる"),
          ("関係代名詞 what と関係副詞", 15, "what＝the thing(s) which、where / when / why / how の働きを、後ろの文が完全か不完全かで整理する（例題1）"),
          ("非制限用法", 12, "コンマの有無による意味の違いと、前の文全体を受ける , which を確認する（例題2）"),
          ("複合関係詞", 11, "名詞節（～する人・ものはだれでも／何でも）と譲歩（だれが・何を～しても）の2つの働きを整理する（例題3）"),
          ("まとめと確認", 7, "確認問題3問、問題プリントA の課題指示")],
    sections=[
        intro("in1", "関係詞を選ぶ手がかりは「後ろの文」にある",
              "This is the town (　) I visited last year. と This is the town (　) I was born. では、どちらも先行詞は the town だが、入る語が違う。前者は which（visited の目的語が欠けている）、後者は where（I was born. で文が完成している）。関係詞は先行詞の種類だけでなく、後ろの文に何が欠けているかで選ぶ。",
              bullets=["関係代名詞（who / which / that / what）：後ろの文に主語・目的語などの名詞が欠けている（不完全な文）。",
                       "関係副詞（where / when / why / how）：後ろの文は名詞が欠けずに完成している（完全な文）。",
                       "先行詞が「場所」でも、関係副詞 where になるとは限らない。"],
              points=[tp("2つの文を板書し、関係詞の後ろの部分だけを独立した文として読ませる。", ask="I visited last year. と I was born. は、それだけで文として完成しているか。",
                         expect="I visited last year. は visited の目的語がなく不完全。I was born. は完成している。", timing="導入の冒頭"),
                      tp("この単元を通して「後ろの文が完全か不完全か」の判断をくり返すことを予告し、判断の手順を全員で共有する。")]),
        definition("df1", "関係代名詞 what と関係副詞",
                   "what は先行詞を含む関係代名詞で、the thing(s) which と同じ意味（～すること・～するもの）を表し、名詞節を作る。関係副詞は「前置詞＋which」の働きをし、後ろには完全な文が続く。",
                   bullets=["What I want is a new bike.（私が欲しいものは新しい自転車だ）＝ The thing which I want is a new bike.",
                            "where：場所の先行詞（the town where I was born ＝ the town in which I was born）",
                            "when：時の先行詞（the day when we first met ＝ the day on which we first met）",
                            "why：the reason を先行詞にとる（the reason why he was late）",
                            "how：方法を表す。the way と how は並べて使わない（the way I solved it ／ how I solved it）",
                            "what の慣用表現：what is called（いわゆる）、what I am（今の私）、what is more（さらに）、A is to B what C is to D（A と B の関係は C と D の関係と同じ）"],
                   conditions=["what には先行詞が含まれているので、前に名詞（先行詞）を置かない（× the thing what）。",
                               "先行詞が場所でも、後ろの文に目的語が欠けていれば which / that を使う（the museum which we visited）。",
                               "関係副詞の先行詞（the place, the day, the reason など）や関係副詞そのものは省略されることがある（This is where I was born.）。"],
                   points=[tp("what の文は「先行詞＋関係代名詞」に分解して考えさせる。", ask="What she said was true. の What を2語で言いかえると。",
                              expect="The thing which（she said）。", caution="all what のように what の前に先行詞を置く誤りが多い。")]),
        theorem("th1", "関係詞を選ぶ判断表",
                "後ろの文が不完全（名詞が欠ける）→ 関係代名詞（先行詞なし → what）　　後ろの文が完全 → 関係副詞（先行詞の種類で where / when / why / how）",
                ["先行詞が人：who（主格）・whom（目的格）・whose（所有格）・that",
                 "先行詞が人以外：which・whose・that",
                 "先行詞がない、または先行詞を含む：what",
                 "非制限用法（コンマのあと）：who / which / where / when は使えるが、that と what は使えない。",
                 "前置詞＋関係代名詞：前置詞の直後には whom / which を置く（in which, to whom）。that は置けない。"],
                body="関係詞を選ぶ順序は、①後ろの文が完全か不完全か、②先行詞があるか・何か、③制限用法か非制限用法か、の3段階である。",
                points=[tp("判断表を板書し、問題を解くときは必ず①→②→③の順に確かめさせる。", ask="This is the hotel (　) we stayed at. は①の段階でどうなるか。",
                           expect="前置詞 at の目的語が欠けている不完全な文なので関係代名詞 which。", timing="判断表の板書後")]),
        derivation("dv1", "関係副詞が「前置詞＋which」と同じになる理由",
                   ["① 2つの文から出発する。This is the town. ／ I was born in the town.",
                    "② 2文目の the town を関係代名詞 which に変え、先行詞の直後に移す。前置詞ごと移すと in which になる。",
                    "③ This is the town in which I was born.（前置詞を後ろに残した This is the town which I was born in. も可）",
                    "④ 「in which」は場所を表す副詞のまとまり（＝there）として働いている。この副詞のまとまりを1語で表すのが関係副詞 where である。",
                    "⑤ This is the town where I was born. where の後ろの I was born は、前置詞の目的語も欠けていない完全な文になる。",
                    "⑥ 反対に、2文目が We visited the town. なら the town は visited の目的語なので、前置詞はなく which（that）を使う。where を使うと目的語が欠けたままになる。"],
                   body="関係副詞＝前置詞＋which と考えると、「後ろが完全な文なら関係副詞、不完全な文なら関係代名詞」という判断の理由がわかる。",
                   points=[tp("2つの文を矢印でつなぐ手順を板書し、①の2文目で the town が「前置詞の目的語」か「動詞の目的語」かを色分けする。",
                              ask="We stayed at the hotel. から関係詞の文を作ると、where と which のどちらを使うか。", expect="at を残すなら which（the hotel which we stayed at）、at ごとなら where（the hotel where we stayed）。")]),
        definition("df2", "非制限用法と複合関係詞",
                   "関係詞の前にコンマを置く非制限用法は、先行詞について補足説明を加える（「そして／しかし～」）。複合関係詞は関係詞に -ever がついた形で、名詞節（～する人・ものはだれでも／何でも）や譲歩の副詞節（だれが・何を・どんなに～しても）を作る。",
                   bullets=["He has two sons, who are doctors.（息子が2人いて、2人とも医者だ）／ He has two sons who are doctors.（医者をしている息子が2人いる：ほかにも息子がいるかもしれない）",
                            ", which は前の文全体（またはその一部）を受けられる：He passed the test, which surprised us.（彼は合格し、そのことは私たちを驚かせた）",
                            "whoever＝anyone who（～する人はだれでも）／ no matter who（だれが～しても）",
                            "whatever＝anything that（～するものは何でも）／ no matter what（何が・何を～しても）",
                            "whichever（どちらの～でも）、whenever（～するときはいつでも・いつ～しても）、wherever（～するところならどこでも・どこへ～しても）",
                            "however＋形容詞・副詞＋S＋V（どんなに～しても）：However tired you are, ..."],
                   conditions=["非制限用法には that を使えない。固有名詞や唯一のもの（my father など）を先行詞にするときは非制限用法にする。",
                               "however の直後には形容詞・副詞を置く（× However you are tired）。"],
                   points=[tp("コンマの有無で「全体」か「一部」かが変わることを、He has two sons の2文で図示する。",
                              caution="非制限用法の which を that に置きかえる誤りが多い。")]),
        example("ex1", "例題1　関係代名詞と関係副詞",
                "（　）に which, where, what のいずれかを入れなさい。(1) This is the museum (　　) we visited last year.　(2) This is the museum (　　) my sister works.　(3) (　　) you need is more practice.",
                ["(1) we visited last year は visited の目的語が欠けた不完全な文。先行詞は the museum なので which。",
                 "(2) my sister works は完全な文（work は自動詞）。場所の先行詞なので where。",
                 "(3) 先行詞がなく、you need は need の目的語が欠けた不完全な文。文の主語になる名詞節を作る what。"],
                "(1) which　(2) where　(3) What",
                thinking="関係詞の後ろだけを取り出して、文として完成しているかを確かめる。次に先行詞の有無を確かめる。",
                points=[tp("(1) と (2) は先行詞が同じ the museum であることを強調し、判断の決め手は後ろの文であることを確認する。")],
                misconceptions=[("This is the museum where we visited last year.", "visited は他動詞で目的語が必要。目的語が欠けているので関係代名詞 which（that）を使う")]),
        example("ex2", "例題2　非制限用法",
                "次の2文を、関係詞を使って1文にしなさい。(1) I visited Nara. There are many old temples there.　(2) She said nothing. That made him angry.",
                ["(1) Nara は固有名詞なので非制限用法。2文目は there（そこに）を含む完全な文なので関係副詞 where。", "(1) I visited Nara, where there are many old temples.",
                 "(2) That は前の文全体（彼女が何も言わなかったこと）を指す。前の文全体を受けるのは , which。", "(2) She said nothing, which made him angry."],
                "(1) I visited Nara, where there are many old temples.　(2) She said nothing, which made him angry.",
                thinking="先行詞が固有名詞や前の文全体なら非制限用法。コンマの後ろでも、完全な文か不完全な文かで関係副詞・関係代名詞を選ぶ。",
                points=[tp("(2) で that を使う誤りが出やすい。非制限用法に that は使えないことを、判断表③で確認させる。", ask="(2) の which は何を指しているか。", expect="She said nothing という前の文全体。")]),
        example("ex3", "例題3　複合関係詞",
                "次の英文を日本語に訳しなさい。(1) Whoever wants to join us is welcome.　(2) Whoever calls, tell them I'm out.　(3) However hard I tried, I couldn't solve it.",
                ["(1) Whoever wants to join us が文の主語（名詞節）。「私たちに加わりたい人はだれでも歓迎だ」。",
                 "(2) Whoever calls はコンマの後ろに命令文が続く副詞節（譲歩）。「だれが電話してきても、私は留守だと言ってください」。",
                 "(3) However hard は「どんなに一生懸命～しても」（譲歩）。「どんなに一生懸命やっても、それを解けなかった」。"],
                "(1) 私たちに加わりたい人はだれでも歓迎だ。　(2) だれが電話してきても、私は留守だと伝えてください。　(3) どんなに一生懸命やっても、それを解けなかった。",
                thinking="複合関係詞の節が文の主語・目的語になっているか（名詞節）、主節とコンマで区切られて文全体にかかっているか（副詞節）を確かめる。",
                points=[tp("(1) と (2) の違いを、「節のあとに動詞が続くか（is welcome）」「コンマのあとに完全な主節が続くか」で判断させる。")],
                misconceptions=[("However I tried hard, I couldn't solve it.", "however の直後に副詞 hard を置き、However hard I tried, ... とする")]),
        board("bd1", "板書案",
              [("① 関係詞の選び方", ["後ろが不完全 → 関係代名詞", "後ろが完全 → 関係副詞", "先行詞なし → what（＝the thing which）", "the museum which we visited", "the town where I was born"]),
               ("② 非制限用法", ["コンマ＋who / which / where / when", "that・what は不可", "two sons, who are doctors（2人だけ）", "two sons who are doctors（ほかにもいるかも）", ", which ＝ 前の文全体"]),
               ("③ 複合関係詞", ["whoever ＝ anyone who ／ no matter who", "whatever ＝ anything that ／ no matter what", "whenever / wherever / whichever", "however＋形容詞・副詞＋S＋V", "名詞節か、譲歩の副詞節か"])],
              points=[tp("板書は3列に分け、①は判断の手順、②はコンマの有無による意味の違い、③は2つの働きの対比として整理する。①は「完全・不完全」を色分けして書く。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("where / which の判断は、先行詞ではなく後ろの文の動詞が目的語をとるか（他動詞か）で行わせる。", ask="the city (　) we visited と the city (　) we lived の違いは。", expect="visit は他動詞（which）、live は自動詞（where）。"),
               tp("what の文は、文頭の What ～ 全体が主語・目的語になる名詞のまとまりであることを、かっこでくくって示す。", timing="定義1の説明時"),
               tp("非制限用法の which が前の文全体を受ける用法は、訳し下げて「そして、そのことは～」と訳させる。", caution="制限用法のように後ろから訳すと意味が崩れる。"),
               tp("複合関係詞は、no matter ～ や anyone who ～ に言いかえさせて、名詞節か副詞節かを確かめさせる。"),
               tp("問題プリント D の誤答例を使い、「what の前に先行詞を置く」「where と which の取り違え」「非制限用法の that」の3種類の誤りを分類させる。")],
              misconceptions=[("All what he said was true.", "what は先行詞を含むので all の後ろには使えない。All that he said was true."),
                              ("This is the city where I visited last year.", "visited の目的語が欠けているので which（that）。"),
                              ("He failed the exam, that surprised us.", "非制限用法に that は使えない。, which surprised us.")]),
        summary("sm1", "まとめ",
                ["関係詞は「後ろの文が完全か不完全か」→「先行詞があるか・何か」→「コンマがあるか」の順に選ぶ。",
                 "what は先行詞を含む（＝the thing which）。関係副詞は前置詞＋which と同じ働きで、後ろに完全な文が続く。",
                 "非制限用法は補足説明で、that は使えない。, which は前の文全体も受けられる。複合関係詞は名詞節と譲歩の副詞節を作る。"]),
        check("ck1", "確認問題",
              [("This is the park (　　) we often play soccer. の（　）に入る関係詞を答えなさい。", "where（we often play soccer は完全な文）"),
               ("The thing that I want to say is this. を what を使って書きかえなさい。", "What I want to say is this."),
               ("No matter what happens, I'll help you. を複合関係詞を使って書きかえなさい。", "Whatever happens, I'll help you.")]),
    ])


# ======================================================================
# 共通の部品
# ======================================================================

def pick_mc(s, jp, ok, wrongs, expl, ap, steps, alt, pit, mis, d=2, pc=None):
    return mc(f"日本語の意味になるように、（　）に入る最も適切なものを選びなさい。\n{jp}\n{s}", [ok] + [w for w, _ in wrongs], expl, d=d,
              ap=ap, steps=steps, alt=alt, pc=pc or [("後ろの文と先行詞から関係詞の種類を判断している", 1), ("正しい関係詞を選んでいる", 1)],
              pit=pit, why={w: (reason, mis) for w, reason in wrongs})


# ======================================================================
# A 基本確認
# ======================================================================

# (英文, 和訳, 正答, [(誤答, 理由)], 判断の説明)
WHAT = [
    ("(　　) I need now is a good rest.", "今私に必要なのは十分な休息だ。", "What",
     [("That", "That I need now ... では need の目的語が欠けたままで、文が成り立たない。「～するもの」の意味の名詞節は what で作る。"),
      ("Which", "which は先行詞が必要な関係代名詞で、先行詞なしに文の主語となる名詞節を作れない。"),
      ("Who", "who は人を表し、先行詞なしに「～するもの」の意味を表せない。")], "先行詞がなく、need の目的語が欠けているので、先行詞を含む what を使う。"),
    ("This is not (　　) I ordered.", "これは私が注文したものではない。", "what",
     [("that", "that の後ろの I ordered は目的語が欠けた不完全な文なので、接続詞の that は使えない。先行詞もないので関係代名詞 that も使えない。"),
      ("which", "which は先行詞が必要。この文には先行詞がない。"), ("who", "who は人を表す。注文したのは「もの」である。")], "先行詞がなく、ordered の目的語が欠けているので what。"),
    ("The book (　　) I bought yesterday is very interesting.", "昨日私が買った本はとてもおもしろい。", "which",
     [("what", "what は先行詞を含むので、先行詞 The book の後ろには置けない。"), ("who", "先行詞 The book は人ではない。"),
      ("where", "bought の目的語が欠けた不完全な文なので、関係副詞 where は使えない。")], "先行詞 The book（人以外）があり、bought の目的語が欠けているので which。"),
    ("Please tell me (　　) you saw there.", "そこで見たことを教えてください。", "what",
     [("which", "which は先行詞が必要。tell me の後ろに先行詞はない。"), ("that", "that の後ろの you saw there は目的語が欠けた不完全な文なので、接続詞の that は使えない。"),
      ("whose", "whose の後ろには名詞が続く。you saw ... とはつながらない。")], "先行詞がなく、saw の目的語が欠けているので what。"),
    ("He is not (　　) he used to be.", "彼は昔の彼ではない。", "what",
     [("who", "who は先行詞が必要で、「人柄・今の姿」の意味の名詞節を作れない。"), ("which", "which は先行詞が必要。"),
      ("that", "that の後ろの he used to be は補語が欠けた不完全な文なので、接続詞の that は使えない。")], "what he used to be は「昔の彼（の人柄・姿）」という慣用的な表現。"),
    ("Everything (　　) he said was true.", "彼が言ったことはすべて本当だった。", "that",
     [("what", "what は先行詞を含むので、先行詞 Everything の後ろには置けない。"), ("who", "先行詞 Everything は人ではない。"),
      ("whose", "whose の後ろには名詞が続く。he said とはつながらない。")], "先行詞 Everything があり、said の目的語が欠けているので関係代名詞 that（every- などが先行詞のときは that が好まれる）。"),
    ("(　　) is important is to keep trying.", "大切なのは努力し続けることだ。", "What",
     [("That", "That is important ... とすると「それは大切だ」で文が終わり、後ろの is とつながらない。"), ("Which", "which は先行詞が必要。"),
      ("It", "It is important is ... のように動詞が2つ並び、文が成り立たない。")], "先行詞がなく、is important の主語が欠けているので what。"),
    ("Reading is to the mind (　　) food is to the body.", "読書の精神に対する関係は、食物の体に対する関係と同じだ。", "what",
     [("which", "which は先行詞が必要。"), ("that", "A is to B what C is to D の慣用表現では that は使わない。"),
      ("who", "who は人を表す関係代名詞で先行詞が必要。この文には先行詞がない。")], "A is to B what C is to D「A と B の関係は C と D の関係と同じだ」という what の慣用表現。"),
    ("The man (　　) is standing by the door is my teacher.", "ドアのそばに立っている男性は私の先生だ。", "who",
     [("what", "what は先行詞を含むので、先行詞 The man の後ろには置けない。"), ("which", "先行詞 The man は人なので which は使わない。"),
      ("whose", "whose の後ろには名詞が続く。is standing とはつながらない。")], "先行詞 The man（人）があり、is standing の主語が欠けているので who。"),
    ("This is the house (　　) roof is red.", "これは屋根が赤い家だ。", "whose",
     [("which", "which roof is red とはならない。roof の前には所有格の関係代名詞が必要。"), ("what", "what は先行詞を含むので、先行詞 the house の後ろには置けない。"),
      ("where", "where の後ろは完全な文が続くが、roof is red の roof に冠詞・所有格がなく、文として成り立たない。")], "「家の屋根」という所有の関係なので whose。"),
    ("She gave me (　　) little money she had.", "彼女はなけなしのお金を私にくれた。", "what",
     [("which", "which little money とはならない。先行詞もない。"), ("that", "that little money she had は「あのわずかなお金」となり、had の後ろとつながらない。"),
      ("whose", "whose little money は「その人のわずかなお金」となり、意味が通らない。")], "what little＋名詞＋S＋V「少ないながら～するすべての…」という what の慣用表現。"),
]


@gen("basic_check", 5, ["condition_check", "concept"])
def what_or_not(r):
    s, jp, ok, wrongs, why_s = r.choice(WHAT)
    return pick_mc(s, jp, ok, wrongs, f"{ok} が入る。{why_s}",
                   ap="空所の前に先行詞（名詞）があるかを確認し、なければ先行詞を含む what を考える。後ろの文に何が欠けているかも確かめる。",
                   steps=["空所の前に先行詞があるかを確認する。", "空所の後ろの文に何（主語・目的語・補語）が欠けているかを確認する。", f"{why_s}"],
                   alt=["what を the thing(s) which に置きかえて意味が通るか、先行詞のある文なら what を入れると先行詞が二重になることを確かめる。"],
                   pit=["先行詞があるのに what を使う（the book what ...）。", "先行詞がないのに which を使う。"],
                   mis="what と先行詞をとる関係代名詞の混同")


# (英文, 和訳, 正答, [(誤答, 理由)], 判断の説明)
ADV = [
    ("This is the town (　　) my mother was born.", "ここは母が生まれた町だ。", "where",
     [("which", "my mother was born は完全な文。which を使うなら前置詞 in が必要（which my mother was born in）。"), ("when", "先行詞 the town は場所なので when は使わない。"),
      ("what", "what は先行詞を含むので、先行詞 the town の後ろには置けない。")], "後ろは完全な文で、先行詞が場所なので関係副詞 where。"),
    ("I remember the day (　　) we first met.", "私たちが初めて会った日を覚えている。", "when",
     [("which", "we first met は完全な文。which を使うなら前置詞 on が必要（on which）。"), ("where", "先行詞 the day は時なので where は使わない。"),
      ("what", "what は先行詞を含むので、先行詞 the day の後ろには置けない。")], "後ろは完全な文で、先行詞が時なので関係副詞 when。"),
    ("Tell me the reason (　　) you were absent yesterday.", "昨日休んだ理由を教えて。", "why",
     [("which", "you were absent yesterday は完全な文。which を使うなら for which とする。"), ("where", "先行詞 the reason は場所ではない。"),
      ("what", "what は先行詞を含むので、先行詞 the reason の後ろには置けない。")], "後ろは完全な文で、先行詞が the reason なので関係副詞 why。"),
    ("This is (　　) I solved the problem.", "このようにして私はその問題を解いた。", "how",
     [("the way how", "the way と how は並べて使わない。the way I solved ... か how I solved ... のどちらかにする。"),
      ("which", "which は先行詞が必要で、後ろの I solved the problem は完全な文なので使えない。"), ("what", "what の後ろは不完全な文が続く。I solved the problem は完全な文。")],
     "「方法」を表す関係副詞 how。先行詞 the way は省かれている。"),
    ("This is the museum (　　) we visited last year.", "これは私たちが昨年訪れた博物館だ。", "which",
     [("where", "visited は他動詞で、後ろに目的語が欠けている不完全な文なので、関係副詞 where は使えない。"), ("when", "先行詞 the museum は時ではない。"),
      ("what", "what は先行詞を含むので、先行詞 the museum の後ろには置けない。")], "先行詞は場所だが、visited の目的語が欠けているので関係代名詞 which。"),
    ("Kyoto is a city (　　) many tourists visit every year.", "京都は毎年多くの観光客が訪れる都市だ。", "which",
     [("where", "visit は他動詞で目的語が欠けている不完全な文なので、関係副詞 where は使えない。"), ("when", "先行詞 a city は時ではない。"),
      ("what", "what は先行詞を含むので、先行詞 a city の後ろには置けない。")], "visit の目的語が欠けているので関係代名詞 which。"),
    ("Do you know the place (　　) the accident happened?", "その事故が起きた場所を知っていますか。", "where",
     [("which", "the accident happened は完全な文（happen は自動詞）。which を使うなら前置詞が必要。"), ("when", "先行詞 the place は時ではない。"),
      ("what", "what は先行詞を含むので、先行詞 the place の後ろには置けない。")], "後ろは完全な文で、先行詞が場所なので where。"),
    ("Summer is the season (　　) we can enjoy swimming in the sea.", "夏は海で泳ぐのを楽しめる季節だ。", "when",
     [("which", "we can enjoy swimming in the sea は完全な文。which を使うなら in which とする。"), ("where", "先行詞 the season は時を表す。"),
      ("what", "what は先行詞を含むので、先行詞 the season の後ろには置けない。")], "後ろは完全な文で、先行詞が時なので when。"),
    ("That is (　　) he got angry.", "それが、彼が怒った理由だ。", "why",
     [("how", "That is how he got angry. は「そのようにして彼は怒った」の意味になり、日本語と合わない。"), ("which", "which は先行詞が必要で、後ろの文も完全な文なので使えない。"),
      ("what", "what の後ろは不完全な文が続く。he got angry は完全な文。")], "「理由」を表す関係副詞 why。先行詞 the reason は省かれている。"),
    ("This is the hotel (　　) we stayed at last summer.", "これは私たちが昨年の夏に泊まったホテルだ。", "which",
     [("where", "文末に前置詞 at があり、at の目的語が欠けている。where を使うと at が余る。"), ("when", "先行詞 the hotel は時ではない。"),
      ("what", "what は先行詞を含むので、先行詞 the hotel の後ろには置けない。")], "前置詞 at の目的語が欠けているので関係代名詞 which。"),
    ("Is there a shop (　　) I can buy stamps near here?", "この近くに切手を買える店はありますか。", "where",
     [("which", "I can buy stamps は完全な文。which を使うなら at which とする。"), ("when", "先行詞 a shop は時ではない。"),
      ("what", "what は先行詞を含むので、先行詞 a shop の後ろには置けない。")], "後ろは完全な文で、先行詞が場所なので where。"),
    ("I'll never forget the morning (　　) I heard the news.", "その知らせを聞いた朝のことは決して忘れない。", "when",
     [("which", "I heard the news は完全な文。which を使うなら on which とする。"), ("where", "先行詞 the morning は時を表す。"),
      ("what", "what は先行詞を含むので、先行詞 the morning の後ろには置けない。")], "後ろは完全な文で、先行詞が時なので when。"),
]


@gen("basic_check", 5, ["condition_check", "computation"])
def adverb_or_pronoun(r):
    s, jp, ok, wrongs, why_s = r.choice(ADV)
    return pick_mc(s, jp, ok, wrongs, f"{ok} が入る。{why_s}",
                   ap="関係詞の後ろの部分だけを取り出し、名詞が欠けている不完全な文か、完全な文かを確かめる。",
                   steps=["空所の後ろの文を取り出す。", "動詞が他動詞か自動詞か、前置詞の目的語が欠けていないかを確かめる。", f"{why_s}"],
                   alt=["2つの文に分けて書き、先行詞が2文目で「動詞・前置詞の目的語」なら関係代名詞、「副詞（there / then など）」なら関係副詞と確かめる。"],
                   pit=["先行詞が場所なら必ず where、時なら必ず when と決めつける。"],
                   mis="関係代名詞と関係副詞の混同")


# (英文, 和訳, 正答, [(誤答, 理由)], 判断の説明)
NONR = [
    ("I have two brothers, (　　) live in Osaka.", "私には兄弟が2人いて、2人とも大阪に住んでいる。", "who",
     [("that", "非制限用法（コンマの後ろ）に that は使えない。"), ("which", "先行詞 two brothers は人なので which は使わない。"),
      ("what", "what は先行詞を含み、非制限用法にも使えない。")], "先行詞は人で、live の主語が欠けているので , who。"),
    ("She passed the exam, (　　) surprised everyone.", "彼女は試験に合格し、そのことはみんなを驚かせた。", "which",
     [("that", "非制限用法に that は使えない。"), ("what", "what は先行詞を含み、非制限用法にも使えない。"),
      ("it", "it を使うと2つの文がコンマだけでつながり、接続詞がないので文が成り立たない。")], "前の文全体（彼女が合格したこと）を受ける , which。"),
    ("We visited Nara, (　　) has many old temples.", "私たちは奈良を訪れたが、そこには古い寺がたくさんある。", "which",
     [("where", "has の主語が欠けているので関係副詞 where は使えない。"), ("that", "非制限用法に that は使えない。"),
      ("what", "what は先行詞を含み、非制限用法にも使えない。")], "has の主語が欠けているので関係代名詞 , which。"),
    ("I met Mr. Kato, (　　) is our new English teacher.", "加藤先生に会ったが、彼は私たちの新しい英語の先生だ。", "who",
     [("that", "非制限用法に that は使えない。"), ("which", "先行詞 Mr. Kato は人なので which は使わない。"),
      ("whom", "is の主語が欠けているので、主格の who が必要。whom は目的格。")], "先行詞は人で、is の主語が欠けているので , who。"),
    ("He tried to open the door, (　　) he found impossible.", "彼はドアを開けようとしたが、それは不可能だとわかった。", "which",
     [("that", "非制限用法に that は使えない。"), ("what", "what は先行詞を含み、非制限用法にも使えない。"),
      ("it", "it を使うと2つの文がコンマだけでつながり、文が成り立たない。")], "found の目的語が欠けており、前の内容（ドアを開けること）を受ける , which。"),
    ("I went to Okinawa, (　　) I swam in the sea.", "私は沖縄へ行き、そこで海で泳いだ。", "where",
     [("which", "I swam in the sea は完全な文なので関係代名詞 which は使えない。"), ("that", "非制限用法に that は使えない。"),
      ("when", "先行詞 Okinawa は場所であり、時ではない。")], "後ろは完全な文で、先行詞が場所なので , where。"),
    ("Come back at six, (　　) dinner will be ready.", "6時に戻ってきて。その時には夕食ができているから。", "when",
     [("which", "dinner will be ready は完全な文なので関係代名詞 which は使えない。"), ("that", "非制限用法に that は使えない。"),
      ("where", "先行詞 six（6時）は時であり、場所ではない。")], "後ろは完全な文で、先行詞が時なので , when。"),
    ("My sister, (　　) lives in Kobe, is a nurse.", "姉は神戸に住んでいて、看護師をしている。", "who",
     [("that", "非制限用法に that は使えない。"), ("which", "先行詞 My sister は人なので which は使わない。"),
      ("whose", "whose の後ろには名詞が続く。lives とはつながらない。")], "先行詞は人で、lives の主語が欠けているので , who。"),
    ("He lent me some books, (　　) were very useful.", "彼は本を何冊か貸してくれ、それらはとても役に立った。", "which",
     [("that", "非制限用法に that は使えない。"), ("what", "what は先行詞を含み、非制限用法にも使えない。"),
      ("who", "先行詞 some books は人ではない。")], "先行詞は人以外で、were の主語が欠けているので , which。"),
    ("Ken said he was sick, (　　) was not true.", "ケンは具合が悪いと言ったが、それは本当ではなかった。", "which",
     [("that", "非制限用法に that は使えない。"), ("what", "what は先行詞を含み、非制限用法にも使えない。"),
      ("it", "it を使うと2つの文がコンマだけでつながり、文が成り立たない。")], "前の内容（具合が悪いということ）を受ける , which。"),
    ("I have a friend in Canada, (　　) father is a pilot.", "カナダに友達がいて、その父親はパイロットだ。", "whose",
     [("who", "who father とはならない。father の前には所有格が必要。"), ("which", "先行詞 a friend は人であり、which father とも言わない。"),
      ("that", "非制限用法に that は使えない。")], "「友達の父親」という所有の関係なので , whose。"),
]


@gen("basic_check", 5, ["concept", "common_error"])
def nonrestrictive(r):
    s, jp, ok, wrongs, why_s = r.choice(NONR)
    return pick_mc(s, jp, ok, wrongs, f"{ok} が入る。{why_s}",
                   ap="コンマの後ろの関係詞（非制限用法）では that と what が使えないことを確認し、後ろの文の欠けている要素と先行詞の種類から選ぶ。",
                   steps=["コンマがあるので非制限用法だと確認する（that・what は不可）。", "先行詞（前の名詞、または前の文全体）を確認する。", f"{why_s}"],
                   alt=["関係詞を「and＋代名詞（and he / and it / and there など）」に置きかえて、意味が通るかを確かめる。"],
                   pit=["非制限用法に that を使う。", "前の文全体を受けるときに it を使い、接続詞のない文にする。"],
                   mis="非制限用法の関係詞の選び方の誤り")


# (英文, 和訳, 正答, [(誤答, 理由)], 判断の説明)
COMP = [
    ("You can invite (　　) you like to the party.", "パーティーには好きな人をだれでも招待していい。", "whoever",
     [("whatever", "whatever は「もの・こと」を表す。招待するのは人。"), ("however", "however の後ろには形容詞・副詞が続き、invite の目的語にならない。"),
      ("whenever", "whenever は「時」を表す副詞節を作り、invite の目的語にならない。")], "invite の目的語になる名詞節で、人を表すので whoever（＝anyone who）。"),
    ("(　　) you do, do it well.", "何をするにしても、しっかりやりなさい。", "Whatever",
     [("However", "however の直後には形容詞・副詞が続く。you do の目的語も欠けたままになる。"), ("Whoever", "do の目的語は「こと」であり、人ではない。"),
      ("Wherever", "wherever は場所を表し、do の目的語が欠けたままになる。")], "do の目的語が欠けており、「何を～しても」の譲歩なので Whatever（＝No matter what）。"),
    ("(　　) tired you are, you must finish this today.", "どんなに疲れていても、今日これを終えなければならない。", "However",
     [("Whatever", "whatever の直後に形容詞 tired を置いて「どんなに～でも」の意味にはできない。"), ("Whenever", "whenever の直後に形容詞は置けない。"),
      ("Whichever", "whichever の直後に形容詞は置けない。")], "however＋形容詞＋S＋V で「どんなに～でも」。"),
    ("Come and see me (　　) you like.", "好きなときにいつでも会いに来て。", "whenever",
     [("whatever", "whatever は「もの・こと」を表す。日本語は「好きなときに」で時を表す。"), ("wherever", "wherever は場所を表し「好きな所で」となり、日本語と合わない。"),
      ("however", "however の後ろには形容詞・副詞が続く。")], "「～するときはいつでも」なので whenever。"),
    ("My dog follows me (　　) I go.", "どこへ行っても犬が私についてくる。", "wherever",
     [("whatever", "whatever は「もの・こと」を表し、go の目的語にはならない。"), ("whoever", "whoever は人を表す。"),
      ("however", "however の後ろには形容詞・副詞が続く。")], "「どこへ～しても」なので wherever。"),
    ("There are three cakes. Take (　　) you like.", "ケーキが3つある。どれでも好きなものを取って。", "whichever",
     [("whoever", "whoever は人を表す。取るのはケーキ。"), ("however", "however の後ろには形容詞・副詞が続き、take の目的語にならない。"),
      ("wherever", "wherever は場所を表し、take の目的語にならない。")], "限られた中から「どれでも」なので whichever。"),
    ("(　　) hard he tried, he couldn't open the door.", "どんなに頑張っても、彼はドアを開けられなかった。", "However",
     [("Whatever", "whatever の直後に副詞 hard を置いて「どんなに～しても」の意味にはできない。"), ("Whenever", "whenever の直後に副詞は置けない。"),
      ("Whoever", "whoever の直後に副詞は置けない。")], "however＋副詞＋S＋V で「どんなに～しても」。"),
    ("(　　) breaks the rules will be punished.", "規則を破る者はだれでも罰せられる。", "Whoever",
     [("Whatever", "whatever は「もの・こと」を表す。規則を破るのは人。"), ("However", "however の後ろには形容詞・副詞が続き、文の主語にならない。"),
      ("Wherever", "wherever は場所を表す副詞節を作り、文の主語にならない。")], "文の主語になる名詞節で、人を表すので Whoever（＝Anyone who）。"),
    ("I'll support you (　　) happens.", "何が起ころうと、私はあなたを支える。", "whatever",
     [("whoever", "whoever は人を表す。起こるのは「こと」。"), ("however", "however の後ろには形容詞・副詞が続き、happens の主語にならない。"),
      ("whenever", "whenever の後ろには主語のある完全な文が続く。happens の主語が欠けたままになる。")], "happens の主語が欠けており、「何が～しても」なので whatever。"),
    ("(　　) you call me, I'll answer.", "いつ電話してくれても、私は出るよ。", "Whenever",
     [("Whatever", "call の目的語 me がすでにあり、whatever の入る場所がない。"), ("Whoever", "you call me は完全な文で、whoever の入る場所がない。"),
      ("However", "however の後ろには形容詞・副詞が続く。")], "後ろが完全な文で、「いつ～しても」なので Whenever。"),
    ("(　　) you choose, you will like it.", "どちらを選んでも、きっと気に入るよ。", "Whichever",
     [("Whoever", "whoever は人を表すが、主節の it は物を指している。"), ("However", "however の後ろには形容詞・副詞が続き、choose の目的語にならない。"),
      ("Whenever", "whenever の後ろには完全な文が続く。choose の目的語が欠けたままになる。")], "choose の目的語が欠けており、「どちらを～しても」なので Whichever。"),
]


@gen("basic_check", 5, ["computation", "concept"])
def compound_relative(r):
    s, jp, ok, wrongs, why_s = r.choice(COMP)
    return pick_mc(s, jp, ok, wrongs, f"{ok} が入る。{why_s}",
                   ap="複合関係詞の後ろの文に何が欠けているか（主語・目的語か、何も欠けていないか、形容詞・副詞が続くか）と、「人・もの・時・場所・程度」のどれを表すかを確かめる。",
                   steps=["空所の後ろの文の形を確かめる。", "日本語から、人・もの・時・場所・程度のどれを表すかを判断する。", f"{why_s}"],
                   alt=["anyone who / anything that / no matter how などに言いかえて、意味が通るかを確かめる。"],
                   pit=["however の直後に S＋V を置き、形容詞・副詞を後ろに回す。", "whatever と whoever（もの・人）を取り違える。"],
                   mis="複合関係詞の種類と働きの混同")


# ======================================================================
# B 標準演習
# ======================================================================

# (指示, 元の文, 答え, 別解, 説明)
COMBINE = [
    ("関係副詞を使って1文にしなさい。", "This is the park. We played tennis there.", "This is the park where we played tennis.",
     ["This is the park in which we played tennis.", "This is the park which we played tennis in."], "there（＝in the park）を関係副詞 where に変える。"),
    ("関係副詞を使って1文にしなさい。", "I remember the day. I met her on that day.", "I remember the day when I met her.",
     ["I remember the day on which I met her."], "on that day を関係副詞 when に変える。"),
    ("非制限用法の関係代名詞を使って1文にしなさい。", "I have an uncle. He lives in Paris.", "I have an uncle, who lives in Paris.", [],
     "He を主格の関係代名詞 who に変え、コンマの後ろに置く。"),
    ("関係代名詞を使って1文にしなさい。", "He didn't come to the party. That made us sad.", "He didn't come to the party, which made us sad.", [],
     "That は前の文全体を指すので、非制限用法の , which で受ける。"),
    ("what を使って書きかえなさい。", "The thing that I want is a new bike.", "What I want is a new bike.", [], "The thing that を、先行詞を含む what 1語にする。"),
    ("関係副詞を使って1文にしなさい。", "Tell me the reason. You were late for that reason.", "Tell me the reason why you were late.",
     ["Tell me the reason for which you were late."], "for that reason を関係副詞 why に変える。"),
    ("非制限用法の関係代名詞を使って1文にしなさい。", "We stayed at a hotel. It had a beautiful garden.", "We stayed at a hotel, which had a beautiful garden.", [],
     "It を主格の関係代名詞 which に変え、コンマの後ろに置く。"),
    ("非制限用法の関係副詞を使って1文にしなさい。", "I visited Kobe. My aunt lives there.", "I visited Kobe, where my aunt lives.", [],
     "there を関係副詞 where に変え、固有名詞 Kobe の後ろにコンマをつけて置く。"),
    ("関係代名詞を使って1文にしなさい。", "Do you know the girl? Her bag is on the desk.", "Do you know the girl whose bag is on the desk?", [],
     "Her を所有格の関係代名詞 whose に変える。"),
    ("複合関係代名詞を使って書きかえなさい。", "Anyone who wants to join us is welcome.", "Whoever wants to join us is welcome.", [],
     "anyone who は whoever 1語で表せる。"),
    ("複合関係詞を使って書きかえなさい。", "No matter what happens, I'll be on your side.", "Whatever happens, I'll be on your side.", [],
     "no matter what は whatever 1語で表せる（譲歩）。"),
    ("複合関係詞を使って書きかえなさい。", "No matter how busy he is, he reads the newspaper every day.", "However busy he is, he reads the newspaper every day.", [],
     "no matter how は however。直後に形容詞 busy を置く。"),
    ("関係代名詞を使って1文にしなさい。", "This is the museum. We visited it last summer.", "This is the museum which we visited last summer.",
     ["This is the museum that we visited last summer.", "This is the museum we visited last summer."], "it は visited の目的語なので、目的格の関係代名詞 which（that）を使う。where は使えない。"),
]


@gen("standard_practice", 5, ["computation", "condition_check"])
def combine(r):
    inst, src, ans, v, why_s = r.choice(COMBINE)
    return sa(f"次の英文を、指示に従って書きかえなさい。（{inst}）\n{src}", ans, why_s, d=3, v=v,
              ap="2文目の中で、1文目の名詞を指している語（代名詞・副詞 there / then など）を探し、それが主語・目的語・所有格・副詞のどれかで関係詞を決める。",
              steps=["1文目と2文目で共通するもの（先行詞）を確認する。", "2文目の中でそれを指す語の働き（主語・目的語・所有格・副詞・前の文全体）を確認する。",
                     f"{why_s}", f"答え：{ans}"],
              alt=["書きかえた文を2文に分け直し、元の2文と意味が一致するかを確かめる。"],
              pc=[("適切な関係詞を選んでいる", 2), ("語順・コンマの有無が正しい", 2)],
              pit=["目的語を指しているのに関係副詞を使う。", "非制限用法でコンマを落とす、または that を使う。"])


# (英文, 和訳, 正答, [(誤答, 理由)])
PREP = [
    ("This is the room in (　　) the meeting was held.", "ここは会議が開かれた部屋だ。", "which",
     [("that", "前置詞の直後に関係代名詞 that は置けない。"), ("where", "前置詞の後ろに関係副詞 where は置けない（in where とは言わない）。"), ("what", "what は先行詞を含むので、先行詞 the room とともに使えない。")]),
    ("The man to (　　) I spoke was very kind.", "私が話しかけた男性はとても親切だった。", "whom",
     [("who", "前置詞の直後には目的格の whom を置く。"), ("that", "前置詞の直後に that は置けない。"), ("which", "先行詞 The man は人なので which は使わない。")]),
    ("Is this the pen with (　　) you wrote the letter?", "これはあなたが手紙を書いたペンですか。", "which",
     [("that", "前置詞の直後に that は置けない。"), ("what", "what は先行詞を含むので、先行詞 the pen とともに使えない。"), ("whom", "先行詞 the pen は人ではない。")]),
    ("The town in (　　) I grew up is near the sea.", "私が育った町は海の近くにある。", "which",
     [("where", "前置詞の後ろに関係副詞 where は置けない。in which か where のどちらかにする。"), ("that", "前置詞の直後に that は置けない。"), ("what", "what は先行詞を含むので、先行詞 The town とともに使えない。")]),
    ("She is the friend on (　　) I can always rely.", "彼女は私がいつも頼りにできる友人だ。", "whom",
     [("who", "前置詞の直後には目的格の whom を置く。"), ("that", "前置詞の直後に that は置けない。"), ("which", "先行詞 the friend は人なので which は使わない。")]),
    ("The day on (　　) we arrived was very hot.", "私たちが着いた日はとても暑かった。", "which",
     [("when", "前置詞の後ろに関係副詞 when は置けない。on which か when のどちらかにする。"), ("that", "前置詞の直後に that は置けない。"), ("what", "what は先行詞を含むので、先行詞 The day とともに使えない。")]),
    ("This is the reason for (　　) he quit his job.", "これが彼が仕事を辞めた理由だ。", "which",
     [("why", "前置詞の後ろに関係副詞 why は置けない。for which か why のどちらかにする。"), ("that", "前置詞の直後に that は置けない。"), ("what", "what は先行詞を含むので、先行詞 the reason とともに使えない。")]),
    ("The girl with (　　) I went to the movies is my cousin.", "私が一緒に映画に行った少女はいとこだ。", "whom",
     [("who", "前置詞の直後には目的格の whom を置く。"), ("that", "前置詞の直後に that は置けない。"), ("whose", "whose の後ろには名詞が続く。I went とはつながらない。")]),
    ("The box in (　　) I keep my letters is under the bed.", "私が手紙をしまっている箱はベッドの下にある。", "which",
     [("where", "前置詞の後ろに関係副詞 where は置けない。"), ("that", "前置詞の直後に that は置けない。"), ("what", "what は先行詞を含むので、先行詞 The box とともに使えない。")]),
    ("He is the doctor to (　　) I owe my life.", "彼は私の命の恩人である医師だ。", "whom",
     [("who", "前置詞の直後には目的格の whom を置く。"), ("that", "前置詞の直後に that は置けない。"), ("which", "先行詞 the doctor は人なので which は使わない。")]),
]


@gen("standard_practice", 5, ["condition_check", "common_error"])
def prep_relative(r):
    s, jp, ok, wrongs = r.choice(PREP)
    return pick_mc(s, jp, ok, wrongs, f"{ok} が入る。前置詞の直後に置ける関係詞は whom（人）と which（人以外）だけで、that・関係副詞・what は置けない。", d=3,
                   ap="前置詞の直後に置ける関係詞は whom と which だけであることを確認し、先行詞が人か人以外かで選ぶ。",
                   steps=["空所の直前が前置詞であることを確認する。", "前置詞の直後に置けるのは whom / which だけ（that・who・関係副詞は不可）。", f"先行詞の種類から {ok} を選ぶ。"],
                   alt=["前置詞を文末に回した形（the man who I spoke to など）や関係副詞を使った形に書きかえ、意味が同じになるかを確かめる。"],
                   pit=["前置詞の直後に that や who を置く。", "in where のように前置詞と関係副詞を重ねる。"],
                   mis="前置詞＋関係代名詞の形の誤り", pc=[("前置詞の直後に置ける関係詞を判断している", 2), ("先行詞に合う関係詞を選んでいる", 2)])


ORDERS = [
    ("私が欲しいのは新しいパソコンだ。", ["what", "I", "want", "is", "a new", "computer"], "what I want が文の主語になる名詞節。"),
    ("ここは私の父が生まれた町だ。", ["this", "is", "the town", "where", "my father", "was born"], "my father was born は完全な文なので関係副詞 where。"),
    ("彼が遅れた理由を知っていますか。", ["do", "you", "know", "the reason", "why", "he was late"], "the reason を先行詞とする関係副詞 why。"),
    ("彼女は試験に合格し、そのことが両親を喜ばせた。", ["she", "passed", "the exam,", "which", "made", "her parents happy"], "前の文全体を受ける非制限用法の , which。"),
    ("何が起ころうとも、私はあきらめない。", ["whatever", "happens,", "I", "won't", "give", "up"], "whatever＝no matter what（譲歩）。"),
    ("どんなに忙しくても、彼は毎朝走る。", ["however", "busy", "he is,", "he", "runs", "every morning"], "however の直後に形容詞 busy を置く。"),
    ("このようにして彼はその問題を解いた。", ["this", "is", "how", "he", "solved", "the problem"], "方法を表す関係副詞 how（the way は省く）。"),
    ("私たちが初めて会った日を覚えていますか。", ["do", "you", "remember", "the day", "when", "we first met"], "時の先行詞 the day と関係副詞 when。"),
    ("今日できることを明日まで延ばすな。", ["don't", "put off", "until tomorrow", "what", "you can do", "today"], "what you can do today が put off の目的語（目的語が長いので後ろに回している）。"),
    ("私にはおじが1人いて、彼は医者をしている。", ["I", "have", "an uncle,", "who", "is", "a doctor"], "補足説明の非制限用法 , who。"),
    ("パーティーには好きな人をだれでも連れてきていいよ。", ["you can", "bring", "whoever", "you", "like", "to the party"], "whoever＝anyone who。whoever you like が bring の目的語になる名詞節。"),
]


@gen("standard_practice", 6, ["application", "computation"])
def build_order(r):
    jp, parts, point = r.choice(ORDERS)
    sent = " ".join(parts)
    sent = sent[0].upper() + sent[1:] + ("?" if parts[0] == "do" else ".")
    return order(f"日本語に合うように、語句を並べかえて英文を完成させなさい。ただし、文頭にくる語も小文字で示してあり、コンマは語句に含めてある。\n{jp}", parts,
                 f"{sent}　{point}", d=3, p=4,
                 ap="関係詞のまとまり（関係詞＋後ろの文）を先に作り、それが名詞を修飾するのか、文の主語・目的語になるのか、文全体にかかるのかを決める。",
                 steps=["関係詞の種類と、その後ろに続く語句のまとまりを作る。", "先行詞の直後、または主語・目的語の位置、文頭の副詞節の位置に置く。", f"ポイント：{point}", f"完成文：{sent}"],
                 alt=["完成した英文を和訳し直して、日本語と一致するかを確かめる。"],
                 pc=[("関係詞のまとまりを正しく作っている", 2), ("全体の語順が正しい", 2)],
                 pit=["however と形容詞を離して置く。", "what の前に名詞（先行詞）を置く。"])


# (英文, 正しい和訳, [(誤訳, 理由)])
IDIOMS = [
    ("He is what is called a walking dictionary.", "彼はいわゆる生き字引だ。",
     [("彼は生き字引と呼ばれるものを持っている。", "動詞は is であり、「持っている」にあたる語はない。what is called は「いわゆる」という慣用表現。"),
      ("彼が呼んだのは生き字引だ。", "is called は受け身で「呼ばれる」の意味。彼が呼んだのではない。"),
      ("生き字引と呼ばれるのは彼だけだ。", "「だけ」にあたる only などの語がない。")]),
    ("My father made me what I am today.", "父のおかげで今日の私がある。",
     [("父は私に、今日私がすることを作ってくれた。", "what I am は「今の私（の姿・人柄）」で、「私がすること」ではない。"),
      ("父は今日、私を作った。", "today は what I am today の一部で「今日の私」を表し、made を修飾していない。"),
      ("今日の私は父のようだ。", "made me ～「私を～にした」の意味が抜けている。「～のようだ」にあたる語もない。")]),
    ("It was cold, and what was worse, it began to rain.", "寒かったし、さらに悪いことに雨が降り出した。",
     [("寒かったが、雨よりは悪くなかった。", "what was worse は「さらに悪いことに」という挿入の慣用表現で、比較の対象を示していない。"),
      ("寒かったことは、雨が降るより悪かった。", "寒さと雨を比べている文ではない。what was worse は後ろの内容を導く挿入表現。"),
      ("寒く、雨が降り出したことはさらに悪くなかった。", "否定語がないのに否定の意味にしている。")]),
    ("A man's worth lies not in what he has but in what he is.", "人の価値は財産ではなく人柄にある。",
     [("人の価値は、持っているものと、いる場所にある。", "what he is は「その人の人柄・人となり」で、場所ではない。また not A but B の否定を落としている。"),
      ("人は持っているものの価値を知らない。", "lies in は「～にある」で、「知らない」の意味はない。"),
      ("人の価値は持ち物にあり、人柄にはない。", "not A but B「A ではなく B」を逆に読んでいる。")]),
    ("Reading is to the mind what exercise is to the body.", "読書の精神に対する関係は、運動の体に対する関係と同じだ。",
     [("読書は精神のためであり、運動は体のためではない。", "否定語がない。A is to B what C is to D は2つの関係が同じだと述べる表現。"),
      ("精神にとって読書とは何か、体にとって運動とは何か。", "what を疑問詞と読んでいる。この文は疑問文ではない。"),
      ("読書は運動よりも精神に良い。", "比較級がなく、読書と運動を比べている文ではない。")]),
    ("She is not what she was ten years ago.", "彼女は10年前の彼女ではない。",
     [("彼女は10年前に何であったかを言わない。", "what を疑問詞と読み、「言わない」にあたる語を補っている。"),
      ("彼女は10年前にいた場所にいない。", "what she was は「（当時の）彼女の姿・人柄」で、場所ではない。"),
      ("10年前、彼女は今の彼女ではなかった。", "is（現在）と was（10年前）の関係が逆になっている。")]),
    ("This is what we call a \"smart city.\"", "これがいわゆる「スマートシティ」だ。",
     [("これは私たちが「スマートシティ」に電話しているところだ。", "call を「電話する」と読んでいる。what we call は「いわゆる」という慣用表現。"),
      ("私たちは何を「スマートシティ」と呼ぶのか。", "what を疑問詞と読んでいる。この文は疑問文ではない。"),
      ("これは「スマートシティ」が私たちを呼ぶものだ。", "主語 we と目的語の関係を逆にしている。呼ぶのは私たち。")]),
    ("He gave her what money he had.", "彼は持っていたお金を全部彼女に与えた。",
     [("彼は彼女に、どんなお金を持っているかたずねた。", "what を疑問詞と読み、gave を「たずねた」と訳している。"),
      ("彼は持っていたお金の一部を彼女に与えた。", "what＋名詞＋S＋V は「～するすべての…」の意味で、「一部」ではない。"),
      ("彼女が持っていたお金を彼は受け取った。", "主語 he と目的語 her の関係を逆にしている。与えたのは彼。")]),
    ("What is more, the hotel was very cheap.", "そのうえ、そのホテルはとても安かった。",
     [("ホテルより安いものは何か。", "what を疑問詞と読んでいる。what is more は「そのうえ・さらに」という慣用表現。"),
      ("そのホテルがとても安かったことがもっと大事だ。", "important などの語がなく、「大事だ」の意味はない。"),
      ("もっと安いホテルはどれだったか。", "疑問文ではなく、more は cheap を比較級にしているのでもない。")]),
]


@gen("standard_practice", 4, ["concept", "common_error"])
def what_idiom(r):
    s, ok, wrongs = r.choice(IDIOMS)
    return mc(f"次の英文の意味として最も適切なものを選びなさい。\n{s}", [ok] + [w for w, _ in wrongs],
              f"「{ok}」が正しい。関係代名詞 what を含む慣用表現の意味をとる。", d=3,
              ap="what を疑問詞と決めつけず、「～すること・もの」の関係代名詞や、what is called / what I am / what is more などの慣用表現として読めないかを考える。",
              steps=["文の主語と述語動詞を確認する。", "what のまとまりが文中でどんな働き（主語・補語・目的語・挿入）をしているかを確認する。", f"慣用表現の意味をあてはめて訳す：「{ok}」。"],
              alt=["what を the thing(s) which に置きかえて直訳し、自然な日本語に整えて確かめる。"],
              pc=[("what のまとまりの働きをとらえている", 2), ("正しい和訳を選んでいる", 2)],
              pit=["文中の what をすべて疑問詞「何」と訳す。"],
              why={w: (reason, "関係代名詞 what の慣用表現の誤読") for w, reason in wrongs})


# ======================================================================
# C 思考力・記述応用
# ======================================================================

PAIRS = [
    ("He has two daughters who are teachers.", "He has two daughters, who are teachers.",
     "Aは制限用法で「彼には教師をしている娘が2人いる」。教師ではない娘がほかにいる可能性がある。Bは非制限用法で「彼には娘が2人いて、2人とも教師だ」。娘は2人だけで、その2人について補足説明している。"),
    ("This is the town where I lived.", "This is the town which I visited.",
     "Aの I lived は live が自動詞で完全な文なので関係副詞 where を使い「ここは私が住んでいた町だ」。Bの I visited は visit が他動詞で目的語が欠けた不完全な文なので関係代名詞 which を使い「ここは私が訪れた町だ」。先行詞は同じ場所でも、後ろの文の形で関係詞が変わる。"),
    ("What he said was true.", "That he said so was true.",
     "Aの what は先行詞を含む関係代名詞で、he said は目的語が欠けた不完全な文。「彼が言ったこと（内容）は本当だった」。Bの that は接続詞で、he said so は完全な文。「彼がそう言ったということ（事実）は本当だった」。"),
    ("The students, who studied hard, passed the exam.", "The students who studied hard passed the exam.",
     "Aは非制限用法で「その学生たちは（全員）一生懸命勉強し、試験に合格した」。Bは制限用法で「一生懸命勉強した学生たちが試験に合格した」。勉強しなかった学生はほかにいて、その人たちは合格しなかった可能性がある。"),
    ("Whoever comes will be welcome.", "Whoever comes, don't open the door.",
     "Aの Whoever comes は文の主語になる名詞節（＝Anyone who comes）で「来る人はだれでも歓迎される」。Bの Whoever comes は譲歩の副詞節（＝No matter who comes）で「だれが来ても、ドアを開けてはいけない」。"),
    ("This is how he solved it.", "This is why he solved it.",
     "Aの how は方法を表す関係副詞で「このようにして彼はそれを解いた」。Bの why は理由を表す関係副詞で「こういうわけで彼はそれを解いた（これが彼がそれを解いた理由だ）」。"),
    ("Whatever you say, I won't change my mind.", "I'll do whatever you say.",
     "Aの whatever は譲歩の副詞節（＝No matter what）で「あなたが何を言おうと、私は考えを変えない」。Bの whatever は do の目的語になる名詞節（＝anything that）で「あなたの言うことは何でもします」。"),
    ("I'll never forget the day when we met.", "I'll never forget the day which we spent together.",
     "Aの we met は完全な文なので関係副詞 when を使い「私たちが出会った日を決して忘れない」。Bの we spent together は spend の目的語が欠けた不完全な文なので関係代名詞 which を使い「私たちが一緒に過ごした日を決して忘れない」。"),
]


@gen("thinking_writing", 4, ["written_reasoning", "concept"])
def explain_difference(r):
    a, b, model = r.choice(PAIRS)
    return desc(f"次の2つの英文A・Bの意味の違いを、関係詞（または接続詞）の働きに触れながら日本語で説明しなさい。\nA：{a}\nB：{b}", model,
                "関係詞は、後ろの文が完全か不完全か、コンマがあるか、名詞節か副詞節かによって、種類と意味が変わる。",
                [("Aの関係詞の働きを正しく説明している", 3), ("Bの関係詞の働きを正しく説明している", 3), ("A・Bの和訳がそれぞれ正しい", 2)], d=4, p=8, lines=6,
                ap="A・Bで違う部分（関係詞の種類・コンマの有無・節の位置）に下線を引き、後ろの文の形と、節が文の中で果たす働きを比べる。",
                steps=["A・Bで形の違う部分を特定する。", "それぞれの関係詞の後ろの文が完全か不完全か、節が名詞・形容詞・副詞のどの働きかを確認する。", "和訳を示しながら違いを説明する。"],
                alt=["それぞれの文を2文に分けたり、anyone who / no matter what などに言いかえたりして違いを示す方法もある。"],
                pc=[("Aの説明", 3), ("Bの説明", 3), ("和訳", 2)],
                pit=["和訳だけを書き、関係詞の働きという根拠を示さない。", "制限用法と非制限用法の違いを「コンマがあるかどうか」だけで説明し、意味の違いを書かない。"])


# (日本語, 答え, 説明)
TRANS = [
    ("ここは私が生まれた病院だ。", "This is the hospital where I was born.（This is the hospital in which I was born. も可）",
     "I was born は完全な文なので、場所の先行詞 the hospital に関係副詞 where を続ける。"),
    ("彼女が言ったことは本当だった。", "What she said was true.", "先行詞がなく、said の目的語が欠けているので、先行詞を含む what を使う。"),
    ("私には兄が1人いて、彼は東京で働いている。", "I have a brother, who works in Tokyo.", "兄は1人だけで、その兄について補足説明するので非制限用法 , who を使う。"),
    ("彼が会議に来なかった理由はだれも知らない。", "Nobody knows the reason why he didn't come to the meeting.（the reason を省いて why ... だけにしてもよい）",
     "he didn't come to the meeting は完全な文で、先行詞が the reason なので関係副詞 why を使う。"),
    ("何を食べても、彼は太らない。", "Whatever he eats, he doesn't gain weight.（No matter what he eats, ... も可）", "eats の目的語が欠けており「何を～しても」の譲歩なので whatever を使う。"),
    ("雨が降り始めたが、それは私たちが予想していたことだった。", "It began to rain, which we had expected.", "前の文全体（雨が降り始めたこと）を受けるので非制限用法 , which を使う。expected の目的語が欠けている。"),
    ("私は祖母が若いころ住んでいた家を訪ねた。", "I visited the house where my grandmother lived when she was young.（which my grandmother lived in も可）",
     "my grandmother lived は完全な文（live は自動詞）なので、関係副詞 where を使う。"),
]


@gen("thinking_writing", 3, ["cross_unit", "written_reasoning"], rel=["HS-ENG-U10", "JH-ENG-G3-U03"])
def translate_relative(r):
    jp, ans, why_s = r.choice(TRANS)
    return desc(f"次の日本語を、関係詞を使って英語に直しなさい。また、その関係詞を選んだ理由を、関係詞の後ろの文の形（完全か不完全か）や用法に触れて説明しなさい。\n{jp}",
                f"{ans}　{why_s}", f"英作文で名詞を説明するときは、関係詞の後ろの文が完全か不完全か、補足説明かどうかを確かめて関係詞を選ぶ。{why_s}",
                [("関係詞を使った英文を正しく書いている", 4), ("関係詞を選んだ理由を、後ろの文の形・用法から説明している", 3), ("時制・語順などその他の部分が正しい", 1)], d=4, p=8, lines=5,
                ap="日本語を「説明される名詞（先行詞）」と「説明の部分」に分け、説明の部分を英文にしたときに名詞が欠けるかどうかで関係詞を決める。",
                steps=["先行詞と説明の部分を分ける。", "説明の部分を英文にし、名詞が欠けるか（不完全か）を確かめる。", "補足説明・前の文全体・譲歩などの用法を判断する。", f"答え：{ans}"],
                alt=["2文に分けた英文（This is the hospital. I was born there. など）を作ってから、関係詞でつなぐ手順で確かめる。"],
                pc=[("関係詞を使った英文", 4), ("関係詞を選んだ理由", 3), ("その他の正確さ", 1)],
                pit=["先行詞が場所なので where と決めつけ、目的語が欠けているのに where を使う。", "補足説明なのにコンマを落とす。"])


# (英文, 答え, 別解, 説明)
PREPW = [
    ("This is the village where my father was born.", "This is the village in which my father was born.", ["This is the village which my father was born in."],
     "where は「in the village」を表しているので、in which に書きかえられる。"),
    ("I remember the year when the Olympic Games were held in our city.", "I remember the year in which the Olympic Games were held in our city.", [],
     "when は「in the year」を表しているので、in which に書きかえられる（年の前置詞は in）。"),
    ("Do you know the reason why she cried?", "Do you know the reason for which she cried?", [], "why は「for the reason」を表しているので、for which に書きかえられる。"),
    ("This is the room where we have meetings.", "This is the room in which we have meetings.", ["This is the room which we have meetings in."],
     "where は「in the room」を表しているので、in which に書きかえられる。"),
    ("Monday is the day when I'm busiest.", "Monday is the day on which I'm busiest.", [], "when は「on the day」を表しているので、on which に書きかえられる（日の前置詞は on）。"),
    ("This is the station where I change trains.", "This is the station at which I change trains.", ["This is the station which I change trains at."],
     "where は「at the station」を表しているので、at which に書きかえられる。"),
]


@gen("thinking_writing", 3, ["written_reasoning", "condition_check"])
def adverb_to_prep(r):
    s, ans, v, why_s = r.choice(PREPW)
    return desc(f"次の英文の関係副詞を「前置詞＋which」に書きかえなさい。また、なぜそのように書きかえられるのかを、前置詞を選んだ理由とともに説明しなさい。\n{s}",
                f"{ans}　{why_s}", f"関係副詞は「前置詞＋which」と同じ働きをする。前置詞は、先行詞を2文目に戻したときに必要な前置詞（in the village / on the day など）で決まる。{why_s}",
                [("前置詞＋which を使った英文を正しく書いている", 4), ("関係副詞＝前置詞＋which の関係を説明している", 2), ("前置詞を選んだ理由を説明している", 2)], d=4, p=8, lines=5,
                ap="関係副詞の文を2文に分け、先行詞を2文目に戻すとどの前置詞が必要になるかを考える。",
                steps=["先行詞を2文目に戻した文を作る（My father was born in the village. など）。", "そこで使った前置詞を which の前に置く。", f"答え：{ans}"],
                alt=["前置詞を文末に残した形（which ... in）でも書けることを確かめる。"],
                pc=[("前置詞＋which の英文", 4), ("関係副詞との関係の説明", 2), ("前置詞の選択理由", 2)],
                pit=["前置詞の後ろに that を置く（in that）。", "日・年・場所に合わない前置詞を使う（in Monday など）。"], v=v)


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(task, wrong, step, etype, tempt, fix, ans, expl, steps, ap, alt, pit, d=3):
    return desc(f"{task}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい英文に書き直しなさい。", ans, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい英文に直している", 3), ("文法の規則を説明している", 1)], d=d, p=6, lines=5,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい英文", 3), ("規則の説明", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix))


# (和文, 誤答, 正答, 誤りの箇所, 種類, 規則, 誤りやすい理由)
CHOICE_ERR = [
    ("私が欲しいものはこの本だ。", "The thing what I want is this book.", "What I want is this book.", "The thing what", "concept",
     "what は先行詞を含むので、前に The thing を置かない（The thing that I want is this book. も可）。", "「もの」を The thing で表し、さらに関係代名詞 what を続けた。"),
    ("これは私が昨日買ったかばんだ。", "This is the bag what I bought yesterday.", "This is the bag which I bought yesterday.", "what", "concept",
     "先行詞 the bag があるので what は使えない。目的格の関係代名詞 which（that、または省略）を使う。", "「買ったもの」の「もの」から what を連想した。"),
    ("ここは私が生まれた町だ。", "This is the town which I was born.", "This is the town where I was born.", "which", "condition",
     "I was born は完全な文なので関係副詞 where を使う（which を使うなら in which / which ... in）。", "先行詞が名詞なので関係代名詞を使えばよいと考えた。"),
    ("私たちは昨年訪れた博物館にもう一度行った。", "We went again to the museum where we visited last year.", "We went again to the museum which we visited last year.", "where", "condition",
     "visited は他動詞で目的語が欠けているので、関係代名詞 which（that）を使う。", "先行詞が場所なので where を使えばよいと考えた。"),
    ("彼の言ったことはすべて本当だった。", "All what he said was true.", "All that he said was true.", "All what", "concept",
     "what は先行詞を含むので all の後ろには置けない。all を先行詞とする関係代名詞 that を使う（What he said was all true. も可）。", "「言ったこと」を what で表し、「すべて」の all を前に足した。"),
    ("これが、私がその問題を解いた方法だ。", "This is the way how I solved the problem.", "This is how I solved the problem.", "the way how", "notation",
     "the way と how は並べて使わない（This is the way I solved the problem. も可）。", "「方法」の the way と、方法を表す how の両方を書いた。"),
    ("彼が遅れた理由を教えて。", "Tell me the reason which he was late.", "Tell me the reason why he was late.", "which", "condition",
     "he was late は完全な文なので、関係副詞 why（または for which）を使う。", "先行詞 the reason があるので関係代名詞 which を使った。"),
    ("これは私が住んでいる家だ。", "This is the house which I live.", "This is the house where I live.", "which", "condition",
     "live は自動詞で I live は完全な文なので、関係副詞 where を使う（which I live in も可）。", "live を他動詞のように考え、目的語が欠けていると判断した。"),
]


@gen("error_correction", 4, ["common_error", "condition_check"])
def err_choice(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(CHOICE_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", etype, tempt, fix, fix, f"{rule}正しくは {fix}",
                    ["先行詞があるかどうかを確認する。", "関係詞の後ろの文が完全か不完全かを確認する。", f"正しい英文：{fix}"],
                    "関係詞は、①後ろの文が完全か不完全か、②先行詞があるか、の2点で選ぶ。日本語の「もの」「場所」などの言葉だけで決めない。",
                    ["関係詞の部分を2文に分けて書き、先行詞が2文目でどんな働き（目的語・副詞）をしているかを確かめる。"],
                    ["先行詞が場所なら where、「もの」なら what と機械的に決める。"], d=3)


# (和文, 誤答, 正答, 誤りの箇所, 種類, 規則, 誤りやすい理由)
NONR_ERR = [
    ("彼は試験に落ちたが、そのことは私たちを驚かせた。", "He failed the exam, that surprised us.", "He failed the exam, which surprised us.", "that", "concept",
     "非制限用法（コンマの後ろ）に that は使えない。前の文全体を受けるのは , which。", "関係代名詞 which と that はいつでも置きかえられると考えた。"),
    ("彼女はそう言ったが、それはうそだった。", "She said so, it was a lie.", "She said so, which was a lie.", "it", "logic",
     "2つの文を接続詞なしにコンマだけでつなぐことはできない。前の文全体を受ける , which を使う（She said so, but it was a lie. も可）。", "日本語の「それは」をそのまま it にした。"),
    ("私は京都を訪れ、そこで古い友人に会った。", "I visited Kyoto, which I met an old friend.", "I visited Kyoto, where I met an old friend.", "which", "condition",
     "I met an old friend は完全な文なので、関係副詞 where を使う。", "先行詞が固有名詞なので , which を使えばよいと考えた。"),
    ("私の父は写真が好きで、毎週末写真を撮りに出かける。", "My father, that likes photography, goes out to take pictures every weekend.", "My father, who likes photography, goes out to take pictures every weekend.", "that", "concept",
     "非制限用法に that は使えない。先行詞が人なので , who を使う。", "先行詞が人でも that が使えることから、非制限用法でも使えると考えた。"),
    ("横浜は港町で、外国との貿易の長い歴史がある。", "Yokohama, where is a port city, has a long history of foreign trade.", "Yokohama, which is a port city, has a long history of foreign trade.", "where", "condition",
     "is の主語が欠けているので、関係副詞ではなく主格の関係代名詞 which を使う。", "先行詞が地名なので where を使えばよいと考えた。"),
    ("彼にはカナダに住んでいる娘が1人いる。", "He has a daughter, whom lives in Canada.", "He has a daughter, who lives in Canada.", "whom", "notation",
     "lives の主語が欠けているので、目的格の whom ではなく主格の who を使う。", "whom の方が改まった形なので、正しいと考えた。"),
]


@gen("error_correction", 3, ["common_error", "written_reasoning"])
def err_nonrestrictive(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(NONR_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", etype, tempt, fix, fix, rule,
                    ["コンマの後ろの関係詞（非制限用法）であることを確認する（that は不可）。", "後ろの文に欠けている要素（主語・目的語・なし）を確かめて関係詞を決める。", f"正しい英文：{fix}"],
                    "非制限用法では that と what は使えない。後ろの文が完全か不完全か、主格か目的格かも確かめる。",
                    ["関係詞の部分を「and＋代名詞（and he / and it / and there）」に置きかえて、意味と文の形が成り立つかを確かめる。"],
                    ["非制限用法に that を使う。", "コンマだけで2つの文をつなぐ。"], d=3)


# (和文, 誤答, 正答, 誤りの箇所, 種類, 規則, 誤りやすい理由)
COMP_ERR = [
    ("どんなに疲れていても、宿題をしなさい。", "However you are tired, do your homework.", "However tired you are, do your homework.", "However you are tired", "notation",
     "however（どんなに～でも）の直後には形容詞・副詞を置く。", "No matter how you are tired のように、how の後ろに S＋V をそのまま続けた。"),
    ("何が起ころうと、私はあなたの味方だ。", "Whatever happen, I'm on your side.", "Whatever happens, I'm on your side.", "happen", "notation",
     "whatever が節の主語になっており、3人称単数として扱うので happens にする。", "whatever の後ろの動詞の主語を意識しなかった。"),
    ("だれがそう言っても、私は信じない。", "Whatever says so, I won't believe it.", "Whoever says so, I won't believe it.", "Whatever", "concept",
     "そう言うのは人なので、whoever（＝No matter who）を使う。", "「だれが～しても」と「何が～しても」を取り違えた。"),
    ("来たい人はだれでも来てよい。", "Anyone whoever wants to come can come.", "Whoever wants to come can come.", "Anyone whoever", "concept",
     "whoever は anyone who の意味を1語で表すので、前に anyone を置かない（Anyone who wants to come can come. も可）。", "「だれでも」を Anyone で表し、さらに whoever を続けた。"),
    ("どこへ行っても、このカードを持っていなさい。", "However you go, carry this card with you.", "Wherever you go, carry this card with you.", "However", "concept",
     "「どこへ～しても」は場所を表す wherever を使う。however は「どんなに～しても」。", "-ever がつけば同じように使えると考えた。"),
    ("好きなときにいつでも電話してね。", "Call me whatever you like.", "Call me whenever you like.", "whatever", "concept",
     "「～するときはいつでも」は whenever を使う。whatever は「～するものは何でも」。", "you like の目的語が欠けていると考え、whatever を使った。"),
]


@gen("error_correction", 3, ["common_error", "concept"])
def err_compound(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(COMP_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", etype, tempt, fix, fix, rule,
                    ["日本語から、人・もの・時・場所・程度のどれを表すかを判断する。", "複合関係詞の後ろの形（however＋形容詞・副詞、主語の数など）を確かめる。", f"正しい英文：{fix}"],
                    "複合関係詞は whoever（人）・whatever（もの）・whenever（時）・wherever（場所）・however（程度）を意味で使い分け、however の直後には形容詞・副詞を置く。",
                    ["no matter who / what / when / where / how に言いかえて、意味と形が合うかを確かめる。"],
                    ["-ever の種類を取り違える。", "however の後ろに S＋V をそのまま続ける。"], d=3)


GENERATORS = [what_or_not, adverb_or_pronoun, nonrestrictive, compound_relative,
              combine, prep_relative, build_order, what_idiom,
              explain_difference, translate_relative, adverb_to_prep,
              err_choice, err_nonrestrictive, err_compound]
