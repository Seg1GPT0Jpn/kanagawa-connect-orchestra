"""単元パック：英語コミュニケーションⅠ 時制（現在・過去・未来、完了形、時・条件の副詞節）。"""
from banks._common import desc, mc, order, sa
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem,
                         tp)

UNIT_ID = "HS-ENG-U02"

# ======================================================================
# 授業プリント
# ======================================================================

LESSON = lesson(
    goals=["現在・過去・未来の基本時制と、進行形・完了形・完了進行形の意味の違いを、基準となる時点を使って説明できる。",
           "過去完了・未来完了を、2つの出来事の前後関係や「基準時までに」の意味から正しく使い分けられる。",
           "時・条件を表す副詞節では未来のことも現在形で表すこと、名詞節では will を使うことを判断できる。"],
    duration=50,
    readiness=["規則動詞・不規則動詞の過去形と過去分詞を言える（中学1・2年）。", "現在完了（継続・経験・完了）の基本の形と意味を知っている（中学3年）。",
               "will と be going to で未来を表せる（中学2年）。"],
    flow=[("導入：日本語の「た」と英語の時制", 5, "「宿題はもう終わった」と「昨日宿題を終えた」の英訳を比べ、同じ「た」でも英語では形が変わることに気づかせる"),
          ("時制の全体像と現在完了", 12, "基準時の考え方で12の形を整理し、現在完了と過去形の違いを時間軸の図で示す"),
          ("過去完了・未来完了", 15, "基準時を過去・未来に移すと完了形がどう変わるかを導出し、例題1・2を解く"),
          ("時・条件の副詞節", 12, "If it rains tomorrow と I don't know if it will rain を比べ、副詞節と名詞節を見分ける（例題3）"),
          ("まとめと確認", 6, "確認問題3問、問題プリントA の課題指示")],
    sections=[
        intro("in1", "日本語の「た」と英語の時制",
              "日本語では「昨日宿題を終えた」も「宿題はもう終わった」も同じ「た」で表す。しかし英語では、前者は I finished my homework yesterday.（過去形）、後者は I have already finished my homework.（現在完了）となる。英語の時制は「いつの出来事か」だけでなく、「どの時点から見ているか（基準時）」と「その時点でどんな状態か」を動詞の形で表し分ける仕組みである。",
              bullets=["過去形：過去の出来事を、現在とは切り離して述べる。", "現在完了：過去の出来事を、現在の状態（もう終わっている・経験がある・ずっと続いている）と結びつけて述べる。",
                       "基準時を過去や未来に移すと、過去完了・未来完了になる。"],
              points=[tp("2つの日本語を英訳させ、出てきた英文を板書して比べさせる。", ask="どちらも「た」なのに、なぜ英語では形が違うのか。",
                         expect="一方は昨日という過去の時点の話、もう一方は今の状態の話だから。", timing="導入の冒頭"),
                      tp("時制は「時間の位置」と「見方（進行・完了）」の組み合わせであることを、最初に時間軸の図で示す。")]),
        definition("df1", "時制の全体像（基準時と相）",
                   "英語の動詞は、基準時が現在・過去・未来のどれか（時制）と、その時点での見方（単純・進行・完了・完了進行）の組み合わせで、12の形をとる。",
                   bullets=["単純形：do ／ did ／ will do（事実・習慣・1回の出来事）", "進行形：be doing（基準時に進行中の動作）",
                            "完了形：have done ／ had done ／ will have done（基準時までの完了・経験・継続）", "完了進行形：have been doing ／ had been doing ／ will have been doing（基準時まで続いている動作）"],
                   conditions=["know, like, belong, resemble など状態を表す動詞は、ふつう進行形にしない（継続は現在完了で表す）。",
                               "現在完了は基準時が現在なので、yesterday, last year, ～ ago, when I was a child, What time ～? など過去の一時点を特定する語句とは使えない。"],
                   points=[tp("12の形を表にまとめ、縦軸を「現在・過去・未来」、横軸を「単純・進行・完了・完了進行」にして整理させる。", caution="表を暗記させるのではなく、「基準時はいつか」を毎回問う習慣をつける。")]),
        theorem("th1", "完了形と時・条件の副詞節の規則",
                "現在完了 have＋過去分詞（基準時＝現在） ／ 過去完了 had＋過去分詞（基準時＝過去のある時点） ／ 未来完了 will have＋過去分詞（基準時＝未来のある時点）",
                ["過去完了は、過去の基準時より前に起きたこと（大過去）や、その時点までの完了・経験・継続を表す。",
                 "未来完了は、未来の基準時（by next week など）までの完了・経験・継続を表す。",
                 "when, if, until, as soon as, by the time, unless などが導く時・条件の副詞節では、未来のことも現在形（未来完了の内容は現在完了）で表す。",
                 "一方、know, wonder などの目的語になる if / when の節（名詞節）では、未来のことは will で表す。"],
                body="副詞節の規則は「主節の will がすでに未来を示しているので、従属節では時を重ねて示さない」と理解しておくとよい。",
                points=[tp("副詞節か名詞節かは、その節を取り除いても文が成り立つか（副詞節）、動詞の目的語になっているか（名詞節）で判断させる。",
                           ask="I don't know if it will rain. の if 節を取り除くと、文は成り立つか。", expect="I don't know. だけでは know の目的語がなくなる。if 節は名詞節。")]),
        derivation("dv1", "なぜ現在完了は yesterday と一緒に使えないのか",
                   ["① 現在完了 have＋過去分詞の have は現在形である。つまり、この形は「現在」に立って過去とのつながりを述べる形である。",
                    "② I have lost my key. は「（過去に）なくして、今も持っていない」という現在の状態を伝えている。",
                    "③ yesterday は「昨日」という過去の一時点を指定する語であり、基準を過去に置く。",
                    "④ 基準を現在に置く現在完了と、基準を過去の一点に置く yesterday は矛盾する。したがって I have lost my key yesterday. は誤りで、I lost my key yesterday. とする。",
                    "⑤ 同じ考え方で、基準時を過去に移せば had＋過去分詞（過去完了）、未来に移せば will have＋過去分詞（未来完了）が得られる。"],
                   body="for three years や since 2020 は「現在までの期間・起点」を表すので現在完了と矛盾しない。three years ago は「現在から3年さかのぼった一点」なので矛盾する。",
                   points=[tp("「基準時」と「出来事の時」を時間軸上に別々の印で書き、現在完了では基準時が現在にあることを図で確認させる。", timing="手順④の説明時")]),
        example("ex1", "例題1　過去完了（大過去）",
                "（　）内の動詞を適切な形にしなさい。When I got to the station, the last train (already leave).",
                ["基準時は「駅に着いた」という過去の時点。", "電車が出たのは、その基準時より前。", "過去の基準時より前のことは had＋過去分詞で表す。"],
                "had already left",
                thinking="2つの過去の出来事のうち、どちらが先に起きたかを時間軸に書いて確かめる。",
                points=[tp("has already left と答える誤りに対して、「基準時が現在ではなく過去（got to the station）である」ことを確認させる。")],
                misconceptions=[("has already left とする", "基準時が過去（got）なので現在完了は使えない。had already left")]),
        example("ex2", "例題2　未来完了",
                "日本語に合うように英文を完成させなさい。「来年の3月で、私はこの町に10年住んだことになる。」　By next March, I (　　) in this town for ten years.",
                ["基準時は next March という未来の時点。", "その時点までの継続を表すので完了形。", "基準時が未来なので will have＋過去分詞。"],
                "will have lived（will have been living も可）",
                thinking="by ～ が「～までに」と期限を表しているので、その時点までの継続・完了を考える。",
                points=[tp("by（～までに）と until（～までずっと）の違いにも触れ、by は完了形と相性がよいことを確認する。")]),
        example("ex3", "例題3　時・条件の副詞節と名詞節",
                "（　）内から適切なものを選びなさい。(1) If it (rains / will rain) tomorrow, the game will be canceled.　(2) I don't know if it (rains / will rain) tomorrow.",
                ["(1) if 節は「もし～なら」と条件を表し、取り除いても the game will be canceled. が成り立つので副詞節。未来でも現在形。",
                 "(2) if 節は know の目的語（「～かどうか」）なので名詞節。未来のことは will で表す。"],
                "(1) rains　(2) will rain",
                thinking="if 節が「もし～なら」（副詞節）か「～かどうか」（名詞節）かを、取り除けるかどうかで判断する。",
                points=[tp("if を「もし」「かどうか」と訳し分けさせ、訳と時制の形を対応させる。", ask="(2) の if を「もし」と訳すと意味が通るか。", expect="通らない。「明日雨が降るかどうか」になる。")]),
        board("bd1", "板書案",
              [("① 基準時で考える", ["現在完了：基準＝今", "過去形：過去の一点（yesterday, ago）", "× have lost ～ yesterday", "○ lost ～ yesterday", "for / since は現在完了 OK"]),
               ("② 基準を動かす", ["過去完了 had＋p.p.：過去の基準より前", "When I got there, the train had left.", "未来完了 will have＋p.p.：未来の基準まで", "By next March, I will have lived ～."]),
               ("③ 副詞節と名詞節", ["副詞節（時・条件）：未来でも現在形", "If it rains tomorrow, ～", "名詞節（know の目的語）：will", "I don't know if it will rain."])],
              points=[tp("①②は時間軸の図とセットで板書する。③は副詞節・名詞節の判定方法（取り除けるか）を赤で書き添える。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("時制の問題では、必ず「基準時はいつか」を最初に言わせる。", ask="この文の基準時は現在・過去・未来のどれか。"),
               tp("状態動詞（know, have「持っている」, belong など）を進行形にする誤りには、継続は現在完了で表すことを示す。", caution="「～している」という日本語につられて進行形にしやすい。"),
               tp("has gone to（行ってしまって今いない）と has been to（行ったことがある）の違いを、主語が今ここにいるかどうかで確認させる。"),
               tp("副詞節の規則は「when / if があれば現在形」と機械的に覚えると名詞節で誤る。節の働きで判断させる。", timing="例題3の後"),
               tp("問題プリント D の誤答例を使い、「現在完了＋過去の一時点」の誤りが英作文で最も多いことを示す。")],
              misconceptions=[("I have visited Kyoto last year.", "last year は過去の一時点なので過去形。I visited Kyoto last year."),
                              ("If it will rain tomorrow, I'll stay home.", "条件の副詞節では未来でも現在形。If it rains tomorrow, ～"),
                              ("I am knowing him for ten years.", "know は状態動詞で、継続は現在完了。I have known him for ten years.")]),
        summary("sm1", "まとめ",
                ["時制は「基準時（現在・過去・未来）」と「見方（単純・進行・完了・完了進行）」の組み合わせで決まる。",
                 "現在完了は基準が今なので、過去の一時点を示す語句とは使えない。基準を過去・未来に移すと過去完了・未来完了。",
                 "時・条件の副詞節では未来でも現在形、know / wonder などの目的語になる名詞節では will。"]),
        check("ck1", "確認問題",
              [("I (lose) my wallet, so I can't buy anything now. の（　）内を適切な形にしなさい。", "have lost（今も持っていないという現在の結果）"),
               ("By the time you come back, I (finish) the report. の（　）内を適切な形にしなさい。", "will have finished（未来の基準時までの完了）"),
               ("Let's start when he (come) back. の（　）内を適切な形にしなさい。", "comes（時の副詞節なので未来でも現在形）")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

FORMS = [
    ("Water (boil) at 100 degrees Celsius.", "boils", [], "いつでも成り立つ一般的な事実は現在形で表す。"),
    ("I (read) this book three times so far.", "have read", [], "so far（今までに）と回数があるので、経験を表す現在完了。"),
    ("When I got to the station, the train (already leave).", "had already left", [], "過去の基準時（got to the station）より前に完了していたので過去完了。"),
    ("She (study) in the library when I called her.", "was studying", [], "過去の基準時（電話したとき）に進行中だった動作なので過去進行形。"),
    ("By next April, I (live) in this town for ten years.", "will have lived", ["will have been living"], "未来の基準時（next April）までの継続なので未来完了。"),
    ("We (know) each other since we were children.", "have known", [], "since 以下から現在までの継続。know は状態動詞なので現在完了（進行形にしない）。"),
    ("It (rain) for three hours now. I hope it stops soon.", "has been raining", [], "3時間前から今も続いている動作なので現在完了進行形。"),
    ("My father usually (get) up at six.", "gets", [], "usually があり現在の習慣を表すので現在形。主語が三人称単数なので -s がつく。"),
    ("Look! The baby (smile) at you.", "is smiling", [], "Look! があり、今まさに進行中の動作なので現在進行形。"),
    ("I lost the watch my father (give) me.", "had given", [], "なくした（過去）時点より前にもらっていたので過去完了。"),
    ("If it (rain) tomorrow, the game will be canceled.", "rains", [], "条件を表す副詞節の中では、未来のことも現在形で表す。"),
    ("I'll call you as soon as I (finish) my homework.", "finish", ["have finished"], "時を表す副詞節（as soon as ～）の中では未来のことも現在形（完了の意味を強めるなら現在完了）。"),
    ("He (live) in Osaka when he was a child.", "lived", [], "when he was a child は過去の一時期を示すので過去形。現在完了は使えない。"),
    ("This time tomorrow, we (fly) over the Pacific.", "will be flying", [], "未来の基準時（明日の今ごろ）に進行中の動作なので未来進行形。"),
    ("I (lose) my key, so I can't open the door now.", "have lost", [], "なくした結果、今もドアを開けられないという現在の状態を表すので現在完了。"),
    ("The museum (open) at nine every morning.", "opens", [], "every morning があり、毎日くり返されることなので現在形。主語が三人称単数なので -s がつく。"),
]


@gen("basic_check", 5, ["computation"])
def verb_form(r):
    s, ans, v, why = r.choice(FORMS)
    return sa(f"（　）内の動詞を適切な形に直しなさい。2語以上になってもよい。\n{s}", ans, why, d=1, v=v,
              ap="まず基準時（現在・過去・未来）を時を表す語句から決め、次にその時点での見方（単純・進行・完了）を決める。",
              steps=["時を表す語句・文脈から基準時を決める。", "基準時に進行中か、基準時までの完了・経験・継続か、単なる事実・習慣かを判断する。", f"形を決める：{ans}。"],
              alt=["答えの形を時間軸の図にかき、出来事の時と基準時の関係が文の意味と合うかを確かめる。"],
              pc=[("基準時を正しく判断している", 1), ("正しい動詞の形を答えている", 1)],
              pit=["現在完了と過去を表す語句を一緒に使う。", "時・条件の副詞節の中で will を使う。", "三人称単数現在の -s を落とす。"])


BASIC = [
    ("Look! The children (　　) in the pool.", "are swimming",
     [("swim", "現在形は習慣や一般的な事実を表す。Look! は「今まさに」進行中の動作を示すので進行形。"),
      ("swam", "過去形では「今」見ている場面と合わない。"),
      ("have swum", "現在完了は完了・経験・継続を表し、目の前で進行中の動作には使わない。")]),
    ("My brother usually (　　) to school by bike.", "goes",
     [("go", "主語 My brother は三人称単数なので、現在形には -es が必要。"),
      ("is going", "現在進行形は一時的な動作を表す。usually が示す習慣は現在形で表す。"),
      ("has gone", "has gone は「行ってしまって今いない」という結果を表し、usually（ふだん）とは合わない。")]),
    ("I (　　) Kyoto with my family last summer.", "visited",
     [("have visited", "last summer は過去の一時点を特定する語句なので、現在完了とは使えない。"),
      ("visit", "現在形では last summer（過去）と合わない。"),
      ("am visiting", "現在進行形では last summer（過去）と合わない。")]),
    ("She (　　) a letter when the phone rang.", "was writing",
     [("writes", "現在形では、過去の出来事（the phone rang）と時が合わない。"),
      ("has written", "現在完了は基準時が現在であり、過去の一時点（電話が鳴ったとき）の状況は表せない。"),
      ("is writing", "現在進行形では、過去の出来事（rang）と時が合わない。")]),
    ("We (　　) each other since we were in elementary school.", "have known",
     [("know", "since ～（～以来）は現在までの継続を表すので、現在形ではなく現在完了。"),
      ("knew", "過去形では「今も知り合いである」という現在までの継続が表せない。"),
      ("are knowing", "know は状態動詞なので、ふつう進行形にしない。")]),
    ("The earth (　　) around the sun.", "goes",
     [("went", "過去形では「今もそうである」という不変の事実が表せない。"),
      ("has gone", "現在完了は完了・結果を表し、いつでも成り立つ事実には使わない。"),
      ("go", "主語 The earth は三人称単数なので -es が必要。")]),
    ("I (　　) my homework yet. I need another hour.", "haven't finished",
     [("don't finish", "現在形の否定は習慣的に「終えない」の意味になり、yet（まだ）と合わない。"),
      ("am not finishing", "現在進行形の否定は「今終えつつあるのではない」となり、yet とともに未完了を表す形ではない。"),
      ("wasn't finishing", "過去進行形では、今の状態（まだ終わっていない）を表せない。")]),
    ("It (　　) heavily when I left home this morning.", "was raining",
     [("rains", "現在形では、過去の時点（left home）の様子が表せない。"),
      ("has rained", "現在完了は基準時が現在なので、過去の一時点の様子は表せない。"),
      ("is raining", "現在進行形では、過去の時点（left home）と時が合わない。")]),
    ("I (　　) a strange noise last night.", "heard",
     [("have heard", "last night は過去の一時点なので、現在完了とは使えない。"),
      ("hear", "現在形では last night（過去）と合わない。"),
      ("am hearing", "hear は知覚を表す状態動詞で、ふつう進行形にしない。また last night とも合わない。")]),
    ("This bag (　　) to my sister.", "belongs",
     [("is belonging", "belong は状態動詞なので、ふつう進行形にしない。"),
      ("belong", "主語 This bag は三人称単数なので -s が必要。"),
      ("are belonging", "belong は状態動詞で進行形にせず、主語とも数が一致しない。")]),
    ("He (　　) his room every Sunday.", "cleans",
     [("clean", "主語 He は三人称単数なので -s が必要。"),
      ("is cleaning", "現在進行形は今進行中の動作を表す。every Sunday の習慣は現在形で表す。"),
      ("cleaning", "動詞の ing 形だけでは述語動詞にならない。")]),
    ("When I was a child, I (　　) in Sendai.", "lived",
     [("have lived", "when I was a child は過去の一時期を特定するので、現在完了とは使えない。"),
      ("live", "現在形では過去の一時期のことが表せない。"),
      ("am living", "現在進行形では過去の一時期のことが表せない。")]),
    ("Where (　　) you go last weekend?", "did",
     [("have", "last weekend は過去の一時点で、現在完了は使えない。また have you go という形はない。"),
      ("do", "現在形では last weekend（過去）と合わない。"),
      ("are", "be 動詞と原形 go を組み合わせる形はない。")]),
    ("The new library (　　) to the public next month.", "will open",
     [("opened", "過去形では next month（未来）と合わない。"),
      ("has opened", "現在完了は基準時が現在であり、next month（未来）と合わない。"),
      ("had opened", "過去完了は過去の基準時より前を表し、next month と合わない。")]),
]


@gen("basic_check", 5, ["concept"])
def basic_tense(r):
    s, ok, wrongs = r.choice(BASIC)
    return mc(f"（　）に入る最も適切なものを選びなさい。\n{s}", [ok] + [w for w, _ in wrongs],
              f"{ok} が入る。時を表す語句・文脈から基準時と動作の見方を判断する。", d=1,
              ap="時を表す語句（last ～、since ～、every ～、Look! など）に印をつけ、基準時が現在・過去・未来のどれかを決める。",
              steps=["時を表す語句を探す。", "基準時と、動作の見方（習慣・進行中・完了・継続）を決める。", f"主語との一致も確かめて {ok} を選ぶ。"],
              alt=["選択肢を1つずつ入れて和訳し、時を表す語句と矛盾しないかを確かめる。"],
              pc=[("時を表す語句から基準時を判断している", 1), ("正しい形を選んでいる", 1)],
              pit=["現在完了と過去の一時点を表す語句を一緒に使う。", "状態動詞を進行形にする。"],
              why={w: (reason, "時制の意味・用法の混同") for w, reason in wrongs})


TIMEX = [
    ("I have seen this movie (　　).", "last week", ["twice", "before", "many times"], "I saw this movie last week."),
    ("She has lived in Kobe (　　).", "five years ago", ["since 2018", "for five years", "all her life"], "She moved to Kobe five years ago."),
    ("My father has been busy (　　).", "yesterday", ["lately", "since last month", "for a week"], "My father was busy yesterday."),
    ("I haven't seen Ken (　　).", "two days ago", ["for a long time", "since Monday", "recently"], "I saw Ken two days ago."),
    ("Kate has studied Japanese (　　).", "when she was in high school", ["for three years", "since she came to Japan", "since last spring"], "Kate studied Japanese when she was in high school."),
    ("We have known each other (　　).", "in 2015", ["since we were children", "for ten years", "for a long time"], "We became friends in 2015."),
    ("He has visited Nara (　　).", "last month", ["three times", "before", "once"], "He visited Nara last month."),
    ("It has been rainy (　　).", "the day before yesterday", ["since Monday", "for days", "all week"], "It was rainy the day before yesterday."),
    ("I have been to Okinawa (　　).", "in 2020", ["twice", "once", "before"], "I went to Okinawa in 2020."),
    ("My grandmother has been in the hospital (　　).", "last Friday", ["since last Friday", "for two weeks", "since the accident"], "My grandmother went into the hospital last Friday."),
    ("They have been married (　　).", "twenty years ago", ["for twenty years", "since 2005", "for a long time"], "They got married twenty years ago."),
]


def timex_ok_reason(x):
    if x.startswith("since"):
        return f"「{x}」は since＋起点で「～以来（今まで）」を表し、現在完了の継続と一緒に使える。"
    if x.startswith("for"):
        return f"「{x}」は for＋期間で「今までの～の間」を表し、現在完了の継続と一緒に使える。"
    if x in ("twice", "once", "three times", "many times", "before"):
        return f"「{x}」は回数・「以前に」を表し、現在完了の経験と一緒に使える。"
    return f"「{x}」は現在を含む期間（最近・これまでずっと）を表し、現在完了と一緒に使える。"


@gen("basic_check", 5, ["condition_check", "concept"])
def time_expression(r):
    s, ng, oks, past = r.choice(TIMEX)
    return mc(f"次の英文の（　）に入れることができないものを1つ選びなさい。\n{s}", [ng] + oks,
              f"「{ng}」は過去の一時点を特定する語句なので、基準時が現在の現在完了とは一緒に使えない。この語句は過去形の文で使う（例：{past}）。", d=2,
              ap="現在完了は「今」を基準にした表現なので、過去の一時点（～ ago、last ～、yesterday、in＋過去の年、when ～ was …）を示す語句とは使えない。",
              steps=["英文が現在完了であることを確認する。", "選択肢を「現在までの期間・回数」と「過去の一時点」に分ける。", f"過去の一時点を示す「{ng}」を選ぶ。"],
              alt=["選択肢の語句に「今」が含まれているか（今までの期間か）、過去の点だけを指すかを、時間軸に印をつけて確かめる。"],
              pc=[("現在完了と過去の一時点の語句が両立しないことを理解している", 1), ("正しく選んでいる", 1)],
              pit=["since＋過去の起点（since last Friday）と、過去の一時点（last Friday）を混同する。"],
              why={x: (timex_ok_reason(x), "現在完了と共起できる語句の誤解") for x in oks})


CLAUSE = [
    ("Please wait here until I (　　) back.", "come", "副詞節（until ～）",
     [("will come", "until が導く時の副詞節の中では、未来のことも現在形で表す。"),
      ("came", "過去形では「これから戻ってくる」という未来の内容と合わない。"),
      ("would come", "would は過去から見た未来や仮定を表し、この文脈には合わない。")]),
    ("I don't know if it (　　) tomorrow.", "will rain", "名詞節（know の目的語）",
     [("rains", "if 節は know の目的語（「～かどうか」）の名詞節なので、未来のことは will で表す。"),
      ("rained", "過去形では tomorrow（未来）と合わない。"),
      ("has rained", "現在完了は基準時が現在であり、tomorrow と合わない。")]),
    ("If it (　　) tomorrow, we'll stay home.", "rains", "副詞節（条件）",
     [("will rain", "条件を表す副詞節の中では、未来のことも現在形で表す。"),
      ("rained", "過去形にすると仮定法（現実と違う仮定）になり、主節の will と合わない。"),
      ("would rain", "would は副詞節の中で未来を表す形ではない。")]),
    ("As soon as you (　　) at the airport, please call me.", "arrive", "副詞節（as soon as ～）",
     [("will arrive", "as soon as が導く時の副詞節の中では、未来のことも現在形で表す。"),
      ("arrived", "過去形では、これから着くという未来の内容と合わない。"),
      ("would arrive", "would は過去から見た未来や仮定を表し、この文脈には合わない。")]),
    ("By the time you (　　) home, dinner will be ready.", "get", "副詞節（by the time ～）",
     [("will get", "by the time が導く時の副詞節の中では、未来のことも現在形で表す。"),
      ("got", "過去形では、主節の will be ready（未来）と合わない。"),
      ("would get", "would は副詞節の中で未来を表す形ではない。")]),
    ("I'm not sure whether he (　　) the party next week.", "will join", "名詞節（sure の後ろの whether 節）",
     [("joins", "whether 節は「～かどうか」を表す名詞節なので、未来のことは will で表す。"),
      ("joined", "過去形では next week（未来）と合わない。"),
      ("has joined", "現在完了は基準時が現在であり、next week と合わない。")]),
    ("Unless it (　　) tomorrow, we will play soccer.", "rains", "副詞節（unless ～）",
     [("will rain", "unless（～しない限り）が導く条件の副詞節の中では、未来のことも現在形で表す。"),
      ("rained", "過去形では tomorrow（未来）と合わない。"),
      ("would rain", "would は副詞節の中で未来を表す形ではない。")]),
    ("I'll lend you this book after I (　　) it.", "have finished", "副詞節（after ～）",
     [("will finish", "after が導く時の副詞節の中では will を使わない。"),
      ("will have finished", "時の副詞節の中では、未来完了の内容は現在完了で表す。"),
      ("had finished", "過去完了は過去の基準時より前を表し、これからのことには使えない。")]),
    ("Nobody knows when the next big earthquake (　　).", "will happen", "名詞節（knows の目的語）",
     [("happens", "when 節は knows の目的語（「いつ～か」）の名詞節なので、未来のことは will で表す。"),
      ("happened", "過去形では「次の地震」という未来の内容と合わない。"),
      ("has happened", "現在完了は基準時が現在であり、未来の出来事は表せない。")]),
    ("Let's go out when the rain (　　).", "stops", "副詞節（when ～）",
     [("will stop", "when が「～したら」と時を表す副詞節の中では、未来のことも現在形で表す。"),
      ("stopped", "過去形では、これから出かけるという未来の内容と合わない。"),
      ("would stop", "would は副詞節の中で未来を表す形ではない。")]),
    ("I wonder if she (　　) my present tomorrow.", "will like", "名詞節（wonder の目的語）",
     [("likes", "if 節は wonder の目的語（「～かどうか」）の名詞節なので、未来のことは will で表す。"),
      ("liked", "過去形では tomorrow（未来）と合わない。"),
      ("has liked", "現在完了は基準時が現在であり、tomorrow と合わない。")]),
]


@gen("basic_check", 5, ["condition_check"])
def adverbial_clause(r):
    s, ok, kind, wrongs = r.choice(CLAUSE)
    return mc(f"（　）に入る最も適切なものを選びなさい。\n{s}", [ok] + [w for w, _ in wrongs],
              f"空所を含む節は{kind}。" + ("時・条件の副詞節なので未来でも現在形（完了の内容は現在完了）。" if "副詞節" in kind else "名詞節なので未来のことは will で表す。"), d=2,
              ap="空所を含む節が、取り除いても文が成り立つ副詞節（時・条件）か、動詞などの目的語になる名詞節かを判断する。",
              steps=["接続詞（if / when / until など）が導く節の範囲を確かめる。", f"その節の働きを判断する：{kind}。",
                     "副詞節なら未来でも現在形、名詞節なら未来は will。", f"{ok} を選ぶ。"],
              alt=["if を「もし～なら」と「～かどうか」、when を「～したら」と「いつ～か」と訳し分けて、どちらの意味が文に合うかで判断する。"],
              pc=[("節の種類（副詞節・名詞節）を判断している", 1), ("正しい形を選んでいる", 1)],
              pit=["when / if があればいつでも現在形にしてしまう（名詞節でも現在形にする）。"],
              why={w: (reason, "副詞節と名詞節の時制の混同") for w, reason in wrongs})


# ======================================================================
# B 標準演習
# ======================================================================

ADV = [
    ("When I got to the station, the last train (　　).", "had already left",
     [("has already left", "基準時は got to the station という過去の時点。現在完了は基準時が現在なので使えない。"),
      ("already leaves", "現在形では、過去の時点より前に出発していたことが表せない。"),
      ("will already leave", "未来の表現は、過去の場面と合わない。")]),
    ("I (　　) the novel by the time you come back.", "will have finished",
     [("have finished", "基準時は「あなたが戻ってくるとき」という未来の時点。現在完了は基準時が現在。"),
      ("had finished", "過去完了は過去の基準時より前を表し、未来の基準時には使えない。"),
      ("finish", "現在形では「未来のある時点までに終えている」という完了が表せない。")]),
    ("She (　　) for two hours when I finally arrived.", "had been waiting",
     [("has been waiting", "基準時は I arrived という過去の時点なので、現在完了進行形は使えない。"),
      ("is waiting", "現在進行形では、過去の時点までの継続が表せない。"),
      ("waits", "現在形では、過去の時点までの継続が表せない。")]),
    ("I lost the umbrella that my aunt (　　) me.", "had given",
     [("has given", "なくした（過去）時点より前のことなので、基準時が現在の現在完了は使えない。"),
      ("gives", "現在形では、過去の出来事より前のことが表せない。"),
      ("will give", "未来の表現では、すでになくした傘をもらった時点と合わない。")]),
    ("He (　　) in Tokyo for three years before he moved to Osaka.", "had lived",
     [("has lived", "基準時は moved to Osaka という過去の時点。現在完了は使えない。"),
      ("lives", "現在形では、過去の時点までの継続が表せない。"),
      ("will have lived", "未来完了は未来の基準時までのことを表し、過去の話には使えない。")]),
    ("This time next week, we (　　) on the beach in Okinawa.", "will be relaxing",
     [("have relaxed", "現在完了は基準時が現在で、next week の一時点の様子は表せない。"),
      ("had relaxed", "過去完了は過去の基準時より前を表し、未来の話には使えない。"),
      ("were relaxing", "過去進行形では next week（未来）と合わない。")]),
    ("I (　　) about you just now.", "was thinking",
     [("have thought", "just now（ついさっき）は過去の一時点を表すので、現在完了とは使えない。"),
      ("am thinking", "現在進行形は今進行中の動作を表し、just now（ついさっき）と合わない。"),
      ("think", "現在形は just now（過去）と合わない。")]),
    ("By next April, my sister (　　) in London for five years.", "will have lived",
     [("has lived", "基準時は next April という未来の時点。現在完了は基準時が現在。"),
      ("had lived", "過去完了は過去の基準時までのことを表す。"),
      ("lives", "現在形では未来の時点までの継続が表せない。")]),
    ("The ground was wet because it (　　) during the night.", "had rained",
     [("has rained", "基準時は was wet という過去の時点なので、現在完了は使えない。"),
      ("rains", "現在形では、過去の時点より前の出来事が表せない。"),
      ("will rain", "未来の表現は、地面がぬれていた原因（過去の出来事）と合わない。")]),
    ("She told me that she (　　) the book twice.", "had read",
     [("has read", "told（過去）の内容なので、時制の一致により現在完了は過去完了になる。"),
      ("reads", "現在形では「2回読んだことがある」という経験が表せない。"),
      ("will have read", "未来完了は未来の基準時までのことを表し、この文脈に合わない。")]),
    ("My father (　　) at the same company since he graduated from college.", "has worked",
     [("worked", "since ～ は現在までの継続を表すので、過去形ではなく現在完了。"),
      ("works", "現在形では、since ～ から今までの継続が表せない。"),
      ("had worked", "過去完了は過去の基準時までの継続を表す。この文には過去の基準時がない。")]),
    ("I'm tired because I (　　) for the exam since early this morning.", "have been studying",
     [("had been studying", "基準時は I'm tired という現在。過去完了進行形は過去の基準時までの継続。"),
      ("am studying", "現在進行形では、since ～ から今までの継続が表せない。"),
      ("studied", "過去形では、since ～ から今まで続いていることが表せない。")]),
]


@gen("standard_practice", 5, ["concept", "condition_check"])
def perfect_tense(r):
    s, ok, wrongs = r.choice(ADV)
    return mc(f"文脈に合うように、（　）に入る最も適切なものを選びなさい。\n{s}", [ok] + [w for w, _ in wrongs],
              f"{ok} が入る。基準時がいつか（現在・過去・未来）を決め、その時点までの完了・継続かどうかで形を選ぶ。", d=3,
              ap="文中のもう1つの出来事や時を表す語句（by ～、when ～、since ～）から基準時を決め、その基準時と出来事の前後関係を時間軸にかく。",
              steps=["基準時を表す語句・節を探す。", "空所の出来事が基準時より前か、基準時に進行中か、基準時まで続いているかを判断する。", f"{ok} を選ぶ。"],
              alt=["選択肢の形から基準時を逆算し（has＝現在、had＝過去、will have＝未来）、文中の時を表す語句と合うかを確かめる。"],
              pc=[("基準時を正しく判断している", 2), ("出来事との前後関係から正しい形を選んでいる", 2)],
              pit=["過去の基準時なのに現在完了を使う。", "by ～（～までに）を見落として未来完了を使わない。"],
              why={w: (reason, "完了形の基準時の誤解") for w, reason in wrongs})


USES = {
    "継続": ("継続（ずっと～している）", "for ～・since ～・How long ～? などとともに、状態や動作が今まで続いていることを表す"),
    "経験": ("経験（～したことがある）", "ever・never・before・回数（once, twice など）とともに、今までの経験を表す"),
    "完了": ("完了・結果（～してしまった・～したところだ）", "just・already・yet などとともに、動作が終わったことや、その結果の今の状態を表す"),
}
PERF = [
    ("I have lived in this town since I was born.", "継続"), ("We have known each other for ten years.", "継続"),
    ("It has been cold since last week.", "継続"), ("How long have you been in Japan?", "継続"), ("She has been sick in bed since Monday.", "継続"),
    ("I have visited Nara twice.", "経験"), ("Have you ever eaten natto?", "経験"), ("He has never seen snow.", "経験"),
    ("I have heard that song before.", "経験"), ("My sister has been to Australia three times.", "経験"),
    ("I have just finished my homework.", "完了"), ("The train has already left.", "完了"), ("Have you done the dishes yet?", "完了"),
    ("He has gone to London, so he isn't here now.", "完了"), ("I have lost my wallet, so I can't buy lunch.", "完了"), ("Spring has come.", "完了"),
]


@gen("standard_practice", 5, ["concept", "computation"])
def perfect_use(r):
    s, u = r.choice(PERF)
    keys = list(USES)
    return mc(f"次の英文の現在完了の用法として最も適切なものを選びなさい。\n{s}", [USES[k][0] for k in keys],
              f"{USES[u][1]}用法。この文は{USES[u][0]}にあたる。", d=2, keep=True, ai=keys.index(u),
              ap="現在完了と一緒に使われている語句（for / since、ever / never / 回数、just / already / yet）や、文の後半が示す今の状態に注目する。",
              steps=["現在完了の部分（have / has＋過去分詞）を確認する。", "一緒に使われている語句や文脈を確認する。", f"{USES[u][0]}と判断する。"],
              alt=["和訳して「ずっと～している」「～したことがある」「～してしまった（今は…）」のどれが自然かで確かめる。"],
              pc=[("手がかりとなる語句・文脈を見つけている", 2), ("用法を正しく判断している", 2)],
              pit=["has gone to（行ってしまった＝結果）と has been to（行ったことがある＝経験）を混同する。"],
              why={USES[k][0]: (f"{USES[k][0]}は{USES[k][1]}。この文はそれにあたらず、{USES[u][0]}である。", "現在完了の用法の手がかりの見落とし") for k in keys if k != u})


REWRITE = [
    ("Ken went to Canada. He is not here now.", "Ken (　)(　) to Canada.", "has gone", "行ってしまって今ここにいないという結果は has gone to で表す。"),
    ("It began to rain three hours ago. It is still raining.", "It (　)(　)(　) for three hours.", "has been raining", "3時間前から今も続いている動作なので現在完了進行形。"),
    ("I lost my umbrella. I don't have it now.", "I (　)(　) my umbrella.", "have lost", "なくした結果、今も持っていないことを現在完了（結果）で表す。"),
    ("This is my first visit to Kyoto.", "I have (　)(　) to Kyoto before.", "never been", "「初めての訪問」は「以前に行ったことがない」という経験の否定で表す。"),
    ("I have never seen such a beautiful sunset.", "This is the most beautiful sunset I (　)(　) seen.", "have ever", "「こんなに～なものは見たことがない」は「今まで見た中で最も～」と言いかえられる。"),
    ("I finished my homework, and then I had dinner.", "I (　)(　) my homework before I had dinner.", "had finished", "夕食を食べた（過去）より前に終えていたので過去完了。"),
    ("We became friends when we were ten. We are still friends.", "We (　)(　) friends since we were ten.", "have been", "10歳のときから今までの継続なので現在完了。"),
    ("I started reading this book this morning. I'm still reading it.", "I (　)(　)(　) this book since this morning.", "have been reading", "今朝から今も続いている動作なので現在完了進行形。"),
    ("Mr. Kato began teaching in 1990. He will retire in 2030.", "Mr. Kato (　)(　)(　) for forty years by 2030.", "will have taught", "2030年という未来の時点までの継続なので未来完了（will have been teaching も可だが空所は3つ）。"),
    ("Mika's grandfather died five years ago.", "Five years (　)(　) since Mika's grandfather died.", "have passed", "「亡くなってから5年が過ぎた」と、今までの時の経過を現在完了で表す。"),
    ("The concert started. Then we arrived at the hall.", "When we arrived at the hall, the concert (　)(　) started.", "had already", "ホールに着いた（過去）時点より前に始まっていたので過去完了。"),
    ("My brother went to Hokkaido last year. He went there again last month.", "My brother (　)(　) to Hokkaido twice.", "has been", "2回行ったことがあるという経験は has been to で表す（has gone to は結果）。"),
]


@gen("standard_practice", 5, ["computation", "application"])
def rewrite(r):
    src, frame, ans, why = r.choice(REWRITE)
    n = frame.count("(　)")
    return sa(f"上の英文とほぼ同じ意味になるように、下の英文の（　）に適切な語を1語ずつ入れなさい。\n{src}\n{frame}", ans, why, d=3,
              ap="元の文が表している「時」と「今の状態」を整理し、それを1文で表すにはどの時制（現在完了・過去完了・未来完了）が必要かを考える。",
              steps=["元の文の出来事を時間軸に並べる。", "書きかえ後の文の基準時（現在・過去・未来）を確かめる。", f"空所の数（{n}語）に合う形を決める：{ans}。"],
              alt=["書きかえた文を和訳し、元の文の和訳と同じ内容になっているかを確かめる。"],
              pc=[("適切な時制を判断している", 2), ("空所の語をすべて正しく入れている", 2)],
              pit=["has gone と has been の意味を取り違える。", "過去完了にすべきところを過去形のままにする。"])


ORD = [
    ("この町に住んでどのくらいになりますか。", ["how long", "have", "you", "lived", "in", "this town"], "?", "How long＋現在完了の疑問文（継続）"),
    ("沖縄に行ったことがありますか。", ["have", "you", "ever", "been", "to", "Okinawa"], "?", "Have you ever been to ～?（経験）"),
    ("こんなに大きな魚は見たことがない。", ["I", "have", "never", "seen", "such", "a big fish"], ".", "have never＋過去分詞（経験の否定）"),
    ("私たちが着いたときには、試合はもう始まっていた。", ["the game", "had", "already", "started", "when", "we", "arrived"], ".", "過去完了（過去の基準時より前の完了）"),
    ("雨が3日間ずっと降り続いている。", ["it", "has", "been", "raining", "for", "three days"], ".", "現在完了進行形（動作の継続）"),
    ("彼女が戻ってくるまで、ここで待ちましょう。", ["let's", "wait", "here", "until", "she", "comes back"], ".", "時の副詞節（until ～）の中は未来でも現在形"),
    ("この本を読み終えたら、あなたに貸してあげます。", ["I'll", "lend", "you", "this book", "when", "I", "have", "finished", "it"], ".", "時の副詞節の中では未来完了の内容を現在完了で表す"),
    ("父は前日に買った傘をなくした。", ["my father", "lost", "the umbrella", "he", "had", "bought", "the day before"], ".", "過去完了（なくした時点より前に買った）"),
    ("何時に家を出たのですか。", ["what time", "did", "you", "leave", "home"], "?", "What time ～? は過去の一時点を尋ねるので過去形（現在完了は使えない）"),
    ("その知らせを聞いてから、彼女はずっと元気がない。", ["she", "has", "been", "sad", "since", "hearing", "the news"], ".", "現在完了（状態の継続）"),
    ("明日の今ごろ、あなたは何をしているでしょうか。", ["what", "will", "you", "be", "doing", "this time tomorrow"], "?", "未来進行形（未来の一時点で進行中の動作）"),
]


@gen("standard_practice", 5, ["application", "computation"])
def build_order(r):
    jp, parts, end, point = r.choice(ORD)
    sent = " ".join(parts)
    sent = sent[0].upper() + sent[1:] + end
    return order(f"日本語に合うように、語句を並べかえて英文を完成させなさい。ただし、文頭にくる語も小文字で示してある。\n{jp}", parts,
                 f"{sent}　ポイント：{point}。", d=3,
                 ap="日本語から時制（基準時と見方）を先に決め、助動詞・have・be などの位置を確定させてから残りを並べる。",
                 steps=[f"時制を決める：{point}。", "主語と述語動詞（have＋過去分詞、be＋ing など）の並びを作る。", "残りの語句（目的語・時を表す語句・節）を並べる。", f"完成文：{sent}"],
                 alt=["完成した英文を和訳し直して、日本語と時の関係が一致しているかを確かめる。"],
                 pc=[("時制の形（助動詞・have・be の位置）が正しい", 2), ("全体の語順が正しい", 2)],
                 pit=["疑問文で have と主語の順を逆にし忘れる。", "時・条件の副詞節の中に will を入れてしまう。"])


# ======================================================================
# C 思考力・記述応用
# ======================================================================

PAIRS = [
    ("Tell me when he comes back.", "Tell me when he will come back.",
     "Aの when 節は「彼が戻ってきたら」という時の副詞節なので、未来でも現在形 comes。意味は「彼が戻ってきたら教えて」。Bの when 節は tell の目的語で「彼がいつ戻ってくるか」という名詞節なので will を使う。意味は「彼がいつ戻ってくるか教えて」。"),
    ("Let me know if she comes.", "Let me know if she will come.",
     "Aの if 節は「もし彼女が来たら」という条件の副詞節なので現在形。意味は「彼女が来たら知らせて」。Bの if 節は know の目的語で「彼女が来るかどうか」という名詞節なので will を使う。意味は「彼女が来るかどうか知らせて」。"),
    ("I lost my key.", "I have lost my key.",
     "Aは過去形で、過去にかぎをなくしたという出来事だけを述べ、今見つかっているかどうかはわからない。Bは現在完了（結果）で、なくした結果、今もかぎがないという現在の状態まで伝えている。"),
    ("He has gone to London.", "He has been to London.",
     "Aは現在完了の結果用法で「ロンドンに行ってしまって、今ここにいない」。Bは現在完了の経験用法で「ロンドンに行ったことがある」（今はここにいてよい）。"),
    ("When I arrived, she left.", "When I arrived, she had left.",
     "Aは過去形どうしで、私が着いたのとほぼ同時かその直後に彼女が出て行った。Bは過去完了で、私が着いた時点より前に彼女はすでに出て行っていた（着いたときにはもういなかった）。"),
    ("I have lived here for ten years.", "I lived here for ten years.",
     "Aは現在完了の継続で、10年前から今もここに住んでいる。Bは過去形で、過去に10年間住んでいたが、今はもう住んでいない（現在とは切り離された出来事）。"),
    ("The bus stopped.", "The bus was stopping.",
     "Aは過去形で、バスが止まったという動作の完了を表す。Bは過去進行形で、バスが止まりかけていた（まだ完全には止まっていない）という、その時点で進行中の動作を表す。"),
    ("I'll ask him when he arrives.", "I'll ask him when he will arrive.",
     "Aの when 節は「彼が着いたら」という時の副詞節で、意味は「彼が着いたら（そのときに）彼に尋ねよう」。Bの when 節は ask の目的語で「彼がいつ着くか」という名詞節で、意味は「彼がいつ着くかを彼に尋ねよう」。"),
    ("By the time you came, I had finished the work.", "By the time you come, I will have finished the work.",
     "Aは基準時が過去（あなたが来た時点）で、その時点までに仕事を終えていたことを過去完了で表す。Bは基準時が未来（あなたが来る時点）で、その時点までに終えているだろうことを未来完了で表す。by the time 節は時の副詞節なので、Bでも come は現在形。"),
]


@gen("thinking_writing", 4, ["written_reasoning", "concept"])
def explain_difference(r):
    a, b, model = r.choice(PAIRS)
    return desc(f"次の2つの英文A・Bの意味の違いを、時制の働きに触れながら日本語で説明しなさい。\nA：{a}\nB：{b}", model,
                "時制の違いは「基準時」と「その時点での見方」の違い、または節の種類（副詞節・名詞節）の違いとして説明できる。",
                [("Aの時制（または節の種類）の働きを正しく説明している", 3), ("Bの時制（または節の種類）の働きを正しく説明している", 3), ("A・Bの意味の違いを和訳などで明確に示している", 2)], d=4, p=8, lines=6,
                ap="2文で異なる部分（動詞の形）に注目し、それぞれの基準時と見方、または節の働き（副詞節か名詞節か）を時間軸や訳し分けで比べる。",
                steps=["A・Bで形が異なる部分を確認する。", "それぞれの基準時と見方（または節の種類）を判断する。", "意味の違いを和訳とともに説明する。"],
                alt=["それぞれの文に続く文を考えると違いがはっきりする（例：I have lost my key. に続くのは So I can't get in.、I lost my key. には But I found it later. も続けられる）。"],
                pc=[("Aの説明", 3), ("Bの説明", 3), ("意味の違いの明示", 2)],
                pit=["和訳だけを並べ、時制の働きに触れない。", "副詞節と名詞節の違いを「when があるから現在形」とだけ説明する。"])


REPORT = [
    ('He said, "I am tired."', "He said (that) he was tired.", "said（過去）に合わせて am を was にする（時制の一致）。I は he に変える。", "現在形 → 過去形"),
    ('She said, "I lost my key."', "She said (that) she had lost her key.", "said より前の出来事なので、過去形 lost を過去完了 had lost にする。I・my は she・her に変える。", "過去形 → 過去完了"),
    ('Ken said to me, "I will call you tomorrow."', "Ken told me (that) he would call me the next day.", "will を would にする。I・you は he・me に、tomorrow は the next day に変える。", "will → would"),
    ('I asked him, "Where do you live?"', "I asked him where he lived.", "疑問詞のある疑問文は間接疑問（疑問詞＋主語＋動詞）にし、asked に合わせて live を過去形 lived にする。", "現在形 → 過去形（間接疑問の語順）"),
    ('Our teacher said, "Light travels faster than sound."', "Our teacher said (that) light travels faster than sound.", "いつでも成り立つ事実は、時制の一致を受けずに現在形のままにすることが多い（traveled としても誤りではない）。", "不変の事実は現在形のまま"),
    ('She said, "I have finished my homework."', "She said (that) she had finished her homework.", "said に合わせて現在完了 have finished を過去完了 had finished にする。", "現在完了 → 過去完了"),
    ('He asked me, "Have you ever been to Kyoto?"', "He asked me if I had ever been to Kyoto.", "Yes / No 疑問文は if（whether）＋主語＋動詞の語順にし、asked に合わせて have been を had been にする。", "現在完了 → 過去完了（if を使った間接疑問）"),
    ('Mari said, "I am going to visit my uncle."', "Mari said (that) she was going to visit her uncle.", "said に合わせて am を was にする。I・my は she・her に変える。", "現在形 → 過去形"),
]


@gen("thinking_writing", 3, ["cross_unit", "written_reasoning"], rel=["JH-ENG-G3-U04"])
def reported_speech(r):
    s, ans, why, shift = r.choice(REPORT)
    return desc(f"次の英文を、引用符を使わない文（間接話法）に書きかえなさい。また、動詞の時制をどう変えたかとその理由を説明しなさい。\n{s}", f"{ans}　{why}",
                f"主節の動詞が過去形のとき、従属節の動詞もそれに合わせて時制を変える（時制の一致）。この文では{shift}。{why}",
                [("書きかえた英文が正しい（語順・代名詞を含む）", 4), ("時制の変化（" + shift + "）を正しく説明している", 3), ("時制の一致の理由（主節の過去形に合わせる）に触れている", 1)], d=4, p=8, lines=5,
                ap="主節の動詞（said / asked）が過去形なので、伝える内容の時制を1つ過去へずらす。疑問文は間接疑問（中学3年）の語順にし、代名詞・時を表す語句も話し手の立場に合わせて変える。",
                steps=["主節の動詞の時制を確認する（過去形）。", f"引用部分の動詞の時制を変える：{shift}。", "代名詞・時を表す語句、疑問文なら語順を変える。", f"答え：{ans}"],
                alt=["書きかえた文の出来事を時間軸に並べ、元の発言の時点との前後関係が保たれているかを確かめる。"],
                pc=[("英文", 4), ("時制の変化の説明", 3), ("理由", 1)],
                pit=["間接疑問の語順を疑問文のままにする（where did he live など）。", "時制をずらし忘れる、または不変の事実まで機械的にずらす。"])


ORDER_EV = [
    ("When Mika got to the theater, the movie had already started.", "映画が始まったこと", "had already started は過去完了で、ミカが着いた（got）時点より前に完了していたことを表す。"),
    ("When Mika got to the theater, the movie started.", "ミカが劇場に着いたこと", "どちらも過去形で、when 節の出来事（着いた）とほぼ同時かその直後に映画が始まったことを表す。過去完了がないので、映画が先に始まっていたとは読めない。"),
    ("I found that someone had opened my letter.", "だれかが手紙を開けたこと", "had opened は過去完了で、私が気づいた（found）時点より前に起きたことを表す。"),
    ("By the time the police arrived, the thief had run away.", "泥棒が逃げたこと", "had run away は過去完了で、警察が着いた（arrived）時点までにすでに完了していたことを表す。"),
    ("She told me that she had lived in Paris as a child.", "彼女がパリに住んでいたこと", "had lived は過去完了で、彼女が話した（told）時点より前のことを表す。"),
    ("When I called him, he had just gone to bed.", "彼が寝たこと", "had just gone は過去完了で、私が電話した（called）時点の直前に完了していたことを表す。"),
    ("When I called him, he was taking a bath.", "彼が風呂に入り始めたこと", "was taking は過去進行形で、電話した時点ですでに入浴が始まっていて、進行中だったことを表す。"),
    ("When I opened the door, the cat ran out.", "私がドアを開けたこと", "どちらも過去形で、出来事が起きた順（ドアを開けた → 猫が飛び出した）に述べている。"),
]


@gen("thinking_writing", 3, ["application", "condition_check"])
def which_first(r):
    s, first, why = r.choice(ORDER_EV)
    return desc(f"次の英文で述べられている2つの出来事のうち、先に起きた（または始まった）のはどちらか。日本語で答え、その根拠を動詞の時制に触れて説明しなさい。\n{s}",
                f"{first}。{why}", why,
                [("先に起きた出来事を正しく答えている", 3), ("根拠として動詞の時制（過去完了・過去進行形・過去形）の働きを説明している", 4), ("2つの出来事の時間関係を明確に述べている", 1)], d=4, p=8, lines=4,
                ap="2つの動詞の形を比べる。過去完了は過去の基準時より前、過去進行形は基準時にすでに進行中、過去形どうしは原則として述べた順（またはほぼ同時）を表す。",
                steps=["2つの出来事と、それぞれの動詞の形を確認する。", "基準時となる出来事（when 節・主節など）を決める。", "時制の働きから前後関係を判断する。", f"答え：{first}"],
                alt=["2つの出来事を時間軸に書きこみ、文の意味と矛盾しない並べ方を確かめる。"],
                pc=[("先の出来事", 3), ("時制の働きの説明", 4), ("時間関係の明示", 1)],
                pit=["過去形どうしの文でも、主節の出来事が先だと思いこむ。", "過去進行形を「後から始まった」と誤解する。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(task, wrong, step, etype, tempt, fix, ans, expl, steps, ap, alt, pit, d=3):
    return desc(f"{task}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい英文に書き直しなさい。", ans, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい英文に直している", 3), ("時制の規則を説明している", 1)], d=d, p=6, lines=5,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい英文", 3), ("規則の説明", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix))


PERF_ERR = [
    ("私は昨日その映画を見た。", "I have seen the movie yesterday.", "I saw the movie yesterday.", "have seen", "condition",
     "yesterday は過去の一時点を特定するので、基準時が現在の現在完了とは使えない。過去形にする。", "日本語の「見た」を「完了」と考えて現在完了にした。"),
    ("彼はいつ日本に来ましたか。", "When has he come to Japan?", "When did he come to Japan?", "has he come", "condition",
     "When ～? は過去の一時点を尋ねるので、現在完了とは使えない。過去形の疑問文にする。", "「来て今もいる」という現在とのつながりを意識して現在完了にした。"),
    ("私は3年前にこの町に引っ越してきた。", "I have moved to this town three years ago.", "I moved to this town three years ago.", "have moved", "condition",
     "～ ago は過去の一時点を表すので、現在完了とは使えない。過去形にする。", "「引っ越してきて今も住んでいる」という気持ちから現在完了にした。"),
    ("子どものころ、私は北海道に住んでいた。", "I have lived in Hokkaido when I was a child.", "I lived in Hokkaido when I was a child.", "have lived", "condition",
     "when I was a child は過去の一時期を特定するので、現在完了とは使えない。過去形にする。", "「住んだことがある」という経験の意味で現在完了を使おうとした。"),
    ("私は10年間ずっとこの町に住んでいる。", "I live in this town for ten years.", "I have lived in this town for ten years.", "live", "concept",
     "for ten years（今までの10年間）は現在までの継続を表すので、現在形ではなく現在完了にする。", "日本語の「住んでいる」が現在形なので、英語も現在形にした。"),
    ("先週からずっと雨が降っている。", "It is raining since last week.", "It has been raining since last week.", "is raining", "concept",
     "since last week（先週から今まで）の継続を表すので、現在進行形ではなく現在完了進行形にする。", "「降っている」という日本語から現在進行形を選んだ。"),
    ("私たちは子どものころから知り合いだ。", "We are knowing each other since we were children.", "We have known each other since we were children.", "are knowing", "concept",
     "know は状態動詞なので進行形にしない。since ～ の継続は現在完了で表す。", "「知り合っている」という日本語から進行形にした。"),
    ("彼女は京都に2回行ったことがある。", "She has gone to Kyoto twice.", "She has been to Kyoto twice.", "has gone", "concept",
     "「行ったことがある」という経験は has been to で表す。has gone to は「行ってしまって今いない」という結果を表す。", "「行った」から go の過去分詞 gone を使った。"),
]


@gen("error_correction", 4, ["common_error", "condition_check"])
def err_perfect(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(PERF_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"動詞「{where}」の時制", etype, tempt, fix, fix, f"{rule}正しくは {fix}",
                    ["時を表す語句から基準時を確かめる。", f"「{where}」がその基準時と合っているかを判断する。", f"正しい英文：{fix}"],
                    "日本語の「た」「ている」ではなく、時を表す語句（yesterday、～ ago、for ～、since ～ など）から基準時を決めて時制を選ぶ。",
                    ["時間軸に出来事と基準時をかき、現在まで続いているか、過去の一点で終わっているかを確かめる。"],
                    ["日本語の語尾（た・ている）から時制を決める。"], d=3)


CLAUSE_ERR = [
    ("明日雨が降ったら、私は家にいます。", "If it will rain tomorrow, I'll stay home.", "If it rains tomorrow, I'll stay home.", "will rain", "condition",
     "if 節は条件を表す副詞節なので、未来のことも現在形で表す。", "tomorrow があるので未来の will が必要だと考えた。"),
    ("彼が戻ってきたら出発しよう。", "Let's start when he will come back.", "Let's start when he comes back.", "will come", "condition",
     "when 節は「～したら」という時の副詞節なので、未来のことも現在形で表す。", "戻ってくるのはこれからなので will を使った。"),
    ("宿題が終わるまで外出してはいけません。", "You must not go out until you will finish your homework.", "You must not go out until you finish your homework.", "will finish", "condition",
     "until 節は時の副詞節なので、未来のことも現在形で表す（have finished も可）。", "宿題を終えるのはこれからなので will を使った。"),
    ("駅に着いたらすぐに電話してね。", "Call me as soon as you will arrive at the station.", "Call me as soon as you arrive at the station.", "will arrive", "condition",
     "as soon as 節は時の副詞節なので、未来のことも現在形で表す。", "着くのはこれからなので will を使った。"),
    ("明日晴れるかどうかわからない。", "I don't know if it is sunny tomorrow.", "I don't know if it will be sunny tomorrow.", "is", "condition",
     "if 節は know の目的語（「～かどうか」）の名詞節なので、未来のことは will で表す。", "「if 節の中は現在形」という規則を、名詞節にも当てはめた。"),
    ("彼女がいつ帰ってくるのか、だれも知らない。", "Nobody knows when she comes back.", "Nobody knows when she will come back.", "comes", "condition",
     "when 節は knows の目的語（「いつ～か」）の名詞節なので、未来のことは will で表す。", "「when 節の中は現在形」という規則を、名詞節にも当てはめた。"),
    ("準備ができたら知らせてください。", "Please let me know when you will be ready.", "Please let me know when you are ready.", "will be", "condition",
     "この when 節は「～したら」という時の副詞節なので、未来のことも現在形で表す。", "準備ができるのはこれからなので will を使った。"),
]


@gen("error_correction", 3, ["common_error", "concept"])
def err_clause(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(CLAUSE_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", etype, tempt, fix, fix, f"{rule}正しくは {fix}",
                    ["接続詞が導く節が副詞節（時・条件）か名詞節（目的語）かを判断する。", "副詞節なら未来でも現在形、名詞節なら will を使う。", f"正しい英文：{fix}"],
                    "if / when の節は、「もし～なら・～したら」（副詞節）か「～かどうか・いつ～か」（名詞節）かを、日本語の意味と文中での働きから判断する。",
                    ["節を取り除いて文が成り立つか（副詞節）、動詞の目的語がなくなるか（名詞節）を確かめる。"],
                    ["when / if があれば必ず現在形、と機械的に覚える。"], d=3)


PAST_ERR = [
    ("駅に着いたとき、電車はもう出てしまっていた。", "When I got to the station, the train has already left.", "When I got to the station, the train had already left.", "has already left", "concept",
     "基準時は「駅に着いた」という過去の時点なので、それより前の完了は過去完了で表す。", "「もう～してしまった」から現在完了を連想した。"),
    ("私は前日に買ったペンをなくした。", "I lost the pen I have bought the day before.", "I lost the pen I had bought the day before.", "have bought", "concept",
     "なくした（過去）時点より前に買ったので過去完了で表す。", "「買った」を完了と考えて現在完了にした。"),
    ("来年の3月で、私たちはここに5年住んだことになる。", "We have lived here for five years by next March.", "We will have lived here for five years by next March.", "have lived", "concept",
     "基準時は next March という未来の時点なので、その時点までの継続は未来完了で表す。", "「5年住んだ」という継続から現在完了を選び、基準時が未来であることを見落とした。"),
    ("彼女は、以前その本を読んだことがあると言った。", "She said that she has read the book before.", "She said that she had read the book before.", "has read", "concept",
     "said（過去）の内容なので、時制の一致により現在完了は過去完了になる。", "元の発言が I have read ～ なので、そのまま現在完了を使った。"),
    ("私が電話したとき、彼は夕食を食べているところだった。", "When I called him, he has eaten dinner.", "When I called him, he was eating dinner.", "has eaten", "concept",
     "電話した（過去）時点で進行中だった動作なので、過去進行形で表す。", "「食べている」から現在完了の継続を連想した。"),
    ("明日の今ごろは、私たちはハワイ行きの飛行機に乗っているだろう。", "This time tomorrow, we will have flown to Hawaii.", "This time tomorrow, we will be flying to Hawaii.", "will have flown", "concept",
     "未来の一時点で進行中の動作は未来進行形で表す。未来完了にすると「その時点までに飛び終えている」という意味になる。", "未来の時点が示されているので、未来完了を使えばよいと考えた。"),
]


@gen("error_correction", 3, ["common_error", "written_reasoning"])
def err_past_perfect(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(PAST_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"動詞「{where}」", etype, tempt, fix, fix, f"{rule}正しくは {fix}",
                    ["基準時（過去・未来のある時点）を確かめる。", "空所の出来事が基準時より前か、基準時に進行中か、基準時までの継続かを判断する。", f"正しい英文：{fix}"],
                    "基準時が現在でないときは、現在完了は使えない。基準時を過去に移せば過去完了、未来に移せば未来完了、その時点で進行中なら進行形になる。",
                    ["2つの出来事を時間軸に書きこみ、前後関係と基準時の位置から時制を確かめる。"],
                    ["基準時が過去・未来なのに現在完了を使う。"], d=4)


GENERATORS = [verb_form, basic_tense, time_expression, adverbial_clause,
              perfect_tense, perfect_use, rewrite, build_order,
              explain_difference, reported_speech, which_first,
              err_perfect, err_clause, err_past_perfect]
