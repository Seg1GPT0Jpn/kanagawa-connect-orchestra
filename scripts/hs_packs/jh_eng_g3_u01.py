"""単元パック：中学3年 英語 現在完了形（継続・経験・完了）・現在完了進行形。"""
from banks._common import desc, mc, order, sa
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem,
                         tp)

UNIT_ID = "JH-ENG-G3-U01"

PREREQUISITES = [
    ("JH-ENG-G1-U05", "過去形（規則動詞・不規則動詞・was / were）。過去形は「過去の一時点」だけを表すことを、現在完了形との対比で使う。"),
    ("JH-ENG-G2-U05", "過去分詞（written, seen, been など）を正しく書けること。現在完了形は have / has＋過去分詞で作る。"),
    ("JH-ENG-G1-U04", "現在進行形 be＋ing 形と、know / like / want など進行形にしない状態の動詞。現在完了進行形でも同じ区別を使う。"),
]
EXTENSIONS = [
    ("HS-ENG-U02", "高校の「時制」で、過去完了形（had＋過去分詞）・未来完了形へと、完了形の考え方を過去や未来の基準点に広げる。"),
    ("HS-ENG-U08", "仮定法過去完了（If I had known ～）でも had＋過去分詞の完了形を使う。完了形の形に慣れておくことが土台になる。"),
    ("JH-ENG-G3-U06", "スピーチや体験談の長文では、I have been to ～ / I have lived here for ～ などの現在完了形で経験や続いていることが語られる。"),
]

NEG = {"have": "haven't", "has": "hasn't"}


def cap(s):
    return s[0].upper() + s[1:]


def low(s):
    if s.split()[0] in ("My", "Your", "The", "This", "Our"):
        return s[0].lower() + s[1:]
    if s in ("You", "She", "He", "We", "They", "It"):
        return s.lower()
    return s


# ======================================================================
# 授業プリント
# ======================================================================

