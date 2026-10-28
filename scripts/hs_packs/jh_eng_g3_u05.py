"""単元パック：中学3年 英語 仮定法過去。"""
from banks._common import desc, mc, order, sa
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem,
                         tp)

UNIT_ID = "JH-ENG-G3-U05"

PREREQUISITES = [
    ("JH-ENG-G2-U03", "接続詞 if（もし～ならば）。If it rains tomorrow, I will stay home. のような「実際に起こりうる条件」の文と比べて、仮定法の意味をとらえる。"),
    ("JH-ENG-G1-U05", "過去形（規則動詞・不規則動詞・be 動詞の過去形）。仮定法過去では、現在のことでも動詞を過去形にする。"),
    ("JH-ENG-G2-U01", "未来表現 will。仮定法の主節では will の過去形 would を使う。"),
    ("JH-ENG-G1-U04", "助動詞 can。仮定法の主節や I wish の文では can の過去形 could を使う。"),
]
EXTENSIONS = [
    ("JH-ENG-G3-U07", "条件英作文で、If I were ～, I would ―. を使って「もし～なら何をするか」という自分の考えを書く。"),
    ("JH-ENG-G3-U06", "スピーチや物語文の中で、I wish ～ や If ～ could ― が表す話し手の気持ち（残念さ・願い）を読み取る。"),
    ("HS-ENG-U06", "高校では、過去の事実に反する仮定法過去完了（If I had known, I would have ～）や、as if、without ～ などの表現へ発展する。"),
]


# ======================================================================
# 授業プリント
# ======================================================================

