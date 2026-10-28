"""単元パック：英語コミュニケーションⅠ 仮定法（仮定法過去・仮定法過去完了・混合仮定法・I wish / as if / without）。"""
from banks._common import desc, mc, sa
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem,
                         tp)

UNIT_ID = "HS-ENG-U08"

# ======================================================================
# 授業プリント
# ======================================================================

LESSON = lesson(
    goals=["仮定法過去・仮定法過去完了・混合仮定法の形を、「事実の時」と「仮定の時制」の対応から正しく作れる。",
           "I wish / as if / If only / It's time の後ろの時制を、主節との時間関係から判断できる。",
           "without / but for / if it were not for、if を省略した倒置、were to / should などの仮定の表し方を使い分けられる。"],
    duration=50,
    readiness=["中学3年で学んだ仮定法過去（If I were ～, I would ～ ／ I wish I could ～）を使える。",
               "動詞の過去形・過去分詞を正しく作れ、過去完了（had＋過去分詞）の形を知っている。",
               "助動詞 will / can / may の過去形 would / could / might を知っている。"],
    flow=[("導入：事実と仮定", 5, "「お金があれば買うのに」と「お金があれば買う」の違いを考えさせ、事実に反する仮定という視点を示す"),
          ("仮定法過去・過去完了", 13, "時制を1つ過去にずらす仕組みを導出し、形を表にまとめる（例題1）"),
          ("混合仮定法", 10, "if 節と主節で「事実の時」が異なる文を、時を表す語（now / then）から判断する（例題2）"),
          ("I wish / as if / without・倒置", 15, "願望・様子・条件の名詞句化・倒置を整理する（例題3）"),
          ("まとめと確認", 7, "確認問題3問、問題プリントA の課題指示")],
    sections=[
        intro("in1", "「事実と違う」ことを、時制で伝える",
              "If I have time, I will help you. は「時間があれば手伝う」という、実際に起こり得る条件を述べている。一方、If I had time, I would help you. は「（実際には時間がないが）時間があれば手伝うのに」という、現在の事実に反する仮定を述べている。英語では、話し手が「これは事実ではない」と考えていることを、動詞の時制を過去にずらすことで示す。これが仮定法である。",
              bullets=["If I have time, I will help you.（直説法：時間があるかもしれない）",
                       "If I had time, I would help you.（仮定法過去：今、時間がない）",
                       "If I had had time, I would have helped you.（仮定法過去完了：あのとき、時間がなかった）"],
              points=[tp("3つの文を板書し、それぞれ「実際に時間はあるか」を生徒に答えさせる。", ask="2文目の話し手は、今、時間があるのか。",
                         expect="時間はない。だから手伝えない。", timing="導入の冒頭"),
                      tp("仮定法過去は「過去のこと」ではなく「現在の事実に反すること」を表す、という点を最初にはっきりさせる。", caution="形が過去形なので、過去の話だと誤解する生徒が多い。")]),
        definition("df1", "仮定法過去と仮定法過去完了",
                   "仮定法過去は現在（または未来）の事実に反する仮定を、仮定法過去完了は過去の事実に反する仮定を表す。if 節と主節の動詞の形は、次のように決まっている。",
                   formula="仮定法過去：If S＋過去形（be 動詞は were）, S would / could / might＋原形 ／ 仮定法過去完了：If S＋had＋過去分詞, S would / could / might＋have＋過去分詞",
                   bullets=["If I were you, I would accept the offer.（私があなたなら、その申し出を受けるのに）",
                            "If I had left home earlier, I would have caught the train.（もっと早く家を出ていたら、電車に間に合ったのに）",
                            "would は「～だろう」、could は「～できるだろう」、might は「～かもしれない」を表す。"],
                   conditions=["if 節には will / would を使わない（If I would have time … は誤り）。",
                               "仮定法過去の be 動詞は、主語が I や3人称単数でも were が正式な形である。"],
                   points=[tp("「if 節」と「主節」の2列の表を作り、仮定法過去・過去完了の形を埋めさせる。", ask="仮定法過去完了の主節に入る形は何か。", expect="would / could / might＋have＋過去分詞。")]),
        theorem("th1", "混合仮定法（if 節と主節で時が違う場合）",
                "If S＋had＋過去分詞（過去の事実に反する）, S would＋原形（現在の事実に反する）＋now など",
                ["if 節の「時」と主節の「時」を別々に判断し、それぞれに合った形を選ぶ。",
                 "過去の事実に反する部分 → had＋過去分詞／would have＋過去分詞。現在の事実に反する部分 → 過去形／would＋原形。",
                 "now・today・then・yesterday・last year など、時を表す語句が判断の手がかりになる。"],
                body="例：If I had taken that flight, I would be in Sapporo now.（あの便に乗っていたら、今ごろ札幌にいるだろう）。逆に、現在も変わらない性質が過去の結果に影響した場合は If he were not so shy, he would have spoken to her yesterday. となる。",
                points=[tp("文中の時を表す語句に下線を引かせ、if 節と主節のそれぞれが「現在」「過去」のどちらの事実に反するかを書きこませる。",
                           ask="If I had taken that flight, I would have been in Sapporo now. はなぜおかしいのか。", expect="now があるので主節は現在の事実に反する内容。would＋原形にする。")]),
        derivation("dv1", "なぜ時制を1つ過去にずらすのか",
                   ["① 事実の文を確認する：I don't have time, so I can't help you.（現在の事実）",
                    "② 事実と反対の内容を仮定する：「時間がある」「手伝える」。",
                    "③ 事実と距離があることを示すため、時制を1つ過去にずらす：have → had、can → could。",
                    "④ If I had time, I could help you. が完成する。過去形は「時間的な距離」だけでなく「現実からの距離」も表せる。",
                    "⑤ 過去の事実（I didn't have time, so I couldn't help you.）に反する場合は、過去形をさらに1つ過去にずらす：didn't have → had had、couldn't help → could have helped。",
                    "⑥ よって、現在の事実に反する → 過去形、過去の事実に反する → 過去完了形、という対応が成り立つ。"],
                   body="この考え方を使えば、I wish / as if の後ろの時制も同じように決まる。I wish I knew.（今知らないのが残念）／ I wish I had known.（あのとき知らなかったのが残念）。",
                   points=[tp("事実の文を板書し、時制を1つずつ過去にずらす操作を矢印で示す。", ask="I can't swim. から「泳げたらいいのに」を作ると、can はどうなるか。",
                              expect="could になり、I wish I could swim. となる。", timing="手順③の説明時")]),
        definition("df2", "I wish / as if / without と、if を使わない仮定",
                   "仮定法は if 節以外にも、願望・様子のたとえ・条件を表す語句とともに使われる。",
                   bullets=["I wish＋仮定法過去（現在の事実に反する願望）／ I wish＋仮定法過去完了（過去の事実に反する願望）。If only ～! はより強い願望。",
                            "as if＋仮定法過去（主節と同じ時の事実に反する）／ as if＋仮定法過去完了（主節より前の事実に反する）。",
                            "Without / But for ～ ＝ If it were not for ～（現在）／ If it had not been for ～（過去）。With ～ は「～があれば」。",
                            "if の省略による倒置：Were I you, … ／ Had I known, … ／ Should it rain, …",
                            "If S were to ～ ／ If S should ～：実現の可能性が低い未来の仮定。",
                            "It's time＋S＋過去形：「もう～してもいいころだ」（まだしていないことを促す）。"],
                   conditions=["I wish の後ろに can / will は使わない（I wish I could ～、I wish S would ～ とする）。",
                               "Without ～ の文では、主節の形（would＋原形か would have＋過去分詞か）で現在の仮定か過去の仮定かを判断する。"],
                   points=[tp("hope と wish を対比させ、hope は実現の可能性がある願望、wish は実現しにくい・事実に反する願望であることを確認する。", caution="I wish you will pass. のように hope と同じ形で書く誤りが多い。")]),
        example("ex1", "例題1　仮定法過去と過去完了",
                "次の英文を、事実に反する仮定を表す文に書きかえなさい。(1) As I don't have a car, I can't drive you home.　(2) Because he didn't get up early, he missed the train.",
                ["(1) 現在の事実（車を持っていない）に反するので仮定法過去：don't have → had、can't → could。", "(1) If I had a car, I could drive you home.",
                 "(2) 過去の事実（早く起きなかった）に反するので仮定法過去完了：didn't get up → had gotten up、missed → would not have missed。", "(2) If he had gotten up early, he would not have missed the train."],
                "(1) If I had a car, I could drive you home.　(2) If he had gotten up early, he would not have missed the train.（had got up も可）",
                thinking="事実の文が現在か過去かを確認し、肯定・否定を逆にしてから、時制を1つ過去にずらす。",
                points=[tp("(2) で「否定 → 肯定」「肯定 → 否定」の入れかえを忘れる生徒が多いので、事実と仮定の内容を日本語で先に書かせる。")],
                misconceptions=[("If he got up early, he would not miss the train.", "過去の事実に反するので仮定法過去完了にする")]),
        example("ex2", "例題2　混合仮定法",
                "日本語に合うように（　）内の動詞を適切な形にしなさい。昨夜もっと早く寝ていたら、今こんなに眠くないだろうに。\nIf I (go) to bed earlier last night, I (not be) so sleepy now.",
                ["if 節は last night があるので過去の事実に反する：had gone。", "主節は now があるので現在の事実に反する：would not be。"],
                "If I had gone to bed earlier last night, I would not be so sleepy now.",
                thinking="if 節と主節の「時」を、それぞれの時を表す語（last night と now）から別々に判断する。",
                points=[tp("if 節と主節の上に「過去」「現在」と書きこませてから形を決めさせる。", ask="主節を would not have been にするとどんな意味になるか。",
                           expect="「（昨夜の時点で）眠くなかっただろう」となり、now と合わない。")]),
        example("ex3", "例題3　I wish / as if / without",
                "（　）内から適切なものを選びなさい。(1) I wish I (can / could) speak Chinese.　(2) She looked as if she (saw / had seen) a ghost.　(3) (Without / With) your help, I could not have finished the report.",
                ["(1) I wish の後ろは仮定法。現在の事実（話せない）に反するので could。",
                 "(2) 見えた時（looked）より前に「幽霊を見た」ことになるので had seen。",
                 "(3) 「あなたの助けがなかったら」なので Without。主節が could not have finished なので過去の仮定。"],
                "(1) could　(2) had seen　(3) Without",
                thinking="I wish・as if の後ろは、主節と同じ時なら仮定法過去、主節より前なら仮定法過去完了。",
                points=[tp("(2) で「同じ時」と「前の時」の違いを数直線で示す。")]),
        board("bd1", "板書案",
              [("① 仮定法の形", ["現在の事実に反する → 過去形", "If S 過去形, S would＋原形", "過去の事実に反する → 過去完了", "If S had p.p., S would have p.p.", "if 節に will / would ×"]),
               ("② 混合仮定法", ["時を表す語に注目（then / now）", "If S had p.p.（過去）,", "S would＋原形 now（現在）", "If S 過去形（今も）,", "S would have p.p.（過去）"]),
               ("③ if を使わない仮定", ["I wish S 過去形 ／ had p.p.", "as if S 過去形 ／ had p.p.", "Without ～ ＝ If it were not for ～", "Were I ～ ／ Had I p.p. ／ Should S", "It's time S 過去形"])],
              points=[tp("①の列は「事実の時」と「仮定法の形」の対応表として整理し、②③は①の応用であることを矢印で示す。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("仮定法の文を作る前に、必ず「事実の文」を日本語か英語で書かせる。事実の時が決まれば形も決まる。", ask="この文の事実は現在か過去か。", expect="時を表す語句から判断できる。"),
               tp("if 節に would を入れる誤りは日本語の「～だろう」につられたものが多いので、if 節は「条件」なので推量の助動詞を使わないと説明する。", caution="If I would have time … は誤り。"),
               tp("as if の後ろの時制は、主節の時制とは独立に「主節と同じ時か、前の時か」で決まることを、talks / talked の両方で確認させる。", timing="例題3の後"),
               tp("Without ～ の文は主節の形が時を決めることを強調し、If it were not for / If it had not been for への書きかえで確かめさせる。"),
               tp("問題プリント D の誤答例を使い、「時のずれ」「if 節の would」「wish の後ろの can / will」の3種類を重点的に扱う。")],
              misconceptions=[("If I would have more time, I would read more books.", "if 節には would を使わない。If I had more time, …"),
                              ("I wish I can speak English fluently.", "I wish の後ろは仮定法なので could を使う"),
                              ("If she had left earlier, she would have been here now.", "now があるので主節は現在の事実に反する。she would be here now")]),
        summary("sm1", "まとめ",
                ["現在の事実に反する仮定は過去形（仮定法過去）、過去の事実に反する仮定は過去完了形（仮定法過去完了）で表す。",
                 "if 節と主節で事実の時が異なるときは、それぞれの時に合わせて形を選ぶ（混合仮定法）。",
                 "I wish・as if の後ろは「主節と同じ時→過去形、前の時→過去完了形」。Without ～・倒置・were to なども仮定を表す。"]),
        check("ck1", "確認問題",
              [("「私があなたなら、そんなことはしないだろう」を英語にしなさい。", "If I were you, I would not do such a thing."),
               ("If I had known the truth, I would have told you. を if を使わずに書きかえなさい。", "Had I known the truth, I would have told you."),
               ("I'm sorry I can't go with you. を I wish を使って書きかえなさい。", "I wish I could go with you.")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

IF_WHY = {
    "pres": ("現在形を使うと、実際に起こり得る条件を述べる直説法の文になる。主節の would などと形が合わない。", "直説法と仮定法の混同"),
    "pp": ("had＋過去分詞は過去の事実に反する仮定（仮定法過去完了）の形で、この文の「時」と合わない。", "仮定法過去と仮定法過去完了の混同"),
    "would": ("if 節には would / will を使わない。条件を表す if 節では、動詞そのものの時制で仮定を示す。", "if 節への推量の助動詞の混入"),
    "past": ("過去形は現在の事実に反する仮定（仮定法過去）の形で、過去の事実に反する仮定には使えない。", "仮定法過去と仮定法過去完了の混同"),
    "perf": ("現在完了は直説法の形で、事実に反する仮定を表せない。", "現在完了と過去完了の混同"),
}
MAIN_WHY = {
    "will": ("will / can / may など助動詞の現在形は直説法の形で、仮定法の if 節と組み合わせることはできない。", "直説法と仮定法の混同"),
    "wh": ("would have＋過去分詞は過去の事実に反する結果を表す形で、この文の「時」と合わない。", "仮定法過去と仮定法過去完了の混同"),
    "past": ("主節にはふつう would / could / might などの助動詞の過去形が必要。動詞の過去形だけでは、過去の事実を述べる文になってしまう。", "主節の助動詞の脱落"),
    "wbase": ("would＋原形は現在の事実に反する結果を表す形で、過去の事実に反する仮定には would have＋過去分詞が必要。", "仮定法過去と仮定法過去完了の混同"),
    "hadpp": ("主節に had＋過去分詞を使うと、仮定の結果を表せない。助動詞の過去形＋have＋過去分詞が必要。", "主節の助動詞の脱落"),
}

# (if 節, 主節, if の正答, [(誤答, 種類)], 主節の正答, [(誤答, 種類)], 和訳)
PAST = [
    ("If I {0} her phone number,", "I {1} her.", "knew", [("know", "pres"), ("had known", "pp"), ("would know", "would")],
     "would call", [("will call", "will"), ("would have called", "wh"), ("called", "past")], "彼女の電話番号を知っていれば、電話するのに。"),
    ("If I {0} more time,", "I {1} you.", "had", [("have", "pres"), ("had had", "pp"), ("would have", "would")],
     "could help", [("can help", "will"), ("could have helped", "wh"), ("helped", "past")], "もっと時間があれば、手伝えるのに。"),
    ("If I {0} you,", "I {1} the offer.", "were", [("am", "pres"), ("had been", "pp"), ("would be", "would")],
     "would accept", [("will accept", "will"), ("would have accepted", "wh"), ("accepted", "past")], "私があなたなら、その申し出を受けるのに。"),
    ("If it {0} not raining,", "we {1} tennis.", "were", [("is", "pres"), ("had been", "pp"), ("would be", "would")],
     "could play", [("can play", "will"), ("could have played", "wh"), ("played", "past")], "雨が降っていなければ、テニスができるのに。"),
    ("If he {0} near here,", "he {1} us more often.", "lived", [("lives", "pres"), ("had lived", "pp"), ("would live", "would")],
     "would visit", [("will visit", "will"), ("would have visited", "wh"), ("visited", "past")], "彼がこの近くに住んでいれば、もっと頻繁に私たちを訪ねてくれるだろうに。"),
    ("If we {0} a car,", "we {1} to the beach.", "had", [("have", "pres"), ("had had", "pp"), ("would have", "would")],
     "would drive", [("will drive", "will"), ("would have driven", "wh"), ("drove", "past")], "車があれば、海辺まで車で行くのに。"),
    ("If my sister {0} here,", "she {1} what to do.", "were", [("is", "pres"), ("had been", "pp"), ("would be", "would")],
     "would know", [("will know", "will"), ("would have known", "wh"), ("knew", "past")], "姉がここにいれば、どうすればいいかわかるだろうに。"),
    ("If I {0} French,", "I {1} with them.", "spoke", [("speak", "pres"), ("had spoken", "pp"), ("would speak", "would")],
     "could talk", [("can talk", "will"), ("could have talked", "wh"), ("talked", "past")], "フランス語が話せれば、彼らと話ができるのに。"),
    ("If this bag {0} cheaper,", "I {1} it.", "were", [("is", "pres"), ("had been", "pp"), ("would be", "would")],
     "would buy", [("will buy", "will"), ("would have bought", "wh"), ("bought", "past")], "このかばんがもっと安ければ、買うのに。"),
    ("If you {0} up earlier,", "you {1} late for school.", "got", [("get", "pres"), ("had got", "pp"), ("would get", "would")],
     "would not be", [("will not be", "will"), ("would not have been", "wh"), ("were not", "past")], "もっと早く起きれば、学校に遅刻しないだろうに。"),
]

PERF = [
    ("If I {0} home earlier,", "I {1} the train.", "had left", [("left", "past"), ("have left", "perf"), ("would have left", "would")],
     "would have caught", [("would catch", "wbase"), ("will catch", "will"), ("had caught", "hadpp")], "もっと早く家を出ていれば、電車に間に合ったのに。"),
    ("If you {0} me the truth,", "I {1} you.", "had told", [("told", "past"), ("have told", "perf"), ("would have told", "would")],
     "would have helped", [("would help", "wbase"), ("will help", "will"), ("had helped", "hadpp")], "本当のことを話してくれていたら、あなたを助けたのに。"),
    ("If it {0},", "we {1} hiking.", "had not rained", [("did not rain", "past"), ("has not rained", "perf"), ("would not have rained", "would")],
     "could have gone", [("could go", "wbase"), ("can go", "will"), ("had gone", "hadpp")], "雨が降らなかったら、ハイキングに行けたのに。"),
    ("If she {0} the medicine,", "she {1} sooner.", "had taken", [("took", "past"), ("has taken", "perf"), ("would have taken", "would")],
     "would have recovered", [("would recover", "wbase"), ("will recover", "will"), ("had recovered", "hadpp")], "その薬を飲んでいたら、彼女はもっと早く回復しただろうに。"),
    ("If we {0} about the party,", "we {1}.", "had known", [("knew", "past"), ("have known", "perf"), ("would have known", "would")],
     "would have come", [("would come", "wbase"), ("will come", "will"), ("had come", "hadpp")], "パーティーのことを知っていたら、私たちは来たのに。"),
    ("If he {0} more,", "he {1} the game.", "had practiced", [("practiced", "past"), ("has practiced", "perf"), ("would have practiced", "would")],
     "might have won", [("might win", "wbase"), ("may win", "will"), ("had won", "hadpp")], "もっと練習していたら、彼は試合に勝てたかもしれない。"),
    ("If I {0} an umbrella,", "I {1} wet.", "had brought", [("brought", "past"), ("have brought", "perf"), ("would have brought", "would")],
     "would not have gotten", [("would not get", "wbase"), ("will not get", "will"), ("had not gotten", "hadpp")], "傘を持ってきていたら、ぬれなかったのに。"),
    ("If they {0} earlier,", "they {1} the work on time.", "had started", [("started", "past"), ("have started", "perf"), ("would have started", "would")],
     "could have finished", [("could finish", "wbase"), ("can finish", "will"), ("had finished", "hadpp")], "もっと早く始めていたら、彼らは時間どおりに仕事を終えられたのに。"),
    ("If you {0} more careful,", "you {1} such a mistake.", "had been", [("were", "past"), ("have been", "perf"), ("would have been", "would")],
     "would not have made", [("would not make", "wbase"), ("will not make", "will"), ("had not made", "hadpp")], "もっと注意していたら、そんな間違いはしなかっただろうに。"),
    ("If the bus {0} on time,", "I {1} late.", "had come", [("came", "past"), ("has come", "perf"), ("would have come", "would")],
     "would not have been", [("would not be", "wbase"), ("will not be", "will"), ("had not been", "hadpp")], "バスが時間どおりに来ていたら、遅刻しなかったのに。"),
]


def _cond_item(r, bank, label, rule):
    a, b, iok, iw, mok, mw, jp = r.choice(bank)
    slot = r.choice([0, 1])
    fill = [iok, mok]
    fill[slot] = "(　　)"
    s = f"{a.format(*fill)} {b.format(*fill)}"
    ok, wrongs = (iok, iw) if slot == 0 else (mok, mw)
    why = {w: (IF_WHY if slot == 0 else MAIN_WHY)[k] for w, k in wrongs}
    full = f"{a.format(iok, mok)} {b.format(iok, mok)}"
    part = "if 節" if slot == 0 else "主節"
    return mc(f"日本語の意味になるように、（　）に入る最も適切なものを選びなさい。\n{jp}\n{s}", [ok] + [w for w, _ in wrongs],
              f"{ok} が入る。{rule}完成文：{full}", d=2,
              ap="和訳から、事実が現在のことか過去のことかを判断する。そのうえで（　）が if 節か主節かを確認し、決まった形を当てはめる。",
              steps=[f"和訳から、{label}の事実に反する仮定であると判断する。", f"（　）は{part}にある。", rule, f"答えは {ok}。"],
              alt=[f"事実の文（例：{'I don’t know …' if label == '現在' else 'I didn’t …'}）を作り、時制を1つ過去にずらして仮定法の形になるかを確かめる。"],
              pc=[("事実の時（現在か過去か）を判断している", 1), ("正しい形を選んでいる", 1)],
              pit=["if 節に would を入れる。", "仮定法過去と仮定法過去完了の形を取り違える。"], why=why)


@gen("basic_check", 5, ["computation", "concept"])
def past_form(r):
    return _cond_item(r, PAST, "現在", "現在の事実に反する仮定は仮定法過去：If S＋過去形（be 動詞は were）, S would / could / might＋原形。")


@gen("basic_check", 5, ["computation", "condition_check"])
def perf_form(r):
    return _cond_item(r, PERF, "過去", "過去の事実に反する仮定は仮定法過去完了：If S＋had＋過去分詞, S would / could / might＋have＋過去分詞。")


WISH = [
    ("I wish I (　　) a little taller.", "were", "もう少し背が高ければいいのに。",
     [("am", "I wish の後ろは仮定法。現在の事実に反する願望なので過去形 were を使う。"), ("had been", "had been は過去の事実に反する願望になる。「今」背が高ければという意味に合わない。"),
      ("will be", "I wish の後ろに will は使わない。")]),
    ("I wish I (　　) harder when I was young.", "had studied", "若いころもっと勉強していればよかった。",
     [("studied", "when I was young とあり過去の事実に反する願望なので、過去形ではなく過去完了形を使う。"), ("study", "I wish の後ろは仮定法。現在形は使えない。"),
      ("would study", "would study は現在・未来についての願望で、過去の事実に反する願望を表せない。")]),
    ("He talks as if he (　　) the president of the company.", "were", "彼はまるで自分が社長であるかのように話す。",
     [("had been", "had been は主節より前の事実に反する内容（社長だったかのように）になり、和訳と合わない。"), ("be", "as if の後ろには主語に合った動詞の形が必要で、原形は使えない。"),
      ("will be", "as if＋仮定法では will は使わない。")]),
    ("She looked as if she (　　) a ghost.", "had seen", "彼女はまるで幽霊を見たかのような顔をしていた。",
     [("sees", "主節が looked（過去）で、見たのはそれより前のことなので had seen。"), ("has seen", "現在完了は過去の主節と組み合わせられない。"),
      ("would see", "would see は未来の推量で、「見たかのような」という意味にならない。")]),
    ("I wish you (　　) here with us now.", "were", "今あなたがここにいてくれたらいいのに。",
     [("are", "I wish の後ろは仮定法なので、現在の事実に反する願望には過去形 were を使う。"), ("had been", "had been は過去の事実に反する願望になり、now と合わない。"),
      ("will be", "I wish の後ろに will は使わない。")]),
    ("I wish I (　　) that to her yesterday.", "had not said", "昨日、彼女にあんなことを言わなければよかった。",
     [("did not say", "yesterday の事実に反する願望なので、過去形ではなく過去完了形を使う。"), ("have not said", "現在完了は I wish＋仮定法の形として使えない。"),
      ("would not say", "would not say は現在・未来についての願望で、昨日のことには使えない。")]),
    ("If only I (　　) more money!", "had", "もっとお金があればなあ。",
     [("have", "If only の後ろは仮定法。現在の事実に反する願望なので過去形を使う。"), ("will have", "If only＋仮定法では will は使わない。"),
      ("had had", "had had は過去の事実に反する願望（あのときお金があれば）になり、和訳と合わない。")]),
    ("If only I (　　) to her advice then!", "had listened", "あのとき彼女の忠告を聞いてさえいればなあ。",
     [("listened", "then とあり過去の事実に反する願望なので、過去完了形を使う。"), ("listen", "If only の後ろは仮定法なので、現在形は使えない。"),
      ("would listen", "would listen は現在・未来についての願望で、then と合わない。")]),
    ("I wish it (　　) raining.", "would stop", "雨がやんでくれればいいのに。",
     [("stops", "I wish の後ろは仮定法。現在形は使えない。"), ("will stop", "I wish の後ろに will は使わない。これから先の変化を願うときは would を使う。"),
      ("has stopped", "現在完了は I wish＋仮定法の形として使えない。")]),
    ("He spoke to me as if we (　　) friends for years.", "had been", "彼はまるで私たちが何年も前から友達だったかのように話しかけてきた。",
     [("are", "主節が過去で、「何年も前から友達だった」という主節より前からの内容なので had been。"), ("will be", "as if＋仮定法では will は使わない。"),
      ("have been", "現在完了は過去の主節と組み合わせられない。")]),
    ("It's high time you (　　) your homework.", "did", "もう宿題をしてもいいころだ。",
     [("do", "It's (high) time の後ろの節は仮定法過去で、動詞は過去形にする。"), ("will do", "It's time の後ろに will は使わない。"),
      ("have done", "現在完了だと「もうしてしまった」ことになり、「まだしていないことを促す」意味にならない。")]),
    ("I wish I (　　) swim.", "could", "泳げたらいいのに。",
     [("can", "I wish の後ろは仮定法なので、can は過去形 could にする。"), ("will", "I wish の後ろに will は使わない。また「泳げる」という能力の意味にならない。"),
      ("have", "have を入れると I wish I have swim となり、文として成り立たない。")]),
]


@gen("basic_check", 5, ["condition_check", "common_error"])
def wish_asif(r):
    s, ok, jp, wrongs = r.choice(WISH)
    return mc(f"日本語の意味になるように、（　）に入る最も適切なものを選びなさい。\n{jp}\n{s}", [ok] + [w for w, _ in wrongs],
              f"{ok} が入る。I wish / If only / as if / It's time の後ろは仮定法で、主節と同じ時のことは過去形、主節より前のことは過去完了形で表す。", d=2,
              ap="（　）の前の I wish / as if などを見て仮定法だと判断し、願望・様子の内容が主節と同じ時か、それより前かを和訳から確かめる。",
              steps=["（　）の前の語句から、仮定法が必要な文だと判断する。", "内容が主節と同じ時か、主節より前の時かを和訳から判断する。", f"同じ時なら過去形、前の時なら過去完了形。答えは {ok}。"],
              alt=["事実の文（例：I am not tall. ／ I didn't study hard.）を作り、時制を1つ過去にずらした形と一致するかを確かめる。"],
              pc=[("仮定法が必要な文だと判断している", 1), ("時のずれを考えて正しい形を選んでいる", 1)],
              pit=["I wish の後ろに can / will をそのまま使う。"], why={w: (reason, "I wish / as if の後ろの時制の誤り") for w, reason in wrongs})


WITHOUT = [
    ("(　　) your advice, I would have failed.", "Without", "あなたの助言がなかったら、私は失敗していただろう。",
     [("With", "With ～ は「～があれば」という意味になり、和訳と逆になる。"), ("Unless", "unless は接続詞なので、後ろに名詞だけを置くことはできない。"),
      ("Because of", "because of は理由を表し、「～がなかったら」という仮定を表さない。")]),
    ("(　　) for the sun, nothing could live on the earth.", "But", "太陽がなければ、地球上の何も生きられないだろう。",
     [("Without", "without は単独で「～がなければ」を表すので、後ろに for は続かない。"), ("Except", "except for は「～を除けば」で、仮定の意味にはならない。"),
      ("If", "If for ～ という形はない。If it were not for ～ とする。")]),
    ("If it (　　) not for water, no living things could survive.", "were", "水がなければ、どんな生物も生きられないだろう。",
     [("is", "主節が could survive で現在の事実に反する仮定なので、if 節は仮定法過去にする。"), ("had been", "had been は過去の事実に反する仮定で、主節の could survive（現在）と合わない。"),
      ("would be", "if 節には would を使わない。")]),
    ("If it (　　) not been for his goal, we would have lost the game.", "had", "彼のゴールがなかったら、私たちは試合に負けていただろう。",
     [("were", "were not been という形は成り立たない。過去の事実に反する仮定は had not been for。"), ("has", "現在完了では事実に反する仮定を表せない。"),
      ("would", "if 節には would を使わない。")]),
    ("(　　) I you, I would apologize to her.", "Were", "私があなたなら、彼女に謝るだろう。",
     [("If", "If を使うなら If I were you の形が必要で、If I you では動詞がない。"), ("Am", "if を省略した倒置は Were I ～ の形で、Am は使えない。"),
      ("Had", "Had I you では動詞 were の働きをする語がなく、意味が通らない。")]),
    ("(　　) I known the truth, I would have told you.", "Had", "本当のことを知っていたら、あなたに話していただろう。",
     [("If", "If I known では had がなく、過去完了の形にならない。"), ("Did", "Did I known という形は成り立たない。"),
      ("Have", "Have I known は疑問文の形で、仮定の倒置にはならない。")]),
    ("(　　) it rain tomorrow, the game would be put off.", "Should", "万一明日雨が降れば、試合は延期されるだろう。",
     [("If", "If を使うなら If it should rain / If it rains となり、If it rain では動詞の形が合わない。"), ("Would", "would を文頭に出した倒置で仮定を表すことはない。"),
      ("Will", "Will it rain … は疑問文の形で、仮定を表さない。")]),
    ("She studied hard; (　　), she would have failed the exam.", "otherwise", "彼女は一生懸命勉強した。そうでなければ、試験に落ちていただろう。",
     [("however", "however は「しかし」で、仮定の意味を表さない。"), ("therefore", "therefore は「それゆえ」で、結果を表し、仮定の意味はない。"),
      ("unless", "unless は接続詞で、後ろに節が必要。単独で「そうでなければ」とはならない。")]),
    ("A wise man (　　) not have said such a thing.", "would", "賢い人ならそんなことは言わなかっただろう。",
     [("will", "will not have said は「言っていないだろう」という未来完了・推量で、事実に反する仮定にならない。"), ("does", "does not have said という形は成り立たない。"),
      ("had", "had not have said という形は成り立たない。")]),
    ("(　　) a little more effort, you could have won.", "With", "もう少し努力していれば、あなたは勝てただろうに。",
     [("Without", "Without ～ は「～がなければ」で、和訳と逆の意味になる。"), ("For", "For ～ だけでは「～があれば」という仮定を表さない。"),
      ("Unless", "unless は接続詞なので、後ろに名詞だけを置くことはできない。")]),
    ("If the sun (　　) to rise in the west, I would not change my mind.", "were", "たとえ太陽が西から昇ったとしても、私は決心を変えないだろう。",
     [("is", "is to は「～することになっている」という予定の意味で、ありえない仮定にはならない。"), ("had", "had to は「～しなければならなかった」で、意味が合わない。"),
      ("would", "if 節には would を使わない。")]),
    ("If it (　　) not for the Internet, our lives would be very different.", "were", "インターネットがなければ、私たちの生活はずいぶん違うだろう。",
     [("is", "主節が would be で現在の事実に反する仮定なので、if 節は仮定法過去にする。"), ("had", "had not for という形は成り立たない。"),
      ("would", "if 節には would を使わない。")]),
]


@gen("basic_check", 5, ["concept", "computation"])
def without_inversion(r):
    s, ok, jp, wrongs = r.choice(WITHOUT)
    return mc(f"日本語の意味になるように、（　）に入る最も適切なものを選びなさい。\n{jp}\n{s}", [ok] + [w for w, _ in wrongs],
              f"{ok} が入る。if 節の代わりに without / but for / with、倒置（Were / Had / Should）、otherwise、主語などで仮定を表すことができる。", d=2,
              ap="文に if がないときは、仮定の条件を表している部分（前置詞句・倒置・otherwise・主語）を探す。主節の形から現在の仮定か過去の仮定かを判断する。",
              steps=["主節の形（would＋原形か、would have＋過去分詞か）を確認する。", "仮定の条件がどの語句で表されているかを考える。", f"形と意味が合う {ok} を選ぶ。"],
              alt=["if を使った文（If it were not for ～ / If I were you など）に戻して、意味と形が一致するかを確かめる。"],
              pc=[("仮定の条件を表す部分に気づいている", 1), ("正しい語を選んでいる", 1)],
              pit=["unless の後ろに名詞だけを置く。", "倒置で had / were / should 以外の語を文頭に出す。"], why={w: (reason, "if を使わない仮定の表し方の誤り") for w, reason in wrongs})


# ======================================================================
# B 標準演習
# ======================================================================

MIXED = [
    ("If I had gone to bed earlier last night, I (　　) so sleepy now.", "would not be", "昨夜もっと早く寝ていたら、今こんなに眠くないだろうに。", "now",
     [("would not have been", "now があるので主節は現在の事実に反する内容。would have＋過去分詞は過去の結果になる。"), ("will not be", "仮定法の主節に will は使わない。"),
      ("had not been", "主節には助動詞の過去形が必要で、had＋過去分詞では仮定の結果を表せない。")]),
    ("If she had not missed the bus, she (　　) here now.", "would be", "彼女がバスに乗り遅れなかったら、今ここにいるだろうに。", "now",
     [("would have been", "now があるので現在の事実に反する結果を表す would＋原形を使う。"), ("will be", "仮定法の主節に will は使わない。"),
      ("is", "is では現在の事実を述べる文になり、仮定の結果を表せない。")]),
    ("If you had followed my advice then, you (　　) in trouble now.", "would not be", "あのとき私の助言に従っていたら、今困っていないだろうに。", "now",
     [("would not have been", "now があるので現在の事実に反する結果を表す would＋原形を使う。"), ("will not be", "仮定法の主節に will は使わない。"),
      ("are not", "are not では現在の事実を述べる文になり、仮定の結果を表せない。")]),
    ("If he (　　) the job offer last year, he would be living in London now.", "had accepted", "昨年その仕事の申し出を受けていたら、彼は今ロンドンに住んでいるだろう。", "last year",
     [("accepted", "last year とあり過去の事実に反する仮定なので、過去完了形を使う。"), ("has accepted", "現在完了は事実に反する仮定を表せず、last year とも一緒に使えない。"),
      ("would accept", "if 節には would を使わない。")]),
    ("If I (　　) English harder in high school, I could understand this article now.", "had studied", "高校でもっと英語を勉強していたら、今この記事が理解できるのに。", "in high school",
     [("studied", "in high school は過去のことなので、過去の事実に反する仮定は過去完了形にする。"), ("have studied", "現在完了は事実に反する仮定を表せない。"),
      ("would study", "if 節には would を使わない。")]),
    ("If he were not so shy, he (　　) to her at the party yesterday.", "would have spoken", "彼がそれほど内気でなければ、昨日のパーティーで彼女に話しかけていただろう。", "yesterday",
     [("would speak", "yesterday の出来事なので、主節は過去の事実に反する would have＋過去分詞にする。"), ("will speak", "仮定法の主節に will は使わない。"),
      ("had spoken", "主節には助動詞の過去形が必要で、had＋過去分詞では仮定の結果を表せない。")]),
    ("If I (　　) afraid of heights, I would have climbed the tower with you yesterday.", "were not", "私が高所恐怖症でなければ、昨日あなたと一緒にその塔に登っただろう。", "主節の yesterday と、if 節が今も変わらない性質であること",
     [("am not", "if 節は現在も続く事実に反する仮定なので、仮定法過去にする。"), ("will not be", "if 節には will を使わない。"),
      ("would not be", "if 節には would を使わない。")]),
    ("If we had bought the tickets in advance, we (　　) in this long line now.", "would not be standing", "前もってチケットを買っていたら、今この長い列に並んでいないだろうに。", "now",
     [("would not have stood", "now があるので現在の事実に反する結果を表す would＋原形（ここでは進行形）を使う。"), ("will not stand", "仮定法の主節に will は使わない。"),
      ("are not standing", "are not standing は現在の事実を述べる文で、仮定の結果を表せない。")]),
    ("If I had saved more money, I (　　) a new bike now.", "could buy", "もっとお金を貯めていたら、今新しい自転車が買えるのに。", "now",
     [("could have bought", "now があるので現在の事実に反する結果を表す could＋原形を使う。"), ("can buy", "仮定法の主節に can は使わない。"),
      ("bought", "主節には助動詞の過去形が必要。過去形だけでは過去の事実を述べる文になる。")]),
    ("If she (　　) Japanese as a child, she could read this book now.", "had learned", "彼女が子どものころに日本語を学んでいたら、今この本が読めるのに。", "as a child",
     [("learned", "as a child は過去のことなので、過去の事実に反する仮定は過去完了形にする。"), ("has learned", "現在完了は事実に反する仮定を表せない。"),
      ("would learn", "if 節には would を使わない。")]),
]


@gen("standard_practice", 5, ["condition_check", "concept"])
def mixed(r):
    s, ok, jp, cue, wrongs = r.choice(MIXED)
    return mc(f"日本語の意味になるように、（　）に入る最も適切なものを選びなさい。\n{jp}\n{s}", [ok] + [w for w, _ in wrongs],
              f"{ok} が入る。if 節と主節で事実の時が異なる混合仮定法。手がかりは {cue}。", d=3,
              ap="if 節と主節のそれぞれについて、時を表す語句（now / yesterday / last year など）から「現在の事実に反する」か「過去の事実に反する」かを別々に判断する。",
              steps=["if 節の時と主節の時を、時を表す語句から判断する。", "現在の事実に反する部分は過去形・would＋原形、過去の事実に反する部分は過去完了形・would have＋過去分詞。", f"（　）に合う形は {ok}。"],
              alt=["事実の文を2つ（過去の事実と現在の事実）に分けて書き、それぞれを1つずつ過去にずらして確かめる。"],
              pc=[("if 節と主節の時を区別している", 2), ("正しい形を選んでいる", 2)],
              pit=["if 節が過去完了なら主節も必ず would have＋過去分詞になると思い込む。"], why={w: (reason, "混合仮定法の時の判断の誤り") for w, reason in wrongs})


FACTS = [
    ("As I don't have a car, I can't drive you home.", "If I had a car, I could drive you home.", "現在の事実に反する → 仮定法過去", []),
    ("As it is raining, we can't go on a picnic.", "If it were not raining, we could go on a picnic.", "現在の事実に反する → 仮定法過去", []),
    ("I am not rich, so I can't buy that house.", "If I were rich, I could buy that house.", "現在の事実に反する → 仮定法過去", []),
    ("As we didn't know her address, we didn't write to her.", "If we had known her address, we would have written to her.", "過去の事実に反する → 仮定法過去完了", []),
    ("I didn't have enough money, so I didn't buy the camera.", "If I had had enough money, I would have bought the camera.", "過去の事実に反する → 仮定法過去完了", []),
    ("She didn't take a taxi, so she is not here yet.", "If she had taken a taxi, she would be here now.", "if 節は過去・主節は現在の事実に反する → 混合仮定法", ["If she had taken a taxi, she would be here already."]),
    ("He didn't study abroad, so he can't speak English well now.", "If he had studied abroad, he could speak English well now.", "if 節は過去・主節は現在の事実に反する → 混合仮定法", []),
    ("As you are not careful, you make many mistakes.", "If you were careful, you would not make many mistakes.", "現在の事実に反する → 仮定法過去", ["If you were careful, you would not make so many mistakes."]),
    ("I'm sorry I can't go with you.", "I wish I could go with you.", "現在の事実に反する願望 → I wish＋仮定法過去", []),
    ("I'm sorry I didn't listen to my teacher.", "I wish I had listened to my teacher.", "過去の事実に反する願望 → I wish＋仮定法過去完了", []),
    ("In fact, he is not a doctor, but he talks like one.", "He talks as if he were a doctor.", "主節と同じ時の事実に反する様子 → as if＋仮定法過去", []),
    ("As the bridge was closed, we had to take a long way around.", "If the bridge had not been closed, we would not have had to take a long way around.", "過去の事実に反する → 仮定法過去完了", []),
]


@gen("standard_practice", 5, ["computation", "application"])
def rewrite_fact(r):
    s, ans, kind, v = r.choice(FACTS)
    head = " ".join(ans.split()[:2])
    return sa(f"次の英文とほぼ同じ内容を、事実に反する仮定を表す文で書きかえなさい。書き出しは「{head}」とすること。\n{s}", ans,
              f"{kind}。事実の肯定・否定を逆にし、時制を1つ過去にずらす。", d=3, **({"v": v} if v else {}),
              ap="事実の文が現在のことか過去のことかを確認し、肯定・否定を逆にしてから、時制を1つ過去にずらす。",
              steps=[f"事実の時を判断する：{kind}。", "事実の肯定・否定を逆にした内容を考える。", "時制を1つ過去にずらして仮定法の形にする。", f"完成文：{ans}"],
              alt=["書きかえた文を事実の文に戻し（時制を1つ現在に近づけ、肯定・否定を逆にする）、元の文と一致するかを確かめる。"],
              pc=[("仮定法の形（時制）が正しい", 2), ("肯定・否定の入れかえが正しい", 2)],
              pit=["事実の文の否定をそのまま残す。", "過去の事実なのに仮定法過去を使う。"])


INV = [
    ("If I were in your position, I would take the job.", "Were I in your position, I would take the job."),
    ("If we had left earlier, we would have caught the last train.", "Had we left earlier, we would have caught the last train."),
    ("If it should rain tomorrow, the event will be canceled.", "Should it rain tomorrow, the event will be canceled."),
    ("If she had not helped me, I could not have finished the report.", "Had she not helped me, I could not have finished the report."),
    ("If it were not for your support, I could not continue.", "Were it not for your support, I could not continue."),
    ("If it had not been for the map, we would have gotten lost.", "Had it not been for the map, we would have gotten lost."),
    ("If you should need any help, please call me.", "Should you need any help, please call me."),
    ("If he were here, he would be glad to see you.", "Were he here, he would be glad to see you."),
    ("If I had had more time, I would have visited the museum.", "Had I had more time, I would have visited the museum."),
    ("If the train had arrived on time, we would not have missed the meeting.", "Had the train arrived on time, we would not have missed the meeting."),
]


@gen("standard_practice", 5, ["computation", "condition_check"])
def inversion(r):
    s, ans = r.choice(INV)
    first = ans.split()[0]
    return sa(f"次の英文を、if を使わずにほぼ同じ意味の文に書きかえなさい。\n{s}", ans,
              f"if を省略すると、were / had / should が主語の前に出る倒置が起こる。ここでは {first} を文頭に出す。", d=3,
              ap="if 節の中の were / had / should を探し、if を消してその語を主語の前に出す。否定の not は主語の後ろに残る。",
              steps=["if 節の動詞が were / had / should のどれかを確認する。", f"if を消し、{first} を主語の前に出す。", "否定の not がある場合は、主語の後ろに残す（Had she not ～）。", f"完成文：{ans}"],
              alt=["書きかえた文の文頭に if を戻して語順を元に戻し、元の文と一致するかを確かめる。"],
              pc=[("倒置の語順が正しい", 3), ("not などの位置が正しい", 1)],
              pit=["Hadn't she helped me のように not を縮めて前に出す（書き言葉ではふつう Had she not ～）。", "were / had / should 以外の動詞（did など）を前に出す。"])


MEAN = [
    ("I wish I had a brother.", "兄弟がいればいいのに（実際にはいない）。",
     [("兄弟がいたらよかったのに（当時はいなかった）。", "過去の事実に反する願望なら I wish I had had a brother. となる。had は仮定法過去で、現在の事実に反する願望。"),
      ("兄弟がいてよかった。", "I wish は事実に反する願望を表すので、兄弟は実際にはいない。"),
      ("兄弟が欲しいと思っていたが、実際にはいた。", "I wish I had … は現在の事実に反する願望で、実際にいるという意味にはならない。")]),
    ("I wish I had had a brother.", "兄弟がいたらよかったのに（実際にはいなかった）。",
     [("兄弟がいればいいのに（今いない）。", "had had は仮定法過去完了で、過去の事実に反する願望を表す。今のことなら I wish I had a brother. となる。"),
      ("兄弟がいてよかった。", "I wish は事実に反する願望を表すので、兄弟は実際にはいなかった。"),
      ("兄弟がいたことを覚えている。", "I wish に「覚えている」という意味はない。")]),
    ("He talks as if he were rich.", "彼はまるで金持ちであるかのように話す。",
     [("彼はまるで以前金持ちだったかのように話す。", "主節より前のことなら as if he had been rich となる。were は主節と同じ時を表す。"),
      ("彼は金持ちなので、そのように話す。", "as if＋仮定法は事実に反する様子のたとえで、実際に金持ちだという意味ではない。"),
      ("彼は金持ちになったら話すつもりだ。", "as if に「～したら」という条件の意味はない。")]),
    ("He talks as if he had been rich.", "彼はまるで以前金持ちだったかのように話す。",
     [("彼はまるで今金持ちであるかのように話す。", "主節と同じ時のことなら as if he were rich となる。had been は主節より前の時を表す。"),
      ("彼は以前金持ちだったので、そのように話す。", "as if＋仮定法は事実に反する様子のたとえで、実際に金持ちだったという意味ではない。"),
      ("彼は金持ちになれたかもしれないと話す。", "as if に「～かもしれない」という意味はない。")]),
    ("It's time you went to bed.", "もう寝る時間ですよ（まだ寝ていない相手を促している）。",
     [("あなたはもう寝てしまった。", "It's time＋過去形は仮定法で、まだしていないことを促す表現。実際に寝たわけではない。"),
      ("あなたが寝たのはちょうどよい時間だった。", "went は仮定法過去で、過去の出来事を表していない。"),
      ("あなたはいつ寝たのですか。", "疑問文ではない。It's time ～ は「～してもいいころだ」の意味。")]),
    ("If it were to snow tomorrow, the trip would be canceled.", "万一明日雪が降るようなことがあれば、旅行は中止になるだろう。",
     [("明日は雪が降るので、旅行は中止になった。", "were to は実現の可能性が低い未来の仮定で、雪が降ると決まっているわけではない。"),
      ("昨日雪が降っていたら、旅行は中止になっていただろう。", "tomorrow があり、未来についての仮定である。"),
      ("明日雪が降ることになっているので、旅行を中止する予定だ。", "were to を予定の be to と取り違えている。仮定法の were to は実現の可能性が低い仮定。")]),
    ("Without your help, I could not have finished it.", "あなたの助けがなかったら、それを終えられなかっただろう（実際には助けがあり、終えられた）。",
     [("あなたの助けがないので、それを終えられない。", "could not have finished は過去の事実に反する結果。実際には助けがあり、終えられた。"),
      ("あなたの助けなしで、私はそれを終えた。", "without ～ は仮定の条件で、「助けなしで終えた」という事実を述べているのではない。"),
      ("あなたの助けがなかったので、それを終えられなかった。", "仮定法なので、実際には助けがあり、終えられたことを表している。")]),
    ("If I had taken the job, I would be living in Osaka now.", "その仕事を引き受けていたら、今ごろ大阪に住んでいるだろう。",
     [("その仕事を引き受けたので、今大阪に住んでいる。", "仮定法なので、実際には仕事を引き受けておらず、大阪に住んでいない。"),
      ("その仕事を引き受けていたら、当時大阪に住んでいただろう。", "主節は would be living … now で、現在の事実に反する結果を表す。"),
      ("その仕事を引き受ければ、大阪に住むことになるだろう。", "if 節は had taken（過去完了）で、過去の事実に反する仮定。これからのことではない。")]),
    ("If only I had listened to her!", "彼女の言うことを聞いてさえいたらなあ。",
     [("彼女の言うことを聞いていてよかった。", "If only＋仮定法過去完了は過去の事実に反する強い願望で、実際には聞かなかった。"),
      ("彼女の言うことだけを聞いた。", "only は「～だけ」ではなく、If only で「～でさえあればなあ」という願望を表す。"),
      ("彼女の言うことを聞けばいいのに（今聞いていない）。", "had listened は過去の事実に反する願望。今のことなら If only I listened to her! となる。")]),
    ("To hear him speak English, you would take him for a native speaker.", "彼が英語を話すのを聞けば、ネイティブスピーカーだと思うだろう。",
     [("彼はネイティブスピーカーなので、英語を話すのを聞くとよい。", "不定詞 To hear … が「聞けば」という仮定の条件を表している。彼がネイティブだとは述べていない。"),
      ("彼が英語を話すのを聞くために、ネイティブスピーカーを連れていくだろう。", "To hear は目的ではなく条件を表す。take A for B は「A を B だと思う」。"),
      ("彼が英語を話すのを聞いたので、ネイティブスピーカーだとわかった。", "would take は仮定の結果で、実際に聞いた・わかったという事実を述べていない。")]),
]


@gen("standard_practice", 5, ["concept", "common_error"])
def meaning(r):
    s, ok, wrongs = r.choice(MEAN)
    return mc(f"次の英文の意味として最も適切なものを選びなさい。\n{s}", [ok] + [w for w, _ in wrongs],
              f"「{ok}」が正しい。仮定法の文では、動詞の時制から「いつの事実に反するのか」を読み取る。", d=3,
              ap="動詞の形（過去形か過去完了形か、would＋原形か would have＋過去分詞か）から、どの時の事実に反する内容かを判断して訳す。",
              steps=["仮定法が使われている部分を見つける。", "動詞の形から、現在の事実に反するのか過去の事実に反するのかを判断する。", f"その時に合う和訳「{ok}」を選ぶ。"],
              alt=["英文を事実の文に書きかえて（肯定・否定を逆にし、時制を1つ現在に近づけて）、選んだ和訳と内容が合うかを確かめる。"],
              pc=[("仮定法であることに気づいている", 2), ("時の判断に基づいて正しい和訳を選んでいる", 2)],
              pit=["仮定法の過去形を、過去の出来事として訳してしまう。"], why={w: (reason, "仮定法の時の読み取りの誤り") for w, reason in wrongs})


# ======================================================================
# C 思考力・記述応用
# ======================================================================

PAIRS = [
    ("If it rains tomorrow, I will stay home.", "If it were to rain tomorrow, I would stay home.",
     "Aは直説法で、明日雨が降ることを実際に起こり得る条件として述べている（「明日雨が降れば家にいる」）。Bは were to を使った仮定法で、話し手は雨が降る可能性は低いと考えている（「万一明日雨が降るようなことがあれば家にいるだろう」）。"),
    ("I wish I knew his name.", "I wish I had known his name.",
     "Aは仮定法過去で、現在の事実に反する願望（「今、彼の名前を知っていればいいのに」＝今知らない）。Bは仮定法過去完了で、過去の事実に反する願望（「あのとき彼の名前を知っていればよかったのに」＝当時知らなかった）。"),
    ("He talks as if he knew everything.", "He talked as if he knew everything.",
     "as if 節の knew はどちらも「主節と同じ時」の事実に反する内容を表す。Aは「彼はまるで何でも知っているかのように話す」、Bは「彼はまるで何でも知っているかのように話した」。主節の時制が変わっても、主節と同じ時なら as if 節は過去形のままでよい。"),
    ("If I had studied harder, I would have passed the exam.", "If I had studied harder, I would be a doctor now.",
     "if 節はどちらも過去の事実に反する仮定（もっと勉強しなかった）。Aは主節も過去の事実に反する（「試験に合格していただろう」）ので仮定法過去完了。Bは now があり主節が現在の事実に反する（「今ごろ医者になっているだろう」）ので混合仮定法。"),
    ("I hope he comes to the party.", "I wish he would come to the party.",
     "Aの hope は実現の可能性があると考えている願望で、直説法を使う（「彼がパーティーに来てくれるといいな」）。Bの wish＋would は実現しそうにないと話し手が考えている願望で、仮定法を使う（「彼がパーティーに来てくれたらいいのに（来そうにない）」）。"),
    ("If he is at home, he will answer the phone.", "If he were at home, he would answer the phone.",
     "Aは直説法で、彼が家にいるかどうかわからないが、いれば電話に出るという実際の条件を述べている。Bは仮定法過去で、彼は実際には家にいないという前提で「家にいれば電話に出るのに」と述べている。"),
    ("Without water, we could not live.", "Without water, we could not have survived the trip.",
     "どちらも without ～ が「～がなければ（なかったら）」という仮定の条件を表す。Aは主節が could＋原形なので現在の事実に反する仮定（「水がなければ生きられないだろう」）。Bは could have＋過去分詞なので過去の事実に反する仮定（「水がなかったら旅を生きのびられなかっただろう」）。"),
    ("She speaks as if she were my mother.", "She speaks as if she had been there.",
     "Aの as if＋過去形は主節と同じ時の事実に反する内容（「まるで私の母親であるかのように話す」）。Bの as if＋過去完了は主節より前の事実に反する内容（「まるで（その時）そこにいたかのように話す」）。"),
]


@gen("thinking_writing", 4, ["written_reasoning", "concept"])
def explain_pair(r):
    a, b, model = r.choice(PAIRS)
    return desc(f"次の2つの英文A・Bの意味の違いを、動詞の形（時制・直説法か仮定法か）に触れながら日本語で説明しなさい。\nA：{a}\nB：{b}", model,
                "仮定法では、動詞の形が「事実に反するかどうか」と「いつの事実か」を同時に示している。形の違いを根拠にして意味を説明する。",
                [("Aの形と意味を正しく説明している", 3), ("Bの形と意味を正しく説明している", 3), ("2つの違いを明確に述べている", 2)], d=4, p=8, lines=6,
                ap="A・B で動詞の形が違う部分を見つけ、それぞれが直説法か仮定法か、仮定法ならいつの事実に反するのかを判断する。",
                steps=["A・B で動詞の形が違う部分を見つける。", "それぞれの形が表す意味（事実か仮定か、どの時か）を確認する。", "和訳を示し、違いをまとめる。"],
                alt=["それぞれの文を事実の文に書きかえて（例：I don't know his name. ／ I didn't know his name.）、違いを示す。"],
                pc=[("Aの説明", 3), ("Bの説明", 3), ("違いのまとめ", 2)],
                pit=["和訳だけを並べ、どの形が意味の違いを生んでいるかを説明しない。"])


COMPOSE = [
    ("もし私が鳥なら、あなたのところへ飛んでいけるのに。", "If I were a bird, I could fly to you.", "現在の事実に反する仮定なので仮定法過去。「できる」は can の過去形 could で表す。"),
    ("あのときもっと注意していれば、事故は起きなかったかもしれない。", "If I had been more careful then, the accident might not have happened.", "過去の事実に反する仮定なので仮定法過去完了。「かもしれない」は may の過去形 might＋have＋過去分詞で表す。"),
    ("昨夜雪が降らなかったら、今日学校に行けるのに。", "If it had not snowed last night, I could go to school today.", "if 節は過去（昨夜）の事実、主節は現在（今日）の事実に反するので混合仮定法。"),
    ("もう少しお金があれば、そのコンピューターが買えるのに。", "If I had a little more money, I could buy the computer.", "現在の事実に反する仮定なので仮定法過去。「買える」は could＋原形。"),
    ("彼の助けがなかったら、私はその試合に勝てなかっただろう。", "Without his help, I could not have won the game.", "過去の事実に反する仮定。without ～ で条件を表し、主節を could not have＋過去分詞にする（If it had not been for his help, … も可）。"),
    ("あの便に乗っていたら、今ごろ札幌にいるだろう。", "If I had taken that flight, I would be in Sapporo now.", "if 節は過去、主節は現在（今ごろ）の事実に反するので混合仮定法。"),
    ("時間を戻せたらいいのに。", "I wish I could turn back time.", "現在の事実（戻せない）に反する願望なので I wish＋仮定法過去。can を could にする。"),
    ("彼はまるで何も起こらなかったかのようにふるまった。", "He behaved as if nothing had happened.", "ふるまった時より前の出来事に反する様子なので as if＋仮定法過去完了。"),
]


@gen("thinking_writing", 3, ["cross_unit", "written_reasoning"], rel=["HS-ENG-U03", "HS-ENG-U02"])
def compose(r):
    jp, ans, why = r.choice(COMPOSE)
    return desc(f"次の日本語を英語に直しなさい。また、動詞と助動詞の形を選んだ理由を、事実の時と助動詞の意味に触れて説明しなさい。\n{jp}",
                f"{ans}　（理由：{why}）", f"仮定法の形は、事実の時（現在か過去か）と、助動詞の意味（would＝だろう、could＝できる、might＝かもしれない）の2つで決まる。{why}",
                [("英文が正しい", 4), ("事実の時に基づいて時制を説明している", 2), ("助動詞の選択を説明している", 2)], d=4, p=8, lines=6,
                ap="まず事実の文を考え（例：私は鳥ではない）、事実の時を決める。次に日本語の「～だろう」「～できる」「～かもしれない」から助動詞を選ぶ。",
                steps=["事実の文を考え、事実の時（現在・過去）を決める。", "時制を1つ過去にずらした形を決める。", "日本語の意味に合う助動詞（would / could / might）を選ぶ。", f"完成文：{ans}"],
                alt=["完成した英文を事実の文に戻し、日本語の状況と一致するかを確かめる。"],
                pc=[("英文", 4), ("時制の理由", 2), ("助動詞の理由", 2)],
                pit=["「～できるのに」を would で表し、could を使わない。", "混合仮定法の主節まで過去完了にしてしまう。"])


ADVICE = [
    ("友達が「数学のテストの点が悪くて落ちこんでいる」と相談してきた。", "If I were you, I would ask the teacher for help after class.", "I would appreciate it if you could explain this problem to me again."),
    ("友達が「部活と勉強の両立ができない」と悩んでいる。", "If I were you, I would make a weekly schedule and stick to it.", "It would be better if you talked to your coach about it."),
    ("友達が「スマートフォンを使いすぎて夜眠れない」と言っている。", "If I were you, I would leave my phone in another room at night.", "It would help if you turned off your phone an hour before bed."),
    ("留学生が「日本語の会話がなかなか上達しない」と言っている。", "If I were you, I would join a club and talk with Japanese students every day.", "It might help if you watched Japanese TV programs with subtitles."),
    ("友達が「けんかした相手と仲直りしたいが、どうしたらいいかわからない」と言っている。", "If I were you, I would write her a short letter to say sorry.", "It would be a good idea if you talked to her face to face."),
    ("友達が「朝起きられず、よく遅刻する」と悩んでいる。", "If I were you, I would go to bed an hour earlier.", "It would help if you put your alarm clock away from your bed."),
    ("友達が「英単語がなかなか覚えられない」と言っている。", "If I were you, I would review the words for ten minutes every morning.", "It might be useful if you made sentences with the new words."),
    ("友達が「文化祭の出し物のアイデアが浮かばない」と困っている。", "If I were you, I would ask the classmates what they want to do.", "It would be fun if your class made a short movie."),
]


@gen("thinking_writing", 3, ["cross_unit", "application", "written_reasoning"], rel=["HS-ENG-U10"])
def advice(r):
    sit, m1, m2 = r.choice(ADVICE)
    return desc(f"次の場面で、相手に助言する英文を、仮定法を使って1文書きなさい。また、仮定法を使うと、直接「～しなさい」と言う場合と比べて、どのような効果があるかを日本語で説明しなさい。\n［場面］{sit}",
                f"（例）{m1}　（別解例：{m2}）　効果：「もし私があなたなら」と現実ではない立場から述べることで、命令ではなく提案として伝わり、相手に判断を任せる控えめで丁寧な言い方になる。",
                "If I were you, I would ～ は「私があなたの立場なら～する」という現実に反する仮定を使った助言の定型表現。仮定法の過去形は現実との距離を表すため、命令や断定を和らげ、丁寧で控えめな印象を与える。",
                [("仮定法の形が正しい（were / would＋原形 など）", 3), ("場面に合った内容の助言になっている", 2), ("仮定法による丁寧さ・控えめさの効果を説明している", 3)], d=4, p=8, lines=6,
                ap="If I were you, I would ～ の型を使う。仮定法の過去形が「現実との距離」を表すことと、言い方の丁寧さとを結びつけて説明する。",
                steps=["場面から、助言の内容を日本語で決める。", "If I were you, I would＋原形 ～. の型に当てはめる。", "命令文（Ask the teacher.）と比べて、相手が受ける印象の違いを説明する。"],
                alt=["It would be better if you ～（過去形）／ It might help if you ～ のように、主節に would / might を使う形でも控えめな助言になる。"],
                pc=[("仮定法の形", 3), ("場面との適合", 2), ("効果の説明", 3)],
                pit=["If I am you, I will ～ と直説法で書く。", "would の後ろを過去形にする（I would asked）。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(task, wrong, step, etype, tempt, fix, expl, steps, ap, alt, pit):
    return desc(f"{task}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい英文に書き直しなさい。", fix, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい英文に直している", 3), ("仮定法の規則を説明している", 1)], d=3, p=6, lines=5,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい英文", 3), ("規則の説明", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix))


TENSE_ERR = [
    ("雨が降っていなければ、散歩に行くのに。", "If it is not raining, I would go for a walk.", "If it were not raining, I would go for a walk.", "is not raining", "formula",
     "現在の事実に反する仮定なので、if 節は仮定法過去（were）にする。", "「今」の話なので現在形を使えばよいと考えた。"),
    ("もっと時間があれば、もっと本を読むのに。", "If I would have more time, I would read more books.", "If I had more time, I would read more books.", "would have", "formula",
     "if 節には would を使わない。現在の事実に反する仮定は過去形 had で表す。", "日本語の「～あれば…だろう」の推量の感じを if 節にも入れてしまった。"),
    ("彼の住所を知っていたら、手紙を書いたのに。", "If I had known his address, I would write to him.", "If I had known his address, I would have written to him.", "would write", "formula",
     "過去の事実に反する結果なので、主節は would have＋過去分詞にする。", "if 節だけを過去完了にして、主節の形を変えるのを忘れた。"),
    ("彼女がもっと早く出発していたら、今ごろここに着いているだろうに。", "If she had left earlier, she would have been here now.", "If she had left earlier, she would be here now.", "would have been", "condition",
     "now があるので主節は現在の事実に反する内容。混合仮定法で would＋原形にする。", "if 節が過去完了なので、主節も過去完了の形にそろえるものと思い込んだ。"),
    ("昨年もっと一生懸命勉強していたら、合格していただろう。", "If he studied harder last year, he would have passed.", "If he had studied harder last year, he would have passed.", "studied", "formula",
     "last year の事実に反する仮定なので、if 節は過去完了 had studied にする。", "last year があるので過去形でよいと考えた。"),
    ("あのとき答えを知っていたら、教えてあげたのに。", "If I knew the answer then, I would have told you.", "If I had known the answer then, I would have told you.", "knew", "formula",
     "then（あのとき）の事実に反する仮定なので、if 節は過去完了 had known にする。", "過去形の knew で過去の仮定が表せると考えた。"),
    ("万一明日雨が降ったら、家にいるだろう。", "If it will rain tomorrow, we would stay home.", "If it were to rain tomorrow, we would stay home.", "will rain", "formula",
     "if 節には will を使わない。可能性の低い未来の仮定は were to（または should）で表す（現実的な条件なら If it rains tomorrow, we will stay home.）。", "「明日」の話なので will が必要だと考えた。"),
    ("車があれば、駅まで送ってあげられるのに。", "If I had a car, I can take you to the station.", "If I had a car, I could take you to the station.", "can", "formula",
     "仮定法の主節には助動詞の過去形を使うので、can を could にする。", "if 節だけ過去形にすれば仮定法になると考えた。"),
    ("タクシーに乗っていたら、映画の始まりに遅れなかったのに。", "If we had taken a taxi, we would not miss the beginning of the movie.", "If we had taken a taxi, we would not have missed the beginning of the movie.", "would not miss", "formula",
     "過去の事実に反する結果なので、主節は would not have＋過去分詞にする。", "主節の would があれば仮定法として十分だと考えた。"),
]


@gen("error_correction", 5, ["common_error", "computation"])
def err_tense(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(TENSE_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", etype, tempt, fix, f"{rule}正しくは {fix}",
                    ["if 節と主節のそれぞれについて、事実の時（現在・過去）を判断する。", f"「{where}」の部分を、その時に合う仮定法の形に直す。", f"正しい英文：{fix}"],
                    "仮定法の誤りは、①if 節に will / would がないか、②if 節と主節の時が事実の時と合っているか、③主節に助動詞の過去形があるか、の順に点検する。",
                    ["直した英文を事実の文に戻し、日本語の状況（いつの事実に反するのか）と一致するかを確かめる。"],
                    ["if 節に would / will を入れる。", "if 節と主節の時を確かめずに形をそろえる。"])


WISH_ERR = [
    ("英語を流ちょうに話せたらいいのに。", "I wish I can speak English fluently.", "I wish I could speak English fluently.", "can", "formula",
     "I wish の後ろは仮定法なので、can を過去形 could にする。", "願望の内容が「今」のことなので、現在形の can を使った。"),
    ("中学生のころもっと勉強しておけばよかった。", "I wish I studied harder when I was in junior high school.", "I wish I had studied harder when I was in junior high school.", "studied", "formula",
     "過去の事実に反する願望なので、I wish の後ろは過去完了 had studied にする。", "when I was … があるので過去形でよいと考えた。"),
    ("彼はまるで幽霊を見たかのような顔をしていた。", "He looked as if he has seen a ghost.", "He looked as if he had seen a ghost.", "has seen", "formula",
     "主節（looked）より前の事実に反する様子なので、as if の後ろは過去完了 had seen にする。", "「見たことがある」の意味で現在完了を使った。"),
    ("あなたの助けがなかったら、昨日その仕事を終えられなかっただろう。", "Without your help, I could not finish the work yesterday.", "Without your help, I could not have finished the work yesterday.", "could not finish", "formula",
     "yesterday の事実に反する仮定なので、主節は could not have＋過去分詞にする。", "without があれば仮定法になると考え、主節の時を確かめなかった。"),
    ("水がなければ、私たちは生きられないだろう。", "If it is not for water, we could not live.", "If it were not for water, we could not live.", "is", "formula",
     "現在の事実に反する仮定なので、If it were not for ～ の形にする。", "水は実際に存在するので、現在形で書けると考えた。"),
    ("その知らせを知っていたら、電話したのに。", "Had I knew the news, I would have called you.", "Had I known the news, I would have called you.", "knew", "notation",
     "倒置でも had の後ろは過去分詞 known にする。", "had を文頭に出したことで、後ろの動詞の形への注意がおろそかになった。"),
    ("パーティーに来てくれたらいいのに（来てくれそうにない）。", "I wish you will come to my party.", "I wish you would come to my party.", "will", "concept",
     "I wish の後ろに will は使わない。相手の行動を願う場合は would を使う（来てくれると思っているなら I hope you will come. とする）。", "hope と wish の使い分けを意識せず、hope と同じ形で書いた。"),
    ("もう寝る時間ですよ。", "It's time you go to bed.", "It's time you went to bed.", "go", "formula",
     "It's time の後ろの節は仮定法過去で、動詞は過去形にする（It's time to go to bed. も可）。", "これからすることなので現在形でよいと考えた。"),
    ("私があなたなら、彼女に本当のことを言うだろう。", "If I were you, I will tell her the truth.", "If I were you, I would tell her the truth.", "will", "formula",
     "仮定法の主節には助動詞の過去形を使うので、will を would にする。", "if 節を were にしたことで、仮定法の形が完成したと考えた。"),
]


@gen("error_correction", 5, ["common_error", "condition_check"])
def err_wish(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(WISH_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", etype, tempt, fix, f"{rule}正しくは {fix}",
                    ["使われている表現（I wish / as if / without / 倒置 / It's time）が仮定法を必要とすることを確認する。", f"「{where}」の部分を、事実の時に合う仮定法の形に直す。", f"正しい英文：{fix}"],
                    "I wish・as if・without などがあれば仮定法が必要。主節と同じ時か、前の時かで過去形と過去完了形を使い分ける。",
                    ["直した英文を事実の文（I can't speak … ／ I didn't study … など）に戻して、日本語と一致するかを確かめる。"],
                    ["I wish の後ろに can / will をそのまま使う。", "without の文で主節の時を確かめない。"])


GENERATORS = [past_form, perf_form, wish_asif, without_inversion,
              mixed, rewrite_fact, inversion, meaning,
              explain_pair, compose, advice,
              err_tense, err_wish]