LESSON = lesson(
    goals=["現在完了形〈have / has＋過去分詞〉が「過去から今につながっていること」を表すと理解し、継続・経験・完了の3つの用法を見分けられる。",
           "for / since / ever / never / just / already / yet / before などの語を、用法と文の種類（肯定・否定・疑問）に合わせて使える。",
           "現在完了進行形〈have / has been＋ing 形〉で、動作が今までずっと続いていることを表せる。状態の動詞では使わないことがわかる。",
           "yesterday / ～ ago / last ～ / When ～? など過去の一時点を表す語句とは現在完了形を使わず、過去形を選べる。"],
    duration=100,
    readiness=["過去形（規則動詞の ed、不規則動詞 went, saw, ate など）を書ける（中1）。",
               "受け身で学んだ過去分詞（written, seen, done, been など）を書ける（中2）。",
               "現在進行形 be＋ing 形と、進行形にしない動詞（know, like, want）を区別できる（中1）。",
               "国語で「ずっと～している」「～したことがある」「もう～した」という言い方の違いがわかる（小学校）。"],
    flow=[("導入：過去と今をつなぐ", 8, "「3年前に横浜に来た。今も住んでいる」を1文で言うには？と問い、時間軸の図で現在完了形を導入する"),
          ("現在完了形の形", 12, "have / has＋過去分詞、短縮形、否定文・疑問文の作り方"),
          ("継続用法と for / since", 15, "How long ～?、for＋期間・since＋起点（例題1）"),
          ("経験用法", 15, "ever / never / before / ～ times、have been to と have gone to、How many times ～?（例題2）"),
          ("完了用法", 15, "just / already / yet の位置と意味、完了の結果が今に残ること"),
          ("現在完了進行形", 15, "have been＋ing 形、状態動詞との区別（例題3）"),
          ("過去形との使い分け・まとめ", 20, "過去の一時点を表す語句と現在完了形がいっしょに使えない理由を話し合い、確認問題")],
    sections=[
        intro("in1", "「過去」と「今」を1文でつなぐ",
              "I came to Yokohama three years ago.（3年前に横浜に来た）は過去のできごとだけを表し、今どうしているかはわかりません。そこに「今も住んでいる」ことまで含めて言いたいときに使うのが現在完了形 I have lived in Yokohama for three years. です。現在完了形は、過去に始まったことや過去のできごとが「今」とつながっていることを表す形です。",
              bullets=["I lived in Yokohama for three years.（過去に3年間住んでいた。今は住んでいない）",
                       "I have lived in Yokohama for three years.（3年間ずっと住んでいて、今も住んでいる）",
                       "日本語では「住んでいる」「住んでいた」の区別だけだが、英語は「今とのつながり」を動詞の形で示す。"],
              points=[tp("黒板に時間軸（過去 ― 今）をかき、過去形は過去の1点、現在完了形は過去から今までの矢印で表すことを示す。",
                         ask="I lived ～ と I have lived ～ では、今も住んでいるのはどちらか。", expect="I have lived ～ のほう。", timing="導入の冒頭")]),
        definition("df1", "現在完了形の形：have / has＋過去分詞",
                   "現在完了形は〈have / has＋過去分詞〉で作ります。主語が三人称単数のときは has を使います。have / has は助動詞のような働きをするので、否定文・疑問文は have / has を使って作ります。",
                   formula="主語＋have / has＋過去分詞 ～.",
                   bullets=["短縮形：I have → I've ／ She has → She's ／ have not → haven't ／ has not → hasn't",
                            "否定文：have / has の後ろに not（I haven't finished my homework yet.）",
                            "疑問文：Have / Has を主語の前に出す（Have you ever been to Kyoto? ― Yes, I have. / No, I haven't.）",
                            "疑問詞：How long have you lived here? ／ How many times have you seen the movie?"],
                   conditions=["否定文・疑問文・答えの文で do / does / did は使わない。",
                               "yesterday / last ～ / ～ ago / When ～? など、過去の一時点をはっきり表す語句とはいっしょに使わない（過去形を使う）。"],
                   points=[tp("過去分詞は2年生の受け身で学んだものと同じであることを確認し、不規則動詞の表をもう一度音読させる。", timing="形の説明時"),
                           tp("Did you ever ～? や Yes, I did. と答える誤りを予告し、「答えも have / has で」と口頭で練習させる。",
                              ask="Have you finished lunch? に「はい」と答えると？", expect="Yes, I have.")]),
        theorem("th1", "現在完了形の3つの用法と目印になる語",
                "継続：ずっと～している ／ 経験：～したことがある ／ 完了：（ちょうど・もう）～したところだ",
                ["継続：for＋期間（for three years）、since＋起点（since 2020 / since I was a child）、How long ～? 状態を表す動詞（live, know, be, want など）でよく使う。",
                 "経験：ever（疑問文で「今までに」）、never（一度も～ない）、before（以前に）、once / twice / ～ times、How many times ～?",
                 "完了：just（ちょうど）、already（肯定文で「もう」）、yet（疑問文で「もう」、否定文で「まだ」・文末）",
                 "have been to ～：～へ行ったことがある（経験）／～へ行ってきたところだ（完了）",
                 "have gone to ～：～へ行ってしまった（今ここにいない）。中学では「結果」の意味として学ぶ。"],
                body="同じ have＋過去分詞でも、いっしょに使われる語や文の内容で用法が決まります。目印になる語がないときは、文の内容と場面から判断します。",
                points=[tp("3つの用法を時間軸の図で区別させる（継続＝矢印、経験＝過去の点がいくつか、完了＝今の直前の点）。",
                           ask="I have been to Kyoto twice. はどの用法か。", expect="経験（twice が目印）。")]),
        definition("df2", "現在完了進行形：have / has been＋ing 形",
                   "動作（read, study, play, wait, rain など）が過去のある時から今までずっと続いていることを強調するときは、現在完了進行形〈have / has been＋ing 形〉を使います。",
                   formula="主語＋have / has been＋動詞の ing 形 ～（for ～ / since ～）.",
                   bullets=["It has been raining since this morning.（今朝からずっと雨が降り続いている）",
                            "I have been reading this book for two hours.（2時間ずっとこの本を読んでいる）",
                            "How long have you been waiting here? ― For thirty minutes."],
                   conditions=["know / like / want / have（持っている）など状態を表す動詞は進行形にしないので、継続は現在完了形で表す（I have known him for ten years.）。",
                               "been を落とさない（× I have reading ～）。have / has＋been＋ing 形の3つがセット。"],
                   points=[tp("「現在進行形 am reading＋現在完了 have been」が合体した形と説明し、be 動詞の部分が been になることを確認させる。",
                              caution="I am reading this book for two hours. は「今」しか表せず、2時間続いていることを表せない。")]),
        derivation("dv1", "なぜ過去の一時点を表す語句と使えないのか（形と意味のつながり）",
                   ["① 現在完了形の have / has は現在形。だから文全体は「今」の話をしている。",
                    "② 過去分詞の部分が「過去に起きたこと・始まったこと」を表す。",
                    "③ 2つが合わさって「過去のことが今につながっている（今どうなっているか）」という意味になる。",
                    "④ yesterday / three days ago / last year / When ～? は「過去の1点」だけを指し、今とのつながりを表さない。",
                    "⑤ ①の「今の話」と④の「過去だけの話」が矛盾するので、いっしょに使えない。過去の1点を言うときは過去形を使う。",
                    "⑥ 一方、for three years（期間）や since 2020（起点から今まで）、ever（今までに）は「今まで」を含むので、現在完了形といっしょに使える。"],
                   body="I have visited Kyoto last year. が誤りになるのは、「今の話」の形に「過去だけの話」の語句をつけているからです。I visited Kyoto last year. か I have visited Kyoto before. にします。",
                   points=[tp("④と⑥の語句をカードにして「今まで」を含むかどうかで2つに分類させる。",
                              ask="since last year は現在完了形と使えるか。", expect="使える。since は「去年から今まで」を表すので、今を含む。", timing="導出の説明時")]),
        example("ex1", "例題1　継続：for と since",
                "日本語に合うように英文を書きなさい。(1) 私は5年間ずっとこの町に住んでいます。　(2) 姉は先週の月曜日からずっと忙しい。　(3) あなたはどのくらいの間、佐藤先生を知っていますか。",
                ["(1) 「5年間」は期間なので for five years。live の過去分詞 lived：I have lived in this town for five years.",
                 "(2) 「先週の月曜日から」は起点なので since last Monday。主語は三人称単数なので has、be の過去分詞は been：My sister has been busy since last Monday.",
                 "(3) 期間をたずねるので How long を文頭に置き、疑問文の語順 have you known を続ける：How long have you known Mr. Sato?"],
                "(1) I have lived in this town for five years.　(2) My sister has been busy since last Monday.　(3) How long have you known Mr. Sato?",
                thinking="for の後ろは「どのくらいの長さ（期間）」、since の後ろは「いつから（起点）」。",
                points=[tp("(2) を My sister is busy since ～. とする誤りに対し、is では「今」しか表せないことを時間軸で確認する。")],
                misconceptions=[("I have lived in this town since five years.", "five years は期間なので for を使う。"),
                                ("My sister has be busy since last Monday.", "has の後ろは過去分詞。be → been。")]),
        example("ex2", "例題2　経験と完了",
                "（　）内の語を使って英文を書きなさい。(1) あなたは今までに沖縄に行ったことがありますか。（ever）　(2) 私は一度もコアラを見たことがありません。（never）　(3) 私はちょうど宿題を終えたところです。（just）　(4) 電車はまだ到着していません。（yet）",
                ["(1) 「行ったことがある」は have been to。ever は have you と過去分詞の間：Have you ever been to Okinawa?",
                 "(2) never は have と過去分詞の間。never 自体に否定の意味があるので not は不要：I have never seen a koala.",
                 "(3) just も have と過去分詞の間：I have just finished my homework.",
                 "(4) 否定文の「まだ」は yet を文末に：The train hasn't arrived yet."],
                "(1) Have you ever been to Okinawa?　(2) I have never seen a koala.　(3) I have just finished my homework.　(4) The train hasn't arrived yet.",
                thinking="ever / never / just / already は have と過去分詞の間、yet は文末。",
                points=[tp("(1) を Have you ever gone to Okinawa? とする生徒に、「行ったことがある」は have been to で表すことを確認する。",
                           ask="He has gone to Okinawa. の彼は今どこにいるか。", expect="沖縄に行ってしまって、ここにはいない。")],
                misconceptions=[("I haven't never seen a koala.", "never だけで否定になる。not と重ねない。"),
                                ("The train hasn't arrived already.", "否定文の「まだ」は yet。")]),
        example("ex3", "例題3　現在完了進行形と状態の動詞",
                "（　）内の動詞を適切な形にしなさい。(1) It (rain) since this morning.　(2) I (know) Ken for six years.　(3) The children (play) in the park for two hours.",
                ["(1) rain は動作（天気の変化）を表す動詞。今朝から今まで降り続いているので現在完了進行形：has been raining。",
                 "(2) know は状態を表す動詞で進行形にしない。継続は現在完了形：have known。",
                 "(3) play は動作を表す動詞で、2時間続いているので現在完了進行形：have been playing。"],
                "(1) has been raining　(2) have known　(3) have been playing",
                thinking="動作の継続 → have been＋ing 形、状態の継続 → have＋過去分詞。",
                points=[tp("(2) を have been knowing とする誤りを取り上げ、1年生の「know は進行形にしない」というルールがここでも生きることを確認する。")]),
        board("bd1", "板書案",
              [("① 形と使い分け", ["have / has＋過去分詞", "否定：haven't / hasn't＋過去分詞", "疑問：Have you ～? ― Yes, I have.", "× yesterday / ～ ago / When", "→ 過去形を使う"]),
               ("② 3つの用法", ["継続：for＋期間 / since＋起点", "How long ～?", "経験：ever / never / before / ～ times", "have been to（行ったことがある）", "完了：just / already / yet（文末）"]),
               ("③ 現在完了進行形", ["have / has been＋ing", "It has been raining since this morning.", "I have been reading for two hours.", "状態の動詞は × 進行形", "I have known him for ten years."])],
              points=[tp("②の目印になる語を色分けして書き、問題を解くときに目印の語から用法を判断する習慣をつけさせる。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("時間軸の図を毎回かかせ、過去形（点）と現在完了形（今につながる）の違いを視覚で押さえる。", timing="導入・用法ごとに"),
               tp("for と since の区別は、後ろの語句を「どのくらい？」「いつから？」のどちらの答えになるかで判断させる。",
                  ask="since の後ろに置けるのは three days と last Friday のどちらか。", expect="last Friday（いつから？の答え）。"),
               tp("yet / already / just / ever / never の位置は、例文ごと音読して体で覚えさせる。", caution="yet を肯定文に使う、ever を肯定文に使う誤りが多い。"),
               tp("have been to と have gone to は、「その人は今どこにいるか」を考えさせて区別する。"),
               tp("問題プリント D の誤答例は「過去の一時点の語句」「for / since」「過去分詞の形」「状態動詞の進行形」「答え方」の5種類にまとめて振り返らせる。")],
              misconceptions=[("I have visited Kyoto last year.", "last year は過去の一時点。I visited Kyoto last year."),
                              ("When have you come to Japan?", "When は過去の一時点をたずねる。When did you come to Japan?"),
                              ("I have been knowing him for ten years.", "know は状態の動詞。I have known him for ten years."),
                              ("I have lived here since three years.", "期間は for。I have lived here for three years.")]),
        summary("sm1", "まとめ",
                ["現在完了形 ＝ have / has＋過去分詞。過去のことが「今」とつながっていることを表す。",
                 "継続（for / since / How long）・経験（ever / never / before / ～ times）・完了（just / already / yet）。",
                 "現在完了進行形 ＝ have / has been＋ing。動作の継続。状態の動詞は現在完了形で継続を表す。",
                 "過去の一時点（yesterday / ～ ago / last ～ / When）とは使えない。過去形を使う。"]),
        check("ck1", "確認問題",
              [("I have lived here (for / since) 2018. の（　）から正しいほうを選びなさい。", "since（2018 は起点）"),
               ("「私は一度もすしを食べたことがありません」を英語にしなさい。", "I have never eaten sushi."),
               ("「彼は1時間ずっとテレビを見ています」を現在完了進行形で英語にしなさい。", "He has been watching TV for an hour.")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

# (日本語, 空所つき英文, 三人称単数か, 過去分詞, 誤りの形（原形・過去形）, ing 形)
HAVE = [
    ("私はこの町に10年間住んでいます。", "I (　　) in this town for ten years.", False, "lived", "live", "living"),
    ("兄は去年から新しい自転車をほしがっています。", "My brother (　　) a new bike since last year.", True, "wanted", "want", "wanting"),
    ("彼女は京都を3回訪れたことがあります。", "She (　　) Kyoto three times.", True, "visited", "visit", "visiting"),
    ("私は以前この映画を見たことがあります。", "I (　　) this movie before.", False, "seen", "saw", "seeing"),
    ("エミは5歳のときからピアノをひいています。", "Emi (　　) the piano since she was five.", True, "played", "play", "playing"),
    ("私の両親は20年間おたがいを知っています。", "My parents (　　) each other for twenty years.", False, "known", "knew", "knowing"),
    ("トムは日本に3年間住んでいます。", "Tom (　　) in Japan for three years.", True, "lived", "live", "living"),
    ("私は富士山に2回登ったことがあります。", "I (　　) Mt. Fuji twice.", False, "climbed", "climb", "climbing"),
    ("姉はその歌手に一度会ったことがあります。", "My sister (　　) the singer once.", True, "met", "meet", "meeting"),
    ("彼らは先週の月曜日からずっと忙しい。", "They (　　) busy since last Monday.", False, "been", "was", "being"),
    ("父はこの車を15年間使っています。", "My father (　　) this car for fifteen years.", True, "used", "use", "using"),
    ("私はその話を何度も聞いたことがあります。", "I (　　) the story many times.", False, "heard", "hear", "hearing"),
    ("佐藤先生はこの学校で8年間英語を教えています。", "Mr. Sato (　　) English at this school for eight years.", True, "taught", "teach", "teaching"),
    ("私たちは以前その湖で泳いだことがあります。", "We (　　) in the lake before.", False, "swum", "swam", "swimming"),
    ("その犬は今朝からずっと具合が悪い。", "The dog (　　) sick since this morning.", True, "been", "was", "being"),
    ("私たちはそのレストランで2回食事をしたことがあります。", "We (　　) at the restaurant twice.", False, "eaten", "ate", "eating"),
]


@gen("basic_check", 4, ["computation", "condition_check"])
def have_form(r):
    jp, s, third, pp, bad, ing = r.choice(HAVE)
    h, oh = ("has", "have") if third else ("have", "has")
    subj = s.split(" (")[0]
    ok = f"{h} {pp}"
    why = {f"{oh} {pp}": (f"主語 {subj} は{'三人称単数なので has' if third else '三人称単数ではないので have'}を使う。", "主語と have / has の対応"),
           f"{h} {bad}": (f"have / has の後ろは過去分詞 {pp}。{bad} は{'過去形' if bad in ('saw', 'knew', 'was', 'swam', 'ate') else '原形'}で、現在完了形にならない。", "過去分詞の形"),
           f"{h} {ing}": ("have / has の後ろに ing 形を置くことはできない。現在完了形では have / has の後ろは過去分詞。", "現在完了形と進行形の混同")}
    return mc(f"日本語に合うように、（　）に入る最も適切なものを選びなさい。\n{jp}\n{s}", [ok] + list(why),
              f"「ずっと～している」「～したことがある」は現在完了形〈have / has＋過去分詞〉。主語 {subj} に合わせて {h}、動詞は過去分詞 {pp}。答え：{ok}", d=1,
              ap="①主語が三人称単数かどうかで have / has を決める、②後ろの動詞が過去分詞になっているかを確かめる。",
              steps=[f"主語 {subj} → {h}。", f"動詞を過去分詞 {pp} にする。", f"答え：{ok}"],
              alt=["選んだ形で疑問文（Have / Has ＋主語＋過去分詞 ～?）を作ってみて、形がくずれないかを確かめる。"],
              pc=[("have / has を正しく選んでいる", 1), ("過去分詞を正しく選んでいる", 1)],
              pit=["主語が三人称単数なのに have を使う。", "過去分詞の代わりに過去形を置く（have saw）。"], why=why)


# (英語の骨組み, 日本語の型, [(期間, 日本語)], [(起点, 日本語)])
FS = [
    ("I have lived in Yokohama", "私は{t}横浜に住んでいます。", [("ten years", "10年間"), ("five years", "5年間"), ("a long time", "長い間")],
     [("2018", "2018年から"), ("I was a child", "子どものころから"), ("last year", "去年から")]),
    ("It has been raining", "{t}ずっと雨が降っています。", [("two hours", "2時間"), ("three days", "3日間")],
     [("this morning", "今朝から"), ("last night", "昨夜から"), ("yesterday", "昨日から")]),
    ("We have known each other", "私たちは{t}おたがいを知っています。", [("ten years", "10年間"), ("a long time", "長い間")],
     [("we were children", "子どものころから"), ("2015", "2015年から")]),
    ("Ken has played soccer", "ケンは{t}サッカーをしています。", [("six years", "6年間")],
     [("he was eight", "8歳のときから"), ("last April", "去年の4月から")]),
    ("My father has worked at this hospital", "父は{t}この病院で働いています。", [("twenty years", "20年間"), ("a long time", "長い間")],
     [("2005", "2005年から")]),
    ("I have been studying English", "私は{t}ずっと英語を勉強しています。", [("two hours", "2時間"), ("three hours", "3時間")],
     [("this morning", "今朝から"), ("lunchtime", "昼食の時間から")]),
    ("She has wanted a dog", "彼女は{t}犬をほしがっています。", [("a long time", "長い間"), ("two years", "2年間")],
     [("last summer", "去年の夏から")]),
    ("They have been busy", "彼らは{t}ずっと忙しい。", [("a week", "1週間"), ("three days", "3日間")],
     [("last Monday", "先週の月曜日から")]),
]


@gen("basic_check", 4, ["concept", "condition_check"])
def for_since(r):
    en, jpf, periods, points = r.choice(FS)
    use_for = r.random() < 0.5
    t, tj = r.choice(periods if use_for else points)
    ok, other = ("for", "since") if use_for else ("since", "for")
    why = {other: ((f"since の後ろには「いつから」を表す起点が来る。{t} は期間（どのくらいの長さ）なので for。") if use_for
                   else (f"for の後ろには期間（どのくらいの長さ）が来る。{t} は起点（いつから）なので since。"), "for と since の区別"),
           "ago": ("ago は「～前」という意味で過去形の文で使い、後ろに語句を続けない。現在完了形とはいっしょに使わない。", "過去の一時点を表す語句"),
           "from": ("from は「～から」だが、現在完了形で「～から今までずっと」を表すときは since を使う。期間の前にも置けない。", "日本語の「から」との混同")}
    return mc(f"日本語に合うように、（　）に入る最も適切なものを選びなさい。\n{jpf.format(t=tj)}\n{en} (　　) {t}.", [ok] + list(why),
              f"{t} は{'期間（どのくらいの長さ）なので for' if use_for else '起点（いつから）なので since'}。答え：{ok}", d=1,
              ap="（　）の後ろの語句が「どのくらいの間？」の答え（期間）か、「いつから？」の答え（起点）かを考える。",
              steps=[f"後ろの語句 {t} は{'期間' if use_for else '起点'}。", f"期間 → for、起点 → since。答え：{ok}"],
              alt=[f"「{t}」に How long ～? と When did it start? のどちらの答えになるかを当てはめて確かめる。"],
              pc=[("期間か起点かを判断している", 1), ("for / since を正しく選んでいる", 1)],
              pit=["日本語の「～から」「～間」だけを見て判断し、for と since を逆にする。", "since の後ろに期間を置く（since three years）。"], why=why)


USAGE = {"cont": "継続（ずっと～している）", "exp": "経験（～したことがある）", "comp": "完了（ちょうど・もう～した）", "prog": "現在完了進行形（動作がずっと続いている）"}
CLUE = {"cont": "for / since / How long と状態を表す動詞", "exp": "ever / never / before / once / twice / ～ times / How many times",
        "comp": "just / already / yet", "prog": "have / has been＋ing 形"}
USAGE_S = [
    ("I have lived in Kamakura for five years.", "cont", "for five years"), ("My brother has been sick since Monday.", "cont", "since Monday"),
    ("We have known Ms. Green for a long time.", "cont", "for a long time"), ("How long have you had this dog?", "cont", "How long"),
    ("She has wanted this bag since last month.", "cont", "since last month"),
    ("I have visited Nara twice.", "exp", "twice"), ("Have you ever eaten natto?", "exp", "ever"), ("My father has never seen snow.", "exp", "never"),
    ("Ken has climbed Mt. Fuji before.", "exp", "before"), ("How many times have you been to Tokyo?", "exp", "How many times"),
    ("I have just finished my homework.", "comp", "just"), ("The train has already left.", "comp", "already"),
    ("Have you cleaned your room yet?", "comp", "yet"), ("She hasn't written the report yet.", "comp", "yet"),
    ("We have just arrived at the station.", "comp", "just"),
    ("It has been raining since this morning.", "prog", "has been raining"), ("I have been reading this book for two hours.", "prog", "have been reading"),
    ("How long have you been waiting here?", "prog", "have you been waiting"), ("They have been playing tennis since ten o'clock.", "prog", "have been playing"),
]


@gen("basic_check", 4, ["concept", "computation"])
def usage_type(r):
    en, k, clue = r.choice(USAGE_S)
    ok = USAGE[k]
    why = {USAGE[w]: (f"{USAGE[w].split('（')[0]}なら {CLUE[w]} などが目印になる。この文の目印は「{clue}」なので{ok.split('（')[0]}。", "用法の見分け方")
           for w in USAGE if w != k}
    return mc(f"次の英文の現在完了形（現在完了進行形）は、どの意味を表しているか。最も適切なものを選びなさい。\n{en}", [ok] + [USAGE[x] for x in ("cont", "exp", "comp", "prog") if x != k],
              f"目印は「{clue}」。答え：{ok}", d=1,
              ap="文の中から用法の目印になる語（for / since / ever / never / just / already / yet / been＋ing など）を探す。",
              steps=[f"目印の語を見つける：{clue}。", f"その語が表す意味から用法を決める。答え：{ok}"],
              alt=["文を日本語に訳してみて、「ずっと～している」「～したことがある」「～したところだ」のどれが自然かで確かめる。"],
              pc=[("目印の語を見つけている", 1), ("用法を正しく選んでいる", 1)],
              pit=["been を見ただけで経験と決めつける（has been sick は継続）。", "yet を経験の目印と取り違える。"], why=why)


ADV_WHY = {"yet": "yet は疑問文（もう）・否定文（まだ）の文末で使う。肯定文や have と過去分詞の間には置かない。",
           "already": "already は肯定文で「もう・すでに」を表す。否定文の文末で「まだ」の意味には使えない。",
           "ever": "ever は疑問文で「今までに」を表し、主語と過去分詞の間に置く。肯定文や文末には置かない。",
           "never": "never は「一度も～ない」という否定の語。",
           "just": "just は「ちょうど」で、have と過去分詞の間に置く。文末には置かない。",
           "since": "since の後ろには「いつから」を表す起点（語句や文）が必要。",
           "for": "for の後ろには期間（three years など）が必要。",
           "ago": "ago は「～前」で過去形の文で使い、前に期間（two days など）が必要。現在完了形とはいっしょに使わない。"}
ADV = [
    ("私はちょうど駅に着いたところです。", "I have (　　) arrived at the station.", "just", ["yet", "ever", "since"]),
    ("電車はもう出発してしまいました。", "The train has (　　) left.", "already", ["yet", "ever", "ago"]),
    ("あなたはもう宿題を終えましたか。", "Have you finished your homework (　　)?", "yet", ["just", "ever", "since"]),
    ("私はまだ手紙を書いていません。", "I haven't written the letter (　　).", "yet", ["already", "ever", "just"]),
    ("あなたは今までにパンダを見たことがありますか。", "Have you (　　) seen a panda?", "ever", ["yet", "since", "for"]),
    ("私は一度も海外に行ったことがありません。", "I have (　　) been abroad.", "never", ["ever", "yet", "for"]),
    ("私は以前その映画を見たことがあります。", "I have seen the movie (　　).", "before", ["ago", "yet", "for"]),
    ("姉はちょうど家を出たところです。", "My sister has (　　) left home.", "just", ["yet", "ever", "for"]),
    ("私はもう昼食を食べました。", "I have (　　) eaten lunch.", "already", ["yet", "ever", "for"]),
    ("父はまだ帰宅していません。", "My father hasn't come home (　　).", "yet", ["already", "ever", "just"]),
    ("彼は一度もすしを食べたことがありません。", "He has (　　) eaten sushi.", "never", ["ever", "yet", "ago"]),
    ("あなたはもうその本を読みましたか。", "Have you read the book (　　)?", "yet", ["ever", "just", "ago"]),
]
ADV_JP = {"just": "ちょうど", "already": "もう（肯定文）", "yet": "もう（疑問文）／まだ（否定文）", "ever": "今までに", "never": "一度も～ない", "before": "以前に"}


@gen("basic_check", 4, ["condition_check", "common_error"])
def adverb(r):
    jp, s, ok, wrongs = r.choice(ADV)
    return mc(f"日本語に合うように、（　）に入る最も適切な語を選びなさい。\n{jp}\n{s}", [ok] + wrongs,
              f"「{ADV_JP[ok]}」を表すのは {ok}。文の種類（肯定・否定・疑問）と（　）の位置も合っている。", d=1,
              ap="日本語の「ちょうど・もう・まだ・今までに・一度も」と、文が肯定文・否定文・疑問文のどれか、（　）が文中か文末かを確かめる。",
              steps=["文の種類と（　）の位置を確かめる。", f"日本語の意味に合う語を選ぶ：{ok}（{ADV_JP[ok]}）。"],
              alt=["選んだ語を入れた英文を日本語に訳して、問題の日本語と一致するかを確かめる。"],
              pc=[("文の種類・位置を確かめている", 1), ("正しい語を選んでいる", 1)],
              pit=["肯定文の「もう」に yet を使う。", "否定文の「まだ」に already を使う。"],
              why={w: (ADV_WHY[w], "現在完了形とともに使う語の使い分け") for w in wrongs})


# (主語, 答えの代名詞, Have/Has, 残りの部分, 誤った代名詞)
QA = [
    ("you", "I", "Have", "ever been to Okinawa", "you"), ("you", "I", "Have", "finished your homework yet", "you"),
    ("your brother", "he", "Has", "ever climbed Mt. Fuji", "she"), ("Emi", "she", "Has", "eaten lunch yet", "he"),
    ("your parents", "they", "Have", "ever visited Hokkaido", "he"), ("Tom", "he", "Has", "read this book before", "she"),
    ("your sister", "she", "Has", "cleaned her room yet", "he"), ("the train", "it", "Has", "left yet", "he"),
    ("you", "I", "Have", "ever seen a koala", "you"), ("Ms. Green", "she", "Has", "ever eaten natto", "he"),
    ("your friends", "they", "Have", "arrived at the station yet", "he"), ("the movie", "it", "Has", "started yet", "he"),
]


@gen("basic_check", 4, ["concept", "common_error"])
def qa(r):
    s, pr, hv, rest, bad_pr = r.choice(QA)
    yes = r.random() < 0.5
    h = hv.lower()
    pr_h = "has" if pr in ("he", "she", "it") else "have"
    other_h = "have" if pr_h == "has" else "has"
    bad_h = "has" if bad_pr in ("he", "she", "it") else "have"
    ok = f"Yes, {pr} {pr_h}." if yes else f"No, {pr} {NEG[pr_h]}."
    why = {(f"Yes, {pr} did." if yes else f"No, {pr} didn't."): ("現在完了形の疑問文には have / has を使って答える。did は過去形の疑問文の答え。", "過去形と現在完了形の答え方の混同"),
           (f"Yes, {pr} {other_h}." if yes else f"No, {pr} {NEG[other_h]}."): (f"{pr} に合うのは {pr_h}。", "主語と have / has の対応"),
           (f"Yes, {bad_pr} {bad_h}." if yes else f"No, {bad_pr} {NEG[bad_h]}."): (f"{s} を受ける代名詞は {pr}。{'you でたずねられたら自分のことなので I で答える。' if s == 'you' else ''}", "答えの代名詞")}
    yn = "「はい」" if yes else "「いいえ」"
    return mc(f"次の疑問文に{yn}と答えるとき、最も適切なものを選びなさい。\n{hv} {s} {rest}?", [ok] + list(why),
              f"Have / Has で始まる現在完了形の疑問文には、主語を代名詞にして have / has で答える。答え：{ok}", d=2,
              ap="疑問文の最初の語（Have / Has）を見て、答えにも have / has を使う。主語は代名詞にかえる。",
              steps=[f"疑問文は {hv} で始まる現在完了形。", f"主語 {s} を代名詞 {pr} にする。", f"答え：{ok}"],
              alt=[f"答えの省略を補って（{cap(pr)} {pr_h}{'' if yes else ' not'} ～.）、正しい文になるかを確かめる。"],
              pc=[("have / has で答えている", 1), ("代名詞・肯定否定が正しい", 1)],
              pit=["Yes, I did. と過去形で答える。", "you の疑問文に you で答える。"], why=why)


# ======================================================================
# B 標準演習
# ======================================================================

COMBINE = [
    ("I came to Yokohama three years ago. I still live here.", "I have lived in Yokohama for three years.", ["I've lived in Yokohama for three years."], "継続：3年前から今まで住んでいる → for three years"),
    ("It started to rain this morning. It is still raining.", "It has been raining since this morning.", ["It's been raining since this morning."], "動作の継続：雨が今朝から降り続いている → 現在完了進行形"),
    ("Ken lost his watch. He doesn't have it now.", "Ken has lost his watch.", ["Ken's lost his watch."], "完了（結果）：なくして今も持っていない"),
    ("My sister went to Canada. She is not here now.", "My sister has gone to Canada.", [], "完了（結果）：行ってしまって今ここにいない → has gone to"),
    ("I visited Kyoto in 2019. I visited Kyoto again in 2022.", "I have visited Kyoto twice.", ["I've visited Kyoto twice.", "I have been to Kyoto twice."], "経験：2回訪れたことがある → twice"),
    ("Emi became sick last Sunday. She is still sick.", "Emi has been sick since last Sunday.", [], "継続：先週の日曜日から今も病気 → since last Sunday"),
    ("We met Mr. Brown ten years ago. We still know him.", "We have known Mr. Brown for ten years.", ["We've known Mr. Brown for ten years."], "継続（状態の動詞 know）→ have known for ten years"),
    ("Tom started reading this book two hours ago. He is still reading it.", "Tom has been reading this book for two hours.", [], "動作の継続：2時間読み続けている → 現在完了進行形"),
    ("I started to study English when I was ten. I still study it.", "I have studied English since I was ten.", ["I have been studying English since I was ten.", "I've studied English since I was ten."], "継続：10歳のときから今まで → since I was ten"),
    ("My father bought this car in 2015. He still uses it.", "My father has used this car since 2015.", ["My father has been using this car since 2015."], "継続：2015年から今まで使っている → since 2015"),
    ("The children started playing soccer at three o'clock. They are still playing.", "The children have been playing soccer since three o'clock.", [], "動作の継続：3時から今まで → 現在完了進行形＋since"),
    ("Aya started waiting for the bus thirty minutes ago. She is still waiting.", "Aya has been waiting for the bus for thirty minutes.", [], "動作の継続：30分間待ち続けている → 現在完了進行形＋for"),
]


@gen("standard_practice", 4, ["computation", "application"])
def combine(r):
    two, ans, v_, pt = r.choice(COMBINE)
    return sa(f"次の2つの英文が表す内容を、現在完了形または現在完了進行形を使って1文で表しなさい。\n{two}", ans,
              f"{pt}。答え：{ans}", d=2, p=4, v=v_ or None,
              ap="1文目（過去に起きたこと・始まったこと）と2文目（今の状態）をつなぎ、「今まで続いている」「結果が今に残る」「経験の回数」のどれかを考える。",
              steps=["1文目から「いつ始まったか（起きたか）」を読み取る。", "2文目から「今どうなっているか」を読み取る。", f"用法と形を決める：{pt}。", f"答え：{ans}"],
              alt=["書いた文を2つの文にもどして、もとの2文と同じ内容になるかを確かめる。"],
              pc=[("用法に合う形（have / has＋過去分詞、または have / has been＋ing）を使っている", 2), ("for / since などの語句と主語との一致が正しい", 2)],
              pit=["three years ago をそのまま残す（I have lived here three years ago.）。", "期間と起点を取り違えて for / since を逆にする。"])


# (主語, 三人称単数か, 過去形, 過去分詞, 目的語など, 種類 exp / comp)
RW = [
    ("Ken", True, "climbed", "climbed", "Mt. Fuji", "exp"), ("I", False, "saw", "seen", "a koala", "exp"),
    ("My sister", True, "wrote", "written", "a letter in English", "exp"), ("We", False, "ate", "eaten", "Thai food", "exp"),
    ("She", True, "rode", "ridden", "a horse", "exp"), ("They", False, "visited", "visited", "the museum", "exp"),
    ("Tom", True, "read", "read", "this comic book", "exp"),
    ("I", False, "cleaned", "cleaned", "my room", "comp"), ("Ken", True, "did", "done", "his homework", "comp"),
    ("My mother", True, "made", "made", "dinner", "comp"), ("We", False, "bought", "bought", "the tickets", "comp"),
    ("She", True, "sent", "sent", "the e-mail", "comp"), ("They", False, "left", "left", "the station", "comp"),
    ("The movie", True, "started", "started", "", "comp"),
]
RW_MODE = {"exp": ["ever_q", "never"], "comp": ["already", "yet_neg", "yet_q"]}


@gen("standard_practice", 4, ["computation", "condition_check"])
def rewrite(r):
    s, third, past, pp, obj, kind = r.choice(RW)
    mode = r.choice(RW_MODE[kind])
    h = "has" if third else "have"
    o = f" {obj}" if obj else ""
    base = f"{s} {past}{o}."
    if mode == "ever_q":
        ins, ans = "ever を使って「今までに～したことがありますか」とたずねる疑問文", f"{cap(h)} {low(s)} ever {pp}{o}?"
        stp = [f"Have / Has を主語の前に出す → {cap(h)}。", f"ever は主語と過去分詞の間に置く。", f"動詞を過去分詞 {pp} にする。"]
    elif mode == "never":
        ins, ans = "never を使って「一度も～したことがない」という文", f"{s} {h} never {pp}{o}."
        stp = [f"主語に合わせて {h} を置く。", "never を have / has と過去分詞の間に置く（not は不要）。", f"動詞を過去分詞 {pp} にする。"]
    elif mode == "already":
        ins, ans = "already を使って「もう～してしまった」という文", f"{s} {h} already {pp}{o}."
        stp = [f"主語に合わせて {h} を置く。", "already を have / has と過去分詞の間に置く。", f"動詞を過去分詞 {pp} にする。"]
    elif mode == "yet_neg":
        ins, ans = "yet を使って「まだ～していない」という文", f"{s} {NEG[h]} {pp}{o} yet."
        stp = [f"否定文なので {NEG[h]} を使う（do / does / did は使わない）。", f"動詞を過去分詞 {pp} にする。", "yet を文末に置く。"]
    else:
        ins, ans = "yet を使って「もう～しましたか」とたずねる疑問文", f"{cap(h)} {low(s)} {pp}{o} yet?"
        stp = [f"Have / Has を主語の前に出す → {cap(h)}。", f"動詞を過去分詞 {pp} にする。", "yet を文末に置く。"]
    v_ = None
    if mode == "yet_neg":
        v_ = [f"{s} {h} not {pp}{o} yet."]
    return sa(f"次の英文を、{ins}に書きかえなさい。\n{base}", ans, f"現在完了形〈have / has＋過去分詞〉にし、語の位置に注意する。答え：{ans}", d=2, p=4, v=v_,
              ap="過去形の動詞を〈have / has＋過去分詞〉にかえてから、ever / never / already / yet をそれぞれ決まった位置に置く。",
              steps=stp + [f"答え：{ans}"],
              alt=["書きかえた文を日本語に訳し、指示された意味（今までに・一度も・もう・まだ）になっているかを確かめる。"],
              pc=[("have / has＋過去分詞の形が正しい", 2), ("ever / never / already / yet の位置が正しい", 2)],
              pit=["過去形 did / ate などをそのまま残す。", "yet を have と過去分詞の間に置く。"])


# (疑問詞, have/has, 主語, 過去分詞（や been ing）, 誤りの原形部分, 残り, B の答え)
HL = [
    ("How long", "have", "you", "lived", "live", "in this city", ["For five years.", "Since 2019.", "For about ten years."]),
    ("How long", "has", "your sister", "played", "play", "the violin", ["Since she was six.", "For eight years."]),
    ("How long", "have", "you", "been", "be", "in Japan", ["For two months.", "Since last April."]),
    ("How long", "has", "Mr. Smith", "taught", "teach", "at this school", ["For three years.", "Since 2021."]),
    ("How long", "have", "you", "been waiting", "wait", "here", ["For thirty minutes.", "Since ten o'clock."]),
    ("How many times", "have", "you", "been", "be", "to Kyoto", ["Three times.", "Twice.", "Only once."]),
    ("How many times", "has", "Ken", "seen", "see", "the movie", ["Four times.", "Twice."]),
    ("How many times", "have", "you", "climbed", "climb", "Mt. Fuji", ["Once.", "Three times."]),
    ("How many times", "has", "your father", "visited", "visit", "Okinawa", ["Five times.", "Many times."]),
]


@gen("standard_practice", 4, ["cross_unit", "concept"], rel=["JH-ENG-G1-U03"])
def how_long_many(r):
    qw, h, s, pp, base, rest, answers = r.choice(HL)
    b = r.choice(answers)
    oh = "has" if h == "have" else "have"
    other_qw = "How many times" if qw == "How long" else "How long"
    ok = f"{qw} {h} {s} {pp} {rest}?"
    base_s = f"{qw} {h} {s} {base} {rest}?"
    why = {f"{other_qw} {h} {s} {pp} {rest}?": (f"B は「{b}」と{'期間・起点' if qw == 'How long' else '回数'}を答えているので、{qw} でたずねる。{other_qw} では答えと合わない。", "疑問詞と答えの対応"),
           base_s: (f"have / has の後ろは過去分詞（{pp.split()[0]}）。{base} では現在完了形にならない。", "過去分詞の形"),
           f"{qw} {oh} {s} {pp} {rest}?": (f"主語 {s} に合うのは {h}。", "主語と have / has の対応")}
    return mc(f"次の対話が成り立つように、A の（　）に入る最も適切なものを選びなさい。\nA：(　　)\nB：{b}", [ok] + list(why),
              f"B の答え「{b}」は{'期間・起点' if qw == 'How long' else '回数'}なので、A は {qw} ＋ 現在完了形の疑問文でたずねる。答え：{ok}", d=3,
              ap="B の答えが for / since（期間・起点）か、～ times / once / twice（回数）かを見て疑問詞を決める。後ろは現在完了形の疑問文の語順。",
              steps=[f"B の答え {b} → {'期間・起点' if qw == 'How long' else '回数'} → {qw}。", f"主語 {s} に合わせて {h}、動詞は過去分詞。", f"答え：{ok}"],
              alt=["選んだ疑問文に B の答えを当てはめて、ふつうの文（I have lived ～ for five years. など）にもどせるかを確かめる。"],
              pc=[("疑問詞を正しく選んでいる", 2), ("現在完了形の疑問文の語順・形を選んでいる", 2)],
              pit=["How long と How many times を取り違える。", "疑問詞の後ろを did＋原形にする。"], why=why)


PROG = [
    ("私は2時間ずっと数学を勉強しています。", "I (　　) math for two hours.", "have been studying",
     [("am studying", "am studying は「今」だけを表し、2時間続いていることは表せない。過去から今までの継続は現在完了進行形。"),
      ("have studying", "現在完了進行形には been が必要。have been＋ing 形の3つがセット。"),
      ("have been study", "been の後ろは ing 形。study のままでは進行形にならない。")]),
    ("私はケンを10年間知っています。", "I (　　) Ken for ten years.", "have known",
     [("have been knowing", "know は状態を表す動詞なので進行形にしない。継続は現在完了形 have known で表す。"),
      ("am knowing", "know は進行形にしない動詞。また am では「今」しか表せない。"),
      ("know", "現在形 know では for ten years（10年間ずっと）という継続を表せない。")]),
    ("今朝からずっと雪が降っています。", "It (　　) since this morning.", "has been snowing",
     [("is snowing", "is snowing は「今」だけを表し、since this morning（今朝から今まで）とは使えない。"),
      ("has snowing", "現在完了進行形には been が必要。"),
      ("have been snowing", "主語 It は三人称単数なので has。")]),
    ("子どもたちは1時間ずっと公園で遊んでいます。", "The children (　　) in the park for an hour.", "have been playing",
     [("has been playing", "主語 The children は複数なので have。"),
      ("are playing", "are playing は「今」だけを表し、1時間続いていることは表せない。"),
      ("have been play", "been の後ろは ing 形。")]),
    ("姉は去年から新しいかばんをほしがっています。", "My sister (　　) a new bag since last year.", "has wanted",
     [("has been wanting", "want は状態を表す動詞なので、ふつう進行形にしない。継続は has wanted で表す。"),
      ("is wanting", "want は進行形にしない動詞。また is では since last year とつながらない。"),
      ("wants", "現在形 wants では since last year（去年から今まで）という継続を表せない。")]),
    ("あなたはどのくらいの間ここで待っているのですか。", "How long (　　) here?", "have you been waiting",
     [("are you waiting", "How long ～ で今までの継続をたずねるときは現在完了進行形を使う。are you waiting では「今」しか表せない。"),
      ("have you waiting", "been が抜けている。have＋主語＋been＋ing 形にする。"),
      ("did you wait", "did you wait は過去に終わったことをたずねる文で、今も待っている場面に合わない。")]),
    ("父は朝からずっと車を洗っています。", "My father (　　) his car since this morning.", "has been washing",
     [("is washing", "is washing は「今」だけを表し、since this morning とは使えない。"),
      ("has washing", "現在完了進行形には been が必要。"),
      ("have been washing", "主語 My father は三人称単数なので has。")]),
    ("私たちは5年間おたがいを知っています。", "We (　　) each other for five years.", "have known",
     [("have been knowing", "know は状態を表す動詞なので進行形にしない。"),
      ("are knowing", "know は進行形にしない動詞。"),
      ("knew", "過去形 knew は過去のことだけを表し、今も知っていることを表せない。")]),
    ("トムは3時間ずっとテレビゲームをしています。", "Tom (　　) video games for three hours.", "has been playing",
     [("is playing", "is playing は「今」だけを表し、3時間続いていることは表せない。"),
      ("has been play", "been の後ろは ing 形。"),
      ("has playing", "現在完了進行形には been が必要。")]),
    ("ケンは子どものころからずっとサッカーが好きです。", "Ken (　　) soccer since he was a child.", "has liked",
     [("has been liking", "like は状態（気持ち）を表す動詞なので、ふつう進行形にしない。継続は has liked で表す。"),
      ("is liking", "like は進行形にしない動詞。また is では since he was a child とつながらない。"),
      ("likes", "現在形 likes では since he was a child（子どものころから今まで）という継続を表せない。")]),
]


@gen("standard_practice", 4, ["condition_check", "concept"])
def perf_prog(r):
    jp, s, ok, wrongs = r.choice(PROG)
    return mc(f"日本語に合うように、（　）に入る最も適切なものを選びなさい。\n{jp}\n{s}", [ok] + [w for w, _ in wrongs],
              f"動作が今まで続いているときは have / has been＋ing 形、状態（know / want / belong など）が続いているときは have / has＋過去分詞。答え：{ok}", d=2,
              ap="動詞が「動作」か「状態」かを先に判断する。動作の継続 → 現在完了進行形、状態の継続 → 現在完了形。",
              steps=["動詞が動作か状態かを判断する。", "主語に合わせて have / has を決める。", f"答え：{ok}"],
              alt=["「～しているところだ」と言いかえて自然なら動作の動詞、不自然（「知っているところだ」）なら状態の動詞と確かめる。"],
              pc=[("動作・状態を判断している", 2), ("正しい形を選んでいる", 2)],
              pit=["know / want を進行形にする。", "been を落とす（have studying）。"],
              why={w: (reason, "現在完了進行形と現在完了形の使い分け") for w, reason in wrongs})


ORDERS = [
    ("私は3年間ずっとこの町に住んでいます。", ["I", "have", "lived", "in", "this town", "for", "three years"]),
    ("あなたは今までに北海道に行ったことがありますか。", ["have", "you", "ever", "been", "to", "Hokkaido"]),
    ("私はちょうど夕食を食べたところです。", ["I", "have", "just", "eaten", "dinner"]),
    ("彼女はまだその手紙を読んでいません。", ["she", "hasn't", "read", "the letter", "yet"]),
    ("兄は一度も海外に行ったことがありません。", ["my brother", "has", "never", "been", "abroad"]),
    ("あなたはどのくらいの間、英語を勉強しているのですか。", ["how long", "have", "you", "studied", "English"]),
    ("今朝からずっと雨が降っています。", ["it", "has", "been", "raining", "since", "this morning"]),
    ("私たちは1時間ずっとバスを待っています。", ["we", "have", "been", "waiting", "for", "the bus", "for an hour"]),
    ("その電車はもう出発してしまいました。", ["the train", "has", "already", "left"]),
    ("あなたはその映画を何回見たことがありますか。", ["how many times", "have", "you", "seen", "the movie"]),
    ("ケンは子どものころからずっとサッカーが好きです。", ["Ken", "has", "liked", "soccer", "since", "he was a child"]),
    ("あなたはもう部屋をそうじしましたか。", ["have", "you", "cleaned", "your room", "yet"]),
]


@gen("standard_practice", 4, ["application", "computation"])
def build_order(r):
    jp, parts = r.choice(ORDERS)
    sent = cap(" ".join(parts)) + ("?" if jp.endswith("か。") else ".")
    return order(f"日本語に合うように、次の語句を並べかえて英文を完成させなさい。ただし、文頭にくる語も小文字で示してある。\n{jp}", parts,
                 f"{sent}　ポイント：have / has＋過去分詞（進行形なら been＋ing 形）を骨組みにし、ever / never / just / already は have と過去分詞の間、yet・for ～・since ～ は後ろに置く。", d=2, p=4,
                 ap="日本語から用法（継続・経験・完了・現在完了進行形）を判断し、主語＋have / has＋過去分詞の骨組みを先に作る。",
                 steps=["主語と have / has（疑問文なら Have / Has を先頭、疑問詞があればその後ろ）を決める。", "ever / never / just / already を過去分詞の前に置く。", "目的語、for / since の句、yet を後ろに置く。", f"完成文：{sent}"],
                 alt=["完成した英文を日本語に訳し直して、問題の日本語と一致するかを確かめる。"],
                 pc=[("have / has と過去分詞の骨組みが正しい", 2), ("副詞・for / since の句の位置が正しい", 2)],
                 pit=["yet を文の途中に置く。", "疑問文で have を主語の後ろに置いたままにする。"])


# ======================================================================
# C 思考力・記述応用
# ======================================================================

PAIRS = [
    ("I lost my key.", "I have lost my key.",
     "A は過去形で「かぎをなくした」という過去のできごとだけを述べ、今かぎがあるかどうかはわからない（見つかったかもしれない）。B は現在完了形（完了・結果）で「かぎをなくしてしまって、今も持っていない」という今の状態まで表している。"),
    ("I lived in Osaka for five years.", "I have lived in Osaka for five years.",
     "A は過去形で「（以前）5年間大阪に住んでいた」という意味で、今は大阪に住んでいない。B は現在完了形（継続）で「5年間ずっと大阪に住んでいて、今も住んでいる」という意味。"),
    ("Ken has been to Canada.", "Ken has gone to Canada.",
     "A の has been to は経験で「ケンはカナダに行ったことがある」の意味で、ケンは今ここにいてもよい。B の has gone to は「ケンはカナダに行ってしまった（今ここにいない）」という結果を表す。"),
    ("I finished my homework an hour ago.", "I have just finished my homework.",
     "A は過去形で、an hour ago（1時間前）という過去の一時点に宿題を終えたことを述べている。B は現在完了形（完了）で「ちょうど今、宿題を終えたところだ」と今とのつながりを表す。an hour ago のような過去の一時点の語句は現在完了形とは使えない。"),
    ("Did you see the movie yesterday?", "Have you ever seen the movie?",
     "A は過去形の疑問文で「昨日その映画を見たか」と過去の一時点のことをたずねている。B は現在完了形（経験）の疑問文で「今までにその映画を見たことがあるか」と、今までの経験をたずねている。"),
    ("It rained yesterday.", "It has been raining since yesterday.",
     "A は過去形で「昨日雨が降った」という過去のできごとだけを表し、今降っているかはわからない。B は現在完了進行形で「昨日からずっと雨が降り続いていて、今も降っている」ことを表す。"),
    ("I am reading this book.", "I have been reading this book for two hours.",
     "A は現在進行形で「今この本を読んでいる」と、今の動作だけを表す。B は現在完了進行形で「2時間前から今までずっとこの本を読み続けている」と、動作が続いている期間まで表している。"),
    ("When did you come to Japan?", "How long have you been in Japan?",
     "A は過去形で、日本に来た過去の一時点（いつ来たか）をたずねている。When は過去の一時点をたずねるので現在完了形とは使わない。B は現在完了形（継続）で、日本に来てから今までの期間（どのくらいいるか）をたずねている。"),
]


@gen("thinking_writing", 4, ["cross_unit", "written_reasoning"], rel=["JH-ENG-G1-U05", "JH-ENG-G1-U04"])
def explain_pair(r):
    a, b, model = r.choice(PAIRS)
    return desc(f"次の2つの英文 A・B の意味の違いを、動詞の形（過去形・現在完了形・進行形など）に注目して日本語で説明しなさい。\nA：{a}\nB：{b}", model,
                "過去形は過去の一時点のことだけ、現在完了形は過去のことが今とつながっていること、進行形は動作の途中であることを表す。",
                [("A の形と意味を正しく説明している", 3), ("B の形と意味を正しく説明している", 3), ("「今とのつながり」の有無など、違いの核心を指摘している", 2)], d=3, p=8, lines=5,
                ap="2つの文の動詞の部分に下線を引き、それぞれが過去形・現在完了形・進行形のどれかを確かめる。そのうえで「今どうなっているか」がわかるかどうかを比べる。",
                steps=["A と B の動詞の形を確認する。", "それぞれが表す時間（過去の一点／過去から今まで／今の途中）を時間軸で考える。", "和訳を示して、違いの核心を説明する。"],
                alt=["時間軸の図をかいて、A は点、B は矢印（今まで）として表し、図をもとに説明する方法もある。"],
                pc=[("A の説明", 3), ("B の説明", 3), ("違いの核心", 2)],
                pit=["和訳だけを書き、どの形が違いを生んでいるかを書かない。", "過去形の文も「今も続いている」と説明してしまう。"])


CHOOSE = [
    ("I (visit) Kyoto last year.", "visited", "last year は過去の一時点を表すので、現在完了形ではなく過去形 visited を使う。"),
    ("I (visit) Kyoto three times.", "have visited", "three times は経験の回数を表すので、現在完了形（経験）have visited を使う。"),
    ("When (you, come) to Japan?", "did you come", "When は過去の一時点をたずねる疑問詞なので現在完了形とは使えない。過去形の疑問文 did you come にする。"),
    ("I (know) Ms. Green since 2018.", "have known", "since 2018 は「2018年から今まで」の継続。know は状態の動詞なので進行形にせず、現在完了形 have known を使う。"),
    ("She (wait) for the bus for twenty minutes.", "has been waiting", "wait は動作の動詞で、20分間今まで続いているので現在完了進行形 has been waiting を使う。主語が三人称単数なので has。"),
    ("My father (go) to London two weeks ago.", "went", "two weeks ago は過去の一時点を表すので、過去形 went を使う。"),
    ("We (be) friends since we were children.", "have been", "since we were children は「子どものころから今まで」の継続。be の過去分詞 been を使い have been にする。"),
    ("Tom (read) a book in his room since lunch.", "has been reading", "read は動作の動詞で、昼食のときから今まで続いているので現在完了進行形 has been reading を使う。"),
    ("(you, finish) your homework yet?", "Have you finished", "yet は疑問文で「もう」を表し、完了用法の目印になる。現在完了形の疑問文 Have you finished にする。"),
    ("I (see) a famous singer at the station yesterday.", "saw", "yesterday は過去の一時点を表すので、過去形 saw を使う。"),
]


@gen("thinking_writing", 2, ["condition_check", "written_reasoning"])
def choose_tense(r):
    s, ans, why_s = r.choice(CHOOSE)
    return desc(f"次の英文の（　）内の語を、適切な形（過去形・現在完了形・現在完了進行形のいずれか）に直しなさい。また、その形を選んだ理由を、文中の語句を根拠にして説明しなさい。\n{s}",
                f"{ans}　理由：{why_s}",
                "文中の時を表す語句（yesterday / ～ ago / last ～ / When は過去形、for / since / ever / ～ times / yet などは現在完了形）と、動詞が動作か状態かで形を決める。",
                [("正しい形を書いている", 4), ("根拠になる語句を挙げている", 2), ("その語句が過去の一時点か、今までを含むかを説明している", 2)], d=4, p=8, lines=4,
                ap="まず文中の「時を表す語句」に印をつけ、それが過去の一時点だけを表すのか、今までを含むのかを判断する。",
                steps=["時を表す語句（または疑問詞）を見つける。", "過去の一時点 → 過去形、今までを含む → 現在完了形。", "継続のときは、動作の動詞なら現在完了進行形、状態の動詞なら現在完了形。", f"答え：{ans}"],
                alt=["時間軸の図に、その語句が「点」か「今までの線」かをかいて確かめる。"],
                pc=[("形", 4), ("根拠の語句", 2), ("理由の説明", 2)],
                pit=["yesterday や ago があるのに現在完了形にする。", "状態の動詞（know / be）を現在完了進行形にする。"])


WRITE = [
    ("日本に来たばかりの留学生に、あなたの町について紹介する。",
     "I have lived in this town for ten years. I have visited the old temple near the station many times.",
     "1文目は継続（have lived ～ for ten years）、2文目は経験（have visited ～ many times）を使っている。"),
    ("英語の授業で、あなたが続けている習い事について話す。",
     "I have played the piano since I was six. I have been practicing a new song for two weeks.",
     "1文目は since を使った継続、2文目は現在完了進行形で今も続けている練習を表している。"),
    ("海外の友だちに、あなたがしたことのある経験を伝える。",
     "I have been to Hokkaido twice. I have never seen such beautiful snow before.",
     "1文目は have been to を使った経験、2文目は never を使った経験（一度も～ない）を表している。"),
    ("友だちに、待ち合わせ場所でずっと待っていることを電話で伝える。",
     "I have been waiting at the station for thirty minutes. The train has not come yet.",
     "1文目は現在完了進行形で待ち続けていること、2文目は yet を使った完了（まだ～していない）を表している。"),
    ("先生に、宿題の進み具合を報告する。",
     "I have already finished the math homework. I haven't started the English essay yet.",
     "1文目は already を使った完了、2文目は yet を使った否定（まだ～していない）を表している。"),
    ("ALT の先生に、あなたの好きな本について話す。",
     "I have read this book three times. I have liked the main character since I first read it.",
     "1文目は ～ times を使った経験、2文目は since を使った継続（状態の動詞 like）を表している。"),
    ("部活動の新入部員に、自分の部活動での経験を伝える。",
     "I have been a member of the tennis team for two years. Our team has won three games this year.",
     "1文目は be の継続（have been ～ for two years）、2文目は this year（今年＝今を含む期間）での完了・経験を表している。"),
    ("オンライン交流で、日本の食べ物の経験をたずねる。",
     "Have you ever eaten okonomiyaki? I have made it with my family many times.",
     "1文目は ever を使った経験の疑問文、2文目は many times を使った経験を表している。"),
]


@gen("thinking_writing", 4, ["application", "written_reasoning"])
def write_exp(r):
    sit, model, point = r.choice(WRITE)
    return desc(f"次の場面で伝える英文を2文で書きなさい。ただし、2文とも現在完了形または現在完了進行形を使い、2文で異なる用法（継続・経験・完了・現在完了進行形）を使うこと。\n場面：{sit}",
                f"（解答例）{model}", f"（解答例の解説）{point}",
                [("1文目が現在完了形（進行形）の正しい文で、場面に合っている", 3), ("2文目が1文目と異なる用法の正しい文で、内容がつながっている", 3), ("過去分詞・have / has・for / since などの表記が正しい", 2)], d=4, p=8, lines=4,
                ap="まず日本語で「ずっと続いていること」「したことがあること」「もう・まだのこと」から2つを選び、それぞれに合う目印の語（for / since / ever / never / ～ times / already / yet）を決める。",
                steps=["場面に合う内容を日本語で2つ決め、それぞれの用法を決める。", "主語＋have / has＋過去分詞（または been＋ing）の骨組みを作る。", "目印の語を正しい位置に置き、2文のつながりを見直す。"],
                alt=["書いた2文に yesterday / ago など過去の一時点の語句がまざっていないかを最後に確かめる。"],
                pc=[("1文目", 3), ("2文目", 3), ("表記の正確さ", 2)],
                pit=["2文とも同じ用法になる。", "現在完了形の文に ago や last ～ を入れる。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(task, wrong, step, etype, tempt, fix, expl, steps, ap, alt, pit):
    return desc(f"{task}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい英文に書き直しなさい。", fix, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい英文に直している", 3), ("文法のルールを説明している", 1)], d=3, p=6, lines=4,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい英文", 3), ("ルールの説明", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix))


FORM_ERR = [
    ("私は5年間名古屋に住んでいます。", "I have live in Nagoya for five years.", "I have lived in Nagoya for five years.", "live", "formula",
     "have の後ろは過去分詞。live → lived。", "have の後ろに原形を置けると考えた。"),
    ("兄はもう宿題を終えました。", "My brother have already finished his homework.", "My brother has already finished his homework.", "have", "condition",
     "主語 My brother は三人称単数なので has。", "主語の数を確かめずに have を使った。"),
    ("私は去年北海道を訪れました。", "I have visited Hokkaido last year.", "I visited Hokkaido last year.", "have visited ～ last year", "condition",
     "last year は過去の一時点を表すので、現在完了形とは使えない。過去形 visited にする。", "日本語の「訪れた」を完了と考えた。"),
    ("あなたはいつ日本に来たのですか。", "When have you come to Japan?", "When did you come to Japan?", "When have you come", "condition",
     "When は過去の一時点をたずねる疑問詞なので現在完了形とは使えない。過去形の疑問文にする。", "「来た」を完了の意味と考えた。"),
    ("ケンはその映画を2回見たことがあります。", "Ken has saw the movie twice.", "Ken has seen the movie twice.", "saw", "formula",
     "has の後ろは過去分詞。see の過去分詞は seen。saw は過去形。", "過去のことなので過去形を使えばよいと考えた。"),
    ("私は5年間ここに住んでいます。", "I have lived here since five years.", "I have lived here for five years.", "since", "condition",
     "five years は期間なので for を使う。since の後ろには起点を置く。", "日本語の「～間」と「～から」の区別を考えなかった。"),
    ("今朝からずっと雨が降っています。", "It has raining since this morning.", "It has been raining since this morning.", "has raining", "formula",
     "現在完了進行形は has been＋ing 形。been が必要。", "has と ing 形だけで進行の意味になると考えた。"),
    ("私は2015年から彼女を知っています。", "I have known her for 2015.", "I have known her since 2015.", "for", "condition",
     "2015 は起点（いつから）なので since を使う。", "「～から」を for で表せると考えた。"),
    ("あなたは今までに沖縄に行ったことがありますか。", "Have you ever went to Okinawa?", "Have you ever been to Okinawa?", "went", "formula",
     "have の後ろは過去分詞。「～へ行ったことがある」は have been to ～ で表す。went は過去形。", "「行った」を過去形 went で表そうとした。"),
    ("私はもう昼食を食べました。", "I have ate lunch already.", "I have already eaten lunch.", "ate", "formula",
     "have の後ろは過去分詞 eaten。ate は過去形。already は have と過去分詞の間に置くのがふつう。", "過去形と過去分詞を区別していなかった。"),
    ("私はちょうど1時間前に宿題を終えました。", "I have just finished my homework an hour ago.", "I finished my homework an hour ago.", "have ～ an hour ago", "condition",
     "an hour ago は過去の一時点を表すので現在完了形とは使えない。過去形 finished にする（just も不要）。", "「終えた」を完了の意味と考え、ago と組み合わせた。"),
]


@gen("error_correction", 5, ["common_error", "condition_check"])
def err_form(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(FORM_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", etype, tempt, fix, f"{rule}正しくは {fix}",
                    ["have / has と過去分詞の形が正しいかを確認する。", "過去の一時点を表す語句（yesterday / ago / last ～ / When）や for / since の使い方を確認する。", f"正しい英文：{fix}"],
                    "現在完了形は「主語に合う have / has」「正しい過去分詞」「今とつながる語句」の3点をそろえる。過去の一時点の語句があれば過去形にする。",
                    ["時間軸の図をかいて、文が表す時間が「過去の一点」か「今まで」かを確かめる。"],
                    ["過去分詞の代わりに過去形を置く。", "過去の一時点の語句と現在完了形をいっしょに使う。"])


USE_ERR = [
    ("私は10年間彼を知っています。", "I have been knowing him for ten years.", "I have known him for ten years.", "have been knowing", "concept",
     "know は状態を表す動詞なので進行形にしない。継続は現在完了形 have known で表す。", "日本語の「知っている」の「～している」につられて進行形にした。"),
    ("私は以前奈良を訪れたことがあります。", "I have ever visited Nara.", "I have visited Nara before.", "ever", "condition",
     "ever（今までに）は疑問文で使い、肯定文には使わない。「以前に」は before を文末に置く。", "「～したことがある」には必ず ever が必要だと考えた。"),
    ("私はまだ宿題を終えていません。", "I haven't finished my homework already.", "I haven't finished my homework yet.", "already", "condition",
     "否定文の「まだ」は yet を文末に置く。already は肯定文で「もう」を表す。", "「まだ・もう」をどちらも already で表せると考えた。"),
    ("「もう宿題を終えましたか。」「はい、終えました。」", "Have you finished your homework yet? ― Yes, I did.", "Have you finished your homework yet? ― Yes, I have.", "I did", "concept",
     "Have で始まる現在完了形の疑問文には have を使って答える。", "「終えました」が過去の意味なので did を使った。"),
    ("私はオーストラリアに2回行ったことがあります。", "I have gone to Australia twice.", "I have been to Australia twice.", "have gone", "interpretation",
     "中学では「～へ行ったことがある」という経験は have been to ～ で表す。have gone to は、ふつう「行ってしまって今ここにいない」という結果の意味で使う。", "go の過去分詞 gone をそのまま使えばよいと考えた。"),
    ("「どのくらいここに住んでいますか。」「3年間です。」", "How long have you lived here? ― Since three years.", "How long have you lived here? ― For three years.", "Since", "condition",
     "three years は期間なので For を使う。", "「～前から」を since で表そうとした。"),
    ("母は2時間ずっと台所を掃除しています。", "My mother has been cleaning the kitchen since two hours.", "My mother has been cleaning the kitchen for two hours.", "since", "condition",
     "two hours は期間なので for を使う。", "「～前から」を since で表そうとした。"),
    ("あなたは今までにコアラを見たことがありますか。", "Did you have ever seen a koala?", "Have you ever seen a koala?", "Did you have", "concept",
     "現在完了形の疑問文は Have を主語の前に出す。did は使わない。", "疑問文には do / does / did が必要だと考えた。"),
    ("私は一度もその歌を聞いたことがありません。", "I haven't never heard the song.", "I have never heard the song.", "haven't never", "logic",
     "never だけで「一度も～ない」という否定になる。not（n't）と重ねない。", "日本語の「ない」を not と never の両方で表した。"),
    ("トムは今、2時間ずっと本を読んでいます。", "Tom is reading a book for two hours.", "Tom has been reading a book for two hours.", "is reading", "concept",
     "for two hours（2時間ずっと）と今まで続いている動作は、現在完了進行形 has been reading で表す。is reading は「今」だけを表す。", "「今」という日本語につられて現在進行形にした。"),
]


@gen("error_correction", 5, ["common_error", "concept"])
def err_usage(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(USE_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", etype, tempt, fix, f"{rule}正しくは {fix}",
                    ["ever / never / already / yet / for / since の使い方が文の種類・意味に合っているかを確認する。", "動詞が状態か動作か、疑問文の答え方が正しいかを確認する。", f"正しい英文：{fix}"],
                    "目印の語（ever / never / already / yet / for / since）は、文の種類（肯定・否定・疑問）と意味で使い分ける。答えは have / has で、状態の動詞は進行形にしない。",
                    ["直した文を日本語に訳し直して、問題の日本語と同じ意味になるかを確かめる。"],
                    ["肯定文に ever / yet を使う。", "状態の動詞を現在完了進行形にする。"])


GENERATORS = [have_form, for_since, usage_type, adverb, qa,
              combine, rewrite, how_long_many, perf_prog, build_order,
              explain_pair, choose_tense, write_exp,
              err_form, err_usage]