LESSON = lesson(
    goals=["現在の事実と違うことを仮定する〈If＋主語＋動詞の過去形 ～, 主語＋would / could＋動詞の原形 ….〉を作り、意味を説明できる。",
           "〈I wish＋主語＋動詞の過去形（were / could）〉で、現在の事実と違う願望を表せる。",
           "実際に起こりうる条件（直説法：If it rains tomorrow, I will ～）と、事実と違う仮定（仮定法）を区別して使い分けられる。"],
    duration=50,
    readiness=["規則動詞・不規則動詞の過去形と、be 動詞の過去形 was / were を正しく使える（中1）。",
               "接続詞 if を使って「もし～ならば」の文を作れる（中2）。",
               "will / can の意味と使い方を理解している（中1・中2）。",
               "小学校の国語で、「もし～だったら」という空想の話（物語）を読んだり書いたりしている。"],
    flow=[("導入：「もし鳥だったら」", 5, "I'm not a bird. という事実と If I were a bird, I could fly to you. を比べ、現在のことに過去形を使う点に気づかせる"),
          ("If を使った仮定法過去", 15, "If＋過去形, would / could＋原形。be 動詞は were（例題1）"),
          ("I wish ～", 10, "I wish＋過去形（were / could / had）で現在の事実と違う願望（例題2）"),
          ("仮定法と直説法", 12, "If it rains tomorrow, I will ～ と If I were ～, I would ～ の違い（例題3）"),
          ("まとめと確認", 8, "板書の3列で整理し、確認問題3問")],
    sections=[
        intro("in1", "「現実」と「空想」で動詞の形が変わる",
              "「もし私が鳥だったら、あなたのところへ飛んでいけるのに」。実際には私は鳥ではありません。英語では、このように現在の事実と違うことを仮定するとき、現在のことなのに動詞を過去形にします。過去形にすることで、「これは現実ではない、空想の話だ」という合図を相手に送るのです。この形を仮定法過去といいます。",
              bullets=["事実：I am not a bird, so I can't fly to you.（私は鳥ではないので、あなたのところへ飛んでいけない）",
                       "仮定：If I were a bird, I could fly to you.（もし私が鳥なら、あなたのところへ飛んでいけるのに）",
                       "願望：I wish I were a bird.（私が鳥ならいいのに）"],
              points=[tp("事実の文と仮定の文を上下に並べ、am → were、can → could と「1つずつ過去に下がっている」ことを矢印で示す。",
                         ask="If I were a bird の文は、過去の話をしているのか。", expect="いいえ。今の話だけれど、事実と違うので過去形になっている。",
                         timing="導入の冒頭")]),
        definition("df1", "仮定法過去〈If＋過去形, would / could＋原形〉",
                   "現在の事実と違うことや、実際には起こりそうにないことを「もし～なら、…だろうに」と仮定する文です。if の中の動詞を過去形にし、もう一方の文（主節）には would（～するだろう）や could（～できるだろう）＋動詞の原形を使います。",
                   formula="If＋主語＋動詞の過去形 ～, 主語＋would / could＋動詞の原形 ….",
                   bullets=["If I had a car, I would drive you home.（車を持っていれば、家まで送るのに：実際は持っていない）",
                            "If I were you, I would ask the teacher.（もし私があなたなら、先生にたずねるだろう：助言）",
                            "If she knew his address, she could write to him.（住所を知っていれば、手紙を書けるのに）",
                            "I would help you if I had time.（if の部分を後ろに置いてもよい。そのときはコンマ不要）"],
                   conditions=["be 動詞は、主語が I / he / she / it でも were を使うのが基本（If I were ～、If he were ～）。",
                               "主節の would / could の後ろは動詞の原形：× would went、× could flew。",
                               "主節に will / can（現在形）を使うと、実際に起こりうる条件の文（直説法）になる。"],
                   points=[tp("「if の中は過去形、主節は would / could＋原形」の2点セットで覚えさせる。片方だけ過去にする誤りが多い。",
                              ask="If I had a car, I will drive you home. はどこがおかしいか。", expect="仮定法なので will ではなく would。",
                              caution="If I were ～ の were を「過去のことだから」と説明しない。現在の事実と違うことを表す合図だと強調する。", timing="定義の説明後")]),
        definition("df2", "I wish＋仮定法過去",
                   "〈I wish＋主語＋動詞の過去形 ～〉で、「（実際はそうではないが）～ならいいのに」という、現在の事実と違う願望を表します。そうではないことへの残念な気持ちがこめられます。",
                   formula="I wish＋主語＋動詞の過去形（were / had / could＋原形 など）",
                   bullets=["I wish I were taller.（もっと背が高ければいいのに：実際は高くない）",
                            "I wish I had a brother.（兄弟がいればいいのに：実際はいない）",
                            "I wish I could speak French.（フランス語を話せたらいいのに：実際は話せない）"],
                   conditions=["wish の後ろは仮定法なので、現在形（am / have / can）にしない。",
                               "実現の可能性があることを望むときは、I hope ～（I hope it will be sunny tomorrow.）を使う。"],
                   points=[tp("hope と wish の違いを、天気の例で比べる。I hope it will be sunny tomorrow.（晴れるといいな：可能性あり）と I wish it were sunny today.（今日晴れていればいいのに：実際は雨）。",
                              ask="明日の遠足が晴れることを願うときは hope と wish のどちらか。", expect="hope。晴れる可能性があるから。")]),
        theorem("th1", "仮定法と直説法の使い分け",
                "実際に起こりうる → 直説法（If＋現在形, will / can ～）　｜　事実と違う・ありえない → 仮定法（If＋過去形, would / could ～）",
                ["直説法：If it is sunny tomorrow, we will go on a picnic.（明日晴れたら、ピクニックに行く：晴れる可能性がある）",
                 "仮定法：If it were sunny today, we would go on a picnic.（今日晴れていたら、ピクニックに行くのに：実際は晴れていない）",
                 "直説法の if の中は、未来のことでも現在形（× If it will be sunny tomorrow）。",
                 "仮定法の if の中は、現在のことでも過去形（If I had time ～）。"],
                body="どちらを使うかは、話し手が「起こりうる」と考えているか、「事実と違う」と考えているかで決まります。",
                points=[tp("同じ場面（時間があるかどうか）で、If I have time, I will help you.（時間があれば手伝うよ）と If I had time, I would help you.（時間があれば手伝うのに：実際はない）を比べ、相手が受け取る意味の違いを考えさせる。", timing="定理の説明時")]),
        derivation("dv1", "事実の文から仮定法の文を作る",
                   ["① 事実を表す文を書く：I don't have a dog, so I can't walk with it every day.",
                    "② 事実と反対の内容に変える：have a dog（犬を飼っている）、can walk（散歩できる）。",
                    "③ if の中の動詞を過去形にする：have → had。If I had a dog,",
                    "④ 主節の助動詞を過去形にする：can → could（will なら would）。I could walk with it every day.",
                    "⑤ つなげる：If I had a dog, I could walk with it every day.（犬を飼っていれば、毎日いっしょに散歩できるのに）",
                    "⑥ be 動詞の場合：I am not rich, so I can't buy the house. → If I were rich, I could buy the house.（am → were）"],
                   body="①の事実の文は否定（don't / can't）、仮定法の文は肯定になるのが典型です。逆に、事実が肯定なら仮定法は否定になります（I am busy → If I weren't busy, ～）。",
                   points=[tp("事実の文と仮定法の文で「肯定・否定が逆になる」ことに気づかせ、書きかえ問題の手順として定着させる。",
                              ask="It is raining, so I can't play outside. を仮定法にすると？", expect="If it weren't raining, I could play outside.",
                              caution="否定・肯定を逆にし忘れて If it were raining とする誤りに注意。", timing="導出の説明時")]),
        example("ex1", "例題1　If を使った仮定法過去",
                "日本語に合うように（　）に適切な1語を入れなさい。(1) もし私があなたなら、そのコンピュータを買うだろう。If I (　　) you, I (　　) buy that computer.　(2) もっとお金があれば、世界中を旅行できるのに。If I (　　) more money, I (　　) travel around the world.",
                ["(1) 「もし私があなたなら」は事実と違う仮定 → be 動詞は were。「買うだろう」→ would。",
                 "(2) 実際にはお金がない → have の過去形 had。「旅行できるのに」→ can の過去形 could。"],
                "(1) were, would　(2) had, could",
                thinking="if の中は過去形、主節は would（～だろう）か could（～できるだろう）。",
                points=[tp("(1) で was を書いた生徒には、話し言葉では使われることもあるが、教科書や試験では were を使うと指導する。")],
                misconceptions=[("If I am you, I would buy that computer.", "事実と違う仮定なので am ではなく were。")]),
        example("ex2", "例題2　I wish ～",
                "次の文を I wish で始まる文に書きかえなさい。(1) I'm sorry I don't have a bike.　(2) I'm sorry I can't play the piano.　(3) I'm sorry it isn't sunny today.",
                ["(1) 事実は「自転車を持っていない」→ 願望「持っていればいいのに」：I wish I had a bike.",
                 "(2) 事実は「ひけない」→ 「ひけたらいいのに」：can の過去形 could を使う。",
                 "(3) 事実は「晴れていない」→ 「晴れていればいいのに」：be 動詞は were。"],
                "(1) I wish I had a bike.　(2) I wish I could play the piano.　(3) I wish it were sunny today.",
                thinking="I'm sorry ～（残念だ）の内容を肯定・否定逆にして、動詞を過去形にする。",
                points=[tp("(3) で it でも were になることを確認する。")],
                misconceptions=[("I wish I can play the piano.", "wish の後ろは仮定法なので can ではなく could。")]),
        example("ex3", "例題3　仮定法か直説法か",
                "（　）内から正しいものを選び、その理由を答えなさい。(1) If it (is / were) sunny tomorrow, we will play soccer.　(2) If I (am / were) a cat, I would sleep all day.",
                ["(1) 主節が will で、「明日晴れる」ことは実際に起こりうる → 直説法。if の中は未来のことでも現在形 is。",
                 "(2) 主節が would で、「私がねこ」は事実と違う → 仮定法。were。"],
                "(1) is（実際に起こりうる条件なので直説法。if の中は現在形）　(2) were（事実と違う仮定なので仮定法）",
                thinking="主節が will / can なら直説法、would / could なら仮定法。内容が「起こりうる」か「事実と違う」かでも判断できる。",
                points=[tp("主節の助動詞（will / would）を手がかりにする方法と、内容から判断する方法の両方で確かめさせる。",
                           ask="(1) を If it were sunny tomorrow, we would ～ にすると、どんな気持ちになるか。", expect="晴れる見こみがほとんどない、と話し手が思っている感じになる。")]),
        board("bd1", "板書案",
              [("① If＋仮定法過去", ["事実：I'm not a bird. I can't fly.", "If I were a bird, I could fly.", "if の中：過去形（be は were）",
                                    "主節：would / could＋原形", "If I had time, I would help you."]),
               ("② I wish ～", ["事実：I can't swim.", "I wish I could swim.", "I wish I had a dog.", "I wish I were taller.",
                               "hope：起こりうること", "I hope it will be sunny tomorrow."]),
               ("③ 仮定法と直説法", ["起こりうる → 直説法", "If it is sunny tomorrow, we will ～.", "事実と違う → 仮定法",
                                   "If it were sunny today, we would ～.", "事実の文 ↔ 仮定法：肯定・否定が逆"])],
              points=[tp("①②の列では、事実の文を青、仮定法の文を赤で書き、動詞が「1つずつ過去に下がる」対応を線で結ぶ。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("「過去形＝過去のこと」という思いこみが最大のつまずき。仮定法の過去形は「現実からの距離」を表す、と繰り返し説明する。", timing="授業全体"),
               tp("If I were you, I would ～. は「私だったら～するよ」という助言の決まり文句として、ロールプレイで使わせると実用的。",
                  ask="友だちが「テストが心配」と言ったら？", expect="If I were you, I would study with friends."),
               tp("I wish と I hope の違いは、実現の可能性の有無で整理する。I hope の後ろには will や現在形を使う。"),
               tp("If I was ～ は話し言葉で使われることがあるが、中学校では were で統一して指導する。",
                  caution="生徒が英語の歌や映画で was を見たと質問したら、「くだけた言い方」として誤りと断定しない。"),
               tp("問題プリント D の誤答例は「if の中の形（am / will）」「主節の形（will / would＋過去形）」「wish / hope の後ろの形」の3種類にまとめて振り返らせる。")],
              misconceptions=[("If I am rich, I would buy a big house.", "事実と違う仮定なので were。"),
                              ("If I had time, I will help you.", "仮定法の主節は would。"),
                              ("I wish I can fly.", "wish の後ろは could。"),
                              ("If it will rain tomorrow, I will stay home.", "条件の if の中は現在形 rains。")]),
        summary("sm1", "まとめ",
                ["仮定法過去：現在の事実と違うことを〈If＋過去形, would / could＋原形〉で表す。be 動詞は were。",
                 "I wish＋過去形（were / had / could＋原形）で「～ならいいのに」という現在の事実と違う願望を表す。",
                 "実際に起こりうる条件は直説法（If＋現在形, will ～）。I hope は起こりうることへの願い。"]),
        check("ck1", "確認問題",
              [("If I (am / were) a bird, I could fly. の正しいほうを選びなさい。", "were（事実と違う仮定）"),
               ("I'm sorry I can't speak English well. を I wish で書きかえなさい。", "I wish I could speak English well."),
               ("If it (rains / rained) tomorrow, I will stay home. の正しいほうを選びなさい。", "rains（実際に起こりうる条件：直説法）")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

# (日本語, if 節の主語, 補語, 主節)
WERE = [
    ("もし私が鳥なら、あなたのところへ飛んでいけるのに。", "I", "a bird", "I could fly to you"),
    ("もし私があなたなら、その本を読むだろう。", "I", "you", "I would read that book"),
    ("もし彼がここにいれば、私たちを助けてくれるのに。", "he", "here", "he would help us"),
    ("もし今日が日曜日なら、一日中寝ていられるのに。", "it", "Sunday today", "I could sleep all day"),
    ("もし私がもっと背が高ければ、あの棚に手が届くのに。", "I", "taller", "I could reach that shelf"),
    ("もし彼女がひまなら、いっしょに買い物に行くだろうに。", "she", "free", "she would go shopping with us"),
    ("もし私が先生なら、宿題を出さないだろう。", "I", "a teacher", "I wouldn't give any homework"),
    ("もし天気がよければ、私たちは海で泳げるのに。", "the weather", "nice", "we could swim in the sea"),
    ("もし私があなたの立場なら、彼に本当のことを言うだろう。", "I", "in your place", "I would tell him the truth"),
    ("もし私が魚なら、海の中で暮らせるのに。", "I", "a fish", "I could live in the sea"),
    ("もし私がお金持ちなら、大きな家を買うのに。", "I", "rich", "I would buy a big house"),
    ("もしケンが私たちのチームにいれば、試合に勝てるのに。", "Ken", "on our team", "we could win the game"),
]
BE_PRES = {"I": "am", "he": "is", "she": "is", "it": "is", "the weather": "is", "Ken": "is"}


@gen("basic_check", 4, ["computation", "condition_check"])
def if_were(r):
    jp, subj, comp, main = r.choice(WERE)
    pres = BE_PRES[subj]
    stem_if = f"If {subj} (　　) {comp}, {main}."
    stem_if = stem_if[0].upper() + stem_if[1:]
    why = {pres: (f"{pres} は現在形で、実際に起こりうる条件（直説法）の形。事実と違う仮定には過去形 were を使う。", "仮定法と直説法の区別"),
           "be": ("be は原形。if の中の動詞は主語のすぐ後ろで形を変える必要がある。", "be 動詞の形"),
           "will be": ("if の中に will は使わない。また、主節が would / could の仮定法なので、if の中は過去形にする。", "if 節の中の形")}
    return mc(f"日本語に合うように、（　）に入る最も適切なものを選びなさい。\n{jp}\n{stem_if}", ["were"] + list(why),
              f"現在の事実と違う仮定なので仮定法過去。be 動詞は主語が {subj} でも were を使う。", d=1,
              ap="主節に would / could があるか、内容が事実と違う仮定かを確かめる。",
              steps=["主節に would / could がある → 仮定法過去。", "if の中の be 動詞は過去形にする。", f"主語が {subj} でも were を使う。答え：were"],
              alt=[f"事実の文に戻して確かめる：実際は {subj} {pres} not {comp}（事実と違う）なので、仮定法を使う。"],
              pc=[("仮定法過去だと判断している", 1), ("were を選んでいる", 1)],
              pit=["主語が I / he / she のとき、現在形の am / is を使う。", "if の中に will を入れる。"], why=why)


# (日本語, if 節, 原形, 過去形, 助動詞)
MAIN = [
    ("もし時間があれば、あなたを手伝うのに。", "If I had time", "help you", "helped you", "would"),
    ("もし車を持っていれば、あなたを家まで送れるのに。", "If I had a car", "drive you home", "drove you home", "could"),
    ("もし彼の電話番号を知っていれば、彼に電話するのに。", "If I knew his phone number", "call him", "called him", "would"),
    ("もし翼があれば、空を飛べるのに。", "If I had wings", "fly in the sky", "flew in the sky", "could"),
    ("もし宝くじに当たったら、新しい家を買うだろう。", "If I won the lottery", "buy a new house", "bought a new house", "would"),
    ("もし英語を上手に話せたら、外国人ともっと話すのに。", "If I could speak English well", "talk more with people from abroad", "talked more with people from abroad", "would"),
    ("もし私たちが近くに住んでいたら、毎日会えるのに。", "If we lived near each other", "see each other every day", "saw each other every day", "could"),
    ("もしピアノがひけたら、この曲をひくのに。", "If I could play the piano", "play this song", "played this song", "would"),
    ("もしペットを飼っていたら、毎朝散歩させるだろう。", "If I had a pet", "walk it every morning", "walked it every morning", "would"),
    ("もしもっと時間があれば、その本を全部読めるのに。", "If I had more time", "read the whole book", "read the whole book", "could"),
    ("もし彼女がここにいたら、とても喜ぶだろう。", "If she were here", "be very happy", "was very happy", "would"),
]


@gen("basic_check", 4, ["computation", "common_error"])
def main_clause(r):
    jp, ifc, base, past, aux = r.choice(MAIN)
    pres_aux = {"would": "will", "could": "can"}[aux]
    subj = "she" if ifc.startswith("If she") else ("we" if ifc.startswith("If we") else "I")
    ok = f"{aux} {base}"
    w1 = f"{pres_aux} {base}"
    w2 = f"{aux} {past}" if past != base else f"{aux} to {base}"
    w3 = f"{aux} to {base}" if past != base else f"{pres_aux} to {base}"
    why = {w1: (f"{pres_aux} は現在形の助動詞で、実際に起こりうる条件（直説法）の文になる。if の中が過去形の仮定法なので {aux} を使う。", "仮定法の主節の形"),
           w2: (f"{aux} の後ろは動詞の原形。" + ("過去形にはしない。" if past != base else "to は置かない。"), "助動詞の後ろの形"),
           w3: ("助動詞の後ろに to は置かない。", "助動詞の後ろの形")}
    return mc(f"日本語に合うように、（　）に入る最も適切なものを選びなさい。\n{jp}\n{ifc}, {subj} (　　).", [ok] + list(why),
              f"if の中が過去形の仮定法過去なので、主節は {aux}＋動詞の原形。答え：{ok}", d=2,
              ap="if の中の動詞が過去形（仮定法）かどうかを見て、主節を would / could＋原形にする。",
              steps=["if の中の動詞が過去形 → 現在の事実と違う仮定（仮定法過去）。", f"日本語「{'～できるのに' if aux == 'could' else '～するのに（だろう）'}」から {aux} を選ぶ。", f"{aux} の後ろは原形：{ok}"],
              alt=[f"事実の文（実際は ～ ので {subj} {"can't" if aux == 'could' else "won't"} ～）を考えて、助動詞を1つ過去に下げた形になっているかを確かめる。"],
              pc=[("仮定法の主節には would / could を使うと判断している", 1), ("would / could＋原形を選んでいる", 1)],
              pit=["主節に will / can を使う。", "would / could の後ろの動詞まで過去形にする。"], why=why)


# (日本語, 空所つき英文, 正答, [(誤答, 理由)])
WISH = [
    ("兄弟がいればいいのに。", "I wish I (　　) a brother.", "had",
     [("have", "wish の後ろは仮定法なので過去形にする。have は現在形。"), ("will have", "wish の後ろに will は使わない。実現の見こみがあるなら hope を使う。"), ("having", "ing 形だけでは文の動詞にならない。")]),
    ("もっと背が高ければいいのに。", "I wish I (　　) taller.", "were",
     [("am", "wish の後ろは仮定法。現在形の am は使わない。"), ("will be", "wish の後ろに will は使わない。"), ("being", "ing 形だけでは文の動詞にならない。")]),
    ("速く走れたらいいのに。", "I wish I (　　) run fast.", "could",
     [("can", "wish の後ろは仮定法なので can の過去形 could にする。"), ("will", "will では「走るだろう」となり、「走れたら」の意味にならない。"), ("could to", "助動詞の後ろに to は置かない。")]),
    ("今日が土曜日ならいいのに。", "I wish it (　　) Saturday today.", "were",
     [("is", "wish の後ろは仮定法。現在形の is は使わない。"), ("will be", "wish の後ろに will は使わない。"), ("be", "be は原形。主語 it の後ろには過去形 were を置く。")]),
    ("もっと時間があればいいのに。", "I wish I (　　) more time.", "had",
     [("have", "wish の後ろは仮定法なので過去形 had にする。"), ("has", "has は三人称単数の現在形。主語は I で、さらに仮定法なので had。"), ("will have", "wish の後ろに will は使わない。")]),
    ("鳥のように飛べたらいいのに。", "I wish I (　　) fly like a bird.", "could",
     [("can", "wish の後ろは仮定法なので could にする。"), ("am", "am の後ろに動詞の原形 fly を続けることはできない。"), ("could to", "助動詞の後ろに to は置かない。")]),
    ("あなたがここにいてくれたらいいのに。", "I wish you (　　) here.", "were",
     [("are", "wish の後ろは仮定法。現在形の are は使わない。"), ("will be", "wish の後ろに will は使わない。"), ("being", "ing 形だけでは文の動詞にならない。")]),
    ("ギターがひけたらいいのに。", "I wish I (　　) play the guitar.", "could",
     [("can", "wish の後ろは仮定法なので could にする。"), ("will", "will では「ひくだろう」となり、「ひけたら」の意味にならない。"), ("played", "played の後ろに動詞の原形 play は続かない。「できる」は could＋原形。")]),
    ("その答えを知っていればいいのに。", "I wish I (　　) the answer.", "knew",
     [("know", "wish の後ろは仮定法なので過去形 knew にする。"), ("knows", "主語 I に三単現の s はつかない。さらに仮定法なので knew。"), ("will know", "wish の後ろに will は使わない。")]),
    ("祖母が近くに住んでいればいいのに。", "I wish my grandmother (　　) near my house.", "lived",
     [("lives", "wish の後ろは仮定法なので過去形 lived にする。lives は現在形。"), ("live", "原形は使わない。主語のすぐ後ろの動詞は過去形 lived。"), ("will live", "wish の後ろに will は使わない。")]),
]


@gen("basic_check", 4, ["condition_check", "concept"])
def wish_form(r):
    jp, s, ok, wrongs = r.choice(WISH)
    return mc(f"日本語に合うように、（　）に入る最も適切なものを選びなさい。\n{jp}\n{s}", [ok] + [w for w, _ in wrongs],
              f"I wish の後ろは仮定法過去で、現在の事実と違う願望を表す。動詞（助動詞）を過去形にする。答え：{ok}", d=1,
              ap="I wish の後ろは、現在のことでも過去形（be 動詞は were、can は could）にする。",
              steps=["I wish ～ は「（実際はそうではないが）～ならいいのに」。", "wish の後ろの動詞を過去形にする。", f"答え：{ok}"],
              alt=["事実の文（I'm sorry ～ / 実際は ～ ない）を考えて、その反対を過去形で表していることを確かめる。"],
              pc=[("wish の後ろは過去形と判断している", 1), ("正しい形を選んでいる", 1)],
              pit=["wish の後ろに現在形（have / can / am）を使う。", "wish と hope を混同し、will を使う。"],
              why={w: (reason, "I wish の後ろの形") for w, reason in wrongs})


# (英文, 事実, [(誤った事実, 理由)])
FACT = [
    ("If I had a car, I could drive you to the station.", "私は車を持っていない。",
     [("私は車を持っている。", "仮定法過去は事実と違うことを仮定する。実際は持っていない。"), ("私は以前、車を持っていた。", "had は過去のことではなく、現在の事実と違う仮定を表す。"), ("私はこれから車を買う予定だ。", "未来の予定は述べていない。")]),
    ("If I were not busy, I would go to the concert.", "私は忙しい。",
     [("私は忙しくない。", "仮定法では事実と反対のことを仮定する。were not busy の反対が事実。"), ("私は昨日忙しかった。", "were は過去のことではなく、現在の事実と違う仮定を表す。"), ("私はコンサートに行く。", "実際は忙しいので行けない。")]),
    ("I wish I could swim.", "私は泳げない。",
     [("私は泳げる。", "I wish は事実と違う願望。実際は泳げない。"), ("私は昔、泳げた。", "could は過去の能力ではなく、現在の事実と違う願望を表す。"), ("私はこれから泳ぐつもりだ。", "未来の予定は述べていない。")]),
    ("If Ken knew the answer, he would tell us.", "ケンは答えを知らない。",
     [("ケンは答えを知っている。", "仮定法は事実と違う仮定。実際は知らない。"), ("ケンは答えを私たちに教えた。", "would tell は「教えるだろうに」で、実際は教えていない。"), ("ケンは答えを忘れた。", "忘れたかどうかは述べていない。現在知らないことだけがわかる。")]),
    ("I wish it were warm today.", "今日は暖かくない。",
     [("今日は暖かい。", "I wish は事実と違う願望。実際は暖かくない。"), ("昨日は暖かかった。", "were は過去のことではなく、今日の事実と違う願望を表す。"), ("明日は暖かくなる。", "明日のことは述べていない。")]),
    ("If my sister were here, she would help me.", "姉はここにいない。",
     [("姉はここにいる。", "仮定法は事実と違う仮定。実際はいない。"), ("姉は私を手伝ってくれた。", "would help は「手伝ってくれるだろうに」で、実際は手伝っていない。"), ("姉は以前ここにいた。", "were は過去のことではなく、現在の事実と違う仮定を表す。")]),
    ("I wish I had a smartphone.", "私はスマートフォンを持っていない。",
     [("私はスマートフォンを持っている。", "I wish は事実と違う願望。実際は持っていない。"), ("私は以前スマートフォンを持っていた。", "had は過去のことではなく、現在の事実と違う願望を表す。"), ("私はスマートフォンを買うつもりだ。", "未来の予定は述べていない。")]),
    ("If we lived in Hokkaido, we could ski every winter.", "私たちは北海道に住んでいない。",
     [("私たちは北海道に住んでいる。", "仮定法は事実と違う仮定。実際は住んでいない。"), ("私たちは以前北海道に住んでいた。", "lived は過去のことではなく、現在の事実と違う仮定を表す。"), ("私たちは毎年冬にスキーをしている。", "could ski は「できるのに」で、実際はできていない。")]),
    ("If I could play the guitar, I would join the band.", "私はギターがひけない。",
     [("私はギターがひける。", "仮定法は事実と違う仮定。実際はひけない。"), ("私はバンドに入っている。", "would join は「入るだろうに」で、実際は入っていない。"), ("私は昔ギターがひけた。", "could は過去の能力ではなく、現在の事実と違う仮定を表す。")]),
]


@gen("basic_check", 4, ["concept", "condition_check"])
def fact_behind(r):
    en, ok, wrongs = r.choice(FACT)
    return mc(f"次の英文からわかる「現在の事実」として最も適切なものを選びなさい。\n{en}", [ok] + [w for w, _ in wrongs],
              f"仮定法過去・I wish は現在の事実と違うことを表す。英文の内容を肯定・否定逆にしたものが事実になる。答え：{ok}", d=2,
              ap="仮定法の文は「事実の反対」を述べている。if や wish の後ろの内容を、肯定・否定逆にして現在形で考える。",
              steps=["if（wish）の後ろの内容を確かめる。", "過去形でも過去のことではなく、現在の事実と違う仮定・願望だと判断する。", "肯定・否定を逆にして現在の事実にする。", f"答え：{ok}"],
              alt=["事実の文を英語で書いてみて（例：I don't have a car.）、もとの英文の反対になっているかを確かめる。"],
              pc=[("仮定法が事実と違うことを表すと理解している", 1), ("正しい事実を選んでいる", 1)],
              pit=["過去形を見て、過去の出来事だと考える。", "仮定の内容をそのまま事実だと思う。"],
              why={w: (reason, "仮定法が表す事実の読み取り") for w, reason in wrongs})


# (英文（空所）, 正答, [(誤答, 理由)], 直説法か)
MOOD = [
    ("If it (　　) sunny tomorrow, we will go hiking.", "is",
     [("were", "主節が will で、明日晴れることは実際に起こりうる。直説法なので if の中は現在形。"), ("will be", "条件を表す if の中は、未来のことでも現在形。will は使わない。"), ("be", "be は原形。主語 it の後ろには is を置く。")]),
    ("If I (　　) a dolphin, I would swim all day.", "were",
     [("am", "私がイルカであることは事実と違う。主節も would なので仮定法で were。"), ("will be", "if の中に will は使わない。"), ("be", "be は原形。if の中では過去形 were にする。")]),
    ("If you (　　) free this afternoon, let's play tennis.", "are",
     [("were", "相手がひまである可能性は十分にあり、主節も Let's ～ なので直説法。現在形 are。"), ("will be", "条件を表す if の中に will は使わない。"), ("be", "be は原形。主語 you の後ろには are を置く。")]),
    ("If I (　　) time now, I would help you.", "had",
     [("have", "主節が would で、今時間がないという事実と違う仮定。仮定法なので過去形 had。"), ("will have", "if の中に will は使わない。"), ("having", "ing 形だけでは文の動詞にならない。")]),
    ("If it (　　) tomorrow, the game will be canceled.", "rains",
     [("rained", "主節が will で、明日雨が降ることは起こりうる。直説法なので現在形 rains。"), ("will rain", "条件を表す if の中は、未来のことでも現在形。"), ("rain", "主語 it は三人称単数なので rains。")]),
    ("If I (　　) the way, I would take you there.", "knew",
     [("know", "主節が would で、道を知らないという事実と違う仮定。仮定法なので過去形 knew。"), ("will know", "if の中に will は使わない。"), ("knows", "主語 I に三単現の s はつかない。さらに仮定法なので knew。")]),
    ("If you (　　) hungry, you can eat this sandwich.", "are",
     [("were", "相手がおなかがすいている可能性があり、主節も can なので直説法。現在形 are。"), ("will be", "条件を表す if の中に will は使わない。"), ("be", "be は原形。主語 you の後ろには are を置く。")]),
    ("If my father (　　) here, he would be glad to see you.", "were",
     [("is", "主節が would で、父がここにいないという事実と違う仮定。仮定法なので were。"), ("will be", "if の中に will は使わない。"), ("be", "be は原形。if の中では過去形 were にする。")]),
    ("If Ken (　　) the bus, he will be late.", "misses",
     [("missed", "主節が will で、バスに乗り遅れることは起こりうる。直説法なので現在形 misses。"), ("will miss", "条件を表す if の中は、未来のことでも現在形。"), ("miss", "主語 Ken は三人称単数なので misses。")]),
]


@gen("basic_check", 4, ["condition_check", "cross_unit"], rel=["JH-ENG-G2-U03"])
def mood_choice(r):
    s, ok, wrongs = r.choice(MOOD)
    return mc(f"（　）に入る最も適切なものを選びなさい。\n{s}", [ok] + [w for w, _ in wrongs],
              f"主節の形（will / can / Let's か、would / could か）と、内容が起こりうるか事実と違うかから判断する。答え：{ok}", d=3,
              ap="中2で学んだ「条件の if（直説法）」と、この単元の仮定法のどちらかを、主節の助動詞から見分ける。",
              steps=["主節の助動詞を確かめる（will / can → 直説法、would / could → 仮定法）。", "内容が実際に起こりうるか、事実と違うかでも確かめる。",
                     "直説法なら if の中は現在形、仮定法なら過去形（be は were）。", f"答え：{ok}"],
              alt=["完成した文を日本語に訳し、「～したら…する」（起こりうる）か「～なら…するのに」（事実と違う）かを確かめる。"],
              pc=[("直説法か仮定法かを判断している", 1), ("正しい形を選んでいる", 1)],
              pit=["if があれば何でも仮定法だと考える。", "未来のことだからと、if の中に will を使う。"],
              why={w: (reason, "仮定法と直説法の区別") for w, reason in wrongs})


# ======================================================================
# B 標準演習
# ======================================================================

# (事実の文, 答え, 別解)
REAL2IF = [
    ("I don't have a bike, so I can't go cycling.", "If I had a bike, I could go cycling.", ["I could go cycling if I had a bike."]),
    ("I am not a good cook, so I can't make dinner for you.", "If I were a good cook, I could make dinner for you.", ["I could make dinner for you if I were a good cook."]),
    ("I don't know her address, so I can't send her a letter.", "If I knew her address, I could send her a letter.", ["I could send her a letter if I knew her address."]),
    ("It is raining, so we can't play outside.", "If it weren't raining, we could play outside.", ["If it were not raining, we could play outside.", "We could play outside if it weren't raining."]),
    ("I am busy, so I won't go to the party.", "If I weren't busy, I would go to the party.", ["If I were not busy, I would go to the party.", "I would go to the party if I weren't busy."]),
    ("Ken doesn't live near here, so he can't come every day.", "If Ken lived near here, he could come every day.", ["Ken could come every day if he lived near here."]),
    ("I don't have enough money, so I won't buy the game.", "If I had enough money, I would buy the game.", ["I would buy the game if I had enough money."]),
    ("My sister isn't here, so she can't help me.", "If my sister were here, she could help me.", ["My sister could help me if she were here."]),
    ("I can't speak Chinese, so I won't talk with him.", "If I could speak Chinese, I would talk with him.", ["I would talk with him if I could speak Chinese."]),
    ("We don't have a garden, so we can't grow vegetables.", "If we had a garden, we could grow vegetables.", ["We could grow vegetables if we had a garden."]),
    ("It isn't sunny today, so we won't go to the beach.", "If it were sunny today, we would go to the beach.", ["We would go to the beach if it were sunny today."]),
]


@gen("standard_practice", 5, ["computation", "application"])
def real_to_if(r):
    a, ans, vs = r.choice(REAL2IF)
    return sa(f"次の英文とほぼ同じ内容を、If を使った仮定法過去の1文で表しなさい。\n{a}", ans,
              f"事実の文の肯定・否定を逆にし、if の中を過去形（be 動詞は were）、主節を would / could＋原形にする。答え：{ans}", d=3, p=4, v=vs,
              ap="事実の文の「～ので」の部分を if の中に、「…できない（しない）」の部分を主節にして、肯定・否定を逆にする。",
              steps=["so の前（理由）を if の中に、so の後ろ（結果）を主節にする。", "肯定・否定を逆にする（don't have → had、isn't → were、is raining → weren't raining）。",
                     "主節の can't → could、won't → would にする（否定を取る）。", f"答え：{ans}"],
              alt=["書いた文を日本語に訳し（もし～なら…できるのに）、もとの文の事実と反対の内容になっているかを確かめる。"],
              pc=[("if の中の過去形（were / 否定の扱い）が正しい", 2), ("主節の would / could＋原形が正しい", 2)],
              pit=["肯定・否定を逆にし忘れる（If I didn't have a bike ～）。", "主節を can / will のままにする。"])


# (残念な事実, 答え, 別解)
SORRY = [
    ("I'm sorry I can't play the guitar.", "I wish I could play the guitar.", []),
    ("I'm sorry I don't have a dog.", "I wish I had a dog.", []),
    ("I'm sorry I'm not good at math.", "I wish I were good at math.", []),
    ("I'm sorry you can't come to my birthday party.", "I wish you could come to my birthday party.", []),
    ("I'm sorry I don't know his name.", "I wish I knew his name.", []),
    ("I'm sorry it isn't summer now.", "I wish it were summer now.", []),
    ("I'm sorry my house isn't near the station.", "I wish my house were near the station.", []),
    ("I'm sorry I can't see the stars tonight.", "I wish I could see the stars tonight.", []),
    ("I'm sorry I don't have a sister.", "I wish I had a sister.", []),
    ("I'm sorry my brother doesn't live with us.", "I wish my brother lived with us.", []),
]


@gen("standard_practice", 4, ["computation", "condition_check"])
def sorry_to_wish(r):
    a, ans, vs = r.choice(SORRY)
    return sa(f"次の英文とほぼ同じ内容を、I wish で始まる1文で表しなさい。\n{a}", ans,
              f"「～できない（ない）のが残念だ」＝「～できたら（あれば）いいのに」。肯定・否定を逆にして、wish の後ろを過去形にする。答え：{ans}", d=2, p=4, v=vs or None,
              ap="I'm sorry の後ろの事実を、肯定・否定逆にして I wish の後ろに置き、動詞を過去形にする。",
              steps=["I'm sorry の後ろの事実を確かめる。", "否定（can't / don't / isn't）を取り、肯定にする。", "動詞を過去形にする（can → could、have → had、is → were）。", f"答え：{ans}"],
              alt=["書いた文を「～ならいいのに」と訳し、もとの文の「～ないのが残念だ」と同じ気持ちを表しているかを確かめる。"],
              pc=[("肯定・否定を逆にしている", 2), ("wish の後ろを正しい過去形にしている", 2)],
              pit=["I wish I can ～ と現在形を使う。", "I wish I couldn't ～ と否定を残す。"])


ORDERS = [
    ("もし私があなたなら、もっと早く寝るだろう。", ["if", "I", "were", "you,", "I would", "go", "to bed", "earlier"], "If I were you, I would ～."),
    ("お金がたくさんあれば、世界中を旅するのに。", ["if", "I", "had", "a lot of money,", "I would", "travel", "around the world"], "If＋過去形, would＋原形"),
    ("フランス語が話せたらいいのに。", ["I wish", "I", "could", "speak", "French"], "I wish I could＋原形"),
    ("今日が休みならいいのに。", ["I", "wish", "today", "were", "a holiday"], "I wish＋主語＋were"),
    ("もし彼女の電話番号を知っていれば、電話をかけられるのに。", ["if", "I", "knew", "her phone number,", "I could", "call", "her"], "If＋過去形, could＋原形"),
    ("翼があれば、あなたのところへ飛んでいけるのに。", ["I could", "fly", "to you", "if", "I", "had", "wings"], "主節を先に置く形：could＋原形＋if＋過去形"),
    ("もし私が先生なら、もっと楽しい授業をするだろう。", ["if", "I", "were", "a teacher,", "I would", "make", "my classes", "more fun"], "If I were ～, I would ～."),
    ("祖父母が近くに住んでいればいいのに。", ["I", "wish", "my grandparents", "lived", "near", "us"], "I wish＋主語＋過去形"),
    ("もしひまだったら、いっしょに買い物に行けるのに。", ["if", "I", "were", "free,", "I could", "go shopping", "with you"], "If I were ～, I could ～."),
    ("ペットを飼えたらいいのに。", ["I wish", "I", "could", "have", "a pet"], "I wish I could＋原形"),
]


@gen("standard_practice", 4, ["application", "computation"])
def build_order(r):
    jp, parts, pat = r.choice(ORDERS)
    sent = " ".join(parts)
    sent = sent[0].upper() + sent[1:] + "."
    return order(f"日本語の意味になるように、次の語句を並べかえて英文を完成させなさい。文頭にくる語も小文字で示してある。\n{jp}", parts,
                 f"{sent}　ポイント：{pat}。", d=2, p=4,
                 ap="if（wish）の後ろに過去形の部分、主節に would / could＋原形の部分を作り、それぞれの中の語順を決める。",
                 steps=["文の型を決める（If ～, … ／ … if ～ ／ I wish ～）。", "if や wish の後ろに〈主語＋過去形〉を置く。", "主節を〈主語＋would / could＋原形〉にする。", f"完成文：{sent}"],
                 alt=["完成した文を日本語に訳し直し、問題の日本語と一致するかを確かめる。"],
                 pc=[("if（wish）の後ろの語順が正しい", 2), ("主節の語順が正しい", 2)],
                 pit=["would / could の後ろの動詞を過去形にしてしまう。", "コンマの位置を誤る（主節を先に置くときはコンマ不要）。"])


# (英文, 正しい訳, [(誤訳, 理由)])
MEANING = [
    ("If I were you, I would apologize to her.", "もし私があなたなら、彼女にあやまるだろう。",
     [("私があなただったとき、彼女にあやまった。", "If I were you は過去の出来事ではなく、現在の事実と違う仮定。"),
      ("もし私があなたなら、彼女にあやまるべきだった。", "would は「～するだろう」。「～すべきだった」の意味はない。"),
      ("あなたは私のために彼女にあやまるだろう。", "主節の主語は I。あやまるのは私。")]),
    ("If it rains tomorrow, I will stay home.", "明日雨が降ったら、私は家にいるつもりだ。",
     [("明日雨が降ればいいのに、家にいられるから。", "これは直説法で、願望ではない。雨が降る可能性がある条件を表す。"),
      ("もし明日雨が降るなら家にいるのに（実際は降らない）。", "仮定法ではなく直説法（if の中が現在形、主節が will）。事実と違う意味はない。"),
      ("昨日雨が降ったので、私は家にいた。", "tomorrow と will から未来のこと。過去の出来事ではない。")]),
    ("I wish I could see you more often.", "あなたにもっとたびたび会えたらいいのに。",
     [("私はあなたにもっとたびたび会えた。", "I wish は願望。could は過去の能力ではない。"),
      ("あなたにもっとたびたび会いたいと思ったことがある。", "wish は現在形で、今の願望を表す。"),
      ("あなたは私にもっとたびたび会えるだろう。", "主語は I。会いたいのは私。")]),
    ("If I had more time, I could join the club.", "もっと時間があれば、そのクラブに入れるのに。",
     [("もっと時間があったので、そのクラブに入れた。", "had は過去のことではなく、現在の事実と違う仮定。"),
      ("もっと時間があれば、そのクラブに入るつもりだ。", "could は「できるのに」で、実際は時間がなく入れない。予定ではない。"),
      ("クラブに入ると、もっと時間ができる。", "条件と結果が逆になっている。")]),
    ("I hope it will be sunny tomorrow.", "明日晴れるといいな。",
     [("明日晴れればいいのに（実際は晴れない）。", "hope は実現の可能性があることへの願い。事実と違う願望は wish。"),
      ("明日は晴れるだろうと思った。", "hope は「望む」。過去の推測ではない。"),
      ("明日晴れたら、出かけるつもりだ。", "条件の文ではない。出かけるとは述べていない。")]),
    ("If my brother were here, he would know what to do.", "もし兄がここにいたら、どうすべきかわかるだろうに。",
     [("兄はここにいたので、どうすべきかわかった。", "were は過去のことではなく、現在の事実（ここにいない）と違う仮定。"),
      ("兄がここにいるので、どうすべきかわかるだろう。", "仮定法なので、実際は兄はここにいない。"),
      ("もし兄がここにいたら、何をしたか知っているだろう。", "what to do は「何をすべきか」。過去にしたことではない。")]),
    ("If you are tired, you can sit here.", "疲れているなら、ここにすわっていいですよ。",
     [("あなたが疲れていればいいのに、ここにすわれるから。", "これは直説法の条件。願望ではない。"),
      ("もし疲れていたら、ここにすわれたのに（実際は疲れていない）。", "直説法（are / can）なので、事実と違う意味はない。"),
      ("あなたは疲れたので、ここにすわった。", "現在の条件と許可を表す文。過去の出来事ではない。")]),
    ("I wish my dog could talk.", "私の犬が話せたらいいのに。",
     [("私の犬は話すことができた。", "I wish は願望。could は過去の能力を表していない。"),
      ("私の犬は話したがっている。", "願っているのは私（I wish）。"),
      ("私の犬が話せるといいな（話せるかもしれない）。", "wish は事実と違う願望。実現の可能性があるなら hope。")]),
]


@gen("standard_practice", 4, ["concept", "application"])
def meaning(r):
    en, ok, wrongs = r.choice(MEANING)
    return mc(f"次の英文の意味として最も適切なものを選びなさい。\n{en}", [ok] + [w for w, _ in wrongs],
              f"仮定法（過去形・would / could・wish）か、直説法（現在形・will / can・hope）かを見分けて訳す。答え：{ok}", d=3, p=4,
              ap="if（wish / hope）の後ろの動詞の形と、主節の助動詞を確かめ、事実と違う仮定・願望か、起こりうることかを判断する。",
              steps=["動詞の形（過去形か現在形か）と助動詞（would / could か will / can か）を確かめる。", "仮定法なら「～なら…のに」、直説法なら「～したら…する」と訳す。", f"答え：{ok}"],
              alt=["選んだ日本語から「現在の事実」を考え、英文の形（仮定法か直説法か）と矛盾しないかを確かめる。"],
              pc=[("仮定法か直説法かを判断している", 2), ("文全体を正しく訳している", 2)],
              pit=["過去形を見て、過去の出来事だと訳す。", "wish と hope の違いを考えずに訳す。"],
              why={w: (reason, "仮定法の意味の読み取り") for w, reason in wrongs})


# (日本語, 原級, 比較級, if 節の主語, 動詞（"be" か一般動詞）, 主節（would / could）, 主節の現在版)
COMP = [
    ("もっと背が高ければ、いちばん上の棚に手が届くのに。", "tall", "taller", "I", "be", "I could reach the top shelf", "I can reach the top shelf"),
    ("もっと速く走れたら、リレーの選手に選ばれるのに。", "fast", "faster", "I", "run", "I could be on the relay team", "I can be on the relay team"),
    ("この部屋がもっと大きければ、ここでパーティーを開けるのに。", "big", "bigger", "this room", "be", "we could have a party here", "we can have a party here"),
    ("もっと年上なら、一人で外国を旅行できるのに。", "old", "older", "I", "be", "I could travel abroad alone", "I can travel abroad alone"),
    ("この問題がもっと簡単なら、すぐに解けるのに。", "easy", "easier", "this problem", "be", "I could solve it soon", "I can solve it soon"),
    ("今日がもっと暖かければ、海で泳ぐのに。", "warm", "warmer", "it", "be", "we would swim in the sea", "we will swim in the sea"),
    ("このかばんがもっと安ければ、買うのに。", "cheap", "cheaper", "this bag", "be", "I would buy it", "I will buy it"),
    ("もっと高くとべたら、バスケットボールでダンクシュートができるのに。", "high", "higher", "I", "jump", "I could dunk in basketball", "I can dunk in basketball"),
]


@gen("standard_practice", 3, ["cross_unit", "condition_check"], rel=["JH-ENG-G2-U04"])
def comp_mix(r):
    jp, pos, comp, subj, verb, main, main_pres = r.choice(COMP)
    if verb == "be":
        be = "am" if subj == "I" else "is"
        ok = f"If {subj} were {comp}, {main}."
        w1 = f"If {subj} {be} {comp}, {main_pres}."
        w2 = f"If {subj} were more {pos}, {main}."
        w3 = f"If {subj} were {comp}, {main_pres}."
    else:
        ok = f"If {subj} could {verb} {comp}, {main}."
        w1 = f"If {subj} can {verb} {comp}, {main_pres}."
        w2 = f"If {subj} could {verb} more {pos}, {main}."
        w3 = f"If {subj} could {verb} {comp}, {main_pres}."
    why = {w1: ("現在形（am / is / can）の if と will / can の主節では、実際に起こりうる条件の文になり、「～なら…のに」という事実と違う仮定にならない。", "仮定法と直説法の区別"),
           w2: (f"{pos} の比較級は {comp}。1音節（または -y で終わる2音節）の形容詞・副詞には more をつけない。", "比較級の作り方"),
           w3: ("if の中を仮定法にしたら、主節も would / could にそろえる。will / can のままでは形が合わない。", "仮定法の主節の形")}
    ok = ok[0].upper() + ok[1:]
    return mc(f"日本語に合う英文として最も適切なものを選びなさい。\n{jp}", [ok] + list(why),
              f"現在の事実と違う仮定なので仮定法過去（if の中は過去形・主節は would / could）。「もっと～」は比較級 {comp}。答え：{ok}", d=3, p=4,
              ap="中2で学んだ比較級の作り方と、仮定法過去の形（if の中は過去形、主節は would / could）の2点を順に確かめる。",
              steps=[f"「もっと～」→ 比較級 {comp}（{pos} に -er）。", "事実と違う仮定 → if の中は were（または could＋原形）。", "主節は would / could＋原形。", f"答え：{ok}"],
              alt=["事実の文（実際は～ないので…できない）を英語で考え、それを仮定法に直した形と比べる。"],
              pc=[("比較級の形が正しいものを選んでいる", 2), ("仮定法の形がそろったものを選んでいる", 2)],
              pit=["more tall のように、-er をつける語に more を使う。", "if の中だけ過去形にして、主節を can / will のままにする。"], why=why)


# ======================================================================
# C 思考力・記述応用
# ======================================================================

PAIRS = [
    ("If I have time, I will help you.", "If I had time, I would help you.",
     "A は直説法で「時間があれば手伝うよ」。時間ができる可能性があり、実際に手伝うつもりがある。B は仮定法過去で「時間があれば手伝うのに」。実際には時間がなく、手伝えないことを表す。if の中の have / had と、主節の will / would の違いが意味を変えている。"),
    ("I hope I can see you again.", "I wish I could see you again.",
     "A は hope＋can で「また会えるといいな」。実際に会える可能性があると考えている。B は wish＋could で「また会えたらいいのに」。実際には会うのが難しい（会えない）と考えていて、残念な気持ちがこめられている。"),
    ("If it is sunny tomorrow, we will go to the beach.", "If it were sunny today, we would go to the beach.",
     "A は直説法で「明日晴れたら海に行く」。明日晴れる可能性がある条件。B は仮定法過去で「今日晴れていたら海に行くのに」。実際には今日は晴れておらず、海に行けないことを表す。"),
    ("When I was a child, I could swim fast.", "If I were a fish, I could swim fast.",
     "A の could は can の過去形で「子どものころは速く泳げた」という過去の能力を表す（過去の事実）。B の could は仮定法過去で「もし私が魚なら速く泳げるのに」という現在の事実と違う仮定を表す。同じ could でも、A は過去、B は現在の空想。"),
    ("I am not a bird, so I can't fly to you.", "If I were a bird, I could fly to you.",
     "A は直説法で「私は鳥ではないので、あなたのところへ飛んでいけない」という現在の事実。B は仮定法過去で「もし私が鳥なら、あなたのところへ飛んでいけるのに」という事実と反対の仮定。B は A と同じ事実をふまえ、肯定・否定を逆にして過去形で表している。"),
    ("If you are free, please call me.", "If you were free, I would call you.",
     "A は直説法で「（もし）ひまなら電話してね」。相手がひまである可能性がある。B は仮定法過去で「あなたがひまなら電話するのに」。実際には相手が忙しいとわかっていて、電話しないことを表す。"),
]


@gen("thinking_writing", 4, ["written_reasoning", "concept"])
def explain_difference(r):
    a, b, model = r.choice(PAIRS)
    return desc(f"次の2つの英文 A・B の意味の違いを、動詞・助動詞の形に注目して日本語で説明しなさい。\nA：{a}\nB：{b}", model,
                "現在形・will / can・hope は「起こりうること」、過去形・would / could・wish（仮定法）は「現在の事実と違うこと」を表す。ただし could が単に過去の能力を表す場合もあるので、文全体から判断する。",
                [("A の形と意味（話し手が事実をどう考えているか）を説明している", 3), ("B の形と意味を説明している", 3), ("違いを生む動詞・助動詞の形を指摘している", 2)], d=4, p=8, lines=5,
                ap="A と B で形が違う部分（現在形と過去形、will と would、hope と wish など）に印をつけ、それぞれが表す「事実の受け止め方」を考える。",
                steps=["A と B で違う部分を見つける。", "それぞれが直説法か仮定法か（過去の事実か）を判断する。", "和訳を示し、話し手が考えている現在の事実を説明する。"],
                alt=["A・B それぞれの「現在の事実」を日本語で1文ずつ書き出すと、違いがはっきりする。"],
                pc=[("A の説明", 3), ("B の説明", 3), ("形の違いの指摘", 2)],
                pit=["過去形を見て「過去の話」と説明する。", "和訳だけを書き、どの形が違いを生んでいるかを書かない。"])


PROMPTS = [
    ("宇宙飛行士", "If I were an astronaut, I would go to the moon. I would take a lot of pictures of the earth from there."),
    ("総理大臣", "If I were the prime minister, I would make more parks for children. I would also make school lunch free for everyone."),
    ("鳥", "If I were a bird, I would fly over the sea to other countries. I could see many beautiful places from the sky."),
    ("学校の校長先生", "If I were the principal of our school, I would make a new library. Students could read many books there."),
    ("透明人間", "If I were invisible, I would visit a famous kitchen. I could learn how the cooks make delicious food."),
    ("100歳", "If I were 100 years old, I would tell young people about my life. I would talk about the changes in our town."),
]


@gen("thinking_writing", 3, ["application", "written_reasoning"])
def write_if_were(r):
    who, model = r.choice(PROMPTS)
    return desc(f"「もしあなたが{who}だったら、何をするか」を英語で2文書きなさい。1文目は If I were ～, I would ―. の形を使い、2文目は would か could を使ってくわしく説明すること。",
                f"（解答例）{model}", "（解答例の解説）1文目は if の中に be 動詞 were、主節に would＋原形を使っている。2文目も仮定の話の続きなので、would / could＋原形を使う。",
                [("1文目が If I were ～, I would ―. の形で正しく書けている", 3), ("2文目に would / could＋原形を正しく使い、内容がつながっている", 3), ("つづり・語順・大文字・ピリオドが正しい", 2)], d=4, p=8, lines=4,
                ap="現在の事実（実際は～ではない）をふまえて、空想の話を would / could で続ける。2文目も仮定の話なので現在形にしない。",
                steps=["If I were ～, の部分を書く（be 動詞は were）。", "主節に would＋動詞の原形で「何をするか」を書く。",
                       "2文目で、would / could＋原形を使ってくわしく説明する。", "動詞の形（were / would / could＋原形）を見直す。"],
                alt=["書いた2文を日本語に訳し、「～なら…するだろう」「…できるだろう」と、空想の話として一貫しているかを確かめる。"],
                pc=[("1文目の形", 3), ("2文目の形と内容", 3), ("表記の正確さ", 2)],
                pit=["If I am ～ と現在形を使う。", "2文目で will / can を使い、仮定の話が現実の話にもどってしまう。"])


WISHES = [
    ("楽器", "I wish I could play the piano. But I can't, so I will start practicing this year.",
     "1文目は I wish I could＋原形 で願望、2文目は現在の事実（can't）と、これからの行動（will）を書いている。"),
    ("ペット", "I wish I had a dog. But my apartment is too small for a dog.",
     "1文目は I wish I had ～ で願望、2文目は現在の事実（アパートがせまい）を現在形で書いている。"),
    ("外国語", "I wish I could speak English like a native speaker. But I still make many mistakes.",
     "1文目は I wish I could＋原形 で願望、2文目は現在の事実を現在形で書いている。"),
    ("天気", "I wish it were sunny today. But it is raining, so I can't play soccer.",
     "1文目は I wish it were ～ で願望、2文目は現在の事実（雨）と結果を現在形で書いている。"),
    ("時間", "I wish I had more time to read books. But I am very busy with club activities.",
     "1文目は I wish I had ～ で願望、2文目は現在の事実（部活動で忙しい）を現在形で書いている。"),
    ("家族", "I wish my grandparents lived near us. But they live far away in Kyushu.",
     "1文目は I wish＋主語＋過去形 で願望、2文目は現在の事実を現在形で書いている。"),
]


@gen("thinking_writing", 3, ["written_reasoning", "application"])
def write_wish(r):
    theme, model, point = r.choice(WISHES)
    return desc(f"「{theme}」について、今は実現していない願望を英語で2文書きなさい。1文目は I wish ～. の文、2文目は But で始めて現在の事実を書くこと。また、1文目と2文目で動詞の形（時制）が違う理由を日本語で説明しなさい。",
                f"（解答例）{model}　理由：1文目は事実と違う願望なので仮定法過去（過去形）、2文目は現在の事実なので現在形を使う。",
                f"（解答例の解説）{point}",
                [("I wish の後ろを正しい過去形（were / had / could＋原形 など）にしている", 3), ("2文目で現在の事実を現在形で書いている", 2), ("時制が違う理由を説明している", 3)], d=4, p=8, lines=5,
                ap="1文目は「事実と違う願望」、2文目は「本当の事実」。どちらも今のことだが、表す内容が違うので動詞の形が変わる。",
                steps=["実現していない願望を決める。", "I wish＋主語＋過去形（were / had / could＋原形）で1文目を書く。", "But ～. で現在の事実を現在形で書く。", "時制の違いの理由を説明する。"],
                alt=["2文目の事実を、1文目の願望と肯定・否定が逆になっているかで確かめる（I wish I could ～ ↔ I can't ～）。"],
                pc=[("1文目の仮定法", 3), ("2文目の現在形", 2), ("理由の説明", 3)],
                pit=["1文目を I wish I can ～ と現在形にする。", "2文目まで過去形にして、事実の文が過去の話になってしまう。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(task, wrong, step, etype, tempt, fix, expl, steps, ap, alt, pit):
    return desc(f"{task}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい英文に書き直しなさい。", fix, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい英文に直している", 3), ("文法のルールを説明している", 1)], d=3, p=6, lines=4,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい英文", 3), ("ルールの説明", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix))


IF_ERR = [
    ("もし私が鳥なら、空を飛べるのに。", "If I am a bird, I could fly in the sky.", "If I were a bird, I could fly in the sky.", "am", "condition",
     "現在の事実と違う仮定なので、if の中の be 動詞は過去形 were にする。", "現在のことなので現在形 am を使った。"),
    ("もし私があなたなら、先生に相談するだろう。", "If I were you, I will ask the teacher.", "If I were you, I would ask the teacher.", "will", "condition",
     "if の中が仮定法（were）なので、主節も would＋原形にする。", "「相談するだろう」を未来の will で表した。"),
    ("もし時間があれば、そのお祭りに行くのに。", "If I had time, I would went to the festival.", "If I had time, I would go to the festival.", "would went", "notation",
     "would の後ろは動詞の原形。went を go にする。", "仮定法は過去形を使うと覚え、would の後ろまで過去形にした。"),
    ("もし彼の住所を知っていれば、手紙を書けるのに。", "If I know his address, I could write to him.", "If I knew his address, I could write to him.", "know", "condition",
     "主節が could の仮定法なので、if の中も過去形 knew にする。", "「知っていれば」を現在形で表した。"),
    ("もし犬を飼っていれば、毎日散歩させるのに。", "If I have a dog, I would walk it every day.", "If I had a dog, I would walk it every day.", "have", "condition",
     "実際は飼っていないので仮定法。if の中は過去形 had にする。", "今のことなので現在形 have を使った。"),
    ("もし私がもっとお金持ちなら、この車を買うのに。", "If I were richer, I can buy this car.", "If I were richer, I could buy this car.", "can", "condition",
     "if の中が仮定法（were）なので、主節も can の過去形 could にする。", "「買える」を can で表した。"),
]


@gen("error_correction", 4, ["common_error", "condition_check"])
def err_if(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(IF_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", etype, tempt, fix, f"{rule}正しくは {fix}",
                    ["日本語が「～なら…のに」（現在の事実と違う仮定）であることを確かめる。", f"「{where}」の部分の誤りを見つける：{rule}", f"正しい英文：{fix}"],
                    "仮定法過去は「if の中は過去形（be は were）」「主節は would / could＋原形」の2点がそろって完成する。",
                    ["直した文から現在の事実（実際は～ない）を考え、事実と違う仮定の形になっているかを確かめる。"],
                    ["if の中か主節の片方だけを過去にする。", "would / could の後ろの動詞まで過去形にする。"])


WISH_ERR = [
    ("もっと上手に歌えたらいいのに。", "I wish I can sing better.", "I wish I could sing better.", "can", "condition",
     "wish の後ろは仮定法過去なので、can の過去形 could にする。", "今の願望なので現在形 can を使った。"),
    ("妹がいればいいのに。", "I wish I have a sister.", "I wish I had a sister.", "have", "condition",
     "wish の後ろは仮定法過去なので、過去形 had にする。", "今のことなので現在形 have を使った。"),
    ("今日が日曜日ならいいのに。", "I wish today is Sunday.", "I wish today were Sunday.", "is", "condition",
     "wish の後ろの be 動詞は、主語が today（単数）でも were にする。", "today は単数なので is を使った。"),
    ("あなたが私たちといっしょにいてくれたらいいのに。", "I wish you will be with us.", "I wish you were with us.", "will be", "concept",
     "wish の後ろに will は使わない。現在の事実と違う願望なので過去形 were にする。", "これからのことを願うと考え、will を使った。"),
    ("明日晴れるといいな。", "I wish it will be sunny tomorrow.", "I hope it will be sunny tomorrow.", "wish", "concept",
     "明日晴れる可能性があるので、wish ではなく hope を使う。hope の後ろは will や現在形でよい。", "「～だといいな」をいつも wish で表した。"),
    ("その答えを知っていればいいのに。", "I wish I know the answer.", "I wish I knew the answer.", "know", "condition",
     "wish の後ろは仮定法過去なので、過去形 knew にする。", "今知らないことなので、現在形 know を使った。"),
]


@gen("error_correction", 3, ["common_error", "concept"])
def err_wish(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(WISH_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", etype, tempt, fix, f"{rule}正しくは {fix}",
                    ["日本語が「事実と違う願望（～ならいいのに）」か、「起こりうることへの願い（～だといいな）」かを確かめる。", f"「{where}」の部分の誤りを見つける：{rule}", f"正しい英文：{fix}"],
                    "事実と違う願望は I wish＋過去形（were / had / could）、起こりうることへの願いは I hope＋現在形・will。",
                    ["直した文の「現在の事実」を考え、wish なら事実と反対、hope なら可能性があることを確かめる。"],
                    ["wish の後ろに現在形や will を使う。", "実現の可能性があるのに wish を使う。"])


MIX_ERR = [
    ("明日雨が降ったら、私は家で本を読みます。", "If it will rain tomorrow, I will read books at home.", "If it rains tomorrow, I will read books at home.", "will rain", "condition",
     "実際に起こりうる条件を表す if の中は、未来のことでも現在形にする。", "tomorrow があるので未来の will を使った。"),
    ("もし私がねこなら、一日中寝ているだろう。", "If I were a cat, I sleep all day.", "If I were a cat, I would sleep all day.", "I sleep", "logic",
     "仮定法の主節は would＋原形。現在形 sleep では、事実と違う仮定の結果を表せない。", "主節の would を落とした。"),
    ("もし魔法が使えたら、世界を平和にするのに。", "If I can use magic, I would make the world peaceful.", "If I could use magic, I would make the world peaceful.", "can", "condition",
     "主節が would の仮定法なので、if の中も can の過去形 could にする。", "「使えたら」を現在形の can で表した。"),
    ("ひまだったら、あなたを手伝います（実際にひまかもしれない）。", "If I were free, I will help you.", "If I am free, I will help you.", "were", "interpretation",
     "ひまである可能性がある（実際に起こりうる）条件なので直説法。if の中は現在形 am にする。", "if を見て、いつも仮定法の were を使うと考えた。"),
    ("もし私があなたなら、そのチケットを買うだろう。", "If I were you, I would buy the ticket yesterday.", "If I were you, I would buy the ticket.", "yesterday", "interpretation",
     "仮定法過去は現在の事実と違う仮定で、過去の出来事ではない。過去を表す yesterday は合わない。", "過去形を使うので、過去のことだと考えた。"),
    ("もっと時間があれば、ピアノの練習ができるのに。", "If I had more time, I could practiced the piano.", "If I had more time, I could practice the piano.", "could practiced", "notation",
     "could の後ろは動詞の原形 practice にする。", "仮定法なので過去形にすると考え、could の後ろまで過去形にした。"),
]


@gen("error_correction", 3, ["common_error", "computation"])
def err_mix(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(MIX_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", etype, tempt, fix, f"{rule}正しくは {fix}",
                    ["日本語が「起こりうる条件」か「事実と違う仮定」かを確かめる。", f"「{where}」の部分の誤りを見つける：{rule}", f"正しい英文：{fix}"],
                    "起こりうる条件は〈If＋現在形, will ～〉、事実と違う仮定は〈If＋過去形, would / could＋原形〉。この2つの型を混ぜない。",
                    ["直した文の if の中と主節の形が、同じ型（直説法どうし・仮定法どうし）でそろっているかを確かめる。"],
                    ["if の中と主節で、直説法と仮定法の形を混ぜる。", "条件の if の中に will を使う。"])


GENERATORS = [if_were, main_clause, wish_form, fact_behind, mood_choice,
              real_to_if, sorry_to_wish, build_order, meaning, comp_mix,
              explain_difference, write_if_were, write_wish,
              err_if, err_wish, err_mix]
