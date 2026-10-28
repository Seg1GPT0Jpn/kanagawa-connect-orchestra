"""単元パック：英語コミュニケーションⅠ 助動詞（推量の助動詞、助動詞＋have＋過去分詞、need / used to）。"""
import random

from banks._common import desc, mc, order, sa
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem,
                         tp)

UNIT_ID = "HS-ENG-U03"


def local(key):
    """問題文から決まる乱数（同じ問題文なら同じ選択肢になるようにする）。"""
    return random.Random(key)


# ======================================================================
# 授業プリント
# ======================================================================

LESSON = lesson(
    goals=["must / should / may / can't などの推量の助動詞を、話し手の確信の度合いと根拠に合わせて使い分けられる。",
           "助動詞＋have＋過去分詞で、過去のことについての推量や、後悔・非難を表せる。",
           "need（助動詞・一般動詞）、used to / would / be used to ～ing、had better の形と意味を区別できる。"],
    duration=50,
    readiness=["can / will / may / must / should の基本の意味を知っている（中学1〜3年）。", "must と have to の違い、must not と don't have to の違いを説明できる（中学2年）。",
               "動詞の過去分詞を正しく作れる（現在完了・受け身で学習済み）。"],
    flow=[("導入：話し手の気持ちを表す助動詞", 5, "He is busy. と He must be busy. を比べ、助動詞が「話し手の判断」を加えることに気づかせる"),
          ("推量の助動詞と確信の度合い", 12, "must → should → may / might → can't の確信度の目盛りを板書し、根拠との対応を確認する（例題1）"),
          ("助動詞＋have＋過去分詞", 15, "なぜ have＋過去分詞を使うのかを導出し、推量と後悔・非難の2系統に整理する（例題2）"),
          ("need・used to・had better", 12, "形と意味を対比表で整理する（例題3）"),
          ("まとめと確認", 6, "確認問題3問、問題プリントA の課題指示")],
    sections=[
        intro("in1", "助動詞は「話し手の判断」を表す",
              "He is busy. は「彼は忙しい」という事実を述べる文である。これに must を加えた He must be busy. は「彼は忙しいにちがいない」となり、事実そのものではなく、話し手が根拠にもとづいて下した判断を表す。助動詞は、動詞が表す内容に「話し手がどれくらい確信しているか」「どうすべきだと考えているか」という気持ちを加える語である。",
              bullets=["義務・許可などを表す用法：You must go.（行かなければならない）／ You may go.（行ってもよい）",
                       "推量を表す用法：He must be busy.（忙しいにちがいない）／ He may be busy.（忙しいかもしれない）",
                       "同じ助動詞が2つの用法をもつので、文脈と後ろの動詞（be 動詞・状態動詞が多いか）から判断する。"],
              points=[tp("2つの文を板書し、それぞれ「だれの考えか」を問う。", ask="He must be busy. は、彼が忙しいという事実を述べているか。",
                         expect="事実ではなく、話し手がそう思っている（判断している）。", timing="導入の冒頭"),
                      tp("推量の must は be 動詞や状態動詞と結びつくことが多い、という手がかりを示す。")]),
        definition("df1", "推量の助動詞と確信の度合い",
                   "推量の助動詞は、話し手の確信の強さによって使い分ける。確信が強い順におおよそ次のようになる。",
                   formula="must（～にちがいない） ＞ will / would（～だろう） ＞ should / ought to（～のはずだ） ＞ may / might / could（～かもしれない） ／ 否定の確信：can't / cannot（～のはずがない）",
                   bullets=["must は「根拠があって、そうとしか考えられない」ときに使う。", "can't は must の反対で「そうであるはずがない」。推量の must の否定には can't を使う。",
                            "may / might / could は、ほかの可能性もある「～かもしれない」。might は may よりやや確信が弱いとされる。"],
                   conditions=["推量の must は、根拠となる事実（文脈）があることが前提である。", "must not は「～してはならない」（禁止）の意味で使うのがふつうで、「～のはずがない」には can't を使う。"],
                   points=[tp("確信度を「目盛り」として板書し、根拠の強さと対応させる。", caution="must の否定を must not とする誤り（推量の否定は can't）が多い。")]),
        theorem("th1", "助動詞＋have＋過去分詞",
                "must have＋過去分詞（～したにちがいない） ／ can't have＋過去分詞（～したはずがない） ／ may (might) have＋過去分詞（～したかもしれない） ／ should (ought to) have＋過去分詞（～すべきだったのに） ／ needn't have＋過去分詞（～する必要はなかったのに）",
                ["must / can't / may / might / could have＋過去分詞は、現在の時点から過去のことを推量する。",
                 "should / ought to have＋過去分詞は、過去にしなかったことへの後悔・非難（～すべきだったのに）を表す。",
                 "needn't have＋過去分詞は、「実際にはしたが、その必要はなかった」ことを表す。didn't need to＋原形は「する必要がなかった」で、実際にしたかどうかは文脈による。",
                 "could have＋過去分詞は「～できただろうに（実際はしなかった）」や「～したかもしれない」を表す。"],
                body="推量なのか後悔・非難なのかは助動詞の種類で決まる。must have は推量、should have は後悔・非難であり、和訳の語尾（～にちがいない／～すべきだったのに）を混同しないことが大切である。",
                points=[tp("推量系（must / can't / may have）と後悔系（should / needn't have）の2つの箱に分けて板書する。",
                           ask="You must have been tired. と You should have been careful. の違いは何か。", expect="前者は過去の推量、後者は過去の行動への非難・後悔。")]),
        derivation("dv1", "なぜ「助動詞＋have＋過去分詞」で過去を表すのか",
                   ["① 助動詞の後ろには動詞の原形しか置けない。したがって He must was busy. や He must forgot. は誤りである。",
                    "② しかし、過去のことについて「今」推量したい場面がある（例：道がぬれている → 昨夜雨が降ったにちがいない）。",
                    "③ 助動詞そのものを過去形にすると、意味が変わったり（must に過去形はない）、別の用法（could は能力の過去など）と区別できなくなったりする。",
                    "④ そこで、原形でありながら「それ以前のこと」を表せる完了形の原形 have＋過去分詞を助動詞の後ろに置く。",
                    "⑤ その結果、助動詞（判断の時点＝現在）＋have＋過去分詞（出来事の時点＝過去）という形で、「今の時点から過去を判断する」意味になる。"],
                   body="この「判断は今、出来事は過去」という構造は、完了不定詞（seem to have＋過去分詞）と同じ考え方である。",
                   points=[tp("時間軸に「判断の時点（今）」と「出来事の時点（過去）」を別々に書きこみ、must が今、have＋過去分詞が過去を担当していることを示す。", timing="手順⑤の説明時")]),
        definition("df2", "need・used to・had better の形と意味",
                   "形が似ていて意味の異なる表現は、後ろに続く形（原形・to 不定詞・動名詞）とセットで覚える。",
                   bullets=["助動詞 need：主に否定文・疑問文で使い、後ろは原形（You need not come. ／ Need I come?）。",
                            "一般動詞 need：need to＋原形（You don't need to come.）。肯定文ではふつうこちらを使う。",
                            "used to＋原形：（今はちがうが）以前は～したものだ・以前は～だった（動作にも状態にも使う）。",
                            "would（often）＋原形：（過去に）よく～したものだ（動作のみ。状態には使わない）。",
                            "be used to＋名詞・動名詞：～に慣れている（get used to で「～に慣れる」）。",
                            "had better＋原形：～したほうがよい（しないと困ったことになるという警告を含む）。否定は had better not＋原形。"],
                   conditions=["used to の後ろは原形、be used to の後ろは名詞・動名詞（to は前置詞）。", "be used to＋原形 は「～するために使われる」（use の受け身＋目的の不定詞）で、別の表現である。"],
                   points=[tp("used to / be used to / be used to＋原形 の3つを並べて板書し、to の後ろの形の違いに印をつけさせる。", caution="I'm used to get up early. のように be used to の後ろに原形を置く誤りが多い。")]),
        example("ex1", "例題1　推量の助動詞",
                "（　）に must か can't を入れなさい。(1) She has been working since six this morning. She (　) be tired.　(2) That (　) be Ken. He is in Australia now.",
                ["(1) 朝6時から働いているという根拠から、「疲れているにちがいない」と強く推量できる。", "(2) ケンは今オーストラリアにいるという根拠から、「ケンであるはずがない」と強く否定できる。"],
                "(1) must　(2) can't",
                thinking="2文目以降に書かれた根拠が、肯定の推量を支えるか、否定の推量を支えるかを判断する。",
                points=[tp("根拠の文に下線を引かせ、根拠 → 判断の順で説明させる。")],
                misconceptions=[("(2) に must not を入れる", "must not は「～してはならない」（禁止）。「～のはずがない」は can't")]),
        example("ex2", "例題2　助動詞＋have＋過去分詞",
                "日本語に合うように、（　）内の語を適切な形にして英文を完成させなさい。(1) 彼はバスに乗り遅れたのかもしれない。He may (miss) the bus.　(2) もっと早く出発すべきだったのに。We should (leave) earlier.",
                ["(1) 過去のことについての推量なので may have＋過去分詞。", "(2) 過去にしなかったことへの後悔なので should have＋過去分詞。"],
                "(1) have missed　(2) have left",
                thinking="過去のことについての判断なので、助動詞の後ろを have＋過去分詞にする。",
                points=[tp("(2) を must have left とする誤答を取り上げ、must have は「出発したにちがいない」という推量になることを確認する。")]),
        example("ex3", "例題3　used to と be used to",
                "（　）内から適切なものを選びなさい。(1) There (used to / would) be a big tree in front of the station.　(2) I'm used to (get / getting) up early.",
                ["(1) be（ある・いる）は状態を表すので、would は使えない。過去の状態は used to で表す。", "(2) be used to の to は前置詞なので、後ろは動名詞。"],
                "(1) used to　(2) getting",
                thinking="(1) は後ろの動詞が動作か状態か、(2) は to が不定詞の to か前置詞の to かで判断する。",
                points=[tp("(2) で to の後ろに名詞（I'm used to this work.）が置けることを示し、前置詞の to だと納得させる。")]),
        board("bd1", "板書案",
              [("① 推量の目盛り", ["must ～にちがいない", "should ～のはずだ", "may / might ～かもしれない", "can't ～のはずがない", "× must not（禁止になる）"]),
               ("② 助動詞＋have＋p.p.", ["判断＝今、出来事＝過去", "推量：must / can't / may have p.p.", "後悔：should have p.p.（～すべきだったのに）", "needn't have p.p.（必要なかったのに）"]),
               ("③ 形に注意", ["need not＋原形 ／ don't need to＋原形", "used to＋原形（以前は～）", "would（動作のみ）", "be used to＋～ing（慣れている）", "had better not＋原形"])],
              points=[tp("板書は3列に分け、②では時間軸の図を添える。③は「to の後ろの形」を色分けする。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("推量の問題では、必ず根拠となる文に下線を引かせてから助動詞を選ばせる。", ask="この文の根拠はどこに書かれているか。"),
               tp("助動詞の後ろに過去形を置く誤り（must went）は、「助動詞の後ろは原形」という規則に立ち返らせる。", caution="過去の内容だと意識すると、過去形を置きたくなる。"),
               tp("must have（推量）と should have（後悔）の取り違えは、和訳の語尾で確認させる。", timing="例題2の後"),
               tp("needn't have＋過去分詞は「実際にはした」ことが前提であることを、具体的な場面（傘を持っていったが晴れた）で示す。"),
               tp("問題プリント D の誤答例を使い、used to と be used to、need not と need to の形の混同を確認させる。")],
              misconceptions=[("推量の否定を He must not be at home. とする", "「～のはずがない」は He can't be at home."),
                              ("He must forgot it.", "助動詞の後ろは原形。過去の推量は He must have forgotten it."),
                              ("I'm used to get up early.", "be used to の to は前置詞。I'm used to getting up early.")]),
        summary("sm1", "まとめ",
                ["推量の助動詞は確信の度合いで選ぶ：must ＞ should ＞ may / might。否定の確信は can't。",
                 "過去のことの推量・後悔は助動詞＋have＋過去分詞（判断は今、出来事は過去）。must have は推量、should have は後悔・非難。",
                 "need not＋原形 ／ need to＋原形、used to＋原形 ／ be used to＋～ing、had better not＋原形 の形を区別する。"]),
        check("ck1", "確認問題",
              [("「彼は病気にちがいない。」を英語にしなさい。", "He must be sick (ill)."),
               ("「あなたは私に言うべきだったのに。」を英語にしなさい。", "You should have told me."),
               ("I used to (live / living) in Osaka. の（　）内から正しい方を選びなさい。", "live（used to＋原形で「以前は～だった」）")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

INFER = [
    ("She has been working since early this morning. She (　) be tired.", "must",
     [("can't", "can't は「～のはずがない」。朝早くから働いているという根拠と逆になる。"),
      ("need", "助動詞の need は主に否定文・疑問文で使い、推量の意味はない。"),
      ("had better", "had better は「～したほうがよい」という忠告で、推量ではない。")]),
    ("That (　) be Ken. He is in Australia now.", "can't",
     [("must", "must は「～にちがいない」。ケンは今オーストラリアにいるという根拠と逆になる。"),
      ("should", "should は「～のはずだ」。根拠と逆の判断になる。"),
      ("may", "may は「～かもしれない」。オーストラリアにいるという根拠があるので、ケンである可能性は否定できる。")]),
    ("Take an umbrella with you. It (　) rain this afternoon.", "may",
     [("can't", "can't は「～のはずがない」。雨が降らないなら傘を持っていく理由がなくなる。"),
      ("need", "助動詞の need は肯定文ではふつう使わず、推量の意味もない。"),
      ("used to", "used to は「以前は～したものだ」という過去の習慣で、this afternoon と合わない。")]),
    ("You walked for five hours. You (　) be hungry.", "must",
     [("can't", "can't は「～のはずがない」。5時間歩いたという根拠と逆になる。"),
      ("used to", "used to は過去の習慣・状態を表し、今の推量にはならない。"),
      ("need", "助動詞の need は肯定文ではふつう使わず、推量の意味もない。")]),
    ("He (　) be a doctor. He doesn't know anything about first aid.", "can't",
     [("must", "must は「～にちがいない」。応急手当を何も知らないという根拠と逆になる。"),
      ("should", "should は「～のはずだ」。根拠と逆の判断になる。"),
      ("will", "will は「～だろう」。根拠と逆の判断になる。")]),
    ("The train left Tokyo two hours ago, so it (　) arrive in Nagoya soon.", "should",
     [("can't", "can't は「～のはずがない」。2時間前に出発したという根拠と逆になる。"),
      ("need", "助動詞の need は肯定文ではふつう使わない。"),
      ("used to", "used to は過去の習慣・状態を表し、soon（まもなく）と合わない。")]),
    ("Your answer (　) be right, but let's check it once more just in case.", "may",
     [("used to", "used to は過去の習慣・状態を表し、今の答えについての推量にならない。"),
      ("need", "助動詞の need は肯定文ではふつう使わない。"),
      ("had better", "had better は「～したほうがよい」という忠告で、推量ではない。")]),
    ("There's a light on in her room. She (　) be at home.", "must",
     [("can't", "can't は「～のはずがない」。明かりがついているという根拠と逆になる。"),
      ("need", "助動詞の need は肯定文ではふつう使わない。"),
      ("had better", "had better は「～したほうがよい」という忠告で、推量ではない。")]),
    ("The story (　) be true. Nobody can live for three hundred years.", "can't",
     [("must", "must は「～にちがいない」。だれも300年生きられないという根拠と逆になる。"),
      ("may", "may は「～かもしれない」。根拠からありえないと断定できる。"),
      ("should", "should は「～のはずだ」。根拠と逆の判断になる。")]),
    ("I'm not sure, but the shop (　) be closed today. It's a holiday.", "might",
     [("can't", "can't は「～のはずがない」。I'm not sure（確かではない）と、休日だから閉まっているかもという根拠に合わない。"),
      ("need", "助動詞の need は肯定文ではふつう使わない。"),
      ("used to", "used to は過去の習慣・状態を表し、today と合わない。")]),
]


@gen("basic_check", 5, ["concept", "condition_check"])
def modal_infer(r):
    s, ok, wrongs = r.choice(INFER)
    return mc(f"文脈に合うように、（　）に入る最も適切なものを選びなさい。\n{s}", [ok] + [w for w, _ in wrongs],
              f"{ok} が入る。根拠となる文から、話し手の確信の度合い（肯定か否定か、強いか弱いか）を判断する。", d=1,
              ap="推量の根拠となる文に下線を引き、その根拠が「そうにちがいない」「そうであるはずがない」「そうかもしれない」のどれを支えるかを考える。",
              steps=["根拠となる文を見つける。", "根拠が肯定・否定のどちらの判断を支えるか、確信は強いか弱いかを決める。", f"確信の度合いに合う {ok} を選ぶ。"],
              alt=["選択肢を入れて和訳し、根拠の文とつなげて自然な話の流れになるかを確かめる。"],
              pc=[("根拠となる文を見つけている", 1), ("確信の度合いに合う助動詞を選んでいる", 1)],
              pit=["推量の否定（～のはずがない）に must not を使う。", "had better や used to を推量の意味だと誤解する。"],
              why={w: (reason, "推量の助動詞の意味・用法の混同") for w, reason in wrongs})


HAVE_PP = [
    ("He must have forgotten our appointment.", "彼は約束を忘れたにちがいない。",
     [("彼は約束を忘れなければならなかった。", "must have＋過去分詞は過去の推量（～したにちがいない）で、過去の義務は had to で表す。"),
      ("彼が約束を忘れたはずがない。", "「～したはずがない」は can't have＋過去分詞。"),
      ("彼は約束を忘れるべきだった。", "「～すべきだった」は should have＋過去分詞。")]),
    ("She can't have said such a thing.", "彼女がそんなことを言ったはずがない。",
     [("彼女はそんなことを言えなかった。", "能力の過去「～できなかった」は couldn't＋原形。can't have＋過去分詞は過去についての否定の推量。"),
      ("彼女はそんなことを言ったにちがいない。", "「～したにちがいない」は must have＋過去分詞で、肯定と否定が逆。"),
      ("彼女はそんなことを言うべきではなかった。", "「～すべきではなかった」は shouldn't have＋過去分詞。")]),
    ("Ken may have missed the train.", "ケンは電車に乗り遅れたのかもしれない。",
     [("ケンは電車に乗り遅れてもよかった。", "may の許可の意味で訳している。may have＋過去分詞は過去についての推量。"),
      ("ケンは電車に乗り遅れたにちがいない。", "「～したにちがいない」は must have＋過去分詞で、may have より確信が強い。"),
      ("ケンは電車に乗り遅れるかもしれない。", "may＋原形なら未来・現在の推量だが、have＋過去分詞があるので過去のこと。")]),
    ("You should have told me the truth.", "あなたは私に本当のことを言うべきだったのに。",
     [("あなたは私に本当のことを言ったにちがいない。", "「～したにちがいない」は must have＋過去分詞。should have＋過去分詞は後悔・非難。"),
      ("あなたは私に本当のことを言うべきだ。", "should＋原形なら現在・未来のことだが、have＋過去分詞があるので過去のこと。"),
      ("あなたは私に本当のことを言う必要はなかった。", "「～する必要はなかった」は needn't have＋過去分詞や didn't need to＋原形。")]),
    ("You needn't have brought your lunch.", "あなたはお弁当を持ってくる必要はなかったのに。",
     [("あなたはお弁当を持ってくるべきだったのに。", "「～すべきだったのに」は should have＋過去分詞。"),
      ("あなたはお弁当を持ってきたはずがない。", "「～したはずがない」は can't have＋過去分詞。"),
      ("あなたはお弁当を持ってこなければならなかった。", "「～しなければならなかった」は had to＋原形で、needn't とは意味が逆。")]),
    ("We could have won the game.", "私たちはその試合に勝てただろうに。",
     [("私たちはその試合に勝つことができた。", "「実際に勝てた」なら was able to win などで表す。could have＋過去分詞は「（実際はそうならなかったが）～できただろうに」。"),
      ("私たちはその試合に勝ったにちがいない。", "「～したにちがいない」は must have＋過去分詞。"),
      ("私たちはその試合に勝つべきだった。", "「～すべきだった」は should have＋過去分詞。")]),
    ("It must have rained during the night.", "夜の間に雨が降ったにちがいない。",
     [("夜の間に雨が降らなければならなかった。", "must have＋過去分詞は過去の推量で、過去の義務ではない。"),
      ("夜の間に雨が降ったはずがない。", "「～したはずがない」は can't have＋過去分詞。"),
      ("夜の間に雨が降るにちがいない。", "must＋原形なら現在の推量だが、have＋過去分詞があるので過去のこと。")]),
    ("He might have lost his way.", "彼は道に迷ったのかもしれない。",
     [("彼は道に迷ってもよかった。", "might の許可の意味で訳している。might have＋過去分詞は過去についての推量。"),
      ("彼は道に迷ったはずがない。", "「～したはずがない」は can't have＋過去分詞。"),
      ("彼は道に迷うべきだった。", "「～すべきだった」は should have＋過去分詞で、意味も通らない。")]),
    ("You ought to have studied harder.", "あなたはもっと一生懸命勉強すべきだったのに。",
     [("あなたはもっと一生懸命勉強したにちがいない。", "「～したにちがいない」は must have＋過去分詞。ought to have＋過去分詞は後悔・非難。"),
      ("あなたはもっと一生懸命勉強すべきだ。", "ought to＋原形なら現在・未来のことだが、have＋過去分詞があるので過去のこと。"),
      ("あなたはもっと一生懸命勉強したかもしれない。", "「～したかもしれない」は may have＋過去分詞。")]),
    ("She can't have finished the work so soon.", "彼女がそんなに早く仕事を終えたはずがない。",
     [("彼女はそんなに早く仕事を終えることはできない。", "can't＋原形なら現在の不可能だが、have＋過去分詞があるので過去についての推量。"),
      ("彼女はそんなに早く仕事を終えたにちがいない。", "「～したにちがいない」は must have＋過去分詞で、肯定と否定が逆。"),
      ("彼女はそんなに早く仕事を終えるべきではなかった。", "「～すべきではなかった」は shouldn't have＋過去分詞。")]),
]


@gen("basic_check", 5, ["concept", "computation"])
def have_pp_meaning(r):
    s, ok, wrongs = r.choice(HAVE_PP)
    return mc(f"次の英文の意味として最も適切なものを選びなさい。\n{s}", [ok] + [w for w, _ in wrongs],
              f"「{ok}」が正しい。助動詞＋have＋過去分詞は、今の時点から過去のことを判断する（推量）か、過去にしなかったことを悔やむ・責める（後悔・非難）。", d=2,
              ap="まず have＋過去分詞があることから「過去のこと」と判断し、次に助動詞の種類から推量系（must / can't / may / might / could）か後悔系（should / ought to / needn't）かを決める。",
              steps=["have＋過去分詞に注目し、過去のことについての判断だと確認する。", "助動詞の種類から意味の系統（推量か後悔・非難か）を決める。", f"「{ok}」を選ぶ。"],
              alt=["選択肢の和訳を英語に戻すとどの形になるか（had to、can't have、should have など）を考え、問題文と一致するものを選ぶ。"],
              pc=[("過去のことについての判断だと理解している", 1), ("助動詞の種類に合う意味を選んでいる", 1)],
              pit=["must have＋過去分詞を「～しなければならなかった」と訳す。", "should have＋過去分詞を推量と取り違える。"],
              why={w: (reason, "助動詞＋have＋過去分詞の意味の混同") for w, reason in wrongs})


USED = [
    ("There (　) be a big tree in front of the station.", "used to",
     [("would", "would は過去の反復的な動作に使い、be（ある）のような状態には使わない。"),
      ("was used to", "be used to は「～に慣れている」で、後ろに原形 be は続かない。"),
      ("use to", "肯定文で「以前は～だった」を表す形は used to。")]),
    ("I'm (　) getting up early, so it's not hard for me.", "used to",
     [("use to", "be 動詞の後ろで「～に慣れている」を表す形は be used to。"),
      ("using to", "using to という形の表現はない。"),
      ("used", "「～に慣れている」は be used to＋動名詞で、to が必要。")]),
    ("When I was a child, my father (　) often take me fishing on Sundays.", "would",
     [("was used to", "be used to の後ろは名詞・動名詞で、原形 take は続かない。また意味も「慣れていた」になる。"),
      ("is used to", "is used to は現在の「慣れている」で、when I was a child と合わず、後ろに原形も続かない。"),
      ("uses to", "uses to という形はない。")]),
    ("She (　) live in Osaka, but now she lives in Nagoya.", "used to",
     [("would", "live は状態を表す動詞なので、過去の習慣を表す would は使えない。"),
      ("is used to", "is used to は「～に慣れている」で、後ろに原形は続かない。"),
      ("uses to", "uses to という形はない。")]),
    ("You'll soon get (　) the new school.", "used to",
     [("use to", "「～に慣れる」は get used to＋名詞。use の過去分詞 used が必要。"),
      ("using", "get using という形では「慣れる」の意味にならない。"),
      ("to use", "get to use は「使えるようになる」となり、the new school と意味が合わない。")]),
    ("This knife is (　) to cut bread.", "used",
     [("using", "主語 This knife は「使われる」側なので、受け身の過去分詞 used が必要。"),
      ("use", "be 動詞の後ろに原形 use は置けない。"),
      ("uses", "be 動詞の後ろに三人称単数現在形は置けない。")]),
    ("He isn't (　) speaking in public, so he was very nervous.", "used to",
     [("use to", "be 動詞の後ろで「～に慣れている」を表す形は be used to。"),
      ("using to", "using to という形の表現はない。"),
      ("used", "「～に慣れている」は be used to＋動名詞で、to が必要。")]),
    ("We (　) sit by the fire and talk for hours on winter nights.", "would",
     [("were used to", "be used to の後ろは名詞・動名詞で、原形 sit は続かない。"),
      ("are used to", "be used to の後ろは名詞・動名詞で、原形は続かない。また時制も合わない。"),
      ("use to", "肯定文で過去の習慣を表す形は used to（または would）。")]),
    ("My grandmother has lived in Hokkaido for years, so she is (　) the cold.", "used to",
     [("use to", "be 動詞の後ろで「～に慣れている」を表す形は be used to。"),
      ("using to", "using to という形の表現はない。"),
      ("used for", "be used for は「～のために使われる」で、the cold と意味が合わない。")]),
    ("This old building (　) be a hospital. Now it's a museum.", "used to",
     [("would", "be（～である）は状態なので、過去の習慣を表す would は使えない。"),
      ("is used to", "is used to は「～に慣れている」で、後ろに原形は続かない。"),
      ("was used", "was used は「使われた」で、後ろの to be a hospital と意味が通らない。")]),
]


@gen("basic_check", 5, ["condition_check", "common_error"])
def used_to(r):
    s, ok, wrongs = r.choice(USED)
    return mc(f"（　）に入る最も適切なものを選びなさい。\n{s}", [ok] + [w for w, _ in wrongs],
              f"{ok} が入る。used to＋原形（以前は～）、would＋原形（よく～したものだ：動作のみ）、be used to＋名詞・動名詞（～に慣れている）を、後ろの形と意味で区別する。", d=2,
              ap="空所の後ろが原形か、動名詞・名詞かを確かめる。原形なら used to / would、名詞・動名詞なら be (get) used to。さらに後ろが状態か動作かを見る。",
              steps=["空所の後ろの形（原形か、名詞・動名詞か）を確かめる。", "意味（以前は～だった／よく～した／慣れている）を文脈から判断する。", f"形と意味の両方に合う {ok} を選ぶ。"],
              alt=["to の後ろに名詞（this work など）を置いて意味が通るなら前置詞の to（be used to）、通らないなら不定詞の to（used to）と確かめる。"],
              pc=[("後ろの形を確かめている", 1), ("形と意味に合うものを選んでいる", 1)],
              pit=["be used to の後ろに原形を置く。", "状態を表す動詞に would を使う。"],
              why={w: (reason, "used to / would / be used to の混同") for w, reason in wrongs})


FORM = [
    ("You (　) not park here. It's against the rules.", "must",
     [("need", "need not は「～する必要はない」で、規則違反の禁止にはならない。"),
      ("would", "would not は「～しようとしない」などの意味で、禁止にはならない。"),
      ("used", "used not は「以前は～しなかった」の意味で、文脈に合わない。")]),
    ("You (　) not bring lunch tomorrow. Lunch will be served.", "need",
     [("must", "must not は「～してはならない」という禁止で、「昼食が出る」という理由と合わない。"),
      ("would", "would not は「～しようとしない」などの意味で、文脈に合わない。"),
      ("used", "used not は「以前は～しなかった」の意味で、tomorrow と合わない。")]),
    ("You don't (　) to come if you are busy.", "have",
     [("must", "don't must という形はない。「～する必要はない」は don't have to。"),
      ("should", "don't should という形はない。助動詞の否定は should not。"),
      ("can", "don't can という形はない。助動詞の否定は cannot。")]),
    ("Must I finish this today? — No, you (　).", "needn't",
     [("mustn't", "mustn't は「～してはならない」という禁止で、「しなければならないか」への No の答えにならない。"),
      ("can't", "can't は「～できない・してはならない」で、「その必要はない」という答えにならない。"),
      ("won't", "won't は「～しないだろう」で、義務を尋ねる質問の答えにならない。")]),
    ("You had better (　) late again.", "not be",
     [("be not", "had better の否定は had better not＋原形で、not の位置は原形の前。"),
      ("don't be", "had better の後ろに don't は置けない。"),
      ("not to be", "had better の後ろは原形で、to 不定詞は置けない。")]),
    ("You ought (　) apologize to her.", "to",
     [("for", "ought to＋原形で「～すべきだ」。for は使わない。"),
      ("that", "ought の後ろに that 節は置けない。"),
      ("being", "ought の後ろに動名詞は置けない。")]),
    ("We (　) to leave now, or we'll miss the train.", "have",
     [("must", "must の後ろは原形で、must to という形はない。"),
      ("should", "should の後ろは原形で、should to という形はない。"),
      ("can", "can の後ろは原形で、can to という形はない。")]),
    ("You (　) better take an umbrella.", "had",
     [("have", "「～したほうがよい」は had better で、現在のことでも had を使う。"),
      ("has", "「～したほうがよい」は had better で、主語に関係なく had を使う。"),
      ("would", "would better という形はない。")]),
    ("He will (　) able to walk again soon.", "be",
     [("can", "助動詞を2つ並べて will can とはできない。will be able to を使う。"),
      ("being", "will の後ろは原形で、ing 形は置けない。"),
      ("been", "will の後ろは原形で、過去分詞は置けない。")]),
    ("You (　) to be careful when you cross this street.", "ought",
     [("should", "should の後ろは原形で、should to という形はない。"),
      ("must", "must の後ろは原形で、must to という形はない。"),
      ("had better", "had better の後ろは原形で、to 不定詞は置けない。")]),
    ("She will (　) to finish the report by Friday.", "have",
     [("must", "助動詞を2つ並べて will must とはできない。未来の義務は will have to。"),
      ("ought", "助動詞を2つ並べて will ought to とはできない。"),
      ("should", "助動詞を2つ並べて will should とはできない。")]),
]


@gen("basic_check", 5, ["computation", "condition_check"])
def modal_form(r):
    s, ok, wrongs = r.choice(FORM)
    return mc(f"（　）に入る最も適切なものを選びなさい。\n{s}", [ok] + [w for w, _ in wrongs],
              f"{ok} が入る。助動詞の後ろは原形、助動詞は2つ並べない、have to・ought to・had better（not）の形を正確に使う。", d=1,
              ap="空所の前後の語（not、to、原形など）から、どの形の表現が入るかを決める。助動詞を2つ並べられないことも確認する。",
              steps=["空所の前後の形を確認する。", "意味（禁止・不必要・義務・忠告など）を文脈から決める。", f"形と意味の両方に合う {ok} を選ぶ。"],
              alt=["選択肢を入れた形が、助動詞の文法規則（後ろは原形、2つ並べない、否定の位置）に合うかを1つずつ点検する。"],
              pc=[("形の規則を確認している", 1), ("意味に合うものを選んでいる", 1)],
              pit=["must not（禁止）と need not / don't have to（不必要）を混同する。", "had better の否定を had not better とする。"],
              why={w: (reason, "助動詞の形・意味の混同") for w, reason in wrongs})


# ======================================================================
# B 標準演習
# ======================================================================

REWRITE = [
    ("You don't have to worry about it.", "You (　) not worry about it.", "need", [], "don't have to（～する必要はない）は、助動詞 need を使って need not＋原形で表せる。"),
    ("You should see a doctor.", "You (　) to see a doctor.", "ought", [], "should（～すべきだ）は ought to＋原形で言いかえられる。"),
    ("It is possible that he knows the answer.", "He (　) know the answer.", "may", ["might"], "「～かもしれない」は may（might）。"),
    ("I'm sure that he is sick.", "He (　) be sick.", "must", [], "「きっと～だ（と確信している）」は推量の must。"),
    ("It is impossible that the story is true.", "The story (　) be true.", "can't", ["cannot"], "「～のはずがない」は can't（cannot）。"),
    ("I'm sure that she missed the bus.", "She (　)(　) missed the bus.", "must have", [], "過去のことについての強い確信は must have＋過去分詞。"),
    ("It is impossible that he said so.", "He (　)(　) said so.", "can't have", ["cannot have", "couldn't have"], "過去のことについての「～したはずがない」は can't have＋過去分詞。"),
    ("Perhaps he forgot about it.", "He (　)(　) forgotten about it.", "may have", ["might have"], "過去のことについての「～したかもしれない」は may（might）have＋過去分詞。"),
    ("It is a pity that you didn't tell me.", "You (　)(　) told me.", "should have", ["ought to have"], "過去にしなかったことへの後悔・非難は should have＋過去分詞（空所2つなので ought to have は入らないが意味は同じ）。"),
    ("There was a post office here before, but there isn't one now.", "There (　)(　) be a post office here.", "used to", [], "今はちがう過去の状態は used to＋原形で表す。"),
    ("It wasn't necessary for you to buy it, but you did.", "You (　)(　) bought it.", "needn't have", [], "「実際にはしたが、その必要はなかった」は needn't have＋過去分詞。"),
    ("It would be a good idea for you not to go out tonight.", "You (　)(　)(　) go out tonight.", "had better not", ["ought not to"], "「～しないほうがよい」は had better not＋原形（not の位置に注意）。"),
]


@gen("standard_practice", 5, ["computation", "condition_check"])
def rewrite(r):
    src, frame, ans, v, why = r.choice(REWRITE)
    v = [x for x in v if len(x.split()) == frame.count("(　)")]
    return sa(f"上の英文とほぼ同じ意味になるように、下の英文の（　）に適切な語を1語ずつ入れなさい。\n{src}\n{frame}", ans, why, d=3, v=v,
              ap="元の文の意味（確信の度合い・必要・義務・過去の習慣など）と、それが現在のことか過去のことかを確かめ、空所の数に合う助動詞表現を選ぶ。",
              steps=["元の文が表す話し手の判断（推量・義務・不必要など）を確かめる。", "現在のことか過去のことかを確かめる（過去なら助動詞＋have＋過去分詞）。", f"空所の数に合う形を入れる：{ans}。"],
              alt=["書きかえた文を和訳し、元の文の和訳と同じ内容になっているかを確かめる。"],
              pc=[("話し手の判断の種類を正しく読み取っている", 2), ("空所に正しい語を入れている", 2)],
              pit=["過去のことなのに助動詞＋原形にする。", "had better の否定で not の位置を誤る。"])


CONTEXT = [
    ("The road is wet. It (　) last night.", "must have rained",
     [("can't have rained", "can't have＋過去分詞は「～したはずがない」。道がぬれているという根拠と逆になる。"),
      ("needn't have rained", "needn't have＋過去分詞は「～する必要はなかったのに」で、天気について使うと意味が通らない。"),
      ("must rain", "must＋原形は現在の推量または義務で、last night（過去）と合わない。")]),
    ("I can't find my wallet. I (　) it on the train.", "may have left",
     [("should have left", "should have＋過去分詞は「～すべきだったのに」で、財布を置き忘れるべきだったという意味になり不自然。"),
      ("needn't have left", "needn't have＋過去分詞は「～する必要はなかったのに」で、文脈に合わない。"),
      ("may leave", "may＋原形は現在・未来の推量で、すでに起きたこと（財布が見つからない原因）を表せない。")]),
    ("You (　) me. I would have helped you.", "should have told",
     [("must have told", "must have＋過去分詞は「話したにちがいない」という推量で、「手伝ったのに」と後悔する流れに合わない。"),
      ("needn't have told", "needn't have＋過去分詞は「話す必要はなかったのに」で、後半の内容と逆になる。"),
      ("may tell", "may＋原形は現在・未来のことで、過去の後悔を表せない。")]),
    ("She (　) the news. She looked so surprised when I told her.", "can't have heard",
     [("must have heard", "must have＋過去分詞は「聞いたにちがいない」。私が話したときに驚いていたという根拠と逆になる。"),
      ("needn't have heard", "needn't have＋過去分詞は「聞く必要はなかったのに」で、文脈に合わない。"),
      ("can't hear", "can't＋原形は現在のことで、過去の時点で聞いていたかどうかの推量にならない。")]),
    ("We (　) a taxi. The station was just around the corner.", "needn't have taken",
     [("must have taken", "must have＋過去分詞は「乗ったにちがいない」という推量で、自分たちの行動について根拠と合わない。"),
      ("can't have taken", "can't have＋過去分詞は「乗ったはずがない」という推量で、自分たちの行動の評価にならない。"),
      ("should take", "should＋原形は現在・未来のことで、駅がすぐそこだったという過去の話と合わない。")]),
    ("Ken is late. He (　) the bus.", "may have missed",
     [("needn't have missed", "needn't have＋過去分詞は「乗り遅れる必要はなかったのに」で、文脈に合わない。"),
      ("should have missed", "should have＋過去分詞は「乗り遅れるべきだったのに」となり意味が通らない。"),
      ("may miss", "may＋原形は現在・未来の推量で、すでに遅れている原因（過去のこと）を表せない。")]),
    ("I (　) harder when I was young. Now I regret it.", "should have studied",
     [("must have studied", "must have＋過去分詞は「勉強したにちがいない」という推量で、Now I regret it.（後悔）と合わない。"),
      ("can't have studied", "can't have＋過去分詞は「勉強したはずがない」という推量で、後悔の気持ちを表せない。"),
      ("may have studied", "may have＋過去分詞は「勉強したかもしれない」という推量で、後悔の気持ちを表せない。")]),
    ("You (　) your homework already! You only started ten minutes ago.", "can't have finished",
     [("must have finished", "must have＋過去分詞は「終えたにちがいない」。10分前に始めたばかりという根拠と逆になる。"),
      ("should have finished", "should have＋過去分詞は「終えるべきだったのに」で、驚きの文脈に合わない。"),
      ("needn't have finished", "needn't have＋過去分詞は「終える必要はなかったのに」で、文脈に合わない。")]),
    ("It (　) worse. At least nobody was hurt.", "could have been",
     [("must have been", "must have＋過去分詞は「～だったにちがいない」で、「少なくともけが人はいなかった」と合わない。"),
      ("should have been", "should have＋過去分詞は「～であるべきだったのに」で、意味が通らない。"),
      ("needn't have been", "needn't have＋過去分詞は「～である必要はなかったのに」で、意味が通らない。")]),
    ("He studied very hard every day. He (　) the exam.", "must have passed",
     [("can't have passed", "can't have＋過去分詞は「合格したはずがない」。毎日一生懸命勉強したという根拠と逆になる。"),
      ("needn't have passed", "needn't have＋過去分詞は「合格する必要はなかったのに」で、意味が通らない。"),
      ("must pass", "must＋原形は現在の推量または義務で、過去の試験の結果を表せない。")]),
]


@gen("standard_practice", 5, ["concept", "application"])
def have_pp_context(r):
    s, ok, wrongs = r.choice(CONTEXT)
    return mc(f"文脈に合うように、（　）に入る最も適切なものを選びなさい。\n{s}", [ok] + [w for w, _ in wrongs],
              f"{ok} が入る。過去のことについての判断なので助動詞＋have＋過去分詞を使い、根拠や話の流れから推量（must / can't / may）か後悔・評価（should / needn't / could）かを選ぶ。", d=3,
              ap="空所の出来事が過去のことかを確かめたうえで、前後の文が「推量の根拠」なのか「後悔・評価」なのかを読み取る。",
              steps=["空所の出来事が過去のことか確かめる（過去なら have＋過去分詞）。", "前後の文から、推量か後悔・評価かを判断する。", "推量なら確信の度合い、後悔なら「すべきだった／必要なかった」を決める。", f"{ok} を選ぶ。"],
              alt=["選択肢を入れて和訳し、前後の文とつなげて自然な流れになるかを確かめる。"],
              pc=[("過去のことについての判断だと判断している", 1), ("推量か後悔・評価かを文脈から判断している", 1), ("適切な表現を選んでいる", 2)],
              pit=["must have（推量）と should have（後悔）を取り違える。", "過去のことなのに助動詞＋原形を選ぶ。"],
              why={w: (reason, "助動詞＋have＋過去分詞の使い分けの誤り") for w, reason in wrongs})


ORD = [
    ("彼はその知らせを聞いたにちがいない。", ["he", "must", "have", "heard", "the news"], ".", "must have＋過去分詞（過去の推量）"),
    ("彼女がそんなことを言ったはずがない。", ["she", "can't", "have", "said", "such", "a thing"], ".", "can't have＋過去分詞（過去についての否定の推量）"),
    ("私たちはもっと早く出発すべきだった。", ["we", "should", "have", "left", "earlier"], ".", "should have＋過去分詞（後悔）"),
    ("あなたは傘を持ってくる必要はなかったのに。", ["you", "needn't", "have", "brought", "an umbrella"], ".", "needn't have＋過去分詞（実際にはしたが不要だった）"),
    ("この近くには以前、大きな池があった。", ["there", "used to", "be", "a big pond", "near here"], ".", "used to＋原形（以前の状態）"),
    ("あなたは今夜は外出しないほうがよい。", ["you", "had", "better", "not", "go out", "tonight"], ".", "had better not＋原形（not の位置）"),
    ("彼女はたぶん道に迷ったのだろう。", ["she", "may", "have", "lost", "her way"], ".", "may have＋過去分詞（過去の推量）"),
    ("私は早起きに慣れている。", ["I", "am", "used", "to", "getting up", "early"], ".", "be used to＋動名詞（～に慣れている）"),
    ("私はよく祖父と釣りに行ったものだ。", ["I", "would", "often", "go fishing", "with", "my grandfather"], ".", "would often＋原形（過去の反復的な動作）"),
    ("あなたが怒るのももっともだ。", ["you", "may", "well", "get", "angry"], ".", "may well＋原形（～するのももっともだ）"),
    ("あなたはその会議に出席する必要はありません。", ["you", "don't", "need", "to", "attend", "the meeting"], ".", "don't need to＋原形（一般動詞 need の否定）"),
]


@gen("standard_practice", 5, ["application", "computation"])
def build_order(r):
    jp, parts, end, point = r.choice(ORD)
    sent = " ".join(parts)
    sent = sent[0].upper() + sent[1:] + end
    return order(f"日本語に合うように、語句を並べかえて英文を完成させなさい。ただし、文頭にくる語も小文字で示してある。\n{jp}", parts,
                 f"{sent}　ポイント：{point}。", d=3,
                 ap="日本語の語尾（～にちがいない・～すべきだった・～したものだ など）から助動詞表現を決め、助動詞 → have → 過去分詞 などの固まりを先に作る。",
                 steps=[f"表現を決める：{point}。", "主語の後ろに助動詞の固まりを置く。", "残りの目的語・修飾語を並べる。", f"完成文：{sent}"],
                 alt=["完成した英文を和訳し直して、日本語の意味（推量・後悔・習慣など）と一致しているかを確かめる。"],
                 pc=[("助動詞表現の固まりを正しく作っている", 2), ("全体の語順が正しい", 2)],
                 pit=["had better not の not を had の後ろに置く。", "助動詞の後ろに過去形を置く。"])


SENSE = {
    "must": {"義務": ("「～しなければならない」（義務）", ["You must wear a helmet when you ride a motorbike.", "Students must turn off their phones in class.", "I must finish this report by noon."]),
             "推量": ("「～にちがいない」（推量）", ["She must be tired after the long trip.", "You must be Mr. Green. I've heard a lot about you.", "There must be some mistake in this bill."])},
    "may": {"許可": ("「～してもよい」（許可）", ["You may use my dictionary if you like.", "You may leave the room when you finish the test.", "Visitors may take pictures in this area."]),
            "推量": ("「～かもしれない」（推量）", ["It may snow tonight.", "He may be in the library now.", "The rumor may be true."])},
    "can": {"能力": ("「～できる」（能力）", ["She can swim very fast.", "My brother can speak three languages.", "This robot can climb stairs."]),
            "可能性": ("「～することがある・～でありうる」（可能性）", ["Even experts can make mistakes.", "It can be very cold here in winter.", "Driving at night can be dangerous."]),
            "許可": ("「～してもよい」（許可）", ["You can use this room after school.", "You can borrow my bike tomorrow."])},
    "should": {"義務": ("「～すべきだ」（義務・忠告）", ["You should apologize to her.", "We should save energy.", "You should take a rest."]),
               "推量": ("「～するはずだ」（推量）", ["The package should arrive tomorrow.", "He left an hour ago, so he should be home by now.", "It should be sunny tomorrow."])},
}


def underline(sent, word):
    toks = sent.split(" ")
    i = toks.index(word)
    toks[i] = f"[[u:{word}]]"
    return " ".join(toks)


@gen("standard_practice", 5, ["concept", "condition_check"])
def modal_sense(r):
    m = r.choice(list(SENSE))
    use = r.choice(list(SENSE[m]))
    label, pool = SENSE[m][use]
    tgt = r.choice(pool)
    rr = local(tgt)
    ok = rr.choice([s for s in pool if s != tgt])
    others = [(u, s) for u, (_, ps) in SENSE[m].items() if u != use for s in ps]
    wrongs = rr.sample(others, 3)
    why = {s: (f"この文の {m} は{SENSE[m][u][0]}の意味で、下線部（{label}）とは用法が異なる。", f"{m} の用法の取り違え") for u, s in wrongs}
    return mc(f"次の英文の下線部と同じ用法の {m} を含む英文を、選択肢から1つ選びなさい。\n{underline(tgt, m)}", [ok] + [s for _, s in wrongs],
              f"下線部の {m} は{label}。{ok} の {m} も同じ用法である。", d=3,
              ap=f"下線部の {m} を和訳して用法を決め、選択肢の {m} も同じように訳して比べる。後ろの動詞が be 動詞・状態動詞なら推量のことが多い。",
              steps=[f"下線部の {m} の意味を文脈から決める：{label}。", f"選択肢の {m} をそれぞれ和訳する。", f"同じ用法の {ok} を選ぶ。"],
              alt=["選択肢の助動詞を言いかえ表現（have to、be allowed to、be able to、It is possible that ～ など）に置きかえ、意味が通るかで用法を確かめる。"],
              pc=[("下線部の用法を正しく判断している", 2), ("同じ用法の文を選んでいる", 2)],
              pit=["主語が人なら義務・能力、と主語だけで判断する。", "後ろが be 動詞のときの推量の用法を見落とす。"],
              why=why)


# ======================================================================
# C 思考力・記述応用
# ======================================================================

PAIRS = [
    ("He must be rich.", "He must have been rich.",
     "Aは must＋原形で、現在のことについての推量「彼は金持ちにちがいない」。Bは must have＋過去分詞で、過去のことについての推量「彼は（当時）金持ちだったにちがいない」。どちらも判断しているのは今である。"),
    ("You should have called me.", "You must have called me.",
     "Aは should have＋過去分詞で、過去にしなかったことへの非難・後悔「電話してくれればよかったのに（実際はしなかった）」。Bは must have＋過去分詞で、過去のことについての推量「あなたは私に電話したにちがいない」。"),
    ("You needn't have come.", "You didn't need to come.",
     "Aは needn't have＋過去分詞で「来る必要はなかったのに（実際には来た）」。Bは didn't need to＋原形で「来る必要はなかった」という過去の不必要を述べるだけで、実際に来たかどうかは文脈によって決まる。"),
    ("I used to drink coffee.", "I am used to drinking coffee.",
     "Aは used to＋原形で「以前はコーヒーを飲んでいた（今は飲んでいない）」という過去の習慣。Bは be used to＋動名詞で「コーヒーを飲むことに慣れている」という現在の状態。Bの to は前置詞なので後ろが動名詞になる。"),
    ("You must not go.", "You don't have to go.",
     "Aは must not で「行ってはならない」という禁止。Bは don't have to で「行く必要はない（行っても行かなくてもよい）」という不必要。must の否定と have to の否定は意味が大きく異なる。"),
    ("He can't be busy.", "He may not be busy.",
     "Aは can't で「彼が忙しいはずがない」という強い否定の推量。Bは may not で「彼は忙しくないかもしれない」という弱い推量で、忙しい可能性も残っている。"),
    ("She may have left.", "She should have left.",
     "Aは may have＋過去分詞で「彼女は出発したかもしれない」という過去についての推量。Bは should have＋過去分詞で「彼女は出発すべきだったのに（実際はしなかった）」という非難・後悔（文脈によっては「もう出発したはずだ」という推量の意味にもなる）。"),
    ("I would often swim in the river.", "I used to live near the river.",
     "Aの would は過去の反復的な動作を表し「よく川で泳いだものだ」。Bの used to は「以前は川の近くに住んでいた（今はちがう）」という過去の状態を表す。live のような状態を表す動詞には would は使えないので、Bでは used to を使っている。"),
    ("You had better leave now.", "You should leave now.",
     "Aは had better で「今出発したほうがいい（さもないと困ったことになる）」という警告を含む強い忠告。Bは should で「今出発すべきだ」という一般的な助言。had better は強い響きがあるので、目上の人に対しては使わないのがふつうである。"),
]


@gen("thinking_writing", 4, ["written_reasoning", "concept"])
def explain_difference(r):
    a, b, model = r.choice(PAIRS)
    return desc(f"次の2つの英文A・Bの意味の違いを、助動詞の働きに触れながら日本語で説明しなさい。\nA：{a}\nB：{b}", model,
                "助動詞の違いは「推量か、義務・忠告・後悔か」「現在のことか、過去のことか」「確信の度合い」の観点で説明できる。",
                [("Aの助動詞表現の働きを正しく説明している", 3), ("Bの助動詞表現の働きを正しく説明している", 3), ("A・Bの意味の違いを和訳などで明確に示している", 2)], d=4, p=8, lines=6,
                ap="2文で異なる部分（助動詞・have＋過去分詞・to の後ろの形など）に注目し、それぞれ「何についての判断か」「いつのことか」を整理する。",
                steps=["A・Bで形が異なる部分を確認する。", "それぞれの意味（推量・義務・不必要・後悔・習慣など）と時（現在・過去）を判断する。", "意味の違いを和訳とともに説明する。"],
                alt=["それぞれの文に続く文を考えると違いがはっきりする（例：You needn't have come. の後には But thank you for coming. が続けられる）。"],
                pc=[("Aの説明", 3), ("Bの説明", 3), ("意味の違いの明示", 2)],
                pit=["和訳だけを並べ、助動詞の働きに触れない。", "must have（推量）と should have（後悔）の違いを説明できない。"])


FACT = [
    ("You should have taken the medicine.", "You didn't take the medicine.", "should have＋過去分詞は「～すべきだったのに」で、実際にはしなかったことを表す。"),
    ("I could have caught the train if I had left earlier.", "I didn't catch the train because I didn't leave earlier.", "仮定法過去完了の帰結節の could have＋過去分詞は「～できただろうに」で、過去の事実とは反対の内容を表す。"),
    ("You needn't have bought so much food.", "You bought so much food, but it wasn't necessary.", "needn't have＋過去分詞は「～する必要はなかったのに」で、実際にはしたことを表す。"),
    ("If he had been more careful, he wouldn't have had the accident.", "He had the accident because he wasn't careful enough.", "仮定法過去完了の帰結節の wouldn't have＋過去分詞は「～しなかっただろうに」で、過去の事実（事故にあった）とは反対の内容を表す。"),
    ("She might have won the race if she hadn't fallen.", "She fell, so she didn't win the race.", "仮定法過去完了の帰結節の might have＋過去分詞は「～したかもしれない」で、過去の事実（勝てなかった）とは反対の内容を表す。"),
    ("We ought to have reserved a table.", "We didn't reserve a table.", "ought to have＋過去分詞は should have＋過去分詞と同じく「～すべきだったのに」で、実際にはしなかったことを表す。"),
    ("I would have helped you if you had asked me.", "You didn't ask me, so I didn't help you.", "仮定法過去完了の帰結節の would have＋過去分詞は「～しただろうに」で、過去の事実（手伝わなかった）とは反対の内容を表す。"),
]


@gen("thinking_writing", 3, ["cross_unit", "written_reasoning"], rel=["HS-ENG-U08", "HS-ENG-U02"])
def fact_rewrite(r):
    s, fact, why = r.choice(FACT)
    return desc(f"次の英文が前提としている過去の事実を、直説法（事実を述べる文）の英文で書きなさい。また、助動詞＋have＋過去分詞の表現が表している意味を説明しなさい。\n{s}",
                f"{fact}　{why}", f"助動詞＋have＋過去分詞のうち、should / ought to / needn't have や、仮定法過去完了の would / could / might have は、過去の事実を前提にしている。{why}",
                [("前提となる過去の事実を、正しい時制の英文で書いている", 4), ("助動詞＋have＋過去分詞の意味（後悔・不必要・事実に反する仮定の帰結）を説明している", 3), ("事実と表現の関係（反対の内容か、実際にしたことか）を明確にしている", 1)], d=4, p=8, lines=5,
                ap="助動詞＋have＋過去分詞の部分が「実際にはしなかった」ことを表すのか、「実際にはした」ことを表すのかを判断し、それを過去形の肯定文・否定文で書く。if 節が過去完了なら仮定法過去完了（時制の単元で学んだ過去完了の形）である。",
                steps=["助動詞＋have＋過去分詞の部分と、if 節があればその時制を確認する。", "その表現が前提とする事実（実際にした・しなかった）を判断する。", f"事実を過去形の英文で書く：{fact}", "表現の意味を説明する。"],
                alt=["書いた事実の文と元の英文を和訳して並べ、「～すべきだったのに → しなかった」「～しただろうに → しなかった」のように意味が反対になっているかを確かめる。"],
                pc=[("事実の英文", 4), ("表現の意味の説明", 3), ("事実との関係", 1)],
                pit=["needn't have＋過去分詞を「しなかった」と誤解する。", "事実の文を過去完了や仮定法のまま書いてしまう。"])


SITU = [
    ("The streets are wet this morning, but the sky is clear now.", "rain", "It must have rained during the night.",
     "道がぬれているという根拠から、過去（夜の間）のことを強く推量するので must have＋過去分詞。"),
    ("Tom got a perfect score on the math test. He says he didn't study at all, but you don't believe him.", "study", "Tom must have studied hard for the test.",
     "満点をとったという根拠から、勉強したと強く推量するので must have＋過去分詞。"),
    ("Emi's light is off and she isn't answering her phone. You are not sure why.", "go to bed", "She may have gone to bed already.",
     "理由がはっきりしない（ほかの可能性もある）ので、弱い推量の may（might）have＋過去分詞。"),
    ("Ken was with you in the library all afternoon. Someone says that he broke a window at school this afternoon.", "break", "Ken can't have broken the window.",
     "午後ずっと図書館にいっしょにいたという根拠から、ありえないと強く否定するので can't have＋過去分詞。"),
    ("You took a taxi to the station, but your train was an hour late.", "take", "I needn't have taken a taxi.",
     "実際にタクシーに乗ったが、電車が遅れたので急ぐ必要はなかったので needn't have＋過去分詞。"),
    ("You didn't bring an umbrella, and now it's raining hard.", "bring", "I should have brought an umbrella.",
     "実際には持ってこなかったことを悔やんでいるので should have＋過去分詞。"),
    ("The door was locked when you went out, but now it is open. Only your sister has a key.", "open", "My sister must have opened the door.",
     "かぎを持っているのは妹（姉）だけという根拠から強く推量するので must have＋過去分詞。"),
]


@gen("thinking_writing", 3, ["application", "condition_check"])
def situation_writing(r):
    s, verb, model, why = r.choice(SITU)
    return desc(f"次の状況を読み、（　）内の語句を使って、過去のことについての判断（推量・後悔など）を表す英文を1文で書きなさい。また、その助動詞を選んだ理由を説明しなさい。\n{s}　（{verb}）",
                f"{model}　{why}", why,
                [("状況に合う助動詞＋have＋過去分詞の英文を書いている", 4), ("助動詞を選んだ理由（根拠の強さ・実際にしたかどうか）を説明している", 3), ("動詞の過去分詞の形が正しい", 1)], d=4, p=8, lines=5,
                ap="状況の文から「根拠の強さ」（強い・弱い・ありえない）と、「話し手自身の行動への後悔・評価か」を読み取り、must / may / can't / should / needn't have の中から選ぶ。",
                steps=["状況の中の根拠や事実に下線を引く。", "推量（強い・弱い・否定）か、後悔・評価かを判断する。", "助動詞＋have＋過去分詞の形で英文を書く。", f"解答例：{model}"],
                alt=["同じ状況を、It is certain that ～ / It is possible that ～ / It is impossible that ～ などの言いかえで考えてから、助動詞の文に戻す。"],
                pc=[("英文", 4), ("理由の説明", 3), ("過去分詞の形", 1)],
                pit=["過去のことなのに助動詞＋原形で書く。", "根拠が強いのに may を使う、または根拠が弱いのに must を使う。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(task, wrong, step, etype, tempt, fix, ans, expl, steps, ap, alt, pit, d=3):
    return desc(f"{task}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい英文に書き直しなさい。", ans, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい英文に直している", 3), ("助動詞の規則を説明している", 1)], d=d, p=6, lines=5,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい英文", 3), ("規則の説明", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix))


HPP_ERR = [
    ("彼は約束を忘れたにちがいない。", "He must forgot our promise.", "He must have forgotten our promise.", "must forgot", "notation",
     "助動詞の後ろは原形。過去のことの推量は must have＋過去分詞で表す。", "「忘れた」という過去の内容なので、動詞を過去形にした。"),
    ("彼女がそれを知っていたはずがない。", "She can't knew it.", "She can't have known it.", "can't knew", "notation",
     "助動詞の後ろは原形。過去のことについての否定の推量は can't have＋過去分詞で表す。", "「知っていた」という過去の内容なので、動詞を過去形にした。"),
    ("あなたはもっと注意すべきだったのに。", "You must have been more careful.", "You should have been more careful.", "must have", "concept",
     "must have＋過去分詞は「～したにちがいない」という推量。「～すべきだったのに」という非難・後悔は should have＋過去分詞。", "must に「～しなければならない」の意味があるので、「～すべきだった」にも使えると考えた。"),
    ("彼はバスに乗り遅れたのかもしれない。", "He may missed the bus.", "He may have missed the bus.", "may missed", "notation",
     "助動詞の後ろは原形。過去のことの推量は may have＋過去分詞で表す。", "「乗り遅れた」という過去の内容なので、動詞を過去形にした。"),
    ("そんなに急ぐ必要はなかったのに。", "You must not have hurried so much.", "You needn't have hurried so much.", "must not have", "concept",
     "「（実際にはしたが）～する必要はなかったのに」は needn't have＋過去分詞。must not は禁止を表す。", "「～しなくてよかった」を「～してはならなかった」と取り違えた。"),
    ("昨夜は雨が降ったにちがいない。", "It must be rained last night.", "It must have rained last night.", "must be rained", "notation",
     "過去のことの推量は must have＋過去分詞。be＋過去分詞にすると受け身になってしまう。", "have と be のどちらを使うかをあいまいに覚えていた。"),
    ("あなたはそのとき本当のことを言うべきだった。", "You should had told the truth then.", "You should have told the truth then.", "should had", "notation",
     "助動詞の後ろは原形なので、have を had にはしない。should have＋過去分詞。", "過去のことなので have も過去形 had にしなければならないと考えた。"),
]


@gen("error_correction", 4, ["common_error", "computation"])
def err_have_pp(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(HPP_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", etype, tempt, fix, fix, f"{rule}正しくは {fix}",
                    ["判断の種類（推量・後悔・不必要）を日本語から決める。", "過去のことなので助動詞＋have＋過去分詞の形にする（助動詞の後ろは原形）。", f"正しい英文：{fix}"],
                    "「判断は今、出来事は過去」なので、助動詞はそのまま、後ろを have＋過去分詞にする。助動詞の種類で推量か後悔かが決まる。",
                    ["時間軸に「判断の時点（今）」と「出来事の時点（過去）」をかき、助動詞と have＋過去分詞がそれぞれどちらを表しているかを確かめる。"],
                    ["助動詞の後ろに過去形を置く。", "must have と should have の意味を取り違える。"], d=3)


USED_ERR = [
    ("私は早起きに慣れている。", "I used to get up early.", "I am used to getting up early.", "used to get", "concept",
     "「～に慣れている」は be used to＋動名詞。used to＋原形は「以前は～したものだ」の意味になる。", "used to という同じ語句が含まれるので、be 動詞と動名詞を落とした。"),
    ("以前ここに図書館があった。", "There would be a library here.", "There used to be a library here.", "would be", "concept",
     "be（ある）は状態を表すので、過去の習慣の would は使えない。過去の状態は used to＋原形で表す。", "would にも「以前は～したものだ」の意味があるので、状態にも使えると考えた。"),
    ("父はコーヒーを飲むことに慣れていない。", "My father isn't used to drink coffee.", "My father isn't used to drinking coffee.", "drink", "notation",
     "be used to の to は前置詞なので、後ろは動名詞（drinking）にする。", "to の後ろは原形という不定詞の規則を当てはめた。"),
    ("子どものころ、私はよく川で泳いだものだ。", "I was used to swim in the river when I was a child.", "I used to swim in the river when I was a child.", "was used to swim", "concept",
     "過去の習慣は used to＋原形（または would often＋原形）。was used to は「～に慣れていた」で、後ろに原形は続かない。", "過去のことなので、used to に be 動詞の過去形をつけた。"),
    ("あなたはすぐに新しい生活に慣れるでしょう。", "You will soon get use to your new life.", "You will soon get used to your new life.", "get use to", "notation",
     "「～に慣れる」は get used to＋名詞で、use は過去分詞 used にする。", "発音が同じなので、つづりの d を落とした。"),
    ("私は以前、東京に住んでいた。", "I would live in Tokyo.", "I used to live in Tokyo.", "would live", "concept",
     "live は状態を表す動詞なので、過去の習慣の would は使えない。used to＋原形で表す。", "would にも「以前は～したものだ」の意味があるので、どの動詞にも使えると考えた。"),
]


@gen("error_correction", 3, ["common_error", "condition_check"])
def err_used_to(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(USED_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", etype, tempt, fix, fix, f"{rule}正しくは {fix}",
                    ["日本語の意味（以前は～した／よく～した／慣れている）を確かめる。", "used to＋原形、would＋原形（動作のみ）、be used to＋名詞・動名詞のどれが合うかを決める。", f"正しい英文：{fix}"],
                    "used to / would / be used to は、意味（過去の習慣・状態か、慣れか）と、後ろの形（原形か動名詞か）、動作か状態か、の3点で区別する。",
                    ["to の後ろに名詞を置いても意味が通るか（前置詞の to か）を確かめる。"],
                    ["be used to の後ろに原形を置く。", "状態を表す動詞に would を使う。"], d=3)


NEED_ERR = [
    ("あなたは来る必要はない。", "You need not to come.", "You need not come.", "need not to", "notation",
     "助動詞の need は後ろに原形をとるので to は不要（一般動詞なら You don't need to come.）。", "一般動詞の need to と助動詞の need not を混ぜてしまった。"),
    ("明日は学校に来なくてもよい。", "You must not come to school tomorrow.", "You don't have to come to school tomorrow.", "must not", "concept",
     "must not は「～してはならない」という禁止。「～しなくてもよい」は don't have to（または need not）。", "must＝have to なので、否定も同じ意味になると考えた。"),
    ("彼はそこに行かなければならなかった。", "He must went there.", "He had to go there.", "must went", "notation",
     "must には過去形がないので、過去の義務は had to＋原形で表す。助動詞の後ろに過去形は置けない。", "過去のことなので、動詞を過去形にすればよいと考えた。"),
    ("あなたはその本を読む必要がありますか。", "Do you need read the book?", "Do you need to read the book?", "need read", "notation",
     "do を使った疑問文では need は一般動詞なので、need to＋原形にする（Need you read the book? も可）。", "助動詞 need の形（後ろに原形）と、一般動詞の疑問文の形を混ぜてしまった。"),
    ("今夜は外出しないほうがよい。", "You had not better go out tonight.", "You had better not go out tonight.", "had not better", "notation",
     "had better の否定は had better not＋原形で、not は better の後ろに置く。", "ふつうの助動詞と同じように、最初の語 had の後ろに not を置いた。"),
    ("彼女は来週までにそれを終えなければならないだろう。", "She will must finish it by next week.", "She will have to finish it by next week.", "will must", "notation",
     "助動詞を2つ並べることはできないので、未来の義務は will have to＋原形で表す。", "「～だろう（will）」と「～しなければならない（must）」を、そのまま並べた。"),
    ("あなたはもっと野菜を食べるべきだ。", "You ought eat more vegetables.", "You ought to eat more vegetables.", "ought eat", "notation",
     "ought は ought to＋原形の形で使い、to を省略できない。", "should と同じように、ought の後ろにすぐ原形を置いた。"),
]


@gen("error_correction", 3, ["common_error", "condition_check"])
def err_need_must(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(NEED_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", etype, tempt, fix, fix, f"{rule}正しくは {fix}",
                    ["日本語の意味（禁止・不必要・義務・忠告）を確かめる。", "その意味を表す表現と、後ろに続く形（原形・to 不定詞）を確かめる。", f"正しい英文：{fix}"],
                    "助動詞の後ろは原形、助動詞は2つ並べない、ought to・have to・had better not の形は固定、の3つの規則に照らして点検する。",
                    ["正しい英文を否定文・疑問文・過去形に変えてみて、それぞれの形が規則どおりに作れるかを確かめる。"],
                    ["must not（禁止）と don't have to（不必要）を混同する。", "助動詞を2つ並べる。"], d=3)


GENERATORS = [modal_infer, have_pp_meaning, used_to, modal_form,
              rewrite, have_pp_context, build_order, modal_sense,
              explain_difference, fact_rewrite, situation_writing,
              err_have_pp, err_used_to, err_need_must]
